"""Schnittstelle der Oberfläche zur Sitzung (Qt-frei).

Die Oberfläche spricht ausschließlich mit diesen Methoden der Sitzungsfassade
(:class:`ldv_automation.sitzung.Sitzung` erfüllt das Protokoll strukturell). Tests setzen
eine Attrappe ein, die ``Zustandsbild``-Attrappen liefert und Befehle aufzeichnet.
"""

from __future__ import annotations

from pathlib import Path
from typing import Protocol
from uuid import UUID

from ldv_automation.domaene import Eintrag
from ldv_automation.sitzung import (
    Betriebsart,
    Fehlerentscheidung,
    SitzungsEreignis,
    Voraussetzung,
    Zustandsbild,
)


class SitzungsFassade(Protocol):
    """Von der Oberfläche benutzte Befehle und Abfragen der Sitzung."""

    def zustandsbild(self) -> Zustandsbild:
        """Aktuelles Zustandsbild."""

    def hole_ereignisse(self) -> list[SitzungsEreignis]:
        """Ereignisse seit dem letzten Abholen."""

    def einfuegen(self, position: int, eintrag: Eintrag) -> None:
        """Eintrag einfügen."""

    def bearbeiten(self, eintrag_id: UUID, **aenderungen: object) -> Eintrag:
        """Wartenden Eintrag ändern."""

    def entfernen(self, eintrag_id: UUID) -> Eintrag:
        """Wartenden Eintrag entfernen."""

    def verschieben(self, eintrag_id: UUID, neue_position: int) -> None:
        """Wartenden Eintrag verschieben."""

    def speichere_warteschlange(self, pfad: Path, *, ueberschreiben: bool = False) -> None:
        """Warteschlange speichern."""

    def lade_warteschlange(self, pfad: Path) -> tuple[str, ...]:
        """Warteschlange laden (ersetzt die aktuelle)."""

    def setze_messdaten_wurzel(self, pfad: Path) -> None:
        """Messdaten-Ordner setzen."""

    def messen_voraussetzungen(self) -> tuple[Voraussetzung, ...]:
        """Voraussetzungen für ``MESSEN``."""

    def setze_betriebsart(self, neu: Betriebsart) -> None:
        """Betriebsart wechseln."""

    def verbinde(self) -> None:
        """Mit dem Gerät verbinden."""

    def trenne(self) -> None:
        """Verbindung trennen."""

    def starte(
        self,
        name: str,
        *,
        messen_bestaetigt: bool = False,
        erwartete_betriebsart: Betriebsart | None = None,
        erwartete_kennung: str | None = None,
    ) -> None:
        """Durchgang starten (auch aus ``BEENDET``), gebunden an den Schnappschuss."""

    def setze_standard_zeitlimit(self, zeitlimit_s: float) -> None:
        """Standard-Zeitlimit in s setzen."""

    def setze_einstellungen(self, messdaten_wurzel: Path, standard_zeitlimit_s: float) -> None:
        """Ordner und Standard-Zeitlimit gemeinsam übernehmen (``EinstellungsFehler``)."""

    def pausiere(self) -> None:
        """Pause anfordern."""

    def setze_fort(self) -> None:
        """Fortsetzen."""

    def brich_ab(self) -> None:
        """Durchgang abbrechen."""

    def bestaetige(self) -> None:
        """Pausenpunkt bestätigen."""

    def entscheide(self, entscheidung: Fehlerentscheidung) -> None:
        """Fehlerentscheidung senden."""

    def zuruecksetzen(self) -> None:
        """Alle Einträge auf wartend zurücksetzen (nur in ``BEREIT``/``BEENDET``)."""

    def quittiere(self) -> None:
        """Beendeten Durchgang quittieren (``BEENDET -> BEREIT``)."""
