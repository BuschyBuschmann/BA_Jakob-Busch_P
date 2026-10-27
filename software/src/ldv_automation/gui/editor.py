"""Editor rechts neben der Tabelle (Zone E, Brief P3, Abschnitt 1 „Zone E“ und 4).

Modi: ``leer``, ``neu_messung``, ``neu_pausenpunkt``, ``bearbeiten``, ``anzeigen``. Die
Parameterzeilen entstehen aus dem Parameterkatalog. Die Prüfung der Eingaben steht in
:mod:`.anzeige` (Qt-frei); die Sitzung prüft beim Übernehmen erneut.
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path
from uuid import UUID

from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QKeySequence, QShortcut
from PySide6.QtWidgets import (
    QCheckBox,
    QComboBox,
    QFileDialog,
    QFormLayout,
    QFrame,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPlainTextEdit,
    QPushButton,
    QScrollArea,
    QSpinBox,
    QVBoxLayout,
    QWidget,
)

from ldv_automation.domaene import KATALOG, Parameterkatalog, ParameterSpec, ParameterWert
from ldv_automation.gui import tokens as t
from ldv_automation.gui.anzeige import (
    Knopf,
    lies_parameter,
    parameter_bezeichnung,
    pruefe_name,
    pruefe_pflichttext,
    wert_text,
    zeilenstatus,
    zieldatei_text,
)
from ldv_automation.gui.stil import schrift
from ldv_automation.sitzung import EintragBild

AUS_SET = "(aus .set)"
ZEITLIMIT_MAX_S = 864_000
"""Obergrenze des Zeitlimit-Felds (10 Tage); nur Eingabegrenze des Felds."""


@dataclass(frozen=True)
class MessungEingaben:
    """Eingaben einer Messung für ``Messung(...)`` bzw. ``Sitzung.bearbeiten``."""

    name: str
    einstellungsdatei: str
    parameter: dict[str, ParameterWert]
    zeitlimit_s: float | None
    notiz: str


class _ParameterZeile:
    """Kontrollkästchen „ändern“, Eingabe und Einheit/Bereich eines Katalogparameters."""

    def __init__(self, spec: ParameterSpec, bei_aenderung: Callable[[], None]) -> None:
        self.spec = spec
        self.aendern = QCheckBox("ändern")
        self.aendern.setObjectName(f"param_aendern_{spec.schluessel}")
        self.eingabe: QLineEdit | QComboBox
        if spec.typ == "str" and spec.erlaubt:
            combo = QComboBox()
            combo.addItem(AUS_SET)
            combo.addItems(list(spec.erlaubt))
            combo.currentIndexChanged.connect(lambda _i: bei_aenderung())
            self.eingabe = combo
        else:
            feld = QLineEdit()
            feld.setPlaceholderText(AUS_SET)
            feld.textChanged.connect(lambda _s: bei_aenderung())
            self.eingabe = feld
        self.eingabe.setObjectName(f"param_{spec.schluessel}")
        self.eingabe.setMinimumWidth(60)
        einheit = f"{spec.einheit} · " if spec.einheit else ""
        # Einheit und Bereich stehen verdichtet in der Beschriftung (K-U4, 5); bei Auswahllisten
        # zeigt die Liste selbst die erlaubten Werte.
        self.bereich_text = f"{einheit}{spec.bereich_text()}"
        name = parameter_bezeichnung(spec)
        self.beschriftung = (
            name if spec.typ == "str" and spec.erlaubt else f"{name} ({self.bereich_text})"
        )
        self.eingabe.setToolTip(self.bereich_text)
        self.fehler = QLabel()
        self.fehler.setObjectName(f"param_fehler_{spec.schluessel}")
        self.fehler.setProperty("art", "fehler")
        self.fehler.setWordWrap(True)
        self.fehler.hide()
        self.aendern.toggled.connect(self._umschalten)
        self.aendern.toggled.connect(lambda _b: bei_aenderung())
        self._umschalten(False)

    def _umschalten(self, an: bool) -> None:
        self.eingabe.setEnabled(an)
        if isinstance(self.eingabe, QComboBox):
            if not an:
                self.eingabe.setCurrentIndex(0)
            elif self.eingabe.currentIndex() == 0:
                self.eingabe.setCurrentIndex(1)
        elif not an:
            self.eingabe.clear()

    def setze(self, wert: ParameterWert | None) -> None:
        """Zeigt einen Wert (``None`` = nicht geändert)."""
        self.aendern.setChecked(wert is not None)
        if wert is None:
            return
        if isinstance(self.eingabe, QComboBox):
            i = self.eingabe.findText(str(wert))
            self.eingabe.setCurrentIndex(max(i, 0))
        else:
            self.eingabe.setText(wert_text(wert))

    def lies(self) -> tuple[ParameterWert | None, str | None]:
        """``(wert, fehler)``; ``(None, None)``, wenn der Parameter nicht geändert wird."""
        if not self.aendern.isChecked():
            return None, None
        if isinstance(self.eingabe, QComboBox):
            text = self.eingabe.currentText() if self.eingabe.currentIndex() > 0 else ""
        else:
            text = self.eingabe.text()
        return lies_parameter(self.spec, text)

    def sperren(self, gesperrt: bool) -> None:
        """Alle Felder der Zeile sperren bzw. freigeben."""
        self.aendern.setEnabled(not gesperrt)
        self.eingabe.setEnabled(not gesperrt and self.aendern.isChecked())


class Editor(QFrame):
    """Editor für Messungen und Pausenpunkte.

    Parameters
    ----------
    katalog : Parameterkatalog
        Quelle der Parameterzeilen.
    """

    uebernehmen_angefordert = Signal()
    verwerfen_angefordert = Signal()
    eingaben_verwerfen_angefordert = Signal()

    def __init__(self, katalog: Parameterkatalog = KATALOG, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setObjectName("editor")
        self.setAccessibleName("Editor")
        self.setMinimumWidth(t.EDITOR_MIN_BREITE_PX)
        self.modus = "leer"
        self.eintrag_id: UUID | None = None
        self.geaendert = False
        self._laedt = False
        self._eintrag: EintragBild | None = None
        self._erlaubt = Knopf(True)
        self.letzter_ordner = ""
        self.datei_waehlen: Callable[[str], str | None] = self._datei_dialog

        aussen = QVBoxLayout(self)
        aussen.setContentsMargins(12, 4, 12, 4)
        self.titel = QLabel()
        self.titel.setObjectName("editor_titel")
        self.titel.setFont(schrift(t.SCHRIFT_PT_TITEL, fett=True))
        self.untertitel = QLabel()
        self.untertitel.setObjectName("editor_untertitel")
        self.untertitel.setProperty("art", "gedaempft")
        self.untertitel.setWordWrap(True)
        aussen.addWidget(self.titel)
        aussen.addWidget(self.untertitel)

        self.konflikt = QFrame()
        self.konflikt.setObjectName("editor_konflikt")
        konflikt_layout = QHBoxLayout(self.konflikt)
        konflikt_layout.setContentsMargins(0, 0, 0, 0)
        self.konflikt_text = QLabel()
        self.konflikt_text.setObjectName("editor_konflikt_text")
        self.konflikt_text.setProperty("art", "fehler")
        self.konflikt_text.setWordWrap(True)
        self.btn_eingaben_verwerfen = QPushButton("Eingaben verwerfen")
        self.btn_eingaben_verwerfen.setObjectName("btn_eingaben_verwerfen")
        self.btn_eingaben_verwerfen.clicked.connect(self.eingaben_verwerfen_angefordert.emit)
        konflikt_layout.addWidget(self.konflikt_text, 1)
        konflikt_layout.addWidget(self.btn_eingaben_verwerfen)
        self.konflikt.hide()
        aussen.addWidget(self.konflikt)

        self.leer_text = QLabel("Eintrag in der Liste wählen oder neu anlegen.")
        self.leer_text.setObjectName("editor_leer")
        self.leer_text.setProperty("art", "gedaempft")
        self.leer_text.setWordWrap(True)
        aussen.addWidget(self.leer_text)

        self._flaeche = QWidget()
        form = QFormLayout(self._flaeche)
        form.setRowWrapPolicy(QFormLayout.RowWrapPolicy.WrapAllRows)
        form.setFieldGrowthPolicy(QFormLayout.FieldGrowthPolicy.AllNonFixedFieldsGrow)
        form.setContentsMargins(0, 0, 0, 0)
        form.setVerticalSpacing(1)
        self._form = form

        # Messung
        self.name = QLineEdit()
        self.name.setObjectName("editor_name")
        self.name.textChanged.connect(self._eingabe)
        self.name_fehler = self._fehlerlabel("editor_name_fehler")
        self.zieldatei = QLabel()
        self.zieldatei.setObjectName("editor_zieldatei")
        self.zieldatei.setProperty("art", "gedaempft")
        self.zieldatei.setWordWrap(True)
        self.set_feld = QLineEdit()
        self.set_feld.setObjectName("editor_set")
        self.set_feld.setReadOnly(True)
        self.set_feld.setMinimumWidth(60)
        self.set_feld.setFont(schrift(t.SCHRIFT_PT_MONO, mono=True))
        self.set_feld.textChanged.connect(self._eingabe)
        self.btn_set = QPushButton("Wählen …")
        self.btn_set.setObjectName("btn_set_waehlen")
        self.btn_set.clicked.connect(self._waehle_set)
        self.set_fehler = self._fehlerlabel("editor_set_fehler")
        set_zeile = QWidget()
        set_layout = QHBoxLayout(set_zeile)
        set_layout.setContentsMargins(0, 0, 0, 0)
        set_layout.addWidget(self.set_feld, 1)
        set_layout.addWidget(self.btn_set)

        self.parameter: list[_ParameterZeile] = [
            _ParameterZeile(spec, self._eingabe) for spec in katalog
        ]

        self.limit_eigen = QCheckBox("eigenes Limit")
        self.limit_eigen.setObjectName("editor_limit_eigen")
        self.limit = QSpinBox()
        self.limit.setObjectName("editor_limit")
        self.limit.setRange(1, ZEITLIMIT_MAX_S)
        self.limit.setValue(600)
        self.limit.setEnabled(False)
        self.limit_hinweis = QLabel("s  (Standard-Zeitlimit der Sitzung)")
        self.limit_hinweis.setProperty("art", "gedaempft")
        self.limit_hinweis.setWordWrap(True)
        self.limit_hinweis.setMinimumWidth(40)
        self.limit_eigen.toggled.connect(self._limit_umschalten)
        self.limit.valueChanged.connect(self._eingabe)
        limit_zeile = QWidget()
        limit_layout = QHBoxLayout(limit_zeile)
        limit_layout.setContentsMargins(0, 0, 0, 0)
        limit_layout.addWidget(self.limit_eigen)
        limit_layout.addWidget(self.limit)
        limit_layout.addWidget(self.limit_hinweis, 1)

        self.notiz = QPlainTextEdit()
        self.notiz.setObjectName("editor_notiz")
        self.notiz.setTabChangesFocus(True)
        zeile_h = self.notiz.fontMetrics().lineSpacing()
        self.notiz.setFixedHeight(zeile_h * 3 + 14)
        self.notiz.textChanged.connect(self._eingabe)

        # Pausenpunkt
        self.text = QLineEdit()
        self.text.setObjectName("editor_text")
        self.text.textChanged.connect(self._eingabe)
        self.text_fehler = self._fehlerlabel("editor_text_fehler")

        # Anzeige
        self.details = QLabel()
        self.details.setObjectName("editor_details")
        self.details.setWordWrap(True)
        self.details.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        self.nicht_aenderbar = QLabel("Dieser Eintrag ist nicht mehr änderbar.")
        self.nicht_aenderbar.setObjectName("editor_nicht_aenderbar")
        self.nicht_aenderbar.setProperty("art", "gedaempft")

        self._zeilen_messung: list[QWidget] = []
        self._zeilen_pause: list[QWidget] = []
        self._zeile(self._zeilen_messung, "&Name", self.name, self.name_fehler, self.zieldatei)
        self._zeile(self._zeilen_messung, "&Einstellungsdatei (.set)", set_zeile, self.set_fehler)
        for pz in self.parameter:
            p_zeile = QWidget()
            p_layout = QHBoxLayout(p_zeile)
            p_layout.setContentsMargins(0, 0, 0, 0)
            p_layout.addWidget(pz.aendern)
            p_layout.addWidget(pz.eingabe, 1)
            self._zeile(
                self._zeilen_messung,
                pz.beschriftung,
                p_zeile,
                pz.fehler,
                buddy=pz.aendern,
            )
        self._zeile(self._zeilen_messung, "&Zeitlimit", limit_zeile, buddy=self.limit_eigen)
        self._zeile(self._zeilen_messung, "N&otiz", self.notiz)
        self._zeile(self._zeilen_pause, "&Text", self.text, self.text_fehler)
        details_rahmen = QWidget()
        details_layout = QVBoxLayout(details_rahmen)
        details_layout.setContentsMargins(0, 8, 0, 0)
        details_layout.addWidget(self.nicht_aenderbar)
        details_layout.addWidget(self.details)
        self._details_rahmen = details_rahmen
        form.addRow(details_rahmen)

        rollen = QScrollArea()
        rollen.setObjectName("editor_rollen")
        rollen.setWidgetResizable(True)
        rollen.setFrameShape(QFrame.Shape.NoFrame)
        rollen.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        rollen.setWidget(self._flaeche)
        aussen.addWidget(rollen, 1)

        knoepfe = QHBoxLayout()
        self.btn_uebernehmen = QPushButton("Übernehmen (Strg+Enter)")
        self.btn_uebernehmen.setObjectName("btn_uebernehmen")
        self.btn_uebernehmen.setProperty("art", "primaer")
        self.btn_uebernehmen.clicked.connect(self._uebernehmen)
        self.btn_verwerfen = QPushButton("Verwerfen (Esc)")
        self.btn_verwerfen.setObjectName("btn_verwerfen")
        self.btn_verwerfen.clicked.connect(self.verwerfen_angefordert.emit)
        knoepfe.addStretch(1)
        knoepfe.addWidget(self.btn_verwerfen)
        knoepfe.addWidget(self.btn_uebernehmen)
        aussen.addLayout(knoepfe)

        for folge in ("Ctrl+Return", "Ctrl+Enter"):
            kurz = QShortcut(QKeySequence(folge), self)
            kurz.setContext(Qt.ShortcutContext.WidgetWithChildrenShortcut)
            kurz.activated.connect(self._uebernehmen)
        esc = QShortcut(QKeySequence(Qt.Key.Key_Escape), self)
        esc.setContext(Qt.ShortcutContext.WidgetWithChildrenShortcut)
        esc.activated.connect(self._esc)

        self.zeige_leer()

    # --- Aufbau ----------------------------------------------------------------------------

    @staticmethod
    def _fehlerlabel(name: str) -> QLabel:
        label = QLabel()
        label.setObjectName(name)
        label.setProperty("art", "fehler")
        label.setWordWrap(True)
        label.hide()
        return label

    def _zeile(
        self,
        sammlung: list[QWidget],
        beschriftung: str,
        feld: QWidget,
        *zusatz: QWidget,
        buddy: QWidget | None = None,
    ) -> None:
        label = QLabel(beschriftung)
        label.setBuddy(buddy or feld)
        behaelter = QWidget()
        layout = QVBoxLayout(behaelter)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.addWidget(feld)
        for z in zusatz:
            layout.addWidget(z)
        self._form.addRow(label, behaelter)
        sammlung.extend((label, behaelter))

    # --- Modi ------------------------------------------------------------------------------

    def _zeige_bereiche(self, *, messung: bool, pause: bool, details: bool) -> None:
        for w in self._zeilen_messung:
            w.setVisible(messung)
        for w in self._zeilen_pause:
            w.setVisible(pause)
        self._details_rahmen.setVisible(details)
        self.leer_text.setVisible(not (messung or pause or details))
        editierbar = self.modus in ("neu_messung", "neu_pausenpunkt", "bearbeiten")
        self.btn_uebernehmen.setVisible(editierbar)
        self.btn_verwerfen.setVisible(editierbar)
        self._sperren(not editierbar)

    def _sperren(self, gesperrt: bool) -> None:
        self.name.setReadOnly(gesperrt)
        self.name.setEnabled(not gesperrt)
        self.btn_set.setEnabled(not gesperrt)
        for pz in self.parameter:
            pz.sperren(gesperrt)
        self.limit_eigen.setEnabled(not gesperrt)
        self.limit.setEnabled(not gesperrt and self.limit_eigen.isChecked())
        self.notiz.setEnabled(not gesperrt)
        self.text.setEnabled(not gesperrt)

    def _leere_felder(self) -> None:
        self.name.clear()
        self.set_feld.clear()
        for pz in self.parameter:
            pz.setze(None)
        self.limit_eigen.setChecked(False)
        self.limit.setValue(600)
        self.notiz.clear()
        self.text.clear()

    def _setze_modus(self, modus: str, titel: str, untertitel: str = "") -> None:
        self.modus = modus
        self.titel.setText(titel)
        self.untertitel.setText(untertitel)
        self.untertitel.setVisible(bool(untertitel))
        self.konflikt.hide()

    def zeige_leer(self) -> None:
        """Modus „leer“ (nichts gewählt)."""
        self._laedt = True
        try:
            self._setze_modus("leer", "")
            self.titel.hide()
            self.eintrag_id = None
            self._eintrag = None
            self._leere_felder()
            self._zeige_bereiche(messung=False, pause=False, details=False)
            self.geaendert = False
        finally:
            self._laedt = False
        self._pruefe()

    def neu_messung(self, einfuegeort: str) -> None:
        """Modus „Neu“ für eine Messung; Fokus ins Feld Name."""
        self._neu("neu_messung", "Neue Messung", einfuegeort)
        self.name.setFocus(Qt.FocusReason.ShortcutFocusReason)

    def neu_pausenpunkt(self, einfuegeort: str) -> None:
        """Modus „Neu“ für einen Pausenpunkt; Fokus ins Feld Text."""
        self._neu("neu_pausenpunkt", "Neuer Pausenpunkt", einfuegeort)
        self.text.setFocus(Qt.FocusReason.ShortcutFocusReason)

    def _neu(self, modus: str, titel: str, einfuegeort: str) -> None:
        self._laedt = True
        try:
            self._setze_modus(modus, titel, einfuegeort)
            self.titel.show()
            self.eintrag_id = None
            self._eintrag = None
            self._leere_felder()
            messung = modus == "neu_messung"
            self._zeige_bereiche(messung=messung, pause=not messung, details=False)
            self.geaendert = False
        finally:
            self._laedt = False
        self._pruefe()

    def _titel_fuer(self, e: EintragBild, nr: str | None, zusatz: str) -> str:
        if e.art == "pausenpunkt":
            return f"Pausenpunkt{zusatz}"
        return f"Messung {nr}{zusatz}" if nr is not None else f"Messung{zusatz}"

    def bearbeite(self, e: EintragBild, nr: str | None) -> None:
        """Modus „Bearbeiten“ für einen wartenden Eintrag."""
        self._laedt = True
        try:
            self._setze_modus("bearbeiten", self._titel_fuer(e, nr, " bearbeiten"))
            self.titel.show()
            self._lade(e)
            messung = e.art == "messung"
            self._zeige_bereiche(messung=messung, pause=not messung, details=False)
            self.geaendert = False
        finally:
            self._laedt = False
        self._pruefe()

    def zeige_an(self, e: EintragBild, nr: str | None) -> None:
        """Modus „Anzeigen“ (schreibgeschützt) für einen nicht mehr wartenden Eintrag."""
        status = zeilenstatus(e).text.split(" ", 1)[-1]
        self._laedt = True
        try:
            self._setze_modus("anzeigen", self._titel_fuer(e, nr, f" ({status})"))
            self.titel.show()
            self._lade(e)
            messung = e.art == "messung"
            self._zeige_bereiche(messung=messung, pause=not messung, details=True)
            self.details.setText(self._detailtext(e))
            self.geaendert = False
        finally:
            self._laedt = False
        self._pruefe()

    def aktualisiere_anzeige(self, e: EintragBild, nr: str | None) -> None:
        """Erneuert den Anzeigemodus mit neuen Laufdaten (Status, Zeiten, Datei)."""
        if self.modus == "anzeigen" and self._eintrag != e:
            konflikt = not self.konflikt.isHidden()
            text = self.konflikt_text.text()
            self.zeige_an(e, nr)
            if konflikt:
                self.zeige_konflikt(text)

    def _lade(self, e: EintragBild) -> None:
        self.eintrag_id = e.id
        self._eintrag = e
        self._leere_felder()
        if e.art == "pausenpunkt":
            self.text.setText(e.text)
            return
        self.name.setText(e.name)
        self.set_feld.setText(e.einstellungsdatei or "")
        self.set_feld.setToolTip(e.einstellungsdatei or "")
        for pz in self.parameter:
            pz.setze(e.parameter.get(pz.spec.schluessel))
        if e.zeitlimit_s is not None:
            self.limit_eigen.setChecked(True)
            self.limit.setValue(round(e.zeitlimit_s))
        self.notiz.setPlainText(e.notiz)

    @staticmethod
    def _detailtext(e: EintragBild) -> str:
        zeilen = [f"Status: {zeilenstatus(e).text}"]
        if e.versuch is not None:
            zeilen.append(f"Versuch: {e.versuch}")
        if e.zeit_start is not None:
            zeilen.append(f"Start: {e.zeit_start:%Y-%m-%d %H:%M:%S}")
        if e.zeit_ende is not None:
            zeilen.append(f"Ende: {e.zeit_ende:%Y-%m-%d %H:%M:%S}")
        if e.messdatei:
            zeilen.append(f"Messdatei: {e.messdatei}")
        if e.protokolldatei:
            zeilen.append(f"Protokoll: {e.protokolldatei}")
        if e.fehlerart or e.fehlertext:
            zeilen.append(f"Fehler ({e.fehlerart or 'unbekannt'}): {e.fehlertext or ''}")
        return "\n".join(zeilen)

    def zeige_konflikt(self, text: str) -> None:
        """Roter Hinweis mit „Eingaben verwerfen“ (Brief Abschnitt 4)."""
        self.konflikt_text.setText(text)
        self.konflikt.show()

    # --- Eingaben --------------------------------------------------------------------------

    def _limit_umschalten(self, an: bool) -> None:
        editierbar = self.modus in ("neu_messung", "neu_pausenpunkt", "bearbeiten")
        self.limit.setEnabled(an and editierbar)
        self.limit_hinweis.setText("s" if an else "s  (Standard-Zeitlimit der Sitzung)")
        self._eingabe()

    def _eingabe(self, *_args: object) -> None:
        if self._laedt:
            return
        if self.modus in ("neu_messung", "neu_pausenpunkt", "bearbeiten"):
            self.geaendert = True
        self._pruefe()

    def _waehle_set(self) -> None:
        pfad = self.datei_waehlen(self.letzter_ordner)
        if pfad:
            self.letzter_ordner = str(Path(pfad).parent)
            self.set_feld.setText(pfad)
            self.set_feld.setToolTip(pfad)

    def _datei_dialog(self, ordner: str) -> str | None:  # pragma: no cover - modaler Dialog
        pfad, _filter = QFileDialog.getOpenFileName(
            self, "Einstellungsdatei wählen", ordner, "PSV-Einstellungen (*.set)"
        )
        return pfad or None

    def fehler(self) -> list[str]:
        """Alle aktuellen Eingabefehler (leer, wenn alles gültig ist)."""
        if self.modus in ("neu_pausenpunkt",) or (
            self.modus == "bearbeiten"
            and self._eintrag is not None
            and self._eintrag.art == "pausenpunkt"
        ):
            f = pruefe_pflichttext("Text", self.text.text())
            return [f] if f else []
        if self.modus not in ("neu_messung", "bearbeiten"):
            return []
        liste: list[str] = []
        for f in (
            pruefe_name(self.name.text()),
            pruefe_pflichttext("Einstellungsdatei", self.set_feld.text()),
        ):
            if f:
                liste.append(f)
        for pz in self.parameter:
            _wert, f = pz.lies()
            if f:
                liste.append(f)
        return liste

    def _pruefe(self) -> None:
        pause = self.modus == "neu_pausenpunkt" or (
            self.modus == "bearbeiten"
            and self._eintrag is not None
            and self._eintrag.art == "pausenpunkt"
        )
        messung = self.modus in ("neu_messung", "bearbeiten") and not pause
        name_f = pruefe_name(self.name.text()) if messung else None
        set_f = pruefe_pflichttext("Einstellungsdatei", self.set_feld.text()) if messung else None
        text_f = pruefe_pflichttext("Text", self.text.text()) if pause else None
        # Pflichtfelder erst nach der ersten Eingabe rot zeigen (kein Fehler beim Öffnen).
        zeigen = self.geaendert or self.modus == "bearbeiten"
        for label, f in (
            (self.name_fehler, name_f),
            (self.set_fehler, set_f),
            (self.text_fehler, text_f),
        ):
            label.setText(f or "")
            label.setVisible(bool(f) and zeigen)
        for pz in self.parameter:
            _wert, f = pz.lies() if messung else (None, None)
            pz.fehler.setText(f or "")
            pz.fehler.setVisible(bool(f))
        if messung or self._eintrag is not None:
            anzeige = self.name.text() if messung else ""
            self.zieldatei.setText(zieldatei_text(self._eintrag, anzeige))
        self._knopf_aktualisieren()

    def setze_uebernehmen_erlaubt(self, knopf: Knopf) -> None:
        """Erlaubnis aus der Aktivierungstabelle 3.3 (Zustand und Eintragszustand)."""
        self._erlaubt = knopf
        self._knopf_aktualisieren()

    def _knopf_aktualisieren(self) -> None:
        fehler = self.fehler()
        if not self._erlaubt.aktiv:
            aktiv, grund = False, self._erlaubt.grund
        elif fehler:
            aktiv, grund = False, f"Eingaben prüfen: {fehler[0]}"
        else:
            aktiv, grund = True, "Übernehmen (Strg+Enter)"
        self.btn_uebernehmen.setEnabled(aktiv)
        self.btn_uebernehmen.setToolTip(grund)

    def messung_eingaben(self) -> MessungEingaben:
        """Gelesene Eingaben einer Messung.

        Raises
        ------
        ValueError
            Bei ungültigen Eingaben (erste Meldung).
        """
        fehler = self.fehler()
        if fehler:
            raise ValueError(fehler[0])
        parameter: dict[str, ParameterWert] = {}
        for pz in self.parameter:
            wert, _f = pz.lies()
            if wert is not None:
                parameter[pz.spec.schluessel] = wert
        return MessungEingaben(
            name=self.name.text(),
            einstellungsdatei=self.set_feld.text(),
            parameter=parameter,
            zeitlimit_s=float(self.limit.value()) if self.limit_eigen.isChecked() else None,
            notiz=self.notiz.toPlainText(),
        )

    def pausenpunkt_text(self) -> str:
        """Gelesener Text eines Pausenpunkts.

        Raises
        ------
        ValueError
            Bei leerem Text.
        """
        f = pruefe_pflichttext("Text", self.text.text())
        if f:
            raise ValueError(f)
        return self.text.text()

    def ist_pausenpunkt(self) -> bool:
        """Prüft, ob der Editor einen Pausenpunkt anlegt oder bearbeitet."""
        return self.modus == "neu_pausenpunkt" or (
            self._eintrag is not None and self._eintrag.art == "pausenpunkt"
        )

    def _uebernehmen(self) -> None:
        if self.btn_uebernehmen.isVisible() and self.btn_uebernehmen.isEnabled():
            self.uebernehmen_angefordert.emit()

    def _esc(self) -> None:
        if self.modus in ("neu_messung", "neu_pausenpunkt", "bearbeiten"):
            self.verwerfen_angefordert.emit()

    def erstes_feld(self) -> QWidget:
        """Erstes bedienbares Feld (Ziel für Enter in der Tabelle)."""
        if self.modus == "neu_pausenpunkt" or (
            self._eintrag is not None and self._eintrag.art == "pausenpunkt"
        ):
            return self.text
        if self.modus in ("neu_messung", "bearbeiten"):
            return self.name
        return self.btn_uebernehmen if self.btn_uebernehmen.isVisible() else self

    @property
    def eintrag(self) -> EintragBild | None:
        """Der zuletzt geladene Eintrag (Bearbeiten/Anzeigen)."""
        return self._eintrag
