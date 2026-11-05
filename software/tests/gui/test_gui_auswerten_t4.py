"""Reiter „Auswerten“ (P-AUSW T4): Export, Bild, Cursor, Klick, Tastatur, Prüfdialog, Zuletzt.

Ausführen: ``QT_QPA_PLATFORM=offscreen uv run pytest -m gui tests/gui/test_gui_auswerten_t4.py``.
Dateidialoge und Meldungsfenster werden durch Attrappen ersetzt; die Datei kommt aus
``gui_ausw_hilfen.synth_geladen``.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import pytest
from gui_ausw_hilfen import (
    PFAD,
    Bauer,
    NieFertigAusfuehrer,
    SteuerbarerAusfuehrer,
    synth_geladen,
)
from matplotlib.backend_bases import MouseButton, MouseEvent
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from PySide6.QtCore import QMimeData, QPoint, QPointF, Qt, QUrl
from PySide6.QtGui import QDropEvent
from PySide6.QtTest import QTest
from PySide6.QtWidgets import QApplication, QWidget
from pytestqt.qtbot import QtBot

from ldv_automation.gui import anzeige_aktionen as ak
from ldv_automation.gui import anzeige_auswerten as aa
from ldv_automation.gui.auswerten_reiter import AuswertenReiter
from ldv_automation.gui.einstellungen_auswerten import AuswertenEinstellungen
from ldv_automation.gui.hauptfenster import Hauptfenster
from ldv_automation.gui.pruefdialog import PruefDialog

pytestmark = pytest.mark.gui

Reiter = tuple[Hauptfenster, AuswertenReiter, Any, Any]
"""Rückgabe der Fixture ``reiter``: Fenster, Reiter, Protokoll, Meldungen (Attrappen)."""


def lade(qtbot: QtBot, w: Hauptfenster, pfad: str = PFAD) -> AuswertenReiter:
    a = w.auswerten
    assert a is not None
    a.oeffne_datei(pfad)
    qtbot.waitUntil(lambda: a.zustand is aa.AuswertenZustand.GELADEN, timeout=5000)
    qtbot.waitUntil(lambda: not a.laeuft(), timeout=5000)
    return a


def ansicht(a: AuswertenReiter, nr: int) -> None:
    a.btn_ansicht[nr].click()
    QApplication.processEvents()


class Meldungen:
    """Ersetzt Dateidialoge, Meldungsfenster und modale Dialoge des Reiters."""

    def __init__(self, a: AuswertenReiter, monkeypatch: pytest.MonkeyPatch) -> None:
        self.warnungen: list[tuple[str, str]] = []
        self.dialoge: list[Any] = []
        self.export_ziel: str | None = None
        self.bild_ziel: str | None = None
        self.datei: str | None = None
        monkeypatch.setattr(a, "_zeige_warnung", lambda t, x: self.warnungen.append((t, x)))
        monkeypatch.setattr(a, "_waehle_export_ziel", lambda _v: self.export_ziel)
        monkeypatch.setattr(a, "_waehle_bild_ziel", lambda _v: self.bild_ziel)
        monkeypatch.setattr(a, "_waehle_datei", lambda: self.datei)
        monkeypatch.setattr(a, "_fuehre_aus", self._dialog)

    def _dialog(self, dialog: Any) -> int:
        self.dialoge.append(dialog)
        dialog.show()
        return 0


@pytest.fixture
def reiter(baue: Bauer, qtbot: QtBot, monkeypatch: pytest.MonkeyPatch) -> Reiter:
    w, protokoll = baue()
    a = lade(qtbot, w)
    return w, a, protokoll, Meldungen(a, monkeypatch)


# --- Export (UI-16) ----------------------------------------------------------------------------


def test_export_schreibt_beide_dateien_und_meldet_beide_pfade(
    reiter: Reiter, qtbot: QtBot, tmp_path: Path
) -> None:
    _w, a, protokoll, m = reiter
    m.export_ziel = str(tmp_path / "ergebnis.json")  # Endung wird zum Basisnamen gekürzt
    a.btn_export.click()
    assert len(protokoll.export) == 1
    qtbot.waitUntil(lambda: a.btn_export.isEnabled(), timeout=3000)  # Abfrage per QTimer
    pfad, basis, sha, baender, ueberschreiben, antrieb = protokoll.export[0]
    assert pfad == PFAD and basis == str(tmp_path / "ergebnis")
    assert sha is not None and baender is None and ueberschreiben is False  # Gesamtband (F-1)
    assert antrieb == aa.waehle_antriebspunkt(a._paare)  # ohne Ref2: None (P-08 nicht prüfbar)
    npz, js = tmp_path / "ergebnis.npz", tmp_path / "ergebnis.json"
    assert npz.exists() and js.exists()
    assert a.lbl_cursor.volltext() == ak.export_meldung(str(npz), str(js))  # ggf. gekürzt sichtbar
    assert a.lbl_cursor.toolTip() == ak.export_meldung(str(npz), str(js))
    assert not a.balken_export.isVisible() and a.btn_export.isEnabled()


def test_export_vorhandenes_ziel_wird_nicht_ueberschrieben(reiter: Reiter, tmp_path: Path) -> None:
    _w, a, protokoll, m = reiter
    (tmp_path / "ex.json").write_text("alt", encoding="utf-8")
    m.export_ziel = str(tmp_path / "ex")
    a.btn_export.click()
    assert protokoll.export == []  # nichts gestartet
    assert len(m.warnungen) == 1 and "existiert bereits" in m.warnungen[0][1]
    assert (tmp_path / "ex.json").read_text(encoding="utf-8") == "alt"
    assert "existiert bereits" in a.lbl_cursor.text()


def test_export_zielordner_fehlt_und_abbruch_im_dialog(reiter: Reiter, tmp_path: Path) -> None:
    _w, a, protokoll, m = reiter
    m.export_ziel = None  # Dialog abgebrochen
    a.btn_export.click()
    assert protokoll.export == [] and m.warnungen == []
    m.export_ziel = str(tmp_path / "gibtsnicht" / "ex")
    a.btn_export.click()
    assert protokoll.export == [] and "Zielordner fehlt" in m.warnungen[0][1]


def test_export_fehler_des_kerns_wird_gemeldet(
    reiter: Reiter, qtbot: QtBot, tmp_path: Path
) -> None:
    _w, a, protokoll, m = reiter
    protokoll.export_fehler = "Datei verändert"
    m.export_ziel = str(tmp_path / "ex")
    a.btn_export.click()
    qtbot.waitUntil(lambda: bool(m.warnungen), timeout=3000)
    assert m.warnungen == [("Export fehlgeschlagen", "Datei verändert")]
    assert "Datei verändert" in a.lbl_cursor.text() and a.btn_export.isEnabled()


def test_export_laeuft_im_hintergrund_mit_busy_anzeige(
    baue: Bauer, qtbot: QtBot, monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    ausfuehrer = SteuerbarerAusfuehrer()
    w, protokoll = baue(ausfuehrer)
    a = w.auswerten
    assert a is not None
    a.oeffne_datei(PFAD)
    ausfuehrer.auftraege[0].freigegeben = True
    qtbot.waitUntil(lambda: a.zustand is aa.AuswertenZustand.GELADEN, timeout=5000)
    ausfuehrer.auftraege[1].freigegeben = True  # Stufe B
    qtbot.waitUntil(lambda: not a.laeuft(), timeout=5000)
    m = Meldungen(a, monkeypatch)
    m.export_ziel = str(tmp_path / "ex")
    a.btn_export.click()
    assert len(ausfuehrer.auftraege) == 3 and a.balken_export.isVisibleTo(a)
    assert not a.btn_export.isEnabled() and a.btn_export.toolTip() == ak.TEXT_EXPORT_LAEUFT
    assert not a.act_export.isEnabled() and "läuft" in a.lbl_cursor.text()
    a._export_geklickt()  # ein zweiter Export startet nicht
    assert len(ausfuehrer.auftraege) == 3 and protokoll.export == []
    ausfuehrer.auftraege[2].freigegeben = True
    qtbot.waitUntil(lambda: a.btn_export.isEnabled(), timeout=5000)
    assert not a.balken_export.isVisibleTo(a) and (tmp_path / "ex.json").exists()
    assert not a._timer.isActive()


def test_export_wird_beim_schliessen_abgebrochen(
    baue: Bauer, qtbot: QtBot, monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    ausfuehrer = SteuerbarerAusfuehrer()
    w, _p = baue(ausfuehrer)
    a = w.auswerten
    assert a is not None
    a.oeffne_datei(PFAD)
    ausfuehrer.auftraege[0].freigegeben = True
    qtbot.waitUntil(lambda: a.zustand is aa.AuswertenZustand.GELADEN, timeout=5000)
    m = Meldungen(a, monkeypatch)
    m.export_ziel = str(tmp_path / "ex")
    a.btn_export.click()
    a.beende()
    assert ausfuehrer.auftraege[-1].abgebrochen and not a._timer.isActive()


# --- Bild speichern (UI-17) --------------------------------------------------------------------


def _fange_bild(a: AuswertenReiter, monkeypatch: pytest.MonkeyPatch) -> list[Any]:
    gespeichert: list[Any] = []
    original = a.plot.speichere

    def erfasse(pfad: Path, stempel: Any) -> Any:
        z = original(pfad, stempel)
        gespeichert.append(z)
        return z

    monkeypatch.setattr(a.plot, "speichere", erfasse)
    return gespeichert


def test_bild_png_mit_stempel_und_zoom(
    reiter: Reiter, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    _w, a, _p, m = reiter
    bilder = _fange_bild(a, monkeypatch)
    assert a.plot.zeichnung is not None
    _achse(a).set_xlim(5.0, 10.0)  # Zoom der Oberfläche
    m.bild_ziel = str(tmp_path / "a.png")
    a.btn_bild.click()
    assert (tmp_path / "a.png").stat().st_size > 1000
    texte = bilder[0].alle_texte()
    assert any(t.startswith("Arbeitsansicht – nicht für die Thesis") for t in texte)
    stempel = next(t for t in texte if t.startswith("Arbeitsansicht"))
    assert "probe.svd" in stempel and "Ansicht 1 Spektrum" in stempel and "c" * 12 in stempel
    assert not any("unbestätigte" in t for t in texte)  # Ansicht 1: keine M8-Größe
    assert bilder[0].achsen[0].get_xlim() == pytest.approx((5.0, 10.0))  # Zoom übernommen
    assert a.lbl_cursor.text() == ak.bild_meldung(str(tmp_path / "a.png"))
    # die Bildschirmfigur bleibt unverändert
    assert (
        a.plot.zeichnung.figure is a.plot.figure and a.plot.zeichnung.figure is not bilder[0].figure
    )


def test_bild_pdf_und_unbestaetigte_phase_im_stempel(
    reiter: Reiter, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    _w, a, _p, m = reiter
    bilder = _fange_bild(a, monkeypatch)
    ansicht(a, 2)
    a.liste_punkte.setCurrentRow(1)  # Punkt: nur dann wird eine Phase gezeichnet (F-4)
    a.auswahl_frf.chk_phase.setChecked(True)
    QApplication.processEvents()
    m.bild_ziel = str(tmp_path / "b.pdf")
    a.btn_bild.click()
    assert (tmp_path / "b.pdf").read_bytes().startswith(b"%PDF")
    assert any("enthält unbestätigte Größen (M8)" in t for t in bilder[0].alle_texte())
    a.auswahl_frf.chk_phase.setChecked(False)
    QApplication.processEvents()
    m.bild_ziel = str(tmp_path / "c.png")
    a.btn_bild.click()
    assert not any("unbestätigte Größen" in t for t in bilder[1].alle_texte())


def test_bild_ansicht_3_nutzt_voreinstellungen_der_zeichenfunktion(
    reiter: Reiter, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    _w, a, _p, m = reiter
    bilder = _fange_bild(a, monkeypatch)
    ansicht(a, 3)
    assert a.plot.zeichnung is not None
    gui_texte = a.plot.zeichnung.alle_texte()
    assert not any("Betragsmittel" in t for t in gui_texte)  # GUI: Legende in der Auswahlspalte
    m.bild_ziel = str(tmp_path / "d.png")
    a.btn_bild.click()
    bild_texte = bilder[0].alle_texte()
    assert any("Betragsmittel" in t for t in bild_texte)  # Bild: Legende mit Mittelformel


def test_bild_fehler_und_abbruch_und_ansicht_ohne_plot(reiter: Reiter, tmp_path: Path) -> None:
    _w, a, _p, m = reiter
    m.bild_ziel = None
    a.btn_bild.click()
    assert m.warnungen == []
    m.bild_ziel = str(tmp_path / "x.txt")
    a.btn_bild.click()
    assert m.warnungen and m.warnungen[0][0] == "Bild nicht gespeichert"
    assert "nicht unterstützt" in m.warnungen[0][1]


def test_bild_gesperrt_wenn_ansicht_nur_text_zeigt(baue: Bauer, qtbot: QtBot) -> None:
    w, protokoll = baue()
    protokoll.geladen[PFAD] = synth_geladen(referenz=False)
    a = lade(qtbot, w)
    assert a.btn_bild.isEnabled()
    ansicht(a, 2)  # keine Übertragungsfunktion: Text statt Plot
    assert not a.btn_bild.isEnabled() and a.btn_bild.toolTip() == ak.TEXT_BILD_KEINE_DARSTELLUNG
    assert not a.act_bild.isEnabled()
    ansicht(a, 1)
    assert a.btn_bild.isEnabled()


# --- Cursor, Klick, Tastatur (UI-13, UI-14) -----------------------------------------------------


def _achse(a: AuswertenReiter) -> Any:
    zeichnung = a.plot.zeichnung
    assert zeichnung is not None
    return zeichnung.achsen[0]


def _maus(name: str, canvas: Any, x: float, y: float, button: MouseButton | None = None) -> None:
    ereignis: Any = MouseEvent(name, canvas, int(x), int(y), button=button)
    ereignis._process()


def _klick(
    a: AuswertenReiter, f_hz: float, y_rel: float = 0.5, button: MouseButton = MouseButton.LEFT
) -> None:
    ax = _achse(a)
    y0, y1 = ax.get_ylim()
    x, y = ax.transData.transform((f_hz, y0 + (y1 - y0) * y_rel))
    _maus("button_press_event", a.plot.canvas, x, y, button)


def test_cursor_setze_cursor_und_cursorzeile(reiter: Reiter) -> None:
    _w, a, _p, _m = reiter
    assert a.plot.setze_cursor(7.3) == 7.5
    text = a.lbl_cursor.text()
    assert text.startswith("f = 7,500 Hz · Vib X = ")  # Werte vor der Auswahl (rechts gekürzt)
    assert "3D = " in text and "m/s" in text
    assert a.lbl_cursor.toolTip() == a.lbl_cursor.volltext()
    assert a.lbl_cursor.volltext().endswith("m/s · Mittel (alle Punkte)")
    ansicht(a, 2)  # Cursor bleibt, Zeile gilt für die neue Ansicht
    assert a.plot.fadenkreuz.frequenz_hz == 7.5
    assert (
        a.lbl_cursor.text().startswith("f = 7,500 Hz · |H1| = ") and "γ² = " in a.lbl_cursor.text()
    )
    a.liste_punkte.setCurrentRow(1)  # Punkt 10: für das Mittel ist die Phase nicht definiert
    a.auswahl_frf.chk_phase.setChecked(True)
    QApplication.processEvents()
    assert "φ = " in a.lbl_cursor.text() and "⚠ unbestätigt" in a.lbl_cursor.text()
    ansicht(a, 3)
    assert a.lbl_cursor.text().startswith("f = 7,500 Hz · Betrag = ")
    ansicht(a, 4)  # Schwingform: keine Frequenzachse, kein Cursor
    assert a.plot.setze_cursor(5.0) is None
    assert a.lbl_cursor.text() == f"Geladen: {PFAD}"
    ansicht(a, 1)
    assert a.plot.fadenkreuz.frequenz_hz == 7.5 and a.lbl_cursor.text().startswith("f = 7,500")


def test_cursor_folgt_der_maus_und_pfeiltasten(reiter: Reiter, qtbot: QtBot) -> None:
    _w, a, _p, _m = reiter
    ax = _achse(a)
    x, y = ax.transData.transform((10.2, sum(ax.get_ylim()) / 2))
    _maus("motion_notify_event", a.plot.canvas, x, y)
    assert a.plot.fadenkreuz.frequenz_hz == 10.0
    a.plot.canvas.setFocus()
    QTest.keyClick(a.plot.canvas, Qt.Key.Key_Right)
    assert a.plot.fadenkreuz.frequenz_hz == 10.5
    QTest.keyClick(a.plot.canvas, Qt.Key.Key_Left)
    QTest.keyClick(a.plot.canvas, Qt.Key.Key_Left)
    assert a.plot.fadenkreuz.frequenz_hz == 9.5
    QTest.keyClick(a.plot.canvas, Qt.Key.Key_Right, Qt.KeyboardModifier.ShiftModifier)
    assert a.plot.fadenkreuz.frequenz_hz == pytest.approx(14.5)  # zehn Linien
    QTest.keyClick(a.plot.canvas, Qt.Key.Key_Left, Qt.KeyboardModifier.ShiftModifier)
    assert a.plot.fadenkreuz.frequenz_hz == pytest.approx(9.5)
    assert a.lbl_cursor.text().startswith("f = 9,500 Hz")


def test_cursor_aus_ohne_blitting_ohne_fehler(
    baue: Bauer, qtbot: QtBot, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(FigureCanvasQTAgg, "supports_blit", False, raising=False)
    w, _p = baue()
    a = lade(qtbot, w)
    assert a.plot.setze_cursor(7.3) is None and not a.plot.fadenkreuz.verfuegbar
    a.plot.canvas.setFocus()
    QTest.keyClick(a.plot.canvas, Qt.Key.Key_Right)  # kein Fehler
    assert a.fehlertext is None and a.lbl_cursor.text() == f"Geladen: {PFAD}"
    _klick(a, 7.3)  # die Frequenzwahl per Klick funktioniert auch ohne Cursor
    assert a.auswahl_sf.frequenz_hz() == 7.5 or a._a4_wunsch_hz == 7.5


def test_klick_setzt_frequenz_der_schwingform_auf_naechste_linie(reiter: Reiter) -> None:
    _w, a, _p, _m = reiter
    _klick(a, 7.3)
    assert a._a4_wunsch_hz == 7.5 and a.plot.fadenkreuz.frequenz_hz == 7.5
    assert "Frequenz der Schwingform gesetzt" in a.lbl_cursor.text()
    ansicht(a, 4)  # erster Besuch: Startfrequenz ist die gewählte Linie
    assert a.auswahl_sf.frequenz_hz() == 7.5
    ansicht(a, 3)
    _klick(a, 20.2, button=MouseButton.RIGHT)  # rechte Maustaste: keine Wirkung
    assert a.auswahl_sf.frequenz_hz() == 7.5
    _klick(a, 20.2)
    assert a.auswahl_sf.frequenz_hz() == pytest.approx(20.0)


def test_enter_im_plot_uebernimmt_cursorfrequenz(reiter: Reiter) -> None:
    _w, a, _p, _m = reiter
    a.plot.canvas.setFocus()
    QTest.keyClick(a.plot.canvas, Qt.Key.Key_Return)  # ohne Cursor: nichts
    assert a._a4_wunsch_hz is None
    a.plot.setze_cursor(12.2)
    QTest.keyClick(a.plot.canvas, Qt.Key.Key_Return)
    assert a._a4_wunsch_hz == pytest.approx(12.0)
    ansicht(a, 4)
    QTest.keyClick(a.plot.canvas, Qt.Key.Key_Return)  # Ansicht 4: kein Cursor, nichts
    assert a.auswahl_sf.frequenz_hz() == pytest.approx(12.0)


def test_klick_auf_spitzenmarker_markiert_zeile(reiter: Reiter) -> None:
    _w, a, _p, _m = reiter
    ansicht(a, 3)
    spitzen: Any = a._a3_spitzen
    assert spitzen, "synthetische Datei hat eine Resonanz bei 16 Hz"
    s = spitzen[0]
    ax = _achse(a)
    x, y = ax.transData.transform((s.f_sp_hz, s.hoehe))
    _maus("button_press_event", a.plot.canvas, x, y, MouseButton.LEFT)
    assert a._spitze == 0
    assert a.tabelle_spitzen.tabelle.currentIndex().row() == 0
    ansicht(a, 1)
    assert a._a4_wunsch_hz == pytest.approx(s.f_k_hz, abs=0.5)  # Klick setzt auch die Frequenz


def test_pos1_setzt_zoom_zurueck_nur_bei_fokus_im_plot(reiter: Reiter, qtbot: QtBot) -> None:
    _w, a, _p, _m = reiter
    ax = _achse(a)
    standard = ax.get_xlim()
    ax.set_xlim(5.0, 10.0)
    a.liste_punkte.setFocus()
    QTest.keyClick(a.liste_punkte, Qt.Key.Key_Home)
    assert ax.get_xlim() == pytest.approx((5.0, 10.0))  # Pos1 in der Liste wirkt nicht auf den Plot
    a.plot.canvas.setFocus()
    QTest.keyClick(a.plot.canvas, Qt.Key.Key_Home)
    qtbot.waitUntil(lambda: ax.get_xlim() == pytest.approx(standard), timeout=3000)
    assert a.plot.act_zuruecksetzen.shortcut().toString() == "Home"
    assert "Pos1" in str(a.plot.toolbar.toolitems[0][1])


# --- Aktionen und Tastatur (UI-19) --------------------------------------------------------------


def test_tooltips_nennen_die_taste(reiter: Reiter) -> None:
    w, a, _p, _m = reiter
    assert "Strg+Umschalt+O" in a.btn_oeffnen.toolTip()
    assert "Strg+E" in a.btn_export.toolTip()
    assert "Strg+Umschalt+S" in a.btn_bild.toolTip()
    for nr in (1, 2, 3, 4):
        assert f"Strg+{nr}" in a.btn_ansicht[nr].toolTip()
    assert "Alt+1" in w.reiter.tabToolTip(0) and "Alt+2" in w.reiter.tabToolTip(1)


def _taste(w: Hauptfenster, key: Qt.Key, mod: Qt.KeyboardModifier) -> None:
    w.activateWindow()
    QTest.keyClick(w, key, mod)


def test_tastenkuerzel(reiter: Reiter, qtbot: QtBot, tmp_path: Path) -> None:
    w, a, protokoll, m = reiter
    strg = Qt.KeyboardModifier.ControlModifier
    for nr, key in ((2, Qt.Key.Key_2), (3, Qt.Key.Key_3), (4, Qt.Key.Key_4), (1, Qt.Key.Key_1)):
        _taste(w, key, strg)
        assert a.ansicht == nr and a.btn_ansicht[nr].isChecked()
    m.export_ziel = str(tmp_path / "t")
    _taste(w, Qt.Key.Key_E, strg)
    assert len(protokoll.export) == 1
    m.bild_ziel = str(tmp_path / "t.png")
    _taste(w, Qt.Key.Key_S, strg | Qt.KeyboardModifier.ShiftModifier)
    assert (tmp_path / "t.png").exists()
    m.datei = "C:\\messungen\\zweite.svd"
    _taste(w, Qt.Key.Key_O, strg | Qt.KeyboardModifier.ShiftModifier)
    qtbot.waitUntil(lambda: protokoll.lese[-1] == "C:\\messungen\\zweite.svd", timeout=3000)


def test_alt_1_alt_2_wechseln_den_reiter(reiter: Reiter) -> None:
    w, _a, _p, _m = reiter
    alt = Qt.KeyboardModifier.AltModifier
    _taste(w, Qt.Key.Key_1, alt)
    assert w.reiter.currentIndex() == 0
    _taste(w, Qt.Key.Key_2, alt)
    assert w.reiter.currentIndex() == 1


def test_auswerten_kuerzel_wirken_nicht_im_reiter_messen_und_f_tasten_nicht_im_auswerten(
    reiter: Reiter,
) -> None:
    w, a, protokoll, m = reiter
    for aktion in (w.act_start, w.act_pause, w.act_abbrechen, w.act_bestaetigen, w.act_laden):
        assert not aktion.isEnabled()  # F5 bis F8, Strg+O: im Reiter „Auswerten“ ohne Wirkung
    _taste(w, Qt.Key.Key_5, Qt.KeyboardModifier.NoModifier)
    w.reiter.setCurrentIndex(0)
    m.export_ziel = "x"
    _taste(w, Qt.Key.Key_E, Qt.KeyboardModifier.ControlModifier)  # im Reiter „Messen“
    assert protokoll.export == [] and not a.isVisible()


# --- Prüfdialog (UI-23) --------------------------------------------------------------------------


def test_klick_auf_pruefzusammenfassung_oeffnet_dialog_esc_schliesst(reiter: Reiter) -> None:
    _w, a, _p, m = reiter
    assert a.lbl_pruefung.text() == "Prüfung: 1 Warnung, 1 ok"
    QTest.mouseClick(a.lbl_pruefung, Qt.MouseButton.LeftButton)
    assert len(m.dialoge) == 1
    d: PruefDialog = m.dialoge[0]
    assert d.isVisible() and d.lbl_zusammenfassung.text() == a.lbl_pruefung.text()
    assert d.tabelle.rowCount() == 2 and d.tabelle.columnCount() == 5
    assert d.tabelle.item(0, 0).text() == "P-01"  # type: ignore[union-attr]
    assert "Warnung" in d.tabelle.item(1, 1).text()  # type: ignore[union-attr]
    assert d.tabelle.editTriggers() == d.tabelle.EditTrigger.NoEditTriggers  # schreibgeschützt
    QTest.keyClick(d, Qt.Key.Key_Escape)
    assert not d.isVisible()


def test_pruefzusammenfassung_per_tastatur_und_ohne_ergebnis(
    baue: Bauer, qtbot: QtBot, monkeypatch: pytest.MonkeyPatch
) -> None:
    w, _p = baue(NieFertigAusfuehrer())
    a = w.auswerten
    assert a is not None
    m = Meldungen(a, monkeypatch)
    QTest.mouseClick(a.lbl_pruefung, Qt.MouseButton.LeftButton)
    assert m.dialoge == []  # ohne Datei kein Dialog
    a._uebernehme(a._job_id, synth_geladen(), PFAD)  # Stufe A fertig, Stufe B läuft noch
    assert a.lbl_pruefung.focusPolicy() != Qt.FocusPolicy.NoFocus
    a.lbl_pruefung.setFocus()
    QTest.keyClick(a.lbl_pruefung, Qt.Key.Key_Return)
    d = m.dialoge[0]
    assert d.tabelle.rowCount() == 0 and "noch nicht berechnet" in d.lbl_leer.text()
    assert d.lbl_leer.isVisibleTo(d) and d.lbl_zusammenfassung.text() == aa.TEXT_PRUEFUNG_BERECHNET
    d.close()
    QTest.keyClick(a.lbl_pruefung, Qt.Key.Key_Space)
    assert len(m.dialoge) == 2
    m.dialoge[1].close()


# --- Zuletzt geöffnet, Ordner, Drag-and-drop -----------------------------------------------------


def test_einstellungen_rundlauf_in_ini(tmp_path: Path, qtbot: QtBot) -> None:
    ini = str(tmp_path / "e.ini")
    e = AuswertenEinstellungen(ini)
    assert e.zuletzt() == () and e.letzter_ordner() == ""
    e.merke_datei("a.svd")
    e.merke_ordner("/ordner")
    zweite = AuswertenEinstellungen(ini)  # frisch gelesen: aus der Datei
    assert zweite.zuletzt() == ("a.svd",) and zweite.letzter_ordner() == "/ordner"
    for n in range(8):
        zweite.merke_datei(f"{n}.svd")
    assert len(AuswertenEinstellungen(ini).zuletzt()) == 5
    assert AuswertenEinstellungen(ini).zuletzt()[0] == "7.svd"
    assert Path(ini).read_text(encoding="utf-8").lstrip().startswith("[General]")


def test_zuletzt_geoeffnet_im_leerzustand_hoechstens_fuenf(
    baue: Bauer, qtbot: QtBot, tmp_path: Path
) -> None:
    w, _p = baue()
    a = lade(qtbot, w, str(tmp_path / "eins.svd"))
    for n in range(7):
        datei = tmp_path / f"d{n}.svd"
        datei.write_bytes(b"")
        lade(qtbot, w, str(datei))
    assert a._einstellungen.letzter_ordner() == str(tmp_path)
    assert len(a._einstellungen.zuletzt()) == 5
    w2, _p2 = baue()  # neues Fenster, gleiche INI: Zustand „Keine Datei“ mit Liste
    a2 = w2.auswerten
    assert a2 is not None and a2.zustand is aa.AuswertenZustand.KEINE_DATEI
    assert a2.zuletzt_gruppe.isVisibleTo(a2) and a2.liste_zuletzt.count() == 5
    assert a2.liste_zuletzt.item(0).text().startswith("d6.svd")
    assert a2._letzter_ordner == str(tmp_path)  # Ordner gemerkt
    assert a2.liste_zuletzt.focusPolicy() != Qt.FocusPolicy.NoFocus
    a2.liste_zuletzt.itemActivated.emit(a2.liste_zuletzt.item(0))
    qtbot.waitUntil(lambda: a2.zustand is aa.AuswertenZustand.GELADEN, timeout=5000)
    assert a2.lbl_datei.text() == "d6.svd" and not a2.zuletzt_gruppe.isVisibleTo(a2)


def test_zuletzt_fehlende_datei_ist_gesperrt_und_leere_liste_hat_hinweis(
    baue: Bauer, qtbot: QtBot, tmp_path: Path
) -> None:
    w, _p = baue()
    a = w.auswerten
    assert a is not None and a.liste_zuletzt.count() == 0
    assert not a.liste_zuletzt.isVisibleTo(a) and a.lbl_zuletzt.text() == ak.TEXT_KEINE_ZULETZT
    a._einstellungen.merke_datei(str(tmp_path / "weg.svd"))
    a._fuelle_zuletzt(sichtbar=True)
    item = a.liste_zuletzt.item(0)
    assert "nicht gefunden" in item.text() and not item.flags() & Qt.ItemFlag.ItemIsEnabled


def _drop(w: Hauptfenster, pfad: str) -> None:
    mime = QMimeData()
    mime.setUrls([QUrl.fromLocalFile(pfad)])
    ereignis = QDropEvent(
        QPointF(5, 5),
        Qt.DropAction.CopyAction,
        mime,
        Qt.MouseButton.LeftButton,
        Qt.KeyboardModifier.NoModifier,
    )
    w.dropEvent(ereignis)


def test_drag_and_drop_einer_svd_oeffnet_im_reiter_auswerten(
    baue: Bauer, qtbot: QtBot, tmp_path: Path
) -> None:
    w, protokoll = baue(aktiv=False)
    assert w.acceptDrops() and w.auswerten is None
    datei = tmp_path / "gedroppt.svd"
    datei.write_bytes(b"")
    _drop(w, str(datei))
    assert w.reiter.currentIndex() == 1 and w.auswerten is not None
    qtbot.waitUntil(lambda: w.auswerten.zustand is aa.AuswertenZustand.GELADEN, timeout=5000)
    assert protokoll.lese == [str(datei)]
    _drop(w, str(tmp_path / "x.txt"))  # keine .svd: ignoriert
    assert protokoll.lese == [str(datei)]


# --- Fokus und Layout (UI-21, UI-25) -------------------------------------------------------------


def _fokuskette(a: AuswertenReiter) -> list[QWidget]:
    kette: list[QWidget] = []
    w: QWidget = a.btn_oeffnen
    for _ in range(400):
        if w in kette:
            break
        if (
            w.isVisibleTo(a)
            and w.isEnabled()
            and a.isAncestorOf(w)
            and bool(w.focusPolicy() & Qt.FocusPolicy.TabFocus)
        ):
            kette.append(w)
        naechster = w.nextInFocusChain()
        assert naechster is not None
        w = naechster
    return kette


def test_tab_reihenfolge_aa_ac_ad_ae_af(reiter: Reiter) -> None:
    _w, a, _p, _m = reiter
    kette = _fokuskette(a)

    def pos(widget: QWidget) -> int:
        return kette.index(widget)

    erwartet: list[QWidget] = [
        a.btn_oeffnen,
        a.btn_export,
        a.btn_bild,
        *(a.btn_ansicht[n] for n in (1, 2, 3, 4)),
        a.liste_punkte,
        a.plot.canvas,
        *(k for k in a.plot.toolbar.knoepfe() if k.isEnabled()),
        a.lbl_pruefung,
    ]
    positionen = [pos(x) for x in erwartet]
    assert positionen == sorted(positionen)  # AA → AC → AD → AE (Plot, Werkzeugleiste) → AF
    assert a.parameterzeile not in kette  # AB nicht fokussierbar
    assert not any(z in kette for z in a.parameterzeile.zellen)


def test_alle_bedienbaren_widgets_sind_fokussierbar(reiter: Reiter) -> None:
    _w, a, _p, _m = reiter
    from PySide6.QtWidgets import (
        QAbstractButton,
        QAbstractSpinBox,
        QComboBox,
        QListWidget,
        QTableView,
    )

    bedienbar = (
        QAbstractButton,
        QAbstractSpinBox,
        QComboBox,
        QListWidget,
        QTableView,
    )
    fehlend = [
        w.objectName() or type(w).__name__
        for w in a.findChildren(QWidget)
        if isinstance(w, bedienbar)
        and w.focusPolicy() == Qt.FocusPolicy.NoFocus
        and not w.objectName().startswith("qt_")  # interne Qt-Teile (Tabellenecke)
    ]
    assert fehlend == []
    assert a.plot.canvas.focusPolicy() != Qt.FocusPolicy.NoFocus
    assert a.lbl_pruefung.focusPolicy() != Qt.FocusPolicy.NoFocus


def test_fokus_ist_sichtbar_qss_regeln(reiter: Reiter) -> None:
    _w, _a, _p, _m = reiter
    app = QApplication.instance()
    assert isinstance(app, QApplication)
    qss = app.styleSheet()
    assert "QLabel#lbl_pruefung:focus" in qss and "QListWidget:focus" in qss
    assert "plot_rahmen" in qss and 'fokus="true"' in qss.replace("'", '"')


@pytest.mark.parametrize("groesse", [(1100, 680), (1366, 768)])
@pytest.mark.parametrize("nr", [1, 2, 3, 4])
def test_ui_25_keine_ueberlappung_der_zonen(
    reiter: Reiter, groesse: tuple[int, int], nr: int
) -> None:
    w, a, _p, _m = reiter
    w.resize(*groesse)
    ansicht(a, nr)
    QApplication.processEvents()
    zonen = {
        "AA": a.findChild(QWidget, "dateileiste"),
        "AB": a.parameterzeile,
        "AC": a.findChild(QWidget, "ansichtswahl"),
        "AD": a.auswahlspalte,
        "AE": a.findChild(QWidget, "darstellung"),
        "AF": a.findChild(QWidget, "fusszeile"),
    }
    rechtecke = {}
    for name, widget in zonen.items():
        assert widget is not None
        ecke = widget.mapTo(a, QPoint(0, 0))
        rechtecke[name] = (ecke.x(), ecke.y(), widget.width(), widget.height())
    namen = list(rechtecke)
    for i, n1 in enumerate(namen):
        for n2 in namen[i + 1 :]:
            x1, y1, b1, h1 = rechtecke[n1]
            x2, y2, b2, h2 = rechtecke[n2]
            ueberlappt = x1 < x2 + b2 and x2 < x1 + b1 and y1 < y2 + h2 and y2 < y1 + h1
            assert not ueberlappt, f"{n1} überlappt {n2} bei {groesse}: {rechtecke}"
    for name, (x, y, b, h) in rechtecke.items():
        assert x >= 0 and y >= 0 and x + b <= a.width() and y + h <= a.height(), name
    if groesse == (1366, 768):
        assert rechtecke["AE"][2] >= 600 and rechtecke["AE"][3] >= 320
    # Fußzeile: Meldung, Busy-Balken und Prüftext überlappen nicht
    fuss = [a.lbl_cursor, a.lbl_pruefung]
    (x1, _), (x2, _) = ((x.geometry().x(), x.width()) for x in fuss)
    assert x1 + a.lbl_cursor.width() <= x2
