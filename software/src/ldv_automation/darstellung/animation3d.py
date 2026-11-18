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
from collections.abc import Mapping
from dataclasses import dataclass, field
from typing import Any, Literal

import numpy as np
from matplotlib.colors import Normalize, TwoSlopeNorm
from matplotlib.figure import Figure
from matplotlib.lines import Line2D
from matplotlib.ticker import FuncFormatter, NullFormatter

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
_BREITE_3D = 0.70  # Anteil der 3D-Achse an der nutzbaren Breite
_SPALTE_X = 0.72
_SPALTE_B = 0.27
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
    Bild ohne diese Kennzeichen entsteht nicht). M8 entfällt nur, wenn die Annahmenliste der
    Daten M8 als bestätigt führt (die Oberfläche ändert dann nichts, UI-11); M12 steht nicht in
    dieser Liste (nur in ``AnnahmenStufe2``, die die Daten nicht tragen) und gilt im 3D-Modus
    immer.
    """
    phase = opt.kennzeichen_phase
    if phase is not None and not phase.strip():
        phase = None
    if phase is None and daten.bezug_modus == "absolut":
        m8 = [a for a in daten.annahmen if a.nr == "M8"]
        if not m8 or any(a.ist_annahme for a in m8):
            phase = KENNZEICHEN_M8
    koordinaten = opt.kennzeichen_koordinaten
    if koordinaten is not None and not koordinaten.strip():
        koordinaten = None
    if koordinaten is None and daten.komponente == "3D":
        koordinaten = KENNZEICHEN_M12
    return phase, koordinaten


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
    bewegten Punkte (die Bahn eines Punkts überschreitet diese Werte nie), plus 5 % Rand je
    Seite. Jede Achse ist mindestens :data:`MINDESTHOEHE_ANTEIL` der größten lang; z liegt
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
    halb = 0.5 * np.maximum(spanne, MINDESTHOEHE_ANTEIL * groesste) * (1.0 + 2.0 * _RAND)
    halb[2] = max(halb[2], ueberhoehung * daten.d_ref * (1.0 + 2.0 * _RAND))
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


def _text_spalte(texte: tuple[str, ...], stil: Plotstil, spalte_pt: float) -> str:
    """Umbrochener Block der Pflichtangaben (jede Angabe und jede Zeile darin beginnt neu)."""
    zeichen = max(int((spalte_pt - 4.0) / (0.55 * stil.schrift_pt)), 8)
    return "\n".join(textwrap.fill(zeile, zeichen) for t in texte for zeile in t.split("\n"))


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
        titel = achsentitel(
            "Betrag der Auslenkung" if daten.groesse == "auslenkung" else "Betrag der Schnelle",
            einheit,
        )
    cb.set_label(titel, fontsize=stil.schrift_pt)
    cb.ax.yaxis.set_major_formatter(
        FuncFormatter(lambda w, _p: tick_text(w * faktor, dezimalkomma=stil.dezimalkomma))
    )
    z.hilfsobjekte["farbkomponente"] = komp
    z.hilfsobjekte["farbbereich"] = (vmin, vmax)
    z.hilfsobjekte["farbtitel"] = titel


def _z_achse(ax: Any, sichtbar: bool, stil: Plotstil) -> None:
    """Beschriftung der z-Achse ein- oder ausblenden.

    In der Aufsicht (Elevation nahe ±90°) fällt die z-Achse in einen Punkt; ihre Ticks lägen
    übereinander und wären unlesbar.
    """
    if sichtbar:
        ax.zaxis.set_major_formatter(dezimalkomma_formatter(dezimalkomma=stil.dezimalkomma))
        ax.set_zlabel(achsentitel("z", "m"), fontsize=stil.schrift_pt)
    else:
        ax.zaxis.set_major_formatter(NullFormatter())
        ax.set_zlabel("")


def _dynamisch(
    z: Zeichnung, daten: AnimationsDaten, opt: AnimationsOptionen, vorher: AnimationsOptionen | None
) -> None:
    """Setzt alle vom Winkel, der Skalierung, dem Blick und dem Farbbereich abhängigen Größen.

    Beim ersten Aufruf (``vorher is None``) wird alles gesetzt; danach nur, was sich ändert.
    Gemeinsamer Weg von :func:`zeichne_animation` und :func:`aktualisiere_animation`; das
    garantiert die Gleichheit beider Wege.

    Zuerst werden **alle** Größen berechnet und geprüft (Skalierung, Farbskala, Grenzen,
    Texte), erst danach wird ein Artist verändert. Ein Fehler (z. B. ein Farbbereich mit
    ``von >= bis``) lässt das Bild deshalb unverändert, nie halb aktualisiert.
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
    spaltentext = _text_spalte(texte, stil, spalte_pt)
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
        ax.set_box_aspect(aspekt, zoom=opt.blick.zoom)
    elif vorher is not None and opt.blick.zoom != vorher.blick.zoom:
        ax.set_box_aspect(z.hilfsobjekte["box_aspekt"], zoom=opt.blick.zoom)
    if vorher is None or opt.blick != vorher.blick:
        ax.view_init(elev=opt.blick.elev_grad, azim=opt.blick.azim_grad)
        _z_achse(ax, abs(opt.blick.elev_grad) < _ELEV_AUFSICHT_GRAD, stil)
    if vorher is None or opt.vereinfacht != vorher.vereinfacht:
        if opt.vereinfacht:
            ax.set_axis_off()
        else:
            ax.set_axis_on()
    z.hilfsobjekte["pflichttext"].set_text(spaltentext)
    z.hilfsobjekte["pflichtangaben"] = texte
    z.hinweise = (hinweis,) if hinweis else ()
    z.hilfsobjekte["optionen"] = opt
    z.hilfsobjekte["skalierung"] = s
    z.hilfsobjekte["ueberhoehung"] = daten.ueberhoehung_aequivalent(s)


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
    _komp, vmin, vmax = farbskala(
        daten, opt
    )  # prüft den Farbbereich, bevor die Figure geleert wird
    fig.clear()
    fig.set_layout_engine("none")
    fig.set_facecolor(stil.flaeche)
    rect = layout_rect(fig)
    kennzeichen = [t for t in kennzeichen_texte(daten, opt) if t]
    kaesten, (x0, y0, breite, hoehe) = kennzeichen_kopf(fig, stil, kennzeichen, rect)

    ax: Any = fig.add_axes(
        (x0, y0, _BREITE_3D * breite, hoehe), projection="3d", computed_zorder=False
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

    # --- rechte Spalte: Pflichtangaben, Zeichenerklärung, Farbleiste -------------------------
    rechts: Any = fig.add_axes((x0 + _SPALTE_X * breite, y0, _SPALTE_B * breite, hoehe))
    rechts.set_axis_off()
    z.hilfsobjekte["rechts"] = rechts
    spalte_pt = _SPALTE_B * breite * float(fig.get_figwidth()) * 72.0
    z.hilfsobjekte["spalte_pt"] = spalte_pt
    z.hilfsobjekte["pflichttext"] = rechts.text(
        0.0, 1.0, "", transform=rechts.transAxes, ha="left", va="top",
        fontsize=stil.schrift_pt, color=stil.achse,
    )  # fmt: skip
    z.texte.append(z.hilfsobjekte["pflichttext"])
    cax = rechts.inset_axes((0.1, 0.04, 0.3, 0.3))
    z.hilfsobjekte["farbleiste"] = fig.colorbar(z.marker["punkte"], cax=cax)
    cb = z.hilfsobjekte["farbleiste"]
    cb.ax.tick_params(labelsize=stil.schrift_pt, colors=stil.achse)
    cb.outline.set_edgecolor(stil.achse)
    _dynamisch(z, daten, opt, None)

    # Zeichenerklärung unter den Pflichtangaben, Farbleiste darunter (gemessene Höhen)
    fig.draw_without_rendering()
    box = rechts.bbox
    y_unten = (float(z.hilfsobjekte["pflichttext"].get_window_extent().y0) - float(box.y0)) / float(
        box.height
    ) - 0.03
    eintraege, anzahl = _zeichenerklaerung(daten, opt, stil)
    z.hilfsobjekte["anzahl"] = anzahl
    if eintraege:
        zeichen = max(int((spalte_pt - 26.0) / (0.55 * stil.schrift_pt)), 8)
        legende = rechts.legend(
            handles=[h for h, _ in eintraege],
            labels=[textwrap.fill(t, zeichen) for _, t in eintraege],
            loc="upper left",
            bbox_to_anchor=(0.0, y_unten),
            borderaxespad=0.0,
            frameon=False,
            fontsize=stil.schrift_pt,
            handlelength=1.2,
            handletextpad=0.5,
            labelspacing=0.6,
            numpoints=1,
        )
        z.hilfsobjekte["zeichenerklaerung"] = legende
        fig.draw_without_rendering()
        y_unten = (float(legende.get_window_extent().y0) - float(box.y0)) / float(box.height) - 0.04
    hoehe_cb = max(min(y_unten - 0.06, 0.6), 0.15)
    cax.set_position(
        (
            x0 + (_SPALTE_X + 0.1 * _SPALTE_B) * breite,
            y0 + 0.04 * hoehe,
            0.3 * _SPALTE_B * breite,
            hoehe_cb * hoehe,
        )
    )
    return z


def aktualisiere_animation(
    zeichnung: Zeichnung, daten: AnimationsDaten, opt: AnimationsOptionen, stil: Plotstil
) -> None:
    """Teilaktualisierung: setzt nur Artist-Daten, ruft nie ``fig.clear()`` und kein Layout.

    Geändert werden dürfen Winkel, Überhöhung, Blick (auch Zoom), ``vereinfacht`` und
    Farbbereich. Das Ergebnis ist gleich dem eines frischen :func:`zeichne_animation` mit
    denselben Optionen (Positionen, Farben, Pflichttexte, Grenzen).

    Raises
    ------
    ValueError
        ``daten`` oder ``stil`` sind nicht die der Zeichnung, oder eine Option, die den Aufbau
        des Bildes betrifft (``farbe``, ``farb_komponente``, ``ruhelage``, ``punktlabels``,
        Kennzeichen), unterscheidet sich: dann ist neu zu zeichnen.
    """
    vorher: AnimationsOptionen | None = zeichnung.hilfsobjekte.get("optionen")
    if vorher is None:
        raise ValueError("Zeichnung stammt nicht von zeichne_animation")
    if zeichnung.hilfsobjekte["daten"] is not daten or zeichnung.hilfsobjekte["stil"] != stil:
        raise ValueError("andere Daten oder anderer Stil: neu zeichnen")
    feste = ("farbe", "farb_komponente", "ruhelage", "punktlabels", "kennzeichen_phase")
    if any(getattr(opt, n) != getattr(vorher, n) for n in feste) or (
        opt.kennzeichen_koordinaten != vorher.kennzeichen_koordinaten
    ):
        raise ValueError("Aufbau des Bildes geändert (Farbe, Ruhelage, Kennzeichen): neu zeichnen")
    _dynamisch(zeichnung, daten, opt, vorher)
