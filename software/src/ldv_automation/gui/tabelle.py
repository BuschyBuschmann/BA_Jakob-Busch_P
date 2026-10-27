"""Warteschlangentabelle (Zone D, Brief P3, Abschnitt 1 und 3.4)."""

from __future__ import annotations

from collections.abc import Sequence
from uuid import UUID

from PySide6.QtCore import QModelIndex, QPersistentModelIndex, Qt, Signal
from PySide6.QtGui import QBrush, QColor, QKeyEvent, QKeySequence, QPainter, QShortcut
from PySide6.QtWidgets import (
    QAbstractItemView,
    QHeaderView,
    QLabel,
    QStyledItemDelegate,
    QStyleOptionViewItem,
    QTableWidget,
    QTableWidgetItem,
    QWidget,
)

from ldv_automation.gui import tokens as t
from ldv_automation.gui.anzeige import LEER_TEXT, NR_VORLAEUFIG_TOOLTIP, Zeile
from ldv_automation.gui.stil import schrift

SPALTEN = ("Nr", "Status", "Name", "Einstellungsdatei", "Änderungen", "Limit")
SP_NR, SP_STATUS, SP_NAME, SP_SET, SP_AENDERUNGEN, SP_LIMIT = range(6)

_ROLLE_ID = Qt.ItemDataRole.UserRole + 1
_ROLLE_LAEUFT = Qt.ItemDataRole.UserRole + 2

_STIL_FARBE = {
    "laeuft": t.C_AKZENT,
    "ok": t.C_OK,
    "fehler": t.C_FEHLER,
    "warn": t.C_TEXT,
    "normal": t.C_TEXT,
}


class _Zeichner(QStyledItemDelegate):
    """Zeichnet den 5-px-Akzentbalken links an der laufenden Zeile und die Fokuslinie."""

    def paint(
        self,
        painter: QPainter,
        option: QStyleOptionViewItem,
        index: QModelIndex | QPersistentModelIndex,
    ) -> None:
        super().paint(painter, option, index)
        rect = option.rect
        if index.column() == SP_NR and index.data(_ROLLE_LAEUFT):
            painter.fillRect(rect.x(), rect.y(), 5, rect.height(), QColor(t.C_AKZENT))
        ansicht = self.parent()
        if (
            isinstance(ansicht, QTableWidget)
            and ansicht.hasFocus()
            and ansicht.currentRow() == index.row()
        ):
            painter.fillRect(rect.x(), rect.bottom() - 1, rect.width(), 2, QColor(t.C_AKZENT))


class Warteschlangentabelle(QTableWidget):
    """Tabelle der Einträge; eine Zeile wählbar, nicht sortierbar.

    Signale
    -------
    auswahl_geaendert(object)
        ID des gewählten Eintrags oder ``None``.
    editor_fokus()
        Enter in der Tabelle: Fokus in den Editor.
    """

    auswahl_geaendert = Signal(object)
    editor_fokus = Signal()
    entfernen_taste = Signal()
    hoch_taste = Signal()
    runter_taste = Signal()

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(0, len(SPALTEN), parent)
        self.setObjectName("tabelle")
        self.setAccessibleName("Warteschlange")
        self.setHorizontalHeaderLabels(list(SPALTEN))
        self.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.setSortingEnabled(False)
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.setTabKeyNavigation(False)
        self.setWordWrap(False)
        self.setTextElideMode(Qt.TextElideMode.ElideRight)
        self.setItemDelegate(_Zeichner(self))
        self.verticalHeader().setVisible(False)
        self.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Fixed)
        self.verticalHeader().setDefaultSectionSize(t.ZEILENHOEHE_TABELLE_PX)
        kopf = self.horizontalHeader()
        kopf.setSectionsClickable(False)
        kopf.setSectionsMovable(False)
        kopf.setHighlightSections(False)
        kopf.setMinimumSectionSize(40)
        for spalte, breite in ((SP_NR, 48), (SP_STATUS, 190), (SP_LIMIT, 70)):
            kopf.setSectionResizeMode(spalte, QHeaderView.ResizeMode.Fixed)
            self.setColumnWidth(spalte, breite)
        kopf.setSectionResizeMode(SP_NAME, QHeaderView.ResizeMode.Stretch)
        kopf.setSectionResizeMode(SP_SET, QHeaderView.ResizeMode.Stretch)
        kopf.setSectionResizeMode(SP_AENDERUNGEN, QHeaderView.ResizeMode.Stretch)
        kopf.setStretchLastSection(False)

        self._leer = QLabel(LEER_TEXT, self.viewport())
        self._leer.setObjectName("tabelle_leer")
        self._leer.setProperty("art", "gedaempft")
        self._leer.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._leer.setWordWrap(True)

        self._zeilen: list[Zeile] = []
        self._ids: list[UUID] = []
        self._melde_auswahl = True
        self.itemSelectionChanged.connect(self._auswahl_geaendert)

        for taste, signal in (
            (QKeySequence(Qt.Key.Key_Delete), self.entfernen_taste),
            (QKeySequence(Qt.Modifier.ALT | Qt.Key.Key_Up), self.hoch_taste),
            (QKeySequence(Qt.Modifier.ALT | Qt.Key.Key_Down), self.runter_taste),
        ):
            kurz = QShortcut(taste, self)
            kurz.setContext(Qt.ShortcutContext.WidgetShortcut)
            kurz.activated.connect(signal.emit)

    # --- Anzeige ---------------------------------------------------------------------------

    def resizeEvent(self, event: object) -> None:  # noqa: N802  # Qt-Name
        """Hält den Leer-Hinweis über der ganzen Fläche."""
        super().resizeEvent(event)  # type: ignore[arg-type]
        self._leer.setGeometry(self.viewport().rect().adjusted(16, 16, -16, -16))

    def leer_sichtbar(self) -> bool:
        """Prüft, ob der Hinweis für die leere Warteschlange angezeigt wird."""
        return not self._leer.isHidden()

    @property
    def ids(self) -> tuple[UUID, ...]:
        """IDs der Zeilen in Reihenfolge."""
        return tuple(self._ids)

    def gewaehlte_id(self) -> UUID | None:
        """ID der gewählten Zeile oder ``None``."""
        zeilen = self.selectionModel().selectedRows()
        if not zeilen:
            return None
        zeile = zeilen[0].row()
        return self._ids[zeile] if 0 <= zeile < len(self._ids) else None

    def waehle(self, eintrag_id: UUID | None) -> None:
        """Wählt die Zeile mit ``eintrag_id`` (``None`` hebt die Auswahl auf)."""
        if eintrag_id is None or eintrag_id not in self._ids:
            self.clearSelection()
            return
        zeile = self._ids.index(eintrag_id)
        self.setCurrentCell(zeile, SP_NAME)
        self.selectRow(zeile)

    def zeige(self, ids: Sequence[UUID], zeilen: Sequence[Zeile]) -> None:
        """Schreibt die Zeilen neu, ohne Auswahl und Scrollposition zu verändern."""
        ids = list(ids)
        zeilen = list(zeilen)
        if ids == self._ids and zeilen == self._zeilen:
            return
        gewaehlt = self.gewaehlte_id()
        scroll = self.verticalScrollBar().value()
        self._melde_auswahl = False
        try:
            self.clearSpans()
            self.setRowCount(len(zeilen))
            for r, z in enumerate(zeilen):
                self._schreibe_zeile(r, ids[r], z)
            self._ids = ids
            self._zeilen = zeilen
            if gewaehlt in self._ids:
                zeile = self._ids.index(gewaehlt)
                self.selectRow(zeile)
            else:
                self.clearSelection()
            self.verticalScrollBar().setValue(scroll)
        finally:
            self._melde_auswahl = True
        self._leer.setVisible(not zeilen)
        neu = self.gewaehlte_id()
        if neu != gewaehlt:
            self.auswahl_geaendert.emit(neu)

    def _item(self, r: int, spalte: int) -> QTableWidgetItem:
        item = self.item(r, spalte)
        if item is None:
            item = QTableWidgetItem()
            self.setItem(r, spalte, item)
        return item

    def _schreibe_zeile(self, r: int, eintrag_id: UUID, z: Zeile) -> None:
        werte = (z.nr, z.status.text, z.name, z.einstellungsdatei, z.aenderungen, z.limit)
        tips = ("", z.status.text, z.name, z.einstellungsdatei_tooltip, z.aenderungen_tooltip, "")
        hintergrund: QBrush | None = None
        if z.laeuft:
            hintergrund = QBrush(QColor(t.C_AKTIV_BG))
        elif z.pausenpunkt:
            hintergrund = QBrush(QColor(t.C_WARN_BG)) if z.status.stil == "warn" else None
        for spalte, (wert, tip) in enumerate(zip(werte, tips, strict=True)):
            item = self._item(r, spalte)
            item.setText(wert)
            item.setToolTip(tip)
            item.setData(_ROLLE_ID, str(eintrag_id))
            item.setData(_ROLLE_LAEUFT, z.laeuft)
            item.setBackground(hintergrund if hintergrund is not None else QBrush())
            item.setForeground(QBrush(QColor(t.C_TEXT)))
            item.setFont(schrift())
            ausrichtung = Qt.AlignmentFlag.AlignVCenter
            if spalte in (SP_NR, SP_LIMIT):
                ausrichtung |= Qt.AlignmentFlag.AlignRight
            else:
                ausrichtung |= Qt.AlignmentFlag.AlignLeft
            item.setTextAlignment(ausrichtung)
        status = self._item(r, SP_STATUS)
        status.setForeground(QBrush(QColor(_STIL_FARBE[z.status.stil])))
        status.setFont(schrift(fett=z.status.stil in ("laeuft", "warn")))
        if z.laeuft:
            self._item(r, SP_NAME).setFont(schrift(fett=True))
        if z.nr_vorlaeufig:
            nr = self._item(r, SP_NR)
            nr.setForeground(QBrush(QColor(t.C_TEXT_GEDAEMPFT)))
            kursiv = schrift()
            kursiv.setItalic(True)
            nr.setFont(kursiv)
            nr.setToolTip(NR_VORLAEUFIG_TOOLTIP)
        if z.pausenpunkt:
            self.setSpan(r, SP_NAME, 1, len(SPALTEN) - SP_NAME)

    # --- Bedienung -------------------------------------------------------------------------

    def _auswahl_geaendert(self) -> None:
        if self._melde_auswahl:
            self.auswahl_geaendert.emit(self.gewaehlte_id())

    def keyPressEvent(self, event: QKeyEvent) -> None:  # noqa: N802  # Qt-Name
        """Enter: Fokus in den Editor; Pos1/Ende: erste bzw. letzte Zeile."""
        taste = event.key()
        if taste in (Qt.Key.Key_Return, Qt.Key.Key_Enter) and not event.modifiers():
            self.editor_fokus.emit()
            return
        if taste in (Qt.Key.Key_Home, Qt.Key.Key_End) and self.rowCount():
            zeile = 0 if taste == Qt.Key.Key_Home else self.rowCount() - 1
            self.setCurrentCell(zeile, SP_NAME)
            self.selectRow(zeile)
            return
        super().keyPressEvent(event)
