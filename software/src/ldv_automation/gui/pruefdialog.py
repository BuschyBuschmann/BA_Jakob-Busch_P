"""Fußzeile und Prüfdialog des Reiters „Auswerten“: gekürzte Labels, Prüflabel, Dialog (T4).

``KuerzLabel`` kürzt zu langen Text (Pfade mittig, Aufzählungen an Teilgrenzen, sonst rechts mit
„…“) und hält den Volltext für Tooltip und Hilfsmittel bereit. ``PruefLabel`` zeigt
„Prüfung: 9 ok, 1 Warnung“ in Wörtern (nie nur Farbe), ist per Tab erreichbar und öffnet mit
Klick, Enter oder Leertaste den Dialog. ``PruefDialog`` listet
P-01 bis P-11 (Nummer, Ergebnis, Prüfung, Bezug, Text) schreibgeschützt; Esc schließt ihn
(UI-23, Brief K-AUSW Abschnitt 6).

Dünnes Qt-Modul (Abdeckung nur mit ``pytest -m gui``); die Zeilen entstehen Qt-frei in
:func:`~ldv_automation.gui.anzeige_aktionen.pruefdialog_zeilen`.
"""

from __future__ import annotations

from collections.abc import Sequence

from PySide6.QtCore import QEvent, Qt, Signal
from PySide6.QtGui import QKeyEvent, QMouseEvent, QShowEvent
from PySide6.QtWidgets import (
    QAbstractItemView,
    QDialog,
    QDialogButtonBox,
    QHeaderView,
    QLabel,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

from ldv_automation.gui import tokens as t
from ldv_automation.gui.anzeige_aktionen import kuerze_meldung, kuerze_rechts, kuerze_teile

__all__ = ["SPALTEN", "KuerzLabel", "PruefDialog", "PruefLabel"]

SPALTEN = ("Nr", "Ergebnis", "Prüfung", "Bezug", "Text")
"""Spaltenköpfe des Dialogs (entsprechen ``pruefdialog_zeilen``)."""


class KuerzLabel(QLabel):
    """Einzeiliges Label, das zu langen Text kürzt; der Volltext bleibt erhalten.

    Die verfügbare Breite setzt der Besitzer mit :meth:`setze_platz` (Fußzeile: Verteilung auf
    Meldezeile und Prüftext); ohne Angabe wird nicht gekürzt. ``text()`` liefert den
    **sichtbaren** (ggf. gekürzten) Text, :meth:`volltext` den vollständigen.

    Parameters
    ----------
    teile : bool, optional
        Kürzen an den Teilgrenzen „, “ (Aufzählung) statt mitten im Wort.
    voll_im_tooltip : bool, optional
        Der Volltext steht immer im Tooltip und in ``accessibleDescription`` (Meldezeile);
        sonst nur, wenn der Text gekürzt ist.
    rand : int, optional
        Pixel, die von der Breite abgezogen werden (Rahmen, Fokusrand).
    """

    _voll = ""
    _pfade: tuple[str, ...] = ()
    _platz = 0
    _zusatz = ""

    def __init__(
        self,
        parent: QWidget | None = None,
        *,
        teile: bool = False,
        voll_im_tooltip: bool = False,
        rand: int = 2,
    ) -> None:
        self._teile = teile
        self._immer = voll_im_tooltip
        self._rand = rand
        super().__init__("", parent)

    def setText(self, text: str, pfade: Sequence[str] = ()) -> None:  # noqa: N802  # Qt-Name
        """Setzt den Volltext; ``pfade`` (Teile des Textes) werden mittig gekürzt.

        Das Hilfsmittel erhält den Volltext in ``accessibleDescription``.
        """
        self._voll = text
        self._pfade = tuple(pfade)
        self._kuerze()

    def volltext(self) -> str:
        """Ungekürzter Text."""
        return self._voll

    def ist_gekuerzt(self) -> bool:
        """Gibt ``True`` zurück, wenn der sichtbare Text vom Volltext abweicht."""
        return self.text() != self._voll

    def natuerliche_breite(self) -> int:
        """Breite des Volltextes in Pixeln (ohne Rand)."""
        return int(self.fontMetrics().horizontalAdvance(self._voll)) + self._rand

    def breite_von(self, text: str) -> int:
        """Breite eines beliebigen Textes in der Schrift des Labels (mit Rand)."""
        return int(self.fontMetrics().horizontalAdvance(text)) + self._rand

    def setze_platz(self, platz: int) -> None:
        """Setzt die verfügbare Breite in Pixeln (``<= 0``: unbegrenzt) und kürzt neu."""
        self._platz = platz
        self._kuerze()

    def setze_teile(self, teile: bool) -> None:
        """Wechselt zwischen Kürzen an Teilgrenzen („, “) und Kürzen rechts; kürzt neu."""
        self._teile = teile
        self._kuerze()

    def setze_zusatz_tooltip(self, text: str) -> None:
        """Erklärender Tooltip (z. B. Fehlergrund); steht hinter dem Volltext."""
        self._zusatz = text
        self._tooltip_setzen()

    def changeEvent(self, event: QEvent) -> None:  # noqa: N802  # Qt-Name
        """Kürzt neu, wenn sich die Schrift ändert (die Breite des Textes ändert sich)."""
        super().changeEvent(event)
        if event.type() == QEvent.Type.FontChange:
            self._kuerze()

    def _kuerze(self) -> None:
        breite = self.fontMetrics().horizontalAdvance
        platz = self._platz - self._rand if self._platz > 0 else 0
        if self._pfade:
            sichtbar = kuerze_meldung(self._voll, self._pfade, platz, breite)
        elif self._teile:
            sichtbar = kuerze_teile(self._voll, platz, breite)
        else:
            sichtbar = kuerze_rechts(self._voll, platz, breite)
        QLabel.setText(self, sichtbar)
        self._tooltip_setzen()
        if self._immer:
            self.setAccessibleDescription(self._voll)

    def _tooltip_setzen(self) -> None:
        voll = self._voll if (self._immer or self.ist_gekuerzt()) else ""
        self.setToolTip("\n".join(t_ for t_ in (voll, self._zusatz) if t_))


class PruefLabel(KuerzLabel):
    """Klickbares, fokussierbares Label (Rolle eines Knopfs) für die Prüfzusammenfassung."""

    geklickt = Signal()
    """Klick mit der linken Maustaste, Enter oder Leertaste."""

    def __init__(self, text: str = "", parent: QWidget | None = None) -> None:
        super().__init__(parent, teile=True, rand=6)  # 2 px Rahmen links und rechts bei Fokus
        self.setText(text)
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setAccessibleName("Prüfzusammenfassung")
        self.setAccessibleDescription("Öffnet die Liste der Prüfungen P-01 bis P-11")

    def mouseReleaseEvent(self, event: QMouseEvent) -> None:  # noqa: N802  # Qt-Name
        """Klick mit der linken Maustaste innerhalb des Labels öffnet den Dialog."""
        if event.button() == Qt.MouseButton.LeftButton and self.rect().contains(
            event.position().toPoint()
        ):
            self.geklickt.emit()
        super().mouseReleaseEvent(event)

    def keyPressEvent(self, event: QKeyEvent) -> None:  # noqa: N802  # Qt-Name
        """Enter, Return und Leertaste öffnen den Dialog."""
        if event.key() in (Qt.Key.Key_Return, Qt.Key.Key_Enter, Qt.Key.Key_Space):
            self.geklickt.emit()
            return
        super().keyPressEvent(event)


class PruefDialog(QDialog):
    """Schreibgeschützte Liste der Prüfungen P-01 bis P-11.

    Parameters
    ----------
    zusammenfassung : str
        Zusammenfassung in Wörtern („Prüfung: 9 ok, 1 Warnung“) als Kopfzeile.
    zeilen : sequence of tuple
        ``(Nr, Ergebnis, Prüfung, Bezug, Text)`` je Prüfung.
    leer_text : str, optional
        Hinweis, wenn keine Zeilen vorliegen (Prüfung noch nicht berechnet).
    start_zeile : int, optional
        Zeile, die beim Öffnen gewählt und sichtbar gescrollt wird (erste Warnung bzw. erster
        Fehler); die Reihenfolge nach Prüfnummer bleibt.
    parent : QWidget, optional
        Elternwidget.
    """

    def __init__(
        self,
        zusammenfassung: str,
        zeilen: Sequence[tuple[str, str, str, str, str]],
        leer_text: str = "",
        start_zeile: int | None = None,
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)
        self._start_zeile = start_zeile
        self.setObjectName("pruef_dialog")
        self.setWindowTitle("Plausibilitätsprüfungen")
        self.setModal(True)
        self.resize(900, 420)
        layout = QVBoxLayout(self)
        self.lbl_zusammenfassung = QLabel(zusammenfassung)
        self.lbl_zusammenfassung.setObjectName("lbl_pruef_zusammenfassung")
        layout.addWidget(self.lbl_zusammenfassung)
        self.tabelle = QTableWidget(len(zeilen), len(SPALTEN))
        self.tabelle.setObjectName("tabelle_pruefung")
        self.tabelle.setAccessibleName("Liste der Prüfungen P-01 bis P-11")
        self.tabelle.setHorizontalHeaderLabels(list(SPALTEN))
        self.tabelle.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.tabelle.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.tabelle.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.tabelle.setWordWrap(True)
        self.tabelle.setAlternatingRowColors(False)
        self.tabelle.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.tabelle.verticalHeader().setVisible(False)
        self.tabelle.verticalHeader().setDefaultSectionSize(t.ZEILENHOEHE_TABELLE_PX)
        kopf = self.tabelle.horizontalHeader()
        kopf.setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        kopf.setSectionResizeMode(len(SPALTEN) - 1, QHeaderView.ResizeMode.Stretch)
        for i, zeile in enumerate(zeilen):
            for j, text in enumerate(zeile):
                self.tabelle.setItem(i, j, QTableWidgetItem(text))
        self.tabelle.resizeRowsToContents()
        for i in range(len(zeilen)):  # mindestens die Zeilenhöhe der Tabellen (32 px)
            self.tabelle.setRowHeight(i, max(self.tabelle.rowHeight(i), t.ZEILENHOEHE_TABELLE_PX))
        if start_zeile is not None and 0 <= start_zeile < len(zeilen):
            self.tabelle.selectRow(start_zeile)
            self.tabelle.setCurrentCell(start_zeile, 0)
            self.tabelle.setFocus()
        layout.addWidget(self.tabelle, 1)
        self.lbl_leer = QLabel(leer_text)
        self.lbl_leer.setObjectName("lbl_pruef_leer")
        self.lbl_leer.setVisible(not zeilen and bool(leer_text))
        layout.addWidget(self.lbl_leer)
        tasten = QDialogButtonBox(QDialogButtonBox.StandardButton.Close)
        tasten.button(QDialogButtonBox.StandardButton.Close).setText("Schließen")
        tasten.button(QDialogButtonBox.StandardButton.Close).setAutoDefault(False)
        tasten.rejected.connect(self.reject)
        layout.addWidget(tasten)

    def showEvent(self, event: QShowEvent) -> None:  # noqa: N802  # Qt-Name
        """Scrollt die Startzeile (erste Warnung bzw. erster Fehler) in den sichtbaren Bereich."""
        super().showEvent(event)
        zeile = self._start_zeile
        if zeile is not None and 0 <= zeile < self.tabelle.rowCount():
            item = self.tabelle.item(zeile, 0)
            if item is not None:
                self.tabelle.scrollToItem(item, QAbstractItemView.ScrollHint.PositionAtTop)
