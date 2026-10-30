"""Export (FG-02 Abschnitt 5, B-7), Anbindung an den W2-Leser (A6), Abbildungen (B-6)
und Beispielskript, mit einem synthetischen Ersatz für das Leserergebnis."""

from __future__ import annotations

import datetime as dt
import json
from pathlib import Path

import abbildungen
import aw_referenz as ref
import beispiel_svd
import numpy as np
import pytest

from ldv_automation.auswertung import Annahmen, werte_aus
from ldv_automation.auswertung.export import (
    FORMAT,
    _json_wert,
    _Sammler,
    exportiere,
    lese_export,
    paar_schluessel,
    sha256_datei,
)
from ldv_automation.auswertung.svd_adapter import aus_svd_messung
from ldv_automation.protokoll.version import BuildInfo

BUILD = BuildInfo(paket_version="0.1.0", git_hash="a" * 40, git_dirty=False, quelle="git")
JETZT = dt.datetime(2026, 10, 29, 12, 0, tzinfo=dt.UTC)


@pytest.fixture
def messdatei(tmp_path: Path) -> Path:
    pfad = tmp_path / "synthetisch.svd"
    pfad.write_bytes(b"Platzhalter der Messdatei")
    return pfad


def test_adapter_bildet_datenvertrag(messdatei: Path) -> None:
    daten = aus_svd_messung(ref.fake_svd_messung(messdatei))
    assert set(daten.cp) == {
        ("Vib X", "Ref1"),
        ("Vib Y", "Ref1"),
        ("Vib Z", "Ref1"),
        ("Ref2", "Ref1"),
    }
    assert set(daten.cph) == {("Vib X", "Ref1"), ("Vib Y", "Ref1"), ("Vib Z", "Ref1")}
    assert set(daten.ap) == {"Vib X", "Vib Y", "Vib Z", "Ref1", "Ref2"}
    assert set(daten.betrag) == {"Ref1"}
    assert daten.ap["Vib X"].dtype == np.float64  # float32 an der Grenze gewandelt
    assert daten.einheiten["Ref2"] == "m/s²" and daten.einheiten["Ref1"] == "N"
    assert daten.phase_gueltig and daten.delta_f_hz == 0.5
    assert daten.herkunft is not None and daten.herkunft.sha256 == sha256_datei(messdatei)
    assert daten.punkte.label[0] == 132


def test_adapter_fehlerfaelle(messdatei: Path) -> None:
    m = ref.fake_svd_messung(messdatei)
    m.signale["X"] = ref.FakeSignal("X", "FRF", ("Vib Z", "Ref1"), np.zeros((4, 800)))
    with pytest.raises(ValueError, match="Signalart"):
        aus_svd_messung(m, sha256="0")
    m = ref.fake_svd_messung(messdatei)
    m.signale["X"] = ref.FakeSignal("X", "CP", ("Vib Z",), np.zeros((4, 800), complex))
    with pytest.raises(ValueError, match="zwei Kanäle"):
        aus_svd_messung(m, sha256="0")
    m = ref.fake_svd_messung(messdatei)
    m.signale["X"] = ref.FakeSignal("X", "AP", ("Vib Z", "Ref1"), np.zeros((4, 800)))
    with pytest.raises(ValueError, match="einen Kanal"):
        aus_svd_messung(m, sha256="0")
    m = ref.fake_svd_messung(messdatei)
    m.signale["X"] = ref.FakeSignal("X", "AP", ("Vib Z",), np.zeros((4, 800)))
    with pytest.raises(ValueError, match="doppelt"):
        aus_svd_messung(m, sha256="0")
    m = ref.fake_svd_messung(messdatei)
    m.baender["S99"] = ref.FakeBand((("Ref1", "Kraft", "kN"),))
    with pytest.raises(ValueError, match="widersprüchliche"):
        aus_svd_messung(m, sha256="0")
    m = ref.fake_svd_messung(messdatei)
    m.baender.clear()
    with pytest.raises(ValueError, match="Einheit fehlt"):
        aus_svd_messung(m, sha256="0")
    daten = aus_svd_messung(m, sha256="0", einheiten=dict.fromkeys(ref.EINHEITEN_DATEI, "x"))
    assert daten.einheiten["Ref1"] == "x"


def test_export_pflichtinhalt_und_rundreise(messdatei: Path, tmp_path: Path) -> None:
    daten = aus_svd_messung(ref.fake_svd_messung(messdatei))
    a = werte_aus(
        daten,
        annahmen=Annahmen(vorzeichen_kanal={"Ref1": -1}),
        antriebspunkt=("Ref2", "Ref1", "akzeleranz"),
        baender=[(90.0, 110.0)],
        f_schwingform_hz=150.0,
    )
    basis = tmp_path / "export"
    npz, js = exportiere(a, basis, build_info=BUILD, jetzt=lambda: JETZT)
    felder, meta = lese_export(basis)
    assert meta["format"] == FORMAT and meta["npz_datei"] == npz.name
    k = meta["konventionen"]
    assert k["zeitkonvention"] == "exp(+i*omega*t)"
    assert k["kreuzspektrum"] == "CP_ab = <A B*>, a = Antwort, b = Referenz"
    assert (k["k0"], k["k0_status"], k["w_rbw"], k["n_d"], k["delta_f_hz"]) == (
        1,
        "Annahme",
        1.0,
        7,
        0.5,
    )
    assert meta["herkunft"]["messdatei_sha256"] == sha256_datei(messdatei)
    assert meta["herkunft"]["software"]["git_hash"] == "a" * 40
    assert meta["herkunft"]["erstellt"] == "2026-10-29T12:00:00+00:00"
    assert {e["nr"] for e in meta["annahmen"]} >= {"M1", "M2", "M5", "M6", "M7", "M8", "M10"}
    # 1./2.: Achse, Linienindex, Punkte
    np.testing.assert_array_equal(felder["frequenz_hz"], daten.frequenz_hz)
    assert felder["linienindex"][0] == 0 and felder["punkte.label"][0] == 132
    assert felder["punkte.gueltig"].all()
    # 3.: Rohgrößen ohne s_b, float64 Real/Imag ohne Rundung
    s = paar_schluessel("Vib Z", "Ref1")
    roh = felder[f"roh.cp.{s}.re"] + 1j * felder[f"roh.cp.{s}.im"]
    np.testing.assert_array_equal(roh, daten.cp[("Vib Z", "Ref1")])
    assert felder[f"roh.cp.{s}.re"].dtype == np.float64
    assert meta["felder"][f"roh.cp.{s}.re"]["angewandt"].startswith("roh")
    np.testing.assert_array_equal(felder["roh.ap.Vib_Z"], daten.ap["Vib Z"])
    np.testing.assert_array_equal(felder["roh.abs.Ref1"], daten.betrag["Ref1"])
    assert f"roh.cph.{s}.im" in felder
    # 4.: abgeleitete Größen mit s_b = -1
    h1 = felder[f"abgeleitet.{s}.h1.re"] + 1j * felder[f"abgeleitet.{s}.h1.im"]
    np.testing.assert_array_equal(h1, a.paare[("Vib Z", "Ref1")].frf.h1)
    h1_roh = daten.cp[("Vib Z", "Ref1")] / daten.ap["Ref1"]
    np.testing.assert_allclose(h1, -h1_roh, rtol=1e-15)
    assert meta["felder"][f"abgeleitet.{s}.h1.re"]["angewandt"] == (
        "s_a = +1, s_b = -1, konjugieren = False"
    )
    assert meta["felder"][f"abgeleitet.{s}.h1.re"]["einheit"] == "(m/s)/N"
    assert meta["felder"][f"abgeleitet.{s}.spektrum_leistung"]["skalierung"].startswith("Spitze")
    # Prüfungen, Spitzen, Bänder, Schwingform
    assert [e["id"] for e in meta["pruefungen"]][-1] == "P-11"
    assert meta["paare"][s]["spitzen"]["spitzen"]
    assert meta["baender"][0]["n_linien"] == 41
    assert meta["schwingform"]["f_hz"] == 150.0 and "schwingform.amplitude.re" in felder
    # Text ist striktes JSON (kein NaN)
    json.loads(js.read_text(encoding="utf-8"), parse_constant=_kein_nan)


def _kein_nan(wert: str) -> None:
    raise AssertionError(f"nicht-standardkonformer JSON-Wert {wert}")


def test_export_ueberschreibt_nicht_und_prueft_ordner_und_pruefsumme(
    messdatei: Path, tmp_path: Path
) -> None:
    a = werte_aus(aus_svd_messung(ref.fake_svd_messung(messdatei, p=2)))
    basis = tmp_path / "e"
    exportiere(a, basis, build_info=BUILD)
    with pytest.raises(FileExistsError):
        exportiere(a, basis, build_info=BUILD)
    exportiere(a, basis, build_info=BUILD, ueberschreiben=True)
    with pytest.raises(FileNotFoundError):
        exportiere(a, tmp_path / "fehlt" / "e", build_info=BUILD)
    npz = basis.with_name("e.npz")
    npz.write_bytes(npz.read_bytes() + b"x")
    with pytest.raises(ValueError, match="SHA-256"):
        lese_export(basis)
    with pytest.raises(abbildungen.ExportFehler, match="SHA-256"):
        abbildungen.lese(basis)
    js = basis.with_name("e.json")
    js.write_text(json.dumps({"format": "anders"}), encoding="utf-8")
    with pytest.raises(ValueError, match="kein Export"):
        lese_export(basis)
    with pytest.raises(abbildungen.ExportFehler, match="kein"):
        abbildungen.lese(basis)


def test_export_ohne_herkunft_und_ohne_phase(tmp_path: Path) -> None:
    daten = ref.messdaten(
        frequenz_hz=np.arange(1.0, 6.0),
        ap={"Vib X": np.ones((2, 5)), "Vib Y": np.ones((2, 5)), "Vib Z": np.ones((2, 5))},
        phase_gueltig=False,
    )
    a = werte_aus(daten, f_schwingform_hz=3.0)
    _, js = exportiere(a, tmp_path / "o", build_info=BUILD)
    meta = json.loads(js.read_text(encoding="utf-8"))
    assert meta["herkunft"]["messdatei"] is None
    assert meta["schwingform"]["phase_gueltig"] is False
    assert meta["paare"] == {}
    pfade = abbildungen.erzeuge(tmp_path / "o", tmp_path / "abb")
    assert [p.name for p in pfade] == ["schwingform.pdf", "schwingform.png"]


def test_abbildungen_aus_export(messdatei: Path, tmp_path: Path) -> None:
    a = werte_aus(
        aus_svd_messung(ref.fake_svd_messung(messdatei)),
        annahmen=Annahmen(gueltig=(True, True, False, True)),
        f_schwingform_hz=100.0,
    )
    basis = tmp_path / "x"
    exportiere(
        a,
        basis,
        build_info=BuildInfo(paket_version="0", git_hash="b" * 40, git_dirty=True, quelle="git"),
    )
    pfade = abbildungen.erzeuge(basis, tmp_path / "abb", ["Vib_Z__Ref1"])
    assert sorted(p.name for p in pfade) == sorted(
        f"{n}.{e}"
        for n in ("frf_Vib_Z__Ref1", "spektren_Vib_Z__Ref1", "schwingform")
        for e in ("pdf", "png")
    )
    assert all(p.stat().st_size > 1000 for p in pfade)
    _, meta = abbildungen.lese(basis)
    zeile = abbildungen.fusszeile(meta)
    assert "bbbbbbbbbb+Änderungen" in zeile and "Annahmen offen: M1, M2" in zeile
    assert abbildungen.SKRIPT in zeile
    with pytest.raises(abbildungen.ExportFehler, match="Paare"):
        abbildungen.erzeuge(basis, tmp_path / "abb", ["gibt_es_nicht"])
    assert abbildungen.main([str(basis), str(tmp_path / "abb2"), "--paar", "Ref2__Ref1"]) == 0
    assert abbildungen.main([str(tmp_path / "fehlt"), str(tmp_path / "abb3")]) == 2


def test_beispielskript_mit_ersatzleser(
    messdatei: Path, tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    def leser(pfad: Path) -> ref.FakeSvdMessung:
        return ref.fake_svd_messung(pfad)

    argv = [
        str(messdatei),
        "--export",
        str(tmp_path / "ex"),
        "--abbildungen",
        str(tmp_path / "abb"),
    ]
    assert beispiel_svd.main(argv, leser=leser) == 0
    aus = capsys.readouterr().out
    assert "vorbehaltlich der Annahmen M1–M11" in aus
    assert "P-08 [Ref2/Ref1 (akzeleranz)]: ok" in aus
    assert "Spitzen Betragsmittel |H1| Vib Z/Ref1" in aus and "Schwingform bei 100 Hz" in aus
    assert (tmp_path / "ex" / "synthetisch.npz").is_file()
    assert (tmp_path / "abb" / "schwingform.png").is_file()
    # zweiter Lauf ohne --ueberschreiben: Fehler 2
    assert beispiel_svd.main(argv, leser=leser) == 2
    assert (
        beispiel_svd.main(
            [
                *argv,
                "--ueberschreiben",
                "--ohne-antriebspunkt",
                "--f-schwingform",
                "150",
                "--name",
                "b",
            ],
            leser=leser,
        )
        == 0
    )
    assert "P-08: nicht_pruefbar" in capsys.readouterr().out
    assert beispiel_svd.main([str(tmp_path / "fehlt.svd"), "--export", str(tmp_path)]) == 2


def test_beispielskript_erkennt_veraenderte_datei(messdatei: Path, tmp_path: Path) -> None:
    def veraendernder_leser(pfad: Path) -> ref.FakeSvdMessung:
        m = ref.fake_svd_messung(pfad)
        pfad.write_bytes(b"veraendert")  # simuliert eine Veränderung während des Lesens
        return m

    argv = [str(messdatei), "--export", str(tmp_path / "ex")]
    assert beispiel_svd.main(argv, leser=veraendernder_leser) == 3


def test_beispielskript_ohne_paar_vib_z(tmp_path: Path) -> None:
    pfad = tmp_path / "m.svd"
    pfad.write_bytes(b"x")
    m = ref.fake_svd_messung(pfad)
    for name in [n for n, s in m.signale.items() if "Vib Z" in s.kanaele]:
        del m.signale[name]
    a, sha = beispiel_svd.auswerten(pfad, leser=lambda _p: m, antriebspunkt=None)
    assert a.schwingform is None and sha == sha256_datei(pfad)
    assert "Spitzen Betragsmittel" not in beispiel_svd.zusammenfassung(a)


def test_json_wert_und_doppelte_felder() -> None:
    assert _json_wert({"a": (float("inf"), -float("inf"), float("nan"), np.float64(2.0))}) == {
        "a": ["inf", "-inf", None, 2.0]
    }
    sammler = _Sammler()
    sammler.reell("x", np.ones(2, dtype=np.float32))
    assert sammler.felder["x"].dtype == np.float64
    with pytest.raises(ValueError, match="doppelt"):
        sammler.reell("x", np.ones(2))


def test_abbildung_mit_niedriger_kohaerenz_und_kennzeichen(messdatei: Path, tmp_path: Path) -> None:
    m = ref.fake_svd_messung(messdatei, rauschen=1e-4)
    a = werte_aus(aus_svd_messung(m), annahmen=Annahmen(m7_grenze_hz=120.0))
    pa = a.paare[("Vib Z", "Ref1")]
    assert np.any(pa.frf.kohaerenz < 0.9)
    kennzeichen = [s.kennzeichen for s in pa.spitzen.spitzen]
    assert any(kennzeichen) and not all(kennzeichen)
    exportiere(a, tmp_path / "k", build_info=BUILD)
    pfade = abbildungen.erzeuge(tmp_path / "k", tmp_path / "abb", ["Vib_Z__Ref1"])
    assert len(pfade) == 4
