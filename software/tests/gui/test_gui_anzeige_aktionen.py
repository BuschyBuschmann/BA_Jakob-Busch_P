"""Reine Logik der Aktionen, Cursorzeile, Prüfdialog, Listen (P-AUSW T4, UI-13/16/17/19/23)."""

from __future__ import annotations

import pytest
from gui_ausw_hilfen import synth_geladen, synth_pruefung

from ldv_automation.auswertung.annahmen import Annahmen
from ldv_automation.auswertung.plausibilitaet import Pruefergebnis
from ldv_automation.darstellung.auswahl import (
    PaarCache,
    frf_daten,
    spektrum_daten,
    spitzen_daten_frf,
)
from ldv_automation.darstellung.frf import FrfOptionen
from ldv_automation.darstellung.schwingform import SchwingformOptionen
from ldv_automation.gui import anzeige_aktionen as ak
from ldv_automation.gui import anzeige_auswerten as aa

Zustand = aa.AuswertenZustand


def test_tasten_nach_brief_und_tooltip() -> None:
    assert ak.AKTIONS_TASTEN["oeffnen"] == ("Ctrl+Shift+O", "Strg+Umschalt+O")
    assert ak.AKTIONS_TASTEN["export"][1] == "Strg+E"
    assert ak.AKTIONS_TASTEN["bild"] == ("Ctrl+Shift+S", "Strg+Umschalt+S")
    assert [ak.AKTIONS_TASTEN[f"ansicht_{n}"][0] for n in (1, 2, 3, 4)] == [
        "Ctrl+1",
        "Ctrl+2",
        "Ctrl+3",
        "Ctrl+4",
    ]
    assert ak.AKTIONS_TASTEN["reiter_messen"][0] == "Alt+1"
    assert ak.AKTIONS_TASTEN["reiter_auswerten"][0] == "Alt+2"
    assert ak.AKTIONS_TASTEN["zoom"] == ("Home", "Pos1")
    assert ak.tooltip_mit_taste("Export", "export") == "Export (Strg+E)"


def test_bedienbarkeit_export_laeuft_und_ansicht_ohne_darstellung() -> None:
    basis = aa.bedienbarkeit_auswerten(Zustand.GELADEN)
    t = ak.bedienbarkeit_aktionen(
        basis, export_laeuft=True, bild_grund=ak.TEXT_BILD_KEINE_DARSTELLUNG
    )
    assert not t["export"].aktiv and t["export"].grund == ak.TEXT_EXPORT_LAEUFT
    assert not t["bild"].aktiv and t["bild"].grund == ak.TEXT_BILD_KEINE_DARSTELLUNG
    frei = ak.bedienbarkeit_aktionen(basis, export_laeuft=False, bild_grund=None)
    assert frei["export"].aktiv and frei["bild"].aktiv
    # ein ohnehin gesperrter Knopf behält seinen Grund
    leer = ak.bedienbarkeit_aktionen(
        aa.bedienbarkeit_auswerten(Zustand.KEINE_DATEI), export_laeuft=True, bild_grund="x"
    )
    assert (
        leer["export"].grund == aa.TEXT_ZUERST_OEFFNEN
        and leer["bild"].grund == aa.TEXT_ZUERST_OEFFNEN
    )


def test_export_vorschlag_und_basis() -> None:
    assert ak.export_vorschlag("C:\\mess\\probe.svd") == "C:\\mess\\probe"
    assert ak.export_vorschlag("/data/probe.svd", "/tmp/x/") == "/tmp/x/probe"
    assert ak.export_vorschlag("probe.svd") == "probe"
    assert ak.export_basis("C:/x/probe.JSON") == "C:/x/probe"
    assert ak.export_basis("probe.npz") == "probe"
    assert ak.export_basis("a.b") == "a.b"  # Punkte im Basisnamen bleiben
    assert ak.export_meldung("a.npz", "a.json") == "Export geschrieben: a.npz und a.json"


def test_bild_vorschlag_endung_meldung_stempel() -> None:
    assert ak.bild_vorschlag("/d/probe.svd", 3) == "/d/probe_ansicht3.png"
    assert ak.bild_endung("x.PNG", "PDF (*.pdf)") == "x.PNG"
    assert ak.bild_endung("x.pdf", "PNG (*.png)") == "x.pdf"
    assert ak.bild_endung("x", "PDF (*.pdf)") == "x.pdf"
    assert ak.bild_endung("x.v2", "PNG (*.png)") == "x.v2.png"
    assert ak.bild_meldung("x.png") == "Bild geschrieben: x.png"
    assert ak.stempel_ansicht(3) == "Ansicht 3 Spitzen und Bänder"
    assert ak.git_hash_text(None, None) is None
    assert ak.git_hash_text("a" * 40, False) == "a" * 12
    assert "geändert" in (ak.git_hash_text("a" * 40, True) or "")


def test_bild_unbestaetigt_nur_wenn_phase_gezeichnet_ist() -> None:
    annahmen = Annahmen().eintraege()
    cache = _daten()[1]
    punkt = frf_daten(cache, "Vib Z", "Ref1", punkt=0)  # mit Phasendaten
    mittel = frf_daten(cache, "Vib Z", "Ref1", punkt=None)  # Mittel: phase_rad ist None
    assert punkt.phase_rad is not None and mittel.phase_rad is None
    phase = FrfOptionen(phase=True, kennzeichen_phase="unbestätigt (M8)")
    assert ak.bild_unbestaetigt(2, punkt, phase, annahmen) == ("M8",)
    assert ak.bild_unbestaetigt(2, mittel, phase, annahmen) == ()  # nur Platzhalter, keine Phase
    ohne = FrfOptionen(phase=False, kennzeichen_phase="unbestätigt (M8)")
    assert ak.bild_unbestaetigt(2, punkt, ohne, annahmen) == ()
    assert ak.bild_unbestaetigt(1, object(), FrfOptionen(), annahmen) == ()


@pytest.mark.parametrize(
    ("darstellung", "erwartet"),
    [("phase_ref", ("M8",)), ("betrag", ()), ("phase_relativ", ())],
)
def test_bild_unbestaetigt_ansicht_4_nur_bei_phase_gegen_ref1(
    darstellung: str, erwartet: tuple[str, ...]
) -> None:
    opt = SchwingformOptionen(darstellung=darstellung, kennzeichen_phase="unbestätigt (M8)")  # type: ignore[arg-type]
    assert ak.bild_unbestaetigt(4, object(), opt, Annahmen().eintraege()) == erwartet


def _daten() -> tuple[object, PaarCache]:
    geladen = synth_geladen()
    return geladen.messdaten, PaarCache(geladen.messdaten)


def test_cursorzeile_spektrum_einzeln_und_mehrfach() -> None:
    daten, cache = _daten()
    einzeln = spektrum_daten(daten, cache, punkt=0, komponenten=("Z",))  # type: ignore[arg-type]
    k = 31  # f = 16 Hz
    text = ak.cursor_zeile(1, einzeln, None, k)
    y = float(einzeln.kurven[0].y[k])
    assert text is not None and text.startswith("f = 16,000 Hz · Amplitude = ")
    assert text.endswith(f"{einzeln.einheit} · Punkt 10 · Vib Z")
    assert aa.cursor_text(16.0, y, einzeln.einheit, "Punkt 10", "Vib Z") == text
    mehr = spektrum_daten(daten, cache, punkt=None, komponenten=("X", "3D"))  # type: ignore[arg-type]
    zeile = ak.cursor_zeile(1, mehr, None, k)
    assert zeile is not None
    assert "Mittel (alle Punkte)" in zeile and "Vib X = " in zeile and "3D = " in zeile


def test_cursorzeile_frf_phase_aus_daten_nicht_aus_linie() -> None:
    cache = _daten()[1]
    frf = frf_daten(cache, "Vib Z", "Ref1", punkt=0)
    k = 31
    opt = FrfOptionen(h1=True, h2=False, phase=True, kennzeichen_phase="unbestätigt (M8)")
    text = ak.cursor_zeile(2, frf, opt, k)
    assert text is not None
    assert "|H1| = " in text and "|H2|" not in text and "γ² = " in text
    assert "⚠ unbestätigt" in text and "gegen" not in text  # Paar steht am Ende der Zeile
    assert frf.phase_rad is not None
    grad = frf.phase_rad[k] * 180.0 / 3.141592653589793
    assert f"φ = {abs(grad):.1f}".replace(".", ",") in text.replace("\u2212", "")
    assert text.endswith("Punkt 10 · Vib Z / Ref1")
    ohne = ak.cursor_zeile(2, frf, FrfOptionen(phase=False), k)
    assert ohne is not None and "φ" not in ohne
    mittel = frf_daten(cache, "Vib Z", "Ref1", punkt=None)
    assert mittel.phase_rad is None
    z = ak.cursor_zeile(2, mittel, FrfOptionen(phase=True), k)
    assert z is not None and "φ" not in z  # für das Mittel nicht definiert


def test_cursorzeile_spitzen_und_ansicht_4() -> None:
    cache = _daten()[1]
    sd = spitzen_daten_frf(cache, "Vib Z", "Ref1", baender=())
    text = ak.cursor_zeile(3, sd, None, 10, kanal="Vib Z / Ref1")
    assert text is not None
    assert text.startswith("f = 5,500 Hz · Betrag = ") and text.endswith(
        "Mittel (alle Punkte) · Vib Z / Ref1"
    )
    assert ak.cursor_zeile(4, sd, None, 0) is None


def test_pruefdialog_zeilen_sortiert_mit_wort_und_symbol() -> None:
    p = synth_pruefung().pruefungen
    zeilen = ak.pruefdialog_zeilen(tuple(reversed(p)))
    assert [z[0] for z in zeilen] == ["P-01", "P-02"]
    assert zeilen[0][1].endswith("ok") and "Warnung" in zeilen[1][1]
    assert zeilen[1][2:] == ("b", "", "g")
    alle = [
        Pruefergebnis(id=f"P-{i:02d}", titel="t", status=s, wert=None, grund="g", bezug="Vib Z")  # type: ignore[arg-type]
        for i, s in enumerate(("fehler", "hinweis", "nicht_pruefbar"), 1)
    ]
    worte = [z[1] for z in ak.pruefdialog_zeilen(alle)]
    assert worte[0].endswith("Fehler") and worte[1] == "Hinweis" and worte[2] == "nicht prüfbar"


def test_zuletzt_liste_und_eintrag() -> None:
    liste: tuple[str, ...] = ()
    for n in range(7):
        liste = ak.zuletzt_aktualisieren(liste, f"/d/{n}.svd")
    assert liste == tuple(f"/d/{n}.svd" for n in (6, 5, 4, 3, 2)) and len(liste) == ak.ZULETZT_MAX
    liste = ak.zuletzt_aktualisieren(liste, "/d/4.svd")  # vorhanden: nach vorn, keine Doppelten
    assert liste[0] == "/d/4.svd" and liste.count("/d/4.svd") == 1 and len(liste) == 5
    assert ak.zuletzt_eintrag("C:\\m\\a.svd", vorhanden=True) == "a.svd  ·  C:\\m"
    assert ak.zuletzt_eintrag("C:\\m\\a.svd", vorhanden=False).endswith("(nicht gefunden)")


def test_svd_aus_pfaden() -> None:
    assert ak.svd_aus_pfaden(["/a/b.txt", "/a/c.SVD", "/a/d.svd"]) == "/a/c.SVD"
    assert ak.svd_aus_pfaden(["/a/b.txt"]) is None
    assert ak.svd_aus_pfaden([]) is None


@pytest.mark.parametrize("nr", [1, 2, 3, 4])
def test_ansichtsnamen_fuer_stempel(nr: int) -> None:
    assert ak.stempel_ansicht(nr).startswith(f"Ansicht {nr} ")


def test_export_und_bildvorschlag_aus_der_angezeigten_datei() -> None:
    assert ak.export_vorschlag("C:\\m\\a.svd") == "C:\\m\\a"
    assert ak.bild_vorschlag("C:\\m\\a.svd", 2) == "C:\\m\\a_ansicht2.png"
    assert ak.export_meldung("a.npz", "a.json") == "Export geschrieben: a.npz und a.json"
    assert ak.export_meldung("a.npz", "a.json", "Rest weg").endswith(" · Rest weg")


def test_cursorzeile_zahlen_exponent_einheit_einmal_auswahl_zuletzt() -> None:
    daten, cache = _daten()
    mehr = spektrum_daten(daten, cache, punkt=None, komponenten=("X", "Y", "Z", "3D"))  # type: ignore[arg-type]
    zeile = ak.cursor_zeile(1, mehr, None, 31)
    assert zeile is not None
    assert zeile.count(mehr.einheit) == 1  # Einheit einmal, hinter der Kurvenliste
    assert zeile.endswith(f"{mehr.einheit} · Mittel (alle Punkte)")
    assert zeile.index("Vib X = ") < zeile.index("3D = ") < zeile.index(mehr.einheit)
    klein = aa.cursor_text(5.0, 1.84e-5, "m/s", "Punkt 1", "Vib Z")
    assert "Amplitude = 1,84·10⁻⁵ m/s" in klein
    assert "Amplitude = 0,00460 m/s" in aa.cursor_text(5.0, 4.6e-3, "m/s", "Punkt 1", "Vib Z")


def test_cursorzeile_frf_einheit_einmal() -> None:
    cache = _daten()[1]
    frf = frf_daten(cache, "Vib Z", "Ref1", punkt=0)
    zeile = ak.cursor_zeile(2, frf, FrfOptionen(h1=True, h2=True, phase=False), 31)
    assert zeile is not None and zeile.count(frf.einheit) == 1
    assert zeile.index("|H2| = ") < zeile.index(frf.einheit) < zeile.index("γ² = ")


def breite8(text: str) -> int:
    """Messfunktion der Kürztests: 8 Pixel je Zeichen."""
    return 8 * len(text)


def test_kuerze_rechts_mitte_und_grenzfaelle() -> None:
    assert ak.kuerze_rechts("abc", 100, breite8) == "abc"
    assert ak.kuerze_rechts("abcdefghij", 0, breite8) == "abcdefghij"  # 0 = unbegrenzt
    k = ak.kuerze_rechts("abcdefghijklmnop", 80, breite8)
    assert k.endswith("…") and breite8(k) <= 80 and k.startswith("abcdefg")
    assert ak.kuerze_rechts("abc", 4, breite8) == "…"  # nur das Auslassungszeichen passt nicht mehr
    m = ak.kuerze_mitte("C:\\Users\\x\\Messungen\\probe.svd", 120, breite8)
    assert "…" in m and m.startswith("C:\\") and m.endswith(".svd")
    assert breite8(m) <= 120
    assert ak.kuerze_mitte("kurz", 100, breite8) == "kurz"


def test_kuerze_teile_an_teilgrenzen() -> None:
    text = "Prüfung: 36 ok, 1 Warnung, 1 Hinweis, 7 nicht prüfbar"
    assert ak.kuerze_teile(text, 1000, breite8) == text
    kurz = ak.kuerze_teile(text, 8 * 28, breite8)
    assert kurz == "Prüfung: 36 ok, 1 Warnung, …" and breite8(kurz) <= 8 * 28
    assert ak.kuerze_teile(text, 8 * 17, breite8) == "Prüfung: 36 ok, …"
    sehr_schmal = ak.kuerze_teile(text, 8 * 6, breite8)  # nicht einmal der erste Teil passt
    assert sehr_schmal.endswith("…") and breite8(sehr_schmal) <= 8 * 6


def test_kuerze_meldung_pfade_mittig_beide_dateinamen_sichtbar() -> None:
    npz = "C:\\Users\\jakob\\Documents\\Bachelorarbeit\\Messungen\\2026-10-12\\auswertung.npz"
    js = npz[:-3] + "json"
    text = f"Export geschrieben: {npz} und {js}"
    platz = 8 * 90
    kurz = ak.kuerze_meldung(text, (npz, js), platz, breite8)
    assert breite8(kurz) <= platz and kurz.count("…") == 2
    assert kurz.startswith("Export geschrieben: C:\\") and " und C:\\" in kurz
    assert kurz.endswith("auswertung.json") and "auswertung.npz und" in kurz
    assert ak.kuerze_meldung(text, (npz, js), 0, breite8) == text
    assert ak.kuerze_meldung("kurz", (), 100, breite8) == "kurz"
    # ohne Pfade oder bei sehr wenig Platz: rechts gekürzt
    fehler = "Export fehlgeschlagen: " + "x" * 200
    r = ak.kuerze_meldung(fehler, (), 8 * 40, breite8)
    assert r.endswith("…") and breite8(r) <= 8 * 40
    eng = ak.kuerze_meldung(text, (npz, js), 8 * 30, breite8)
    assert eng.endswith("…") and breite8(eng) <= 8 * 30


def test_erste_auffaellige_zeile() -> None:
    p = synth_pruefung().pruefungen
    assert ak.erste_auffaellige_zeile(tuple(reversed(p))) == 1  # P-02 ist die Warnung
    assert ak.erste_auffaellige_zeile(p[:1]) is None
    assert ak.erste_auffaellige_zeile(()) is None
