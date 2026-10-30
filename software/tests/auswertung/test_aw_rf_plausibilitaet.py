"""Referenzfälle FG-02 9.7 (RF-K1 bis RF-K4) und Plausibilitätsprüfungen P-01 bis P-11.

RF-K1 bis RF-K3 laufen wie im Prüfskript ohne Prominenzauswahl (alle lokalen Maxima, wie
RF-M): Mit W = 20 Linien ist das Fenster bei Δf = 0,05 Hz nur ±1 Hz breit, die
Prominenz 2 wird dort nicht erreicht. RF-K4 nutzt die Prominenzauswahl nach 3.9.
Die Anteile q und r sind exakt (Zählungen).
"""

from __future__ import annotations

import math

import aw_referenz as ref
import numpy as np
import pytest

from ldv_automation.auswertung.annahmen import Annahmen, Schwellen
from ldv_automation.auswertung.plausibilitaet import (
    p01_kreuzspektrum,
    p02_cph,
    p03_vorzeichen,
    p04_jensen,
    p06_frequenzachse,
    p07_phasensinn,
    p08_passivitaet,
    p09_referenzstabilitaet,
    p10_punktstatus,
    p11_annahmen,
    phasensinn_anteil,
    pruefe_eingang,
)

S = Schwellen()
F_K = (np.arange(1, 4000) * 0.05).astype(np.float64)
Y_K = ref.mobilitaet_moden(F_K, [100.0, 120.0])
EINS = np.ones(F_K.size)


@pytest.mark.parametrize(
    ("rf", "frf", "q", "r", "p08_status"),
    [
        ("RF-K1", Y_K, 1.0, 1.0, "ok"),
        ("RF-K2", np.conj(Y_K), 0.0, 1.0, "ok"),
        ("RF-K3", -Y_K, 1.0, 0.0, "warnung"),
    ],
)
def test_rf_k1_bis_k3(rf: str, frf: np.ndarray, q: float, r: float, p08_status: str) -> None:
    ohne_prominenz = Schwellen(prominenz_min=None)
    anteil, anzahl = phasensinn_anteil(F_K, frf, EINS, ohne_prominenz)
    assert anzahl == 2 and anteil == q, rf
    p07 = p07_phasensinn(F_K, frf, EINS, ohne_prominenz)
    assert p07.status == "nicht_pruefbar" and p07.wert == q, rf  # < 10 Spitzen
    mit_eins = p07_phasensinn(F_K, frf, EINS, Schwellen(prominenz_min=None, p07_min_spitzen=1))
    assert mit_eins.wert == q
    assert mit_eins.status == ("fehler" if q == 0.0 else "ok"), rf
    if q == 0.0:
        assert "konjugiert" in mit_eins.grund
    p08 = p08_passivitaet(F_K, frf, EINS, "mobilitaet", S)
    assert p08.wert == r and p08.status == p08_status, rf
    if r == 0.0:
        assert "Vorzeichen" in p08.grund


F_K4 = (0.5 * np.arange(1, 800)).astype(np.float64)
Y_K4 = ref.mobilitaet_moden(F_K4, [float(f) for f in range(100, 321, 20)])
EINS_K4 = np.ones(F_K4.size)


@pytest.mark.parametrize(
    ("name", "frf", "q", "r", "p07_status", "p08_status"),
    [
        ("Y", Y_K4, 1.0, 1.0, "ok", "ok"),
        ("Y*", np.conj(Y_K4), 0.0, 1.0, "fehler", "ok"),
        ("-Y", -Y_K4, 1.0, 0.0, "ok", "warnung"),
    ],
)
def test_rf_k4_zwoelf_moden_mit_mindestanzahl(
    name: str, frf: np.ndarray, q: float, r: float, p07_status: str, p08_status: str
) -> None:
    _, anzahl = phasensinn_anteil(F_K4, frf, EINS_K4, S)
    assert anzahl == 11, name
    p07 = p07_phasensinn(F_K4, frf, EINS_K4, S, bezug=name)
    assert p07.wert == q and p07.status == p07_status, name
    p08 = p08_passivitaet(F_K4, frf, EINS_K4, "mobilitaet", S)
    assert p08.wert == r and p08.status == p08_status, name


def test_p07_warnung_dazwischen_und_kohaerenz_filter() -> None:
    frf = np.vstack([Y_K4, np.conj(Y_K4)])  # 11 fallend, 11 steigend
    p07 = p07_phasensinn(F_K4, frf, np.ones(frf.shape), S)
    assert p07.status == "warnung" and p07.wert == 0.5
    nur_erster = p07_phasensinn(F_K4, frf, np.ones(frf.shape), S, np.array([True, False]))
    assert nur_erster.wert == 1.0
    tief = p07_phasensinn(F_K4, Y_K4, np.full(F_K4.size, 0.5), S)
    assert tief.status == "nicht_pruefbar" and tief.wert is None


def test_p08_akzeleranz_und_dazwischen_und_nicht_pruefbar() -> None:
    akz = 1j * 2 * np.pi * F_K4 * Y_K4
    assert p08_passivitaet(F_K4, akz, EINS_K4, "akzeleranz", S).wert == 1.0
    gemischt = np.vstack([Y_K4, -Y_K4])
    p = p08_passivitaet(F_K4, gemischt, np.ones(gemischt.shape), "mobilitaet", S)
    assert p.status == "warnung" and "Antriebspunkt" in p.grund and p.wert == 0.5
    p_g = p08_passivitaet(
        F_K4, gemischt, np.ones(gemischt.shape), "mobilitaet", S, np.array([True, False])
    )
    assert p_g.wert == 1.0
    leer = p08_passivitaet(F_K4, Y_K4, np.zeros(F_K4.size), "mobilitaet", S)
    assert leer.status == "nicht_pruefbar"
    assert p08_passivitaet(F_K4, Y_K4, None, "mobilitaet", S).wert == 1.0


def test_p01_p02_p04_ungleichungen() -> None:
    ap = np.array([[1.0, 4.0]])
    ok = p01_kreuzspektrum(np.array([[1.0 + 0j, 2.0 + 0j]]), ap, np.ones((1, 2)), S, "a/b")
    assert ok.status == "ok" and ok.wert == pytest.approx(1.0) and ok.bezug == "a/b"
    falsch = p01_kreuzspektrum(np.array([[1.1 + 0j, 0j]]), ap, np.ones((1, 2)), S)
    assert falsch.status == "fehler"
    null = p01_kreuzspektrum(np.array([[1.0 + 0j, 0j]]), np.zeros((1, 2)), np.ones((1, 2)), S)
    assert null.status == "fehler" and null.wert == math.inf
    leer = p01_kreuzspektrum(np.zeros((1, 2), dtype=complex), np.zeros((1, 2)), np.ones((1, 2)), S)
    assert leer.status == "nicht_pruefbar"
    assert p02_cph(np.array([[1.0 + 0j]]), np.array([[1.0 - 5e-6]]), S).status == "ok"
    assert p02_cph(np.array([[1.0 + 0j]]), np.array([[0.99]]), S).status == "fehler"
    assert p04_jensen(np.array([[1.0]]), np.array([[1.0]]), S).status == "ok"
    assert p04_jensen(np.array([[2.0]]), np.array([[1.0]]), S).status == "fehler"


def test_p03_vorzeichen() -> None:
    assert p03_vorzeichen({"AP a": np.array([[0.0, np.nan]])}).status == "ok"
    fehler = p03_vorzeichen({"AP a": np.array([[-1.0]]), "ABS a": np.array([[1.0]])})
    assert fehler.status == "fehler" and "AP a: 1" in fehler.grund


def test_p06_frequenzachse() -> None:
    f = (np.arange(1, 11) * 1.5625).astype(np.float64)
    assert p06_frequenzachse(f, 1.5625, 1, S).status == "ok"
    assert p06_frequenzachse(f, 1.5625, 0, S).status == "fehler"
    gestoert = f.copy()
    gestoert[3] += 1e-5
    assert p06_frequenzachse(gestoert, 1.5625, 1, S).status == "fehler"


def test_p09_referenzstabilitaet() -> None:
    ap_b = np.array([[1.0, 1.0], [1.0, 1.21]])  # √AP: (1, 1) und (1, 1,1)
    g2 = np.ones((2, 2))
    erg = p09_referenzstabilitaet(ap_b, g2, S)
    # Variationskoeffizient (ddof = 0): Linie 0: 0; Linie 1: 0,05/1,05; Median = Mittel
    assert erg.wert == pytest.approx(0.5 * 0.05 / 1.05, rel=1e-12)
    assert erg.status == "ok"
    stark = p09_referenzstabilitaet(np.array([[1.0], [4.0]]), np.ones((2, 1)), S)
    assert stark.status == "warnung"
    assert p09_referenzstabilitaet(ap_b[:1], g2[:1], S).status == "nicht_pruefbar"
    assert p09_referenzstabilitaet(ap_b, np.zeros((2, 2)), S).status == "nicht_pruefbar"
    assert p09_referenzstabilitaet(ap_b, g2, S, np.array([True, False])).status == "nicht_pruefbar"


def test_p10_und_p11() -> None:
    assert p10_punktstatus(Annahmen(), 3).status == "hinweis"
    bestaetigt = Annahmen(status={"M6": "bestätigt am 2026-11-02"})
    assert p10_punktstatus(bestaetigt, 3).status == "ok"
    p10 = p10_punktstatus(Annahmen(gueltig=(True, False, True)), 3)
    assert p10.status == "hinweis" and p10.wert == 1.0
    p11 = p11_annahmen(Annahmen())
    assert p11.status == "hinweis" and p11.wert == 10.0
    for teil in ("M1 konjugieren", "M2 k0", "M8 vorzeichen_kanal", "M10 bandregel", "M7", "M5 n_d"):
        assert teil in p11.grund
    alle = Annahmen(
        status=dict.fromkeys(
            ("M1", "M2", "M4", "M5", "M6", "M7", "M8", "M10", "M11"),
            "bestätigt am 2026-11-02",
        )
    )
    assert p11_annahmen(alle).grund == "Annahmen: keine"


def test_pruefe_eingang_umfasst_p01_bis_p06() -> None:
    daten = ref.messdaten(
        frequenz_hz=np.array([1.5625, 3.125]),
        ap={"Vib Z": np.ones((1, 2)), "Ref1": np.ones((1, 2))},
        betrag={"Vib Z": np.ones((1, 2))},
        cp={("Vib Z", "Ref1"): np.full((1, 2), 0.5 + 0j)},
        cph={("Vib Z", "Ref1"): np.full((1, 2), 0.5 + 0j)},
    )
    ids = [e.id for e in pruefe_eingang(daten, S, Annahmen())]
    assert ids == ["P-01", "P-02", "P-03", "P-04", "P-04", "P-06"]  # P-04 Ref1: kein ABS
