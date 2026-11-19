"""Animation, Korrektur 3 (R-071, Re-Review RR2-AUSW3-2, MINOR-Befunde a bis e).

Je Befund ein Regressionstest, der vor der Korrektur scheitert.
"""

from __future__ import annotations

import re
from dataclasses import replace

import numpy as np
import pytest
from dar_animation_hilfen import KohaerenzCache, messdaten_mit_amplitude
from test_dar_animation_n3 import D_REF, KOORD_2, OMEGA, _daten

from ldv_automation.auswertung.annahmen import ANNAHME, AnnahmenStufe2
from ldv_automation.darstellung.animation3d import (
    KENNZEICHEN_M8,
    KENNZEICHEN_M12,
    AnimationsOptionen,
    kennzeichen_texte,
    pflichttexte,
)
from ldv_automation.darstellung.animation_daten import AnimationsDaten, animation_daten
from ldv_automation.darstellung.stil import THESIS_STIL
from ldv_automation.gui.animation_steuerung import beschreibung_animation

LEER = ("", " ", "  \t\n")


# --- K-a: leerer Aufrufertext unterdrückt kein Pflichtkennzeichen ---------------------------------


@pytest.mark.parametrize("leer", LEER)
def test_k_a_leerer_text_unterdrueckt_m8_und_m12_nicht(leer: str) -> None:
    absolut = _daten(KOORD_2, bezug_modus="absolut")
    opt = AnimationsOptionen(kennzeichen_phase=leer, kennzeichen_koordinaten=leer)
    assert kennzeichen_texte(absolut, opt) == (KENNZEICHEN_M8, None)
    drei_d = _daten(KOORD_2, komponente="3D", bezug_modus="absolut")
    assert kennzeichen_texte(drei_d, opt) == (KENNZEICHEN_M8, KENNZEICHEN_M12)


def test_k_a_leerer_text_bei_bestaetigtem_m8_und_relativ_bleibt_ohne_kennzeichen() -> None:
    opt = AnimationsOptionen(kennzeichen_phase="", kennzeichen_koordinaten=" ")
    relativ = _daten(KOORD_2, bezug_modus="relativ", bezug=0)
    assert kennzeichen_texte(relativ, opt) == (None, None)
    absolut = _daten(KOORD_2, bezug_modus="absolut")
    bestaetigt = tuple(
        replace(a, status="bestätigt am 2027-01-01") if a.nr == "M8" else a
        for a in absolut.annahmen
    )
    assert kennzeichen_texte(replace(absolut, annahmen=bestaetigt), opt) == (None, None)


def test_k_a_gesetzter_text_hat_weiter_vorrang() -> None:
    absolut = _daten(KOORD_2, komponente="3D", bezug_modus="absolut")
    opt = AnimationsOptionen(kennzeichen_phase="eigener Text", kennzeichen_koordinaten="anderer")
    assert kennzeichen_texte(absolut, opt) == ("eigener Text", "anderer")


# --- K-b: Textalternative nennt dieselben Kennzeichen wie das Bild --------------------------------


def test_k_b_textalternative_nennt_m8_bei_absolutem_bezug() -> None:
    a = _daten(KOORD_2, bezug_modus="absolut")
    text = beschreibung_animation(a, 0.0, None, THESIS_STIL)
    assert f"Kennzeichen: {KENNZEICHEN_M8}" in text
    assert "M12" not in text  # Einzelkomponente


def test_k_b_textalternative_nennt_m12_im_3d_modus_und_keine_bei_relativ() -> None:
    drei_d = _daten(KOORD_2, komponente="3D", bezug_modus="absolut")
    text = beschreibung_animation(drei_d, 0.0, None, THESIS_STIL)
    assert f"Kennzeichen: {KENNZEICHEN_M8}" in text
    assert f"Kennzeichen: {KENNZEICHEN_M12}" in text
    relativ = _daten(KOORD_2, bezug_modus="relativ", bezug=0)
    assert "Kennzeichen" not in beschreibung_animation(relativ, 0.0, None, THESIS_STIL)


def test_k_b_textalternative_entspricht_den_texten_des_bildes() -> None:
    a = _daten(KOORD_2, komponente="3D", bezug_modus="absolut")
    m8, m12 = kennzeichen_texte(a, AnimationsOptionen(ueberhoehung=3.0))
    text = beschreibung_animation(a, 0.0, 3.0, THESIS_STIL)
    assert m8 is not None and m12 is not None and m8 in text and m12 in text
    eigen = beschreibung_animation(
        a, 0.0, 3.0, THESIS_STIL, kennzeichen_phase="P-Text", kennzeichen_koordinaten="K-Text"
    )
    assert "Kennzeichen: P-Text" in eigen and "Kennzeichen: K-Text" in eigen
    assert KENNZEICHEN_M8 not in eigen


# --- K-c: M12 folgt dem Status aus AnnahmenStufe2 (Nutzerentscheidung 2026-11-18) -----------------


def _m12_daten(
    status: str | None, drehung: tuple[tuple[float, ...], ...] | None = None
) -> AnimationsDaten:
    """3D-Daten mit M12-Status aus ``AnnahmenStufe2`` (``None``: keine Statusangabe)."""
    k = np.asarray(KOORD_2, dtype=np.float64)
    md = messdaten_mit_amplitude(np.full(2, D_REF * OMEGA, dtype=complex), koordinaten_m=k)
    if status is None:
        annahmen2 = None
    elif drehung is None:
        annahmen2 = AnnahmenStufe2(status={"M12": status})
    else:
        annahmen2 = AnnahmenStufe2(drehung_komponenten=drehung, status={"M12": status})
    return animation_daten(
        md,
        KohaerenzCache(md),
        100.0,
        komponente="3D",
        bezug_modus="relativ",
        bezug=0,
        annahmen2=annahmen2,
    )


def test_k_c_ohne_statusangabe_bleibt_m12_pflicht() -> None:
    a = _m12_daten(None)
    assert all(e.nr != "M12" for e in a.annahmen)  # keine Angabe: nicht in der Liste
    assert kennzeichen_texte(a, AnimationsOptionen()) == (None, KENNZEICHEN_M12)
    assert kennzeichen_texte(_daten(KOORD_2), AnimationsOptionen()) == (None, None)


def test_k_c_m12_entfaellt_genau_bei_bestaetigtem_status() -> None:
    offen = _m12_daten(ANNAHME)
    m12 = [e for e in offen.annahmen if e.nr == "M12"]
    assert len(m12) == 1 and m12[0].ist_annahme
    assert kennzeichen_texte(offen, AnimationsOptionen()) == (None, KENNZEICHEN_M12)
    bestaetigt = _m12_daten("bestätigt am 2026-12-01")
    assert [e.status for e in bestaetigt.annahmen if e.nr == "M12"] == ["bestätigt am 2026-12-01"]
    assert kennzeichen_texte(bestaetigt, AnimationsOptionen()) == (None, None)


def test_k_c_textalternative_und_bild_bleiben_beim_m12_status_konsistent() -> None:
    offen = _m12_daten(ANNAHME)
    bestaetigt = _m12_daten("bestätigt")
    assert f"Kennzeichen: {KENNZEICHEN_M12}" in beschreibung_animation(
        offen, 0.0, None, THESIS_STIL
    )
    assert "M12" not in beschreibung_animation(bestaetigt, 0.0, None, THESIS_STIL)
    # Gesetzter Aufrufertext hat weiter Vorrang, auch bei bestätigtem Status
    eigen = AnimationsOptionen(kennzeichen_koordinaten="eigener Text")
    assert kennzeichen_texte(bestaetigt, eigen) == (None, "eigener Text")


def test_k_c_m12_status_gilt_nur_im_3d_modus_und_andere_annahmen_bleiben() -> None:
    a = _m12_daten("bestätigt")
    assert {e.nr for e in a.annahmen} >= {"M8", "M12"}  # M1 bis M11 unverändert, M12 dazu
    k = np.asarray(KOORD_2, dtype=np.float64)
    md = messdaten_mit_amplitude(np.full(2, D_REF * OMEGA, dtype=complex), koordinaten_m=k)
    ohne = animation_daten(md, KohaerenzCache(md), 100.0, komponente="3D", bezug=0)
    assert [e.nr for e in a.annahmen if e.nr != "M12"] == [e.nr for e in ohne.annahmen]


# --- K-d: Wortlaut des Duplikatehinweises ---------------------------------------------------------


def test_k_d_hinweis_singular() -> None:
    a = _daten([[0.0, 0.0, 0.0], [0.0, 0.0, 0.0], [0.03, 0.0, 0.0]])
    assert a.n_dup == 1
    assert a.hinweis_duplikate == (
        "1 Punkt liegt auf dem Ort eines anderen Punkts (Abstand ≤ 3,000·10⁻⁸ m) "
        "und zählt beim Nachbarabstand nicht mit"
    )


def test_k_d_hinweis_plural_mit_dezimalkomma_und_vier_stellen() -> None:
    a = _daten([[0.0, 0.0, 0.0]] * 3 + [[1.0, 0.0, 0.0]])  # S = 1 m: eps = 1e-6 m
    assert a.n_dup == 2
    text = a.hinweis_duplikate
    assert text is not None
    assert text.startswith("2 Punkte liegen auf dem Ort anderer Punkte")
    assert text.endswith("und zählen beim Nachbarabstand nicht mit")
    assert "." not in text and "e-" not in text
    assert "1,000·10⁻⁶ m" in text


def test_k_d_ohne_duplikate_kein_hinweis() -> None:
    assert _daten(KOORD_2).hinweis_duplikate is None


# --- K-e: keine verschachtelten oder aneinanderstoßenden Klammern ---------------------------------

_KLAMMERN = re.compile(r"\)\s*\(|\(\([^)]*\)\)|\([^()]*\([^()]*\)[^()]*\)")


@pytest.mark.parametrize("groesse", ["auslenkung", "schnelle"])
@pytest.mark.parametrize("quelle", ["cph", "h1"])
@pytest.mark.parametrize("kein_nachbar", [False, True])
@pytest.mark.parametrize("modus", ["absolut", "relativ"])
def test_k_e_pflichtangaben_ohne_doppelte_klammern(
    groesse: str, quelle: str, kein_nachbar: bool, modus: str
) -> None:
    kw = {"bezug": 0} if modus == "relativ" else {}
    a = _daten(KOORD_2, groesse=groesse, quelle=quelle, bezug_modus=modus, **kw)
    texte = pflichttexte(a, 0.3, 2.0, THESIS_STIL, kein_nachbarabstand=kein_nachbar)
    for t in texte:
        # Einheiten wie „(µm/s)/N“ sind erlaubt: sie stehen nie in einer weiteren Klammer
        bereinigt = re.sub(r"\([^()]*/[^()]*\)/N", "EINHEIT", t)
        assert not _KLAMMERN.search(bereinigt), t
    assert t  # mindestens ein Text


def test_k_e_schnelle_ohne_nachbarabstand_hat_eine_klammer() -> None:
    a = _daten([[0.0, 0.0, 0.0]], groesse="schnelle")
    zeile = pflichttexte(a, 0.0, 1.0 / 628.3185307179587, THESIS_STIL, kein_nachbarabstand=True)[0]
    assert zeile.count("(") == 1 and zeile.count(")") == 1
    assert "(Bild = Skalierung · Schnelle; κ = 1/ω, kein Nachbarabstand)" in zeile
    assert beschreibung_animation(a, 0.0, None, THESIS_STIL).count(")(") == 0


# --- K-e: M12 bleibt bei D != I (Drehung wird nicht angewendet), M8/M12 nur bei „bestätigt“ -----

DREHUNG_Z90 = ((0.0, -1.0, 0.0), (1.0, 0.0, 0.0), (0.0, 0.0, 1.0))


def test_k_e_m12_bleibt_bei_bestaetigtem_status_und_gedrehtem_koordinatensystem() -> None:
    a = _m12_daten("bestätigt am 2026-12-01", DREHUNG_Z90)
    assert kennzeichen_texte(a, AnimationsOptionen()) == (None, KENNZEICHEN_M12)
    m12 = [e for e in a.annahmen if e.nr == "M12"]
    assert len(m12) == 1 and m12[0].ist_annahme
    assert "nicht angewendet" in m12[0].wert
    einheit = _m12_daten("bestätigt am 2026-12-01", ((1, 0, 0), (0, 1, 0), (0, 0, 1)))
    assert kennzeichen_texte(einheit, AnimationsOptionen()) == (None, None)


@pytest.mark.parametrize("status", ["offen", "Annahme", "unbestätigt", "nicht bestätigt", "x"])
def test_k_e_m12_status_ohne_bestaetigungsvermerk_laesst_kennzeichen_stehen(status: str) -> None:
    assert kennzeichen_texte(_m12_daten(status), AnimationsOptionen()) == (None, KENNZEICHEN_M12)


@pytest.mark.parametrize("status", ["bestätigt", "Bestätigt am 2026-12-01", "  BESTÄTIGT (Labor)"])
def test_k_e_bestaetigungsvermerk_ignoriert_gross_klein_und_fuehrenden_leerraum(
    status: str,
) -> None:
    assert kennzeichen_texte(_m12_daten(status), AnimationsOptionen()) == (None, None)


@pytest.mark.parametrize("status", ["offen", "unbestätigt", ""])
def test_k_e_m8_nur_bei_ausdruecklicher_bestaetigung_entfallen(status: str) -> None:
    absolut = _daten(KOORD_2, bezug_modus="absolut")
    gesetzt = tuple(replace(a, status=status) if a.nr == "M8" else a for a in absolut.annahmen)
    ergebnis = kennzeichen_texte(replace(absolut, annahmen=gesetzt), AnimationsOptionen())
    assert ergebnis == (KENNZEICHEN_M8, None)
