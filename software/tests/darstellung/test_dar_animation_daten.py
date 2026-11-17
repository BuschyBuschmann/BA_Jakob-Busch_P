"""Datenvertrag der 3D-Animation (R-071, Plan P-AUSW3 AN3): Referenzfälle RF-A* auf Datenebene.

Die Sollwerte stammen aus FG-04 Abschnitt 5 und Nachtrag 1. Toleranzen: ``rtol = 1e-12`` für
geschlossene Ausdrücke (reine float64-Rundung, FG-04 5); Zahlen, die die Fachgrundlage nur mit
begrenzter Stellenzahl druckt, mit der halben Einheit der letzten angegebenen Stelle
(KONVENTIONEN); Nullwerte mit ``atol = 1e-12·a`` (Rundungsrest von θ_n, ``a`` = Amplitude).
"""

from __future__ import annotations

import dar_daten as dd
import numpy as np
import pytest
from dar_animation_hilfen import KohaerenzCache, messdaten_mit_amplitude

from ldv_automation.auswertung.animation import animierte_amplitude, bildwinkel, maximum_theta
from ldv_automation.auswertung.daten import Messdaten
from ldv_automation.auswertung.gesamt import schwingform_aus
from ldv_automation.darstellung.animation_daten import (
    BEWEGT,
    KEIN_WERT,
    NULL,
    TEXT_KEINE_PHASE,
    TEXT_KEINE_PUNKTE,
    UNGUELTIG,
    UNSICHER,
    AnimationsDaten,
    BezugModus,
    animation_daten,
)
from ldv_automation.darstellung.auswahl import DarstellungsFehler, PaarCache

#: a = 1 mm/s / ω bei 100 Hz (FG-04 5)
A_MM = 1e-3 / (2.0 * np.pi * 100.0)
TH_N = np.array([0.0, np.pi / 2.0, np.pi, 3.0 * np.pi / 2.0])
TH_13 = np.linspace(0.0, 2.0 * np.pi, 13)
KOORD_2 = [[0.0, 0.0, 0.0], [0.029, 0.0, 0.0]]


# --- RF-A1, RF-A2: Einzelpunkt -----------------------------------------------------------------


def test_rf_a1_einzelpunkt_reell() -> None:
    md = messdaten_mit_amplitude(np.array([1e-3]))
    a = animation_daten(md, KohaerenzCache(md), 100.0, komponente="Z", bezug_modus="absolut")
    assert a.f_hz == 100.0
    assert a.einheit_anim == "m"
    # d = -i * 1,5915494309e-6 m, Fachwert mit 11 Stellen: halbe Einheit der letzten Stelle
    assert a.amplitude_anim[0, 2] == pytest.approx(-1j * 1.5915494309e-6, abs=0.5e-16)
    # geschlossener Ausdruck: rtol 1e-12
    assert a.amplitude_anim[0, 2] == pytest.approx(-1j * A_MM, rel=1e-12)
    z = np.array([a.positionen(t, 1.0)[0, 2] for t in TH_N])
    assert z == pytest.approx([0.0, A_MM, 0.0, -A_MM], rel=1e-12, abs=1e-12 * A_MM)
    # Einzelkomponente: die beiden anderen Achsen bewegen sich nicht
    assert np.array_equal(a.positionen(1.0, 1.0)[0, :2], a.koordinaten_m[0, :2])
    assert list(a.achsen_aktiv) == [False, False, True]


def test_rf_a1_h1_einheit_m_je_n() -> None:
    md = messdaten_mit_amplitude(np.array([1.0]))
    a = animation_daten(
        md, KohaerenzCache(md), 100.0, komponente="Z", bezug_modus="absolut", quelle="h1"
    )
    assert a.einheit_anim == "m/N"
    assert a.amplitude_anim[0, 2] == pytest.approx(-1j * 1.5915494309e-3, abs=0.5e-13)


def test_rf_a1_schnelle_ohne_division() -> None:
    md = messdaten_mit_amplitude(np.array([1e-3]))
    a = animation_daten(
        md, KohaerenzCache(md), 100.0, komponente="Z", bezug_modus="absolut", groesse="schnelle"
    )
    assert a.einheit_anim == "m/s"
    u = np.array([a.positionen(t, 1.0)[0, 2] for t in TH_N])
    # u(θ_n) = 1e-3; 0; -1e-3; 0 (m/s, Rundungsrest atol 1e-12·1e-3)
    assert u == pytest.approx([1e-3, 0.0, -1e-3, 0.0], rel=1e-12, abs=1e-15)


def test_rf_a2_einzelpunkt_mit_phase() -> None:
    md = messdaten_mit_amplitude(np.array([1e-3 * np.exp(1j * np.pi / 3.0)]))
    a = animation_daten(md, KohaerenzCache(md), 100.0, komponente="Z", bezug_modus="absolut")
    d = np.array([a.auslenkung(t)[0, 2] for t in TH_N]) / A_MM
    # sin(θ_n + π/3): geschlossener Ausdruck
    assert d == pytest.approx([0.8660254038, 0.5, -0.8660254038, -0.5], rel=1e-9)
    assert d == pytest.approx(np.sin(TH_N + np.pi / 3.0), rel=1e-12, abs=1e-12)


def test_rf_a3_zwei_punkte_gegenphasig() -> None:
    md = messdaten_mit_amplitude(np.array([1e-3, -1e-3]), koordinaten_m=KOORD_2)
    a = animation_daten(md, KohaerenzCache(md), 100.0, komponente="Z")
    d1 = np.array([a.auslenkung(t)[0, 2] for t in TH_13])
    d2 = np.array([a.auslenkung(t)[1, 2] for t in TH_13])
    assert d2 == pytest.approx(-d1, rel=0.0, abs=1e-12 * A_MM)
    assert d1 + d2 == pytest.approx(0.0, abs=1e-12 * A_MM)
    # Phasenunterschied einheitlich +180° (relativ zum Bezug, hier Punkt 0 wegen Gleichstand)
    w = a.amplitude_anim[:, 2] * 1j * a.omega_rad_s
    assert abs(np.angle(w[1] / w[0])) == pytest.approx(np.pi, abs=1e-12)


def test_rf_a4_phasenvorlauf() -> None:
    v = np.array([1e-3, 1j * 1e-3])
    md = messdaten_mit_amplitude(v, koordinaten_m=KOORD_2)
    a = animation_daten(md, KohaerenzCache(md), 100.0, komponente="Z", bezug_modus="absolut")
    # θ_max = π/2 - φ (Weg) bzw. aus d̂ direkt: θ_max = -arg d̂
    theta_max = np.mod(-np.angle(a.amplitude_anim[:, 2]), 2.0 * np.pi)
    assert theta_max == pytest.approx([np.pi / 2.0, 0.0], abs=1e-12)
    assert maximum_theta(np.angle(v)) == pytest.approx(theta_max, abs=1e-12)
    # q erreicht das Maximum um T/4 früher: Δt = -T/4 = -2,5 ms bei 100 Hz
    dt = (theta_max[1] - theta_max[0]) / a.omega_rad_s
    assert dt == pytest.approx(-2.5e-3, rel=1e-12)


def test_rf_a6_kreisbahn_3d() -> None:
    md = messdaten_mit_amplitude(np.array([[1e-3, 1e-3j, 0.0]]))
    a = animation_daten(md, KohaerenzCache(md), 100.0, komponente="3D")
    d = np.array([a.auslenkung(t)[0] for t in TH_N]) / A_MM
    soll = np.array([[0, 1, 0], [1, 0, 0], [0, -1, 0], [-1, 0, 0]], dtype=float)
    assert d == pytest.approx(soll, abs=1e-12)
    assert a.bezug_komponente == 0  # Gleichstand X/Y: kleinster Index (Nachtrag 1)
    assert a.achsen_aktiv.all()


# --- RF-A7, RF-A8: Überhöhung, maskierte Punkte ---------------------------------------------


def _s(a: AnimationsDaten) -> float:
    assert a.s_auto is not None
    return a.s_auto


def _a7() -> Messdaten:
    koord = [[0.0, 0.0, 0.0], [0.029, 0.0, 0.0], [0.058, 0.0, 0.0]]
    return messdaten_mit_amplitude(np.array([1e-3, 0.5e-3, 1e-2]), koordinaten_m=koord)


def test_rf_a7_ueberhoehung() -> None:
    md = messdaten_mit_amplitude(np.array([1e-3, 0.5e-3]), koordinaten_m=KOORD_2)
    a = animation_daten(md, KohaerenzCache(md), 100.0, komponente="Z")
    # Fachwerte (FG-04 5): D_ref = 1,5915494309e-6 m, s = 4555,3093477, s·D_ref = 7,25e-3 m.
    # Toleranz: halbe Einheit der letzten angegebenen Stelle.
    assert a.d_ref == pytest.approx(1.5915494309e-6, abs=0.5e-15)
    assert a.d_nn_m == pytest.approx(0.029, rel=1e-12)
    assert a.s_auto == pytest.approx(4555.3093477, abs=0.5e-7)
    assert _s(a) * a.d_ref == pytest.approx(7.25e-3, abs=0.5e-5)
    # Verhältnis der angezeigten Amplituden Punkt 2 / Punkt 1 = 0,5 (rtol 1e-12)
    z = np.abs(a.positionen(np.pi / 2.0, _s(a))[:, 2] - a.koordinaten_m[:, 2])
    assert z[1] / z[0] == pytest.approx(0.5, rel=1e-12)


def test_rf_a8_unsicherer_punkt_steht_und_geht_nicht_in_d_ref_ein() -> None:
    md = _a7()
    cache = KohaerenzCache(md, ok=[[1, 1, 1], [1, 1, 1], [1, 1, 0]])
    mit = animation_daten(md, cache, 100.0, komponente="Z")
    assert list(mit.status) == [BEWEGT, BEWEGT, UNSICHER]
    assert not mit.bewegt[2]
    # s unverändert gegenüber RF-A7 (der Punkt mit 1e-2 geht nicht in D_ref ein)
    assert mit.s_auto == pytest.approx(4555.3093477, abs=0.5e-7)
    # Position exakt Ruhelage (Gleichheit), unabhängig von θ und s
    for theta in (0.0, 0.3, 2.0, 5.5):
        for s in (1.0, _s(mit), 1e6):
            assert np.array_equal(mit.positionen(theta, s)[2], mit.koordinaten_m[2])


def test_rf_a8_ungueltig_m6_und_nan_amplitude() -> None:
    koord = [[0.0, 0.0, 0.0], [0.029, 0.0, 0.0], [0.058, 0.0, 0.0], [0.087, 0.0, 0.0]]
    v = np.array([1e-3, 0.5e-3, 1e-2, np.nan])
    md = messdaten_mit_amplitude(v, koordinaten_m=koord)
    cache = KohaerenzCache(md, gueltig=[True, True, False, True])
    a = animation_daten(md, cache, 100.0, komponente="Z")
    assert list(a.status) == [BEWEGT, BEWEGT, UNGUELTIG, KEIN_WERT]
    assert a.s_auto == pytest.approx(4555.3093477, abs=0.5e-7)
    for p in (2, 3):
        assert np.array_equal(a.positionen(1.3, _s(a))[p], a.koordinaten_m[p])
    assert np.isnan(a.farbwert(1.3, 2)[3])
    assert np.isnan(a.betrag(1.3)[2])
    # Rangfolge UNGUELTIG > KEIN_WERT > UNSICHER wie Ansicht 4 (schwingform.py:715-719): ein
    # Punkt, der M6, NaN und unsicher zugleich ist, zählt als UNGUELTIG
    cache2 = KohaerenzCache(md, ok=[[1, 1, 1]] * 3 + [[1, 1, 0]], gueltig=[True] * 3 + [False])
    assert animation_daten(md, cache2, 100.0, komponente="Z").status[3] == UNGUELTIG
    # NaN und unsicher, aber gültig: KEIN_WERT
    cache4 = KohaerenzCache(md, ok=[[1, 1, 1]] * 3 + [[1, 1, 0]])
    assert animation_daten(md, cache4, 100.0, komponente="Z").status[3] == KEIN_WERT
    v2 = np.array([1e-3, 0.5e-3, 1e-2, 1e-3])
    md2 = messdaten_mit_amplitude(v2, koordinaten_m=koord)
    cache3 = KohaerenzCache(md2, ok=[[1, 1, 1]] * 3 + [[1, 1, 0]], gueltig=[True] * 3 + [False])
    assert animation_daten(md2, cache3, 100.0, komponente="Z").status[3] == UNGUELTIG


def test_3d_nur_bei_drei_gueltigen_komponenten() -> None:
    """A-1: eine Komponente unter γ²_min lässt den Punkt stehen („3D unvollständig“)."""
    v = np.array([[1e-3, 2e-3j, 0.5e-3], [1e-3, 1e-3, 1e-3], [0.3e-3, 0.2e-3, 0.1e-3]])
    koord = [[0.0, 0.0, 0.0], [0.03, 0.0, 0.0], [0.06, 0.0, 0.0]]
    md = messdaten_mit_amplitude(v, koordinaten_m=koord)
    cache = KohaerenzCache(md, ok=[[1, 1, 1], [1, 0, 1], [1, 1, 1]])
    a = animation_daten(md, cache, 100.0, komponente="3D")
    assert list(a.status) == [BEWEGT, UNSICHER, BEWEGT]
    assert list(a.grund_3d_unvollstaendig) == [False, True, False]
    assert not a.bewegt[1]
    assert np.array_equal(a.positionen(0.7, 5.0)[1], a.koordinaten_m[1])
    assert a.kohaerenz_ok.shape == (3, 3) and a.kohaerenz.shape == (3, 3)
    assert list(a.kohaerenz_ok[1]) == [True, False, True]
    # derselbe Punkt bewegt sich in der Einzelkomponente Z, deren γ² genügt
    z = animation_daten(md, cache, 100.0, komponente="Z")
    assert z.status[1] == BEWEGT and not z.grund_3d_unvollstaendig[1]
    # Einzelkomponente: die nicht gewählten Spalten von kohaerenz sind NaN, ok True
    assert np.isnan(z.kohaerenz[:, :2]).all() and z.kohaerenz_ok[:, :2].all()


def test_nicht_bewegter_bezug_in_3d_wird_abgelehnt() -> None:
    """A-2: ein Bezugspunkt mit maskierter Komponente steht und hat keinen Nulldurchgang."""
    v = np.array([[1e-3, 2e-3j, 0.5e-3], [1e-3, 1e-3, 1e-3]])
    md = messdaten_mit_amplitude(v, koordinaten_m=KOORD_2)
    cache = KohaerenzCache(md, ok=[[1, 0, 1], [1, 1, 1]])
    a = animation_daten(md, cache, 100.0, komponente="3D")
    assert a.bezug_index == 1  # Voreinstellung A-3: der einzige bewegte Punkt
    with pytest.raises(DarstellungsFehler, match="nicht animiert"):
        animation_daten(md, cache, 100.0, komponente="3D", bezug=0)


# --- RF-A9 bis RF-A11 ----------------------------------------------------------------------


def test_rf_a9_linienfrequenz_nicht_gewaehlte_frequenz() -> None:
    md = messdaten_mit_amplitude(
        np.array([1e-3]), delta_f_hz=0.625, k_linien=200, koordinaten_m=[[0.0, 0.0, 0.0]]
    )
    a = animation_daten(md, KohaerenzCache(md), 100.2, komponente="Z", bezug_modus="absolut")
    assert a.f_wahl_hz == pytest.approx(100.2, rel=1e-12)
    assert a.f_hz == 100.0
    assert a.linie == 159
    assert abs(a.amplitude_anim[0, 2]) == pytest.approx(1.5915494309e-6, abs=0.5e-15)
    assert abs(a.amplitude_anim[0, 2]) == pytest.approx(A_MM, rel=1e-12)
    # mit f_wahl gerechnet wäre es 1,5883726855e-6 m (-0,1996 %): das Testergebnis unterscheidet
    assert abs(a.amplitude_anim[0, 2]) != pytest.approx(1.5883726855e-6, rel=1e-4)


V_A10 = 1e-3 * np.array([1.0, 0.5 * np.exp(1.1j), 0.8 * np.exp(-2.0j)])


def _a10(
    vorzeichen: float, *, bezug_modus: BezugModus = "relativ", bezug: int | None = None
) -> AnimationsDaten:
    md = messdaten_mit_amplitude(
        (vorzeichen * V_A10).reshape(1, 3).repeat(2, axis=0) * np.array([[1.0], [0.5]]),
        koordinaten_m=KOORD_2,
    )
    return animation_daten(
        md, KohaerenzCache(md), 100.0, komponente="3D", bezug_modus=bezug_modus, bezug=bezug
    )


def test_rf_a10_polaritaet_m8_absolut_um_n_halbe_verschoben() -> None:
    plus = _a10(+1.0, bezug_modus="absolut")
    minus = _a10(-1.0, bezug_modus="absolut")
    n = 36
    theta = bildwinkel(n)
    for j in range(n):
        assert minus.positionen(theta[j], 1.0) == pytest.approx(
            plus.positionen(theta[(j + n // 2) % n], 1.0),
            rel=0.0,
            abs=1e-12 * A_MM,
        )


def test_rf_a10_polaritaet_m8_relativ_identisch() -> None:
    plus = _a10(+1.0, bezug=0)
    minus = _a10(-1.0, bezug=0)
    assert plus.amplitude_anim == pytest.approx(minus.amplitude_anim, rel=1e-12, abs=1e-18)
    for theta in bildwinkel(36):
        assert minus.positionen(theta, 3.0) == pytest.approx(
            plus.positionen(theta, 3.0),
            rel=0.0,
            abs=1e-12 * A_MM,
        )


def test_rf_a11_relative_amplitude_und_phasen() -> None:
    md = messdaten_mit_amplitude(V_A10.reshape(1, 3), koordinaten_m=[[0.0, 0.0, 0.0]])
    # Einzelkomponente je Spalte: gedrehte Phase relativ zur Komponente des Bezugs
    kern = schwingform_aus(md, 100.0, referenz="Ref1")
    assert kern.amplitude is not None
    a = animation_daten(md, KohaerenzCache(md), 100.0, komponente="3D", bezug=0)
    w = a.amplitude_anim[0] * 1j * a.omega_rad_s
    assert w[0] == pytest.approx(1e-3, rel=1e-12)  # ŵ_0 reell positiv (Pivot X, größter Betrag)
    assert abs(w[0].imag) < 1e-12 * 1e-3
    # Phasendifferenzen (0; 1,1; -2,0) rad (FG-04 RF-A11, Fachwerte mit 2 Stellen)
    assert np.angle(w) == pytest.approx([0.0, 1.1, -2.0], abs=1e-12)
    assert np.degrees(np.angle(w)) == pytest.approx([0.0, 63.03, -114.59], abs=0.005)


# --- RF-A14 und Randfälle --------------------------------------------------------------------


def test_rf_a14_ohne_phase_darstellungsfehler() -> None:
    md = dd.synthetische_messdaten(referenz=False)
    with pytest.raises(DarstellungsFehler) as exc:
        animation_daten(md, PaarCache(md), 10.0)
    assert str(exc.value) == TEXT_KEINE_PHASE == "Animation braucht eine Phase: keine Referenz."


def test_frequenz_ausserhalb_der_achse() -> None:
    md = messdaten_mit_amplitude(np.array([1e-3]))
    with pytest.raises(DarstellungsFehler):
        animation_daten(md, KohaerenzCache(md), 1e9, komponente="Z")


def test_alle_punkte_unsicher_oder_ungueltig_meldung_statt_division() -> None:
    md = messdaten_mit_amplitude(np.array([1e-3, 2e-3]), koordinaten_m=KOORD_2)
    cache = KohaerenzCache(md, ok=[[1, 1, 0], [1, 1, 0]])
    with pytest.raises(DarstellungsFehler) as exc:
        animation_daten(md, cache, 100.0, komponente="Z")
    assert str(exc.value) == TEXT_KEINE_PUNKTE == "Keine Punkte mit gültiger Phase."
    cache2 = KohaerenzCache(md, gueltig=[False, False])
    with pytest.raises(DarstellungsFehler, match="Keine Punkte"):
        animation_daten(md, cache2, 100.0, komponente="Z")


def test_d_ref_null_ist_meldung_nicht_division_durch_null() -> None:
    md = messdaten_mit_amplitude(np.array([0.0, 0.0]), koordinaten_m=KOORD_2)
    # v = 0 bei erreichter γ²-Schwelle: bewegt sich nicht, kein Kennzeichen, D_ref = 0
    with pytest.raises(DarstellungsFehler, match="Keine Punkte"):
        animation_daten(md, KohaerenzCache(md), 100.0, komponente="Z", bezug_modus="absolut")
    # relativ: ohne Punkt mit v != 0 gibt es keinen Bezug (gleiche Meldung)
    with pytest.raises(DarstellungsFehler, match="Keine Punkte"):
        animation_daten(md, KohaerenzCache(md), 100.0, komponente="3D")


def test_nullpunkt_hat_status_null_und_steht() -> None:
    md = messdaten_mit_amplitude(np.array([1e-3, 0.0]), koordinaten_m=KOORD_2)
    a = animation_daten(md, KohaerenzCache(md), 100.0, komponente="Z")
    assert list(a.status) == [BEWEGT, NULL]
    assert a.bewegt[1]  # zählt zur Maske des Kerns (Auslenkung 0, gültig)
    assert np.array_equal(a.positionen(1.0, 100.0)[1], a.koordinaten_m[1])
    assert a.bezug_index == 0  # ein Punkt mit v = 0 liefert keine Bezugsphase


def test_ein_punkt_kein_nachbarabstand_kein_automatisches_s() -> None:
    md = messdaten_mit_amplitude(np.array([1e-3]))
    a = animation_daten(md, KohaerenzCache(md), 100.0, komponente="Z", bezug_modus="absolut")
    assert a.d_nn_m is None and a.d_nn_min_m is None and a.s_auto is None
    assert a.hinweis_ueberhoehung(1e9) is None


def test_hinweis_ueberlagerung_ab_halbem_nachbarabstand() -> None:
    md = messdaten_mit_amplitude(np.array([1e-3, 0.5e-3]), koordinaten_m=KOORD_2)
    a = animation_daten(md, KohaerenzCache(md), 100.0, komponente="Z")
    grenze = 0.5 * 0.029 / a.d_ref
    assert a.hinweis_ueberhoehung(0.99 * grenze) is None
    assert a.hinweis_ueberhoehung(grenze) == "Punkte können sich überlagern"
    assert a.hinweis_ueberhoehung(_s(a)) is None  # alpha = 0,25 < 0,5


def test_bezug_fehler_und_parameterpruefung() -> None:
    md = messdaten_mit_amplitude(np.array([1e-3, 0.5e-3]), koordinaten_m=KOORD_2)
    cache = KohaerenzCache(md)
    with pytest.raises(DarstellungsFehler):
        animation_daten(md, cache, 100.0, komponente="Z", bezug=5)
    with pytest.raises(DarstellungsFehler, match="Unbekannte Komponente"):
        animation_daten(md, cache, 100.0, komponente="W")
    with pytest.raises(ValueError, match="bezug_modus"):
        animation_daten(md, cache, 100.0, komponente="Z", bezug_modus="beliebig")  # type: ignore[arg-type]
    with pytest.raises(DarstellungsFehler, match="gewählte"):
        animation_daten(md, cache, 100.0, komponente="Z", bezug_komponente=0)
    # Pivot-Komponente mit |v| = 0 (3D): Meldung des Kerns als DarstellungsFehler
    v = np.array([[1e-3, 1e-3, 0.0], [1e-3, 0.0, 1e-3]])
    md3 = messdaten_mit_amplitude(v, koordinaten_m=KOORD_2)
    with pytest.raises(DarstellungsFehler):
        animation_daten(
            md3, KohaerenzCache(md3), 100.0, komponente="3D", bezug=0, bezug_komponente=2
        )
    with pytest.raises(ValueError, match="Komponente"):
        animation_daten(md3, KohaerenzCache(md3), 100.0, komponente="3D").farbwert(0.0, 3)


def test_bezug_komponente_einzel_ist_die_gewaehlte() -> None:
    md = messdaten_mit_amplitude(np.array([1e-3, 0.5e-3]), koordinaten_m=KOORD_2)
    a = animation_daten(md, KohaerenzCache(md), 100.0, komponente="Z", bezug_komponente=2)
    assert a.bezug_komponente == 2 and a.bezug_index == 0 and a.bezug_modus == "relativ"
    absolut = animation_daten(md, KohaerenzCache(md), 100.0, komponente="Z", bezug_modus="absolut")
    assert absolut.bezug_index is None and absolut.bezug_komponente is None


# --- Kern, Cache, Farbgrößen -----------------------------------------------------------------


def test_amplituden_bitgleich_zum_kern_und_cache_haelt_drei_paare() -> None:
    md = dd.synthetische_messdaten()
    cache = PaarCache(md)
    assert cache.groesse == 2
    a = animation_daten(md, cache, 10.0, komponente="3D")
    assert cache.groesse == 3
    assert len(cache.gespeichert()) == 3
    kern = schwingform_aus(md, 10.0, referenz="Ref1")
    assert kern.amplitude is not None
    assert np.array_equal(a.amplitude_v, kern.amplitude)
    erwartet = animierte_amplitude(
        kern.amplitude, kern.f_hz, bezug=a.bezug_index, komponente=None, bewegt=a.bewegt
    )
    assert np.array_equal(a.amplitude_anim[a.bewegt], erwartet[a.bewegt])
    assert np.isnan(a.amplitude_anim[~a.bewegt]).all()
    # Kohärenz je Komponente aus dem echten Cache
    for c, kanal in enumerate(("Vib X", "Vib Y", "Vib Z")):
        frf = cache.paar(kanal, "Ref1").frf
        assert np.array_equal(a.kohaerenz[:, c], frf.kohaerenz[:, kern.linie])
        assert np.array_equal(a.kohaerenz_ok[:, c], frf.kohaerenz_ok[:, kern.linie])
    assert a.kohaerenz_min == cache.paar("Vib X", "Ref1").frf.kohaerenz_min
    assert a.ebene == "xy" and a.farb_komponente_standard() == 2
    assert a.anzahl_punkte == dd.P and a.phase_gueltig
    # Standardreferenz und Annahmen/Hinweise aus dem Kern
    assert a.referenz == "Ref1" and a.annahmen == kern.annahmen and a.hinweise == kern.hinweise


def test_farbgroessen_ueber_volle_periode() -> None:
    md = dd.synthetische_messdaten()
    a = animation_daten(md, PaarCache(md), 10.0, komponente="3D")
    theta = np.linspace(0.0, 2.0 * np.pi, 3601)
    z_max = max(float(np.max(np.abs(a.farbwert(t, 2)[a.bewegt]))) for t in theta[::7])
    assert a.farbgrenze("auslenkung", 2) == pytest.approx(z_max, rel=1e-4)
    b_max = max(float(np.max(a.betrag(t)[a.bewegt])) for t in theta[::7])
    assert a.farbgrenze("betrag", 0) == pytest.approx(b_max, rel=1e-4)
    assert a.farbgrenze("betrag", 0) == a.d_ref
    with pytest.raises(ValueError, match="Komponente"):
        a.farbgrenze("auslenkung", 3)
    # eine Komponente, die überall 0 ist, fällt auf D_ref zurück (kein Intervall der Breite 0)
    md0 = messdaten_mit_amplitude(np.array([[1e-3, 1e-3, 0.0]]))
    a0 = animation_daten(md0, KohaerenzCache(md0), 100.0, komponente="3D")
    assert a0.farbgrenze("auslenkung", 2) == a0.d_ref


def test_farbkomponente_standard_je_ebene_und_einzelkomponente() -> None:
    koord = [[0.0, 0.0, 0.0], [0.0, 0.03, 0.0], [0.0, 0.0, 0.2]]  # Ausdehnung x = 0 → Ebene yz
    md = messdaten_mit_amplitude(np.ones((3, 3)) * 1e-3, koordinaten_m=koord)
    a = animation_daten(md, KohaerenzCache(md), 100.0, komponente="3D")
    assert a.ebene == "yz" and a.farb_komponente_standard() == 0
    x = animation_daten(md, KohaerenzCache(md), 100.0, komponente="Y")
    assert x.farb_komponente_standard() == 1


def test_cache_groesse_wird_nur_bei_3d_erhoeht() -> None:
    """Review MINOR: eine Einzelkomponente braucht nur ein Paar, der Cache bleibt unverändert."""
    md = dd.synthetische_messdaten()
    cache = PaarCache(md)
    assert cache.groesse == 2
    animation_daten(md, cache, 10.0, komponente="Z")
    assert cache.groesse == 2 and len(cache.gespeichert()) == 1
    animation_daten(md, cache, 10.0, komponente="3D")
    assert cache.groesse == 3
