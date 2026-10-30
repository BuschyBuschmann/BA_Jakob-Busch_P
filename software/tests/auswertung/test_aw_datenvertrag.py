"""Datenvertrag FG-02 6.1/6.3, Annahmen M1–M11 (A2), Toleranzen (Abschnitt 8), Gesamtauswertung."""

from __future__ import annotations

import math

import aw_referenz as ref
import numpy as np
import pytest

from ldv_automation.auswertung import (
    ANNAHME,
    Annahmen,
    Messdaten,
    Punkte,
    Schwellen,
    Toleranzen,
    bereite_paar,
    werte_aus,
)
from ldv_automation.auswertung.annahmen import ANNAHME_NUMMERN
from ldv_automation.auswertung.daten import cph_aus_cp, einheit_quotient
from ldv_automation.auswertung.gesamt import hoechste_spitze
from ldv_automation.auswertung.spektren import spektren_kanal
from ldv_automation.auswertung.spitzen import Spitzenergebnis

F = np.array([1.5625, 3.125, 4.6875])


def _punkte(p: int = 1) -> Punkte:
    return Punkte(
        index=np.arange(p, dtype=np.int64),
        label=np.arange(p, dtype=np.int64),
        koordinaten_m=np.zeros((p, 3)),
    )


# --- Annahmen -------------------------------------------------------------------------


def test_voreinstellungen_nach_fg02() -> None:
    a = Annahmen()
    assert (a.k0, a.konjugieren, a.w_rbw, a.n_d, a.bandregel) == (1, False, 1.0, 7, "geschlossen")
    assert a.vorzeichen("Ref1") == 1 and a.m7_grenze_hz == 1000.0
    assert a.gueltig_je_punkt(3).tolist() == [True, True, True]
    eintraege = a.eintraege()
    assert {e.nr for e in eintraege} == set(ANNAHME_NUMMERN)
    assert all(e.status == ANNAHME and e.ist_annahme for e in eintraege)
    s = Schwellen()
    assert (s.kohaerenz_min, s.prominenz_min, s.fenster_linien, s.n_min_linien, s.k_eps) == (
        0.9,
        2.0,
        20,
        3.0,
        2.0,
    )
    assert s.nachbar_faktor == 3.0 and s.p07_min_spitzen == 10


def test_annahmen_status_und_werte_im_text() -> None:
    a = Annahmen(
        vorzeichen_kanal={"Ref2": -1},
        n_d=[7, 25],
        gueltig=[True, False],
        m7_grenze_hz=None,
        status={"M1": "bestätigt am 2026-11-02"},
    )
    texte = {(e.nr, e.parameter): e for e in a.eintraege()}
    assert texte[("M1", "konjugieren")].status == "bestätigt am 2026-11-02"
    assert not texte[("M1", "konjugieren")].ist_annahme
    assert texte[("M8", "vorzeichen_kanal")].wert == "Ref2: -1; übrige +1"
    assert texte[("M5", "n_d")].wert == "je Punkt 7 … 25"
    assert texte[("M6", "gueltig")].wert == "1 von 2 ungültig"
    assert texte[("M7", "m7_grenze_hz")].wert == "aus"
    assert a.n_d_je_punkt(2).tolist() == [7, 25]
    with pytest.raises(ValueError, match="P"):
        a.n_d_je_punkt(3)
    with pytest.raises(ValueError, match="P"):
        a.gueltig_je_punkt(3)
    with pytest.raises(ValueError, match="Annahmennummer"):
        a.status_von("M3")


@pytest.mark.parametrize(
    "kwargs",
    [
        {"k0": -1},
        {"k0": True},
        {"w_rbw": 0.5},
        {"w_rbw": float("nan")},
        {"n_d": 0},
        {"n_d": [7, 0]},
        {"n_d": []},
        {"vorzeichen_kanal": {"Ref1": 2}},
        {"m7_grenze_hz": 0.0},
        {"bandregel": "halboffen"},
        {"status": {"M3": "x"}},
        {"status": {"M1": " "}},
    ],
)
def test_ungueltige_annahmen(kwargs: dict[str, object]) -> None:
    with pytest.raises(ValueError):
        Annahmen(**kwargs)  # type: ignore[arg-type]


@pytest.mark.parametrize(
    "kwargs",
    [
        {"kohaerenz_min": 1.5},
        {"prominenz_min": 0.0},
        {"fenster_linien": 0},
        {"p07_min_spitzen": 0},
        {"gewicht_kohaerenz_max": 1.0},
    ],
)
def test_ungueltige_schwellen(kwargs: dict[str, object]) -> None:
    with pytest.raises(ValueError):
        Schwellen(**kwargs)  # type: ignore[arg-type]


def test_toleranzen_abschnitt_8() -> None:
    t = Toleranzen()
    ref_kurve = np.array([1.0, 2.0, 0.0])
    assert t.kurve_stimmt(ref_kurve * (1 + 9e-6), ref_kurve)
    assert not t.kurve_stimmt(ref_kurve * (1 + 2e-5), ref_kurve)
    assert t.kurve_stimmt(np.array([1.0, 2.0, 1.9e-6]), ref_kurve)  # atol = 1e-6·max
    assert t.spitze_stimmt(100.2, 100.0, 1.0, ())
    assert not t.spitze_stimmt(100.3, 100.0, 1.0, ())
    assert t.spitze_stimmt(100.45, 100.0, 1.0, ("aufloesungsbegrenzt",))
    assert t.spitze_stimmt(100.0, 100.0, 1.0, ("nachbarmode",)) is None
    assert t.breite_stimmt(2.19, 2.0, ()) is True
    assert t.breite_stimmt(2.21, 2.0, ()) is False
    assert t.breite_stimmt(2.0, 2.0, ("aufloesungsbegrenzt",)) is None


# --- Messdaten (6.1) ----------------------------------------------------------------------


def test_messdaten_formen_typen_und_vorzeichen() -> None:
    gut = {"Vib Z": np.ones((1, 3)), "Ref1": np.ones((1, 3))}
    with pytest.raises(TypeError, match="dtype"):
        Messdaten(
            frequenz_hz=F,
            delta_f_hz=1.5625,
            punkte=_punkte(),
            einheiten={"Vib Z": "m/s"},
            ap={"Vib Z": np.ones((1, 3), dtype=np.float32)},
        )
    with pytest.raises(ValueError, match="Form"):
        Messdaten(
            frequenz_hz=F,
            delta_f_hz=1.5625,
            punkte=_punkte(),
            einheiten={"Vib Z": "m/s"},
            ap={"Vib Z": np.ones((2, 3))},
        )
    with pytest.raises(ValueError, match="P-03"):
        Messdaten(
            frequenz_hz=F,
            delta_f_hz=1.5625,
            punkte=_punkte(),
            einheiten={"Vib Z": "m/s"},
            ap={"Vib Z": np.ones((1, 3))},
            betrag={"Vib Z": -np.ones((1, 3))},
        )
    with pytest.raises(ValueError, match="streng steigend"):
        Messdaten(
            frequenz_hz=F[::-1].copy(), delta_f_hz=1.5625, punkte=_punkte(), einheiten={}, ap={}
        )
    with pytest.raises(ValueError, match="K >= 1"):
        Messdaten(frequenz_hz=np.array([]), delta_f_hz=1.0, punkte=_punkte(), einheiten={}, ap={})
    with pytest.raises(ValueError, match="delta_f_hz"):
        Messdaten(frequenz_hz=F, delta_f_hz=0.0, punkte=_punkte(), einheiten={}, ap={})
    with pytest.raises(ValueError, match="Autospektrum"):
        Messdaten(
            frequenz_hz=F,
            delta_f_hz=1.5625,
            punkte=_punkte(),
            einheiten={"Vib Z": "m/s"},
            ap={"Vib Z": np.ones((1, 3))},
            cp={("Vib Z", "Ref1"): np.ones((1, 3), dtype=np.complex128)},
        )
    with pytest.raises(ValueError, match="Einheit"):
        Messdaten(
            frequenz_hz=F, delta_f_hz=1.5625, punkte=_punkte(), einheiten={"Vib Z": "m/s"}, ap=gut
        )
    with pytest.raises(TypeError, match="cph"):
        Messdaten(
            frequenz_hz=F,
            delta_f_hz=1.5625,
            punkte=_punkte(),
            einheiten={"Vib Z": "m/s", "Ref1": "N"},
            ap=gut,
            cph={("Vib Z", "Ref1"): np.ones((1, 3))},  # type: ignore[dict-item]
        )
    d = Messdaten(
        frequenz_hz=F,
        delta_f_hz=1.5625,
        punkte=_punkte(),
        einheiten={"Vib Z": "m/s", "Ref1": "N"},
        ap=gut,
    )
    assert (d.anzahl_punkte, d.anzahl_linien) == (1, 3)


def test_punkte_formen() -> None:
    with pytest.raises(ValueError, match="Punkte"):
        Punkte(index=np.arange(2), label=np.arange(3), koordinaten_m=np.zeros((2, 3)))
    with pytest.raises(TypeError, match="float64"):
        Punkte(index=np.arange(2), label=np.arange(2), koordinaten_m=np.zeros((2, 3), np.float32))


def test_bereite_paar_und_cph_ersatz() -> None:
    daten = ref.erwartungswert_paar(0.8 + 0.3j, 1.0, 0.0, 0.0)
    with pytest.raises(KeyError):
        bereite_paar(daten, "Ref1", "Vib Z")
    paar = bereite_paar(
        daten, "Vib Z", "Ref1", Annahmen(vorzeichen_kanal={"Ref1": -1}, konjugieren=True)
    )
    np.testing.assert_allclose(paar.cp, -np.conj(daten.cp[("Vib Z", "Ref1")]), rtol=0)
    assert paar.cph_berechnet and paar.bezeichnung == "Vib Z/Ref1"
    cph = cph_aus_cp(np.array([[1.0 + 1j, 2.0 + 0j]]), np.array([[4.0, 0.0]]))
    assert cph[0, 0] == 0.5 + 0.5j and np.isnan(cph[0, 1].real)


def test_einheit_quotient() -> None:
    assert einheit_quotient("m/s", "N") == "(m/s)/N"
    assert einheit_quotient("m/s²", "N") == "(m/s²)/N"
    assert einheit_quotient("m/s", "m/s²") == "(m/s)/(m/s²)"
    assert einheit_quotient("N", "N") == "N/N"


def test_spektren_ohne_referenz_nur_leistung() -> None:
    daten = ref.messdaten(frequenz_hz=F, ap={"Vib Z": np.full((1, 3), 4.0)}, phase_gueltig=False)
    sp = spektren_kanal(daten, "Vib Z")
    assert sp.spektrum_kohaerent is None and sp.referenz is None
    np.testing.assert_allclose(sp.spektrum_leistung, 2.0, rtol=0)


# --- Gesamtauswertung ---------------------------------------------------------------------


def _messung_zwei_moden(p: int = 3) -> Messdaten:
    f = (np.arange(1, 801) * 0.5).astype(np.float64)
    y = ref.mobilitaet_moden(f, [100.0, 150.0, 260.0])
    skala = np.linspace(1.0, 2.0, p)[:, None]
    h = skala * y[None, :]
    ap_b = np.ones((p, f.size))
    ap_a = np.abs(h) ** 2 * 1.0 + 1e-12
    cp = h.astype(np.complex128)
    akz = 1j * 2 * np.pi * f * y  # Ref2/Ref1 als Akzeleranz eines Antriebspunkts
    return ref.messdaten(
        frequenz_hz=f,
        ap={"Vib Z": ap_a, "Ref1": ap_b, "Ref2": np.abs(akz[None, :] * np.ones((p, 1))) ** 2},
        betrag={"Ref1": np.ones((p, f.size))},
        cp={
            ("Vib Z", "Ref1"): cp,
            ("Ref2", "Ref1"): (akz[None, :] * np.ones((p, 1))).astype(np.complex128),
        },
        cph={("Vib Z", "Ref1"): (cp / np.sqrt(ap_b)).astype(np.complex128)},
        delta_f_hz=0.5,
    )


def test_werte_aus_gesamt() -> None:
    daten = _messung_zwei_moden()
    a = werte_aus(
        daten,
        antriebspunkt=("Ref2", "Ref1", "akzeleranz"),
        baender=[(90.0, 110.0)],
    )
    assert set(a.paare) == {("Vib Z", "Ref1"), ("Ref2", "Ref1")}
    pa = a.paare[("Vib Z", "Ref1")]
    f_sp = [s.f_sp_hz for s in pa.spitzen.spitzen]
    assert len(f_sp) == 3 and abs(f_sp[0] - 100.0) < 0.5 and abs(f_sp[2] - 260.0) < 0.5
    assert hoechste_spitze(pa.spitzen) is not None
    assert pa.mittel_h1.n_mittel.tolist()[0] == 3
    ids = [e.id for e in a.pruefungen]
    assert ids == sorted(ids) and ids[-1] == "P-11"
    p08 = next(e for e in a.pruefungen if e.id == "P-08")
    assert p08.status == "ok" and p08.wert == 1.0
    assert a.schwingform is None
    with pytest.raises(ValueError, match="Komponenten"):  # nur Z-Komponente vorhanden
        werte_aus(daten, f_schwingform_hz=150.2)
    assert "Ref2" not in a.kanaele and "Vib Z" not in a.kanaele and "Ref1" not in a.kanaele
    bezuege = {b.bezug for b in a.baender}
    assert "|H1| Vib Z/Ref1 Betragsmittel" in bezuege and "AP Ref1 Punktmittel" in bezuege
    assert all(b.n_linien == 41 for b in a.baender)
    assert a.annahmen_liste == Annahmen().eintraege()


def test_werte_aus_ohne_antriebspunkt_und_falsches_paar() -> None:
    daten = _messung_zwei_moden(2)
    a = werte_aus(daten)
    p08 = next(e for e in a.pruefungen if e.id == "P-08")
    assert p08.status == "nicht_pruefbar" and "konfiguriert" in p08.grund
    assert a.schwingform is None and a.baender == ()
    with pytest.raises(ValueError, match="Antriebspunkt"):
        werte_aus(daten, antriebspunkt=("Vib X", "Ref1", "mobilitaet"))


def test_hoechste_spitze_leer() -> None:
    leer = Spitzenergebnis(
        spitzen=(), groesse="", einheit="", delta_f_hz=1.0, hinweise=(), grenzen=(), annahmen=()
    )
    assert hoechste_spitze(leer) is None


def test_ungueltige_punkte_gehen_nicht_ins_mittel() -> None:
    daten = _messung_zwei_moden(3)
    a = werte_aus(daten, annahmen=Annahmen(gueltig=(True, False, True)))
    pa = a.paare[("Vib Z", "Ref1")]
    assert pa.mittel_h1.n_mittel[0] == 2
    assert pa.mittel_h1.mittel_betrag is not None
    h = pa.frf.h1
    assert pa.mittel_h1.mittel_betrag[10] == pytest.approx(
        (abs(h[0, 10]) + abs(h[2, 10])) / 2, rel=1e-14
    )
    p10 = next(e for e in a.pruefungen if e.id == "P-10")
    assert p10.wert == 1.0
    assert not math.isnan(pa.mittel_h1.mittel_betrag[0])
