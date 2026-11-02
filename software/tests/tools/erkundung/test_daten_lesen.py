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


# --- Konfigurierbare Auswahl, Domäne, Amplitude, --liste (Golden File v2) ---

ZIEL_SIG = ("Ref1 & Ref2", "Kohärenz")


def v2_signale() -> dict[tuple[str, str], dict[str, object]]:
    signale = alle_signale()
    signale[ZIEL_SIG] = {"abs": [0.9, 0.8, 0.7, 0.6, 0.5], "typen": (1,), "df": DF}
    return signale


def cli_lauf(
    monkeypatch: pytest.MonkeyPatch,
    signale: dict[tuple[str, str], dict[str, object]],
    argv: list[str],
    **kw: object,
) -> int:
    installiere_fake_win32(monkeypatch, daten_datei(Protokoll(), signale, **kw))  # type: ignore[arg-type]
    return daten_lesen.cli(argv)


def test_signal_option_waehlt_aus_und_amplitude_rueckfall(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    ziel = tmp_path / "g.csv"
    argv = [
        "k.svd",
        str(ziel),
        "--signal",
        "Vib Y | Geschwindigkeit",
        "--signal",
        "Ref1 & Ref2|Kohärenz",
    ]
    assert cli_lauf(monkeypatch, v2_signale(), argv) == 0
    zeilen = lies_csv(ziel)
    assert zeilen[0] == [
        "f_Hz",
        "Vib Y | Geschwindigkeit | Re",
        "Vib Y | Geschwindigkeit | Im",
        "Ref1 & Ref2 | Kohärenz | Abs",
    ]
    assert [float(z[3]) for z in zeilen[1:]] == [0.9, 0.8, 0.7, 0.6, 0.5]


def test_auswahl_datei_mit_kommentaren(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    datei = tmp_path / "auswahl.txt"
    datei.write_text(
        "# v2\n\nVib X | Geschwindigkeit\n   # eingerückter Kommentar\nRef1 & Ref2 | Kohärenz\n",
        encoding="utf-8",
    )
    ziel = tmp_path / "g.csv"
    code = cli_lauf(monkeypatch, v2_signale(), ["k.svd", str(ziel), "--auswahl", str(datei)])
    assert code == 0
    assert len(lies_csv(ziel)[0]) == 1 + 2 + 1


def test_auswahl_und_signal_werden_kombiniert(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    datei = tmp_path / "a.txt"
    datei.write_text("Vib X | Geschwindigkeit\n", encoding="utf-8")
    ziel = tmp_path / "g.csv"
    argv = ["k.svd", str(ziel), "--auswahl", str(datei), "--signal", "Vib Y|Geschwindigkeit"]
    assert cli_lauf(monkeypatch, v2_signale(), argv) == 0
    assert len(lies_csv(ziel)[0]) == 1 + 4


@pytest.mark.parametrize(
    "argv_extra",
    [
        ["--signal", "ohne_trenner"],
        ["--signal", "Kanal | "],
        ["--signal", "A|B", "--signal", "A | B"],
        ["--auswahl", "gibt_es_nicht.txt"],
    ],
)
def test_ungueltige_auswahl_exit_2(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path, argv_extra: list[str]
) -> None:
    log = Protokoll()
    installiere_fake_win32(monkeypatch, daten_datei(log, alle_signale()))
    assert daten_lesen.cli(["k.svd", str(tmp_path / "g.csv"), *argv_extra]) == 2
    assert not log.pfade  # nichts geöffnet


def test_auswahl_datei_fehlerzeile_und_leere_auswahl(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    schlecht = tmp_path / "s.txt"
    schlecht.write_text("# ok\nkaputt\n", encoding="utf-8")
    leer = tmp_path / "l.txt"
    leer.write_text("# nur Kommentar\n", encoding="utf-8")
    installiere_fake_win32(monkeypatch, daten_datei(Protokoll(), alle_signale()))
    ziel = str(tmp_path / "g.csv")
    assert daten_lesen.cli(["k.svd", ziel, "--auswahl", str(schlecht)]) == 2
    assert "Zeile 2" in capsys.readouterr().out
    assert daten_lesen.cli(["k.svd", ziel, "--auswahl", str(leer)]) == 2
    assert "leer" in capsys.readouterr().out


def test_domaene_gefunden(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    terz = {("Vib X", "Terz"): {"abs": [1.0, 2.0], "typen": (1,), "df": 2.0}}
    ziel = tmp_path / "g.csv"
    argv = ["k.svd", str(ziel), "--domaene", "Terzen", "--signal", "Vib X | Terz"]
    assert cli_lauf(monkeypatch, alle_signale(), argv, weitere={"Terzen": terz}) == 0
    zeilen = lies_csv(ziel)
    assert zeilen[0] == ["f_Hz", "Vib X | Terz | Abs"]
    assert [float(z[0]) for z in zeilen[1:]] == [0.0, 2.0]


def test_domaene_nicht_gefunden_exit_2(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    log = Protokoll()
    installiere_fake_win32(monkeypatch, daten_datei(log, alle_signale(), weitere={"Terzen": {}}))
    ziel = tmp_path / "g.csv"
    assert daten_lesen.cli(["k.svd", str(ziel), "--domaene", "PSD"]) == 2
    ausgabe = capsys.readouterr().out
    assert "Domäne 'PSD' nicht gefunden. Vorhanden: FFT, Terzen" in ausgabe
    assert not ziel.exists()
    assert log.geschlossen


def test_domaene_name_nicht_lesbar_wird_uebersprungen(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    log = Protokoll()
    pf = daten_datei(log, alle_signale())
    erste = pf.GetPointDomains().Item(1)
    object.__setattr__(erste, "_fehler", {"Name": OSError("weg")})
    installiere_fake_win32(monkeypatch, pf)
    assert daten_lesen.waehle_domaene(pf, "X") is None
    assert "(nicht lesbar: OSError)" in capsys.readouterr().out
    assert daten_lesen.waehle_domaene(pf, None) is erste
    assert "(nicht lesbar: OSError)" in capsys.readouterr().out


def test_domaene_explizit_fft_ohne_warnung_standard_mit(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    argv = ["k.svd", str(tmp_path / "g.csv"), "--domaene", "Zeit"]
    assert cli_lauf(monkeypatch, alle_signale(), argv, domaenenname="Zeit") == 0
    assert "WARNUNG" not in capsys.readouterr().out  # ausdrücklich gewählt


def test_amplitude_schalter_erzwingt_abs(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    signale = alle_signale()
    signale[("Ref1", "Kraft")] = {"re": RE, "im": IM, "abs": [9.0] * N, "typen": (7, 8, 1)}
    ziel = tmp_path / "g.csv"
    argv = ["k.svd", str(ziel), "--signal", "Ref1|Kraft", "--amplitude"]
    assert cli_lauf(monkeypatch, signale, argv) == 0
    zeilen = lies_csv(ziel)
    assert zeilen[0] == ["f_Hz", "Ref1 | Kraft | Abs"]
    assert [float(z[1]) for z in zeilen[1:]] == [9.0] * N


def test_amplitude_schalter_ohne_typ1_fehlt(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    argv = ["k.svd", str(tmp_path / "g.csv"), "--signal", "Vib X|Geschwindigkeit", "--amplitude"]
    assert cli_lauf(monkeypatch, alle_signale(), argv) == 1  # einziges Signal fehlt


def test_kein_rueckfall_wenn_nur_imag_vorhanden(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    signale = {("A", "S"): {"im": IM, "abs": RE, "typen": (8, 1), "df": DF}}
    ziel = tmp_path / "g.csv"
    assert cli_lauf(monkeypatch, signale, ["k.svd", str(ziel), "--signal", "A|S"]) == 1


def test_amplitude_laenge_abweichend_meldet_fehlend(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    signale = v2_signale()
    signale[("X", "Leer")] = {"abs": [], "typen": (1,)}
    ziel = tmp_path / "g.csv"
    argv = ["k.svd", str(ziel), "--signal", "Ref1 & Ref2|Kohärenz", "--signal", "X|Leer"]
    assert cli_lauf(monkeypatch, signale, argv) == 3
    assert "X | Leer\tValueError: keine Werte" in (tmp_path / "g.csv.fehlend.txt").read_text(
        encoding="utf-8"
    )


def test_liste_gibt_alles_aus_und_schreibt_nichts(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    log = Protokoll()
    installiere_fake_win32(monkeypatch, daten_datei(log, v2_signale(), weitere={"Terzen": {}}))
    assert daten_lesen.cli(["k.svd", "--liste"]) == 0
    ausgabe = capsys.readouterr().out
    assert "Domänen: 1: FFT; 2: Terzen" in ausgabe
    assert "Kanal 1: Vib X" in ausgabe
    assert "  Signal 1: Geschwindigkeit  [Typ 7 Display7; Typ 8 Display8]" in ausgabe
    assert "Kanal 9: Ref1 & Ref2" in ausgabe
    assert "Signal 1: Kohärenz  [Typ 1 Display1]" in ausgabe
    assert log.geschlossen
    assert log.zuweisungen == [("ReadOnly", True, False)]
    assert list(tmp_path.iterdir()) == []


def test_liste_domaene_nicht_gefunden_und_gefunden(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    terz = {("K", "T"): {"abs": [1.0], "typen": (1,)}}
    installiere_fake_win32(monkeypatch, daten_datei(Protokoll(), {}, weitere={"Terzen": terz}))
    assert daten_lesen.cli(["k.svd", "--liste", "--domaene", "Nein"]) == 2
    assert "nicht gefunden" in capsys.readouterr().out
    assert daten_lesen.cli(["k.svd", "--liste", "--domaene", "Terzen"]) == 0
    assert "Signal 1: T  [Typ 1 Display1]" in capsys.readouterr().out


def test_liste_nicht_lesbare_namen_und_typen(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    log = Protokoll()
    pf = daten_datei(log, {("K", "S"): {"re": RE, "im": IM}})
    dom = pf.GetPointDomains().Item(1)
    signal = dom.Channels.Item(1).Signals.Item(1)
    disp = signal.Displays.Item(1)
    object.__setattr__(signal, "_fehler", {"Name": OSError("x")})
    object.__setattr__(disp, "_fehler", {"Type": OSError("y")})
    installiere_fake_win32(monkeypatch, pf)
    assert daten_lesen.liste("k.svd") == 0
    ausgabe = capsys.readouterr().out
    assert "Signal 1: (nicht lesbar: OSError)" in ausgabe
    assert "Typ ? (OSError)" in ausgabe


def test_ziel_fehlt_ohne_liste_exit_2(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    installiere_fake_win32(monkeypatch, daten_datei(Protokoll(), alle_signale()))
    assert daten_lesen.cli(["k.svd"]) == 2
    assert "Ziel-CSV fehlt" in capsys.readouterr().out


def test_standard_auswahl_unveraendert(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    ziel = tmp_path / "g.csv"
    assert cli_lauf(monkeypatch, alle_signale(), ["k.svd", str(ziel)]) == 0
    kopf = lies_csv(ziel)[0]
    erwartet = [f"{k} | {s} | {x}" for k, s in daten_lesen.AUSWAHL for x in ("Re", "Im")]
    assert kopf == ["f_Hz", *erwartet]
