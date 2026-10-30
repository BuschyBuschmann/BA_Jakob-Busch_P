r"""Betriebsschwingform bei gewählter Frequenz (FG-02 3.6, A-5, R-052).

- Linienwahl :math:`k^\ast = \arg\min_k |f_k - f_\mathrm{wahl}|`; bei Gleichstand die
  kleinere Linie. Außerhalb :math:`[f_0 - \Delta f/2,\ f_{K-1} + \Delta f/2]` folgt
  ``ValueError``.
- Komplexe Amplitude je Punkt und Komponente: ``quelle="cph"`` (Voreinstellung)
  :math:`\hat v = \mathrm{CPH}_{k^\ast}` in m/s (Spitzenwert) oder ``quelle="h1"``
  :math:`\hat v = H_{1,k^\ast}` in (m/s)/N. Phase bezogen auf die Referenz.
- Momentanwert :math:`u(\theta) = \mathrm{Re}\{\hat v\,e^{i\theta}\}`.
- Ohne Referenz oder Trigger: nur :math:`\sqrt{\mathrm{AP}}` als Betrag mit
  ``phase_gueltig = False``; eine Animation wird abgelehnt (``ValueError``, Entscheidung
  zu RF-3D7).
- 3D-Kennwerte [A, W3 2.4]: ``betrag_3d_psv`` = :math:`\sqrt{\sum|\hat v_c|^2}`,
  ``auslenkung_max`` = :math:`\sqrt{\tfrac12(\sum|\hat v_c|^2 + |\sum\hat v_c^2|)}`,
  ``auslenkung_min`` = :math:`\sqrt{\max(0, \tfrac12(\sum|\hat v_c|^2 - |\sum\hat v_c^2|))}`.

Das globale Vorzeichen hängt von :math:`s_a s_b` ab (M8), die Form nicht.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

import numpy as np
import numpy.typing as npt

from .annahmen import AnnahmeEintrag, Annahmen
from .daten import ComplexArray, FloatArray

Quelle = Literal["cph", "h1", "leistung"]

#: Relative Toleranz der Gleichstandsprüfung bei der Linienwahl (bezogen auf Δf).
GLEICHSTAND_RTOL = 1e-9


def waehle_linie(frequenz_hz: FloatArray, f_wahl_hz: float, delta_f_hz: float | None = None) -> int:
    r"""Index der nächsten Linie; Gleichstand → kleinere Linie (FG-02 3.6, RF-3D6).

    Raises
    ------
    ValueError
        Wenn ``f_wahl_hz`` außerhalb :math:`[f_0 - \Delta f/2, f_{K-1} + \Delta f/2]` liegt.
    """
    if frequenz_hz.ndim != 1 or frequenz_hz.size < 1:
        raise ValueError("Frequenzachse (K,) mit K >= 1 erwartet")
    if delta_f_hz is None:
        if frequenz_hz.size < 2:
            raise ValueError("delta_f_hz nötig bei nur einer Linie")
        delta_f_hz = float((frequenz_hz[-1] - frequenz_hz[0]) / (frequenz_hz.size - 1))
    unten = frequenz_hz[0] - delta_f_hz / 2.0
    oben = frequenz_hz[-1] + delta_f_hz / 2.0
    if not (np.isfinite(f_wahl_hz) and unten <= f_wahl_hz <= oben):
        raise ValueError(
            f"f_wahl = {f_wahl_hz} Hz liegt außerhalb [{unten:g}, {oben:g}] Hz der Achse"
        )
    abstand = np.abs(frequenz_hz - f_wahl_hz)
    kandidaten = np.flatnonzero(abstand <= abstand.min() + GLEICHSTAND_RTOL * delta_f_hz)
    return int(kandidaten[0])


def ellipse_kennwerte(amplitude: npt.ArrayLike) -> tuple[FloatArray, FloatArray, FloatArray]:
    """3D-Kennwerte einer komplexen Amplitude ``(..., 3)`` (FG-02 3.6).

    Returns
    -------
    betrag_3d_psv, auslenkung_max, auslenkung_min : numpy.ndarray
        Form ``(...)``. Es gilt min <= max <= betrag_3d_psv.
    """
    a = np.asarray(amplitude, dtype=np.complex128)
    if a.shape[-1] != 3:
        raise ValueError(f"letzte Achse muss die 3 Komponenten X, Y, Z sein: {a.shape}")
    summe_betrag = np.sum(np.abs(a) ** 2, axis=-1)
    betrag_summe = np.abs(np.sum(a**2, axis=-1))
    psv: FloatArray = np.sqrt(summe_betrag)
    maximum: FloatArray = np.sqrt(0.5 * (summe_betrag + betrag_summe))
    minimum: FloatArray = np.sqrt(np.maximum(0.0, 0.5 * (summe_betrag - betrag_summe)))
    return psv, maximum, minimum


def momentanwert(amplitude: npt.ArrayLike, theta_rad: npt.ArrayLike) -> FloatArray:
    r""":math:`u(\theta) = \mathrm{Re}\{\hat v\,e^{i\theta}\}`.

    Parameters
    ----------
    amplitude : array_like
        Komplexe Amplitude beliebiger Form.
    theta_rad : float or array_like
        Phasenwinkel :math:`\theta = \omega t` in rad; ein Feld wird als neue letzte Achse
        angehängt.
    """
    a = np.asarray(amplitude, dtype=np.complex128)
    theta = np.asarray(theta_rad, dtype=np.float64)
    if theta.ndim == 0:
        ergebnis: FloatArray = np.real(a * np.exp(1j * theta))
        return ergebnis
    ergebnis = np.real(a[..., None] * np.exp(1j * theta))
    return ergebnis


@dataclass(frozen=True, kw_only=True, eq=False)
class Schwingform:
    r"""Betriebsschwingform (FG-02 3.6, Datenvertrag 6.2).

    Attributes
    ----------
    f_wahl_hz, f_hz : float
        Gewählte Frequenz und Frequenz der Linie :math:`f_{k^\ast}` in Hz.
    linie : int
        0-basierter Linienindex :math:`k^\ast`.
    quelle : {"cph", "h1", "leistung"}
        Herkunft der Amplitude (``"leistung"``: √AP ohne Phase).
    referenz : str or None
        Bezugskanal der Phase.
    einheit : str
        m/s bzw. (m/s)/N (Einheit der Antwort bzw. FRF).
    amplitude : numpy.ndarray or None
        ``(P, 3)`` complex; ``None`` ohne gültige Phase.
    betrag : numpy.ndarray
        ``(P, 3)`` Beträge je Komponente.
    betrag_3d_psv, auslenkung_max, auslenkung_min : numpy.ndarray
        ``(P,)``; ohne Phase sind max/min NaN.
    phase_gueltig : bool
        ``False`` ohne Referenz oder Trigger.
    hinweise : tuple of str
        Hinweise zur Ausgabe.
    annahmen : tuple of AnnahmeEintrag
        Geltende Annahmen (P-11).
    """

    f_wahl_hz: float
    f_hz: float
    linie: int
    quelle: Quelle
    referenz: str | None
    einheit: str
    amplitude: ComplexArray | None
    betrag: FloatArray
    betrag_3d_psv: FloatArray
    auslenkung_max: FloatArray
    auslenkung_min: FloatArray
    phase_gueltig: bool
    hinweise: tuple[str, ...]
    annahmen: tuple[AnnahmeEintrag, ...]

    def momentanwert(self, theta_rad: npt.ArrayLike) -> FloatArray:
        """Momentanwert ``(P, 3)`` bzw. ``(P, 3, n)``.

        Raises
        ------
        ValueError
            Ohne gültige Phase (``phase_gueltig = False``), RF-3D7.
        """
        if not self.phase_gueltig or self.amplitude is None:
            raise ValueError("ohne Referenz oder Trigger keine Animation mit Vorzeichen (R-052)")
        return momentanwert(self.amplitude, theta_rad)


def betriebsschwingform(
    frequenz_hz: FloatArray,
    f_wahl_hz: float,
    *,
    amplitude_3d: ComplexArray | None = None,
    leistung_3d: FloatArray | None = None,
    phase_gueltig: bool = True,
    quelle: Quelle = "cph",
    referenz: str | None = None,
    einheit: str = "",
    delta_f_hz: float | None = None,
    annahmen: Annahmen | None = None,
) -> Schwingform:
    """Betriebsschwingform bei ``f_wahl_hz`` (FG-02 3.6).

    Parameters
    ----------
    frequenz_hz : numpy.ndarray
        Achse ``(K,)``.
    f_wahl_hz : float
        Gewählte Frequenz in Hz.
    amplitude_3d : numpy.ndarray, optional
        ``(P, 3, K)`` complex (CPH oder H1 je Komponente X, Y, Z); nötig mit Phase.
    leistung_3d : numpy.ndarray, optional
        ``(P, 3, K)`` √AP je Komponente; nötig ohne Phase.
    phase_gueltig : bool
        Referenz oder Trigger vorhanden.
    quelle : {"cph", "h1"}
        Herkunft der Amplitude (nur mit Phase).
    referenz, einheit : str
        Beschriftung.
    delta_f_hz : float, optional
        Linienabstand für die Bereichsgrenze.
    annahmen : Annahmen, optional
        Für die Annahmenliste.

    Raises
    ------
    ValueError
        Bei fehlenden Eingaben, falscher Form oder ``f_wahl_hz`` außerhalb der Achse.
    """
    annahmen = annahmen if annahmen is not None else Annahmen()
    k = waehle_linie(frequenz_hz, f_wahl_hz, delta_f_hz)
    hinweise: list[str] = []
    if phase_gueltig:
        if (
            amplitude_3d is None
            or amplitude_3d.ndim != 3
            or amplitude_3d.shape[1:]
            != (
                3,
                frequenz_hz.size,
            )
        ):
            raise ValueError("amplitude_3d (P, 3, K) nötig, wenn die Phase gültig ist")
        werte_k: ComplexArray = amplitude_3d[:, :, k].astype(np.complex128)
        amplitude: ComplexArray | None = werte_k
        psv, maximum, minimum = ellipse_kennwerte(werte_k)
        betrag: FloatArray = np.abs(werte_k)
        quelle_aus: Quelle = quelle
    else:
        if (
            leistung_3d is None
            or leistung_3d.ndim != 3
            or leistung_3d.shape[1:]
            != (
                3,
                frequenz_hz.size,
            )
        ):
            raise ValueError("leistung_3d (P, 3, K) nötig, wenn die Phase ungültig ist")
        amplitude = None
        betrag = leistung_3d[:, :, k].astype(np.float64)
        psv = np.sqrt(np.sum(betrag**2, axis=-1))
        maximum = np.full(betrag.shape[0], np.nan)
        minimum = np.full(betrag.shape[0], np.nan)
        quelle_aus = "leistung"
        hinweise.append("ohne Referenz oder Trigger: nur Betrag √AP, keine Phase, keine Animation")
    return Schwingform(
        f_wahl_hz=float(f_wahl_hz),
        f_hz=float(frequenz_hz[k]),
        linie=k,
        quelle=quelle_aus,
        referenz=referenz if phase_gueltig else None,
        einheit=einheit,
        amplitude=amplitude,
        betrag=betrag,
        betrag_3d_psv=psv,
        auslenkung_max=maximum,
        auslenkung_min=minimum,
        phase_gueltig=phase_gueltig,
        hinweise=tuple(hinweise),
        annahmen=annahmen.eintraege(),
    )
