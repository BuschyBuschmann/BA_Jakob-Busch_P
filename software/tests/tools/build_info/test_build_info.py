"""Build-Info-Skript (U5-2, ADR-012)."""

from __future__ import annotations

import importlib.util
import json
import shutil
import subprocess
import tomllib
from collections.abc import Sequence
from pathlib import Path
from typing import Any

import build_info
import pytest

from ldv_automation.protokoll import version

HASH = "a" * 40


def _ausfuehren(hash_text: str = HASH, status: str = "") -> build_info.Befehl:
    def ausfuehren(befehl: Sequence[str], _ordner: Path) -> str:
        return hash_text + "\n" if befehl[1] == "rev-parse" else status

    return ausfuehren


@pytest.mark.parametrize(("status", "dirty"), [("", False), (" M datei.py\n", True)])
def test_u5_2_schreibt_hash_und_dirty_flag(tmp_path: Path, status: str, dirty: bool) -> None:
    ziel = tmp_path / "_build_info.json"
    assert build_info.main(["--ziel", str(ziel)], _ausfuehren(status=status)) == 0
    daten = json.loads(ziel.read_text(encoding="utf-8"))
    assert daten["git_hash"] == HASH and daten["git_dirty"] is dirty
    # Gegenprobe: protokoll.version liest genau diese Datei, wenn git fehlt
    ziel.rename(tmp_path / version.BUILD_INFO_DATEI)

    def ohne_git(_b: Sequence[str], _o: Path) -> str:
        raise OSError("kein git")

    info = version.ermittle_build_info(paketordner=tmp_path, ausfuehren=ohne_git)
    assert (info.git_hash, info.git_dirty, info.quelle) == (HASH, dirty, "build_info")


def test_u5_2_ohne_gueltigen_hash_keine_datei(tmp_path: Path) -> None:
    ziel = tmp_path / "_build_info.json"
    assert build_info.main(["--ziel", str(ziel)], _ausfuehren(hash_text="kaputt")) == 1
    assert not ziel.exists()

    def scheitert(_b: Sequence[str], _o: Path) -> str:
        raise subprocess.CalledProcessError(128, "git")

    assert build_info.main(["--ziel", str(ziel)], scheitert) == 1
    assert not ziel.exists()


@pytest.mark.skipif(shutil.which("git") is None, reason="git nicht installiert")
def test_u5_2_mit_echtem_git_repository(tmp_path: Path) -> None:
    repo = tmp_path / "repo"
    repo.mkdir()

    def git(*args: str) -> None:
        subprocess.run(["git", *args], cwd=repo, check=True, capture_output=True)

    git("init", "-q")
    (repo / "a.txt").write_text("a", encoding="utf-8")
    git("add", "a.txt")
    git("-c", "user.name=t", "-c", "user.email=t@t", "commit", "-q", "-m", "x")
    daten = build_info.ermittle(repo)
    assert len(str(daten["git_hash"])) == 40 and daten["git_dirty"] is False
    (repo / "b.txt").write_text("b", encoding="utf-8")
    assert build_info.ermittle(repo)["git_dirty"] is True


def test_u5_2_ziel_passt_zu_version_und_wheel_konfiguration() -> None:
    assert build_info.ZIEL.name == version.BUILD_INFO_DATEI
    pyproject = tomllib.loads((build_info.SOFTWARE / "pyproject.toml").read_text("utf-8"))
    rad = pyproject["tool"]["hatch"]["build"]["targets"]["wheel"]
    assert "artifacts" not in rad  # Quellbaum-Datei wird nie gepackt (K-U5)
    assert rad["hooks"]["custom"]["path"] == "hatch_build.py"
    gitignore = (build_info.SOFTWARE / ".gitignore").read_text(encoding="utf-8")
    assert "src/ldv_automation/_build_info.json" in gitignore.splitlines()


def test_k_u5_fehlschlag_loescht_veraltete_datei(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    ziel = tmp_path / "_build_info.json"
    ziel.write_text('{"git_hash": "' + "b" * 40 + '", "git_dirty": false}', encoding="utf-8")
    assert build_info.main(["--ziel", str(ziel)], _ausfuehren(hash_text="kaputt")) == 1
    assert not ziel.exists()
    assert "gelöscht" in capsys.readouterr().err


# --- Hatch-Build-Hook (K-U5) ------------------------------------------------------------------


def _hook_modul() -> Any:
    spec = importlib.util.spec_from_file_location(
        "_hatch_build", build_info.SOFTWARE / "hatch_build.py"
    )
    assert spec is not None and spec.loader is not None
    modul = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modul)
    return modul


def _hook(root: Path, ziel: str = "wheel") -> Any:
    return _hook_modul().BuildInfoHook(str(root), {}, None, None, str(root / "dist"), ziel)


def _repo_mit_skript(tmp_path: Path) -> Path:
    root = tmp_path / "software"
    (root / "tools" / "build_info").mkdir(parents=True)
    shutil.copy(
        build_info.SOFTWARE / "tools" / "build_info" / "build_info.py",
        root / "tools" / "build_info" / "build_info.py",
    )
    return root


@pytest.mark.skipif(shutil.which("git") is None, reason="git nicht installiert")
def test_k_u5_hook_erzeugt_build_info_aus_aktuellem_head(tmp_path: Path) -> None:
    root = _repo_mit_skript(tmp_path)

    def git(*args: str) -> str:
        return subprocess.run(
            ["git", *args], cwd=root, check=True, capture_output=True, text=True
        ).stdout

    git("init", "-q")
    git("add", ".")
    git("-c", "user.name=t", "-c", "user.email=t@t", "commit", "-q", "-m", "x")
    # veraltete Datei im Quellbaum darf keine Rolle spielen
    (root / "_build_info.json").write_text('{"git_hash": "' + "b" * 40 + '"}', "utf-8")
    hook = _hook(root)
    build_data: dict[str, Any] = {"force_include": {}}
    hook.initialize("standard", build_data)
    ((quelle, ziel),) = build_data["force_include"].items()
    assert ziel == "ldv_automation/_build_info.json"
    daten = json.loads(Path(quelle).read_text(encoding="utf-8"))
    assert daten["git_hash"] == git("rev-parse", "HEAD").strip()
    hook.finalize("standard", build_data, "x.whl")
    assert not Path(quelle).exists()


def test_k_u5_hook_bricht_ohne_git_hash_ab(tmp_path: Path) -> None:
    root = _repo_mit_skript(tmp_path)  # kein Git-Repository
    with pytest.raises(RuntimeError, match="Wheel-Bau abgebrochen"):
        _hook(root).initialize("standard", {"force_include": {}})


def test_k_u5_hook_ueberspringt_editierbar_und_sdist(tmp_path: Path) -> None:
    root = _repo_mit_skript(tmp_path)
    daten: dict[str, Any] = {"force_include": {}}
    _hook(root).initialize("editable", daten)
    _hook(root, "sdist").initialize("standard", daten)
    assert daten == {"force_include": {}}
    _hook(root).finalize("editable", daten, "x")  # ohne temporären Ordner: nichts zu tun
