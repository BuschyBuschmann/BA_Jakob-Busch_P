"""Fadenkreuz-Cursor mit Blitting für die Ansichten 1 bis 3 (P-AUSW T4, UI-13, ADR-021).

Der Cursor ist eine senkrechte Linie durch alle Achsen der Figure, die auf die **nächste Linie
der Frequenzachse** einrastet. Er wird nur über Blitting bewegt (``copy_from_bbox``,
``restore_region``, ``blit``): Der Hintergrund wird nach jedem vollständigen Zeichnen
(``draw_event``) neu aufgenommen, beim Bewegen nur die Linie über den gemerkten Hintergrund
gelegt (ADR-021: 0,3 ms gegen 27 ms ohne Blitting).

Fällt der Blitting-Pfad aus (Canvas ohne Unterstützung oder Ausnahme beim Blitten), bleibt der
Cursor aus, ohne dass ein Fehler erscheint: die Zahlenfelder genügen (Brief K-AUSW Abschnitt 4).
Die Linien gehören **nicht** zu den Kindern der Achsen (sie erscheinen weder in ``ax.lines``
noch in einem gespeicherten Bild).

Das Modul importiert nur matplotlib und NumPy, kein Qt: Es läuft mit jedem Agg-Canvas und ist
ohne Oberfläche testbar.
"""

from __future__ import annotations

import logging
from collections.abc import Sequence
from typing import Any

import numpy as np
import numpy.typing as npt
from matplotlib.axes import Axes
from matplotlib.backends.backend_agg import FigureCanvasAgg
from matplotlib.lines import Line2D

__all__ = ["FadenkreuzCursor", "naechste_linie"]

_log = logging.getLogger(__name__)

LINIENBREITE_PT = 1.0
"""Linienbreite des Cursors in pt."""


def naechste_linie(linien_hz: npt.ArrayLike, f_hz: float) -> int:
    """Index der Linie der Frequenzachse, die ``f_hz`` am nächsten liegt (aufsteigend sortiert).

    Parameters
    ----------
    linien_hz : array_like
        Frequenzachse in Hz, aufsteigend, nicht leer.
    f_hz : float
        Gesuchte Frequenz in Hz.

    Raises
    ------
    ValueError
        Leere Achse oder ``f_hz`` nicht endlich.
    """
    achse = np.asarray(linien_hz, dtype=np.float64)
    if achse.size == 0:
        raise ValueError("Frequenzachse ist leer")
    if not np.isfinite(f_hz):
        raise ValueError(f"Frequenz nicht endlich: {f_hz}")
    k = int(np.searchsorted(achse, f_hz))
    if k <= 0:
        return 0
    if k >= achse.size:
        return int(achse.size - 1)
    return k if achse[k] - f_hz < f_hz - achse[k - 1] else k - 1


class FadenkreuzCursor:
    """Senkrechte Cursorlinie über Blitting.

    Parameters
    ----------
    canvas : FigureCanvasAgg
        Canvas der Figure (Agg-basiert, z. B. ``FigureCanvasQTAgg``).
    farbe : str
        Linienfarbe.

    Notes
    -----
    Ablauf: :meth:`anlegen` nach dem Füllen der Figure und **vor** dem Zeichnen; danach
    :meth:`setze` bzw. :meth:`schritt`. :meth:`abbauen` vor dem Leeren der Figure.
    """

    def __init__(self, canvas: FigureCanvasAgg, farbe: str = "#595959") -> None:
        self._canvas = canvas
        self._farbe = farbe
        self._achsen: tuple[Axes, ...] = ()
        self._linien: list[Line2D] = []
        self._linien_hz: npt.NDArray[np.float64] | None = None
        self._hintergrund: Any = None
        self._k: int | None = None
        self._merk_hz: float | None = None
        self._defekt = False
        canvas.mpl_connect("draw_event", self._bei_zeichnen)

    # --- Zustand ---------------------------------------------------------------------------

    @property
    def verfuegbar(self) -> bool:
        """``True``, wenn der Cursor angelegt ist und das Blitting funktioniert."""
        return bool(self._linien) and not self._defekt

    @property
    def index(self) -> int | None:
        """Linienindex der Cursorposition (``None`` = noch nicht gesetzt)."""
        return self._k

    @property
    def frequenz_hz(self) -> float | None:
        """Frequenz der Cursorposition in Hz (``None`` = noch nicht gesetzt)."""
        if self._k is None or self._linien_hz is None:
            return None
        return float(self._linien_hz[self._k])

    @property
    def linien(self) -> tuple[Line2D, ...]:
        """Die Cursorlinien (eine je Achse), für Tests."""
        return tuple(self._linien)

    @property
    def linien_hz(self) -> npt.NDArray[np.float64] | None:
        """Frequenzachse, auf die der Cursor einrastet (``None`` = kein Cursor angelegt)."""
        return self._linien_hz

    # --- Aufbau ----------------------------------------------------------------------------

    def anlegen(self, achsen: Sequence[Axes], linien_hz: npt.ArrayLike | None) -> None:
        """Legt je Achse eine unsichtbare, animierte Cursorlinie an.

        Die gemerkte Frequenz bleibt erhalten (Neuzeichnen nach Wechsel von Punkt oder Größe, auch
        über eine Ansicht ohne Cursor hinweg) und rastet auf die nächste Linie der neuen Achse ein.

        Parameters
        ----------
        achsen : sequence of Axes
            Achsen mit gemeinsamer Frequenzachse (x).
        linien_hz : array_like or None
            Frequenzachse der Daten; ``None`` oder leer = kein Cursor (z. B. Ansicht 4).
        """
        self.abbauen()
        self._k = None
        if linien_hz is None or np.size(linien_hz) == 0 or not achsen:
            return
        if not getattr(self._canvas, "supports_blit", False) or self._defekt:
            return
        self._linien_hz = np.asarray(linien_hz, dtype=np.float64)
        self._achsen = tuple(achsen)
        for ax in self._achsen:
            linie = Line2D(
                [0.0, 0.0],
                [0.0, 1.0],
                transform=ax.get_xaxis_transform(),
                color=self._farbe,
                linewidth=LINIENBREITE_PT,
                animated=True,
                visible=False,
            )
            linie.set_figure(ax.figure)
            linie.axes = ax
            linie.set_clip_box(ax.bbox)
            self._linien.append(linie)
        if self._merk_hz is not None:
            self._k = naechste_linie(self._linien_hz, self._merk_hz)
        self._positioniere()

    def abbauen(self) -> None:
        """Entfernt die Cursorlinien und den gemerkten Hintergrund (Figure wird geleert)."""
        self._linien = []
        self._achsen = ()
        self._linien_hz = None
        self._hintergrund = None

    def vergiss(self) -> None:
        """Verwirft die gemerkte Position (neue Datei)."""
        self._k = None
        self._merk_hz = None
        self._positioniere()

    # --- Bewegen ---------------------------------------------------------------------------

    def setze(self, f_hz: float) -> float | None:
        """Setzt den Cursor auf die Linie, die ``f_hz`` am nächsten liegt.

        Returns
        -------
        float or None
            Frequenz der Linie in Hz; ``None``, wenn der Cursor nicht verfügbar ist.
        """
        if not self.verfuegbar or self._linien_hz is None:
            return None
        self._merke(naechste_linie(self._linien_hz, f_hz))
        self._blitte()
        return self.frequenz_hz

    def schritt(self, anzahl: int) -> float | None:
        """Bewegt den Cursor um ``anzahl`` Linien, begrenzt auf den sichtbaren Frequenzbereich.

        Ohne bisherige Position beginnt er in der Mitte des sichtbaren Bereichs.

        Returns
        -------
        float or None
            Neue Frequenz in Hz; ``None``, wenn der Cursor nicht verfügbar ist.
        """
        if not self.verfuegbar or self._linien_hz is None:
            return None
        links, rechts = sorted(self._achsen[0].get_xlim())
        erste = int(np.searchsorted(self._linien_hz, links, side="left"))
        letzte = int(np.searchsorted(self._linien_hz, rechts, side="right")) - 1
        erste = min(erste, self._linien_hz.size - 1)
        letzte = max(letzte, erste)
        neu = (erste + letzte) // 2 if self._k is None else self._k + anzahl
        self._merke(min(max(neu, erste), letzte))
        self._blitte()
        return self.frequenz_hz

    # --- Intern ----------------------------------------------------------------------------

    def _merke(self, k: int) -> None:
        """Setzt die Position auf die Linie ``k`` und merkt ihre Frequenz."""
        assert self._linien_hz is not None
        self._k = k
        self._merk_hz = float(self._linien_hz[k])
        self._positioniere()

    def _positioniere(self) -> None:
        f = self.frequenz_hz
        for linie in self._linien:
            if f is None:
                linie.set_visible(False)
            else:
                linie.set_xdata([f, f])
                linie.set_visible(True)

    def _zeichne_linien(self) -> None:
        for ax, linie in zip(self._achsen, self._linien, strict=True):
            if linie.get_visible():
                ax.draw_artist(linie)

    def _bei_zeichnen(self, _ereignis: object) -> None:
        """Nimmt nach jedem vollständigen Zeichnen den Hintergrund neu auf (draw_event)."""
        if not self._linien or self._defekt:
            return
        try:
            self._hintergrund = self._canvas.copy_from_bbox(  # type: ignore[no-untyped-call]
                self._canvas.figure.bbox
            )
            self._zeichne_linien()
        except Exception:
            self._ausfall()

    def _blitte(self) -> None:
        if self._hintergrund is None or self._defekt:
            return  # noch nicht gezeichnet: das draw_event zeichnet die Linie nach
        try:
            self._canvas.restore_region(self._hintergrund)  # type: ignore[no-untyped-call]
            self._zeichne_linien()
            self._canvas.blit(self._canvas.figure.bbox)
        except Exception:
            self._ausfall()

    def _ausfall(self) -> None:
        """Blitting funktioniert nicht: Cursor aus, ohne Fehlermeldung (nur Protokoll)."""
        _log.warning("Blitting für den Cursor nicht verfügbar; Cursor aus", exc_info=True)
        self._defekt = True
        for linie in self._linien:
            linie.set_visible(False)
