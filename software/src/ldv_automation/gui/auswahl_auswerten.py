"""Auswahlseiten (Zone AD) der Ansichten 2 bis 4 (P-AUSW T3b, Brief K-AUSW 3.2 bis 3.4).

Dünnes Widgetmodul (Abdeckung nur mit ``pytest -m gui``). Jede Seite hält nur ihre
Bedienelemente und meldet Änderungen über das Signal ``geaendert``; Daten, Zustände und das
Zeichnen liegen im Reiter (:mod:`.auswerten_reiter`) und in Qt-freien Modulen. Am Ende jeder
Seite steht ein Textfeld ``lbl_hinweise_<n>`` für ``Zeichnung.hinweise``.
"""

from __future__ import annotations

from collections.abc import Sequence

from PySide6.QtCore import QEvent, QLocale, QObject, Qt, Signal
from PySide6.QtGui import QKeyEvent
from PySide6.QtWidgets import (
    QButtonGroup,
    QCheckBox,
    QComboBox,
    QDoubleSpinBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QRadioButton,
    QSizePolicy,
    QSlider,
    QVBoxLayout,
    QWidget,
)

from ldv_automation.gui import tokens
from ldv_automation.gui.achsenleiste import FlussLayout
from ldv_automation.gui.animation_anzeige import (
    BILDRATEN,
    FAKTOR_REGLER_MAX,
    FAKTOR_REGLER_MIN,
    PHASE_REGLER_MAX,
    TEMPO_REGLER_MAX,
    TEMPO_REGLER_MIN,
    regler_aus_tempo,
    regler_aus_theta_rad,
    regler_namen,
    tempo_aus_regler,
    tempo_text,
    theta_grad_aus_regler,
)
from ldv_automation.gui.animation_anzeige import (
    TEXT_KEINE_PHASE as TEXT_ANIMATION_KEINE_PHASE,
)
from ldv_automation.gui.animation_steuerung import Aktion, phase_text
from ldv_automation.gui.animation_tasten import aktion_aus_tastenereignis
from ldv_automation.gui.anzeige_aktionen import AKTIONS_TASTEN, tooltip_mit_taste
from ldv_automation.gui.anzeige_auswerten import (
    TEXT_PHASE_EINZELKOMPONENTE,
    TEXT_PHASE_KEINE_REFERENZ,
    TEXT_SPITZE_WAEHLEN,
)
from ldv_automation.gui.daten_auswerten import FrequenzPruefung
from ldv_automation.gui.stil import schrift, setze_eigenschaft

__all__ = ["AnimationsLeiste", "AuswahlFrf", "AuswahlSchwingform", "AuswahlSpitzen", "tab_halt"]

_FOKUS_RAND_PX = 4
"""Zuschlag zur Knopfbreite für den 2-px-Fokusrahmen (je Seite 1 px mehr als der 1-px-Rand)."""
_REGLER_HOEHE_PX = 24
"""Feste Höhe der Regler der Leiste AH."""
_MAL = "\N{MULTIPLICATION SIGN}"
"""Malzeichen der Überhöhungsanzeige."""
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


def _radiozeile(layout: QVBoxLayout, gruppe: QButtonGroup, knoepfe: Sequence[QRadioButton]) -> None:
    """Radiogruppe in einer Zeile (kurze Optionen, spart Höhe in der schmalen Auswahlspalte)."""
    zeile = QHBoxLayout()
    zeile.setSpacing(12)
    for knopf in knoepfe:
        knopf.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        gruppe.addButton(knopf)
        zeile.addWidget(knopf)
    zeile.addStretch(1)
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
    """Ansicht 4: Frequenz, Spitzenwahl, Modus, Ebene, Komponente, Darstellung und Bezugspunkt.

    Der Modus „Standbild | Animation“ (R-071) schaltet zwischen den Gruppen des Standbilds (Größe
    Betrag/Phase) und denen der Animation (Größe, Phasenbezug, Farbe, Farbbereich, Blick,
    Bildrate) um; Frequenz, Spitzenwahl, Ebene, Komponente, Bezugspunkt und Punktlabels gelten
    für beide Modi.

    Signale: ``geaendert`` bei jeder Änderung, die neu zu zeichnen ist; ``frequenz_geaendert``
    **vor** ``geaendert`` bei jeder Änderung der Frequenz (der Reiter springt dann ins Standbild,
    F-A4); ``modus_geaendert`` vor ``geaendert`` beim Wechsel des Modus.
    """

    geaendert = Signal()
    spitze_gewaehlt = Signal(int)
    frequenz_geaendert = Signal()
    modus_geaendert = Signal(bool)
    farbfeld_eingegeben = Signal(str, str)
    bildrate_geaendert = Signal(float)

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setObjectName("auswahl_schwingform")
        self._phase_moeglich = False
        self._referenz_text = "Phase gegen Ref1"
        self._erklaerung = ""
        self._grund_phase = ""
        self._farbtext = {"von": "", "bis": ""}
        self._farbfehler: set[str] = set()
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

        self.titel_modus = _titel("Darstellung")
        v.addWidget(self.titel_modus)
        self._gruppe_modus = QButtonGroup(self)
        self.rb_modus_standbild = QRadioButton("Standbild")
        self.rb_modus_standbild.setObjectName("rb_modus_standbild")
        self.rb_modus_animation = QRadioButton("Animation")
        self.rb_modus_animation.setObjectName("rb_modus_animation")
        _radiozeile(v, self._gruppe_modus, [self.rb_modus_standbild, self.rb_modus_animation])
        self.rb_modus_standbild.setChecked(True)
        self.lbl_modus_grund = _gedaempft("lbl_modus_grund")
        self.lbl_modus_grund.setVisible(False)
        v.addWidget(self.lbl_modus_grund)

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

        self.titel_groesse = _titel("Größe")
        v.addWidget(self.titel_groesse)
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

        self._baue_animation_a(v)

        self.titel_bezug = _titel("Bezugspunkt der Phase")
        v.addWidget(self.titel_bezug)
        self.combo_bezug = QComboBox()
        self.combo_bezug.setObjectName("combo_bezug")
        self.combo_bezug.setAccessibleName("Bezugspunkt der Phase")
        self.combo_bezug.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        # Breite folgt der Spalte, nicht dem längsten Eintrag: sonst wäre der Inhalt der Spalte
        # breiter als ihr Sichtfenster und die Segmentzeilen würden abgeschnitten
        self.combo_bezug.setSizeAdjustPolicy(
            QComboBox.SizeAdjustPolicy.AdjustToMinimumContentsLengthWithIcon
        )
        self.combo_bezug.setMinimumContentsLength(12)
        v.addWidget(self.combo_bezug)
        self._bezug_sichtbarkeit()

        self._baue_animation_b(v)

        self.chk_punktlabels = QCheckBox("Punktlabels")
        self.chk_punktlabels.setObjectName("chk_punktlabels")
        self.chk_punktlabels.setChecked(True)
        self.chk_punktlabels.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        v.addWidget(self.chk_punktlabels)

        self.lbl_hinweise = _gedaempft("lbl_hinweise_4")
        v.addWidget(self.lbl_hinweise)
        v.addStretch(1)

        self.feld_frequenz.valueChanged.connect(self._frequenz_gemeldet)
        self.combo_bezug.currentIndexChanged.connect(self._melde)
        self.chk_punktlabels.toggled.connect(self._melde)
        self.combo_spitze.activated.connect(self._spitze_aktiviert)
        for gruppe in (
            self._gruppe_ebene,
            self._gruppe_komp,
            self._gruppe_groesse,
            self._gruppe_an_groesse,
            self._gruppe_an_bezug,
            self._gruppe_an_farbe,
        ):
            gruppe.buttonToggled.connect(self._knopf_umgeschaltet)
        self._gruppe_modus.buttonToggled.connect(self._modus_umgeschaltet)
        self._modus_sichtbarkeit()

    # --- Aufbau der Animationsgruppen ----------------------------------------------------------

    def _baue_animation_a(self, v: QVBoxLayout) -> None:
        """Gruppe „Größe“ und „Phasenbezug“ der Animation (R-071)."""
        self.gruppe_animation_a = QWidget()
        self.gruppe_animation_a.setObjectName("gruppe_animation_a")
        a = QVBoxLayout(self.gruppe_animation_a)
        a.setContentsMargins(0, 0, 0, 0)
        a.setSpacing(6)
        a.addWidget(_titel("Größe"))
        self._gruppe_an_groesse = QButtonGroup(self)
        self.rb_groesse_auslenkung = QRadioButton("Auslenkung")
        self.rb_groesse_auslenkung.setObjectName("rb_groesse_auslenkung")
        self.rb_groesse_schnelle = QRadioButton("Schnelle")
        self.rb_groesse_schnelle.setObjectName("rb_groesse_schnelle")
        _radiozeile(
            a, self._gruppe_an_groesse, [self.rb_groesse_auslenkung, self.rb_groesse_schnelle]
        )
        self.rb_groesse_auslenkung.setChecked(True)
        a.addWidget(_titel("Phasenbezug"))
        self._gruppe_an_bezug = QButtonGroup(self)
        self.rb_bezug_relativ = QRadioButton("Relativ zu Bezugspunkt")
        self.rb_bezug_relativ.setObjectName("rb_bezug_relativ")
        self.rb_bezug_absolut = QRadioButton("Absolut gegen Ref1")
        self.rb_bezug_absolut.setObjectName("rb_bezug_absolut")
        _radiogruppe(a, self._gruppe_an_bezug, [self.rb_bezug_relativ, self.rb_bezug_absolut])
        self.rb_bezug_relativ.setChecked(True)
        self.gruppe_animation_a.setVisible(False)
        v.addWidget(self.gruppe_animation_a)

    def _baue_animation_b(self, v: QVBoxLayout) -> None:
        """Gruppe Farbe, Farbbereich und Bildrate der Animation (R-071; Blickknöpfe: AH)."""
        self.gruppe_animation_b = QWidget()
        self.gruppe_animation_b.setObjectName("gruppe_animation_b")
        b = QVBoxLayout(self.gruppe_animation_b)
        b.setContentsMargins(0, 0, 0, 0)
        b.setSpacing(6)
        b.addWidget(_titel("Farbe zeigt"))
        self._gruppe_an_farbe = QButtonGroup(self)
        self.rb_farbe_auslenkung = QRadioButton("Auslenkung")
        self.rb_farbe_auslenkung.setObjectName("rb_farbe_auslenkung")
        self.rb_farbe_betrag = QRadioButton("Betrag")
        self.rb_farbe_betrag.setObjectName("rb_farbe_betrag")
        _radiozeile(b, self._gruppe_an_farbe, [self.rb_farbe_auslenkung, self.rb_farbe_betrag])
        self.rb_farbe_auslenkung.setChecked(True)

        b.addWidget(_titel("Farbbereich"))
        self.feld_farbe_von = self._farbfeld("feld_farbe_von", "Farbbereich von")
        self.feld_farbe_bis = self._farbfeld("feld_farbe_bis", "Farbbereich bis")
        self.lbl_farbe_einheit = _gedaempft("lbl_farbe_einheit")
        self.lbl_farbe_einheit.setWordWrap(False)
        zeile = QHBoxLayout()
        zeile.setSpacing(6)
        zeile.addWidget(self.feld_farbe_von)
        zeile.addWidget(QLabel("–"))
        zeile.addWidget(self.feld_farbe_bis)
        zeile.addWidget(self.lbl_farbe_einheit, 1)
        b.addLayout(zeile)
        self.lbl_farbbereich_meldung = QLabel()
        self.lbl_farbbereich_meldung.setObjectName("lbl_farbbereich_meldung")
        self.lbl_farbbereich_meldung.setProperty("art", "fehler")
        self.lbl_farbbereich_meldung.setWordWrap(True)
        self.lbl_farbbereich_meldung.setVisible(False)
        b.addWidget(self.lbl_farbbereich_meldung)

        b.addWidget(_titel("Bildrate"))
        self.combo_bildrate = QComboBox()
        self.combo_bildrate.setObjectName("combo_bildrate")
        self.combo_bildrate.setAccessibleName("Bildrate der Wiedergabe")
        self.combo_bildrate.setToolTip("Soll-Bildrate der Wiedergabe (Bilder je Sekunde)")
        self.combo_bildrate.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        for rate in BILDRATEN:
            self.combo_bildrate.addItem(f"{rate} Bilder/s", rate)
        self.combo_bildrate.currentIndexChanged.connect(self._bildrate_gewaehlt)
        b.addWidget(self.combo_bildrate)
        self.gruppe_animation_b.setVisible(False)
        v.addWidget(self.gruppe_animation_b)

    def _farbfeld(self, name: str, accessible: str) -> QLineEdit:
        """Feld des Farbbereichs: leer = Auto, Eingabe wirkt erst bei Enter oder Fokuswechsel."""
        feld = QLineEdit()
        feld.setObjectName(name)
        feld.setAccessibleName(accessible)
        feld.setPlaceholderText("Auto")
        feld.setFixedWidth(72)
        feld.setAlignment(Qt.AlignmentFlag.AlignRight)
        feld.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        feld.setProperty("achsenfeld", "true")  # gleiche Höhe mit und ohne Rahmen (Regeln in stil)
        seite = "von" if name.endswith("von") else "bis"
        feld.editingFinished.connect(lambda s=seite, f=feld: self._farbfeld_fertig(s, f))
        return feld

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

    def modus_animation(self) -> bool:
        """Gibt ``True`` im Modus „Animation“ und ``False`` im Modus „Standbild“ zurück."""
        return self.rb_modus_animation.isChecked()

    def groesse_animation(self) -> str:
        """Animierte Größe: ``"auslenkung"`` oder ``"schnelle"``."""
        return "schnelle" if self.rb_groesse_schnelle.isChecked() else "auslenkung"

    def bezug_modus(self) -> str:
        """Phasenbezug der Animation: ``"relativ"`` oder ``"absolut"``."""
        return "absolut" if self.rb_bezug_absolut.isChecked() else "relativ"

    def farbe(self) -> str:
        """Die Farbe zeigt ``"auslenkung"`` (vorzeichenbehaftet) oder ``"betrag"``."""
        return "betrag" if self.rb_farbe_betrag.isChecked() else "auslenkung"

    def bildrate(self) -> float:
        """Gewählte Soll-Bildrate in Bildern je Sekunde."""
        return float(self.combo_bildrate.currentData())

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
            self._gruppe_modus,
            self._gruppe_an_groesse,
            self._gruppe_an_bezug,
            self._gruppe_an_farbe,
            self.chk_punktlabels,
        ]
        alt = self._blockiert(gruppen)
        try:
            self.feld_frequenz.setSingleStep(schritt_hz)
            self.feld_frequenz.setValue(frequenz_hz)
            self.rb_ebene[ebene].setChecked(True)
            self.rb_komp["3D"].setChecked(True)
            self.rb_groesse_betrag.setChecked(True)
            self.rb_modus_standbild.setChecked(True)  # nach dem Öffnen steht Standbild (UI-22)
            self.rb_groesse_auslenkung.setChecked(True)
            self.rb_bezug_relativ.setChecked(True)
            self.rb_farbe_auslenkung.setChecked(True)
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
        for gruppe in (
            self._gruppe_ebene,
            self._gruppe_komp,
            self._gruppe_groesse,
            self._gruppe_modus,
            self._gruppe_an_groesse,
            self._gruppe_an_bezug,
            self._gruppe_an_farbe,
        ):
            tab_halt(gruppe)
        self.setze_farbfelder("", "", "")
        self._modus_optionen()
        self._phase_optionen()
        self._modus_sichtbarkeit()

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
        """Die Bezugspunktwahl gehört nur zur Phase relativ zu einem Bezugspunkt.

        Standbild: zur Option „Phase relativ“ (gesperrt bei 3D). Animation: zum relativen
        Phasenbezug; die Animation kennt auch 3D, gesperrt ist die Wahl nur ohne Referenz.
        """
        if self.modus_animation():
            sichtbar = self.rb_bezug_relativ.isChecked()
            aktiv = self._phase_moeglich
        else:
            sichtbar = self.rb_groesse_phase_relativ.isChecked()
            aktiv = not self._grund_phase
        self.titel_bezug.setVisible(sichtbar)
        self.combo_bezug.setVisible(sichtbar)
        self.combo_bezug.setEnabled(aktiv)

    def _modus_sichtbarkeit(self) -> None:
        """Zeigt die Gruppen des gewählten Modus und blendet die des anderen aus.

        Nach dem Umbau folgt ``updateGeometry`` (KONVENTIONEN).
        """
        animation = self.modus_animation()
        for widget in (
            self.titel_groesse,
            self.rb_groesse_betrag,
            self.rb_groesse_phase_ref,
            self.rb_groesse_phase_relativ,
        ):
            widget.setVisible(not animation)
        self.lbl_phase_grund.setVisible(bool(self._grund_phase) and not animation)
        self.gruppe_animation_a.setVisible(animation)
        self.gruppe_animation_b.setVisible(animation)
        self._bezug_sichtbarkeit()
        self.updateGeometry()

    def _modus_optionen(self) -> None:
        """Sperrt „Animation“ ohne Phase (keine Referenz) mit sichtbarem Grund (UI-30)."""
        grund = "" if self._phase_moeglich else TEXT_ANIMATION_KEINE_PHASE
        self.rb_modus_animation.setEnabled(self._phase_moeglich)
        self.rb_modus_animation.setToolTip(grund)
        self.lbl_modus_grund.setText(grund)
        self.lbl_modus_grund.setVisible(bool(grund))

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

    def setze_absolut_text(self, text: str, erklaerung: str = "") -> None:
        """Beschriftung des absoluten Phasenbezugs der Animation (mit ⚠ unbestätigt, M8).

        Parameters
        ----------
        text : str
            Beschriftung, z. B. „Absolut gegen Ref1 (⚠ unbestätigt, M8)“.
        erklaerung : str, optional
            Erklärung der offenen Annahme (Tooltip).
        """
        # QRadioButton bricht nicht um: Zusatz in Klammern kommt in eine zweite Zeile.
        self.rb_bezug_absolut.setText(text.replace(" (", "\n(", 1))
        self.rb_bezug_absolut.setAccessibleName(text)
        self.rb_bezug_absolut.setToolTip(erklaerung)

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
        self.lbl_phase_grund.setText(grund)
        self.lbl_phase_grund.setVisible(bool(grund) and not self.modus_animation())
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

    def _frequenz_gemeldet(self, *_args: object) -> None:
        """Meldet erst ``frequenz_geaendert`` (Sprung ins Standbild), dann das Neuzeichnen."""
        self.frequenz_geaendert.emit()
        self.geaendert.emit()

    def _modus_umgeschaltet(self, _knopf: object, an: bool) -> None:
        if not an:
            return
        self._modus_sichtbarkeit()
        self.modus_geaendert.emit(self.modus_animation())
        self.geaendert.emit()

    def setze_modus_standbild(self) -> None:
        """Stellt den Modus „Standbild“ ein, ohne ``geaendert`` zu melden (Frequenzwechsel)."""
        sperre = self._gruppe_modus.blockSignals(True)
        try:
            self.rb_modus_standbild.setChecked(True)
        finally:
            self._gruppe_modus.blockSignals(sperre)
        tab_halt(self._gruppe_modus)
        self._modus_sichtbarkeit()

    def setze_bildrate(self, bildrate: float) -> None:
        """Wählt die Bildrate in der Liste, die der Soll-Bildrate am nächsten liegt (still)."""
        index = min(range(len(BILDRATEN)), key=lambda i: abs(BILDRATEN[i] - bildrate))
        sperre = self.combo_bildrate.blockSignals(True)
        try:
            self.combo_bildrate.setCurrentIndex(index)
        finally:
            self.combo_bildrate.blockSignals(sperre)

    def _bildrate_gewaehlt(self, _index: int) -> None:
        self.bildrate_geaendert.emit(self.bildrate())

    def setze_farbfelder(self, von: str, bis: str, einheit: str) -> None:
        """Zeigt den wirksamen Farbbereich in den Feldern (leer = Auto) und löscht Meldungen.

        Parameters
        ----------
        von, bis : str
            Feldtexte in der Anzeigeeinheit (leer = Auto).
        einheit : str
            Einheit hinter den Feldern („µm“, „mm/s“ …).
        """
        self._farbtext = {"von": von, "bis": bis}
        for seite, feld, text in (
            ("von", self.feld_farbe_von, von),
            ("bis", self.feld_farbe_bis, bis),
        ):
            sperre = feld.blockSignals(True)
            try:
                feld.setText(text)
            finally:
                feld.blockSignals(sperre)
            setze_eigenschaft(feld, "fest", "true" if text else "false")
            self._setze_farbfehler(seite, None)
        self.lbl_farbe_einheit.setText(einheit)
        self.feld_farbe_von.setToolTip(f"Untere Grenze der Farbskala in {einheit}; leer = Auto")
        self.feld_farbe_bis.setToolTip(f"Obere Grenze der Farbskala in {einheit}; leer = Auto")

    def zeige_farbfehler(self, seite: str, text: str) -> None:
        """Inline-Meldung zum Farbbereich (wie UI-5); das Feld trägt den gestrichelten Rand."""
        self._setze_farbfehler(seite, text)

    def _setze_farbfehler(self, seite: str, text: str | None) -> None:
        feld = self.feld_farbe_von if seite == "von" else self.feld_farbe_bis
        if text:
            self._farbfehler.add(seite)
            setze_eigenschaft(feld, "fehler", "true")
            self.lbl_farbbereich_meldung.setText(f"{tokens.symbol('fehler')} {text}")
        else:
            self._farbfehler.discard(seite)
            setze_eigenschaft(feld, "fehler", "false")
            if not self._farbfehler:
                self.lbl_farbbereich_meldung.setText("")
        self.lbl_farbbereich_meldung.setVisible(bool(self._farbfehler))
        self.updateGeometry()

    def farbfehler_aktiv(self, seite: str) -> bool:
        """Gibt an, ob das Feld ``"von"`` oder ``"bis"`` eine Meldung zeigt (ungültige Eingabe)."""
        return seite in self._farbfehler

    def _farbfeld_fertig(self, seite: str, feld: QLineEdit) -> None:
        """Enter oder Fokuswechsel: nur eine geänderte Eingabe löst das Neuzeichnen aus (UI-37)."""
        text = feld.text()
        if text.strip() == self._farbtext[seite].strip():
            self._setze_farbfehler(seite, None)  # Eingabe wieder wie angewendet: Meldung weg
            return
        self.farbfeld_eingegeben.emit(seite, text)

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
        kette += list(self._gruppe_modus.buttons())
        for gruppe in (self._gruppe_ebene, self._gruppe_komp, self._gruppe_groesse):
            kette += list(gruppe.buttons())
        for gruppe in (self._gruppe_an_groesse, self._gruppe_an_bezug):
            kette += list(gruppe.buttons())
        kette.append(self.combo_bezug)
        kette += list(self._gruppe_an_farbe.buttons())
        kette += [self.feld_farbe_von, self.feld_farbe_bis]
        kette += [self.combo_bildrate, self.chk_punktlabels]
        return kette


_REGLER_KOMPAKT_PHASE_PX = 110
"""Breite des Phasenreglers im kompakten Modus (normal 150 px)."""
_REGLER_KOMPAKT_PX = 56
"""Breite von Tempo- und Überhöhungsregler im kompakten Modus (normal 100 px)."""
_GRUPPENABSTAND_PX = 24
"""Abstand zwischen den Gruppen der Bedienleiste AH (Etikett und Regler bleiben beisammen)."""


class _Gruppe(QWidget):
    """Eine Gruppe der Bedienleiste AH: Elemente nebeneinander, bricht nie in sich um."""

    def __init__(self, name: str, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setObjectName(name)
        self.zeile = QHBoxLayout(self)
        self.zeile.setContentsMargins(0, 0, 0, 0)
        self.zeile.setSpacing(6)
        # feste Höhe: Fokusrahmen und Zustandswechsel der Elemente ändern die Zeilenhöhe der Leiste
        # nicht (sonst änderte sich die Canvasgröße und die Wiedergabe hielte an)
        self.setFixedHeight(tokens.KNOPF_MIN_HOEHE_PX)


class AnimationsLeiste(QWidget):
    """Zone AH: Bedienleiste der Animation (nur Ansicht 4, Modus Animation; R-071, UI-24).

    Gruppen im :class:`~ldv_automation.gui.achsenleiste.FlussLayout` (Umbruch statt
    Abschneiden): Abspielen/Pause und Einzelschritte, Schrittweite, Phasenregler mit Gradanzeige,
    Tempo, Überhöhung (Regler als Faktor der automatischen Skalierung und Eingabefeld) und
    „Ansicht zurücksetzen“. Die Leiste hält nur Bedienelemente und meldet Eingaben über Signale;
    Winkel, Uhr und Zeichnen liegen in der
    :class:`~ldv_automation.gui.animationsflaeche.AnimationsFlaeche` und im Reiter.

    Texte, die sich während der Wiedergabe ändern (Winkelanzeige, Abspielen/Pause), haben eine
    **feste Breite**: Eine Größenänderung der Leiste änderte die Größe des Canvas und hielte die
    Wiedergabe an.
    """

    abspielen_geklickt = Signal()
    schritt_geklickt = Signal(int)
    phase_gewaehlt = Signal(float, bool)
    phase_losgelassen = Signal()
    schrittweite_geaendert = Signal(float)
    tempo_geaendert = Signal(float)
    ueberhoehung_regler = Signal(int)
    ueberhoehung_losgelassen = Signal()
    skalierung_eingegeben = Signal(str)
    ansicht_zurueck = Signal()
    blick_gewaehlt = Signal(str)
    werte_tabelle_geklickt = Signal()
    aktion_gewaehlt = Signal(object)
    """Tastenaktion (:class:`Aktion`) mit Fokus in einem Regler (außer Abspielen/Pause)."""

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setObjectName("animationsleiste")
        self.setAccessibleName("Bedienleiste der Animation")
        self._kompakt = False
        self._skalierungstext = ""
        self._schnelle = False
        fluss = FlussLayout(self, abstand=_GRUPPENABSTAND_PX, zeilenabstand=4)
        fluss.setContentsMargins(0, 2, 0, 2)
        self._fluss = fluss

        wiedergabe = _Gruppe("gruppe_wiedergabe")
        self.btn_schritt_zurueck = self._knopf(
            "btn_schritt_zurueck",
            "Schritt zurück",
            tooltip_mit_taste("Einzelschritt zurück", "animation_phase_zurueck"),
        )
        self.btn_abspielen = self._knopf("btn_abspielen", "Abspielen", "")
        self.btn_schritt_vor = self._knopf(
            "btn_schritt_vor",
            "Schritt vor",
            tooltip_mit_taste("Einzelschritt vor", "animation_phase_vor"),
        )
        for knopf in (self.btn_schritt_zurueck, self.btn_abspielen, self.btn_schritt_vor):
            wiedergabe.zeile.addWidget(knopf)
        fluss.addWidget(wiedergabe)

        schritt = _Gruppe("gruppe_schrittweite")
        lbl = QLabel("Schrittweite")
        self.feld_schrittweite = QDoubleSpinBox()
        self.feld_schrittweite.setObjectName("feld_schrittweite")
        self.feld_schrittweite.setLocale(QLocale(QLocale.Language.German, QLocale.Country.Germany))
        self.feld_schrittweite.setDecimals(1)
        self.feld_schrittweite.setRange(0.1, 360.0)
        self.feld_schrittweite.setSingleStep(1.0)
        self.feld_schrittweite.setSuffix("°")
        self.feld_schrittweite.setKeyboardTracking(False)
        self.feld_schrittweite.setAccessibleName("Schrittweite der Einzelschritte in Grad")
        self.feld_schrittweite.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.feld_schrittweite.setFixedWidth(82)
        lbl.setBuddy(self.feld_schrittweite)
        schritt.zeile.addWidget(lbl)
        schritt.zeile.addWidget(self.feld_schrittweite)
        fluss.addWidget(schritt)

        phase = _Gruppe("gruppe_phase")
        self.lbl_phase_grad = QLabel(phase_text(0.0))
        self.lbl_phase_grad.setObjectName("lbl_phase_grad")
        self.lbl_phase_grad.setAccessibleName("Phasenwinkel")
        self.regler_phase = self._regler(
            "regler_phase", 0, PHASE_REGLER_MAX, "Phasenwinkel in Grad", breite=150
        )
        self.regler_phase.setPageStep(900)
        self.regler_phase.setAccessibleDescription("Wert in Zehntelgrad: 900 entspricht 90,0°")
        self.lbl_phase_grad.setBuddy(self.regler_phase)
        phase.zeile.addWidget(self.lbl_phase_grad)
        phase.zeile.addWidget(self.regler_phase)
        fluss.addWidget(phase)

        self.btn_werte_tabelle = self._knopf(
            "btn_werte_tabelle",
            "Werte als Tabelle",
            "Auslenkung je Messpunkt bei dem aktuellen Winkel als Tabelle (Ersatz für das Bild)",
        )
        fluss.addWidget(self.btn_werte_tabelle)

        tempo = _Gruppe("gruppe_tempo")
        self.lbl_tempo_titel = QLabel("Tempo")
        self.lbl_tempo_titel.setObjectName("lbl_tempo_titel")
        self.lbl_tempo = QLabel(tempo_text(0.25))
        self.lbl_tempo.setObjectName("lbl_tempo")
        self.lbl_tempo.setAccessibleName("Tempo der Wiedergabe")
        self.regler_tempo = self._regler(
            "regler_tempo",
            TEMPO_REGLER_MIN,
            TEMPO_REGLER_MAX,
            "Tempo der Wiedergabe in Perioden je Sekunde",
            breite=100,
        )
        self.regler_tempo.setAccessibleDescription(
            "logarithmische Stellung, 0 entspricht 1 Periode/s"
        )
        self.lbl_tempo_titel.setBuddy(self.regler_tempo)
        tempo.zeile.addWidget(self.lbl_tempo_titel)
        tempo.zeile.addWidget(self.lbl_tempo)
        tempo.zeile.addWidget(self.regler_tempo)
        fluss.addWidget(tempo)

        ueber = _Gruppe("gruppe_ueberhoehung")
        self.lbl_ueberhoehung = QLabel("")
        self.lbl_ueberhoehung.setObjectName("lbl_ueberhoehung")
        self.lbl_ueberhoehung.setAccessibleName("Überhöhung")
        self.regler_ueberhoehung = self._regler(
            "regler_ueberhoehung",
            FAKTOR_REGLER_MIN,
            FAKTOR_REGLER_MAX,
            "Überhöhung als Faktor der automatischen Skalierung",
            breite=100,
        )
        self.regler_ueberhoehung.setToolTip(
            "Überhöhung: Faktor 0,1 bis 20 auf die automatische Skalierung (Mitte = Auto)"
        )
        self.regler_ueberhoehung.setAccessibleDescription(
            "logarithmische Stellung, 0 entspricht der automatischen Skalierung"
        )
        self.feld_skalierung = QLineEdit()
        self.feld_skalierung.setObjectName("feld_skalierung")
        self.feld_skalierung.setAccessibleName("Skalierung der Auslenkung")
        self.feld_skalierung.setPlaceholderText("Auto")
        self.feld_skalierung.setFixedWidth(72)
        self.feld_skalierung.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.feld_skalierung.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.feld_skalierung.setProperty("achsenfeld", "true")
        self.lbl_ueberhoehung.setBuddy(self.feld_skalierung)
        ueber.zeile.addWidget(self.lbl_ueberhoehung)
        ueber.zeile.addWidget(self.regler_ueberhoehung)
        ueber.zeile.addWidget(self.feld_skalierung)
        fluss.addWidget(ueber)

        blick = _Gruppe("gruppe_blick")
        blick.zeile.setSpacing(2)
        self.btn_blick: dict[str, QPushButton] = {}
        for name, text, tip in (
            ("xy", "xy", "Aufsicht xy"),
            ("xz", "xz", "Ansicht xz"),
            ("yz", "yz", "Ansicht yz"),
            ("iso", "Iso", "Isometrisch"),
        ):
            knopf = self._knopf(f"btn_blick_{name}", text, tip)
            knopf.setAccessibleName(f"Blick {tip}")
            knopf.setProperty("art", "segment")
            knopf.clicked.connect(lambda _c=False, n=name: self.blick_gewaehlt.emit(n))
            self.btn_blick[name] = knopf
            blick.zeile.addWidget(knopf)

        self.btn_ansicht_zurueck = self._knopf(
            "btn_ansicht_zurueck",
            "Ansicht zurücksetzen",
            tooltip_mit_taste(
                "Blick und Zoom zurücksetzen; Winkel und Überhöhung bleiben",
                "animation_ansicht_zurueck",
            ),
        )
        blick.zeile.addSpacing(6)
        blick.zeile.addWidget(self.btn_ansicht_zurueck)
        fluss.addWidget(blick)

        self.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Minimum)
        self.setze_wiedergabe(False)
        self._feste_breiten()
        self._texte_knoepfe()
        self._verbinde()

    # --- Aufbau --------------------------------------------------------------------------------

    @staticmethod
    def _knopf(name: str, text: str, tooltip: str) -> QPushButton:
        knopf = QPushButton(text)
        knopf.setObjectName(name)
        knopf.setAccessibleName(text)
        knopf.setToolTip(tooltip)
        knopf.setAutoDefault(False)
        knopf.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        # feste Höhe: der Fokusrahmen (2 px statt 1 px) ändert die Höhe der Leiste nicht, sonst
        # änderte der Klick auf „Abspielen“ die Canvasgröße und hielte die Wiedergabe an
        knopf.setFixedHeight(tokens.KNOPF_MIN_HOEHE_PX)
        return knopf

    @staticmethod
    def _regler(name: str, minimum: int, maximum: int, accessible: str, *, breite: int) -> QSlider:
        regler = QSlider(Qt.Orientation.Horizontal)
        regler.setObjectName(name)
        regler.setRange(minimum, maximum)
        regler.setAccessibleName(accessible)
        regler.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        regler.setFixedWidth(breite)
        regler.setFixedHeight(_REGLER_HOEHE_PX)  # Fokusrahmen ändert die Höhe nicht (siehe Knöpfe)
        return regler

    def _feste_breiten(self) -> None:
        """Feste Breiten für Texte, die sich während der Wiedergabe ändern (kein Umbruch)."""
        for widget in (self.lbl_phase_grad, self.lbl_tempo, self.btn_abspielen):
            widget.ensurePolished()
        metrik = self.lbl_phase_grad.fontMetrics()
        self.lbl_phase_grad.setFixedWidth(metrik.horizontalAdvance("θ = 359,9°") + 6)
        self.lbl_phase_grad.setMinimumHeight(self.lbl_phase_grad.sizeHint().height())
        muster = "0,00/s" if self._kompakt else "0,00 Perioden/s"
        self.lbl_tempo.setFixedWidth(metrik.horizontalAdvance(muster) + 6)
        breite = 0
        for art in ("abspielen", "pause"):
            self.btn_abspielen.setText(regler_namen(art)[0])
            breite = max(breite, self.btn_abspielen.sizeHint().width())
        self.btn_abspielen.setFixedWidth(breite + _FOKUS_RAND_PX)
        self.setze_wiedergabe(False)
        self._breite_ueberhoehung()

    def _breiten_regler(self) -> None:
        """Feste Breiten der Regler (im kompakten Modus schmaler, UI-D3)."""
        for regler, normal, kompakt in (
            (self.regler_phase, 150, _REGLER_KOMPAKT_PHASE_PX),
            (self.regler_tempo, 100, _REGLER_KOMPAKT_PX),
            (self.regler_ueberhoehung, 100, _REGLER_KOMPAKT_PX),
        ):
            regler.setFixedWidth(kompakt if self._kompakt else normal)

    def _texte_knoepfe(self) -> None:
        """Beschriftung der Knöpfe (kurz bei schmalem Fenster) mit fester Breite je Text.

        Der Fokusrahmen (2 px statt 1 px) ändert die Knopfbreite nicht: sonst bräche die Leiste
        beim Klick anders um und die Canvasgröße änderte sich.
        """
        texte = (
            (self.btn_schritt_zurueck, "Zurück", "Schritt zurück"),
            (self.btn_schritt_vor, "Vor", "Schritt vor"),
            (self.btn_ansicht_zurueck, "Zurücksetzen", "Ansicht zurücksetzen"),
            (self.btn_werte_tabelle, "Tabelle", "Werte als Tabelle"),
        )
        for knopf, kurz, lang in texte:
            knopf.setText(kurz if self._kompakt else lang)
            knopf.ensurePolished()
            knopf.setFixedWidth(knopf.sizeHint().width() + _FOKUS_RAND_PX)
        self.updateGeometry()

    def _breite_ueberhoehung(self) -> None:
        """Feste Breite der Überhöhungsanzeige je Größe (die Schnelle trägt den längeren Text)."""
        metrik = self.lbl_ueberhoehung.fontMetrics()
        muster = (
            f"00,000 s (entspricht Überhöhung {_MAL}0000000)"
            if self._schnelle
            else f"Überhöhung {_MAL}0000000"
        )
        self.lbl_ueberhoehung.setFixedWidth(metrik.horizontalAdvance(muster) + 6)
        self.updateGeometry()

    def _verbinde(self) -> None:
        self.btn_abspielen.clicked.connect(lambda _c=False: self.abspielen_geklickt.emit())
        self.btn_schritt_zurueck.clicked.connect(lambda _c=False: self.schritt_geklickt.emit(-1))
        self.btn_schritt_vor.clicked.connect(lambda _c=False: self.schritt_geklickt.emit(1))
        self.btn_ansicht_zurueck.clicked.connect(lambda _c=False: self.ansicht_zurueck.emit())
        self.btn_werte_tabelle.clicked.connect(lambda _c=False: self.werte_tabelle_geklickt.emit())
        self.feld_schrittweite.valueChanged.connect(self._schrittweite_gewaehlt)
        self.regler_phase.valueChanged.connect(self._phase_gewaehlt)
        self.regler_phase.sliderReleased.connect(self.phase_losgelassen.emit)
        self.regler_tempo.valueChanged.connect(self._tempo_gewaehlt)
        self.regler_ueberhoehung.valueChanged.connect(self.ueberhoehung_regler.emit)
        self.regler_ueberhoehung.sliderReleased.connect(self.ueberhoehung_losgelassen.emit)
        self.feld_skalierung.editingFinished.connect(self._skalierung_fertig)
        for regler in (self.regler_phase, self.regler_tempo, self.regler_ueberhoehung):
            regler.installEventFilter(self)  # Tasten im Regler: wie in der Fläche

    # --- Eingaben --------------------------------------------------------------------------------

    def eventFilter(self, watched: QObject, event: QEvent) -> bool:  # noqa: N802  # Qt-Name
        """Mit Fokus in einem Regler gelten die Tasten der Animationsfläche (Plan 5.2, UI-32).

        Im Phasenregler wirken alle belegten Tasten wie in der Fläche (Elevation, Azimut, Blick
        zurück …) statt der Eigenbelegung des Reglers (θ-Wert). Tempo- und Überhöhungsregler
        behalten ihre Pfeiltasten (feine Verstellung); nur Pos1 und Leertaste wirken in allen
        drei Reglern wie in der Fläche. Felder (Schrittweite, Skalierung) behalten ihr Verhalten.
        """
        if (
            isinstance(event, QKeyEvent)
            and event.type() == QEvent.Type.KeyPress
            and watched in (self.regler_phase, self.regler_tempo, self.regler_ueberhoehung)
        ):
            aktion = aktion_aus_tastenereignis(event)
            if watched is not self.regler_phase and aktion not in (
                Aktion.ABSPIELEN,
                Aktion.ANSICHT_ZURUECK,
            ):
                aktion = None
            if aktion is not None:
                if aktion is Aktion.ABSPIELEN:
                    self.abspielen_geklickt.emit()
                else:
                    self.aktion_gewaehlt.emit(aktion)
                return True
        return super().eventFilter(watched, event)

    def _schrittweite_gewaehlt(self, grad: float) -> None:
        self.regler_phase.setSingleStep(max(1, round(grad * 10.0)))
        self.schrittweite_geaendert.emit(float(grad))

    def _phase_gewaehlt(self, wert: int) -> None:
        self.phase_gewaehlt.emit(theta_grad_aus_regler(wert), self.regler_phase.isSliderDown())

    def _tempo_gewaehlt(self, wert: int) -> None:
        hz = tempo_aus_regler(wert)
        self.lbl_tempo.setText(tempo_text(hz, kompakt=self._kompakt))
        self.tempo_geaendert.emit(hz)

    def _skalierung_fertig(self) -> None:
        text = self.feld_skalierung.text()
        if text.strip() == self._skalierungstext.strip():
            self.zeige_skalierungsfehler(None)
            return
        self.skalierung_eingegeben.emit(text)

    # --- Zustand ---------------------------------------------------------------------------------

    def setze_wiedergabe(self, laeuft: bool) -> None:
        """Beschriftung des Abspielen-Knopfs: „Pause“, solange die Wiedergabe läuft."""
        text, name = regler_namen("pause" if laeuft else "abspielen")
        self.btn_abspielen.setText(text)
        self.btn_abspielen.setAccessibleName(name)
        self.btn_abspielen.setToolTip(f"{name} ({AKTIONS_TASTEN['animation_abspielen'][1]})")
        setze_eigenschaft(self.btn_abspielen, "laeuft", "true" if laeuft else "false")

    def setze_phase(self, theta_rad: float) -> None:
        """Zeigt den Winkel (Anzeige und Regler) ohne Signal (nur Anzeige, kein Rückkanal)."""
        self.lbl_phase_grad.setText(phase_text(theta_rad))
        stand = regler_aus_theta_rad(theta_rad)
        if self.regler_phase.value() != stand:
            sperre = self.regler_phase.blockSignals(True)
            try:
                self.regler_phase.setValue(stand)
            finally:
                self.regler_phase.blockSignals(sperre)

    def setze_nullpunkt(self, text: str) -> None:
        """Tooltip der Winkelanzeige: Bedeutung von θ = 0° (Pflichtangabe, KONVENTIONEN)."""
        self.lbl_phase_grad.setToolTip(text)
        self.regler_phase.setToolTip(text)

    def setze_schrittweite(self, grad: float) -> None:
        """Zeigt die Schrittweite ohne Signal; die Einzelschritte des Reglers folgen ihr."""
        sperre = self.feld_schrittweite.blockSignals(True)
        try:
            self.feld_schrittweite.setValue(grad)
        finally:
            self.feld_schrittweite.blockSignals(sperre)
        self.regler_phase.setSingleStep(max(1, round(grad * 10.0)))

    def setze_tempo(self, tempo_hz: float) -> None:
        """Zeigt das Tempo ohne Signal."""
        sperre = self.regler_tempo.blockSignals(True)
        try:
            self.regler_tempo.setValue(regler_aus_tempo(tempo_hz))
        finally:
            self.regler_tempo.blockSignals(sperre)
        self.lbl_tempo.setText(tempo_text(tempo_hz, kompakt=self._kompakt))

    def setze_skalierung(
        self,
        anzeige: str,
        regler: int,
        feld: str,
        *,
        auto_moeglich: bool,
        schnelle: bool,
    ) -> None:
        """Zeigt die Skalierung (Text, Regler, Feld) ohne Signal.

        Parameters
        ----------
        anzeige : str
            Text der Überhöhungsanzeige (Malzeichen und Zahl, bei der Schnelle mit Skalierung in s).
        regler : int
            Stand des Überhöhungsreglers (0 = automatisch).
        feld : str
            Text des Eingabefelds (leer = Auto).
        auto_moeglich : bool
            ``False`` ohne automatische Skalierung (ein einziger Punkt): der Regler hat dann keine
            Bezugsgröße und ist gesperrt.
        schnelle : bool
            Größe Schnelle (Skalierung in s, längerer Text, Einheit „s“ am Feld).
        """
        if schnelle != self._schnelle:
            self._schnelle = schnelle
            self._breite_ueberhoehung()
        self.lbl_ueberhoehung.setText(anzeige)
        sperre = self.regler_ueberhoehung.blockSignals(True)
        try:
            self.regler_ueberhoehung.setValue(regler)
        finally:
            self.regler_ueberhoehung.blockSignals(sperre)
        self.regler_ueberhoehung.setEnabled(auto_moeglich)
        self._skalierungstext = feld
        self.feld_skalierung.setText(feld)
        setze_eigenschaft(self.feld_skalierung, "fest", "true" if feld else "false")
        einheit = "Skalierung κ in Sekunden" if schnelle else "Überhöhung"
        self.feld_skalierung.setAccessibleName(f"{einheit}, leer = automatisch")
        self.feld_skalierung.setToolTip(f"{einheit}; leer = automatisch")
        self.zeige_skalierungsfehler(None)

    def zeige_skalierungsfehler(self, text: str | None) -> None:
        """Markiert das Feld bei ungültiger Eingabe (gestrichelter Rand, Text im Tooltip)."""
        setze_eigenschaft(self.feld_skalierung, "fehler", "true" if text else "false")
        if text:
            self.feld_skalierung.setToolTip(text)

    def setze_kompakt(self, kompakt: bool) -> None:
        """Kurze Beschriftungen bei schmalem Fenster (< 1200 px); volle Namen im Tooltip."""
        if kompakt == self._kompakt:
            return
        self._kompakt = kompakt
        self._breiten_regler()
        self._feste_breiten()
        self.lbl_tempo.setText(
            tempo_text(tempo_aus_regler(self.regler_tempo.value()), kompakt=kompakt)
        )
        self.lbl_tempo.setToolTip("Perioden je Sekunde" if kompakt else "")
        self._texte_knoepfe()
        self._fluss.setze_abstand(_GRUPPENABSTAND_PX // 2 if kompakt else _GRUPPENABSTAND_PX)
        self.updateGeometry()

    def tab_kette(self) -> list[QWidget]:
        """Bedienbare Elemente in Tab-Reihenfolge (Brief 6: AE → AH → AF)."""
        return [
            self.btn_schritt_zurueck,
            self.btn_abspielen,
            self.btn_schritt_vor,
            self.feld_schrittweite,
            self.regler_phase,
            self.btn_werte_tabelle,
            self.regler_tempo,
            self.regler_ueberhoehung,
            self.feld_skalierung,
            *self.btn_blick.values(),
            self.btn_ansicht_zurueck,
        ]
