r"""Datenvertrag der 3D-Animation der Betriebsschwingform (R-071, FG-04, FG-04 Nachtrag 1).

Keine neue Mathematik: Dieses Modul **setzt zusammen**, was :mod:`ldv_automation.auswertung`
(``schwingform_aus``, :mod:`ldv_automation.auswertung.animation`) und :class:`.auswahl.PaarCache`
liefern, und stellt die Größen bereit, die die Zeichenfunktion
(:mod:`ldv_automation.darstellung.animation3d`) braucht: Amplituden ``(P, 3)``, Masken ``(P, 3)``,
Status je Punkt, :math:`D_\mathrm{ref}`, :math:`s` und die rein rechnenden Bildgrößen
(:meth:`AnimationsDaten.positionen`, :meth:`AnimationsDaten.auslenkung`).

Die Daten sind zustandslos: Jedes Bild rechnet :meth:`AnimationsDaten.positionen` neu. Standbild
und Bewegung sind deshalb derselbe Datenpfad (UI-25).

Annahmen (FG-04 3.6, Nachtrag 1): Ein Punkt bewegt sich nur, wenn alle gewählten Komponenten
gültig (M6), kohärent (:math:`\gamma^2 \ge \gamma^2_\mathrm{min}`) und endlich sind (A-1); beim
3D-Vektor heißt ein Ausfall einer Komponente „3D unvollständig“. Der Bezugspunkt muss ein
bewegter Punkt sein (A-2); Voreinstellung in 3D ist der bewegte Punkt mit der größten
``auslenkung_max`` (A-3).
"""

from __future__ import annotations

import math
from dataclasses import dataclass, replace
from typing import Literal

import numpy as np
import numpy.typing as npt

from ldv_automation.auswertung.animation import (
    ALPHA_VORGABE,
    Groesse,
    animierte_amplitude,
    bewegt_maske,
    bezugsgroesse,
    bezugsphase,
    positionen_m,
    ueberhoehung_auto,
    ueberhoehung_hinweis,
    verschiebung,
    waehle_bezugspunkt_3d,
)
from ldv_automation.auswertung.annahmen import ANNAHME, AnnahmeEintrag, AnnahmenStufe2
from ldv_automation.auswertung.daten import (
    BoolArray,
    ComplexArray,
    FloatArray,
    IntArray,
    Messdaten,
)
from ldv_automation.auswertung.gesamt import KOMPONENTEN_3D, schwingform_aus
from ldv_automation.auswertung.schwingform import Quelle, waehle_bezugspunkt

from .auswahl import (
    KOMPONENTEN,
    DarstellungsFehler,
    Ebene,
    PaarCache,
    _standard_referenz,
    waehle_ebene,
)
from .formate import zahl_kurz_text

__all__ = [
    "BEWEGT",
    "KEIN_WERT",
    "NULL",
    "TEXT_KEINE_PHASE",
    "TEXT_KEINE_PUNKTE",
    "UNGUELTIG",
    "UNSICHER",
    "AnimationsDaten",
    "BezugModus",
    "NachbarAbstaende",
    "animation_daten",
    "naechste_abstaende_3d",
]

BEWEGT = 0
"""Status: bewegt sich nach FG-04 3.2."""
NULL = 1
"""Status: :math:`|\\hat v| = 0` an allen gewählten Komponenten, gültig, bewegt sich nicht."""
UNSICHER = 2
"""Status: :math:`\\gamma^2 < \\gamma^2_\\mathrm{min}` (bei 3D: mindestens eine Komponente)."""
UNGUELTIG = 3
"""Status: von PSV als ungültig markiert (M6)."""
KEIN_WERT = 4
"""Status: Amplitude nicht endlich (NaN, Inf)."""

TEXT_KEINE_PHASE = "Animation braucht eine Phase: keine Referenz."
"""Meldung ohne gültige Phase (UI-30, RF-A14)."""
TEXT_KEINE_PUNKTE = "Keine Punkte mit gültiger Phase."
"""Meldung, wenn kein Punkt animiert werden kann (:math:`D_\\mathrm{ref}` fehlt)."""

BezugModus = Literal["relativ", "absolut"]
"""Phasenbezug: relativ zu einem Bezugspunkt (Voreinstellung) oder absolut gegen die Referenz."""

EPS_REL = 1e-6
r""":math:`\varepsilon_\mathrm{rel}` der Duplikattoleranz (FG-04 Nachtrag 3, Abschnitt 3)."""
EPS_ABS_M = 1e-8
r""":math:`\varepsilon_\mathrm{abs}` in m, Boden der Duplikattoleranz (FG-04 Nachtrag 3)."""
_BLOCK_ELEMENTE = 1_000_000
"""Größe eines Blocks der Abstandsrechnung in Matrixelementen (Zeilen · Spalten); je Hilfsfeld
8 MB, der Spitzenbedarf ist unabhängig von P etwa das Vierfache (FG-04 Nachtrag 2 4.3)."""

_ACHSE_SENKRECHT: dict[str, int] = {"xy": 2, "xz": 1, "yz": 0}
_BUCHSTABEN = ("X", "Y", "Z")


@dataclass(frozen=True, kw_only=True, eq=False)
class AnimationsDaten:
    r"""Daten der 3D-Animation bei einer Linie (Plan P-AUSW3, Abschnitt 2.2).

    Attributes
    ----------
    f_wahl_hz, f_hz : float
        Gewählte Frequenz und Frequenz der Linie :math:`f_{k^\ast}` (RF-A9).
    linie : int
        0-basierter Linienindex.
    omega_rad_s : float
        :math:`\omega = 2\pi f_{k^\ast}`.
    koordinaten_m : numpy.ndarray
        Ruhelage ``(P, 3)`` in m.
    label : numpy.ndarray
        Punktlabels ``(P,)``.
    ebene : {"xy", "xz", "yz"}
        Voreingestellte Projektionsebene (:func:`.auswahl.waehle_ebene`).
    komponente : str
        ``"X"``, ``"Y"``, ``"Z"`` oder ``"3D"``.
    amplitude_v : numpy.ndarray
        :math:`\hat v` ``(P, 3)`` aus ``Schwingform.amplitude`` (m/s bzw. (m/s)/N).
    amplitude_anim : numpy.ndarray
        Animierte Amplitude ``(P, 3)`` (:math:`\hat d` in m bzw. m/N, bei Größe Schnelle
        :math:`\hat w`); NaN in den Zeilen nicht bewegter Punkte. Bei einer Einzelkomponente
        sind die beiden anderen Spalten 0.
    achsen_aktiv : numpy.ndarray
        ``(3,)`` bool: bei einer Einzelkomponente genau eine, bei 3D alle.
    kohaerenz, kohaerenz_ok : numpy.ndarray
        :math:`\gamma^2` und Maske ``(P, 3)``; Einzelkomponente: nur die gewählte Spalte, die
        übrigen NaN bzw. ``True``.
    status : numpy.ndarray
        ``(P,)`` int8, :data:`BEWEGT`, :data:`NULL`, :data:`UNSICHER`, :data:`UNGUELTIG`,
        :data:`KEIN_WERT`; Rangfolge UNGUELTIG > KEIN_WERT > UNSICHER wie in der 2D-Ansicht 4
        (``schwingform.py``). Das weicht von Plan P-AUSW3 2.2 ab (dort KEIN_WERT > UNGUELTIG);
        es gilt die Rangfolge der Ansicht 4, damit derselbe Punkt in beiden Bildern dasselbe
        Kennzeichen trägt (Fachabnahme FA-AN3 MINOR-3).
    bewegt : numpy.ndarray
        ``(P,)`` bool: Punkte, die in :meth:`positionen` bewegt werden (Maske des Kerns,
        :func:`~ldv_automation.auswertung.animation.bewegt_maske`); enthält auch :data:`NULL`.
    grund_3d_unvollstaendig : numpy.ndarray
        ``(P,)`` bool: :data:`UNSICHER` bei 3D (Zeichenerklärung „3D unvollständig“).
    d_ref : float
        Bezugsgröße (größte Spitzenauslenkung der bewegten Punkte) in m bzw. m/N bzw. m/s.
    d_nn_m, d_nn_min_m : float or None
        Median und Minimum der **räumlichen** Abstände zum nächsten Nachbarn der
        **Repräsentanten** (FG-04 Nachtrag 2, Abschnitt 4 und Nachtrag 3: je Ort der erste Punkt,
        Duplikate zählen nicht; auch nicht animierte Punkte zählen); ``None`` bei weniger als
        zwei Repräsentanten.
    n_dup : int
        Zahl der Duplikate (Punkte mit einem früheren Punkt im Abstand :math:`\le\varepsilon`,
        FG-04 Nachtrag 3).
    eps_dup_m : float
        Duplikattoleranz :math:`\varepsilon` in m (Nachtrag 3, Abschnitt 3).
    s_auto : float or None
        Automatische **Skalierung** :math:`\alpha\,d_\mathrm{NN}/D_\mathrm{ref}`. Die Einheit
        hängt von der Größe ab (:attr:`skalierung_einheit`): bei der Auslenkung die
        dimensionslose Überhöhung :math:`s`, bei der Schnelle die Skalierung :math:`\kappa` in s
        (FG-04 Nachtrag 2 3.1). Die vergleichbare Überhöhung gegenüber der Auslenkung ist
        :attr:`s_auto_aequivalent` bzw. :meth:`ueberhoehung_aequivalent`.
    groesse : {"auslenkung", "schnelle"}
        Animierte Größe.
    einheit_anim : str
        Einheit von ``amplitude_anim`` (m, m/N, m/s, (m/s)/N).
    quelle : str
        ``"cph"`` oder ``"h1"``.
    referenz : str or None
        Bezugskanal der Phase.
    bezug_modus : {"relativ", "absolut"}
        Phasenbezug.
    bezug_index : int or None
        Bezugspunkt (0-basiert) bei relativem Bezug.
    bezug_komponente : int or None
        Pivot-Komponente 0..2 des Bezugs (Nachtrag 1); bei einer Einzelkomponente deren Index.
    kohaerenz_min : float or None
        Schwelle :math:`\gamma^2_\mathrm{min}`.
    phase_gueltig : bool
        Immer ``True`` (ohne Phase gibt es diese Daten nicht).
    hinweise : tuple of str
        Hinweise des Kerns.
    annahmen : tuple of AnnahmeEintrag
        Geltende Annahmen.
    """

    f_wahl_hz: float
    f_hz: float
    linie: int
    omega_rad_s: float
    koordinaten_m: FloatArray
    label: IntArray
    ebene: Ebene
    komponente: str
    amplitude_v: ComplexArray
    amplitude_anim: ComplexArray
    achsen_aktiv: BoolArray
    kohaerenz: FloatArray
    kohaerenz_ok: BoolArray
    status: npt.NDArray[np.int8]
    bewegt: BoolArray
    grund_3d_unvollstaendig: BoolArray
    d_ref: float
    d_nn_m: float | None
    d_nn_min_m: float | None
    n_dup: int
    eps_dup_m: float
    s_auto: float | None
    groesse: Groesse
    einheit_anim: str
    quelle: Quelle
    referenz: str | None
    bezug_modus: BezugModus
    bezug_index: int | None
    bezug_komponente: int | None
    kohaerenz_min: float | None
    phase_gueltig: bool
    hinweise: tuple[str, ...]
    annahmen: tuple[AnnahmeEintrag, ...]

    @property
    def anzahl_punkte(self) -> int:
        """Zahl der Messpunkte."""
        return int(self.koordinaten_m.shape[0])

    @property
    def hinweis_duplikate(self) -> str | None:
        r"""Informationshinweis zu doppelten Punkten (Nachtrag 3 Abschnitt 3); ``None`` ohne.

        Kein Überlagerungshinweis: Duplikate liegen bei jeder Überhöhung übereinander.
        """
        if self.n_dup == 0:
            return None
        grenze = zahl_kurz_text(self.eps_dup_m, 4)  # Dezimalkomma, 4 signifikante Stellen
        if self.n_dup == 1:
            return (
                f"1 Punkt liegt auf dem Ort eines anderen Punkts (Abstand \u2264 {grenze} m) "
                "und zählt beim Nachbarabstand nicht mit"
            )
        return (
            f"{self.n_dup} Punkte liegen auf dem Ort anderer Punkte (Abstand \u2264 {grenze} m) "
            "und zählen beim Nachbarabstand nicht mit"
        )

    @property
    def skalierung_einheit(self) -> str:
        r"""Einheit der Skalierung: ``"1"`` (Überhöhung :math:`s`) bzw. ``"s"`` (Schnelle)."""
        return "s" if self.groesse == "schnelle" else "1"

    def ueberhoehung_aequivalent(self, skalierung: float) -> float:
        r"""Äquivalente Überhöhung :math:`s_\ddot{a}` gegenüber der realen Auslenkung.

        Auslenkung: :math:`s_\ddot{a} = s`. Schnelle: :math:`s_\ddot{a} = \kappa\,\omega` mit
        :math:`\omega` der **Linie** (FG-04 Nachtrag 2 3.1). Bei :math:`\omega \le 0` NaN.
        """
        if self.groesse != "schnelle":
            return float(skalierung)
        if not self.omega_rad_s > 0.0:
            return math.nan
        return float(skalierung) * self.omega_rad_s

    def skalierung_aus_ueberhoehung(self, ueberhoehung_aequiv: float) -> float:
        r"""Umkehrung von :meth:`ueberhoehung_aequivalent`: :math:`\kappa = s_\ddot{a}/\omega`."""
        if self.groesse != "schnelle":
            return float(ueberhoehung_aequiv)
        if not self.omega_rad_s > 0.0:
            return math.nan
        return float(ueberhoehung_aequiv) / self.omega_rad_s

    @property
    def s_auto_aequivalent(self) -> float | None:
        r""":math:`s_\ddot{a}` der automatischen Skalierung; ``None`` ohne :attr:`s_auto`.

        Bei der Schnelle gleich dem :math:`s_\mathrm{auto}` der Auslenkung (Nachtrag 2 3.2).
        """
        if self.s_auto is None:
            return None
        return self.ueberhoehung_aequivalent(self.s_auto)

    @property
    def d_ref_auslenkung(self) -> float:
        r""":math:`D_\mathrm{ref}` als Spitzenauslenkung (m bzw. m/N).

        Bei der Schnelle :math:`D_{\mathrm{ref},v}/\omega`.
        """
        if self.groesse != "schnelle":
            return self.d_ref
        return self.d_ref / self.omega_rad_s if self.omega_rad_s > 0.0 else math.nan

    @property
    def einheit_auslenkung(self) -> str:
        """Einheit der Spitzenauslenkung: ``"m"`` bzw. ``"m/N"``."""
        return _einheit_anim(self.einheit_anim, "auslenkung")

    def positionen(self, theta_rad: float, ueberhoehung: float) -> FloatArray:
        r"""Bildpositionen :math:`\vec X_p + s\,\mathrm{Re}\{\hat d_p e^{i\theta}\}` ``(P, 3)``.

        ``ueberhoehung`` ist die **Skalierung** (Auslenkung: :math:`s` dimensionslos; Schnelle:
        :math:`\kappa` in s, Einheit m/s · s = m, :attr:`skalierung_einheit`). Nicht bewegte
        Punkte liegen **exakt** in der Ruhelage (RF-A8); die Skalierung ändert daran nichts.
        """
        return positionen_m(
            self.koordinaten_m, self.amplitude_anim, theta_rad, ueberhoehung, self.bewegt
        )

    def auslenkung(self, theta_rad: float) -> FloatArray:
        r"""Momentane Auslenkung :math:`\mathrm{Re}\{\hat d_p e^{i\theta}\}` ``(P, 3)``.

        Ohne Überhöhung (m bzw. m/N bzw. m/s); 0 für nicht bewegte Punkte.
        """
        a = np.zeros(self.amplitude_anim.shape, dtype=np.float64)
        a[self.bewegt] = verschiebung(self.amplitude_anim[self.bewegt], theta_rad)
        return a

    def betrag(self, theta_rad: float) -> FloatArray:
        """Betrag des momentanen Auslenkungsvektors ``(P,)``; NaN für nicht bewegte Punkte."""
        norm: FloatArray = np.linalg.norm(self.auslenkung(theta_rad), axis=1)
        return np.where(self.bewegt, norm, np.nan)

    def farbwert(self, theta_rad: float, komponente: int) -> FloatArray:
        """Vorzeichenbehaftete Komponente 0..2 der momentanen Auslenkung ``(P,)``.

        NaN für nicht bewegte Punkte.
        """
        if not 0 <= komponente < 3:
            raise ValueError(f"Komponente 0..2 erwartet: {komponente}")
        wert = self.auslenkung(theta_rad)[:, komponente]
        return np.where(self.bewegt, wert, np.nan)

    def farbgrenze(self, art: Literal["auslenkung", "betrag"], komponente: int) -> float:
        r"""Größter Betrag der Farbgröße über eine **volle Periode** (geschlossen, ohne Abtastung).

        Auslenkung: :math:`\max_p |\hat d_{pc}|`; Betrag: :math:`D_\mathrm{ref}` (große Halbachse
        der Bahnellipse). Die Skala pumpt deshalb nicht mit dem Bild. Ist die Komponente überall 0,
        gilt :math:`D_\mathrm{ref}`.
        """
        if art == "betrag":
            return self.d_ref
        if not 0 <= komponente < 3:
            raise ValueError(f"Komponente 0..2 erwartet: {komponente}")
        werte = np.abs(self.amplitude_anim[self.bewegt, komponente])
        maximum = float(np.max(werte)) if werte.size else 0.0
        return maximum if maximum > 0.0 else self.d_ref

    def farb_komponente_standard(self) -> int:
        """Voreinstellung der Farbkomponente.

        Die gewählte Komponente, bei 3D die Achse senkrecht zur Projektionsebene (die in
        :attr:`ebene` fehlende).
        """
        if self.komponente != "3D":
            return _BUCHSTABEN.index(self.komponente)
        return _ACHSE_SENKRECHT[self.ebene]

    def hinweis_ueberhoehung(self, ueberhoehung: float) -> str | None:
        r"""Hinweis „Punkte können sich überlagern“ (FG-04 3.5).

        Bedingung :math:`s D_\mathrm{ref} \ge d_\mathrm{NN,min}/2` bzw. bei der Schnelle
        :math:`\kappa D_{\mathrm{ref},v} \ge d_\mathrm{NN,min}/2`; beides ist die größte
        gezeigte Strecke in m (Nachtrag 2 3.4). ``ueberhoehung`` ist die Skalierung.
        ``None`` bei nur einem Punkt (kein Nachbarabstand) oder unterhalb der Grenze.
        """
        if self.d_nn_min_m is None:
            return None
        return ueberhoehung_hinweis(ueberhoehung, self.d_ref, self.d_nn_min_m)


@dataclass(frozen=True)
class NachbarAbstaende:
    r"""Ergebnis von :func:`naechste_abstaende_3d` (FG-04 Nachtrag 3).

    Attributes
    ----------
    abstaende_m : numpy.ndarray
        Abstand jedes Repräsentanten zum nächsten anderen Repräsentanten in m; leer bei weniger
        als zwei Repräsentanten.
    eps_m : float
        Duplikattoleranz :math:`\varepsilon` in m.
    n_dup : int
        Zahl der Duplikate.
    """

    abstaende_m: FloatArray
    eps_m: float
    n_dup: int


def _block_zeilen(spalten: int) -> int:
    """Zeilen je Block, so dass Zeilen · Spalten höchstens :data:`_BLOCK_ELEMENTE` ist."""
    return max(1, _BLOCK_ELEMENTE // max(spalten, 1))


def _abstaende_zu(x: FloatArray, zeilen: slice, spalten: slice) -> FloatArray:
    """Euklidische Abstände der Punkte ``x[zeilen]`` zu ``x[spalten]``, komponentenweise summiert.

    Dieselbe Rechenfolge wie ``sqrt(sum(diff * diff, axis=2))`` über die drei Komponenten, aber
    ohne das ``(Zeilen, Spalten, 3)``-Feld.
    """
    a = x[zeilen]
    b = x[spalten]
    quadrat = np.zeros((a.shape[0], b.shape[0]), dtype=np.float64)
    for c in range(x.shape[1]):
        d = a[:, c, None] - b[None, :, c]
        quadrat += d * d
    abstand: FloatArray = np.sqrt(quadrat)
    return abstand


def naechste_abstaende_3d(x: FloatArray) -> NachbarAbstaende:
    r"""Nächste-Nachbar-Abstände mit Duplikatregel (FG-04 Nachtrag 2 Abschnitt 4, Nachtrag 3).

    Skala :math:`S = \max(\lVert\max_p X_p - \min_p X_p\rVert, \max_p\lVert X_p\rVert)`,
    Toleranz :math:`\varepsilon = \max(\varepsilon_\mathrm{abs}, \varepsilon_\mathrm{rel} S)`.
    Punkt :math:`i` ist Duplikat, wenn ein Punkt :math:`j < i` mit Abstand
    :math:`\le\varepsilon` existiert (Gleichheit zählt). Die Abstände laufen nur über die
    Nicht-Duplikate (Repräsentanten). Die Rechnung geht blockweise (:data:`_BLOCK_ELEMENTE`); das
    Ergebnis hängt nicht von der Blockgröße ab.

    Parameters
    ----------
    x : numpy.ndarray
        Ruhelagen ``(P, 3)`` in m, endlich (Aufgabe des Einlesens).
    """
    n = int(x.shape[0])
    if n == 0:
        return NachbarAbstaende(np.empty(0, dtype=np.float64), EPS_ABS_M, 0)
    ausdehnung = float(np.linalg.norm(np.max(x, axis=0) - np.min(x, axis=0)))
    skala = max(ausdehnung, float(np.max(np.linalg.norm(x, axis=1))))
    eps = max(EPS_ABS_M, EPS_REL * skala)

    # Duplikate: Zeile i gegen alle früheren Spalten j < i (Spalten nur bis zum Blockende)
    block = _block_zeilen(n)
    dup = np.zeros(n, dtype=bool)
    for start in range(0, n, block):
        ende = min(start + block, n)
        nah = _abstaende_zu(x, slice(start, ende), slice(0, ende)) <= eps
        frueher = np.arange(ende)[None, :] < np.arange(start, ende)[:, None]
        dup[start:ende] = np.any(nah & frueher, axis=1)
    n_dup = int(np.sum(dup))

    rep = x[~dup]
    m = int(rep.shape[0])
    if m < 2:
        return NachbarAbstaende(np.empty(0, dtype=np.float64), eps, n_dup)
    kleinste = np.empty(m, dtype=np.float64)
    block = _block_zeilen(m)
    for start in range(0, m, block):
        ende = min(start + block, m)
        abstand = _abstaende_zu(rep, slice(start, ende), slice(0, m))
        abstand[np.arange(ende - start), np.arange(start, ende)] = np.inf  # nicht der Punkt selbst
        kleinste[start:ende] = np.min(abstand, axis=1)
    return NachbarAbstaende(kleinste, eps, n_dup)


def _einheit_anim(einheit_v: str, groesse: Groesse) -> str:
    """Einheit der animierten Größe aus der Einheit der Schnelle."""
    if groesse == "schnelle":
        return einheit_v
    return "m/N" if "N" in einheit_v else "m"


def _m12_eintrag(annahmen2: AnnahmenStufe2 | None) -> tuple[AnnahmeEintrag, ...]:
    """Eintrag M12 aus den Annahmen der Stufe 2 (leer ohne Angabe: M12 bleibt Pflicht).

    Die Animation wendet die Drehung D (``v_geo = D·v``) nicht an. Ist D nicht exakt die
    Einheitsmatrix, wird der Status deshalb als offen geführt und der Wert nennt, dass D nicht
    dargestellt wird (fail-closed: das Kennzeichen M12 bleibt, auch bei bestätigtem Status).
    """
    if annahmen2 is None:
        return ()
    eintraege = tuple(e for e in annahmen2.eintraege() if e.nr == "M12")
    if np.array_equal(annahmen2.drehung, np.eye(3)):
        return eintraege
    return tuple(
        replace(
            e,
            wert="D ≠ Einheitsmatrix, in der Animation nicht angewendet",
            status=ANNAHME,
        )
        for e in eintraege
    )


def animation_daten(
    daten: Messdaten,
    cache: PaarCache,
    f_wahl_hz: float,
    *,
    komponente: str = "3D",
    groesse: Groesse = "auslenkung",
    bezug_modus: BezugModus = "relativ",
    bezug: int | None = None,
    bezug_komponente: int | None = None,
    referenz: str | None = None,
    quelle: Quelle = "cph",
    alpha: float = ALPHA_VORGABE,
    annahmen2: AnnahmenStufe2 | None = None,
) -> AnimationsDaten:
    r"""Daten der Animation bei ``f_wahl_hz``.

    Die Kanalpaare der Komponenten werden über ``cache`` bei Bedarf berechnet (3D: drei Paare mit
    derselben Referenz). Nur bei ``komponente="3D"`` und weniger als drei gehaltenen Paaren wird
    die Größe von ``cache`` auf drei erhöht (:meth:`.auswahl.PaarCache.setze_groesse`), sonst
    verdrängte das dritte Paar das erste; eine Einzelkomponente braucht nur ein Paar.

    Parameters
    ----------
    daten : Messdaten
        Eingangsdaten.
    cache : PaarCache
        Kohärenz je Komponente (:math:`\gamma^2` an der Linie).
    f_wahl_hz : float
        Gewählte Frequenz in Hz (rastet auf die nächste Linie ein, RF-A9).
    komponente : str
        ``"X"``, ``"Y"``, ``"Z"`` oder ``"3D"`` (Vektor aller drei Komponenten, A-1).
    groesse : {"auslenkung", "schnelle"}
        Animierte Größe (E1).
    bezug_modus : {"relativ", "absolut"}
        Relativ zu einem Bezugspunkt (Voreinstellung) oder absolut gegen die Referenz (M8).
    bezug : int, optional
        Bezugspunkt (0-basiert); ``None`` = Voreinstellung (3D: A-3, sonst größtes :math:`|v|`
        unter den kohärenten gültigen Punkten).
    bezug_komponente : int, optional
        Nur 3D: Pivot-Komponente 0..2 des Bezugspunkts; ``None`` = betragsgrößte (Nachtrag 1).
    referenz : str, optional
        Referenzkanal; Voreinstellung wie :func:`.auswahl.schwingform_daten`.
    quelle : {"cph", "h1"}
        Herkunft der Amplitude.
    alpha : float
        Größte angezeigte Strecke in Einheiten von :math:`d_\mathrm{NN}` (FG-04 3.5);
        :math:`d_\mathrm{NN}` ist räumlich (FG-04 Nachtrag 2, Abschnitt 4) und läuft nur über
        Nicht-Duplikate (FG-04 Nachtrag 3).
    annahmen2 : AnnahmenStufe2, optional
        Annahmen der Stufe 2: Der Status von M12 (Komponenten im Geometrie-KS) kommt als Eintrag
        in :attr:`AnimationsDaten.annahmen`, damit das Kennzeichen M12 genau bei bestätigtem
        Status entfällt (analog M8; Nutzerentscheidung 2026-11-18). Ohne Angabe bleibt es
        Pflicht.

    Raises
    ------
    DarstellungsFehler
        Ohne Phase (:data:`TEXT_KEINE_PHASE`), ohne bewegbaren Punkt oder mit
        :math:`D_\mathrm{ref} = 0` (:data:`TEXT_KEINE_PUNKTE`), bei unbekannter Komponente,
        ungültigem Bezug (nicht bewegt, :math:`|v| = 0`, außerhalb) oder Frequenz außerhalb der
        Achse (Text des Kerns).
    """
    if komponente not in KOMPONENTEN:
        raise DarstellungsFehler(f"Unbekannte Komponente {komponente!r}.")
    if bezug_modus not in ("relativ", "absolut"):
        raise ValueError(f"bezug_modus 'relativ' oder 'absolut' erwartet: {bezug_modus!r}")
    ref = referenz or _standard_referenz(daten, ("3D",)) or "Ref1"
    try:
        sf = schwingform_aus(
            daten,
            f_wahl_hz,
            referenz=ref,
            quelle="h1" if quelle == "h1" else "cph",
            annahmen=cache.annahmen,
        )
    except ValueError as exc:
        raise DarstellungsFehler(str(exc)) from exc
    if not sf.phase_gueltig or sf.amplitude is None:
        raise DarstellungsFehler(TEXT_KEINE_PHASE)

    v = sf.amplitude
    anzahl = int(v.shape[0])
    index = None if komponente == "3D" else _BUCHSTABEN.index(komponente)
    aktiv = np.ones(3, dtype=bool) if index is None else np.arange(3) == index
    if index is None and cache.groesse < len(KOMPONENTEN_3D):
        cache.setze_groesse(len(KOMPONENTEN_3D))
    g2 = np.full((anzahl, 3), np.nan, dtype=np.float64)
    ok = np.ones((anzahl, 3), dtype=bool)
    g2_min: float | None = None
    for c in np.flatnonzero(aktiv):
        frf = cache.paar(KOMPONENTEN_3D[int(c)], ref).frf
        g2[:, c] = frf.kohaerenz[:, sf.linie]
        ok[:, c] = frf.kohaerenz_ok[:, sf.linie]
        g2_min = frf.kohaerenz_min
    gueltig = cache.gueltig()

    # --- Maske und Status (FG-04 3.6, A-1) --------------------------------------------------
    sel = v[:, aktiv]
    ok_sel = ok[:, aktiv]
    if index is None:
        bewegt = bewegt_maske(v, ok, gueltig)
    else:
        bewegt = bewegt_maske(v[:, index], ok[:, index], gueltig)
    endlich = np.all(np.isfinite(sel), axis=1)
    unsicher = ~np.all(ok_sel, axis=1)
    status = np.full(anzahl, BEWEGT, dtype=np.int8)
    # Rangfolge wie Ansicht 4 (schwingform.py): UNGUELTIG vor KEIN_WERT vor UNSICHER
    status[unsicher] = UNSICHER
    status[~endlich] = KEIN_WERT
    status[~gueltig] = UNGUELTIG
    # Gültig, kohärent, endlich, aber v = 0: bewegt sich nicht, kein Kennzeichen
    null = bewegt & np.all(sel == 0.0, axis=1)
    status[null] = NULL
    unvollstaendig = (status == UNSICHER) & (index is None)
    if not np.any(bewegt):
        raise DarstellungsFehler(TEXT_KEINE_PUNKTE)

    # --- animierte Amplitude (Nachtrag 1: ein gemeinsamer Skalar) ---------------------------
    bezug_idx: int | None = None
    c_b: int | None = None
    try:
        if bezug_modus == "relativ":
            if bezug is not None:
                bezug_idx = int(bezug)
            elif index is None:
                bezug_idx = waehle_bezugspunkt_3d(v, bewegt)
            else:
                bezug_idx = waehle_bezugspunkt(np.abs(v[:, index]), ok[:, index], gueltig)
            if bezug_idx is None:
                raise DarstellungsFehler(TEXT_KEINE_PUNKTE)
        if index is None:
            anim = animierte_amplitude(
                v,
                sf.f_hz,
                groesse=groesse,
                bezug=bezug_idx,
                komponente=bezug_komponente,
                bewegt=bewegt,
            )
            if bezug_idx is not None:
                c_b = bezugsphase(v[bezug_idx], bezug_komponente)[0]
        else:
            if bezug_komponente not in (None, index):
                raise DarstellungsFehler(
                    "Bei einer Einzelkomponente ist die Bezugskomponente die gewählte."
                )
            eins = animierte_amplitude(
                v[:, index],
                sf.f_hz,
                groesse=groesse,
                bezug=bezug_idx,
                bewegt=bewegt,
            )
            anim = np.zeros((anzahl, 3), dtype=np.complex128)
            anim[:, index] = eins
            c_b = index if bezug_idx is not None else None
    except ValueError as exc:
        if isinstance(exc, DarstellungsFehler):
            raise
        raise DarstellungsFehler(str(exc)) from exc
    anim = np.where(bewegt[:, None], anim, np.nan + 0j)

    # --- Bezugsgröße und Überhöhung (FG-04 3.5) --------------------------------------------
    d_ref = bezugsgroesse(anim if index is None else anim[:, index], bewegt)
    if d_ref is None:
        raise DarstellungsFehler(TEXT_KEINE_PUNKTE)
    nachbar = naechste_abstaende_3d(daten.punkte.koordinaten_m)
    nachbarn = nachbar.abstaende_m
    d_nn = float(np.median(nachbarn)) if nachbarn.size else None
    d_nn_min = float(np.min(nachbarn)) if nachbarn.size else None
    s_auto = ueberhoehung_auto(d_nn, d_ref, alpha)

    return AnimationsDaten(
        f_wahl_hz=sf.f_wahl_hz,
        f_hz=sf.f_hz,
        linie=sf.linie,
        omega_rad_s=2.0 * math.pi * sf.f_hz,
        koordinaten_m=daten.punkte.koordinaten_m,
        label=daten.punkte.label,
        ebene=waehle_ebene(daten.punkte.koordinaten_m),
        komponente=komponente,
        amplitude_v=v,
        amplitude_anim=anim,
        achsen_aktiv=aktiv,
        kohaerenz=g2,
        kohaerenz_ok=ok,
        status=status,
        bewegt=bewegt,
        grund_3d_unvollstaendig=unvollstaendig,
        d_ref=d_ref,
        d_nn_m=d_nn,
        d_nn_min_m=d_nn_min,
        n_dup=nachbar.n_dup,
        eps_dup_m=nachbar.eps_m,
        s_auto=s_auto,
        groesse=groesse,
        einheit_anim=_einheit_anim(sf.einheit, groesse),
        quelle=sf.quelle,
        referenz=sf.referenz,
        bezug_modus=bezug_modus,
        bezug_index=bezug_idx,
        bezug_komponente=c_b,
        kohaerenz_min=g2_min,
        phase_gueltig=True,
        hinweise=sf.hinweise,
        annahmen=sf.annahmen + _m12_eintrag(annahmen2),
    )
