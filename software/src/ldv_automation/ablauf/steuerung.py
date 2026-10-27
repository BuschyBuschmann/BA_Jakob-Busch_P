"""Ablaufsteuerung eines Durchgangs: Zustandsmaschine und Messablauf (Plan P2, 2 und 3).

Arbeitsweise
------------
Die Steuerung ist eine taktgetriebene Zustandsmaschine. Ein Aufruf von :meth:`schritt`
erledigt eine Arbeitseinheit: Befehle abholen, dann entweder den nächsten Eintrag
beanspruchen und eine Messung bis zum Scanstart vorbereiten (M1-M8) oder den laufenden
Scan einmal abfragen (M9-M12). Im Betrieb ruft der Geräte-Thread (:meth:`starte_thread`)
``schritt`` in einer Schleife und wartet im Scan ``poll_s`` zwischen zwei Abfragen. Tests
und der Selbsttest rufen :meth:`schritt` bzw. :meth:`bis_ruhe` direkt mit einer Testuhr
auf; so sind auch Nebenläufigkeitsfälle (Bearbeiten während einer Messung) deterministisch.

Alle Geräteaufrufe geschehen in dem Thread, der ``schritt`` aufruft (ein Geräte-Thread,
ADR-008). Befehle anderer Threads laufen über eine thread-sichere Befehlswarteschlange.
Die Warteschlange der Einträge wird direkt (unter ihrer eigenen Sperre) bearbeitet; die
Steuerung beansprucht Einträge atomar mit ``naechsten_beanspruchen()`` und arbeitet mit
der eingefrorenen Kopie (R-016).

Fehlerverhalten (R-019) ist **vorläufig** und über :class:`Fehlerstrategie` austauschbar.
Ein Messprotokoll entsteht für jeden Messversuch, auch bei Fehler und Abbruch (R-020).
Die Fehlerentscheidung des Nutzers kommt erst nach dem Protokoll; sie steht deshalb im
Ereignisprotokoll, im Messprotokoll steht ``fehlerentscheidung = "ausstehend"``.
"""

from __future__ import annotations

import math
import queue
import threading
import traceback
from collections.abc import Callable, Mapping
from dataclasses import dataclass, field, replace
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import TypeAlias, TypeVar
from uuid import UUID, uuid4

from ldv_automation.ablauf.fehlerstrategie import (
    FehlerArt,
    FehlerEreignis,
    FehlerReaktion,
    Fehlerstrategie,
    PausierenUndNachfragen,
)
from ldv_automation.ablauf.geraetestand import (
    UNBEKANNTER_GENERATOR,
    DateiKennung,
    EinstellungsKenntnis,
    GeraeteStand,
    Herkunft,
    generator_aus_stand,
    pfad_schluessel,
)
from ldv_automation.ablauf.uhr import Uhr
from ldv_automation.domaene.eintraege import (
    Messung,
    MessungZustand,
    Pausenpunkt,
    PausenpunktZustand,
)
from ldv_automation.domaene.parameter import KATALOG, ParameterWert
from ldv_automation.domaene.warteschlange import Warteschlange
from ldv_automation.geraet.schnittstelle import (
    EinstellungsStand,
    Fortschritt,
    GeraeteFehler,
    GeraeteInfo,
    GeraeteZustand,
    GeraetNichtBereitFehler,
    Messgeraet,
    VerweigertFehler,
    ZeitlimitFehler,
)
from ldv_automation.persistenz.warteschlangendatei import speichere_warteschlange
from ldv_automation.protokoll.ablage import (
    ENDUNG_EINSTELLUNGEN,
    ENDUNG_MESSDATEI,
    ENDUNG_PROTOKOLL,
    EREIGNISPROTOKOLL,
    WARTESCHLANGENKOPIE,
    dateibasis,
    lege_durchgangsordner,
    sha256_datei,
)
from ldv_automation.protokoll.messprotokoll import (
    MELDUNGEN_HINWEIS,
    SCHEMA_VERSION,
    Ereignisprotokoll,
    einstellungsstand_zu_dict,
    fehler_zu_dict,
    schreibe_messprotokoll,
    zeitstempel,
)
from ldv_automation.protokoll.version import BuildInfo

_T = TypeVar("_T")

ERWARTETER_MODUS = "Fft"
"""Erfassungsmodus, den der Prototyp nach dem Laden erwartet (Plan P2, M5)."""

EINSCHRAENKUNG_VOLLSTAENDIGKEIT = (
    "Vollständigkeit des Scans im Prototyp nicht geprüft (vorzeitig beendeter Scan gilt "
    "als fertig, wenn die Datei existiert)"
)


class DurchgangZustand(Enum):
    """Zustand des Durchgangs (Plan P2, 2.3)."""

    BEREIT = "bereit"
    LAEUFT = "laeuft"
    PAUSE_ANGEFORDERT = "pause_angefordert"
    PAUSIERT = "pausiert"
    WARTET_AUF_BESTAETIGUNG = "wartet_auf_bestaetigung"
    WARTET_AUF_ENTSCHEIDUNG = "wartet_auf_entscheidung"
    ABBRUCH_LAEUFT = "abbruch_laeuft"
    GERAET_UNKLAR = "geraet_unklar"
    BEENDET = "beendet"


AKTIVE_ZUSTAENDE = frozenset(
    {DurchgangZustand.LAEUFT, DurchgangZustand.PAUSE_ANGEFORDERT, DurchgangZustand.ABBRUCH_LAEUFT}
)
"""Zustände, in denen die Steuerung ohne Befehl weiterarbeitet."""


class DurchgangErgebnis(Enum):
    """Ergebnis eines beendeten Durchgangs."""

    VOLLSTAENDIG = "vollstaendig"
    ABGEBROCHEN = "abgebrochen"
    GERAET_UNKLAR = "geraet_unklar"


class Fehlerentscheidung(Enum):
    """Entscheidung des Nutzers in ``WARTET_AUF_ENTSCHEIDUNG`` (vorläufig, O1/F20)."""

    WIEDERHOLEN = "wiederholen"
    UEBERSPRINGEN = "ueberspringen"
    ABBRECHEN = "abbrechen"


@dataclass(frozen=True, kw_only=True)
class AblaufKonfiguration:
    """Einstellungen der Ablaufsteuerung.

    Parameters
    ----------
    poll_s : float
        Abfragetakt im Scan in s (Plan M9: 0,5 s, zwischen den Polytec-Beispielen).
    zeitlimit_s : float
        Globales Zeitlimit je Scan in s für Messungen mit ``zeitlimit_s = None``.
        Startwert 600 s ist **nicht belegt**; nach der ersten Messung am Gerät anpassen.
    stop_frist_s : float
        Frist in s, in der nach ``stoppe()`` der Zustand ``GESTOPPT`` erreicht sein muss,
        sonst ``GERAET_UNKLAR``. Annahme, am Gerät einzustellen.
    punktdauer_schaetzung_s : float
        Geschätzte Dauer je Messpunkt in s, solange im Durchgang keine Messung fertig ist.
    einstellungen_sichern : bool
        ``True``: Einstellungen je Messung als ``.einstellungen.set`` sichern (M6, optional).
    aufruf_grenze_s : float
        Dauert ein einzelner Geräteaufruf länger, gilt das Gerät als unklar
        (``GERAET_UNKLAR``), auch wenn der Aufruf danach normal zurückkehrt
        (Nutzerentscheidung K-U2b). Gemessen wird die Aufrufdauer in der Steuerung mit der
        injizierten Uhr; das funktioniert auch mit einem Adapter, der selbst keinen
        ``ZeitlimitFehler`` auslöst. Ausnahme ``starte_scan``: Dort gilt das Zeitlimit der
        Messung, weil ``ScanEx`` möglicherweise bis zum Scanende blockiert (am Gerät
        unbestätigt). Standardwert 60 s ist eine **unbelegte Annahme, am Montag
        einzustellen**. Getrennt davon warnt die Sitzung schon ab ``aufruf_warnung_s``.
    """

    poll_s: float = 0.5
    zeitlimit_s: float = 600.0
    stop_frist_s: float = 10.0
    punktdauer_schaetzung_s: float = 1.0
    einstellungen_sichern: bool = False
    aufruf_grenze_s: float = 60.0

    def __post_init__(self) -> None:
        for name in (
            "poll_s",
            "zeitlimit_s",
            "stop_frist_s",
            "punktdauer_schaetzung_s",
            "aufruf_grenze_s",
        ):
            wert = getattr(self, name)
            if isinstance(wert, bool) or not math.isfinite(wert) or wert <= 0:
                raise ValueError(f"AblaufKonfiguration: {name} muss endlich und > 0 sein")


@dataclass(frozen=True, kw_only=True)
class DurchgangsAuftrag:
    """Angaben zum Start eines Durchgangs.

    Parameters
    ----------
    name : str
        Durchgangsname (Teil des Ordnernamens).
    messdaten_wurzel : pathlib.Path
        Wurzelordner der Messdaten (muss existieren).
    betriebsart : str
        Text der Betriebsart für Protokolle.
    trockenlauf : bool
        ``True``: nur M1-M6, kein Scan (Status ``trockenlauf``).
    messfreigabe : bool
        ``True``: Die Steuerung setzt zu Beginn die Messfreigabe des Geräts und entzieht
        sie am Ende. Ohne Freigabe verweigert das Gerät jeden Scan.
    messen_bestaetigt : bool
        Ausdrückliche Bestätigung des Durchgangs (Dialog 3.9); Pflicht für ``"messen"``.
    startangaben : tuple of mapping
        Angaben des Startdialogs je Messung (Messpunkte, Generator, Herkunft); stehen im
        Ereignis ``durchgang_start`` (K-U5b).

    Notes
    -----
    Die Steuerung startet nur, wenn ``betriebsart`` beim Ausführen im Geräte-Thread der
    Betriebsart des dann aktiven Geräts entspricht (Korrektur K-U5): Ein Auftrag, der vor
    einem noch ausstehenden Gerätetausch erstellt wurde, wird verworfen.
    """

    name: str
    messdaten_wurzel: Path
    betriebsart: str
    trockenlauf: bool
    messfreigabe: bool
    messen_bestaetigt: bool = False
    startangaben: tuple[Mapping[str, object], ...] = ()


@dataclass(frozen=True, kw_only=True)
class AblaufEreignis:
    """Ereignis der Steuerung (für Ereignisprotokoll und Sitzung).

    ``art`` ist z. B. ``"durchgang_zustand"`` (``von``, ``nach``), ``"eintrag_zustand"``
    (``eintrag_id``, ``von``, ``nach``), ``"befehl"``, ``"befehl_verworfen"``,
    ``"fehler"``, ``"fehlerentscheidung"``, ``"verbindung"``, ``"durchgang_beendet"``.
    """

    art: str
    text: str
    daten: Mapping[str, object] = field(default_factory=dict)


@dataclass(frozen=True, kw_only=True)
class EintragLaufinfo:
    """Laufdaten eines Eintrags (für das Zustandsbild).

    ``nummer`` ist die laufende Nummer im Durchgang (ab 1), ``versuch`` der letzte Versuch.
    """

    nummer: int | None = None
    versuch: int = 1
    zeit_start: datetime | None = None
    zeit_ende: datetime | None = None
    messdatei: str | None = None
    protokolldatei: str | None = None
    fehlerart: str | None = None
    fehlertext: str | None = None
    uebersprungen: bool = False
    trockenlauf: bool = False


@dataclass(frozen=True, kw_only=True)
class FortschrittStand:
    """Fortschritt der laufenden Messung (R-031).

    ``anteil`` liegt in 0 … 1 oder ist ``None`` (unbestimmt). ``geschaetzt`` ist ``True``
    bei Zeitschätzung (Plan 5.3). Zeiten in s.
    """

    messung_id: UUID
    anteil: float | None
    geschaetzt: bool
    quelle: str
    restzeit_s: float | None
    zeitlimit_rest_s: float


@dataclass(frozen=True, kw_only=True)
class AblaufStand:
    """Unveränderliche Momentaufnahme der Steuerung."""

    durchgang: DurchgangZustand
    ergebnis: DurchgangErgebnis | None
    betriebsart: str
    verbindung: GeraeteInfo | None
    laufinfo: Mapping[UUID, EintragLaufinfo]
    fortschritt: FortschrittStand | None
    fehler_offen: str | None
    fehler_eintrag_id: UUID | None
    pausenpunkt_id: UUID | None
    durchgang_id: UUID | None
    durchgangsordner: Path | None
    fehlerstrategie: str
    trockenlauf_ok: bool
    trockenlauf_messung: Messung | None
    geraet_verloren: bool
    interner_fehler: str | None
    durchgang_eintraege: tuple[UUID, ...] = ()
    """IDs der Messungen, die der aktuelle bzw. letzte Durchgang beansprucht hat."""
    durchgang_bilanz: tuple[UUID, ...] = ()
    """Messungen des beendeten Durchgangs: beansprucht oder bei Ende noch wartend (B2)."""
    standard_zeitlimit_s: float = 600.0
    """Zeitlimit in s für Messungen ohne eigenes Limit."""
    geraete_stand: GeraeteStand | None = None
    """Zuletzt gelesener Gerätestand (Verbinden bzw. nach dem letzten Laden)."""
    einstellungs_kenntnis: Mapping[str, EinstellungsKenntnis] = field(default_factory=dict)
    geraete_herkunft: Herkunft | None = None
    """Herkunft des aktuell verbundenen Geräts; ``None`` ohne Verbindung oder verloren."""
    """Je Einstellungsdatei (Schlüssel :func:`pfad_schluessel`) das nach dem Laden Gelesene."""


# --- Befehle -----------------------------------------------------------------------------


@dataclass(frozen=True)
class _Start:
    auftrag: DurchgangsAuftrag


@dataclass(frozen=True)
class _Einfach:
    art: str  # pause, fortsetzen, abbrechen, bestaetigen, quittieren, verbinden, trennen


@dataclass(frozen=True)
class _Entscheidung:
    entscheidung: Fehlerentscheidung


@dataclass(frozen=True)
class _Tausch:
    erzeuger: Callable[[], Messgeraet]
    betriebsart: str


_Befehl: TypeAlias = _Start | _Einfach | _Entscheidung | _Tausch


# --- laufende Messung --------------------------------------------------------------------


@dataclass
class _Aktiv:
    messung: Messung
    position: int
    nummer: int
    basis: str
    zielpfad: Path
    protokollpfad: Path
    zeit_start: datetime
    t_start_s: float
    zeitlimit_s: float
    t_scan_s: float | None = None
    scan_gestartet: bool = False
    phase: str = "vorbereitung"  # vorbereitung | scan | stop
    stop_grund: str | None = None  # abbruch | zeitlimit | fehler
    stop_gesendet: bool = False
    t_stop_s: float | None = None
    fehler: tuple[FehlerArt, str, BaseException | None] | None = None
    einstellungsdatei_sha256: str | None = None
    einstellungsdatei_kennung: DateiKennung | None = None
    geaenderte: list[dict[str, object]] = field(default_factory=list)
    einstellungen_ist: dict[str, object] | None = None
    messpunkte: int | None = None
    meldungen: list[dict[str, object]] = field(default_factory=list)
    fortschritt_quelle: str = "zeitschaetzung"


def _hinweis(eintrag: Messung | Pausenpunkt) -> str | None:
    """Hinweis je Eintrag für die Durchgangszusammenfassung."""
    if eintrag.zustand.value != "wartend":
        return None
    if isinstance(eintrag, Messung) and eintrag.versuch > 1:
        return (
            f"Wiederholung (Versuch {eintrag.versuch}) nicht gestartet; "
            "frühere Versuche siehe Messprotokolle"
        )
    return "nicht gestartet"


class Steuerung:
    """Zustandsmaschine eines Durchgangs.

    Parameters
    ----------
    warteschlange : Warteschlange
        Einträge; wird von der Sitzung parallel bearbeitet.
    geraet : Messgeraet or None
        Gerät bzw. Simulator. ``None``: Das Gerät wird später per :meth:`tausche_geraet`
        im Geräte-Thread erzeugt (COM-Objekte gehören dem Thread, der sie anlegt).
    betriebsart : str
        Text der Betriebsart des Geräts (für Protokolle und Zustandsbild).
    uhr : Uhr
        Zeitquelle (Testuhr in Tests).
    build_info : BuildInfo
        Versionsangaben für die Protokolle.
    fehlerstrategie : Fehlerstrategie
        Fehlerverhalten (Standard: vorläufige :class:`PausierenUndNachfragen`).
    konfiguration : AblaufKonfiguration
        Takt, Zeitlimit, Fristen.
    bei_ereignis : callable or None
        Wird für jedes Ereignis aufgerufen (im Thread, der ``schritt`` aufruft).
    konfiguration_info : mapping or None
        Herkunft und Werte der Konfigurationsdatei (K-U5); steht in jedem Messprotokoll
        (Feld ``konfiguration``) und im Ereignis ``durchgang_start``.
    """

    def __init__(
        self,
        *,
        warteschlange: Warteschlange,
        geraet: Messgeraet | None,
        betriebsart: str,
        uhr: Uhr,
        build_info: BuildInfo,
        fehlerstrategie: Fehlerstrategie | None = None,
        konfiguration: AblaufKonfiguration | None = None,
        bei_ereignis: Callable[[AblaufEreignis], None] | None = None,
        konfiguration_info: Mapping[str, object] | None = None,
    ) -> None:
        self._konfig_info = dict(konfiguration_info) if konfiguration_info is not None else None
        self._ws = warteschlange
        self._geraet = geraet
        self._betriebsart = betriebsart
        self._uhr = uhr
        self._build = build_info
        self._strategie: Fehlerstrategie = fehlerstrategie or PausierenUndNachfragen()
        self._konf = konfiguration or AblaufKonfiguration()
        self._bei_ereignis = bei_ereignis
        self._befehle: queue.Queue[_Befehl] = queue.Queue()
        self._signal = threading.Event()
        self._sperre = threading.RLock()
        self._thread: threading.Thread | None = None
        self._thread_ende = threading.Event()

        self._zustand = DurchgangZustand.BEREIT
        self._ergebnis: DurchgangErgebnis | None = None
        self._verbindung: GeraeteInfo | None = None
        self._laufinfo: dict[UUID, EintragLaufinfo] = {}
        self._fortschritt: FortschrittStand | None = None
        self._fehler_offen: str | None = None
        self._fehler_eintrag_id: UUID | None = None
        self._pausenpunkt_id: UUID | None = None
        self._pause_vorgemerkt = False
        self._auftrag: DurchgangsAuftrag | None = None
        self._durchgang_id: UUID | None = None
        self._ordner: Path | None = None
        self._ereignisprotokoll: Ereignisprotokoll | None = None
        self._nummern: dict[UUID, int] = {}
        self._bilanz: tuple[UUID, ...] = ()
        self._punktdauer_s: float | None = None
        self._freigabe_gesetzt = False
        self._trockenlauf_messung: Messung | None = None
        self._erste_trockenmessung = True
        self._interner_fehler: str | None = None
        self._geraete_stand: GeraeteStand | None = None
        self._kenntnis: dict[str, EinstellungsKenntnis] = {}
        self._geraet_nr = 0
        self._aufruf_haengt = False
        self._geraet_verloren = False
        self._durchgang_offen = False
        self._aktiv: _Aktiv | None = None

    # --- Lesen -------------------------------------------------------------------------

    @property
    def warteschlange(self) -> Warteschlange:
        """Die bearbeitete Warteschlange."""
        return self._ws

    @property
    def geraet(self) -> Messgeraet:
        """Das angesteuerte Gerät.

        Raises
        ------
        RuntimeError
            Wenn noch kein Gerät erzeugt wurde.
        """
        geraet = self._geraet
        if geraet is None:
            raise RuntimeError("Steuerung: kein Gerät vorhanden")
        return geraet

    @property
    def geraet_oder_none(self) -> Messgeraet | None:
        """Das Gerät oder ``None`` (ein Lesezugriff, für andere Threads geeignet)."""
        return self._geraet

    def verwerfe_trockenlauf(self) -> None:
        """Entzieht die Trockenlauf-Freischaltung (z. B. nach Laden einer Warteschlange)."""
        with self._sperre:
            self._trockenlauf_messung = None

    @property
    def standard_zeitlimit_s(self) -> float:
        """Zeitlimit in s für Messungen ohne eigenes Limit."""
        return self._konf.zeitlimit_s

    def _herkunft(self) -> Herkunft | None:
        """Herkunft des verbundenen, nicht verlorenen Geräts (unter der Sperre aufrufen)."""
        if self._verbindung is None or self._geraet_verloren:
            return None
        return Herkunft(
            geraet_nr=self._geraet_nr,
            betriebsart=self._betriebsart,
            lademaske=self._verbindung.lademaske,
            psv_prozesse=self._verbindung.hardware.get("psv_prozesse"),
        )

    def setze_standard_zeitlimit(self, zeitlimit_s: float) -> None:
        """Setzt das Standard-Zeitlimit (gilt ab der nächsten gestarteten Messung).

        Raises
        ------
        ValueError
            Wenn der Wert nicht endlich und > 0 ist.
        """
        neu = replace(self._konf, zeitlimit_s=zeitlimit_s)  # prüft in __post_init__
        with self._sperre:
            self._konf = neu

    @property
    def hat_geraet(self) -> bool:
        """Gibt an, ob ein Gerät vorhanden ist."""
        return self._geraet is not None

    @property
    def betriebsart(self) -> str:
        """Betriebsart des aktuellen Geräts (Text)."""
        return self._betriebsart

    def setze_warteschlange(self, warteschlange: Warteschlange) -> None:
        """Ersetzt die Warteschlange (z. B. nach dem Laden einer Datei).

        Raises
        ------
        ValueError
            Wenn ein Durchgang läuft oder noch Befehle ausstehen.
        """
        with self._sperre:
            if self._zustand not in (DurchgangZustand.BEREIT, DurchgangZustand.BEENDET):
                raise ValueError(
                    f"Warteschlange kann im Zustand {self._zustand.value} nicht ersetzt werden"
                )
            if not self._befehle.empty():
                raise ValueError(
                    "Warteschlange kann bei ausstehenden Befehlen nicht ersetzt werden"
                )
            self._ws = warteschlange
            self._laufinfo = {}

    @property
    def zustand(self) -> DurchgangZustand:
        """Aktueller Durchgangszustand."""
        return self._zustand

    def ist_aktiv(self) -> bool:
        """Gibt an, ob der Durchgang ohne Befehl weiterarbeitet (``LAEUFT`` u. a.)."""
        return self._zustand in AKTIVE_ZUSTAENDE

    def momentaufnahme(self) -> AblaufStand:
        """Thread-sichere Momentaufnahme (blockiert nicht durch Geräteaufrufe)."""
        with self._sperre:
            return AblaufStand(
                durchgang=self._zustand,
                ergebnis=self._ergebnis,
                betriebsart=self._betriebsart,
                verbindung=self._verbindung,
                laufinfo=dict(self._laufinfo),
                fortschritt=self._fortschritt,
                fehler_offen=self._fehler_offen,
                fehler_eintrag_id=self._fehler_eintrag_id,
                pausenpunkt_id=self._pausenpunkt_id,
                durchgang_id=self._durchgang_id,
                durchgangsordner=self._ordner,
                fehlerstrategie=self._strategie.bezeichnung,
                trockenlauf_ok=self._trockenlauf_messung is not None,
                trockenlauf_messung=self._trockenlauf_messung,
                geraet_verloren=self._geraet_verloren,
                interner_fehler=self._interner_fehler,
                durchgang_eintraege=tuple(self._nummern),
                durchgang_bilanz=self._bilanz,
                standard_zeitlimit_s=self._konf.zeitlimit_s,
                geraete_stand=self._geraete_stand,
                einstellungs_kenntnis=dict(self._kenntnis),
                geraete_herkunft=self._herkunft(),
            )

    # --- Befehle (aus jedem Thread) ----------------------------------------------------

    def _sende(self, befehl: _Befehl) -> None:
        self._befehle.put(befehl)
        self._signal.set()

    def starte(self, auftrag: DurchgangsAuftrag) -> None:
        """Befehl: Durchgang starten (nur aus ``BEREIT`` mit Verbindung)."""
        self._sende(_Start(auftrag))

    def pausiere(self) -> None:
        """Befehl: nach der laufenden Messung anhalten (R-018)."""
        self._sende(_Einfach("pause"))

    def setze_fort(self) -> None:
        """Befehl: pausierten Durchgang fortsetzen."""
        self._sende(_Einfach("fortsetzen"))

    def brich_ab(self) -> None:
        """Befehl: Durchgang abbrechen; die laufende eigene Messung wird gestoppt."""
        self._sende(_Einfach("abbrechen"))

    def bestaetige(self) -> None:
        """Befehl: erreichten Pausenpunkt bestätigen (R-017)."""
        self._sende(_Einfach("bestaetigen"))

    def entscheide(self, entscheidung: Fehlerentscheidung) -> None:
        """Befehl: Fehlerentscheidung (vorläufig, O1/F20)."""
        self._sende(_Entscheidung(entscheidung))

    def quittiere(self) -> None:
        """Befehl: beendeten Durchgang quittieren (``BEENDET -> BEREIT``)."""
        self._sende(_Einfach("quittieren"))

    def verbinde(self) -> None:
        """Befehl: mit dem Gerät verbinden (nur ohne laufenden Durchgang)."""
        self._sende(_Einfach("verbinden"))

    def trenne(self) -> None:
        """Befehl: Verbindung trennen (ohne laufenden Durchgang oder in ``GERAET_UNKLAR``)."""
        self._sende(_Einfach("trennen"))

    def tausche_geraet(self, erzeuger: Callable[[], Messgeraet], betriebsart: str) -> None:
        """Befehl: altes Gerät trennen, neues im Geräte-Thread erzeugen (Betriebsart wechseln).

        Nur ohne laufenden Durchgang (``BEREIT``, ``BEENDET``) bzw. in ``GERAET_UNKLAR``
        (dann wird das alte Gerät nicht mehr angesprochen).
        """
        self._sende(_Tausch(erzeuger, betriebsart))

    # --- Takt --------------------------------------------------------------------------

    def braucht_takt(self) -> bool:
        """Gibt an, ob vor dem nächsten Schritt ``poll_s`` gewartet werden soll."""
        aktiv = self._aktiv
        return aktiv is not None and aktiv.phase in ("scan", "stop") and self.ist_aktiv()

    def schritt(self) -> None:
        """Eine Arbeitseinheit: anstehende Befehle verarbeiten *oder* den Ablauf weiterschalten.

        Gab es Befehle, endet der Schritt nach ihrer Verarbeitung; der Ablauf geht im
        nächsten Schritt weiter.

        Ein unerwarteter interner Fehler führt nicht in eine Sackgasse: Er wird sichtbar
        gemacht (``GERAET_UNKLAR``, :attr:`AblaufStand.interner_fehler`), der laufende
        Eintrag wird ``FEHLER``, die Messfreigabe entzogen, und weitere Befehle (Trennen,
        Gerät tauschen, Quittieren) werden verarbeitet.
        """
        try:
            self._schritt()
        except Exception:  # Letzte Linie: sichtbar machen statt den Geräte-Thread zu verlieren
            self._behandle_internen_fehler(traceback.format_exc())

    def _schritt(self) -> None:
        befehle = False
        while True:
            try:
                befehl = self._befehle.get_nowait()
            except queue.Empty:
                break
            befehle = True
            self._verarbeite(befehl)
        if befehle or not self.ist_aktiv():
            return
        aktiv = self._aktiv
        if aktiv is not None:
            self._pruefe_scan(aktiv)
            return
        if self._zustand is DurchgangZustand.PAUSE_ANGEFORDERT:
            self._wechsle(DurchgangZustand.PAUSIERT)
            return
        if self._zustand is DurchgangZustand.ABBRUCH_LAEUFT:
            self._beende_durchgang(DurchgangErgebnis.ABGEBROCHEN)
            return
        self._starte_naechsten()

    def bis_ruhe(self, max_schritte: int = 100_000) -> None:
        """Arbeitet synchron, bis der Durchgang auf einen Befehl wartet oder endet.

        Für Tests und Selbsttest mit Testuhr. Wartet zwischen Abfragen per ``uhr.sleep``.

        Raises
        ------
        RuntimeError
            Wenn nach ``max_schritte`` Schritten keine Ruhe erreicht ist.
        """
        for _ in range(max_schritte):
            self.schritt()
            if not self.ist_aktiv() and self._befehle.empty():
                return
            if self.braucht_takt():
                self._uhr.sleep(self._konf.poll_s)
        raise RuntimeError(f"Steuerung: keine Ruhe nach {max_schritte} Schritten")

    # --- Geräte-Thread -----------------------------------------------------------------

    def starte_thread(self) -> None:
        """Startet den Geräte-Thread (einmalig).

        Raises
        ------
        RuntimeError
            Wenn der Thread schon läuft.
        """
        if self._thread is not None and self._thread.is_alive():
            raise RuntimeError("Steuerung: Geräte-Thread läuft bereits")
        self._thread_ende.clear()
        self._thread = threading.Thread(
            target=self._thread_schleife, name="ldv-geraet", daemon=True
        )
        self._thread.start()

    def beende_thread(self, timeout_s: float = 5.0) -> bool:
        """Beendet den Geräte-Thread; ``True``, wenn er innerhalb ``timeout_s`` endete.

        Ein laufender Durchgang wird dabei nicht abgebrochen; vorher ``brich_ab`` senden.
        """
        thread = self._thread
        if thread is None:
            return True
        self._thread_ende.set()
        self._signal.set()
        thread.join(timeout_s)
        return not thread.is_alive()

    def _thread_schleife(self) -> None:
        while not self._thread_ende.is_set():
            self.schritt()
            if self.braucht_takt():
                self._uhr.sleep(self._konf.poll_s)
            elif not self.ist_aktiv():
                self._signal.wait(self._konf.poll_s)
                self._signal.clear()

    def _aufruf(
        self, methode: str, ausfuehren: Callable[[], _T], *, grenze_s: float | None = None
    ) -> _T:
        """Führt einen Geräteaufruf aus und misst seine Dauer (Nutzerentscheidung K-U2b).

        Überschreitet die Dauer ``grenze_s`` (Standard: ``aufruf_grenze_s``), wird ein
        :class:`ZeitlimitFehler` ausgelöst, auch wenn der Aufruf normal zurückkehrte oder
        einen anderen Gerätefehler meldete. Die Aufrufer behandeln ihn als Hänger.
        """
        grenze = self._konf.aufruf_grenze_s if grenze_s is None else grenze_s
        beginn_s = self._uhr.monotonic()
        try:
            ergebnis = ausfuehren()
        except ZeitlimitFehler:
            raise
        except GeraeteFehler as fehler:
            dauer_s = self._uhr.monotonic() - beginn_s
            if dauer_s > grenze:
                raise ZeitlimitFehler(
                    f"Geräteaufruf '{methode}' dauerte {dauer_s:.1f} s (Grenze {grenze:g} s) "
                    f"und scheiterte: {fehler.text}",
                    methode=methode,
                ) from fehler
            raise
        dauer_s = self._uhr.monotonic() - beginn_s
        if dauer_s > grenze:
            raise ZeitlimitFehler(
                f"Geräteaufruf '{methode}' dauerte {dauer_s:.1f} s (Grenze {grenze:g} s)",
                methode=methode,
            )
        return ergebnis

    def _markiere_verloren(self, haengt: bool) -> None:
        """Gerät gilt als verloren; bei ``haengt`` wird es auch zum Trennen nicht mehr gerufen."""
        self._geraet_verloren = True
        if haengt:
            self._aufruf_haengt = True

    def _behandle_internen_fehler(self, text: str) -> None:
        """Interner Fehler: sichtbar machen und die Steuerung bedienbar halten (best effort).

        Jeder Teilschritt ist einzeln abgesichert, damit ein Folgefehler die übrigen nicht
        verhindert. Folgefehler stehen im Ereignis ``interner_fehler``.
        """
        folgefehler: list[str] = []
        with self._sperre:
            self._interner_fehler = text
        aktiv = self._aktiv
        if aktiv is not None:
            try:
                self._protokolliere(
                    aktiv,
                    MessungZustand.FEHLER,
                    (FehlerArt.GERAET_UNKLAR, "Interner Fehler der Steuerung", None),
                    None,
                )
            except Exception as exc:  # best effort, Folgefehler wird gemeldet
                folgefehler.append(f"Messprotokoll: {exc!r}")
            try:
                if self._ws.hole(aktiv.messung.id).zustand is MessungZustand.LAEUFT:
                    self._setze_info(
                        aktiv.messung.id,
                        fehlerart=FehlerArt.GERAET_UNKLAR.value,
                        fehlertext="Interner Fehler der Steuerung",
                    )
                    self._eintrag_zustand(aktiv.messung.id, MessungZustand.FEHLER, von="laeuft")
            except Exception as exc:  # best effort, Folgefehler wird gemeldet
                folgefehler.append(f"Eintragszustand: {exc!r}")
        geraet = self._geraet
        if self._freigabe_gesetzt and not self._aufruf_haengt and geraet is not None:
            try:
                self._aufruf("setze_messfreigabe", lambda: geraet.setze_messfreigabe(False))
            except ZeitlimitFehler as exc:
                # Hänger: Gerät auch zum Trennen nicht mehr ansprechen.
                self._markiere_verloren(haengt=True)
                folgefehler.append(f"Messfreigabe entziehen hängt: {exc!r}")
            except Exception as exc:  # best effort, Folgefehler wird gemeldet
                folgefehler.append(f"Messfreigabe entziehen: {exc!r}")
        self._freigabe_gesetzt = False
        self._geraet_verloren = True
        with self._sperre:
            self._aktiv = None
            self._fortschritt = None
            self._fehler_offen = "Interner Fehler der Steuerung; PSV manuell prüfen"
            self._fehler_eintrag_id = aktiv.messung.id if aktiv is not None else None
            if self._zustand is not DurchgangZustand.GERAET_UNKLAR:
                alt = self._zustand
                self._zustand = DurchgangZustand.GERAET_UNKLAR
            else:
                alt = None
        try:
            self._melde(
                "interner_fehler",
                "Interner Fehler der Steuerung",
                traceback=text,
                folgefehler=folgefehler,
            )
            if alt is not None:
                self._melde(
                    "durchgang_zustand",
                    f"Durchgang: {alt.value} -> {DurchgangZustand.GERAET_UNKLAR.value}",
                    von=alt.value,
                    nach=DurchgangZustand.GERAET_UNKLAR.value,
                )
        except Exception:  # Meldeweg selbst defekt: Zustand ist trotzdem gesetzt
            with self._sperre:
                self._interner_fehler = (
                    text + "\n(Meldung fehlgeschlagen)\n" + traceback.format_exc()
                )

    # --- Ereignisse und Zustände -------------------------------------------------------

    def _melde(self, art: str, text: str, **daten: object) -> None:
        ereignis = AblaufEreignis(art=art, text=text, daten=daten)
        protokoll = self._ereignisprotokoll
        if protokoll is not None:
            try:
                protokoll.schreibe(self._uhr.jetzt(), art, {"text": text, **daten})
            except OSError as fehler:
                # Nicht still: als eigenes Ereignis an die Sitzung, Durchgang läuft weiter.
                if self._bei_ereignis is not None:
                    self._bei_ereignis(
                        AblaufEreignis(
                            art="fehler",
                            text=f"Ereignisprotokoll nicht schreibbar: {fehler}",
                        )
                    )
        if self._bei_ereignis is not None:
            self._bei_ereignis(ereignis)

    def _wechsle(self, neu: DurchgangZustand) -> None:
        alt = self._zustand
        if alt is neu:
            return
        with self._sperre:
            self._zustand = neu
        self._melde(
            "durchgang_zustand",
            f"Durchgang: {alt.value} -> {neu.value}",
            von=alt.value,
            nach=neu.value,
        )

    def _setze_info(self, eintrag_id: UUID, **werte: object) -> None:
        with self._sperre:
            alt = self._laufinfo.get(eintrag_id, EintragLaufinfo())
            self._laufinfo[eintrag_id] = replace(alt, **werte)  # type: ignore[arg-type]

    def _eintrag_zustand(
        self, eintrag_id: UUID, neu: MessungZustand | PausenpunktZustand, *, von: str
    ) -> None:
        self._ws.zustand_setzen(eintrag_id, neu)
        self._melde(
            "eintrag_zustand",
            f"Eintrag {eintrag_id}: {von} -> {neu.value}",
            eintrag_id=str(eintrag_id),
            von=von,
            nach=neu.value,
        )

    def _verwerfen(self, befehl: str, grund: str) -> None:
        self._melde("befehl_verworfen", f"Befehl '{befehl}' verworfen: {grund}", befehl=befehl)

    # --- Befehlsverarbeitung -----------------------------------------------------------

    def _verarbeite(self, befehl: _Befehl) -> None:
        z = self._zustand
        if isinstance(befehl, _Start):
            self._melde("befehl", "Start", befehl="start")
            self._starte_durchgang(befehl.auftrag)
            return
        if isinstance(befehl, _Tausch):
            self._melde("befehl", "Gerät tauschen", befehl="geraet_tauschen")
            self._tausche(befehl)
            return
        if isinstance(befehl, _Entscheidung):
            self._melde("befehl", "Fehlerentscheidung", befehl=befehl.entscheidung.value)
            if z is not DurchgangZustand.WARTET_AUF_ENTSCHEIDUNG:
                self._verwerfen(befehl.entscheidung.value, f"Zustand {z.value}")
                return
            self._fehlerentscheidung(befehl.entscheidung)
            return
        art = befehl.art
        self._melde("befehl", art, befehl=art)
        if art == "pause":
            if z is DurchgangZustand.LAEUFT:
                self._wechsle(DurchgangZustand.PAUSE_ANGEFORDERT)
            else:
                self._verwerfen(art, f"Zustand {z.value}")
        elif art == "fortsetzen":
            if z is DurchgangZustand.PAUSIERT:
                self._wechsle(DurchgangZustand.LAEUFT)
            else:
                self._verwerfen(art, f"Zustand {z.value}")
        elif art == "abbrechen":
            self._abbrechen()
        elif art == "bestaetigen":
            if z is DurchgangZustand.WARTET_AUF_BESTAETIGUNG and self._pausenpunkt_id:
                pp = self._pausenpunkt_id
                self._eintrag_zustand(pp, PausenpunktZustand.ERLEDIGT, von="erreicht")
                with self._sperre:
                    self._pausenpunkt_id = None
                self._wechsle(DurchgangZustand.LAEUFT)
            else:
                self._verwerfen(art, f"Zustand {z.value}")
        elif art == "quittieren":
            if z is DurchgangZustand.BEENDET:
                with self._sperre:
                    self._ergebnis = None
                    self._fortschritt = None
                self._wechsle(DurchgangZustand.BEREIT)
            else:
                self._verwerfen(art, f"Zustand {z.value}")
        elif art == "verbinden":
            self._verbinden()
        else:  # trennen
            self._trennen()

    def _tausche(self, befehl: _Tausch) -> None:
        z = self._zustand
        if z not in (
            DurchgangZustand.BEREIT,
            DurchgangZustand.BEENDET,
            DurchgangZustand.GERAET_UNKLAR,
        ):
            self._verwerfen("geraet_tauschen", f"Zustand {z.value}")
            return
        alt = self._geraet
        if (
            alt is not None
            and z is not DurchgangZustand.GERAET_UNKLAR
            and not self._geraet_verloren
        ):
            try:
                self._aufruf("trenne", alt.trenne)
            except ZeitlimitFehler as fehler:
                # Altes Gerät wird verworfen; es wird nicht erneut angesprochen.
                self._melde("fehler", f"Trennen des alten Geräts hängt: {fehler.text}")
            except GeraeteFehler as fehler:
                self._melde("fehler", f"Trennen des alten Geräts fehlgeschlagen: {fehler.text}")
        try:
            neu = befehl.erzeuger()
        except (GeraeteFehler, ValueError, OSError) as fehler:
            with self._sperre:
                self._geraet = None
                self._verbindung = None
                self._geraete_stand = None
                self._kenntnis = {}
                self._geraet_nr += 1
            self._melde("fehler", f"Gerät nicht erzeugt ({befehl.betriebsart}): {fehler}")
            return
        with self._sperre:
            self._geraet = neu
            self._betriebsart = befehl.betriebsart
            self._verbindung = None
            self._geraete_stand = None
            if z is DurchgangZustand.GERAET_UNKLAR or self._geraet_verloren:
                self._kenntnis = {}  # Zustand der PSV unklar: nichts übernehmen
            # Sonst bleibt das Wissen mit seiner Herkunft erhalten; ob es für das neue
            # Gerät gilt, entscheidet geraetestand.uebertragbar (K-U5b).
            self._geraet_nr += 1
        self._aufruf_haengt = False
        self._geraet_verloren = False
        self._melde(
            "geraet_getauscht",
            f"Betriebsart {befehl.betriebsart}",
            betriebsart=befehl.betriebsart,
        )
        if z is DurchgangZustand.GERAET_UNKLAR:
            self._verlasse_geraet_unklar()

    def _verbinden(self) -> None:
        if self._zustand not in (DurchgangZustand.BEREIT, DurchgangZustand.BEENDET):
            self._verwerfen("verbinden", f"Zustand {self._zustand.value}")
            return
        if self._geraet is None:
            self._verwerfen("verbinden", "kein Gerät vorhanden")
            return
        if self._geraet_verloren:
            self._verwerfen(
                "verbinden",
                "Gerät nach GERAET_UNKLAR verloren; erst Gerät neu erzeugen (Gerätetausch)",
            )
            return
        try:
            info = self._aufruf("verbinde", self.geraet.verbinde)
        except ZeitlimitFehler as fehler:
            # Hänger beim Verbinden: Gerät verloren, kein weiterer Aufruf (auch nicht trenne).
            self._markiere_verloren(haengt=True)
            with self._sperre:
                self._verbindung = None
            self._melde(
                "fehler",
                f"Verbinden hängt; Gerät verloren: {fehler.text}",
                art_fehler=FehlerArt.GERAET_UNKLAR.value,
            )
            return
        except GeraeteFehler as fehler:
            with self._sperre:
                self._verbindung = None
            self._melde("fehler", f"Verbinden fehlgeschlagen: {fehler.text}", art_fehler="geraet")
            return
        try:
            stand = self._aufruf("lies_einstellungsstand", self.geraet.lies_einstellungsstand)
        except ZeitlimitFehler as fehler:
            # Wie ein Hänger beim Verbinden: Gerät verloren (Nutzerentscheidung).
            self._markiere_verloren(haengt=True)
            with self._sperre:
                self._verbindung = None
                self._geraete_stand = None
            self._melde(
                "fehler",
                f"Lesen des Gerätestands beim Verbinden hängt; Gerät verloren: {fehler.text}",
                art_fehler=FehlerArt.GERAET_UNKLAR.value,
            )
            return
        except GeraeteFehler as fehler:
            geraete_stand = GeraeteStand(
                messpunkte=None,
                generator=UNBEKANNTER_GENERATOR,
                quelle="beim Verbinden",
                zeit=self._uhr.jetzt(),
                fehler=fehler.text,
            )
            self._melde("fehler", f"Gerätestand beim Verbinden nicht lesbar: {fehler.text}")
        else:
            geraete_stand = self._geraete_stand_aus(stand, "beim Verbinden")
        with self._sperre:
            self._verbindung = info
            self._geraete_stand = geraete_stand
        self._melde(
            "verbindung",
            f"Verbunden: {info.psv_version}",
            psv_version=info.psv_version,
            zustand=info.zustand.value,
        )

    def _geraete_stand_aus(self, stand: EinstellungsStand, quelle: str) -> GeraeteStand:
        return GeraeteStand(
            messpunkte=stand.messpunkte_anzahl,
            generator=generator_aus_stand(stand),
            quelle=quelle,
            zeit=self._uhr.jetzt(),
        )

    def _trennen(self) -> None:
        z = self._zustand
        if z not in (
            DurchgangZustand.BEREIT,
            DurchgangZustand.BEENDET,
            DurchgangZustand.GERAET_UNKLAR,
        ):
            self._verwerfen("trennen", f"Zustand {z.value}")
            return
        geraet = self._geraet
        if geraet is not None and self._aufruf_haengt:
            self._melde(
                "verbindung",
                "Gerät nach hängendem Aufruf nicht mehr angesprochen; Verbindung verworfen",
            )
        elif geraet is not None:
            try:
                self._aufruf("trenne", geraet.trenne)
            except ZeitlimitFehler as fehler:
                self._markiere_verloren(haengt=True)
                self._melde("fehler", f"Trennen hängt; Gerät verloren: {fehler.text}")
            except GeraeteFehler as fehler:
                self._melde("fehler", f"Trennen fehlgeschlagen: {fehler.text}")
        with self._sperre:
            self._verbindung = None
            self._geraete_stand = None
            self._kenntnis = {}  # nach erneutem Verbinden kann PSV anders eingestellt sein
        self._melde("verbindung", "Getrennt")
        if z is DurchgangZustand.GERAET_UNKLAR:
            self._verlasse_geraet_unklar()

    def _verlasse_geraet_unklar(self) -> None:
        """Nach Trennen bzw. Gerätetausch: offenen Durchgang beenden, sonst nach ``BEREIT``."""
        if self._durchgang_offen:
            self._beende_durchgang(DurchgangErgebnis.GERAET_UNKLAR, geraet_verloren=True)
        else:
            # z. B. interner Fehler ohne Durchgang: es gab nichts zu beenden.
            with self._sperre:
                self._fehler_offen = None
                self._fehler_eintrag_id = None
            self._wechsle(DurchgangZustand.BEREIT)

    def _abbrechen(self) -> None:
        z = self._zustand
        aktiv = self._aktiv
        if z in (DurchgangZustand.LAEUFT, DurchgangZustand.PAUSE_ANGEFORDERT):
            if aktiv is not None and aktiv.phase == "scan":
                self._wechsle(DurchgangZustand.ABBRUCH_LAEUFT)
                self._sende_stop(aktiv, "abbruch")
            elif aktiv is not None and aktiv.phase == "stop":
                # Stop läuft schon (z. B. Zeitlimit); kein zweites Stop senden.
                self._wechsle(DurchgangZustand.ABBRUCH_LAEUFT)
            else:
                self._beende_durchgang(DurchgangErgebnis.ABGEBROCHEN)
        elif z is DurchgangZustand.WARTET_AUF_BESTAETIGUNG:
            pp = self._pausenpunkt_id
            if pp is not None:
                self._eintrag_zustand(pp, PausenpunktZustand.WARTEND, von="erreicht")
                with self._sperre:
                    self._pausenpunkt_id = None
            self._beende_durchgang(DurchgangErgebnis.ABGEBROCHEN)
        elif z in (DurchgangZustand.PAUSIERT, DurchgangZustand.WARTET_AUF_ENTSCHEIDUNG):
            if z is DurchgangZustand.WARTET_AUF_ENTSCHEIDUNG:
                self._melde_entscheidung(Fehlerentscheidung.ABBRECHEN)
            self._beende_durchgang(DurchgangErgebnis.ABGEBROCHEN)
        else:
            self._verwerfen("abbrechen", f"Zustand {z.value}")

    def _melde_entscheidung(self, entscheidung: Fehlerentscheidung) -> None:
        eintrag_id = self._fehler_eintrag_id
        versuch = self._laufinfo[eintrag_id].versuch if eintrag_id in self._laufinfo else None
        self._melde(
            "fehlerentscheidung",
            f"Fehlerentscheidung: {entscheidung.value}",
            eintrag_id=str(eintrag_id),
            versuch=versuch,
            entscheidung=entscheidung.value,
            fehlerstrategie=self._strategie.bezeichnung,
        )
        with self._sperre:
            self._fehler_offen = None
            self._fehler_eintrag_id = None

    def _fehlerentscheidung(self, entscheidung: Fehlerentscheidung) -> None:
        eintrag_id = self._fehler_eintrag_id
        if entscheidung is Fehlerentscheidung.ABBRECHEN or eintrag_id is None:
            self._abbrechen()
            return
        self._melde_entscheidung(entscheidung)
        if entscheidung is Fehlerentscheidung.WIEDERHOLEN:
            self._eintrag_zustand(eintrag_id, MessungZustand.WARTEND, von="fehler")
        else:
            self._setze_info(eintrag_id, uebersprungen=True)
            self._melde(
                "uebersprungen_nach_fehler",
                f"Eintrag {eintrag_id} nach Fehler übersprungen",
                eintrag_id=str(eintrag_id),
            )
        self._weiter_nach_messung()

    def _weiter_nach_messung(self) -> None:
        if self._pause_vorgemerkt:
            self._pause_vorgemerkt = False
            self._wechsle(DurchgangZustand.PAUSIERT)
        else:
            self._wechsle(DurchgangZustand.LAEUFT)

    # --- Durchgang ---------------------------------------------------------------------

    def _starte_durchgang(self, auftrag: DurchgangsAuftrag) -> None:
        if self._zustand is not DurchgangZustand.BEREIT:
            self._verwerfen("start", f"Zustand {self._zustand.value}")
            return
        if self._verbindung is None:
            self._verwerfen("start", "keine Verbindung zum Gerät")
            return
        if auftrag.betriebsart != self._betriebsart:
            self._verwerfen(
                "start",
                f"Auftrag für Betriebsart {auftrag.betriebsart}, aktives Gerät ist "
                f"{self._betriebsart}; bitte erneut starten",
            )
            return
        if self._betriebsart == "messen" and not auftrag.messen_bestaetigt:
            self._verwerfen("start", "MESSEN ohne ausdrückliche Bestätigung des Durchgangs")
            return
        try:
            ordner = lege_durchgangsordner(
                auftrag.messdaten_wurzel, auftrag.name, self._uhr.jetzt()
            )
        except (OSError, ValueError, RuntimeError) as fehler:
            self._verwerfen("start", f"Durchgangsordner nicht anlegbar: {fehler}")
            return
        with self._sperre:
            self._auftrag = auftrag
            self._durchgang_id = uuid4()
            self._ordner = ordner
            self._ergebnis = None
            self._nummern = {}
            self._bilanz = ()
            self._punktdauer_s = None
            self._pause_vorgemerkt = False
            self._erste_trockenmessung = True
        self._ereignisprotokoll = Ereignisprotokoll(ordner / EREIGNISPROTOKOLL)
        self._melde(
            "durchgang_start",
            f"Durchgang '{auftrag.name}' gestartet",
            durchgang_id=str(self._durchgang_id),
            ordner=str(ordner),
            betriebsart=auftrag.betriebsart,
            trockenlauf=auftrag.trockenlauf,
            paket_version=self._build.paket_version,
            git_hash=self._build.git_hash,
            git_dirty=self._build.git_dirty,
            fehlerstrategie=self._strategie.bezeichnung,
            konfiguration=self._konfig_info,
            startangaben=[dict(a) for a in auftrag.startangaben],
        )
        try:
            speichere_warteschlange(
                self._ws.eintraege(),
                ordner / WARTESCHLANGENKOPIE,
                paket_version=self._build.paket_version,
                git_hash=self._build.git_hash,
                jetzt=self._uhr.jetzt,
            )
        except (OSError, ValueError) as fehler:
            self._melde("fehler", f"Warteschlangenkopie nicht geschrieben: {fehler}")
        self._durchgang_offen = True
        if auftrag.messfreigabe:
            try:
                self._aufruf("setze_messfreigabe", lambda: self.geraet.setze_messfreigabe(True))
            except ZeitlimitFehler as fehler:
                self._markiere_verloren(haengt=True)
                self._geraet_unklar(None, f"Messfreigabe setzen hängt: {fehler.text}", fehler)
                return
            except GeraeteFehler as fehler:
                self._melde("fehler", f"Messfreigabe verweigert: {fehler.text}")
                self._beende_durchgang(DurchgangErgebnis.ABGEBROCHEN)
                return
            self._freigabe_gesetzt = True
        self._wechsle(DurchgangZustand.LAEUFT)

    def _eintraege_zusammenfassung(self) -> list[dict[str, object]]:
        ergebnis: list[dict[str, object]] = []
        for e in self._ws.eintraege():
            zustand = e.zustand.value
            info = self._laufinfo.get(e.id)
            ergebnis.append(
                {
                    "eintrag_id": str(e.id),
                    "art": "messung" if isinstance(e, Messung) else "pausenpunkt",
                    "name": e.name if isinstance(e, Messung) else e.text,
                    "zustand": zustand,
                    "hinweis": _hinweis(e),
                    "uebersprungen": bool(info and info.uebersprungen),
                    "versuch": e.versuch if isinstance(e, Messung) else None,
                }
            )
        return ergebnis

    def _beende_durchgang(
        self, ergebnis: DurchgangErgebnis, *, geraet_verloren: bool = False
    ) -> None:
        if self._freigabe_gesetzt and not geraet_verloren:
            try:
                self._aufruf("setze_messfreigabe", lambda: self.geraet.setze_messfreigabe(False))
            except ZeitlimitFehler as fehler:
                self._markiere_verloren(haengt=True)
                self._geraet_unklar(None, f"Messfreigabe entziehen hängt: {fehler.text}", fehler)
                return
            except GeraeteFehler as fehler:
                self._melde("fehler", f"Messfreigabe nicht entzogen: {fehler.text}")
        self._freigabe_gesetzt = False
        self._durchgang_offen = False
        bilanz = tuple(
            e.id
            for e in self._ws.eintraege()
            if isinstance(e, Messung)
            and (e.id in self._nummern or e.zustand is MessungZustand.WARTEND)
        )
        with self._sperre:
            self._ergebnis = ergebnis
            self._fortschritt = None
            self._aktiv = None
            self._bilanz = bilanz
        self._melde(
            "durchgang_beendet",
            f"Durchgang beendet ({ergebnis.value})",
            ergebnis=ergebnis.value,
            eintraege=self._eintraege_zusammenfassung(),
        )
        self._wechsle(DurchgangZustand.BEENDET)
        self._ereignisprotokoll = None

    # --- Messung -----------------------------------------------------------------------

    def _starte_naechsten(self) -> None:
        eintrag = self._ws.naechsten_beanspruchen()
        if eintrag is None:
            self._beende_durchgang(DurchgangErgebnis.VOLLSTAENDIG)
            return
        if isinstance(eintrag, Pausenpunkt):
            self._melde(
                "eintrag_zustand",
                f"Pausenpunkt erreicht: {eintrag.text}",
                eintrag_id=str(eintrag.id),
                von="wartend",
                nach=eintrag.zustand.value,
            )
            with self._sperre:
                self._pausenpunkt_id = eintrag.id
            self._wechsle(DurchgangZustand.WARTET_AUF_BESTAETIGUNG)
            return
        self._melde(
            "eintrag_zustand",
            f"Messung gestartet: {eintrag.name} (Versuch {eintrag.versuch})",
            eintrag_id=str(eintrag.id),
            von="wartend",
            nach=eintrag.zustand.value,
            versuch=eintrag.versuch,
        )
        self._fuehre_messung_aus(eintrag)

    def _fuehre_messung_aus(self, m: Messung) -> None:
        auftrag = self._auftrag
        ordner = self._ordner
        assert auftrag is not None and ordner is not None
        nummer = self._nummern.setdefault(m.id, len(self._nummern) + 1)
        namensfehler: str | None = None
        try:
            basis = dateibasis(nummer, m.name, m.versuch)
        except ValueError as fehler:
            # M1: Name ergibt keinen Dateinamen. Ersatzname nur für Protokoll und Anzeige;
            # eine Messdatei entsteht nicht (kein Geräteaufruf).
            namensfehler = f"Kein Dateiname bildbar: {fehler}"
            basis = dateibasis(nummer, f"messung_{m.id.hex[:8]}", m.versuch)
        aktiv = _Aktiv(
            messung=m,
            position=self._ws.index_von(m.id),
            nummer=nummer,
            basis=basis,
            zielpfad=ordner / (basis + ENDUNG_MESSDATEI),
            protokollpfad=ordner / (basis + ENDUNG_PROTOKOLL),
            zeit_start=self._uhr.jetzt(),
            t_start_s=self._uhr.monotonic(),
            zeitlimit_s=m.zeitlimit_s if m.zeitlimit_s is not None else self._konf.zeitlimit_s,
        )
        with self._sperre:
            self._aktiv = aktiv
        self._setze_info(
            m.id,
            nummer=nummer,
            versuch=m.versuch,
            zeit_start=aktiv.zeit_start,
            zeit_ende=None,
            messdatei=str(aktiv.zielpfad),
            protokolldatei=str(aktiv.protokollpfad),
            fehlerart=None,
            fehlertext=None,
            uebersprungen=False,
            trockenlauf=auftrag.trockenlauf,
        )
        vorpruefung = namensfehler or self._vorpruefung(aktiv)
        if vorpruefung is not None:
            self._messung_fehler(aktiv, FehlerArt.VORPRUEFUNG, vorpruefung, None)
            return
        try:
            if self._aufruf("zustand", self.geraet.zustand) is not GeraeteZustand.GESTOPPT:
                self._messung_fehler(
                    aktiv,
                    FehlerArt.GERAET_NICHT_BEREIT,
                    "Gerät nicht bereit: Zustand ≠ gestoppt (fremde Messung?)",
                    None,
                )
                return
            self._aufruf(
                "lade_einstellungen", lambda: self.geraet.lade_einstellungen(m.einstellungsdatei)
            )
            if m.parameter:
                self._aufruf("setze_parameter", lambda: self.geraet.setze_parameter(m.parameter))
                ist = self._aufruf(
                    "lies_parameter", lambda: self.geraet.lies_parameter(tuple(m.parameter))
                )
                abweichung = self._vergleiche(aktiv, m.parameter, ist)
            else:
                abweichung = None
            stand = self._aufruf("lies_einstellungsstand", self.geraet.lies_einstellungsstand)
            aktiv.einstellungen_ist = einstellungsstand_zu_dict(stand)
            aktiv.messpunkte = stand.messpunkte_anzahl
            self._merke_einstellungsstand(aktiv, stand)
            if abweichung is not None:
                self._messung_fehler(aktiv, FehlerArt.ABWEICHUNG, abweichung, None)
                return
            if stand.modus != ERWARTETER_MODUS:
                self._messung_fehler(
                    aktiv,
                    FehlerArt.ABWEICHUNG,
                    f"Modus nach dem Laden {stand.modus!r}, erwartet {ERWARTETER_MODUS!r}",
                    None,
                )
                return
            if self._konf.einstellungen_sichern:
                ziel = str(ordner / (basis + ENDUNG_EINSTELLUNGEN))
                self._aufruf(
                    "speichere_einstellungen", lambda: self.geraet.speichere_einstellungen(ziel)
                )
            if auftrag.trockenlauf:
                self._schliesse_messung(aktiv, MessungZustand.FERTIG)
                return
            aktiv.t_scan_s = self._uhr.monotonic()
            # ScanEx blockiert evtl. bis zum Scanende: Grenze ist das Zeitlimit der Messung.
            self._aufruf(
                "starte_scan",
                lambda: self.geraet.starte_scan(str(aktiv.zielpfad)),
                grenze_s=aktiv.zeitlimit_s,
            )
            aktiv.scan_gestartet = True
            aktiv.phase = "scan"
        except ZeitlimitFehler as fehler:
            self._haenger(aktiv, fehler)
        except GeraetNichtBereitFehler as fehler:
            self._messung_fehler(aktiv, FehlerArt.GERAET_NICHT_BEREIT, fehler.text, fehler)
        except VerweigertFehler as fehler:
            self._messung_fehler(aktiv, FehlerArt.VERWEIGERT, fehler.text, fehler)
        except GeraeteFehler as fehler:
            self._messung_fehler(aktiv, FehlerArt.GERAET, fehler.text, fehler)

    def _merke_einstellungsstand(self, aktiv: _Aktiv, stand: EinstellungsStand) -> None:
        """Merkt den nach dem Laden gelesenen Stand je Einstellungsdatei (Dialog 3.9)."""
        datei = aktiv.messung.einstellungsdatei
        geraete_stand = self._geraete_stand_aus(stand, f"nach Laden von {datei}")
        with self._sperre:
            self._geraete_stand = geraete_stand
            herkunft = self._herkunft()
            if aktiv.einstellungsdatei_kennung is not None and herkunft is not None:
                self._kenntnis[pfad_schluessel(datei)] = EinstellungsKenntnis(
                    einstellungsdatei=datei,
                    kennung=aktiv.einstellungsdatei_kennung,
                    stand=geraete_stand,
                    herkunft=herkunft,
                )

    def _vorpruefung(self, aktiv: _Aktiv) -> str | None:
        """M1 ohne Gerätewirkung; Text des ersten Problems oder ``None``."""
        m = aktiv.messung
        einstellung = Path(m.einstellungsdatei)
        if einstellung.suffix.lower() != ".set":
            return f"Einstellungsdatei hat nicht die Endung .set: {einstellung}"
        if not einstellung.is_file():
            return f"Einstellungsdatei fehlt: {einstellung}"
        try:
            st = einstellung.stat()
            aktiv.einstellungsdatei_sha256 = sha256_datei(einstellung)
        except OSError as fehler:
            return f"Einstellungsdatei nicht lesbar: {fehler}"
        aktiv.einstellungsdatei_kennung = DateiKennung(
            sha256=aktiv.einstellungsdatei_sha256,
            groesse_b=st.st_size,
            mtime_ns=st.st_mtime_ns,
        )
        if aktiv.zielpfad.exists() or aktiv.protokollpfad.exists():
            return f"Zieldatei existiert bereits (nie überschreiben): {aktiv.zielpfad}"
        try:
            KATALOG.pruefe(m.parameter)
        except ValueError as fehler:
            return str(fehler)
        return None

    def _vergleiche(
        self,
        aktiv: _Aktiv,
        soll: Mapping[str, ParameterWert],
        ist: Mapping[str, ParameterWert],
    ) -> str | None:
        """M5: Soll/Ist je Parameter; füllt ``geaenderte_parameter``; Text der Abweichungen."""
        probleme: list[str] = []
        for schluessel, soll_wert in soll.items():
            spec = KATALOG.spec(schluessel)
            ist_wert = ist.get(schluessel)
            aktiv.geaenderte.append(
                {
                    "schluessel": schluessel,
                    "einheit": spec.einheit,
                    "soll": soll_wert,
                    "ist": ist_wert,
                }
            )
            if ist_wert is None or not spec.stimmt_ueberein(soll_wert, ist_wert):
                probleme.append(f"{schluessel}: Soll {soll_wert!r}, Ist {ist_wert!r}")
        if probleme:
            return "Abweichung beim Zurücklesen: " + "; ".join(probleme)
        return None

    def _pruefe_scan(self, aktiv: _Aktiv) -> None:
        jetzt_s = self._uhr.monotonic()
        if aktiv.phase == "stop":
            try:
                zustand = self._aufruf("zustand", self.geraet.zustand)
            except ZeitlimitFehler as fehler:
                self._haenger(aktiv, fehler)
                return
            except GeraeteFehler:
                zustand = None
            if zustand is GeraeteZustand.GESTOPPT:
                self._nach_stop(aktiv)
            elif aktiv.t_stop_s is not None and jetzt_s - aktiv.t_stop_s > self._konf.stop_frist_s:
                self._geraet_unklar(
                    aktiv,
                    f"Stop greift nicht innerhalb von {self._konf.stop_frist_s:g} s",
                )
            return
        try:
            zustand = self._aufruf("zustand", self.geraet.zustand)
            for meldung in self._aufruf("hole_meldungen", self.geraet.hole_meldungen):
                aktiv.meldungen.append(
                    {"stil": meldung.stil, "text": meldung.text, "antwort": meldung.antwort}
                )
            fortschritt = self._aufruf("fortschritt", self.geraet.fortschritt)
        except ZeitlimitFehler as fehler:
            self._haenger(aktiv, fehler)
            return
        except GeraeteFehler as fehler:
            aktiv.fehler = (FehlerArt.GERAET, fehler.text, fehler)
            self._melde("fehler", f"Gerätefehler im Scan: {fehler.text}")
            self._sende_stop(aktiv, "fehler")
            return
        if zustand is GeraeteZustand.GESTOPPT:
            self._scan_ende(aktiv)
            return
        vergangen = jetzt_s - (aktiv.t_scan_s if aktiv.t_scan_s is not None else jetzt_s)
        if vergangen > aktiv.zeitlimit_s:
            aktiv.fehler = (
                FehlerArt.ZEITLIMIT,
                f"Zeitlimit {aktiv.zeitlimit_s:g} s überschritten",
                None,
            )
            self._sende_stop(aktiv, "zeitlimit")
            return
        self._aktualisiere_fortschritt(aktiv, vergangen, fortschritt)

    def _aktualisiere_fortschritt(
        self, aktiv: _Aktiv, vergangen_s: float, fortschritt: Fortschritt | None
    ) -> None:
        punktdauer = self._punktdauer_s or self._konf.punktdauer_schaetzung_s
        rest_limit = max(aktiv.zeitlimit_s - vergangen_s, 0.0)
        if isinstance(fortschritt, Fortschritt) and fortschritt.punkte_gesamt > 0:
            aktiv.fortschritt_quelle = fortschritt.quelle
            offen = max(fortschritt.punkte_gesamt - fortschritt.punkte_erledigt, 0)
            stand = FortschrittStand(
                messung_id=aktiv.messung.id,
                anteil=min(max(fortschritt.punkte_erledigt / fortschritt.punkte_gesamt, 0.0), 1.0),
                geschaetzt=False,
                quelle=fortschritt.quelle,
                restzeit_s=offen * punktdauer,
                zeitlimit_rest_s=rest_limit,
            )
        elif aktiv.messpunkte:
            dauer = aktiv.messpunkte * punktdauer
            stand = FortschrittStand(
                messung_id=aktiv.messung.id,
                anteil=min(vergangen_s / dauer, 1.0),
                geschaetzt=True,
                quelle="zeitschaetzung",
                restzeit_s=max(dauer - vergangen_s, 0.0),
                zeitlimit_rest_s=rest_limit,
            )
        else:
            stand = FortschrittStand(
                messung_id=aktiv.messung.id,
                anteil=None,
                geschaetzt=True,
                quelle="zeitschaetzung",
                restzeit_s=None,
                zeitlimit_rest_s=rest_limit,
            )
        with self._sperre:
            self._fortschritt = stand

    def _sende_stop(self, aktiv: _Aktiv, grund: str) -> None:
        try:
            gesendet = self._aufruf("stoppe", self.geraet.stoppe)
        except ZeitlimitFehler as fehler:
            self._haenger(aktiv, fehler)
            return
        except GeraeteFehler as fehler:
            self._geraet_unklar(aktiv, f"Stop fehlgeschlagen: {fehler.text}")
            return
        aktiv.phase = "stop"
        aktiv.stop_grund = grund
        aktiv.stop_gesendet = gesendet
        aktiv.t_stop_s = self._uhr.monotonic()
        self._melde(
            "stop",
            f"Stop {'gesendet' if gesendet else 'nicht nötig (kein eigener Scan aktiv)'}",
            grund=grund,
            gesendet=gesendet,
        )

    def _nach_stop(self, aktiv: _Aktiv) -> None:
        if aktiv.stop_grund == "fehler" or (
            aktiv.stop_grund == "zeitlimit" and aktiv.stop_gesendet
        ):
            assert aktiv.fehler is not None
            art, text, fehler = aktiv.fehler
            self._messung_fehler(aktiv, art, text, fehler)
            return
        if aktiv.stop_grund == "abbruch" and aktiv.stop_gesendet:
            self._schliesse_messung(aktiv, MessungZustand.ABGEBROCHEN)
            return
        # Scan endete von selbst, bevor Stop wirken musste.
        aktiv.fehler = None
        self._scan_ende(aktiv)

    def _scan_ende(self, aktiv: _Aktiv) -> None:
        if not aktiv.zielpfad.is_file():
            self._messung_fehler(
                aktiv,
                FehlerArt.KEINE_DATEI,
                f"Messdatei fehlt nach dem Scan: {aktiv.zielpfad}",
                None,
            )
            return
        if aktiv.t_scan_s is not None and aktiv.messpunkte:
            dauer = self._uhr.monotonic() - aktiv.t_scan_s
            if dauer > 0:
                self._punktdauer_s = dauer / aktiv.messpunkte
        self._schliesse_messung(aktiv, MessungZustand.FERTIG)

    def _haenger(self, aktiv: _Aktiv, fehler: ZeitlimitFehler) -> None:
        """Ein Geräteaufruf hing (Plan 2.3): ``GERAET_UNKLAR`` ohne Strategie und ohne Stop.

        Kein vorsorgliches ``stoppe()``, kein Wiederholen: Das Gerät hat gerade nicht
        geantwortet; jeder weitere Aufruf könnte erneut hängen.
        """
        self._markiere_verloren(haengt=True)
        methode = fehler.methode or "unbekannt"
        self._geraet_unklar(aktiv, f"Geräteaufruf '{methode}' hängt: {fehler.text}", fehler)

    def _geraet_unklar(
        self, aktiv: _Aktiv | None, text: str, fehler: BaseException | None = None
    ) -> None:
        """Gerät verloren: danach keine Geräteaufrufe mehr.

        Lief eine Messung, wird ihr Protokoll geschrieben und sie wird ``FEHLER``. Der
        Durchgang wartet in ``GERAET_UNKLAR`` auf Trennen oder Gerätetausch.
        """
        self._melde("fehler", f"Gerät unklar: {text}", art_fehler=FehlerArt.GERAET_UNKLAR.value)
        if aktiv is not None:
            self._protokolliere(
                aktiv, MessungZustand.FEHLER, (FehlerArt.GERAET_UNKLAR, text, fehler), None
            )
            self._setze_info(
                aktiv.messung.id, fehlerart=FehlerArt.GERAET_UNKLAR.value, fehlertext=text
            )
            self._eintrag_zustand(aktiv.messung.id, MessungZustand.FEHLER, von="laeuft")
        with self._sperre:
            self._aktiv = None
            self._fortschritt = None
            self._fehler_offen = text
            self._fehler_eintrag_id = aktiv.messung.id if aktiv is not None else None
        self._freigabe_gesetzt = False  # Gerät verloren; Sitzung baut es neu (Vertrag)
        self._geraet_verloren = True
        self._melde(
            "durchgang_beendet",
            "Gerät unklar: PSV manuell prüfen; nur Trennen möglich",
            ergebnis=DurchgangErgebnis.GERAET_UNKLAR.value,
            eintraege=self._eintraege_zusammenfassung(),
        )
        self._wechsle(DurchgangZustand.GERAET_UNKLAR)

    def _messung_fehler(
        self,
        aktiv: _Aktiv,
        art: FehlerArt,
        text: str,
        fehler: BaseException | None,
    ) -> None:
        m = aktiv.messung
        if self._zustand is DurchgangZustand.ABBRUCH_LAEUFT:
            # Abbruch läuft bereits: keine Strategie, keine Entscheidung nötig.
            reaktion = FehlerReaktion.ABBRECHEN
            entscheidung = "entfaellt_abbruch"
        else:
            ereignis = FehlerEreignis(art=art, text=text, messung=m, gestartet=aktiv.scan_gestartet)
            reaktion = self._strategie.entscheide(ereignis)
            entscheidung = (
                "ausstehend" if reaktion is FehlerReaktion.ANHALTEN_UND_FRAGEN else reaktion.value
            )
        self._melde(
            "fehler",
            f"Messung '{m.name}' (Versuch {m.versuch}): {text}",
            eintrag_id=str(m.id),
            art_fehler=art.value,
            reaktion=reaktion.value,
        )
        self._protokolliere(aktiv, MessungZustand.FEHLER, (art, text, fehler), entscheidung)
        self._merke_trockenlauf(m, erfolgreich=False)
        self._setze_info(m.id, fehlerart=art.value, fehlertext=text)
        self._eintrag_zustand(m.id, MessungZustand.FEHLER, von="laeuft")
        with self._sperre:
            self._aktiv = None
            self._fortschritt = None
        if self._zustand is DurchgangZustand.ABBRUCH_LAEUFT:
            self._beende_durchgang(DurchgangErgebnis.ABGEBROCHEN)
            return
        if self._zustand is DurchgangZustand.PAUSE_ANGEFORDERT:
            self._pause_vorgemerkt = True
        if reaktion is FehlerReaktion.ANHALTEN_UND_FRAGEN:
            with self._sperre:
                self._fehler_offen = text
                self._fehler_eintrag_id = m.id
            self._wechsle(DurchgangZustand.WARTET_AUF_ENTSCHEIDUNG)
        elif reaktion is FehlerReaktion.UEBERSPRINGEN:
            self._setze_info(m.id, uebersprungen=True)
            self._melde(
                "uebersprungen_nach_fehler",
                f"Eintrag {m.id} nach Fehler übersprungen (Strategie)",
                eintrag_id=str(m.id),
            )
            self._weiter_nach_messung()
        else:
            self._beende_durchgang(DurchgangErgebnis.ABGEBROCHEN)

    def _merke_trockenlauf(self, messung: Messung, *, erfolgreich: bool) -> None:
        """Ergebnis der ersten Messung eines Trockenlaufs (Voraussetzung für MESSEN).

        Gemerkt wird die eingefrorene Definition; die Sitzung bindet die Freischaltung
        daran (erlischt bei Änderung des ersten Eintrags oder neuer Warteschlange).
        """
        auftrag = self._auftrag
        if auftrag is None or not auftrag.trockenlauf or not self._erste_trockenmessung:
            return
        self._erste_trockenmessung = False
        with self._sperre:
            self._trockenlauf_messung = messung if erfolgreich else None

    def _schliesse_messung(self, aktiv: _Aktiv, status: MessungZustand) -> None:
        m = aktiv.messung
        auftrag = self._auftrag
        trocken = auftrag is not None and auftrag.trockenlauf
        self._protokolliere(aktiv, status, None, None)
        self._eintrag_zustand(m.id, status, von="laeuft")
        with self._sperre:
            self._aktiv = None
            self._fortschritt = None
        self._merke_trockenlauf(m, erfolgreich=trocken and status is MessungZustand.FERTIG)
        z = self._zustand
        if z is DurchgangZustand.ABBRUCH_LAEUFT or status is MessungZustand.ABGEBROCHEN:
            self._beende_durchgang(DurchgangErgebnis.ABGEBROCHEN)
        elif z is DurchgangZustand.PAUSE_ANGEFORDERT:
            self._wechsle(DurchgangZustand.PAUSIERT)

    def _protokolliere(
        self,
        aktiv: _Aktiv,
        status: MessungZustand,
        fehler: tuple[FehlerArt, str, BaseException | None] | None,
        entscheidung: str | None,
    ) -> None:
        """M12: Messprotokoll schreiben (immer); Fehler beim Schreiben werden gemeldet."""
        m = aktiv.messung
        auftrag = self._auftrag
        info = self._verbindung
        ende = self._uhr.jetzt()
        trocken = auftrag is not None and auftrag.trockenlauf
        sha: str | None = None
        sha_grund: str | None
        if not aktiv.scan_gestartet:
            sha_grund = "Kein Scan gestartet; Datei stammt nicht aus diesem Messversuch"
        elif not aktiv.zielpfad.is_file():
            sha_grund = "Messdatei nicht vorhanden"
        else:
            try:
                sha = sha256_datei(aktiv.zielpfad)
                sha_grund = None
            except OSError as exc:
                sha_grund = f"Hash nicht verfügbar: {exc}"
        status_text = "trockenlauf" if trocken and status is MessungZustand.FERTIG else status.value
        einschraenkungen = [EINSCHRAENKUNG_VOLLSTAENDIGKEIT]
        if self._build.git_dirty:
            einschraenkungen.append("Softwarestand mit nicht eingecheckten Änderungen (git_dirty)")
        daten: dict[str, object] = {
            "schema_version": SCHEMA_VERSION,
            "messung_id": str(m.id),
            "name": m.name,
            "versuch": m.versuch,
            "durchgang_id": str(self._durchgang_id),
            "position": aktiv.position,
            "messdatei": str(aktiv.zielpfad),
            "messdatei_sha256": sha,
            "messdatei_sha256_grund": sha_grund,
            "status": status_text,
            "fehler": fehler_zu_dict(fehler[0].value, fehler[1], fehler[2]) if fehler else None,
            "fehlerstrategie": self._strategie.bezeichnung,
            "fehlerentscheidung": entscheidung,
            "zeit_start": zeitstempel(aktiv.zeit_start),
            "zeit_ende": zeitstempel(ende),
            "dauer_s": self._uhr.monotonic() - aktiv.t_start_s,
            "zeitlimit_s": aktiv.zeitlimit_s,
            "paket_version": self._build.paket_version,
            "git_hash": self._build.git_hash,
            "git_hash_grund": self._build.grund,
            "git_dirty": self._build.git_dirty,
            "psv_version": info.psv_version if info else None,
            "betriebsart": auftrag.betriebsart if auftrag else None,
            "hardware": dict(info.hardware) if info else None,
            "messpunkte_anzahl": aktiv.messpunkte,
            "einstellungsdatei": {
                "pfad": m.einstellungsdatei,
                "sha256": aktiv.einstellungsdatei_sha256,
            },
            "lademaske": info.lademaske if info else None,
            "geaenderte_parameter": list(aktiv.geaenderte)
            or [
                {"schluessel": k, "einheit": KATALOG.spec(k).einheit, "soll": v, "ist": None}
                for k, v in m.parameter.items()
            ],
            "einstellungen_ist": aktiv.einstellungen_ist,
            "meldungen": list(aktiv.meldungen),
            "meldungen_hinweis": MELDUNGEN_HINWEIS,
            "fortschritt_quelle": aktiv.fortschritt_quelle,
            "einschraenkungen": einschraenkungen,
            "konfiguration": self._konfig_info,
        }
        try:
            schreibe_messprotokoll(aktiv.protokollpfad, daten)
        except (OSError, ValueError) as exc:
            self._melde("fehler", f"Messprotokoll nicht geschrieben: {exc}", eintrag_id=str(m.id))
        self._setze_info(m.id, zeit_ende=ende)
