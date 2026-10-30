r"""Band-Effektivwerte (FG-02 3.8, A-7, R-053).

Bandzugehörigkeit (Annahme M10, Voreinstellung „geschlossen“): Linie k gehört zum Band
:math:`[f_u, f_o]`, wenn :math:`f_u - 10^{-6}\Delta f \le f_k \le f_o + 10^{-6}\Delta f`.
Die Variante „offen“ (nur für den Prüfschritt M10) zählt keine Grenzlinie:
:math:`f_u + 10^{-6}\Delta f < f_k < f_o - 10^{-6}\Delta f`.

=============  =============================================================  ==============
Ausgabe        Formel                                                         Einheit
=============  =============================================================  ==============
``rms``        :math:`\sqrt{\sum |\hat X_k|^2/(2W_\mathrm{RBW})}` bzw.        [a] effektiv
               :math:`\sqrt{\sum \mathrm{AP}_k/(2W_\mathrm{RBW})}`
``rms_psv``    :math:`\sqrt{\sum |\hat X_k|^2/2}` (CPH, ABS) bzw.                wie PSV
               :math:`\sum\mathrm{AP}_k/2` (AP, quadratischer Mittelwert)
``bandnorm``   :math:`\sqrt{\sum |H_k|^2/2}` (FRF; kein physikalischer          [a]/[b]
               Effektivwert)
=============  =============================================================  ==============

Quelle: Polytec Theory Manual Gl. 3.17 über I2 [H]; ``rms_psv`` und ``bandnorm`` an der
Datei bestätigt (W2, FG-02 [D]). :math:`W_\mathrm{RBW} = N\sum w_n^2/(\sum w_n)^2`
(Rechteck 1, Hann 1,5) ist Annahme M5. Exakt (Parseval) nur für Signalanteile auf Linien.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

import numpy as np
import numpy.typing as npt

from .annahmen import AnnahmeEintrag, Annahmen, Bandregel
from .daten import BoolArray, FloatArray, einheit_quadrat

HINWEIS_LEER = "leeres Band"
HINWEIS_ABGESCHNITTEN = "Band abgeschnitten"
HINWEIS_BANDNORM = "Bandnorm der FRF: kein physikalischer Effektivwert"

#: Reserve der Bandgrenzen relativ zu Δf (FG-02 3.8).
GRENZ_RESERVE = 1e-6

Bandgroesse = Literal["amplitude", "ap", "frf"]


@dataclass(frozen=True, kw_only=True, eq=False)
class Bandwert:
    """Ergebnis eines Bands.

    Attributes
    ----------
    f_u_hz, f_o_hz : float
        Bandgrenzen in Hz.
    groesse : {"amplitude", "ap", "frf"}
        Art der Eingangsgröße.
    bezug : str
        Beschriftung (Kanal, Paar, „Punktmittel“).
    einheit : str
        Einheit der Amplitude [a] bzw. der FRF [a]/[b]; bei AP die Kanaleinheit [a] (nicht
        [a]²). Einheit und Art je Ausgabe liefert :meth:`kennzeichen`.
    rms : numpy.ndarray or None
        Physikalischer Effektivwert (nicht für FRF); Form wie Eingang ohne letzte Achse.
    rms_psv : numpy.ndarray or None
        PSV-konformer Bandwert (nicht für FRF).
    bandnorm : numpy.ndarray or None
        Nur für FRF.
    n_linien : int
        Anzahl der Linien im Band.
    w_rbw : float
        Verwendeter Bandbreitenfaktor (M5).
    hinweise : tuple of str
        „leeres Band“, „Band abgeschnitten“, Kennzeichnung der Bandnorm.
    annahmen : tuple of AnnahmeEintrag
        Geltende Annahmen (P-11).
    """

    f_u_hz: float
    f_o_hz: float
    groesse: Bandgroesse
    bezug: str
    einheit: str
    rms: FloatArray | None
    rms_psv: FloatArray | None
    bandnorm: FloatArray | None
    n_linien: int
    w_rbw: float
    hinweise: tuple[str, ...]
    annahmen: tuple[AnnahmeEintrag, ...]

    def kennzeichen(self) -> dict[str, dict[str, str]]:
        """Art (Effektivwert, quadratischer Mittelwert, Bandnorm) und Einheit je Ausgabe.

        FG-02 Abschnitt 5, Punkt 5. Grundlage aller Bandwerte sind einseitige Spektren mit
        Spitzenwerten (M4); die Ausgaben ``rms``/``rms_psv`` sind daraus Effektivwerte.
        """
        e = self.einheit
        if self.groesse == "frf":
            return {"bandnorm": {"art": "Bandnorm √(Σ|H|²/2), kein Effektivwert", "einheit": e}}
        psv = (
            {"art": "quadratischer Mittelwert ΣAP/2 (PSV)", "einheit": einheit_quadrat(e)}
            if self.groesse == "ap"
            else {"art": "Effektivwert √(Σ|X|²/2) (PSV, ohne W_RBW)", "einheit": e}
        )
        return {
            "rms": {"art": f"Effektivwert mit W_RBW = {self.w_rbw:g}", "einheit": e},
            "rms_psv": psv,
        }


def w_rbw_aus_fenster(fenster: npt.ArrayLike) -> float:
    r""":math:`W_\mathrm{RBW} = N\sum w_n^2/(\sum w_n)^2` (FG-02 3.8; Rechteck 1, Hann 1,5)."""
    w = np.asarray(fenster, dtype=np.float64)
    if w.ndim != 1 or w.size == 0 or np.sum(w) == 0:
        raise ValueError("Fenster muss ein nicht leeres 1D-Feld mit Summe != 0 sein")
    return float(w.size * np.sum(w**2) / np.sum(w) ** 2)


def _delta_f(frequenz_hz: FloatArray, delta_f_hz: float | None) -> float:
    if delta_f_hz is not None:
        return float(delta_f_hz)
    if frequenz_hz.size < 2:
        raise ValueError("delta_f_hz nötig bei weniger als zwei Linien")
    return float((frequenz_hz[-1] - frequenz_hz[0]) / (frequenz_hz.size - 1))


def band_linien(
    frequenz_hz: FloatArray,
    f_u_hz: float,
    f_o_hz: float,
    *,
    delta_f_hz: float | None = None,
    regel: Bandregel = "geschlossen",
) -> tuple[BoolArray, tuple[str, ...]]:
    """Maske der Linien im Band und Hinweise (FG-02 3.8, M10).

    Raises
    ------
    ValueError
        Bei :math:`f_u > f_o`.
    """
    if not f_u_hz <= f_o_hz:
        raise ValueError(f"Bandgrenzen: f_u = {f_u_hz} Hz > f_o = {f_o_hz} Hz")
    reserve = GRENZ_RESERVE * _delta_f(frequenz_hz, delta_f_hz)
    if regel == "geschlossen":
        maske = (frequenz_hz >= f_u_hz - reserve) & (frequenz_hz <= f_o_hz + reserve)
    elif regel == "offen":
        maske = (frequenz_hz > f_u_hz + reserve) & (frequenz_hz < f_o_hz - reserve)
    else:
        raise ValueError(f"unbekannte Bandregel {regel!r}")
    hinweise: list[str] = []
    if not np.any(maske):
        hinweise.append(HINWEIS_LEER)
    elif f_u_hz < frequenz_hz[0] - reserve or f_o_hz > frequenz_hz[-1] + reserve:
        hinweise.append(HINWEIS_ABGESCHNITTEN)
    return maske, tuple(hinweise)


def _summe(quadrate: npt.NDArray[np.float64], maske: BoolArray) -> FloatArray:
    if quadrate.shape[-1] != maske.shape[0]:
        raise ValueError(f"letzte Achse {quadrate.shape} passt nicht zur Achse ({maske.shape[0]},)")
    if not np.any(maske):
        return np.full(quadrate.shape[:-1], np.nan)
    ergebnis: FloatArray = np.sum(quadrate[..., maske], axis=-1)
    return ergebnis


def _band(
    werte: npt.ArrayLike,
    frequenz_hz: FloatArray,
    f_u_hz: float,
    f_o_hz: float,
    groesse: Bandgroesse,
    *,
    annahmen: Annahmen | None,
    delta_f_hz: float | None,
    bezug: str,
    einheit: str,
) -> Bandwert:
    annahmen = annahmen if annahmen is not None else Annahmen()
    x = np.asarray(werte)
    maske, hinweise = band_linien(
        frequenz_hz, f_u_hz, f_o_hz, delta_f_hz=delta_f_hz, regel=annahmen.bandregel
    )
    w_rbw = annahmen.w_rbw
    rms = rms_psv = bandnorm = None
    if groesse == "ap":
        if np.iscomplexobj(x):
            raise TypeError("AP muss reell sein")
        summe = _summe(x.astype(np.float64), maske)
        rms = np.sqrt(summe / (2.0 * w_rbw))
        rms_psv = summe / 2.0
    else:
        summe = _summe((np.abs(x) ** 2).astype(np.float64), maske)
        if groesse == "frf":
            bandnorm = np.sqrt(summe / 2.0)
            hinweise = (*hinweise, HINWEIS_BANDNORM)
        else:
            rms = np.sqrt(summe / (2.0 * w_rbw))
            rms_psv = np.sqrt(summe / 2.0)
    return Bandwert(
        f_u_hz=float(f_u_hz),
        f_o_hz=float(f_o_hz),
        groesse=groesse,
        bezug=bezug,
        einheit=einheit,
        rms=rms,
        rms_psv=rms_psv,
        bandnorm=bandnorm,
        n_linien=int(np.count_nonzero(maske)),
        w_rbw=w_rbw,
        hinweise=hinweise,
        annahmen=annahmen.eintraege(),
    )


def band_amplitude(
    spektrum: npt.ArrayLike,
    frequenz_hz: FloatArray,
    f_u_hz: float,
    f_o_hz: float,
    *,
    annahmen: Annahmen | None = None,
    delta_f_hz: float | None = None,
    bezug: str = "",
    einheit: str = "",
) -> Bandwert:
    r"""Band-Effektivwert eines Amplitudenspektrums (CPH, ABS, √AP; Spitzenwerte).

    Parameters
    ----------
    spektrum : array_like
        ``(..., K)``, reell oder komplex, Spitzenwert.
    frequenz_hz : numpy.ndarray
        Achse ``(K,)``.
    f_u_hz, f_o_hz : float
        Bandgrenzen in Hz.
    annahmen : Annahmen, optional
        :math:`W_\mathrm{RBW}` (M5) und Bandregel (M10).
    delta_f_hz : float, optional
        Linienabstand; Voreinstellung aus der Achse.
    bezug, einheit : str
        Beschriftung.

    Returns
    -------
    Bandwert
        ``rms`` und ``rms_psv``; leeres Band → NaN mit Hinweis.
    """
    return _band(
        spektrum,
        frequenz_hz,
        f_u_hz,
        f_o_hz,
        "amplitude",
        annahmen=annahmen,
        delta_f_hz=delta_f_hz,
        bezug=bezug,
        einheit=einheit,
    )


def band_ap(
    ap: npt.ArrayLike,
    frequenz_hz: FloatArray,
    f_u_hz: float,
    f_o_hz: float,
    *,
    annahmen: Annahmen | None = None,
    delta_f_hz: float | None = None,
    bezug: str = "",
    einheit: str = "",
) -> Bandwert:
    """Band-Effektivwert aus einem Autospektrum: ``rms`` = √(ΣAP/(2W)), ``rms_psv`` = ΣAP/2."""
    return _band(
        ap,
        frequenz_hz,
        f_u_hz,
        f_o_hz,
        "ap",
        annahmen=annahmen,
        delta_f_hz=delta_f_hz,
        bezug=bezug,
        einheit=einheit,
    )


def band_frf(
    frf: npt.ArrayLike,
    frequenz_hz: FloatArray,
    f_u_hz: float,
    f_o_hz: float,
    *,
    annahmen: Annahmen | None = None,
    delta_f_hz: float | None = None,
    bezug: str = "",
    einheit: str = "",
) -> Bandwert:
    r"""Bandnorm einer FRF :math:`\sqrt{\sum|H_k|^2/2}` (kein physikalischer Effektivwert)."""
    return _band(
        frf,
        frequenz_hz,
        f_u_hz,
        f_o_hz,
        "frf",
        annahmen=annahmen,
        delta_f_hz=delta_f_hz,
        bezug=bezug,
        einheit=einheit,
    )
