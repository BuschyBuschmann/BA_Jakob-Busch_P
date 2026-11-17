"""Ansicht 5 „Diagramm“ (R-059, P-AUSW2 Etappe C, S8 bis S10; UI-15 bis UI-21, UI-34 bis UI-37).

Ergänzt ``test_gui_ansicht_5.py`` (Aufbau mit zwei Messungen A und B): Serienliste und -dialog
(Bearbeiten, Esc, Vorbelegung), ``Aus aktueller Ansicht übernehmen``, ``Bild speichern …`` mit
Stempel über alle Dateien und der Querschnitt (Tab-Reihenfolge, Fokus, Layout, Kontraste).
Offscreen, ohne Hardware.
"""

from __future__ import annotations

import itertools
from collections.abc import Sequence
from pathlib import Path
from typing import Any

import pytest
from gui_ausw_hilfen import Bauer
from PySide6.QtCore import QEvent, QPoint, Qt
from PySide6.QtGui import QFocusEvent
from PySide6.QtTest import QTest
from PySide6.QtWidgets import (
    QAbstractButton,
    QAbstractItemView,
    QAbstractSlider,
    QAbstractSpinBox,
    QApplication,
    QComboBox,
    QDialog,
    QLineEdit,
    QScrollBar,
    QWidget,
)
from pytestqt.qtbot import QtBot
from test_gui_achsen import _tab_reihenfolge
from test_gui_ansicht_5 import (
    DATEI_A,
    DATEI_B,
    PAAR,
    achsen,
    ansicht_5,
    aufbau,
    lege_an,
    mid,
)

from ldv_automation.darstellung.achsen import Bereich
from ldv_automation.darstellung.serien_daten import SerienSpec
from ldv_automation.gui import tokens
from ldv_automation.gui.auswahl_diagramm import MessungsAngabe, SerienDialog
from ldv_automation.gui.auswerten_reiter import TEXT_BILD_KEINE_SERIE, AuswertenReiter
from ldv_automation.gui.serien import (
    SERIEN_MAX,
    TEXT_SERIE_DOPPELT,
    TEXT_SERIEN_VOLL,
    baue_spec,
)

pytestmark = pytest.mark.gui

PAAR_Y = ("Vib Y", "Ref1")


def h1(a: AuswertenReiter, nr: int, label: int | None, paar: tuple[str, str] = PAAR) -> SerienSpec:
    return baue_spec(mid(a, nr), label, "h1", kanalpaar=paar)


def waehle(a: AuswertenReiter, zeile: int) -> None:
    a.auswahl_diagramm.liste_serien.setCurrentRow(zeile)


def meldung_af(a: AuswertenReiter) -> str:
    return a.lbl_cursor.volltext()


# --- S8: Bearbeiten und Dialog (UI-15, UI-18) ---------------------------------------------------


def test_bearbeiten_aendert_die_serie_und_behaelt_slot_und_haekchen(
    baue: Bauer, monkeypatch: pytest.MonkeyPatch
) -> None:
    a, _, _, _ = aufbau(baue)
    ansicht_5(a)
    lege_an(a, h1(a, 0, 10), h1(a, 0, 11))
    a._serien.setze_sichtbar(1, False)
    a._zeichne()
    vorgaben: list[SerienSpec] = []

    def frage(spec: SerienSpec) -> SerienSpec:
        vorgaben.append(spec)
        return h1(a, 1, 12, PAAR_Y)

    monkeypatch.setattr(a, "_frage_serie_bearbeiten", frage)
    sel = a.auswahl_diagramm
    waehle(a, 1)
    sel.btn_serie_bearbeiten.click()
    assert vorgaben[0].punkt_label == 11 and vorgaben[0].messung_id == mid(a, 0)
    neu = a._serien.specs[1]
    assert (neu.messung_id, neu.punkt_label, neu.kanalpaar) == (mid(a, 1), 12, PAAR_Y)
    assert neu.slot == 1 and not neu.sichtbar and len(a._serien) == 2  # Slot und Häkchen bleiben
    item = sel.liste_serien.item(1)
    assert item is not None and item.text() == "B · Punkt 12 · Vib Y / Ref1"
    assert sel.lbl_meldung.isHidden() or sel.lbl_meldung.text() == ""


def test_bearbeiten_zu_doppelter_serie_und_abbruch_aendern_nichts(
    baue: Bauer, monkeypatch: pytest.MonkeyPatch
) -> None:
    a, _, _, _ = aufbau(baue)
    ansicht_5(a)
    lege_an(a, h1(a, 0, 10), h1(a, 0, 11))
    vorher = a._serien.specs
    antworten: list[SerienSpec | None] = [h1(a, 0, 10), None]
    monkeypatch.setattr(a, "_frage_serie_bearbeiten", lambda _spec: antworten.pop(0))
    sel = a.auswahl_diagramm
    waehle(a, 1)
    sel.btn_serie_bearbeiten.click()  # gleicht der ersten Serie
    assert sel.lbl_meldung.text() == TEXT_SERIE_DOPPELT and a._serien.specs == vorher
    sel.setze_meldung("")
    sel.btn_serie_bearbeiten.click()  # Dialog abgebrochen
    assert a._serien.specs == vorher and sel.lbl_meldung.text() == ""


def test_bearbeiten_und_entfernen_brauchen_eine_gewaehlte_zeile_doppelklick_bearbeitet(
    baue: Bauer, monkeypatch: pytest.MonkeyPatch
) -> None:
    a, _, _, _ = aufbau(baue)
    ansicht_5(a)
    sel = a.auswahl_diagramm
    assert not sel.btn_serie_bearbeiten.isEnabled() and not sel.btn_serie_entfernen.isEnabled()
    assert sel.btn_serie_bearbeiten.toolTip() == "Zuerst eine Serie in der Liste wählen."
    lege_an(a, h1(a, 0, 10))
    waehle(a, 0)
    assert sel.btn_serie_bearbeiten.isEnabled() and sel.btn_serie_entfernen.isEnabled()
    aufrufe: list[SerienSpec] = []
    monkeypatch.setattr(a, "_frage_serie_bearbeiten", lambda spec: aufrufe.append(spec))
    item = sel.liste_serien.item(0)
    assert item is not None
    sel.liste_serien.itemDoubleClicked.emit(item)
    assert len(aufrufe) == 1  # Doppelklick = Bearbeiten (Abbruch ändert nichts)
    assert [s.punkt_label for s in a._serien.specs] == [10]


def test_serien_dialog_esc_schliesst_und_bearbeiten_belegt_vor(baue: Bauer) -> None:
    a, _, _, _ = aufbau(baue)
    angaben: Sequence[MessungsAngabe] = a._angaben_der_messungen()
    dialog = SerienDialog(angaben, "h1", "kohaerent", nebeneinander=False)
    dialog.show()
    assert dialog.isModal() and dialog.windowTitle() == "Serie hinzufügen"
    QTest.keyClick(dialog, Qt.Key.Key_Escape)  # UI-15: mit Esc schließbar, ohne Ergebnis
    assert dialog.result() == QDialog.DialogCode.Rejected and not dialog.isVisible()
    spec = baue_spec(mid(a, 1), 11, "h1", kanalpaar=PAAR_Y)
    bearbeiten = SerienDialog(angaben, "h1", "kohaerent", nebeneinander=False, vorgabe=spec)
    assert bearbeiten.windowTitle() == "Serie bearbeiten"
    assert bearbeiten.combo_messung.currentData() == mid(a, 1)
    assert bearbeiten.combo_punkt.currentData() == 11
    assert bearbeiten.combo_paar.currentData() == PAAR_Y
    assert bearbeiten.ergebnis() == spec
    mittel = baue_spec(mid(a, 0), None, "spektrum", komponente="Y", teilgroesse="leistung")
    spektrum = SerienDialog(angaben, "spektrum", "leistung", nebeneinander=True, vorgabe=mittel)
    assert (
        spektrum.combo_punkt.currentData() is None
        and spektrum.combo_komponente.currentData() == "Y"
    )
    assert spektrum.ergebnis() == mittel
    for d in (dialog, bearbeiten, spektrum):
        d.close()


def test_groessenknoepfe_lassen_genau_eine_groesse_zu_nebeneinander_je_teilbild_eine(
    baue: Bauer,
) -> None:
    a, _, _, _ = aufbau(baue)
    ansicht_5(a)
    sel = a.auswahl_diagramm
    for g in ("h1", "kohaerenz", "spektrum"):  # UI-16: ein Radioknopf, nie zwei
        sel.rb_groesse[g].setChecked(True)
        assert [k.isChecked() for k in sel.rb_groesse.values()].count(True) == 1
    sel.rb_anordnung_nebeneinander.setChecked(True)
    lege_an(a, h1(a, 0, 10), baue_spec(mid(a, 0), 10, "kohaerenz", kanalpaar=PAAR))
    z = a.plot.zeichnung
    assert z is not None and len(z.achsen) == 2
    labels = sorted(ax.get_ylabel() for ax in z.achsen)
    assert len(set(labels)) == 2 and all("[" in label for label in labels)  # eigene Größe, Einheit
    assert any("|H1|" in t for t in z.alle_texte()) and any("Kohärenz" in t for t in z.alle_texte())


# --- S8: Aus aktueller Ansicht übernehmen (UI-15, UI-16, UI-18) ---------------------------------


def uebernehmen(a: AuswertenReiter, von: int) -> None:
    a.btn_ansicht[von].click()
    ansicht_5(a)
    a.auswahl_diagramm.btn_serie_aus_ansicht.click()


def test_aus_ansicht_1_uebernimmt_je_komponente_eine_serie_und_setzt_die_groesse(
    baue: Bauer,
) -> None:
    a, _, _, _ = aufbau(baue)
    a.btn_ansicht[1].click()
    a.chk["Y"].setChecked(False)
    a.chk["3D"].setChecked(False)
    a.liste_punkte.setCurrentRow(2)  # Zeile 0 = Mittel, Zeile 2 = zweiter Punkt
    a.rb_groesse_ap.setChecked(True)
    aktive = a.messungen.aktive
    assert aktive is not None and aktive.geladen is not None
    label = int(aktive.geladen.messdaten.punkte.label[1])
    ansicht_5(a)
    sel = a.auswahl_diagramm
    sel.rb_groesse["h1"].setChecked(True)  # Liste leer: die Übernahme bestimmt die Größe neu
    sel.btn_serie_aus_ansicht.click()
    assert [(s.groesse, s.komponente, s.punkt_label) for s in a._serien.specs] == [
        ("spektrum", "X", label),
        ("spektrum", "Z", label),
    ]
    assert all(s.messung_id == aktive.id and s.teilgroesse == "leistung" for s in a._serien.specs)
    assert sel.groesse() == "spektrum" and sel.teilgroesse() == "leistung"
    assert sel.rb_teil_ap.isChecked()
    assert len(achsen(a)[0].get_lines()) == 2  # type: ignore[attr-defined]
    assert sel.lbl_meldung.text() == "2 Serien aus Ansicht 1 übernommen."
    sel.btn_serie_aus_ansicht.click()  # nochmal: nichts doppelt, Hinweis
    assert len(a._serien) == 2 and "2 gab es schon" in sel.lbl_meldung.text()


def test_aus_ansicht_2_uebernimmt_h1_oder_nur_h2_des_kanalpaars(baue: Bauer) -> None:
    a, _, _, _ = aufbau(baue)
    aktive = a.messungen.aktive  # die zuletzt geladene Messung ist aktiv
    assert aktive is not None and aktive.geladen is not None
    a.btn_ansicht[2].click()
    a.liste_punkte.setCurrentRow(1)  # Zeile 0 = Mittel, Zeile 1 = erster Punkt
    a.btn_ansicht[5].click()
    sel = a.auswahl_diagramm
    sel.btn_serie_aus_ansicht.click()
    spec = a._serien.specs[0]
    assert (spec.groesse, spec.kanalpaar, spec.messung_id) == ("h1", PAAR, aktive.id)
    assert spec.punkt_label == int(aktive.geladen.messdaten.punkte.label[0])
    assert sel.groesse() == "h1"
    a.btn_ansicht[2].click()
    a.auswahl_frf.chk_h1.setChecked(False)
    a.auswahl_frf.chk_h2.setChecked(True)
    a.btn_ansicht[5].click()
    sel.btn_serie_aus_ansicht.click()
    assert len(a._serien) == 1  # |H2| passt nicht zur Größe |H1| des Diagramms: nichts gewechselt
    assert "nicht übernommen" in sel.lbl_meldung.text() and sel.groesse() == "h1"
    a._serien.leere()
    sel.btn_serie_aus_ansicht.click()  # leere Liste: die Übernahme setzt die Größe
    assert a._serien.specs[0].groesse == "h2" and sel.groesse() == "h2"


def test_aus_ansicht_3_uebernimmt_die_gezeigte_kurve_als_mittel(baue: Bauer) -> None:
    a, _, _, _ = aufbau(baue)
    uebernehmen(a, 3)
    spec = a._serien.specs[0]
    assert (spec.groesse, spec.punkt_label, spec.kanalpaar) == ("h1", None, PAAR)
    z = a.plot.zeichnung
    assert z is not None and len(achsen(a)[0].get_lines()) == 1  # type: ignore[attr-defined]


def test_aus_ansicht_nimmt_die_zuletzt_benutzte_ansicht_1_bis_3(baue: Bauer) -> None:
    a, _, _, _ = aufbau(baue)
    a.btn_ansicht[2].click()
    a.btn_ansicht[4].click()  # Ansicht 4 hat nichts zu übernehmen: es gilt Ansicht 2
    ansicht_5(a)
    a.auswahl_diagramm.btn_serie_aus_ansicht.click()
    assert a.auswahl_diagramm.lbl_meldung.text().startswith("1 Serie aus Ansicht 2")
    assert a._serien.specs[0].groesse == "h1"


def test_aus_ansicht_wechselt_die_groesse_nicht_still_und_nennt_den_rest_in_af(
    baue: Bauer,
) -> None:
    a, _, _, _ = aufbau(baue)
    ansicht_5(a)
    sel = a.auswahl_diagramm
    sel.rb_groesse["h1"].setChecked(True)
    lege_an(a, h1(a, 0, 10))
    uebernehmen(a, 1)  # Spektrum passt nicht zu |H1| (überlagert)
    assert len(a._serien) == 1 and "Ansicht 1 zeigt Spektrum" in sel.lbl_meldung.text()
    assert sel.groesse() == "h1"
    a._serien.leere()
    sel.rb_groesse["spektrum"].setChecked(True)
    lege_an(a, *[baue_spec(mid(a, 0), 10 + i, "spektrum", komponente="Z") for i in range(3)])
    a.btn_ansicht[1].click()
    a.chk["Y"].setChecked(False)
    a.chk["3D"].setChecked(False)
    a.chk["Z"].setChecked(False)  # nur X: passt als vierte
    ansicht_5(a)
    sel.btn_serie_aus_ansicht.click()
    assert len(a._serien) == SERIEN_MAX and not sel.btn_serie_aus_ansicht.isEnabled()
    assert sel.btn_serie_aus_ansicht.toolTip() == TEXT_SERIEN_VOLL
    a._serien.entferne(3)
    a._serien.entferne(2)
    a._zeichne()
    a.btn_ansicht[1].click()
    for c in ("X", "Y", "Z", "3D"):
        a.chk[c].setChecked(True)  # vier Komponenten in Mittel, zwei Plätze frei
    ansicht_5(a)
    sel.btn_serie_aus_ansicht.click()
    assert len(a._serien) == SERIEN_MAX
    assert "2 passten nicht (höchstens 4 Serien)" in sel.lbl_meldung.text()
    assert "2 passten nicht" in meldung_af(a)  # AF nennt den Rest


# --- S9: Bild speichern (UI-19) -----------------------------------------------------------------


def richte_bild_ein(
    a: AuswertenReiter, monkeypatch: pytest.MonkeyPatch, ziel: Path
) -> tuple[list[Any], list[str]]:
    bilder: list[Any] = []
    vorschlaege: list[str] = []
    original = a.plot.speichere

    def erfasse(pfad: Path, stempel: Any) -> Any:
        z = original(pfad, stempel)
        bilder.append(z)
        return z

    def waehle_ziel(vorschlag: str) -> str:
        vorschlaege.append(vorschlag)
        return str(ziel)

    monkeypatch.setattr(a.plot, "speichere", erfasse)
    monkeypatch.setattr(a, "_waehle_bild_ziel", waehle_ziel)
    monkeypatch.setattr(a, "_git_hash", lambda: ("a1b2c3d4e5f6" + "0" * 28, False))
    return bilder, vorschlaege


def test_bild_ansicht_5_png_mit_legende_allen_dateien_und_git_hash(
    baue: Bauer, monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    a, _, _, _ = aufbau(baue)
    ansicht_5(a)
    lege_an(a, h1(a, 0, 10), h1(a, 1, 10))
    a.plot.achsen_zustand.setze_bereich(5, "frequenz", Bereich(4.0, 12.0))
    a._zeichne()
    bilder, vorschlaege = richte_bild_ein(a, monkeypatch, tmp_path / "v.png")
    assert a.btn_bild.isEnabled()
    a.btn_bild.click()
    assert bilder[0].achsen[0].get_xlim() == pytest.approx((4.0, 12.0))  # feste Bereiche im Bild
    assert (tmp_path / "v.png").read_bytes()[:8] == b"\x89PNG\r\n\x1a\n"
    assert vorschlaege[0].endswith("a_ansicht5.png")  # Basisname der ersten Serie
    texte = bilder[0].alle_texte()
    kopf = next(t for t in texte if t.startswith("Arbeitsansicht – nicht für die Thesis"))
    assert "Ansicht 5 Diagramm" in kopf and "a1b2c3d4e5f6" in kopf  # Git-Hash
    assert "A: a.svd" in texte and "B: b.svd" in texte  # je Datei eine Zeile
    assert any("A · Punkt 10" in t for t in texte) and any("B · Punkt 10" in t for t in texte)
    assert not any("unbestätigte Größen" in t for t in texte)  # kein M8 ohne Phase
    # die Bildschirmdarstellung trägt den Stempel nicht (Zeichenfunktion ohne Stempel)
    assert a.plot.zeichnung is not None
    gui_texte = a.plot.zeichnung.alle_texte()
    assert not any("Arbeitsansicht" in t or "A: a.svd" in t for t in gui_texte)
    assert a.lbl_cursor.volltext() == f"Bild geschrieben: {tmp_path / 'v.png'}"


def test_bild_ansicht_5_pdf_mit_unbestaetigter_phase_und_ohne_unsichtbare_datei(
    baue: Bauer, monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    a, _, _, _ = aufbau(baue)
    ansicht_5(a)
    a.auswahl_diagramm.rb_groesse["phase"].setChecked(True)
    lege_an(a, baue_spec(mid(a, 0), 10, "phase", kanalpaar=PAAR))
    lege_an(a, baue_spec(mid(a, 1), 10, "phase", kanalpaar=PAAR))
    bilder, _ = richte_bild_ein(a, monkeypatch, tmp_path / "p.pdf")
    a._serien.setze_sichtbar(1, False)  # B hat keine Linie im Bild: auch nicht im Stempel
    a._zeichne()
    a.btn_bild.click()
    assert (tmp_path / "p.pdf").read_bytes().startswith(b"%PDF")
    texte = bilder[0].alle_texte()
    assert "A: a.svd" in texte and "B: b.svd" not in texte
    assert any("enthält unbestätigte Größen (M8)" in t for t in texte)  # M8 bei Phase
    # nur noch |H1|: kein Zusatz
    a._serien.leere()
    a.auswahl_diagramm.rb_groesse["h1"].setChecked(True)
    lege_an(a, h1(a, 0, 10))
    a.btn_bild.click()
    assert not any("unbestätigte Größen" in t for t in bilder[1].alle_texte())


def test_bild_ansicht_5_ohne_sichtbare_darstellbare_serie_ist_gesperrt(
    baue: Bauer, monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    a, _, _, _ = aufbau(baue)
    ansicht_5(a)
    a.auswahl_diagramm.rb_groesse["phase"].setChecked(True)
    lege_an(a, baue_spec(mid(a, 0), None, "phase", kanalpaar=PAAR))  # Mittel: nicht darstellbar
    assert not a.btn_bild.isEnabled() and a.btn_bild.toolTip() == TEXT_BILD_KEINE_SERIE
    lege_an(a, baue_spec(mid(a, 0), 11, "phase", kanalpaar=PAAR))
    assert a.btn_bild.isEnabled()
    a._serien.setze_sichtbar(1, False)  # die darstellbare Serie ausgeblendet
    a._zeichne()
    assert not a.btn_bild.isEnabled()
    bilder, _ = richte_bild_ein(a, monkeypatch, tmp_path / "m.png")
    a.btn_bild.click()  # gesperrt: nichts geschrieben
    assert bilder == [] and not (tmp_path / "m.png").exists()


def test_bild_ansicht_5_nebeneinander_mit_vier_dateien_nennt_jede_datei_einmal(
    baue: Bauer, monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    a, _ = vier_messungen(baue)
    bilder, _ = richte_bild_ein(a, monkeypatch, tmp_path / "n.png")
    a.btn_bild.click()
    z = bilder[0]
    assert len(z.achsen) == 4  # vier Messungen, ein Teilbild je Messung
    for kurz in ("A", "B", "C", "D"):
        assert z.alle_texte().count(f"{kurz}: {kurz.lower()}.svd") == 1  # jede Datei einmal


# --- S10: Tab-Reihenfolge, Fokus, Layout, Kontraste (UI-34 bis UI-37) ---------------------------


def test_ui34_tab_reihenfolge_aa_ac_ad_ag_ae_af(baue: Bauer) -> None:
    a, _, _, _ = aufbau(baue)
    QApplication.processEvents()
    reihe = _tab_reihenfolge(a)

    def stellen(widgets: Sequence[QWidget]) -> list[int]:
        return [reihe.index(w) for w in widgets]

    aa = [a.btn_oeffnen, a.btn_messung_hinzu, *a.messungsleiste.tab_kette(), a.btn_export]
    gruppen: dict[str, Sequence[QWidget]] = {
        "AA": [*aa, a.btn_bild],
        "AC": [a.btn_ansicht[nr] for nr in sorted(a.btn_ansicht)],
        "AD": a.auswahl_diagramm.tab_kette(),
        "AG": a.achsenleiste.tab_kette(),
        "AE": a.plot.tab_kette(),
        "AF": [a.lbl_pruefung],
    }
    belegt = {n: stellen(w) for n, w in gruppen.items()}
    namen = list(gruppen)
    for vorher, nachher in itertools.pairwise(namen):
        assert max(belegt[vorher]) < min(belegt[nachher]), (vorher, nachher)
    # innerhalb der Ansicht-5-Auswahl: Größe, Anordnung, Knöpfe, Serienliste
    ad = a.auswahl_diagramm
    kette = stellen(ad.tab_kette())
    assert kette == sorted(kette)
    assert ad.tab_kette()[-1] is ad.liste_serien
    assert ad.btn_serie_aus_ansicht in ad.tab_kette() and ad.btn_serie_bearbeiten in ad.tab_kette()


def test_ui34_jedes_bedienbare_widget_der_oberflaeche_kann_den_fokus_bekommen(
    baue: Bauer,
) -> None:
    a, _, _, _ = aufbau(baue)
    ansicht_5(a)
    lege_an(a, h1(a, 0, 10), h1(a, 1, 10))
    QApplication.processEvents()
    bedienbar = (
        QAbstractButton,
        QLineEdit,
        QComboBox,
        QAbstractItemView,
        QAbstractSlider,
        QAbstractSpinBox,
    )
    ohne: list[str] = []
    for w in a.findChildren(QWidget):
        if not isinstance(w, bedienbar) or isinstance(w, QScrollBar):
            continue
        # Kind eines Kombinationsfelds (Editor, Listenansicht) gehört zum Feld
        if isinstance(w.parent(), (QComboBox, QAbstractItemView, QAbstractSpinBox)):
            continue
        if w.focusPolicy() == Qt.FocusPolicy.NoFocus:
            ohne.append(f"{type(w).__name__}:{w.objectName()}")
    # Knöpfe der Matplotlib-Werkzeugleiste gehören zur Plotfläche (eigene Tab-Kette, geprüft unten)
    ohne = [n for n in ohne if a.plot.findChild(QWidget, n.split(":", 1)[1] or "-") is None]
    assert ohne == []
    for w in a.plot.tab_kette():
        assert w.focusPolicy() != Qt.FocusPolicy.NoFocus


def sammle_rechtecke(
    fenster: QWidget, namen: Sequence[str], a: AuswertenReiter
) -> dict[str, tuple[int, int, int, int]]:
    ergebnis: dict[str, tuple[int, int, int, int]] = {}
    for name in namen:
        wid = a.findChild(QWidget, name)
        assert wid is not None, name
        p = wid.mapTo(fenster, QPoint(0, 0))
        ergebnis[name] = (p.x(), p.y(), wid.width(), wid.height())
    return ergebnis


def ueberlappt(r1: tuple[int, int, int, int], r2: tuple[int, int, int, int]) -> bool:
    x1, y1, b1, h1_ = r1
    x2, y2, b2, h2 = r2
    return x1 < x2 + b2 and x2 < x1 + b1 and y1 < y2 + h2 and y2 < y1 + h1_


def vier_messungen(baue: Bauer) -> tuple[AuswertenReiter, QWidget]:
    """Vier Messungen (Höchstzahl) in Ansicht 5 mit vier Serien, nebeneinander."""
    from gui_ausw_hilfen import SteuerbarerAusfuehrer, synth_geladen

    ausf = SteuerbarerAusfuehrer()
    w, prot = baue(ausf)
    a = w.auswerten
    assert a is not None
    dateien = [DATEI_A, DATEI_B, "C:\\messungen\\c.svd", "C:\\messungen\\d.svd"]
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
    assert len(a.messungen) == 4
    ansicht_5(a)
    a.auswahl_diagramm.rb_anordnung_nebeneinander.setChecked(True)
    lege_an(a, *[h1(a, i, 10) for i in range(4)])
    return a, w


@pytest.mark.parametrize(("breite", "hoehe"), [(1100, 680), (1366, 768)])
def test_ui36_ansicht_5_mit_vier_messungen_und_serien_ueberlappt_nichts(
    baue: Bauer, qtbot: QtBot, breite: int, hoehe: int
) -> None:
    a, w = vier_messungen(baue)
    w.resize(breite, hoehe)
    qtbot.waitUntil(lambda: w.width() == breite, timeout=2000)
    qtbot.wait(100)
    zonen = ("dateileiste", "ansichtswahl", "auswahlspalte", "darstellung", "fusszeile")
    r = sammle_rechtecke(w, zonen, a)
    for i, n1 in enumerate(zonen):
        assert r[n1][2] > 0 and r[n1][3] > 0, n1
        for n2 in zonen[i + 1 :]:
            assert not ueberlappt(r[n1], r[n2]), (n1, n2, r[n1], r[n2])
    # AA mit vier Chips: nebeneinander, in der Dateileiste, nicht übereinander
    chips = [a.messungsleiste.chip(m.id) for m in a.messungen.alle]
    assert all(c is not None for c in chips)
    boxen = [(c.mapTo(w, QPoint(0, 0)), c.size()) for c in chips if c is not None]
    rechtecke = [(p.x(), p.y(), s.width(), s.height()) for p, s in boxen]
    for i, r1 in enumerate(rechtecke):
        assert r1[2] > 0 and r1[3] > 0
        for r2 in rechtecke[i + 1 :]:
            assert not ueberlappt(r1, r2), (r1, r2)
    # AD: keine Überlappung der Elemente der Spalte und nichts unterhalb der Spalte
    spalte = r["auswahlspalte"]
    kinder = [
        k
        for k in a.auswahl_diagramm.findChildren(
            QWidget, options=Qt.FindChildOption.FindDirectChildrenOnly
        )
        if k.isVisibleTo(a.auswahl_diagramm)
    ]
    boxen_ad = []
    for k in kinder:
        p = k.mapTo(w, QPoint(0, 0))
        boxen_ad.append((p.x(), p.y(), k.width(), k.height()))
    for i, r1 in enumerate(boxen_ad):
        assert r1[1] + r1[3] <= spalte[1] + spalte[3] + 1, ("unterhalb der Spalte", r1, spalte)
        for r2 in boxen_ad[i + 1 :]:
            assert not ueberlappt(r1, r2), (r1, r2)
    # AG: Gruppen der Achsenleiste nebeneinander ohne Überlappung, nichts abgeschnitten
    leiste = a.achsenleiste
    gruppen = [
        g.geometry()
        for r_ in ("frequenz", "betrag", "phase")
        if (g := leiste.gruppe(r_)) and g.isVisibleTo(leiste)
    ]
    for i, g1 in enumerate(gruppen):
        assert leiste.rect().contains(g1)
        for g2 in gruppen[i + 1 :]:
            assert not g1.intersects(g2)
    if (breite, hoehe) == (1366, 768):
        ae = r["darstellung"]
        assert ae[2] >= 600 and ae[3] >= 320  # UI-36
    else:
        assert r["darstellung"][2] >= tokens.PLOT_MIN_BREITE_PX
        assert r["darstellung"][3] >= tokens.PLOT_MIN_HOEHE_PX


def test_ui37_zahlenfelder_in_ansicht_5_zeichnen_erst_bei_enter_oder_fokuswechsel(
    baue: Bauer, monkeypatch: pytest.MonkeyPatch
) -> None:
    a, _, _, _ = aufbau(baue)
    ansicht_5(a)
    lege_an(a, h1(a, 0, 10), h1(a, 1, 10))
    QApplication.processEvents()
    aufrufe: list[int] = []
    original = a.plot.zeichne

    def zaehle(*args: Any, **kwargs: Any) -> Any:
        aufrufe.append(1)
        return original(*args, **kwargs)

    monkeypatch.setattr(a.plot, "zeichne", zaehle)
    feld = a.achsenleiste.findChild(QLineEdit, "achse_f_von")
    assert feld is not None
    feld.setFocus()
    for ziffer in "2,5":
        QTest.keyClicks(feld, ziffer)
    assert aufrufe == []  # Tippen zeichnet nicht (UI-37)
    QTest.keyClick(feld, Qt.Key.Key_Return)
    assert len(aufrufe) == 1  # genau ein Neuzeichnen je Übernahme
    QTest.keyClick(feld, Qt.Key.Key_Return)
    assert len(aufrufe) == 1  # derselbe Wert: nichts zu zeichnen
    feld.selectAll()
    QTest.keyClicks(feld, "7")  # neuer Wert, noch nicht bestätigt
    assert len(aufrufe) == 1
    QApplication.sendEvent(feld, QFocusEvent(QEvent.Type.FocusOut, Qt.FocusReason.TabFocusReason))
    assert len(aufrufe) == 2  # Fokuswechsel übernimmt den Wert: genau ein Neuzeichnen


def test_ui36_ansicht_5_vier_serien_ohne_bildlauf_bei_1366_768(baue: Bauer, qtbot: QtBot) -> None:
    a, w = vier_messungen(baue)
    w.resize(1366, 768)
    qtbot.waitUntil(lambda: w.width() == 1366, timeout=2000)
    qtbot.wait(100)
    # Der Hinweis „Höchstens vier Serien“ steht nur im Tooltip: die Spalte passt ohne Bildlauf.
    assert a.auswahlspalte.verticalScrollBar().maximum() == 0


def test_ui36_ansicht_5_vier_serien_kein_bildlauf_nach_groessenwechseln(
    baue: Bauer, qtbot: QtBot
) -> None:
    """Prüfpunkt B9: Nach dem Umschalten der kompakten Anzeige misst die Spalte neu.

    Ursache des früheren 12-px-Bildlaufs bei 1100 mal 680: Die Anordnungsbox behielt nach dem
    Richtungswechsel ihre alte Höhe (zwei Zeilen) im Größenspeicher des Spaltenlayouts.
    """
    a, w = vier_messungen(baue)
    for breite, hoehe in ((1100, 680), (1366, 768), (1100, 680), (1366, 768), (1100, 680)):
        w.resize(breite, hoehe)
        ziel = breite
        qtbot.waitUntil(lambda: w.width() == ziel, timeout=2000)  # noqa: B023  # sofort geprüft
        qtbot.wait(50)
        assert a.auswahlspalte.verticalScrollBar().maximum() == 0, (breite, hoehe)
        inhalt = a.auswahlspalte.widget()
        assert inhalt is not None
        assert inhalt.minimumSizeHint().height() <= a.auswahlspalte.viewport().height()


NEUE_KONTRASTPAARE = (
    "text/aktiv_bg",
    "deaktiviert_text/flaeche",
    "deaktiviert_text/deaktiviert_bg",
)


def test_ui35_kontrastpaare_der_neuen_elemente_stehen_in_den_tokens_und_bestehen() -> None:
    namen = {n: (v, h) for n, v, h in tokens.KONTRAST_PAARE}
    for n in NEUE_KONTRASTPAARE:
        assert n in namen, n
    for n, (vorder, hinter) in namen.items():
        if n in NEUE_KONTRASTPAARE:
            assert tokens.kontrastverhaeltnis(vorder, hinter) >= tokens.KONTRAST_MINDEST_TEXT, n
