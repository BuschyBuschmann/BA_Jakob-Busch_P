"""Gestaltungs-Tokens der Oberfläche (Design-Brief P3, Abschnitt 2), Qt-frei.

Alle Farben stehen nur hier als benannte Konstanten. Die Symbole stehen in **einer** Tabelle
mit ASCII-Rückfall (:data:`SYMBOLE_UNICODE`, :data:`SYMBOLE_ASCII`); umgeschaltet wird über
:data:`ASCII_RUECKFALL` bzw. :func:`symbol`. Ob die Unicode-Zeichen am Messrechner
erscheinen, wird dort geprüft (T0).
"""

from __future__ import annotations

from collections.abc import Mapping
from types import MappingProxyType

# --- Farben (Hex, sRGB) ---------------------------------------------------------------------

C_BG = "#F4F3EF"
"""Fensterhintergrund."""
C_FLAECHE = "#FFFFFF"
"""Tabelle, Editor, Protokoll, Eingaben."""
C_LEISTE = "#E7E5DF"
"""Werkzeugleiste, Tabellenkopf, neutrales Hinweisband."""
C_LINIE = "#C9CDD1"
"""Rahmen, Trennlinien."""
C_LINIE_ZEILE = "#E1E3E5"
"""Trennlinien zwischen Tabellenzeilen."""
C_RAND_EINGABE = "#8A9199"
"""Rand von Eingaben und Knöpfen."""
C_TEXT = "#1D2327"
"""Haupttext."""
C_TEXT_GEDAEMPFT = "#5B6670"
"""Nebentext, Einheiten."""
C_AKZENT = "#0B5C73"
"""Primäraktion, laufende Zeile, Fokus, Fortschritt."""
C_AKTIV_BG = "#DCEBF0"
"""Hintergrund der laufenden Zeile."""
C_AUSWAHL_BG = "#DDDAD2"
"""Hintergrund der gewählten Tabellenzeile (neutral, klar verschieden von ``C_AKTIV_BG``)."""
C_OK = "#1F6B3A"
"""Text „fertig“."""
C_WARN_BG = "#FFF1CC"
"""Hinweisband Pausenpunkt/Warnung, erreichter Pausenpunkt."""
C_WARN_RAND = "#8A5A00"
"""Rand des Hinweisbands Pausenpunkt."""
C_FEHLER = "#9C1C1C"
"""Fehler, Abbrechen."""
C_FEHLER_BG = "#FBE9E7"
"""Hintergrund bei Fehler."""
C_STATUSZEILE = "#1D2327"
"""Hintergrund der Statuszeile (Zone A)."""
C_STATUSZEILE_TEXT = "#FFFFFF"
"""Text der Statuszeile."""
C_DEAKTIVIERT_TEXT = "#6B747C"
"""Text deaktivierter Knöpfe und Felder."""
C_DEAKTIVIERT_BG = "#ECEBE6"
"""Hintergrund deaktivierter Knöpfe und Felder."""

# --- Plot (Auswertungsoberfläche, Brief K-AUSW Abschnitt 2) ----------------------------------
# Farben der Plotfläche stehen nur hier; ``gui/plotstil.py`` baut daraus den ``Plotstil`` der
# Zeichenfunktionen. Die Unterscheidung der Serien trägt die Linienart, nicht die Farbe.

C_PLOT_HAUPT = C_AKZENT
"""Erste Kurve, Marker, dunkles Ende des Verlaufs."""
C_PLOT_GITTER = C_LINIE_ZEILE
"""Gitterlinien der Achsen."""
C_PLOT_ACHSE = C_TEXT
"""Achsen, Ticks und Achsentitel."""
C_PLOT_FLAECHE = C_FLAECHE
"""Hintergrund der Achsen und der Figure."""
C_PLOT_BAND = "#E7E5DF"
"""Schattierung von Frequenzbändern (hellgrau; Kurven darauf mindestens 3:1)."""
C_PLOT_VERLAUF_HELL = C_LEISTE
"""Helles Ende des Einfarbverlaufs der Betragsfüllung (Ansicht 4)."""
C_PLOT_SERIE_4 = "#2A7A93"
"""Vierte Serienfarbe (mittlerer Blauton, auf Weiß 4,9:1)."""
PLOT_SERIENFARBEN = (C_PLOT_HAUPT, C_TEXT, C_TEXT_GEDAEMPFT, C_PLOT_SERIE_4)
"""Serienfarben: Helligkeitsstufen zwischen ``C_TEXT`` und ``C_PLOT_SERIE_4`` (kein Gelb, kein
Rot-Grün-Paar). Zusätzlich trägt die Linienart die Unterscheidung."""

PLOT_LINIENARTEN: tuple[tuple[str, str], ...] = (
    ("durchgezogen", "-"),
    ("gestrichelt", "--"),
    ("punktiert", ":"),
    ("strichpunkt", "-."),
)
"""Linienarten je Serie als ``(Name, matplotlib-Linienstil)``, paarweise verschieden."""
PLOT_LINIENBREITE_PT = 1.5
"""Breite der Kurven in der Oberfläche."""

KONTRAST_PAARE: tuple[tuple[str, str, str], ...] = (
    ("text/flaeche", C_TEXT, C_FLAECHE),
    ("text_gedaempft/flaeche", C_TEXT_GEDAEMPFT, C_FLAECHE),
    ("text_gedaempft/bg", C_TEXT_GEDAEMPFT, C_BG),
    ("akzent/flaeche", C_AKZENT, C_FLAECHE),
    ("akzent/aktiv_bg", C_AKZENT, C_AKTIV_BG),
    ("fehler/fehler_bg", C_FEHLER, C_FEHLER_BG),
    ("ok/flaeche", C_OK, C_FLAECHE),
    ("text/warn_bg", C_TEXT, C_WARN_BG),
    ("text/auswahl_bg", C_TEXT, C_AUSWAHL_BG),
    ("akzent/auswahl_bg", C_AKZENT, C_AUSWAHL_BG),
    ("weiss/statuszeile", C_STATUSZEILE_TEXT, C_STATUSZEILE),
    ("weiss/akzent", C_STATUSZEILE_TEXT, C_AKZENT),
    # Auswertungsoberfläche (K-AUSW, UI-22): Plotlinien, Kennzeichen „unbestätigt“, Bänder.
    ("plot_haupt/plot_flaeche", C_PLOT_HAUPT, C_PLOT_FLAECHE),
    ("plot_serie_2/plot_flaeche", PLOT_SERIENFARBEN[1], C_PLOT_FLAECHE),
    ("plot_serie_3/plot_flaeche", PLOT_SERIENFARBEN[2], C_PLOT_FLAECHE),
    ("plot_serie_4/plot_flaeche", PLOT_SERIENFARBEN[3], C_PLOT_FLAECHE),
    ("plot_achse/plot_flaeche", C_PLOT_ACHSE, C_PLOT_FLAECHE),
    ("plot_achse/plot_band", C_PLOT_ACHSE, C_PLOT_BAND),
    ("plot_haupt/plot_band", C_PLOT_HAUPT, C_PLOT_BAND),
    ("text_gedaempft/plot_band", C_TEXT_GEDAEMPFT, C_PLOT_BAND),
    ("warn_rand/warn_bg", C_WARN_RAND, C_WARN_BG),
    ("text/leiste", C_TEXT, C_LEISTE),
    ("fehler/leiste", C_FEHLER, C_LEISTE),
)
"""Text/Hintergrund-Paare, deren Kontrast ≥ 4,5:1 sein muss (UI-23)."""

KONTRAST_PAARE_LINIE: tuple[tuple[str, str, str], ...] = (
    ("plot_serie_2/plot_band", PLOT_SERIENFARBEN[1], C_PLOT_BAND),
    ("plot_serie_3/plot_band", PLOT_SERIENFARBEN[2], C_PLOT_BAND),
    ("plot_serie_4/plot_band", PLOT_SERIENFARBEN[3], C_PLOT_BAND),
    ("akzent/fokus_flaeche", C_AKZENT, C_PLOT_FLAECHE),
)
"""Linien-Paare mit Mindestkontrast ≥ 3:1 (WCAG 1.4.11, Nicht-Text-Kontrast; UI-22)."""

KONTRAST_MINDEST_LINIE = 3.0
"""Mindestkontrast für Linien und Fokusrahmen gegen die Plotfläche."""

KONTRAST_MINDEST_TEXT = 4.5
"""Mindestkontrast für Text nach WCAG 2.x (Brief Abschnitt 7)."""

# --- Schrift und Maße (logische Pixel, Punkt) ------------------------------------------------

SCHRIFT_FAMILIEN = ("Segoe UI", "Arial")
"""Fließtext, mit Rückfall."""
SCHRIFT_FAMILIEN_MONO = ("Consolas", "Courier New")
"""Pfade und Protokoll, mit Rückfall."""
SCHRIFT_PT = 10
SCHRIFT_PT_MONO = 10
SCHRIFT_PT_PROTOKOLL = 9
SCHRIFT_PT_TITEL = 11

HOEHE_STATUSZEILE_PX = 44
HOEHE_WERKZEUGLEISTE_PX = 48
HOEHE_HINWEISBAND_PX = 44
HOEHE_FORTSCHRITT_PX = 30
ZEILENHOEHE_TABELLE_PX = 32
KNOPF_MIN_HOEHE_PX = 32
EINGABE_HOEHE_PX = 28
FENSTERRAND_PX = 12
EDITOR_MIN_BREITE_PX = 340
FENSTER_MIN_BREITE_PX = 1100
FENSTER_MIN_HOEHE_PX = 680
HOEHE_DATEILEISTE_PX = 48
"""Auswerten, Zone AA (Dateileiste)."""
HOEHE_PARAMETERZEILE_PX = 44
"""Auswerten, Zone AB (Parameterzeile, Platz immer reserviert)."""
HOEHE_ANSICHTSWAHL_PX = 32
"""Auswerten, Zone AC (Ansichtswahl)."""
HOEHE_FUSSZEILE_PX = 30
"""Auswerten, Zone AF (Fußzeile)."""
BREITE_AUSWAHLSPALTE_PX = 260
"""Auswerten, Zone AD (Auswahlspalte, fest)."""
PLOT_MIN_BREITE_PX = 600
PLOT_MIN_HOEHE_PX = 320
"""Mindestgröße der Darstellung (AE) bei 1366 x 768 (Brief K-AUSW Abschnitt 1)."""
ABFRAGE_AUSWERTEN_MS = 50
"""Takt, in dem der Reiter „Auswerten“ Hintergrundaufträge abfragt."""
PROTOKOLL_MIN_ZEILEN = 4
PROTOKOLL_MAX_ZEILEN = 8
PROTOKOLL_MAX_BLOCKS = 1000
"""Höchstzahl der Zeilen im Ereignisprotokoll (Zone G)."""
AKTUALISIERUNG_MS = 100
"""Takt, in dem die Oberfläche Zustandsbild und Ereignisse abholt (Brief Abschnitt 4)."""

# --- Symbole -------------------------------------------------------------------------------

SYMBOLE_UNICODE: Mapping[str, str] = MappingProxyType(
    {
        "wartend": "○",
        "laeuft": "▶",
        "fertig": "✔",
        "fehler": "✖",
        "abgebrochen": "■",
        "pause": "⏸",
        "warnung": "⚠",
    }
)
SYMBOLE_ASCII: Mapping[str, str] = MappingProxyType(
    {
        "wartend": "[ ]",
        "laeuft": "[>]",
        "fertig": "[ok]",
        "fehler": "[x]",
        "abgebrochen": "[-]",
        "pause": "[||]",
        "warnung": "[!]",
    }
)

ASCII_RUECKFALL = False
"""``True`` schaltet alle Symbole auf die ASCII-Marken um (wenn Zeichen am Messrechner fehlen)."""


def symbol(name: str) -> str:
    """Gibt das Symbol ``name`` gemäß :data:`ASCII_RUECKFALL` zurück.

    Raises
    ------
    KeyError
        Bei unbekanntem Namen.
    """
    tabelle = SYMBOLE_ASCII if ASCII_RUECKFALL else SYMBOLE_UNICODE
    return tabelle[name]


# --- Kontrast (WCAG 2.x) ---------------------------------------------------------------------


def _kanal_linear(wert_8bit: int) -> float:
    c = wert_8bit / 255.0
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def relative_leuchtdichte(hex_farbe: str) -> float:
    """Relative Leuchtdichte nach WCAG 2.x (sRGB), Wert in 0 … 1.

    Raises
    ------
    ValueError
        Wenn ``hex_farbe`` nicht die Form ``#RRGGBB`` hat.
    """
    if len(hex_farbe) != 7 or not hex_farbe.startswith("#"):
        raise ValueError(f"Farbe muss #RRGGBB sein, erhalten {hex_farbe!r}")
    try:
        r, g, b = (int(hex_farbe[i : i + 2], 16) for i in (1, 3, 5))
    except ValueError:
        raise ValueError(f"Farbe muss #RRGGBB sein, erhalten {hex_farbe!r}") from None
    return 0.2126 * _kanal_linear(r) + 0.7152 * _kanal_linear(g) + 0.0722 * _kanal_linear(b)


def kontrastverhaeltnis(vorder: str, hinter: str) -> float:
    """Kontrastverhältnis ``(L1 + 0,05) / (L2 + 0,05)`` nach WCAG 2.x, Wert in 1 … 21."""
    a = relative_leuchtdichte(vorder)
    b = relative_leuchtdichte(hinter)
    hell, dunkel = max(a, b), min(a, b)
    return (hell + 0.05) / (dunkel + 0.05)
