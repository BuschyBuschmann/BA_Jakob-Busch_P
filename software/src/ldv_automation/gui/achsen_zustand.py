"""Zustand der Achsenwahl je Ansicht (R-073, P-AUSW2 S2, ADR-028), ohne Qt.

Eine Quelle für Oberfläche, Werkzeugleiste und Arbeitsbild: je Ansicht und Rolle (``"frequenz"``,
``"betrag"``, ``"phase"``) der Bereich, je Ansicht und Achse die Skala. Ein Bereich mit gesetzter
Seite gilt als „fest“, eine ``None``-Seite als „Auto“. Der Zustand bleibt beim Wechsel von Punkt,
Komponente, Größe, Mittel und Ansicht erhalten (UI-3); nur eine neue Datei setzt die Bereiche
zurück, die Skalen bleiben (UI-6).

Nutzerentscheidung F3 (2026-11-09): Zoom und Verschieben der Werkzeugleiste schreiben feste
Werte (:meth:`AchsenZustand.uebernehme_grenzen`); Zurücksetzen heißt „Auto für die Ansicht“
(:meth:`AchsenZustand.auf_auto`).
"""

from __future__ import annotations

from collections.abc import Mapping

from ldv_automation.darstellung.achsen import AchsenOptionen, Bereich
from ldv_automation.darstellung.zeichnung import Skala

__all__ = [
    "ACHSEN_JE_ANSICHT",
    "ACHSEN_NAMEN",
    "AchsenZustand",
    "einheit_aus_achsentitel",
    "ist_fest",
]

ACHSEN_JE_ANSICHT: Mapping[int, tuple[str, ...]] = {
    1: ("frequenz", "betrag"),
    2: ("frequenz", "betrag", "phase"),
    3: ("frequenz", "betrag"),
}
"""Rollen der Eingabefelder je Ansicht (Brief 3.1). Ansicht 4 hat keine Achsenleiste; eine
weitere Ansicht (R-072) braucht hier nur einen Eintrag. In Ansicht 2 gibt es die Phase nur mit
„Phase anzeigen“ (Auswahl der Oberfläche), die Kohärenz bleibt fest 0 bis 1,05."""

ACHSEN_NAMEN: Mapping[str, str] = {
    "frequenz": "Frequenz",
    "betrag": "Betrag",
    "phase": "Phase",
}
"""Anzeigename je Rolle (Beschriftung der Felder)."""

_VOREINSTELLUNG_SKALA: Mapping[str, Skala] = {"frequenz": "linear", "betrag": "log"}
"""Voreinstellung: Frequenz linear, Amplitude/Betrag logarithmisch (UI-2, OE-2 aus K-AUSW)."""
_SKALA_ACHSEN = frozenset(_VOREINSTELLUNG_SKALA)
"""Achsen mit wählbarer Skala (die Phase ist nur linear)."""


def einheit_aus_achsentitel(titel: str) -> str:
    """Einheit aus einem Achsentitel „Größe [Einheit]“ (leer, wenn keine Klammer vorkommt)."""
    ende = titel.rfind("]")
    anfang = titel.rfind("[", 0, ende) if ende >= 0 else -1
    return titel[anfang + 1 : ende] if anfang >= 0 else ""


def ist_fest(bereich: Bereich) -> bool:
    """Mindestens eine Seite von Hand gesetzt (Feld „fest“, nicht Auto)."""
    return not bereich.ist_auto


class AchsenZustand:
    """Bereiche und Skalen je Ansicht.

    Der Zustand kennt nur Zahlen. Das Prüfen der Eingaben (:func:`pruefe_bereich`) und das
    Neuzeichnen liegen bei der Oberfläche; ein hier gespeicherter Bereich wird von den
    Zeichenfunktionen noch einmal geprüft.
    """

    def __init__(self) -> None:
        self._bereiche: dict[tuple[int, str], Bereich] = {}
        self._skalen: dict[tuple[int, str], Skala] = {}

    # --- Lesen -----------------------------------------------------------------------------

    def bereich(self, ansicht: int, rolle: str) -> Bereich:
        """Bereich der Rolle in der Ansicht (Auto, wenn nie gesetzt)."""
        return self._bereiche.get((ansicht, rolle), Bereich())

    def skala(self, ansicht: int, achse: str) -> Skala:
        """Skala der Achse (``"frequenz"`` oder ``"betrag"``); die Phase ist immer linear."""
        if achse not in _SKALA_ACHSEN:
            return "linear"
        return self._skalen.get((ansicht, achse), _VOREINSTELLUNG_SKALA[achse])

    def optionen(self, ansicht: int) -> AchsenOptionen:
        """Achsenoptionen für die Zeichenfunktion der Ansicht (Frequenz, Skala, y je Rolle).

        Die Skala der Amplitude gehört in ``Optionen.skala`` der Zeichenfunktion
        (:meth:`skala` mit ``"betrag"``), nicht in :class:`AchsenOptionen`.
        """
        rollen = ACHSEN_JE_ANSICHT.get(ansicht, ())
        return AchsenOptionen(
            frequenz=self.bereich(ansicht, "frequenz"),
            frequenz_skala=self.skala(ansicht, "frequenz"),
            y={r: self.bereich(ansicht, r) for r in rollen if r != "frequenz"},
        )

    def hat_feste(self, ansicht: int) -> bool:
        """Mindestens ein Bereich der Ansicht ist fest."""
        return any(ist_fest(b) for (a, _rolle), b in self._bereiche.items() if a == ansicht)

    # --- Schreiben -------------------------------------------------------------------------

    def setze_bereich(self, ansicht: int, rolle: str, bereich: Bereich) -> None:
        """Setzt den Bereich (aus den Feldern der Achsenleiste)."""
        self._bereiche[(ansicht, rolle)] = bereich

    def uebernehme_grenzen(self, ansicht: int, rolle: str, von: float, bis: float) -> None:
        """Schreibt sichtbare Grenzen als feste Werte (Zoom, Verschieben, Verlauf; F3)."""
        self._bereiche[(ansicht, rolle)] = Bereich(float(von), float(bis))

    def setze_skala(self, ansicht: int, achse: str, skala: Skala) -> None:
        """Setzt die Skala von ``"frequenz"`` oder ``"betrag"``.

        Raises
        ------
        ValueError
            Unbekannte Achse (die Phase hat nur die lineare Skala) oder Skala.
        """
        if achse not in _SKALA_ACHSEN:
            raise ValueError(f"Achse {achse!r} hat keine wählbare Skala")
        if skala not in ("linear", "log"):
            raise ValueError(f"unbekannte Skala {skala!r}")
        self._skalen[(ansicht, achse)] = skala

    def auf_auto(self, ansicht: int) -> None:
        """„Alles auf Auto“ und Zurücksetzen: alle Bereiche der Ansicht automatisch.

        Die Skalen bleiben.
        """
        for schluessel in [k for k in self._bereiche if k[0] == ansicht]:
            del self._bereiche[schluessel]

    def alles_auf_auto(self) -> None:
        """Alle Bereiche aller Ansichten automatisch (Skalen bleiben)."""
        self._bereiche.clear()

    def bei_neuer_datei(self) -> None:
        """Neue Datei (Ersetzen): Bereiche zurück, Skalen bleiben (UI-6)."""
        self.alles_auf_auto()
