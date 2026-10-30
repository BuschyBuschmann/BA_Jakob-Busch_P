r"""B-1: Parametrische Dämpfungsschätzung mit komplexem Moden-Fit (FG-03 Abschnitt 3).

Modellform (FG-03 2, Mobilität :math:`Y` in (m/s)/N, Zeitabhängigkeit :math:`e^{+i\omega t}`):

.. math::

    \hat Y(\omega) = \sum_{r=1}^{n}\frac{i\omega\,R_r}{\omega_r^2-\omega^2+2i\zeta_r\omega_r\omega}
    + C ,\qquad \omega_r = 2\pi f_r .

Schätzer (FG-03 3.2, Entscheidung E1 a): Variablenprojektion. Für feste
:math:`\theta = (f_r, \ln\zeta_r)` folgen :math:`R_r` und :math:`C` aus dem komplexen
Kleinste-Quadrate-Problem; über θ minimiert Levenberg-Marquardt
:math:`S(\theta) = \lVert H - \Phi(\theta)c^\ast(\theta)\rVert_2^2` (Jacobi-Matrix aus finiten
Vorwärtsdifferenzen über Real- und Imaginärteil, Abbruch bei relativer Änderung von S kleiner
``tol_rel``; das gilt für einen angenommenen wie für einen verworfenen Versuchsschritt, siehe
:func:`fit_moden`). Standardabweichungen aus der Gauss-Newton-Kovarianz
:math:`s^2 (J^\mathsf{T}J)^{-1}` mit :math:`s^2 = S/(2|\mathcal K| - p)`, :math:`p = 4n + 2`.
Gütemaß :math:`\rho = \lVert H - \hat H\rVert_2/\lVert H\rVert_2`.

Die Schritte folgen dem Prüfskript ``fit.py`` im Anhang von FG-03 (Schrittweite der
Differenzen :math:`10^{-7}\max(1, |\theta_j|)`, Start :math:`\lambda = 10^{-3}`, Dämpfung mit
:math:`\mathrm{diag}(J^\mathsf{T}J)`, :math:`\lambda` bei Erfolg durch 10 bis
:math:`10^{-12}`, bei Misserfolg mal 10).

Gültigkeit (FG-03 3.6): Linearität, schwache Dämpfung (ζ < 0,2), Fitband mit nur den Moden der
Gruppe und konstantem Residuum. Ohne Rauschen und Leckage exakt für :math:`B/\Delta f \ge 0{,}64`
(RF-F1); Pole bei Impulsanregung trotz Abschneidung unverfälscht (RF-F4); Burst-Chirp mit
Rechteckfenster ζ-Fehler <= 2,5 % (RF-F5). Moden, die Stufe 1 nicht als getrennte Spitzen
findet, erkennt auch dieser Fit nicht. Hann-Fenster auf transienten Daten ist nicht geprüft (M5).
"""

from __future__ import annotations

import math
from collections.abc import Sequence
from dataclasses import dataclass
from typing import Literal

import numpy as np
import numpy.typing as npt

from .annahmen import AnnahmeEintrag, Schwellen, SchwellenStufe2
from .daten import BoolArray, ComplexArray, FloatArray
from .gesamt import Auswertung, PaarAuswertung
from .spitzen import (
    GUELTIGKEIT_OFFEN_M7,
    KOHAERENZ_NIEDRIG,
    NACHBARMODE,
    UEBERLAPPEND,
    Spitze,
)
from .umrechnung import akzeleranz_zu_mobilitaet

# Kennzeichen nach FG-03 3.3, 3.4 und 6.3.
MODELL_PASST_NICHT = "modell_passt_nicht"
UNSICHER = "unsicher"
NICHT_KONVERGIERT = "nicht_konvergiert"
AUSSERHALB_BAND = "ausserhalb_band"
KEIN_MOBILITAETSBEZUG = "kein_mobilitaetsbezug"
ZU_WENIG_LINIEN = "zu_wenig_linien"
GRUPPE_ZU_GROSS = "gruppe_zu_gross"
#: Mehr-Moden-Fit: Reihenfolge der gefitteten f_r weicht von der der Startwerte ab
#: (Korrektur K-W5-2, Review M2). Die Zuordnung Mode ↔ Stufe-1-Spitze ist dann unsicher.
MODEN_VERTAUSCHT = "moden_vertauscht"

#: Kennzeichen, mit denen ein Ergebnis nicht in die Zusammenfassung eingeht (FG-03 3.4).
AUSSCHLUSS_ZUSAMMENFASSUNG: tuple[str, ...] = (
    MODELL_PASST_NICHT,
    NICHT_KONVERGIERT,
    AUSSERHALB_BAND,
    MODEN_VERTAUSCHT,
)

HINWEIS_NULL = "‖H‖ = 0 im Fitband: kein Fit"
HINWEIS_KEINE_PUNKTE = "keine brauchbaren Punkte für die Zusammenfassung"
HINWEIS_GEWICHT = (
    "Gewichtung 1/(|H1|ε)²: Linien ohne endliches Gewicht (n_d < 2) entfallen; rho_max ist für "
    "die gewichtete Rechnung nicht kalibriert (FG-03 3.4 gilt für ungewichtete Fits)"
)
HINWEIS_KOHAERENZ_NAN = "Kohärenz nicht prüfbar: γ² = NaN im Fitband (Linien bleiben im Fit)"
HINWEIS_VIB_REF2 = (
    "FRF ist weder Mobilität noch Akzeleranz: Modellform nur lokale Näherung "
    "(kein_mobilitaetsbezug)"
)
GRENZE_VERFAHREN = (
    "Moden, die Stufe 1 nicht als getrennte Spitzen findet (Abstand ≲ B), erkennt auch B-1 "
    "nicht; rho zeigt sie nur bei merklicher Modellabweichung (FG-03 3.3)"
)
GRENZE_LECKAGE = (
    "Hann-Fenster auf transienten Daten: Modellform nicht geprüft (M5); Linienversatz (M2) "
    "verschiebt f_r um Δf (FG-03 3.6)"
)

FrfArt = Literal["mobilitaet", "akzeleranz", "andere"]
"""Art der FRF des Paars (FG-03 2)."""

#: Relative Schrittweite der finiten Differenzen (Prüfskript ``fit.py``).
DIFF_SCHRITT = 1e-7
#: Startwert und Untergrenze von λ (Prüfskript ``fit.py``).
LAMBDA_START = 1e-3
LAMBDA_MIN = 1e-12


def basis_mobilitaet(
    frequenz_hz: npt.ArrayLike, fr_hz: npt.ArrayLike, zeta: npt.ArrayLike
) -> ComplexArray:
    r"""Basismatrix :math:`\Phi`, Form ``(K, n + 1)``.

    Spalte r: :math:`i\omega/(\omega_r^2 - \omega^2 + 2i\zeta_r\omega_r\omega)` in
    (m/s)/N je kg⁻¹; letzte Spalte 1 für das Residuum :math:`C`.
    """
    w = 2.0 * np.pi * np.asarray(frequenz_hz, dtype=np.float64)[:, None]
    wr = 2.0 * np.pi * np.asarray(fr_hz, dtype=np.float64)[None, :]
    z = np.asarray(zeta, dtype=np.float64)[None, :]
    spalten = 1j * w / (wr**2 - w**2 + 2j * z * wr * w)
    ergebnis: ComplexArray = np.hstack([spalten, np.ones((w.shape[0], 1))]).astype(np.complex128)
    return ergebnis


@dataclass(frozen=True, kw_only=True, eq=False)
class FitRoh:
    r"""Ergebnis des reinen Schätzers (FG-03 3.2).

    Attributes
    ----------
    fr_hz, zeta : numpy.ndarray
        ``(n,)`` Eigenfrequenzen in Hz und Dämpfungsgrade.
    sd_fr_hz, sd_zeta_rel : numpy.ndarray
        ``(n,)`` Standardabweichungen :math:`\sigma_{f_r}` in Hz und
        :math:`\sigma_\zeta/\zeta = \sigma_{\ln\zeta}`; NaN bei singulärer Normalgleichung.
    modalkonstante : numpy.ndarray
        ``(n,)`` complex, :math:`R_r` in kg⁻¹ (bei Mobilität).
    residuum : complex
        :math:`C` in der Einheit der FRF.
    rho : float
        :math:`\lVert H - \hat H\rVert_2/\lVert H\rVert_2` (mit Gewichten, falls gesetzt).
    iterationen : int
        Ausgeführte Levenberg-Marquardt-Schritte.
    konvergiert : bool
        ``True`` nur bei Abbruch über das Konvergenzkriterium.
    abbruch : str
        ``"konvergiert"``, ``"max_iter"``, ``"lambda"`` oder ``"singulaer"``.
    """

    fr_hz: FloatArray
    zeta: FloatArray
    sd_fr_hz: FloatArray
    sd_zeta_rel: FloatArray
    modalkonstante: ComplexArray
    residuum: complex
    rho: float
    iterationen: int
    konvergiert: bool
    abbruch: str


def _projektion(
    f: FloatArray, h: ComplexArray, fr: FloatArray, zeta: FloatArray, w: FloatArray
) -> tuple[ComplexArray, ComplexArray]:
    phi = basis_mobilitaet(f, fr, zeta)
    loesung, *_ = np.linalg.lstsq(phi * w[:, None], h * w, rcond=None)
    c: ComplexArray = np.asarray(loesung, dtype=np.complex128)
    r: ComplexArray = (h - phi @ c) * w
    return c, r


def fit_moden(
    frequenz_hz: npt.ArrayLike,
    h: npt.ArrayLike,
    fr0_hz: Sequence[float] | npt.ArrayLike,
    zeta0: Sequence[float] | npt.ArrayLike,
    *,
    gewicht: npt.ArrayLike | None = None,
    max_iter: int = 200,
    tol_rel: float = 1e-12,
    lambda_max: float = 1e12,
) -> FitRoh:
    r"""Komplexer Moden-Fit mit Variablenprojektion und Levenberg-Marquardt (FG-03 3.2).

    Parameters
    ----------
    frequenz_hz : array_like
        Fitlinien ``(m,)`` in Hz (nur die verwendeten Linien, Maske bereits angewandt).
    h : array_like
        Komplexe Mobilität ``(m,)`` in (m/s)/N auf diesen Linien.
    fr0_hz, zeta0 : array_like
        Startwerte ``(n,)``; :math:`f_r^{(0)} > 0`, :math:`\zeta^{(0)} > 0`.
    gewicht : array_like, optional
        Gewichte ``(m,)`` >= 0 (E3 b); ``None`` = ungewichtet (Voreinstellung E3 a).
    max_iter, tol_rel, lambda_max
        Abbruchgrenzen (FG-03 3.2, 3.4).

    Returns
    -------
    FitRoh

    Notes
    -----
    Abbruchkriterium (FG-03 3.2, K2-2): Der Fit gilt als konvergiert, sobald ein
    Versuchsschritt S relativ um höchstens ``tol_rel`` ändert, gleich ob der Schritt angenommen
    oder verworfen wird: :math:`|S(\theta + \delta) - S(\theta)| \le 10^{-12}\,S(\theta)`. Ein
    verworfener Schritt mit so kleiner Änderung zeigt, dass der Gradient auf Rundungsniveau
    liegt. ``nicht_konvergiert`` bleibt für ``max_iter`` Schritte ohne Abbruch,
    :math:`\lambda > \lambda_\mathrm{max}` oder eine singuläre Normalgleichung.

    Raises
    ------
    ValueError
        Bei unpassenden Formen, nicht endlichen Werten, ungültigen Startwerten oder weniger
        als :math:`4n + 3` Linien.
    """
    f = np.asarray(frequenz_hz, dtype=np.float64)
    hh = np.asarray(h, dtype=np.complex128)
    fr0 = np.atleast_1d(np.asarray(fr0_hz, dtype=np.float64))
    z0 = np.atleast_1d(np.asarray(zeta0, dtype=np.float64))
    n = fr0.shape[0]
    if f.ndim != 1 or hh.shape != f.shape:
        raise ValueError(f"frequenz_hz {f.shape} und h {hh.shape} müssen (m,) sein")
    if fr0.ndim != 1 or z0.shape != fr0.shape or n < 1:
        raise ValueError(f"Startwerte fr0 {fr0.shape} und zeta0 {z0.shape} müssen (n,) sein")
    if not (np.all(np.isfinite(f)) and np.all(np.isfinite(hh))):
        raise ValueError("frequenz_hz und h müssen endlich sein")
    if not (np.all(np.isfinite(fr0)) and np.all(fr0 > 0) and np.all(z0 > 0)):
        raise ValueError("Startwerte müssen endlich und > 0 sein")
    if f.shape[0] < 4 * n + 3:
        raise ValueError(f"{f.shape[0]} Linien < 4n + 3 = {4 * n + 3} (zu_wenig_linien)")
    if gewicht is None:
        w = np.ones_like(f)
    else:
        g = np.asarray(gewicht, dtype=np.float64)
        if g.shape != f.shape or not np.all(np.isfinite(g)) or np.any(g < 0):
            raise ValueError("gewicht muss (m,), endlich und >= 0 sein")
        w = np.sqrt(g)

    unendlich = np.full(2 * f.shape[0], np.inf)

    def residuen(theta: FloatArray) -> FloatArray:
        # Ein Versuchsschritt mit nicht darstellbaren Parametern (ζ-Überlauf, Pol auf einer
        # Linie) ergibt S = +∞ und wird verworfen.
        with np.errstate(over="ignore", invalid="ignore", divide="ignore"):
            zeta = np.exp(theta[n:])
            if not (np.all(np.isfinite(theta)) and np.all(np.isfinite(zeta))):
                return unendlich
            phi = basis_mobilitaet(f, theta[:n], zeta)
        if not np.all(np.isfinite(phi)):
            return unendlich
        try:
            _, r = _projektion(f, hh, theta[:n], zeta, w)
        except np.linalg.LinAlgError:  # pragma: no cover - nur bei endlicher, entarteter Basis
            return unendlich
        ergebnis: FloatArray = np.concatenate([r.real, r.imag])
        return ergebnis

    def jacobi(theta: FloatArray, r0: FloatArray) -> FloatArray:
        j = np.empty((r0.shape[0], theta.shape[0]))
        for i in range(theta.shape[0]):
            schritt = DIFF_SCHRITT * max(1.0, abs(float(theta[i])))
            d = theta.copy()
            d[i] += schritt
            j[:, i] = (residuen(d) - r0) / schritt
        return j

    norm_h = float(np.linalg.norm(hh * w))
    theta = np.concatenate([fr0, np.log(z0)])
    lam = LAMBDA_START
    r0 = residuen(theta)
    s0 = float(r0 @ r0)
    abbruch = "max_iter"
    iterationen = 0
    for schritt_nr in range(max_iter):
        iterationen = schritt_nr + 1
        jac = jacobi(theta, r0)
        if not np.all(np.isfinite(jac)):
            abbruch = "singulaer"
            break
        a = jac.T @ jac
        g = jac.T @ r0
        akzeptiert = False
        r1 = r0
        s1 = s0
        while True:
            try:
                delta = -np.linalg.solve(a + lam * np.diag(np.diag(a)), g)
            except np.linalg.LinAlgError:
                abbruch = "singulaer"
                break
            r_versuch = residuen(theta + delta)
            s_versuch = float(r_versuch @ r_versuch)
            if s_versuch < s0:
                theta = theta + delta
                r1, s1 = r_versuch, s_versuch
                lam = max(lam / 10.0, LAMBDA_MIN)
                akzeptiert = True
                break
            if s_versuch - s0 <= tol_rel * max(s0, 1e-300):
                # Auch ein verworfener Versuch, der S relativ um weniger als tol_rel ändert,
                # erfüllt das Abbruchkriterium (FG-03 3.2): S ist im Rahmen der
                # Differenzen-Jacobi-Matrix stationär.
                abbruch = "konvergiert"
                break
            lam *= 10.0
            if lam > lambda_max:
                abbruch = "lambda"
                break
        if abbruch == "konvergiert":
            break
        if not akzeptiert:
            break  # singulär oder λ > λ_max: θ bleibt beim letzten akzeptierten Schritt
        if abs(s0 - s1) <= tol_rel * max(s0, 1e-300):
            r0, s0 = r1, s1
            abbruch = "konvergiert"
            break
        r0, s0 = r1, s1
    fr = theta[:n].copy()
    zeta = np.exp(theta[n:])
    c, r = _projektion(f, hh, fr, zeta, w)
    r0 = np.concatenate([r.real, r.imag])
    s0 = float(r0 @ r0)
    m = r0.shape[0]
    p = 4 * n + 2
    s2 = s0 / max(m - p, 1)
    jac = jacobi(theta, r0)
    try:
        kov = s2 * np.linalg.inv(jac.T @ jac)
        with np.errstate(invalid="ignore"):
            sd = np.sqrt(np.diag(kov))
    except np.linalg.LinAlgError:
        sd = np.full(theta.shape[0], np.nan)
    rho = float(np.linalg.norm(r) / norm_h)
    return FitRoh(
        fr_hz=fr,
        zeta=zeta,
        sd_fr_hz=sd[:n].astype(np.float64),
        sd_zeta_rel=sd[n:].astype(np.float64),
        modalkonstante=c[:n].astype(np.complex128),
        residuum=complex(c[n]),
        rho=rho,
        iterationen=iterationen,
        konvergiert=abbruch == "konvergiert",
        abbruch=abbruch,
    )


def kennzeichen_fit(
    roh: FitRoh,
    *,
    f_band_hz: tuple[float, float],
    delta_f_hz: float,
    schwellen2: SchwellenStufe2,
    m7_grenze_hz: float | None = None,
    mobilitaetsbezug: bool = True,
) -> tuple[tuple[str, ...], ...]:
    r"""Kennzeichen je Mode nach FG-03 3.4.

    ``modell_passt_nicht`` (rho > rho_max), ``nicht_konvergiert`` und ``kein_mobilitaetsbezug``
    gelten für alle Moden des Fits; ``unsicher`` (:math:`\sigma_\zeta/\zeta` >
    ``sd_zeta_rel_max`` oder :math:`\sigma_{f_r} > 0{,}5\,\Delta f`, auch bei nicht bestimmbarer
    Standardabweichung), ``ausserhalb_band`` (:math:`f_r` außerhalb ``f_band_hz``, ζ >= ζ_max
    oder ζ < ζ_min) und ``gueltigkeit_offen_m7`` (:math:`f_r` > M7-Grenze) je Mode.
    """
    gemeinsam: list[str] = []
    if roh.rho > schwellen2.rho_max:
        gemeinsam.append(MODELL_PASST_NICHT)
    if not roh.konvergiert:
        gemeinsam.append(NICHT_KONVERGIERT)
    if not mobilitaetsbezug:
        gemeinsam.append(KEIN_MOBILITAETSBEZUG)
    ergebnis: list[tuple[str, ...]] = []
    for i in range(roh.fr_hz.shape[0]):
        k = list(gemeinsam)
        sd_z = float(roh.sd_zeta_rel[i])
        sd_f = float(roh.sd_fr_hz[i])
        if not (
            math.isfinite(sd_z)
            and math.isfinite(sd_f)
            and sd_z <= schwellen2.sd_zeta_rel_max
            and sd_f <= schwellen2.sd_fr_df_max * delta_f_hz
        ):
            k.append(UNSICHER)
        fr = float(roh.fr_hz[i])
        z = float(roh.zeta[i])
        if (
            not f_band_hz[0] <= fr <= f_band_hz[1]
            or not z < schwellen2.zeta_max
            or z < schwellen2.zeta_min
        ):
            k.append(AUSSERHALB_BAND)
        if m7_grenze_hz is not None and fr > m7_grenze_hz:
            k.append(GUELTIGKEIT_OFFEN_M7)
        ergebnis.append(tuple(k))
    return tuple(ergebnis)


def frf_art_aus_einheiten(einheit_antwort: str, einheit_referenz: str) -> FrfArt:
    """Art der FRF aus den Kanaleinheiten (FG-03 2): Mobilität (m/s)/N, Akzeleranz (m/s²)/N."""
    a = einheit_antwort.replace(" ", "").replace("²", "^2")
    b = einheit_referenz.replace(" ", "")
    if b != "N":
        return "andere"
    if a == "m/s":
        return "mobilitaet"
    if a in ("m/s^2", "m/s2"):
        return "akzeleranz"
    return "andere"


@dataclass(frozen=True, kw_only=True)
class Gruppe:
    r"""Fitgruppe aus Spitzen der Stufe 1 (FG-03 3.3).

    Attributes
    ----------
    nummer : int
        0-basierte Gruppennummer.
    spitzen : tuple of int
        Indizes der Stufe-1-Spitzen (nach Frequenz sortiert).
    f_sp_hz : tuple of float
        Spitzenfrequenzen aus Stufe 1.
    k_von, k_bis : int
        Fitband als 0-basierte Linienindizes (beide inklusive).
    kennzeichen : tuple of str
        ``gruppe_zu_gross`` bei mehr als :math:`n_\mathrm{max}` Spitzen.
    """

    nummer: int
    spitzen: tuple[int, ...]
    f_sp_hz: tuple[float, ...]
    k_von: int
    k_bis: int
    kennzeichen: tuple[str, ...]


def _verbunden(a: Spitze, b: Spitze, faktor: float, n_fit_hz: float) -> bool:
    abstand = abs(a.f_sp_hz - b.f_sp_hz)
    for s in (a, b):
        if NACHBARMODE in s.kennzeichen and abstand < faktor * s.breite_3db_hz:
            return True
    return (UEBERLAPPEND in a.kennzeichen or UEBERLAPPEND in b.kennzeichen) and (
        abstand <= n_fit_hz
    )


def _lokales_minimum(y: FloatArray, start: int, ende: int, richtung: int) -> int | None:
    """Erste Linie j zwischen ``start`` und ``ende`` (ohne ``ende``) mit lokalem Minimum."""
    j = start
    while j != ende:
        if 0 < j < y.shape[0] - 1 and y[j] <= y[j - 1] and y[j] <= y[j + 1]:
            return j
        j += richtung
    return None


def bilde_gruppen(
    spitzen: Sequence[Spitze],
    y_betrag: npt.ArrayLike,
    delta_f_hz: float,
    *,
    schwellen2: SchwellenStufe2 | None = None,
    nachbar_faktor: float = 3.0,
) -> tuple[Gruppe, ...]:
    r"""Gruppen und Fitbänder aus den Spitzen der Stufe 1 (FG-03 3.3).

    Zwei Spitzen gehören zusammen, wenn ihr Abstand kleiner als ``nachbar_faktor``·B einer
    Spitze mit Kennzeichen ``nachbarmode`` ist oder eine von beiden ``ueberlappend`` trägt und
    der Abstand höchstens :math:`n_\mathrm{fit}\,\Delta f` beträgt; die Gruppe wird transitiv
    gebildet. Fitband: erste Spitzenlinie :math:`- n_\mathrm{fit}` bis letzte
    :math:`+ n_\mathrm{fit}`, an der Achse begrenzt und je Seite am nächsten lokalen Minimum
    von ``y_betrag`` gekürzt, wenn dahinter im Band eine Spitze einer anderen Gruppe liegt.

    Parameters
    ----------
    spitzen : sequence of Spitze
        Spitzen der Stufe 1 (nach Frequenz sortiert).
    y_betrag : array_like
        Kurve ``(K,)``, auf der Stufe 1 gesucht hat (Betragsmittel |H1|).
    delta_f_hz : float
        Linienabstand.
    schwellen2 : SchwellenStufe2, optional
        :math:`n_\mathrm{fit}` und :math:`n_\mathrm{max}`.
    nachbar_faktor : float
        Faktor des Kennzeichens ``nachbarmode`` aus Stufe 1 (FG-02 3.9), 3.
    """
    schwellen2 = schwellen2 if schwellen2 is not None else SchwellenStufe2()
    y = np.asarray(y_betrag, dtype=np.float64)
    anzahl = len(spitzen)
    eltern = list(range(anzahl))

    def wurzel(i: int) -> int:
        while eltern[i] != i:
            eltern[i] = eltern[eltern[i]]
            i = eltern[i]
        return i

    n_fit_hz = schwellen2.n_fit * delta_f_hz
    for i in range(anzahl):
        for j in range(i + 1, anzahl):
            if _verbunden(spitzen[i], spitzen[j], nachbar_faktor, n_fit_hz):
                eltern[wurzel(j)] = wurzel(i)
    mengen: dict[int, list[int]] = {}
    for i in range(anzahl):
        mengen.setdefault(wurzel(i), []).append(i)
    reihen = sorted(
        (sorted(m, key=lambda i: spitzen[i].f_sp_hz) for m in mengen.values()),
        key=lambda m: spitzen[m[0]].f_sp_hz,
    )
    gruppen: list[Gruppe] = []
    for nummer, glieder in enumerate(reihen):
        ks = [spitzen[i].k for i in glieder]
        k_erste, k_letzte = min(ks), max(ks)
        von = max(0, k_erste - schwellen2.n_fit)
        bis = min(y.shape[0] - 1, k_letzte + schwellen2.n_fit)
        fremd = [spitzen[i].k for i in range(anzahl) if i not in glieder]
        links = [k for k in fremd if von <= k < k_erste]
        if links:
            k_andere = max(links)
            j_links = _lokales_minimum(y, k_erste - 1, k_andere, -1)
            von = j_links if j_links is not None else k_andere + 1
        rechts = [k for k in fremd if k_letzte < k <= bis]
        if rechts:
            k_andere = min(rechts)
            j_rechts = _lokales_minimum(y, k_letzte + 1, k_andere, +1)
            bis = j_rechts if j_rechts is not None else k_andere - 1
        gruppen.append(
            Gruppe(
                nummer=nummer,
                spitzen=tuple(glieder),
                f_sp_hz=tuple(spitzen[i].f_sp_hz for i in glieder),
                k_von=int(von),
                k_bis=int(bis),
                kennzeichen=(GRUPPE_ZU_GROSS,) if len(glieder) > schwellen2.n_max else (),
            )
        )
    return tuple(gruppen)


@dataclass(frozen=True, kw_only=True)
class ModenErgebnis:
    r"""B-1 an einem Punkt für eine Gruppe (FG-03 Datenvertrag 6.2).

    Alle Tupel haben die Länge ``n_moden`` (Reihenfolge der Spitzen der Gruppe).

    Attributes
    ----------
    punkt : int
        0-basierter Punktindex.
    gruppe : int
        Gruppennummer.
    spitzen : tuple of int
        Indizes der Stufe-1-Spitzen der Gruppe.
    gefittet : bool
        ``False``, wenn kein Fit möglich war (Kennzeichen bzw. Hinweis).
    fr_hz, sd_fr_hz : tuple of float
        :math:`f_r` und :math:`\sigma_{f_r}` in Hz.
    zeta, sd_zeta_rel : tuple of float
        ζ und :math:`\sigma_\zeta/\zeta`.
    breite_fit_hz : tuple of float
        :math:`B_\mathrm{fit} = 2\zeta_r f_r` in Hz.
    modalkonstante : tuple of complex
        :math:`R_r` in kg⁻¹ (Mobilität).
    residuum : complex
        :math:`C` in (m/s)/N.
    rho : float
        Gütemaß.
    n_linien : int
        Linien im Fit nach Maske.
    n_moden : int
        Modenzahl n.
    iterationen : int
        Levenberg-Marquardt-Schritte.
    kennzeichen : tuple of tuple of str
        Kennzeichen je Mode.
    hinweise : tuple of str
        Hinweise (z. B. ‖H‖ = 0).
    """

    punkt: int
    gruppe: int
    spitzen: tuple[int, ...]
    gefittet: bool
    fr_hz: tuple[float, ...]
    sd_fr_hz: tuple[float, ...]
    zeta: tuple[float, ...]
    sd_zeta_rel: tuple[float, ...]
    breite_fit_hz: tuple[float, ...]
    modalkonstante: tuple[complex, ...]
    residuum: complex
    rho: float
    n_linien: int
    n_moden: int
    iterationen: int
    kennzeichen: tuple[tuple[str, ...], ...]
    hinweise: tuple[str, ...]


@dataclass(frozen=True, kw_only=True)
class Zusammenfassung:
    r"""Zusammenfassung je Stufe-1-Spitze über die stärksten Punkte (FG-03 3.5).

    Attributes
    ----------
    spitze : int
        Index der Stufe-1-Spitze.
    gruppe : int
        Gruppennummer.
    mode : int
        Index der Mode in der Gruppe.
    f_sp_hz : float
        Spitzenfrequenz aus Stufe 1.
    fr_median_hz, fr_iqr_hz : float
        Median und Interquartilsabstand von :math:`f_r` in Hz.
    zeta_median, zeta_iqr : float
        Median und Interquartilsabstand von ζ.
    sd_fr_median_hz : float
        Median der Fit-Standardabweichungen :math:`\sigma_{f_r}` in Hz der verwendeten Punkte.
    rho_median : float
        Median von rho der verwendeten Punkte.
    n_punkte : int
        Anzahl verwendeter Punkte (ohne Ausschlusskennzeichen).
    punkte : tuple of int
        Die :math:`n_\mathrm{P}` stärksten Punkte (Kandidaten).
    hinweise : tuple of str
        Hinweise.
    """

    spitze: int
    gruppe: int
    mode: int
    f_sp_hz: float
    fr_median_hz: float
    fr_iqr_hz: float
    zeta_median: float
    zeta_iqr: float
    sd_fr_median_hz: float
    rho_median: float
    n_punkte: int
    punkte: tuple[int, ...]
    hinweise: tuple[str, ...]


@dataclass(frozen=True, kw_only=True, eq=False)
class ModenfitErgebnis:
    """B-1 eines Kanalpaars (FG-03 3, Datenvertrag 6.2).

    Attributes
    ----------
    antwort, referenz : str
        Kanalpaar.
    frf_art : {"mobilitaet", "akzeleranz", "andere"}
        Art der FRF; Akzeleranz wird vor dem Fit in Mobilität umgerechnet.
    einheit_fit : str
        Einheit der gefitteten FRF.
    gruppen : tuple of Gruppe
        Alle Gruppen der Stufe-1-Spitzen.
    ergebnisse : tuple of ModenErgebnis
        Fit je Punkt und ausgewählter Gruppe.
    zusammenfassung : tuple of Zusammenfassung
        Je Stufe-1-Spitze der ausgewählten Gruppen.
    schwellen2 : SchwellenStufe2
        Verwendete Parameter.
    hinweise, grenzen : tuple of str
        Hinweise und dokumentierte Grenzen.
    annahmen : tuple of AnnahmeEintrag
        Geltende Annahmen M1–M11 (P-11).
    """

    antwort: str
    referenz: str
    frf_art: FrfArt
    einheit_fit: str
    gruppen: tuple[Gruppe, ...]
    ergebnisse: tuple[ModenErgebnis, ...]
    zusammenfassung: tuple[Zusammenfassung, ...]
    schwellen2: SchwellenStufe2
    hinweise: tuple[str, ...]
    grenzen: tuple[str, ...]
    annahmen: tuple[AnnahmeEintrag, ...]

    def ergebnis(self, punkt: int, gruppe: int) -> ModenErgebnis | None:
        """Ergebnis eines Punkts für eine Gruppe oder ``None``."""
        for e in self.ergebnisse:
            if e.punkt == punkt and e.gruppe == gruppe:
                return e
        return None

    def zusammenfassung_bei(self, f_hz: float) -> Zusammenfassung:
        """Zusammenfassung der Spitze mit der nächsten Stufe-1-Frequenz.

        Raises
        ------
        ValueError
            Ohne Zusammenfassung.
        """
        if not self.zusammenfassung:
            raise ValueError("keine Zusammenfassung vorhanden")
        return min(self.zusammenfassung, key=lambda z: abs(z.f_sp_hz - f_hz))


def _leer(
    punkt: int, gruppe: Gruppe, n_linien: int, kennzeichen: tuple[str, ...], hinweise: list[str]
) -> ModenErgebnis:
    n = len(gruppe.spitzen)
    nan = (math.nan,) * n
    return ModenErgebnis(
        punkt=punkt,
        gruppe=gruppe.nummer,
        spitzen=gruppe.spitzen,
        gefittet=False,
        fr_hz=nan,
        sd_fr_hz=nan,
        zeta=nan,
        sd_zeta_rel=nan,
        breite_fit_hz=nan,
        modalkonstante=(complex(math.nan, math.nan),) * n,
        residuum=complex(math.nan, math.nan),
        rho=math.nan,
        n_linien=n_linien,
        n_moden=n,
        iterationen=0,
        kennzeichen=(kennzeichen,) * n,
        hinweise=tuple(hinweise),
    )


def fit_punkt(
    frequenz_hz: FloatArray,
    y: ComplexArray,
    maske: BoolArray,
    gruppe: Gruppe,
    spitzen: Sequence[Spitze],
    *,
    punkt: int,
    delta_f_hz: float,
    schwellen2: SchwellenStufe2,
    gewicht: FloatArray | None = None,
    m7_grenze_hz: float | None = None,
    mobilitaetsbezug: bool = True,
    zusatz: Sequence[tuple[str, ...]] | None = None,
    kohaerenz: FloatArray | None = None,
    kohaerenz_min: float = 0.9,
) -> ModenErgebnis:
    r"""Fit einer Gruppe an einem Punkt mit Randfällen nach FG-03 6.3.

    Parameters
    ----------
    frequenz_hz : numpy.ndarray
        Achse ``(K,)``.
    y : numpy.ndarray
        Mobilität des Punkts ``(K,)``.
    maske : numpy.ndarray
        Verwendbare Linien ``(K,)`` (Kohärenzmaske und endliche Werte).
    gruppe : Gruppe
        Gruppe mit Fitband.
    spitzen : sequence of Spitze
        Alle Stufe-1-Spitzen (Startwerte).
    zusatz : sequence of tuple of str, optional
        Zusätzliche Kennzeichen je Mode (z. B. ``kohaerenz_niedrig``).
    kohaerenz : numpy.ndarray, optional
        γ² des Punkts ``(K,)``. Linien mit endlichem :math:`\gamma^2 < \gamma^2_\mathrm{min}`
        entfallen; γ² = NaN (nicht prüfbar, z. B. :math:`n_d = 1`) bleibt im Fit mit dem
        Hinweis „Kohärenz nicht prüfbar“ (FG-03 3.2, 6.3, K2-4).
    kohaerenz_min : float
        :math:`\gamma^2_\mathrm{min}`.

    Notes
    -----
    Bei n >= 2 erhält jede Mode ohne ``ausserhalb_band``, deren Rang in der Reihenfolge der
    gefitteten :math:`f_r` (unter den Moden ohne ``ausserhalb_band``) von ihrem Rang bei den
    Startwerten abweicht, das Kennzeichen ``moden_vertauscht`` (Korrektur K-W5-2, Review M2).
    Es schließt die Mode aus Zusammenfassung und Drift aus.
    """
    n = len(gruppe.spitzen)
    extra = list(zusatz) if zusatz is not None else [()] * n
    if GRUPPE_ZU_GROSS in gruppe.kennzeichen:
        return _leer(punkt, gruppe, 0, (GRUPPE_ZU_GROSS,), [])
    band = slice(gruppe.k_von, gruppe.k_bis + 1)
    m = maske[band].copy()
    hinweise: list[str] = []
    if kohaerenz is not None:
        g2 = kohaerenz[band]
        with np.errstate(invalid="ignore"):
            m &= ~(g2 < kohaerenz_min)  # NaN bleibt (K2-4)
        if np.any(np.isnan(g2) & m):
            hinweise.append(HINWEIS_KOHAERENZ_NAN)
    if gewicht is not None:
        m &= np.isfinite(gewicht[band])
    f = frequenz_hz[band][m]
    h = y[band][m]
    if f.shape[0] < 4 * n + 3:
        return _leer(punkt, gruppe, int(f.shape[0]), (ZU_WENIG_LINIEN,), hinweise)
    if not np.linalg.norm(h) > 0:
        return _leer(punkt, gruppe, int(f.shape[0]), (), [*hinweise, HINWEIS_NULL])
    fr0 = [spitzen[i].f_sp_hz for i in gruppe.spitzen]
    z0 = [
        spitzen[i].zeta
        if math.isfinite(spitzen[i].zeta) and spitzen[i].zeta > 0
        else delta_f_hz / (2.0 * spitzen[i].f_sp_hz)
        for i in gruppe.spitzen
    ]
    roh = fit_moden(
        f,
        h,
        fr0,
        z0,
        gewicht=None if gewicht is None else gewicht[band][m],
        max_iter=schwellen2.max_iter,
        tol_rel=schwellen2.tol_rel,
        lambda_max=schwellen2.lambda_max,
    )
    kennzeichen = kennzeichen_fit(
        roh,
        f_band_hz=(float(frequenz_hz[gruppe.k_von]), float(frequenz_hz[gruppe.k_bis])),
        delta_f_hz=delta_f_hz,
        schwellen2=schwellen2,
        m7_grenze_hz=m7_grenze_hz,
        mobilitaetsbezug=mobilitaetsbezug,
    )
    vertauscht = vertauschte_moden(fr0, roh.fr_hz, kennzeichen)
    kennzeichen = tuple(
        (*k, MODEN_VERTAUSCHT) if v else k for k, v in zip(kennzeichen, vertauscht, strict=True)
    )
    return ModenErgebnis(
        punkt=punkt,
        gruppe=gruppe.nummer,
        spitzen=gruppe.spitzen,
        gefittet=True,
        fr_hz=tuple(float(x) for x in roh.fr_hz),
        sd_fr_hz=tuple(float(x) for x in roh.sd_fr_hz),
        zeta=tuple(float(x) for x in roh.zeta),
        sd_zeta_rel=tuple(float(x) for x in roh.sd_zeta_rel),
        breite_fit_hz=tuple(float(2.0 * z * fr) for z, fr in zip(roh.zeta, roh.fr_hz, strict=True)),
        modalkonstante=tuple(complex(x) for x in roh.modalkonstante),
        residuum=roh.residuum,
        rho=roh.rho,
        n_linien=int(f.shape[0]),
        n_moden=n,
        iterationen=roh.iterationen,
        kennzeichen=tuple(
            tuple(dict.fromkeys((*k, *e))) for k, e in zip(kennzeichen, extra, strict=True)
        ),
        hinweise=tuple(hinweise),
    )


def vertauschte_moden(
    fr0_hz: Sequence[float],
    fr_hz: Sequence[float] | npt.ArrayLike,
    kennzeichen: Sequence[Sequence[str]],
) -> list[bool]:
    r"""Moden mit Kennzeichen ``moden_vertauscht`` (FG-03 K3-1).

    Bewertet werden nur Moden ohne ``ausserhalb_band``; eine weggelaufene Partnermode erhält
    das Kennzeichen nicht. Gesetzt wird es für Mode r, wenn

    (a) ihr Rang in :math:`f_r` (unter den Moden ohne ``ausserhalb_band``) vom Rang ihres
        Startwerts :math:`f_{\mathrm{sp},r}` abweicht, oder
    (b) :math:`f_r` einem anderen Startwert der Gruppe echt näher liegt als dem eigenen:
        :math:`|f_r - f_{\mathrm{sp},j}| < |f_r - f_{\mathrm{sp},r}|` für ein j ≠ r (alle
        Startwerte der Gruppe; bei Gleichstand kein Kennzeichen).
    """
    fr = [float(x) for x in np.asarray(fr_hz, dtype=np.float64)]
    start = [float(x) for x in fr0_hz]
    gueltig = [i for i in range(len(fr)) if AUSSERHALB_BAND not in kennzeichen[i]]
    nach_start = sorted(gueltig, key=lambda i: start[i])
    nach_fit = sorted(gueltig, key=lambda i: fr[i])
    vertauscht = [False] * len(fr)
    for soll, ist in zip(nach_start, nach_fit, strict=True):
        if soll != ist:
            vertauscht[soll] = True  # Regel (a)
    for r in gueltig:
        eigen = abs(fr[r] - start[r])
        if any(abs(fr[r] - start[j]) < eigen for j in range(len(start)) if j != r):
            vertauscht[r] = True  # Regel (b)
    return vertauscht


def iqr(werte: npt.ArrayLike) -> float:
    """Interquartilsabstand (75-%- minus 25-%-Quantil, lineare Interpolation)."""
    q75, q25 = np.percentile(np.asarray(werte, dtype=np.float64), [75.0, 25.0])
    return float(q75 - q25)


def staerkste_punkte(betrag: FloatArray, gueltig: BoolArray, anzahl: int) -> tuple[int, ...]:
    """Die ``anzahl`` Punkte mit größtem endlichem Betrag unter den gültigen (absteigend)."""
    kandidaten = np.flatnonzero(gueltig & np.isfinite(betrag))
    reihenfolge = kandidaten[np.argsort(-betrag[kandidaten], kind="stable")]
    return tuple(int(p) for p in reihenfolge[:anzahl])


def fasse_zusammen(
    ergebnisse: Sequence[ModenErgebnis],
    gruppe: Gruppe,
    mode: int,
    spitze: Spitze,
    spitzen_index: int,
    punkte: Sequence[int],
    ausschluss: Sequence[str] = AUSSCHLUSS_ZUSAMMENFASSUNG,
) -> Zusammenfassung:
    """Median und IQR von :math:`f_r` und ζ über ``punkte`` ohne Ausschlusskennzeichen (3.5)."""
    je_punkt = {e.punkt: e for e in ergebnisse if e.gruppe == gruppe.nummer}
    fr: list[float] = []
    zeta: list[float] = []
    sd: list[float] = []
    rho: list[float] = []
    gruende: dict[str, int] = {}
    for p in punkte:
        e = je_punkt.get(p)
        if e is None:
            gruende["nicht gefittet"] = gruende.get("nicht gefittet", 0) + 1
            continue
        treffer = [k for k in e.kennzeichen[mode] if k in ausschluss or not e.gefittet]
        if not e.gefittet and not treffer:
            treffer = list(e.hinweise) or ["kein Fit"]
        if treffer:
            for k in treffer:
                gruende[k] = gruende.get(k, 0) + 1
            continue
        fr.append(e.fr_hz[mode])
        zeta.append(e.zeta[mode])
        sd.append(e.sd_fr_hz[mode])
        rho.append(e.rho)
    hinweise: tuple[str, ...] = ()
    if not fr:
        ursache = ", ".join(f"{k}: {n}" for k, n in sorted(gruende.items()))
        hinweise = (f"{HINWEIS_KEINE_PUNKTE} ({ursache})" if ursache else HINWEIS_KEINE_PUNKTE,)
    return Zusammenfassung(
        spitze=spitzen_index,
        gruppe=gruppe.nummer,
        mode=mode,
        f_sp_hz=spitze.f_sp_hz,
        fr_median_hz=float(np.median(fr)) if fr else math.nan,
        fr_iqr_hz=iqr(fr) if fr else math.nan,
        zeta_median=float(np.median(zeta)) if zeta else math.nan,
        zeta_iqr=iqr(zeta) if zeta else math.nan,
        sd_fr_median_hz=float(np.nanmedian(sd)) if sd and not np.all(np.isnan(sd)) else math.nan,
        rho_median=float(np.median(rho)) if rho else math.nan,
        n_punkte=len(fr),
        punkte=tuple(punkte),
        hinweise=hinweise,
    )


def mobilitaet_des_paars(pa: PaarAuswertung, frf_art: FrfArt) -> ComplexArray:
    r"""H1 des Paars als Mobilität (Akzeleranz: :math:`Y = H/(i\omega)`, FG-02 3.7)."""
    if frf_art == "akzeleranz":
        return akzeleranz_zu_mobilitaet(pa.frf.h1, pa.paar.frequenz_hz)
    return pa.frf.h1


def schaetze_daempfung(
    auswertung: Auswertung,
    paar: tuple[str, str],
    *,
    schwellen2: SchwellenStufe2 | None = None,
    frf_art: FrfArt | None = None,
    spitzen: Sequence[int] | None = None,
    punkte: Sequence[int] | None = None,
) -> ModenfitErgebnis:
    """B-1 für ein Kanalpaar einer Stufe-1-Auswertung (FG-03 3.2 bis 3.5, E1–E3).

    Parameters
    ----------
    auswertung : Auswertung
        Ergebnis von Stufe 1 (wird nur gelesen).
    paar : tuple of str
        ``(antwort, referenz)`` mit Kreuzspektrum.
    schwellen2 : SchwellenStufe2, optional
        Parameter (Voreinstellungen FG-03 E6).
    frf_art : {"mobilitaet", "akzeleranz", "andere"}, optional
        Art der FRF; ohne Angabe aus den Einheiten.
    spitzen : sequence of int, optional
        Nur die Gruppen dieser Stufe-1-Spitzen fitten; ``None`` = alle.
    punkte : sequence of int, optional
        An genau diesen Punkten fitten (gültige Punkte); ``None`` = nach ``punktauswahl``.

    Returns
    -------
    ModenfitErgebnis

    Raises
    ------
    KeyError
        Wenn das Paar fehlt.
    ValueError
        Bei ungültigen Spitzen- oder Punktindizes.
    """
    schwellen2 = schwellen2 if schwellen2 is not None else SchwellenStufe2()
    schwellen: Schwellen = auswertung.schwellen
    if paar not in auswertung.paare:
        raise KeyError(f"kein Kanalpaar {paar[0]}/{paar[1]} in der Auswertung")
    pa = auswertung.paare[paar]
    art = (
        frf_art
        if frf_art is not None
        else frf_art_aus_einheiten(pa.paar.einheit_antwort, pa.paar.einheit_referenz)
    )
    f = pa.paar.frequenz_hz
    df = auswertung.daten.delta_f_hz
    y = mobilitaet_des_paars(pa, art)
    einheit = f"(m/s)/{pa.paar.einheit_referenz}" if art == "akzeleranz" else pa.frf.einheit
    sp = pa.spitzen.spitzen
    assert pa.mittel_h1.mittel_betrag is not None
    gruppen = bilde_gruppen(
        sp,
        pa.mittel_h1.mittel_betrag,
        df,
        schwellen2=schwellen2,
        nachbar_faktor=schwellen.nachbar_faktor,
    )
    if spitzen is None:
        auswahl = list(gruppen)
    else:
        if any(not 0 <= i < len(sp) for i in spitzen):
            raise ValueError(f"Spitzenindex außerhalb 0..{len(sp) - 1}: {list(spitzen)}")
        auswahl = [g for g in gruppen if set(g.spitzen) & set(spitzen)]
    gueltig = pa.paar.gueltig
    betrag_h1 = np.abs(pa.frf.h1)
    hinweise: list[str] = []
    if art == "andere":
        hinweise.append(HINWEIS_VIB_REF2)
    gewicht: FloatArray | None = None
    if schwellen2.gewichtung == "fehler":
        with np.errstate(divide="ignore", invalid="ignore"):
            gewicht = pa.frf.gewicht / np.abs(y) ** 2
        gewicht = np.where(np.isfinite(gewicht), gewicht, np.nan)
        hinweise.append(HINWEIS_GEWICHT)
    maske = np.isfinite(y)  # Kohärenzmaske in fit_punkt (K2-4: γ² = NaN bleibt)
    if punkte is not None:
        p_anzahl = gueltig.shape[0]
        if any(not 0 <= p < p_anzahl for p in punkte):
            raise ValueError(f"Punktindex außerhalb 0..{p_anzahl - 1}: {list(punkte)}")
    ergebnisse: list[ModenErgebnis] = []
    zusammen: list[Zusammenfassung] = []
    m7 = auswertung.annahmen.m7_grenze_hz
    kandidat = gueltig.copy()
    if punkte is not None:
        kandidat &= np.isin(np.arange(gueltig.shape[0]), np.asarray(list(punkte), dtype=np.int64))
    for g in auswahl:
        staerkste = {
            i: staerkste_punkte(betrag_h1[:, sp[i].k], kandidat, schwellen2.n_punkte)
            for i in g.spitzen
        }
        if punkte is not None:
            fit_punkte = [int(p) for p in np.flatnonzero(kandidat)]
        elif schwellen2.punktauswahl == "alle":
            fit_punkte = [int(p) for p in np.flatnonzero(gueltig)]
        else:
            fit_punkte = sorted({p for s in staerkste.values() for p in s})
        g_ergebnisse: list[ModenErgebnis] = []
        for p in fit_punkte:
            zusatz = []
            for i in g.spitzen:
                niedrig = KOHAERENZ_NIEDRIG in sp[i].kennzeichen or bool(
                    pa.frf.kohaerenz[p, sp[i].k] < schwellen.kohaerenz_min
                )
                zusatz.append((KOHAERENZ_NIEDRIG,) if niedrig else ())
            g_ergebnisse.append(
                fit_punkt(
                    f,
                    y[p],
                    maske[p],
                    g,
                    sp,
                    punkt=p,
                    delta_f_hz=df,
                    schwellen2=schwellen2,
                    gewicht=None if gewicht is None else gewicht[p],
                    m7_grenze_hz=m7,
                    mobilitaetsbezug=art != "andere",
                    zusatz=zusatz,
                    kohaerenz=pa.frf.kohaerenz[p],
                    kohaerenz_min=schwellen.kohaerenz_min,
                )
            )
        ergebnisse.extend(g_ergebnisse)
        for mode, i in enumerate(g.spitzen):
            zusammen.append(fasse_zusammen(g_ergebnisse, g, mode, sp[i], i, staerkste[i]))
    return ModenfitErgebnis(
        antwort=paar[0],
        referenz=paar[1],
        frf_art=art,
        einheit_fit=einheit,
        gruppen=gruppen,
        ergebnisse=tuple(ergebnisse),
        zusammenfassung=tuple(zusammen),
        schwellen2=schwellen2,
        hinweise=tuple(hinweise),
        grenzen=(GRENZE_VERFAHREN, GRENZE_LECKAGE),
        annahmen=auswertung.annahmen_liste,
    )
