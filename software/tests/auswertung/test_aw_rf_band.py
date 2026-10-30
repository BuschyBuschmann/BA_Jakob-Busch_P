"""Referenzfälle FG-02 9.1: Skalierung und Band-RMS (RF-S1 bis RF-S3, RF-B1 bis RF-B9).

Toleranzen wie in FG-02 9.1 angegeben: rtol 1e-12 bei exakten (Parseval-)Werten (nur
Gleitkommarundung), rtol 1e-9 bei Algorithmus-Sollwerten mit zehn gültigen Stellen. Wo
FG-02 einen exakten Wert auf zehn Nachkommastellen gerundet angibt (z. B. 1,4142135624 =
√2), wird gegen die geschlossene Form verglichen, denn die Rundung (bis 3·10⁻¹¹) liegt über
rtol 1e-12.
"""

from __future__ import annotations

import math

import aw_referenz as ref
import numpy as np
import pytest

from ldv_automation.auswertung.annahmen import Annahmen
from ldv_automation.auswertung.baender import (
    HINWEIS_ABGESCHNITTEN,
    HINWEIS_BANDNORM,
    HINWEIS_LEER,
    band_amplitude,
    band_ap,
    band_frf,
    band_linien,
    w_rbw_aus_fenster,
)

F = ref.FREQUENZ_HZ
DF = ref.DF_HZ
A = 2.0
PHI = math.pi / 3


@pytest.mark.parametrize("fenster", [ref.RECHTECK, ref.HANN], ids=["rechteck", "hann"])
def test_rf_s1_sinus_auf_linie_ergibt_spitzenwert_mit_phase(fenster: np.ndarray) -> None:
    x = ref.spektrum(ref.sinus(A, 64, PHI), fenster)
    # Linie 64 = Arrayindex 63 (k0 = 1); 100 Hz
    assert F[63] == pytest.approx(100.0, rel=1e-15)
    np.testing.assert_allclose(x[63], 1.0 + 1j * math.sqrt(3.0), rtol=1e-12)  # 1 + 1,7320508076i
    assert abs(x[63]) == pytest.approx(2.0, rel=1e-12)
    assert np.angle(x[63]) == pytest.approx(math.pi / 3, rel=1e-12)


@pytest.mark.parametrize(
    ("fenster", "soll"),
    [(ref.RECHTECK, 1.2752815250), (ref.HANN, 1.6976528729)],
    ids=["rechteck", "hann"],
)
def test_rf_s2_sinus_zwischen_linien(fenster: np.ndarray, soll: float) -> None:
    x = ref.spektrum(ref.sinus(A, 64.5, PHI), fenster)
    assert np.max(np.abs(x)) == pytest.approx(soll, rel=1e-9)


def test_rf_s3_w_rbw_der_fenster() -> None:
    assert w_rbw_aus_fenster(ref.RECHTECK) == pytest.approx(1.0, rel=1e-12)
    assert w_rbw_aus_fenster(ref.HANN) == pytest.approx(1.5, rel=1e-12)


def test_w_rbw_ungueltiges_fenster() -> None:
    with pytest.raises(ValueError, match="Fenster"):
        w_rbw_aus_fenster(np.zeros(4))


@pytest.mark.parametrize(
    ("fenster", "w_rbw"), [(ref.RECHTECK, 1.0), (ref.HANN, 1.5)], ids=["rechteck", "hann"]
)
def test_rf_b1_band_um_linie_ist_exakt(fenster: np.ndarray, w_rbw: float) -> None:
    x = ref.spektrum(ref.sinus(A, 64, PHI), fenster)
    b = band_amplitude(x, F, 61 * DF, 67 * DF, annahmen=Annahmen(w_rbw=w_rbw))
    assert b.rms is not None
    assert float(b.rms) == pytest.approx(2.0 / math.sqrt(2.0), rel=1e-12)
    assert b.n_linien == 7
    assert b.hinweise == ()


def test_rf_b2_geschlossenes_band_nur_eine_linie() -> None:
    x = ref.spektrum(ref.sinus(A, 64, PHI), ref.RECHTECK)
    b = band_amplitude(x, F, 100.0, 100.0)
    assert b.n_linien == 1
    assert b.rms is not None and float(b.rms) == pytest.approx(math.sqrt(2.0), rel=1e-12)


def test_rf_b3_leeres_band() -> None:
    x = ref.spektrum(ref.sinus(A, 64, PHI), ref.RECHTECK)
    b = band_amplitude(x, F, 100.1, 100.2)
    assert b.rms is not None and b.rms_psv is not None
    assert np.isnan(b.rms) and np.isnan(b.rms_psv)
    assert b.n_linien == 0
    assert HINWEIS_LEER in b.hinweise


@pytest.mark.parametrize(
    ("halb", "soll"), [(3, 1.3722894714), (10, 1.4006918958), (50, 1.4122824908)]
)
def test_rf_b4_rechteck_sinus_zwischen_linien(halb: int, soll: float) -> None:
    x = ref.spektrum(ref.sinus(A, 64.5, PHI), ref.RECHTECK)
    b = band_amplitude(x, F, (64 - halb) * DF, (64 + halb) * DF)
    assert b.rms is not None and float(b.rms) == pytest.approx(soll, rel=1e-9)


@pytest.mark.parametrize(("halb", "soll"), [(3, 1.4141638634), (10, 1.4142134072)])
def test_rf_b5_hann_sinus_zwischen_linien(halb: int, soll: float) -> None:
    x = ref.spektrum(ref.sinus(A, 64.5, PHI), ref.HANN)
    b = band_amplitude(x, F, (64 - halb) * DF, (64 + halb) * DF, annahmen=Annahmen(w_rbw=1.5))
    assert b.rms is not None and float(b.rms) == pytest.approx(soll, rel=1e-9)


@pytest.mark.parametrize(
    ("f_u", "f_o", "soll"),
    [
        (90.0, 110.0, math.sqrt(2.0)),  # 1,4142135624
        (990.0, 1010.0, 0.5 / math.sqrt(2.0)),  # 0,3535533906
        (0.0, 2500.0, math.sqrt(2.0 + 0.125)),  # 1,4577379737
    ],
)
def test_rf_b6_zwei_sinus(f_u: float, f_o: float, soll: float) -> None:
    x = ref.spektrum(ref.sinus(2.0, 64) + ref.sinus(0.5, 640, 1.0), ref.RECHTECK)
    b = band_amplitude(x, F, f_u, f_o)
    assert b.rms is not None and float(b.rms) == pytest.approx(soll, rel=1e-12)


def test_rf_b6_band_ab_null_ist_abgeschnitten() -> None:
    x = ref.spektrum(ref.sinus(2.0, 64), ref.RECHTECK)
    assert HINWEIS_ABGESCHNITTEN in band_amplitude(x, F, 0.0, 2500.0).hinweise


def test_rf_b7_untere_grenze_groesser_obere() -> None:
    with pytest.raises(ValueError, match="f_u"):
        band_amplitude(np.ones(F.size), F, 200.0, 100.0)


def test_rf_b8_frf_bandnorm() -> None:
    f = np.array([1.0, 2.0, 3.0, 4.0, 5.0, 6.0])
    h = np.array([5.0, 1.0, 1.0, 1.0, 1.0, 5.0], dtype=np.complex128)
    b = band_frf(h, f, 2.0, 5.0)
    assert b.bandnorm is not None and float(b.bandnorm) == pytest.approx(math.sqrt(2.0), rel=1e-12)
    assert b.rms is None and b.rms_psv is None
    assert HINWEIS_BANDNORM in b.hinweise


def test_rf_b9_rms_psv_fuer_ap() -> None:
    f = np.array([1.0, 2.0, 3.0, 4.0])
    b = band_ap(np.array([4.0, 4.0, 4.0, 100.0]), f, 1.0, 3.0)
    assert b.rms_psv is not None and float(b.rms_psv) == 6.0
    assert b.rms is not None and float(b.rms) == pytest.approx(
        math.sqrt(6.0), rel=1e-15
    )  # √(ΣAP/2)


def test_band_ap_lehnt_komplex_ab() -> None:
    with pytest.raises(TypeError):
        band_ap(np.ones(3, dtype=np.complex128), np.array([1.0, 2.0, 3.0]), 1.0, 3.0)


def test_rms_gleich_rms_psv_bei_w_rbw_1_und_je_punkt() -> None:
    x = np.array([[1.0, 2.0, 3.0], [0.0, 1.0, 0.0]])
    b = band_amplitude(x, np.array([1.0, 2.0, 3.0]), 1.0, 3.0, bezug="t", einheit="m/s")
    assert b.rms is not None and b.rms_psv is not None
    np.testing.assert_allclose(b.rms, b.rms_psv, rtol=0, atol=0)
    np.testing.assert_allclose(b.rms, [math.sqrt(14 / 2), math.sqrt(1 / 2)], rtol=1e-15)


def test_bandregel_offen_schliesst_grenzlinien_aus() -> None:
    f = np.array([100.0, 150.0, 200.0])
    maske, _ = band_linien(f, 100.0, 200.0, regel="offen")
    assert maske.tolist() == [False, True, False]
    maske, _ = band_linien(f, 100.0, 200.0)
    assert maske.tolist() == [True, True, True]
    with pytest.raises(ValueError, match="Bandregel"):
        band_linien(f, 100.0, 200.0, regel="halb")  # type: ignore[arg-type]


def test_band_ganz_ausserhalb_ist_leer_und_achse_mit_einer_linie_braucht_delta_f() -> None:
    f = np.array([100.0])
    with pytest.raises(ValueError, match="delta_f"):
        band_linien(f, 0.0, 10.0)
    maske, hinweise = band_linien(f, 0.0, 10.0, delta_f_hz=1.0)
    assert not maske.any() and hinweise == (HINWEIS_LEER,)


def test_band_falsche_laenge() -> None:
    with pytest.raises(ValueError, match="letzte Achse"):
        band_amplitude(np.ones(4), np.array([1.0, 2.0, 3.0]), 1.0, 3.0)


def test_band_nan_wird_weitergegeben() -> None:
    b = band_amplitude(np.array([1.0, np.nan, 1.0]), np.array([1.0, 2.0, 3.0]), 1.0, 3.0)
    assert b.rms is not None and np.isnan(b.rms)
