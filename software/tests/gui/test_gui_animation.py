"""Animation in Ansicht 4 (R-071, Plan P-AUSW3 AN7): UI-22, UI-24 bis UI-30, UI-32, UI-34 bis UI-37.

Geprüft werden Zustände und die Struktur von Oberfläche und Figure (Sichtbarkeit, Texte, Positionen
der Scatter, ``ax.azim/elev``), keine Pixel. Die Uhr der Wiedergabe wird von Hand geführt
(``Uhr``), die Takte kommen von Hand über ``takt()``; echte Zeit geht nicht ein. Daten:
``gui_ausw_hilfen.synth_geladen`` (4 Punkte, Linie bei 16 Hz) über einen ``DirektAusfuehrer``.
"""

from __future__ import annotations

import itertools
import math
from dataclasses import replace
from pathlib import Path
from typing import Any

import numpy as np
import pytest
from gui_ausw_hilfen import PFAD, Bauer, synth_geladen
from PySide6.QtCore import QPoint, Qt
from PySide6.QtGui import QKeySequence
from PySide6.QtTest import QTest
from PySide6.QtWidgets import QAbstractButton, QApplication, QLineEdit, QSlider, QWidget
from pytestqt.qtbot import QtBot
from test_gui_ansicht_5 import aufbau
from test_gui_auswerten import lade
from test_gui_auswerten_ansichten import geladen_mit
from test_gui_auswerten_t4 import Meldungen

from ldv_automation.auswertung.annahmen import Annahmen, AnnahmenStufe2
from ldv_automation.auswertung.daten import Punkte
from ldv_automation.auswertung.laden import Geladen
from ldv_automation.darstellung.achsen import TEXT_REIHENFOLGE, Bereich
from ldv_automation.darstellung.animation3d import (
    BLICK_VORGABEN,
    KENNZEICHEN_M8,
    KENNZEICHEN_M12,
    AnimationsOptionen,
    effektive_ueberhoehung,
    scatter_positionen,
    skaliere_einheit,
)
from ldv_automation.darstellung.animation_daten import AnimationsDaten
from ldv_automation.darstellung.auswahl import PaarCache
from ldv_automation.gui import animation_anzeige as an
from ldv_automation.gui import anzeige_aktionen as ak
from ldv_automation.gui import stil, tokens
from ldv_automation.gui.animation_steuerung import (
    ANIMATIONS_TASTEN,
    DREH_SCHRITT_GRAD,
    Aktion,
    skalierung_nach_groessenwechsel,
)
from ldv_automation.gui.animation_tabelle import WerteTabelleDialog
from ldv_automation.gui.anzeige_auswerten import AuswertenZustand
from ldv_automation.gui.auswerten_reiter import AuswertenReiter
from ldv_automation.gui.plotflaeche import NEUZEICHNEN_MS

pytestmark = pytest.mark.gui

ATOL_GRAD = 1e-9  # Winkel: nur Gleitkomma-Rundung der Uhr (Plan 8)
RTOL = 1e-12  # Skalierung ↔ Überhöhung: Gleitkomma-Rundung einer Multiplikation/Division


class Uhr:
    """Handgeführte Zeitquelle in s (Phasenuhr): ``t`` ist die Zeit, Aufruf liefert sie."""

    def __init__(self) -> None:
        self.t = 0.0

    def __call__(self) -> float:
        return self.t


def ansicht_4(a: AuswertenReiter) -> None:
    a.btn_ansicht[4].click()
    QApplication.processEvents()


def animation(a: AuswertenReiter) -> None:
    """Wählt den Modus „Animation“ (Klick auf den Radioknopf)."""
    a.auswahl_sf.rb_modus_animation.click()
    QApplication.processEvents()


def oeffne(baue: Bauer, qtbot: QtBot, **synth: Any) -> tuple[AuswertenReiter, Uhr]:
    """Datei geladen, Ansicht 4 gewählt, Uhr der Wiedergabe von Hand geführt."""
    a = geladen_mit(baue, qtbot, **synth)
    ansicht_4(a)
    uhr = Uhr()
    a.animation.uhr._zeit = uhr
    return a, uhr


def daten(a: AuswertenReiter) -> AnimationsDaten:
    assert a._an_daten is not None
    return a._an_daten


def achse(a: AuswertenReiter) -> Any:
    assert a.animation.zeichnung is not None
    return a.animation.zeichnung.achsen[0]


def hilfs(a: AuswertenReiter, name: str) -> Any:
    assert a.animation.zeichnung is not None
    return a.animation.zeichnung.hilfsobjekte[name]


def geladen_mit_duplikat() -> Geladen:
    """Wie ``synth_geladen``, aber Punkt 1 liegt exakt auf Punkt 0 (Nachtrag 3)."""
    g = synth_geladen()
    d = g.messdaten
    koord = d.punkte.koordinaten_m.copy()
    koord[1] = koord[0]
    punkte = Punkte(index=d.punkte.index, label=d.punkte.label, koordinaten_m=koord)
    return replace(g, messdaten=replace(d, punkte=punkte))


def setze_annahmen(a: AuswertenReiter, annahmen: Annahmen) -> None:
    """Ersetzt den Cache der aktiven Messung (Annahmen wie M6 oder bestätigtes M8)."""
    a._cache = PaarCache(a._geladen.messdaten, annahmen=annahmen)  # type: ignore[union-attr]


def zaehle(a: AuswertenReiter, monkeypatch: pytest.MonkeyPatch) -> dict[str, int]:
    """Zählt Aufrufe von ``zeichne`` und ``aktualisiere`` der Animationsfläche."""
    zaehler = {"zeichne": 0, "aktualisiere": 0}
    zeichne, aktualisiere = a.animation.zeichne, a.animation.aktualisiere

    def z(*args: Any, **kw: Any) -> Any:
        zaehler["zeichne"] += 1
        return zeichne(*args, **kw)

    def ak(*args: Any, **kw: Any) -> Any:
        zaehler["aktualisiere"] += 1
        return aktualisiere(*args, **kw)

    monkeypatch.setattr(a.animation, "zeichne", z)
    monkeypatch.setattr(a.animation, "aktualisiere", ak)
    return zaehler


# --- UI-22: Standbild nach Öffnen und Frequenzwechsel, nie von selbst -------------------------


def test_ui22_nach_dem_oeffnen_steht_standbild_und_nichts_laeuft(baue: Bauer, qtbot: QtBot) -> None:
    a = geladen_mit(baue, qtbot)
    ansicht_4(a)
    sel = a.auswahl_sf
    assert sel.rb_modus_standbild.isChecked() and not sel.modus_animation()
    assert not a.animation.laeuft and not a.animation._timer.isActive()
    assert a.plot.isVisible() and not a.animation.isVisible()
    assert not a.animationsleiste.isVisible() and not sel.gruppe_animation_a.isVisible()
    assert sel.rb_groesse_betrag.isVisible()  # Gruppe des Standbilds unverändert


def test_ui22_die_animation_startet_nie_von_selbst(baue: Bauer, qtbot: QtBot) -> None:
    a, _uhr = oeffne(baue, qtbot)
    animation(a)
    assert a.animation.isVisible() and a.animationsleiste.isVisible()
    qtbot.wait(300)  # echte Zeit: ohne Klick läuft nichts
    assert not a.animation.laeuft and not a.animation._timer.isActive()
    assert a.animation.uhr.theta_grad == 0.0
    assert a.animationsleiste.btn_abspielen.text() == "Abspielen"


def test_ui22_frequenzwechsel_springt_ins_standbild_und_haelt_an(baue: Bauer, qtbot: QtBot) -> None:
    a, uhr = oeffne(baue, qtbot)
    animation(a)
    a.animationsleiste.btn_abspielen.click()
    assert a.animation.laeuft
    uhr.t = 1.0  # θ stünde nach 1 s bei 90°
    a.auswahl_sf.feld_frequenz.setValue(17.0)
    QApplication.processEvents()
    assert a.auswahl_sf.rb_modus_standbild.isChecked()
    assert not a.animation.laeuft and not a.animation._timer.isActive()
    assert a.animation.uhr.theta_rad == 0.0
    assert a.plot.isVisible() and not a.animation.isVisible()
    assert a._plot_ansicht == 4 and a.plot.zeichnung is not None  # das Standbild ist gezeichnet
    assert not a._an_gezeichnet and a._an_skalierung is None


def test_ui22_frequenz_ohne_signal_gesetzt_springt_ebenfalls_ins_standbild(
    baue: Bauer, qtbot: QtBot
) -> None:
    """Klick im Plot einer anderen Ansicht setzt die Frequenz still: trotzdem Standbild (F-A4)."""
    a, _uhr = oeffne(baue, qtbot)
    animation(a)
    a.btn_ansicht[1].click()
    a._plot_geklickt(10.0)
    assert a.auswahl_sf.rb_modus_standbild.isChecked() and not a.animation.laeuft
    ansicht_4(a)
    assert a.plot.isVisible() and a.auswahl_sf.frequenz_hz() == pytest.approx(10.0, abs=0.25)


def test_eintritt_in_den_modus_pausiert_und_setzt_theta_null(baue: Bauer, qtbot: QtBot) -> None:
    a, _uhr = oeffne(baue, qtbot)
    animation(a)
    a.animation.setze_theta_grad(90.0)
    assert a.animation.uhr.theta_grad == pytest.approx(90.0, abs=ATOL_GRAD)
    a.auswahl_sf.rb_modus_standbild.click()
    animation(a)
    assert a.animation.uhr.theta_grad == 0.0 and not a.animation.laeuft
    assert a.animationsleiste.lbl_phase_grad.text() == "θ = 0,0°"


def test_standbild_bleibt_nach_hin_und_zurueck_unveraendert(baue: Bauer, qtbot: QtBot) -> None:
    a, _uhr = oeffne(baue, qtbot)
    assert a.plot.zeichnung is not None
    vorher = a.plot.zeichnung.alle_texte()
    kopf = a.lbl_plotkopf.text()
    animation(a)
    assert a.lbl_plotkopf.text() != kopf  # Kopf der Animation
    a.auswahl_sf.rb_modus_standbild.click()
    QApplication.processEvents()
    assert a.plot.zeichnung is not None and a.plot.zeichnung.alle_texte() == vorher
    assert a.lbl_plotkopf.text() == kopf and a.plot.isVisible() and not a.animation.isVisible()


# --- UI-30: ohne Phase ist der Modus gesperrt -------------------------------------------------


def test_ui30_ohne_referenz_ist_der_modus_animation_gesperrt(baue: Bauer, qtbot: QtBot) -> None:
    a = geladen_mit(baue, qtbot, referenz=False)
    ansicht_4(a)
    sel = a.auswahl_sf
    assert not sel.rb_modus_animation.isEnabled()
    assert sel.lbl_modus_grund.text() == "Animation braucht eine Phase: keine Referenz."
    assert sel.rb_modus_animation.toolTip() == sel.lbl_modus_grund.text()
    assert sel.lbl_modus_grund.isVisible()
    QTest.mouseClick(sel.rb_modus_animation, Qt.MouseButton.LeftButton)
    assert sel.rb_modus_standbild.isChecked() and not a.animation.isVisible()


def test_mit_referenz_ist_der_modus_frei_und_ohne_grundtext(baue: Bauer, qtbot: QtBot) -> None:
    a = geladen_mit(baue, qtbot)
    ansicht_4(a)
    assert a.auswahl_sf.rb_modus_animation.isEnabled()
    assert not a.auswahl_sf.lbl_modus_grund.isVisible()


# --- UI-23: Blickrichtung ---------------------------------------------------------------------


@pytest.mark.parametrize("name", ["xy", "xz", "yz", "iso"])
def test_ui23_blickknoepfe_stellen_die_vorgaben_ein(baue: Bauer, qtbot: QtBot, name: str) -> None:
    a, _uhr = oeffne(baue, qtbot)
    animation(a)
    a.animationsleiste.btn_blick[name].click()
    vorgabe = BLICK_VORGABEN[name]
    assert a.animation.blick == vorgabe
    assert (achse(a).azim, achse(a).elev) == pytest.approx(
        (vorgabe.azim_grad, vorgabe.elev_grad), abs=ATOL_GRAD
    )


def test_ui23_mausziehen_dreht_und_zuruecksetzen_stellt_die_vorgabe_her(
    baue: Bauer, qtbot: QtBot
) -> None:
    a, _uhr = oeffne(baue, qtbot)
    animation(a)
    a.animationsleiste.btn_blick["iso"].click()
    start = QPoint(100, 100)
    canvas = a.animation.canvas
    QTest.mousePress(canvas, Qt.MouseButton.LeftButton, Qt.KeyboardModifier.NoModifier, start)
    QTest.mouseMove(canvas, start + QPoint(40, -20))
    QTest.mouseRelease(
        canvas, Qt.MouseButton.LeftButton, Qt.KeyboardModifier.NoModifier, start + QPoint(40, -20)
    )
    assert a.animation.blick != BLICK_VORGABEN["iso"]
    a.animationsleiste.btn_ansicht_zurueck.click()
    assert a.animation.blick == BLICK_VORGABEN["iso"]  # Zurücksetzen: zurück zur gewählten Vorgabe


def test_ui23_blickvorgabe_folgt_der_projektionsebene(baue: Bauer, qtbot: QtBot) -> None:
    a, _uhr = oeffne(baue, qtbot)
    animation(a)
    ebene = a.auswahl_sf.ebene()
    assert a.animation.blick == BLICK_VORGABEN[ebene]
    a.auswahl_sf.rb_ebene["xz"].click()
    assert a.animation.blick == BLICK_VORGABEN["xz"]
    a.animationsleiste.btn_blick["iso"].click()
    a.auswahl_sf.chk_punktlabels.click()  # andere Änderung: der Blick bleibt (Iso)
    assert a.animation.blick == BLICK_VORGABEN["iso"]


def test_farbkomponente_bei_3d_ist_die_achse_senkrecht_zur_ebene(baue: Bauer, qtbot: QtBot) -> None:
    a, _uhr = oeffne(baue, qtbot)
    animation(a)
    for ebene, komp in (("xy", 2), ("xz", 1), ("yz", 0)):
        a.auswahl_sf.rb_ebene[ebene].click()
        assert hilfs(a, "farbkomponente") == komp, ebene


# --- UI-24 und UI-32: Phasenregler, Abspielen, Einzelschritte ---------------------------------


def test_ui24_phasenanzeige_in_grad_schritte_und_regler(baue: Bauer, qtbot: QtBot) -> None:
    a, _uhr = oeffne(baue, qtbot)
    animation(a)
    ah = a.animationsleiste
    assert ah.lbl_phase_grad.text() == "θ = 0,0°"
    ah.btn_schritt_vor.click()  # Voreinstellung 10°
    assert a.animation.uhr.theta_grad == pytest.approx(10.0, abs=ATOL_GRAD)
    assert ah.lbl_phase_grad.text() == "θ = 10,0°" and ah.regler_phase.value() == 100
    ah.feld_schrittweite.setValue(45.0)
    ah.btn_schritt_zurueck.click()
    assert a.animation.uhr.theta_grad == pytest.approx(
        325.0, abs=ATOL_GRAD
    )  # 10° minus 45° mod 360°
    assert ah.lbl_phase_grad.text() == "θ = 325,0°"
    ah.regler_phase.setValue(900)  # Regler auf 90,0°
    assert a.animation.uhr.theta_grad == pytest.approx(90.0, abs=ATOL_GRAD)
    assert ah.lbl_phase_grad.text() == "θ = 90,0°"
    assert ah.regler_phase.maximum() == 3599  # 0 bis 359,9° in 0,1°-Schritten


def test_ui24_abspielen_laeuft_um_pause_haelt_an(baue: Bauer, qtbot: QtBot) -> None:
    a, uhr = oeffne(baue, qtbot)
    animation(a)
    ah = a.animationsleiste
    ah.btn_abspielen.click()
    assert a.animation.laeuft and ah.btn_abspielen.text() == "Pause"
    assert ah.btn_abspielen.accessibleName() == "Animation anhalten"
    uhr.t = 1.0  # 0,25 Perioden/s: nach 1 s steht θ bei 90°
    a.animation.takt()
    assert a.animation.uhr.theta_grad == pytest.approx(90.0, abs=1e-6)
    assert ah.lbl_phase_grad.text() == "θ = 90,0°" and ah.regler_phase.value() == 900
    uhr.t = 5.0  # eine volle Periode später (4 s · 0,25 Hz): wieder 90°
    a.animation.takt()
    assert a.animation.uhr.theta_grad == pytest.approx(90.0, abs=1e-6)
    ah.btn_abspielen.click()  # Pause
    assert not a.animation.laeuft and ah.btn_abspielen.text() == "Abspielen"
    uhr.t = 9.0
    a.animation.takt()  # hält: kein Fortschritt ohne Wiedergabe
    assert a.animation.uhr.theta_grad == pytest.approx(90.0, abs=1e-6)


def test_ui24_tempo_regler_aendert_die_geschwindigkeit(baue: Bauer, qtbot: QtBot) -> None:
    a, uhr = oeffne(baue, qtbot)
    animation(a)
    ah = a.animationsleiste
    assert a.animation.uhr.tempo_hz == 0.25 and ah.lbl_tempo.text() == "0,25 Perioden/s"
    ah.regler_tempo.setValue(0)  # 1,0 Perioden/s
    assert (
        a.animation.uhr.tempo_hz == pytest.approx(1.0) and ah.lbl_tempo.text() == "1,0 Perioden/s"
    )
    ah.btn_abspielen.click()
    uhr.t = 0.25  # 1/4 Periode bei 1 Hz: 90°
    a.animation.takt()
    assert a.animation.uhr.theta_grad == pytest.approx(90.0, abs=1e-6)
    ah.btn_abspielen.click()


def test_ui32_alles_ohne_wiedergabe_ueber_regler_und_tastatur(baue: Bauer, qtbot: QtBot) -> None:
    a, _uhr = oeffne(baue, qtbot)
    animation(a)
    ah = a.animationsleiste
    a.animation.canvas.setFocus()
    QTest.keyClick(a.animation.canvas, Qt.Key.Key_Right)  # →: Phase um die Schrittweite
    assert a.animation.uhr.theta_grad == pytest.approx(10.0, abs=ATOL_GRAD)
    assert ah.lbl_phase_grad.text() == "θ = 10,0°" and ah.regler_phase.value() == 100
    QTest.keyClick(a.animation.canvas, Qt.Key.Key_Left)
    assert a.animation.uhr.theta_grad == pytest.approx(0.0, abs=ATOL_GRAD)
    ah.regler_phase.setFocus()
    QTest.keyClick(ah.regler_phase, Qt.Key.Key_Right)  # Pfeil im Regler: eine Schrittweite
    assert a.animation.uhr.theta_grad == pytest.approx(10.0, abs=ATOL_GRAD)
    assert not a.animation.laeuft  # nichts davon braucht die Wiedergabe
    # Aussage über die Auslenkung ist ohne Wiedergabe abrufbar: Textalternative nennt den Winkel
    assert "θ = 10,0°" in a.animation.beschreibung
    assert a.animation.canvas.accessibleDescription() == a.animation.beschreibung


def test_leertaste_im_regler_schaltet_abspielen_und_pause(baue: Bauer, qtbot: QtBot) -> None:
    a, _uhr = oeffne(baue, qtbot)
    animation(a)
    ah = a.animationsleiste
    ah.regler_tempo.setFocus()
    QTest.keyClick(ah.regler_tempo, Qt.Key.Key_Space)
    assert a.animation.laeuft
    QTest.keyClick(ah.regler_tempo, Qt.Key.Key_Space)
    assert not a.animation.laeuft


def test_schrittweite_steuert_die_einzelschritte_des_reglers(baue: Bauer, qtbot: QtBot) -> None:
    a, _uhr = oeffne(baue, qtbot)
    animation(a)
    ah = a.animationsleiste
    ah.feld_schrittweite.setValue(30.0)
    assert a.animation.uhr.schritt_grad == 30.0 and ah.regler_phase.singleStep() == 300
    assert ah.regler_phase.pageStep() == 900


# --- UI-25: dargestellte Phase = Zustand der Animation ----------------------------------------


def test_ui25_positionen_der_figure_folgen_dem_winkel_der_leiste(baue: Bauer, qtbot: QtBot) -> None:
    a, _uhr = oeffne(baue, qtbot)
    animation(a)
    d = daten(a)
    s = effektive_ueberhoehung(d, AnimationsOptionen())
    for grad in (0.0, 90.0, 215.5):
        a.animationsleiste.regler_phase.setValue(round(grad * 10))
        erwartet = d.positionen(math.radians(grad), s)[d.bewegt]
        punkte = a.animation.zeichnung.marker["punkte"]  # type: ignore[union-attr]
        ist = np.column_stack([np.asarray(v) for v in punkte._offsets3d])
        np.testing.assert_allclose(ist, erwartet, rtol=1e-12, atol=1e-15)


# --- UI-26: Überhöhung ------------------------------------------------------------------------


def test_ui26_ueberhoehung_steht_als_zahl_in_bild_leiste_und_textalternative(
    baue: Bauer, qtbot: QtBot
) -> None:
    a, _uhr = oeffne(baue, qtbot)
    animation(a)
    ah = a.animationsleiste
    s_auto = daten(a).s_auto
    assert s_auto is not None
    assert ah.regler_ueberhoehung.value() == 0 and ah.feld_skalierung.text() == ""  # automatisch
    assert ah.feld_skalierung.placeholderText() == "Auto"
    zahl = f"{s_auto:.4g}".replace(".", ",")
    assert ah.lbl_ueberhoehung.text() == f"Überhöhung \N{MULTIPLICATION SIGN}{zahl}"
    assert f"Überhöhung \N{MULTIPLICATION SIGN}{zahl}" in hilfs(a, "pflichttext").get_text()
    assert f"Überhöhung \N{MULTIPLICATION SIGN}{zahl}" in a.animation.beschreibung


def test_ui26_regler_und_feld_setzen_die_ueberhoehung_im_bild(baue: Bauer, qtbot: QtBot) -> None:
    a, _uhr = oeffne(baue, qtbot)
    animation(a)
    ah = a.animationsleiste
    s_auto = daten(a).s_auto
    assert s_auto is not None
    ah.regler_ueberhoehung.setValue(100)  # Faktor 10
    assert a._an_skalierung == pytest.approx(10.0 * s_auto, rel=RTOL)
    assert hilfs(a, "skalierung") == pytest.approx(10.0 * s_auto, rel=RTOL)
    assert ah.feld_skalierung.text() != "" and ah.feld_skalierung.property("fest") == "true"
    ah.feld_skalierung.setText("1,5")  # Feld: Zahl mit Dezimalkomma
    ah.feld_skalierung.editingFinished.emit()
    assert a._an_skalierung == 1.5 and hilfs(a, "skalierung") == 1.5
    assert "Überhöhung \N{MULTIPLICATION SIGN}1,5" in a.animation.beschreibung
    assert "Überhöhung \N{MULTIPLICATION SIGN}1,5" in hilfs(a, "pflichttext").get_text()
    assert ah.regler_ueberhoehung.value() == an.regler_aus_skalierung(1.5, s_auto)
    ah.feld_skalierung.setText("")  # leer = automatisch
    ah.feld_skalierung.editingFinished.emit()
    assert a._an_skalierung is None and ah.regler_ueberhoehung.value() == 0
    assert hilfs(a, "skalierung") == pytest.approx(s_auto, rel=RTOL)


def test_ui26_ungueltige_skalierung_meldet_und_aendert_nichts(baue: Bauer, qtbot: QtBot) -> None:
    a, _uhr = oeffne(baue, qtbot)
    animation(a)
    ah = a.animationsleiste
    vorher = hilfs(a, "skalierung")
    for text in ("0", "-2", "abc"):
        ah.feld_skalierung.setText(text)
        ah.feld_skalierung.editingFinished.emit()
        assert a._an_skalierung is None and hilfs(a, "skalierung") == vorher, text
        assert ah.feld_skalierung.property("fehler") == "true", text
        assert a.lbl_cursor.volltext().startswith(tokens.symbol("fehler")), text
    ah.feld_skalierung.setText("")  # wieder wie angewendet: Meldung weg
    ah.feld_skalierung.editingFinished.emit()
    assert ah.feld_skalierung.property("fehler") == "false"


def test_ui26_ohne_nachbarabstand_ist_der_regler_gesperrt_und_das_feld_gilt(
    baue: Bauer, qtbot: QtBot
) -> None:
    a = geladen_mit(baue, qtbot)
    g = a._geladen
    assert g is not None
    eins = replace(
        g.messdaten,
        punkte=Punkte(
            index=g.messdaten.punkte.index[:1],
            label=g.messdaten.punkte.label[:1],
            koordinaten_m=g.messdaten.punkte.koordinaten_m[:1],
        ),
        ap={k: v[:1] for k, v in g.messdaten.ap.items()},
        cp={k: v[:1] for k, v in g.messdaten.cp.items()},
    )
    a._geladen = replace(g, messdaten=eins)
    a._cache = PaarCache(eins)
    ansicht_4(a)
    animation(a)
    ah = a.animationsleiste
    assert daten(a).s_auto is None and not ah.regler_ueberhoehung.isEnabled()
    ah.feld_skalierung.setText("100")
    ah.feld_skalierung.editingFinished.emit()
    assert a._an_skalierung == 100.0 and hilfs(a, "skalierung") == 100.0


def test_ueberlagerungshinweis_steht_in_ad_und_af(baue: Bauer, qtbot: QtBot) -> None:
    a, _uhr = oeffne(baue, qtbot)
    animation(a)
    assert "überlagern" not in a.auswahl_sf.lbl_hinweise.text()  # automatisch: unterhalb der Grenze
    ah = a.animationsleiste
    ah.feld_skalierung.setText("1e9")
    ah.feld_skalierung.editingFinished.emit()
    hinweis = daten(a).hinweis_ueberhoehung(1e9)
    assert hinweis is not None and "überlagern" in hinweis
    assert hinweis in a.auswahl_sf.lbl_hinweise.text()
    # AF nennt auch den Hinweis zur Dichte der Punktlabels, wenn er gilt (UI-D2)
    assert a.lbl_cursor.volltext().startswith(f"{tokens.symbol('warnung')} {hinweis}")


def test_hinweis_zu_doppelten_punkten_steht_in_der_oberflaeche(baue: Bauer, qtbot: QtBot) -> None:
    w, prot = baue()
    prot.geladen[PFAD] = geladen_mit_duplikat()
    a = lade(qtbot, w)
    ansicht_4(a)
    animation(a)
    hinweis = daten(a).hinweis_duplikate
    assert hinweis is not None and daten(a).n_dup == 1
    assert hinweis in a.auswahl_sf.lbl_hinweise.text()
    assert a.auswahl_sf.lbl_hinweise.isVisible()
    assert "1 Punkt liegt auf dem Ort eines anderen Punkts" in a.auswahl_sf.lbl_hinweise.text()


def test_groessenwechsel_erhaelt_die_bildgroesse_der_skalierung(baue: Bauer, qtbot: QtBot) -> None:
    a, _uhr = oeffne(baue, qtbot)
    animation(a)
    ah = a.animationsleiste
    ah.feld_skalierung.setText("12,5")
    ah.feld_skalierung.editingFinished.emit()
    alt = daten(a)
    aequivalent = alt.ueberhoehung_aequivalent(12.5)
    a.auswahl_sf.rb_groesse_schnelle.click()
    neu = daten(a)
    assert neu.groesse == "schnelle" and alt.groesse == "auslenkung"
    assert a._an_skalierung == pytest.approx(neu.skalierung_aus_ueberhoehung(aequivalent), rel=RTOL)
    assert a._an_skalierung == skalierung_nach_groessenwechsel(alt, neu, 12.5)
    assert a._an_skalierung is not None
    assert neu.ueberhoehung_aequivalent(a._an_skalierung) == pytest.approx(12.5, rel=RTOL)
    assert " s (entspricht Überhöhung " in ah.lbl_ueberhoehung.text()  # Schnelle: Skalierung in s
    a.auswahl_sf.rb_groesse_auslenkung.click()
    assert a._an_skalierung == pytest.approx(12.5, rel=RTOL)  # und zurück: derselbe Wert


# --- UI-27: Farbbereich -----------------------------------------------------------------------


def farbfeld(a: AuswertenReiter, seite: str, text: str) -> None:
    feld: QLineEdit = a.auswahl_sf.feld_farbe_von if seite == "von" else a.auswahl_sf.feld_farbe_bis
    feld.setText(text)
    feld.editingFinished.emit()


def test_ui27_farbbereich_in_anzeigeeinheit_wirkt_auf_die_farbleiste(
    baue: Bauer, qtbot: QtBot
) -> None:
    a, _uhr = oeffne(baue, qtbot)
    animation(a)
    sel = a.auswahl_sf
    faktor, einheit = an.farb_anzeige(daten(a), a._an_optionen(daten(a)))
    assert sel.lbl_farbe_einheit.text() == einheit != ""
    assert sel.feld_farbe_von.text() == "" and sel.feld_farbe_bis.text() == ""  # Auto
    farbfeld(a, "von", "-0,5")
    farbfeld(a, "bis", "0,25")
    assert hilfs(a, "farbbereich") == pytest.approx((-0.5 / faktor, 0.25 / faktor), rel=RTOL)
    norm = hilfs(a, "farbleiste").mappable.norm
    assert (norm.vmin, norm.vmax) == pytest.approx((-0.5 / faktor, 0.25 / faktor), rel=RTOL)
    assert sel.feld_farbe_von.text() == "\N{MINUS SIGN}0,5" and sel.feld_farbe_bis.text() == "0,25"
    titel = hilfs(a, "farbtitel")
    vmax = max(0.5 / faktor, 0.25 / faktor)
    assert titel.endswith(f"[{skaliere_einheit(vmax, daten(a).einheit_anim)[1]}]")  # Einheit
    farbfeld(a, "von", "")  # leer = Auto (jede Seite einzeln)
    assert a._an_farbbereich == Bereich(None, pytest.approx(0.25 / faktor, rel=RTOL))  # type: ignore[arg-type]


def test_ui27_ungueltige_eingabe_zeigt_die_meldung_wie_ui_5(baue: Bauer, qtbot: QtBot) -> None:
    a, _uhr = oeffne(baue, qtbot)
    animation(a)
    sel = a.auswahl_sf
    farbfeld(a, "von", "-1")
    farbfeld(a, "bis", "1")
    vorher = hilfs(a, "farbbereich")
    farbfeld(a, "von", "2")  # von >= bis
    assert sel.lbl_farbbereich_meldung.isVisible() and sel.farbfehler_aktiv("von")
    assert sel.lbl_farbbereich_meldung.text() == f"{tokens.symbol('fehler')} {TEXT_REIHENFOLGE}"
    assert sel.feld_farbe_von.property("fehler") == "true"
    assert hilfs(a, "farbbereich") == vorher  # nichts gezeichnet
    farbfeld(a, "von", "abc")
    assert "Zahl" in sel.lbl_farbbereich_meldung.text()
    farbfeld(a, "von", "-1")  # wieder der angewendete Wert: Meldung weg
    assert not sel.lbl_farbbereich_meldung.isVisible() and not sel.farbfehler_aktiv("von")
    farbfeld(a, "von", "-2")  # gültig
    assert not sel.farbfehler_aktiv("von")


def test_ui27_gemischter_bereich_wird_gegen_auto_geprueft(baue: Bauer, qtbot: QtBot) -> None:
    a, _uhr = oeffne(baue, qtbot)
    animation(a)
    farbfeld(a, "von", "1e9")  # jenseits der automatischen Obergrenze
    assert a.auswahl_sf.farbfehler_aktiv("von") and a._an_farbbereich == Bereich()


def test_ui37_eingaben_im_farbbereich_zeichnen_erst_bei_enter_oder_fokuswechsel(
    baue: Bauer, qtbot: QtBot, monkeypatch: pytest.MonkeyPatch
) -> None:
    a, _uhr = oeffne(baue, qtbot)
    animation(a)
    zaehler = zaehle(a, monkeypatch)
    sel = a.auswahl_sf
    feld = sel.feld_farbe_von
    feld.setFocus()
    feld.selectAll()
    QTest.keyClicks(feld, "-1,5")  # Tippen: kein Neuzeichnen
    assert zaehler == {"zeichne": 0, "aktualisiere": 0}
    QTest.keyClick(feld, Qt.Key.Key_Return)  # Enter: genau eine Teilaktualisierung
    assert zaehler == {"zeichne": 0, "aktualisiere": 1}
    QTest.keyClick(feld, Qt.Key.Key_Return)  # Enter ohne Änderung: keines
    assert zaehler["aktualisiere"] == 1
    feld.selectAll()
    QTest.keyClicks(feld, "-2")
    sel.feld_farbe_bis.setFocus()  # Fokuswechsel mit Änderung: eines
    assert zaehler["aktualisiere"] == 2
    sel.feld_farbe_von.setFocus()  # Fokuswechsel ohne Änderung: keines
    sel.feld_farbe_bis.setFocus()
    assert zaehler["aktualisiere"] == 2 and zaehler["zeichne"] == 0


def test_farbe_betrag_zeichnet_neu_und_behaelt_winkel_und_blick(baue: Bauer, qtbot: QtBot) -> None:
    a, _uhr = oeffne(baue, qtbot)
    animation(a)
    a.animationsleiste.btn_blick["iso"].click()
    a.animationsleiste.regler_phase.setValue(900)
    a.auswahl_sf.rb_farbe_betrag.click()
    assert hilfs(a, "optionen").farbe == "betrag" and "Betrag" in hilfs(a, "farbtitel")
    assert a.animation.uhr.theta_grad == pytest.approx(90.0, abs=ATOL_GRAD)
    assert a.animation.blick == BLICK_VORGABEN["iso"]
    vmin, vmax = hilfs(a, "farbbereich")
    assert vmin == 0.0 and vmax > 0.0  # Betrag: 0 bis Maximum


# --- Bezug, Größe, Komponente: neue Daten, Blick und Winkel bleiben ---------------------------


def test_wechsel_von_bezug_groesse_und_komponente_behaelt_blick_und_winkel(
    baue: Bauer, qtbot: QtBot
) -> None:
    a, _uhr = oeffne(baue, qtbot)
    animation(a)
    sel = a.auswahl_sf
    a.animationsleiste.btn_blick["yz"].click()
    a.animationsleiste.regler_phase.setValue(1234)
    alt = daten(a)
    sel.rb_bezug_absolut.click()
    assert daten(a) is not alt and daten(a).bezug_modus == "absolut"
    sel.rb_groesse_schnelle.click()
    assert daten(a).groesse == "schnelle"
    sel.rb_komp["Z"].click()
    assert daten(a).komponente == "Z"
    assert a.animation.blick == BLICK_VORGABEN["yz"]
    assert a.animation.uhr.theta_grad == pytest.approx(123.4, abs=ATOL_GRAD)
    assert not a.animation.laeuft


def test_daten_werden_bei_unveraenderter_auswahl_nicht_neu_berechnet(
    baue: Bauer, qtbot: QtBot
) -> None:
    a, _uhr = oeffne(baue, qtbot)
    animation(a)
    erste = daten(a)
    a.auswahl_sf.rb_farbe_betrag.click()  # nur die Farbe: dieselben Daten
    assert daten(a) is erste
    a.auswahl_sf.chk_punktlabels.click()
    assert daten(a) is erste


def test_ungueltiger_bezugspunkt_meldet_in_af_und_das_bild_bleibt(
    baue: Bauer, qtbot: QtBot
) -> None:
    a, _uhr = oeffne(baue, qtbot)
    animation(a)
    setze_annahmen(a, Annahmen(gueltig=[True, False, True, True]))
    a.auswahl_sf.rb_farbe_betrag.click()  # neuer Cache: Daten neu, Punkt 1 ist M6-ungültig
    a.auswahl_sf.combo_bezug.setCurrentIndex(2)  # Punkt 1
    assert a.lbl_cursor.volltext().startswith(tokens.symbol("fehler"))
    assert "Bezugspunkt" in a.lbl_cursor.volltext()
    assert a._an_gezeichnet and a.animation.isVisible()  # das letzte gültige Bild bleibt


# --- UI-28: Kennzeichen im Kopf ---------------------------------------------------------------


def test_ui28_kopf_nennt_m8_bei_absolutem_bezug_dauerhaft(baue: Bauer, qtbot: QtBot) -> None:
    a, uhr = oeffne(baue, qtbot)
    animation(a)
    kopf = a.lbl_plotkopf.text()
    assert KENNZEICHEN_M8 not in kopf  # relativ: kein M8
    assert f"{tokens.symbol('warnung')} {KENNZEICHEN_M12}" in kopf  # 3D: M12 solange offen
    a.auswahl_sf.rb_bezug_absolut.click()
    kopf = a.lbl_plotkopf.text()
    assert f"{tokens.symbol('warnung')} {KENNZEICHEN_M8}" in kopf
    assert "Phase gegen Ref1" in kopf
    # dauerhaft: der Kopf bleibt während der Wiedergabe unverändert sichtbar
    a.animationsleiste.btn_abspielen.click()
    uhr.t = 0.5
    a.animation.takt()
    assert a.lbl_plotkopf.text() == kopf and a.lbl_plotkopf.isVisible()
    a.animationsleiste.btn_abspielen.click()
    # dasselbe Kennzeichen steht im Bild und in der Textalternative
    assert any(KENNZEICHEN_M8 in t for t in a.animation.zeichnung.alle_texte())  # type: ignore[union-attr]
    assert KENNZEICHEN_M8 in a.animation.beschreibung


def test_ui28_kennzeichen_m8_verschwindet_bei_bestaetigtem_status_ohne_codeaenderung(
    baue: Bauer, qtbot: QtBot
) -> None:
    a, _uhr = oeffne(baue, qtbot)
    animation(a)
    a.auswahl_sf.rb_bezug_absolut.click()
    assert KENNZEICHEN_M8 in a.lbl_plotkopf.text()
    assert "M8" in a.auswahl_sf.rb_bezug_absolut.text()  # Beschriftung des Radioknopfs
    setze_annahmen(a, Annahmen(status={"M8": "bestätigt am 2026-12-01"}))
    a.auswahl_sf.chk_punktlabels.click()  # beliebige Änderung: neu zeichnen
    assert "M8" not in a.lbl_plotkopf.text()
    assert not any("M8" in t for t in a.animation.zeichnung.alle_texte())  # type: ignore[union-attr]
    assert "M8" not in a.animation.beschreibung


def test_ui28_kennzeichen_m12_folgt_dem_status_aus_stufe_2(
    baue: Bauer, qtbot: QtBot, monkeypatch: pytest.MonkeyPatch
) -> None:
    a, _uhr = oeffne(baue, qtbot)
    animation(a)
    assert KENNZEICHEN_M12 in a.lbl_plotkopf.text()
    assert any(KENNZEICHEN_M12 in t for t in a.animation.zeichnung.alle_texte())  # type: ignore[union-attr]
    monkeypatch.setattr(
        a, "_annahmen_stufe2", lambda: AnnahmenStufe2(status={"M12": "bestätigt am 2026-12-01"})
    )
    a._kennzeichen_aktualisieren()  # Annahmen neu übernommen
    assert "M12" not in a.lbl_plotkopf.text()
    assert not any("M12" in t for t in a.animation.zeichnung.alle_texte())  # type: ignore[union-attr]
    assert "M12" not in a.animation.beschreibung


# --- UI-29: gekennzeichnete Punkte ------------------------------------------------------------


def test_ui29_gekennzeichnete_punkte_mit_symbol_wie_im_standbild_und_anzahl(
    baue: Bauer, qtbot: QtBot
) -> None:
    a, _uhr = oeffne(baue, qtbot)
    setze_annahmen(a, Annahmen(gueltig=[True, False, True, True]))
    a.auswahl_sf.chk_punktlabels.click()  # Standbild mit dem neuen Cache zeichnen
    standbild = a.plot.zeichnung
    assert standbild is not None and "ungueltig" in standbild.marker
    form_2d = standbild.marker["ungueltig"].get_paths()[0].vertices
    animation(a)
    z = a.animation.zeichnung
    assert z is not None and "ungueltig" in z.marker
    np.testing.assert_allclose(z.marker["ungueltig"].get_paths()[0].vertices, form_2d, atol=1e-12)
    assert z.hilfsobjekte["anzahl"]["ungueltig"] == 1
    legende = [t.get_text() for t in z.hilfsobjekte["zeichenerklaerung"].get_texts()]
    assert "ungültig (M6) (1)" in legende
    assert any("ungültig (M6) (1)" in t for t in standbild.alle_texte())  # Standbild: gleiche Zeile
    d = daten(a)
    assert not d.bewegt[1] and bool(d.bewegt[0])
    pos = d.positionen(math.radians(90.0), 5.0)
    np.testing.assert_array_equal(pos[1], d.koordinaten_m[1])  # steht exakt in der Ruhelage


# --- Seiten, Zustände, Meldungen --------------------------------------------------------------


def test_leaving_ansicht_4_pausiert_und_der_modus_bleibt(baue: Bauer, qtbot: QtBot) -> None:
    a, _uhr = oeffne(baue, qtbot)
    animation(a)
    a.animationsleiste.btn_abspielen.click()
    assert a.animation.laeuft
    a.btn_ansicht[1].click()
    assert not a.animation.laeuft and not a.animation._timer.isActive()  # Fortsetzen nur per Nutzer
    assert not a.animation.isVisible() and not a.animationsleiste.isVisible()
    ansicht_4(a)
    assert a.animation.isVisible() and a.animationsleiste.isVisible()
    assert not a.animation.laeuft and a.animationsleiste.btn_abspielen.text() == "Abspielen"


def test_wechsel_der_aktiven_messung_loest_standbild_aus(baue: Bauer) -> None:
    a, _prot, _w, ausf = aufbau(baue)
    del ausf
    messung_b = next(m for m in a.messungen.bereite() if m is not a.messungen.aktive)
    a.btn_ansicht[4].click()
    QApplication.processEvents()
    animation(a)
    assert a.auswahl_sf.modus_animation() and a._an_gezeichnet
    a._aktiviere_messung(messung_b.id)
    QApplication.processEvents()
    assert a.auswahl_sf.rb_modus_standbild.isChecked() and not a._an_gezeichnet
    assert a.plot.isVisible() and not a.animation.isVisible() and not a.animation.laeuft


def test_neue_datei_setzt_die_animation_zurueck(baue: Bauer, qtbot: QtBot) -> None:
    a, _uhr = oeffne(baue, qtbot)
    animation(a)
    a.animationsleiste.feld_skalierung.setText("7")
    a.animationsleiste.feld_skalierung.editingFinished.emit()
    farbfeld(a, "von", "-1")
    a.oeffne_datei(PFAD)
    qtbot.waitUntil(lambda: a.zustand is AuswertenZustand.GELADEN and not a.laeuft(), timeout=5000)
    assert a._an_daten is None and a._an_skalierung is None and a._an_farbbereich == Bereich()
    assert a.auswahl_sf.rb_modus_standbild.isChecked() and not a.animation.isVisible()
    ansicht_4(a)
    assert a.auswahl_sf.feld_farbe_von.text() == "" and a.plot.isVisible()


def test_paarcache_haelt_in_der_animation_drei_paare(baue: Bauer, qtbot: QtBot) -> None:
    a, _uhr = oeffne(baue, qtbot)
    assert a._cache is not None and a._cache.groesse == 2
    animation(a)
    assert a._cache.groesse >= 3 and len(a._cache.gespeichert()) == 3  # X, Y, Z derselben Referenz
    a._cache_groessen_anpassen()  # Ansicht 5 darf die Größe der aktiven Messung nicht senken
    assert a._cache.groesse >= 3
    a.auswahl_sf.rb_modus_standbild.click()
    assert a._cache.groesse == 2  # zurück: Speicher wieder frei


def test_paarcache_hat_nach_abstecher_in_ansicht_5_wieder_drei_paare(
    baue: Bauer, qtbot: QtBot
) -> None:
    a, _uhr = oeffne(baue, qtbot)
    animation(a)
    assert a._cache is not None and a._cache.groesse == 3
    a.btn_ansicht[5].click()  # Ansicht 5 stellt den Cache auf den Serienbedarf (2)
    QApplication.processEvents()
    assert a._cache.groesse == 2
    ansicht_4(a)
    assert a.auswahl_sf.modus_animation() and a._cache.groesse == 3


def test_bild_speichern_ist_im_modus_animation_frei(baue: Bauer, qtbot: QtBot) -> None:
    a, _uhr = oeffne(baue, qtbot)
    assert a.btn_bild.isEnabled()
    animation(a)
    assert a.btn_bild.isEnabled()  # AN8: das Standbild der Animation lässt sich speichern
    a.auswahl_sf.rb_modus_standbild.click()
    assert a.btn_bild.isEnabled()


# --- AN8: Standbild speichern (UI-31) ---------------------------------------------------------


def _speichere_animation(
    a: AuswertenReiter, m: Meldungen, monkeypatch: pytest.MonkeyPatch, pfad: Path
) -> tuple[Any, list[str]]:
    """Klickt ``Bild speichern …`` im Modus Animation; liefert die gespeicherte Zeichnung."""
    gespeichert: list[Any] = []
    vorschlaege: list[str] = []
    original = a.animation.speichere

    def erfasse(ziel: Path, stempel: Any) -> Any:
        z = original(ziel, stempel)
        gespeichert.append(z)
        return z

    monkeypatch.setattr(a.animation, "speichere", erfasse)

    def waehle(vorschlag: str) -> str | None:
        vorschlaege.append(vorschlag)
        return m.bild_ziel

    monkeypatch.setattr(a, "_waehle_bild_ziel", waehle)
    m.bild_ziel = str(pfad)
    a.btn_bild.click()
    return (gespeichert[0] if gespeichert else None), vorschlaege


def test_ui31_png_mit_stempel_winkel_blick_ueberhoehung_frequenz(
    baue: Bauer, qtbot: QtBot, monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    a, _uhr = oeffne(baue, qtbot)
    m = Meldungen(a, monkeypatch)
    animation(a)
    a.animation.setze_theta_grad(90.0)
    a.animation.setze_blick_vorgabe("iso")
    z, vorschlaege = _speichere_animation(a, m, monkeypatch, tmp_path / "an.png")
    assert (tmp_path / "an.png").read_bytes()[:4] == b"\x89PNG"
    assert vorschlaege[0].endswith("_ansicht4_animation_theta090.png")
    texte = z.alle_texte()
    stempel = next(t for t in texte if t.startswith("Arbeitsansicht"))
    assert "probe.svd" in stempel and "Ansicht 4" in stempel and "c" * 12 in stempel
    zusatz = next(t for t in texte if t.startswith("Animation · θ"))
    assert "θ = 90,0°" in zusatz and f"f = {16:d},000 Hz" in zusatz
    assert "Überhöhung \N{MULTIPLICATION SIGN}" in zusatz
    blick = next(t for t in texte if t.startswith("Blickrichtung:"))
    assert "Elevation 35,3°" in blick and "Azimut \N{MINUS SIGN}45,0°" in blick
    assert any("enthält unbestätigte Größen (M12)" in t for t in texte)  # 3D, M12 offen
    assert not any("M8" in t for t in texte)  # relativer Bezug: kein M8
    assert a.lbl_cursor.text() == ak.bild_meldung(str(tmp_path / "an.png"))
    # das Bild enthält zusätzlich die Pflichttexte der Zeichenfunktion (Überhöhung, D_ref, f, θ)
    assert any("größte reale Spitzenauslenkung" in t for t in texte)


def test_ui31_standbild_bei_theta_hat_die_positionen_der_animation_bei_theta(
    baue: Bauer, qtbot: QtBot, monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    a, _uhr = oeffne(baue, qtbot)
    m = Meldungen(a, monkeypatch)
    animation(a)
    for grad in (0.0, 90.0, 217.0):
        a.animation.setze_theta_grad(grad)
        live = scatter_positionen(a.animation.zeichnung)  # type: ignore[arg-type]
        z, _v = _speichere_animation(a, m, monkeypatch, tmp_path / f"p{int(grad)}.png")
        d = daten(a)
        s = effektive_ueberhoehung(d, a.animation.standbild_optionen)  # type: ignore[arg-type]
        theta = a.animation.uhr.theta_rad
        assert np.array_equal(scatter_positionen(z), live)  # Bildschirm = Datei
        assert np.array_equal(scatter_positionen(z), d.positionen(theta, s)[d.bewegt])
        assert not np.allclose(live, d.koordinaten_m[d.bewegt]) or grad == 0.0


def test_ui31_pdf_ist_ein_pdf(
    baue: Bauer, qtbot: QtBot, monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    a, _uhr = oeffne(baue, qtbot)
    m = Meldungen(a, monkeypatch)
    animation(a)
    _speichere_animation(a, m, monkeypatch, tmp_path / "an.pdf")
    assert (tmp_path / "an.pdf").read_bytes()[:4] == b"%PDF"


def test_ui31_nur_png_und_pdf_kein_video_oder_gif() -> None:
    filter_text = ak.DATEIFILTER_BILD.lower()
    assert "png" in filter_text and "pdf" in filter_text
    assert not any(x in filter_text for x in ("gif", "mp4", "avi", "webm", "mov"))


def test_ui28_stempel_nennt_m8_und_m12_aus_derselben_quelle_wie_das_bild(
    baue: Bauer, qtbot: QtBot, monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    a, _uhr = oeffne(baue, qtbot)
    m = Meldungen(a, monkeypatch)
    animation(a)
    a.auswahl_sf.rb_bezug_absolut.click()
    z, _v = _speichere_animation(a, m, monkeypatch, tmp_path / "m8.png")
    texte = z.alle_texte()
    assert any("enthält unbestätigte Größen (M8, M12)" in t for t in texte)
    assert any(KENNZEICHEN_M8 in t for t in texte)  # Kennzeichen im Bild selbst
    # M8 bestätigt: weder Stempel noch Bild nennen es
    setze_annahmen(a, Annahmen(status={"M8": "bestätigt am 2026-12-01"}))
    a.auswahl_sf.chk_punktlabels.click()
    z, _v = _speichere_animation(a, m, monkeypatch, tmp_path / "m8b.png")
    texte = z.alle_texte()
    assert any("enthält unbestätigte Größen (M12)" in t for t in texte)
    assert not any("M8" in t for t in texte)


def test_ui31_einzelkomponente_relativ_hat_keinen_unbestaetigt_vermerk(
    baue: Bauer, qtbot: QtBot, monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    a, _uhr = oeffne(baue, qtbot)
    m = Meldungen(a, monkeypatch)
    a.auswahl_sf.rb_komp["Z"].click()
    animation(a)
    z, _v = _speichere_animation(a, m, monkeypatch, tmp_path / "z.png")
    assert not any("unbestätigte" in t for t in z.alle_texte())


def test_ui31_speichern_haelt_die_wiedergabe_an(
    baue: Bauer, qtbot: QtBot, monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    a, _uhr = oeffne(baue, qtbot)
    m = Meldungen(a, monkeypatch)
    animation(a)
    a.animationsleiste.btn_abspielen.click()
    assert a.animation.laeuft
    _speichere_animation(a, m, monkeypatch, tmp_path / "w.png")
    assert not a.animation.laeuft and (tmp_path / "w.png").exists()


def test_ui31_abbruch_des_dialogs_schreibt_nichts(
    baue: Bauer, qtbot: QtBot, monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    a, _uhr = oeffne(baue, qtbot)
    m = Meldungen(a, monkeypatch)
    animation(a)
    m.bild_ziel = None
    a.btn_bild.click()
    assert not [*tmp_path.glob("*.png"), *tmp_path.glob("*.pdf")] and not m.warnungen


def test_ui31_schreibfehler_wird_gemeldet_nicht_verschluckt(
    baue: Bauer, qtbot: QtBot, monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    a, _uhr = oeffne(baue, qtbot)
    m = Meldungen(a, monkeypatch)
    animation(a)
    m.bild_ziel = str(tmp_path / "gibtsnicht" / "x.png")
    a.btn_bild.click()
    assert m.warnungen and m.warnungen[0][0] == "Bild nicht gespeichert"


def test_standbildmodus_speichert_weiter_den_2d_plot(
    baue: Bauer, qtbot: QtBot, monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    """Regression: im Modus Standbild bleibt ``Bild speichern …`` bei der 2D-Fläche."""
    a, _uhr = oeffne(baue, qtbot)
    m = Meldungen(a, monkeypatch)
    animation(a)
    a.auswahl_sf.rb_modus_standbild.click()
    QApplication.processEvents()
    m.bild_ziel = str(tmp_path / "s.png")
    a.btn_bild.click()
    assert (tmp_path / "s.png").read_bytes()[:4] == b"\x89PNG"


# --- AN9: „Werte als Tabelle“ (UI-26) -----------------------------------------------------------


def test_ui26_werte_als_tabelle_nennt_alle_punkte_beim_aktuellen_winkel(
    baue: Bauer, qtbot: QtBot, monkeypatch: pytest.MonkeyPatch
) -> None:
    a, _uhr = oeffne(baue, qtbot)
    m = Meldungen(a, monkeypatch)
    animation(a)
    a.animation.setze_theta_grad(90.0)
    knopf = a.animationsleiste.btn_werte_tabelle
    assert knopf.isEnabled() and knopf.focusPolicy() != Qt.FocusPolicy.NoFocus
    assert knopf in a.animationsleiste.tab_kette()
    knopf.click()
    dialog = m.dialoge[0]
    assert isinstance(dialog, WerteTabelleDialog)
    d = daten(a)
    assert dialog.tabelle.rowCount() == d.anzahl_punkte
    assert dialog.tabelle.columnCount() == 9
    assert "θ = 90,0°" in dialog.lbl_titel.text()
    erstes = dialog.tabelle.item(0, 0)
    assert erstes is not None and erstes.text() == str(int(d.label[0]))
    dialog.close()


def test_ui26_werte_als_tabelle_haelt_die_wiedergabe_an(
    baue: Bauer, qtbot: QtBot, monkeypatch: pytest.MonkeyPatch
) -> None:
    a, _uhr = oeffne(baue, qtbot)
    m = Meldungen(a, monkeypatch)
    animation(a)
    a.animationsleiste.btn_abspielen.click()
    a.animationsleiste.btn_werte_tabelle.click()
    assert not a.animation.laeuft and len(m.dialoge) == 1


def test_beende_stoppt_timer_und_wiedergabe(baue: Bauer, qtbot: QtBot) -> None:
    a, _uhr = oeffne(baue, qtbot)
    animation(a)
    a.animationsleiste.btn_abspielen.click()
    assert a.animation._timer.isActive()
    a.beende()
    assert not a.animation.laeuft and not a.animation._timer.isActive()


# --- AF-Meldungen und Canvasgröße -------------------------------------------------------------


def test_meldung_langsam_in_af_aendert_die_canvasgroesse_nicht_und_haelt_nicht_an(
    baue: Bauer, qtbot: QtBot
) -> None:
    a, _uhr = oeffne(baue, qtbot)
    animation(a)
    a.animationsleiste.btn_abspielen.click()
    groesse = a.animation.canvas.size()
    a.animation.langsam_geaendert.emit(True)
    QApplication.processEvents()
    assert a.lbl_cursor.volltext() == f"{tokens.symbol('warnung')} {an.TEXT_LANGSAM}"
    assert a.animation.canvas.size() == groesse  # sonst hielte sich die Animation selbst an
    qtbot.wait(NEUZEICHNEN_MS + 100)  # ein Resize hätte den Neuzeichnen-Timer gestartet
    assert a.animation.laeuft and not a.animation._neuzeichnen_timer.isActive()
    a.animation.langsam_geaendert.emit(False)
    assert a.lbl_cursor.volltext() == "" and a.animation.canvas.size() == groesse
    a.animationsleiste.btn_abspielen.click()


def test_wiedergabe_aendert_die_canvasgroesse_nicht(baue: Bauer, qtbot: QtBot) -> None:
    """Winkelanzeige, Tempo und Abspielen/Pause haben feste Breite: kein Umbruch der Leiste."""
    a, uhr = oeffne(baue, qtbot)
    animation(a)
    ah = a.animationsleiste
    groesse, leiste = a.animation.canvas.size(), ah.size()
    QTest.mouseClick(ah.btn_abspielen, Qt.MouseButton.LeftButton)  # echter Klick: Fokus kommt dazu
    assert a.animation.laeuft
    for i in range(1, 40):  # Winkel von 0° bis 359,9° mit allen Stellenzahlen der Anzeige
        uhr.t = i * 0.1
        a.animation.takt()
        QApplication.processEvents()
        assert a.animation.canvas.size() == groesse and ah.size() == leiste, i
    ah.regler_tempo.setValue(-130)  # Beschriftung des Tempos wechselt: gleiche Breite
    ah.regler_tempo.setValue(30)
    assert a.animation.canvas.size() == groesse
    qtbot.wait(NEUZEICHNEN_MS + 100)
    assert a.animation.laeuft  # keine Größenänderung hat die Wiedergabe angehalten
    QTest.mouseClick(ah.btn_abspielen, Qt.MouseButton.LeftButton)  # Pause
    assert not a.animation.laeuft and a.animation.canvas.size() == groesse


def test_slot_von_phase_geaendert_bleibt_kurz_waehrend_der_wiedergabe(
    baue: Bauer, qtbot: QtBot, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Die Textalternative entsteht nicht je Bild (die Slot-Zeit geht ins Restintervall ein)."""
    a, uhr = oeffne(baue, qtbot)
    animation(a)
    aufrufe: list[int] = []
    original = an.animations_beschreibung

    def zaehlend(*args: Any, **kw: Any) -> str:
        aufrufe.append(1)
        return original(*args, **kw)

    monkeypatch.setattr("ldv_automation.gui.auswerten_reiter.animations_beschreibung", zaehlend)
    a.animationsleiste.btn_abspielen.click()
    for i in range(1, 6):
        uhr.t = i * 0.2
        a.animation.takt()
    assert aufrufe == []  # keine Berechnung der Beschreibung in der Wiedergabe
    a.animationsleiste.btn_abspielen.click()  # Pause: einmal die Beschreibung
    assert aufrufe == [1]


# --- UI-34 bis UI-36: Fokus, Tab, Kontrast, Layout --------------------------------------------


def tab_reihenfolge(a: AuswertenReiter) -> list[QWidget]:
    start: QWidget = a.btn_oeffnen
    reihe: list[QWidget] = [start]
    w: QWidget | None = start.nextInFocusChain()
    while w is not None and w is not start and len(reihe) < 500:
        reihe.append(w)
        w = w.nextInFocusChain()
    return reihe


def test_ui34_tab_reihenfolge_ad_ag_ae_ah_af_und_fokus_aller_elemente(
    baue: Bauer, qtbot: QtBot
) -> None:
    a, _uhr = oeffne(baue, qtbot)
    animation(a)
    kette = tab_reihenfolge(a)
    ah = a.animationsleiste
    pos = {w: i for i, w in enumerate(kette)}
    erste_ad = a.auswahl_sf.tab_kette()[0]
    assert pos[erste_ad] < pos[a.achsenleiste.tab_kette()[0]] < pos[a.plot.tab_kette()[0]]
    assert pos[a.plot.tab_kette()[0]] < pos[a.animation.canvas]  # AE
    ah_kette = ah.tab_kette()
    assert [pos[w] for w in ah_kette] == sorted(pos[w] for w in ah_kette)  # AH in Reihenfolge
    assert pos[a.animation.canvas] < pos[ah_kette[0]] and pos[ah_kette[-1]] < pos[a.lbl_pruefung]
    bedienbar: list[QWidget] = [
        *ah.findChildren(QAbstractButton),
        *ah.findChildren(QSlider),
        *ah.findChildren(QLineEdit),
    ]
    for w in bedienbar:
        assert w.focusPolicy() != Qt.FocusPolicy.NoFocus, w.objectName()
    sel = a.auswahl_sf
    assert pos[sel.rb_modus_standbild] < pos[sel.combo_bildrate]
    for w in (
        sel.feld_farbe_von,
        sel.feld_farbe_bis,
        sel.combo_bildrate,
        sel.rb_modus_animation,
    ):
        assert w.focusPolicy() != Qt.FocusPolicy.NoFocus, w.objectName()


def test_ui34_alle_neuen_elemente_haben_name_und_beschriftung(baue: Bauer, qtbot: QtBot) -> None:
    a, _uhr = oeffne(baue, qtbot)
    animation(a)
    ah = a.animationsleiste
    assert ah.accessibleName() and a.animation.canvas.accessibleName()
    for w in (*ah.tab_kette(), a.auswahl_sf.feld_farbe_von, a.auswahl_sf.combo_bildrate):
        assert w.accessibleName() or w.toolTip(), w.objectName()
    assert ah.btn_abspielen.accessibleName() == "Animation abspielen"
    assert "Leertaste" in ah.btn_abspielen.toolTip()
    assert "←" in ah.btn_schritt_zurueck.toolTip() and "→" in ah.btn_schritt_vor.toolTip()
    assert "θ = 0°" in ah.lbl_phase_grad.toolTip()  # Pflichtangabe zu θ = 0 (KONVENTIONEN)


def test_ui35_kontrastpaare_der_animation_stehen_in_den_tokens_und_im_stylesheet() -> None:
    namen = {n for n, _v, _h in tokens.KONTRAST_PAARE}
    assert {"text/bg", "text_gedaempft/aktiv_bg", "deaktiviert_text/bg"} <= namen
    linie = {n for n, _v, _h in tokens.KONTRAST_PAARE_LINIE}
    assert {"regler_rinne/bg", "regler_griff/bg", "akzent/fokus_bg"} <= linie
    for regel in ("QSlider::groove:horizontal", "QSlider:focus", '#btn_abspielen[laeuft="true"]'):
        assert regel in stil.QSS, regel
    for name, vorder, hinter in tokens.KONTRAST_PAARE_LINIE:
        if name in {"regler_rinne/bg", "regler_griff/bg", "akzent/fokus_bg"}:
            assert tokens.kontrastverhaeltnis(vorder, hinter) >= tokens.KONTRAST_MINDEST_LINIE


def rechtecke_der_leiste(a: AuswertenReiter) -> list[Any]:
    ah = a.animationsleiste
    gruppen = [g for g in ah.children() if isinstance(g, QWidget) and not g.isHidden()]
    return [g.geometry() for g in gruppen]


@pytest.mark.parametrize("groesse", [(1100, 680), (1366, 768)])
def test_ui36_layout_ohne_ueberlappung_und_ae_mit_ah_mindestens_600_x_320(
    baue: Bauer, qtbot: QtBot, groesse: tuple[int, int]
) -> None:
    a, _uhr = oeffne(baue, qtbot)
    w = a.window()
    w.resize(*groesse)
    animation(a)
    qtbot.wait(100)
    ah = a.animationsleiste
    assert a.animation.isVisible() and ah.isVisible() and a._an_gezeichnet
    # AH: nichts abgeschnitten, nichts übereinander, Höhe folgt der Breite (Umbruch)
    gruppen = [g for g in ah.children() if isinstance(g, QWidget) and g.isVisibleTo(ah)]
    assert len(gruppen) == 7  # Wiedergabe, Schrittweite, Phase, Tabelle, Tempo, Überhöhung, Blick
    for i, g1 in enumerate(gruppen):
        assert ah.rect().contains(g1.geometry()), (groesse, g1.objectName())
        for g2 in gruppen[i + 1 :]:
            assert not g1.geometry().intersects(g2.geometry()), (g1.objectName(), g2.objectName())
    layout = ah.layout()
    assert layout is not None and ah.height() >= layout.heightForWidth(ah.width()) - 1
    # AE einschließlich AH, kein Element überlagert den Canvas
    ae = a.findChild(QWidget, "darstellung")
    assert ae is not None and ae.width() >= 600 and ae.height() >= 320
    assert a.animation.geometry().bottom() < ah.geometry().top()
    assert a.animation.canvas.width() >= 600 and a.animation.canvas.height() >= 250
    assert ah.width() <= a._plot_spalte.width()  # kein Bildlauf nach rechts


def test_ui36_ah_bricht_bei_schmalem_fenster_um_und_kuerzt_die_beschriftung(
    baue: Bauer, qtbot: QtBot
) -> None:
    a, _uhr = oeffne(baue, qtbot)
    animation(a)
    ah = a.animationsleiste
    a.window().resize(1366, 768)
    qtbot.wait(100)
    breit = ah.height()
    assert ah.btn_schritt_vor.text() == "Schritt vor" and a.window().width() >= 1200
    a.window().resize(1100, 680)  # unter 1200 px: kompakte Darstellung
    qtbot.wait(100)
    assert ah.btn_schritt_vor.text() == "Vor" and ah.btn_schritt_zurueck.text() == "Zurück"
    assert ah.btn_ansicht_zurueck.text() == "Zurücksetzen"
    assert ah.lbl_tempo.text() == "0,25/s" and ah.lbl_tempo.toolTip() == "Perioden je Sekunde"
    assert ah.height() >= breit  # schmaler: mindestens so viele Zeilen wie zuvor
    assert ah.btn_ansicht_zurueck.toolTip()  # volle Bedeutung bleibt im Tooltip
    assert a.animation.canvas.height() > 0 and a._an_gezeichnet


def test_ui34_modus_umschalten_per_tastatur_im_radiogruppen_halt(baue: Bauer, qtbot: QtBot) -> None:
    a, _uhr = oeffne(baue, qtbot)
    sel = a.auswahl_sf
    assert sel.rb_modus_standbild.focusPolicy() == Qt.FocusPolicy.StrongFocus  # Tab-Halt: gewählt
    animation(a)
    assert sel.rb_modus_animation.focusPolicy() == Qt.FocusPolicy.StrongFocus
    assert sel.rb_modus_standbild.focusPolicy() == Qt.FocusPolicy.ClickFocus


# --- Tasten -----------------------------------------------------------------------------------


def test_tasten_drehen_in_der_flaeche_und_pos1_setzt_nur_den_blick_zurueck(
    baue: Bauer, qtbot: QtBot
) -> None:
    a, _uhr = oeffne(baue, qtbot)
    animation(a)
    f = a.animation
    f.canvas.setFocus()
    a.animationsleiste.regler_phase.setValue(900)
    f.canvas.setFocus()
    QTest.keyClick(f.canvas, Qt.Key.Key_Down)  # ↓: Elevation minus 5° (Aufsicht 90° → 85°)
    assert f.blick.elev_grad == pytest.approx(BLICK_VORGABEN["xy"].elev_grad - DREH_SCHRITT_GRAD)
    QTest.keyClick(f.canvas, Qt.Key.Key_Home)  # Pos1: Blick zurück, nicht Winkel und Überhöhung
    assert f.blick == BLICK_VORGABEN[a.auswahl_sf.ebene()]
    assert f.uhr.theta_grad == pytest.approx(90.0, abs=ATOL_GRAD)


def test_tasten_im_phasenregler_gelten_wie_in_der_flaeche(baue: Bauer, qtbot: QtBot) -> None:
    """Mit Fokus im Phasenregler wirken ↓, Umschalt+→ und Pos1 wie in der Fläche."""
    a, _uhr = oeffne(baue, qtbot)
    animation(a)
    f, ah = a.animation, a.animationsleiste
    regler = ah.regler_phase
    regler.setFocus()
    wert = regler.value()
    theta = f.uhr.theta_grad
    start = f.blick
    QTest.keyClick(regler, Qt.Key.Key_Down)  # ↓: Elevation minus (Aufsicht 90° → 85°)
    assert f.blick.elev_grad == pytest.approx(start.elev_grad - DREH_SCHRITT_GRAD)
    assert regler.value() == wert and f.uhr.theta_grad == theta
    QTest.keyClick(regler, Qt.Key.Key_Right, Qt.KeyboardModifier.ShiftModifier)  # Azimut
    assert f.blick.azim_grad == pytest.approx(start.azim_grad + DREH_SCHRITT_GRAD)
    assert regler.value() == wert and f.uhr.theta_grad == theta
    QTest.keyClick(regler, Qt.Key.Key_Home)  # Pos1: Blick zurück, nicht θ = 0
    assert f.blick == BLICK_VORGABEN[a.auswahl_sf.ebene()]
    assert regler.value() == wert and f.uhr.theta_grad == theta


@pytest.mark.parametrize("regler_name", ["regler_tempo", "regler_ueberhoehung"])
def test_tempo_und_ueberhoehungsregler_behalten_ihre_pfeiltasten(
    baue: Bauer, qtbot: QtBot, regler_name: str
) -> None:
    a, _uhr = oeffne(baue, qtbot)
    animation(a)
    f, ah = a.animation, a.animationsleiste
    regler: QSlider = getattr(ah, regler_name)
    regler.setValue(regler.minimum() + 5)
    regler.setFocus()
    wert, blick = regler.value(), f.blick
    QTest.keyClick(regler, Qt.Key.Key_Right)  # feine Verstellung des Reglers
    assert regler.value() == wert + regler.singleStep()
    QTest.keyClick(regler, Qt.Key.Key_Down)
    assert f.blick == blick  # keine Elevation
    QTest.keyClick(regler, Qt.Key.Key_Home)  # Pos1 wirkt wie in der Fläche
    assert f.blick == BLICK_VORGABEN[a.auswahl_sf.ebene()]


def test_pos1_im_phasenregler_laesst_theta_stehen(baue: Bauer, qtbot: QtBot) -> None:
    a, _uhr = oeffne(baue, qtbot)
    animation(a)
    ah = a.animationsleiste
    ah.regler_phase.setValue(900)
    ah.regler_phase.setFocus()
    QTest.keyClick(ah.regler_phase, Qt.Key.Key_Home)
    assert a.animation.uhr.theta_grad == pytest.approx(90.0, abs=ATOL_GRAD)
    assert ah.regler_phase.value() == 900


def test_tasten_in_ah_decken_alle_belegten_animationstasten_ab(baue: Bauer, qtbot: QtBot) -> None:
    """Jede Taste aus ``ANIMATIONS_TASTEN`` erreicht aus einem Regler dieselbe Aktion."""
    a, _uhr = oeffne(baue, qtbot)
    animation(a)
    ah = a.animationsleiste
    erhalten: list[Aktion] = []
    ah.aktion_gewaehlt.connect(erhalten.append)
    ah.abspielen_geklickt.connect(lambda: erhalten.append(Aktion.ABSPIELEN))
    ah.regler_phase.setFocus()
    for aktion, (folge, _anzeige) in ANIMATIONS_TASTEN.items():
        kombi: Any = QKeySequence(folge)[0]  # type: ignore[index]  # QKeyCombination
        QTest.keyClick(ah.regler_phase, kombi.key(), kombi.keyboardModifiers())
        assert erhalten[-1] is aktion, folge
    assert len(erhalten) == len(ANIMATIONS_TASTEN)


def test_ui28_kopf_mit_beiden_kennzeichen_wird_nicht_abgeschnitten(
    baue: Bauer, qtbot: QtBot
) -> None:
    """Bei 1100 px bricht der Kopf um: M8 und M12 bleiben lesbar (dauerhaft sichtbar)."""
    a, _uhr = oeffne(baue, qtbot)
    a.window().resize(1100, 680)
    animation(a)
    a.auswahl_sf.rb_bezug_absolut.click()
    qtbot.wait(50)
    kopf = a.lbl_plotkopf
    assert "M8" in kopf.text() and "M12" in kopf.text() and kopf.wordWrap()
    assert kopf.height() >= kopf.heightForWidth(kopf.width())  # ganze Höhe: nichts abgeschnitten
    a.auswahl_sf.rb_modus_standbild.click()
    assert not kopf.wordWrap()  # die übrigen Kopfzeilen bleiben unverändert


# --- Korrektur K-AUSW3-7: UI-A5 bis UI-A7 -----------------------------------------------------


def test_ui_a5_tempo_regler_hat_etikett_und_gruppen_haben_abstand(
    baue: Bauer, qtbot: QtBot
) -> None:
    a, _uhr = oeffne(baue, qtbot)
    a.window().resize(1366, 768)
    animation(a)
    qtbot.wait(100)
    ah = a.animationsleiste
    assert ah.lbl_tempo_titel.text() == "Tempo" and ah.lbl_tempo_titel.buddy() is ah.regler_tempo
    assert ah.lbl_tempo.text() == "0,25 Perioden/s"  # Wert unverändert
    gruppen = [g for g in ah.children() if isinstance(g, QWidget) and g.isVisibleTo(ah)]
    nebeneinander = 0
    for links, rechts in itertools.pairwise(gruppen):
        if links.geometry().top() == rechts.geometry().top():  # gleiche Zeile
            nebeneinander += 1
            luecke = rechts.geometry().left() - links.geometry().right() - 1
            assert luecke >= 24, (links.objectName(), rechts.objectName(), luecke)
            assert luecke > 6  # größer als der Abstand innerhalb einer Gruppe (Etikett–Regler)
    assert nebeneinander >= 3


@pytest.mark.parametrize("groesse", [(1100, 680), (1366, 768)])
def test_ui_a7_blickknoepfe_sind_ohne_scrollen_sichtbar_und_wirken(
    baue: Bauer, qtbot: QtBot, groesse: tuple[int, int]
) -> None:
    a, _uhr = oeffne(baue, qtbot)
    w = a.window()
    w.resize(*groesse)
    animation(a)
    qtbot.wait(100)
    ah = a.animationsleiste
    fenster = w.rect()
    assert set(ah.btn_blick) == {"xy", "xz", "yz", "iso"}
    for name, knopf in [*ah.btn_blick.items(), ("zurueck", ah.btn_ansicht_zurueck)]:
        assert knopf.isVisible(), name
        ecke = knopf.mapTo(w, QPoint(0, 0))
        assert fenster.contains(ecke) and fenster.contains(
            ecke + QPoint(knopf.width(), knopf.height())
        ), name
    # sie liegen unter der Fläche, nicht in der scrollbaren Auswahlspalte AD
    assert not a.auswahl_sf.isAncestorOf(ah.btn_blick["xy"])
    assert not hasattr(a.auswahl_sf, "btn_blick")
    ah.btn_blick["xz"].click()
    assert a.animation.blick == BLICK_VORGABEN["xz"]


def test_ui_a6_unter_1200_px_stehen_im_kopf_nur_m8_und_m12_mit_langtext_im_tooltip(
    baue: Bauer, qtbot: QtBot
) -> None:
    a, _uhr = oeffne(baue, qtbot)
    w = a.window()
    w.resize(1366, 768)
    animation(a)
    a.auswahl_sf.rb_bezug_absolut.click()
    qtbot.wait(100)
    kopf = a.lbl_plotkopf
    assert KENNZEICHEN_M12 in kopf.text() and KENNZEICHEN_M8 in kopf.text()  # breit: voll
    w.resize(1100, 680)  # kompakt
    qtbot.wait(100)
    zeichen = tokens.symbol("warnung")
    assert f"{zeichen} M8" in kopf.text() and f"{zeichen} M12" in kopf.text()
    assert KENNZEICHEN_M12 not in kopf.text() and KENNZEICHEN_M8 not in kopf.text()
    assert KENNZEICHEN_M12 in kopf.toolTip() and KENNZEICHEN_M8 in kopf.toolTip()
    # ausführliche Fassung bleibt im Kasten des Bildes
    assert any(KENNZEICHEN_M12 in t for t in a.animation.zeichnung.alle_texte())  # type: ignore[union-attr]
    w.resize(1366, 768)  # wieder breit: voller Text
    qtbot.wait(100)
    assert KENNZEICHEN_M12 in kopf.text()


def test_ui_a6_tooltip_des_kopfes_verschwindet_mit_der_animation(baue: Bauer, qtbot: QtBot) -> None:
    a, _uhr = oeffne(baue, qtbot)
    animation(a)
    assert a.lbl_plotkopf.toolTip()
    a.auswahl_sf.rb_modus_standbild.click()
    assert a.lbl_plotkopf.toolTip() == ""


def test_ueberhoehungsregler_misst_den_zoom_nur_beim_loslassen(
    baue: Bauer, qtbot: QtBot, monkeypatch: pytest.MonkeyPatch
) -> None:
    from ldv_automation.darstellung import animation3d

    a, _uhr = oeffne(baue, qtbot)
    animation(a)
    aufrufe: list[int] = []
    original = animation3d._passe_zoom_an

    def zaehler(*args: Any, **kwargs: Any) -> None:
        aufrufe.append(1)
        original(*args, **kwargs)

    monkeypatch.setattr(animation3d, "_passe_zoom_an", zaehler)
    regler = a.animationsleiste.regler_ueberhoehung
    regler.setSliderDown(True)  # Ziehen beginnt
    for wert in (20, 40, 60, 80):
        regler.setValue(wert)
    assert aufrufe == []
    regler.setSliderDown(False)  # Loslassen
    assert len(aufrufe) == 1
    regler.setValue(-20)  # Tasten oder Rad: kein Ziehen, volle Messung je Schritt
    assert len(aufrufe) == 2


def test_ui_d3_ah_bleibt_bei_1100_x_680_zweizeilig(baue: Bauer, qtbot: QtBot) -> None:
    """UI-D3: im kompakten Modus brechen die Gruppen von AH in höchstens zwei Zeilen um."""
    a, _uhr = oeffne(baue, qtbot)
    a.window().resize(1100, 680)
    animation(a)
    qtbot.wait(100)
    ah = a.animationsleiste
    gruppen = [g for g in ah.children() if isinstance(g, QWidget) and g.isVisibleTo(ah)]
    zeilen = {g.geometry().y() for g in gruppen}
    assert len(zeilen) == 2, sorted(zeilen)
    assert ah.btn_werte_tabelle.isVisible() and ah.btn_ansicht_zurueck.isVisible()
    assert ah.height() <= 2 * 36 + 8
    ae = a.findChild(QWidget, "darstellung")
    assert ae is not None and ae.width() >= 600 and ae.height() >= 320
    assert a.animation.canvas.height() >= 300  # die eingesparte Zeile kommt dem Bild zugute
    # ausgeschrieben, wenn Platz ist
    a.window().resize(1366, 768)
    qtbot.wait(100)
    assert ah.btn_ansicht_zurueck.text() == "Ansicht zurücksetzen"
    assert ah.lbl_tempo.text() == "0,25 Perioden/s"


def test_k2_nach_mausziehen_und_loslassen_gilt_der_grundzoom_des_neuen_blicks(
    baue: Bauer, qtbot: QtBot
) -> None:
    """K2 MAJOR: Die Box wird nach dem Loslassen neu eingepasst (wie ein frisches Zeichnen)."""
    a, _uhr = oeffne(baue, qtbot)
    animation(a)
    canvas = a.animation.canvas
    start = QPoint(canvas.width() // 2, canvas.height() // 2)
    QTest.mousePress(canvas, Qt.MouseButton.LeftButton, Qt.KeyboardModifier.NoModifier, start)
    for dx, dy in ((30, -20), (60, -50), (90, -90)):
        QTest.mouseMove(canvas, start + QPoint(dx, dy))
    QTest.mouseRelease(
        canvas, Qt.MouseButton.LeftButton, Qt.KeyboardModifier.NoModifier, start + QPoint(90, -90)
    )
    QApplication.processEvents()
    z = a.animation.zeichnung
    assert z is not None and a.animation.blick != BLICK_VORGABEN["xy"]
    nachher = z.hilfsobjekte["grund_zoom"]
    frisch = a.animation.zeichne(daten(a), a.animation._basis)
    assert nachher == pytest.approx(frisch.hilfsobjekte["grund_zoom"])
