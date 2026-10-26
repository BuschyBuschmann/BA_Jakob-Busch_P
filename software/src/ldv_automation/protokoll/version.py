"""Paketversion und Git-Hash für Messprotokolle (Plan P2, 4.4; ADR-012).

Reihenfolge der Quellen:

1. ``git rev-parse HEAD`` und ``git status --porcelain``, wenn das Paket aus einem
   Git-Arbeitsverzeichnis gestartet wird;
2. sonst die beim Wheel-Bau erzeugte Datei ``ldv_automation/_build_info.json`` mit den
   Schlüsseln ``git_hash`` (Text) und ``git_dirty`` (bool). Das Erzeugungsskript ist
   Teil von Paket U5.

Ist keine Quelle verfügbar, bleibt ``git_hash`` ``None`` und :attr:`BuildInfo.grund` nennt
den Grund. Ohne Git-Hash ist der Messbetrieb gesperrt (Prüfung in der Sitzung).
"""

from __future__ import annotations

import json
import re
import subprocess
from collections.abc import Callable, Sequence
from dataclasses import dataclass
from pathlib import Path

from ldv_automation import __version__

BUILD_INFO_DATEI = "_build_info.json"
_PAKETORDNER = Path(__file__).resolve().parent.parent
_HASH_MUSTER = re.compile(r"[0-9a-f]{40}")

Befehlsausfuehrer = Callable[[Sequence[str], Path], str]
"""Führt einen Befehl im Ordner aus und gibt stdout zurück; wirft ``OSError`` bzw.
``subprocess.SubprocessError`` bei Fehlschlag."""


@dataclass(frozen=True, kw_only=True)
class BuildInfo:
    """Versionsangaben des laufenden Pakets.

    Parameters
    ----------
    paket_version : str
        Version aus ``ldv_automation.__version__``.
    git_hash : str or None
        Vollständiger Commit-Hash (40 Hex-Zeichen) oder ``None``.
    git_dirty : bool or None
        ``True``, wenn das Arbeitsverzeichnis Änderungen hatte; ``None`` wenn unbekannt.
    quelle : str
        ``"git"``, ``"build_info"`` oder ``"keine"``.
    grund : str or None
        Warum kein Hash vorliegt (nur bei ``git_hash is None``).
    """

    paket_version: str
    git_hash: str | None
    git_dirty: bool | None
    quelle: str
    grund: str | None = None


def _fuehre_aus(befehl: Sequence[str], ordner: Path) -> str:
    ergebnis = subprocess.run(  # fester Befehl ohne Shell
        list(befehl),
        cwd=ordner,
        capture_output=True,
        text=True,
        check=True,
        timeout=10,
    )
    return ergebnis.stdout


def ermittle_build_info(
    *,
    paketordner: Path = _PAKETORDNER,
    ausfuehren: Befehlsausfuehrer = _fuehre_aus,
) -> BuildInfo:
    """Ermittelt Paketversion, Git-Hash und Dirty-Flag.

    Parameters
    ----------
    paketordner : pathlib.Path
        Ordner des Pakets ``ldv_automation`` (dort liegt ggf. ``_build_info.json``).
    ausfuehren : callable
        Befehlsausführung (injizierbar für Tests).

    Returns
    -------
    BuildInfo
        Nie eine Ausnahme: Fehlschläge stehen in :attr:`BuildInfo.grund`.
    """
    gruende: list[str] = []
    try:
        hash_text = ausfuehren(["git", "rev-parse", "HEAD"], paketordner).strip()
        status = ausfuehren(["git", "status", "--porcelain"], paketordner)
        if _HASH_MUSTER.fullmatch(hash_text):
            return BuildInfo(
                paket_version=__version__,
                git_hash=hash_text,
                git_dirty=bool(status.strip()),
                quelle="git",
            )
        gruende.append(f"git lieferte keinen gültigen Hash: {hash_text[:60]!r}")
    except (OSError, subprocess.SubprocessError) as fehler:
        gruende.append(f"git nicht verfügbar: {type(fehler).__name__}")

    datei = paketordner / BUILD_INFO_DATEI
    try:
        daten = json.loads(datei.read_text(encoding="utf-8"))
        git_hash = daten.get("git_hash") if isinstance(daten, dict) else None
        dirty = daten.get("git_dirty") if isinstance(daten, dict) else None
        if isinstance(git_hash, str) and _HASH_MUSTER.fullmatch(git_hash):
            return BuildInfo(
                paket_version=__version__,
                git_hash=git_hash,
                git_dirty=dirty if isinstance(dirty, bool) else None,
                quelle="build_info",
            )
        gruende.append(f"{BUILD_INFO_DATEI} ohne gültigen git_hash")
    except FileNotFoundError:
        gruende.append(f"{BUILD_INFO_DATEI} fehlt")
    except (OSError, ValueError) as fehler:
        gruende.append(f"{BUILD_INFO_DATEI} nicht lesbar: {fehler}")

    return BuildInfo(
        paket_version=__version__,
        git_hash=None,
        git_dirty=None,
        quelle="keine",
        grund="; ".join(gruende),
    )
