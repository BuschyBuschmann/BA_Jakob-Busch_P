"""Phase relativ zu einem Bezugspunkt und Wahl des Bezugspunkts (P-AUSW T2, FA-AUSW F-4a).

Referenzfall RF-UI-F4a: v = (1, 0,8·e^{iπ}, 0,5·e^{i·0,1}) und -v ergeben dieselben relativen
Phasen (0°, 180°, 5,7296°); die absoluten Phasen von -v sind um 180° verschoben (globale
Drehung der Referenz, M8). Toleranz 1e-12 rad: Rundung der Exponentialfunktion (Größenordnung
1e-16) mit Reserve.
"""

from __future__ import annotations

import math

import numpy as np
import pytest

from ldv_automation.auswertung.schwingform import (
    UMBRUCH_TOLERANZ_RAD,
    phase_relativ_rad,
    waehle_bezugspunkt,
)

V = np.array([1.0, 0.8 * np.exp(1j * math.pi), 0.5 * np.exp(1j * 0.1)])


def test_rf_ui_f4a_relative_phase_ist_unabhaengig_vom_gemeinsamen_vorzeichen() -> None:
    soll = np.array([0.0, math.pi, 0.1])
    np.testing.assert_allclose(phase_relativ_rad(V, 0), soll, rtol=0, atol=1e-12)
    np.testing.assert_allclose(phase_relativ_rad(-V, 0), soll, rtol=0, atol=1e-12)
    np.testing.assert_allclose(
        np.degrees(phase_relativ_rad(V, 0)), [0.0, 180.0, 5.7295779513], atol=1e-9
    )


def test_rf_ui_f4a_absolute_phase_verschiebt_sich_um_180_grad() -> None:
    absolut = np.angle(V)
    gedreht = np.angle(-V)
    differenz = np.mod(gedreht - absolut, 2 * math.pi)
    np.testing.assert_allclose(differenz, math.pi, rtol=0, atol=1e-12)


def test_bezug_beliebig_und_gegenseitig() -> None:
    d02 = phase_relativ_rad(V, 2)
    d20 = phase_relativ_rad(V, 0)
    # Δφ(p; ref) = arg(v_p · conj(v_ref)): zweiter Punkt relativ zu Punkt 2 = π - 0,1
    assert d02[1] == pytest.approx(math.pi - 0.1, abs=1e-12)
    assert d02[2] == pytest.approx(0.0, abs=1e-12)
    assert d20[2] == pytest.approx(0.1, abs=1e-12)


def test_minus_pi_wird_als_plus_pi_ausgegeben() -> None:
    v = np.array([1.0 + 0.0j, complex(-1.0, -0.0), complex(-1.0, -1e-300)])
    ergebnis = phase_relativ_rad(v, 0)
    assert ergebnis[1] == pytest.approx(math.pi, abs=1e-12)
    assert ergebnis[2] == pytest.approx(math.pi, abs=1e-12)
    assert np.all(ergebnis > -math.pi) and np.all(ergebnis <= math.pi)
    assert ergebnis[1] == math.pi and ergebnis[2] == math.pi  # exakt +π, nicht π + ε


def test_ergebnis_liegt_garantiert_in_minus_pi_exklusiv_bis_pi() -> None:
    """Auch Rundungsfälle um den Umbruch (-π + ε) überschreiten +π nie (Bereich (-π, π])."""
    rng = np.random.default_rng(20261104)
    zufall = rng.normal(size=500) + 1j * rng.normal(size=500)
    # Gegenphase mit winzigem Imaginärteil beider Vorzeichen und ε im Bereich der Toleranz
    gegen = np.array(
        [complex(-1.0, s * e) for e in (0.0, 1e-300, 1e-14, 1e-13, 1e-12, 5e-12) for s in (1, -1)]
    )
    v = np.concatenate([[1.0 + 0.0j], gegen, zufall])
    ergebnis = phase_relativ_rad(v, 0)
    assert np.all(ergebnis > -math.pi) and np.all(ergebnis <= math.pi)
    # knapp oberhalb der Toleranz bleibt der Wert unverändert (kein Anheben um 2π)
    abstand = 5 * UMBRUCH_TOLERANZ_RAD
    knapp = phase_relativ_rad(np.array([1.0, complex(-1.0, -abstand)]), 0)
    assert knapp[1] == pytest.approx(-math.pi + abstand, abs=1e-15)


def test_nan_bleibt_nan_und_form_wird_geprueft() -> None:
    v = np.array([1.0 + 0j, complex("nan+nanj"), 1j])
    ergebnis = phase_relativ_rad(v, 0)
    assert math.isnan(ergebnis[1]) and ergebnis[2] == pytest.approx(math.pi / 2)
    with pytest.raises(ValueError, match="bezug"):
        phase_relativ_rad(v, 3)
    with pytest.raises(ValueError, match="bezug"):
        phase_relativ_rad(v, -1)
    with pytest.raises(ValueError, match="amplitude"):
        phase_relativ_rad(np.ones((2, 2), dtype=complex), 0)


def test_waehle_bezugspunkt_groesster_betrag_unter_kohaerenten() -> None:
    betrag = np.array([1.0, 5.0, 3.0, 4.0])
    ok = np.array([True, False, True, True])
    assert waehle_bezugspunkt(betrag, ok) == 3  # Punkt 1 ist größer, aber γ² < γ²_min
    assert waehle_bezugspunkt(betrag, np.ones(4, dtype=bool)) == 1
    assert waehle_bezugspunkt(betrag, ok, gueltig=np.array([True, True, True, False])) == 2


def test_waehle_bezugspunkt_gleichstand_kleinster_index_und_nan() -> None:
    betrag = np.array([2.0, np.nan, 2.0, 1.0])
    assert waehle_bezugspunkt(betrag, np.ones(4, dtype=bool)) == 0
    assert waehle_bezugspunkt(np.array([np.nan, 1.0]), np.array([True, False])) is None


def test_waehle_bezugspunkt_ohne_kandidaten_und_formfehler() -> None:
    assert waehle_bezugspunkt(np.ones(3), np.zeros(3, dtype=bool)) is None
    with pytest.raises(ValueError, match="Form"):
        waehle_bezugspunkt(np.ones(3), np.ones(2, dtype=bool))


def test_waehle_bezugspunkt_schliesst_betrag_null_aus() -> None:
    """MINOR-2: |v_ref| = 0 liefert keine Bezugsphase und darf nicht gewählt werden."""
    betrag = np.array([0.0, 2.0, 0.0, 1.0])
    alle = np.ones(4, dtype=bool)
    assert waehle_bezugspunkt(betrag, alle) == 1  # Punkt 0 und 2 haben |v| = 0
    # Kein Kandidat mit |v| > 0 unter den kohärenten Punkten: kein Bezugspunkt
    assert waehle_bezugspunkt(np.array([0.0, 3.0]), np.array([True, False])) is None
    assert waehle_bezugspunkt(np.zeros(4), alle) is None
    # Nicht-Null-Fälle unverändert: größter Betrag gewinnt, Gleichstand kleinster Index
    assert waehle_bezugspunkt(np.array([0.0, 1.0, 1.0]), np.ones(3, dtype=bool)) == 1
    # Unendliche Beträge zählen wie NaN nicht (konsistent zu _pruefe_bezug)
    assert waehle_bezugspunkt(np.array([np.inf, 1.0]), np.ones(2, dtype=bool)) == 1
