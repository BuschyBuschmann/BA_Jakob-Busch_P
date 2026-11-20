"""Oberfläche ist gegen eine fremde ``matplotlibrc`` gehärtet (Paket U-HAERTUNG).

Eine Rechnerdatei mit ``figure.dpi: 200`` und ``text.hinting: no_hinting`` (Container-Fund)
machte alle Plotschriften und Abstände in Pixeln doppelt so groß. Die Oberflächen-Figures legen
ihre DPI selbst fest; die Layoutkriterien gelten mit verstellter ``figure.dpi`` wie mit 100.
"""

from __future__ import annotations

import warnings

import matplotlib
import pytest
from gui_ausw_hilfen import Bauer
from pytestqt.qtbot import QtBot
from test_gui_animation import animation, oeffne
from test_gui_auswerten_ansichten import geladen_mit

from ldv_automation.gui.plotflaeche import FIGURE_DPI

pytestmark = pytest.mark.gui


def fremde_rc(monkeypatch: pytest.MonkeyPatch, dpi: float) -> None:
    """Wie die Container-``matplotlibrc``: verstellte DPI und Hinting (vor dem Bau der Fläche)."""
    monkeypatch.setitem(matplotlib.rcParams, "figure.dpi", dpi)
    monkeypatch.setitem(matplotlib.rcParams, "text.hinting", "no_hinting")


@pytest.mark.parametrize("dpi", [100.0, 200.0])
def test_ansicht_3_achse_ist_bei_fremder_figure_dpi_mindestens_160_px_hoch(
    baue: Bauer, qtbot: QtBot, monkeypatch: pytest.MonkeyPatch, dpi: float
) -> None:
    fremde_rc(monkeypatch, dpi)
    a = geladen_mit(baue, qtbot)
    a.window().resize(1366, 768)
    a.btn_ansicht[3].click()
    qtbot.wait(60)
    a.plot._neuzeichnen_timer.stop()
    a.plot._neuzeichnen()
    z = a.plot.zeichnung
    assert z is not None
    assert z.figure.dpi == FIGURE_DPI * a.plot.canvas.device_pixel_ratio
    assert float(z.achsen[0].get_window_extent().height) >= 160.0


@pytest.mark.parametrize("dpi", [100.0, 200.0])
@pytest.mark.parametrize("nr", [2, 3])
def test_ansicht_mit_phase_bei_1100_x_680_wird_ohne_layoutwarnung_gezeichnet(
    baue: Bauer, qtbot: QtBot, monkeypatch: pytest.MonkeyPatch, dpi: float, nr: int
) -> None:
    fremde_rc(monkeypatch, dpi)
    a = geladen_mit(baue, qtbot, mit_ref2=True)
    a.window().resize(1100, 680)
    a.auswahl_frf.chk_phase.setChecked(True)
    with warnings.catch_warnings():
        warnings.simplefilter("error", UserWarning)  # „constrained_layout not applied“ → Fehler
        for nummer in (nr, 2):
            a.btn_ansicht[nummer].click()
            qtbot.wait(40)
        a.plot._neuzeichnen_timer.stop()
        a.plot._neuzeichnen()
    assert a.fehlertext is None
    z = a.plot.zeichnung
    assert z is not None and "phase" in z.rollen and len(z.achsen) == 3
    assert all(float(ax.get_window_extent().height) > 0.0 for ax in z.achsen)


@pytest.mark.parametrize("dpi", [100.0, 200.0])
def test_animationsflaeche_hat_feste_figure_dpi(
    baue: Bauer, qtbot: QtBot, monkeypatch: pytest.MonkeyPatch, dpi: float
) -> None:
    fremde_rc(monkeypatch, dpi)
    a, _uhr = oeffne(baue, qtbot)
    animation(a)
    qtbot.wait(100)
    canvas = a.animation.canvas
    assert canvas.figure.dpi == FIGURE_DPI * canvas.device_pixel_ratio
