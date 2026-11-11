"""Vorbereitung des Arbeitsbildes „Bild speichern …“ (P-AUSW T4, UI-17, ADR-026 Nachtrag 2).

Das Arbeitsbild wird mit **denselben Zeichenfunktionen** wie die Bildschirmdarstellung auf einer
neuen Figure erzeugt (:func:`ldv_automation.darstellung.bild.speichere_arbeitsbild`). Eine Sache
unterscheidet es von der Bildschirmdarstellung und steht hier, Qt-frei und testbar:

- **Optionen:** Die Oberfläche blendet Legende, Beschriftungsstreifen und Kasten in Ansicht 3 aus
  (die Angaben stehen in der Auswahlspalte). Das Bild nimmt die Voreinstellungen der
  Zeichenfunktion (Legende, Streifen und Kasten im Bild), nicht die Optionen der Oberfläche.

Der Ausschnitt (Zoom) steht seit P-AUSW2 S2 in den Achsenoptionen (``achsen``, eine Quelle,
ADR-028) und gelangt ohne Sonderweg ins Bild; die frühere Funktion ``bild_grenzen`` entfällt.
"""

from __future__ import annotations

import dataclasses

from ldv_automation.darstellung import Ansicht
from ldv_automation.darstellung.spitzen import SpitzenOptionen

__all__ = ["bild_optionen"]


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
