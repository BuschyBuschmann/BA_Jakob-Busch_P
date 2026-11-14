"""Mehrere Messungen im Reiter „Auswerten“ (R-058, P-AUSW2 S4/S5; UI-3, UI-9, UI-14); offscreen.

Aufträge laufen über ``SteuerbarerAusfuehrer`` (der Test bestimmt, wann ein Auftrag fertig wird),
Daten über ``gui_ausw_hilfen.Protokoll`` (synthetische Dateien, Lesefehler wählbar).
"""

from __future__ import annotations

import pytest
from gui_ausw_hilfen import (
    Bauer,
    DirektAusfuehrer,
    NieFertigAusfuehrer,
    Protokoll,
    SteuerbarerAusfuehrer,
)
from PySide6.QtCore import Qt
from PySide6.QtTest import QTest
from PySide6.QtWidgets import QAbstractButton, QApplication, QWidget

from ldv_automation.darstellung.achsen import Bereich
from ldv_automation.gui import anzeige_auswerten as aa
from ldv_automation.gui.auswerten_reiter import (
    TEXT_HINZU_ERST_DATEI,
    TEXT_HINZU_LAEDT,
    TEXT_HINZU_VOLL,
    AuswertenReiter,
)
from ldv_automation.gui.hauptfenster import Hauptfenster
from ldv_automation.gui.messungen import MESSUNGEN_MAX, MessungsZustand

pytestmark = pytest.mark.gui

DATEI_A = "C:\\messungen\\a.svd"
DATEI_B = "C:\\messungen\\b.svd"
DATEI_C = "C:\\messungen\\c.svd"


def reiter(
    baue: Bauer, ausfuehrer: object | None = None
) -> tuple[AuswertenReiter, Protokoll, Hauptfenster]:
    w, prot = baue(ausfuehrer)
    a = w.auswerten
    assert a is not None
    return a, prot, w


def fertig(ausf: SteuerbarerAusfuehrer, nummer: int, a: AuswertenReiter) -> None:
    """Gibt Auftrag ``nummer`` frei und lässt den Reiter abfragen."""
    ausf.auftraege[nummer].freigegeben = True
    a._abfrage()


def zwei_messungen(baue: Bauer) -> tuple[AuswertenReiter, Protokoll, SteuerbarerAusfuehrer]:
    ausf = SteuerbarerAusfuehrer()
    a, prot, _ = reiter(baue, ausf)
    a.oeffne_datei(DATEI_A)
    fertig(ausf, 0, a)  # lese A; danach pruef A (Auftrag 1)
    a.messung_hinzufuegen(DATEI_B)  # lese B (Auftrag 2)
    fertig(ausf, 2, a)
    return a, prot, ausf


# --- S4: eine Messung, Verhalten unverändert ---------------------------------------------


def test_eine_messung_ein_chip_aktiv_kurzname_a(baue: Bauer) -> None:
    a, _, _ = reiter(baue)
    assert a.messungen.aktive is None and not a.messungsleiste.isVisibleTo(a)
    a.oeffne_datei(DATEI_A)
    a._abfrage()
    m = a.messungen.aktive
    assert m is not None and m.kurzname == "A" and m.pfad == DATEI_A
    assert a.geladen is m.geladen and a._cache is m.cache  # Eigenschaften delegieren
    assert a.messungsleiste.chip_ids() == [m.id]
    knopf = a.messungsleiste.chip_knopf(m.id)
    assert knopf is not None and knopf.text().startswith("✔ (A) a.svd")
    assert "aktiv" in knopf.accessibleName()
    assert a.messungsleiste.chip(m.id).property("aktiv") == "true"


def test_oeffnen_ersetzt_die_aktive_messung_kurzname_bleibt(baue: Bauer) -> None:
    a, _, _ = reiter(baue)
    a.oeffne_datei(DATEI_A)
    a._abfrage()
    erste = a.messungen.aktive
    assert erste is not None
    a.messungen.umbenennen(erste.id, "Referenz")
    a.oeffne_datei(DATEI_B)
    a._abfrage()
    zweite = a.messungen.aktive
    assert zweite is not None and zweite.id != erste.id
    assert zweite.kurzname == "Referenz" and len(a.messungen) == 1 and zweite.pfad == DATEI_B
    assert a.lbl_datei.text() == "b.svd"


# --- S5: weitere Messungen ------------------------------------------------------------------------


def test_hinzufuegen_zweiter_chip_eindeutige_kurznamen_wird_aktiv(baue: Bauer) -> None:
    a, _, _ = zwei_messungen(baue)
    namen = [m.kurzname for m in a.messungen.alle]
    assert namen == ["A", "B"] and len(set(namen)) == 2  # UI-9
    assert a.messungen.aktive is a.messungen.alle[1] and a.lbl_datei.text() == "b.svd"
    assert len(a.messungsleiste.chip_ids()) == 2


def test_oberflaeche_bleibt_waehrend_des_ladens_bedienbar(baue: Bauer) -> None:
    ausf = SteuerbarerAusfuehrer()
    a, _, w = reiter(baue, ausf)
    a.oeffne_datei(DATEI_A)
    fertig(ausf, 0, a)
    a.messung_hinzufuegen(DATEI_B)  # Auftrag 2 wird nie fertig
    b = a.messungen.alle[1]
    assert b.zustand is MessungsZustand.LADEN and a.zustand is aa.AuswertenZustand.GELADEN
    knopf = a.messungsleiste.chip_knopf(b.id)
    assert knopf is not None and "lädt …" in knopf.text() and not knopf.isEnabled()
    assert (
        not a.messungsleiste.chip(b.id)
        .findChild(  # type: ignore[union-attr]
            QWidget, f"balken_chip_{b.id}"
        )
        .isHidden()
    )
    w.reiter.setCurrentIndex(0)  # Klick auf einen anderen Reiter wird verarbeitet (UI-9)
    QApplication.processEvents()
    assert w.reiter.currentIndex() == 0
    w.reiter.setCurrentIndex(1)
    a.btn_ansicht[2].click()
    assert a.ansicht == 2 and a.laeuft()
    assert a.plot.zeichnung is not None  # A bleibt bedienbar
    assert a.btn_messung_hinzu.isEnabled() is True  # weitere dürfen warten
    a.beende()
    assert ausf.auftraege[2].abgebrochen


def test_hoechstens_ein_ladeauftrag_gleichzeitig(baue: Bauer) -> None:
    ausf = SteuerbarerAusfuehrer()
    a, prot, _ = reiter(baue, ausf)
    a.oeffne_datei(DATEI_A)
    fertig(ausf, 0, a)
    a.messung_hinzufuegen(DATEI_B)
    a.messung_hinzufuegen(DATEI_C)
    lese_args = [x.argumente for x in ausf.auftraege if x.funktion == prot.lese_job]
    assert lese_args == [(DATEI_A,), (DATEI_B,)]  # C wartet
    fertig(ausf, 2, a)  # B fertig: C startet
    lese_args = [x.argumente for x in ausf.auftraege if x.funktion == prot.lese_job]
    assert lese_args == [(DATEI_A,), (DATEI_B,), (DATEI_C,)]
    c = a.messungen.alle[2]
    assert c.zustand is MessungsZustand.LADEN and c.gestartet
    a.beende()


def test_stufe_b_nur_fuer_die_aktive_messung_wechsel_bricht_ab(baue: Bauer) -> None:
    ausf = SteuerbarerAusfuehrer()
    a, prot, _ = reiter(baue, ausf)
    a.oeffne_datei(DATEI_A)
    fertig(ausf, 0, a)
    pruef_a = ausf.auftraege[1]
    assert pruef_a.funktion == prot.pruef_job and pruef_a.argumente[0] == DATEI_A
    a.messung_hinzufuegen(DATEI_B)
    fertig(ausf, 2, a)  # B wird aktiv
    assert pruef_a.abgebrochen  # höchstens ein B-Auftrag, der alte wird verworfen
    pruef_b = ausf.auftraege[3]
    assert pruef_b.argumente[0] == DATEI_B and not pruef_b.abgebrochen
    fertig(ausf, 3, a)
    assert a.pruefung is not None and a.messungen.alle[1].pruefung is a.pruefung
    assert a.messungen.alle[0].pruefung is None  # A wurde nie geprüft
    a._aktiviere_messung(a.messungen.alle[0].id)  # Rückwechsel startet B für A neu
    assert ausf.auftraege[4].argumente[0] == DATEI_A
    a.beende()


def test_ergebnis_von_stufe_b_gehoert_der_gestarteten_messung(baue: Bauer) -> None:
    ausf = SteuerbarerAusfuehrer()
    a, _, _ = reiter(baue, ausf)
    a.oeffne_datei(DATEI_A)
    fertig(ausf, 0, a)
    ausf.auftraege[1].freigegeben = True  # Prüfung A ist fertig, aber noch nicht abgefragt
    m_a = a.messungen.aktive
    assert m_a is not None
    a._ergebnis_b(ausf.auftraege[1])
    assert m_a.pruefung is not None
    a.beende()


def test_wechsel_der_aktiven_messung_aendert_achsen_nicht(baue: Bauer) -> None:
    a, _, _ = zwei_messungen(baue)
    zustand = a.plot.achsen_zustand
    zustand.setze_bereich(1, "frequenz", Bereich(4.0, 12.0))
    zustand.setze_skala(1, "betrag", "linear")
    a._zeichne()
    vorher = (a.plot.zeichnung.achsen[0].get_xlim(), a.plot.zeichnung.achsen[0].get_yscale())  # type: ignore[union-attr]
    erste = a.messungen.alle[0]
    a.messungsleiste.chip_knopf(erste.id).click()  # type: ignore[union-attr]
    assert a.messungen.aktive is erste and a.lbl_datei.text() == "a.svd"
    assert a.ansicht == 1
    achse = a.plot.zeichnung.achsen[0]  # type: ignore[union-attr]
    assert (achse.get_xlim(), achse.get_yscale()) == vorher  # UI-3
    assert zustand.bereich(1, "frequenz") == Bereich(4.0, 12.0)
    assert a.plot.zeichnung is not None and a.zustand is aa.AuswertenZustand.GELADEN


def test_wechsel_behaelt_die_gewaehlte_ansicht_und_setzt_die_auswahl_zurueck(
    baue: Bauer,
) -> None:
    a, _, _ = zwei_messungen(baue)
    a.btn_ansicht[2].click()
    a.liste_punkte.setCurrentRow(3)
    a._aktiviere_messung(a.messungen.alle[0].id)
    assert a.ansicht == 2 and a.btn_ansicht[2].isChecked()
    assert a.liste_punkte.currentRow() == 0  # Auswahl wie bei einer neuen Datei zurück


def test_ladefehler_der_zweiten_datei_laesst_bisherige_messungen_unveraendert(
    baue: Bauer,
) -> None:
    a, prot, _ = reiter(baue, DirektAusfuehrer())
    prot.fehler_lese[DATEI_B] = "kaputt"
    a.oeffne_datei(DATEI_A)
    a._abfrage()
    erste = a.messungen.aktive
    assert erste is not None
    a.messung_hinzufuegen(DATEI_B)
    a._abfrage()
    assert a.messungen.alle == (erste,) and a.messungen.aktive is erste
    assert a.fehlertext is not None and "kaputt" in a.fehlertext
    assert a.band_fehler.isVisibleTo(a) and a.zustand is aa.AuswertenZustand.GELADEN
    assert a.plot.zeichnung is not None and not a.laeuft()
    assert a.messungsleiste.chip_ids() == [erste.id]


def test_aufbereitung_der_zweiten_datei_scheitert_als_lesefehler(
    baue: Bauer, monkeypatch: pytest.MonkeyPatch
) -> None:
    a, _, _ = reiter(baue, DirektAusfuehrer())
    a.oeffne_datei(DATEI_A)
    a._abfrage()
    original = AuswertenReiter._bereite_auf

    def kaputt(geladen: object) -> object:
        raise ValueError("Cache nicht aufbaubar")

    monkeypatch.setattr(AuswertenReiter, "_bereite_auf", staticmethod(kaputt))
    a.messung_hinzufuegen(DATEI_B)
    a._abfrage()
    monkeypatch.setattr(AuswertenReiter, "_bereite_auf", original)
    assert len(a.messungen) == 1 and a.fehlertext is not None
    assert "Auswertung nicht möglich" in a.fehlertext


def test_prozess_nicht_startbar_ist_ein_fehlerband_ohne_haengendes_laden(baue: Bauer) -> None:
    class Kaputt(SteuerbarerAusfuehrer):
        def starte(self, funktion, *argumente):  # type: ignore[no-untyped-def]
            if argumente and argumente[0] == DATEI_B:
                raise OSError("Spawn nicht möglich")
            return super().starte(funktion, *argumente)

    ausf = Kaputt()
    a, _, _ = reiter(baue, ausf)
    a.oeffne_datei(DATEI_A)
    fertig(ausf, 0, a)
    a.messung_hinzufuegen(DATEI_B)
    assert len(a.messungen) == 1 and a.fehlertext is not None and "Spawn" in a.fehlertext
    a.beende()


def test_hinzufuegen_knopf_zustaende_und_grenze(baue: Bauer) -> None:
    ausf = SteuerbarerAusfuehrer()
    a, _, _ = reiter(baue, ausf)
    assert not a.btn_messung_hinzu.isEnabled()
    assert a.btn_messung_hinzu.toolTip() == TEXT_HINZU_ERST_DATEI
    a.oeffne_datei(DATEI_A)
    assert not a.btn_messung_hinzu.isEnabled()
    assert a.btn_messung_hinzu.toolTip() == TEXT_HINZU_LAEDT
    a.messung_hinzufuegen(DATEI_B)  # wirkungslos: noch nichts geladen
    assert len(a.messungen) == 0
    fertig(ausf, 0, a)
    assert a.btn_messung_hinzu.isEnabled()
    for i in range(MESSUNGEN_MAX - 1):
        a.messung_hinzufuegen(f"C:\\m\\{i}.svd")
        fertig(ausf, len(ausf.auftraege) - 1 if i else 2, a)
    assert a.messungen.ist_voll and not a.btn_messung_hinzu.isEnabled()
    assert a.btn_messung_hinzu.toolTip() == TEXT_HINZU_VOLL
    a.messung_hinzufuegen("C:\\zu\\viel.svd")
    assert len(a.messungen) == MESSUNGEN_MAX
    a.beende()


def test_dieselbe_datei_zweimal_mit_hinweis(baue: Bauer) -> None:
    ausf = SteuerbarerAusfuehrer()
    a, _, _ = reiter(baue, ausf)
    a.oeffne_datei(DATEI_A)
    fertig(ausf, 0, a)
    a.messung_hinzufuegen(DATEI_A)
    fertig(ausf, 2, a)
    assert [m.kurzname for m in a.messungen.alle] == ["A", "B"]
    assert "Dieselbe Datei wie A." in a.lbl_cursor.volltext()
    a.beende()


def test_entfernen_aktive_rueckt_auf_vorige_und_letzte_gibt_keine_datei(baue: Bauer) -> None:
    a, _, _ = zwei_messungen(baue)
    erste, zweite = a.messungen.alle
    assert a.messungen.aktive is zweite
    chip = a.messungsleiste.chip(zweite.id)
    assert chip is not None
    entfernen = chip.findChild(QWidget, f"btn_chip_entfernen_{zweite.id}")
    assert isinstance(entfernen, QAbstractButton)
    entfernen.click()
    assert a.messungen.alle == (erste,) and a.messungen.aktive is erste
    assert a.lbl_datei.text() == "a.svd" and a.zustand is aa.AuswertenZustand.GELADEN
    a.entferne_messung(erste.id)
    assert len(a.messungen) == 0 and a.zustand.name == "KEINE_DATEI"
    assert a.geladen is None and not a.messungsleiste.isVisibleTo(a)
    assert a.lbl_datei.text() == "–" and not a.laeuft()


def test_entfernen_einer_ladenden_messung_bricht_ihren_auftrag_ab(baue: Bauer) -> None:
    ausf = SteuerbarerAusfuehrer()
    a, _, _ = reiter(baue, ausf)
    a.oeffne_datei(DATEI_A)
    fertig(ausf, 0, a)
    a.messung_hinzufuegen(DATEI_B)
    b = a.messungen.alle[1]
    a.entferne_messung(b.id)
    assert ausf.auftraege[2].abgebrochen and len(a.messungen) == 1
    a._abfrage()  # kein Absturz durch das abgebrochene Ergebnis
    a.beende()


def test_entfernen_nicht_aktiver_laesst_aktive_unveraendert(baue: Bauer) -> None:
    a, _, _ = zwei_messungen(baue)
    erste, zweite = a.messungen.alle
    a.entferne_messung(erste.id)
    assert a.messungen.aktive is zweite and a.lbl_datei.text() == "b.svd"
    a.entferne_messung(12345)  # unbekannt: nichts
    assert len(a.messungen) == 1


def test_rueckfrage_vor_dem_entfernen_wenn_serien_betroffen(
    baue: Bauer, monkeypatch: pytest.MonkeyPatch
) -> None:
    a, _, _ = zwei_messungen(baue)
    zweite = a.messungen.alle[1]
    gefragt: list[str] = []

    def ablehnen(_titel: str, text: str) -> bool:
        gefragt.append(text)
        return False

    monkeypatch.setattr(a, "_serien_betroffen", lambda _i: 2)
    monkeypatch.setattr(a, "_bestaetige_entfernen", ablehnen)
    a._entferne_geklickt(zweite.id)  # abgelehnt
    assert len(a.messungen) == 2 and "2 Serien" in gefragt[0] and "Messung B" in gefragt[0]
    monkeypatch.setattr(a, "_bestaetige_entfernen", lambda titel, text: True)
    a._entferne_geklickt(zweite.id)
    assert len(a.messungen) == 1


def test_umbenennen_ueber_dialog_eindeutig_und_pflicht(
    baue: Bauer, monkeypatch: pytest.MonkeyPatch
) -> None:
    a, _, _ = zwei_messungen(baue)
    erste, zweite = a.messungen.alle
    antworten = iter(["A", "Probe 2"])  # erst doppelt, dann gültig
    gefragt: list[str] = []

    def frage(_aktuell: str, grund: str) -> str:
        gefragt.append(grund)
        return next(antworten)

    monkeypatch.setattr(a, "_frage_kurzname", frage)
    a._umbenennen_geklickt(zweite.id)
    assert zweite.kurzname == "Probe 2" and "bereits" in gefragt[1]
    assert a.messungsleiste.chip_knopf(zweite.id).text().startswith("✔ (Probe 2)")  # type: ignore[union-attr]
    monkeypatch.setattr(a, "_frage_kurzname", lambda aktuell, grund: None)
    a._umbenennen_geklickt(erste.id)  # abgebrochen
    assert erste.kurzname == "A"


def test_tastatur_pfeile_fokus_entf_entfernt_nach_rueckfrage(
    baue: Bauer, monkeypatch: pytest.MonkeyPatch
) -> None:
    a, _, _ = zwei_messungen(baue)
    erste, zweite = a.messungen.alle
    k1 = a.messungsleiste.chip_knopf(erste.id)
    k2 = a.messungsleiste.chip_knopf(zweite.id)
    assert k1 is not None and k2 is not None
    assert k1.focusPolicy() == Qt.FocusPolicy.StrongFocus
    k2.setFocus()
    QTest.keyClick(k2, Qt.Key.Key_Left)
    assert k1.hasFocus() or QApplication.focusWidget() is k1
    monkeypatch.setattr(a, "_bestaetige_entfernen", lambda t, x: True)
    monkeypatch.setattr(a, "_serien_betroffen", lambda _i: 0)
    QTest.keyClick(k1, Qt.Key.Key_Delete)
    assert a.messungen.alle == (zweite,)


def test_tab_reihenfolge_enthaelt_hinzu_knopf_und_chips(baue: Bauer) -> None:
    a, _, _ = zwei_messungen(baue)
    ketten = a.messungsleiste.tab_kette()
    assert len(ketten) == 4  # zwei Chips mit je Wechsel- und Entfernen-Knopf
    for w in [a.btn_oeffnen, a.btn_messung_hinzu, *ketten]:
        assert w.focusPolicy() != Qt.FocusPolicy.NoFocus


def test_dateileiste_ueberlappt_bei_1100_mal_680_nicht(baue: Bauer) -> None:
    a, _, _ = zwei_messungen(baue)
    w = a.window()
    w.resize(1100, 680)
    QApplication.processEvents()
    leiste = a.findChild(QWidget, "dateileiste")
    assert leiste is not None
    teile = [
        a.btn_oeffnen,
        a.btn_messung_hinzu,
        a.messungsleiste,
        a.lbl_datei,
        a.btn_export,
        a.btn_bild,
        a.lbl_arbeitsansicht,
    ]
    rects = [(t.mapTo(leiste, t.rect().topLeft()), t.size(), t) for t in teile if t.isVisibleTo(a)]
    for i, (p1, s1, t1) in enumerate(rects):
        for p2, s2, t2 in rects[i + 1 :]:
            ueber = (
                p1.x() < p2.x() + s2.width()
                and p2.x() < p1.x() + s1.width()
                and p1.y() < p2.y() + s2.height()
                and p2.y() < p1.y() + s1.height()
            )
            assert not ueber, (t1.objectName(), t2.objectName())
    assert a.messungsleiste.width() >= 120  # Chipzeile behält Platz (scrollt sonst)
    assert a.lbl_pfad.width() >= 40


def test_schliessen_bricht_ladende_messungen_ab(baue: Bauer) -> None:
    ausf = SteuerbarerAusfuehrer()
    a, _, _ = reiter(baue, ausf)
    a.oeffne_datei(DATEI_A)
    fertig(ausf, 0, a)
    a.messung_hinzufuegen(DATEI_B)
    assert a.laeuft()
    a.beende()
    assert ausf.auftraege[2].abgebrochen and not a.laeuft()
    a2, _, _ = reiter(baue, NieFertigAusfuehrer())
    a2.beende()
