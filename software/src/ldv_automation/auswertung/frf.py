r"""H1, H2, Kohärenz, Zufallsfehler, Kohärenzmaske und Gewichte (FG-02 3.3 bis 3.5).

Formeln (FG-02 3.3, identisch mit Polytec Theory Manual S. 14–15 über I2):

.. math::

    H_1 = \frac{\mathrm{CP}_{ab}}{\mathrm{AP}_b},\qquad
    H_2 = \frac{\mathrm{AP}_a}{\mathrm{CP}_{ab}^{*}},\qquad
    \gamma^2_{ab} = \frac{|\mathrm{CP}_{ab}|^2}{\mathrm{AP}_a\,\mathrm{AP}_b}.

Einheit [a]/[b]. Ohne Mittelung (:math:`n_d = 1`) ist γ² ≡ 1 ohne Aussage: γ² wird NaN,
H1 heißt dann „FRF“.

Zufallsfehler (FG-02 3.4, Näherung erster Ordnung nach Bendat/Piersol, Volltext nicht
gelesen [L-m]; numerisch eigen geprüft [N]):

.. math::

    \varepsilon[|\hat H_1|] \approx \frac{\sqrt{1-\gamma^2}}{|\gamma|\sqrt{2n_d}},\quad
    \sigma[\arg\hat H_1] \approx \varepsilon[|\hat H_1|]\ \mathrm{rad},\quad
    \varepsilon[\hat\gamma^2] \approx \frac{\sqrt2\,(1-\gamma^2)}{|\gamma|\sqrt{n_d}}.

Gewicht (FG-02 3.5, inverse Varianz von |H1|): :math:`w = 2n_d\gamma^2/(1-\gamma^2)` mit
γ² auf :math:`\le 1 - 10^{-6}` begrenzt. Gewichte sind **nicht** für räumliche
Punktmittel bestimmt.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import numpy.typing as npt

from .annahmen import AnnahmeEintrag, Schwellen
from .daten import BoolArray, ComplexArray, FloatArray, Paardaten

HINWEIS_FEHLERGRENZEN = (
    "Zufallsfehler: Näherung erster Ordnung (Bendat/Piersol, Volltext nicht gelesen); setzt "
    "unabhängige Blöcke und stationäre Zufallssignale voraus; erfasst keine systematischen "
    "Fehler (Leckage durch nicht abgeklungene Antwort, Auflösungsbias, Nichtlinearität)"
)
HINWEIS_ND1 = "n_d = 1: γ² ohne Aussage (NaN), H1 wird als FRF bezeichnet"
HINWEIS_ND_KLEIN = "n_d < 2: Zufallsfehler nicht bestimmbar (NaN)"
#: Kennzeichen nach FG-02 3.4 (K1-6).
FEHLERBAND_NICHT_AUSSAGEKRAEFTIG = "Fehlerband nicht aussagekräftig"
HINWEIS_BAND_NICHT_AUSSAGEKRAEFTIG = (
    f"{FEHLERBAND_NICHT_AUSSAGEKRAEFTIG} an Linien mit k_ε·ε >= 1 (untere Grenze auf 0 "
    "begrenzt; Maske h1_band_aussagekraeftig = False)"
)

_NAN_C = complex(np.nan, np.nan)


def h1_h2_kohaerenz(
    cp: ComplexArray, ap_antwort: FloatArray, ap_referenz: FloatArray
) -> tuple[ComplexArray, ComplexArray, FloatArray]:
    r"""Berechnet H1, H2 und γ² ohne Begrenzung (FG-02 3.3 und Randfälle 6.3).

    Returns
    -------
    h1, h2 : numpy.ndarray
        ``complex128``. :math:`\mathrm{AP}_b = 0` → H1 = NaN+iNaN; CP = 0 → H2 = NaN+iNaN.
    kohaerenz : numpy.ndarray
        ``float64``. :math:`\mathrm{AP}_a\mathrm{AP}_b = 0` → NaN; CP = 0 bei AP > 0 → 0.
    """
    with np.errstate(divide="ignore", invalid="ignore"):
        h1 = np.where(ap_referenz > 0, cp / np.where(ap_referenz > 0, ap_referenz, 1.0), _NAN_C)
        cp_konj = np.conj(cp)
        h2 = np.where(cp != 0, ap_antwort / np.where(cp != 0, cp_konj, 1.0), _NAN_C)
        nenner = ap_antwort * ap_referenz
        g2 = np.where(nenner > 0, np.abs(cp) ** 2 / np.where(nenner > 0, nenner, 1.0), np.nan)
    # NaN im Eingang wird weitergegeben (FG-02 6.3).
    nan_eingang = np.isnan(cp) | np.isnan(ap_antwort) | np.isnan(ap_referenz)
    g2 = np.where(nan_eingang, np.nan, g2)
    return h1.astype(np.complex128), h2.astype(np.complex128), g2.astype(np.float64)


def begrenze_kohaerenz(kohaerenz: FloatArray, rtol: float = 1e-5) -> tuple[FloatArray, int, float]:
    r"""Setzt γ² in :math:`(1, 1 + \mathrm{rtol}]` auf 1 und zählt (P-05, FG-02 6.3).

    Werte über :math:`1 + \mathrm{rtol}` bleiben unverändert; sie sind ein Fehler der
    Prüfung P-05 und werden nicht still korrigiert.

    Returns
    -------
    kohaerenz : numpy.ndarray
        Begrenzte Kohärenz.
    anzahl_begrenzt : int
        Anzahl der auf 1 gesetzten Werte.
    maximum_roh : float
        Größter Wert vor der Begrenzung (NaN, wenn alle NaN).
    """
    with np.errstate(invalid="ignore"):
        begrenzen = (kohaerenz > 1.0) & (kohaerenz <= 1.0 + rtol)
    maximum = float(np.nanmax(kohaerenz)) if np.any(~np.isnan(kohaerenz)) else float("nan")
    ergebnis: FloatArray = np.where(begrenzen, 1.0, kohaerenz)
    return ergebnis, int(np.count_nonzero(begrenzen)), maximum


def _n_d_spalte(n_d: npt.ArrayLike, form: tuple[int, ...]) -> FloatArray:
    werte = np.asarray(n_d, dtype=np.float64)
    if werte.ndim == 1 and len(form) == 2:
        werte = werte[:, None]
    ergebnis: FloatArray = np.broadcast_to(werte, form).astype(np.float64)
    return ergebnis


def zufallsfehler(
    kohaerenz: FloatArray, n_d: npt.ArrayLike
) -> tuple[FloatArray, FloatArray, FloatArray]:
    """Normierte Zufallsfehler nach FG-02 3.4.

    Parameters
    ----------
    kohaerenz : numpy.ndarray
        γ², beliebige Form, typisch ``(P, K)``.
    n_d : int or array_like
        Mittelungsanzahl; Skalar, ``(P,)`` (je Punkt) oder in der Form von ``kohaerenz``.

    Returns
    -------
    eps_betrag_h1, sigma_phase_h1_rad, eps_kohaerenz : numpy.ndarray
        γ² = 0 → +∞; γ² = 1 → 0; γ² = NaN → NaN; :math:`n_d < 2` → NaN.
    """
    nd = _n_d_spalte(n_d, kohaerenz.shape)
    gamma = np.sqrt(kohaerenz)
    rest = 1.0 - kohaerenz
    with np.errstate(divide="ignore", invalid="ignore"):
        eps_h1 = np.sqrt(rest) / (gamma * np.sqrt(2.0 * nd))
        eps_g2 = np.sqrt(2.0) * rest / (gamma * np.sqrt(nd))
    eps_h1 = np.where(nd < 2, np.nan, eps_h1)
    eps_g2 = np.where(nd < 2, np.nan, eps_g2)
    return eps_h1, eps_h1.copy(), eps_g2


def gewicht(
    kohaerenz: FloatArray, n_d: npt.ArrayLike, kohaerenz_max: float = 1.0 - 1e-6
) -> FloatArray:
    r"""Gewicht :math:`w = 2n_d\gamma^2/(1-\gamma^2)` (FG-02 3.5).

    γ² wird für die Rechnung auf ``kohaerenz_max`` begrenzt, damit γ² = 1 ein endliches
    Gewicht ergibt. γ² = 0 → 0; NaN → NaN; :math:`n_d < 2` → NaN.
    """
    nd = _n_d_spalte(n_d, kohaerenz.shape)
    g2 = np.minimum(kohaerenz, kohaerenz_max)
    w: FloatArray = 2.0 * nd * g2 / (1.0 - g2)
    ergebnis: FloatArray = np.where(nd < 2, np.nan, w)
    return ergebnis


def fehlerband(
    betrag: npt.ArrayLike, eps: npt.ArrayLike, k_eps: float
) -> tuple[FloatArray, FloatArray, BoolArray]:
    r"""Fehlerband von :math:`|H_1|` nach FG-02 3.4 (K1-6).

    Returns
    -------
    unten, oben : numpy.ndarray
        :math:`\max(0, |H_1|(1 - k_\varepsilon\varepsilon))` und
        :math:`|H_1|(1 + k_\varepsilon\varepsilon)`; :math:`|H_1| = 0` bei ε = ∞ ergibt NaN.
    aussagekraeftig : numpy.ndarray
        ``False`` bei :math:`k_\varepsilon\varepsilon \ge 1` (auch ε = +∞) oder ε = NaN;
        Kennzeichen „Fehlerband nicht aussagekräftig“.
    """
    b = np.asarray(betrag, dtype=np.float64)
    e = np.asarray(eps, dtype=np.float64)
    with np.errstate(invalid="ignore"):
        unten: FloatArray = np.maximum(0.0, b * (1.0 - k_eps * e))
        oben: FloatArray = b * (1.0 + k_eps * e)
        aussagekraeftig: BoolArray = k_eps * e < 1.0
    return unten, oben, aussagekraeftig


def kohaerenz_maske(kohaerenz: FloatArray, kohaerenz_min: float) -> BoolArray:
    """Maske ``kohaerenz_ok = γ² >= γ²_min`` (Grenze inklusiv; NaN → ``False``)."""
    with np.errstate(invalid="ignore"):
        ergebnis: BoolArray = kohaerenz >= kohaerenz_min
    return ergebnis


@dataclass(frozen=True, kw_only=True, eq=False)
class FrfErgebnis:
    r"""H1, H2, Kohärenz und Unsicherheit eines Kanalpaars (FG-02 3.3 bis 3.5, 6.2).

    Attributes
    ----------
    antwort, referenz, einheit : str
        Paar und Einheit [a]/[b].
    bezeichnung_h1 : str
        ``"H1"`` oder ``"FRF"`` (alle Punkte mit :math:`n_d = 1`).
    h1, h2 : numpy.ndarray
        ``(P, K)`` complex.
    kohaerenz : numpy.ndarray
        γ², ``(P, K)``; Werte in :math:`(1, 1+10^{-5}]` auf 1 gesetzt.
    anzahl_kohaerenz_begrenzt : int
        Zähler der auf 1 gesetzten Werte (P-05).
    kohaerenz_maximum_roh : float
        Größtes γ² vor der Begrenzung (P-05).
    eps_betrag_h1, sigma_phase_h1_rad, eps_kohaerenz, gewicht : numpy.ndarray
        ``(P, K)``; Einheiten 1, rad, 1, 1.
    h1_band_unten, h1_band_oben : numpy.ndarray
        :math:`\max(0, |H_1|(1 - k_\varepsilon\varepsilon))` und
        :math:`|H_1|(1 + k_\varepsilon\varepsilon)` in [a]/[b] (FG-02 3.4, K1-6).
    h1_band_aussagekraeftig : numpy.ndarray
        ``False`` bei :math:`k_\varepsilon\varepsilon \ge 1` (auch ε = +∞): Kennzeichen
        „Fehlerband nicht aussagekräftig“; NaN-ε ergibt ``False`` ohne Hinweis.
    kohaerenz_ok : numpy.ndarray
        Maske ``γ² >= γ²_min``.
    k_eps, kohaerenz_min : float
        Verwendete Parameter.
    hinweise : tuple of str
        Gültigkeitsgrenzen und Randfälle.
    annahmen : tuple of AnnahmeEintrag
        Geltende Annahmen (P-11).
    """

    antwort: str
    referenz: str
    einheit: str
    bezeichnung_h1: str
    h1: ComplexArray
    h2: ComplexArray
    kohaerenz: FloatArray
    anzahl_kohaerenz_begrenzt: int
    kohaerenz_maximum_roh: float
    eps_betrag_h1: FloatArray
    sigma_phase_h1_rad: FloatArray
    eps_kohaerenz: FloatArray
    gewicht: FloatArray
    h1_band_unten: FloatArray
    h1_band_oben: FloatArray
    h1_band_aussagekraeftig: BoolArray
    kohaerenz_ok: BoolArray
    k_eps: float
    kohaerenz_min: float
    hinweise: tuple[str, ...]
    annahmen: tuple[AnnahmeEintrag, ...]


def berechne_frf(paar: Paardaten, schwellen: Schwellen | None = None) -> FrfErgebnis:
    """H1, H2, γ², Zufallsfehler, Maske und Gewichte eines Paars (FG-02 3.3 bis 3.5).

    Parameters
    ----------
    paar : Paardaten
        Vorverarbeitetes Paar (Vorzeichen s_a·s_b und Konjugation angewandt).
    schwellen : Schwellen, optional
        Freigegebene Schwellen (γ²_min, k_ε, P-05-Reserve).

    Returns
    -------
    FrfErgebnis
    """
    schwellen = schwellen if schwellen is not None else Schwellen()
    h1, h2, g2_roh = h1_h2_kohaerenz(paar.cp, paar.ap_antwort, paar.ap_referenz)
    g2, anzahl, maximum = begrenze_kohaerenz(g2_roh, schwellen.ungleichung_rtol)
    hinweise = [HINWEIS_FEHLERGRENZEN]
    ohne_mittelung = paar.n_d == 1
    if np.any(ohne_mittelung):
        g2 = np.where(ohne_mittelung[:, None], np.nan, g2)
        hinweise.append(HINWEIS_ND1)
    if np.any(paar.n_d < 2):
        hinweise.append(HINWEIS_ND_KLEIN)
    eps_h1, sigma_phase, eps_g2 = zufallsfehler(g2, paar.n_d)
    betrag = np.abs(h1)
    band_unten, band_oben, aussagekraeftig = fehlerband(betrag, eps_h1, schwellen.k_eps)
    if np.any(~aussagekraeftig & ~np.isnan(eps_h1)):
        hinweise.append(HINWEIS_BAND_NICHT_AUSSAGEKRAEFTIG)
    return FrfErgebnis(
        antwort=paar.antwort,
        referenz=paar.referenz,
        einheit=paar.einheit_frf,
        bezeichnung_h1="FRF" if bool(np.all(ohne_mittelung)) else "H1",
        h1=h1,
        h2=h2,
        kohaerenz=g2,
        anzahl_kohaerenz_begrenzt=anzahl,
        kohaerenz_maximum_roh=maximum,
        eps_betrag_h1=eps_h1,
        sigma_phase_h1_rad=sigma_phase,
        eps_kohaerenz=eps_g2,
        gewicht=gewicht(g2, paar.n_d, schwellen.gewicht_kohaerenz_max),
        h1_band_unten=band_unten,
        h1_band_oben=band_oben,
        h1_band_aussagekraeftig=aussagekraeftig,
        kohaerenz_ok=kohaerenz_maske(g2, schwellen.kohaerenz_min),
        k_eps=schwellen.k_eps,
        kohaerenz_min=schwellen.kohaerenz_min,
        hinweise=tuple(hinweise),
        annahmen=paar.annahmen,
    )
