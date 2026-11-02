"""Tests für ``daten_lesen`` gegen Fake-COM-Objekte (K6 Nr. 1-5, 7, 8 und Zusatzfälle)."""

from __future__ import annotations

import ast
import csv
from pathlib import Path

import daten_lesen
import pytest
from fake_polyfile import Protokoll, daten_datei, installiere_fake_win32

N = 5
RE = [1.0, 2.0, 3.0, 4.0, 5.0]
IM = [0.5, 0.25, -1.0, 0.0, 2.0]
DF = 0.5


def alle_signale(n: int = N) -> dict[tuple[str, str], dict[str, object]]:
    return {
        sig: {"re": [v * (k + 1) for v in RE[:n]], "im": IM[:n], "df": DF}
        for k, sig in enumerate(daten_lesen.AUSWAHL)
    }


def lauf(
    monkeypatch: pytest.MonkeyPatch,
    signale: dict[tuple[str, str], dict[str, object]],
    ziel: Path,
    log: Protokoll,
    **kw: object,
) -> int:
    pf = daten_datei(log, signale, **kw)  # type: ignore[arg-type]
    installiere_fake_win32(monkeypatch, pf)
    return daten_lesen.main("kopie.svd", str(ziel), 1)


def lies_csv(ziel: Path) -> list[list[str]]:
    with open(ziel, newline="", encoding="utf-8") as f:
        return list(csv.reader(f, delimiter=";"))


def test_csv_korrekt(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    ziel = tmp_path / "g.csv"
    log = Protokoll()
    code = lauf(monkeypatch, alle_signale(), ziel, log)
    zeilen = lies_csv(ziel)
    assert code == 0
    assert zeilen[0][0] == "f_Hz"
    assert len(zeilen[0]) == 1 + 2 * len(daten_lesen.AUSWAHL)
    assert zeilen[0][1] == "Vib X | Geschwindigkeit | Re"
    assert len(zeilen) == 1 + N  # Kopfzeile plus eine Zeile je Frequenzpunkt
    # Achse aus GetMidX: f_i = i * df, exakt darstellbar (rtol 0 genügt)
    assert [float(z[0]) for z in zeilen[1:]] == [i * DF for i in range(N)]
    assert [float(z[1]) for z in zeilen[1:]] == RE
    assert [float(z[2]) for z in zeilen[1:]] == IM
    assert not (tmp_path / ("g.csv" + daten_lesen.BEGLEIT_ENDUNG)).exists()
    assert log.geschlossen


def test_signal_ohne_realteil_fehlt(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    signale = alle_signale()
    signale[("Ref1", "Kraft")]["typen"] = (8,)  # kein Display-Typ 7
    ziel = tmp_path / "g.csv"
    code = lauf(monkeypatch, signale, ziel, Protokoll())
    kopf = lies_csv(ziel)[0]
    assert code == 3
    assert not any(s.startswith("Ref1 | Kraft") for s in kopf)
    assert len(kopf) == 1 + 2 * (len(daten_lesen.AUSWAHL) - 1)
    vermerk = (tmp_path / "g.csv.fehlend.txt").read_text(encoding="utf-8").splitlines()
    assert vermerk[0] == "# Fehlende Signale"
    assert vermerk[1].startswith("Ref1 | Kraft\tLookupError")
    assert len(vermerk) == 2
    ausgabe = capsys.readouterr().out
    assert "HINWEIS: 1 von 8" in ausgabe
    assert "fehlt Ref1 | Kraft" in ausgabe


@pytest.mark.parametrize("variante", ["im_kuerzer", "re_laenge_anders", "achse_anders"])
def test_abweichung_wird_abgelehnt(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path, variante: str
) -> None:
    signale = alle_signale()
    ziel_sig = ("Vib Y", "Geschwindigkeit")
    if variante == "im_kuerzer":
        signale[ziel_sig]["im"] = IM[:3]
    elif variante == "re_laenge_anders":
        signale[ziel_sig]["re"] = RE[:3]
        signale[ziel_sig]["im"] = IM[:3]
    else:
        signale[ziel_sig]["df"] = 1.0  # gleiche Länge, andere Achse
    ziel = tmp_path / "g.csv"
    code = lauf(monkeypatch, signale, ziel, Protokoll())
    assert code == 3
    kopf = lies_csv(ziel)[0]
    assert not any(s.startswith("Vib Y | Geschwindigkeit") for s in kopf)
    assert "Vib X | Geschwindigkeit | Re" in kopf
    text = (tmp_path / "g.csv.fehlend.txt").read_text(encoding="utf-8")
    assert "Vib Y | Geschwindigkeit\tValueError" in text


def test_kein_signal_lesbar(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    ziel = tmp_path / "g.csv"
    log = Protokoll()
    code = lauf(monkeypatch, {}, ziel, log)
    assert code == 1
    assert not ziel.exists()
    assert not (tmp_path / "g.csv.fehlend.txt").exists()
    assert "Keine Daten gelesen." in capsys.readouterr().out
    assert log.geschlossen


def test_close_auch_bei_ausnahme(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    log = Protokoll()
    pf = daten_datei(log, alle_signale())

    def kaputt() -> None:
        raise RuntimeError("COM weg")

    object.__setattr__(pf, "_methoden", {**pf._methoden, "GetPointDomains": kaputt})
    installiere_fake_win32(monkeypatch, pf)
    with pytest.raises(RuntimeError, match="COM weg"):
        daten_lesen.main("kopie.svd", str(tmp_path / "g.csv"), 1)
    assert log.geschlossen
    assert not (tmp_path / "g.csv").exists()


def test_nur_lesend(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    log = Protokoll()
    code = lauf(monkeypatch, alle_signale(), tmp_path / "g.csv", log)
    assert code == 0
    assert log.zuweisungen == [("ReadOnly", True, False)]  # genau eine, vor Open
    assert log.pfade == ["kopie.svd"]
    verboten = {"Save", "SaveAs", "Create", "CalcBands"}
    assert verboten.isdisjoint(log.zugriffe)


def test_domaene_nicht_fft_warnt(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    code = lauf(monkeypatch, alle_signale(), tmp_path / "g.csv", Protokoll(), domaenenname="Zeit")
    assert code == 0
    assert "WARNUNG: Domäne 1 heißt nicht 'FFT'" in capsys.readouterr().out


def test_vorhandene_zieldatei_nicht_ueberschrieben(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    ziel = tmp_path / "g.csv"
    ziel.write_text("alt", encoding="utf-8")
    log = Protokoll()
    code = lauf(monkeypatch, alle_signale(), ziel, log)
    assert code == 2
    assert ziel.read_text(encoding="utf-8") == "alt"
    assert not log.pfade  # Datei wurde gar nicht geöffnet
    assert "existiert bereits" in capsys.readouterr().out


def test_vorhandene_begleitdatei_blockiert(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    (tmp_path / "g.csv.fehlend.txt").write_text("alt", encoding="utf-8")
    assert lauf(monkeypatch, alle_signale(), tmp_path / "g.csv", Protokoll()) == 2


def test_ueberschreiben_ersetzt_und_raeumt_begleitdatei(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    ziel = tmp_path / "g.csv"
    ziel.write_text("alt", encoding="utf-8")
    begleit = tmp_path / "g.csv.fehlend.txt"
    begleit.write_text("alt", encoding="utf-8")
    installiere_fake_win32(monkeypatch, daten_datei(Protokoll(), alle_signale()))
    assert daten_lesen.main("kopie.svd", str(ziel), 1, ueberschreiben=True) == 0
    assert lies_csv(ziel)[0][0] == "f_Hz"
    assert not begleit.exists()


def test_cli(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    installiere_fake_win32(monkeypatch, daten_datei(Protokoll(), alle_signale()))
    ziel = tmp_path / "g.csv"
    assert daten_lesen.cli(["kopie.svd", str(ziel), "1"]) == 0
    assert daten_lesen.cli(["kopie.svd", str(ziel)]) == 2  # existiert jetzt
    assert daten_lesen.cli(["kopie.svd", str(ziel), "--ueberschreiben"]) == 0
    assert daten_lesen.cli(["nur_eins"]) == 2
    assert daten_lesen.cli(["--help"]) == 0
    assert daten_lesen.cli(["a", "b", "keine_zahl"]) == 2


def test_achse_nicht_lesbarer_label_und_einheit(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    log = Protokoll()
    pf = daten_datei(log, alle_signale())
    dom = pf.GetPointDomains().Item(1)
    dp = dom.DataPoints.Item(1)
    object.__setattr__(dp, "_fehler", {"MeasPoint": OSError("kein Label")})
    object.__setattr__(dom, "_methoden", {**dom._methoden, "GetYAxes": lambda d: 1 / 0})
    installiere_fake_win32(monkeypatch, pf)
    assert daten_lesen.main("k.svd", str(tmp_path / "g.csv"), 1) == 0
    ausgabe = capsys.readouterr().out
    assert "Label nicht lesbar (OSError)" in ausgabe
    assert "(Einheit nicht lesbar)" in ausgabe


def test_quelltext_ohne_verbotene_namen() -> None:
    baum = ast.parse(Path(daten_lesen.__file__).read_text(encoding="utf-8"))
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


@pytest.mark.parametrize(
    ("variante", "erwartet"),
    [
        ("re_laenge_anders", "Frequenzachse hat 3 Werte, das erste Signal hat 5"),
        ("achse_anders", "Frequenzachse weicht von der des ersten Signals ab"),
    ],
)
def test_meldetext_trennt_laenge_und_achswerte(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path, variante: str, erwartet: str
) -> None:
    signale = alle_signale()
    ziel_sig = ("Vib Y", "Geschwindigkeit")
    if variante == "re_laenge_anders":
        signale[ziel_sig]["re"] = RE[:3]
        signale[ziel_sig]["im"] = IM[:3]
    else:
        signale[ziel_sig]["df"] = 1.0  # gleiche Länge, andere Achse
    ziel = tmp_path / "g.csv"
    assert lauf(monkeypatch, signale, ziel, Protokoll()) == 3
    text = (tmp_path / "g.csv.fehlend.txt").read_text(encoding="utf-8")
    assert f"Vib Y | Geschwindigkeit\tValueError: {erwartet}" in text
    assert "(3 statt 3" not in text


@pytest.mark.parametrize("leer", ["re", "im"])
def test_leeres_signal_fehlt_mit_grund_keine_werte(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path, leer: str
) -> None:
    signale = alle_signale()
    ziel_sig = ("Vib Y", "Geschwindigkeit")
    signale[ziel_sig][leer] = []
    ziel = tmp_path / "g.csv"
    assert lauf(monkeypatch, signale, ziel, Protokoll()) == 3
    kopf = lies_csv(ziel)[0]
    assert not any(s.startswith("Vib Y | Geschwindigkeit") for s in kopf)
    text = (tmp_path / "g.csv.fehlend.txt").read_text(encoding="utf-8")
    assert "Vib Y | Geschwindigkeit\tValueError: keine Werte" in text


def test_alle_signale_leer_exit_1_ohne_csv(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    signale = {sig: {"re": [], "im": [], "df": DF} for sig in daten_lesen.AUSWAHL}
    ziel = tmp_path / "g.csv"
    log = Protokoll()
    assert lauf(monkeypatch, signale, ziel, log) == 1
    assert not ziel.exists()
    assert not (tmp_path / "g.csv.fehlend.txt").exists()
    assert "Keine Daten gelesen." in capsys.readouterr().out
    assert log.geschlossen
