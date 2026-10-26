"""Thread-sichere, geordnete Warteschlange von Messungen und Pausenpunkten.

Alle Methoden laufen unter einer Sperre. Strukturänderungen (Einfügen ausgenommen, das ein
neuer Eintrag ist) sind nur für Einträge im Zustand ``WARTEND`` erlaubt (R-012 bis R-016).
Schlägt eine Operation fehl, bleibt die Warteschlange unverändert.
"""

from __future__ import annotations

import threading
from collections.abc import Iterable
from dataclasses import fields, replace
from uuid import UUID

from ldv_automation.domaene.eintraege import (
    Eintrag,
    Messung,
    MessungZustand,
    Pausenpunkt,
    PausenpunktZustand,
)

_BEARBEITBARE_FELDER: dict[type, frozenset[str]] = {
    Messung: frozenset({"name", "einstellungsdatei", "parameter", "zeitlimit_s", "notiz"}),
    Pausenpunkt: frozenset({"text"}),
}


_NUR_BEANSPRUCHEN = (
    "Eintrag {id}: Übergang WARTEND -> {neu} nur über naechsten_beanspruchen() erlaubt"
)


def _pruefe_index(position: object) -> None:
    """Lehnt Nicht-Ganzzahlen und ``bool`` als Position ab."""
    if type(position) is not int:
        raise ValueError(f"Position muss eine Ganzzahl sein, erhalten {position!r}")


class Warteschlange:
    """Geordnete Liste von Einträgen.

    Parameters
    ----------
    eintraege : iterable of Messung or Pausenpunkt
        Anfangsinhalt (beliebige Zustände, z. B. zur Wiederherstellung); IDs müssen
        eindeutig sein.

    Raises
    ------
    ValueError
        Bei doppelter ID im Anfangsinhalt.
    """

    def __init__(self, eintraege: Iterable[Eintrag] = ()) -> None:
        self._sperre = threading.Lock()
        self._eintraege: list[Eintrag] = []
        for eintrag in eintraege:
            if any(e.id == eintrag.id for e in self._eintraege):
                raise ValueError(f"Doppelte Eintrags-ID {eintrag.id}")
            self._eintraege.append(eintrag)

    # --- Lesen -----------------------------------------------------------------------

    def __len__(self) -> int:
        with self._sperre:
            return len(self._eintraege)

    def eintraege(self) -> tuple[Eintrag, ...]:
        """Momentaufnahme aller Einträge in Reihenfolge (unveränderliche Objekte)."""
        with self._sperre:
            return tuple(self._eintraege)

    def hole(self, eintrag_id: UUID) -> Eintrag:
        """Gibt den Eintrag zur ID zurück (``KeyError`` bei unbekannter ID)."""
        with self._sperre:
            return self._eintraege[self._index(eintrag_id)]

    def index_von(self, eintrag_id: UUID) -> int:
        """Position des Eintrags (``KeyError`` bei unbekannter ID)."""
        with self._sperre:
            return self._index(eintrag_id)

    # --- Strukturänderungen (R-012 bis R-015) -------------------------------------------

    def einfuegen(self, position: int, eintrag: Eintrag) -> None:
        """Fügt einen neuen Eintrag an ``position`` ein (R-012).

        Parameters
        ----------
        position : int
            Zielindex, ``0 <= position <= len`` (0-basiert).
        eintrag : Messung or Pausenpunkt
            Neuer Eintrag im Zustand ``WARTEND`` mit bisher unbekannter ID.

        Raises
        ------
        IndexError
            Wenn ``position`` außerhalb von ``0 … len`` liegt.
        ValueError
            Wenn der Eintrag nicht ``WARTEND`` ist oder seine ID schon vorkommt.
        """
        if not isinstance(eintrag, Messung | Pausenpunkt):
            raise ValueError(f"Eintrag muss Messung oder Pausenpunkt sein, erhalten {eintrag!r}")
        _pruefe_index(position)
        if not eintrag.bearbeitbar:
            raise ValueError("Nur Einträge im Zustand WARTEND können eingefügt werden")
        with self._sperre:
            if not 0 <= position <= len(self._eintraege):
                raise IndexError(f"Position {position} außerhalb von 0 … {len(self._eintraege)}")
            if any(e.id == eintrag.id for e in self._eintraege):
                raise ValueError(f"Eintrags-ID {eintrag.id} ist bereits vorhanden")
            self._eintraege.insert(position, eintrag)

    def entfernen(self, eintrag_id: UUID) -> Eintrag:
        """Entfernt einen wartenden Eintrag (R-013) und gibt ihn zurück.

        Raises
        ------
        KeyError
            Bei unbekannter ID.
        ValueError
            Wenn der Eintrag nicht ``WARTEND`` ist.
        """
        with self._sperre:
            index = self._index(eintrag_id)
            self._pruefe_bearbeitbar(self._eintraege[index], "entfernt")
            return self._eintraege.pop(index)

    def bearbeiten(self, eintrag_id: UUID, **aenderungen: object) -> Eintrag:
        """Ändert Felder eines wartenden Eintrags (R-014) und gibt den neuen Eintrag zurück.

        Parameters
        ----------
        eintrag_id : uuid.UUID
            ID des Eintrags.
        **aenderungen
            Messung: ``name``, ``einstellungsdatei``, ``parameter`` (ersetzt die gesamte
            Zuordnung), ``zeitlimit_s``, ``notiz``. Pausenpunkt: ``text``.

        Raises
        ------
        KeyError
            Bei unbekannter ID.
        ValueError
            Wenn der Eintrag nicht ``WARTEND`` ist, ein Feld nicht änderbar ist oder ein Wert
            ungültig ist (z. B. Parameter außerhalb des Katalogbereichs).
        """
        with self._sperre:
            index = self._index(eintrag_id)
            alt = self._eintraege[index]
            self._pruefe_bearbeitbar(alt, "bearbeitet")
            erlaubt = _BEARBEITBARE_FELDER[type(alt)]
            unzulaessig = sorted(set(aenderungen) - erlaubt)
            if unzulaessig:
                bekannt = {f.name for f in fields(alt)}
                art = "unbekannt" if set(unzulaessig) - bekannt else "nicht änderbar"
                raise ValueError(
                    f"Feld(er) {', '.join(unzulaessig)} {art}; "
                    f"änderbar: {', '.join(sorted(erlaubt))}"
                )
            neu = replace(alt, **aenderungen)  # type: ignore[arg-type]  # validiert in __post_init__
            self._eintraege[index] = neu
            return neu

    def verschieben(self, eintrag_id: UUID, neue_position: int) -> None:
        """Verschiebt einen wartenden Eintrag (R-015).

        Parameters
        ----------
        neue_position : int
            Zielindex in der Liste nach dem Verschieben, ``0 <= neue_position < len``.

        Raises
        ------
        KeyError
            Bei unbekannter ID.
        ValueError
            Wenn der Eintrag nicht ``WARTEND`` ist.
        IndexError
            Wenn ``neue_position`` außerhalb von ``0 … len-1`` liegt.
        """
        _pruefe_index(neue_position)
        with self._sperre:
            index = self._index(eintrag_id)
            eintrag = self._eintraege[index]
            self._pruefe_bearbeitbar(eintrag, "verschoben")
            if not 0 <= neue_position < len(self._eintraege):
                raise IndexError(
                    f"Position {neue_position} außerhalb von 0 … {len(self._eintraege) - 1}"
                )
            del self._eintraege[index]
            self._eintraege.insert(neue_position, eintrag)

    # --- Für die Ablaufsteuerung --------------------------------------------------------

    def naechsten_beanspruchen(self) -> Eintrag | None:
        """Beansprucht atomar den ersten wartenden Eintrag.

        Eine Messung wird ``WARTEND -> LAEUFT``, ein Pausenpunkt
        ``WARTEND -> ERREICHT``. Änderungen vor diesem Moment wirken im selben Durchgang
        (R-016); danach ist der Eintrag unveränderlich.

        Returns
        -------
        Messung or Pausenpunkt or None
            Der beanspruchte Eintrag im neuen Zustand, ``None`` wenn nichts wartet.
        """
        with self._sperre:
            for index, eintrag in enumerate(self._eintraege):
                if not eintrag.bearbeitbar:
                    continue
                if isinstance(eintrag, Messung):
                    neu: Eintrag = eintrag.mit_zustand(MessungZustand.LAEUFT)
                else:
                    neu = eintrag.mit_zustand(PausenpunktZustand.ERREICHT)
                self._eintraege[index] = neu
                return neu
            return None

    def zustand_setzen(self, eintrag_id: UUID, neu: MessungZustand | PausenpunktZustand) -> Eintrag:
        """Setzt den Zustand eines Eintrags nach den erlaubten Übergängen.

        ``FEHLER -> WARTEND`` (Wiederholen) erhöht den Versuchszähler der Messung; der
        Eintrag behält seine Position.

        ``WARTEND -> LAEUFT`` und ``WARTEND -> ERREICHT`` sind hier **nicht** erlaubt;
        sie gibt es nur über :meth:`naechsten_beanspruchen` (atomar, Reihenfolge).

        Raises
        ------
        KeyError
            Bei unbekannter ID.
        ValueError
            Bei unerlaubtem Übergang oder Zustandsart, die nicht zum Eintrag passt.
        """
        with self._sperre:
            index = self._index(eintrag_id)
            alt = self._eintraege[index]
            if isinstance(alt, Messung):
                if not isinstance(neu, MessungZustand):
                    raise ValueError(f"Messung '{alt.name}': Zustand {neu!r} passt nicht")
                if alt.bearbeitbar and neu is MessungZustand.LAEUFT:
                    raise ValueError(_NUR_BEANSPRUCHEN.format(id=alt.id, neu=neu.name))
                ergebnis: Eintrag = alt.mit_zustand(neu)
            else:
                if not isinstance(neu, PausenpunktZustand):
                    raise ValueError(f"Pausenpunkt '{alt.text}': Zustand {neu!r} passt nicht")
                if alt.bearbeitbar and neu is PausenpunktZustand.ERREICHT:
                    raise ValueError(_NUR_BEANSPRUCHEN.format(id=alt.id, neu=neu.name))
                ergebnis = alt.mit_zustand(neu)
            self._eintraege[index] = ergebnis
            return ergebnis

    # --- intern (Sperre muss gehalten werden) ---------------------------------------------

    def _index(self, eintrag_id: UUID) -> int:
        for index, eintrag in enumerate(self._eintraege):
            if eintrag.id == eintrag_id:
                return index
        raise KeyError(f"Unbekannte Eintrags-ID {eintrag_id}")

    @staticmethod
    def _pruefe_bearbeitbar(eintrag: Eintrag, taetigkeit: str) -> None:
        if not eintrag.bearbeitbar:
            raise ValueError(
                f"Eintrag {eintrag.id} im Zustand {eintrag.zustand.name} kann nicht "
                f"{taetigkeit} werden (nur WARTEND)"
            )
