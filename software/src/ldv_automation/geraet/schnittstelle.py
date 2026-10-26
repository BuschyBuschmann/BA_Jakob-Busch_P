"""Abstrakte Geräteschnittstelle des Vibrometers (Protocol, Datentypen, Fehler).

Diese Datei ist die feste Grenze zwischen Ablaufsteuerung (U2), Simulator (U2) und
COM-Adapter (U3). Sie importiert nur aus ``domaene``. Gleitkommawerte sind ``float``
(float64, Konvention: Wandlung an der Adaptergrenze), Zeiten in s, Frequenzen in Hz,
Spannungen in V.

Vertrag der Aufrufe
-------------------
* Alle Methoden werden aus **einem** Geräte-Thread aufgerufen (STA, Plan P2 2.5), mit
  einer Ausnahme: :meth:`Messgeraet.haengender_aufruf_seit_s` darf vom Wächter-Thread
  kommen und muss thread-sicher sein.
* Fehler des Geräts werden als :class:`GeraeteFehler` (bzw. Unterklasse) gemeldet, nie als
  rohe COM-Ausnahme. Ein stiller Ersatzwert ist unzulässig.
* Indizes sind 0-basiert; die Umrechnung auf Polytec-Indizes geschieht im Adapter.
* Alle Pfade sind Text (``str``) in der Schreibweise des Messrechners.
* **Betriebsart:** Ein Gerät (Simulator wie Adapter) erhält die Betriebsart bei der
  Konstruktion und setzt sie selbst durch: In der Betriebsart verbotene Aufrufe lösen
  :class:`VerweigertFehler` aus. Umschalten der Betriebsart heißt: Die Sitzung trennt und
  konstruiert das Gerät neu. Die Steuerung ruft zusätzlich keine in der Betriebsart
  verbotenen Methoden auf.
* **Stoppen:** :meth:`Messgeraet.stoppe` sendet nur ``Stop`` und kehrt sofort zurück. Das
  Warten bis ``GESTOPPT`` (Frist ``stop_frist_s``) erledigt die Steuerung per Polling von
  :meth:`Messgeraet.zustand` mit injizierbarer Uhr; wird die Frist überschritten, wechselt
  sie nach ``GERAET_UNKLAR``. :class:`ZeitlimitFehler` steht nur für hängende
  COM-Aufrufe, nicht für ein wirkungsloses ``Stop``.
* **Hängender Aufruf:** :meth:`Messgeraet.trenne` ist bei einem hängenden Aufruf nicht
  garantiert ausführbar (es gibt nur einen Geräte-Thread). In ``GERAET_UNKLAR`` gilt das
  Gerät als verloren; die Behandlung liegt in U2.

Offene Punkte für U2/U3
-----------------------
* Ob ``ScanEx`` ohne ``AsynchronousScanEvent`` bis zum Scanende blockiert, ist unbestätigt
  (Montag). Der Vertrag von :meth:`Messgeraet.starte_scan` deckt beides: Er kehrt zurück,
  wenn der Aufruf zurückkehrt; die Steuerung prüft danach ``zustand()``. Blockiert er, ist
  währenddessen kein ``stoppe`` möglich; der Wächter meldet den Hänger.
* Die Lademaske für ``Settings.Load`` ist Konfiguration des Adapters; sie wird über
  ``GeraeteInfo.lademaske`` an die Steuerung gemeldet (für das Messprotokoll).
* Die Vorprüfung (M1) und der Soll/Ist-Vergleich (M5) liegen in der Steuerung; der
  Vergleich selbst steht in ``ParameterSpec.stimmt_ueberein``.
"""

from __future__ import annotations

from collections.abc import Collection, Mapping
from dataclasses import dataclass, field
from enum import Enum
from typing import Protocol, TypeAlias, runtime_checkable

from ldv_automation.domaene.parameter import ParameterWert

EinstellungsWert: TypeAlias = bool | int | float | str | None
"""Wert in einem :class:`EinstellungsStand` (JSON-fähig)."""


# --- Fehler ------------------------------------------------------------------------------


class GeraeteFehler(Exception):  # noqa: N818  (Name laut freigegebenem Plan P2)
    """Basisklasse aller Fehler der Geräteschnittstelle.

    Parameters
    ----------
    text : str
        Beschreibung (Meldungstext des Geräts, falls vorhanden).
    methode : str or None
        Name der fehlgeschlagenen Geräteoperation.
    argumente : tuple
        Argumente des Aufrufs (für das Protokoll).
    hresult : int or None
        COM-HRESULT, falls vorhanden.
    excepinfo : str or None
        Text aus ``excepinfo`` der COM-Ausnahme, falls vorhanden.
    """

    def __init__(
        self,
        text: str,
        *,
        methode: str | None = None,
        argumente: tuple[object, ...] = (),
        hresult: int | None = None,
        excepinfo: str | None = None,
    ) -> None:
        super().__init__(text)
        self.text = text
        self.methode = methode
        self.argumente = argumente
        self.hresult = hresult
        self.excepinfo = excepinfo


class ZeitlimitFehler(GeraeteFehler):
    """Ein Geräteaufruf hat seine Frist überschritten (hängender COM-Aufruf, Wächter).

    Nicht dafür gedacht: ein ``Stop``, das nicht greift. Das erkennt die Steuerung selbst
    per Polling von ``zustand()`` (``GERAET_UNKLAR``).
    """


class GeraetNichtBereitFehler(GeraeteFehler):
    """Das Gerät ist nicht bereit: ``zustand() != GESTOPPT`` (z. B. fremde Messung)."""


class VerweigertFehler(GeraeteFehler):
    """Die Operation ist verboten (Default deny, fehlende Messfreigabe, Betriebsart)."""


class AbweichungFehler(GeraeteFehler):
    """Zurückgelesener Wert weicht vom Sollwert ab.

    Parameters
    ----------
    schluessel : str
        Parameterschlüssel.
    soll, ist : int or float or str
        Sollwert und zurückgelesener Wert.
    """

    def __init__(self, schluessel: str, soll: ParameterWert, ist: ParameterWert) -> None:
        super().__init__(f"Parameter '{schluessel}': Soll {soll!r}, Ist {ist!r}")
        self.schluessel = schluessel
        self.soll = soll
        self.ist = ist


# --- Datentypen --------------------------------------------------------------------------


class GeraeteZustand(Enum):
    """Zustand der Messsoftware (entspricht ``Acquisition.State``, vergröbert)."""

    GESTOPPT = "gestoppt"
    SCANNT = "scannt"
    BESCHAEFTIGT = "beschaeftigt"
    """Andere Aktivität (Einzel-/Dauermessung, Autofokus, Pfadlänge): fremde Messung."""


@dataclass(frozen=True, kw_only=True)
class GeraeteInfo:
    """Ergebnis von :meth:`Messgeraet.verbinde`.

    Parameters
    ----------
    psv_version : str
        Version der Messsoftware (``Application.Version``).
    erfassungsmodus : bool
        ``True``, wenn PSV im Erfassungsmodus (Acquisition) ist.
    meldungen_unterdrueckt : bool
        ``SuppressMessagesForAutomation``; ist es ``False``, ist der Messbetrieb zu sperren.
    zustand : GeraeteZustand
        Zustand beim Verbinden.
    hardware : mapping
        Hardware-Kennungen (Frontend, Karte, Firmware, Sensorkopf-Seriennummern, soweit
        gelesen); Schlüssel nach Adapter.
    lademaske : str
        Maske, mit der ``lade_einstellungen`` Einstellungsdateien lädt (Pflichtfeld des
        Messprotokolls, Plan 4.3): Namen nach ``PTCSettings``, getrennt durch ``"|"``
        (z. B. ``"Acquisition|Alignment|APS|2DAlignment|3DAlignment"``). Leer, wenn das
        Gerät keine Maske verwendet (z. B. Simulator). Sie ist Konfiguration des
        Geräts und steht hier nur zur Dokumentation im Protokoll.
    """

    psv_version: str
    erfassungsmodus: bool
    meldungen_unterdrueckt: bool
    zustand: GeraeteZustand
    hardware: Mapping[str, str] = field(default_factory=dict)
    lademaske: str = ""


@dataclass(frozen=True, kw_only=True)
class EinstellungsStand:
    """Von PSV tatsächlich übernommene Einstellungen (nur lesend erhoben, R-020).

    Parameters
    ----------
    modus : str
        Erfassungsmodus, erwartet ``"Fft"``.
    messpunkte_anzahl : int or None
        Anzahl Messpunkte der geladenen Einstellung.
    generator_aktiv : bool or None
        ``GeneratorsOn`` bzw. Generator-Aktiv; ``None`` wenn nicht lesbar.
    generator_amplitude_v : float or None
        Generatoramplitude in V; ``None`` wenn nicht lesbar.
    gruppen : mapping
        Gruppen ``fft``, ``mittelung``, ``allgemein``, ``trigger``, ``se``, ``kanaele``,
        ``generator`` mit flachen Schlüssel/Wert-Paaren (Einheit im Schlüssel,
        z. B. ``start_frequenz_hz``).
    """

    modus: str
    messpunkte_anzahl: int | None = None
    generator_aktiv: bool | None = None
    generator_amplitude_v: float | None = None
    gruppen: Mapping[str, Mapping[str, EinstellungsWert]] = field(default_factory=dict)


@dataclass(frozen=True, kw_only=True)
class Meldung:
    """Meldung der Messsoftware (nur mit Ereignisbetrieb).

    Parameters
    ----------
    stil : int
        Meldungsstil nach ``PTCMessageStyle``.
    text : str
        Meldungstext.
    antwort : str or None
        Vom Programm gegebene Antwort (z. B. ``"Cancel"``).
    """

    stil: int
    text: str
    antwort: str | None = None


@dataclass(frozen=True, kw_only=True)
class Fortschritt:
    """Fortschritt eines laufenden Scans.

    Parameters
    ----------
    punkte_erledigt : int
        Bereits gemessene Punkte.
    punkte_gesamt : int
        Gesamtzahl der Punkte.
    quelle : str
        ``"ereignisse"`` oder ``"punktstatus"`` (geschätzt über die Zeit rechnet die
        Steuerung selbst und kennzeichnet es als solches).
    """

    punkte_erledigt: int
    punkte_gesamt: int
    quelle: str


# --- Protocol ----------------------------------------------------------------------------


@runtime_checkable
class Messgeraet(Protocol):
    """Schnittstelle zum Vibrometer bzw. seinem Simulator."""

    def verbinde(self) -> GeraeteInfo:
        """Verbindet mit der laufenden Messsoftware und liest Version, Modus, Zustand.

        Startet die Messsoftware nie von selbst.

        Raises
        ------
        GeraeteFehler
            Wenn die Software nicht läuft oder die Verbindung scheitert.
        """
        ...

    def trenne(self) -> None:
        """Beendet die Verbindung (idempotent). Beendet die Messsoftware nicht."""
        ...

    def zustand(self) -> GeraeteZustand:
        """Liest den aktuellen Zustand der Messsoftware."""
        ...

    def setze_messfreigabe(self, freigegeben: bool) -> None:
        """Setzt oder entzieht die Messfreigabe (gilt für einen Durchgang).

        Ohne Freigabe verweigert :meth:`starte_scan` mit :class:`VerweigertFehler`.
        """
        ...

    def lade_einstellungen(self, pfad: str) -> None:
        """Lädt eine Einstellungsdatei (``.set``) in die Messsoftware.

        Raises
        ------
        GeraeteFehler
            Bei unbekannter Datei oder Fehler der Software.
        """
        ...

    def setze_parameter(self, parameter: Mapping[str, ParameterWert]) -> None:
        """Setzt Katalogparameter. Die Software kann Werte einrasten.

        Der Aufrufer liest danach mit :meth:`lies_parameter` zurück.

        Raises
        ------
        GeraeteFehler
            Bei ungültiger Kombination (mit Meldungstext der Software).
        """
        ...

    def lies_parameter(self, schluessel: Collection[str]) -> Mapping[str, ParameterWert]:
        """Liest die aktuellen Werte der Katalogparameter zurück (float64 bzw. int)."""
        ...

    def lies_einstellungsstand(self) -> EinstellungsStand:
        """Liest den vollständigen Einstellungsstand (nur lesend)."""
        ...

    def speichere_einstellungen(self, pfad: str) -> None:
        """Speichert die Einstellungen als Nachweis (optional, M6).

        Raises
        ------
        VerweigertFehler
            Wenn die Datei schon existiert (nie überschreiben).
        """
        ...

    def starte_scan(self, zieldatei: str) -> None:
        """Setzt die Zieldatei und startet einen vollständigen Scan.

        Voraussetzungen: Messfreigabe gesetzt, ``zustand() == GESTOPPT``, ``zieldatei``
        existiert nicht (nie leer, nie überschreiben). Die Zieldatei wird zurückgelesen
        und verglichen, bevor der Scan startet.

        Raises
        ------
        GeraetNichtBereitFehler
            Wenn ``zustand() != GESTOPPT`` (fremde Messung wird nie angefasst).
        VerweigertFehler
            Bei fehlender Freigabe, vorhandener Zieldatei, unerlaubtem Pfad oder in der
            Betriebsart verbotenem Aufruf.
        GeraeteFehler
            Bei Fehlern der Software.
        """
        ...

    def stoppe(self) -> bool:
        """Sendet ``Stop`` an den **eigenen** laufenden Scan; blockiert nicht.

        Kehrt sofort zurück. Das Warten bis ``GESTOPPT`` macht die Steuerung per Polling
        von :meth:`zustand`. Einen fremden Scan stoppt diese Methode nie.

        Returns
        -------
        bool
            ``True``, wenn ``Stop`` gesendet wurde (eigener Scan aktiv). ``False`` als
            No-op ohne Ausnahme, wenn kein eigener Scan (mehr) aktiv ist, auch wenn er
            gerade natürlich geendet hat, und bei fremdem Scan.

        Raises
        ------
        GeraeteFehler
            Bei Fehlern der Software beim Senden von ``Stop``.
        """
        ...

    def fortschritt(self) -> Fortschritt | None:
        """Fortschritt des laufenden Scans oder ``None``, wenn nicht ermittelbar."""
        ...

    def hole_meldungen(self) -> tuple[Meldung, ...]:
        """Gibt neue Meldungen seit dem letzten Aufruf zurück (leer ohne Ereignisbetrieb)."""
        ...

    def haengender_aufruf_seit_s(self) -> float | None:
        """Dauer des gerade blockierenden Geräteaufrufs in s, sonst ``None``.

        Thread-sicher; für den Wächter-Thread (Plan P2 2.5).
        """
        ...
