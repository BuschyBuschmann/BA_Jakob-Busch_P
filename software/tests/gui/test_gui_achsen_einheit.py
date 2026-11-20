"""Betragsgruppe der Achsenleiste springt bei keiner Einheit (Pakete K-HAERTUNG, K2-HAERTUNG).

Die Einheit des Betrags steht erst nach dem ersten Zeichnen fest und wechselt mit der Ansicht
(„m/s“, „mm/s“, „(m/s)/N“ …); die Gruppe war dadurch breiter geworden. Das Einheitenlabel hat
jetzt eine feste Breite (normal: bis „(m/s²)/N“; kleines
Fenster: bis „(m/s)/N“, längere Texte werden in der Mitte gekürzt und stehen im Tooltip).
"""

from __future__ import annotations

import pytest
from PySide6.QtWidgets import QApplication
from pytestqt.qtbot import QtBot

from ldv_automation.gui.achsen_zustand import AchsenZustand
from ldv_automation.gui.achsenleiste import _EINHEIT_KOMPAKT, _EINHEITEN_VOLL, Achsenleiste

pytestmark = pytest.mark.gui

WIRKSAM = {"frequenz": (0.5, 32.0), "betrag": (1e-6, 1e-3)}
GENANNT = ("m", "m/s", "mm/s", "µm/s", "m/s/N", "(m/s)/N")
"""Vom Nutzer genannte und häufige Einheiten (müssen auch bei kleinem Fenster ganz erscheinen)."""
LANG = ("(nm/s²)/N", "(m/s)/(m/s²)", "((m/s)/N)^2")
"""Länger als die reservierte Breite: gekürzt mit Tooltip, springt trotzdem nicht."""


def _leiste(qtbot: QtBot, ansicht: int, *, kompakt: bool) -> Achsenleiste:
    leiste = Achsenleiste(AchsenZustand())
    qtbot.addWidget(leiste)
    leiste.setze_ansicht(ansicht)
    leiste.resize(804 if kompakt else 1366, 90)
    leiste.setze_kompakt(kompakt)
    leiste.show()
    leiste.aktualisiere(WIRKSAM, {})  # erstes Zeichnen: Einheit noch nicht bekannt
    return leiste


def _geometrie(leiste: Achsenleiste) -> tuple[object, ...]:
    layout = leiste.layout()
    assert layout is not None
    layout.activate()
    QApplication.processEvents()
    g = leiste.gruppe("betrag")
    return (leiste.height(), g.geometry(), g.sizeHint(), leiste.gruppe("frequenz").geometry())


@pytest.mark.parametrize("kompakt", [False, True])
@pytest.mark.parametrize("ansicht", [1, 5])
def test_betragsgruppe_springt_bei_keiner_einheit(
    qtbot: QtBot, ansicht: int, kompakt: bool
) -> None:
    leiste = _leiste(qtbot, ansicht, kompakt=kompakt)
    vorher = _geometrie(leiste)
    for einheit in (*_EINHEITEN_VOLL, *GENANNT, *LANG, ""):
        leiste.aktualisiere(WIRKSAM, {"frequenz": "Hz", "betrag": einheit})
        assert _geometrie(leiste) == vorher, einheit


@pytest.mark.parametrize("kompakt", [False, True])
def test_genannte_einheiten_erscheinen_ganz_ohne_tooltip(qtbot: QtBot, kompakt: bool) -> None:
    leiste = _leiste(qtbot, 5, kompakt=kompakt)
    label = leiste.gruppe("betrag").lbl_einheit
    for einheit in GENANNT:
        leiste.aktualisiere(WIRKSAM, {"betrag": einheit})
        assert label.text() == einheit and label.toolTip() == "", einheit


def test_normale_leiste_zeigt_jede_erzeugte_einheit_ganz(qtbot: QtBot) -> None:
    leiste = _leiste(qtbot, 5, kompakt=False)
    label = leiste.gruppe("betrag").lbl_einheit
    for einheit in _EINHEITEN_VOLL:
        leiste.aktualisiere(WIRKSAM, {"betrag": einheit})
        assert label.text() == einheit and label.toolTip() == "", einheit


def test_zu_lange_einheit_ist_gekuerzt_und_steht_im_tooltip(qtbot: QtBot) -> None:
    leiste = _leiste(qtbot, 5, kompakt=True)
    label = leiste.gruppe("betrag").lbl_einheit
    for einheit in LANG:
        leiste.aktualisiere(WIRKSAM, {"betrag": einheit})
        assert label.text() != einheit and label.text().startswith(einheit[0]), einheit
        assert "…" in label.text() and label.toolTip() == einheit
    leiste.aktualisiere(WIRKSAM, {"betrag": "m/s"})
    assert label.toolTip() == ""  # kein Tooltip-Rest


@pytest.mark.parametrize("einheit", [*GENANNT, *_EINHEITEN_VOLL, *LANG])
def test_kompakte_leiste_bleibt_bei_804_px_mit_jeder_einheit_einzeilig(
    qtbot: QtBot, einheit: str
) -> None:
    leiste = _leiste(qtbot, 5, kompakt=True)
    leiste.aktualisiere(WIRKSAM, {"frequenz": "Hz", "betrag": einheit})
    layout = leiste.layout()
    assert layout is not None
    zeile = leiste.gruppe("betrag").sizeHint().height() + 4  # wie test_kompakte_achsenleiste_…
    assert layout.heightForWidth(804) <= zeile + 2, einheit


def test_kompakte_grenzeinheit_ist_die_breiteste_ganz_gezeigte(qtbot: QtBot) -> None:
    assert _EINHEIT_KOMPAKT == "(m/s)/N" and _EINHEIT_KOMPAKT in GENANNT
