"""Gemeinsame Bausteine der Zeichenfunktionen: Rückgabeobjekt, Achsenstil, Kennzeichen.

Keine Qt-, keine ``pyplot``-Importe (ADR-021): Die Zeichenfunktionen füllen eine übergebene
:class:`matplotlib.figure.Figure`. Sie zeichnen **keinen Diagrammtitel** (KONVENTIONEN) und
**keinen Arbeitsstempel** (:mod:`.bild`).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Literal

from matplotlib.axes import Axes
from matplotlib.figure import Figure
from matplotlib.layout_engine import ConstrainedLayoutEngine
from matplotlib.lines import Line2D
from matplotlib.text import Text

from .formate import dezimalkomma_formatter
from .stil import Plotstil

__all__ = [
    "Ansicht",
    "Skala",
    "Zeichnung",
    "achse_pt",
    "constrained_layout",
    "kennzeichen_anbringen",
    "layout_rect",
    "platzhalter_anbringen",
    "setze_achsenstil",
]

Skala = Literal["linear", "log"]
"""Amplitudenskala. „dB“ gibt es nicht: In der Datei existiert keine Referenzgröße (0 dB)."""


class Ansicht(Enum):
    """Die vier Ansichten der Auswertungsoberfläche."""

    SPEKTRUM = 1
    FRF = 2
    SPITZEN = 3
    SCHWINGFORM = 4


@dataclass(eq=False)
class Zeichnung:
    """Rückgabeobjekt einer Zeichenfunktion (Hilfsobjekte für Oberfläche und Tests).

    Attributes
    ----------
    figure : Figure
        Die gefüllte Figure.
    achsen : tuple of Axes
        Hauptachsen von oben nach unten (ohne Farbleiste und Legendenhilfen).
    linien : dict
        Datenlinien je Schlüssel (z. B. ``"X"``, ``"H1"``, ``"kohaerenz"``).
    marker : dict
        Marker-Artists je Schlüssel (``"spitzen"``, ``"gewaehlt"``, ``"bezug"`` …).
    hilfsobjekte : dict
        Weitere Artists (Bänder, Farbleiste, Kreislegende, Pfeile …).
    texte : list of Text
        Zusatztexte der Zeichenfunktion (Platzhalter, Kennzeichen, Beschriftung der Spitze).
    hinweise : tuple of str
        Anzeigehinweise für die Oberfläche (z. B. Formel des Mittels), nicht im Bild.
    """

    figure: Figure
    achsen: tuple[Axes, ...]
    linien: dict[str, Line2D] = field(default_factory=dict)
    marker: dict[str, Any] = field(default_factory=dict)
    hilfsobjekte: dict[str, Any] = field(default_factory=dict)
    texte: list[Text] = field(default_factory=list)
    hinweise: tuple[str, ...] = ()

    def alle_texte(self) -> list[str]:
        """Alle sichtbaren Texte der Figure (Achsentitel, Ticks nach Zeichnen, Legenden, Texte)."""
        texte = [t.get_text() for t in self.figure.findobj(Text) if t.get_visible()]
        return [t for t in texte if t]


def layout_rect(fig: Figure) -> tuple[float, float, float, float]:
    """Nutzbares Rechteck der Figure ``(x0, y0, Breite, Höhe)`` in Figure-Anteilen.

    Das Arbeitsbild reserviert unten Platz für den Stempel (``rect`` des Constrained Layouts,
    siehe :func:`constrained_layout`); ohne Engine ist es die ganze Figure.
    """
    engine = fig.get_layout_engine()
    rect = engine.get().get("rect") if isinstance(engine, ConstrainedLayoutEngine) else None
    if rect is None:
        return (0.0, 0.0, 1.0, 1.0)
    return (float(rect[0]), float(rect[1]), float(rect[2]), float(rect[3]))


def constrained_layout(fig: Figure) -> None:
    """Setzt das Constrained Layout und behält dabei den ``rect`` einer vorhandenen Engine.

    Der Aufrufer (Arbeitsbild mit Stempel) legt den Rand für den Stempel **vor** dem Zeichnen
    fest. Die Zeichenfunktionen messen Größen in pt (Pfeile, Marker, Beschriftungsstreifen) und
    brauchen dafür das endgültige Layout.
    """
    alt = fig.get_layout_engine()
    rect = alt.get().get("rect") if isinstance(alt, ConstrainedLayoutEngine) else None
    if rect is None:
        fig.set_layout_engine("constrained")
    else:
        fig.set_layout_engine("constrained", rect=rect)


def achse_pt(ax: Axes) -> tuple[float, float]:
    """Breite und Höhe der Achsenfläche in pt (nach ``fig.draw_without_rendering()``)."""
    box = ax.get_window_extent()
    faktor = 72.0 / ax.figure.dpi
    return float(box.width) * faktor, float(box.height) * faktor


def setze_achsenstil(
    ax: Axes, stil: Plotstil, *, x_komma: bool = True, y_komma: bool = True
) -> None:
    """Gitter, Rahmen, Tickformat (Dezimalkomma) und Schrift der Achse."""
    ax.set_facecolor(stil.flaeche)
    ax.grid(True, color=stil.gitter, linewidth=0.6)
    ax.set_axisbelow(True)
    for spine in ax.spines.values():
        spine.set_color(stil.achse)
    ax.tick_params(colors=stil.achse, labelsize=stil.schrift_pt)
    if x_komma:
        ax.xaxis.set_major_formatter(dezimalkomma_formatter(dezimalkomma=stil.dezimalkomma))
    if y_komma:
        ax.yaxis.set_major_formatter(dezimalkomma_formatter(dezimalkomma=stil.dezimalkomma))


def kennzeichen_anbringen(ax: Axes, stil: Plotstil, text: str) -> Text:
    """Kennzeichen „⚠ unbestätigt …“ im Kopf der Achse (Symbol plus Wort, nie nur Farbe)."""
    return ax.text(
        0.0,
        1.0,
        f"{stil.warn_symbol} {text}",
        transform=ax.transAxes,
        ha="left",
        va="bottom",
        fontsize=stil.schrift_pt,
        color=stil.achse,
        bbox={
            "boxstyle": "square,pad=0.25",
            "facecolor": stil.warn_bg,
            "edgecolor": stil.warn_rand,
            "linewidth": 1.0,
        },
    )


def platzhalter_anbringen(ax: Axes, stil: Plotstil, text: str) -> Text:
    """Platzhaltertext mittig in der Achse (statt Daten)."""
    return ax.text(
        0.5,
        0.5,
        text,
        transform=ax.transAxes,
        ha="center",
        va="center",
        fontsize=stil.schrift_pt,
        color=stil.text_gedaempft,
        wrap=True,
    )
