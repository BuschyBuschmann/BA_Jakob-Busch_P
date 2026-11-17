"""Animation, Korrektur 2 (R-071): FG-04 Nachtrag 3 (doppelte Punkte), Pflichtkennzeichen M8/M12,
Kennzeichnung des Maßstabs „reale Größe“ und Benennung der Skalierung.

Referenzfälle RF-DUP1 bis RF-DUP8 aus ``FG-04_nachtrag-3_doppelte-punkte.md`` Abschnitt 5, Toleranz
wie dort angegeben (halbe Einheit der letzten angegebenen Stelle), Zählwerte und None exakt.
"""

from __future__ import annotations

import math
from dataclasses import replace
from pathlib import Path
from typing import Any

import numpy as np
import pytest
from dar_animation_hilfen import KohaerenzCache, messdaten_mit_amplitude
from matplotlib.figure import Figure

from ldv_automation.auswertung.svd_lesen import lese_svd
from ldv_automation.darstellung import animation_daten as modul
from ldv_automation.darstellung.animation3d import (
    KENNZEICHEN_M8,
    KENNZEICHEN_M12,
    AnimationsOptionen,
    aktualisiere_animation,
    kennzeichen_texte,
    ohne_nachbarabstand,
    pflichttexte,
    zeichne_animation,
)
from ldv_automation.darstellung.animation_daten import (
    AnimationsDaten,
    animation_daten,
    naechste_abstaende_3d,
)
from ldv_automation.darstellung.stil import THESIS_STIL
from ldv_automation.gui.animation_steuerung import beschreibung_animation

OMEGA = 2.0 * math.pi * 100.0
ALPHA = 0.25
D_REF = 1e-6
KOORD_2 = [[0.0, 0.0, 0.0], [0.029, 0.0, 0.0]]
DATEI = Path(__file__).resolve().parents[3] / "Input" / "20261012_ref_Mitte.svd"


def _daten(koord: Any, *, v: Any = None, **kw: Any) -> AnimationsDaten:
    """Daten bei 100 Hz; Voreinstellung: Z-Amplitude so, dass D_ref = 1 µm gilt."""
    k = np.asarray(koord, dtype=np.float64)
    amp = np.full(k.shape[0], D_REF * OMEGA, dtype=complex) if v is None else np.asarray(v)
    md = messdaten_mit_amplitude(amp, koordinaten_m=k)
    return animation_daten(
        md, KohaerenzCache(md), 100.0, komponente=kw.pop("komponente", "Z"), **kw
    )


def _raster(a: float, off: tuple[float, float, float] = (0.0, 0.0, 0.0)) -> np.ndarray:
    return np.array([[i * a + off[0], j * a + off[1], off[2]] for j in range(3) for i in range(3)])


def _stat(x: Any) -> tuple[float | None, float | None, int, float]:
    r = naechste_abstaende_3d(np.asarray(x, dtype=np.float64))
    a = r.abstaende_m
    med = float(np.median(a)) if a.size else None
    mini = float(np.min(a)) if a.size else None
    return med, mini, r.n_dup, r.eps_m


# --- FG-04 Nachtrag 3: RF-DUP1 bis RF-DUP8 --------------------------------------------------------


def test_rf_dup1_raster_mit_duplikat() -> None:
    x = np.vstack([_raster(0.02), [1e-9, 0.0, 0.0]])
    med, mini, n_dup, eps = _stat(x)
    assert eps == pytest.approx(5.657e-8, abs=5e-12)
    assert n_dup == 1
    assert med == pytest.approx(0.02000, abs=5e-6) and mini == pytest.approx(0.02000, abs=5e-6)
    a = _daten(x)
    assert a.n_dup == 1 and a.eps_dup_m == pytest.approx(eps, rel=1e-15)
    assert a.s_auto == pytest.approx(5000.0, abs=0.05)  # bisherige Regel: d_NN,min = 1e-9


def test_rf_dup2_zwei_paare_aus_dem_re_review() -> None:
    x = [[0, 0, 0], [1e-9, 0, 0], [0.03, 0, 0], [0.03, 1e-9, 0]]
    med, mini, n_dup, eps = _stat(x)
    assert eps == pytest.approx(3.0e-8, abs=5e-10)
    assert n_dup == 2
    assert med == pytest.approx(0.030000, abs=5e-7) and mini == pytest.approx(0.030000, abs=5e-7)
    a = _daten(x)
    assert a.s_auto == pytest.approx(7500.0, abs=0.5)  # (7499,9998)
    assert a.n_dup == 2


def test_rf_dup3_mehrfachduplikate_invariant() -> None:
    x = [[0, 0, 0], [0.01, 0, 0], [0.03, 0, 0], [0.06, 0, 0], [0.06, 1e-9, 0], [0.06, 2e-9, 0]]
    med, mini, n_dup, _eps = _stat(x)
    assert n_dup == 2
    assert med == pytest.approx(0.01500, abs=5e-6) and mini == pytest.approx(0.01000, abs=5e-6)
    # Negativtest: ohne Duplikate dieselben Werte (Invarianz); die Zählung je Punkt gäbe 0,025
    ohne = _stat(x[:4])
    assert ohne[0] == pytest.approx(med, abs=5e-6) and ohne[1] == pytest.approx(mini, abs=5e-6)
    assert med != pytest.approx(0.025, abs=5e-6)


def test_rf_dup4_alle_punkte_gleich_nicht_definiert() -> None:
    nah = [[0.1, 0.2, 0.3], [0.1 + 1e-9, 0.2, 0.3], [0.1, 0.2 + 1e-9, 0.3], [0.1, 0.2, 0.3]]
    assert _stat(nah)[:3] == (None, None, 3)
    null = np.zeros((4, 3))
    med, mini, n_dup, eps = _stat(null)
    assert (med, mini, n_dup, eps) == (None, None, 3, 1e-8)
    a = _daten(nah)
    assert a.d_nn_m is None and a.d_nn_min_m is None and a.s_auto is None and a.n_dup == 3
    assert a.hinweis_ueberhoehung(1e9) is None  # kein Nachbarabstand, kein Hinweis


def test_rf_dup5_zwei_punkte() -> None:
    med, mini, n_dup, _eps = _stat([[0, 0, 0], [0.02, 0, 0]])
    assert med == pytest.approx(0.02000, abs=5e-6) and mini == pytest.approx(0.02000, abs=5e-6)
    assert n_dup == 0
    assert _stat([[0, 0, 0], [1e-9, 0, 0]]) == (None, None, 1, 1e-8)


def test_rf_dup6_grenze_der_toleranz() -> None:
    med, mini, n_dup, eps = _stat([[0, 0, 0], [1, 0, 0], [0.5e-6, 0, 0]])
    assert eps == pytest.approx(1e-6, rel=1e-12) and n_dup == 1
    assert med == pytest.approx(1.0000, abs=5e-5) and mini == pytest.approx(1.0000, abs=5e-5)
    med, mini, n_dup, _eps = _stat([[0, 0, 0], [1, 0, 0], [2e-6, 0, 0]])  # echter Nachbar bleibt
    assert n_dup == 0
    assert med == pytest.approx(2.00e-6, abs=5e-9) and mini == pytest.approx(2.00e-6, abs=5e-9)
    abstaende = naechste_abstaende_3d(np.array([[0, 0, 0], [1, 0, 0], [2e-6, 0, 0]])).abstaende_m
    assert abstaende == pytest.approx([2e-6, 0.999998, 2e-6], abs=5e-9)


def test_rf_dup7_fernes_raster_float32_quantum() -> None:
    x = np.vstack([_raster(0.02, (10.0, 0.0, 0.0)), [10.0 + 9.537e-7, 0.0, 0.0]])
    med, mini, n_dup, eps = _stat(x)
    assert eps == pytest.approx(1.004e-5, abs=5e-9)
    assert n_dup == 1
    assert med == pytest.approx(0.02000, abs=5e-6) and mini == pytest.approx(0.02000, abs=5e-6)


@pytest.mark.skipif(not DATEI.is_file(), reason="Messdatei nicht vorhanden")
def test_rf_dup8_realdaten_unveraendert() -> None:
    x = lese_svd(DATEI).punkte.koordinaten_m
    med, mini, n_dup, eps = _stat(x)
    assert x.shape[0] == 135 and n_dup == 0
    assert eps == pytest.approx(6.14e-7, abs=5e-10)
    assert med == pytest.approx(0.02387, abs=5e-6) and mini == pytest.approx(0.02314, abs=5e-6)
    # unverändert gegenüber der bisherigen Regel (Abstand > 0, volle Matrix)
    d = np.linalg.norm(x[:, None] - x[None], axis=2)
    d = np.where(d > 0.0, d, np.inf)
    assert np.array_equal(np.sort(naechste_abstaende_3d(x).abstaende_m), np.sort(d.min(axis=1)))


def test_duplikate_loesen_keinen_ueberlagerungshinweis_aus() -> None:
    x = np.vstack([_raster(0.02), [0.0, 0.0, 0.0]])  # exaktes Duplikat des Ursprungs
    a = _daten(x)
    assert a.n_dup == 1 and a.d_nn_min_m == pytest.approx(0.02, abs=5e-6)
    # s D_ref liegt unter d_NN,min/2 = 10 mm: kein Hinweis, obwohl das Duplikat immer überlagert
    assert a.hinweis_ueberhoehung(0.5 * 0.02 / D_REF * 0.99) is None
    assert a.hinweis_ueberhoehung(0.5 * 0.02 / D_REF) is not None
    text = a.hinweis_duplikate
    assert text is not None and text.startswith("1 Punkte liegen auf dem Ort")
    assert _daten(_raster(0.02)).hinweis_duplikate is None


# --- blockweise Abstandsrechnung ------------------------------------------------------------------


def _vollstaendig_alt(x: np.ndarray) -> np.ndarray:
    """Bisherige Rechnung (volle ``(P, P, 3)``-Matrix, Abstand 0 zählt nicht) als Orakel."""
    diff = x[:, None, :] - x[None, :, :]
    abstand = np.sqrt(np.sum(diff * diff, axis=2))
    abstand = np.where(abstand > 0.0, abstand, np.inf)
    kleinste = np.min(abstand, axis=1)
    return np.asarray(kleinste[np.isfinite(kleinste)], dtype=np.float64)


@pytest.mark.parametrize("block", [1, 7, 50, 20_000, 1_000_000])
def test_blockweise_gleich_voller_matrix(monkeypatch: pytest.MonkeyPatch, block: int) -> None:
    rng = np.random.default_rng(20261117)
    x = rng.uniform(-0.3, 0.3, size=(157, 3))
    erwartet = _vollstaendig_alt(x)
    monkeypatch.setattr(modul, "_BLOCK_ELEMENTE", block)
    r = naechste_abstaende_3d(x)
    assert r.n_dup == 0
    assert np.array_equal(r.abstaende_m, erwartet)  # bitgleich, nicht nur nahe


@pytest.mark.parametrize("block", [1, 5, 1_000_000])
def test_blockweise_duplikate_unabhaengig_von_blockgroesse(
    monkeypatch: pytest.MonkeyPatch, block: int
) -> None:
    rng = np.random.default_rng(7)
    x = rng.uniform(-0.3, 0.3, size=(60, 3))
    x = np.vstack([x, x[[3, 3, 10, 59]]])  # exakte Duplikate, auch von einem Duplikat
    monkeypatch.setattr(modul, "_BLOCK_ELEMENTE", 1_000_000)
    ref = naechste_abstaende_3d(x)
    monkeypatch.setattr(modul, "_BLOCK_ELEMENTE", block)
    r = naechste_abstaende_3d(x)
    assert r.n_dup == ref.n_dup == 4
    assert np.array_equal(r.abstaende_m, ref.abstaende_m) and r.eps_m == ref.eps_m


def test_leere_und_einzelne_punktmenge() -> None:
    assert naechste_abstaende_3d(np.empty((0, 3))).abstaende_m.size == 0
    r = naechste_abstaende_3d(np.array([[1.0, 2.0, 3.0]]))
    assert r.abstaende_m.size == 0 and r.n_dup == 0 and r.eps_m == pytest.approx(3.74e-6, rel=1e-3)


# --- Pflichtkennzeichen M8 und M12 ----------------------------------------------------------------


def _bild(daten: AnimationsDaten, **opt: Any) -> Any:
    return zeichne_animation(
        Figure(figsize=(9.0, 5.6)), daten, AnimationsOptionen(**opt), THESIS_STIL
    )


def _alle(z: Any) -> str:
    return " ".join(" ".join(z.alle_texte()).split())


@pytest.mark.parametrize(
    ("kw", "m8", "m12"),
    [
        ({"komponente": "Z"}, False, False),
        ({"komponente": "Z", "bezug_modus": "absolut"}, True, False),
        ({"komponente": "3D"}, False, True),
        ({"komponente": "3D", "bezug_modus": "absolut"}, True, True),
    ],
)
def test_m8_m12_werden_von_der_zeichenfunktion_gesetzt(
    kw: dict[str, Any], m8: bool, m12: bool
) -> None:
    daten = _daten(KOORD_2, v=[1e-3, 0.5e-3], **kw)
    assert kennzeichen_texte(daten, AnimationsOptionen()) == (
        KENNZEICHEN_M8 if m8 else None,
        KENNZEICHEN_M12 if m12 else None,
    )
    text = _alle(_bild(daten))  # Standardoptionen, kein Kennzeichen übergeben
    assert (KENNZEICHEN_M8 in text) is m8
    assert (KENNZEICHEN_M12 in text) is m12


def test_m8_m12_nach_aktualisieren_und_text_des_aufrufers_hat_vorrang() -> None:
    daten = _daten(KOORD_2, v=[1e-3, 0.5e-3], komponente="3D", bezug_modus="absolut")
    z = _bild(daten)
    vorher = _alle(z)
    aktualisiere_animation(z, daten, AnimationsOptionen(theta_rad=1.0), THESIS_STIL)
    assert KENNZEICHEN_M8 in _alle(z) and KENNZEICHEN_M12 in _alle(z)
    assert KENNZEICHEN_M8 in vorher
    eigen = _alle(_bild(daten, kennzeichen_phase="unbestätigt (eigen)"))
    assert "unbestätigt (eigen)" in eigen and KENNZEICHEN_M8 not in eigen


def test_m8_entfaellt_wenn_bestaetigt() -> None:
    daten = _daten(KOORD_2, v=[1e-3, 0.5e-3], bezug_modus="absolut")
    bestaetigt = tuple(
        replace(a, status="bestätigt am 2027-01-01") if a.nr == "M8" else a for a in daten.annahmen
    )
    assert kennzeichen_texte(replace(daten, annahmen=bestaetigt), AnimationsOptionen()) == (
        None,
        None,
    )


# --- Maßstab ohne Nachbarabstand ---------------------------------------------------------------


def test_ein_punkt_massstab_wird_im_bild_gekennzeichnet() -> None:
    a = _daten([[0.0, 0.0, 0.0]])
    assert a.s_auto is None and ohne_nachbarabstand(a, None) and not ohne_nachbarabstand(a, 5.0)
    assert pflichttexte(a, 0.0, 1.0, THESIS_STIL, kein_nachbarabstand=True)[0] == (
        "Überhöhung \N{MULTIPLICATION SIGN}1,000 (reale Größe, kein Nachbarabstand)"
    )
    assert "Überhöhung \N{MULTIPLICATION SIGN}1,000 (reale Größe, kein Nachbarabstand)" in _alle(
        _bild(a)
    )
    # Eingabe des Nutzers: keine Kennzeichnung
    assert "kein Nachbarabstand" not in _alle(_bild(a, ueberhoehung=50.0))
    assert "Überhöhung \N{MULTIPLICATION SIGN}50" in _alle(_bild(a, ueberhoehung=50.0))
    assert "kein Nachbarabstand" in beschreibung_animation(a, 0.0, None, THESIS_STIL)
    assert "kein Nachbarabstand" not in beschreibung_animation(a, 0.0, 5.0, THESIS_STIL)
    # mit Nachbarabstand nie
    zwei = _daten(KOORD_2, v=[1e-3, 0.5e-3])
    assert not ohne_nachbarabstand(zwei, None)
    assert "kein Nachbarabstand" not in _alle(_bild(zwei))


def test_ein_punkt_schnelle_kappa_gleich_eins_durch_omega() -> None:
    a = _daten([[0.0, 0.0, 0.0]], groesse="schnelle")
    kappa = 1.0 / OMEGA  # 1,592 ms
    text = pflichttexte(a, 0.0, kappa, THESIS_STIL, kein_nachbarabstand=True)[0]
    assert text == (
        "Skalierung 0,001592 s (κ = 1/ω, kein Nachbarabstand) (Bild = Skalierung · Schnelle) · "
        "Amplitude wie Auslenkung mit Überhöhung \N{MULTIPLICATION SIGN}1,000"
    )
    assert "κ = 1/ω, kein Nachbarabstand" in _alle(_bild(a))


def test_duplikate_ergeben_gekennzeichneten_massstab() -> None:
    a = _daten([[0.1, 0.2, 0.3], [0.1, 0.2, 0.3]])  # zwei gleiche Punkte
    assert a.s_auto is None and a.n_dup == 1
    assert "(reale Größe, kein Nachbarabstand)" in _alle(_bild(a))


# --- Benennung der Skalierung ---------------------------------------------------------------------


def test_hilfsobjekte_skalierung_und_ueberhoehung() -> None:
    schnelle = _daten(KOORD_2, v=[1e-3, 0.5e-3], groesse="schnelle")
    z = _bild(schnelle)
    kappa = z.hilfsobjekte["skalierung"]
    assert kappa == schnelle.s_auto  # κ in s
    assert z.hilfsobjekte["ueberhoehung"] == pytest.approx(kappa * schnelle.omega_rad_s, rel=1e-15)
    ausl = _daten(KOORD_2, v=[1e-3, 0.5e-3])
    z2 = _bild(ausl)
    assert z2.hilfsobjekte["skalierung"] == z2.hilfsobjekte["ueberhoehung"] == ausl.s_auto
