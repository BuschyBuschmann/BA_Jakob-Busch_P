"""Referenzfälle B-8 (FG-03 9.3, RF-G1 bis RF-G5), Annahmen M12–M15 und Randfälle 6.3."""

from __future__ import annotations

import math
from pathlib import Path

import numpy as np
import pytest
from aw_referenz import fake_svd_messung

from ldv_automation.auswertung import schwingform_aus, werte_aus
from ldv_automation.auswertung.annahmen import (
    ANNAHME,
    ANNAHME_NUMMERN,
    ANNAHME_NUMMERN_STUFE2,
    AnnahmenStufe2,
    SchwellenStufe2,
)
from ldv_automation.auswertung.bezug3d import (
    HINWEIS_OHNE_PHASE,
    bahnellipse,
    element_normalen,
    komponentenbezug,
    punkt_normalen,
    zerlege,
)
from ldv_automation.auswertung.svd_adapter import aus_svd_messung

AL = math.radians(30.0)
N_SOLL = np.array([math.sin(AL), 0.0, math.cos(AL)])


def ebene() -> tuple[np.ndarray, list[tuple[int, int, int, int]]]:
    u, v = np.meshgrid(np.arange(4) * 0.02, np.arange(5) * 0.03, indexing="ij")
    g = np.column_stack([(u * math.cos(AL)).ravel(), v.ravel(), (-u * math.sin(AL)).ravel()])

    def i(a: int, b: int) -> int:
        return a * 5 + b

    e = [(i(a, b), i(a + 1, b), i(a + 1, b + 1), i(a, b + 1)) for a in range(3) for b in range(4)]
    return g, e


def test_rf_g1_geneigte_ebene() -> None:
    g, e = ebene()
    en = element_normalen(g, e)
    assert len(e) == 12
    # FG-03 RF-G1: atol 1e-12.
    np.testing.assert_allclose(
        en.normale, np.tile([0.5, 0.0, 0.8660254038], (12, 1)), rtol=0, atol=1e-10
    )
    np.testing.assert_allclose(en.normale, np.tile(N_SOLL, (12, 1)), rtol=0, atol=1e-12)
    np.testing.assert_allclose(en.flaeche_m2, 6.0e-4, rtol=0, atol=1e-12)
    v = np.array([0.3 + 0.1j, 0.2j, 1.0])
    z = zerlege(v, N_SOLL)
    assert abs(z.v_normal - (1.0160254038 + 0.05j)) <= 1e-10
    assert math.isclose(float(z.betrag_tangential_psv), 0.3243337461, rel_tol=0, abs_tol=1e-10)
    assert abs(N_SOLL @ z.v_tangential) <= 1e-12
    np.testing.assert_allclose(z.v_normal, N_SOLL @ v, rtol=0, atol=1e-12)
    assert math.isclose(
        float(z.anteil_normal), abs(N_SOLL @ v) ** 2 / np.sum(np.abs(v) ** 2), rel_tol=1e-12
    )


def test_rf_g2_verwunden_und_umkehr() -> None:
    w = np.array([[0, 0, 0], [1, 0, 0], [1, 1, 0.1], [0, 1, 0.0]])
    soll = np.array([-0.0498754668, -0.0498754668, 0.9975093361])
    en = element_normalen(w, [(0, 1, 2, 3), (0, 3, 2, 1)])
    # FG-03 RF-G2: atol 1e-10; Umkehr ergibt -n, nach Ausrichtung auf +z wieder n.
    np.testing.assert_allclose(en.normale, [soll, soll], rtol=0, atol=1e-10)
    np.testing.assert_allclose(en.flaeche_m2, 1.0024968828, rtol=0, atol=1e-10)
    roh = element_normalen(w, [(0, 3, 2, 1)], e_ref=(0, 0, -1))
    np.testing.assert_allclose(roh.normale[0], -soll, rtol=0, atol=1e-10)


def test_rf_g3_zylinder() -> None:
    rz, nphi, nz = 0.1, 7, 3
    dphi = math.radians(10.0)
    phi = (np.arange(nphi) - 3) * dphi
    zz = np.arange(nz) * 0.02
    c = np.array([[rz * math.sin(p), z, rz * math.cos(p)] for p in phi for z in zz])

    def i(a: int, b: int) -> int:
        return a * nz + b

    e = [
        (i(a, b), i(a + 1, b), i(a + 1, b + 1), i(a, b + 1))
        for a in range(nphi - 1)
        for b in range(nz - 1)
    ]
    n_p, hinweise = punkt_normalen(c.shape[0], element_normalen(c, e))
    assert hinweise == ()
    soll = np.array([[math.sin(p), 0, math.cos(p)] for p in phi for _ in zz])
    fehler = np.degrees(np.arccos(np.clip(np.sum(n_p * soll, axis=1), -1, 1))).reshape(nphi, nz)
    assert fehler[1:-1].max() <= 1e-5  # innen: Rundung von arccos
    np.testing.assert_allclose(fehler[[0, -1]], 5.0, rtol=0, atol=1e-9)  # halber Schritt


def test_rf_g4_bahnellipse() -> None:
    n = np.array([0.0, 0.0, 1.0])
    a = bahnellipse(np.array([1, 1j, 0]), n)
    assert math.isclose(a.auslenkung_max[0], 1.0, rel_tol=1e-9)
    assert math.isclose(a.auslenkung_min[0], 1.0, rel_tol=1e-9)
    assert np.all(np.isnan(a.achse_max[0])) and a.hinweise and a.drehsinn[0] == -1.0
    v = np.array([1, 0.5 * np.exp(1j * np.pi / 3), 0.2j])
    b = bahnellipse(v, n)
    # FG-03 RF-G4: rtol 1e-9; Achse über |e·e_soll| >= 1 - 1e-6.
    assert math.isclose(b.theta_stern_rad[0], -0.1268510019, rel_tol=1e-9)
    assert math.isclose(b.auslenkung_max[0], 1.0374517607, rel_tol=1e-9)
    assert math.isclose(b.auslenkung_min[0], 0.4622703151, rel_tol=1e-9)
    e_soll = np.array([0.9561554879, 0.2918421984, 0.0243888118])
    assert abs(b.achse_max[0] @ e_soll) >= 1 - 1e-6
    assert b.achse_max[0] @ np.array([0, 0, 1.0]) >= 0
    assert math.isclose(float(n @ b.bahnnormale[0]), -0.4330127019, rel_tol=1e-9)
    assert b.drehsinn[0] == -1.0
    c = bahnellipse(np.array([1, -1j, 0]), n)
    assert c.drehsinn[0] == 1.0


def test_bahnellipse_sonderfaelle() -> None:
    lin = bahnellipse(np.array([[1.0, 2.0, 0.0]]), np.array([0, 0, 1.0]))
    assert lin.drehsinn[0] == 0.0
    np.testing.assert_allclose(lin.achse_max[0], np.array([1, 2, 0]) / math.sqrt(5), atol=1e-12)
    neg = bahnellipse(np.array([[-1.0, 0.0, -0.5]]))
    assert neg.achse_max[0][2] > 0 and np.isnan(neg.drehsinn[0])
    # Achse senkrecht zu e_ref: erste Komponente positiv
    senk = bahnellipse(np.array([[-1.0, 0.3, 0.0]]))
    assert senk.achse_max[0][0] > 0
    null = bahnellipse(np.zeros((1, 3)))
    assert np.all(np.isnan(null.achse_max)) and "Amplitude 0" in null.hinweise[0]
    with pytest.raises(ValueError, match="\\(P, 3\\)"):
        bahnellipse(np.zeros((2, 2)))


def test_rf_g5_ohne_element_und_entartet() -> None:
    g, e = ebene()
    x = np.vstack([g, [[1.0, 1.0, 1.0]]])  # Punkt 20 ohne Element
    elemente = [*e, (0, 0, 0)]  # entartetes Dreieck
    en = element_normalen(x, elemente)
    assert en.entartet[-1] and not en.entartet[:-1].any()
    assert np.all(np.isnan(en.normale[-1])) and en.hinweise
    n_p, hinweise = punkt_normalen(x.shape[0], en)
    assert np.all(np.isnan(n_p[20])) and "20" in hinweise[0]
    z = zerlege(np.ones((21, 3), dtype=complex), n_p)
    assert np.isnan(z.v_normal[20]) and np.isnan(z.anteil_normal[20])
    assert not np.isnan(z.v_normal[:20]).any()


def test_elemente_fehler_und_orientierung() -> None:
    g, e = ebene()
    with pytest.raises(ValueError, match="3 oder 4"):
        element_normalen(g, [(0, 1)])
    with pytest.raises(ValueError, match="außerhalb"):
        element_normalen(g, [(0, 1, 99)])
    with pytest.raises(ValueError, match="\\(P, 3\\)"):
        element_normalen(g[:, :2], e)
    en1 = element_normalen(g, [tuple(i + 1 for i in el) for el in e], index_basis=1)
    np.testing.assert_allclose(en1.normale, element_normalen(g, e).normale, atol=0)
    steil = np.array([[0, 0, 0], [1, 0, 0], [0, 0, 1.0]])  # Normale ⟂ z
    en = element_normalen(steil, [(0, 1, 2)])
    assert en.orientierung_unsicher[0] and "orientierung_unsicher" in en.hinweise[0]
    with pytest.raises(ValueError, match="X, Y, Z"):
        zerlege(np.ones(2), np.ones(3))
    # entgegengesetzte Elemente heben sich am Punkt nicht auf (Ausrichtung auf e_ref)
    n_p, _ = punkt_normalen(3, en)
    assert np.all(np.isfinite(n_p))


def test_normalensumme_null() -> None:
    # Zwei gleich große Elemente mit Normalen (0, -1, 0) und (0, 1, 0) senkrecht zu e_ref:
    # Die Ausrichtung ändert sie nicht, am gemeinsamen Punkt heben sie sich auf.
    x = np.array([[0, 0, 0], [1, 0, 0], [0, 0, 1.0]])
    en = element_normalen(x, [(0, 1, 2), (0, 2, 1)])
    np.testing.assert_allclose(en.normale, [[0, -1, 0], [0, 1, 0]], atol=1e-15)
    n_p, hinweise = punkt_normalen(3, en)
    assert np.all(np.isnan(n_p)) and "nicht bestimmbar" in hinweise[0]


def test_komponentenbezug_mit_schwingform(tmp_path: Path) -> None:
    pfad = tmp_path / "x.svd"
    pfad.write_bytes(b"x")
    daten = aus_svd_messung(fake_svd_messung(pfad, p=4), sha256="0" * 64)
    sf = schwingform_aus(daten, 100.0)
    e = [(0, 1, 3, 2)]
    kb = komponentenbezug(daten.punkte.koordinaten_m, e, sf)
    assert kb.zerlegung is not None and kb.ellipse is not None
    np.testing.assert_allclose(kb.normale_punkt, np.tile([0, 0, 1.0], (4, 1)), atol=1e-12)
    # Komponenten X: 0,3·y, Y: 0,5i·y, Z: y → η = 1/(0,09 + 0,25 + 1)
    np.testing.assert_allclose(kb.zerlegung.anteil_normal, 1 / 1.34, rtol=1e-6)
    kb2 = komponentenbezug(
        daten.punkte.koordinaten_m,
        e,
        sf,
        annahmen2=AnnahmenStufe2(drehung_komponenten=[[0, 0, 1], [0, 1, 0], [-1, 0, 0]]),
    )
    assert kb2.zerlegung is not None
    np.testing.assert_allclose(kb2.zerlegung.anteil_normal, 0.09 / 1.34, rtol=1e-6)
    ohne = komponentenbezug(
        daten.punkte.koordinaten_m,
        e,
        schwingform_aus(werte_aus(daten).daten, 100.0, referenz="Ref9"),
    )
    assert ohne.zerlegung is None and HINWEIS_OHNE_PHASE in ohne.hinweise
    nur = komponentenbezug(daten.punkte.koordinaten_m, e)
    assert nur.zerlegung is None and math.isnan(nur.f_hz)
    null = sf.__class__(**{**sf.__dict__, "amplitude": np.zeros((4, 3), dtype=complex)})
    kb3 = komponentenbezug(daten.punkte.koordinaten_m, e, null)
    assert any("Amplitude 0" in h for h in kb3.hinweise)


def test_annahmen_stufe2() -> None:
    a = AnnahmenStufe2()
    eintraege = a.eintraege()
    assert [x.nr for x in eintraege] == list(ANNAHME_NUMMERN_STUFE2)
    assert all(x.status == ANNAHME for x in eintraege)
    assert not set(ANNAHME_NUMMERN_STUFE2) & set(ANNAHME_NUMMERN)  # Stufe 1 unverändert
    assert np.array_equal(a.drehung, np.eye(3)) and np.array_equal(a.e_ref_vektor, [0, 0, 1.0])
    b = AnnahmenStufe2(
        e_ref=(0, 0, 2),
        status={"M13": "bestätigt am 2026-11-02"},
        drehung_komponenten=[[0, -1, 0], [1, 0, 0], [0, 0, 1]],
    )
    assert b.e_ref == (0.0, 0.0, 1.0) and b.status_von("M13").startswith("bestätigt")
    assert "0 -1 0" in b.eintraege()[0].wert
    for kw in (
        {"drehung_komponenten": [[1, 0], [0, 1]]},
        {"drehung_komponenten": [[1, 0, 0], [0, 1, 0], [0, 0, -1]]},
        {"e_ref": (0, 0, 0)},
        {"elemente_index_basis": 2},
        {"zeitstempel": "zeit_c"},
        {"status": {"M1": "x"}},
        {"status": {"M12": " "}},
    ):
        with pytest.raises(ValueError):
            AnnahmenStufe2(**kw)
    with pytest.raises(ValueError):
        a.status_von("M1")


def test_schwellen_stufe2() -> None:
    s = SchwellenStufe2()
    assert (s.rho_max, s.sd_zeta_rel_max, s.n_fit, s.n_max, s.n_punkte) == (0.10, 0.2, 6, 4, 20)
    assert (s.df_tol_faktor, s.d_tol_faktor, s.zuordnung, s.gewichtung) == (
        2.0,
        0.5,
        "label",
        "keine",
    )
    for kw in (
        {"n_fit": 0},
        {"n_max": True},
        {"rho_max": -1.0},
        {"drift_min_punkte": 2},
        {"zeta_min": 0.5},
        {"gewichtung": "x"},
        {"punktauswahl": "x"},
        {"zuordnung": "x"},
    ):
        with pytest.raises(ValueError):
            SchwellenStufe2(**kw)
