"""Tests für ``einstellungen_lesen`` gegen Fake-COM-Objekte (K6 Nr. 5-8)."""

from __future__ import annotations

import ast
from pathlib import Path

import einstellungen_lesen
import pytest
from fake_polyfile import Knoten, Protokoll, einstellungen_datei, installiere_fake_win32, sammlung


def test_attributefehler_nicht_lesbar_rest_laeuft(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    log = Protokoll()
    pf = einstellungen_datei(
        log,
        {
            "FftProperties": {"Bandwidth": 1000.0, "Lines": 400},  # StartFrequency fehlt
            "AverageProperties": {"Type": 1, "Count": 5},
        },
    )
    installiere_fake_win32(monkeypatch, pf)
    assert einstellungen_lesen.main("kopie.svd") == 0
    ausgabe = capsys.readouterr().out
    assert "StartFrequency: nicht lesbar (AttributeError)" in ausgabe
    assert "Bandwidth = 1000.0" in ausgabe
    assert "Count = 5" in ausgabe  # nachfolgender Abschnitt wurde noch gelesen
    assert "Datei geschlossen." in ausgabe


def test_has_false_und_has_fehlt(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    log = Protokoll()
    pf = einstellungen_datei(log, {"FftProperties": None, "AverageProperties": {"Type": 1}})
    # HasTriggerProperties gibt es gar nicht (AttributeError), HasGeneralProperties wirft COM-Fehler
    props = pf.Infos.AcquisitionInfoModes.ActiveProperties
    object.__setattr__(props, "_fehler", {"HasGeneralProperties": OSError("COM")})
    installiere_fake_win32(monkeypatch, pf)
    assert einstellungen_lesen.main("kopie.svd") == 0
    ausgabe = capsys.readouterr().out
    assert "[FFT] nicht vorhanden\n" in ausgabe
    assert "[Trigger] nicht vorhanden (HasTriggerProperties)" in ausgabe
    assert "[Allgemein] nicht lesbar (OSError: COM)" in ausgabe
    assert "[Mittelung]" in ausgabe


def test_aufrufbare_eigenschaft_wird_gemeldet(capsys: pytest.CaptureFixture[str]) -> None:
    obj = Knoten(Protokoll(), {"Name": "x", "Methode": lambda: 1, "Liste": (1, 2)})
    assert einstellungen_lesen.lies(obj, ["Name", "Methode", "Liste"]) == (2, 0)
    ausgabe = capsys.readouterr().out
    assert "Methode: übersprungen (aufrufbar, keine Eigenschaft)" in ausgabe
    assert "Liste = [1, 2]" in ausgabe


def test_waveform_cast_hinweis(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    log = Protokoll()
    waveform = Knoten(log)  # keine Eigenschaft lesbar
    gen = Knoten(log, {"Active": True, "Waveform": waveform})
    gen_ohne = Knoten(log, {"Active": False}, fehler={"Waveform": OSError("kein Cast")})
    pf = einstellungen_datei(log, {"FftProperties": {}})
    props = pf.Infos.AcquisitionInfoModes.ActiveProperties
    object.__setattr__(
        props,
        "_werte",
        {
            **props._werte,
            "HasGeneratorsProperties": True,
            "GeneratorsProperties": sammlung(log, [gen, gen_ohne]),
        },
    )
    installiere_fake_win32(monkeypatch, pf)
    assert einstellungen_lesen.main("kopie.svd") == 0
    ausgabe = capsys.readouterr().out
    assert ausgabe.count("Waveform-Parameter nicht lesbar (Cast auf das konkrete") == 2
    assert "Waveform: nicht lesbar (OSError)" in ausgabe


def test_kanaele_und_fehler_je_kanal(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    log = Protokoll()
    kanal = Knoten(log, {"Name": "Vib X", "Unit": "m/s"})

    def item(i: int) -> Knoten:
        if i == 2:
            raise OSError("Kanal kaputt")
        return kanal

    pf = einstellungen_datei(log, {})
    props = pf.Infos.AcquisitionInfoModes.ActiveProperties
    object.__setattr__(
        props,
        "_werte",
        {
            **props._werte,
            "HasChannelsProperties": True,
            "ChannelsProperties": Knoten(log, {"Count": 2}, {"Item": item}),
        },
    )
    installiere_fake_win32(monkeypatch, pf)
    assert einstellungen_lesen.main("kopie.svd") == 0
    ausgabe = capsys.readouterr().out
    assert "Name = 'Vib X'" in ausgabe
    assert "nicht lesbar (OSError: Kanal kaputt)" in ausgabe


def test_close_auch_bei_ausnahme(monkeypatch: pytest.MonkeyPatch) -> None:
    log = Protokoll()
    pf = einstellungen_datei(log, {})
    object.__setattr__(pf, "_fehler", {"Infos": RuntimeError("COM weg")})
    installiere_fake_win32(monkeypatch, pf)
    with pytest.raises(RuntimeError, match="COM weg"):
        einstellungen_lesen.main("kopie.svd")
    assert log.geschlossen


def test_nur_lesend(monkeypatch: pytest.MonkeyPatch) -> None:
    log = Protokoll()
    pf = einstellungen_datei(log, {"FftProperties": {"Bandwidth": 1.0}})
    installiere_fake_win32(monkeypatch, pf)
    assert einstellungen_lesen.main("kopie.svd") == 0
    assert log.zuweisungen == [("ReadOnly", True, False)]
    assert log.pfade == ["kopie.svd"]
    assert {"Save", "SaveAs", "Create", "CalcBands"}.isdisjoint(log.zugriffe)


def test_quelltext_ohne_verbotene_namen() -> None:
    baum = ast.parse(Path(einstellungen_lesen.__file__).read_text(encoding="utf-8"))
    namen = {n.attr for n in ast.walk(baum) if isinstance(n, ast.Attribute)}
    namen |= {n.id for n in ast.walk(baum) if isinstance(n, ast.Name)}
    assert {"Save", "SaveAs", "Create", "CalcBands", "eval", "exec", "pickle"}.isdisjoint(namen)
    zuweisungen = [
        t.attr
        for n in ast.walk(baum)
        if isinstance(n, ast.Assign | ast.AugAssign | ast.AnnAssign)
        for t in (n.targets if isinstance(n, ast.Assign) else [n.target])
        if isinstance(t, ast.Attribute)
    ]
    assert zuweisungen == ["ReadOnly"]  # einzige Zuweisung an ein Attribut: ReadOnly = True
