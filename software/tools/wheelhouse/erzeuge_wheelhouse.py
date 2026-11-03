"""Lädt die Abhängigkeiten für den Messrechner als Windows-Wheels in einen Ordner (Wheelhouse).

Läuft auf einem Rechner **mit Internet** (beliebiges Betriebssystem mit Python und pip), nicht
auf dem Messrechner. Das Skript bündelt nur den dokumentierten ``pip download``-Befehl aus
``in_progress/versuche/2026-11-02_prototyp/installation_messrechner.md`` (Abschnitt 3). Es
baut kein Wheel des eigenen Pakets und importiert nichts aus dem Hauptpaket.

Aufruf (aus ``software/``)::

    python tools/wheelhouse/erzeuge_wheelhouse.py --nur-anzeigen
    python tools/wheelhouse/erzeuge_wheelhouse.py --ziel wheelhouse

Die Versionen entsprechen ``software/uv.lock`` (Stand 2026-11-03). Ändert sich das Lockfile,
müssen die Konstanten unten angepasst werden; ein Test (``test_wheelhouse_pins.py``)
erzwingt das. Die Plattformangaben erzwingen Wheels für Windows x64 und CPython 3.11,
unabhängig vom Rechner, auf dem das Skript läuft. Hinweis: ``pip`` wertet Umgebungsmarker
(z. B. ``sys_platform == 'win32'``) auf dem laufenden Rechner aus; deshalb stehen die Pakete
hier als feste Pins ohne Marker.
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from collections.abc import Sequence

PINS: tuple[str, ...] = (
    "numpy==2.4.6",  # pyproject.toml, uv.lock (fehlte bis P-AUSW T1.1 in dieser Liste)
    "pyside6-essentials==6.11.3",  # pyproject.toml; ADR-001 (Nachtrag), nicht 6.12.0
    "shiboken6==6.11.3",  # Abhängigkeit von pyside6-essentials, uv.lock
    "pywin32==312",  # Extra "com" (pywin32>=306), Stand uv.lock
    # Auswertungsoberfläche (P-AUSW T1.1): matplotlib und seine Abhängigkeiten laut uv.lock
    "matplotlib==3.11.2",  # pyproject.toml
    "contourpy==1.3.3",
    "cycler==0.12.1",
    "fonttools==4.68.0",
    "kiwisolver==1.5.1",
    "packaging==26.3",
    "pillow==13.0.0",
    "pyparsing==3.3.3",
    "python-dateutil==3.0.0",
    "six==1.17.0",  # Abhängigkeit von python-dateutil
    "tzdata==2026.6",  # Abhängigkeit von python-dateutil 3.0.0 (im Plan P-AUSW nicht genannt)
    "olefile==0.47",  # pyproject.toml: .svd-Leser im Paket (ADR-020)
)
"""Feste Pins aus ``pyproject.toml`` und ``uv.lock``.

``tests/tools/wheelhouse/test_wheelhouse_pins.py`` gleicht die Liste mit ``uv.lock`` ab."""

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
