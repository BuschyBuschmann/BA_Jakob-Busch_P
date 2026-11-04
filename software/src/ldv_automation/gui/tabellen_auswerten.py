"""Tabellen der Ansicht 3 (P-AUSW T3b, Brief K-AUSW 3.3): Spitzen und Bänder.

Dünnes Widgetmodul (Abdeckung nur mit ``pytest -m gui``): Die Zeilen entstehen Qt-frei in
:mod:`.daten_auswerten`; hier stehen nur Modell, Sortierung und Auswahl. Zeilenhöhe 32 px,
Sortieren per Klick auf den Spaltenkopf, Auswahl einer Zeile meldet den Schlüssel des Eintrags.
Ohne Zeilen zeigt der Bereich statt der Tabelle den Platzhaltertext (Zustände „Keine Spitzensuche“,
„Keine Spitzen gefunden“, „Keine Bänder angegeben“).
"""

from __future__ import annotations

from collections.abc import Sequence

from PySide6.QtCore import (
    QAbstractTableModel,
    QModelIndex,
    QPersistentModelIndex,
    QSortFilterProxyModel,
    Qt,
    Signal,
)
from PySide6.QtWidgets import (
    QAbstractItemView,
    QHeaderView,
    QLabel,
    QStackedWidget,
    QTableView,
    QWidget,
)

from ldv_automation.gui.daten_auswerten import TabellenZeile
from ldv_automation.gui.stil import schrift

__all__ = ["TabellenBereich", "ZeilenModell"]

ZEILENHOEHE_PX = 32
"""Zeilenhöhe der Tabellen (Brief P3, Tabellenzeilen)."""

_Index = QModelIndex | QPersistentModelIndex
_WURZEL = QModelIndex()


class ZeilenModell(QAbstractTableModel):
    """Tabellenmodell aus :class:`~.daten_auswerten.TabellenZeile` (Anzeige und Sortierwert)."""

    def __init__(self, spalten: Sequence[str], parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._spalten = tuple(spalten)
        self._zeilen: tuple[TabellenZeile, ...] = ()

    def setze_zeilen(self, zeilen: Sequence[TabellenZeile]) -> None:
        """Ersetzt alle Zeilen."""
        self.beginResetModel()
        self._zeilen = tuple(zeilen)
        self.endResetModel()

    def zeile(self, row: int) -> TabellenZeile:
        """Zeile ``row`` (Modellreihenfolge, unsortiert)."""
        return self._zeilen[row]

    def rowCount(self, parent: _Index = _WURZEL) -> int:  # noqa: N802  # Qt-Name
        """Anzahl der Zeilen."""
        return 0 if parent.isValid() else len(self._zeilen)

    def columnCount(self, parent: _Index = _WURZEL) -> int:  # noqa: N802  # Qt-Name
        """Anzahl der Spalten."""
        return 0 if parent.isValid() else len(self._spalten)

    def headerData(  # noqa: N802  # Qt-Name
        self, section: int, orientation: Qt.Orientation, role: int = Qt.ItemDataRole.DisplayRole
    ) -> object:
        """Spaltenköpfe."""
        if orientation == Qt.Orientation.Horizontal and role == Qt.ItemDataRole.DisplayRole:
            return self._spalten[section]
        return None

    def data(self, index: _Index, role: int = Qt.ItemDataRole.DisplayRole) -> object:
        """Anzeigetext, Sortierwert (``UserRole``) und Ausrichtung."""
        if not index.isValid():
            return None
        zeile = self._zeilen[index.row()]
        if role == Qt.ItemDataRole.DisplayRole:
            return zeile.zellen[index.column()]
        if role == Qt.ItemDataRole.UserRole:
            return zeile.sortwerte[index.column()]
        if role == Qt.ItemDataRole.ToolTipRole:
            return zeile.zellen[index.column()]
        if role == Qt.ItemDataRole.TextAlignmentRole:
            zahl = isinstance(zeile.sortwerte[index.column()], float)
            return int(
                (Qt.AlignmentFlag.AlignRight if zahl else Qt.AlignmentFlag.AlignLeft)
                | Qt.AlignmentFlag.AlignVCenter
            )
        return None


class TabellenBereich(QStackedWidget):
    """Tabelle oder Platzhaltertext (je nachdem, ob Zeilen vorhanden sind).

    Parameters
    ----------
    name : str
        ``objectName`` der Tabelle (``tabelle_spitzen``, ``tabelle_baender``); der Bereich
        selbst heißt ``<name>_bereich``, der Platzhalter ``<name>_leer``.
    spalten : sequence of str
        Spaltenköpfe.

    Signals
    -------
    zeile_gewaehlt(int)
        Schlüssel (:attr:`~.daten_auswerten.TabellenZeile.schluessel`) der gewählten Zeile.
    """

    zeile_gewaehlt = Signal(int)

    def __init__(self, name: str, spalten: Sequence[str], parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setObjectName(f"{name}_bereich")
        self.modell = ZeilenModell(spalten, self)
        self._proxy = QSortFilterProxyModel(self)
        self._proxy.setSourceModel(self.modell)
        self._proxy.setSortRole(Qt.ItemDataRole.UserRole)
        self.tabelle = QTableView()
        self.tabelle.setObjectName(name)
        self.tabelle.setAccessibleName(name.replace("tabelle_", "Tabelle ").replace("_", " "))
        self.tabelle.setModel(self._proxy)
        self.tabelle.setSortingEnabled(True)
        self.tabelle.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.tabelle.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.tabelle.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.tabelle.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.tabelle.setAlternatingRowColors(False)
        self.tabelle.verticalHeader().setVisible(False)
        self.tabelle.verticalHeader().setDefaultSectionSize(ZEILENHOEHE_PX)
        self.tabelle.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Fixed)
        kopf = self.tabelle.horizontalHeader()
        kopf.setStretchLastSection(True)
        kopf.setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        kopf.setSortIndicatorShown(True)
        self.tabelle.setFont(schrift(mono=False))
        self.leer = QLabel()
        self.leer.setObjectName(f"{name}_leer")
        self.leer.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.leer.setWordWrap(True)
        self.addWidget(self.leer)
        self.addWidget(self.tabelle)
        self.tabelle.selectionModel().currentRowChanged.connect(self._zeile_gewechselt)
        self.setCurrentIndex(0)

    def setze(self, zeilen: Sequence[TabellenZeile], leer_text: str) -> None:
        """Zeigt ``zeilen`` bzw. ``leer_text``, wenn keine Zeile vorhanden ist."""
        self.modell.setze_zeilen(zeilen)
        self.tabelle.sortByColumn(0, Qt.SortOrder.AscendingOrder)  # Voreinstellung: nach Nr
        self.leer.setText(leer_text)
        self.setCurrentIndex(1 if zeilen else 0)
        if zeilen:
            self.tabelle.resizeColumnsToContents()

    def zeilenzahl(self) -> int:
        """Anzahl der angezeigten Zeilen."""
        return int(self.modell.rowCount())

    def waehle(self, schluessel: int | None, *, melden: bool = False) -> None:
        """Wählt die Zeile mit ``schluessel`` (``None`` = Auswahl aufheben).

        Parameters
        ----------
        schluessel : int or None
            Schlüssel der Zeile.
        melden : bool
            ``True`` löst auch :attr:`zeile_gewaehlt` aus (sonst nur die Markierung).
        """
        sperre = self.tabelle.selectionModel().blockSignals(not melden)
        try:
            if schluessel is None:
                self.tabelle.clearSelection()
                return
            for r in range(self._proxy.rowCount()):
                quelle = self._proxy.mapToSource(self._proxy.index(r, 0)).row()
                if self.modell.zeile(quelle).schluessel == schluessel:
                    self.tabelle.selectRow(r)
                    self.tabelle.scrollTo(self._proxy.index(r, 0))
                    return
        finally:
            self.tabelle.selectionModel().blockSignals(sperre)

    def gewaehlter_schluessel(self) -> int | None:
        """Schlüssel der gewählten Zeile (``None`` = keine)."""
        zeilen = self.tabelle.selectionModel().selectedRows()
        if not zeilen:
            return None
        return self.modell.zeile(self._proxy.mapToSource(zeilen[0]).row()).schluessel

    def _zeile_gewechselt(self, aktuell: QModelIndex, _vorher: QModelIndex) -> None:
        if aktuell.isValid():
            quelle = self._proxy.mapToSource(aktuell).row()
            self.zeile_gewaehlt.emit(self.modell.zeile(quelle).schluessel)
