"""Rechenkern der Animation (R-071): Referenzfälle RF-A1 bis RF-A14 und RF-N1 bis RF-N7.

Sollwerte aus FG-04 (Abschnitt 5) und FG-04 Nachtrag 1 (Abschnitt 6). Toleranzen wie dort:
``rtol = 1e-12`` für Werte ungleich null; Nullwerte (z. B. cos(π/2) ≈ 6e-17) mit
``atol = 1e-12 * a`` (a = Amplitude des Falls, weil der Rundungsrest von θ_n so skaliert);
Winkel mit ``atol = 1e-12`` rad, bei ±π über e^{iφ} verglichen; Überhöhung ``rtol = 1e-10``;
RF-A12 ``rtol = 1e-9``. Literalwerte aus der Fachgrundlage haben nur 10 bis 11 Stellen und
werden mit ``rtol = 1e-9`` verglichen, die geschlossenen Ausdrücke mit ``rtol = 1e-12``.
"""

from __future__ import annotations

import math

import numpy as np
import pytest

from ldv_automation.auswertung.animation import (
    ALPHA_VORGABE,
    HINWEIS_UEBERLAGERUNG,
    animierte_amplitude,
    auslenkung_amplitude,
    bewegt_maske,
    bezugsgroesse,
    bezugsphase,
    bildwinkel,
    kreisfrequenz_rad_s,
    maximum_theta,
    phasenfehler_grenze,
    positionen_m,
    relativ_gedreht,
    ueberhoehung_auto,
    ueberhoehung_hinweis,
    verschiebung,
    waehle_bezugskomponente,
    waehle_bezugspunkt_3d,
)
from ldv_automation.auswertung.schwingform import (
    betriebsschwingform,
    ellipse_kennwerte,
    momentanwert,
    phase_relativ_rad,
)

F_HZ = 100.0
OMEGA = 2.0 * math.pi * F_HZ
#: a = 1 mm/s / ω = 1,5915494309e-6 m (FG-04 5)
A_MM = 1e-3 / OMEGA
TH_N = np.array([0.0, math.pi / 2.0, math.pi, 3.0 * math.pi / 2.0])
TH_13 = np.linspace(0.0, 2.0 * math.pi, 13)


def _e(winkel: np.ndarray) -> np.ndarray:
    """e^{iφ}: Winkelvergleich ohne Sprung bei ±π."""
    return np.exp(1j * np.asarray(winkel))


# --------------------------------------------------------------------------- RF-A1 .. RF-A5


def test_rf_a1_einzelpunkt_reell() -> None:
    v = np.array([1e-3 + 0j])
    d = auslenkung_amplitude(v, F_HZ)
    np.testing.assert_allclose(d, [-1j * A_MM], rtol=1e-12, atol=0)
    np.testing.assert_allclose(d, [-1j * 1.5915494309e-6], rtol=1e-9)
    np.testing.assert_allclose(
        verschiebung(d, TH_N)[0], [0.0, A_MM, 0.0, -A_MM], rtol=1e-12, atol=1e-12 * A_MM
    )
    # Schnelle: u(θ_n) = 1e-3, 0, -1e-3, 0 m/s
    np.testing.assert_allclose(
        verschiebung(v, TH_N)[0], [1e-3, 0.0, -1e-3, 0.0], rtol=1e-12, atol=1e-12 * 1e-3
    )


def test_rf_a1_h1_je_newton() -> None:
    d = auslenkung_amplitude(np.array([1.0 + 0j]), F_HZ)  # H1 = 1 (m/s)/N
    np.testing.assert_allclose(d, [-1j * 1.5915494309e-3], rtol=1e-9)
    np.testing.assert_allclose(d, [-1j / OMEGA], rtol=1e-12)


def test_rf_a2_einzelpunkt_mit_phase() -> None:
    v = np.array([1e-3 * np.exp(1j * math.pi / 3.0)])
    d = verschiebung(auslenkung_amplitude(v, F_HZ), TH_N)[0] / A_MM
    soll = np.sin(TH_N + math.pi / 3.0)
    np.testing.assert_allclose(d, soll, rtol=1e-12, atol=1e-12)
    np.testing.assert_allclose(d, [0.8660254038, 0.5, -0.8660254038, -0.5], rtol=1e-9)


def test_rf_a3_zwei_punkte_gegenphasig() -> None:
    v = np.array([1e-3, -1e-3], dtype=np.complex128)
    d = auslenkung_amplitude(v, F_HZ)
    x = verschiebung(d, TH_13)
    np.testing.assert_allclose(x[1], -x[0], rtol=0, atol=1e-12 * A_MM)
    np.testing.assert_allclose(np.sum(x, axis=0), 0.0, rtol=0, atol=1e-12 * A_MM)
    # Δφ = +π einheitlich (180°), Maxima um T/2 versetzt
    assert phase_relativ_rad(v, 0)[1] == pytest.approx(math.pi, abs=1e-12)
    theta_max = maximum_theta(np.angle(v))
    diff = np.mod(theta_max[1] - theta_max[0], 2.0 * math.pi)
    assert diff == pytest.approx(math.pi, abs=1e-12)


def test_rf_a4_phasenvorlauf() -> None:
    v = np.array([1e-3, 1e-3j])
    phi = np.angle(v)
    theta_max = maximum_theta(phi)
    assert theta_max[0] == pytest.approx(math.pi / 2.0, abs=1e-12)
    assert theta_max[1] == pytest.approx(0.0, abs=1e-12)
    # q erreicht das Maximum um T/4 = 2,5 ms früher
    delta_t_s = (theta_max[1] - theta_max[0]) / OMEGA
    assert delta_t_s == pytest.approx(-2.5e-3, rel=1e-12)
    # Gitter: Maximum von q bei θ = 0 (Auslenkung = +a), von p bei θ = π/2
    x = verschiebung(auslenkung_amplitude(v, F_HZ), TH_N)
    assert x[1, 0] == pytest.approx(A_MM, rel=1e-12)
    assert x[0, 1] == pytest.approx(A_MM, rel=1e-12)
    # Schnelle: θ_max = -φ
    np.testing.assert_allclose(
        np.exp(1j * maximum_theta(phi, "schnelle")), np.exp(-1j * phi), atol=1e-12
    )


@pytest.mark.parametrize("phi", [0.0, 0.7, -2.0, math.pi])
def test_rf_a5_reelle_gegen_komplexe_form(phi: float) -> None:
    betrag = 3e-4
    v = np.array([betrag * np.exp(1j * phi)])
    theta = np.linspace(-7.0, 7.0, 57)
    komplex_ = verschiebung(auslenkung_amplitude(v, F_HZ), theta)[0]
    reell = (betrag / OMEGA) * (np.sin(phi) * np.cos(theta) + np.cos(phi) * np.sin(theta))
    np.testing.assert_allclose(komplex_, reell, rtol=0, atol=1e-12 * betrag / OMEGA)


# --------------------------------------------------------------------------- RF-A6


def test_rf_a6_3d_kreisbahn() -> None:
    v = 1e-3 * np.array([[1.0, 1j, 0.0]])
    d = auslenkung_amplitude(v, F_HZ)
    x = verschiebung(d[0], TH_N)  # (3, 4): Zeilen X, Y, Z
    soll = np.array([[0, 1, 0], [1, 0, 0], [0, -1, 0], [-1, 0, 0]], dtype=float).T
    np.testing.assert_allclose(x / A_MM, soll, rtol=0, atol=1e-12)
    # Drehsinn im Uhrzeigersinn um +z: m = Im v kreuz Re v = (0, 0, -1) 1e-6
    m = np.cross(v[0].imag, v[0].real)
    np.testing.assert_allclose(m, [0.0, 0.0, -1e-6], rtol=0, atol=1e-18)
    # Halbachsen gleich a (Schnelle: 1e-3)
    _, maximum, minimum = ellipse_kennwerte(d)
    np.testing.assert_allclose([maximum[0], minimum[0]], [A_MM, A_MM], rtol=1e-12)
    _, v_max, v_min = ellipse_kennwerte(v)
    np.testing.assert_allclose([v_max[0], v_min[0]], [1e-3, 1e-3], rtol=1e-12)


# --------------------------------------------------------------------------- RF-A7, RF-A8


def _rf_a7_daten() -> tuple[np.ndarray, np.ndarray]:
    d = auslenkung_amplitude(np.array([1e-3, 0.5e-3, 1e-2], dtype=np.complex128), F_HZ)
    return d[:2], d


def test_rf_a7_ueberhoehung() -> None:
    d, _ = _rf_a7_daten()
    d_ref = bezugsgroesse(d, [True, True])
    assert d_ref == pytest.approx(1.5915494309e-6, rel=1e-9)
    assert d_ref == pytest.approx(A_MM, rel=1e-12)
    assert d_ref is not None
    s = ueberhoehung_auto(0.029, d_ref, ALPHA_VORGABE)
    assert s is not None
    assert s == pytest.approx(4555.3093477, rel=1e-10)
    assert s * d_ref == pytest.approx(7.25e-3, rel=1e-12)
    # angezeigte Amplitude Punkt 2 / Punkt 1 = 0,5 (ein Faktor für alle)
    assert (s * abs(d[1])) / (s * abs(d[0])) == pytest.approx(0.5, rel=1e-12)
    # größte angezeigte Auslenkung = alpha d_NN
    x0 = np.zeros((2, 3))
    d3 = np.zeros((2, 3), dtype=np.complex128)
    d3[:, 2] = d
    gross = max(
        abs(positionen_m(x0, d3, th, s, [True, True])[0, 2]) for th in np.linspace(0, 7, 4001)
    )
    assert gross == pytest.approx(7.25e-3, rel=1e-6)


def test_rf_a8_maskierter_punkt_veraendert_s_nicht() -> None:
    d2, d3 = _rf_a7_daten()
    s_ref = ueberhoehung_auto(0.029, bezugsgroesse(d2, [True, True]))
    assert s_ref is not None
    koord = np.array([[0.0, 0.0, 0.0], [0.029, 0.0, 0.0], [0.0, 0.029, 0.0]])
    schnelle = np.array([1e-3, 0.5e-3, 1e-2], dtype=np.complex128)
    faelle = {
        "kohaerenz": (np.array([True, True, False]), np.array([True, True, True]), d3),
        "m6": (np.array([True, True, True]), np.array([True, True, False]), d3),
        "nan": (np.array([True, True, True]), np.array([True, True, True]), d3.copy()),
    }
    faelle["nan"][2][2] = complex(math.nan, math.nan)
    schnelle_nan = schnelle.copy()
    schnelle_nan[2] = complex(math.nan, math.nan)
    for name, (koh, gueltig, d_voll) in faelle.items():
        v = schnelle_nan if name == "nan" else schnelle
        bewegt = bewegt_maske(v, koh, gueltig)
        np.testing.assert_array_equal(bewegt, [True, True, False])
        s = ueberhoehung_auto(0.029, bezugsgroesse(d_voll, bewegt))
        assert s == pytest.approx(s_ref, rel=1e-12)
        d3d = np.zeros((3, 3), dtype=np.complex128)
        d3d[:, 0] = d_voll
        for theta in TH_13:
            pos = positionen_m(koord, d3d, float(theta), s_ref, bewegt)
            np.testing.assert_array_equal(pos[2], koord[2])  # exakt, nicht Näherung
        # bewegte Punkte bewegen sich
        assert positionen_m(koord, d3d, math.pi / 2, s_ref, bewegt)[0, 0] != koord[0, 0]


# --------------------------------------------------------------------------- RF-A9


def test_rf_a9_linienfrequenz_statt_f_wahl() -> None:
    frequenz = (0.625 * np.arange(1, 321)).astype(np.float64)
    amp = np.full((1, 3, frequenz.size), 1e-3, dtype=np.complex128)
    sf = betriebsschwingform(frequenz, 100.2, amplitude_3d=amp, delta_f_hz=0.625)
    assert sf.linie == 159
    assert sf.f_hz == pytest.approx(100.0, abs=1e-12)
    assert sf.amplitude is not None
    d = animierte_amplitude(sf.amplitude, sf.f_hz, phase_gueltig=sf.phase_gueltig)
    np.testing.assert_allclose(np.abs(d), 1.5915494309e-6, rtol=1e-9)
    np.testing.assert_allclose(np.abs(d), 1e-3 / (2.0 * math.pi * 100.0), rtol=1e-12)
    # mit f_wahl gerechnet wäre es 1,5883726855e-6 (-0,1996 %): der Test muss das unterscheiden
    falsch = np.abs(auslenkung_amplitude(sf.amplitude, sf.f_wahl_hz))
    np.testing.assert_allclose(falsch, 1.5883726855e-6, rtol=1e-9)
    assert (np.abs(d) - falsch).max() / np.abs(d).max() == pytest.approx(0.001996, rel=1e-3)
    assert not np.allclose(np.abs(d), falsch, rtol=1e-4, atol=0)


# --------------------------------------------------------------------------- RF-A10, A11

V_A10 = 1e-3 * np.array([1.0, 0.5 * np.exp(1.1j), 0.8 * np.exp(-2.0j)])


def test_rf_a10_polaritaet_absolut_verschiebt_um_halbe_periode() -> None:
    n = 36
    theta = bildwinkel(n)
    bilder = verschiebung(auslenkung_amplitude(V_A10, F_HZ), theta)  # (P, N)
    bilder_neg = verschiebung(auslenkung_amplitude(-V_A10, F_HZ), theta)
    np.testing.assert_allclose(
        bilder_neg, np.roll(bilder, -n // 2, axis=1), rtol=0, atol=1e-12 * A_MM
    )
    # genau die um N/2 zyklisch verschobene Folge
    for j in range(n):
        np.testing.assert_allclose(
            bilder_neg[:, j], bilder[:, (j + n // 2) % n], rtol=0, atol=1e-12 * A_MM
        )


def test_rf_a10_relativ_ist_bildgleich() -> None:
    w = relativ_gedreht(V_A10, 0)
    w_neg = relativ_gedreht(-V_A10, 0)
    np.testing.assert_array_equal(w, w_neg)
    theta = bildwinkel(36)
    np.testing.assert_array_equal(
        verschiebung(auslenkung_amplitude(w, F_HZ), theta),
        verschiebung(auslenkung_amplitude(w_neg, F_HZ), theta),
    )


def test_rf_a11_relative_amplitude() -> None:
    w = relativ_gedreht(V_A10, 0)
    assert w[0].real == pytest.approx(1e-3, rel=1e-12)
    assert abs(w[0].imag) <= 1e-12 * 1e-3
    delta = np.angle(w)
    np.testing.assert_allclose(_e(delta), _e(np.array([0.0, 1.1, -2.0])), rtol=0, atol=1e-12)
    np.testing.assert_allclose(np.degrees(delta), [0.0, 63.03, -114.59], atol=5e-3)
    np.testing.assert_allclose(np.abs(w), np.abs(V_A10), rtol=1e-12)
    # Konsistenz mit der 2D-Phase (ADR-025)
    np.testing.assert_allclose(_e(delta), _e(phase_relativ_rad(V_A10, 0)), rtol=0, atol=1e-12)


# --------------------------------------------------------------------------- RF-A12, A13, A14


#: Sollwerte ΔA/A = 1 - cos(π/N) wie in FG-04 gedruckt (N=24: "0,856 %", N=72: "0,095 %").
#: Toleranz = halbe Einheit der letzten angegebenen Stelle (Rundung der Fachgrundlage).
@pytest.mark.parametrize(
    ("n", "delta_a_rel", "halbe_stelle"),
    [
        (36, 0.0038053, 5e-8),
        (12, 0.034074, 5e-7),
        (24, 0.00856, 5e-6),
        (72, 0.00095, 5e-6),
    ],
)
def test_rf_a12_bilder_je_periode(n: int, delta_a_rel: float, halbe_stelle: float) -> None:
    theta = bildwinkel(n)
    assert theta.shape == (n,)
    assert theta[0] == 0.0
    assert theta[-1] == pytest.approx(2.0 * math.pi * (n - 1) / n, rel=1e-12)
    assert theta[-1] < 2.0 * math.pi - 1e-9  # kein Bild bei 360° (Duplikat)
    delta_phi, delta_a = phasenfehler_grenze(n)
    assert delta_phi == pytest.approx(math.pi / n, rel=1e-12)
    assert delta_a == pytest.approx(1.0 - math.cos(math.pi / n), rel=1e-9)
    assert delta_a == pytest.approx(delta_a_rel, abs=halbe_stelle)
    # Worst case auf dem Gitter: Maximum genau zwischen zwei Bildern
    spitze = np.max(np.cos(theta - math.pi / n))  # Maximum genau zwischen zwei Bildern
    assert spitze == pytest.approx(math.cos(math.pi / n), rel=1e-9)


def test_rf_a12_zahlenwerte_n36_n12() -> None:
    theta36 = bildwinkel(36)
    assert theta36[9] == pytest.approx(math.pi / 2.0, abs=1e-12)
    assert math.degrees(theta36[-1]) == pytest.approx(350.0, abs=1e-9)
    d36, a36 = phasenfehler_grenze(36)
    assert math.degrees(d36) == pytest.approx(5.0, rel=1e-12)
    assert a36 == pytest.approx(1.0 - math.cos(math.radians(5.0)), rel=1e-9)
    assert a36 == pytest.approx(0.0038053, rel=1e-4)
    d12, a12 = phasenfehler_grenze(12)
    assert math.degrees(d12) == pytest.approx(15.0, rel=1e-12)
    assert a12 == pytest.approx(0.034074, rel=1e-4)


def test_rf_a12_ungueltige_bildzahl() -> None:
    with pytest.raises(ValueError, match="n >= 1"):
        bildwinkel(0)
    with pytest.raises(ValueError, match="n >= 1"):
        phasenfehler_grenze(0)


@pytest.mark.parametrize("n", [2.5, 36.0, math.nan, -1.0])
def test_n2_bildwinkel_nur_ganzzahlig(n: float) -> None:
    with pytest.raises(ValueError, match="ganzzahlig"):
        bildwinkel(n)  # type: ignore[arg-type]


def test_n2_bildwinkel_akzeptiert_numpy_ganzzahl() -> None:
    np.testing.assert_array_equal(bildwinkel(np.int64(12)), bildwinkel(12))  # type: ignore[arg-type]


def test_rf_a13_weg_gegen_schnelle() -> None:
    v = np.array([1e-3 * np.exp(0.7j)])
    d = auslenkung_amplitude(v, F_HZ)
    theta = np.linspace(-6.0, 6.0, 49)
    u = verschiebung(v, theta)[0]
    d_versetzt = verschiebung(d, theta + math.pi / 2.0)[0]
    np.testing.assert_allclose(u, OMEGA * d_versetzt, rtol=0, atol=1e-12 * 1e-3)


def test_momentanwert_bleibt_die_schnelle() -> None:
    """Regression: ``momentanwert`` ist unverändert Re{v e^{iθ}} (Schnelle, nicht Auslenkung)."""
    v = np.array([1e-3 * np.exp(0.7j), 2e-3 * np.exp(-1.0j)])
    theta = np.linspace(-3.0, 3.0, 11)
    np.testing.assert_array_equal(momentanwert(v, theta), np.real(v[:, None] * np.exp(1j * theta)))
    np.testing.assert_array_equal(momentanwert(v, theta), verschiebung(v, theta))
    np.testing.assert_array_equal(momentanwert(v, 0.4), np.real(v * np.exp(0.4j)))


def test_rf_a14_ohne_phase_keine_animation() -> None:
    with pytest.raises(ValueError, match="ohne Referenz"):
        animierte_amplitude(None, F_HZ, phase_gueltig=False)
    with pytest.raises(ValueError, match="ohne Referenz"):
        animierte_amplitude(np.ones((2, 3), dtype=np.complex128), F_HZ, phase_gueltig=False)
    frequenz = (0.5 * np.arange(1, 9)).astype(np.float64)
    sf = betriebsschwingform(frequenz, 2.0, leistung_3d=np.ones((2, 3, 8)), phase_gueltig=False)
    assert sf.amplitude is None
    with pytest.raises(ValueError, match="ohne Referenz"):
        animierte_amplitude(sf.amplitude, sf.f_hz, phase_gueltig=sf.phase_gueltig)
    with pytest.raises(ValueError):
        sf.momentanwert(0.0)


# --------------------------------------------------------------------------- Randfälle (Kern)


@pytest.mark.parametrize("f", [0.0, -1.0, math.nan, math.inf])
def test_omega_nicht_positiv_oder_nicht_endlich_ergibt_nan(f: float) -> None:
    assert math.isnan(kreisfrequenz_rad_s(f))
    d = auslenkung_amplitude(np.array([1e-3 + 0j, 0.0 + 0j]), f)
    assert d.shape == (2,)
    assert np.all(np.isnan(d.real)) and np.all(np.isnan(d.imag))
    # ein solcher Punkt wird wie ungültig behandelt (nicht endlich -> steht)
    assert not bewegt_maske(d, np.array([True, True])).any()


def test_alle_punkte_ohne_bewegung_haben_keine_bezugsgroesse() -> None:
    d = auslenkung_amplitude(np.array([1e-3, 2e-3], dtype=np.complex128), F_HZ)
    assert bezugsgroesse(d, [False, False]) is None
    assert bezugsgroesse(np.zeros(0, dtype=np.complex128), np.zeros(0, dtype=bool)) is None
    d_nan = np.full(2, complex(math.nan, math.nan))
    assert bezugsgroesse(d_nan, [True, True]) is None


def test_d_ref_null_ergibt_none_und_kein_s() -> None:
    d = np.zeros(3, dtype=np.complex128)
    assert bezugsgroesse(d, [True, True, True]) is None
    d3 = np.zeros((3, 3), dtype=np.complex128)
    assert bezugsgroesse(d3, [True, True, True]) is None
    assert ueberhoehung_auto(0.029, None) is None
    assert ueberhoehung_auto(0.029, 0.0) is None


def test_ein_punkt_kein_nachbarabstand_kein_s() -> None:
    d = auslenkung_amplitude(np.array([1e-3 + 0j]), F_HZ)
    assert bezugsgroesse(d, [True]) == pytest.approx(A_MM, rel=1e-12)
    assert ueberhoehung_auto(None, bezugsgroesse(d, [True])) is None
    assert ueberhoehung_auto(0.0, A_MM) is None
    assert ueberhoehung_auto(math.nan, A_MM) is None


def test_ueberhoehung_alpha_muss_positiv_sein() -> None:
    with pytest.raises(ValueError, match="alpha"):
        ueberhoehung_auto(0.029, A_MM, alpha=0.0)
    assert ueberhoehung_auto(0.04, 0.001, alpha=0.5) == pytest.approx(20.0, rel=1e-12)


def test_ueberhoehung_hinweis_grenze() -> None:
    d_nn_min = 0.02
    d_ref = 1e-6
    grenze = 0.5 * d_nn_min / d_ref
    assert ueberhoehung_hinweis(0.99 * grenze, d_ref, d_nn_min) is None
    assert ueberhoehung_hinweis(grenze, d_ref, d_nn_min) == HINWEIS_UEBERLAGERUNG
    assert ueberhoehung_hinweis(2.0 * grenze, d_ref, d_nn_min) == HINWEIS_UEBERLAGERUNG


def test_bezugsgroesse_3d_nimmt_grosse_halbachse() -> None:
    v = 1e-3 * np.array([[1.0, 1j, 0.0], [3.0, 0.0, 0.0], [10.0, 0.0, 0.0]])
    d = auslenkung_amplitude(v, F_HZ)
    assert bezugsgroesse(d, [True, True, False]) == pytest.approx(3e-3 / OMEGA, rel=1e-12)
    assert bezugsgroesse(d, [True, False, False]) == pytest.approx(1e-3 / OMEGA, rel=1e-12)


def test_bewegt_maske_einzelkomponente() -> None:
    v = np.array([1.0, 0.0, math.nan, math.inf, 1.0, 1.0], dtype=np.complex128)
    koh = np.array([True, True, True, True, False, True])
    gueltig = np.array([True, True, True, True, True, False])
    np.testing.assert_array_equal(
        bewegt_maske(v, koh, gueltig), [True, True, False, False, False, False]
    )
    # |v| = 0 exakt: gültig und "bewegt" (Auslenkung 0)
    assert bewegt_maske(v, koh)[1]


def test_a1_3d_bewegt_nur_bei_drei_gueltigen_komponenten() -> None:
    v = np.ones((4, 3), dtype=np.complex128)
    koh = np.ones((4, 3), dtype=bool)
    koh[1, 2] = False  # eine Komponente unter γ²_min
    v[2, 0] = complex(math.nan, 0.0)  # eine nicht endliche Komponente
    gueltig = np.array([True, True, True, False])  # M6 je Punkt
    np.testing.assert_array_equal(bewegt_maske(v, koh, gueltig), [True, False, False, False])
    # M6 je Komponente
    g3 = np.ones((4, 3), dtype=bool)
    g3[0, 1] = False
    assert not bewegt_maske(v, np.ones((4, 3), dtype=bool), g3)[0]


def test_formfehler() -> None:
    with pytest.raises(ValueError):
        bewegt_maske(np.ones(3), np.ones(2, dtype=bool))
    with pytest.raises(ValueError):
        bewegt_maske(np.ones((3, 2)), np.ones((3, 2), dtype=bool))
    with pytest.raises(ValueError):
        bewegt_maske(np.ones(3), np.ones(3, dtype=bool), np.ones(4, dtype=bool))
    with pytest.raises(ValueError):
        bezugsgroesse(np.ones(3), np.ones(2, dtype=bool))
    with pytest.raises(ValueError):
        bezugsgroesse(np.ones((3, 2)), np.ones(3, dtype=bool))
    with pytest.raises(ValueError):
        relativ_gedreht(np.ones((3, 2)), 0)
    with pytest.raises(ValueError):
        relativ_gedreht(np.ones(3), 3)
    with pytest.raises(ValueError):
        relativ_gedreht(np.ones(3), 0, komponente=1)
    with pytest.raises(ValueError):
        relativ_gedreht(np.ones(3), 0, bewegt=np.ones(2, dtype=bool))
    with pytest.raises(ValueError):
        positionen_m(np.zeros((2, 3)), np.zeros((2, 2)), 0.0, 1.0, [True, True])
    with pytest.raises(ValueError):
        positionen_m(np.zeros((2, 3)), np.zeros((2, 3)), 0.0, 1.0, [True])
    with pytest.raises(ValueError):
        positionen_m(np.zeros((2, 3)), np.zeros((2, 3)), np.array([0.0, 1.0]), 1.0, [True, True])  # type: ignore[arg-type]
    with pytest.raises(ValueError):
        waehle_bezugspunkt_3d(np.ones(3), [True] * 3)
    with pytest.raises(ValueError):
        waehle_bezugspunkt_3d(np.ones((3, 3)), [True] * 2)
    with pytest.raises(ValueError, match="groesse"):
        maximum_theta(0.0, "weg")  # type: ignore[arg-type]
    with pytest.raises(ValueError, match="groesse"):
        animierte_amplitude(np.ones(2), F_HZ, groesse="weg")  # type: ignore[arg-type]
    with pytest.raises(ValueError, match="erwartet"):
        bezugsphase(np.ones(2))
    with pytest.raises(ValueError, match=r"Bezugskomponente 0\.\.2"):
        bezugsphase(np.ones(3), 3)
    with pytest.raises(ValueError, match="Einzelkomponente"):
        bezugsphase(1.0 + 0j, 1)


def test_animierte_amplitude_kombinationen() -> None:
    v = 1e-3 * np.array([[1.0, 0.5j, 0.2], [0.3, 0.4, 0.1j]])
    d_abs = animierte_amplitude(v, F_HZ)
    np.testing.assert_array_equal(d_abs, auslenkung_amplitude(v, F_HZ))
    w = relativ_gedreht(v, 0)
    np.testing.assert_array_equal(
        animierte_amplitude(v, F_HZ, bezug=0), auslenkung_amplitude(w, F_HZ)
    )
    np.testing.assert_array_equal(animierte_amplitude(v, F_HZ, groesse="schnelle"), v)
    np.testing.assert_array_equal(animierte_amplitude(v, F_HZ, groesse="schnelle", bezug=0), w)
    # Auslenkung gegen Schnelle: Zeitnullpunkt um T/4 verschoben (RF-A13), Form gleich
    u = verschiebung(animierte_amplitude(v, F_HZ, groesse="schnelle"), TH_13)
    dd = verschiebung(d_abs, TH_13 + math.pi / 2.0)
    np.testing.assert_allclose(u, OMEGA * dd, rtol=0, atol=1e-12 * 1e-3)
    # Einzelkomponente
    np.testing.assert_array_equal(
        animierte_amplitude(v[:, 1], F_HZ, bezug=1, komponente=None),
        auslenkung_amplitude(relativ_gedreht(v[:, 1], 1), F_HZ),
    )


def test_positionen_nur_bewegte_punkte_und_ein_faktor() -> None:
    koord = np.array([[0.0, 0.0, 0.0], [0.1, 0.2, 0.3]])
    d = np.array([[1j, 0, 0], [0, 2.0, 0]], dtype=np.complex128)
    pos = positionen_m(koord, d, math.pi / 2.0, 10.0, [True, True])
    # d_x = Re{ i e^{iπ/2} } = -1; d_y = Re{2 e^{iπ/2}} = 0
    np.testing.assert_allclose(pos[0], [-10.0, 0.0, 0.0], atol=1e-12)
    np.testing.assert_allclose(pos[1], [0.1, 0.2, 0.3], atol=1e-12)
    pos0 = positionen_m(koord, d, 0.0, 10.0, [False, True])
    np.testing.assert_array_equal(pos0[0], koord[0])
    np.testing.assert_allclose(pos0[1], [0.1, 0.2 + 20.0, 0.3], atol=1e-12)


# --------------------------------------------------------------------------- Nachtrag 1: RF-N1 ..

D = 1e-3
DS1 = D * np.array(
    [
        [0.5, 1.0 * np.exp(1j * math.pi / 3.0), 0.3 * np.exp(-0.4j)],
        [
            0.2 * np.exp(0.2j),
            0.4 * np.exp(1j * (math.pi / 3.0 + math.pi / 2.0)),
            0.1 * np.exp(2.0j),
        ],
        [0.3 * np.exp(1.0j), 0.6 * np.exp(1j * (math.pi / 3.0 - math.pi)), 0.2 * np.exp(-1.0j)],
    ]
)
# Zeichen: Pivot-Komponente = Y (Index 1)


def _m(v: np.ndarray) -> np.ndarray:
    return np.cross(v.imag, v.real)


def test_rf_n1_rotation_voreinstellung_a() -> None:
    assert waehle_bezugskomponente(DS1[0]) == 1
    c_b, u_b = bezugsphase(DS1[0])
    assert c_b == 1
    assert abs(u_b) == pytest.approx(1.0, rel=1e-15)
    assert np.angle(u_b) == pytest.approx(math.pi / 3.0, abs=1e-12)
    w = relativ_gedreht(DS1, 0)
    soll = np.array(
        [
            [-1.0471975512, 0.0, -1.4471975512],
            [-0.8471975512, math.pi / 2.0, 0.9528024488],
            [-0.0471975512, math.pi, -2.0471975512],
        ]
    )
    np.testing.assert_allclose(_e(np.angle(w)), _e(soll), rtol=0, atol=1e-9)
    # exakte Sollwerte (geschlossene Ausdrücke) mit 1e-12
    exakt = np.angle(DS1) - math.pi / 3.0
    np.testing.assert_allclose(_e(np.angle(w)), _e(exakt), rtol=0, atol=1e-12)
    np.testing.assert_allclose(np.abs(w), np.abs(DS1), rtol=1e-12)
    assert w[0, 1].real == pytest.approx(1e-3, rel=1e-12)
    assert abs(w[0, 1].imag) < 1e-12 * 1e-3  # Pivot: bis auf Rundung reell und positiv
    # Positionen: d_0Y(θ_n)/(|v_0Y|/ω) = 0, 1, 0, -1; d_1Y = 1, 0, -1, 0
    d = auslenkung_amplitude(w, F_HZ)
    np.testing.assert_allclose(
        verschiebung(d[0, 1], TH_N) / (abs(DS1[0, 1]) / OMEGA), [0, 1, 0, -1], rtol=0, atol=1e-12
    )
    np.testing.assert_allclose(
        verschiebung(d[1, 1], TH_N) / (abs(DS1[1, 1]) / OMEGA), [1, 0, -1, 0], rtol=0, atol=1e-12
    )
    # reine Zeitverschiebung: d^w(θ) = d^v(θ - π/3) für 13 Stützstellen, alle p, c
    d_v = auslenkung_amplitude(DS1, F_HZ)
    np.testing.assert_allclose(
        verschiebung(d, TH_13),
        verschiebung(d_v, TH_13 - math.pi / 3.0),
        rtol=0,
        atol=1e-12 * D / OMEGA,
    )


def test_rf_n1b_bahn_bleibt_unveraendert() -> None:
    w = relativ_gedreht(DS1, 0)
    for gross, klein in zip(ellipse_kennwerte(w)[1:], ellipse_kennwerte(DS1)[1:], strict=True):
        np.testing.assert_allclose(gross, klein, rtol=1e-12)
    _, v_max, v_min = ellipse_kennwerte(DS1)
    np.testing.assert_allclose(v_max, [1.0399657157e-3, 4.3641466585e-4, 6.771649794e-4], rtol=1e-9)
    np.testing.assert_allclose(v_min, [5.084007377e-4, 1.3979356006e-4, 1.7733468559e-4], rtol=1e-9)
    np.testing.assert_allclose(_m(w), _m(DS1), rtol=1e-9, atol=1e-18)
    np.testing.assert_allclose(
        _m(DS1[0]), np.array([2.9771142, -0.58412751, -4.3301270]) * 1e-7, rtol=1e-6
    )
    # Auslenkung: Halbachsen / ω
    np.testing.assert_allclose(
        ellipse_kennwerte(auslenkung_amplitude(w, F_HZ))[1], v_max / OMEGA, rtol=1e-12
    )


def test_rf_n2_kreisbahn_bezugspunkt() -> None:
    v_b = D * np.array([1.0, 1j, 0.0])
    v_p = D * np.array([0.5, 0.5j * np.exp(0.3j), 0.2])
    v = np.stack([v_b, v_p])
    # A: Gleichstand X = Y, kleinster Index, ψ = 0
    assert waehle_bezugskomponente(v_b) == 0
    assert np.angle(bezugsphase(v_b)[1]) == pytest.approx(0.0, abs=1e-12)
    w = relativ_gedreht(v, 0)
    np.testing.assert_allclose(w[0], v_b, rtol=0, atol=1e-12 * D)
    d_b = auslenkung_amplitude(w[0], F_HZ)
    soll = np.array([[0, 1, 0], [1, 0, 0], [0, -1, 0], [-1, 0, 0]], dtype=float).T
    np.testing.assert_allclose(verschiebung(d_b, TH_N) / (D / OMEGA), soll, rtol=0, atol=1e-12)
    _, w_max, w_min = ellipse_kennwerte(w[0])
    np.testing.assert_allclose([w_max, w_min], [D, D], rtol=1e-12)
    np.testing.assert_allclose(_m(w[0]), [0.0, 0.0, -1e-6], rtol=0, atol=1e-18)
    # C(Y): ψ = π/2, ŵ_b = 1e-3 (-i, 1, 0), gleiche Kreisbahn um T/4 verschoben
    c_b, u_y = bezugsphase(v_b, 1)
    assert c_b == 1
    assert np.angle(u_y) == pytest.approx(math.pi / 2.0, abs=1e-12)
    w_y = relativ_gedreht(v, 0, 1)
    np.testing.assert_allclose(w_y[0], D * np.array([-1j, 1.0, 0.0]), rtol=0, atol=1e-12 * D)
    d_y = auslenkung_amplitude(w_y[0], F_HZ)
    soll_y = np.array([[-1, 0, 0], [0, 1, 0], [1, 0, 0], [0, -1, 0]], dtype=float).T
    np.testing.assert_allclose(verschiebung(d_y, TH_N) / (D / OMEGA), soll_y, rtol=0, atol=1e-12)
    # C(Z): ValueError (Betrag 0)
    with pytest.raises(ValueError, match="Betrag 0"):
        bezugsphase(v_b, 2)
    with pytest.raises(ValueError, match="Betrag 0"):
        relativ_gedreht(v, 0, 2)


def test_rf_n2_negativtest_komponentenweises_drehen_ist_falsch() -> None:
    """Alternative D (verboten) würde die Kreisbahn zur Linie machen; die Umsetzung nicht."""
    v_b = D * np.array([1.0, 1j, 0.0])
    v_p = D * np.array([0.5, 0.5j * np.exp(0.3j), 0.2])
    v = np.stack([v_b, v_p])
    faktor = np.where(
        np.abs(v_b) > 0.0, np.conj(v_b) / np.where(np.abs(v_b) > 0, np.abs(v_b), 1.0), 1.0
    )
    naiv = v * faktor
    np.testing.assert_allclose(naiv[0], D * np.array([1.0, 1.0, 0.0]), rtol=0, atol=1e-12 * D)
    np.testing.assert_allclose(ellipse_kennwerte(naiv[0])[1:], [math.sqrt(2) * D, 0.0], atol=1e-15)
    richtig = relativ_gedreht(v, 0)
    diff_richtig = np.angle(richtig[1, 1] * np.conj(richtig[1, 0]))
    diff_naiv = np.angle(naiv[1, 1] * np.conj(naiv[1, 0]))
    assert diff_richtig == pytest.approx(math.pi / 2.0 + 0.3, abs=1e-12)  # 1,8707963 rad
    assert diff_naiv == pytest.approx(0.3, abs=1e-12)
    assert abs(diff_richtig - diff_naiv) > 0.1
    # Halbachsen von p bleiben erhalten
    np.testing.assert_allclose(
        ellipse_kennwerte(richtig[1])[1:], ellipse_kennwerte(v[1])[1:], rtol=1e-12
    )


def test_rf_n3_lineares_b_reduziert_auf_fg04() -> None:
    v_b = D * np.exp(0.4j) * np.array([1.0, 1.0, 0.0])
    for komp in (None, 0, 1):
        c_b, u = bezugsphase(v_b, komp)
        assert np.angle(u) == pytest.approx(0.4, abs=1e-12)
        if komp is None:
            assert c_b == 0
    with pytest.raises(ValueError):
        bezugsphase(v_b, 2)
    # Einzelkomponente: identisch zur Formel aus FG-04 3.2 ŵ = v v_b^* / |v_b|
    v = np.stack([v_b, D * np.array([0.3, 0.7j, 0.1])])
    w3 = relativ_gedreht(v, 0, 0)
    w1 = relativ_gedreht(v[:, 0], 0)
    soll = v[:, 0] * np.conj(v[0, 0]) / abs(v[0, 0])
    np.testing.assert_allclose(w1, soll, rtol=1e-12, atol=0)
    np.testing.assert_allclose(w3[:, 0], w1, rtol=1e-12, atol=0)
    # Skalar als Bezug
    c_skalar, u_skalar = bezugsphase(v[0, 0])
    assert c_skalar == 0
    assert u_skalar == pytest.approx(np.exp(0.4j), abs=1e-12)


def test_rf_n4_polaritaet_und_kovarianz() -> None:
    w = relativ_gedreht(DS1, 0)
    # M8: v -> -v
    for komp in (None, 1):
        psi = np.angle(bezugsphase(DS1[0], komp)[1])
        psi_neg = np.angle(bezugsphase(-DS1[0], komp)[1])
        np.testing.assert_allclose(_e(np.array(psi_neg)), _e(np.array(psi - math.pi)), atol=1e-12)
        np.testing.assert_allclose(
            relativ_gedreht(-DS1, 0, komp), relativ_gedreht(DS1, 0, komp), rtol=0, atol=1e-12 * D
        )
    # gemeinsame Drehung e^{i*0,7}
    dreh = np.exp(0.7j) * DS1
    np.testing.assert_allclose(relativ_gedreht(dreh, 0), w, rtol=0, atol=1e-12 * D)
    np.testing.assert_allclose(
        auslenkung_amplitude(relativ_gedreht(-DS1, 0), F_HZ),
        auslenkung_amplitude(w, F_HZ),
        rtol=0,
        atol=1e-12 * D / OMEGA,
    )


def test_rf_n5_konsistenz_mit_2d_phase() -> None:
    w = relativ_gedreht(DS1, 0)  # Pivot Y
    phase_y = np.angle(w[:, 1])
    np.testing.assert_allclose(_e(phase_y), _e(phase_relativ_rad(DS1[:, 1], 0)), rtol=0, atol=1e-12)
    # Pivot X: konstanter Offset -π/3; Z: -1,4471975512 (gleich für alle p)
    for spalte, offset in ((0, -math.pi / 3.0), (2, -0.4 - math.pi / 3.0)):
        delta_2d = phase_relativ_rad(DS1[:, spalte], 0)
        np.testing.assert_allclose(
            _e(np.angle(w[:, spalte]) - delta_2d), _e(np.full(3, offset)), rtol=0, atol=1e-12
        )
    assert -0.4 - math.pi / 3.0 == pytest.approx(-1.4471975512, abs=1e-9)
    # B-Äquivalenz (Orakel im Test, nicht im Kern): ψ_B = ½ arg Σ v_b², Hauptachse reell
    psi_b = 0.5 * np.angle(np.sum(DS1[0] ** 2))
    assert abs(psi_b) == pytest.approx(0.9001846763, abs=1e-9) or abs(
        abs(psi_b) - math.pi
    ) == pytest.approx(0.9001846763, abs=1e-9)
    w_b = DS1[0] * np.exp(-1j * psi_b)
    assert abs(np.dot(w_b.real, w_b.imag)) < 1e-12 * D * D


def test_rf_n6_gleichstand_und_sprungverhalten() -> None:
    def v_b(r: float) -> np.ndarray:
        return D * np.array([1.0, r * np.exp(1.0j), 0.3 * np.exp(0.5j)])

    psi = {r: np.angle(bezugsphase(v_b(r))[1]) for r in (0.99, 1.01)}
    assert psi[0.99] == pytest.approx(0.0, abs=1e-12)  # X
    assert psi[1.01] == pytest.approx(1.0, abs=1e-12)  # Y
    assert psi[1.01] - psi[0.99] == pytest.approx(1.0, abs=1e-12)  # dokumentierter Sprung
    for r in (0.99, 1.01):  # C: stetig
        assert np.angle(bezugsphase(v_b(r), 0)[1]) == pytest.approx(0.0, abs=1e-12)
        assert np.angle(bezugsphase(v_b(r), 1)[1]) == pytest.approx(1.0, abs=1e-12)
    # exakt gleiche Beträge: kleinster Index
    assert waehle_bezugskomponente(D * np.array([1.0, -1.0, 0.3])) == 0
    assert waehle_bezugskomponente(D * np.array([0.3, 1.0, -1.0])) == 1
    assert waehle_bezugskomponente(D * np.array([-1.0, -1.0, -1.0])) == 0


def test_rf_n7_bezugspunkt_3d() -> None:
    alle = np.ones(3, dtype=bool)
    _, gross, _ = ellipse_kennwerte(DS1)
    assert gross[0] > gross[2] > gross[1]
    np.testing.assert_allclose(gross, [1.04e-3, 4.36e-4, 6.77e-4], rtol=1e-2)
    assert waehle_bezugspunkt_3d(DS1, alle) == 0
    np.testing.assert_allclose(np.linalg.norm(DS1, axis=1), [1.1576e-3, 4.58e-4, 7.0e-4], rtol=1e-2)
    # p0 in einer Komponente maskiert (A-1): p0 steht, Bezug ist p2
    koh = np.ones((3, 3), dtype=bool)
    koh[0, 2] = False
    bewegt = bewegt_maske(DS1, koh)
    np.testing.assert_array_equal(bewegt, [False, True, True])
    assert waehle_bezugspunkt_3d(DS1, bewegt) == 2
    # manuelle Wahl von p0 wird abgelehnt (A-2)
    with pytest.raises(ValueError, match="nicht animiert"):
        relativ_gedreht(DS1, 0, bewegt=bewegt)
    relativ_gedreht(DS1, 2, bewegt=bewegt)  # animierter Punkt ist erlaubt
    # alle v = 0 oder alle maskiert: kein Bezug
    assert waehle_bezugspunkt_3d(np.zeros((3, 3), dtype=np.complex128), alle) is None
    assert waehle_bezugspunkt_3d(DS1, np.zeros(3, dtype=bool)) is None
    # nicht endliche Amplitude: nie Bezug
    nan = DS1.copy()
    nan[0, 1] = complex(math.nan, math.nan)
    assert waehle_bezugspunkt_3d(nan, alle) == 2
    # Bezugspunkt mit v = 0 liefert keine Phase
    with pytest.raises(ValueError, match="v = 0"):
        waehle_bezugskomponente(np.zeros(3, dtype=np.complex128))
    with pytest.raises(ValueError, match="nicht endlich"):
        waehle_bezugskomponente(nan[0])
    with pytest.raises(ValueError, match="erwartet"):
        waehle_bezugskomponente(np.ones(2))
    # Gleichstand der Halbachsen: kleinster Index
    gleich = np.tile(np.array([[1.0, 0.0, 0.0]], dtype=np.complex128), (3, 1))
    assert waehle_bezugspunkt_3d(gleich, alle) == 0


# --------------------------------------------------------------------------- Korrektur K-AN2


def test_m1_bezugspunkt_muss_bei_animierter_amplitude_bewegt_sein() -> None:
    """A-2 (FG-04 Nachtrag 1): ein Bezugspunkt mit Komponente unter γ²_min ist abzulehnen."""
    v = 1e-3 * np.array([[1.0, 1j, 0.2], [0.5, 0.5, 0.0], [0.3, 0.1j, 0.2]])
    koh = np.ones((3, 3), dtype=bool)
    koh[0, 1] = False  # Bezugspunkt 0: Komponente Y unter γ²_min, damit steht der ganze Punkt still
    bewegt = bewegt_maske(v, koh)
    np.testing.assert_array_equal(bewegt, [False, True, True])
    with pytest.raises(ValueError, match="nicht animiert"):
        animierte_amplitude(v, F_HZ, bezug=0, bewegt=bewegt)
    d = animierte_amplitude(v, F_HZ, bezug=1, bewegt=bewegt)
    np.testing.assert_array_equal(d, auslenkung_amplitude(relativ_gedreht(v, 1), F_HZ))


def test_m3_maximum_theta_liefert_nie_2pi() -> None:
    phi = math.pi / 2.0 + 2e-16  # Rundungsfall: π/2 - φ ≈ -2e-16
    assert np.mod(math.pi / 2.0 - phi, 2.0 * math.pi) == 2.0 * math.pi  # bitgenau: der Fehlfall
    np.testing.assert_array_equal(maximum_theta(np.array([phi])), [0.0])
    np.testing.assert_array_equal(maximum_theta(np.array([2e-16]), "schnelle"), [0.0])
    phis = np.concatenate([np.linspace(-20.0, 20.0, 4001), [phi, -phi, 2e-16, -2e-16]])
    for groesse in ("auslenkung", "schnelle"):
        theta = maximum_theta(phis, groesse)
        assert np.all(theta >= 0.0)
        assert np.all(theta < 2.0 * math.pi)


@pytest.mark.filterwarnings("error::RuntimeWarning")
def test_n1_nan_und_inf_zeilen_ohne_runtimewarnung() -> None:
    nan = complex(math.nan, math.nan)
    inf = complex(math.inf, 0.0)
    v = np.array([1e-3 + 0j, nan, inf, 0.0 + 0j])
    v3 = np.array([[1e-3, 1e-3j, 0.0], [nan, 0j, 0j], [inf, 0j, 1e-3], [0j, 0j, 0j]])
    gueltig = np.array([True, False, False, True])
    # gültige Zeilen unverändert, ungültige bleiben nicht endlich
    d = auslenkung_amplitude(v, F_HZ)
    np.testing.assert_allclose(d[0], -1j * 1e-3 / OMEGA, rtol=1e-12, atol=0)
    assert not np.isfinite(d[1:3]).any()
    np.testing.assert_allclose(d[3], 0.0, atol=0)
    assert not np.isfinite(verschiebung(v, TH_N)[2]).all()
    assert np.isfinite(relativ_gedreht(v, 0)[0])
    assert np.isfinite(animierte_amplitude(v, F_HZ, bezug=0)[0])
    w3 = relativ_gedreht(v3, 0)
    assert np.isfinite(w3[0]).all()
    assert not np.isfinite(w3[1]).all()
    assert not np.isfinite(w3[2]).all()
    d3 = auslenkung_amplitude(v3, F_HZ)
    assert bezugsgroesse(d3, gueltig) == pytest.approx(bezugsgroesse(d3[:1], [True]), rel=1e-12)
    assert waehle_bezugspunkt_3d(v3, [True, False, True, True]) == 0
    theta = maximum_theta(np.array([math.inf, 0.1]))
    assert np.isnan(theta[0])
    assert theta[1] == pytest.approx(math.pi / 2.0 - 0.1, abs=1e-12)
    pos = positionen_m(np.zeros((4, 3)), d3, 0.3, 2.0, gueltig)
    np.testing.assert_array_equal(pos[1], [0.0, 0.0, 0.0])
    assert np.isfinite(pos[0]).all()


@pytest.mark.parametrize(
    ("s", "d_ref", "d_nn_min"),
    [
        (math.nan, 1e-6, 0.02),
        (-1.0, 1e-6, 0.02),
        (1.0, math.nan, 0.02),
        (1.0, -1e-6, 0.02),
        (1.0, 1e-6, math.nan),
        (1.0, 1e-6, -0.02),
    ],
)
def test_n3_ueberhoehung_hinweis_eingabepruefung(s: float, d_ref: float, d_nn_min: float) -> None:
    with pytest.raises(ValueError):
        ueberhoehung_hinweis(s, d_ref, d_nn_min)


def test_n3_ueberhoehung_hinweis_grenzfaelle_gueltig() -> None:
    assert ueberhoehung_hinweis(0.0, 1e-6, 0.02) is None
    assert ueberhoehung_hinweis(1.0, 0.0, 0.02) is None
    assert ueberhoehung_hinweis(1.0, 1e-6, 0.0) == HINWEIS_UEBERLAGERUNG


def test_n3_ueberhoehung_auto_prueft_alpha_vor_fruehabbruch() -> None:
    with pytest.raises(ValueError, match="alpha"):
        ueberhoehung_auto(None, A_MM, alpha=0.0)
    with pytest.raises(ValueError, match="alpha"):
        ueberhoehung_auto(0.029, None, alpha=math.nan)
    assert ueberhoehung_auto(None, A_MM, ALPHA_VORGABE) is None


def test_n3_relativ_gedreht_bezug_muss_ganzzahlig_sein() -> None:
    with pytest.raises(ValueError, match="ganze Zahl"):
        relativ_gedreht(np.ones(3), 1.0)  # type: ignore[arg-type]
