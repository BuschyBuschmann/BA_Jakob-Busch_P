"""Plotstil der Oberfläche aus den Tokens (P-AUSW T3a, Brief K-AUSW Abschnitt 2).

Die Zeichenfunktionen (:mod:`ldv_automation.darstellung`) kennen keine Oberflächen-Tokens, sie
bekommen einen :class:`~ldv_automation.darstellung.stil.Plotstil`. Dieses Modul baut ihn aus
``gui/tokens.py``; Farben stehen nur dort. Das Thesis-Skript nimmt dagegen
:data:`~ldv_automation.darstellung.stil.THESIS_STIL`. Das Modul ist Qt-frei.
"""

from __future__ import annotations

from ldv_automation.darstellung.stil import Plotstil
from ldv_automation.gui import tokens as t

__all__ = ["SCHRIFT_RUECKFALL", "baue_plotstil"]

SCHRIFT_RUECKFALL = "DejaVu Sans"
"""Schrift, die matplotlib mitbringt: Rückfall, wenn Segoe UI und Arial fehlen (Linux, CI)."""


def baue_plotstil() -> Plotstil:
    """Plotstil der Oberfläche: Farben und Schrift aus :mod:`ldv_automation.gui.tokens`.

    Returns
    -------
    Plotstil
        Hauptfarbe, Gitter, Achse, Fläche, Band, Serienfarben und Linienarten aus den Tokens;
        das Warnsymbol folgt :func:`ldv_automation.gui.tokens.symbol` (ASCII-Rückfall).
    """
    return Plotstil(
        haupt=t.C_PLOT_HAUPT,
        gitter=t.C_PLOT_GITTER,
        achse=t.C_PLOT_ACHSE,
        flaeche=t.C_PLOT_FLAECHE,
        text_gedaempft=t.C_TEXT_GEDAEMPFT,
        band=t.C_PLOT_BAND,
        warn_bg=t.C_WARN_BG,
        warn_rand=t.C_WARN_RAND,
        serienfarben=t.PLOT_SERIENFARBEN,
        linienarten=tuple(stil for _name, stil in t.PLOT_LINIENARTEN),
        verlauf_hell=t.C_PLOT_VERLAUF_HELL,
        schrift_pt=float(t.SCHRIFT_PT),
        schriftfamilie=(*t.SCHRIFT_FAMILIEN, SCHRIFT_RUECKFALL),
        linienbreite_pt=t.PLOT_LINIENBREITE_PT,
        dezimalkomma=True,
        warn_symbol=t.symbol("warnung"),
    )
