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

import dataclasses
import math
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
from ldv_automation.gui.achsen_zustand import ACHSEN_JE_ANSICHT, AchsenZustand
from ldv_automation.gui.anzeige_aktionen import AKTIONS_TASTEN
from ldv_automation.gui.anzeige_auswerten import ANSICHT_NAMEN
from ldv_automation.gui.arbeitsbild import bild_optionen
from ldv_automation.gui.cursor import FadenkreuzCursor, naechste_linie
from ldv_automation.gui.stil import setze_eigenschaft

__all__ = ["NEUZEICHNEN_ANSICHTEN", "NEUZEICHNEN_MS", "PlotFlaeche", "PlotToolbar"]

NEUZEICHNEN_MS = 150
"""Entprellzeit: erst wenn die Größe so lange stillsteht, wird neu gezeichnet."""
NEUZEICHNEN_ANSICHTEN = frozenset({Ansicht.SPITZEN, Ansicht.SCHWINGFORM})
"""Ansichten, die Größen in pt zum Zeichenzeitpunkt messen (Beschriftungsabstände, Pfeillängen)
und deshalb bei Größenänderung der Figure neu gezeichnet werden. Ansicht 1 und 2 haben nur
Achsen im ``constrained``-Layout, das beim Skalieren des Canvas selbst nachzieht
(``draw_idle``); ein Neuzeichnen wäre dort unnötig. Das Neuzeichnen in Ansicht 3 und 4 liest
die Achsengrenzen aus dem :class:`~ldv_automation.gui.achsen_zustand.AchsenZustand` (Zoom und
Verschieben stehen dort als feste Werte, F3) und setzt den Verlauf der Werkzeugleiste auf den
festen Ausschnitt zurück."""

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
    ersetzt Save). Alle Knöpfe sind fokussierbar (UI-21). Nach Zurück und Vor liegen die Achsen
    wieder im Layout der Figure (matplotlib nimmt sie dabei aus dem ``constrained``-Layout).

    Rückkopplung zu den Achsenfeldern (R-073, P-AUSW2 S2): Ein abgeschlossener Zoom oder
    Verschiebevorgang (``push_current``) sowie Zurück und Vor melden :attr:`bereich_geaendert`;
    „Zurücksetzen“ meldet :attr:`zuruecksetzen` (Bedeutung „Auto für die Ansicht“ legt
    :class:`PlotFlaeche` fest). Die Fläche selbst ruft ``push_current`` beim Zeichnen mit
    ``melden = False`` auf, damit daraus keine Meldung und keine Schleife entsteht (gemessen im
    Spike: Zoom und Verschieben je genau eine Meldung, Zurück/Vor/Zurücksetzen je eine).
    """

    bereich_geaendert = Signal()
    """Zoom, Verschieben, Zurück oder Vor haben die sichtbaren Grenzen der Achsen geändert."""
    zuruecksetzen = Signal()
    """Der Knopf „Zurücksetzen“ (Pos1) wurde ausgelöst."""

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
        self.melden = True
        """``False``: ``push_current`` meldet nicht (eigenes Zeichnen der Fläche)."""
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

    def push_current(self) -> None:
        """Merkt die Ansicht im Verlauf und meldet die neuen Grenzen (außer beim Zeichnen)."""
        super().push_current()
        if self.melden:
            self.bereich_geaendert.emit()

    def home(self, *args: Any) -> None:
        """Zurücksetzen: meldet :attr:`zuruecksetzen` (die Fläche stellt „Auto“ her)."""
        self.zuruecksetzen.emit()

    def stapel_home(self) -> None:
        """Zurücksetzen auf die erste Ansicht des Verlaufs (Ansicht 4 ohne Achsenwahl)."""
        super().home()
        self._layout_wiederherstellen()

    def back(self, *args: Any) -> None:
        """Vorherige Ansicht (Layout bleibt aktiv)."""
        super().back(*args)
        self._layout_wiederherstellen()
        self.bereich_geaendert.emit()

    def forward(self, *args: Any) -> None:
        """Nächste Ansicht (Layout bleibt aktiv)."""
        super().forward(*args)
        self._layout_wiederherstellen()
        self.bereich_geaendert.emit()


class PlotFlaeche(QFrame):
    """Darstellungsfläche (Zone AE): Werkzeugleiste und Plot mit sichtbarem Fokusrahmen.

    Parameters
    ----------
    stil : Plotstil
        Stil der Oberfläche (:func:`ldv_automation.gui.plotstil.baue_plotstil`).
    parent : QWidget, optional
        Elternwidget.
    achsen_zustand : AchsenZustand, optional
        Bereiche und Skalen je Ansicht (R-073, **die** Quelle der Achsengrenzen); ohne Angabe
        legt die Fläche einen eigenen an.

    Notes
    -----
    Der Plot (``canvas``) ist fokussierbar (UI-21). Beim Fokus erhält der Rahmen die Eigenschaft
    ``fokus="true"`` (Stylesheet: 2 px ``C_AKZENT``).

    Achsengrenzen (P-AUSW2 S2, ADR-028): Es gibt nur eine Quelle, den
    :class:`~ldv_automation.gui.achsen_zustand.AchsenZustand`. :meth:`zeichne` reicht ihn als
    ``achsen`` an die Zeichenfunktion (Ansichten 1 bis 3). Zoom und Verschieben der Werkzeugleiste
    schreiben die sichtbaren Grenzen als feste Werte in den Zustand (:attr:`achsen_geaendert`),
    „Zurücksetzen“ (Knopf, Pos1) setzt die Ansicht auf Auto und zeichnet neu. Grenzen, die
    jemand ohne Werkzeugleiste an den Achsen ändert, übernimmt die Fläche vor jedem Zeichnen,
    Leeren und Speichern (:meth:`_synchronisiere`); so geht kein Ausschnitt verloren.
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
    achsen_geaendert = Signal()
    """Zoom, Verschieben, Verlauf oder Zurücksetzen haben den Achsenzustand geändert (R-073)."""
    grenzen_gezeichnet = Signal(int)
    """Nach jedem Zeichnen: Nummer der Ansicht; die wirksamen Grenzen stehen in
    :meth:`wirksame_grenzen` (die Achsenleiste zeigt Auto-Werte grau)."""

    def __init__(
        self,
        stil: Plotstil,
        parent: QWidget | None = None,
        achsen_zustand: AchsenZustand | None = None,
    ) -> None:
        super().__init__(parent)
        self.setObjectName("plot")
        self._achsen = achsen_zustand if achsen_zustand is not None else AchsenZustand()
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
        self._ansicht: Ansicht | None = None
        self._bekannt: dict[str, tuple[float, float]] | None = None
        self._letzter_aufruf: tuple[Ansicht, object, object, str] | None = None
        self._gezeichnet_groesse = QSize()
        self._neuzeichnen_timer = QTimer(self)
        self._neuzeichnen_timer.setObjectName("neuzeichnen")
        self._neuzeichnen_timer.setSingleShot(True)
        self._neuzeichnen_timer.setInterval(NEUZEICHNEN_MS)
        self._neuzeichnen_timer.timeout.connect(self._neuzeichnen)
        self._linien_hz: np.ndarray[Any, Any] | None = None
        self._toolbar.bereich_geaendert.connect(self._werkzeug_hat_geaendert)
        self._toolbar.zuruecksetzen.connect(self.zoom_zuruecksetzen)
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
    def achsen_zustand(self) -> AchsenZustand:
        """Bereiche und Skalen je Ansicht (die eine Quelle der Achsengrenzen)."""
        return self._achsen

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

        Die Achsengrenzen kommen aus dem :class:`AchsenZustand` (Ansichten 1 bis 3): Die Fläche
        setzt ihn als ``achsen`` in die Optionen. Vorher übernimmt sie Grenzen, die an den Achsen
        der bisherigen Darstellung geändert wurden (:meth:`_synchronisiere`). Die Standardansicht
        kommt als erster Eintrag in den Verlauf der Werkzeugleiste.

        Parameters
        ----------
        ansicht : Ansicht
            Welche der vier Ansichten.
        daten, optionen : object
            Daten und Optionen der Zeichenfunktion (``SpektrumDaten``/``SpektrumOptionen`` …).
        beschreibung : str, optional
            Textalternative des Plots (``accessibleDescription``).
        zoom_behalten : bool, optional
            Ohne Wirkung: Den Ausschnitt hält der Achsenzustand (eine Quelle). Der Parameter
            bleibt bis P-AUSW2 S10, damit Aufrufer und Tests nicht brechen.

        Returns
        -------
        Zeichnung
            Hilfsobjekte der Zeichenfunktion.

        Raises
        ------
        ldv_automation.darstellung.achsen.AchsenFehler
            Der Achsenzustand enthält einen ungültigen Bereich (die Oberfläche prüft Eingaben
            vorher; das ist die Absicherung).
        """
        del zoom_behalten
        self._synchronisiere()
        zeichnung = ZEICHNER[ansicht](
            self._figure, daten, self._mit_achsen(ansicht, optionen), self._stil
        )
        # Cursor vor dem Zeichnen anlegen: das draw_event nimmt den Hintergrund auf (Blitting).
        # Ansicht 4 zeigt Ortskoordinaten und hat keine Frequenzachse, also keinen Cursor.
        frequenz = getattr(daten, "frequenz_hz", None) if ansicht in CURSOR_ANSICHTEN else None
        self._linien_hz = np.asarray(frequenz, dtype=np.float64) if frequenz is not None else None
        self._cursor.anlegen(zeichnung.achsen, self._linien_hz)
        # Erst zeichnen, dann Standardansicht merken: constrained-Layout kennt die Positionen
        # erst nach dem Zeichnen.
        self._canvas.draw()  # type: ignore[no-untyped-call]
        self._toolbar.melden = False  # eigenes Zeichnen ist keine Eingabe des Nutzers
        try:
            self._toolbar.update()
            self._toolbar.push_current()
        finally:
            self._toolbar.melden = True
        self._ansicht = ansicht
        self._zeichnung = zeichnung
        self._bekannt = self._lese_grenzen(ansicht, zeichnung)
        self._letzter_aufruf = (ansicht, daten, optionen, beschreibung)
        self._gezeichnet_groesse = self._canvas.size()
        self._canvas.setAccessibleName(f"Diagramm: {ANSICHT_NAMEN[ansicht.value]}")
        self._canvas.setAccessibleDescription(beschreibung)
        self.grenzen_gezeichnet.emit(ansicht.value)
        return zeichnung

    # --- Achsengrenzen: eine Quelle (R-073) ---------------------------------------------------

    def _mit_achsen(self, ansicht: Ansicht, optionen: object) -> object:
        """Setzt die Achsenoptionen des Zustands in die Optionen der Zeichenfunktion.

        Nur Optionen mit dem Feld ``achsen`` und nur Ansichten mit Achsenwahl (1 bis 3); alles
        andere (Ansicht 4, Attrappen ohne Optionen) bleibt unverändert.
        """
        if ansicht.value not in ACHSEN_JE_ANSICHT:
            return optionen
        if not dataclasses.is_dataclass(optionen) or isinstance(optionen, type):
            return optionen
        if not any(feld.name == "achsen" for feld in dataclasses.fields(optionen)):
            return optionen
        return dataclasses.replace(
            optionen,
            achsen=self._achsen.optionen(ansicht.value),
        )

    @staticmethod
    def _lese_grenzen(ansicht: Ansicht, zeichnung: Zeichnung) -> dict[str, tuple[float, float]]:
        """Sichtbare Grenzen je Rolle (``frequenz`` sowie ``betrag``/``phase``) der Zeichnung."""
        if ansicht.value not in ACHSEN_JE_ANSICHT or not zeichnung.achsen:
            return {}
        x = zeichnung.achsen[0].get_xlim()
        grenzen = {"frequenz": (float(x[0]), float(x[1]))}
        for achse, rolle in zip(zeichnung.achsen, zeichnung.rollen, strict=False):
            if rolle in ACHSEN_JE_ANSICHT[ansicht.value]:
                y = achse.get_ylim()
                grenzen[rolle] = (float(y[0]), float(y[1]))
        return grenzen

    def wirksame_grenzen(self) -> dict[str, tuple[float, float]]:
        """Grenzen der gezeigten Darstellung je Rolle (leer ohne Darstellung oder in Ansicht 4)."""
        return dict(self._bekannt) if self._bekannt else {}

    def _synchronisiere(self) -> bool:
        """Schreibt Grenzen, die seit dem Zeichnen an den Achsen geändert wurden, in den Zustand.

        Zoom, Verschieben und Verlauf der Werkzeugleiste kommen über :attr:`bereich_geaendert`;
        das hier fängt jede andere Änderung (z. B. direktes ``set_xlim``) ab, damit sie das
        Neuzeichnen übersteht. Verglichen wird je Rolle mit den Grenzen beim Zeichnen
        (relative Toleranz 1e-12); nur geänderte Rollen werden fest (F3).

        Returns
        -------
        bool
            ``True``, wenn der Zustand geändert wurde.
        """
        if self._zeichnung is None or self._ansicht is None or self._bekannt is None:
            return False
        aktuell = self._lese_grenzen(self._ansicht, self._zeichnung)
        geaendert = False
        for rolle, (von, bis) in aktuell.items():
            alt = self._bekannt.get(rolle)
            if alt is not None and all(
                math.isclose(n, o, rel_tol=1e-12, abs_tol=0.0)
                for n, o in zip((von, bis), alt, strict=True)
            ):
                continue
            self._achsen.uebernehme_grenzen(self._ansicht.value, rolle, von, bis)
            geaendert = True
        self._bekannt = aktuell
        return geaendert

    def _werkzeug_hat_geaendert(self) -> None:
        """Zoom, Verschieben, Zurück oder Vor der Werkzeugleiste: Grenzen in den Zustand."""
        if self._synchronisiere():
            self.achsen_geaendert.emit()

    def neue_datei(self) -> None:
        """Neue Datei (Ersetzen): Bereiche zurücksetzen, Skalen bleiben (UI-6)."""
        self._achsen.bei_neuer_datei()
        self._bekannt = None  # Grenzen der alten Darstellung gehören nicht in den neuen Zustand

    def leere(self, *, zoom_vergessen: bool = False) -> None:
        """Löscht die Darstellung (Figure leer, Verlauf der Werkzeugleiste leer).

        Der Achsenzustand bleibt (ein einzelner Zeichenfehler verwirft den Ausschnitt nicht);
        nur beim Dateiwechsel (``zoom_vergessen=True``) werden die Bereiche zurückgesetzt.

        Parameters
        ----------
        zoom_vergessen : bool, optional
            ``True`` setzt zusätzlich die Bereiche aller Ansichten auf Auto (Skalen bleiben).
        """
        self._synchronisiere()
        self._cursor.abbauen()
        self._linien_hz = None
        self._figure.clear()
        self._canvas.draw_idle()  # type: ignore[no-untyped-call]
        self._toolbar.melden = False
        try:
            self._toolbar.update()
        finally:
            self._toolbar.melden = True
        self._zeichnung = None
        self._ansicht = None
        self._bekannt = None
        if zoom_vergessen:
            self._achsen.bei_neuer_datei()
            self._cursor.vergiss()
        self._letzter_aufruf = None
        self._neuzeichnen_timer.stop()
        self._canvas.setAccessibleDescription("")

    def zoom_zuruecksetzen(self) -> None:
        """Zurücksetzen (Knopf, Pos1): „Auto für die Ansicht“ und neu zeichnen (F3).

        In Ansicht 4 (keine Achsenwahl) geht die Werkzeugleiste auf den Anfang ihres Verlaufs.
        """
        aufruf = self._letzter_aufruf
        if aufruf is None or aufruf[0].value not in ACHSEN_JE_ANSICHT:
            self._toolbar.stapel_home()
            return
        ansicht, daten, optionen, beschreibung = aufruf
        self._achsen.auf_auto(ansicht.value)
        self._bekannt = None  # nicht mehr in den Zustand zurückschreiben, was gerade verworfen wird
        self.zeichne(ansicht, daten, optionen, beschreibung)
        self.achsen_geaendert.emit()

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
        dieselben Achsenoptionen wie die Bildschirmdarstellung (feste Bereiche des
        :class:`AchsenZustand`; in Ansicht 3 kommt der Beschriftungsstreifen oberhalb der
        gewählten oberen Grenze dazu).

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
        self._synchronisiere()
        optionen_bild = bild_optionen(ansicht, self._mit_achsen(ansicht, optionen))
        zeichner = ZEICHNER[ansicht]
        return speichere_arbeitsbild(
            lambda fig: zeichner(fig, daten, optionen_bild, self._stil),
            pfad,
            stempel,
            self._stil,
        )

    # --- Größenänderung ----------------------------------------------------------------------

    def _neuzeichnen(self) -> None:
        """Zeichnet die aktuelle Ansicht mit denselben Daten und Optionen neu.

        Die Achsengrenzen kommen aus dem Achsenzustand (Zoom und Verschieben sind dort fest
        übernommen); der Verlauf der Werkzeugleiste („Zurück“) beginnt danach neu.
        """
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
