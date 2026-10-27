"""Reine Anzeigelogik der Oberfläche (Design-Brief P3, Abschnitt 3 und 8), Qt-frei.

Jede Funktion bildet ein ``Zustandsbild`` der Sitzung (bzw. einen Teil davon) auf
Anzeigewerte ab: Aktivierungstabelle (3.3), Hinweisband (3.5), Fortschritt (3.6),
Zeilenstatus (3.4), Kurzform der Änderungen, Eingabeprüfung des Editors. Die Funktionen
haben keinen Zustand und keine Qt-Abhängigkeit; die Widgets rufen sie nur auf.

Den zulässigen Einfügebereich (``Zustandsbild.einfuegen_ab``) und die Angaben für den
Startdialog (``Zustandsbild.start_vorschau``) liefert die Sitzung (U5, B1/B8); die
Oberfläche leitet sie nicht selbst ab. Zieldateinamen außerhalb des Startdialogs werden
**nicht** nachgebildet.
"""

from __future__ import annotations

import math
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from pathlib import PurePath, PureWindowsPath
from uuid import UUID

from ldv_automation.domaene import KATALOG, Parameterkatalog, ParameterSpec, ParameterWert
from ldv_automation.gui.tokens import symbol
from ldv_automation.sitzung import (
    Betriebsart,
    DurchgangErgebnis,
    DurchgangZustand,
    EintragBild,
    GeneratorStand,
    GeraeteDiagnose,
    GeraeteStand,
    SitzungsEreignis,
    StartVorschau,
    Voraussetzung,
    Zustandsbild,
)

Z = DurchgangZustand

RUHE_ZUSTAENDE = frozenset({Z.BEREIT, Z.BEENDET})
"""Zustände ohne laufenden Durchgang."""

ANLEGEN_ZUSTAENDE = frozenset(
    {
        Z.BEREIT,
        Z.LAEUFT,
        Z.PAUSE_ANGEFORDERT,
        Z.PAUSIERT,
        Z.WARTET_AUF_BESTAETIGUNG,
        Z.WARTET_AUF_ENTSCHEIDUNG,
        Z.BEENDET,
    }
)
"""Zustände, in denen Einträge angelegt, geändert, verschoben und entfernt werden dürfen."""

ABBRECHEN_ZUSTAENDE = frozenset(
    {
        Z.LAEUFT,
        Z.PAUSE_ANGEFORDERT,
        Z.PAUSIERT,
        Z.WARTET_AUF_BESTAETIGUNG,
        Z.WARTET_AUF_ENTSCHEIDUNG,
    }
)
"""Zustände, in denen Abbrechen möglich ist (Tabelle 3.3, gleich Sitzung.brich_ab)."""

SCHLIESSEN_GESPERRT = frozenset({Z.LAEUFT, Z.PAUSE_ANGEFORDERT, Z.ABBRUCH_LAEUFT})
"""Zustände, in denen das Fenster nicht geschlossen werden darf (3.13)."""

BETRIEBSART_WORT: Mapping[Betriebsart, str] = {
    Betriebsart.SIMULATOR: "SIMULATOR",
    Betriebsart.NUR_LESEN: "NUR LESEN",
    Betriebsart.TROCKENLAUF: "TROCKENLAUF",
    Betriebsart.MESSEN: "MESSEN",
}

BETRIEBSART_TOOLTIP: Mapping[Betriebsart, str] = {
    Betriebsart.SIMULATOR: "Alle Aktionen laufen gegen den Simulator. Keine Verbindung zur PSV.",
    Betriebsart.NUR_LESEN: (
        "Verbindung und Lesen. Es werden keine Einträge ausgeführt, nichts wird in die PSV "
        "geschrieben."
    ),
    Betriebsart.TROCKENLAUF: (
        "Einstellungen werden in die PSV geladen und gelesen, es wird nicht gescannt. Ändert "
        "die aktuellen PSV-Einstellungen."
    ),
    Betriebsart.MESSEN: (
        "Echte Messung. Die Freigabe gilt für diese Sitzung; jeder Durchgang braucht eine "
        "Bestätigung."
    ),
}

FEHLERSTRATEGIE_VERMERK = "Fehlerstrategie: vorläufig (O1)"
FEHLERSTRATEGIE_TOOLTIP = "Verhalten bei Fehlern ist mit dem Betreuer noch zu klären (O1/F20)."

LEER_TEXT = "Noch keine Messung. Mit „+ Messung“ anlegen oder eine Warteschlange laden."
UNZULAESSIGE_NAMENSZEICHEN = '\\/:*?"<>|'
"""Zeichen, die im Namen einer Messung nicht vorkommen dürfen (Teil des Dateinamens)."""

WARTEND = "wartend"


# --- Hilfen über die Einträge ----------------------------------------------------------------


@dataclass(frozen=True)
class Nr:
    """Anzeige der Nummer einer Messung (= Präfix ``<nn>`` des Dateinamens).

    ``endgueltig`` ist ``True``, wenn die Sitzung die Nummer vergeben hat
    (``EintragBild.nummer``); sonst ist ``wert`` eine vorläufige Schätzung.
    """

    wert: int
    endgueltig: bool

    @property
    def kurz(self) -> str:
        """Tabellenspalte: „01“ bzw. vorläufig „(02)“."""
        return f"{self.wert:02d}" if self.endgueltig else f"({self.wert:02d})"

    @property
    def lang(self) -> str:
        """Fließtext: „01“ bzw. vorläufig „02 (vorl.)“."""
        return f"{self.wert:02d}" if self.endgueltig else f"{self.wert:02d} (vorl.)"


def nummern_bild(bild: Zustandsbild) -> dict[UUID, Nr]:
    """:func:`nummern` für ein Zustandsbild (Schätzung abhängig vom Durchgangszustand)."""
    return nummern(
        bild.eintraege,
        durchgang_aktiv=bild.durchgang not in RUHE_ZUSTAENDE,
        durchgangsordner=bild.durchgangsordner,
    )


NR_VORLAEUFIG_TOOLTIP = (
    "Vorläufige Nummer. Die Dateinummer vergibt der Durchgang, wenn er die Messung startet."
)


def _im_ordner(datei: str | None, ordner: str | None) -> bool:
    """Prüft, ob ``datei`` im Ordner ``ordner`` liegt (Durchgangsordner, Plan 4.2)."""
    if not datei or not ordner:
        return False
    return PurePath(datei).is_relative_to(PurePath(ordner))


def nummern(
    eintraege: Sequence[EintragBild],
    *,
    durchgang_aktiv: bool = False,
    durchgangsordner: str | None = None,
) -> dict[UUID, Nr]:
    """Nummer jeder Messung; Pausenpunkte zählen nicht.

    Endgültig ist die von der Sitzung vergebene Dateinummer (``EintragBild.nummer``) eines
    gestarteten Eintrags. Vor der Vergabe wird geschätzt: Rang unter den wartenden Messungen,
    fortgezählt ab der höchsten Nummer des **aktuellen** Durchgangs. Zum aktuellen Durchgang
    gehören die laufende Messung und Messungen, deren Messdatei im Durchgangsordner liegt;
    Nummern früherer Durchgänge zählen nicht (die Sitzung zählt je Durchgang ab 01). Ohne
    laufenden Durchgang ist die Basis 0. Der Wert bleibt als vorläufig gekennzeichnet, weil
    sich die Warteschlange bis zum Start noch ändern kann.
    """
    basis = 0
    if durchgang_aktiv:
        aktuell = [
            e.nummer
            for e in eintraege
            if e.art == "messung"
            and e.nummer is not None
            and e.zustand != WARTEND
            and (e.zustand == "laeuft" or _im_ordner(e.messdatei, durchgangsordner))
        ]
        basis = max(aktuell, default=0)
    ergebnis: dict[UUID, Nr] = {}
    rang = 0
    for e in eintraege:
        if e.art != "messung":
            continue
        if e.nummer is not None and e.zustand != WARTEND:
            ergebnis[e.id] = Nr(e.nummer, True)
        else:
            rang += 1
            ergebnis[e.id] = Nr(basis + rang, False)
    return ergebnis


def finde(eintraege: Sequence[EintragBild], eintrag_id: UUID | None) -> EintragBild | None:
    """Eintrag mit ``eintrag_id`` oder ``None``."""
    if eintrag_id is None:
        return None
    return next((e for e in eintraege if e.id == eintrag_id), None)


def index_von(eintraege: Sequence[EintragBild], eintrag_id: UUID | None) -> int | None:
    """Index des Eintrags mit ``eintrag_id`` oder ``None``."""
    if eintrag_id is None:
        return None
    return next((i for i, e in enumerate(eintraege) if e.id == eintrag_id), None)


def laufende_messung(bild: Zustandsbild) -> EintragBild | None:
    """Die Messung im Zustand ``laeuft`` oder ``None``."""
    return next((e for e in bild.eintraege if e.art == "messung" and e.zustand == "laeuft"), None)


def einfuegeposition(bild: Zustandsbild, auswahl_index: int | None) -> int:
    """Einfügeposition: hinter der Auswahl, ohne Auswahl am Ende, nie vor Gestartetes.

    Die Untergrenze ist der von der Sitzung gelieferte Einfügebereich
    (``Zustandsbild.einfuegen_ab``, Brief 1 „Einfügeposition“).
    """
    eintraege = bild.eintraege
    wunsch = len(eintraege) if auswahl_index is None else auswahl_index + 1
    wunsch = min(max(wunsch, 0), len(eintraege))
    return max(wunsch, bild.einfuegen_ab)


def einfuegeort_text(
    eintraege: Sequence[EintragBild],
    position: int,
    *,
    durchgang_aktiv: bool = False,
    ordner: str | None = None,
) -> str:
    """Zeile im Editor-Modus „Neu“: „wird eingefügt nach Nr 2“, „am Anfang“, „am Ende“."""
    if position <= 0 or not eintraege:
        return "wird eingefügt am Anfang"
    if position >= len(eintraege):
        return "wird eingefügt am Ende"
    vorher = eintraege[position - 1]
    if vorher.art == "messung":
        nr = nummern(eintraege, durchgang_aktiv=durchgang_aktiv, durchgangsordner=ordner)[vorher.id]
        return f"wird eingefügt nach Nr {nr.lang}"
    return f"wird eingefügt nach dem Pausenpunkt „{vorher.text}“"


def wartende_messungen(bild: Zustandsbild) -> list[EintragBild]:
    """Alle wartenden Messungen in Tabellenreihenfolge."""
    return [e for e in bild.eintraege if e.art == "messung" and e.zustand == WARTEND]


# --- Statuszeile -----------------------------------------------------------------------------


def fenstertitel(bild: Zustandsbild) -> str:
    """Fenstertitel mit Betriebsart, z. B. „LDV-Warteschlange – MESSEN“."""
    return f"LDV-Warteschlange – {BETRIEBSART_WORT[bild.betriebsart]}"


def durchgang_text(bild: Zustandsbild) -> str:
    """Text hinter „Durchgang:“ in der Statuszeile (Tabelle 3.3)."""
    z = bild.durchgang
    if z is Z.LAEUFT or z is Z.PAUSE_ANGEFORDERT:
        lauf = laufende_messung(bild)
        if lauf is None:
            return "Läuft" if z is Z.LAEUFT else "Pause angefordert"
        nr = nummern_bild(bild)[lauf.id]
        if z is Z.LAEUFT:
            gesamt = nr.wert + len(wartende_messungen(bild))
            return f"Läuft · Messung {nr.lang} von {gesamt:02d}"
        return f"Pause angefordert · Messung {nr.lang} läuft zu Ende"
    if z is Z.BEENDET:
        if bild.ergebnis is DurchgangErgebnis.ABGEBROCHEN:
            return "Beendet (abgebrochen)"
        if bild.ergebnis is DurchgangErgebnis.GERAET_UNKLAR:
            return "Beendet (Gerätezustand unklar)"
        return "Beendet (vollständig)"
    texte = {
        Z.BEREIT: "Bereit",
        Z.PAUSIERT: "Pausiert",
        Z.WARTET_AUF_BESTAETIGUNG: "Wartet auf Bestätigung (Pausenpunkt)",
        Z.WARTET_AUF_ENTSCHEIDUNG: "Wartet auf Entscheidung (Fehler)",
        Z.ABBRUCH_LAEUFT: "Abbruch läuft …",
        Z.GERAET_UNKLAR: "Gerätezustand unklar",
    }
    return texte[z]


def verbindung_text(bild: Zustandsbild) -> str:
    """Verbindungstext in Zone A (3.2)."""
    info = bild.verbindung
    if bild.betriebsart is Betriebsart.SIMULATOR:
        return "Simulator aktiv" if info is not None else "Simulator nicht verbunden"
    if info is None:
        return "PSV nicht verbunden"
    return f"PSV {info.psv_version} verbunden · Gerät: {info.zustand.value}"


# --- Aktivierung (Tabelle 3.3) ---------------------------------------------------------------


@dataclass(frozen=True)
class Knopf:
    """Aktivierungszustand eines Bedienelements.

    ``grund`` ist bei deaktivierten Elementen der Tooltip-Grund; ``text`` eine abweichende
    Beschriftung (``None`` = Standardbeschriftung).
    """

    aktiv: bool
    grund: str = ""
    text: str | None = None


def _zustandsgrund(z: DurchgangZustand) -> str:
    if z is Z.ABBRUCH_LAEUFT:
        return "Während des Abbruchs nicht möglich"
    if z is Z.GERAET_UNKLAR:
        return "Gerätezustand unklar: zuerst die Verbindung trennen"
    return "Während eines Durchgangs nicht möglich"


def _start(bild: Zustandsbild) -> Knopf:
    text = "Start"
    z = bild.durchgang
    if z not in RUHE_ZUSTAENDE:
        return Knopf(False, f"Start nicht möglich: {_zustandsgrund(z)}.", text)
    if bild.betriebsart is Betriebsart.NUR_LESEN:
        return Knopf(
            False, "Start nicht möglich: Betriebsart NUR LESEN führt keine Einträge aus.", text
        )
    if not wartende_messungen(bild):
        return Knopf(False, "Start nicht möglich: keine wartende Messung.", text)
    if bild.verbindung is None:
        if bild.betriebsart is Betriebsart.SIMULATOR:
            return Knopf(False, "Start nicht möglich: Simulator nicht verbunden.", text)
        return Knopf(False, "Start nicht möglich: keine Verbindung zur PSV („Verbinden“).", text)
    if bild.messdaten_wurzel is None:
        return Knopf(
            False, "Start nicht möglich: kein Messdaten-Ordner gesetzt („Einstellungen …“).", text
        )
    return Knopf(True, "", text)


def _pause(z: DurchgangZustand) -> Knopf:
    if z is Z.LAEUFT:
        return Knopf(True, "", "Pausieren (F6)")
    if z is Z.PAUSIERT:
        return Knopf(True, "", "Fortsetzen (F6)")
    if z is Z.PAUSE_ANGEFORDERT:
        return Knopf(False, "Pause ist bereits angefordert.", "Pause angefordert")
    if z in RUHE_ZUSTAENDE:
        return Knopf(False, "Kein Durchgang läuft.", "Pausieren (F6)")
    return Knopf(False, f"Im Zustand „{durchgang_text_kurz(z)}“ nicht möglich.", "Pausieren (F6)")


def durchgang_text_kurz(z: DurchgangZustand) -> str:
    """Kurzname eines Durchgangszustands für Tooltips."""
    return {
        Z.BEREIT: "Bereit",
        Z.LAEUFT: "Läuft",
        Z.PAUSE_ANGEFORDERT: "Pause angefordert",
        Z.PAUSIERT: "Pausiert",
        Z.WARTET_AUF_BESTAETIGUNG: "Wartet auf Bestätigung",
        Z.WARTET_AUF_ENTSCHEIDUNG: "Wartet auf Entscheidung",
        Z.ABBRUCH_LAEUFT: "Abbruch läuft",
        Z.GERAET_UNKLAR: "Gerätezustand unklar",
        Z.BEENDET: "Beendet",
    }[z]


def _eintrag_grund(e: EintragBild) -> str:
    if e.zustand == "laeuft":
        return "Eintrag läuft bereits"
    if e.art == "pausenpunkt":
        return {
            "erreicht": "Pausenpunkt ist erreicht",
            "erledigt": "Pausenpunkt ist bereits bestätigt",
        }.get(e.zustand, "Eintrag ist nicht mehr wartend")
    return {
        "fertig": "Eintrag ist bereits fertig",
        "fehler": "Eintrag ist mit Fehler beendet",
        "abgebrochen": "Eintrag wurde abgebrochen",
    }.get(e.zustand, "Eintrag ist nicht mehr wartend")


def bedienbarkeit(bild: Zustandsbild, auswahl: UUID | None) -> dict[str, Knopf]:
    """Aktivierung aller Bedienelemente nach Tabelle 3.3 und 3.2.

    Parameters
    ----------
    bild : Zustandsbild
        Aktuelles Zustandsbild.
    auswahl : uuid.UUID or None
        ID des gewählten Eintrags.

    Returns
    -------
    dict
        Schlüssel ``start``, ``pause``, ``abbrechen``, ``messung_neu``, ``pausenpunkt_neu``,
        ``entfernen``, ``hoch``, ``runter``, ``uebernehmen``, ``laden``, ``speichern``,
        ``betriebsart``, ``verbinden``, ``geraet``, ``einstellungen``.
    """
    z = bild.durchgang
    k: dict[str, Knopf] = {}
    k["start"] = _start(bild)
    k["pause"] = _pause(z)
    k["abbrechen"] = (
        Knopf(True, "", "Abbrechen …")
        if z in ABBRECHEN_ZUSTAENDE
        else Knopf(False, "Kein Durchgang zum Abbrechen.", "Abbrechen …")
        if z in RUHE_ZUSTAENDE
        else Knopf(False, f"{_zustandsgrund(z)}.", "Abbrechen …")
    )
    anlegen = z in ANLEGEN_ZUSTAENDE
    k["messung_neu"] = Knopf(anlegen, "" if anlegen else f"{_zustandsgrund(z)}.")
    k["pausenpunkt_neu"] = Knopf(anlegen, "" if anlegen else f"{_zustandsgrund(z)}.")

    eintraege = bild.eintraege
    index = index_von(eintraege, auswahl)
    if not anlegen:
        grund = f"{_zustandsgrund(z)}."
        for name in ("entfernen", "hoch", "runter", "uebernehmen"):
            k[name] = Knopf(False, grund)
    elif index is None:
        for name in ("entfernen", "hoch", "runter", "uebernehmen"):
            k[name] = Knopf(False, "Kein Eintrag gewählt.")
    else:
        e = eintraege[index]
        if e.zustand != WARTEND:
            grund = _eintrag_grund(e) + "."
            for name in ("entfernen", "hoch", "runter", "uebernehmen"):
                k[name] = Knopf(False, grund)
        else:
            anfang = bild.einfuegen_ab
            k["entfernen"] = Knopf(True)
            k["uebernehmen"] = Knopf(True)
            k["hoch"] = (
                Knopf(True)
                if index - 1 >= anfang
                else Knopf(False, "Schon am Anfang der wartenden Einträge.")
            )
            k["runter"] = (
                Knopf(True)
                if index + 1 < len(eintraege) and index + 1 >= anfang
                else Knopf(False, "Schon am Ende der Liste.")
            )

    ruhe = z in RUHE_ZUSTAENDE
    k["laden"] = Knopf(ruhe, "" if ruhe else "Während eines Durchgangs nicht möglich.")
    k["speichern"] = Knopf(True)
    k["betriebsart"] = Knopf(ruhe, "" if ruhe else "Während eines Durchgangs nicht änderbar")
    if z is Z.GERAET_UNKLAR:
        k["verbinden"] = Knopf(True, "", "Trennen")
    elif bild.betriebsart is Betriebsart.SIMULATOR:
        k["verbinden"] = Knopf(
            False,
            "Im SIMULATOR verbindet sich die Oberfläche selbst.",
            "Trennen" if bild.verbunden else "Verbinden",
        )
    else:
        k["verbinden"] = Knopf(
            ruhe,
            "" if ruhe else "Während eines Durchgangs nicht möglich.",
            "Trennen" if bild.verbunden else "Verbinden",
        )
    k["geraet"] = (
        Knopf(False, "Gerätezustand unklar: zuerst die Verbindung trennen.")
        if z is Z.GERAET_UNKLAR
        else Knopf(True)
    )
    k["einstellungen"] = Knopf(ruhe, "" if ruhe else "Während eines Durchgangs nicht möglich.")
    return k


# --- Zeilenstatus (3.4) ----------------------------------------------------------------------


@dataclass(frozen=True)
class ZeilenStatus:
    """Statuszelle: Text (Symbol, Leerzeichen, Wort) und Stil.

    ``stil`` ist ``"normal"``, ``"laeuft"``, ``"ok"``, ``"fehler"`` oder ``"warn"``.
    """

    text: str
    stil: str


def zeilenstatus(e: EintragBild) -> ZeilenStatus:
    """Statusanzeige eines Eintrags (Tabelle 3.4).

    Raises
    ------
    ValueError
        Bei unbekanntem Zustand.
    """
    if e.art == "pausenpunkt":
        if e.zustand == WARTEND:
            return ZeilenStatus(f"{symbol('pause')} Pausenpunkt", "normal")
        if e.zustand == "erreicht":
            return ZeilenStatus(f"{symbol('pause')} wartet auf Bestätigung", "warn")
        if e.zustand == "erledigt":
            return ZeilenStatus(f"{symbol('fertig')} bestätigt", "normal")
    else:
        if e.zustand == WARTEND:
            zusatz = f" (Versuch {e.versuch})" if e.versuch is not None and e.versuch > 1 else ""
            return ZeilenStatus(f"{symbol('wartend')} wartend{zusatz}", "normal")
        if e.zustand == "laeuft":
            return ZeilenStatus(f"{symbol('laeuft')} läuft", "laeuft")
        if e.zustand == "fertig":
            zusatz = " (Trockenlauf)" if e.trockenlauf else ""
            return ZeilenStatus(f"{symbol('fertig')} fertig{zusatz}", "ok")
        if e.zustand == "fehler":
            zusatz = " (übersprungen)" if e.uebersprungen else ""
            return ZeilenStatus(f"{symbol('fehler')} Fehler{zusatz}", "fehler")
        if e.zustand == "abgebrochen":
            return ZeilenStatus(f"{symbol('abgebrochen')} abgebrochen", "normal")
    raise ValueError(f"Unbekannter Zustand {e.zustand!r} für {e.art}")


# --- Tabellenspalten -------------------------------------------------------------------------


def parameter_bezeichnung(spec: ParameterSpec) -> str:
    """Anzeigename eines Katalogparameters, z. B. ``mittelung.anzahl`` → „Mittelung Anzahl“.

    Aus dem Schlüssel gebildet (Einheitensuffix ``_hz`` u. Ä. entfällt), damit neue
    Katalogeinträge ohne Änderung der Oberfläche erscheinen.
    """
    gruppe, _, name = spec.schluessel.partition(".")
    if not name:
        gruppe, name = "", gruppe
    teile = name.split("_")
    if len(teile) > 1 and spec.einheit and teile[-1].lower() == spec.einheit.lower():
        teile = teile[:-1]
    name_text = " ".join(t.capitalize() for t in teile if t)
    if not gruppe:
        return name_text
    gruppe_text = gruppe.upper() if len(gruppe) <= 3 else gruppe.capitalize()
    return f"{gruppe_text} {name_text}"


def wert_text(wert: ParameterWert, einheit: str = "") -> str:
    """Wert mit Einheit, z. B. „1000 Hz“ (Gleitkomma kompakt mit ``%g``)."""
    text = f"{wert:g}" if isinstance(wert, float) else str(wert)
    return f"{text} {einheit}" if einheit else text


def aenderungen_text(
    parameter: Mapping[str, ParameterWert], katalog: Parameterkatalog = KATALOG
) -> tuple[str, str]:
    """Kurzform und Volltext der geänderten Parameter.

    Returns
    -------
    tuple of str
        ``(kurz, tooltip)``; „–“ bzw. „Keine Änderungen gegenüber der .set“ ohne Parameter.
    """
    if not parameter:
        return "–", "Keine Änderungen gegenüber der Einstellungsdatei."
    kurz: list[str] = []
    voll: list[str] = []
    for schluessel, wert in parameter.items():
        if schluessel in katalog:
            spec = katalog.spec(schluessel)
            name = parameter_bezeichnung(spec)
            kurz.append(f"{name} {wert_text(wert, spec.einheit)}")
            voll.append(f"{name}: {wert_text(wert, spec.einheit)} ({schluessel})")
        else:
            kurz.append(f"{schluessel} {wert_text(wert)}")
            voll.append(f"{schluessel}: {wert_text(wert)}")
    return ", ".join(kurz), "\n".join(voll)


def limit_text(zeitlimit_s: float | None) -> str:
    """Spalte Limit: „600 s“ bzw. „Std.“ (Standard-Zeitlimit der Sitzung)."""
    return "Std." if zeitlimit_s is None else f"{zeitlimit_s:g} s"


def standard_limit_hinweis(standard_zeitlimit_s: float) -> str:
    """Kurzer Hinweis im Editor neben dem Limitfeld (B3, K-U5b); Langform im Tooltip."""
    return f"(Standard: {standard_zeitlimit_s:g} s)"


@dataclass(frozen=True)
class Zeile:
    """Anzeigewerte einer Tabellenzeile."""

    nr: str
    status: ZeilenStatus
    name: str
    einstellungsdatei: str
    einstellungsdatei_tooltip: str
    aenderungen: str
    aenderungen_tooltip: str
    limit: str
    pausenpunkt: bool
    laeuft: bool
    nr_vorlaeufig: bool = False


def zeilen(bild: Zustandsbild, katalog: Parameterkatalog = KATALOG) -> list[Zeile]:
    """Alle Tabellenzeilen in Warteschlangenreihenfolge (Brief 1, Zone D)."""
    nrn = nummern_bild(bild)
    ergebnis: list[Zeile] = []
    for e in bild.eintraege:
        status = zeilenstatus(e)
        if e.art == "pausenpunkt":
            ergebnis.append(
                Zeile(
                    nr="–",
                    status=status,
                    name=f"Pausenpunkt: {e.text}",
                    einstellungsdatei="",
                    einstellungsdatei_tooltip="",
                    aenderungen="",
                    aenderungen_tooltip="",
                    limit="",
                    pausenpunkt=True,
                    laeuft=False,
                )
            )
            continue
        pfad = e.einstellungsdatei or ""
        dateiname = pfad.replace("\\", "/").rsplit("/", 1)[-1]
        if e.set_fehlt:
            datei_text = f"{symbol('warnung')} {dateiname}"
            datei_tip = f"Einstellungsdatei nicht gefunden\n{pfad}"
        else:
            datei_text, datei_tip = dateiname, pfad
        kurz, voll = aenderungen_text(e.parameter, katalog)
        ergebnis.append(
            Zeile(
                nr=nrn[e.id].kurz,
                status=status,
                name=e.name,
                einstellungsdatei=datei_text,
                einstellungsdatei_tooltip=datei_tip,
                aenderungen=kurz,
                aenderungen_tooltip=voll,
                limit=limit_text(e.zeitlimit_s),
                pausenpunkt=False,
                laeuft=e.zustand == "laeuft",
                nr_vorlaeufig=not nrn[e.id].endgueltig,
            )
        )
    return ergebnis


# --- Hinweisband (3.5) -----------------------------------------------------------------------


@dataclass(frozen=True)
class BandKnopf:
    """Knopf im Hinweisband: Schlüssel (``objectName`` ``btn_band_<schluessel>``) und Text."""

    schluessel: str
    text: str
    primaer: bool = False
    tooltip: str = ""


@dataclass(frozen=True)
class Hinweis:
    """Ein Hinweis im Band.

    ``fall`` ist die Nummer aus Tabelle 3.5 (``"1"`` … ``"8"``, ``"6a"``, ``"6b"``),
    ``stil`` ist ``"fehler"``, ``"warn"``, ``"warn_rand"`` oder ``"neutral"``. ``alarm``
    fordert ``QApplication.alert`` an (Fälle 1, 4, 5).
    """

    fall: str
    text: str
    stil: str
    knoepfe: tuple[BandKnopf, ...] = ()
    alarm: bool = False


def _zaehlertext(teile: Sequence[tuple[int, str]]) -> str:
    gewaehlt = [f"{n} {wort}" for n, wort in teile if n > 0]
    return ", ".join(gewaehlt) if gewaehlt else "keine Messung"


def zusammenfassung_text(bild: Zustandsbild) -> str:
    """Text des Falls 7 (Durchgang beendet) aus der Zusammenfassung der Sitzung."""
    z = dict(bild.zusammenfassung or {})
    fertig = z.get("fertig", 0)
    uebersprungen = z.get("uebersprungen", 0)
    fehler = max(z.get("fehler", 0) - uebersprungen, 0)
    abgebrochen = z.get("abgebrochen", 0)
    wartend = z.get("wartend", 0)
    if bild.ergebnis is DurchgangErgebnis.ABGEBROCHEN:
        zaehler = _zaehlertext(
            [
                (fertig, "fertig"),
                (fehler, "Fehler"),
                (uebersprungen, "übersprungen"),
                (abgebrochen, "abgebrochen"),
                (wartend, "nicht gestartet (bleiben wartend)"),
            ]
        )
        return f"{symbol('abgebrochen')} Durchgang abgebrochen: {zaehler}."
    zaehler = _zaehlertext(
        [
            (fertig, "fertig"),
            (fehler, "Fehler"),
            (uebersprungen, "übersprungen"),
            (abgebrochen, "abgebrochen"),
            (wartend, "wartend"),
        ]
    )
    if bild.ergebnis is DurchgangErgebnis.GERAET_UNKLAR:
        return f"{symbol('fehler')} Durchgang beendet (Gerätezustand unklar): {zaehler}."
    return f"{symbol('fertig')} Durchgang beendet: {zaehler}."


ZURUECKSETZEN_KNOPF = BandKnopf(
    "zuruecksetzen",
    "Zurücksetzen",
    tooltip="Alle Einträge wieder auf wartend setzen. Messdateien und Protokolle bleiben erhalten.",
)
"""Knopf „Zurücksetzen“ im Hinweisband (Nachtrag 2026-10-27)."""

ZURUECKSETZEN_TEXT = (
    "Einträge sind bereits ausgeführt (fertig, Fehler oder abgebrochen). Zum erneuten "
    "Ausführen auf wartend zurücksetzen."
)


def echt_gemessen(bild: Zustandsbild) -> int:
    """Anzahl der Messungen, die echt ``fertig`` (nicht Trockenlauf) oder ``abgebrochen`` sind.

    Ist sie > 0, fragt die Oberfläche vor dem Zurücksetzen nach (Nachtrag, UI-30).
    """
    return sum(
        1
        for e in bild.eintraege
        if e.art == "messung"
        and ((e.zustand == "fertig" and not e.trockenlauf) or e.zustand == "abgebrochen")
    )


def zuruecksetzen_frage_text(anzahl: int) -> str:
    """Text der Rückfrage „Warteschlange zurücksetzen?“."""
    return (
        f"{anzahl} Einträge wurden bereits gemessen. Nach dem Zurücksetzen werden sie beim "
        "nächsten Start erneut gemessen, in einem neuen Durchgangsordner. Vorhandene "
        "Messdateien und Protokolle bleiben unverändert."
    )


def hinweis(bild: Zustandsbild, *, beendet_quittiert: bool = False) -> Hinweis | None:
    """Der eine Hinweis für das Band nach der Rangfolge 3.5 (höchster zuerst).

    Parameters
    ----------
    bild : Zustandsbild
        Aktuelles Zustandsbild.
    beendet_quittiert : bool
        ``True``, wenn der Nutzer den Fall 7 dieses Durchgangs mit „Schließen“ ausgeblendet hat.
    """
    z = bild.durchgang
    nrn = nummern_bild(bild)
    if z is Z.GERAET_UNKLAR:
        return Hinweis(
            "1",
            f"{symbol('fehler')} Gerätezustand unklar. Die PSV reagiert nicht wie erwartet. "
            "Bitte PSV am Gerät prüfen. Es werden keine weiteren Befehle an das Gerät gesendet.",
            "fehler",
            (BandKnopf("trennen", "Verbindung trennen"),),
            alarm=True,
        )
    if z is Z.ABBRUCH_LAEUFT:
        return Hinweis(
            "2",
            f"{symbol('warnung')} Abbruch läuft … Die laufende Messung wird gestoppt.",
            "warn",
        )
    if bild.waechter_s is not None:
        return Hinweis(
            "3",
            f"{symbol('warnung')} PSV reagiert nicht seit {bild.waechter_s:.0f} s. "
            "Bitte am Gerät prüfen (Dialog in der PSV?).",
            "warn",
        )
    if z is Z.WARTET_AUF_ENTSCHEIDUNG:
        e = finde(bild.eintraege, bild.fehler_eintrag_id)
        fehlertext = bild.fehlertext or (e.fehlertext if e else None) or "unbekannter Fehler"
        wer = f"Messung {nrn[e.id].lang} „{e.name}“" if e is not None and e.id in nrn else "Messung"
        return Hinweis(
            "4",
            f"{symbol('fehler')} {wer} fehlgeschlagen: {fehlertext}. "
            "Vorläufiges Verhalten (O1): Durchgang angehalten.",
            "fehler",
            (
                BandKnopf("wiederholen", "Wiederholen"),
                BandKnopf("ueberspringen", "Überspringen"),
                BandKnopf("abbrechen", "Durchgang abbrechen …"),
            ),
            alarm=True,
        )
    if z is Z.WARTET_AUF_BESTAETIGUNG:
        p = finde(bild.eintraege, bild.pausenpunkt_id)
        text = p.text if p is not None else "(Pausenpunkt)"
        return Hinweis(
            "5",
            f"{symbol('pause')} Pausenpunkt erreicht: {text}. "
            "Die nächste Messung startet erst nach Bestätigung.",
            "warn_rand",
            (BandKnopf("bestaetigen", "Bestätigen (F7)", primaer=True),),
            alarm=True,
        )
    if z is Z.PAUSE_ANGEFORDERT:
        lauf = laufende_messung(bild)
        wer = f"Messung {nrn[lauf.id].lang}" if lauf is not None else "Die laufende Messung"
        return Hinweis(
            "6a",
            f"{symbol('pause')} Pause angefordert. {wer} läuft zu Ende, danach startet keine neue.",
            "neutral",
        )
    if z is Z.PAUSIERT:
        wartend = wartende_messungen(bild)
        if wartend:
            n = wartend[0]
            naechste = f"Nächste wartende Messung: Nr {nrn[n.id].lang} „{n.name}“."
        else:
            naechste = "Keine wartende Messung mehr."
        return Hinweis(
            "6b",
            f"{symbol('pause')} Durchgang pausiert. {naechste}",
            "neutral",
            (BandKnopf("fortsetzen", "Fortsetzen (F6)"),),
        )
    if z is Z.BEENDET and not beendet_quittiert:
        knoepfe: list[BandKnopf] = []
        if bild.zuruecksetzen_moeglich:
            knoepfe.append(ZURUECKSETZEN_KNOPF)
        if bild.durchgangsordner:
            knoepfe.append(BandKnopf("ordner", "Ordner öffnen"))
        knoepfe.append(BandKnopf("schliessen", "Schließen"))
        return Hinweis("7", zusammenfassung_text(bild), "neutral", tuple(knoepfe))
    if z in RUHE_ZUSTAENDE and bild.zuruecksetzen_moeglich:
        # Fall 7b (Nachtrag 2026-10-27): über Fall 8. Auch in BEENDET nach „Schließen“,
        # damit der Knopf genau dann sichtbar ist, wenn Zurücksetzen möglich ist (UI-29).
        return Hinweis("7b", ZURUECKSETZEN_TEXT, "neutral", (ZURUECKSETZEN_KNOPF,))
    if z in RUHE_ZUSTAENDE:
        if bild.betriebsart is Betriebsart.SIMULATOR:
            return Hinweis(
                "8", "Simulator: Es entstehen Platzhalterdateien, keine Messdaten.", "neutral"
            )
        if bild.betriebsart is Betriebsart.TROCKENLAUF:
            return Hinweis(
                "8",
                "Trockenlauf: Es wird nicht gescannt. Die aktuellen PSV-Einstellungen werden "
                "geändert.",
                "neutral",
            )
    return None


# --- Fortschritt (3.6) -----------------------------------------------------------------------


@dataclass(frozen=True)
class FortschrittAnzeige:
    """Anzeigewerte der Fortschrittszeile.

    ``wert`` in Prozent 0 … 100 oder ``None`` (letzten Stand behalten); ``unbestimmt``
    schaltet den Balken in den Bereich 0 … 0; ``aktiv`` deaktiviert den Balken, wenn
    ``False``.
    """

    beschriftung: str
    wert: int | None
    unbestimmt: bool
    text: str
    aktiv: bool


def dauer_text(sekunden: float) -> str:
    """Grobe Restdauer, z. B. „45 s“ oder „2 min“ (gerundet)."""
    s = max(sekunden, 0.0)
    if s < 90.0:
        return f"{round(s)} s"
    if s < 5400.0:
        return f"{round(s / 60.0)} min"
    return f"{s / 3600.0:.1f} h".replace(".", ",")


def uhr_text(sekunden: float) -> str:
    """Restzeit als ``m:ss`` bzw. ``h:mm:ss`` (abgeschnitten auf ganze Sekunden, ≥ 0)."""
    gesamt = max(math.floor(sekunden), 0) if math.isfinite(sekunden) else 0
    h, rest = divmod(gesamt, 3600)
    m, s = divmod(rest, 60)
    return f"{h}:{m:02d}:{s:02d}" if h else f"{m}:{s:02d}"


def fortschritt_anzeige(bild: Zustandsbild) -> FortschrittAnzeige:
    """Anzeigewerte der Zone F nach Tabelle 3.6."""
    z = bild.durchgang
    nrn = nummern_bild(bild)
    if z in RUHE_ZUSTAENDE:
        return FortschrittAnzeige("", 0, False, "Kein Durchgang läuft.", False)
    if z is Z.GERAET_UNKLAR:
        return FortschrittAnzeige("", None, False, "Gerätezustand unklar.", False)
    if z in (Z.PAUSIERT, Z.WARTET_AUF_BESTAETIGUNG, Z.WARTET_AUF_ENTSCHEIDUNG):
        return FortschrittAnzeige("", None, False, "Zwischen den Messungen.", False)
    f = bild.fortschritt
    lauf = finde(bild.eintraege, f.messung_id) if f is not None else laufende_messung(bild)
    beschriftung = f"Messung {nrn[lauf.id].lang}:" if lauf is not None and lauf.id in nrn else ""
    if f is None:
        if lauf is not None and lauf.zustand == "laeuft":
            return FortschrittAnzeige(beschriftung, None, True, "Messung wird vorbereitet.", True)
        fertig = [e for e in bild.eintraege if e.art == "messung" and e.zustand == "fertig"]
        letzte = max(
            (e for e in fertig if e.zeit_ende is not None),
            key=lambda e: e.zeit_ende,  # type: ignore[arg-type,return-value]  # oben gefiltert
            default=None,
        )
        if letzte is not None:
            nr = nrn[letzte.id].lang
            return FortschrittAnzeige(f"Messung {nr}:", 100, False, f"Messung {nr} fertig.", True)
        return FortschrittAnzeige("", None, False, "Zwischen den Messungen.", True)
    limit = f" · Zeitlimit in {uhr_text(f.zeitlimit_rest_s)}"
    if f.anteil is None:
        return FortschrittAnzeige(beschriftung, None, True, f"Fortschritt unbekannt{limit}", True)
    rest = f" · noch ca. {dauer_text(f.restzeit_s)}" if f.restzeit_s is not None else ""
    if f.geschaetzt:
        if f.anteil >= 1.0:
            return FortschrittAnzeige(
                beschriftung,
                99,
                False,
                f"Schätzung überschritten – Messung läuft noch{limit}",
                True,
            )
        prozent = min(max(math.floor(f.anteil * 100.0), 0), 99)
        return FortschrittAnzeige(
            beschriftung, prozent, False, f"ca. {prozent} % (geschätzt){rest}{limit}", True
        )
    prozent = min(max(math.floor(f.anteil * 100.0), 0), 100)
    return FortschrittAnzeige(
        beschriftung, prozent, False, f"{prozent} % (Quelle: {f.quelle}){rest}{limit}", True
    )


# --- Editor: Eingabeprüfung ------------------------------------------------------------------


def pruefe_name(name: str) -> str | None:
    """Fehlermeldung zum Namen einer Messung oder ``None``, wenn er zulässig ist."""
    if not name.strip():
        return f"{symbol('fehler')} Name: Pflichtfeld."
    if name != name.strip():
        return f"{symbol('fehler')} Name: keine Leerzeichen am Anfang oder Ende."
    falsch = sorted({c for c in name if c in UNZULAESSIGE_NAMENSZEICHEN})
    if falsch:
        return (
            f"{symbol('fehler')} Name: unzulässige Zeichen {' '.join(falsch)} "
            f"(nicht erlaubt: {' '.join(UNZULAESSIGE_NAMENSZEICHEN)})."
        )
    return None


def pruefe_pflichttext(feld: str, text: str) -> str | None:
    """Fehlermeldung für ein leeres Pflichtfeld oder ``None``."""
    return f"{symbol('fehler')} {feld}: Pflichtfeld." if not text.strip() else None


def lies_parameter(spec: ParameterSpec, text: str) -> tuple[ParameterWert | None, str | None]:
    """Liest und prüft eine Parametereingabe gegen den Katalog.

    Gleitkommazahlen dürfen Dezimalkomma oder -punkt haben. Maßgeblich ist der Katalog
    (:meth:`ParameterSpec.pruefe`); die Sitzung prüft beim Übernehmen erneut.

    Returns
    -------
    tuple
        ``(wert, None)`` bei gültiger Eingabe, sonst ``(None, meldung)``.
    """
    name = parameter_bezeichnung(spec)
    roh = text.strip()
    if not roh:
        return None, f"{symbol('fehler')} {name}: Wert fehlt."
    wert: ParameterWert
    if spec.typ == "int":
        try:
            wert = int(roh)
        except ValueError:
            return None, f"{symbol('fehler')} {name}: Ganzzahl erwartet."
    elif spec.typ == "float":
        try:
            wert = float(roh.replace(",", "."))
        except ValueError:
            return None, f"{symbol('fehler')} {name}: Zahl erwartet."
        if not math.isfinite(wert):
            return None, f"{symbol('fehler')} {name}: Zahl muss endlich sein."
    else:
        wert = roh
    try:
        return spec.pruefe(wert), None
    except ValueError:
        return None, (
            f"{symbol('fehler')} {name}: {wert_text(wert)} liegt außerhalb {spec.bereich_text()}."
        )


def zieldatei_text(e: EintragBild | None, name: str) -> str:
    """Zeile „Zieldatei“ im Editor.

    Den Dateinamen vor dem Start bildet erst die Ablaufsteuerung (Nummer im Durchgang,
    Umschreibung des Namens); die Oberfläche bildet ihn nicht nach (Rückfrage U4).
    """
    if e is not None and e.messdatei:
        return f"Zieldatei: {e.messdatei}"
    anzeige = name.strip() or "<Name>"
    return f"Zieldatei: NN_{anzeige}.svd (NN und Schreibweise vergibt der Durchgang)"


# --- Abbrechen, Schließen, Start-Dialog ----------------------------------------------------


def abbruch_laeuft_messung(bild: Zustandsbild) -> bool:
    """Prüft, ob beim Abbruch eine Messung läuft (wählt den Text des Dialogs 3.12)."""
    return bild.durchgang in (Z.LAEUFT, Z.PAUSE_ANGEFORDERT) and laufende_messung(bild) is not None


def definitionen(bild: Zustandsbild) -> tuple[tuple[object, ...], ...]:
    """Definitionen der Einträge (ohne Laufzustand) zum Erkennen ungespeicherter Änderungen."""
    return tuple(
        (
            e.art,
            e.id,
            e.name,
            e.text,
            e.einstellungsdatei,
            tuple(sorted(e.parameter.items())),
            e.zeitlimit_s,
            e.notiz,
        )
        for e in bild.eintraege
    )


def schliessen_entscheidung(bild: Zustandsbild, *, ungespeichert: bool) -> str:
    """Verhalten beim Schließen (3.13): ``"sperren"``, ``"unklar"``, ``"fragen"``, ``"frei"``."""
    if bild.durchgang in SCHLIESSEN_GESPERRT:
        return "sperren"
    if bild.durchgang is Z.GERAET_UNKLAR:
        return "unklar"
    if ungespeichert and bild.eintraege:
        return "fragen"
    return "frei"


def start_dialog(bild: Zustandsbild) -> str:
    """Dialog vor dem Start (3.9): ``"messen"``, ``"trockenlauf"`` oder ``"keiner"``."""
    if bild.betriebsart is Betriebsart.MESSEN:
        return "messen"
    if bild.betriebsart is Betriebsart.TROCKENLAUF:
        return "trockenlauf"
    return "keiner"


# --- Freischaltung MESSEN (3.8) --------------------------------------------------------------


@dataclass(frozen=True)
class VoraussetzungZeile:
    """Eine Zeile der Checkliste im Dialog „Messen freischalten“."""

    text: str
    erfuellt: bool
    detail: str
    abhilfe: str


_VORAUSSETZUNG_ZEILEN: tuple[tuple[str, tuple[str, ...], str], ...] = (
    (
        "Verbindung steht, Gerät gestoppt",
        ("verbindung", "geraet_gestoppt"),
        "Mit „Verbinden“ verbinden; in der PSV darf keine Messung laufen.",
    ),
    (
        "Meldungen unterdrückt (Suppress)",
        ("meldungen_unterdrueckt",),
        "In der PSV „SuppressMessagesForAutomation“ aktivieren und neu verbinden.",
    ),
    (
        "Git-Hash bekannt",
        ("git_hash",),
        "Programm aus dem Repository oder mit Build-Info-Datei starten.",
    ),
    (
        "Messdaten-Ordner gesetzt und beschreibbar",
        ("messdaten_wurzel",),
        "In den Einstellungen setzen.",
    ),
    (
        "Trockenlauf des ersten Eintrags ohne Abweichung in dieser Sitzung",
        ("trockenlauf",),
        "Trockenlauf mit dem ersten Eintrag durchführen.",
    ),
)


def voraussetzung_zeilen(voraussetzungen: Sequence[Voraussetzung]) -> list[VoraussetzungZeile]:
    """Checkliste 3.8 aus den Voraussetzungen der Sitzung (die Oberfläche rechnet nicht selbst).

    Unbekannte Voraussetzungen der Sitzung erscheinen als eigene Zeile, damit keine
    verloren geht.
    """
    nach_name = {v.name: v for v in voraussetzungen}
    zeilen_: list[VoraussetzungZeile] = []
    benutzt: set[str] = set()
    for text, namen, abhilfe in _VORAUSSETZUNG_ZEILEN:
        teile = [nach_name[n] for n in namen if n in nach_name]
        benutzt.update(namen)
        erfuellt = bool(teile) and all(v.erfuellt for v in teile)
        detail = "; ".join(v.text for v in teile) if teile else "Keine Angabe der Sitzung"
        zeilen_.append(VoraussetzungZeile(text, erfuellt, detail, "" if erfuellt else abhilfe))
    for v in voraussetzungen:
        if v.name not in benutzt:
            zeilen_.append(
                VoraussetzungZeile(v.text, v.erfuellt, v.text, "" if v.erfuellt else v.text)
            )
    return zeilen_


# --- Ereignisprotokoll (Zone G) --------------------------------------------------------------

_FEHLER_ARTEN = frozenset({"fehler", "interner_fehler", "waechter_fehler"})
_WARN_ARTEN = frozenset(
    {"waechter", "befehl_verworfen", "trockenlauf_verworfen", "uebersprungen_nach_fehler"}
)
_EIGENE_ZEILE = frozenset(
    {"warteschlange_gespeichert", "warteschlange_geladen", "warteschlange_zurueckgesetzt"}
)
"""Diese Ereignisse protokolliert die Oberfläche selbst im Wortlaut des Briefs (3.7)."""


def protokolltext(ereignis: SitzungsEreignis) -> str | None:
    """Protokolltext eines Sitzungsereignisses (ohne Uhrzeit) oder ``None`` (nicht anzeigen).

    Warnungen beginnen mit „Warnung:“, Fehler mit „Fehler:“ (Brief 1, Zone G).
    """
    if ereignis.art in _EIGENE_ZEILE:
        return None
    if ereignis.art in _FEHLER_ARTEN:
        return f"Fehler: {ereignis.text}"
    if ereignis.art in _WARN_ARTEN:
        return f"Warnung: {ereignis.text}"
    return ereignis.text


# --- Startdialog 3.9 und Gerät 3.10 (Angaben der Sitzung, U5/B1) -----------------------------

UNBEKANNT = "unbekannt"


def _ja_nein(wert: bool | None) -> str:
    return UNBEKANNT if wert is None else "ja" if wert else "nein"


def generator_text(g: GeneratorStand | None) -> str:
    """„GeneratorsOn: nein, Aktiv: nein, Amplitude: 0.5 V“ (unbekannte Werte als „unbekannt“)."""
    if g is None:
        return "GeneratorsOn: unbekannt, Aktiv: unbekannt, Amplitude: unbekannt"
    amplitude = UNBEKANNT if g.amplitude_v is None else f"{g.amplitude_v:g} V"
    text = (
        f"GeneratorsOn: {_ja_nein(g.generatoren_an)}, Aktiv: {_ja_nein(g.aktiv)}, "
        f"Amplitude: {amplitude}"
    )
    if g.anzahl is not None and g.anzahl > 1:
        text += f" (nur Generator 1 von {g.anzahl} gelesen)"
    return text


def generator_kurz(g: GeneratorStand | None) -> str:
    """Tabellenspalte Generator: „aus“, „AKTIV“ oder „unbekannt“."""
    if g is None:
        return UNBEKANNT
    if g.aktiv is True or g.generatoren_an is True:
        return "AKTIV"
    return "aus" if g.unbedenklich else UNBEKANNT


def geraet_generator_text(stand: GeraeteStand | None, *, startdialog: bool = False) -> str:
    """Block „Generator (gelesen …)“ aus dem zuletzt gelesenen Gerätestand.

    Im Startdialog folgt der Hinweis, dass der Wert nur für die zuletzt geladene
    Einstellung gilt; maßgeblich sind die Angaben je Messung in der Tabelle (K-U5b).
    """
    if stand is None:
        text = "Generator (gelesen): unbekannt (kein Gerätestand gelesen)"
    elif stand.fehler is not None:
        text = f"Generator (gelesen {stand.quelle}): unbekannt ({stand.fehler})"
    else:
        text = f"Generator (gelesen {stand.quelle}): {generator_text(stand.generator)}"
    if startdialog:
        text += (
            " – gilt nur für diese Datei bzw. die zuletzt in PSV geladene Einstellung; "
            "maßgeblich sind die Angaben je Messung in der Tabelle."
        )
    return text


def messpunkte_text(stand: GeraeteStand | None) -> str:
    """Zeile Messpunkte im Dialog „Gerät“ (3.10)."""
    if stand is None or stand.messpunkte is None:
        grund = f" ({stand.fehler})" if stand is not None and stand.fehler else ""
        return f"{UNBEKANNT}{grund}"
    return f"{stand.messpunkte} (gelesen {stand.quelle})"


def diagnose_text(diagnose: GeraeteDiagnose | None) -> str:
    """Zeile Aufrufprotokoll im Dialog „Gerät“ (Prüfung T1: ohne Verweigerung)."""
    if diagnose is None:
        return "nicht verfügbar (Simulator)"
    if not diagnose.verweigerungen:
        return f"{diagnose.aufrufe_anzahl} Zugriffe, keine Verweigerung"
    return (
        f"{diagnose.aufrufe_anzahl} Zugriffe, {len(diagnose.verweigerungen)} Verweigerungen:\n"
        + "\n".join(diagnose.verweigerungen)
    )


def start_anzahl_text(vorschau: Sequence[StartVorschau]) -> str:
    """„<n> Messungen, <m> Messpunkte insgesamt (soweit bekannt)“ (Brief 3.9).

    Ist kein Wert bekannt, heißt es „Messpunkte insgesamt: unbekannt“ statt „0“ (K-U5b).
    """
    bekannt = [v.messpunkte for v in vorschau if v.messpunkte is not None]
    if not bekannt:
        return f"{len(vorschau)} Messungen, Messpunkte insgesamt: unbekannt"
    text = f"{len(vorschau)} Messungen, {sum(bekannt)} Messpunkte insgesamt (soweit bekannt"
    offen = len(vorschau) - len(bekannt)
    return text + (f"; bei {offen} Messungen unbekannt)" if offen else ")")


def start_zeile(v: StartVorschau) -> tuple[str, str, str, str, str]:
    """Tabellenzeile Nr · Einstellungsdatei · Zieldatei · Messpunkte · Generator.

    Die Zieldatei erscheint nur als Dateiname; den vollen Pfad zeigt der Tooltip
    (:func:`start_tooltip`). Übernommene Werte sind gekennzeichnet (K-U5b).
    """
    generator = generator_kurz(v.generator)
    if v.uebernommen:
        generator += " (übernommen)"
    return (
        f"{v.nummer:02d}",
        v.einstellungsdatei,
        PureWindowsPath(v.zielpfad).name if v.zielpfad else UNBEKANNT,
        UNBEKANNT if v.messpunkte is None else str(v.messpunkte),
        generator,
    )


def start_tooltip(v: StartVorschau, spalte: int) -> str:
    """Tooltip einer Zelle des Startdialogs (voller Zielpfad, Herkunft der Werte)."""
    wert = start_zeile(v)[spalte]
    if spalte == 2:
        return f"{v.zielpfad or UNBEKANNT}\n{v.hinweis}"
    if spalte == 4:
        return f"{generator_text(v.generator)}\n{v.hinweis}"
    if spalte == 3:
        return f"{wert}\n{v.hinweis}"
    return wert


def generator_warnung(vorschau: Sequence[StartVorschau]) -> str | None:
    """Rote Warnzeile des Startdialogs oder ``None`` (nur bei aktiv oder unbekannt, B1).

    Nennt aktive **und** unbekannte Messungen zugleich (K-U5b).
    """
    aktiv = [
        v
        for v in vorschau
        if v.generator is not None
        and (v.generator.aktiv is True or v.generator.generatoren_an is True)
    ]
    unklar = [v for v in vorschau if not v.generator_unbedenklich and v not in aktiv]
    if not aktiv and not unklar:
        return None
    teile: list[str] = []
    if aktiv:
        teile.append(f"Generator ist aktiv (Nr {', '.join(f'{v.nummer:02d}' for v in aktiv)})")
    if unklar:
        nrn = ", ".join(f"{v.nummer:02d}" for v in unklar)
        teile.append(
            f"Generatorzustand unbekannt (Nr {nrn}; .set mit dem verbundenen Gerät nicht "
            "geladen oder Wert nicht lesbar)"
        )
    return (
        f"{symbol('fehler')} "
        + "; ".join(teile)
        + ". Ein in der .set aktiver Generator startet mit der Messung automatisch. Nur "
        "fortfahren, wenn Shaker/Verstärker freigegeben sind."
    )


def konfiguration_text(info: Mapping[str, object] | None) -> str:
    """Zeile Konfiguration im Dialog „Gerät“: Datei, SHA-256 und verwendete Werte (K-U5)."""
    if info is None:
        return "keine Angabe (Standardwerte der Sitzung)"
    pfad = info.get("pfad")
    sha = info.get("sha256")
    kopf = (
        f"Datei: {pfad} (SHA-256 {str(sha)[:12]}…)"
        if pfad
        else "Standardwerte (keine Konfigurationsdatei)"
    )
    werte = info.get("werte")
    zeilen = [kopf]
    if isinstance(werte, Mapping):
        zeilen.extend(f"{k}: {v}" for k, v in werte.items())
    return "\n".join(zeilen)
