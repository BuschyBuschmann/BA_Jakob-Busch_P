"""Dialoge der Oberfläche (Brief P3, Abschnitte 3.7 bis 3.13).

Die Dialoge werden hier nur gebaut; ausgeführt (``exec``) werden sie im Hauptfenster über
eine austauschbare Methode, damit Tests sie ohne modale Schleife bedienen können. Kein
Dialog der Gefahr-Klasse hat den Gefahr-Knopf als Standard.
"""

from __future__ import annotations

from collections.abc import Callable, Mapping, Sequence
from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QAbstractButton,
    QDialog,
    QDialogButtonBox,
    QFileDialog,
    QFormLayout,
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QSpinBox,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

from ldv_automation.gui import tokens as t
from ldv_automation.gui.anzeige import (
    VoraussetzungZeile,
    diagnose_text,
    generator_warnung,
    geraet_generator_text,
    konfiguration_text,
    messpunkte_text,
    start_anzahl_text,
    start_tooltip,
    start_zeile,
)
from ldv_automation.gui.stil import schrift
from ldv_automation.sitzung import GeraeteDiagnose, GeraeteInfo, GeraeteStand, StartVorschau

BESTAETIGUNGSWORT = "MESSEN"
"""Text, der im Dialog „Durchgang starten“ exakt einzutippen ist (Brief 3.9)."""

EINSTELLUNGEN_MIN_BREITE_PX = 480
"""Mindestbreite des Dialogs „Einstellungen“ (K-U5b: Pfade und Meldungen lesbar)."""

LIMIT_MAX_S = 864_000
"""Obergrenze des Felds Standard-Zeitlimit (10 Tage); nur Eingabegrenze des Felds."""


def _titel(text: str) -> QLabel:
    label = QLabel(text)
    label.setFont(schrift(t.SCHRIFT_PT_TITEL, fett=True))
    label.setWordWrap(True)
    return label


def frage(
    parent: QWidget | None,
    titel: str,
    text: str,
    ja_text: str,
    nein_text: str,
    *,
    ja_gefahr: bool = False,
    symbol: QMessageBox.Icon = QMessageBox.Icon.Question,
) -> tuple[QMessageBox, QAbstractButton]:
    """Ja/Nein-Frage mit sicherem Standardknopf (``nein_text``; auch Esc).

    Returns
    -------
    tuple
        ``(box, ja_knopf)``; nach ``exec`` gilt die Frage als bejaht, wenn
        ``box.clickedButton() is ja_knopf``.
    """
    box = QMessageBox(parent)
    box.setIcon(symbol)
    box.setWindowTitle(titel)
    box.setText(text)
    rolle = (
        QMessageBox.ButtonRole.DestructiveRole if ja_gefahr else QMessageBox.ButtonRole.AcceptRole
    )
    ja = box.addButton(ja_text, rolle)
    ja.setObjectName("btn_dialog_ja")
    nein = box.addButton(nein_text, QMessageBox.ButtonRole.RejectRole)
    nein.setObjectName("btn_dialog_nein")
    box.setDefaultButton(nein)
    box.setEscapeButton(nein)
    if ja_gefahr:
        ja.setProperty("art", "gefahr")
    return box, ja


def abbrechen_dialog(
    parent: QWidget | None, *, messung_laeuft: bool
) -> tuple[QMessageBox, QAbstractButton]:
    """Dialog 3.12 „Durchgang abbrechen?“ mit Standard und Fokus auf dem sicheren Knopf."""
    if messung_laeuft:
        text = (
            "Die laufende Messung wird sofort gestoppt. Bereits gemessene Punkte bleiben in der "
            "Datei. Nicht gestartete Messungen bleiben wartend."
        )
        sicher = "Weiter messen"
    else:
        text = "Der Durchgang wird beendet. Nicht gestartete Messungen bleiben wartend."
        sicher = "Zurück"
    box, ja = frage(
        parent,
        "Durchgang abbrechen?",
        text,
        "Durchgang abbrechen",
        sicher,
        ja_gefahr=True,
        symbol=QMessageBox.Icon.Warning,
    )
    box.setObjectName("dialog_abbrechen")
    return box, ja


def trockenlauf_dialog(parent: QWidget | None) -> tuple[QMessageBox, QAbstractButton]:
    """Hinweisdialog vor einem Trockenlauf (Brief 3.9)."""
    box, ja = frage(
        parent,
        "Trockenlauf starten",
        "Ein Trockenlauf ändert die aktuellen PSV-Einstellungen. Es wird nicht gescannt.",
        "Trockenlauf starten",
        "Abbrechen",
        symbol=QMessageBox.Icon.Information,
    )
    box.setObjectName("dialog_trockenlauf")
    return box, ja


class MessenFreischaltenDialog(QDialog):
    """Dialog 3.8 „Messen freischalten“; die Voraussetzungen kommen aus der Sitzung."""

    def __init__(self, zeilen: Sequence[VoraussetzungZeile], parent: QWidget | None = None):
        super().__init__(parent)
        self.setObjectName("dialog_freischalten")
        self.setWindowTitle("Messen freischalten")
        self.setModal(True)
        layout = QVBoxLayout(self)
        layout.addWidget(_titel("Messen freischalten"))
        einleitung = QLabel(
            "Damit werden echte Messungen an der PSV möglich. Jeder Durchgang braucht danach "
            "eine eigene Bestätigung."
        )
        einleitung.setWordWrap(True)
        layout.addWidget(einleitung)
        for i, z in enumerate(zeilen):
            zeichen = t.symbol("fertig") if z.erfuellt else t.symbol("fehler")
            zeile = QLabel(f"{zeichen} {z.text}")
            zeile.setObjectName(f"voraussetzung_{i}")
            zeile.setToolTip(z.detail)
            zeile.setProperty("art", "" if z.erfuellt else "fehler")
            layout.addWidget(zeile)
            if not z.erfuellt:
                abhilfe = QLabel(f"{z.detail}. {z.abhilfe}")
                abhilfe.setObjectName(f"abhilfe_{i}")
                abhilfe.setProperty("art", "gedaempft")
                abhilfe.setWordWrap(True)
                abhilfe.setContentsMargins(20, 0, 0, 0)
                layout.addWidget(abhilfe)
        knoepfe = QDialogButtonBox()
        self.btn_abbrechen = knoepfe.addButton("Abbrechen", QDialogButtonBox.ButtonRole.RejectRole)
        self.btn_abbrechen.setObjectName("btn_freischalten_abbrechen")
        self.btn_freischalten = knoepfe.addButton(
            "Freischalten", QDialogButtonBox.ButtonRole.AcceptRole
        )
        self.btn_freischalten.setObjectName("btn_freischalten")
        self.btn_freischalten.setAutoDefault(False)
        self.btn_abbrechen.setDefault(True)
        alle = bool(zeilen) and all(z.erfuellt for z in zeilen)
        self.btn_freischalten.setEnabled(alle)
        if not alle:
            self.btn_freischalten.setToolTip("Nicht alle Voraussetzungen sind erfüllt.")
        knoepfe.accepted.connect(self.accept)
        knoepfe.rejected.connect(self.reject)
        layout.addWidget(knoepfe)
        self.btn_abbrechen.setFocus()


class DurchgangStartenDialog(QDialog):
    """Dialog 3.9 „Durchgang starten: echte Messung“ (Schnappschuss zum Startzeitpunkt).

    Alle Angaben kommen aus dem Zustandsbild der Sitzung (``start_vorschau`` je wartender
    Messung, ``geraete_stand``). Messpunkte und Generator sind nur bekannt, wenn die ``.set``
    in dieser Sitzung geladen und danach gelesen wurde; sonst steht „unbekannt“. Die rote
    Warnzeile erscheint, wenn ein Generator aktiv oder sein Zustand unbekannt ist.
    Abweichung vom Brief: zusätzliche Tabellenspalte „Generator“ je Messung.
    """

    def __init__(
        self,
        vorschau: Sequence[StartVorschau],
        geraet: GeraeteStand | None = None,
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)
        self.setObjectName("dialog_durchgang_starten")
        self.setWindowTitle("Durchgang starten: echte Messung")
        self.setModal(True)
        self.resize(860, 480)
        layout = QVBoxLayout(self)
        layout.addWidget(_titel("Durchgang starten: echte Messung"))
        anzahl = QLabel(start_anzahl_text(vorschau))
        anzahl.setObjectName("start_anzahl")
        anzahl.setWordWrap(True)
        layout.addWidget(anzahl)
        spalten = ["Nr", "Einstellungsdatei", "Zieldatei", "Messpunkte", "Generator"]
        tabelle = QTableWidget(len(vorschau), len(spalten))
        tabelle.setObjectName("start_tabelle")
        tabelle.setHorizontalHeaderLabels(spalten)
        tabelle.verticalHeader().setVisible(False)
        tabelle.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        kopf = tabelle.horizontalHeader()
        for nr, modus in enumerate(
            (
                QHeaderView.ResizeMode.ResizeToContents,
                QHeaderView.ResizeMode.Stretch,
                QHeaderView.ResizeMode.Stretch,
                QHeaderView.ResizeMode.ResizeToContents,
                QHeaderView.ResizeMode.ResizeToContents,
            )
        ):
            kopf.setSectionResizeMode(nr, modus)
        tabelle.setWordWrap(True)
        tabelle.setTextElideMode(Qt.TextElideMode.ElideNone)
        for r, v in enumerate(vorschau):
            for spalte, wert in enumerate(start_zeile(v)):
                item = QTableWidgetItem(wert)
                item.setToolTip(start_tooltip(v, spalte))
                tabelle.setItem(r, spalte, item)
        tabelle.resizeRowsToContents()
        self.tabelle = tabelle
        layout.addWidget(tabelle, 1)
        generator = QLabel(geraet_generator_text(geraet, startdialog=True))
        generator.setObjectName("start_generator")
        generator.setWordWrap(True)
        layout.addWidget(generator)
        warnung = QLabel(generator_warnung(vorschau) or "")
        warnung.setObjectName("start_generator_warnung")
        warnung.setProperty("art", "fehler")
        warnung.setWordWrap(True)
        warnung.setVisible(bool(warnung.text()))
        self.warnung = warnung
        layout.addWidget(warnung)
        eingabe_label = QLabel(f"Zur Bestätigung {BESTAETIGUNGSWORT} eintippen")
        self.eingabe = QLineEdit()
        self.eingabe.setObjectName("eingabe_messen")
        eingabe_label.setBuddy(self.eingabe)
        layout.addWidget(eingabe_label)
        layout.addWidget(self.eingabe)
        knoepfe = QDialogButtonBox()
        self.btn_abbrechen = knoepfe.addButton("Abbrechen", QDialogButtonBox.ButtonRole.RejectRole)
        self.btn_abbrechen.setObjectName("btn_start_abbrechen")
        self.btn_starten = knoepfe.addButton(
            "Messung starten", QDialogButtonBox.ButtonRole.AcceptRole
        )
        self.btn_starten.setObjectName("btn_messung_starten")
        self.btn_starten.setAutoDefault(False)
        self.btn_starten.setEnabled(False)
        self.btn_abbrechen.setDefault(True)
        knoepfe.accepted.connect(self._annehmen)
        knoepfe.rejected.connect(self.reject)
        layout.addWidget(knoepfe)
        self.eingabe.textChanged.connect(self._pruefe)
        self.btn_abbrechen.setFocus()

    def _pruefe(self, text: str) -> None:
        self.btn_starten.setEnabled(text == BESTAETIGUNGSWORT)

    def _annehmen(self) -> None:
        if self.eingabe.text() == BESTAETIGUNGSWORT:
            self.accept()


class GeraetDialog(QDialog):
    """Dialog 3.10 „Gerät“: schreibgeschützte Anzeige aus dem Zustandsbild."""

    def __init__(
        self,
        info: GeraeteInfo | None,
        parent: QWidget | None = None,
        *,
        stand: GeraeteStand | None = None,
        diagnose: GeraeteDiagnose | None = None,
        konfiguration: Mapping[str, object] | None = None,
    ) -> None:
        super().__init__(parent)
        self.setObjectName("dialog_geraet")
        self.setWindowTitle("Gerät")
        layout = QVBoxLayout(self)
        layout.addWidget(_titel("Gerät"))
        if info is None:
            nicht = QLabel("Nicht verbunden.")
            nicht.setObjectName("geraet_nicht_verbunden")
            layout.addWidget(nicht)
        else:
            form = QFormLayout()
            hardware = "\n".join(f"{k}: {v}" for k, v in sorted(info.hardware.items())) or "–"
            for name, wert, objekt in (
                ("PSV-Version", info.psv_version, "geraet_version"),
                (
                    "Modus",
                    "Erfassung (Acquisition)" if info.erfassungsmodus else "nicht Erfassung",
                    "geraet_modus",
                ),
                ("Gerätezustand (State)", info.zustand.value, "geraet_state"),
                (
                    "Meldungen unterdrückt",
                    "ja" if info.meldungen_unterdrueckt else "nein",
                    "geraet_suppress",
                ),
                ("Hardware", hardware, "geraet_hardware"),
                ("Lademaske", info.lademaske or "–", "geraet_lademaske"),
                ("Messpunkte", messpunkte_text(stand), "geraet_messpunkte"),
                ("Generator", geraet_generator_text(stand), "geraet_generator"),
                ("Aufrufprotokoll", diagnose_text(diagnose), "geraet_aufrufe"),
                ("Konfiguration", konfiguration_text(konfiguration), "geraet_konfiguration"),
            ):
                label = QLabel(wert)
                label.setObjectName(objekt)
                label.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
                label.setWordWrap(True)
                form.addRow(name, label)
            layout.addLayout(form)
        knoepfe = QDialogButtonBox(QDialogButtonBox.StandardButton.Close)
        schliessen = knoepfe.button(QDialogButtonBox.StandardButton.Close)
        schliessen.setText("Schließen")
        schliessen.setObjectName("btn_geraet_schliessen")
        knoepfe.rejected.connect(self.reject)
        layout.addWidget(knoepfe)


Uebernahme = Callable[[Path, int], tuple[str | None, str | None]]
"""Setzt Ordner und Standard-Zeitlimit (s) in der Sitzung; liefert je Feld Fehlertext/None."""


class EinstellungenDialog(QDialog):
    """Dialog 3.11 „Einstellungen“: Messdaten-Ordner und Standard-Zeitlimit.

    Parameters
    ----------
    ordner : str or None
        Aktueller Messdaten-Ordner.
    zeitlimit_s : float
        Aktuelles Standard-Zeitlimit der Sitzung in s.
    uebernehmen : callable
        Setzt Ordner und Zeitlimit in der Sitzung; gibt ``(fehler_ordner, fehler_limit)``
        zurück (je ``None`` bei Erfolg). Die Prüfung des Ordners macht die Sitzung.
    probleme : sequence of str
        Meldungen der Sitzung zum aktuellen Ordner; sie stehen beim Öffnen unter dem Feld.
    """

    def __init__(
        self,
        ordner: str | None,
        zeitlimit_s: float,
        uebernehmen: Uebernahme,
        parent: QWidget | None = None,
        *,
        probleme: Sequence[str] = (),
    ) -> None:
        super().__init__(parent)
        self.setObjectName("dialog_einstellungen")
        self.setWindowTitle("Einstellungen")
        self.setMinimumWidth(EINSTELLUNGEN_MIN_BREITE_PX)
        self._uebernehmen = uebernehmen
        self.ordner_waehlen: Callable[[str], str | None] = self._ordner_dialog
        layout = QVBoxLayout(self)
        layout.addWidget(_titel("Einstellungen"))
        form = QFormLayout()
        form.setRowWrapPolicy(QFormLayout.RowWrapPolicy.WrapAllRows)
        self.ordner = QLineEdit(ordner or "")
        self.ordner.setObjectName("einstellung_ordner")
        self.ordner.setFont(schrift(t.SCHRIFT_PT_MONO, mono=True))
        waehlen = QPushButton("Wählen …")
        waehlen.setObjectName("btn_ordner_waehlen")
        waehlen.clicked.connect(self._waehle)
        zeile = QWidget()
        zeile_layout = QHBoxLayout(zeile)
        zeile_layout.setContentsMargins(0, 0, 0, 0)
        zeile_layout.addWidget(self.ordner, 1)
        zeile_layout.addWidget(waehlen)
        self.fehler = QLabel()
        self.fehler.setObjectName("einstellung_ordner_fehler")
        self.fehler.setProperty("art", "fehler")
        self.fehler.setWordWrap(True)
        self.fehler.hide()
        behaelter = QWidget()
        b_layout = QVBoxLayout(behaelter)
        b_layout.setContentsMargins(0, 0, 0, 0)
        b_layout.addWidget(zeile)
        b_layout.addWidget(self.fehler)
        label_ordner = QLabel("&Messdaten-Ordner")
        label_ordner.setBuddy(self.ordner)
        form.addRow(label_ordner, behaelter)
        self.limit = QSpinBox()
        self.limit.setObjectName("einstellung_limit")
        self.limit.setRange(1, LIMIT_MAX_S)
        self.limit.setValue(min(max(round(zeitlimit_s), 1), LIMIT_MAX_S))
        self.limit.setSuffix(" s")
        self.limit.setToolTip("Gilt für Messungen ohne eigenes Limit, ab dem nächsten Durchgang.")
        self.limit_fehler = QLabel()
        self.limit_fehler.setObjectName("einstellung_limit_fehler")
        self.limit_fehler.setProperty("art", "fehler")
        self.limit_fehler.setWordWrap(True)
        self.limit_fehler.hide()
        limit_behaelter = QWidget()
        l_layout = QVBoxLayout(limit_behaelter)
        l_layout.setContentsMargins(0, 0, 0, 0)
        l_layout.addWidget(self.limit)
        l_layout.addWidget(self.limit_fehler)
        label_limit = QLabel("Standard-&Zeitlimit")
        label_limit.setBuddy(self.limit)
        form.addRow(label_limit, limit_behaelter)
        layout.addLayout(form)
        knoepfe = QDialogButtonBox()
        abbrechen = knoepfe.addButton("Abbrechen", QDialogButtonBox.ButtonRole.RejectRole)
        abbrechen.setObjectName("btn_einstellungen_abbrechen")
        self.btn_uebernehmen = knoepfe.addButton(
            "Übernehmen", QDialogButtonBox.ButtonRole.AcceptRole
        )
        self.btn_uebernehmen.setObjectName("btn_einstellungen_uebernehmen")
        knoepfe.accepted.connect(self._annehmen)
        knoepfe.rejected.connect(self.reject)
        layout.addWidget(knoepfe)
        if probleme:
            self._zeige_fehler(f"{t.symbol('fehler')} " + "; ".join(probleme))

    def _waehle(self) -> None:
        pfad = self.ordner_waehlen(self.ordner.text())
        if pfad:
            self.ordner.setText(pfad)

    def _ordner_dialog(self, start: str) -> str | None:  # pragma: no cover - modaler Dialog
        pfad = QFileDialog.getExistingDirectory(self, "Messdaten-Ordner wählen", start)
        return pfad or None

    def _annehmen(self) -> None:
        text = self.ordner.text().strip()
        self.fehler.hide()
        self.limit_fehler.hide()
        if not text:
            self._zeige_fehler(f"{t.symbol('fehler')} Bitte einen Ordner angeben.")
            return
        fehler_ordner, fehler_limit = self._uebernehmen(Path(text), self.limit.value())
        if fehler_ordner:
            self._zeige_fehler(f"{t.symbol('fehler')} {fehler_ordner}")
        if fehler_limit:
            self.limit_fehler.setText(f"{t.symbol('fehler')} {fehler_limit}")
            self.limit_fehler.show()
        if fehler_ordner or fehler_limit:
            return
        self.accept()

    def _zeige_fehler(self, text: str) -> None:
        self.fehler.setText(text)
        self.fehler.show()
