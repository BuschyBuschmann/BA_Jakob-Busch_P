"""Qt-freie Anzeigelogik der Animation in Ansicht 4 (R-071, P-AUSW3 AN7; Standardlauf).

Regler und Eingaben (Skalierung, Farbbereich), Kopf mit den Kennzeichen M8 und M12 (UI-28),
Textalternative (UI-26) und die Texte der Meldungen. Daten: ``gui_ausw_hilfen.synth_geladen``
(4 Punkte, Linie bei 16 Hz).

Toleranzen: Reglerabbildungen sind ganzzahlig (exakt); Umrechnungen Anzeigeeinheit ↔ SI haben
``rtol = 1e-12`` (nur Gleitkomma-Rundung der Division/Multiplikation mit 10⁶).
"""

from __future__ import annotations

import math
from dataclasses import replace

import numpy as np
import pytest
from gui_ausw_hilfen import synth_geladen

from ldv_automation.auswertung.annahmen import Annahmen, AnnahmenStufe2
from ldv_automation.darstellung.achsen import (
    TEXT_KEINE_ZAHL,
    TEXT_REIHENFOLGE,
    AchsenFehler,
    Bereich,
)
from ldv_automation.darstellung.animation3d import (
    KENNZEICHEN_M8,
    KENNZEICHEN_M12,
    AnimationsOptionen,
    Blick,
)
from ldv_automation.darstellung.animation_daten import (
    TEXT_KEINE_PHASE as DAR_TEXT_KEINE_PHASE,
)
from ldv_automation.darstellung.animation_daten import (
    UNGUELTIG,
    UNSICHER,
    AnimationsDaten,
    animation_daten,
)
from ldv_automation.darstellung.auswahl import PaarCache
from ldv_automation.gui import animation_anzeige as an
from ldv_automation.gui.animation_steuerung import (
    ANIMATIONS_TASTEN,
    Aktion,
    tabelle_auslenkungen,
)
from ldv_automation.gui.anzeige_aktionen import (
    AKTIONS_TASTEN,
    TASTEN_KONTEXT,
    tasten_konflikte,
)
from ldv_automation.gui.anzeige_auswerten import unbestaetigte_annahmen
from ldv_automation.gui.plotstil import baue_plotstil

STIL = baue_plotstil()
RTOL = 1e-12


def _daten(komponente: str = "3D", **kw: object) -> AnimationsDaten:
    md = synth_geladen().messdaten
    annahmen2 = kw.pop("annahmen2", None)
    return animation_daten(
        md,
        PaarCache(md),
        16.0,
        komponente=komponente,
        annahmen2=annahmen2,  # type: ignore[arg-type]
        **kw,  # type: ignore[arg-type]
    )


def _bestaetigt(nr: str, status: str = "bestätigt am 2026-12-01") -> Annahmen:
    return Annahmen(status={nr: status})


# --- Regler -----------------------------------------------------------------------------------


def test_phasenregler_in_zehntelgrad_und_begrenzt() -> None:
    assert an.theta_grad_aus_regler(900) == 90.0
    assert an.regler_aus_theta_rad(math.pi / 2) == 900
    assert an.regler_aus_theta_rad(0.0) == 0
    # knapp unter 360° rundet auf 3600 und wird auf 359,9° begrenzt (kein Winkel 360° im Regler)
    assert an.regler_aus_theta_rad(math.radians(359.96)) == an.PHASE_REGLER_MAX == 3599
    assert an.regler_aus_theta_rad(-math.pi / 2) == 2700  # 270°


def test_tempo_regler_logarithmisch_mit_grenzen_und_umkehrung() -> None:
    assert an.tempo_aus_regler(an.TEMPO_REGLER_MIN) == pytest.approx(an.TEMPO_MIN_HZ, rel=1e-2)
    assert an.tempo_aus_regler(an.TEMPO_REGLER_MAX) == pytest.approx(an.TEMPO_MAX_HZ, rel=1e-2)
    assert an.tempo_aus_regler(-1000) == an.tempo_aus_regler(an.TEMPO_REGLER_MIN)  # begrenzt
    assert an.regler_aus_tempo(0.25) == -60  # Voreinstellung 0,25 Perioden/s
    assert an.regler_aus_tempo(0.0) == an.TEMPO_REGLER_MIN  # ungültig: kleinster Wert
    assert an.regler_aus_tempo(1e9) == an.TEMPO_REGLER_MAX
    assert an.tempo_text(0.25) == "0,25 Perioden/s"
    assert an.tempo_text(2.0) == "2,0 Perioden/s"


def test_ueberhoehungsregler_ist_faktor_der_automatischen_skalierung() -> None:
    assert an.faktor_aus_regler(0) == 1.0
    assert an.faktor_aus_regler(an.FAKTOR_REGLER_MIN) == pytest.approx(an.FAKTOR_MIN, rel=1e-12)
    assert an.faktor_aus_regler(an.FAKTOR_REGLER_MAX) == pytest.approx(an.FAKTOR_MAX, rel=1e-2)
    assert an.regler_aus_faktor(1.0) == 0
    assert an.regler_aus_faktor(10.0) == 100
    assert an.regler_aus_faktor(1e9) == an.FAKTOR_REGLER_MAX  # begrenzt
    assert an.regler_aus_faktor(1e-9) == an.FAKTOR_REGLER_MIN
    assert an.regler_aus_faktor(float("nan")) == 0


def test_skalierung_aus_regler_bei_faktor_eins_oder_ohne_autowert_automatisch() -> None:
    assert an.skalierung_aus_regler(0, 4555.0) is None  # Mitte = Auto
    assert an.skalierung_aus_regler(100, 4555.0) == pytest.approx(45550.0, rel=RTOL)
    assert an.skalierung_aus_regler(100, None) is None  # kein Nachbarabstand: keine Bezugsgröße
    assert an.regler_aus_skalierung(None, 4555.0) == 0
    assert an.regler_aus_skalierung(45550.0, 4555.0) == 100
    assert an.regler_aus_skalierung(45550.0, None) == 0
    assert an.regler_aus_skalierung(45550.0, 0.0) == 0


# --- Skalierung (Eingabefeld) -----------------------------------------------------------------


def test_skalierung_eingabe_leer_ist_auto_komma_und_exponent_gelten() -> None:
    assert an.lese_skalierung("") is None
    assert an.lese_skalierung("  ") is None
    assert an.lese_skalierung("4555") == 4555.0
    assert an.lese_skalierung("1,5e3") == 1500.0
    assert an.lese_skalierung("2,5·10⁻³") == pytest.approx(2.5e-3, rel=RTOL)


@pytest.mark.parametrize("text", ["0", "-3", "\N{MINUS SIGN}0,5"])
def test_skalierung_null_oder_negativ_ist_ein_fehler(text: str) -> None:
    with pytest.raises(AchsenFehler) as fehler:
        an.lese_skalierung(text)
    assert str(fehler.value) == an.TEXT_SKALIERUNG_POSITIV


def test_skalierung_keine_zahl_ist_ein_fehler() -> None:
    with pytest.raises(AchsenFehler) as fehler:
        an.lese_skalierung("abc")
    assert str(fehler.value) == TEXT_KEINE_ZAHL


# --- Farbbereich ------------------------------------------------------------------------------


def test_farbanzeige_nennt_einheit_und_faktor_der_automatischen_grenze() -> None:
    daten = _daten()
    opt = AnimationsOptionen()
    faktor, einheit = an.farb_anzeige(daten, opt)
    assert einheit in {"m", "mm", "µm", "nm", "pm"} and faktor >= 1.0
    # Einheit unabhängig von einer Eingabe (eine getippte Zahl behält ihre Einheit)
    gross = replace(opt, farbbereich=Bereich(-1.0, 1.0))
    assert an.farb_anzeige(daten, gross) == (faktor, einheit)


def test_farbfeld_wird_in_si_umgerechnet_und_rundreise_stimmt() -> None:
    faktor = 1.0e6  # µm
    bereich = an.lese_farbfeld("-1,5", "von", Bereich(), faktor)
    assert bereich.von == pytest.approx(-1.5e-6, rel=RTOL) and bereich.bis is None
    beide = an.lese_farbfeld("2", "bis", bereich, faktor)
    assert beide.bis == pytest.approx(2.0e-6, rel=RTOL)
    assert an.farb_feldtexte(beide, faktor) == ("\N{MINUS SIGN}1,5", "2")  # typografisches Minus
    assert an.farb_feldtexte(Bereich(), faktor) == ("", "")  # Auto = leer
    assert an.lese_farbfeld("", "von", beide, faktor) == Bereich(None, beide.bis)  # leer = Auto


def test_farbfeld_von_nicht_kleiner_als_bis_gibt_die_meldung_wie_ui_5() -> None:
    gesetzt = Bereich(-1.0e-6, 1.0e-6)
    for text, seite in (("2", "von"), ("-2", "bis"), ("1", "von")):
        with pytest.raises(AchsenFehler) as fehler:
            an.lese_farbfeld(text, seite, gesetzt, 1.0e6)
        assert str(fehler.value) == TEXT_REIHENFOLGE, (text, seite)


def test_farbfeld_keine_zahl_ist_ein_fehler() -> None:
    with pytest.raises(AchsenFehler):
        an.lese_farbfeld("x", "von", Bereich(), 1.0e6)


def test_gemischter_bereich_wird_gegen_die_automatische_gegenseite_geprueft() -> None:
    daten = _daten()
    opt = AnimationsOptionen()
    an.pruefe_farbbereich(daten, opt, Bereich(-1.0, 1.0))  # beide gesetzt: gültig
    an.pruefe_farbbereich(daten, opt, Bereich())  # Auto
    # „von“ jenseits der automatischen Obergrenze: die Zeichenfunktion lehnt das ab
    with pytest.raises(AchsenFehler) as fehler:
        an.pruefe_farbbereich(daten, opt, Bereich(1.0e3, None))
    assert str(fehler.value) == TEXT_REIHENFOLGE


# --- Kopf: Kennzeichen M8 und M12 (UI-28) -----------------------------------------------------


def test_kopf_nennt_datei_linie_groesse_bezug_und_m12_bei_3d() -> None:
    daten = _daten("3D", bezug_modus="relativ")
    kopf = an.animations_kopf_text("probe.svd", daten, AnimationsOptionen(), STIL)
    teile = kopf.split(" · ")
    assert teile[0] == "probe.svd" and teile[1] == "Linie 16,000 Hz"
    assert teile[2] == "Animation Auslenkung 3D (CPH)"
    assert teile[3].startswith("Phase relativ zu Punkt ")
    assert f"{STIL.warn_symbol} {KENNZEICHEN_M12}" in kopf  # M12 offen: dauerhaft im Kopf
    assert "M8" not in kopf  # relativ: kein M8


def test_kopf_m8_nur_bei_absolutem_bezug_und_verschwindet_bei_bestaetigtem_status() -> None:
    absolut = _daten("Z", bezug_modus="absolut")
    kopf = an.animations_kopf_text("probe.svd", absolut, AnimationsOptionen(), STIL)
    assert f"{STIL.warn_symbol} {KENNZEICHEN_M8}" in kopf
    assert "Phase gegen Ref1" in kopf and "M12" not in kopf  # Einzelkomponente: kein M12
    md = synth_geladen().messdaten
    bestaetigt = animation_daten(
        md, PaarCache(md, annahmen=_bestaetigt("M8")), 16.0, komponente="Z", bezug_modus="absolut"
    )
    assert "M8" not in an.animations_kopf_text("probe.svd", bestaetigt, AnimationsOptionen(), STIL)


def test_kopf_m12_verschwindet_genau_bei_bestaetigtem_status_aus_stufe2() -> None:
    offen = _daten("3D", annahmen2=AnnahmenStufe2())
    bestaetigt = _daten("3D", annahmen2=AnnahmenStufe2(status={"M12": "bestätigt"}))
    opt = AnimationsOptionen()
    assert "M12" in an.animations_kopf_text("d", offen, opt, STIL)
    assert "M12" not in an.animations_kopf_text("d", bestaetigt, opt, STIL)
    assert "M12" in an.animations_kopf_text("d", _daten("3D"), opt, STIL)  # ohne Angabe: Pflicht


def test_kopf_schnelle_und_h1_stehen_im_kopf() -> None:
    kopf = an.animations_kopf_text("d", _daten("Z", groesse="schnelle"), AnimationsOptionen(), STIL)
    assert "Animation Schnelle Z (CPH)" in kopf


# --- Textalternative (UI-26) ------------------------------------------------------------------


def test_textalternative_nennt_datei_winkel_ueberhoehung_blick_und_kennzeichen() -> None:
    daten = _daten("3D", bezug_modus="relativ")
    opt = AnimationsOptionen(
        theta_rad=math.pi / 2, ueberhoehung=3.0, blick=Blick(azim_grad=-45.0, elev_grad=35.3)
    )
    text = an.animations_beschreibung("probe.svd", daten, opt, STIL)
    assert text.startswith("Datei probe.svd. Animation der Betriebsschwingform.")
    assert "Überhöhung \N{MULTIPLICATION SIGN}3" in text  # Faktor im Text (UI-26)
    assert "θ = 90,0°" in text and "f = 16,000 Hz" in text
    assert "Blickrichtung: Azimut \N{MINUS SIGN}45,0°, Elevation 35,3°, Zoom 1,00." in text
    assert f"Kennzeichen: {KENNZEICHEN_M12}" in text
    assert "Standbild" in text
    assert "Wiedergabe läuft" in an.animations_beschreibung("p", daten, opt, STIL, laeuft=True)


# --- Texte ------------------------------------------------------------------------------------


def test_absolut_text_mit_kennzeichen_m8_solange_offen() -> None:
    offen = Annahmen().eintraege()
    assert (
        an.absolut_text("Ref1", offen) == f"Absolut gegen Ref1 ({STIL.warn_symbol} unbestätigt, M8)"
    )
    assert an.absolut_text("Ref1", _bestaetigt("M8").eintraege()) == "Absolut gegen Ref1"
    assert unbestaetigte_annahmen("phase", offen)  # dieselbe Quelle wie das Standbild


@pytest.mark.parametrize("status", ["offen", "unbestätigt", "nicht bestätigt"])
def test_absolut_text_bleibt_bei_status_ohne_bestaetigungsvermerk_gekennzeichnet(
    status: str,
) -> None:
    """Fail-closed wie das Bild (K-AUSW3-7 Befund 4): nur „bestätigt …“ nimmt das Kennzeichen."""
    assert an.absolut_text("Ref1", _bestaetigt("M8", status).eintraege()) == (
        f"Absolut gegen Ref1 ({STIL.warn_symbol} unbestätigt, M8)"
    )
    assert an.absolut_text("Ref1", _bestaetigt("M8", "Bestätigt am 2027-01-01").eintraege()) == (
        "Absolut gegen Ref1"
    )


def test_bezug_automatisch_text_nennt_den_gewaehlten_punkt() -> None:
    daten = _daten("3D", bezug_modus="relativ")
    assert daten.bezug_index is not None
    assert an.bezug_automatisch_text(daten) == (
        f"Automatisch (Punkt {int(daten.label[daten.bezug_index])})"
    )
    assert an.bezug_automatisch_text(None).startswith("Automatisch (")


def test_hinweise_text_fuegt_duplikatehinweis_an() -> None:
    daten = _daten("3D")
    assert an.hinweise_text(daten, ["Punkte können sich überlagern"]) == (
        "Punkte können sich überlagern"
    )
    mit_dup = replace(daten, n_dup=2, eps_dup_m=1e-8)
    text = an.hinweise_text(mit_dup, ["A"])
    assert text.splitlines()[0] == "A" and "2 Punkte liegen auf dem Ort" in text
    assert mit_dup.hinweis_duplikate is not None and mit_dup.hinweis_duplikate in text


def test_texte_der_meldungen_und_der_sperre() -> None:
    assert an.TEXT_KEINE_PHASE == "Animation braucht eine Phase: keine Referenz."
    assert an.TEXT_KEINE_PHASE == DAR_TEXT_KEINE_PHASE  # eine Quelle für Oberfläche und Daten
    assert an.TEXT_LANGSAM == "Wiedergabe langsamer als eingestellt"
    assert an.regler_namen("abspielen") == ("Abspielen", "Animation abspielen")
    assert an.regler_namen("pause")[0] == "Pause"
    assert an.FARBE_SENKRECHT == {"xy": "Z", "xz": "Y", "yz": "X"}
    assert an.BILDRATEN == (5, 10, 20)


# --- Tasten in AKTIONS_TASTEN (Plan 5.2, U-A4) ---------------------------------------


def test_animations_tasten_stehen_in_aktions_tasten_und_gleichen_der_steuerung() -> None:
    erwartet = {f"animation_{a.value}": t for a, t in ANIMATIONS_TASTEN.items()}
    vorhanden = {k: v for k, v in AKTIONS_TASTEN.items() if k.startswith("animation_")}
    assert vorhanden == erwartet and len(erwartet) == len(Aktion)  # alle Aktionen, eine Quelle


def test_tastenbelegung_ist_konfliktfrei() -> None:
    assert tasten_konflikte() == ()


def test_pos1_gilt_in_plot_und_animation_in_getrennten_bereichen() -> None:
    assert AKTIONS_TASTEN["zoom"][0] == AKTIONS_TASTEN["animation_ansicht_zurueck"][0] == "Home"
    assert TASTEN_KONTEXT["zoom"] == "plot" and TASTEN_KONTEXT["animation_ansicht_zurueck"] == (
        "animation"
    )
    assert ("animation_ansicht_zurueck", "zoom") not in tasten_konflikte()


def test_kein_fensterweiter_kuerzel_gleicht_einer_animationstaste() -> None:
    animation = {v[0] for k, v in AKTIONS_TASTEN.items() if TASTEN_KONTEXT[k] == "animation"}
    fenster = {v[0] for k, v in AKTIONS_TASTEN.items() if TASTEN_KONTEXT[k] == "fenster"}
    assert not animation & fenster


def test_konflikte_werden_erkannt(monkeypatch: pytest.MonkeyPatch) -> None:
    # gleicher Bereich: zwei Animationstasten mit derselben Tastenfolge
    monkeypatch.setitem(AKTIONS_TASTEN, "animation_x", ("Space", "Leertaste"))
    monkeypatch.setitem(TASTEN_KONTEXT, "animation_x", "animation")
    assert ("animation_abspielen", "animation_x") in tasten_konflikte()
    # fensterweit gegen Animation: das Fensterkürzel nähme der Animation die Taste
    monkeypatch.setitem(AKTIONS_TASTEN, "fenster_y", ("Left", "←"))
    monkeypatch.setitem(TASTEN_KONTEXT, "fenster_y", "fenster")
    assert ("animation_phase_zurueck", "fenster_y") in tasten_konflikte()


# --- Standbild speichern: Stempelzeilen und offene Annahmen (AN8, UI-31) --------------------------


def test_stempel_zusatz_nennt_winkel_frequenz_ueberhoehung_und_blick() -> None:
    daten = _daten()
    opt = AnimationsOptionen(
        theta_rad=math.pi / 2.0, ueberhoehung=12.0, blick=Blick(azim_grad=-60.0, elev_grad=30.0)
    )
    zeilen = an.animations_stempel_zusatz(daten, opt, STIL)
    assert (
        zeilen[0]
        == "Animation · θ = 90,0° · f = 16,000 Hz · Überhöhung \N{MULTIPLICATION SIGN}12,00"
    )
    assert zeilen[1] == "Blickrichtung: Azimut \N{MINUS SIGN}60,0°, Elevation 30,0°, Zoom 1,00"


def test_stempel_zusatz_schnelle_nennt_skalierung_in_sekunden() -> None:
    daten = _daten(groesse="schnelle")
    zeilen = an.animations_stempel_zusatz(daten, AnimationsOptionen(ueberhoehung=0.001), STIL)
    assert " · Skalierung 0,001000 s (entspricht Überhöhung " in zeilen[0]
    assert "Überhöhung Skalierung" not in zeilen[0]


def test_unbestaetigt_nennt_m12_bei_3d_und_m8_nur_bei_absolutem_bezug() -> None:
    opt = AnimationsOptionen()
    assert an.animations_unbestaetigt(_daten(), opt) == ("M12",)
    assert an.animations_unbestaetigt(_daten(bezug_modus="absolut"), opt) == ("M8", "M12")
    assert an.animations_unbestaetigt(_daten("Z"), opt) == ()  # relativ, eine Komponente


def test_unbestaetigt_folgt_dem_bestaetigungsvermerk_fail_closed() -> None:
    opt = AnimationsOptionen()
    daten = _daten(
        bezug_modus="absolut",
        annahmen2=AnnahmenStufe2(status={"M12": "bestätigt am 2026-12-01"}),
    )
    assert an.animations_unbestaetigt(daten, opt) == ("M8",)
    # Status ohne Bestätigungsvermerk („Annahme“) lässt das Kennzeichen stehen
    offen = _daten(annahmen2=AnnahmenStufe2(status={"M12": "Annahme, bestätigt nicht"}))
    assert an.animations_unbestaetigt(offen, opt) == ("M12",)


@pytest.mark.parametrize(
    ("theta", "zusatz"),
    [
        (0.0, "_animation_theta000"),
        (math.pi / 2.0, "_animation_theta090"),
        (math.radians(359.6), "_animation_theta000"),  # rundet auf 360° = 0°
        (-math.pi / 2.0, "_animation_theta270"),
    ],
)
def test_namenszusatz_des_dateivorschlags(theta: float, zusatz: str) -> None:
    assert an.bild_vorschlag_zusatz(theta) == zusatz


# --- „Werte als Tabelle“ (AN9, UI-26) ------------------------------------------------------------


def _zahl(text: str) -> float:
    return float(text.replace(",", "."))


def test_tabelle_zeigt_reale_auslenkung_je_punkt_gegen_unabhaengige_rechnung() -> None:
    daten = _daten()
    theta = math.pi / 3.0
    t = tabelle_auslenkungen(daten, theta, 2.5, STIL)
    assert t.spalten[:5] == ("Punkt", "Status", "x [mm]", "y [mm]", "z [mm]")
    assert t.spalten[5:] == (
        "Auslenkung x [mm]",
        "Auslenkung y [mm]",
        "Auslenkung z [mm]",
        "Betrag [mm]",
    )
    assert len(t.zeilen) == daten.anzahl_punkte == 4
    # Orakel: Re{d e^{iθ}} aus der animierten Amplitude, Einheit mm (Faktor 1e3, 4 Stellen)
    soll = np.real(daten.amplitude_anim * np.exp(1j * theta)) * 1e3
    for p, zeile in enumerate(t.zeilen):
        assert zeile[0] == str(int(daten.label[p])) and zeile[1] == "bewegt"
        ist = [_zahl(x) for x in zeile[5:8]]
        assert ist == pytest.approx(soll[p], rel=1e-3)  # 4 signifikante Stellen
        assert _zahl(zeile[8]) == pytest.approx(float(np.linalg.norm(soll[p])), rel=1e-3)
        ort = [_zahl(x) for x in zeile[2:5]]
        assert ort == pytest.approx(daten.koordinaten_m[p] * 1e3, rel=1e-3, abs=1e-9)
    assert "θ = 60,0°" in t.titel and "f = 16,000 Hz" in t.titel
    assert "ohne Überhöhung (im Bild: Überhöhung \N{MULTIPLICATION SIGN}2,500)" in t.titel


def test_tabelle_einzelkomponente_zeigt_nicht_gewaehlte_achsen_als_strich() -> None:
    t = tabelle_auslenkungen(_daten("Z"), 0.0, 1.0, STIL)
    for zeile in t.zeilen:
        assert zeile[5:7] == ("–", "–") and zeile[7] != "–"
        assert _zahl(zeile[8]) == pytest.approx(abs(_zahl(zeile[7])), rel=1e-12)


def test_tabelle_gekennzeichnete_punkte_stehen_ohne_werte_mit_status_in_worten() -> None:
    daten = _daten()
    status = daten.status.copy()
    status[1], status[2] = UNSICHER, UNGUELTIG
    bewegt = daten.bewegt.copy()
    bewegt[1] = bewegt[2] = False
    daten = replace(daten, status=status, bewegt=bewegt)
    t = tabelle_auslenkungen(daten, 1.0, 1.0, STIL)
    assert t.zeilen[1][1] == "steht, unsicher (γ² unter der Schwelle)"
    assert t.zeilen[2][1] == "steht, ungültig (M6)"
    assert all(x == "–" for x in t.zeilen[1][5:]) and all(x == "–" for x in t.zeilen[2][5:])
    assert t.zeilen[0][1] == "bewegt" and t.zeilen[0][5] != "–"


def test_tabelle_3d_unvollstaendig_und_ruhende_punkte() -> None:
    daten = _daten()
    status = daten.status.copy()
    status[0] = UNSICHER
    grund = daten.grund_3d_unvollstaendig.copy()
    grund[0] = True
    bewegt = daten.bewegt.copy()
    bewegt[0] = False
    daten = replace(daten, status=status, grund_3d_unvollstaendig=grund, bewegt=bewegt)
    assert tabelle_auslenkungen(daten, 0.0, 1.0, STIL).zeilen[0][1] == "steht, 3D unvollständig"


def test_tabelle_schnelle_nennt_skalierung_und_einheit() -> None:
    t = tabelle_auslenkungen(_daten(groesse="schnelle"), 0.0, 0.001, STIL)
    assert t.titel.startswith("Schnelle je Messpunkt bei θ = 0,0°")
    assert "im Bild: 0,001000 s (entspricht Überhöhung" in t.titel
    assert t.spalten[5].startswith("Schnelle x [") and "/s]" in t.spalten[5]


def test_tabelle_zahlen_ausserhalb_von_1e_minus_3_bis_1e6_in_potenzschreibweise() -> None:
    """Review MINOR 1: Rundungsreste wie 6e-17 stehen als „m·10ⁿ“ (KONVENTIONEN)."""
    daten = _daten()
    amplitude = daten.amplitude_anim.copy()
    amplitude[0] = [1e-9 + 0j, 6e-17 + 0j, 2.5e-3 + 0j]  # reale Auslenkung bei θ = 0 in m
    t = tabelle_auslenkungen(replace(daten, amplitude_anim=amplitude), 0.0, 1.0, STIL)
    assert t.spalten[5].endswith("[mm]")  # Anzeigeeinheit der Beispieldaten: Faktor 10³
    assert t.zeilen[0][5:8] == (
        "1,000·10\N{SUPERSCRIPT MINUS}\N{SUPERSCRIPT SIX}",  # 1e-9 m = 1e-6 mm
        "6,000·10\N{SUPERSCRIPT MINUS}\N{SUPERSCRIPT ONE}\N{SUPERSCRIPT FOUR}",  # 6e-17 m
        "2,500",
    )


def test_tempo_text_kompakt_ohne_wort_perioden() -> None:
    assert an.tempo_text(0.25, kompakt=True) == "0,25/s"
    assert an.tempo_text(2.0, kompakt=True) == "2,0/s"
