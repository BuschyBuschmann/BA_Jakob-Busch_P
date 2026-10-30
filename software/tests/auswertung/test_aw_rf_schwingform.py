"""Referenzfälle FG-02 9.5 und 9.6: Schwingform/3D (RF-3D1 bis RF-3D7), Umrechnung (RF-W1 bis W3).

Toleranzen wie in FG-02 angegeben. Wo FG-02 exakte Werte zehnstellig gerundet angibt,
wird gegen die geschlossene Form verglichen (z. B. 1,4142135624 = √2).
"""

from __future__ import annotations

import math

import aw_referenz as ref
import numpy as np
import pytest

from ldv_automation.auswertung.gesamt import schwingform_aus
from ldv_automation.auswertung.schwingform import (
    betriebsschwingform,
    ellipse_kennwerte,
    momentanwert,
    waehle_linie,
)
from ldv_automation.auswertung.spektren import betrag_3d, betrag_3d_ap, staple_3d
from ldv_automation.auswertung.umrechnung import (
    ap_schnelle_zu_beschleunigung,
    ap_schnelle_zu_weg,
    mobilitaet_zu_akzeleranz,
    mobilitaet_zu_rezeptanz,
    schnelle_zu_beschleunigung,
    schnelle_zu_weg,
)


@pytest.mark.parametrize(
    ("rf", "v", "psv", "maximum", "minimum", "rtol"),
    [
        ("RF-3D1", [1, 1j, 0], math.sqrt(2), 1.0, 1.0, 1e-12),
        ("RF-3D2", np.array([1, 1, 0]) * np.exp(0.7j), math.sqrt(2), math.sqrt(2), 0.0, 1e-12),
        (
            "RF-3D3",
            [1, 0.5 * np.exp(1j * math.pi / 3), 0.2j],
            1.1357816692,
            1.0374517607,
            0.4622703151,
            1e-9,
        ),
        ("RF-3D4", [0, 0, 1e-3 * np.exp(-0.4j)], 1e-3, 1e-3, 0.0, 1e-12),
    ],
)
def test_rf_3d1_bis_3d4_kennwerte(
    rf: str, v: list[complex], psv: float, maximum: float, minimum: float, rtol: float
) -> None:
    p, mx, mn = ellipse_kennwerte(np.asarray(v, dtype=np.complex128))
    assert float(p) == pytest.approx(psv, rel=rtol), rf
    assert float(mx) == pytest.approx(maximum, rel=rtol), rf
    assert float(mn) == pytest.approx(minimum, rel=rtol, abs=1e-12), rf
    assert float(mn) <= float(mx) <= float(p) * (1 + 1e-15)


def test_rf_3d3_gegen_brute_force() -> None:
    v = np.array([1, 0.5 * np.exp(1j * math.pi / 3), 0.2j])
    theta = np.linspace(0, 2 * math.pi, 200001)
    r = np.linalg.norm(momentanwert(v, theta), axis=0)
    _, mx, mn = ellipse_kennwerte(v)
    # Rasterfehler der Brute-Force-Suche ~ (Δθ)²: rtol 1e-9
    assert r.max() == pytest.approx(float(mx), rel=1e-9)
    assert r.min() == pytest.approx(float(mn), rel=1e-9)


def test_rf_3d5_momentanwert() -> None:
    u = momentanwert(np.exp(1j * math.pi / 3), np.array([0.0, math.pi / 2, math.pi]))
    np.testing.assert_allclose(u, [0.5, -0.8660254038, -0.5], rtol=0, atol=1e-10)
    np.testing.assert_allclose(u, [0.5, -math.sqrt(3) / 2, -0.5], rtol=0, atol=1e-12)
    assert float(momentanwert(np.exp(1j * math.pi / 3), 0.0)) == pytest.approx(0.5, abs=1e-12)


F_ACHSE = (np.arange(1, 1601) * 1.5625).astype(np.float64)


@pytest.mark.parametrize(
    ("f_wahl", "index"), [(100.7, 63), (100.78125, 63), (0.8, 0), (2500.5, 1599)]
)
def test_rf_3d6_linienwahl(f_wahl: float, index: int) -> None:
    assert waehle_linie(F_ACHSE, f_wahl) == index


@pytest.mark.parametrize("f_wahl", [0.0, 2501.0, float("nan")])
def test_rf_3d6_ausserhalb_der_achse(f_wahl: float) -> None:
    with pytest.raises(ValueError, match="außerhalb"):
        waehle_linie(F_ACHSE, f_wahl)


def test_linienwahl_formfehler() -> None:
    with pytest.raises(ValueError, match="K >= 1"):
        waehle_linie(np.array([]), 1.0)
    with pytest.raises(ValueError, match="delta_f"):
        waehle_linie(np.array([5.0]), 5.0)
    assert waehle_linie(np.array([5.0]), 5.2, delta_f_hz=1.0) == 0


def _daten_3d(phase_gueltig: bool = True):  # type: ignore[no-untyped-def]
    f = np.array([10.0, 20.0, 30.0])
    p = 2
    amp = {
        "Vib X": np.array([[1, 2, 3], [0, 1, 0]], dtype=np.complex128),
        "Vib Y": np.array([[1j, 2j, 3j], [0, 0, 0]], dtype=np.complex128),
        "Vib Z": np.zeros((p, 3), dtype=np.complex128),
    }
    ap = {k: np.abs(v) ** 2 + 0.0 for k, v in amp.items()}
    ap["Ref1"] = np.ones((p, 3))
    cp = {(k, "Ref1"): v for k, v in amp.items()} if phase_gueltig else {}
    return ref.messdaten(frequenz_hz=f, ap=ap, cp=cp, phase_gueltig=phase_gueltig)


def test_schwingform_aus_daten_mit_phase() -> None:
    sf = schwingform_aus(_daten_3d(), 21.0)
    assert sf.linie == 1 and sf.f_hz == 20.0 and sf.phase_gueltig and sf.quelle == "cph"
    assert sf.amplitude is not None
    np.testing.assert_allclose(sf.amplitude[0], [2, 2j, 0], rtol=1e-15)
    assert sf.betrag_3d_psv[0] == pytest.approx(math.sqrt(8), rel=1e-15)
    assert sf.auslenkung_max[0] == pytest.approx(2.0, rel=1e-15)
    assert sf.momentanwert(0.0).shape == (2, 3)
    assert sf.momentanwert(np.array([0.0, 1.0])).shape == (2, 3, 2)
    h1 = schwingform_aus(_daten_3d(), 21.0, quelle="h1")
    assert h1.einheit == "(m/s)/N" and h1.quelle == "h1"
    assert h1.amplitude is not None
    np.testing.assert_allclose(h1.amplitude, sf.amplitude, rtol=1e-15)  # AP_Ref1 = 1


def test_rf_3d7_ohne_phase_nur_betrag_und_keine_animation() -> None:
    sf = schwingform_aus(_daten_3d(phase_gueltig=False), 30.0)
    assert not sf.phase_gueltig and sf.amplitude is None and sf.quelle == "leistung"
    np.testing.assert_allclose(sf.betrag[0], [3.0, 3.0, 0.0], rtol=1e-15)
    assert sf.betrag_3d_psv[0] == pytest.approx(math.sqrt(18), rel=1e-15)
    assert np.isnan(sf.auslenkung_max).all()
    with pytest.raises(ValueError, match="Animation"):
        sf.momentanwert(0.0)


def test_betriebsschwingform_eingabefehler() -> None:
    f = np.array([1.0, 2.0])
    with pytest.raises(ValueError, match="amplitude_3d"):
        betriebsschwingform(f, 1.0)
    with pytest.raises(ValueError, match="leistung_3d"):
        betriebsschwingform(f, 1.0, phase_gueltig=False)
    with pytest.raises(ValueError, match="Komponenten"):
        ellipse_kennwerte(np.ones(2))


def test_3d_betrag_aus_komponenten_und_ap() -> None:
    x = np.array([[3.0 + 0j]])
    y = np.array([[4j]])
    z = np.zeros((1, 1), dtype=np.complex128)
    s = staple_3d(x, y, z)
    assert s.shape == (1, 3, 1)
    assert betrag_3d(s)[0, 0] == pytest.approx(5.0, rel=1e-15)
    assert betrag_3d_ap(np.abs(s) ** 2)[0, 0] == pytest.approx(5.0, rel=1e-15)
    with pytest.raises(ValueError):
        staple_3d(x, y, np.zeros((2, 1)))
    with pytest.raises(ValueError):
        betrag_3d(np.ones((1, 2, 1)))
    with pytest.raises(ValueError):
        betrag_3d_ap(np.ones((1, 2, 1)))


# --- 9.6 Umrechnung ---------------------------------------------------------------------


def test_rf_w1_weg_und_beschleunigung() -> None:
    f = np.array([100.0])
    d = schnelle_zu_weg(np.array([1.0]), f)[0]
    a = schnelle_zu_beschleunigung(np.array([1.0]), f)[0]
    assert d.real == 0.0
    assert d.imag == pytest.approx(-1.5915494309e-3, rel=1e-10)
    assert d.imag == pytest.approx(-1 / (2 * math.pi * 100), rel=1e-12)
    assert np.angle(d) == pytest.approx(-math.pi / 2, rel=1e-12)
    assert a == pytest.approx(628.3185307j, rel=1e-10)
    assert a.imag == pytest.approx(200 * math.pi, rel=1e-12)


def test_rf_w2_rezeptanz_und_akzeleranz_des_einmassenschwingers() -> None:
    f = np.array([100.0])
    y = ref.mobilitaet_sdof(f)
    rez = mobilitaet_zu_rezeptanz(y, f)[0]
    akz = mobilitaet_zu_akzeleranz(y, f)[0]
    assert rez.imag == pytest.approx(-1.2665147955e-4, rel=1e-10)
    assert abs(rez.real) <= 1e-10 * abs(rez)
    assert akz.imag == pytest.approx(50.0, rel=1e-10)
    assert abs(akz.real) <= 1e-10 * abs(akz)


def test_rf_w3_omega_null_weg_nan() -> None:
    f = np.array([0.0, 1.0])
    d = schnelle_zu_weg(np.array([1.0, 1.0]), f)
    assert np.isnan(d[0].real) and np.isnan(d[0].imag) and np.isfinite(d[1])
    assert np.isnan(ap_schnelle_zu_weg(np.array([1.0, 1.0]), f)[0])


def test_autospektren_umrechnung_und_phasenlage() -> None:
    f = np.array([50.0])
    w = 2 * math.pi * 50.0
    assert ap_schnelle_zu_weg(np.array([4.0]), f)[0] == pytest.approx(4.0 / w**2, rel=1e-15)
    assert ap_schnelle_zu_beschleunigung(np.array([4.0]), f)[0] == pytest.approx(
        4 * w**2, rel=1e-15
    )
    v = np.exp(0.3j)
    assert np.angle(schnelle_zu_weg(np.array([v]), f)[0]) == pytest.approx(0.3 - math.pi / 2)
    assert np.angle(schnelle_zu_beschleunigung(np.array([v]), f)[0]) == pytest.approx(
        0.3 + math.pi / 2
    )
    with pytest.raises(ValueError, match="Frequenzachse"):
        schnelle_zu_weg(np.ones(3), np.ones(2))
