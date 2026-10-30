"""Referenzfälle FG-02 9.2, 9.3 und 9.8: H1/H2/γ², Spektren, Zufallsfehler, Maske, Punktmittel.

Eingänge als Erwartungswerte (deterministisch). Toleranzen wie in FG-02 angegeben
(rtol 1e-12 für exakte Werte, rtol 1e-10 für zehnstellig angegebene Sollwerte, rtol 1e-9
für die Fehlerformeln). RF-U5 ist statistisch (Monte-Carlo, fester Seed) mit ±10 %.
"""

from __future__ import annotations

import math

import aw_referenz as ref
import numpy as np
import numpy.typing as npt
import pytest

from ldv_automation.auswertung.annahmen import Annahmen, Schwellen
from ldv_automation.auswertung.daten import bereite_paar
from ldv_automation.auswertung.frf import (
    FEHLERBAND_NICHT_AUSSAGEKRAEFTIG,
    HINWEIS_BAND_NICHT_AUSSAGEKRAEFTIG,
    HINWEIS_ND1,
    HINWEIS_ND_KLEIN,
    begrenze_kohaerenz,
    berechne_frf,
    fehlerband,
    gewicht,
    h1_h2_kohaerenz,
    kohaerenz_maske,
    zufallsfehler,
)
from ldv_automation.auswertung.mittel import punktmittel_arithmetisch, punktmittel_betrag
from ldv_automation.auswertung.plausibilitaet import p05_kohaerenz
from ldv_automation.auswertung.spektren import HINWEIS_CPH_BERECHNET, spektren_paar

H = 0.8 + 0.3j
DF = ref.DF_HZ


def _frf(n_r: float, n_v: float, annahmen: Annahmen | None = None):  # type: ignore[no-untyped-def]
    daten = ref.erwartungswert_paar(H, 1.0, n_r, n_v)
    paar = bereite_paar(daten, "Vib Z", "Ref1", annahmen)
    return paar, berechne_frf(paar)


@pytest.mark.parametrize(
    ("rf", "n_r", "n_v", "h1", "h2", "g2", "rtol"),
    [
        ("RF-H1", 0.0, 0.0, H, H, 1.0, 1e-12),
        (
            "RF-H2",
            0.05,
            0.08,
            0.7619047619 + 0.2857142857j,
            0.8876712329 + 0.3328767123j,
            0.8583186361,
            1e-10,
        ),
        ("RF-H3", 0.0, 0.08, H, 1.1095890411 * H, 0.9012345679, 1e-10),
        ("RF-H4", 0.05, 0.0, 0.9523809524 * H, H, 0.9523809524, 1e-10),
    ],
)
def test_rf_h1_bis_h4(
    rf: str, n_r: float, n_v: float, h1: complex, h2: complex, g2: float, rtol: float
) -> None:
    _, frf = _frf(n_r, n_v)
    np.testing.assert_allclose(frf.h1[0, 0], h1, rtol=rtol, err_msg=rf)
    np.testing.assert_allclose(frf.h2[0, 0], h2, rtol=rtol, err_msg=rf)
    np.testing.assert_allclose(frf.kohaerenz[0, 0], g2, rtol=rtol, err_msg=rf)
    assert frf.einheit == "(m/s)/N"
    assert frf.bezeichnung_h1 == "H1"


def test_rf_h5_kohaerenz_ist_h1_durch_h2_und_phasen_gleich() -> None:
    _, frf = _frf(0.05, 0.08)
    q = frf.h1[0, 0] / frf.h2[0, 0]
    assert abs(q.imag) < 1e-15
    assert q.real == pytest.approx(frf.kohaerenz[0, 0], rel=1e-12)
    assert np.angle(frf.h1[0, 0]) == pytest.approx(np.angle(H), abs=1e-12)
    assert np.angle(frf.h2[0, 0]) == pytest.approx(np.angle(H), abs=1e-12)


def test_rf_h6_spektren_kohaerent_und_leistung() -> None:
    paar, frf = _frf(0.05, 0.08)
    sp = spektren_paar(paar)
    assert sp.cph_berechnet and HINWEIS_CPH_BERECHNET in sp.hinweise
    assert sp.spektrum_kohaerent is not None
    k = abs(sp.spektrum_kohaerent[0, 0])
    lst = sp.spektrum_leistung[0, 0]
    assert k == pytest.approx(0.8338093878, rel=1e-10)
    assert lst == pytest.approx(0.9, rel=1e-10)
    assert k / lst == pytest.approx(0.9264548754, rel=1e-10)
    assert k / lst == pytest.approx(math.sqrt(frf.kohaerenz[0, 0]), rel=1e-12)


def test_rf_h7_randfaelle_ap_b_null_und_cp_null() -> None:
    cp = np.array([[0.5 + 0j, 0.0 + 0j, 0.0 + 0j]])
    ap_a = np.array([[1.0, 1.0, 0.0]])
    ap_b = np.array([[0.0, 1.0, 1.0]])
    h1, h2, g2 = h1_h2_kohaerenz(cp, ap_a, ap_b)
    # AP_b = 0
    assert np.isnan(h1[0, 0].real) and np.isnan(h1[0, 0].imag) and np.isnan(g2[0, 0])
    # CP = 0 bei AP > 0
    assert h1[0, 1] == 0 and np.isnan(h2[0, 1].real) and g2[0, 1] == 0.0
    # AP_a = 0 (und CP = 0)
    assert h1[0, 2] == 0 and np.isnan(h2[0, 2].real) and np.isnan(g2[0, 2])
    eps, _, _ = zufallsfehler(g2, 7)
    assert math.isnan(eps[0, 0]) and eps[0, 1] == math.inf
    w = gewicht(g2, 7)
    assert math.isnan(w[0, 0]) and w[0, 1] == 0.0


def test_rf_h7_negatives_ap_wirft() -> None:
    with pytest.raises(ValueError, match="P-03"):
        ref.erwartungswert_paar(H, 1.0, -2.0, 0.0)


def test_rf_h7_kohaerenz_knapp_ueber_eins_wird_eins_und_gezaehlt() -> None:
    # Konstruiert: |CP|² = AP_a·AP_b·(1 + 5e-6)
    daten = ref.messdaten(
        frequenz_hz=np.array([1.0, 2.0]),
        ap={"Vib Z": np.array([[1.0, 1.0]]), "Ref1": np.array([[1.0, 1.0]])},
        cp={("Vib Z", "Ref1"): np.array([[math.sqrt(1 + 5e-6) + 0j, 0.5 + 0j]])},
    )
    frf = berechne_frf(bereite_paar(daten, "Vib Z", "Ref1"))
    assert frf.kohaerenz[0, 0] == 1.0
    assert frf.anzahl_kohaerenz_begrenzt == 1
    p05 = p05_kohaerenz(frf, Schwellen())
    assert p05.status == "ok" and "1 Werte" in p05.grund


def test_rf_h7_kohaerenz_1_001_ist_fehler_p05() -> None:
    daten = ref.messdaten(
        frequenz_hz=np.array([1.0, 2.0]),
        ap={"Vib Z": np.array([[1.0, 1.0]]), "Ref1": np.array([[1.0, 1.0]])},
        cp={("Vib Z", "Ref1"): np.array([[math.sqrt(1.001) + 0j, 0.5 + 0j]])},
    )
    frf = berechne_frf(bereite_paar(daten, "Vib Z", "Ref1"))
    p05 = p05_kohaerenz(frf, Schwellen())
    assert p05.status == "fehler"
    assert p05.wert == pytest.approx(1.001, rel=1e-12)
    assert frf.kohaerenz[0, 0] == pytest.approx(1.001, rel=1e-12)  # nicht still korrigiert


def test_p05_nicht_pruefbar_ohne_kohaerenz() -> None:
    daten = ref.messdaten(
        frequenz_hz=np.array([1.0, 2.0]),
        ap={"Vib Z": np.zeros((1, 2)), "Ref1": np.zeros((1, 2))},
        cp={("Vib Z", "Ref1"): np.zeros((1, 2), dtype=np.complex128)},
    )
    frf = berechne_frf(bereite_paar(daten, "Vib Z", "Ref1"))
    assert p05_kohaerenz(frf, Schwellen()).status == "nicht_pruefbar"


def _frf_paar(antwort: str, referenz: str, annahmen: Annahmen | None = None):  # type: ignore[no-untyped-def]
    daten = ref.erwartungswert_paar(H, 1.0, 0.05, 0.08, antwort=antwort, referenz=referenz)
    paar = bereite_paar(daten, antwort, referenz, annahmen)
    return paar, berechne_frf(paar)


@pytest.mark.parametrize(
    ("vorzeichen", "faktor"),
    [({"Ref1": -1}, -1.0), ({"Ref2": -1}, -1.0), ({"Ref1": -1, "Ref2": -1}, 1.0)],
    ids=["nur_s_b", "nur_s_a", "s_a_und_s_b"],
)
def test_rf_h8_vorzeichen_je_kanal(vorzeichen: dict[str, int], faktor: float) -> None:
    """RF-H8 (K1-1) mit Eingang RF-H2 am Paar Ref2/Ref1 (Antwort darf ein Vorzeichen haben)."""
    basis_paar, basis = _frf_paar("Ref2", "Ref1")
    paar, frf = _frf_paar("Ref2", "Ref1", Annahmen(vorzeichen_kanal=vorzeichen))
    np.testing.assert_allclose(frf.h1, faktor * basis.h1, rtol=1e-12)
    np.testing.assert_allclose(frf.h2, faktor * basis.h2, rtol=1e-12)
    np.testing.assert_allclose(frf.kohaerenz, basis.kohaerenz, rtol=1e-12)
    np.testing.assert_array_equal(paar.ap_antwort, basis_paar.ap_antwort)
    np.testing.assert_array_equal(paar.ap_referenz, basis_paar.ap_referenz)
    sp, sp0 = spektren_paar(paar), spektren_paar(basis_paar)
    assert sp.spektrum_kohaerent is not None and sp0.spektrum_kohaerent is not None
    np.testing.assert_allclose(sp.spektrum_kohaerent, faktor * sp0.spektrum_kohaerent, rtol=1e-12)
    assert (paar.vorzeichen_antwort, paar.vorzeichen_referenz) == (
        vorzeichen.get("Ref2", 1),
        vorzeichen.get("Ref1", 1),
    )


def test_rf_h8_kanal_in_zwei_rollen() -> None:
    """s_Ref2 = -1 dreht Ref2/Ref1 (Antwort) und Vib Z/Ref2 (Referenz), nicht Vib Z/Ref1."""
    f = np.array([DF])
    cp = np.array([[H]], dtype=np.complex128)
    ap = {"Vib Z": np.array([[0.81]]), "Ref1": np.array([[1.05]]), "Ref2": np.array([[0.81]])}
    daten = ref.messdaten(
        frequenz_hz=f,
        ap=ap,
        cp={("Vib Z", "Ref1"): cp, ("Ref2", "Ref1"): cp, ("Vib Z", "Ref2"): cp},
        delta_f_hz=DF,
    )
    a = Annahmen(vorzeichen_kanal={"Ref2": -1})
    for paar, faktor in (
        (("Ref2", "Ref1"), -1.0),
        (("Vib Z", "Ref2"), -1.0),
        (("Vib Z", "Ref1"), 1.0),
    ):
        h1 = berechne_frf(bereite_paar(daten, *paar, a)).h1
        h1_0 = berechne_frf(bereite_paar(daten, *paar)).h1
        np.testing.assert_allclose(h1, faktor * h1_0, rtol=1e-12, err_msg=str(paar))


def test_rf_h8_konjugation_und_annahmentext() -> None:
    _, basis = _frf(0.05, 0.08)
    _, konj = _frf(0.05, 0.08, Annahmen(konjugieren=True))
    np.testing.assert_allclose(konj.h1, np.conj(basis.h1), rtol=1e-12)
    _, minus = _frf(0.05, 0.08, Annahmen(vorzeichen_kanal={"Ref1": -1}))
    assert any(e.nr == "M8" and "Ref1: -1" in e.wert for e in minus.annahmen)


@pytest.mark.parametrize(
    ("g2", "unten", "oben", "aussagekraeftig"),
    [
        (0.9, 0.8218258387, 1.1781741613, True),
        (0.2, 0.0, 2.0690449676, False),
        (0.0, 0.0, math.inf, False),
    ],
)
def test_rf_u7_fehlerband_unten_bei_null_begrenzt(
    g2: float, unten: float, oben: float, aussagekraeftig: bool
) -> None:
    """RF-U7 (K1-6): |H1| = 1, n_d = 7, k_ε = 2; rtol 1e-9 (+ halbe letzte Stelle)."""
    eps, _, _ = zufallsfehler(np.array([[g2]]), 7)
    if g2 == 0.2:
        assert eps[0, 0] == pytest.approx(0.5345224838, rel=1e-9, abs=5e-11)
        assert 1.0 - 2.0 * eps[0, 0] == pytest.approx(-0.0690449676, rel=1e-9, abs=5e-11)
    u, o, ok = fehlerband(np.ones((1, 1)), eps, 2.0)
    assert u[0, 0] == pytest.approx(unten, rel=1e-9, abs=5e-11)
    assert o[0, 0] == pytest.approx(oben, rel=1e-9, abs=5e-11)
    assert bool(ok[0, 0]) is aussagekraeftig


def test_rf_u7_kennzeichen_in_berechne_frf() -> None:
    # γ² = 0,2 aus Erwartungswerten: H = 1, S_x = 1, N_V = 1/0,2 - 1 = 4
    daten = ref.erwartungswert_paar(1.0 + 0j, 1.0, 0.0, 4.0)
    frf = berechne_frf(bereite_paar(daten, "Vib Z", "Ref1"))
    assert frf.kohaerenz[0, 0] == pytest.approx(0.2, rel=1e-12)
    assert frf.h1_band_unten[0, 0] == 0.0 and not frf.h1_band_aussagekraeftig[0, 0]
    assert HINWEIS_BAND_NICHT_AUSSAGEKRAEFTIG in frf.hinweise
    assert HINWEIS_BAND_NICHT_AUSSAGEKRAEFTIG.startswith(FEHLERBAND_NICHT_AUSSAGEKRAEFTIG)
    _, gut = _frf(0.05, 0.08)
    assert gut.h1_band_aussagekraeftig.all()
    assert HINWEIS_BAND_NICHT_AUSSAGEKRAEFTIG not in gut.hinweise


@pytest.mark.parametrize(
    ("rf", "n_d", "g2", "eps", "eps_g2", "w"),
    [
        ("RF-U1", 7, 0.9, 0.0890870806, 0.0563436170, 126.0),
        ("RF-U2", 7, 0.5, 0.2672612419, 0.3779644730, 14.0),
        ("RF-U3", 25, 0.99, 0.0142133811, 0.0028426762, 4950.0),
    ],
)
def test_rf_u1_bis_u3_zufallsfehler_und_gewicht(
    rf: str, n_d: int, g2: float, eps: float, eps_g2: float, w: float
) -> None:
    # Sollwerte mit zehn Nachkommastellen: zusätzlich atol = halbe letzte Stelle (5e-11),
    # sonst überschreitet die Rundung kleiner Werte (z. B. 0,0028426762) rtol 1e-9.
    feld = np.array([[g2]])
    e_h1, s_ph, e_g2 = zufallsfehler(feld, n_d)
    assert e_h1[0, 0] == pytest.approx(eps, rel=1e-9, abs=5e-11), rf
    assert s_ph[0, 0] == pytest.approx(eps, rel=1e-9, abs=5e-11), rf
    assert e_g2[0, 0] == pytest.approx(eps_g2, rel=1e-9, abs=5e-11), rf
    assert gewicht(feld, n_d)[0, 0] == pytest.approx(w, rel=1e-9), rf


def test_rf_u4_randwerte() -> None:
    e0, _, eg0 = zufallsfehler(np.array([[0.0]]), 7)
    assert e0[0, 0] == math.inf and eg0[0, 0] == math.inf
    assert gewicht(np.array([[0.0]]), 7)[0, 0] == 0.0
    e1, _, eg1 = zufallsfehler(np.array([[1.0]]), 7)
    assert e1[0, 0] == 0.0 and eg1[0, 0] == 0.0
    w1 = gewicht(np.array([[1.0]]), 7)[0, 0]
    assert math.isfinite(w1) and w1 == pytest.approx(2 * 7 * (1 - 1e-6) / 1e-6, rel=1e-6)
    en, _, _ = zufallsfehler(np.array([[0.9]]), 1)
    assert math.isnan(en[0, 0]) and math.isnan(gewicht(np.array([[0.9]]), 1)[0, 0])
    enan, _, _ = zufallsfehler(np.array([[np.nan]]), 7)
    assert math.isnan(enan[0, 0])


def test_rf_u4_n_d_eins_kohaerenz_nan_und_frf_bezeichnung() -> None:
    _, frf = _frf(0.05, 0.08, Annahmen(n_d=1))
    assert math.isnan(frf.kohaerenz[0, 0])
    assert math.isnan(frf.eps_betrag_h1[0, 0])
    assert frf.bezeichnung_h1 == "FRF"
    assert HINWEIS_ND1 in frf.hinweise and HINWEIS_ND_KLEIN in frf.hinweise
    assert not frf.kohaerenz_ok[0, 0]


def test_n_d_je_punkt() -> None:
    daten = ref.erwartungswert_paar(H, 1.0, 0.05, 0.08, form=(2, 3))
    frf = berechne_frf(bereite_paar(daten, "Vib Z", "Ref1", Annahmen(n_d=(7, 25))))
    e7, _, _ = zufallsfehler(np.array([[frf.kohaerenz[0, 0]]]), 7)
    e25, _, _ = zufallsfehler(np.array([[frf.kohaerenz[1, 0]]]), 25)
    assert frf.eps_betrag_h1[0, 0] == pytest.approx(e7[0, 0], rel=1e-15)
    assert frf.eps_betrag_h1[1, 2] == pytest.approx(e25[0, 0], rel=1e-15)
    assert frf.bezeichnung_h1 == "H1"


def test_fehlerband_um_h1() -> None:
    _, frf = _frf(0.05, 0.08)
    betrag = abs(frf.h1[0, 0])
    eps = frf.eps_betrag_h1[0, 0]
    assert frf.h1_band_unten[0, 0] == pytest.approx(betrag * (1 - 2 * eps), rel=1e-14)
    assert frf.h1_band_oben[0, 0] == pytest.approx(betrag * (1 + 2 * eps), rel=1e-14)


def test_rf_u5_monte_carlo_streuung_von_h1() -> None:
    """Statistisch (optional in FG-02): Std(|Ĥ1|/|H|) gegen Formelwert 0,04714, ±10 %."""
    rng = np.random.default_rng(20261029)
    m, n_d, g2 = 40000, 25, 0.9

    def cgauss(form: tuple[int, int], var: float) -> npt.NDArray[np.complex128]:
        werte = np.sqrt(var / 2) * (rng.standard_normal(form) + 1j * rng.standard_normal(form))
        return np.asarray(werte, dtype=np.complex128)

    x = cgauss((m, n_d), 1.0)
    y = H * x + cgauss((m, n_d), abs(H) ** 2 * (1 / g2 - 1))
    ap_b = np.mean(np.abs(x) ** 2, axis=1)[:, None]
    ap_a = np.mean(np.abs(y) ** 2, axis=1)[:, None]
    cp = np.mean(y * np.conj(x), axis=1)[:, None]
    h1, _, _ = h1_h2_kohaerenz(cp, ap_a, ap_b)
    streuung = float(np.std(np.abs(h1) / abs(H)))
    formel, _, _ = zufallsfehler(np.array([[g2]]), n_d)
    assert formel[0, 0] == pytest.approx(0.04714, rel=1e-4)
    assert streuung == pytest.approx(formel[0, 0], rel=0.10)


def test_rf_u6_maske_grenze_inklusiv() -> None:
    assert kohaerenz_maske(np.array([0.95, 0.9, 0.85, np.nan]), 0.9).tolist() == [
        True,
        True,
        False,
        False,
    ]


def test_begrenze_kohaerenz_alle_nan() -> None:
    werte, anzahl, maximum = begrenze_kohaerenz(np.array([np.nan, np.nan]))
    assert anzahl == 0 and math.isnan(maximum) and np.all(np.isnan(werte))


def test_nan_im_eingang_wird_weitergegeben() -> None:
    h1, _, g2 = h1_h2_kohaerenz(
        np.array([[np.nan + 0j, 1.0 + 0j]]), np.array([[1.0, 1.0]]), np.array([[1.0, np.nan]])
    )
    assert np.isnan(g2).all() and np.isnan(h1[0, 0]) and np.isnan(h1[0, 1])


# --- 9.8 Punktmittel ----------------------------------------------------------------------

X = np.array([[1.0 + 0j], [-1.0 + 0j], [2j]])


def test_rf_g1_betrags_und_quadratisches_mittel() -> None:
    m = punktmittel_betrag(X)
    assert m.mittel_betrag is not None and m.mittel_quadratisch is not None
    assert m.mittel_betrag[0] == pytest.approx(4 / 3, rel=1e-12)
    assert m.mittel_quadratisch[0] == pytest.approx(math.sqrt(2), rel=1e-12)
    komplex = abs(np.mean(X[:, 0]))
    assert komplex == pytest.approx(2 / 3, rel=1e-12)
    assert komplex <= m.mittel_betrag[0] <= m.mittel_quadratisch[0]
    assert m.n_mittel.tolist() == [3]


def test_rf_g2_ungueltiger_punkt() -> None:
    m = punktmittel_betrag(X, np.array([True, True, False]))
    assert m.mittel_betrag is not None and m.mittel_quadratisch is not None
    assert m.mittel_betrag[0] == pytest.approx(1.0, rel=1e-12)
    assert m.mittel_quadratisch[0] == pytest.approx(1.0, rel=1e-12)
    assert m.n_mittel.tolist() == [2]


def test_rf_g3_ap_mittel_und_wurzel() -> None:
    ap = np.array([[1.0], [4.0], [9.0]])
    m_ap = punktmittel_arithmetisch(ap)
    assert m_ap.mittel_arithmetisch is not None
    assert m_ap.mittel_arithmetisch[0] == pytest.approx(14 / 3, rel=1e-12)
    m_w = punktmittel_betrag(np.sqrt(ap))
    assert m_w.mittel_quadratisch is not None and m_w.mittel_betrag is not None
    assert m_w.mittel_quadratisch[0] == pytest.approx(2.1602468995, rel=1e-10)
    assert m_w.mittel_quadratisch[0] == pytest.approx(math.sqrt(14 / 3), rel=1e-12)
    assert m_w.mittel_betrag[0] == pytest.approx(2.0, rel=1e-12)


def test_rf_g4_nan_und_keine_gueltigen_punkte() -> None:
    x = np.array([[np.nan, 1.0], [2.0, 1.0], [4.0, 1.0]])
    m = punktmittel_betrag(x)
    assert m.mittel_betrag is not None
    assert m.mittel_betrag[0] == pytest.approx(3.0, rel=1e-12)
    assert m.n_mittel.tolist() == [2, 3]
    leer = punktmittel_betrag(x, np.zeros(3, dtype=bool))
    assert leer.mittel_betrag is not None and np.isnan(leer.mittel_betrag).all()
    assert leer.n_mittel.tolist() == [0, 0]


def test_punktmittel_formfehler() -> None:
    with pytest.raises(ValueError, match="P, K"):
        punktmittel_betrag(np.ones(3))
    with pytest.raises(ValueError, match="gueltig"):
        punktmittel_betrag(np.ones((3, 2)), np.ones(2, dtype=bool))
    with pytest.raises(TypeError):
        punktmittel_arithmetisch(np.ones((2, 2), dtype=np.complex128))
