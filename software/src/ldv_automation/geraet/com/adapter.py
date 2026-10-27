"""COM-Adapter :class:`PsvComGeraet`: setzt ``Messgeraet`` für die PSV-Software um.

Ablauf und Belege: Plan P2, Abschnitt 3 (V0-M12), Analysebericht I5 Abschnitt 3. Jeder
COM-Zugriff läuft über den Whitelist-Proxy mit der Produktiv-Richtlinie (ADR-007); der
Adapter hält selbst keine rohen COM-Objekte.

Fehlerübersetzung (Vertrag ``Messgeraet``):

* ``PermissionError`` des Proxys (Default deny) → :class:`VerweigertFehler`.
* :class:`~.whitelist.ComFehler` (COM-Ausnahme) → :class:`GeraeteFehler` mit Methode
  (``Typ.Mitglied``), Argumenten, ``hresult`` und ``excepinfo``.

Unbestätigte COM-Annahmen (Montag, Plan P2 Abschnitt 9) sind Konfiguration:

* ``validator_rueckfall_direkt`` (S4): ohne Validator direkt ``FftProperties`` setzen.
* ``lademaske``: Maske für ``Settings.Load``.
* ``start_psv_erlaubt``: ``GetApplication(True, …)`` (nur mit ``--start-psv`` und ``JA``).
* Der Ereignisbetrieb (``--ereignisse``) und ``--fortschritt punktstatus`` sind nicht
  umgesetzt (Streichliste Plan P2, Abschnitt 8): :meth:`PsvComGeraet.fortschritt` liefert
  ``None``, :meth:`PsvComGeraet.hole_meldungen` ein leeres Tupel.
"""

from __future__ import annotations

import enum
import functools
import os.path
import time
from collections.abc import Callable, Collection, Iterator, Mapping
from contextlib import contextmanager
from dataclasses import dataclass, field
from typing import ParamSpec, TypeVar

from ldv_automation.domaene.parameter import KATALOG, Parameterkatalog, ParameterWert
from ldv_automation.geraet.com.bindung import ComBindung
from ldv_automation.geraet.com.konstanten import (
    ACQ_MODE_NAMEN,
    AVERAGE_TYPE_NAMEN,
    SCAN_ZUSTAENDE,
    AcqMode,
    AcqState,
    ApplicationMode,
    AverageType,
    ScanCaps,
    ScanMode,
    lademaske_text,
)
from ldv_automation.geraet.com.richtlinie import (
    PROGID_ACQUISITION_INSTANCE,
    STANDARD_LADEMASKE,
    erstelle_richtlinie,
    ganzzahl_oder_none,
    pfad_unter,
)
from ldv_automation.geraet.com.whitelist import (
    Aufruf,
    ComFehler,
    ProxyKontext,
    Verweigerung,
    WhitelistProxy,
    com_details,
    oeffne,
)
from ldv_automation.geraet.schnittstelle import (
    AbweichungFehler,
    EinstellungsStand,
    EinstellungsWert,
    Fortschritt,
    GeraeteFehler,
    GeraeteInfo,
    GeraeteZustand,
    GeraetNichtBereitFehler,
    Meldung,
    VerweigertFehler,
)

START_ZEITLIMIT_MS = 30000
"""``GetApplication(True, …)``-Zeitlimit in ms (wie Erkundung, I5 Abschnitt 10, P1-5)."""

MAX_KANAELE = 16
"""Obergrenze gelesener Kanäle im Einstellungsstand (Ressourcenschranke)."""

_P = ParamSpec("_P")
_R = TypeVar("_R")


class ComBetriebsart(enum.Enum):
    """Betriebsart des Adapters (Plan P2, Abschnitt 6; ``SIMULATOR`` betrifft ihn nicht)."""

    NUR_LESEN = "nur_lesen"
    """Verbinden und Lesen; keine Schreibzugriffe (nur S1 mit ``--start-psv``)."""
    TROCKENLAUF = "trockenlauf"
    """Zusätzlich S2-S5 und S9; kein ``ScanFileName``, ``ScanEx``, ``Stop``."""
    MESSEN = "messen"
    """Voller Ablauf S2-S9 (``ScanEx`` zusätzlich nur mit Messfreigabe)."""


@dataclass(frozen=True, kw_only=True)
class ComKonfiguration:
    """Konfiguration des Adapters (je Rechner bzw. Sitzung).

    Parameters
    ----------
    betriebsart : ComBetriebsart
        Fest für die Lebensdauer des Adapters; Umschalten heißt neu konstruieren.
    messdaten_wurzel : str or None
        Wurzelordner, unter dem Scandateien (``.svd``) und Nachweise (``.set``) liegen
        dürfen. Pflicht für Trockenlauf (S9) und Messen.
    start_psv_erlaubt : bool
        ``--start-psv`` mit getipptem ``JA``; sonst wird PSV nie gestartet.
    start_zeitlimit_ms : int
        Zeitlimit für ``GetApplication(True, …)`` in ms.
    lademaske : int
        ``PTCSettings``-Maske für ``Settings.Load`` (Prüfung in S2).
    validator_rueckfall_direkt : bool
        Schalter S4: ohne ``FftAcqPropertiesValidator`` direkt über ``FftProperties``
        setzen. Standard aus, bis Erkundung E1 das Fehlen des Validators zeigt.
    katalog : Parameterkatalog
        Parameterkatalog (Schlüssel und Bereiche).
    existiert : callable or None
        Existenzprüfung für Pfade (Tests); ``None`` = ``os.path.lexists``.
    uhr : callable
        Monotone Uhr in s.
    """

    betriebsart: ComBetriebsart
    messdaten_wurzel: str | None = None
    start_psv_erlaubt: bool = False
    start_zeitlimit_ms: int = START_ZEITLIMIT_MS
    lademaske: int = STANDARD_LADEMASKE
    validator_rueckfall_direkt: bool = False
    katalog: Parameterkatalog = field(default=KATALOG)
    existiert: Callable[[str], bool] | None = None
    uhr: Callable[[], float] = time.monotonic


@dataclass(frozen=True)
class _Zuordnung:
    gruppe: str
    property: str


_PARAMETER: dict[str, _Zuordnung] = {
    "fft.bandbreite_hz": _Zuordnung("fft", "Bandwidth"),
    "fft.linien": _Zuordnung("fft", "Lines"),
    "mittelung.anzahl": _Zuordnung("mittelung", "Count"),
    "mittelung.typ": _Zuordnung("mittelung", "Type"),
}
"""Katalogschlüssel → COM-Property (Gruppe nach ``ParameterSpec.com_gruppe``)."""

# Einstellungsstand: (COM-Property, Schlüssel mit Einheit). Einheiten nach I5 2.5.
_FFT_STAND = (
    ("Bandwidth", "bandbreite_hz"),
    ("StartFrequency", "start_frequenz_hz"),
    ("EndFrequency", "end_frequenz_hz"),
    ("Lines", "linien"),
    ("Overlap", "ueberlappung_prozent"),
    ("SampleFrequency", "abtastfrequenz_hz"),
    ("SampleResolution", "aufloesung_hz"),
    ("SampleTime", "messzeit_s"),
)
_MITTELUNG_STAND = (("Type", "typ"), ("Count", "anzahl"))
_ALLGEMEIN_STAND = (
    ("AutoRemeasure", "auto_nachmessen"),
    ("AutoRemeasureAutoRange", "auto_nachmessen_bereich"),
    ("SaveTimeDataForScan", "zeitdaten_speichern"),
    ("PrincipalComponentAnalysis", "pca"),
)
_TRIGGER_STAND = (
    ("Source", "quelle"),
    ("Edge", "flanke"),
    ("Level", "pegel_prozent"),
    ("PreTrigger", "vortrigger_prozent"),
    ("PhaseFromRef", "phase_aus_referenz"),
    ("AnalogSourceChannel", "analog_quellkanal"),
)
_SE_STAND = (("Mode", "modus"), ("SpeckleTracking", "speckle_tracking"))
_KANAL_STAND = (
    ("Name", "name"),
    ("Active", "aktiv"),
    ("Reference", "referenz"),
    ("Quantity", "groesse"),
    ("Unit", "einheit"),
    ("InputRange", "eingangsbereich_v"),
    ("Calibration", "kalibrierfaktor_si_je_v"),
    ("DirectionOfVibration", "schwingrichtung"),
    ("WindowFunction", "fensterfunktion"),
)
_HARDWARE = (
    ("AcqBoardName", "erfassungskarte"),
    ("AcqBoardFirmwareVersion", "erfassungskarte_firmware"),
    ("FrontEnd", "frontend"),
    ("FrontEndFirmwareVersion", "frontend_firmware"),
    ("GeneratorName", "generator"),
    ("ScanHeadType", "scankopf_typ"),
    ("SensorHeadNames", "sensorkoepfe"),
    ("SensorHeadSerialNumbers", "sensorkopf_seriennummern"),
    ("SensorHeadVersions", "sensorkopf_versionen"),
)


def _einstellungswert(wert: object) -> EinstellungsWert:
    """COM-Wert → JSON-fähiger Wert (float64; Tupel als Text)."""
    if wert is None or isinstance(wert, bool | int | str):
        return wert
    if isinstance(wert, float):
        return float(wert)
    return repr(wert)


def _als_ganzzahl(wert: object, pfad: str) -> int:
    zahl = ganzzahl_oder_none(wert)  # gleiche Regel wie S7 (ganzzahliger float zulässig)
    if zahl is not None:
        return zahl
    raise GeraeteFehler(f"{pfad}: Ganzzahl erwartet, erhalten {wert!r}", methode=pfad)


def _als_float(wert: object, pfad: str) -> float:
    if isinstance(wert, int | float) and not isinstance(wert, bool):
        return float(wert)
    raise GeraeteFehler(f"{pfad}: Zahl erwartet, erhalten {wert!r}", methode=pfad)


def _gleicher_pfad(a: str, b: str) -> bool:
    return os.path.normcase(os.path.normpath(a)) == os.path.normcase(os.path.normpath(b))


@contextmanager
def _uebersetze(methode: str) -> Iterator[None]:
    """Übersetzt Proxy- und COM-Ausnahmen in die Fehler der Geräteschnittstelle."""
    try:
        yield
    except GeraeteFehler:
        raise
    except PermissionError as exc:
        raise VerweigertFehler(str(exc), methode=methode) from exc
    except ComFehler as exc:
        raise GeraeteFehler(
            exc.text,
            methode=exc.pfad,
            argumente=exc.argumente,
            hresult=exc.hresult,
            excepinfo=exc.excepinfo,
        ) from exc


def _geraeteaufruf(fn: Callable[_P, _R]) -> Callable[_P, _R]:
    @functools.wraps(fn)
    def huelle(*args: _P.args, **kwargs: _P.kwargs) -> _R:
        with _uebersetze(fn.__name__):
            return fn(*args, **kwargs)

    return huelle


class PsvComGeraet:
    """``Messgeraet`` über COM (pywin32, Late Binding, Polling).

    Parameters
    ----------
    bindung : ComBindung
        COM-Laufzeit (:class:`~.pywin32_bindung.Pywin32Bindung` bzw. Attrappe in Tests).
    konfiguration : ComKonfiguration
        Betriebsart, Wurzelordner, Schalter für unbestätigte COM-Annahmen.

    Notes
    -----
    Alle Methoden außer :meth:`haengender_aufruf_seit_s`, :meth:`aufrufe`,
    :meth:`verweigerungen`, :meth:`aufrufe_anzahl` und :meth:`verweigerungen_text` sind nur
    aus dem Geräte-Thread aufzurufen (ADR-008).
    """

    def __init__(self, bindung: ComBindung, konfiguration: ComKonfiguration) -> None:
        self._bindung = bindung
        self._konf = konfiguration
        art = konfiguration.betriebsart
        self._kontext = ProxyKontext(
            start_erlaubt=konfiguration.start_psv_erlaubt,
            schreiben_erlaubt=art in (ComBetriebsart.TROCKENLAUF, ComBetriebsart.MESSEN),
            messen_erlaubt=art is ComBetriebsart.MESSEN,
            direkt_setzen_erlaubt=konfiguration.validator_rueckfall_direkt,
            messdaten_wurzel=konfiguration.messdaten_wurzel,
            existiert=konfiguration.existiert,
            uhr=konfiguration.uhr,
        )
        self._app: WhitelistProxy | None = None
        self._acq: WhitelistProxy | None = None
        self._info: GeraeteInfo | None = None
        self._thread_initialisiert = False
        self._psv_prozesse: tuple[str, ...] | None = None
        self._richtlinie = erstelle_richtlinie(konfiguration.katalog)

    # --- Zusatz für Sitzung und Protokoll ------------------------------------------------

    @property
    def betriebsart(self) -> ComBetriebsart:
        """Betriebsart (fest seit der Konstruktion)."""
        return self._konf.betriebsart

    @property
    def lademaske(self) -> int:
        """``PTCSettings``-Maske, mit der :meth:`lade_einstellungen` lädt (Protokoll)."""
        return self._konf.lademaske

    @property
    def psv_prozesse(self) -> tuple[str, ...] | None:
        """Abbildnamen der PSV-Treffer der letzten Prozessprüfung (``None``: nicht lesbar).

        Annahme [ungeprüft]: Nur PSV selbst enthält „psv“ (siehe
        :data:`~.bindung.PSV_PROZESS_KENNUNG`); Erkundung Stufe 0 prüft das.
        """
        return self._psv_prozesse

    def _bindungsaufruf(self, methode: str, fn: Callable[[], _R]) -> _R:
        """Ruft die COM-Laufzeit außerhalb des Proxys auf (Wächter, Fehlerübersetzung)."""
        with self._kontext.ueberwache():
            try:
                return fn()
            except Exception as exc:  # roh: ImportError, com_error, OSError ...
                hresult, excepinfo, text = com_details(exc)
                raise GeraeteFehler(
                    f"{methode}: {text}", methode=methode, hresult=hresult, excepinfo=excepinfo
                ) from exc

    def aufrufe(self) -> tuple[Aufruf, ...]:
        """Aufrufprotokoll aller weitergereichten COM-Zugriffe (thread-sicher)."""
        return self._kontext.aufrufe()

    def verweigerungen(self) -> tuple[Verweigerung, ...]:
        """Alle verweigerten Zugriffsversuche (thread-sicher; am Gerät erwartet: leer)."""
        return self._kontext.verweigerungen()

    def aufrufe_anzahl(self) -> int:
        """Anzahl der weitergereichten COM-Zugriffe (thread-sicher; Diagnose der Sitzung)."""
        return self._kontext.anzahl_aufrufe()

    def verweigerungen_text(self) -> tuple[str, ...]:
        """Verweigerte Zugriffe als Text ``Pfad (op): Grund`` (thread-sicher; Diagnose T1)."""
        return tuple(f"{v.pfad} ({v.op}): {v.grund}" for v in self._kontext.verweigerungen())

    # --- interne Helfer ------------------------------------------------------------------

    def _verbunden(self) -> tuple[WhitelistProxy, WhitelistProxy, GeraeteInfo]:
        if self._app is None or self._acq is None or self._info is None:
            raise GeraeteFehler("Nicht mit PSV verbunden (zuerst verbinde())")
        return self._app, self._acq, self._info

    def _verlange_schreiben(self, methode: str) -> None:
        _, _, info = self._verbunden()
        if not self._kontext.schreiben_erlaubt:
            raise VerweigertFehler(
                f"Betriebsart {self.betriebsart.value} erlaubt keine Schreibzugriffe",
                methode=methode,
            )
        if not info.meldungen_unterdrueckt:
            raise VerweigertFehler(
                "SuppressMessagesForAutomation ist False: Schreib- und Messbetrieb gesperrt; "
                "in PSV aktivieren",
                methode=methode,
            )
        if not info.erfassungsmodus:
            raise VerweigertFehler("PSV ist nicht im Erfassungsmodus", methode=methode)

    def _lies_zustand_roh(self) -> AcqState:
        _, acq, _ = self._verbunden()
        wert = acq.State
        try:
            return AcqState(_als_ganzzahl(wert, "Acquisition.State"))
        except ValueError:
            raise GeraeteFehler(
                f"Unbekannter Acquisition.State {wert!r}", methode="Acquisition.State"
            ) from None

    def _verlange_gestoppt(self, methode: str) -> None:
        zustand = self._lies_zustand_roh()
        if zustand is not AcqState.STOPPED:
            raise GeraetNichtBereitFehler(
                f"PSV ist nicht bereit (State {zustand.name}); fremde Messung wird nicht angefasst",
                methode=methode,
            )

    def _eigenschaften(self) -> WhitelistProxy:
        _, acq, _ = self._verbunden()
        props: WhitelistProxy | None = acq.ActiveProperties
        if props is None:
            raise GeraeteFehler("ActiveProperties nicht verfügbar", methode="ActiveProperties")
        return props

    def _gruppe(self, props: WhitelistProxy, gruppe: str) -> WhitelistProxy:
        name, has = {
            "fft": ("FftProperties", "HasFftProperties"),
            "mittelung": ("AverageProperties", "HasAverageProperties"),
        }[gruppe]
        if getattr(props, has) is not True:
            raise GeraeteFehler(
                f"Einstellungsgruppe {name} im aktiven Modus nicht vorhanden",
                methode=f"AcquisitionProperties.{has}",
            )
        obj: WhitelistProxy | None = getattr(props, name)
        if obj is None:
            raise GeraeteFehler(f"{name} nicht verfügbar", methode=f"AcquisitionProperties.{name}")
        return obj

    def _zuordnung(self, schluessel: str) -> _Zuordnung:
        try:
            self._konf.katalog.spec(schluessel)
        except ValueError as exc:
            raise GeraeteFehler(str(exc), methode="setze_parameter") from None
        zuordnung = _PARAMETER.get(schluessel)
        if zuordnung is None:
            raise GeraeteFehler(
                f"Parameter '{schluessel}' hat keine COM-Zuordnung im Adapter",
                methode="setze_parameter",
            )
        return zuordnung

    # --- Messgeraet ----------------------------------------------------------------------

    @_geraeteaufruf
    def verbinde(self) -> GeraeteInfo:
        """V0/V1: Prozessprüfung, ``Dispatch``, ``GetApplication``, Version, Modus, Zustand.

        Raises
        ------
        GeraeteFehler
            Wenn PSV nicht läuft (ohne ``--start-psv``) oder die Verbindung scheitert. Meldet
            die Prozessprüfung kein PSV (oder ist sie nicht lesbar), gibt es **keinen**
            ``Dispatch`` (COM könnte PSV als ``LocalServer32`` sonst selbst starten).
        """
        if self._app is not None:
            return self._verbunden()[2]
        start_erlaubt = self._konf.start_psv_erlaubt
        treffer = self._bindungsaufruf("psv_prozesse", self._bindung.psv_prozesse)
        self._psv_prozesse = treffer
        if not treffer and not start_erlaubt:
            grund = "nicht ermittelbar" if treffer is None else "kein PSV-Prozess gefunden"
            raise GeraeteFehler(
                f"Prozessprüfung: {grund}. PSV im Erfassungsmodus starten (Start durch dieses "
                "Programm nur mit --start-psv)",
                methode="verbinde",
            )
        if not self._thread_initialisiert:
            self._bindungsaufruf("initialisiere_thread", self._bindung.initialisiere_thread)
            self._thread_initialisiert = True
        inst = oeffne(
            PROGID_ACQUISITION_INSTANCE, self._bindung.dispatch, self._richtlinie, self._kontext
        )
        laeuft_com = inst.IsRunning is True
        if laeuft_com:
            app: WhitelistProxy | None = inst.GetApplication(False)
        elif start_erlaubt:
            app = inst.GetApplication(True, self._konf.start_zeitlimit_ms)
        else:
            raise GeraeteFehler(
                "PSV läuft nicht (IsRunning=False); Start nur mit --start-psv",
                methode="AcquisitionInstance.IsRunning",
            )
        if app is None:
            raise GeraeteFehler("GetApplication lieferte keine Anwendung", methode="GetApplication")
        version = app.Version
        modus = app.Mode
        unterdrueckt = app.SuppressMessagesForAutomation is True
        acq: WhitelistProxy | None = app.Acquisition
        if acq is None:
            raise GeraeteFehler("Acquisition nicht verfügbar", methode="Application.Acquisition")
        self._app, self._acq = app, acq
        self._info = GeraeteInfo(
            psv_version=str(version),
            erfassungsmodus=modus == ApplicationMode.ACQUISITION and not isinstance(modus, bool),
            meldungen_unterdrueckt=unterdrueckt,
            zustand=GeraeteZustand.GESTOPPT,
        )
        try:
            zustand = self.zustand()
            hardware = self._lies_hardware(acq)
        except BaseException:
            self._app = self._acq = self._info = None
            raise
        self._info = GeraeteInfo(
            psv_version=str(version),
            erfassungsmodus=self._info.erfassungsmodus,
            meldungen_unterdrueckt=unterdrueckt,
            zustand=zustand,
            hardware={**hardware, "psv_prozesse": ", ".join(treffer or ())},
            lademaske=lademaske_text(self._konf.lademaske),
        )
        return self._info

    def _lies_hardware(self, acq: WhitelistProxy) -> dict[str, str]:
        ergebnis: dict[str, str] = {}
        infos: WhitelistProxy | None = acq.Infos
        if infos is None or infos.HasHardware is not True:
            ergebnis["hinweis"] = "Infos.Hardware nicht verfügbar"
            return ergebnis
        hw: WhitelistProxy = infos.Hardware
        fehlend: list[str] = []
        for com_name, schluessel in _HARDWARE:
            try:
                wert = getattr(hw, com_name)
            except ComFehler:
                fehlend.append(com_name)
                continue
            ergebnis[schluessel] = wert if isinstance(wert, str) else repr(wert)
        if fehlend:
            ergebnis["nicht_lesbar"] = ", ".join(fehlend)
        return ergebnis

    def trenne(self) -> None:
        """Gibt alle Proxys frei (idempotent). PSV bleibt offen; es wird nichts gestoppt.

        Raises
        ------
        GeraeteFehler
            Wenn ``CoUninitialize`` scheitert (die Verbindung ist dann trotzdem getrennt).
        """
        self._app = self._acq = self._info = None
        self._kontext.messfreigabe = False
        self._kontext.eigene_messung_aktiv = False
        if self._thread_initialisiert:
            self._thread_initialisiert = False
            self._bindungsaufruf("beende_thread", self._bindung.beende_thread)

    @_geraeteaufruf
    def zustand(self) -> GeraeteZustand:
        """Liest ``Acquisition.State`` (vergröbert). Beendet ggf. das Flag „eigene Messung“."""
        zustand = self._lies_zustand_roh()
        if zustand is AcqState.STOPPED:
            self._kontext.eigene_messung_aktiv = False
            return GeraeteZustand.GESTOPPT
        if zustand in SCAN_ZUSTAENDE:
            return GeraeteZustand.SCANNT
        return GeraeteZustand.BESCHAEFTIGT

    def setze_messfreigabe(self, freigegeben: bool) -> None:
        """Setzt bzw. entzieht die Messfreigabe des Durchgangs (M7).

        Raises
        ------
        VerweigertFehler
            Beim Setzen außerhalb der Betriebsart ``MESSEN``. Entziehen geht immer.
        """
        if freigegeben and not self._kontext.messen_erlaubt:
            raise VerweigertFehler(
                f"Messfreigabe in Betriebsart {self.betriebsart.value} nicht möglich",
                methode="setze_messfreigabe",
            )
        self._kontext.messfreigabe = bool(freigegeben)

    @_geraeteaufruf
    def lade_einstellungen(self, pfad: str) -> None:
        """M2/M3: ``State == Stopped`` prüfen, dann ``Settings.Load(pfad, lademaske)``."""
        self._verlange_schreiben("lade_einstellungen")
        self._verlange_gestoppt("lade_einstellungen")
        app, _, _ = self._verbunden()
        settings: WhitelistProxy = app.Settings
        settings.Load(pfad, self._konf.lademaske)

    @_geraeteaufruf
    def setze_parameter(self, parameter: Mapping[str, ParameterWert]) -> None:
        """M4: FFT über den Validator (Rückfall S4 per Schalter), Mittelung direkt.

        Raises
        ------
        GeraeteFehler
            Unbekannter Schlüssel, Wert außerhalb des Katalogs, fehlender Validator ohne
            Schalter („Validator fehlt“) oder Ausnahme der Software (mit ``excepinfo``).
        VerweigertFehler
            In der Betriebsart ``NUR_LESEN``.
        """
        self._verlange_schreiben("setze_parameter")
        werte: dict[str, ParameterWert] = {}
        for schluessel, wert in parameter.items():
            self._zuordnung(schluessel)
            try:
                werte[schluessel] = self._konf.katalog.spec(schluessel).pruefe(wert)
            except ValueError as exc:
                raise GeraeteFehler(
                    str(exc), methode="setze_parameter", argumente=(schluessel, wert)
                ) from None
        if not werte:
            return
        props = self._eigenschaften()
        fft = {k: v for k, v in werte.items() if _PARAMETER[k].gruppe == "fft"}
        mittelung = {k: v for k, v in werte.items() if _PARAMETER[k].gruppe == "mittelung"}
        if fft:
            self._setze_fft(self._gruppe(props, "fft"), fft)
        if mittelung:
            avg = self._gruppe(props, "mittelung")
            if "mittelung.typ" in mittelung:
                avg.Type = int(AVERAGE_TYPE_NAMEN[str(mittelung["mittelung.typ"])])
            if "mittelung.anzahl" in mittelung:
                avg.Count = int(mittelung["mittelung.anzahl"])

    def _setze_fft(self, fft: WhitelistProxy, werte: Mapping[str, ParameterWert]) -> None:
        # Reihenfolge: Bandbreite vor Linien (AvailableLines hängt von der Bandbreite ab, I5 2.6)
        if fft.existiert("FftAcqPropertiesValidator"):
            validator: WhitelistProxy | None = fft.FftAcqPropertiesValidator
            if validator is None:
                raise GeraeteFehler(
                    "FftAcqPropertiesValidator lieferte kein Objekt",
                    methode="FftProperties.FftAcqPropertiesValidator",
                )
            ziel = validator
        elif self._konf.validator_rueckfall_direkt:
            ziel = fft
        else:
            raise GeraeteFehler(
                "Validator fehlt (FftAcqPropertiesValidator nicht vorhanden); Rückfall S4 "
                "(validator_rueckfall_direkt) ist ausgeschaltet",
                methode="FftProperties.FftAcqPropertiesValidator",
            )
        if "fft.bandbreite_hz" in werte:
            ziel.Bandwidth = float(werte["fft.bandbreite_hz"])
        if "fft.linien" in werte:
            ziel.Lines = int(werte["fft.linien"])
        if ziel is not fft:
            fft.FftAcqPropertiesValidator = ziel

    @_geraeteaufruf
    def lies_parameter(self, schluessel: Collection[str]) -> Mapping[str, ParameterWert]:
        """M5: liest die Katalogparameter zurück (``float`` bzw. ``int`` bzw. Name)."""
        self._verbunden()
        zuordnungen = {k: self._zuordnung(k) for k in schluessel}
        if not zuordnungen:
            return {}
        props = self._eigenschaften()
        gruppen: dict[str, WhitelistProxy] = {}
        ergebnis: dict[str, ParameterWert] = {}
        for k, z in zuordnungen.items():
            if z.gruppe not in gruppen:
                gruppen[z.gruppe] = self._gruppe(props, z.gruppe)
            roh = getattr(gruppen[z.gruppe], z.property)
            pfad = f"{z.gruppe}.{z.property}"
            spec = self._konf.katalog.spec(k)
            if k == "mittelung.typ":
                try:
                    ergebnis[k] = _AVERAGE_NAME[AverageType(_als_ganzzahl(roh, pfad))]
                except ValueError:
                    raise GeraeteFehler(f"{pfad}: unbekannter Wert {roh!r}", methode=pfad) from None
            elif spec.typ == "int":
                ergebnis[k] = _als_ganzzahl(roh, pfad)
            else:
                ergebnis[k] = _als_float(roh, pfad)
        return ergebnis

    @_geraeteaufruf
    def lies_einstellungsstand(self) -> EinstellungsStand:
        """M5: vollständiger Einstellungsstand, nur lesend (Generator nur gelesen).

        Nicht lesbare Einzelwerte stehen als ``None`` mit Begleitschlüssel
        ``<schluessel>__fehler`` (Fehlertext) in der Gruppe, nie still weggelassen.
        """
        _, acq, _ = self._verbunden()
        modus_roh = acq.Mode
        try:
            modus = ACQ_MODE_NAMEN[AcqMode(_als_ganzzahl(modus_roh, "Acquisition.Mode"))]
        except ValueError:
            modus = f"unbekannt({modus_roh!r})"
        generator_an = acq.GeneratorsOn
        props = self._eigenschaften()
        gruppen: dict[str, dict[str, EinstellungsWert]] = {}
        for gruppe, has, name, felder in (
            ("fft", "HasFftProperties", "FftProperties", _FFT_STAND),
            ("mittelung", "HasAverageProperties", "AverageProperties", _MITTELUNG_STAND),
            ("allgemein", "HasGeneralProperties", "GeneralProperties", _ALLGEMEIN_STAND),
            ("trigger", "HasTriggerProperties", "TriggerProperties", _TRIGGER_STAND),
            ("se", "HasSignalEnhancementProperties", "SignalEnhancementProperties", _SE_STAND),
        ):
            if getattr(props, has) is True:
                gruppen[gruppe] = self._lies_felder(getattr(props, name), felder)
        if props.HasChannelsProperties is True:
            gruppen["kanaele"] = self._lies_kanaele(props.ChannelsProperties)
        generator_aktiv: bool | None = None
        amplitude_v: float | None = None
        if props.HasGeneratorsProperties is True:
            generator = self._lies_generator(props.GeneratorsProperties)
            gruppen["generator"] = generator
            aktiv = generator.get("aktiv")
            generator_aktiv = aktiv if isinstance(aktiv, bool) else None
            amp = generator.get("amplitude_v")
            amplitude_v = float(amp) if isinstance(amp, int | float) else None
        if isinstance(generator_an, bool):
            gruppen.setdefault("generator", {})["generatoren_an"] = generator_an
            generator_aktiv = generator_an or bool(generator_aktiv)
        infos: WhitelistProxy | None = acq.Infos
        punkte: int | None = None
        if infos is not None and infos.HasMeasPoints is True:
            punkte = _als_ganzzahl(infos.MeasPoints.Count, "MeasPoints.Count")
        return EinstellungsStand(
            modus=modus,
            messpunkte_anzahl=punkte,
            generator_aktiv=generator_aktiv,
            generator_amplitude_v=amplitude_v,
            gruppen=gruppen,
        )

    @staticmethod
    def _lies_felder(
        obj: WhitelistProxy, felder: tuple[tuple[str, str], ...]
    ) -> dict[str, EinstellungsWert]:
        werte: dict[str, EinstellungsWert] = {}
        for com_name, schluessel in felder:
            try:
                werte[schluessel] = _einstellungswert(getattr(obj, com_name))
            except ComFehler as exc:
                werte[schluessel] = None
                werte[f"{schluessel}__fehler"] = exc.text
        return werte

    def _lies_kanaele(self, kanaele: WhitelistProxy) -> dict[str, EinstellungsWert]:
        werte: dict[str, EinstellungsWert] = {}
        anzahl = _als_ganzzahl(kanaele.Count, "ChannelsProperties.Count")
        werte["anzahl"] = anzahl
        for nr in range(1, min(anzahl, MAX_KANAELE) + 1):  # Polytec-Index 1-basiert
            kanal: WhitelistProxy | None = kanaele.Item(nr)
            if kanal is None:
                werte[f"k{nr - 1}__fehler"] = "Item lieferte nichts"
                continue
            for schluessel, wert in self._lies_felder(kanal, _KANAL_STAND).items():
                werte[f"k{nr - 1}.{schluessel}"] = wert  # intern 0-basiert
        if anzahl > MAX_KANAELE:
            werte["hinweis"] = f"nur die ersten {MAX_KANAELE} Kanäle gelesen"
        return werte

    def _lies_generator(self, generatoren: WhitelistProxy) -> dict[str, EinstellungsWert]:
        anzahl = _als_ganzzahl(generatoren.Count, "GeneratorsProperties.Count")
        werte: dict[str, EinstellungsWert] = {"anzahl": anzahl}
        if anzahl < 1:
            return werte
        gen: WhitelistProxy | None = generatoren.Item(1)
        if gen is None:
            werte["__fehler"] = "Item(1) lieferte nichts"
            return werte
        werte.update(self._lies_felder(gen, (("Active", "aktiv"), ("Amplitude", "amplitude_v"))))
        try:
            form: WhitelistProxy | None = gen.Waveform
            werte["signalform_typ"] = None if form is None else _einstellungswert(form.Type)
        except ComFehler as exc:
            werte["signalform_typ"] = None
            werte["signalform_typ__fehler"] = exc.text
        return werte

    @_geraeteaufruf
    def speichere_einstellungen(self, pfad: str) -> None:
        """M6 (S9): ``Settings.Save`` als Nachweis; nie überschreiben."""
        self._verlange_schreiben("speichere_einstellungen")
        existiert = self._kontext.existiert
        if existiert(pfad):
            raise VerweigertFehler(
                f"Datei existiert bereits (nie überschreiben): {pfad}",
                methode="speichere_einstellungen",
            )
        app, _, _ = self._verbunden()
        settings: WhitelistProxy = app.Settings
        settings.Save(pfad)

    @_geraeteaufruf
    def starte_scan(self, zieldatei: str) -> None:
        """M7/M8: Freigabe, ``State``, ``ScanFileName`` setzen und zurücklesen, ``ScanEx``.

        Raises
        ------
        VerweigertFehler
            Betriebsart nicht ``MESSEN``, keine Messfreigabe, Ziel vorhanden oder nicht unter
            der Messdaten-Wurzel.
        GeraetNichtBereitFehler
            ``State != Stopped``.
        AbweichungFehler
            Zurückgelesener ``ScanFileName`` weicht ab (kein ``ScanEx``).
        """
        methode = "starte_scan"
        if not self._kontext.messen_erlaubt:
            raise VerweigertFehler(
                f"Betriebsart {self.betriebsart.value} erlaubt keinen Scan", methode=methode
            )
        self._verlange_schreiben(methode)
        if not self._kontext.messfreigabe:
            raise VerweigertFehler("Keine Messfreigabe für diesen Durchgang", methode=methode)
        wurzel = self._konf.messdaten_wurzel
        if wurzel is None or not pfad_unter(zieldatei, wurzel):
            raise VerweigertFehler(
                f"Zieldatei liegt nicht unter dem Messdaten-Wurzelordner: {zieldatei}",
                methode=methode,
            )
        if self._kontext.existiert(zieldatei):
            raise VerweigertFehler(
                f"Zieldatei existiert bereits (nie überschreiben): {zieldatei}", methode=methode
            )
        self._verlange_gestoppt(methode)
        _, acq, _ = self._verbunden()
        acq.ScanFileName = zieldatei
        ist = acq.ScanFileName
        if not isinstance(ist, str) or not _gleicher_pfad(ist, zieldatei):
            raise AbweichungFehler("Acquisition.ScanFileName", zieldatei, str(ist))
        self._verlange_gestoppt(methode)  # unmittelbar vor ScanEx (S7)
        acq.ScanEx(int(ScanMode.ALL), int(ScanCaps.NONE))

    @_geraeteaufruf
    def stoppe(self) -> bool:
        """M10: sendet ``Stop`` an den eigenen Scan; blockiert nicht.

        Returns
        -------
        bool
            ``True``, wenn ``Stop`` gesendet wurde; ``False`` (No-op), wenn kein eigener
            Scan (mehr) aktiv ist. ``Stop`` wird dann nicht angefragt.

        Notes
        -----
        Vor der Entscheidung wird ``Acquisition.State`` frisch gelesen (der eigene Scan kann
        seit dem letzten Polling von selbst geendet haben). Ist der Zustand ``Stopped`` oder
        keiner der Scan-Zustände (dann läuft eine andere, fremde Aktivität), wird das Flag
        „eigene Messung“ gelöscht und ``False`` geliefert.
        """
        if not self._kontext.eigene_messung_aktiv or not self._kontext.messen_erlaubt:
            return False
        _, acq, _ = self._verbunden()
        if self._lies_zustand_roh() not in SCAN_ZUSTAENDE:
            self._kontext.eigene_messung_aktiv = False
            return False
        acq.Stop()
        return True

    def fortschritt(self) -> Fortschritt | None:
        """Ohne Ereignisbetrieb nicht ermittelbar: ``None`` (Zeitschätzung in der Steuerung)."""
        return None

    def hole_meldungen(self) -> tuple[Meldung, ...]:
        """Ohne Ereignisbetrieb leer (Meldungen stehen in der Messdatei, I5 5.1)."""
        return ()

    def haengender_aufruf_seit_s(self) -> float | None:
        """Dauer des laufenden COM-Zugriffs in s (thread-sicher, Wächter)."""
        return self._kontext.haengender_aufruf_seit_s()


_AVERAGE_NAME: dict[AverageType, str] = {v: k for k, v in AVERAGE_TYPE_NAMEN.items()}
