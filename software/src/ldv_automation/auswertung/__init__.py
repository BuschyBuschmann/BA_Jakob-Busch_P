"""Auswertung von PSV-Messdaten, Stufe 1 (Paket W5-1).

Umsetzung der vom Nutzer am 2026-10-29 freigegebenen Fachgrundlage
``in_progress/fachgrundlagen/FG-02_auswertung-stufe1.md`` (R-050 bis R-053). Qt-frei,
abhängig nur von NumPy, der Standardbibliothek und ``ldv_automation.protokoll.version``
(Git-Hash im Export).

Module (FG-02-Abschnitt in Klammern):

- :mod:`.annahmen` – Annahmen M1–M11, Schwellen, Toleranzen (2.3, 2.4, 4, 8, 11)
- :mod:`.daten` – Datenvertrag, Vorzeichen und Konjugation (2.4, 6.1)
- :mod:`.spektren` – ``spektrum_kohaerent``, ``spektrum_leistung``, 3D-Betrag (3.1)
- :mod:`.mittel` – Punktmittel (3.2)
- :mod:`.frf` – H1, H2, γ², Zufallsfehler, Maske, Gewichte (3.3–3.5)
- :mod:`.schwingform` – Betriebsschwingform, 3D-Kennwerte (3.6)
- :mod:`.umrechnung` – Weg/Schnelle/Beschleunigung (3.7)
- :mod:`.baender` – Band-Effektivwerte (3.8)
- :mod:`.spitzen` – Spitzensuche, -3-dB-Breite (3.9)
- :mod:`.plausibilitaet` – P-01 bis P-11 (4)
- :mod:`.gesamt` – Gesamtauswertung einer Messung
- :mod:`.export` – Export npz + JSON (5)
- :mod:`.svd_adapter` – Anbindung an den W2-Leser
"""

from .annahmen import ANNAHME, AnnahmeEintrag, Annahmen, Schwellen, Toleranzen
from .daten import Herkunft, Messdaten, Paardaten, Punkte, bereite_paar
from .gesamt import Auswertung, PaarAuswertung, schwingform_aus, werte_aus

__all__ = [
    "ANNAHME",
    "AnnahmeEintrag",
    "Annahmen",
    "Auswertung",
    "Herkunft",
    "Messdaten",
    "PaarAuswertung",
    "Paardaten",
    "Punkte",
    "Schwellen",
    "Toleranzen",
    "bereite_paar",
    "schwingform_aus",
    "werte_aus",
]
