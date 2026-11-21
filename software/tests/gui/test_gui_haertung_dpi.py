"""Oberfläche ist gegen eine fremde ``matplotlibrc`` gehärtet (Paket U-HAERTUNG).

Eine Rechnerdatei mit ``figure.dpi: 200`` und ``text.hinting: no_hinting`` (Container-Fund)
machte alle Plotschriften und Abstände in Pixeln doppelt so groß. Die Oberflächen-Figures legen
ihre DPI selbst fest; die Layoutkriterien gelten mit verstellter ``figure.dpi`` wie mit 100.
"""

from __future__ import annotations

import warnings
from collections.abc import Callable
from pathlib import Path
from typing import Any

import matplotlib
import pytest
from dar_animation_hilfen import lange_platte
from gui_ausw_hilfen import Bauer
from pytestqt.qtbot import QtBot
from test_dar_animation_rc_haertung import ABWEICHEND
from test_gui_animation import animation, oeffne
from test_gui_animationsflaeche import Uhr
from test_gui_ansicht_5 import aufbau as aufbau_5
from test_gui_auswerten_ansichten import geladen_mit

from ldv_automation.darstellung.animation3d import AnimationsOptionen
from ldv_automation.darstellung.bild import Stempel, baue_stempel
from ldv_automation.darstellung.stil import THESIS_STIL
from ldv_automation.gui.animationsflaeche import AnimationsFlaeche
from ldv_automation.gui.plotflaeche import FIGURE_DPI
from ldv_automation.gui.serien import baue_spec

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


# --- Export (Paket K-HAERTUNG): Bilddatei unabhängig von rc-figure.dpi ---------------------------


def _stempel() -> Stempel:
    return baue_stempel(dateiname="a.svd", ansicht="Test", git_hash="abc")


def _bytes_je_dpi(
    monkeypatch: pytest.MonkeyPatch, erzeuge: Callable[[float], bytes]
) -> dict[float, bytes]:
    monkeypatch.setenv("SOURCE_DATE_EPOCH", "1700000000")  # PDF: festes CreationDate
    return {dpi: erzeuge(dpi) for dpi in (100.0, 200.0)}


@pytest.mark.parametrize("endung", ["png", "pdf"])
@pytest.mark.parametrize("ansicht", [1, 3, 4])
def test_plotflaeche_export_ist_bei_rc_figure_dpi_100_und_200_gleich(
    baue: Bauer,
    qtbot: QtBot,
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
    ansicht: int,
    endung: str,
) -> None:
    def erzeuge(dpi: float) -> bytes:
        fremde_rc(monkeypatch, dpi)
        a = geladen_mit(baue, qtbot)
        a.window().resize(1366, 768)
        a.btn_ansicht[ansicht].click()
        qtbot.wait(60)
        ziel = tmp_path / f"p{ansicht}_{int(dpi)}.{endung}"
        a.plot.speichere(ziel, _stempel())
        return ziel.read_bytes()

    inhalte = _bytes_je_dpi(monkeypatch, erzeuge)
    assert inhalte[100.0] == inhalte[200.0]


@pytest.mark.parametrize("endung", ["png", "pdf"])
def test_diagramm_export_ist_bei_rc_figure_dpi_100_und_200_gleich(
    baue: Bauer,
    qtbot: QtBot,
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
    endung: str,
) -> None:
    def erzeuge(dpi: float) -> bytes:
        fremde_rc(monkeypatch, dpi)
        a, _, _, _ = aufbau_5(baue)
        a.btn_ansicht[5].click()
        for spec in (
            baue_spec(a.messungen.alle[0].id, None, "h1", kanalpaar=("Vib X", "Ref1")),
            baue_spec(a.messungen.alle[1].id, None, "h1", kanalpaar=("Vib X", "Ref1")),
        ):
            assert a._serie_anlegen(spec)
        a._zeichne()
        ziel = tmp_path / f"d_{int(dpi)}.{endung}"
        a.plot.speichere(ziel, _stempel())
        return ziel.read_bytes()

    inhalte = _bytes_je_dpi(monkeypatch, erzeuge)
    assert inhalte[100.0] == inhalte[200.0]


@pytest.mark.parametrize("endung", ["png", "pdf"])
def test_animation_standbild_export_ist_bei_rc_figure_dpi_100_und_200_gleich(
    qtbot: QtBot, monkeypatch: pytest.MonkeyPatch, tmp_path: Path, endung: str
) -> None:
    schritte: dict[float, object] = {}

    def erzeuge(dpi: float) -> bytes:
        fremde_rc(monkeypatch, dpi)
        f = AnimationsFlaeche(THESIS_STIL, zeit=Uhr(), tempo_hz=0.25, blick_vorgabe="iso")
        qtbot.addWidget(f)
        f.resize(640, 480)
        f.show()
        qtbot.waitExposed(f)
        f.zeichne(lange_platte(2.25, 45, 9), AnimationsOptionen(punktlabels=True), "Beschreibung")
        ziel = tmp_path / f"a_{int(dpi)}.{endung}"
        z = f.speichere(ziel, _stempel())
        schritte[dpi] = z.hilfsobjekte["punktlabels_schritt"]
        return ziel.read_bytes()

    inhalte = _bytes_je_dpi(monkeypatch, erzeuge)
    assert schritte[100.0] == schritte[200.0] and schritte[100.0] != 0
    assert inhalte[100.0] == inhalte[200.0]


# --- Paket U-HAERTUNG-3D: Gitter, Wände, Linien, Hinting der Animation aus dem Standard ---------


def _pixel_der_flaeche(
    qtbot: QtBot, monkeypatch: pytest.MonkeyPatch, rc: dict[Any, Any]
) -> tuple[bytes, Any]:
    """Pixelpuffer der gezeichneten Animationsfläche unter den rc-Werten ``rc`` (vor dem Bau)."""
    for k, v in rc.items():
        monkeypatch.setitem(matplotlib.rcParams, k, v)
    f = AnimationsFlaeche(THESIS_STIL, zeit=Uhr(), tempo_hz=0.25, blick_vorgabe="iso")
    qtbot.addWidget(f)
    f.resize(640, 480)
    f.show()
    qtbot.waitExposed(f)
    f.zeichne(lange_platte(2.25, 45, 9), AnimationsOptionen(punktlabels=True), "Beschreibung")
    f.canvas.draw()  # type: ignore[no-untyped-call]
    puffer = bytes(f.canvas.buffer_rgba())  # type: ignore[no-untyped-call]
    z = f.zeichnung
    assert z is not None
    for k in rc:  # außerhalb des Kontexts der Fläche bleibt der Wert des Rechners stehen
        assert matplotlib.rcParams[k] == rc[k]
    return puffer, z.hilfsobjekte["punktlabels_schritt"]


@pytest.mark.parametrize("schluessel", sorted(ABWEICHEND))
def test_animationsflaeche_zeichnet_bei_abweichendem_rc_schluessel_wie_im_standard(
    qtbot: QtBot, monkeypatch: pytest.MonkeyPatch, schluessel: str
) -> None:
    standard, s0 = _pixel_der_flaeche(qtbot, monkeypatch, {})
    fremd, s1 = _pixel_der_flaeche(qtbot, monkeypatch, {schluessel: ABWEICHEND[schluessel]})
    assert s0 not in (None, 0) and s1 == s0
    assert fremd == standard


def test_animationsflaeche_zeichnet_bei_allen_abweichenden_schluesseln_wie_im_standard(
    qtbot: QtBot, monkeypatch: pytest.MonkeyPatch
) -> None:
    standard, _ = _pixel_der_flaeche(qtbot, monkeypatch, {})
    fremd, _ = _pixel_der_flaeche(qtbot, monkeypatch, dict(ABWEICHEND))
    assert fremd == standard
