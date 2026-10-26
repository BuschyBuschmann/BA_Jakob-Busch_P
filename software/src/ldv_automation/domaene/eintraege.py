"""Einträge der Warteschlange: Messungen und Pausenpunkte.

Beide Eintragsarten sind unveränderliche Datenklassen. Eine "Änderung" erzeugt eine neue
Instanz (``dataclasses.replace``), die Warteschlange tauscht sie unter ihrer Sperre aus.
Die Ablaufsteuerung arbeitet dadurch automatisch mit einer eingefrorenen Kopie der
Messdefinition (Plan P2, 2.4).
"""

from __future__ import annotations

import math
from collections.abc import Mapping
from dataclasses import dataclass, field, replace
from enum import Enum
from types import MappingProxyType
from typing import TypeAlias
from uuid import UUID, uuid4

from ldv_automation.domaene.parameter import KATALOG, ParameterWert


class MessungZustand(Enum):
    """Zustand einer Messung (Plan P2, 2.1)."""

    WARTEND = "wartend"
    LAEUFT = "laeuft"
    FERTIG = "fertig"
    FEHLER = "fehler"
    ABGEBROCHEN = "abgebrochen"


class PausenpunktZustand(Enum):
    """Zustand eines Pausenpunkts (Plan P2, 2.2)."""

    WARTEND = "wartend"
    ERREICHT = "erreicht"
    ERLEDIGT = "erledigt"


_MESSUNG_UEBERGAENGE: Mapping[MessungZustand, frozenset[MessungZustand]] = {
    MessungZustand.WARTEND: frozenset({MessungZustand.LAEUFT}),
    MessungZustand.LAEUFT: frozenset(
        {MessungZustand.FERTIG, MessungZustand.FEHLER, MessungZustand.ABGEBROCHEN}
    ),
    # Wiederholen nach Fehler (Fehlerentscheidung); erhöht den Versuchszähler.
    MessungZustand.FEHLER: frozenset({MessungZustand.WARTEND}),
    MessungZustand.FERTIG: frozenset(),
    MessungZustand.ABGEBROCHEN: frozenset(),
}

_PAUSENPUNKT_UEBERGAENGE: Mapping[PausenpunktZustand, frozenset[PausenpunktZustand]] = {
    PausenpunktZustand.WARTEND: frozenset({PausenpunktZustand.ERREICHT}),
    # ERREICHT -> WARTEND: Rücksetzen, wenn der Durchgang am Pausenpunkt abgebrochen wird
    # (nicht gestartete Einträge bleiben WARTEND, Plan P2, 2.1).
    PausenpunktZustand.ERREICHT: frozenset(
        {PausenpunktZustand.ERLEDIGT, PausenpunktZustand.WARTEND}
    ),
    PausenpunktZustand.ERLEDIGT: frozenset(),
}


def _kurz(wert: object) -> str:
    """Kurzdarstellung für Fehlermeldungen (begrenzt, auch bei riesigen Ganzzahlen)."""
    text = repr(wert)
    return text if len(text) <= 30 else text[:27] + "..."


@dataclass(frozen=True, kw_only=True)
class Messung:
    """Definition und Zustand einer Messung.

    Parameters
    ----------
    name : str
        Anzeigename (nicht leer); dient auch zur Bildung von Dateinamen.
    einstellungsdatei : str
        Pfad der in PSV vorbereiteten Einstellungsdatei (``.set``). Wird als Text
        gespeichert und hier nicht auf Existenz geprüft (Vorprüfung im Ablauf).
    parameter : mapping
        Gegenüber der Einstellungsdatei geänderte Parameter (Schlüssel aus
        :data:`ldv_automation.domaene.parameter.KATALOG`). Werden beim Anlegen geprüft
        und normalisiert; das Ergebnis ist schreibgeschützt.
    zeitlimit_s : float or None
        Zeitlimit dieser Messung in s (Ganzzahlen werden zu ``float``); ``None`` bedeutet
        globales Zeitlimit.
    notiz : str
        Freitext.
    id : uuid.UUID
        Eindeutige Kennung (Standard: neue UUID4).
    zustand : MessungZustand
        Aktueller Zustand.
    versuch : int
        Versuchszähler, beginnt bei 1; steigt bei "Wiederholen".

    Raises
    ------
    ValueError
        Bei leerem Namen oder leerer Einstellungsdatei, ungültigem Zeitlimit, ungültigem
        Versuchszähler oder ungültigem Parameter (Meldung nennt Schlüssel und Bereich).
    """

    name: str
    einstellungsdatei: str
    parameter: Mapping[str, ParameterWert] = field(default_factory=dict)
    zeitlimit_s: float | None = None
    notiz: str = ""
    id: UUID = field(default_factory=uuid4)
    zustand: MessungZustand = MessungZustand.WARTEND
    versuch: int = 1

    def __post_init__(self) -> None:
        if not isinstance(self.name, str) or not self.name.strip():
            raise ValueError(f"Messung: Name muss nicht leerer Text sein, erhalten {self.name!r}")
        if not isinstance(self.einstellungsdatei, str) or not self.einstellungsdatei.strip():
            raise ValueError(
                f"Messung '{self.name}': Einstellungsdatei muss nicht leerer Text sein"
            )
        if not isinstance(self.notiz, str):
            raise ValueError(f"Messung '{self.name}': notiz muss Text sein")
        if not isinstance(self.id, UUID):
            raise ValueError(f"Messung '{self.name}': id muss eine UUID sein")
        if not isinstance(self.zustand, MessungZustand):
            raise ValueError(f"Messung '{self.name}': zustand muss MessungZustand sein")
        if type(self.versuch) is not int or self.versuch < 1:
            raise ValueError(
                f"Messung '{self.name}': versuch muss eine Ganzzahl ≥ 1 sein, "
                f"erhalten {self.versuch!r}"
            )
        if self.zeitlimit_s is not None:
            limit = self.zeitlimit_s
            try:
                ok = (
                    not isinstance(limit, bool)
                    and isinstance(limit, int | float)
                    and math.isfinite(limit)
                    and limit > 0
                )
                zahl = float(limit) if ok else 0.0
            except OverflowError:
                ok = False
            if not ok:
                raise ValueError(
                    f"Messung '{self.name}': zeitlimit_s muss eine endliche Zahl > 0 oder "
                    f"None sein, erhalten {_kurz(limit)}"
                )
            object.__setattr__(self, "zeitlimit_s", zahl)
        geprueft = KATALOG.pruefe(self.parameter)
        object.__setattr__(self, "parameter", MappingProxyType(geprueft))

    @property
    def bearbeitbar(self) -> bool:
        """``True``, solange die Messung noch nicht gestartet wurde (``WARTEND``)."""
        return self.zustand is MessungZustand.WARTEND

    def mit_zustand(self, neu: MessungZustand) -> Messung:
        """Gibt eine Kopie im neuen Zustand zurück.

        Raises
        ------
        ValueError
            Wenn der Übergang nicht erlaubt ist.
        """
        if not isinstance(neu, MessungZustand) or neu not in _MESSUNG_UEBERGAENGE[self.zustand]:
            name = neu.name if isinstance(neu, Enum) else repr(neu)
            raise ValueError(
                f"Messung '{self.name}': Übergang {self.zustand.name} -> {name} nicht erlaubt"
            )
        wiederholung = self.zustand is MessungZustand.FEHLER
        return replace(
            self, zustand=neu, versuch=self.versuch + 1 if wiederholung else self.versuch
        )


@dataclass(frozen=True, kw_only=True)
class Pausenpunkt:
    """Pausenpunkt: Der Durchgang hält hier an, bis der Nutzer bestätigt (R-017).

    Parameters
    ----------
    text : str
        Hinweistext für den Nutzer (nicht leer).
    id : uuid.UUID
        Eindeutige Kennung.
    zustand : PausenpunktZustand
        Aktueller Zustand.
    """

    text: str
    id: UUID = field(default_factory=uuid4)
    zustand: PausenpunktZustand = PausenpunktZustand.WARTEND

    def __post_init__(self) -> None:
        if not isinstance(self.text, str) or not self.text.strip():
            raise ValueError(
                f"Pausenpunkt: Text muss nicht leerer Text sein, erhalten {self.text!r}"
            )
        if not isinstance(self.id, UUID):
            raise ValueError("Pausenpunkt: id muss eine UUID sein")
        if not isinstance(self.zustand, PausenpunktZustand):
            raise ValueError("Pausenpunkt: zustand muss PausenpunktZustand sein")

    @property
    def bearbeitbar(self) -> bool:
        """``True``, solange der Pausenpunkt nicht erreicht wurde (``WARTEND``)."""
        return self.zustand is PausenpunktZustand.WARTEND

    def mit_zustand(self, neu: PausenpunktZustand) -> Pausenpunkt:
        """Gibt eine Kopie im neuen Zustand zurück.

        Raises
        ------
        ValueError
            Wenn der Übergang nicht erlaubt ist.
        """
        if (
            not isinstance(neu, PausenpunktZustand)
            or neu not in _PAUSENPUNKT_UEBERGAENGE[self.zustand]
        ):
            name = neu.name if isinstance(neu, Enum) else repr(neu)
            raise ValueError(
                f"Pausenpunkt '{self.text}': Übergang {self.zustand.name} -> {name} nicht erlaubt"
            )
        return replace(self, zustand=neu)


Eintrag: TypeAlias = Messung | Pausenpunkt
"""Ein Element der Warteschlange."""
