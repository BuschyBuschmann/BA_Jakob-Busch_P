"""Hauptfenster der Mess-Warteschlange (Brief P3, Abschnitte 1, 3, 4 und 5).

Ein einziger Aktualisierungspfad (:meth:`Hauptfenster.aktualisiere`, per ``QTimer`` im
GUI-Thread) holt Ereignisse und ``Zustandsbild`` der Sitzung ab und schreibt alle Zonen
neu. Die Oberfläche ruft nie selbst in den Geräte-Thread und startet keinen Thread.
"""

from __future__ import annotations

import itertools
import time
from collections.abc import Callable
from datetime import datetime
from pathlib import Path
from uuid import UUID

from PySide6.QtCore import QSize, Qt, QTimer, QUrl
from PySide6.QtGui import (
    QAction,
    QActionGroup,
    QCloseEvent,
    QDesktopServices,
    QKeySequence,
    QPainter,
    QPaintEvent,
)
from PySide6.QtWidgets import (
    QApplication,
    QDialog,
    QFileDialog,
    QFrame,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QMenu,
    QMessageBox,
    QPlainTextEdit,
    QProgressBar,
    QPushButton,
    QSizePolicy,
    QSplitter,
    QToolButton,
    QVBoxLayout,
    QWidget,
)

from ldv_automation.domaene import KATALOG, Messung, Parameterkatalog, Pausenpunkt
from ldv_automation.gui import tokens as t
from ldv_automation.gui.anzeige import (
    BETRIEBSART_TOOLTIP,
    BETRIEBSART_WORT,
    FEHLERSTRATEGIE_TOOLTIP,
    FEHLERSTRATEGIE_VERMERK,
    RUHE_ZUSTAENDE,
    WARTEND,
    Knopf,
    abbruch_laeuft_messung,
    bedienbarkeit,
    definitionen,
    durchgang_text,
    echt_gemessen,
    einfuegeort_text,
    einfuegeposition,
    fenstertitel,
    finde,
    fortschritt_anzeige,
    hinweis,
    index_von,
    protokolltext,
    schliessen_entscheidung,
    start_dialog,
    verbindung_text,
    voraussetzung_zeilen,
    zeilen,
    zuruecksetzen_frage_text,
)
from ldv_automation.gui.anzeige import nummern_bild as nr_anzeige
from ldv_automation.gui.dialoge import (
    DurchgangStartenDialog,
    EinstellungenDialog,
    GeraetDialog,
    MessenFreischaltenDialog,
    abbrechen_dialog,
    frage,
    trockenlauf_dialog,
)
from ldv_automation.gui.editor import Editor
from ldv_automation.gui.fassade import SitzungsFassade
from ldv_automation.gui.hinweisband import Hinweisband
from ldv_automation.gui.stil import schrift, setze_eigenschaft
from ldv_automation.gui.tabelle import Warteschlangentabelle
from ldv_automation.sitzung import (
    Betriebsart,
    DurchgangZustand,
    EinstellungsFehler,
    Fehlerentscheidung,
    Zustandsbild,
)

Z = DurchgangZustand

DURCHGANG_MAX_BREITE_PX = 480
"""Breite, bis zu der der Durchgangstext nie gekürzt wird (Statuszeile, 1100 px)."""
BEFEHL_SPERRE_MAX_S = 2.0
"""Längste Sperre der Ablaufknöpfe nach einem Befehl, falls kein neues Zustandsbild kommt."""
DATEIFILTER_WARTESCHLANGE = "Warteschlange (*.warteschlange.json)"
ENDUNG_WARTESCHLANGE = ".warteschlange.json"
KONFLIKT_GESTARTET = (
    f"{t.symbol('fehler')} Der Eintrag wurde inzwischen gestartet. "
    "Deine Änderungen wurden nicht übernommen."
)


def _nr_text(bild: Zustandsbild, eintrag_id: UUID) -> str | None:
    """Nummer eines Eintrags für Titel und Texte (endgültig „01“, sonst „02 (vorl.)“)."""
    nr = nr_anzeige(bild).get(eintrag_id)
    return nr.lang if nr is not None else None


class KurzLabel(QLabel):
    """Label, das zu langen Text rechts mit „…“ kürzt; der Volltext steht im Tooltip."""

    def __init__(self, text: str = "", parent: QWidget | None = None) -> None:
        super().__init__(text, parent)
        self._voll = text
        self.setSizePolicy(QSizePolicy.Policy.Ignored, QSizePolicy.Policy.Preferred)
        self.setMinimumWidth(40)

    def setText(self, text: str) -> None:  # noqa: N802  # Qt-Name
        """Setzt den Volltext (Anzeige gekürzt, Tooltip vollständig)."""
        self._voll = text
        self.setToolTip(text)
        super().setText(text)

    def volltext(self) -> str:
        """Ungekürzter Text."""
        return self._voll

    def paintEvent(self, event: QPaintEvent) -> None:  # noqa: N802  # Qt-Name
        """Zeichnet den Text gekürzt auf die verfügbare Breite."""
        painter = QPainter(self)
        gekuerzt = self.fontMetrics().elidedText(
            self._voll, Qt.TextElideMode.ElideRight, self.contentsRect().width()
        )
        ausrichtung = int(Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft)
        painter.drawText(self.contentsRect(), ausrichtung, gekuerzt)

    def sizeHint(self) -> QSize:  # noqa: N802  # Qt-Name
        """Bevorzugte Größe nach Volltext."""
        breite = self.fontMetrics().horizontalAdvance(self._voll) + 8
        return QSize(breite, super().sizeHint().height())


class Hauptfenster(QMainWindow):
    """Hauptfenster mit den Zonen A bis G des Design-Briefs.

    Parameters
    ----------
    sitzung : SitzungsFassade
        Sitzung (oder Attrappe in Tests).
    katalog : Parameterkatalog
        Parameterkatalog für Editor und Tabelle.
    takt_ms : int or None
        Abholtakt in ms; ``None`` startet keinen Timer (Tests rufen :meth:`aktualisiere`).
    """

    def __init__(
        self,
        sitzung: SitzungsFassade,
        *,
        katalog: Parameterkatalog = KATALOG,
        takt_ms: int | None = t.AKTUALISIERUNG_MS,
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)
        self.setObjectName("hauptfenster")
        self._sitzung = sitzung
        self._katalog = katalog
        self._bild: Zustandsbild = sitzung.zustandsbild()
        # Bisher nichts gespeichert oder geladen: jede nicht leere Warteschlange ist neu.
        self._gespeichert: tuple[tuple[object, ...], ...] = ()
        self._beendet_quittiert: str | None = None
        self._sperre_revision: int | None = None
        self._sperre_seit = 0.0
        self._auto_verbinden_versucht = False
        self._war_verbunden = False
        self._letzte_betriebsart: Betriebsart | None = None
        self._neu_anker: UUID | None = None
        self._neu_am_anfang = False
        self._auswahl_ruecksprung = False
        self._in_zeige = False
        self._letzte_auswahl: UUID | None = None
        self._dateiname: str | None = None

        self.setMinimumSize(t.FENSTER_MIN_BREITE_PX, t.FENSTER_MIN_HOEHE_PX)
        self.resize(1366, 768)
        self._baue_aktionen()
        self._baue_oberflaeche()
        self._verbinde_signale()

        self._timer = QTimer(self)
        self._timer.setObjectName("aktualisierung")
        self._timer.timeout.connect(self.aktualisiere)
        if takt_ms is not None:
            self._timer.start(takt_ms)
        self.aktualisiere()

    # --- Aufbau ----------------------------------------------------------------------------

    def _aktion(self, text: str, objekt: str, taste: QKeySequence | None, slot: object) -> QAction:
        a = QAction(text, self)
        a.setObjectName(objekt)
        if taste is not None:
            a.setShortcut(taste)
            a.setShortcutContext(Qt.ShortcutContext.WindowShortcut)
        a.triggered.connect(slot)
        self.addAction(a)
        return a

    def _baue_aktionen(self) -> None:
        q = QKeySequence
        self.act_messung_neu = self._aktion(
            "+ Messung", "act_messung_neu", q("Ctrl+N"), self._messung_neu
        )
        self.act_pausenpunkt_neu = self._aktion(
            "+ Pausenpunkt", "act_pausenpunkt_neu", q("Ctrl+Shift+N"), self._pausenpunkt_neu
        )
        self.act_entfernen = self._aktion("Entfernen", "act_entfernen", None, self._entfernen)
        self.act_hoch = self._aktion("▲", "act_hoch", None, self._hoch)
        self.act_runter = self._aktion("▼", "act_runter", None, self._runter)
        self.act_speichern = self._aktion(
            "Speichern …", "act_speichern", q("Ctrl+S"), self._speichern
        )
        self.act_laden = self._aktion("Laden …", "act_laden", q("Ctrl+O"), self._laden)
        self.act_start = self._aktion("Start", "act_start", q("F5"), self._start)
        self.act_pause = self._aktion("Pausieren (F6)", "act_pause", q("F6"), self._pause)
        self.act_abbrechen = self._aktion("Abbrechen …", "act_abbrechen", q("F8"), self._abbrechen)
        self.act_bestaetigen = self._aktion(
            "Pausenpunkt bestätigen (F7)", "act_bestaetigen", q("F7"), self._bestaetigen
        )
        self._tasten_hinweis = {
            "messung_neu": "Strg+N",
            "pausenpunkt_neu": "Strg+Umschalt+N",
            "entfernen": "Entf",
            "hoch": "Alt+↑",
            "runter": "Alt+↓",
            "speichern": "Strg+S",
            "laden": "Strg+O",
        }

    def _knopf(self, aktion: QAction, objekt: str, art: str = "") -> QToolButton:
        b = QToolButton()
        b.setDefaultAction(aktion)
        b.setObjectName(objekt)
        b.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextOnly)
        b.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        b.setMinimumHeight(t.KNOPF_MIN_HOEHE_PX)
        if art:
            b.setProperty("art", art)
        return b

    def _baue_oberflaeche(self) -> None:
        zentral = QWidget()
        haupt = QVBoxLayout(zentral)
        haupt.setContentsMargins(0, 0, 0, 0)
        haupt.setSpacing(0)

        # Zone A: Statuszeile
        self.statuszeile = QFrame()
        self.statuszeile.setObjectName("statuszeile")
        self.statuszeile.setFixedHeight(t.HOEHE_STATUSZEILE_PX)
        a = QHBoxLayout(self.statuszeile)
        a.setContentsMargins(12, 4, 12, 4)
        self.btn_betriebsart = QToolButton()
        self.btn_betriebsart.setObjectName("btn_betriebsart")
        self.btn_betriebsart.setPopupMode(QToolButton.ToolButtonPopupMode.InstantPopup)
        self.btn_betriebsart.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.btn_betriebsart.setAccessibleName("Betriebsart")
        self.menu_betriebsart = QMenu(self.btn_betriebsart)
        self.menu_betriebsart.setObjectName("menu_betriebsart")
        self._gruppe_betriebsart = QActionGroup(self)
        self._gruppe_betriebsart.setExclusive(True)
        self.act_betriebsart: dict[Betriebsart, QAction] = {}
        for art in Betriebsart:
            act = QAction(BETRIEBSART_WORT[art], self.menu_betriebsart)
            act.setObjectName(f"act_betriebsart_{art.value}")
            act.setCheckable(True)
            act.setToolTip(BETRIEBSART_TOOLTIP[art])
            act.triggered.connect(
                lambda _c=False, gewaehlt=art: self._betriebsart_gewaehlt(gewaehlt)
            )
            self._gruppe_betriebsart.addAction(act)
            self.menu_betriebsart.addAction(act)
            self.act_betriebsart[art] = act
        self.btn_betriebsart.setMenu(self.menu_betriebsart)
        self.lbl_durchgang = KurzLabel()
        self.lbl_durchgang.setObjectName("lbl_durchgang")
        self.lbl_durchgang.setFont(schrift(fett=True))
        self.lbl_verbindung = KurzLabel()
        self.lbl_verbindung.setObjectName("lbl_verbindung")
        self.lbl_fehlerstrategie = KurzLabel(FEHLERSTRATEGIE_VERMERK)
        self.lbl_fehlerstrategie.setObjectName("lbl_fehlerstrategie")
        self.lbl_fehlerstrategie.setToolTip(f"{FEHLERSTRATEGIE_VERMERK}. {FEHLERSTRATEGIE_TOOLTIP}")
        self.btn_verbinden = QPushButton("Verbinden")
        self.btn_verbinden.setObjectName("btn_verbinden")
        self.btn_geraet = QPushButton("Gerät …")
        self.btn_geraet.setObjectName("btn_geraet")
        self.btn_einstellungen = QPushButton("Einstellungen …")
        self.btn_einstellungen.setObjectName("btn_einstellungen")
        for knopf_a in (self.btn_verbinden, self.btn_geraet, self.btn_einstellungen):
            knopf_a.setAutoDefault(False)
            knopf_a.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        a.addWidget(self.btn_betriebsart)
        a.addSpacing(8)
        a.addWidget(self.lbl_durchgang, 3)
        a.addWidget(self.lbl_verbindung, 3)
        a.addWidget(self.lbl_fehlerstrategie, 2)
        a.addSpacing(8)
        a.addWidget(self.btn_verbinden)
        a.addWidget(self.btn_geraet)
        a.addWidget(self.btn_einstellungen)
        haupt.addWidget(self.statuszeile)

        # Zone B: Werkzeugleiste
        self.werkzeugleiste = QFrame()
        self.werkzeugleiste.setObjectName("werkzeugleiste")
        self.werkzeugleiste.setFixedHeight(t.HOEHE_WERKZEUGLEISTE_PX)
        b = QHBoxLayout(self.werkzeugleiste)
        b.setSpacing(4)  # 1100 px: alle Knöpfe ungekürzt (K-U4, 5)
        b.setContentsMargins(12, 6, 12, 6)
        self.btn_messung_neu = self._knopf(self.act_messung_neu, "btn_messung_neu")
        self.btn_pausenpunkt_neu = self._knopf(self.act_pausenpunkt_neu, "btn_pausenpunkt_neu")
        self.btn_entfernen = self._knopf(self.act_entfernen, "btn_entfernen")
        self.btn_hoch = self._knopf(self.act_hoch, "btn_hoch")
        self.btn_hoch.setAccessibleName("Eintrag nach oben")
        self.btn_runter = self._knopf(self.act_runter, "btn_runter")
        self.btn_runter.setAccessibleName("Eintrag nach unten")
        self.btn_speichern = self._knopf(self.act_speichern, "btn_speichern")
        self.btn_laden = self._knopf(self.act_laden, "btn_laden")
        self.btn_start = self._knopf(self.act_start, "btn_start", "primaer")
        self.btn_pause = self._knopf(self.act_pause, "btn_pause")
        self.btn_abbrechen = self._knopf(self.act_abbrechen, "btn_abbrechen", "gefahr")
        self._werkzeugknoepfe = (
            self.btn_messung_neu,
            self.btn_pausenpunkt_neu,
            self.btn_entfernen,
            self.btn_hoch,
            self.btn_runter,
            self.btn_speichern,
            self.btn_laden,
            self.btn_start,
            self.btn_pause,
            self.btn_abbrechen,
        )
        for knopf in self._werkzeugknoepfe[:7]:
            b.addWidget(knopf)
        b.addStretch(1)
        b.addWidget(self.btn_start)
        b.addWidget(self.btn_pause)
        b.addSpacing(16)
        b.addWidget(self.btn_abbrechen)
        haupt.addWidget(self.werkzeugleiste)

        inhalt = QWidget()
        c = QVBoxLayout(inhalt)
        c.setContentsMargins(t.FENSTERRAND_PX, 8, t.FENSTERRAND_PX, t.FENSTERRAND_PX)
        c.setSpacing(8)

        # Zone C: Hinweisband
        self.hinweisband = Hinweisband()
        c.addWidget(self.hinweisband)

        # Zone D/E: Tabelle und Editor
        self.splitter = QSplitter(Qt.Orientation.Horizontal)
        self.splitter.setObjectName("teiler")
        self.splitter.setChildrenCollapsible(False)
        self.tabelle = Warteschlangentabelle()
        self.editor = Editor(self._katalog)
        self.splitter.addWidget(self.tabelle)
        self.splitter.addWidget(self.editor)
        self.splitter.setStretchFactor(0, 65)
        self.splitter.setStretchFactor(1, 35)
        self.splitter.setSizes([650, 350])
        c.addWidget(self.splitter, 4)

        # Zone F: Fortschritt
        fortschritt = QFrame()
        fortschritt.setObjectName("fortschritt")
        fortschritt.setFixedHeight(t.HOEHE_FORTSCHRITT_PX)
        f = QHBoxLayout(fortschritt)
        f.setContentsMargins(0, 0, 0, 0)
        self.fortschritt_beschriftung = QLabel()
        self.fortschritt_beschriftung.setObjectName("fortschritt_beschriftung")
        self.fortschritt_beschriftung.setFont(schrift(fett=True))
        self.fortschritt_balken = QProgressBar()
        self.fortschritt_balken.setObjectName("fortschritt_balken")
        self.fortschritt_balken.setTextVisible(False)
        self.fortschritt_balken.setRange(0, 100)
        self.fortschritt_balken.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.fortschritt_balken.setAccessibleName("Fortschritt der laufenden Messung")
        self.fortschritt_text = KurzLabel()
        self.fortschritt_text.setObjectName("fortschritt_text")
        f.addWidget(self.fortschritt_beschriftung)
        f.addWidget(self.fortschritt_balken, 2)
        f.addWidget(self.fortschritt_text, 3)
        c.addWidget(fortschritt)

        # Zone G: Ereignisprotokoll
        self.protokoll = QPlainTextEdit()
        self.protokoll.setObjectName("protokoll")
        self.protokoll.setAccessibleName("Ereignisprotokoll")
        self.protokoll.setReadOnly(True)
        self.protokoll.setMaximumBlockCount(t.PROTOKOLL_MAX_BLOCKS)
        self.protokoll.setFont(schrift(t.SCHRIFT_PT_PROTOKOLL, mono=True))
        self.protokoll.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.protokoll.setTabChangesFocus(True)
        zeile = self.protokoll.fontMetrics().lineSpacing()
        # Protokoll auf Mindesthöhe (4 Zeilen): Tabelle und Editor haben Vorrang (K-U4, 5).
        self.protokoll.setFixedHeight(zeile * t.PROTOKOLL_MIN_ZEILEN + 12)
        c.addWidget(self.protokoll)

        haupt.addWidget(inhalt, 1)
        self.setCentralWidget(zentral)
        self._tab_reihenfolge()

    def _tab_reihenfolge(self) -> None:
        """Tabulatorreihenfolge A → B → C → D → E → G (F ist nicht fokussierbar)."""
        kette: list[QWidget] = [
            self.btn_betriebsart,
            self.btn_verbinden,
            self.btn_geraet,
            self.btn_einstellungen,
            *self._werkzeugknoepfe,
        ]
        h = self.hinweisband.hinweis
        if h is not None:
            for k in h.knoepfe:
                knopf = self.hinweisband.knopf(k.schluessel)
                if knopf is not None:
                    kette.append(knopf)
        kette.append(self.tabelle)
        kette.append(self.editor.erstes_feld())
        for vorher, nachher in itertools.pairwise(kette):
            QWidget.setTabOrder(vorher, nachher)
        QWidget.setTabOrder(self.editor.btn_uebernehmen, self.protokoll)

    def _verbinde_signale(self) -> None:
        self.btn_verbinden.clicked.connect(self._verbinden_knopf)
        self.btn_geraet.clicked.connect(self._geraet)
        self.btn_einstellungen.clicked.connect(self._einstellungen)
        self.hinweisband.knopf_geklickt.connect(self._band_knopf)
        self.tabelle.auswahl_geaendert.connect(self._auswahl)
        self.tabelle.editor_fokus.connect(self._editor_fokus)
        self.tabelle.entfernen_taste.connect(self._entfernen)
        self.tabelle.hoch_taste.connect(self._hoch)
        self.tabelle.runter_taste.connect(self._runter)
        self.editor.uebernehmen_angefordert.connect(self._uebernehmen)
        self.editor.verwerfen_angefordert.connect(self._verwerfen)
        self.editor.eingaben_verwerfen_angefordert.connect(self._eingaben_verwerfen)

    # --- austauschbare Ausführung (Tests ersetzen diese Methoden) -------------------------

    def _fuehre_aus(self, dialog: QDialog) -> int:  # pragma: no cover - modale Schleife
        """Führt einen Dialog modal aus."""
        return dialog.exec()

    def _angenommen(self, dialog: QDialog) -> bool:
        """Führt ``dialog`` aus; ``True``, wenn er angenommen wurde."""
        self._fuehre_aus(dialog)
        return dialog.result() == QDialog.DialogCode.Accepted.value

    def _pfad_speichern(self) -> str | None:  # pragma: no cover - modaler Dateidialog
        pfad, _f = QFileDialog.getSaveFileName(
            self, "Warteschlange speichern", self._dateiname or "", DATEIFILTER_WARTESCHLANGE
        )
        return pfad or None

    def _pfad_laden(self) -> str | None:  # pragma: no cover - modaler Dateidialog
        pfad, _f = QFileDialog.getOpenFileName(
            self, "Warteschlange laden", self._dateiname or "", DATEIFILTER_WARTESCHLANGE
        )
        return pfad or None

    def _oeffne_ordner(self, ordner: str) -> None:  # pragma: no cover - startet Dateimanager
        QDesktopServices.openUrl(QUrl.fromLocalFile(ordner))

    def _meldung(self, symbol: QMessageBox.Icon, titel: str, text: str) -> None:
        """Zeigt eine Meldung modal.

        Während :meth:`_zeige` läuft, wird sie nach dessen Ende nachgeholt (``QTimer``), damit
        der Aktualisierungspfad nicht mitten im Schreiben modal unterbrochen wird. Nach einer
        nachgeholten Meldung wird mit dem dann aktuellen Zustandsbild neu gezeichnet.
        """
        if self._in_zeige:
            QTimer.singleShot(0, lambda: self._meldung_nachgeholt(symbol, titel, text))
            return
        box = QMessageBox(symbol, titel, text, QMessageBox.StandardButton.Ok, self)
        box.setObjectName("meldung")
        self._fuehre_aus(box)

    def _meldung_nachgeholt(self, symbol: QMessageBox.Icon, titel: str, text: str) -> None:
        self._meldung(symbol, titel, text)
        self.aktualisiere()

    def _warnung(self, text: str) -> None:
        self._meldung(QMessageBox.Icon.Warning, "Nicht möglich", text)

    # --- Aktualisierung --------------------------------------------------------------------

    @property
    def bild(self) -> Zustandsbild:
        """Das zuletzt angezeigte Zustandsbild."""
        return self._bild

    def aktualisiere(self) -> None:
        """Holt Ereignisse und Zustandsbild ab und schreibt alle Zonen neu."""
        for ereignis in self._sitzung.hole_ereignisse():
            text = protokolltext(ereignis)
            if text is not None:
                self.protokolliere(text)
        self._zeige(self._sitzung.zustandsbild())

    def protokolliere(self, text: str) -> None:
        """Hängt eine Zeile ``HH:MM:SS  Text`` an; folgt dem Ende, wenn der Nutzer dort ist."""
        leiste = self.protokoll.verticalScrollBar()
        am_ende = leiste.value() >= leiste.maximum()
        alt = leiste.value()
        self.protokoll.appendPlainText(f"{datetime.now():%H:%M:%S}  {text}")
        if am_ende:
            leiste.setValue(leiste.maximum())
        else:
            leiste.setValue(alt)

    def _befehl_gesperrt(self, bild: Zustandsbild) -> bool:
        if self._sperre_revision is None:
            return False
        if (
            bild.revision > self._sperre_revision
            or time.monotonic() - self._sperre_seit > BEFEHL_SPERRE_MAX_S
        ):
            self._sperre_revision = None
            return False
        return True

    def _automatik(self, bild: Zustandsbild) -> None:
        """Verbindet im SIMULATOR selbst (Knopf dort deaktiviert)."""
        if bild.betriebsart != self._letzte_betriebsart:
            self._letzte_betriebsart = bild.betriebsart
            self._auto_verbinden_versucht = False
        if self._war_verbunden and not bild.verbunden:
            self._auto_verbinden_versucht = False
        self._war_verbunden = bild.verbunden
        if (
            bild.betriebsart is Betriebsart.SIMULATOR
            and not bild.verbunden
            and bild.durchgang in (Z.BEREIT, Z.BEENDET)
            and not self._auto_verbinden_versucht
        ):
            self._auto_verbinden_versucht = True
            try:
                self._sitzung.verbinde()
            except ValueError as fehler:
                self.protokolliere(f"Fehler: Simulator nicht verbunden: {fehler}")

    def _zeige(self, bild: Zustandsbild) -> None:
        aussen = not self._in_zeige
        self._in_zeige = True
        try:
            self._zeige_bild(bild)
        finally:
            if aussen:
                self._in_zeige = False

    def _zeige_bild(self, bild: Zustandsbild) -> None:
        self._bild = bild
        self._automatik(bild)
        z = bild.durchgang
        gesperrt = self._befehl_gesperrt(bild)

        # Zone A
        wort = BETRIEBSART_WORT[bild.betriebsart]
        self.setWindowTitle(fenstertitel(bild))
        self.btn_betriebsart.setText(wort)
        setze_eigenschaft(
            self.btn_betriebsart,
            "messen",
            "true" if bild.betriebsart is Betriebsart.MESSEN else "false",
        )
        self.act_betriebsart[bild.betriebsart].setChecked(True)
        self.lbl_durchgang.setText(f"Durchgang: {durchgang_text(bild)}")
        # Der Durchgangstext hat Vorrang: Verbindungs- und Strategietext werden zuerst gekürzt.
        self.lbl_durchgang.setMinimumWidth(
            min(self.lbl_durchgang.sizeHint().width(), DURCHGANG_MAX_BREITE_PX)
        )
        self.lbl_verbindung.setText(verbindung_text(bild))

        k = bedienbarkeit(bild, self.tabelle.gewaehlte_id())
        ba = k["betriebsart"]
        self.btn_betriebsart.setEnabled(ba.aktiv)
        self.btn_betriebsart.setToolTip(
            BETRIEBSART_TOOLTIP[bild.betriebsart] if ba.aktiv else ba.grund
        )
        self._setze_knopf(self.btn_verbinden, k["verbinden"])
        self._setze_knopf(self.btn_einstellungen, k["einstellungen"])
        self._setze_knopf(self.btn_geraet, k["geraet"])

        # Zone B
        for name, aktion in (
            ("messung_neu", self.act_messung_neu),
            ("pausenpunkt_neu", self.act_pausenpunkt_neu),
            ("entfernen", self.act_entfernen),
            ("hoch", self.act_hoch),
            ("runter", self.act_runter),
            ("speichern", self.act_speichern),
            ("laden", self.act_laden),
        ):
            self._setze_aktion(aktion, k[name], self._tasten_hinweis[name])
        for name, aktion, kuerzel in (
            ("start", self.act_start, "F5"),
            ("pause", self.act_pause, ""),
            ("abbrechen", self.act_abbrechen, "F8"),
        ):
            knopf = k[name]
            if gesperrt and knopf.aktiv:
                knopf = Knopf(False, "Befehl wird ausgeführt …", knopf.text)
            self._setze_aktion(aktion, knopf, kuerzel)
        self.act_bestaetigen.setEnabled(z is Z.WARTET_AUF_BESTAETIGUNG and not gesperrt)

        # Zone C
        schluessel = bild.durchgangsordner or ""
        h = hinweis(bild, beendet_quittiert=self._beendet_quittiert == schluessel)
        if self.hinweisband.zeige(h):
            self._tab_reihenfolge()
            if h is not None and h.alarm:
                QApplication.alert(self)
        for knopf_def in h.knoepfe if h is not None else ():
            b = self.hinweisband.knopf(knopf_def.schluessel)
            if b is not None:
                ablauf = knopf_def.schluessel not in ("ordner", "schliessen", "trennen")
                b.setEnabled(not (gesperrt and ablauf))

        # Zone D und E
        self.tabelle.zeige([e.id for e in bild.eintraege], zeilen(bild, self._katalog))
        self._editor_abgleich(bild)

        # Zone F
        fa = fortschritt_anzeige(bild)
        self.fortschritt_beschriftung.setText(fa.beschriftung)
        if fa.unbestimmt:
            self.fortschritt_balken.setRange(0, 0)
        else:
            self.fortschritt_balken.setRange(0, 100)
            if fa.wert is not None:
                self.fortschritt_balken.setValue(fa.wert)
        self.fortschritt_balken.setEnabled(fa.aktiv)
        self.fortschritt_text.setText(fa.text)

    @staticmethod
    def _setze_knopf(knopf: QWidget, k: Knopf) -> None:
        knopf.setEnabled(k.aktiv)
        if k.text is not None and hasattr(knopf, "setText"):
            knopf.setText(k.text)
        if not k.aktiv:
            knopf.setToolTip(k.grund)
        else:
            knopf.setToolTip("")

    @staticmethod
    def _setze_aktion(aktion: QAction, k: Knopf, taste: str) -> None:
        aktion.setEnabled(k.aktiv)
        if k.text is not None:
            aktion.setText(k.text)
        basis = aktion.text() + (f" ({taste})" if taste else "")
        aktion.setToolTip(basis if k.aktiv else f"{basis} – {k.grund}")

    def _editor_abgleich(self, bild: Zustandsbild) -> None:
        ed = self.editor
        nummern = {i: n.lang for i, n in nr_anzeige(bild).items()}
        if ed.modus in ("bearbeiten", "anzeigen"):
            e = finde(bild.eintraege, ed.eintrag_id)
            if e is None:
                ed.zeige_leer()
            elif ed.modus == "bearbeiten" and e.zustand != WARTEND:
                hatte_aenderungen = ed.geaendert
                ed.zeige_an(e, nummern.get(e.id))
                if hatte_aenderungen:
                    ed.zeige_konflikt(KONFLIKT_GESTARTET)
            elif ed.modus == "bearbeiten" and not ed.geaendert and ed.eintrag != e:
                ed.bearbeite(e, nummern.get(e.id))
            elif ed.modus == "anzeigen":
                ed.aktualisiere_anzeige(e, nummern.get(e.id))
        ed.setze_standard_limit(bild.standard_zeitlimit_s)
        k = bedienbarkeit(bild, ed.eintrag_id)
        if ed.modus == "neu_messung":
            ed.setze_uebernehmen_erlaubt(k["messung_neu"])
        elif ed.modus == "neu_pausenpunkt":
            ed.setze_uebernehmen_erlaubt(k["pausenpunkt_neu"])
        elif ed.modus == "bearbeiten":
            ed.setze_uebernehmen_erlaubt(k["uebernehmen"])

    # --- Tabelle und Editor ----------------------------------------------------------------

    def _verwirft_eingaben(self, neu_id: UUID | None) -> bool:
        """Prüft, ob der Auswahlwechsel ungespeicherte Editor-Eingaben verwerfen würde."""
        ed = self.editor
        if not ed.geaendert or ed.modus not in ("neu_messung", "neu_pausenpunkt", "bearbeiten"):
            return False
        if ed.modus == "bearbeiten":
            if neu_id == ed.eintrag_id:
                return False
            # Eintrag verschwunden (z. B. nach Laden): nichts mehr zurückzuholen.
            return finde(self._bild.eintraege, ed.eintrag_id) is not None
        return neu_id is not None  # Modus Neu bleibt bei aufgehobener Auswahl erhalten

    def _frage_eingaben_verwerfen(self) -> bool:
        box, ja = frage(
            self,
            "Änderungen verwerfen?",
            "Die Eingaben im Editor sind noch nicht übernommen.",
            "Verwerfen",
            "Zurück zum Editor",
        )
        box.setObjectName("dialog_eingaben_verwerfen")
        self._fuehre_aus(box)
        return box.clickedButton() is ja

    def _auswahl(self, eintrag_id: object) -> None:
        if self._auswahl_ruecksprung:
            return
        neu_id = eintrag_id if isinstance(eintrag_id, UUID) else None
        if self._verwirft_eingaben(neu_id) and not self._frage_eingaben_verwerfen():
            zurueck = (
                self.editor.eintrag_id
                if self.editor.modus == "bearbeiten"
                else self._letzte_auswahl
            )
            self._auswahl_ruecksprung = True
            try:
                self.tabelle.waehle(zurueck)
            finally:
                self._auswahl_ruecksprung = False
            self.editor.erstes_feld().setFocus(Qt.FocusReason.OtherFocusReason)
            return
        self._letzte_auswahl = neu_id
        bild = self._bild
        e = finde(bild.eintraege, neu_id)
        if e is None:
            if self.editor.modus in ("bearbeiten", "anzeigen"):
                self.editor.zeige_leer()
            return
        nr = _nr_text(bild, e.id)
        if e.zustand == WARTEND:
            self.editor.bearbeite(e, nr)
        else:
            self.editor.zeige_an(e, nr)
        self._editor_abgleich(bild)
        self._tab_reihenfolge()

    def _editor_fokus(self) -> None:
        self.editor.erstes_feld().setFocus(Qt.FocusReason.OtherFocusReason)

    def _neu(self, pausenpunkt: bool) -> None:
        bild = self._bild
        aktion = self.act_pausenpunkt_neu if pausenpunkt else self.act_messung_neu
        if not aktion.isEnabled():
            return
        index = index_von(bild.eintraege, self.tabelle.gewaehlte_id())
        position = einfuegeposition(bild, index)
        self._neu_am_anfang = position == 0
        self._neu_anker = bild.eintraege[position - 1].id if position > 0 else None
        ort = einfuegeort_text(
            bild.eintraege,
            position,
            durchgang_aktiv=bild.durchgang not in RUHE_ZUSTAENDE,
            ordner=bild.durchgangsordner,
        )
        if pausenpunkt:
            self.editor.neu_pausenpunkt(ort)
        else:
            self.editor.neu_messung(ort)
        self._editor_abgleich(bild)
        self._tab_reihenfolge()

    def _messung_neu(self) -> None:
        self._neu(pausenpunkt=False)

    def _pausenpunkt_neu(self) -> None:
        self._neu(pausenpunkt=True)

    def _einfuegeposition_jetzt(self) -> int:
        """Position zum Zeitpunkt von „Übernehmen“: hinter dem Anker, nie vor Gestartetes.

        Die Untergrenze liefert die Sitzung (``Zustandsbild.einfuegen_ab``, B8).
        """
        eintraege = self._bild.eintraege
        if self._neu_am_anfang or self._neu_anker is None:
            wunsch = 0
        else:
            i = index_von(eintraege, self._neu_anker)
            wunsch = len(eintraege) if i is None else i + 1
        return max(wunsch, self._bild.einfuegen_ab)

    def _uebernehmen(self) -> None:
        ed = self.editor
        self.aktualisiere()
        try:
            if ed.modus in ("neu_messung", "neu_pausenpunkt"):
                eintrag: Messung | Pausenpunkt
                if ed.modus == "neu_pausenpunkt":
                    eintrag = Pausenpunkt(text=ed.pausenpunkt_text())
                else:
                    m = ed.messung_eingaben()
                    eintrag = Messung(
                        name=m.name,
                        einstellungsdatei=m.einstellungsdatei,
                        parameter=m.parameter,
                        zeitlimit_s=m.zeitlimit_s,
                        notiz=m.notiz,
                    )
                self._sitzung.einfuegen(self._einfuegeposition_jetzt(), eintrag)
                neu_id = eintrag.id
            elif ed.modus == "bearbeiten" and ed.eintrag_id is not None:
                neu_id = ed.eintrag_id
                if ed.ist_pausenpunkt():
                    self._sitzung.bearbeiten(neu_id, text=ed.pausenpunkt_text())
                else:
                    m = ed.messung_eingaben()
                    self._sitzung.bearbeiten(
                        neu_id,
                        name=m.name,
                        einstellungsdatei=m.einstellungsdatei,
                        parameter=m.parameter,
                        zeitlimit_s=m.zeitlimit_s,
                        notiz=m.notiz,
                    )
            else:
                return
        except (ValueError, KeyError, IndexError) as fehler:
            text = fehler.args[0] if fehler.args else str(fehler)
            ed.zeige_konflikt(f"{t.symbol('fehler')} {text}")
            self.aktualisiere()
            return
        ed.geaendert = False
        self.aktualisiere()
        e = finde(self._bild.eintraege, neu_id)
        if e is not None:
            self.tabelle.waehle(neu_id)
            nr = _nr_text(self._bild, neu_id)
            if e.zustand == WARTEND:
                ed.bearbeite(e, nr)
            else:
                ed.zeige_an(e, nr)
            self._editor_abgleich(self._bild)

    def _verwerfen(self) -> None:
        ed = self.editor
        e = finde(self._bild.eintraege, self.tabelle.gewaehlte_id())
        if e is None:
            ed.zeige_leer()
        else:
            nr = _nr_text(self._bild, e.id)
            if e.zustand == WARTEND:
                ed.bearbeite(e, nr)
            else:
                ed.zeige_an(e, nr)
        self._editor_abgleich(self._bild)
        self.tabelle.setFocus(Qt.FocusReason.ShortcutFocusReason)

    def _eingaben_verwerfen(self) -> None:
        e = finde(self._bild.eintraege, self.editor.eintrag_id)
        if e is None:
            self.editor.zeige_leer()
            return
        nr = _nr_text(self._bild, e.id)
        if e.zustand == WARTEND:
            self.editor.bearbeite(e, nr)
        else:
            self.editor.zeige_an(e, nr)
        self._editor_abgleich(self._bild)

    def _gewaehlt(self) -> tuple[UUID, int] | None:
        eintrag_id = self.tabelle.gewaehlte_id()
        index = index_von(self._bild.eintraege, eintrag_id)
        if eintrag_id is None or index is None:
            return None
        return eintrag_id, index

    def _entfernen(self) -> None:
        if not self.act_entfernen.isEnabled() or (g := self._gewaehlt()) is None:
            return
        try:
            self._sitzung.entfernen(g[0])
        except (ValueError, KeyError) as fehler:
            self._warnung(str(fehler.args[0] if fehler.args else fehler))
        self.aktualisiere()

    def _verschiebe(self, aktion: QAction, delta: int) -> None:
        if not aktion.isEnabled() or (g := self._gewaehlt()) is None:
            return
        try:
            self._sitzung.verschieben(g[0], g[1] + delta)
        except (ValueError, KeyError, IndexError) as fehler:
            self._warnung(str(fehler.args[0] if fehler.args else fehler))
        self.aktualisiere()

    def _hoch(self) -> None:
        self._verschiebe(self.act_hoch, -1)

    def _runter(self) -> None:
        self._verschiebe(self.act_runter, +1)

    # --- Warteschlangendatei (3.7) ---------------------------------------------------------

    def ungespeichert(self) -> bool:
        """Prüft, ob sich die Definitionen seit dem letzten Speichern/Laden geändert haben."""
        return definitionen(self._bild) != self._gespeichert

    def _speichern(self) -> bool:
        if not self.act_speichern.isEnabled():
            return False
        roh = self._pfad_speichern()
        if not roh:
            return False
        pfad = Path(roh)
        if not pfad.name.endswith(ENDUNG_WARTESCHLANGE):
            pfad = pfad.with_name(pfad.name.removesuffix(".json") + ENDUNG_WARTESCHLANGE)
            if pfad.exists():
                box, ja = frage(
                    self,
                    "Datei ersetzen?",
                    f"Die Datei {pfad} existiert bereits. Ersetzen?",
                    "Ersetzen",
                    "Abbrechen",
                    ja_gefahr=True,
                )
                self._fuehre_aus(box)
                if box.clickedButton() is not ja:
                    return False
        try:
            self._sitzung.speichere_warteschlange(pfad, ueberschreiben=True)
        except (OSError, ValueError) as fehler:
            self._meldung(
                QMessageBox.Icon.Critical, "Datei kann nicht gespeichert werden", str(fehler)
            )
            return False
        self._dateiname = str(pfad)
        self.aktualisiere()
        self._gespeichert = definitionen(self._bild)
        self.protokolliere(f"Warteschlange gespeichert: {pfad}")
        return True

    def _laden(self) -> None:
        if not self.act_laden.isEnabled():
            return
        anzahl = len(self._bild.eintraege)
        if anzahl:
            box, ja = frage(
                self,
                "Warteschlange laden",
                f"Die aktuelle Warteschlange ({anzahl} Einträge) wird ersetzt. Fortfahren?",
                "Ersetzen",
                "Abbrechen",
            )
            self._fuehre_aus(box)
            if box.clickedButton() is not ja:
                return
        roh = self._pfad_laden()
        if not roh:
            return
        try:
            warnungen = self._sitzung.lade_warteschlange(Path(roh))
        except (OSError, ValueError) as fehler:
            self._meldung(QMessageBox.Icon.Critical, "Datei kann nicht geladen werden", str(fehler))
            self.aktualisiere()
            return
        self._dateiname = roh
        self.aktualisiere()
        self._gespeichert = definitionen(self._bild)
        self.protokolliere(f"Warteschlange geladen: {roh}")
        if warnungen:
            self.protokolliere(f"Warnung: {len(warnungen)} Einstellungsdateien nicht gefunden")

    # --- Ablauf ----------------------------------------------------------------------------

    def _befehl(self, fn: Callable[[], object], *, sperren: bool = True) -> bool:
        """Sendet einen Ablaufbefehl genau einmal; sperrt die Ablaufknöpfe bis zum nächsten Bild."""
        try:
            fn()
        except ValueError as fehler:
            self._warnung(str(fehler))
            return False
        # Basis ist die Revision der Sitzung direkt nach dem Senden, nicht das zuletzt
        # angezeigte Bild: sonst gäbe ein dazwischen erhöhtes Bild die Sperre sofort frei.
        if sperren:
            self._sperre_revision = self._sitzung.zustandsbild().revision
        self._sperre_seit = time.monotonic()
        self.aktualisiere()
        return True

    def _start(self) -> None:
        if not self.act_start.isEnabled():
            return
        # Schnappschuss beim Klick (K-U4): Die Sitzung startet nur, wenn Betriebsart und
        # Warteschlange danach unverändert sind, auch direkt aus BEENDET (B7).
        bild = self._bild
        art = start_dialog(bild)
        bestaetigt = False
        if art == "messen":
            dialog = DurchgangStartenDialog(bild.start_vorschau, bild.geraete_stand, self)
            if not self._angenommen(dialog):
                return
            bestaetigt = True
        elif art == "trockenlauf":
            box, ja = trockenlauf_dialog(self)
            self._fuehre_aus(box)
            if box.clickedButton() is not ja:
                return
        self._befehl(
            lambda: self._sitzung.starte(
                bild.durchgangsname,
                messen_bestaetigt=bestaetigt,
                erwartete_betriebsart=bild.betriebsart,
                erwartete_kennung=bild.warteschlangen_kennung,
            )
        )

    def _pause(self) -> None:
        if not self.act_pause.isEnabled():
            return
        if self._bild.durchgang is Z.PAUSIERT:
            self._befehl(self._sitzung.setze_fort)
        elif self._bild.durchgang is Z.LAEUFT:
            self._befehl(self._sitzung.pausiere)

    def _frage_abbrechen(self) -> bool:
        box, ja = abbrechen_dialog(self, messung_laeuft=abbruch_laeuft_messung(self._bild))
        self._fuehre_aus(box)
        return box.clickedButton() is ja

    def _abbrechen(self) -> None:
        if not self.act_abbrechen.isEnabled():
            return
        if self._frage_abbrechen():
            self._befehl(self._sitzung.brich_ab)

    def _bestaetigen(self) -> None:
        if not self.act_bestaetigen.isEnabled():
            return
        if self._bild.durchgang is Z.WARTET_AUF_BESTAETIGUNG:
            self._befehl(self._sitzung.bestaetige)

    def _band_knopf(self, schluessel: str) -> None:
        if schluessel == "trennen":
            self._befehl(self._sitzung.trenne)
        elif schluessel == "wiederholen":
            self._befehl(lambda: self._sitzung.entscheide(Fehlerentscheidung.WIEDERHOLEN))
        elif schluessel == "ueberspringen":
            self._befehl(lambda: self._sitzung.entscheide(Fehlerentscheidung.UEBERSPRINGEN))
        elif schluessel == "abbrechen":
            if self._frage_abbrechen():
                self._befehl(lambda: self._sitzung.entscheide(Fehlerentscheidung.ABBRECHEN))
        elif schluessel == "bestaetigen":
            self._bestaetigen()
        elif schluessel == "fortsetzen":
            self._pause()
        elif schluessel == "ordner":
            if self._bild.durchgangsordner:
                self._oeffne_ordner(self._bild.durchgangsordner)
        elif schluessel == "schliessen":
            self._beendet_quittiert = self._bild.durchgangsordner or ""
            self.aktualisiere()
        elif schluessel == "zuruecksetzen":
            self._zuruecksetzen()

    def _zuruecksetzen(self) -> None:
        """Zurücksetzen der Warteschlange (Nachtrag 2026-10-27, UI-29/UI-30)."""
        if not self._bild.zuruecksetzen_moeglich:
            return
        anzahl = echt_gemessen(self._bild)
        if anzahl:
            box, ja = frage(
                self,
                "Warteschlange zurücksetzen?",
                zuruecksetzen_frage_text(anzahl),
                "Zurücksetzen",
                "Abbrechen",
            )
            box.setObjectName("dialog_zuruecksetzen")
            self._fuehre_aus(box)
            if box.clickedButton() is not ja:
                return
        # Synchroner Befehl: Das Ergebnis steht im nächsten Bild, der Knopf verschwindet dann.
        if self._befehl(self._sitzung.zuruecksetzen, sperren=False):
            wartend = sum(1 for e in self._bild.eintraege if e.zustand == WARTEND)
            self.protokolliere(f"Warteschlange zurückgesetzt: {wartend} Einträge wartend.")

    # --- Statuszeile -----------------------------------------------------------------------

    def _betriebsart_gewaehlt(self, art: Betriebsart) -> None:
        bild = self._bild
        try:
            if art is bild.betriebsart:
                return
            if art is Betriebsart.MESSEN:
                dialog = MessenFreischaltenDialog(
                    voraussetzung_zeilen(self._sitzung.messen_voraussetzungen()), self
                )
                if not self._angenommen(dialog):
                    return
            try:
                self._sitzung.setze_betriebsart(art)
            except ValueError as fehler:
                self._warnung(str(fehler))
        finally:
            self.aktualisiere()
            self.act_betriebsart[self._bild.betriebsart].setChecked(True)

    def _verbinden_knopf(self) -> None:
        bild = self._bild
        if bild.durchgang is Z.GERAET_UNKLAR or bild.verbunden:
            self._befehl(self._sitzung.trenne)
        else:
            self._befehl(self._sitzung.verbinde)

    def _geraet(self) -> None:
        bild = self._bild
        self._fuehre_aus(
            GeraetDialog(
                bild.verbindung,
                self,
                stand=bild.geraete_stand,
                diagnose=bild.geraet_diagnose,
                konfiguration=bild.konfiguration,
            )
        )

    def _einstellungen(self) -> None:
        def setze(pfad: Path, limit_s: int) -> tuple[str | None, str | None]:
            # Beides oder nichts; die Prüfung macht die Sitzung (B4, K-U5b).
            try:
                self._sitzung.setze_einstellungen(pfad, float(limit_s))
            except EinstellungsFehler as fehler:
                return fehler.ordner, fehler.zeitlimit
            except ValueError as fehler:
                return str(fehler), None
            return None, None

        bild = self._bild
        self._fuehre_aus(
            EinstellungenDialog(
                bild.messdaten_wurzel,
                bild.standard_zeitlimit_s,
                setze,
                self,
                probleme=bild.messdaten_wurzel_probleme,
            )
        )
        self.aktualisiere()

    # --- Schließen (3.13) ------------------------------------------------------------------

    def closeEvent(self, event: QCloseEvent) -> None:  # noqa: N802  # Qt-Name
        """Verhindert das Schließen im Lauf; fragt bei ungespeicherter Warteschlange."""
        self.aktualisiere()
        entscheidung = schliessen_entscheidung(self._bild, ungespeichert=self.ungespeichert())
        if entscheidung == "sperren":
            self._meldung(
                QMessageBox.Icon.Information,
                "Durchgang läuft",
                "Es läuft ein Durchgang. Bitte zuerst abbrechen oder warten.",
            )
            event.ignore()
            return
        if entscheidung == "unklar":
            box, ja = frage(
                self,
                "Gerätezustand unklar",
                "PSV vorher prüfen.",
                "Trotzdem schließen",
                "Abbrechen",
                symbol=QMessageBox.Icon.Warning,
            )
            self._fuehre_aus(box)
            if box.clickedButton() is not ja:
                event.ignore()
                return
        elif entscheidung == "fragen":
            box = QMessageBox(self)
            box.setObjectName("dialog_schliessen")
            box.setIcon(QMessageBox.Icon.Question)
            box.setWindowTitle("Warteschlange nicht gespeichert")
            box.setText("Die Warteschlange hat ungespeicherte Änderungen.")
            speichern = box.addButton("Speichern", QMessageBox.ButtonRole.AcceptRole)
            verwerfen = box.addButton("Verwerfen", QMessageBox.ButtonRole.DestructiveRole)
            abbrechen = box.addButton("Abbrechen", QMessageBox.ButtonRole.RejectRole)
            box.setDefaultButton(abbrechen)
            box.setEscapeButton(abbrechen)
            self._fuehre_aus(box)
            geklickt = box.clickedButton()
            if geklickt is speichern:
                if not self._speichern():
                    event.ignore()
                    return
            elif geklickt is not verwerfen:
                event.ignore()
                return
        self._timer.stop()
        event.accept()
