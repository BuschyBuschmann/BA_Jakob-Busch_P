"""Selbsttest und Betriebsart-Abbildung im Einstieg (U5-1, B9)."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pytest

import ldv_automation.__main__ as einstieg
from ldv_automation.geraet.com.adapter import ComBetriebsart, PsvComGeraet
from ldv_automation.geraet.simulator import BETRIEBSARTEN, Simulator
from ldv_automation.sitzung import Betriebsart

PYWIN32 = ("win32", "pythoncom", "pywintypes")


def test_u5_1_selbsttest_besteht_ohne_pywin32() -> None:
    zeilen: list[str] = []
    assert einstieg.selbsttest(ausgabe=zeilen.append) == 0
    assert zeilen[-1] == "Selbsttest bestanden"
    assert not any("FEHLER" in z for z in zeilen)
    assert not [m for m in sys.modules if m.startswith(PYWIN32)]


def test_u5_1_selbsttest_als_prozess() -> None:
    ergebnis = subprocess.run(
        [sys.executable, "-m", "ldv_automation", "selbsttest"],
        capture_output=True,
        text=True,
        timeout=120,
        check=False,
    )
    assert ergebnis.returncode == 0, ergebnis.stdout + ergebnis.stderr
    assert "Selbsttest bestanden" in ergebnis.stdout


def test_u5_1_selbsttest_mit_ordner_behaelt_ergebnisse(tmp_path: Path) -> None:
    assert einstieg.selbsttest(tmp_path, ausgabe=lambda _z: None) == 0
    ordner = sorted(p.name for p in tmp_path.iterdir())
    assert len(ordner) == 2
    assert ordner[0].endswith("_simulator") and ordner[1].endswith("_trockenlauf")
    assert len(list((tmp_path / ordner[0]).glob("*.svd"))) == 2


def test_u5_1_selbsttest_meldet_gescheiterte_pruefung(tmp_path: Path) -> None:
    (tmp_path / ".git").mkdir()  # Ordner in einem Git-Repository ist ungeeignet
    zeilen: list[str] = []
    assert einstieg.selbsttest(tmp_path, ausgabe=zeilen.append) == 1
    assert zeilen[-1] == "Selbsttest FEHLGESCHLAGEN"
    assert any("FEHLER Messdaten-Ordner geeignet" in z for z in zeilen)


def test_u5_1_selbsttest_meldet_unerwarteten_fehler(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    def kaputt(*_a: object, **_k: object) -> None:
        raise RuntimeError("kaputt")

    monkeypatch.setattr(einstieg, "_selbsttest_ablauf", kaputt)
    zeilen: list[str] = []
    assert einstieg.selbsttest(ausgabe=zeilen.append) == 1
    assert "RuntimeError: kaputt" in zeilen[1]
    assert zeilen[-1].startswith("Selbsttest FEHLGESCHLAGEN")


def test_b9_abbildung_deckt_jede_betriebsart_ab() -> None:
    assert set(einstieg.SIMULATOR_BETRIEBSART) == set(Betriebsart)
    assert set(einstieg.COM_BETRIEBSART) == set(Betriebsart)
    assert sorted(einstieg.SIMULATOR_BETRIEBSART.values()) == sorted(BETRIEBSARTEN)
    assert einstieg.COM_BETRIEBSART[Betriebsart.SIMULATOR] is None
    com = {a: c for a, c in einstieg.COM_BETRIEBSART.items() if c is not None}
    assert sorted(c.name for c in com.values()) == sorted(c.name for c in ComBetriebsart)
    for art, c in com.items():
        assert c.name == art.name


def test_b9_fabrik_nutzt_die_abbildung(monkeypatch: pytest.MonkeyPatch) -> None:
    fabrik = einstieg.erzeuge_fabrik(
        psv=False, start_psv_erlaubt=False, messdaten_wurzel=lambda: None
    )
    for art in Betriebsart:
        geraet = fabrik(art)
        assert isinstance(geraet, Simulator)
        assert geraet.betriebsart == einstieg.SIMULATOR_BETRIEBSART[art]

    import ldv_automation.geraet.com.pywin32_bindung as pb

    class Attrappe:
        pass

    monkeypatch.setattr(pb, "Pywin32Bindung", Attrappe)
    psv = einstieg.erzeuge_fabrik(
        psv=True, start_psv_erlaubt=False, messdaten_wurzel=lambda: Path("/m")
    )
    assert isinstance(psv(Betriebsart.SIMULATOR), Simulator)
    for art in (Betriebsart.NUR_LESEN, Betriebsart.TROCKENLAUF, Betriebsart.MESSEN):
        geraet = psv(art)
        assert isinstance(geraet, PsvComGeraet)
        assert geraet.betriebsart is einstieg.COM_BETRIEBSART[art]
