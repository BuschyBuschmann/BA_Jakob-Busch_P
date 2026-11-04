"""Auswahlseiten (Zone AD) der Ansichten 2 bis 4 (P-AUSW T3b, Brief K-AUSW 3.2 bis 3.4).

Dünnes Widgetmodul (Abdeckung nur mit ``pytest -m gui``). Jede Seite hält nur ihre
Bedienelemente und meldet Änderungen über das Signal ``geaendert``; Daten, Zustände und das
Zeichnen liegen im Reiter (:mod:`.auswerten_reiter`) und in Qt-freien Modulen. Am Ende jeder
Seite steht ein Textfeld ``lbl_hinweise_<n>`` für ``Zeichnung.hinweise``.
"""

from __future__ import annotations

from collections.abc import Sequence

from PySide6.QtCore import QLocale, Qt, Signal
from PySide6.QtWidgets import (
    QButtonGroup,
    QCheckBox,
    QComboBox,
    QDoubleSpinBox,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QRadioButton,
    QVBoxLayout,
    QWidget,
)

from ldv_automation.gui.anzeige_auswerten import (
    TEXT_PHASE_EINZELKOMPONENTE,
    TEXT_PHASE_KEINE_REFERENZ,
    TEXT_SPITZE_WAEHLEN,
)
from ldv_automation.gui.daten_auswerten import FrequenzPruefung
from ldv_automation.gui.stil import schrift

__all__ = ["AuswahlFrf", "AuswahlSchwingform", "AuswahlSpitzen", "tab_halt"]

TEXT_MINDESTENS_H = "Mindestens H1 oder H2 bleibt gewählt."
"""Tooltip der Kontrollkästchen H1 und H2 (UI-5)."""


def tab_halt(gruppe: QButtonGroup) -> None:
    """Tab-Halt einer Radiogruppe auf der **gewählten** Option (Pfeiltasten wechseln).

    Qt hält sonst bei der ersten Option der Gruppe an. Die übrigen Optionen bleiben mit
    ``ClickFocus`` fokussierbar (UI-21), nehmen aber nicht an der Tab-Reihenfolge teil.
    """
    for knopf in gruppe.buttons():
        knopf.setFocusPolicy(
            Qt.FocusPolicy.StrongFocus if knopf.isChecked() else Qt.FocusPolicy.ClickFocus
        )


def _titel(text: str) -> QLabel:
    titel = QLabel(text)
    titel.setFont(schrift(fett=True))
    return titel


def _gedaempft(name: str, text: str = "") -> QLabel:
    label = QLabel(text)
    label.setObjectName(name)
    label.setProperty("art", "gedaempft")
    label.setWordWrap(True)
    return label


def _segmentzeile(
    layout: QVBoxLayout, gruppe: QButtonGroup, knoepfe: Sequence[QPushButton]
) -> None:
    """Horizontale Segmentzeile (umschaltbare Knöpfe einer exklusiven Gruppe), platzsparend."""
    zeile = QHBoxLayout()
    zeile.setSpacing(2)
    for knopf in knoepfe:
        knopf.setCheckable(True)
        knopf.setAutoDefault(False)
        knopf.setProperty("art", "segment")
        knopf.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        gruppe.addButton(knopf)
        zeile.addWidget(knopf)
    layout.addLayout(zeile)
    gruppe.buttonToggled.connect(lambda _k, _an, g=gruppe: tab_halt(g))
    tab_halt(gruppe)


def _radiogruppe(
    layout: QVBoxLayout, gruppe: QButtonGroup, knoepfe: Sequence[QRadioButton]
) -> None:
    for knopf in knoepfe:
        knopf.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        gruppe.addButton(knopf)
        layout.addWidget(knopf)
    gruppe.buttonToggled.connect(lambda _k, _an, g=gruppe: tab_halt(g))
    tab_halt(gruppe)


class AuswahlFrf(QWidget):
    """Ansicht 2: H1, H2 und „Phase anzeigen“ (Punkt und Kanalpaar stehen oberhalb der Seiten)."""

    geaendert = Signal()

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setObjectName("auswahl_frf")
        v = QVBoxLayout(self)
        v.setContentsMargins(0, 0, 8, 0)
        v.setSpacing(6)
        v.addWidget(_titel("Darstellung"))
        self.chk_h1 = QCheckBox("H1")
        self.chk_h1.setObjectName("chk_h1")
        self.chk_h2 = QCheckBox("H2")
        self.chk_h2.setObjectName("chk_h2")
        self.chk_phase = QCheckBox("Phase anzeigen")
        self.chk_phase.setObjectName("chk_phase")
        for kasten in (self.chk_h1, self.chk_h2):
            kasten.setChecked(True)
            kasten.setToolTip(TEXT_MINDESTENS_H)
        for kasten in (self.chk_h1, self.chk_h2, self.chk_phase):
            kasten.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
            kasten.toggled.connect(self._geaendert)
            v.addWidget(kasten)
        self.lbl_hinweise = _gedaempft("lbl_hinweise_2")
        v.addWidget(self.lbl_hinweise)
        v.addStretch(1)

    def _geaendert(self, _an: bool) -> None:
        if not (self.chk_h1.isChecked() or self.chk_h2.isChecked()):
            quelle = self.sender()
            wieder = self.chk_h1 if quelle is not self.chk_h2 else self.chk_h2
            wieder.blockSignals(True)
            wieder.setChecked(True)
            wieder.blockSignals(False)
            return
        self.geaendert.emit()

    def zuruecksetzen(self) -> None:
        """Voreinstellung: H1 und H2, ohne Phase (beim Dateiwechsel)."""
        for kasten, wert in ((self.chk_h1, True), (self.chk_h2, True), (self.chk_phase, False)):
            kasten.blockSignals(True)
            kasten.setChecked(wert)
            kasten.blockSignals(False)

    def setze_phase_erklaerung(self, text: str) -> None:
        """Tooltip von „Phase anzeigen“: Erklärung der offenen Annahme (leer = keine)."""
        self.chk_phase.setToolTip(text)

    def setze_hinweise(self, text: str) -> None:
        """Zeigt die Hinweise der Zeichnung (``Zeichnung.hinweise``)."""
        self.lbl_hinweise.setText(text)
        self.lbl_hinweise.setVisible(bool(text))


class AuswahlSpitzen(QWidget):
    """Ansicht 3: Angaben der gewählten Spitze, Meldungen und Hinweise der Zeichnung.

    Das Kanalpaar steht über dem Seitenstapel und gilt gemeinsam für alle Ansichten (Nutzer
    bestätigt): Ansicht 2, 3 und 4 benutzen dieselbe Wahl.
    """

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setObjectName("auswahl_spitzen")
        v = QVBoxLayout(self)
        v.setContentsMargins(0, 0, 8, 0)
        v.setSpacing(6)
        v.addWidget(_titel("Spitzen und Bänder"))
        self.lbl_kurve = QLabel()
        self.lbl_kurve.setObjectName("lbl_spitzen_kurve")
        self.lbl_kurve.setAccessibleName("Kurvenlegende")
        self.lbl_kurve.setWordWrap(True)
        self.lbl_kurve.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        self.lbl_kurve.setVisible(False)
        v.addWidget(self.lbl_kurve)
        self.lbl_angaben = QLabel(TEXT_SPITZE_WAEHLEN)
        self.lbl_angaben.setObjectName("lbl_spitze_angaben")
        self.lbl_angaben.setAccessibleName("Angaben der gewählten Spitze")
        self.lbl_angaben.setWordWrap(True)
        self.lbl_angaben.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        v.addWidget(self.lbl_angaben)
        self.lbl_fehler = QLabel()
        self.lbl_fehler.setObjectName("lbl_spitzen_fehler")
        self.lbl_fehler.setProperty("art", "fehler")
        self.lbl_fehler.setWordWrap(True)
        self.lbl_fehler.setVisible(False)
        v.addWidget(self.lbl_fehler)
        self.lbl_hinweise = _gedaempft("lbl_hinweise_3")
        v.addWidget(self.lbl_hinweise)
        v.addStretch(1)

    def setze_kurve(self, text: str) -> None:
        """Zeigt die Kurvenlegende (Mittelformel, Punktzahl, Spitzen, Band) statt im Bild."""
        self.lbl_kurve.setText(text)
        self.lbl_kurve.setVisible(bool(text))

    def setze_angaben(self, text: str) -> None:
        """Zeigt die Angaben der gewählten Spitze (f, ζ, Methode, Bandgrenzen, Kennzeichen)."""
        self.lbl_angaben.setText(text)

    def setze_fehler(self, text: str) -> None:
        """Zeigt die ausgelassenen, unvollständigen Spitzen (R-055)."""
        self.lbl_fehler.setText(text)
        self.lbl_fehler.setVisible(bool(text))

    def setze_hinweise(self, text: str) -> None:
        """Zeigt die Hinweise der Zeichnung."""
        self.lbl_hinweise.setText(text)
        self.lbl_hinweise.setVisible(bool(text))


class AuswahlSchwingform(QWidget):
    """Ansicht 4: Frequenz, Spitzenwahl, Ebene, Komponente, Darstellung und Bezugspunkt."""

    geaendert = Signal()
    spitze_gewaehlt = Signal(int)

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setObjectName("auswahl_schwingform")
        self._phase_moeglich = False
        self._referenz_text = "Phase gegen Ref1"
        self._erklaerung = ""
        self._grund_phase = ""
        v = QVBoxLayout(self)
        v.setContentsMargins(0, 0, 8, 0)
        v.setSpacing(6)

        v.addWidget(_titel("Frequenz [Hz]"))
        self.feld_frequenz = QDoubleSpinBox()
        self.feld_frequenz.setObjectName("feld_frequenz")
        self.feld_frequenz.setLocale(QLocale(QLocale.Language.German, QLocale.Country.Germany))
        self.feld_frequenz.setDecimals(3)
        self.feld_frequenz.setRange(0.0, 1.0e9)  # Eingabe außerhalb der Datei wird gemeldet
        self.feld_frequenz.setKeyboardTracking(False)
        self.feld_frequenz.setSuffix(" Hz")
        self.feld_frequenz.setAccessibleName("Frequenz in Hertz")
        self.feld_frequenz.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.lbl_naechste_linie = _gedaempft("lbl_naechste_linie")
        self.lbl_frequenz_fehler = QLabel()
        self.lbl_frequenz_fehler.setObjectName("lbl_frequenz_fehler")
        self.lbl_frequenz_fehler.setProperty("art", "fehler")
        self.lbl_frequenz_fehler.setWordWrap(True)
        self.lbl_frequenz_fehler.setVisible(False)
        v.addWidget(self.feld_frequenz)
        v.addWidget(self.lbl_naechste_linie)
        v.addWidget(self.lbl_frequenz_fehler)

        self.combo_spitze = QComboBox()
        self.combo_spitze.setObjectName("combo_spitze")
        self.combo_spitze.setAccessibleName("Schnellwahl Spitze")
        self.combo_spitze.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        v.addWidget(self.combo_spitze)

        v.addWidget(_titel("Projektionsebene"))
        self._gruppe_ebene = QButtonGroup(self)
        self.rb_ebene = {e: QPushButton(e) for e in ("xy", "xz", "yz")}
        for e, knopf in self.rb_ebene.items():
            knopf.setObjectName(f"rb_ebene_{e}")
            knopf.setAccessibleName(f"Projektionsebene {e}")
        _segmentzeile(v, self._gruppe_ebene, list(self.rb_ebene.values()))
        self.rb_ebene["xy"].setChecked(True)

        v.addWidget(_titel("Komponente"))
        self._gruppe_komp = QButtonGroup(self)
        self.rb_komp = {c: QPushButton(c) for c in ("X", "Y", "Z", "3D")}
        for c, knopf in self.rb_komp.items():
            knopf.setObjectName(f"rb_komp_{c.lower()}")
            knopf.setAccessibleName(f"Komponente {c}")
        _segmentzeile(v, self._gruppe_komp, list(self.rb_komp.values()))
        self.rb_komp["3D"].setChecked(True)

        v.addWidget(_titel("Größe"))
        self._gruppe_groesse = QButtonGroup(self)
        self.rb_groesse_betrag = QRadioButton("Betrag")
        self.rb_groesse_betrag.setObjectName("rb_groesse_betrag")
        self.rb_groesse_phase_ref = QRadioButton(self._referenz_text)
        self.rb_groesse_phase_ref.setObjectName("rb_groesse_phase_ref")
        self.rb_groesse_phase_relativ = QRadioButton("Phase relativ zu Bezugspunkt")
        self.rb_groesse_phase_relativ.setObjectName("rb_groesse_phase_relativ")
        _radiogruppe(
            v,
            self._gruppe_groesse,
            [self.rb_groesse_betrag, self.rb_groesse_phase_ref, self.rb_groesse_phase_relativ],
        )
        self.rb_groesse_betrag.setChecked(True)
        self.lbl_phase_grund = _gedaempft("lbl_phase_grund")
        v.addWidget(self.lbl_phase_grund)

        self.titel_bezug = _titel("Bezugspunkt der Phase")
        v.addWidget(self.titel_bezug)
        self.combo_bezug = QComboBox()
        self.combo_bezug.setObjectName("combo_bezug")
        self.combo_bezug.setAccessibleName("Bezugspunkt der Phase")
        self.combo_bezug.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        v.addWidget(self.combo_bezug)
        self._bezug_sichtbarkeit()

        self.chk_punktlabels = QCheckBox("Punktlabels")
        self.chk_punktlabels.setObjectName("chk_punktlabels")
        self.chk_punktlabels.setChecked(True)
        self.chk_punktlabels.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        v.addWidget(self.chk_punktlabels)

        self.lbl_hinweise = _gedaempft("lbl_hinweise_4")
        v.addWidget(self.lbl_hinweise)
        v.addStretch(1)

        self.feld_frequenz.valueChanged.connect(self._melde)
        self.combo_bezug.currentIndexChanged.connect(self._melde)
        self.chk_punktlabels.toggled.connect(self._melde)
        self.combo_spitze.activated.connect(self._spitze_aktiviert)
        for gruppe in (self._gruppe_ebene, self._gruppe_komp, self._gruppe_groesse):
            gruppe.buttonToggled.connect(self._knopf_umgeschaltet)

    # --- Zugriff -----------------------------------------------------------------------------

    def frequenz_hz(self) -> float:
        """Eingegebene Frequenz in Hz."""
        return float(self.feld_frequenz.value())

    def komponente(self) -> str:
        """``"X"``, ``"Y"``, ``"Z"`` oder ``"3D"``."""
        return next(c for c, k in self.rb_komp.items() if k.isChecked())

    def ebene(self) -> str:
        """``"xy"``, ``"xz"`` oder ``"yz"``."""
        return next(e for e, k in self.rb_ebene.items() if k.isChecked())

    def darstellung(self) -> str:
        """``"betrag"``, ``"phase_ref"`` oder ``"phase_relativ"``."""
        if self.rb_groesse_phase_ref.isChecked():
            return "phase_ref"
        if self.rb_groesse_phase_relativ.isChecked():
            return "phase_relativ"
        return "betrag"

    def bezug(self) -> int | None:
        """0-basierter Bezugspunkt; ``None`` = Voreinstellung (Eintrag „Automatisch“)."""
        daten = self.combo_bezug.currentData()
        return None if daten is None else int(daten)

    def punktlabels(self) -> bool:
        """Punktlabels gewünscht (die Zeichenfunktion blendet sie bei zu dichten Punkten aus)."""
        return self.chk_punktlabels.isChecked()

    # --- Aufbau und Zustand ------------------------------------------------------------------

    def _blockiert(self, widgets: Sequence[QWidget | QButtonGroup]) -> list[bool]:
        return [w.blockSignals(True) for w in widgets]

    def setze_datei(
        self,
        *,
        schritt_hz: float,
        frequenz_hz: float,
        ebene: str,
        spitzen: Sequence[str],
        punkte: Sequence[str],
        phase_referenz: bool,
        referenz_text: str,
        referenz_erklaerung: str = "",
    ) -> None:
        """Setzt die Seite für eine neu geladene Datei zurück (Voreinstellungen).

        Parameters
        ----------
        schritt_hz : float
            Linienabstand Δf (Schrittweite der Pfeiltasten im Frequenzfeld).
        frequenz_hz : float
            Startfrequenz.
        ebene : str
            Voreingestellte Projektionsebene (``waehle_ebene``).
        spitzen : sequence of str
            Einträge der Schnellwahl (leer = nur Platzhalter).
        punkte : sequence of str
            Einträge der Bezugspunktwahl (Punktnamen).
        phase_referenz : bool
            ``True``, wenn die Datei eine Referenz hat (Phase überhaupt möglich).
        referenz_text : str
            Beschriftung der Option „Phase gegen Referenz“ (mit Kennzeichen).
        referenz_erklaerung : str, optional
            Erklärung der offenen Annahme für den Tooltip dieser Option.
        """
        gruppen: list[QWidget | QButtonGroup] = [
            self.feld_frequenz,
            self.combo_bezug,
            self.combo_spitze,
            self._gruppe_ebene,
            self._gruppe_komp,
            self._gruppe_groesse,
            self.chk_punktlabels,
        ]
        alt = self._blockiert(gruppen)
        try:
            self.feld_frequenz.setSingleStep(schritt_hz)
            self.feld_frequenz.setValue(frequenz_hz)
            self.rb_ebene[ebene].setChecked(True)
            self.rb_komp["3D"].setChecked(True)
            self.rb_groesse_betrag.setChecked(True)
            self.chk_punktlabels.setChecked(True)
            self.combo_spitze.clear()
            self.combo_spitze.addItem("Spitze …" if spitzen else "Keine Spitzen")
            self.combo_spitze.addItems(list(spitzen))
            self.combo_spitze.setEnabled(bool(spitzen))
            self.combo_bezug.clear()
            self.combo_bezug.addItem("Automatisch (größtes |v|, γ² ≥ γ²_min)", None)
            for i, name in enumerate(punkte):
                self.combo_bezug.addItem(name, i)
            self._phase_moeglich = phase_referenz
            self.setze_referenz_text(referenz_text, referenz_erklaerung)
        finally:
            for w, a in zip(gruppen, alt, strict=True):
                w.blockSignals(a)
        for gruppe in (self._gruppe_ebene, self._gruppe_komp, self._gruppe_groesse):
            tab_halt(gruppe)
        self._phase_optionen()

    def setze_spitzen(self, spitzen: Sequence[str]) -> None:
        """Ersetzt die Einträge der Schnellwahl „Spitze …“ (Kanalpaar gewechselt)."""
        sperre = self.combo_spitze.blockSignals(True)
        try:
            self.combo_spitze.clear()
            self.combo_spitze.addItem("Spitze …" if spitzen else "Keine Spitzen")
            self.combo_spitze.addItems(list(spitzen))
            self.combo_spitze.setEnabled(bool(spitzen))
        finally:
            self.combo_spitze.blockSignals(sperre)

    def _bezug_sichtbarkeit(self) -> None:
        """Die Bezugspunktwahl gehört nur zur Phase relativ zu einem Bezugspunkt."""
        sichtbar = self.rb_groesse_phase_relativ.isChecked()
        self.titel_bezug.setVisible(sichtbar)
        self.combo_bezug.setVisible(sichtbar)

    def setze_referenz_text(self, text: str, erklaerung: str = "") -> None:
        """Beschriftung der Option „Phase gegen Referenz“ (Kennzeichen folgt ``ABHAENGIG_VON``).

        Parameters
        ----------
        text : str
            Beschriftung, ggf. mit „(⚠ unbestätigt, M8)“.
        erklaerung : str, optional
            Ausführliche Erklärung der offenen Annahme (Tooltip, nicht im Bild).
        """
        self._referenz_text = text
        self._erklaerung = erklaerung
        self._tooltip_phase_ref()
        # QRadioButton bricht nicht um: Zusatz in Klammern kommt in eine zweite Zeile.
        self.rb_groesse_phase_ref.setText(text.replace(" (", "\n(", 1))
        self.rb_groesse_phase_ref.setAccessibleName(text)

    def setze_bezug_automatisch(self, text: str) -> None:
        """Beschriftung des Eintrags „Automatisch“ mit dem gewählten Punkt."""
        self.combo_bezug.setItemText(0, text)

    def setze_frequenz(self, f_hz: float, *, melden: bool = True) -> None:
        """Setzt das Frequenzfeld (z. B. aus der Spitzenwahl)."""
        sperre = self.feld_frequenz.blockSignals(not melden)
        try:
            self.feld_frequenz.setValue(f_hz)
        finally:
            self.feld_frequenz.blockSignals(sperre)

    def setze_pruefung(self, pruefung: FrequenzPruefung) -> None:
        """Zeigt „nächste Linie“ bzw. die Inline-Meldung bei Eingabe außerhalb."""
        self.lbl_naechste_linie.setText(pruefung.naechste_linie)
        self.lbl_frequenz_fehler.setText(pruefung.fehler)
        self.lbl_frequenz_fehler.setVisible(bool(pruefung.fehler))

    def setze_hinweise(self, text: str) -> None:
        """Zeigt die Hinweise der Zeichnung."""
        self.lbl_hinweise.setText(text)
        self.lbl_hinweise.setVisible(bool(text))

    def _phase_optionen(self) -> None:
        """Sperrt „Phase“ ohne Referenz oder bei 3D, mit sichtbarem Grund (UI-10)."""
        if not self._phase_moeglich:
            grund = TEXT_PHASE_KEINE_REFERENZ
        elif self.komponente() == "3D":
            grund = TEXT_PHASE_EINZELKOMPONENTE
        else:
            grund = ""
        for knopf in (self.rb_groesse_phase_ref, self.rb_groesse_phase_relativ):
            knopf.setEnabled(not grund)
        self.rb_groesse_phase_relativ.setToolTip(grund)
        self._grund_phase = grund
        self._tooltip_phase_ref()
        self.combo_bezug.setEnabled(not grund)
        self.lbl_phase_grund.setText(grund)
        self.lbl_phase_grund.setVisible(bool(grund))
        if grund and self.darstellung() != "betrag":
            sperre = self._gruppe_groesse.blockSignals(True)
            self.rb_groesse_betrag.setChecked(True)
            self._gruppe_groesse.blockSignals(sperre)
            tab_halt(self._gruppe_groesse)
        self._bezug_sichtbarkeit()

    # --- Signale -----------------------------------------------------------------------------

    def _tooltip_phase_ref(self) -> None:
        """Tooltip der Option „Phase gegen Referenz“: Sperrgrund, sonst Erklärung der Annahme."""
        self.rb_groesse_phase_ref.setToolTip(self._grund_phase or self._erklaerung)

    def _melde(self, *_args: object) -> None:
        self.geaendert.emit()

    def _knopf_umgeschaltet(self, _knopf: object, an: bool) -> None:
        if not an:
            return
        self._bezug_sichtbarkeit()
        self._phase_optionen()
        self.geaendert.emit()

    def _spitze_aktiviert(self, index: int) -> None:
        if index > 0:
            self.spitze_gewaehlt.emit(index - 1)
            self.combo_spitze.setCurrentIndex(0)

    def tab_kette(self) -> list[QWidget]:
        """Fokussierbare Teile in Tab-Reihenfolge (Radiogruppen: nur der gewählte Halt)."""
        kette: list[QWidget] = [self.feld_frequenz, self.combo_spitze]
        for gruppe in (self._gruppe_ebene, self._gruppe_komp, self._gruppe_groesse):
            kette += list(gruppe.buttons())
        kette += [self.combo_bezug, self.chk_punktlabels]
        return kette
