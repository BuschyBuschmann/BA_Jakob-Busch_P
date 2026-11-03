"""Kern-Zusätze für die Auswertungsoberfläche (P-AUSW T1.3), rein additiv.

- ``referenzen_aus`` (Referenzkanäle für die Parameterzeile),
- Hinweis-Konstanten der Mittelformeln (FA-AUSW F-2, RF-UI-F2a/F2d) mit den Referenzwerten,
- ``daempfung_der_spitze`` (öffentlich, identisch zur bisherigen Exportstruktur),
- ``berechne_baender`` (öffentlicher Wrapper, identisch zu ``werte_aus``).

Das Laden aus Dateien (``lade_svd``) steht in ``tests/tools/svd_analyse/test_svd_laden.py``
(synthetische Streams) und ``test_aw_laden_datei.py`` (Beispieldatei).
"""

from __future__ import annotations

import math

import aw_referenz as ref
import numpy as np
import pytest

from ldv_automation.auswertung import Messdaten, werte_aus
from ldv_automation.auswertung.export import METHODE_SPITZEN, daempfung_der_spitze
from ldv_automation.auswertung.gesamt import berechne_baender
from ldv_automation.auswertung.laden import referenzen_aus
from ldv_automation.auswertung.mittel import (
    HINWEIS_MITTEL_3D,
    HINWEIS_MITTEL_KOHAERENT,
    HINWEIS_MITTEL_LEISTUNG,
    KENNZEICHEN_3D_MITTEL_UNGEPRUEFT,
    punktmittel_betrag,
)
from ldv_automation.auswertung.spektren import betrag_3d, spektrum_leistung, staple_3d
from ldv_automation.auswertung.spitzen import Spitze

# --- referenzen_aus ---------------------------------------------------------------------------


def _daten_mit_paaren(paare: list[tuple[str, str]]) -> Messdaten:
    k = 8
    f = 0.5 * np.arange(1, k + 1, dtype=np.float64)
    kanaele = {kk for p in paare for kk in p}
    ap = {kk: np.ones((2, k)) for kk in kanaele}
    cp = {p: np.ones((2, k), dtype=np.complex128) for p in paare}
    return ref.messdaten(frequenz_hz=f, ap=ap, cp=cp)


def test_referenzen_aus_eindeutige_zweite_kanaele_in_reihenfolge_des_auftretens() -> None:
    paare = [
        ("Vib X", "Ref1"),
        ("Vib Y", "Ref1"),
        ("Ref2", "Ref1"),
        ("Vib X", "Ref2"),
        ("Vib Y", "Ref2"),
    ]
    daten = _daten_mit_paaren(paare)
    assert referenzen_aus(daten) == (("Ref1", "N"), ("Ref2", "m/s²"))


def test_referenzen_aus_ohne_kreuzspektrum_ist_leer() -> None:
    f = 0.5 * np.arange(1, 5, dtype=np.float64)
    daten = ref.messdaten(frequenz_hz=f, ap={"Vib Z": np.ones((2, 4))})
    assert referenzen_aus(daten) == ()


def test_referenzen_aus_antwort_wird_nicht_zur_referenz() -> None:
    # (Ref2, Ref1): nur der zweite Kanal Ref1 ist Referenz, Ref2 ist hier Antwort
    daten = _daten_mit_paaren([("Ref2", "Ref1")])
    assert referenzen_aus(daten) == (("Ref1", "N"),)


# --- Hinweis-Konstanten der Mittelformeln (RF-UI-F2a, F2d) ------------------------------------


def test_rf_ui_f2a_mittel_von_cph_ist_das_betragsmittel() -> None:
    """Drei Punkte als Zeilen: |CPH| = (3, 4, 5) → Betragsmittel 4, quadratisch 4,0825."""
    cph = np.array([[3.0 + 0.0j], [4.0j], [-5.0 + 0.0j]])  # (P=3, K=1)
    m = punktmittel_betrag(cph)
    assert m.mittel_betrag is not None and m.mittel_quadratisch is not None
    # exakt rechenbar: (3 + 4 + 5)/3 = 4; sqrt((9 + 16 + 25)/3) = sqrt(50/3)
    np.testing.assert_allclose(m.mittel_betrag, [4.0], rtol=1e-12, atol=0.0)
    np.testing.assert_allclose(m.mittel_quadratisch, [math.sqrt(50.0 / 3.0)], rtol=1e-12, atol=0.0)
    assert math.isclose(math.sqrt(50.0 / 3.0), 4.0824829, rel_tol=1e-7)


def test_rf_ui_f2a_f2d_mittel_von_sqrt_ap_ist_das_quadratische_mittel() -> None:
    """AP = (16, 25, 36): √AP-Mittel = √(77/3) = 5,06623 (PSV); das Betragsmittel wäre 5."""
    ap = np.array([[16.0], [25.0], [36.0]])  # (P=3, K=1)
    m = punktmittel_betrag(spektrum_leistung(ap))
    assert m.mittel_quadratisch is not None and m.mittel_betrag is not None
    np.testing.assert_allclose(m.mittel_quadratisch, [math.sqrt(77.0 / 3.0)], rtol=1e-12, atol=0.0)
    assert math.isclose(math.sqrt(77.0 / 3.0), 5.06623, rel_tol=1e-6)
    # das Betragsmittel (4 + 5 + 6)/3 = 5 ist NICHT das PSV-Mittel und unterscheidet sich
    np.testing.assert_allclose(m.mittel_betrag, [5.0], rtol=1e-12, atol=0.0)
    assert not math.isclose(float(m.mittel_betrag[0]), float(m.mittel_quadratisch[0]), rel_tol=1e-3)


def test_rf_ui_f2d_3d_mittel_ist_mittel_der_punktweisen_3d_betraege() -> None:
    """x = (1, 0), y = (0, 1), z = 0 an zwei Punkten: 3D-Beträge 1 und 1 → Mittel 1,0.

    Der 3D-Betrag der Komponentenmittel wäre √(0,5² + 0,5²) = 0,7071 (anderer Kandidat).
    """
    x = np.array([[1.0], [0.0]])
    y = np.array([[0.0], [1.0]])
    z = np.zeros((2, 1))
    betrag = betrag_3d(staple_3d(x, y, z))  # (P=2, K=1)
    m = punktmittel_betrag(betrag)
    assert m.mittel_betrag is not None
    np.testing.assert_allclose(m.mittel_betrag, [1.0], rtol=1e-12, atol=0.0)
    komponentenmittel = math.hypot(float(x.mean()), float(y.mean()))
    assert math.isclose(komponentenmittel, 0.7071067811865476, rel_tol=1e-12)


def test_hinweise_nennen_formel_und_punktzahl() -> None:
    assert "|CPH|" in HINWEIS_MITTEL_KOHAERENT.format(n=135)
    assert "135 Punkte" in HINWEIS_MITTEL_KOHAERENT.format(n=135)
    assert "√(Mittel von AP)" in HINWEIS_MITTEL_LEISTUNG.format(n=135)
    assert "quadratisches Mittel" in HINWEIS_MITTEL_LEISTUNG.format(n=135)
    # das Betragsmittel von √AP darf nirgends als Formel auftauchen
    assert "Betragsmittel" not in HINWEIS_MITTEL_LEISTUNG
    assert "punktweisen 3D-Beträge" in HINWEIS_MITTEL_3D.format(n=135)
    assert KENNZEICHEN_3D_MITTEL_UNGEPRUEFT == "nicht gegen PSV geprüft"
    assert KENNZEICHEN_3D_MITTEL_UNGEPRUEFT in HINWEIS_MITTEL_3D


# --- daempfung_der_spitze ---------------------------------------------------------------------


def test_daempfung_der_spitze_traegt_zeta_bandgrenzen_und_methode() -> None:
    """R-055: ζ mit Bandgrenzen (-3-dB-Kreuzungen in Hz) und Methode; Struktur wie im Export."""
    s = Spitze(
        k=159,
        f_k_hz=100.0,
        f_sp_hz=100.0,
        hoehe=1.0,
        breite_3db_hz=2.0,
        q=50.0,
        zeta=0.01,
        f_l_hz=99.0,
        f_r_hz=101.0,
        delta=0.0,
        kennzeichen=(),
    )
    assert daempfung_der_spitze(s) == {
        "zeta": 0.01,
        "band_u_hz": 99.0,
        "band_o_hz": 101.0,
        "methode": METHODE_SPITZEN,
    }
    assert METHODE_SPITZEN == "-3dB-Breite"


def test_daempfung_der_spitze_nan_bleibt_erhalten() -> None:
    s = Spitze(
        k=3,
        f_k_hz=1.0,
        f_sp_hz=1.0,
        hoehe=1.0,
        breite_3db_hz=math.nan,
        q=math.nan,
        zeta=math.nan,
        f_l_hz=math.nan,
        f_r_hz=math.nan,
        delta=0.0,
        kennzeichen=("aufloesungsbegrenzt",),
    )
    d = daempfung_der_spitze(s)
    assert math.isnan(d["zeta"]) and math.isnan(d["band_u_hz"]) and math.isnan(d["band_o_hz"])
    assert d["methode"] == METHODE_SPITZEN


# --- berechne_baender -------------------------------------------------------------------------


def test_berechne_baender_ist_identisch_zu_werte_aus() -> None:
    k = 800
    f = 0.5 * np.arange(1, k + 1, dtype=np.float64)
    y = ref.mobilitaet_moden(f, [100.0, 150.0])
    p = 3
    h = np.broadcast_to(y, (p, k)).astype(np.complex128)
    daten = ref.messdaten(
        frequenz_hz=f,
        ap={"Vib Z": (np.abs(h) ** 2 * 1.01).astype(np.float64), "Ref1": np.ones((p, k))},
        cp={("Vib Z", "Ref1"): h},
    )
    grenzen = [(50.0, 200.0), (0.5, 400.0)]
    a = werte_aus(daten, baender=grenzen)
    b = berechne_baender(daten, a.paare, a.mittel_ap, grenzen)
    assert len(a.baender) == len(b) > 0
    for x, y_ in zip(a.baender, b, strict=True):
        assert (x.f_u_hz, x.f_o_hz, x.groesse, x.bezug, x.einheit, x.n_linien, x.hinweise) == (
            y_.f_u_hz,
            y_.f_o_hz,
            y_.groesse,
            y_.bezug,
            y_.einheit,
            y_.n_linien,
            y_.hinweise,
        )
        for feld in ("rms", "rms_psv", "bandnorm"):
            u, v = getattr(x, feld), getattr(y_, feld)
            assert (u is None) == (v is None)
            if u is not None:
                np.testing.assert_array_equal(u, v)  # bitgleich: dieselbe Rechnung


def test_berechne_baender_ohne_grenzen_ist_leer() -> None:
    f = 0.5 * np.arange(1, 9, dtype=np.float64)
    daten = ref.messdaten(frequenz_hz=f, ap={"Vib Z": np.ones((2, 8))})
    a = werte_aus(daten)
    assert berechne_baender(daten, a.paare, a.mittel_ap, []) == ()


@pytest.mark.parametrize("n", [1, 135])
def test_hinweise_lassen_sich_formatieren(n: int) -> None:
    for text in (HINWEIS_MITTEL_KOHAERENT, HINWEIS_MITTEL_LEISTUNG, HINWEIS_MITTEL_3D):
        assert str(n) in text.format(n=n)
