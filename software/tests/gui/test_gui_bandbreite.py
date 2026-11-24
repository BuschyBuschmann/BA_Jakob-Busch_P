"""BW-2: Bandbreite im Editor nur als PSV-Stufe waehlbar (Qt offscreen, Marker ``gui``)."""

from __future__ import annotations

from dataclasses import replace
from typing import Any

import pytest
from gui_hilfen import INFO, AttrappenSitzung, bild
from PySide6.QtWidgets import QComboBox
from pytestqt.qtbot import QtBot

from ldv_automation.gui.editor import HINWEIS_OFFLINE, HINWEIS_STUFEN_NICHT_LESBAR, Editor

pytestmark = pytest.mark.gui

STUFEN = (3125.0, 5000.0, 6250.0)
SCHLUESSEL = "fft.bandbreite_hz"


def _editor(qtbot: QtBot) -> Editor:
    ed = Editor()
    qtbot.addWidget(ed)
    ed.neu_messung("am Ende")
    return ed


def _zeile(ed: Editor) -> Any:
    return next(pz for pz in ed.parameter if pz.spec.schluessel == SCHLUESSEL)


def _texte(combo: QComboBox) -> list[str]:
    return [combo.itemText(i) for i in range(combo.count())]


def test_offline_auswahl_gesperrt_mit_hinweis(qtbot: QtBot) -> None:
    ed = _editor(qtbot)
    pz = _zeile(ed)
    assert isinstance(pz.eingabe, QComboBox)
    assert _texte(pz.eingabe) == [HINWEIS_OFFLINE]
    assert not pz.aendern.isEnabled()
    assert not pz.eingabe.isEnabled()
    assert pz.eingabe.toolTip() == HINWEIS_OFFLINE


def test_online_nur_stufen_waehlbar_und_uebernommen(qtbot: QtBot) -> None:
    ed = _editor(qtbot)
    ed.setze_bandbreiten_stufen(STUFEN, "")
    pz = _zeile(ed)
    assert _texte(pz.eingabe) == ["(aus .set)", "3125", "5000", "6250"]  # keine freie Eingabe
    assert pz.aendern.isEnabled()
    pz.aendern.setChecked(True)
    assert pz.eingabe.isEnabled()
    pz.eingabe.setCurrentIndex(3)
    assert pz.lies() == (6250.0, None)
    ed.name.setText("M1")
    ed.set_feld.setText("/x/a.set")
    assert ed.messung_eingaben().parameter == {SCHLUESSEL: 6250.0}


def test_stufenliste_unveraendert_behaelt_auswahl(qtbot: QtBot) -> None:
    ed = _editor(qtbot)
    ed.setze_bandbreiten_stufen(STUFEN, "")
    pz = _zeile(ed)
    pz.aendern.setChecked(True)
    pz.eingabe.setCurrentIndex(2)
    ed.setze_bandbreiten_stufen(STUFEN, "")  # jede Zustandsaktualisierung ruft das auf
    assert pz.lies() == (5000.0, None)
    ed.setze_bandbreiten_stufen((5000.0, 6250.0), "")  # neue Liste: Wert bleibt, falls enthalten
    assert pz.lies() == (5000.0, None)


def test_gespeicherter_wert_ausserhalb_der_liste_ist_fehler(qtbot: QtBot) -> None:
    ed = _editor(qtbot)
    pz = _zeile(ed)
    pz.setze(5600.0)  # Altdatei, offline
    assert _texte(pz.eingabe) == [HINWEIS_OFFLINE, "5600"]  # Wert bleibt sichtbar
    assert pz.lies() == (5600.0, None)  # ohne Liste nicht beurteilbar
    ed.setze_bandbreiten_stufen(STUFEN, "")
    assert "5600 (keine PSV-Stufe)" in _texte(pz.eingabe)
    wert, fehler = pz.lies()
    assert wert is None and fehler is not None and "keine PSV-Stufe" in fehler
    assert ed.fehler()
    assert pz.fehler.text() == fehler
    assert not pz.fehler.isHidden()
    pz.eingabe.setCurrentIndex(3)  # auf eine echte Stufe wechseln behebt den Fehler
    assert pz.lies() == (6250.0, None)


def test_gespeicherter_wert_auf_stufe_bleibt_gueltig(qtbot: QtBot) -> None:
    ed = _editor(qtbot)
    pz = _zeile(ed)
    pz.setze(6250.0)
    ed.setze_bandbreiten_stufen(STUFEN, "")
    assert pz.lies() == (6250.0, None)
    assert pz.eingabe.currentText() == "6250"


def test_liste_nicht_lesbar_sperrt_auswahl(qtbot: QtBot) -> None:
    ed = _editor(qtbot)
    ed.setze_bandbreiten_stufen(None, HINWEIS_STUFEN_NICHT_LESBAR)
    pz = _zeile(ed)
    assert _texte(pz.eingabe) == [HINWEIS_STUFEN_NICHT_LESBAR]
    assert not pz.aendern.isEnabled()


def test_verbindung_verlorenes_stufen_wieder_gesperrt(qtbot: QtBot) -> None:
    ed = _editor(qtbot)
    ed.setze_bandbreiten_stufen(STUFEN, "")
    ed.setze_bandbreiten_stufen(None, HINWEIS_OFFLINE)
    pz = _zeile(ed)
    assert not pz.aendern.isEnabled()
    assert _texte(pz.eingabe) == [HINWEIS_OFFLINE]


def test_hauptfenster_gibt_stufen_der_verbindung_an_den_editor(baue: Any, qtbot: QtBot) -> None:
    s = AttrappenSitzung(bild(verbindung=None))
    w, _ = baue(sitzung=s)
    assert _zeile(w.editor).eingabe.count() == 1  # offline: nur Hinweis
    s.setze(verbindung=replace(INFO, bandbreiten_stufen_hz=STUFEN))
    w.aktualisiere()
    assert _texte(_zeile(w.editor).eingabe) == ["(aus .set)", "3125", "5000", "6250"]
    s.setze(verbindung=replace(INFO, bandbreiten_stufen_hz=None, bandbreiten_stufen_fehler="x"))
    w.aktualisiere()
    assert _texte(_zeile(w.editor).eingabe) == ["x"]
