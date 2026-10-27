"""Einstieg ``python -m ldv_automation`` (Plan P2, Abschnitt 1).

Aufruf::

    python -m ldv_automation gui [--simulator | --psv] [--betriebsart ART] [--start-psv]
                                 [--messdaten ORDNER] [--konfig DATEI]
    python -m ldv_automation selbsttest [--ordner ORDNER] [--konfig DATEI]

``--konfig`` nennt die JSON-Konfigurationsdatei des Messrechners (:mod:`.konfig`, K-U5). Eine
ungültige Datei bricht den Start mit Meldung und Rückgabewert 2 ab; ohne Datei gelten die
Standardwerte.

``__main__`` ist die Stelle, an der das Gerät zusammengesetzt wird (Simulator bzw.
COM-Adapter); deshalb darf nur dieses Modul neben ``sitzung`` und ``gui`` auch
``geraet.simulator`` und ``geraet.com`` importieren (Importtest). Hier steht auch die
einzige Abbildung der Sitzungs-Betriebsart auf die Betriebsart des Geräts
(:data:`SIMULATOR_BETRIEBSART`, :data:`COM_BETRIEBSART`; Entscheidung B9: kein gemeinsamer
Aufzählungstyp in ``geraet/schnittstelle.py``).

``selbsttest`` (Paket U5, Plan 9 T0) führt ohne Oberfläche und ohne pywin32 zwei Durchgänge
gegen den Simulator aus (Simulator und Trockenlauf, mit Pausenpunkt) und prüft Dateien,
Protokolle und Zustandsbild. Er arbeitet mit simulierter Zeit (kein Warten).
"""

from __future__ import annotations

import argparse
import json
import sys
import tempfile
import time
import traceback
from collections.abc import Callable, Mapping, Sequence
from datetime import datetime
from pathlib import Path

from ldv_automation.ablauf.uhr import Testuhr
from ldv_automation.domaene.eintraege import Messung, Pausenpunkt
from ldv_automation.geraet.com.adapter import ComBetriebsart
from ldv_automation.geraet.schnittstelle import Messgeraet
from ldv_automation.geraet.simulator import SIMULATOR_KENNUNG, Simulator
from ldv_automation.konfig import STANDARD, KonfigFehler, MessrechnerKonfig, lade_konfig
from ldv_automation.protokoll.ablage import (
    ENDUNG_MESSDATEI,
    ENDUNG_PROTOKOLL,
    EREIGNISPROTOKOLL,
    WARTESCHLANGENKOPIE,
)
from ldv_automation.protokoll.messprotokoll import PFLICHTFELDER
from ldv_automation.sitzung import (
    Betriebsart,
    DurchgangErgebnis,
    DurchgangZustand,
    GeraeteFabrik,
    Sitzung,
)

START_BESTAETIGUNG = "JA"
"""Text, der für ``--start-psv`` eingetippt werden muss (Plan P2, V0)."""

BETRIEBSARTEN_START = (Betriebsart.SIMULATOR, Betriebsart.NUR_LESEN, Betriebsart.TROCKENLAUF)
"""Zulässige Anfangsbetriebsarten; ``MESSEN`` nur über die Freischaltung in der Oberfläche."""

SIMULATOR_BETRIEBSART: Mapping[Betriebsart, str] = {
    Betriebsart.SIMULATOR: "simulator",
    Betriebsart.NUR_LESEN: "nur_lesen",
    Betriebsart.TROCKENLAUF: "trockenlauf",
    Betriebsart.MESSEN: "messen",
}
"""Sitzungs-Betriebsart -> Betriebsart-Text des Simulators (``simulator.BETRIEBSARTEN``)."""

COM_BETRIEBSART: Mapping[Betriebsart, ComBetriebsart | None] = {
    Betriebsart.SIMULATOR: None,
    Betriebsart.NUR_LESEN: ComBetriebsart.NUR_LESEN,
    Betriebsart.TROCKENLAUF: ComBetriebsart.TROCKENLAUF,
    Betriebsart.MESSEN: ComBetriebsart.MESSEN,
}
"""Sitzungs-Betriebsart -> Betriebsart des COM-Adapters; ``None``: immer Simulator."""


KONFIG_HILFE = "Konfigurationsdatei des Messrechners (JSON, siehe konfig/beispiel_messrechner.json)"


def baue_parser() -> argparse.ArgumentParser:
    """Kommandozeile des Einstiegs."""
    parser = argparse.ArgumentParser(
        prog="python -m ldv_automation",
        description="Mess-Warteschlange für das 3D-Laser-Doppler-Vibrometer (Prototyp).",
    )
    unter = parser.add_subparsers(dest="befehl", required=True)
    gui = unter.add_parser("gui", help="Oberfläche starten")
    quelle = gui.add_mutually_exclusive_group()
    quelle.add_argument(
        "--simulator",
        action="store_true",
        help="alle Betriebsarten gegen den Simulator (Standard)",
    )
    quelle.add_argument(
        "--psv", action="store_true", help="NUR LESEN, TROCKENLAUF und MESSEN über COM an der PSV"
    )
    gui.add_argument(
        "--betriebsart",
        choices=[a.value for a in BETRIEBSARTEN_START],
        default=Betriebsart.SIMULATOR.value,
        help="Anfangsbetriebsart (MESSEN nur über die Freischaltung in der Oberfläche)",
    )
    gui.add_argument(
        "--start-psv",
        action="store_true",
        help=(
            f"PSV darf über COM gestartet werden (nur mit --psv, Bestätigung {START_BESTAETIGUNG})"
        ),
    )
    gui.add_argument("--messdaten", metavar="ORDNER", help="Messdaten-Ordner (Wurzel)")
    gui.add_argument("--konfig", metavar="DATEI", help=KONFIG_HILFE)
    test = unter.add_parser(
        "selbsttest", help="Simulator- und Trockenlauf-Durchgang ohne Oberfläche (Simulator)"
    )
    test.add_argument(
        "--ordner",
        metavar="ORDNER",
        help="vorhandener Messdaten-Ordner für die Ergebnisse (Standard: temporär, wird gelöscht)",
    )
    test.add_argument("--konfig", metavar="DATEI", help=KONFIG_HILFE)
    return parser


def erzeuge_fabrik(
    *,
    psv: bool,
    start_psv_erlaubt: bool,
    messdaten_wurzel: Callable[[], Path | None],
    konfig: MessrechnerKonfig = STANDARD,
) -> GeraeteFabrik:
    """Gerätefabrik: Simulator oder COM-Adapter je Betriebsart.

    Parameters
    ----------
    psv : bool
        ``False``: jede Betriebsart läuft gegen den Simulator. ``True``: ``SIMULATOR`` gegen
        den Simulator, alle anderen über COM (``PsvComGeraet``, nur unter Windows).
    start_psv_erlaubt : bool
        ``--start-psv`` mit getipptem ``JA``.
    messdaten_wurzel : callable
        Liefert den aktuellen Messdaten-Ordner beim Erzeugen des Geräts (Pflicht für den
        COM-Adapter in TROCKENLAUF und MESSEN; Prüfung im Adapter).
    konfig : MessrechnerKonfig
        Lademaske und Rückfallschalter S4 für den COM-Adapter.
    """

    def fabrik(art: Betriebsart) -> Messgeraet:
        com_art = COM_BETRIEBSART[art]
        if not psv or com_art is None:
            return Simulator(time.monotonic, betriebsart=SIMULATOR_BETRIEBSART[art])
        from ldv_automation.geraet.com.adapter import ComKonfiguration, PsvComGeraet
        from ldv_automation.geraet.com.pywin32_bindung import Pywin32Bindung

        wurzel = messdaten_wurzel()
        return PsvComGeraet(
            Pywin32Bindung(),
            ComKonfiguration(
                betriebsart=com_art,
                messdaten_wurzel=str(wurzel) if wurzel is not None else None,
                start_psv_erlaubt=start_psv_erlaubt,
                lademaske=konfig.lademaske,
                validator_rueckfall_direkt=konfig.validator_rueckfall_direkt,
            ),
        )

    return fabrik


def erzeuge_sitzung(
    args: argparse.Namespace,
    eingabe: Callable[[str], str] = input,
    konfig: MessrechnerKonfig = STANDARD,
) -> Sitzung:
    """Baut die Sitzung aus den Argumenten des Unterbefehls ``gui`` und der Konfiguration.

    Raises
    ------
    SystemExit
        Bei ``--start-psv`` ohne ``--psv``.
    """
    if args.start_psv and not args.psv:
        raise SystemExit("--start-psv ist nur zusammen mit --psv zulässig.")
    start_psv = False
    if args.start_psv:
        antwort = eingabe(
            f"PSV darf bei Bedarf über COM gestartet werden. Zur Bestätigung "
            f"{START_BESTAETIGUNG} eintippen: "
        )
        start_psv = antwort.strip() == START_BESTAETIGUNG
        if not start_psv:
            print("Nicht bestätigt: PSV wird nicht gestartet.")
    wurzel = Path(args.messdaten) if args.messdaten else None
    halter: list[Sitzung] = []

    def aktuelle_wurzel() -> Path | None:
        if not halter:
            return wurzel
        text = halter[0].zustandsbild().messdaten_wurzel
        return Path(text) if text else None

    sitzung = Sitzung(
        geraete_fabrik=erzeuge_fabrik(
            psv=args.psv,
            start_psv_erlaubt=start_psv,
            messdaten_wurzel=aktuelle_wurzel,
            konfig=konfig,
        ),
        betriebsart=Betriebsart(args.betriebsart),
        messdaten_wurzel=wurzel,
        konfiguration=konfig.ablauf_konfiguration(),
        aufruf_warnung_s=konfig.aufruf_warnung_s,
        konfiguration_info=konfig.protokoll_info(),
    )
    halter.append(sitzung)
    return sitzung


def main(argv: Sequence[str] | None = None, eingabe: Callable[[str], str] = input) -> int:
    """Einstieg; gibt den Rückgabewert des Prozesses zurück."""
    args = baue_parser().parse_args(argv)
    try:
        konfig = lade_konfig(Path(args.konfig)) if args.konfig else STANDARD
    except KonfigFehler as fehler:
        print(f"Abbruch: {fehler}", file=sys.stderr)
        return 2
    if args.befehl == "selbsttest":
        return selbsttest(Path(args.ordner) if args.ordner else None, konfig=konfig)
    sitzung = erzeuge_sitzung(args, eingabe, konfig)
    return _starte_gui(sitzung)


# --- Selbsttest (U5-1) ----------------------------------------------------------------------


class SelbsttestFehler(Exception):  # noqa: N818  (fachlicher Name)
    """Eine Prüfung des Selbsttests ist gescheitert."""


def _pruefe(bedingung: bool, text: str, ausgabe: Callable[[str], None]) -> None:
    if not bedingung:
        raise SelbsttestFehler(text)
    ausgabe(f"  ok    {text}")


def _lies_json(pfad: Path) -> dict[str, object]:
    daten = json.loads(pfad.read_text(encoding="utf-8"))
    if not isinstance(daten, dict):
        raise SelbsttestFehler(f"{pfad.name}: kein JSON-Objekt")
    return daten


def _durchgang(
    sitzung: Sitzung, ausgabe: Callable[[str], None]
) -> tuple[Path, list[dict[str, object]]]:
    """Startet einen Durchgang, bestätigt den Pausenpunkt, prüft Ende und Protokolle."""
    sitzung.starte(sitzung.zustandsbild().durchgangsname)
    sitzung.verarbeite()
    bild = sitzung.zustandsbild()
    _pruefe(
        bild.durchgang is DurchgangZustand.WARTET_AUF_BESTAETIGUNG,
        "Pausenpunkt hält den Durchgang an",
        ausgabe,
    )
    sitzung.bestaetige()
    sitzung.verarbeite()
    bild = sitzung.zustandsbild()
    _pruefe(
        bild.durchgang is DurchgangZustand.BEENDET
        and bild.ergebnis is DurchgangErgebnis.VOLLSTAENDIG,
        "Durchgang vollständig beendet",
        ausgabe,
    )
    _pruefe(
        dict(bild.zusammenfassung or {}) == {"fertig": 2},
        f"Zusammenfassung: 2 fertig ({dict(bild.zusammenfassung or {})})",
        ausgabe,
    )
    ordner = Path(bild.durchgangsordner or "")
    _pruefe(
        (ordner / EREIGNISPROTOKOLL).is_file() and (ordner / WARTESCHLANGENKOPIE).is_file(),
        f"Ereignisprotokoll und Warteschlangenkopie in {ordner}",
        ausgabe,
    )
    protokolle = [_lies_json(p) for p in sorted(ordner.glob("*" + ENDUNG_PROTOKOLL))]
    _pruefe(len(protokolle) == 2, "zwei Messprotokolle", ausgabe)
    fehlend = sorted({f for p in protokolle for f in PFLICHTFELDER if f not in p})
    _pruefe(not fehlend, f"alle Pflichtfelder der Messprotokolle vorhanden {fehlend}", ausgabe)
    erwartet = sitzung.zustandsbild().konfiguration
    _pruefe(
        all(p.get("konfiguration") == erwartet for p in protokolle),
        "Konfiguration (Pfad, SHA-256, Werte) in beiden Protokollen",
        ausgabe,
    )
    return ordner, protokolle


def _selbsttest_ablauf(
    wurzel: Path,
    vorlagen: Path,
    ausgabe: Callable[[str], None],
    konfig: MessrechnerKonfig = STANDARD,
) -> None:
    uhr = Testuhr(datetime.now().astimezone())
    sitzung = Sitzung(
        geraete_fabrik=lambda art: Simulator(uhr.monotonic, betriebsart=SIMULATOR_BETRIEBSART[art]),
        betriebsart=Betriebsart.SIMULATOR,
        uhr=uhr,
        messdaten_wurzel=wurzel,
        konfiguration=konfig.ablauf_konfiguration(),
        aufruf_warnung_s=konfig.aufruf_warnung_s,
        konfiguration_info=konfig.protokoll_info(),
    )
    bild = sitzung.zustandsbild()
    ausgabe(f"Paketversion {bild.paket_version}, Git-Hash {bild.git_hash or 'unbekannt'}")
    ausgabe(f"Konfiguration: {konfig.pfad or 'Standardwerte'}")
    _pruefe(
        bild.standard_zeitlimit_s == konfig.standard_zeitlimit_s,
        f"Standard-Zeitlimit aus der Konfiguration: {konfig.standard_zeitlimit_s:g} s",
        ausgabe,
    )
    _pruefe(
        not bild.messdaten_wurzel_probleme,
        f"Messdaten-Ordner geeignet: {wurzel} {list(bild.messdaten_wurzel_probleme)}",
        ausgabe,
    )
    set_datei = vorlagen / "selbsttest.set"
    set_datei.write_bytes(b"SELBSTTEST (Platzhalter, keine PSV-Einstellungsdatei)\n")
    sitzung.verbinde()
    sitzung.verarbeite()
    bild = sitzung.zustandsbild()
    _pruefe(bild.verbunden, "Simulator verbunden", ausgabe)
    stand = bild.geraete_stand
    _pruefe(
        stand is not None and stand.messpunkte == 9 and stand.generator.unbedenklich,
        "Gerätestand gelesen (9 Messpunkte, Generator aus)",
        ausgabe,
    )
    sitzung.einfuegen(
        0, Messung(name="Selbsttest 1", einstellungsdatei=str(set_datei), parameter={})
    )
    sitzung.einfuegen(1, Pausenpunkt(text="Selbsttest: Pausenpunkt"))
    sitzung.einfuegen(
        2,
        Messung(
            name="Selbsttest 2",
            einstellungsdatei=str(set_datei),
            parameter={"fft.bandbreite_hz": 3125.0, "fft.linien": 800},
        ),
    )
    ausgabe("Durchgang 1: SIMULATOR")
    ordner, protokolle = _durchgang(sitzung, ausgabe)
    messdateien = sorted(ordner.glob("*" + ENDUNG_MESSDATEI))
    _pruefe(
        len(messdateien) == 2
        and all(p.read_bytes().startswith(SIMULATOR_KENNUNG) for p in messdateien),
        "zwei Platzhalter-Messdateien mit Kennung SIMULATOR",
        ausgabe,
    )
    _pruefe(
        all(p.get("status") == "fertig" for p in protokolle),
        "Status in beiden Protokollen: fertig",
        ausgabe,
    )
    ausgabe("Durchgang 2: TROCKENLAUF (Simulator)")
    sitzung.setze_betriebsart(Betriebsart.TROCKENLAUF)
    sitzung.verarbeite()
    sitzung.zuruecksetzen()
    sitzung.verbinde()
    sitzung.verarbeite()
    _pruefe(
        sitzung.zustandsbild().betriebsart is Betriebsart.TROCKENLAUF,
        "Betriebsart TROCKENLAUF",
        ausgabe,
    )
    ordner, protokolle = _durchgang(sitzung, ausgabe)
    _pruefe(not list(ordner.glob("*" + ENDUNG_MESSDATEI)), "Trockenlauf: keine Messdatei", ausgabe)
    _pruefe(
        all(p.get("status") == "trockenlauf" for p in protokolle),
        "Status in beiden Protokollen: trockenlauf",
        ausgabe,
    )
    sitzung.zuruecksetzen()
    vorschau = sitzung.zustandsbild().start_vorschau
    _pruefe(
        len(vorschau) == 2
        and all(v.messpunkte == 9 and v.generator_unbedenklich for v in vorschau),
        "Startvorschau nach Trockenlauf: Messpunkte und Generator bekannt",
        ausgabe,
    )


def selbsttest(
    ordner: Path | None = None,
    ausgabe: Callable[[str], None] = print,
    konfig: MessrechnerKonfig = STANDARD,
) -> int:
    """Selbsttest ohne Oberfläche gegen den Simulator (U5-1).

    Parameters
    ----------
    ordner : pathlib.Path or None
        Vorhandener Messdaten-Ordner, in dem die Ergebnisse bleiben; ``None``: temporärer
        Ordner, der danach gelöscht wird.
    ausgabe : callable
        Ausgabe je Zeile (Standard: ``print``).
    konfig : MessrechnerKonfig
        Konfiguration (Zeiten der Steuerung; erscheint in den Protokollen).

    Returns
    -------
    int
        0 bei Erfolg, 1 bei einer gescheiterten Prüfung oder einem Fehler.
    """
    ausgabe("Selbsttest ldv_automation (Simulator, ohne Oberfläche)")
    try:
        with tempfile.TemporaryDirectory(prefix="ldv_selbsttest_") as temp:
            vorlagen = Path(temp) / "vorlagen"
            vorlagen.mkdir()
            wurzel = ordner if ordner is not None else Path(temp) / "messdaten"
            wurzel.mkdir(exist_ok=ordner is not None)
            _selbsttest_ablauf(wurzel.resolve(), vorlagen, ausgabe, konfig)
    except SelbsttestFehler as fehler:
        ausgabe(f"  FEHLER {fehler}")
        ausgabe("Selbsttest FEHLGESCHLAGEN")
        return 1
    except Exception:  # Selbsttest meldet jeden Fehler mit Ablauf statt abzustürzen
        ausgabe(traceback.format_exc())
        ausgabe("Selbsttest FEHLGESCHLAGEN (unerwarteter Fehler)")
        return 1
    ausgabe("Selbsttest bestanden")
    return 0


def _starte_gui(sitzung: Sitzung) -> int:  # pragma: no cover - öffnet ein Fenster
    from ldv_automation.gui.start import starte_gui

    return starte_gui(sitzung)


if __name__ == "__main__":  # pragma: no cover - Programmstart
    sys.exit(main())
