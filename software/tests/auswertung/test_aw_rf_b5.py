"""Referenzfälle B-5 (FG-03 9.2, RF-V1 bis RF-V5) und Randfälle 6.3 des Vergleichs."""

from __future__ import annotations

import dataclasses
import math
from pathlib import Path
from typing import Any

import numpy as np
import numpy.typing as npt
import pytest
from aw_referenz import fake_svd_messung

from ldv_automation.auswertung import Annahmen, werte_aus
from ldv_automation.auswertung.annahmen import AnnahmenStufe2
from ldv_automation.auswertung.daten import Punkte
from ldv_automation.auswertung.modenfit import schaetze_daempfung
from ldv_automation.auswertung.svd_adapter import aus_svd_messung
from ldv_automation.auswertung.vergleich import (
    HINWEIS_ACHSEN,
    HINWEIS_KEINE_ZUORDNUNG,
    HINWEIS_MAC_1D,
    HINWEIS_OHNE_PHASE,
    PASSPUNKTE_UNGENAU,
    achsen_gleich,
    auto_mac,
    drehe_nach_a,
    drift_aus,
    drift_regression,
    kabsch,
    kleinster_abstand,
    mac,
    ordne_punkte,
    paare_spitzen,
    vergleiche_frf,
    vergleiche_messungen,
)

NX, NY, D = 9, 15, 0.029
GX, GY = np.meshgrid(np.arange(NX) * D, np.arange(NY) * D, indexing="ij")
P = np.column_stack([GX.ravel(), GY.ravel(), np.zeros(GX.size)])
LX, LY = (NX - 1) * D, (NY - 1) * D


def form(m: int, n: int) -> npt.NDArray[np.float64]:
    return np.asarray(
        np.sin(m * np.pi * (P[:, 0] + D) / (LX + 2 * D))
        * np.sin(n * np.pi * (P[:, 1] + D) / (LY + 2 * D))
    )


P11, P21, P12 = form(1, 1), form(2, 1), form(1, 2)
WINKEL = np.radians(10.0)
R = np.array([[np.cos(WINKEL), -np.sin(WINKEL), 0], [np.sin(WINKEL), np.cos(WINKEL), 0], [0, 0, 1]])
T = np.array([0.05, -0.02, 0.01])
ECKEN = [0, NX * NY - 1, NY - 1, (NX - 1) * NY]


def punkte(x: npt.NDArray[np.float64], label0: int = 1) -> Punkte:
    n = x.shape[0]
    return Punkte(
        index=np.arange(n, dtype=np.int64),
        label=np.arange(label0, label0 + n, dtype=np.int64),
        koordinaten_m=np.asarray(x, dtype=np.float64),
    )


# --- RF-V1 ---------------------------------------------------------------------------------


def test_rf_v1_mac() -> None:
    # FG-03 RF-V1: atol 1e-12.
    soll = [
        (P11, P11, 1.0),
        (P11, (2 - 3j) * P11, 1.0),
        (P11, P21, 0.0),
        (P11, P12, 0.0),
        (P21, P12, 0.0),
        (P11, P11 + 0.5 * P21, 0.8),
    ]
    for a, b, w in soll:
        assert math.isclose(mac(a, b), w, rel_tol=0.0, abs_tol=1e-12)


def test_rf_v1b_mac_3d() -> None:
    v = np.column_stack([0.1 * P21, 0.05j * P11, P11])
    nur_z = np.column_stack([0 * P11, 0 * P11, P11])
    assert math.isclose(mac(v, nur_z), 0.9876543210, rel_tol=1e-9)


def test_mac_randfaelle_und_auto_mac() -> None:
    assert math.isnan(mac(np.zeros(3), np.ones(3)))
    with pytest.raises(ValueError, match="Längen"):
        mac(np.ones(3), np.ones(4))
    m = auto_mac([P11, P21, 2 * P11])
    assert m.shape == (3, 3)
    np.testing.assert_allclose(np.diag(m), 1.0, rtol=0, atol=1e-12)
    assert math.isclose(m[0, 2], 1.0, abs_tol=1e-12) and math.isclose(m[0, 1], 0.0, abs_tol=1e-12)


# --- RF-V2 ---------------------------------------------------------------------------------


def test_rf_v2_kabsch_exakt_und_zuordnung() -> None:
    q = P @ R.T + T
    trafo = kabsch(P[ECKEN], q[ECKEN])
    # FG-03 RF-V2: R, t atol 1e-12.
    np.testing.assert_allclose(trafo.drehung, R, rtol=0, atol=1e-12)
    np.testing.assert_allclose(trafo.verschiebung_m, T, rtol=0, atol=1e-12)
    assert trafo.rms_m <= 1e-12 and trafo.n_passpunkte == 4
    pa, pb = punkte(P), punkte(q, label0=500)
    passp = [(int(pa.label[i]), int(pb.label[i])) for i in ECKEN]
    z = ordne_punkte(pa, pb, variante="koordinaten", passpunkte=passp)
    assert z.index_a.size == 135
    np.testing.assert_array_equal(z.index_a, z.index_b)
    assert z.kennzeichen == () and math.isclose(z.d_tol_m, 0.5 * D, rel_tol=1e-12)
    assert z.ohne_partner_a == () and z.ohne_partner_b == ()


def test_rf_v2b_rauschen() -> None:
    rng = np.random.default_rng(20261030)
    q = P @ R.T + T
    qn = q + rng.normal(0, 0.0005, q.shape)
    pa, pb = punkte(P), punkte(qn)
    z = ordne_punkte(
        pa, pb, variante="koordinaten", passpunkte=[(i, i) for i in ECKEN], passpunkt_art="index"
    )
    assert z.index_a.size == 135
    np.testing.assert_array_equal(z.index_a, z.index_b)
    winkel = math.degrees(math.atan2(z.drehung[1, 0], z.drehung[0, 0]))
    assert abs(winkel - 10.0) <= 0.2  # FG-03 RF-V2b: ±0,2°
    assert z.abstand_m.max() <= 0.5 * D  # d_tol = 14,5 mm (beobachtet 2,0 mm)


def test_rf_v2c_komponenten_drehen() -> None:
    va = np.column_stack([0.3 * P21, 0.2 * P11, P11])
    vb = va @ R.T
    assert math.isclose(mac(va, vb), 0.9965074935, rel_tol=1e-6)
    assert math.isclose(mac(va, drehe_nach_a(vb, R)), 1.0, rel_tol=0.0, abs_tol=1e-12)
    with pytest.raises(ValueError, match="R \\(3, 3\\)"):
        drehe_nach_a(va[:, :2], R)


def test_rf_v2d_kollinear_und_zu_wenige() -> None:
    linie = np.array([[0, 0, 0], [1, 0, 0], [2, 0, 0.0]])
    with pytest.raises(ValueError, match="kollinear"):
        kabsch(linie, linie)
    with pytest.raises(ValueError, match="drei Passpunkte"):
        kabsch(linie[:2], linie[:2])
    with pytest.raises(ValueError, match="kollinear"):
        kabsch(np.zeros((3, 3)), np.zeros((3, 3)))
    with pytest.raises(ValueError, match="\\(N, 3\\)"):
        kabsch(np.zeros((3, 2)), np.zeros((3, 2)))
    with pytest.raises(ValueError, match="endlich"):
        kabsch(np.full((3, 3), np.nan), np.zeros((3, 3)))


def test_zuordnung_label_ungenau_und_fehler() -> None:
    pa = punkte(P[:10])
    pb = punkte(P[5:20] + 0.003, label0=6)  # Labels 6..20; A hat 1..10
    z = ordne_punkte(pa, pb)
    assert list(pa.label[z.index_a]) == [6, 7, 8, 9, 10]
    assert z.ohne_partner_a == (0, 1, 2, 3, 4) and math.isnan(z.rms_passpunkte_m)
    # Passpunkte mit großem Restfehler → passpunkte_ungenau
    ecken = punkte(P[ECKEN])
    xb = P[ECKEN].copy()
    xb[1] += [0.3, 0.0, 0.0]
    z2 = ordne_punkte(ecken, punkte(xb), passpunkte=[(1, 1), (2, 2), (3, 3), (4, 4)])
    assert z2.kennzeichen == (PASSPUNKTE_UNGENAU,)
    with pytest.raises(ValueError, match="Label 99"):
        ordne_punkte(pa, punkte(xb), passpunkte=[(99, 1), (2, 2), (3, 3)])
    with pytest.raises(ValueError, match="Index 99"):
        ordne_punkte(pa, punkte(xb), passpunkte=[(0, 99), (1, 1), (2, 2)], passpunkt_art="index")
    with pytest.raises(ValueError, match="Zuordnungsvariante"):
        ordne_punkte(pa, pa, variante="x")  # type: ignore[arg-type]
    leer = ordne_punkte(pa, punkte(P[:3] + 5.0), variante="koordinaten")
    assert leer.index_a.size == 0 and leer.hinweise == (HINWEIS_KEINE_ZUORDNUNG,)
    with pytest.raises(ValueError, match="zwei Punkte"):
        kleinster_abstand(P[:1])
    with pytest.raises(ValueError, match="selben Ort"):
        kleinster_abstand(np.zeros((3, 3)))


# --- RF-V3 ---------------------------------------------------------------------------------


def test_rf_v3_spitzenpaarung() -> None:
    r = paare_spitzen([100.0, 150.2, 260.5], [100.3, 149.9, 261.4, 300.0], 1.5)
    soll = [(0, 0, 0.3), (1, 1, -0.3), (2, 2, 0.9)]
    assert [(p.index_a, p.index_b) for p in r.paare] == [(i, j) for i, j, _ in soll]
    for p, (_, _, df) in zip(r.paare, soll, strict=True):
        assert math.isclose(p.delta_f_hz, df, rel_tol=0.0, abs_tol=1e-12)  # atol 1e-12
        assert math.isclose(p.delta_f_rel, df / p.f_a_hz, rel_tol=1e-12)
    assert r.ohne_partner_b == (3,) and r.ohne_partner_a == ()


def test_spitzenpaarung_signifikanz() -> None:
    r = paare_spitzen(
        [100.0, 200.0],
        [100.3, 200.01],
        1.0,
        sd_a_hz=[0.05, np.nan],
        sd_b_hz=[0.05, 0.05],
        zeta_a=[0.01, 0.01],
        zeta_b=[0.012, 0.01],
        sigma_ohne_b1_hz=0.08,
    )
    assert r.paare[0].signifikant and not r.paare[1].signifikant
    assert math.isclose(r.paare[0].sigma_hz, math.hypot(0.05, 0.05), rel_tol=1e-12)
    assert math.isclose(r.paare[1].sigma_hz, math.hypot(0.08, 0.05), rel_tol=1e-12)
    assert math.isclose(r.paare[0].delta_zeta, 0.002, abs_tol=1e-15)
    with pytest.raises(ValueError, match="passt nicht"):
        paare_spitzen([1.0], [1.0], 1.0, sd_a_hz=[1.0, 2.0])
    leer = paare_spitzen([], [1.0], 1.0)
    assert leer.paare == () and leer.ohne_partner_b == (0,)


# --- RF-V4 ---------------------------------------------------------------------------------


def y_sdof(f: npt.NDArray[np.float64], fn: float = 100.0, z: float = 0.01) -> np.ndarray:
    w = 2 * np.pi * f
    wn = 2 * np.pi * fn
    return 1j * w / (wn**2 - w**2 + 2j * z * wn * w)


@pytest.mark.parametrize(
    ("hb", "soll"),
    [
        ("skaliert", (1.0, 0.8278537032, 0.1)),
        ("verschoben", (0.8024872570, -0.0518051640, 0.6489671289)),
        ("gedaempft", (0.9917806594, -0.8499289122, 0.1271162285)),
    ],
)
def test_rf_v4_frf_vergleich(hb: str, soll: tuple[float, float, float]) -> None:
    f = np.arange(90, 110.0001, 0.25)
    ha = y_sdof(f)
    b = {
        "skaliert": 1.1 * ha,
        "verschoben": y_sdof(f, 101.0),
        "gedaempft": y_sdof(f, 100.0, 0.012),
    }[hb]
    r = vergleiche_frf(ha, b, f, 90.0, 110.0, delta_f_hz=0.25)
    # FG-03 RF-V4: rtol 1e-9.
    assert math.isclose(r.frac[0], soll[0], rel_tol=1e-9)
    assert math.isclose(r.pegel_db[0], soll[1], rel_tol=1e-9)
    assert math.isclose(r.diff_rel[0], soll[2], rel_tol=1e-9)
    assert r.n_linien[0] == f.size


def test_frf_vergleich_randfaelle() -> None:
    f = np.arange(90, 110.0001, 0.25)
    ha = np.vstack([y_sdof(f), np.zeros(f.size), y_sdof(f)])
    hb = np.vstack([y_sdof(f), y_sdof(f), y_sdof(f)])
    maske = np.ones(ha.shape, dtype=bool)
    maske[2, :] = False
    maske[2, :2] = True
    r = vergleiche_frf(ha, hb, f, 90.0, 110.0, maske_a=maske, maske_b=np.ones(ha.shape, bool))
    assert math.isclose(r.frac[0], 1.0, rel_tol=1e-12)
    assert math.isnan(r.frac[1]) and math.isnan(r.diff_rel[1]) and math.isnan(r.pegel_db[1])
    assert math.isnan(r.frac[2]) and r.n_linien[2] == 2
    assert len(r.hinweise) == 2
    nur_b = vergleiche_frf(y_sdof(f), np.zeros(f.size), f, 90.0, 110.0)
    assert math.isnan(nur_b.frac[0]) and math.isclose(nur_b.diff_rel[0], 1.0, rel_tol=1e-12)
    with pytest.raises(ValueError, match="passen nicht"):
        vergleiche_frf(ha, hb[:2], f, 90.0, 110.0)
    assert achsen_gleich(f, f + 1e-9, 0.25) and not achsen_gleich(f, f[:-1], 0.25)


# --- RF-V5 ---------------------------------------------------------------------------------


def test_rf_v5_drift() -> None:
    t = np.linspace(0, 2376.0, 135)
    d = drift_regression(418.9 - 2.0e-5 * t, t)
    # FG-03 RF-V5: rtol 1e-9; sigma_b1 = 0 (Rundungsniveau, daher atol).
    assert math.isclose(d.steigung_hz_h, -0.072, rel_tol=1e-9)
    assert math.isclose(d.gesamt_hz, -0.04752, rel_tol=1e-9)
    assert math.isclose(d.gesamt_rel, -1.1344e-4, rel_tol=1e-4)  # Sollwert auf 5 Stellen
    assert math.isclose(d.gesamt_rel, -0.04752 / 418.9, rel_tol=1e-9)
    assert d.sd_steigung_hz_h <= 1e-9
    assert d.signifikant and d.pruefbar and d.n_punkte == 135


def test_drift_randfaelle() -> None:
    t = np.arange(9, dtype=np.float64)
    d = drift_regression(np.ones(9), t)
    assert not d.pruefbar and math.isnan(d.steigung_hz_h) and d.hinweise
    d2 = drift_regression(np.ones(12), np.zeros(12))
    assert not d2.pruefbar and "selben Zeit" in d2.hinweise[0]
    rng = np.random.default_rng(3)
    d3 = drift_regression(100 + rng.normal(0, 0.01, 50), np.arange(50.0))
    assert d3.pruefbar and not d3.signifikant
    with pytest.raises(ValueError, match="\\(N,\\)"):
        drift_regression(np.ones(3), np.ones(4))


# --- Paarebene mit synthetischen Messungen -----------------------------------------------


def _aw(tmp_path: Path, p: int = 4, **kw: Any):  # type: ignore[no-untyped-def]
    pfad = tmp_path / "x.svd"
    pfad.write_bytes(b"x")
    daten = aus_svd_messung(fake_svd_messung(pfad, p=p), sha256="0" * 64)
    if kw:
        daten = dataclasses.replace(daten, **kw)
    return werte_aus(daten)


def test_vergleich_gleiche_messung(tmp_path: Path) -> None:
    a = _aw(tmp_path)
    b1 = schaetze_daempfung(a, ("Vib Z", "Ref1"))
    v = vergleiche_messungen(a, a, ("Vib Z", "Ref1"), baender=[(90.0, 110.0)], b1_a=b1, b1_b=b1)
    assert v.achsen_gleich and v.mac_3d
    assert len(v.spitzen.paare) == len(a.paare[("Vib Z", "Ref1")].spitzen.spitzen)
    assert all(p.delta_f_hz == 0.0 and not p.signifikant for p in v.spitzen.paare)
    np.testing.assert_allclose(v.mac, 1.0, rtol=0, atol=1e-12)
    np.testing.assert_allclose(v.frf[0].frac, 1.0, rtol=0, atol=1e-12)
    np.testing.assert_allclose(np.diag(v.auto_mac_a), 1.0, rtol=0, atol=1e-12)
    with pytest.raises(KeyError):
        vergleiche_messungen(a, a, ("Vib Q", "Ref1"))


def test_vergleich_randfaelle(tmp_path: Path) -> None:
    a = _aw(tmp_path)
    ohne_phase = _aw(tmp_path, phase_gueltig=False)
    v = vergleiche_messungen(a, ohne_phase, ("Vib Z", "Ref1"))
    assert HINWEIS_OHNE_PHASE in v.hinweise and np.all(np.isnan(v.mac))
    assert np.all(np.isnan(v.auto_mac_b))
    nur_z = _aw(tmp_path)
    nur_z = werte_aus(
        dataclasses.replace(
            nur_z.daten, cp={k: v for k, v in nur_z.daten.cp.items() if k[0] != "Vib X"}
        )
    )
    v1 = vergleiche_messungen(nur_z, nur_z, ("Vib Z", "Ref1"))
    assert not v1.mac_3d and HINWEIS_MAC_1D in v1.hinweise
    f = a.daten.frequenz_hz + 0.1
    verschoben = _aw(tmp_path, frequenz_hz=f)
    v2 = vergleiche_messungen(a, verschoben, ("Vib Z", "Ref1"), baender=[(90.0, 110.0)])
    assert not v2.achsen_gleich and HINWEIS_ACHSEN in v2.hinweise and v2.frf == ()
    weg = dataclasses.replace(
        a.daten,
        punkte=dataclasses.replace(a.daten.punkte, label=a.daten.punkte.label + 1000),
    )
    v3 = vergleiche_messungen(a, werte_aus(weg), ("Vib Z", "Ref1"), baender=[(90.0, 110.0)])
    assert HINWEIS_KEINE_ZUORDNUNG in v3.hinweise and np.all(np.isnan(v3.mac))
    assert v3.frf[0].frac.size == 0
    # M12-Drehung wirkt auf beide Messungen gleich: MAC bleibt 1
    d = AnnahmenStufe2(drehung_komponenten=R.tolist())
    v4 = vergleiche_messungen(a, a, ("Vib Z", "Ref1"), annahmen2=d)
    np.testing.assert_allclose(v4.mac, 1.0, rtol=0, atol=1e-12)


def test_drift_aus(tmp_path: Path) -> None:
    a = _aw(tmp_path, p=12)
    t = np.arange(12) * 60.0
    d, fit = drift_aus(a, t, 150.0, ("Ref2", "Ref1"))
    assert d.pruefbar and d.n_punkte == 12
    assert math.isclose(d.steigung_hz_h, 0.0, abs_tol=1e-6)  # stationäre Daten
    assert fit.zusammenfassung
    d2, _ = drift_aus(a, t, 100.0, ("Vib Z", "Ref1"), antriebspunkt=False)
    assert d2.n_punkte >= 1  # Punkte mit |H1| >= 0,3·max
    with pytest.raises(ValueError, match="zeit_s"):
        drift_aus(a, t[:3], 100.0, ("Ref2", "Ref1"))
    with pytest.raises(KeyError):
        drift_aus(a, t, 100.0, ("Vib Q", "Ref1"))
    assert Annahmen().k0 == 1
