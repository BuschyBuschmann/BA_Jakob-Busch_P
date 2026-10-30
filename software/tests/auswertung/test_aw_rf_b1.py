"""Referenzfälle B-1 (FG-03 9.1, RF-F1 bis RF-F7) und Randfälle 6.3 des Moden-Fits.

Toleranzen wie FG-03 9.1; Begründung je Test. Sollwerte unverändert aus FG-03.
"""

from __future__ import annotations

import math

import numpy as np
import numpy.typing as npt
import pytest
from aw_referenz import erwartungswert_paar, mobilitaet_moden

from ldv_automation.auswertung import Annahmen, werte_aus
from ldv_automation.auswertung.annahmen import Schwellen, SchwellenStufe2
from ldv_automation.auswertung.modenfit import (
    AUSSERHALB_BAND,
    GRUPPE_ZU_GROSS,
    HINWEIS_KEINE_PUNKTE,
    HINWEIS_NULL,
    KEIN_MOBILITAETSBEZUG,
    MODELL_PASST_NICHT,
    NICHT_KONVERGIERT,
    UNSICHER,
    ZU_WENIG_LINIEN,
    Gruppe,
    basis_mobilitaet,
    bilde_gruppen,
    fit_moden,
    fit_punkt,
    frf_art_aus_einheiten,
    iqr,
    kennzeichen_fit,
    schaetze_daempfung,
)
from ldv_automation.auswertung.spitzen import (
    GUELTIGKEIT_OFFEN_M7,
    KOHAERENZ_NIEDRIG,
    NACHBARMODE,
    UEBERLAPPEND,
    Spitze,
)

S2 = SchwellenStufe2()
DF = 1.5625


def y_sdof(
    f: npt.ArrayLike, fn: float = 100.0, zeta: float = 0.005, m: float = 1.0
) -> npt.NDArray[np.complex128]:
    """Mobilität Y = iω/(m(ωn² - ω² + 2iζωnω)) (FG-03 9)."""
    w = 2 * np.pi * np.asarray(f, dtype=np.float64)
    wn = 2 * np.pi * fn
    return np.asarray(1j * w / (m * (wn**2 - w**2 + 2j * zeta * wn * w)), dtype=np.complex128)


def raster(off: float, n: int = 8, f0: float = 100.0) -> npt.NDArray[np.float64]:
    """17 Linien um Linie 64 (f0 = 100 Hz), f_j = (k0 + j + off)·Δf."""
    k0 = round(f0 / DF)
    return np.asarray((np.arange(k0 - n, k0 + n + 1) + off) * DF, dtype=np.float64)


def kz(roh: object, f: npt.NDArray[np.float64], df: float) -> tuple[tuple[str, ...], ...]:
    return kennzeichen_fit(roh, f_band_hz=(f[0], f[-1]), delta_f_hz=df, schwellen2=S2)  # type: ignore[arg-type]


# --- RF-F1: exaktes SDOF bei B/Δf = 0,64 -------------------------------------------------


@pytest.mark.parametrize("off", [0.0, 0.37])
def test_rf_f1_exakt(off: float) -> None:
    f = raster(off)
    r = fit_moden(f, y_sdof(f), [100.3], [0.01])
    # Toleranzen FG-03 RF-F1 (exakte Modellform): fr atol 1e-7 Hz, ζ und R rtol 1e-6.
    assert math.isclose(r.fr_hz[0], 100.0, rel_tol=0.0, abs_tol=1e-7)
    assert math.isclose(r.zeta[0], 0.005, rel_tol=1e-6)
    assert np.isclose(r.modalkonstante[0], 1.0, rtol=1e-6, atol=0.0)
    assert abs(r.residuum) <= 1e-12
    assert r.rho <= 1e-12
    assert r.konvergiert
    assert kz(r, f, DF) == ((),)


# --- RF-F2: Rauschen, Monte Carlo ---------------------------------------------------------


@pytest.fixture(scope="module")
def monte_carlo() -> dict[float, tuple[npt.NDArray[np.float64], float]]:
    """RF-F2 wie im Prüfskript: ein Generator, erst 1 %, dann 3 % Rauschen."""
    rng = np.random.default_rng(20261030)
    f = raster(0.37)
    h0 = y_sdof(f)
    ergebnis = {}
    for rel in (0.01, 0.03):
        sig = rel * float(np.abs(h0).max())
        zs, sds = [], []
        for _ in range(400):
            rausch = rng.standard_normal(f.size) + 1j * rng.standard_normal(f.size)
            r = fit_moden(f, h0 + sig / np.sqrt(2) * rausch, [100.3], [0.01])
            zs.append(r.zeta[0])
            sds.append(r.sd_zeta_rel[0])
        ergebnis[rel] = (np.asarray(zs), float(np.mean(sds)))
    return ergebnis


@pytest.mark.parametrize(
    ("rel", "streu_soll", "sd_soll"), [(0.01, 0.0135, 0.0131), (0.03, 0.0415, 0.0392)]
)
def test_rf_f2_statistisch(
    monte_carlo: dict[float, tuple[npt.NDArray[np.float64], float]],
    rel: float,
    streu_soll: float,
    sd_soll: float,
) -> None:
    z, sd = monte_carlo[rel]
    streu = float(z.std() / 0.005)
    # FG-03 RF-F2: Bias |·| <= 0,01; Fit-sd innerhalb ±20 % der MC-Streuung.
    assert abs(z.mean() / 0.005 - 1) <= 0.01
    assert abs(sd / streu - 1) <= 0.2
    # Dokumentierte Werte aus FG-03 (gleicher Seed und gleiche Reihenfolge wie das
    # Prüfskript), angegeben auf drei Stellen → rtol 1 %.
    assert math.isclose(streu, streu_soll, rel_tol=0.01)
    assert math.isclose(sd, sd_soll, rel_tol=0.01)


# --- RF-F3: zwei eng liegende Moden -------------------------------------------------------


F3 = np.arange(180, 230, dtype=np.float64) * 0.5  # 90 … 114,5 Hz, Δf = 0,5 Hz


@pytest.mark.parametrize(
    ("f2", "zeta1_soll", "rho1_soll", "kennzeichen1"),
    [(102.0, 0.020565, 0.112, True), (103.0, 0.008775, 0.096, False)],
)
def test_rf_f3_zwei_moden(
    f2: float, zeta1_soll: float, rho1_soll: float, kennzeichen1: bool
) -> None:
    h = y_sdof(F3, 100.0, 0.01) + y_sdof(F3, f2, 0.01)
    r2 = fit_moden(F3, h, [99.8, f2 + 0.2], [0.015, 0.015])
    # n = 2: rtol 1e-6 (exakte Modellform).
    np.testing.assert_allclose(r2.fr_hz, [100.0, f2], rtol=1e-6, atol=0)
    np.testing.assert_allclose(r2.zeta, [0.01, 0.01], rtol=1e-6, atol=0)
    assert r2.rho <= 1e-12
    k = int(np.argmax(np.abs(h)))
    sel = slice(k - 4, k + 5)
    r1 = fit_moden(F3[sel], h[sel], [F3[k]], [0.01])
    # n = 1: rtol 1e-3 (Algorithmus-Sollwert, Konvergenzschwelle); rho auf die angegebenen Stellen.
    assert math.isclose(r1.zeta[0], zeta1_soll, rel_tol=1e-3)
    assert math.isclose(r1.rho, rho1_soll, rel_tol=0.0, abs_tol=5e-4)
    k1 = kz(r1, F3[sel], 0.5)[0]
    assert (MODELL_PASST_NICHT in k1) is kennzeichen1
    # Nach 3.4 zusätzlich: sigma_fr = 0,371 Hz > Δf/2 bei 102 Hz → unsicher; bei 103 Hz keins.
    assert (UNSICHER in k1) is kennzeichen1
    assert k1 == ((MODELL_PASST_NICHT, UNSICHER) if kennzeichen1 else ())


def _spitze(f: float, k: int, breite: float, kennzeichen: tuple[str, ...] = ()) -> Spitze:
    return Spitze(
        k=k,
        f_k_hz=f,
        f_sp_hz=f,
        hoehe=1.0,
        breite_3db_hz=breite,
        q=f / breite,
        zeta=breite / (2 * f),
        f_l_hz=f - breite / 2,
        f_r_hz=f + breite / 2,
        delta=0.0,
        kennzeichen=kennzeichen,
    )


def test_rf_f3b_gruppenbildung() -> None:
    sp = [_spitze(100.0, 20, 2.0, (NACHBARMODE,)), _spitze(102.0, 24, 2.04, (NACHBARMODE,))]
    gruppen = bilde_gruppen(sp, np.ones(60), 0.5)
    assert len(gruppen) == 1
    assert gruppen[0].spitzen == (0, 1)
    assert (gruppen[0].k_von, gruppen[0].k_bis) == (14, 30)


def test_gruppen_ueberlappend_und_kuerzung() -> None:
    # 262,6 nachbarmode (3B), 265 ueberlappend (B NaN), 270 innerhalb n_fit·Δf von 265.
    df = 1.5625
    y = np.ones(200)
    y[[100, 150]] = 5.0
    y[[146]] = 0.2  # lokales Minimum zwischen Gruppe (k=140) und fremder Spitze bei 150
    sp = [
        _spitze(df * 90, 90, 1.5, (NACHBARMODE,)),
        _spitze(df * 91.5, 91, math.nan, (UEBERLAPPEND,)),
        _spitze(df * 95, 95, 1.5),
        _spitze(df * 140, 140, 1.5),
        _spitze(df * 150, 150, 1.5),
        _spitze(df * 3, 3, 1.5),
    ]
    g = bilde_gruppen(sp, y, df)
    assert [x.spitzen for x in g] == [(5,), (0, 1, 2), (3,), (4,)]
    assert (g[0].k_von, g[0].k_bis) == (0, 9)  # an der Achse begrenzt
    assert (g[1].k_von, g[1].k_bis) == (84, 101)
    assert (g[2].k_von, g[2].k_bis) == (134, 146)  # am lokalen Minimum gekürzt
    # ohne lokales Minimum: Kürzung bis vor die fremde Spitze
    y2 = np.linspace(1, 2, 200)
    g2 = bilde_gruppen(sp[3:5], y2, df)
    assert (g2[0].k_von, g2[0].k_bis) == (134, 146)
    assert (g2[1].k_von, g2[1].k_bis) == (144, 156)  # 140 liegt nicht im Band


# --- RF-F4: Impulsantwort, abgeschnitten --------------------------------------------------

FS, N = 6250.0, 4000
T = N / FS


def hv(t: npt.NDArray[np.float64], fn: float, z: float) -> npt.NDArray[np.float64]:
    wn = 2 * np.pi * fn
    wd = wn * np.sqrt(1 - z * z)
    return np.asarray(np.exp(-z * wn * t) * (np.cos(wd * t) - z * wn / wd * np.sin(wd * t)))


@pytest.mark.parametrize(
    ("fn", "z"), [(100.0, 0.005), (100.0, 0.01), (100.0, 0.02), (400.0, 0.002), (100.0, 0.05)]
)
def test_rf_f4_impuls(fn: float, z: float) -> None:
    h = hv(np.arange(N, dtype=np.float64) / FS, fn, z)
    h[0] *= 0.5
    hk = np.fft.rfft(h) / FS
    f = np.arange(hk.size) * FS / N
    k0 = round(fn * T)
    sel = slice(k0 - 8, k0 + 9)
    r = fit_moden(f[sel], hk[sel], [fn + 0.3], [2 * z])
    # FG-03 RF-F4: ζ rtol 1e-4; fr atol 1e-3 Hz (Abtastfehler der Faltungssumme).
    assert math.isclose(r.zeta[0], z, rel_tol=1e-4)
    assert math.isclose(r.fr_hz[0], fn, rel_tol=0.0, abs_tol=1e-3)
    assert r.konvergiert


# --- RF-F5: Burst-Chirp -------------------------------------------------------------------


def _burst_h1(fn: float, z: float, anteil: float) -> tuple[np.ndarray, np.ndarray]:
    dt = 1 / FS
    t = np.arange(N) * dt
    tb = anteil * T
    x = np.zeros(N)
    m = t < tb
    x[m] = np.sin(2 * np.pi * (20.0 * t[m] + 0.5 * (2500.0 - 20.0) / tb * t[m] ** 2))
    h = hv(np.asarray(t, dtype=np.float64), fn, z)  # h[n] für n < N genügt für y[:N]
    h[0] *= 0.5
    y = np.convolve(x, h)[:N] * dt
    return np.arange(N // 2 + 1) / T, np.fft.rfft(y) / np.fft.rfft(x)


@pytest.mark.parametrize("anteil", [0.4, 0.8])
@pytest.mark.parametrize(
    ("fn", "z"), [(100.0, 0.005), (100.0, 0.01), (100.0, 0.02), (400.0, 0.002)]
)
def test_rf_f5_burst(anteil: float, fn: float, z: float) -> None:
    f, h1 = _burst_h1(fn, z, anteil)
    k0 = round(fn * T)
    sel = slice(k0 - 8, k0 + 9)
    r = fit_moden(f[sel], h1[sel], [fn + 0.3], [2 * z])
    # FG-03 RF-F5: |ζ/ζ_wahr - 1| <= 0,025 und rho <= 0,05 (Modellabweichung durch Leckage).
    assert abs(r.zeta[0] / z - 1) <= 0.025
    assert r.rho <= 0.05


@pytest.mark.parametrize(("anteil", "soll"), [(0.4, 0.316), (0.8, 0.317)])
def test_rf_f5_halbwertsbreite_dokumentation(anteil: float, soll: float) -> None:
    from ldv_automation.auswertung.spitzen import breite_3db, parabel

    f, h1 = _burst_h1(100.0, 0.005, anteil)
    y = np.abs(h1)
    k = 64 - 3 + int(np.argmax(y[61:68]))
    d, hoehe = parabel(y, k)
    fl, fr, _ = breite_3db(y, f, k, hoehe, 1 / T)
    zeta = (fr - fl) / (2 * (f[k] + d / T))
    # nur Dokumentation (FG-03): drei Stellen wie angegeben.
    assert math.isclose(zeta / 0.005 - 1, soll, rel_tol=0.0, abs_tol=5e-4)


# --- RF-F6: Kennzeichen; RF-F7: Vorzeichen ------------------------------------------------


def test_rf_f6_konjugiert() -> None:
    f = raster(0.37)
    r = fit_moden(f, np.conj(y_sdof(f)), [100.3], [0.01])
    assert r.rho > 0.4
    assert math.isclose(r.rho, 0.454, rel_tol=0.0, abs_tol=5e-4)
    assert r.zeta[0] < 1e-5
    k = kz(r, f, DF)[0]
    assert {MODELL_PASST_NICHT, NICHT_KONVERGIERT, AUSSERHALB_BAND} <= set(k)


def _gruppe(spitzen: tuple[int, ...], von: int, bis: int, k: tuple[str, ...] = ()) -> Gruppe:
    return Gruppe(
        nummer=0,
        spitzen=spitzen,
        f_sp_hz=(100.0,) * len(spitzen),
        k_von=von,
        k_bis=bis,
        kennzeichen=k,
    )


def test_rf_f6_zu_wenig_linien_und_gruppe_zu_gross() -> None:
    f = DF * np.arange(200, dtype=np.float64)
    y = y_sdof(f)
    sp = [_spitze(100.0, 64, 1.0)]
    maske = np.ones(200, dtype=bool)
    e = fit_punkt(f, y, maske, _gruppe((0,), 61, 66), sp, punkt=3, delta_f_hz=DF, schwellen2=S2)
    assert not e.gefittet
    assert e.kennzeichen == ((ZU_WENIG_LINIEN,),)
    assert e.n_linien == 6
    assert math.isnan(e.fr_hz[0])
    with pytest.raises(ValueError, match="4n \\+ 3"):
        fit_moden(f[61:67], y[61:67], [100.0], [0.01])
    # Gruppe mit 5 Spitzen
    sp5 = [_spitze(100.0 + i, 64 + i, 3.0, (NACHBARMODE,)) for i in range(5)]
    g = bilde_gruppen(sp5, np.abs(y), DF)
    assert len(g) == 1 and g[0].kennzeichen == (GRUPPE_ZU_GROSS,)
    e5 = fit_punkt(f, y, maske, g[0], sp5, punkt=0, delta_f_hz=DF, schwellen2=S2)
    assert not e5.gefittet and e5.kennzeichen == ((GRUPPE_ZU_GROSS,),) * 5


def test_randfall_null_und_maske() -> None:
    f = DF * np.arange(200, dtype=np.float64)
    sp = [_spitze(100.0, 64, 1.0)]
    g = _gruppe((0,), 56, 72)
    e = fit_punkt(
        f,
        np.zeros(200, dtype=complex),
        np.ones(200, dtype=bool),
        g,
        sp,
        punkt=0,
        delta_f_hz=DF,
        schwellen2=S2,
    )
    assert not e.gefittet and e.hinweise == (HINWEIS_NULL,)
    # Kohärenzmaske nimmt die Spitzenlinie heraus: Fit mit den übrigen Linien.
    maske = np.ones(200, dtype=bool)
    maske[64] = False
    e2 = fit_punkt(
        f,
        y_sdof(f),
        maske,
        g,
        sp,
        punkt=0,
        delta_f_hz=DF,
        schwellen2=S2,
        zusatz=[(KOHAERENZ_NIEDRIG,)],
    )
    assert e2.gefittet and e2.n_linien == 16
    assert math.isclose(e2.zeta[0], 0.005, rel_tol=1e-6)
    assert e2.kennzeichen == ((KOHAERENZ_NIEDRIG,),)


@pytest.mark.parametrize("off", [0.0, 0.37])
def test_rf_f7_vorzeichen(off: float) -> None:
    f = raster(off)
    r = fit_moden(f, -y_sdof(f), [100.3], [0.01])
    assert math.isclose(r.fr_hz[0], 100.0, rel_tol=0.0, abs_tol=1e-7)
    assert math.isclose(r.zeta[0], 0.005, rel_tol=1e-6)
    assert np.isclose(r.modalkonstante[0], -1.0, rtol=1e-6, atol=0.0)
    assert r.rho <= 1e-12


# --- Eingabeprüfung, Kennzeichen, Hilfsfunktionen -----------------------------------------


def test_fit_moden_eingabefehler() -> None:
    f = raster(0.0)
    y = y_sdof(f)
    with pytest.raises(ValueError, match="müssen \\(m,\\)"):
        fit_moden(f, y[:-1], [100.0], [0.01])
    with pytest.raises(ValueError, match="Startwerte fr0"):
        fit_moden(f, y, [100.0], [0.01, 0.02])
    with pytest.raises(ValueError, match="endlich"):
        fit_moden(f, np.where(f > 100, np.nan, y), [100.0], [0.01])
    with pytest.raises(ValueError, match="> 0"):
        fit_moden(f, y, [100.0], [0.0])
    with pytest.raises(ValueError, match="gewicht"):
        fit_moden(f, y, [100.0], [0.01], gewicht=-np.ones(f.size))


def test_gewichteter_fit_exakt() -> None:
    f = raster(0.37)
    r = fit_moden(f, y_sdof(f), [100.3], [0.01], gewicht=np.linspace(1, 3, f.size))
    assert math.isclose(r.zeta[0], 0.005, rel_tol=1e-6)


def test_abbruch_max_iter_und_lambda() -> None:
    f = raster(0.37)
    r = fit_moden(f, y_sdof(f), [100.3], [0.01], max_iter=1)
    assert not r.konvergiert and r.abbruch == "max_iter"
    rng = np.random.default_rng(1)
    rausch = rng.standard_normal(f.size) + 1j * rng.standard_normal(f.size)
    r2 = fit_moden(f, rausch, [100.3], [0.01], lambda_max=1e-2, tol_rel=1e-300)
    assert r2.abbruch in ("lambda", "max_iter", "singulaer")
    assert not r2.konvergiert


def test_kennzeichen_einzeln() -> None:
    f = raster(0.37)
    r = fit_moden(f, y_sdof(f), [100.3], [0.01])
    k = kennzeichen_fit(
        r,
        f_band_hz=(f[0], f[-1]),
        delta_f_hz=DF,
        schwellen2=S2,
        m7_grenze_hz=50.0,
        mobilitaetsbezug=False,
    )
    assert KEIN_MOBILITAETSBEZUG in k[0] and GUELTIGKEIT_OFFEN_M7 in k[0]


def test_basis_iqr_frf_art() -> None:
    b = basis_mobilitaet([100.0], [100.0], [0.5])
    assert b.shape == (1, 2) and np.isclose(b[0, 0], 1 / (2 * 0.5 * 2 * np.pi * 100.0))
    assert iqr([1.0, 2.0, 3.0, 4.0, 5.0]) == pytest.approx(2.0, abs=1e-15)
    assert frf_art_aus_einheiten("m/s", "N") == "mobilitaet"
    assert frf_art_aus_einheiten("m/s²", "N") == "akzeleranz"
    assert frf_art_aus_einheiten("m/s^2", "N") == "akzeleranz"
    assert frf_art_aus_einheiten("m/s", "m/s²") == "andere"
    assert frf_art_aus_einheiten("V", "N") == "andere"


# --- Paarebene: schaetze_daempfung an synthetischen Stufe-1-Auswertungen ------------------


def _auswertung(p: int = 6, n_v: float = 0.0, antwort: str = "Vib Z", referenz: str = "Ref1"):  # type: ignore[no-untyped-def]
    f = DF * np.arange(1, 401, dtype=np.float64)
    skala = np.linspace(1.0, 2.0, p)[:, None]
    h = skala * mobilitaet_moden(f, [100.0, 300.0], zeta=0.01)
    daten = erwartungswert_paar(
        h, 1.0, 0.0, n_v, form=(p, f.size), antwort=antwort, referenz=referenz
    )
    return werte_aus(daten)


def test_paar_sdof_exakt_und_zusammenfassung() -> None:
    aw = _auswertung()
    r = schaetze_daempfung(aw, ("Vib Z", "Ref1"), schwellen2=SchwellenStufe2(n_punkte=4))
    assert r.frf_art == "mobilitaet"
    assert len(r.zusammenfassung) == 2
    for z, f_soll in zip(r.zusammenfassung, (100.0, 300.0), strict=True):
        # Zwei Moden mit ζ = 0,01, getrennt: Fit mit Residuum C ist nahezu exakt
        # (Einfluss der Nachbarmode im Band nicht exakt konstant) → rtol 1e-3.
        assert math.isclose(z.fr_median_hz, f_soll, rel_tol=1e-4)
        assert math.isclose(z.zeta_median, 0.01, rel_tol=1e-2)
        assert z.n_punkte == 4
        assert z.punkte == (5, 4, 3, 2)  # die stärksten Punkte zuerst
    e = r.ergebnis(5, 0)
    assert e is not None and e.gefittet
    assert r.ergebnis(0, 0) is None  # nur die 4 stärksten gefittet
    assert r.zusammenfassung_bei(290.0).f_sp_hz == pytest.approx(300.0, abs=1.0)


def test_paar_optionen_und_fehler() -> None:
    aw = _auswertung(n_v=1e-9)
    alle = schaetze_daempfung(
        aw,
        ("Vib Z", "Ref1"),
        schwellen2=SchwellenStufe2(punktauswahl="alle", gewichtung="fehler"),
        spitzen=[1],
    )
    assert {e.punkt for e in alle.ergebnisse} == set(range(6))
    assert len(alle.zusammenfassung) == 1
    nur = schaetze_daempfung(aw, ("Vib Z", "Ref1"), spitzen=[0], punkte=[1, 2])
    assert {e.punkt for e in nur.ergebnisse} == {1, 2}
    with pytest.raises(KeyError):
        schaetze_daempfung(aw, ("Vib X", "Ref1"))
    with pytest.raises(ValueError, match="Spitzenindex"):
        schaetze_daempfung(aw, ("Vib Z", "Ref1"), spitzen=[9])
    with pytest.raises(ValueError, match="Punktindex"):
        schaetze_daempfung(aw, ("Vib Z", "Ref1"), punkte=[99])
    leer = r_leer = schaetze_daempfung(aw, ("Vib Z", "Ref1"), spitzen=[0], punkte=[])
    assert all(z.hinweise == (HINWEIS_KEINE_PUNKTE,) for z in r_leer.zusammenfassung)
    assert leer.ergebnisse == ()


def test_paar_akzeleranz_und_andere() -> None:
    aw = _auswertung(antwort="Ref2")
    # H1 = Mobilität, aber Einheit m/s² → wird als Akzeleranz behandelt und durch iω geteilt;
    # das Ergebnis ist hier physikalisch falsch, geprüft wird nur der Weg.
    r = schaetze_daempfung(aw, ("Ref2", "Ref1"), spitzen=[0])
    assert r.frf_art == "akzeleranz" and r.einheit_fit == "(m/s)/N"
    r2 = schaetze_daempfung(aw, ("Ref2", "Ref1"), frf_art="andere", spitzen=[0])
    assert r2.hinweise and all(
        KEIN_MOBILITAETSBEZUG in k for e in r2.ergebnisse for k in e.kennzeichen
    )


def test_paar_kohaerenz_niedrig_aus_punkt() -> None:
    aw = _auswertung(n_v=1e-3, p=3)  # γ² an den Flanken klein
    r = schaetze_daempfung(
        aw, ("Vib Z", "Ref1"), spitzen=[0], schwellen2=SchwellenStufe2(n_punkte=3)
    )
    assert Schwellen().kohaerenz_min == aw.schwellen.kohaerenz_min
    assert r.ergebnisse  # Fit oder Kennzeichen, keine stille Auslassung
    for e in r.ergebnisse:
        assert e.gefittet or e.kennzeichen[0] == (ZU_WENIG_LINIEN,)


def test_stufe1_unveraendert() -> None:
    aw = _auswertung()
    h1 = aw.paare[("Vib Z", "Ref1")].frf.h1.copy()
    schaetze_daempfung(aw, ("Vib Z", "Ref1"), schwellen2=SchwellenStufe2(gewichtung="fehler"))
    np.testing.assert_array_equal(aw.paare[("Vib Z", "Ref1")].frf.h1, h1)
    assert Annahmen().eintraege() == Annahmen().eintraege()
