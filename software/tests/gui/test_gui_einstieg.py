"""Einstieg ``python -m ldv_automation`` und Architekturregeln der Oberfläche (UI-28).

Läuft im Standardlauf (ohne Qt).
"""

from __future__ import annotations

import ast
from pathlib import Path

import pytest

import ldv_automation
from ldv_automation import __main__ as einstieg
from ldv_automation.geraet.com.adapter import ComBetriebsart, PsvComGeraet
from ldv_automation.geraet.simulator import Simulator
from ldv_automation.sitzung import Betriebsart, GeraeteFabrik, Sitzung

GUI = Path(ldv_automation.__file__).resolve().parent / "gui"


def test_parser_standardwerte() -> None:
    args = einstieg.baue_parser().parse_args(["gui"])
    assert args.befehl == "gui"
    assert not args.psv and not args.start_psv
    assert args.betriebsart == "simulator"
    assert args.messdaten is None


def test_parser_messen_ist_als_anfang_nicht_waehlbar(capsys: pytest.CaptureFixture[str]) -> None:
    with pytest.raises(SystemExit):
        einstieg.baue_parser().parse_args(["gui", "--betriebsart", "messen"])
    assert "invalid choice" in capsys.readouterr().err


def test_parser_simulator_und_psv_schliessen_sich_aus() -> None:
    with pytest.raises(SystemExit):
        einstieg.baue_parser().parse_args(["gui", "--simulator", "--psv"])


def test_selbsttest_ueber_main(capsys: pytest.CaptureFixture[str]) -> None:
    assert einstieg.main(["selbsttest"]) == 0
    assert "Selbsttest bestanden" in capsys.readouterr().out


def test_fabrik_simulator_fuer_alle_betriebsarten() -> None:
    fabrik = einstieg.erzeuge_fabrik(
        psv=False, start_psv_erlaubt=False, messdaten_wurzel=lambda: None
    )
    for art in Betriebsart:
        geraet = fabrik(art)
        assert isinstance(geraet, Simulator)
        assert geraet.betriebsart == art.value


def test_fabrik_psv_nutzt_com_ausser_im_simulator(tmp_path: Path) -> None:
    fabrik = einstieg.erzeuge_fabrik(
        psv=True, start_psv_erlaubt=True, messdaten_wurzel=lambda: tmp_path
    )
    assert isinstance(fabrik(Betriebsart.SIMULATOR), Simulator)
    geraet = fabrik(Betriebsart.TROCKENLAUF)
    assert isinstance(geraet, PsvComGeraet)
    assert geraet.betriebsart is ComBetriebsart.TROCKENLAUF
    ohne = einstieg.erzeuge_fabrik(psv=True, start_psv_erlaubt=False, messdaten_wurzel=lambda: None)
    assert isinstance(ohne(Betriebsart.NUR_LESEN), PsvComGeraet)


def test_sitzung_aus_argumenten(tmp_path: Path) -> None:
    args = einstieg.baue_parser().parse_args(
        ["gui", "--betriebsart", "trockenlauf", "--messdaten", str(tmp_path)]
    )
    s = einstieg.erzeuge_sitzung(args)
    s.verarbeite()
    b = s.zustandsbild()
    assert b.betriebsart is Betriebsart.TROCKENLAUF
    assert b.messdaten_wurzel == str(tmp_path)


def test_start_psv_nur_mit_psv() -> None:
    args = einstieg.baue_parser().parse_args(["gui", "--start-psv"])
    with pytest.raises(SystemExit, match="nur zusammen mit --psv"):
        einstieg.erzeuge_sitzung(args)


@pytest.mark.parametrize(("antwort", "erlaubt"), [("JA", True), ("ja", False), ("", False)])
def test_start_psv_verlangt_getipptes_ja(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
    antwort: str,
    erlaubt: bool,
) -> None:
    gesehen: dict[str, object] = {}
    echte = einstieg.erzeuge_fabrik

    def fabrik_spion(**kw: object) -> GeraeteFabrik:
        gesehen.update(kw)
        return echte(**kw)  # type: ignore[arg-type]

    monkeypatch.setattr(einstieg, "erzeuge_fabrik", fabrik_spion)
    args = einstieg.baue_parser().parse_args(
        ["gui", "--psv", "--start-psv", "--messdaten", str(tmp_path)]
    )
    s = einstieg.erzeuge_sitzung(args, eingabe=lambda _t: antwort)
    assert gesehen["start_psv_erlaubt"] is erlaubt
    if not erlaubt:
        assert "nicht bestätigt" in capsys.readouterr().out.lower()
    wurzel = gesehen["messdaten_wurzel"]
    assert callable(wurzel) and wurzel() == tmp_path
    (tmp_path / "neu").mkdir()  # U5/B4: die Sitzung nimmt nur vorhandene Ordner an
    s.setze_messdaten_wurzel(tmp_path / "neu")
    assert wurzel() == tmp_path / "neu"


def test_main_startet_gui_mit_sitzung(monkeypatch: pytest.MonkeyPatch) -> None:
    gestartet: list[Sitzung] = []

    def starte(s: Sitzung) -> int:
        gestartet.append(s)
        return 0

    monkeypatch.setattr(einstieg, "_starte_gui", starte)
    assert einstieg.main(["gui"]) == 0
    assert len(gestartet) == 1


def _gui_baeume() -> list[tuple[Path, ast.Module]]:
    return [(p, ast.parse(p.read_text(encoding="utf-8"))) for p in sorted(GUI.glob("*.py"))]


def test_ui_28_gui_startet_keinen_thread() -> None:
    verboten = {"threading", "_thread", "concurrent", "multiprocessing", "asyncio"}
    for pfad, baum in _gui_baeume():
        for knoten in ast.walk(baum):
            if isinstance(knoten, ast.Import):
                namen = [a.name.split(".")[0] for a in knoten.names]
            elif isinstance(knoten, ast.ImportFrom):
                namen = [(knoten.module or "").split(".")[0]]
            else:
                continue
            assert not set(namen) & verboten, f"{pfad.name}: {namen}"
        text = pfad.read_text(encoding="utf-8")
        for name in ("QThread", "QThreadPool", "QRunnable", "moveToThread"):
            assert name not in text, pfad.name


def test_ui_28_gui_kennt_nur_sitzung_und_domaene() -> None:
    erlaubt = ("ldv_automation.sitzung", "ldv_automation.domaene", "ldv_automation.gui")
    for pfad, baum in _gui_baeume():
        for knoten in ast.walk(baum):
            if isinstance(knoten, ast.ImportFrom) and (knoten.module or "").startswith(
                "ldv_automation"
            ):
                modul = knoten.module or ""
                assert modul.startswith(erlaubt), f"{pfad.name}: {modul}"


def test_ui_28_qt_freie_module_importieren_kein_qt() -> None:
    for name in ("__init__.py", "anzeige.py", "tokens.py", "fassade.py"):
        baum = ast.parse((GUI / name).read_text(encoding="utf-8"))
        for knoten in ast.walk(baum):
            if isinstance(knoten, ast.ImportFrom):
                assert not (knoten.module or "").startswith("PySide6"), name
            elif isinstance(knoten, ast.Import):
                assert not any(a.name.startswith("PySide6") for a in knoten.names), name
