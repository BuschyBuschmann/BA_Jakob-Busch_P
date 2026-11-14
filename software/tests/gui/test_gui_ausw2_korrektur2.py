"""Korrektur Runde 2 Etappe B (K2-AUSW2-B): Dialog-Überschneidung bei „Öffnen …“, Betragsfelder
je Größe (Ansicht 5, nebeneinander) und kompakte Anzeige bei kleinem Fenster; offscreen."""

from __future__ import annotations

import pytest
from gui_ausw_hilfen import Bauer, SteuerbarerAusfuehrer, synth_geladen
from PySide6.QtCore import QSize
from PySide6.QtGui import QResizeEvent
from PySide6.QtWidgets import QApplication, QBoxLayout

from ldv_automation.darstellung.achsen import Bereich
from ldv_automation.gui import anzeige_auswerten as aa
from ldv_automation.gui.achsen_zustand import AchsenZustand
from ldv_automation.gui.achsenleiste import Achsenleiste
from ldv_automation.gui.auswerten_reiter import KOMPAKT_BREITE_PX, AuswertenReiter
from ldv_automation.gui.messungen import MessungsZustand
from ldv_automation.gui.serien import baue_spec

pytestmark = pytest.mark.gui

A, B, C = "C:\\m\\a.svd", "C:\\m\\b.svd", "C:\\m\\c.svd"
PAAR = ("Vib X", "Ref1")


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


def lade_b_waehrend_dialog(
    a: AuswertenReiter, ausf: SteuerbarerAusfuehrer, zeugen: list[str | None]
) -> None:
    """Lässt B fertig werden, während die Ereignisschleife eines modalen Dialogs läuft."""
    frei(ausf, a, "lese_job", B)
    aktive = a.messungen.aktive
    zeugen.append(aktive.kurzname if aktive is not None else None)


def starte_mit_ladender_b(
    baue: Bauer,
) -> tuple[AuswertenReiter, SteuerbarerAusfuehrer]:
    """A aktiv (mit einer Serie in Ansicht 5), B lädt noch."""
    a, ausf = start(baue, A)
    a._serie_anlegen(baue_spec(a.messungen.alle[0].id, None, "spektrum", komponente="Z"))
    a.messung_hinzufuegen(B)
    assert a.messungen.alle[1].zustand is MessungsZustand.LADEN
    return a, ausf


# --- Dialog-Überschneidung -----------------------------------------------------------------


def test_zusatz_fertig_waehrend_ersetzen_rueckfrage_aendert_ziel_und_anzeige_nicht(
    baue: Bauer,
) -> None:
    a, ausf = starte_mit_ladender_b(baue)
    zeugen: list[str | None] = []

    def frage(titel: str, text: str) -> bool:
        lade_b_waehrend_dialog(a, ausf, zeugen)
        return True

    a._bestaetige_ersetzen = frage  # type: ignore[method-assign]
    a.oeffne_datei(C)  # A hat eine Serie: Rückfrage; B wird währenddessen fertig
    assert zeugen == ["A"]  # nicht aktiviert, solange der Dialog offen ist
    assert a.messungen.alle[1].zustand is MessungsZustand.BEREIT
    assert a.messungen.aktive is a.messungen.alle[0] and a.zustand is aa.AuswertenZustand.LADEN
    frei(ausf, a, "lese_job", C)
    assert [(m.kurzname, m.pfad) for m in a.messungen.alle] == [("A", C), ("B", B)]  # C ersetzt A
    # die zurückgestellte Zusatzmessung wird nach „Öffnen …“ aktiv; Anzeige und Meldung gehören
    # zu derselben Messung
    assert a.messungen.aktive is a.messungen.alle[1]
    assert a.lbl_datei.text() == "b.svd" and "Messung B aktiv" in a._meldung
    a.beende()


def test_rueckfrage_abgebrochen_holt_zurueckgestellte_aktivierung_nach(baue: Bauer) -> None:
    a, ausf = starte_mit_ladender_b(baue)
    zeugen: list[str | None] = []

    def frage(titel: str, text: str) -> bool:
        lade_b_waehrend_dialog(a, ausf, zeugen)
        return False

    a._bestaetige_ersetzen = frage  # type: ignore[method-assign]
    a.oeffne_datei(C)
    assert zeugen == ["A"]
    assert a.zustand is aa.AuswertenZustand.GELADEN
    assert [m.pfad for m in a.messungen.alle] == [A, B]  # nichts ersetzt
    assert a.messungen.aktive is a.messungen.alle[1]  # nachgeholt, nicht verloren
    assert a.lbl_datei.text() == "b.svd"
    a.beende()


def test_zusatz_fertig_waehrend_dateidialog_ersetzt_trotzdem_die_beim_klick_aktive(
    baue: Bauer,
) -> None:
    a, ausf = start(baue, A)  # keine Serie: keine Rückfrage, nur der Dateidialog
    a.messung_hinzufuegen(B)
    zeugen: list[str | None] = []

    def datei() -> str | None:
        lade_b_waehrend_dialog(a, ausf, zeugen)
        return C

    a._waehle_datei = datei  # type: ignore[method-assign]
    a._oeffnen_geklickt()
    assert zeugen == ["A"]
    frei(ausf, a, "lese_job", C)
    assert [(m.kurzname, m.pfad) for m in a.messungen.alle] == [("A", C), ("B", B)]
    assert a.messungen.aktive is a.messungen.alle[1] and a.lbl_datei.text() == "b.svd"
    a.beende()


def test_dateidialog_abgebrochen_holt_aktivierung_nach(baue: Bauer) -> None:
    a, ausf = start(baue, A)
    a.messung_hinzufuegen(B)
    zeugen: list[str | None] = []

    def datei() -> str | None:
        lade_b_waehrend_dialog(a, ausf, zeugen)
        return None

    a._waehle_datei = datei  # type: ignore[method-assign]
    a._oeffnen_geklickt()
    assert zeugen == ["A"]
    assert a.messungen.aktive is a.messungen.alle[1] and a.lbl_datei.text() == "b.svd"
    assert a.zustand is aa.AuswertenZustand.GELADEN
    a.beende()


def test_zusatz_ohne_dialog_wird_sofort_aktiv(baue: Bauer) -> None:
    a, ausf = start(baue, A)
    a.messung_hinzufuegen(B)
    frei(ausf, a, "lese_job", B)
    assert a.messungen.aktive is a.messungen.alle[1] and a._dialog_tiefe == 0
    a.beende()


def test_entferne_rueckfrage_stellt_aktivierung_zurueck(baue: Bauer) -> None:
    a, ausf = starte_mit_ladender_b(baue)
    zeugen: list[str | None] = []

    def frage(titel: str, text: str) -> bool:
        lade_b_waehrend_dialog(a, ausf, zeugen)
        return False

    a._bestaetige_entfernen = frage  # type: ignore[method-assign]
    a._entferne_geklickt(a.messungen.alle[0].id)
    assert zeugen == ["A"]  # während der Frage blieb A aktiv
    assert [m.kurzname for m in a.messungen.alle] == ["A", "B"]
    assert a.messungen.aktive is a.messungen.alle[1]  # danach nachgeholt
    a.beende()


# --- Betragsfelder je Größe ------------------------------------------------------------------


def zwei_groessen(baue: Bauer) -> AuswertenReiter:
    a, _ausf = start(baue, A)
    a.btn_ansicht[5].click()
    mid = a.messungen.alle[0].id
    a._serie_anlegen(baue_spec(mid, None, "spektrum", komponente="Z"))
    a._serie_anlegen(baue_spec(mid, None, "h1", kanalpaar=PAAR))
    return a


def setze(a: AuswertenReiter, seite: str, text: str) -> None:
    feld = a.achsenleiste.gruppe("betrag").feld(seite)
    feld.setText(text)
    feld.editingFinished.emit()


def test_auswahl_der_betragsgroesse_nur_nebeneinander_mit_mehreren_groessen(baue: Bauer) -> None:
    a = zwei_groessen(baue)
    cb = a.achsenleiste.gruppe("betrag").cb_groesse
    assert cb is not None
    assert cb.isHidden()  # überlagert: eine Größe
    assert a.auswahl_diagramm.groesse() == "spektrum"
    a.auswahl_diagramm.rb_anordnung_nebeneinander.click()
    assert not cb.isHidden()
    assert [cb.itemText(i) for i in range(cb.count())] == ["Spektrum", "|H1|"]
    assert cb.accessibleName() == "Größe der Betragsfelder" and cb.currentText() == "Spektrum"
    assert cb in a.achsenleiste.tab_kette()
    a.auswahl_diagramm.rb_anordnung_ueberlagert.click()
    assert cb.isHidden() and cb not in a.achsenleiste.tab_kette()
    a.beende()


def test_betragsfelder_zeigen_und_schreiben_bereich_und_skala_der_gewaehlten_groesse(
    baue: Bauer,
) -> None:
    a = zwei_groessen(baue)
    a.auswahl_diagramm.rb_anordnung_nebeneinander.click()
    z = a.plot.achsen_zustand
    gruppe = a.achsenleiste.gruppe("betrag")
    cb = gruppe.cb_groesse
    assert cb is not None
    setze(a, "von", "1e-6")
    setze(a, "bis", "1e-3")
    assert z.bereich(5, "spektrum") == Bereich(1e-6, 1e-3) and z.bereich(5, "h1").ist_auto
    # Auswahl |H1|: die Felder gehören nun zu |H1| (Auto), Skala-Umschalter ebenso
    cb.setCurrentIndex(1)
    cb.activated.emit(1)
    assert z.groesse_5 == "h1"
    assert gruppe.ed_von.text() == "" and gruppe.ed_bis.text() == ""
    setze(a, "von", "0.5")
    setze(a, "bis", "50")
    assert z.bereich(5, "h1") == Bereich(0.5, 50.0)
    assert z.bereich(5, "spektrum") == Bereich(1e-6, 1e-3)  # unberührt
    assert gruppe.rb_log is not None and gruppe.rb_linear is not None
    gruppe.rb_linear.setChecked(True)
    assert z.skala(5, "h1") == "linear" and z.skala(5, "spektrum") == "log"
    # zurück zum Spektrum: Bereich und Skala kommen wieder, die Einheit der Größe steht dabei
    cb.setCurrentIndex(0)
    cb.activated.emit(0)
    assert z.groesse_5 == "spektrum"
    assert gruppe.ed_von.text() != "" and z.bereich(5, "spektrum") == Bereich(1e-6, 1e-3)
    assert gruppe.rb_log.isChecked()
    # die Zeichnung trägt je Teilbild den Bereich seiner Größe
    assert a.plot.zeichnung is not None
    ylim = {
        r: ax.get_ylim()
        for r, ax in zip(a.plot.zeichnung.rollen, a.plot.zeichnung.achsen, strict=True)
    }
    assert ylim["spektrum"] == pytest.approx((1e-6, 1e-3), rel=1e-9)
    assert ylim["h1"] == pytest.approx((0.5, 50.0), rel=1e-9)
    a.beende()


def test_groessenwechsel_verwirft_halbe_eingabe_und_meldung(baue: Bauer) -> None:
    a = zwei_groessen(baue)
    a.auswahl_diagramm.rb_anordnung_nebeneinander.click()
    gruppe = a.achsenleiste.gruppe("betrag")
    cb = gruppe.cb_groesse
    assert cb is not None
    setze(a, "von", "abc")  # ungültig: Meldung bleibt stehen
    assert a.achsenleiste.fehler_aktiv("betrag", "von")
    cb.setCurrentIndex(1)
    cb.activated.emit(1)
    assert not a.achsenleiste.fehler_aktiv("betrag", "von")
    assert gruppe.ed_von.text() == ""
    assert a.plot.achsen_zustand.bereich(5, "spektrum").ist_auto
    a.beende()


# --- Kleines Fenster ---------------------------------------------------------------------------


def groesse_melden(a: AuswertenReiter, breite: int) -> None:
    QApplication.sendEvent(a, QResizeEvent(QSize(breite, 680), QSize(1366, 768)))
    QApplication.processEvents()  # Layouts übernehmen die neuen Größenhinweise


def test_kompakt_unter_1200_px_blendet_namen_aus_und_kuerzt_beschriftungen(baue: Bauer) -> None:
    a, _ = start(baue, A)
    assert KOMPAKT_BREITE_PX == 1200
    leiste = a.achsenleiste
    gruppe = leiste.gruppe("betrag")
    groesse_melden(a, 1100)
    assert a._namen_box.isHidden()
    assert gruppe.rb_log is not None and gruppe.rb_linear is not None
    assert (gruppe.rb_linear.text(), gruppe.rb_log.text()) == ("lin", "log")
    assert leiste.btn_auto.text() == "Auto"
    # vollständige Namen bleiben für Hilfsmittel und Tooltip
    assert gruppe.rb_log.accessibleName() == "Skala Betrag logarithmisch"
    assert gruppe.rb_log.toolTip() == "logarithmisch"
    assert leiste.btn_auto.accessibleName() == "Alle Achsen auf Auto"
    groesse_melden(a, 1366)
    assert not a._namen_box.isHidden()
    assert (gruppe.rb_linear.text(), gruppe.rb_log.text()) == ("linear", "logarithmisch")
    assert leiste.btn_auto.text() == "Alles auf Auto" and gruppe.rb_log.toolTip() == ""
    a.beende()


def test_kompakte_achsenleiste_braucht_bei_804_px_eine_zeile(qtbot) -> None:  # type: ignore[no-untyped-def]
    leiste = Achsenleiste(AchsenZustand())
    qtbot.addWidget(leiste)
    leiste.setze_ansicht(5)
    leiste.aktualisiere(
        {"frequenz": (0.625, 1000.0), "betrag": (2.4e-8, 9.3e-4)},
        {"frequenz": "Hz", "betrag": "m/s"},
    )
    leiste.show()
    layout = leiste.layout()
    assert layout is not None
    hoch = layout.heightForWidth(804)
    leiste.setze_kompakt(True)
    QApplication.processEvents()
    flach = layout.heightForWidth(804)
    assert flach < hoch  # Frequenz, Betrag und „Auto“ in einer Zeile
    zeile = leiste.gruppe("betrag").sizeHint().height() + 4  # mit reservierter Meldezeile
    assert flach <= zeile + 2


def test_kompakt_hinweis_serien_voll_nur_im_tooltip_anordnung_nebeneinander(baue: Bauer) -> None:
    a, _ = start(baue, A)
    sel = a.auswahl_diagramm
    sel.setze_voll(True)
    assert not sel.lbl_voll.isHidden()
    groesse_melden(a, 1100)
    assert sel.lbl_voll.isHidden() and sel.btn_serie_neu.toolTip() != ""
    assert sel._anordnung_zeile.direction() == QBoxLayout.Direction.LeftToRight
    sel.setze_voll(True)  # bleibt ausgeblendet
    assert sel.lbl_voll.isHidden()
    groesse_melden(a, 1366)
    assert not sel.lbl_voll.isHidden()
    assert sel._anordnung_zeile.direction() == QBoxLayout.Direction.TopToBottom
    a.beende()
