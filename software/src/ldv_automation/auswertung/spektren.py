r"""Spektren je Punkt (FG-02 3.1, A-2, R-050).

Beide Spektren werden immer getrennt und benannt ausgegeben:

``spektrum_kohaerent``
    :math:`\mathrm{CPH}_{ab}` (komplex, Spitzenwert in [a]): Anteil der Antwort, der mit
    der Referenz b kohärent ist; Phase relativ zu b.
``spektrum_leistung``
    :math:`\sqrt{\mathrm{AP}_a}` (reell, Spitzenwert in [a]): quadratisch gemittelter
    Betrag aller Blöcke, mit Rauschen und unkorrelierten Anteilen, ohne Phase.

Es gilt :math:`|\mathrm{CPH}| \le \sqrt{\mathrm{AP}_a}`; bei
:math:`\mathrm{CPH} = \mathrm{CP}/\sqrt{\mathrm{AP}_b}` ist
:math:`|\mathrm{CPH}| = \gamma\sqrt{\mathrm{AP}_a}` [FG-02 3.1, A].
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from .annahmen import AnnahmeEintrag, Annahmen
from .daten import ComplexArray, FloatArray, Messdaten, Paardaten

HINWEIS_CPH_BERECHNET = (
    "CPH berechnet als CP/√AP_b (exakt nur bei konstanter Referenzamplitude über die Blöcke)"
)


@dataclass(frozen=True, kw_only=True, eq=False)
class Spektren:
    r"""Spektren eines Kanals (FG-02 3.1).

    Attributes
    ----------
    kanal : str
        Antwortkanal a.
    referenz : str or None
        Referenzkanal b; ``None`` ohne Referenz.
    einheit : str
        Einheit [a] (Spitzenwert, einseitig).
    spektrum_kohaerent : numpy.ndarray or None
        ``(P, K)`` complex; ``None`` ohne Referenz (kein NaN-Feld).
    spektrum_leistung : numpy.ndarray
        ``(P, K)`` float, :math:`\sqrt{\mathrm{AP}_a}`.
    cph_berechnet : bool
        Kennzeichen „CPH berechnet“.
    hinweise : tuple of str
        Hinweise zur Ausgabe.
    annahmen : tuple of AnnahmeEintrag
        Geltende Annahmen (P-11).
    """

    kanal: str
    referenz: str | None
    einheit: str
    spektrum_kohaerent: ComplexArray | None
    spektrum_leistung: FloatArray
    cph_berechnet: bool
    hinweise: tuple[str, ...]
    annahmen: tuple[AnnahmeEintrag, ...]


def spektrum_leistung(ap: FloatArray) -> FloatArray:
    r"""Leistungsmittel :math:`\sqrt{\mathrm{AP}}` (Spitzenwert, Einheit [a])."""
    ergebnis: FloatArray = np.sqrt(ap)
    return ergebnis


def spektren_paar(paar: Paardaten) -> Spektren:
    """Spektren der Antwort a mit Referenz b (kohärent und Leistungsmittel)."""
    return Spektren(
        kanal=paar.antwort,
        referenz=paar.referenz,
        einheit=paar.einheit_antwort,
        spektrum_kohaerent=paar.cph,
        spektrum_leistung=spektrum_leistung(paar.ap_antwort),
        cph_berechnet=paar.cph_berechnet,
        hinweise=(HINWEIS_CPH_BERECHNET,) if paar.cph_berechnet else (),
        annahmen=paar.annahmen,
    )


def spektren_kanal(daten: Messdaten, kanal: str, annahmen: Annahmen | None = None) -> Spektren:
    """Spektren eines Kanals ohne Referenz: nur ``spektrum_leistung`` (FG-02 3.1)."""
    annahmen = annahmen if annahmen is not None else Annahmen()
    return Spektren(
        kanal=kanal,
        referenz=None,
        einheit=daten.einheiten[kanal],
        spektrum_kohaerent=None,
        spektrum_leistung=spektrum_leistung(daten.ap[kanal]),
        cph_berechnet=False,
        hinweise=("ohne Referenz: nur Leistungsmittel √AP, keine Phase",),
        annahmen=annahmen.eintraege(),
    )


def staple_3d(x: np.ndarray, y: np.ndarray, z: np.ndarray) -> np.ndarray:
    """Stapelt Komponenten X, Y, Z der Form ``(P, K)`` zu ``(P, 3, K)``.

    Raises
    ------
    ValueError
        Bei ungleichen Formen.
    """
    if not (x.shape == y.shape == z.shape) or x.ndim != 2:
        raise ValueError(f"X, Y, Z brauchen gleiche Form (P, K): {x.shape}, {y.shape}, {z.shape}")
    return np.stack([x, y, z], axis=1)


def betrag_3d(komponenten: np.ndarray) -> FloatArray:
    r"""3D-Betrag je Linie :math:`\sqrt{\sum_c |X_c|^2}` (PSV-Konvention, FG-02 3.1).

    Parameters
    ----------
    komponenten : numpy.ndarray
        Form ``(P, 3, K)`` (komplex oder reell), Reihenfolge X, Y, Z.
    """
    if komponenten.ndim != 3 or komponenten.shape[1] != 3:
        raise ValueError(f"(P, 3, K) erwartet: {komponenten.shape}")
    ergebnis: FloatArray = np.sqrt(np.sum(np.abs(komponenten) ** 2, axis=1))
    return ergebnis


def betrag_3d_ap(ap_3d: FloatArray) -> FloatArray:
    r"""3D-Betrag aus Autospektren :math:`\sqrt{\sum_c \mathrm{AP}_c}`, Form ``(P, 3, K)``."""
    if ap_3d.ndim != 3 or ap_3d.shape[1] != 3:
        raise ValueError(f"(P, 3, K) erwartet: {ap_3d.shape}")
    ergebnis: FloatArray = np.sqrt(np.sum(ap_3d, axis=1))
    return ergebnis
