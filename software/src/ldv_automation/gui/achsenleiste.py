"""Achsenleiste AG der Auswertungsoberfläche (R-073, P-AUSW2 S3, Brief K1-AUSW2 3.1).

Je sichtbarer Achse eine Gruppe aus Beschriftung, Feld „von“, Feld „bis“, Einheit und (Frequenz,
Betrag) einem Umschalter linear/logarithmisch; dazu „Alles auf Auto“. Leere Felder bedeuten
Auto (die wirksamen Werte stehen grau im Feld), ein von Hand gesetzter oder per Zoom
übernommener Wert ist „fest“ (2 px Rahmen, getönter Hintergrund und „fest“ im
``accessibleDescription``, nie nur Farbe). Phase in Grad, Frequenz in Hz mit Dezimalkomma.

Die Leiste kennt nur den :class:`~ldv_automation.gui.achsen_zustand.AchsenZustand` (eine Quelle)
und meldet Änderungen über :attr:`Achsenleiste.geaendert`; Zeichnen und Zuordnung der Achsen
liegen beim Reiter und bei der :class:`~ldv_automation.gui.plotflaeche.PlotFlaeche`. Eine Eingabe
wirkt erst bei Enter oder Fokuswechsel und nur, wenn sich der Text geändert hat (UI-37).
Ungültige Eingaben (Text, ``von`` ≥ ``bis`` bei zwei gesetzten Seiten, Wert ≤ 0 auf der
Logarithmusachse) zeigen eine Meldung in einer reservierten Zeile unter der Gruppe (kein
Layoutsprung) und lassen den Zustand und damit den Plot unverändert (UI-5). Das Feld zeigt dabei
einen gestrichelten Rahmen in Fehlerfarbe (auch mit Fokus, auch in Graustufen vom festen Feld mit
durchgezogenem Rahmen unterscheidbar). Wird nur **eine** Seite gesetzt und liegt sie jenseits der
automatischen Gegenseite, gibt es keine Meldung: die Zeichenschicht verschiebt die Auto-Seite
(``achsen._wirksam``), und die Leiste zeigt danach diesen Wert grau (eine Regel für beide).

Dieses Modul ist ein dünnes Widget (Abdeckung nur mit ``pytest -m gui``); Prüfung, Einlesen,
Anzeigeformat und Texte liegen Qt-frei in :mod:`ldv_automation.darstellung.achsen`
(:func:`~ldv_automation.darstellung.achsen.uebernehme_eingabe`) und
:mod:`ldv_automation.gui.achsen_zustand`; hier bleiben nur Geometrie und Ereignisse.
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence

from PySide6.QtCore import QEvent, QObject, QPoint, QRect, QSize, Qt, Signal
from PySide6.QtWidgets import (
    QComboBox,
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QLayout,
    QLayoutItem,
    QLineEdit,
    QPushButton,
    QRadioButton,
    QSizePolicy,
    QWidget,
)

from ldv_automation.darstellung.achsen import (
    TEXT_KEINE_ZAHL,
    TEXT_LOG_NUR_POSITIV,
    TEXT_REIHENFOLGE,
    AchsenFehler,
    feld_text,
    pruefe_bereich,
    uebernehme_eingabe,
)
from ldv_automation.darstellung.zeichnung import Skala
from ldv_automation.gui import tokens as t
from ldv_automation.gui.achsen_zustand import ACHSEN_JE_ANSICHT, ACHSEN_NAMEN, AchsenZustand
from ldv_automation.gui.stil import setze_eigenschaft

__all__ = ["Achsenleiste", "FlussLayout"]

_PRAEFIX = {"frequenz": "achse_f", "betrag": "achse_y", "phase": "achse_phase"}
"""Präfix der ``objectName`` je Rolle (Brief K1-AUSW2 Abschnitt 7)."""
_EINHEIT_VORGABE = {"frequenz": "Hz", "phase": "°"}
"""Einheit je Rolle, solange die Zeichnung keine nennt (Frequenz, Phase in Grad)."""
_FELD_BREITE_PX = 84
"""Breite eines Zahlenfelds: reicht für die längsten Texte von ``feld_text`` (negative Potenz
mit zweistelligem Exponenten, negative Dezimalzahl mit sieben Stellen); ein Test misst es mit
der Schrift der Oberfläche."""
_MELDUNGEN = (TEXT_KEINE_ZAHL, TEXT_LOG_NUR_POSITIV, TEXT_REIHENFOLGE)
"""Standardmeldungen; die längste bestimmt die reservierte Breite der Meldezeile."""
_ABSTAND_PX = 12
"""Abstand zwischen den Gruppen nebeneinander (8-px-Raster)."""
_ZEILE_ABSTAND_PX = 4
"""Abstand der Teile innerhalb einer Gruppe (Beschriftung, Felder, Einheit, Skala)."""
_ZEILE_ABSTAND_KOMPAKT_PX = 2
"""Dasselbe bei kleinem Fenster: Frequenz, Betrag und „Auto“ bleiben bei 1100 px in einer Zeile."""
_ABSTAND_KOMPAKT_PX = 8
"""Abstand zwischen den Gruppen bei kleinem Fenster."""
_ZEILENABSTAND_PX = 2
"""Abstand zwischen den Zeilen der Leiste (jede Gruppe trägt ihre Meldezeile selbst)."""


class FlussLayout(QLayout):
    """Ordnet Widgets von links nach rechts und bricht bei Platzmangel in die nächste Zeile um.

    Nichts wird abgeschnitten (Brief 1: AG und AH brechen um); die Höhe folgt der Breite
    (``heightForWidth``). Die Umbruchlogik rechnet nur mit den ``sizeHint`` der Elemente und ist
    deshalb auch für die spätere Bedienleiste AH (Animation) verwendbar.

    Parameters
    ----------
    parent : QWidget, optional
        Widget, dessen Layout dies wird.
    abstand : int, optional
        Abstand zwischen Elementen (und, ohne ``zeilenabstand``, zwischen Zeilen) in Pixeln.
    zeilenabstand : int, optional
        Abstand zwischen den Zeilen, wenn er vom Abstand der Elemente abweichen soll.
    """

    def __init__(
        self,
        parent: QWidget | None = None,
        abstand: int = _ABSTAND_PX,
        zeilenabstand: int | None = None,
    ) -> None:
        super().__init__(parent)
        self._elemente: list[QLayoutItem] = []
        self._abstand = abstand
        self._zeilenabstand = abstand if zeilenabstand is None else zeilenabstand

    def setze_abstand(self, abstand: int) -> None:
        """Ändert den Abstand zwischen den Elementen (Zeilenabstand bleibt)."""
        self._abstand = abstand
        self.invalidate()

    def addItem(self, item: QLayoutItem) -> None:  # noqa: N802  # Qt-Name
        """Fügt ein Element am Ende hinzu."""
        self._elemente.append(item)

    def count(self) -> int:
        """Anzahl der Elemente."""
        return len(self._elemente)

    def itemAt(self, index: int) -> QLayoutItem | None:  # noqa: N802  # Qt-Name
        """Element an Position ``index`` (``None`` außerhalb)."""
        return self._elemente[index] if 0 <= index < len(self._elemente) else None

    def takeAt(self, index: int) -> QLayoutItem | None:  # noqa: N802  # Qt-Name
        """Entfernt das Element an Position ``index``."""
        return self._elemente.pop(index) if 0 <= index < len(self._elemente) else None

    def expandingDirections(self) -> Qt.Orientation:  # noqa: N802  # Qt-Name
        """Das Layout dehnt sich nicht aus."""
        return Qt.Orientation(0)

    def hasHeightForWidth(self) -> bool:  # noqa: N802  # Qt-Name
        """Die Höhe hängt von der Breite ab (Umbruch)."""
        return True

    def heightForWidth(self, breite: int) -> int:  # noqa: N802  # Qt-Name
        """Höhe bei der Breite ``breite``."""
        return self._ordne(QRect(0, 0, breite, 0), nur_messen=True)

    def setGeometry(self, rect: QRect) -> None:  # noqa: N802  # Qt-Name
        """Ordnet die Elemente in ``rect`` an."""
        super().setGeometry(rect)
        self._ordne(rect, nur_messen=False)

    def sizeHint(self) -> QSize:  # noqa: N802  # Qt-Name
        """Bevorzugt eine Zeile; mindestens das breiteste Element."""
        return self.minimumSize()

    def minimumSize(self) -> QSize:  # noqa: N802  # Qt-Name
        """Das größte Element plus Ränder: schmaler wird nie umbrochen."""
        groesse = QSize()
        for element in self._elemente:
            groesse = groesse.expandedTo(element.minimumSize())
        raender = self.contentsMargins()
        return groesse + QSize(raender.left() + raender.right(), raender.top() + raender.bottom())

    def _ordne(self, rect: QRect, *, nur_messen: bool) -> int:
        raender = self.contentsMargins()
        innen = rect.adjusted(raender.left(), raender.top(), -raender.right(), -raender.bottom())
        x = innen.x()
        y = innen.y()
        zeilenhoehe = 0
        for element in self._elemente:
            if element.isEmpty():  # ausgeblendetes Widget
                continue
            groesse = element.sizeHint()
            if x > innen.x() and x + groesse.width() > innen.right() + 1:
                x = innen.x()
                y += zeilenhoehe + self._zeilenabstand
                zeilenhoehe = 0
            if not nur_messen:
                element.setGeometry(QRect(QPoint(x, y), groesse))
            x += groesse.width() + self._abstand
            zeilenhoehe = max(zeilenhoehe, groesse.height())
        return y + zeilenhoehe - rect.y() + raender.bottom()


class _Gruppe(QFrame):
    """Eine Achse: Beschriftung, Felder „von“ und „bis“, Einheit, Skalaumschalter, Meldung."""

    def __init__(self, rolle: str, mit_skala: bool, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        name = ACHSEN_NAMEN[rolle]
        praefix = _PRAEFIX[rolle]
        self.rolle = rolle
        self.setObjectName(f"{praefix}_gruppe")
        gitter = QGridLayout(self)
        gitter.setContentsMargins(0, 0, 0, 0)
        gitter.setHorizontalSpacing(6)
        gitter.setVerticalSpacing(0)
        self.lbl_name = QLabel(f"{name}:")
        self.lbl_name.setObjectName(f"{praefix}_name")
        self.ed_von = self._feld(f"{praefix}_von", f"Achsenbereich {name} von")
        self.ed_bis = self._feld(f"{praefix}_bis", f"Achsenbereich {name} bis")
        # „von – bis“: dekorativ, ohne eigenen accessibleName (die Felder tragen „von“/„bis“)
        self.lbl_trenner = QLabel("–")
        self.lbl_einheit = QLabel(_EINHEIT_VORGABE.get(rolle, ""))
        self.lbl_einheit.setObjectName(f"{praefix}_einheit")
        self.lbl_einheit.setProperty("art", "gedaempft")
        self.lbl_name.setBuddy(self.ed_von)
        # Ansicht 5, nebeneinander: Auswahl der Betragsgröße, auf die sich die Felder beziehen
        self.cb_groesse: QComboBox | None = None
        if rolle == "betrag":
            self.cb_groesse = QComboBox()
            self.cb_groesse.setObjectName(f"{praefix}_groesse")
            self.cb_groesse.setAccessibleName("Größe der Betragsfelder")
            self.cb_groesse.setToolTip(
                "Größe, auf die sich Bereich und Skala des Betrags beziehen "
                "(nebeneinander: jede Größe hat ihre eigene Achse)"
            )
            self.cb_groesse.setVisible(False)
        zeile = QHBoxLayout()
        self._zeile = zeile
        zeile.setContentsMargins(0, 0, 0, 0)
        zeile.setSpacing(_ZEILE_ABSTAND_PX)
        for widget in (
            self.lbl_name,
            *([self.cb_groesse] if self.cb_groesse is not None else []),
            self.ed_von,
            self.lbl_trenner,
            self.ed_bis,
            self.lbl_einheit,
        ):
            zeile.addWidget(widget)
        self.rb_linear: QRadioButton | None = None
        self.rb_log: QRadioButton | None = None
        self.skala_box: QWidget | None = None
        if mit_skala:
            self.skala_box = QWidget()
            self.skala_box.setObjectName(f"{praefix}_skala")
            box = QHBoxLayout(self.skala_box)
            box.setContentsMargins(0, 0, 0, 0)
            box.setSpacing(4)
            self.rb_linear = QRadioButton("linear")
            self.rb_log = QRadioButton("logarithmisch")
            for knopf, zusatz in ((self.rb_linear, "linear"), (self.rb_log, "logarithmisch")):
                knopf.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
                knopf.setAccessibleName(f"Skala {name} {zusatz}")
                box.addWidget(knopf)
            self.rb_linear.setObjectName(f"{praefix}_skala_linear")
            self.rb_log.setObjectName(f"{praefix}_skala_log")
            zeile.addSpacing(8)  # Einheit und Umschalter nicht aneinander (Abstand 12 px)
            zeile.addWidget(self.skala_box)
        gitter.addLayout(zeile, 0, 0)
        self.lbl_meldung = QLabel()
        self.lbl_meldung.setObjectName(f"{praefix}_meldung")
        self.lbl_meldung.setProperty("art", "fehler")
        self.lbl_meldung.setWordWrap(False)
        # Reservierte Zeile: Höhe und Breite bleiben auch ohne Meldung erhalten, damit Werkzeug-
        # leiste und Plot beim Ein- und Ausblenden nicht springen und die Leiste nicht umbricht.
        self.lbl_meldung.ensurePolished()
        breiteste = max(_MELDUNGEN, key=self.lbl_meldung.fontMetrics().horizontalAdvance)
        self.lbl_meldung.setText(f"{t.symbol('fehler')} {breiteste}")
        platz = self.lbl_meldung.sizeHint()  # Größe mit Text: so viel Platz wird reserviert
        self.lbl_meldung.setText("")
        self.lbl_meldung.setFixedHeight(platz.height())
        self.lbl_meldung.setMinimumWidth(platz.width() + 8)
        reserviert = self.lbl_meldung.sizePolicy()
        reserviert.setRetainSizeWhenHidden(True)
        self.lbl_meldung.setSizePolicy(reserviert)
        self.lbl_meldung.setVisible(False)
        gitter.addWidget(self.lbl_meldung, 1, 0)

    def setze_kompakt(self, kompakt: bool) -> None:
        """Enger Abstand der Teile einer Gruppe (kleines Fenster)."""
        self._zeile.setSpacing(_ZEILE_ABSTAND_KOMPAKT_PX if kompakt else _ZEILE_ABSTAND_PX)

    @staticmethod
    def _feld(objekt: str, accessible: str) -> QLineEdit:
        feld = QLineEdit()
        feld.setObjectName(objekt)
        feld.setAccessibleName(accessible)
        feld.setPlaceholderText("Auto")
        feld.setFixedWidth(_FELD_BREITE_PX)
        # gleiche Höhe bei 1 px Rahmen und Innenabstand wie bei 2 px Rahmen (fest, Fehler, Fokus):
        # sonst spränge die Leiste beim Setzen eines Werts (Regeln in ``stil``)
        feld.setProperty("achsenfeld", "true")
        feld.setAlignment(Qt.AlignmentFlag.AlignRight)
        feld.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        return feld

    def feld(self, seite: str) -> QLineEdit:
        """Das Feld ``"von"`` oder ``"bis"``."""
        return self.ed_von if seite == "von" else self.ed_bis


class Achsenleiste(QWidget):
    """Zone AG: Eingabe der Achsenbereiche und -skalen (R-073).

    Parameters
    ----------
    zustand : AchsenZustand
        Der Zustand, den die Leiste liest und schreibt (derselbe wie der der Plotfläche).
    parent : QWidget, optional
        Elternwidget.

    Notes
    -----
    Die Leiste liegt als **Geschwister** der Plotfläche im Reiter: Ihre Textfelder behalten so
    „Pos1“ (Zeilenanfang); der Kurzbefehl „Zurücksetzen“ gilt nur im Teilbaum der Plotfläche.
    """

    geaendert = Signal()
    """Der Zustand wurde durch eine gültige Eingabe, den Skalaumschalter oder „Alles auf Auto“
    geändert; die Plotfläche ist neu zu zeichnen (genau einmal je Eingabe)."""

    groesse_gewaehlt = Signal(str)
    """Die Betragsgröße der Betragsfelder wurde gewählt (Ansicht 5, nebeneinander); der Zustand
    ist schon umgestellt, die Felder sind aus den Grenzen der Größe neu zu zeigen."""

    def __init__(self, zustand: AchsenZustand, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setObjectName("achsenleiste")
        self.setAccessibleName("Achsenleiste")
        self._zustand = zustand
        self._ansicht = 1
        self._wirksam: dict[str, tuple[float, float]] = {}
        self._angezeigt: dict[tuple[str, str], str] = {}
        self._fehler: set[tuple[str, str]] = set()
        self._gruppen: dict[str, _Gruppe] = {
            "frequenz": _Gruppe("frequenz", True),
            "betrag": _Gruppe("betrag", True),
            "phase": _Gruppe("phase", False),
        }
        # Die reservierte Meldezeile trennt die Zeilen schon; ein kleiner Zeilenabstand hält die
        # Leiste bei 1100 mal 680 so niedrig, dass der Plot in Ansicht 3 seine Mindesthöhe behält.
        layout = FlussLayout(self, zeilenabstand=_ZEILENABSTAND_PX)
        layout.setContentsMargins(0, 2, 0, 2)
        self._fluss = layout
        for gruppe in self._gruppen.values():
            layout.addWidget(gruppe)
        self.btn_auto = QPushButton("Alles auf Auto")
        self.btn_auto.setObjectName("btn_achsen_auto")
        self.btn_auto.setAccessibleName("Alle Achsen auf Auto")
        self.btn_auto.setToolTip("Alle Achsenbereiche dieser Ansicht automatisch (Skalen bleiben)")
        self.btn_auto.setAutoDefault(False)
        self.btn_auto.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.btn_auto.clicked.connect(self._alles_auto)
        layout.addWidget(self.btn_auto)
        cb = self._gruppen["betrag"].cb_groesse
        assert cb is not None
        cb.activated.connect(self._groesse_aktiviert)
        for gruppe in self._gruppen.values():
            for seite in ("von", "bis"):
                feld = gruppe.feld(seite)
                feld.installEventFilter(self)
                feld.editingFinished.connect(
                    lambda r=gruppe.rolle, s=seite: self._uebernehme_feld(r, s)
                )
                self._angezeigt[(gruppe.rolle, seite)] = ""
            if gruppe.rb_linear is not None and gruppe.rb_log is not None:
                gruppe.rb_linear.toggled.connect(
                    lambda an, r=gruppe.rolle: self._skala_gewaehlt(r, "linear", an)
                )
                gruppe.rb_log.toggled.connect(
                    lambda an, r=gruppe.rolle: self._skala_gewaehlt(r, "log", an)
                )
        self.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Minimum)
        self._zeige_skalen()

    # --- Zugriff ---------------------------------------------------------------------------

    def gruppe(self, rolle: str) -> _Gruppe:
        """Die Gruppe der Rolle (``"frequenz"``, ``"betrag"``, ``"phase"``)."""
        return self._gruppen[rolle]

    def fehler_aktiv(self, rolle: str, seite: str) -> bool:
        """Zeigt das Feld eine Fehlermeldung (ungültige Eingabe, noch nicht quittiert)."""
        return (rolle, seite) in self._fehler

    def tab_kette(self) -> list[QWidget]:
        """Bedienbare Elemente in Tab-Reihenfolge (Brief Abschnitt 6: AD → AG → AE)."""
        kette: list[QWidget] = []
        for gruppe in self._gruppen.values():
            if gruppe.cb_groesse is not None and not gruppe.cb_groesse.isHidden():
                kette.append(gruppe.cb_groesse)
            kette += [gruppe.ed_von, gruppe.ed_bis]
            if gruppe.rb_linear is not None and gruppe.rb_log is not None:
                kette += [gruppe.rb_linear, gruppe.rb_log]
        kette.append(self.btn_auto)
        return kette

    def setze_ansicht(self, ansicht: int) -> None:
        """Wechselt die Ansicht: Meldungen der alten Ansicht entfallen, Skalen werden gezeigt."""
        self._ansicht = ansicht
        self._wirksam = {}
        self._verwerfe_fehler()
        self._verwerfe_entwuerfe()
        self.setze_groessen([], self._zustand.groesse_5)  # nur Ansicht 5 nebeneinander bietet an
        self._zeige_skalen()
        self.setVisible(ansicht in ACHSEN_JE_ANSICHT)

    def setze_kompakt(self, kompakt: bool) -> None:
        """Kurze Beschriftungen bei schmalem Fenster (Skalaknöpfe „lin“/„log“, „Auto“).

        Die vollständigen Namen bleiben in ``accessibleName`` und Tooltip; die Leiste braucht so
        bei 1100 px Breite nur noch eine Zeile für Frequenz und Betrag.
        """
        self._fluss.setze_abstand(_ABSTAND_KOMPAKT_PX if kompakt else _ABSTAND_PX)
        for gruppe in self._gruppen.values():
            gruppe.setze_kompakt(kompakt)
            if gruppe.rb_linear is not None and gruppe.rb_log is not None:
                gruppe.rb_linear.setText("lin" if kompakt else "linear")
                gruppe.rb_log.setText("log" if kompakt else "logarithmisch")
                gruppe.rb_linear.setToolTip("linear" if kompakt else "")
                gruppe.rb_log.setToolTip("logarithmisch" if kompakt else "")
        self.btn_auto.setText("Auto" if kompakt else "Alles auf Auto")
        self.updateGeometry()

    def setze_groessen(self, angebot: Sequence[tuple[str, str]], aktuell: str) -> None:
        """Bietet die Betragsgrößen an, auf die sich die Betragsfelder beziehen können.

        Parameters
        ----------
        angebot : sequence of (str, str)
            Kennung und Anzeigename der gezeichneten Betragsgrößen; weniger als zwei blenden die
            Auswahl aus (die Felder gehören dann zur einzigen Größe).
        aktuell : str
            Kennung der Größe, auf die sich die Felder jetzt beziehen.
        """
        cb = self._gruppen["betrag"].cb_groesse
        assert cb is not None
        kennungen = [k for k, _name in angebot]
        sichtbar = len(angebot) > 1
        cb.blockSignals(True)
        if kennungen != [cb.itemData(i) for i in range(cb.count())]:
            cb.clear()
            for kennung, name in angebot:
                cb.addItem(name, kennung)
        if aktuell in kennungen:
            cb.setCurrentIndex(kennungen.index(aktuell))
        cb.blockSignals(False)
        if cb.isHidden() == sichtbar:
            cb.setVisible(sichtbar)
            self.updateGeometry()

    def _groesse_aktiviert(self, index: int) -> None:
        """Auswahl der Größe: Entwürfe und Meldungen entfallen, der Zustand bezieht sich um."""
        cb = self._gruppen["betrag"].cb_groesse
        assert cb is not None
        kennung = cb.itemData(index)
        if not isinstance(kennung, str) or kennung == self._zustand.groesse_5:
            return
        self._verwerfe_fehler()
        self._verwerfe_entwuerfe()
        self._zustand.setze_groesse_5(kennung)
        self.groesse_gewaehlt.emit(kennung)

    def aktualisiere(
        self, wirksam: Mapping[str, tuple[float, float]], einheiten: Mapping[str, str]
    ) -> None:
        """Zeigt Zustand und wirksame Grenzen (nach jedem Zeichnen und nach jeder Rückkopplung).

        Parameters
        ----------
        wirksam : mapping
            Sichtbare Grenzen je Rolle (``frequenz``, ``betrag``, ``phase``) der gezeichneten
            Achsen; nur diese Rollen erscheinen (Phase nur mit „Phase anzeigen“).
        einheiten : mapping
            Einheit je Rolle (aus den Achsentiteln der Zeichnung); fehlende Rollen behalten
            Hz bzw. Grad.
        """
        self._wirksam = dict(wirksam)
        rollen = [r for r in ACHSEN_JE_ANSICHT.get(self._ansicht, ()) if r in self._wirksam]
        for rolle, gruppe in self._gruppen.items():
            gruppe.setVisible(rolle in rollen)
            if rolle not in rollen:
                continue
            gruppe.lbl_einheit.setText(einheiten.get(rolle, _EINHEIT_VORGABE.get(rolle, "")))
            bereich = self._zustand.bereich(self._ansicht, rolle)
            auto = self._wirksam[rolle]
            for seite, fest, wirksam_wert in (
                ("von", bereich.von, auto[0]),
                ("bis", bereich.bis, auto[1]),
            ):
                self._zeige_feld(gruppe, seite, fest, wirksam_wert)
        self._zeige_skalen()
        self.updateGeometry()

    # --- Anzeige ---------------------------------------------------------------------------

    def _zeige_feld(
        self, gruppe: _Gruppe, seite: str, fest: float | None, wirksam_wert: float
    ) -> None:
        schluessel = (gruppe.rolle, seite)
        feld = gruppe.feld(seite)
        if schluessel in self._fehler:
            return  # die Meldung bleibt, bis sie quittiert wird (Fokuswechsel, UI-5)
        if feld.hasFocus() and feld.text() != self._angezeigt[schluessel]:
            return  # gerade in Bearbeitung: nichts überschreiben
        text = feld_text(fest)
        name = ACHSEN_NAMEN[gruppe.rolle]
        self._angezeigt[schluessel] = text
        feld.setText(text)
        feld.setPlaceholderText(feld_text(wirksam_wert))
        ist_fest = fest is not None
        setze_eigenschaft(feld, "fest", "true" if ist_fest else "false")
        setze_eigenschaft(feld, "fehler", "false")
        beschreibung = (
            f"{name} {seite}: fest, von Hand gesetzt"
            if ist_fest
            else f"{name} {seite}: Auto, aktuell {feld_text(wirksam_wert)}"
        )
        feld.setAccessibleDescription(beschreibung)
        feld.setToolTip("fest (von Hand gesetzt oder per Zoom übernommen)" if ist_fest else "Auto")
        gruppe.lbl_meldung.setVisible(any(k[0] == gruppe.rolle for k in self._fehler))

    def _zeige_skalen(self) -> None:
        """Stellt die Umschalter nach dem Zustand der Ansicht (ohne Signal)."""
        for rolle in ("frequenz", "betrag"):
            gruppe = self._gruppen[rolle]
            if gruppe.rb_linear is None or gruppe.rb_log is None:
                continue
            log = self._zustand.skala(self._ansicht, rolle) == "log"
            for knopf in (gruppe.rb_linear, gruppe.rb_log):
                knopf.blockSignals(True)
            gruppe.rb_log.setChecked(log)
            gruppe.rb_linear.setChecked(not log)
            for knopf in (gruppe.rb_linear, gruppe.rb_log):
                knopf.blockSignals(False)
            self._tab_halt(gruppe)

    @staticmethod
    def _tab_halt(gruppe: _Gruppe) -> None:
        """Tab-Halt auf der gewählten Skala (Pfeiltasten wechseln, UI-34)."""
        if gruppe.rb_linear is None or gruppe.rb_log is None:
            return
        for knopf in (gruppe.rb_linear, gruppe.rb_log):
            knopf.setFocusPolicy(
                Qt.FocusPolicy.StrongFocus if knopf.isChecked() else Qt.FocusPolicy.ClickFocus
            )

    # --- Eingabe ---------------------------------------------------------------------------

    def _skala_der_rolle(self, rolle: str) -> Skala:
        return self._zustand.skala(self._ansicht, rolle) if rolle != "phase" else "linear"

    def _uebernehme_feld(self, rolle: str, seite: str) -> None:
        """Enter oder Fokuswechsel im Feld: prüfen, in den Zustand schreiben, neu zeichnen."""
        gruppe = self._gruppen[rolle]
        feld = gruppe.feld(seite)
        text = feld.text()
        if text == self._angezeigt[(rolle, seite)] and (rolle, seite) not in self._fehler:
            return  # unverändert: kein Neuzeichnen (UI-37)
        alt = self._zustand.bereich(self._ansicht, rolle)
        try:
            neu = uebernehme_eingabe(
                text,
                seite,
                alt,
                self._skala_der_rolle(rolle),
                ACHSEN_NAMEN[rolle],
            )
        except AchsenFehler as fehler:
            self._zeige_fehler(rolle, seite, str(fehler))
            return
        self._quittiere(rolle, seite)
        self._angezeigt[(rolle, seite)] = text
        if neu == alt:
            return
        self._zustand.setze_bereich(self._ansicht, rolle, neu)
        self.geaendert.emit()

    def _zeige_fehler(self, rolle: str, seite: str, text: str) -> None:
        gruppe = self._gruppen[rolle]
        feld = gruppe.feld(seite)
        self._fehler.add((rolle, seite))
        gruppe.lbl_meldung.setText(f"{t.symbol('fehler')} {text}")
        gruppe.lbl_meldung.setVisible(True)
        gruppe.lbl_meldung.setAccessibleName(f"Fehler: {text}")
        setze_eigenschaft(feld, "fehler", "true")
        feld.setAccessibleDescription(f"Ungültige Eingabe: {text}")
        self.updateGeometry()

    def _quittiere(self, rolle: str, seite: str) -> None:
        """Nimmt die Fehlermeldung des Felds zurück (gültige Eingabe oder Fokuswechsel)."""
        self._fehler.discard((rolle, seite))
        gruppe = self._gruppen[rolle]
        setze_eigenschaft(gruppe.feld(seite), "fehler", "false")
        if not any(k[0] == rolle for k in self._fehler):
            gruppe.lbl_meldung.setVisible(False)
            gruppe.lbl_meldung.setText("")
        self.updateGeometry()

    def _verwerfe_fehler(self) -> None:
        for rolle, seite in list(self._fehler):
            self._quittiere(rolle, seite)

    def _verwerfe_entwuerfe(self) -> None:
        """Setzt jedes Feld mit ungeschriebenem Text (auch ungültigem) auf den letzten Wert.

        Beim Ansichtswechsel per Tastatur behält ein Feld seinen Fokus; sein Text gehörte aber
        zur Achse der alten Ansicht und darf nicht stehen bleiben.
        """
        for (rolle, seite), gespeichert in self._angezeigt.items():
            feld = self._gruppen[rolle].feld(seite)
            if feld.text() != gespeichert:
                feld.setText(gespeichert)  # setText löst kein editingFinished aus

    def eventFilter(self, watched: QObject, event: QEvent) -> bool:  # noqa: N802  # Qt-Name
        """Fokuswechsel aus einem Feld mit Meldung quittiert sie: der alte Wert kehrt zurück."""
        if event.type() == QEvent.Type.FocusOut:
            for (rolle, seite), _text in list(self._angezeigt.items()):
                gruppe = self._gruppen[rolle]
                if gruppe.feld(seite) is watched and (rolle, seite) in self._fehler:
                    gespeichert = self._angezeigt[(rolle, seite)]
                    self._quittiere(rolle, seite)
                    gruppe.feld(seite).setText(gespeichert)  # alter Wert, kein editingFinished
                    gruppe.feld(seite).setToolTip("")
        return super().eventFilter(watched, event)

    def _skala_gewaehlt(self, rolle: str, skala: str, an: bool) -> None:
        """Umschalter linear/logarithmisch: nur bei gültigen festen Werten (Logarithmus > 0)."""
        if not an:
            return
        gruppe = self._gruppen[rolle]
        if skala == "log":
            try:
                pruefe_bereich(
                    self._zustand.bereich(self._ansicht, rolle), "log", ACHSEN_NAMEN[rolle]
                )
            except AchsenFehler as fehler:
                self._zeige_skala_fehler(gruppe, str(fehler))
                self._zeige_skalen()  # Umschalter zurück auf die gültige Skala
                return
        self._verwerfe_skala_fehler(gruppe)
        achse = "frequenz" if rolle == "frequenz" else "betrag"
        if self._zustand.skala(self._ansicht, achse) == skala:
            self._tab_halt(gruppe)
            return
        self._zustand.setze_skala(self._ansicht, achse, skala)  # type: ignore[arg-type]
        self._tab_halt(gruppe)
        self.geaendert.emit()

    def _zeige_skala_fehler(self, gruppe: _Gruppe, text: str) -> None:
        gruppe.lbl_meldung.setText(f"{t.symbol('fehler')} {text}")
        gruppe.lbl_meldung.setVisible(True)
        gruppe.lbl_meldung.setAccessibleName(f"Fehler: {text}")
        self.updateGeometry()

    def _verwerfe_skala_fehler(self, gruppe: _Gruppe) -> None:
        if not any(k[0] == gruppe.rolle for k in self._fehler):
            gruppe.lbl_meldung.setVisible(False)
            gruppe.lbl_meldung.setText("")

    def _alles_auto(self) -> None:
        """„Alles auf Auto“: alle Bereiche der Ansicht automatisch, Felder leer (UI-4)."""
        self._verwerfe_fehler()
        self._verwerfe_entwuerfe()
        self._zustand.auf_auto(self._ansicht)
        self.geaendert.emit()

    def sizeHint(self) -> QSize:  # noqa: N802  # Qt-Name
        """Bevorzugte Größe: eine Zeile, bei Platzmangel bricht das Layout um."""
        layout = self.layout()
        return layout.sizeHint() if layout is not None else super().sizeHint()
