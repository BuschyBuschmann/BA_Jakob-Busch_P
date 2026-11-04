"""Arbeitsbild mit Stempel aus derselben Zeichenfunktion (P-AUSW T2, UI-17/UI-18).

``speichere_arbeitsbild`` baut eine **neue** Figure, ruft dieselbe Zeichenfunktion wie die
Bildschirmdarstellung auf, übernimmt den Zoom und ergänzt den Fußstempel. Die Bildschirmfigur
bleibt unverändert (Abweichung vom Brief „auf derselben Figure“, Annahme N-6). Thesis-Abbildungen
rufen die Zeichenfunktion auf :func:`neue_figure` **ohne** Stempel auf.
"""

from __future__ import annotations

from collections.abc import Callable, Mapping, Sequence
from dataclasses import dataclass
from pathlib import Path

from matplotlib.figure import Figure
from matplotlib.layout_engine import ConstrainedLayoutEngine

from .stil import Plotstil
from .zeichnung import Zeichnung

__all__ = [
    "ARBEITSANSICHT",
    "Grenzen",
    "Stempel",
    "baue_stempel",
    "neue_figure",
    "speichere_arbeitsbild",
]

ARBEITSANSICHT = "Arbeitsansicht – nicht für die Thesis"
"""Anfang des Fußstempels (UI-17)."""

STANDARD_DPI = 200
"""PNG-Auflösung (Brief: nur im Code einstellbar, kein Dialogfeld)."""

STANDARD_GROESSE_ZOLL = (9.0, 5.6)

Grenzen = tuple[tuple[float, float] | None, tuple[float, float] | None]
"""Achsengrenzen ``(xlim, ylim)``; ``None`` = unverändert."""


@dataclass(frozen=True, kw_only=True)
class Stempel:
    """Fußstempel des Arbeitsbildes.

    Attributes
    ----------
    zeilen : tuple of str
        Zeilen von oben nach unten.
    """

    zeilen: tuple[str, ...]


def baue_stempel(
    *,
    dateiname: str,
    ansicht: str,
    git_hash: str | None,
    unbestaetigt: Sequence[str] = (),
    warn_symbol: str = "⚠",
) -> Stempel:
    """Stempel „Arbeitsansicht – nicht für die Thesis · Datei · Ansicht · Git-Hash“.

    Parameters
    ----------
    dateiname : str
        Name der Messdatei.
    ansicht : str
        Name der Ansicht, z. B. „Ansicht 1 Spektrum“.
    git_hash : str or None
        Git-Hash der Software; ``None`` ergibt „Git-Hash unbekannt“.
    unbestaetigt : sequence of str
        Nummern der Annahmen, von denen unbestätigte Größen im Bild abhängen (z. B. ``("M8",)``);
        leer = keine zweite Zeile.
    warn_symbol : str
        Symbol der Warnzeile (Oberfläche: ``tokens.symbol("warnung")``).
    """
    erste = f"{ARBEITSANSICHT} · {dateiname} · {ansicht} · {git_hash or 'Git-Hash unbekannt'}"
    if not unbestaetigt:
        return Stempel(zeilen=(erste,))
    zweite = f"{warn_symbol} enthält unbestätigte Größen ({', '.join(unbestaetigt)})"
    return Stempel(zeilen=(erste, zweite))


def neue_figure(
    stil: Plotstil, groesse_zoll: tuple[float, float] = STANDARD_GROESSE_ZOLL
) -> Figure:
    """Neue leere Figure (ohne ``pyplot``) mit der Flächenfarbe des Stils."""
    return Figure(figsize=groesse_zoll, facecolor=stil.flaeche)


def speichere_arbeitsbild(
    zeichne: Callable[[Figure], Zeichnung],
    pfad: Path,
    stempel: Stempel,
    stil: Plotstil,
    *,
    dpi: int = STANDARD_DPI,
    grenzen: Mapping[int, Grenzen] | None = None,
    groesse_zoll: tuple[float, float] = STANDARD_GROESSE_ZOLL,
) -> Zeichnung:
    """Schreibt die Ansicht als PNG oder PDF mit Stempel.

    Parameters
    ----------
    zeichne : callable
        Füllt die übergebene Figure und gibt die :class:`Zeichnung` zurück; dieselbe Funktion
        (mit denselben Daten und Optionen) wie die Bildschirmdarstellung, z. B.
        ``lambda fig: zeichne_spektrum(fig, daten, opt, stil)``.
    pfad : pathlib.Path
        Ziel; die Endung (``.png`` oder ``.pdf``) bestimmt das Format.
    stempel : Stempel
        Fußstempel.
    stil : Plotstil
        Stil der Figure und des Stempels.
    dpi : int, optional
        Auflösung für PNG (Voreinstellung 200).
    grenzen : mapping, optional
        Zoom je Achsenindex (Reihenfolge ``Zeichnung.achsen``): ``(xlim, ylim)``.
    groesse_zoll : tuple of float, optional
        Bildgröße in Zoll.

    Returns
    -------
    Zeichnung
        Die gezeichnete Kopie (für Tests und Protokolle).

    Raises
    ------
    ValueError
        Endung weder ``.png`` noch ``.pdf``.
    """
    if pfad.suffix.lower() not in (".png", ".pdf"):
        raise ValueError(f"Bildformat {pfad.suffix!r} nicht unterstützt (.png oder .pdf)")
    fig = neue_figure(stil, groesse_zoll)
    zeichnung = zeichne(fig)
    for index, (xlim, ylim) in (grenzen or {}).items():
        ax = zeichnung.achsen[index]
        if xlim is not None:
            ax.set_xlim(*xlim)
        if ylim is not None:
            ax.set_ylim(*ylim)
    hoehe = 0.028 * len(stempel.zeilen) + 0.012
    engine = fig.get_layout_engine()
    if isinstance(engine, ConstrainedLayoutEngine):
        engine.set(rect=(0.0, hoehe, 1.0, 1.0 - hoehe))
    for n, zeile in enumerate(reversed(stempel.zeilen)):
        fig.text(
            0.01,
            0.008 + 0.028 * n,
            zeile,
            ha="left",
            va="bottom",
            fontsize=stil.schrift_pt * 0.85,
            color=stil.text_gedaempft,
        )
    with_dpi = dpi if pfad.suffix.lower() == ".png" else None
    fig.savefig(pfad, dpi=with_dpi)
    return zeichnung
