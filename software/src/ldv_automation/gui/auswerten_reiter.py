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

import itertools
from collections.abc import Callable
from contextlib import suppress
from dataclasses import dataclass
from pathlib import Path

from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QResizeEvent
from PySide6.QtWidgets import (
    QButtonGroup,
    QCheckBox,
    QFileDialog,
    QFrame,
    QGraphicsOpacityEffect,
    QHBoxLayout,
    QLabel,
    QListWidget,
    QProgressBar,
    QPushButton,
    QRadioButton,
    QScrollArea,
    QSizePolicy,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
)

from ldv_automation.auswertung.jobs import PruefErgebnis, lese_job, pruef_job
from ldv_automation.auswertung.laden import Geladen
from ldv_automation.darstellung import Ansicht
from ldv_automation.darstellung.auswahl import (
    KOMPONENTEN,
    DarstellungsFehler,
    Groesse,
    PaarCache,
    kanalpaare,
    spektrum_daten,
    verfuegbare_groessen,
)
from ldv_automation.darstellung.spektrum import DB_GRUND, SpektrumOptionen
from ldv_automation.gui import tokens as t
from ldv_automation.gui.anzeige import Knopf
from ldv_automation.gui.anzeige_auswerten import (
    ANSICHT_NAMEN,
    TEXT_KEINE_DATEI,
    TEXT_PRUEFUNG_ABGEBROCHEN,
    TEXT_PRUEFUNG_BERECHNET,
    AuswertenZustand,
    ParameterZelle,
    bedienbarkeit_auswerten,
    dateiname_von,
    fehler_band_text,
    geladen_text,
    lade_text,
    parameter_tooltip,
    parameter_zellen,
    plot_beschreibung,
    plotkopf_text,
    pruefung_fehler_text,
    pruefung_text,
    punkt_eintraege,
    waehle_antriebspunkt,
    zeichen_fehler_text,
    zellen_sichtbar,
)
from ldv_automation.gui.plotflaeche import PlotFlaeche
from ldv_automation.gui.plotstil import baue_plotstil
from ldv_automation.gui.stil import schrift
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

_SEITE_LEER = 0
_SEITE_PLOT = 1


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


class AuswertenReiter(QWidget):
    """Inhalt des Reiters „Auswerten“.

    Parameters
    ----------
    ausfuehrer : Ausfuehrer
        Startet die Hintergrundaufträge (:class:`~ldv_automation.hintergrund.ProzessAusfuehrer`
        in der Oberfläche, ``DirektAusfuehrer`` oder ein nie fertiger Ausführer in Tests).
    abfrage_ms : int, optional
        Takt der Abfrage laufender Aufträge.
    parent : QWidget, optional
        Elternwidget.
    """

    def __init__(
        self,
        ausfuehrer: Ausfuehrer,
        *,
        abfrage_ms: int = t.ABFRAGE_AUSWERTEN_MS,
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)
        self.setObjectName("auswerten_inhalt")
        self._ausfuehrer = ausfuehrer
        self._zustand = AuswertenZustand.KEINE_DATEI
        self._geladen: Geladen | None = None
        self._cache: PaarCache | None = None
        self._auswahl = _Auswahl()
        self._job_id = 0
        self._auftrag_a: tuple[int, Auftrag, str] | None = None
        self._auftrag_b: tuple[int, Auftrag] | None = None
        self._pruefung: PruefErgebnis | None = None
        self._fehlertext: str | None = None
        self._pruef_fehler: str | None = None
        self._ansicht = 1
        self._in_aufbau = False
        self._letzter_ordner = ""
        self._abfrage_ms = abfrage_ms

        self._baue()
        self._timer = QTimer(self)
        self._timer.setObjectName("abfrage_auswerten")
        self._timer.setInterval(abfrage_ms)
        self._timer.timeout.connect(self._abfrage)
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

    def _baue_dateileiste(self) -> QFrame:
        leiste = QFrame()
        leiste.setObjectName("dateileiste")
        leiste.setFixedHeight(t.HOEHE_DATEILEISTE_PX)
        z = QHBoxLayout(leiste)
        z.setContentsMargins(12, 4, 12, 4)
        self.btn_oeffnen = QPushButton("Öffnen …")
        self.btn_oeffnen.setObjectName("btn_oeffnen")
        self.btn_oeffnen.setProperty("art", "primaer")
        self.lbl_datei = QLabel("–")
        self.lbl_datei.setObjectName("lbl_datei")
        self.lbl_datei.setFont(schrift(fett=True))
        self.lbl_pfad = _LinksKuerzLabel()
        self.lbl_pfad.setObjectName("lbl_pfad")
        self.lbl_pfad.setFont(schrift(t.SCHRIFT_PT, mono=True))
        self.lbl_pfad.setProperty("art", "gedaempft")
        namen = QVBoxLayout()
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
        for knopf in (self.btn_oeffnen, self.btn_export, self.btn_bild):
            knopf.setAutoDefault(False)
            knopf.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        z.addWidget(self.btn_oeffnen)
        z.addSpacing(8)
        z.addLayout(namen, 1)
        z.addWidget(self.btn_export)
        z.addWidget(self.btn_bild)
        z.addWidget(self.lbl_arbeitsansicht)
        self.btn_oeffnen.clicked.connect(self._oeffnen_geklickt)
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
        """Zone AD: 260 px fest, scrollbar bei Überlänge (T3a: nur die Seite von Ansicht 1)."""
        self.auswahlspalte = QScrollArea()
        self.auswahlspalte.setObjectName("auswahlspalte")
        self.auswahlspalte.setFixedWidth(t.BREITE_AUSWAHLSPALTE_PX)
        self.auswahlspalte.setWidgetResizable(True)
        self.auswahlspalte.setFrameShape(QFrame.Shape.NoFrame)
        self.auswahlspalte.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.auswahlspalte.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self._ad_stapel = QStackedWidget()
        self._ad_stapel.setObjectName("auswahl_stapel")
        self._ad_stapel.addWidget(self._baue_auswahl_spektrum())
        self.auswahlspalte.setWidget(self._ad_stapel)
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

        titel_punkt = self._gruppentitel("Punkt")
        self.liste_punkte = QListWidget()
        self.liste_punkte.setObjectName("liste_punkte")
        self.liste_punkte.setAccessibleName("Punkt oder Mittel")
        self.liste_punkte.setMinimumHeight(140)
        self.liste_punkte.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        v.addWidget(titel_punkt)
        v.addWidget(self.liste_punkte, 1)

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

        v.addWidget(self._gruppentitel("Amplitude"))
        self._gruppe_skala = QButtonGroup(self)
        self.rb_skala_linear = QRadioButton("linear")
        self.rb_skala_linear.setObjectName("rb_skala_linear")
        self.rb_skala_log = QRadioButton("logarithmisch")
        self.rb_skala_log.setObjectName("rb_skala_log")
        self.rb_skala_db = QRadioButton("dB")
        self.rb_skala_db.setObjectName("rb_skala_db")
        for knopf in (self.rb_skala_linear, self.rb_skala_log, self.rb_skala_db):
            knopf.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
            self._gruppe_skala.addButton(knopf)
            v.addWidget(knopf)
        self.rb_skala_log.setChecked(True)
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

        self.liste_punkte.currentRowChanged.connect(self._auswahl_geaendert)
        for kasten in self.chk.values():
            kasten.toggled.connect(self._auswahl_geaendert)
        self._gruppe_groesse.buttonToggled.connect(self._auswahl_geaendert)
        self._gruppe_skala.buttonToggled.connect(self._auswahl_geaendert)
        for gruppe in (self._gruppe_groesse, self._gruppe_skala):
            gruppe.buttonToggled.connect(lambda _k, _an, g=gruppe: self._tab_halt(g))
            self._tab_halt(gruppe)
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
        lv.addStretch(1)
        self._ae_stapel.addWidget(leer)
        self.plot = PlotFlaeche(baue_plotstil())
        self.plot.fehler.connect(self._zeichenfehler)
        self._grau_effekt = QGraphicsOpacityEffect(self.plot)
        self._grau_effekt.setOpacity(GRAU_DECKKRAFT)
        self._grau_effekt.setEnabled(False)
        self.plot.setGraphicsEffect(self._grau_effekt)
        self._ae_stapel.addWidget(self.plot)
        v.addWidget(self._ae_stapel, 1)
        return ae

    def _baue_fusszeile(self) -> QFrame:
        fuss = QFrame()
        fuss.setObjectName("fusszeile")
        fuss.setFixedHeight(t.HOEHE_FUSSZEILE_PX)
        f = QHBoxLayout(fuss)
        f.setContentsMargins(12, 2, 12, 2)
        self.lbl_cursor = QLabel()
        self.lbl_cursor.setObjectName("lbl_cursor")
        self.lbl_cursor.setFont(schrift(t.SCHRIFT_PT, mono=True))
        self.lbl_cursor.setSizePolicy(QSizePolicy.Policy.Ignored, QSizePolicy.Policy.Preferred)
        self.lbl_pruefung = QLabel(pruefung_text(()))
        self.lbl_pruefung.setObjectName("lbl_pruefung")
        self.lbl_pruefung.setFont(schrift(t.SCHRIFT_PT, mono=True))
        f.addWidget(self.lbl_cursor, 1)
        f.addWidget(self.lbl_pruefung)
        return fuss

    def _tab_reihenfolge(self) -> None:
        """AA → AC → AD → AE (Plot, Werkzeugleiste); AB ist nicht fokussierbar (Abschnitt 8)."""
        kette: list[QWidget] = [self.btn_oeffnen, self.btn_export, self.btn_bild]
        kette += [self.btn_ansicht[nr] for nr in sorted(self.btn_ansicht)]
        kette.append(self.liste_punkte)
        kette += list(self.chk.values())
        kette += [self.rb_groesse_cph, self.rb_groesse_ap]
        kette += [self.rb_skala_linear, self.rb_skala_log, self.rb_skala_db]
        kette += [self.btn_fehler_schliessen, self.btn_oeffnen_leer]
        kette += self.plot.tab_kette()
        for vorher, nachher in itertools.pairwise(kette):
            QWidget.setTabOrder(vorher, nachher)

    # --- Zugriff ---------------------------------------------------------------------------

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
        return self._auftrag_a is not None or self._auftrag_b is not None

    # --- Zustand ---------------------------------------------------------------------------

    @staticmethod
    def _setze(widget: QWidget, knopf: Knopf, normal: str = "") -> None:
        widget.setEnabled(knopf.aktiv)
        widget.setToolTip(normal if knopf.aktiv else knopf.grund)

    def _wende_zustand_an(self) -> None:
        """Aktivierung, Tooltips und sichtbare Seite je Zustand (Brief Abschnitt 6)."""
        tabelle = bedienbarkeit_auswerten(self._zustand)
        self._setze(self.btn_oeffnen, tabelle["oeffnen"], "Messdatei öffnen")
        self._setze(self.btn_oeffnen_leer, tabelle["oeffnen"])
        self._setze(self.btn_export, tabelle["export"], "Auswertungsdaten exportieren")
        self._setze(self.btn_bild, tabelle["bild"], "Aktuelle Ansicht als Bild speichern")
        auswahl = tabelle["auswahl"]
        self._ad_stapel.setEnabled(auswahl.aktiv)
        self.auswahlspalte.setToolTip("" if auswahl.aktiv else auswahl.grund)
        for nr, knopf in self.btn_ansicht.items():
            self._setze(knopf, tabelle[f"ansicht_{nr}"])
        laedt = self._zustand is AuswertenZustand.LADEN
        hat_daten = self._geladen is not None
        self.laden_leiste.setVisible(laedt)
        self.plot.setEnabled(not laedt)
        self._ausgrauen(laedt and hat_daten)
        if self._zustand is AuswertenZustand.GELADEN or (laedt and hat_daten):
            self._ae_stapel.setCurrentIndex(_SEITE_PLOT)
            self.lbl_plotkopf.setVisible(True)
        else:
            self._ae_stapel.setCurrentIndex(_SEITE_LEER)
            self.lbl_plotkopf.setVisible(False)
            self.plot_platzhalter.setVisible(not laedt)
            self.btn_oeffnen_leer.setVisible(not laedt)

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

    def _oeffnen_geklickt(self) -> None:
        pfad = self._waehle_datei()
        if pfad:
            self.oeffne_datei(pfad)

    def oeffne_datei(self, pfad: str) -> None:
        """Liest ``pfad`` im Hintergrund; laufende Aufträge werden abgebrochen (Job-ID).

        Parameters
        ----------
        pfad : str
            Pfad der ``.svd``-Datei.
        """
        self._abbrechen()
        self._zeige_pruefung()  # abgebrochene Stufe B steht nicht mehr als „wird berechnet“
        self._job_id += 1
        self._letzter_ordner = str(Path(pfad).parent)
        self.schliesse_fehlerband()
        self.lbl_laden.setText(lade_text(dateiname_von(pfad)))
        self._setze_zustand(AuswertenZustand.LADEN)
        try:
            auftrag = self._ausfuehrer.starte(lese_job, pfad)
        except Exception as fehler:  # Prozess nicht startbar (Spawn, Pipe): als Lesefehler zeigen
            self._lesefehler(f"{pfad}: {fehler}")
            return
        self._auftrag_a = (self._job_id, auftrag, pfad)
        self._timer.start()

    def schliesse_fehlerband(self) -> None:
        """Blendet das Fehlerband aus (Knopf „Schließen“)."""
        self._fehlertext = None
        self.band_fehler.setVisible(False)

    def _lesefehler(self, text: str) -> None:
        """Zeigt das Fehlerband; die zuvor geladene Datei bleibt unverändert (UI-15).

        Auch dieser Pfad darf nicht scheitern: Der Zustand wird zuerst gesetzt (nie „Laden“ nach
        einer Ausnahme), danach folgen die Widgets einzeln; Ladeleiste und Abfrage werden in
        jedem Fall beendet.
        """
        self._fehlertext = fehler_band_text(text)
        zustand = (
            AuswertenZustand.GELADEN if self._geladen is not None else AuswertenZustand.KEINE_DATEI
        )
        self._zustand = zustand
        schritte: tuple[Callable[[], object], ...] = (
            lambda: self.lbl_fehler.setText(self._fehlertext or ""),
            lambda: self.band_fehler.setVisible(True),
            lambda: self.laden_leiste.setVisible(False),
            self._wende_zustand_an,
            self._zeige_pruefung,
        )
        for schritt in schritte:
            with suppress(Exception):
                schritt()
        if self._auftrag_a is None and self._auftrag_b is None:
            self._timer.stop()

    def _zeige_pruefung(self) -> None:
        """Fußzeile rechts: Prüfung der **angezeigten** Datei, nie ein veralteter Stand."""
        if self._geladen is None:
            self.lbl_pruefung.setText(pruefung_text(()))
            self.lbl_pruefung.setToolTip("")
        elif self._pruefung is not None:
            self.lbl_pruefung.setText(pruefung_text(self._pruefung.pruefungen))
            self.lbl_pruefung.setToolTip("")
        elif self._pruef_fehler is not None:
            self.lbl_pruefung.setText(pruefung_fehler_text(self._pruef_fehler))
            self.lbl_pruefung.setToolTip(self._pruef_fehler)
        elif self._auftrag_b is not None:
            self.lbl_pruefung.setText(TEXT_PRUEFUNG_BERECHNET)
            self.lbl_pruefung.setToolTip("")
        else:
            self.lbl_pruefung.setText(TEXT_PRUEFUNG_ABGEBROCHEN)
            self.lbl_pruefung.setToolTip("Stufe B wurde vor dem Ende abgebrochen.")

    # --- Hintergrundaufträge ---------------------------------------------------------------

    def _abbrechen(self) -> None:
        for eintrag in (self._auftrag_a, self._auftrag_b):
            if eintrag is not None:
                eintrag[1].abbrechen()
        self._auftrag_a = None
        self._auftrag_b = None
        self._timer.stop()

    def beende(self) -> None:
        """Bricht laufende Aufträge ab und stoppt die Abfrage (Schließen des Fensters)."""
        self._abbrechen()

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
        if self._auftrag_a is None and self._auftrag_b is None:
            self._timer.stop()

    def _ergebnis_a(self, job: int, auftrag: Auftrag, pfad: str) -> None:
        try:
            geladen = auftrag.ergebnis()
        except AuftragAbgebrochen:
            return
        except AuftragFehler as fehler:
            self._lesefehler(fehler.meldung)
            return
        self._uebernehme(job, geladen, pfad)

    def _ergebnis_b(self, auftrag: Auftrag) -> None:
        try:
            ergebnis = auftrag.ergebnis()
        except AuftragAbgebrochen:
            self._zeige_pruefung()
            return
        except AuftragFehler as fehler:
            self._pruef_fehler = fehler.meldung
            self._zeige_pruefung()
            return
        self._pruefung = ergebnis
        self._zeige_pruefung()

    def _verwerfe_datei(self) -> None:
        """Setzt den Reiter in den Zustand „Keine Datei“ zurück (nach einem Fehler beim Aufbau).

        Der Rückfallpfad darf selbst nicht scheitern: Jeder Schritt läuft einzeln und ein
        Fehler darin wird übergangen (der auslösende Fehler steht schon im Fehlerband).
        """
        self._geladen = None
        self._cache = None
        self._pruefung = None
        self._pruef_fehler = None
        self._in_aufbau = True
        schritte: tuple[Callable[[], object], ...] = (
            self.liste_punkte.clear,
            self.plot.leere,
            lambda: self.lbl_datei.setText("–"),
            lambda: self.lbl_pfad.setText(""),
            lambda: self.lbl_plotkopf.setText(""),
            lambda: self.lbl_hinweise.setText(""),
            self._fuelle_parameter,
        )
        try:
            for schritt in schritte:
                with suppress(Exception):
                    schritt()
        finally:
            self._in_aufbau = False

    def _uebernehme(self, job: int, geladen: Geladen, pfad: str) -> None:
        """Stufe A fertig: Ansicht 1 sofort zeigen, Stufe B im Hintergrund starten.

        Tempo (Nutzerentscheidung): Zielwert für den Erstaufbau und für jeden Wechsel von Punkt,
        Komponente, Größe oder Skala ist **unter 400 ms** (statt 100 ms im Brief); er ist am
        Messrechner zu messen. ``PaarCache`` und Zeichnen laufen bewusst im GUI-Thread, eine
        Verlagerung in den Hintergrund ist nicht vorgesehen.

        Scheitert die Aufbereitung (Cache, Punktliste, Parameterzeile, Auswahl), meldet der Reiter
        das wie einen Lesefehler (Fehlerband mit Pfad). Davor wird nichts am Reiter geändert, die
        bisherige Datei bleibt; scheitert es danach, geht der Reiter in „Keine Datei“.
        """
        daten = geladen.messdaten
        try:
            cache = PaarCache(daten)
            eintraege = punkt_eintraege(daten.punkte.label, daten.punkte.koordinaten_m)
            zellen = parameter_zellen(geladen.einstellungen)
            verfuegbare_groessen(daten, KOMPONENTEN)
            antrieb = waehle_antriebspunkt(kanalpaare(daten))
        except Exception as fehler:  # jede Ausnahme der Aufbereitung ist ein Lesefehler
            self._lesefehler(f"{pfad}: Auswertung nicht möglich: {fehler}")
            return
        self._geladen = geladen
        self._cache = cache
        self._pruefung = None
        self._pruef_fehler = None
        self._in_aufbau = True
        try:
            self.liste_punkte.clear()
            self.liste_punkte.addItems(eintraege)
            self.liste_punkte.setCurrentRow(0)
            for kasten in self.chk.values():
                kasten.setChecked(True)
            self.rb_skala_log.setChecked(True)
            self.rb_groesse_cph.setChecked(True)
            self._aktualisiere_groessen()
            self._auswahl = self._lese_auswahl()
            self.lbl_datei.setText(dateiname_von(pfad))
            self.lbl_pfad.setText(pfad)
            self.parameterzeile.setze_zellen(zellen)
        except Exception as fehler:  # Qt-Aufbau schlägt fehl: nichts halb geladen stehen lassen
            self._in_aufbau = False
            self._verwerfe_datei()
            self._lesefehler(f"{pfad}: Anzeige nicht möglich: {fehler}")
            return
        finally:
            self._in_aufbau = False
        self.lbl_cursor.setText(geladen_text(pfad))
        self._setze_zustand(AuswertenZustand.GELADEN)
        self._zeichne()
        herkunft = daten.herkunft
        sha = herkunft.sha256 if herkunft is not None else None
        try:
            auftrag = self._ausfuehrer.starte(pruef_job, pfad, sha, antrieb)
        except Exception as fehler:  # Prozess nicht startbar: Prüfung nicht möglich
            self._pruef_fehler = str(fehler)
            self._zeige_pruefung()
            return
        self._auftrag_b = (job, auftrag)
        self._zeige_pruefung()
        self._timer.start()

    # --- Parameterzeile --------------------------------------------------------------------

    def _fuelle_parameter(self) -> None:
        einstellungen = self._geladen.einstellungen if self._geladen is not None else None
        self.parameterzeile.setze_zellen(parameter_zellen(einstellungen))

    # --- Ansicht 1 -------------------------------------------------------------------------

    def _ansicht_gewaehlt(self, nr: int) -> None:
        """Ansichtsknopf gedrückt (T3a: nur Ansicht 1 ist freigeschaltet)."""
        if nr == 1:
            self._ansicht = 1

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

    @staticmethod
    def _tab_halt(gruppe: QButtonGroup) -> None:
        """Tab-Halt einer Radiogruppe auf der **gewählten** Option (Pfeiltasten wechseln).

        Qt hält sonst bei der ersten Option der Gruppe an. Die übrigen Optionen bleiben mit
        ``ClickFocus`` fokussierbar (UI-21), nehmen aber nicht an der Tab-Reihenfolge teil.
        """
        for knopf in gruppe.buttons():
            knopf.setFocusPolicy(
                Qt.FocusPolicy.StrongFocus if knopf.isChecked() else Qt.FocusPolicy.ClickFocus
            )

    def _lese_auswahl(self) -> _Auswahl:
        """Liest die Bedienelemente von AD."""
        zeile = self.liste_punkte.currentRow()
        return _Auswahl(
            punkt=None if zeile <= 0 else zeile - 1,
            komponenten=tuple(c for c in KOMPONENTEN if self.chk[c].isChecked()),
            groesse="kohaerent" if self.rb_groesse_cph.isChecked() else "leistung",
            skala="linear" if self.rb_skala_linear.isChecked() else "log",
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
        """Zeichnet Ansicht 1 mit der gemeinsamen Zeichenfunktion in die Plotfläche.

        Erwartete Fehler der Datenauswahl (``DarstellungsFehler``) stehen in der Meldezeile,
        alle anderen Ausnahmen im Fehlerband (nichts wird verschluckt); die Darstellung ist dann
        leer.
        """
        if self._geladen is None or self._cache is None:
            return
        try:
            self._zeichne_ansicht_1(zoom_behalten=zoom_behalten)
        except DarstellungsFehler as fehler:
            self.lbl_cursor.setText(f"{t.symbol('fehler')} {fehler}")
        except Exception as fehler:  # unerwartet: sichtbar melden, Darstellung leeren
            self._zeichenfehler(str(fehler))

    def _zeichenfehler(self, text: str) -> None:
        """Meldet einen unerwarteten Fehler der Darstellung im Fehlerband."""
        self.plot.leere()
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
        self.plot.zeichne(
            Ansicht.SPEKTRUM,
            spektrum,
            SpektrumOptionen(skala="linear" if a.skala == "linear" else "log"),
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
