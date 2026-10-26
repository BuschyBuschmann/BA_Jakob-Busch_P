"""Austauschbares Fehlerverhalten der Ablaufsteuerung (R-019, **vorläufig**).

Wie die Software auf eine fehlgeschlagene Messung reagieren soll, ist mit dem Betreuer
noch zu klären (offene Frage O1, Betreuerfrage F20). Bis dahin gilt die vorläufige
Strategie :class:`PausierenUndNachfragen`: Der Durchgang hält an, der Nutzer entscheidet
zwischen Wiederholen, Überspringen und Abbrechen.

Eine andere Strategie ist eine neue Klasse, die :class:`Fehlerstrategie` erfüllt. Die
Steuerung (``ablauf/steuerung.py``) ändert sich dafür nicht (Plan P2, 2.6).

Eine Strategie kann bewusst nicht automatisch "wiederholen": Ohne Obergrenze könnte das
in einer Endlosschleife enden. Wiederholen ist nur eine Entscheidung des Nutzers.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Protocol, runtime_checkable

from ldv_automation.domaene.eintraege import Messung


class FehlerArt(Enum):
    """Art eines Fehlers einer Messung (Plan P2, 2.6)."""

    VORPRUEFUNG = "vorpruefung"
    """Zieldatei existiert, Einstellungsdatei fehlt, Parameter ungültig (ohne Gerätewirkung)."""
    GERAET_NICHT_BEREIT = "geraet_nicht_bereit"
    """Zustand ≠ gestoppt vor dem Start, also eine fremde Messung oder Aktivität."""
    GERAET = "geraet"
    """Fehler der Messsoftware bzw. COM-Ausnahme."""
    VERWEIGERT = "verweigert"
    """Operation wurde verweigert (Whitelist, Messfreigabe, vorhandene Datei)."""
    ABWEICHUNG = "abweichung"
    """Zurückgelesener Wert weicht vom Sollwert ab (z. B. eingerastete Bandbreite)."""
    ZEITLIMIT = "zeitlimit"
    """Zeitlimit der Messung überschritten; die eigene Messung wurde gestoppt."""
    KEINE_DATEI = "keine_datei"
    """Nach dem Scan existiert die Zieldatei nicht."""
    GERAET_UNKLAR = "geraet_unklar"
    """``Stop`` greift nicht in der Frist; Zustand des Geräts unklar."""


@dataclass(frozen=True, kw_only=True)
class FehlerEreignis:
    """Beschreibung eines Fehlers für die Strategie.

    Parameters
    ----------
    art : FehlerArt
        Fehlerart.
    text : str
        Beschreibung für Nutzer und Protokoll.
    messung : Messung
        Die betroffene Messung (eingefrorene Kopie).
    gestartet : bool
        ``True``, wenn der Scan bereits gestartet wurde.
    """

    art: FehlerArt
    text: str
    messung: Messung
    gestartet: bool


class FehlerReaktion(Enum):
    """Antwort einer Strategie."""

    ANHALTEN_UND_FRAGEN = "anhalten_und_fragen"
    UEBERSPRINGEN = "ueberspringen"
    ABBRECHEN = "abbrechen"


@runtime_checkable
class Fehlerstrategie(Protocol):
    """Entscheidet, wie der Durchgang nach einem Fehler weitergeht."""

    @property
    def bezeichnung(self) -> str:
        """Name für Protokollfeld ``fehlerstrategie`` und Statuszeile."""
        ...

    def entscheide(self, ereignis: FehlerEreignis) -> FehlerReaktion:
        """Liefert die Reaktion auf ``ereignis``."""
        ...


class PausierenUndNachfragen:
    """**Vorläufige** Strategie (O1/F20): immer anhalten und den Nutzer fragen.

    Der Nutzer wählt danach Wiederholen, Überspringen oder Durchgang abbrechen. Die
    Kennzeichnung "vorläufig" steht in :attr:`bezeichnung` und damit im Messprotokoll.
    """

    @property
    def bezeichnung(self) -> str:
        """``"PausierenUndNachfragen (vorläufig, O1/F20)"``."""
        return "PausierenUndNachfragen (vorläufig, O1/F20)"

    def entscheide(self, ereignis: FehlerEreignis) -> FehlerReaktion:
        """Gibt immer :attr:`FehlerReaktion.ANHALTEN_UND_FRAGEN` zurück."""
        return FehlerReaktion.ANHALTEN_UND_FRAGEN
