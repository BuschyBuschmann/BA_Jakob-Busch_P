"""Zeichenfunktionen der Auswertung, GUI-frei (P-AUSW T2, ADR-021).

Je Ansicht eine Zeichenfunktion für Oberfläche **und** Thesis-Abbildung
(``zeichne_spektrum``, ``zeichne_frf``, ``zeichne_spitzen``, ``zeichne_schwingform``). Sie
füllen eine übergebene :class:`matplotlib.figure.Figure`, importieren weder Qt noch ``pyplot``
(Importtest) und rechnen nichts Neues: Daten kommen aus :mod:`ldv_automation.auswertung`
(:mod:`.auswahl`), der Stil als Parameter (:mod:`.stil`).

Module:

- :mod:`.stil` – :class:`~.stil.Plotstil`, :data:`~.stil.THESIS_STIL`
- :mod:`.formate` – Dezimalkomma, Einheiten, Gradanzeige
- :mod:`.auswahl` – Daten der Ansichten, :class:`~.auswahl.PaarCache`
- :mod:`.zeichnung` – Rückgabeobjekt, gemeinsame Bausteine
- :mod:`.spektrum`, :mod:`.frf`, :mod:`.spitzen`, :mod:`.schwingform` – die Zeichenfunktionen
- :mod:`.bild` – Arbeitsbild mit Stempel
"""

from .stil import THESIS_STIL, Plotstil
from .zeichnung import Ansicht, Zeichnung

__all__ = ["THESIS_STIL", "Ansicht", "Plotstil", "Zeichnung"]
