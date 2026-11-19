"""AnimationsFlaeche (R-071, Plan P-AUSW3 AN6): UI-23, UI-24, UI-32, UI-34; offscreen, ``gui``.

Geprüft werden Zustände und die Struktur der Figure (``ax.azim/elev``, Positionen der Scatter),
keine Pixel. Der Timer wird von Hand getaktet (``takt()``) mit einer injizierten Uhr, damit nichts
von der echten Zeit abhängt. Daten: ``gui_ausw_hilfen.synth_geladen`` (4 Punkte, Linie 16 Hz).
"""

from __future__ import annotations

import math
from collections.abc import Callable
from dataclasses import replace
from pathlib import Path
from typing import Any

import numpy as np
import pytest
from gui_ausw_hilfen import synth_geladen
from matplotlib.backend_bases import MouseButton, MouseEvent
from PySide6.QtCore import QEvent, QPoint, QPointF, Qt
from PySide6.QtGui import QFocusEvent, QWheelEvent
from PySide6.QtTest import QTest
from PySide6.QtWidgets import QApplication
from pytestqt.qtbot import QtBot

from ldv_automation.darstellung.achsen import Bereich
from ldv_automation.darstellung.animation3d import (
    BLICK_VORGABEN,
    AnimationsOptionen,
    effektive_ueberhoehung,
    scatter_positionen,
)
from ldv_automation.darstellung.animation_daten import AnimationsDaten, animation_daten
from ldv_automation.darstellung.auswahl import PaarCache
from ldv_automation.darstellung.bild import baue_stempel
from ldv_automation.darstellung.stil import THESIS_STIL
from ldv_automation.gui import animationsflaeche, tokens
from ldv_automation.gui.animation_steuerung import (
    DREH_SCHRITT_GRAD,
    GRAD_JE_PIXEL,
    ZOOM_MAX,
    Stufe,
)
from ldv_automation.gui.animationsflaeche import (
    BILDZEIT_MINDEST,
    AnimationsFlaeche,
)

pytestmark = pytest.mark.gui

TEMPO_HZ = 0.25  # Perioden je Sekunde: nach 1 s steht θ bei 90°
ATOL_RAD = 1e-9  # Rundung von θ aus der Uhr (Fließkomma, kein Modellfehler)


class Uhr:
    """Handgeführte Zeitquelle in s (Phasenuhr bzw. Bildzeitmessung)."""

    def __init__(self, schritt: float = 0.0) -> None:
        self.t = 0.0
        self.schritt = schritt

    def __call__(self) -> float:
        wert = self.t
        self.t += self.schritt  # Messzeit: jeder Aufruf schreitet fort
        return wert


def _daten(komponente: str = "3D", **kw: Any) -> AnimationsDaten:
    md = synth_geladen().messdaten
    return animation_daten(md, PaarCache(md), 16.0, komponente=komponente, **kw)


@pytest.fixture
def bau(qtbot: QtBot) -> Callable[..., tuple[AnimationsFlaeche, Uhr]]:
    """Baut eine gezeichnete Fläche mit handgeführter Uhr (Blick Isometrie, 640 x 480)."""

    def _bau(
        *, stufe: Stufe = Stufe.L0, zeichnen: bool = True, **kw: Any
    ) -> tuple[AnimationsFlaeche, Uhr]:
        uhr = Uhr()
        f = AnimationsFlaeche(
            THESIS_STIL, zeit=uhr, tempo_hz=TEMPO_HZ, stufe=stufe, blick_vorgabe="iso", **kw
        )
        qtbot.addWidget(f)
        f.resize(640, 480)
        f.show()
        qtbot.waitExposed(f)
        if zeichnen:
            f.zeichne(_daten(), AnimationsOptionen(), "Beschreibung")
        return f, uhr

    return _bau


def _achse(f: AnimationsFlaeche) -> Any:
    assert f.zeichnung is not None
    return f.zeichnung.achsen[0]


def _optionen(f: AnimationsFlaeche) -> AnimationsOptionen:
    assert f.zeichnung is not None
    opt: AnimationsOptionen = f.zeichnung.hilfsobjekte["optionen"]
    return opt


def _ziehe(
    f: AnimationsFlaeche, dx: int, dy: int, taste: Qt.MouseButton = Qt.MouseButton.LeftButton
) -> None:
    start = QPoint(100, 100)
    QTest.mousePress(f.canvas, taste, Qt.KeyboardModifier.NoModifier, start)
    QTest.mouseMove(f.canvas, start + QPoint(dx, dy))
    QTest.mouseRelease(f.canvas, taste, Qt.KeyboardModifier.NoModifier, start + QPoint(dx, dy))


def _rad(f: AnimationsFlaeche, rasten: float) -> None:
    pos = QPointF(50.0, 50.0)
    ereignis = QWheelEvent(
        pos,
        f.canvas.mapToGlobal(pos),
        QPoint(0, 0),
        QPoint(0, round(120 * rasten)),
        Qt.MouseButton.NoButton,
        Qt.KeyboardModifier.NoModifier,
        Qt.ScrollPhase.NoScrollPhase,
        False,
    )
    QApplication.sendEvent(f.canvas, ereignis)


# --- Aufbau, Fokus (UI-34) -------------------------------------------------------------------


def test_zeichnet_3d_figure_mit_blickvorgabe_und_beschreibung(bau: Any) -> None:
    f, _ = bau()
    ax = _achse(f)
    assert ax.name == "3d" and f.zeichnung is not None
    assert (ax.azim, ax.elev) == pytest.approx(
        (BLICK_VORGABEN["iso"].azim_grad, BLICK_VORGABEN["iso"].elev_grad)
    )
    assert f.canvas.accessibleDescription() == "Beschreibung" and f.beschreibung == "Beschreibung"
    assert not f.laeuft  # nichts startet von selbst (UI-22)


def test_eigene_steuerung_statt_mplot3d_rotation(bau: Any) -> None:
    f, _ = bau()
    # disable_mouse_rotation: matplotlib reagiert selbst nicht auf Ziehen (keine zweite Steuerung)
    azim = _achse(f).azim
    for art, x in (("button_press_event", 200), ("motion_notify_event", 260)):
        ereignis = MouseEvent(art, f.canvas, x, 200, button=MouseButton.LEFT)
        f.canvas.callbacks.process(art, ereignis)
    assert _achse(f).azim == azim


def test_fokus_sichtbar_und_fokussierbar(bau: Any) -> None:
    f, _ = bau()
    assert f.canvas.focusPolicy() == Qt.FocusPolicy.StrongFocus
    assert f.tab_kette() == [f.canvas]
    assert tokens.C_AKZENT in f._rahmen.styleSheet()
    assert f._rahmen.property("fokus") in (None, "false")
    QApplication.sendEvent(f.canvas, QFocusEvent(QEvent.Type.FocusIn))
    assert f._rahmen.property("fokus") == "true"
    QApplication.sendEvent(f.canvas, QFocusEvent(QEvent.Type.FocusOut))
    assert f._rahmen.property("fokus") == "false"


# --- Maus: Drehen und Zoom (UI-23) -----------------------------------------------------------


def test_mausziehen_aendert_azimut_und_elevation(bau: Any) -> None:
    f, _ = bau()
    azim0, elev0 = _achse(f).azim, _achse(f).elev
    gemeldet: list[int] = []
    f.blick_geaendert.connect(lambda: gemeldet.append(1))
    _ziehe(f, 50, 20)
    assert _achse(f).azim == pytest.approx(azim0 + GRAD_JE_PIXEL * 50)
    assert _achse(f).elev == pytest.approx(elev0 - GRAD_JE_PIXEL * 20)
    assert f.blick.azim_grad == pytest.approx(_achse(f).azim)
    assert gemeldet
    # nach dem Loslassen steht das Bild voll (Achsen, Panes, Ticks)
    assert not _optionen(f).vereinfacht and _achse(f)._axis3don


def test_waehrend_des_ziehens_sind_die_achsen_vereinfacht_stufe_l0(bau: Any) -> None:
    f, _ = bau()
    start = QPoint(100, 100)
    QTest.mousePress(f.canvas, Qt.MouseButton.LeftButton, Qt.KeyboardModifier.NoModifier, start)
    QTest.mouseMove(f.canvas, start + QPoint(10, 0))
    assert _optionen(f).vereinfacht and not _achse(f)._axis3don
    QTest.mouseRelease(
        f.canvas, Qt.MouseButton.LeftButton, Qt.KeyboardModifier.NoModifier, start + QPoint(10, 0)
    )
    assert not _optionen(f).vereinfacht and _achse(f)._axis3don


def test_elevation_bleibt_in_den_grenzen(bau: Any) -> None:
    f, _ = bau()
    _ziehe(f, 0, -2000)
    assert _achse(f).elev == pytest.approx(90.0)
    _ziehe(f, 0, 2000)
    assert _achse(f).elev == pytest.approx(-90.0)


def test_rechte_und_mittlere_taste_haben_keine_wirkung(bau: Any) -> None:
    f, _ = bau()
    vorher = f.blick
    _ziehe(f, 50, 20, Qt.MouseButton.RightButton)
    _ziehe(f, 50, 20, Qt.MouseButton.MiddleButton)
    assert f.blick == vorher and _achse(f).azim == pytest.approx(vorher.azim_grad)


def test_bewegen_ohne_taste_dreht_nicht(bau: Any) -> None:
    f, _ = bau()
    vorher = f.blick
    QTest.mouseMove(f.canvas, QPoint(10, 10))
    QTest.mouseMove(f.canvas, QPoint(60, 40))
    assert f.blick == vorher


def test_rad_aendert_den_zoom_und_ist_begrenzt(bau: Any) -> None:
    f, _ = bau()
    ax = _achse(f)
    vorher = float(np.linalg.norm(ax.get_box_aspect()))
    _rad(f, 1.0)
    assert f.blick.zoom == pytest.approx(1.1)
    assert float(np.linalg.norm(ax.get_box_aspect())) == pytest.approx(1.1 * vorher, rel=1e-9)
    _rad(f, -2.0)
    assert f.blick.zoom == pytest.approx(1.1 * 1.1**-2)
    _rad(f, 100.0)
    assert f.blick.zoom == pytest.approx(ZOOM_MAX)  # Grenze
    _rad(f, 0.0)  # keine Raste: nichts geändert
    assert f.blick.zoom == pytest.approx(ZOOM_MAX)


def test_doppelklick_und_vorgaben_setzen_die_ansicht(bau: Any) -> None:
    f, _ = bau()
    _ziehe(f, 80, 30)
    _rad(f, 3.0)
    QTest.mouseDClick(
        f.canvas, Qt.MouseButton.LeftButton, Qt.KeyboardModifier.NoModifier, QPoint(10, 10)
    )
    assert f.blick == BLICK_VORGABEN["iso"]
    for name in ("xy", "xz", "yz", "iso"):  # die fünf Knöpfe: vier Vorgaben und Zurücksetzen
        f.setze_blick_vorgabe(name)
        assert (_achse(f).azim, _achse(f).elev) == pytest.approx(
            (BLICK_VORGABEN[name].azim_grad, BLICK_VORGABEN[name].elev_grad)
        )
    f.setze_blick_vorgabe("xz")
    _ziehe(f, 10, 10)
    f.ansicht_zuruecksetzen()  # kehrt zur gewählten Vorgabe zurück
    assert f.blick == BLICK_VORGABEN["xz"]
    with pytest.raises(ValueError, match="Blickvorgabe"):
        f.setze_blick_vorgabe("unbekannt")


# --- Tasten (UI-32) --------------------------------------------------------------------------


def test_pfeiltasten_aendern_die_phase_nicht_den_blick(bau: Any) -> None:
    f, _ = bau()
    gemeldet: list[float] = []
    f.phase_geaendert.connect(gemeldet.append)
    blick = f.blick
    QTest.keyClick(f.canvas, Qt.Key.Key_Right)
    assert math.degrees(f.uhr.theta_rad) == pytest.approx(10.0)
    assert _optionen(f).theta_rad == pytest.approx(math.radians(10.0))
    QTest.keyClick(f.canvas, Qt.Key.Key_Left)
    QTest.keyClick(f.canvas, Qt.Key.Key_Left)
    assert math.degrees(f.uhr.theta_rad) == pytest.approx(350.0)  # Umlauf
    assert f.blick == blick and len(gemeldet) == 3
    QTest.keyClick(f.canvas, Qt.Key.Key_Right, Qt.KeyboardModifier.ControlModifier)
    assert math.degrees(f.uhr.theta_rad) == pytest.approx(80.0)  # 90°-Schritt


def test_umschalt_pfeile_und_auf_ab_drehen(bau: Any) -> None:
    f, _ = bau()
    b0 = f.blick
    QTest.keyClick(f.canvas, Qt.Key.Key_Right, Qt.KeyboardModifier.ShiftModifier)
    assert f.blick.azim_grad == pytest.approx(b0.azim_grad + DREH_SCHRITT_GRAD)
    QTest.keyClick(f.canvas, Qt.Key.Key_Left, Qt.KeyboardModifier.ShiftModifier)
    assert f.blick.azim_grad == pytest.approx(b0.azim_grad)
    QTest.keyClick(f.canvas, Qt.Key.Key_Up)
    assert f.blick.elev_grad == pytest.approx(b0.elev_grad + DREH_SCHRITT_GRAD)
    QTest.keyClick(f.canvas, Qt.Key.Key_Down)
    QTest.keyClick(f.canvas, Qt.Key.Key_Down)
    assert f.blick.elev_grad == pytest.approx(b0.elev_grad - DREH_SCHRITT_GRAD)
    assert _achse(f).elev == pytest.approx(f.blick.elev_grad)
    assert f.uhr.theta_rad == 0.0  # Drehen ändert die Phase nicht


def test_zoomtasten_und_pos1(bau: Any) -> None:
    f, _ = bau()
    QTest.keyClick(f.canvas, Qt.Key.Key_Plus)
    QTest.keyClick(f.canvas, Qt.Key.Key_Plus, Qt.KeyboardModifier.ShiftModifier)  # „+“ mit Umschalt
    assert f.blick.zoom == pytest.approx(1.1**2)
    QTest.keyClick(f.canvas, Qt.Key.Key_Minus)
    assert f.blick.zoom == pytest.approx(1.1)
    QTest.keyClick(f.canvas, Qt.Key.Key_Up)
    f.uhr.setze_theta_grad(40.0)
    QTest.keyClick(f.canvas, Qt.Key.Key_Home)
    assert f.blick == BLICK_VORGABEN["iso"]  # Blick und Zoom zurück
    assert math.degrees(f.uhr.theta_rad) == pytest.approx(40.0)  # nicht θ


def test_nicht_belegte_tasten_werden_nicht_verbraucht(bau: Any, qtbot: QtBot) -> None:
    f, _ = bau()
    vorher = (f.blick, f.uhr.theta_rad)
    for taste, mods in (
        (Qt.Key.Key_A, Qt.KeyboardModifier.NoModifier),
        (Qt.Key.Key_Left, Qt.KeyboardModifier.AltModifier),
        (Qt.Key.Key_Left, Qt.KeyboardModifier.ShiftModifier | Qt.KeyboardModifier.ControlModifier),
        (Qt.Key.Key_Space, Qt.KeyboardModifier.ShiftModifier),
    ):
        QTest.keyClick(f.canvas, taste, mods)
    assert (f.blick, f.uhr.theta_rad) == vorher and not f.laeuft


# --- Wiedergabe (UI-24) ----------------------------------------------------------------------


def test_abspielen_laeuft_pause_haelt_an(bau: Any) -> None:
    f, uhr = bau()
    wechsel: list[bool] = []
    f.wiedergabe_geaendert.connect(wechsel.append)
    assert f.abspielen() and f.laeuft and f._timer.isActive()
    assert f._timer.timerType() == Qt.TimerType.PreciseTimer and f._timer.isSingleShot()
    uhr.t = 1.0  # eine Sekunde bei 0,25 Perioden/s: θ = 90°
    f.takt()
    assert f.uhr.theta_rad == pytest.approx(math.pi / 2.0, abs=ATOL_RAD)
    assert _optionen(f).vereinfacht and not _achse(f)._axis3don  # Stufe L0: vereinfacht in Bewegung
    assert f._timer.isActive()  # je Bild neu gestartet
    f.pausiere()
    assert not f.laeuft and not f._timer.isActive() and wechsel == [True, False]
    assert not _optionen(f).vereinfacht and _achse(f)._axis3don  # im Stand voll
    uhr.t = 5.0
    f.takt()  # nach der Pause ohne Wirkung
    assert f.uhr.theta_rad == pytest.approx(math.pi / 2.0, abs=ATOL_RAD)


def test_bild_der_wiedergabe_ist_das_standbild_bei_theta(bau: Any) -> None:
    """UI-25: Positionen der Figure = ``AnimationsDaten.positionen`` (ein Datenpfad)."""
    f, uhr = bau()
    daten = _daten()
    s = effektive_ueberhoehung(daten, AnimationsOptionen())
    f.abspielen()
    uhr.t = 2.0  # θ = 180°
    f.takt()
    assert f.zeichnung is not None
    soll = daten.positionen(f.uhr.theta_rad, s)[daten.bewegt]
    assert np.allclose(scatter_positionen(f.zeichnung), soll, rtol=1e-12, atol=1e-15)


def test_ausgelassene_bilder_aendern_die_phase_nicht(bau: Any) -> None:
    f, uhr = bau()
    f.abspielen()
    uhr.t = 3.0  # ein einziger Takt nach drei Sekunden: θ = 270°
    f.takt()
    assert f.uhr.theta_rad == pytest.approx(1.5 * math.pi, abs=ATOL_RAD)


def test_leertaste_schaltet_um_und_schritt_haelt_an(bau: Any) -> None:
    f, uhr = bau()
    QTest.keyClick(f.canvas, Qt.Key.Key_Space)
    assert f.laeuft and f._timer.isActive()
    uhr.t = 1.0
    QTest.keyClick(f.canvas, Qt.Key.Key_Right)  # Einzelschritt: hält die Wiedergabe an
    assert not f.laeuft and not f._timer.isActive()
    assert math.degrees(f.uhr.theta_rad) == pytest.approx(100.0)  # 90° (Uhr) + 10° (Schritt)
    QTest.keyClick(f.canvas, Qt.Key.Key_Space)
    assert f.laeuft
    QTest.keyClick(f.canvas, Qt.Key.Key_Space)
    assert not f.laeuft


def test_abspielen_ohne_darstellung_tut_nichts(bau: Any) -> None:
    f, _ = bau(zeichnen=False)
    assert not f.abspielen() and not f.laeuft and not f._timer.isActive()
    f.takt()  # kein Bild, kein Fehler
    assert not f.umschalten()


def test_regler_und_einzelschritt_in_grad(bau: Any) -> None:
    f, _ = bau()
    f.setze_schritt_grad(30.0)
    f.schritt(+1)
    assert math.degrees(f.uhr.theta_rad) == pytest.approx(30.0)
    f.schritt(-1, 90.0)
    assert math.degrees(f.uhr.theta_rad) == pytest.approx(300.0)
    f.setze_theta_grad(45.0)
    assert math.degrees(_optionen(f).theta_rad) == pytest.approx(45.0)
    f.setze_tempo_hz(0.5)
    assert f.uhr.tempo_hz == 0.5


def test_wiedergabe_pausiert_beim_ziehen_und_setzt_nicht_selbst_fort(bau: Any) -> None:
    f, uhr = bau()
    f.abspielen()
    uhr.t = 1.0
    f.takt()
    start = QPoint(100, 100)
    QTest.mousePress(f.canvas, Qt.MouseButton.LeftButton, Qt.KeyboardModifier.NoModifier, start)
    assert not f.laeuft and not f._timer.isActive()
    QTest.mouseMove(f.canvas, start + QPoint(20, 0))
    QTest.mouseRelease(
        f.canvas, Qt.MouseButton.LeftButton, Qt.KeyboardModifier.NoModifier, start + QPoint(20, 0)
    )
    assert not f.laeuft and not f._timer.isActive()  # Fortsetzen nur durch Nutzeraktion
    assert f.uhr.theta_rad == pytest.approx(math.pi / 2.0, abs=ATOL_RAD)


def test_wiedergabe_pausiert_beim_ziehen_des_reglers(bau: Any) -> None:
    f, _ = bau()
    f.abspielen()
    f.setze_theta_grad(120.0, ziehend=True)
    assert not f.laeuft and not f._timer.isActive()
    assert math.degrees(f.uhr.theta_rad) == pytest.approx(120.0)
    assert not _optionen(f).vereinfacht  # Stufe L0: nur Wiedergabe und Drehen vereinfacht
    f.phase_losgelassen()
    assert _achse(f)._axis3don


def test_frequenzwechsel_fuehrt_ins_standbild(bau: Any) -> None:
    f, uhr = bau()
    wechsel: list[bool] = []
    f.wiedergabe_geaendert.connect(wechsel.append)
    f.abspielen()
    uhr.t = 1.0
    f.takt()
    assert f.frequenz_gewechselt() == "standbild"
    assert not f.laeuft and not f._timer.isActive() and f.uhr.theta_rad == 0.0
    assert wechsel == [True, False]
    assert f.frequenz_gewechselt() == "standbild"  # ohne Wiedergabe: kein weiteres Signal
    assert wechsel == [True, False]


def test_neue_daten_behalten_blick_und_winkel_und_wiedergabe(bau: Any) -> None:
    f, _ = bau()
    _ziehe(f, 30, 10)
    f.uhr.setze_theta_grad(70.0)
    blick = f.blick
    f.abspielen()
    f.zeichne(_daten("Z"), AnimationsOptionen(farbe="betrag"), "neu")
    assert f.blick == blick and f.laeuft
    assert math.degrees(_optionen(f).theta_rad) == pytest.approx(70.0)
    assert (_achse(f).azim, _achse(f).elev) == pytest.approx((blick.azim_grad, blick.elev_grad))
    assert f.canvas.accessibleDescription() == "neu"


# --- Bildzeit und Hinweis „langsam“ -----------------------------------------------------------


def test_messung_der_bildzeit_und_hinweis_langsam(qtbot: QtBot) -> None:
    mess = Uhr(schritt=0.25)  # jede Messung 0,25 s weiter: Bildzeit 0,25 s > Intervall 0,1 s
    f = AnimationsFlaeche(THESIS_STIL, zeit=Uhr(), messzeit=mess, bildrate=10, blick_vorgabe="iso")
    qtbot.addWidget(f)
    f.resize(640, 480)
    f.show()
    f.zeichne(_daten(), AnimationsOptionen())
    assert f.bildzeit_median_s is None and not f.langsam
    meldungen: list[bool] = []
    f.langsam_geaendert.connect(meldungen.append)
    f.abspielen()
    for _ in range(BILDZEIT_MINDEST - 1):
        f.takt()
    assert not f.langsam  # zu wenige Bilder: ein langsames erstes Bild löst nichts aus
    f.takt()
    assert f.langsam and meldungen == [True]
    assert f.bildzeit_median_s == pytest.approx(0.25)
    assert f.bildrate == 10  # nie still herabgesetzt
    assert f._timer.interval() == 0  # kein Restintervall: Zeichnen dauert länger als der Takt
    f.pausiere()  # der Hinweis gilt nur für die laufende Wiedergabe: beim Pausieren zurück
    assert not f.langsam and meldungen == [True, False]
    f.abspielen()  # neuer Lauf: Messung beginnt neu
    assert not f.langsam and meldungen == [True, False] and f.bildzeit_median_s is None


def test_hinweis_langsam_endet_auch_beim_einzelschritt_aus_der_wiedergabe(qtbot: QtBot) -> None:
    f = AnimationsFlaeche(
        THESIS_STIL, zeit=Uhr(), messzeit=Uhr(schritt=0.25), bildrate=10, blick_vorgabe="iso"
    )
    qtbot.addWidget(f)
    f.resize(640, 480)
    f.show()
    f.zeichne(_daten(), AnimationsOptionen())
    meldungen: list[bool] = []
    f.langsam_geaendert.connect(meldungen.append)
    f.abspielen()
    for _ in range(BILDZEIT_MINDEST):
        f.takt()
    assert f.langsam and meldungen == [True]
    f.schritt(1)  # hält die Wiedergabe an
    assert not f.laeuft and not f.langsam and meldungen == [True, False]


def test_rechtzeitige_wiedergabe_meldet_nicht(qtbot: QtBot) -> None:
    f = AnimationsFlaeche(
        THESIS_STIL, zeit=Uhr(), messzeit=Uhr(schritt=0.01), bildrate=10, blick_vorgabe="iso"
    )
    qtbot.addWidget(f)
    f.resize(640, 480)
    f.show()
    f.zeichne(_daten(), AnimationsOptionen())
    f.abspielen()
    for _ in range(BILDZEIT_MINDEST + 2):
        f.takt()
    assert not f.langsam and f.bildzeit_median_s == pytest.approx(0.01)


class _ZeichenUhr:
    """Handgeführte Messzeit; das (ersetzte) Zeichnen verbraucht ``dauer_s`` Zeit."""

    def __init__(self, dauer_s: float) -> None:
        self.t = 0.0
        self.dauer_s = dauer_s

    def __call__(self) -> float:
        return self.t

    def zeichne(self, *args: Any, **kwargs: Any) -> None:
        self.t += self.dauer_s


def _flaeche_mit_zeichenzeit(
    qtbot: QtBot, monkeypatch: pytest.MonkeyPatch, bildrate: float, dauer_s: float
) -> tuple[AnimationsFlaeche, _ZeichenUhr]:
    mess = _ZeichenUhr(dauer_s)
    f = AnimationsFlaeche(
        THESIS_STIL, zeit=Uhr(), messzeit=mess, bildrate=bildrate, blick_vorgabe="iso"
    )
    qtbot.addWidget(f)
    f.resize(640, 480)
    f.show()
    qtbot.waitExposed(f)
    f.zeichne(_daten(), AnimationsOptionen())
    monkeypatch.setattr(animationsflaeche, "aktualisiere_animation", mess.zeichne)
    f.abspielen()
    return f, mess


def test_restintervall_haelt_den_abstand_der_bilder_beim_intervall(
    qtbot: QtBot, monkeypatch: pytest.MonkeyPatch
) -> None:
    f, mess = _flaeche_mit_zeichenzeit(qtbot, monkeypatch, bildrate=5, dauer_s=0.1)
    f.takt()
    # Abstand zweier Bilder = Zeichenzeit + gestartetes Restintervall = 1/Bildrate (200 ms);
    # mit dem vollen Intervall wären es 300 ms (Ist-Rate 3,3 statt 5 Bilder/s).
    assert f._timer.isActive() and f._timer.interval() == 100
    assert mess.dauer_s + f._timer.interval() / 1000.0 == pytest.approx(1.0 / 5)
    mess.dauer_s = 0.35  # Zeichnen länger als das Intervall: Restintervall nie negativ
    f.takt()
    assert f._timer.interval() == 0


def test_langsamer_slot_verkuerzt_das_restintervall(
    qtbot: QtBot, monkeypatch: pytest.MonkeyPatch
) -> None:
    f, mess = _flaeche_mit_zeichenzeit(qtbot, monkeypatch, bildrate=5, dauer_s=0.1)

    def langsamer_slot(_theta: float) -> None:
        mess.t += 0.06

    f.phase_geaendert.connect(langsamer_slot)
    f.takt()
    assert f._timer.interval() == 40  # 200 ms - 100 ms Zeichnen - 60 ms Slot


def test_langsam_wird_bei_zeichenzeit_nahe_dem_intervall_gemeldet(
    qtbot: QtBot, monkeypatch: pytest.MonkeyPatch
) -> None:
    f, _ = _flaeche_mit_zeichenzeit(qtbot, monkeypatch, bildrate=5, dauer_s=0.19)  # 190 von 200 ms
    meldungen: list[bool] = []
    f.langsam_geaendert.connect(meldungen.append)
    for _ in range(BILDZEIT_MINDEST):
        f.takt()
    assert f.langsam and meldungen == [True] and f.bildrate == 5


def test_langsam_meldet_auch_eine_zu_lange_bildperiode(
    qtbot: QtBot, monkeypatch: pytest.MonkeyPatch
) -> None:
    f, mess = _flaeche_mit_zeichenzeit(qtbot, monkeypatch, bildrate=5, dauer_s=0.05)
    for _ in range(BILDZEIT_MINDEST + 1):  # Zeichnen schnell, aber der Takt kommt zu spät
        f.takt()
        mess.t += 0.4
    assert f.bildperiode_median_s == pytest.approx(0.45) and f.langsam


def test_zeichenzeit_mit_reserve_ist_nicht_langsam_und_haelt_die_bildrate(
    qtbot: QtBot, monkeypatch: pytest.MonkeyPatch
) -> None:
    f, mess = _flaeche_mit_zeichenzeit(qtbot, monkeypatch, bildrate=5, dauer_s=0.1)
    for _ in range(BILDZEIT_MINDEST + 2):
        f.takt()
        mess.t += f._timer.interval() / 1000.0  # der Timer läuft das Restintervall ab
    assert f.bildperiode_median_s == pytest.approx(0.2) and not f.langsam


def test_bildrate_aendern_und_pruefen(bau: Any) -> None:
    f, _ = bau()
    f.setze_bildrate(20)
    assert f.bildrate == 20 and f._timer.interval() == 50
    for falsch in (0.0, -1.0, math.nan):
        with pytest.raises(ValueError, match="bildrate"):
            f.setze_bildrate(falsch)
    with pytest.raises(ValueError, match="bildrate"):
        AnimationsFlaeche(THESIS_STIL, bildrate=0)


# --- Beenden, Ausblenden, Größe ----------------------------------------------------------------


def test_timer_stoppt_beim_schliessen(bau: Any) -> None:
    f, _ = bau()
    f.abspielen()
    assert f._timer.isActive()
    f.close()
    assert not f._timer.isActive() and not f.laeuft and not f._neuzeichnen_timer.isActive()


def test_beende_ist_ohne_wiedergabe_harmlos(bau: Any) -> None:
    f, _ = bau()
    f.beende()
    f.beende()
    assert not f._timer.isActive()


def test_ausblenden_pausiert_die_wiedergabe_und_zeigen_setzt_nicht_fort(bau: Any) -> None:
    f, _ = bau()
    f.abspielen()
    f.hide()
    assert not f.laeuft and not f._timer.isActive()
    f.show()
    assert not f.laeuft


def test_abspielen_bei_ausgeblendeter_flaeche_startet_nichts(bau: Any) -> None:
    f, _ = bau()
    f.hide()
    assert not f.abspielen() and not f.laeuft and not f._timer.isActive()
    f.show()
    assert f.abspielen() and f._timer.isActive()


def test_ausblenden_stoppt_auch_das_neuzeichnen(bau: Any) -> None:
    f, _ = bau()
    f._neuzeichnen_timer.start()
    assert f._neuzeichnen_timer.isActive()
    f.hide()
    assert not f._neuzeichnen_timer.isActive()
    z = f.zeichnung
    f._gezeichnet_groesse = (0, 0)  # Größe "geändert"
    f._neuzeichnen()  # ausgeblendet: nichts zeichnen
    assert f.zeichnung is z


def test_groessenaenderung_pausiert_und_zeichnet_nach_stillstand_neu(
    bau: Any, qtbot: QtBot
) -> None:
    f, _ = bau()
    f.abspielen()
    f.resize(720, 520)
    QApplication.processEvents()
    assert not f.laeuft
    alt = f._gezeichnet_groesse
    qtbot.waitUntil(lambda: f._gezeichnet_groesse != alt, timeout=3000)
    assert f._gezeichnet_groesse == (f.canvas.width(), f.canvas.height())


def test_neuzeichnen_ohne_groessenaenderung_und_ohne_daten_tut_nichts(bau: Any) -> None:
    f, _ = bau()
    zeichnung = f.zeichnung
    f._neuzeichnen()
    assert f.zeichnung is zeichnung
    leer, _ = bau(zeichnen=False)
    leer._neuzeichnen()
    leer._groesse_geaendert()
    assert leer.zeichnung is None


def test_neuzeichnen_meldet_fehler(bau: Any, monkeypatch: pytest.MonkeyPatch) -> None:
    f, _ = bau()
    meldungen: list[str] = []
    f.fehler.connect(meldungen.append)

    def kaputt(*_a: Any, **_k: Any) -> None:
        raise RuntimeError("kaputt")

    monkeypatch.setattr(animationsflaeche, "zeichne_animation", kaputt)
    f._gezeichnet_groesse = (0, 0)
    f._neuzeichnen()
    assert meldungen == ["kaputt"]


# --- Aktualisieren, Leeren, Speichern, Fehler ---------------------------------------------------


def test_aktualisiere_teilweise_und_vollstaendig(bau: Any) -> None:
    f, _ = bau()
    z = f.zeichnung
    f.aktualisiere(AnimationsOptionen(ueberhoehung=5.0))  # Überhöhung: Teilaktualisierung
    assert f.zeichnung is z and z is not None and z.hilfsobjekte["skalierung"] == 5.0
    f.aktualisiere(AnimationsOptionen(ueberhoehung=5.0, farbe="betrag"))  # Aufbau: neu zeichnen
    assert f.zeichnung is not z and _optionen(f).farbe == "betrag"
    f.aktualisiere()  # ohne Angabe: Zustand der Fläche neu darstellen
    with pytest.raises(ValueError, match="Farbbereich"):
        f.aktualisiere(AnimationsOptionen(farbe="betrag", farbbereich=Bereich(von=5.0, bis=None)))
    assert _optionen(f).farbbereich == Bereich()  # Bild unverändert


def test_aktualisiere_und_speichere_ohne_zeichnung(bau: Any, tmp_path: Path) -> None:
    f, _ = bau(zeichnen=False)
    with pytest.raises(RuntimeError, match="keine Animation"):
        f.aktualisiere()
    with pytest.raises(RuntimeError, match="keine Animation"):
        f.speichere(tmp_path / "a.png", baue_stempel(dateiname="x.svd", ansicht="A", git_hash="1"))


def test_leere_haelt_an_und_loescht(bau: Any) -> None:
    f, _ = bau()
    f.abspielen()
    f.leere()
    assert not f.laeuft and f.zeichnung is None and f.figure.axes == []
    assert f.canvas.accessibleDescription() == "" and not f.abspielen()


def test_speichere_standbild_png_und_pdf(bau: Any, tmp_path: Path) -> None:
    f, _ = bau()
    f.uhr.setze_theta_grad(90.0)
    stempel = baue_stempel(dateiname="probe.svd", ansicht="Animation", git_hash="abc1234")
    for name, magic in (("bild.png", b"\x89PNG"), ("bild.pdf", b"%PDF")):
        z = f.speichere(tmp_path / name, stempel)
        assert (tmp_path / name).read_bytes()[:4] == magic
        assert any("θ = 90,0°" in t for t in z.hilfsobjekte["pflichtangaben"])
        assert scatter_positionen(z).shape[1] == 3
    assert f.zeichnung is not None and _achse(f)._axis3don  # Bildschirmfigur unverändert


def test_zeichenfehler_haelt_die_wiedergabe_an_und_meldet(
    bau: Any, monkeypatch: pytest.MonkeyPatch
) -> None:
    f, uhr = bau()
    meldungen: list[str] = []
    wechsel: list[bool] = []
    f.fehler.connect(meldungen.append)
    f.wiedergabe_geaendert.connect(wechsel.append)
    f.abspielen()

    def kaputt(*_a: Any, **_k: Any) -> None:
        raise RuntimeError("Zeichenfehler")

    monkeypatch.setattr(animationsflaeche, "aktualisiere_animation", kaputt)
    uhr.t = 1.0
    f.takt()
    assert meldungen == ["Zeichenfehler"] and not f.laeuft and not f._timer.isActive()
    assert wechsel == [True, False]


def test_zeichenfehler_ohne_wiedergabe_sendet_kein_wiedergabe_signal(
    bau: Any, monkeypatch: pytest.MonkeyPatch
) -> None:
    f, _ = bau()
    meldungen: list[str] = []
    wechsel: list[bool] = []
    f.fehler.connect(meldungen.append)
    f.wiedergabe_geaendert.connect(wechsel.append)

    def kaputt(*_a: Any, **_k: Any) -> None:
        raise RuntimeError("Zeichenfehler")

    monkeypatch.setattr(animationsflaeche, "aktualisiere_animation", kaputt)
    f.schritt(+1)  # Einzelschritt ohne laufende Wiedergabe
    assert meldungen == ["Zeichenfehler"] and wechsel == []


# --- Rückfallstufen (ADR-029, Plan 4.3) ---------------------------------------------------------


def test_stufe_l1_vereinfacht_auch_beim_ziehen_des_reglers(bau: Any) -> None:
    f, _ = bau(stufe=Stufe.L1)
    f.setze_theta_grad(100.0, ziehend=True)
    assert _optionen(f).vereinfacht and not _achse(f)._axis3don
    f.phase_losgelassen()
    assert not _optionen(f).vereinfacht and _achse(f)._axis3don


def test_stufe_l2_zeichnet_beim_loslassen_und_kennt_keine_wiedergabe(bau: Any) -> None:
    f, _ = bau(stufe=Stufe.L2)
    assert f.stufe is Stufe.L2 and not f.abspielen() and not f.laeuft
    z = f.zeichnung
    azim0 = _achse(f).azim
    start = QPoint(100, 100)
    QTest.mousePress(f.canvas, Qt.MouseButton.LeftButton, Qt.KeyboardModifier.NoModifier, start)
    QTest.mouseMove(f.canvas, start + QPoint(40, 0))
    assert _optionen(f).blick.azim_grad == pytest.approx(azim0)  # nicht voll gezeichnet
    assert f.blick.azim_grad == pytest.approx(azim0 + GRAD_JE_PIXEL * 40)
    QTest.mouseRelease(
        f.canvas, Qt.MouseButton.LeftButton, Qt.KeyboardModifier.NoModifier, start + QPoint(40, 0)
    )
    assert _achse(f).azim == pytest.approx(azim0 + GRAD_JE_PIXEL * 40) and f.zeichnung is z
    gemeldet: list[float] = []
    f.phase_geaendert.connect(gemeldet.append)
    f.setze_theta_grad(80.0, ziehend=True)  # Regler ziehen: erst beim Loslassen zeichnen
    assert _optionen(f).theta_rad == 0.0 and len(gemeldet) == 1
    f.phase_losgelassen()
    assert math.degrees(_optionen(f).theta_rad) == pytest.approx(80.0)


def test_stufe_l2_zeigt_beim_drehen_ein_achsen_skelett_ohne_punkte(bau: Any) -> None:
    f, _ = bau(stufe=Stufe.L2)
    ax = _achse(f)
    punkte = f.zeichnung.marker["punkte"]
    linien_vorher = len(ax.lines)
    lims = (ax.get_xlim3d(), ax.get_ylim3d(), ax.get_zlim3d())
    start = QPoint(100, 100)
    QTest.mousePress(f.canvas, Qt.MouseButton.LeftButton, Qt.KeyboardModifier.NoModifier, start)
    QTest.mouseMove(f.canvas, start + QPoint(40, 0))
    assert len(ax.lines) == linien_vorher + 15  # 12 Kanten + 3 Achsen
    assert not punkte.get_visible() and not ax._axis3don
    assert ax.azim == pytest.approx(f.blick.azim_grad)  # Skelett folgt dem Blick
    assert np.allclose(
        [*ax.get_xlim3d(), *ax.get_ylim3d(), *ax.get_zlim3d()], [v for g in lims for v in g]
    )
    QTest.mouseMove(f.canvas, start + QPoint(60, 10))
    assert len(ax.lines) == linien_vorher + 15  # nicht noch einmal angelegt
    QTest.mouseRelease(
        f.canvas, Qt.MouseButton.LeftButton, Qt.KeyboardModifier.NoModifier, start + QPoint(60, 10)
    )
    assert len(ax.lines) == linien_vorher and punkte.get_visible() and ax._axis3don


def test_stufe_l0_zeigt_kein_skelett(bau: Any) -> None:
    f, _ = bau()
    n = len(_achse(f).lines)
    _ziehe(f, 30, 0)
    assert len(_achse(f).lines) == n and f.zeichnung.marker["punkte"].get_visible()


def test_zeichnen_waehrend_des_skeletts_setzt_es_zurueck(bau: Any) -> None:
    f, _ = bau(stufe=Stufe.L2)
    start = QPoint(100, 100)
    QTest.mousePress(f.canvas, Qt.MouseButton.LeftButton, Qt.KeyboardModifier.NoModifier, start)
    QTest.mouseMove(f.canvas, start + QPoint(20, 0))
    assert f._skelett
    f.zeichne(_daten(), AnimationsOptionen())
    assert not f._skelett
    QTest.mouseMove(f.canvas, start + QPoint(30, 0))  # neues Skelett auf der neuen Figure
    assert f._skelett
    f.leere()
    assert not f._skelett
    QTest.mouseRelease(f.canvas, Qt.MouseButton.LeftButton, Qt.KeyboardModifier.NoModifier, start)


def _beginne_ziehen_l2(f: AnimationsFlaeche) -> None:
    start = QPoint(100, 100)
    QTest.mousePress(f.canvas, Qt.MouseButton.LeftButton, Qt.KeyboardModifier.NoModifier, start)
    QTest.mouseMove(f.canvas, start + QPoint(30, 0))
    assert f._skelett and f._zieht


def _ist_wiederhergestellt(f: AnimationsFlaeche, sichtbar: dict[str, bool]) -> bool:
    z = f.zeichnung
    assert z is not None
    return (
        not f._skelett
        and not f._zieht
        and f._letzte_pos is None
        and bool(_achse(f)._axis3don)
        and {n: bool(m.get_visible()) for n, m in z.marker.items()} == sichtbar
    )


def test_skelett_blendet_alle_punktmarker_aus_und_stellt_sie_wieder_her(bau: Any) -> None:
    f, _ = bau(stufe=Stufe.L2)
    z = f.zeichnung
    assert z is not None
    z.marker["ruhelage"].set_visible(True)
    vorher = {n: bool(m.get_visible()) for n, m in z.marker.items()}
    assert len(vorher) >= 2
    _beginne_ziehen_l2(f)
    assert not any(m.get_visible() for m in z.marker.values())
    QTest.mouseRelease(f.canvas, Qt.MouseButton.LeftButton, Qt.KeyboardModifier.NoModifier)
    assert _ist_wiederhergestellt(f, vorher)


def test_ausblenden_waehrend_des_ziehens_raeumt_das_skelett_ab(bau: Any) -> None:
    f, _ = bau(stufe=Stufe.L2)
    vorher = {n: bool(m.get_visible()) for n, m in f.zeichnung.marker.items()}
    _beginne_ziehen_l2(f)
    f.hide()
    assert _ist_wiederhergestellt(f, vorher)


def test_fokusverlust_waehrend_des_ziehens_raeumt_ab_und_zeichnet_voll(bau: Any) -> None:
    f, _ = bau(stufe=Stufe.L2)
    vorher = {n: bool(m.get_visible()) for n, m in f.zeichnung.marker.items()}
    _beginne_ziehen_l2(f)
    # Offscreen ist das Fenster nicht aktiv: Fokusverlust wie in den Fokustests senden
    QApplication.sendEvent(f.canvas, QFocusEvent(QEvent.Type.FocusOut))
    assert _ist_wiederhergestellt(f, vorher)
    assert _optionen(f).blick.azim_grad == pytest.approx(f.blick.azim_grad)  # voll gezeichnet


def test_schliessen_waehrend_des_ziehens_raeumt_ab(bau: Any) -> None:
    f, _ = bau(stufe=Stufe.L2)
    vorher = {n: bool(m.get_visible()) for n, m in f.zeichnung.marker.items()}
    _beginne_ziehen_l2(f)
    f.close()
    assert _ist_wiederhergestellt(f, vorher)


def test_phasenaenderung_waehrend_des_skeletts_stellt_die_darstellung_wieder_her(bau: Any) -> None:
    f, _ = bau(stufe=Stufe.L2)
    vorher = {n: bool(m.get_visible()) for n, m in f.zeichnung.marker.items()}
    _beginne_ziehen_l2(f)
    f.setze_theta_grad(45.0)
    assert not f._skelett and bool(_achse(f)._axis3don)
    assert {n: bool(m.get_visible()) for n, m in f.zeichnung.marker.items()} == vorher
    QTest.mouseRelease(f.canvas, Qt.MouseButton.LeftButton, Qt.KeyboardModifier.NoModifier)


def test_einblenden_zeichnet_bei_geaenderter_groesse_neu(bau: Any, qtbot: QtBot) -> None:
    f, _ = bau()
    gezeichnet = f._gezeichnet_groesse
    f.resize(800, 600)
    f.hide()  # Resize kurz vor dem Ausblenden: Neuzeichnen-Timer wird gestoppt
    assert not f._neuzeichnen_timer.isActive()
    f.show()
    qtbot.waitUntil(
        lambda: f._gezeichnet_groesse == (f.canvas.width(), f.canvas.height()), timeout=3000
    )
    assert f._gezeichnet_groesse != gezeichnet


def test_optionen_der_aufrufer_werden_durch_den_zustand_der_flaeche_ersetzt(bau: Any) -> None:
    f, _ = bau()
    f.uhr.setze_theta_grad(33.0)
    f.zeichne(
        _daten(),
        replace(AnimationsOptionen(), theta_rad=1.0, blick=BLICK_VORGABEN["yz"], vereinfacht=True),
    )
    assert math.degrees(_optionen(f).theta_rad) == pytest.approx(33.0)
    assert f.blick == BLICK_VORGABEN["iso"] and not _optionen(f).vereinfacht
