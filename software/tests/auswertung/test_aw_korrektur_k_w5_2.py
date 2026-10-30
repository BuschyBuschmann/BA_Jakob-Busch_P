"""Korrektur K-W5-2: neue Referenzfälle FG-03 (RF-F8, RF-V6, RF-V7) und Review-Befunde M2–M5,
N2–N4, FA-6 sowie die Drehrichtungen der Komponenten (M3)."""

from __future__ import annotations

import dataclasses
import math
from pathlib import Path
from typing import Any

import numpy as np
import pytest
from aw_referenz import fake_svd_messung

from ldv_automation.auswertung import Annahmen, schwingform_aus, werte_aus
from ldv_automation.auswertung import export as export_modul
from ldv_automation.auswertung.annahmen import AnnahmenStufe2, SchwellenStufe2
from ldv_automation.auswertung.bezug3d import bahnellipse, komponentenbezug
from ldv_automation.auswertung.daten import Messdaten, Punkte
from ldv_automation.auswertung.modenfit import (
    AUSSERHALB_BAND,
    GRUPPE_ZU_GROSS,
    HINWEIS_KOHAERENZ_NAN,
    MODELL_PASST_NICHT,
    MODEN_VERTAUSCHT,
    NICHT_KONVERGIERT,
    UNSICHER,
    Gruppe,
    ModenErgebnis,
    fasse_zusammen,
    fit_punkt,
    schaetze_daempfung,
    vertauschte_moden,
)
from ldv_automation.auswertung.spitzen import GUELTIGKEIT_OFFEN_M7, KOHAERENZ_NIEDRIG, Spitze
from ldv_automation.auswertung.svd_adapter import aus_svd_messung
from ldv_automation.auswertung.vergleich import (
    HINWEIS_MAC_1D,
    amplituden,
    drift_aus_ergebnissen,
    ordne_punkte,
    paare_spitzen,
    vergleiche_messungen,
)

S2 = SchwellenStufe2()
DF = 1.5625


def y_sdof(f: np.ndarray, fn: float = 100.0, zeta: float = 0.005) -> np.ndarray:
    w = 2 * np.pi * f
    wn = 2 * np.pi * fn
    return np.asarray(1j * w / (wn**2 - w**2 + 2j * zeta * wn * w))


def spitze(f: float, k: int) -> Spitze:
    return Spitze(
        k=k,
        f_k_hz=f,
        f_sp_hz=f,
        hoehe=1.0,
        breite_3db_hz=1.0,
        q=f,
        zeta=0.01,
        f_l_hz=f - 0.5,
        f_r_hz=f + 0.5,
        delta=0.0,
        kennzeichen=(),
    )


# --- RF-F8: γ² = NaN bleibt im Fit (K2-4) -------------------------------------------------


@pytest.mark.parametrize("fall", ["a", "b"])
def test_rf_f8_kohaerenz_nan(fall: str) -> None:
    f = np.asarray((np.arange(200) + 0.37) * DF, dtype=np.float64)
    y = y_sdof(f)
    g = Gruppe(nummer=0, spitzen=(0,), f_sp_hz=(100.3,), k_von=56, k_bis=72, kennzeichen=())
    sp = [spitze(100.3, 64)]  # Start f = 100,3 Hz, ζ = 0,01 wie RF-F1
    g2 = np.full(200, np.nan)
    if fall == "b":
        g2[58] = 0.5  # dritte Linie des Bands, γ² < γ²_min
    e = fit_punkt(
        f,
        y,
        np.isfinite(y),
        g,
        sp,
        punkt=0,
        delta_f_hz=DF,
        schwellen2=S2,
        kohaerenz=g2,
        kohaerenz_min=0.9,
    )
    # FG-03 RF-F8: Werte wie RF-F1 (atol 1e-7 Hz, rtol 1e-6), Linienzahl und Kennzeichen exakt.
    assert e.gefittet and e.n_linien == (17 if fall == "a" else 16)
    assert math.isclose(e.fr_hz[0], 100.0, rel_tol=0.0, abs_tol=1e-7)
    assert math.isclose(e.zeta[0], 0.005, rel_tol=1e-6)
    assert e.kennzeichen == ((),)
    assert e.hinweise == (HINWEIS_KOHAERENZ_NAN,)


def test_k2_4_paarebene_ohne_mittelung(tmp_path: Path) -> None:
    pfad = tmp_path / "n.svd"
    pfad.write_bytes(b"n")
    daten = aus_svd_messung(fake_svd_messung(pfad, p=3), sha256="0" * 64)
    aw = werte_aus(daten, annahmen=Annahmen(n_d=1))
    assert np.all(np.isnan(aw.paare[("Vib Z", "Ref1")].frf.kohaerenz))
    r = schaetze_daempfung(aw, ("Vib Z", "Ref1"), spitzen=[0])
    assert r.ergebnisse and all(e.gefittet for e in r.ergebnisse)
    assert all(HINWEIS_KOHAERENZ_NAN in e.hinweise for e in r.ergebnisse)
    assert math.isclose(r.zusammenfassung[0].fr_median_hz, 100.0, rel_tol=1e-4)


# --- RF-V6: Drift-Ausschluss je gewählter Mode (K2-1) -------------------------------------


def _ergebnis(p: int, fr: float, n: int, kz: list[tuple[str, ...]]) -> ModenErgebnis:
    nan = (math.nan,) * n
    return ModenErgebnis(
        punkt=p,
        gruppe=0,
        spitzen=tuple(range(n)),
        gefittet=True,
        fr_hz=(fr, *(700.0,) * (n - 1)),
        sd_fr_hz=(0.05,) * n,
        zeta=(0.002,) * n,
        sd_zeta_rel=(0.05,) * n,
        breite_fit_hz=nan,
        modalkonstante=(0j,) * n,
        residuum=0j,
        rho=0.05,
        n_linien=13,
        n_moden=n,
        iterationen=5,
        kennzeichen=tuple(kz),
        hinweise=(),
    )


T6 = np.arange(20) * 120.0
F6 = 631.7 - 2e-5 * T6


def _rf_v6(n: int) -> list[ModenErgebnis]:
    erg = []
    aus = {10, 11, 12} | ({0, 1, 2} if n == 1 else set())
    for p in range(20):
        k1: list[str] = []
        k2: list[str] = []
        if (n == 2 and p <= 9) or (n == 1 and p <= 2):
            k1.append(NICHT_KONVERGIERT)
            k2 += [NICHT_KONVERGIERT, AUSSERHALB_BAND]
        if p in (10, 11):
            k1.append(UNSICHER)
        if p == 12:
            k1.append(AUSSERHALB_BAND)
        if p >= 13:
            k1.append(MODELL_PASST_NICHT)
            k2.append(MODELL_PASST_NICHT)
        if n == 2 and p == 5:
            k1.append(GUELTIGKEIT_OFFEN_M7)
        if n == 2 and p == 6:
            k1.append(KOHAERENZ_NIEDRIG)
        kz = [tuple(k1), tuple(k2)][:n]
        erg.append(_ergebnis(p, F6[p] + (1.0 if p in aus else 0.0), n, kz))
    return erg


@pytest.mark.parametrize(
    ("n", "anzahl", "gesamt", "rel", "b0"),
    [
        (2, 17, -0.0456, -7.2186164318e-5, 631.7),
        (1, 14, -0.0384, -6.0789041762e-5, 631.6928),
    ],
)
def test_rf_v6_drift_ausschluss(n: int, anzahl: int, gesamt: float, rel: float, b0: float) -> None:
    d = drift_aus_ergebnissen(_rf_v6(n), 0, T6)
    # FG-03 RF-V6: rtol 1e-9; N exakt.
    assert d.n_punkte == anzahl and d.n_modell_passt_nicht == 7
    assert math.isclose(d.steigung_hz_h, -0.072, rel_tol=1e-9)
    assert math.isclose(d.gesamt_hz, gesamt, rel_tol=1e-9)
    assert math.isclose(d.gesamt_rel, rel, rel_tol=1e-9)
    assert math.isclose(d.achsenabschnitt_hz, b0, rel_tol=1e-9)
    assert d.signifikant


def test_drift_ausschluss_ohne_fit_und_schalter() -> None:
    erg = _rf_v6(1)
    erg[3] = dataclasses.replace(erg[3], gefittet=False, fr_hz=(631.7 + 1.0,))
    d = drift_aus_ergebnissen(erg, 0, T6)
    assert d.n_punkte == 13
    alle = drift_aus_ergebnissen(
        erg,
        0,
        T6,
        schwellen2=SchwellenStufe2(drift_ausschluss=(), drift_nicht_konvergiert_einzelmode=False),
    )
    assert alle.n_punkte == 19
    vertauscht = [
        dataclasses.replace(e, kennzeichen=((MODEN_VERTAUSCHT,),)) for e in _rf_v6(1)[13:]
    ]
    assert drift_aus_ergebnissen(vertauscht, 0, T6).n_punkte == 0


# --- RF-V7: sigma der Spitzenpaarung (K2-3) ----------------------------------------------------


def _zusammenfassung(f: float, sd: tuple[float, ...]) -> Any:
    g = Gruppe(nummer=0, spitzen=(0,), f_sp_hz=(f,), k_von=0, k_bis=10, kennzeichen=())
    erg = [dataclasses.replace(_ergebnis(p, f, 1, [()]), sd_fr_hz=(s,)) for p, s in enumerate(sd)]
    return fasse_zusammen(erg, g, 0, spitze(f, 5), 0, (0, 1, 2))


@pytest.mark.parametrize(("fb", "sig"), [(100.15, True), (100.09, False)])
def test_rf_v7_sigma_spitzenpaarung(fb: float, sig: bool) -> None:
    za = _zusammenfassung(100.0, (0.02, 0.04, 0.05))
    zb = _zusammenfassung(fb, (0.03, 0.03, 0.09))
    # FG-03 RF-V7: atol 1e-12.
    assert math.isclose(za.sd_fr_median_hz, 0.04, abs_tol=1e-12)
    assert math.isclose(zb.sd_fr_median_hz, 0.03, abs_tol=1e-12)
    r = paare_spitzen(
        [za.fr_median_hz],
        [zb.fr_median_hz],
        1.0,
        sd_a_hz=[za.sd_fr_median_hz],
        sd_b_hz=[zb.sd_fr_median_hz],
    )
    p = r.paare[0]
    assert math.isclose(p.sigma_hz, 0.05, abs_tol=1e-12)
    assert math.isclose(p.delta_f_hz, fb - 100.0, abs_tol=1e-12)
    assert p.signifikant is sig


# --- M2: Modenvertauschung -----------------------------------------------------------------


def test_m2_vertauschte_moden() -> None:
    leer: list[tuple[str, ...]] = [(), (), ()]
    assert vertauschte_moden([100, 102, 104], [100.1, 101.9, 104.2], leer) == [False] * 3
    # Beispiel Review: Gruppe 58, Punkt 46 (1072,86; 1058,49; 1065,96)
    assert vertauschte_moden([1059.1, 1065.1, 1072.0], [1072.86, 1058.49, 1065.96], leer) == [
        True,
        True,
        True,
    ]
    assert vertauschte_moden([100, 102], [102.5, 101.0], leer) == [True, True]
    # Weggelaufene Partnermode mit ausserhalb_band vertauscht die übrige nicht
    assert vertauschte_moden([631.6, 640.6], [631.7, 600.0], [(), (AUSSERHALB_BAND,)]) == [
        False,
        False,
    ]
    # Startwerte nicht sortiert: verglichen wird mit ihrer Reihenfolge
    assert vertauschte_moden([104, 100], [104.1, 99.9], [(), ()]) == [False, False]


@pytest.mark.parametrize(
    ("start", "fit", "kz", "soll"),
    [
        ((100.0, 102.0, 104.0), (100.1, 101.9, 104.2), [(), (), ()], [False] * 3),
        ((1059.1, 1065.1, 1072.0), (1072.86, 1058.49, 1065.96), [(), (), ()], [True] * 3),
        ((1325.55, 1329.35), (1350.24, 1325.01), [(AUSSERHALB_BAND,), ()], [False, True]),
        ((834.95, 845.05), (832.66, 835.40), [(), ()], [False, True]),
        ((104.0, 100.0), (104.1, 99.9), [(), ()], [False, False]),
    ],
    ids=["i", "ii", "iii", "iv", "v"],
)
def test_rf_f9_moden_vertauscht(
    start: tuple[float, ...], fit: tuple[float, ...], kz: list[tuple[str, ...]], soll: list[bool]
) -> None:
    # FG-03 RF-F9 (K3-4): Kennzeichen exakt.
    assert vertauschte_moden(start, fit, kz) == soll


def test_rf_f9_gleichstand_ohne_kennzeichen() -> None:
    # |f_r - f_sp,j| = |f_r - f_sp,r|: kein Kennzeichen nach Regel (b)
    assert vertauschte_moden([100.0, 102.0], [101.0, 103.0], [(), ()]) == [False, False]


def test_m2_ausschluss_zusammenfassung() -> None:
    g = Gruppe(nummer=0, spitzen=(0,), f_sp_hz=(100.0,), k_von=0, k_bis=10, kennzeichen=())
    erg = [_ergebnis(0, 100.0, 1, [(MODEN_VERTAUSCHT,)]), _ergebnis(1, 101.0, 1, [()])]
    z = fasse_zusammen(erg, g, 0, spitze(100.0, 5), 0, (0, 1))
    assert z.n_punkte == 1 and z.fr_median_hz == 101.0


def test_n4_ursache_ohne_ergebnis() -> None:
    g = Gruppe(
        nummer=0, spitzen=(0,), f_sp_hz=(100.0,), k_von=0, k_bis=10, kennzeichen=(GRUPPE_ZU_GROSS,)
    )
    erg = [dataclasses.replace(_ergebnis(0, math.nan, 1, [(GRUPPE_ZU_GROSS,)]), gefittet=False)]
    z = fasse_zusammen(erg, g, 0, spitze(100.0, 5), 0, (0, 7))
    assert "gruppe_zu_gross: 1" in z.hinweise[0] and "nicht gefittet: 1" in z.hinweise[0]
    leer = dataclasses.replace(erg[0], kennzeichen=((),), hinweise=("‖H‖ = 0",))
    z2 = fasse_zusammen([leer], g, 0, spitze(100.0, 5), 0, (0,))
    assert "‖H‖ = 0: 1" in z2.hinweise[0]


# --- M3: Ende-zu-Ende-Vergleich mit gedrehter Messung B ------------------------------------


def _drehung(achse: np.ndarray, winkel_rad: float) -> np.ndarray:
    a = achse / np.linalg.norm(achse)
    k = np.array([[0, -a[2], a[1]], [a[2], 0, -a[0]], [-a[1], a[0], 0]])
    return np.asarray(np.eye(3) + math.sin(winkel_rad) * k + (1 - math.cos(winkel_rad)) * k @ k)


R_ALLG = _drehung(np.array([1.0, 2.0, 3.0]), math.radians(40.0))
KOMP = ("Vib X", "Vib Y", "Vib Z")


def _gedreht(daten: Messdaten, r: np.ndarray, t: np.ndarray) -> Messdaten:
    """Messung B: dieselbe Bewegung, Geometrie x_B = R x_A + t, Komponenten v_B = R v_A."""
    cp = dict(daten.cp)
    cph = dict(daten.cph)
    ap = dict(daten.ap)
    for quelle in (cp, cph):
        alt = np.stack([quelle[(k, "Ref1")] for k in KOMP], axis=1)
        neu = np.einsum("ij,pjk->pik", r, alt)
        for i, k in enumerate(KOMP):
            quelle[(k, "Ref1")] = np.ascontiguousarray(neu[:, i])
    for k in KOMP:
        ap[k] = (np.abs(cp[(k, "Ref1")]) ** 2 / daten.ap["Ref1"] * 1.0001).astype(np.float64)
    punkte = Punkte(
        index=daten.punkte.index,
        label=daten.punkte.label,
        koordinaten_m=daten.punkte.koordinaten_m @ r.T + t,
    )
    return dataclasses.replace(daten, cp=cp, cph=cph, ap=ap, punkte=punkte)


@pytest.fixture
def messung_a(tmp_path: Path) -> Messdaten:
    pfad = tmp_path / "a.svd"
    pfad.write_bytes(b"a")
    return aus_svd_messung(fake_svd_messung(pfad, p=4), sha256="0" * 64)


def test_m3_vergleich_gedrehte_messung(messung_a: Messdaten) -> None:
    a = werte_aus(messung_a)
    b = werte_aus(_gedreht(messung_a, R_ALLG, np.array([0.05, -0.02, 0.01])))
    passp = [(int(x), int(x)) for x in messung_a.punkte.label]
    v = vergleiche_messungen(a, b, ("Vib Z", "Ref1"), passpunkte=passp)
    np.testing.assert_allclose(v.zuordnung.drehung, R_ALLG, rtol=0, atol=1e-12)
    assert v.mac_3d and len(v.mac) >= 2
    # Mit R^T v_B ist die Form gleich: MAC = 1 auf 1e-12.
    np.testing.assert_allclose(v.mac, 1.0, rtol=0, atol=1e-12)
    ohne = vergleiche_messungen(a, b, ("Vib Z", "Ref1"))
    assert np.all(ohne.mac < 0.9999)
    assert np.all(ohne.mac > 0.5)


def test_m3_amplituden_mit_d(messung_a: Messdaten) -> None:
    a = werte_aus(messung_a)
    roh, _ = amplituden(a, ("Vib Z", "Ref1"), AnnahmenStufe2())
    d = AnnahmenStufe2(drehung_komponenten=R_ALLG.tolist())
    gedreht, ist_3d = amplituden(a, ("Vib Z", "Ref1"), d)
    assert ist_3d
    k = 199  # 100 Hz
    np.testing.assert_allclose(gedreht[:, :, k], roh[:, :, k] @ R_ALLG.T, rtol=0, atol=1e-15)
    assert not np.allclose(gedreht[:, :, k], roh[:, :, k] @ R_ALLG, atol=1e-6)


def test_m3_b8_d_und_dt_verschieden(messung_a: Messdaten) -> None:
    sf = schwingform_aus(messung_a, 100.0)
    w = math.radians(30.0)
    d = [[math.cos(w), 0.0, math.sin(w)], [0.0, 1.0, 0.0], [-math.sin(w), 0.0, math.cos(w)]]
    kb = komponentenbezug(
        messung_a.punkte.koordinaten_m,
        [(0, 1, 3, 2)],
        sf,
        annahmen2=AnnahmenStufe2(drehung_komponenten=d),
    )
    assert kb.zerlegung is not None
    # v = (0,3; 0,5i; 1)·y: z_geo = -0,3·sin30° + cos30° (mit Dᵀ wäre es +0,3·sin30° + cos30°)
    soll = (-0.3 * math.sin(w) + math.cos(w)) ** 2 / 1.34
    np.testing.assert_allclose(kb.zerlegung.anteil_normal, soll, rtol=1e-6)
    assert not math.isclose(soll, (0.3 * math.sin(w) + math.cos(w)) ** 2 / 1.34, rel_tol=1e-2)


# --- M4, M5, FA-6/N5 -----------------------------------------------------------------------


def test_m4_ungueltige_punkte(messung_a: Messdaten) -> None:
    a = werte_aus(messung_a, annahmen=Annahmen(gueltig=[True, False, True, True]))
    v = vergleiche_messungen(a, a, ("Vib Z", "Ref1"), baender=[(90.0, 110.0)])
    assert any("ungültige Punkte" in h for h in v.hinweise)
    assert v.frf[0].frac.shape == (3,)
    np.testing.assert_allclose(v.mac, 1.0, atol=1e-12)
    voll = werte_aus(messung_a)
    v2 = vergleiche_messungen(voll, voll, ("Vib Z", "Ref1"), baender=[(90.0, 110.0)])
    assert v2.frf[0].frac.shape == (4,) and not any("ungültige" in h for h in v2.hinweise)


def test_m5_doppelte_labels() -> None:
    x = np.array([[0, 0, 0], [1, 0, 0], [0, 1, 0.0]])
    pa = Punkte(index=np.arange(3), label=np.array([1, 2, 2]), koordinaten_m=x)
    pb = Punkte(index=np.arange(3), label=np.array([1, 2, 3]), koordinaten_m=x)
    with pytest.raises(ValueError, match="doppelte Labels in A"):
        ordne_punkte(pa, pb)
    with pytest.raises(ValueError, match="doppelte Labels in B"):
        ordne_punkte(pb, pa)
    assert ordne_punkte(pa, pb, variante="koordinaten").index_a.size == 3


def test_fa6_quelle_h1(messung_a: Messdaten) -> None:
    a = werte_aus(messung_a)
    h1, ist_3d = amplituden(a, ("Vib Z", "Ref1"), AnnahmenStufe2(), quelle="h1")
    assert ist_3d
    np.testing.assert_allclose(h1[:, 2, :], a.paare[("Vib Z", "Ref1")].frf.h1, rtol=1e-12)
    eins, ist = amplituden(a, ("Ref2", "Ref1"), AnnahmenStufe2(), quelle="h1", nur_1d=True)
    assert not ist and eins.shape[1] == 1
    with pytest.raises(ValueError, match="Quelle"):
        amplituden(a, ("Vib Z", "Ref1"), AnnahmenStufe2(), quelle="x")  # type: ignore[arg-type]
    v = vergleiche_messungen(a, a, ("Vib Z", "Ref1"), quelle="h1")
    np.testing.assert_allclose(v.mac, 1.0, atol=1e-12)
    nur_z = werte_aus(
        dataclasses.replace(
            messung_a, cp={k: w for k, w in messung_a.cp.items() if k[0] != "Vib X"}
        )
    )
    v1 = vergleiche_messungen(nur_z, nur_z, ("Vib Z", "Ref1"), quelle="h1")
    assert HINWEIS_MAC_1D in v1.hinweise and not v1.mac_3d


# --- N2, N3 --------------------------------------------------------------------------------


def test_n2_drehsinn_bei_amplitude_null() -> None:
    e = bahnellipse(np.zeros((1, 3)), np.array([0, 0, 1.0]))
    assert np.isnan(e.drehsinn[0])


def test_n3_export_prueft_ziel_vor_dem_zusammenstellen(
    messung_a: Messdaten, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    a = werte_aus(messung_a)

    def nicht_aufrufen(*_: object) -> None:
        raise AssertionError("baue_export vor der Zielprüfung aufgerufen")

    monkeypatch.setattr(export_modul, "baue_export", nicht_aufrufen)
    with pytest.raises(FileNotFoundError):
        export_modul.exportiere(a, tmp_path / "fehlt" / "x")
    (tmp_path / "x.json").write_text("{}")
    with pytest.raises(FileExistsError):
        export_modul.exportiere(a, tmp_path / "x")
    assert export_modul.Sammler is export_modul._Sammler
