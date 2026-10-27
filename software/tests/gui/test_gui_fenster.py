"""Oberflächentests mit Qt (pytest-qt, offscreen), Marker ``gui``.

Ausführen: ``QT_QPA_PLATFORM=offscreen uv run pytest -m gui``. Die meisten Tests nutzen die
Sitzungsattrappe mit ``Zustandsbild``-Attrappen; Rauch- und Ablauftests nutzen die echte
Sitzung mit Simulator. Modale Dialoge werden über ``Hauptfenster._fuehre_aus`` bedient.
"""

from __future__ import annotations

import json
import sys
import time
from collections.abc import Callable, Iterator
from pathlib import Path
from typing import Any

import pytest
from gui_hilfen import (
    GENERATOR_AN,
    GENERATOR_AUS,
    INFO,
    VORAUSSETZUNGEN_ERFUELLT,
    AttrappenSitzung,
    Z,
    bild,
    echte_sitzung,
    eintrag,
    fortschritt,
    set_datei,
    vorschau_zu,
    zusammenfassung,
)
from PySide6.QtCore import Qt
from PySide6.QtTest import QTest
from PySide6.QtWidgets import (
    QAbstractButton,
    QApplication,
    QDialog,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QWidget,
)
from pytestqt.qtbot import QtBot

from ldv_automation.ablauf.steuerung import DurchgangErgebnis, Fehlerentscheidung
from ldv_automation.ablauf.uhr import Echtzeituhr
from ldv_automation.domaene import KATALOG, Messung, Parameterkatalog, ParameterSpec, Pausenpunkt
from ldv_automation.geraet.schnittstelle import Messgeraet
from ldv_automation.geraet.simulator import HaengenderAufruf, Simulator, SimulatorKonfiguration
from ldv_automation.gui import stil
from ldv_automation.gui.dialoge import (
    DurchgangStartenDialog,
    EinstellungenDialog,
    GeraetDialog,
    MessenFreischaltenDialog,
)
from ldv_automation.gui.hauptfenster import Hauptfenster
from ldv_automation.sitzung import (
    Betriebsart,
    EinstellungsFehler,
    Sitzung,
    SitzungsEreignis,
    Voraussetzung,
)

pytestmark = pytest.mark.gui

Aktion = Callable[[QDialog], None]


class Dialoge:
    """Ersatz für ``Hauptfenster._fuehre_aus``: merkt Dialoge und bedient sie."""

    def __init__(self) -> None:
        self.gesehen: list[QDialog] = []
        self.aktionen: list[Aktion] = []

    def __call__(self, dialog: QDialog) -> int:
        self.gesehen.append(dialog)
        if self.aktionen:
            self.aktionen.pop(0)(dialog)
        return dialog.result()


def klicke(text: str) -> Aktion:
    """Klickt den Knopf mit ``text`` im Dialog."""

    def aktion(dialog: QDialog) -> None:
        knoepfe = [b for b in dialog.findChildren(QAbstractButton) if b.text() == text]
        assert knoepfe, (
            f"kein Knopf {text!r}: {[b.text() for b in dialog.findChildren(QAbstractButton)]}"
        )
        knoepfe[0].click()

    return aktion


def annehmen(dialog: QDialog) -> None:
    dialog.accept()


def ablehnen(dialog: QDialog) -> None:
    dialog.reject()


@pytest.fixture
def baue(
    qtbot: QtBot, monkeypatch: pytest.MonkeyPatch
) -> Iterator[Callable[..., tuple[Hauptfenster, Dialoge]]]:
    stil.wende_an(QApplication.instance())  # type: ignore[arg-type]
    erzeugt: list[Hauptfenster] = []

    def bau(sitzung: Any, **kw: Any) -> tuple[Hauptfenster, Dialoge]:
        kw.setdefault("takt_ms", None)
        w = Hauptfenster(sitzung, **kw)
        dialoge = Dialoge()
        monkeypatch.setattr(w, "_fuehre_aus", dialoge)
        qtbot.addWidget(w)
        w.show()
        qtbot.waitExposed(w)
        w.activateWindow()
        qtbot.waitUntil(w.isActiveWindow, timeout=2000)
        erzeugt.append(w)
        return w, dialoge

    yield bau
    for w in erzeugt:
        w._timer.stop()


def fokus_ist(widget: QWidget | None) -> bool:
    """Prüft den Tastaturfokus (ohne Typverengung durch ``is``)."""
    return QApplication.focusWidget() is widget


def letzter(s: AttrappenSitzung) -> tuple[Any, ...]:
    """Letzter aufgezeichneter Befehl."""
    return s.befehle[-1]


def zelle(w: Hauptfenster, zeile: int, spalte: int) -> str:
    item = w.tabelle.item(zeile, spalte)
    assert item is not None
    return item.text()


def taste(
    qtbot: QtBot, w: QWidget, key: Qt.Key, mod: Qt.KeyboardModifier = Qt.KeyboardModifier.NoModifier
) -> None:
    QTest.keyClick(w, key, mod)


# --- UI-1 -----------------------------------------------------------------------------------


def test_ui_1_leere_warteschlange(baue: Any) -> None:
    s = AttrappenSitzung(bild(betriebsart=Betriebsart.NUR_LESEN))
    w, _ = baue(s)
    assert w.tabelle.leer_sichtbar()
    leer = w.tabelle.findChild(QLabel, "tabelle_leer")
    assert leer is not None and leer.text().startswith("Noch keine Messung. Mit „+ Messung“")
    assert not w.btn_start.isEnabled()
    assert "Start nicht möglich" in w.act_start.toolTip()
    assert w.lbl_durchgang.volltext() == "Durchgang: Bereit"
    assert w.hinweisband.property("fall") == ""
    assert w.hinweisband.text.text() == ""
    assert w.hinweisband.height() == 44
    # Simulator: Fall 8 belegt dieselbe Höhe (kein Springen)
    s.setze(betriebsart=Betriebsart.SIMULATOR)
    w.aktualisiere()
    assert w.hinweisband.property("fall") == "8"
    assert w.hinweisband.height() == 44


# --- UI-2 -----------------------------------------------------------------------------------


def test_ui_2_neue_messung_hinter_auswahl(baue: Any, qtbot: QtBot, tmp_path: Path) -> None:
    m1, m2 = eintrag(name="A"), eintrag(name="B")
    s = AttrappenSitzung(bild(eintraege=[m1, m2]))
    w, _ = baue(s)
    w.tabelle.waehle(m1.id)
    taste(qtbot, w, Qt.Key.Key_N, Qt.KeyboardModifier.ControlModifier)
    assert w.editor.modus == "neu_messung"
    assert w.editor.titel.text() == "Neue Messung"
    assert w.editor.untertitel.text() == "wird eingefügt nach Nr 01 (vorl.)"
    assert fokus_ist(w.editor.name)
    assert not w.editor.btn_uebernehmen.isEnabled()
    QTest.keyClicks(w.editor.name, "Platte_Mitte")
    w.editor.datei_waehlen = lambda _o: set_datei(tmp_path)
    QTest.mouseClick(w.editor.btn_set, Qt.MouseButton.LeftButton)
    assert w.editor.btn_uebernehmen.isEnabled()
    QTest.mouseClick(w.editor.btn_uebernehmen, Qt.MouseButton.LeftButton)
    assert s.namen() == ["einfuegen"]
    _name, position, neu = s.befehle[0]
    assert position == 1 and isinstance(neu, Messung) and neu.name == "Platte_Mitte"
    assert w.tabelle.gewaehlte_id() == neu.id
    assert zelle(w, 1, 1) == "○ wartend"
    assert w.editor.modus == "bearbeiten"


def test_ui_2_ohne_auswahl_am_ende_und_verwerfen(baue: Any, qtbot: QtBot) -> None:
    s = AttrappenSitzung(bild(eintraege=[eintrag(), eintrag()]))
    w, _ = baue(s)
    taste(qtbot, w, Qt.Key.Key_N, Qt.KeyboardModifier.ControlModifier)
    assert w.editor.untertitel.text() == "wird eingefügt am Ende"
    QTest.keyClicks(w.editor.name, "X")
    QTest.mouseClick(w.editor.btn_verwerfen, Qt.MouseButton.LeftButton)
    assert s.befehle == [] and w.editor.modus == "leer"
    taste(qtbot, w, Qt.Key.Key_N, Qt.KeyboardModifier.ControlModifier)
    QTest.keyClicks(w.editor.name, "Y")
    taste(qtbot, w.editor.name, Qt.Key.Key_Escape)
    assert s.befehle == [] and w.editor.modus == "leer"
    assert fokus_ist(w.tabelle)


def test_ui_2_einfuegen_nie_vor_gestartete(baue: Any, qtbot: QtBot, tmp_path: Path) -> None:
    f, lauf = eintrag(zustand="fertig"), eintrag(zustand="laeuft")
    s = AttrappenSitzung(bild(durchgang=Z.LAEUFT, eintraege=[f, lauf]))
    w, _ = baue(s)
    w.tabelle.waehle(f.id)
    taste(qtbot, w, Qt.Key.Key_N, Qt.KeyboardModifier.ControlModifier)
    assert w.editor.untertitel.text() == "wird eingefügt am Ende"
    QTest.keyClicks(w.editor.name, "N")
    w.editor.set_feld.setText(set_datei(tmp_path))
    taste(qtbot, w.editor.name, Qt.Key.Key_Return, Qt.KeyboardModifier.ControlModifier)
    assert s.befehle[0][1] == 2


def test_ui_2_fehler_der_sitzung_im_editor(baue: Any, qtbot: QtBot, tmp_path: Path) -> None:
    s = AttrappenSitzung(bild())
    s.fehler["einfuegen"] = ValueError("Nur Einträge im Zustand WARTEND können eingefügt werden")
    w, _ = baue(s)
    taste(qtbot, w, Qt.Key.Key_N, Qt.KeyboardModifier.ControlModifier)
    QTest.keyClicks(w.editor.name, "N")
    w.editor.set_feld.setText(set_datei(tmp_path))
    QTest.mouseClick(w.editor.btn_uebernehmen, Qt.MouseButton.LeftButton)
    assert not w.editor.konflikt.isHidden()
    assert "Nur Einträge im Zustand WARTEND" in w.editor.konflikt_text.text()
    assert w.editor.modus == "neu_messung"


# --- UI-3 -----------------------------------------------------------------------------------


@pytest.mark.parametrize("zustand", ["laeuft", "fertig", "fehler", "abgebrochen"])
def test_ui_3_knoepfe_bei_nicht_wartendem_eintrag(baue: Any, zustand: str) -> None:
    e = eintrag(zustand=zustand)
    s = AttrappenSitzung(bild(durchgang=Z.LAEUFT, eintraege=[e, eintrag()]))
    w, _ = baue(s)
    w.tabelle.waehle(e.id)
    w.aktualisiere()
    for b, aktion in (
        (w.btn_entfernen, w.act_entfernen),
        (w.btn_hoch, w.act_hoch),
        (w.btn_runter, w.act_runter),
    ):
        assert not b.isEnabled()
        assert " – " in aktion.toolTip()


def test_ui_3_tasten_wie_knoepfe(baue: Any, qtbot: QtBot) -> None:
    f, a1, a2, a3 = (
        eintrag(zustand="fertig"),
        eintrag(name="A"),
        eintrag(name="B"),
        eintrag(name="C"),
    )
    s = AttrappenSitzung(bild(eintraege=[f, a1, a2, a3]))
    w, _ = baue(s)
    w.tabelle.waehle(a1.id)
    w.aktualisiere()
    assert not w.btn_hoch.isEnabled() and "Anfang der wartenden" in w.act_hoch.toolTip()
    assert w.btn_runter.isEnabled() and w.btn_entfernen.isEnabled()
    w.tabelle.setFocus()
    taste(qtbot, w.tabelle, Qt.Key.Key_Up, Qt.KeyboardModifier.AltModifier)  # gesperrt
    assert s.befehle == []
    taste(qtbot, w.tabelle, Qt.Key.Key_Down, Qt.KeyboardModifier.AltModifier)
    assert letzter(s) == ("verschieben", a1.id, 2)
    assert w.tabelle.gewaehlte_id() == a1.id
    QTest.mouseClick(w.btn_hoch, Qt.MouseButton.LeftButton)
    assert letzter(s) == ("verschieben", a1.id, 1)
    w.tabelle.waehle(a3.id)
    w.aktualisiere()
    assert not w.btn_runter.isEnabled() and "Ende der Liste" in w.act_runter.toolTip()
    w.tabelle.setFocus()
    taste(qtbot, w.tabelle, Qt.Key.Key_Delete)
    assert letzter(s) == ("entfernen", a3.id)
    assert [e.id for e in s.bild.eintraege] == [f.id, a1.id, a2.id]
    w.tabelle.waehle(a2.id)
    w.aktualisiere()
    QTest.mouseClick(w.btn_entfernen, Qt.MouseButton.LeftButton)
    assert letzter(s) == ("entfernen", a2.id)


def test_ui_3_race_zeigt_warnung(baue: Any, qtbot: QtBot) -> None:
    a1 = eintrag()
    s = AttrappenSitzung(bild(eintraege=[a1]))
    s.fehler["entfernen"] = ValueError("Eintrag kann nicht entfernt werden: läuft")
    w, dialoge = baue(s)
    w.tabelle.waehle(a1.id)
    w.aktualisiere()
    QTest.mouseClick(w.btn_entfernen, Qt.MouseButton.LeftButton)
    assert isinstance(dialoge.gesehen[-1], QMessageBox)
    assert "läuft" in dialoge.gesehen[-1].text()


# --- UI-4 -----------------------------------------------------------------------------------


def test_ui_4_bearbeiten_auch_waehrend_des_laufs(baue: Any, qtbot: QtBot) -> None:
    lauf, warte = eintrag(zustand="laeuft", name="L", nummer=1), eintrag(name="W")
    s = AttrappenSitzung(bild(durchgang=Z.LAEUFT, eintraege=[lauf, warte]))
    w, _ = baue(s)
    w.tabelle.waehle(warte.id)
    assert w.editor.modus == "bearbeiten"
    assert w.editor.titel.text() == "Messung 02 (vorl.) bearbeiten"
    w.editor.name.setText("W_neu")
    zeile = w.editor.parameter[2]  # mittelung.anzahl
    zeile.aendern.setChecked(True)
    zeile.eingabe.setText("10")
    w.editor.limit_eigen.setChecked(True)
    w.editor.limit.setValue(300)
    QTest.mouseClick(w.editor.btn_uebernehmen, Qt.MouseButton.LeftButton)
    name, eid, aenderungen = letzter(s)
    assert name == "bearbeiten" and eid == warte.id
    assert aenderungen["name"] == "W_neu"
    assert aenderungen["parameter"] == {"mittelung.anzahl": 10}
    assert aenderungen["zeitlimit_s"] == 300.0
    assert zelle(w, 1, 2) == "W_neu"
    assert zelle(w, 1, 4) == "Mittelung Anzahl 10"
    assert zelle(w, 1, 5) == "300 s"
    assert w.editor.modus == "bearbeiten" and not w.editor.geaendert


def test_ui_4_anzeigemodus_fuer_laufende_und_fertige(baue: Any) -> None:
    lauf = eintrag(zustand="laeuft", nummer=2)
    fertig = eintrag(zustand="fertig", messdatei="D:/d/01_M.svd", fehlertext=None, nummer=1)
    fehler = eintrag(zustand="fehler", fehlerart="zeitlimit", fehlertext="zu lang", nummer=3)
    s = AttrappenSitzung(bild(durchgang=Z.LAEUFT, eintraege=[fertig, lauf, fehler]))
    w, _ = baue(s)
    w.tabelle.waehle(lauf.id)
    assert w.editor.modus == "anzeigen"
    assert w.editor.titel.text() == "Messung 02 (läuft)"
    assert not w.editor.name.isEnabled() and not w.editor.btn_set.isEnabled()
    assert all(not p.aendern.isEnabled() for p in w.editor.parameter)
    assert not w.editor.nicht_aenderbar.isHidden()
    assert w.editor.nicht_aenderbar.text() == "Dieser Eintrag ist nicht mehr änderbar."
    assert w.editor.btn_uebernehmen.isHidden() and w.editor.btn_verwerfen.isHidden()
    w.tabelle.waehle(fertig.id)
    assert w.editor.titel.text() == "Messung 01 (fertig)"
    assert "Messdatei: D:/d/01_M.svd" in w.editor.details.text()
    w.tabelle.waehle(fehler.id)
    assert "Fehler (zeitlimit): zu lang" in w.editor.details.text()


def test_ui_4_pausenpunkt_anzeigen_und_auswahl_aufheben(baue: Any) -> None:
    p = eintrag("pausenpunkt", "erledigt")
    s = AttrappenSitzung(bild(eintraege=[p]))
    w, _ = baue(s)
    w.tabelle.waehle(p.id)
    assert w.editor.modus == "anzeigen" and w.editor.titel.text() == "Pausenpunkt (bestätigt)"
    w.tabelle.waehle(None)
    assert w.editor.modus == "leer"
    assert not w.editor.leer_text.isHidden()


# --- UI-5 -----------------------------------------------------------------------------------


def test_ui_5_sofortige_pruefung(baue: Any, qtbot: QtBot, tmp_path: Path) -> None:
    s = AttrappenSitzung(bild())
    w, _ = baue(s)
    taste(qtbot, w, Qt.Key.Key_N, Qt.KeyboardModifier.ControlModifier)
    QTest.keyClicks(w.editor.name, "M1")
    w.editor.set_feld.setText(set_datei(tmp_path))
    assert w.editor.btn_uebernehmen.isEnabled()
    zeile = next(p for p in w.editor.parameter if p.spec.schluessel == "mittelung.anzahl")
    assert not zeile.eingabe.isEnabled() and zeile.eingabe.placeholderText() == "(aus .set)"
    zeile.aendern.setChecked(True)
    QTest.keyClicks(zeile.eingabe, "2")
    assert not zeile.fehler.isHidden()
    assert zeile.fehler.text() == "✖ Mittelung Anzahl: 2 liegt außerhalb 3 … 10000."
    assert not w.editor.btn_uebernehmen.isEnabled()
    assert w.editor.btn_uebernehmen.toolTip().startswith("Eingaben prüfen: ✖ Mittelung Anzahl")
    zeile.eingabe.setText("20")
    assert zeile.fehler.isHidden() and w.editor.btn_uebernehmen.isEnabled()
    for zeichen in '\\/:*?"<>|':
        w.editor.name.setText(f"a{zeichen}b")
        assert not w.editor.btn_uebernehmen.isEnabled(), zeichen
        assert "unzulässige Zeichen" in w.editor.name_fehler.text()
        assert not w.editor.name_fehler.isHidden()
    w.editor.name.setText("ok")
    assert w.editor.btn_uebernehmen.isEnabled()
    taste(qtbot, w.editor.name, Qt.Key.Key_Return, Qt.KeyboardModifier.ControlModifier)
    assert letzter(s)[2].parameter == {"mittelung.anzahl": 20}


def test_ui_5_parameterzeilen_aus_dem_katalog(baue: Any) -> None:
    katalog = Parameterkatalog(KATALOG)
    katalog.registrieren(
        ParameterSpec(
            schluessel="trigger.pegel_v",
            typ="float",
            einheit="V",
            com_gruppe="trigger",
            minimum=-10,
            maximum=10,
        )
    )
    w, _ = baue(AttrappenSitzung(bild()), katalog=katalog)
    namen = [p.spec.schluessel for p in w.editor.parameter]
    assert namen == [s.schluessel for s in katalog]
    assert w.editor.findChild(QLineEdit, "param_trigger.pegel_v") is not None
    typ = next(p for p in w.editor.parameter if p.spec.schluessel == "mittelung.typ")
    typ.aendern.setChecked(True)
    assert typ.lies() == ("Magnitude", None) or typ.lies()[0] in typ.spec.erlaubt


# --- UI-6 -----------------------------------------------------------------------------------


def test_ui_6_pausenpunkt_anlegen_bearbeiten(baue: Any, qtbot: QtBot) -> None:
    m = eintrag()
    s = AttrappenSitzung(bild(eintraege=[m]))
    w, _ = baue(s)
    w.tabelle.waehle(m.id)
    taste(
        qtbot,
        w,
        Qt.Key.Key_N,
        Qt.KeyboardModifier.ControlModifier | Qt.KeyboardModifier.ShiftModifier,
    )
    assert w.editor.modus == "neu_pausenpunkt"
    assert w.editor.titel.text() == "Neuer Pausenpunkt"
    assert fokus_ist(w.editor.text)
    assert not w.editor.btn_uebernehmen.isEnabled()
    QTest.keyClicks(w.editor.text, "Sensorkopf umsetzen")
    assert w.editor.btn_uebernehmen.isEnabled()
    QTest.mouseClick(w.editor.btn_uebernehmen, Qt.MouseButton.LeftButton)
    _n, pos, p = letzter(s)
    assert pos == 1 and isinstance(p, Pausenpunkt)
    assert zelle(w, 1, 0) == "–"
    assert zelle(w, 1, 1) == "⏸ Pausenpunkt"
    assert zelle(w, 1, 2) == "Pausenpunkt: Sensorkopf umsetzen"
    assert w.tabelle.columnSpan(1, 2) == 4
    # bearbeiten, verschieben, entfernen wie eine Messung
    assert w.editor.modus == "bearbeiten" and w.editor.titel.text() == "Pausenpunkt bearbeiten"
    w.editor.text.setText("")
    assert not w.editor.btn_uebernehmen.isEnabled()
    w.editor.text.setText("Umbau")
    QTest.mouseClick(w.editor.btn_uebernehmen, Qt.MouseButton.LeftButton)
    assert letzter(s) == ("bearbeiten", p.id, {"text": "Umbau"})
    QTest.mouseClick(w.btn_hoch, Qt.MouseButton.LeftButton)
    assert letzter(s) == ("verschieben", p.id, 0)
    QTest.mouseClick(w.btn_entfernen, Qt.MouseButton.LeftButton)
    assert letzter(s) == ("entfernen", p.id)


# --- UI-7 -----------------------------------------------------------------------------------


def test_ui_7_alle_zustaende_gleichzeitig(baue: Any) -> None:
    eintraege = [
        eintrag(zustand="fertig", nummer=1),
        eintrag("pausenpunkt", "erledigt"),
        eintrag(zustand="fehler", uebersprungen=True, nummer=2),
        eintrag(zustand="abgebrochen", nummer=3),
        eintrag(zustand="laeuft", nummer=4),
        eintrag("pausenpunkt", "erreicht"),
        eintrag(),
        eintrag("pausenpunkt"),
    ]
    s = AttrappenSitzung(bild(durchgang=Z.LAEUFT, eintraege=eintraege))
    w, _ = baue(s)
    texte = [zelle(w, r, 1) for r in range(w.tabelle.rowCount())]
    assert texte == [
        "✔ fertig",
        "✔ bestätigt",
        "✖ Fehler (übersprungen)",
        "■ abgebrochen",
        "▶ läuft",
        "⏸ wartet auf Bestätigung",
        "○ wartend",
        "⏸ Pausenpunkt",
    ]
    assert [zelle(w, r, 0) for r in range(8)] == ["01", "–", "02", "03", "04", "–", "(05)", "–"]
    nr_vorl = w.tabelle.item(6, 0)
    assert nr_vorl is not None and nr_vorl.font().italic()
    assert nr_vorl.toolTip().startswith("Vorläufige Nummer.")
    name = w.tabelle.item(4, 2)
    assert name is not None and name.font().bold()


# --- UI-8 -----------------------------------------------------------------------------------


def test_ui_8_fortschritt_und_statuswechsel_unter_300_ms(baue: Any, qtbot: QtBot) -> None:
    m = eintrag(zustand="laeuft", nummer=1)
    s = AttrappenSitzung(
        bild(durchgang=Z.LAEUFT, eintraege=[m], fortschritt=fortschritt(m.id, 0.4))
    )
    w, _ = baue(s, takt_ms=100)
    assert "40 %" in w.fortschritt_text.volltext()
    assert "geschätzt" in w.fortschritt_text.volltext()
    assert w.fortschritt_balken.value() > 0
    assert w.fortschritt_beschriftung.text() == "Messung 01:"
    s.setze(eintraege=[eintrag(id=m.id, zustand="fertig")], fortschritt=None)
    t0 = time.monotonic()
    qtbot.waitUntil(lambda: zelle(w, 0, 1) == "✔ fertig", timeout=300)
    assert time.monotonic() - t0 <= 0.3
    s.setze(
        eintraege=[eintrag(id=m.id, zustand="laeuft")],
        fortschritt=fortschritt(m.id, 1.2, zeitlimit_rest_s=130),
    )
    w.aktualisiere()
    assert w.fortschritt_balken.value() == 99
    assert w.fortschritt_text.volltext().startswith("Schätzung überschritten – Messung läuft noch")
    s.setze(fortschritt=fortschritt(m.id, None))
    w.aktualisiere()
    assert w.fortschritt_balken.maximum() == 0
    s.setze(durchgang=Z.BEREIT, fortschritt=None)
    w.aktualisiere()
    assert w.fortschritt_text.volltext() == "Kein Durchgang läuft."
    assert not w.fortschritt_balken.isEnabled()
    assert w.fortschritt_balken.focusPolicy() == Qt.FocusPolicy.NoFocus


# --- UI-9 -----------------------------------------------------------------------------------

AKTIVIERUNG = {
    Z.BEREIT: (True, False, "Pausieren (F6)", False),
    Z.LAEUFT: (False, True, "Pausieren (F6)", True),
    Z.PAUSE_ANGEFORDERT: (False, False, "Pause angefordert", True),
    Z.PAUSIERT: (False, True, "Fortsetzen (F6)", True),
    Z.WARTET_AUF_BESTAETIGUNG: (False, False, "Pausieren (F6)", True),
    Z.WARTET_AUF_ENTSCHEIDUNG: (False, False, "Pausieren (F6)", True),
    Z.ABBRUCH_LAEUFT: (False, False, "Pausieren (F6)", False),
    Z.GERAET_UNKLAR: (False, False, "Pausieren (F6)", False),
    Z.BEENDET: (True, False, "Pausieren (F6)", False),
}


@pytest.mark.parametrize("zustand", list(Z))
def test_ui_9_knoepfe_je_zustand(baue: Any, zustand: Z) -> None:
    s = AttrappenSitzung(bild(durchgang=zustand, eintraege=[eintrag()]))
    w, _ = baue(s)
    start, pause, text, abbrechen = AKTIVIERUNG[zustand]
    assert w.btn_start.isEnabled() is start
    assert w.btn_pause.isEnabled() is pause
    assert w.btn_pause.text() == text
    assert w.btn_abbrechen.isEnabled() is abbrechen
    for b in (w.btn_start, w.btn_pause, w.btn_abbrechen):
        if not b.isEnabled():
            assert " – " in b.defaultAction().toolTip()


def test_ui_9_befehl_genau_einmal_bis_zum_naechsten_bild(baue: Any, qtbot: QtBot) -> None:
    s = AttrappenSitzung(bild(durchgang=Z.LAEUFT, eintraege=[eintrag(zustand="laeuft")]))
    w, _ = baue(s)
    QTest.mouseClick(w.btn_pause, Qt.MouseButton.LeftButton)
    QTest.mouseClick(w.btn_pause, Qt.MouseButton.LeftButton)
    taste(qtbot, w, Qt.Key.Key_F6)
    assert s.namen() == ["pausiere"]
    assert "Befehl wird ausgeführt" in w.act_pause.toolTip()
    s.setze(durchgang=Z.PAUSIERT)
    w.aktualisiere()
    assert w.btn_pause.text() == "Fortsetzen (F6)" and w.btn_pause.isEnabled()
    taste(qtbot, w, Qt.Key.Key_F6)
    assert s.namen() == ["pausiere", "setze_fort"]


# --- UI-10 ----------------------------------------------------------------------------------


@pytest.mark.parametrize("ausloeser", ["knopf", "f8"])
def test_ui_10_abbrechen_mit_bestaetigung(baue: Any, qtbot: QtBot, ausloeser: str) -> None:
    s = AttrappenSitzung(bild(durchgang=Z.LAEUFT, eintraege=[eintrag(zustand="laeuft")]))
    w, dialoge = baue(s)

    def ausloesen() -> None:
        if ausloeser == "knopf":
            QTest.mouseClick(w.btn_abbrechen, Qt.MouseButton.LeftButton)
        else:
            taste(qtbot, w, Qt.Key.Key_F8)

    dialoge.aktionen.append(klicke("Weiter messen"))
    ausloesen()
    box = dialoge.gesehen[-1]
    assert isinstance(box, QMessageBox)
    assert box.windowTitle() == "Durchgang abbrechen?"
    assert box.text().startswith("Die laufende Messung wird sofort gestoppt.")
    assert box.defaultButton().text() == "Weiter messen"
    assert box.escapeButton().text() == "Weiter messen"
    assert s.befehle == []
    dialoge.aktionen.append(lambda d: d.escapeButton().click())
    ausloesen()
    assert s.befehle == []
    dialoge.aktionen.append(klicke("Durchgang abbrechen"))
    ausloesen()
    assert s.namen() == ["brich_ab"]


def test_ui_10_ohne_laufende_messung_zurueck(baue: Any, qtbot: QtBot) -> None:
    s = AttrappenSitzung(bild(durchgang=Z.PAUSIERT, eintraege=[eintrag()]))
    w, dialoge = baue(s)
    dialoge.aktionen.append(klicke("Zurück"))
    QTest.mouseClick(w.btn_abbrechen, Qt.MouseButton.LeftButton)
    box = dialoge.gesehen[-1]
    assert isinstance(box, QMessageBox)
    assert box.text() == "Der Durchgang wird beendet. Nicht gestartete Messungen bleiben wartend."
    assert box.defaultButton().text() == "Zurück"
    assert s.befehle == []


# --- UI-11 ----------------------------------------------------------------------------------


def test_ui_11_pausenpunkt_bestaetigen(baue: Any, qtbot: QtBot) -> None:
    p = eintrag("pausenpunkt", "erreicht", text="Sensorkopf umsetzen")
    s = AttrappenSitzung(bild(durchgang=Z.LAEUFT, eintraege=[p]))
    w, _ = baue(s)
    taste(qtbot, w, Qt.Key.Key_F7)
    assert s.befehle == []  # F7 ohne Fall 5 wirkungslos
    w.tabelle.setFocus()
    fokus = QApplication.focusWidget()
    s.setze(durchgang=Z.WARTET_AUF_BESTAETIGUNG, pausenpunkt_id=p.id)
    w.aktualisiere()
    assert fokus_ist(fokus)
    assert w.hinweisband.property("fall") == "5"
    assert "Pausenpunkt erreicht: Sensorkopf umsetzen" in w.hinweisband.text.text()
    assert zelle(w, 0, 1) == "⏸ wartet auf Bestätigung"
    knopf = w.hinweisband.knopf("bestaetigen")
    assert knopf is not None and knopf.text() == "Bestätigen (F7)"
    assert w.hinweisband.accessibleName() == "Hinweis"
    assert "Sensorkopf" in w.hinweisband.accessibleDescription()
    QTest.mouseClick(knopf, Qt.MouseButton.LeftButton)
    assert s.namen() == ["bestaetige"]
    s.setze()  # neues Bild: Sperre aufgehoben
    w.aktualisiere()
    taste(qtbot, w, Qt.Key.Key_F7)
    assert s.namen() == ["bestaetige", "bestaetige"]


# --- UI-12 ----------------------------------------------------------------------------------


@pytest.mark.parametrize(
    ("knopf", "entscheidung"),
    [
        ("wiederholen", Fehlerentscheidung.WIEDERHOLEN),
        ("ueberspringen", Fehlerentscheidung.UEBERSPRINGEN),
        ("abbrechen", Fehlerentscheidung.ABBRECHEN),
    ],
)
def test_ui_12_fehlerentscheidung(
    baue: Any, qtbot: QtBot, knopf: str, entscheidung: Fehlerentscheidung
) -> None:
    m = eintrag(zustand="fehler", name="Platte_Mitte", nummer=1)
    s = AttrappenSitzung(
        bild(
            durchgang=Z.WARTET_AUF_ENTSCHEIDUNG,
            eintraege=[m],
            fehler_eintrag_id=m.id,
            fehlertext="Zeitlimit überschritten",
        )
    )
    w, dialoge = baue(s)
    assert w.hinweisband.property("fall") == "4"
    text = w.hinweisband.text.text()
    assert "Messung 01 „Platte_Mitte“ fehlgeschlagen: Zeitlimit überschritten" in text
    assert "vorläufiges verhalten (o1)" in text.lower()
    assert w.lbl_fehlerstrategie.text() == "Fehlerstrategie: vorläufig (O1)"
    for k in ("wiederholen", "ueberspringen", "abbrechen"):
        b = w.hinweisband.knopf(k)
        assert b is not None and not b.isDefault() and not b.autoDefault()
    if knopf == "abbrechen":
        dialoge.aktionen.append(klicke("Zurück"))
        QTest.mouseClick(w.hinweisband.knopf(knopf), Qt.MouseButton.LeftButton)
        assert s.befehle == []
        dialoge.aktionen.append(klicke("Durchgang abbrechen"))
    QTest.mouseClick(w.hinweisband.knopf(knopf), Qt.MouseButton.LeftButton)
    assert s.befehle == [("entscheide", entscheidung)]


# --- UI-13 ----------------------------------------------------------------------------------


def test_ui_13_pause_angefordert_und_pausiert(baue: Any, qtbot: QtBot) -> None:
    lauf, naechste = eintrag(zustand="laeuft", nummer=1), eintrag(name="Platte_Rand")
    s = AttrappenSitzung(bild(durchgang=Z.PAUSE_ANGEFORDERT, eintraege=[lauf, naechste]))
    w, _ = baue(s)
    assert w.hinweisband.property("fall") == "6a"
    assert w.hinweisband.text.text() == (
        "⏸ Pause angefordert. Messung 01 läuft zu Ende, danach startet keine neue."
    )
    assert not w.btn_pause.isEnabled() and w.btn_pause.text() == "Pause angefordert"
    s.setze(
        durchgang=Z.PAUSIERT, eintraege=[eintrag(id=lauf.id, zustand="fertig", nummer=1), naechste]
    )
    w.aktualisiere()
    assert w.hinweisband.property("fall") == "6b"
    assert "Nächste wartende Messung: Nr 01 (vorl.) „Platte_Rand“." in w.hinweisband.text.text()
    QTest.mouseClick(w.hinweisband.knopf("fortsetzen"), Qt.MouseButton.LeftButton)
    assert s.namen() == ["setze_fort"]


# --- UI-14 ----------------------------------------------------------------------------------


@pytest.mark.parametrize("zustand", list(Z))
def test_ui_14_betriebsart_immer_sichtbar(baue: Any, zustand: Z) -> None:
    s = AttrappenSitzung(bild(durchgang=zustand, betriebsart=Betriebsart.MESSEN))
    w, _ = baue(s)
    assert w.btn_betriebsart.text() == "MESSEN"
    assert w.windowTitle() == "LDV-Warteschlange – MESSEN"
    assert w.btn_betriebsart.property("messen") == "true"
    assert w.btn_betriebsart.isEnabled() is (zustand in (Z.BEREIT, Z.BEENDET))
    if not w.btn_betriebsart.isEnabled():
        assert w.btn_betriebsart.toolTip() == "Während eines Durchgangs nicht änderbar"


def test_ui_14_messen_nur_ueber_freischaltung(baue: Any) -> None:
    s = AttrappenSitzung(bild())
    s.voraussetzungen = tuple(
        Voraussetzung(name=v.name, erfuellt=v.name != "trockenlauf", text=v.text)
        for v in VORAUSSETZUNGEN_ERFUELLT
    )
    w, dialoge = baue(s)
    assert w.btn_betriebsart.property("messen") == "false"
    dialoge.aktionen.append(ablehnen)
    w.act_betriebsart[Betriebsart.MESSEN].trigger()
    dialog = dialoge.gesehen[-1]
    assert isinstance(dialog, MessenFreischaltenDialog)
    assert not dialog.btn_freischalten.isEnabled()
    assert dialog.btn_abbrechen.isDefault()
    abhilfe = [
        x.text() for x in dialog.findChildren(QLabel) if x.objectName().startswith("abhilfe_")
    ]
    assert any("Trockenlauf mit dem ersten Eintrag durchführen." in t for t in abhilfe)
    assert s.befehle == []
    assert w.act_betriebsart[Betriebsart.SIMULATOR].isChecked()
    s.voraussetzungen = tuple(
        Voraussetzung(name=v.name, erfuellt=True, text="ok") for v in s.voraussetzungen
    )
    dialoge.aktionen.append(klicke("Freischalten"))
    w.act_betriebsart[Betriebsart.MESSEN].trigger()
    assert s.befehle == [("betriebsart", Betriebsart.MESSEN)]
    assert w.btn_betriebsart.text() == "MESSEN"
    assert w.btn_betriebsart.property("messen") == "true"
    # andere Betriebsarten direkt, ohne Dialog
    anzahl = len(dialoge.gesehen)
    w.act_betriebsart[Betriebsart.NUR_LESEN].trigger()
    assert len(dialoge.gesehen) == anzahl
    assert letzter(s) == ("betriebsart", Betriebsart.NUR_LESEN)
    assert w.btn_betriebsart.text() == "NUR LESEN"


def test_ui_14_fehler_der_sitzung_beim_wechsel(baue: Any) -> None:
    s = AttrappenSitzung(bild())
    s.fehler["betriebsart"] = ValueError("MESSEN nicht freigeschaltet: Git-Hash unbekannt")
    w, dialoge = baue(s)
    dialoge.aktionen.append(klicke("Freischalten"))
    w.act_betriebsart[Betriebsart.MESSEN].trigger()
    meldung = dialoge.gesehen[-1]
    assert isinstance(meldung, QMessageBox) and "Git-Hash" in meldung.text()
    assert w.act_betriebsart[Betriebsart.SIMULATOR].isChecked()


# --- UI-15 ----------------------------------------------------------------------------------


def test_ui_15_start_in_messen_mit_bestaetigung(baue: Any, qtbot: QtBot) -> None:
    m1, m2 = eintrag(name="A"), eintrag(name="B")
    s = AttrappenSitzung(
        bild(
            betriebsart=Betriebsart.MESSEN, eintraege=[m1, m2], start_vorschau=vorschau_zu([m1, m2])
        )
    )
    w, dialoge = baue(s)
    gesehen: dict[str, Any] = {}

    def pruefen_und_abbrechen(d: QDialog) -> None:
        assert isinstance(d, DurchgangStartenDialog)
        gesehen["titel"] = d.windowTitle()
        gesehen["zeilen"] = d.findChild(QWidget, "start_tabelle").rowCount()  # type: ignore[union-attr]
        gesehen["warnung"] = d.findChild(QLabel, "start_generator_warnung").text()  # type: ignore[union-attr]
        gesehen["default"] = d.btn_abbrechen.isDefault()
        d.eingabe.setText("messen")
        gesehen["klein"] = d.btn_starten.isEnabled()
        d.eingabe.setText("MESSEN")
        gesehen["gross"] = d.btn_starten.isEnabled()
        d.reject()

    dialoge.aktionen.append(pruefen_und_abbrechen)
    taste(qtbot, w, Qt.Key.Key_F5)
    assert gesehen["titel"] == "Durchgang starten: echte Messung"
    assert gesehen["zeilen"] == 2
    assert gesehen["warnung"].startswith("✖ Generatorzustand unbekannt")  # nicht gelesen
    assert gesehen["default"] and not gesehen["klein"] and gesehen["gross"]
    assert s.befehle == []

    def bestaetigen(d: QDialog) -> None:
        assert isinstance(d, DurchgangStartenDialog)
        d.eingabe.setText("MESSEN")
        d.btn_starten.click()

    dialoge.aktionen.append(bestaetigen)
    QTest.mouseClick(w.btn_start, Qt.MouseButton.LeftButton)
    assert s.befehle == [("starte", "messen", True)]
    assert s.letzter_start == (Betriebsart.MESSEN, s.bild.warteschlangen_kennung)


def test_u5_b1_startdialog_zeigt_vorschau_und_warnt_nur_bei_bedarf(baue: Any, qtbot: QtBot) -> None:
    m1, m2 = eintrag(name="A"), eintrag(name="B")
    gesehen: dict[str, Any] = {}

    def lies(d: QDialog) -> None:
        assert isinstance(d, DurchgangStartenDialog)
        tab = d.tabelle
        gesehen["zeile"] = [tab.item(0, c).text() for c in range(tab.columnCount())]  # type: ignore[union-attr]
        gesehen["anzahl"] = d.findChild(QLabel, "start_anzahl").text()  # type: ignore[union-attr]
        gesehen["generator"] = d.findChild(QLabel, "start_generator").text()  # type: ignore[union-attr]
        gesehen["warnung"] = d.warnung.text()
        gesehen["warnung_sichtbar"] = not d.warnung.isHidden()
        d.reject()

    for generator, sichtbar, anfang in (
        (GENERATOR_AUS, False, ""),
        (GENERATOR_AN, True, "✖ Generator ist aktiv"),
        (None, True, "✖ Generatorzustand unbekannt"),
    ):
        vorschau = vorschau_zu([m1, m2], messpunkte=9 if generator else None, generator=generator)
        s = AttrappenSitzung(
            bild(betriebsart=Betriebsart.MESSEN, eintraege=[m1, m2], start_vorschau=vorschau)
        )
        w, dialoge = baue(s)
        dialoge.aktionen.append(lies)
        QTest.mouseClick(w.btn_start, Qt.MouseButton.LeftButton)
        assert gesehen["warnung_sichtbar"] is sichtbar
        assert gesehen["warnung"].startswith(anfang)
        assert gesehen["zeile"][0] == "01"
        assert gesehen["zeile"][2].endswith("01_A.svd")
        if generator is None:
            assert gesehen["zeile"][3:] == ["unbekannt", "unbekannt"]
            assert gesehen["anzahl"] == "2 Messungen, Messpunkte insgesamt: unbekannt"
        else:
            assert gesehen["zeile"][3] == "9"
            assert gesehen["anzahl"].startswith("2 Messungen, 18 Messpunkte insgesamt")
        assert gesehen["generator"].startswith("Generator (gelesen")
        assert s.befehle == []


def test_ui_15_simulator_ohne_trockenlauf_mit_dialog(baue: Any, qtbot: QtBot) -> None:
    s = AttrappenSitzung(bild(eintraege=[eintrag()]))
    w, dialoge = baue(s)
    QTest.mouseClick(w.btn_start, Qt.MouseButton.LeftButton)
    assert dialoge.gesehen == []
    assert s.befehle == [("starte", "simulator", False)]
    s2 = AttrappenSitzung(bild(betriebsart=Betriebsart.TROCKENLAUF, eintraege=[eintrag()]))
    w2, dialoge2 = baue(s2)
    dialoge2.aktionen.append(klicke("Abbrechen"))
    QTest.mouseClick(w2.btn_start, Qt.MouseButton.LeftButton)
    box = dialoge2.gesehen[-1]
    assert isinstance(box, QMessageBox)
    assert (
        box.text()
        == "Ein Trockenlauf ändert die aktuellen PSV-Einstellungen. Es wird nicht gescannt."
    )
    assert box.defaultButton().text() == "Abbrechen"
    assert s2.befehle == []
    dialoge2.aktionen.append(klicke("Trockenlauf starten"))
    QTest.mouseClick(w2.btn_start, Qt.MouseButton.LeftButton)
    assert s2.befehle == [("starte", "trockenlauf", False)]


# --- UI-16 / U4-4 ---------------------------------------------------------------------------


def test_ui_16_waechter_und_bedienbarkeit_mit_haengendem_simulator(
    baue: Any, qtbot: QtBot, tmp_path: Path
) -> None:
    uhr = Echtzeituhr()
    erzeugt: list[Simulator] = []

    def fabrik(art: Betriebsart) -> Messgeraet:
        sim = Simulator(
            uhr.monotonic,
            betriebsart=art.value,
            drehbuch=[HaengenderAufruf(vorgang=0, methode="lade_einstellungen", max_echtzeit_s=20)],
            konfiguration=SimulatorKonfiguration(punkte_anzahl=2, punktdauer_s=0.05),
        )
        erzeugt.append(sim)
        return sim

    wurzel = tmp_path / "daten"
    wurzel.mkdir()
    s = Sitzung(geraete_fabrik=fabrik, uhr=uhr, messdaten_wurzel=wurzel, aufruf_warnung_s=0.3)
    s.einfuegen(0, Messung(name="M1", einstellungsdatei=set_datei(tmp_path)))
    s.starte_threads(waechter_takt_s=0.05)
    try:
        w, _ = baue(s, takt_ms=100)
        qtbot.waitUntil(lambda: w.bild.verbunden, timeout=3000)
        QTest.mouseClick(w.btn_start, Qt.MouseButton.LeftButton)
        qtbot.waitUntil(lambda: w.hinweisband.property("fall") == "3", timeout=3000)
        text = w.hinweisband.text.text()
        assert text.startswith("⚠ PSV reagiert nicht seit") and "am Gerät prüfen" in text
        # GUI verarbeitet weiter Eingaben, während der Geräte-Thread hängt
        QTest.mouseClick(w.btn_messung_neu, Qt.MouseButton.LeftButton)
        assert w.editor.modus == "neu_messung"
        erster = text
        qtbot.waitUntil(lambda: w.hinweisband.text.text() != erster, timeout=3000)  # Zahl live
        assert "Warnung: PSV reagiert nicht" in w.protokoll.toPlainText()
    finally:
        for sim in erzeugt:
            sim.haenger_loesen()
        assert s.beende_threads(5.0)


# --- UI-17 ----------------------------------------------------------------------------------


def test_ui_17_geraet_unklar(baue: Any, qtbot: QtBot) -> None:
    s = AttrappenSitzung(
        bild(
            durchgang=Z.GERAET_UNKLAR,
            betriebsart=Betriebsart.MESSEN,
            waechter_s=70.0,
            eintraege=[eintrag(), eintrag(zustand="laeuft")],
        )
    )
    w, _ = baue(s)
    assert w.hinweisband.property("fall") == "1"
    assert w.hinweisband.text.text().startswith("✖ Gerätezustand unklar.")
    aktiv = sorted(
        b.objectName()
        for b in w.findChildren(QAbstractButton)
        if b.isVisible() and b.isEnabled() and b.objectName().startswith("btn_")
    )
    assert aktiv == ["btn_band_trennen", "btn_speichern", "btn_verbinden"]
    assert "Gerätezustand unklar" in w.btn_geraet.toolTip()
    assert w.btn_verbinden.text() == "Trennen"
    QTest.mouseClick(w.hinweisband.knopf("trennen"), Qt.MouseButton.LeftButton)
    assert s.namen() == ["trenne"]


# --- UI-18 ----------------------------------------------------------------------------------


def test_ui_18_beendet_zusammenfassung_und_neustart(
    baue: Any, qtbot: QtBot, monkeypatch: pytest.MonkeyPatch
) -> None:
    s = AttrappenSitzung(
        bild(
            durchgang=Z.BEENDET,
            ergebnis=DurchgangErgebnis.ABGEBROCHEN,
            zusammenfassung=zusammenfassung(fertig=1, abgebrochen=1, wartend=3),
            durchgangsordner="/daten/2026-11-02_simulator",
            eintraege=[eintrag(zustand="fertig"), eintrag(zustand="abgebrochen"), eintrag()],
        )
    )
    w, _ = baue(s)
    assert w.hinweisband.property("fall") == "7"
    assert w.hinweisband.text.text() == (
        "■ Durchgang abgebrochen: 1 fertig, 1 abgebrochen, 3 nicht gestartet (bleiben wartend)."
    )
    geoeffnet: list[str] = []
    monkeypatch.setattr(w, "_oeffne_ordner", geoeffnet.append)
    QTest.mouseClick(w.hinweisband.knopf("ordner"), Qt.MouseButton.LeftButton)
    assert geoeffnet == ["/daten/2026-11-02_simulator"]
    QTest.mouseClick(w.hinweisband.knopf("schliessen"), Qt.MouseButton.LeftButton)
    assert w.hinweisband.property("fall") == "8"
    # Start in BEENDET: ein Startbefehl, das Quittieren übernimmt die Sitzung (U5/B7)
    QTest.mouseClick(w.btn_start, Qt.MouseButton.LeftButton)
    assert s.namen() == ["starte"]


def test_ui_18_start_in_beendet_mit_echter_sitzung(baue: Any, qtbot: QtBot, tmp_path: Path) -> None:
    s, _f, _u = echte_sitzung(tmp_path)
    s.einfuegen(0, Messung(name="M1", einstellungsdatei=set_datei(tmp_path)))
    w, _ = baue(s)
    QTest.mouseClick(w.btn_start, Qt.MouseButton.LeftButton)
    s.verarbeite()
    w.aktualisiere()
    assert w.bild.durchgang is Z.BEENDET
    assert w.hinweisband.text.text() == "✔ Durchgang beendet: 1 fertig."
    s.einfuegen(1, Messung(name="M2", einstellungsdatei=set_datei(tmp_path)))
    w.aktualisiere()
    QTest.mouseClick(w.btn_start, Qt.MouseButton.LeftButton)  # quittiert und startet (B7)
    s.verarbeite()
    w.aktualisiere()
    assert [zelle(w, r, 1) for r in range(2)] == ["✔ fertig", "✔ fertig"]
    assert w.bild.durchgang is Z.BEENDET


# --- UI-19 / U4-1: Rauchtest über die GUI ---------------------------------------------------


def test_ui_19_rauchtest_durchgang_ueber_die_gui(baue: Any, qtbot: QtBot, tmp_path: Path) -> None:
    s, _f, _u = echte_sitzung(tmp_path)
    w, _ = baue(s)
    datei = set_datei(tmp_path)
    w.editor.datei_waehlen = lambda _o: datei
    for name in ("M1", "M2", "M3"):
        taste(qtbot, w, Qt.Key.Key_N, Qt.KeyboardModifier.ControlModifier)
        QTest.keyClicks(w.editor.name, name)
        QTest.mouseClick(w.editor.btn_set, Qt.MouseButton.LeftButton)
        taste(qtbot, w.editor.name, Qt.Key.Key_Return, Qt.KeyboardModifier.ControlModifier)
    w.tabelle.waehle(w.tabelle.ids[0])
    taste(
        qtbot,
        w,
        Qt.Key.Key_N,
        Qt.KeyboardModifier.ControlModifier | Qt.KeyboardModifier.ShiftModifier,
    )
    QTest.keyClicks(w.editor.text, "Umbau")
    taste(qtbot, w.editor.text, Qt.Key.Key_Return, Qt.KeyboardModifier.ControlModifier)
    assert [zelle(w, r, 2) for r in range(4)] == ["M1", "Pausenpunkt: Umbau", "M2", "M3"]
    taste(qtbot, w, Qt.Key.Key_F5)
    s.verarbeite()
    w.aktualisiere()
    assert w.hinweisband.property("fall") == "5"
    taste(qtbot, w, Qt.Key.Key_F7)
    s.verarbeite()
    w.aktualisiere()
    assert w.bild.durchgang is Z.BEENDET
    assert [zelle(w, r, 1) for r in range(4)] == ["✔ fertig", "✔ bestätigt", "✔ fertig", "✔ fertig"]
    protokoll = w.protokoll.toPlainText()
    assert "Pausenpunkt erreicht: Umbau" in protokoll
    zeilen = protokoll.splitlines()
    assert all(z[2] == ":" and z[5] == ":" and z[8:10] == "  " for z in zeilen)


# --- UI-20 ----------------------------------------------------------------------------------


def test_ui_20_speichern_laden_rundlauf(
    baue: Any, qtbot: QtBot, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    s, _f, _u = echte_sitzung(tmp_path)
    datei = set_datei(tmp_path)
    s.einfuegen(0, Messung(name="A", einstellungsdatei=datei, parameter={"fft.linien": 1600}))
    s.einfuegen(1, Pausenpunkt(text="Umbau"))
    w, dialoge = baue(s)
    assert w.ungespeichert()
    ziel = tmp_path / "serie"
    monkeypatch.setattr(w, "_pfad_speichern", lambda: str(ziel))
    taste(qtbot, w, Qt.Key.Key_S, Qt.KeyboardModifier.ControlModifier)
    gespeichert = tmp_path / "serie.warteschlange.json"
    assert gespeichert.is_file()
    assert f"Warteschlange gespeichert: {gespeichert}" in w.protokoll.toPlainText()
    assert not w.ungespeichert()
    vorher = [(e.art, e.id, e.name, e.text, dict(e.parameter)) for e in w.bild.eintraege]
    # Laden bei nicht leerer Liste fragt nach (Standard Abbrechen)
    monkeypatch.setattr(w, "_pfad_laden", lambda: str(gespeichert))
    dialoge.aktionen.append(klicke("Abbrechen"))
    taste(qtbot, w, Qt.Key.Key_O, Qt.KeyboardModifier.ControlModifier)
    frage = dialoge.gesehen[-1]
    assert isinstance(frage, QMessageBox)
    assert frage.text() == "Die aktuelle Warteschlange (2 Einträge) wird ersetzt. Fortfahren?"
    assert frage.defaultButton().text() == "Abbrechen"
    dialoge.aktionen.append(klicke("Ersetzen"))
    taste(qtbot, w, Qt.Key.Key_O, Qt.KeyboardModifier.ControlModifier)
    nachher = [(e.art, e.id, e.name, e.text, dict(e.parameter)) for e in w.bild.eintraege]
    assert nachher == vorher
    assert all(e.zustand == "wartend" for e in w.bild.eintraege)


def test_ui_20_fehlerhafte_datei_und_fehlende_set(
    baue: Any, qtbot: QtBot, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    s, _f, _u = echte_sitzung(tmp_path)
    w, dialoge = baue(s)
    datei = set_datei(tmp_path, "weg.set")
    s.einfuegen(0, Messung(name="A", einstellungsdatei=datei))
    pfad = tmp_path / "x.warteschlange.json"
    s.speichere_warteschlange(pfad)
    roh = json.loads(pfad.read_text(encoding="utf-8"))
    s.entfernen(s.zustandsbild().eintraege[0].id)
    w.aktualisiere()
    kaputt = tmp_path / "kaputt.warteschlange.json"
    roh_kaputt = json.loads(json.dumps(roh))
    roh_kaputt["eintraege"][0]["unbekannt"] = 1
    kaputt.write_text(json.dumps(roh_kaputt), encoding="utf-8")
    monkeypatch.setattr(w, "_pfad_laden", lambda: str(kaputt))
    w.act_laden.trigger()
    fehler = dialoge.gesehen[-1]
    assert isinstance(fehler, QMessageBox)
    assert fehler.windowTitle() == "Datei kann nicht geladen werden"
    assert "eintraege[0]" in fehler.text() or "eintraege" in fehler.text()
    assert w.bild.eintraege == ()
    Path(datei).unlink()
    monkeypatch.setattr(w, "_pfad_laden", lambda: str(pfad))
    w.act_laden.trigger()
    assert zelle(w, 0, 3).startswith("⚠ weg.set")
    assert "Warnung: 1 Einstellungsdateien nicht gefunden" in w.protokoll.toPlainText()


# --- UI-21 ----------------------------------------------------------------------------------


def test_ui_21_tastatur_in_tabelle_und_editor(baue: Any, qtbot: QtBot) -> None:
    eintraege = [eintrag(name=f"M{i}") for i in range(5)]
    s = AttrappenSitzung(bild(eintraege=eintraege))
    w, _ = baue(s)
    w.tabelle.setFocus()
    w.tabelle.waehle(eintraege[0].id)
    taste(qtbot, w.tabelle, Qt.Key.Key_Down)
    assert w.tabelle.gewaehlte_id() == eintraege[1].id
    taste(qtbot, w.tabelle, Qt.Key.Key_End)
    assert w.tabelle.gewaehlte_id() == eintraege[4].id
    taste(qtbot, w.tabelle, Qt.Key.Key_Home)
    assert w.tabelle.gewaehlte_id() == eintraege[0].id
    taste(qtbot, w.tabelle, Qt.Key.Key_Up)
    assert w.tabelle.gewaehlte_id() == eintraege[0].id
    taste(qtbot, w.tabelle, Qt.Key.Key_Return)
    assert fokus_ist(w.editor.name)
    QTest.keyClicks(w.editor.name, "_x")
    taste(qtbot, w.editor.name, Qt.Key.Key_Return, Qt.KeyboardModifier.ControlModifier)
    assert letzter(s)[0] == "bearbeiten" and letzter(s)[2]["name"] == "M0_x"
    QTest.keyClicks(w.editor.name, "y")
    taste(qtbot, w.editor.name, Qt.Key.Key_Escape)
    assert fokus_ist(w.tabelle)
    assert w.editor.name.text() == "M0_x"


def test_ui_21_fokus_und_tabulatorreihenfolge(baue: Any, qtbot: QtBot) -> None:
    s = AttrappenSitzung(
        bild(
            durchgang=Z.BEENDET,
            ergebnis=DurchgangErgebnis.VOLLSTAENDIG,
            durchgangsordner="/d",
            eintraege=[eintrag(zustand="fertig"), eintrag()],
        )
    )
    w, _ = baue(s)
    assert ":focus" in stil.QSS and "border: 2px solid #0B5C73" in stil.QSS
    for b in w.findChildren(QAbstractButton):
        if b.isVisible():
            assert b.focusPolicy() != Qt.FocusPolicy.NoFocus, b.objectName()
    for wid in (w.tabelle, w.protokoll, w.editor.name, w.btn_betriebsart):
        assert wid.focusPolicy() != Qt.FocusPolicy.NoFocus
    w.btn_betriebsart.setFocus()
    reihe = [QApplication.focusWidget().objectName()]  # type: ignore[union-attr]
    for _ in range(20):
        taste(qtbot, QApplication.focusWidget(), Qt.Key.Key_Tab)  # type: ignore[arg-type]
        reihe.append(QApplication.focusWidget().objectName())  # type: ignore[union-attr]
    erwartet = [
        "btn_betriebsart",
        "btn_geraet",
        "btn_einstellungen",
        "btn_messung_neu",
        "btn_pausenpunkt_neu",
        "btn_speichern",
        "btn_laden",
        "btn_start",
        "btn_band_ordner",
        "btn_band_schliessen",
        "tabelle",
    ]
    positionen = [reihe.index(n) for n in erwartet]
    assert positionen == sorted(positionen), reihe


def test_ui_21_tasten_f5_f8_strg_s_o(
    baue: Any, qtbot: QtBot, monkeypatch: pytest.MonkeyPatch
) -> None:
    s = AttrappenSitzung(bild(eintraege=[eintrag()]))
    w, dialoge = baue(s)
    aufrufe: list[str] = []

    def speichern() -> None:
        aufrufe.append("s")

    def laden() -> None:
        aufrufe.append("o")

    monkeypatch.setattr(w, "_pfad_speichern", speichern)
    monkeypatch.setattr(w, "_pfad_laden", laden)
    taste(qtbot, w, Qt.Key.Key_S, Qt.KeyboardModifier.ControlModifier)
    dialoge.aktionen.append(klicke("Ersetzen"))
    taste(qtbot, w, Qt.Key.Key_O, Qt.KeyboardModifier.ControlModifier)
    assert aufrufe == ["s", "o"]
    taste(qtbot, w, Qt.Key.Key_F5)
    assert s.namen() == ["starte"]
    for b in (w.btn_start, w.btn_pause, w.btn_abbrechen, w.btn_messung_neu, w.btn_speichern):
        tip = b.defaultAction().toolTip()
        assert any(k in tip for k in ("F5", "F6", "F8", "Strg+N", "Strg+S")), tip


# --- UI-22 ----------------------------------------------------------------------------------


def test_ui_22_aktualisierung_aendert_auswahl_scroll_und_eingaben_nicht(
    baue: Any, qtbot: QtBot
) -> None:
    eintraege = [eintrag(name=f"M{i}") for i in range(40)]
    s = AttrappenSitzung(bild(eintraege=eintraege, durchgang=Z.LAEUFT))
    w, _ = baue(s)
    ziel = eintraege[25]
    w.tabelle.waehle(ziel.id)
    w.tabelle.verticalScrollBar().setValue(10)
    w.editor.name.setText("ungespeichert")
    assert w.editor.geaendert
    for i in range(50):
        s.setze(waechter_s=None if i % 2 else 1.0)
        w.aktualisiere()
    assert w.tabelle.gewaehlte_id() == ziel.id
    assert w.tabelle.verticalScrollBar().value() == 10
    assert w.editor.name.text() == "ungespeichert"
    neu = list(s.bild.eintraege)
    neu[25] = eintrag(id=ziel.id, name=ziel.name, zustand="laeuft")
    s.setze(eintraege=neu)
    w.aktualisiere()
    assert w.editor.modus == "anzeigen"
    assert not w.editor.konflikt.isHidden()
    assert w.editor.konflikt_text.text() == (
        "✖ Der Eintrag wurde inzwischen gestartet. Deine Änderungen wurden nicht übernommen."
    )
    QTest.mouseClick(w.editor.btn_eingaben_verwerfen, Qt.MouseButton.LeftButton)
    assert w.editor.konflikt.isHidden() and w.editor.name.text() == ziel.name


# --- UI-24 ----------------------------------------------------------------------------------


def test_ui_24_groessen_und_sichtbare_zeilen(baue: Any, qtbot: QtBot) -> None:
    s = AttrappenSitzung(bild(eintraege=[eintrag() for _ in range(20)]))
    w, _ = baue(s)
    assert w.minimumWidth() == 1100 and w.minimumHeight() == 680
    for breite, hoehe, zeilen_min in ((1366, 768, 10), (1100, 680, 1)):
        w.resize(breite, hoehe)
        qtbot.wait(20)
        QApplication.processEvents()
        sichtbar = w.tabelle.viewport().height() // w.tabelle.rowHeight(0)
        assert sichtbar >= zeilen_min, (breite, hoehe, sichtbar)
        fenster = w.rect()
        for b in w.findChildren(QAbstractButton):
            if not b.isVisible() or b.parent() is w.tabelle:
                continue
            ecke = b.mapTo(w, b.rect().bottomRight())
            assert fenster.contains(ecke), (b.objectName(), breite)
            assert b.width() >= b.minimumSizeHint().width(), (b.objectName(), breite)


# --- UI-25 ----------------------------------------------------------------------------------


def test_ui_25_geraet_und_einstellungen(baue: Any, qtbot: QtBot, tmp_path: Path) -> None:
    s = AttrappenSitzung(bild(betriebsart=Betriebsart.NUR_LESEN))
    w, dialoge = baue(s)
    QTest.mouseClick(w.btn_geraet, Qt.MouseButton.LeftButton)
    d = dialoge.gesehen[-1]
    assert isinstance(d, GeraetDialog)
    werte = {x.objectName(): x.text() for x in d.findChildren(QLabel) if x.objectName()}
    assert werte["geraet_version"] == INFO.psv_version
    assert werte["geraet_state"] == "gestoppt"
    assert werte["geraet_suppress"] == "ja"
    assert "frontend: SIM-FE" in werte["geraet_hardware"]
    assert "geraet_messpunkte" in werte and werte["geraet_modus"].startswith("Erfassung")
    assert werte["geraet_messpunkte"] == "unbekannt"
    assert werte["geraet_aufrufe"] == "nicht verfügbar (Simulator)"
    s.setze(verbindung=None)
    w.aktualisiere()
    QTest.mouseClick(w.btn_geraet, Qt.MouseButton.LeftButton)
    nicht = dialoge.gesehen[-1].findChild(QLabel, "geraet_nicht_verbunden")
    assert nicht is not None and nicht.text() == "Nicht verbunden."

    def einstellen(d: QDialog) -> None:
        assert isinstance(d, EinstellungenDialog)
        assert d.limit.isEnabled() and d.limit.value() == 600
        d.limit.setValue(900)
        d.ordner_waehlen = lambda _s: str(tmp_path)
        d.findChild(QPushButton, "btn_ordner_waehlen").click()  # type: ignore[union-attr]
        d.btn_uebernehmen.click()

    dialoge.aktionen.append(einstellen)
    QTest.mouseClick(w.btn_einstellungen, Qt.MouseButton.LeftButton)
    assert letzter(s) == ("einstellungen", tmp_path, 900.0)
    assert w.bild.standard_zeitlimit_s == 900.0
    s.fehler["einstellungen"] = ValueError(
        "Einstellungen übernehmen ist im Zustand laeuft nicht möglich"
    )
    gesehen: dict[str, str] = {}

    def fehlschlag(d: QDialog) -> None:
        assert isinstance(d, EinstellungenDialog)
        d.btn_uebernehmen.click()
        gesehen["fehler"] = d.fehler.text()
        gesehen["sichtbar"] = str(not d.fehler.isHidden())
        d.ordner.setText("")
        d.btn_uebernehmen.click()
        gesehen["leer"] = d.fehler.text()
        d.reject()

    dialoge.aktionen.append(fehlschlag)
    QTest.mouseClick(w.btn_einstellungen, Qt.MouseButton.LeftButton)
    assert gesehen["fehler"].startswith("✖ Einstellungen übernehmen ist im Zustand")
    assert gesehen["sichtbar"] == "True"
    assert "Ordner angeben" in gesehen["leer"]


# --- UI-26 ----------------------------------------------------------------------------------


@pytest.mark.parametrize("zustand", [Z.LAEUFT, Z.PAUSE_ANGEFORDERT, Z.ABBRUCH_LAEUFT])
def test_ui_26_schliessen_im_lauf_gesperrt(baue: Any, zustand: Z) -> None:
    s = AttrappenSitzung(bild(durchgang=zustand))
    w, dialoge = baue(s)
    assert not w.close()
    assert w.isVisible()
    assert (
        dialoge.gesehen[-1].text() == "Es läuft ein Durchgang. Bitte zuerst abbrechen oder warten."
    )


def test_ui_26_ungespeichert_fragt(baue: Any, monkeypatch: pytest.MonkeyPatch) -> None:
    s = AttrappenSitzung(bild(eintraege=[eintrag()]))
    w, dialoge = baue(s)
    dialoge.aktionen.append(klicke("Abbrechen"))
    assert not w.close()
    box = dialoge.gesehen[-1]
    assert isinstance(box, QMessageBox)
    assert sorted(b.text() for b in box.buttons()) == ["Abbrechen", "Speichern", "Verwerfen"]
    assert box.defaultButton().text() == "Abbrechen"
    monkeypatch.setattr(w, "_pfad_speichern", lambda: None)
    dialoge.aktionen.append(klicke("Speichern"))
    assert not w.close()  # Speichern abgebrochen
    dialoge.aktionen.append(klicke("Verwerfen"))
    assert w.close()


def test_ui_26_geraet_unklar_warnt(baue: Any) -> None:
    s = AttrappenSitzung(bild(durchgang=Z.GERAET_UNKLAR))
    w, dialoge = baue(s)
    dialoge.aktionen.append(klicke("Abbrechen"))
    assert not w.close()
    assert dialoge.gesehen[-1].text() == "PSV vorher prüfen."
    dialoge.aktionen.append(klicke("Trotzdem schließen"))
    assert w.close()


# --- UI-28 und Stabilität -------------------------------------------------------------------


def test_ui_28_nur_qtimer_im_gui_thread(baue: Any) -> None:
    w, _ = baue(AttrappenSitzung(bild()), takt_ms=100)
    assert w._timer.isActive() and w._timer.interval() == 100


def test_simulator_verbindet_sich_selbst_und_protokolliert_ereignisse(
    baue: Any, tmp_path: Path
) -> None:
    s = AttrappenSitzung(bild(verbindung=None))
    s.ereignisse.append(SitzungsEreignis(revision=2, art="fehler", text="kaputt"))
    w, _ = baue(s)
    assert s.namen() == ["verbinde"]
    assert "Fehler: kaputt" in w.protokoll.toPlainText()
    w.aktualisiere()
    assert s.namen() == ["verbinde"]  # nur ein Versuch


@pytest.mark.skipif(sys.version_info >= (3, 12), reason="None ist ab Python 3.12 unsterblich")
def test_pyside_verliert_keine_referenzen_auf_none(baue: Any) -> None:
    # Regression zu PySide6 6.12.0 (Absturz „none_dealloc“ unter Python 3.11): 1000
    # Aktualisierungen mit je Dutzenden Qt-Aufrufen ohne Rückgabewert dürfen den Zähler von
    # None nicht spürbar senken. Toleranz 50: zufällige Referenzen aus Python selbst.
    w, _ = baue(AttrappenSitzung(bild(eintraege=[eintrag()])))
    vorher = sys.getrefcount(None)
    for _ in range(1000):
        w.aktualisiere()
    assert sys.getrefcount(None) - vorher > -50


def test_protokoll_folgt_dem_ende_und_ist_begrenzt(baue: Any) -> None:
    w, _ = baue(AttrappenSitzung(bild()))
    for i in range(1100):
        w.protokolliere(f"Zeile {i}")
    assert w.protokoll.blockCount() == 1000
    leiste = w.protokoll.verticalScrollBar()
    assert leiste.value() == leiste.maximum()
    leiste.setValue(5)
    w.protokolliere("Fehler: neu")
    assert leiste.value() == 5
    assert w.protokoll.toPlainText().splitlines()[-1].endswith("  Fehler: neu")


# --- UI-29/UI-30: Zurücksetzen (Nachtrag 2026-10-27) ----------------------------------------


def test_ui_29_zuruecksetzen_ohne_rueckfrage_nach_trockenlauf(baue: Any, qtbot: QtBot) -> None:
    eintraege = [eintrag(zustand="fertig", trockenlauf=True, name=f"M{i}") for i in range(30)]
    eintraege.append(eintrag(zustand="fehler"))
    s = AttrappenSitzung(bild(betriebsart=Betriebsart.TROCKENLAUF, eintraege=eintraege))
    w, dialoge = baue(s)
    assert w.hinweisband.knopf("zuruecksetzen") is None  # Feld falsch: kein Knopf
    assert w.hinweisband.property("fall") == "8"
    s.setze(zuruecksetzen_moeglich=True)
    w.aktualisiere()
    assert w.hinweisband.property("fall") == "7b"
    knopf = w.hinweisband.knopf("zuruecksetzen")
    assert knopf is not None and knopf.isEnabled()
    assert knopf.toolTip().startswith("Alle Einträge wieder auf wartend setzen.")
    assert not w.btn_start.isEnabled()
    w.tabelle.waehle(eintraege[20].id)
    w.tabelle.verticalScrollBar().setValue(7)
    QTest.mouseClick(knopf, Qt.MouseButton.LeftButton)
    assert dialoge.gesehen == []
    assert s.namen() == ["zuruecksetzen"]
    assert all(zelle(w, r, 1) == "○ wartend" for r in range(w.tabelle.rowCount()))
    assert w.tabelle.gewaehlte_id() == eintraege[20].id
    assert w.tabelle.verticalScrollBar().value() == 7
    assert w.btn_start.isEnabled()
    assert w.hinweisband.property("fall") == "8"
    assert w.hinweisband.knopf("zuruecksetzen") is None
    assert "Warteschlange zurückgesetzt: 31 Einträge wartend." in w.protokoll.toPlainText()


def test_ui_29_knopf_im_fall_7_und_fehler_der_sitzung(baue: Any, qtbot: QtBot) -> None:
    s = AttrappenSitzung(
        bild(
            durchgang=Z.BEENDET,
            ergebnis=DurchgangErgebnis.VOLLSTAENDIG,
            zusammenfassung=zusammenfassung(fehler=1),
            durchgangsordner="/d",
            zuruecksetzen_moeglich=True,
            eintraege=[eintrag(zustand="fehler")],
        )
    )
    s.fehler["zuruecksetzen"] = ValueError("Zurücksetzen ist im Zustand laeuft nicht möglich")
    w, dialoge = baue(s)
    assert w.hinweisband.property("fall") == "7"
    QTest.mouseClick(w.hinweisband.knopf("zuruecksetzen"), Qt.MouseButton.LeftButton)
    assert s.namen() == ["zuruecksetzen"]
    meldung = dialoge.gesehen[-1]
    assert isinstance(meldung, QMessageBox) and "Zurücksetzen ist im Zustand" in meldung.text()
    assert "Warteschlange zurückgesetzt" not in w.protokoll.toPlainText()


@pytest.mark.parametrize("zustand", ["fertig", "abgebrochen"])
def test_ui_30_rueckfrage_bei_echt_gemessenen(baue: Any, qtbot: QtBot, zustand: str) -> None:
    s = AttrappenSitzung(
        bild(zuruecksetzen_moeglich=True, eintraege=[eintrag(zustand=zustand), eintrag()])
    )
    w, dialoge = baue(s)
    knopf = w.hinweisband.knopf("zuruecksetzen")
    assert knopf is not None
    dialoge.aktionen.append(lambda d: d.escapeButton().click())
    QTest.mouseClick(knopf, Qt.MouseButton.LeftButton)
    box = dialoge.gesehen[-1]
    assert isinstance(box, QMessageBox)
    assert box.windowTitle() == "Warteschlange zurücksetzen?"
    assert box.text().startswith("1 Einträge wurden bereits gemessen.")
    assert box.defaultButton().text() == "Abbrechen"
    assert box.escapeButton().text() == "Abbrechen"
    dialoge.aktionen.append(klicke("Abbrechen"))
    QTest.mouseClick(knopf, Qt.MouseButton.LeftButton)
    assert s.befehle == []
    dialoge.aktionen.append(klicke("Zurücksetzen"))
    QTest.mouseClick(knopf, Qt.MouseButton.LeftButton)
    assert s.namen() == ["zuruecksetzen"]


def test_ui_29_zuruecksetzen_mit_echter_sitzung(baue: Any, qtbot: QtBot, tmp_path: Path) -> None:
    s, _f, _u = echte_sitzung(tmp_path)
    s.einfuegen(0, Messung(name="M1", einstellungsdatei=set_datei(tmp_path)))
    w, dialoge = baue(s)
    QTest.mouseClick(w.btn_start, Qt.MouseButton.LeftButton)
    s.verarbeite()
    w.aktualisiere()
    assert w.bild.zuruecksetzen_moeglich and w.hinweisband.property("fall") == "7"
    dialoge.aktionen.append(klicke("Zurücksetzen"))  # echt fertig: Rückfrage
    QTest.mouseClick(w.hinweisband.knopf("zuruecksetzen"), Qt.MouseButton.LeftButton)
    assert zelle(w, 0, 1) == "○ wartend"
    assert w.btn_start.isEnabled()


# --- K-U4: Korrekturen nach Review und Design-Abnahme -----------------------------------------


def test_k_u4_1_nr_ist_dateinummer_nach_abbruch_und_neuem_durchgang(
    baue: Any, qtbot: QtBot, tmp_path: Path
) -> None:
    s, _f, _u = echte_sitzung(tmp_path)
    datei = set_datei(tmp_path)
    s.einfuegen(0, Messung(name="A", einstellungsdatei=datei))
    s.einfuegen(1, Pausenpunkt(text="Umbau"))
    s.einfuegen(2, Messung(name="B", einstellungsdatei=datei))
    w, dialoge = baue(s)
    assert [zelle(w, r, 0) for r in range(3)] == ["(01)", "–", "(02)"]
    taste(qtbot, w, Qt.Key.Key_F5)
    s.verarbeite()
    w.aktualisiere()
    assert w.hinweisband.property("fall") == "5"
    assert zelle(w, 0, 0) == "01"
    dialoge.aktionen.append(klicke("Durchgang abbrechen"))
    taste(qtbot, w, Qt.Key.Key_F8)
    s.verarbeite()
    w.aktualisiere()
    assert w.bild.durchgang is Z.BEENDET
    # B wartet; ein neuer Durchgang zählt ab 01 (vorläufig gekennzeichnet)
    assert [zelle(w, r, 0) for r in range(3)] == ["01", "–", "(01)"]
    taste(qtbot, w, Qt.Key.Key_F5)  # quittiert
    s.verarbeite()
    w.aktualisiere()  # startet
    s.verarbeite()
    w.aktualisiere()
    assert w.hinweisband.property("fall") == "5"
    taste(qtbot, w, Qt.Key.Key_F7)
    s.verarbeite()
    w.aktualisiere()
    b = w.bild.eintraege[2]
    assert b.messdatei is not None and Path(b.messdatei).name.startswith("01_B")
    assert zelle(w, 2, 0) == "01"
    nr = w.tabelle.item(2, 0)
    assert nr is not None and not nr.font().italic()


def test_k_u4_1_startdialog_nummern_und_spalten(baue: Any, qtbot: QtBot) -> None:
    lang = "Platte_mit_einem_sehr_langen_Namen_fuer_die_Zieldatei_im_Startdialog"
    eintraege = [eintrag(zustand="fertig", nummer=1), eintrag(name=lang), eintrag()]
    s = AttrappenSitzung(
        bild(
            betriebsart=Betriebsart.MESSEN,
            eintraege=eintraege,
            start_vorschau=vorschau_zu(eintraege),
        )
    )
    w, dialoge = baue(s)
    gesehen: dict[str, Any] = {}

    def pruefen(d: QDialog) -> None:
        assert isinstance(d, DurchgangStartenDialog)
        d.resize(760, 480)
        d.show()
        QApplication.processEvents()
        tab = d.tabelle
        gesehen["nr"] = [tab.item(r, 0).text() for r in range(tab.rowCount())]  # type: ignore[union-attr]
        gesehen["breiten"] = (tab.columnWidth(0), tab.columnWidth(2))
        ziel = tab.item(0, 2)
        assert ziel is not None
        gesehen["tip"] = ziel.toolTip()
        gesehen["zelle"] = ziel.text()
        d.reject()

    dialoge.aktionen.append(pruefen)
    QTest.mouseClick(w.btn_start, Qt.MouseButton.LeftButton)
    assert gesehen["nr"] == ["01", "02"]
    assert gesehen["breiten"][0] < 60 < gesehen["breiten"][1]
    # K-U5b: nur der Dateiname in der Zelle, voller Pfad (mit Platzhalter) im Tooltip
    assert gesehen["zelle"] == f"01_{lang}.svd"
    assert "<JJJJ-MM-TT_HHMMSS>" in gesehen["tip"] and lang in gesehen["tip"]


def test_k_u4_2_befehlssperre_mit_revision_aus_der_sitzung(baue: Any, qtbot: QtBot) -> None:
    s = AttrappenSitzung(bild(durchgang=Z.LAEUFT, eintraege=[eintrag(zustand="laeuft")]))
    w, _ = baue(s)
    s.setze()  # Sitzung ist schon eine Revision weiter als das angezeigte Bild
    s.setze()
    QTest.mouseClick(w.btn_pause, Qt.MouseButton.LeftButton)
    QTest.mouseClick(w.btn_pause, Qt.MouseButton.LeftButton)
    taste(qtbot, w, Qt.Key.Key_F6)
    assert s.namen() == ["pausiere"]
    s.setze()  # erst ein neues Bild nach dem Senden hebt die Sperre auf
    w.aktualisiere()
    assert w.btn_pause.isEnabled()


def _beendet(**felder: Any) -> AttrappenSitzung:
    return AttrappenSitzung(
        bild(
            durchgang=Z.BEENDET,
            ergebnis=DurchgangErgebnis.VOLLSTAENDIG,
            durchgangsordner="/d",
            eintraege=[eintrag(zustand="fertig", nummer=1), eintrag(name="W")],
            **felder,
        )
    )


def test_u5_b7_start_aus_beendet_ein_befehl_mit_schnappschuss(baue: Any, qtbot: QtBot) -> None:
    s = _beendet()
    w, _ = baue(s)
    QTest.mouseClick(w.btn_start, Qt.MouseButton.LeftButton)
    assert s.namen() == ["starte"]
    assert s.letzter_start == (Betriebsart.SIMULATOR, s.bild.warteschlangen_kennung)


def test_u5_b7_start_verworfen_meldung_der_sitzung(baue: Any, qtbot: QtBot) -> None:
    s = _beendet()
    s.fehler["starte"] = ValueError(
        "Start verworfen: Warteschlange oder Messdaten-Ordner hat sich seit der Bestätigung "
        "geändert"
    )
    w, dialoge = baue(s)
    QTest.mouseClick(w.btn_start, Qt.MouseButton.LeftButton)
    assert s.namen() == ["starte"]
    meldung = dialoge.gesehen[-1]
    assert isinstance(meldung, QMessageBox) and "Start verworfen" in meldung.text()
    assert w.btn_messung_neu.isEnabled()  # keine Sperre bleibt zurück


def test_k_u4_4_auswahlwechsel_fragt_bei_ungespeicherten_eingaben(baue: Any, qtbot: QtBot) -> None:
    a1, a2 = eintrag(name="A"), eintrag(name="B")
    s = AttrappenSitzung(bild(eintraege=[a1, a2]))
    w, dialoge = baue(s)
    w.tabelle.waehle(a1.id)
    w.editor.name.setText("A_geaendert")
    dialoge.aktionen.append(lambda d: d.escapeButton().click())
    w.tabelle.waehle(a2.id)
    box = dialoge.gesehen[-1]
    assert isinstance(box, QMessageBox) and box.windowTitle() == "Änderungen verwerfen?"
    assert box.defaultButton().text() == "Zurück zum Editor"
    assert box.escapeButton().text() == "Zurück zum Editor"
    assert w.tabelle.gewaehlte_id() == a1.id
    assert w.editor.name.text() == "A_geaendert"
    dialoge.aktionen.append(klicke("Verwerfen"))
    w.tabelle.waehle(a2.id)
    assert w.tabelle.gewaehlte_id() == a2.id and w.editor.name.text() == "B"
    # Modus Neu
    taste(qtbot, w, Qt.Key.Key_N, Qt.KeyboardModifier.ControlModifier)
    QTest.keyClicks(w.editor.name, "Neu")
    dialoge.aktionen.append(klicke("Zurück zum Editor"))
    w.tabelle.waehle(a1.id)
    assert w.editor.modus == "neu_messung" and w.editor.name.text() == "Neu"
    assert w.tabelle.gewaehlte_id() == a2.id
    # ohne Änderungen keine Rückfrage
    anzahl = len(dialoge.gesehen)
    QTest.mouseClick(w.editor.btn_verwerfen, Qt.MouseButton.LeftButton)
    w.tabelle.waehle(a1.id)
    assert len(dialoge.gesehen) == anzahl


def test_k_u4_5_statuszeile_durchgangstext_hat_vorrang(baue: Any) -> None:
    s = AttrappenSitzung(
        bild(
            durchgang=Z.PAUSE_ANGEFORDERT,
            betriebsart=Betriebsart.NUR_LESEN,
            eintraege=[eintrag(zustand="laeuft", nummer=12)],
        )
    )
    w, _ = baue(s)
    w.resize(1100, 680)
    QApplication.processEvents()
    lbl = w.lbl_durchgang
    assert lbl.width() >= lbl.fontMetrics().horizontalAdvance(lbl.volltext())
    assert w.lbl_fehlerstrategie.toolTip().startswith("Fehlerstrategie: vorläufig (O1).")
    assert w.lbl_verbindung.toolTip() == w.lbl_verbindung.volltext()


def test_k_u4_5_editor_ohne_scrollen_bis_notiz_bei_1366(baue: Any) -> None:
    from PySide6.QtWidgets import QScrollArea

    m = eintrag(name="M")
    s = AttrappenSitzung(bild(eintraege=[m]))
    w, _ = baue(s)
    w.resize(1366, 768)
    w.tabelle.waehle(m.id)
    QApplication.processEvents()
    rollen = w.editor.findChild(QScrollArea, "editor_rollen")
    assert rollen is not None
    unten = w.editor.notiz.mapTo(rollen.viewport(), w.editor.notiz.rect().bottomLeft()).y()
    assert unten <= rollen.viewport().height()
    assert rollen.verticalScrollBar().value() == 0


def test_k_u4_6_verbinden_knopf_und_geraet_unklar(baue: Any, qtbot: QtBot) -> None:
    s = AttrappenSitzung(bild(betriebsart=Betriebsart.NUR_LESEN, verbindung=None))
    w, _ = baue(s)
    assert w.btn_verbinden.text() == "Verbinden"
    QTest.mouseClick(w.btn_verbinden, Qt.MouseButton.LeftButton)
    assert s.namen() == ["verbinde"]
    s.setze(verbindung=INFO)
    w.aktualisiere()
    QTest.mouseClick(w.btn_verbinden, Qt.MouseButton.LeftButton)
    assert s.namen() == ["verbinde", "trenne"]
    s.setze(durchgang=Z.GERAET_UNKLAR, betriebsart=Betriebsart.SIMULATOR)
    w.aktualisiere()
    assert w.btn_verbinden.isEnabled() and w.btn_verbinden.text() == "Trennen"
    assert not w.btn_geraet.isEnabled()
    QTest.mouseClick(w.btn_verbinden, Qt.MouseButton.LeftButton)
    assert s.namen() == ["verbinde", "trenne", "trenne"]


def test_k_u4_6_automatisches_verbinden_scheitert(baue: Any) -> None:
    s = AttrappenSitzung(bild(verbindung=None))
    s.fehler["verbinde"] = ValueError("Verbinden ist im Zustand x nicht möglich")
    w, _ = baue(s)
    assert s.namen() == ["verbinde"]
    assert (
        "Fehler: Simulator nicht verbunden: Verbinden ist im Zustand" in w.protokoll.toPlainText()
    )
    w.aktualisiere()
    assert s.namen() == ["verbinde"]


def test_k_u4_6_speichern_mit_ergaenzter_endung_und_vorhandener_datei(
    baue: Any, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    s = AttrappenSitzung(bild(eintraege=[eintrag()]))
    w, dialoge = baue(s)
    vorhanden = tmp_path / "serie.warteschlange.json"
    vorhanden.write_text("{}", encoding="utf-8")
    monkeypatch.setattr(w, "_pfad_speichern", lambda: str(tmp_path / "serie.json"))
    dialoge.aktionen.append(klicke("Abbrechen"))
    w.act_speichern.trigger()
    frage = dialoge.gesehen[-1]
    assert isinstance(frage, QMessageBox) and frage.windowTitle() == "Datei ersetzen?"
    assert frage.defaultButton().text() == "Abbrechen"
    assert s.befehle == []
    dialoge.aktionen.append(klicke("Ersetzen"))
    w.act_speichern.trigger()
    assert s.befehle == [("speichern", vorhanden, True)]


def test_k_u4_6_zuruecksetzen_nur_eine_protokollzeile(baue: Any, tmp_path: Path) -> None:
    s, _f, _u = echte_sitzung(tmp_path)
    s.einfuegen(0, Messung(name="M1", einstellungsdatei=set_datei(tmp_path)))
    s.setze_betriebsart(Betriebsart.TROCKENLAUF)
    s.verarbeite()
    s.verbinde()
    s.verarbeite()
    s.starte("t")
    s.verarbeite()
    w, _ = baue(s)
    QTest.mouseClick(w.hinweisband.knopf("zuruecksetzen"), Qt.MouseButton.LeftButton)
    w.aktualisiere()
    zeilen = [z for z in w.protokoll.toPlainText().splitlines() if "zurückgesetzt" in z]
    assert len(zeilen) == 1 and zeilen[0].endswith(
        "Warteschlange zurückgesetzt: 1 Einträge wartend."
    )


# --- K-U4b ------------------------------------------------------------------------------------


def test_k_u4b_n1_vorlaeufige_nummern_im_zweiten_durchgang(
    baue: Any, qtbot: QtBot, tmp_path: Path
) -> None:
    import dataclasses

    from ldv_automation.gui import anzeige

    s, _f, _u = echte_sitzung(tmp_path)
    datei = set_datei(tmp_path)
    folge: tuple[Messung | Pausenpunkt, ...] = (
        Messung(name="A", einstellungsdatei=datei),
        Pausenpunkt(text="Umbau"),
        Messung(name="B", einstellungsdatei=datei),
        Messung(name="C", einstellungsdatei=datei),
    )
    for i, e in enumerate(folge):
        s.einfuegen(i, e)
    w, dialoge = baue(s)
    taste(qtbot, w, Qt.Key.Key_F5)
    s.verarbeite()
    w.aktualisiere()
    dialoge.aktionen.append(klicke("Durchgang abbrechen"))
    taste(qtbot, w, Qt.Key.Key_F8)
    s.verarbeite()
    w.aktualisiere()
    taste(qtbot, w, Qt.Key.Key_F5)  # quittiert
    s.verarbeite()
    w.aktualisiere()  # startet den zweiten Durchgang
    s.verarbeite()
    w.aktualisiere()
    bild_ = w.bild
    assert bild_.durchgang is Z.WARTET_AUF_BESTAETIGUNG
    # Zwischenstand am Pausenpunkt im zweiten Durchgang: A trägt 01 aus Durchgang 1
    assert [zelle(w, r, 0) for r in range(4)] == ["01", "–", "(01)", "(02)"]
    b_id, c_id = bild_.eintraege[2].id, bild_.eintraege[3].id
    pausiert = dataclasses.replace(bild_, durchgang=Z.PAUSIERT)
    h = anzeige.hinweis(pausiert)
    assert h is not None and h.fall == "6b"
    assert h.text == "⏸ Durchgang pausiert. Nächste wartende Messung: Nr 01 (vorl.) „B“."
    # B laufend gedacht: „Messung 01 von 02“, C folgt als 02
    b_laeuft = dataclasses.replace(bild_.eintraege[2], zustand="laeuft", nummer=1)
    laeuft = dataclasses.replace(
        bild_,
        durchgang=Z.LAEUFT,
        eintraege=(*bild_.eintraege[:2], b_laeuft, bild_.eintraege[3]),
    )
    assert anzeige.durchgang_text(laeuft) == "Läuft · Messung 01 von 02"
    assert anzeige.nummern_bild(laeuft)[c_id] == anzeige.Nr(2, False)
    # Nachweis am Ende: tatsächliche Dateinamen 01_B und 02_C
    taste(qtbot, w, Qt.Key.Key_F7)
    s.verarbeite()
    w.aktualisiere()
    namen = {e.id: Path(e.messdatei or "").name for e in w.bild.eintraege}
    assert namen[b_id].startswith("01_B") and namen[c_id].startswith("02_C")
    assert [zelle(w, r, 0) for r in (2, 3)] == ["01", "02"]


# --- U5: B3 Standard-Zeitlimit im Editor, B1 Gerät-Dialog mit gelesenem Stand ---------------


def test_u5_b3_editor_zeigt_standard_zeitlimit_der_sitzung(baue: Any, qtbot: QtBot) -> None:
    s = AttrappenSitzung(bild())
    w, _ = baue(s)
    taste(qtbot, w, Qt.Key.Key_N, Qt.KeyboardModifier.ControlModifier)
    assert w.editor.limit_hinweis.text() == "(Standard: 600 s)"
    s.setze(standard_zeitlimit_s=120.0)
    w.aktualisiere()
    assert w.editor.limit_hinweis.text() == "(Standard: 120 s)"
    assert w.editor.limit.value() == 120
    assert not w.editor.geaendert  # Übernahme des Standards ist keine Eingabe
    w.editor.limit_eigen.setChecked(True)
    assert w.editor.limit_hinweis.text() == "(Standard: 120 s)"
    s.setze(standard_zeitlimit_s=60.0)
    w.aktualisiere()
    assert w.editor.limit.value() == 120  # eigenes Limit bleibt
    assert w.editor.limit_hinweis.text() == "(Standard: 60 s)"


def test_k_u5b_limit_hinweis_bei_1100x680_vollstaendig_sichtbar(baue: Any, qtbot: QtBot) -> None:
    s = AttrappenSitzung(bild())
    w, _ = baue(s)
    w.resize(1100, 680)
    w.show()
    taste(qtbot, w, Qt.Key.Key_N, Qt.KeyboardModifier.ControlModifier)
    QApplication.processEvents()
    hinweis = w.editor.limit_hinweis
    rollen = w.editor.findChild(QWidget, "editor_rollen")
    assert rollen is not None
    flaeche = rollen.viewport()
    links = hinweis.mapTo(flaeche, hinweis.rect().topLeft())
    rechts = hinweis.mapTo(flaeche, hinweis.rect().topRight())
    assert links.x() >= 0 and rechts.x() <= flaeche.width()
    assert hinweis.width() >= hinweis.fontMetrics().horizontalAdvance(hinweis.text())


def test_u5_b1_geraet_dialog_mit_messpunkten_und_aufrufprotokoll(baue: Any, qtbot: QtBot) -> None:
    from datetime import UTC, datetime

    from ldv_automation.sitzung import GeraeteDiagnose, GeraeteStand

    stand = GeraeteStand(
        messpunkte=9, generator=GENERATOR_AUS, quelle="beim Verbinden", zeit=datetime.now(UTC)
    )
    s = AttrappenSitzung(
        bild(
            betriebsart=Betriebsart.NUR_LESEN,
            geraete_stand=stand,
            geraet_diagnose=GeraeteDiagnose(aufrufe_anzahl=40, verweigerungen=()),
            konfiguration={"pfad": "D:/k.json", "sha256": "ab" * 32, "werte": {"x": 1}},
        )
    )
    w, dialoge = baue(s)
    QTest.mouseClick(w.btn_geraet, Qt.MouseButton.LeftButton)
    d = dialoge.gesehen[-1]
    werte = {x.objectName(): x.text() for x in d.findChildren(QLabel) if x.objectName()}
    assert werte["geraet_messpunkte"] == "9 (gelesen beim Verbinden)"
    assert werte["geraet_aufrufe"] == "40 Zugriffe, keine Verweigerung"
    assert "GeneratorsOn: nein, Aktiv: nein" in werte["geraet_generator"]
    assert werte["geraet_konfiguration"] == "Datei: D:/k.json (SHA-256 abababababab…)\nx: 1"


def test_u5_b3_einstellungen_fehler_des_zeitlimits_unter_dem_feld(
    baue: Any, qtbot: QtBot, tmp_path: Path
) -> None:
    s = AttrappenSitzung(bild(messdaten_wurzel_probleme=("Ordner existiert nicht: /x",)))
    s.fehler["einstellungen"] = EinstellungsFehler(
        ordner=None, zeitlimit="Standard-Zeitlimit muss endlich und > 0 s sein"
    )
    w, dialoge = baue(s)
    gesehen: dict[str, str] = {}

    def pruefen(d: QDialog) -> None:
        assert isinstance(d, EinstellungenDialog)
        gesehen["anfang"] = d.fehler.text()
        d.ordner.setText(str(tmp_path))
        d.limit.setValue(30)
        d.btn_uebernehmen.click()
        gesehen["limit"] = d.limit_fehler.text()
        gesehen["ordner_fehler_sichtbar"] = str(not d.fehler.isHidden())
        gesehen["breite"] = str(d.minimumWidth())
        gesehen["offen"] = str(d.result())
        d.reject()

    dialoge.aktionen.append(pruefen)
    QTest.mouseClick(w.btn_einstellungen, Qt.MouseButton.LeftButton)
    assert gesehen["anfang"] == "✖ Ordner existiert nicht: /x"
    assert gesehen["limit"].startswith("✖ Standard-Zeitlimit muss")
    assert gesehen["ordner_fehler_sichtbar"] == "False"
    assert int(gesehen["breite"]) >= 480
    assert s.namen() == ["einstellungen"]
