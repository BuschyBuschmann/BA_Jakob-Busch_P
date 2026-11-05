"""Plotfläche der Auswertungsoberfläche (P-AUSW T3a, ADR-021, Brief K-AUSW Abschnitte 2 und 4).

:class:`PlotFlaeche` hält eine ``matplotlib.figure.Figure`` mit ``FigureCanvasQTAgg`` (nie
``pyplot``) und eine deutsche Werkzeugleiste. Die Schnittstelle ist schmal
(:meth:`PlotFlaeche.zeichne`), damit ein anderes Plotpaket als Rückfallweg möglich bleibt: Die
Oberfläche kennt weder Achsen noch Linien, nur die Zeichenfunktionen aus
:mod:`ldv_automation.darstellung`.

Beim Aufbau wird :meth:`~ldv_automation.darstellung.stil.Plotstil.rc` in die globalen
``rcParams`` übernommen (Schrift, Farben der Achsen) – nur in der Oberfläche; die
Zeichenfunktionen selbst setzen ihren Stil in einem ``rc_context``.

Dieses Modul ist ein dünnes Widget (Abdeckung nur mit ``pytest -m gui``, siehe
``pyproject.toml``); die Logik liegt in :mod:`.anzeige_auswerten` und den Zeichenfunktionen.
"""

from __future__ import annotations

from collections.abc import Callable
from pathlib import Path
from typing import Any

import matplotlib
import numpy as np
from matplotlib.backend_bases import FigureCanvasBase, MouseEvent
from matplotlib.backends.backend_qt import NavigationToolbar2QT
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from matplotlib.figure import Figure
from PySide6.QtCore import QEvent, QObject, QSize, Qt, QTimer, Signal
from PySide6.QtGui import QAction, QKeyEvent, QKeySequence
from PySide6.QtWidgets import QFrame, QToolButton, QVBoxLayout, QWidget

from ldv_automation.darstellung import Ansicht, Plotstil, Zeichnung
from ldv_automation.darstellung.bild import Stempel, speichere_arbeitsbild
from ldv_automation.darstellung.frf import zeichne_frf
from ldv_automation.darstellung.schwingform import zeichne_schwingform
from ldv_automation.darstellung.spektrum import zeichne_spektrum
from ldv_automation.darstellung.spitzen import zeichne_spitzen
from ldv_automation.gui.anzeige_aktionen import AKTIONS_TASTEN
from ldv_automation.gui.anzeige_auswerten import ANSICHT_NAMEN
from ldv_automation.gui.arbeitsbild import bild_grenzen, bild_optionen
from ldv_automation.gui.cursor import FadenkreuzCursor, naechste_linie
from ldv_automation.gui.stil import setze_eigenschaft

__all__ = ["NEUZEICHNEN_ANSICHTEN", "NEUZEICHNEN_MS", "PlotFlaeche", "PlotToolbar"]

NEUZEICHNEN_MS = 150
"""Entprellzeit: erst wenn die Größe so lange stillsteht, wird neu gezeichnet."""
NEUZEICHNEN_ANSICHTEN = frozenset({Ansicht.SPITZEN, Ansicht.SCHWINGFORM})
"""Ansichten, die Größen in pt zum Zeichenzeitpunkt messen (Beschriftungsabstände, Pfeillängen)
und deshalb bei Größenänderung der Figure neu gezeichnet werden. Ansicht 1 und 2 haben nur
Achsen im ``constrained``-Layout, das beim Skalieren des Canvas selbst nachzieht
(``draw_idle``); ein Neuzeichnen würde dort nur den Verlauf der Werkzeugleiste und die
y-Skalierung des Zooms verwerfen."""

MARKER_TREFFER_PX = 10
"""Größter Abstand (Pixel) zwischen Mausklick und Spitzenmarker, der den Marker trifft."""

CURSOR_ANSICHTEN = frozenset({Ansicht.SPEKTRUM, Ansicht.FRF, Ansicht.SPITZEN})
"""Ansichten mit Frequenzachse: nur dort gibt es Cursor und Klick-Frequenzwahl."""

Zeichner = Callable[[Figure, Any, Any, Plotstil], Zeichnung]

ZEICHNER: dict[Ansicht, Zeichner] = {
    Ansicht.SPEKTRUM: zeichne_spektrum,
    Ansicht.FRF: zeichne_frf,
    Ansicht.SPITZEN: zeichne_spitzen,
    Ansicht.SCHWINGFORM: zeichne_schwingform,
}
"""Zeichenfunktion je Ansicht (genau eine je Ansicht, gemeinsam mit den Thesis-Skripten)."""

# Namen der Knöpfe: Text -> objectName (eine Quelle für Beschriftung und Tests).
_KNOPF_NAMEN = {
    "Zurücksetzen": "btn_plot_zuruecksetzen",
    "Zurück": "btn_plot_zurueck",
    "Vor": "btn_plot_vor",
    "Verschieben": "btn_plot_verschieben",
    "Zoom": "btn_plot_zoom",
}


class PlotToolbar(NavigationToolbar2QT):
    """Deutsche Werkzeugleiste zu :class:`PlotFlaeche`: nur Textknöpfe, keine Bilddateien.

    Behalten sind Zurücksetzen, Zurück, Vor, Verschieben und Zoom (Brief K-AUSW Abschnitt 4).
    „Subplots“, „Customize“ und „Save“ der matplotlib-Leiste entfallen („Bild speichern …“
    ersetzt Save). Alle Knöpfe sind fokussierbar (UI-21). Nach Zurücksetzen, Zurück und Vor
    liegen die Achsen wieder im Layout der Figure (matplotlib nimmt sie dabei aus dem
    ``constrained``-Layout).
    """

    toolitems: list[tuple[str, ...] | tuple[None, ...]] = [  # noqa: RUF012  (Basisklasse)
        ("Zurücksetzen", "Zoom zurücksetzen (Pos1)", "home", "home"),
        ("Zurück", "Vorherige Ansicht", "back", "back"),
        ("Vor", "Nächste Ansicht", "forward", "forward"),
        (None, None, None, None),
        (
            "Verschieben",
            "Verschieben: linke Maustaste verschiebt, rechte Maustaste zoomt",
            "move",
            "pan",
        ),
        ("Zoom", "Auf einen Rechteckausschnitt zoomen", "zoom_to_rect", "zoom"),
    ]

    def __init__(self, canvas: FigureCanvasBase, parent: QWidget | None = None) -> None:
        super().__init__(canvas, parent, coordinates=False)  # type: ignore[no-untyped-call]
        self.setObjectName("plot_toolbar")
        self.setAccessibleName("Diagrammwerkzeuge")
        self.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextOnly)
        self.setMovable(False)
        for aktion in self.actions():
            knopf = self.widgetForAction(aktion)
            if isinstance(knopf, QToolButton):
                knopf.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
                knopf.setObjectName(_KNOPF_NAMEN.get(aktion.text(), ""))
                knopf.setAccessibleName(aktion.text())

    def knoepfe(self) -> list[QToolButton]:
        """Die Knöpfe der Leiste in Anzeigereihenfolge (für die Tab-Reihenfolge)."""
        alle = (self.widgetForAction(a) for a in self.actions())
        return [k for k in alle if isinstance(k, QToolButton)]

    def _layout_wiederherstellen(self) -> None:
        """Legt die Achsen nach einem Wechsel der Ansicht wieder ins Layout der Figure."""
        for achse in self.canvas.figure.get_axes():
            achse.set_in_layout(True)
        self.canvas.draw_idle()

    def home(self, *args: Any) -> None:
        """Zurücksetzen auf die Ausgangsansicht (Layout bleibt aktiv)."""
        super().home(*args)
        self._layout_wiederherstellen()

    def back(self, *args: Any) -> None:
        """Vorherige Ansicht (Layout bleibt aktiv)."""
        super().back(*args)
        self._layout_wiederherstellen()

    def forward(self, *args: Any) -> None:
        """Nächste Ansicht (Layout bleibt aktiv)."""
        super().forward(*args)
        self._layout_wiederherstellen()


class PlotFlaeche(QFrame):
    """Darstellungsfläche (Zone AE): Werkzeugleiste und Plot mit sichtbarem Fokusrahmen.

    Parameters
    ----------
    stil : Plotstil
        Stil der Oberfläche (:func:`ldv_automation.gui.plotstil.baue_plotstil`).
    parent : QWidget, optional
        Elternwidget.

    Notes
    -----
    Der Plot (``canvas``) ist fokussierbar (UI-21). Beim Fokus erhält der Rahmen die Eigenschaft
    ``fokus="true"`` (Stylesheet: 2 px ``C_AKZENT``).
    """

    fehler = Signal(str)
    """Meldet einen Fehler beim Neuzeichnen nach einer Größenänderung (Text der Ausnahme)."""
    cursor_bewegt = Signal(float)
    """Der Cursor steht auf einer neuen Linie (Frequenz der Linie in Hz)."""
    frequenz_geklickt = Signal(float)
    """Mausklick im Plot (Ansichten 1 bis 3): Frequenz der nächsten Linie in Hz."""
    cursor_uebernommen = Signal(float)
    """Enter im Plot: Frequenz der Cursorlinie in Hz."""
    spitze_geklickt = Signal(int)
    """Mausklick auf einen Spitzenmarker in Ansicht 3: Index der Spitze."""

    def __init__(self, stil: Plotstil, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setObjectName("plot")
        self._stil = stil
        matplotlib.rcParams.update(stil.rc())
        self._figure = Figure()
        self._canvas = FigureCanvasQTAgg(self._figure)  # type: ignore[no-untyped-call]
        self._canvas.setObjectName("plot_canvas")
        self._canvas.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self._canvas.setMinimumSize(0, 0)
        self._canvas.installEventFilter(self)
        self._toolbar = PlotToolbar(self._canvas, self)
        self._rahmen = QFrame(self)
        self._rahmen.setObjectName("plot_rahmen")
        rahmen_layout = QVBoxLayout(self._rahmen)
        rahmen_layout.setContentsMargins(0, 0, 0, 0)
        rahmen_layout.addWidget(self._canvas)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(4)
        layout.addWidget(self._toolbar)
        layout.addWidget(self._rahmen, 1)
        self._zeichnung: Zeichnung | None = None
        self._standard_x: tuple[float, float] | None = None
        self._ansicht: Ansicht | None = None
        self._zoom: dict[Ansicht, tuple[tuple[float, float], tuple[float, float]]] = {}
        self._letzter_aufruf: tuple[Ansicht, object, object, str] | None = None
        self._gezeichnet_groesse = QSize()
        self._neuzeichnen_timer = QTimer(self)
        self._neuzeichnen_timer.setObjectName("neuzeichnen")
        self._neuzeichnen_timer.setSingleShot(True)
        self._neuzeichnen_timer.setInterval(NEUZEICHNEN_MS)
        self._neuzeichnen_timer.timeout.connect(self._neuzeichnen)
        self._standard_grenzen: list[tuple[tuple[float, float], tuple[float, float]]] = []
        self._linien_hz: np.ndarray[Any, Any] | None = None
        self._cursor = FadenkreuzCursor(self._canvas, farbe=stil.text_gedaempft)
        self._canvas.mpl_connect("motion_notify_event", self._maus_bewegt)
        self._canvas.mpl_connect("button_press_event", self._maus_geklickt)
        # Pos1 setzt den Zoom zurück, solange der Fokus im Plot oder in der Werkzeugleiste liegt
        # (Brief K-AUSW Abschnitt 8; sonst bliebe Pos1 den Listen und Tabellen vorbehalten).
        self.act_zuruecksetzen = QAction("Zurücksetzen", self)
        self.act_zuruecksetzen.setObjectName("act_plot_zuruecksetzen")
        self.act_zuruecksetzen.setShortcut(QKeySequence(AKTIONS_TASTEN["zoom"][0]))
        self.act_zuruecksetzen.setShortcutContext(Qt.ShortcutContext.WidgetWithChildrenShortcut)
        self.act_zuruecksetzen.triggered.connect(self.zoom_zuruecksetzen)
        self.addAction(self.act_zuruecksetzen)

    # --- Zugriff ---------------------------------------------------------------------------

    @property
    def figure(self) -> Figure:
        """Die Figure der Fläche."""
        return self._figure

    @property
    def canvas(self) -> FigureCanvasQTAgg:
        """Der fokussierbare Plot."""
        return self._canvas

    @property
    def toolbar(self) -> PlotToolbar:
        """Die deutsche Werkzeugleiste."""
        return self._toolbar

    @property
    def zeichnung(self) -> Zeichnung | None:
        """Rückgabe der letzten Zeichenfunktion (Achsen, Linien); ``None`` = leer."""
        return self._zeichnung

    @property
    def letzter_aufruf(self) -> tuple[Ansicht, object, object] | None:
        """``(Ansicht, Daten, Optionen)`` der gezeigten Darstellung (``None`` = leer)."""
        if self._letzter_aufruf is None:
            return None
        ansicht, daten, optionen, _beschreibung = self._letzter_aufruf
        return ansicht, daten, optionen

    @property
    def fadenkreuz(self) -> FadenkreuzCursor:
        """Der Fadenkreuz-Cursor (für Tests und die Cursorzeile)."""
        return self._cursor

    def tab_kette(self) -> list[QWidget]:
        """Fokussierbare Teile in Tab-Reihenfolge: Plot, dann Werkzeugleiste (Brief Abschnitt 8)."""
        return [self._canvas, *self._toolbar.knoepfe()]

    # --- Zeichnen --------------------------------------------------------------------------

    def zeichne(
        self,
        ansicht: Ansicht,
        daten: object,
        optionen: object,
        beschreibung: str = "",
        *,
        zoom_behalten: bool = False,
    ) -> Zeichnung:
        """Zeichnet ``ansicht`` mit der gemeinsamen Zeichenfunktion in die Figure.

        Der Zoom wird zurückgesetzt: Die Standardansicht kommt als erster Eintrag in den Verlauf
        der Werkzeugleiste, damit „Zurücksetzen“ nach dem Zoomen den Ausgangsbereich
        wiederherstellt.

        Parameters
        ----------
        ansicht : Ansicht
            Welche der vier Ansichten.
        daten, optionen : object
            Daten und Optionen der Zeichenfunktion (``SpektrumDaten``/``SpektrumOptionen`` …).
        beschreibung : str, optional
            Textalternative des Plots (``accessibleDescription``).
        zoom_behalten : bool, optional
            ``True``: Der Frequenzausschnitt (x) bleibt je Ansicht erhalten, wenn dieselbe Ansicht
            mit derselben Frequenzachse neu gezeichnet wird (Wechsel von Punkt, Komponente,
            Größe oder Skala, aber auch nach dem Besuch einer anderen Ansicht); die y-Achse
            skaliert neu, weil sich die Werte ändern. „Zurücksetzen“
            führt weiter auf den Ausgangsbereich. Ein neuer Dateiaufruf übergibt ``False``.

        Returns
        -------
        Zeichnung
            Hilfsobjekte der Zeichenfunktion.
        """
        self._merke_zoom()  # Zoom (x) der Ansicht, die gleich verlassen wird (je Ansicht, UI-12)
        if not zoom_behalten:
            self._zoom.clear()
        zeichnung = ZEICHNER[ansicht](self._figure, daten, optionen, self._stil)
        # Cursor vor dem Zeichnen anlegen: das draw_event nimmt den Hintergrund auf (Blitting).
        # Ansicht 4 zeigt Ortskoordinaten und hat keine Frequenzachse, also keinen Cursor.
        frequenz = getattr(daten, "frequenz_hz", None) if ansicht in CURSOR_ANSICHTEN else None
        self._linien_hz = np.asarray(frequenz, dtype=np.float64) if frequenz is not None else None
        self._cursor.anlegen(zeichnung.achsen, self._linien_hz)
        # Erst zeichnen, dann Standardansicht merken: constrained-Layout kennt die Positionen
        # erst nach dem Zeichnen.
        self._canvas.draw()  # type: ignore[no-untyped-call]
        self._toolbar.update()
        self._toolbar.push_current()
        standard_x = zeichnung.achsen[0].get_xlim()
        self._standard_grenzen = [(ax.get_xlim(), ax.get_ylim()) for ax in zeichnung.achsen]
        gemerkt = self._zoom.get(ansicht)
        if (
            zoom_behalten
            and ansicht is not Ansicht.SCHWINGFORM  # Ortskoordinaten: Zoom ist dort kein Ziel
            and gemerkt is not None
            and np.allclose(gemerkt[0], standard_x, rtol=1e-12, atol=0.0)
            and not np.allclose(gemerkt[1], standard_x, rtol=1e-12, atol=0.0)
        ):
            # Achsen teilen die Frequenzachse (Ansicht 2: sharex); der Ausschnitt gilt für alle.
            zeichnung.achsen[0].set_xlim(gemerkt[1])
            self._canvas.draw()  # type: ignore[no-untyped-call]
            self._toolbar.push_current()
        self._standard_x = standard_x
        self._ansicht = ansicht
        self._zeichnung = zeichnung
        self._letzter_aufruf = (ansicht, daten, optionen, beschreibung)
        self._gezeichnet_groesse = self._canvas.size()
        self._canvas.setAccessibleName(f"Diagramm: {ANSICHT_NAMEN[ansicht.value]}")
        self._canvas.setAccessibleDescription(beschreibung)
        return zeichnung

    def _merke_zoom(self) -> None:
        if (
            self._zeichnung is not None
            and self._ansicht is not None
            and self._standard_x is not None
        ):
            self._zoom[self._ansicht] = (self._standard_x, self._zeichnung.achsen[0].get_xlim())

    def zoom_vergessen(self) -> None:
        """Löscht den gemerkten Zoom aller Ansichten (Dateiwechsel)."""
        self._zoom.clear()

    def leere(self, *, zoom_vergessen: bool = False) -> None:
        """Löscht die Darstellung (Figure leer, Verlauf der Werkzeugleiste leer).

        Der Zoom bleibt gemerkt (ein einzelner Zeichenfehler verwirft ihn nicht); nur beim
        Dateiwechsel (``zoom_vergessen=True``) wird er für alle Ansichten gelöscht.

        Parameters
        ----------
        zoom_vergessen : bool, optional
            ``True`` löscht zusätzlich den gemerkten Zoom aller Ansichten.
        """
        self._merke_zoom()
        self._cursor.abbauen()
        self._linien_hz = None
        self._figure.clear()
        self._canvas.draw_idle()  # type: ignore[no-untyped-call]
        self._toolbar.update()
        self._zeichnung = None
        self._standard_x = None
        self._ansicht = None
        if zoom_vergessen:
            self._zoom.clear()
            self._cursor.vergiss()
        self._letzter_aufruf = None
        self._neuzeichnen_timer.stop()
        self._canvas.setAccessibleDescription("")

    def zoom_zuruecksetzen(self) -> None:
        """Stellt den Ausgangsbereich wieder her (Knopf „Zurücksetzen“, Pos1)."""
        self._toolbar.home()

    # --- Cursor, Klick und Tastatur ----------------------------------------------------------

    def setze_cursor(self, f_hz: float) -> float | None:
        """Setzt den Cursor auf die Linie, die ``f_hz`` am nächsten liegt (Ansichten 1 bis 3).

        Parameters
        ----------
        f_hz : float
            Frequenz in Hz.

        Returns
        -------
        float or None
            Frequenz der Linie; ``None``, wenn es keinen Cursor gibt (Ansicht 4, leere Fläche
            oder Blitting nicht verfügbar).
        """
        gerastet = self._cursor.setze(f_hz)
        if gerastet is not None:
            self.cursor_bewegt.emit(gerastet)
        return gerastet

    def cursor_schritt(self, anzahl: int) -> float | None:
        """Bewegt den Cursor um ``anzahl`` Linien (←/→ eine, Umschalt ±10)."""
        gerastet = self._cursor.schritt(anzahl)
        if gerastet is not None:
            self.cursor_bewegt.emit(gerastet)
        return gerastet

    def _mit_werkzeug(self) -> bool:
        """Zoom oder Verschieben ist aktiv: Maus und Cursor gehören dann dem Werkzeug."""
        return bool(self._toolbar.mode)

    def _maus_bewegt(self, ereignis: MouseEvent) -> None:
        if self._ansicht not in CURSOR_ANSICHTEN or self._mit_werkzeug():
            return
        if ereignis.inaxes is None or ereignis.xdata is None:
            return
        if self._cursor.verfuegbar:
            alt = self._cursor.index
            gerastet = self._cursor.setze(float(ereignis.xdata))
            if gerastet is not None and self._cursor.index != alt:
                self.cursor_bewegt.emit(gerastet)

    def _maus_geklickt(self, ereignis: MouseEvent) -> None:
        """Linksklick: Frequenz der nächsten Linie melden, bei Treffer einer Spitze auch diese."""
        if self._ansicht not in CURSOR_ANSICHTEN or self._mit_werkzeug():
            return
        if ereignis.button != 1 or ereignis.dblclick:
            return
        if ereignis.inaxes is None or ereignis.xdata is None or self._linien_hz is None:
            return
        f = float(self._linien_hz[naechste_linie(self._linien_hz, float(ereignis.xdata))])
        gerastet = self._cursor.setze(f)
        if gerastet is not None:
            self.cursor_bewegt.emit(gerastet)
        treffer = self._spitze_unter_maus(ereignis)
        self.frequenz_geklickt.emit(f)
        if treffer is not None:
            self.spitze_geklickt.emit(treffer)

    def _spitze_unter_maus(self, ereignis: MouseEvent) -> int | None:
        """Index des Spitzenmarkers unter dem Mauszeiger (Ansicht 3), sonst ``None``."""
        if self._ansicht is not Ansicht.SPITZEN or self._zeichnung is None:
            return None
        aufruf = self._letzter_aufruf
        spitzen = getattr(aufruf[1], "spitzen", ()) if aufruf is not None else ()
        if not spitzen:
            return None
        punkte = np.array([[s.f_sp_hz, s.hoehe] for s in spitzen], dtype=np.float64)
        achse = self._zeichnung.achsen[0]
        bild = achse.transData.transform(punkte)
        abstand = np.hypot(bild[:, 0] - ereignis.x, bild[:, 1] - ereignis.y)
        abstand[~np.isfinite(abstand)] = np.inf
        index = int(np.argmin(abstand))
        return index if abstand[index] <= MARKER_TREFFER_PX else None

    def _taste(self, ereignis: QKeyEvent) -> bool:
        """←/→ bewegen den Cursor, Enter übernimmt seine Frequenz; ``True`` = verbraucht."""
        stoerend = (
            Qt.KeyboardModifier.ControlModifier
            | Qt.KeyboardModifier.AltModifier
            | Qt.KeyboardModifier.MetaModifier
        )
        if ereignis.modifiers() & stoerend or self._ansicht not in CURSOR_ANSICHTEN:
            return False
        taste = ereignis.key()
        if taste in (Qt.Key.Key_Left, Qt.Key.Key_Right):
            n = 10 if ereignis.modifiers() & Qt.KeyboardModifier.ShiftModifier else 1
            richtung = -1 if taste == Qt.Key.Key_Left else 1
            return self.cursor_schritt(richtung * n) is not None
        if taste in (Qt.Key.Key_Return, Qt.Key.Key_Enter):
            f = self._cursor.frequenz_hz
            if f is None:
                return False
            self.cursor_uebernommen.emit(f)
            return True
        return False

    # --- Bild speichern ----------------------------------------------------------------------

    def speichere(self, pfad: Path, stempel: Stempel) -> Zeichnung:
        """Schreibt die gezeigte Ansicht als Arbeitsbild (PNG oder PDF) mit Stempel (UI-17).

        Das Bild entsteht mit derselben Zeichenfunktion und denselben Daten auf einer **neuen**
        Figure; die Bildschirmfigur bleibt unverändert. Es nimmt die Voreinstellungen der
        Zeichenfunktion (Legende, Streifen und Kasten in Ansicht 3, ADR-026 Nachtrag 2) und
        übernimmt den Zoom (:func:`~ldv_automation.gui.arbeitsbild.bild_grenzen`).

        Parameters
        ----------
        pfad : pathlib.Path
            Ziel; die Endung ``.png`` oder ``.pdf`` bestimmt das Format.
        stempel : Stempel
            Fußstempel.

        Raises
        ------
        RuntimeError
            Es ist nichts gezeichnet.
        ValueError
            Endung weder ``.png`` noch ``.pdf``.
        """
        if self._letzter_aufruf is None or self._zeichnung is None:
            raise RuntimeError("Es ist keine Darstellung zum Speichern vorhanden.")
        ansicht, daten, optionen, _beschreibung = self._letzter_aufruf
        optionen_bild = bild_optionen(ansicht, optionen)
        grenzen = bild_grenzen(ansicht, self._zeichnung.achsen, self._standard_grenzen)
        zeichner = ZEICHNER[ansicht]
        return speichere_arbeitsbild(
            lambda fig: zeichner(fig, daten, optionen_bild, self._stil),
            pfad,
            stempel,
            self._stil,
            grenzen=grenzen,
        )

    # --- Größenänderung ----------------------------------------------------------------------

    def _neuzeichnen(self) -> None:
        """Zeichnet die aktuelle Ansicht mit denselben Daten und Optionen neu (Zoom x bleibt)."""
        if self._letzter_aufruf is None or self._canvas.size() == self._gezeichnet_groesse:
            return
        ansicht, daten, optionen, beschreibung = self._letzter_aufruf
        try:
            self.zeichne(ansicht, daten, optionen, beschreibung, zoom_behalten=True)
        except Exception as fehler:  # Zeichenfunktion scheitert: melden statt verschlucken
            self.fehler.emit(str(fehler))

    # --- Fokusrahmen -----------------------------------------------------------------------

    def eventFilter(self, watched: QObject, event: QEvent) -> bool:  # noqa: N802  # Qt-Name
        """Zeigt den Fokusrahmen, solange der Plot den Tastaturfokus hat."""
        if watched is self._canvas:
            if event.type() == QEvent.Type.Resize:
                if self._ansicht in NEUZEICHNEN_ANSICHTEN:
                    self._neuzeichnen_timer.start()  # entprellt: jedes Resize startet neu
            elif event.type() == QEvent.Type.KeyPress and isinstance(event, QKeyEvent):
                if self._taste(event):
                    return True
            elif event.type() == QEvent.Type.FocusIn:
                setze_eigenschaft(self._rahmen, "fokus", "true")
            elif event.type() == QEvent.Type.FocusOut:
                setze_eigenschaft(self._rahmen, "fokus", "false")
        return super().eventFilter(watched, event)
