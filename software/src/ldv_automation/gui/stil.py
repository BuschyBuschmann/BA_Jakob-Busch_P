"""Qt-Stil der Oberfläche: Fusion, Palette, knappes QSS und Schriften (Brief P3, Abschnitt 2)."""

from __future__ import annotations

from PySide6.QtGui import QColor, QFont, QPalette
from PySide6.QtWidgets import QApplication, QWidget

from ldv_automation.gui import tokens as t


def schrift(pt: int = t.SCHRIFT_PT, *, fett: bool = False, mono: bool = False) -> QFont:
    """Schrift mit Familienliste und Rückfall (Segoe UI/Arial bzw. Consolas/Courier New)."""
    f = QFont()
    f.setFamilies(list(t.SCHRIFT_FAMILIEN_MONO if mono else t.SCHRIFT_FAMILIEN))
    if mono:
        f.setStyleHint(QFont.StyleHint.Monospace)
    f.setPointSize(pt)
    f.setBold(fett)
    return f


def palette() -> QPalette:
    """Helle Palette aus den Tokens."""
    p = QPalette()
    p.setColor(QPalette.ColorRole.Window, QColor(t.C_BG))
    p.setColor(QPalette.ColorRole.WindowText, QColor(t.C_TEXT))
    p.setColor(QPalette.ColorRole.Base, QColor(t.C_FLAECHE))
    p.setColor(QPalette.ColorRole.AlternateBase, QColor(t.C_BG))
    p.setColor(QPalette.ColorRole.Text, QColor(t.C_TEXT))
    p.setColor(QPalette.ColorRole.Button, QColor(t.C_FLAECHE))
    p.setColor(QPalette.ColorRole.ButtonText, QColor(t.C_TEXT))
    p.setColor(QPalette.ColorRole.Highlight, QColor(t.C_AUSWAHL_BG))
    p.setColor(QPalette.ColorRole.HighlightedText, QColor(t.C_TEXT))
    p.setColor(QPalette.ColorRole.ToolTipBase, QColor(t.C_FLAECHE))
    p.setColor(QPalette.ColorRole.ToolTipText, QColor(t.C_TEXT))
    p.setColor(QPalette.ColorRole.PlaceholderText, QColor(t.C_TEXT_GEDAEMPFT))
    for rolle in (
        QPalette.ColorRole.WindowText,
        QPalette.ColorRole.Text,
        QPalette.ColorRole.ButtonText,
    ):
        p.setColor(QPalette.ColorGroup.Disabled, rolle, QColor(t.C_DEAKTIVIERT_TEXT))
    p.setColor(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Button, QColor(t.C_DEAKTIVIERT_BG))
    p.setColor(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Base, QColor(t.C_DEAKTIVIERT_BG))
    return p


QSS = f"""
QWidget {{ color: {t.C_TEXT}; }}
QMainWindow, QDialog {{ background: {t.C_BG}; }}
QPushButton, QToolButton {{
    min-height: {t.KNOPF_MIN_HOEHE_PX - 4}px; padding: 0 16px;
    border: 1px solid {t.C_RAND_EINGABE}; border-radius: 0; background: {t.C_FLAECHE};
}}
QPushButton:disabled, QToolButton:disabled {{
    color: {t.C_DEAKTIVIERT_TEXT}; background: {t.C_DEAKTIVIERT_BG};
    border-color: {t.C_LINIE};
}}
QPushButton[art="primaer"], QToolButton[art="primaer"] {{
    border: 2px solid {t.C_AKZENT}; color: {t.C_AKZENT}; font-weight: bold;
}}
QPushButton[art="primaer_gefuellt"] {{
    border: 2px solid {t.C_AKZENT}; background: {t.C_AKZENT}; color: {t.C_STATUSZEILE_TEXT};
    font-weight: bold;
}}
QPushButton[art="gefahr"], QToolButton[art="gefahr"] {{
    border: 2px solid {t.C_FEHLER}; color: {t.C_FEHLER};
}}
QPushButton[art="primaer"]:disabled, QToolButton[art="primaer"]:disabled,
QPushButton[art="gefahr"]:disabled, QToolButton[art="gefahr"]:disabled {{
    color: {t.C_DEAKTIVIERT_TEXT}; border-color: {t.C_LINIE};
}}
QLineEdit, QSpinBox, QComboBox, QPlainTextEdit {{
    min-height: {t.EINGABE_HOEHE_PX - 4}px; border: 1px solid {t.C_RAND_EINGABE};
    background: {t.C_FLAECHE};
}}
QLineEdit:disabled, QSpinBox:disabled, QComboBox:disabled, QPlainTextEdit:disabled {{
    color: {t.C_DEAKTIVIERT_TEXT}; background: {t.C_DEAKTIVIERT_BG};
}}
*:focus {{ outline: none; }}
QPushButton:focus, QToolButton:focus, QLineEdit:focus, QSpinBox:focus, QComboBox:focus,
QPlainTextEdit:focus, QCheckBox:focus, QTableWidget:focus, QListWidget:focus,
QRadioButton:focus {{
    border: 2px solid {t.C_AKZENT};
}}
QTabBar::tab {{
    min-height: {t.KNOPF_MIN_HOEHE_PX - 8}px; padding: 2px 20px; background: {t.C_LEISTE};
    border: 1px solid {t.C_LINIE}; border-bottom: none;
}}
QTabBar::tab:selected {{ background: {t.C_FLAECHE}; font-weight: bold; }}
QTabBar:focus {{ border: 2px solid {t.C_AKZENT}; }}
QTabWidget::pane {{ border: none; border-top: 1px solid {t.C_LINIE}; }}
QPushButton[art="segment"] {{ padding: 0 12px; min-height: {t.KNOPF_MIN_HOEHE_PX - 12}px; }}
QPushButton[art="segment"]:checked {{
    border: 2px solid {t.C_AKZENT}; background: {t.C_AKTIV_BG}; font-weight: bold;
}}
QPushButton[art="segment"]:disabled:checked {{ border-color: {t.C_LINIE}; }}
QListWidget {{
    background: {t.C_FLAECHE}; border: 1px solid {t.C_LINIE};
    selection-background-color: {t.C_AUSWAHL_BG}; selection-color: {t.C_TEXT};
}}
QListWidget:disabled {{ background: {t.C_DEAKTIVIERT_BG}; color: {t.C_DEAKTIVIERT_TEXT}; }}
QCheckBox:disabled, QRadioButton:disabled {{ color: {t.C_DEAKTIVIERT_TEXT}; }}
QFrame#dateileiste, QFrame#parameterzeile, QFrame#ansichtswahl, QFrame#fusszeile {{
    background: {t.C_LEISTE};
}}
QFrame#parameterzeile {{ border-bottom: 1px solid {t.C_LINIE}; }}
QFrame#fusszeile {{ border-top: 1px solid {t.C_LINIE}; }}
QFrame#band_fehler {{ background: {t.C_FEHLER_BG}; border: 2px solid {t.C_FEHLER}; }}
QFrame#band_fehler QLabel {{ color: {t.C_FEHLER}; }}
QFrame#plot_rahmen {{ border: 2px solid transparent; background: {t.C_PLOT_FLAECHE}; }}
QFrame#plot_rahmen[fokus="true"] {{ border: 2px solid {t.C_AKZENT}; }}
QTableWidget {{
    background: {t.C_FLAECHE}; gridline-color: {t.C_LINIE_ZEILE};
    border: 1px solid {t.C_LINIE};
    selection-background-color: {t.C_AUSWAHL_BG}; selection-color: {t.C_TEXT};
}}
QHeaderView::section {{
    background: {t.C_LEISTE}; border: none; border-bottom: 1px solid {t.C_LINIE};
    padding: 0 6px; font-weight: bold;
}}
QFrame#statuszeile {{ background: {t.C_STATUSZEILE}; }}
QFrame#statuszeile QLabel {{ color: {t.C_STATUSZEILE_TEXT}; }}
QFrame#statuszeile QPushButton {{
    background: {t.C_STATUSZEILE}; color: {t.C_STATUSZEILE_TEXT};
    border: 1px solid {t.C_STATUSZEILE_TEXT};
}}
QFrame#statuszeile QPushButton:disabled {{
    color: {t.C_DEAKTIVIERT_TEXT}; border-color: {t.C_DEAKTIVIERT_TEXT};
}}
QToolButton#btn_betriebsart {{
    background: {t.C_STATUSZEILE}; color: {t.C_STATUSZEILE_TEXT};
    border: 1px solid {t.C_STATUSZEILE_TEXT}; font-weight: bold;
}}
QToolButton#btn_betriebsart[messen="true"] {{
    background: {t.C_STATUSZEILE_TEXT}; color: {t.C_STATUSZEILE};
}}
QFrame#werkzeugleiste {{ background: {t.C_LEISTE}; border-bottom: 1px solid {t.C_LINIE}; }}
QFrame#hinweisband[stil="neutral"] {{ background: {t.C_LEISTE}; }}
QFrame#hinweisband[stil="warn"] {{ background: {t.C_WARN_BG}; }}
QFrame#hinweisband[stil="warn_rand"] {{
    background: {t.C_WARN_BG}; border: 2px solid {t.C_WARN_RAND};
}}
QFrame#hinweisband[stil="fehler"] {{
    background: {t.C_FEHLER_BG}; border: 2px solid {t.C_FEHLER};
}}
QLabel[art="fehler"] {{ color: {t.C_FEHLER}; }}
QLabel[art="gedaempft"] {{ color: {t.C_TEXT_GEDAEMPFT}; }}
QProgressBar {{ border: 1px solid {t.C_LINIE}; background: {t.C_FLAECHE}; }}
QProgressBar::chunk {{ background: {t.C_AKZENT}; }}
QPlainTextEdit#protokoll {{ background: {t.C_FLAECHE}; }}
"""
"""Knappes Stylesheet: nur Farben, Rahmen, Fokus und Mindesthöhen (Brief Abschnitt 2)."""


def wende_an(app: QApplication) -> None:
    """Setzt Stil ``Fusion``, Palette, Schrift und Stylesheet für die Anwendung."""
    app.setStyle("Fusion")
    app.setPalette(palette())
    app.setFont(schrift())
    app.setStyleSheet(QSS)


def setze_eigenschaft(widget: QWidget, name: str, wert: object) -> None:
    """Setzt eine dynamische Qt-Eigenschaft und erneuert das Stylesheet des Widgets."""
    if widget.property(name) == wert:
        return
    widget.setProperty(name, wert)
    stil = widget.style()
    stil.unpolish(widget)
    stil.polish(widget)
    widget.update()
