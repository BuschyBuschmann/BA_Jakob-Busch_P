"""Dialog „Werte als Tabelle“ der Animation (R-071, Plan P-AUSW3 AN9, UI-26).

Die Tabelle ist der Ersatz für das Bild: Sie nennt je Messpunkt Ruhelage, Status und die
momentane Auslenkung bei dem Winkel, bei dem der Dialog geöffnet wurde. Dünnes Widgetmodul
(Abdeckung nur mit ``pytest -m gui``); der Inhalt entsteht Qt-frei in
:func:`~ldv_automation.gui.animation_steuerung.tabelle_auslenkungen`.
"""

from __future__ import annotations

from PySide6.QtCore import Qt
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
from ldv_automation.gui.animation_steuerung import WerteTabelle

__all__ = ["WerteTabelleDialog"]


class WerteTabelleDialog(QDialog):
    """Schreibgeschützte Tabelle der Auslenkungen je Messpunkt (Esc oder „Schließen“ beendet).

    Parameters
    ----------
    tabelle : WerteTabelle
        Inhalt (Titel, Spaltenköpfe, Zeilen).
    parent : QWidget, optional
        Elternwidget.
    """

    def __init__(self, tabelle: WerteTabelle, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setObjectName("werte_tabelle_dialog")
        self.setWindowTitle("Werte als Tabelle")
        self.setModal(True)
        self.resize(960, 420)
        layout = QVBoxLayout(self)
        self.lbl_titel = QLabel(tabelle.titel)
        self.lbl_titel.setObjectName("lbl_werte_titel")
        self.lbl_titel.setWordWrap(True)
        layout.addWidget(self.lbl_titel)
        self.tabelle = QTableWidget(len(tabelle.zeilen), len(tabelle.spalten))
        self.tabelle.setObjectName("tabelle_werte")
        self.tabelle.setAccessibleName("Auslenkung je Messpunkt")
        self.tabelle.setAccessibleDescription(tabelle.titel)
        self.tabelle.setHorizontalHeaderLabels(list(tabelle.spalten))
        self.tabelle.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.tabelle.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.tabelle.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.tabelle.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.tabelle.verticalHeader().setVisible(False)
        self.tabelle.verticalHeader().setDefaultSectionSize(t.ZEILENHOEHE_TABELLE_PX)
        self.tabelle.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.ResizeToContents
        )
        rechts = Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter
        for i, zeile in enumerate(tabelle.zeilen):
            for j, text in enumerate(zeile):
                item = QTableWidgetItem(text)
                if j >= 2:  # Zahlenspalten rechtsbündig
                    item.setTextAlignment(rechts)
                self.tabelle.setItem(i, j, item)
        layout.addWidget(self.tabelle, 1)
        tasten = QDialogButtonBox(QDialogButtonBox.StandardButton.Close)
        schliessen = tasten.button(QDialogButtonBox.StandardButton.Close)
        schliessen.setText("Schließen")
        schliessen.setAutoDefault(False)
        tasten.rejected.connect(self.reject)
        layout.addWidget(tasten)
