"""Achsenwahl in der Oberfläche (R-073, P-AUSW2 S2/S3; UI-1 bis UI-8); offscreen, Marker ``gui``.

S2: eine Quelle der Grenzen (``AchsenZustand``), Rückkopplung der Werkzeugleiste. Daten:
``gui_ausw_hilfen.synth_geladen`` (4 Punkte, 64 Linien, 0,5 … 32 Hz).
"""

from __future__ import annotations

import itertools
from dataclasses import replace
from pathlib import Path
from typing import Any

import pytest
from gui_ausw_hilfen import PFAD, Bauer, synth_geladen
from matplotlib.backend_bases import MouseButton, MouseEvent
from PySide6.QtCore import QEvent, Qt
from PySide6.QtGui import QFocusEvent
from PySide6.QtTest import QTest
from PySide6.QtWidgets import (
    QAbstractButton,
    QApplication,
    QLineEdit,
    QStyle,
    QStyleOptionFrame,
    QWidget,
)
from pytestqt.qtbot import QtBot
from test_gui_auswerten_ansichten import geladen_mit

from ldv_automation.darstellung.achsen import (
    TEXT_KEINE_ZAHL,
    TEXT_LOG_NUR_POSITIV,
    TEXT_REIHENFOLGE,
    Bereich,
    feld_text,
)
from ldv_automation.darstellung.bild import baue_stempel
from ldv_automation.gui import tokens
from ldv_automation.gui.auswerten_reiter import AuswertenReiter

pytestmark = pytest.mark.gui

RTOL = 1e-9  # Eingabe → float → set_xlim: nur Rundung von Dezimaltext


def achse(a: AuswertenReiter, index: int = 0) -> Any:
    assert a.plot.zeichnung is not None
    return a.plot.zeichnung.achsen[index]


def zaehle_zeichnen(a: AuswertenReiter, monkeypatch: pytest.MonkeyPatch) -> list[int]:
    """Zählt die Aufrufe von ``PlotFlaeche.zeichne`` (UI-37)."""
    zaehler = [0]
    original = a.plot.zeichne

    def zeichne(*args: Any, **kw: Any) -> Any:
        zaehler[0] += 1
        return original(*args, **kw)

    monkeypatch.setattr(a.plot, "zeichne", zeichne)
    return zaehler


def maus(
    a: AuswertenReiter, name: str, ax_x: float, ax_y: float, button: MouseButton
) -> MouseEvent:
    """Mausereignis in Achsenanteilen (0 … 1) der ersten Achse."""
    box = achse(a).bbox
    canvas = a.plot.canvas
    return MouseEvent(
        name,
        canvas,
        box.x0 + ax_x * box.width,
        box.y0 + ax_y * box.height,
        button=button,
        buttons={button} if name == "motion_notify_event" else None,
    )


def ziehe_zoom(a: AuswertenReiter) -> None:
    """Rechteckzoom der Werkzeugleiste von (0,2 / 0,2) nach (0,6 / 0,7) der Achse."""
    tb = a.plot.toolbar
    tb.zoom()  # type: ignore[no-untyped-call]
    tb.press_zoom(maus(a, "button_press_event", 0.2, 0.2, MouseButton.LEFT))
    tb.drag_zoom(maus(a, "motion_notify_event", 0.6, 0.7, MouseButton.LEFT))
    tb.release_zoom(maus(a, "button_release_event", 0.6, 0.7, MouseButton.LEFT))
    tb.zoom()  # type: ignore[no-untyped-call]  # Werkzeug wieder aus


def ziehe_pan(a: AuswertenReiter) -> None:
    tb = a.plot.toolbar
    tb.pan()  # type: ignore[no-untyped-call]
    tb.press_pan(maus(a, "button_press_event", 0.2, 0.2, MouseButton.LEFT))
    tb.drag_pan(maus(a, "motion_notify_event", 0.4, 0.3, MouseButton.LEFT))
    tb.release_pan(maus(a, "button_release_event", 0.4, 0.3, MouseButton.LEFT))
    tb.pan()  # type: ignore[no-untyped-call]


# --- UI-3: eine Quelle, Wechsel ändern die Grenzen nicht --------------------------------------


def test_ui3_wechsel_von_punkt_komponente_groesse_aendern_grenzen_und_skala_nicht(
    baue: Bauer, qtbot: QtBot
) -> None:
    a = geladen_mit(baue, qtbot)
    z = a.plot.achsen_zustand
    z.setze_bereich(1, "frequenz", Bereich(5.0, 12.5))
    z.setze_bereich(1, "betrag", Bereich(1e-5, 3.0))
    z.setze_skala(1, "frequenz", "log")
    a._zeichne()
    soll = (achse(a).get_xlim(), achse(a).get_ylim(), achse(a).get_xscale(), achse(a).get_yscale())
    assert soll[0] == pytest.approx((5.0, 12.5), rel=RTOL)
    assert soll[1] == pytest.approx((1e-5, 3.0), rel=RTOL)
    assert soll[2:] == ("log", "log")
    aenderungen = [
        lambda: a.liste_punkte.setCurrentRow(2),  # Punkt
        lambda: a.liste_punkte.setCurrentRow(0),  # Mittel
        lambda: a.chk["X"].setChecked(False),  # Komponente
        lambda: a.rb_groesse_ap.setChecked(True),  # Größe
    ]
    for aendern in aenderungen:
        aendern()  # type: ignore[no-untyped-call]
        ax = achse(a)
        assert ax.get_xlim() == pytest.approx(soll[0], rel=RTOL)
        assert ax.get_ylim() == pytest.approx(soll[1], rel=RTOL)
        assert (ax.get_xscale(), ax.get_yscale()) == soll[2:]


def test_zustand_je_ansicht_bleibt_beim_ansichtswechsel_erhalten(baue: Bauer, qtbot: QtBot) -> None:
    a = geladen_mit(baue, qtbot)
    a.plot.achsen_zustand.setze_bereich(1, "frequenz", Bereich(5.0, 10.0))
    a._zeichne()
    a.btn_ansicht[2].click()
    assert achse(a).get_xlim() == pytest.approx((0.5, 32.0))  # Ansicht 2: eigener Zustand
    a.btn_ansicht[3].click()
    assert achse(a).get_xlim() == pytest.approx((0.5, 32.0))
    a.btn_ansicht[1].click()
    assert achse(a).get_xlim() == pytest.approx((5.0, 10.0), rel=RTOL)  # kommt zurück


def test_ansicht_3_oberflaeche_ylim_ist_genau_die_eingabe(baue: Bauer, qtbot: QtBot) -> None:
    a = geladen_mit(baue, qtbot)
    a.btn_ansicht[3].click()
    a.plot.achsen_zustand.setze_bereich(3, "betrag", Bereich(1e-3, 2.0))
    a._zeichne()
    assert achse(a).get_ylim() == pytest.approx((1e-3, 2.0), rel=RTOL)  # kein Streifen


# --- UI-4: Werkzeugleiste → Zustand -----------------------------------------------------------


def test_ui4_zoom_schreibt_feste_werte_ohne_neuzeichnen(
    baue: Bauer, qtbot: QtBot, monkeypatch: pytest.MonkeyPatch
) -> None:
    a = geladen_mit(baue, qtbot)
    gemeldet: list[int] = []
    a.plot.achsen_geaendert.connect(lambda: gemeldet.append(1))
    gezeichnet = zaehle_zeichnen(a, monkeypatch)
    ziehe_zoom(a)
    ax = achse(a)
    z = a.plot.achsen_zustand
    assert ax.get_xlim() != pytest.approx((0.5, 32.0))  # der Zoom hat gewirkt
    assert z.bereich(1, "frequenz") == Bereich(*ax.get_xlim())  # Zoom → fest
    assert z.bereich(1, "betrag") == Bereich(*ax.get_ylim())
    assert gemeldet == [1]  # genau eine Meldung (Spike S1)
    assert gezeichnet == [0]  # Zoom zeichnet nicht neu


def test_ui4_zoom_bleibt_beim_auswahlwechsel_und_wird_gezeichnet(baue: Bauer, qtbot: QtBot) -> None:
    a = geladen_mit(baue, qtbot)
    ziehe_zoom(a)
    gezoomt = (achse(a).get_xlim(), achse(a).get_ylim())
    a.liste_punkte.setCurrentRow(2)
    assert achse(a).get_xlim() == pytest.approx(gezoomt[0], rel=RTOL)
    assert achse(a).get_ylim() == pytest.approx(gezoomt[1], rel=RTOL)


def test_ui4_verschieben_schreibt_feste_werte(baue: Bauer, qtbot: QtBot) -> None:
    a = geladen_mit(baue, qtbot)
    gemeldet: list[int] = []
    a.plot.achsen_geaendert.connect(lambda: gemeldet.append(1))
    ziehe_pan(a)
    ax = achse(a)
    assert ax.get_xlim() != pytest.approx((0.5, 32.0))
    assert a.plot.achsen_zustand.bereich(1, "frequenz") == Bereich(*ax.get_xlim())
    assert gemeldet == [1]


def test_ui4_zurueck_und_vor_schreiben_die_gezeigten_grenzen(baue: Bauer, qtbot: QtBot) -> None:
    a = geladen_mit(baue, qtbot)
    standard = achse(a).get_xlim()
    ziehe_zoom(a)
    gezoomt = achse(a).get_xlim()
    gemeldet: list[int] = []
    a.plot.achsen_geaendert.connect(lambda: gemeldet.append(1))
    a.plot.toolbar.back()
    assert achse(a).get_xlim() == pytest.approx(standard)
    assert a.plot.achsen_zustand.bereich(1, "frequenz") == Bereich(*achse(a).get_xlim())
    a.plot.toolbar.forward()
    assert a.plot.achsen_zustand.bereich(1, "frequenz") == Bereich(*gezoomt)
    assert gemeldet == [1, 1]


def test_ui4_zuruecksetzen_heisst_auto_und_zeichnet_genau_einmal_neu(
    baue: Bauer, qtbot: QtBot, monkeypatch: pytest.MonkeyPatch
) -> None:
    a = geladen_mit(baue, qtbot)
    ziehe_zoom(a)
    a.plot.achsen_zustand.setze_skala(1, "frequenz", "log")
    gemeldet: list[int] = []
    a.plot.achsen_geaendert.connect(lambda: gemeldet.append(1))
    gezeichnet = zaehle_zeichnen(a, monkeypatch)
    a.plot.toolbar.knoepfe()[0].click()  # „Zurücksetzen“ (Pos1)
    z = a.plot.achsen_zustand
    assert not z.hat_feste(1) and z.skala(1, "frequenz") == "log"  # Auto, Skala bleibt
    assert achse(a).get_xlim() == pytest.approx((0.5, 32.0))
    assert gezeichnet == [1] and gemeldet == [1]


def test_zuruecksetzen_in_ansicht_4_geht_auf_den_verlauf(baue: Bauer, qtbot: QtBot) -> None:
    a = geladen_mit(baue, qtbot)
    a.btn_ansicht[4].click()
    ax = achse(a)
    standard = ax.get_xlim()
    ax.set_xlim(standard[0] + 0.01, standard[1] - 0.01)
    a.plot.toolbar.push_current()
    a.plot.zoom_zuruecksetzen()
    assert ax.get_xlim() == pytest.approx(standard)  # Verlauf der Werkzeugleiste (keine Achsenwahl)
    assert not any(a.plot.achsen_zustand.hat_feste(nr) for nr in (1, 2, 3))


def test_direkte_aenderung_der_achsen_uebersteht_das_neuzeichnen(baue: Bauer, qtbot: QtBot) -> None:
    a = geladen_mit(baue, qtbot)
    achse(a).set_xlim(5.0, 10.0)  # ohne Werkzeugleiste
    a.liste_punkte.setCurrentRow(1)
    assert achse(a).get_xlim() == pytest.approx((5.0, 10.0))


def test_ansicht_2_zoom_schreibt_nur_geaenderte_achsen(baue: Bauer, qtbot: QtBot) -> None:
    a = geladen_mit(baue, qtbot)
    a.btn_ansicht[2].click()
    a.auswahl_frf.chk_phase.setChecked(True)
    a.liste_punkte.setCurrentRow(1)
    assert a.plot.zeichnung is not None and a.plot.zeichnung.rollen == (
        "betrag",
        "phase",
        "kohaerenz",
    )
    ziehe_zoom(a)  # Zoom im Betrags-Teilbild: x und Betrag, nicht die Phase
    z = a.plot.achsen_zustand
    assert z.bereich(2, "frequenz") == Bereich(*achse(a, 0).get_xlim())
    assert z.bereich(2, "betrag") == Bereich(*achse(a, 0).get_ylim())
    assert z.bereich(2, "phase").ist_auto


# --- UI-6: neue Datei, Arbeitsbild ------------------------------------------------------------


def test_ui6_neue_datei_setzt_bereiche_zurueck_skalen_bleiben(baue: Bauer, qtbot: QtBot) -> None:
    from test_gui_auswerten import lade

    a = geladen_mit(baue, qtbot)
    z = a.plot.achsen_zustand
    z.setze_bereich(1, "frequenz", Bereich(5.0, 10.0))
    z.setze_bereich(2, "betrag", Bereich(1e-3, 1.0))
    z.setze_skala(1, "frequenz", "log")
    z.setze_skala(1, "betrag", "linear")
    a._zeichne()
    assert achse(a).get_xlim() == pytest.approx((5.0, 10.0), rel=RTOL)
    lade(qtbot, a.window(), "C:\\messungen\\zweite.svd")  # type: ignore[arg-type]
    assert not any(z.hat_feste(nr) for nr in (1, 2, 3))
    assert z.skala(1, "frequenz") == "log" and z.skala(1, "betrag") == "linear"
    assert achse(a).get_xlim() == pytest.approx((0.5, 32.0))
    assert achse(a).get_xscale() == "log"


def test_arbeitsbild_uebernimmt_feste_grenzen_und_skalen(
    baue: Bauer, qtbot: QtBot, tmp_path: Path
) -> None:
    a = geladen_mit(baue, qtbot)
    a.plot.achsen_zustand.setze_bereich(1, "frequenz", Bereich(5.0, 12.5))
    a.plot.achsen_zustand.setze_bereich(1, "betrag", Bereich(1e-5, 3.0))
    a._zeichne()
    stempel = baue_stempel(dateiname="x.svd", ansicht="Ansicht 1", git_hash="abc")
    kopie = a.plot.speichere(tmp_path / "b.png", stempel)
    assert kopie.achsen[0].get_xlim() == pytest.approx((5.0, 12.5), rel=RTOL)
    assert kopie.achsen[0].get_ylim() == pytest.approx((1e-5, 3.0), rel=RTOL)
    assert kopie.figure is not a.plot.figure


def test_arbeitsbild_ansicht_3_ergaenzt_den_streifen_ueber_der_eingabe(
    baue: Bauer, qtbot: QtBot, tmp_path: Path
) -> None:
    a = geladen_mit(baue, qtbot)
    a.btn_ansicht[3].click()
    a.plot.achsen_zustand.setze_bereich(3, "betrag", Bereich(1e-3, 2.0))
    a._zeichne()
    stempel = baue_stempel(dateiname="x.svd", ansicht="Ansicht 3", git_hash="abc")
    kopie = a.plot.speichere(tmp_path / "c.png", stempel)
    unten, oben = kopie.achsen[0].get_ylim()
    assert unten == pytest.approx(1e-3, rel=RTOL) and oben > 2.0
    assert achse(a).get_ylim()[1] == pytest.approx(2.0, rel=RTOL)  # Oberfläche: genau die Eingabe


def test_ungueltiger_zustand_wird_gemeldet_nicht_gezeichnet(baue: Bauer, qtbot: QtBot) -> None:
    a = geladen_mit(baue, qtbot)
    a.plot.achsen_zustand.setze_bereich(1, "frequenz", Bereich(10.0, 5.0))  # Absicherung
    a._zeichne()
    assert "Unterer Wert muss kleiner sein als der obere." in a.lbl_cursor.text()
    assert a.band_fehler.isHidden()  # kein unerwarteter Fehler
    QApplication.processEvents()


# --- S3: Achsenleiste AG -------------------------------------------------------------------------


def feld(a: AuswertenReiter, rolle: str, seite: str) -> QLineEdit:
    return a.achsenleiste.gruppe(rolle).feld(seite)


def eingabe(a: AuswertenReiter, rolle: str, seite: str, text: str, *, enter: bool = True) -> None:
    """Tippt ``text`` ins Feld (Taste für Taste) und bestätigt mit Enter."""
    ed = feld(a, rolle, seite)
    ed.selectAll()
    ed.del_()
    QTest.keyClicks(ed, text)
    if enter:
        QTest.keyClick(ed, Qt.Key.Key_Return)


def fokus_verlassen(ed: QLineEdit) -> None:
    QApplication.sendEvent(ed, QFocusEvent(QEvent.Type.FocusOut, Qt.FocusReason.TabFocusReason))


def meldung(a: AuswertenReiter, rolle: str) -> str:
    g = a.achsenleiste.gruppe(rolle)
    return g.lbl_meldung.text() if not g.lbl_meldung.isHidden() else ""


def test_ui1_felder_je_sichtbarer_achse_und_objektnamen(baue: Bauer, qtbot: QtBot) -> None:
    a = geladen_mit(baue, qtbot)
    a.window().show()
    namen = {
        "achse_f_von",
        "achse_f_bis",
        "achse_f_skala",
        "achse_y_von",
        "achse_y_bis",
        "achse_y_skala",
        "achse_phase_von",
        "achse_phase_bis",
        "btn_achsen_auto",
        "achsenleiste",
    }
    for name in namen:
        assert a.findChild(QWidget, name) is not None, name
    leiste = a.achsenleiste
    sichtbar = {r: leiste.gruppe(r).isVisibleTo(leiste) for r in ("frequenz", "betrag", "phase")}
    assert sichtbar == {"frequenz": True, "betrag": True, "phase": False}  # Ansicht 1
    a.btn_ansicht[2].click()
    a.liste_punkte.setCurrentRow(1)
    assert not leiste.gruppe("phase").isVisibleTo(leiste)  # ohne „Phase anzeigen“ keine Phase
    a.auswahl_frf.chk_phase.setChecked(True)
    assert leiste.gruppe("phase").isVisibleTo(leiste)  # Ansicht 2 mit Phase
    a.btn_ansicht[3].click()
    assert not leiste.gruppe("phase").isVisibleTo(leiste) and leiste.isVisibleTo(a)
    a.btn_ansicht[4].click()
    assert not leiste.isVisibleTo(a)  # Ansicht 4: keine Achsenleiste


def test_ui1_eingabe_und_enter_setzt_die_grenzen_in_den_ansichten_1_2_3(
    baue: Bauer, qtbot: QtBot
) -> None:
    a = geladen_mit(baue, qtbot)
    eingabe(a, "frequenz", "von", "5,5")
    eingabe(a, "frequenz", "bis", "12")
    eingabe(a, "betrag", "von", "1e-6")
    eingabe(a, "betrag", "bis", "2,5")
    assert achse(a).get_xlim() == pytest.approx((5.5, 12.0), rel=RTOL)
    assert achse(a).get_ylim() == pytest.approx((1e-6, 2.5), rel=RTOL)
    a.btn_ansicht[2].click()
    a.auswahl_frf.chk_phase.setChecked(True)
    a.liste_punkte.setCurrentRow(1)
    eingabe(a, "frequenz", "von", "4")
    eingabe(a, "frequenz", "bis", "20,5")
    eingabe(a, "betrag", "von", "0,001")
    eingabe(a, "betrag", "bis", "3")
    eingabe(a, "phase", "von", "-90")
    eingabe(a, "phase", "bis", "45,5")
    betrag, phase, _koh = a.plot.zeichnung.achsen  # type: ignore[union-attr]
    assert betrag.get_xlim() == pytest.approx((4.0, 20.5), rel=RTOL)
    assert betrag.get_ylim() == pytest.approx((1e-3, 3.0), rel=RTOL)
    assert phase.get_ylim() == pytest.approx((-90.0, 45.5), rel=RTOL)  # Grad
    a.btn_ansicht[3].click()
    eingabe(a, "frequenz", "von", "6")
    eingabe(a, "betrag", "bis", "5")
    eingabe(a, "betrag", "von", "0,0005")
    assert achse(a).get_xlim()[0] == pytest.approx(6.0, rel=RTOL)
    assert achse(a).get_ylim() == pytest.approx((5e-4, 5.0), rel=RTOL)
    a.btn_ansicht[1].click()  # Ansicht 1 behält ihren Zustand
    assert achse(a).get_xlim() == pytest.approx((5.5, 12.0), rel=RTOL)


def test_ui2_umschalter_aendern_die_skalen_voreinstellung_betrag_log_frequenz_linear(
    baue: Bauer, qtbot: QtBot
) -> None:
    a = geladen_mit(baue, qtbot)
    assert (achse(a).get_xscale(), achse(a).get_yscale()) == ("linear", "log")
    g_f, g_y = a.achsenleiste.gruppe("frequenz"), a.achsenleiste.gruppe("betrag")
    assert g_f.rb_linear.isChecked() and g_y.rb_log.isChecked()  # type: ignore[union-attr]
    g_f.rb_log.setChecked(True)  # type: ignore[union-attr]
    assert achse(a).get_xscale() == "log"
    g_y.rb_linear.setChecked(True)  # type: ignore[union-attr]
    assert (achse(a).get_xscale(), achse(a).get_yscale()) == ("log", "linear")
    a.btn_ansicht[2].click()  # je Ansicht: Ansicht 2 hat ihre eigenen Skalen
    assert (achse(a, 0).get_xscale(), achse(a, 0).get_yscale()) == ("linear", "log")
    a.btn_ansicht[1].click()
    assert a.achsenleiste.gruppe("betrag").rb_linear.isChecked()  # type: ignore[union-attr]
    assert a.rb_skala_linear is a.achsenleiste.gruppe("betrag").rb_linear


def test_ui3_felder_und_skalen_bleiben_bei_wechsel(baue: Bauer, qtbot: QtBot) -> None:
    a = geladen_mit(baue, qtbot)
    eingabe(a, "frequenz", "von", "5")
    eingabe(a, "betrag", "bis", "2")
    a.achsenleiste.gruppe("frequenz").rb_log.setChecked(True)  # type: ignore[union-attr]
    felder = (feld(a, "frequenz", "von").text(), feld(a, "betrag", "bis").text())
    grenzen = (achse(a).get_xlim(), achse(a).get_ylim())
    for aendern in (
        lambda: a.liste_punkte.setCurrentRow(2),
        lambda: a.liste_punkte.setCurrentRow(0),
        lambda: a.chk["Y"].setChecked(False),
        lambda: a.rb_groesse_ap.setChecked(True),
    ):
        aendern()  # type: ignore[no-untyped-call]
        assert (feld(a, "frequenz", "von").text(), feld(a, "betrag", "bis").text()) == felder
        assert achse(a).get_xlim() == pytest.approx(grenzen[0], rel=RTOL)
        assert achse(a).get_ylim()[1] == pytest.approx(2.0, rel=RTOL)
        assert achse(a).get_xscale() == "log"


def test_ui4_zoom_aktualisiert_die_felder_und_felder_setzen_den_plot(
    baue: Bauer, qtbot: QtBot
) -> None:
    a = geladen_mit(baue, qtbot)
    assert feld(a, "frequenz", "von").text() == "" and feld(a, "frequenz", "von").placeholderText()
    ziehe_zoom(a)
    ax = achse(a)
    von = feld(a, "frequenz", "von")
    assert von.text() != "" and von.property("fest") == "true"  # Zoom → fest
    assert von.accessibleDescription().endswith("fest, von Hand gesetzt")
    assert "," in von.text() or von.text().isdigit()  # Dezimalkomma
    assert float(von.text().replace(",", ".")) == pytest.approx(ax.get_xlim()[0], rel=5.1e-4)
    assert float(feld(a, "betrag", "bis").text().replace(",", ".")) == pytest.approx(
        ax.get_ylim()[1], rel=5.1e-4
    )
    eingabe(a, "frequenz", "von", "3")  # Feld → Plot
    assert achse(a).get_xlim()[0] == pytest.approx(3.0, rel=RTOL)
    ziehe_pan(a)
    assert float(feld(a, "frequenz", "bis").text().replace(",", ".")) == pytest.approx(
        achse(a).get_xlim()[1], rel=5.1e-4
    )


def test_ui4_alles_auf_auto_leert_die_felder_und_zeigt_auto_werte_grau(
    baue: Bauer, qtbot: QtBot
) -> None:
    a = geladen_mit(baue, qtbot)
    a.achsenleiste.gruppe("betrag").rb_linear.setChecked(True)  # type: ignore[union-attr]
    eingabe(a, "frequenz", "von", "5")
    eingabe(a, "betrag", "bis", "2")
    a.achsenleiste.btn_auto.click()
    for rolle, seite in (("frequenz", "von"), ("frequenz", "bis"), ("betrag", "von")):
        ed = feld(a, rolle, seite)
        assert ed.text() == "" and ed.property("fest") == "false"
        assert "Auto, aktuell" in ed.accessibleDescription()
    assert not a.plot.achsen_zustand.hat_feste(1)
    assert achse(a).get_xlim() == pytest.approx((0.5, 32.0))
    assert a.plot.achsen_zustand.skala(1, "betrag") == "linear"  # Skalen bleiben
    assert feld(a, "frequenz", "von").placeholderText() == "0,5"  # Auto-Wert als Platzhalter
    assert feld(a, "frequenz", "bis").placeholderText() == "32"


@pytest.mark.parametrize(
    ("rolle", "seite", "text", "erwartet"),
    [
        ("frequenz", "von", "abc", TEXT_KEINE_ZAHL),
        ("frequenz", "von", "20", TEXT_REIHENFOLGE),  # von 20 ≥ bis 12 (beide fest gesetzt)
        ("betrag", "von", "-1", TEXT_LOG_NUR_POSITIV),  # y ist logarithmisch
    ],
)
def test_ui5_ungueltige_eingaben_zeigen_meldung_und_lassen_den_plot_unveraendert(
    baue: Bauer, qtbot: QtBot, rolle: str, seite: str, text: str, erwartet: str
) -> None:
    a = geladen_mit(baue, qtbot)
    if text == "20":  # von 20 mit bis = 12: Reihenfolge verletzt
        eingabe(a, "frequenz", "bis", "12")
    vorher = (achse(a).get_xlim(), achse(a).get_ylim(), a.plot.achsen_zustand.bereich(1, rolle))
    alt_text = feld(a, rolle, seite).text()
    eingabe(a, rolle, seite, text)
    assert meldung(a, rolle) == f"{tokens.symbol('fehler')} {erwartet}"
    assert feld(a, rolle, seite).property("fehler") == "true"
    assert (achse(a).get_xlim(), achse(a).get_ylim()) == vorher[:2]  # Plot unverändert
    assert a.plot.achsen_zustand.bereich(1, rolle) == vorher[2]
    fokus_verlassen(feld(a, rolle, seite))  # quittiert: alter Wert kehrt zurück
    assert meldung(a, rolle) == "" and feld(a, rolle, seite).text() == alt_text
    assert feld(a, rolle, seite).property("fehler") == "false"
    assert a.band_fehler.isHidden()


def test_ui5_logarithmus_mit_festem_wert_kleiner_null_wird_abgelehnt(
    baue: Bauer, qtbot: QtBot
) -> None:
    a = geladen_mit(baue, qtbot)
    eingabe(a, "frequenz", "von", "-2")  # linear: gültig
    assert achse(a).get_xlim()[0] == pytest.approx(-2.0)
    g = a.achsenleiste.gruppe("frequenz")
    g.rb_log.setChecked(True)  # type: ignore[union-attr]
    assert meldung(a, "frequenz").endswith(TEXT_LOG_NUR_POSITIV)
    assert g.rb_linear.isChecked() and achse(a).get_xscale() == "linear"  # type: ignore[union-attr]


def test_ui6_neue_datei_leert_felder_skalen_bleiben(baue: Bauer, qtbot: QtBot) -> None:
    from test_gui_auswerten import lade

    a = geladen_mit(baue, qtbot)
    eingabe(a, "frequenz", "von", "5")
    a.achsenleiste.gruppe("betrag").rb_linear.setChecked(True)  # type: ignore[union-attr]
    assert feld(a, "frequenz", "von").text() == "5"
    lade(qtbot, a.window(), "C:\\messungen\\zweite.svd")  # type: ignore[arg-type]
    assert feld(a, "frequenz", "von").text() == ""
    assert a.achsenleiste.gruppe("betrag").rb_linear.isChecked()  # type: ignore[union-attr]
    assert achse(a).get_yscale() == "linear"


def test_ui7_einheiten_hz_grad_und_dezimalkomma(baue: Bauer, qtbot: QtBot) -> None:
    a = geladen_mit(baue, qtbot)
    leiste = a.achsenleiste
    assert leiste.gruppe("frequenz").lbl_einheit.text() == "Hz"
    assert leiste.gruppe("betrag").lbl_einheit.text() == "m/s"  # Einheit der Größe
    a.btn_ansicht[2].click()
    a.auswahl_frf.chk_phase.setChecked(True)
    a.liste_punkte.setCurrentRow(1)
    assert leiste.gruppe("phase").lbl_einheit.text() == "°"  # Phase in Grad, nie rad
    assert leiste.gruppe("betrag").lbl_einheit.text() == "(m/s)/N"
    eingabe(a, "frequenz", "von", "1,25")
    assert feld(a, "frequenz", "von").text() == "1,25"
    assert a.plot.achsen_zustand.bereich(2, "frequenz").von == 1.25


def test_ui37_neuzeichnen_nur_bei_enter_und_nur_bei_aenderung(
    baue: Bauer, qtbot: QtBot, monkeypatch: pytest.MonkeyPatch
) -> None:
    a = geladen_mit(baue, qtbot)
    zaehler = zaehle_zeichnen(a, monkeypatch)
    ed = feld(a, "frequenz", "von")
    ed.setFocus()
    QTest.keyClicks(ed, "5,5")  # Tippen: kein Neuzeichnen
    assert zaehler == [0]
    QTest.keyClick(ed, Qt.Key.Key_Return)  # Enter: genau eines
    assert zaehler == [1]
    fokus_verlassen(ed)  # Fokuswechsel ohne Änderung: keines
    QTest.keyClick(ed, Qt.Key.Key_Return)
    assert zaehler == [1]
    ed.selectAll()
    QTest.keyClicks(ed, "6")
    fokus_verlassen(ed)  # Fokuswechsel mit Änderung: eines
    assert zaehler == [2]
    a.achsenleiste.btn_auto.click()  # Alles auf Auto: eines
    assert zaehler == [3]
    a.achsenleiste.gruppe("betrag").rb_linear.setChecked(True)  # type: ignore[union-attr]
    assert zaehler == [4]
    ed.setFocus()
    ed.selectAll()
    QTest.keyClicks(ed, "abc")
    QTest.keyClick(ed, Qt.Key.Key_Return)  # ungültig: keines
    assert zaehler == [4]


def test_pos1_im_feld_setzt_den_plot_nicht_zurueck(
    baue: Bauer, qtbot: QtBot, monkeypatch: pytest.MonkeyPatch
) -> None:
    a = geladen_mit(baue, qtbot)
    eingabe(a, "frequenz", "von", "5")
    zaehler = zaehle_zeichnen(a, monkeypatch)
    ed = feld(a, "frequenz", "von")
    ed.setFocus()
    QTest.keyClick(ed, Qt.Key.Key_Home)  # Zeilenanfang im Textfeld
    assert zaehler == [0] and a.plot.achsen_zustand.bereich(1, "frequenz").von == 5.0
    assert not a.achsenleiste.isAncestorOf(a.plot) and not a.plot.isAncestorOf(a.achsenleiste)
    assert a.achsenleiste.parent() is a.plot.parent()  # Geschwister (Plan U-A4)


def test_ui34_tab_reihenfolge_und_fokus_der_achsenleiste(baue: Bauer, qtbot: QtBot) -> None:
    a = geladen_mit(baue, qtbot)
    a.window().show()
    kette = a.achsenleiste.tab_kette()
    namen = [w.objectName() for w in kette]
    assert namen[:2] == ["achse_f_von", "achse_f_bis"] and namen[-1] == "btn_achsen_auto"
    plot_kette = a.plot.tab_kette()
    gesamt = list(_tab_reihenfolge(a))
    assert gesamt.index(kette[0]) < gesamt.index(plot_kette[0])  # AD → AG → AE
    assert gesamt.index(a.rb_skala_db) < gesamt.index(kette[0])
    for w in a.achsenleiste.findChildren(QAbstractButton) + a.achsenleiste.findChildren(QLineEdit):
        assert w.focusPolicy() != Qt.FocusPolicy.NoFocus, w.objectName()


def _tab_reihenfolge(a: AuswertenReiter) -> list[QWidget]:
    """Tab-Reihenfolge ab dem ersten Widget (über ``nextInFocusChain``)."""
    start: QWidget = a.btn_oeffnen
    reihe: list[QWidget] = [start]
    w: QWidget | None = start.nextInFocusChain()
    while w is not None and w is not start and len(reihe) < 400:
        reihe.append(w)
        w = w.nextInFocusChain()
    return reihe


def test_ui36_layout_ueberlappungsfrei_bei_1100_x_680_und_ae_mindestens_600_x_320(
    baue: Bauer, qtbot: QtBot
) -> None:
    a = geladen_mit(baue, qtbot)
    w = a.window()
    w.show()
    w.resize(1100, 680)
    for nr in (1, 2, 3):
        a.btn_ansicht[nr].click()
        if nr == 2:
            a.auswahl_frf.chk_phase.setChecked(True)
            a.liste_punkte.setCurrentRow(1)
        qtbot.wait(50)
        assert a.plot.zeichnung is not None and a.band_fehler.isHidden(), nr  # Plot gezeichnet
        leiste = a.achsenleiste
        gruppen = [leiste.gruppe(r) for r in ("frequenz", "betrag", "phase")]
        rechtecke = [g.geometry() for g in gruppen if g.isVisibleTo(leiste)]
        rechtecke.append(leiste.btn_auto.geometry())
        for i, r1 in enumerate(rechtecke):
            assert leiste.rect().contains(r1), (nr, r1)  # nichts abgeschnitten
            for r2 in rechtecke[i + 1 :]:
                assert not r1.intersects(r2), (nr, r1, r2)
        layout = leiste.layout()
        assert layout is not None and leiste.height() >= layout.heightForWidth(leiste.width()) - 1
    w.resize(1366, 768)
    qtbot.wait(100)
    ae = a.findChild(QWidget, "darstellung")
    assert ae is not None and ae.width() >= 600 and ae.height() >= 320


def test_kontrastpaare_der_achsenleiste_stehen_in_den_tokens() -> None:
    namen = {n for n, _v, _h in tokens.KONTRAST_PAARE}
    assert {"text/feld_fest_bg", "fehler/bg", "text_gedaempft/feld_fest_bg"} <= namen
    linie = {n for n, _v, _h in tokens.KONTRAST_PAARE_LINIE}
    assert {"feld_fest_rand/flaeche", "feld_fest_rand/bg"} <= linie


# --- K-AUSW2-A: Korrekturrunde 1 ---------------------------------------------------------------


def zeige(a: AuswertenReiter) -> None:
    """Fenster zeigen und Ereignisse abarbeiten (Geometrie und Rendern brauchen es)."""
    a.window().show()
    QApplication.processEvents()


def test_k1_kleine_betraege_stehen_als_potenz_im_feld_und_die_rundreise_stimmt(
    baue: Bauer, qtbot: QtBot
) -> None:
    a = geladen_mit(baue, qtbot)
    a.achsenleiste.gruppe("betrag").rb_log.setChecked(True)  # type: ignore[union-attr]
    ed = feld(a, "betrag", "von")  # Potenzschreibweise (Sonderzeichen einsetzen, nicht tippen)
    ed.setFocus()
    ed.setText("1,4\u00b710\u207b\u2077")
    QTest.keyClick(ed, Qt.Key.Key_Return)
    eingabe(a, "betrag", "bis", "8,5e-4")  # Exponentenschreibweise wird eingelesen
    z = a.plot.achsen_zustand.bereich(1, "betrag")
    assert z.von == 1.4e-7 and z.bis == 8.5e-4
    assert achse(a).get_ylim() == pytest.approx((1.4e-7, 8.5e-4), rel=RTOL)
    assert feld(a, "betrag", "von").text() == "1,4\u00b710\u207b\u2077"
    assert feld(a, "betrag", "bis").text() == "8,5\u00b710\u207b\u2074"  # Feld → Wert → Feld
    for seite in ("von", "bis"):
        assert "0,000" not in feld(a, "betrag", seite).text()
    a.achsenleiste.btn_auto.click()  # Auto: die grauen Werte sind lesbar (Potenz bei < 1e-3)
    for seite in ("von", "bis"):
        platz = feld(a, "betrag", seite).placeholderText()
        wert = achse(a).get_ylim()[0 if seite == "von" else 1]
        assert platz == feld_text(wert) and len(platz) <= 12


def test_k1_feld_ist_breit_genug_fuer_die_laengsten_texte(baue: Bauer, qtbot: QtBot) -> None:
    a = geladen_mit(baue, qtbot)
    zeige(a)
    ed = feld(a, "betrag", "von")
    opt = QStyleOptionFrame()
    ed.initStyleOption(opt)
    innen = ed.style().subElementRect(QStyle.SubElement.SE_LineEditContents, opt, ed)
    metrik = ed.fontMetrics()
    assert innen.width() > 60  # Rahmen und Innenabstand sind abgezogen, es bleibt Platz für Text
    for wert in (-1.234e-12, -1.234e-9, -8.543e-4, -0.01235, -123457.0, -9.999e-4):
        assert metrik.horizontalAdvance(feld_text(wert)) <= innen.width() + 2, feld_text(wert)


def test_k1_fehlerrahmen_ist_sichtbar_gestrichelt_und_vom_festen_feld_unterscheidbar(
    baue: Bauer, qtbot: QtBot
) -> None:
    a = geladen_mit(baue, qtbot)
    zeige(a)
    ed = feld(a, "frequenz", "von")
    ed.setFocus()
    eingabe(a, "frequenz", "bis", "20")  # festes Feld: durchgezogener Rahmen
    fest_bild = feld(a, "frequenz", "bis").grab().toImage()
    ed.setFocus()
    eingabe(a, "frequenz", "von", "abc")  # Fehler, Fokus bleibt im Feld (Fokusregel!)
    assert ed.hasFocus() or a.achsenleiste.fehler_aktiv("frequenz", "von")
    fehler_bild = ed.grab().toImage()

    def wechsel(bild: Any) -> int:
        """Farbwechsel entlang der oberen Rahmenzeile (Zeile 0): 0 = durchgezogen."""
        zeile = [bild.pixelColor(x, 0).name() for x in range(6, bild.width() - 6)]
        return sum(1 for a_, b_ in itertools.pairwise(zeile) if a_ != b_)

    assert wechsel(fest_bild) == 0  # fest: durchgezogen
    assert wechsel(fehler_bild) >= 4  # Fehler: gestrichelt, auch in Graustufen unterscheidbar
    farben = {fehler_bild.pixelColor(x, 0).name() for x in range(6, fehler_bild.width() - 6)}
    assert tokens.C_FEHLER.lower() in {f.lower() for f in farben}  # Fehlerfarbe, nicht Akzent
    assert tokens.C_AKZENT.lower() not in {f.lower() for f in farben}


def test_k1_meldung_verschiebt_das_layout_nicht(baue: Bauer, qtbot: QtBot) -> None:
    a = geladen_mit(baue, qtbot)
    zeige(a)

    def geometrie() -> tuple[object, ...]:
        return (
            a.achsenleiste.height(),
            a.plot.geometry(),
            a.plot.canvas.height(),
            a.achsenleiste.gruppe("frequenz").geometry(),
            a.achsenleiste.gruppe("betrag").geometry(),
        )

    vorher = geometrie()
    eingabe(a, "frequenz", "bis", "20")  # auch ein fester Wert (2 px Rahmen) ändert die Höhe nicht
    QApplication.processEvents()
    assert geometrie()[:3] == vorher[:3]
    a.achsenleiste.btn_auto.click()
    QApplication.processEvents()
    assert geometrie() == vorher
    eingabe(a, "frequenz", "von", "abc")
    QApplication.processEvents()
    assert meldung(a, "frequenz") != "" and geometrie() == vorher  # Meldung da, nichts springt
    fokus_verlassen(feld(a, "frequenz", "von"))
    QApplication.processEvents()
    assert meldung(a, "frequenz") == "" and geometrie() == vorher
    g = a.achsenleiste.gruppe("frequenz")
    assert g.lbl_meldung.sizePolicy().retainSizeWhenHidden()
    meldungen = (TEXT_KEINE_ZAHL, TEXT_LOG_NUR_POSITIV, TEXT_REIHENFOLGE)
    for text in meldungen:  # die reservierte Breite reicht für jede Standardmeldung
        voll = f"{tokens.symbol('fehler')} {text}"
        assert g.lbl_meldung.fontMetrics().horizontalAdvance(voll) <= g.lbl_meldung.minimumWidth()


def test_k1_ungueltiger_text_wird_beim_ansichtswechsel_per_tastatur_ersetzt(
    baue: Bauer, qtbot: QtBot
) -> None:
    a = geladen_mit(baue, qtbot)
    zeige(a)
    w = a.window()
    ed = feld(a, "frequenz", "von")
    ed.setFocus()
    eingabe(a, "frequenz", "von", "abc")
    assert a.achsenleiste.fehler_aktiv("frequenz", "von") and ed.text() == "abc"
    w.activateWindow()
    QTest.keyClick(w, Qt.Key.Key_2, Qt.KeyboardModifier.ControlModifier)  # Strg+2
    QApplication.processEvents()
    assert a.ansicht == 2
    assert ed.text() == "" and not a.achsenleiste.fehler_aktiv("frequenz", "von")
    assert meldung(a, "frequenz") == "" and ed.property("fehler") == "false"
    # auch ein gültiger, nicht bestätigter Text gehört zur alten Achse und entfällt
    ed.setFocus()
    ed.setText("7")
    QTest.keyClick(w, Qt.Key.Key_3, Qt.KeyboardModifier.ControlModifier)
    QApplication.processEvents()
    assert a.ansicht == 3 and ed.text() == ""
    assert not a.plot.achsen_zustand.hat_feste(2) and not a.plot.achsen_zustand.hat_feste(3)


def test_k1_ansicht_3_bei_1100_x_680_gibt_dem_plot_vorrang_vor_der_tabelle(
    baue: Bauer, qtbot: QtBot
) -> None:
    from ldv_automation.gui.auswerten_reiter import (
        PLOT_MIN_HOEHE_SPLITTER_PX,
        PLOT_WUNSCH_HOEHE_SPLITTER_PX,
    )

    a = geladen_mit(baue, qtbot)
    w = a.window()
    w.show()
    w.resize(1100, 680)
    a.btn_ansicht[3].click()
    qtbot.wait(100)
    QApplication.processEvents()
    assert a.plot.zeichnung is not None and a.band_fehler.isHidden()
    assert a.plot.height() >= PLOT_MIN_HOEHE_SPLITTER_PX  # nicht auf rund 85 px gequetscht
    assert a.tabellen.isVisible() and a.tabellen.height() > 0  # die Tabelle gibt nach, bleibt da
    fig = a.plot.zeichnung.figure
    fig.canvas.draw()
    ax = a.plot.zeichnung.achsen[0]
    achsen_titel = ax.yaxis.label.get_window_extent()
    figur = fig.bbox
    assert figur.x0 - 1 <= achsen_titel.x0 and achsen_titel.x1 <= figur.x1 + 1
    assert (
        figur.y0 - 1 <= achsen_titel.y0 and achsen_titel.y1 <= figur.y1 + 1
    )  # nicht abgeschnitten
    x_titel = a.plot.zeichnung.achsen[-1].xaxis.label.get_window_extent()
    assert figur.y0 - 1 <= x_titel.y0 and x_titel.y1 <= figur.y1 + 1
    w.resize(1366, 768)
    qtbot.wait(100)
    a._splitter_anwenden()
    assert a.plot.height() >= PLOT_WUNSCH_HOEHE_SPLITTER_PX  # genug Platz: Plot wie gewünscht
    assert a.tabellen.height() >= 150  # und die Tabelle behält fast ihre vier Zeilen


def test_k1_einseitige_eingabe_jenseits_der_gegenseite_verschiebt_diese_ohne_meldung(
    baue: Bauer, qtbot: QtBot, monkeypatch: pytest.MonkeyPatch
) -> None:
    a = geladen_mit(baue, qtbot)  # Auto-Frequenz 0,5 … 32 Hz
    zaehler = zaehle_zeichnen(a, monkeypatch)
    eingabe(a, "frequenz", "von", "40")  # hinter dem Datenende, „bis“ ist Auto
    assert meldung(a, "frequenz") == "" and not a.achsenleiste.fehler_aktiv("frequenz", "von")
    assert zaehler == [1]
    spanne = 32.0 - 0.5
    assert achse(a).get_xlim() == pytest.approx((40.0, 40.0 + spanne), rel=RTOL)  # wie _wirksam
    assert feld(a, "frequenz", "von").text() == "40" and feld(a, "frequenz", "von").property("fest")
    bis = feld(a, "frequenz", "bis")  # Leiste zeigt die verschobene Gegenseite grau (Auto)
    assert bis.text() == "" and bis.property("fest") == "false"
    assert bis.placeholderText() == feld_text(40.0 + spanne)
    assert a.plot.achsen_zustand.bereich(1, "frequenz") == Bereich(40.0, None)
    # umgekehrt: nur „bis“ vor dem Datenanfang
    a.achsenleiste.btn_auto.click()
    eingabe(a, "frequenz", "bis", "0,1")
    assert meldung(a, "frequenz") == ""
    assert achse(a).get_xlim() == pytest.approx((0.1 - spanne, 0.1), rel=RTOL)
    # sind beide Seiten gesetzt, gilt die Reihenfolge-Prüfung weiter
    eingabe(a, "frequenz", "von", "5")
    assert meldung(a, "frequenz").endswith(TEXT_REIHENFOLGE)


def test_k1_logarithmische_frequenzachse_ab_0_hz_gibt_weder_fehler_noch_leeren_plot(
    baue: Bauer, qtbot: QtBot
) -> None:
    w, prot = baue(None)
    g = synth_geladen()
    d = g.messdaten
    f0 = d.frequenz_hz - d.frequenz_hz[0]  # k0 = 0: die Frequenzachse beginnt bei 0 Hz
    prot.geladen[PFAD] = replace(g, messdaten=replace(d, frequenz_hz=f0))
    from test_gui_auswerten import lade

    a = lade(qtbot, w)
    assert achse(a).get_xlim()[0] == 0.0 and feld(a, "frequenz", "von").placeholderText() == "0"
    a.achsenleiste.gruppe("frequenz").rb_log.setChecked(True)  # type: ignore[union-attr]
    QApplication.processEvents()
    assert a.band_fehler.isHidden() and meldung(a, "frequenz") == ""
    assert a.plot.zeichnung is not None and achse(a).get_xscale() == "log"
    assert len(achse(a).get_lines()) > 0
    unten, oben = achse(a).get_xlim()
    assert unten == pytest.approx(float(f0[1]), rel=RTOL) and oben == pytest.approx(float(f0[-1]))
    assert feld(a, "frequenz", "von").placeholderText() == feld_text(unten)  # positiv, kein „0“


def test_k1_kleinkram_trenner_ohne_namen_und_abstand_zum_umschalter(
    baue: Bauer, qtbot: QtBot
) -> None:
    a = geladen_mit(baue, qtbot)
    zeige(a)
    for rolle in ("frequenz", "betrag", "phase"):
        assert a.achsenleiste.gruppe(rolle).lbl_trenner.accessibleName() == ""  # dekorativ
    g = a.achsenleiste.gruppe("betrag")
    assert g.skala_box is not None
    luecke = g.skala_box.geometry().left() - g.lbl_einheit.geometry().right()
    assert luecke >= 10  # Einheit und Umschalter stehen nicht aneinander
    assert feld(a, "betrag", "von").accessibleName() == "Achsenbereich Betrag von"


def test_k1_minus_null_zeigt_null(baue: Bauer, qtbot: QtBot) -> None:
    a = geladen_mit(baue, qtbot)
    a.achsenleiste.gruppe("betrag").rb_linear.setChecked(True)  # type: ignore[union-attr]
    eingabe(a, "betrag", "von", "-0")
    assert a.plot.achsen_zustand.bereich(1, "betrag").von == 0.0
    assert feld(a, "betrag", "von").text() == "0"  # Anzeige „0“, nie negativ null
    eingabe(a, "betrag", "von", "1_000")  # Unterstrich ist keine Zahl
    assert meldung(a, "betrag").endswith(TEXT_KEINE_ZAHL)
