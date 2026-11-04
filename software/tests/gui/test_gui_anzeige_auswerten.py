"""Reine Anzeigelogik des Reiters „Auswerten“ (P-AUSW T3a, UI-2, 3, 15, 20, 22, 24; ohne Qt)."""

from __future__ import annotations

import ast
from collections.abc import Sequence
from pathlib import Path
from typing import Any

import pytest

from ldv_automation.auswertung.annahmen import Annahmen
from ldv_automation.auswertung.laden import Dateieinstellungen
from ldv_automation.auswertung.plausibilitaet import Pruefergebnis
from ldv_automation.auswertung.svd_lesen import SICHERHEIT, Mittelung
from ldv_automation.gui import anzeige_auswerten as aa
from ldv_automation.gui import plotstil, tokens
from ldv_automation.sitzung import DurchgangZustand as Z

Zustand = aa.AuswertenZustand


def einstellungen(**felder: object) -> Dateieinstellungen:
    """Einstellungen der Beispieldatei (1000 Hz, 1600 Linien, Δf 0,625 Hz, Mittelung 7 komplex)."""
    werte: dict[str, object] = {
        "bandbreite_hz": 1000.0,
        "linien": 1600,
        "delta_f_hz": 0.625,
        "abtastfrequenz_hz": 2500.0,
        "mittelung": Mittelung(typ=2, anzahl=7),
        "punkte": 135,
        "referenzen": (("Ref1", "N"), ("Ref2", "m/s²")),
    }
    werte.update(felder)
    return Dateieinstellungen(**werte)  # type: ignore[arg-type]


def zelle(zellen: tuple[aa.ParameterZelle, ...], schluessel: str) -> aa.ParameterZelle:
    return next(z for z in zellen if z.schluessel == schluessel)


# --- Parameterzeile (UI-2) -------------------------------------------------------------------


def test_ui_2_zellen_der_beispieldatei() -> None:
    z = aa.parameter_zellen(einstellungen())
    assert [c.schluessel for c in z] == [
        "bandbreite",
        "linien",
        "delta_f",
        "mittelung",
        "fenster",
        "punkte",
        "referenz",
    ]
    assert zelle(z, "bandbreite").wert == "1000 Hz"
    assert zelle(z, "linien").wert == "1600"
    assert zelle(z, "delta_f").wert == "0,625 Hz"
    assert zelle(z, "mittelung").wert == "7 (komplex)"
    assert zelle(z, "punkte").wert == "135"
    assert zelle(z, "referenz").wert == "Ref1 [N], Ref2 [m/s²]"


def test_ui_2_mittelung_ist_plausibel_und_fenster_nicht_lesbar() -> None:
    z = aa.parameter_zellen(einstellungen())
    assert aa.MITTELUNG_SICHERHEIT == SICHERHEIT["fft.mittelung"] == "plausibel"
    assert "plausibel" in zelle(z, "mittelung").tooltip
    fenster = zelle(z, "fenster")
    assert fenster.wert == aa.NICHT_LESBAR == "–"
    assert fenster.tooltip == "in der Datei nicht lesbar"


def test_ui_2_mittelung_nicht_lesbar_zeigt_strich_mit_tooltip() -> None:
    m = zelle(aa.parameter_zellen(einstellungen(mittelung=None)), "mittelung")
    assert (m.wert, m.tooltip) == ("–", "in der Datei nicht lesbar")


def test_ui_2_mittelung_aus_und_referenz_keine() -> None:
    z = aa.parameter_zellen(einstellungen(mittelung=Mittelung(typ=0, anzahl=1), referenzen=()))
    assert zelle(z, "mittelung").wert == "aus"
    assert zelle(z, "referenz").wert == "keine"  # bekannter Wert, kein „–“


def test_ui_3_ohne_datei_alle_werte_strich_mit_grund() -> None:
    z = aa.parameter_zellen(None)
    assert len(z) == 7
    assert all(c.wert == "–" and c.tooltip == aa.TEXT_ZUERST_OEFFNEN for c in z)


def test_parameter_tooltip_nennt_alle_werte() -> None:
    text = aa.parameter_tooltip(aa.parameter_zellen(einstellungen()))
    assert "Bandbreite: 1000 Hz" in text and "Referenz: Ref1 [N], Ref2 [m/s²]" in text


@pytest.mark.parametrize(
    ("breiten", "verfuegbar", "erwartet"),
    [
        ([100, 100, 100], 1000, 3),
        ([100, 100, 100], 316, 3),  # 100 + 8 + 100 + 8 + 100
        ([100, 100, 100], 315, 2),
        ([100, 100, 100], 99, 0),
        ([], 500, 0),
    ],
)
def test_zellen_rechts_ausblenden(breiten: list[int], verfuegbar: int, erwartet: int) -> None:
    assert aa.zellen_sichtbar(breiten, verfuegbar) == erwartet


# --- Zustände und Aktivierung (UI-3, UI-15, UI-24) ---------------------------------------------


def test_ui_3_keine_datei_sperrt_alles_ausser_oeffnen() -> None:
    t = aa.bedienbarkeit_auswerten(Zustand.KEINE_DATEI)
    assert t["oeffnen"].aktiv
    for name in ("export", "bild", "auswahl", "ansicht_1", "ansicht_2", "ansicht_3", "ansicht_4"):
        assert not t[name].aktiv and t[name].grund == "Zuerst eine Messdatei öffnen."


def test_ui_15_laden_sperrt_oeffnen_ansichten_und_auswahl() -> None:
    t = aa.bedienbarkeit_auswerten(Zustand.LADEN)
    assert not any(k.aktiv for k in t.values())
    assert all(k.grund == aa.TEXT_LAEDT for k in t.values())
    assert aa.lade_text("a.svd") == "Lese a.svd …"


def test_geladen_alle_ansichten_frei_export_und_bild_folgen() -> None:
    t = aa.bedienbarkeit_auswerten(Zustand.GELADEN)
    assert t["oeffnen"].aktiv and t["auswahl"].aktiv
    for nr in (1, 2, 3, 4):
        assert t[f"ansicht_{nr}"].aktiv
    for name in ("export", "bild"):
        assert not t[name].aktiv and t[name].grund == aa.TEXT_FOLGT
    assert {1, 2, 3, 4} == aa.FREIGESCHALTETE_ANSICHTEN


def test_ui_24_texte_der_zustaende() -> None:
    assert aa.TEXT_KEINE_DATEI == "Noch keine Messdatei geöffnet."
    assert aa.TEXT_PRUEFUNG_BERECHNET == "Prüfung: wird berechnet …"
    assert (
        aa.fehler_band_text("C:/x.svd: kaputt")
        == "✖ Datei kann nicht gelesen werden: C:/x.svd: kaputt"
    )
    assert aa.geladen_text("C:/x.svd") == "Geladen: C:/x.svd"
    assert aa.pruefung_fehler_text("boom") == "✖ Prüfung nicht möglich: boom"
    assert aa.zeichen_fehler_text("x") == "✖ Darstellung nicht möglich: x"
    assert aa.TEXT_PRUEFUNG_ABGEBROCHEN.startswith("Prüfung:")


@pytest.mark.parametrize(
    ("pfad", "name"),
    [("C:\\daten\\a.svd", "a.svd"), ("/home/x/b.svd", "b.svd"), ("c.svd", "c.svd"), ("", "")],
)
def test_dateiname_von(pfad: str, name: str) -> None:
    assert aa.dateiname_von(pfad) == name


# --- Prüfzusammenfassung und P-08 (UI-23) --------------------------------------------------------


def pruef(status: str, nr: int = 1) -> Pruefergebnis:
    return Pruefergebnis(id=f"P-{nr:02d}", titel="t", status=status, wert=None, grund="g")  # type: ignore[arg-type]


def test_pruefung_text_zaehlt_als_woerter() -> None:
    liste = (
        [pruef("ok")] * 36 + [pruef("warnung"), pruef("hinweis")] + [pruef("nicht_pruefbar")] * 7
    )
    assert aa.pruefung_text(liste) == "Prüfung: 36 ok, 1 Warnung, 1 Hinweis, 7 nicht prüfbar"


def test_pruefung_text_mehrzahl_und_leer() -> None:
    assert aa.pruefung_text([pruef("warnung")] * 2 + [pruef("fehler")]) == (
        "Prüfung: 2 Warnungen, 1 Fehler"
    )
    assert aa.pruefung_text([pruef("hinweis")] * 3) == "Prüfung: 3 Hinweise"
    assert aa.pruefung_text([]) == aa.TEXT_PRUEFUNG_LEER == "Prüfung: –"


def test_p08_voreinstellung_ref2_gegen_ref1_akzeleranz() -> None:
    assert aa.P08_ANTRIEBSPUNKT == ("Ref2", "Ref1", "akzeleranz")
    paare = [("Vib X", "Ref1"), ("Ref2", "Ref1")]
    assert aa.waehle_antriebspunkt(paare) == ("Ref2", "Ref1", "akzeleranz")


def test_p08_fehlen_die_kanaele_gilt_nicht_pruefbar() -> None:
    assert aa.waehle_antriebspunkt([("Vib X", "Ref1")]) is None
    assert aa.waehle_antriebspunkt([]) is None


# --- Kennzeichnung (UI-11) ---------------------------------------------------------------------


def test_abhaengig_von_ist_die_einzige_zuordnung() -> None:
    assert dict(aa.ABHAENGIG_VON) == {"phase": (("M8", "Polarität der Referenzkanäle offen"),)}
    quelle = Path(aa.__file__).parent
    treffer = [
        p.name
        for p in quelle.glob("*.py")
        if any(
            isinstance(n, ast.Name) and n.id == "ABHAENGIG_VON" and isinstance(n.ctx, ast.Store)
            for n in ast.walk(ast.parse(p.read_text(encoding="utf-8")))
        )
    ]
    assert treffer == ["anzeige_auswerten.py"]


def test_ui_11_m8_kennzeichen_verschwindet_ohne_codeaenderung() -> None:
    eintraege = Annahmen().eintraege()
    m8 = next(e for e in eintraege if e.nr == "M8")
    assert m8.ist_annahme
    offen = aa.unbestaetigte_annahmen("phase", eintraege)
    assert [e.nr for e in offen] == ["M8"] and offen[0].beschreibung
    bestaetigt = [
        type(e)(
            nr=e.nr,
            parameter=e.parameter,
            wert=e.wert,
            status="bestätigt",
            beschreibung=e.beschreibung,
        )
        if e.nr == "M8"
        else e
        for e in eintraege
    ]
    assert not next(e for e in bestaetigt if e.nr == "M8").ist_annahme
    assert aa.unbestaetigte_annahmen("phase", bestaetigt) == ()
    assert aa.unbestaetigte_annahmen("betrag", eintraege) == ()  # Größe ohne Zuordnung


# --- Cursor, Plotkopf, Textalternative, Punktliste ---------------------------------------------


def test_cursor_text_nach_brief() -> None:
    assert aa.cursor_text(123.75, 1.234e-3, "m/s", "Punkt 12", "Vib Z") == (
        "f = 123,750 Hz · Amplitude = 0,00123 m/s · Punkt 12 · Vib Z"  # feste Nachkommastellen
    )


def test_plotkopf_und_beschreibung() -> None:
    assert aa.plotkopf_text("a.svd", "Mittel (alle Punkte)", ["X", "3D"], "Geschwindigkeit") == (
        "a.svd · Mittel (alle Punkte) · X, 3D · Geschwindigkeit"
    )
    text = aa.plot_beschreibung(1, "a.svd", "Punkt 3", ["X"], 0.625, 1000.0)
    assert "Ansicht 1: Spektrum" in text and "0,625 bis 1000 Hz" in text and "a.svd" in text


def test_punkt_eintraege_mit_mittel_und_koordinaten() -> None:
    zeilen = aa.punkt_eintraege([5, 7], [(0.1, 0.25, -0.0125), (1.0, 2.0, 3.0)])
    assert zeilen[0] == "Mittel (alle Punkte)"
    assert zeilen[1] == "Punkt 5 (x 0,100; y 0,250; z -0,013 m)"
    assert len(zeilen) == 3


# --- Reiterkopf (UI-20) --------------------------------------------------------------------------


@pytest.mark.parametrize(
    ("fall", "durchgang", "erwartet"),
    [
        (None, Z.BEREIT, "Messen"),
        (None, Z.BEENDET, "Messen"),
        (None, Z.LAEUFT, "Messen ▶ läuft"),
        (None, Z.PAUSE_ANGEFORDERT, "Messen ▶ läuft"),
        (None, Z.ABBRUCH_LAEUFT, "Messen ▶ läuft"),
        ("1", Z.BEREIT, "Messen ✖ Gerät unklar"),
        (None, Z.GERAET_UNKLAR, "Messen ✖ Gerät unklar"),
        ("4", Z.WARTET_AUF_ENTSCHEIDUNG, "Messen ⚠ Entscheidung nötig"),
        ("4", Z.LAEUFT, "Messen ⚠ Entscheidung nötig"),
        ("5", Z.WARTET_AUF_BESTAETIGUNG, "Messen ⚠ Bestätigung nötig"),
        (None, Z.WARTET_AUF_BESTAETIGUNG, "Messen ⚠ Bestätigung nötig"),
        ("3", Z.BEREIT, "Messen"),  # Fall 3 bekommt kein Zusatzwort
        ("3", Z.LAEUFT, "Messen ▶ läuft"),
        ("1", Z.LAEUFT, "Messen ✖ Gerät unklar"),  # Vorrang vor „läuft“
    ],
)
def test_ui_20_reiterkopf_messen(fall: str | None, durchgang: Z, erwartet: str) -> None:
    assert aa.reiterkopf_messen(fall, durchgang) == erwartet


# --- Tokens, Plotstil (UI-4, UI-22) --------------------------------------------------------------


@pytest.mark.parametrize(("name", "vorder", "hinter"), tokens.KONTRAST_PAARE_LINIE)
def test_ui_22_linienkontrast_mindestens_3(name: str, vorder: str, hinter: str) -> None:
    assert tokens.kontrastverhaeltnis(vorder, hinter) >= tokens.KONTRAST_MINDEST_LINIE, name


def test_ui_22_neue_paare_stehen_in_kontrast_paare() -> None:
    namen = {n for n, _v, _h in tokens.KONTRAST_PAARE}
    assert {
        "plot_haupt/plot_flaeche",
        "plot_achse/plot_flaeche",
        "plot_achse/plot_band",
        "warn_rand/warn_bg",
    } <= namen
    linien = {n for n, _v, _h in tokens.KONTRAST_PAARE_LINIE}
    assert {"plot_serie_2/plot_band", "plot_serie_4/plot_band"} <= linien


def test_ui_4_linienarten_paarweise_verschieden_und_je_serie_ein_eintrag() -> None:
    stile = [stil for _name, stil in tokens.PLOT_LINIENARTEN]
    assert len(set(stile)) == len(stile) == 4
    assert len(tokens.PLOT_SERIENFARBEN) == 4


def test_plotstil_aus_tokens() -> None:
    s = plotstil.baue_plotstil()
    assert s.haupt == tokens.C_PLOT_HAUPT == tokens.C_AKZENT
    assert s.gitter == tokens.C_PLOT_GITTER and s.achse == tokens.C_PLOT_ACHSE
    assert s.flaeche == tokens.C_PLOT_FLAECHE and s.band == tokens.C_PLOT_BAND
    assert s.serienfarben == tokens.PLOT_SERIENFARBEN
    assert s.linienarten == tuple(stil for _n, stil in tokens.PLOT_LINIENARTEN)
    assert s.warn_symbol == tokens.symbol("warnung")
    assert s.dezimalkomma and s.schriftfamilie[-1] == plotstil.SCHRIFT_RUECKFALL
    assert s.schriftfamilie[:-1] == tuple(tokens.SCHRIFT_FAMILIEN)


def test_plotstil_ist_qt_und_pyplot_frei() -> None:
    import subprocess
    import sys

    code = (
        "import sys; import ldv_automation.gui.plotstil, ldv_automation.gui.anzeige_auswerten;"
        "assert not any(m.startswith('PySide6') for m in sys.modules);"
        "assert 'matplotlib.pyplot' not in sys.modules"
    )
    ergebnis = subprocess.run(
        [sys.executable, "-I", "-c", code], capture_output=True, text=True, check=False
    )
    assert ergebnis.returncode == 0, ergebnis.stderr


def test_anzeige_auswerten_importiert_matplotlib_nicht() -> None:
    """Der Messbetrieb braucht ``reiterkopf_messen``; matplotlib (0,6 s) darf nicht mitkommen."""
    import subprocess
    import sys

    code = (
        "import sys; import ldv_automation.gui.anzeige_auswerten;"
        "assert 'matplotlib' not in sys.modules and 'numpy' not in sys.modules and "
        "'olefile' not in sys.modules"
    )
    ergebnis = subprocess.run(
        [sys.executable, "-I", "-c", code], capture_output=True, text=True, check=False
    )
    assert ergebnis.returncode == 0, ergebnis.stderr


# --- T3b: Kennzeichen, Texte ----------------------------------------------------------------------


def _mit_status(eintraege: Sequence[Any], nr: str, status: str) -> list[Any]:
    return [
        type(e)(
            nr=e.nr, parameter=e.parameter, wert=e.wert, status=status, beschreibung=e.beschreibung
        )
        if e.nr == nr
        else e
        for e in eintraege
    ]


def test_ui_11_kennzeichen_text_aus_der_annahme_und_verschwindet_bei_bestaetigung() -> None:
    eintraege = Annahmen().eintraege()
    m8 = next(e for e in eintraege if e.nr == "M8")
    text = aa.kennzeichen_text("phase", eintraege)
    assert text == "unbestätigt (M8: Polarität der Referenzkanäle offen)"  # Kurztext, keine Formel
    assert m8.beschreibung not in text
    assert aa.kennzeichen_beschreibung("phase", eintraege) == f"M8 (unbestätigt): {m8.beschreibung}"
    assert aa.kennzeichen_text("betrag", eintraege) is None
    bestaetigt = _mit_status(eintraege, "M8", "bestätigt")
    assert not next(e for e in bestaetigt if e.nr == "M8").ist_annahme
    assert aa.kennzeichen_text("phase", bestaetigt) is None
    assert aa.kennzeichen_beschreibung("phase", bestaetigt) == ""


def test_phase_ref_text_mit_und_ohne_kennzeichen() -> None:
    eintraege = Annahmen().eintraege()
    assert aa.phase_ref_text("Ref1", eintraege) == "Phase gegen Ref1 (⚠ unbestätigt, M8)"
    assert aa.phase_ref_text("Ref2", _mit_status(eintraege, "M8", "bestätigt")) == (
        "Phase gegen Ref2"
    )


def test_t3b_zustandstexte_nach_brief() -> None:
    assert aa.TEXT_KEINE_FRF == (
        "Keine Übertragungsfunktion: Die Datei enthält keinen aktiven Referenzkanal. "
        "H1, H2 und Kohärenz brauchen eine Referenz."
    )
    assert aa.TEXT_KEINE_SPITZENSUCHE == "Keine Spitzensuche: Referenzkanal fehlt."
    assert aa.TEXT_KEINE_SPITZEN == "Keine Spitzen gefunden."
    assert aa.TEXT_KEINE_BAENDER == "Keine Bänder angegeben."
    assert aa.TEXT_PHASE_KEINE_REFERENZ == "Phase nicht verfügbar: keine Referenz."
    assert aa.TEXT_NAECHSTE_LINIE.format(f="123,750 Hz") == "nächste Linie: 123,750 Hz"


def test_phasentexte_stimmen_mit_der_zeichenfunktion_ueberein() -> None:
    from ldv_automation.darstellung import schwingform as sf

    assert aa.TEXT_PHASE_KEINE_REFERENZ == sf.PHASE_KEINE_REFERENZ
    assert aa.TEXT_PHASE_EINZELKOMPONENTE == sf.PHASE_NUR_EINZELKOMPONENTE


def test_folgefehler_text() -> None:
    assert aa.folgefehler_text([]) == ""
    assert aa.folgefehler_text(["Parameterzeile: x", "Plot: y"]) == (
        " [Folgefehler im Rückfall: Parameterzeile: x; Plot: y]"
    )


def test_ansicht_zugang_sperrt_nicht_freigeschaltete_ansichten(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(aa, "FREIGESCHALTETE_ANSICHTEN", frozenset({1}))
    assert aa.ansicht_zugang(1, Zustand.GELADEN).aktiv
    k = aa.ansicht_zugang(3, Zustand.GELADEN)
    assert not k.aktiv and k.grund == aa.TEXT_FOLGT
