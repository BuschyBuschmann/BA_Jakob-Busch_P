r"""Punktmittel (FG-02 3.2, A-3, B-9, R-050).

Über die Menge :math:`\mathcal P` der gültigen Punkte (Annahme M6) und je Linie:

.. math::

    M^\mathrm{Betrag}_k = \frac{1}{n}\sum_{p} |X_{pk}|,\qquad
    M^\mathrm{quadr}_k = \sqrt{\frac{1}{n}\sum_{p} |X_{pk}|^2}.

``mittel_betrag`` ist PSV-konform (``AVGSEQ[ABS[…]]``) für CPH, ABS, |H1|, |H2|, |CP|;
``mittel_quadratisch`` zusätzlich. Für AP und γ² bildet PSV das arithmetische Mittel
(``AVGSEQ[AVG[AP]]``, ``AVGSEQ[COH]``): :func:`punktmittel_arithmetisch`. Es gilt
:math:`M^\mathrm{quadr}(\sqrt{\mathrm{AP}}) = \sqrt{\overline{\mathrm{AP}}}`.

Alle Gewichte sind gleich (flächengewichtete Mittel: Stufe 2). NaN-Linien eines Punkts
zählen nicht mit; je Linie wird die Anzahl ``n_mittel`` ausgegeben, bei ``n = 0`` ist das
Ergebnis NaN. Ein komplexes Punktmittel gehört nicht zu Stufe 1.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import numpy.typing as npt

from .annahmen import AnnahmeEintrag, Annahmen
from .daten import BoolArray, FloatArray, IntArray


@dataclass(frozen=True, kw_only=True, eq=False)
class Punktmittel:
    r"""Ergebnis eines Punktmittels.

    Attributes
    ----------
    groesse : str
        Bezeichnung der gemittelten Größe, z. B. ``"|H1| Vib Z/Ref1"``.
    einheit : str
        Einheit wie Eingang.
    mittel_betrag : numpy.ndarray or None
        :math:`M^\mathrm{Betrag}`, ``(K,)``.
    mittel_quadratisch : numpy.ndarray or None
        :math:`M^\mathrm{quadr}`, ``(K,)``.
    mittel_arithmetisch : numpy.ndarray or None
        Arithmetisches Mittel (AP, γ²), ``(K,)``.
    n_mittel : numpy.ndarray
        Anzahl der beitragenden Punkte je Linie, ``(K,)``.
    annahmen : tuple of AnnahmeEintrag
        Geltende Annahmen (P-11).
    """

    groesse: str
    einheit: str
    mittel_betrag: FloatArray | None
    mittel_quadratisch: FloatArray | None
    mittel_arithmetisch: FloatArray | None
    n_mittel: IntArray
    annahmen: tuple[AnnahmeEintrag, ...]


def _auswahl(werte: npt.NDArray[np.generic], gueltig: BoolArray | None) -> npt.NDArray[np.generic]:
    if werte.ndim != 2:
        raise ValueError(f"Punktmittel erwartet (P, K): {werte.shape}")
    if gueltig is None:
        return werte
    if gueltig.shape != (werte.shape[0],):
        raise ValueError(f"gueltig hat Form {gueltig.shape}, erwartet ({werte.shape[0]},)")
    return werte[gueltig]


def _mittel(summand: FloatArray) -> tuple[FloatArray, IntArray]:
    vorhanden = ~np.isnan(summand)
    n = np.count_nonzero(vorhanden, axis=0).astype(np.int64)
    summe = np.sum(np.where(vorhanden, summand, 0.0), axis=0)
    with np.errstate(invalid="ignore", divide="ignore"):
        mittel: FloatArray = np.where(n > 0, summe / np.where(n > 0, n, 1), np.nan)
    return mittel, n


def punktmittel_betrag(
    werte: npt.NDArray[np.generic],
    gueltig: BoolArray | None = None,
    *,
    groesse: str = "",
    einheit: str = "",
    annahmen: Annahmen | None = None,
) -> Punktmittel:
    """Betragsmittel und quadratisches Mittel über die gültigen Punkte (FG-02 3.2).

    Parameters
    ----------
    werte : numpy.ndarray
        ``(P, K)``, reell oder komplex; gemittelt wird :math:`|X|`.
    gueltig : numpy.ndarray, optional
        Gültigkeit ``(P,)``; ``None`` = alle gültig.
    groesse, einheit : str
        Beschriftung.
    annahmen : Annahmen, optional
        Für die Annahmenliste der Ausgabe.
    """
    annahmen = annahmen if annahmen is not None else Annahmen()
    betrag = np.abs(_auswahl(werte, gueltig)).astype(np.float64)
    m_betrag, n = _mittel(betrag)
    m_quadrat, _ = _mittel(betrag**2)
    return Punktmittel(
        groesse=groesse,
        einheit=einheit,
        mittel_betrag=m_betrag,
        mittel_quadratisch=np.sqrt(m_quadrat),
        mittel_arithmetisch=None,
        n_mittel=n,
        annahmen=annahmen.eintraege(),
    )


def punktmittel_arithmetisch(
    werte: FloatArray,
    gueltig: BoolArray | None = None,
    *,
    groesse: str = "",
    einheit: str = "",
    annahmen: Annahmen | None = None,
) -> Punktmittel:
    """Arithmetisches Mittel über die gültigen Punkte (AP und γ², FG-02 3.2)."""
    annahmen = annahmen if annahmen is not None else Annahmen()
    auswahl = _auswahl(werte, gueltig)
    if np.iscomplexobj(auswahl):
        raise TypeError("arithmetisches Punktmittel nur für reelle Größen (AP, γ²)")
    m, n = _mittel(auswahl.astype(np.float64))
    return Punktmittel(
        groesse=groesse,
        einheit=einheit,
        mittel_betrag=None,
        mittel_quadratisch=None,
        mittel_arithmetisch=m,
        n_mittel=n,
        annahmen=annahmen.eintraege(),
    )
