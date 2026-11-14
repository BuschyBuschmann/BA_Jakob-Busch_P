"""Chips der geöffneten Messungen in der Dateileiste AA (R-058, P-AUSW2 S5, Brief K1-AUSW2).

Je Messung ein Chip „(A) Dateiname“ mit Entfernen-Knopf (Kreuz). Der aktive Chip trägt einen
Rahmen von 2 px ``C_AKZENT`` **und** das Symbol ✔ samt Wort „aktiv“ im ``accessibleName`` (nie nur
Farbe). Eine ladende Messung zeigt „lädt …“ mit unbestimmtem Balken. Die Chips umbrechen nicht;
reicht der Platz nicht, ist die Zeile scrollbar. Pfeiltasten wechseln zwischen den Chips, Entf
entfernt (die Bestätigung folgt im Reiter), Doppelklick benennt um.

Dieses Modul ist ein dünnes Widget (Abdeckung nur mit ``pytest -m gui``); Kurznamen, aktive
Messung und Speicher liegen Qt-frei in :mod:`.messungen`.
"""

from __future__ import annotations

from collections.abc import Callable

from PySide6.QtCore import QSize, Qt, Signal
from PySide6.QtGui import QKeyEvent, QMouseEvent
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QProgressBar,
    QPushButton,
    QScrollArea,
    QSizePolicy,
    QToolButton,
    QWidget,
)

from ldv_automation.gui import tokens as t
from ldv_automation.gui.messungen import Messung, Messungen, MessungsZustand
from ldv_automation.gui.stil import setze_eigenschaft

__all__ = ["CHIP_HOEHE_PX", "CHIP_TEXT_MAX", "Messungsleiste", "chip_text"]

CHIP_HOEHE_PX = 26
"""Höhe eines Chips (die Zeile bleibt in der Dateileiste, Platz für eine Bildlaufleiste)."""
CHIP_TEXT_MAX = 18
"""Längster Text im Chip (Kurzname und gekürzter Dateiname); der Volltext steht im Tooltip."""
TEXT_LAEDT = "lädt …"


def chip_text(kurzname: str, dateiname: str, *, aktiv: bool, laedt: bool) -> str:
    """Text des Chips: ``(A) Dateiname`` (gekürzt); aktiv mit Haken davor, ladend „lädt …“."""
    kopf = f"({kurzname}) "
    rest = TEXT_LAEDT if laedt else dateiname
    platz = max(CHIP_TEXT_MAX - len(kopf), 4)
    if len(rest) > platz:
        rest = rest[: platz - 1] + "…"
    return (f"{t.symbol('fertig')} " if aktiv else "") + kopf + rest


class _ChipKnopf(QPushButton):
    """Wechselknopf eines Chips: Pfeiltasten, Entf und Doppelklick melden sich der Leiste."""

    pfeil = Signal(int)
    entf = Signal()
    doppelklick = Signal()

    def keyPressEvent(self, event: QKeyEvent) -> None:  # noqa: N802  # Qt-Name
        """Links/rechts wechseln den Chip, Entf entfernt."""
        taste = event.key()
        if taste in (Qt.Key.Key_Left, Qt.Key.Key_Right):
            self.pfeil.emit(-1 if taste == Qt.Key.Key_Left else 1)
        elif taste == Qt.Key.Key_Delete:
            self.entf.emit()
        else:
            super().keyPressEvent(event)

    def mouseDoubleClickEvent(self, event: QMouseEvent) -> None:  # noqa: N802  # Qt-Name
        """Doppelklick: Kurzname ändern."""
        self.doppelklick.emit()
        event.accept()


class _Chip(QFrame):
    """Ein Chip: Wechselknopf, Entfernen-Knopf und bei ladender Messung ein unbestimmter Balken."""

    def __init__(self, messung_id: int, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.messung_id = messung_id
        self.setObjectName(f"chip_messung_{messung_id}")
        self.setProperty("art", "chip")
        self.setFixedHeight(CHIP_HOEHE_PX)
        z = QHBoxLayout(self)
        z.setContentsMargins(2, 0, 2, 0)
        z.setSpacing(2)
        self.knopf = _ChipKnopf()
        self.knopf.setObjectName(f"btn_chip_{messung_id}")
        self.knopf.setProperty("art", "chip")
        self.knopf.setAutoDefault(False)
        self.knopf.setFlat(True)
        self.knopf.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.balken = QProgressBar()
        self.balken.setObjectName(f"balken_chip_{messung_id}")
        self.balken.setRange(0, 0)
        self.balken.setTextVisible(False)
        self.balken.setFixedSize(40, 8)
        self.balken.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.entfernen = QToolButton()
        self.entfernen.setObjectName(f"btn_chip_entfernen_{messung_id}")
        self.entfernen.setText(chr(0xD7))  # Multiplikationszeichen als Kreuz
        self.entfernen.setAutoRaise(True)
        self.entfernen.setProperty("art", "chipx")  # eigene QSS-Regel (kein Innenabstand)
        self.entfernen.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.entfernen.setFixedSize(CHIP_HOEHE_PX - 6, CHIP_HOEHE_PX - 6)
        z.addWidget(self.knopf)
        z.addWidget(self.balken)
        z.addWidget(self.entfernen)

    def setze(
        self,
        messung: Messung,
        *,
        aktiv: bool,
        speicher_mib: float | None,
        gesperrt: bool = False,
    ) -> None:
        """Text, Tooltip, accessibleName und Zustand des Chips.

        ``gesperrt``: Die Messung wird gerade durch „Öffnen …“ ersetzt, Entfernen ist aus.
        """
        laedt = messung.zustand is MessungsZustand.LADEN
        self.knopf.setText(chip_text(messung.kurzname, messung.dateiname, aktiv=aktiv, laedt=laedt))
        zusatz = "" if speicher_mib is None else f"\nSpeicher mindestens {speicher_mib:.0f} MiB"
        status = "lädt" if laedt else "aktiv" if aktiv else "bereit"
        self.knopf.setToolTip(f"{messung.dateiname}\n{messung.pfad}{zusatz}")
        self.knopf.setAccessibleName(f"Messung {messung.kurzname}: {messung.dateiname}, {status}")
        self.knopf.setAccessibleDescription(
            "Klick wechselt die aktive Messung, Doppelklick ändert den Kurznamen, "
            "Entf entfernt die Messung."
        )
        self.knopf.setEnabled(not laedt)
        self.balken.setVisible(laedt)
        self.entfernen.setEnabled(not gesperrt)
        self.entfernen.setToolTip(
            f"Messung {messung.kurzname} wird gerade ersetzt und lässt sich jetzt nicht entfernen"
            if gesperrt
            else f"Messung {messung.kurzname} entfernen"
        )
        self.entfernen.setAccessibleName(f"Messung {messung.kurzname} entfernen")
        setze_eigenschaft(self, "aktiv", "true" if aktiv else "false")
        setze_eigenschaft(self, "laedt", "true" if laedt else "false")


class Messungsleiste(QScrollArea):
    """Horizontal scrollbare Zeile der Chips (nicht umbrechend).

    Signals
    -------
    wechsel : int
        Klick auf einen Chip (Kennung der Messung).
    entfernen : int
        Entfernen-Knopf oder Entf (der Reiter fragt bei betroffenen Serien nach).
    umbenennen : int
        Doppelklick auf den Chip.
    """

    wechsel = Signal(int)
    entfernen = Signal(int)
    umbenennen = Signal(int)

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setObjectName("messungsleiste")
        self.setAccessibleName("Geöffnete Messungen")
        self.setFrameShape(QFrame.Shape.NoFrame)
        self.setWidgetResizable(True)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        self.setFixedHeight(t.HOEHE_DATEILEISTE_PX - 8)
        inhalt = QWidget()
        inhalt.setObjectName("messungsleiste_inhalt")
        self._zeile = QHBoxLayout(inhalt)
        self._zeile.setContentsMargins(0, 0, 0, 0)
        self._zeile.setSpacing(4)
        self._zeile.addStretch(1)
        self.setWidget(inhalt)
        self._chips: dict[int, _Chip] = {}
        self.setVisible(False)

    # --- Anzeige -----------------------------------------------------------------------------

    def setze(
        self,
        messungen: Messungen,
        speicher: Callable[[int], float] | None = None,
        *,
        gesperrt: int | None = None,
    ) -> None:
        """Zeigt die Chips der Messungen (legt fehlende an, entfernt entfallene).

        Reihenfolge der Chips (Anzeige, Pfeiltasten, Tab) ist die der Messungen. ``gesperrt`` ist
        die Kennung der Messung, deren Entfernen-Knopf aus ist.
        """
        vorhanden = {m.id for m in messungen.alle}
        for messung_id in [i for i in self._chips if i not in vorhanden]:
            chip = self._chips.pop(messung_id)
            self._zeile.removeWidget(chip)
            chip.deleteLater()
        aktiv_id = messungen.aktive.id if messungen.aktive is not None else None
        for position, messung in enumerate(messungen.alle):
            vorhandener = self._chips.get(messung.id)
            if vorhandener is None:
                chip = self._neuer_chip(messung.id)
                self._chips[messung.id] = chip
                self._zeile.insertWidget(position, chip)
            else:
                chip = vorhandener
            mib = (
                speicher(messung.id)
                if speicher is not None and messung.zustand is MessungsZustand.BEREIT
                else None
            )
            chip.setze(
                messung,
                aktiv=messung.id == aktiv_id,
                speicher_mib=mib,
                gesperrt=messung.id == gesperrt,
            )
        # Das Dict folgt der Anzeige (Pfeiltasten, Tab-Kette, chip_ids), auch nach „Ersetzen“.
        self._chips = {m.id: self._chips[m.id] for m in messungen.alle}
        self.setVisible(bool(self._chips))
        inhalt = self.widget()
        assert inhalt is not None
        inhalt.adjustSize()
        self.updateGeometry()
        if aktiv_id in self._chips:
            self.ensureWidgetVisible(self._chips[aktiv_id])

    def _neuer_chip(self, messung_id: int) -> _Chip:
        chip = _Chip(messung_id)
        chip.knopf.clicked.connect(lambda _c=False, i=messung_id: self.wechsel.emit(i))
        chip.knopf.pfeil.connect(lambda richtung, i=messung_id: self._pfeil(i, richtung))
        chip.knopf.entf.connect(lambda i=messung_id: self.entfernen.emit(i))
        chip.knopf.doppelklick.connect(lambda i=messung_id: self.umbenennen.emit(i))
        chip.entfernen.clicked.connect(lambda _c=False, i=messung_id: self.entfernen.emit(i))
        return chip

    def _pfeil(self, messung_id: int, richtung: int) -> None:
        """Fokus auf den Nachbarchip (Pfeil links/rechts); wechseln: Klick oder Leertaste."""
        ids = list(self._chips)
        ziel = ids.index(messung_id) + richtung
        if 0 <= ziel < len(ids):
            chip = self._chips[ids[ziel]]
            chip.knopf.setFocus(Qt.FocusReason.TabFocusReason)
            self.ensureWidgetVisible(chip)

    # --- Zugriff -----------------------------------------------------------------------------

    def chip(self, messung_id: int) -> QFrame | None:
        """Der Chip der Messung (``None``, wenn es ihn nicht gibt)."""
        return self._chips.get(messung_id)

    def chip_knopf(self, messung_id: int) -> QPushButton | None:
        """Wechselknopf des Chips."""
        chip = self._chips.get(messung_id)
        return chip.knopf if chip is not None else None

    def chip_ids(self) -> list[int]:
        """Kennungen der Chips in Anzeigereihenfolge."""
        return list(self._chips)

    def tab_kette(self) -> list[QWidget]:
        """Bedienbare Teile in Tab-Reihenfolge (Chip, dann sein Entfernen-Knopf)."""
        kette: list[QWidget] = []
        for chip in self._chips.values():
            kette += [chip.knopf, chip.entfernen]
        return kette

    def sizeHint(self) -> QSize:  # noqa: N802  # Qt-Name
        """Breite aller Chips; reicht der Platz nicht, scrollt die Zeile."""
        inhalt = self.widget()
        breite = inhalt.sizeHint().width() if inhalt is not None and self._chips else 0
        return QSize(breite + 4, self.height())

    def minimumSizeHint(self) -> QSize:  # noqa: N802  # Qt-Name
        """Mindestens ein Chip-Ausschnitt; darüber hinaus scrollt die Zeile."""
        return QSize(120, self.height())
