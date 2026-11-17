r"""Qt-freie Steuerung der 3D-Animation (R-071, Plan P-AUSW3 AN5, ADR-029).

Alles, was die Oberfläche entscheidet, aber ohne Qt prüfbar ist, steht hier und wird im
Standardlauf voll gemessen (KONVENTIONEN, Coverage-Regel für GUI-Logik):

- :class:`Phasenuhr`: Winkel :math:`\theta` aus einer **Uhr** (injizierbar), Wiedergabe, Pause,
  Einzelschritt. Ausgelassene Bilder ändern die Phase nicht (E-A4, FG-04 3.7: nicht die
  Echtzeit, die Phase wird abgetastet).
- :class:`Blickzustand`: Drehen, Zoom, Blickvorgaben, Zurücksetzen (Pixel → Winkel).
- :func:`taste_zu_aktion`: Tastenbelegung (F-A3: ←/→ ändern die Phase, Umschalt+Pfeile und ↑/↓
  drehen) und :func:`wende_an`.
- :func:`optionen_stufe`/:class:`Stufe`: Rückfallstufen L0 bis L2 (ADR-029, Plan 4.3) als eine
  Einstellung, nicht als Verzweigungen im Code.
- :func:`beschreibung_animation`: Textalternative (zugängliche Beschreibung).
- :func:`frequenzwechsel`: Zustand nach Frequenzwechsel (F-A4: zurück ins Standbild).
- :func:`skalierung_nach_groessenwechsel`: Bildgröße beim Wechsel Auslenkung ↔ Schnelle erhalten
  (FG-04 Nachtrag 2, F-S1).

Winkel intern in rad, Anzeige in Grad (KONVENTIONEN). Voreinstellungen von Bildrate, Tempo
und Stufe sind **vorläufig** bis zur Messung am Messrechner (Plan Abschnitt 6, UI-38).
"""

from __future__ import annotations

import math
import time
from collections.abc import Callable, Mapping
from dataclasses import dataclass, replace
from enum import Enum

from ldv_automation.darstellung.animation3d import (
    BLICK_VORGABEN,
    AnimationsOptionen,
    Blick,
    effektive_ueberhoehung,
    ohne_nachbarabstand,
    pflichttexte,
)
from ldv_automation.darstellung.animation_daten import AnimationsDaten
from ldv_automation.darstellung.formate import zahl_kurz_text, zahl_text
from ldv_automation.darstellung.stil import Plotstil

__all__ = [
    "ANIMATIONS_TASTEN",
    "BILDRATE_VORGABE",
    "DREH_SCHRITT_GRAD",
    "GRAD_JE_PIXEL",
    "SCHRITT_VORGABE_GRAD",
    "STUFE_VORGABE",
    "TEMPO_VORGABE",
    "ZOOM_MAX",
    "ZOOM_MIN",
    "Aktion",
    "Blickzustand",
    "Ereignis",
    "Phasenuhr",
    "Stufe",
    "StufenVerhalten",
    "beschreibung_animation",
    "frequenzwechsel",
    "optionen_stufe",
    "phase_text",
    "skalierung_nach_groessenwechsel",
    "skalierung_text",
    "taste_zu_aktion",
    "ueberhoehung_text",
    "verhalten",
    "wende_an",
]

BILDRATE_VORGABE = 10
"""Bilder je Sekunde (vorläufig, Plan Abschnitt 6; Anpassung nach Messung M2)."""
TEMPO_VORGABE = 0.25
"""Perioden je Sekunde Echtzeit (vorläufig; unabhängig von der Messfrequenz, Zeitlupe)."""
SCHRITT_VORGABE_GRAD = 10.0
"""Schrittweite der Einzelschritte in Grad: 36 Bilder je Periode (E3, FG-04 3.7)."""
DREH_SCHRITT_GRAD = 5.0
"""Drehen und Elevation je Tastendruck in Grad (F-A3)."""
GRAD_JE_PIXEL = 0.4
"""Drehen mit der Maus: Grad je Pixel (Azimut += k·dx, Elevation -= k·dy)."""
ZOOM_MIN = 0.4
"""Kleinster Zoomfaktor (Plan 5.1)."""
ZOOM_MAX = 6.0
"""Größter Zoomfaktor (Plan 5.1)."""
_ZOOM_RASTE = 1.1  # Faktor je Rastschritt des Mausrads
_PHASE_GROB_GRAD = 90.0  # Strg+←/→ (Kann)
_VOLLKREIS = 2.0 * math.pi


class Stufe(Enum):
    """Rückfallstufe der Darstellung (ADR-029, Plan 4.3); L3 gehört nicht zum Umfang."""

    L0 = 0
    L1 = 1
    L2 = 2


STUFE_VORGABE = Stufe.L0
"""Voreinstellung: Teilaktualisierung, vereinfachte Achsen nur in Bewegung."""


class Ereignis(Enum):
    """Anlass einer Darstellung, für den die Stufe das Verhalten bestimmt."""

    STAND = "stand"
    WIEDERGABE = "wiedergabe"
    REGLER = "regler"
    DREHEN = "drehen"


@dataclass(frozen=True)
class StufenVerhalten:
    """Verhalten einer Rückfallstufe.

    Attributes
    ----------
    vereinfacht : frozenset of Ereignis
        Ereignisse, bei denen die Achsen vereinfacht (ohne Panes und Ticks) gezeichnet werden.
    neuzeichnen_beim_loslassen : bool
        Regler und Drehen zeichnen erst beim Loslassen (Regler ``tracking`` aus, Drehen zeigt
        nur ein Skelett).
    wiedergabe : bool
        ``False``: Einzelschritt statt Wiedergabe (Remotedesktop zu langsam, OE-A2).
    """

    vereinfacht: frozenset[Ereignis]
    neuzeichnen_beim_loslassen: bool
    wiedergabe: bool


_STUFEN: Mapping[Stufe, StufenVerhalten] = {
    Stufe.L0: StufenVerhalten(
        vereinfacht=frozenset({Ereignis.WIEDERGABE, Ereignis.DREHEN}),
        neuzeichnen_beim_loslassen=False,
        wiedergabe=True,
    ),
    Stufe.L1: StufenVerhalten(
        vereinfacht=frozenset({Ereignis.WIEDERGABE, Ereignis.DREHEN, Ereignis.REGLER}),
        neuzeichnen_beim_loslassen=False,
        wiedergabe=True,
    ),
    Stufe.L2: StufenVerhalten(
        vereinfacht=frozenset({Ereignis.WIEDERGABE, Ereignis.DREHEN, Ereignis.REGLER}),
        neuzeichnen_beim_loslassen=True,
        wiedergabe=False,
    ),
}


def verhalten(stufe: Stufe) -> StufenVerhalten:
    """Verhalten der Stufe ``stufe``."""
    return _STUFEN[stufe]


def optionen_stufe(stufe: Stufe, ereignis: Ereignis) -> bool:
    """Prüft, ob die Achsen bei ``ereignis`` in Stufe ``stufe`` vereinfacht gezeichnet werden.

    Im Stand (:attr:`Ereignis.STAND`) sind die Achsen nie vereinfacht: Panes, Ticks und Gitter
    stehen im ruhenden Bild und im gespeicherten Standbild.
    """
    return ereignis in _STUFEN[stufe].vereinfacht


# --- Phase ------------------------------------------------------------------------------------


def _normiere(theta_rad: float) -> float:
    """Winkel auf ``[0, 2π)``."""
    wert = math.fmod(theta_rad, _VOLLKREIS)
    if wert < 0.0:
        wert += _VOLLKREIS
    return 0.0 if wert >= _VOLLKREIS else wert


class Phasenuhr:
    r"""Animationswinkel :math:`\theta`, Wiedergabe und Einzelschritte (UI-24, UI-32).

    Während der Wiedergabe gilt :math:`\theta = \theta_0 + 2\pi f_\mathrm{anim}\,(t - t_0)` mit der
    **Uhr** ``zeit`` (nicht der Zahl der Takte): Eine langsame Zeichnung lässt Bilder aus, die
    Bewegung bleibt zeitrichtig. Die Messfrequenz geht nicht ein; ``tempo_hz`` sind Perioden je
    Sekunde Echtzeit (Zeitlupe).

    Parameters
    ----------
    zeit : callable, optional
        Zeitquelle in s (monoton); Voreinstellung :func:`time.monotonic`.
    tempo_hz : float
        Perioden je Sekunde, > 0.
    schritt_grad : float
        Schrittweite der Einzelschritte in Grad, 0 < schritt ≤ 360.
    """

    def __init__(
        self,
        zeit: Callable[[], float] = time.monotonic,
        *,
        tempo_hz: float = TEMPO_VORGABE,
        schritt_grad: float = SCHRITT_VORGABE_GRAD,
    ) -> None:
        self._zeit = zeit
        self._theta = 0.0
        self._t0 = 0.0
        self._laeuft = False
        self._tempo = _pruefe_tempo(tempo_hz)
        self._schritt = _pruefe_schritt(schritt_grad)

    @property
    def laeuft(self) -> bool:
        """Wiedergabe aktiv."""
        return self._laeuft

    @property
    def tempo_hz(self) -> float:
        """Perioden je Sekunde."""
        return self._tempo

    @property
    def schritt_grad(self) -> float:
        """Schrittweite der Einzelschritte in Grad."""
        return self._schritt

    @property
    def theta_rad(self) -> float:
        """Letzter ausgewerteter Winkel in rad, ``[0, 2π)`` (ohne neue Zeitabfrage)."""
        return self._theta

    @property
    def theta_grad(self) -> float:
        """Letzter ausgewerteter Winkel in Grad, ``[0, 360)``."""
        return math.degrees(self._theta)

    def tick(self) -> float:
        r"""Winkel zur aktuellen Zeit (bei laufender Wiedergabe), im Zustand festgehalten.

        Returns
        -------
        float
            :math:`\\theta` in rad, ``[0, 2π)``.
        """
        if self._laeuft:
            jetzt = self._zeit()
            self._theta = _normiere(self._theta + _VOLLKREIS * self._tempo * (jetzt - self._t0))
            self._t0 = jetzt
        return self._theta

    def start(self) -> None:
        """Wiedergabe starten oder fortsetzen (aus dem aktuellen Winkel)."""
        if not self._laeuft:
            self._t0 = self._zeit()
            self._laeuft = True

    def pause(self) -> float:
        """Wiedergabe anhalten; der Winkel zum Zeitpunkt der Pause bleibt stehen.

        Returns
        -------
        float
            Winkel in rad.
        """
        wert = self.tick()
        self._laeuft = False
        return wert

    def umschalten(self) -> bool:
        """Abspielen/Pause (Leertaste); gibt ``True`` zurück, wenn danach abgespielt wird."""
        if self._laeuft:
            self.pause()
        else:
            self.start()
        return self._laeuft

    def schritt(self, vorzeichen: int, grad: float | None = None) -> float:
        """Einzelschritt um die Schrittweite (``grad`` überschreibt sie); hält die Wiedergabe an.

        Parameters
        ----------
        vorzeichen : int
            ``+1`` vor, ``-1`` zurück.
        grad : float, optional
            Schrittweite in Grad für diesen Schritt (z. B. 90° bei Strg+Pfeil).

        Returns
        -------
        float
            Neuer Winkel in rad.
        """
        if vorzeichen not in (-1, 1):
            raise ValueError(f"vorzeichen +1 oder -1 erwartet: {vorzeichen}")
        weite = self._schritt if grad is None else _pruefe_schritt(grad)
        self.pause()
        self._theta = _normiere(self._theta + vorzeichen * math.radians(weite))
        return self._theta

    def setze_theta_rad(self, theta_rad: float) -> None:
        """Setzt den Winkel (Phasenregler); die Wiedergabe läuft ab dem neuen Winkel weiter."""
        if not math.isfinite(theta_rad):
            raise ValueError(f"theta endlich erwartet: {theta_rad}")
        self.tick()
        self._theta = _normiere(theta_rad)
        self._t0 = self._zeit()

    def setze_theta_grad(self, grad: float) -> None:
        """Wie :meth:`setze_theta_rad`, Eingabe in Grad (Phasenregler, Feld)."""
        self.setze_theta_rad(math.radians(grad))

    def setze_tempo(self, tempo_hz: float) -> None:
        """Ändert das Tempo; der bisherige Verlauf bleibt erhalten."""
        self.tick()
        self._tempo = _pruefe_tempo(tempo_hz)

    def setze_schritt_grad(self, schritt_grad: float) -> None:
        """Ändert die Schrittweite der Einzelschritte."""
        self._schritt = _pruefe_schritt(schritt_grad)

    def zuruecksetzen(self) -> None:
        """Winkel 0 und Wiedergabe aus (Modus-Wechsel, Frequenzwechsel)."""
        self._laeuft = False
        self._theta = 0.0


def _pruefe_tempo(tempo_hz: float) -> float:
    if not (math.isfinite(tempo_hz) and tempo_hz > 0.0):
        raise ValueError(f"tempo_hz > 0 erwartet: {tempo_hz}")
    return float(tempo_hz)


def _pruefe_schritt(grad: float) -> float:
    if not (math.isfinite(grad) and 0.0 < grad <= 360.0):
        raise ValueError(f"Schrittweite 0 < Grad <= 360 erwartet: {grad}")
    return float(grad)


# --- Blick ------------------------------------------------------------------------------------


def _normiere_azimut(azim_grad: float) -> float:
    """Azimut auf ``(-180°, 180°]``."""
    wert = math.fmod(azim_grad + 180.0, 360.0)
    if wert <= 0.0:
        wert += 360.0
    return wert - 180.0


class Blickzustand:
    """Blickrichtung und Zoom mit Drehen, Zoom, Vorgaben und Zurücksetzen (Plan 5.1, UI-23).

    Parameters
    ----------
    vorgabe : str
        Name in :data:`~ldv_automation.darstellung.animation3d.BLICK_VORGABEN`; Zurücksetzen
        kehrt zu ihr zurück (Pos1 setzt Blick und Zoom, nicht Winkel und Überhöhung).
    """

    def __init__(self, vorgabe: str = "xy") -> None:
        self._vorgabe_name = vorgabe
        self._blick = BLICK_VORGABEN[vorgabe]

    @property
    def blick(self) -> Blick:
        """Aktueller Blick."""
        return self._blick

    @property
    def vorgabe(self) -> str:
        """Name der Vorgabe, zu der :meth:`zuruecksetzen` zurückkehrt."""
        return self._vorgabe_name

    def waehle_vorgabe(self, name: str) -> Blick:
        """Setzt Blick und Zoom auf die Vorgabe ``name`` (Knöpfe xy, xz, yz, iso)."""
        if name not in BLICK_VORGABEN:
            raise ValueError(f"unbekannte Blickvorgabe {name!r}; erlaubt: {tuple(BLICK_VORGABEN)}")
        self._vorgabe_name = name
        self._blick = BLICK_VORGABEN[name]
        return self._blick

    def zuruecksetzen(self) -> Blick:
        """Zurück zur gewählten Vorgabe samt Zoom (Pos1, Doppelklick)."""
        self._blick = BLICK_VORGABEN[self._vorgabe_name]
        return self._blick

    def drehen_pixel(self, dx_px: float, dy_px: float) -> Blick:
        """Drehen mit der Maus: Azimut += k·dx, Elevation -= k·dy, Elevation auf ±90° begrenzt."""
        return self._drehe(GRAD_JE_PIXEL * dx_px, -GRAD_JE_PIXEL * dy_px)

    def drehen_grad(self, d_azim_grad: float, d_elev_grad: float) -> Blick:
        """Drehen um Winkel (Tastatur: Umschalt+Pfeil bzw. ↑/↓)."""
        return self._drehe(d_azim_grad, d_elev_grad)

    def _drehe(self, d_azim: float, d_elev: float) -> Blick:
        if not (math.isfinite(d_azim) and math.isfinite(d_elev)):
            raise ValueError("Drehung muss endlich sein")
        azim = _normiere_azimut(self._blick.azim_grad + d_azim)
        elev = min(max(self._blick.elev_grad + d_elev, -90.0), 90.0)
        self._blick = replace(self._blick, azim_grad=azim, elev_grad=elev)
        return self._blick

    def zoomen(self, rasten: float) -> Blick:
        """Zoom um ``rasten`` Rastschritte (Mausrad); Faktor 1,1 je Raste, 0,4 bis 6."""
        if not math.isfinite(rasten):
            raise ValueError("rasten muss endlich sein")
        zoom = min(max(self._blick.zoom * _ZOOM_RASTE**rasten, ZOOM_MIN), ZOOM_MAX)
        self._blick = replace(self._blick, zoom=zoom)
        return self._blick


# --- Tasten -----------------------------------------------------------------------------------


class Aktion(Enum):
    """Aktionen der Tastatursteuerung."""

    ABSPIELEN = "abspielen"
    PHASE_ZURUECK = "phase_zurueck"
    PHASE_VOR = "phase_vor"
    PHASE_ZURUECK_GROB = "phase_zurueck_grob"
    PHASE_VOR_GROB = "phase_vor_grob"
    ELEVATION_PLUS = "elevation_plus"
    ELEVATION_MINUS = "elevation_minus"
    AZIMUT_PLUS = "azimut_plus"
    AZIMUT_MINUS = "azimut_minus"
    ZOOM_PLUS = "zoom_plus"
    ZOOM_MINUS = "zoom_minus"
    ANSICHT_ZURUECK = "ansicht_zurueck"


ANIMATIONS_TASTEN: Mapping[Aktion, tuple[str, str]] = {
    Aktion.ABSPIELEN: ("Space", "Leertaste"),
    Aktion.PHASE_ZURUECK: ("Left", "←"),
    Aktion.PHASE_VOR: ("Right", "→"),
    Aktion.PHASE_ZURUECK_GROB: ("Ctrl+Left", "Strg+←"),
    Aktion.PHASE_VOR_GROB: ("Ctrl+Right", "Strg+→"),
    Aktion.ELEVATION_PLUS: ("Up", "↑"),
    Aktion.ELEVATION_MINUS: ("Down", "↓"),
    Aktion.AZIMUT_MINUS: ("Shift+Left", "Umschalt+←"),
    Aktion.AZIMUT_PLUS: ("Shift+Right", "Umschalt+→"),
    Aktion.ZOOM_PLUS: ("+", "+"),
    Aktion.ZOOM_MINUS: ("-", "\N{MINUS SIGN}"),
    Aktion.ANSICHT_ZURUECK: ("Home", "Pos1"),
}
"""Aktion → ``(Qt-Tastenfolge, Anzeige im Tooltip)``, eine Quelle für Taste und Tooltip.

Die Belegung folgt Frage F-A3 des Plans: ←/→ ändern die Phase, Umschalt+←/→ und ↑/↓ drehen.
Für die Aufnahme in ``AKTIONS_TASTEN`` (``gui/anzeige_aktionen.py``) beim Einbau in die
Oberfläche (AN6/AN7) steht die Tabelle in derselben Form bereit."""

_TASTEN_OHNE_MODIFIKATOR: Mapping[str, Aktion] = {
    "Space": Aktion.ABSPIELEN,
    "Left": Aktion.PHASE_ZURUECK,
    "Right": Aktion.PHASE_VOR,
    "Up": Aktion.ELEVATION_PLUS,
    "Down": Aktion.ELEVATION_MINUS,
    "+": Aktion.ZOOM_PLUS,
    "-": Aktion.ZOOM_MINUS,
    "Home": Aktion.ANSICHT_ZURUECK,
}
_TASTEN_UMSCHALT: Mapping[str, Aktion] = {
    "Left": Aktion.AZIMUT_MINUS,
    "Right": Aktion.AZIMUT_PLUS,
}
_TASTEN_STRG: Mapping[str, Aktion] = {
    "Left": Aktion.PHASE_ZURUECK_GROB,
    "Right": Aktion.PHASE_VOR_GROB,
}


def taste_zu_aktion(
    taste: str,
    modifikatoren: frozenset[str] = frozenset(),
    *,
    fokus: bool = True,
    modus_animation: bool = True,
) -> Aktion | None:
    """Bildet eine Taste auf eine Aktion ab (UI-32).

    Parameters
    ----------
    taste : str
        Name der Taste: ``"Space"``, ``"Left"``, ``"Right"``, ``"Up"``, ``"Down"``, ``"+"``,
        ``"-"``, ``"Home"``.
    modifikatoren : frozenset of str
        Gedrückte Modifikatoren: ``"shift"``, ``"ctrl"`` (andere ergeben keine Aktion).
    fokus : bool
        Der Fokus liegt in der Animationsfläche bzw. der Animationsleiste.
    modus_animation : bool
        Der Modus Animation ist aktiv.

    Returns
    -------
    Aktion or None
        ``None`` ohne Fokus, außerhalb des Modus Animation und für nicht belegte Tasten.
    """
    if not (fokus and modus_animation):
        return None
    if not modifikatoren:
        return _TASTEN_OHNE_MODIFIKATOR.get(taste)
    if modifikatoren == frozenset({"shift"}):
        return _TASTEN_UMSCHALT.get(taste)
    if modifikatoren == frozenset({"ctrl"}):
        return _TASTEN_STRG.get(taste)
    return None


def wende_an(aktion: Aktion, uhr: Phasenuhr, blick: Blickzustand) -> None:
    """Führt eine Aktion auf Phasenuhr und Blick aus.

    Pos1 setzt Blick und Zoom zurück, **nicht** Winkel und Überhöhung.
    """
    if aktion is Aktion.ABSPIELEN:
        uhr.umschalten()
    elif aktion is Aktion.PHASE_ZURUECK:
        uhr.schritt(-1)
    elif aktion is Aktion.PHASE_VOR:
        uhr.schritt(+1)
    elif aktion is Aktion.PHASE_ZURUECK_GROB:
        uhr.schritt(-1, _PHASE_GROB_GRAD)
    elif aktion is Aktion.PHASE_VOR_GROB:
        uhr.schritt(+1, _PHASE_GROB_GRAD)
    elif aktion is Aktion.ELEVATION_PLUS:
        blick.drehen_grad(0.0, +DREH_SCHRITT_GRAD)
    elif aktion is Aktion.ELEVATION_MINUS:
        blick.drehen_grad(0.0, -DREH_SCHRITT_GRAD)
    elif aktion is Aktion.AZIMUT_PLUS:
        blick.drehen_grad(+DREH_SCHRITT_GRAD, 0.0)
    elif aktion is Aktion.AZIMUT_MINUS:
        blick.drehen_grad(-DREH_SCHRITT_GRAD, 0.0)
    elif aktion is Aktion.ZOOM_PLUS:
        blick.zoomen(+1.0)
    elif aktion is Aktion.ZOOM_MINUS:
        blick.zoomen(-1.0)
    else:
        blick.zuruecksetzen()


# --- Zustände und Texte -----------------------------------------------------------------------


def frequenzwechsel(uhr: Phasenuhr) -> str:
    """Zustand nach einem Frequenzwechsel (F-A4): Wiedergabe aus, Winkel 0, Modus „Standbild“.

    Returns
    -------
    str
        Neuer Modus, immer ``"standbild"``. Die Animation startet nie ohne Nutzeraktion (UI-22);
        ein neues Linienbild hat andere Phasen, Wiedergabe und Winkel gälten nicht weiter.
    """
    uhr.zuruecksetzen()
    return "standbild"


def phase_text(theta_rad: float, stil: Plotstil | None = None) -> str:
    """Anzeige des Winkels „θ = 90,0°“ auf ``[0°, 360°)`` mit Dezimalkomma (UI-24)."""
    komma = True if stil is None else stil.dezimalkomma
    grad = round(math.degrees(_normiere(theta_rad)), 1)
    if grad >= 360.0:
        grad = 0.0
    return f"θ = {zahl_text(grad + 0.0, 1, dezimalkomma=komma)}°"


def ueberhoehung_text(ueberhoehung: float, stil: Plotstil | None = None) -> str:
    """Anzeige des Überhöhungsfaktors mit 4 signifikanten Stellen, z. B. mit Malzeichen „4555“."""
    komma = True if stil is None else stil.dezimalkomma
    return f"\N{MULTIPLICATION SIGN}{zahl_kurz_text(ueberhoehung, 4, dezimalkomma=komma)}"


def skalierung_text(daten: AnimationsDaten, skalierung: float, stil: Plotstil | None = None) -> str:
    r"""Anzeige der Skalierung für Eingabefeld und Beschriftung (Nachtrag 2 3.2).

    Auslenkung: Malzeichen und Überhöhung :math:`s` („4555“). Schnelle: Skalierung
    :math:`\kappa` in s mit der äquivalenten Überhöhung :math:`s_\ddot{a} = \kappa\omega` daneben
    („7,250 s (entspricht Überhöhung 4555)“, jeweils mit Malzeichen); nur lesend.
    """
    komma = True if stil is None else stil.dezimalkomma
    if daten.groesse != "schnelle":
        return ueberhoehung_text(skalierung, stil)
    kappa = zahl_kurz_text(skalierung, 4, dezimalkomma=komma)
    aequiv = ueberhoehung_text(daten.ueberhoehung_aequivalent(skalierung), stil)
    return f"{kappa} s (entspricht Überhöhung {aequiv})"


def skalierung_nach_groessenwechsel(
    alt: AnimationsDaten, neu: AnimationsDaten, skalierung: float | None
) -> float | None:
    r"""Skalierung nach einem Wechsel Auslenkung ↔ Schnelle: die **Bildgröße bleibt erhalten**.

    Die äquivalente Überhöhung :math:`s_\ddot{a}` der alten Daten gilt weiter, die neue
    Skalierung ist :math:`s = s_\ddot{a}` (Auslenkung) bzw. :math:`\kappa = s_\ddot{a}/\omega`
    (Schnelle); ein manueller Wert springt so nicht auf eine andere Bildgröße (FG-04 Nachtrag 2,
    ANN S-1, F-S1). Der automatische Wert (``None``) bleibt automatisch: die Voreinstellung
    beider Größen hat dieselbe Bildgröße.

    Returns
    -------
    float or None
        Neue Skalierung; ``None``, wenn ``skalierung`` ``None`` war oder :math:`\omega` nicht
        positiv ist (dann kann die Überhöhung nicht umgerechnet werden; zurück auf automatisch).
    """
    if skalierung is None:
        return None
    s_aequiv = alt.ueberhoehung_aequivalent(skalierung)
    wert = neu.skalierung_aus_ueberhoehung(s_aequiv)
    return wert if math.isfinite(wert) else None


def beschreibung_animation(
    daten: AnimationsDaten,
    theta_rad: float,
    ueberhoehung: float | None,
    stil: Plotstil,
    *,
    laeuft: bool = False,
) -> str:
    r"""Textalternative der Animation (zugängliche Beschreibung, UI-26).

    Nennt die Pflichtangaben (Überhöhung bzw. Skalierung, Spitzenauslenkung bzw. -schnelle,
    Frequenz, Winkel, Bezug, Bedeutung von θ = 0), die Zahl der Punkte und die Zahl der
    stehenden gekennzeichneten Punkte.

    Parameters
    ----------
    daten : AnimationsDaten
        Daten der Animation.
    theta_rad : float
        Aktueller Winkel.
    ueberhoehung : float or None
        Skalierung (Auslenkung: :math:`s`; Schnelle: :math:`\kappa` in s); ``None`` = automatisch.
    stil : Plotstil
        Für Dezimalkomma.
    laeuft : bool
        Wiedergabe aktiv.
    """
    s = effektive_ueberhoehung(daten, AnimationsOptionen(ueberhoehung=ueberhoehung))
    kein_nachbar = ohne_nachbarabstand(daten, ueberhoehung)
    texte = tuple(
        t.replace("\n", ". ")
        for t in pflichttexte(daten, theta_rad, s, stil, kein_nachbarabstand=kein_nachbar)
    )
    gekennzeichnet = daten.anzahl_punkte - int(daten.bewegt.sum())
    zustand = "Wiedergabe läuft" if laeuft else "Standbild"
    teile = [
        "Animation der Betriebsschwingform",
        *texte,
        f"{daten.anzahl_punkte} Messpunkte",
    ]
    if gekennzeichnet:
        teile.append(f"davon {gekennzeichnet} stehend und gekennzeichnet")
    teile.append(zustand)
    return ". ".join(teile) + "."
