"""Vorbereitung des Arbeitsbildes „Bild speichern …“ (P-AUSW T4, UI-17, ADR-026 Nachtrag 2).

Das Arbeitsbild wird mit **denselben Zeichenfunktionen** wie die Bildschirmdarstellung auf einer
neuen Figure erzeugt (:func:`ldv_automation.darstellung.bild.speichere_arbeitsbild`). Zwei Dinge
unterscheiden es von der Bildschirmdarstellung und stehen hier, Qt-frei und testbar:

- **Optionen:** Die Oberfläche blendet Legende, Beschriftungsstreifen und Kasten in Ansicht 3 aus
  (die Angaben stehen in der Auswahlspalte). Das Bild nimmt die Voreinstellungen der
  Zeichenfunktion (Legende, Streifen und Kasten im Bild), nicht die Optionen der Oberfläche.
- **Zoom:** Der Ausschnitt der Oberfläche wird übernommen, soweit er vom Ausgangsbereich abweicht.
"""

from __future__ import annotations

import dataclasses
import math
from collections.abc import Sequence

from matplotlib.axes import Axes

from ldv_automation.darstellung import Ansicht
from ldv_automation.darstellung.bild import Grenzen
from ldv_automation.darstellung.spitzen import SpitzenOptionen

__all__ = ["bild_grenzen", "bild_optionen"]


def bild_optionen(ansicht: Ansicht, optionen: object) -> object:
    """Optionen für das Arbeitsbild: Voreinstellungen der Zeichenfunktion für das Bild.

    Nur Ansicht 3 unterscheidet sich (Legende, Streifen und Kasten stehen im Bild); die Skala
    der Oberfläche bleibt erhalten. Die anderen Ansichten übernehmen die Optionen unverändert.
    """
    if ansicht is Ansicht.SPITZEN and isinstance(optionen, SpitzenOptionen):
        vorgabe = SpitzenOptionen()
        return dataclasses.replace(
            optionen,
            beschriftung_im_bild=vorgabe.beschriftung_im_bild,
            legende_im_bild=vorgabe.legende_im_bild,
        )
    return optionen


def _anders(a: tuple[float, float], b: tuple[float, float]) -> bool:
    """Prüft, ob ``a`` vom Ausgangsbereich ``b`` abweicht (relative Toleranz 1e-12)."""
    return not all(
        math.isclose(wert, ref, rel_tol=1e-12, abs_tol=1e-15)
        for wert, ref in zip(a, b, strict=True)
    )


def bild_grenzen(
    ansicht: Ansicht,
    achsen: Sequence[Axes],
    standard: Sequence[tuple[tuple[float, float], tuple[float, float]]],
) -> dict[int, Grenzen]:
    """Zoom der Oberfläche als Grenzen für das Arbeitsbild (Achsenindex → ``(xlim, ylim)``).

    Übernommen wird nur, was der Nutzer verändert hat (Abweichung vom Ausgangsbereich). Die
    Schwingform (Ortskoordinaten) hat keinen Zoom. In Ansicht 3 gilt nur der Frequenzausschnitt:
    Die y-Grenzen der Oberfläche kennen den Beschriftungsstreifen des Bildes nicht, ihre
    Übernahme würde Kasten und Kurve überlagern.

    Parameters
    ----------
    ansicht : Ansicht
        Gezeigte Ansicht.
    achsen : sequence of Axes
        Achsen der Bildschirmfigur (Reihenfolge wie ``Zeichnung.achsen``).
    standard : sequence of tuple
        ``(xlim, ylim)`` je Achse unmittelbar nach dem Zeichnen (Ausgangsbereich).
    """
    if ansicht is Ansicht.SCHWINGFORM:
        return {}
    ergebnis: dict[int, Grenzen] = {}
    for i, (ax, (x0, y0)) in enumerate(zip(achsen, standard, strict=False)):
        x = ax.get_xlim()
        y = ax.get_ylim()
        xlim = x if _anders(x, x0) else None
        ylim = y if ansicht is not Ansicht.SPITZEN and _anders(y, y0) else None
        if xlim is not None or ylim is not None:
            ergebnis[i] = (xlim, ylim)
    return ergebnis
