"""Erzeugt ``src/ldv_automation/_build_info.json`` vor dem Wheel-Bau (Plan P2, 4.4; ADR-012).

Auf dem Messrechner ist kein Git vorausgesetzt. Damit Messprotokolle trotzdem den Git-Hash
des Softwarestands tragen (KONVENTIONEN „Messdaten“), schreibt dieses Skript Hash und
Dirty-Flag in eine Datei im Paket. ``ldv_automation.protokoll.version`` liest zuerst Git
und nur ohne Git diese Datei.

Beim Wheel-Bau ruft der Hatch-Build-Hook ``software/hatch_build.py`` die Funktionen
:func:`ermittle` und :func:`schreibe` selbst auf und packt das Ergebnis ins Wheel (K-U5);
ein Wheel enthält damit immer den Hash des Stands, aus dem es gebaut wurde. Der
Kommandozeilenaufruf erzeugt die Datei nur im Quellbaum (z. B. für Tests ohne Git)::

    uv run python tools/build_info/build_info.py

Die Datei im Quellbaum ist per ``.gitignore`` ausgenommen und wird nie gepackt. Sie wird
bei jedem Aufruf neu geschrieben (sie ist kein Rohdatum). Das Skript importiert nichts aus
dem Hauptpaket (KONVENTIONEN, Werkzeuge).

Format (UTF-8, JSON)::

    {"git_hash": "<40 Hex-Zeichen>", "git_dirty": true|false,
     "erzeugt_utc": "<ISO 8601>", "erzeugt_von": "tools/build_info/build_info.py"}

Ist der Hash nicht ermittelbar, ist der Rückgabewert 1 und eine vorhandene Datei wird
**gelöscht**, damit kein veralteter Hash liegen bleibt (K-U5).
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from collections.abc import Callable, Sequence
from datetime import UTC, datetime
from pathlib import Path

SOFTWARE = Path(__file__).resolve().parent.parent.parent
"""Ordner ``software/`` (Arbeitsverzeichnis für Git)."""

ZIEL = SOFTWARE / "src" / "ldv_automation" / "_build_info.json"
"""Standardziel; Name muss zu ``protokoll.version.BUILD_INFO_DATEI`` passen."""

_HASH = re.compile(r"[0-9a-f]{40}")

Befehl = Callable[[Sequence[str], Path], str]
"""Führt einen Befehl im Ordner aus und gibt stdout zurück (``OSError``/``SubprocessError``)."""


class BuildInfoFehler(Exception):  # noqa: N818  (fachlicher Name)
    """Hash oder Status nicht ermittelbar."""


def _git(befehl: Sequence[str], ordner: Path) -> str:
    return subprocess.run(  # fester Befehl ohne Shell
        list(befehl), cwd=ordner, capture_output=True, text=True, check=True, timeout=30
    ).stdout


def ermittle(ordner: Path, ausfuehren: Befehl = _git) -> dict[str, object]:
    """Liest Hash und Dirty-Flag aus Git.

    ``git_dirty`` ist ``True``, wenn ``git status --porcelain`` irgendeine Änderung meldet
    (auch nicht verfolgte Dateien; die Build-Info selbst ist per ``.gitignore`` ausgenommen).

    Raises
    ------
    BuildInfoFehler
        Wenn Git fehlt, scheitert oder keinen gültigen Hash liefert.
    """
    try:
        git_hash = ausfuehren(["git", "rev-parse", "HEAD"], ordner).strip()
        status = ausfuehren(["git", "status", "--porcelain"], ordner)
    except (OSError, subprocess.SubprocessError) as fehler:
        raise BuildInfoFehler(f"git nicht ausführbar: {fehler}") from fehler
    if not _HASH.fullmatch(git_hash):
        raise BuildInfoFehler(f"git lieferte keinen gültigen Hash: {git_hash[:60]!r}")
    return {
        "git_hash": git_hash,
        "git_dirty": bool(status.strip()),
        "erzeugt_utc": datetime.now(UTC).isoformat(timespec="seconds"),
        "erzeugt_von": "tools/build_info/build_info.py",
    }


def schreibe(ziel: Path, daten: dict[str, object]) -> None:
    """Schreibt die Build-Info (UTF-8, ersetzt eine vorhandene Datei)."""
    ziel.write_text(json.dumps(daten, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main(argv: Sequence[str] | None = None, ausfuehren: Befehl = _git) -> int:
    """Einstieg; 0 bei Erfolg, 1 wenn keine Build-Info geschrieben wurde."""
    parser = argparse.ArgumentParser(description="Build-Info (Git-Hash) für das Wheel erzeugen")
    parser.add_argument("--repo", type=Path, default=SOFTWARE, help="Ordner im Git-Repository")
    parser.add_argument("--ziel", type=Path, default=ZIEL, help="Zieldatei")
    args = parser.parse_args(argv)
    try:
        daten = ermittle(args.repo, ausfuehren)
    except BuildInfoFehler as fehler:
        geloescht = ""
        if args.ziel.exists():
            args.ziel.unlink()
            geloescht = f"; vorhandene {args.ziel} gelöscht"
        print(f"Keine Build-Info geschrieben: {fehler}{geloescht}", file=sys.stderr)
        return 1
    schreibe(args.ziel, daten)
    hinweis = " (mit nicht eingecheckten Änderungen)" if daten["git_dirty"] else ""
    print(f"Build-Info geschrieben: {args.ziel}: {daten['git_hash']}{hinweis}")
    return 0


if __name__ == "__main__":  # pragma: no cover - Programmstart
    sys.exit(main())
