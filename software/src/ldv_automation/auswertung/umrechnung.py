r"""Umrechnung Weg/Schnelle/Beschleunigung je Linie (FG-02 3.7, B-10).

Mit :math:`\omega_k = 2\pi f_k` in rad/s und Zeitabhängigkeit :math:`e^{+i\omega t}` [A]:

.. math::

    \hat d = \frac{\hat v}{i\omega_k}\ [\mathrm m],\qquad
    \hat a = i\omega_k\,\hat v\ [\mathrm{m/s^2}],\qquad
    \mathrm{AP}_d = \mathrm{AP}_v/\omega_k^2,\qquad \mathrm{AP}_a = \omega_k^2\,\mathrm{AP}_v.

Für Übertragungsfunktionen: Rezeptanz = Mobilität/(iω) [m/N], Akzeleranz = iω·Mobilität
[(m/s²)/N]. Der Weg eilt der Schnelle um π/2 nach, die Beschleunigung um π/2 vor. Bei
:math:`\omega_k = 0` (nur bei :math:`k_0 = 0`) ist der Weg NaN. Band-Effektivwerte
umgerechneter Größen werden aus den umgerechneten Linien gebildet (FG-02 3.7).

Die Frequenzachse gehört zur letzten Achse der Werte (``(..., K)``).
"""

from __future__ import annotations

import numpy as np
import numpy.typing as npt

from .daten import ComplexArray, FloatArray

_NAN_C = complex(np.nan, np.nan)


def _omega(werte: npt.NDArray[np.generic], frequenz_hz: FloatArray) -> FloatArray:
    if frequenz_hz.ndim != 1 or werte.shape[-1] != frequenz_hz.shape[0]:
        raise ValueError(
            f"Frequenzachse {frequenz_hz.shape} passt nicht zur letzten Achse {werte.shape}"
        )
    omega: FloatArray = 2.0 * np.pi * frequenz_hz
    return omega


def durch_i_omega(werte: npt.ArrayLike, frequenz_hz: FloatArray) -> ComplexArray:
    r""":math:`X/(i\omega)` (Schnelle → Weg, Mobilität → Rezeptanz); ω = 0 → NaN."""
    x = np.asarray(werte, dtype=np.complex128)
    w = _omega(x, frequenz_hz)
    with np.errstate(divide="ignore", invalid="ignore"):
        ergebnis = np.where(w != 0, x / (1j * np.where(w != 0, w, 1.0)), _NAN_C)
    return ergebnis.astype(np.complex128)


def mal_i_omega(werte: npt.ArrayLike, frequenz_hz: FloatArray) -> ComplexArray:
    r""":math:`i\omega X` (Schnelle → Beschleunigung, Mobilität → Akzeleranz)."""
    x = np.asarray(werte, dtype=np.complex128)
    w = _omega(x, frequenz_hz)
    ergebnis: ComplexArray = (1j * w * x).astype(np.complex128)
    return ergebnis


def schnelle_zu_weg(schnelle_m_s: npt.ArrayLike, frequenz_hz: FloatArray) -> ComplexArray:
    """Weg in m aus Schnelle in m/s."""
    return durch_i_omega(schnelle_m_s, frequenz_hz)


def schnelle_zu_beschleunigung(
    schnelle_m_s: npt.ArrayLike, frequenz_hz: FloatArray
) -> ComplexArray:
    """Beschleunigung in m/s² aus Schnelle in m/s."""
    return mal_i_omega(schnelle_m_s, frequenz_hz)


def mobilitaet_zu_rezeptanz(mobilitaet: npt.ArrayLike, frequenz_hz: FloatArray) -> ComplexArray:
    """Rezeptanz in m/N aus Mobilität in (m/s)/N."""
    return durch_i_omega(mobilitaet, frequenz_hz)


def mobilitaet_zu_akzeleranz(mobilitaet: npt.ArrayLike, frequenz_hz: FloatArray) -> ComplexArray:
    """Akzeleranz in (m/s²)/N aus Mobilität in (m/s)/N."""
    return mal_i_omega(mobilitaet, frequenz_hz)


def akzeleranz_zu_mobilitaet(akzeleranz: npt.ArrayLike, frequenz_hz: FloatArray) -> ComplexArray:
    """Mobilität in (m/s)/N aus Akzeleranz in (m/s²)/N (für P-08)."""
    return durch_i_omega(akzeleranz, frequenz_hz)


def ap_schnelle_zu_weg(ap_v: npt.ArrayLike, frequenz_hz: FloatArray) -> FloatArray:
    r""":math:`\mathrm{AP}_d = \mathrm{AP}_v/\omega^2` in m²; ω = 0 → NaN."""
    x = np.asarray(ap_v, dtype=np.float64)
    w = _omega(x, frequenz_hz)
    with np.errstate(divide="ignore", invalid="ignore"):
        ergebnis: FloatArray = np.where(w != 0, x / np.where(w != 0, w, 1.0) ** 2, np.nan)
    return ergebnis


def ap_schnelle_zu_beschleunigung(ap_v: npt.ArrayLike, frequenz_hz: FloatArray) -> FloatArray:
    r""":math:`\mathrm{AP}_a = \omega^2\,\mathrm{AP}_v` in (m/s²)²."""
    x = np.asarray(ap_v, dtype=np.float64)
    w = _omega(x, frequenz_hz)
    ergebnis: FloatArray = w**2 * x
    return ergebnis
