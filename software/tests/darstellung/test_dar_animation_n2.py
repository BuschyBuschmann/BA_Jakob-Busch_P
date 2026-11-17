"""FG-04 Nachtrag 2 (R-071): Skalierung bei Schnelle, räumliches d_NN, Wortlaut θ = 0, DS1.

Referenzfälle RF-S1 bis RF-S7, RF-D1 bis RF-D4, RF-T1 bis RF-T6 und die Datenebene von RF-N1 und
RF-N7 (FG-04 Nachtrag 1, Datensatz DS1). Toleranz: halbe Einheit der letzten angegebenen Stelle
(KONVENTIONEN, Nutzerentscheidung 2026-11-14), Textvergleiche exakt.
"""

from __future__ import annotations

import math
from dataclasses import replace
from typing import Any

import numpy as np
import pytest
from dar_animation_hilfen import KohaerenzCache, messdaten_mit_amplitude

from ldv_automation.darstellung.animation3d import (
    AnimationsOptionen,
    effektive_ueberhoehung,
    nullpunkt_satz,
    pflichttexte,
)
from ldv_automation.darstellung.animation_daten import (
    UNSICHER,
    AnimationsDaten,
    animation_daten,
)
from ldv_automation.darstellung.auswahl import DarstellungsFehler
from ldv_automation.darstellung.stil import THESIS_STIL
from ldv_automation.gui.animation_steuerung import (
    beschreibung_animation,
    skalierung_nach_groessenwechsel,
    skalierung_text,
)

OMEGA = 2.0 * math.pi * 100.0
KOORD_2 = [[0.0, 0.0, 0.0], [0.029, 0.0, 0.0]]
TH_N = (0.0, math.pi / 2.0, math.pi, 3.0 * math.pi / 2.0)
TH_13 = np.linspace(0.0, 2.0 * np.pi, 13)
S_AUTO = 4555.3093477  # FG-04 RF-A7, auch RF-S1
STIL = THESIS_STIL


def _z(v: Any, koord: Any = KOORD_2, *, delta_f: float = 12.5, k: int = 16, **kw: Any) -> Any:
    md = messdaten_mit_amplitude(
        np.asarray(v, dtype=complex), koordinaten_m=koord, delta_f_hz=delta_f, k_linien=k
    )
    return animation_daten(md, KohaerenzCache(md), kw.pop("f", 100.0), **kw)


def _rf_s(**kw: Any) -> AnimationsDaten:
    """Zwei Punkte mit 1,000 und 0,5000 mm/s, Einzelkomponente Z (RF-S1)."""
    return _z([1e-3, 0.5e-3], komponente="Z", **kw)  # type: ignore[no-any-return]


# --- RF-S1 bis RF-S7: Skalierung bei Schnelle ----------------------------------------------------


def test_rf_s1_voreinstellung_schnelle() -> None:
    a = _rf_s(groesse="schnelle")
    assert a.skalierung_einheit == "s"
    assert a.d_ref == pytest.approx(1.0e-3, abs=5e-10)  # mm/s: ±5e-7 mm/s
    assert a.d_ref_auslenkung == pytest.approx(1.591549e-6, abs=5e-13)  # ±5e-7 µm
    assert a.s_auto == pytest.approx(7.250000, abs=5e-7)  # κ_auto in s
    assert a.s_auto_aequivalent == pytest.approx(S_AUTO, abs=5e-5)
    ausl = _rf_s()
    assert ausl.skalierung_einheit == "1" and ausl.s_auto == pytest.approx(S_AUTO, abs=5e-5)
    assert a.s_auto_aequivalent == pytest.approx(ausl.s_auto, rel=1e-12)  # gleiche Bildgröße
    kappa = a.s_auto
    assert kappa is not None
    assert kappa * a.d_ref == pytest.approx(7.25e-3, abs=5e-10)  # größte Bildstrecke in m
    # Bild bei θ_n (Ruhelage z = 0): Punkt 1 ±7,25 mm, Punkt 2 ±3,625 mm
    bild = np.array([a.positionen(t, kappa)[:, 2] for t in TH_N])
    assert bild[:, 0] == pytest.approx([7.25e-3, 0.0, -7.25e-3, 0.0], abs=5e-10)
    assert bild[:, 1] == pytest.approx([3.625e-3, 0.0, -3.625e-3, 0.0], abs=5e-10)
    assert bild[0, 1] / bild[0, 0] == pytest.approx(0.5, abs=5e-7)
    assert effektive_ueberhoehung(a, AnimationsOptionen()) == a.s_auto


def test_rf_s1t_texte_schnelle_und_auslenkung() -> None:
    a = _rf_s(groesse="schnelle")
    ta, tb, _, _ = pflichttexte(a, 0.0, effektive_ueberhoehung(a, AnimationsOptionen()), STIL)
    assert ta == (
        "Skalierung 7,250 s (Bild = Skalierung · Schnelle) · "
        "Amplitude wie Auslenkung mit Überhöhung \N{MULTIPLICATION SIGN}4555"
    )
    assert tb == "größte reale Spitzenschnelle D_ref = 1,00 mm/s (Spitzenauslenkung 1,59 µm)"
    b = _rf_s()
    ta, tb, _, _ = pflichttexte(b, 0.0, effektive_ueberhoehung(b, AnimationsOptionen()), STIL)
    assert ta == "Überhöhung \N{MULTIPLICATION SIGN}4555"
    assert tb == "größte reale Spitzenauslenkung D_ref = 1,59 µm"


def test_rf_s2_schnelle_ist_auslenkung_um_viertelperiode() -> None:
    schnelle = _rf_s(groesse="schnelle")
    ausl = _rf_s()
    kappa, s = 7.25, S_AUTO
    assert schnelle.ueberhoehung_aequivalent(kappa) == pytest.approx(s, abs=5e-5)
    for t in TH_13:
        assert schnelle.positionen(t, kappa) == pytest.approx(
            ausl.positionen(t + math.pi / 2.0, s), abs=5e-10
        )
    # Auslenkung bei θ_n (Punkt 1): 0; +7,25; 0; -7,25 mm
    bild = [ausl.positionen(t, s)[0, 2] for t in TH_N]
    assert bild == pytest.approx([0.0, 7.25e-3, 0.0, -7.25e-3], abs=5e-10)


def test_rf_s3_manuelles_kappa() -> None:
    a = _rf_s(groesse="schnelle")
    assert a.ueberhoehung_aequivalent(2.0) == pytest.approx(1256.637, abs=5e-4)
    amp = [np.max(np.abs(np.array([a.positionen(t, 2.0)[p, 2] for t in TH_13]))) for p in (0, 1)]
    assert amp == pytest.approx([2.0e-3, 1.0e-3], abs=5e-10)
    assert pflichttexte(a, 0.0, 2.0, STIL)[0] == (
        "Skalierung 2,000 s (Bild = Skalierung · Schnelle) · "
        "Amplitude wie Auslenkung mit Überhöhung \N{MULTIPLICATION SIGN}1257"
    )


def test_rf_s4_linie_statt_wunschfrequenz() -> None:
    a = _z([1e-3, 0.5e-3], komponente="Z", groesse="schnelle", f=100.2, delta_f=0.625, k=200)
    assert a.linie == 159 and a.f_hz == pytest.approx(100.0, abs=5e-4)
    assert a.ueberhoehung_aequivalent(7.25) == pytest.approx(S_AUTO, abs=5e-5)
    mit_wunsch = 7.25 * 2.0 * math.pi * 100.2
    assert mit_wunsch == pytest.approx(4564.4200, abs=5e-5)
    assert abs(a.ueberhoehung_aequivalent(7.25) - mit_wunsch) > 1.0  # Test unterscheidet beides


def test_rf_s5_ueberlagerungshinweis_gleich_fuer_beide_bedingungen() -> None:
    a = _rf_s(groesse="schnelle")
    assert a.d_nn_min_m == pytest.approx(0.029, abs=5e-6)
    assert a.hinweis_ueberhoehung(14.4) is None  # 14,40 mm < 14,50 mm
    assert a.hinweis_ueberhoehung(14.6) == "Punkte können sich überlagern"
    for kappa in (14.4, 14.6):
        strecke_v = kappa * a.d_ref
        strecke_d = a.ueberhoehung_aequivalent(kappa) * a.d_ref_auslenkung
        assert strecke_v == pytest.approx(strecke_d, rel=1e-12)
        assert strecke_v == pytest.approx(kappa * 1e-3, abs=5e-6)


def test_rf_s6_quelle_h1() -> None:
    a = _z([1.0, 0.5], komponente="Z", groesse="schnelle", quelle="h1")
    assert a.einheit_anim == "(m/s)/N" and a.einheit_auslenkung == "m/N"
    assert a.d_ref_auslenkung == pytest.approx(1.591549e-3, abs=5e-10)  # mm/N: ±5e-7
    assert a.s_auto == pytest.approx(7.250e-3, abs=5e-6)
    assert a.s_auto_aequivalent == pytest.approx(4.5553, abs=5e-5)
    ta, tb, tc, _ = pflichttexte(a, 0.0, a.s_auto or 0.0, STIL)
    assert tb == "größte reale Spitzenschnelle D_ref = 1,00 (m/s)/N (Spitzenauslenkung 1,59 mm/N)"
    assert tc == "f = 100,000 Hz · Schnelle Z (H1, je 1 N)"
    assert ta.startswith("Skalierung 0,007250 s (Bild = Skalierung · Schnelle)")


def test_rf_s7_negativtest_ueberhoehung_nie_mit_kappa() -> None:
    a = _rf_s(groesse="schnelle")
    text = pflichttexte(a, 0.0, 7.25, STIL)[0]
    assert "Überhöhung \N{MULTIPLICATION SIGN}7,250" not in text
    assert a.ueberhoehung_aequivalent(7.25) / 7.25 == pytest.approx(OMEGA, rel=1e-12)


def test_omega_null_gibt_strich_statt_zahl() -> None:
    a = replace(_rf_s(groesse="schnelle"), omega_rad_s=0.0)
    assert math.isnan(a.ueberhoehung_aequivalent(1.0)) and math.isnan(a.d_ref_auslenkung)
    assert math.isnan(a.skalierung_aus_ueberhoehung(1.0))
    assert a.s_auto_aequivalent is not None and math.isnan(a.s_auto_aequivalent)
    assert pflichttexte(a, 0.0, 1.0, STIL)[0].endswith("Überhöhung \N{MULTIPLICATION SIGN}–")
    assert "Spitzenauslenkung – m)" in pflichttexte(a, 0.0, 1.0, STIL)[1]
    assert effektive_ueberhoehung(replace(a, s_auto=None), AnimationsOptionen()) == 1.0


def test_ohne_zweiten_punkt_gilt_reale_auslenkung_auch_bei_schnelle() -> None:
    a = _z([1e-3], koord=[[0.0, 0.0, 0.0]], komponente="Z", groesse="schnelle")
    assert a.s_auto is None
    kappa = effektive_ueberhoehung(a, AnimationsOptionen())
    assert kappa == pytest.approx(1.0 / OMEGA, rel=1e-12)
    assert a.ueberhoehung_aequivalent(kappa) == pytest.approx(1.0, rel=1e-12)


# --- Bildgröße beim Wechsel der Größe (F-S1) -----------------------------------------------------


def test_groessenwechsel_erhaelt_die_bildgroesse() -> None:
    ausl, schnelle = _rf_s(), _rf_s(groesse="schnelle")
    kappa = skalierung_nach_groessenwechsel(ausl, schnelle, 1256.637)
    assert kappa == pytest.approx(2.0, abs=5e-7)
    s = skalierung_nach_groessenwechsel(schnelle, ausl, kappa)
    assert s == pytest.approx(1256.637, rel=1e-9)
    # gleiche größte Bildstrecke vor und nach dem Wechsel
    assert (kappa or 0.0) * schnelle.d_ref == pytest.approx(1256.637 * ausl.d_ref, rel=1e-9)
    assert skalierung_nach_groessenwechsel(ausl, schnelle, None) is None  # automatisch bleibt
    ohne_omega = replace(schnelle, omega_rad_s=0.0)
    assert skalierung_nach_groessenwechsel(ohne_omega, ausl, 2.0) is None


def test_skalierung_text() -> None:
    ausl, schnelle = _rf_s(), _rf_s(groesse="schnelle")
    assert skalierung_text(ausl, 4555.3093, STIL) == "\N{MULTIPLICATION SIGN}4555"
    assert (
        skalierung_text(schnelle, 7.25, STIL)
        == "7,250 s (entspricht Überhöhung \N{MULTIPLICATION SIGN}4555)"
    )


def test_textalternative_schnelle_nennt_pflichtangaben_und_nullpunkt() -> None:
    a = _rf_s(groesse="schnelle")
    text = beschreibung_animation(a, math.pi / 2.0, None, STIL)
    assert "Skalierung 7,250 s (Bild = Skalierung · Schnelle)" in text
    assert (
        "Überhöhung \N{MULTIPLICATION SIGN}4555" in text and "(Spitzenauslenkung 1,59 µm)" in text
    )
    assert "θ = 90,0° · Bezug: relativ zu Punkt 100 (Referenz Ref1)" in text
    assert "θ = 0°: Schnelle von Punkt 100, Komponente Z im positiven Maximum" in text
    assert "\n" not in text


# --- RF-D1 bis RF-D4: räumlicher Nachbarabstand --------------------------------------------------

_GEKIPPT = [
    [0.0, 0.0, 0.0],
    [0.029, 0.0, 0.0],
    [0.0, 0.029 * math.cos(math.radians(60.0)), 0.029 * math.sin(math.radians(60.0))],
]


def test_rf_d1_geneigte_ebene_raeumlich() -> None:
    a = _z([1e-3, 0.5e-3, 0.5e-3], koord=_GEKIPPT, komponente="Z")
    assert a.d_nn_m == pytest.approx(0.029, abs=5e-6) and a.d_nn_min_m == pytest.approx(
        0.029, abs=5e-6
    )
    assert a.s_auto == pytest.approx(4555.309, abs=5e-4)
    assert a.s_auto != pytest.approx(2277.655, abs=5e-4)  # in der XY-Ebene wäre es die Hälfte
    parallel = [[0.0, 0.0, 0.1], [0.029, 0.0, 0.1], [0.0, 0.029, 0.1]]
    p = _z([1e-3, 0.5e-3, 0.5e-3], koord=parallel, komponente="Z")
    assert p.d_nn_m == pytest.approx(0.029, abs=5e-6)


def test_rf_d2_nicht_animierter_punkt_zaehlt() -> None:
    koord = [*_GEKIPPT, [0.005, 0.0, 0.0]]
    md = messdaten_mit_amplitude(
        np.array([1e-3, 0.5e-3, 0.5e-3, 0.5e-3], dtype=complex), koordinaten_m=koord
    )
    cache = KohaerenzCache(md, ok=[[1, 1, 1]] * 3 + [[1, 1, 0]])
    a = animation_daten(md, cache, 100.0, komponente="Z")
    assert a.status[3] == UNSICHER and not a.bewegt[3]  # steht, zählt aber als Nachbar
    assert a.d_nn_m == pytest.approx(0.0145, abs=5e-6)  # Median von 5; 24; 29; 5 mm
    assert a.d_nn_min_m == pytest.approx(0.005, abs=5e-6)
    assert a.s_auto == pytest.approx(2277.655, abs=5e-4)


def test_rf_d3_ausschluesse() -> None:
    koord = [*_GEKIPPT, _GEKIPPT[0]]  # Duplikat von X0
    a = _z([1e-3, 0.5e-3, 0.5e-3, 0.5e-3], koord=koord, komponente="Z")
    assert a.d_nn_m == pytest.approx(0.029, abs=5e-6)  # Abstand 0 zählt nicht
    ein = _z([1e-3], koord=[[0.0, 0.0, 0.0]], komponente="Z")
    assert ein.d_nn_m is None and ein.d_nn_min_m is None and ein.s_auto is None


def test_rf_d4_beruehrung_erst_ab_halbem_abstand() -> None:
    # Zwei Punkte im Abstand 29 mm, in X gegeneinander (Gegenphase), größte Bildstrecke A
    v = np.array([[1e-3, 0.0, 0.0], [-1e-3, 0.0, 0.0]])
    a = _z(v, komponente="X", bezug_modus="absolut")
    theta = np.linspace(0.0, 2.0 * np.pi, 3601)
    soll = {14.4e-3: 0.2e-3, 14.5e-3: 0.0, 14.6e-3: 0.0}
    for strecke, abstand in soll.items():
        s = strecke / a.d_ref_auslenkung
        d = [np.linalg.norm(np.diff(a.positionen(t, s)[:, :], axis=0)) for t in theta]
        assert min(d) == pytest.approx(abstand, abs=5e-6 + 1e-9)
    # der Hinweis erscheint genau ab 14,50 mm
    assert a.hinweis_ueberhoehung(14.49e-3 / a.d_ref_auslenkung) is None
    assert a.hinweis_ueberhoehung(14.5e-3 / a.d_ref_auslenkung) is not None


# --- RF-T1 bis RF-T6: Bedeutung von θ = 0 --------------------------------------------------------

A = 1e-3 / OMEGA  # |v̂|/ω


def _einzel(v: Any, **kw: Any) -> AnimationsDaten:
    koord = [[0.029 * i, 0.0, 0.0] for i in range(len(np.atleast_1d(v)))]
    return _z(v, koord=koord, komponente="Z", **kw)  # type: ignore[no-any-return]


def test_rf_t1_t2_relativ_einzel() -> None:
    ausl = _einzel([1e-3])
    assert ausl.auslenkung(0.0)[0, 2] == pytest.approx(0.0, abs=5e-13)
    assert ausl.auslenkung(1e-3)[0, 2] > 0.0
    assert ausl.auslenkung(math.pi / 2.0)[0, 2] == pytest.approx(A, abs=5e-13)
    schnelle = _einzel([1e-3], groesse="schnelle")
    assert schnelle.auslenkung(0.0)[0, 2] == pytest.approx(1e-3, abs=5e-10)  # Maximum
    assert schnelle.auslenkung(1e-3)[0, 2] < schnelle.auslenkung(0.0)[0, 2]
    assert schnelle.auslenkung(math.pi / 2.0)[0, 2] == pytest.approx(0.0, abs=5e-10)


def test_rf_t3_zweiter_punkt_relativ() -> None:
    v = [1e-3, 1e-3 * np.exp(0.7j)]
    d = _einzel(v, bezug=0)
    assert d.auslenkung(0.0)[1, 2] / A == pytest.approx(math.sin(0.7), abs=5e-7)
    u = _einzel(v, bezug=0, groesse="schnelle")
    assert u.auslenkung(0.0)[1, 2] / 1e-3 == pytest.approx(math.cos(0.7), abs=5e-7)


def test_rf_t4_absolut() -> None:
    for phi, u_soll in ((0.0, 1e-3), (math.pi, -1e-3)):
        v = [1e-3 * np.exp(1j * phi)]
        d = _einzel(v, bezug_modus="absolut")
        u = _einzel(v, bezug_modus="absolut", groesse="schnelle")
        assert d.auslenkung(0.0)[0, 2] == pytest.approx(0.0, abs=5e-13)
        assert u.auslenkung(0.0)[0, 2] == pytest.approx(u_soll, abs=5e-7 * 1e-3)


def _ds1() -> np.ndarray:
    d = 1e-3
    return d * np.array(
        [
            [0.5, 1.0 * np.exp(1j * math.pi / 3.0), 0.3 * np.exp(-0.4j)],
            [
                0.2 * np.exp(0.2j),
                0.4 * np.exp(1j * (math.pi / 3.0 + math.pi / 2.0)),
                0.1 * np.exp(2.0j),
            ],
            [
                0.3 * np.exp(1.0j),
                0.6 * np.exp(1j * (math.pi / 3.0 - math.pi)),
                0.2 * np.exp(-1.0j),
            ],
        ]
    )


_KOORD_3 = [[0.0, 0.0, 0.0], [0.03, 0.0, 0.0], [0.06, 0.0, 0.0]]


def test_rf_t5_nur_die_bezugskomponente_erfuellt_den_nullpunkt_satz() -> None:
    ds1 = _ds1()
    d = _z(ds1, koord=_KOORD_3, komponente="3D")
    assert d.bezug_index == 0 and d.bezug_komponente == 1  # Pivot Y
    ausl = d.auslenkung(0.0)[0] / (np.abs(ds1[0]) / OMEGA)
    assert ausl == pytest.approx([-0.8660254, 0.0, -0.9923714], abs=5e-7)
    u = _z(ds1, koord=_KOORD_3, komponente="3D", groesse="schnelle")
    assert u.auslenkung(0.0)[0] / np.abs(ds1[0]) == pytest.approx([0.5, 1.0, 0.1232843], abs=5e-7)


def test_rf_n1_n7_ds1_auf_datenebene() -> None:
    """Nachtrag 1, Datensatz DS1 über ``animation_daten`` (nicht nur der Kern)."""
    ds1 = _ds1()
    u = _z(ds1, koord=_KOORD_3, komponente="3D", groesse="schnelle")
    w = u.amplitude_anim
    assert np.angle(w) == pytest.approx(
        np.array(
            [
                [-1.0471975512, 0.0, -1.4471975512],
                [-0.8471975512, math.pi / 2.0, 0.9528024488],
                [-0.0471975512, math.pi, -2.0471975512],
            ]
        ),
        abs=5e-11,
    )
    assert np.abs(w) == pytest.approx(np.abs(ds1), rel=1e-12)
    assert w[0, 1].real == pytest.approx(1e-3, rel=1e-12)  # ŵ_{0Y} reell, positiv
    assert abs(w[0, 1].imag) < 1e-15
    # RF-N7: Voreinstellung b = 0
    assert u.bezug_index == 0
    md = messdaten_mit_amplitude(ds1, koordinaten_m=_KOORD_3)
    maske = [[0, 1, 1], [1, 1, 1], [1, 1, 1]]  # p0 in X unsicher
    cache = KohaerenzCache(md, ok=maske)
    b = animation_daten(md, cache, 100.0, komponente="3D")
    assert b.bezug_index == 2 and b.status[0] == UNSICHER and not b.bewegt[0]
    with pytest.raises(DarstellungsFehler):
        animation_daten(md, cache, 100.0, komponente="3D", bezug=0)
    alle = KohaerenzCache(md, ok=np.zeros((3, 3)))
    with pytest.raises(DarstellungsFehler):
        animation_daten(md, alle, 100.0, komponente="3D")


def test_rf_t6_texte() -> None:
    ausl = _z(np.array([[1e-3, 0.0, 0.0]]), koord=[[0, 0, 0]], komponente="X")
    schnelle = _z(
        np.array([[1e-3, 0.0, 0.0]]), koord=[[0, 0, 0]], komponente="X", groesse="schnelle"
    )
    absolut = _z(
        np.array([[1e-3, 0.0, 0.0]]), koord=[[0, 0, 0]], komponente="X", bezug_modus="absolut"
    )
    assert nullpunkt_satz(absolut) == "θ = 0°: Ref1 im positiven Maximum"
    assert nullpunkt_satz(replace(schnelle, bezug_modus="absolut", bezug_index=None)) == (
        "θ = 0°: Ref1 im positiven Maximum"
    )
    assert nullpunkt_satz(ausl) == (
        "θ = 0°: Auslenkung von Punkt 100, Komponente X steigt durch null; "
        "positives Maximum bei θ = 90°"
    )
    assert nullpunkt_satz(schnelle) == (
        "θ = 0°: Schnelle von Punkt 100, Komponente X im positiven Maximum; "
        "Nulldurchgang bei θ = 90°"
    )
    drei = _z(np.array([[1e-3, 2e-3j, 0.5e-3]]), koord=[[0, 0, 0]], komponente="3D")
    zusatz = "; andere Komponenten mit festem Phasenversatz"
    assert nullpunkt_satz(drei) == (
        "θ = 0°: Auslenkung von Punkt 100, Komponente Y steigt durch null; "
        "positives Maximum bei θ = 90°" + zusatz
    )
    drei_u = _z(
        np.array([[1e-3, 2e-3j, 0.5e-3]]), koord=[[0, 0, 0]], komponente="3D", groesse="schnelle"
    )
    assert nullpunkt_satz(drei_u).endswith("Nulldurchgang bei θ = 90°" + zusatz)
    # Teil von Pflichtangabe (d), auch in der Textalternative
    assert pflichttexte(ausl, 0.0, 1.0, STIL)[3].endswith("\n" + nullpunkt_satz(ausl))
    assert nullpunkt_satz(ausl) in beschreibung_animation(ausl, 0.0, None, STIL)
