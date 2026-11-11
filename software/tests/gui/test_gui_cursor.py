"""Fadenkreuz-Cursor (Blitting) und Arbeitsbild-Vorbereitung ohne Qt (P-AUSW T4, UI-13/17)."""

from __future__ import annotations

import numpy as np
import pytest
from matplotlib.backends.backend_agg import FigureCanvasAgg
from matplotlib.figure import Figure

from ldv_automation.darstellung import Ansicht
from ldv_automation.darstellung.spitzen import SpitzenOptionen
from ldv_automation.gui.arbeitsbild import bild_optionen
from ldv_automation.gui.cursor import FadenkreuzCursor, naechste_linie

F = 0.5 * np.arange(1, 101)  # 0,5 … 50 Hz


def _aufbau(n_achsen: int = 1) -> tuple[Figure, FigureCanvasAgg, FadenkreuzCursor, list]:  # type: ignore[type-arg]
    fig = Figure()
    canvas = FigureCanvasAgg(fig)
    achsen = list(fig.subplots(n_achsen, 1, sharex=True, squeeze=False).ravel())
    for ax in achsen:
        ax.plot(F, np.sin(F))
    cur = FadenkreuzCursor(canvas)
    cur.anlegen(achsen, F)
    canvas.draw()  # type: ignore[no-untyped-call]
    return fig, canvas, cur, achsen


def test_naechste_linie_raster_und_raender() -> None:
    assert naechste_linie(F, 7.3) == 14  # 7,5 Hz
    assert naechste_linie(F, 7.24) == 13  # 7,0 Hz
    assert naechste_linie(F, -5.0) == 0 and naechste_linie(F, 1e6) == 99
    with pytest.raises(ValueError, match="leer"):
        naechste_linie([], 1.0)
    with pytest.raises(ValueError, match="endlich"):
        naechste_linie(F, float("nan"))


def test_cursor_rastet_ein_ohne_kinder_der_achse() -> None:
    _fig, _c, cur, achsen = _aufbau(3)
    assert cur.verfuegbar and cur.frequenz_hz is None
    assert cur.setze(7.3) == 7.5 and cur.index == 14
    assert [float(np.asarray(lin.get_xdata())[0]) for lin in cur.linien] == [
        7.5,
        7.5,
        7.5,
    ]  # in allen Achsen
    assert all(len(ax.lines) == 1 for ax in achsen)  # keine Cursorlinie unter den Linien
    assert all(lin.get_animated() for lin in cur.linien)


def test_cursor_schritte_und_sichtbarer_bereich() -> None:
    _f, _c, cur, achsen = _aufbau()
    achsen[0].set_xlim(10.0, 20.0)
    assert cur.schritt(1) == pytest.approx(15.0)  # Start in der Mitte des sichtbaren Bereichs
    assert cur.schritt(1) == pytest.approx(15.5)
    assert cur.schritt(10) == pytest.approx(20.0)  # Umschalt: zehn Linien, an der Grenze gestoppt
    assert cur.schritt(10) == pytest.approx(20.0)
    assert cur.schritt(-100) == pytest.approx(10.0)


def test_cursor_bleibt_ueber_neu_anlegen_und_vergiss() -> None:
    _fig, _canvas, cur, achsen = _aufbau()
    cur.setze(12.0)
    cur.anlegen([achsen[0]], None)  # Ansicht ohne Frequenzachse (Schwingform)
    assert not cur.verfuegbar and cur.setze(5.0) is None and cur.schritt(1) is None
    cur.anlegen([achsen[0]], F)
    assert cur.frequenz_hz == 12.0
    cur.vergiss()
    assert cur.frequenz_hz is None and all(not lin.get_visible() for lin in cur.linien)


def test_cursor_zeichnet_per_blitting(monkeypatch: pytest.MonkeyPatch) -> None:
    _f, canvas, cur, _a = _aufbau()
    aufrufe: list[str] = []
    orig_restore, orig_blit = canvas.restore_region, canvas.blit

    def restore(region: object) -> None:
        aufrufe.append("restore")
        orig_restore(region)  # type: ignore[no-untyped-call]

    def blit(bbox: object = None) -> None:
        aufrufe.append("blit")
        orig_blit(bbox)  # type: ignore[arg-type]

    monkeypatch.setattr(canvas, "restore_region", restore)
    monkeypatch.setattr(canvas, "blit", blit)
    cur.setze(3.0)
    cur.setze(4.0)
    assert aufrufe == ["restore", "blit", "restore", "blit"]  # nur Blitten, kein volles Zeichnen


def test_cursor_aus_ohne_fehler_wenn_blitting_ausfaellt(monkeypatch: pytest.MonkeyPatch) -> None:
    _f, canvas, cur, _a = _aufbau()

    def kaputt(_region: object) -> None:
        raise RuntimeError("kein Blitting")

    monkeypatch.setattr(canvas, "restore_region", kaputt)
    cur.setze(3.0)  # darf nicht werfen
    assert not cur.verfuegbar
    assert cur.setze(4.0) is None


def test_cursor_aus_wenn_canvas_kein_blitting_kann(monkeypatch: pytest.MonkeyPatch) -> None:
    fig = Figure()
    canvas = FigureCanvasAgg(fig)
    monkeypatch.setattr(type(canvas), "supports_blit", False, raising=False)
    ax = fig.add_subplot()
    cur = FadenkreuzCursor(canvas)
    cur.anlegen([ax], F)
    canvas.draw()  # type: ignore[no-untyped-call]
    assert not cur.verfuegbar and cur.setze(5.0) is None  # still aus, kein Fehler


def test_cursor_defekt_beim_draw_event(monkeypatch: pytest.MonkeyPatch) -> None:
    fig = Figure()
    canvas = FigureCanvasAgg(fig)
    ax = fig.add_subplot()
    cur = FadenkreuzCursor(canvas)
    cur.anlegen([ax], F)

    def kaputt(_bbox: object) -> None:
        raise RuntimeError("kein copy_from_bbox")

    monkeypatch.setattr(canvas, "copy_from_bbox", kaputt)
    canvas.draw()  # type: ignore[no-untyped-call]
    assert not cur.verfuegbar


def test_bild_optionen_ansicht_3_nimmt_voreinstellung_der_zeichenfunktion() -> None:
    gui = SpitzenOptionen(skala="linear", beschriftung_im_bild=False, legende_im_bild=False)
    bild = bild_optionen(Ansicht.SPITZEN, gui)
    assert isinstance(bild, SpitzenOptionen)
    assert bild.beschriftung_im_bild and bild.legende_im_bild and bild.skala == "linear"
    sonst = object()
    assert bild_optionen(Ansicht.SPEKTRUM, sonst) is sonst
