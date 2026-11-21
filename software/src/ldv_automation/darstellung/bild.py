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

from matplotlib import rc_context
from matplotlib.figure import Figure

from .stil import Plotstil
from .zeichnung import Zeichnung

__all__ = [
    "ARBEITSANSICHT",
    "EXPORT_FIGURE_DPI",
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

EXPORT_FIGURE_DPI = 100.0
"""Feste Figure-DPI aller Export-Figures (matplotlib-Standard).

Zeichenfunktionen messen Beschriftungen und Abstände in Pixeln bei der Figure-DPI (Punktlabels,
Zoom der Animation); ohne feste Angabe würde ``rcParams["figure.dpi"]`` einer fremden
``matplotlibrc`` Layout und Bild verändern. Mit dem matplotlib-Standard 100 bleiben bisherige
Abbildungen unverändert."""

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
    dateiname: str | None = None,
    ansicht: str,
    git_hash: str | None,
    unbestaetigt: Sequence[str] = (),
    warn_symbol: str = "⚠",
    dateien: Sequence[tuple[str, str]] = (),
    zusatz: Sequence[str] = (),
) -> Stempel:
    """Stempel „Arbeitsansicht – nicht für die Thesis · Datei · Ansicht · Git-Hash“.

    Mit ``dateien`` (Ansicht 5: mehrere Messungen) steht in der Kopfzeile statt der Datei nur
    „Ansicht · Git-Hash“, danach je Datei eine Zeile ``<Kurzname>: <Dateiname>``. Mit ``zusatz``
    (Animation: Winkel, Frequenz, Überhöhung, Blick) folgen die Zeilen danach, vor der Warnzeile.

    Parameters
    ----------
    dateiname : str, optional
        Name der Messdatei (eine Datei). Entfällt, wenn ``dateien`` gesetzt ist.
    ansicht : str
        Name der Ansicht, z. B. „Ansicht 1 Spektrum“.
    git_hash : str or None
        Git-Hash der Software; ``None`` ergibt „Git-Hash unbekannt“.
    unbestaetigt : sequence of str
        Nummern der Annahmen, von denen unbestätigte Größen im Bild abhängen (z. B. ``("M8",)``);
        leer = keine Warnzeile.
    warn_symbol : str
        Symbol der Warnzeile (Oberfläche: ``tokens.symbol("warnung")``).
    dateien : sequence of tuple of str
        ``(Kurzname, Dateiname)`` jeder beteiligten Messung (Ansicht 5); leer = eine Datei über
        ``dateiname``.
    zusatz : sequence of str
        Weitere Stempelzeilen mit dem Zustand des Bildes (Animation: Winkel θ, Frequenz,
        Überhöhung, Blickrichtung); leer = keine.

    Raises
    ------
    ValueError
        Weder ``dateiname`` noch ``dateien`` angegeben.
    """
    hash_text = git_hash or "Git-Hash unbekannt"
    if dateien:
        zeilen = [f"{ARBEITSANSICHT} · {ansicht} · {hash_text}"]
        zeilen += [f"{kurzname}: {name}" for kurzname, name in dateien]
    elif dateiname is not None:
        zeilen = [f"{ARBEITSANSICHT} · {dateiname} · {ansicht} · {hash_text}"]
    else:
        raise ValueError("Der Stempel braucht einen Dateinamen oder eine Liste von Dateien.")
    zeilen.extend(zusatz)
    if unbestaetigt:
        zeilen.append(f"{warn_symbol} enthält unbestätigte Größen ({', '.join(unbestaetigt)})")
    return Stempel(zeilen=tuple(zeilen))


def neue_figure(
    stil: Plotstil, groesse_zoll: tuple[float, float] = STANDARD_GROESSE_ZOLL
) -> Figure:
    """Neue leere Figure (ohne ``pyplot``) mit der Flächenfarbe und fester DPI."""
    return Figure(figsize=groesse_zoll, dpi=EXPORT_FIGURE_DPI, facecolor=stil.flaeche)


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
    with rc_context(stil.schrift_rc()):  # Stempeltext und Messungen in der Stilschrift
        fig = neue_figure(stil, groesse_zoll)
        # Rand für den Stempel **vor** dem Zeichnen: die Zeichenfunktionen messen in pt (Layout)
        hoehe = 0.028 * len(stempel.zeilen) + 0.012
        fig.set_layout_engine("constrained", rect=(0.0, hoehe, 1.0, 1.0 - hoehe))
        zeichnung = zeichne(fig)
        for index, (xlim, ylim) in (grenzen or {}).items():
            ax = zeichnung.achsen[index]
            if xlim is not None:
                ax.set_xlim(*xlim)
            if ylim is not None:
                ax.set_ylim(*ylim)
        # Stempel und Speichern im Kontext der Zeichnung (Animation: Matplotlib-Standard für
        # Hinting, Antialiasing, Schriftgewicht, Speicherfläche), sonst nur in der Stilschrift
        with rc_context(zeichnung.hilfsobjekte.get("zeichen_rc", {})):
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
            # PDF: explizit die Figure-DPI (Rasteranteile), nie ``savefig.dpi`` der rc-Datei
            fig.savefig(pfad, dpi=dpi if pfad.suffix.lower() == ".png" else EXPORT_FIGURE_DPI)
        return zeichnung
