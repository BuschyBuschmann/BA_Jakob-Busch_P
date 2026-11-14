"""Ansicht 5 „Diagramm“ in der Oberfläche (R-058, P-AUSW2 S7; UI-10 bis UI-14, UI-17, UI-34).

Zwei synthetische Messungen mit verschiedener Linienzahl: A 64 Linien und 4 Punkte (Label 10 bis
13), B 32 Linien und 3 Punkte (Label 10 bis 12). Aufträge laufen über ``SteuerbarerAusfuehrer``.
"""

from __future__ import annotations

from dataclasses import replace

import numpy as np
import pytest
from gui_ausw_hilfen import Bauer, Protokoll, SteuerbarerAusfuehrer, synth_geladen
from PySide6.QtCore import Qt
from PySide6.QtTest import QTest
from PySide6.QtWidgets import QApplication, QWidget

from ldv_automation.auswertung.daten import Punkte
from ldv_automation.auswertung.laden import Geladen
from ldv_automation.darstellung.achsen import Bereich
from ldv_automation.darstellung.serien_daten import SerienSpec
from ldv_automation.gui.auswahl_diagramm import SerienDialog
from ldv_automation.gui.auswerten_reiter import (
    TEXT_BILD_ANSICHT_5,
    AuswertenReiter,
)
from ldv_automation.gui.hauptfenster import Hauptfenster
from ldv_automation.gui.serien import (
    SERIEN_MAX,
    TEXT_KEINE_SERIE,
    TEXT_SERIE_DOPPELT,
    TEXT_SERIEN_VOLL,
    baue_spec,
)

pytestmark = pytest.mark.gui

DATEI_A = "C:\\messungen\\a.svd"
DATEI_B = "C:\\messungen\\b.svd"
PAAR = ("Vib X", "Ref1")
K_B = 32
P_B = 3


def geladen_klein(pfad: str, *, referenz: bool = True) -> Geladen:
    """Messung B: 32 Linien (0,5 … 16 Hz), 3 Punkte (Label 10 … 12)."""
    g = synth_geladen(pfad=pfad, referenz=referenz)
    d = g.messdaten
    punkte = Punkte(
        index=d.punkte.index[:P_B],
        label=d.punkte.label[:P_B],
        koordinaten_m=d.punkte.koordinaten_m[:P_B],
    )
    daten = replace(
        d,
        frequenz_hz=d.frequenz_hz[:K_B],
        punkte=punkte,
        ap={k: v[:P_B, :K_B] for k, v in d.ap.items()},
        cp={k: v[:P_B, :K_B] for k, v in d.cp.items()},
    )
    return replace(g, messdaten=daten)


def aufbau(
    baue: Bauer, *, ref_b: bool = True
) -> tuple[AuswertenReiter, Protokoll, Hauptfenster, SteuerbarerAusfuehrer]:
    ausf = SteuerbarerAusfuehrer()
    w, prot = baue(ausf)
    a = w.auswerten
    assert a is not None
    prot.geladen[DATEI_B] = geladen_klein(DATEI_B, referenz=ref_b)
    a.oeffne_datei(DATEI_A)
    ausf.auftraege[0].freigegeben = True
    a._abfrage()
    a.messung_hinzufuegen(DATEI_B)
    ausf.auftraege[2].freigegeben = True
    a._abfrage()
    assert len(a.messungen) == 2
    return a, prot, w, ausf


def ansicht_5(a: AuswertenReiter) -> None:
    a.btn_ansicht[5].click()
    assert a.ansicht == 5


def mid(a: AuswertenReiter, nr: int) -> int:
    return a.messungen.alle[nr].id


def lege_an(a: AuswertenReiter, *specs: SerienSpec) -> None:
    for s in specs:
        assert a._serie_anlegen(s)
    a._zeichne()


def achsen(a: AuswertenReiter) -> tuple[object, ...]:
    assert a.plot.zeichnung is not None
    return a.plot.zeichnung.achsen


# --- Knopf, Taste, Hinweis -----


def test_knopf_fuenf_strg_5_und_hinweis_ohne_serie(baue: Bauer) -> None:
    a, _, w, _ = aufbau(baue)
    assert a.btn_ansicht[5].text() == "5 Diagramm" and a.btn_ansicht[5].isEnabled()
    assert a.btn_ansicht[5].objectName() == "btn_ansicht_5"
    assert a.act_ansicht[5].shortcut().toString() == "Ctrl+5"
    w.activateWindow()
    QTest.keyClick(w, Qt.Key.Key_5, Qt.KeyboardModifier.ControlModifier)  # UI-34
    assert a.ansicht == 5 and a.btn_ansicht[5].isChecked()
    assert a.lbl_ansicht_platzhalter.text() == TEXT_KEINE_SERIE
    assert a._ae_stapel.currentIndex() == 2  # Textseite statt Plot
    assert a.plot.zeichnung is None
    assert a.punkt_gruppe.isHidden() and a.kanalpaar_gruppe.isHidden()
    assert not a.auswahl_diagramm.isHidden()


def test_ansicht_5_mit_einer_messung_ohne_vergleichspartner(baue: Bauer) -> None:
    ausf = SteuerbarerAusfuehrer()
    w, _ = baue(ausf)
    a = w.auswerten
    assert a is not None
    a.oeffne_datei(DATEI_A)
    ausf.auftraege[0].freigegeben = True
    a._abfrage()
    ansicht_5(a)
    lege_an(
        a,
        baue_spec(mid(a, 0), 10, "h1", kanalpaar=PAAR),
        baue_spec(mid(a, 0), 11, "h1", kanalpaar=PAAR),
    )
    assert len(achsen(a)) == 1 and len(achsen(a)[0].get_lines()) == 2  # type: ignore[attr-defined]


# --- UI-10, UI-11, UI-13 -----


def test_ueberlagert_zwei_messungen_linien_linienarten_und_laenge(baue: Bauer) -> None:
    a, _, _, _ = aufbau(baue)
    ansicht_5(a)
    lege_an(
        a,
        baue_spec(mid(a, 0), 10, "h1", kanalpaar=PAAR),
        baue_spec(mid(a, 1), 10, "h1", kanalpaar=PAAR),
    )
    ax = achsen(a)[0]
    l1, l2 = ax.get_lines()  # type: ignore[attr-defined]
    assert l1.get_linestyle() != l2.get_linestyle()  # UI-10
    assert (len(l1.get_xdata()), len(l2.get_xdata())) == (64, K_B)  # UI-13
    eintraege = a.plot.zeichnung.hilfsobjekte["legende_eintraege"]  # type: ignore[union-attr]
    assert eintraege == ["A · Punkt 10 · Vib X / Ref1", "B · Punkt 10 · Vib X / Ref1"]  # UI-11
    assert "Messungen A, B" in a.lbl_plotkopf.text() and "überlagert" in a.lbl_plotkopf.text()
    beschreibung = a.plot.canvas.accessibleDescription()
    assert "A · Punkt 10" in beschreibung and "Frequenzbereich" in beschreibung
    assert a.plot.canvas.accessibleName() == "Diagramm: Diagramm"


def test_nebeneinander_zwei_teilbilder_mit_gekoppelten_achsen(baue: Bauer) -> None:
    a, _, _, _ = aufbau(baue)
    ansicht_5(a)
    lege_an(
        a,
        baue_spec(mid(a, 0), None, "h1", kanalpaar=PAAR),
        baue_spec(mid(a, 1), None, "h1", kanalpaar=PAAR),
    )
    a.auswahl_diagramm.rb_anordnung_nebeneinander.setChecked(True)
    a1, a2 = achsen(a)
    assert a1.get_shared_x_axes().joined(a1, a2) and a1.get_shared_y_axes().joined(a1, a2)  # type: ignore[attr-defined]
    assert a1.get_title(loc="left") == "A · |H1|" and a2.get_title(loc="left") == "B · |H1|"  # type: ignore[attr-defined]
    assert "nebeneinander" in a.lbl_plotkopf.text()
    a.auswahl_diagramm.rb_anordnung_ueberlagert.setChecked(True)
    assert len(achsen(a)) == 1


def test_mittel_nennt_formel_und_punktzahl_aus_den_daten(baue: Bauer) -> None:
    a, _, _, _ = aufbau(baue)
    ansicht_5(a)
    lege_an(a, baue_spec(mid(a, 0), None, "h1", kanalpaar=PAAR))
    eintrag = a.plot.zeichnung.hilfsobjekte["legende_eintraege"][0]  # type: ignore[union-attr]
    assert eintrag.endswith("Betragsmittel |H1| über 4 Punkte")  # Formel und Punktzahl (UI-11)


# --- UI-12: Für alle Messungen -----


def test_fuer_alle_legt_je_messung_eine_serie_an_und_meldet_fehlendes_label(baue: Bauer) -> None:
    a, _, _, _ = aufbau(baue)
    ansicht_5(a)
    lege_an(a, baue_spec(mid(a, 0), 12, "h1", kanalpaar=PAAR))
    a.auswahl_diagramm.btn_serie_alle.click()
    assert [(s.messung_id, s.punkt_label) for s in a._serien.specs] == [
        (mid(a, 0), 12),
        (mid(a, 1), 12),
    ]
    assert len(achsen(a)[0].get_lines()) == 2  # type: ignore[attr-defined]
    a._serien.leere()
    lege_an(a, baue_spec(mid(a, 0), 13, "h1", kanalpaar=PAAR))  # Label 13 gibt es nur in A
    a.auswahl_diagramm.btn_serie_alle.click()
    assert len(a._serien) == 1  # für B wurde nichts angelegt
    meldung = a.auswahl_diagramm.lbl_meldung.text()
    assert "B: Punkt 13 gibt es nicht." in meldung and "✖" in meldung
    assert "B: Punkt 13 gibt es nicht." in a.lbl_cursor.volltext()  # Grund in AF


def test_fuer_alle_ohne_serie_nimmt_die_voreinstellung(baue: Bauer) -> None:
    a, _, _, _ = aufbau(baue)
    ansicht_5(a)
    a.auswahl_diagramm.btn_serie_alle.click()
    assert [(s.groesse, s.komponente, s.punkt_label) for s in a._serien.specs] == [
        ("spektrum", "Z", None),
        ("spektrum", "Z", None),
    ]
    assert a._serien.specs[0].messung_id != a._serien.specs[1].messung_id


def test_fuer_alle_mit_voller_liste_legt_nur_an_was_passt(baue: Bauer) -> None:
    a, _, _, _ = aufbau(baue)
    ansicht_5(a)
    lege_an(a, *[baue_spec(mid(a, 0), 10 + i, "h1", kanalpaar=PAAR) for i in range(3)])
    a.auswahl_diagramm.liste_serien.setCurrentRow(2)
    a.auswahl_diagramm.btn_serie_alle.click()  # für A vorhanden (Dopplung), für B ein freier Platz
    assert len(a._serien) == SERIEN_MAX
    a.auswahl_diagramm.liste_serien.setCurrentRow(0)
    a.auswahl_diagramm.btn_serie_alle.click()  # B hätte keinen Platz mehr
    assert TEXT_SERIEN_VOLL in a.auswahl_diagramm.lbl_meldung.text()


# --- Dopplung, Grenze, Slots, Sichtbarkeit -----


def test_dopplung_und_fuenfte_serie_mit_hinweistext(baue: Bauer) -> None:
    a, _, _, _ = aufbau(baue)
    ansicht_5(a)
    sel = a.auswahl_diagramm
    erste = baue_spec(mid(a, 0), 10, "h1", kanalpaar=PAAR)
    lege_an(a, erste)
    assert not a._serie_anlegen(erste)
    assert sel.lbl_meldung.text() == TEXT_SERIE_DOPPELT and len(a._serien) == 1
    lege_an(a, *[baue_spec(mid(a, 0), 11 + i, "h1", kanalpaar=PAAR) for i in range(3)])
    assert len(a._serien) == SERIEN_MAX
    assert not sel.btn_serie_neu.isEnabled() and sel.btn_serie_neu.toolTip() == TEXT_SERIEN_VOLL
    assert sel.lbl_voll.isVisibleTo(a)
    assert not a._serie_anlegen(baue_spec(mid(a, 1), 10, "h1", kanalpaar=PAAR))
    assert sel.lbl_meldung.text() == TEXT_SERIEN_VOLL


def test_serie_neu_ueber_dialog_und_entfernen_slot_bleibt(
    baue: Bauer, monkeypatch: pytest.MonkeyPatch
) -> None:
    a, _, _, _ = aufbau(baue)
    ansicht_5(a)
    antworten = iter(
        [
            baue_spec(mid(a, 0), 10, "h1", kanalpaar=PAAR),
            baue_spec(mid(a, 1), 10, "h1", kanalpaar=PAAR),
        ]
    )
    monkeypatch.setattr(a, "_frage_serie", lambda: next(antworten))
    sel = a.auswahl_diagramm
    sel.btn_serie_neu.click()
    sel.btn_serie_neu.click()
    assert sel.liste_serien.count() == 2
    b_vorher = achsen(a)[0].get_lines()[1].get_linestyle()  # type: ignore[attr-defined]
    sel.liste_serien.setCurrentRow(0)
    sel.btn_serie_entfernen.click()  # A entfernt, B behält Slot 1
    assert sel.liste_serien.count() == 1
    assert achsen(a)[0].get_lines()[0].get_linestyle() == b_vorher  # type: ignore[attr-defined]  # UI-20


def test_sichtbar_haekchen_blendet_aus_ohne_die_grenzen_zu_aendern(baue: Bauer) -> None:
    a, _, _, _ = aufbau(baue)
    ansicht_5(a)
    lege_an(
        a,
        baue_spec(mid(a, 0), 10, "h1", kanalpaar=PAAR),
        baue_spec(mid(a, 1), 10, "h1", kanalpaar=PAAR),
    )
    a.plot.achsen_zustand.setze_bereich(5, "frequenz", Bereich(4.0, 12.0))
    a._zeichne()
    vorher = achsen(a)[0].get_ylim()  # type: ignore[attr-defined]
    liste = a.auswahl_diagramm.liste_serien
    item = liste.item(1)
    assert item is not None
    item.setCheckState(Qt.CheckState.Unchecked)
    assert not a._serien.specs[1].sichtbar
    ax = achsen(a)[0]
    assert ax.get_ylim() == pytest.approx(vorher, rel=1e-12)  # type: ignore[attr-defined]  # UI-21
    assert not ax.get_lines()[1].get_visible()  # type: ignore[attr-defined]
    assert len(a.plot.zeichnung.hilfsobjekte["legende_eintraege"]) == 1  # type: ignore[union-attr]


# --- Größen -----


def test_groessenwahl_zieht_serien_mit_und_zeigt_einheit(baue: Bauer) -> None:
    a, _, _, _ = aufbau(baue)
    ansicht_5(a)
    sel = a.auswahl_diagramm
    lege_an(a, baue_spec(mid(a, 0), None, "spektrum", komponente="Z"))
    assert achsen(a)[0].get_ylabel() == "Amplitude [m/s]"  # type: ignore[attr-defined]
    sel.rb_groesse["h1"].setChecked(True)
    assert a._serien.specs[0].groesse == "h1" and a._serien.specs[0].kanalpaar == ("Vib Z", "Ref1")
    assert achsen(a)[0].get_ylabel() == "|H1| [(m/s)/N]"  # type: ignore[attr-defined]  # UI-15
    sel.rb_groesse["kohaerenz"].setChecked(True)
    ax = achsen(a)[0]
    assert ax.get_ylim() == (0.0, 1.05) and ax.get_ylabel() == "Kohärenz γ² [1]"  # type: ignore[attr-defined]
    sel.rb_groesse["spektrum"].setChecked(True)
    assert a._serien.specs[0].komponente == "Z" and sel.rb_teil_cph.isVisibleTo(a)


def test_phase_in_grad_und_kennzeichen_m8_im_bild(baue: Bauer) -> None:
    a, _, _, _ = aufbau(baue)
    ansicht_5(a)
    lege_an(a, baue_spec(mid(a, 0), 10, "phase", kanalpaar=PAAR))
    ax = achsen(a)[0]
    assert ax.get_ylabel() == "Phase [°]" and ax.get_ylim() == (-180.0, 180.0)  # type: ignore[attr-defined]
    assert any("unbestätigt" in t for t in a.plot.zeichnung.alle_texte())  # type: ignore[union-attr]
    assert a.achsenleiste.gruppe("phase").isVisibleTo(a)


def test_ohne_referenz_sind_groessen_gesperrt_mit_begruendung(baue: Bauer) -> None:
    ausf = SteuerbarerAusfuehrer()
    w, prot = baue(ausf)
    a = w.auswerten
    assert a is not None
    prot.geladen[DATEI_A] = synth_geladen(pfad=DATEI_A, referenz=False)
    a.oeffne_datei(DATEI_A)
    ausf.auftraege[0].freigegeben = True
    a._abfrage()
    ansicht_5(a)
    sel = a.auswahl_diagramm
    for g in ("h1", "h2", "kohaerenz", "phase"):
        assert not sel.rb_groesse[g].isEnabled()  # UI-17
        assert "Referenz" in sel._lbl_grund[g].text() and sel._lbl_grund[g].isVisibleTo(a)
    assert sel.rb_groesse["spektrum"].isEnabled() and sel.rb_groesse["spektrum"].isChecked()
    assert not sel.rb_teil_cph.isEnabled() and sel.rb_teil_ap.isChecked()  # |CPH| braucht Referenz
    lege_an(a, baue_spec(mid(a, 0), None, "spektrum", komponente="X", teilgroesse="leistung"))
    assert len(achsen(a)[0].get_lines()) == 1  # type: ignore[attr-defined]


def test_nicht_darstellbare_serie_wird_markiert_und_in_af_gemeldet(baue: Bauer) -> None:
    a, _, _, _ = aufbau(baue)
    ansicht_5(a)
    lege_an(
        a,
        baue_spec(mid(a, 0), 10, "h1", kanalpaar=PAAR),
        baue_spec(mid(a, 1), 11, "h1", kanalpaar=PAAR),
    )
    a._serien.hinzufuegen(
        baue_spec(mid(a, 0), None, "phase", kanalpaar=PAAR)
    )  # Mittel: keine Phase
    a.auswahl_diagramm.rb_anordnung_nebeneinander.setChecked(True)
    a._zeichne()
    zeile = a.auswahl_diagramm.liste_serien.item(2)
    assert zeile is not None and zeile.text().startswith("✖ Nicht darstellbar")  # UI-17
    assert "Phase beim Mittel nicht darstellbar" in a.lbl_cursor.volltext()  # AF
    assert len(a.plot.zeichnung.achsen) == 2  # type: ignore[union-attr]  # die möglichen Serien


# --- UI-14: Entfernen einer Messung -----


def test_entfernen_einer_messung_mit_serien_fragt_nach_und_entfernt_sie(
    baue: Bauer, monkeypatch: pytest.MonkeyPatch
) -> None:
    a, _, _, _ = aufbau(baue)
    ansicht_5(a)
    lege_an(
        a,
        baue_spec(mid(a, 0), 10, "h1", kanalpaar=PAAR),
        baue_spec(mid(a, 1), 10, "h1", kanalpaar=PAAR),
        baue_spec(mid(a, 1), 11, "h1", kanalpaar=PAAR),
    )
    fragen: list[tuple[str, str]] = []
    antwort = [False]

    def frage(titel: str, text: str) -> bool:
        fragen.append((titel, text))
        return antwort[0]

    monkeypatch.setattr(a, "_bestaetige_entfernen", frage)
    b = a.messungen.alle[1]
    a._entferne_geklickt(b.id)  # abgelehnt: nichts passiert
    assert len(a.messungen) == 2 and len(a._serien) == 3
    assert "2 Serien" in fragen[0][1] and "Messung B" in fragen[0][1]
    antwort[0] = True
    a._entferne_geklickt(b.id)
    assert len(a.messungen) == 1 and [s.messung_id for s in a._serien.specs] == [mid(a, 0)]
    assert a.ansicht == 5 and len(achsen(a)[0].get_lines()) == 1  # type: ignore[attr-defined]
    a._entferne_geklickt(a.messungen.alle[0].id)  # eine Serie betroffen: wieder gefragt
    assert "1 Serie " in fragen[-1][1] and len(a.messungen) == 0
    assert len(a._serien) == 0 and a.zustand.name == "KEINE_DATEI"


def test_entfernen_ohne_betroffene_serien_ohne_rueckfrage(
    baue: Bauer, monkeypatch: pytest.MonkeyPatch
) -> None:
    a, _, _, _ = aufbau(baue)
    monkeypatch.setattr(a, "_bestaetige_entfernen", lambda *_: pytest.fail("keine Rückfrage"))
    a._entferne_geklickt(mid(a, 1))
    assert len(a.messungen) == 1


def test_oeffnen_ersetzt_die_messung_und_entfernt_nur_ihre_serien(
    baue: Bauer, monkeypatch: pytest.MonkeyPatch
) -> None:
    a, _, _, ausf = aufbau(baue)
    fragen: list[str] = []

    def zustimmen(_titel: str, text: str) -> bool:
        fragen.append(text)
        return True

    monkeypatch.setattr(a, "_bestaetige_ersetzen", zustimmen)
    ansicht_5(a)
    lege_an(
        a,
        baue_spec(mid(a, 0), 10, "h1", kanalpaar=PAAR),
        baue_spec(mid(a, 1), 10, "h1", kanalpaar=PAAR),
    )
    b = a.messungen.alle[1]
    assert a.messungen.aktive is b
    a.oeffne_datei(DATEI_A)  # ersetzt die aktive Messung B durch A' (Datei A noch einmal)
    assert len(fragen) == 1 and "Messung B" in fragen[0] and "1 Serie" in fragen[0]  # UI-14
    ausf.auftraege[-1].freigegeben = True
    a._abfrage()
    assert [s.messung_id for s in a._serien.specs] == [mid(a, 0)]  # nur A behält seine Serie
    assert a.messungen.alle[1].kurzname == "B" and a.ansicht == 1  # Kurzname bleibt, Ansicht 1


# --- Achsen, Wechsel der aktiven Messung, Bild -----


def test_achsenleiste_in_ansicht_5_setzt_frequenz_und_skala(baue: Bauer) -> None:
    a, _, _, _ = aufbau(baue)
    ansicht_5(a)
    lege_an(
        a,
        baue_spec(mid(a, 0), 10, "h1", kanalpaar=PAAR),
        baue_spec(mid(a, 1), 10, "h1", kanalpaar=PAAR),
    )
    ed_von = a.achsenleiste.gruppe("frequenz").feld("von")
    ed_bis = a.achsenleiste.gruppe("frequenz").feld("bis")
    for ed, text in ((ed_von, "2"), (ed_bis, "10")):
        ed.selectAll()
        ed.del_()
        QTest.keyClicks(ed, text)
        QTest.keyClick(ed, Qt.Key.Key_Return)
    ax = achsen(a)[0]
    assert ax.get_xlim() == pytest.approx((2.0, 10.0), rel=1e-9)  # type: ignore[attr-defined]  # UI-1
    a.achsenleiste.gruppe("betrag").rb_linear.click()  # type: ignore[union-attr]
    assert achsen(a)[0].get_yscale() == "linear"  # type: ignore[attr-defined]  # UI-2
    assert a.plot.achsen_zustand.skala(5, "betrag") == "linear"
    assert a.plot.achsen_zustand.skala(1, "betrag") == "log"  # je Ansicht


def test_wechsel_der_aktiven_messung_aendert_das_diagramm_nicht(baue: Bauer) -> None:
    a, _, _, _ = aufbau(baue)
    ansicht_5(a)
    lege_an(
        a,
        baue_spec(mid(a, 0), 10, "h1", kanalpaar=PAAR),
        baue_spec(mid(a, 1), 10, "h1", kanalpaar=PAAR),
    )
    a.plot.achsen_zustand.setze_bereich(5, "frequenz", Bereich(3.0, 9.0))
    a._zeichne()
    vorher = [np.asarray(linie.get_ydata()).copy() for linie in achsen(a)[0].get_lines()]  # type: ignore[attr-defined]
    xlim = achsen(a)[0].get_xlim()  # type: ignore[attr-defined]
    a._aktiviere_messung(mid(a, 0))
    assert a.ansicht == 5 and len(a._serien) == 2
    nachher = [np.asarray(linie.get_ydata()) for linie in achsen(a)[0].get_lines()]  # type: ignore[attr-defined]
    assert all(np.array_equal(v, n) for v, n in zip(vorher, nachher, strict=True))
    assert achsen(a)[0].get_xlim() == xlim  # type: ignore[attr-defined]


def test_bild_speichern_ist_in_ansicht_5_noch_gesperrt_export_nicht(baue: Bauer) -> None:
    a, _, _, _ = aufbau(baue)
    ansicht_5(a)
    lege_an(a, baue_spec(mid(a, 0), 10, "h1", kanalpaar=PAAR))
    assert not a.btn_bild.isEnabled() and a.btn_bild.toolTip() == TEXT_BILD_ANSICHT_5
    assert a.btn_export.isEnabled()  # Export bleibt auf die aktive Messung bezogen
    a.btn_ansicht[1].click()
    assert a.btn_bild.isEnabled()


def test_cache_groesse_folgt_den_serien(baue: Bauer) -> None:
    a, _, _, _ = aufbau(baue)
    ansicht_5(a)
    cache = a.messungen.alle[0].cache
    assert cache is not None and cache.groesse == 2
    lege_an(
        a,
        baue_spec(mid(a, 0), 10, "h1", kanalpaar=("Vib X", "Ref1")),
        baue_spec(mid(a, 0), 10, "h1", kanalpaar=("Vib Y", "Ref1")),
        baue_spec(mid(a, 0), 10, "h1", kanalpaar=("Vib Z", "Ref1")),
    )
    assert cache.groesse == 3
    a._serien.leere()
    a._zeichne()
    assert cache.groesse == 2


# --- Dialog -----


def test_serien_dialog_liefert_die_beschreibung(baue: Bauer) -> None:
    a, _, _, _ = aufbau(baue)
    dialog = SerienDialog(
        a._angaben_der_messungen(), "h1", "kohaerent", nebeneinander=False, aktiv_id=mid(a, 1)
    )
    assert dialog.combo_messung.currentData() == mid(a, 1)  # die aktive Messung ist vorgewählt
    assert dialog.combo_punkt.count() == 1 + P_B and dialog.combo_punkt.itemText(0).startswith(
        "Mittel"
    )
    assert dialog.combo_groesse.isHidden() and not dialog.combo_paar.isHidden()
    assert dialog.combo_komponente.isHidden()
    dialog.combo_punkt.setCurrentIndex(2)
    dialog.combo_paar.setCurrentIndex(1)
    spec = dialog.ergebnis()
    assert spec is not None
    assert (spec.messung_id, spec.punkt_label, spec.groesse) == (mid(a, 1), 11, "h1")
    assert spec.kanalpaar == ("Vib Y", "Ref1")
    dialog.combo_messung.setCurrentIndex(0)  # anderer Messungsinhalt: Punktliste neu
    assert dialog.combo_punkt.count() == 1 + 4
    dialog.close()
    spektrum = SerienDialog(a._angaben_der_messungen(), "spektrum", "leistung", nebeneinander=True)
    assert not spektrum.combo_groesse.isHidden() and spektrum.combo_paar.isHidden()
    spektrum.combo_komponente.setCurrentIndex(3)
    s = spektrum.ergebnis()
    assert s is not None and s.komponente == "3D" and s.teilgroesse == "leistung"
    spektrum.combo_groesse.setCurrentIndex(1)  # |H1| je Serie bei „nebeneinander“
    assert spektrum.groesse() == "h1" and not spektrum.combo_paar.isHidden()
    ohne = SerienDialog([], "h1", "kohaerent", nebeneinander=False)
    assert ohne.ergebnis() is None


def test_tab_reihenfolge_und_fokus_der_neuen_elemente(baue: Bauer) -> None:
    a, _, _, _ = aufbau(baue)
    QApplication.processEvents()
    for widget in a.auswahl_diagramm.tab_kette():
        assert widget.focusPolicy() != Qt.FocusPolicy.NoFocus
    assert a.auswahl_diagramm.objectName() == "auswahl_diagramm"
    for name in ("liste_serien", "btn_serie_neu", "btn_serie_alle", "rb_anordnung_ueberlagert"):
        assert a.auswahl_diagramm.findChild(QWidget, name) is not None
