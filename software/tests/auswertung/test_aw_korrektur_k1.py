"""Korrekturpaket K-W5-1: FG-02 nach K1 (K1-1, K1-6 bis K1-8) und Review-Befunde R-W5-1."""

from __future__ import annotations

import json
import math
from pathlib import Path

import aw_referenz as ref
import numpy as np
import pytest

from ldv_automation.auswertung import Annahmen, Messdaten, Toleranzen, werte_aus
from ldv_automation.auswertung.annahmen import SKALIERUNG_SPITZENWERT
from ldv_automation.auswertung.baender import band_amplitude, band_ap, band_frf
from ldv_automation.auswertung.daten import (
    einheit_produkt,
    einheit_quadrat,
    einheit_quotient,
)
from ldv_automation.auswertung.export import exportiere
from ldv_automation.auswertung.plausibilitaet import Antriebsart
from ldv_automation.auswertung.spitzen import (
    KOHAERENZ_NICHT_PRUEFBAR,
    KOHAERENZ_NIEDRIG,
    kandidaten,
    suche_spitzen,
)
from ldv_automation.auswertung.svd_adapter import aus_svd_messung
from ldv_automation.protokoll.version import BuildInfo

BUILD = BuildInfo(paket_version="0.1.0", git_hash="c" * 40, git_dirty=False, quelle="git")
ALLE_IDS = [f"P-{i:02d}" for i in range(1, 12)]


# --- K1-1: Vorzeichen je Kanal -------------------------------------------------------------


@pytest.mark.parametrize("kanal", ["Vib X", "Vib Y", "Vib Z"])
def test_k1_1_vibrometerkomponenten_fest_plus_eins(kanal: str) -> None:
    with pytest.raises(ValueError, match="fest"):
        Annahmen(vorzeichen_kanal={kanal: -1})
    assert Annahmen(vorzeichen_kanal={kanal: 1}).vorzeichen(kanal) == 1


def test_k1_1_gedrehter_ref2_p08_bestaetigt_korrektur(tmp_path: Path) -> None:
    """Ref2 mit umgekehrtem Vorzeichen gemessen: P-08 warnt; s_Ref2 = -1 korrigiert beide
    Rollen (Ref2/Ref1 als Antwort, Vib X/Ref2 als Referenz) und P-08 wird ok."""
    pfad = tmp_path / "m.svd"
    pfad.write_bytes(b"x")
    m = ref.fake_svd_messung(pfad)
    for signal in m.signale.values():
        if signal.art == "CP" and "Ref2" in signal.kanaele:
            signal.werte = -signal.werte
    vib_ref2 = np.asarray(m.signale["M0"].werte)  # Vib X/Ref1 als Kreuzspektrum Vib X/Ref2
    m.signale["X"] = ref.FakeSignal("X", "CP", ("Vib X", "Ref2"), -vib_ref2)
    daten = aus_svd_messung(m)
    antrieb: tuple[str, str, Antriebsart] = ("Ref2", "Ref1", "akzeleranz")
    roh = werte_aus(daten, antriebspunkt=antrieb)
    korr = werte_aus(daten, antriebspunkt=antrieb, annahmen=Annahmen(vorzeichen_kanal={"Ref2": -1}))
    p08 = {
        a: next(e for e in x.pruefungen if e.id == "P-08") for a, x in (("roh", roh), ("k", korr))
    }
    assert p08["roh"].status == "warnung" and p08["roh"].wert == 0.0
    assert p08["k"].status == "ok" and p08["k"].wert == 1.0
    for paar in (("Ref2", "Ref1"), ("Vib X", "Ref2")):
        np.testing.assert_allclose(korr.paare[paar].frf.h1, -roh.paare[paar].frf.h1, rtol=0)
    np.testing.assert_array_equal(
        korr.paare[("Vib X", "Ref1")].frf.h1, roh.paare[("Vib X", "Ref1")].frf.h1
    )


# --- K1-7: Kohärenz vollständig NaN ----------------------------------------------------------


def test_k1_7_kohaerenz_vollstaendig_nan_gibt_hinweis() -> None:
    f = (np.arange(1, 801) * 0.5).astype(np.float64)
    y = np.abs(ref.mobilitaet_moden(f, [100.0, 200.0]))
    g2 = np.ones_like(y)
    g2[150:250] = np.nan  # um 100 Hz
    erg = suche_spitzen(f, y, kohaerenz=g2)
    assert len(erg.spitzen) == 2
    assert all(KOHAERENZ_NIEDRIG not in s.kennzeichen for s in erg.spitzen)
    hinweis = [h for h in erg.hinweise if h.startswith(KOHAERENZ_NICHT_PRUEFBAR)]
    assert len(hinweis) == 1 and "99.99" in hinweis[0] and "200." not in hinweis[0]
    alle_nan = suche_spitzen(f, y, kohaerenz=np.full_like(y, np.nan))
    assert "200." in next(h for h in alle_nan.hinweise if h.startswith(KOHAERENZ_NICHT_PRUEFBAR))
    ohne = suche_spitzen(f, y)
    assert any(h.startswith(KOHAERENZ_NICHT_PRUEFBAR) for h in ohne.hinweise)


# --- K1-8: PSV-Vergleich mit reinem M7-Kennzeichen --------------------------------------------


def test_k1_8_vergleich_bei_nur_m7() -> None:
    t = Toleranzen()
    assert t.spitze_stimmt(1000.2, 1000.0, 1.0, ("gueltigkeit_offen_m7",)) is True
    assert t.spitze_stimmt(1000.3, 1000.0, 1.0, ("gueltigkeit_offen_m7",)) is False
    assert (
        t.spitze_stimmt(1000.45, 1000.0, 1.0, ("aufloesungsbegrenzt", "gueltigkeit_offen_m7"))
        is True
    )
    assert t.spitze_stimmt(1000.0, 1000.0, 1.0, ("gueltigkeit_offen_m7", "nachbarmode")) is None
    assert t.breite_stimmt(2.19, 2.0, ("gueltigkeit_offen_m7",)) is True
    assert t.breite_stimmt(2.0, 2.0, ("gueltigkeit_offen_m7", "ueberlappend")) is None


# --- MAJOR: jede Prüfung erscheint mit Status -------------------------------------------------


def test_major_nur_ap_alle_pruefungen_mit_status_und_grund() -> None:
    daten = ref.messdaten(
        frequenz_hz=np.arange(1.0, 6.0),
        ap={"Vib Z": np.ones((2, 5)), "Ref1": np.ones((2, 5))},
        phase_gueltig=False,
    )
    a = werte_aus(daten)
    ids = [e.id for e in a.pruefungen]
    assert sorted(set(ids)) == ALLE_IDS
    for e in a.pruefungen:
        assert e.status in ("ok", "warnung", "fehler", "hinweis", "nicht_pruefbar")
        assert e.grund
    nach_id = {e.id: e for e in a.pruefungen if e.id != "P-04"}
    for pid in ("P-01", "P-02", "P-05", "P-07", "P-08", "P-09"):
        assert nach_id[pid].status == "nicht_pruefbar", pid
    p04 = [e for e in a.pruefungen if e.id == "P-04"]
    assert {e.bezug for e in p04} == {"Vib Z", "Ref1"}
    assert all(e.status == "nicht_pruefbar" and "kein ABS" in e.grund for e in p04)


def test_major_p02_je_paar_ohne_cph_und_p04_ohne_ap() -> None:
    eins = np.ones((1, 3))
    halb = np.full((1, 3), 0.5, dtype=np.complex128)
    daten = ref.messdaten(
        frequenz_hz=np.arange(1.0, 4.0),
        ap={"Vib Z": eins, "Ref1": eins, "Ref2": eins},
        betrag={"Ref1": eins, "Vib X": eins},
        cp={("Vib Z", "Ref1"): halb, ("Vib Z", "Ref2"): halb},
        cph={("Vib Z", "Ref1"): halb, ("Vib Y", "Ref1"): halb},
    )
    a = werte_aus(daten)
    p02 = {e.bezug: e for e in a.pruefungen if e.id == "P-02"}
    assert p02["Vib Z/Ref1"].status == "ok"
    assert p02["Vib Z/Ref2"].status == "nicht_pruefbar" and "kein CPH" in p02["Vib Z/Ref2"].grund
    assert p02["Vib Y/Ref1"].status == "nicht_pruefbar" and "kein AP" in p02["Vib Y/Ref1"].grund
    p04 = {e.bezug: e for e in a.pruefungen if e.id == "P-04"}
    assert p04["Ref1"].status == "ok"
    assert p04["Vib X"].status == "nicht_pruefbar" and "kein AP" in p04["Vib X"].grund
    assert p04["Ref2"].status == "nicht_pruefbar" and "kein ABS" in p04["Ref2"].grund
    assert sorted({e.id for e in a.pruefungen}) == ALLE_IDS


def test_major_ohne_jedes_spektrum() -> None:
    basis = ref.messdaten(frequenz_hz=np.arange(1.0, 4.0), ap={"Vib Z": np.ones((1, 3))})
    daten = Messdaten(
        frequenz_hz=basis.frequenz_hz,
        delta_f_hz=basis.delta_f_hz,
        punkte=basis.punkte,
        einheiten={},
        ap={},
    )
    a = werte_aus(daten)
    assert sorted({e.id for e in a.pruefungen}) == ALLE_IDS
    p04 = next(e for e in a.pruefungen if e.id == "P-04")
    assert p04.status == "nicht_pruefbar" and "weder AP noch ABS" in p04.grund


# --- MINOR 2: M4 und M11 ----------------------------------------------------------------------


def test_minor2_m11_aus_toleranzen_und_m4_einstellbar() -> None:
    t = Toleranzen(rtol=2e-5, breite_rel=0.2)
    eintraege = {e.parameter: e for e in Annahmen(toleranzen=t).eintraege()}
    assert "rtol 2e-05" in eintraege["toleranzen"].wert and "B ±0.2" in eintraege["toleranzen"].wert
    assert eintraege["skalierung"].wert == SKALIERUNG_SPITZENWERT
    with pytest.raises(ValueError, match="M4"):
        Annahmen(skalierung="Effektivwert")


# --- MINOR 3: Pfad, Bandkennzeichen, Einheitentexte --------------------------------------------


def test_minor3_einheitentexte() -> None:
    assert einheit_quadrat("m/s") == "(m/s)^2"
    assert einheit_quadrat("N") == "N^2"
    assert einheit_quadrat("m/s²") == "(m/s²)^2"
    assert einheit_produkt("m/s", "N") == "(m/s)·N"
    assert einheit_quotient("(m/s)·N", "N") == "((m/s)·N)/N"


def test_minor3_bandkennzeichen() -> None:
    f = np.array([1.0, 2.0])
    amp = band_amplitude(np.ones(2), f, 1.0, 2.0, einheit="m/s").kennzeichen()
    assert amp["rms"]["einheit"] == "m/s" and amp["rms"]["art"].startswith("Effektivwert")
    assert amp["rms_psv"]["art"].startswith("Effektivwert")
    ap = band_ap(np.ones(2), f, 1.0, 2.0, einheit="m/s").kennzeichen()
    assert ap["rms_psv"] == {"art": "quadratischer Mittelwert ΣAP/2 (PSV)", "einheit": "(m/s)^2"}
    assert ap["rms"]["einheit"] == "m/s"
    frf = band_frf(np.ones(2), f, 1.0, 2.0, einheit="(m/s)/N").kennzeichen()
    assert set(frf) == {"bandnorm"} and "kein Effektivwert" in frf["bandnorm"]["art"]


def test_minor3_export_pfad_absolut_und_kennzeichen(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.chdir(tmp_path)
    Path("m.svd").write_bytes(b"x")
    m = ref.fake_svd_messung(Path("m.svd"))
    daten = aus_svd_messung(m)
    assert daten.herkunft is not None and Path(daten.herkunft.pfad).is_absolute()
    a = werte_aus(daten, baender=[(90.0, 110.0)])
    _, js = exportiere(a, tmp_path / "e", build_info=BUILD)
    meta = json.loads(js.read_text(encoding="utf-8"))
    assert Path(meta["herkunft"]["messdatei"]).is_absolute()
    assert all("kennzeichen" in b for b in meta["baender"])
    ap_band = next(b for b in meta["baender"] if b["bezug"] == "AP Ref1 je Punkt")
    assert ap_band["kennzeichen"]["rms_psv"]["einheit"] == "N^2"
    assert meta["felder"]["roh.ap.Vib_Z"]["einheit"] == "(m/s)^2"
    assert meta["felder"]["roh.cp.Vib_Z__Ref1.re"]["einheit"] == "(m/s)·N"
    assert meta["paare"]["Vib_Z__Ref1"]["vorzeichen_antwort"] == 1


# --- MINOR 4: NaN im Prominenzfenster symmetrisch ---------------------------------------------


@pytest.mark.parametrize("seite", ["links", "rechts"])
def test_minor4_nan_im_prominenzfenster_symmetrisch(seite: str) -> None:
    y = np.array([0.2, 0.2, 0.2, 0.5, 2.0, 0.5, 0.2, 0.2, 0.2])
    f = np.arange(1.0, 10.0)
    gespiegelt = y.copy()
    if seite == "links":
        gespiegelt[1] = np.nan
    else:
        gespiegelt[7] = np.nan
    assert kandidaten(gespiegelt, f, prominenz_min=2.0, fenster_linien=3) == [4]
    ganz = y.copy()
    if seite == "links":
        ganz[1:4] = np.nan
    else:
        ganz[5:8] = np.nan
    # ganzes Fenster NaN: die andere Seite entscheidet; Linie neben der Spitze NaN → kein
    # lokales Maximum
    assert kandidaten(ganz, f, prominenz_min=2.0, fenster_linien=3) == []
    weit = y.copy()
    weit[[1, 2] if seite == "links" else [6, 7]] = np.nan
    assert kandidaten(weit, f, prominenz_min=2.0, fenster_linien=3) == [4]


def test_minor4_nan_neben_der_spitze_kein_kandidat() -> None:
    f = np.arange(1.0, 6.0)
    assert kandidaten(
        np.array([np.nan, 1.0, 3.0, 1.0, np.nan]), f, prominenz_min=2.0, fenster_linien=2
    ) == [2]
    assert kandidaten(np.array([0.1, np.nan, 3.0, 1.0, 0.1]), f, prominenz_min=2.0) == []


# --- MINOR 5: Imaginärteil reeller Größen -----------------------------------------------------


def test_minor5_imaginaerteil_von_ap_wird_geprueft(tmp_path: Path) -> None:
    pfad = tmp_path / "m.svd"
    pfad.write_bytes(b"x")
    m = ref.fake_svd_messung(pfad)
    name = next(n for n, s in m.signale.items() if s.art == "AP" and s.kanaele == ("Ref1",))
    m.signale[name].werte = m.signale[name].werte + 0j  # komplex, Imaginärteil 0
    assert aus_svd_messung(m).ap["Ref1"].dtype == np.float64
    m.signale[name].werte = m.signale[name].werte + 1e-3j
    with pytest.raises(ValueError, match="Imaginärteil"):
        aus_svd_messung(m)


# --- NITPICK 6: atomarer Export ---------------------------------------------------------------


def test_nitpick6_export_atomar_ohne_verwaiste_dateien(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    daten = ref.messdaten(frequenz_hz=np.arange(1.0, 4.0), ap={"Vib Z": np.ones((1, 3))})
    a = werte_aus(daten)
    import ldv_automation.auswertung.export as export_modul

    def kaputt(_wert: object) -> object:
        raise OSError("Platte voll")  # Fehler nach dem Schreiben der .npz, vor der .json

    monkeypatch.setattr(export_modul, "_json_wert", kaputt)
    with pytest.raises(OSError, match="Platte voll"):
        exportiere(a, tmp_path / "e", build_info=BUILD)
    assert list(tmp_path.iterdir()) == []


def test_fehlerband_randfaelle_fg02_6_3() -> None:
    """FG-02 6.3: k_ε·ε >= 1 → untere Grenze 0, auch bei |H1| = 0 und ε = +∞; obere Grenze
    bei ε = +∞ wie RF-U7 (γ² = 0) +∞; ε = NaN bleibt NaN ohne Kennzeichen-Wert True."""
    from ldv_automation.auswertung.frf import fehlerband

    u, o, ok = fehlerband(
        np.array([0.0, 1.0, 0.0, 1.0]), np.array([math.inf, math.inf, 0.6, math.nan]), 2.0
    )
    assert u.tolist()[:3] == [0.0, 0.0, 0.0]
    assert o[0] == math.inf and o[1] == math.inf and o[2] == 0.0
    assert math.isnan(u[3]) and math.isnan(o[3])
    assert ok.tolist() == [False, False, False, False]
