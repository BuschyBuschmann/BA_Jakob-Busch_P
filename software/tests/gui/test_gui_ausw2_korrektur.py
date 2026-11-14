"""Korrekturen Etappe B (K-AUSW2-B): Entfernen während „Öffnen …“, y-Bereiche je Größe,
Kreuz am Chip, Dialogtexte, Reihenfolge der Chips, Anzeigefehler, Serienknöpfe; offscreen."""

from __future__ import annotations

import pytest
from gui_ausw_hilfen import Bauer, SteuerbarerAusfuehrer, synth_geladen
from PySide6.QtCore import QTimer
from PySide6.QtWidgets import QApplication, QMessageBox

from ldv_automation.darstellung.achsen import Bereich
from ldv_automation.gui import anzeige_auswerten as aa
from ldv_automation.gui.achsen_zustand import AchsenZustand
from ldv_automation.gui.auswahl_diagramm import SerienDialog
from ldv_automation.gui.auswerten_reiter import AuswertenReiter
from ldv_automation.gui.messungen import MessungsZustand
from ldv_automation.gui.serien import baue_spec
from ldv_automation.gui.stil import QSS

pytestmark = pytest.mark.gui

A, B, C = "C:\\m\\a.svd", "C:\\m\\b.svd", "C:\\m\\c.svd"


def start(baue: Bauer, *dateien: str) -> tuple[AuswertenReiter, SteuerbarerAusfuehrer]:
    ausf = SteuerbarerAusfuehrer()
    w, prot = baue(ausf)
    a = w.auswerten
    assert a is not None
    for d in dateien:
        prot.geladen[d] = synth_geladen(pfad=d)
    a.oeffne_datei(dateien[0])
    ausf.auftraege[0].freigegeben = True
    a._abfrage()
    for d in dateien[1:]:
        n = len(ausf.auftraege)
        a.messung_hinzufuegen(d)
        ausf.auftraege[n].freigegeben = True
        a._abfrage()
    return a, ausf


def frei(ausf: SteuerbarerAusfuehrer, a: AuswertenReiter, art: str, datei: str) -> None:
    nr = next(
        i
        for i, x in enumerate(ausf.auftraege)
        if x.funktion.__name__ == art and x.argumente[0] == datei and not x.freigegeben
    )
    ausf.auftraege[nr].freigegeben = True
    a._abfrage()


def test_entfernen_waehrend_oeffnen_sperrt_die_zielmessung(baue: Bauer) -> None:
    a, ausf = start(baue, A, B)
    ziel_a = a.messungen.alle[0]
    a._aktiviere_messung(ziel_a.id)
    a.oeffne_datei(C)  # ersetzt A
    assert a.zustand is aa.AuswertenZustand.LADEN
    knopf = a.messungsleiste.chip(ziel_a.id).entfernen  # type: ignore[union-attr]
    anderer = a.messungsleiste.chip(a.messungen.alle[1].id).entfernen  # type: ignore[union-attr]
    assert not knopf.isEnabled() and anderer.isEnabled()
    a._entferne_geklickt(ziel_a.id)
    a.entferne_messung(ziel_a.id)
    assert [m.kurzname for m in a.messungen.alle] == ["A", "B"]
    frei(ausf, a, "lese_job", C)
    pfade = [(m.kurzname, m.pfad) for m in a.messungen.alle]
    assert pfade == [("A", C), ("B", B)]  # C ersetzt A, nicht B
    a.beende()


def test_entfernen_einer_anderen_messung_waehrend_oeffnen_aendert_das_ziel_nicht(
    baue: Bauer,
) -> None:
    a, ausf = start(baue, A, B)
    a._aktiviere_messung(a.messungen.alle[0].id)
    ausf_b = [x for x in ausf.auftraege if x.funktion.__name__ == "pruef_job" and not x.abgebrochen]
    a.oeffne_datei(C)
    assert all(x.abgebrochen for x in ausf_b)  # Öffnen bricht die laufende Stufe B ab
    a.entferne_messung(a.messungen.alle[1].id)  # B entfernen: erlaubt
    frei(ausf, a, "lese_job", C)
    assert [(m.kurzname, m.pfad) for m in a.messungen.alle] == [("A", C)]
    a.beende()


def test_stufe_b_wird_nie_verwaist_ueberschrieben(baue: Bauer) -> None:
    a, ausf = start(baue, A)
    laufend = [x for x in ausf.auftraege if x.funktion.__name__ == "pruef_job"]
    assert len(laufend) == 1 and not laufend[0].abgebrochen
    a._b_messung = -1  # anderer Besitzer: der neue Start muss den alten beenden
    a._starte_pruefung(a._job_id)
    assert laufend[0].abgebrochen
    a.beende()


def test_einzige_messung_im_zustand_laden_ist_nicht_entfernbar_zustand_bleibt_sauber(
    baue: Bauer,
) -> None:
    a, _ausf = start(baue, A)
    a.oeffne_datei(B)
    m = a.messungen.alle[0]
    a.entferne_messung(m.id)
    assert len(a.messungen) == 1 and a.zustand is aa.AuswertenZustand.LADEN and a.laeuft()
    assert a.lbl_pfad is not None
    a.beende()


def test_zusatz_fertig_waehrend_oeffnen_wird_danach_aktiv(baue: Bauer) -> None:
    a, ausf = start(baue, A)
    a.messung_hinzufuegen(B)
    a.oeffne_datei(C)  # ersetzt A, während B noch lädt
    ausf.auftraege[2].freigegeben = True  # B fertig (Öffnen läuft)
    a._abfrage()
    b = a.messungen.alle[1]
    assert b.zustand is MessungsZustand.BEREIT
    assert "lädt" not in a.messungsleiste.chip_knopf(b.id).text()  # type: ignore[union-attr]
    frei(ausf, a, "lese_job", C)
    assert a.messungen.aktive is b and a.zustand is aa.AuswertenZustand.GELADEN
    assert a.lbl_datei.text() == "b.svd"
    a.beende()


def test_chipreihenfolge_folgt_der_anzeige_nach_oeffnen(baue: Bauer) -> None:
    a, ausf = start(baue, A, B)
    a._aktiviere_messung(a.messungen.alle[0].id)
    a.oeffne_datei(C)
    frei(ausf, a, "lese_job", C)
    modell = [m.id for m in a.messungen.alle]
    assert a.messungsleiste.chip_ids() == modell
    kette = [w.objectName() for w in a.messungsleiste.tab_kette()]
    assert kette[0] == f"btn_chip_{modell[0]}" and kette[2] == f"btn_chip_{modell[1]}"
    a.beende()


def test_anzeigefehler_verwirft_nur_die_betroffene_messung(
    baue: Bauer, monkeypatch: pytest.MonkeyPatch
) -> None:
    a, _ausf = start(baue, A, B)
    aktiv_b = a.messungen.aktive
    assert aktiv_b is not None and len(a.messungen) == 2
    original = a.liste_punkte.addItems
    zaehler = {"n": 0}

    def einmal_kaputt(eintraege: list[str]) -> None:
        zaehler["n"] += 1
        if zaehler["n"] == 1:
            raise RuntimeError("Anzeige kaputt")
        original(eintraege)

    monkeypatch.setattr(a.liste_punkte, "addItems", einmal_kaputt)
    a._aktiviere_messung(a.messungen.alle[0].id)  # Wechsel zu A scheitert
    assert [m.kurzname for m in a.messungen.alle] == ["B"]
    assert a.messungen.aktive is not None and a.zustand is aa.AuswertenZustand.GELADEN
    assert a.fehlertext is not None and "Anzeige kaputt" in a.fehlertext
    a.beende()


def _klicke_knopf(text: str, gesehen: list[str]) -> None:
    for w in QApplication.topLevelWidgets():
        if isinstance(w, QMessageBox) and w.isVisible():
            gesehen.extend(sorted(b.text() for b in w.buttons()))
            next(b for b in w.buttons() if b.text() == text).click()


def test_rueckfrage_beim_oeffnen_wenn_serien_der_ersetzten_messung_entfallen(
    baue: Bauer, monkeypatch: pytest.MonkeyPatch
) -> None:
    a, ausf = start(baue, A, B)
    ersetzt = a.messungen.alle[1]
    a._serien.hinzufuegen(baue_spec(ersetzt.id, None, "spektrum", komponente="Z"))
    gesehen: list[str] = []
    QTimer.singleShot(50, lambda: _klicke_knopf("Abbrechen", gesehen))
    a.oeffne_datei(C)
    assert gesehen == ["Abbrechen", "Ersetzen"]  # deutsche Knöpfe
    assert a.zustand is aa.AuswertenZustand.GELADEN and not any(
        x.argumente[0] == C for x in ausf.auftraege
    )
    QTimer.singleShot(50, lambda: _klicke_knopf("Ersetzen", gesehen))
    a.oeffne_datei(C)
    assert a.zustand.name == "LADEN"
    a.beende()


def test_entfernen_dialog_hat_deutsche_knoepfe(baue: Bauer) -> None:
    a, _ = start(baue, A, B)
    m = a.messungen.alle[1]
    a._serien.hinzufuegen(baue_spec(m.id, None, "spektrum", komponente="Z"))
    gesehen: list[str] = []
    QTimer.singleShot(50, lambda: _klicke_knopf("Entfernen", gesehen))
    a._entferne_geklickt(m.id)
    assert gesehen == ["Abbrechen", "Entfernen"] and len(a.messungen) == 1
    a.beende()


def test_serien_dialog_hat_deutsche_knoepfe() -> None:
    import inspect

    quelle = inspect.getsource(SerienDialog.__init__)
    assert '"Übernehmen"' in quelle and '"Abbrechen"' in quelle


def test_kreuz_am_chip_ist_gross_genug_und_gezeichnet(baue: Bauer) -> None:
    a, _ = start(baue, A, B)
    app = QApplication.instance()
    assert isinstance(app, QApplication)
    altes_qss = app.styleSheet()
    app.setStyleSheet(QSS)  # die Regel für das Kreuz steht in der Anwendungs-QSS
    a.window().show()
    QApplication.processEvents()
    chip = a.messungsleiste.chip(a.messungen.alle[0].id)
    assert chip is not None
    kreuz = chip.entfernen  # type: ignore[attr-defined]
    assert kreuz.height() <= chip.height() and kreuz.width() >= 14 and kreuz.height() >= 14
    bild = kreuz.grab().toImage()
    leer = bild.pixel(0, 0)
    dunkel = sum(
        1 for x in range(bild.width()) for y in range(bild.height()) if bild.pixel(x, y) != leer
    )
    app.setStyleSheet(altes_qss)
    assert dunkel >= 8  # ein sichtbares Kreuz, kein leeres Kästchen
    a.beende()


def test_serienknoepfe_bei_vier_serien_und_kleinem_fenster_sichtbar(baue: Bauer) -> None:
    a, _ = start(baue, A, B)
    w = a.window()
    w.resize(1100, 680)
    w.show()
    a.btn_ansicht[5].click()
    for i in range(2):
        for kanal in ("X", "Z"):
            a._serie_anlegen(baue_spec(a.messungen.alle[i].id, None, "spektrum", komponente=kanal))
    a.auswahl_diagramm.rb_anordnung_nebeneinander.click()
    QApplication.processEvents()
    sel = a.auswahl_diagramm
    sichtbar = a._ad_stapel.mapToGlobal(a._ad_stapel.rect().topLeft()).y()
    unten = sichtbar + a._ad_stapel.height()
    for k in (sel.btn_serie_neu, sel.btn_serie_entfernen, sel.btn_serie_alle):
        y = k.mapToGlobal(k.rect().bottomLeft()).y()
        assert y <= unten, k.objectName()
    assert "Spektrum" not in sel.liste_serien.item(0).text()  # Größe steht nicht doppelt
    a.beende()


def test_betragsbereiche_ansicht_5_je_groesse() -> None:
    z = AchsenZustand()
    z.setze_groesse_5("spektrum")
    z.setze_bereich(5, "betrag", Bereich(1e-6, 1e-3))
    z.setze_skala(5, "betrag", "linear")
    z.setze_groesse_5("h1")
    assert z.bereich(5, "betrag").ist_auto and z.skala(5, "betrag") == "log"
    z.uebernehme_grenzen(5, "betrag", 2.0, 8.0)
    assert z.bereich(5, "h1") == Bereich(2.0, 8.0) and z.bereich(5, "spektrum") == Bereich(
        1e-6, 1e-3
    )
    z.setze_groesse_5("spektrum")  # Rückwechsel stellt wieder her
    assert z.bereich(5, "betrag") == Bereich(1e-6, 1e-3) and z.skala(5, "betrag") == "linear"
    opt = z.optionen(5)
    assert opt.y_bereich("h1") == Bereich(2.0, 8.0) and opt.y_bereich("spektrum").von == 1e-6
    z.auf_auto(5)
    assert z.bereich(5, "h1").ist_auto
    with pytest.raises(ValueError, match="Betragsgröße"):
        z.setze_groesse_5("phase")


def test_groessenwechsel_und_zoom_schreiben_in_den_bereich_der_richtigen_groesse(
    baue: Bauer,
) -> None:
    a, _ = start(baue, A)
    a.btn_ansicht[5].click()
    sel = a.auswahl_diagramm
    z = a.plot.achsen_zustand
    a._serie_anlegen(baue_spec(a.messungen.alle[0].id, None, "spektrum", komponente="Z"))
    a._zeichne()
    gruppe = a.achsenleiste.gruppe("betrag")
    gruppe.ed_von.setText("1e-6")
    gruppe.ed_von.editingFinished.emit()
    gruppe.ed_bis.setText("1e-3")
    gruppe.ed_bis.editingFinished.emit()
    assert z.bereich(5, "spektrum") == Bereich(1e-6, 1e-3)
    sel.rb_groesse["h1"].setChecked(True)
    assert z.groesse_5 == "h1" and z.bereich(5, "h1").ist_auto
    assert a.plot.zeichnung is not None
    ax = a.plot.zeichnung.achsen[0]
    ax.set_ylim(0.5, 50.0)  # Zoom der Werkzeugleiste
    a.plot._werkzeug_hat_geaendert()
    assert z.bereich(5, "h1").von == pytest.approx(0.5)
    assert z.bereich(5, "spektrum") == Bereich(1e-6, 1e-3)  # unberührt
    sel.rb_groesse["spektrum"].setChecked(True)
    assert a.plot.zeichnung is not None
    assert a.plot.zeichnung.achsen[0].get_ylim() == pytest.approx((1e-6, 1e-3), rel=1e-9)
    a.beende()
