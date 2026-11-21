r"""Darstellungsfläche der 3D-Animation (R-071, Plan P-AUSW3 AN6, ADR-021, ADR-029).

:class:`AnimationsFlaeche` hält eine eigene ``matplotlib.figure.Figure`` mit
``FigureCanvasQTAgg`` (nie ``pyplot``) und zeigt die Schwingform mit
:func:`~ldv_automation.darstellung.animation3d.zeichne_animation`. Die Fläche steuert Drehen
und Zoom selbst (``Axes3D.disable_mouse_rotation`` ist gesetzt, damit nicht zwei Steuerungen
konkurrieren): linke Maustaste ziehen dreht, das Rad zoomt, ein Doppelklick und Pos1 setzen den
Blick zurück, die Tasten folgen :data:`~ldv_automation.gui.animation_steuerung.ANIMATIONS_TASTEN`
(←/→ Phase, Umschalt+←/→ und ↑/↓ drehen, Leertaste Abspielen/Pause).

Ein Qt-Timer (``PreciseTimer``, je Bild einzeln neu gestartet, damit sich keine Zeitereignisse
anstauen) taktet die Wiedergabe. Der Winkel ergibt sich aus der **Uhr** der
:class:`~ldv_automation.gui.animation_steuerung.Phasenuhr`, nicht aus der Zahl der Takte: Eine
langsame Zeichnung lässt Bilder aus, die Bewegung bleibt zeitrichtig (E-A4). Die Fläche misst die
Zeit je Bild (gleitender Median der letzten 30). Der Timer wird nach jedem Bild mit dem
**Restintervall** (Bildintervall minus im Bild verbrauchte Zeit, mindestens 0) neu gestartet, damit
die Bildperiode das Intervall 1000/Bildrate bleibt und nicht Zeichenzeit plus Intervall wird.
:attr:`AnimationsFlaeche.langsam` meldet, wenn die Zeichenzeit dem Intervall nahe kommt
(:data:`LANGSAM_ZEICHENANTEIL`) oder die gemessene Bildperiode das Intervall merklich überschreitet
(:data:`LANGSAM_PERIODENFAKTOR`); die Bildrate wird nie still herabgesetzt (Brief 4).

Rückfallstufen (ADR-029, Plan 4.3) sind eine Einstellung (:class:`Stufe`), nicht über den Code
verteilt: L0 vereinfachte Achsen nur in Wiedergabe und beim Drehen, L1 zusätzlich beim Ziehen des
Phasenreglers, L2 zeichnet beim Loslassen neu und kennt keine Wiedergabe (Einzelschritt); beim
Drehen zeigt L2 ein Achsen-Skelett (Box und Achsenkreuz, keine Punkte).

Die Wiedergabe pausiert beim Ziehen, beim Ziehen des Phasenreglers, bei Größenänderung, beim
Ausblenden (Verlassen des Reiters) und beim Schließen; **Fortsetzen nur durch Nutzeraktion**.

Dieses Modul ist ein dünnes Widget (Abdeckung nur mit ``pytest -m gui``, siehe
``pyproject.toml``); die Logik (Uhr, Blick, Tasten, Stufen, Texte) liegt Qt-frei in
:mod:`.animation_steuerung`.
"""

from __future__ import annotations

import statistics
import time
from collections import deque
from collections.abc import Callable
from dataclasses import replace
from pathlib import Path
from typing import Any

from matplotlib import rc_context
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from matplotlib.figure import Figure
from PySide6.QtCore import QEvent, QObject, QPointF, Qt, QTimer, Signal
from PySide6.QtGui import (
    QAction,
    QCloseEvent,
    QHideEvent,
    QKeyEvent,
    QKeySequence,
    QMouseEvent,
    QShowEvent,
    QWheelEvent,
)
from PySide6.QtWidgets import QFrame, QVBoxLayout, QWidget

from ldv_automation.darstellung.animation3d import (
    AnimationsOptionen,
    Blick,
    aktualisiere_animation,
    zeichne_animation,
)
from ldv_automation.darstellung.animation_daten import AnimationsDaten
from ldv_automation.darstellung.bild import Stempel, speichere_arbeitsbild
from ldv_automation.darstellung.stil import Plotstil
from ldv_automation.darstellung.zeichnung import Zeichnung
from ldv_automation.gui import tokens
from ldv_automation.gui.animation_steuerung import (
    ANIMATIONS_TASTEN,
    BILDRATE_VORGABE,
    SCHRITT_VORGABE_GRAD,
    STUFE_VORGABE,
    TEMPO_VORGABE,
    Aktion,
    Blickzustand,
    Ereignis,
    Phasenuhr,
    Stufe,
    frequenzwechsel,
    optionen_stufe,
    verhalten,
    wende_an,
)
from ldv_automation.gui.animation_tasten import aktion_aus_tastenereignis
from ldv_automation.gui.plotflaeche import FIGURE_DPI, NEUZEICHNEN_MS
from ldv_automation.gui.stil import setze_eigenschaft

__all__ = [
    "BILDZEIT_FENSTER",
    "BILDZEIT_MINDEST",
    "LANGSAM_PERIODENFAKTOR",
    "LANGSAM_ZEICHENANTEIL",
    "RASTE_WINKEL_EINHEIT",
    "AnimationsFlaeche",
]

BILDZEIT_FENSTER = 30
"""Zahl der Bilder im gleitenden Median der Bildzeit (Plan 4.2)."""
BILDZEIT_MINDEST = 3
"""Mindestzahl gemessener Bilder, bevor „langsam“ gemeldet wird (ein einzelnes, langsames
erstes Bild, etwa nach dem Aufbau der Schriften, löst den Hinweis nicht aus)."""
LANGSAM_ZEICHENANTEIL = 0.9
"""Liegt die mediane Zeichenzeit über diesem Anteil des Bildintervalls, bleibt kein Restintervall
für den Takt: „langsam“ (vorläufiger Wert, bis zur Messung M2 am Messrechner)."""
LANGSAM_PERIODENFAKTOR = 1.25
"""Liegt die mediane Bildperiode über diesem Vielfachen des Intervalls, wird die Soll-Bildrate nicht
erreicht: „langsam“ (vorläufiger Wert, bis zur Messung M2 am Messrechner)."""
RASTE_WINKEL_EINHEIT = 120.0
"""``angleDelta`` einer Raste des Mausrads (Qt: 1/8 Grad, 15° je Raste = 120)."""


class _StilCanvas(FigureCanvasQTAgg):
    """Canvas, der jedes Zeichnen (auch ``draw_idle``) in der Schriftfamilie des Stils ausführt.

    Die Texte tragen die generische Familie ``sans-serif``; welche Datei dahinter steht, entscheidet
    ``findfont`` erst beim Zeichnen aus der globalen rc. Ohne diesen Kontext liefe die Darstellung
    mit der Rechnerschrift, die Messung der Labels (``LabelMasse``) mit der Stilschrift.
    """

    def __init__(self, figure: Figure, stil: Plotstil) -> None:
        super().__init__(figure)  # type: ignore[no-untyped-call]
        self._stil_rc = stil.text_rc()

    def draw(self) -> None:
        """Zeichnet mit Schriftfamilie und Textfarben des Stils."""
        with rc_context(self._stil_rc):
            super().draw()  # type: ignore[no-untyped-call]


class AnimationsFlaeche(QFrame):
    r"""Darstellungsfläche der Animation: Canvas, Maus, Rad, Tasten, Timer, Fokusrahmen.

    Die Fläche **besitzt** Winkel (:class:`Phasenuhr`) und Blick (:class:`Blickzustand`). Beim
    Zeichnen und Aktualisieren ersetzt sie ``theta_rad``, ``blick`` und ``vereinfacht`` der
    übergebenen :class:`AnimationsOptionen` durch ihren Zustand; ein Wechsel von Komponente,
    Bezug, Größe oder Farbe (neue Daten und Optionen über :meth:`zeichne`) behält Blick und
    Winkel.

    Parameters
    ----------
    stil : Plotstil
        Stil der Oberfläche (:func:`ldv_automation.gui.plotstil.baue_plotstil`).
    parent : QWidget, optional
        Elternwidget.
    zeit : callable, optional
        Zeitquelle der :class:`Phasenuhr` in s (injizierbar, damit Tests nichts von der echten
        Zeit abhängig machen); Voreinstellung :func:`time.monotonic`.
    messzeit : callable, optional
        Zeitquelle der Bildzeitmessung in s; Voreinstellung :func:`time.perf_counter`.
    bildrate : float
        Soll-Bilder je Sekunde (vorläufig, bis zur Messung M2 am Messrechner).
    tempo_hz : float
        Perioden je Sekunde Echtzeit (vorläufig).
    schritt_grad : float
        Schrittweite der Einzelschritte in Grad.
    stufe : Stufe
        Rückfallstufe (:data:`~ldv_automation.gui.animation_steuerung.STUFE_VORGABE`).
    blick_vorgabe : str
        Name der Blickvorgabe, zu der das Zurücksetzen zurückkehrt (``"xy"`` Aufsicht).
    """

    phase_geaendert = Signal(float)
    """Der Winkel hat sich geändert (Wiedergabe, Einzelschritt, Taste, Regler): θ in rad."""
    wiedergabe_geaendert = Signal(bool)
    """Die Wiedergabe wurde gestartet (``True``) bzw. angehalten (``False``)."""
    blick_geaendert = Signal()
    """Blickrichtung oder Zoom haben sich geändert (Maus, Rad, Tasten, Vorgaben, Zurücksetzen)."""
    langsam_geaendert = Signal(bool)
    """Die Wiedergabe ist langsamer als eingestellt (``True``) bzw. wieder rechtzeitig."""
    fehler = Signal(str)
    """Beim Zeichnen ist ein Fehler aufgetreten (Text der Ausnahme); die Wiedergabe ist dann aus."""

    def __init__(
        self,
        stil: Plotstil,
        parent: QWidget | None = None,
        *,
        zeit: Callable[[], float] = time.monotonic,
        messzeit: Callable[[], float] = time.perf_counter,
        bildrate: float = BILDRATE_VORGABE,
        tempo_hz: float = TEMPO_VORGABE,
        schritt_grad: float = SCHRITT_VORGABE_GRAD,
        stufe: Stufe = STUFE_VORGABE,
        blick_vorgabe: str = "xy",
    ) -> None:
        super().__init__(parent)
        if not bildrate > 0.0:
            raise ValueError(f"bildrate > 0 erwartet: {bildrate}")
        self.setObjectName("animationsflaeche")
        self._stil = stil
        self._uhr = Phasenuhr(zeit, tempo_hz=tempo_hz, schritt_grad=schritt_grad)
        self._blick = Blickzustand(blick_vorgabe)
        self._stufe = stufe
        self._bildrate = float(bildrate)
        self._messzeit = messzeit
        self._bildzeiten: deque[float] = deque(maxlen=BILDZEIT_FENSTER)
        self._perioden: deque[float] = deque(maxlen=BILDZEIT_FENSTER)
        self._letzter_takt: float | None = None
        self._langsam = False
        self._daten: AnimationsDaten | None = None
        self._basis = AnimationsOptionen()
        self._beschreibung = ""
        self._zeichnung: Zeichnung | None = None
        self._zieht = False
        self._letzte_pos: QPointF | None = None
        self._gezeichnet_groesse = (0, 0)
        self._skelett: list[Any] = []  # Linien des Achsen-Skeletts (L2, nur beim Drehen)
        self._marker_sichtbar: dict[str, bool] = {}  # Sichtbarkeit der Marker vor dem Skelett

        self._figure = Figure(dpi=FIGURE_DPI)
        self._canvas = _StilCanvas(self._figure, stil)
        self._canvas.setObjectName("animation_canvas")
        self._canvas.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self._canvas.setMinimumSize(0, 0)
        self._canvas.installEventFilter(self)
        self._rahmen = QFrame(self)
        self._rahmen.setObjectName("animation_rahmen")
        # Fokusrahmen (UI-34): 2 px C_AKZENT bei Fokus, sonst durchsichtig (kein Layoutsprung).
        # Die Regel steht hier und nicht in ``gui/stil.py``; AN7 darf sie dorthin verlegen.
        self._rahmen.setStyleSheet(
            f"QFrame#animation_rahmen {{ border: 2px solid transparent;"
            f" background: {tokens.C_PLOT_FLAECHE}; }}"
            f'QFrame#animation_rahmen[fokus="true"] {{ border: 2px solid {tokens.C_AKZENT}; }}'
        )
        rahmen_layout = QVBoxLayout(self._rahmen)
        rahmen_layout.setContentsMargins(0, 0, 0, 0)
        rahmen_layout.addWidget(self._canvas)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self._rahmen, 1)

        self._timer = QTimer(self)
        self._timer.setObjectName("animation_takt")
        self._timer.setTimerType(Qt.TimerType.PreciseTimer)
        self._timer.setSingleShot(True)  # je Bild neu gestartet: nichts staut sich an
        self._timer.setInterval(self._intervall_ms())
        self._timer.timeout.connect(self.takt)
        self._neuzeichnen_timer = QTimer(self)
        self._neuzeichnen_timer.setObjectName("animation_neuzeichnen")
        self._neuzeichnen_timer.setSingleShot(True)
        self._neuzeichnen_timer.setInterval(NEUZEICHNEN_MS)
        self._neuzeichnen_timer.timeout.connect(self._neuzeichnen)

        # Pos1 im Teilbaum der Fläche (kollidiert nicht mit „Zoom zurücksetzen“ der PlotFlaeche)
        self.act_ansicht_zurueck = QAction("Ansicht zurücksetzen", self)
        self.act_ansicht_zurueck.setObjectName("act_animation_ansicht_zurueck")
        self.act_ansicht_zurueck.setShortcut(
            QKeySequence(ANIMATIONS_TASTEN[Aktion.ANSICHT_ZURUECK][0])
        )
        # Pos1 ist doppelt gebunden: als Shortcut der Aktion (verbraucht das Tastenereignis im
        # Normalfall, bevor es den Canvas erreicht) und im KeyPress-Pfad (``_taste``) als Rückfall,
        # wenn der Shortcut nicht greift (z. B. Fokus im Canvas ohne Shortcut-Zustellung).
        self.act_ansicht_zurueck.setShortcutContext(Qt.ShortcutContext.WidgetWithChildrenShortcut)
        self.act_ansicht_zurueck.triggered.connect(self.ansicht_zuruecksetzen)
        self.addAction(self.act_ansicht_zurueck)

    # --- Zugriff ---------------------------------------------------------------------------

    @property
    def figure(self) -> Figure:
        """Die Figure der Fläche."""
        return self._figure

    @property
    def canvas(self) -> FigureCanvasQTAgg:
        """Der fokussierbare Canvas."""
        return self._canvas

    @property
    def uhr(self) -> Phasenuhr:
        """Winkel, Tempo, Schrittweite und Wiedergabezustand."""
        return self._uhr

    @property
    def zeichnung(self) -> Zeichnung | None:
        """Rückgabe von ``zeichne_animation`` (``None`` = leer)."""
        return self._zeichnung

    @property
    def blick(self) -> Blick:
        """Aktuelle Blickrichtung und Zoom."""
        return self._blick.blick

    @property
    def blickzustand(self) -> Blickzustand:
        """Zustand des Blicks (Vorgaben, Zurücksetzen)."""
        return self._blick

    @property
    def laeuft(self) -> bool:
        """Die Wiedergabe ist aktiv."""
        return self._uhr.laeuft

    @property
    def stufe(self) -> Stufe:
        """Rückfallstufe."""
        return self._stufe

    @property
    def bildrate(self) -> float:
        """Soll-Bildrate in Bildern je Sekunde."""
        return self._bildrate

    @property
    def langsam(self) -> bool:
        """Die Soll-Bildrate wird nicht (sicher) erreicht (Hinweis in AF, Brief 4)."""
        return self._langsam

    @property
    def bildzeit_median_s(self) -> float | None:
        """Gleitender Median der Bildzeit in s (letzte 30 Bilder); ``None`` ohne Messung."""
        return statistics.median(self._bildzeiten) if self._bildzeiten else None

    @property
    def bildperiode_median_s(self) -> float | None:
        """Gleitender Median der Bildperiode (Abstand zweier Bilder) in s; ``None`` ohne Messung."""
        return statistics.median(self._perioden) if self._perioden else None

    @property
    def beschreibung(self) -> str:
        """Textalternative des Canvas (``accessibleDescription``)."""
        return self._beschreibung

    @property
    def standbild_optionen(self) -> AnimationsOptionen | None:
        """Optionen des Standbilds bei Winkel und Blick der Fläche; ohne Bild ``None``.

        Dieselben Optionen, mit denen :meth:`speichere` zeichnet; der Reiter leitet daraus die
        Stempelzeilen (Winkel, Frequenz, Überhöhung, Blick) und die offenen Annahmen ab.
        """
        if self._daten is None:
            return None
        return self._optionen(self._basis, Ereignis.STAND)

    def tab_kette(self) -> list[QWidget]:
        """Fokussierbare Teile der Fläche in Tab-Reihenfolge (nur der Canvas)."""
        return [self._canvas]

    def _intervall_ms(self) -> int:
        return max(1, round(1000.0 / self._bildrate))

    # --- Zeichnen --------------------------------------------------------------------------

    def zeichne(
        self, daten: AnimationsDaten, optionen: AnimationsOptionen, beschreibung: str = ""
    ) -> Zeichnung:
        """Zeichnet die Animation vollständig neu (Daten, Komponente, Bezug, Größe, Farbe, Größe).

        Winkel und Blick behält die Fläche (Plan 4.1), ``optionen.theta_rad``, ``.blick`` und
        ``.vereinfacht`` werden ersetzt. Die Wiedergabe läuft weiter, wenn sie lief.

        Parameters
        ----------
        daten : AnimationsDaten
            Aus :func:`~ldv_automation.darstellung.animation_daten.animation_daten`.
        optionen : AnimationsOptionen
            Überhöhung, Farbe, Farbbereich, Ruhelage, Punktlabels, Kennzeichen.
        beschreibung : str, optional
            Textalternative des Canvas (``accessibleDescription``).

        Raises
        ------
        ValueError
            Ungültige Optionen (z. B. Farbbereich mit ``von >= bis``); die Fläche bleibt dann
            unverändert.
        """
        opt = self._optionen(optionen, Ereignis.STAND)
        self._skelett = []  # die Figure wird neu aufgebaut: alte Linien sind weg
        zeichnung = zeichne_animation(self._figure, daten, opt, self._stil)
        self._daten = daten
        self._basis = optionen
        self._zeichnung = zeichnung
        self._beschreibung = beschreibung
        self._canvas.setAccessibleName("Animation der Betriebsschwingform")
        self._canvas.setAccessibleDescription(beschreibung)
        self._gezeichnet_groesse = (self._canvas.width(), self._canvas.height())
        self._canvas.draw()
        return zeichnung

    def aktualisiere(
        self, optionen: AnimationsOptionen | None = None, *, zoom_fest: bool = False
    ) -> None:
        """Setzt Winkel, Blick und die übergebenen dynamischen Optionen (Teilaktualisierung).

        Ändert sich ein Teil, der den Aufbau betrifft (Farbe, Ruhelage, Kennzeichen), zeichnet
        die Fläche vollständig neu. Mit ``zoom_fest=True`` (Überhöhungsregler wird gezogen) bleibt
        der Zoom der Box stehen, die Messung holt das nächste Aktualisieren nach.

        Raises
        ------
        RuntimeError
            Es wurde noch nichts gezeichnet.
        ValueError
            Ungültige Optionen; das Bild bleibt unverändert.
        """
        if self._daten is None or self._zeichnung is None:
            raise RuntimeError("Es ist keine Animation gezeichnet.")
        basis = self._basis if optionen is None else optionen
        try:
            aktualisiere_animation(
                self._zeichnung,
                self._daten,
                self._optionen(basis, Ereignis.STAND),
                self._stil,
                zoom_fest=zoom_fest,
            )
        except ValueError:
            # Aufbau geändert (Farbe, Kennzeichen …) oder Option ungültig: ein frisches Zeichnen
            # führt beides richtig aus; bei ungültiger Option wirft es denselben Fehler.
            self.zeichne(self._daten, basis, self._beschreibung)
            return
        self._basis = basis
        self._canvas.draw()

    def setze_beschreibung(self, beschreibung: str) -> None:
        """Setzt die Textalternative (z. B. nach neuem Winkel oder Blick), ohne neu zu zeichnen."""
        self._beschreibung = beschreibung
        self._canvas.setAccessibleDescription(beschreibung)

    def leere(self) -> None:
        """Hält die Wiedergabe an und löscht die Darstellung (Figure leer)."""
        self.pausiere(neu_zeichnen=False)
        self._skelett = []
        self._figure.clear()
        self._canvas.draw_idle()  # type: ignore[no-untyped-call]
        self._daten = None
        self._zeichnung = None
        self._beschreibung = ""
        self._canvas.setAccessibleDescription("")

    def _optionen(self, basis: AnimationsOptionen, ereignis: Ereignis) -> AnimationsOptionen:
        """Optionen mit dem Winkel und Blick der Fläche; ``vereinfacht`` je Stufe und Anlass."""
        return replace(
            basis,
            theta_rad=self._uhr.theta_rad,
            blick=self._blick.blick,
            vereinfacht=optionen_stufe(self._stufe, ereignis),
        )

    def _zeige(self, ereignis: Ereignis, *, sofort: bool) -> bool:
        """Teilaktualisierung für ``ereignis``; ``sofort`` zeichnet synchron, sonst ``draw_idle``.

        Fehler beim Zeichnen halten die Wiedergabe an und werden als :attr:`fehler` gemeldet.

        Returns
        -------
        bool
            ``True``, wenn gezeichnet wurde.
        """
        if self._daten is None or self._zeichnung is None:
            return False
        self._entferne_skelett()  # ein Bild mit Daten nie unter einem stehengebliebenen Skelett
        try:
            aktualisiere_animation(
                self._zeichnung, self._daten, self._optionen(self._basis, ereignis), self._stil
            )
            if sofort:
                self._canvas.draw()
            else:
                self._canvas.draw_idle()  # type: ignore[no-untyped-call]
        except Exception as fehler:  # Zeichenfunktion scheitert: melden statt verschlucken
            lief = self._uhr.laeuft
            self._stoppe_timer()
            self._uhr.pause()
            self.fehler.emit(str(fehler))
            if lief:  # Signal nur bei echter Zustandsänderung
                self.wiedergabe_geaendert.emit(False)
            return False
        return True

    # --- Wiedergabe ------------------------------------------------------------------------

    def abspielen(self) -> bool:
        """Startet die Wiedergabe aus dem aktuellen Winkel.

        Returns
        -------
        bool
            ``True``, wenn die Wiedergabe läuft. ``False`` ohne Darstellung, bei ausgeblendeter
            Fläche und in Stufe L2 (Einzelschritt statt Wiedergabe, OE-A2).
        """
        if self._daten is None or not self.isVisible() or not verhalten(self._stufe).wiedergabe:
            return False
        if self._uhr.laeuft:
            return True
        self._bildzeiten.clear()
        self._perioden.clear()
        self._letzter_takt = None
        self._setze_langsam(False)
        self._uhr.start()
        self._timer.start(self._intervall_ms())
        self.wiedergabe_geaendert.emit(True)
        return True

    def pausiere(self, *, neu_zeichnen: bool = True) -> None:
        """Hält die Wiedergabe an; das Bild steht danach voll (Achsen, Panes, Ticks) im Stand.

        Fortsetzen nur durch Nutzeraktion (:meth:`abspielen`, Leertaste).
        """
        lief = self._uhr.laeuft
        self._stoppe_timer()
        if lief:
            self._uhr.pause()
            if neu_zeichnen:
                self._zeige(Ereignis.STAND, sofort=True)
            self._setze_langsam(False)  # Hinweis „langsam“ gilt nur für die laufende Wiedergabe
            self.phase_geaendert.emit(self._uhr.theta_rad)
            self.wiedergabe_geaendert.emit(False)

    def umschalten(self) -> bool:
        """Abspielen/Pause (Leertaste); gibt ``True`` zurück, wenn danach abgespielt wird."""
        if self._uhr.laeuft:
            self.pausiere()
            return False
        return self.abspielen()

    def _stoppe_timer(self) -> None:
        self._timer.stop()

    def takt(self) -> None:
        """Ein Bild der Wiedergabe: Winkel aus der Uhr, Teilaktualisierung, Bildzeit messen.

        Der Timer ruft diese Methode je Intervall; Tests rufen sie von Hand (Uhr injiziert).
        Danach wird der Timer für das nächste Bild mit dem Restintervall neu gestartet (Intervall
        minus im Bild verbrauchte Zeit, mindestens 0), solange die Wiedergabe läuft.
        """
        if not self._uhr.laeuft:
            return
        start = self._messzeit()
        if self._letzter_takt is not None:
            self._perioden.append(start - self._letzter_takt)
        self._letzter_takt = start
        self._uhr.tick()
        gezeichnet = self._zeige(Ereignis.WIEDERGABE, sofort=True)
        if not gezeichnet:
            return
        self._bildzeiten.append(self._messzeit() - start)
        self._pruefe_langsam()
        self.phase_geaendert.emit(self._uhr.theta_rad)
        if self._uhr.laeuft:
            # Verbrauchte Zeit einschließlich der Slots von ``phase_geaendert``
            rest_s = max(0.0, 1.0 / self._bildrate - (self._messzeit() - start))
            self._timer.start(round(rest_s * 1000.0))

    def _pruefe_langsam(self) -> None:
        """„Langsam“: Zeichenzeit nahe am Intervall oder Bildperiode merklich darüber."""
        if len(self._bildzeiten) < BILDZEIT_MINDEST:
            return
        intervall_s = 1.0 / self._bildrate
        zu_lang = statistics.median(self._bildzeiten) > LANGSAM_ZEICHENANTEIL * intervall_s
        if len(self._perioden) >= BILDZEIT_MINDEST:
            zu_lang = zu_lang or (
                statistics.median(self._perioden) > LANGSAM_PERIODENFAKTOR * intervall_s
            )
        self._setze_langsam(zu_lang)

    def _setze_langsam(self, wert: bool) -> None:
        if wert != self._langsam:
            self._langsam = wert
            self.langsam_geaendert.emit(wert)

    # --- Phase -----------------------------------------------------------------------------

    def schritt(self, vorzeichen: int, grad: float | None = None) -> None:
        """Einzelschritt um die Schrittweite; hält die Wiedergabe an (UI-24, UI-32)."""
        lief = self._uhr.laeuft
        phase_vorher = self._uhr.theta_rad
        self._uhr.schritt(vorzeichen, grad)
        self._nach_aenderung(lief, phase_vorher, self._blick.blick)

    def setze_theta_grad(self, grad: float, *, ziehend: bool = False) -> None:
        """Setzt den Winkel (Phasenregler, Feld).

        Mit ``ziehend=True`` (Regler wird gezogen) pausiert die Wiedergabe und die Achsen sind
        je Stufe vereinfacht (L1, L2); ``ziehend=False`` zeichnet voll.
        """
        if ziehend:
            lief = self._uhr.laeuft
            self._stoppe_timer()
            self._uhr.pause()
            self._uhr.setze_theta_grad(grad)
            ereignis = Ereignis.REGLER
            if lief:
                self.wiedergabe_geaendert.emit(False)
            if verhalten(self._stufe).neuzeichnen_beim_loslassen:
                self.phase_geaendert.emit(self._uhr.theta_rad)  # L2: Zeichnen beim Loslassen
                return
        else:
            self._uhr.setze_theta_grad(grad)
            ereignis = Ereignis.STAND
        self._zeige(ereignis, sofort=not ziehend)
        self.phase_geaendert.emit(self._uhr.theta_rad)

    def phase_losgelassen(self) -> None:
        """Der Phasenregler wurde losgelassen: Voll-Neuzeichnen (Achsen, Panes, Ticks)."""
        self._zeige(Ereignis.STAND, sofort=True)

    def setze_tempo_hz(self, tempo_hz: float) -> None:
        """Ändert das Tempo (Perioden je Sekunde Echtzeit); die Phase bleibt erhalten."""
        self._uhr.setze_tempo(tempo_hz)

    def setze_schritt_grad(self, grad: float) -> None:
        """Ändert die Schrittweite der Einzelschritte."""
        self._uhr.setze_schritt_grad(grad)

    def setze_bildrate(self, bildrate: float) -> None:
        """Ändert die Soll-Bildrate (Bilder je Sekunde); der Hinweis „langsam“ wird neu bewertet."""
        if not bildrate > 0.0:
            raise ValueError(f"bildrate > 0 erwartet: {bildrate}")
        self._bildrate = float(bildrate)
        self._timer.setInterval(self._intervall_ms())
        self._bildzeiten.clear()
        self._perioden.clear()
        self._setze_langsam(False)

    def frequenz_gewechselt(self) -> str:
        """Schnittstelle für Frequenzwechsel (F-A4): zurück ins Standbild.

        Hält die Wiedergabe an, setzt den Winkel auf 0 und gibt den Modus zurück, den die
        Oberfläche (AN7) einstellen muss (immer ``"standbild"``). Die Animation startet nie ohne
        Nutzeraktion (UI-22). Gezeichnet wird nicht: die Oberfläche wechselt die Seite.
        """
        lief = self._uhr.laeuft
        self._stoppe_timer()
        modus = frequenzwechsel(self._uhr)
        if lief:
            self.wiedergabe_geaendert.emit(False)
        self.phase_geaendert.emit(self._uhr.theta_rad)
        return modus

    # --- Blick -----------------------------------------------------------------------------

    def setze_blick_vorgabe(self, name: str) -> Blick:
        """Setzt Blick und Zoom auf die Vorgabe ``name`` (Knöpfe xy, xz, yz, iso; UI-23)."""
        blick = self._blick.waehle_vorgabe(name)
        self._nach_blickaenderung(Ereignis.STAND)
        return blick

    def ansicht_zuruecksetzen(self) -> Blick:
        """Blick und Zoom zurück zur gewählten Vorgabe (Pos1, Doppelklick); nicht Winkel und s."""
        blick = self._blick.zuruecksetzen()
        self._nach_blickaenderung(Ereignis.STAND)
        return blick

    def _nach_blickaenderung(self, ereignis: Ereignis, *, sofort: bool = True) -> None:
        self._zeige(ereignis, sofort=sofort)
        self.blick_geaendert.emit()

    # --- Speichern -------------------------------------------------------------------------

    def speichere(self, pfad: Path, stempel: Stempel) -> Zeichnung:
        """Schreibt das Standbild bei Winkel und Blick der Fläche als PNG oder PDF mit Stempel.

        Das Bild entsteht mit derselben Zeichenfunktion und denselben Daten auf einer **neuen**
        Figure (volle Achsen, nicht vereinfacht); die Bildschirmfigur bleibt unverändert.

        Raises
        ------
        RuntimeError
            Es ist nichts gezeichnet.
        ValueError
            Endung weder ``.png`` noch ``.pdf``.
        """
        if self._daten is None:
            raise RuntimeError("Es ist keine Animation zum Speichern vorhanden.")
        daten = self._daten
        opt = self._optionen(self._basis, Ereignis.STAND)  # = standbild_optionen
        return speichere_arbeitsbild(
            lambda fig: zeichne_animation(fig, daten, opt, self._stil), pfad, stempel, self._stil
        )

    # --- Ereignisse ------------------------------------------------------------------------

    def eventFilter(self, watched: QObject, event: QEvent) -> bool:  # noqa: N802  # Qt-Name
        """Maus, Rad, Tasten, Größe und Fokusrahmen des Canvas."""
        if watched is self._canvas:
            art = event.type()
            if art == QEvent.Type.MouseButtonPress and isinstance(event, QMouseEvent):
                return self._maus_gedrueckt(event)
            if art == QEvent.Type.MouseMove and isinstance(event, QMouseEvent):
                return self._maus_bewegt(event)
            if art == QEvent.Type.MouseButtonRelease and isinstance(event, QMouseEvent):
                return self._maus_losgelassen(event)
            if art == QEvent.Type.MouseButtonDblClick and isinstance(event, QMouseEvent):
                return self._maus_doppelklick(event)
            if art == QEvent.Type.Wheel and isinstance(event, QWheelEvent):
                return self._rad(event)
            if art == QEvent.Type.KeyPress and isinstance(event, QKeyEvent):
                return self._taste(event)
            if art == QEvent.Type.Resize:
                self._groesse_geaendert()
            elif art == QEvent.Type.FocusIn:
                setze_eigenschaft(self._rahmen, "fokus", "true")
            elif art == QEvent.Type.FocusOut:
                setze_eigenschaft(self._rahmen, "fokus", "false")
                self._ziehen_abbrechen(zeichnen=True)
        return super().eventFilter(watched, event)

    def _maus_gedrueckt(self, ereignis: QMouseEvent) -> bool:
        """Linke Taste: Drehen beginnt, die Wiedergabe pausiert (Fortsetzen nur durch Nutzer)."""
        if ereignis.button() != Qt.MouseButton.LeftButton:
            return False  # rechte und mittlere Taste: keine Wirkung (kein Verschieben)
        self.pausiere()
        self._canvas.setFocus(Qt.FocusReason.MouseFocusReason)
        self._zieht = True
        self._letzte_pos = ereignis.position()
        return True

    def _maus_bewegt(self, ereignis: QMouseEvent) -> bool:
        if not self._zieht or self._letzte_pos is None:
            return False
        pos = ereignis.position()
        dx = pos.x() - self._letzte_pos.x()
        dy = pos.y() - self._letzte_pos.y()
        self._letzte_pos = pos
        if dx == 0.0 and dy == 0.0:
            return True
        self._blick.drehen_pixel(dx, dy)
        if verhalten(self._stufe).neuzeichnen_beim_loslassen:
            self._zeige_skelett()  # L2: nur Achsen-Skelett, volles Zeichnen beim Loslassen
            self.blick_geaendert.emit()
        else:
            self._nach_blickaenderung(Ereignis.DREHEN, sofort=False)
        return True

    def _zeige_skelett(self) -> None:
        """L2 beim Drehen: Box und Achsenkreuz in der neuen Blickrichtung, Punkte ausgeblendet.

        Leichtgewichtig (zwölf Kanten, drei Achsenlinien, ``draw_idle``); die Daten werden erst
        beim Loslassen (:meth:`_entferne_skelett`, dann voll zeichnen) wieder gezeigt.
        """
        z = self._zeichnung
        if z is None or not z.achsen:
            return
        ax: Any = z.achsen[0]
        grenzen = z.hilfsobjekte.get("grenzen")
        if grenzen is None:
            return
        if not self._skelett:
            (x0, x1), (y0, y1), (z0, z1) = grenzen
            farbe = self._stil.text_gedaempft
            ecken = [(x, y, zz) for x in (x0, x1) for y in (y0, y1) for zz in (z0, z1)]
            kanten = [
                (a, b)
                for i, a in enumerate(ecken)
                for b in ecken[i + 1 :]
                if sum(p != q for p, q in zip(a, b, strict=True)) == 1
            ]
            achsen = [
                ((x0, y0, z0), (x1, y0, z0)),
                ((x0, y0, z0), (x0, y1, z0)),
                ((x0, y0, z0), (x0, y0, z1)),
            ]
            for (a, b), breite in [(k, 0.8) for k in kanten] + [(k, 1.6) for k in achsen]:
                (linie,) = ax.plot(
                    [a[0], b[0]], [a[1], b[1]], [a[2], b[2]], color=farbe, linewidth=breite
                )
                self._skelett.append(linie)
            self._marker_sichtbar = {}
            for name, marker in z.marker.items():  # alle Punktmarker (keine Punkte im Skelett)
                self._marker_sichtbar[name] = bool(marker.get_visible())
                marker.set_visible(False)
            ax.set_xlim3d(x0, x1)
            ax.set_ylim3d(y0, y1)
            ax.set_zlim3d(z0, z1)
            ax.set_axis_off()
        ax.view_init(elev=self._blick.blick.elev_grad, azim=self._blick.blick.azim_grad)
        self._canvas.draw_idle()  # type: ignore[no-untyped-call]

    def _entferne_skelett(self) -> None:
        """Nimmt das Skelett weg und stellt Punkte und Achsen für das volle Zeichnen wieder her."""
        if not self._skelett:
            return
        for linie in self._skelett:
            linie.remove()
        self._skelett = []
        z = self._zeichnung
        if z is not None and z.achsen:
            for name, sichtbar in self._marker_sichtbar.items():
                if name in z.marker:
                    z.marker[name].set_visible(sichtbar)
            z.achsen[0].set_axis_on()
        self._marker_sichtbar = {}

    def _ziehen_abbrechen(self, *, zeichnen: bool) -> None:
        """Bricht ein laufendes Ziehen ab (Ausblenden, Fokusverlust, Schließen).

        Entfernt das Skelett, stellt Marker und Achsen wieder her, setzt den Ziehzustand zurück und
        zeichnet voll, wenn ``zeichnen`` gesetzt und die Fläche sichtbar ist.
        """
        if not self._zieht and not self._skelett:
            return
        self._zieht = False
        self._letzte_pos = None
        self._entferne_skelett()
        if zeichnen and self.isVisible():
            self._zeige(Ereignis.STAND, sofort=True)

    def _maus_losgelassen(self, ereignis: QMouseEvent) -> bool:
        if ereignis.button() != Qt.MouseButton.LeftButton or not self._zieht:
            return False
        self._zieht = False
        self._letzte_pos = None
        self._entferne_skelett()
        self._zeige(Ereignis.STAND, sofort=True)  # Voll-Neuzeichnen nach Stillstand
        return True

    def _maus_doppelklick(self, ereignis: QMouseEvent) -> bool:
        if ereignis.button() != Qt.MouseButton.LeftButton:
            return False
        self._zieht = False
        self._letzte_pos = None
        self.ansicht_zuruecksetzen()
        return True

    def _rad(self, ereignis: QWheelEvent) -> bool:
        """Zoom um die Rasten des Mausrads (Faktor 1,1 je Raste, Grenzen 0,4 bis 6)."""
        rasten = ereignis.angleDelta().y() / RASTE_WINKEL_EINHEIT
        if rasten == 0.0:
            return False
        self._blick.zoomen(rasten)
        self._nach_blickaenderung(Ereignis.STAND)
        return True

    def _taste(self, ereignis: QKeyEvent) -> bool:
        """Tastenbelegung der Animation (UI-32); ``True`` = verbraucht."""
        aktion = aktion_aus_tastenereignis(ereignis)
        if aktion is None:
            return False
        self.fuehre_aus(aktion)
        return True

    def fuehre_aus(self, aktion: Aktion) -> None:
        """Führt eine Tastenaktion aus (Fokus in der Fläche oder in einem Regler von AH)."""
        if aktion is Aktion.ABSPIELEN:
            self.umschalten()
            return
        lief = self._uhr.laeuft
        phase_vorher = self._uhr.theta_rad
        blick_vorher = self._blick.blick
        wende_an(aktion, self._uhr, self._blick)
        self._nach_aenderung(lief, phase_vorher, blick_vorher)

    def _nach_aenderung(self, lief: bool, phase_vorher: float, blick_vorher: Blick) -> None:
        """Timer anhalten, wenn die Uhr stand, voll zeichnen und Änderungen melden."""
        if lief and not self._uhr.laeuft:
            self._stoppe_timer()
            self._setze_langsam(False)
            self.wiedergabe_geaendert.emit(False)
        self._zeige(Ereignis.STAND, sofort=True)
        if self._uhr.theta_rad != phase_vorher:
            self.phase_geaendert.emit(self._uhr.theta_rad)
        if self._blick.blick != blick_vorher:
            self.blick_geaendert.emit()

    # --- Größe, Ausblenden, Schließen -------------------------------------------------------

    def _groesse_geaendert(self) -> None:
        """Größenänderung pausiert die Wiedergabe; nach Stillstand wird neu gezeichnet."""
        if self._daten is None:
            return
        self.pausiere()
        self._neuzeichnen_timer.start()  # entprellt: jedes Resize startet neu

    def _neuzeichnen(self) -> None:
        """Zeichnet bei geänderter Größe vollständig neu (Texte werden in pt umbrochen)."""
        if self._daten is None or not self.isVisible():
            return
        if (self._canvas.width(), self._canvas.height()) == self._gezeichnet_groesse:
            return
        try:
            self.zeichne(self._daten, self._basis, self._beschreibung)
        except Exception as fehler:  # Zeichenfunktion scheitert: melden statt verschlucken
            self.fehler.emit(str(fehler))

    def beende(self) -> None:
        """Stoppt alle Timer und die Wiedergabe (Schließen; kein hängender Timer beim Beenden)."""
        self._neuzeichnen_timer.stop()
        self._timer.stop()
        self._ziehen_abbrechen(zeichnen=False)
        if self._uhr.laeuft:
            self._uhr.pause()
            self.wiedergabe_geaendert.emit(False)

    def hideEvent(self, event: QHideEvent) -> None:  # noqa: N802  # Qt-Name
        """Ausblenden (Verlassen des Reiters, Wechsel des Modus) pausiert die Wiedergabe."""
        self.pausiere(neu_zeichnen=False)
        self._neuzeichnen_timer.stop()  # ausgeblendet wird nichts gezeichnet
        self._ziehen_abbrechen(zeichnen=False)
        super().hideEvent(event)

    def showEvent(self, event: QShowEvent) -> None:  # noqa: N802  # Qt-Name
        """Einblenden: passt die gezeichnete Größe nicht zum Canvas, entprellt neu zeichnen."""
        super().showEvent(event)
        if self._daten is not None and (
            (self._canvas.width(), self._canvas.height()) != self._gezeichnet_groesse
        ):
            self._neuzeichnen_timer.start()

    def closeEvent(self, event: QCloseEvent) -> None:  # noqa: N802  # Qt-Name
        """Schließen stoppt Timer und Wiedergabe."""
        self.beende()
        super().closeEvent(event)
