"""Ansicht 3: Spitzen und Bänder (eine Zeichenfunktion für Oberfläche und Thesis, P-AUSW T2).

Die Kurve (Betragsmittel ``|H1|`` bzw. ohne Referenz das Leistungsmittel ``√AP``) trägt einen
Marker an jeder Spitze; **beschriftet wird nur die gewählte Spitze** (in der Beispieldatei gibt
es 111 Spitzen, alle Beschriftungen wären unlesbar). Bänder sind schattierte Flächen unterhalb
der Kurve. Zahlen kommen aus den Ergebnisobjekten des Kerns, hier wird nichts gerechnet.

Layout (K-AUSW-LAYOUT 3.1 bis 3.5): Oberhalb der höchsten Kurvenstelle bleibt ein leerer
Streifen in der Achse (immer, sobald Spitzen existieren, damit die y-Skala beim Wechsel der
Spitze nicht springt); dort steht der Kasten der gewählten Spitze, eine Leitlinie führt zur
Spitze. Die Legende steht unterhalb der Achse. Alle Maße in pt werden nach dem Layout gemessen,
die Figure muss deshalb vor dem Aufruf ihre endgültige Größe haben.
"""

from __future__ import annotations

import math
from dataclasses import dataclass

from matplotlib import rc_context
from matplotlib.axes import Axes
from matplotlib.figure import Figure
from matplotlib.legend import Legend
from matplotlib.lines import Line2D
from matplotlib.patches import Patch
from matplotlib.transforms import ScaledTranslation

from ldv_automation.auswertung.export import METHODE_SPITZEN
from ldv_automation.auswertung.spitzen import Spitze

from .achsen import AchsenOptionen, nebenticks_log, wende_frequenz_an, wende_y_an
from .auswahl import SpitzenDaten
from .formate import MINUS, achsentitel, frequenz_text, zahl_signifikant_text, zahl_text
from .stil import Plotstil
from .zeichnung import Skala, Zeichnung, achse_pt, constrained_layout, setze_achsenstil

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
    beschriftung_im_bild : bool
        ``True`` (Voreinstellung, Thesis-Abbildung und Arbeitsbild): Beschriftungsstreifen,
        Kasten und Leitlinie der gewählten Spitze im Bild. ``False`` (Oberfläche, ADR-026
        Nachtrag): nur der Ring um die gewählte Spitze, kein Streifen und kein Kasten; die
        Oberfläche zeigt die Angaben (:func:`beschriftung_der_spitze`) als Text in der
        Auswahlspalte.
    legende_im_bild : bool
        ``True`` (Voreinstellung, Thesis-Abbildung und Arbeitsbild): Kurvenlegende unterhalb
        der Achsenbeschriftung. ``False`` (Oberfläche, ADR-026 Nachtrag 2): keine Legende im
        Bild, die Achse bekommt die Höhe; die Einträge stehen in
        ``Zeichnung.hilfsobjekte["legende_eintraege"]`` (Mittelformel und Punktzahl, Spitzen,
        Band) und die Oberfläche zeigt sie als Text.
    achsen : AchsenOptionen or None
        Feste Bereiche und Frequenzskala (R-073, Rolle ``"betrag"``); ``None`` lässt die Achsen
        unverändert. Ein gesetzter y-Bereich ist der **Datenbereich**: Ist
        ``beschriftung_im_bild`` gesetzt, kommt der Beschriftungsstreifen oberhalb der oberen
        Grenze dazu (die obere Achsengrenze im Bild liegt dann über der Eingabe); in der
        Oberfläche (ohne Streifen) entspricht sie genau der Eingabe.
    """

    skala: Skala = "log"
    beschriftung_im_bild: bool = True
    legende_im_bild: bool = True
    achsen: AchsenOptionen | None = None

    def __post_init__(self) -> None:
        if self.skala not in ("linear", "log"):
            raise ValueError(f"unbekannte Skala {self.skala!r}")


def beschriftung_der_spitze(
    spitze: Spitze, *, dezimalkomma: bool = True, warn_symbol: str = "⚠"
) -> str:
    """Beschriftung der gewählten Spitze mit ζ, Bandgrenzen, Methode und Warnkennzeichen.

    Höchstens drei Zeilen::

        f = 65,121 Hz · ζ ≈ 0,0058
        -3dB-Breite, 64,768 … 65,526 Hz
        ⚠ auflösungsbegrenzt

    Die zweite Zeile nennt Methode (:data:`~ldv_automation.auswertung.export.METHODE_SPITZEN`)
    und Bandgrenzen, die dritte alle Warnkennzeichen (``Spitze.kennzeichen``, kommagetrennt;
    sie entfällt ohne Kennzeichen). Frequenzen haben feste drei Nachkommastellen, ζ zwei
    signifikante Stellen (KONVENTIONEN). Ohne bestimmte Breite (ζ oder Bandgrenzen NaN) steht
    „ζ = –“ ohne Methodenzeile, denn es wird kein Wert angegeben.

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
        unten = zahl_text(round(spitze.f_l_hz, 3) + 0.0, 3, dezimalkomma=dezimalkomma)
        oben = frequenz_text(spitze.f_r_hz, 3, dezimalkomma=dezimalkomma)
        zeilen = [f"f = {f_text} · ζ ≈ {zeta}", f"{METHODE_SPITZEN}, {unten} … {oben}"]
    else:
        zeilen = [f"f = {f_text} · ζ = –"]
    if spitze.kennzeichen:
        worte = ", ".join(_KENNZEICHEN_TEXT.get(k, k) for k in spitze.kennzeichen)
        zeilen.append(f"{warn_symbol} {worte}")
    return "\n".join(zeilen)


STREIFEN_MIN = 0.10
STREIFEN_MAX = 0.50
"""Grenzen des Anteils der Achsenhöhe für den Beschriftungsstreifen.

Das Layout nennt 0,10 … 0,30. Bei 11,5 cm mal 7 cm (Achsenhöhe ca. 116 pt) braucht der
Dreizeilenkasten aber 0,46; mit 0,30 läge er auf den Daten (L3-2/L3-7). Die Obergrenze ist
deshalb 0,50 (Abweichung vom Layout, im Bericht genannt)."""

KASTEN_ABSTAND_OBEN_PT = 4.0
"""Abstand der Kasten-Oberkante zur Achsenoberkante."""

_ZEILENABSTAND = 1.25
_KASTEN_PAD = 0.2
_LUFT_UNTER_KASTEN_PT = 16.0
_LEITLINIE_ENDE_PT = 7.0


def streifen_anteil(achsenhoehe_pt: float, schrift_pt: float) -> float:
    """Anteil der Achsenhöhe für den Beschriftungsstreifen (drei Zeilen plus 16 pt Luft).

    ``s = (3 · 1,25 · schrift + 2 · 0,2 · schrift + 16 pt) / Achsenhöhe``, begrenzt auf
    :data:`STREIFEN_MIN` … :data:`STREIFEN_MAX`.
    """
    kasten = 3 * _ZEILENABSTAND * schrift_pt + 2 * _KASTEN_PAD * schrift_pt
    s = (kasten + _LUFT_UNTER_KASTEN_PT) / max(achsenhoehe_pt, 1e-9)
    return min(max(s, STREIFEN_MIN), STREIFEN_MAX)


def obere_grenze(unten: float, oben: float, anteil: float, *, log: bool) -> float:
    """Obere y-Grenze, so dass über ``oben`` der Streifen ``anteil`` der Achsenhöhe frei bleibt."""
    if log:
        return float(math.exp(math.log(unten) + (math.log(oben) - math.log(unten)) / (1 - anteil)))
    return unten + (oben - unten) / (1 - anteil)


def _legende(ax: Axes, handles: list[Line2D | Patch], stil: Plotstil) -> Legend:
    """Legende unterhalb der Achsenbeschriftung; einzeilig, wenn sie passt, sonst eine Spalte.

    Die Legende hängt an der Achse (das Constrained Layout reserviert den Platz und achtet auf
    den ``rect`` des Arbeitsbildes, anders als ``fig.legend(loc="outside lower center")``).
    """
    fig = ax.figure
    assert isinstance(fig, Figure)
    fig.draw_without_rendering()
    titel = ax.xaxis.label.get_window_extent()
    tiefe_pt = (float(ax.bbox.y0) - float(titel.y0)) * 72.0 / fig.dpi + 4.0
    versatz = ScaledTranslation(0.0, -tiefe_pt / 72.0, fig.dpi_scale_trans)
    ncol = max(len(handles), 1)
    for _ in range(2):
        legende = ax.legend(
            handles=handles,
            loc="upper center",
            bbox_to_anchor=(0.5, 0.0),
            bbox_transform=ax.transAxes + versatz,
            borderaxespad=0.0,
            ncol=ncol,
            fontsize=stil.schrift_pt,
            framealpha=0.9,
            numpoints=1,
        )
        if ncol == 1 or legende.get_window_extent().width <= 0.98 * fig.bbox.width:
            fig.draw_without_rendering()
            return legende
        legende.remove()
        ncol = 1
    fig.draw_without_rendering()  # pragma: no cover
    return legende  # pragma: no cover


def zeichne_spitzen(
    fig: Figure, daten: SpitzenDaten, opt: SpitzenOptionen, stil: Plotstil
) -> Zeichnung:
    """Zeichnet Kurve, Spitzenmarker und Bänder in ``fig`` (ohne Titel, ohne Stempel).

    Parameters
    ----------
    fig : Figure
        Wird geleert und neu gefüllt; die Größe muss endgültig sein (Messung in pt).
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
        ``marker["gewaehlt"]`` (gewählte Spitze), ``hilfsobjekte["baender"]`` (Liste),
        ``hilfsobjekte["legende"]`` (Legende unterhalb der Achsenbeschriftung, nur mit
        ``opt.legende_im_bild``), ``hilfsobjekte["legende_eintraege"]`` (Texte der Einträge),
        ``hilfsobjekte["leitlinie"]`` (nur mit gewählter Spitze), ``hilfsobjekte["streifen"]``
        (Anteil der Achsenhöhe, nur mit Spitzen), beide nur mit
        ``opt.beschriftung_im_bild``; ``texte`` mit dem Kasten der gewählten
        Spitze bzw. dem Hinweis ohne Spitzen, ``hinweise`` mit :data:`HINWEIS_ZETA` (nur bei
        vorhandenen Spitzen).
    """
    with rc_context(stil.rc()):
        fig.clear()
        constrained_layout(fig)
        ax = fig.subplots()
        z = Zeichnung(
            figure=fig,
            achsen=(ax,),
            hinweise=(HINWEIS_ZETA,) if daten.spitzen else (),
            rollen=("betrag",),
        )
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
        if daten.baender:
            teile = "; ".join(
                f"{zahl_text(u, 3, dezimalkomma=stil.dezimalkomma)} … "
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
        f_min, f_max = float(daten.frequenz_hz[0]), float(daten.frequenz_hz[-1])
        if opt.achsen is None:
            ax.set_xlim(f_min, f_max)
        else:
            x_fest = wende_frequenz_an(ax, opt.achsen, f_min, f_max)
            wende_y_an(
                ax,
                opt.achsen.y_bereich("betrag"),
                log=opt.skala == "log",
                x_gesetzt=x_fest,
                name="Betrag",
            )
        ax.set_xlabel(achsentitel("Frequenz", "Hz"))
        ax.set_ylabel(achsentitel(daten.groesse, daten.einheit))
        setze_achsenstil(ax, stil)
        if opt.achsen is not None:
            nebenticks_log(ax, dezimalkomma=stil.dezimalkomma)
        z.hilfsobjekte["legende_eintraege"] = [str(h.get_label()) for h in handles]
        if opt.legende_im_bild:
            z.hilfsobjekte["legende"] = _legende(ax, handles, stil)
        if daten.spitzen and opt.beschriftung_im_bild:
            _streifen_und_kasten(z, ax, daten, opt, stil)
    return z


def _streifen_und_kasten(
    z: Zeichnung, ax: Axes, daten: SpitzenDaten, opt: SpitzenOptionen, stil: Plotstil
) -> None:
    """Reserviert den Streifen über der Kurve und setzt Kasten und Leitlinie hinein."""
    fig = ax.figure
    assert isinstance(fig, Figure)
    fig.draw_without_rendering()  # endgültiges Layout (Legende unten, Achsenbeschriftung)
    _, hoehe_pt = achse_pt(ax)
    unten, oben = ax.get_ylim()  # Autoskalierung von Kurve und Markern
    anteil = streifen_anteil(hoehe_pt, stil.schrift_pt)
    ax.set_ylim(unten, obere_grenze(unten, oben, anteil, log=opt.skala == "log"))
    z.hilfsobjekte["streifen"] = anteil
    if daten.gewaehlt is None:
        return
    s = daten.spitzen[daten.gewaehlt]
    x_unten, x_oben = sorted(ax.get_xlim())
    if (
        not x_unten <= s.f_sp_hz <= x_oben
    ):  # Spitze außerhalb des Frequenzbereichs: keine Beschriftung
        return
    pt = ax.figure.dpi / 72.0  # px je pt
    pad_pt = _KASTEN_PAD * stil.schrift_pt
    kasten = ax.text(
        0.0,
        1.0,
        beschriftung_der_spitze(s, dezimalkomma=stil.dezimalkomma, warn_symbol=stil.warn_symbol),
        transform=ax.transAxes,
        ha="left",
        va="top",
        multialignment="left",
        linespacing=_ZEILENABSTAND,
        fontsize=stil.schrift_pt,
        bbox={
            "boxstyle": f"square,pad={_KASTEN_PAD}",
            "facecolor": stil.flaeche,
            "edgecolor": stil.achse,
            "linewidth": 0.6,
        },
        zorder=5,
    )
    text_px = kasten.get_window_extent()
    ges_breite_px = text_px.width + 2 * pad_pt * pt
    ges_hoehe_pt = text_px.height / pt + 2 * pad_pt
    x0 = float(ax.bbox.x0)
    breite_px = float(ax.bbox.width)
    x_spitze_px = float(ax.transData.transform((s.f_sp_hz, s.hoehe))[0])
    links_px = min(
        max(x_spitze_px - ges_breite_px / 2, x0 + 0.01 * breite_px),
        x0 + 0.99 * breite_px - ges_breite_px,
    )
    kasten.set_position(
        (
            (links_px + pad_pt * pt - x0) / breite_px,
            1.0 - (KASTEN_ABSTAND_OBEN_PT + pad_pt) / hoehe_pt,
        )
    )
    z.texte.append(kasten)
    start_px = min(max(x_spitze_px, links_px), links_px + ges_breite_px)
    unterkante = 1.0 - (KASTEN_ABSTAND_OBEN_PT + ges_hoehe_pt) / hoehe_pt
    z.hilfsobjekte["leitlinie"] = ax.annotate(
        "",
        xy=(s.f_sp_hz, s.hoehe),
        xycoords="data",
        xytext=((start_px - x0) / breite_px, unterkante),
        textcoords="axes fraction",
        arrowprops={
            "arrowstyle": "-",
            "color": stil.achse,
            "linewidth": 0.8,
            "shrinkA": 0,
            "shrinkB": _LEITLINIE_ENDE_PT,
        },
        zorder=4.5,
    )
