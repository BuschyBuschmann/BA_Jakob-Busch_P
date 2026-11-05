"""Verwaiste Zwischendateien des Exports erkennen und entfernen (K-AUSW-T4, Export-Abbruch)."""

from __future__ import annotations

import os
from pathlib import Path

import numpy as np
import pytest

from ldv_automation.auswertung import export
from ldv_automation.auswertung.export import (
    entferne_verwaiste_tmp,
    tmp_pfade,
    unvollstaendiger_export,
)
from ldv_automation.protokoll.version import BuildInfo

BUILD = BuildInfo(paket_version="0.1.0", git_hash="a" * 40, git_dirty=False, quelle="git")


def test_tmp_pfade_sind_versteckt_und_tragen_den_basisnamen(tmp_path: Path) -> None:
    npz, js = tmp_pfade(tmp_path / "probe.v1")
    assert npz == tmp_path / ".probe.v1.npz.tmp"
    assert js == tmp_path / ".probe.v1.json.tmp"


def test_tmp_pfade_stimmen_mit_dem_schreibweg_ueberein(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Drift-Wächter: ``schreibe_export`` benennt genau diese Dateien um."""
    gesehen: list[Path] = []
    echt = os.replace

    def merke(quelle: str | os.PathLike[str], ziel: str | os.PathLike[str]) -> None:
        gesehen.append(Path(quelle))
        echt(quelle, ziel)

    monkeypatch.setattr(os, "replace", merke)
    basis = tmp_path / "ex"
    export.schreibe_export({"x": np.arange(3.0)}, {}, basis, messdatei={}, build_info=BUILD)
    assert tuple(gesehen) == tmp_pfade(basis)


def test_verwaiste_tmp_werden_entfernt_und_gemeldet(tmp_path: Path) -> None:
    basis = tmp_path / "ex"
    a, b = tmp_pfade(basis)
    a.write_bytes(b"halb")
    b.write_text("{", encoding="utf-8")
    fremd = tmp_path / ".anderer.npz.tmp"  # anderer Basisname: unberührt
    fremd.write_bytes(b"x")
    assert set(entferne_verwaiste_tmp(basis)) == {a, b}
    assert not a.exists() and not b.exists() and fremd.exists()
    assert entferne_verwaiste_tmp(basis) == ()  # nichts mehr zu tun


def test_nur_eine_verwaiste_datei_und_fehlender_ordner(tmp_path: Path) -> None:
    basis = tmp_path / "ex"
    a, _b = tmp_pfade(basis)
    a.write_bytes(b"halb")
    assert entferne_verwaiste_tmp(basis) == (a,)
    assert entferne_verwaiste_tmp(tmp_path / "gibtsnicht" / "ex") == ()


def test_einzelne_npz_ohne_json_wird_gemeldet_nicht_geloescht(tmp_path: Path) -> None:
    basis = tmp_path / "ex"
    assert unvollstaendiger_export(basis) is None
    npz = tmp_path / "ex.npz"
    npz.write_bytes(b"npz")
    assert unvollstaendiger_export(basis) == npz
    assert entferne_verwaiste_tmp(basis) == () and npz.exists()  # Ziel, kein Zwischenstand
    (tmp_path / "ex.json").write_text("{}", encoding="utf-8")
    assert unvollstaendiger_export(basis) is None
