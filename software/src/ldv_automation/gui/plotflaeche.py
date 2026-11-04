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
from typing import Any

import matplotlib
import numpy as np
from matplotlib.backend_bases import FigureCanvasBase
from matplotlib.backends.backend_qt import NavigationToolbar2QT
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from matplotlib.figure import Figure
from PySide6.QtCore import QEvent, QObject, QSize, Qt, QTimer, Signal
from PySide6.QtWidgets import QFrame, QToolButton, QVBoxLayout, QWidget

from ldv_automation.darstellung import Ansicht, Plotstil, Zeichnung
from ldv_automation.darstellung.frf import zeichne_frf
from ldv_automation.darstellung.schwingform import zeichne_schwingform
from ldv_automation.darstellung.spektrum import zeichne_spektrum
from ldv_automation.darstellung.spitzen import zeichne_spitzen
from ldv_automation.gui.anzeige_auswerten import ANSICHT_NAMEN
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
        self._letzter_aufruf: tuple[Ansicht, object, object, str] | None = None
        self._gezeichnet_groesse = QSize()
        self._neuzeichnen_timer = QTimer(self)
        self._neuzeichnen_timer.setObjectName("neuzeichnen")
        self._neuzeichnen_timer.setSingleShot(True)
        self._neuzeichnen_timer.setInterval(NEUZEICHNEN_MS)
        self._neuzeichnen_timer.timeout.connect(self._neuzeichnen)

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
            ``True``: Der Frequenzausschnitt (x) bleibt erhalten, wenn dieselbe Ansicht mit
            derselben Frequenzachse neu gezeichnet wird (Wechsel von Punkt, Komponente, Größe
            oder Skala); die y-Achse skaliert neu, weil sich die Werte ändern. „Zurücksetzen“
            führt weiter auf den Ausgangsbereich. Ein neuer Dateiaufruf übergibt ``False``.

        Returns
        -------
        Zeichnung
            Hilfsobjekte der Zeichenfunktion.
        """
        alt_x = self._zeichnung.achsen[0].get_xlim() if self._zeichnung is not None else None
        alt_ansicht = self._ansicht
        zeichnung = ZEICHNER[ansicht](self._figure, daten, optionen, self._stil)
        # Erst zeichnen, dann Standardansicht merken: constrained-Layout kennt die Positionen
        # erst nach dem Zeichnen.
        self._canvas.draw()  # type: ignore[no-untyped-call]
        self._toolbar.update()
        self._toolbar.push_current()
        standard_x = zeichnung.achsen[0].get_xlim()
        if (
            zoom_behalten
            and alt_x is not None
            and alt_ansicht is ansicht
            and self._standard_x is not None
            and np.allclose(self._standard_x, standard_x, rtol=1e-12, atol=0.0)
            and not np.allclose(alt_x, standard_x, rtol=1e-12, atol=0.0)
        ):
            # Achsen teilen die Frequenzachse (Ansicht 2: sharex); der Ausschnitt gilt für alle.
            zeichnung.achsen[0].set_xlim(alt_x)
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

    def leere(self) -> None:
        """Löscht die Darstellung (Figure leer, Verlauf der Werkzeugleiste leer)."""
        self._figure.clear()
        self._canvas.draw_idle()  # type: ignore[no-untyped-call]
        self._toolbar.update()
        self._zeichnung = None
        self._standard_x = None
        self._ansicht = None
        self._letzter_aufruf = None
        self._neuzeichnen_timer.stop()
        self._canvas.setAccessibleDescription("")

    def zoom_zuruecksetzen(self) -> None:
        """Stellt den Ausgangsbereich wieder her (Knopf „Zurücksetzen“, Pos1)."""
        self._toolbar.home()

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
            elif event.type() == QEvent.Type.FocusIn:
                setze_eigenschaft(self._rahmen, "fokus", "true")
            elif event.type() == QEvent.Type.FocusOut:
                setze_eigenschaft(self._rahmen, "fokus", "false")
        return super().eventFilter(watched, event)
