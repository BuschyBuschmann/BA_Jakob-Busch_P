"""Hatch-Build-Hook: Build-Info (Git-Hash) entsteht beim Wheel-Bau selbst (ADR-012, K-U5).

Beim Bau eines Wheels ermittelt der Hook Hash und Dirty-Flag aus dem **aktuellen** Git-Stand
(``tools/build_info/build_info.py``, ``ermittle``) und legt sie als
``ldv_automation/_build_info.json`` ins Wheel. Eine im Quellbaum liegende Datei wird nie
gepackt (sie ist per ``.gitignore`` ausgenommen). So kann kein Wheel mit fremdem oder
veraltetem Hash entstehen.

Ist kein Git-Hash ermittelbar (kein Git, kein Repository, z. B. Bau aus einem sdist),
bricht der Bau ab. Editierbare Installationen (``uv sync``) bleiben unberührt; dort liest
``protokoll.version`` den Hash direkt aus Git.

Bauen (aus ``software/``): ``uv build --wheel``.
"""

from __future__ import annotations

import importlib.util
import shutil
import tempfile
from pathlib import Path
from types import ModuleType
from typing import Any

from hatchling.builders.hooks.plugin.interface import BuildHookInterface

ZIEL_IM_WHEEL = "ldv_automation/_build_info.json"
SKRIPT = Path("tools") / "build_info" / "build_info.py"


def lade_build_info_modul(root: Path) -> ModuleType:
    """Lädt ``tools/build_info/build_info.py`` (kein Import aus dem Hauptpaket)."""
    spec = importlib.util.spec_from_file_location("_ldv_build_info", root / SKRIPT)
    if spec is None or spec.loader is None:  # pragma: no cover - Datei fehlt im Quellbaum
        raise RuntimeError(f"Build-Info-Skript nicht gefunden: {root / SKRIPT}")
    modul = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modul)
    return modul


class BuildInfoHook(BuildHookInterface[Any]):
    """Erzeugt die Build-Info beim Wheel-Bau und packt sie ins Wheel."""

    PLUGIN_NAME = "build-info"

    def initialize(self, version: str, build_data: dict[str, Any]) -> None:
        """Ermittelt den Git-Stand und fügt die Build-Info dem Wheel hinzu.

        Raises
        ------
        RuntimeError
            Wenn kein gültiger Git-Hash ermittelbar ist (Bau bricht ab).
        """
        self._ordner: str | None = None
        if self.target_name != "wheel" or version == "editable":
            return
        root = Path(self.root)
        modul = lade_build_info_modul(root)
        try:
            daten = modul.ermittle(root)
        except modul.BuildInfoFehler as fehler:
            raise RuntimeError(
                f"Wheel-Bau abgebrochen: keine Build-Info ({fehler}). Wheels nur aus dem "
                "Git-Repository bauen (uv build --wheel)."
            ) from fehler
        self._ordner = tempfile.mkdtemp(prefix="ldv_build_info_")
        datei = Path(self._ordner) / "_build_info.json"
        modul.schreibe(datei, daten)
        build_data.setdefault("force_include", {})[str(datei)] = ZIEL_IM_WHEEL

    def finalize(self, version: str, build_data: dict[str, Any], artifact_path: str) -> None:
        """Löscht die temporäre Build-Info nach dem Bau."""
        ordner = getattr(self, "_ordner", None)
        if ordner:
            shutil.rmtree(ordner, ignore_errors=True)
