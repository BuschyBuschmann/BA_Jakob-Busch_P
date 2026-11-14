"""Messungsverwaltung des Reiters „Auswerten“ (R-058, P-AUSW2 S4), ohne Qt.

Der Reiter hält bis zu :data:`MESSUNGEN_MAX` geladene Messungen. Jede :class:`Messung` trägt
ihre Daten (``Geladen``), den ``PaarCache``, das Ergebnis von Stufe B und den Antriebspunkt;
die Ansichten 1 bis 4 arbeiten auf der **aktiven** Messung, Ansicht 5 greift auf alle zu.
Diese Logik ist Qt-frei und im Standardlauf voll getestet; das Widget
(:mod:`.messungsleiste`) und der Reiter zeigen nur an.

Kennungen (``id``) sind stabil und werden nie wiederverwendet: Eine Serie in Ansicht 5 bezieht
sich auf die ``id``, nicht auf den (änderbaren) Kurznamen oder die Listenposition. Der Kurzname
ist eindeutig (ohne Beachtung der Groß-/Kleinschreibung), nicht leer, höchstens
:data:`KURZNAME_MAX` Zeichen lang und ohne Zeilenumbruch (Brief K1-AUSW2, UI-9).
"""

from __future__ import annotations

import dataclasses
import string
from collections.abc import Iterable
from dataclasses import dataclass, field
from enum import Enum
from typing import Any

import numpy as np

from ldv_automation.auswertung.jobs import PruefErgebnis
from ldv_automation.auswertung.laden import Geladen
from ldv_automation.darstellung.auswahl import PaarCache
from ldv_automation.gui.anzeige_auswerten import dateiname_von

__all__ = [
    "KURZNAME_MAX",
    "MESSUNGEN_MAX",
    "TEXT_KURZNAME_DOPPELT",
    "TEXT_KURZNAME_LANG",
    "TEXT_KURZNAME_LEER",
    "TEXT_KURZNAME_UMBRUCH",
    "Messung",
    "Messungen",
    "MessungsZustand",
    "kurzname_vorschlag",
    "nbytes_von",
    "pruefe_kurzname",
]

MESSUNGEN_MAX = 4
"""Höchstzahl geöffneter Messungen (Annahme zu OF-5 aus P-AUSW2 Abschnitt 3, rund 115 MiB je
Messung mit zwei Kanalpaaren; der Arbeitsspeicher des Messrechners ist unbekannt, die Zahl wird
nach der Messung mit ``tools/auswertung/speicher_messen.py`` angepasst)."""
KURZNAME_MAX = 12
"""Längster Kurzname (Chip, Legende und Stempel bleiben lesbar)."""

TEXT_KURZNAME_LEER = "Der Kurzname darf nicht leer sein."
TEXT_KURZNAME_LANG = f"Der Kurzname darf höchstens {KURZNAME_MAX} Zeichen lang sein."
TEXT_KURZNAME_DOPPELT = "Diesen Kurznamen gibt es bereits."
TEXT_KURZNAME_UMBRUCH = "Der Kurzname darf keinen Zeilenumbruch enthalten."


class MessungsZustand(Enum):
    """Zustand einer Messung in der Liste."""

    LADEN = "laden"
    BEREIT = "bereit"
    FEHLER = "fehler"


@dataclass(eq=False)
class Messung:
    """Eine geöffnete Messung.

    Attributes
    ----------
    id : int
        Stabile Kennung (nie wiederverwendet).
    kurzname : str
        Eindeutiger Kurzname („A“, „B“, … oder vom Nutzer gewählt).
    pfad : str
        Pfad der ``.svd``-Datei.
    zustand : MessungsZustand
        Laden, bereit oder Fehler.
    geladen, cache, pruefung, pruef_fehler, antrieb, fehlertext
        Daten und Ergebnisse; ``None``, solange sie nicht vorliegen.
    paare : tuple
        Kanalpaare (Antwort, Referenz) der Datei.
    gestartet : bool
        Der Ladeauftrag ist gestartet (höchstens einer gleichzeitig).
    """

    id: int
    kurzname: str
    pfad: str
    zustand: MessungsZustand = MessungsZustand.LADEN
    geladen: Geladen | None = None
    cache: PaarCache | None = None
    pruefung: PruefErgebnis | None = None
    pruef_fehler: str | None = None
    antrieb: tuple[str, str, Any] | None = None
    fehlertext: str | None = None
    paare: tuple[tuple[str, str], ...] = ()
    gestartet: bool = False

    @property
    def dateiname(self) -> str:
        """Dateiname ohne Ordner."""
        return dateiname_von(self.pfad)

    @property
    def sha256(self) -> str | None:
        """Prüfsumme der Datei (``None``, solange nicht geladen)."""
        if self.geladen is None or self.geladen.messdaten.herkunft is None:
            return None
        return self.geladen.messdaten.herkunft.sha256


def kurzname_vorschlag(vorhandene: Iterable[str]) -> str:
    """Erster freier Kurzname „A“ … „Z“, „AA“ … (ohne Beachtung der Schreibweise)."""
    belegt = {n.casefold() for n in vorhandene}
    buchstaben = string.ascii_uppercase
    laenge = 1
    while True:
        # Spaltenfolge wie in Tabellen: A..Z, AA..AZ, BA..
        for zahl in range(len(buchstaben) ** laenge):
            name = ""
            rest = zahl
            for _ in range(laenge):
                name = buchstaben[rest % len(buchstaben)] + name
                rest //= len(buchstaben)
            if name.casefold() not in belegt:
                return name
        laenge += 1


def pruefe_kurzname(text: str, vorhandene: Iterable[str]) -> str | None:
    """Prüft einen Kurznamen.

    Parameters
    ----------
    text : str
        Eingabe (führende und nachgestellte Leerzeichen zählen nicht).
    vorhandene : iterable of str
        Kurznamen **der anderen** Messungen.

    Returns
    -------
    str or None
        Meldung (ohne Symbol) oder ``None``, wenn der Name gültig ist.
    """
    if "\n" in text or "\r" in text:
        return TEXT_KURZNAME_UMBRUCH
    name = text.strip()
    if not name:
        return TEXT_KURZNAME_LEER
    if len(name) > KURZNAME_MAX:
        return TEXT_KURZNAME_LANG
    if name.casefold() in {v.casefold() for v in vorhandene}:
        return TEXT_KURZNAME_DOPPELT
    return None


def nbytes_von(objekt: object, _gesehen: set[int] | None = None) -> int:
    """Summe der ``nbytes`` aller NumPy-Felder in ``objekt`` (Felder, Dicts, Tupel, Dataclasses).

    Jedes Feld zählt einmal (auch bei mehrfacher Verwendung). Das ist die Grundlage der
    Speicherangabe im Tooltip des Chips; es ist eine Untergrenze (Python-Objekte zählen nicht).
    """
    gesehen = _gesehen if _gesehen is not None else set()
    if id(objekt) in gesehen:
        return 0
    if isinstance(objekt, np.ndarray):
        gesehen.add(id(objekt))
        return int(objekt.nbytes)
    if isinstance(objekt, dict):
        gesehen.add(id(objekt))
        return sum(nbytes_von(w, gesehen) for w in objekt.values())
    if isinstance(objekt, (list, tuple)):
        gesehen.add(id(objekt))
        return sum(nbytes_von(w, gesehen) for w in objekt)
    if dataclasses.is_dataclass(objekt) and not isinstance(objekt, type):
        gesehen.add(id(objekt))
        return sum(nbytes_von(getattr(objekt, f.name), gesehen) for f in dataclasses.fields(objekt))
    return 0


@dataclass
class Messungen:
    """Liste der geöffneten Messungen mit aktiver Messung und Ladewarteschlange."""

    _liste: list[Messung] = field(default_factory=list)
    _aktiv_id: int | None = None
    _naechste_id: int = 1

    # --- Lesen -----------------------------------------------------------------------------

    @property
    def alle(self) -> tuple[Messung, ...]:
        """Alle Messungen in Reihenfolge des Öffnens."""
        return tuple(self._liste)

    @property
    def aktive(self) -> Messung | None:
        """Die aktive Messung (``None`` = keine)."""
        return self.finde(self._aktiv_id) if self._aktiv_id is not None else None

    @property
    def ist_voll(self) -> bool:
        """Die Höchstzahl :data:`MESSUNGEN_MAX` ist erreicht."""
        return len(self._liste) >= MESSUNGEN_MAX

    def __len__(self) -> int:
        return len(self._liste)

    def finde(self, messung_id: int | None) -> Messung | None:
        """Messung zur Kennung (``None``, wenn es sie nicht (mehr) gibt)."""
        for m in self._liste:
            if m.id == messung_id:
                return m
        return None

    def bereite(self) -> tuple[Messung, ...]:
        """Messungen, deren Daten vorliegen (für Ansicht 5)."""
        return tuple(m for m in self._liste if m.zustand is MessungsZustand.BEREIT)

    def kurznamen(self, ohne: int | None = None) -> tuple[str, ...]:
        """Kurznamen aller Messungen (optional ohne die mit Kennung ``ohne``)."""
        return tuple(m.kurzname for m in self._liste if m.id != ohne)

    # --- Ändern ----------------------------------------------------------------------------

    def hinzufuegen(self, pfad: str) -> Messung:
        """Legt eine Messung im Zustand „Laden“ an; sie wird erst mit :meth:`fertig` aktivierbar.

        Raises
        ------
        ValueError
            Die Höchstzahl ist erreicht.
        """
        if self.ist_voll:
            raise ValueError(f"Höchstens {MESSUNGEN_MAX} Messungen.")
        m = Messung(
            id=self._naechste_id,
            kurzname=kurzname_vorschlag(self.kurznamen()),
            pfad=pfad,
        )
        self._naechste_id += 1
        self._liste.append(m)
        return m

    def fertig(
        self,
        messung_id: int,
        *,
        geladen: Geladen,
        cache: PaarCache,
        antrieb: tuple[str, str, Any] | None,
        paare: tuple[tuple[str, str], ...],
    ) -> Messung:
        """Setzt die Daten einer ladenden Messung und macht sie „bereit“.

        Ist noch keine Messung aktiv, wird sie aktiv.
        """
        m = self._hole(messung_id)
        m.geladen, m.cache, m.antrieb, m.paare = geladen, cache, antrieb, paare
        m.zustand = MessungsZustand.BEREIT
        m.fehlertext = None
        if self._aktiv_id is None:
            self._aktiv_id = m.id
        return m

    def ersetze(
        self,
        messung_id: int,
        pfad: str,
        *,
        geladen: Geladen,
        cache: PaarCache,
        antrieb: tuple[str, str, Any] | None,
        paare: tuple[tuple[str, str], ...],
    ) -> Messung:
        """„Öffnen“: ersetzt eine Messung durch eine neue (Kurzname und Position bleiben).

        Die neue Messung bekommt eine **neue** Kennung (Serien der alten gelten nicht weiter);
        war die alte aktiv, ist die neue aktiv.
        """
        alt = self._hole(messung_id)
        neu = Messung(
            id=self._naechste_id,
            kurzname=alt.kurzname,
            pfad=pfad,
            zustand=MessungsZustand.BEREIT,
            geladen=geladen,
            cache=cache,
            antrieb=antrieb,
            paare=paare,
            gestartet=True,
        )
        self._naechste_id += 1
        self._liste[self._liste.index(alt)] = neu
        if self._aktiv_id == alt.id:
            self._aktiv_id = neu.id
        return neu

    def entferne(self, messung_id: int) -> Messung | None:
        """Entfernt eine Messung; die aktive rückt auf die vorige (sonst die nächste bereite).

        Returns
        -------
        Messung or None
            Die entfernte Messung (``None``, wenn es sie nicht gab).
        """
        m = self.finde(messung_id)
        if m is None:
            return None
        pos = self._liste.index(m)
        del self._liste[pos]
        if self._aktiv_id == m.id:
            kandidaten = [x for x in self._liste if x.zustand is MessungsZustand.BEREIT]
            davor = [x for x in kandidaten if self._liste.index(x) < pos]
            neu = davor[-1] if davor else (kandidaten[0] if kandidaten else None)
            self._aktiv_id = neu.id if neu is not None else None
        return m

    def leere(self) -> None:
        """Entfernt alle Messungen (Zustand „Keine Datei“); Kennungen bleiben unverbraucht."""
        self._liste.clear()
        self._aktiv_id = None

    def setze_aktiv(self, messung_id: int) -> Messung:
        """Macht eine bereite Messung zur aktiven.

        Raises
        ------
        ValueError
            Unbekannte Messung oder Messung noch nicht bereit.
        """
        m = self._hole(messung_id)
        if m.zustand is not MessungsZustand.BEREIT:
            raise ValueError(f"Messung {m.kurzname} ist noch nicht bereit.")
        self._aktiv_id = m.id
        return m

    def umbenennen(self, messung_id: int, text: str) -> str | None:
        """Ändert den Kurznamen.

        Returns
        -------
        str or None
            Meldung bei ungültigem Namen (Name bleibt), sonst ``None``.
        """
        m = self._hole(messung_id)
        fehler = pruefe_kurzname(text, self.kurznamen(ohne=m.id))
        if fehler is None:
            m.kurzname = text.strip()
        return fehler

    # --- Ladewarteschlange und Speicher ------------------------------------------------------

    def naechster_ladeauftrag(self) -> Messung | None:
        """Nächste Messung, deren Ladeauftrag zu starten ist (höchstens einer gleichzeitig).

        Läuft schon ein Auftrag einer zusätzlichen Messung (Zustand „Laden“, gestartet), gibt es
        keinen neuen; der Aufrufer setzt ``gestartet`` beim Start.
        """
        laden = [m for m in self._liste if m.zustand is MessungsZustand.LADEN]
        if any(m.gestartet for m in laden):
            return None
        for m in laden:
            return m
        return None

    def speicher_mib(self, messung_id: int) -> float:
        """Untergrenze des Speicherbedarfs einer Messung in MiB (Daten plus Paarcache)."""
        m = self._hole(messung_id)
        gesehen: set[int] = set()
        summe = 0
        if m.geladen is not None:
            summe += nbytes_von(m.geladen.messdaten, gesehen)
        if m.cache is not None:
            summe += nbytes_von(list(m.cache.alle_paare()), gesehen)
        return summe / (1024.0 * 1024.0)

    def _hole(self, messung_id: int) -> Messung:
        m = self.finde(messung_id)
        if m is None:
            raise ValueError(f"Messung {messung_id} gibt es nicht.")
        return m
