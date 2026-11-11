"""Reiter „Auswerten“ (P-AUSW T3a): Reiterrahmen, Laden, Ansicht 1, Zustände; offscreen, ``gui``.

Ausführen: ``QT_QPA_PLATFORM=offscreen uv run pytest -m gui tests/gui/test_gui_auswerten.py``.
Die Datei kommt aus ``gui_ausw_hilfen.synth_geladen`` (4 Punkte, 64 Linien) über einen
``DirektAusfuehrer`` bzw. eine Ausführer-Attrappe; die Beispieldatei ``Input/...svd`` prüft
``test_beispieldatei_*`` (übersprungen, wenn sie fehlt).
"""

from __future__ import annotations

import dataclasses
from collections.abc import Callable
from pathlib import Path
from typing import Any

import matplotlib
import pytest
from gui_ausw_hilfen import (
    PFAD,
    SHA,
    Bauer,
    NieFertigAusfuehrer,
    SteuerbarerAusfuehrer,
    synth_geladen,
)
from gui_hilfen import AttrappenSitzung, Z, bild, eintrag
from PySide6.QtCore import QPoint, Qt
from PySide6.QtTest import QTest
from PySide6.QtWidgets import QAbstractButton, QApplication, QLabel, QWidget
from pytestqt.qtbot import QtBot

from ldv_automation.darstellung import Ansicht, Zeichnung
from ldv_automation.darstellung.achsen import AchsenOptionen, Bereich
from ldv_automation.gui import anzeige_auswerten as aa
from ldv_automation.gui import auswerten_reiter, plotflaeche, stil, tokens
from ldv_automation.gui.auswerten_reiter import AuswertenReiter
from ldv_automation.gui.hauptfenster import Hauptfenster
from ldv_automation.gui.plotflaeche import PlotFlaeche
from ldv_automation.gui.plotstil import baue_plotstil

pytestmark = pytest.mark.gui

BEISPIEL = Path(__file__).resolve().parents[3] / "Input" / "20261012_ref_Mitte.svd"


def lade(qtbot: QtBot, w: Hauptfenster, pfad: str = PFAD) -> AuswertenReiter:
    """Öffnet ``pfad`` und wartet, bis Ansicht 1 und die Prüfung (Stufe B) da sind."""
    a = w.auswerten
    assert a is not None
    a.oeffne_datei(pfad)
    qtbot.waitUntil(lambda: a.zustand is aa.AuswertenZustand.GELADEN, timeout=5000)
    qtbot.waitUntil(lambda: not a.laeuft(), timeout=5000)
    return a


def linien(a: AuswertenReiter) -> dict[str, Any]:
    zeichnung = a.plot.zeichnung
    assert zeichnung is not None
    return dict(zeichnung.linien)


def taste(_qtbot: QtBot, widget: QWidget, key: Qt.Key) -> None:
    QTest.keyClick(widget, key)


# --- Reiterrahmen ------------------------------------------------------------------------------


def test_reiterrahmen_und_lazy_aufbau(baue: Bauer) -> None:
    w, _ = baue(aktiv=False)
    assert w.findChild(QWidget, "reiter") is w.reiter
    assert [w.reiter.tabText(i) for i in range(2)] == ["Messen", "Auswerten"]
    assert w.reiter.currentIndex() == 0
    assert w.auswerten is None  # „Auswerten“ wird erst beim ersten Aktivieren aufgebaut
    assert w.findChild(QWidget, "messen") is not None and w.findChild(QWidget, "auswerten")
    w.reiter.setCurrentIndex(1)
    assert isinstance(w.auswerten, AuswertenReiter)
    erster = w.auswerten
    w.reiter.setCurrentIndex(0)
    w.reiter.setCurrentIndex(1)
    assert w.auswerten is erster  # nicht erneut aufgebaut
    assert w.statuszeile.isVisible()  # Zone A bleibt über beiden Reitern


def test_messen_reiter_unveraendert_enthaelt_zonen_b_bis_g(baue: Bauer) -> None:
    w, _ = baue(aktiv=False)
    messen = w.reiter.widget(0)
    assert messen is not None
    for ziel in (w.werkzeugleiste, w.hinweisband, w.tabelle, w.editor, w.protokoll):
        assert messen.isAncestorOf(ziel)
    assert not messen.isAncestorOf(w.statuszeile)


def test_aufbau_fehler_laesst_messbetrieb_unberuehrt(
    baue: Bauer, monkeypatch: pytest.MonkeyPatch
) -> None:
    class Kaputt:
        def __init__(self, *_a: object, **_k: object) -> None:
            raise RuntimeError("matplotlib nicht ladbar")

    monkeypatch.setattr(auswerten_reiter, "AuswertenReiter", Kaputt)
    w, _ = baue(sitzung=AttrappenSitzung(bild(eintraege=[eintrag()])), aktiv=False)
    start_vorher = w.act_start.isEnabled()
    assert start_vorher
    w.reiter.setCurrentIndex(1)
    text = w.findChild(QLabel, "auswerten_fehler")
    assert text is not None and "konnte nicht aufgebaut werden" in text.text()
    assert "matplotlib nicht ladbar" in text.text()
    assert w.auswerten is None
    w.reiter.setCurrentIndex(0)
    w.reiter.setCurrentIndex(1)
    assert len(w.findChildren(QLabel, "auswerten_fehler")) == 1  # kein zweiter Versuch
    w.reiter.setCurrentIndex(0)
    assert w.tabelle.isEnabled() and w.btn_betriebsart.isEnabled()
    assert w.act_start.isEnabled() == start_vorher  # die Messen-Aktionen laufen weiter


def test_aktionen_f5_bis_f8_und_strg_nso_im_reiter_auswerten_gesperrt(baue: Bauer) -> None:
    sitzung = AttrappenSitzung(bild(eintraege=[eintrag()]))
    w, _ = baue(sitzung=sitzung, aktiv=False)
    messen = {
        n: getattr(w, n).isEnabled()
        for n in (
            "act_messung_neu",
            "act_pausenpunkt_neu",
            "act_speichern",
            "act_laden",
            "act_start",
        )
    }
    assert messen["act_messung_neu"] and messen["act_start"]
    w.reiter.setCurrentIndex(1)
    for name in (*messen, "act_pause", "act_abbrechen", "act_bestaetigen"):
        assert not getattr(w, name).isEnabled(), name
    sitzung.befehle.clear()
    for key, mod in (
        (Qt.Key.Key_F5, Qt.KeyboardModifier.NoModifier),
        (Qt.Key.Key_F8, Qt.KeyboardModifier.NoModifier),
        (Qt.Key.Key_N, Qt.KeyboardModifier.ControlModifier),
    ):
        QTest.keyClick(w, key, mod)
    assert sitzung.befehle == []
    w.reiter.setCurrentIndex(0)
    assert {n: getattr(w, n).isEnabled() for n in messen} == messen  # wie vorher


def test_ui_20_reiterkopf_laeuft_und_faelle(baue: Bauer, qtbot: QtBot) -> None:
    sitzung = AttrappenSitzung(bild())
    w, _ = baue(sitzung=sitzung)
    w.auswerten.btn_oeffnen.setFocus()
    fokus_vorher = QApplication.focusWidget()
    assert fokus_vorher is w.auswerten.btn_oeffnen
    sitzung.setze(durchgang=Z.LAEUFT)
    w.aktualisiere()
    assert w.reiter.tabText(0) == "Messen ▶ läuft"
    sitzung.setze(durchgang=Z.WARTET_AUF_ENTSCHEIDUNG)
    w.aktualisiere()
    assert w.reiter.tabText(0) == "Messen ⚠ Entscheidung nötig"
    sitzung.setze(durchgang=Z.WARTET_AUF_BESTAETIGUNG)
    w.aktualisiere()
    assert w.reiter.tabText(0) == "Messen ⚠ Bestätigung nötig"
    sitzung.setze(durchgang=Z.GERAET_UNKLAR)
    w.aktualisiere()
    assert w.reiter.tabText(0) == "Messen ✖ Gerät unklar"
    sitzung.setze(durchgang=Z.BEREIT)
    w.aktualisiere()
    assert w.reiter.tabText(0) == "Messen"
    # nie automatisch wechseln, nie den Fokus verschieben
    assert w.reiter.currentIndex() == 1
    assert QApplication.focusWidget() is fokus_vorher


# --- Keine Datei (UI-3) ------------------------------------------------------------------------


def test_ui_3_keine_datei(baue: Bauer) -> None:
    w, _ = baue()
    a = w.auswerten
    assert a is not None and a.zustand is aa.AuswertenZustand.KEINE_DATEI
    assert a.plot_platzhalter.text() == "Noch keine Messdatei geöffnet."
    assert a.plot_platzhalter.isVisible() and a.btn_oeffnen_leer.isVisible()
    assert a.btn_oeffnen.isEnabled()
    for knopf in (a.btn_export, a.btn_bild, *a.btn_ansicht.values()):
        assert not knopf.isEnabled()
        assert knopf.toolTip() == "Zuerst eine Messdatei öffnen."
    assert not a.liste_punkte.isEnabled() and not a.chk["X"].isEnabled()
    assert a.parameterzeile.height() == tokens.HOEHE_PARAMETERZEILE_PX == 44
    assert [z.wert.text() for z in a.parameterzeile.zellen] == ["–"] * 7
    assert a.lbl_pruefung.text() == "Prüfung: –"


def test_ui_3_ansichtswahl_namen_und_accessible(baue: Bauer) -> None:
    w, _ = baue()
    a = w.auswerten
    assert a is not None
    assert [a.btn_ansicht[n].text() for n in (1, 2, 3, 4)] == [
        "1 Spektrum",
        "2 H1/H2 und Kohärenz",
        "3 Spitzen und Bänder",
        "4 Schwingform",
    ]
    assert a.btn_ansicht[1].accessibleName() == "Ansicht 1: Spektrum"
    assert a.btn_ansicht[1].isChecked()


# --- Laden (UI-1, UI-2, UI-15) ---------------------------------------------------------------


def test_ui_1_ui_2_geladen_zeigt_spektrum_und_parameter(baue: Bauer, qtbot: QtBot) -> None:
    w, prot = baue()
    a = lade(qtbot, w)
    assert prot.lese == [PFAD]
    assert a.btn_ansicht[1].isChecked() and a.ansicht == 1
    ax = a.plot.zeichnung.achsen[0]  # type: ignore[union-attr]
    assert len(linien(a)) >= 1
    assert ax.get_xlabel() == "Frequenz [Hz]" and ax.get_ylabel() == "Amplitude [m/s]"
    wert = {z.objectName(): z.wert.text() for z in a.parameterzeile.zellen}
    assert wert["par_bandbreite"] == "32 Hz"
    assert wert["par_linien"] == "64"
    assert wert["par_delta_f"] == "0,5 Hz"
    assert wert["par_mittelung"] == "7 (komplex)"
    assert wert["par_fenster"] == "–"
    assert wert["par_punkte"] == "4"
    assert wert["par_referenz"] == "Ref1 [N]"
    fenster = next(z for z in a.parameterzeile.zellen if z.objectName() == "par_fenster")
    assert fenster.toolTip() == "in der Datei nicht lesbar"
    assert a.lbl_datei.text() == "probe.svd" and a.lbl_pfad.volltext() == PFAD
    assert a.lbl_cursor.text() == f"Geladen: {PFAD}"
    assert a.btn_export.isEnabled() and "Strg+E" in a.btn_export.toolTip()  # T4
    for nr in (1, 2, 3, 4):  # T3b: alle Ansichten frei
        assert a.btn_ansicht[nr].isEnabled() and f"Strg+{nr}" in a.btn_ansicht[nr].toolTip()
    assert a.liste_punkte.isEnabled()


def test_ui_1_beispieldatei_spektrum_und_parameterzeile(
    baue: Bauer, qtbot: QtBot, monkeypatch: pytest.MonkeyPatch
) -> None:
    if not BEISPIEL.exists():
        pytest.skip("Beispieldatei Input/20261012_ref_Mitte.svd fehlt")
    from ldv_automation.auswertung.jobs import lese_job as echter_lese_job

    w, _ = baue()
    monkeypatch.setattr(auswerten_reiter, "lese_job", echter_lese_job)
    a = w.auswerten
    assert a is not None
    a.oeffne_datei(str(BEISPIEL))
    qtbot.waitUntil(lambda: a.zustand is aa.AuswertenZustand.GELADEN, timeout=20000)
    wert = {z.objectName(): z.wert.text() for z in a.parameterzeile.zellen}
    assert (wert["par_bandbreite"], wert["par_linien"], wert["par_delta_f"]) == (
        "1000 Hz",
        "1600",
        "0,625 Hz",
    )
    assert wert["par_fenster"] == "–"
    ax = a.plot.zeichnung.achsen[0]
    assert len(ax.lines) >= 1 and ax.get_xlabel() == "Frequenz [Hz]"
    assert ax.get_ylabel() == "Amplitude [m/s]"
    a.beende()


def test_ui_15_laden_sperrt_aa_ac_ad_und_oberflaeche_bleibt_bedienbar(
    baue: Bauer, qtbot: QtBot
) -> None:
    ausf = NieFertigAusfuehrer()
    w, _ = baue(ausf)
    a = w.auswerten
    assert a is not None
    a.oeffne_datei(PFAD)
    assert a.zustand is aa.AuswertenZustand.LADEN
    assert a.lbl_laden.text() == "Lese probe.svd …" and a.laden_leiste.isVisible()
    assert a.balken_laden.minimum() == 0 and a.balken_laden.maximum() == 0  # unbestimmt
    assert not a.btn_oeffnen.isEnabled() and not a.btn_oeffnen_leer.isEnabled()
    assert not a.btn_ansicht[1].isEnabled() and not a.liste_punkte.isEnabled()
    assert not a.plot_platzhalter.isVisible()  # „Keine Datei“ steht nicht mehr da
    # ein Klick auf den Reiter „Messen“ wird währenddessen verarbeitet
    leiste = w.reiter.tabBar()
    QTest.mouseClick(leiste, Qt.MouseButton.LeftButton, pos=leiste.tabRect(0).center())
    assert w.reiter.currentIndex() == 0
    w.reiter.setCurrentIndex(1)
    assert a.zustand is aa.AuswertenZustand.LADEN


def test_ui_15_bisherige_datei_bleibt_ausgegraut_sichtbar(baue: Bauer, qtbot: QtBot) -> None:
    ausf = SteuerbarerAusfuehrer()
    w, _ = baue(ausf)
    a = w.auswerten
    assert a is not None
    a.oeffne_datei(PFAD)
    ausf.auftraege[0].freigegeben = True
    a._abfrage()
    assert a.zustand is aa.AuswertenZustand.GELADEN
    zeichnung = a.plot.zeichnung
    a.oeffne_datei("C:\\zweite.svd")
    assert a.zustand.value == "laden"
    assert a.lbl_laden.text() == "Lese zweite.svd …"
    assert a.plot.isVisible() and a.plot.zeichnung is zeichnung  # bisherige Datei sichtbar
    assert a._grau_effekt.isEnabled() and a._grau_effekt.opacity() < 1.0
    assert not a.plot.isEnabled()
    a.beende()


def test_zweistufiges_laden_pruefung_wird_berechnet(baue: Bauer, qtbot: QtBot) -> None:
    ausf = SteuerbarerAusfuehrer()
    w, _ = baue(ausf)
    a = w.auswerten
    assert a is not None
    a.oeffne_datei(PFAD)
    assert len(ausf.auftraege) == 1
    ausf.auftraege[0].freigegeben = True
    a._abfrage()  # Stufe A fertig: Ansicht 1 sofort
    assert a.zustand is aa.AuswertenZustand.GELADEN and len(linien(a)) == 4
    assert a.lbl_pruefung.text() == "Prüfung: wird berechnet …"
    assert a.laeuft() and a.pruefung is None
    assert len(ausf.auftraege) == 2
    ausf.auftraege[1].freigegeben = True
    a._abfrage()  # Stufe B fertig
    assert a.lbl_pruefung.text() == "Prüfung: 1 Warnung, 1 ok"
    assert a.pruefung is not None and not a.laeuft()
    assert not a._timer.isActive()


def test_p08_antriebspunkt_wird_uebergeben_wenn_ref2_ref1_vorhanden(
    baue: Bauer, qtbot: QtBot
) -> None:
    w, prot = baue()
    prot.geladen[PFAD] = synth_geladen(mit_ref2=True)
    lade(qtbot, w)
    assert prot.pruef == [(PFAD, SHA, ("Ref2", "Ref1", "akzeleranz"))]


def test_p08_ohne_die_kanaele_ist_nicht_pruefbar(baue: Bauer, qtbot: QtBot) -> None:
    w, prot = baue()
    lade(qtbot, w)
    assert prot.pruef == [(PFAD, SHA, None)]


def test_pruefung_fehler_steht_in_der_fusszeile(baue: Bauer, qtbot: QtBot) -> None:
    w, prot = baue()
    prot.pruef_fehler = "kaputt"
    a = lade(qtbot, w)
    assert a.lbl_pruefung.text() == "✖ Prüfung nicht möglich: kaputt"
    assert a.zustand is aa.AuswertenZustand.GELADEN  # Ansicht 1 bleibt


# --- Fehler beim Lesen (UI-15, UI-24) -----------------------------------------------------------


def test_ui_24_fehler_ohne_vorherige_datei_zeigt_band_und_keine_datei(
    baue: Bauer, qtbot: QtBot
) -> None:
    w, prot = baue()
    a = w.auswerten
    assert a is not None
    prot.fehler_lese["C:\\x.svd"] = "C:\\x.svd: keine gültige PSV-Datei"
    a.oeffne_datei("C:\\x.svd")
    qtbot.waitUntil(lambda: a.fehlertext is not None, timeout=3000)
    assert a.band_fehler.isVisible()
    assert (
        a.lbl_fehler.text()
        == "✖ Datei kann nicht gelesen werden: C:\\x.svd: keine gültige PSV-Datei"
    )
    assert a.zustand is aa.AuswertenZustand.KEINE_DATEI
    assert a.plot_platzhalter.isVisible() and a.plot_platzhalter.text() == aa.TEXT_KEINE_DATEI
    assert a.btn_oeffnen.isEnabled()
    assert not a.laeuft() and not a._timer.isActive()
    a.btn_fehler_schliessen.click()
    assert not a.band_fehler.isVisible() and a.fehlertext is None


def test_ui_15_fehler_laesst_vorherige_datei_unveraendert(baue: Bauer, qtbot: QtBot) -> None:
    w, prot = baue()
    a = lade(qtbot, w)
    geladen, zeichnung = a.geladen, a.plot.zeichnung
    wert_vorher = [z.wert.text() for z in a.parameterzeile.zellen]
    prot.fehler_lese["C:\\x.svd"] = "C:\\x.svd: abgeschnitten"
    a.oeffne_datei("C:\\x.svd")
    qtbot.waitUntil(lambda: a.fehlertext is not None, timeout=3000)
    assert a.band_fehler.isVisible() and "abgeschnitten" in a.lbl_fehler.text()
    assert a.zustand is aa.AuswertenZustand.GELADEN
    assert a.geladen is geladen and a.plot.zeichnung is zeichnung
    assert [z.wert.text() for z in a.parameterzeile.zellen] == wert_vorher
    assert a.lbl_datei.text() == "probe.svd"
    assert a.btn_ansicht[1].isEnabled() and a.plot.isEnabled() and not a._grau_effekt.isEnabled()
    # ein neuer Dateiaufruf blendet das Band aus
    a.oeffne_datei(PFAD)
    assert not a.band_fehler.isVisible()
    a.beende()


def test_prozess_nicht_startbar_ist_ein_lesefehler(baue: Bauer) -> None:
    class Defekt:
        def starte(self, *_a: object) -> None:
            raise OSError("Spawn nicht möglich")

        def beende(self) -> None:
            pass

    w, _ = baue(Defekt())
    a = w.auswerten
    assert a is not None
    a.oeffne_datei(PFAD)
    assert a.fehlertext is not None and "Spawn nicht möglich" in a.fehlertext
    assert a.zustand is aa.AuswertenZustand.KEINE_DATEI and not a.laeuft()


def test_neuer_dateiaufruf_bricht_alten_auftrag_ab_und_job_id_verwirft_altes(
    baue: Bauer, qtbot: QtBot
) -> None:
    ausf = SteuerbarerAusfuehrer()
    w, prot = baue(ausf)
    a = w.auswerten
    assert a is not None
    a.oeffne_datei("C:\\eins.svd")
    a.oeffne_datei("C:\\zwei.svd")
    erster, zweiter = ausf.auftraege
    assert erster.abgebrochen and not zweiter.abgebrochen
    erster.freigegeben = True  # veraltetes Ergebnis darf nichts bewirken
    a._abfrage()
    assert a.geladen is None and a.zustand is aa.AuswertenZustand.LADEN
    zweiter.freigegeben = True
    a._abfrage()
    assert a.geladen is not None and a.lbl_datei.text() == "zwei.svd"
    assert prot.lese == ["C:\\zwei.svd"]  # nur das aktuelle Ergebnis wurde je abgeholt
    a.beende()


def test_stale_job_id_wird_verworfen_und_abgebrochen(baue: Bauer) -> None:
    ausf = SteuerbarerAusfuehrer()
    w, prot = baue(ausf)
    a = w.auswerten
    assert a is not None
    a.oeffne_datei(PFAD)
    auftrag = ausf.auftraege[0]
    auftrag.freigegeben = True
    a._auftrag_a = (a._job_id - 1, auftrag, PFAD)  # Eintrag einer früheren Anfrage
    a._abfrage()
    assert auftrag.abgebrochen and a._auftrag_a is None and a.geladen is None
    assert prot.lese == []
    a.oeffne_datei(PFAD)
    ausf.auftraege[1].freigegeben = True
    a._abfrage()
    a._auftrag_b = (a._job_id - 1, ausf.auftraege[2])  # veraltete Prüfung
    ausf.auftraege[2].freigegeben = True
    a._abfrage()
    assert a.pruefung is None and ausf.auftraege[2].abgebrochen


def test_close_beendet_den_ausfuehrer_und_bricht_auftraege_ab(baue: Bauer) -> None:
    ausf = NieFertigAusfuehrer()
    w, _ = baue(ausf)
    a = w.auswerten
    assert a is not None
    a.oeffne_datei(PFAD)
    assert a.laeuft()
    w.close()
    assert ausf.beendet and ausf.auftraege[0].abgebrochen
    assert not a.laeuft() and not a._timer.isActive()


def test_open_dialog_uebergibt_pfad_und_abbruch_tut_nichts(
    baue: Bauer, qtbot: QtBot, monkeypatch: pytest.MonkeyPatch
) -> None:
    w, prot = baue()
    a = w.auswerten
    assert a is not None
    monkeypatch.setattr(a, "_waehle_datei", lambda: None)
    a.btn_oeffnen.click()
    assert prot.lese == [] and a.zustand is aa.AuswertenZustand.KEINE_DATEI
    monkeypatch.setattr(a, "_waehle_datei", lambda: PFAD)
    a.btn_oeffnen_leer.click()
    qtbot.waitUntil(lambda: a.zustand is aa.AuswertenZustand.GELADEN, timeout=3000)
    assert prot.lese == [PFAD]


# --- Ansicht 1 (UI-4) -----------------------------------------------------------------------------


def test_ui_4_voreinstellung_log_mittel_alle_komponenten(baue: Bauer, qtbot: QtBot) -> None:
    w, _ = baue()
    a = lade(qtbot, w)
    assert a.auswahl == (None, ("X", "Y", "Z", "3D"), "kohaerent", "log")
    assert a.liste_punkte.count() == 5 and a.liste_punkte.currentRow() == 0
    assert a.liste_punkte.item(0).text() == "Mittel (alle Punkte)"
    assert a.liste_punkte.item(1).text().startswith("Punkt 10 (x 0,000;")
    assert a.rb_skala_log.isChecked() and a.rb_groesse_cph.isChecked()
    ln = linien(a)
    assert list(ln) == ["X", "Y", "Z", "3D"]
    stile = [ln[c].get_linestyle() for c in ln]
    assert len(set(stile)) == 4  # paarweise verschieden
    assert a.plot.zeichnung.achsen[0].get_yscale() == "log"  # type: ignore[union-attr]
    assert a.lbl_plotkopf.text() == (
        "probe.svd · Mittel (alle Punkte) · X, Y, Z, 3D · Geschwindigkeit, kohärent mit Ref1"
    )
    assert "Punkte" in a.lbl_hinweise.text() and not a.lbl_hinweise.isHidden()
    assert a.plot.canvas.accessibleName() == "Diagramm: Spektrum"
    assert "probe.svd" in a.plot.canvas.accessibleDescription()


def test_ui_4_komponenten_einzeln_und_gemeinsam(baue: Bauer, qtbot: QtBot) -> None:
    w, _ = baue()
    a = lade(qtbot, w)
    a.chk["X"].setChecked(False)
    assert list(linien(a)) == ["Y", "Z", "3D"]
    a.chk["3D"].setChecked(False)
    a.chk["Y"].setChecked(False)
    assert list(linien(a)) == ["Z"]
    a.chk["X"].setChecked(True)
    assert list(linien(a)) == ["X", "Z"]
    assert a.auswahl[1] == ("X", "Z")


def test_ui_4_letzte_komponente_laesst_sich_nicht_abwaehlen(baue: Bauer, qtbot: QtBot) -> None:
    w, _ = baue()
    a = lade(qtbot, w)
    for c in ("X", "Y", "3D"):
        a.chk[c].setChecked(False)
    assert list(linien(a)) == ["Z"]
    a.chk["Z"].click()  # Klick auf die letzte gewählte Komponente
    assert a.chk["Z"].isChecked()
    assert list(linien(a)) == ["Z"] and a.auswahl[1] == ("Z",)


def test_ui_4_punkt_und_skala_und_groesse(baue: Bauer, qtbot: QtBot) -> None:
    w, _ = baue()
    a = lade(qtbot, w)
    a.liste_punkte.setCurrentRow(2)
    assert a.auswahl[0] == 1 and len(linien(a)) == 4
    assert "Punkt 11" in a.lbl_plotkopf.text()
    a.rb_skala_linear.setChecked(True)
    assert a.plot.zeichnung.achsen[0].get_yscale() == "linear"  # type: ignore[union-attr]
    a.rb_groesse_ap.setChecked(True)
    assert a.auswahl[2] == "leistung"
    assert "Leistungsmittel" in a.lbl_plotkopf.text()
    a.liste_punkte.setCurrentRow(0)
    assert a.auswahl[0] is None


def test_ui_4_db_ist_deaktiviert_mit_grund(baue: Bauer, qtbot: QtBot) -> None:
    w, _ = baue()
    a = lade(qtbot, w)
    assert not a.rb_skala_db.isEnabled()
    assert "keine Referenzgröße (0 dB) in der Datei" in a.rb_skala_db.toolTip()
    assert a.lbl_db_grund.isVisible()


def test_ui_4_kohaerent_gesperrt_ohne_referenz(baue: Bauer, qtbot: QtBot) -> None:
    w, prot = baue()
    prot.geladen[PFAD] = synth_geladen(referenz=False)
    a = lade(qtbot, w)
    assert not a.rb_groesse_cph.isEnabled() and a.rb_groesse_ap.isChecked()
    assert "Keine Referenz" in a.rb_groesse_cph.toolTip()
    assert a.lbl_groesse_grund.isVisible() and "Keine Referenz" in a.lbl_groesse_grund.text()
    assert a.auswahl[2] == "leistung" and len(linien(a)) == 4
    assert [z.wert.text() for z in a.parameterzeile.zellen][-1] == "keine"
    assert prot.pruef == [(PFAD, SHA, None)]


def test_oe_3_auswahl_wird_beim_dateiwechsel_zurueckgesetzt(baue: Bauer, qtbot: QtBot) -> None:
    w, _ = baue()
    a = lade(qtbot, w)
    a.liste_punkte.setCurrentRow(3)
    a.chk["X"].setChecked(False)
    a.rb_skala_linear.setChecked(True)
    a.rb_groesse_ap.setChecked(True)
    lade(qtbot, w, "C:\\messungen\\zweite.svd")
    # UI-6 (R-073): Punkt, Komponenten, Größe werden zurückgesetzt, die Skala (linear/log) bleibt
    assert a.auswahl == (None, ("X", "Y", "Z", "3D"), "kohaerent", "linear")
    assert a.rb_skala_linear.isChecked()
    assert a.liste_punkte.currentRow() == 0 and a.chk["X"].isChecked()
    assert a.lbl_datei.text() == "zweite.svd"


# --- Plot und Werkzeugleiste (UI-12, UI-21) -------------------------------------------------------


def test_toolbar_deutsch_nur_textknoepfe_fokussierbar(baue: Bauer, qtbot: QtBot) -> None:
    w, _ = baue()
    a = lade(qtbot, w)
    tb = a.plot.toolbar
    texte = [akt.text() for akt in tb.actions() if akt.text()]
    assert texte == ["Zurücksetzen", "Zurück", "Vor", "Verschieben", "Zoom"]
    assert tb.toolButtonStyle() == Qt.ToolButtonStyle.ToolButtonTextOnly
    assert all(k.focusPolicy() == Qt.FocusPolicy.StrongFocus for k in tb.knoepfe())
    assert [k.objectName() for k in tb.knoepfe()] == [
        "btn_plot_zuruecksetzen",
        "btn_plot_zurueck",
        "btn_plot_vor",
        "btn_plot_verschieben",
        "btn_plot_zoom",
    ]
    assert not any(t in ("Save", "Subplots", "Customize") for t in texte)
    assert a.plot.canvas.focusPolicy() == Qt.FocusPolicy.StrongFocus
    assert a.plot.objectName() == "plot"


def test_plot_fokus_zeigt_rahmen(baue: Bauer, qtbot: QtBot) -> None:
    w, _ = baue()
    a = lade(qtbot, w)
    w.activateWindow()
    rahmen = a.plot.findChild(QWidget, "plot_rahmen")
    assert rahmen is not None and rahmen.property("fokus") in (None, "false")
    a.plot.canvas.setFocus()
    qtbot.waitUntil(lambda: rahmen.property("fokus") == "true", timeout=2000)
    w.reiter.tabBar().setFocus()
    qtbot.waitUntil(lambda: rahmen.property("fokus") == "false", timeout=2000)
    assert 'QFrame#plot_rahmen[fokus="true"]' in stil.QSS
    assert f"border: 2px solid {tokens.C_AKZENT}" in stil.QSS


def test_ui_12_zoom_zuruecksetzen_und_neue_datei_setzt_zoom_zurueck(
    baue: Bauer, qtbot: QtBot
) -> None:
    # P-AUSW2 S2: Zurücksetzen heißt „Auto“ und zeichnet neu (neue Achsenobjekte), der Zoom steht
    # als fester Bereich im Achsenzustand (eine Quelle).
    w, _ = baue()
    a = lade(qtbot, w)
    ax = a.plot.zeichnung.achsen[0]  # type: ignore[union-attr]
    x0 = ax.get_xlim()
    ax.set_xlim(5.0, 10.0)
    a.plot.toolbar.push_current()
    assert ax.get_xlim() == (5.0, 10.0)
    assert a.plot.achsen_zustand.bereich(1, "frequenz") == Bereich(5.0, 10.0)  # Zoom → fest
    a.plot.zoom_zuruecksetzen()
    ax = a.plot.zeichnung.achsen[0]  # type: ignore[union-attr]
    assert ax.get_xlim() == pytest.approx(x0)
    assert a.plot.achsen_zustand.bereich(1, "frequenz").ist_auto  # Zurücksetzen → Auto
    ax.set_xlim(5.0, 10.0)
    a.plot.toolbar.push_current()
    a.plot.toolbar.back()  # Zurück: letzter Verlaufseintrag (Standardansicht)
    assert ax.get_xlim() == pytest.approx(x0)
    ax.set_xlim(5.0, 10.0)
    lade(qtbot, w, "C:\\messungen\\zweite.svd")
    ax2 = a.plot.zeichnung.achsen[0]  # type: ignore[union-attr]
    assert ax2.get_xlim() == pytest.approx(x0)  # neuer Dateiaufruf: Zoom zurückgesetzt


def test_plotstil_rcparams_global_gesetzt_beim_aufbau(baue: Bauer) -> None:
    w, _ = baue()
    a = w.auswerten
    assert a is not None
    stil_rc = a.plot._stil.rc()
    for schluessel in ("axes.edgecolor", "axes.facecolor", "font.size", "grid.color"):
        assert matplotlib.rcParams[schluessel] == stil_rc[schluessel], schluessel
    assert matplotlib.rcParams["axes.facecolor"] == tokens.C_PLOT_FLAECHE


def test_pos1_zurücksetzen_ueber_knopf(baue: Bauer, qtbot: QtBot) -> None:
    w, _ = baue()
    a = lade(qtbot, w)
    ax = a.plot.zeichnung.achsen[0]  # type: ignore[union-attr]
    x0 = ax.get_xlim()
    ax.set_xlim(2.0, 4.0)
    a.plot.toolbar.push_current()
    a.plot.toolbar.knoepfe()[0].click()
    # Zurücksetzen zeichnet neu (P-AUSW2 S2): die Achsen sind neue Objekte
    assert a.plot.zeichnung.achsen[0].get_xlim() == pytest.approx(x0)  # type: ignore[union-attr]


# --- Tab-Reihenfolge, Geometrie (UI-21, UI-25) ----------------------------------------------------


def test_ui_21_tab_reihenfolge_im_reiter_auswerten(baue: Bauer, qtbot: QtBot) -> None:
    w, _ = baue()
    a = lade(qtbot, w)
    w.activateWindow()
    qtbot.waitUntil(w.isActiveWindow, timeout=2000)
    for b in a.findChildren(QAbstractButton):
        if b.isVisible() and b.isEnabled():
            assert b.focusPolicy() != Qt.FocusPolicy.NoFocus, b.objectName()
    a.btn_oeffnen.setFocus()
    reihe = [QApplication.focusWidget().objectName()]  # type: ignore[union-attr]
    for _ in range(30):
        taste(qtbot, QApplication.focusWidget(), Qt.Key.Key_Tab)  # type: ignore[arg-type]
        reihe.append(QApplication.focusWidget().objectName())  # type: ignore[union-attr]
    erwartet = [
        "btn_oeffnen",
        "btn_ansicht_1",
        "liste_punkte",
        "chk_x",
        "chk_y",
        "chk_z",
        "chk_3d",
        "rb_groesse_cph",
        "rb_skala_log",  # Tab-Halt auf der gewählten Option
        "plot_canvas",
        "btn_plot_zuruecksetzen",
    ]
    positionen = [reihe.index(n) for n in erwartet]
    assert positionen == sorted(positionen), reihe
    assert "parameterzeile" not in reihe and not any(n.startswith("par_") for n in reihe)


def rechtecke(w: Hauptfenster, a: AuswertenReiter) -> dict[str, tuple[int, int, int, int]]:
    ergebnis = {}
    for name in (
        "dateileiste",
        "parameterzeile",
        "ansichtswahl",
        "auswahlspalte",
        "darstellung",
        "fusszeile",
    ):
        wid = a.findChild(QWidget, name)
        assert wid is not None, name
        oben_links = wid.mapTo(w, QPoint(0, 0))
        ergebnis[name] = (oben_links.x(), oben_links.y(), wid.width(), wid.height())
    return ergebnis


@pytest.mark.parametrize(("breite", "hoehe"), [(1100, 680), (1366, 768)])
def test_ui_25_kein_element_ueberlappt(baue: Bauer, qtbot: QtBot, breite: int, hoehe: int) -> None:
    w, _ = baue()
    w.resize(breite, hoehe)
    a = lade(qtbot, w)
    qtbot.waitUntil(lambda: w.width() == breite, timeout=2000)
    r = rechtecke(w, a)
    namen = list(r)
    for i, n1 in enumerate(namen):
        x1, y1, b1, h1 = r[n1]
        assert b1 > 0 and h1 > 0, n1
        for n2 in namen[i + 1 :]:
            x2, y2, b2, h2 = r[n2]
            ueberlappt = x1 < x2 + b2 and x2 < x1 + b1 and y1 < y2 + h2 and y2 < y1 + h1
            assert not ueberlappt, (n1, n2, r[n1], r[n2])
    # feste Höhen
    assert r["dateileiste"][3] == tokens.HOEHE_DATEILEISTE_PX
    assert r["parameterzeile"][3] == tokens.HOEHE_PARAMETERZEILE_PX
    assert r["ansichtswahl"][3] == tokens.HOEHE_ANSICHTSWAHL_PX
    assert r["fusszeile"][3] == tokens.HOEHE_FUSSZEILE_PX
    assert r["auswahlspalte"][2] == tokens.BREITE_AUSWAHLSPALTE_PX
    assert r["darstellung"][2] >= tokens.PLOT_MIN_BREITE_PX
    assert r["darstellung"][3] >= tokens.PLOT_MIN_HOEHE_PX
    # Fenster-Mindestgröße: alles liegt im Fenster
    for name, (x, y, bb, hh) in r.items():
        assert x >= 0 and y >= 0 and x + bb <= breite and y + hh <= hoehe, name


def test_ui_25_ae_mindestens_600_x_320_bei_1366_x_768(baue: Bauer, qtbot: QtBot) -> None:
    w, _ = baue()
    a = lade(qtbot, w)
    ae = a.findChild(QWidget, "darstellung")
    assert ae is not None
    assert ae.width() >= 600 and ae.height() >= 320
    assert a.plot.canvas.width() > 0 and a.plot.canvas.height() > 0


def test_parameterzeile_blendet_rechts_aus_und_tooltip_nennt_alles(
    baue: Bauer, qtbot: QtBot
) -> None:
    w, _ = baue()
    a = lade(qtbot, w)
    zeile = a.parameterzeile
    assert zeile.sichtbare_zellen() == [z.objectName() for z in zeile.zellen]
    zeile.setFixedWidth(260)
    zeile.blende_aus()
    sichtbar = zeile.sichtbare_zellen()
    assert 0 < len(sichtbar) < 7
    assert sichtbar == [z.objectName() for z in zeile.zellen][: len(sichtbar)]  # rechts fehlt
    assert "Referenz: Ref1 [N]" in zeile.toolTip() and "Bandbreite: 32 Hz" in zeile.toolTip()
    assert zeile.height() == tokens.HOEHE_PARAMETERZEILE_PX
    zeile.setMinimumWidth(0)
    zeile.setMaximumWidth(16777215)
    zeile.blende_aus()
    assert len(zeile.sichtbare_zellen()) >= len(sichtbar)


def tab_namen(qtbot: QtBot, start: QWidget, n: int = 30) -> list[str]:
    start.setFocus()
    reihe = [QApplication.focusWidget().objectName()]  # type: ignore[union-attr]
    for _ in range(n):
        taste(qtbot, QApplication.focusWidget(), Qt.Key.Key_Tab)  # type: ignore[arg-type]
        reihe.append(QApplication.focusWidget().objectName())  # type: ignore[union-attr]
    return reihe


def test_tab_halt_der_radiogruppen_liegt_auf_der_gewaehlten_option(
    baue: Bauer, qtbot: QtBot
) -> None:
    w, _ = baue()
    a = lade(qtbot, w)
    w.activateWindow()
    qtbot.waitUntil(w.isActiveWindow, timeout=2000)
    reihe = tab_namen(qtbot, a.btn_oeffnen)
    assert "rb_skala_log" in reihe and "rb_skala_linear" not in reihe
    assert "rb_groesse_cph" in reihe and "rb_groesse_ap" not in reihe
    a.rb_skala_linear.setChecked(True)
    a.rb_groesse_ap.setChecked(True)
    reihe = tab_namen(qtbot, a.btn_oeffnen)
    assert "rb_skala_linear" in reihe and "rb_skala_log" not in reihe
    assert "rb_groesse_ap" in reihe and "rb_groesse_cph" not in reihe
    # UI-21: alle bleiben fokussierbar (Klick, Pfeiltasten)
    for knopf in (a.rb_skala_log, a.rb_groesse_cph):
        assert knopf.focusPolicy() != Qt.FocusPolicy.NoFocus


def test_zoom_bleibt_bei_auswahlwechsel_erhalten_und_zuruecksetzen_fuehrt_zurueck(
    baue: Bauer, qtbot: QtBot
) -> None:
    w, _ = baue()
    a = lade(qtbot, w)
    x0 = a.plot.zeichnung.achsen[0].get_xlim()  # type: ignore[union-attr]
    ax = a.plot.zeichnung.achsen[0]  # type: ignore[union-attr]
    ax.set_xlim(5.0, 10.0)
    a.plot.toolbar.push_current()
    aenderungen: list[Callable[[], object]] = [
        lambda: a.liste_punkte.setCurrentRow(2),
        lambda: a.chk["X"].setChecked(False),
        lambda: a.rb_groesse_ap.setChecked(True),
        lambda: a.rb_skala_linear.setChecked(True),
    ]
    for aendern in aenderungen:
        aendern()
        assert a.plot.zeichnung.achsen[0].get_xlim() == pytest.approx((5.0, 10.0))  # type: ignore[union-attr]
    a.plot.zoom_zuruecksetzen()
    assert a.plot.zeichnung.achsen[0].get_xlim() == pytest.approx(x0)  # type: ignore[union-attr]
    # nach dem Zurücksetzen bleibt der volle Bereich bei weiterem Wechsel
    a.liste_punkte.setCurrentRow(1)
    assert a.plot.zeichnung.achsen[0].get_xlim() == pytest.approx(x0)  # type: ignore[union-attr]


def test_zoom_wird_bei_neuem_dateiaufruf_zurueckgesetzt_auch_bei_gleicher_achse(
    baue: Bauer, qtbot: QtBot
) -> None:
    w, _ = baue()
    a = lade(qtbot, w)
    x0 = a.plot.zeichnung.achsen[0].get_xlim()  # type: ignore[union-attr]
    a.plot.zeichnung.achsen[0].set_xlim(5.0, 10.0)  # type: ignore[union-attr]
    lade(qtbot, w, "C:\\messungen\\zweite.svd")
    assert a.plot.zeichnung.achsen[0].get_xlim() == pytest.approx(x0)  # type: ignore[union-attr]


def test_zoom_zurueck_geht_auf_standardansicht(baue: Bauer, qtbot: QtBot) -> None:
    # P-AUSW2 S2: Nach einem Neuzeichnen beginnt der Verlauf der Werkzeugleiste mit dem dann
    # gültigen (festen) Ausschnitt; „Zurück“ geht innerhalb einer Zeichnung auf die Standardansicht.
    w, _ = baue()
    a = lade(qtbot, w)
    ax = a.plot.zeichnung.achsen[0]  # type: ignore[union-attr]
    x0 = ax.get_xlim()
    ax.set_xlim(5.0, 10.0)
    a.plot.toolbar.push_current()
    a.plot.toolbar.back()
    assert ax.get_xlim() == pytest.approx(x0)
    assert a.plot.achsen_zustand.bereich(1, "frequenz") == Bereich(*x0)  # Verlauf schreibt Grenzen


def test_barrierefreiheit_pfad_ist_voll_im_accessible_name(baue: Bauer, qtbot: QtBot) -> None:
    w, _ = baue()
    a = lade(qtbot, w)
    w.resize(1100, 680)
    lang = "C:\\sehr\\langer\\ordner\\" + "unterordner\\" * 12 + "probe.svd"
    a.lbl_pfad.setText(lang)
    assert a.lbl_pfad.accessibleName() == lang
    assert lang in a.lbl_pfad.accessibleDescription()
    assert a.lbl_pfad.toolTip() == lang and a.lbl_pfad.volltext() == lang


# --- Fehler bei der Aufbereitung und beim Zeichnen (K-AUSW-T3a) ---------------------------


def test_aufbereitung_fehler_wird_wie_lesefehler_gemeldet_ohne_datei(
    baue: Bauer, qtbot: QtBot, monkeypatch: pytest.MonkeyPatch
) -> None:
    def kaputt(*_a: object, **_k: object) -> None:
        raise ValueError("Cache kaputt")

    monkeypatch.setattr(auswerten_reiter, "PaarCache", kaputt)
    w, _ = baue()
    a = w.auswerten
    assert a is not None
    a.oeffne_datei(PFAD)
    qtbot.waitUntil(lambda: a.fehlertext is not None, timeout=3000)
    assert a.zustand is aa.AuswertenZustand.KEINE_DATEI  # nicht in „Laden“ hängen geblieben
    assert PFAD in a.lbl_fehler.text() and "Cache kaputt" in a.lbl_fehler.text()
    assert a.band_fehler.isVisible() and not a.laeuft() and not a._timer.isActive()
    assert a.btn_oeffnen.isEnabled() and not a.laden_leiste.isVisible()
    assert a.plot_platzhalter.isVisible() and a.lbl_pruefung.text() == "Prüfung: –"


def test_aufbereitung_fehler_laesst_vorherige_datei_unveraendert(
    baue: Bauer, qtbot: QtBot, monkeypatch: pytest.MonkeyPatch
) -> None:
    w, _ = baue()
    a = lade(qtbot, w)
    geladen, zeichnung, pruef = a.geladen, a.plot.zeichnung, a.lbl_pruefung.text()

    def kaputt(*_a: object, **_k: object) -> None:
        raise ValueError("Punktliste kaputt")

    monkeypatch.setattr(auswerten_reiter, "punkt_eintraege", kaputt)
    a.oeffne_datei("C:\\zweite.svd")
    qtbot.waitUntil(lambda: a.fehlertext is not None, timeout=3000)
    assert "Punktliste kaputt" in a.lbl_fehler.text()
    assert a.zustand is aa.AuswertenZustand.GELADEN and a.geladen is geladen
    assert a.plot.zeichnung is zeichnung and a.lbl_pruefung.text() == pruef
    assert a.btn_ansicht[1].isEnabled() and a.plot.isEnabled() and not a._timer.isActive()
    assert a.lbl_datei.text() == "probe.svd"


def test_aufbau_der_anzeige_scheitert_reiter_wird_konsistent_zurueckgesetzt(
    baue: Bauer, qtbot: QtBot, monkeypatch: pytest.MonkeyPatch
) -> None:
    w, _ = baue()
    a = w.auswerten
    assert a is not None

    def kaputt() -> None:
        raise ValueError("Größen kaputt")

    monkeypatch.setattr(a, "_aktualisiere_groessen", kaputt)
    a.oeffne_datei(PFAD)
    qtbot.waitUntil(lambda: a.fehlertext is not None, timeout=3000)
    assert "Anzeige nicht möglich" in a.lbl_fehler.text() and "Größen kaputt" in a.lbl_fehler.text()
    assert a.zustand is aa.AuswertenZustand.KEINE_DATEI and a.geladen is None
    assert not a.laeuft() and a.liste_punkte.count() == 0
    assert [z.wert.text() for z in a.parameterzeile.zellen] == ["–"] * 7
    assert a.btn_oeffnen.isEnabled() and a.plot_platzhalter.isVisible()


def test_zeichenfehler_wird_im_fehlerband_gemeldet_nichts_verschluckt(
    baue: Bauer, qtbot: QtBot, monkeypatch: pytest.MonkeyPatch
) -> None:
    def kaputt(*_a: object, **_k: object) -> None:
        raise ValueError("Zeichnen kaputt")

    monkeypatch.setattr(auswerten_reiter, "spektrum_daten", kaputt)
    w, _ = baue()
    a = lade(qtbot, w)  # Stufe A und B laufen trotz Zeichenfehler durch
    assert a.zustand is aa.AuswertenZustand.GELADEN
    assert a.band_fehler.isVisible()
    assert a.lbl_fehler.text() == "✖ Darstellung nicht möglich: Zeichnen kaputt"
    assert a.plot.zeichnung is None  # Darstellung leer, aber gemeldet
    assert a.lbl_pruefung.text() == "Prüfung: 1 Warnung, 1 ok"
    # ein späterer Wechsel meldet erneut
    a.schliesse_fehlerband()
    a.liste_punkte.setCurrentRow(2)
    assert a.band_fehler.isVisible() and "Zeichnen kaputt" in a.lbl_fehler.text()


def test_fusszeile_nach_abbruch_von_stufe_b_und_lesefehler(baue: Bauer, qtbot: QtBot) -> None:
    ausf = SteuerbarerAusfuehrer()
    w, prot = baue(ausf)
    a = w.auswerten
    assert a is not None
    a.oeffne_datei(PFAD)
    ausf.auftraege[0].freigegeben = True
    a._abfrage()  # Datei A da, Stufe B läuft
    assert a.lbl_pruefung.text() == "Prüfung: wird berechnet …"
    prot.fehler_lese["C:\\b.svd"] = "C:\\b.svd: kaputt"
    a.oeffne_datei("C:\\b.svd")  # bricht Stufe B von A ab
    assert ausf.auftraege[1].abgebrochen
    assert a.lbl_pruefung.text() == aa.TEXT_PRUEFUNG_ABGEBROCHEN
    ausf.auftraege[2].freigegeben = True
    a._abfrage()  # Datei B scheitert
    assert a.zustand is aa.AuswertenZustand.GELADEN and a.lbl_datei.text() == "probe.svd"
    assert a.lbl_pruefung.text() == aa.TEXT_PRUEFUNG_ABGEBROCHEN
    assert "wird berechnet" not in a.lbl_pruefung.text()


def test_fusszeile_zeigt_ergebnis_der_angezeigten_datei_nach_lesefehler(
    baue: Bauer, qtbot: QtBot
) -> None:
    w, prot = baue()
    a = lade(qtbot, w)
    assert a.lbl_pruefung.text() == "Prüfung: 1 Warnung, 1 ok"
    prot.fehler_lese["C:\\b.svd"] = "kaputt"
    a.oeffne_datei("C:\\b.svd")
    qtbot.waitUntil(lambda: a.fehlertext is not None, timeout=3000)
    assert a.lbl_pruefung.text() == "Prüfung: 1 Warnung, 1 ok"  # gehört zur angezeigten Datei


# --- Rückfallpfad (K-AUSW-T3a-2) ---------------------------------------------------


def test_rueckfallpfad_mit_dauerhaft_fehlerhafter_parameterzeile(
    baue: Bauer, qtbot: QtBot, monkeypatch: pytest.MonkeyPatch
) -> None:
    w, _ = baue()
    a = w.auswerten
    assert a is not None

    def kaputt(*_a: object, **_k: object) -> None:
        raise ValueError("Parameterzeile kaputt")

    monkeypatch.setattr(a.parameterzeile, "setze_zellen", kaputt)  # dauerhaft, auch im Rückfall
    a.oeffne_datei(PFAD)
    qtbot.waitUntil(lambda: a.fehlertext is not None, timeout=3000)  # kein Absturz im Timer
    assert a.zustand is aa.AuswertenZustand.KEINE_DATEI  # nie „Laden“ nach einer Ausnahme
    assert "Parameterzeile kaputt" in a.lbl_fehler.text() and a.band_fehler.isVisible()
    assert not a.laden_leiste.isVisible() and not a.laeuft() and not a._timer.isActive()
    assert a.geladen is None and a.liste_punkte.count() == 0
    assert a.btn_oeffnen.isEnabled() and a.plot_platzhalter.isVisible()
    assert a.lbl_pruefung.text() == "Prüfung: –"


def test_lesefehler_scheitert_selbst_nicht(
    baue: Bauer, qtbot: QtBot, monkeypatch: pytest.MonkeyPatch
) -> None:
    ausf = SteuerbarerAusfuehrer()
    w, prot = baue(ausf)
    a = w.auswerten
    assert a is not None
    prot.fehler_lese[PFAD] = f"{PFAD}: kaputt"

    def kaputt() -> None:
        raise RuntimeError("Widgets kaputt")

    a.oeffne_datei(PFAD)
    monkeypatch.setattr(a, "_wende_zustand_an", kaputt)
    monkeypatch.setattr(a, "_zeige_pruefung", kaputt)
    ausf.auftraege[0].freigegeben = True
    a._abfrage()  # darf nicht werfen
    assert a.zustand is aa.AuswertenZustand.KEINE_DATEI
    assert a.band_fehler.isVisible() and "kaputt" in a.lbl_fehler.text()
    assert not a.laden_leiste.isVisible() and not a._timer.isActive() and not a.laeuft()


# --- Neuzeichnen bei Größenänderung (K-AUSW-T3a-2) ---------------------------------------------


class Zeichner:
    """Ersatz für eine Zeichenfunktion: zählt Aufrufe und merkt die Figure-Größe in Pixeln."""

    def __init__(self) -> None:
        self.aufrufe = 0
        self.groessen: list[tuple[float, float]] = []

    def __call__(self, fig: Any, _daten: object, opt: object, _stil: object) -> Zeichnung:
        self.aufrufe += 1
        fig.clear()
        ax = fig.subplots()
        ax.plot([0.0, 100.0], [0.0, 1.0])
        ax.set_xlim(0.0, 100.0)
        achsen = getattr(opt, "achsen", None)  # wie die echten Zeichenfunktionen (R-073)
        if achsen is not None and achsen.frequenz.von is not None:
            ax.set_xlim(achsen.frequenz.von, achsen.frequenz.bis)
        self.groessen.append((fig.get_figwidth(), fig.get_figheight()))
        return Zeichnung(figure=fig, achsen=(ax,))


@dataclasses.dataclass(frozen=True)
class AttrappenOptionen:
    """Optionen der Attrappe: nur das Feld ``achsen`` wie bei den echten Zeichenfunktionen."""

    achsen: AchsenOptionen | None = None


def baue_plot(qtbot: QtBot, monkeypatch: pytest.MonkeyPatch) -> tuple[PlotFlaeche, Zeichner]:
    stil.wende_an(QApplication.instance())  # type: ignore[arg-type]
    zeichner = Zeichner()
    monkeypatch.setitem(plotflaeche.ZEICHNER, Ansicht.SPITZEN, zeichner)
    monkeypatch.setitem(plotflaeche.ZEICHNER, Ansicht.SPEKTRUM, zeichner)
    plot = PlotFlaeche(baue_plotstil())
    qtbot.addWidget(plot)
    plot.resize(700, 400)
    plot.show()
    qtbot.waitExposed(plot)
    return plot, zeichner


def test_groessenaenderung_zeichnet_spitzen_neu_und_erhaelt_zoom(
    qtbot: QtBot, monkeypatch: pytest.MonkeyPatch
) -> None:
    plot, zeichner = baue_plot(qtbot, monkeypatch)
    plot.zeichne(Ansicht.SPITZEN, None, AttrappenOptionen(), "Beschreibung")
    qtbot.wait(plotflaeche.NEUZEICHNEN_MS + 100)  # ggf. Resize vom Anzeigen abwarten
    start = zeichner.aufrufe
    plot.zeichnung.achsen[0].set_xlim(20.0, 40.0)  # type: ignore[union-attr]
    plot.toolbar.push_current()
    plot.resize(900, 520)
    qtbot.waitUntil(lambda: zeichner.aufrufe > start, timeout=3000)
    assert plot.zeichnung.achsen[0].get_xlim() == pytest.approx((20.0, 40.0))  # type: ignore[union-attr]
    assert plot.canvas.accessibleDescription() == "Beschreibung"
    plot.zoom_zuruecksetzen()  # Auto: zeichnet neu, der gemerkte Ausschnitt entfällt
    assert plot.zeichnung.achsen[0].get_xlim() == pytest.approx((0.0, 100.0))  # type: ignore[union-attr]


def test_groessenaenderung_ist_entprellt(qtbot: QtBot, monkeypatch: pytest.MonkeyPatch) -> None:
    plot, zeichner = baue_plot(qtbot, monkeypatch)
    plot.zeichne(Ansicht.SPITZEN, None, None)
    qtbot.wait(plotflaeche.NEUZEICHNEN_MS + 100)
    start = zeichner.aufrufe
    for breite in (720, 760, 800, 840, 880):
        plot.resize(breite, 400)
        qtbot.wait(10)
    assert zeichner.aufrufe == start  # noch nicht: Größe steht nicht still
    qtbot.waitUntil(lambda: zeichner.aufrufe > start, timeout=3000)
    qtbot.wait(plotflaeche.NEUZEICHNEN_MS + 100)
    assert zeichner.aufrufe == start + 1  # genau ein Neuzeichnen für die ganze Folge


def test_spektrum_wird_bei_groessenaenderung_nicht_neu_gezeichnet(
    qtbot: QtBot, monkeypatch: pytest.MonkeyPatch
) -> None:
    plot, zeichner = baue_plot(qtbot, monkeypatch)
    plot.zeichne(Ansicht.SPEKTRUM, None, None)
    start = zeichner.aufrufe
    plot.resize(900, 520)
    qtbot.wait(plotflaeche.NEUZEICHNEN_MS + 200)
    assert zeichner.aufrufe == start  # constrained-Layout zieht selbst nach (draw_idle)


def test_neuzeichnen_fehler_wird_gemeldet(qtbot: QtBot, monkeypatch: pytest.MonkeyPatch) -> None:
    plot, _zeichner = baue_plot(qtbot, monkeypatch)
    plot.zeichne(Ansicht.SPITZEN, None, None)
    qtbot.wait(plotflaeche.NEUZEICHNEN_MS + 100)

    def kaputt(*_a: object) -> None:
        raise ValueError("Neuzeichnen kaputt")

    monkeypatch.setitem(plotflaeche.ZEICHNER, Ansicht.SPITZEN, kaputt)
    with qtbot.waitSignal(plot.fehler, timeout=3000) as sig:
        plot.resize(1000, 600)
    assert sig.args == ["Neuzeichnen kaputt"]


def test_leere_stoppt_das_neuzeichnen(qtbot: QtBot, monkeypatch: pytest.MonkeyPatch) -> None:
    plot, zeichner = baue_plot(qtbot, monkeypatch)
    plot.zeichne(Ansicht.SPITZEN, None, None)
    qtbot.wait(plotflaeche.NEUZEICHNEN_MS + 100)
    start = zeichner.aufrufe
    plot.resize(1000, 600)
    plot.leere()
    qtbot.wait(plotflaeche.NEUZEICHNEN_MS + 200)
    assert zeichner.aufrufe == start
