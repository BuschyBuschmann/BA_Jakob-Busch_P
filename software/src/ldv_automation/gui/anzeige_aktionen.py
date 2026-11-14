"""Reine Logik der Aktionen, des Cursors und der Listen des Reiters „Auswerten“ (P-AUSW T4).

Qt-frei und ohne NumPy- oder matplotlib-Import zur Laufzeit (wie
:mod:`ldv_automation.gui.anzeige_auswerten`): Tastenzuordnung (Brief K-AUSW Abschnitt 8),
Vorschläge und Meldungen für ``Daten exportieren …`` und ``Bild speichern …`` (UI-16, UI-17),
Cursorzeile der Ansichten 1 bis 3 (UI-13), Zeilen des Prüfdialogs (UI-23) und die Liste
„Zuletzt geöffnet“. Die Widgets liegen in :mod:`.auswerten_reiter`, :mod:`.plotflaeche` und
:mod:`.pruefdialog`.
"""

from __future__ import annotations

import re
from collections.abc import Callable, Iterable, Mapping, Sequence
from pathlib import PureWindowsPath
from typing import TYPE_CHECKING

from ldv_automation.gui.anzeige import Knopf
from ldv_automation.gui.anzeige_auswerten import (
    ANSICHT_NAMEN,
    cursor_text,
    unbestaetigte_annahmen,
)
from ldv_automation.gui.tokens import symbol

if TYPE_CHECKING:
    from ldv_automation.auswertung.annahmen import AnnahmeEintrag
    from ldv_automation.auswertung.plausibilitaet import Pruefergebnis
    from ldv_automation.darstellung.auswahl import FrfDaten, SpektrumDaten, SpitzenDaten

__all__ = [
    "AKTIONS_TASTEN",
    "DATEIFILTER_BILD",
    "DATEIFILTER_EXPORT",
    "TEXT_BILD_KEINE_DARSTELLUNG",
    "TEXT_EXPORT_LAEUFT",
    "TEXT_KEINE_ZULETZT",
    "TEXT_PRUEFUNG_NOCH_NICHT",
    "TEXT_ZIEHEN",
    "ZULETZT_MAX",
    "bedienbarkeit_aktionen",
    "bild_endung",
    "bild_meldung",
    "bild_unbestaetigt",
    "bild_vorschlag",
    "cursor_zeile",
    "erste_auffaellige_zeile",
    "export_basis",
    "export_meldung",
    "export_vorschlag",
    "git_hash_text",
    "kuerze_meldung",
    "kuerze_mitte",
    "kuerze_rechts",
    "kuerze_teile",
    "pruefdialog_zeilen",
    "stempel_ansicht",
    "svd_aus_pfaden",
    "tooltip_mit_taste",
    "zuletzt_aktualisieren",
    "zuletzt_eintrag",
]

# --- Tasten (Brief K-AUSW Abschnitt 8) -------------------------------------------------------

AKTIONS_TASTEN: Mapping[str, tuple[str, str]] = {
    "oeffnen": ("Ctrl+Shift+O", "Strg+Umschalt+O"),
    "export": ("Ctrl+E", "Strg+E"),
    "bild": ("Ctrl+Shift+S", "Strg+Umschalt+S"),
    "ansicht_1": ("Ctrl+1", "Strg+1"),
    "ansicht_2": ("Ctrl+2", "Strg+2"),
    "ansicht_3": ("Ctrl+3", "Strg+3"),
    "ansicht_4": ("Ctrl+4", "Strg+4"),
    "ansicht_5": ("Ctrl+5", "Strg+5"),
    "reiter_messen": ("Alt+1", "Alt+1"),
    "reiter_auswerten": ("Alt+2", "Alt+2"),
    "zoom": ("Home", "Pos1"),
}
"""Name → ``(Qt-Tastenfolge, Anzeige im Tooltip)``; einzige Quelle für Taste und Tooltip."""


def tooltip_mit_taste(text: str, name: str) -> str:
    """Tooltip „Text (Taste)“ für die Aktion ``name`` aus :data:`AKTIONS_TASTEN`."""
    return f"{text} ({AKTIONS_TASTEN[name][1]})"


# --- Texte -----------------------------------------------------------------------------------

TEXT_EXPORT_LAEUFT = "Export läuft …"
"""Grund (Tooltip), solange ein Export im Hintergrundprozess rechnet."""
TEXT_BILD_KEINE_DARSTELLUNG = "Diese Ansicht hat keine Darstellung zum Speichern."
"""Grund für ``Bild speichern …``, wenn die Ansicht nur einen Platzhaltertext zeigt."""
TEXT_PRUEFUNG_NOCH_NICHT = "Die Prüfung ist noch nicht berechnet."
"""Hinweis im Prüfdialog, solange Stufe B läuft oder fehlschlug."""
TEXT_KEINE_ZULETZT = "Noch keine Datei zuletzt geöffnet."
"""Hinweis anstelle der Liste „Zuletzt geöffnet“, wenn sie leer ist."""
DATEIFILTER_EXPORT = "Auswertungsdaten (*.json *.npz)"
"""Filter des Export-Dialogs; Endung ``.json`` bzw. ``.npz`` wird zum Basisnamen gekürzt."""
DATEIFILTER_BILD = "PNG (*.png);;PDF (*.pdf)"
"""Filter des Bild-Dialogs (Brief K-AUSW Abschnitt 7)."""
TEXT_ZIEHEN = "oder .svd-Datei hierher ziehen"
"""Hinweis im Zustand „Keine Datei“ auf Drag-and-drop (Brief K-AUSW Abschnitt 3.0)."""
ZULETZT_MAX = 5
"""Höchstzahl der Einträge „Zuletzt geöffnet“ (Brief K-AUSW Abschnitt 3.0)."""


def bedienbarkeit_aktionen(
    tabelle: Mapping[str, Knopf], *, export_laeuft: bool, bild_grund: str | None
) -> dict[str, Knopf]:
    """Ergänzt die Zustandstabelle um laufenden Export und Ansicht ohne Darstellung.

    Parameters
    ----------
    tabelle : mapping
        Ergebnis von :func:`~ldv_automation.gui.anzeige_auswerten.bedienbarkeit_auswerten`.
    export_laeuft : bool
        Ein Export rechnet im Hintergrund: ``export`` ist gesperrt (:data:`TEXT_EXPORT_LAEUFT`).
    bild_grund : str or None
        Grund, warum die Ansicht kein Bild liefert (Platzhaltertext statt Plot); ``None`` = ok.
    """
    neu = dict(tabelle)
    if export_laeuft and neu["export"].aktiv:
        neu["export"] = Knopf(False, TEXT_EXPORT_LAEUFT)
    if bild_grund is not None and neu["bild"].aktiv:
        neu["bild"] = Knopf(False, bild_grund)
    return neu


# --- Export und Bild -------------------------------------------------------------------------


def _trenner(ordner: str) -> str:
    return "\\" if "\\" in ordner else "/"


def export_vorschlag(messdatei: str, ordner: str = "") -> str:
    """Vorschlag für den Export: Ordner (oder Ordner der Messdatei) und Basisname der Messdatei.

    Parameters
    ----------
    messdatei : str
        Pfad der ``.svd``-Datei.
    ordner : str, optional
        Zuletzt benutzter Ordner; leer = Ordner der Messdatei.
    """
    schnitt = max(messdatei.rfind("/"), messdatei.rfind("\\"))
    stamm = PureWindowsPath(messdatei[schnitt + 1 :]).stem
    if ordner:
        wurzel, trenner = ordner.rstrip("/\\"), _trenner(ordner)
    elif schnitt >= 0:
        wurzel, trenner = messdatei[:schnitt], messdatei[schnitt]
    else:
        return stamm
    return f"{wurzel}{trenner}{stamm}"


def export_basis(gewaehlt: str) -> str:
    """Basisname ohne Endung ``.json`` oder ``.npz`` (der Kern hängt beide Endungen selbst an).

    Andere Endungen bleiben Teil des Namens (Basisnamen dürfen Punkte enthalten).
    """
    for endung in (".json", ".npz"):
        if gewaehlt.lower().endswith(endung):
            return gewaehlt[: -len(endung)]
    return gewaehlt


def export_meldung(npz: str, json_pfad: str, notiz: str = "") -> str:
    """Meldung in der Fußzeile nach erfolgreichem Export (beide Pfade, UI-16).

    ``notiz`` (z. B. „2 verwaiste Dateien entfernt“) steht, wenn vorhanden, hinter den Pfaden.
    """
    text = f"Export geschrieben: {npz} und {json_pfad}"
    return f"{text} · {notiz}" if notiz else text


def bild_vorschlag(messdatei: str, ansicht: int, ordner: str = "") -> str:
    """Vorschlag für ``Bild speichern …``: ``<Basisname>_ansicht<n>.png`` im Ordner."""
    return f"{export_vorschlag(messdatei, ordner)}_ansicht{ansicht}.png"


def bild_endung(pfad: str, filter_text: str) -> str:
    """Ergänzt eine fehlende Endung ``.png`` bzw. ``.pdf`` nach dem gewählten Filter.

    Eine vorhandene Endung ``.png`` oder ``.pdf`` bleibt; jede andere (auch eine fremde) wird
    nicht stillschweigend geändert, sondern ergänzt – der Aufrufer schreibt dann ``name.xyz.png``.
    """
    if pfad.lower().endswith((".png", ".pdf")):
        return pfad
    return pfad + (".pdf" if "PDF" in filter_text else ".png")


def bild_meldung(pfad: str) -> str:
    """Meldung in der Fußzeile nach dem Speichern des Arbeitsbildes."""
    return f"Bild geschrieben: {pfad}"


def stempel_ansicht(nr: int) -> str:
    """Ansichtsname im Fußstempel, z. B. „Ansicht 3 Spitzen und Bänder“."""
    return f"Ansicht {nr} {ANSICHT_NAMEN[nr]}"


def git_hash_text(git_hash: str | None, dirty: bool | None) -> str | None:
    """Git-Hash für den Stempel: 12 Zeichen, mit Zusatz bei ungespeicherten Änderungen.

    Parameters
    ----------
    git_hash : str or None
        Vollständiger Hash der Software; ``None`` = unbekannt.
    dirty : bool or None
        ``True``, wenn der Arbeitsbaum Änderungen hatte.
    """
    if not git_hash:
        return None
    return git_hash[:12] + (" (Arbeitsbaum geändert)" if dirty else "")


def bild_unbestaetigt(
    ansicht: int, daten: object, optionen: object, annahmen: Iterable[AnnahmeEintrag]
) -> tuple[str, ...]:
    """Nummern der offenen Annahmen, deren Größen im **Bild** vorkommen (Stempel, UI-17).

    Der Zusatz erscheint nur, wenn tatsächlich eine Phase gegen die Referenz gezeichnet ist:
    Ansicht 2 mit angezeigter Phase **und** vorhandenen Phasendaten (``daten.phase_rad``; beim
    Mittel gibt es keine, es steht nur ein Platzhalter), Ansicht 4 nur in der Darstellung
    „Phase gegen Ref1“. Die Phase relativ zu einem Bezugspunkt ist von M8 unabhängig.

    Parameters
    ----------
    ansicht : int
        Ansicht 1 bis 4.
    daten : object
        Daten der Zeichenfunktion (``FrfDaten`` in Ansicht 2).
    optionen : object
        Optionen der Zeichenfunktion (``kennzeichen_phase``, ``phase``, ``darstellung``).
    annahmen : iterable of AnnahmeEintrag
        Annahmen der Sitzung.
    """
    if not getattr(optionen, "kennzeichen_phase", None):
        return ()
    if ansicht == 2 and not (
        getattr(optionen, "phase", False) and getattr(daten, "phase_rad", None) is not None
    ):
        return ()
    if ansicht == 4 and getattr(optionen, "darstellung", None) != "phase_ref":
        return ()
    return tuple(a.nr for a in unbestaetigte_annahmen("phase", annahmen))


# --- Cursorzeile -----------------------------------------------------------------------------


def _wert(wert: float) -> str:
    from ldv_automation.darstellung.formate import zahl_kurz_text

    return zahl_kurz_text(float(wert), 3)


def _kanal_name(schluessel: str) -> str:
    return schluessel if schluessel == "3D" else f"Vib {schluessel}"


def _cursor_spektrum(daten: SpektrumDaten, k: int) -> str:
    """Eine Kurve: wie im Brief; mehrere: Einheit einmal hinter der Kurvenliste, Auswahl zuletzt.

    Die Reihenfolge richtet sich nach der Wichtigkeit, weil die Zeile rechts gekürzt wird
    (1100 px): Frequenz, Werte mit Einheit, erst danach die Auswahl.
    """
    from ldv_automation.darstellung.formate import frequenz_text

    f = float(daten.frequenz_hz[k])
    if len(daten.kurven) == 1:
        kurve = daten.kurven[0]
        return cursor_text(
            f, float(kurve.y[k]), daten.einheit, daten.auswahl_text, _kanal_name(kurve.schluessel)
        )
    werte = " · ".join(f"{_kanal_name(c.schluessel)} = {_wert(c.y[k])}" for c in daten.kurven)
    return f"f = {frequenz_text(f)} · {werte} {daten.einheit} · {daten.auswahl_text}"


def _cursor_frf(daten: FrfDaten, k: int, optionen: object) -> str:
    """Betrag mit Einheit einmal hinter H1/H2, dann γ², Phase, zuletzt Auswahl und Kanalpaar."""
    from ldv_automation.darstellung.formate import frequenz_text, winkel_text

    betraege = []
    if getattr(optionen, "h1", True):
        betraege.append(f"|{daten.bezeichnung_h1}| = {_wert(daten.betrag_h1[k])}")
    if getattr(optionen, "h2", True):
        betraege.append(f"|H2| = {_wert(daten.betrag_h2[k])}")
    teile = [f"f = {frequenz_text(float(daten.frequenz_hz[k]))}"]
    if betraege:
        teile.append(" · ".join(betraege) + f" {daten.einheit}")
    teile.append(f"γ² = {_wert(daten.kohaerenz[k])}")
    if getattr(optionen, "phase", False) and daten.phase_rad is not None:
        phase = f"φ = {winkel_text(float(daten.phase_rad[k]))}"
        if getattr(optionen, "kennzeichen_phase", None):
            phase += f" {symbol('warnung')} unbestätigt"
        teile.append(phase)
    teile.append(daten.auswahl_text)
    teile.append(f"{daten.antwort} / {daten.referenz}")
    return " · ".join(teile)


def _cursor_spitzen(daten: SpitzenDaten, k: int, kanal: str) -> str:
    from ldv_automation.darstellung.formate import frequenz_text

    return (
        f"f = {frequenz_text(float(daten.frequenz_hz[k]))} · {daten.groesse} = "
        f"{_wert(daten.y[k])} {daten.einheit} · Mittel (alle Punkte) · {kanal}"
    )


def cursor_zeile(
    ansicht: int, daten: object, optionen: object, k: int, *, kanal: str = ""
) -> str | None:
    """Cursorzeile der Ansichten 1 bis 3 für die Linie ``k`` (UI-13), Werte aus den Daten.

    Die Werte stammen aus den Datenarrays der Zeichenfunktion (auch die Phase aus
    ``FrfDaten.phase_rad``), nie aus den Linien des Diagramms.

    Parameters
    ----------
    ansicht : int
        Ansicht 1 bis 3; für Ansicht 4 (Ortskoordinaten) gibt es keinen Cursor.
    daten : object
        ``SpektrumDaten``, ``FrfDaten`` bzw. ``SpitzenDaten``.
    optionen : object
        Optionen der Zeichenfunktion (bei Ansicht 2: welche Kurven angezeigt werden).
    k : int
        0-basierter Linienindex.
    kanal : str, optional
        Kurvenname in Ansicht 3 (z. B. „Vib Z / Ref1“).

    Returns
    -------
    str or None
        ``None`` für Ansicht 4.
    """
    if ansicht == 1:
        return _cursor_spektrum(daten, k)  # type: ignore[arg-type]
    if ansicht == 2:
        return _cursor_frf(daten, k, optionen)  # type: ignore[arg-type]
    if ansicht == 3:
        return _cursor_spitzen(daten, k, kanal)  # type: ignore[arg-type]
    return None


# --- Kürzen langer Texte (Fußzeile) ----------------------------------------------------------

ELLIPSE = "…"
"""Auslassungszeichen der gekürzten Texte."""


def _groesstes(passt: Callable[[int], bool], hoechstens: int) -> int:
    """Größtes ``n`` in ``0..hoechstens`` mit ``passt(n)`` (``passt`` ist monoton fallend)."""
    unten, oben = 0, hoechstens
    while unten < oben:
        mitte = (unten + oben + 1) // 2
        if passt(mitte):
            unten = mitte
        else:
            oben = mitte - 1
    return unten


def kuerze_rechts(text: str, platz: int, breite: Callable[[str], int]) -> str:
    """Kürzt ``text`` rechts mit „…“, bis die Breite ``platz`` nicht überschreitet.

    Parameters
    ----------
    text : str
        Ungekürzter Text.
    platz : int
        Verfügbare Breite (Pixel); ``<= 0`` bedeutet unbegrenzt.
    breite : callable
        Misst die Breite eines Textes in Pixeln (in der Oberfläche ``fontMetrics``).
    """
    if platz <= 0 or breite(text) <= platz:
        return text
    n = _groesstes(lambda k: breite(text[:k].rstrip() + ELLIPSE) <= platz, len(text))
    return text[:n].rstrip() + ELLIPSE


def kuerze_mitte(text: str, platz: int, breite: Callable[[str], int]) -> str:
    """Kürzt ``text`` in der Mitte mit „…“ (Pfade: Anfang und Dateiname bleiben sichtbar).

    Enthält der Text einen Pfadtrenner (Schrägstrich oder Rückwärtsschrägstrich), bleibt
    möglichst der ganze Dateiname (mit dem Trenner davor) erhalten; mindestens sechs Zeichen
    vom Anfang bleiben.
    """
    if platz <= 0 or breite(text) <= platz:
        return text
    name = len(text) - max(text.rfind("/"), text.rfind("\\")) - 1  # Länge des Dateinamens
    anfang_min = 6

    def kurz(n: int) -> str:
        rechts = n // 2
        if name < len(text) - 1:  # mit Pfadtrenner: Dateiname behalten, soweit es der Platz erlaubt
            rechts = max(rechts, min(name + 1, n - anfang_min))
        return text[: n - rechts] + ELLIPSE + (text[len(text) - rechts :] if rechts else "")

    n = _groesstes(lambda k: breite(kurz(k)) <= platz, len(text))
    return kurz(n)


def kuerze_teile(text: str, platz: int, breite: Callable[[str], int], trenner: str = ", ") -> str:
    """Kürzt eine Aufzählung an Teilgrenzen („Prüfung: 36 ok, 1 Warnung, …“).

    Es fallen ganze Teile von hinten weg, nie ein halbes Wort; passt nicht einmal der erste
    Teil mit „…“, wird rechts gekürzt (:func:`kuerze_rechts`).
    """
    if platz <= 0 or breite(text) <= platz:
        return text
    teile = text.split(trenner)
    for anzahl in range(len(teile) - 1, 0, -1):
        kandidat = trenner.join(teile[:anzahl]) + trenner + ELLIPSE
        if breite(kandidat) <= platz:
            return kandidat
    return kuerze_rechts(text, platz, breite)


def kuerze_meldung(
    text: str, pfade: Sequence[str], platz: int, breite: Callable[[str], int]
) -> str:
    """Kürzt eine Meldung: Pfade gleichmäßig in der Mitte, sonst der ganze Text rechts.

    Jeder Pfad in ``pfade`` bekommt dieselbe Höchstbreite (die größte, mit der die Meldung
    noch passt), damit beide Dateinamen eines Exports sichtbar bleiben. Reicht selbst eine
    kurze Pfadform nicht, steht der Text rechts gekürzt.

    Parameters
    ----------
    text : str
        Ganze Meldung.
    pfade : sequence of str
        Pfade, die im ``text`` vorkommen (andere Teile werden nicht gekürzt).
    platz : int
        Verfügbare Breite (Pixel); ``<= 0`` bedeutet unbegrenzt.
    breite : callable
        Misst die Breite eines Textes in Pixeln.
    """
    if platz <= 0 or breite(text) <= platz:
        return text
    vorkommen = sorted({p for p in pfade if p and p in text}, key=len, reverse=True)
    if vorkommen:
        stuecke = re.split("(" + "|".join(re.escape(p) for p in vorkommen) + ")", text)

        def mit(budget: int) -> str:
            return "".join(
                kuerze_mitte(st, budget, breite) if st in vorkommen else st for st in stuecke
            )

        groesster = max(breite(p) for p in vorkommen)
        budget = _groesstes(lambda b: breite(mit(b)) <= platz, groesster)
        if budget >= breite("m" * 12):  # mindestens ein erkennbarer Rest je Pfad
            return mit(budget)
    return kuerze_rechts(text, platz, breite)


# --- Prüfdialog ------------------------------------------------------------------------------

_ERGEBNIS: Mapping[str, tuple[str, str]] = {
    "ok": ("fertig", "ok"),
    "warnung": ("warnung", "Warnung"),
    "fehler": ("fehler", "Fehler"),
    "hinweis": ("", "Hinweis"),
    "nicht_pruefbar": ("", "nicht prüfbar"),
}
"""Status → ``(Symbolname, Wort)``; das Wort steht immer, das Symbol nur ergänzend."""


def pruefdialog_zeilen(
    pruefungen: Sequence[Pruefergebnis],
) -> tuple[tuple[str, str, str, str, str], ...]:
    """Zeilen des Prüfdialogs ``(Nr, Ergebnis, Prüfung, Bezug, Text)`` nach Prüfnummer.

    Parameters
    ----------
    pruefungen : sequence of Pruefergebnis
        Ergebnisse P-01 bis P-11 (``PruefErgebnis.pruefungen``).
    """
    zeilen = []
    for p in sorted(pruefungen, key=lambda e: e.id):
        name, wort = _ERGEBNIS.get(p.status, ("", p.status))
        ergebnis = f"{symbol(name)} {wort}" if name else wort
        zeilen.append((p.id, ergebnis, p.titel, p.bezug, p.grund))
    return tuple(zeilen)


def erste_auffaellige_zeile(pruefungen: Sequence[Pruefergebnis]) -> int | None:
    """Index der ersten Warnung bzw. des ersten Fehlers in :func:`pruefdialog_zeilen`.

    ``None``, wenn keine Prüfung auffällt. Der Prüfdialog wählt diese Zeile beim Öffnen.
    """
    for i, p in enumerate(sorted(pruefungen, key=lambda e: e.id)):
        if p.status in ("warnung", "fehler"):
            return i
    return None


# --- Zuletzt geöffnet und Drag-and-drop ------------------------------------------------------


def zuletzt_aktualisieren(
    liste: Sequence[str], pfad: str, maximal: int = ZULETZT_MAX
) -> tuple[str, ...]:
    """Setzt ``pfad`` an den Anfang der Liste (ohne Doppelte, höchstens ``maximal``)."""
    rest = [p for p in liste if p != pfad]
    return tuple([pfad, *rest][:maximal])


def zuletzt_eintrag(pfad: str, *, vorhanden: bool) -> str:
    """Anzeigetext eines Listeneintrags: Dateiname, Ordner; fehlende Datei mit Hinweis."""
    schnitt = max(pfad.rfind("/"), pfad.rfind("\\"))
    ordner = pfad[:schnitt] if schnitt >= 0 else ""
    text = f"{pfad[schnitt + 1 :]}  ·  {ordner}" if ordner else pfad
    return text if vorhanden else f"{text}  (nicht gefunden)"


def svd_aus_pfaden(pfade: Iterable[str]) -> str | None:
    """Erste ``.svd``-Datei aus abgelegten Pfaden (Drag-and-drop), sonst ``None``."""
    return next((p for p in pfade if p.lower().endswith(".svd")), None)
