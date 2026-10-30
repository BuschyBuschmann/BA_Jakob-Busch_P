"""Referenzfälle FG-02 9.4: Einmassenschwinger (RF-P0 bis RF-P5) und zwei Moden (RF-M1 bis M4).

Algorithmus-Sollwerte aus dem Prüfskript im Anhang von FG-02 (ausgeführt im Paket W5-1 mit
voller Stellenzahl). Toleranzen nach FG-02: rtol 1e-9 (RF-P) bzw. 1e-6 (RF-M). Wo FG-02
einen Wert mit weniger Stellen angibt, als rtol verlangt (ζ achtstellig), gilt zusätzlich
atol = halbe letzte Stelle.
"""

from __future__ import annotations

import math

import aw_referenz as ref
import numpy as np
import numpy.typing as npt
import pytest

from ldv_automation.auswertung.annahmen import Annahmen, Schwellen
from ldv_automation.auswertung.spitzen import (
    AUFLOESUNGSBEGRENZT,
    GRENZE_VERFAHREN,
    GUELTIGKEIT_OFFEN_M7,
    HINWEIS_K_KLEIN,
    HINWEIS_OHNE_KOHAERENZ,
    KOHAERENZ_NIEDRIG,
    NACHBARMODE,
    UEBERLAPPEND,
    kandidaten,
    parabel,
    suche_spitzen,
)

OHNE_PROMINENZ = Schwellen(prominenz_min=None)


def _raster(df: float, off: float) -> npt.NDArray[np.float64]:
    anzahl = 128 if df > 1 else 800  # wie Prüfskript: bis 200 Hz
    return ((np.arange(1, anzahl + 1) + off) * df).astype(np.float64)


def test_rf_p0_analytische_werte() -> None:
    c = 2 * 0.01 * 1.0 * 2 * math.pi * 100.0
    assert c == pytest.approx(12.566370614, rel=1e-10)
    assert (2 * math.pi * 100.0) ** 2 == pytest.approx(394784.17604, rel=1e-10)
    y_max = abs(ref.mobilitaet_sdof(np.array([100.0]))[0])
    assert y_max == pytest.approx(1 / c, rel=1e-12)
    assert y_max == pytest.approx(0.0795774715, rel=1e-9)
    f1, f2 = 99.004999875, 101.004999875
    y12 = np.abs(ref.mobilitaet_sdof(np.array([f1, f2])))
    np.testing.assert_allclose(y12, y_max / math.sqrt(2), rtol=1e-9)
    assert f2 - f1 == pytest.approx(2.0, rel=1e-12)


@pytest.mark.parametrize(
    ("rf", "zeta", "df", "off", "f_sp", "hoehe", "breite", "z", "kennzeichen"),
    [
        ("RF-P1", 0.01, 0.25, 0.0, 100.000298644, 7.957747494e-2, 2.000591366, 0.010002927, ()),
        ("RF-P2", 0.01, 0.25, 0.37, 100.002070830, 7.953876069e-2, 2.008976145, 0.010044673, ()),
        (
            "RF-P3",
            0.005,
            1.5625,
            0.0,
            100.002427267,
            0.1591552101,
            1.316512038,
            0.006582400,
            (AUFLOESUNGSBEGRENZT,),
        ),
        (
            "RF-P4",
            0.005,
            1.5625,
            0.37,
            100.303481217,
            0.1058309032,
            2.095705355,
            0.010446823,
            (AUFLOESUNGSBEGRENZT,),
        ),
    ],
)
def test_rf_p1_bis_p4_einmassenschwinger(
    rf: str,
    zeta: float,
    df: float,
    off: float,
    f_sp: float,
    hoehe: float,
    breite: float,
    z: float,
    kennzeichen: tuple[str, ...],
) -> None:
    f = _raster(df, off)
    y = np.abs(ref.mobilitaet_sdof(f, zeta=zeta))
    erg = suche_spitzen(f, y, kohaerenz=np.ones_like(y))
    assert len(erg.spitzen) == 1, rf
    s = erg.spitzen[0]
    assert s.f_sp_hz == pytest.approx(f_sp, rel=1e-9), rf
    assert s.hoehe == pytest.approx(hoehe, rel=1e-9), rf
    assert s.breite_3db_hz == pytest.approx(breite, rel=1e-9), rf
    assert s.zeta == pytest.approx(z, rel=1e-9, abs=5e-10), rf
    assert s.zeta == pytest.approx(s.breite_3db_hz / (2 * s.f_sp_hz), rel=1e-15)
    assert s.q == pytest.approx(s.f_sp_hz / s.breite_3db_hz, rel=1e-15)
    assert s.kennzeichen == kennzeichen, rf
    assert erg.delta_f_hz == pytest.approx(df, rel=1e-12)


def test_rf_p1_gegen_physikalische_wahrheit() -> None:
    f = _raster(0.25, 0.0)
    s = suche_spitzen(f, np.abs(ref.mobilitaet_sdof(f))).spitzen[0]
    assert abs(s.breite_3db_hz / 2.0 - 1.0) <= 0.005
    assert abs(s.f_sp_hz - 100.0) <= 0.01 * 0.25


def test_rf_p5_fuenfzig_rasterlagen() -> None:
    """RF-P5 nach FG-02 9.4 (Korrektur K1-2): max|f_sp - 100| = 0,00954 Δf (<= 0,010 Δf);
    B - 2 in [0; +0,005364·2] Hz, Maximum +0,005364·2 Hz mit Toleranz 1e-6·2 Hz.
    """
    df = 0.25
    fehler_f = []
    fehler_b = []
    for off in np.linspace(0, 1, 50, endpoint=False):
        f = _raster(df, float(off))
        erg = suche_spitzen(f, np.abs(ref.mobilitaet_sdof(f)))
        assert len(erg.spitzen) == 1
        s = erg.spitzen[0]
        assert s.kennzeichen == ()
        fehler_f.append(abs(s.f_sp_hz - 100.0))
        fehler_b.append(s.breite_3db_hz - 2.0)
    assert max(fehler_f) <= 0.010 * df  # Prüfskript: 0,009538 Δf
    assert min(fehler_b) >= 0.0
    assert max(fehler_b) == pytest.approx(0.005364 * 2.0, abs=1e-6 * 2.0)


# Prüfskript FG-02 (RF-M), volle Stellenzahl
RF_M: dict[str, tuple[float, list[tuple[float, float, tuple[str, ...]]]]] = {
    "RF-M1": (101.0, [(100.315041369198, 3.037501853481, ())]),
    "RF-M2": (
        103.0,
        [
            (99.844888943907, 2.048914031079, (NACHBARMODE,)),
            (103.165646560764, 2.135187090995, (NACHBARMODE,)),
        ],
    ),
    "RF-M3": (
        106.0,
        [
            (99.871086271581, 1.992936444035, ()),
            (106.151108115259, 2.132966986506, (NACHBARMODE,)),
        ],
    ),
    "RF-M4": (
        120.0,
        [(99.955499995409, 1.996776801400, ()), (120.076234031781, 2.406106288102, ())],
    ),
}
# FG-02-Tabelle, vierstellig
RF_M_TABELLE = {
    "RF-M1": [(100.3150, 3.0375)],
    "RF-M2": [(99.8449, 2.0489), (103.1656, 2.1352)],
    "RF-M3": [(99.8711, 1.9929), (106.1511, 2.1330)],
    "RF-M4": [(99.9555, 1.9968), (120.0762, 2.4061)],
}


@pytest.mark.parametrize("rf", list(RF_M))
def test_rf_m_zwei_moden(rf: str) -> None:
    f2, soll = RF_M[rf]
    f = (np.arange(1, 3000) * 0.05).astype(np.float64)
    y = np.abs(ref.mobilitaet_moden(f, [100.0, f2]))
    erg = suche_spitzen(f, y, schwellen=OHNE_PROMINENZ)
    assert len(erg.spitzen) == len(soll), rf
    for s, (f_sp, breite, kz), (f4, b4) in zip(erg.spitzen, soll, RF_M_TABELLE[rf], strict=True):
        assert s.f_sp_hz == pytest.approx(f_sp, rel=1e-6), rf
        assert s.breite_3db_hz == pytest.approx(breite, rel=1e-6), rf
        assert s.f_sp_hz == pytest.approx(f4, abs=5e-5), rf
        assert s.breite_3db_hz == pytest.approx(b4, abs=5e-5), rf
        assert s.kennzeichen == kz, rf
    assert GRENZE_VERFAHREN in erg.grenzen


def test_kandidaten_randlinien_und_f_min() -> None:
    f = np.arange(1.0, 8.0)
    y = np.array([5.0, 1.0, 3.0, 1.0, 1.0, 2.0, 9.0])
    assert kandidaten(y, f, prominenz_min=None) == [2]
    assert kandidaten(y, f, prominenz_min=None, f_min_hz=4.0) == []
    assert kandidaten(y, f, prominenz_min=4.0, fenster_linien=2) == []
    assert kandidaten(y, f, prominenz_min=3.0, fenster_linien=2) == [2]


def test_parabel_nenner_nicht_negativ() -> None:
    assert parabel(np.array([1.0, 2.0, 3.0]), 1) == (0.0, 2.0)


def test_k_kleiner_drei() -> None:
    erg = suche_spitzen(np.array([1.0, 2.0]), np.array([1.0, 2.0]))
    assert erg.spitzen == () and erg.hinweise == (HINWEIS_K_KLEIN,)


def test_ueberlappend_am_achsenende_und_kohaerenz_niedrig_und_m7() -> None:
    f = (np.arange(1, 13) * 100.0).astype(np.float64)
    y = np.array([1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.5, 4.0, 3.9])
    g2 = np.ones(12)
    g2[10] = 0.5
    erg = suche_spitzen(f, y, kohaerenz=g2, schwellen=OHNE_PROMINENZ)
    (s,) = erg.spitzen
    assert UEBERLAPPEND in s.kennzeichen and math.isnan(s.breite_3db_hz) and math.isnan(s.q)
    assert math.isnan(s.f_r_hz) and math.isfinite(s.f_l_hz)
    assert KOHAERENZ_NIEDRIG in s.kennzeichen
    assert GUELTIGKEIT_OFFEN_M7 in s.kennzeichen
    ohne_m7 = suche_spitzen(f, y, schwellen=OHNE_PROMINENZ, annahmen=Annahmen(m7_grenze_hz=None))
    assert GUELTIGKEIT_OFFEN_M7 not in ohne_m7.spitzen[0].kennzeichen
    assert HINWEIS_OHNE_KOHAERENZ in ohne_m7.hinweise


def test_ueberlappend_durch_lokales_minimum() -> None:
    f = np.arange(1.0, 10.0)
    y = np.array([0.1, 1.0, 0.9, 1.0, 3.0, 1.0, 0.9, 1.0, 0.1])
    s = suche_spitzen(f, y, schwellen=OHNE_PROMINENZ).spitzen
    mitte = next(x for x in s if x.k == 4)
    assert UEBERLAPPEND not in mitte.kennzeichen  # Schwelle wird vor dem Minimum unterschritten
    hoch = np.array([0.1, 3.0, 2.9, 3.0, 4.0, 3.0, 2.9, 3.0, 0.1])
    s2 = suche_spitzen(f, hoch, schwellen=OHNE_PROMINENZ).spitzen
    assert UEBERLAPPEND in next(x for x in s2 if x.k == 4).kennzeichen


def test_eingabefehler() -> None:
    f = np.arange(1.0, 5.0)
    with pytest.raises(ValueError, match="Betrag"):
        suche_spitzen(f, np.ones(4, dtype=np.complex128))
    with pytest.raises(ValueError, match="Achse"):
        suche_spitzen(f, np.ones(3))
    with pytest.raises(ValueError, match=">= 0"):
        suche_spitzen(f, -np.ones(4))
    with pytest.raises(ValueError, match="kohaerenz"):
        suche_spitzen(f, np.ones(4), kohaerenz=np.ones(3))


def test_nan_im_eingang_ergibt_keine_spitze() -> None:
    f = np.arange(1.0, 6.0)
    erg = suche_spitzen(f, np.array([0.1, np.nan, 1.0, 0.2, 0.1]), schwellen=OHNE_PROMINENZ)
    assert all(s.k != 1 for s in erg.spitzen)
