"""Ansicht 5: eigenes Diagramm aus bis zu vier Serien (R-058/R-059, P-AUSW2 S6).

Eine Zeichenfunktion für Oberfläche und Thesis, GUI-frei und ohne ``pyplot``. Die Serien kommen
aufgelöst aus :mod:`.serien_daten`.

* **Überlagert:** eine Achse, eine Größe; alle Linien tragen ihre eigene Frequenzachse
  (Messungen mit verschiedener Linienzahl, keine Interpolation).
* **Nebeneinander:** ein Teilbild je Gruppe (Größe, Messung), sortiert nach Größe, dann
  Messung, höchstens :data:`TEILBILDER_MAX`; bei mehr als zwei Teilbildern in zwei Spalten
  umgebrochen. Die Frequenzachse ist immer gekoppelt; die y-Achse ist nur zwischen Teilbildern
  gleicher Größe **und** gleicher Einheit gekoppelt. Der Teilbildkopf nennt Kurzname und Größe.
* **Einheit:** Ein Teilbild trägt genau eine Einheit (A-3, siehe
  :func:`~ldv_automation.darstellung.serien_daten.loese_alle_auf`); die y-Achse nennt die der
  ersten sichtbaren Serie.

Linienart und Farbe folgen dem festen ``slot`` der Serie (:meth:`Plotstil.linienart`), damit eine
Serie beim Entfernen einer anderen optisch gleich bleibt. Die Legende steht **einmal** unter dem
Gesamtbild (eigene Zeile des Layouts, bleibt im Rechteck des Arbeitsbildes); sie führt nur
sichtbare Serien. Unsichtbare Serien zählen für die Achsenwahl mit, damit die Grenzen beim
Ein- und Ausblenden gleich bleiben (UI-21). Diagrammtitel gibt es nicht.
"""

from __future__ import annotations

import math
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from typing import Literal

from matplotlib import rc_context
from matplotlib.axes import Axes
from matplotlib.figure import Figure
from matplotlib.lines import Line2D
from matplotlib.text import Text
from matplotlib.ticker import AutoLocator

from .achsen import (
    AchsenOptionen,
    nebenticks_log,
    wende_bereich_an,
    wende_frequenz_an,
    wende_y_gruppe_an,
)
from .formate import achsentitel
from .frf import HINWEIS_PHASE_VORZEICHEN
from .serien_daten import (
    GROESSEN,
    GROESSEN_NAMEN,
    DiagrammDaten,
    DiagrammSerie,
    GroessenId,
    betrag_groesse,
    referenz_serie,
)
from .stil import Plotstil
from .zeichnung import (
    Skala,
    Zeichnung,
    constrained_layout,
    kennzeichen_kopf,
    layout_rect,
    platzhalter_anbringen,
    setze_achsenstil,
)

__all__ = [
    "PLATZHALTER_KEINE_SERIE",
    "TEILBILDER_MAX",
    "Anordnung",
    "DiagrammOptionen",
    "Teilbild",
    "teilbilder",
    "zeichne_diagramm",
]

Anordnung = Literal["ueberlagert", "nebeneinander"]
"""Anordnung der Serien: eine gemeinsame Achse oder ein Teilbild je Gruppe (Größe, Messung)."""

TEILBILDER_MAX = 4
"""Höchstzahl der Teilbilder (so viele wie Serien)."""
PLATZHALTER_KEINE_SERIE = "Keine darstellbare Serie."
"""Text in der leeren Achse, wenn keine Serie gezeichnet werden kann."""
LEGENDE_ANTEIL_MAX = 0.35
"""Größter Anteil der Legendenzeile an der nutzbaren Höhe (der Plot geht vor der Legende)."""


@dataclass(frozen=True, kw_only=True)
class DiagrammOptionen:
    """Darstellungsoptionen von Ansicht 5.

    Attributes
    ----------
    anordnung : {"ueberlagert", "nebeneinander"}
        Überlagert oder ein Teilbild je Gruppe.
    skala : {"linear", "log"}
        Skala der Betragsgrößen (Spektrum, |H1|, |H2|); Kohärenz und Phase sind linear.
    skalen : mapping of str to {"linear", "log"} or None
        Skala je Größe (``"spektrum"``, ``"h1"``, ``"h2"``); fehlende Größen und ``None``
        nehmen ``skala``.
    achsen : AchsenOptionen or None
        Feste Bereiche und Frequenzskala (R-073): Frequenz gemeinsam, y je Größe
        (``"spektrum"``, ``"h1"``, ``"h2"``, ``"phase"`` in Grad; E11, ein Bereich je Größe);
        die Kohärenz bleibt fest 0 bis 1,05. ``None`` = alles automatisch.
    kennzeichen_phase : str or None
        Kennzeichen „unbestätigt (M8 …)“ für gezeichnete Phasenserien (Kopf des Bildes);
        ``None`` = keines.
    """

    anordnung: Anordnung = "ueberlagert"
    skala: Skala = "log"
    skalen: Mapping[str, Skala] | None = None
    achsen: AchsenOptionen | None = None
    kennzeichen_phase: str | None = None

    def __post_init__(self) -> None:
        if self.anordnung not in ("ueberlagert", "nebeneinander"):
            raise ValueError(f"unbekannte Anordnung {self.anordnung!r}")
        if self.skala not in ("linear", "log"):
            raise ValueError(f"unbekannte Skala {self.skala!r}")
        for skala in (self.skalen or {}).values():
            if skala not in ("linear", "log"):
                raise ValueError(f"unbekannte Skala {skala!r}")

    def skala_von(self, groesse: GroessenId) -> Skala:
        """Skala der Größe (je Größe, sonst die allgemeine Skala)."""
        return (self.skalen or {}).get(groesse, self.skala)


@dataclass(frozen=True)
class Teilbild:
    """Ein Teilbild: Serien einer Gruppe (Größe, Messung).

    Attributes
    ----------
    groesse : GroessenId
        Größe des Teilbilds.
    messung_id : int or None
        Messung des Teilbilds (``None`` überlagert: mehrere Messungen).
    kopf : str
        Teilbildkopf („A · |H1|“, überlagert leer).
    serien : tuple of DiagrammSerie
        Serien des Teilbilds in Reihenfolge der Liste.
    """

    groesse: GroessenId
    messung_id: int | None
    kopf: str
    serien: tuple[DiagrammSerie, ...]


def teilbilder(serien: Sequence[DiagrammSerie], anordnung: Anordnung) -> list[Teilbild]:
    """Teilt die Serien in Teilbilder (Regel E10).

    Überlagert gibt es ein Teilbild (alle Serien, Größe der ersten sichtbaren). Nebeneinander
    ein Teilbild je (Größe, Messung), sortiert nach Größe (Reihenfolge :data:`GROESSEN`), dann
    Messung (Reihenfolge der Kennung).
    """
    if not serien:
        return []
    if anordnung == "ueberlagert":
        return [Teilbild(referenz_serie(serien).groesse, None, "", tuple(serien))]
    gruppen: dict[tuple[int, int], list[DiagrammSerie]] = {}
    for s in serien:
        gruppen.setdefault((GROESSEN.index(s.groesse), s.spec.messung_id), []).append(s)
    ergebnis = []
    for (g_index, messung_id), inhalt in sorted(gruppen.items()):
        groesse = GROESSEN[g_index]
        kopf = f"{inhalt[0].kurzname} · {GROESSEN_NAMEN[groesse]}"
        ergebnis.append(Teilbild(groesse, messung_id, kopf, tuple(inhalt)))
    return ergebnis


def _raster(anzahl: int) -> tuple[int, int]:
    """Zeilen und Spalten der Teilbilder: eine Zeile bis zwei Teilbilder, sonst zwei Spalten."""
    if anzahl <= 2:
        return 1, max(anzahl, 1)
    return math.ceil(anzahl / 2), 2


def _legende_pt(stil: Plotstil) -> float:
    """Schriftgröße der Legende: etwas kleiner als die Achsen (kompakt, der Plot geht vor)."""
    return 0.85 * stil.schrift_pt


def _legende_plan(
    fig: Figure, labels: Sequence[str], stil: Plotstil, rect: tuple[float, float, float, float]
) -> tuple[list[str], int, float]:
    """Einträge, Spaltenzahl und Höhenanteil der Legendenzeile (gemessen mit der Schrift).

    Zweizeilige Einträge (Mittel mit Formel und Punktzahl) werden einzeilig gesetzt, wenn die
    Legende dadurch niedriger wird: Sie braucht dann bei kleinem Fenster weniger Plotfläche.
    """
    breite_pt = float(fig.get_figwidth()) * 72.0 * rect[2]
    hoehe_pt = float(fig.get_figheight()) * 72.0 * rect[3]
    k = 72.0 / fig.dpi
    fig.draw_without_rendering()
    varianten = [list(labels)]
    if any("\n" in label for label in labels):
        varianten.append([label.replace("\n", " · ") for label in labels])
    beste: tuple[list[str], int, float] | None = None
    for texte in varianten:
        breiten = []
        for label in texte:
            text = fig.text(0.0, 0.0, label, fontsize=_legende_pt(stil))
            breiten.append(max(float(text.get_window_extent().width) * k, 1.0))
            text.remove()
        eintrag = max(breiten) + 4.5 * _legende_pt(stil)  # Linienprobe und Abstände
        spalten = max(1, min(len(texte), int(breite_pt // eintrag)))
        zeilen_je_eintrag = max(label.count("\n") + 1 for label in texte)
        reihen = math.ceil(len(texte) / spalten)
        noetig_pt = reihen * zeilen_je_eintrag * _legende_pt(stil) * 1.35 + 2.5 * _legende_pt(stil)
        anteil = noetig_pt / hoehe_pt
        if beste is None or anteil < beste[2] - 1e-9:
            beste = (texte, spalten, anteil)
    assert beste is not None  # labels ist nicht leer
    return beste[0], beste[1], min(beste[2], LEGENDE_ANTEIL_MAX)


def zeichne_diagramm(
    fig: Figure, daten: DiagrammDaten, opt: DiagrammOptionen, stil: Plotstil
) -> Zeichnung:
    """Zeichnet das Diagramm in ``fig`` (ohne Diagrammtitel, ohne Stempel).

    Parameters
    ----------
    fig : Figure
        Wird geleert und neu gefüllt; die Größe muss endgültig sein (Messung in pt).
    daten : DiagrammDaten
        Aufgelöste Serien aus :func:`~ldv_automation.darstellung.serien_daten.loese_alle_auf`.
    opt : DiagrammOptionen
        Anordnung, Skala, Achsen, Kennzeichen.
    stil : Plotstil
        Farben, Linienarten, Schrift.

    Returns
    -------
    Zeichnung
        ``achsen`` die Teilbilder in Zeilenreihenfolge, ``rollen`` die Größe je Achse
        (``"spektrum"``, ``"h1"``, ``"h2"``, ``"kohaerenz"``, ``"phase"``; Schlüssel des
        y-Bereichs, E11), ``linien["s<i>"]`` je Serie (``i`` =
        Position in ``daten.serien``), ``hilfsobjekte["legende"]`` und
        ``["legende_eintraege"]`` (Texte der sichtbaren Serien), ``["teilbilder"]`` (Köpfe).

    Raises
    ------
    ldv_automation.darstellung.achsen.AchsenFehler
        Ungültiger Achsenbereich.
    """
    with rc_context(stil.rc()):
        fig.clear()
        constrained_layout(fig)
        teile = teilbilder(daten.serien, opt.anordnung)[:TEILBILDER_MAX]
        if not teile:
            ax = fig.subplots()
            setze_achsenstil(ax, stil)
            z = Zeichnung(figure=fig, achsen=(ax,), rollen=())
            z.texte.append(platzhalter_anbringen(ax, stil, PLATZHALTER_KEINE_SERIE))
            return z
        serien = [s for t in teile for s in t.serien]
        sichtbare = [s for s in serien if s.sichtbar]
        phasen = [s for s in sichtbare if s.groesse == "phase"]
        rect = layout_rect(fig)
        kaesten: list[Text] = []
        if phasen and opt.kennzeichen_phase:
            kaesten, rect = kennzeichen_kopf(fig, stil, [opt.kennzeichen_phase], rect)
            fig.set_layout_engine("constrained", rect=rect)
        labels = [s.legende for s in sichtbare]
        if labels:
            labels, spalten, anteil = _legende_plan(fig, labels, stil, rect)
        else:
            spalten, anteil = 1, 0.0
        zeilen, spaltenzahl = _raster(len(teile))
        ratios = [(1.0 - anteil) / zeilen] * zeilen + ([anteil] if labels else [])
        gs = fig.add_gridspec(len(ratios), spaltenzahl, height_ratios=ratios)

        achsen: list[Axes] = []
        gruppen_y: dict[tuple[GroessenId, str], list[Axes]] = {}
        rollen: list[str] = []
        linien: dict[int, Line2D] = {}
        position = {id(s): i for i, s in enumerate(daten.serien)}
        for i, teil in enumerate(teile):
            r, c = divmod(i, spaltenzahl)
            erste = referenz_serie(teil.serien)
            schluessel_y = (teil.groesse, erste.einheit)  # y nur bei gleicher Größe und Einheit
            teilen_y = gruppen_y.get(schluessel_y)
            ax = fig.add_subplot(
                gs[r, c],
                sharex=achsen[0] if achsen else None,
                sharey=teilen_y[0] if teilen_y else None,
            )
            achsen.append(ax)
            gruppen_y.setdefault(schluessel_y, []).append(ax)
            rollen.append(teil.groesse)
            for s in teil.serien:
                (linie,) = ax.plot(
                    s.frequenz_hz,
                    s.y,
                    linestyle=stil.linienart(s.slot),
                    color=stil.serienfarbe(s.slot),
                    linewidth=stil.linienbreite_pt,
                    label=s.legende,
                )
                linien[position[id(s)]] = linie
            ax.set_ylabel(achsentitel(erste.groesse_name, erste.einheit))
            ax.set_xlabel(achsentitel("Frequenz", "Hz"))
            if opt.anordnung == "nebeneinander":
                ax.set_title(teil.kopf, loc="left", fontsize=stil.schrift_pt)
            if betrag_groesse(teil.groesse) and opt.skala_von(teil.groesse) == "log":
                ax.set_yscale("log", nonpositive="mask")

        _wende_achsen_an(achsen, teile, serien, opt)
        for ax in achsen:
            setze_achsenstil(ax, stil)
            if opt.achsen is not None:
                nebenticks_log(ax, dezimalkomma=stil.dezimalkomma)

        z = Zeichnung(figure=fig, achsen=tuple(achsen), rollen=tuple(rollen))
        z.texte.extend(kaesten)
        for index, linie in linien.items():
            z.linien[f"s{index}"] = linie
            if not daten.serien[index].sichtbar:
                linie.set_visible(False)  # zählt für die Grenzen, wird nicht gezeigt
        _vorzeichen_hinweis(z, achsen, teile, stil)
        if labels:
            ax_legende = fig.add_subplot(gs[-1, :])
            ax_legende.set_axis_off()
            legende = ax_legende.legend(
                handles=[linien[position[id(s)]] for s in sichtbare],
                labels=labels,
                loc="center",
                ncol=spalten,
                fontsize=_legende_pt(stil),
                framealpha=0.9,
                numpoints=1,
            )
            z.hilfsobjekte["legende"] = legende
        z.hilfsobjekte["legende_eintraege"] = labels
        z.hilfsobjekte["teilbilder"] = [t.kopf for t in teile]
        if len(daten.serien) > len(serien):
            z.hinweise = (*z.hinweise, f"Höchstens {TEILBILDER_MAX} Teilbilder; weitere entfallen.")
    return z


def _wende_achsen_an(
    achsen: Sequence[Axes],
    teile: Sequence[Teilbild],
    serien: Sequence[DiagrammSerie],
    opt: DiagrammOptionen,
) -> None:
    """Frequenzbereich (gemeinsam) und y-Bereich je Größe setzen (Gruppen: Größe und Einheit)."""
    f_min = min(float(s.frequenz_hz[0]) for s in serien)
    f_max = max(float(s.frequenz_hz[-1]) for s in serien)
    x_fest = False
    if opt.achsen is None:
        achsen[0].set_xlim(f_min, f_max)
    else:
        if opt.achsen.frequenz_skala == "log" and f_min <= 0.0:
            positiv = [float(f) for s in serien for f in s.frequenz_hz[s.frequenz_hz > 0.0][:1]]
            f_min = min(positiv) if positiv else f_max / 1000.0
        x_fest = wende_frequenz_an(achsen[0], opt.achsen, f_min, f_max)
    je_gruppe: dict[tuple[GroessenId, str], list[Axes]] = {}
    for ax, teil in zip(achsen, teile, strict=True):
        schluessel = (teil.groesse, referenz_serie(teil.serien).einheit)
        je_gruppe.setdefault(schluessel, []).append(ax)
    for (groesse, _einheit), gruppe in je_gruppe.items():
        if groesse == "kohaerenz":
            gruppe[0].set_ylim(0.0, 1.05)
            gruppe[0].set_yticks([0.0, 0.5, 1.0])
        elif groesse == "phase":
            gruppe[0].set_ylim(-180.0, 180.0)
            gruppe[0].set_yticks([-180, -90, 0, 90, 180])
            if opt.achsen is not None and not opt.achsen.y_bereich("phase").ist_auto:
                wende_bereich_an(gruppe[0], opt.achsen.y_bereich("phase"), (-180.0, 180.0), "Phase")
                gruppe[0].yaxis.set_major_locator(AutoLocator())
        elif opt.achsen is not None:
            wende_y_gruppe_an(
                gruppe,
                opt.achsen.y_bereich(groesse),
                log=opt.skala_von(groesse) == "log",
                x_gesetzt=x_fest,
                name="Betrag",
            )


def _vorzeichen_hinweis(
    z: Zeichnung, achsen: Sequence[Axes], teile: Sequence[Teilbild], stil: Plotstil
) -> None:
    """Vorzeichenkonvention der Phase mit Subjekt im Phasen-Teilbild (KONVENTIONEN)."""
    for ax, teil in zip(achsen, teile, strict=True):
        if teil.groesse != "phase":
            continue
        paare = {
            s.spec.kanalpaar: None
            for s in teil.serien
            if s.sichtbar and s.spec.kanalpaar is not None
        }
        if not paare:
            continue
        text = "; ".join(
            HINWEIS_PHASE_VORZEICHEN.format(antwort=a, referenz=r) for a, r in paare if a
        )
        z.texte.append(
            ax.text(
                1.0,
                1.0,
                text,
                transform=ax.transAxes,
                ha="right",
                va="bottom",
                fontsize=stil.schrift_pt * 0.8,
                color=stil.text_gedaempft,
            )
        )
        z.hinweise = (*z.hinweise, f"Phase: {text}")
