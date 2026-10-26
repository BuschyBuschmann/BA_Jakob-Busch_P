"""Sitzungsfassade für die Oberfläche (Plan P2, 1 und 2.5).

Die Sitzung hält Warteschlange, Steuerung, Gerät und Betriebsart. Die Oberfläche spricht
nur mit ihr:

* :meth:`Sitzung.zustandsbild` liefert ein unveränderliches :class:`Zustandsbild`
  (jederzeit aus jedem Thread, blockiert nicht durch Geräteaufrufe);
* :meth:`Sitzung.hole_ereignisse` liefert die Ereignisse seit dem letzten Abholen in
  Reihenfolge; jedes trägt das Zustandsbild unmittelbar nach dem Ereignis;
* Befehlsmethoden prüfen offensichtliche Vorbedingungen sofort (``ValueError`` mit Grund)
  und reichen den Befehl an den Geräte-Thread weiter.

Betriebsarten (Plan P2, 6): Umschalten heißt, das Gerät im Geräte-Thread neu zu erzeugen
(Vertrag in ``geraet/schnittstelle.py``). ``MESSEN`` setzt die Voraussetzungen aus
:meth:`Sitzung.messen_voraussetzungen` voraus, ein Durchgang in ``MESSEN`` zusätzlich die
ausdrückliche Bestätigung (``messen_bestaetigt=True``).
"""

from __future__ import annotations

import contextlib
import os
import queue
import threading
import traceback
from collections.abc import Callable, Mapping
from dataclasses import dataclass, field
from datetime import datetime
from enum import StrEnum
from pathlib import Path
from uuid import UUID

from ldv_automation.ablauf.fehlerstrategie import Fehlerstrategie
from ldv_automation.ablauf.steuerung import (
    AblaufEreignis,
    AblaufKonfiguration,
    AblaufStand,
    DurchgangErgebnis,
    DurchgangsAuftrag,
    DurchgangZustand,
    Fehlerentscheidung,
    FortschrittStand,
    Steuerung,
)
from ldv_automation.ablauf.uhr import Echtzeituhr, Uhr
from ldv_automation.domaene.eintraege import Eintrag, Messung, MessungZustand, Pausenpunkt
from ldv_automation.domaene.parameter import ParameterWert
from ldv_automation.domaene.warteschlange import Warteschlange
from ldv_automation.geraet.schnittstelle import GeraeteInfo, GeraeteZustand, Messgeraet
from ldv_automation.persistenz.warteschlangendatei import (
    lade_warteschlange,
    speichere_warteschlange,
)
from ldv_automation.protokoll.version import BuildInfo, ermittle_build_info


class Betriebsart(StrEnum):
    """Betriebsart der Sitzung (Plan P2, 6). Der Wert wird dem Gerät übergeben."""

    SIMULATOR = "simulator"
    NUR_LESEN = "nur_lesen"
    TROCKENLAUF = "trockenlauf"
    MESSEN = "messen"


GeraeteFabrik = Callable[[Betriebsart], Messgeraet]
"""Erzeugt das Gerät für eine Betriebsart (wird im Geräte-Thread aufgerufen)."""


@dataclass(frozen=True, kw_only=True)
class Voraussetzung:
    """Eine Voraussetzung für ``MESSEN`` (Plan P2, 6)."""

    name: str
    erfuellt: bool
    text: str


@dataclass(frozen=True, kw_only=True)
class EintragBild:
    """Anzeigedaten eines Eintrags (unveränderlich).

    ``nummer`` ist die laufende Nummer im Durchgang (ab 1, ``None`` vor dem ersten Start).
    ``set_fehlt`` ist nur für wartende Messungen geprüft.
    """

    art: str
    id: UUID
    name: str
    text: str
    einstellungsdatei: str | None
    parameter: Mapping[str, ParameterWert]
    zeitlimit_s: float | None
    notiz: str
    zustand: str
    versuch: int | None
    nummer: int | None
    fehlerart: str | None
    fehlertext: str | None
    zeit_start: datetime | None
    zeit_ende: datetime | None
    messdatei: str | None
    protokolldatei: str | None
    uebersprungen: bool
    trockenlauf: bool
    set_fehlt: bool


@dataclass(frozen=True, kw_only=True)
class Zustandsbild:
    """Unveränderliches Bild des Sitzungszustands für die Oberfläche (R-031)."""

    revision: int
    durchgang: DurchgangZustand
    ergebnis: DurchgangErgebnis | None
    betriebsart: Betriebsart
    verbindung: GeraeteInfo | None
    eintraege: tuple[EintragBild, ...]
    fortschritt: FortschrittStand | None
    waechter_s: float | None
    fehlerentscheidung_offen: bool
    fehlertext: str | None
    fehler_eintrag_id: UUID | None
    pausenpunkt_id: UUID | None
    durchgangsordner: str | None
    zusammenfassung: Mapping[str, int] | None
    messen_voraussetzungen: tuple[Voraussetzung, ...]
    fehlerstrategie: str
    messdaten_wurzel: str | None
    paket_version: str
    git_hash: str | None
    git_dirty: bool | None
    interner_fehler: str | None
    zuruecksetzen_moeglich: bool
    """``True``, wenn :meth:`Sitzung.zuruecksetzen` jetzt sinnvoll und erlaubt ist."""

    @property
    def verbunden(self) -> bool:
        """Gibt an, ob eine Verbindung zum Gerät besteht."""
        return self.verbindung is not None


@dataclass(frozen=True, kw_only=True)
class SitzungsEreignis:
    """Ereignis für die Oberfläche; ``bild`` ist das Zustandsbild direkt danach."""

    revision: int
    art: str
    text: str
    daten: Mapping[str, object] = field(default_factory=dict)
    bild: Zustandsbild | None = None


class Sitzung:
    """Fassade über Warteschlange, Steuerung und Gerät.

    Parameters
    ----------
    geraete_fabrik : callable
        Erzeugt das Gerät zu einer Betriebsart.
    betriebsart : Betriebsart
        Anfangsbetriebsart (``MESSEN`` ist als Anfang nicht erlaubt).
    uhr : Uhr or None
        Zeitquelle (Standard: Echtzeituhr).
    build_info : BuildInfo or None
        Versionsangaben (Standard: :func:`ermittle_build_info`).
    messdaten_wurzel : pathlib.Path or None
        Wurzelordner der Messdaten.
    fehlerstrategie : Fehlerstrategie or None
        Fehlerverhalten (Standard: vorläufige Strategie der Steuerung).
    konfiguration : AblaufKonfiguration or None
        Einstellungen der Steuerung.
    aufruf_warnung_s : float
        Ab dieser Dauer eines hängenden Geräteaufrufs meldet der Wächter (Annahme, am
        Gerät einzustellen).
    warteschlange : Warteschlange or None
        Anfangswarteschlange.

    Raises
    ------
    ValueError
        Wenn ``betriebsart`` ``MESSEN`` ist (Freischaltung nur über
        :meth:`setze_betriebsart`).
    """

    def __init__(
        self,
        *,
        geraete_fabrik: GeraeteFabrik,
        betriebsart: Betriebsart = Betriebsart.SIMULATOR,
        uhr: Uhr | None = None,
        build_info: BuildInfo | None = None,
        messdaten_wurzel: Path | None = None,
        fehlerstrategie: Fehlerstrategie | None = None,
        konfiguration: AblaufKonfiguration | None = None,
        aufruf_warnung_s: float = 5.0,
        warteschlange: Warteschlange | None = None,
    ) -> None:
        if betriebsart is Betriebsart.MESSEN:
            raise ValueError("Sitzung: MESSEN nur über setze_betriebsart nach Freischaltung")
        self._fabrik = geraete_fabrik
        self._uhr: Uhr = uhr or Echtzeituhr()
        self._build = build_info or ermittle_build_info()
        self._wurzel = messdaten_wurzel
        self._warnung_s = aufruf_warnung_s
        self._sperre = threading.RLock()
        self._revision = 0
        self._ereignisse: queue.Queue[SitzungsEreignis] = queue.Queue()
        self._waechter_gemeldet = False
        self._waechter_fehler: str | None = None
        self._waechter_ende = threading.Event()
        self._waechter_thread: threading.Thread | None = None
        self.steuerung = Steuerung(
            warteschlange=warteschlange or Warteschlange(),
            geraet=None,
            betriebsart=betriebsart.value,
            uhr=self._uhr,
            build_info=self._build,
            fehlerstrategie=fehlerstrategie,
            konfiguration=konfiguration,
            bei_ereignis=self._bei_ablauf,
        )
        self._tausche(betriebsart)

    # --- Zustandsbild und Ereignisse ---------------------------------------------------

    @property
    def warteschlange(self) -> Warteschlange:
        """Die aktuelle Warteschlange."""
        return self.steuerung.warteschlange

    @property
    def betriebsart(self) -> Betriebsart:
        """Betriebsart des aktuellen Geräts."""
        return Betriebsart(self.steuerung.betriebsart)

    def _waechter_s(self) -> float | None:
        geraet = self.steuerung.geraet_oder_none  # ein Lesezugriff: Tausch im Geräte-Thread
        if geraet is None:
            return None
        dauer = geraet.haengender_aufruf_seit_s()
        if dauer is None or dauer < self._warnung_s:
            return None
        return dauer

    def _waechter_s_fuer_bild(self) -> float | None:
        """Wächterwert für das Zustandsbild; ein Fehler des Geräts darf das Bild nicht verhindern.

        Der Fehler selbst wird vom Wächter-Takt gemeldet (``waechter_fehler``).
        """
        try:
            return self._waechter_s()
        except Exception:  # bewusst: Anzeige ohne Wächterwert statt ohne Zustandsbild
            return None

    def _baue_bild(self) -> Zustandsbild:
        stand = self.steuerung.momentaufnahme()
        eintraege: list[EintragBild] = []
        zaehler: dict[str, int] = {}
        for e in self.warteschlange.eintraege():
            info = stand.laufinfo.get(e.id)
            if isinstance(e, Messung):
                zaehler[e.zustand.value] = zaehler.get(e.zustand.value, 0) + 1
                if info is not None and info.uebersprungen:
                    zaehler["uebersprungen"] = zaehler.get("uebersprungen", 0) + 1
                set_fehlt = e.zustand is MessungZustand.WARTEND and not os.path.isfile(
                    e.einstellungsdatei
                )
                eintraege.append(
                    EintragBild(
                        art="messung",
                        id=e.id,
                        name=e.name,
                        text="",
                        einstellungsdatei=e.einstellungsdatei,
                        parameter=dict(e.parameter),
                        zeitlimit_s=e.zeitlimit_s,
                        notiz=e.notiz,
                        zustand=e.zustand.value,
                        versuch=e.versuch,
                        nummer=info.nummer if info else None,
                        fehlerart=info.fehlerart if info else None,
                        fehlertext=info.fehlertext if info else None,
                        zeit_start=info.zeit_start if info else None,
                        zeit_ende=info.zeit_ende if info else None,
                        messdatei=info.messdatei if info else None,
                        protokolldatei=info.protokolldatei if info else None,
                        uebersprungen=bool(info and info.uebersprungen),
                        trockenlauf=bool(info and info.trockenlauf),
                        set_fehlt=set_fehlt,
                    )
                )
            else:
                eintraege.append(
                    EintragBild(
                        art="pausenpunkt",
                        id=e.id,
                        name="",
                        text=e.text,
                        einstellungsdatei=None,
                        parameter={},
                        zeitlimit_s=None,
                        notiz="",
                        zustand=e.zustand.value,
                        versuch=None,
                        nummer=None,
                        fehlerart=None,
                        fehlertext=None,
                        zeit_start=None,
                        zeit_ende=None,
                        messdatei=None,
                        protokolldatei=None,
                        uebersprungen=False,
                        trockenlauf=False,
                        set_fehlt=False,
                    )
                )
        beendet = stand.durchgang is DurchgangZustand.BEENDET
        return Zustandsbild(
            revision=self._revision,
            durchgang=stand.durchgang,
            ergebnis=stand.ergebnis,
            betriebsart=Betriebsart(stand.betriebsart),
            verbindung=stand.verbindung,
            eintraege=tuple(eintraege),
            fortschritt=stand.fortschritt,
            waechter_s=self._waechter_s_fuer_bild(),
            fehlerentscheidung_offen=stand.durchgang is DurchgangZustand.WARTET_AUF_ENTSCHEIDUNG,
            fehlertext=stand.fehler_offen,
            fehler_eintrag_id=stand.fehler_eintrag_id,
            pausenpunkt_id=stand.pausenpunkt_id,
            durchgangsordner=str(stand.durchgangsordner) if stand.durchgangsordner else None,
            zusammenfassung=zaehler if beendet else None,
            messen_voraussetzungen=self._voraussetzungen(
                stand.verbindung, self._trockenlauf_gueltig(stand)
            ),
            fehlerstrategie=stand.fehlerstrategie,
            messdaten_wurzel=str(self._wurzel) if self._wurzel else None,
            paket_version=self._build.paket_version,
            git_hash=self._build.git_hash,
            git_dirty=self._build.git_dirty,
            interner_fehler=stand.interner_fehler,
            zuruecksetzen_moeglich=(
                stand.durchgang in (DurchgangZustand.BEREIT, DurchgangZustand.BEENDET)
                and any(not e.bearbeitbar for e in self.warteschlange.eintraege())
            ),
        )

    def zustandsbild(self) -> Zustandsbild:
        """Aktuelles Zustandsbild (aus jedem Thread)."""
        with self._sperre:
            return self._baue_bild()

    def _neues_ereignis(self, art: str, text: str, daten: Mapping[str, object]) -> None:
        with self._sperre:
            self._revision += 1
            bild = self._baue_bild()
            self._ereignisse.put(
                SitzungsEreignis(
                    revision=self._revision, art=art, text=text, daten=dict(daten), bild=bild
                )
            )

    def _bei_ablauf(self, ereignis: AblaufEreignis) -> None:
        self._neues_ereignis(ereignis.art, ereignis.text, ereignis.daten)

    def hole_ereignisse(self) -> list[SitzungsEreignis]:
        """Alle seit dem letzten Abholen eingetroffenen Ereignisse, in Reihenfolge."""
        ergebnis: list[SitzungsEreignis] = []
        while True:
            try:
                ergebnis.append(self._ereignisse.get_nowait())
            except queue.Empty:
                return ergebnis

    # --- Wächter (Plan P2, 2.5) --------------------------------------------------------

    def pruefe_waechter(self) -> float | None:
        """Prüft auf einen hängenden Geräteaufruf; meldet ihn einmal je Hänger.

        Returns
        -------
        float or None
            Dauer des Hängers in s, wenn sie ``aufruf_warnung_s`` erreicht, sonst ``None``.
        """
        dauer = self._waechter_s()
        with self._sperre:
            if dauer is None:
                self._waechter_gemeldet = False
                return None
            melden = not self._waechter_gemeldet
            self._waechter_gemeldet = True
        if melden:
            self._neues_ereignis(
                "waechter", f"PSV reagiert nicht seit {dauer:.0f} s", {"dauer_s": dauer}
            )
        return dauer

    def _waechter_takt(self) -> None:
        """Ein Takt des Wächter-Threads; Fehler werden gemeldet, der Thread läuft weiter.

        Ein anhaltender Fehler wird einmal gemeldet, bis ein Takt wieder gelingt.
        """
        try:
            self.pruefe_waechter()
        except Exception:  # Wächter darf nicht still sterben: melden und weiterlaufen
            text = traceback.format_exc()
            with self._sperre:
                if self._waechter_fehler is not None:
                    return
                self._waechter_fehler = text
            # Ist der Meldeweg selbst defekt, bleibt der Text in _waechter_fehler erhalten.
            with contextlib.suppress(Exception):
                self._neues_ereignis(
                    "waechter_fehler",
                    "Fehler im Wächter; Wächter läuft weiter",
                    {"traceback": text},
                )
        else:
            with self._sperre:
                self._waechter_fehler = None

    # --- Threads -----------------------------------------------------------------------

    def starte_threads(self, waechter_takt_s: float = 0.5) -> None:
        """Startet Geräte-Thread und Wächter-Thread."""
        self.steuerung.starte_thread()
        self._waechter_ende.clear()

        def schleife() -> None:
            while not self._waechter_ende.wait(waechter_takt_s):
                self._waechter_takt()

        self._waechter_thread = threading.Thread(target=schleife, name="ldv-waechter", daemon=True)
        self._waechter_thread.start()

    def beende_threads(self, timeout_s: float = 5.0) -> bool:
        """Beendet beide Threads; ``True``, wenn beide rechtzeitig endeten."""
        self._waechter_ende.set()
        ok = self.steuerung.beende_thread(timeout_s)
        thread = self._waechter_thread
        if thread is not None:
            thread.join(timeout_s)
            ok = ok and not thread.is_alive()
        return ok

    def verarbeite(self, max_schritte: int = 100_000) -> None:
        """Arbeitet synchron bis zur Ruhe (ohne Geräte-Thread; Tests und Selbsttest)."""
        self.steuerung.bis_ruhe(max_schritte)

    # --- Warteschlange (R-012 bis R-016, R-021) ----------------------------------------

    def einfuegen(self, position: int, eintrag: Eintrag) -> None:
        """Fügt einen wartenden Eintrag ein (``IndexError``/``ValueError`` mit Grund)."""
        self.warteschlange.einfuegen(position, eintrag)
        self._pruefe_trockenlauf_bindung()
        self._neues_ereignis("warteschlange", "Eintrag eingefügt", {"eintrag_id": str(eintrag.id)})

    def bearbeiten(self, eintrag_id: UUID, **aenderungen: object) -> Eintrag:
        """Ändert einen wartenden Eintrag (``KeyError``/``ValueError`` mit Grund)."""
        neu = self.warteschlange.bearbeiten(eintrag_id, **aenderungen)
        self._pruefe_trockenlauf_bindung()
        self._neues_ereignis("warteschlange", "Eintrag geändert", {"eintrag_id": str(eintrag_id)})
        return neu

    def entfernen(self, eintrag_id: UUID) -> Eintrag:
        """Entfernt einen wartenden Eintrag."""
        alt = self.warteschlange.entfernen(eintrag_id)
        self._pruefe_trockenlauf_bindung()
        self._neues_ereignis("warteschlange", "Eintrag entfernt", {"eintrag_id": str(eintrag_id)})
        return alt

    def verschieben(self, eintrag_id: UUID, neue_position: int) -> None:
        """Verschiebt einen wartenden Eintrag."""
        self.warteschlange.verschieben(eintrag_id, neue_position)
        self._pruefe_trockenlauf_bindung()
        self._neues_ereignis("warteschlange", "Eintrag verschoben", {"eintrag_id": str(eintrag_id)})

    def speichere_warteschlange(self, pfad: Path, *, ueberschreiben: bool = False) -> None:
        """Speichert die Definitionen (R-021); ``FileExistsError`` ohne ``ueberschreiben``."""
        speichere_warteschlange(
            self.warteschlange.eintraege(),
            pfad,
            paket_version=self._build.paket_version,
            git_hash=self._build.git_hash,
            ueberschreiben=ueberschreiben,
            jetzt=self._uhr.jetzt,
        )
        self._neues_ereignis("warteschlange_gespeichert", f"Gespeichert: {pfad}", {})

    def lade_warteschlange(self, pfad: Path) -> tuple[str, ...]:
        """Lädt eine Warteschlange und ersetzt die aktuelle (nur ohne laufenden Durchgang).

        Returns
        -------
        tuple of str
            Warnungen des Ladens (z. B. fehlende Einstellungsdatei).

        Raises
        ------
        ValueError
            Bei ungültiger Datei oder laufendem Durchgang.
        """
        self._pruefe_ruhe("Warteschlange laden")
        ergebnis = lade_warteschlange(pfad)
        self.steuerung.setze_warteschlange(Warteschlange(ergebnis.eintraege))
        self.steuerung.verwerfe_trockenlauf()  # andere Warteschlange: Freischaltung erlischt
        self._neues_ereignis(
            "warteschlange_geladen", f"Geladen: {pfad}", {"warnungen": list(ergebnis.warnungen)}
        )
        return ergebnis.warnungen

    # --- Einstellungen und Betriebsart -------------------------------------------------

    def setze_messdaten_wurzel(self, pfad: Path) -> None:
        """Setzt den Wurzelordner der Messdaten (nur ohne laufenden Durchgang)."""
        self._pruefe_ruhe("Messdaten-Wurzel setzen")
        with self._sperre:
            self._wurzel = pfad
        self._neues_ereignis("einstellung", f"Messdaten-Wurzel: {pfad}", {"pfad": str(pfad)})

    def _voraussetzungen(
        self, verbindung: GeraeteInfo | None, trockenlauf_ok: bool
    ) -> tuple[Voraussetzung, ...]:
        wurzel = self._wurzel
        wurzel_ok = wurzel is not None and wurzel.is_dir() and os.access(wurzel, os.W_OK | os.X_OK)
        build = self._build
        return (
            Voraussetzung(
                name="verbindung",
                erfuellt=verbindung is not None,
                text="Verbindung zu PSV steht" if verbindung else "Keine Verbindung zu PSV",
            ),
            Voraussetzung(
                name="geraet_gestoppt",
                erfuellt=verbindung is not None and verbindung.zustand is GeraeteZustand.GESTOPPT,
                text="PSV beim Verbinden im Zustand gestoppt",
            ),
            Voraussetzung(
                name="meldungen_unterdrueckt",
                erfuellt=verbindung is not None and verbindung.meldungen_unterdrueckt,
                text="SuppressMessagesForAutomation ist aktiv (in PSV aktivieren)",
            ),
            Voraussetzung(
                name="git_hash",
                erfuellt=build.git_hash is not None,
                text=(
                    f"Git-Hash {build.git_hash[:12]}"
                    + (" (mit Änderungen)" if build.git_dirty else "")
                    if build.git_hash
                    else f"Git-Hash unbekannt: {build.grund}"
                ),
            ),
            Voraussetzung(
                name="messdaten_wurzel",
                erfuellt=wurzel_ok,
                text=f"Messdaten-Wurzel beschreibbar: {wurzel}"
                if wurzel_ok
                else f"Messdaten-Wurzel fehlt oder ist nicht beschreibbar: {wurzel}",
            ),
            Voraussetzung(
                name="trockenlauf",
                erfuellt=trockenlauf_ok,
                text="Trockenlauf des ersten Eintrags in dieser Sitzung ohne Abweichung",
            ),
        )

    def messen_voraussetzungen(self) -> tuple[Voraussetzung, ...]:
        """Voraussetzungen für ``MESSEN``, jede einzeln mit Text."""
        stand = self.steuerung.momentaufnahme()
        return self._voraussetzungen(stand.verbindung, self._trockenlauf_gueltig(stand))

    # --- Trockenlauf-Bindung (Plan 6, Nutzerentscheidung zu MINOR-2) ---------------------

    @staticmethod
    def _definition(m: Messung) -> tuple[object, ...]:
        return (
            m.id,
            m.name,
            m.einstellungsdatei,
            tuple(sorted(m.parameter.items())),
            m.zeitlimit_s,
            m.notiz,
        )

    def _erste_messung(self) -> Messung | None:
        return next((e for e in self.warteschlange.eintraege() if isinstance(e, Messung)), None)

    def _trockenlauf_gueltig(self, stand: AblaufStand) -> bool:
        """Freischaltung gilt nur für die unveränderte erste Messung der Warteschlange."""
        gemerkt = stand.trockenlauf_messung
        erste = self._erste_messung()
        return (
            gemerkt is not None
            and erste is not None
            and self._definition(gemerkt) == self._definition(erste)
        )

    def _pruefe_trockenlauf_bindung(self) -> None:
        """Entzieht die Freischaltung dauerhaft, sobald die erste Messung abweicht."""
        stand = self.steuerung.momentaufnahme()
        if stand.trockenlauf_messung is not None and not self._trockenlauf_gueltig(stand):
            self.steuerung.verwerfe_trockenlauf()
            self._neues_ereignis(
                "trockenlauf_verworfen",
                "Trockenlauf-Freischaltung erloschen: erste Messung geändert",
                {},
            )

    def zuruecksetzen(self) -> None:
        """Baut die Warteschlange aus denselben Definitionen wieder auf ``WARTEND`` auf.

        Nur in ``BEREIT``/``BEENDET``. IDs, Reihenfolge und Definitionen bleiben gleich,
        Versuchszähler beginnen wieder bei 1, Laufdaten der Anzeige werden geleert.
        Messprotokolle und Messdateien bleiben unberührt. Eine Trockenlauf-Freischaltung
        bleibt erhalten, weil die Definitionen unverändert sind.

        Raises
        ------
        ValueError
            Bei laufendem Durchgang oder ausstehenden Befehlen.
        """
        self._pruefe_ruhe("Zurücksetzen")
        neu: list[Eintrag] = []
        for e in self.warteschlange.eintraege():
            if isinstance(e, Messung):
                neu.append(
                    Messung(
                        name=e.name,
                        einstellungsdatei=e.einstellungsdatei,
                        parameter=dict(e.parameter),
                        zeitlimit_s=e.zeitlimit_s,
                        notiz=e.notiz,
                        id=e.id,
                    )
                )
            else:
                neu.append(Pausenpunkt(text=e.text, id=e.id))
        self.steuerung.setze_warteschlange(Warteschlange(neu))
        self._neues_ereignis("warteschlange_zurueckgesetzt", "Warteschlange zurückgesetzt", {})

    def _pruefe_ruhe(self, taetigkeit: str) -> None:
        z = self.steuerung.zustand
        if z not in (DurchgangZustand.BEREIT, DurchgangZustand.BEENDET):
            raise ValueError(f"{taetigkeit} ist im Zustand {z.value} nicht möglich")

    def _tausche(self, betriebsart: Betriebsart) -> None:
        fabrik = self._fabrik
        self.steuerung.tausche_geraet(lambda: fabrik(betriebsart), betriebsart.value)

    def setze_betriebsart(self, neu: Betriebsart) -> None:
        """Wechselt die Betriebsart; das Gerät wird getrennt und neu erzeugt.

        Raises
        ------
        ValueError
            Bei laufendem Durchgang oder, für ``MESSEN``, bei nicht erfüllten
            Voraussetzungen (Meldung nennt jede fehlende einzeln).
        """
        if self.steuerung.zustand is not DurchgangZustand.GERAET_UNKLAR:
            self._pruefe_ruhe("Betriebsart wechseln")
        if neu is Betriebsart.MESSEN:
            fehlend = [v.text for v in self.messen_voraussetzungen() if not v.erfuellt]
            if fehlend:
                raise ValueError("MESSEN nicht freigeschaltet: " + "; ".join(fehlend))
        self._tausche(neu)

    # --- Befehle -----------------------------------------------------------------------

    def verbinde(self) -> None:
        """Verbindet mit dem Gerät; ein nach ``GERAET_UNKLAR`` verlorenes wird neu erzeugt."""
        self._pruefe_ruhe("Verbinden")
        if self.steuerung.momentaufnahme().geraet_verloren:
            # Nach GERAET_UNKLAR gilt das Gerät als verloren: neu erzeugen (Vertrag).
            self._tausche(self.betriebsart)
        self.steuerung.verbinde()

    def trenne(self) -> None:
        """Trennt die Verbindung (auch in ``GERAET_UNKLAR``)."""
        if self.steuerung.zustand is not DurchgangZustand.GERAET_UNKLAR:
            self._pruefe_ruhe("Trennen")
        self.steuerung.trenne()

    def starte(self, name: str, *, messen_bestaetigt: bool = False) -> None:
        """Startet einen Durchgang.

        Parameters
        ----------
        name : str
            Durchgangsname.
        messen_bestaetigt : bool
            In ``MESSEN`` Pflicht: ausdrückliche Bestätigung des Durchgangs (Dialog).

        Raises
        ------
        ValueError
            Wenn der Durchgang nicht ``BEREIT`` ist, keine Verbindung besteht, keine
            Messdaten-Wurzel gesetzt ist, die Betriebsart ``NUR_LESEN`` ist oder in
            ``MESSEN`` die Bestätigung bzw. eine Voraussetzung fehlt.
        """
        stand = self.steuerung.momentaufnahme()
        if stand.durchgang is not DurchgangZustand.BEREIT:
            raise ValueError(f"Start nur im Zustand bereit (aktuell {stand.durchgang.value})")
        if stand.verbindung is None:
            raise ValueError("Start nicht möglich: keine Verbindung zum Gerät")
        if self._wurzel is None:
            raise ValueError("Start nicht möglich: keine Messdaten-Wurzel gesetzt")
        art = self.betriebsart
        if art is Betriebsart.NUR_LESEN:
            raise ValueError("In der Betriebsart NUR_LESEN ist kein Durchgang möglich")
        if art is Betriebsart.MESSEN:
            if not messen_bestaetigt:
                raise ValueError("MESSEN: Durchgang muss ausdrücklich bestätigt werden")
            fehlend = [v.text for v in self.messen_voraussetzungen() if not v.erfuellt]
            if fehlend:
                raise ValueError("MESSEN nicht freigeschaltet: " + "; ".join(fehlend))
        self.steuerung.starte(
            DurchgangsAuftrag(
                name=name,
                messdaten_wurzel=self._wurzel,
                betriebsart=art.value,
                trockenlauf=art is Betriebsart.TROCKENLAUF,
                messfreigabe=art in (Betriebsart.SIMULATOR, Betriebsart.MESSEN),
            )
        )

    def _erwarte(self, befehl: str, *zustaende: DurchgangZustand) -> None:
        z = self.steuerung.zustand
        if z not in zustaende:
            raise ValueError(f"'{befehl}' ist im Zustand {z.value} nicht möglich")

    def pausiere(self) -> None:
        """Pause nach der laufenden Messung (R-018)."""
        self._erwarte("Pause", DurchgangZustand.LAEUFT)
        self.steuerung.pausiere()

    def setze_fort(self) -> None:
        """Setzt einen pausierten Durchgang fort."""
        self._erwarte("Fortsetzen", DurchgangZustand.PAUSIERT)
        self.steuerung.setze_fort()

    def brich_ab(self) -> None:
        """Bricht den Durchgang ab (laufende eigene Messung wird gestoppt)."""
        self._erwarte(
            "Abbrechen",
            DurchgangZustand.LAEUFT,
            DurchgangZustand.PAUSE_ANGEFORDERT,
            DurchgangZustand.PAUSIERT,
            DurchgangZustand.WARTET_AUF_BESTAETIGUNG,
            DurchgangZustand.WARTET_AUF_ENTSCHEIDUNG,
        )
        self.steuerung.brich_ab()

    def bestaetige(self) -> None:
        """Bestätigt den erreichten Pausenpunkt (R-017)."""
        self._erwarte("Bestätigen", DurchgangZustand.WARTET_AUF_BESTAETIGUNG)
        self.steuerung.bestaetige()

    def entscheide(self, entscheidung: Fehlerentscheidung) -> None:
        """Fehlerentscheidung: Wiederholen, Überspringen oder Abbrechen (vorläufig)."""
        self._erwarte("Fehlerentscheidung", DurchgangZustand.WARTET_AUF_ENTSCHEIDUNG)
        self.steuerung.entscheide(entscheidung)

    def quittiere(self) -> None:
        """Quittiert einen beendeten Durchgang (``BEENDET -> BEREIT``)."""
        self._erwarte("Quittieren", DurchgangZustand.BEENDET)
        self.steuerung.quittiere()
