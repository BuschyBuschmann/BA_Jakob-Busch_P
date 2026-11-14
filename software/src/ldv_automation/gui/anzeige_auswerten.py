"""Reine Anzeigelogik des Reiters „Auswerten“ (P-AUSW T3a, Brief K-AUSW), Qt-frei.

Wie :mod:`ldv_automation.gui.anzeige` für die Warteschlange bildet dieses Modul Daten der
Auswertung auf Anzeigewerte ab: Zellen der Parameterzeile (UI-2), Platzhalter- und
Zustandstexte (UI-3, UI-15, UI-24), Aktivierung der Bedienelemente je Zustand,
Prüfzusammenfassung (UI-23), Kennzeichnung unbestätigter Größen (UI-11), Cursortext (UI-13),
Zusätze der Reiterköpfe (UI-20) und Texte der Auswahl von Ansicht 1.

Das Modul importiert zur Laufzeit weder matplotlib noch ``olefile`` noch NumPy: Das Hauptfenster
braucht :func:`reiterkopf_messen` bei jeder Aktualisierung des Reiters „Messen“, und der
matplotlib-Import (etwa 0,6 s) darf den Messbetrieb nichts kosten (Reiter wird erst beim ersten
Aktivieren aufgebaut). Datentypen der Auswertung stehen deshalb nur unter ``TYPE_CHECKING``;
Zahlen formatiert eine kleine eigene Funktion (Dezimalkomma).
"""

from __future__ import annotations

from collections.abc import Iterable, Mapping, Sequence
from dataclasses import dataclass
from enum import Enum
from pathlib import PureWindowsPath
from typing import TYPE_CHECKING

from ldv_automation.gui.anzeige import Knopf
from ldv_automation.gui.tokens import symbol
from ldv_automation.sitzung import DurchgangZustand

if TYPE_CHECKING:
    from ldv_automation.auswertung.annahmen import AnnahmeEintrag
    from ldv_automation.auswertung.laden import Dateieinstellungen
    from ldv_automation.auswertung.plausibilitaet import Antriebsart, Pruefergebnis

__all__ = [
    "ABHAENGIG_VON",
    "ANSICHT_NAMEN",
    "BILD_FREIGESCHALTET",
    "EXPORT_FREIGESCHALTET",
    "FREIGESCHALTETE_ANSICHTEN",
    "NICHT_LESBAR",
    "P08_ANTRIEBSPUNKT",
    "TEXT_KEINE_BAENDER",
    "TEXT_KEINE_DATEI",
    "TEXT_KEINE_FRF",
    "TEXT_KEINE_SPITZEN",
    "TEXT_KEINE_SPITZENSUCHE",
    "TEXT_NAECHSTE_LINIE",
    "TEXT_NICHT_LESBAR",
    "TEXT_PHASE_EINZELKOMPONENTE",
    "TEXT_PHASE_KEINE_REFERENZ",
    "TEXT_PRUEFUNG_ABGEBROCHEN",
    "TEXT_PRUEFUNG_BERECHNET",
    "TEXT_SPITZE_WAEHLEN",
    "TEXT_ZUERST_OEFFNEN",
    "AuswertenZustand",
    "ParameterZelle",
    "ansicht_zugang",
    "bedienbarkeit_auswerten",
    "cursor_text",
    "dateiname_von",
    "fehler_band_text",
    "folgefehler_text",
    "geladen_text",
    "kennzeichen_beschreibung",
    "kennzeichen_text",
    "lade_text",
    "parameter_tooltip",
    "parameter_zellen",
    "phase_ref_text",
    "plot_beschreibung",
    "plotkopf_text",
    "pruefung_fehler_text",
    "pruefung_kern",
    "pruefung_text",
    "punkt_eintraege",
    "reiterkopf_messen",
    "unbestaetigte_annahmen",
    "waehle_antriebspunkt",
    "zeichen_fehler_text",
    "zellen_sichtbar",
]

# --- Texte und Konstanten --------------------------------------------------------------------

NICHT_LESBAR = "–"
"""Anzeige für einen Wert, der in der Datei nicht lesbar ist (kein Raten, UI-2)."""
TEXT_NICHT_LESBAR = "in der Datei nicht lesbar"
"""Tooltip der Zellen mit „–“."""
TEXT_KEINE_DATEI = "Noch keine Messdatei geöffnet."
"""Platzhalter in AE ohne Datei (UI-3)."""
TEXT_ZUERST_OEFFNEN = "Zuerst eine Messdatei öffnen."
"""Tooltip der deaktivierten Elemente ohne Datei (UI-3)."""
TEXT_LAEDT = "Die Datei wird gelesen …"
"""Tooltip der deaktivierten Elemente während des Lesens (UI-15)."""
TEXT_FOLGT = "Noch nicht verfügbar (folgt)."
"""Tooltip der Elemente, die in einem späteren Teilpaket folgen (T3b: Ansichten 2 bis 4, T4:
Export und Bild)."""
TEXT_PRUEFUNG_BERECHNET = "Prüfung: wird berechnet …"
"""Fußzeile während Stufe B des Ladens (Nutzerentscheidung F-3)."""
TEXT_PRUEFUNG_LEER = "Prüfung: –"
"""Fußzeile ohne Datei."""
TEXT_PRUEFUNG_ABGEBROCHEN = "Prüfung: nicht berechnet (abgebrochen)"
"""Fußzeile, wenn Stufe B der angezeigten Datei abgebrochen wurde (neuer Dateiaufruf)."""

TEXT_KEINE_FRF = (
    "Keine Übertragungsfunktion: Die Datei enthält keinen aktiven Referenzkanal. "
    "H1, H2 und Kohärenz brauchen eine Referenz."
)
"""Ansicht 2 ohne Referenz, statt des Plots (UI-6)."""
TEXT_KEINE_SPITZENSUCHE = "Keine Spitzensuche: Referenzkanal fehlt."
"""Spitzentabelle ohne Referenz (U-3)."""
TEXT_KEINE_SPITZEN = "Keine Spitzen gefunden."
"""Spitzentabelle ohne Treffer (UI-24)."""
TEXT_KEINE_BAENDER = "Keine Bänder angegeben."
"""Bändertabelle ohne Band (UI-24)."""
TEXT_PHASE_KEINE_REFERENZ = "Phase nicht verfügbar: keine Referenz."
"""Ansicht 4: Option „Phase“ deaktiviert (UI-10; Wortlaut wie in ``darstellung.schwingform``)."""
TEXT_PHASE_EINZELKOMPONENTE = "Phase nur für eine Einzelkomponente (X, Y oder Z), nicht für 3D."
"""Ansicht 4: Option „Phase“ deaktiviert bei 3D."""
TEXT_SPITZE_WAEHLEN = "Spitze in der Tabelle wählen; ihre Angaben erscheinen hier."
"""Hinweis in der Auswahlspalte von Ansicht 3, wenn Spitzen da sind, aber keine gewählt ist."""
TEXT_NAECHSTE_LINIE = "nächste Linie: {f}"
"""Zeile unter dem Frequenzfeld von Ansicht 4 (``f`` = Frequenztext der Linie)."""

MITTELUNG_SICHERHEIT = "plausibel"
"""Sicherheitsgrad der Mittelung (Test gegen ``svd_lesen.SICHERHEIT['fft.mittelung']``)."""

ANSICHT_NAMEN: Mapping[int, str] = {
    1: "Spektrum",
    2: "H1/H2 und Kohärenz",
    3: "Spitzen und Bänder",
    4: "Schwingform",
    5: "Diagramm",
}
"""Namen der Ansichten (Knopftext „1 Spektrum“, ``accessibleName`` „Ansicht 1: Spektrum“).

Ansicht 5 ist das eigene Diagramm aus Serien (R-058/R-059)."""

FREIGESCHALTETE_ANSICHTEN: frozenset[int] = frozenset({1, 2, 3, 4, 5})
"""Ansichten, die bedienbar sind (alle fünf)."""
EXPORT_FREIGESCHALTET = True
"""``Daten exportieren …`` ist bedienbar (T4)."""
BILD_FREIGESCHALTET = True
"""``Bild speichern …`` ist bedienbar (T4)."""

P08_ANTRIEBSPUNKT: tuple[str, str, Antriebsart] = ("Ref2", "Ref1", "akzeleranz")
"""Treibpunkt für P-08 ``(antwort, referenz, art)`` (Nutzerentscheidung zu P-08): Ref2
(Beschleunigung am Treibpunkt) gegen Ref1 (Kraft)."""

ABHAENGIG_VON: Mapping[str, tuple[tuple[str, str], ...]] = {
    "phase": (("M8", "Polarität der Referenzkanäle offen"),)
}
"""Einzige Zuordnung Größe → Annahmen, von denen sie abhängt (Brief K-AUSW Abschnitt 5, UI-11).

Ist eine zugeordnete Annahme noch nicht bestätigt (``AnnahmeEintrag.ist_annahme``), trägt die
Größe das Kennzeichen „unbestätigt“. Wird die Annahme bestätigt, verschwindet es ohne Änderung
an der Oberfläche."""

_LAUFEND = frozenset(
    {DurchgangZustand.LAEUFT, DurchgangZustand.PAUSE_ANGEFORDERT, DurchgangZustand.ABBRUCH_LAEUFT}
)
"""Zustände, in denen eine Messung läuft oder gestoppt wird (Reiterkopf „▶ läuft“)."""


class AuswertenZustand(Enum):
    """Zustand des Reiters „Auswerten“ (der Lesefehler ist ein Band, kein eigener Zustand)."""

    KEINE_DATEI = "keine_datei"
    LADEN = "laden"
    GELADEN = "geladen"


# --- Zahlen und Namen ------------------------------------------------------------------------


def _komma(wert: float, stellen: int | None = None) -> str:
    """Zahl mit Dezimalkomma; ``stellen=None`` = kürzeste Form (bis 10 signifikante Stellen)."""
    text = f"{wert:.10g}" if stellen is None else f"{wert:.{stellen}f}"
    return text.replace(".", ",")


def dateiname_von(pfad: str) -> str:
    """Dateiname eines Pfads mit Schrägstrich oder Rückwärtsschrägstrich (Messrechner: Windows)."""
    return PureWindowsPath(pfad).name or pfad


# --- Parameterzeile (AB) ---------------------------------------------------------------------


@dataclass(frozen=True)
class ParameterZelle:
    """Eine Zelle der Parameterzeile: Beschriftung über dem Wert (UI-2).

    Attributes
    ----------
    schluessel : str
        ``bandbreite``, ``linien``, ``delta_f``, ``mittelung``, ``fenster``, ``punkte`` oder
        ``referenz`` (``objectName`` ``par_<schluessel>``).
    beschriftung : str
        Kleine Beschriftung über dem Wert.
    wert : str
        Angezeigter Wert; ``NICHT_LESBAR`` („–“), wenn er in der Datei nicht lesbar ist.
    tooltip : str
        Erklärung (leer, wenn der Wert für sich spricht).
    """

    schluessel: str
    beschriftung: str
    wert: str
    tooltip: str = ""


def parameter_zellen(einstellungen: Dateieinstellungen | None) -> tuple[ParameterZelle, ...]:
    """Zellen der Parameterzeile aus den Einstellungen der Datei (nichts Berechnetes).

    Parameters
    ----------
    einstellungen : Dateieinstellungen or None
        Einstellungen der geladenen Datei; ``None`` = keine Datei (alle Werte „–“).

    Returns
    -------
    tuple of ParameterZelle
        Bandbreite, Linien, Δf, Mittelung, Fenster, Punkte, Referenz (in dieser Reihenfolge).
        Die Mittelung steht als „7 (komplex)“ mit dem Sicherheitsgrad „plausibel“ im Tooltip;
        das Fenster ist in der Datei nicht lesbar (``svd_lesen.FENSTER_IN_DATEI_LESBAR``) und
        zeigt „–“. Ohne Referenzkanal steht „keine“ (der Wert ist bekannt).
    """
    if einstellungen is None:
        leer = TEXT_ZUERST_OEFFNEN
        return (
            ParameterZelle("bandbreite", "Bandbreite", NICHT_LESBAR, leer),
            ParameterZelle("linien", "Linien", NICHT_LESBAR, leer),
            ParameterZelle("delta_f", "Δf", NICHT_LESBAR, leer),
            ParameterZelle("mittelung", "Mittelung", NICHT_LESBAR, leer),
            ParameterZelle("fenster", "Fenster", NICHT_LESBAR, leer),
            ParameterZelle("punkte", "Punkte", NICHT_LESBAR, leer),
            ParameterZelle("referenz", "Referenz", NICHT_LESBAR, leer),
        )
    e = einstellungen
    if e.mittelung is None:
        mittelung = ParameterZelle("mittelung", "Mittelung", NICHT_LESBAR, TEXT_NICHT_LESBAR)
    else:
        wert = "aus" if e.mittelung.typ == 0 else f"{e.mittelung.anzahl} ({e.mittelung.typ_name})"
        mittelung = ParameterZelle(
            "mittelung",
            "Mittelung",
            wert,
            f"Mittelungsart und -anzahl aus der Datei. Sicherheitsgrad: {MITTELUNG_SICHERHEIT} "
            f"(bisher an einer Datei gegengeprüft); Anzahl {e.mittelung.anzahl}.",
        )
    if e.referenzen:
        referenz = ", ".join(f"{name} [{einheit}]" for name, einheit in e.referenzen)
        referenz_tipp = "Referenzkanäle der Datei (Name und Einheit)."
    else:
        referenz = "keine"
        referenz_tipp = "Die Datei enthält keinen Referenzkanal."
    return (
        ParameterZelle("bandbreite", "Bandbreite", f"{_komma(e.bandbreite_hz)} Hz"),
        ParameterZelle("linien", "Linien", str(e.linien)),
        ParameterZelle("delta_f", "Δf", f"{_komma(e.delta_f_hz)} Hz"),
        mittelung,
        # Das Fenster ist in der Datei nicht zuordenbar (svd_lesen.FENSTER_IN_DATEI_LESBAR).
        ParameterZelle("fenster", "Fenster", NICHT_LESBAR, TEXT_NICHT_LESBAR),
        ParameterZelle("punkte", "Punkte", str(e.punkte)),
        ParameterZelle("referenz", "Referenz", referenz, referenz_tipp),
    )


def parameter_tooltip(zellen: Sequence[ParameterZelle]) -> str:
    """Tooltip der ganzen Parameterzeile: alle Werte, auch die ausgeblendeten."""
    return "\n".join(f"{z.beschriftung}: {z.wert}" for z in zellen)


def zellen_sichtbar(breiten_px: Sequence[int], verfuegbar_px: int, abstand_px: int = 8) -> int:
    """Anzahl der Zellen von links, die in die verfügbare Breite passen.

    Zu schmal: Zellen werden **rechts** ausgeblendet (Brief K-AUSW Abschnitt 1, AB).

    Parameters
    ----------
    breiten_px : sequence of int
        Breite jeder Zelle in Pixel, in Anzeigereihenfolge.
    verfuegbar_px : int
        Verfügbare Breite in Pixel.
    abstand_px : int, optional
        Abstand zwischen zwei Zellen.
    """
    summe = 0
    anzahl = 0
    for breite in breiten_px:
        neu = summe + (abstand_px if anzahl else 0) + breite
        if neu > verfuegbar_px:
            break
        summe = neu
        anzahl += 1
    return anzahl


# --- Zustände und Aktivierung ----------------------------------------------------------------


def lade_text(dateiname: str) -> str:
    """Text von AE während des Lesens (UI-15)."""
    return f"Lese {dateiname} …"


def fehler_band_text(text: str) -> str:
    """Text des Fehlerbands bei Lesefehler; ``text`` ist die Meldung des Lesers mit Pfad."""
    return f"{symbol('fehler')} Datei kann nicht gelesen werden: {text}"


def geladen_text(pfad: str) -> str:
    """Meldung in der Fußzeile nach erfolgreichem Lesen."""
    return f"Geladen: {pfad}"


def _gesperrt(grund: str) -> Knopf:
    return Knopf(False, grund)


def ansicht_zugang(ansicht: int, zustand: AuswertenZustand) -> Knopf:
    """Aktivierung des Ansichtsknopfs ``ansicht`` (1 bis 4) im Zustand ``zustand``."""
    if zustand is AuswertenZustand.KEINE_DATEI:
        return _gesperrt(TEXT_ZUERST_OEFFNEN)
    if zustand is AuswertenZustand.LADEN:
        return _gesperrt(TEXT_LAEDT)
    if ansicht not in FREIGESCHALTETE_ANSICHTEN:
        return _gesperrt(TEXT_FOLGT)
    return Knopf(True)


def bedienbarkeit_auswerten(zustand: AuswertenZustand) -> dict[str, Knopf]:
    """Aktivierungstabelle der Bedienelemente des Reiters (Brief K-AUSW Abschnitt 6).

    Schlüssel: ``oeffnen``, ``export``, ``bild``, ``auswahl`` (Zone AD) und ``ansicht_1`` bis
    ``ansicht_4``. Deaktivierte Elemente tragen den Grund für den Tooltip.

    Parameters
    ----------
    zustand : AuswertenZustand
        Keine Datei, Laden oder geladen.
    """
    if zustand is AuswertenZustand.KEINE_DATEI:
        grund = TEXT_ZUERST_OEFFNEN
        tabelle = {
            "oeffnen": Knopf(True),
            "export": _gesperrt(grund),
            "bild": _gesperrt(grund),
            "auswahl": _gesperrt(grund),
        }
    elif zustand is AuswertenZustand.LADEN:
        tabelle = {
            "oeffnen": _gesperrt(TEXT_LAEDT),
            "export": _gesperrt(TEXT_LAEDT),
            "bild": _gesperrt(TEXT_LAEDT),
            "auswahl": _gesperrt(TEXT_LAEDT),
        }
    else:
        tabelle = {
            "oeffnen": Knopf(True),
            "export": Knopf(True) if EXPORT_FREIGESCHALTET else _gesperrt(TEXT_FOLGT),
            "bild": Knopf(True) if BILD_FREIGESCHALTET else _gesperrt(TEXT_FOLGT),
            "auswahl": Knopf(True),
        }
    for nr in ANSICHT_NAMEN:
        tabelle[f"ansicht_{nr}"] = ansicht_zugang(nr, zustand)
    return tabelle


# --- Prüfzusammenfassung (AF) ----------------------------------------------------------------

_PRUEF_WORTE: tuple[tuple[str, str, str], ...] = (
    ("fehler", "Fehler", "Fehler"),
    ("warnung", "Warnung", "Warnungen"),
    ("hinweis", "Hinweis", "Hinweise"),
    ("nicht_pruefbar", "nicht prüfbar", "nicht prüfbar"),
    ("ok", "ok", "ok"),
)
"""``(Status, Einzahl, Mehrzahl)`` nach Auffälligkeit geordnet (UI-23): Auffälliges steht vorn,
damit das Kürzen am Ende nie eine Fehler-, Warn- oder Hinweiszahl entfernt."""

_PRUEF_UNAUFFAELLIG = ("ok", "nicht prüfbar")


def pruefung_kern(text: str) -> str:
    """Kürzester Anfang des Prüftextes, der alle Auffälligkeiten (Fehler, Warnung, Hinweis) zeigt.

    Folgen danach nur noch „nicht prüfbar“ und „ok“, steht „, …“ am Ende. Ohne Auffälligkeiten
    bleibt „Prüfung:“ plus erster Teil mit „, …“ (bzw. der ganze Text, wenn er nur einen hat).
    """
    teile = text.split(", ")
    letzt = 0
    for i, teil in enumerate(teile):
        if not teil.endswith(_PRUEF_UNAUFFAELLIG):
            letzt = i
    if letzt == len(teile) - 1:
        return text
    return ", ".join(teile[: letzt + 1]) + ", …"


def pruefung_text(pruefungen: Sequence[Pruefergebnis]) -> str:
    """Zusammenfassung der Plausibilitätsprüfungen als Wörter („Prüfung: 1 Hinweis, 36 ok“).

    Zählungen stehen als Wörter, nie nur als Farbe (UI-23); Status ohne Treffer entfallen.

    Parameters
    ----------
    pruefungen : sequence of Pruefergebnis
        Ergebnisse P-01 bis P-11.
    """
    zaehler: dict[str, int] = {}
    for p in pruefungen:
        zaehler[p.status] = zaehler.get(p.status, 0) + 1
    teile = [
        f"{zaehler[status]} {einzahl if zaehler[status] == 1 else mehrzahl}"
        for status, einzahl, mehrzahl in _PRUEF_WORTE
        if zaehler.get(status)
    ]
    return "Prüfung: " + ", ".join(teile) if teile else TEXT_PRUEFUNG_LEER


def folgefehler_text(fehler: Sequence[str]) -> str:
    """Anhang an eine Fehlermeldung, wenn der Rückfallpfad selbst Fehler hatte (nie spurlos).

    Parameters
    ----------
    fehler : sequence of str
        Texte „Schritt: Ausnahme“ der gescheiterten Rückfallschritte.

    Returns
    -------
    str
        Leer ohne Folgefehler, sonst `` [Folgefehler im Rückfall: …]``.
    """
    return f" [Folgefehler im Rückfall: {'; '.join(fehler)}]" if fehler else ""


def zeichen_fehler_text(text: str) -> str:
    """Text des Fehlerbands, wenn die Darstellung der geladenen Datei scheitert."""
    return f"{symbol('fehler')} Darstellung nicht möglich: {text}"


def pruefung_fehler_text(text: str) -> str:
    """Fußzeilentext, wenn die Prüfung (Stufe B) scheitert."""
    return f"{symbol('fehler')} Prüfung nicht möglich: {text}"


def waehle_antriebspunkt(
    kanalpaare: Iterable[tuple[str, str]],
) -> tuple[str, str, Antriebsart] | None:
    """Treibpunkt für P-08, falls die Datei das Kreuzspektrum dazu enthält.

    Parameters
    ----------
    kanalpaare : iterable of tuple of str
        Kanalpaare ``(Antwort, Referenz)`` mit Kreuzspektrum (``Messdaten.cp``).

    Returns
    -------
    tuple or None
        :data:`P08_ANTRIEBSPUNKT`, wenn das Paar vorhanden ist; sonst ``None`` (P-08 ist dann
        „nicht prüfbar“).
    """
    antwort, referenz, _art = P08_ANTRIEBSPUNKT
    if (antwort, referenz) in set(kanalpaare):
        return P08_ANTRIEBSPUNKT
    return None


# --- Kennzeichnung unbestätigter Größen ------------------------------------------------------


def unbestaetigte_annahmen(
    groesse: str, annahmen: Iterable[AnnahmeEintrag]
) -> tuple[AnnahmeEintrag, ...]:
    """Annahmen, von denen ``groesse`` abhängt und die noch nicht bestätigt sind.

    Quelle der Zuordnung ist :data:`ABHAENGIG_VON`, die Texte stehen in
    ``AnnahmeEintrag.beschreibung``; die Oberfläche schreibt keine Annahme fest. Leer = die
    Größe trägt kein Kennzeichen.

    Parameters
    ----------
    groesse : str
        Schlüssel in :data:`ABHAENGIG_VON`, z. B. ``"phase"``.
    annahmen : iterable of AnnahmeEintrag
        ``Annahmen().eintraege()`` bzw. ``Auswertung.annahmen_liste``.
    """
    nummern = {nr for nr, _kurz in ABHAENGIG_VON.get(groesse, ())}
    return tuple(a for a in annahmen if a.nr in nummern and a.ist_annahme)


def kennzeichen_text(groesse: str, annahmen: Iterable[AnnahmeEintrag]) -> str | None:
    """Kennzeichentext „unbestätigt (M8: …)“ für ``groesse``; ``None`` = kein Kennzeichen.

    Das Symbol ⚠ setzt die Zeichenfunktion davor. Der Kurztext je Annahme steht in
    :data:`ABHAENGIG_VON` (einmalige Quelle), mehrere offene Annahmen stehen durch Semikolon
    getrennt. Die Formel der Annahme (``AnnahmeEintrag.beschreibung``) steht nicht im Bild,
    sondern im Tooltip (:func:`kennzeichen_beschreibung`). Ist die Annahme bestätigt
    (``ist_annahme`` falsch), entfällt das Kennzeichen ohne Codeänderung (UI-11).

    Parameters
    ----------
    groesse : str
        Schlüssel in :data:`ABHAENGIG_VON`.
    annahmen : iterable of AnnahmeEintrag
        ``Annahmen().eintraege()`` bzw. ``Auswertung.annahmen_liste``.
    """
    offen = unbestaetigte_annahmen(groesse, annahmen)
    if not offen:
        return None
    kurz = dict(ABHAENGIG_VON.get(groesse, ()))
    return "unbestätigt (" + "; ".join(f"{a.nr}: {kurz[a.nr]}" for a in offen) + ")"


def kennzeichen_beschreibung(groesse: str, annahmen: Iterable[AnnahmeEintrag]) -> str:
    """Ausführliche Erklärung der offenen Annahmen (Tooltip), leer ohne Kennzeichen.

    Parameters
    ----------
    groesse : str
        Schlüssel in :data:`ABHAENGIG_VON`.
    annahmen : iterable of AnnahmeEintrag
        ``Annahmen().eintraege()`` bzw. ``Auswertung.annahmen_liste``.
    """
    return "\n".join(
        f"{a.nr} (unbestätigt): {a.beschreibung}" for a in unbestaetigte_annahmen(groesse, annahmen)
    )


def phase_ref_text(referenz: str, annahmen: Iterable[AnnahmeEintrag]) -> str:
    """Beschriftung der Option „Phase gegen Referenz“, mit Kennzeichen solange M8 offen ist.

    Beispiel: „Phase gegen Ref1 (⚠ unbestätigt, M8)“. Ist die Annahme bestätigt, entfällt der
    Zusatz ohne Änderung an der Oberfläche (UI-11).
    """
    offen = unbestaetigte_annahmen("phase", annahmen)
    if not offen:
        return f"Phase gegen {referenz}"
    nummern = ", ".join(a.nr for a in offen)
    return f"Phase gegen {referenz} ({symbol('warnung')} unbestätigt, {nummern})"


# --- Cursor, Plotkopf, Textalternative -------------------------------------------------------


def cursor_text(f_hz: float, amplitude: float, einheit: str, auswahl: str, kanal: str) -> str:
    """Cursorzeile „f = 123,750 Hz · Amplitude = 1,23 m/s · Punkt 12 · Vib Z“ (UI-13).

    Der Wert steht in der Einheit der Datei (keine Umrechnung), mit drei signifikanten Stellen;
    außerhalb von 10⁻³ bis 10⁶ als „1,84·10⁻⁵“ (wie an der Farbleiste).

    Parameters
    ----------
    f_hz : float
        Frequenz am Cursor in Hz.
    amplitude : float
        Wert der Kurve in ``einheit``.
    einheit : str
        Einheit der Datei, z. B. ``"m/s"``.
    auswahl : str
        „Punkt 12“ bzw. „Mittel“.
    kanal : str
        Kurve, z. B. „Vib Z“.
    """
    # Lazy: darstellung.formate importiert matplotlib (siehe Moduldoku).
    from ldv_automation.darstellung.formate import frequenz_text, zahl_kurz_text

    return (
        f"f = {frequenz_text(f_hz)} · Amplitude = {zahl_kurz_text(amplitude, 3)} {einheit}"
        f" · {auswahl} · {kanal}"
    )


def plotkopf_text(
    dateiname: str, auswahl_text: str, komponenten: Sequence[str], bezeichnung: str
) -> str:
    """Kopfzeile über dem Plot (Qt-Label, nicht im Bild): Datei, Punkt, Komponenten, Größe."""
    return " · ".join((dateiname, auswahl_text, ", ".join(komponenten), bezeichnung))


def plot_beschreibung(
    ansicht: int,
    dateiname: str,
    auswahl_text: str,
    komponenten: Sequence[str],
    f_min_hz: float,
    f_max_hz: float,
) -> str:
    """Textalternative des Plots (``accessibleDescription``, Brief K-AUSW Abschnitt 10)."""
    return (
        f"Ansicht {ansicht}: {ANSICHT_NAMEN[ansicht]} der Datei {dateiname}, {auswahl_text}, "
        f"Komponenten {', '.join(komponenten)}, Frequenzbereich {_komma(f_min_hz)} bis "
        f"{_komma(f_max_hz)} Hz."
    )


def punkt_eintraege(
    labels: Iterable[int], koordinaten_m: Iterable[Sequence[float]]
) -> tuple[str, ...]:
    """Einträge der Punktliste: „Mittel (alle Punkte)“, dann je Messpunkt mit Koordinaten.

    Parameters
    ----------
    labels : iterable of int
        In der PSV angezeigte Punktnummer je Punkt (``Punkte.label``).
    koordinaten_m : iterable of sequence of float
        Koordinaten ``(x, y, z)`` in m je Punkt (``Punkte.koordinaten_m``).
    """
    zeilen = ["Mittel (alle Punkte)"]
    for label, (x, y, z) in zip(labels, koordinaten_m, strict=True):
        zeilen.append(
            f"Punkt {int(label)} (x {_komma(x, 3)}; y {_komma(y, 3)}; z {_komma(z, 3)} m)"
        )
    return tuple(zeilen)


# --- Reiterköpfe -----------------------------------------------------------------------------


def reiterkopf_messen(fall: str | None, durchgang: DurchgangZustand) -> str:
    """Beschriftung des Reiters „Messen“ mit Zusatzwort (Brief K-AUSW Abschnitt 1, UI-20).

    Fälle 1, 4 und 5 aus dem Hinweisband (P3 3.5) haben Vorrang vor „▶ läuft“. Das Zusatzwort
    folgt auch dem Zustand des Durchgangs, weil ein anderer Hinweis (Fall 3: PSV reagiert nicht)
    das Band belegen kann, während eine Entscheidung oder Bestätigung wartet.

    Parameters
    ----------
    fall : str or None
        ``Hinweis.fall`` des Hinweisbands (``None`` ohne Hinweis).
    durchgang : DurchgangZustand
        Zustand des Durchgangs (``Zustandsbild.durchgang``).
    """
    if fall == "1" or durchgang is DurchgangZustand.GERAET_UNKLAR:
        zusatz = f"{symbol('fehler')} Gerät unklar"
    elif fall == "4" or durchgang is DurchgangZustand.WARTET_AUF_ENTSCHEIDUNG:
        zusatz = f"{symbol('warnung')} Entscheidung nötig"
    elif fall == "5" or durchgang is DurchgangZustand.WARTET_AUF_BESTAETIGUNG:
        zusatz = f"{symbol('warnung')} Bestätigung nötig"
    elif durchgang in _LAUFEND:
        zusatz = f"{symbol('laeuft')} läuft"
    else:
        return "Messen"
    return f"Messen {zusatz}"
