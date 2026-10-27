"""Einstieg ``python -m ldv_automation`` (Plan P2, Abschnitt 1).

Aufruf::

    python -m ldv_automation gui [--simulator | --psv] [--betriebsart ART] [--start-psv]
                                 [--messdaten ORDNER]

``__main__`` ist die Stelle, an der das Gerät zusammengesetzt wird (Simulator bzw.
COM-Adapter); deshalb darf nur dieses Modul neben ``sitzung`` und ``gui`` auch
``geraet.simulator`` und ``geraet.com`` importieren (Importtest). ``selbsttest`` folgt mit
Paket U5.
"""

from __future__ import annotations

import argparse
import sys
import time
from collections.abc import Callable, Sequence
from pathlib import Path

from ldv_automation.geraet.schnittstelle import Messgeraet
from ldv_automation.geraet.simulator import Simulator
from ldv_automation.sitzung import Betriebsart, GeraeteFabrik, Sitzung

START_BESTAETIGUNG = "JA"
"""Text, der für ``--start-psv`` eingetippt werden muss (Plan P2, V0)."""

BETRIEBSARTEN_START = (Betriebsart.SIMULATOR, Betriebsart.NUR_LESEN, Betriebsart.TROCKENLAUF)
"""Zulässige Anfangsbetriebsarten; ``MESSEN`` nur über die Freischaltung in der Oberfläche."""


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
    unter.add_parser("selbsttest", help="Simulator-Durchgang ohne Oberfläche (folgt mit U5)")
    return parser


def erzeuge_fabrik(
    *,
    psv: bool,
    start_psv_erlaubt: bool,
    messdaten_wurzel: Callable[[], Path | None],
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
    """

    def fabrik(art: Betriebsart) -> Messgeraet:
        if not psv or art is Betriebsart.SIMULATOR:
            return Simulator(time.monotonic, betriebsart=art.value)
        from ldv_automation.geraet.com.adapter import (
            ComBetriebsart,
            ComKonfiguration,
            PsvComGeraet,
        )
        from ldv_automation.geraet.com.pywin32_bindung import Pywin32Bindung

        wurzel = messdaten_wurzel()
        return PsvComGeraet(
            Pywin32Bindung(),
            ComKonfiguration(
                betriebsart=ComBetriebsart(art.value),
                messdaten_wurzel=str(wurzel) if wurzel is not None else None,
                start_psv_erlaubt=start_psv_erlaubt,
            ),
        )

    return fabrik


def erzeuge_sitzung(args: argparse.Namespace, eingabe: Callable[[str], str] = input) -> Sitzung:
    """Baut die Sitzung aus den Argumenten des Unterbefehls ``gui``.

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
            psv=args.psv, start_psv_erlaubt=start_psv, messdaten_wurzel=aktuelle_wurzel
        ),
        betriebsart=Betriebsart(args.betriebsart),
        messdaten_wurzel=wurzel,
    )
    halter.append(sitzung)
    return sitzung


def main(argv: Sequence[str] | None = None, eingabe: Callable[[str], str] = input) -> int:
    """Einstieg; gibt den Rückgabewert des Prozesses zurück."""
    args = baue_parser().parse_args(argv)
    if args.befehl == "selbsttest":
        print("Der Selbsttest ist noch nicht umgesetzt (folgt mit Paket U5).", file=sys.stderr)
        return 2
    sitzung = erzeuge_sitzung(args, eingabe)
    return _starte_gui(sitzung)


def _starte_gui(sitzung: Sitzung) -> int:  # pragma: no cover - öffnet ein Fenster
    from ldv_automation.gui.start import starte_gui

    return starte_gui(sitzung)


if __name__ == "__main__":  # pragma: no cover - Programmstart
    sys.exit(main())
