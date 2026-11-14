"""Serien von Ansicht 5 „Diagramm“: Verwaltung ohne Qt (R-058/R-059, P-AUSW2 S7).

Die Liste der Serien (höchstens :data:`SERIEN_MAX`), die Regeln beim Anlegen (keine Dopplung,
Grenze, fester Slot), das Entfernen mit einer Messung, ``Für alle Messungen`` mit Grund je
fehlendem Label (UI-12), die Texte von Kopfzeile, Listenzeile und Textalternative sowie der
Zugriff auf die geöffneten Messungen für die Auflösung
(:func:`~ldv_automation.darstellung.serien_daten.loese_alle_auf`). Das Widget
(:mod:`.auswahl_diagramm`) zeigt das nur an.
"""

from __future__ import annotations

import dataclasses
from collections.abc import Callable, Iterable, Mapping, Sequence

from ldv_automation.auswertung.daten import Messdaten
from ldv_automation.darstellung.auswahl import Groesse, PaarCache
from ldv_automation.darstellung.diagramm import Anordnung
from ldv_automation.darstellung.serien_daten import (
    GROESSEN,
    GROESSEN_NAMEN,
    GroessenId,
    MessungsZugriff,
    SerienSpec,
    verfuegbare_diagramm_groessen,
)
from ldv_automation.gui.messungen import Messung, Messungen

__all__ = [
    "ANORDNUNG_TEXT",
    "SERIEN_MAX",
    "TEXT_KEINE_MESSUNG",
    "TEXT_KEINE_SERIE",
    "TEXT_SERIEN_VOLL",
    "TEXT_SERIE_DOPPELT",
    "SerienFehler",
    "SerienListe",
    "baue_spec",
    "groessen_verfuegbar",
    "komponente_von_paar",
    "kopf_text",
    "messungs_zugriff",
    "paare_je_messung",
    "serie_text",
    "serien_fuer_alle",
    "standard_paar",
    "unmoeglich_text",
]

SERIEN_MAX = 4
"""Höchstzahl der Serien je Diagramm (Linienarten paarweise verschieden)."""
TEXT_SERIE_DOPPELT = "Diese Serie gibt es bereits."
TEXT_SERIEN_VOLL = "Höchstens vier Serien; mehr Serien über „nebeneinander“."
TEXT_KEINE_SERIE = (
    "Noch keine Serie. Mit „+ Serie“ oder „Aus aktueller Ansicht übernehmen“ beginnen."
)
TEXT_KEINE_MESSUNG = "Noch keine Messdatei geöffnet."
ANORDNUNG_TEXT: Mapping[Anordnung, str] = {
    "ueberlagert": "überlagert",
    "nebeneinander": "nebeneinander",
}
"""Anzeigename der Anordnung."""


class SerienFehler(ValueError):  # noqa: N818  (fachlicher Name wie DarstellungsFehler)
    """Eine Serie lässt sich nicht anlegen; ``str(fehler)`` ist der Hinweistext für AD."""


class SerienListe:
    """Die Serien des Diagramms in Reihenfolge der Anzeige.

    Jede Serie bekommt beim Anlegen den **niedrigsten freien Slot** 0 bis 3; er bleibt, wenn eine
    andere Serie entfernt wird (UI-18, UI-20).
    """

    def __init__(self) -> None:
        self._specs: list[SerienSpec] = []

    @property
    def specs(self) -> tuple[SerienSpec, ...]:
        """Alle Serien (auch unsichtbare)."""
        return tuple(self._specs)

    def __len__(self) -> int:
        return len(self._specs)

    @property
    def ist_voll(self) -> bool:
        """:data:`SERIEN_MAX` Serien sind angelegt."""
        return len(self._specs) >= SERIEN_MAX

    def freier_slot(self) -> int | None:
        """Niedrigster freier Slot (``None`` bei voller Liste)."""
        belegt = {s.slot for s in self._specs}
        return next((i for i in range(SERIEN_MAX) if i not in belegt), None)

    def hinzufuegen(self, spec: SerienSpec) -> SerienSpec:
        """Legt eine Serie an (Slot wird vergeben).

        Raises
        ------
        SerienFehler
            Dieselbe Serie gibt es schon (:data:`TEXT_SERIE_DOPPELT`) oder die Liste ist voll
            (:data:`TEXT_SERIEN_VOLL`).
        """
        if any(s.schluessel() == spec.schluessel() for s in self._specs):
            raise SerienFehler(TEXT_SERIE_DOPPELT)
        slot = self.freier_slot()
        if slot is None:
            raise SerienFehler(TEXT_SERIEN_VOLL)
        neu = dataclasses.replace(spec, slot=slot)
        self._specs.append(neu)
        return neu

    def entferne(self, index: int) -> SerienSpec:
        """Entfernt die Serie an Position ``index``."""
        return self._specs.pop(index)

    def setze_sichtbar(self, index: int, sichtbar: bool) -> None:
        """Blendet eine Serie ein oder aus (sie zählt weiter für die Achsenwahl, UI-21)."""
        self._specs[index] = dataclasses.replace(self._specs[index], sichtbar=sichtbar)

    def betroffene(self, messung_id: int) -> int:
        """Zahl der Serien einer Messung (für die Rückfrage vor dem Entfernen, UI-14)."""
        return sum(1 for s in self._specs if s.messung_id == messung_id)

    def entferne_messung(self, messung_id: int) -> int:
        """Entfernt alle Serien einer Messung; Rückgabe: Zahl der entfernten Serien."""
        vorher = len(self._specs)
        self._specs = [s for s in self._specs if s.messung_id != messung_id]
        return vorher - len(self._specs)

    def wandle_groesse(
        self,
        groesse: GroessenId,
        standard: Callable[[int, str | None], tuple[str, str] | None],
    ) -> int:
        """Stellt alle Serien auf eine Größe um (Radioknopf „Größe“ bei überlagerter Anordnung).

        Ein Diagramm hat überlagert **eine** Größe. Beim Umstellen von einer Kanalpaar-Größe auf
        das Spektrum wird die Komponente aus der Antwort des Kanalpaars gebildet; umgekehrt nimmt
        die Serie das Standardkanalpaar der Messung zur Komponente. Serien, die dadurch gleich
        würden, entfallen (die erste bleibt).

        Parameters
        ----------
        groesse : GroessenId
            Neue Größe aller Serien.
        standard : callable
            ``(messung_id, komponente)`` → Standardkanalpaar der Messung (``None`` = keines).

        Returns
        -------
        int
            Zahl der Serien, die als Dopplung entfielen.
        """
        neu: list[SerienSpec] = []
        for s in self._specs:
            if s.groesse == groesse:
                kandidat = s
            elif groesse == "spektrum":
                komp = s.komponente or (
                    komponente_von_paar(s.kanalpaar) if s.kanalpaar is not None else "3D"
                )
                kandidat = dataclasses.replace(s, groesse=groesse, komponente=komp, kanalpaar=None)
            else:
                paar = s.kanalpaar or standard(s.messung_id, s.komponente)
                kandidat = dataclasses.replace(s, groesse=groesse, komponente=None, kanalpaar=paar)
            if all(kandidat.schluessel() != n.schluessel() for n in neu):
                neu.append(kandidat)
        entfallen = len(self._specs) - len(neu)
        self._specs = neu
        return entfallen

    def setze_teilgroesse(self, teilgroesse: str) -> int:
        """Stellt alle Spektren auf |CPH| (``"kohaerent"``) bzw. √AP (``"leistung"``) um.

        Returns
        -------
        int
            Zahl der Serien, die als Dopplung entfielen.
        """
        wert: Groesse = "leistung" if teilgroesse == "leistung" else "kohaerent"
        neu: list[SerienSpec] = []
        for s in self._specs:
            kandidat = dataclasses.replace(s, teilgroesse=wert) if s.groesse == "spektrum" else s
            if all(kandidat.schluessel() != n.schluessel() for n in neu):
                neu.append(kandidat)
        entfallen = len(self._specs) - len(neu)
        self._specs = neu
        return entfallen

    def leere(self) -> None:
        """Entfernt alle Serien."""
        self._specs.clear()


# --- Anlegen ------------------------------------------------------------


def baue_spec(
    messung_id: int,
    punkt_label: int | None,
    groesse: GroessenId,
    *,
    komponente: str | None = None,
    kanalpaar: tuple[str, str] | None = None,
    teilgroesse: str = "kohaerent",
) -> SerienSpec:
    """Bildet eine Serienbeschreibung aus den Angaben des Dialogs.

    Raises
    ------
    SerienFehler
        Das Spektrum braucht eine Komponente, alle anderen Größen ein Kanalpaar.
    """
    if groesse == "spektrum":
        if komponente is None:
            raise SerienFehler("Das Spektrum braucht eine Komponente (X, Y, Z oder 3D).")
        return SerienSpec(
            messung_id,
            punkt_label,
            groesse,
            komponente=komponente,
            teilgroesse="leistung" if teilgroesse == "leistung" else "kohaerent",
        )
    if kanalpaar is None:
        raise SerienFehler(f"{GROESSEN_NAMEN[groesse]} braucht ein Kanalpaar.")
    return SerienSpec(messung_id, punkt_label, groesse, kanalpaar=kanalpaar)


def komponente_von_paar(paar: tuple[str, str]) -> str:
    """Komponente zur Antwort eines Kanalpaars („Vib X“ → „X“); sonst ``"3D"``."""
    antwort = paar[0]
    return antwort[-1] if antwort.startswith("Vib ") and antwort[-1] in "XYZ" else "3D"


def standard_paar(messung: Messung, komponente: str | None) -> tuple[str, str] | None:
    """Standardkanalpaar einer Messung: „Vib <Komponente> / Referenz“, sonst das erste Paar."""
    if not messung.paare:
        return None
    if komponente in ("X", "Y", "Z"):
        kanal = f"Vib {komponente}"
        for paar in messung.paare:
            if paar[0] == kanal:
                return paar
    return messung.paare[0]


def serien_fuer_alle(
    vorlage: SerienSpec, messungen: Iterable[Messung]
) -> tuple[list[SerienSpec], list[str]]:
    """``Für alle Messungen``: je bereiter Messung eine Serie mit derselben Auswahl (UI-12).

    Der Punkt wird über das **Label** zugeordnet; das Mittel gibt es immer. Fehlt das Label (oder
    das Kanalpaar) in einer Messung, wird für sie keine Serie angelegt und der Grund genannt.

    Returns
    -------
    tuple
        ``(Serien, Gründe)``: die Serien mit der Kennung je Messung und je ausgelassener Messung
        ein Text „B: Punkt 105 gibt es nicht.“.
    """
    serien: list[SerienSpec] = []
    gruende: list[str] = []
    for m in messungen:
        if m.geladen is None:
            continue
        labels = {int(x) for x in m.geladen.messdaten.punkte.label}
        if vorlage.punkt_label is not None and vorlage.punkt_label not in labels:
            gruende.append(f"{m.kurzname}: Punkt {vorlage.punkt_label} gibt es nicht.")
            continue
        if vorlage.kanalpaar is not None and vorlage.kanalpaar not in m.paare:
            antwort, referenz = vorlage.kanalpaar
            gruende.append(f"{m.kurzname}: Kanalpaar {antwort} / {referenz} gibt es nicht.")
            continue
        serien.append(dataclasses.replace(vorlage, messung_id=m.id))
    return serien, gruende


def groessen_verfuegbar(messungen: Messungen) -> dict[GroessenId, str | None]:
    """Welche Größen mindestens eine bereite Messung liefert (``None``), sonst der Grund."""
    bereite = messungen.bereite()
    ergebnis: dict[GroessenId, str | None] = {}
    for g in GROESSEN:
        gruende = [
            verfuegbare_diagramm_groessen(m.geladen.messdaten)[g]
            for m in bereite
            if m.geladen is not None
        ]
        ergebnis[g] = None if any(x is None for x in gruende) else (gruende[0] if gruende else "")
    return ergebnis


def messungs_zugriff(messungen: Messungen) -> MessungsZugriff:
    """Zugriff der Auflösung auf die bereiten Messungen (``None`` = Messung fehlt oder lädt)."""

    def zugriff(messung_id: int) -> tuple[Messdaten, PaarCache, str, str] | None:
        m = messungen.finde(messung_id)
        if m is None or m.geladen is None or m.cache is None:
            return None
        return (m.geladen.messdaten, m.cache, m.kurzname, m.dateiname)

    return zugriff


def paare_je_messung(specs: Sequence[SerienSpec]) -> dict[int, int]:
    """Zahl der verschiedenen Kanalpaare, die die Serien je Messung brauchen (Größe des LRU).

    Spektrum als ``|CPH|`` braucht ein Paar je Einzelkomponente (3D: drei); ``√AP`` keines.
    """
    paare: dict[int, set[object]] = {}
    for s in specs:
        belegt = paare.setdefault(s.messung_id, set())
        if s.kanalpaar is not None:
            belegt.add(s.kanalpaar)
        elif s.groesse == "spektrum" and s.teilgroesse == "kohaerent" and s.komponente:
            komponenten = ("X", "Y", "Z") if s.komponente == "3D" else (s.komponente,)
            belegt.update(("komp", c) for c in komponenten)
    return {m: len(p) for m, p in paare.items()}


# --- Texte ------------------------------------------------------------


def serie_text(spec: SerienSpec, kurzname: str, *, mit_groesse: bool = False) -> str:
    """Zeile der Serienliste: „A · Punkt 100 · Vib X / Ref1“ (bei nebeneinander mit Größe)."""
    punkt = "Mittel" if spec.punkt_label is None else f"Punkt {spec.punkt_label}"
    if spec.kanalpaar is not None:
        was = f"{spec.kanalpaar[0]} / {spec.kanalpaar[1]}"
    else:
        c = spec.komponente or ""
        was = c if c == "3D" else f"Vib {c}"
    text = f"{kurzname} · {punkt} · {was}"
    return f"{text} · {GROESSEN_NAMEN[spec.groesse]}" if mit_groesse else text


def unmoeglich_text(spec: SerienSpec, kurzname: str, grund: str, *, symbol: str) -> str:
    """Meldung zu einer nicht darstellbaren Serie (Symbol plus Wort, UI-17)."""
    return f"{symbol} Nicht darstellbar: {serie_text(spec, kurzname)}: {grund}"


def kopf_text(
    kurznamen: Sequence[str], groessen: Sequence[GroessenId], anordnung: Anordnung
) -> str:
    """Kopfzeile von Ansicht 5: Messungen, Größe(n) und Anordnung (Brief 3.2)."""
    mess = ", ".join(kurznamen) if kurznamen else "–"
    gr = ", ".join(GROESSEN_NAMEN[g] for g in dict.fromkeys(groessen)) or "–"
    return f"Diagramm · Messungen {mess} · {gr} · {ANORDNUNG_TEXT[anordnung]}"
