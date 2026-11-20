"""Betragsgruppe der Achsenleiste springt beim Erscheinen der Einheit nicht (Paket K-HAERTUNG).

Die Einheit des Betrags („m/s“, „m“, „m/s²“) steht erst nach dem ersten Zeichnen fest; die
Gruppe war dadurch 15 px breiter geworden. Das Einheitenlabel reserviert jetzt die Breite
der breitesten möglichen Einheit.
"""

from __future__ import annotations

import pytest
from PySide6.QtWidgets import QApplication
from pytestqt.qtbot import QtBot

from ldv_automation.gui.achsen_zustand import AchsenZustand
from ldv_automation.gui.achsenleiste import _EINHEITEN_BREIT, Achsenleiste

pytestmark = pytest.mark.gui

WIRKSAM = {"frequenz": (0.5, 32.0), "betrag": (1e-6, 1e-3)}


def _geometrie(leiste: Achsenleiste) -> tuple[object, ...]:
    layout = leiste.layout()
    assert layout is not None
    layout.activate()
    QApplication.processEvents()
    g = leiste.gruppe("betrag")
    return (leiste.height(), g.geometry(), g.sizeHint(), leiste.gruppe("frequenz").geometry())


def test_betragsgruppe_hat_von_anfang_an_die_breite_fuer_jede_einheit(qtbot: QtBot) -> None:
    leiste = Achsenleiste(AchsenZustand())
    qtbot.addWidget(leiste)
    leiste.setze_ansicht(1)
    leiste.resize(1300, 80)
    leiste.show()
    leiste.aktualisiere(WIRKSAM, {})  # erstes Zeichnen: Einheit noch nicht bekannt
    vorher = _geometrie(leiste)
    for einheit in ("m/s", "m", "m/s²", ""):
        leiste.aktualisiere(WIRKSAM, {"frequenz": "Hz", "betrag": einheit})
        assert _geometrie(leiste) == vorher, einheit


def test_reservierte_einheitenbreite_reicht_fuer_alle_bekannten_einheiten(qtbot: QtBot) -> None:
    leiste = Achsenleiste(AchsenZustand())
    qtbot.addWidget(leiste)
    label = leiste.gruppe("betrag").lbl_einheit
    for einheit in _EINHEITEN_BREIT:
        label.setText(einheit)
        assert label.sizeHint().width() <= label.minimumWidth()
