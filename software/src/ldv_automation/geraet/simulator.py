"""Simulator der Geräteschnittstelle :class:`~ldv_automation.geraet.schnittstelle.Messgeraet`.

Der Simulator bildet das *Verhalten* der Messsoftware auf Ebene des Protocols nach
(ADR-009), nicht das COM-Objektmodell. Er ist deterministisch: Zeit kommt aus einer
übergebenen Funktion (in Tests die Testuhr), Fehler kommen aus einem **Drehbuch**
(Liste von Ereignissen je Messvorgang). Zufall gibt es nicht.

Ein *Messvorgang* ist hier jeder Aufruf von :meth:`Simulator.lade_einstellungen`
(0-basiert gezählt). Jede Messung und jede Wiederholung lädt genau einmal; ein
Drehbuch-Ereignis mit ``vorgang=1`` betrifft also den zweiten Messvorgang des Simulators.

Nachgebildet (Plan P2, Abschnitt 5):

1. Verbindung: PSV läuft oder nicht, Version ``"10.x-SIM"``, ``Suppress`` wahr oder
   falsch, Erfassungsmodus ja oder nein.
2. Zustände ``GESTOPPT -> SCANNT -> GESTOPPT``; fremde Messung beim Start.
3. Dauer = Punkteanzahl mal Punktdauer über die übergebene Zeitfunktion. Einen eigenen
   Schrittmodus (Halt an Punkt k) hat der Simulator nicht; deterministisches Anhalten
   mitten im Scan geschieht über das taktweise ``Steuerung.schritt()`` mit Testuhr.
5. Einrasten von Bandbreite und Linien auf die nächste verfügbare Stufe.
6. Ungültige Mittelungsanzahl (< 3) löst einen Gerätefehler aus.
7. Fehlender Validator (ohne Rückfallschalter: Gerätefehler).
8. Unbekannte Einstellungsdatei; Teil-Laden (Modus bleibt falsch).
9. Platzhalter-Scandatei mit Kennung ``SIMULATOR``; vorhandene Datei wird verweigert.
10. Drehbuch-Fehler: Ausnahme bei Start, Ausnahme während des Scans, vorzeitiges Ende,
    Hänger, wirkungsloses ``Stop``, hängender Aufruf, langsamer (normal zurückkehrender)
    Aufruf, keine Datei.
11. Meldungen an Punkt k.
12. Aufrufprotokoll.

Nicht nachgebildet: nicht fortlaufende Punktreihenfolge (Plan 5, Punkt 4). Der
Fortschritt zählt nur erledigte Punkte; die Reihenfolge spielt dafür keine Rolle.

Betriebsart
-----------
Das Gerät erhält die Betriebsart bei der Konstruktion und setzt sie selbst durch
(Vertrag in ``schnittstelle.py``). Bis die Schnittstelle einen gemeinsamen Aufzählungstyp
anbietet, wird sie als Text übergeben (``"simulator"``, ``"nur_lesen"``,
``"trockenlauf"``, ``"messen"``; entspricht ``Betriebsart.value`` der Sitzung).
"""

from __future__ import annotations

import json
import math
import os
import threading
from collections.abc import Callable, Collection, Mapping, Sequence
from dataclasses import dataclass, field
from typing import TypeAlias

from ldv_automation.domaene.parameter import ParameterWert
from ldv_automation.geraet.schnittstelle import (
    EinstellungsStand,
    Fortschritt,
    GeraeteFehler,
    GeraeteInfo,
    GeraeteZustand,
    GeraetNichtBereitFehler,
    Meldung,
    VerweigertFehler,
    ZeitlimitFehler,
)

SIMULATOR_KENNUNG = b"SIMULATOR"
"""Erste Bytes jeder Platzhalter-Scandatei."""

BETRIEBSARTEN = ("simulator", "nur_lesen", "trockenlauf", "messen")
"""Zulässige Werte für ``betriebsart`` (Text, siehe Modul-Docstring)."""

_SCHREIBEN_ERLAUBT = frozenset({"simulator", "trockenlauf", "messen"})
_SCAN_ERLAUBT = frozenset({"simulator", "messen"})


# --- Drehbuch ----------------------------------------------------------------------------


@dataclass(frozen=True, kw_only=True)
class LadeFehler:
    """``lade_einstellungen`` im Vorgang ``vorgang`` scheitert mit ``text``."""

    vorgang: int
    text: str = "Simulator: Einstellungsdatei konnte nicht geladen werden"


@dataclass(frozen=True, kw_only=True)
class TeilLaden:
    """Teil-Laden: Der Modus bleibt nach dem Laden auf ``modus`` statt ``"Fft"``."""

    vorgang: int
    modus: str = "Time"


@dataclass(frozen=True, kw_only=True)
class StartFehler:
    """``starte_scan`` scheitert mit Gerätefehler; es entsteht keine Datei."""

    vorgang: int
    text: str = "Simulator: ScanEx fehlgeschlagen"
    hresult: int | None = None


@dataclass(frozen=True, kw_only=True)
class ScanFehler:
    """``zustand()`` wirft einmal einen Gerätefehler, sobald der Scan ``nach_s`` läuft.

    Der Scan läuft danach weiter, bis er endet oder gestoppt wird.
    """

    vorgang: int
    nach_s: float
    text: str = "Simulator: Fehler während des Scans"


@dataclass(frozen=True, kw_only=True)
class VorzeitigesEnde:
    """Der Scan endet nach ``nach_punkten`` Punkten (wie nach drei Fehlversuchen)."""

    vorgang: int
    nach_punkten: int


@dataclass(frozen=True, kw_only=True)
class Haenger:
    """Der Scan endet nie von selbst; mit ``stop_wirkt=False`` greift auch ``Stop`` nicht."""

    vorgang: int
    stop_wirkt: bool = True


@dataclass(frozen=True, kw_only=True)
class KeineDatei:
    """Der Scan läuft normal, legt aber keine Datei an."""

    vorgang: int


@dataclass(frozen=True, kw_only=True)
class HaengenderAufruf:
    """Der Aufruf ``methode`` blockiert im Vorgang ``vorgang`` bis :meth:`Simulator.haenger_loesen`.

    Für den Wächter (Plan P2, 2.5). Wird er nicht innerhalb von ``max_echtzeit_s``
    (Echtzeit) gelöst, wirft der Aufruf :class:`ZeitlimitFehler`. ``vorgang=-1`` meint
    Aufrufe vor dem ersten Laden (z. B. ``verbinde``, ``setze_messfreigabe(True)``).
    """

    vorgang: int
    methode: str
    max_echtzeit_s: float = 30.0


@dataclass(frozen=True, kw_only=True)
class LangsamerAufruf:
    """Der Aufruf ``methode`` dauert ``dauer_s`` und kehrt dann **normal** zurück.

    Die Dauer vergeht über die beim Simulator übergebene Funktion ``schlafen`` (in Tests
    ``Testuhr.sleep``, also ohne echtes Warten). Für die Aufrufgrenze der Steuerung
    (Nutzerentscheidung K-U2b). ``vorgang=-1`` wie bei :class:`HaengenderAufruf`.
    """

    vorgang: int
    methode: str
    dauer_s: float


@dataclass(frozen=True, kw_only=True)
class MeldungBeiPunkt:
    """Die Software meldet nach ``nach_punkten`` Punkten eine Meldung."""

    vorgang: int
    nach_punkten: int
    stil: int
    text: str


DrehbuchEreignis: TypeAlias = (
    LadeFehler
    | TeilLaden
    | StartFehler
    | ScanFehler
    | VorzeitigesEnde
    | Haenger
    | KeineDatei
    | HaengenderAufruf
    | LangsamerAufruf
    | MeldungBeiPunkt
)


# --- Konfiguration -----------------------------------------------------------------------


@dataclass(frozen=True, kw_only=True)
class SimulatorKonfiguration:
    """Feste Eigenschaften des simulierten Geräts.

    Parameters
    ----------
    psv_laeuft : bool
        ``False``: :meth:`Simulator.verbinde` scheitert (PSV wird nie gestartet).
    version : str
        Gemeldete Version.
    meldungen_unterdrueckt : bool
        ``SuppressMessagesForAutomation``.
    erfassungsmodus : bool
        PSV im Erfassungsmodus.
    fremde_messung : bool
        Beim Verbinden läuft eine fremde Aktivität (Zustand ``BESCHAEFTIGT``), bis
        :meth:`Simulator.fremde_messung_beenden` aufgerufen wird.
    punkte_anzahl : int
        Messpunkte der geladenen Einstellung (> 0).
    punktdauer_s : float
        Dauer je Punkt in s (> 0).
    bandbreiten_hz : tuple of float
        Verfügbare Bandbreiten; gesetzte Werte rasten auf die nächste Stufe ein.
    linien : tuple of int
        Verfügbare Linienzahlen; Einrasten wie bei der Bandbreite.
    validator_vorhanden : bool
        ``False`` bildet ein PSV ohne ``FftAcqPropertiesValidator`` nach.
    rueckfall_direkt : bool
        Mit ``validator_vorhanden=False``: ``True`` setzt direkt (Rückfall S4), sonst
        Gerätefehler "Validator fehlt".
    fortschritt_ereignisse : bool
        ``True``: :meth:`Simulator.fortschritt` liefert erledigte Punkte (wie mit
        ``--ereignisse``); sonst ``None``.
    hardware : mapping
        Gemeldete Hardware-Kennungen.
    """

    psv_laeuft: bool = True
    version: str = "10.x-SIM"
    meldungen_unterdrueckt: bool = True
    erfassungsmodus: bool = True
    fremde_messung: bool = False
    punkte_anzahl: int = 9
    punktdauer_s: float = 1.0
    bandbreiten_hz: tuple[float, ...] = (
        781.25,
        1562.5,
        3125.0,
        5000.0,
        6250.0,
        12500.0,
        25000.0,
    )
    linien: tuple[int, ...] = (100, 200, 400, 800, 1600, 3200, 6400, 12800)
    validator_vorhanden: bool = True
    rueckfall_direkt: bool = False
    fortschritt_ereignisse: bool = False
    hardware: Mapping[str, str] = field(
        default_factory=lambda: {"frontend": "SIM-FE", "firmware": "SIM-1.0"}
    )

    def __post_init__(self) -> None:
        if self.punkte_anzahl <= 0:
            raise ValueError("SimulatorKonfiguration: punkte_anzahl muss > 0 sein")
        if not math.isfinite(self.punktdauer_s) or self.punktdauer_s <= 0:
            raise ValueError("SimulatorKonfiguration: punktdauer_s muss endlich und > 0 sein")
        if not self.bandbreiten_hz or not self.linien:
            raise ValueError(
                "SimulatorKonfiguration: Bandbreiten und Linien dürfen nicht leer sein"
            )


_STANDARDWERTE: Mapping[str, ParameterWert] = {
    "fft.bandbreite_hz": 3125.0,
    "fft.linien": 800,
    "mittelung.anzahl": 3,
    "mittelung.typ": "Complex",
}


def _einrasten(soll: float, stufen: Sequence[float]) -> float:
    """Nächste Stufe; bei gleichem Abstand die größere."""
    return min(stufen, key=lambda s: (abs(s - soll), -s))


@dataclass
class _Scan:
    zieldatei: str
    start_s: float
    vorgang: int
    gestoppt: bool = False
    stop_gesendet: bool = False
    scanfehler_gemeldet: bool = False
    gemeldet: set[int] = field(default_factory=set)


class Simulator:
    """Deterministischer Simulator von :class:`Messgeraet`.

    Parameters
    ----------
    zeit : callable
        Monotone Zeit in s (z. B. ``Testuhr.monotonic``).
    betriebsart : str
        Eine aus :data:`BETRIEBSARTEN`; wird selbst durchgesetzt.
    konfiguration : SimulatorKonfiguration
        Eigenschaften des Geräts.
    drehbuch : sequence of DrehbuchEreignis
        Geplante Fehler und Meldungen.

    Raises
    ------
    ValueError
        Bei unbekannter Betriebsart oder negativem Vorgang im Drehbuch.
    """

    def __init__(
        self,
        zeit: Callable[[], float],
        *,
        betriebsart: str = "simulator",
        konfiguration: SimulatorKonfiguration | None = None,
        drehbuch: Sequence[DrehbuchEreignis] = (),
        schlafen: Callable[[float], None] | None = None,
    ) -> None:
        if betriebsart not in BETRIEBSARTEN:
            raise ValueError(
                f"Simulator: unbekannte Betriebsart {betriebsart!r} "
                f"(erlaubt: {', '.join(BETRIEBSARTEN)})"
            )
        for e in drehbuch:
            minimum = -1 if isinstance(e, HaengenderAufruf | LangsamerAufruf) else 0
            if e.vorgang < minimum:
                raise ValueError(f"Simulator: Drehbuch-Vorgang muss ≥ {minimum} sein: {e!r}")
        if schlafen is None and any(isinstance(e, LangsamerAufruf) for e in drehbuch):
            raise ValueError("Simulator: LangsamerAufruf braucht die Funktion 'schlafen'")
        self._schlafen = schlafen
        self._zeit = zeit
        self.betriebsart = betriebsart
        self.konfiguration = konfiguration or SimulatorKonfiguration()
        self._drehbuch = tuple(drehbuch)
        self._aufrufe: list[tuple[str, tuple[object, ...]]] = []
        self._verbunden = False
        self._freigabe = False
        self._fremd = self.konfiguration.fremde_messung
        self._werte: dict[str, ParameterWert] = dict(_STANDARDWERTE)
        self._modus = "Fft"
        self._vorgang = -1
        self._scan: _Scan | None = None
        self._meldungen: list[Meldung] = []
        self._sperre = threading.Lock()
        self._haenger_seit_s: float | None = None
        self._haenger_frei = threading.Event()

    # --- Testhilfen ------------------------------------------------------------------

    @property
    def aufrufe(self) -> tuple[tuple[str, tuple[object, ...]], ...]:
        """Aufrufprotokoll ``(methode, argumente)`` in Reihenfolge."""
        return tuple(self._aufrufe)

    def aufgerufene_methoden(self) -> tuple[str, ...]:
        """Nur die Methodennamen des Aufrufprotokolls."""
        return tuple(name for name, _ in self._aufrufe)

    @property
    def vorgang(self) -> int:
        """Aktueller Messvorgang (0-basiert; ``-1`` vor dem ersten Laden)."""
        return self._vorgang

    def fremde_messung_beenden(self) -> None:
        """Beendet die simulierte fremde Aktivität."""
        self._fremd = False

    def haenger_loesen(self) -> None:
        """Gibt einen blockierten :class:`HaengenderAufruf` frei."""
        self._haenger_frei.set()

    # --- intern ----------------------------------------------------------------------

    def _protokolliere(self, methode: str, *argumente: object) -> None:
        self._aufrufe.append((methode, argumente))

    def _ereignisse(self, art: type[DrehbuchEreignis]) -> list[DrehbuchEreignis]:
        return [e for e in self._drehbuch if isinstance(e, art) and e.vorgang == self._vorgang]

    def _pruefe_verbunden(self, methode: str) -> None:
        if not self._verbunden:
            raise GeraeteFehler("Simulator: nicht verbunden", methode=methode)

    def _pruefe_schreiben(self, methode: str) -> None:
        if self.betriebsart not in _SCHREIBEN_ERLAUBT:
            raise VerweigertFehler(
                f"Simulator: {methode} in Betriebsart {self.betriebsart} verboten",
                methode=methode,
            )

    def _vielleicht_haengen(self, methode: str) -> None:
        for langsam in self._ereignisse(LangsamerAufruf):
            assert isinstance(langsam, LangsamerAufruf) and self._schlafen is not None
            if langsam.methode == methode:
                self._schlafen(langsam.dauer_s)
        for e in self._ereignisse(HaengenderAufruf):
            assert isinstance(e, HaengenderAufruf)
            if e.methode != methode:
                continue
            with self._sperre:
                self._haenger_seit_s = self._zeit()
            try:
                if not self._haenger_frei.wait(timeout=e.max_echtzeit_s):
                    raise ZeitlimitFehler(
                        f"Simulator: {methode} hängt länger als {e.max_echtzeit_s} s",
                        methode=methode,
                    )
            finally:
                with self._sperre:
                    self._haenger_seit_s = None
                self._haenger_frei.clear()

    def _scan_ende_s(self, scan: _Scan) -> float | None:
        """Zeitpunkt des natürlichen Scanendes; ``None`` bei Hänger."""
        if any(isinstance(e, Haenger) and e.vorgang == scan.vorgang for e in self._drehbuch):
            return None
        punkte = self.konfiguration.punkte_anzahl
        for e in self._drehbuch:
            if isinstance(e, VorzeitigesEnde) and e.vorgang == scan.vorgang:
                punkte = min(punkte, max(e.nach_punkten, 0))
        return scan.start_s + punkte * self.konfiguration.punktdauer_s

    def _punkte_erledigt(self, scan: _Scan) -> int:
        vergangen = max(self._zeit() - scan.start_s, 0.0)
        erledigt = int(vergangen / self.konfiguration.punktdauer_s)
        return min(erledigt, self.konfiguration.punkte_anzahl)

    def _aktualisiere_scan(self) -> None:
        scan = self._scan
        if scan is None or scan.gestoppt:
            return
        erledigt = self._punkte_erledigt(scan)
        for index, e in enumerate(self._drehbuch):
            if (
                isinstance(e, MeldungBeiPunkt)
                and e.vorgang == scan.vorgang
                and erledigt >= e.nach_punkten
                and index not in scan.gemeldet
            ):
                self._meldungen.append(Meldung(stil=e.stil, text=e.text))
                scan.gemeldet.add(index)
        ende = self._scan_ende_s(scan)
        if ende is not None and self._zeit() >= ende:
            scan.gestoppt = True

    # --- Messgeraet ------------------------------------------------------------------

    def verbinde(self) -> GeraeteInfo:
        """Verbindet; scheitert, wenn PSV nicht läuft (startet es nie)."""
        self._protokolliere("verbinde")
        self._vielleicht_haengen("verbinde")
        if not self.konfiguration.psv_laeuft:
            raise GeraeteFehler("Simulator: PSV läuft nicht", methode="verbinde")
        self._verbunden = True
        return GeraeteInfo(
            psv_version=self.konfiguration.version,
            erfassungsmodus=self.konfiguration.erfassungsmodus,
            meldungen_unterdrueckt=self.konfiguration.meldungen_unterdrueckt,
            zustand=self.zustand(),
            hardware=dict(self.konfiguration.hardware),
        )

    def trenne(self) -> None:
        """Trennt (idempotent)."""
        self._protokolliere("trenne")
        self._vielleicht_haengen("trenne")
        self._verbunden = False
        self._freigabe = False

    def zustand(self) -> GeraeteZustand:
        """Aktueller Zustand; wirft ggf. den :class:`ScanFehler` aus dem Drehbuch."""
        self._protokolliere("zustand")
        self._pruefe_verbunden("zustand")
        self._vielleicht_haengen("zustand")
        if self._fremd:
            return GeraeteZustand.BESCHAEFTIGT
        scan = self._scan
        if scan is None:
            return GeraeteZustand.GESTOPPT
        self._aktualisiere_scan()
        if not scan.gestoppt and not scan.scanfehler_gemeldet:
            for e in self._drehbuch:
                if (
                    isinstance(e, ScanFehler)
                    and e.vorgang == scan.vorgang
                    and self._zeit() - scan.start_s >= e.nach_s
                ):
                    scan.scanfehler_gemeldet = True
                    raise GeraeteFehler(e.text, methode="zustand", hresult=-2147352567)
        return GeraeteZustand.GESTOPPT if scan.gestoppt else GeraeteZustand.SCANNT

    def setze_messfreigabe(self, freigegeben: bool) -> None:
        """Setzt die Messfreigabe; in Betriebsarten ohne Scan nur ``False`` erlaubt."""
        self._protokolliere("setze_messfreigabe", freigegeben)
        self._vielleicht_haengen("setze_messfreigabe")
        if freigegeben and self.betriebsart not in _SCAN_ERLAUBT:
            raise VerweigertFehler(
                f"Simulator: Messfreigabe in Betriebsart {self.betriebsart} verboten",
                methode="setze_messfreigabe",
            )
        self._freigabe = freigegeben

    def lade_einstellungen(self, pfad: str) -> None:
        """Lädt eine Einstellungsdatei; beginnt einen neuen Messvorgang."""
        self._protokolliere("lade_einstellungen", pfad)
        self._pruefe_verbunden("lade_einstellungen")
        self._pruefe_schreiben("lade_einstellungen")
        self._vorgang += 1
        self._vielleicht_haengen("lade_einstellungen")
        for e in self._ereignisse(LadeFehler):
            assert isinstance(e, LadeFehler)
            raise GeraeteFehler(e.text, methode="lade_einstellungen", argumente=(pfad,))
        if not os.path.isfile(pfad):
            raise GeraeteFehler(
                f"Simulator: Einstellungsdatei unbekannt: {pfad}",
                methode="lade_einstellungen",
                argumente=(pfad,),
            )
        self._werte = dict(_STANDARDWERTE)
        teil = self._ereignisse(TeilLaden)
        self._modus = teil[0].modus if teil and isinstance(teil[0], TeilLaden) else "Fft"

    def setze_parameter(self, parameter: Mapping[str, ParameterWert]) -> None:
        """Setzt Parameter; Bandbreite und Linien rasten ein."""
        self._protokolliere("setze_parameter", dict(parameter))
        self._pruefe_verbunden("setze_parameter")
        self._pruefe_schreiben("setze_parameter")
        self._vielleicht_haengen("setze_parameter")
        konf = self.konfiguration
        fft = {"fft.bandbreite_hz", "fft.linien"} & set(parameter)
        if fft and not konf.validator_vorhanden and not konf.rueckfall_direkt:
            raise GeraeteFehler("Simulator: Validator fehlt", methode="setze_parameter")
        neu = dict(self._werte)
        for schluessel, wert in parameter.items():
            if schluessel == "fft.bandbreite_hz":
                neu[schluessel] = _einrasten(float(wert), konf.bandbreiten_hz)
            elif schluessel == "fft.linien":
                neu[schluessel] = int(_einrasten(float(wert), [float(x) for x in konf.linien]))
            elif schluessel == "mittelung.anzahl":
                if isinstance(wert, bool) or not isinstance(wert, int) or not 3 <= wert <= 10000:
                    raise GeraeteFehler(
                        f"Simulator: Mittelungsanzahl {wert!r} ungültig (3 … 10000)",
                        methode="setze_parameter",
                        argumente=(schluessel, wert),
                    )
                neu[schluessel] = wert
            elif schluessel in _STANDARDWERTE:
                neu[schluessel] = wert
            else:
                raise GeraeteFehler(
                    f"Simulator: unbekannter Parameter {schluessel!r}",
                    methode="setze_parameter",
                )
        self._werte = neu

    def lies_parameter(self, schluessel: Collection[str]) -> Mapping[str, ParameterWert]:
        """Liest die aktuellen (ggf. eingerasteten) Werte."""
        self._protokolliere("lies_parameter", tuple(schluessel))
        self._pruefe_verbunden("lies_parameter")
        self._vielleicht_haengen("lies_parameter")
        unbekannt = [s for s in schluessel if s not in self._werte]
        if unbekannt:
            raise GeraeteFehler(
                f"Simulator: unbekannte Parameter {unbekannt}", methode="lies_parameter"
            )
        return {s: self._werte[s] for s in schluessel}

    def lies_einstellungsstand(self) -> EinstellungsStand:
        """Liest den Einstellungsstand (Generator immer aus)."""
        self._protokolliere("lies_einstellungsstand")
        self._pruefe_verbunden("lies_einstellungsstand")
        self._vielleicht_haengen("lies_einstellungsstand")
        w = self._werte
        return EinstellungsStand(
            modus=self._modus,
            messpunkte_anzahl=self.konfiguration.punkte_anzahl,
            generator_aktiv=False,
            generator_amplitude_v=0.0,
            gruppen={
                "fft": {"bandbreite_hz": w["fft.bandbreite_hz"], "linien": w["fft.linien"]},
                "mittelung": {"anzahl": w["mittelung.anzahl"], "typ": w["mittelung.typ"]},
                "generator": {"aktiv": False, "amplitude_v": 0.0},
            },
        )

    def speichere_einstellungen(self, pfad: str) -> None:
        """Legt eine Platzhalter-Einstellungsdatei an (nie überschreiben)."""
        self._protokolliere("speichere_einstellungen", pfad)
        self._pruefe_verbunden("speichere_einstellungen")
        self._pruefe_schreiben("speichere_einstellungen")
        self._vielleicht_haengen("speichere_einstellungen")
        try:
            with open(pfad, "xb") as datei:
                datei.write(SIMULATOR_KENNUNG + b" Einstellungen\n")
        except FileExistsError:
            raise VerweigertFehler(
                f"Simulator: Datei existiert bereits: {pfad}",
                methode="speichere_einstellungen",
                argumente=(pfad,),
            ) from None

    def starte_scan(self, zieldatei: str) -> None:
        """Startet einen Scan und legt die Platzhalterdatei an."""
        self._protokolliere("starte_scan", zieldatei)
        self._pruefe_verbunden("starte_scan")
        if self.betriebsart not in _SCAN_ERLAUBT:
            raise VerweigertFehler(
                f"Simulator: starte_scan in Betriebsart {self.betriebsart} verboten",
                methode="starte_scan",
            )
        if not self._freigabe:
            raise VerweigertFehler("Simulator: keine Messfreigabe", methode="starte_scan")
        if not zieldatei:
            raise VerweigertFehler("Simulator: Zieldatei leer", methode="starte_scan")
        if self.zustand() is not GeraeteZustand.GESTOPPT:
            raise GeraetNichtBereitFehler(
                "Simulator: Gerät nicht bereit (Zustand ≠ gestoppt)", methode="starte_scan"
            )
        if os.path.exists(zieldatei):
            raise VerweigertFehler(
                f"Simulator: Zieldatei existiert bereits: {zieldatei}",
                methode="starte_scan",
                argumente=(zieldatei,),
            )
        self._vielleicht_haengen("starte_scan")
        for e in self._ereignisse(StartFehler):
            assert isinstance(e, StartFehler)
            raise GeraeteFehler(
                e.text, methode="starte_scan", argumente=(zieldatei,), hresult=e.hresult
            )
        if not self._ereignisse(KeineDatei):
            kopf = {"vorgang": self._vorgang, "parameter": self._werte}
            with open(zieldatei, "xb") as datei:
                datei.write(SIMULATOR_KENNUNG + b"\n" + json.dumps(kopf).encode("utf-8"))
        self._scan = _Scan(zieldatei=zieldatei, start_s=self._zeit(), vorgang=self._vorgang)

    def stoppe(self) -> bool:
        """Sendet Stop an den eigenen Scan; ``False`` ohne eigenen aktiven Scan."""
        self._protokolliere("stoppe")
        self._pruefe_verbunden("stoppe")
        self._vielleicht_haengen("stoppe")
        self._aktualisiere_scan()
        scan = self._scan
        if scan is None or scan.gestoppt:
            return False
        scan.stop_gesendet = True
        wirkt = not any(
            isinstance(e, Haenger) and e.vorgang == scan.vorgang and not e.stop_wirkt
            for e in self._drehbuch
        )
        if wirkt:
            scan.gestoppt = True
        return True

    def fortschritt(self) -> Fortschritt | None:
        """Erledigte Punkte (nur mit ``fortschritt_ereignisse``), sonst ``None``."""
        self._protokolliere("fortschritt")
        self._vielleicht_haengen("fortschritt")
        scan = self._scan
        if not self.konfiguration.fortschritt_ereignisse or scan is None or scan.gestoppt:
            return None
        return Fortschritt(
            punkte_erledigt=self._punkte_erledigt(scan),
            punkte_gesamt=self.konfiguration.punkte_anzahl,
            quelle="ereignisse",
        )

    def hole_meldungen(self) -> tuple[Meldung, ...]:
        """Neue Meldungen seit dem letzten Aufruf."""
        self._protokolliere("hole_meldungen")
        self._vielleicht_haengen("hole_meldungen")
        self._aktualisiere_scan()
        neu = tuple(self._meldungen)
        self._meldungen.clear()
        return neu

    def haengender_aufruf_seit_s(self) -> float | None:
        """Dauer des blockierten Aufrufs in s (thread-sicher), sonst ``None``."""
        with self._sperre:
            if self._haenger_seit_s is None:
                return None
            return max(self._zeit() - self._haenger_seit_s, 0.0)
