r"""B-5: Vergleich mehrerer Messungen und Drift innerhalb einer Messung (FG-03 Abschnitt 4).

Eingang sind zwei Stufe-1-Auswertungen **A** (Bezug) und **B** (Vergleich) mit gleichem
Kanalpaar; beide werden nur gelesen.

- Punktzuordnung (4.1, E4): über das Label (Voreinstellung) oder über Koordinaten als
  gegenseitig nächste Nachbarn innerhalb :math:`d_\mathrm{tol} = 0{,}5\,d_\mathrm{min}`,
  optional nach einer starren Transformation :math:`x_B = R\,x_A + t` aus Passpunkten
  (Kabsch [A]: :math:`H = \sum (x_A - \bar x_A)(x_B - \bar x_B)^\mathsf{T} = U\Sigma V^\mathsf{T}`,
  :math:`R = V\,\mathrm{diag}(1, 1, \det(VU^\mathsf{T}))\,U^\mathsf{T}`,
  :math:`t = \bar x_B - R\bar x_A`). 3D-Größen aus B werden vor jedem Vergleich mit
  :math:`v_{B\to A} = R^\mathsf{T} v_B` in das System A gedreht.
- Spitzenpaarung (4.2): gegenseitig nächste Spitzen mit
  :math:`|f^B - f^A| \le \Delta f_\mathrm{tol} = 2\,\Delta f`.
- FRF-Vergleich je Punkt und Band (4.3) über Linien mit :math:`\gamma^2 \ge \gamma^2_\mathrm{min}`
  in beiden Messungen:
  ``frac`` :math:`= |\sum H^{A*}H^B|^2/(\sum|H^A|^2\sum|H^B|^2)`,
  ``pegel_db`` :math:`= 10\log_{10}(\sum|H^B|^2/\sum|H^A|^2)`,
  ``diff_rel`` :math:`= \lVert H^B - H^A\rVert_2/\lVert H^A\rVert_2`.
- MAC (4.4):
  :math:`|\phi_A^\mathsf{H}\phi_B|^2/((\phi_A^\mathsf{H}\phi_A)(\phi_B^\mathsf{H}\phi_B))`
  über die zugeordneten Punkte (3D: X, Y, Z je Punkt hintereinander), Auto-MAC je Messung.
  Eine Schwelle wird nicht festgelegt.
- Drift (4.5): lineare Regression :math:`f_{r,p} = b_0 + b_1 t_p` mit Standardfehler aus der
  Streuung um die Gerade; ``drift_signifikant`` bei :math:`|b_1| > 3\sigma_{b_1}`.

Zwischen Linien wird nicht interpoliert. Haben A und B verschiedene Frequenzachsen, werden
nur Spitzen verglichen.
"""

from __future__ import annotations

import dataclasses
import math
from collections.abc import Sequence
from dataclasses import dataclass
from typing import Literal

import numpy as np
import numpy.typing as npt

from .annahmen import AnnahmenStufe2, Bandregel, SchwellenStufe2
from .baender import band_linien
from .daten import ComplexArray, FloatArray, IntArray, Punkte, bereite_paar
from .frf import berechne_frf
from .gesamt import KOMPONENTEN_3D, Auswertung
from .modenfit import (
    MODELL_PASST_NICHT,
    NICHT_KONVERGIERT,
    ModenErgebnis,
    ModenfitErgebnis,
    Zusammenfassung,
    schaetze_daempfung,
)

PASSPUNKTE_UNGENAU = "passpunkte_ungenau"
SIGNIFIKANT = "signifikant"
DRIFT_SIGNIFIKANT = "drift_signifikant"

HINWEIS_ACHSEN = "Achsen verschieden: nur Spitzenpaarung (kein FRF-Vergleich, kein MAC)"
HINWEIS_KEINE_ZUORDNUNG = "keine zugeordneten Punkte: MAC und FRF-Vergleich NaN"
HINWEIS_WENIG_LINIEN = "weniger als {n} gemeinsame Linien im Band: frac, pegel_db, diff_rel NaN"
HINWEIS_NULL_FRF = "‖H^A‖ = 0 oder ‖H^B‖ = 0 im Band: frac, pegel_db bzw. diff_rel NaN"
HINWEIS_OHNE_PHASE = "ohne gültige Phase ist der MAC nicht definiert (NaN)"
HINWEIS_MAC_1D = (
    "MAC aus 1D-Amplituden des Paars (X, Y, Z nicht vollständig): Komponenten nicht gedreht"
)
HINWEIS_MAC_SCHWELLE = (
    "MAC ohne Schwelle; Polytec nennt im Beispiel < 0,9 verschieden, > 0,9 ähnlich (SM 9-38)"
)
HINWEIS_DRIFT_WENIG = "Drift nicht prüfbar: weniger als {n} brauchbare Punkte"
HINWEIS_DRIFT_ZEIT = "Drift nicht prüfbar: alle Punkte zur selben Zeit"
HINWEIS_UNGUELTIG = "ungültige Punkte (M6) aus FRF-Vergleich, MAC und Auto-MAC ausgeschlossen: {n}"

Quelle = Literal["cph", "h1"]
"""Quelle der Amplituden für MAC (FG-02 3.6): CPH (Voreinstellung) oder H1."""

PasspunktArt = Literal["label", "index"]


def mac(phi_a: npt.ArrayLike, phi_b: npt.ArrayLike) -> float:
    r"""Modal Assurance Criterion zweier komplexer Vektoren (FG-03 4.4).

    Beide Felder werden flach gelegt (3D: Form ``(P, 3)`` → X, Y, Z je Punkt
    hintereinander). Unabhängig von einem komplexen Faktor; 1 für gleiche Form, 0 für
    orthogonale Vektoren. Ein Nullvektor ergibt NaN (FG-03 6.3).

    Raises
    ------
    ValueError
        Bei verschiedener Länge.
    """
    a = np.ravel(np.asarray(phi_a, dtype=np.complex128))
    b = np.ravel(np.asarray(phi_b, dtype=np.complex128))
    if a.shape != b.shape:
        raise ValueError(f"MAC: Längen {a.shape} und {b.shape} verschieden")
    na = float(np.vdot(a, a).real)
    nb = float(np.vdot(b, b).real)
    if not (na > 0 and nb > 0):
        return math.nan
    return float(abs(np.vdot(a, b)) ** 2 / (na * nb))


def auto_mac(formen: Sequence[npt.ArrayLike]) -> FloatArray:
    """Auto-MAC-Matrix ``(S, S)`` der Formen einer Messung (FG-03 4.4)."""
    s = len(formen)
    matrix = np.full((s, s), np.nan)
    for i in range(s):
        for j in range(i, s):
            matrix[i, j] = matrix[j, i] = mac(formen[i], formen[j])
    return matrix


@dataclass(frozen=True, kw_only=True, eq=False)
class Transformation:
    r"""Starre Transformation :math:`x_B = R\,x_A + t` (FG-03 4.1).

    Attributes
    ----------
    drehung : numpy.ndarray
        :math:`R`, ``(3, 3)``.
    verschiebung_m : numpy.ndarray
        :math:`t` in m, ``(3,)``.
    rms_m : float
        RMS-Restabstand der Passpunkte in m.
    n_passpunkte : int
        Anzahl der Passpunkte.
    """

    drehung: FloatArray
    verschiebung_m: FloatArray
    rms_m: float
    n_passpunkte: int


def kabsch(
    x_a_m: npt.ArrayLike, x_b_m: npt.ArrayLike, *, kollinear_min: float = 1e-6
) -> Transformation:
    r"""Starre Transformation aus Passpunkten nach Kabsch (FG-03 4.1, [A]).

    Parameters
    ----------
    x_a_m, x_b_m : array_like
        Passpunkte ``(N, 3)`` in m, zeilenweise einander zugeordnet.
    kollinear_min : float
        Kollinear bei :math:`\sigma_2/\sigma_1 <` ``kollinear_min`` der Matrix H.

    Raises
    ------
    ValueError
        Bei weniger als drei Passpunkten oder kollinearen Passpunkten (FG-03 6.3).
    """
    a = np.asarray(x_a_m, dtype=np.float64)
    b = np.asarray(x_b_m, dtype=np.float64)
    if a.ndim != 2 or a.shape[1] != 3 or b.shape != a.shape:
        raise ValueError(f"Passpunkte (N, 3) erwartet: {a.shape}, {b.shape}")
    if a.shape[0] < 3:
        raise ValueError(f"mindestens drei Passpunkte nötig, erhalten {a.shape[0]}")
    if not (np.all(np.isfinite(a)) and np.all(np.isfinite(b))):
        raise ValueError("Passpunkte müssen endlich sein")
    ca = a.mean(axis=0)
    cb = b.mean(axis=0)
    h = (a - ca).T @ (b - cb)
    u, sigma, vt = np.linalg.svd(h)
    if not (sigma[0] > 0 and sigma[1] / sigma[0] >= kollinear_min):
        verhaeltnis = sigma[1] / sigma[0] if sigma[0] > 0 else 0.0
        raise ValueError(
            f"Passpunkte kollinear (sigma2/sigma1 = {verhaeltnis:.3g} < {kollinear_min:g})"
        )
    v = vt.T
    d = np.diag([1.0, 1.0, float(np.sign(np.linalg.det(v @ u.T)))])
    r = v @ d @ u.T
    t = cb - r @ ca
    rest = a @ r.T + t - b
    return Transformation(
        drehung=r,
        verschiebung_m=t,
        rms_m=float(np.sqrt(np.mean(np.sum(rest**2, axis=1)))),
        n_passpunkte=int(a.shape[0]),
    )


def drehe_nach_a(v_b: npt.ArrayLike, drehung: npt.ArrayLike) -> ComplexArray:
    r""":math:`v_{B\to A} = R^\mathsf{T} v_B` für Felder ``(..., 3)`` (FG-03 4.1)."""
    v = np.asarray(v_b, dtype=np.complex128)
    r = np.asarray(drehung, dtype=np.float64)
    if v.shape[-1] != 3 or r.shape != (3, 3):
        raise ValueError(f"v (..., 3) und R (3, 3) erwartet: {v.shape}, {r.shape}")
    ergebnis: ComplexArray = v @ r
    return ergebnis


def kleinster_abstand(koordinaten_m: npt.ArrayLike) -> float:
    r"""Kleinster Abstand zweier verschiedener Punkte in m (:math:`d_\mathrm{min}`).

    Raises
    ------
    ValueError
        Bei weniger als zwei Punkten oder lauter gleichen Koordinaten.
    """
    x = np.asarray(koordinaten_m, dtype=np.float64)
    if x.ndim != 2 or x.shape[0] < 2:
        raise ValueError("d_min braucht mindestens zwei Punkte")
    d = np.linalg.norm(x[:, None, :] - x[None, :, :], axis=2)
    positiv = d[np.triu_indices(x.shape[0], k=1)]
    positiv = positiv[positiv > 0]
    if positiv.size == 0:
        raise ValueError("d_min nicht bestimmbar: alle Punkte am selben Ort")
    return float(positiv.min())


@dataclass(frozen=True, kw_only=True, eq=False)
class Zuordnung:
    r"""Punktzuordnung A ↔ B (FG-03 4.1, Datenvertrag 6.2).

    Attributes
    ----------
    variante : {"label", "koordinaten"}
        Verwendete Variante (E4).
    index_a, index_b : numpy.ndarray
        Zugeordnete 0-basierte Punktindizes ``(Z,)``.
    abstand_m : numpy.ndarray
        Abstand :math:`\lVert R x_A + t - x_B\rVert` je Paar in m ``(Z,)``.
    drehung, verschiebung_m : numpy.ndarray
        :math:`R` ``(3, 3)`` und :math:`t` ``(3,)`` in m (ohne Passpunkte: Einheit und 0).
    rms_passpunkte_m : float
        RMS-Restabstand der Passpunkte (NaN ohne Passpunkte).
    d_tol_m : float
        Zuordnungstoleranz (NaN, wenn nicht verwendet).
    ohne_partner_a, ohne_partner_b : tuple of int
        Punktindizes ohne Partner.
    kennzeichen : tuple of str
        ``passpunkte_ungenau``.
    hinweise : tuple of str
        Hinweise.
    """

    variante: str
    index_a: IntArray
    index_b: IntArray
    abstand_m: FloatArray
    drehung: FloatArray
    verschiebung_m: FloatArray
    rms_passpunkte_m: float
    d_tol_m: float
    ohne_partner_a: tuple[int, ...]
    ohne_partner_b: tuple[int, ...]
    kennzeichen: tuple[str, ...]
    hinweise: tuple[str, ...]


def _passpunkt_index(punkte: Punkte, wert: int, art: PasspunktArt, seite: str) -> int:
    if art == "index":
        if not 0 <= wert < punkte.index.shape[0]:
            raise ValueError(f"Passpunkt-Index {wert} in {seite} nicht vorhanden")
        return int(wert)
    treffer = np.flatnonzero(punkte.label == wert)
    if treffer.size != 1:
        raise ValueError(f"Passpunkt-Label {wert} in {seite} nicht eindeutig vorhanden")
    return int(treffer[0])


def ordne_punkte(
    punkte_a: Punkte,
    punkte_b: Punkte,
    *,
    variante: Literal["label", "koordinaten"] = "label",
    passpunkte: Sequence[tuple[int, int]] | None = None,
    passpunkt_art: PasspunktArt = "label",
    schwellen2: SchwellenStufe2 | None = None,
) -> Zuordnung:
    r"""Ordnet die Punkte von A und B einander zu (FG-03 4.1, E4).

    Parameters
    ----------
    punkte_a, punkte_b : Punkte
        Messpunkte von A und B.
    variante : {"label", "koordinaten"}
        ``"label"``: gleiche Labels; ``"koordinaten"``: gegenseitig nächste Nachbarn nach der
        Transformation innerhalb :math:`d_\mathrm{tol}`.
    passpunkte : sequence of tuple of int, optional
        Paare (A, B) als Labels bzw. Indizes für die starre Transformation; auch bei der
        Variante ``"label"`` erlaubt (dann nur für das Drehen der Komponenten und die
        Abstände).
    passpunkt_art : {"label", "index"}
        Bedeutung der Passpunktangaben.
    schwellen2 : SchwellenStufe2, optional
        :math:`d_\mathrm{tol}`-Faktor und Kollinearitätsgrenze.

    Raises
    ------
    ValueError
        Bei weniger als drei bzw. kollinearen Passpunkten, unbekannten Passpunkten, nicht
        bestimmbarem :math:`d_\mathrm{min}` oder doppelten Labels (Variante ``"label"``).
    """
    schwellen2 = schwellen2 if schwellen2 is not None else SchwellenStufe2()
    if variante not in ("label", "koordinaten"):
        raise ValueError(f"unbekannte Zuordnungsvariante {variante!r}")
    xa = punkte_a.koordinaten_m
    xb = punkte_b.koordinaten_m
    hinweise: list[str] = []
    kennzeichen: list[str] = []
    r = np.eye(3)
    t = np.zeros(3)
    rms = math.nan
    if passpunkte is not None:
        ia = [_passpunkt_index(punkte_a, int(p[0]), passpunkt_art, "A") for p in passpunkte]
        ib = [_passpunkt_index(punkte_b, int(p[1]), passpunkt_art, "B") for p in passpunkte]
        trafo = kabsch(xa[ia], xb[ib], kollinear_min=schwellen2.kollinear_min)
        r, t, rms = trafo.drehung, trafo.verschiebung_m, trafo.rms_m
    d_tol = math.nan
    if variante == "koordinaten" or passpunkte is not None:
        d_tol = schwellen2.d_tol_faktor * kleinster_abstand(xa)
        if passpunkte is not None and rms > d_tol / 2.0:
            kennzeichen.append(PASSPUNKTE_UNGENAU)
    xa_in_b = xa @ r.T + t
    if variante == "label":
        for name, pk in (("A", punkte_a), ("B", punkte_b)):
            werte, anzahl = np.unique(pk.label, return_counts=True)
            if np.any(anzahl > 1):
                raise ValueError(
                    f"doppelte Labels in {name}: {werte[anzahl > 1].tolist()} "
                    "(Zuordnung über Label nicht eindeutig)"
                )
        paare_a: list[int] = []
        paare_b: list[int] = []
        b_nach_label = {int(lb): i for i, lb in enumerate(punkte_b.label)}
        for i, lb in enumerate(punkte_a.label):
            j = b_nach_label.get(int(lb))
            if j is not None:
                paare_a.append(i)
                paare_b.append(j)
    else:
        abstand = np.linalg.norm(xa_in_b[:, None, :] - xb[None, :, :], axis=2)
        nn_a = np.argmin(abstand, axis=1)
        nn_b = np.argmin(abstand, axis=0)
        paare_a = [
            i for i in range(xa.shape[0]) if nn_b[nn_a[i]] == i and abstand[i, nn_a[i]] <= d_tol
        ]
        paare_b = [int(nn_a[i]) for i in paare_a]
    index_a = np.asarray(paare_a, dtype=np.int64)
    index_b = np.asarray(paare_b, dtype=np.int64)
    if index_a.size == 0:
        hinweise.append(HINWEIS_KEINE_ZUORDNUNG)
    abstand_paare = (
        np.linalg.norm(xa_in_b[index_a] - xb[index_b], axis=1) if index_a.size else (np.zeros(0))
    )
    return Zuordnung(
        variante=variante,
        index_a=index_a,
        index_b=index_b,
        abstand_m=abstand_paare.astype(np.float64),
        drehung=r,
        verschiebung_m=t,
        rms_passpunkte_m=rms,
        d_tol_m=d_tol,
        ohne_partner_a=tuple(sorted(set(range(xa.shape[0])) - set(paare_a))),
        ohne_partner_b=tuple(sorted(set(range(xb.shape[0])) - set(paare_b))),
        kennzeichen=tuple(kennzeichen),
        hinweise=tuple(hinweise),
    )


@dataclass(frozen=True, kw_only=True)
class SpitzenPaar:
    r"""Ein Spitzenpaar A/B (FG-03 4.2).

    Attributes
    ----------
    index_a, index_b : int
        Indizes der Spitzen in A und B.
    f_a_hz, f_b_hz : float
        Spitzenfrequenzen (B-1-Median, falls vorhanden, sonst Stufe 1).
    delta_f_hz, delta_f_rel : float
        :math:`f^B - f^A` in Hz und :math:`\Delta f/f^A`.
    delta_zeta : float
        :math:`\zeta^B - \zeta^A` (NaN ohne B-1).
    sigma_hz : float
        :math:`\sqrt{\sigma_A^2 + \sigma_B^2}` in Hz.
    signifikant : bool
        :math:`|\Delta f| > 2\sigma`.
    """

    index_a: int
    index_b: int
    f_a_hz: float
    f_b_hz: float
    delta_f_hz: float
    delta_f_rel: float
    delta_zeta: float
    sigma_hz: float
    signifikant: bool


@dataclass(frozen=True, kw_only=True)
class Spitzenpaarung:
    r"""Ergebnis der Spitzenpaarung (FG-03 4.2).

    Attributes
    ----------
    paare : tuple of SpitzenPaar
        Gegenseitig nächste Paare innerhalb :math:`\Delta f_\mathrm{tol}`.
    ohne_partner_a, ohne_partner_b : tuple of int
        Spitzen ohne Partner.
    df_tol_hz : float
        Verwendete Toleranz.
    """

    paare: tuple[SpitzenPaar, ...]
    ohne_partner_a: tuple[int, ...]
    ohne_partner_b: tuple[int, ...]
    df_tol_hz: float


def _optional(werte: npt.ArrayLike | None, anzahl: int) -> FloatArray:
    if werte is None:
        return np.full(anzahl, np.nan)
    feld = np.asarray(werte, dtype=np.float64)
    if feld.shape != (anzahl,):
        raise ValueError(f"Feld {feld.shape} passt nicht zu ({anzahl},)")
    return feld


def paare_spitzen(
    f_a_hz: npt.ArrayLike,
    f_b_hz: npt.ArrayLike,
    df_tol_hz: float,
    *,
    sd_a_hz: npt.ArrayLike | None = None,
    sd_b_hz: npt.ArrayLike | None = None,
    zeta_a: npt.ArrayLike | None = None,
    zeta_b: npt.ArrayLike | None = None,
    sigma_ohne_b1_hz: float = math.nan,
    signifikanz_faktor: float = 2.0,
) -> Spitzenpaarung:
    r"""Paart Spitzen als gegenseitig nächste Nachbarn (FG-03 4.2).

    Parameters
    ----------
    f_a_hz, f_b_hz : array_like
        Spitzenfrequenzen ``(S_A,)``, ``(S_B,)`` in Hz.
    df_tol_hz : float
        :math:`\Delta f_\mathrm{tol}` in Hz.
    sd_a_hz, sd_b_hz : array_like, optional
        Fit-Standardabweichungen aus B-1; nicht endliche Werte werden durch
        ``sigma_ohne_b1_hz`` ersetzt.
    zeta_a, zeta_b : array_like, optional
        ζ aus B-1 für :math:`\Delta\zeta`.
    sigma_ohne_b1_hz : float
        Unsicherheit ohne B-1 (0,0508 Δf, FG-02 3.9).
    signifikanz_faktor : float
        Faktor der Signifikanzgrenze (2).
    """
    fa = np.asarray(f_a_hz, dtype=np.float64)
    fb = np.asarray(f_b_hz, dtype=np.float64)
    sa = _optional(sd_a_hz, fa.shape[0])
    sb = _optional(sd_b_hz, fb.shape[0])
    sa = np.where(np.isfinite(sa), sa, sigma_ohne_b1_hz)
    sb = np.where(np.isfinite(sb), sb, sigma_ohne_b1_hz)
    za = _optional(zeta_a, fa.shape[0])
    zb = _optional(zeta_b, fb.shape[0])
    paare: list[SpitzenPaar] = []
    if fa.size and fb.size:
        for i, x in enumerate(fa):
            j = int(np.argmin(np.abs(fb - x)))
            if abs(fb[j] - x) <= df_tol_hz and int(np.argmin(np.abs(fa - fb[j]))) == i:
                df = float(fb[j] - x)
                sigma = float(math.hypot(sa[i], sb[j]))
                paare.append(
                    SpitzenPaar(
                        index_a=i,
                        index_b=j,
                        f_a_hz=float(x),
                        f_b_hz=float(fb[j]),
                        delta_f_hz=df,
                        delta_f_rel=df / float(x),
                        delta_zeta=float(zb[j] - za[i]),
                        sigma_hz=sigma,
                        signifikant=bool(abs(df) > signifikanz_faktor * sigma),
                    )
                )
    return Spitzenpaarung(
        paare=tuple(paare),
        ohne_partner_a=tuple(sorted(set(range(fa.shape[0])) - {p.index_a for p in paare})),
        ohne_partner_b=tuple(sorted(set(range(fb.shape[0])) - {p.index_b for p in paare})),
        df_tol_hz=float(df_tol_hz),
    )


@dataclass(frozen=True, kw_only=True, eq=False)
class FrfVergleich:
    """FRF-Vergleich je Punkt in einem Band (FG-03 4.3, Datenvertrag 6.2).

    Attributes
    ----------
    f_u_hz, f_o_hz : float
        Bandgrenzen.
    frac, pegel_db, diff_rel : numpy.ndarray
        ``(Z,)``; Einheiten 1, dB, 1.
    n_linien : numpy.ndarray
        Gemeinsame Linien je Punkt ``(Z,)``.
    hinweise : tuple of str
        Hinweise.
    """

    f_u_hz: float
    f_o_hz: float
    frac: FloatArray
    pegel_db: FloatArray
    diff_rel: FloatArray
    n_linien: IntArray
    hinweise: tuple[str, ...]


def vergleiche_frf(
    h_a: npt.ArrayLike,
    h_b: npt.ArrayLike,
    frequenz_hz: FloatArray,
    f_u_hz: float,
    f_o_hz: float,
    *,
    maske_a: npt.ArrayLike | None = None,
    maske_b: npt.ArrayLike | None = None,
    delta_f_hz: float | None = None,
    regel: Bandregel = "geschlossen",
    min_linien: int = 3,
) -> FrfVergleich:
    """``frac``, ``pegel_db`` und ``diff_rel`` je Zeile über ein Band (FG-03 4.3).

    Parameters
    ----------
    h_a, h_b : array_like
        FRF ``(Z, K)`` oder ``(K,)`` der zugeordneten Punkte von A und B.
    frequenz_hz : numpy.ndarray
        Gemeinsame Achse ``(K,)``.
    f_u_hz, f_o_hz : float
        Bandgrenzen (Bandregel FG-02 3.8, M10).
    maske_a, maske_b : array_like, optional
        Kohärenzmasken ``γ² >= γ²_min`` in der Form von ``h_a`` bzw. ``h_b``.
    min_linien : int
        Mindestzahl gemeinsamer Linien (3); darunter NaN mit Hinweis.
    """
    a = np.atleast_2d(np.asarray(h_a, dtype=np.complex128))
    b = np.atleast_2d(np.asarray(h_b, dtype=np.complex128))
    if a.shape != b.shape or a.shape[1] != frequenz_hz.shape[0]:
        raise ValueError(f"h_a {a.shape}, h_b {b.shape} passen nicht zur Achse")
    ma = np.ones(a.shape, dtype=bool) if maske_a is None else np.atleast_2d(maske_a)
    mb = np.ones(b.shape, dtype=bool) if maske_b is None else np.atleast_2d(maske_b)
    band, band_hinweise = band_linien(
        frequenz_hz, f_u_hz, f_o_hz, delta_f_hz=delta_f_hz, regel=regel
    )
    z = a.shape[0]
    frac = np.full(z, np.nan)
    pegel = np.full(z, np.nan)
    diff = np.full(z, np.nan)
    anzahl = np.zeros(z, dtype=np.int64)
    hinweise: list[str] = list(band_hinweise)
    for i in range(z):
        m = band & ma[i] & mb[i] & np.isfinite(a[i]) & np.isfinite(b[i])
        anzahl[i] = int(np.count_nonzero(m))
        if anzahl[i] < min_linien:
            continue
        ha = a[i, m]
        hb = b[i, m]
        ea = float(np.sum(np.abs(ha) ** 2))
        eb = float(np.sum(np.abs(hb) ** 2))
        if ea > 0 and eb > 0:
            frac[i] = abs(np.vdot(ha, hb)) ** 2 / (ea * eb)
            pegel[i] = 10.0 * math.log10(eb / ea)
        if ea > 0:
            diff[i] = float(np.linalg.norm(hb - ha) / math.sqrt(ea))
    if np.any(anzahl < min_linien):
        hinweise.append(HINWEIS_WENIG_LINIEN.format(n=min_linien))
    gefuellt = anzahl >= min_linien
    if np.any(gefuellt & (np.isnan(frac) | np.isnan(diff))):
        hinweise.append(HINWEIS_NULL_FRF)
    return FrfVergleich(
        f_u_hz=float(f_u_hz),
        f_o_hz=float(f_o_hz),
        frac=frac,
        pegel_db=pegel,
        diff_rel=diff,
        n_linien=anzahl,
        hinweise=tuple(dict.fromkeys(hinweise)),
    )


def achsen_gleich(
    f_a_hz: FloatArray, f_b_hz: FloatArray, delta_f_hz: float, rtol: float = 1e-6
) -> bool:
    r"""Gleiche Linien und :math:`|f^A_k - f^B_k| \le \mathrm{rtol}\cdot\Delta f` (wie P-06)."""
    return bool(
        f_a_hz.shape == f_b_hz.shape and np.all(np.abs(f_a_hz - f_b_hz) <= rtol * delta_f_hz)
    )


def amplituden(
    auswertung: Auswertung,
    paar: tuple[str, str],
    annahmen2: AnnahmenStufe2,
    *,
    quelle: Quelle = "cph",
    nur_1d: bool = False,
) -> tuple[ComplexArray, bool]:
    """Komplexe Amplituden ``(P, c, K)`` für MAC und Normalenbezug (FG-02 3.6, FG-03 4.4).

    Mit allen Komponenten X, Y, Z (Kreuzspektren zur Referenz des Paars) ist c = 3: CPH bzw.
    H1 (``quelle``) mit :math:`s_a s_b` und Konjugation, in das Geometrie-KS gedreht
    (:math:`D v`, M12). Sonst oder mit ``nur_1d`` ist c = 1: CPH bzw. H1 des Paars.

    Returns
    -------
    amplitude : numpy.ndarray
        ``(P, c, K)`` complex.
    ist_3d : bool
        ``True`` bei c = 3.
    """
    if quelle not in ("cph", "h1"):
        raise ValueError(f"unbekannte Quelle {quelle!r}")
    daten = auswertung.daten
    referenz = paar[1]
    if not nur_1d and all((k, referenz) in daten.cp for k in KOMPONENTEN_3D):
        felder = []
        for k in KOMPONENTEN_3D:
            pd = bereite_paar(daten, k, referenz, auswertung.annahmen)
            felder.append(berechne_frf(pd, auswertung.schwellen).h1 if quelle == "h1" else pd.cph)
        gedreht: ComplexArray = np.einsum("ij,pjk->pik", annahmen2.drehung, np.stack(felder, 1))
        return gedreht, True
    pa = auswertung.paare[paar]
    feld = pa.frf.h1 if quelle == "h1" else pa.paar.cph
    return feld[:, None, :], False


@dataclass(frozen=True, kw_only=True, eq=False)
class Drift:
    r"""Frequenzdrift innerhalb einer Messung (FG-03 4.5, Datenvertrag 6.2).

    Attributes
    ----------
    f_spitze_hz : float
        Stufe-1-Frequenz der ausgewählten Spitze.
    paar : str
        Datengrundlage (Paar und Auswahl).
    steigung_hz_h, sd_steigung_hz_h : float
        :math:`b_1` und :math:`\sigma_{b_1}` in Hz/h.
    achsenabschnitt_hz : float
        :math:`b_0` in Hz (bei :math:`t = 0`, erster Punkt).
    gesamt_hz, gesamt_rel : float
        :math:`b_1(t_\mathrm{max} - t_\mathrm{min})` in Hz und relativ zu :math:`b_0`.
    streuung_hz : float
        Standardabweichung um die Gerade in Hz.
    signifikant : bool
        ``drift_signifikant``.
    n_punkte : int
        Brauchbare Punkte.
    pruefbar : bool
        ``False`` bei weniger als ``drift_min_punkte`` Punkten oder gleicher Zeit.
    dauer_s : float
        :math:`t_\mathrm{max} - t_\mathrm{min}` in s.
    hinweise : tuple of str
        Hinweise.
    n_modell_passt_nicht : int
        Anzahl der verwendeten Punkte mit ``modell_passt_nicht`` (FG-03 4.5, K2-1).
    """

    f_spitze_hz: float
    paar: str
    steigung_hz_h: float
    sd_steigung_hz_h: float
    achsenabschnitt_hz: float
    gesamt_hz: float
    gesamt_rel: float
    streuung_hz: float
    signifikant: bool
    n_punkte: int
    pruefbar: bool
    dauer_s: float
    hinweise: tuple[str, ...]
    n_modell_passt_nicht: int = 0


def drift_regression(
    fr_hz: npt.ArrayLike,
    zeit_s: npt.ArrayLike,
    *,
    min_punkte: int = 10,
    faktor: float = 3.0,
    f_spitze_hz: float = math.nan,
    paar: str = "",
) -> Drift:
    r"""Lineare Regression :math:`f_r = b_0 + b_1 t` (FG-03 4.5).

    :math:`\sigma_{b_1} = s/\sqrt{\sum (t - \bar t)^2}` mit
    :math:`s^2 = \sum e_p^2/(N - 2)` aus der Streuung um die Gerade. Nicht endliche Werte
    entfallen. Die Zeit wird auf den ersten (frühesten) Punkt bezogen.
    """
    f = np.asarray(fr_hz, dtype=np.float64)
    t = np.asarray(zeit_s, dtype=np.float64)
    if f.shape != t.shape or f.ndim != 1:
        raise ValueError(f"fr_hz {f.shape} und zeit_s {t.shape} müssen (N,) sein")
    ok = np.isfinite(f) & np.isfinite(t)
    f = f[ok]
    t = t[ok]
    n = int(f.shape[0])
    nan = math.nan
    leer = Drift(
        f_spitze_hz=f_spitze_hz,
        paar=paar,
        steigung_hz_h=nan,
        sd_steigung_hz_h=nan,
        achsenabschnitt_hz=nan,
        gesamt_hz=nan,
        gesamt_rel=nan,
        streuung_hz=nan,
        signifikant=False,
        n_punkte=n,
        pruefbar=False,
        dauer_s=float(t.max() - t.min()) if n else nan,
        hinweise=(HINWEIS_DRIFT_WENIG.format(n=min_punkte),),
    )
    if n < min_punkte:
        return leer
    t = t - t.min()
    sxx = float(np.sum((t - t.mean()) ** 2))
    if not sxx > 0:
        return Drift(**{**leer.__dict__, "hinweise": (HINWEIS_DRIFT_ZEIT,)})
    matrix = np.column_stack([t, np.ones_like(t)])
    (b1, b0), *_ = np.linalg.lstsq(matrix, f, rcond=None)
    rest = f - (b0 + b1 * t)
    s = math.sqrt(float(rest @ rest) / (n - 2))
    sd_b1 = s / math.sqrt(sxx)
    dauer = float(t.max())
    return Drift(
        f_spitze_hz=f_spitze_hz,
        paar=paar,
        steigung_hz_h=float(b1) * 3600.0,
        sd_steigung_hz_h=sd_b1 * 3600.0,
        achsenabschnitt_hz=float(b0),
        gesamt_hz=float(b1) * dauer,
        gesamt_rel=float(b1) * dauer / float(b0),
        streuung_hz=s,
        signifikant=bool(abs(b1) > faktor * sd_b1),
        n_punkte=n,
        pruefbar=True,
        dauer_s=dauer,
        hinweise=(),
    )


def drift_aus(
    auswertung: Auswertung,
    zeit_s: npt.ArrayLike,
    f_spitze_hz: float,
    paar: tuple[str, str],
    *,
    antriebspunkt: bool = True,
    schwellen2: SchwellenStufe2 | None = None,
) -> tuple[Drift, ModenfitErgebnis]:
    r"""Drift einer Spitze über die Messzeit mit B-1 je Punkt (FG-03 4.5).

    Parameters
    ----------
    auswertung : Auswertung
        Stufe-1-Auswertung.
    zeit_s : array_like
        Zeit je Punkt ``(P,)`` in s (M15, nur Differenzen).
    f_spitze_hz : float
        Frequenz der Spitze; gewählt wird die nächste Stufe-1-Spitze des Paars.
    paar : tuple of str
        Datengrundlage, z. B. das Antriebspunkt-Paar ``("Ref2", "Ref1")``.
    antriebspunkt : bool
        ``True``: alle gültigen Punkte (das Paar misst an jedem Punkt dasselbe). ``False``:
        nur Punkte mit :math:`|H_1| \ge 0{,}3\max` an der Spitzenlinie.
    schwellen2 : SchwellenStufe2, optional
        Parameter; Punktausschluss nach :func:`drift_verwendbar`.

    Returns
    -------
    drift : Drift
    fit : ModenfitErgebnis
        B-1 an den verwendeten Punkten.

    Raises
    ------
    ValueError
        Bei falscher Länge von ``zeit_s`` oder ohne Stufe-1-Spitzen im Paar.
    """
    schwellen2 = schwellen2 if schwellen2 is not None else SchwellenStufe2()
    t = np.asarray(zeit_s, dtype=np.float64)
    p_anzahl = auswertung.daten.anzahl_punkte
    if t.shape != (p_anzahl,):
        raise ValueError(f"zeit_s hat Form {t.shape}, erwartet ({p_anzahl},)")
    if paar not in auswertung.paare:
        raise KeyError(f"kein Kanalpaar {paar[0]}/{paar[1]} in der Auswertung")
    pa = auswertung.paare[paar]
    spitzen = pa.spitzen.spitzen
    if not spitzen:
        raise ValueError(f"keine Stufe-1-Spitzen im Paar {paar[0]}/{paar[1]}")
    i = int(np.argmin([abs(s.f_sp_hz - f_spitze_hz) for s in spitzen]))
    gueltig = pa.paar.gueltig
    if antriebspunkt:
        punkte = np.flatnonzero(gueltig)
        grundlage = f"{paar[0]}/{paar[1]} (Antriebspunkt-Paar, alle gültigen Punkte)"
    else:
        betrag = np.abs(pa.frf.h1[:, spitzen[i].k])
        grenze = schwellen2.drift_anteil * float(np.nanmax(np.where(gueltig, betrag, np.nan)))
        punkte = np.flatnonzero(gueltig & (betrag >= grenze))
        grundlage = f"{paar[0]}/{paar[1]} (|H1| >= {schwellen2.drift_anteil:g}·max)"
    fit = schaetze_daempfung(
        auswertung, paar, schwellen2=schwellen2, spitzen=[i], punkte=[int(p) for p in punkte]
    )
    gruppe = next(g for g in fit.gruppen if i in g.spitzen)
    drift = drift_aus_ergebnissen(
        fit.ergebnisse,
        gruppe.spitzen.index(i),
        t,
        schwellen2=schwellen2,
        f_spitze_hz=spitzen[i].f_sp_hz,
        paar=grundlage,
    )
    return drift, fit


def drift_verwendbar(e: ModenErgebnis, mode: int, schwellen2: SchwellenStufe2) -> bool:
    """Punktausschluss der Drift je gewählter Mode (FG-03 4.5, K2-1 Option A).

    Ausgeschlossen: Punkte ohne Fit; Kennzeichen der gewählten Mode aus
    ``drift_ausschluss`` (Voreinstellung ``ausserhalb_band``, ``unsicher``,
    ``moden_vertauscht``); ``nicht_konvergiert`` nur bei n = 1
    (``drift_nicht_konvergiert_einzelmode``). Nicht ausgeschlossen: ``modell_passt_nicht``,
    ``gueltigkeit_offen_m7``, ``kohaerenz_niedrig``, ``kein_mobilitaetsbezug``.
    """
    if not e.gefittet:
        return False
    k = set(e.kennzeichen[mode])
    if k & set(schwellen2.drift_ausschluss):
        return False
    return not (
        schwellen2.drift_nicht_konvergiert_einzelmode and e.n_moden == 1 and NICHT_KONVERGIERT in k
    )


def drift_aus_ergebnissen(
    ergebnisse: Sequence[ModenErgebnis],
    mode: int,
    zeit_s: npt.ArrayLike,
    *,
    schwellen2: SchwellenStufe2 | None = None,
    f_spitze_hz: float = math.nan,
    paar: str = "",
) -> Drift:
    """Drift aus vorgegebenen B-1-Ergebnissen je Punkt (FG-03 4.5, RF-V6).

    Parameters
    ----------
    ergebnisse : sequence of ModenErgebnis
        Ergebnisse einer Gruppe je Punkt (``punkt`` indiziert ``zeit_s``).
    mode : int
        Index der gewählten Mode in der Gruppe.
    zeit_s : array_like
        Zeit je Punkt ``(P,)`` in s.
    """
    schwellen2 = schwellen2 if schwellen2 is not None else SchwellenStufe2()
    t = np.asarray(zeit_s, dtype=np.float64)
    fr = np.full(t.shape[0], np.nan)
    n_mpn = 0
    for e in ergebnisse:
        if drift_verwendbar(e, mode, schwellen2):
            fr[e.punkt] = e.fr_hz[mode]
            n_mpn += MODELL_PASST_NICHT in e.kennzeichen[mode]
    drift = drift_regression(
        fr,
        t,
        min_punkte=schwellen2.drift_min_punkte,
        faktor=schwellen2.drift_faktor,
        f_spitze_hz=f_spitze_hz,
        paar=paar,
    )
    return dataclasses.replace(drift, n_modell_passt_nicht=n_mpn)


@dataclass(frozen=True, kw_only=True, eq=False)
class Vergleich:
    """B-5-Vergleich zweier Messungen (FG-03 4, Datenvertrag 6.2).

    Attributes
    ----------
    paar : tuple of str
        Kanalpaar.
    achsen_gleich : bool
        Gleiche Frequenzachsen (sonst nur Spitzenpaarung).
    zuordnung : Zuordnung
        Punktzuordnung.
    spitzen : Spitzenpaarung
        Spitzenpaare.
    frf : tuple of FrfVergleich
        Je Band (leer bei verschiedenen Achsen).
    mac : numpy.ndarray
        MAC je Spitzenpaar ``(N_paare,)``.
    mac_3d : bool
        MAC aus X, Y, Z (sonst 1D).
    auto_mac_a, auto_mac_b : numpy.ndarray
        Auto-MAC über die Spitzen je Messung (alle Punkte).
    hinweise : tuple of str
        Hinweise.
    """

    paar: tuple[str, str]
    achsen_gleich: bool
    zuordnung: Zuordnung
    spitzen: Spitzenpaarung
    frf: tuple[FrfVergleich, ...]
    mac: FloatArray
    mac_3d: bool
    auto_mac_a: FloatArray
    auto_mac_b: FloatArray
    hinweise: tuple[str, ...]


def _b1_werte(
    b1: ModenfitErgebnis | None, anzahl: int, f_sp: Sequence[float]
) -> tuple[FloatArray, FloatArray, FloatArray]:
    f = np.asarray(f_sp, dtype=np.float64)
    sd = np.full(anzahl, np.nan)
    zeta = np.full(anzahl, np.nan)
    if b1 is not None:
        je_spitze: dict[int, Zusammenfassung] = {z.spitze: z for z in b1.zusammenfassung}
        for i, z in je_spitze.items():
            if i < anzahl and math.isfinite(z.fr_median_hz):
                f[i] = z.fr_median_hz
                sd[i] = z.sd_fr_median_hz
                zeta[i] = z.zeta_median
    return f, sd, zeta


def vergleiche_messungen(
    a: Auswertung,
    b: Auswertung,
    paar: tuple[str, str],
    *,
    baender: Sequence[tuple[float, float]] = (),
    b1_a: ModenfitErgebnis | None = None,
    b1_b: ModenfitErgebnis | None = None,
    passpunkte: Sequence[tuple[int, int]] | None = None,
    passpunkt_art: PasspunktArt = "label",
    annahmen2: AnnahmenStufe2 | None = None,
    schwellen2: SchwellenStufe2 | None = None,
    quelle: Quelle = "cph",
) -> Vergleich:
    """Vergleicht zwei Stufe-1-Auswertungen A (Bezug) und B (FG-03 4.1 bis 4.4).

    Parameters
    ----------
    a, b : Auswertung
        Stufe-1-Auswertungen mit dem Kanalpaar ``paar``.
    paar : tuple of str
        Kanalpaar.
    baender : sequence of tuple of float
        Bänder des FRF-Vergleichs in Hz.
    b1_a, b1_b : ModenfitErgebnis, optional
        B-1-Ergebnisse des Paars; dann Spitzenpaarung mit B-1-Medianen, Δζ und
        Fit-Standardabweichungen (Median über die verwendeten Punkte).
    passpunkte, passpunkt_art
        Passpunkte für die starre Transformation (4.1).
    annahmen2 : AnnahmenStufe2, optional
        M12 (Drehung der Komponenten in das Geometrie-KS).
    schwellen2 : SchwellenStufe2, optional
        Zuordnungsvariante, Toleranzen.
    quelle : {"cph", "h1"}
        Amplituden der MAC-Formen (wie die Schwingform, FG-02 3.6).

    Notes
    -----
    Ungültige Punkte (M6) gehen weder in den FRF-Vergleich noch in MAC und Auto-MAC ein
    (Hinweis); die Zuordnung selbst listet alle Punkte.

    Raises
    ------
    KeyError
        Wenn das Paar in A oder B fehlt.
    """
    annahmen2 = annahmen2 if annahmen2 is not None else AnnahmenStufe2()
    schwellen2 = schwellen2 if schwellen2 is not None else SchwellenStufe2()
    for name, aw in (("A", a), ("B", b)):
        if paar not in aw.paare:
            raise KeyError(f"kein Kanalpaar {paar[0]}/{paar[1]} in {name}")
    pa_a = a.paare[paar]
    pa_b = b.paare[paar]
    df = a.daten.delta_f_hz
    hinweise: list[str] = [HINWEIS_MAC_SCHWELLE]
    zuordnung = ordne_punkte(
        a.daten.punkte,
        b.daten.punkte,
        variante=schwellen2.zuordnung,
        passpunkte=passpunkte,
        passpunkt_art=passpunkt_art,
        schwellen2=schwellen2,
    )
    sp_a = pa_a.spitzen.spitzen
    sp_b = pa_b.spitzen.spitzen
    fa, sda, za = _b1_werte(b1_a, len(sp_a), [s.f_sp_hz for s in sp_a])
    fb, sdb, zb = _b1_werte(b1_b, len(sp_b), [s.f_sp_hz for s in sp_b])
    paarung = paare_spitzen(
        fa,
        fb,
        schwellen2.df_tol_faktor * df,
        sd_a_hz=sda,
        sd_b_hz=sdb,
        zeta_a=za,
        zeta_b=zb,
        sigma_ohne_b1_hz=schwellen2.unsicherheit_ohne_b1_df * df,
        signifikanz_faktor=schwellen2.signifikanz_faktor,
    )
    gleich = achsen_gleich(a.daten.frequenz_hz, b.daten.frequenz_hz, df, schwellen2.achse_rtol)
    frf: list[FrfVergleich] = []
    mac_werte = np.full(len(paarung.paare), np.nan)
    amp_a, ist_3d = amplituden(a, paar, annahmen2, quelle=quelle)
    amp_b, ist_3d_b = amplituden(b, paar, annahmen2, quelle=quelle)
    mac_3d = ist_3d and ist_3d_b
    if not mac_3d:
        hinweise.append(HINWEIS_MAC_1D)
        amp_a, _ = amplituden(a, paar, annahmen2, quelle=quelle, nur_1d=True)
        amp_b, _ = amplituden(b, paar, annahmen2, quelle=quelle, nur_1d=True)
    else:
        amp_b = np.einsum("pjk,ji->pik", amp_b, zuordnung.drehung)  # R^T v_B
    phase = a.daten.phase_gueltig and b.daten.phase_gueltig
    g_a = pa_a.paar.gueltig
    g_b = pa_b.paar.gueltig
    beide = g_a[zuordnung.index_a] & g_b[zuordnung.index_b]
    ungueltig = int(np.count_nonzero(~beide) + np.count_nonzero(~g_a) + np.count_nonzero(~g_b))
    if ungueltig:
        hinweise.append(HINWEIS_UNGUELTIG.format(n=ungueltig))
    if not gleich:
        hinweise.append(HINWEIS_ACHSEN)
    else:
        ia, ib = zuordnung.index_a[beide], zuordnung.index_b[beide]
        for f_u, f_o in baender:
            frf.append(
                vergleiche_frf(
                    pa_a.frf.h1[ia],
                    pa_b.frf.h1[ib],
                    a.daten.frequenz_hz,
                    f_u,
                    f_o,
                    maske_a=pa_a.frf.kohaerenz_ok[ia],
                    maske_b=pa_b.frf.kohaerenz_ok[ib],
                    delta_f_hz=df,
                    regel=a.annahmen.bandregel,
                    min_linien=schwellen2.frac_min_linien,
                )
            )
        if not phase:
            hinweise.append(HINWEIS_OHNE_PHASE)
        elif ia.size:
            for n, sp in enumerate(paarung.paare):
                mac_werte[n] = mac(
                    amp_a[ia, :, sp_a[sp.index_a].k], amp_b[ib, :, sp_b[sp.index_b].k]
                )
    if zuordnung.index_a.size == 0:
        hinweise.append(HINWEIS_KEINE_ZUORDNUNG)
    if phase:
        auto_a = auto_mac([amp_a[g_a, :, s.k] for s in sp_a])
        auto_b = auto_mac([amp_b[g_b, :, s.k] for s in sp_b])
    else:
        auto_a = np.full((len(sp_a), len(sp_a)), np.nan)
        auto_b = np.full((len(sp_b), len(sp_b)), np.nan)
    return Vergleich(
        paar=paar,
        achsen_gleich=gleich,
        zuordnung=zuordnung,
        spitzen=paarung,
        frf=tuple(frf),
        mac=mac_werte,
        mac_3d=mac_3d,
        auto_mac_a=auto_a,
        auto_mac_b=auto_b,
        hinweise=tuple(dict.fromkeys(hinweise)),
    )
