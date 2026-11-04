"""Ansichten 2 bis 4 im Reiter „Auswerten“ (P-AUSW T3b); offscreen, Marker ``gui``.

Daten: ``gui_ausw_hilfen.synth_geladen`` (4 Punkte, 64 Linien, eine Resonanz bei 16 Hz,
ζ = 0,125 aus der -3-dB-Breite) über einen ``DirektAusfuehrer``.
"""

from __future__ import annotations

import logging
from typing import Any

import pytest
from gui_ausw_hilfen import (
    PFAD,
    Bauer,
    DirektAusfuehrer,
    NieFertigAusfuehrer,
    PruefErgebnis,
    SteuerbarerAusfuehrer,
    synth_geladen,
    synth_pruefung,
)
from gui_hilfen import AttrappenSitzung, bild
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QAbstractButton, QApplication
from pytestqt.qtbot import QtBot
from test_gui_auswerten import lade, linien

from ldv_automation.auswertung.annahmen import Annahmen
from ldv_automation.darstellung import auswahl as dar_auswahl
from ldv_automation.darstellung.schwingform import HINWEIS_PHASE_SPRUNG
from ldv_automation.gui import anzeige_auswerten as aa
from ldv_automation.gui import auswerten_reiter, daten_auswerten
from ldv_automation.gui.auswerten_reiter import AuswertenReiter

pytestmark = pytest.mark.gui


def geladen_mit(
    baue: Bauer, qtbot: QtBot, *, ausfuehrer: Any = None, **synth: Any
) -> AuswertenReiter:
    w, prot = baue(ausfuehrer)
    prot.geladen[PFAD] = synth_geladen(**synth)
    return lade(qtbot, w)


def xlim(a: AuswertenReiter) -> tuple[float, float]:
    z = a.plot.zeichnung
    assert z is not None
    return tuple(z.achsen[0].get_xlim())  # type: ignore[return-value]


def texte(a: AuswertenReiter) -> list[str]:
    assert a.plot.zeichnung is not None
    return a.plot.zeichnung.alle_texte()


# --- Freischaltung, Kanalpaarwahl -----------------------------------------------------------------


def test_ansichten_2_bis_4_sind_nach_dem_laden_frei(baue: Bauer, qtbot: QtBot) -> None:
    a = geladen_mit(baue, qtbot)
    for nr in (1, 2, 3, 4):
        assert a.btn_ansicht[nr].isEnabled(), nr
        assert a.btn_ansicht[nr].toolTip() == ""
    a.btn_ansicht[2].click()
    assert a.ansicht == 2 and a.btn_ansicht[2].isChecked()
    assert a._ad_stapel.currentIndex() == 1


def test_kanalpaarwahl_gemeinsam_fuer_ansicht_2_und_3_erstes_paar_voreingestellt(
    baue: Bauer, qtbot: QtBot
) -> None:
    a = geladen_mit(baue, qtbot, mit_ref2=True)
    assert a.combo_kanalpaar.count() == 4
    assert a.combo_kanalpaar.itemText(0) == "Vib X / Ref1"  # Dateireihenfolge
    assert a.combo_kanalpaar.currentIndex() == 0
    assert a.kanalpaar_gruppe.isHidden()  # Ansicht 1: nicht sichtbar
    a.btn_ansicht[2].click()
    assert not a.kanalpaar_gruppe.isHidden() and a.punkt_gruppe.isVisible()
    a.combo_kanalpaar.setCurrentIndex(3)
    assert "Ref2 / Ref1" in a.lbl_plotkopf.text()
    a.btn_ansicht[3].click()
    assert not a.kanalpaar_gruppe.isHidden() and a.punkt_gruppe.isHidden()
    assert a.combo_kanalpaar.currentIndex() == 3  # dieselbe Wahl in beiden Ansichten
    assert "Ref2 / Ref1" in a.lbl_plotkopf.text()
    a.btn_ansicht[4].click()
    assert (
        not a.kanalpaar_gruppe.isHidden()
    )  # auch in Ansicht 4 wählbar (Spitzenliste, Kennzeichen)


def test_kanalpaarwahl_nur_bei_mehr_als_einem_paar_sichtbar(baue: Bauer, qtbot: QtBot) -> None:
    a = geladen_mit(baue, qtbot)  # nur Vib X, Y, Z gegen Ref1
    assert a.combo_kanalpaar.count() == 3
    a.btn_ansicht[2].click()
    assert not a.kanalpaar_gruppe.isHidden()


# --- Ansicht 2 (UI-5, UI-6, UI-11) --------------------------------------------------------------


def test_ui_5_betrag_und_kohaerenz_mit_einheit_des_quotienten(baue: Bauer, qtbot: QtBot) -> None:
    a = geladen_mit(baue, qtbot)
    a.btn_ansicht[2].click()
    z = a.plot.zeichnung
    assert z is not None and set(z.linien) == {"H1", "H2", "kohaerenz"}
    assert len(z.achsen) == 2  # ohne Phase: Betrag und Kohärenz
    assert z.achsen[0].get_ylabel() == "Betrag [(m/s)/N]"  # Antwort- durch Referenzeinheit
    assert "Kohärenz" in z.achsen[1].get_ylabel()
    assert z.achsen[1].get_ylim() == (0.0, 1.0) or z.achsen[1].get_ylim()[1] >= 1.0
    assert a.plot.canvas.accessibleName() == "Diagramm: H1/H2 und Kohärenz"


def test_ui_5_h1_und_h2_einzeln_abschaltbar_mindestens_eins(baue: Bauer, qtbot: QtBot) -> None:
    a = geladen_mit(baue, qtbot)
    a.btn_ansicht[2].click()
    sel = a.auswahl_frf
    sel.chk_h2.setChecked(False)
    assert set(a.plot.zeichnung.linien) == {"H1", "kohaerenz"}  # type: ignore[union-attr]
    sel.chk_h1.click()  # letztes darf nicht abgewählt werden
    assert sel.chk_h1.isChecked()
    assert set(a.plot.zeichnung.linien) == {"H1", "kohaerenz"}  # type: ignore[union-attr]
    sel.chk_h2.setChecked(True)
    sel.chk_h1.setChecked(False)
    assert set(a.plot.zeichnung.linien) == {"H2", "kohaerenz"}  # type: ignore[union-attr]


def test_ui_5_phase_anzeigen_fuegt_teilbild_hinzu(baue: Bauer, qtbot: QtBot) -> None:
    a = geladen_mit(baue, qtbot)
    a.btn_ansicht[2].click()
    a.liste_punkte.setCurrentRow(2)  # Punkt statt Mittel
    a.auswahl_frf.chk_phase.setChecked(True)
    z = a.plot.zeichnung
    assert z is not None and "phase" in z.linien and len(z.achsen) == 3
    assert z.achsen[1].get_ylabel() == "Phase [°]"  # Anzeige in Grad
    assert "Punkt 11" in a.lbl_plotkopf.text()


def test_ui_11_phase_traegt_kennzeichen_unbestaetigt_aus_der_annahme(
    baue: Bauer, qtbot: QtBot
) -> None:
    a = geladen_mit(baue, qtbot)
    a.btn_ansicht[2].click()
    a.liste_punkte.setCurrentRow(1)
    a.auswahl_frf.chk_phase.setChecked(True)
    m8 = next(e for e in Annahmen().eintraege() if e.nr == "M8")
    kennzeichen = [t for t in texte(a) if "unbestätigt" in t]
    assert (
        kennzeichen and kennzeichen[0] == "⚠ unbestätigt (M8: Polarität der Referenzkanäle offen)"
    )
    assert m8.beschreibung not in kennzeichen[0]  # Formel nur im Tooltip
    assert m8.beschreibung in a.auswahl_frf.chk_phase.toolTip()
    assert kennzeichen[0].startswith("⚠")  # Symbol plus Wort
    # Kohärenz und Betrag tragen das Kennzeichen nicht: genau ein Kennzeichen im Bild
    assert len(kennzeichen) == 1


def test_ui_11_kennzeichen_verschwindet_wenn_m8_bestaetigt_ist_ohne_codeaenderung(
    baue: Bauer, qtbot: QtBot
) -> None:
    a = geladen_mit(baue, qtbot)
    bestaetigt = tuple(
        type(e)(
            nr=e.nr,
            parameter=e.parameter,
            wert=e.wert,
            status="bestätigt",
            beschreibung=e.beschreibung,
        )
        if e.nr == "M8"
        else e
        for e in Annahmen().eintraege()
    )
    a._pruefung = PruefErgebnis(
        pruefungen=synth_pruefung().pruefungen, annahmen=bestaetigt, sha256="a" * 64
    )
    a.btn_ansicht[2].click()
    a.liste_punkte.setCurrentRow(1)
    a.auswahl_frf.chk_phase.setChecked(True)
    assert not [t for t in texte(a) if "unbestätigt" in t]


def test_mittel_hat_phasen_platzhalter(baue: Bauer, qtbot: QtBot) -> None:
    a = geladen_mit(baue, qtbot)
    a.btn_ansicht[2].click()
    a.auswahl_frf.chk_phase.setChecked(True)  # Auswahl: Mittel
    assert any("für das Mittel nicht definiert" in t for t in texte(a))
    assert "phase" not in a.plot.zeichnung.linien  # type: ignore[union-attr]


def test_ui_6_ohne_referenz_text_statt_plot_und_ansicht_1_bleibt_nutzbar(
    baue: Bauer, qtbot: QtBot
) -> None:
    a = geladen_mit(baue, qtbot, referenz=False)
    assert a.combo_kanalpaar.count() == 0
    a.btn_ansicht[2].click()
    assert a.lbl_ansicht_platzhalter.text() == aa.TEXT_KEINE_FRF
    assert a._ae_stapel.currentWidget() is a._ae_stapel.widget(2)
    assert a.lbl_ansicht_platzhalter.isVisible()
    a.btn_ansicht[1].click()
    assert a._ae_stapel.currentWidget() is a._plot_seite
    assert len(linien(a)) == 4 and a.btn_ansicht[1].isEnabled()


# --- Ansicht 3 (UI-7, UI-8, UI-24) --------------------------------------------------------------


def test_ui_7_spitzentabelle_stimmt_mit_dem_kern_ueberein(baue: Bauer, qtbot: QtBot) -> None:
    a = geladen_mit(baue, qtbot)
    a.btn_ansicht[3].click()
    pa = a._cache.paar("Vib X", "Ref1")  # type: ignore[union-attr]
    kern = pa.spitzen.spitzen
    assert a.tabelle_spitzen.zeilenzahl() == len(kern) == 1
    zeile = a.tabelle_spitzen.modell.zeile(0)
    s = kern[0]
    assert zeile.zellen[0] == "1" and zeile.zellen[1] == "16,000"
    assert zeile.sortwerte[2] == s.zeta and zeile.zellen[2] == "0,12"  # ζ, 2 signifikante Stellen
    assert (zeile.sortwerte[3], zeile.sortwerte[4]) == (s.f_l_hz, s.f_r_hz)
    assert zeile.zellen[5] == "-3dB-Breite"
    kopf = [
        a.tabelle_spitzen.modell.headerData(i, Qt.Orientation.Horizontal)
        for i in range(a.tabelle_spitzen.modell.columnCount())
    ]
    assert kopf[:6] == ["Nr", "f_sp [Hz]", "ζ", "band_u_hz [Hz]", "band_o_hz [Hz]", "Methode"]
    assert a.tabelle_spitzen.currentIndex() == 1  # Tabelle statt Platzhalter
    assert a.tabelle_spitzen.tabelle.verticalHeader().defaultSectionSize() == 32


def test_ui_7_baendertabelle_zeigt_das_gesamtband_mit_rms_und_einheit(
    baue: Bauer, qtbot: QtBot
) -> None:
    a = geladen_mit(baue, qtbot)
    a.btn_ansicht[3].click()
    modell = a.tabelle_baender.modell
    assert modell.columnCount() == 5 and modell.rowCount() >= 1
    erste = modell.zeile(0)
    assert erste.zellen[:3] == ("1", "0,500", "32,000")  # Gesamtband über die ganze Achse (F-1)
    assert erste.zellen[3].endswith("m/s") and "Betragsmittel" in erste.zellen[4]


def test_ui_8_klick_auf_zeile_markiert_spitze_im_plot_und_zeigt_die_angaben(
    baue: Bauer, qtbot: QtBot
) -> None:
    a = geladen_mit(baue, qtbot)
    a.btn_ansicht[3].click()
    z0 = a.plot.zeichnung
    assert z0 is not None and "gewaehlt" not in z0.marker
    ylim_vorher = z0.achsen[0].get_ylim()
    assert z0.marker["spitzen"] is not None
    a.tabelle_spitzen.tabelle.selectRow(0)
    z = a.plot.zeichnung
    assert z is not None and "gewaehlt" in z.marker
    angaben = a.auswahl_spitzen.lbl_angaben.text()  # f, ζ, Methode, Band stehen in der Spalte
    assert "ζ ≈ 0,12" in angaben and "f = 16,000 Hz" in angaben and "-3dB-Breite" in angaben
    assert z.achsen[0].get_ylim() == pytest.approx(ylim_vorher)  # y-Skala springt nicht (L3-3)
    assert a.tabelle_spitzen.gewaehlter_schluessel() == 0


def test_ui_8_baender_sind_schattierte_flaechen_und_kurve_bleibt_sichtbar(
    baue: Bauer, qtbot: QtBot
) -> None:
    a = geladen_mit(baue, qtbot)
    a.btn_ansicht[3].click()
    z = a.plot.zeichnung
    assert z is not None and len(z.hilfsobjekte["baender"]) == 1
    assert z.linien["kurve"].get_zorder() > z.hilfsobjekte["baender"][0].get_zorder()


def test_ui_24_keine_spitzen_gefunden(baue: Bauer, qtbot: QtBot) -> None:
    a = geladen_mit(baue, qtbot, resonanz=False)
    a.btn_ansicht[3].click()
    assert a.tabelle_spitzen.currentIndex() == 0
    assert a.tabelle_spitzen.leer.text() == "Keine Spitzen gefunden."
    assert a.tabelle_spitzen.leer.isVisible()
    assert a.tabelle_baender.currentIndex() == 1  # Bänder bleiben vorhanden


def test_ui_24_ohne_referenz_keine_spitzensuche_aber_band_rms(baue: Bauer, qtbot: QtBot) -> None:
    a = geladen_mit(baue, qtbot, referenz=False)
    a.btn_ansicht[3].click()
    assert a.tabelle_spitzen.leer.text() == "Keine Spitzensuche: Referenzkanal fehlt."
    assert a.tabelle_spitzen.currentIndex() == 0
    assert a.tabelle_baender.zeilenzahl() == 3  # Vib X, Y, Z: vorhandene Band-RMS
    assert "kurve" in a.plot.zeichnung.linien  # type: ignore[union-attr]
    assert "spitzen" not in a.plot.zeichnung.marker  # type: ignore[union-attr]


def test_ansicht_3_ohne_referenz_keine_aufforderung_zur_spitzenwahl(
    baue: Bauer, qtbot: QtBot
) -> None:
    a = geladen_mit(baue, qtbot, referenz=False)
    a.btn_ansicht[3].click()
    assert a.tabelle_spitzen.leer.text() == "Keine Spitzensuche: Referenzkanal fehlt."
    assert a.auswahl_spitzen.lbl_angaben.text() == ""  # keine Spitze, also keine Wahl-Aufforderung


def test_ansicht_3_ohne_spitzen_keine_aufforderung_zur_spitzenwahl(
    baue: Bauer, qtbot: QtBot
) -> None:
    a = geladen_mit(baue, qtbot, resonanz=False)
    a.btn_ansicht[3].click()
    assert a.tabelle_spitzen.leer.text() == "Keine Spitzen gefunden."
    assert a.auswahl_spitzen.lbl_angaben.text() == ""


def test_ui_24_keine_baender_angegeben(baue: Bauer, qtbot: QtBot) -> None:
    a = geladen_mit(baue, qtbot)
    a.tabelle_baender.setze([], aa.TEXT_KEINE_BAENDER)
    assert a.tabelle_baender.currentIndex() == 0
    assert a.tabelle_baender.leer.text() == "Keine Bänder angegeben."


def test_unvollstaendige_spitze_wird_nicht_angezeigt_sondern_gemeldet(
    baue: Bauer, qtbot: QtBot, monkeypatch: pytest.MonkeyPatch
) -> None:
    import math
    from dataclasses import replace

    original = daten_auswerten.spitzen_zeilen

    def kaputt(spitzen: Any, **kw: Any) -> Any:
        return original([replace(s, f_r_hz=math.nan) for s in spitzen], **kw)

    monkeypatch.setattr(auswerten_reiter, "spitzen_zeilen", kaputt)
    a = geladen_mit(baue, qtbot)
    a.btn_ansicht[3].click()
    assert a.tabelle_spitzen.zeilenzahl() == 0
    assert "ζ ohne Bandgrenzen" in a.auswahl_spitzen.lbl_fehler.text()
    assert not a.auswahl_spitzen.lbl_fehler.isHidden()


def test_sortieren_per_spaltenkopf(baue: Bauer, qtbot: QtBot) -> None:
    a = geladen_mit(baue, qtbot, referenz=False)
    a.btn_ansicht[3].click()
    tabelle = a.tabelle_baender.tabelle
    tabelle.sortByColumn(3, Qt.SortOrder.DescendingOrder)
    werte = [
        tabelle.model().data(tabelle.model().index(r, 3), Qt.ItemDataRole.UserRole)
        for r in range(tabelle.model().rowCount())
    ]
    assert werte == sorted(werte, reverse=True)


# --- Ansicht 4 (UI-9, UI-10, UI-24) --------------------------------------------------------------


def test_ui_9_ansicht_4_voreinstellungen_und_naechste_linie(baue: Bauer, qtbot: QtBot) -> None:
    a = geladen_mit(baue, qtbot)
    a.btn_ansicht[4].click()
    sel = a.auswahl_sf
    assert sel.ebene() == "xy"  # waehle_ebene: z hat die kleinste Ausdehnung
    assert sel.komponente() == "3D" and sel.darstellung() == "betrag"
    assert sel.frequenz_hz() == pytest.approx(16.0)  # Spitze mit größter Höhe des Paars
    assert sel.lbl_naechste_linie.text() == "nächste Linie: 16,000 Hz"
    assert sel.feld_frequenz.singleStep() == pytest.approx(0.5)  # Δf der Datei
    z = a.plot.zeichnung
    assert z is not None and "punkte" in z.marker
    assert a.plot.canvas.accessibleName() == "Diagramm: Schwingform"
    assert z.achsen[0].get_xlabel() == "x [m]" and z.achsen[0].get_ylabel() == "y [m]"


def test_ui_9_frequenz_rastet_ein_und_zeichnet_neu(baue: Bauer, qtbot: QtBot) -> None:
    a = geladen_mit(baue, qtbot)
    a.btn_ansicht[4].click()
    sel = a.auswahl_sf
    zeichnung = a.plot.zeichnung
    sel.feld_frequenz.setValue(10.2)
    assert sel.lbl_naechste_linie.text() == "nächste Linie: 10,000 Hz"
    assert a.plot.zeichnung is not zeichnung
    assert "10,000 Hz" in a.lbl_plotkopf.text()


def test_ui_9_ui_24_eingabe_ausserhalb_meldung_und_plot_unveraendert(
    baue: Bauer, qtbot: QtBot
) -> None:
    a = geladen_mit(baue, qtbot)
    a.btn_ansicht[4].click()
    sel = a.auswahl_sf
    zeichnung = a.plot.zeichnung
    sel.feld_frequenz.setValue(100.0)
    assert sel.lbl_frequenz_fehler.text() == "✖ Frequenz 100 Hz liegt außerhalb 0,5 … 32 Hz."
    assert not sel.lbl_frequenz_fehler.isHidden()
    assert sel.lbl_naechste_linie.text() == ""
    assert a.plot.zeichnung is zeichnung  # Plot unverändert
    sel.feld_frequenz.setValue(20.0)  # gültig: Meldung weg
    assert sel.lbl_frequenz_fehler.isHidden()
    assert sel.lbl_naechste_linie.text() == "nächste Linie: 20,000 Hz"


def test_schnellwahl_spitze_setzt_die_frequenz(baue: Bauer, qtbot: QtBot) -> None:
    a = geladen_mit(baue, qtbot)
    a.btn_ansicht[4].click()
    sel = a.auswahl_sf
    sel.feld_frequenz.setValue(5.0)
    assert sel.combo_spitze.count() == 2 and sel.combo_spitze.itemText(1).startswith("Nr 1 · 16,0")
    sel.combo_spitze.activated.emit(1)
    assert sel.frequenz_hz() == pytest.approx(16.0)
    assert sel.combo_spitze.currentIndex() == 0  # zurück auf „Spitze …“
    assert sel.lbl_naechste_linie.text() == "nächste Linie: 16,000 Hz"


def test_schnellwahl_ohne_spitzen(baue: Bauer, qtbot: QtBot) -> None:
    a = geladen_mit(baue, qtbot, resonanz=False)
    a.btn_ansicht[4].click()
    assert a.auswahl_sf.combo_spitze.itemText(0) == "Keine Spitzen"
    assert not a.auswahl_sf.combo_spitze.isEnabled()
    assert a.auswahl_sf.frequenz_hz() == pytest.approx(0.5)  # erste Linie der Datei


def test_projektionsebene_wechselt_die_achsen(baue: Bauer, qtbot: QtBot) -> None:
    a = geladen_mit(baue, qtbot)
    a.btn_ansicht[4].click()
    a.auswahl_sf.rb_ebene["xz"].setChecked(True)
    z = a.plot.zeichnung
    assert z is not None and z.achsen[0].get_ylabel() == "z [m]"


def test_ui_10_phase_nicht_voreingestellt_gesperrt_bei_3d_mit_grund(
    baue: Bauer, qtbot: QtBot
) -> None:
    a = geladen_mit(baue, qtbot)
    a.btn_ansicht[4].click()
    sel = a.auswahl_sf
    assert sel.rb_groesse_betrag.isChecked()
    assert not sel.rb_groesse_phase_ref.isEnabled() and not sel.rb_groesse_phase_relativ.isEnabled()
    assert sel.lbl_phase_grund.text() == aa.TEXT_PHASE_EINZELKOMPONENTE
    assert sel.rb_groesse_phase_ref.toolTip() == aa.TEXT_PHASE_EINZELKOMPONENTE
    sel.rb_komp["Z"].setChecked(True)
    assert sel.rb_groesse_phase_ref.isEnabled() and sel.lbl_phase_grund.isHidden()
    assert sel.rb_groesse_betrag.isChecked()  # auch jetzt nie Voreinstellung


def test_ui_10_option_phase_gegen_referenz_traegt_unbestaetigt_und_nr(
    baue: Bauer, qtbot: QtBot
) -> None:
    a = geladen_mit(baue, qtbot)
    a.btn_ansicht[4].click()
    sel = a.auswahl_sf
    assert sel.rb_groesse_phase_ref.accessibleName() == "Phase gegen Ref1 (⚠ unbestätigt, M8)"
    assert sel.rb_groesse_phase_ref.text() == "Phase gegen Ref1\n(⚠ unbestätigt, M8)"
    sel.rb_komp["Z"].setChecked(True)
    sel.rb_groesse_phase_ref.setChecked(True)
    z = a.plot.zeichnung
    assert z is not None
    kennzeichen = [t for t in z.alle_texte() if "unbestätigt" in t]
    assert kennzeichen and "M8" in kennzeichen[0]
    assert "Phase gegen Ref1" in a.lbl_plotkopf.text()


def test_phase_relativ_ist_m8_unabhaengig_ohne_kennzeichen_und_bezug_voreingestellt(
    baue: Bauer, qtbot: QtBot
) -> None:
    a = geladen_mit(baue, qtbot)
    a.btn_ansicht[4].click()
    sel = a.auswahl_sf
    sel.rb_komp["Z"].setChecked(True)
    sel.rb_groesse_phase_relativ.setChecked(True)
    z = a.plot.zeichnung
    assert z is not None and not [t for t in z.alle_texte() if "unbestätigt" in t]
    assert sel.bezug() is None and sel.combo_bezug.itemText(0).startswith("Automatisch (Punkt ")
    assert sel.combo_bezug.count() == 5  # automatisch plus vier Punkte
    sel.combo_bezug.setCurrentIndex(2)  # Punkt 11 als Bezug
    assert sel.bezug() == 1
    assert any("Punkt 11" in t for t in a.plot.zeichnung.alle_texte())  # type: ignore[union-attr]


def test_ui_10_ohne_referenz_phase_gesperrt_und_text_im_plotkopf(baue: Bauer, qtbot: QtBot) -> None:
    a = geladen_mit(baue, qtbot, referenz=False)
    a.btn_ansicht[4].click()
    sel = a.auswahl_sf
    sel.rb_komp["Z"].setChecked(True)
    assert not sel.rb_groesse_phase_ref.isEnabled()
    assert sel.lbl_phase_grund.text() == "Phase nicht verfügbar: keine Referenz."
    assert "Phase nicht verfügbar: keine Referenz." in a.lbl_plotkopf.text()
    assert a.plot.zeichnung is not None  # nur Betrag


def test_spitzen_kennzeichen_der_linie_liefern_den_sprung_hinweis(
    baue: Bauer, qtbot: QtBot, monkeypatch: pytest.MonkeyPatch
) -> None:
    from dataclasses import replace

    original = daten_auswerten.spitze_der_linie

    def mit_kennzeichen(spitzen: Any, linie: int) -> Any:
        s = original(spitzen, linie)
        return replace(s, kennzeichen=("aufloesungsbegrenzt",)) if s is not None else None

    monkeypatch.setattr(auswerten_reiter, "spitze_der_linie", mit_kennzeichen)
    a = geladen_mit(baue, qtbot)
    a.btn_ansicht[4].click()
    sel = a.auswahl_sf
    assert sel.frequenz_hz() == pytest.approx(16.0)  # Linie der Spitze
    assert HINWEIS_PHASE_SPRUNG not in a.auswahl_sf.lbl_hinweise.text()  # Betrag: kein Hinweis
    sel.rb_komp["Z"].setChecked(True)
    sel.rb_groesse_phase_relativ.setChecked(True)
    assert HINWEIS_PHASE_SPRUNG in sel.lbl_hinweise.text()
    sel.feld_frequenz.setValue(5.0)  # Linie ohne Spitze: kein Hinweis
    assert HINWEIS_PHASE_SPRUNG not in sel.lbl_hinweise.text()


def test_alle_hinweise_der_zeichnung_sind_sichtbar(baue: Bauer, qtbot: QtBot) -> None:
    a = geladen_mit(baue, qtbot)
    for nr, seite in ((2, a.auswahl_frf), (3, a.auswahl_spitzen), (4, a.auswahl_sf)):
        a.btn_ansicht[nr].click()
        z = a.plot.zeichnung
        assert z is not None
        if nr == 2:
            a.liste_punkte.setCurrentRow(1)
            a.auswahl_frf.chk_phase.setChecked(True)
            z = a.plot.zeichnung
            assert z is not None
        if z.hinweise:
            assert seite.lbl_hinweise.text() == "\n".join(z.hinweise)
            assert not seite.lbl_hinweise.isHidden()
    a.btn_ansicht[3].click()
    assert "ζ aus der" in a.auswahl_spitzen.lbl_hinweise.text()  # HINWEIS_ZETA


# --- Zoom je Ansicht, Dateiwechsel, Fokus ----------------------------------------------------


def test_zoom_je_ansicht_bleibt_beim_ansichtswechsel_erhalten(baue: Bauer, qtbot: QtBot) -> None:
    a = geladen_mit(baue, qtbot)
    a.plot.zeichnung.achsen[0].set_xlim(5.0, 10.0)  # type: ignore[union-attr]
    a.btn_ansicht[2].click()
    assert a.plot.zeichnung.achsen[0].get_xlim() == pytest.approx((0.5, 32.0))  # type: ignore[union-attr]
    a.plot.zeichnung.achsen[0].set_xlim(20.0, 30.0)  # type: ignore[union-attr]
    a.btn_ansicht[1].click()
    assert a.plot.zeichnung.achsen[0].get_xlim() == pytest.approx((5.0, 10.0))  # type: ignore[union-attr]
    a.btn_ansicht[2].click()
    assert a.plot.zeichnung.achsen[0].get_xlim() == pytest.approx((20.0, 30.0))  # type: ignore[union-attr]
    a.plot.zoom_zuruecksetzen()
    assert a.plot.zeichnung.achsen[0].get_xlim() == pytest.approx((0.5, 32.0))  # type: ignore[union-attr]


def test_neuer_dateiaufruf_setzt_zoom_und_ansicht_zurueck(baue: Bauer, qtbot: QtBot) -> None:
    a = geladen_mit(baue, qtbot)
    a.plot.zeichnung.achsen[0].set_xlim(5.0, 10.0)  # type: ignore[union-attr]
    a.btn_ansicht[3].click()
    a.btn_ansicht[1].click()
    lade(qtbot, a.window(), "C:\\messungen\\zweite.svd")  # type: ignore[arg-type]
    assert a.ansicht == 1 and a.btn_ansicht[1].isChecked() and a._ad_stapel.currentIndex() == 0
    assert a.plot.zeichnung.achsen[0].get_xlim() == pytest.approx((0.5, 32.0))  # type: ignore[union-attr]
    assert a.auswahl_frf.chk_h1.isChecked() and not a.auswahl_frf.chk_phase.isChecked()
    assert a.auswahl_sf.komponente() == "3D" and a.auswahl_sf.darstellung() == "betrag"


@pytest.mark.parametrize("nr", [2, 3, 4])
def test_ui_21_alle_bedienelemente_der_ansicht_sind_fokussierbar(
    baue: Bauer, qtbot: QtBot, nr: int
) -> None:
    a = geladen_mit(baue, qtbot, mit_ref2=True)
    a.btn_ansicht[nr].click()
    QApplication.processEvents()
    for b in a.findChildren(QAbstractButton):
        if b.isVisible() and b.isEnabled():
            assert b.focusPolicy() != Qt.FocusPolicy.NoFocus, b.objectName()
    for wid in (a.auswahl_sf.feld_frequenz, a.combo_kanalpaar, a.combo_kanalpaar):
        assert wid.focusPolicy() != Qt.FocusPolicy.NoFocus
    for t in (a.tabelle_spitzen.tabelle, a.tabelle_baender.tabelle):
        assert t.focusPolicy() != Qt.FocusPolicy.NoFocus


def test_tab_halt_der_ansicht_4_radiogruppen_liegt_auf_der_gewaehlten_option(
    baue: Bauer, qtbot: QtBot
) -> None:
    a = geladen_mit(baue, qtbot)
    a.btn_ansicht[4].click()
    sel = a.auswahl_sf
    assert sel.rb_komp["3D"].focusPolicy() == Qt.FocusPolicy.StrongFocus
    assert sel.rb_komp["X"].focusPolicy() == Qt.FocusPolicy.ClickFocus
    sel.rb_komp["Y"].setChecked(True)
    assert sel.rb_komp["Y"].focusPolicy() == Qt.FocusPolicy.StrongFocus
    assert sel.rb_komp["3D"].focusPolicy() == Qt.FocusPolicy.ClickFocus
    assert sel.rb_ebene["xy"].focusPolicy() == Qt.FocusPolicy.StrongFocus


def test_ad_seite_misst_nur_die_aktuelle_ansicht(baue: Bauer, qtbot: QtBot) -> None:
    a = geladen_mit(baue, qtbot)
    a.btn_ansicht[2].click()
    assert a._ad_stapel.sizeHint().height() <= a.auswahl_frf.sizeHint().height() + 2


# --- Rückfallpfad (Plus aus RR-AUSW-T3a-2) ---------------------------------------------------


def test_oeffne_datei_mit_dauerhaft_fehlerhaftem_zustand_haengt_nicht_in_laden(
    baue: Bauer, qtbot: QtBot, monkeypatch: pytest.MonkeyPatch, caplog: pytest.LogCaptureFixture
) -> None:
    ausf = SteuerbarerAusfuehrer()
    w, _ = baue(ausf)
    a = w.auswerten
    assert a is not None

    def kaputt() -> None:
        raise RuntimeError("Zustand kaputt")

    monkeypatch.setattr(a, "_wende_zustand_an", kaputt)
    with caplog.at_level(logging.WARNING, logger=auswerten_reiter.__name__):
        a.oeffne_datei(PFAD)  # darf nicht werfen
    assert a.zustand is aa.AuswertenZustand.KEINE_DATEI  # kein hängendes „Laden“
    assert ausf.auftraege == [] and not a.laeuft() and not a._timer.isActive()
    assert a.fehlertext is not None and "Zustand kaputt" in a.fehlertext
    assert not a.laden_leiste.isVisible() and a.band_fehler.isVisible()
    assert "Rückfall im Reiter Auswerten" in caplog.text  # Folgefehler im Protokoll


def test_folgefehler_im_rueckfall_stehen_in_der_fehlermeldung_und_im_protokoll(
    baue: Bauer, qtbot: QtBot, monkeypatch: pytest.MonkeyPatch, caplog: pytest.LogCaptureFixture
) -> None:
    w, _ = baue()
    a = w.auswerten
    assert a is not None

    def kaputt(*_a: object, **_k: object) -> None:
        raise ValueError("Zeile kaputt")

    monkeypatch.setattr(a.parameterzeile, "setze_zellen", kaputt)  # dauerhaft, auch im Rückfall
    with caplog.at_level(logging.WARNING, logger=auswerten_reiter.__name__):
        a.oeffne_datei(PFAD)
        qtbot.waitUntil(lambda: a.fehlertext is not None, timeout=3000)
    assert a.zustand is aa.AuswertenZustand.KEINE_DATEI and not a._timer.isActive()
    text = a.lbl_fehler.text()
    assert "Anzeige nicht möglich: Zeile kaputt" in text  # auslösender Fehler
    assert "Folgefehler im Rückfall: Parameterzeile: Zeile kaputt" in text  # nicht spurlos
    assert "Parameterzeile" in caplog.text and "Traceback" in caplog.text


def test_ohne_folgefehler_kein_anhang(baue: Bauer, qtbot: QtBot) -> None:
    w, prot = baue()
    a = w.auswerten
    assert a is not None
    prot.fehler_lese[PFAD] = f"{PFAD}: kaputt"
    a.oeffne_datei(PFAD)
    qtbot.waitUntil(lambda: a.fehlertext is not None, timeout=3000)
    assert "Folgefehler" not in a.lbl_fehler.text()


def test_nie_fertiger_ausfuehrer_ansicht_wechsel_bleibt_bedienbar(baue: Bauer) -> None:
    w, _ = baue(NieFertigAusfuehrer())
    a = w.auswerten
    assert a is not None
    a.btn_ansicht[2].click()  # ohne Datei gesperrt: nichts geschieht
    assert a.ansicht == 1


def test_direkt_ausfuehrer_typ_wird_importiert() -> None:
    assert DirektAusfuehrer is not None and AttrappenSitzung is not None and bild is not None


# --- K-AUSW-T3b: Wechsel, Splitter, Kennzeichen, Kanalpaar, Segmentzeilen -------------------------


def test_nach_ungueltiger_frequenz_zeigt_der_wechsel_zurueck_keinen_fremden_inhalt(
    baue: Bauer, qtbot: QtBot
) -> None:
    a = geladen_mit(baue, qtbot)
    a.btn_ansicht[4].click()
    sel = a.auswahl_sf
    gueltig = a.lbl_plotkopf.text()
    assert "Linie 16,000 Hz" in gueltig and a._plot_ansicht == 4
    sel.feld_frequenz.setValue(5000.0)  # außerhalb: Plot bleibt Ansicht 4
    assert a._plot_ansicht == 4 and a.lbl_plotkopf.text() == gueltig
    a.btn_ansicht[3].click()
    assert a._plot_ansicht == 3 and a.plot.canvas.accessibleName() == "Diagramm: Spitzen und Bänder"
    a.btn_ansicht[4].click()  # Frequenz ist weiter ungültig
    assert a._plot_ansicht == 4
    assert a.plot.canvas.accessibleName() == "Diagramm: Schwingform"  # nie der Plot von Ansicht 3
    assert a.lbl_plotkopf.text() == gueltig  # letzter gültiger Stand von Ansicht 4, kein Fremdkopf
    assert "5000 Hz liegt außerhalb" in sel.lbl_frequenz_fehler.text()
    assert a._ae_stapel.currentWidget() is a._plot_seite
    sel.feld_frequenz.setValue(20.0)
    assert "Linie 20,000 Hz" in a.lbl_plotkopf.text()


def test_ohne_letzten_stand_steht_ein_platzhalter_statt_fremdem_inhalt(
    baue: Bauer, qtbot: QtBot, monkeypatch: pytest.MonkeyPatch
) -> None:
    from ldv_automation.darstellung.auswahl import DarstellungsFehler

    a = geladen_mit(baue, qtbot)  # zeigt Ansicht 1
    assert a._plot_ansicht == 1 and "Spektrum" in a.plot.canvas.accessibleName()

    def kaputt(*_a: object, **_k: object) -> None:
        raise DarstellungsFehler("Linie nicht darstellbar")

    monkeypatch.setattr(auswerten_reiter, "schwingform_daten", kaputt)
    a.btn_ansicht[4].click()  # erstes Zeichnen von Ansicht 4 scheitert
    assert a._plot_ansicht is None and a.plot.zeichnung is None
    assert a.lbl_ansicht_platzhalter.text() == "Linie nicht darstellbar"
    assert a._ae_stapel.currentWidget() is not a._plot_seite
    assert a.lbl_plotkopf.text() == ""  # kein Kopf der vorigen Ansicht
    assert "Linie nicht darstellbar" in a.lbl_cursor.text()


def test_darstellungsfehler_in_ansicht_2_zeigt_nie_den_plot_von_ansicht_1(
    baue: Bauer, qtbot: QtBot, monkeypatch: pytest.MonkeyPatch
) -> None:
    from ldv_automation.darstellung.auswahl import DarstellungsFehler

    a = geladen_mit(baue, qtbot)

    def kaputt(*_a: object, **_k: object) -> None:
        raise DarstellungsFehler("kein Kreuzspektrum")

    monkeypatch.setattr(auswerten_reiter, "frf_daten", kaputt)
    a.btn_ansicht[2].click()
    assert a.lbl_ansicht_platzhalter.text() == "kein Kreuzspektrum" and a.plot.zeichnung is None


def test_splitterposition_wird_je_sitzung_gemerkt(baue: Bauer, qtbot: QtBot) -> None:
    a = geladen_mit(baue, qtbot)
    a.btn_ansicht[3].click()
    QApplication.processEvents()
    gesamt = sum(a._plot_seite.sizes())
    a._plot_seite.setSizes([gesamt - 200, 200])
    a._splitter_bewegt(0, 1)  # wie nach dem Ziehen mit der Maus
    a.btn_ansicht[1].click()
    a.btn_ansicht[3].click()
    QApplication.processEvents()
    assert abs(a._plot_seite.sizes()[1] - 200) <= 2


def test_splitter_laesst_dem_plot_mindesthoehe(baue: Bauer, qtbot: QtBot) -> None:
    a = geladen_mit(baue, qtbot)
    a._tabellen_hoehe = 10_000  # unsinnig groß gemerkt
    a.btn_ansicht[3].click()
    QApplication.processEvents()
    assert a._plot_seite.sizes()[0] >= auswerten_reiter.PLOT_MIN_HOEHE_SPLITTER_PX


def test_ui_10_plotkopf_nennt_phase_unbestaetigt_nur_bei_phase_gegen_referenz(
    baue: Bauer, qtbot: QtBot
) -> None:
    a = geladen_mit(baue, qtbot)
    a.btn_ansicht[4].click()
    sel = a.auswahl_sf
    assert "Phase unbestätigt" not in a.lbl_plotkopf.text()  # Betrag
    sel.rb_komp["Z"].setChecked(True)
    sel.rb_groesse_phase_ref.setChecked(True)
    assert a.lbl_plotkopf.text().endswith("Phase gegen Ref1 · ⚠ Phase unbestätigt")
    sel.rb_groesse_phase_relativ.setChecked(True)  # M8-unabhängig
    assert "unbestätigt" not in a.lbl_plotkopf.text()


def test_ui_10_kein_kennzeichen_im_plotkopf_wenn_m8_bestaetigt(baue: Bauer, qtbot: QtBot) -> None:
    a = geladen_mit(baue, qtbot)
    bestaetigt = tuple(
        type(e)(
            nr=e.nr,
            parameter=e.parameter,
            wert=e.wert,
            status="bestätigt",
            beschreibung=e.beschreibung,
        )
        if e.nr == "M8"
        else e
        for e in Annahmen().eintraege()
    )
    a._pruefung = PruefErgebnis(
        pruefungen=synth_pruefung().pruefungen, annahmen=bestaetigt, sha256="a" * 64
    )
    a.btn_ansicht[4].click()
    a._kennzeichen_aktualisieren()
    sel = a.auswahl_sf
    sel.rb_komp["Z"].setChecked(True)
    sel.rb_groesse_phase_ref.setChecked(True)
    assert "unbestätigt" not in a.lbl_plotkopf.text()
    assert (
        sel.rb_groesse_phase_ref.text() == "Phase gegen Ref1"
        and sel.rb_groesse_phase_ref.toolTip() == ""
    )


def test_phase_option_erklaert_die_annahme_im_tooltip(baue: Bauer, qtbot: QtBot) -> None:
    a = geladen_mit(baue, qtbot)
    m8 = next(e for e in Annahmen().eintraege() if e.nr == "M8")
    a.btn_ansicht[4].click()
    a.auswahl_sf.rb_komp["Z"].setChecked(True)
    assert m8.beschreibung in a.auswahl_sf.rb_groesse_phase_ref.toolTip()
    assert m8.beschreibung in a.auswahl_frf.chk_phase.toolTip()


def test_ansicht_4_kasten_in_kopfzeile_innerhalb_der_figure(baue: Bauer, qtbot: QtBot) -> None:
    a = geladen_mit(baue, qtbot)
    a.btn_ansicht[4].click()
    a.auswahl_sf.rb_komp["Z"].setChecked(True)
    a.auswahl_sf.rb_groesse_phase_ref.setChecked(True)
    z = a.plot.zeichnung
    assert z is not None
    z.figure.draw_without_rendering()
    kasten = [t for t in z.texte if "unbestätigt" in t.get_text()]
    assert (
        kasten and kasten[0].get_text() == "⚠ unbestätigt (M8: Polarität der Referenzkanäle offen)"
    )
    box = kasten[0].get_window_extent()
    assert z.figure.bbox.x0 <= box.x0 and box.x1 <= z.figure.bbox.x1 and box.y1 <= z.figure.bbox.y1
    assert box.y0 >= z.achsen[0].get_window_extent().y1 - 0.5  # oberhalb der Achse


def test_spitzentabelle_ist_standardmaessig_nach_nr_aufsteigend(baue: Bauer, qtbot: QtBot) -> None:
    from ldv_automation.gui.daten_auswerten import TabellenZeile

    a = geladen_mit(baue, qtbot)
    zeilen = [TabellenZeile((str(n), *["x"] * 6), (float(n), *["x"] * 6), n - 1) for n in (3, 1, 2)]
    a.tabelle_spitzen.setze(zeilen, "leer")
    tabelle = a.tabelle_spitzen.tabelle
    modell = tabelle.model()
    assert [modell.index(r, 0).data() for r in range(3)] == ["1", "2", "3"]
    kopf = tabelle.horizontalHeader()
    assert (
        kopf.sortIndicatorSection() == 0
        and kopf.sortIndicatorOrder() == Qt.SortOrder.AscendingOrder
    )


def test_baendertabelle_bezug_in_klartext(baue: Bauer, qtbot: QtBot) -> None:
    a = geladen_mit(baue, qtbot)
    a.btn_ansicht[3].click()
    bezuege = [
        a.tabelle_baender.modell.zeile(r).zellen[4] for r in range(a.tabelle_baender.zeilenzahl())
    ]
    assert "kohärentes Spektrum Vib X/Ref1 (Betragsmittel)" in bezuege
    assert "Leistungsmittel Vib X (Punktmittel)" in bezuege
    assert not any("spektrum_kohaerent" in b or b.startswith("AP ") for b in bezuege)


def test_a3_schluessel_wird_erst_nach_erfolgreichem_fuellen_gesetzt(
    baue: Bauer, qtbot: QtBot, monkeypatch: pytest.MonkeyPatch
) -> None:
    original = daten_auswerten.bandwerte_fuer
    aufrufe = {"n": 0}

    def einmal_kaputt(*args: Any, **kw: Any) -> Any:
        aufrufe["n"] += 1
        if aufrufe["n"] == 1:
            raise ValueError("Bänder kaputt")
        return original(*args, **kw)

    monkeypatch.setattr(auswerten_reiter, "bandwerte_fuer", einmal_kaputt)
    a = geladen_mit(baue, qtbot)
    a.btn_ansicht[3].click()  # erster Versuch scheitert, Fehlerband
    assert a.fehlertext is not None and "Bänder kaputt" in a.fehlertext
    assert a._a3_schluessel is None  # nicht als „gefüllt“ gemerkt
    a.btn_ansicht[1].click()
    a.btn_ansicht[3].click()  # zweiter Versuch füllt beide Tabellen
    assert a.tabelle_baender.zeilenzahl() >= 1 and a.tabelle_spitzen.zeilenzahl() == 1
    assert a._a3_schluessel is not None


def test_kanalpaar_in_ansicht_4_sichtbar_und_passend_zur_komponente(
    baue: Bauer, qtbot: QtBot
) -> None:
    a = geladen_mit(baue, qtbot, mit_ref2=True)
    a.btn_ansicht[4].click()
    assert not a.kanalpaar_gruppe.isHidden() and a.lbl_kanalpaar_hinweis.text()
    assert a.combo_kanalpaar.itemText(a.combo_kanalpaar.currentIndex()) == "Vib X / Ref1"
    sel = a.auswahl_sf
    sel.rb_komp["Z"].setChecked(True)
    assert a.combo_kanalpaar.currentText() == "Vib Z / Ref1"  # passend zur Komponente
    assert a._paar() == ("Vib Z", "Ref1")
    sel.rb_komp["Y"].setChecked(True)
    assert a._paar() == ("Vib Y", "Ref1")
    sel.rb_komp["3D"].setChecked(True)
    assert a._paar() == ("Vib Y", "Ref1")  # bei 3D bleibt das gewählte Paar
    a.combo_kanalpaar.setCurrentIndex(3)  # bei 3D frei wählbar
    assert a._paar() == ("Ref2", "Ref1")
    assert a._a4_paar_schluessel == ("Ref2", "Ref1")


def test_spitzenliste_und_kennzeichen_stammen_aus_dem_gewaehlten_paar(
    baue: Bauer, qtbot: QtBot, monkeypatch: pytest.MonkeyPatch
) -> None:
    gesehen: list[Any] = []
    original = daten_auswerten.spitze_der_linie

    def merke(spitzen: Any, linie: int) -> Any:
        gesehen.append(tuple(spitzen))
        return original(spitzen, linie)

    monkeypatch.setattr(auswerten_reiter, "spitze_der_linie", merke)
    a = geladen_mit(baue, qtbot, mit_ref2=True)
    a.btn_ansicht[4].click()
    a.combo_kanalpaar.setCurrentIndex(3)  # Ref2 / Ref1
    assert a.auswahl_sf.combo_spitze.count() == 2  # Platzhalter und die Spitze dieses Paars
    erwartet = tuple(a._cache.paar("Ref2", "Ref1").spitzen.spitzen)  # type: ignore[union-attr]
    assert gesehen[-1] == erwartet
    a.auswahl_sf.rb_komp["Z"].setChecked(True)  # Komponente → Paar Vib Z / Ref1
    assert gesehen[-1] == tuple(a._cache.paar("Vib Z", "Ref1").spitzen.spitzen)  # type: ignore[union-attr]


def test_auswahlspalte_ansicht_4_passt_bei_1366_x_768_ohne_scrollen(
    baue: Bauer, qtbot: QtBot
) -> None:
    a = geladen_mit(baue, qtbot, mit_ref2=True)  # Kanalpaarwahl sichtbar: ungünstigster Fall
    a.btn_ansicht[4].click()
    for _ in range(3):
        QApplication.processEvents()
    assert a.auswahlspalte.verticalScrollBar().maximum() == 0
    assert a.auswahlspalte.horizontalScrollBar().maximum() == 0


def test_projektionsebene_und_komponente_sind_horizontale_segmentzeilen(
    baue: Bauer, qtbot: QtBot
) -> None:
    from PySide6.QtWidgets import QPushButton

    a = geladen_mit(baue, qtbot)
    a.btn_ansicht[4].click()
    QApplication.processEvents()
    sel = a.auswahl_sf
    for gruppe in (sel.rb_ebene, sel.rb_komp):
        knoepfe = list(gruppe.values())
        assert all(isinstance(k, QPushButton) and k.isCheckable() for k in knoepfe)
        ys = {k.mapTo(a, k.rect().topLeft()).y() for k in knoepfe}
        assert max(ys) - min(ys) <= 2  # alle in einer Zeile (Rahmen des markierten Knopfs)
        xs = [k.mapTo(a, k.rect().topLeft()).x() for k in knoepfe]
        assert xs == sorted(xs) and len(set(xs)) == len(xs)
    assert sum(k.isChecked() for k in sel.rb_ebene.values()) == 1
    assert sum(k.isChecked() for k in sel.rb_komp.values()) == 1
    assert sel.rb_komp["3D"].isChecked() and sel.rb_ebene["xy"].isChecked()


def test_bezugspunktwahl_nur_bei_phase_relativ_sichtbar(baue: Bauer, qtbot: QtBot) -> None:
    a = geladen_mit(baue, qtbot)
    a.btn_ansicht[4].click()
    sel = a.auswahl_sf
    assert sel.combo_bezug.isHidden() and sel.titel_bezug.isHidden()
    sel.rb_komp["Z"].setChecked(True)
    sel.rb_groesse_phase_relativ.setChecked(True)
    assert not sel.combo_bezug.isHidden()
    sel.rb_groesse_betrag.setChecked(True)
    assert sel.combo_bezug.isHidden()


def test_zeichenfehler_verwirft_den_zoom_nicht_nur_der_dateiwechsel(
    baue: Bauer, qtbot: QtBot, monkeypatch: pytest.MonkeyPatch
) -> None:
    a = geladen_mit(baue, qtbot)
    a.plot.zeichnung.achsen[0].set_xlim(5.0, 10.0)  # type: ignore[union-attr]
    a.btn_ansicht[2].click()
    a.plot.zeichnung.achsen[0].set_xlim(20.0, 30.0)  # type: ignore[union-attr]
    original = dar_auswahl.spektrum_daten
    zaehler = {"n": 0}

    def einmal_kaputt(*args: Any, **kw: Any) -> Any:
        zaehler["n"] += 1
        if zaehler["n"] == 1:
            raise ValueError("Zeichnen kaputt")
        return original(*args, **kw)

    monkeypatch.setattr(auswerten_reiter, "spektrum_daten", einmal_kaputt)
    a.btn_ansicht[1].click()  # Zeichenfehler: Fehlerband, Plot leer
    assert a.fehlertext is not None and a.plot.zeichnung is None
    a.schliesse_fehlerband()
    a.btn_ansicht[1].click()  # gelingt: der Zoom von Ansicht 1 ist noch da
    assert xlim(a) == pytest.approx((5.0, 10.0))
    a.btn_ansicht[2].click()
    assert xlim(a) == pytest.approx((20.0, 30.0))


def test_dateiwechsel_loescht_den_zoom_aller_ansichten(baue: Bauer, qtbot: QtBot) -> None:
    a = geladen_mit(baue, qtbot)
    a.plot.zeichnung.achsen[0].set_xlim(5.0, 10.0)  # type: ignore[union-attr]
    a.btn_ansicht[2].click()
    a.plot.zeichnung.achsen[0].set_xlim(20.0, 30.0)  # type: ignore[union-attr]
    a.btn_ansicht[1].click()
    lade(qtbot, a.window(), "C:\\messungen\\zweite.svd")  # type: ignore[arg-type]
    assert a.plot._zoom == {}
    a.btn_ansicht[2].click()
    assert a.plot.zeichnung.achsen[0].get_xlim() == pytest.approx((0.5, 32.0))  # type: ignore[union-attr]


# --- K-AUSW-T3b-2 ---------------------------------------------------------------


def test_rueckfall_in_ansicht_4_loescht_den_zoom_der_anderen_ansichten_nicht(
    baue: Bauer, qtbot: QtBot
) -> None:
    a = geladen_mit(baue, qtbot)
    a.btn_ansicht[2].click()
    a.plot.zeichnung.achsen[0].set_xlim(5.0, 10.0)  # type: ignore[union-attr]
    a.btn_ansicht[4].click()
    a.auswahl_sf.feld_frequenz.setValue(5000.0)  # außerhalb, Plot bleibt Ansicht 4
    a.btn_ansicht[1].click()
    a.btn_ansicht[4].click()  # Rückfall: letzter gültiger Stand von Ansicht 4
    assert a._plot_ansicht == 4 and "Linie 16,000 Hz" in a.lbl_plotkopf.text()
    a.btn_ansicht[2].click()
    assert xlim(a) == pytest.approx((5.0, 10.0))  # Zoom von Ansicht 2 ist erhalten (UI-12)


def test_ansicht_3_angaben_der_gewaehlten_spitze_als_textblock(baue: Bauer, qtbot: QtBot) -> None:
    a = geladen_mit(baue, qtbot)
    a.btn_ansicht[3].click()
    hinweis = a.auswahl_spitzen.lbl_angaben.text()
    assert "Tabelle" in hinweis and "wählen" in hinweis and "Angaben" in hinweis
    assert "Diagramm" not in hinweis  # Beschriftung steht nicht mehr im Diagramm
    a.tabelle_spitzen.tabelle.selectRow(0)
    text = a.auswahl_spitzen.lbl_angaben.text()
    s: Any = a._a3_spitzen[0]
    assert "f = 16,000 Hz" in text and "ζ ≈ 0,12" in text  # 2 signifikante Stellen
    assert "-3dB-Breite" in text  # Methode
    assert f"{s.f_l_hz:.3f}".replace(".", ",") in text and "… " in text  # Bandgrenzen
    assert text.count("\n") == 1  # f/ζ, Methode mit Band; keine Kennzeichen bei dieser Spitze


def test_ansicht_3_angaben_enthalten_alle_kennzeichen_und_bei_nan_keine_methode(
    baue: Bauer, qtbot: QtBot
) -> None:
    import math
    from dataclasses import replace

    from ldv_automation.auswertung.spitzen import Spitze
    from ldv_automation.gui.daten_auswerten import spitze_angaben_text

    a = geladen_mit(baue, qtbot)
    a.btn_ansicht[3].click()
    s = a._a3_spitzen[0]
    assert isinstance(s, Spitze)
    voll = spitze_angaben_text(
        replace(s, kennzeichen=("aufloesungsbegrenzt", "kohaerenz_niedrig")), warn_symbol="⚠"
    )
    assert voll.splitlines()[-1] == "⚠ auflösungsbegrenzt, Kohärenz niedrig"
    ohne = spitze_angaben_text(replace(s, zeta=math.nan, f_l_hz=math.nan, f_r_hz=math.nan))
    assert "ζ = –" in ohne and "-3dB" not in ohne  # kein Wert, keine Methode (R-055)
    assert spitze_angaben_text(None) == aa.TEXT_SPITZE_WAEHLEN


def test_ansicht_3_im_gui_plot_nur_der_ring_kein_kasten_und_kein_streifen(
    baue: Bauer, qtbot: QtBot
) -> None:
    a = geladen_mit(baue, qtbot)
    a.btn_ansicht[3].click()
    ohne_auswahl = a.plot.zeichnung
    assert ohne_auswahl is not None and "streifen" not in ohne_auswahl.hilfsobjekte
    ylim0 = ohne_auswahl.achsen[0].get_ylim()
    a.tabelle_spitzen.tabelle.selectRow(0)
    z = a.plot.zeichnung
    assert z is not None and "gewaehlt" in z.marker  # Ring um die gewählte Spitze
    assert "streifen" not in z.hilfsobjekte and "leitlinie" not in z.hilfsobjekte
    assert not [t for t in z.alle_texte() if "ζ" in t or "-3dB" in t]  # kein Kasten im Bild
    assert z.achsen[0].get_ylim() == pytest.approx(ylim0)  # y-Skala springt nicht


def test_thesis_variante_der_spitzen_behaelt_streifen_und_kasten(baue: Bauer, qtbot: QtBot) -> None:
    from matplotlib.figure import Figure

    from ldv_automation.darstellung.auswahl import spitzen_daten_frf
    from ldv_automation.darstellung.spitzen import SpitzenOptionen, zeichne_spitzen
    from ldv_automation.gui.plotstil import baue_plotstil

    a = geladen_mit(baue, qtbot)
    assert a._cache is not None
    sd = spitzen_daten_frf(a._cache, "Vib X", "Ref1", gewaehlt=0)
    assert SpitzenOptionen().beschriftung_im_bild  # Voreinstellung: wie bisher
    z = zeichne_spitzen(Figure(figsize=(12.0, 7.4)), sd, SpitzenOptionen(), baue_plotstil())
    assert "streifen" in z.hilfsobjekte and "leitlinie" in z.hilfsobjekte
    assert any("ζ ≈" in t for t in z.alle_texte())


def test_tabelle_ansicht_3_hat_vier_zeilen_standard_bei_1366_x_768(
    baue: Bauer, qtbot: QtBot
) -> None:
    a = geladen_mit(baue, qtbot)
    a.window().resize(1366, 768)
    a.btn_ansicht[3].click()
    qtbot.wait(40)
    t = a.tabelle_spitzen.tabelle
    assert auswerten_reiter.TABELLE_STANDARD_ZEILEN == 4
    assert t.viewport().height() // t.verticalHeader().defaultSectionSize() >= 4


def test_ansicht_3_legende_steht_im_text_und_nicht_im_gui_plot(baue: Bauer, qtbot: QtBot) -> None:
    a = geladen_mit(baue, qtbot)
    a.btn_ansicht[3].click()
    qtbot.wait(40)
    z = a.plot.zeichnung
    assert z is not None and "legende" not in z.hilfsobjekte
    assert z.achsen[0].get_legend() is None
    eintraege = z.hilfsobjekte["legende_eintraege"]
    text = a.auswahl_spitzen.lbl_kurve.text()
    assert eintraege and text == "\n".join(eintraege)
    assert "über" in text and "Punkt" in text  # Mittelformel und Punktzahl (KONVENTIONEN)
    assert a.auswahl_spitzen.lbl_kurve.isVisibleTo(a.auswahl_spitzen)


def test_thesis_variante_behaelt_die_legende_im_bild(baue: Bauer, qtbot: QtBot) -> None:
    from matplotlib.figure import Figure

    from ldv_automation.darstellung.auswahl import spitzen_daten_frf
    from ldv_automation.darstellung.spitzen import SpitzenOptionen, zeichne_spitzen
    from ldv_automation.gui.plotstil import baue_plotstil

    a = geladen_mit(baue, qtbot)
    assert a._cache is not None
    sd = spitzen_daten_frf(a._cache, "Vib X", "Ref1", gewaehlt=0)
    assert SpitzenOptionen().legende_im_bild
    z = zeichne_spitzen(Figure(figsize=(12.0, 7.4)), sd, SpitzenOptionen(), baue_plotstil())
    assert "legende" in z.hilfsobjekte
    assert any("über" in t.get_text() for t in z.hilfsobjekte["legende"].get_texts())


def test_ansicht_3_achse_ist_bei_1366_x_768_mindestens_160_px_hoch(
    baue: Bauer, qtbot: QtBot
) -> None:
    a = geladen_mit(baue, qtbot)
    a.window().resize(1366, 768)
    a.btn_ansicht[3].click()
    qtbot.wait(60)
    a.plot._neuzeichnen_timer.stop()
    a.plot._neuzeichnen()
    z = a.plot.zeichnung
    assert z is not None
    assert float(z.achsen[0].get_window_extent().height) >= 160.0


@pytest.mark.parametrize(("breite", "hoehe"), [(1366, 768), (1100, 680)])
@pytest.mark.parametrize("nr", [1, 2, 3, 4])
def test_keine_layoutwarnung_bei_mindest_und_standardgroesse(
    baue: Bauer, qtbot: QtBot, breite: int, hoehe: int, nr: int
) -> None:
    import warnings

    a = geladen_mit(baue, qtbot, mit_ref2=True)
    a.window().resize(breite, hoehe)
    with warnings.catch_warnings():
        warnings.simplefilter("error", UserWarning)  # „constrained_layout not applied“ → Fehler
        for nummer in (nr, 3, nr):
            a.btn_ansicht[nummer].click()
            qtbot.wait(40)
        a.plot._neuzeichnen_timer.stop()
        a.plot._neuzeichnen()
    assert a.fehlertext is None
