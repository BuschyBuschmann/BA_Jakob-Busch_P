r"""Zeichenfunktion der 3D-Animation der Betriebsschwingform (R-071, FG-04, ADR-029).

``zeichne_animation`` füllt eine übergebene :class:`matplotlib.figure.Figure` mit einer
``Axes3D`` (matplotlib ``mplot3d``, Gleichmaßstab, feste Achsengrenzen), einer Spalte mit den
**Pflichtangaben** (FG-04 3.5: Überhöhung, :math:`D_\mathrm{ref}`, Frequenz und Größe, Winkel
und Phasenbezug), der Zeichenerklärung der gekennzeichneten Punkte und einer Farbleiste mit
Einheit. ``aktualisiere_animation`` setzt danach **nur** die Daten der vorhandenen Artists
(Positionen, Farben, Texte, Blick); es ruft nie ``fig.clear()``.

Ein Bild ist ein reiner Wert der Daten: Positionen kommen aus
:meth:`~ldv_automation.darstellung.animation_daten.AnimationsDaten.positionen` (derselbe Pfad
für das Standbild und für jedes Bild der Bewegung, UI-25). ``aktualisiere`` nach ``zeichne`` mit
anderem Winkel liefert dieselben Positionen, Farben und Texte wie ein frisches ``zeichne``.

Es gibt weder Qt- noch ``pyplot``-Importe (Importtest). Die Zeichenfunktion enthält keinen
Arbeitsstempel (:mod:`.bild`); er kommt nur über ``speichere_arbeitsbild``.

Gekennzeichnete Punkte (FG-04 3.6) bleiben in der **Ruhelage** und tragen dieselben Symbole wie
das Standbild der Ansicht 4: Kreuz = unsicher, hohle Raute = ungültig (M6), hohles Quadrat = kein
Wert. Die Form trägt die Aussage, nicht die Farbe (Graustufendruck).
"""

from __future__ import annotations

import math
import textwrap
from collections.abc import Callable, Iterator, Mapping, Sequence
from contextlib import contextmanager
from dataclasses import dataclass, field, replace
from typing import Any, Literal

import matplotlib
import numpy as np
from matplotlib import rc_context
from matplotlib.colors import Normalize, TwoSlopeNorm
from matplotlib.figure import Figure
from matplotlib.font_manager import FontProperties, findfont
from matplotlib.lines import Line2D
from matplotlib.patheffects import withStroke
from matplotlib.ticker import FuncFormatter, MaxNLocator, NullFormatter
from mpl_toolkits.mplot3d import proj3d

from ldv_automation.auswertung.annahmen import AnnahmeEintrag
from ldv_automation.auswertung.daten import FloatArray

from .achsen import Bereich
from .animation_daten import KEIN_WERT, UNGUELTIG, UNSICHER, AnimationsDaten
from .formate import (
    achsentitel,
    dezimalkomma_formatter,
    frequenz_text,
    tick_text,
    zahl_kurz_text,
    zahl_signifikant_text,
    zahl_text,
)
from .stil import Plotstil
from .zeichnung import Zeichnung, kennzeichen_kopf, layout_rect

__all__ = [
    "BLICK_VORGABEN",
    "MINDESTHOEHE_ANTEIL",
    "AnimationsOptionen",
    "Blick",
    "achsengrenzen_3d",
    "aktualisiere_animation",
    "effektive_ueberhoehung",
    "farb_norm",
    "farbskala",
    "ist_bestaetigt",
    "kennzeichen_texte",
    "nullpunkt_satz",
    "ohne_nachbarabstand",
    "pflichttexte",
    "scatter_positionen",
    "skaliere_einheit",
    "zeichne_animation",
]

MINDESTHOEHE_ANTEIL = 0.15
"""Kleinste Ausdehnung einer Achsenbox als Anteil der größten (E-A5, Plan 3.3).

Eine nahezu ebene Platte bekäme sonst eine entartete Box (Panes flackern, Tiefensortierung
unscharf). Die Grenzen liegen symmetrisch um den Mittelwert der Daten."""

_ELEV_AUFSICHT_GRAD = 89.0  # ab dieser Elevation entfallen die z-Beschriftungen
_RAND = 0.05  # Rand je Seite als Anteil der Spannweite
_MARKER_RAND = 0.02  # zusätzlich, damit Marker am Achsenrand nicht angeschnitten werden
_SPALTE_B_STUFEN = (0.31, 0.35, 0.40, 0.45)
"""Breite der rechten Spalte (Pflichtangaben, Zeichenerklärung) als Anteil der nutzbaren Breite;
bei kleiner Höhe wird die nächstbreitere Stufe gewählt, bis beide Blöcke untereinander passen."""
_SPALTE_RAND = 0.01  # Anteil der nutzbaren Breite am rechten Rand der Spalte
_Z_LUECKE_SCHRIFT = 1.0
"""Lücke zwischen der Beschriftung der 3D-Achse (z-Ticks, z-Titel) und der Spalte, in
Schriftgrößen (UI-A2)."""
_FARBBAND_SCHRIFT = 6.2
"""Höhe von Farbleiste, Ticks und Titel unter der 3D-Achse, in Schriftgrößen (UI-A1)."""
_FARBBALKEN_SCHRIFT = 1.0  # Höhe des Farbbalkens in Schriftgrößen
_FARBBALKEN_UNTEN_SCHRIFT = 4.4  # Platz unter dem Balken für Ticks und Titel in Schriftgrößen
_Z_TICK_ABSTAND_SCHRIFT = 1.7  # kleinster Abstand zweier z-Tick-Beschriftungen in Schriftgrößen
_KOMPAKT_HOEHE_ZOLL = 3.6
"""Kompakte Stufe (Figure niedriger als :data:`_KOMPAKT_HOEHE_ZOLL`, z. B. die Animationsfläche
bei 1100 x 680 px; schmale, aber hohe Figures wie A5 bleiben normal): Schrift höchstens
9 pt, Pflichtangaben ohne Leerzeilen (hängender Einzug), schmale Farbleiste am Fuß der rechten
Spalte (die 3D-Achse behält die volle Höhe); die Spalte reicht neben dem Kopf bis zum oberen
Rand, solange der Kopf nicht in sie ragt."""
_KOMPAKT_SCHRIFT_PT = 9.0
_FARBLEISTE_LUECKE_SCHRIFT = 0.4  # Abstand zwischen Beschriftung der 3D-Achse und Farbleiste
_LABEL_RAND_SCHRIFT = 0.15
"""Rand um jedes Punktlabel bei der Überlappungsprüfung (UI-D2), in Schriftgrößen des Labels."""
_LABEL_JEDE_MAX = 8
"""Größtes n von „nur jedes n-te Label“; wäre mehr nötig, werden alle Labels ausgeblendet."""
_LABEL_MAX = 1500
"""Mehr Labels werden nicht gemessen (die Paarprüfung ist quadratisch), sondern ausgeblendet."""
_ZOOM_GRUND_MAX = 1.5
_ZOOM_GRUND_MIN = 0.5  # passt die Beschriftung auch bei 1 nicht ins Rechteck, wird die Box kleiner
"""Obergrenze der Grundvergrößerung der 3D-Box (``set_box_aspect(..., zoom=)``), die
:func:`_passe_zoom_an` je Blick so wählt, dass die Box die Achse füllt (UI-B1); sie wird mit dem
Zoom des Blicks multipliziert."""
_FARBBALKEN_UNTEN_KOMPAKT_SCHRIFT = 3.9  # Platz für Zahlen und Titel unter dem schmalen Balken
_FARBBALKEN_KOMPAKT_SCHRIFT = 0.55  # Balkenhöhe in Schriftgrößen (kompakt)
_WORST_THETA_GRAD = 359.9  # längster Winkeltext: Grundlage der reservierten Texthöhe
_PRAEFIXE = ((0, ""), (-3, "m"), (-6, "µ"), (-9, "n"), (-12, "p"))
_BUCHSTABEN = ("X", "Y", "Z")
_MAL = "\N{MULTIPLICATION SIGN}"
_QUELLE_TEXT = {"cph": "CPH", "h1": "H1"}
KENNZEICHEN_M8 = "unbestätigt (M8: Polarität der Referenzkanäle offen)"
"""Kennzeichen bei absolutem Phasenbezug (FG-04 Nachtrag 2 5.2, Pflicht)."""
KENNZEICHEN_M12 = "Komponenten im Geometrie-KS unbestätigt (M12)"
"""Kennzeichen im 3D-Modus (FG-04 Nachtrag 2 8 Nr. 2, Pflicht)."""


@dataclass(frozen=True)
class Blick:
    """Blickrichtung und Zoom der 3D-Achse.

    Attributes
    ----------
    azim_grad, elev_grad : float
        Azimut und Elevation in Grad (``Axes3D.view_init``; Elevation -90 bis 90).
    zoom : float
        Zoomfaktor (``set_box_aspect(..., zoom=)``), 1 = Voreinstellung.
    """

    azim_grad: float
    elev_grad: float
    zoom: float = 1.0

    def __post_init__(self) -> None:
        if not (math.isfinite(self.azim_grad) and math.isfinite(self.elev_grad)):
            raise ValueError("azim_grad und elev_grad müssen endlich sein")
        if not (math.isfinite(self.zoom) and self.zoom > 0.0):
            raise ValueError(f"zoom > 0 erwartet: {self.zoom}")


_ISO_ELEV_GRAD = math.degrees(math.atan(1.0 / math.sqrt(2.0)))  # ≈ 35,264°, Isometrie

BLICK_VORGABEN: Mapping[str, Blick] = {
    "xy": Blick(azim_grad=-90.0, elev_grad=90.0),
    "xz": Blick(azim_grad=-90.0, elev_grad=0.0),
    "yz": Blick(azim_grad=0.0, elev_grad=0.0),
    "iso": Blick(azim_grad=-45.0, elev_grad=_ISO_ELEV_GRAD),
}
"""Blickvorgaben je Projektionsebene und Isometrie (UI-23): Aufsicht ``xy``, Seitenansichten
``xz`` und ``yz``, ``iso`` (Elevation ≈ 35,3°, Azimut -45°)."""


@dataclass(frozen=True, kw_only=True)
class AnimationsOptionen:
    r"""Darstellungsoptionen der Animation.

    Attributes
    ----------
    theta_rad : float
        Animationswinkel :math:`\\theta = \\omega t` in rad.
    ueberhoehung : float or None
        **Skalierung**: bei der Auslenkung die Überhöhung :math:`s` (dimensionslos), bei der
        Schnelle die Skalierung :math:`\kappa` in s (FG-04 Nachtrag 2 3.1; Bild = Skalierung ·
        Schnelle); ``None`` = automatisch (:func:`effektive_ueberhoehung`).
    farbe : {"auslenkung", "betrag"}
        Farbe zeigt die vorzeichenbehaftete Auslenkung einer Komponente (Voreinstellung) oder den
        Betrag des momentanen Auslenkungsvektors.
    farb_komponente : {"X", "Y", "Z"} or None
        Komponente der Farbe bei ``"auslenkung"``; ``None`` =
        :meth:`~.animation_daten.AnimationsDaten.farb_komponente_standard`.
    farbbereich : Bereich
        Sichtbarer Farbbereich in der Einheit der animierten Größe (SI: m bzw. m/N bzw. m/s);
        ``None`` je Seite = automatisch (über eine volle Periode).
    blick : Blick
        Blickrichtung und Zoom.
    vereinfacht : bool
        Ohne Achsen, Panes und Ticks (Wiedergabe, Ziehen; Rückfallstufe, Plan 4.3).
    ruhelage : bool
        Hohle graue Punkte an den Ruhelagen (Referenz für Vorzeichen und Richtung).
    punktlabels : bool
        Punktlabels an den Ruhelagen.
    kennzeichen_phase : str or None
        Kennzeichentext „unbestätigt (M8 …)“ (nur bei absolutem Bezug). Fehlt er, setzt
        :func:`kennzeichen_texte` bei absolutem Bezug :data:`KENNZEICHEN_M8` selbst.
    kennzeichen_koordinaten : str or None
        Kennzeichentext „Komponenten im Geometrie-KS unbestätigt (M12)“. Fehlt er, setzt
        :func:`kennzeichen_texte` im 3D-Modus :data:`KENNZEICHEN_M12` selbst.
    """

    theta_rad: float = 0.0
    ueberhoehung: float | None = None
    farbe: Literal["auslenkung", "betrag"] = "auslenkung"
    farb_komponente: str | None = None
    farbbereich: Bereich = field(default_factory=Bereich)
    blick: Blick = field(default_factory=lambda: BLICK_VORGABEN["xy"])
    vereinfacht: bool = False
    ruhelage: bool = True
    punktlabels: bool = False
    kennzeichen_phase: str | None = None
    kennzeichen_koordinaten: str | None = None

    def __post_init__(self) -> None:
        if not math.isfinite(self.theta_rad):
            raise ValueError(f"theta_rad muss endlich sein: {self.theta_rad}")
        if self.farbe not in ("auslenkung", "betrag"):
            raise ValueError(f"unbekannte Farbe {self.farbe!r}")
        if self.farb_komponente is not None and self.farb_komponente not in _BUCHSTABEN:
            raise ValueError(f"farb_komponente X, Y oder Z erwartet: {self.farb_komponente!r}")
        if self.ueberhoehung is not None and not (
            math.isfinite(self.ueberhoehung) and self.ueberhoehung >= 0.0
        ):
            raise ValueError(
                f"ueberhoehung endlich und nicht negativ erwartet: {self.ueberhoehung}"
            )
        von, bis = self.farbbereich.von, self.farbbereich.bis
        if (von is not None and not math.isfinite(von)) or (
            bis is not None and not math.isfinite(bis)
        ):
            raise ValueError("farbbereich muss endliche Grenzen haben")
        if von is not None and bis is not None and not von < bis:
            raise ValueError(f"farbbereich: von < bis erwartet: {von}, {bis}")


# --- Größen ohne Zeichnen ---------------------------------------------------------------------


def effektive_ueberhoehung(daten: AnimationsDaten, opt: AnimationsOptionen) -> float:
    r"""Angezeigte Skalierung: Eingabe, sonst automatisch, sonst reale Auslenkung.

    Auslenkung: Überhöhung :math:`s`; Schnelle: Skalierung :math:`\kappa` in s (Nachtrag 2 3.1).
    Ohne zweiten Punkt gibt es keinen Nachbarabstand und damit keine automatische Skalierung
    (FG-04 6); dann gilt der Maßstab der realen Auslenkung (:math:`s = 1`, bei der Schnelle
    :math:`\kappa = 1/\omega`, also :math:`s_\ddot{a} = 1`), bis der Nutzer einen Wert setzt.
    """
    if opt.ueberhoehung is not None:
        return float(opt.ueberhoehung)
    if daten.s_auto is not None:
        return float(daten.s_auto)
    real = daten.skalierung_aus_ueberhoehung(1.0)
    return real if math.isfinite(real) else 1.0


def ohne_nachbarabstand(daten: AnimationsDaten, ueberhoehung: float | None) -> bool:
    """Prüft, ob die Skalierung der reale Maßstab ohne Nachbarabstand ist (``True``).

    Das gilt ohne Nutzereingabe (``ueberhoehung is None``) und ohne automatische Skalierung
    (:attr:`~.animation_daten.AnimationsDaten.s_auto` ist ``None``: weniger als zwei
    Nicht-Duplikate, FG-04 Nachtrag 3). Das Bild trägt dann einen ausdrücklichen Hinweis.
    """
    return ueberhoehung is None and daten.s_auto is None


def kennzeichen_texte(
    daten: AnimationsDaten, opt: AnimationsOptionen
) -> tuple[str | None, str | None]:
    """Kennzeichen ``(Phase M8, Koordinaten M12)`` des Bildes (FG-04 Nachtrag 2 5.2, 8 Nr. 2).

    Bei absolutem Bezug gilt M8, im 3D-Modus M12; ein Bild ohne diese Kennzeichen entsteht nicht.
    Ein vom Aufrufer gesetzter Text hat Vorrang; ein leerer oder nur aus Leerraum bestehender
    Text gilt als nicht gesetzt und unterdrückt kein Pflichtkennzeichen (FG-04 Nachtrag 2: ein
    Bild ohne diese Kennzeichen entsteht nicht). M8 und M12 entfallen nur, wenn die
    Annahmenliste der Daten sie ausdrücklich als bestätigt führt (Status beginnt mit
    „bestätigt“, :func:`ist_bestaetigt`; die Oberfläche ändert dann nichts, UI-11);
    M12 kommt aus ``AnnahmenStufe2`` (``animation_daten(..., annahmen2=...)``,
    Nutzerentscheidung 2026-11-18); ohne Eintrag oder bei offenem Status gilt M12 im 3D-Modus
    immer.
    """
    phase = opt.kennzeichen_phase
    if phase is not None and not phase.strip():
        phase = None
    if phase is None and daten.bezug_modus == "absolut":
        m8 = [a for a in daten.annahmen if a.nr == "M8"]
        if not m8 or not all(ist_bestaetigt(a) for a in m8):
            phase = KENNZEICHEN_M8
    koordinaten = opt.kennzeichen_koordinaten
    if koordinaten is not None and not koordinaten.strip():
        koordinaten = None
    if koordinaten is None and daten.komponente == "3D":
        m12 = [a for a in daten.annahmen if a.nr == "M12"]
        if not m12 or not all(ist_bestaetigt(a) for a in m12):
            koordinaten = KENNZEICHEN_M12
    return phase, koordinaten


def ist_bestaetigt(eintrag: AnnahmeEintrag) -> bool:
    """Ausdrücklicher Bestätigungsvermerk: Status beginnt mit „bestätigt“ (fail-closed).

    Groß-/Kleinschreibung und führender Leerraum zählen nicht; jeder andere Text („Annahme“,
    „offen“ …) lässt das Kennzeichen stehen. Gilt nur für die Animation.
    """
    return eintrag.status.strip().casefold().startswith("bestätigt")


def skaliere_einheit(wert: float, einheit: str) -> tuple[float, str]:
    """Faktor und Einheit mit SI-Vorsatz, so dass ``wert · faktor`` in ``[1, 1000)`` liegt.

    Der Vorsatz steht vor dem ersten „m“ der Einheit (m → µm, m/N → µm/N, (m/s)/N → (µm/s)/N);
    die Auswahl reicht von m bis pm.

    Parameters
    ----------
    wert : float
        Größenordnung (Betrag); 0, NaN oder Inf ergeben den Faktor 1.
    einheit : str
        Einheit der Größe in SI (enthält „m“).
    """
    stelle = einheit.find("m")
    if stelle < 0:
        raise ValueError(f"Einheit mit Meter erwartet: {einheit!r}")
    if not (math.isfinite(wert) and wert > 0.0):
        return 1.0, einheit
    dekade = 3 * math.floor(math.log10(wert) / 3.0)
    gewaehlt = min(_PRAEFIXE, key=lambda p: abs(p[0] - max(min(dekade, 0), -12)))
    exponent, praefix = gewaehlt
    return 10.0 ** (-exponent), einheit[:stelle] + praefix + einheit[stelle:]


def achsengrenzen_3d(
    daten: AnimationsDaten, ueberhoehung: float
) -> tuple[tuple[float, float], tuple[float, float], tuple[float, float]]:
    r"""Feste Achsengrenzen ``(x, y, z)``, unabhängig vom Winkel :math:`\theta` (Plan 3.3).

    Je Achse die Spanne über die Ruhelage aller Punkte und :math:`X_p \pm s|\hat d_{pc}|` der
    bewegten Punkte (die Bahn eines Punkts überschreitet diese Werte nie), plus 7 % Rand je
    Seite (5 % Rand und 2 % für die Marker am Rand, :data:`_MARKER_RAND`). Jede Achse ist
    mindestens :data:`MINDESTHOEHE_ANTEIL` der größten lang; z liegt
    symmetrisch um die Datenmitte und enthält immer :math:`\pm s D_\mathrm{ref}`.
    """
    if not (math.isfinite(ueberhoehung) and ueberhoehung >= 0.0):
        raise ValueError(f"ueberhoehung endlich und nicht negativ erwartet: {ueberhoehung}")
    x = daten.koordinaten_m
    unten = np.min(x, axis=0)
    oben = np.max(x, axis=0)
    # ``animation_daten`` liefert nie leere ``bewegt``; die Bahn eines Punkts bleibt in X_p ± s|d|
    a = ueberhoehung * np.abs(daten.amplitude_anim[daten.bewegt])
    unten = np.minimum(unten, np.min(x[daten.bewegt] - a, axis=0))
    oben = np.maximum(oben, np.max(x[daten.bewegt] + a, axis=0))
    mitte = 0.5 * (unten + oben)
    spanne = oben - unten
    groesste = float(np.max(spanne))
    if groesste <= 0.0:
        groesste = max(ueberhoehung * daten.d_ref, 1e-12)
    halb = (
        0.5
        * np.maximum(spanne, MINDESTHOEHE_ANTEIL * groesste)
        * (1.0 + 2.0 * (_RAND + _MARKER_RAND))
    )
    halb[2] = max(halb[2], ueberhoehung * daten.d_ref * (1.0 + 2.0 * (_RAND + _MARKER_RAND)))
    grenzen = [(float(m - h), float(m + h)) for m, h in zip(mitte, halb, strict=True)]
    return grenzen[0], grenzen[1], grenzen[2]


def farbskala(daten: AnimationsDaten, opt: AnimationsOptionen) -> tuple[int, float, float]:
    """Farbkomponente und Farbbereich ``(komponente, vmin, vmax)`` in SI-Einheit der Größe.

    Auto: Auslenkung symmetrisch um 0 mit dem Maximum über eine volle Periode, Betrag von 0 bis
    zum Maximum (:meth:`~.animation_daten.AnimationsDaten.farbgrenze`); die Skala pumpt nicht mit
    dem Bild. Eingaben des Nutzers ersetzen je Seite den Autowert.

    Raises
    ------
    ValueError
        Der gemischte Bereich (eine Seite Eingabe, eine Seite Auto) hat ``von >= bis``.
    """
    if daten.komponente != "3D":
        komp = daten.farb_komponente_standard()  # Einzelkomponente: nur die gewählte bewegt sich
    elif opt.farb_komponente is not None:
        komp = _BUCHSTABEN.index(opt.farb_komponente)
    else:
        komp = daten.farb_komponente_standard()
    gr = daten.farbgrenze(opt.farbe, komp)
    auto = (-gr, gr) if opt.farbe == "auslenkung" else (0.0, gr)
    vmin = auto[0] if opt.farbbereich.von is None else float(opt.farbbereich.von)
    vmax = auto[1] if opt.farbbereich.bis is None else float(opt.farbbereich.bis)
    if not vmin < vmax:
        raise ValueError(f"Farbbereich: von < bis erwartet: {vmin}, {vmax}")
    return komp, vmin, vmax


def farb_norm(vmin: float, vmax: float, *, divergierend: bool) -> Normalize:
    """Normierung der Farbe: bei divergierender Skala und ``vmin < 0 < vmax`` Null in der Mitte.

    Ein Nutzerbereich wie ``(-1, 3)`` liefe sonst linear von ``vmin`` bis ``vmax``, und die
    neutrale Mitte der Skala läge nicht bei 0 (Fachabnahme FA-AN3 MINOR-1). Bei symmetrischem
    Bereich (Auto) ist :class:`~matplotlib.colors.TwoSlopeNorm` gleich der linearen Norm.
    """
    if divergierend and vmin < 0.0 < vmax:
        return TwoSlopeNorm(vcenter=0.0, vmin=vmin, vmax=vmax)
    return Normalize(vmin=vmin, vmax=vmax)


def _winkel_text(theta_rad: float, stil: Plotstil) -> str:
    """Winkel in Grad auf [0°, 360°) mit einer Nachkommastelle („θ = 90,0°“)."""
    grad = math.degrees(theta_rad % (2.0 * math.pi))
    grad = round(grad, 1)
    if grad >= 360.0:
        grad = 0.0
    return zahl_text(grad + 0.0, 1, dezimalkomma=stil.dezimalkomma) + "°"


def _bezug_komponente_text(daten: AnimationsDaten) -> str | None:
    """Bezugskomponente (X, Y, Z): bei 3D die Pivot-Komponente, sonst die gewählte."""
    if daten.komponente != "3D":
        return daten.komponente
    if daten.bezug_komponente is None:
        return None
    return _BUCHSTABEN[daten.bezug_komponente]


def _bezug_text(daten: AnimationsDaten) -> str:
    """Zeile „Bezug: …“ der Pflichtangaben (FG-04 3.5 (d), Nachtrag 1).

    Bei relativem Bezug stehen Bezugspunkt, bei 3D die Pivot-Komponente und die **Referenz**
    (FG-04 3.5 (d) „die Referenz und den Phasenbezug“; das Beispiel im Plan P-AUSW3 3.1 ohne
    Referenz weicht davon ab, es gilt die Fachgrundlage).
    """
    referenz = daten.referenz or "Referenz"
    if daten.bezug_modus == "relativ" and daten.bezug_index is not None:
        text = f"Bezug: relativ zu Punkt {int(daten.label[daten.bezug_index])}"
        if daten.komponente == "3D" and daten.bezug_komponente is not None:
            text += f", Komponente {_BUCHSTABEN[daten.bezug_komponente]}"
        return f"{text} (Referenz {referenz})"
    return f"Bezug: absolut zu {referenz}"


def nullpunkt_satz(daten: AnimationsDaten) -> str:
    """Bedeutung von θ = 0 (FG-04 Nachtrag 2 Abschnitt 5.2), immer Teil der Pflichtangabe (d).

    Absolut: Referenz im positiven Maximum (für Auslenkung und Schnelle gleich). Relativ: die
    animierte Größe der Bezugskomponente des Bezugspunkts; bei 3D gilt der Satz nur für diese
    Komponente (Zusatz „andere Komponenten mit festem Phasenversatz“).
    """
    if daten.bezug_modus != "relativ" or daten.bezug_index is None:
        return f"θ = 0°: {daten.referenz or 'Referenz'} im positiven Maximum"
    punkt = int(daten.label[daten.bezug_index])
    komp = _bezug_komponente_text(daten) or "?"
    if daten.groesse == "auslenkung":
        text = (
            f"θ = 0°: Auslenkung von Punkt {punkt}, Komponente {komp} steigt durch null; "
            "positives Maximum bei θ = 90°"
        )
    else:
        text = (
            f"θ = 0°: Schnelle von Punkt {punkt}, Komponente {komp} im positiven Maximum; "
            "Nulldurchgang bei θ = 90°"
        )
    if daten.komponente == "3D":
        text += "; andere Komponenten mit festem Phasenversatz"
    return text


def pflichttexte(
    daten: AnimationsDaten,
    theta_rad: float,
    ueberhoehung: float,
    stil: Plotstil,
    *,
    kein_nachbarabstand: bool = False,
) -> tuple[str, str, str, str]:
    r"""Die vier Pflichtangaben (a) bis (d) nach FG-04 3.5 und Nachtrag 2 (3.3, 5.2).

    ``ueberhoehung`` ist die **Skalierung** (Auslenkung: :math:`s`; Schnelle: :math:`\kappa`
    in s). Zeile (d) besteht aus zwei Zeilen: Winkel und Bezug, dann der Nullpunkt-Satz
    (:func:`nullpunkt_satz`), getrennt durch ``"\n"``. Mit ``kein_nachbarabstand``
    (:func:`ohne_nachbarabstand`) kennzeichnet (a) den realen Maßstab ausdrücklich: „Überhöhung
    (Malzeichen) 1,000 (reale Größe, kein Nachbarabstand)“, bei Schnelle „Skalierung 0,001592 s
    (Bild = Skalierung · Schnelle; κ = 1/ω, kein Nachbarabstand) …“ (eine Klammer, nie zwei
    aneinanderstoßende).

    Returns
    -------
    tuple of str
        (a) Auslenkung: „Überhöhung (Malzeichen) 4555“; Schnelle: „Skalierung 7,250 s (Bild =
        Skalierung · Schnelle) · Amplitude wie Auslenkung mit Überhöhung (Malzeichen) 4555“
        (:math:`s_\ddot{a} = \kappa\omega`; die Überhöhung steht nie mit :math:`\kappa`);
        (b) „größte reale
        Spitzenauslenkung D_ref = 1,59 µm“, bei Schnelle „größte reale Spitzenschnelle D_ref =
        1,00 mm/s (Spitzenauslenkung 1,59 µm)“ (bei H1 mit „/N“); (c) „f = 100,000 Hz ·
        Auslenkung Y (CPH)“ (bei H1 „(H1, je 1 N)“, Komponente X, Y, Z oder 3D); (d) „θ = 90,0° ·
        Bezug: relativ zu Punkt 17 (Referenz Ref1)“ und der Nullpunkt-Satz.
    """
    komma = stil.dezimalkomma
    faktor, einheit = skaliere_einheit(daten.d_ref, daten.einheit_anim)
    d_text = zahl_signifikant_text(daten.d_ref * faktor, 3, dezimalkomma=komma)
    schnelle = daten.groesse == "schnelle"
    if schnelle:
        s_aeq = daten.ueberhoehung_aequivalent(ueberhoehung)
        kappa_text = zahl_kurz_text(ueberhoehung, 4, dezimalkomma=komma)
        aeq_text = zahl_kurz_text(s_aeq, 4, dezimalkomma=komma)
        real = "; κ = 1/ω, kein Nachbarabstand" if kein_nachbarabstand else ""
        text_a = (
            f"Skalierung {kappa_text} s (Bild = Skalierung · Schnelle{real}) · "
            f"Amplitude wie Auslenkung mit Überhöhung {_MAL}{aeq_text}"
        )
        f_a, e_a = skaliere_einheit(daten.d_ref_auslenkung, daten.einheit_auslenkung)
        da_text = zahl_signifikant_text(daten.d_ref_auslenkung * f_a, 3, dezimalkomma=komma)
        text_b = (
            f"größte reale Spitzenschnelle D_ref = {d_text} {einheit} "
            f"(Spitzenauslenkung {da_text} {e_a})"
        )
    else:
        s_text = zahl_kurz_text(ueberhoehung, 4, dezimalkomma=komma)
        real = " (reale Größe, kein Nachbarabstand)" if kein_nachbarabstand else ""
        text_a = f"Überhöhung {_MAL}{s_text}{real}"
        text_b = f"größte reale Spitzenauslenkung D_ref = {d_text} {einheit}"
    groesse = "Schnelle" if schnelle else "Auslenkung"
    f_text = frequenz_text(daten.f_hz, 3, dezimalkomma=komma)
    quelle = _QUELLE_TEXT.get(daten.quelle, daten.quelle)
    if daten.quelle == "h1":
        quelle += ", je 1 N"
    return (
        text_a,
        text_b,
        f"f = {f_text} · {groesse} {daten.komponente} ({quelle})",
        f"θ = {_winkel_text(theta_rad, stil)} · {_bezug_text(daten)}\n{nullpunkt_satz(daten)}",
    )


def scatter_positionen(zeichnung: Zeichnung) -> FloatArray:
    """Positionen ``(n, 3)`` der bewegten Punkte, wie sie in der Figure stehen (Tests, UI-25)."""
    xs, ys, zs = zeichnung.marker["punkte"]._offsets3d
    spalten = [np.asarray(a, dtype=np.float64) for a in (xs, ys, zs)]
    return np.column_stack(spalten)


# --- Zeichnen ---------------------------------------------------------------------------------


def _text_spalte(
    texte: tuple[str, ...], stil: Plotstil, spalte_pt: float, kompakt: bool = False
) -> str:
    """Umbrochener Block der Pflichtangaben.

    Jede Angabe und jede Zeile darin beginnt neu; zwischen den Angaben steht eine Leerzeile
    (klare Trennung, UI-A4).
    """
    zeichen = max(int((spalte_pt - 4.0) / (0.55 * stil.schrift_pt)), 8)
    if kompakt:  # keine Leerzeilen: jede Angabe beginnt linksbündig, Folgezeilen sind eingerückt
        return "\n".join(
            textwrap.fill(zeile, zeichen, subsequent_indent="  ")
            for t in texte
            for zeile in t.split("\n")
        )
    return "\n\n".join(
        "\n".join(textwrap.fill(zeile, zeichen) for zeile in t.split("\n")) for t in texte
    )


def _skala_anpassen(
    z: Zeichnung, daten: AnimationsDaten, opt: AnimationsOptionen, skala: tuple[int, float, float]
) -> None:
    """Farbbereich, Farbleiste (Einheit, Ticks) und Farben des Scatter-Objekts setzen.

    ``skala`` ist das (bereits geprüfte) Ergebnis von :func:`farbskala`.
    """
    stil: Plotstil = z.hilfsobjekte["stil"]
    komp, vmin, vmax = skala
    faktor, einheit = skaliere_einheit(max(abs(vmin), abs(vmax)), daten.einheit_anim)
    punkte = z.marker["punkte"]
    cb = z.hilfsobjekte["farbleiste"]
    punkte.set_norm(farb_norm(vmin, vmax, divergierend=opt.farbe == "auslenkung"))
    cb.update_normal(punkte)
    if opt.farbe == "auslenkung":
        groesse = "Auslenkung" if daten.groesse == "auslenkung" else "Schnelle"
        titel = achsentitel(f"{groesse} {_BUCHSTABEN[komp]}", einheit)
    else:
        if z.hilfsobjekte["kompakt"]:
            lang = "Betrag"
        else:
            lang = (
                "Betrag der Auslenkung" if daten.groesse == "auslenkung" else "Betrag der Schnelle"
            )
        titel = achsentitel(lang, einheit)
    cb.set_label(titel, fontsize=stil.schrift_pt)
    cb.ax.xaxis.set_major_formatter(
        FuncFormatter(lambda w, _p: tick_text(w * faktor, dezimalkomma=stil.dezimalkomma))
    )
    z.hilfsobjekte["farbkomponente"] = komp
    z.hilfsobjekte["farbbereich"] = (vmin, vmax)
    z.hilfsobjekte["farbtitel"] = titel


def _z_laenge_pt(ax: Any) -> float:
    """Kürzeste Bildschirmlänge einer senkrechten Kante der Achsenbox in pt (konservativ)."""
    matrix = ax.get_proj()
    (x0, x1), (y0, y1), (z0, z1) = ax.get_xlim3d(), ax.get_ylim3d(), ax.get_zlim3d()
    k = 72.0 / float(ax.figure.dpi)
    laengen: list[float] = []
    for x_, y_ in ((x0, y0), (x0, y1), (x1, y0), (x1, y1)):
        unten = proj3d.proj_transform(x_, y_, z0, matrix)
        oben = proj3d.proj_transform(x_, y_, z1, matrix)
        p = ax.transData.transform([unten[:2], oben[:2]])
        laengen.append(float(np.hypot(*(p[1] - p[0]))) * k)
    return min(laengen)


def _z_achse(ax: Any, sichtbar: bool, stil: Plotstil) -> None:
    """Beschriftung der z-Achse ein- oder ausblenden und die Tick-Zahl begrenzen.

    In der Aufsicht (Elevation nahe ±90°) fällt die z-Achse in einen Punkt; ihre Ticks lägen
    übereinander und wären unlesbar. Bei einer ebenen Platte ist die z-Achse im Bild kurz: die
    Zahl der Ticks richtet sich nach der Bildschirmlänge der Achse (höchstens ein Tick je
    :data:`_Z_TICK_ABSTAND_SCHRIFT` Schriftgrößen); reicht sie nicht für zwei Ticks, entfallen
    Ticks und Titel (UI-A2).
    """
    ticks = MaxNLocator(nbins=1)
    if sichtbar:
        erlaubt = int(_z_laenge_pt(ax) // (_Z_TICK_ABSTAND_SCHRIFT * stil.schrift_pt)) + 1
        unten, oben = sorted(float(g) for g in ax.get_zlim3d())
        sichtbar = False
        for nbins in range(min(erlaubt - 1, 6), 0, -1):  # möglichst viele Ticks, die passen
            kandidat = MaxNLocator(nbins=nbins)
            werte = np.asarray(kandidat.tick_values(unten, oben), dtype=np.float64)
            if int(np.sum((werte >= unten) & (werte <= oben))) <= erlaubt:
                ticks, sichtbar = kandidat, True
                break
    if sichtbar:
        ax.zaxis.set_major_locator(ticks)
        ax.zaxis.set_major_formatter(dezimalkomma_formatter(dezimalkomma=stil.dezimalkomma))
        ax.set_zlabel(achsentitel("z", "m"), fontsize=stil.schrift_pt)
    else:
        ax.zaxis.set_major_formatter(NullFormatter())
        ax.set_zlabel("")


class LabelMasse:
    """Speicher der Textmaße ``(Breite, Höhe, Abstieg)`` in Pixeln je Label-Text und Schrift.

    Die Maße eines Labels hängen nur von Text, Schrift und den Messbedingungen des Renderers ab,
    nicht vom Blick; die Abfrage beim Renderer ist der Hauptkostenanteil der Label-Dichte (bei
    1500 Punkten etwa 250 ms). Die Messbedingungen (:meth:`_bedingungen`) sind Renderer-Typ, DPI
    und ``rcParams["text.hinting"]``: Agg misst mit dem Hinting-Flag (gemessen: Breite 270,75 statt
    270,28 px je nach Wert), die übrigen Text-``rcParams`` ändern das Maß nicht
    (``text.antialiased`` wirkt nur beim Zeichnen; ``text.hinting_factor`` und
    ``text.kerning_factor`` sind seit Matplotlib 3.11 wirkungslos und veraltet). Der Speicher leert
    sich, wenn sich die Messbedingungen ändern, und behält nach jeder Abfrage nur Einträge, die
    der aktuelle Labelsatz braucht.

    Der Schlüssel ist ein **Abbild** der Schrift (``FontProperties.copy``): ``Text.set_fontsize``
    ändert das Schriftobjekt des Textes an Ort und Stelle, ein Schlüssel auf das Original würde
    sich im Speicher mitändern. Zusätzlich gehört die **aufgelöste Schriftdatei**
    (``font_manager.findfont``) zum Schlüssel: Die Labels tragen die generische Familie
    ``sans-serif``, welche Datei dahinter steht, entscheidet erst ``findfont`` beim Messen aus
    ``rcParams["font.sans-serif"]``/``font.family`` (gemessen: nach ``font.sans-serif =
    ["Caladea"]`` Breite 87 statt 106 px). Je Aufruf wird jede verschiedene Schrift nur einmal
    aufgelöst. Nicht erfasst: Ersatzschriften für Zeichen, die die Hauptschrift nicht enthält.

    Attributes
    ----------
    anzahl_messungen : int
        Wie oft insgesamt beim Renderer gemessen wurde (für Tests und Messungen).
    """

    def __init__(self) -> None:
        self._werte: dict[tuple[str, FontProperties, str], tuple[float, float, float]] = {}
        self._messbedingungen: tuple[type, float, Any] | None = None
        self.anzahl_messungen = 0

    @staticmethod
    def _bedingungen(renderer: Any) -> tuple[type, float, Any]:
        """Alles außer Text und Schrift, wovon das Textmaß abhängt: Typ, DPI, Hinting."""
        return type(renderer), float(renderer.dpi), matplotlib.rcParams["text.hinting"]

    def __len__(self) -> int:
        return len(self._werte)

    def abmessungen(self, renderer: Any, labels: Sequence[Any]) -> list[tuple[float, float, float]]:
        """``(Breite, Höhe, Abstieg)`` in Pixeln je Label; Unbekanntes wird gemessen."""
        bedingungen = self._bedingungen(renderer)
        if bedingungen != self._messbedingungen:
            self._werte.clear()
            self._messbedingungen = bedingungen
        aufgeloest: dict[FontProperties, str] = {}
        schluessel: list[tuple[str, FontProperties, str]] = []
        for t in labels:
            schrift = t.get_fontproperties().copy()
            datei = aufgeloest.get(schrift)
            if datei is None:
                datei = aufgeloest[schrift] = findfont(schrift)
            schluessel.append((t.get_text(), schrift, datei))
        ergebnis: list[tuple[float, float, float]] = []
        for k, t in zip(schluessel, labels, strict=True):
            text = k[0]
            wert = self._werte.get(k)
            if wert is None:
                breite, hoehe, abstieg = renderer.get_text_width_height_descent(
                    text, t.get_fontproperties(), False
                )
                wert = (float(breite), float(hoehe), float(abstieg))
                self._werte[k] = wert
                self.anzahl_messungen += 1
            ergebnis.append(wert)
        gebraucht = set(schluessel)
        for k in [k for k in self._werte if k not in gebraucht]:
            del self._werte[k]
        return ergebnis


def _label_rechtecke_px(
    ax: Any,
    koordinaten_m: Any,
    labels: Sequence[Any],
    renderer: Any,
    masse: LabelMasse | None = None,
) -> Any:
    """Fensterrechtecke ``(n, 4)`` der Labels bei der aktuellen Projektion in Pixeln.

    ``Text3D.get_window_extent`` taugt dafür nicht (die Projektion gilt nur während des Zeichnens),
    deshalb wird der Ankerpunkt hier projiziert und die Textgröße beim Renderer erfragt, mit
    ``masse`` über den Speicher :class:`LabelMasse` (Ergebnis gleich).
    """
    x = np.asarray(koordinaten_m, dtype=np.float64)
    px, py, _pz = proj3d.proj_transform(x[:, 0], x[:, 1], x[:, 2], ax.get_proj())
    anker = ax.transData.transform(np.column_stack([px, py]))
    if masse is None:
        masse_px = [
            renderer.get_text_width_height_descent(t.get_text(), t.get_fontproperties(), False)
            for t in labels
        ]
    else:
        masse_px = masse.abmessungen(renderer, labels)
    boxen = np.empty((len(labels), 4))
    for i, (breite, hoehe, abstieg) in enumerate(masse_px):
        boxen[i] = (
            anker[i, 0],
            anker[i, 1] - abstieg,
            anker[i, 0] + breite,
            anker[i, 1] + hoehe - abstieg,
        )
    return boxen


def label_schritt(
    ax: Any,
    koordinaten_m: Any,
    labels: Sequence[Any],
    renderer: Any,
    masse: LabelMasse | None = None,
) -> int:
    """Wie viele Punktlabels bei der aktuellen Ansicht gezeigt werden (UI-D2).

    Gemessen werden die Fensterrechtecke der Labels (samt Rand :data:`_LABEL_RAND_SCHRIFT`): das
    kleinste ``n`` mit ``2 <= n <= _LABEL_JEDE_MAX``, bei dem die Rechtecke jedes n-ten Labels
    einander nicht überlappen, gilt als Schritt. ``masse`` (optional) speichert die Textmaße
    zwischen; das Ergebnis ändert sich dadurch nicht.

    Returns
    -------
    int
        1 = alle; n = nur jedes n-te; 0 = alle ausgeblendet (auch mehr als :data:`_LABEL_MAX`
        Labels, die Messung wäre zu teuer).
    """
    if len(labels) > _LABEL_MAX:
        return 0
    boxen = _label_rechtecke_px(ax, koordinaten_m, labels, renderer, masse)
    if not np.all(np.isfinite(boxen)):
        return 0
    rand = (
        _LABEL_RAND_SCHRIFT * float(labels[0].get_fontsize()) * float(labels[0].figure.dpi) / 72.0
    )
    boxen = boxen + np.array([-rand, -rand, rand, rand])
    for n in range(1, _LABEL_JEDE_MAX + 1):
        b = boxen[::n]
        ueberlappt = (
            (b[:, None, 0] < b[None, :, 2])
            & (b[None, :, 0] < b[:, None, 2])
            & (b[:, None, 1] < b[None, :, 3])
            & (b[None, :, 1] < b[:, None, 3])
        )
        np.fill_diagonal(ueberlappt, False)
        if not ueberlappt.any():
            return n
    return 0


def label_text(schritt: int) -> str:
    """Hinweistext zur Dichte der Punktlabels (Zeichenerklärung und Meldezeile)."""
    if schritt == 1:
        return "Punktlabels: alle gezeigt"
    if schritt == 0:
        return "Punktlabels wegen Dichte ausgeblendet"
    return f"Punktlabels: nur jedes {schritt}. gezeigt (Dichte)"


class _ZeichenStand:
    """Figure-Größe und DPI, für die die Achsenlage der 3D-Achse zuletzt berechnet wurde.

    Projektion und ``transData`` stimmen nach einem Blick- oder Zoomwechsel ohne Zeichnen; die
    Achsenlage (Box-Seitenverhältnis, ``Axes3D.apply_aspect``) liegt nach einer Größen- oder
    DPI-Änderung aber erst nach dem Zeichnen richtig. Der Stand wird bei **jedem** Zeichnen der
    Figure (``draw_event``, auch ``draw_without_rendering`` anderer) festgehalten, nicht nur bei
    eigenem. Wechselt das Canvas der Figure oder ist nichts bekannt, gilt der Stand als veraltet.
    """

    def __init__(self, figure: Figure) -> None:
        self._figure = figure
        self._canvas: Any = None
        self._stand: tuple[tuple[float, float], float] | None = None

    def _aktuell(self) -> tuple[tuple[float, float], float]:
        breite, hoehe = self._figure.get_size_inches()
        return (float(breite), float(hoehe)), float(self._figure.dpi)

    def _gezeichnet(self, _ereignis: Any) -> None:
        self._stand = self._aktuell()

    def veraltet(self) -> bool:
        """Prüft, ob die Figure vor dem Messen neu gezeichnet werden muss (``True``)."""
        canvas = self._figure.canvas
        if canvas is not self._canvas:  # ein Zeichnen auf dem alten Canvas ist unbekannt
            self._canvas = canvas
            self._stand = None
            canvas.mpl_connect("draw_event", self._gezeichnet)
        return self._stand != self._aktuell()


def _punktlabels_anwenden(z: Zeichnung, daten: AnimationsDaten, stil: Plotstil) -> None:
    """Blendet Punktlabels nach der Dichte aus, meldet es in ``z.hinweise`` und der Legende.

    Gezeichnet wird nur, wenn sich Figure-Größe oder DPI seit dem letzten Zeichnen irgendeiner
    Seite geändert haben (:class:`_ZeichenStand`); die Textmaße liegen in
    ``z.hilfsobjekte["label_masse"]`` (:class:`LabelMasse`).
    """
    labels = z.hilfsobjekte.get("punktlabels")
    if not labels:
        return
    stand: _ZeichenStand = z.hilfsobjekte.setdefault("zeichenstand", _ZeichenStand(z.figure))
    if stand.veraltet():
        z.figure.draw_without_rendering()
    renderer = z.figure._get_renderer()  # type: ignore[attr-defined]
    masse: LabelMasse = z.hilfsobjekte.setdefault("label_masse", LabelMasse())
    schritt = label_schritt(z.achsen[0], daten.koordinaten_m, labels, renderer, masse)
    for i, t in enumerate(labels):
        t.set_visible(schritt != 0 and i % max(schritt, 1) == 0)
    z.hilfsobjekte["punktlabels_schritt"] = schritt
    basis = tuple(h for h in z.hinweise if not h.startswith("Punktlabels"))
    z.hinweise = basis if schritt == 1 else (*basis, label_text(schritt))
    eintrag = z.hilfsobjekte.get("punktlabels_legende")
    if eintrag is not None:
        eintrag.set_text(textwrap.fill(label_text(schritt), z.hilfsobjekte["legende_zeichen"]))


def _dynamisch(
    z: Zeichnung,
    daten: AnimationsDaten,
    opt: AnimationsOptionen,
    vorher: AnimationsOptionen | None,
    *,
    zoom_messen: bool = True,
    zoom_fest: bool = False,
) -> None:
    """Setzt alle vom Winkel, der Skalierung, dem Blick und dem Farbbereich abhängigen Größen.

    Beim ersten Aufruf (``vorher is None``) wird alles gesetzt; danach nur, was sich ändert.
    Gemeinsamer Weg von :func:`zeichne_animation` und :func:`aktualisiere_animation`; das
    garantiert die Gleichheit beider Wege.

    Zuerst werden **alle** Größen berechnet und geprüft (Skalierung, Farbskala, Grenzen,
    Texte), erst danach wird ein Artist verändert. Ein Fehler (z. B. ein Farbbereich mit
    ``von >= bis``) lässt das Bild deshalb unverändert, nie halb aktualisiert.

    ``zoom_messen=False`` überspringt die Zoom-Messung (:func:`_passe_zoom_an`; der Aufrufer misst
    selbst). ``zoom_fest=True`` (Überhöhungsregler wird gezogen) lässt den Grundzoom stehen und
    merkt vor, dass die Messung beim nächsten vollen Aktualisieren nachzuholen ist.
    """
    stil: Plotstil = z.hilfsobjekte["stil"]
    ax: Any = z.achsen[0]
    s = effektive_ueberhoehung(daten, opt)
    skala = farbskala(daten, opt)
    komp = skala[0]
    grenzen = (
        achsengrenzen_3d(daten, s)
        if vorher is None or effektive_ueberhoehung(daten, vorher) != s
        else None
    )
    pos = daten.positionen(opt.theta_rad, s)[daten.bewegt]
    werte = (
        daten.farbwert(opt.theta_rad, komp)
        if opt.farbe == "auslenkung"
        else daten.betrag(opt.theta_rad)
    )[daten.bewegt]
    texte = pflichttexte(
        daten, opt.theta_rad, s, stil,
        kein_nachbarabstand=ohne_nachbarabstand(daten, opt.ueberhoehung),
    )  # fmt: skip
    spalte_pt: float = z.hilfsobjekte["spalte_pt"]
    spaltentext = _text_spalte(texte, stil, spalte_pt, z.hilfsobjekte["kompakt"])
    hinweis = daten.hinweis_ueberhoehung(s)

    punkte = z.marker["punkte"]
    punkte._offsets3d = (pos[:, 0], pos[:, 1], pos[:, 2])
    punkte.set_array(werte)
    if vorher is None or opt.farbbereich != vorher.farbbereich:
        _skala_anpassen(z, daten, opt, skala)
    if grenzen is not None:
        gx, gy, gz = grenzen
        ax.set_xlim3d(*gx)
        ax.set_ylim3d(*gy)
        ax.set_zlim3d(*gz)
        aspekt = (gx[1] - gx[0], gy[1] - gy[0], gz[1] - gz[0])
        z.hilfsobjekte["box_aspekt"] = aspekt
        z.hilfsobjekte["grenzen"] = (gx, gy, gz)
        ax.set_box_aspect(aspekt, zoom=opt.blick.zoom * z.hilfsobjekte["grund_zoom"])
    elif vorher is not None and opt.blick.zoom != vorher.blick.zoom:
        ax.set_box_aspect(
            z.hilfsobjekte["box_aspekt"], zoom=opt.blick.zoom * z.hilfsobjekte["grund_zoom"]
        )
    if vorher is None or opt.blick != vorher.blick:
        ax.view_init(elev=opt.blick.elev_grad, azim=opt.blick.azim_grad)
    # Achsen vor der Messung wieder einschalten: die Messung braucht Ticks und Titel (nach dem
    # Drehen im vereinfachten Modus steht das erste volle Bild an)
    if vorher is None or opt.vereinfacht != vorher.vereinfacht:
        if opt.vereinfacht:
            ax.set_axis_off()
        else:
            ax.set_axis_on()
    # Der Grundzoom gilt für den Blick, bei dem zuletzt gemessen wurde (nicht für den des
    # vorigen Bildes: im vereinfachten Modus ändert sich der Blick ohne Messung, K2-AUSW3-89)
    blick_jetzt = (float(ax.azim), float(ax.elev))
    zoom_noetig = (
        vorher is None
        or blick_jetzt != z.hilfsobjekte.get("gemessen_blick")
        or grenzen is not None
        or bool(z.hilfsobjekte.get("zoom_veraltet", False))
    )
    if zoom_noetig and zoom_fest and zoom_messen:
        z.hilfsobjekte["zoom_veraltet"] = True  # beim Loslassen messen
    elif zoom_noetig and zoom_messen and not opt.vereinfacht and "zoom_grenzen" in z.hilfsobjekte:
        z.hilfsobjekte["zoom_veraltet"] = False
        _passe_zoom_an(z.figure, ax, z, stil, z.hilfsobjekte["zoom_grenzen"])
        z.hilfsobjekte["gemessen_blick"] = blick_jetzt
        ax.set_box_aspect(
            z.hilfsobjekte["box_aspekt"], zoom=opt.blick.zoom * z.hilfsobjekte["grund_zoom"]
        )
    else:
        zoom_noetig = False  # nichts gemessen: die Label-Dichte bleibt, bis gemessen wird
    if vorher is None or opt.blick != vorher.blick or grenzen is not None:
        _z_achse(ax, abs(opt.blick.elev_grad) < _ELEV_AUFSICHT_GRAD, stil)
    z.hilfsobjekte["pflichttext"].set_text(spaltentext)
    z.hilfsobjekte["pflichtangaben"] = texte
    z.hinweise = (hinweis,) if hinweis else ()
    z.hilfsobjekte["optionen"] = opt
    z.hilfsobjekte["skalierung"] = s
    z.hilfsobjekte["ueberhoehung"] = daten.ueberhoehung_aequivalent(s)
    label_schluessel = (*blick_jetzt, float(opt.blick.zoom))
    if (
        "punktlabels" in z.hilfsobjekte
        and not opt.vereinfacht
        and not zoom_fest
        and zoom_messen
        and (zoom_noetig or label_schluessel != z.hilfsobjekte.get("label_schluessel"))
    ):
        _punktlabels_anwenden(z, daten, stil)  # Dichte hängt von Blick und Zoom ab
        z.hilfsobjekte["label_schluessel"] = label_schluessel
    elif "punktlabels_schritt" in z.hilfsobjekte and z.hilfsobjekte["punktlabels_schritt"] != 1:
        schritt = z.hilfsobjekte["punktlabels_schritt"]
        z.hinweise = (*z.hinweise, label_text(schritt))  # unverändert gültiger Stand


def _g2_text(wert: float | None, stil: Plotstil) -> str:
    return zahl_text(float(wert or 0.0), None, dezimalkomma=stil.dezimalkomma)


def _zeichenerklaerung(
    daten: AnimationsDaten, opt: AnimationsOptionen, stil: Plotstil
) -> tuple[list[tuple[Line2D, str]], dict[str, int]]:
    """Einträge der Zeichenerklärung (Symbol, Wort, Anzahl) und die Anzahlen je Status."""
    anzahl = {
        "unsicher": int(np.sum(daten.status == UNSICHER)),
        "ungueltig": int(np.sum(daten.status == UNGUELTIG)),
        "kein_wert": int(np.sum(daten.status == KEIN_WERT)),
    }
    eintraege: list[tuple[Line2D, str]] = []
    if opt.ruhelage:
        eintraege.append(
            (
                Line2D(
                    [], [], linestyle="none", marker="o", markersize=5, markerfacecolor="none",
                    markeredgecolor=stil.text_gedaempft,
                ),
                "Ruhelage",
            )
        )  # fmt: skip
    if anzahl["unsicher"]:
        if bool(np.any(daten.grund_3d_unvollstaendig)):
            text = (
                f"3D unvollständig (mindestens eine Komponente unter γ²_min = "
                f"{_g2_text(daten.kohaerenz_min, stil)}) ({anzahl['unsicher']})"
            )
        else:
            text = f"γ² < {_g2_text(daten.kohaerenz_min, stil)}: unsicher ({anzahl['unsicher']})"
        eintraege.append(
            (Line2D([], [], linestyle="none", marker="x", color=stil.achse, markersize=6), text)
        )
    if anzahl["ungueltig"]:
        eintraege.append(
            (
                Line2D(
                    [], [], linestyle="none", marker="D", markersize=6,
                    markerfacecolor=stil.flaeche, markeredgecolor=stil.text_gedaempft,
                ),
                f"ungültig (M6) ({anzahl['ungueltig']})",
            )
        )  # fmt: skip
    if anzahl["kein_wert"]:
        eintraege.append(
            (
                Line2D(
                    [], [], linestyle="none", marker="s", markersize=6,
                    markerfacecolor=stil.flaeche, markeredgecolor=stil.text_gedaempft,
                ),
                f"kein Messwert ({anzahl['kein_wert']})",
            )
        )  # fmt: skip
    return eintraege, anzahl


_SPALTE_LUECKE_SCHRIFT = 1.0  # Abstand zwischen Pflichtangaben und Zeichenerklärung (Schriftgrößen)
_LEGENDE_ARGUMENTE: dict[str, Any] = {
    "borderaxespad": 0.0,
    "frameon": False,
    "handlelength": 1.2,
    "handletextpad": 0.5,
    "labelspacing": 0.6,
    "numpoints": 1,
}


def _legende_zeichen(spalte_pt: float, stil: Plotstil) -> int:
    """Zeichen je Zeile der Zeichenerklärung (Umbruch)."""
    return max(int((spalte_pt - 26.0) / (0.55 * stil.schrift_pt)), 8)


def _spaltenhoehe_pt(
    fig: Figure,
    daten: AnimationsDaten,
    opt: AnimationsOptionen,
    stil: Plotstil,
    spalte_pt: float,
    kompakt: bool = False,
) -> tuple[float, float]:
    """Gemessene Höhen ``(Pflichtangaben, Zeichenerklärung)`` in pt bei Spaltenbreite ``spalte_pt``.

    Der Winkeltext ist der längste (θ = 359,9°), damit der Platz für jeden Winkel reicht. Die
    Messung nutzt vorübergehende Artists der Figure; sie werden wieder entfernt.
    """
    k = 72.0 / float(fig.dpi)
    s = effektive_ueberhoehung(daten, opt)
    texte = pflichttexte(
        daten, math.radians(_WORST_THETA_GRAD), s, stil,
        kein_nachbarabstand=ohne_nachbarabstand(daten, opt.ueberhoehung),
    )  # fmt: skip
    probe = fig.text(
        0.0, 1.0, _text_spalte(texte, stil, spalte_pt, kompakt), fontsize=stil.schrift_pt, va="top"
    )
    eintraege, _anzahl = _zeichenerklaerung(daten, opt, stil)
    legende = None
    if eintraege:
        legende = fig.legend(
            handles=[h for h, _ in eintraege],
            labels=[textwrap.fill(t, _legende_zeichen(spalte_pt, stil)) for _, t in eintraege],
            loc="upper left",
            **_LEGENDE_ARGUMENTE,
            fontsize=stil.schrift_pt,
        )
    fig.draw_without_rendering()
    h_text = float(probe.get_window_extent().height) * k
    h_legende = float(legende.get_window_extent().height) * k if legende is not None else 0.0
    probe.remove()
    if legende is not None:
        legende.remove()
    return h_text, h_legende


def _zoom_grenzen_px(
    fig: Figure, ax: Any, rechts: Any, y0: float, stil: Plotstil, kaesten: Sequence[Any]
) -> tuple[float, float, float, float]:
    """Erlaubtes Rechteck ``(links, unten, rechts, oben)`` der Box samt Beschriftung in Pixeln.

    Links der Figurrand, unten der Rand des nutzbaren Rechtecks, oben die Achsenoberkante und
    rechts die Spalte (abzüglich der Lücke).
    """
    fig.draw_without_rendering()
    feld = ax.get_window_extent()
    luecke = _Z_LUECKE_SCHRIFT * stil.schrift_pt * float(fig.dpi) / 72.0
    spalte_links = float(rechts.get_window_extent().x0)
    return (
        2.0,
        y0 * float(fig.bbox.height),
        spalte_links - luecke,
        float(feld.y1),
    )


@contextmanager
def _ohne_punkte(z: Zeichnung) -> Iterator[None]:
    """Nimmt alle Marker und Punktlabels während der Messung aus ``ax._children``.

    ``set_visible(False)`` reicht nicht: ``Text3D.draw`` projiziert auch unsichtbare Texte. Die
    Grenze der Box samt Beschriftung (``get_tightbbox``) hängt nicht von Punkten und Labels ab
    (``Text3D.get_tightbbox`` ist ``None``, Scatter ist auf ``ax.patch`` geclippt). Im ``finally``
    wird **dasselbe Listenobjekt** mit allen Artists in Ausgangsreihenfolge wiederhergestellt
    (private Matplotlib-API; mpl 3.11.2, gepinnt in ``uv.lock``).

    Im Kontext dürfen keine Artists angelegt oder entfernt werden: ein dort angelegter Artist ginge
    nach dem ``finally`` verloren.
    """
    ax: Any = z.achsen[0]
    kinder: list[Any] = ax._children
    original = list(kinder)
    weg = {id(a) for a in (*z.marker.values(), *z.hilfsobjekte.get("punktlabels", ()))}
    kinder[:] = [a for a in original if id(a) not in weg]
    try:
        yield
    finally:
        kinder[:] = original


def _zeichne_ohne_punkte(z: Zeichnung) -> None:
    """Zeichnet die Figure ohne Marker und Punktlabels (nur für die Zoom-Messung)."""
    with _ohne_punkte(z):
        z.figure.draw_without_rendering()


def _passe_zoom_an(
    fig: Figure,
    ax: Any,
    z: Zeichnung,
    stil: Plotstil,
    grenzen_px: tuple[float, float, float, float],
) -> None:
    """Wählt die Grundvergrößerung der Box so groß, dass Box und Beschriftung im Rechteck bleiben.

    ``grenzen_px = (links, unten, rechts, oben)`` ist das erlaubte Rechteck in Pixeln. Beim
    aktuellen Blick wird die Vergrößerung zwischen :data:`_ZOOM_GRUND_MIN` und
    :data:`_ZOOM_GRUND_MAX` durch Intervallhalbierung (fünf Messungen) bestimmt: die größte,
    bei der die Achse samt Tick- und Achsentiteln (``get_tightbbox``) das Rechteck nicht
    verlässt. Das Ergebnis steht in
    ``z.hilfsobjekte["grund_zoom"]``. Gemessen wird ohne Marker und Punktlabels
    (:func:`_zeichne_ohne_punkte`); sie ändern die Grenze nicht.
    """
    renderer = fig._get_renderer()  # type: ignore[attr-defined]
    aspekt = z.hilfsobjekte["box_aspekt"]
    links, unten, rechts, oben = grenzen_px

    def passt(zoom: float) -> bool:
        ax.set_box_aspect(aspekt, zoom=zoom)
        _z_achse(ax, abs(ax.elev) < _ELEV_AUFSICHT_GRAD, stil)
        _zeichne_ohne_punkte(z)
        box = ax.get_tightbbox(renderer)
        return bool(
            box.x0 >= links - 0.5
            and box.y0 >= unten - 0.5
            and box.x1 <= rechts + 0.5
            and box.y1 <= oben + 0.5
        )

    if passt(_ZOOM_GRUND_MAX):
        z.hilfsobjekte["grund_zoom"] = _ZOOM_GRUND_MAX
        return
    klein, gross = _ZOOM_GRUND_MIN, _ZOOM_GRUND_MAX
    for _ in range(4):
        mitte = 0.5 * (klein + gross)
        if passt(mitte):
            klein = mitte
        else:
            gross = mitte
    z.hilfsobjekte["grund_zoom"] = klein


def _waehle_spalte(
    fig: Figure,
    daten: AnimationsDaten,
    opt: AnimationsOptionen,
    stil: Plotstil,
    breite_pt: float,
    hoehe_pt: Callable[[float], float],
    kompakt: bool = False,
) -> tuple[float, float]:
    """Schmalste Spaltenbreite aus :data:`_SPALTE_B_STUFEN`, in der die Blöcke untereinander passen.

    ``hoehe_pt(anteil)`` ist die für Pflichtangaben und Zeichenerklärung verfügbare Höhe in pt
    bei der Spaltenbreite ``anteil``. Passt keine Stufe, gilt die breiteste.

    Returns
    -------
    tuple of float
        Spaltenanteil und gemessene Höhe der Pflichtangaben in pt.
    """
    for i, anteil in enumerate(_SPALTE_B_STUFEN):
        h_text, h_legende = _spaltenhoehe_pt(fig, daten, opt, stil, anteil * breite_pt, kompakt)
        luecke = _SPALTE_LUECKE_SCHRIFT * stil.schrift_pt if h_legende else 0.0
        if h_text + luecke + h_legende <= hoehe_pt(anteil) or i == len(_SPALTE_B_STUFEN) - 1:
            return anteil, h_text
    raise AssertionError("unerreichbar")  # pragma: no cover  # Stufen sind nicht leer


def zeichne_animation(
    fig: Figure, daten: AnimationsDaten, opt: AnimationsOptionen, stil: Plotstil
) -> Zeichnung:
    r"""Zeichnet die Schwingform als 3D-Bild bei :math:`\theta` = ``opt.theta_rad`` in ``fig``.

    Das Standbild (Speichern, Thesis) und jedes Bild der Bewegung sind dasselbe Bild; die Bewegung
    ruft danach :func:`aktualisiere_animation`. Die Figure wird geleert; ihr Layout-Engine wird
    abgeschaltet, die Achsen stehen in festen Figure-Anteilen im nutzbaren Rechteck
    (:func:`~.zeichnung.layout_rect`, damit der Stempel von ``speichere_arbeitsbild`` Platz hat).
    ``Axes3D.disable_mouse_rotation`` ist gesetzt: Drehen und Zoom steuert die Oberfläche selbst.

    Parameters
    ----------
    fig : Figure
        Wird geleert und neu gefüllt; sie muss ihre endgültige Größe haben (Umbruch der Texte).
    daten : AnimationsDaten
        Aus :func:`~.animation_daten.animation_daten`.
    opt : AnimationsOptionen
        Winkel, Überhöhung, Farbe, Blick und Kennzeichen.
    stil : Plotstil
        Farben, Divergierend-Skala, Verlauf, Schrift.

    Returns
    -------
    Zeichnung
        ``achsen = (Axes3D,)``; ``marker`` mit ``"punkte"`` (bewegte Punkte), ``"ruhelage"``
        (falls gezeigt) sowie ``"unsicher"``, ``"ungueltig"``, ``"kein_wert"`` (falls
        vorhanden); ``hilfsobjekte`` mit ``"pflichttext"``, ``"pflichtangaben"``,
        ``"farbleiste"``, ``"zeichenerklaerung"``, ``"anzahl"``, ``"grenzen"``,
        ``"skalierung"`` (Auslenkung: :math:`s`, Schnelle: :math:`\kappa` in s),
        ``"ueberhoehung"`` (dimensionslos: bei Schnelle die äquivalente Überhöhung
        :math:`\kappa\omega`, NaN bei :math:`\omega \le 0`), ``"farbbereich"`` und
        ``"punktlabels"``; ``texte`` mit dem Pflichttext
        und den Kennzeichen; ``hinweise`` mit dem Überlagerungshinweis.
    """
    with rc_context(stil.schrift_rc()):
        return _zeichne_animation(fig, daten, opt, stil)


def _zeichne_animation(
    fig: Figure, daten: AnimationsDaten, opt: AnimationsOptionen, stil: Plotstil
) -> Zeichnung:
    """Rumpf von :func:`zeichne_animation` (im Stil-Kontext)."""
    _komp, vmin, vmax = farbskala(
        daten, opt
    )  # prüft den Farbbereich, bevor die Figure geleert wird
    rect = layout_rect(fig)  # vor dem Abschalten der Engine: der Stempel braucht seinen Rand
    fig.clear()
    fig.set_layout_engine("none")
    stil_eingabe = stil
    kompakt = float(fig.get_figheight()) < _KOMPAKT_HOEHE_ZOLL
    if kompakt and stil.schrift_pt > _KOMPAKT_SCHRIFT_PT:
        stil = replace(stil, schrift_pt=_KOMPAKT_SCHRIFT_PT)
    fig.set_facecolor(stil.flaeche)
    kennzeichen = [t for t in kennzeichen_texte(daten, opt) if t]
    kaesten, (x0, y0, breite, hoehe) = kennzeichen_kopf(
        fig, stil, kennzeichen, rect, gemeinsamer_rahmen=True
    )
    breite_pt = float(fig.get_figwidth()) * 72.0
    hoehe_pt = float(fig.get_figheight()) * 72.0
    voll_hoehe = rect[3]
    kopf_rechts = 0.0  # rechter Rand des Kopfes in Figure-Anteilen
    if kaesten:
        fig.draw_without_rendering()
        kopf_rechts = max(float(k.get_window_extent().x1) for k in kaesten) / float(fig.bbox.width)
        kopf_rechts += 0.02
    block_pt = (  # Farbleiste samt Zahlen und Titel am Fuß der Spalte (kompakt)
        (_FARBBALKEN_UNTEN_KOMPAKT_SCHRIFT + _FARBBALKEN_KOMPAKT_SCHRIFT + _SPALTE_LUECKE_SCHRIFT)
        * stil.schrift_pt
        if kompakt
        else 0.0
    )

    def spalte_hoehe(anteil: float) -> float:
        """Höhe der Spalte in Figure-Anteilen: neben dem Kopf bis oben, wenn er nicht hineinragt."""
        links = x0 + (1.0 - anteil - _SPALTE_RAND) * breite
        return voll_hoehe if kompakt and kopf_rechts <= links else hoehe

    spalte_b, text_hoehe_pt = _waehle_spalte(
        fig,
        daten,
        opt,
        stil,
        breite * breite_pt,
        lambda anteil: spalte_hoehe(anteil) * hoehe_pt - block_pt,
        kompakt,
    )
    spalte_h = spalte_hoehe(spalte_b)
    spalte_x = 1.0 - spalte_b - _SPALTE_RAND
    breite_3d = spalte_x - 0.03
    band = 0.0 if kompakt else _FARBBAND_SCHRIFT * stil.schrift_pt / hoehe_pt  # Farbleiste unten

    ax: Any = fig.add_axes(
        (x0, y0 + band, breite_3d * breite, max(hoehe - band, 0.05)),
        projection="3d",
        computed_zorder=False,
    )
    ax.disable_mouse_rotation()
    ax.set_facecolor(stil.flaeche)
    for achse in (ax.xaxis, ax.yaxis, ax.zaxis):
        achse.set_major_formatter(dezimalkomma_formatter(dezimalkomma=stil.dezimalkomma))
        achse.label.set_color(stil.achse)
    ax.set_xlabel(achsentitel("x", "m"), fontsize=stil.schrift_pt)
    ax.set_ylabel(achsentitel("y", "m"), fontsize=stil.schrift_pt)
    ax.set_zlabel(achsentitel("z", "m"), fontsize=stil.schrift_pt)
    ax.tick_params(colors=stil.achse, labelsize=stil.schrift_pt)

    z = Zeichnung(figure=fig, achsen=(ax,))
    z.hilfsobjekte["stil"] = stil
    z.hilfsobjekte["stil_eingabe"] = stil_eingabe
    z.hilfsobjekte["kompakt"] = kompakt
    z.hilfsobjekte["grund_zoom"] = 1.0
    z.hilfsobjekte["daten"] = daten
    z.texte.extend(kaesten)

    x = daten.koordinaten_m
    if opt.ruhelage:
        z.marker["ruhelage"] = ax.scatter(
            x[:, 0], x[:, 1], x[:, 2], s=22, marker="o", facecolors="none",
            edgecolors=stil.text_gedaempft, linewidths=0.8, depthshade=False, zorder=1,
        )  # fmt: skip
    for schluessel, status, marker in (
        ("unsicher", UNSICHER, "x"),
        ("ungueltig", UNGUELTIG, "D"),
        ("kein_wert", KEIN_WERT, "s"),
    ):
        maske = daten.status == status
        if not np.any(maske):
            continue
        if marker == "x":
            z.marker[schluessel] = ax.scatter(
                x[maske, 0], x[maske, 1], x[maske, 2], s=40, marker="x", c=stil.achse,
                linewidths=1.3, depthshade=False, zorder=2,
            )  # fmt: skip
        else:
            z.marker[schluessel] = ax.scatter(
                x[maske, 0], x[maske, 1], x[maske, 2], s=34, marker=marker,
                facecolors=stil.flaeche, edgecolors=stil.text_gedaempft, linewidths=1.0,
                depthshade=False, zorder=2,
            )  # fmt: skip
    if opt.punktlabels:
        z.hilfsobjekte["punktlabels"] = [
            ax.text(
                x[i, 0],
                x[i, 1],
                x[i, 2],
                f" {int(daten.label[i])}",
                fontsize=0.8 * stil.schrift_pt,
                color=stil.text_gedaempft,
                zorder=2,
                path_effects=[withStroke(linewidth=2.0, foreground=stil.flaeche)],  # Halo
            )
            for i in range(daten.anzahl_punkte)
        ]

    cmap = stil.divergierend() if opt.farbe == "auslenkung" else stil.verlauf()
    norm = farb_norm(vmin, vmax, divergierend=opt.farbe == "auslenkung")
    ersterwert = np.zeros(int(np.sum(daten.bewegt)))
    z.marker["punkte"] = ax.scatter(
        x[daten.bewegt, 0], x[daten.bewegt, 1], x[daten.bewegt, 2], c=ersterwert, cmap=cmap,
        norm=norm, s=46, marker="o", edgecolors=stil.achse, linewidths=0.5,
        depthshade=False, zorder=3,
    )  # fmt: skip

    # --- rechte Spalte: Pflichtangaben, Zeichenerklärung; Farbleiste unter der 3D-Achse ------
    rechts: Any = fig.add_axes((x0 + spalte_x * breite, y0, spalte_b * breite, spalte_h))
    rechts.set_axis_off()
    z.hilfsobjekte["rechts"] = rechts
    spalte_pt = spalte_b * breite * breite_pt
    z.hilfsobjekte["spalte_pt"] = spalte_pt
    z.hilfsobjekte["spalte_anteil"] = spalte_b
    z.hilfsobjekte["pflichttext"] = rechts.text(
        0.0, 1.0, "", transform=rechts.transAxes, ha="left", va="top",
        fontsize=stil.schrift_pt, color=stil.achse,
    )  # fmt: skip
    z.texte.append(z.hilfsobjekte["pflichttext"])
    if kompakt:  # schmaler Balken am Fuß der Spalte, Zahlen und Titel darunter
        balken_unten = _FARBBALKEN_UNTEN_KOMPAKT_SCHRIFT * stil.schrift_pt / hoehe_pt
        balken_hoehe = _FARBBALKEN_KOMPAKT_SCHRIFT * stil.schrift_pt / hoehe_pt
        balken_x, balken_b = x0 + (spalte_x + 0.1 * spalte_b) * breite, 0.8 * spalte_b * breite
    else:
        balken_unten = _FARBBALKEN_UNTEN_SCHRIFT * stil.schrift_pt / hoehe_pt
        balken_hoehe = _FARBBALKEN_SCHRIFT * stil.schrift_pt / hoehe_pt
        balken_x, balken_b = x0 + 0.2 * breite_3d * breite, 0.6 * breite_3d * breite
    cax = fig.add_axes((balken_x, y0 + balken_unten, balken_b, balken_hoehe))
    z.hilfsobjekte["farbleiste"] = fig.colorbar(
        z.marker["punkte"], cax=cax, orientation="horizontal"
    )
    cb = z.hilfsobjekte["farbleiste"]
    cb.ax.tick_params(labelsize=stil.schrift_pt, colors=stil.achse)
    cb.outline.set_edgecolor(stil.achse)
    _dynamisch(z, daten, opt, None, zoom_messen=False)  # gemessen wird unten, einmal

    # Unterkante der Box samt Beschriftung: bei der Farbleiste unter der Achse deren Oberkante
    # (UI-D1: die Zahlen und der Titel der x-Achse dürfen die Leiste nicht überdecken), sonst
    # der Rand des nutzbaren Rechtecks
    unten_zoom = y0
    if not kompakt:
        unten_zoom += (
            balken_unten + balken_hoehe + _FARBLEISTE_LUECKE_SCHRIFT * stil.schrift_pt / hoehe_pt
        )
    z.hilfsobjekte["zoom_grenzen"] = _zoom_grenzen_px(fig, ax, rechts, unten_zoom, stil, kaesten)
    ax.set_axis_on()  # gemessen wird mit Beschriftung; die Achse hat ihre Endgröße
    _passe_zoom_an(fig, ax, z, stil, z.hilfsobjekte["zoom_grenzen"])
    z.hilfsobjekte["gemessen_blick"] = (float(ax.azim), float(ax.elev))
    if opt.vereinfacht:
        ax.set_axis_off()
    ax.set_box_aspect(
        z.hilfsobjekte["box_aspekt"], zoom=opt.blick.zoom * z.hilfsobjekte["grund_zoom"]
    )
    _z_achse(ax, abs(opt.blick.elev_grad) < _ELEV_AUFSICHT_GRAD, stil)
    z.hilfsobjekte["legende_zeichen"] = _legende_zeichen(spalte_pt, stil)
    _punktlabels_anwenden(z, daten, stil)
    z.hilfsobjekte["label_schluessel"] = (
        float(ax.azim), float(ax.elev), float(opt.blick.zoom)
    )  # fmt: skip
    eintraege, anzahl = _zeichenerklaerung(daten, opt, stil)
    z.hilfsobjekte["anzahl"] = anzahl
    if opt.punktlabels:
        eintraege.append(
            (
                Line2D([], [], linestyle="none", marker=""),
                label_text(z.hilfsobjekte["punktlabels_schritt"]),
            )
        )
    if eintraege:
        # Die Zeichenerklärung steht unter der für den längsten Winkeltext reservierten Texthöhe
        y_oben = 1.0 - (text_hoehe_pt + _SPALTE_LUECKE_SCHRIFT * stil.schrift_pt) / (
            spalte_h * hoehe_pt
        )
        legende = rechts.legend(
            handles=[h for h, _ in eintraege],
            labels=[textwrap.fill(t, _legende_zeichen(spalte_pt, stil)) for _, t in eintraege],
            loc="upper left",
            bbox_to_anchor=(0.0, y_oben),
            **_LEGENDE_ARGUMENTE,
            fontsize=stil.schrift_pt,
        )
        z.hilfsobjekte["zeichenerklaerung"] = legende
        if opt.punktlabels:
            z.hilfsobjekte["punktlabels_legende"] = legende.get_texts()[-1]
    return z


def aktualisiere_animation(
    zeichnung: Zeichnung,
    daten: AnimationsDaten,
    opt: AnimationsOptionen,
    stil: Plotstil,
    *,
    zoom_fest: bool = False,
) -> None:
    """Teilaktualisierung: setzt nur Artist-Daten, ruft nie ``fig.clear()`` und kein Layout.

    Geändert werden dürfen Winkel, Überhöhung, Blick (auch Zoom), ``vereinfacht`` und
    Farbbereich. Das Ergebnis ist gleich dem eines frischen :func:`zeichne_animation` mit
    denselben Optionen (Positionen, Farben, Pflichttexte, Grenzen). Mit ``zoom_fest=True``
    (Überhöhungsregler wird gezogen) bleibt der Grundzoom der Box stehen; die Messung holt das
    nächste Aktualisieren ohne ``zoom_fest`` nach.

    Raises
    ------
    ValueError
        ``daten`` oder ``stil`` sind nicht die der Zeichnung, oder eine Option, die den Aufbau
        des Bildes betrifft (``farbe``, ``farb_komponente``, ``ruhelage``, ``punktlabels``,
        Kennzeichen), unterscheidet sich: dann ist neu zu zeichnen.
    """
    with rc_context(stil.schrift_rc()):
        _aktualisiere_animation(zeichnung, daten, opt, stil, zoom_fest=zoom_fest)


def _aktualisiere_animation(
    zeichnung: Zeichnung,
    daten: AnimationsDaten,
    opt: AnimationsOptionen,
    stil: Plotstil,
    *,
    zoom_fest: bool = False,
) -> None:
    """Rumpf von :func:`aktualisiere_animation` (im Stil-Kontext)."""
    vorher: AnimationsOptionen | None = zeichnung.hilfsobjekte.get("optionen")
    if vorher is None:
        raise ValueError("Zeichnung stammt nicht von zeichne_animation")
    if (
        zeichnung.hilfsobjekte["daten"] is not daten
        or zeichnung.hilfsobjekte["stil_eingabe"] != stil
    ):
        raise ValueError("andere Daten oder anderer Stil: neu zeichnen")
    feste = ("farbe", "farb_komponente", "ruhelage", "punktlabels", "kennzeichen_phase")
    if any(getattr(opt, n) != getattr(vorher, n) for n in feste) or (
        opt.kennzeichen_koordinaten != vorher.kennzeichen_koordinaten
    ):
        raise ValueError("Aufbau des Bildes geändert (Farbe, Ruhelage, Kennzeichen): neu zeichnen")
    _dynamisch(zeichnung, daten, opt, vorher, zoom_fest=zoom_fest)
