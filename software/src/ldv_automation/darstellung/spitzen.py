"""Ansicht 3: Spitzen und Bänder (eine Zeichenfunktion für Oberfläche und Thesis, P-AUSW T2).

Die Kurve (Betragsmittel ``|H1|`` bzw. ohne Referenz das Leistungsmittel ``√AP``) trägt einen
Marker an jeder Spitze; **beschriftet wird nur die gewählte Spitze** (in der Beispieldatei gibt
es 111 Spitzen, alle Beschriftungen wären unlesbar). Bänder sind schattierte Flächen unterhalb
der Kurve. Zahlen kommen aus den Ergebnisobjekten des Kerns, hier wird nichts gerechnet.
"""

from __future__ import annotations

import math
from dataclasses import dataclass

from matplotlib import rc_context
from matplotlib.figure import Figure
from matplotlib.lines import Line2D
from matplotlib.patches import Patch

from ldv_automation.auswertung.export import METHODE_SPITZEN
from ldv_automation.auswertung.spitzen import Spitze

from .auswahl import SpitzenDaten
from .formate import MINUS, achsentitel, frequenz_text, zahl_signifikant_text, zahl_text
from .stil import Plotstil
from .zeichnung import Skala, Zeichnung, setze_achsenstil

__all__ = ["HINWEIS_ZETA", "SpitzenOptionen", "beschriftung_der_spitze", "zeichne_spitzen"]

HINWEIS_ZETA = (
    f"ζ aus der {MINUS}3-dB-Breite des Betragsmittels |H1| "
    "(kein Modaldämpfungswert eines einzelnen Punktes)"
)
"""Hinweis zur Bedeutung von ζ der Spitzen (``Zeichnung.hinweise``; KONVENTIONEN Messdaten)."""

_KENNZEICHEN_TEXT = {
    "aufloesungsbegrenzt": "auflösungsbegrenzt",
    "ueberlappend": "überlappend",
    "nachbarmode": "Nachbarmode",
    "kohaerenz_niedrig": "Kohärenz niedrig",
}
"""Anzeigetexte der Warnkennzeichen des Kerns (Bezeichner wie im Export; unbekannte unverändert)."""


@dataclass(frozen=True, kw_only=True)
class SpitzenOptionen:
    """Darstellungsoptionen von Ansicht 3.

    Attributes
    ----------
    skala : {"linear", "log"}
        Skala der Kurve (Voreinstellung logarithmisch).
    """

    skala: Skala = "log"

    def __post_init__(self) -> None:
        if self.skala not in ("linear", "log"):
            raise ValueError(f"unbekannte Skala {self.skala!r}")


def beschriftung_der_spitze(
    spitze: Spitze, *, dezimalkomma: bool = True, warn_symbol: str = "⚠"
) -> str:
    """Beschriftung der gewählten Spitze mit ζ, Bandgrenzen, Methode und Warnkennzeichen.

    Beispiel: ``f = 65,121 Hz · ζ ≈ 0,0058 (-3dB-Breite, 64,7 … 65,5 Hz)``; trägt die Spitze
    Warnkennzeichen (``Spitze.kennzeichen``), folgt eine zweite Zeile ``⚠ auflösungsbegrenzt``.
    Jede Dämpfungsangabe nennt ζ, Bandgrenzen und Methode (KONVENTIONEN, R-055); die Methode
    ist :data:`~ldv_automation.auswertung.export.METHODE_SPITZEN`. Ohne bestimmte Breite
    (ζ oder Bandgrenzen NaN) steht „ζ = –“ ohne Methodenangabe, denn es wird kein Wert angegeben.

    Parameters
    ----------
    spitze : Spitze
        Gewählte Spitze (``f_sp_hz``, ``zeta``, ``f_l_hz``, ``f_r_hz``, ``kennzeichen``).
    dezimalkomma : bool, optional
        ``False`` behält den Dezimalpunkt.
    warn_symbol : str, optional
        Symbol vor den Warnkennzeichen (Symbol plus Wort, nie nur Farbe).
    """
    f_text = frequenz_text(spitze.f_sp_hz, 3, dezimalkomma=dezimalkomma)
    bestimmt = not any(math.isnan(w) for w in (spitze.zeta, spitze.f_l_hz, spitze.f_r_hz))
    if bestimmt:
        zeta = zahl_signifikant_text(spitze.zeta, 2, dezimalkomma=dezimalkomma)
        unten = zahl_text(round(spitze.f_l_hz, 3), None, dezimalkomma=dezimalkomma)
        oben = frequenz_text(spitze.f_r_hz, 3, dezimalkomma=dezimalkomma)
        zeta_text = f"ζ ≈ {zeta} ({METHODE_SPITZEN}, {unten} … {oben})"
    else:
        zeta_text = "ζ = –"
    text = f"f = {f_text} · {zeta_text}"
    if spitze.kennzeichen:
        worte = ", ".join(_KENNZEICHEN_TEXT.get(k, k) for k in spitze.kennzeichen)
        text += f"\n{warn_symbol} {worte}"
    return text


def zeichne_spitzen(
    fig: Figure, daten: SpitzenDaten, opt: SpitzenOptionen, stil: Plotstil
) -> Zeichnung:
    """Zeichnet Kurve, Spitzenmarker und Bänder in ``fig`` (ohne Titel, ohne Stempel).

    Parameters
    ----------
    fig : Figure
        Wird geleert und neu gefüllt.
    daten : SpitzenDaten
        Aus :func:`~ldv_automation.darstellung.auswahl.spitzen_daten_frf` bzw.
        :func:`~ldv_automation.darstellung.auswahl.spitzen_daten_spektrum`.
    opt : SpitzenOptionen
        Skala.
    stil : Plotstil
        Farben, Linienarten, Schrift.

    Returns
    -------
    Zeichnung
        ``linien["kurve"]``, ``marker["spitzen"]`` (alle Spitzen, nur bei vorhandenen Spitzen),
        ``marker["gewaehlt"]`` (gewählte Spitze), ``hilfsobjekte["baender"]`` (Liste), ``texte``
        mit der Beschriftung der gewählten Spitze bzw. dem Hinweis ohne Spitzen, ``hinweise``
        mit :data:`HINWEIS_ZETA` (nur bei vorhandenen Spitzen).
    """
    with rc_context(stil.rc()):
        fig.clear()
        fig.set_layout_engine("constrained")
        ax = fig.subplots()
        z = Zeichnung(figure=fig, achsen=(ax,), hinweise=(HINWEIS_ZETA,) if daten.spitzen else ())
        handles: list[Line2D | Patch] = []
        baender = []
        for f_u, f_o in daten.baender:
            baender.append(ax.axvspan(f_u, f_o, facecolor=stil.band, edgecolor="none", zorder=0.5))
        z.hilfsobjekte["baender"] = baender
        (kurve,) = ax.plot(
            daten.frequenz_hz,
            daten.y,
            linestyle=stil.linienart(0),
            color=stil.haupt,
            linewidth=stil.linienbreite_pt,
            label=daten.beschriftung,
            zorder=2,
        )
        z.linien["kurve"] = kurve
        handles.append(kurve)
        if daten.spitzen:
            (alle,) = ax.plot(
                [s.f_sp_hz for s in daten.spitzen],
                [s.hoehe for s in daten.spitzen],
                linestyle="none",
                marker="v",
                markersize=5,
                markerfacecolor=stil.haupt,
                markeredgecolor=stil.achse,
                label=f"Spitzen ({len(daten.spitzen)})",
                zorder=3,
            )
            z.marker["spitzen"] = alle
            handles.append(alle)
        if daten.gewaehlt is not None:
            s = daten.spitzen[daten.gewaehlt]
            (gew,) = ax.plot(
                [s.f_sp_hz],
                [s.hoehe],
                linestyle="none",
                marker="o",
                markersize=11,
                markerfacecolor="none",
                markeredgecolor=stil.achse,
                markeredgewidth=1.5,
                zorder=4,
            )
            z.marker["gewaehlt"] = gew
            # Beschriftung nahe dem linken/rechten Rand nach innen ausrichten (nicht abschneiden)
            lage = (s.f_sp_hz - float(daten.frequenz_hz[0])) / max(
                float(daten.frequenz_hz[-1] - daten.frequenz_hz[0]), 1e-300
            )
            ausrichtung = "left" if lage < 0.25 else "right" if lage > 0.75 else "center"
            z.texte.append(
                ax.annotate(
                    beschriftung_der_spitze(
                        s, dezimalkomma=stil.dezimalkomma, warn_symbol=stil.warn_symbol
                    ),
                    xy=(s.f_sp_hz, s.hoehe),
                    xytext=(0, 16),
                    textcoords="offset points",
                    ha=ausrichtung,
                    va="bottom",
                    multialignment="left",
                    fontsize=stil.schrift_pt,
                    arrowprops={"arrowstyle": "-", "color": stil.achse, "linewidth": 0.8},
                    bbox={
                        "boxstyle": "square,pad=0.2",
                        "facecolor": stil.flaeche,
                        "edgecolor": stil.achse,
                        "linewidth": 0.6,
                    },
                    zorder=5,
                )
            )
        if daten.baender:
            teile = "; ".join(
                f"{zahl_text(u, None, dezimalkomma=stil.dezimalkomma)} … "
                f"{frequenz_text(o, 3, dezimalkomma=stil.dezimalkomma)}"
                for u, o in daten.baender
            )
            handles.append(Patch(facecolor=stil.band, edgecolor=stil.gitter, label=f"Band {teile}"))
        if not daten.spitzen and daten.hinweis:
            z.texte.append(
                ax.text(
                    0.5,
                    0.04,
                    daten.hinweis,
                    transform=ax.transAxes,
                    ha="center",
                    va="bottom",
                    fontsize=stil.schrift_pt,
                    color=stil.text_gedaempft,
                )
            )
        if opt.skala == "log":
            ax.set_yscale("log", nonpositive="mask")
        ax.set_xlim(float(daten.frequenz_hz[0]), float(daten.frequenz_hz[-1]))
        ax.set_xlabel(achsentitel("Frequenz", "Hz"))
        ax.set_ylabel(achsentitel(daten.groesse, daten.einheit))
        setze_achsenstil(ax, stil)
        z.hilfsobjekte["legende"] = ax.legend(
            handles=handles,
            loc="upper right",
            fontsize=stil.schrift_pt,
            framealpha=0.9,
            numpoints=1,
        )
    return z
