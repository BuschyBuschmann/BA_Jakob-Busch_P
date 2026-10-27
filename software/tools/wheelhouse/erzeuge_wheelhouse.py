"""Lädt die Abhängigkeiten für den Messrechner als Windows-Wheels in einen Ordner (Wheelhouse).

Läuft auf einem Rechner **mit Internet** (beliebiges Betriebssystem mit Python und pip), nicht
auf dem Messrechner. Das Skript bündelt nur den dokumentierten ``pip download``-Befehl aus
``in_progress/versuche/2026-11-02_prototyp/installation_messrechner.md`` (Abschnitt 3). Es
baut kein Wheel des eigenen Pakets und importiert nichts aus dem Hauptpaket.

Aufruf (aus ``software/``)::

    python tools/wheelhouse/erzeuge_wheelhouse.py --nur-anzeigen
    python tools/wheelhouse/erzeuge_wheelhouse.py --ziel wheelhouse

Die Versionen entsprechen ``software/uv.lock`` (Stand 2026-10-27). Ändert sich das Lockfile,
müssen die Konstanten unten angepasst werden. Die Plattformangaben erzwingen Wheels für
Windows x64 und CPython 3.11, unabhängig vom Rechner, auf dem das Skript läuft. Hinweis:
``pip`` wertet Umgebungsmarker (z. B. ``sys_platform == 'win32'``) auf dem laufenden Rechner
aus; deshalb stehen die Pakete hier als feste Pins ohne Marker.
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from collections.abc import Sequence

PINS: tuple[str, ...] = (
    "pyside6-essentials==6.11.3",  # pyproject.toml; ADR-001 (Nachtrag), nicht 6.12.0
    "shiboken6==6.11.3",  # Abhängigkeit von pyside6-essentials, uv.lock
    "pywin32==312",  # Extra "com" (pywin32>=306), Stand uv.lock
)
"""Feste Pins aus ``pyproject.toml`` und ``uv.lock``."""

OPTIONAL_UV = "uv"
"""Nur mit ``--mit-uv``; nicht im Lockfile, ungepinnt (uv ist für den Messrechner optional)."""


def baue_befehl(ziel: str, *, mit_uv: bool = False) -> list[str]:
    """Baut den ``pip download``-Befehl für Windows x64 / CPython 3.11.

    Parameters
    ----------
    ziel : str
        Zielordner des Wheelhouse (wird von pip angelegt).
    mit_uv : bool
        ``True``: zusätzlich das Paket ``uv`` laden.

    Returns
    -------
    list of str
        Befehl als Argumentliste (ohne Shell).
    """
    pakete = [*PINS, OPTIONAL_UV] if mit_uv else list(PINS)
    return [
        sys.executable,
        "-m",
        "pip",
        "download",
        "--dest",
        ziel,
        "--platform",
        "win_amd64",
        "--python-version",
        "3.11",
        "--implementation",
        "cp",
        "--abi",
        "cp311",
        "--only-binary=:all:",
        *pakete,
    ]


def main(argv: Sequence[str] | None = None) -> int:
    """Einstieg; gibt den Rückgabewert des Prozesses zurück."""
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0] if __doc__ else None)
    parser.add_argument("--ziel", default="wheelhouse", help="Zielordner (Standard: wheelhouse)")
    parser.add_argument("--mit-uv", action="store_true", help="zusätzlich uv laden (optional)")
    parser.add_argument(
        "--nur-anzeigen", action="store_true", help="Befehl nur ausgeben, nichts herunterladen"
    )
    args = parser.parse_args(argv)
    befehl = baue_befehl(args.ziel, mit_uv=args.mit_uv)
    print(" ".join(befehl))
    if args.nur_anzeigen:
        return 0
    return subprocess.run(befehl, check=False).returncode


if __name__ == "__main__":
    sys.exit(main())
