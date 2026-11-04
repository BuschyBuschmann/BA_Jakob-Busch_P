"""Ansicht 4: Schwingform als Aufsicht (eine Zeichenfunktion für Oberfläche und Thesis, T2).

Drei Darstellungen:

``"betrag"``
    Betrag je Punkt als Füllung eines Einfarbverlaufs (graustufentauglich) mit Farbleiste.
``"phase_ref"``
    Phase einer Einzelkomponente gegen den Referenzkanal (Datei-Ref1). Sie hängt von der
    Polarität der Referenz ab (Annahme M8); das Kennzeichen „unbestätigt“ übergibt die
    Oberfläche als Text.
``"phase_relativ"``
    Phase relativ zu einem Bezugspunkt (``phase_relativ_rad`` im Kern: arg(v_p · v_ref*));
    unabhängig von M8.

Phase als **Pfeil je Punkt** (Winkel = Phase, Länge proportional zum Betrag) auf einem Punkt, der
zusätzlich mit der **zyklischen Skala** :data:`~.stil.ZYKLISCHE_SKALA` gefüllt ist, dazu eine
Kreislegende. Eine Helligkeit allein kann den Phasenkreis in Graustufen nie eindeutig kodieren
(FA-AUSW F-4c); der Pfeilwinkel trägt die Information. Punkte mit γ² unter γ²_min bleiben im
Bild, sind grau und mit einem Kreuz markiert; ein Bezugspunkt darunter trägt ein Kennzeichen.
Vorzeichen: φ > 0 heißt, der Punkt eilt der Referenz bzw. dem Bezugspunkt voraus
(Zeitabhängigkeit e^{+iωt}). Winkel werden in Grad angezeigt (Rechnung in rad).
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

import numpy as np
from matplotlib import rc_context
from matplotlib.axes import Axes
from matplotlib.cm import ScalarMappable
from matplotlib.colors import Normalize
from matplotlib.figure import Figure

from ldv_automation.auswertung.schwingform import phase_relativ_rad

from .auswahl import (
    _ACHSE_VON_EBENE,
    DarstellungsFehler,
    Ebene,
    SchwingformDaten,
    kanal_der_komponente,
    standard_bezug,
)
from .formate import achsentitel, dezimalkomma_formatter, grad, zahl_text
from .stil import Plotstil
from .zeichnung import Zeichnung, kennzeichen_anbringen, platzhalter_anbringen, setze_achsenstil

__all__ = [
    "PHASE_KEINE_REFERENZ",
    "PHASE_NUR_EINZELKOMPONENTE",
    "Darstellung",
    "SchwingformOptionen",
    "zeichne_schwingform",
]

Darstellung = Literal["betrag", "phase_ref", "phase_relativ"]

PHASE_KEINE_REFERENZ = "Phase nicht verfügbar: keine Referenz."
PHASE_NUR_EINZELKOMPONENTE = "Phase nur für eine Einzelkomponente (X, Y oder Z), nicht für 3D."
KEIN_BEZUGSPUNKT = "Kein Bezugspunkt: kein Punkt mit γ² ≥ γ²_min."

PFEIL_ANTEIL = 0.035
"""Größte Pfeillänge als Anteil der größten Ausdehnung der Projektion."""


@dataclass(frozen=True, kw_only=True)
class SchwingformOptionen:
    """Darstellungsoptionen von Ansicht 4.

    Attributes
    ----------
    darstellung : {"betrag", "phase_ref", "phase_relativ"}
        Betrag (Voreinstellung), Phase gegen die Referenz oder relativ zum Bezugspunkt.
    ebene : {"xy", "xz", "yz"} or None
        Projektionsebene; ``None`` = ``daten.ebene`` (kleinste Ausdehnung entfällt).
    punktlabels : bool
        Punktlabels klein neben den Punkten (abschaltbar).
    bezug : int or None
        0-basierter Bezugspunkt für ``"phase_relativ"``; ``None`` = Voreinstellung
        (:func:`~ldv_automation.darstellung.auswahl.standard_bezug`).
    kennzeichen_phase : str or None
        Kennzeichentext für ``"phase_ref"`` („unbestätigt (M8: …)“); ``None`` = keiner.
    """

    darstellung: Darstellung = "betrag"
    ebene: Ebene | None = None
    punktlabels: bool = True
    bezug: int | None = None
    kennzeichen_phase: str | None = None

    def __post_init__(self) -> None:
        if self.darstellung not in ("betrag", "phase_ref", "phase_relativ"):
            raise ValueError(f"unbekannte Darstellung {self.darstellung!r}")
        if self.ebene is not None and self.ebene not in _ACHSE_VON_EBENE:
            raise ValueError(f"unbekannte Ebene {self.ebene!r}")


def _g2_text(wert: float, stil: Plotstil) -> str:
    """γ² bzw. γ²_min ohne Rundungsverlust (kürzeste Darstellung, 6 signifikante Stellen)."""
    return zahl_text(float(wert), None, dezimalkomma=stil.dezimalkomma)


def _pruefe_bezug(daten: SchwingformDaten, bezug: int) -> None:
    """Prüft einen manuell gewählten Bezugspunkt (Bereich, |v_ref| > 0, Endlichkeit).

    Raises
    ------
    DarstellungsFehler
        ``bezug`` außerhalb ``0 … P-1`` oder ``v_ref`` null bzw. nicht endlich (die relative
        Phase ist dann nicht definiert).
    """
    anzahl = int(daten.label.shape[0])
    if not 0 <= bezug < anzahl:
        raise DarstellungsFehler(f"Bezugspunkt {bezug} existiert nicht (0 … {anzahl - 1}).")
    assert daten.amplitude is not None
    v_ref = complex(daten.amplitude[bezug])
    if not np.isfinite(v_ref) or abs(v_ref) <= 0.0:
        raise DarstellungsFehler(
            f"Bezugspunkt {int(daten.label[bezug])}: Betrag null oder nicht endlich, "
            "die Phase relativ zu ihm ist nicht definiert."
        )


def winkel_zu_skalenwert(phase_rad: np.ndarray) -> np.ndarray:
    """Bildet Winkel auf ``[0, 1)`` der zyklischen Skala ab (-π und +π ergeben denselben Wert).

    Die Skala ist an beiden Enden gleichfarbig; ein Winkel von +179° und -179° liegt damit
    auch farblich 2° auseinander (RF-UI-F4c).
    """
    wrapped = np.mod(np.asarray(phase_rad, dtype=np.float64) + np.pi, 2.0 * np.pi)
    return wrapped / (2.0 * np.pi)


def _pfeile(
    phase_rad: np.ndarray, betrag: np.ndarray, laenge_max: float
) -> tuple[np.ndarray, np.ndarray]:
    endlich = np.where(np.isfinite(betrag), betrag, np.nan)  # inf/NaN: Pfeil der Länge 0
    groesster = np.nanmax(endlich) if np.any(np.isfinite(betrag)) else 0.0
    anteil = np.zeros_like(betrag) if groesster <= 0 else np.nan_to_num(endlich / groesster)
    laenge = laenge_max * anteil
    return laenge * np.cos(phase_rad), laenge * np.sin(phase_rad)


def _farbleiste(
    fig: Figure,
    cax: Axes,
    abbildbar: ScalarMappable,
    titel: str,
    stil: Plotstil,
    ticks: list[float] | None = None,
) -> object:
    cb = fig.colorbar(abbildbar, cax=cax)
    cb.set_label(titel, fontsize=stil.schrift_pt)
    if ticks is not None:
        cb.set_ticks(ticks)
    cb.ax.yaxis.set_major_formatter(dezimalkomma_formatter(dezimalkomma=stil.dezimalkomma))
    cb.ax.tick_params(labelsize=stil.schrift_pt, colors=stil.achse)
    cb.outline.set_edgecolor(stil.achse)
    return cb


def _kreislegende(ax: Axes, stil: Plotstil, hinweis: str) -> None:
    """Kreis mit Pfeilen bei 0°, 90°, ±180°, -90° und der zyklischen Skala als Ring."""
    zyklisch = stil.zyklisch()
    winkel = np.linspace(-np.pi, np.pi, 72, endpoint=False) + np.pi / 72
    ax.scatter(
        np.cos(winkel),
        np.sin(winkel),
        c=winkel_zu_skalenwert(winkel),
        cmap=zyklisch,
        vmin=0.0,
        vmax=1.0,
        s=18,
        edgecolors="none",
    )
    for grad_wert, text in ((0, "0°"), (90, "90°"), (180, "±180°"), (-90, f"{chr(0x2212)}90°")):
        w = np.radians(grad_wert)
        ax.annotate(
            "",
            xy=(0.82 * np.cos(w), 0.82 * np.sin(w)),
            xytext=(0.0, 0.0),
            arrowprops={"arrowstyle": "->", "color": stil.achse, "linewidth": 0.9},
        )
        ax.text(
            1.38 * np.cos(w),
            1.38 * np.sin(w),
            text,
            ha="center",
            va="center",
            fontsize=stil.schrift_pt * 0.8,
            color=stil.achse,
        )
    ax.set_xlim(-1.9, 1.9)
    ax.set_ylim(-1.7, 1.9)
    ax.set_aspect("equal")
    ax.set_axis_off()
    ax.text(
        0.0,
        1.78,
        hinweis,
        ha="center",
        va="bottom",
        fontsize=stil.schrift_pt * 0.8,
        color=stil.achse,
    )


def zeichne_schwingform(
    fig: Figure, daten: SchwingformDaten, opt: SchwingformOptionen, stil: Plotstil
) -> Zeichnung:
    """Zeichnet die Schwingform als Aufsicht in ``fig`` (ohne Titel, ohne Stempel).

    Parameters
    ----------
    fig : Figure
        Wird geleert und neu gefüllt.
    daten : SchwingformDaten
        Aus :func:`~ldv_automation.darstellung.auswahl.schwingform_daten`.
    opt : SchwingformOptionen
        Darstellung, Ebene, Punktlabels, Bezugspunkt, Kennzeichen.
    stil : Plotstil
        Farben, Verlauf, zyklische Skala, Schrift.

    Returns
    -------
    Zeichnung
        ``marker["punkte"]`` (Streudiagramm der Punkte), ``marker["unsicher"]`` (Kreuz der Punkte
        unter γ²_min, falls vorhanden), ``marker["bezug"]`` (Ring um den Bezugspunkt),
        ``hilfsobjekte`` mit ``"pfeile"``, ``"farbleiste"``, ``"kreislegende"``,
        ``"punktlabels"``.

    Raises
    ------
    DarstellungsFehler
        Phase ohne Referenz (:data:`PHASE_KEINE_REFERENZ`) oder für 3D
        (:data:`PHASE_NUR_EINZELKOMPONENTE`); manueller Bezugspunkt außerhalb der Punktliste,
        mit Betrag null oder nicht endlich (vor dem Zeichnen, die Figure bleibt unverändert).
        Ein Bezugspunkt mit γ² < γ²_min wird gezeichnet und im Bild gekennzeichnet.
    """
    if opt.darstellung != "betrag":
        if not daten.phase_gueltig:
            raise DarstellungsFehler(PHASE_KEINE_REFERENZ)
        if daten.amplitude is None:
            raise DarstellungsFehler(PHASE_NUR_EINZELKOMPONENTE)
        if opt.darstellung == "phase_relativ" and opt.bezug is not None:
            _pruefe_bezug(daten, opt.bezug)
    ebene = opt.ebene or daten.ebene
    i, j = _ACHSE_VON_EBENE[ebene]
    x = daten.koordinaten_m[:, i]
    y = daten.koordinaten_m[:, j]
    with rc_context(stil.rc()):
        fig.clear()
        fig.set_layout_engine("constrained")
        gs = fig.add_gridspec(1, 2, width_ratios=[1.0, 0.3])
        ax = fig.add_subplot(gs[0, 0])
        rechts = fig.add_subplot(gs[0, 1])
        rechts.set_axis_off()
        z = Zeichnung(figure=fig, achsen=(ax,))
        ax.set_aspect("equal", adjustable="datalim")
        ax.margins(0.1)
        ax.set_xlabel(achsentitel(ebene[0], "m"))
        ax.set_ylabel(achsentitel(ebene[1], "m"))
        ausdehnung = max(float(np.ptp(x)), float(np.ptp(y)), 1e-9)
        if opt.darstellung == "betrag":
            punkte = ax.scatter(
                x,
                y,
                c=daten.betrag,
                cmap=stil.verlauf(),
                s=46,
                edgecolors=stil.achse,
                linewidths=0.6,
                zorder=3,
            )
            z.marker["punkte"] = punkte
            cax = rechts.inset_axes((0.1, 0.05, 0.3, 0.9))
            z.hilfsobjekte["farbleiste"] = _farbleiste(
                fig, cax, punkte, achsentitel(f"Betrag {daten.komponente}", daten.einheit), stil
            )
        else:
            _phase_zeichnen(fig, ax, rechts, z, daten, opt, stil, x, y, ausdehnung)
        if opt.punktlabels:
            z.hilfsobjekte["punktlabels"] = [
                ax.annotate(
                    str(int(label)),
                    (px, py),
                    xytext=(3, 3),
                    textcoords="offset points",
                    fontsize=stil.schrift_pt * 0.65,
                    color=stil.text_gedaempft,
                    zorder=4,
                )
                for label, px, py in zip(daten.label, x, y, strict=True)
            ]
        setze_achsenstil(ax, stil)
    return z


def _phase_zeichnen(
    fig: Figure,
    ax: Axes,
    rechts: Axes,
    z: Zeichnung,
    daten: SchwingformDaten,
    opt: SchwingformOptionen,
    stil: Plotstil,
    x: np.ndarray,
    y: np.ndarray,
    ausdehnung: float,
) -> None:
    assert daten.amplitude is not None
    betrag = np.abs(daten.amplitude)
    bezug: int | None = None
    if opt.darstellung == "phase_relativ":
        bezug = opt.bezug if opt.bezug is not None else standard_bezug(daten)
        if bezug is None:
            z.texte.append(platzhalter_anbringen(ax, stil, KEIN_BEZUGSPUNKT))
            ax.scatter(x, y, c=stil.text_gedaempft, s=30, zorder=3)
            return
        phase = phase_relativ_rad(daten.amplitude, bezug)
        bezug_label = int(daten.label[bezug])
        titel = f"Phase relativ zu Punkt {bezug_label} [°]"
        hinweis = f"Δφ > 0: Punkt eilt Punkt {bezug_label} voraus"
    else:
        phase = np.angle(daten.amplitude)
        titel = f"Phase gegen {daten.referenz} [°]"
        ziel = daten.referenz or "der Referenz"
        hinweis = f"φ > 0: {kanal_der_komponente(daten.komponente)} eilt {ziel} voraus"
        if opt.kennzeichen_phase is not None:
            z.texte.append(kennzeichen_anbringen(ax, stil, opt.kennzeichen_phase))
    unsicher = np.zeros(x.shape, dtype=bool) if daten.kohaerenz_ok is None else ~daten.kohaerenz_ok
    if bezug is not None and unsicher[bezug]:
        g2_bezug = ""
        if daten.kohaerenz is not None:
            g2_bezug = f"γ² = {_g2_text(float(daten.kohaerenz[bezug]), stil)} < "
        z.texte.append(
            kennzeichen_anbringen(
                ax,
                stil,
                f"Bezugspunkt {int(daten.label[bezug])} unsicher: {g2_bezug}"
                f"γ²_min = {_g2_text(daten.kohaerenz_min or 0.0, stil)}",
            )
        )
    sicher = ~unsicher
    zyklisch = stil.zyklisch()
    skala = winkel_zu_skalenwert(phase)
    punkte = ax.scatter(
        x[sicher],
        y[sicher],
        c=skala[sicher],
        cmap=zyklisch,
        vmin=0.0,
        vmax=1.0,
        s=46,
        edgecolors=stil.achse,
        linewidths=0.6,
        zorder=3,
    )
    z.marker["punkte"] = punkte
    u, v = _pfeile(phase, betrag, PFEIL_ANTEIL * ausdehnung)
    pfeile = ax.quiver(
        x[sicher],
        y[sicher],
        u[sicher],
        v[sicher],
        angles="xy",
        scale_units="xy",
        scale=1.0,
        color=stil.achse,
        width=0.004,
        pivot="tail",
        zorder=4,
    )
    z.hilfsobjekte["pfeile"] = pfeile
    if np.any(unsicher):
        ax.scatter(
            x[unsicher],
            y[unsicher],
            c=stil.gitter,
            s=46,
            edgecolors=stil.text_gedaempft,
            linewidths=0.6,
            zorder=3,
        )
        g2_min_text = _g2_text(daten.kohaerenz_min or 0.0, stil)
        (kreuz,) = ax.plot(
            x[unsicher],
            y[unsicher],
            linestyle="none",
            marker="x",
            markersize=6,
            color=stil.achse,
            zorder=5,
            label=f"γ² < {g2_min_text}: Phase unsicher",
        )
        z.marker["unsicher"] = kreuz
        ax.legend(
            handles=[kreuz], loc="best", fontsize=stil.schrift_pt, framealpha=0.9, numpoints=1
        )
    if bezug is not None:
        (ring,) = ax.plot(
            [x[bezug]],
            [y[bezug]],
            linestyle="none",
            marker="o",
            markersize=14,
            markerfacecolor="none",
            markeredgecolor=stil.achse,
            markeredgewidth=1.6,
            zorder=6,
        )
        z.marker["bezug"] = ring
    kl = rechts.inset_axes((0.0, 0.62, 1.0, 0.36))
    _kreislegende(kl, stil, hinweis)
    z.hilfsobjekte["kreislegende"] = kl
    cax = rechts.inset_axes((0.1, 0.05, 0.3, 0.5))
    abbildbar = ScalarMappable(norm=Normalize(-180.0, 180.0), cmap=zyklisch)
    z.hilfsobjekte["farbleiste"] = _farbleiste(
        fig, cax, abbildbar, titel, stil, ticks=[-180, -90, 0, 90, 180]
    )
    z.hilfsobjekte["winkel_grad"] = grad(phase)
