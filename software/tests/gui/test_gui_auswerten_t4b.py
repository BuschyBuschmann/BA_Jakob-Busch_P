"""Korrekturrunde T4 (K-AUSW-T4): Fußzeile bei 1100x680, Stempel, Vorschläge, Dialoge, Export-Reste.

Ausführen: ``QT_QPA_PLATFORM=offscreen uv run pytest -m gui tests/gui/test_gui_auswerten_t4b.py``.
"""

from __future__ import annotations

import dataclasses
from pathlib import Path
from typing import Any

import pytest
from gui_ausw_hilfen import PFAD, Bauer, SteuerbarerAusfuehrer
from PySide6.QtCore import Qt
from PySide6.QtTest import QTest
from PySide6.QtWidgets import QAbstractButton, QApplication
from pytestqt.qtbot import QtBot
from test_gui_auswerten_t4 import Meldungen, Reiter, _fange_bild, ansicht, lade

from ldv_automation.darstellung.auswahl import PaarCache, frf_daten, spektrum_daten
from ldv_automation.darstellung.frf import FrfOptionen
from ldv_automation.gui import anzeige_aktionen as ak
from ldv_automation.gui import anzeige_auswerten as aa
from ldv_automation.gui import auswerten_reiter, tokens
from ldv_automation.gui.auswerten_reiter import AuswertenReiter
from ldv_automation.gui.pruefdialog import PruefDialog

pytestmark = pytest.mark.gui


@pytest.fixture
def reiter(baue: Bauer, qtbot: QtBot, monkeypatch: pytest.MonkeyPatch) -> Reiter:
    """Fenster mit geladener Datei (Attrappen für Dialoge), wie in ``test_gui_auswerten_t4``."""
    w, protokoll = baue()
    a = lade(qtbot, w)
    return w, a, protokoll, Meldungen(a, monkeypatch)


LANG_NPZ = (
    "C:\\Users\\jakob.busch\\Documents\\Bachelorarbeit\\Messungen\\2026-10-12_Plattenversuch\\"
    "Auswertung\\ergebnis_ref_mitte.npz"
)
LANG_JSON = LANG_NPZ[:-3] + "json"


def klein(w: Any) -> None:
    """Mindestgröße der Oberfläche (FENSTER_MIN: 1100x680)."""
    w.resize(1100, 680)
    QApplication.processEvents()


def sichtbar_passt(a: AuswertenReiter) -> bool:
    """Gemessene Textbreite des sichtbaren Textes ≤ Breite des Labels."""
    QApplication.processEvents()  # das Layout übernimmt zuerst die neuen Breiten
    label = a.lbl_cursor
    return label.fontMetrics().horizontalAdvance(label.text()) <= label.width()


# --- F-1: Meldezeile ---------------------------------------------------------------------------


def test_export_meldung_mit_langen_pfaden_ist_gekuerzt_und_voll_im_tooltip(
    reiter: Reiter, qtbot: QtBot, monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    w, a, _p, m = reiter
    klein(w)
    monkeypatch.setattr(auswerten_reiter, "export_job", lambda *_args: (LANG_NPZ, LANG_JSON))
    m.export_ziel = str(tmp_path / "ex")
    a.btn_export.click()
    qtbot.waitUntil(lambda: a.btn_export.isEnabled(), timeout=3000)
    voll = ak.export_meldung(LANG_NPZ, LANG_JSON)
    assert LANG_NPZ in a.lbl_cursor.toolTip() and LANG_JSON in a.lbl_cursor.toolTip()
    assert a.lbl_cursor.toolTip() == voll and a.lbl_cursor.accessibleDescription() == voll
    text = a.lbl_cursor.text()
    assert text != voll and "…" in text and sichtbar_passt(a)
    assert text.startswith("Export geschrieben: C:\\") and " und C:\\" in text  # Anfang bleibt
    assert "ergebnis_ref_mitte.npz und" in text and text.endswith("ergebnis_ref_mitte.json")


def test_fehlertext_wird_rechts_gekuerzt_volltext_im_tooltip(
    reiter: Reiter, qtbot: QtBot, tmp_path: Path
) -> None:
    w, a, protokoll, m = reiter
    klein(w)
    protokoll.export_fehler = "Datei verändert " + "ohne erkennbaren Grund " * 20
    m.export_ziel = str(tmp_path / "ex")
    a.btn_export.click()
    qtbot.waitUntil(lambda: bool(m.warnungen), timeout=3000)
    text = a.lbl_cursor.text()
    assert text.endswith("…") and text != a.lbl_cursor.volltext() and sichtbar_passt(a)
    assert protokoll.export_fehler in a.lbl_cursor.toolTip()
    assert protokoll.export_fehler in a.lbl_cursor.accessibleDescription()


def test_bildmeldung_kuerzt_den_pfad_mittig(
    reiter: Reiter, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    w, a, _p, m = reiter
    klein(w)
    lang = str(tmp_path / ("sehr_langer_ordnername_" * 6) / "bild_ansicht1.png")
    Path(lang).parent.mkdir(parents=True)
    m.bild_ziel = lang
    a.btn_bild.click()
    assert a.lbl_cursor.toolTip() == ak.bild_meldung(lang) and sichtbar_passt(a)
    assert "…" in a.lbl_cursor.text() and a.lbl_cursor.text().endswith("bild_ansicht1.png")


# --- F-2/F-3: Cursorzeile und Prüftext bei 1100x680 ---------------------------------------------


def zeige_zeile(a: AuswertenReiter, text: str) -> None:
    a._cursor_aktiv = True
    a.lbl_cursor.setText(text)
    a._fuss_verteilen()


def test_cursorzeile_ansicht_1_passt_bei_1100x680(reiter: Reiter) -> None:
    w, a, _p, _m = reiter
    klein(w)
    for kasten in a.chk.values():
        kasten.setChecked(True)
    QApplication.processEvents()
    a.plot.setze_cursor(7.5)
    voll = a.lbl_cursor.volltext()
    assert "Vib X = " in voll and "3D = " in voll and voll.count("m/s") == 1
    wichtig = voll.split(" · Mittel")[0]  # f, alle Kurvenwerte und die Einheit
    assert wichtig in a.lbl_cursor.text() and wichtig.endswith("m/s")
    assert sichtbar_passt(a)


def test_cursorzeile_ansicht_2_passt_bei_1100x680(reiter: Reiter) -> None:
    w, a, _p, _m = reiter
    klein(w)
    ansicht(a, 2)
    a.liste_punkte.setCurrentRow(1)
    a.auswahl_frf.chk_phase.setChecked(True)
    QApplication.processEvents()
    a.plot.setze_cursor(7.5)
    voll = a.lbl_cursor.volltext()
    assert "|H1| = " in voll and "|H2| = " in voll and "φ = " in voll and "⚠ unbestätigt" in voll
    wichtig = voll.split(" · Punkt")[0]  # bis einschließlich Phase
    assert wichtig in a.lbl_cursor.text() and sichtbar_passt(a)


def test_ungünstigster_fall_mit_exponentialwerten_passt_in_beiden_ansichten(
    reiter: Reiter,
) -> None:
    """Alle Werte in Exponentialschreibweise (je 10 Zeichen) und der längste Kanalname."""
    w, a, _p, _m = reiter
    klein(w)
    geladen = a._geladen
    assert geladen is not None
    cache = PaarCache(geladen.messdaten)
    k = 31
    # Ansicht 1: vier Kurven, Mittel
    sp = spektrum_daten(geladen.messdaten, cache, punkt=None, komponenten=("X", "Y", "Z", "3D"))
    sp = dataclasses.replace(
        sp, kurven=tuple(dataclasses.replace(c, y=c.y * 1.8372e-5 / c.y[k]) for c in sp.kurven)
    )
    zeile1 = ak.cursor_zeile(1, sp, None, k)
    assert zeile1 is not None and zeile1.count("1,84·10⁻⁵") == 4
    zeige_zeile(a, zeile1)
    wichtig1 = zeile1.split(" · Mittel")[0]
    assert wichtig1 in a.lbl_cursor.text() and sichtbar_passt(a)
    # Ansicht 2: H1, H2 und Phase mit Kennzeichen
    fd = frf_daten(cache, "Vib Z", "Ref1", punkt=0)
    fd = dataclasses.replace(
        fd,
        betrag_h1=fd.betrag_h1 * 1.8372e-5 / fd.betrag_h1[k],
        betrag_h2=fd.betrag_h2 * 1.8372e-5 / fd.betrag_h2[k],
        einheit="(m/s²)/N",
    )
    opt = FrfOptionen(phase=True, kennzeichen_phase="unbestätigt (M8)")
    zeile2 = ak.cursor_zeile(2, fd, opt, k)
    assert zeile2 is not None and "⚠ unbestätigt" in zeile2
    zeige_zeile(a, zeile2)
    wichtig2 = zeile2.split(" · Punkt")[0]
    assert wichtig2 in a.lbl_cursor.text() and sichtbar_passt(a)


def test_pruefzusammenfassung_wird_an_teilgrenzen_gekuerzt_volltext_im_tooltip(
    reiter: Reiter,
) -> None:
    w, a, _p, m = reiter
    klein(w)
    voll = "Prüfung: 1 Warnung, 1 Hinweis, 7 nicht prüfbar, 36 ok"
    a.lbl_pruefung.setText(voll)
    zeige_zeile(a, "f = 7,500 Hz · " + "x" * 100)  # die Meldezeile braucht fast die ganze Breite
    text = a.lbl_pruefung.text()
    assert text.startswith("Prüfung: 1 Warnung, 1 Hinweis, ") and text.endswith(", …")
    assert text != voll
    assert a.lbl_pruefung.volltext() == voll and voll in a.lbl_pruefung.toolTip()
    assert a.lbl_pruefung.fontMetrics().horizontalAdvance(text) <= a.lbl_pruefung.width()
    QTest.mouseClick(a.lbl_pruefung, Qt.MouseButton.LeftButton)
    assert m.dialoge[0].lbl_zusammenfassung.text() == voll  # der Dialog zeigt den Volltext
    # genug Platz: nichts gekürzt, kein Tooltip
    zeige_zeile(a, "f = 7,500 Hz")
    assert a.lbl_pruefung.text() == voll and a.lbl_pruefung.toolTip() == ""


VOLL_FEHLER = "Prüfung: 1 Fehler, 2 Warnungen, 3 Hinweise, 7 nicht prüfbar, 36 ok"
VOLL_WARNUNG = "Prüfung: 1 Warnung, 38 ok"


@pytest.mark.parametrize("voll", [VOLL_WARNUNG, VOLL_FEHLER])
def test_auffaelligkeiten_bleiben_bei_1100_mit_langer_cursorzeile_sichtbar(
    reiter: Reiter, voll: str
) -> None:
    """UI-23: Die Warn-/Fehlerzahl wird nie gekürzt, die Meldezeile gibt Platz ab."""
    w, a, _p, _m = reiter
    klein(w)
    a.lbl_pruefung.setText(voll)
    zeige_zeile(a, "f = 7,500 Hz · " + "Vib X = 1,84·10⁻⁵ m/s · " * 4 + "x" * 200)
    text = a.lbl_pruefung.text()
    kern = aa.pruefung_kern(voll)
    assert text.startswith(kern.removesuffix(", …")), text
    assert a.lbl_pruefung.fontMetrics().horizontalAdvance(text) <= a.lbl_pruefung.width()
    assert voll in a.lbl_pruefung.toolTip() or text == voll


def test_auffaelligkeiten_bleiben_nach_export_mit_langen_pfaden_sichtbar(
    reiter: Reiter, qtbot: QtBot, monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    w, a, _p, m = reiter
    klein(w)
    a.lbl_pruefung.setText(VOLL_FEHLER)
    monkeypatch.setattr(auswerten_reiter, "export_job", lambda *_args: (LANG_NPZ, LANG_JSON))
    m.export_ziel = str(tmp_path / "ex")
    a.btn_export.click()
    qtbot.waitUntil(lambda: a.btn_export.isEnabled(), timeout=3000)
    QApplication.processEvents()
    assert "…" in a.lbl_cursor.text()
    assert a.lbl_pruefung.text().startswith("Prüfung: 1 Fehler, 2 Warnungen, 3 Hinweise")
    assert a.lbl_cursor.geometry().right() < a.lbl_pruefung.geometry().left()


def test_cursorzeile_vier_kurven_laesst_die_warnzahl_stehen(reiter: Reiter) -> None:
    w, a, _p, _m = reiter
    klein(w)
    for kasten in a.chk.values():
        kasten.setChecked(True)
    QApplication.processEvents()
    a.plot.setze_cursor(7.5)
    assert "1 Warnung" in a.lbl_pruefung.text() and sichtbar_passt(a)


@pytest.mark.parametrize("groesse", [(1366, 768), (1920, 1080)])
def test_pruefung_bleibt_bei_breiten_fenstern_vollstaendig(
    reiter: Reiter, groesse: tuple[int, int]
) -> None:
    w, a, _p, _m = reiter
    w.resize(*groesse)
    QApplication.processEvents()
    for kasten in a.chk.values():
        kasten.setChecked(True)
    a.lbl_pruefung.setText(VOLL_FEHLER)
    QApplication.processEvents()
    a.plot.setze_cursor(7.5)  # Cursorzeile mit vier Kurven
    assert "Vib X = " in a.lbl_cursor.volltext() and "3D = " in a.lbl_cursor.volltext()
    assert a.lbl_pruefung.text() == VOLL_FEHLER and a.lbl_pruefung.toolTip() == ""


def test_fussteile_ueberlappen_nicht_und_fuellen_die_zeile(reiter: Reiter) -> None:
    w, a, _p, _m = reiter
    for breite, hoehe in ((1100, 680), (1366, 768)):
        w.resize(breite, hoehe)
        QApplication.processEvents()
        zeige_zeile(a, "f = 7,500 Hz · " + "x" * 300)
        c = a.lbl_cursor.geometry()
        p = a.lbl_pruefung.geometry()
        assert c.right() < p.left() and p.right() <= a._fuss.width()
        assert a.lbl_pruefung.width() >= 150


# --- F-4: Stempel nur bei gezeichneter Phase ---------------------------------------------------


def test_bild_ansicht_2_mittel_mit_phase_hat_keinen_zusatz(
    reiter: Reiter, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    _w, a, _p, m = reiter
    bilder = _fange_bild(a, monkeypatch)
    ansicht(a, 2)
    assert a._auswahl.punkt is None  # Mittel
    a.auswahl_frf.chk_phase.setChecked(True)
    QApplication.processEvents()
    m.bild_ziel = str(tmp_path / "mittel.png")
    a.btn_bild.click()
    assert (tmp_path / "mittel.png").exists()
    assert not any("unbestätigte Größen" in t for t in bilder[0].alle_texte())
    a.liste_punkte.setCurrentRow(1)  # Punkt: die Phase wird gezeichnet
    QApplication.processEvents()
    m.bild_ziel = str(tmp_path / "punkt.png")
    a.btn_bild.click()
    assert any("enthält unbestätigte Größen (M8)" in t for t in bilder[1].alle_texte())


# --- Review MINOR 1: Vorschlag aus der angezeigten Datei ---------------------------------------


def test_vorschlag_gehoert_zur_angezeigten_datei_nicht_zum_letzten_oeffnen_ordner(
    reiter: Reiter, qtbot: QtBot, monkeypatch: pytest.MonkeyPatch, protokoll_b: str = "D:\\b\\b.svd"
) -> None:
    _w, a, protokoll, _m = reiter
    vorschlaege: list[str] = []
    monkeypatch.setattr(a, "_waehle_export_ziel", lambda v: vorschlaege.append(v))
    monkeypatch.setattr(a, "_waehle_bild_ziel", lambda v: vorschlaege.append(v))
    protokoll.fehler_lese[protokoll_b] = "kaputt"
    a.oeffne_datei(protokoll_b)  # Laden B scheitert; A bleibt angezeigt
    qtbot.waitUntil(lambda: a.fehlertext is not None, timeout=5000)
    assert a._letzter_ordner == str(Path(protokoll_b).parent)  # nur für den Öffnen-Dialog
    a.btn_export.click()
    a.btn_bild.click()
    assert vorschlaege == ["C:\\messungen\\probe", "C:\\messungen\\probe_ansicht1.png"]


# --- Review MINOR 3: F5 bis F8 im Reiter „Auswerten“ -------------------------------------------


def test_f5_bis_f8_loesen_im_reiter_auswerten_keine_messen_aktion_aus(reiter: Reiter) -> None:
    w, _a, _p, _m = reiter
    ausgeloest: list[str] = []
    aktionen = {
        "F5": (Qt.Key.Key_F5, w.act_start),
        "F6": (Qt.Key.Key_F6, w.act_pause),
        "F7": (Qt.Key.Key_F7, w.act_bestaetigen),
        "F8": (Qt.Key.Key_F8, w.act_abbrechen),
    }
    for name, (_key, aktion) in aktionen.items():
        aktion.triggered.connect(lambda *_x, n=name: ausgeloest.append(n))
    w.activateWindow()
    for _name, (key, _aktion) in aktionen.items():
        QTest.keyClick(w, key)
    QApplication.processEvents()
    assert ausgeloest == []
    assert w.reiter.currentIndex() == 1
    # Positivkontrolle: im Reiter „Messen“ lösen die aktiven Aktionen aus
    w.reiter.setCurrentIndex(0)
    w.activateWindow()
    for _name, (key, aktion) in aktionen.items():
        aktion.setEnabled(True)  # ein Tastendruck kann den Zustand und die Aktionen ändern
        QTest.keyClick(w, key)
        QApplication.processEvents()
    assert sorted(ausgeloest) == ["F5", "F6", "F7", "F8"]


# --- F-5: Prüfdialog ---------------------------------------------------------------------------


def test_pruefdialog_waehlt_erste_warnung_und_behaelt_die_reihenfolge(reiter: Reiter) -> None:
    _w, a, _p, m = reiter
    QTest.mouseClick(a.lbl_pruefung, Qt.MouseButton.LeftButton)
    d: PruefDialog = m.dialoge[0]
    assert d.tabelle.currentRow() == 1  # P-02 ist die erste Warnung
    nummern = [getattr(d.tabelle.item(i, 0), "text", lambda: "")() for i in range(2)]
    assert nummern == ["P-01", "P-02"]
    assert d.tabelle.selectionModel().selectedRows()[0].row() == 1
    assert all(d.tabelle.rowHeight(i) >= 32 for i in range(d.tabelle.rowCount()))
    assert d.tabelle.verticalHeader().defaultSectionSize() == 32


def test_pruefdialog_scrollt_die_auffaellige_zeile_in_den_sichtbaren_bereich(
    qtbot: QtBot,
) -> None:
    zeilen = [(f"P-{i:02d}", "ok", "Prüfung", "Vib Z", "Grund") for i in range(1, 41)]
    d = PruefDialog("Prüfung: 39 ok, 1 Warnung", zeilen, start_zeile=35)
    qtbot.addWidget(d)
    d.resize(900, 300)
    d.show()
    qtbot.waitExposed(d)
    QApplication.processEvents()
    item = d.tabelle.item(35, 0)
    assert item is not None and d.tabelle.currentRow() == 35
    zelle = d.tabelle.visualItemRect(item)
    assert d.tabelle.viewport().rect().intersects(zelle) and d.tabelle.rowHeight(35) >= 32
    assert d.tabelle.verticalScrollBar().value() > 0
    ohne = PruefDialog("Prüfung: 40 ok", zeilen)  # ohne Auffälliges: keine Vorauswahl
    qtbot.addWidget(ohne)
    assert ohne.tabelle.currentRow() == -1


# --- F-6/F-8: Zuletzt-Liste und Hinweis auf Drag-and-drop ---------------------------------------


def test_zuletzt_liste_32px_zeilen_kontrast_und_ziehen_hinweis(
    baue: Bauer, qtbot: QtBot, tmp_path: Path
) -> None:
    w, _p = baue()
    a = w.auswerten
    assert a is not None
    vorhanden = tmp_path / "da.svd"
    vorhanden.write_bytes(b"")
    a._einstellungen.merke_datei(str(vorhanden))
    a._einstellungen.merke_datei(str(tmp_path / "weg.svd"))
    a._fuelle_zuletzt(sichtbar=True)
    liste = a.liste_zuletzt
    QApplication.processEvents()
    assert [liste.visualItemRect(liste.item(i)).height() for i in range(2)] == [32, 32]
    assert liste.height() == 2 * 32 + 2 * liste.frameWidth()
    fehlt = liste.item(0)  # zuletzt gemerkt = oberster Eintrag
    assert "(nicht gefunden)" in fehlt.text()
    assert fehlt.foreground().color().name().lower() == tokens.C_NICHT_GEFUNDEN.lower()
    assert ("nicht_gefunden/flaeche", tokens.C_NICHT_GEFUNDEN, tokens.C_FLAECHE) in (
        tokens.KONTRAST_PAARE
    )
    assert a.lbl_ziehen.text() == ak.TEXT_ZIEHEN == "oder .svd-Datei hierher ziehen"
    assert a.lbl_ziehen.isVisibleTo(a)
    lade(qtbot, w, PFAD)
    assert not a.lbl_ziehen.isVisibleTo(a)


# --- Export: Schließen und Reste ---------------------------------------------------------------


def starte_laufenden_export(
    baue: Bauer, qtbot: QtBot, monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> tuple[Any, AuswertenReiter, SteuerbarerAusfuehrer]:
    ausfuehrer = SteuerbarerAusfuehrer()
    w, _p = baue(ausfuehrer)
    a = w.auswerten
    assert a is not None
    a.oeffne_datei(PFAD)
    ausfuehrer.auftraege[0].freigegeben = True
    qtbot.waitUntil(lambda: a.zustand is aa.AuswertenZustand.GELADEN, timeout=5000)
    m = Meldungen(a, monkeypatch)
    m.export_ziel = str(tmp_path / "ex")
    a.btn_export.click()
    assert a.export_laeuft()
    return w, a, ausfuehrer


def test_schliessen_waehrend_export_nein_laesst_das_fenster_offen(
    baue: Bauer, qtbot: QtBot, monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    w, a, ausfuehrer = starte_laufenden_export(baue, qtbot, monkeypatch, tmp_path)
    fragen: list[str] = []

    def attrappe(box: Any) -> int:
        fragen.append(box.text())
        box.findChild(QAbstractButton, "btn_dialog_nein").click()
        return 0

    monkeypatch.setattr(w, "_fuehre_aus", attrappe)
    w.close()
    assert fragen == ["Export läuft – abbrechen und schließen?"]
    assert w.isVisible() and a.export_laeuft()
    assert not ausfuehrer.auftraege[-1].abgebrochen


def test_schliessen_waehrend_export_ja_bricht_ab_und_schliesst(
    baue: Bauer, qtbot: QtBot, monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    w, a, ausfuehrer = starte_laufenden_export(baue, qtbot, monkeypatch, tmp_path)

    def attrappe(box: Any) -> int:
        box.findChild(QAbstractButton, "btn_dialog_ja").click()
        return 0

    monkeypatch.setattr(w, "_fuehre_aus", attrappe)
    w.close()
    assert not w.isVisible() and not a.export_laeuft()
    assert ausfuehrer.auftraege[-1].abgebrochen


def test_schliessen_ohne_export_fragt_nicht(
    reiter: Reiter, monkeypatch: pytest.MonkeyPatch
) -> None:
    w, _a, _p, _m = reiter
    fragen: list[Any] = []

    def merke(box: Any) -> int:
        fragen.append(box)
        return 0

    monkeypatch.setattr(w, "_fuehre_aus", merke)
    w.close()
    assert fragen == [] and not w.isVisible()


def test_verwaiste_tmp_dateien_werden_gemeldet_und_vor_dem_export_entfernt(
    reiter: Reiter, qtbot: QtBot, tmp_path: Path
) -> None:
    _w, a, protokoll, m = reiter
    npz_tmp, js_tmp = tmp_path / ".ex.npz.tmp", tmp_path / ".ex.json.tmp"
    npz_tmp.write_bytes(b"halb")
    js_tmp.write_text("{", encoding="utf-8")
    m.export_ziel = str(tmp_path / "ex")
    a.btn_export.click()
    assert not npz_tmp.exists() and not js_tmp.exists()  # vor dem Start entfernt
    assert len(protokoll.export) == 1
    assert ".ex.npz.tmp" in a._export_notiz and ".ex.json.tmp" in a._export_notiz
    qtbot.waitUntil(lambda: a.btn_export.isEnabled(), timeout=3000)
    assert "abgebrochenen Exports entfernt" in a.lbl_cursor.volltext()
    assert (tmp_path / "ex.npz").exists() and (tmp_path / "ex.json").exists()
    a.btn_export.click()  # zweiter Export zum selben Namen: nichts Verwaistes, kein Hinweis
    assert a._export_notiz == "" and "entfernt" not in a.lbl_cursor.volltext()


def test_einzelne_npz_ohne_json_wird_gemeldet_nicht_geloescht_und_stoppt_den_export(
    reiter: Reiter, tmp_path: Path
) -> None:
    _w, a, protokoll, m = reiter
    halb = tmp_path / "ex.npz"
    halb.write_bytes(b"npz")
    m.export_ziel = str(tmp_path / "ex")
    a.btn_export.click()
    assert protokoll.export == [] and halb.exists()
    assert len(m.warnungen) == 1 and "keine .json-Datei" in m.warnungen[0][1]
    assert str(halb) in a.lbl_cursor.volltext() and not a.export_laeuft()


def test_verwaiste_datei_nicht_entfernbar_stoppt_den_export(
    reiter: Reiter, monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    _w, a, protokoll, m = reiter

    def verweigert(_basis: Path) -> tuple[Path, ...]:
        raise PermissionError("gesperrt")

    monkeypatch.setattr(auswerten_reiter, "entferne_verwaiste_tmp", verweigert)
    m.export_ziel = str(tmp_path / "ex")
    a.btn_export.click()
    assert protokoll.export == [] and "nicht entfernbar" in m.warnungen[0][1]
    assert "gesperrt" in a.lbl_cursor.volltext()


def test_langer_pruef_fehler_verdraengt_die_meldezeile_nicht(
    reiter: Reiter, qtbot: QtBot, monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    """UI-25 (RR-AUSW-T4-2): Der Kern hat eine Obergrenze, Fehlertexte stehen rechts gekürzt."""
    w, a, _p, m = reiter
    klein(w)
    a._pruefung = None
    a._pruef_fehler = "ValueError: " + "sehr lange Fehlermeldung des Rechenkerns " * 6
    a._zeige_pruefung()
    monkeypatch.setattr(auswerten_reiter, "export_job", lambda *_args: (LANG_NPZ, LANG_JSON))
    m.export_ziel = str(tmp_path / "ex")
    a.btn_export.click()
    qtbot.waitUntil(lambda: a.btn_export.isEnabled(), timeout=3000)
    QApplication.processEvents()
    voll = a.lbl_pruefung.volltext()
    assert voll.startswith("✖ Prüfung nicht möglich: ValueError")
    assert a.lbl_pruefung.text().endswith("…") and a.lbl_pruefung.text() != voll
    assert voll in a.lbl_pruefung.toolTip()
    fuss = a._fuss
    assert a.lbl_pruefung.geometry().right() <= fuss.width()
    assert a.lbl_cursor.width() >= auswerten_reiter._MELDE_MIN_PX
    assert a.lbl_cursor.geometry().right() < a.lbl_pruefung.geometry().left()
    assert a.lbl_cursor.text() and a.lbl_cursor.toolTip() == ak.export_meldung(LANG_NPZ, LANG_JSON)
    assert sichtbar_passt(a)
