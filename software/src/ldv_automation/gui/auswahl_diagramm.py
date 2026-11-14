"""Auswahlseite (Zone AD) von Ansicht 5 „Diagramm“ (R-058/R-059, P-AUSW2 S7, Brief K1-AUSW2 3.2).

Dünnes Widgetmodul (Abdeckung nur mit ``pytest -m gui``): Größe (Radioknöpfe, eine für das ganze
Diagramm), Anordnung, Serienliste mit Linienprobe und Sichtbar-Häkchen sowie die Knöpfe
``+ Serie``, ``Entfernen`` und ``Für alle Messungen``. Regeln und Texte liegen Qt-frei in
:mod:`.serien`; das Widget meldet nur Bedienung über Signale. Der Serien-Dialog (``+ Serie``) ist
ein kleiner modaler Dialog (Esc schließt) und liefert eine
:class:`~ldv_automation.darstellung.serien_daten.SerienSpec`.
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import dataclass

from PySide6.QtCore import QSize, Qt, Signal
from PySide6.QtGui import QColor, QIcon, QPainter, QPen, QPixmap
from PySide6.QtWidgets import (
    QBoxLayout,
    QButtonGroup,
    QComboBox,
    QDialog,
    QDialogButtonBox,
    QFormLayout,
    QHBoxLayout,
    QLabel,
    QListWidget,
    QListWidgetItem,
    QPushButton,
    QRadioButton,
    QVBoxLayout,
    QWidget,
)

from ldv_automation.darstellung.diagramm import Anordnung
from ldv_automation.darstellung.serien_daten import (
    GROESSEN,
    GROESSEN_NAMEN,
    GroessenId,
    SerienSpec,
)
from ldv_automation.darstellung.stil import Plotstil
from ldv_automation.gui.auswahl_auswerten import tab_halt
from ldv_automation.gui.serien import (
    TEXT_SERIEN_VOLL,
    SerienFehler,
    baue_spec,
)
from ldv_automation.gui.stil import schrift

__all__ = ["AuswahlDiagramm", "MessungsAngabe", "SerienDialog", "SerienEintrag", "linienprobe"]

_PEN_STILE: Mapping[str, Qt.PenStyle] = {
    "-": Qt.PenStyle.SolidLine,
    "--": Qt.PenStyle.DashLine,
    ":": Qt.PenStyle.DotLine,
    "-.": Qt.PenStyle.DashDotLine,
}
LISTE_MIN_HOEHE_PX = 56
"""Mindesthöhe der Serienliste (leer oder ein Eintrag); sonst wächst sie mit den Zeilen."""
PROBE_BREITE_PX = 36
PROBE_HOEHE_PX = 14


def linienprobe(stil: Plotstil, slot: int) -> QIcon:
    """Linienprobe der Serie (Linienart und Farbe des Slots, wie im Plot)."""
    bild = QPixmap(PROBE_BREITE_PX, PROBE_HOEHE_PX)
    bild.fill(Qt.GlobalColor.transparent)
    maler = QPainter(bild)
    stift = QPen(QColor(stil.serienfarbe(slot)))
    stift.setWidthF(2.0)
    stift.setStyle(_PEN_STILE.get(stil.linienart(slot), Qt.PenStyle.SolidLine))
    maler.setPen(stift)
    maler.drawLine(1, PROBE_HOEHE_PX // 2, PROBE_BREITE_PX - 1, PROBE_HOEHE_PX // 2)
    maler.end()
    return QIcon(bild)


@dataclass(frozen=True)
class SerienEintrag:
    """Eine Zeile der Serienliste.

    Attributes
    ----------
    text : str
        Zeilentext („A · Punkt 100 · Vib X / Ref1“).
    slot : int
        Slot der Serie (bestimmt die Linienprobe).
    sichtbar : bool
        Sichtbar-Häkchen.
    problem : str
        Grund, wenn die Serie nicht gezeichnet werden kann (Symbol plus Wort in der Zeile);
        leer = darstellbar.
    """

    text: str
    slot: int
    sichtbar: bool
    problem: str = ""


class AuswahlDiagramm(QWidget):
    """Ansicht 5: Größe, Anordnung und Serienliste.

    Signals
    -------
    groesse_geaendert : str
        Radioknopf „Größe“ (eine Größe für das ganze Diagramm).
    geaendert : (kein Wert)
        Teilgröße oder Anordnung geändert (neu zeichnen).
    serie_neu, serie_alle : (kein Wert)
        ``+ Serie`` bzw. ``Für alle Messungen``.
    serie_entfernen : int
        ``Entfernen`` mit der Zeile der gewählten Serie.
    serie_sichtbar : int, bool
        Sichtbar-Häkchen einer Zeile.
    """

    groesse_geaendert = Signal(str)
    geaendert = Signal()
    serie_neu = Signal()
    serie_alle = Signal()
    serie_entfernen = Signal(int)
    serie_sichtbar = Signal(int, bool)

    def __init__(self, stil: Plotstil, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setObjectName("auswahl_diagramm")
        self._stil = stil
        self._fuellt = False
        v = QVBoxLayout(self)
        v.setContentsMargins(0, 0, 8, 0)
        v.setSpacing(6)

        v.addWidget(_titel("Größe"))
        self._gruppe_groesse = QButtonGroup(self)
        self.rb_groesse: dict[GroessenId, QRadioButton] = {}
        self._lbl_grund: dict[GroessenId, QLabel] = {}
        for g in GROESSEN:
            knopf = QRadioButton(GROESSEN_NAMEN[g])
            knopf.setObjectName(f"rb_groesse_{g}")
            knopf.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
            knopf.setAccessibleName(f"Größe {GROESSEN_NAMEN[g]}")
            self._gruppe_groesse.addButton(knopf)
            self.rb_groesse[g] = knopf
            v.addWidget(knopf)
            grund = _gedaempft(f"lbl_groesse_grund_{g}")
            grund.setVisible(False)
            self._lbl_grund[g] = grund
            v.addWidget(grund)
        self.rb_groesse["spektrum"].setChecked(True)
        tab_halt(self._gruppe_groesse)

        self._teil = QWidget()
        self._teil.setObjectName("teilgroesse_gruppe")
        tv = QVBoxLayout(self._teil)
        tv.setContentsMargins(16, 0, 0, 0)
        tv.setSpacing(2)
        self._gruppe_teil = QButtonGroup(self)
        self.rb_teil_cph = QRadioButton("|CPH|, kohärent mit Referenz")
        self.rb_teil_cph.setObjectName("rb_teil_cph")
        self.rb_teil_ap = QRadioButton("√AP, Leistungsmittel")
        self.rb_teil_ap.setObjectName("rb_teil_ap")
        for knopf in (self.rb_teil_cph, self.rb_teil_ap):
            knopf.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
            self._gruppe_teil.addButton(knopf)
            tv.addWidget(knopf)
        self.rb_teil_cph.setChecked(True)
        tab_halt(self._gruppe_teil)
        v.addWidget(self._teil)

        v.addWidget(_titel("Anordnung"))
        self._gruppe_anordnung = QButtonGroup(self)
        self.rb_anordnung_ueberlagert = QRadioButton("überlagert")
        self.rb_anordnung_ueberlagert.setObjectName("rb_anordnung_ueberlagert")
        self.rb_anordnung_nebeneinander = QRadioButton("nebeneinander")
        self.rb_anordnung_nebeneinander.setObjectName("rb_anordnung_nebeneinander")
        # untereinander; bei kleinem Fenster nebeneinander (spart eine Zeile für die Serienliste)
        self._anordnung_box = QWidget()
        self._anordnung_zeile = QBoxLayout(QBoxLayout.Direction.TopToBottom, self._anordnung_box)
        self._anordnung_zeile.setContentsMargins(0, 0, 0, 0)
        for knopf in (self.rb_anordnung_ueberlagert, self.rb_anordnung_nebeneinander):
            knopf.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
            self._gruppe_anordnung.addButton(knopf)
            self._anordnung_zeile.addWidget(knopf)
        v.addWidget(self._anordnung_box)
        self.rb_anordnung_ueberlagert.setChecked(True)
        tab_halt(self._gruppe_anordnung)

        v.addWidget(_titel("Serien (Häkchen = sichtbar)"))
        self.btn_serie_neu = QPushButton("+ Serie")
        self.btn_serie_neu.setObjectName("btn_serie_neu")
        self.btn_serie_entfernen = QPushButton("Entfernen")
        self.btn_serie_entfernen.setObjectName("btn_serie_entfernen")
        self.btn_serie_alle = QPushButton("Für alle Messungen")
        self.btn_serie_alle.setObjectName("btn_serie_alle")
        for taste in (self.btn_serie_neu, self.btn_serie_entfernen, self.btn_serie_alle):
            taste.setAutoDefault(False)
            taste.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        # Die Knöpfe stehen über der Liste: Bei vier Serien und kleinem Fenster (1100 mal 680)
        # bleiben sie sichtbar, statt unter der Liste aus der Spalte zu rutschen (Design-Abnahme).
        knopfzeile = QHBoxLayout()
        knopfzeile.setSpacing(6)
        knopfzeile.addWidget(self.btn_serie_neu)
        knopfzeile.addWidget(self.btn_serie_entfernen)
        v.addLayout(knopfzeile)
        v.addWidget(self.btn_serie_alle)
        self.liste_serien = QListWidget()
        self.liste_serien.setObjectName("liste_serien")
        self.liste_serien.setAccessibleName("Serien des Diagramms")
        self.liste_serien.setIconSize(QSize(PROBE_BREITE_PX, PROBE_HOEHE_PX))
        self.liste_serien.setMinimumHeight(LISTE_MIN_HOEHE_PX)
        self.liste_serien.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.liste_serien.setWordWrap(True)
        self.liste_serien.setTextElideMode(Qt.TextElideMode.ElideRight)
        v.addWidget(self.liste_serien)
        self.lbl_voll = _gedaempft("lbl_serien_voll", TEXT_SERIEN_VOLL)
        self.lbl_voll.setVisible(False)
        self._voll = False
        self._kompakt = False
        v.addWidget(self.lbl_voll)
        self.lbl_meldung = _gedaempft("lbl_serien_meldung")
        self.lbl_meldung.setVisible(False)
        v.addWidget(self.lbl_meldung)
        self.lbl_hinweise = _gedaempft("lbl_hinweise_5")
        v.addWidget(self.lbl_hinweise)
        v.addStretch(1)

        self._gruppe_groesse.buttonToggled.connect(self._groesse_gewaehlt)
        self._gruppe_teil.buttonToggled.connect(lambda _k, _an: self._teil_geaendert())
        self._gruppe_anordnung.buttonToggled.connect(lambda _k, _an: self._anordnung_geaendert())
        self.liste_serien.itemChanged.connect(self._item_geaendert)
        self.liste_serien.currentRowChanged.connect(lambda _r: self._sync_knoepfe())
        self.btn_serie_neu.clicked.connect(self.serie_neu)
        self.btn_serie_alle.clicked.connect(self.serie_alle)
        self.btn_serie_entfernen.clicked.connect(self._entfernen_geklickt)
        self._sync_knoepfe()

    # --- Zugriff ---------------------------------------------------------------------------

    def groesse(self) -> GroessenId:
        """Gewählte Größe des Diagramms."""
        return next((g for g, k in self.rb_groesse.items() if k.isChecked()), "spektrum")

    def teilgroesse(self) -> str:
        """Teilgröße des Spektrums: ``"kohaerent"`` (|CPH|) oder ``"leistung"`` (√AP)."""
        return "kohaerent" if self.rb_teil_cph.isChecked() else "leistung"

    def anordnung(self) -> Anordnung:
        """Gewählte Anordnung."""
        return "nebeneinander" if self.rb_anordnung_nebeneinander.isChecked() else "ueberlagert"

    def tab_kette(self) -> list[QWidget]:
        """Bedienbare Teile in Tab-Reihenfolge."""
        kette: list[QWidget] = [*self.rb_groesse.values(), self.rb_teil_cph, self.rb_teil_ap]
        kette += [self.rb_anordnung_ueberlagert, self.rb_anordnung_nebeneinander]
        kette += [self.btn_serie_neu, self.btn_serie_entfernen, self.btn_serie_alle]
        kette.append(self.liste_serien)
        return kette

    # --- Anzeige ---------------------------------------------------------------------------

    def setze_groessen(self, verfuegbar: Mapping[GroessenId, str | None]) -> None:
        """Sperrt nicht verfügbare Größen mit Begründung neben dem Knopf (UI-17)."""
        self._fuellt = True
        try:
            for g, knopf in self.rb_groesse.items():
                grund = verfuegbar.get(g)
                knopf.setEnabled(grund is None)
                knopf.setToolTip(grund or "")
                self._lbl_grund[g].setText(grund or "")
                self._lbl_grund[g].setVisible(grund is not None)
            if not self.rb_groesse[self.groesse()].isEnabled():
                erste = next((k for k in self.rb_groesse.values() if k.isEnabled()), None)
                if erste is not None:
                    erste.setChecked(True)
            tab_halt(self._gruppe_groesse)
        finally:
            self._fuellt = False
        self._teil.setVisible(self.groesse() == "spektrum")

    def setze_teilgroesse_moeglich(self, grund: str | None) -> None:
        """Sperrt |CPH| ohne Referenz (Rückfall auf √AP)."""
        self.rb_teil_cph.setEnabled(grund is None)
        self.rb_teil_cph.setToolTip(grund or "")
        if grund is not None and not self.rb_teil_ap.isChecked():
            self._fuellt = True
            try:
                self.rb_teil_ap.setChecked(True)
            finally:
                self._fuellt = False

    def setze_serien(self, eintraege: Sequence[SerienEintrag], *, symbol_fehler: str) -> None:
        """Füllt die Serienliste (Linienprobe, Sichtbar-Häkchen, Markierung unmöglicher Serien)."""
        zeile = self.liste_serien.currentRow()
        self._fuellt = True
        try:
            self.liste_serien.clear()
            for e in eintraege:
                text = e.text if not e.problem else f"{symbol_fehler} Nicht darstellbar: {e.text}"
                item = QListWidgetItem(linienprobe(self._stil, e.slot), text)
                item.setFlags(
                    Qt.ItemFlag.ItemIsEnabled
                    | Qt.ItemFlag.ItemIsSelectable
                    | Qt.ItemFlag.ItemIsUserCheckable
                )
                item.setCheckState(Qt.CheckState.Checked if e.sichtbar else Qt.CheckState.Unchecked)
                item.setToolTip(e.problem or f"{e.text} (Häkchen = sichtbar)")
                self.liste_serien.addItem(item)
            if 0 <= zeile < self.liste_serien.count():
                self.liste_serien.setCurrentRow(zeile)
        finally:
            self._fuellt = False
        self._passe_listenhoehe()
        self._sync_knoepfe()

    def _passe_listenhoehe(self) -> None:
        """Listenhöhe nach Zeilenzahl: so hoch wie die Einträge, mindestens zwei Zeilen."""
        liste = self.liste_serien
        zeilen = sum(max(liste.sizeHintForRow(i), 0) for i in range(liste.count()))
        hoehe = max(zeilen, LISTE_MIN_HOEHE_PX - 2 * liste.frameWidth()) + 2 * liste.frameWidth()
        liste.setMinimumHeight(hoehe)
        liste.setMaximumHeight(hoehe)

    def setze_voll(self, voll: bool) -> None:
        """``+ Serie`` bei voller Liste sperren (Text unter den Knöpfen)."""
        self._voll = voll
        self.btn_serie_neu.setEnabled(not voll)
        self.btn_serie_neu.setToolTip(TEXT_SERIEN_VOLL if voll else "")
        self.lbl_voll.setVisible(voll and not self._kompakt)

    def setze_kompakt(self, kompakt: bool) -> None:
        """Kleines Fenster: Platz für die Serienliste (vier Serien bei 1100 mal 680 sichtbar).

        Der Hinweis „Höchstens vier Serien“ steht dann nur im Tooltip von ``+ Serie``, die beiden
        Knöpfe der Anordnung stehen nebeneinander.
        """
        self._kompakt = kompakt
        self.lbl_voll.setVisible(self._voll and not kompakt)
        self._anordnung_zeile.setDirection(
            QBoxLayout.Direction.LeftToRight if kompakt else QBoxLayout.Direction.TopToBottom
        )

    def setze_meldung(self, text: str) -> None:
        """Hinweis unter den Knöpfen (z. B. „Diese Serie gibt es bereits.“)."""
        self.lbl_meldung.setText(text)
        self.lbl_meldung.setVisible(bool(text))

    def setze_hinweise(self, text: str) -> None:
        """Hinweise der Zeichenfunktion und Gründe nicht darstellbarer Serien."""
        self.lbl_hinweise.setText(text)
        self.lbl_hinweise.setVisible(bool(text))

    def zuruecksetzen(self) -> None:
        """Voreinstellung: Spektrum, überlagert, keine Serie."""
        self._fuellt = True
        try:
            self.rb_groesse["spektrum"].setChecked(True)
            self.rb_teil_cph.setChecked(True)
            self.rb_anordnung_ueberlagert.setChecked(True)
            self.liste_serien.clear()
        finally:
            self._fuellt = False
        self._passe_listenhoehe()
        self._teil.setVisible(True)
        self.setze_meldung("")
        self._sync_knoepfe()

    # --- Bedienung -------------------------------------------------------------------------

    def _sync_knoepfe(self) -> None:
        self.btn_serie_entfernen.setEnabled(self.liste_serien.currentRow() >= 0)

    def _groesse_gewaehlt(self, _knopf: QRadioButton, an: bool) -> None:
        tab_halt(self._gruppe_groesse)
        if self._fuellt or not an:
            return
        self._teil.setVisible(self.groesse() == "spektrum")
        self.groesse_geaendert.emit(self.groesse())

    def _teil_geaendert(self) -> None:
        tab_halt(self._gruppe_teil)
        if not self._fuellt:
            self.geaendert.emit()

    def _anordnung_geaendert(self) -> None:
        tab_halt(self._gruppe_anordnung)
        if not self._fuellt:
            self.geaendert.emit()

    def _item_geaendert(self, item: QListWidgetItem) -> None:
        if self._fuellt:
            return
        self.serie_sichtbar.emit(
            self.liste_serien.row(item), item.checkState() == Qt.CheckState.Checked
        )

    def _entfernen_geklickt(self) -> None:
        zeile = self.liste_serien.currentRow()
        if zeile >= 0:
            self.serie_entfernen.emit(zeile)


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


# --- Serien-Dialog --------------------------------------------------


@dataclass(frozen=True)
class MessungsAngabe:
    """Was der Dialog über eine Messung wissen muss.

    Attributes
    ----------
    id : int
        Kennung.
    kurzname : str
        Anzeigename.
    labels : tuple of int
        Punktlabels der Messung.
    paare : tuple
        Kanalpaare (Antwort, Referenz).
    """

    id: int
    kurzname: str
    labels: tuple[int, ...]
    paare: tuple[tuple[str, str], ...]


class SerienDialog(QDialog):
    """``+ Serie``: Messung, Punkt (oder Mittel), Komponente bzw. Kanalpaar (modal, Esc schließt).

    Parameters
    ----------
    messungen : sequence of MessungsAngabe
        Bereite Messungen.
    groesse : GroessenId
        Größe des Diagramms; bei Anordnung „nebeneinander“ wählt der Dialog sie je Serie.
    teilgroesse : str
        ``"kohaerent"`` oder ``"leistung"`` für das Spektrum.
    nebeneinander : bool
        Größe je Serie wählbar.
    aktiv_id : int, optional
        Vorgewählte Messung.
    parent : QWidget, optional
        Elternwidget.
    """

    def __init__(
        self,
        messungen: Sequence[MessungsAngabe],
        groesse: GroessenId,
        teilgroesse: str,
        *,
        nebeneinander: bool,
        aktiv_id: int | None = None,
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)
        self.setObjectName("dialog_serie")
        self.setWindowTitle("Serie hinzufügen")
        self.setModal(True)
        self._messungen = {m.id: m for m in messungen}
        self._teilgroesse = teilgroesse
        form = QFormLayout()
        self.combo_messung = QComboBox()
        self.combo_messung.setObjectName("combo_serie_messung")
        self.combo_messung.setAccessibleName("Messung der Serie")
        for m in messungen:
            self.combo_messung.addItem(f"{m.kurzname}", m.id)
        self.combo_groesse = QComboBox()
        self.combo_groesse.setObjectName("combo_serie_groesse")
        self.combo_groesse.setAccessibleName("Größe der Serie")
        for g in GROESSEN:
            self.combo_groesse.addItem(GROESSEN_NAMEN[g], g)
        self.combo_groesse.setCurrentIndex(GROESSEN.index(groesse))
        self.combo_punkt = QComboBox()
        self.combo_punkt.setObjectName("combo_serie_punkt")
        self.combo_punkt.setAccessibleName("Punkt oder Mittel")
        self.combo_komponente = QComboBox()
        self.combo_komponente.setObjectName("combo_serie_komponente")
        self.combo_komponente.setAccessibleName("Komponente")
        for c in ("X", "Y", "Z", "3D"):
            self.combo_komponente.addItem(c if c == "3D" else f"Vib {c}", c)
        self.combo_paar = QComboBox()
        self.combo_paar.setObjectName("combo_serie_paar")
        self.combo_paar.setAccessibleName("Kanalpaar")
        form.addRow("Messung", self.combo_messung)
        self._zeile_groesse = QLabel("Größe")
        form.addRow(self._zeile_groesse, self.combo_groesse)
        form.addRow("Punkt", self.combo_punkt)
        self._zeile_komponente = QLabel("Komponente")
        form.addRow(self._zeile_komponente, self.combo_komponente)
        self._zeile_paar = QLabel("Kanalpaar")
        form.addRow(self._zeile_paar, self.combo_paar)
        self.lbl_fehler = _gedaempft("lbl_serie_fehler")
        tasten = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        tasten.button(QDialogButtonBox.StandardButton.Ok).setText("Übernehmen")
        tasten.button(QDialogButtonBox.StandardButton.Cancel).setText("Abbrechen")
        tasten.accepted.connect(self.accept)
        tasten.rejected.connect(self.reject)
        v = QVBoxLayout(self)
        v.addLayout(form)
        v.addWidget(self.lbl_fehler)
        v.addWidget(tasten)
        self._groesse_sichtbar = nebeneinander
        self.combo_messung.currentIndexChanged.connect(self._messung_gewaehlt)
        self.combo_groesse.currentIndexChanged.connect(self._groesse_gewaehlt)
        if aktiv_id is not None and (i := self.combo_messung.findData(aktiv_id)) >= 0:
            self.combo_messung.setCurrentIndex(i)
        self._messung_gewaehlt()
        self._groesse_gewaehlt()

    def _messung_gewaehlt(self, _index: int = 0) -> None:
        m = self._messungen.get(self.combo_messung.currentData())
        self.combo_punkt.clear()
        self.combo_paar.clear()
        self.combo_punkt.addItem("Mittel (alle Punkte)", None)
        if m is None:
            return
        for label in m.labels:
            self.combo_punkt.addItem(f"Punkt {label}", label)
        for antwort, referenz in m.paare:
            self.combo_paar.addItem(f"{antwort} / {referenz}", (antwort, referenz))

    def _groesse_gewaehlt(self, _index: int = 0) -> None:
        spektrum = self.groesse() == "spektrum"
        self._zeile_groesse.setVisible(self._groesse_sichtbar)
        self.combo_groesse.setVisible(self._groesse_sichtbar)
        self._zeile_komponente.setVisible(spektrum)
        self.combo_komponente.setVisible(spektrum)
        self._zeile_paar.setVisible(not spektrum)
        self.combo_paar.setVisible(not spektrum)

    def groesse(self) -> GroessenId:
        """Gewählte Größe (bei überlagerter Anordnung die des Diagramms)."""
        daten = self.combo_groesse.currentData()
        return daten if daten in GROESSEN else "spektrum"

    def ergebnis(self) -> SerienSpec | None:
        """Beschreibung der gewählten Serie (``None``, wenn die Angaben nicht reichen)."""
        messung_id = self.combo_messung.currentData()
        if messung_id is None:
            return None
        try:
            spec = baue_spec(
                int(messung_id),
                self.combo_punkt.currentData(),
                self.groesse(),
                komponente=self.combo_komponente.currentData(),
                kanalpaar=self.combo_paar.currentData(),
                teilgroesse=self._teilgroesse,
            )
        except SerienFehler as fehler:
            self.lbl_fehler.setText(str(fehler))
            return None
        return spec
