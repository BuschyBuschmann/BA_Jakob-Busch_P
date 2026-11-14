"""Reiter „Auswerten“ (P-AUSW T3a, Brief K-AUSW Abschnitte 1, 3.1, 6 und 10).

Zonen: AA Dateileiste, AB Parameterzeile (Platz immer reserviert), AC Ansichtswahl, AD
Auswahlspalte, AE Darstellung, AF Fußzeile. T3a liefert Ansicht 1 (Spektrum); die Ansichten 2 bis 4
sind sichtbar, aber deaktiviert (T3b), Export und Bild folgen in T4.

Laden (Nutzerentscheidung F-3, zweistufig): Stufe A
(:func:`~ldv_automation.auswertung.jobs.lese_job`) läuft in einem eigenen Prozess und zeigt
Ansicht 1 sofort; Stufe B (:func:`~ldv_automation.auswertung.jobs.pruef_job`) rechnet im
Hintergrund die Plausibilitätsprüfungen, die Fußzeile zeigt bis dahin „Prüfung: wird
berechnet …“. Ein ``QTimer`` fragt alle :data:`~ldv_automation.gui.tokens.ABFRAGE_AUSWERTEN_MS`
ms ab (kein Qt-Thread). Eine Job-ID verwirft veraltete Ergebnisse; ein neuer Dateiaufruf
bricht laufende Aufträge ab.

Dieses Modul ist ein dünnes Widget (Abdeckung nur mit ``pytest -m gui``); die Logik liegt in
:mod:`.anzeige_auswerten` und den Zeichenfunktionen.
"""

from __future__ import annotations

import functools
import itertools
import logging
from collections.abc import Callable, Iterator, Sequence
from contextlib import contextmanager
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from PySide6.QtCore import QSize, Qt, QTimer, Signal
from PySide6.QtGui import QAction, QColor, QKeySequence, QResizeEvent
from PySide6.QtWidgets import (
    QButtonGroup,
    QCheckBox,
    QComboBox,
    QDialog,
    QFileDialog,
    QFrame,
    QGraphicsOpacityEffect,
    QHBoxLayout,
    QInputDialog,
    QLabel,
    QListWidget,
    QListWidgetItem,
    QMessageBox,
    QProgressBar,
    QPushButton,
    QRadioButton,
    QScrollArea,
    QSizePolicy,
    QSplitter,
    QStackedWidget,
    QTabWidget,
    QVBoxLayout,
    QWidget,
)

from ldv_automation.auswertung.annahmen import AnnahmeEintrag, Annahmen
from ldv_automation.auswertung.export import (
    entferne_verwaiste_tmp,
    pruefe_ziel,
    unvollstaendiger_export,
)
from ldv_automation.auswertung.jobs import PruefErgebnis, export_job, lese_job, pruef_job
from ldv_automation.auswertung.laden import Geladen
from ldv_automation.darstellung import Ansicht, Zeichnung
from ldv_automation.darstellung.achsen import AchsenFehler
from ldv_automation.darstellung.auswahl import (
    KOMPONENTEN,
    DarstellungsFehler,
    Groesse,
    PaarCache,
    frf_daten,
    gesamtband,
    kanalpaare,
    schwingform_daten,
    spektrum_daten,
    spitzen_daten_frf,
    spitzen_daten_spektrum,
    standard_bezug,
    verfuegbare_groessen,
    waehle_ebene,
)
from ldv_automation.darstellung.bild import baue_stempel
from ldv_automation.darstellung.diagramm import TEILBILDER_MAX, DiagrammOptionen, teilbilder
from ldv_automation.darstellung.formate import frequenz_text
from ldv_automation.darstellung.frf import FrfOptionen
from ldv_automation.darstellung.schwingform import SchwingformOptionen
from ldv_automation.darstellung.serien_daten import (
    DiagrammSerie,
    SerienSpec,
    betrag_groesse,
    loese_alle_auf,
)
from ldv_automation.darstellung.spektrum import DB_GRUND, SpektrumOptionen
from ldv_automation.darstellung.spitzen import SpitzenOptionen
from ldv_automation.gui import tokens as t
from ldv_automation.gui.achsen_zustand import (
    ACHSEN_JE_ANSICHT,
    BETRAG_GROESSEN_5,
    einheit_aus_achsentitel,
)
from ldv_automation.gui.achsenleiste import Achsenleiste
from ldv_automation.gui.anzeige import Knopf
from ldv_automation.gui.anzeige_aktionen import (
    AKTIONS_TASTEN,
    DATEIFILTER_BILD,
    DATEIFILTER_EXPORT,
    TEXT_BILD_KEINE_DARSTELLUNG,
    TEXT_KEINE_ZULETZT,
    TEXT_PRUEFUNG_NOCH_NICHT,
    TEXT_ZIEHEN,
    bedienbarkeit_aktionen,
    bild_endung,
    bild_meldung,
    bild_unbestaetigt,
    bild_vorschlag,
    cursor_zeile,
    erste_auffaellige_zeile,
    export_basis,
    export_meldung,
    export_vorschlag,
    git_hash_text,
    pruefdialog_zeilen,
    stempel_ansicht,
    tooltip_mit_taste,
    zuletzt_eintrag,
)
from ldv_automation.gui.anzeige_auswerten import (
    ANSICHT_NAMEN,
    FREIGESCHALTETE_ANSICHTEN,
    TEXT_KEINE_BAENDER,
    TEXT_KEINE_DATEI,
    TEXT_KEINE_FRF,
    TEXT_KEINE_SPITZEN,
    TEXT_KEINE_SPITZENSUCHE,
    TEXT_PHASE_KEINE_REFERENZ,
    TEXT_PRUEFUNG_ABGEBROCHEN,
    TEXT_PRUEFUNG_BERECHNET,
    TEXT_SPITZE_WAEHLEN,
    AuswertenZustand,
    ParameterZelle,
    bedienbarkeit_auswerten,
    dateiname_von,
    fehler_band_text,
    folgefehler_text,
    geladen_text,
    kennzeichen_beschreibung,
    kennzeichen_text,
    lade_text,
    parameter_tooltip,
    parameter_zellen,
    phase_ref_text,
    plot_beschreibung,
    plotkopf_text,
    pruefung_fehler_text,
    pruefung_kern,
    pruefung_text,
    punkt_eintraege,
    waehle_antriebspunkt,
    zeichen_fehler_text,
    zellen_sichtbar,
)
from ldv_automation.gui.auswahl_auswerten import (
    AuswahlFrf,
    AuswahlSchwingform,
    AuswahlSpitzen,
    tab_halt,
)
from ldv_automation.gui.auswahl_diagramm import (
    AuswahlDiagramm,
    MessungsAngabe,
    SerienDialog,
    SerienEintrag,
)
from ldv_automation.gui.daten_auswerten import (
    BAENDER_SPALTEN,
    SPITZEN_SPALTEN,
    baender_zeilen,
    bandwerte_fuer,
    frequenz_pruefen,
    kanalpaar_text,
    spitze_angaben_text,
    spitze_der_linie,
    spitzen_zeilen,
)
from ldv_automation.gui.dialoge import frage
from ldv_automation.gui.einstellungen_auswerten import AuswertenEinstellungen
from ldv_automation.gui.messungen import MESSUNGEN_MAX, Messung, Messungen, MessungsZustand
from ldv_automation.gui.messungsleiste import Messungsleiste
from ldv_automation.gui.plotflaeche import PlotFlaeche
from ldv_automation.gui.plotstil import baue_plotstil
from ldv_automation.gui.pruefdialog import KuerzLabel, PruefDialog, PruefLabel
from ldv_automation.gui.serien import (
    TEXT_KEINE_SERIE,
    TEXT_SERIEN_VOLL,
    SerienFehler,
    SerienListe,
    baue_spec,
    groessen_verfuegbar,
    kopf_text,
    messungs_zugriff,
    paare_je_messung,
    serie_text,
    serien_fuer_alle,
    standard_paar,
    unmoeglich_text,
)
from ldv_automation.gui.stil import schrift
from ldv_automation.gui.tabellen_auswerten import ZEILENHOEHE_PX, TabellenBereich
from ldv_automation.hintergrund import (
    Auftrag,
    AuftragAbgebrochen,
    AuftragFehler,
    Ausfuehrer,
)

__all__ = ["AuswertenReiter", "ParameterZelleWidget"]

DATEIFILTER_SVD = "PSV-Messdatei (*.svd)"
"""Filter des Öffnen-Dialogs."""
TEXT_MINDESTENS_EINE = "Mindestens eine Komponente bleibt gewählt."
"""Tooltip der Komponenten-Kontrollkästchen (UI-4)."""
GRUND_DB = f"Nicht verfügbar: {DB_GRUND}."
"""Tooltip der deaktivierten Skala „dB“ (Nutzerentscheidung N-2)."""
BEZEICHNUNG_ZELLEN_PT = 8
"""Schriftgröße der kleinen Beschriftung über den Werten der Parameterzeile."""
GRAU_DECKKRAFT = 0.4
"""Deckkraft der Darstellung, solange eine neue Datei gelesen wird (bisherige Datei ausgegraut)."""

TABELLE_STANDARD_ZEILEN = 4
"""Sichtbare Zeilen der Tabelle in Ansicht 3 bei genügender Höhe. Bei kleinem Fenster hat der
Plot Vorrang (Nutzerentscheidung 2026-11-11, KONVENTIONEN.md): Die Tabelle zeigt dann weniger
Zeilen (:data:`PLOT_MIN_HOEHE_SPLITTER_PX`); T3b-3 gilt nur noch für große Fenster."""
PLOT_MIN_HOEHE_SPLITTER_PX = 212
"""Kleinste Höhe des Plots (ohne Achsenleiste) in Ansicht 3: Die Tabelle gibt zuerst nach, der
Plot behält so Achsenbeschriftung und Spitzen lesbar (Abnahme D-AUSW2-A, Befund 2)."""
PLOT_WUNSCH_HOEHE_SPLITTER_PX = 264
"""Gewünschte Höhe des Plots (ohne Achsenleiste) in Ansicht 3 bei der Standardhöhe der Tabelle:
Die Achse ist dann auch bei 1366 mal 768 mindestens 160 px hoch. Reicht der Platz nicht, gibt die
Tabelle bis auf ihre Mindesthöhe nach, danach der Plot bis :data:`PLOT_MIN_HOEHE_SPLITTER_PX`."""
TEXT_BILD_ANSICHT_5 = "Bild speichern ist für Ansicht 5 noch nicht freigeschaltet."
_BETRAG_NAMEN = {"spektrum": "Spektrum", "h1": "|H1|", "h2": "|H2|"}
"""Kurznamen der Betragsgrößen für die Auswahl der Achsenleiste (Ansicht 5, nebeneinander)."""
KOMPAKT_BREITE_PX = 1200
"""Unter dieser Breite des Reiters wird die Oberfläche kompakt: Dateiname neben den Chips,
Hinweis „Höchstens vier Serien“ und lange Beschriftungen der Achsenleiste entfallen (Plot und
Chips bekommen den Platz; die vollständigen Texte stehen in Tooltips)."""

TEXT_HINZU_ERST_DATEI = "Zuerst eine Messdatei öffnen."
"""Tooltip von ``Messung hinzufügen …`` ohne Datei (Brief K1-AUSW2 Abschnitt 4)."""
TEXT_HINZU_LAEDT = "Die Datei wird gerade gelesen."
TEXT_ENTFERNEN_ERSETZT = (
    "Messung {kurzname} wird gerade durch „Öffnen …“ ersetzt und lässt sich jetzt nicht entfernen."
)
TEXT_HINZU_VOLL = f"Höchstens {MESSUNGEN_MAX} Messungen; zuerst eine entfernen."
TEXT_DIESELBE_DATEI = "Dieselbe Datei wie {kurzname}."
TEXT_KANALPAAR_ANSICHT_4 = "Spitzenliste und Kennzeichen der Linie stammen aus diesem Paar."

_SEITE_LEER = 0
_SEITE_PLOT = 1
_SEITE_TEXT = 2

_log = logging.getLogger(__name__)


@dataclass
class _Auswahl:
    """Auswahl von Ansicht 1 (wird beim Dateiwechsel zurückgesetzt, OE-3)."""

    punkt: int | None = None
    komponenten: tuple[str, ...] = KOMPONENTEN
    groesse: Groesse = "kohaerent"
    skala: str = "log"


class _LinksKuerzLabel(QLabel):
    """Label, das zu langen Text links mit „…“ kürzt (Pfad); der Volltext steht im Tooltip."""

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._voll = ""
        self.setSizePolicy(QSizePolicy.Policy.Ignored, QSizePolicy.Policy.Preferred)
        self.setMinimumWidth(40)

    def setText(self, text: str) -> None:  # noqa: N802  # Qt-Name
        """Setzt den Volltext (Anzeige links gekürzt, Tooltip vollständig)."""
        self._voll = text
        self.setToolTip(text)
        # Die Anzeige ist gekürzt; Hilfsmittel bekommen den vollen Pfad.
        self.setAccessibleName(text)
        self.setAccessibleDescription(f"Pfad der Messdatei: {text}" if text else "")
        self._kuerze()

    def volltext(self) -> str:
        """Ungekürzter Text."""
        return self._voll

    def resizeEvent(self, event: QResizeEvent) -> None:  # noqa: N802  # Qt-Name
        """Kürzt neu, wenn sich die Breite ändert."""
        super().resizeEvent(event)
        self._kuerze()

    def _kuerze(self) -> None:
        breite = max(self.width() - 2, 0)
        QLabel.setText(
            self, self.fontMetrics().elidedText(self._voll, Qt.TextElideMode.ElideLeft, breite)
        )


class _Fusszeile(QFrame):
    """Fußzeile (Zone AF), die ihre Größenänderung meldet (Verteilung der Breite)."""

    groesse_geaendert = Signal()

    def resizeEvent(self, event: QResizeEvent) -> None:  # noqa: N802  # Qt-Name
        """Meldet die neue Breite."""
        super().resizeEvent(event)
        self.groesse_geaendert.emit()


_PRUEF_MIN_PX = 150
"""Mindestbreite des Prüftextes in der Fußzeile (reicht für „Prüfung: 36 ok, …“)."""
_MELDE_MIN_PX = 160
"""Mindestbreite der Meldezeile (Cursor-/Exportmeldung): der Prüftext darf sie nie verdrängen
(UI-25); der Prüftext gibt sie notfalls ab, auch die Auffälligkeitszahlen werden dann gekürzt."""


class ParameterZelleWidget(QWidget):
    """Eine Zelle der Parameterzeile: kleine Beschriftung über dem Wert (Consolas)."""

    def __init__(self, schluessel: str, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setObjectName(f"par_{schluessel}")
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        self.beschriftung = QLabel()
        self.beschriftung.setObjectName(f"par_{schluessel}_beschriftung")
        self.beschriftung.setFont(schrift(BEZEICHNUNG_ZELLEN_PT))
        self.beschriftung.setProperty("art", "gedaempft")
        self.wert = QLabel()
        self.wert.setObjectName(f"par_{schluessel}_wert")
        self.wert.setFont(schrift(t.SCHRIFT_PT, mono=True))
        layout.addWidget(self.beschriftung)
        layout.addWidget(self.wert)

    def setze(self, zelle: ParameterZelle) -> None:
        """Zeigt Beschriftung, Wert und Tooltip der Zelle."""
        self.beschriftung.setText(zelle.beschriftung)
        self.wert.setText(zelle.wert)
        self.setToolTip(zelle.tooltip)
        self.setAccessibleName(f"{zelle.beschriftung}: {zelle.wert}")


class _Parameterzeile(QFrame):
    """Zone AB: feste Höhe; Zellen werden rechts ausgeblendet, wenn die Breite nicht reicht."""

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setObjectName("parameterzeile")
        self.setAccessibleName("Parameter der Messdatei")
        self.setFixedHeight(t.HOEHE_PARAMETERZEILE_PX)
        self._layout = QHBoxLayout(self)
        self._layout.setContentsMargins(12, 2, 12, 2)
        self._layout.setSpacing(0)
        self.zellen: list[ParameterZelleWidget] = []

    def setze_zellen(self, zellen: tuple[ParameterZelle, ...]) -> None:
        """Legt die Zellen beim ersten Aufruf an und setzt ihre Werte."""
        if not self.zellen:
            for z in zellen:
                w = ParameterZelleWidget(z.schluessel)
                self.zellen.append(w)
                self._layout.addWidget(w)
                self._layout.addSpacing(24)
            self._layout.addStretch(1)
        for w, z in zip(self.zellen, zellen, strict=True):
            w.setze(z)
        self.setToolTip(parameter_tooltip(zellen))
        self.blende_aus()

    def blende_aus(self) -> None:
        """Blendet Zellen rechts aus, die nicht mehr passen (Brief Abschnitt 1, AB)."""
        if not self.zellen:
            return
        for w in self.zellen:
            w.setVisible(True)
        breiten = [w.sizeHint().width() for w in self.zellen]
        verfuegbar = self.width() - 24
        anzahl = zellen_sichtbar(breiten, verfuegbar, abstand_px=24)
        for i, w in enumerate(self.zellen):
            w.setVisible(i < anzahl)

    def sichtbare_zellen(self) -> list[str]:
        """``objectName`` der sichtbaren Zellen (nicht ``isVisible``: auch vor dem Anzeigen)."""
        return [w.objectName() for w in self.zellen if not w.isHidden()]

    def resizeEvent(self, event: QResizeEvent) -> None:  # noqa: N802  # Qt-Name
        """Blendet bei Breitenänderung Zellen ein bzw. aus."""
        super().resizeEvent(event)
        self.blende_aus()


def _sha_von(geladen: Geladen) -> str | None:
    """Prüfsumme der Datei aus der Herkunft (``None`` ohne Herkunft)."""
    herkunft = geladen.messdaten.herkunft
    return herkunft.sha256 if herkunft is not None else None


class AuswertenReiter(QWidget):
    """Inhalt des Reiters „Auswerten“.

    Parameters
    ----------
    ausfuehrer : Ausfuehrer
        Startet die Hintergrundaufträge (:class:`~ldv_automation.hintergrund.ProzessAusfuehrer`
        in der Oberfläche, ``DirektAusfuehrer`` oder ein nie fertiger Ausführer in Tests).
    abfrage_ms : int, optional
        Takt der Abfrage laufender Aufträge.
    einstellungen : AuswertenEinstellungen, optional
        Gemerkter Ordner und „Zuletzt geöffnet“ (INI); ohne Angabe die Standarddatei.
    git_hash : callable, optional
        Liefert ``(Git-Hash, Arbeitsbaum geändert)`` der Software für den Bildstempel.
    parent : QWidget, optional
        Elternwidget.
    """

    def __init__(
        self,
        ausfuehrer: Ausfuehrer,
        *,
        abfrage_ms: int = t.ABFRAGE_AUSWERTEN_MS,
        einstellungen: AuswertenEinstellungen | None = None,
        git_hash: Callable[[], tuple[str | None, bool | None]] | None = None,
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)
        self.setObjectName("auswerten_inhalt")
        self._ausfuehrer = ausfuehrer
        self._zustand = AuswertenZustand.KEINE_DATEI
        self._messungen = Messungen()
        self._serien = SerienListe()
        self._serien_aufgeloest: dict[tuple[object, ...], DiagrammSerie] = {}
        self._auswahl = _Auswahl()
        self._job_id = 0
        self._ersetze_ziel: int | None = None
        self._aktiviere_danach: int | None = None
        self._dialog_tiefe = 0
        self._kompakt = False
        self._zusatz: dict[int, Auftrag] = {}
        self._b_messung: int | None = None
        self._auftrag_a: tuple[int, Auftrag, str] | None = None
        self._auftrag_b: tuple[int, Auftrag] | None = None
        self._fehlertext: str | None = None
        self._ansicht = 1
        self._paare: tuple[tuple[str, str], ...] = ()
        self._spitze: int | None = None
        self._ansichtstext: str | None = None
        self._plot_ansicht: int | None = None
        self._a4_letzt: tuple[Any, Any, str, str, str] | None = None
        self._a4_komponente: str | None = None
        self._tabellen_hoehe: int | None = None
        self._a3_schluessel: tuple[str, str] | str | None = None
        self._a3_spitzen: tuple[object, ...] = ()
        self._a4_geladen = False
        self._a4_paar_schluessel: object = None
        self._in_aufbau = False
        self._einstellungen = (
            einstellungen if einstellungen is not None else AuswertenEinstellungen()
        )
        self._git_hash = git_hash if git_hash is not None else (lambda: (None, None))
        self._letzter_ordner = self._einstellungen.letzter_ordner()
        self._abfrage_ms = abfrage_ms
        self._auftrag_c: tuple[Auftrag, str] | None = None
        self._meldung = ""
        self._meldung_pfade: tuple[str, ...] = ()
        self._export_notiz = ""
        self._cursor_aktiv = False
        self._a4_wunsch_hz: float | None = None
        self._kanal_a3 = ""

        self._baue()
        self._timer = QTimer(self)
        self._timer.setObjectName("abfrage_auswerten")
        self._timer.setInterval(abfrage_ms)
        self._timer.timeout.connect(self._abfrage)
        self._baue_aktionen()
        self._wende_zustand_an()
        self._fuelle_parameter()
        self._tab_reihenfolge()

    # --- Aufbau ----------------------------------------------------------------------------

    def _baue(self) -> None:
        haupt = QVBoxLayout(self)
        haupt.setContentsMargins(0, 0, 0, 0)
        haupt.setSpacing(0)
        haupt.addWidget(self._baue_dateileiste())
        self.parameterzeile = _Parameterzeile()
        haupt.addWidget(self.parameterzeile)
        haupt.addWidget(self._baue_ansichtswahl())
        mitte = QWidget()
        mitte_layout = QHBoxLayout(mitte)
        mitte_layout.setContentsMargins(t.FENSTERRAND_PX, 8, t.FENSTERRAND_PX, 8)
        mitte_layout.setSpacing(12)
        mitte_layout.addWidget(self._baue_auswahlspalte())
        mitte_layout.addWidget(self._baue_darstellung(), 1)
        haupt.addWidget(mitte, 1)
        haupt.addWidget(self._baue_fusszeile())

    def _baue_aktionen(self) -> None:
        """Aktionen mit Tastenkürzel (Brief Abschnitt 8): eine Quelle für Knopf, Taste, Aktivierung.

        ``Qt.WindowShortcut``: Die Aktionen hängen am Reiter und gelten nur, solange er sichtbar
        ist, also nicht im Reiter „Messen“.
        """
        self.act_oeffnen = self._aktion("oeffnen", "Messdatei öffnen", self._oeffnen_geklickt)
        self.act_export = self._aktion("export", "Daten exportieren", self._export_geklickt)
        self.act_bild = self._aktion("bild", "Bild speichern", self._bild_geklickt)
        self.btn_export.clicked.connect(self._export_geklickt)
        self.btn_bild.clicked.connect(self._bild_geklickt)
        self.act_ansicht = {
            nr: self._aktion(
                f"ansicht_{nr}", f"Ansicht {nr}", functools.partial(self._ansicht_per_taste, nr)
            )
            for nr in ANSICHT_NAMEN
        }

    def _aktion(self, name: str, text: str, slot: Callable[[], None]) -> QAction:
        aktion = QAction(text, self)
        aktion.setObjectName(f"act_ausw_{name}")
        aktion.setShortcut(QKeySequence(AKTIONS_TASTEN[name][0]))
        aktion.setShortcutContext(Qt.ShortcutContext.WindowShortcut)
        aktion.triggered.connect(slot)
        self.addAction(aktion)
        return aktion

    def _ansicht_per_taste(self, nr: int) -> None:
        knopf = self.btn_ansicht[nr]
        if knopf.isEnabled():
            knopf.click()

    def _baue_dateileiste(self) -> QFrame:
        leiste = QFrame()
        leiste.setObjectName("dateileiste")
        leiste.setFixedHeight(t.HOEHE_DATEILEISTE_PX)
        z = QHBoxLayout(leiste)
        z.setContentsMargins(12, 4, 12, 4)
        self.btn_oeffnen = QPushButton("Öffnen …")
        self.btn_oeffnen.setObjectName("btn_oeffnen")
        self.btn_oeffnen.setProperty("art", "primaer")
        self.btn_messung_hinzu = QPushButton("Messung hinzufügen …")
        self.btn_messung_hinzu.setObjectName("btn_messung_hinzu")
        self.messungsleiste = Messungsleiste()
        self.lbl_datei = QLabel("–")
        self.lbl_datei.setObjectName("lbl_datei")
        self.lbl_datei.setFont(schrift(fett=True))
        self.lbl_datei.setSizePolicy(QSizePolicy.Policy.Ignored, QSizePolicy.Policy.Preferred)
        self.lbl_datei.setMinimumWidth(90)  # bei kleinem Fenster gekürzt, Platz gehört den Chips
        self.lbl_pfad = _LinksKuerzLabel()
        self.lbl_pfad.setObjectName("lbl_pfad")
        self.lbl_pfad.setFont(schrift(t.SCHRIFT_PT, mono=True))
        self.lbl_pfad.setProperty("art", "gedaempft")
        self._namen_box = QWidget()  # eigener Behälter: ausgeblendet gibt er den Platz frei
        namen = QVBoxLayout(self._namen_box)
        namen.setContentsMargins(0, 0, 0, 0)
        namen.setSpacing(0)
        namen.addWidget(self.lbl_datei)
        namen.addWidget(self.lbl_pfad)
        self.btn_export = QPushButton("Daten exportieren …")
        self.btn_export.setObjectName("btn_export")
        self.btn_bild = QPushButton("Bild speichern …")
        self.btn_bild.setObjectName("btn_bild")
        self.lbl_arbeitsansicht = QLabel("Arbeitsansicht")
        self.lbl_arbeitsansicht.setObjectName("lbl_arbeitsansicht")
        self.lbl_arbeitsansicht.setProperty("art", "gedaempft")
        for knopf in (self.btn_oeffnen, self.btn_messung_hinzu, self.btn_export, self.btn_bild):
            knopf.setAutoDefault(False)
            knopf.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        z.addWidget(self.btn_oeffnen)
        z.addWidget(self.btn_messung_hinzu)
        z.addSpacing(8)
        z.addWidget(self.messungsleiste, 2)  # freier Platz geht zuerst an die Chips
        z.addSpacing(8)
        z.addWidget(self._namen_box, 1)
        z.addWidget(self.btn_export)
        z.addWidget(self.btn_bild)
        z.addWidget(self.lbl_arbeitsansicht)
        self.btn_oeffnen.clicked.connect(self._oeffnen_geklickt)
        self.btn_messung_hinzu.clicked.connect(self._messung_hinzu_geklickt)
        self.messungsleiste.wechsel.connect(self._aktiviere_messung)
        self.messungsleiste.entfernen.connect(self._entferne_geklickt)
        self.messungsleiste.umbenennen.connect(self._umbenennen_geklickt)
        return leiste

    def _baue_ansichtswahl(self) -> QFrame:
        leiste = QFrame()
        leiste.setObjectName("ansichtswahl")
        leiste.setFixedHeight(t.HOEHE_ANSICHTSWAHL_PX)
        z = QHBoxLayout(leiste)
        z.setContentsMargins(12, 0, 12, 0)
        z.setSpacing(4)
        self._ansicht_gruppe = QButtonGroup(self)
        self._ansicht_gruppe.setExclusive(True)
        self.btn_ansicht: dict[int, QPushButton] = {}
        for nr, name in ANSICHT_NAMEN.items():
            knopf = QPushButton(f"{nr} {name}")
            knopf.setObjectName(f"btn_ansicht_{nr}")
            knopf.setCheckable(True)
            knopf.setAutoDefault(False)
            knopf.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
            knopf.setAccessibleName(f"Ansicht {nr}: {name}")
            knopf.setProperty("art", "segment")
            self._ansicht_gruppe.addButton(knopf, nr)
            self.btn_ansicht[nr] = knopf
            z.addWidget(knopf)
        self.btn_ansicht[1].setChecked(True)
        z.addStretch(1)
        self._ansicht_gruppe.idClicked.connect(self._ansicht_gewaehlt)
        return leiste

    def _baue_auswahlspalte(self) -> QScrollArea:
        """Zone AD: 260 px fest, scrollbar bei Überlänge; Seiten je Ansicht (Brief Abschnitt 3).

        Oberhalb des Stapels stehen die Elemente, die mehrere Ansichten teilen: die Kanalpaarwahl
        (Ansichten 2, 3 und 4, nur bei mehr als einem Paar) und die Punktliste (Ansichten 1 und 2).

        Das Kanalpaar gilt gemeinsam für alle Ansichten (Nutzer bestätigt): Eine Wahl in Ansicht 2
        bleibt in Ansicht 3 und 4 bestehen und umgekehrt.
        """
        self.auswahlspalte = QScrollArea()
        self.auswahlspalte.setObjectName("auswahlspalte")
        self.auswahlspalte.setFixedWidth(t.BREITE_AUSWAHLSPALTE_PX)
        self.auswahlspalte.setWidgetResizable(True)
        self.auswahlspalte.setFrameShape(QFrame.Shape.NoFrame)
        self.auswahlspalte.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.auswahlspalte.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self._ad_inhalt = QWidget()
        self._ad_inhalt.setObjectName("auswahl_inhalt")
        v = QVBoxLayout(self._ad_inhalt)
        v.setContentsMargins(0, 0, 0, 0)
        v.setSpacing(6)

        self.kanalpaar_gruppe = QWidget()
        self.kanalpaar_gruppe.setObjectName("kanalpaar_gruppe")
        kv = QVBoxLayout(self.kanalpaar_gruppe)
        kv.setContentsMargins(0, 0, 8, 0)
        kv.setSpacing(4)
        kv.addWidget(self._gruppentitel("Kanalpaar (Antwort / Referenz)"))
        self.combo_kanalpaar = QComboBox()
        self.combo_kanalpaar.setObjectName("combo_kanalpaar")
        self.combo_kanalpaar.setAccessibleName("Kanalpaar, Antwort und Referenz")
        self.combo_kanalpaar.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        kv.addWidget(self.combo_kanalpaar)
        self.lbl_kanalpaar_hinweis = QLabel()
        self.lbl_kanalpaar_hinweis.setObjectName("lbl_kanalpaar_hinweis")
        self.lbl_kanalpaar_hinweis.setProperty("art", "gedaempft")
        self.lbl_kanalpaar_hinweis.setWordWrap(True)
        self.lbl_kanalpaar_hinweis.setFont(schrift(8))
        kv.addWidget(self.lbl_kanalpaar_hinweis)
        self.kanalpaar_gruppe.setVisible(False)
        v.addWidget(self.kanalpaar_gruppe)

        self.punkt_gruppe = QWidget()
        self.punkt_gruppe.setObjectName("punkt_gruppe")
        pv = QVBoxLayout(self.punkt_gruppe)
        pv.setContentsMargins(0, 0, 8, 0)
        pv.setSpacing(4)
        pv.addWidget(self._gruppentitel("Punkt"))
        self.liste_punkte = QListWidget()
        self.liste_punkte.setObjectName("liste_punkte")
        self.liste_punkte.setAccessibleName("Punkt oder Mittel")
        self.liste_punkte.setMinimumHeight(140)
        self.liste_punkte.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        pv.addWidget(self.liste_punkte, 1)
        v.addWidget(self.punkt_gruppe, 1)

        self._ad_stapel = QStackedWidget()
        self._ad_stapel.setObjectName("auswahl_stapel")
        self.auswahl_frf = AuswahlFrf()
        self.auswahl_spitzen = AuswahlSpitzen()
        self.auswahl_sf = AuswahlSchwingform()
        self.auswahl_diagramm = AuswahlDiagramm(baue_plotstil())
        self._ad_seiten = [
            self._baue_auswahl_spektrum(),
            self.auswahl_frf,
            self.auswahl_spitzen,
            self.auswahl_sf,
            self.auswahl_diagramm,
        ]
        for seite in self._ad_seiten:
            self._ad_stapel.addWidget(seite)
        v.addWidget(self._ad_stapel)
        self.auswahlspalte.setWidget(self._ad_inhalt)
        self.liste_punkte.currentRowChanged.connect(self._auswahl_geaendert)
        self.combo_kanalpaar.currentIndexChanged.connect(self._paar_geaendert)
        self.auswahl_frf.geaendert.connect(self._ansicht_geaendert)
        self.auswahl_sf.geaendert.connect(self._ansicht_geaendert)
        self.auswahl_sf.spitze_gewaehlt.connect(self._spitze_fuer_schwingform)
        self.auswahl_diagramm.groesse_geaendert.connect(self._groesse_5_geaendert)
        self.auswahl_diagramm.geaendert.connect(self._optionen_5_geaendert)
        self.auswahl_diagramm.serie_neu.connect(self._serie_neu)
        self.auswahl_diagramm.serie_alle.connect(self._serie_alle)
        self.auswahl_diagramm.serie_entfernen.connect(self._serie_entfernen_geklickt)
        self.auswahl_diagramm.serie_sichtbar.connect(self._serie_sichtbar_geaendert)
        return self.auswahlspalte

    @staticmethod
    def _gruppentitel(text: str) -> QLabel:
        titel = QLabel(text)
        titel.setFont(schrift(fett=True))
        return titel

    def _baue_auswahl_spektrum(self) -> QWidget:
        seite = QWidget()
        seite.setObjectName("auswahl_spektrum")
        v = QVBoxLayout(seite)
        v.setContentsMargins(0, 0, 8, 0)
        v.setSpacing(6)

        v.addWidget(self._gruppentitel("Komponente"))
        self.chk: dict[str, QCheckBox] = {}
        reihe = QHBoxLayout()
        for c in KOMPONENTEN:
            kasten = QCheckBox(c)
            kasten.setObjectName(f"chk_{c.lower()}")
            kasten.setChecked(True)
            kasten.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
            kasten.setToolTip(TEXT_MINDESTENS_EINE)
            kasten.setAccessibleName(f"Komponente {c}")
            self.chk[c] = kasten
            reihe.addWidget(kasten)
        v.addLayout(reihe)

        v.addWidget(self._gruppentitel("Größe"))
        self._gruppe_groesse = QButtonGroup(self)
        self.rb_groesse_cph = QRadioButton("|CPH|, kohärent mit Referenz")
        self.rb_groesse_cph.setObjectName("rb_groesse_cph")
        self.rb_groesse_ap = QRadioButton("√AP, Leistungsmittel")
        self.rb_groesse_ap.setObjectName("rb_groesse_ap")
        for knopf in (self.rb_groesse_cph, self.rb_groesse_ap):
            knopf.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
            self._gruppe_groesse.addButton(knopf)
            v.addWidget(knopf)
        self.rb_groesse_cph.setChecked(True)
        self.lbl_groesse_grund = QLabel()
        self.lbl_groesse_grund.setObjectName("lbl_groesse_grund")
        self.lbl_groesse_grund.setProperty("art", "gedaempft")
        self.lbl_groesse_grund.setWordWrap(True)
        self.lbl_groesse_grund.setVisible(False)
        v.addWidget(self.lbl_groesse_grund)

        # Skala linear/logarithmisch: Achsenleiste AG (R-073, A-2); „dB“ bleibt hier.
        v.addWidget(self._gruppentitel("Amplitude"))
        self.rb_skala_db = QRadioButton("dB")
        self.rb_skala_db.setObjectName("rb_skala_db")
        self.rb_skala_db.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        v.addWidget(self.rb_skala_db)
        self.rb_skala_db.setEnabled(False)
        self.rb_skala_db.setToolTip(GRUND_DB)
        self.rb_skala_db.setAccessibleDescription(GRUND_DB)
        self.lbl_db_grund = QLabel(GRUND_DB)
        self.lbl_db_grund.setObjectName("lbl_db_grund")
        self.lbl_db_grund.setProperty("art", "gedaempft")
        self.lbl_db_grund.setWordWrap(True)
        v.addWidget(self.lbl_db_grund)

        self.lbl_hinweise = QLabel()
        self.lbl_hinweise.setObjectName("lbl_hinweise")
        self.lbl_hinweise.setProperty("art", "gedaempft")
        self.lbl_hinweise.setWordWrap(True)
        v.addWidget(self.lbl_hinweise)
        v.addStretch(0)

        for kasten in self.chk.values():
            kasten.toggled.connect(self._auswahl_geaendert)
        self._gruppe_groesse.buttonToggled.connect(self._auswahl_geaendert)
        self._gruppe_groesse.buttonToggled.connect(lambda _k, _an: tab_halt(self._gruppe_groesse))
        tab_halt(self._gruppe_groesse)
        return seite

    def _baue_darstellung(self) -> QWidget:
        """Zone AE: Fehlerband, Ladeleiste, Kopfzeile und Plot bzw. Platzhalter."""
        ae = QWidget()
        ae.setObjectName("darstellung")
        ae.setMinimumSize(t.PLOT_MIN_BREITE_PX, t.PLOT_MIN_HOEHE_PX)
        v = QVBoxLayout(ae)
        v.setContentsMargins(0, 0, 0, 0)
        v.setSpacing(6)

        self.band_fehler = QFrame()
        self.band_fehler.setObjectName("band_fehler")
        self.band_fehler.setAccessibleName("Fehler beim Lesen")
        b = QHBoxLayout(self.band_fehler)
        b.setContentsMargins(12, 6, 12, 6)
        self.lbl_fehler = QLabel()
        self.lbl_fehler.setObjectName("lbl_fehler")
        self.lbl_fehler.setWordWrap(True)
        self.lbl_fehler.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        self.btn_fehler_schliessen = QPushButton("Schließen")
        self.btn_fehler_schliessen.setObjectName("btn_fehler_schliessen")
        self.btn_fehler_schliessen.setAutoDefault(False)
        self.btn_fehler_schliessen.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        b.addWidget(self.lbl_fehler, 1)
        b.addWidget(self.btn_fehler_schliessen)
        self.band_fehler.setVisible(False)
        self.btn_fehler_schliessen.clicked.connect(self.schliesse_fehlerband)
        v.addWidget(self.band_fehler)

        self.laden_leiste = QFrame()
        self.laden_leiste.setObjectName("laden_leiste")
        ll = QHBoxLayout(self.laden_leiste)
        ll.setContentsMargins(0, 0, 0, 0)
        self.lbl_laden = QLabel()
        self.lbl_laden.setObjectName("lbl_laden")
        self.lbl_laden.setFont(schrift(fett=True))
        self.balken_laden = QProgressBar()
        self.balken_laden.setObjectName("balken_laden")
        self.balken_laden.setRange(0, 0)
        self.balken_laden.setTextVisible(False)
        self.balken_laden.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.balken_laden.setAccessibleName("Datei wird gelesen")
        ll.addWidget(self.lbl_laden)
        ll.addWidget(self.balken_laden, 1)
        self.laden_leiste.setVisible(False)
        v.addWidget(self.laden_leiste)

        self.lbl_plotkopf = QLabel()
        self.lbl_plotkopf.setObjectName("lbl_plotkopf")
        self.lbl_plotkopf.setProperty("art", "gedaempft")
        self.lbl_plotkopf.setVisible(False)
        v.addWidget(self.lbl_plotkopf)

        self._ae_stapel = QStackedWidget()
        self._ae_stapel.setObjectName("darstellung_stapel")
        leer = QWidget()
        leer.setObjectName("darstellung_leer")
        lv = QVBoxLayout(leer)
        lv.addStretch(1)
        self.plot_platzhalter = QLabel(TEXT_KEINE_DATEI)
        self.plot_platzhalter.setObjectName("plot_platzhalter")
        self.plot_platzhalter.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.plot_platzhalter.setFont(schrift(12))
        self.btn_oeffnen_leer = QPushButton("Messdatei (.svd) öffnen …")
        self.btn_oeffnen_leer.setObjectName("btn_oeffnen_leer")
        self.btn_oeffnen_leer.setProperty("art", "primaer")
        self.btn_oeffnen_leer.setAutoDefault(False)
        self.btn_oeffnen_leer.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.btn_oeffnen_leer.clicked.connect(self._oeffnen_geklickt)
        lv.addWidget(self.plot_platzhalter)
        zeile = QHBoxLayout()
        zeile.addStretch(1)
        zeile.addWidget(self.btn_oeffnen_leer)
        zeile.addStretch(1)
        lv.addLayout(zeile)
        self.lbl_ziehen = QLabel(TEXT_ZIEHEN)
        self.lbl_ziehen.setObjectName("lbl_ziehen")
        self.lbl_ziehen.setProperty("art", "gedaempft")
        self.lbl_ziehen.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lv.addWidget(self.lbl_ziehen)
        self.zuletzt_gruppe = QWidget()
        self.zuletzt_gruppe.setObjectName("zuletzt_gruppe")
        self.zuletzt_gruppe.setMaximumWidth(620)
        zg = QVBoxLayout(self.zuletzt_gruppe)
        zg.setContentsMargins(0, 8, 0, 0)
        zg.setSpacing(4)
        self.lbl_zuletzt = QLabel("Zuletzt geöffnet")
        self.lbl_zuletzt.setObjectName("lbl_zuletzt")
        self.lbl_zuletzt.setFont(schrift(fett=True))
        self.liste_zuletzt = QListWidget()
        self.liste_zuletzt.setObjectName("liste_zuletzt")
        self.liste_zuletzt.setAccessibleName("Zuletzt geöffnete Dateien")
        self.liste_zuletzt.setToolTip("Doppelklick oder Enter öffnet die Datei")
        self.liste_zuletzt.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.liste_zuletzt.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.liste_zuletzt.setTextElideMode(Qt.TextElideMode.ElideMiddle)
        self.liste_zuletzt.itemActivated.connect(self._zuletzt_aktiviert)
        zg.addWidget(self.lbl_zuletzt)
        zg.addWidget(self.liste_zuletzt)
        zz = QHBoxLayout()
        zz.addStretch(1)
        zz.addWidget(self.zuletzt_gruppe, 3)
        zz.addStretch(1)
        lv.addLayout(zz)
        lv.addStretch(1)
        self._ae_stapel.addWidget(leer)
        self.plot = PlotFlaeche(baue_plotstil())
        self.plot.fehler.connect(self._zeichenfehler)
        self.plot.cursor_bewegt.connect(self._cursor_bewegt)
        self.plot.frequenz_geklickt.connect(self._plot_geklickt)
        self.plot.cursor_uebernommen.connect(self._plot_geklickt)
        self.plot.spitze_geklickt.connect(self._spitze_in_tabelle_gewaehlt)
        self._grau_effekt = QGraphicsOpacityEffect(self.plot)
        self._grau_effekt.setOpacity(GRAU_DECKKRAFT)
        self._grau_effekt.setEnabled(False)
        self.plot.setGraphicsEffect(self._grau_effekt)
        self._plot_seite = QSplitter(Qt.Orientation.Vertical)
        self._plot_seite.setObjectName("plot_seite")
        self._plot_seite.setChildrenCollapsible(False)
        # AG liegt als Geschwister der Plotfläche (nicht als Kind): Pos1 gilt nur im Teilbaum der
        # Plotfläche und nähme den Textfeldern sonst den Zeilenanfang (Plan U-A4).
        self.achsenleiste = Achsenleiste(self.plot.achsen_zustand)
        self.achsenleiste.geaendert.connect(self._achsen_geaendert)
        self.achsenleiste.groesse_gewaehlt.connect(self._achsenleiste_aktualisieren)
        self.plot.grenzen_gezeichnet.connect(self._achsenleiste_aktualisieren)
        self.plot.achsen_geaendert.connect(self._achsenleiste_aktualisieren)
        # Die Skala der Amplitude gehört der Achsenleiste; die Namen bleiben für Aufrufer und Tests.
        betrag = self.achsenleiste.gruppe("betrag")
        assert betrag.rb_linear is not None and betrag.rb_log is not None
        self.rb_skala_linear = betrag.rb_linear
        self.rb_skala_log = betrag.rb_log
        self.rb_skala_linear.setObjectName("rb_skala_linear")
        self.rb_skala_log.setObjectName("rb_skala_log")
        self._plot_spalte = QWidget()
        self._plot_spalte.setObjectName("plot_spalte")
        spalte = QVBoxLayout(self._plot_spalte)
        spalte.setContentsMargins(0, 0, 0, 0)
        spalte.setSpacing(0)
        spalte.addWidget(self.achsenleiste)
        spalte.addWidget(self.plot, 1)
        self._plot_seite.addWidget(self._plot_spalte)
        self.tabellen = QTabWidget()
        self.tabellen.setObjectName("tabellen")
        self.tabelle_spitzen = TabellenBereich("tabelle_spitzen", SPITZEN_SPALTEN)
        self.tabelle_baender = TabellenBereich("tabelle_baender", BAENDER_SPALTEN)
        self.tabellen.addTab(self.tabelle_spitzen, "Spitzen")
        self.tabellen.addTab(self.tabelle_baender, "Bänder")
        self.tabellen.setVisible(False)
        self._plot_seite.addWidget(self.tabellen)
        self._plot_seite.setStretchFactor(0, 3)
        self._plot_seite.setStretchFactor(1, 2)
        self.tabelle_spitzen.zeile_gewaehlt.connect(self._spitze_in_tabelle_gewaehlt)
        self._plot_seite.splitterMoved.connect(self._splitter_bewegt)
        self._ae_stapel.addWidget(self._plot_seite)
        text_seite = QWidget()
        text_seite.setObjectName("darstellung_text")
        tv = QVBoxLayout(text_seite)
        self.lbl_ansicht_platzhalter = QLabel()
        self.lbl_ansicht_platzhalter.setObjectName("lbl_ansicht_platzhalter")
        self.lbl_ansicht_platzhalter.setWordWrap(True)
        self.lbl_ansicht_platzhalter.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lbl_ansicht_platzhalter.setFont(schrift(11))
        tv.addWidget(self.lbl_ansicht_platzhalter)
        self._ae_stapel.addWidget(text_seite)
        v.addWidget(self._ae_stapel, 1)
        return ae

    def _baue_fusszeile(self) -> QFrame:
        fuss = _Fusszeile()
        fuss.setObjectName("fusszeile")
        fuss.setFixedHeight(t.HOEHE_FUSSZEILE_PX)
        f = QHBoxLayout(fuss)
        f.setContentsMargins(12, 2, 12, 2)
        self.lbl_cursor = KuerzLabel(voll_im_tooltip=True)
        self.lbl_cursor.setObjectName("lbl_cursor")
        self.lbl_cursor.setFont(schrift(t.SCHRIFT_PT, mono=True))
        self.lbl_cursor.setSizePolicy(QSizePolicy.Policy.Ignored, QSizePolicy.Policy.Preferred)
        self.balken_export = QProgressBar()
        self.balken_export.setObjectName("balken_export")
        self.balken_export.setRange(0, 0)
        self.balken_export.setTextVisible(False)
        self.balken_export.setFixedWidth(120)
        self.balken_export.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.balken_export.setAccessibleName("Export läuft")
        self.balken_export.setVisible(False)
        self.lbl_pruefung = PruefLabel(pruefung_text(()))
        self.lbl_pruefung.setObjectName("lbl_pruefung")
        self.lbl_pruefung.setFont(schrift(t.SCHRIFT_PT, mono=True))
        self.lbl_pruefung.geklickt.connect(self._zeige_pruefdialog)
        f.addWidget(self.lbl_cursor, 1)
        f.addWidget(self.balken_export)
        f.addWidget(self.lbl_pruefung)
        self._fuss = fuss
        self._fuss_layout = f
        fuss.groesse_geaendert.connect(self._fuss_verteilen)
        return fuss

    def _fuss_verteilen(self) -> None:
        """Teilt die Breite der Fußzeile: erst die Meldezeile, der Prüftext bekommt den Rest.

        Der Prüftext wird an Teilgrenzen gekürzt („Prüfung: 1 Warnung, …“), mindestens
        :data:`_PRUEF_MIN_PX` und mindestens so breit, dass alle Auffälligkeiten sichtbar sind
        (UI-23, :func:`pruefung_kern`), höchstens aber so breit, dass die Meldezeile
        :data:`_MELDE_MIN_PX` behält (UI-25); die Meldezeile kürzt Pfade mittig, sonst rechts. Beide
        Labels tragen den Volltext im Tooltip. Gemessen wird mit der Schrift der Labels, nicht
        mit dem Text, der gerade sichtbar ist.
        """
        fuss = self._fuss
        if fuss.width() <= 0:  # noch nicht angezeigt: nicht kürzen
            self.lbl_cursor.setze_platz(0)
            self.lbl_pruefung.setze_platz(0)
            return
        raender = self._fuss_layout.contentsMargins()
        abstand = self._fuss_layout.spacing()
        sichtbar = 3 if self.balken_export.isVisibleTo(fuss) else 2
        frei = (
            fuss.width()
            - raender.left()
            - raender.right()
            - abstand * (sichtbar - 1)
            - (self.balken_export.width() if sichtbar == 3 else 0)
        )
        voll = self.lbl_pruefung.volltext()
        zaehltext = voll.startswith("Prüfung: ")
        self.lbl_pruefung.setze_teile(zaehltext)  # Fehlertexte stehen rechts gekürzt
        prueft = self.lbl_pruefung.natuerliche_breite() + 4
        kern = self.lbl_pruefung.breite_von(pruefung_kern(voll)) + 4 if zaehltext else 0
        prueft = min(prueft, max(_PRUEF_MIN_PX, kern, frei - self.lbl_cursor.natuerliche_breite()))
        prueft = max(0, min(prueft, frei - _MELDE_MIN_PX))  # Kern hat eine Obergrenze (UI-25)
        self.lbl_pruefung.setFixedWidth(prueft)
        self.lbl_pruefung.setze_platz(prueft)
        self.lbl_cursor.setze_platz(frei - prueft)

    def _tab_reihenfolge(self) -> None:
        """AA → AC → AD → AE (Plot, Werkzeugleiste) → AF (Prüftext); AB ohne Fokus (Abschnitt 8)."""
        kette: list[QWidget] = [self.btn_oeffnen, self.btn_messung_hinzu]
        kette += self.messungsleiste.tab_kette()
        kette += [self.btn_export, self.btn_bild]
        kette += [self.btn_ansicht[nr] for nr in sorted(self.btn_ansicht)]
        kette.append(self.combo_kanalpaar)
        kette.append(self.liste_punkte)
        kette += list(self.chk.values())
        kette += [self.rb_groesse_cph, self.rb_groesse_ap]
        kette.append(self.rb_skala_db)
        kette += [self.auswahl_frf.chk_h1, self.auswahl_frf.chk_h2, self.auswahl_frf.chk_phase]
        kette += self.auswahl_sf.tab_kette()
        kette += self.auswahl_diagramm.tab_kette()
        kette += [self.tabelle_spitzen.tabelle, self.tabelle_baender.tabelle]
        kette += [self.btn_fehler_schliessen, self.btn_oeffnen_leer, self.liste_zuletzt]
        kette += self.achsenleiste.tab_kette()  # AD → AG → AE (Brief Abschnitt 6)
        kette += self.plot.tab_kette()
        kette.append(self.lbl_pruefung)
        for vorher, nachher in itertools.pairwise(kette):
            QWidget.setTabOrder(vorher, nachher)

    # --- Zugriff ---------------------------------------------------------------------------

    # --- Delegation an die aktive Messung (P-AUSW2 S4) --------------------------------------
    # Der bestehende Code (und die Tests) arbeiten weiter mit ``_geladen``, ``_cache`` usw.;
    # diese Eigenschaften lesen und schreiben die Felder der **aktiven** Messung.

    def _feld(self, name: str) -> Any:
        m = self._messungen.aktive
        return getattr(m, name) if m is not None else None

    def _setze_feld(self, name: str, wert: Any) -> None:
        m = self._messungen.aktive
        if m is None:
            if wert is None:
                return
            raise RuntimeError(f"Keine aktive Messung für {name}.")
        setattr(m, name, wert)

    @property
    def _geladen(self) -> Geladen | None:
        result: Geladen | None = self._feld("geladen")
        return result

    @_geladen.setter
    def _geladen(self, wert: Geladen | None) -> None:
        self._setze_feld("geladen", wert)

    @property
    def _cache(self) -> PaarCache | None:
        result: PaarCache | None = self._feld("cache")
        return result

    @_cache.setter
    def _cache(self, wert: PaarCache | None) -> None:
        self._setze_feld("cache", wert)

    @property
    def _datei_pfad(self) -> str | None:
        result: str | None = self._feld("pfad")
        return result

    @_datei_pfad.setter
    def _datei_pfad(self, wert: str | None) -> None:
        if wert is not None:
            self._setze_feld("pfad", wert)

    @property
    def _pruefung(self) -> PruefErgebnis | None:
        result: PruefErgebnis | None = self._feld("pruefung")
        return result

    @_pruefung.setter
    def _pruefung(self, wert: PruefErgebnis | None) -> None:
        self._setze_feld("pruefung", wert)

    @property
    def _pruef_fehler(self) -> str | None:
        result: str | None = self._feld("pruef_fehler")
        return result

    @_pruef_fehler.setter
    def _pruef_fehler(self, wert: str | None) -> None:
        self._setze_feld("pruef_fehler", wert)

    @property
    def _antrieb(self) -> tuple[str, str, Any] | None:
        result: tuple[str, str, Any] | None = self._feld("antrieb")
        return result

    @_antrieb.setter
    def _antrieb(self, wert: tuple[str, str, Any] | None) -> None:
        self._setze_feld("antrieb", wert)

    @property
    def messungen(self) -> Messungen:
        """Die geöffneten Messungen (Kurznamen, aktive Messung)."""
        return self._messungen

    @property
    def zustand(self) -> AuswertenZustand:
        """Keine Datei, Laden oder geladen."""
        return self._zustand

    @property
    def geladen(self) -> Geladen | None:
        """Die angezeigte Datei samt Einstellungen (``None`` = keine)."""
        return self._geladen

    @property
    def pruefung(self) -> PruefErgebnis | None:
        """Ergebnis von Stufe B (``None``, solange es nicht vorliegt)."""
        return self._pruefung

    @property
    def fehlertext(self) -> str | None:
        """Text des sichtbaren Fehlerbands (``None`` = kein Band)."""
        return self._fehlertext

    @property
    def ansicht(self) -> int:
        """Nummer der gewählten Ansicht (1 bis 4)."""
        return self._ansicht

    @property
    def auswahl(self) -> tuple[int | None, tuple[str, ...], Groesse, str]:
        """Auswahl von Ansicht 1: Punktindex (``None`` = Mittel), Komponenten, Größe, Skala."""
        a = self._auswahl
        return a.punkt, a.komponenten, a.groesse, a.skala

    def laeuft(self) -> bool:
        """Meldet, ob ein Hintergrundauftrag (Stufe A oder B) läuft."""
        return self._auftrag_a is not None or self._auftrag_b is not None or bool(self._zusatz)

    # --- Zustand ---------------------------------------------------------------------------

    @staticmethod
    def _setze(
        widget: QWidget,
        knopf: Knopf,
        normal: str = "",
        aktion: QAction | None = None,
        taste: str | None = None,
    ) -> None:
        widget.setEnabled(knopf.aktiv)
        if aktion is not None:
            aktion.setEnabled(knopf.aktiv)
        mit_taste = tooltip_mit_taste(normal, taste) if taste and normal else normal
        widget.setToolTip(mit_taste if knopf.aktiv else knopf.grund)

    def _bild_grund(self) -> str | None:
        """Grund, warum die gezeigte Ansicht kein Bild liefert (Platzhaltertext statt Plot)."""
        if self._zustand is AuswertenZustand.GELADEN and self._ansicht == 5:
            return TEXT_BILD_ANSICHT_5  # Bildstempel für mehrere Dateien: P-AUSW2 S9
        if self._zustand is AuswertenZustand.GELADEN and (
            self._ansichtstext is not None or self.plot.letzter_aufruf is None
        ):
            return TEXT_BILD_KEINE_DARSTELLUNG
        return None

    def _sync_knoepfe(self) -> None:
        """Aktivierung und Tooltips der Knöpfe und Aktionen (Zustand, Export, Ansicht)."""
        tabelle = bedienbarkeit_aktionen(
            bedienbarkeit_auswerten(self._zustand),
            export_laeuft=self._auftrag_c is not None,
            bild_grund=self._bild_grund(),
        )
        self._setze(
            self.btn_oeffnen, tabelle["oeffnen"], "Messdatei öffnen", self.act_oeffnen, "oeffnen"
        )
        self._setze(self.btn_oeffnen_leer, tabelle["oeffnen"])
        self._setze(self.btn_messung_hinzu, self._hinzu_knopf(), "Weitere Messdatei laden")
        self._setze(
            self.btn_export,
            tabelle["export"],
            "Auswertungsdaten exportieren",
            self.act_export,
            "export",
        )
        self._setze(
            self.btn_bild,
            tabelle["bild"],
            "Aktuelle Ansicht als Bild speichern",
            self.act_bild,
            "bild",
        )
        for nr, knopf in self.btn_ansicht.items():
            self._setze(
                knopf,
                tabelle[f"ansicht_{nr}"],
                ANSICHT_NAMEN[nr],
                self.act_ansicht[nr],
                f"ansicht_{nr}",
            )

    def _hinzu_knopf(self) -> Knopf:
        """Bedienbarkeit von ``Messung hinzufügen …`` (Brief K1-AUSW2 Abschnitt 4)."""
        if self._zustand is AuswertenZustand.LADEN:
            return Knopf(False, TEXT_HINZU_LAEDT)
        if self._geladen is None:
            return Knopf(False, TEXT_HINZU_ERST_DATEI)
        if self._messungen.ist_voll:
            return Knopf(False, TEXT_HINZU_VOLL)
        return Knopf(True)

    def _chips_aktualisieren(self) -> None:
        """Zeigt die Messungen als Chips (Zustand, aktive Messung, Speicherangabe) neu."""
        kette = self.messungsleiste.chip_ids()
        self.messungsleiste.setze(
            self._messungen, self._messungen.speicher_mib, gesperrt=self._ersetzte_messung()
        )
        if self.messungsleiste.chip_ids() != kette:
            self._tab_reihenfolge()  # Chips kamen hinzu oder fielen weg
        self._sync_knoepfe()

    def _ersetzte_messung(self) -> int | None:
        """Kennung der Messung, die „Öffnen …“ gerade ersetzt (sie lässt sich nicht entfernen)."""
        return self._ersetze_ziel if self._zustand is AuswertenZustand.LADEN else None

    def _wende_zustand_an(self) -> None:
        """Aktivierung, Tooltips und sichtbare Seite je Zustand (Brief Abschnitt 6)."""
        self._chips_aktualisieren()
        auswahl = bedienbarkeit_auswerten(self._zustand)["auswahl"]
        self._ad_inhalt.setEnabled(auswahl.aktiv)
        self.auswahlspalte.setToolTip("" if auswahl.aktiv else auswahl.grund)
        laedt = self._zustand is AuswertenZustand.LADEN
        hat_daten = self._geladen is not None
        self.laden_leiste.setVisible(laedt)
        self.plot.setEnabled(not laedt)
        self.tabellen.setEnabled(not laedt)
        self._ausgrauen(laedt and hat_daten)
        if self._zustand is AuswertenZustand.GELADEN or (laedt and hat_daten):
            self._zeige_ae_seite()
            self.lbl_plotkopf.setVisible(True)
        else:
            self._ae_stapel.setCurrentIndex(_SEITE_LEER)
            self.lbl_plotkopf.setVisible(False)
            self.plot_platzhalter.setVisible(not laedt)
            self.btn_oeffnen_leer.setVisible(not laedt)
            self.lbl_ziehen.setVisible(not laedt)
            self._fuelle_zuletzt(sichtbar=not laedt)

    def _zeige_ae_seite(self) -> None:
        """Plot (mit Tabellen in Ansicht 3) oder Platzhaltertext der Ansicht (Zone AE)."""
        if self._ansichtstext is not None:
            self.lbl_ansicht_platzhalter.setText(self._ansichtstext)
            self._ae_stapel.setCurrentIndex(_SEITE_TEXT)
        else:
            self._ae_stapel.setCurrentIndex(_SEITE_PLOT)
        self.tabellen.setVisible(self._ansicht == 3)
        self._sync_knoepfe()

    def _ausgrauen(self, grau: bool) -> None:
        """Zeigt die bisherige Darstellung ausgegraut, solange die neue Datei gelesen wird."""
        self._grau_effekt.setEnabled(grau)

    def _setze_zustand(self, zustand: AuswertenZustand) -> None:
        self._zustand = zustand
        self._wende_zustand_an()

    # --- Datei öffnen ----------------------------------------------------------------------

    def _waehle_datei(self) -> str | None:  # pragma: no cover - modaler Dateidialog
        """Öffnet den Dateidialog (Tests ersetzen diese Methode)."""
        pfad, _filter = QFileDialog.getOpenFileName(
            self, "Messdatei öffnen", self._letzter_ordner, DATEIFILTER_SVD
        )
        return pfad or None

    @contextmanager
    def _dialog(self) -> Iterator[None]:
        """Klammert modale Dialoge (Datei, Rückfrage, Kurzname).

        Die Ereignisschleife des Dialogs lässt die Abfrage weiterlaufen. Eine Zusatzmessung, die
        währenddessen fertig wird, bleibt bereit, wird aber nicht aktiviert (Aktivwechsel
        zurückgestellt, :meth:`_ergebnis_zusatz`); so bleibt die beim Klick aktive Messung die,
        die „Öffnen …“ ersetzt und anzeigt. Nach dem äußersten Dialog wird sie nachgeholt, sofern
        nicht „Öffnen …“ läuft (dann nach dessen Ende, :meth:`_aktiviere_nachgeladene`).
        """
        self._dialog_tiefe += 1
        try:
            yield
        finally:
            self._dialog_tiefe -= 1
            if (
                self._dialog_tiefe == 0
                and self._aktiviere_danach is not None
                and self._zustand is AuswertenZustand.GELADEN
            ):
                self._aktiviere_nachgeladene()

    def _oeffnen_geklickt(self) -> None:
        with self._dialog():
            aktive = self._messungen.aktive  # Ziel steht beim Klick fest, vor jedem Dialog
            ziel_id = aktive.id if aktive is not None else None
            pfad = self._waehle_datei()
            if pfad:
                self.oeffne_datei(pfad, ziel_id=ziel_id)

    def oeffne_datei(self, pfad: str, *, ziel_id: int | None = None) -> None:
        """Liest ``pfad`` im Hintergrund; laufende Aufträge werden abgebrochen (Job-ID).

        Parameters
        ----------
        pfad : str
            Pfad der ``.svd``-Datei.
        ziel_id : int, optional
            Die zu ersetzende Messung (beim Klick aktiv); ohne Angabe die jetzt aktive. Gibt es
            sie nicht mehr, kommt die Datei als neue Messung dazu.
        """
        with self._dialog():
            self._oeffne_datei(pfad, ziel_id)

    def _oeffne_datei(self, pfad: str, ziel_id: int | None) -> None:
        aktive = self._messungen.finde(ziel_id) if ziel_id is not None else self._messungen.aktive
        anzahl = self._serien_betroffen(aktive.id) if aktive is not None else 0
        if aktive is not None and anzahl:
            text = (
                f"Die Messung {aktive.kurzname} wird durch die neue Datei ersetzt. {anzahl} "
                f"{'Serie' if anzahl == 1 else 'Serien'} in Ansicht 5 "
                f"{'wird' if anzahl == 1 else 'werden'} mit entfernt."
            )
            if not self._bestaetige_ersetzen("Messung ersetzen", text):
                return
        self._abbrechen()
        self._job_id += 1
        self._ersetze_ziel = aktive.id if aktive is not None else None
        try:  # derselbe Rückfallschutz wie nach dem Lesen: kein hängendes „Laden“
            self._zeige_pruefung()  # abgebrochene Stufe B steht nicht mehr als „wird berechnet“
            self._letzter_ordner = str(Path(pfad).parent)
            self._einstellungen.merke_ordner(self._letzter_ordner)
            self.schliesse_fehlerband()
            self.lbl_laden.setText(lade_text(dateiname_von(pfad)))
            self._setze_zustand(AuswertenZustand.LADEN)
            auftrag = self._ausfuehrer.starte(lese_job, pfad)
        except Exception as fehler:  # Widgets oder Prozess (Spawn, Pipe): als Lesefehler zeigen
            self._lesefehler(f"{pfad}: {fehler}")
            return
        self._auftrag_a = (self._job_id, auftrag, pfad)
        self._timer.start()

    def schliesse_fehlerband(self) -> None:
        """Blendet das Fehlerband aus (Knopf „Schließen“)."""
        self._fehlertext = None
        self.band_fehler.setVisible(False)

    def _rueckfall(self, schritte: Sequence[tuple[str, Callable[[], object]]]) -> list[str]:
        """Führt Rückfallschritte einzeln aus; Fehler brechen nichts ab und gehen nicht verloren.

        Jede Ausnahme kommt mit Ablaufverfolgung ins Protokoll (``logging``, Logger dieses
        Moduls) und als Text „Schritt: Ausnahme“ in die Rückgabe, die an die Fehlermeldung
        angehängt wird (:func:`~ldv_automation.gui.anzeige_auswerten.folgefehler_text`).
        """
        fehler: list[str] = []
        for name, schritt in schritte:
            try:
                schritt()
            except Exception as exc:  # der Rückfallpfad selbst darf nicht scheitern
                _log.warning("Rückfall im Reiter Auswerten: %s fehlgeschlagen", name, exc_info=True)
                fehler.append(f"{name}: {exc}")
        return fehler

    def _lesefehler(self, text: str) -> None:
        """Zeigt das Fehlerband; die zuvor geladene Datei bleibt unverändert (UI-15).

        Auch dieser Pfad darf nicht scheitern: Der Zustand wird zuerst gesetzt (nie „Laden“ nach
        einer Ausnahme), danach folgen die Widgets einzeln; Ladeleiste und Abfrage werden in
        jedem Fall beendet. Fehler in den Rückfallschritten stehen im Protokoll und als Anhang
        in der Fehlermeldung.
        """
        self._fehlertext = fehler_band_text(text)
        self._zustand = (
            AuswertenZustand.GELADEN if self._geladen is not None else AuswertenZustand.KEINE_DATEI
        )
        folge = self._rueckfall(
            (
                ("Fehlerband (Text)", lambda: self.lbl_fehler.setText(self._fehlertext or "")),
                ("Fehlerband (sichtbar)", lambda: self.band_fehler.setVisible(True)),
                ("Ladeleiste", lambda: self.laden_leiste.setVisible(False)),
                ("Zustand anwenden", self._wende_zustand_an),
                ("Fußzeile Prüfung", self._zeige_pruefung),
            )
        )
        if folge:
            self._fehlertext += folgefehler_text(folge)
            self._rueckfall(
                (("Fehlerband (Anhang)", lambda: self.lbl_fehler.setText(self._fehlertext or "")),)
            )
        if (
            self._auftrag_a is None
            and self._auftrag_b is None
            and self._auftrag_c is None
            and not self._zusatz
        ):
            self._timer.stop()

    def _zeige_pruefung(self) -> None:
        """Fußzeile rechts: Prüfung der **angezeigten** Datei, nie ein veralteter Stand."""
        if self._geladen is None:
            text, grund = pruefung_text(()), ""
        elif self._pruefung is not None:
            text, grund = pruefung_text(self._pruefung.pruefungen), ""
        elif self._pruef_fehler is not None:
            text, grund = pruefung_fehler_text(self._pruef_fehler), self._pruef_fehler
        elif self._auftrag_b is not None:
            text, grund = TEXT_PRUEFUNG_BERECHNET, ""
        else:
            text, grund = TEXT_PRUEFUNG_ABGEBROCHEN, "Stufe B wurde vor dem Ende abgebrochen."
        self.lbl_pruefung.setText(text)
        self.lbl_pruefung.setze_zusatz_tooltip(grund)
        self._fuss_verteilen()

    # --- Hintergrundaufträge ---------------------------------------------------------------

    def _abbrechen(self) -> None:
        for eintrag in (self._auftrag_a, self._auftrag_b):
            if eintrag is not None:
                eintrag[1].abbrechen()
        self._auftrag_a = None
        self._auftrag_b = None
        self._b_messung = None
        if self._auftrag_c is None and not self._zusatz:  # Export und Zusatzladen laufen weiter
            self._timer.stop()

    def export_laeuft(self) -> bool:
        """Gibt ``True`` zurück, solange ein Export im Hintergrundprozess rechnet."""
        return self._auftrag_c is not None

    def beende(self) -> None:
        """Bricht laufende Aufträge (auch einen Export) ab und stoppt die Abfrage (Schließen)."""
        self._abbrechen()
        self._zusatz_abbrechen()
        if self._auftrag_c is not None:
            self._auftrag_c[0].abbrechen()
            self._auftrag_c = None
        self._timer.stop()

    def _abfrage(self) -> None:
        """Fragt laufende Aufträge ab; nur Ergebnisse der aktuellen Job-ID werden übernommen."""
        a = self._auftrag_a
        if a is not None:
            job, auftrag, pfad = a
            if job != self._job_id:
                auftrag.abbrechen()
                self._auftrag_a = None
            elif auftrag.fertig():
                self._auftrag_a = None
                self._ergebnis_a(job, auftrag, pfad)
        b = self._auftrag_b
        if b is not None:
            job, auftrag_b = b
            if job != self._job_id:
                auftrag_b.abbrechen()
                self._auftrag_b = None
            elif auftrag_b.fertig():
                self._auftrag_b = None
                self._ergebnis_b(auftrag_b)
        c = self._auftrag_c
        if c is not None and c[0].fertig():
            self._auftrag_c = None
            self._ergebnis_c(c[0])
        for messung_id, auftrag_z in list(self._zusatz.items()):
            if auftrag_z.fertig():
                del self._zusatz[messung_id]
                self._ergebnis_zusatz(messung_id, auftrag_z)
        if (
            self._auftrag_a is None
            and self._auftrag_b is None
            and self._auftrag_c is None
            and not self._zusatz
        ):
            self._timer.stop()

    def _ergebnis_a(self, job: int, auftrag: Auftrag, pfad: str) -> None:
        try:
            geladen = auftrag.ergebnis()
        except AuftragAbgebrochen:
            return
        except AuftragFehler as fehler:
            self._lesefehler(fehler.meldung)
            self._aktiviere_nachgeladene()
            return
        self._uebernehme(job, geladen, pfad)

    def _ergebnis_b(self, auftrag: Auftrag) -> None:
        """Stufe B fertig: Ergebnis gehört der Messung, für die sie gestartet wurde."""
        ziel = (
            self._messungen.finde(self._b_messung)
            if self._b_messung is not None
            else self._messungen.aktive
        )
        self._b_messung = None
        try:
            ergebnis = auftrag.ergebnis()
        except AuftragAbgebrochen:
            self._zeige_pruefung()
            return
        except AuftragFehler as fehler:
            if ziel is not None:
                ziel.pruef_fehler = fehler.meldung
            self._zeige_pruefung()
            return
        if ziel is None:  # Messung inzwischen entfernt
            return
        ziel.pruefung = ergebnis
        if ziel is self._messungen.aktive:
            self._zeige_pruefung()
            self._kennzeichen_aktualisieren()

    def _kennzeichen_aktualisieren(self) -> None:
        """Übernimmt die Annahmen aus Stufe B in Beschriftung und Darstellung (M8)."""
        if self._geladen is None:
            return
        if self._a4_geladen:
            self.auswahl_sf.setze_referenz_text(
                phase_ref_text(self._phase_referenz(), self._annahmen()),
                kennzeichen_beschreibung("phase", self._annahmen()),
            )
        self.auswahl_frf.setze_phase_erklaerung(kennzeichen_beschreibung("phase", self._annahmen()))
        if self._ansicht in (2, 4, 5):
            self._zeichne(zoom_behalten=True)

    def _verwerfe_datei(self) -> list[str]:
        """Setzt den Reiter in den Zustand „Keine Datei“ zurück (nach einem Fehler beim Aufbau).

        Der Rückfallpfad darf selbst nicht scheitern: Jeder Schritt läuft einzeln (siehe
        :meth:`_rueckfall`).

        Returns
        -------
        list of str
            Fehler der Rückfallschritte (leer, wenn alles gelang); der Aufrufer hängt sie an die
            Fehlermeldung an.
        """
        self._zusatz_abbrechen()
        self._messungen.leere()
        self._serien.leere()
        self._serien_aufgeloest.clear()
        self.auswahl_diagramm.zuruecksetzen()
        self._a4_letzt = None
        self._in_aufbau = True
        try:
            return self._rueckfall(
                (
                    ("Punktliste", self.liste_punkte.clear),
                    ("Darstellung", lambda: self._leere_plot(zoom_vergessen=True)),
                    ("Dateiname", lambda: self.lbl_datei.setText("–")),
                    ("Pfad", lambda: self.lbl_pfad.setText("")),
                    ("Plotkopf", lambda: self.lbl_plotkopf.setText("")),
                    ("Hinweise", lambda: self.lbl_hinweise.setText("")),
                    ("Parameterzeile", self._fuelle_parameter),
                )
            )
        finally:
            self._in_aufbau = False

    @staticmethod
    def _bereite_auf(
        geladen: Geladen,
    ) -> tuple[PaarCache, tuple[tuple[str, str], ...], tuple[str, str, Any] | None]:
        """Aufbereiten einer geladenen Datei: Cache, Kanalpaare und Antriebspunkt.

        Prüft nebenbei, dass Punktliste und Parameterzeile entstehen können; scheitert etwas, ist
        das ein Lesefehler (Aufrufer).
        """
        daten = geladen.messdaten
        cache = PaarCache(daten)
        punkt_eintraege(daten.punkte.label, daten.punkte.koordinaten_m)
        parameter_zellen(geladen.einstellungen)
        verfuegbare_groessen(daten, KOMPONENTEN)
        paare = kanalpaare(daten)
        return cache, paare, waehle_antriebspunkt(paare)

    def _uebernehme(self, job: int, geladen: Geladen, pfad: str) -> None:
        """Stufe A fertig (``Öffnen``): Ansicht 1 sofort zeigen, Stufe B im Hintergrund starten.

        Tempo (Nutzerentscheidung): Zielwert für den Erstaufbau und für jeden Wechsel von Punkt,
        Komponente, Größe oder Skala ist **unter 400 ms** (statt 100 ms im Brief); er ist am
        Messrechner zu messen. ``PaarCache`` und Zeichnen laufen bewusst im GUI-Thread, eine
        Verlagerung in den Hintergrund ist nicht vorgesehen.

        Die Datei ersetzt die aktive Messung (Kurzname bleibt, Serien der alten Messung
        entfallen), bei „Keine Datei“ ist sie die erste Messung. Scheitert die Aufbereitung
        (Cache, Punktliste, Parameterzeile, Auswahl), meldet der Reiter das wie einen Lesefehler
        (Fehlerband mit Pfad). Davor wird nichts am Reiter geändert, die bisherige Datei bleibt;
        scheitert es danach, geht der Reiter in „Keine Datei“.
        """
        try:
            cache, paare, antrieb = self._bereite_auf(geladen)
        except Exception as fehler:  # jede Ausnahme der Aufbereitung ist ein Lesefehler
            self._lesefehler(f"{pfad}: Auswertung nicht möglich: {fehler}")
            self._aktiviere_nachgeladene()
            return
        # Das Ziel ist fest an die beim Öffnen aktive Messung gebunden (nie die gerade aktive);
        # gibt es sie nicht mehr, kommt die Datei als neue Messung dazu.
        alt = self._messungen.finde(self._ersetze_ziel)
        self._ersetze_ziel = None
        if alt is None and self._messungen.ist_voll:
            self._lesefehler(f"{pfad}: Höchstens {MESSUNGEN_MAX} Messungen.")
            self._aktiviere_nachgeladene()
            return
        if alt is not None:
            self._messungen.ersetze(
                alt.id, pfad, geladen=geladen, cache=cache, antrieb=antrieb, paare=paare
            )
            self._serien_entfernen(alt.id)
        else:
            neu = self._messungen.hinzufuegen(pfad)
            self._messungen.fertig(
                neu.id, geladen=geladen, cache=cache, antrieb=antrieb, paare=paare
            )
        if not self._zeige_aktive(pfad, neue_datei=True):
            self._aktiviere_nachgeladene()
            return
        self._setze_meldung(geladen_text(pfad))
        self._einstellungen.merke_datei(pfad)
        self._setze_zustand(AuswertenZustand.GELADEN)
        self._zeichne()
        if not self._aktiviere_nachgeladene():
            self._starte_pruefung(job)

    def _aktiviere_nachgeladene(self) -> bool:
        """Aktiviert eine Messung, die während „Öffnen …“ fertig wurde (nach dessen Ende).

        Returns
        -------
        bool
            ``True``, wenn eine Messung aktiviert wurde (sie startet die Prüfung selbst).
        """
        ziel_id, self._aktiviere_danach = self._aktiviere_danach, None
        messung = self._messungen.finde(ziel_id)
        if (
            messung is None
            or messung is self._messungen.aktive
            or messung.zustand is not MessungsZustand.BEREIT
            or self._zustand is not AuswertenZustand.GELADEN
        ):
            return False
        self._aktiviere_messung(messung.id)
        return self._messungen.aktive is messung

    def _zeige_aktive(self, pfad: str, *, neue_datei: bool) -> bool:
        """Zeigt die aktive Messung in AD, AB, AA und Plot (Ansicht, Auswahl zurückgesetzt).

        Parameters
        ----------
        pfad : str
            Pfad der aktiven Messung (für die Fehlermeldung).
        neue_datei : bool
            ``True`` bei ``Öffnen``: Bereiche der Achsen zurück (UI-6) und Ansicht 1. ``False``
            beim Wechsel der aktiven Messung: Achsenbereiche und Ansicht bleiben (UI-3).

        Returns
        -------
        bool
            ``False``, wenn der Aufbau scheiterte (Fehlerband steht, Reiter ohne Datei).
        """
        messung = self._messungen.aktive
        assert messung is not None and messung.geladen is not None
        daten = messung.geladen.messdaten
        eintraege = punkt_eintraege(daten.punkte.label, daten.punkte.koordinaten_m)
        zellen = parameter_zellen(messung.geladen.einstellungen)
        self._a4_wunsch_hz = None
        if neue_datei:
            self.plot.neue_datei()  # Bereiche zurück, Skalen bleiben (UI-6, R-073)
        self.plot.fadenkreuz.vergiss()
        self._a4_letzt = None
        self._a4_komponente = None
        ansicht = 1 if neue_datei else self._ansicht
        self._in_aufbau = True
        try:
            self.liste_punkte.clear()
            self.liste_punkte.addItems(eintraege)
            self.liste_punkte.setCurrentRow(0)
            self._paare = messung.paare
            self._spitze = None
            self._a3_schluessel = None
            self._a4_geladen = False
            self._a4_paar_schluessel = None
            self.combo_kanalpaar.clear()
            for antwort, referenz in messung.paare:
                self.combo_kanalpaar.addItem(kanalpaar_text(antwort, referenz))
            self.auswahl_frf.zuruecksetzen()
            self.auswahl_frf.setze_phase_erklaerung(
                kennzeichen_beschreibung("phase", Annahmen().eintraege())
            )
            self.btn_ansicht[ansicht].setChecked(True)
            self._aktiviere_ansicht(ansicht)
            for kasten in self.chk.values():
                kasten.setChecked(True)
            self.rb_groesse_cph.setChecked(True)
            self._aktualisiere_groessen()
            self._auswahl = self._lese_auswahl()
            self.lbl_datei.setText(messung.dateiname)
            self.lbl_pfad.setText(messung.pfad)
            self.parameterzeile.setze_zellen(zellen)
        except Exception as fehler:  # Qt-Aufbau schlägt fehl: nichts halb geladen stehen lassen
            self._in_aufbau = False
            folge = self._verwerfe_anzeige(messung)
            self._lesefehler(f"{pfad}: Anzeige nicht möglich: {fehler}" + folgefehler_text(folge))
            return False
        finally:
            self._in_aufbau = False
        return True

    def _verwerfe_anzeige(self, messung: Messung) -> list[str]:
        """Anzeigefehler einer Messung: nur diese wird verworfen, die übrigen bleiben.

        Gibt es keine weitere bereite Messung, geht der Reiter in „Keine Datei“
        (:meth:`_verwerfe_datei`); sonst wird die nun aktive Messung gezeigt.

        Returns
        -------
        list of str
            Fehler der Rückfallschritte (der Aufrufer hängt sie an die Meldung an).
        """
        self._serien_entfernen(messung.id)
        self._messungen.entferne(messung.id)
        if self._b_messung == messung.id and self._auftrag_b is not None:
            self._auftrag_b[1].abbrechen()
            self._auftrag_b = None
            self._b_messung = None
        rest = self._messungen.aktive
        if rest is None:
            return self._verwerfe_datei()
        folge = self._rueckfall(
            (
                ("Anzeige der übrigen Messung", lambda: self._zeige_rest(rest)),
                ("Chips", self._chips_aktualisieren),
            )
        )
        return folge

    def _zeige_rest(self, rest: Messung) -> None:
        """Zeigt die nach einem Anzeigefehler verbliebene aktive Messung."""
        if self._zeige_aktive(rest.pfad, neue_datei=False):
            self._zeichne()
            self._starte_pruefung(self._job_id)

    def _starte_pruefung(self, job: int) -> None:
        """Startet Stufe B für die aktive Messung, wenn noch kein Ergebnis vorliegt.

        Höchstens ein Auftrag gleichzeitig; der Wechsel der aktiven Messung bricht den laufenden
        ab (:meth:`_aktiviere_messung`).
        """
        messung = self._messungen.aktive
        if messung is None or messung.geladen is None:
            return
        if self._auftrag_b is not None:
            if self._b_messung == messung.id:
                return  # läuft schon für diese Messung
            self._auftrag_b[1].abbrechen()  # nie einen laufenden Auftrag verwaist überschreiben
            self._auftrag_b = None
            self._b_messung = None
        if messung.pruefung is not None or messung.pruef_fehler is not None:
            self._zeige_pruefung()
            return
        herkunft = messung.geladen.messdaten.herkunft
        sha = herkunft.sha256 if herkunft is not None else None
        try:
            auftrag = self._ausfuehrer.starte(pruef_job, messung.pfad, sha, messung.antrieb)
        except Exception as fehler:  # Prozess nicht startbar: Prüfung nicht möglich
            messung.pruef_fehler = str(fehler)
            self._zeige_pruefung()
            return
        self._auftrag_b = (job, auftrag)
        self._b_messung = messung.id
        self._zeige_pruefung()
        self._timer.start()

    # --- Weitere Messungen (R-058, P-AUSW2 S5) -------------------------------------------------

    def _serien_entfernen(self, messung_id: int) -> None:
        """Entfernt die Serien von Ansicht 5, die zu einer entfallenen Messung gehören."""
        self._serien.entferne_messung(messung_id)
        self._serien_aufgeloest = {
            k: v for k, v in self._serien_aufgeloest.items() if k[0] != messung_id
        }

    def _serien_betroffen(self, messung_id: int) -> int:
        """Zahl der Serien in Ansicht 5, die zu der Messung gehören (UI-14)."""
        return self._serien.betroffene(messung_id)

    def _zusatz_abbrechen(self) -> None:
        """Bricht alle Ladeaufträge zusätzlicher Messungen ab (Schließen, Rückfallpfad)."""
        for auftrag in self._zusatz.values():
            auftrag.abbrechen()
        self._zusatz.clear()

    def _messung_hinzu_geklickt(self) -> None:
        with self._dialog():
            pfad = self._waehle_datei()
            if pfad:
                self.messung_hinzufuegen(pfad)

    def messung_hinzufuegen(self, pfad: str) -> None:
        """Lädt eine weitere ``.svd`` im Hintergrund als zusätzliche Messung (R-058).

        Die Oberfläche bleibt bedienbar; die Messung erscheint sofort als Chip „lädt …“, wird nach
        dem Laden aktiv und bleibt bis dahin für Serien unwählbar. Es lädt höchstens eine Messung
        gleichzeitig, weitere warten (Speicherspitze). Ohne geladene Datei, während ``Öffnen``
        läuft oder bei erreichter Höchstzahl (:data:`~ldv_automation.gui.messungen.MESSUNGEN_MAX`)
        passiert nichts.

        Parameters
        ----------
        pfad : str
            Pfad der ``.svd``-Datei (dieselbe Datei zweimal ist erlaubt, Hinweis in AF).
        """
        if not self._hinzu_knopf().aktiv:
            return
        self._messungen.hinzufuegen(pfad)
        self._letzter_ordner = str(Path(pfad).parent)
        self._einstellungen.merke_ordner(self._letzter_ordner)
        self.schliesse_fehlerband()
        self._starte_naechsten()
        self._chips_aktualisieren()

    def _starte_naechsten(self) -> None:
        """Startet den Ladeauftrag der nächsten wartenden Messung (höchstens einer gleichzeitig)."""
        messung = self._messungen.naechster_ladeauftrag()
        if messung is None:
            return
        messung.gestartet = True
        try:
            auftrag = self._ausfuehrer.starte(lese_job, messung.pfad)
        except Exception as fehler:  # Prozess nicht startbar: wie ein Lesefehler der Datei
            self._messungen.entferne(messung.id)
            self._zusatz_fehler(f"{messung.pfad}: {fehler}")
            self._starte_naechsten()
            return
        self._zusatz[messung.id] = auftrag
        self._timer.start()

    def _zusatz_fehler(self, text: str) -> None:
        """Fehlerband für eine zusätzliche Messung; die bisherigen Messungen bleiben unverändert."""
        self._fehlertext = fehler_band_text(text)
        folge = self._rueckfall(
            (
                ("Fehlerband (Text)", lambda: self.lbl_fehler.setText(self._fehlertext or "")),
                ("Fehlerband (sichtbar)", lambda: self.band_fehler.setVisible(True)),
                ("Chips", self._chips_aktualisieren),
            )
        )
        if folge:
            self._fehlertext += folgefehler_text(folge)
            self._rueckfall(
                (("Fehlerband (Anhang)", lambda: self.lbl_fehler.setText(self._fehlertext or "")),)
            )

    def _ergebnis_zusatz(self, messung_id: int, auftrag: Auftrag) -> None:
        """Stufe A einer zusätzlichen Messung fertig: aufbereiten, bereit machen, aktivieren."""
        messung = self._messungen.finde(messung_id)
        if messung is None:  # in der Zwischenzeit entfernt
            self._starte_naechsten()
            return
        try:
            geladen = auftrag.ergebnis()
            cache, paare, antrieb = self._bereite_auf(geladen)
        except AuftragAbgebrochen:
            self._messungen.entferne(messung_id)
        except AuftragFehler as fehler:
            self._messungen.entferne(messung_id)
            self._zusatz_fehler(fehler.meldung)
        except Exception as fehler:  # Aufbereitung scheitert wie beim Öffnen: Lesefehler
            self._messungen.entferne(messung_id)
            self._zusatz_fehler(f"{messung.pfad}: Auswertung nicht möglich: {fehler}")
        else:
            gleiche = next(
                (
                    m
                    for m in self._messungen.bereite()
                    if m.sha256 is not None and m.sha256 == _sha_von(geladen)
                ),
                None,
            )
            self._messungen.fertig(
                messung_id, geladen=geladen, cache=cache, antrieb=antrieb, paare=paare
            )
            self._starte_naechsten()
            if self._zustand is AuswertenZustand.GELADEN and not self._dialog_tiefe:
                self._aktiviere_messung(messung_id)
            else:  # Dialog offen oder „Öffnen …“ läuft: aktiv wird sie danach
                self._aktiviere_danach = messung_id
                self._chips_aktualisieren()
            if gleiche is not None:
                self._setze_meldung(
                    f"{t.symbol('warnung')} "
                    + TEXT_DIESELBE_DATEI.format(kurzname=gleiche.kurzname)
                )
            return
        self._starte_naechsten()
        self._chips_aktualisieren()

    def _aktiviere_messung(self, messung_id: int) -> None:
        """Macht eine bereite Messung zur aktiven (Chip-Klick, nach dem Laden).

        Achsenbereiche, Skalen und Ansicht bleiben (UI-3); Auswahl in AD und Tabellen werden wie
        bei einer neuen Datei zurückgesetzt. Stufe B läuft nur für die aktive Messung: ein
        laufender Auftrag der bisherigen wird abgebrochen und verworfen.
        """
        messung = self._messungen.finde(messung_id)
        if (
            messung is None
            or messung.zustand is not MessungsZustand.BEREIT
            or self._zustand is not AuswertenZustand.GELADEN
        ):
            return
        if messung is self._messungen.aktive:
            self._chips_aktualisieren()
            return
        if self._auftrag_b is not None:
            self._auftrag_b[1].abbrechen()
            self._auftrag_b = None
            self._b_messung = None
        self._messungen.setze_aktiv(messung_id)
        if not self._zeige_aktive(messung.pfad, neue_datei=False):
            return
        self._setze_meldung(f"Messung {messung.kurzname} aktiv: {messung.dateiname}")
        self._chips_aktualisieren()
        self._zeichne()
        self._starte_pruefung(self._job_id)

    def _bestaetige_entfernen(self, titel: str, text: str) -> bool:  # pragma: no cover - modal
        """Fragt vor dem Entfernen einer Messung mit Serien nach (Tests ersetzen die Methode)."""
        return self._frage_bestaetigung(titel, text, "Entfernen")

    def _bestaetige_ersetzen(self, titel: str, text: str) -> bool:  # pragma: no cover - modal
        """Fragt vor „Öffnen …“ nach, wenn Serien der ersetzten Messung entfallen (UI-14)."""
        return self._frage_bestaetigung(titel, text, "Ersetzen")

    def _frage_bestaetigung(self, titel: str, text: str, ja_text: str) -> bool:  # pragma: no cover
        """Modale Frage mit deutschen Knöpfen; Standard und Esc sind „Abbrechen“."""
        box, ja = frage(self, titel, text, ja_text, "Abbrechen", ja_gefahr=True)
        box.exec()
        return box.clickedButton() is ja

    def _frage_kurzname(self, aktuell: str, grund: str) -> str | None:  # pragma: no cover - modal
        """Fragt einen neuen Kurznamen ab (Tests ersetzen die Methode); ``None`` = abgebrochen."""
        text, ok = QInputDialog.getText(
            self, "Kurzname ändern", grund or "Kurzname der Messung:", text=aktuell
        )
        return text if ok else None

    def _entfernen_gesperrt(self, messung_id: int) -> bool:
        """Sperre für die Messung, die „Öffnen …“ gerade ersetzt (mit Meldung in AF)."""
        if messung_id != self._ersetzte_messung():
            return False
        messung = self._messungen.finde(messung_id)
        kurzname = messung.kurzname if messung is not None else ""
        self._setze_meldung(TEXT_ENTFERNEN_ERSETZT.format(kurzname=kurzname))
        return True

    def _entferne_geklickt(self, messung_id: int) -> None:
        """Entfernen-Knopf oder Entf am Chip: bei betroffenen Serien erst nachfragen (UI-14)."""
        messung = self._messungen.finde(messung_id)
        if messung is None:
            return
        if self._entfernen_gesperrt(messung_id):
            return
        anzahl = self._serien_betroffen(messung_id)
        if anzahl:
            text = (
                f"Die Messung {messung.kurzname} wird entfernt. {anzahl} "
                f"{'Serie' if anzahl == 1 else 'Serien'} in Ansicht 5 "
                f"{'wird' if anzahl == 1 else 'werden'} mit entfernt."
            )
            with self._dialog():
                if not self._bestaetige_entfernen("Messung entfernen", text):
                    return
        self.entferne_messung(messung_id)

    def entferne_messung(self, messung_id: int) -> None:
        """Entfernt eine Messung samt ihren Serien (ohne Rückfrage; die Rückfrage steht davor).

        War sie aktiv, rückt die vorige bereite Messung nach; war es die letzte, geht der Reiter
        in „Keine Datei“. Ladende Messungen werden abgebrochen.
        """
        messung = self._messungen.finde(messung_id)
        if messung is None or self._entfernen_gesperrt(messung_id):
            return
        war_aktiv = messung is self._messungen.aktive
        laufend = self._zusatz.pop(messung_id, None)
        if laufend is not None:
            laufend.abbrechen()
        if self._b_messung == messung_id and self._auftrag_b is not None:
            self._auftrag_b[1].abbrechen()
            self._auftrag_b = None
            self._b_messung = None
        if self._aktiviere_danach == messung_id:
            self._aktiviere_danach = None
        self._messungen.entferne(messung_id)
        self._serien_entfernen(messung_id)
        neu = self._messungen.aktive
        if war_aktiv and neu is None:
            self._abbrechen()  # kein Auftrag darf nach „Keine Datei“ weiterlaufen
            self._verwerfe_datei()  # leert Anzeige, bricht die übrigen Ladeaufträge ab
            self.schliesse_fehlerband()
            self._setze_zustand(AuswertenZustand.KEINE_DATEI)
            self._zeige_pruefung()
            return
        if war_aktiv and neu is not None:
            if not self._zeige_aktive(neu.pfad, neue_datei=False):
                return
            self._setze_meldung(f"Messung {neu.kurzname} aktiv: {neu.dateiname}")
            self._zeichne()
            self._starte_pruefung(self._job_id)
        elif self._ansicht == 5:
            self._zeichne()
        self._starte_naechsten()
        self._chips_aktualisieren()

    def _umbenennen_geklickt(self, messung_id: int) -> None:
        """Doppelklick am Chip: Kurzname ändern (Pflicht, eindeutig), Meldung bei Fehler."""
        messung = self._messungen.finde(messung_id)
        if messung is None:
            return
        grund = ""
        while True:
            with self._dialog():
                neu = self._frage_kurzname(messung.kurzname, grund)
            if neu is None:
                return
            fehler = self._messungen.umbenennen(messung_id, neu)
            if fehler is None:
                break
            grund = f"{t.symbol('fehler')} {fehler}"
            if not self._wiederhole_kurzname():
                self._setze_meldung(grund)
                return
        self._chips_aktualisieren()
        if self._ansicht == 5:
            self._zeichne()

    def _wiederhole_kurzname(self) -> bool:  # pragma: no cover - modal
        """Nach einem ungültigen Kurznamen erneut fragen (Tests ersetzen die Methode)."""
        return True

    # --- Meldungen und Cursor ----------------------------------------------------------------

    def _setze_meldung(self, text: str, pfade: Sequence[str] = ()) -> None:
        """Zeigt die letzte Aktion in der Meldezeile (links in AF); ein Cursortext weicht ihr.

        Zu lange Meldungen werden gekürzt (``pfade`` mittig, sonst rechts mit „…“); der
        Volltext steht immer im Tooltip und in ``accessibleDescription`` des Labels.
        """
        self._meldung = text
        self._meldung_pfade = tuple(pfade)
        self._cursor_aktiv = False
        self.lbl_cursor.setText(text, pfade)
        self._fuss_verteilen()

    def _zeige_cursor(self, zusatz: str = "") -> None:
        """Cursorzeile (Ansichten 1 bis 3, Werte aus den Daten); Ansicht 4 zeigt die Meldung."""
        aufruf = self.plot.letzter_aufruf
        k = self.plot.fadenkreuz.index
        if aufruf is None or k is None:  # z. B. Ansicht 4: kein Cursor, die Meldung kehrt zurück
            if self._cursor_aktiv:
                self._setze_meldung(self._meldung, self._meldung_pfade)
            return
        ansicht, daten, optionen = aufruf
        text = cursor_zeile(ansicht.value, daten, optionen, k, kanal=self._kanal_a3)
        if text is None:
            if self._cursor_aktiv:
                self._setze_meldung(self._meldung, self._meldung_pfade)
            return
        self._cursor_aktiv = True
        self.lbl_cursor.setText(text + zusatz)
        self._fuss_verteilen()

    def _cursor_bewegt(self, _f_hz: float) -> None:
        self._zeige_cursor()

    def _plot_geklickt(self, f_hz: float) -> None:
        """Klick oder Enter im Plot: Frequenz der Schwingform (Ansicht 4) auf die Linie setzen."""
        if self._geladen is None:
            return
        if self._a4_geladen:
            self.auswahl_sf.setze_frequenz(f_hz, melden=self._ansicht == 4)
        else:
            self._a4_wunsch_hz = f_hz
        self._zeige_cursor(f" · {t.symbol('fertig')} Frequenz der Schwingform gesetzt")

    # --- Export, Bild, Prüfdialog, Zuletzt ---------------------------------------------------

    def _waehle_export_ziel(self, vorschlag: str) -> str | None:  # pragma: no cover - Dialog
        """Dateidialog des Exports; ohne Rückfrage zum Überschreiben (das prüft der Kern)."""
        pfad, _filter = QFileDialog.getSaveFileName(
            self,
            "Auswertungsdaten exportieren",
            vorschlag,
            DATEIFILTER_EXPORT,
            options=QFileDialog.Option.DontConfirmOverwrite,
        )
        return pfad or None

    def _waehle_bild_ziel(self, vorschlag: str) -> str | None:  # pragma: no cover - Dialog
        """Dateidialog für PNG oder PDF; ergänzt eine fehlende Endung nach dem Filter."""
        pfad, filter_text = QFileDialog.getSaveFileName(
            self, "Bild speichern", vorschlag, DATEIFILTER_BILD
        )
        return bild_endung(pfad, filter_text) if pfad else None

    def _zeige_warnung(self, titel: str, text: str) -> None:  # pragma: no cover - modal
        """Meldungsfenster mit dem Text des Rechenkerns (Tests ersetzen diese Methode)."""
        QMessageBox.warning(self, titel, text)

    def _fuehre_aus(self, dialog: QDialog) -> int:  # pragma: no cover - modale Schleife
        """Führt einen Dialog modal aus (Tests ersetzen diese Methode)."""
        return int(dialog.exec())

    def _export_geklickt(self) -> None:
        """``Daten exportieren …`` als Auftrag C (UI-16): Ziel prüfen, im Hintergrund rechnen."""
        if self._zustand is not AuswertenZustand.GELADEN or self._datei_pfad is None:
            return
        if self._auftrag_c is not None or self._geladen is None:
            return
        # Der Vorschlag gehört zur **angezeigten** Messdatei (Brief 7), nicht zum Öffnen-Ordner.
        gewaehlt = self._waehle_export_ziel(export_vorschlag(self._datei_pfad))
        if not gewaehlt:
            return
        basis = export_basis(gewaehlt)
        if not self._raeume_ziel_auf(Path(basis)):
            return
        try:
            pruefe_ziel(Path(basis), False)  # Überschreibschutz des Kerns, vor dem Start
        except (FileExistsError, FileNotFoundError) as fehler:
            self._zeige_warnung("Export nicht möglich", str(fehler))
            self._setze_meldung(f"{t.symbol('fehler')} {fehler} {self._export_notiz}".rstrip())
            return
        herkunft = self._geladen.messdaten.herkunft
        sha = herkunft.sha256 if herkunft is not None else None
        try:
            auftrag = self._ausfuehrer.starte(
                export_job, self._datei_pfad, basis, sha, None, False, self._antrieb
            )
        except Exception as fehler:  # Prozess nicht startbar
            self._zeige_warnung("Export nicht möglich", str(fehler))
            self._setze_meldung(f"{t.symbol('fehler')} Export nicht gestartet: {fehler}")
            return
        self._auftrag_c = (auftrag, basis)
        self.balken_export.setVisible(True)
        laeuft = "Export läuft … Die Auswertung wird neu berechnet."
        self._setze_meldung(f"{laeuft} {self._export_notiz}".rstrip())
        self._sync_knoepfe()
        self._timer.start()

    def _raeume_ziel_auf(self, basis: Path) -> bool:
        """Entfernt verwaiste Zwischendateien eines früheren Exports und meldet sie.

        Die Kern-Funktion kennt die Namen der Zwischendateien (``.<basis>.npz.tmp``,
        ``.<basis>.json.tmp``). Eine einzelne ``.npz`` ohne ``.json`` bleibt (sie ist ein Ziel,
        kein Zwischenstand) und wird gemeldet; der Export startet dann nicht.

        Returns
        -------
        bool
            ``True``, wenn der Export weiterlaufen darf.
        """
        self._export_notiz = ""
        try:
            entfernt = entferne_verwaiste_tmp(basis)
        except OSError as fehler:
            text = f"Verwaiste Zwischendatei nicht entfernbar: {fehler}"
            self._zeige_warnung("Export nicht möglich", text)
            self._setze_meldung(f"{t.symbol('fehler')} {text}")
            return False
        if entfernt:
            namen = ", ".join(p.name for p in entfernt)
            self._export_notiz = (
                f"{t.symbol('warnung')} Reste eines abgebrochenen Exports entfernt: {namen}"
            )
        halb = unvollstaendiger_export(basis)
        if halb is not None:
            text = (
                f"Unvollständiger früherer Export: {halb} hat keine .json-Datei (abgebrochener "
                "Export?). Die Datei wurde nicht verändert; bitte prüfen und löschen oder einen "
                "anderen Namen wählen."
            )
            self._zeige_warnung("Export nicht möglich", text)
            self._setze_meldung(f"{t.symbol('fehler')} {text}", (str(halb),))
            return False
        return True

    def _ergebnis_c(self, auftrag: Auftrag) -> None:
        self.balken_export.setVisible(False)
        try:
            npz, js = auftrag.ergebnis()
        except AuftragAbgebrochen:
            self._setze_meldung("Export abgebrochen.")
        except AuftragFehler as fehler:
            self._zeige_warnung("Export fehlgeschlagen", fehler.meldung)
            self._setze_meldung(f"{t.symbol('fehler')} Export fehlgeschlagen: {fehler.meldung}")
        else:
            self._setze_meldung(
                export_meldung(str(npz), str(js), self._export_notiz), (str(npz), str(js))
            )
        self._export_notiz = ""
        self._sync_knoepfe()

    def _bild_geklickt(self) -> None:
        """``Bild speichern …`` (UI-17): Arbeitsbild mit Stempel, Zoom übernommen."""
        if self._zustand is not AuswertenZustand.GELADEN or self._datei_pfad is None:
            return
        if self._bild_grund() is not None:
            return
        gewaehlt = self._waehle_bild_ziel(bild_vorschlag(self._datei_pfad, self._ansicht))
        if not gewaehlt:
            return
        aufruf = self.plot.letzter_aufruf
        assert aufruf is not None  # _bild_grund() hat die leere Fläche ausgeschlossen
        ansicht, daten, optionen = aufruf
        git_hash, geaendert = self._git_hash()
        stempel = baue_stempel(
            dateiname=dateiname_von(self._datei_pfad),
            ansicht=stempel_ansicht(self._ansicht),
            git_hash=git_hash_text(git_hash, geaendert),
            unbestaetigt=bild_unbestaetigt(ansicht.value, daten, optionen, self._annahmen()),
            warn_symbol=t.symbol("warnung"),
        )
        try:
            self.plot.speichere(Path(gewaehlt), stempel)
        except Exception as fehler:  # Zeichnen oder Schreiben: nichts verschlucken
            self._zeige_warnung("Bild nicht gespeichert", str(fehler))
            self._setze_meldung(f"{t.symbol('fehler')} Bild nicht gespeichert: {fehler}")
            return
        self._setze_meldung(bild_meldung(gewaehlt), (gewaehlt,))

    def _zeige_pruefdialog(self) -> None:
        """Klick auf die Prüfzusammenfassung: schreibgeschützte Liste P-01 bis P-11 (UI-23)."""
        if self._geladen is None:
            return
        pruefungen = self._pruefung.pruefungen if self._pruefung is not None else ()
        zeilen = pruefdialog_zeilen(pruefungen)
        dialog = PruefDialog(
            self.lbl_pruefung.volltext(),
            zeilen,
            TEXT_PRUEFUNG_NOCH_NICHT,
            start_zeile=erste_auffaellige_zeile(pruefungen),
            parent=self,
        )
        self._fuehre_aus(dialog)

    def _fuelle_zuletzt(self, *, sichtbar: bool) -> None:
        """Füllt „Zuletzt geöffnet“ im Zustand „Keine Datei“ (höchstens fünf Einträge)."""
        eintraege = self._einstellungen.zuletzt()
        self.liste_zuletzt.clear()
        for pfad in eintraege:
            vorhanden = Path(pfad).is_file()
            item = QListWidgetItem(zuletzt_eintrag(pfad, vorhanden=vorhanden))
            item.setData(Qt.ItemDataRole.UserRole, pfad)
            item.setToolTip(pfad)
            item.setSizeHint(QSize(0, ZEILENHOEHE_PX))
            if not vorhanden:  # gesperrt, aber lesbar (Kontrast ≥ 4,5:1, UI-23)
                item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEnabled)
                item.setForeground(QColor(t.C_NICHT_GEFUNDEN))
            self.liste_zuletzt.addItem(item)
        rahmen = 2 * self.liste_zuletzt.frameWidth()
        self.liste_zuletzt.setFixedHeight(max(len(eintraege), 1) * ZEILENHOEHE_PX + rahmen)
        self.lbl_zuletzt.setText("Zuletzt geöffnet" if eintraege else TEXT_KEINE_ZULETZT)
        self.liste_zuletzt.setVisible(bool(eintraege))
        self.zuletzt_gruppe.setVisible(sichtbar)

    def _zuletzt_aktiviert(self, item: QListWidgetItem) -> None:
        pfad = item.data(Qt.ItemDataRole.UserRole)
        if isinstance(pfad, str):
            self.oeffne_datei(pfad)

    # --- Parameterzeile --------------------------------------------------------------------

    def _fuelle_parameter(self) -> None:
        einstellungen = self._geladen.einstellungen if self._geladen is not None else None
        self.parameterzeile.setze_zellen(parameter_zellen(einstellungen))

    # --- Ansicht 1 -------------------------------------------------------------------------

    def _aktiviere_ansicht(self, nr: int) -> None:
        """Schaltet Auswahlseite und gemeinsame Elemente der Ansicht ``nr`` (1 bis 4) um."""
        self._ansicht = nr
        self.achsenleiste.setze_ansicht(nr)  # Ansicht 4 hat keine Achsenleiste
        self._ad_stapel.setCurrentIndex(nr - 1)
        for i, seite in enumerate(self._ad_seiten):  # der Stapel misst nur die aktuelle Seite
            seite.setSizePolicy(
                QSizePolicy.Policy.Preferred,
                QSizePolicy.Policy.Preferred if i == nr - 1 else QSizePolicy.Policy.Ignored,
            )
        self.kanalpaar_gruppe.setVisible(nr in (2, 3, 4) and len(self._paare) > 1)
        self.lbl_kanalpaar_hinweis.setText(TEXT_KANALPAAR_ANSICHT_4 if nr == 4 else "")
        self.lbl_kanalpaar_hinweis.setVisible(nr == 4)
        self.punkt_gruppe.setVisible(nr in (1, 2))
        self.tabellen.setVisible(nr == 3)
        self._plot_seite.refresh()  # Plot hat vor dem Zeichnen seine endgültige Größe (pt-Maße)
        if nr == 3:
            self._splitter_anwenden()
            # Qt verteilt die Höhen nach dem Einblenden der Tabelle noch einmal: danach erneut.
            QTimer.singleShot(0, self._splitter_nachziehen)

    def resizeEvent(self, event: QResizeEvent) -> None:  # noqa: N802  # Qt-Name
        """Schaltet bei schmalem Fenster (< :data:`KOMPAKT_BREITE_PX`) auf kompakte Anzeige."""
        super().resizeEvent(event)
        self._setze_kompakt(event.size().width() < KOMPAKT_BREITE_PX)

    def _setze_kompakt(self, kompakt: bool) -> None:
        """Kompakte Anzeige: Dateiname neben den Chips weg, kurze Achsenbeschriftungen."""
        if kompakt == self._kompakt:
            return
        self._kompakt = kompakt
        self._namen_box.setVisible(not kompakt)
        self.achsenleiste.setze_kompakt(kompakt)
        self.auswahl_diagramm.setze_kompakt(kompakt)
        self._plot_spalte.setMinimumHeight(self._plot_min_hoehe())

    def _plot_min_hoehe(self) -> int:
        """Mindesthöhe des Plotbereichs: Plot (:data:`PLOT_MIN_HOEHE_SPLITTER_PX`) plus Leiste.

        Die Achsenleiste liegt über der Plotfläche und bricht bei Platzmangel um; sie braucht
        ihre Höhe vollständig (Brief K1-AUSW2: zuerst schrumpft der Plot, nie die Leiste).
        """
        leiste = self.achsenleiste
        if not leiste.isVisibleTo(self):
            return PLOT_MIN_HOEHE_SPLITTER_PX
        layout = leiste.layout()
        breite = self._plot_spalte.width() or leiste.width() or leiste.sizeHint().width()
        hoehe = layout.heightForWidth(breite) if layout is not None else leiste.sizeHint().height()
        return PLOT_MIN_HOEHE_SPLITTER_PX + hoehe

    def _achsen_geaendert(self) -> None:
        """Eingabe in der Achsenleiste (gültig): genau einmal neu zeichnen (UI-37)."""
        if not self._in_aufbau and self._geladen is not None:
            self._zeichne()

    def _achsenleiste_aktualisieren(self, *_ansicht: int) -> None:
        """Zeigt Zustand und wirksame Grenzen der gezeichneten Achsen in der Achsenleiste."""
        zeichnung = self.plot.zeichnung
        einheiten: dict[str, str] = {}
        wirksam = self.plot.wirksame_grenzen()
        if zeichnung is not None and self._ansicht in ACHSEN_JE_ANSICHT:
            # Ansicht 5: die Zeichnung trägt die Größe als Rolle (E11); die Betragsfelder der
            # Leiste beziehen sich auf die Größe des Achsenzustands.
            betrag_rolle = self.plot.achsen_zustand.groesse_5 if self._ansicht == 5 else "betrag"
            alias = {betrag_rolle: "betrag"}
            for achse, rolle in zip(zeichnung.achsen, zeichnung.rollen, strict=False):
                rolle = alias.get(rolle, rolle)
                if rolle in ACHSEN_JE_ANSICHT[self._ansicht] and rolle not in einheiten:
                    einheiten[rolle] = einheit_aus_achsentitel(achse.get_ylabel())
            einheiten["frequenz"] = einheit_aus_achsentitel(zeichnung.achsen[-1].get_xlabel())
            if self._ansicht == 5:
                wirksam = {
                    alias.get(k, k): v
                    for k, v in wirksam.items()
                    if k in ("frequenz", "phase", betrag_rolle)
                }
        self.achsenleiste.aktualisiere(wirksam, einheiten)
        self._plot_spalte.setMinimumHeight(self._plot_min_hoehe())

    def _splitter_nachziehen(self) -> None:
        if self._ansicht == 3 and self.tabellen.isVisible():
            self._splitter_anwenden()

    def _splitter_anwenden(self) -> None:
        """Gibt der Tabelle ihre Standardhöhe (vier Zeilen) bzw. die gemerkte Höhe.

        Standard: Kopf der Tabelle, Reiterleiste und vier Zeilen zu 32 px, soweit der Plot seine
        gewünschte Höhe (:data:`PLOT_WUNSCH_HOEHE_SPLITTER_PX`) behält. Der Plot behält
        mindestens :data:`PLOT_MIN_HOEHE_SPLITTER_PX`; die Höhe wird nur für diese Sitzung
        gemerkt (:meth:`_splitter_bewegt`).
        """
        gesamt = sum(self._plot_seite.sizes()) or self._plot_seite.height()  # ohne Teilergriff
        if gesamt <= 0:
            return
        plot_min = self._plot_min_hoehe()
        kopf = self.tabelle_spitzen.tabelle.horizontalHeader().height()
        standard = (
            TABELLE_STANDARD_ZEILEN * ZEILENHOEHE_PX
            + max(kopf, ZEILENHOEHE_PX)
            + self.tabellen.tabBar().sizeHint().height()
            + 6
        )
        if self._tabellen_hoehe is not None:
            ziel = (
                self._tabellen_hoehe
            )  # vom Nutzer gezogen: gilt, soweit der Plot sein Minimum hat
        else:
            # Standard: der Plot hat Vorrang vor den vier Zeilen (Abnahme D-AUSW2-A, Befund 2);
            # die Tabelle gibt bis auf ihre Mindesthöhe nach.
            wunsch = plot_min - PLOT_MIN_HOEHE_SPLITTER_PX + PLOT_WUNSCH_HOEHE_SPLITTER_PX
            ziel = max(min(standard, gesamt - wunsch - 4), self.tabellen.minimumSizeHint().height())
        ziel = max(min(ziel, gesamt - plot_min - 4), 0)  # 4 px: Teilergriff
        self._plot_seite.setSizes([gesamt - ziel, ziel])
        for _ in range(2):  # Qt rundet und verrechnet den Teilergriff: nachstellen
            fehlt = plot_min - self._plot_seite.sizes()[0]
            if fehlt <= 0:
                break
            ziel = max(self._plot_seite.sizes()[1] - fehlt, 0)
            self._plot_seite.setSizes([gesamt - ziel, ziel])

    def _splitter_bewegt(self, _pos: int, _index: int) -> None:
        """Merkt die Tabellenhöhe, wenn der Nutzer den Teiler verschiebt (nur in dieser Sitzung)."""
        if self.tabellen.isVisible():
            self._tabellen_hoehe = int(self._plot_seite.sizes()[1])

    def _ansicht_gewaehlt(self, nr: int) -> None:
        """Ansichtsknopf gedrückt: Seite umschalten und neu zeichnen (Zoom je Ansicht bleibt)."""
        if nr not in FREIGESCHALTETE_ANSICHTEN or self._geladen is None:
            return
        self._aktiviere_ansicht(nr)
        self._zeichne(zoom_behalten=True)

    def _ansicht_geaendert(self) -> None:
        """Bedienelement einer Auswahlseite (Ansicht 2 oder 4) geändert."""
        if not self._in_aufbau and self._geladen is not None:
            self._zeichne(zoom_behalten=True)

    def _paar(self) -> tuple[str, str] | None:
        """Gewähltes Kanalpaar (``None`` = Datei ohne Referenz)."""
        i = self.combo_kanalpaar.currentIndex()
        return self._paare[i] if 0 <= i < len(self._paare) else None

    def _paar_geaendert(self, _index: int) -> None:
        self._spitze = None
        self._a3_schluessel = None
        self._a4_paar_schluessel = None
        if not self._in_aufbau and self._geladen is not None:
            self._zeichne(zoom_behalten=True)

    def _annahmen(self) -> Sequence[AnnahmeEintrag]:
        """Annahmen der Auswertung: aus Stufe B, bis dahin die Voreinstellungen (``Annahmen``)."""
        if self._pruefung is not None:
            return self._pruefung.annahmen
        return Annahmen().eintraege()

    def _aktualisiere_groessen(self) -> None:
        """Sperrt „kohärent“, wenn zu den gewählten Komponenten keine Referenz existiert."""
        if self._geladen is None:
            return
        daten = self._geladen.messdaten
        komponenten = tuple(c for c in KOMPONENTEN if self.chk[c].isChecked()) or KOMPONENTEN
        grund = verfuegbare_groessen(daten, komponenten)["kohaerent"]
        self.rb_groesse_cph.setEnabled(grund is None)
        self.rb_groesse_cph.setToolTip(grund or "")
        self.lbl_groesse_grund.setText(grund or "")
        self.lbl_groesse_grund.setVisible(grund is not None)
        if grund is not None:
            self.rb_groesse_ap.setChecked(True)
        elif not self.rb_groesse_ap.isChecked():
            self.rb_groesse_cph.setChecked(True)

    def _lese_auswahl(self) -> _Auswahl:
        """Liest die Bedienelemente von AD."""
        zeile = self.liste_punkte.currentRow()
        return _Auswahl(
            punkt=None if zeile <= 0 else zeile - 1,
            komponenten=tuple(c for c in KOMPONENTEN if self.chk[c].isChecked()),
            groesse="kohaerent" if self.rb_groesse_cph.isChecked() else "leistung",
            skala=self.plot.achsen_zustand.skala(1, "betrag"),
        )

    def _auswahl_geaendert(self, *_args: object) -> None:
        """Liest die Bedienelemente von AD und zeichnet neu."""
        if self._in_aufbau or self._geladen is None:
            return
        # Letzte gewählte Komponente lässt sich nicht abwählen (UI-4).
        if not any(k.isChecked() for k in self.chk.values()):
            quelle = self.sender()
            wieder = next((k for k in self.chk.values() if k is quelle), self.chk["X"])
            wieder.blockSignals(True)
            wieder.setChecked(True)
            wieder.blockSignals(False)
            return
        self._in_aufbau = True
        try:
            self._aktualisiere_groessen()
        finally:
            self._in_aufbau = False
        self._auswahl = self._lese_auswahl()
        self._zeichne(zoom_behalten=True)

    def _zeichne(self, *, zoom_behalten: bool = False) -> None:
        """Zeichnet die gewählte Ansicht mit der gemeinsamen Zeichenfunktion in die Plotfläche.

        Erwartete Fehler der Datenauswahl (``DarstellungsFehler``) stehen in der Meldezeile,
        alle anderen Ausnahmen im Fehlerband (nichts wird verschluckt); die Darstellung ist dann
        leer.
        """
        if self._geladen is None or self._cache is None:
            return
        zeichner = {
            1: self._zeichne_ansicht_1,
            2: self._zeichne_ansicht_2,
            3: self._zeichne_ansicht_3,
            4: self._zeichne_ansicht_4,
            5: self._zeichne_ansicht_5,
        }[self._ansicht]
        try:
            self._ansichtstext = None
            zeichner(zoom_behalten=zoom_behalten)
            self._zeige_cursor()
        except (DarstellungsFehler, AchsenFehler) as fehler:
            self._setze_meldung(f"{t.symbol('fehler')} {fehler}")
            self._fremden_inhalt_ersetzen(str(fehler))
        except Exception as fehler:  # unerwartet: sichtbar melden, Darstellung leeren
            self._zeichenfehler(str(fehler))
        self._zeige_ae_seite()

    def _zeichne_plot(
        self,
        nr: int,
        ansicht: Ansicht,
        daten: object,
        optionen: object,
        beschreibung: str,
        *,
        zoom_behalten: bool,
    ) -> Zeichnung:
        """Zeichnet in die Plotfläche und merkt, welche Ansicht sie jetzt zeigt."""
        zeichnung = self.plot.zeichne(
            ansicht, daten, optionen, beschreibung, zoom_behalten=zoom_behalten
        )
        self._plot_ansicht = nr
        return zeichnung

    def _leere_plot(self, *, zoom_vergessen: bool = False) -> None:
        """Leert die Plotfläche; der gemerkte Zoom bleibt, außer beim Dateiwechsel."""
        self.plot.leere(zoom_vergessen=zoom_vergessen)
        self._plot_ansicht = None

    def _fremden_inhalt_ersetzen(self, text: str) -> None:
        """Verhindert, dass die Plotfläche Inhalt oder Kopf einer anderen Ansicht zeigt.

        Zeigt die Plotfläche schon die gewählte Ansicht, bleibt sie unverändert. Sonst steht in
        Ansicht 4 der letzte gültige Stand (falls vorhanden), in allen anderen Fällen der
        Platzhaltertext ``text`` statt des Plots.
        """
        if self._plot_ansicht == self._ansicht:
            return
        if self._ansicht == 4 and self._a4_letzt is not None:
            daten, optionen, beschreibung, kopf, hinweise = self._a4_letzt
            self._zeichne_plot(
                4, Ansicht.SCHWINGFORM, daten, optionen, beschreibung, zoom_behalten=True
            )
            self.lbl_plotkopf.setText(kopf)
            self.auswahl_sf.setze_hinweise(hinweise)
            return
        self._leere_plot()
        self.lbl_plotkopf.setText("")
        self._ansichtstext = text

    def _zeichenfehler(self, text: str) -> None:
        """Meldet einen unerwarteten Fehler der Darstellung im Fehlerband."""
        self._leere_plot()
        self.lbl_plotkopf.setText("")
        self._fehlertext = zeichen_fehler_text(text)
        self.lbl_fehler.setText(self._fehlertext)
        self.band_fehler.setVisible(True)

    def _zeichne_ansicht_1(self, *, zoom_behalten: bool) -> None:
        assert self._geladen is not None and self._cache is not None
        daten = self._geladen.messdaten
        a = self._auswahl
        spektrum = spektrum_daten(
            daten,
            self._cache,
            punkt=a.punkt,
            komponenten=a.komponenten,
            groesse=a.groesse,
        )
        name = dateiname_von(daten.herkunft.pfad) if daten.herkunft is not None else ""
        f_min, f_max = float(daten.frequenz_hz[0]), float(daten.frequenz_hz[-1])
        beschreibung = plot_beschreibung(
            1, name, spektrum.auswahl_text, [k.beschriftung for k in spektrum.kurven], f_min, f_max
        )
        self._zeichne_plot(
            1,
            Ansicht.SPEKTRUM,
            spektrum,
            SpektrumOptionen(skala=self.plot.achsen_zustand.skala(1, "betrag")),
            beschreibung,
            zoom_behalten=zoom_behalten,
        )
        self.lbl_plotkopf.setText(
            plotkopf_text(
                name,
                spektrum.auswahl_text,
                [k.schluessel for k in spektrum.kurven],
                spektrum.bezeichnung,
            )
        )
        self.lbl_hinweise.setText("\n".join(spektrum.hinweise))
        self.lbl_hinweise.setVisible(bool(spektrum.hinweise))

    # --- Ansichten 2 bis 4 -----------------------------------------------------------------

    def _dateiname(self) -> str:
        assert self._geladen is not None
        herkunft = self._geladen.messdaten.herkunft
        return dateiname_von(herkunft.pfad) if herkunft is not None else ""

    def _beschreibung(self, ansicht: int, auswahl_text: str, komponenten: Sequence[str]) -> str:
        assert self._geladen is not None
        f = self._geladen.messdaten.frequenz_hz
        return plot_beschreibung(
            ansicht, self._dateiname(), auswahl_text, komponenten, float(f[0]), float(f[-1])
        )

    def _zeichne_ansicht_2(self, *, zoom_behalten: bool) -> None:
        """Ansicht 2: Betrag, optional Phase, Kohärenz des gewählten Kanalpaars (UI-5, UI-6)."""
        assert self._geladen is not None and self._cache is not None
        paar = self._paar()
        if paar is None:
            self._ansichtstext = TEXT_KEINE_FRF
            self.lbl_plotkopf.setText("")
            self.auswahl_frf.setze_hinweise("")
            return
        sel = self.auswahl_frf
        daten = frf_daten(self._cache, *paar, punkt=self._auswahl.punkt)
        opt = FrfOptionen(
            h1=sel.chk_h1.isChecked(),
            h2=sel.chk_h2.isChecked(),
            phase=sel.chk_phase.isChecked(),
            skala=self.plot.achsen_zustand.skala(2, "betrag"),
            kennzeichen_phase=kennzeichen_text("phase", self._annahmen()),
        )
        kurven = [n for n, an in (("H1", opt.h1), ("H2", opt.h2)) if an]
        zeichnung = self._zeichne_plot(
            2,
            Ansicht.FRF,
            daten,
            opt,
            self._beschreibung(2, daten.auswahl_text, [kanalpaar_text(*paar), *kurven]),
            zoom_behalten=zoom_behalten,
        )
        self.lbl_plotkopf.setText(
            plotkopf_text(
                self._dateiname(),
                daten.auswahl_text,
                [kanalpaar_text(*paar), *kurven],
                "H1/H2 und Kohärenz",
            )
        )
        sel.setze_hinweise("\n".join(zeichnung.hinweise))

    def _ansicht_3_tabellen(self, paar: tuple[str, str] | None) -> tuple[object, ...]:
        """Füllt Spitzen- und Bändertabelle (nur wenn sich Datei oder Kanalpaar geändert haben)."""
        assert self._geladen is not None and self._cache is not None
        schluessel: tuple[str, str] | str = paar if paar is not None else "ohne"
        daten = self._geladen.messdaten
        grenzen = gesamtband(daten.frequenz_hz)
        if self._a3_schluessel != schluessel:
            spitzen = self._cache.paar(*paar).spitzen.spitzen if paar is not None else ()
            zeilen, fehler = spitzen_zeilen(spitzen, warn_symbol=t.symbol("warnung"))
            leer = TEXT_KEINE_SPITZENSUCHE if paar is None else TEXT_KEINE_SPITZEN
            self.tabelle_spitzen.setze(zeilen, leer)
            self.auswahl_spitzen.setze_fehler(
                f"{t.symbol('fehler')} " + "; ".join(fehler) if fehler else ""
            )
            bandwerte = bandwerte_fuer(daten, self._cache, paar, grenzen)
            self.tabelle_baender.setze(
                baender_zeilen(bandwerte, grenzen, None, daten.punkte.label.tolist()),
                TEXT_KEINE_BAENDER,
            )
            self._a3_spitzen = tuple(spitzen)
            self._a3_schluessel = schluessel  # erst nach vollständigem Füllen (sonst Neuversuch)
        return self._a3_spitzen

    def _zeichne_ansicht_3(self, *, zoom_behalten: bool) -> None:
        """Ansicht 3: Kurve mit Spitzen und Band, Tabellen für Spitzen und Bänder (UI-7, UI-8)."""
        assert self._geladen is not None and self._cache is not None
        daten = self._geladen.messdaten
        paar = self._paar()
        spitzen = self._ansicht_3_tabellen(paar)
        grenzen = gesamtband(daten.frequenz_hz)
        if self._spitze is not None and not 0 <= self._spitze < len(spitzen):
            self._spitze = None
        if paar is not None:
            sd = spitzen_daten_frf(self._cache, *paar, baender=grenzen, gewaehlt=self._spitze)
            kopf_kanal = kanalpaar_text(*paar)
        else:
            kanal = next((k for k in daten.ap if k.startswith("Vib")), next(iter(daten.ap)))
            sd = spitzen_daten_spektrum(daten, self._cache, kanal, baender=grenzen)
            kopf_kanal = kanal
        self._kanal_a3 = kopf_kanal
        beschreibung = self._beschreibung(3, "Mittel (alle Punkte)", [kopf_kanal]) + (
            f" {len(sd.spitzen)} Spitzen gefunden." if sd.spitzen else f" {sd.hinweis}"
        )
        # Oberfläche: nur der Ring um die gewählte Spitze im Bild (ADR-026 Nachtrag); die Angaben
        # stehen als Text in der Auswahlspalte. Thesis und Arbeitsbild behalten Streifen und Kasten.
        zeichnung = self._zeichne_plot(
            3,
            Ansicht.SPITZEN,
            sd,
            SpitzenOptionen(
                skala=self.plot.achsen_zustand.skala(3, "betrag"),
                beschriftung_im_bild=False,
                legende_im_bild=False,
            ),
            beschreibung,
            zoom_behalten=zoom_behalten,
        )
        gewaehlt = spitzen[self._spitze] if self._spitze is not None else None
        self.auswahl_spitzen.setze_kurve("\n".join(zeichnung.hilfsobjekte["legende_eintraege"]))
        # Ohne Spitze wird nur dann zur Wahl aufgefordert, wenn es welche gibt. Ohne Referenz
        # bzw. ohne Spitzen erklärt die Tabelle den Zustand bereits, hier bleibt die Angabe leer.
        if gewaehlt is not None:
            angaben = spitze_angaben_text(gewaehlt, warn_symbol=t.symbol("warnung"))  # type: ignore[arg-type]
        elif sd.spitzen:
            angaben = TEXT_SPITZE_WAEHLEN
        else:
            angaben = ""
        self.auswahl_spitzen.setze_angaben(angaben)
        self.tabelle_spitzen.waehle(self._spitze)
        self.lbl_plotkopf.setText(
            plotkopf_text(
                self._dateiname(), "Mittel (alle Punkte)", [kopf_kanal], "Spitzen und Bänder"
            )
        )
        self.auswahl_spitzen.setze_hinweise("\n".join(zeichnung.hinweise))

    def _spitze_in_tabelle_gewaehlt(self, index: int) -> None:
        """Klick auf eine Zeile der Spitzentabelle markiert die Spitze im Plot (UI-8)."""
        if self._ansicht != 3 or index == self._spitze:
            return
        self._spitze = index
        self._zeichne(zoom_behalten=True)

    # --- Ansicht 4 --------------------------------------------------------------------------

    def _phase_referenz(self) -> str:
        """Referenzkanal der Phase: erster mit Kreuzspektren aller Vib-Kanäle, sonst ``Ref1``."""
        assert self._geladen is not None
        cp = self._geladen.messdaten.cp
        for referenz in dict.fromkeys(b for _a, b in cp):
            if all((f"Vib {c}", referenz) in cp for c in ("X", "Y", "Z")):
                return referenz
        return "Ref1"

    def _spitzen_der_paar(self) -> tuple[object, ...]:
        paar = self._paar()
        if paar is None or self._cache is None:
            return ()
        return tuple(self._cache.paar(*paar).spitzen.spitzen)

    def _paar_zur_komponente(self, komponente: str) -> None:
        """Stellt bei einer Einzelkomponente das Kanalpaar „Vib <Komponente> / <Referenz>“ ein.

        Nur beim Wechsel der Komponente; bei 3D bleibt das gewählte Paar. Danach gelten
        Spitzenliste, Schnellwahl und ``spitzen_kennzeichen`` für dieses Paar.
        """
        if komponente == self._a4_komponente:
            return
        self._a4_komponente = komponente
        if komponente == "3D":
            return
        ziel = (f"Vib {komponente}", self._phase_referenz())
        if ziel in self._paare and self._paar() != ziel:
            sperre = self.combo_kanalpaar.blockSignals(True)
            try:
                self.combo_kanalpaar.setCurrentIndex(self._paare.index(ziel))
            finally:
                self.combo_kanalpaar.blockSignals(sperre)
            self._spitze = None
            self._a3_schluessel = None
            self._a4_paar_schluessel = None

    def _fuelle_ansicht_4(self) -> None:
        """Setzt die Auswahlseite von Ansicht 4 (einmal je Datei) und die Spitzenliste (je Paar).

        Die Startfrequenz ist die Linie der höchsten Spitze des gewählten Kanalpaars (Nutzer
        bestätigt), ohne Spitze die erste Linie der Datei.
        """
        assert self._geladen is not None
        daten = self._geladen.messdaten
        spitzen = self._spitzen_der_paar()
        eintraege = [
            f"Nr {i + 1} · {frequenz_text(s.f_sp_hz, 3)}"  # type: ignore[attr-defined]
            for i, s in enumerate(spitzen)
        ]
        if not self._a4_geladen:
            start = (
                self._a4_wunsch_hz  # Klick oder Enter im Plot vor dem ersten Besuch von Ansicht 4
                if self._a4_wunsch_hz is not None
                else max(spitzen, key=lambda s: s.hoehe).f_sp_hz  # type: ignore[attr-defined]
                if spitzen
                else float(daten.frequenz_hz[0])
            )
            self.auswahl_sf.setze_datei(
                schritt_hz=float(daten.delta_f_hz),
                frequenz_hz=float(start),
                ebene=waehle_ebene(daten.punkte.koordinaten_m),
                spitzen=eintraege,
                punkte=[f"Punkt {int(p)}" for p in daten.punkte.label],
                phase_referenz=bool(daten.phase_gueltig and daten.cp),
                referenz_text=phase_ref_text(self._phase_referenz(), self._annahmen()),
                referenz_erklaerung=kennzeichen_beschreibung("phase", self._annahmen()),
            )
            self._a4_geladen = True
        else:
            self.auswahl_sf.setze_spitzen(eintraege)
        self._a4_paar_schluessel = self._paar()

    def _spitze_fuer_schwingform(self, index: int) -> None:
        """Schnellwahl „Spitze …“: setzt die Frequenz auf die Spitzenfrequenz."""
        spitzen = self._spitzen_der_paar()
        if 0 <= index < len(spitzen):
            self.auswahl_sf.setze_frequenz(float(spitzen[index].f_sp_hz))  # type: ignore[attr-defined]

    def _zeichne_ansicht_4(self, *, zoom_behalten: bool) -> None:
        """Ansicht 4: Schwingform bei einer Linie, Betrag oder Phase (UI-9, UI-10)."""
        assert self._geladen is not None and self._cache is not None
        daten = self._geladen.messdaten
        sel = self.auswahl_sf
        self._paar_zur_komponente(sel.komponente())
        if not self._a4_geladen or self._a4_paar_schluessel != self._paar():
            self._fuelle_ansicht_4()
        pruefung = frequenz_pruefen(sel.frequenz_hz(), daten.frequenz_hz, daten.delta_f_hz)
        sel.setze_pruefung(pruefung)
        if not pruefung.gueltig:
            # Eingabe außerhalb: Meldung unter dem Feld. Der Plot bleibt nur unverändert, wenn er
            # schon Ansicht 4 zeigt; sonst letzter gültiger Stand oder Platzhalter.
            self._fremden_inhalt_ersetzen(pruefung.fehler)
            return
        sd = schwingform_daten(
            daten,
            self._cache,
            sel.frequenz_hz(),
            komponente=sel.komponente(),
            referenz=self._phase_referenz(),
        )
        darstellung = sel.darstellung()
        spitze = spitze_der_linie(self._spitzen_der_paar(), sd.linie)  # type: ignore[arg-type]
        bezug_auto = standard_bezug(sd)
        sel.setze_bezug_automatisch(
            f"Automatisch (Punkt {int(sd.label[bezug_auto])})"
            if bezug_auto is not None
            else "Automatisch (kein Punkt mit γ² ≥ γ²_min)"
        )
        opt = SchwingformOptionen(
            darstellung=darstellung,  # type: ignore[arg-type]
            ebene=sel.ebene(),  # type: ignore[arg-type]
            punktlabels=sel.punktlabels(),
            bezug=sel.bezug() if darstellung == "phase_relativ" else None,
            kennzeichen_phase=(
                kennzeichen_text("phase", self._annahmen()) if darstellung == "phase_ref" else None
            ),
            spitzen_kennzeichen=spitze.kennzeichen if spitze is not None else (),
        )
        beschreibung = self._beschreibung(
            4, f"Linie {frequenz_text(sd.f_hz, 3)}", [sd.komponente, darstellung]
        )
        zeichnung = self._zeichne_plot(
            4, Ansicht.SCHWINGFORM, sd, opt, beschreibung, zoom_behalten=zoom_behalten
        )
        kopf = plotkopf_text(
            self._dateiname(),
            f"Linie {frequenz_text(sd.f_hz, 3)}",
            [sd.komponente],
            {
                "betrag": "Betrag",
                "phase_ref": f"Phase gegen {sd.referenz or 'Referenz'}",
                "phase_relativ": "Phase relativ zum Bezugspunkt",
            }[darstellung],
        )
        if not sd.phase_gueltig:
            kopf += f" · {TEXT_PHASE_KEINE_REFERENZ}"
        if opt.kennzeichen_phase is not None:  # Phase gegen Referenz solange M8 offen ist (UI-10)
            kopf += f" · {t.symbol('warnung')} Phase unbestätigt"
        self.lbl_plotkopf.setText(kopf)
        hinweise = "\n".join(zeichnung.hinweise)
        sel.setze_hinweise(hinweise)
        self._a4_letzt = (sd, opt, beschreibung, kopf, hinweise)

    # --- Ansicht 5: eigenes Diagramm aus Serien (R-058, R-059; P-AUSW2 S7) ---------------------

    def _kurzname(self, messung_id: int) -> str:
        messung = self._messungen.finde(messung_id)
        return messung.kurzname if messung is not None else "?"

    def _standard_paar_der_messung(
        self, messung_id: int, komponente: str | None
    ) -> tuple[str, str] | None:
        messung = self._messungen.finde(messung_id)
        return standard_paar(messung, komponente) if messung is not None else None

    def _aktualisiere_auswahl_5(self) -> None:
        """Größen (Verfügbarkeit mit Begründung) und Teilgröße des Spektrums in AD."""
        sel = self.auswahl_diagramm
        sel.setze_groessen(groessen_verfuegbar(self._messungen))
        gruende = [
            verfuegbare_groessen(m.geladen.messdaten, KOMPONENTEN)["kohaerent"]
            for m in self._messungen.bereite()
            if m.geladen is not None
        ]
        sel.setze_teilgroesse_moeglich(
            None if any(g is None for g in gruende) or not gruende else gruende[0]
        )

    def _cache_groessen_anpassen(self) -> None:
        """Hält je Messung so viele Kanalpaare, wie ihre Serien brauchen (2 bis 4).

        Sonst rechnet jeder Wechsel der Serie 250 ms neu (P-AUSW2 Abschnitt 3).
        """
        bedarf = paare_je_messung(self._serien.specs)
        for messung in self._messungen.bereite():
            if messung.cache is None:
                continue
            ziel = max(2, min(4, bedarf.get(messung.id, 0)))
            if messung.cache.groesse != ziel:
                messung.cache.setze_groesse(ziel)

    def _groesse_5_geaendert(self, groesse: str) -> None:
        """Radioknopf „Größe“: überlagert hat das Diagramm eine Größe, alle Serien ziehen mit."""
        del groesse
        sel = self.auswahl_diagramm
        if sel.anordnung() == "ueberlagert" and len(self._serien):
            entfallen = self._serien.wandle_groesse(sel.groesse(), self._standard_paar_der_messung)
            sel.setze_meldung(
                f"{entfallen} Serie(n) entfielen, weil sie dadurch doppelt wären."
                if entfallen
                else ""
            )
        if not self._in_aufbau and self._geladen is not None:
            self._zeichne()

    def _optionen_5_geaendert(self) -> None:
        """Teilgröße des Spektrums oder Anordnung geändert."""
        sel = self.auswahl_diagramm
        if self._serien.specs:
            entfallen = self._serien.setze_teilgroesse(sel.teilgroesse())
            sel.setze_meldung(
                f"{entfallen} Serie(n) entfielen, weil sie dadurch doppelt wären."
                if entfallen
                else ""
            )
        if not self._in_aufbau and self._geladen is not None:
            self._zeichne()

    def _serie_anlegen(self, spec: SerienSpec) -> bool:
        """Legt eine Serie an; Hinweistext in AD bei Dopplung oder voller Liste."""
        sel = self.auswahl_diagramm
        try:
            self._serien.hinzufuegen(spec)
        except SerienFehler as fehler:
            sel.setze_meldung(str(fehler))
            return False
        sel.setze_meldung("")
        return True

    def _angaben_der_messungen(self) -> list[MessungsAngabe]:
        return [
            MessungsAngabe(
                m.id,
                m.kurzname,
                tuple(int(x) for x in m.geladen.messdaten.punkte.label),
                m.paare,
            )
            for m in self._messungen.bereite()
            if m.geladen is not None
        ]

    def _frage_serie(self) -> SerienSpec | None:  # pragma: no cover - modaler Dialog
        """Zeigt den Serien-Dialog (Tests ersetzen die Methode); ``None`` = abgebrochen."""
        sel = self.auswahl_diagramm
        aktive = self._messungen.aktive
        dialog = SerienDialog(
            self._angaben_der_messungen(),
            sel.groesse(),
            sel.teilgroesse(),
            nebeneinander=sel.anordnung() == "nebeneinander",
            aktiv_id=aktive.id if aktive is not None else None,
            parent=self,
        )
        return dialog.ergebnis() if dialog.exec() == QDialog.DialogCode.Accepted else None

    def _serie_neu(self) -> None:
        """``+ Serie``: Dialog, dann anlegen und neu zeichnen."""
        if self._geladen is None:
            return
        spec = self._frage_serie()
        if spec is not None and self._serie_anlegen(spec):
            self._zeichne()

    def _vorlage_fuer_alle(self) -> SerienSpec | None:
        """Auswahl für „Für alle Messungen“: gewählte Serie, sonst letzte, sonst Voreinstellung."""
        sel = self.auswahl_diagramm
        specs = self._serien.specs
        zeile = sel.liste_serien.currentRow()
        if 0 <= zeile < len(specs):
            return specs[zeile]
        if specs:
            return specs[-1]
        aktive = self._messungen.aktive
        if aktive is None:
            return None
        try:
            return baue_spec(
                aktive.id,
                None,
                sel.groesse(),
                komponente="Z",
                kanalpaar=standard_paar(aktive, "Z"),
                teilgroesse=sel.teilgroesse(),
            )
        except SerienFehler as fehler:
            sel.setze_meldung(str(fehler))
            return None

    def _serie_alle(self) -> None:
        """``Für alle Messungen``: je Messung eine Serie mit derselben Auswahl (UI-12).

        Fehlt das Label oder das Kanalpaar in einer Messung, entfällt ihre Serie; der Grund steht
        in AD und in der Meldezeile (AF). Passt nicht alles in die Liste (höchstens vier), werden
        so viele angelegt wie passen.
        """
        vorlage = self._vorlage_fuer_alle()
        if vorlage is None or self._geladen is None:
            return
        specs, gruende = serien_fuer_alle(vorlage, self._messungen.bereite())
        for spec in specs:
            try:
                self._serien.hinzufuegen(spec)
            except SerienFehler as fehler:
                if str(fehler) == TEXT_SERIEN_VOLL:
                    gruende.append(f"{self._kurzname(spec.messung_id)}: {fehler}")
                # doppelte Serien sind schon da: nichts zu melden
        symbol = t.symbol("fehler") if gruende else ""
        text = " ".join(f"{symbol} {g}" for g in gruende)
        self.auswahl_diagramm.setze_meldung(text)
        self._zeichne()
        if gruende:  # AF zeigt den Grund auch nach dem Neuzeichnen
            self._setze_meldung(text)

    def _serie_entfernen_geklickt(self, zeile: int) -> None:
        if 0 <= zeile < len(self._serien):
            self._serien.entferne(zeile)
            self.auswahl_diagramm.setze_meldung("")
            self._zeichne()

    def _serie_sichtbar_geaendert(self, zeile: int, sichtbar: bool) -> None:
        if 0 <= zeile < len(self._serien):
            self._serien.setze_sichtbar(zeile, sichtbar)
            self._zeichne()

    def _zeichne_ansicht_5(self, *, zoom_behalten: bool) -> None:
        """Ansicht 5: Diagramm aus den Serien aller Messungen (R-058, R-059).

        Die Serien werden nur neu aufgelöst, wenn sich ihre Beschreibung geändert hat
        (``_serien_aufgeloest``); Achsen-, Sichtbarkeits- und Anordnungswechsel rechnen nichts.
        Nicht darstellbare Serien stehen mit Grund in AD (und AF); ohne Serie steht ein Hinweis.
        """
        sel = self.auswahl_diagramm
        self._aktualisiere_auswahl_5()
        specs = self._serien.specs
        self._cache_groessen_anpassen()
        if not specs:
            sel.setze_serien([], symbol_fehler=t.symbol("fehler"))
            sel.setze_voll(False)
            sel.setze_hinweise("")
            self.lbl_plotkopf.setText("")
            self._leere_plot()
            self._ansichtstext = TEXT_KEINE_SERIE
            return
        anordnung = sel.anordnung()
        daten = loese_alle_auf(
            specs,
            messungs_zugriff(self._messungen),
            anordnung=anordnung,
            bereits=self._serien_aufgeloest,
        )
        self._serien_aufgeloest = {s.spec.aufloesung_schluessel(): s for s in daten.serien}
        probleme = {spec.schluessel(): grund for spec, grund in daten.nicht_darstellbar}
        # Die Größe steht im Eintrag nur, wo sie unterscheidet: nebeneinander mit mehreren Größen.
        mit_groesse = anordnung == "nebeneinander" and len({s.groesse for s in specs}) > 1
        sel.setze_serien(
            [
                SerienEintrag(
                    serie_text(s, self._kurzname(s.messung_id), mit_groesse=mit_groesse),
                    s.slot,
                    s.sichtbar,
                    probleme.get(s.schluessel(), ""),
                )
                for s in specs
            ],
            symbol_fehler=t.symbol("fehler"),
        )
        sel.setze_voll(self._serien.ist_voll)
        phasen = any(s.groesse == "phase" and s.sichtbar for s in daten.serien)
        zustand = self.plot.achsen_zustand
        gezeichnet = [
            t.groesse
            for t in teilbilder(daten.serien, anordnung)[:TEILBILDER_MAX]
            if betrag_groesse(t.groesse)
        ]
        if gezeichnet and zustand.groesse_5 not in gezeichnet:
            zustand.setze_groesse_5(gezeichnet[0])  # deren Bereich und Skala kommen wieder (E11)
        # Nebeneinander mit mehreren Betragsgrößen: die Achsenleiste bietet die Größe der
        # Betragsfelder zur Wahl an (sonst gelten sie für die eine gezeichnete Größe).
        self.achsenleiste.setze_groessen(
            [(g, _BETRAG_NAMEN[g]) for g in dict.fromkeys(gezeichnet)]
            if anordnung == "nebeneinander"
            else [],
            zustand.groesse_5,
        )
        opt = DiagrammOptionen(
            anordnung=anordnung,
            skalen={g: zustand.skala(5, g) for g in BETRAG_GROESSEN_5},
            kennzeichen_phase=kennzeichen_text("phase", self._annahmen()) if phasen else None,
        )
        kurznamen = list(dict.fromkeys(s.kurzname for s in daten.serien))
        groessen = [s.groesse for s in daten.serien if s.sichtbar]
        beschreibung = self._beschreibung_5(daten.serien, kurznamen, groessen, anordnung)
        zeichnung = self._zeichne_plot(
            5, Ansicht.DIAGRAMM, daten, opt, beschreibung, zoom_behalten=zoom_behalten
        )
        self.lbl_plotkopf.setText(kopf_text(kurznamen, groessen, anordnung))
        gruende = [
            unmoeglich_text(spec, self._kurzname(spec.messung_id), grund, symbol=t.symbol("fehler"))
            for spec, grund in daten.nicht_darstellbar
        ]
        sel.setze_hinweise("\n".join([*gruende, *zeichnung.hinweise]))
        if gruende:
            self._setze_meldung(" · ".join(gruende))

    @staticmethod
    def _beschreibung_5(
        serien: Sequence[DiagrammSerie],
        kurznamen: Sequence[str],
        groessen: Sequence[str],
        anordnung: str,
    ) -> str:
        """Textalternative des Diagramms: Serien, Größe, Anordnung, Frequenzbereich (Brief 6)."""
        if not serien:
            return "Ansicht 5: Diagramm ohne darstellbare Serie."
        f_min = min(float(s.frequenz_hz[0]) for s in serien)
        f_max = max(float(s.frequenz_hz[-1]) for s in serien)
        texte = "; ".join(s.legende.replace("\n", ", ") for s in serien if s.sichtbar)
        return (
            f"Ansicht 5: Diagramm aus {len(serien)} Serien der Messungen {', '.join(kurznamen)}, "
            f"Größe {', '.join(dict.fromkeys(groessen))}, {anordnung}: {texte}. "
            f"Frequenzbereich {frequenz_text(f_min, 3)} bis {frequenz_text(f_max, 3)}."
        )
