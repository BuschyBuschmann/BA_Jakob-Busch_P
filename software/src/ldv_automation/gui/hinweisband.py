"""Hinweisband (Zone C, Brief P3, Abschnitt 3.5): genau ein Hinweis, Höhe immer reserviert."""

from __future__ import annotations

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import QFrame, QHBoxLayout, QLabel, QPushButton, QSizePolicy, QWidget

from ldv_automation.gui import tokens as t
from ldv_automation.gui.anzeige import BandKnopf, Hinweis
from ldv_automation.gui.stil import setze_eigenschaft


class Hinweisband(QFrame):
    """Zeigt einen :class:`~.anzeige.Hinweis` mit Aktionsknöpfen.

    Die Eigenschaft ``fall`` trägt die Nummer aus Tabelle 3.5 (leer ohne Hinweis). Der
    Fokus wird nie automatisch in das Band verschoben.

    Signale
    -------
    knopf_geklickt(str)
        Schlüssel des geklickten Knopfs (``trennen``, ``wiederholen``, ``ueberspringen``,
        ``abbrechen``, ``bestaetigen``, ``fortsetzen``, ``ordner``, ``schliessen``).
    """

    knopf_geklickt = Signal(str)

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setObjectName("hinweisband")
        self.setAccessibleName("Hinweis")
        self.setFixedHeight(t.HOEHE_HINWEISBAND_PX)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.setProperty("fall", "")
        self.setProperty("stil", "leer")
        layout = QHBoxLayout(self)
        layout.setContentsMargins(12, 4, 12, 4)
        self.text = QLabel()
        self.text.setObjectName("hinweis_text")
        self.text.setSizePolicy(QSizePolicy.Policy.Ignored, QSizePolicy.Policy.Preferred)
        layout.addWidget(self.text, 1)
        self._knopf_layout = QHBoxLayout()
        layout.addLayout(self._knopf_layout)
        self._knoepfe: tuple[BandKnopf, ...] = ()
        self._hinweis: Hinweis | None = None

    @property
    def hinweis(self) -> Hinweis | None:
        """Der angezeigte Hinweis oder ``None``."""
        return self._hinweis

    def knopf(self, schluessel: str) -> QPushButton | None:
        """Knopf ``btn_band_<schluessel>`` oder ``None``."""
        return self.findChild(QPushButton, f"btn_band_{schluessel}")

    def zeige(self, hinweis: Hinweis | None) -> bool:
        """Zeigt ``hinweis``; gibt ``True`` zurück, wenn sich der Fall geändert hat."""
        alt = self._hinweis
        if hinweis == alt:
            return False
        self._hinweis = hinweis
        text = hinweis.text if hinweis is not None else ""
        self.text.setText(text)
        self.text.setToolTip(text)
        self.setAccessibleDescription(text)
        setze_eigenschaft(self, "stil", hinweis.stil if hinweis is not None else "leer")
        self.setProperty("fall", hinweis.fall if hinweis is not None else "")
        knoepfe = hinweis.knoepfe if hinweis is not None else ()
        if knoepfe != self._knoepfe:
            self._baue_knoepfe(knoepfe)
        return (alt.fall if alt else None) != (hinweis.fall if hinweis else None)

    def _baue_knoepfe(self, knoepfe: tuple[BandKnopf, ...]) -> None:
        while self._knopf_layout.count():
            item = self._knopf_layout.takeAt(0)
            w = item.widget() if item is not None else None
            if w is not None:
                w.hide()
                w.setParent(None)
                w.deleteLater()
        for k in knoepfe:
            b = QPushButton(k.text, self)
            b.setObjectName(f"btn_band_{k.schluessel}")
            b.setAutoDefault(False)
            b.setDefault(False)
            b.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
            if k.primaer:
                b.setProperty("art", "primaer_gefuellt")
            elif k.schluessel == "abbrechen":
                b.setProperty("art", "gefahr")
            if k.tooltip:
                b.setToolTip(k.tooltip)
            b.clicked.connect(lambda _c=False, s=k.schluessel: self.knopf_geklickt.emit(s))
            self._knopf_layout.addWidget(b)
        self._knoepfe = knoepfe
