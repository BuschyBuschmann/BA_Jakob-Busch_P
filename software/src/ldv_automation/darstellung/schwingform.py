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

Phase als **Pfeil je Punkt** (Winkel = Phase, Länge für alle Punkte gleich 0,8·d_NN; der Betrag
steht in der Markerfläche, ADR-025) auf einem Punkt, der zusätzlich mit der **zyklischen Skala**
:data:`~.stil.ZYKLISCHE_SKALA` gefüllt ist, dazu eine Kreislegende. Eine Helligkeit allein kann
den Phasenkreis in Graustufen nie eindeutig kodieren (FA-AUSW F-4c); der Pfeilwinkel trägt die
Information. Punkte mit γ² unter γ²_min bleiben im Bild, sind grau und mit einem Kreuz markiert,
M6-ungültige Punkte sind hohle Rauten (ohne Pfeil); ein Bezugspunkt darunter trägt ein
Kennzeichen.
Vorzeichen: φ > 0 heißt, der Punkt eilt der Referenz bzw. dem Bezugspunkt voraus
(Zeitabhängigkeit e^{+iωt}). Winkel werden in Grad angezeigt (Rechnung in rad).
"""

from __future__ import annotations

import textwrap
from dataclasses import dataclass
from typing import Literal

import numpy as np
from matplotlib import patheffects, rc_context
from matplotlib.axes import Axes
from matplotlib.cm import ScalarMappable
from matplotlib.colors import Normalize
from matplotlib.figure import Figure
from matplotlib.legend import Legend
from matplotlib.lines import Line2D
from matplotlib.text import Annotation

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
from .zeichnung import (
    Zeichnung,
    kennzeichen_anbringen,
    layout_rect,
    platzhalter_anbringen,
    setze_achsenstil,
)

__all__ = [
    "HINWEIS_LABELS_AUS",
    "HINWEIS_PFEILE_KURZ",
    "PHASE_KEINE_REFERENZ",
    "PHASE_NUR_EINZELKOMPONENTE",
    "Darstellung",
    "SchwingformOptionen",
    "bildgroesse_schwingform",
    "zeichne_schwingform",
]

Darstellung = Literal["betrag", "phase_ref", "phase_relativ"]

PHASE_KEINE_REFERENZ = "Phase nicht verfügbar: keine Referenz."
PHASE_NUR_EINZELKOMPONENTE = "Phase nur für eine Einzelkomponente (X, Y oder Z), nicht für 3D."
KEIN_BEZUGSPUNKT = "Kein Bezugspunkt: kein Punkt mit γ² ≥ γ²_min."

PFEIL_ANTEIL_DNN = 0.8
"""Pfeillänge als Vielfaches des Medians d_NN der Abstände zum nächsten Nachbarn (ADR-025)."""
PFEIL_MIN_PT = 10.0
"""Unter dieser Pfeillänge (in pt) meldet ``Zeichnung.hinweise`` einen zu kleinen Maßstab."""
HINWEIS_PFEILE_KURZ = "Pfeile kürzer als 10 pt: größeres Bild oder Ausschnitt wählen"
HINWEIS_LABELS_AUS = "Punktlabels ausgeblendet: Punkte zu dicht"
_MARKER_ANTEIL = 0.22  # r_max ≤ 0,22 · d_pt, damit die Pfeilspitze den Nachbarmarker nicht deckt
_MARKER_MAX_PT = 5.5
_MARKER_MIN_PT = 2.5
_BETRAG_ANTEIL = 0.35
_BETRAG_MAX_PT = 6.5
_RING_PLUS_PT = 3.0


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


def _abstand_naechster(x: np.ndarray, y: np.ndarray) -> float | None:
    """Median d_NN der Abstände zum nächsten Nachbarn (Abstand 0 zählt nicht), sonst ``None``."""
    pts = np.column_stack([x, y])
    pts = pts[np.isfinite(pts).all(axis=1)]
    if pts.shape[0] < 2:
        return None
    kleinste = np.full(pts.shape[0], np.inf)
    for i0 in range(0, pts.shape[0], 512):
        block = pts[i0 : i0 + 512]
        dist = np.hypot(block[:, None, 0] - pts[None, :, 0], block[:, None, 1] - pts[None, :, 1])
        dist[dist <= 0.0] = np.inf
        kleinste[i0 : i0 + 512] = dist.min(axis=1)
    kleinste = kleinste[np.isfinite(kleinste)]
    return float(np.median(kleinste)) if kleinste.size else None


def achsengrenzen(
    x: np.ndarray, y: np.ndarray, d_nn: float
) -> tuple[tuple[float, float], tuple[float, float]]:
    """Achsengrenzen: Bounding-Box der Punkte ± pad (Layout 4.1).

    ``pad = max(0,9·d_NN, 0,05·L_max)``; je Richtung mindestens ``0,25·L_max + 2·pad``, damit
    Punktreihen nicht zur Linie entarten. NaN-Koordinaten zählen nicht.
    """
    xs, ys = x[np.isfinite(x)], y[np.isfinite(y)]
    if xs.size == 0 or ys.size == 0:
        return (-1.0, 1.0), (-1.0, 1.0)
    laenge = max(float(np.ptp(xs)), float(np.ptp(ys)))
    pad = max(0.9 * d_nn, 0.05 * laenge)
    mindest = 0.25 * laenge + 2 * pad
    grenzen = []
    for werte in (xs, ys):
        unten, oben = float(werte.min()) - pad, float(werte.max()) + pad
        fehlt = mindest - (oben - unten)
        if fehlt > 0:
            unten, oben = unten - fehlt / 2, oben + fehlt / 2
        grenzen.append((unten, oben))
    return grenzen[0], grenzen[1]


def bildgroesse_schwingform(
    daten: SchwingformDaten,
    *,
    breite_cm: float = 11.5,
    ebene: Ebene | None = None,
    hoehe_max_cm: float = 17.0,
) -> tuple[float, float]:
    """Bildgröße in Zoll aus dem Seitenverhältnis der Punktwolke (Layout 4.2, Thesis-Abbildung).

    Hochformatdaten (hier 0,2 m mal 0,5 m) füllen ein Querformatbild nie; die Höhe folgt aus der
    Breite der Plotspalte (Bildbreite abzüglich rechter Spalte und Rändern) geteilt durch das
    Seitenverhältnis ``q`` der Achsengrenzen, begrenzt auf ``hoehe_max_cm``. Die Ränder sind
    Schätzwerte für Achsentitel und Ticks bei 9 pt.

    Returns
    -------
    tuple of float
        ``(Breite, Höhe)`` in Zoll.
    """
    i, j = _ACHSE_VON_EBENE[ebene or daten.ebene]
    x, y = daten.koordinaten_m[:, i], daten.koordinaten_m[:, j]
    d_nn = _abstand_naechster(x, y) or 0.01
    xlim, ylim = achsengrenzen(x, y, d_nn)
    q = (xlim[1] - xlim[0]) / (ylim[1] - ylim[0])
    breite_pt = breite_cm / 2.54 * 72.0
    spalte = max(1.7 * 72.0, 0.22 * breite_pt)
    plot_b = max(breite_pt - spalte - 6.0 - 48.0 - 10.0 - 8.0, 20.0)
    hoehe_pt = plot_b / q + 36.0 + 8.0 + 8.0
    hoehe_pt = min(max(hoehe_pt, 0.5 * breite_pt), hoehe_max_cm / 2.54 * 72.0)
    return breite_pt / 72.0, hoehe_pt / 72.0


def _platziere(
    fig: Figure,
    ax: Axes,
    rechts: Axes,
    rect: tuple[float, float, float, float],
    q: float,
) -> None:
    """Setzt Plotachse und rechte Spalte (Layout 4.2): Randspalte | Plot | rechts | Randspalte.

    Zwei Schritte: Die Ränder für Achsentitel und Ticks werden an der provisorisch gesetzten Achse
    gemessen; daraus folgen Größe (Höhe voll genutzt, Breite durch ``q`` bestimmt, sonst durch die
    Spaltenbreite begrenzt) und mittige Lage des Inhalts.
    """
    breite_in, hoehe_in = (float(w) for w in fig.get_size_inches())
    bild_b, bild_h = breite_in * 72.0, hoehe_in * 72.0
    fx0, fy0, fw, fh = rect
    verf_b, verf_h = fw * bild_b, fh * bild_h
    fig.draw_without_rendering()
    k = 72.0 / fig.dpi
    tight = ax.get_tightbbox()
    assert tight is not None
    box = ax.get_window_extent()
    ex_l = max((float(box.x0) - float(tight.x0)) * k, 0.0)
    ex_r = max((float(tight.x1) - float(box.x1)) * k, 0.0)
    ex_u = max((float(box.y0) - float(tight.y0)) * k, 0.0)
    ex_o = max((float(tight.y1) - float(box.y1)) * k, 0.0)
    rand, luecke = 4.0, 6.0
    spalte = max(1.7 * 72.0, 0.22 * bild_b)
    hb = max(verf_h - ex_u - ex_o - 2 * rand, 20.0)
    wb = q * hb
    wb_max = max(verf_b - spalte - luecke - ex_l - ex_r - 2 * rand, 20.0)
    if wb > wb_max:
        wb, hb = wb_max, wb_max / q
    links = max((verf_b - (ex_l + wb + ex_r + luecke + spalte)) / 2.0, 0.0)
    x_ax = fx0 * bild_b + links + ex_l
    y_ax = fy0 * bild_h + rand + ex_u + (verf_h - 2 * rand - ex_u - ex_o - hb) / 2.0
    ax.set_position((x_ax / bild_b, y_ax / bild_h, wb / bild_b, hb / bild_h))
    ax.apply_aspect()
    x_r = x_ax + wb + ex_r + luecke
    rechts.set_position((x_r / bild_b, y_ax / bild_h, spalte / bild_b, hb / bild_h))


def _radien(
    beitrag: np.ndarray, normal: np.ndarray, d_pt: float, *, einheitlich: bool
) -> tuple[np.ndarray, float]:
    """Markerradien in pt und ``r_max`` (Layout 4.3).

    Phasendarstellung: Fläche ∝ |v|, ``r = r_max·√(|v|/|v|max)`` (mindestens 0,35·r_max und
    1,5 pt), ``r_max = min(0,22·d_pt, 5,5 pt)``, mindestens 2,5 pt. Betragsdarstellung: ein
    Radius ``min(0,35·d_pt, 6,5 pt)``, mindestens 2,5 pt (der Betrag steht in der Füllung).
    """
    if einheitlich:
        r_max = max(min(_BETRAG_ANTEIL * d_pt, _BETRAG_MAX_PT), _MARKER_MIN_PT)
        return np.full(beitrag.shape, r_max), r_max
    r_max = max(min(_MARKER_ANTEIL * d_pt, _MARKER_MAX_PT), _MARKER_MIN_PT)
    groesst = float(np.max(beitrag[normal])) if np.any(normal) else 0.0
    anteil = np.sqrt(beitrag / groesst) if groesst > 0 else np.zeros_like(beitrag)
    r = np.where(normal, r_max * anteil, r_max)
    return np.maximum(r, max(0.35 * r_max, 1.5)), r_max


def _abstand_zu_rechteck(
    px: np.ndarray, py: np.ndarray, x0: float, y0: float, x1: float, y1: float
) -> np.ndarray:
    return np.hypot(
        np.maximum(np.maximum(x0 - px, px - x1), 0.0), np.maximum(np.maximum(y0 - py, py - y1), 0.0)
    )


def _platziere_labels(
    ax: Axes,
    x: np.ndarray,
    y: np.ndarray,
    label: np.ndarray,
    radius_pt: np.ndarray,
    winkel_pfeil: np.ndarray,
    hat_pfeil: np.ndarray,
    r_ring: tuple[int, float] | None,
    laenge_pt: float,
    d_pt: float,
    r_max: float,
    stil: Plotstil,
) -> list[Annotation] | None:
    """Punktlabels gegenüber dem Pfeil (Layout 4.7); ``None``, wenn sie nicht frei passen.

    Das Label steht in Richtung φ + 180° (ohne Pfeil: 45°) mit 2 pt Abstand zum Markerrand. Trifft
    es Marker, Pfeil, Bezugsring, anderes Label oder den Achsenrand, wird der Reihe nach in die
    Nachbarrichtungen ausgewichen; findet ein Label keinen Platz, entfallen alle Labels.
    """
    k = 72.0 / ax.figure.dpi
    mitte = ax.transData.transform(np.column_stack([x, y])) * k
    box = ax.get_window_extent()
    gx0, gy0, gx1, gy1 = (float(v) * k for v in (box.x0, box.y0, box.x1, box.y1))
    texte: list[Annotation] = []
    breiten, hoehen = [], []
    for lab, px, py in zip(label, x, y, strict=True):
        a = ax.annotate(
            str(int(lab)),
            (px, py),
            xytext=(0, 0),
            textcoords="offset points",
            fontsize=stil.schrift_pt * 0.75,
            color=stil.text_gedaempft,
            zorder=4.2,
            path_effects=[patheffects.withStroke(linewidth=1.5, foreground=stil.flaeche)],
        )
        ext = a.get_window_extent()
        breiten.append(float(ext.width) * k)
        hoehen.append(float(ext.height) * k)
        texte.append(a)

    def entfernen() -> None:
        for a in texte:
            a.remove()

    if d_pt < 2 * r_max + 4.0 + max(breiten, default=0.0):
        entfernen()
        return None
    ring_c = None if r_ring is None else (mitte[r_ring[0]], r_ring[1] + 0.65)
    s_t = np.linspace(0.0, 1.0, 17)
    pfeil_pkt = [
        np.column_stack(
            [
                mitte[i, 0] + s_t * laenge_pt * np.cos(winkel_pfeil[i]),
                mitte[i, 1] + s_t * laenge_pt * np.sin(winkel_pfeil[i]),
            ]
        )
        for i in np.flatnonzero(hat_pfeil)
    ]
    pfeil_alle = np.vstack(pfeil_pkt) if pfeil_pkt else np.empty((0, 2))
    belegt: list[tuple[float, float, float, float]] = []
    stufen = (0, 1, -1, 2, -2, 3, -3, 4)
    for i, a in enumerate(texte):
        w, h = breiten[i], hoehen[i]
        basis = winkel_pfeil[i] + np.pi if hat_pfeil[i] else np.pi / 4
        gewaehlt = False
        for stufe in stufen:
            theta = basis + stufe * np.pi / 4
            c, s_ = float(np.cos(theta)), float(np.sin(theta))
            abstand = float(radius_pt[i]) + 2.0
            if r_ring is not None and i == r_ring[0]:
                abstand = r_ring[1] + 0.65 + 2.0  # außerhalb des Bezugsrings
            ax_, ay_ = mitte[i, 0] + abstand * c, mitte[i, 1] + abstand * s_
            ha: Literal["left", "center", "right"] = (
                "left" if c > 0.3 else "right" if c < -0.3 else "center"
            )
            va: Literal["bottom", "center", "top"] = (
                "bottom" if s_ > 0.3 else "top" if s_ < -0.3 else "center"
            )
            x0 = ax_ if ha == "left" else ax_ - w if ha == "right" else ax_ - w / 2
            y0 = ay_ if va == "bottom" else ay_ - h if va == "top" else ay_ - h / 2
            x1, y1 = x0 + w, y0 + h
            if x0 < gx0 or x1 > gx1 or y0 < gy0 or y1 > gy1:
                continue
            if np.any(
                _abstand_zu_rechteck(mitte[:, 0], mitte[:, 1], x0, y0, x1, y1) < radius_pt + 0.8
            ):
                continue
            if ring_c is not None and (
                float(
                    _abstand_zu_rechteck(
                        np.array([ring_c[0][0]]), np.array([ring_c[0][1]]), x0, y0, x1, y1
                    )[0]
                )
                < ring_c[1]
            ):
                continue
            if pfeil_alle.shape[0] and np.any(
                _abstand_zu_rechteck(pfeil_alle[:, 0], pfeil_alle[:, 1], x0, y0, x1, y1) < 2.0
            ):
                continue
            if any(
                x0 < bx1 + 1 and bx0 < x1 + 1 and y0 < by1 + 1 and by0 < y1 + 1
                for bx0, by0, bx1, by1 in belegt
            ):
                continue
            belegt.append((x0, y0, x1, y1))
            a.xyann = (abstand * c, abstand * s_)
            a.set_horizontalalignment(ha)
            a.set_verticalalignment(va)
            gewaehlt = True
            break
        if not gewaehlt:
            entfernen()
            return None
    return texte


def _erklaerung(
    rechts: Axes,
    stil: Plotstil,
    eintraege: list[tuple[Line2D, str]],
    y_oben: float,
    spalte_pt: float,
) -> Legend | None:
    """Zeichenerklärung (Symbol vor dem Wort) in der rechten Spalte, umbrochen auf Spaltenbreite."""
    if not eintraege:
        return None
    zeichen = max(int((spalte_pt - 26.0) / (0.55 * stil.schrift_pt)), 8)
    k = 72.0 / rechts.figure.dpi
    legende: Legend | None = None
    for _ in range(8):
        if legende is not None:
            legende.remove()
        legende = rechts.legend(
            handles=[h for h, _ in eintraege],
            labels=[textwrap.fill(t, zeichen) for _, t in eintraege],
            loc="upper left",
            bbox_to_anchor=(0.0, y_oben),
            borderaxespad=0.0,
            frameon=False,
            fontsize=stil.schrift_pt,
            handlelength=1.2,
            handletextpad=0.5,
            labelspacing=0.6,
            numpoints=1,
        )
        if float(legende.get_window_extent().width) * k <= spalte_pt or zeichen <= 8:
            break
        zeichen -= 2
    return legende


def zeichne_schwingform(
    fig: Figure, daten: SchwingformDaten, opt: SchwingformOptionen, stil: Plotstil
) -> Zeichnung:
    """Zeichnet die Schwingform als Aufsicht in ``fig`` (ohne Titel, ohne Stempel).

    Layout (K-AUSW-LAYOUT 4.1 bis 4.9): Achse mit gleichem Maßstab (``adjustable="box"``) und
    Grenzen aus der Punktwolke, rechts eine Spalte mit Kreislegende, Zeichenerklärung und
    Farbleiste. Alle Größen in pt (Marker, Pfeile, Labels) folgen aus dem gemessenen Maßstab; die
    Figure muss deshalb ihre endgültige Größe haben, bei Größenänderung ist neu zu zeichnen.

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
        ``marker["punkte"]`` (Streudiagramm der gewöhnlichen Punkte), ``marker["unsicher"]``
        (Kreuz der Punkte unter γ²_min, falls vorhanden), ``marker["ungueltig"]`` (Rauten der
        M6-ungültigen Punkte, falls vorhanden), ``marker["bezug"]`` (Ring um den Bezugspunkt),
        ``hilfsobjekte`` mit ``"pfeile"``, ``"farbleiste"``, ``"kreislegende"``,
        ``"punktlabels"`` (nur wenn gezeigt), ``"zeichenerklaerung"``, ``"punktzahl"``,
        ``"radius_pt"`` (Markerradius je Punkt), ``"r_max_pt"``, ``"d_pt"``, ``"d_nn_m"``,
        ``"pt_je_m"``; ``hinweise`` mit Pfeil- und Labelhinweisen.

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
    anzahl = int(x.shape[0])
    phase_modus = opt.darstellung != "betrag"
    rect = layout_rect(fig)
    with rc_context(stil.rc()):
        fig.clear()
        fig.set_layout_engine("none")
        ax = fig.add_axes((0.1, 0.1, 0.5, 0.8))
        rechts = fig.add_axes((0.7, 0.1, 0.25, 0.8))
        rechts.set_axis_off()
        z = Zeichnung(figure=fig, achsen=(ax,))
        d_nn = _abstand_naechster(x, y)
        if d_nn is None:  # ein Punkt oder alle identisch: Maßstab frei wählbar
            xs, ys = x[np.isfinite(x)], y[np.isfinite(y)]
            spanne = max(
                float(np.ptp(xs)) if xs.size else 0.0, float(np.ptp(ys)) if ys.size else 0.0
            )
            d_nn = spanne if spanne > 0 else 0.01
        xlim, ylim = achsengrenzen(x, y, d_nn)
        ax.set_xlim(*xlim)
        ax.set_ylim(*ylim)
        ax.set_aspect("equal", adjustable="box")
        ax.set_anchor("C")
        ax.set_xlabel(achsentitel(ebene[0], "m"))
        ax.set_ylabel(achsentitel(ebene[1], "m"))
        setze_achsenstil(ax, stil)

        # --- Größen je Punkt und Kennzeichen (vor dem Layout, die Texte zählen zum Rand) ---
        phase: np.ndarray | None = None
        bezug: int | None = None
        titel = ""
        hinweis = ""
        if phase_modus:
            assert daten.amplitude is not None
            beitrag = np.abs(daten.amplitude).astype(np.float64)
            if opt.darstellung == "phase_relativ":
                bezug = opt.bezug if opt.bezug is not None else standard_bezug(daten)
                if bezug is None:
                    z.texte.append(platzhalter_anbringen(ax, stil, KEIN_BEZUGSPUNKT))
                    _platziere(fig, ax, rechts, rect, (xlim[1] - xlim[0]) / (ylim[1] - ylim[0]))
                    ax.scatter(x, y, c=stil.text_gedaempft, s=30, zorder=3)
                    return z
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
        else:
            beitrag = np.asarray(daten.betrag, dtype=np.float64)
        ungueltig = ~daten.gueltig | ~np.isfinite(beitrag)
        unsicher = np.zeros(anzahl, dtype=bool)
        if phase_modus and daten.kohaerenz_ok is not None:
            unsicher = ~daten.kohaerenz_ok & ~ungueltig
        if (
            bezug is not None
            and phase_modus
            and daten.kohaerenz_ok is not None
            and not daten.kohaerenz_ok[bezug]
        ):
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
        normal = ~ungueltig & ~unsicher

        # --- Layout und Maßstab ---
        _platziere(fig, ax, rechts, rect, (xlim[1] - xlim[0]) / (ylim[1] - ylim[0]))
        k = 72.0 / fig.dpi
        pt_je_m = float(ax.get_window_extent().width) * k / (xlim[1] - xlim[0])
        d_pt = d_nn * pt_je_m
        radius, r_max = _radien(
            np.where(np.isfinite(beitrag), beitrag, 0.0), normal, d_pt, einheitlich=not phase_modus
        )
        r_med = float(np.median(radius[normal])) if np.any(normal) else r_max
        radius = np.where(normal, radius, r_med)
        z.hilfsobjekte.update(
            radius_pt=radius, r_max_pt=r_max, d_pt=d_pt, d_nn_m=d_nn, pt_je_m=pt_je_m
        )

        # --- Punkte ---
        if phase_modus:
            assert phase is not None
            zyklisch = stil.zyklisch()
            farbe = winkel_zu_skalenwert(phase)
            punkte = ax.scatter(
                x[normal], y[normal], c=farbe[normal], cmap=zyklisch, vmin=0.0, vmax=1.0,
                s=(2 * radius[normal]) ** 2, edgecolors=stil.achse, linewidths=0.6, zorder=3,
            )  # fmt: skip
        else:
            werte = beitrag[normal]
            vmin, vmax = (float(werte.min()), float(werte.max())) if werte.size else (0.0, 1.0)
            punkte = ax.scatter(
                x[normal], y[normal], c=werte, cmap=stil.verlauf(),
                norm=Normalize(vmin, vmax if vmax > vmin else vmin + 1.0),
                s=(2 * radius[normal]) ** 2, edgecolors=stil.achse, linewidths=0.6, zorder=3,
            )  # fmt: skip
        z.marker["punkte"] = punkte
        arrow = np.zeros(anzahl, dtype=bool)
        laenge_m = PFEIL_ANTEIL_DNN * d_nn
        if phase_modus:
            assert phase is not None
            arrow = normal & (beitrag > 0.0)
            pfeile = ax.quiver(
                x[arrow], y[arrow],
                laenge_m * np.cos(phase[arrow]), laenge_m * np.sin(phase[arrow]),
                angles="xy", scale_units="xy", scale=1.0, units="inches", width=1.4 / 72.0,
                headwidth=4, headlength=5, headaxislength=4.5, pivot="tail",
                color=stil.achse, zorder=4,
            )  # fmt: skip
            pfeile.set_path_effects(
                [patheffects.withStroke(linewidth=1.6, foreground=stil.flaeche)]
            )
            z.hilfsobjekte["pfeile"] = pfeile
            if PFEIL_ANTEIL_DNN * d_pt < PFEIL_MIN_PT:
                z.hinweise = (*z.hinweise, HINWEIS_PFEILE_KURZ)
        if np.any(unsicher):
            ax.scatter(
                x[unsicher], y[unsicher], c=stil.gitter, s=(2 * r_med) ** 2,
                edgecolors=stil.text_gedaempft, linewidths=0.6, zorder=3,
            )  # fmt: skip
            g2_min_text = _g2_text(daten.kohaerenz_min or 0.0, stil)
            (kreuz,) = ax.plot(
                x[unsicher], y[unsicher], linestyle="none", marker="x", markersize=1.4 * r_med,
                color=stil.achse, zorder=5,
                label=f"γ² < {g2_min_text}: Phase unsicher ({int(np.sum(unsicher))})",
            )  # fmt: skip
            z.marker["unsicher"] = kreuz
        if np.any(ungueltig):
            z.marker["ungueltig"] = ax.scatter(
                x[ungueltig], y[ungueltig], marker="D", s=(2 * r_med) ** 2 / 2.0,
                facecolors=stil.flaeche, edgecolors=stil.text_gedaempft, linewidths=1.0, zorder=3,
            )  # fmt: skip
        if bezug is not None:
            (ring,) = ax.plot(
                [x[bezug]], [y[bezug]], linestyle="none", marker="o",
                markersize=2 * (r_max + _RING_PLUS_PT), markerfacecolor="none",
                markeredgecolor=stil.achse, markeredgewidth=1.3, zorder=3.5,
            )  # fmt: skip
            z.marker["bezug"] = ring

        # --- Punktlabels ---
        if opt.punktlabels:
            winkel = phase if phase is not None else np.zeros(anzahl)
            labels = _platziere_labels(
                ax, x, y, daten.label, radius, winkel, arrow,
                None if bezug is None else (bezug, r_max + _RING_PLUS_PT),
                PFEIL_ANTEIL_DNN * d_pt, d_pt, r_max, stil,
            )  # fmt: skip
            if labels is None:
                z.hinweise = (*z.hinweise, HINWEIS_LABELS_AUS)
            else:
                z.hilfsobjekte["punktlabels"] = labels

        # --- rechte Spalte ---
        spalte_pt = float(rechts.get_window_extent().width) * k
        y_oben = 1.0
        if phase_modus:
            kl = rechts.inset_axes((0.0, 0.62, 1.0, 0.36))
            _kreislegende(kl, stil, hinweis)
            z.hilfsobjekte["kreislegende"] = kl
            y_oben = 0.58
        eintraege: list[tuple[Line2D, str]] = []
        if np.any(unsicher):
            eintraege.append(
                (
                    Line2D([], [], linestyle="none", marker="x", color=stil.achse, markersize=6),
                    f"γ² < {_g2_text(daten.kohaerenz_min or 0.0, stil)}: Phase unsicher "
                    f"({int(np.sum(unsicher))})",
                )
            )
        if np.any(ungueltig):
            eintraege.append(
                (
                    Line2D([], [], linestyle="none", marker="D", markersize=6,
                           markerfacecolor=stil.flaeche, markeredgecolor=stil.text_gedaempft),
                    f"ungültig (M6) ({int(np.sum(ungueltig))})",
                )
            )  # fmt: skip
        if bezug is not None:
            eintraege.append(
                (
                    Line2D([], [], linestyle="none", marker="o", markersize=8,
                           markerfacecolor="none", markeredgecolor=stil.achse, markeredgewidth=1.3),
                    f"Bezugspunkt {int(daten.label[bezug])}",
                )
            )  # fmt: skip
        legende = _erklaerung(rechts, stil, eintraege, y_oben, spalte_pt)
        y_unten = y_oben
        if legende is not None:
            z.hilfsobjekte["zeichenerklaerung"] = legende
            ext = legende.get_window_extent()
            y_unten = (float(ext.y0) - float(rechts.bbox.y0)) / float(rechts.bbox.height) - 0.015
        gekennzeichnet = int(np.sum(unsicher | ungueltig))
        zeilen = [f"{anzahl} Messpunkte"]
        if gekennzeichnet:
            zeilen.append(f"davon {gekennzeichnet} gekennzeichnet")
        zeichen = max(int((spalte_pt - 4.0) / (0.55 * stil.schrift_pt)), 8)
        punktzahl = rechts.text(
            0.0, y_unten, "\n".join(textwrap.fill(t, zeichen) for t in zeilen),
            transform=rechts.transAxes, ha="left", va="top", fontsize=stil.schrift_pt,
            color=stil.achse,
        )  # fmt: skip
        z.hilfsobjekte["punktzahl"] = punktzahl
        y_unten = (float(punktzahl.get_window_extent().y0) - float(rechts.bbox.y0)) / float(
            rechts.bbox.height
        ) - 0.04

        # --- Farbleiste ---
        hoehe_cb = max(min(y_unten - 0.04, 0.5 if phase_modus else 0.7), 0.15)
        cax = rechts.inset_axes((0.1, 0.04, 0.3, hoehe_cb))
        if phase_modus:
            abbildbar = ScalarMappable(norm=Normalize(-180.0, 180.0), cmap=stil.zyklisch())
            z.hilfsobjekte["farbleiste"] = _farbleiste(
                fig, cax, abbildbar, titel, stil, ticks=[-180, -90, 0, 90, 180]
            )
            assert phase is not None
            z.hilfsobjekte["winkel_grad"] = grad(phase)
        else:
            z.hilfsobjekte["farbleiste"] = _farbleiste(
                fig, cax, punkte, achsentitel(f"Betrag {daten.komponente}", daten.einheit), stil
            )
    return z
