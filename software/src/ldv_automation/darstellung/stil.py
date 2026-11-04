"""Plotstil der Zeichenfunktionen (P-AUSW T2, ADR-021).

Die Zeichenfunktionen kennen keine Oberflächen-Tokens: Sie bekommen einen :class:`Plotstil`.
Die Oberfläche baut ihn aus ``gui/tokens.py`` (Farben bleiben nur dort), das Thesis-Skript
nimmt :data:`THESIS_STIL` (Graustufen, 9 pt). So nutzen beide dieselbe Zeichenfunktion.

Linienarten tragen die Unterscheidung der Serien, nicht die Farbe (KONVENTIONEN,
Abbildungsregeln: Graustufendruck, kein Gelb, Rot-Grün-Schwäche).
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from matplotlib import colormaps
from matplotlib.colors import Colormap, LinearSegmentedColormap

__all__ = [
    "LINIENARTEN",
    "THESIS_STIL",
    "ZYKLISCHE_SKALA",
    "Plotstil",
]

LINIENARTEN: tuple[str, ...] = ("-", "--", ":", "-.")
"""Durchgezogen, gestrichelt, punktiert, Strichpunkt (paarweise verschieden)."""

ZYKLISCHE_SKALA = "twilight"
"""Zyklische Farbskala der Phase (Schwingform, Ansicht 4).

``twilight`` ist eine in matplotlib enthaltene, wahrnehmungsgleichmäßige zyklische Skala:
Anfang und Ende haben dieselbe Farbe (Abweichung höchstens 2,3·10⁻³ je Farbkanal, nicht
sichtbar), bei ±180° gibt es also keinen Sprung. Anders als ``hsv`` oder ``jet`` hat sie keinen
Regenbogenverlauf mit Helligkeitssprüngen. In Graustufen ist sie **nicht** eindeutig (eine
stetige Helligkeit auf dem Kreis nimmt jeden Wert mindestens zweimal an, FA-AUSW F-4c); die
Phase steht deshalb zusätzlich im Pfeilwinkel."""


@dataclass(frozen=True, kw_only=True)
class Plotstil:
    """Darstellungsparameter der Zeichenfunktionen.

    Attributes
    ----------
    haupt : str
        Farbe der ersten Kurve, der Marker und des Verlaufs-Dunkelendes.
    gitter, achse, flaeche : str
        Gitter-, Achsen-/Text- und Flächenfarbe (Hintergrund).
    text_gedaempft : str
        Nebentext (Konventionen, Platzhalter).
    band : str
        Schattierung von Frequenzbändern.
    warn_bg, warn_rand : str
        Hintergrund und Rand der Kennzeichnung „unbestätigt“.
    serienfarben : tuple of str
        Farben der Serien, im Graustufendruck unterscheidbar; die Linienart unterscheidet
        zusätzlich.
    linienarten : tuple of str
        Linienarten je Serie, paarweise verschieden.
    verlauf_hell : str
        Hellstes Ende des Einfarbverlaufs der Betragsfüllung (Ansicht 4).
    schrift_pt : float
        Schriftgröße in pt (Achsen, Ticks, Legende).
    schriftfamilie : tuple of str
        Schriftfamilien in Rückfallreihenfolge.
    linienbreite_pt : float
        Breite der Kurven in pt.
    dezimalkomma : bool
        Dezimalkomma statt Dezimalpunkt in Tickbeschriftungen und Texten.
    warn_symbol : str
        Symbol der Kennzeichnung „unbestätigt“ (Oberfläche: ``tokens.symbol("warnung")``).
    """

    haupt: str = "#000000"
    gitter: str = "#CCCCCC"
    achse: str = "#000000"
    flaeche: str = "#FFFFFF"
    text_gedaempft: str = "#555555"
    band: str = "#E0E0E0"
    warn_bg: str = "#EEEEEE"
    warn_rand: str = "#000000"
    serienfarben: tuple[str, ...] = ("#000000", "#333333", "#666666", "#808080")
    linienarten: tuple[str, ...] = LINIENARTEN
    verlauf_hell: str = "#F2F2F2"
    schrift_pt: float = 9.0
    schriftfamilie: tuple[str, ...] = ("DejaVu Sans",)
    linienbreite_pt: float = 1.0
    dezimalkomma: bool = True
    warn_symbol: str = "⚠"

    def __post_init__(self) -> None:
        if len(set(self.linienarten)) != len(self.linienarten) or not self.linienarten:
            raise ValueError(
                f"linienarten müssen nicht leer und paarweise verschieden sein: {self.linienarten}"
            )
        if not self.serienfarben:
            raise ValueError("serienfarben darf nicht leer sein")
        if not self.schrift_pt > 0 or not self.linienbreite_pt > 0:
            raise ValueError("schrift_pt und linienbreite_pt müssen > 0 sein")

    def linienart(self, i: int) -> str:
        """Linienart der Serie ``i`` (zyklisch; paarweise verschieden für ``i < len``)."""
        return self.linienarten[i % len(self.linienarten)]

    def serienfarbe(self, i: int) -> str:
        """Farbe der Serie ``i`` (zyklisch)."""
        return self.serienfarben[i % len(self.serienfarben)]

    def verlauf(self) -> Colormap:
        """Einfarbverlauf von :attr:`verlauf_hell` nach :attr:`haupt` (Betragsfüllung)."""
        return LinearSegmentedColormap.from_list("ldv_verlauf", [self.verlauf_hell, self.haupt])

    def zyklisch(self) -> Colormap:
        """Zyklische Farbskala der Phase (:data:`ZYKLISCHE_SKALA`)."""
        return colormaps[ZYKLISCHE_SKALA]

    def rc(self) -> dict[Any, Any]:
        """``rcParams``-Wörterbuch für ``matplotlib.rc_context`` (kein globaler Zustand)."""
        return {
            "font.family": "sans-serif",
            "font.sans-serif": list(self.schriftfamilie),
            "font.size": self.schrift_pt,
            "axes.labelsize": self.schrift_pt,
            "xtick.labelsize": self.schrift_pt,
            "ytick.labelsize": self.schrift_pt,
            "legend.fontsize": self.schrift_pt,
            "axes.edgecolor": self.achse,
            "axes.labelcolor": self.achse,
            "xtick.color": self.achse,
            "ytick.color": self.achse,
            "text.color": self.achse,
            "axes.facecolor": self.flaeche,
            "figure.facecolor": self.flaeche,
            "savefig.facecolor": self.flaeche,
            "grid.color": self.gitter,
            "axes.unicode_minus": True,
            "axes.formatter.use_locale": False,
        }


THESIS_STIL = Plotstil()
"""Stil der Thesis-Abbildungen: schwarz/grau, 9 pt, kein Gelb, ohne Farbe als Information."""
