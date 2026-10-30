r"""B-8: 3D-Komponentenbezug zur Oberfläche (FG-03 Abschnitt 5).

- **Elementnormalen** (5.1): Viereck :math:`\tilde n_e = (p_2 - p_0)\times(p_3 - p_1)`,
  Dreieck :math:`\tilde n_e = (p_1 - p_0)\times(p_2 - p_0)`,
  :math:`A_e = \tfrac12\lVert\tilde n_e\rVert` (beim verwundenen Viereck eine mittlere
  Normale, RF-G2). Ausrichtung auf :math:`e_\mathrm{ref}` (M13, Voreinstellung +z):
  :math:`n_e \leftarrow n_e\,\mathrm{sign}(n_e\cdot e_\mathrm{ref})`; Kennzeichen
  ``orientierung_unsicher`` bei :math:`|n_e\cdot e_\mathrm{ref}| < 0{,}1`. Entartete Elemente
  (Fläche < 1e-12·Median) werden ignoriert.
- **Punktnormalen**: :math:`n_p = \sum_e A_e n_e/\lVert\sum_e A_e n_e\rVert`; Punkte ohne
  Element bekommen NaN.
- **Normal- und Tangentialanteil** (5.2): :math:`\hat v_n = n\cdot\hat v`,
  :math:`\hat v_t = \hat v - n\hat v_n`, :math:`\eta = |\hat v_n|^2/\sum_i|\hat v_i|^2`.
- **Bahnellipse** (5.3): :math:`x(\theta) = \mathrm{Re}\{\hat v e^{i\theta}\}`; große Halbachse
  in Richtung :math:`\mathrm{Re}\{\hat v e^{i\theta^\ast}\}` mit
  :math:`\theta^\ast = -\tfrac12\arg\sum_i\hat v_i^2`, Vorzeichen
  :math:`e_\mathrm{max}\cdot e_\mathrm{ref} \ge 0`; Bahnnormale
  :math:`m = \mathrm{Im}\,\hat v\times\mathrm{Re}\,\hat v`, Drehsinn
  :math:`\sigma = \mathrm{sign}(n\cdot m)` (+1 mathematisch positiv um n).

Annahmen: Koordinaten in m im System des 3D-Abgleichs; Komponenten X/Y/Z im selben System
(M12, Drehung :math:`D`); Elementindizes 0-basiert (M14).
"""

from __future__ import annotations

import math
from collections.abc import Sequence
from dataclasses import dataclass

import numpy as np
import numpy.typing as npt

from .annahmen import AnnahmeEintrag, AnnahmenStufe2, SchwellenStufe2
from .daten import BoolArray, ComplexArray, FloatArray
from .schwingform import Schwingform, ellipse_kennwerte

ORIENTIERUNG_UNSICHER = "orientierung_unsicher"

HINWEIS_ENTARTET = "entartete Elemente ignoriert (Fläche < {f:g}·Median): {liste}"
HINWEIS_ORIENTIERUNG = "orientierung_unsicher (|n_e·e_ref| < {g:g}) bei Elementen {liste}"
HINWEIS_OHNE_ELEMENT = "Punkte ohne Element: Normale und Zerlegung NaN: {liste}"
HINWEIS_NORMALE_NULL = "Punktnormale nicht bestimmbar (Summe der Normalen 0): {liste}"
HINWEIS_AMPLITUDE_NULL = "Amplitude 0: Anteil und Achse NaN bei Punkten {liste}"
HINWEIS_KREIS = "Kreisbahn: Richtung der großen Halbachse unbestimmt (NaN) bei Punkten {liste}"
HINWEIS_OHNE_PHASE = "Schwingform ohne gültige Phase: keine Zerlegung und keine Bahnellipse"

#: Schwelle für „Komponente 0“ beim Festlegen des Achsvorzeichens (normierte Achse).
NULL_KOMPONENTE = 1e-12


def _liste(indizes: npt.ArrayLike) -> str:
    return ", ".join(str(int(i)) for i in np.ravel(indizes))


@dataclass(frozen=True, kw_only=True, eq=False)
class Elementnormalen:
    """Normalen und Flächen der Elemente (FG-03 5.1).

    Attributes
    ----------
    elemente : tuple of tuple of int
        Elemente mit 0-basierten Punktindizes (nach M14).
    normale : numpy.ndarray
        ``(E, 3)`` ausgerichtete Einheitsnormalen; NaN bei entarteten Elementen.
    flaeche_m2 : numpy.ndarray
        ``(E,)`` Flächen in m².
    orientierung_unsicher, entartet : numpy.ndarray
        ``(E,)`` Kennzeichen.
    hinweise : tuple of str
        Hinweise.
    """

    elemente: tuple[tuple[int, ...], ...]
    normale: FloatArray
    flaeche_m2: FloatArray
    orientierung_unsicher: BoolArray
    entartet: BoolArray
    hinweise: tuple[str, ...]


def element_normalen(
    koordinaten_m: npt.ArrayLike,
    elemente: Sequence[Sequence[int]],
    *,
    e_ref: npt.ArrayLike = (0.0, 0.0, 1.0),
    index_basis: int = 0,
    orientierung_min: float = 0.1,
    entartet_rel: float = 1e-12,
) -> Elementnormalen:
    """Elementnormalen, ausgerichtet auf ``e_ref`` (FG-03 5.1).

    Raises
    ------
    ValueError
        Bei Elementen mit anderer Eckenzahl als 3 oder 4, Indizes außerhalb der Punkte oder
        falscher Form der Koordinaten.
    """
    x = np.asarray(koordinaten_m, dtype=np.float64)
    if x.ndim != 2 or x.shape[1] != 3:
        raise ValueError(f"koordinaten_m (P, 3) erwartet: {x.shape}")
    ref = np.asarray(e_ref, dtype=np.float64)
    ref = ref / np.linalg.norm(ref)
    elem: list[tuple[int, ...]] = []
    for e in elemente:
        idx = tuple(int(i) - index_basis for i in e)
        if len(idx) not in (3, 4):
            raise ValueError(f"Element {tuple(e)}: 3 oder 4 Knoten erwartet")
        if any(not 0 <= i < x.shape[0] for i in idx):
            raise ValueError(f"Element {tuple(e)}: Punktindex außerhalb 0..{x.shape[0] - 1}")
        elem.append(idx)
    anzahl = len(elem)
    roh = np.zeros((anzahl, 3))
    for j, idx in enumerate(elem):
        p = x[list(idx)]
        if len(idx) == 4:
            roh[j] = np.cross(p[2] - p[0], p[3] - p[1])
        else:
            roh[j] = np.cross(p[1] - p[0], p[2] - p[0])
    laenge = np.linalg.norm(roh, axis=1)
    flaeche = 0.5 * laenge
    median = float(np.median(flaeche)) if anzahl else 0.0
    entartet = ~(flaeche > 0) | (flaeche < entartet_rel * median)
    normale = np.full((anzahl, 3), np.nan)
    gut = ~entartet
    normale[gut] = roh[gut] / laenge[gut, None]
    projektion = normale @ ref
    vorzeichen = np.where(projektion < 0, -1.0, 1.0)
    normale = normale * vorzeichen[:, None]
    with np.errstate(invalid="ignore"):
        unsicher = gut & (np.abs(projektion) < orientierung_min)
    hinweise: list[str] = []
    if np.any(entartet):
        hinweise.append(
            HINWEIS_ENTARTET.format(f=entartet_rel, liste=_liste(np.flatnonzero(entartet)))
        )
    if np.any(unsicher):
        hinweise.append(
            HINWEIS_ORIENTIERUNG.format(g=orientierung_min, liste=_liste(np.flatnonzero(unsicher)))
        )
    return Elementnormalen(
        elemente=tuple(elem),
        normale=normale,
        flaeche_m2=flaeche,
        orientierung_unsicher=unsicher,
        entartet=entartet,
        hinweise=tuple(hinweise),
    )


def punkt_normalen(anzahl_punkte: int, en: Elementnormalen) -> tuple[FloatArray, tuple[str, ...]]:
    r"""Flächengewichtete Punktnormalen :math:`n_p` ``(P, 3)`` (FG-03 5.1).

    Punkte ohne (nicht entartetes) Element oder mit Normalensumme 0 bekommen NaN und einen
    Hinweis.
    """
    summe = np.zeros((anzahl_punkte, 3))
    hat = np.zeros(anzahl_punkte, dtype=bool)
    for j, idx in enumerate(en.elemente):
        if en.entartet[j]:
            continue
        for i in idx:
            summe[i] += en.flaeche_m2[j] * en.normale[j]
            hat[i] = True
    laenge = np.linalg.norm(summe, axis=1)
    null = hat & ~(laenge > 0)
    ok = hat & ~null
    normale = np.full((anzahl_punkte, 3), np.nan)
    normale[ok] = summe[ok] / laenge[ok, None]
    hinweise: list[str] = []
    if np.any(~hat):
        hinweise.append(HINWEIS_OHNE_ELEMENT.format(liste=_liste(np.flatnonzero(~hat))))
    if np.any(null):
        hinweise.append(HINWEIS_NORMALE_NULL.format(liste=_liste(np.flatnonzero(null))))
    return normale, tuple(hinweise)


@dataclass(frozen=True, kw_only=True, eq=False)
class Zerlegung:
    r"""Normal- und Tangentialanteil (FG-03 5.2).

    Attributes
    ----------
    v_normal : numpy.ndarray
        :math:`\hat v_n` complex, Form der Eingabe ohne letzte Achse.
    betrag_normal : numpy.ndarray
        :math:`|\hat v_n|`.
    v_tangential : numpy.ndarray
        :math:`\hat v_t` complex ``(..., 3)``.
    betrag_tangential_psv : numpy.ndarray
        :math:`\sqrt{\sum_i|\hat v_{t,i}|^2}`.
    anteil_normal : numpy.ndarray
        η; NaN bei Amplitude 0 oder ohne Normale.
    """

    v_normal: ComplexArray
    betrag_normal: FloatArray
    v_tangential: ComplexArray
    betrag_tangential_psv: FloatArray
    anteil_normal: FloatArray


def zerlege(v: npt.ArrayLike, normale: npt.ArrayLike) -> Zerlegung:
    """Zerlegt komplexe 3-Vektoren ``(..., 3)`` bezüglich reeller Normalen (FG-03 5.2).

    ``normale`` muss auf die Form von ``v`` broadcastbar sein; NaN-Normalen ergeben NaN.
    """
    vv = np.asarray(v, dtype=np.complex128)
    n = np.asarray(normale, dtype=np.float64)
    if vv.shape[-1] != 3 or n.shape[-1] != 3:
        raise ValueError(f"letzte Achse muss X, Y, Z sein: {vv.shape}, {n.shape}")
    vn = np.sum(n * vv, axis=-1)
    vt = vv - n * vn[..., None]
    gesamt = np.sum(np.abs(vv) ** 2, axis=-1)
    with np.errstate(divide="ignore", invalid="ignore"):
        eta = np.where(gesamt > 0, np.abs(vn) ** 2 / np.where(gesamt > 0, gesamt, 1.0), np.nan)
    return Zerlegung(
        v_normal=vn.astype(np.complex128),
        betrag_normal=np.abs(vn),
        v_tangential=vt.astype(np.complex128),
        betrag_tangential_psv=np.sqrt(np.sum(np.abs(vt) ** 2, axis=-1)),
        anteil_normal=eta.astype(np.float64),
    )


@dataclass(frozen=True, kw_only=True, eq=False)
class Bahnellipse:
    r"""Bahnellipse je Punkt (FG-03 5.3).

    Attributes
    ----------
    auslenkung_max, auslenkung_min : numpy.ndarray
        Halbachsen ``(P,)`` in der Einheit von :math:`\hat v` (wie FG-02 3.6).
    theta_stern_rad : numpy.ndarray
        :math:`\theta^\ast` in rad ``(P,)``.
    achse_max : numpy.ndarray
        Einheitsvektor der großen Halbachse ``(P, 3)``; NaN bei Kreisbahn oder Amplitude 0.
    bahnnormale : numpy.ndarray
        :math:`m = \mathrm{Im}\,\hat v\times\mathrm{Re}\,\hat v` ``(P, 3)``.
    drehsinn : numpy.ndarray
        Drehsinn ``(P,)``: +1, -1, 0 (lineare Bahn) oder NaN (ohne Normale).
    hinweise : tuple of str
        Hinweise.
    """

    auslenkung_max: FloatArray
    auslenkung_min: FloatArray
    theta_stern_rad: FloatArray
    achse_max: FloatArray
    bahnnormale: FloatArray
    drehsinn: FloatArray
    hinweise: tuple[str, ...]


def bahnellipse(
    v: npt.ArrayLike,
    normale: npt.ArrayLike | None = None,
    *,
    e_ref: npt.ArrayLike = (0.0, 0.0, 1.0),
    kreis_rel: float = 1e-12,
    linear_rel: float = 1e-6,
) -> Bahnellipse:
    """Halbachsen, Richtung der großen Halbachse und Drehsinn (FG-03 5.3).

    Parameters
    ----------
    v : array_like
        Komplexe Amplituden ``(P, 3)`` (oder ``(3,)``).
    normale : array_like, optional
        Flächennormalen ``(P, 3)`` für den Drehsinn; ``None`` → Drehsinn NaN.
    e_ref : array_like
        Bezugsrichtung für das Vorzeichen der Achse (M13).
    """
    vv = np.atleast_2d(np.asarray(v, dtype=np.complex128))
    if vv.shape[-1] != 3:
        raise ValueError(f"v (P, 3) erwartet: {vv.shape}")
    ref = np.asarray(e_ref, dtype=np.float64)
    ref = ref / np.linalg.norm(ref)
    _, a_max, a_min = ellipse_kennwerte(vv)
    s = np.sum(vv**2, axis=1)
    gesamt = np.sum(np.abs(vv) ** 2, axis=1)
    theta = -0.5 * np.angle(s)
    achse = np.real(vv * np.exp(1j * theta)[:, None])
    laenge = np.linalg.norm(achse, axis=1)
    null = ~(gesamt > 0)
    kreis = ~null & (np.abs(s) < kreis_rel * gesamt)
    ok = ~null & ~kreis
    achse_n = np.full_like(achse, np.nan)
    achse_n[ok] = achse[ok] / laenge[ok, None]
    for p in np.flatnonzero(ok):
        e = achse_n[p]
        proj = float(e @ ref)
        if abs(proj) > NULL_KOMPONENTE:
            if proj < 0:
                achse_n[p] = -e
        else:
            erste = np.flatnonzero(np.abs(e) > NULL_KOMPONENTE)
            if e[erste[0]] < 0:
                achse_n[p] = -e
    m = np.cross(np.imag(vv), np.real(vv))
    if normale is None:
        drehsinn = np.full(vv.shape[0], np.nan)
    else:
        n = np.broadcast_to(np.asarray(normale, dtype=np.float64), vv.shape)
        drehsinn = np.sign(np.sum(n * m, axis=1))
        with np.errstate(divide="ignore", invalid="ignore"):
            linear = a_min < linear_rel * a_max
        drehsinn = np.where(linear & np.isfinite(drehsinn), 0.0, drehsinn)
        drehsinn = np.where(null, np.nan, drehsinn)  # Amplitude 0: Drehsinn unbestimmt
    hinweise: list[str] = []
    if np.any(null):
        hinweise.append(HINWEIS_AMPLITUDE_NULL.format(liste=_liste(np.flatnonzero(null))))
    if np.any(kreis):
        hinweise.append(HINWEIS_KREIS.format(liste=_liste(np.flatnonzero(kreis))))
    return Bahnellipse(
        auslenkung_max=a_max,
        auslenkung_min=a_min,
        theta_stern_rad=theta,
        achse_max=achse_n,
        bahnnormale=m,
        drehsinn=drehsinn.astype(np.float64),
        hinweise=tuple(hinweise),
    )


@dataclass(frozen=True, kw_only=True, eq=False)
class Komponentenbezug:
    r"""B-8-Ergebnis einer Messung und Schwingform (FG-03 5, Datenvertrag 6.2).

    Attributes
    ----------
    elemente : Elementnormalen
        ``normale_element``, ``flaeche_element``.
    normale_punkt : numpy.ndarray
        ``(P, 3)``.
    f_hz : float
        Frequenz der Schwingform (NaN ohne).
    einheit : str
        Einheit von :math:`\hat v`.
    zerlegung : Zerlegung or None
        ``v_normal``, ``v_tangential``, ``anteil_normal`` (ohne Phase ``None``).
    ellipse : Bahnellipse or None
        ``achse_max``, ``drehsinn``.
    hinweise : tuple of str
        Hinweise.
    annahmen : tuple of AnnahmeEintrag
        M12–M15.
    """

    elemente: Elementnormalen
    normale_punkt: FloatArray
    f_hz: float
    einheit: str
    zerlegung: Zerlegung | None
    ellipse: Bahnellipse | None
    hinweise: tuple[str, ...]
    annahmen: tuple[AnnahmeEintrag, ...]


def komponentenbezug(
    koordinaten_m: npt.ArrayLike,
    elemente: Sequence[Sequence[int]],
    schwingform: Schwingform | None = None,
    *,
    annahmen2: AnnahmenStufe2 | None = None,
    schwellen2: SchwellenStufe2 | None = None,
) -> Komponentenbezug:
    """Normalen, Zerlegung und Bahnellipse für eine Schwingform (FG-03 5).

    Die Amplitude der Schwingform (X, Y, Z) wird mit :math:`D` (M12) in das Geometrie-KS
    gedreht. Ohne gültige Phase entfallen Zerlegung und Bahnellipse (Hinweis).
    """
    annahmen2 = annahmen2 if annahmen2 is not None else AnnahmenStufe2()
    schwellen2 = schwellen2 if schwellen2 is not None else SchwellenStufe2()
    x = np.asarray(koordinaten_m, dtype=np.float64)
    en = element_normalen(
        x,
        elemente,
        e_ref=annahmen2.e_ref_vektor,
        index_basis=annahmen2.elemente_index_basis,
        orientierung_min=schwellen2.orientierung_min,
        entartet_rel=schwellen2.entartet_rel,
    )
    n_p, hinweise_p = punkt_normalen(x.shape[0], en)
    hinweise = [*en.hinweise, *hinweise_p]
    zerlegung: Zerlegung | None = None
    ellipse: Bahnellipse | None = None
    f_hz = math.nan
    einheit = ""
    if schwingform is not None:
        f_hz = schwingform.f_hz
        einheit = schwingform.einheit
        if schwingform.amplitude is None or not schwingform.phase_gueltig:
            hinweise.append(HINWEIS_OHNE_PHASE)
        else:
            v = schwingform.amplitude @ annahmen2.drehung.T
            zerlegung = zerlege(v, n_p)
            ellipse = bahnellipse(
                v,
                n_p,
                e_ref=annahmen2.e_ref_vektor,
                kreis_rel=schwellen2.kreis_rel,
                linear_rel=schwellen2.linear_rel,
            )
            hinweise.extend(ellipse.hinweise)
            null = np.flatnonzero(np.isnan(zerlegung.anteil_normal) & ~np.isnan(n_p[:, 0]))
            if null.size:
                hinweise.append(HINWEIS_AMPLITUDE_NULL.format(liste=_liste(null)))
    return Komponentenbezug(
        elemente=en,
        normale_punkt=n_p,
        f_hz=f_hz,
        einheit=einheit,
        zerlegung=zerlegung,
        ellipse=ellipse,
        hinweise=tuple(dict.fromkeys(hinweise)),
        annahmen=annahmen2.eintraege(),
    )
