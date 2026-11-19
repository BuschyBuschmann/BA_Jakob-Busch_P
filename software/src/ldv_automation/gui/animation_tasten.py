"""Tastenereignis → Aktion der Animation (UI-32), gemeinsam für Animationsfläche und AH.

Die Animationsfläche und die Regler der Bedienleiste AH setzen Tastenereignisse über dieselbe
Abbildung in :class:`~ldv_automation.gui.animation_steuerung.Aktion` um (Plan 5.2: mit Fokus in
AH gelten dieselben Tasten wie in der Fläche).
"""

from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtGui import QKeyEvent

from ldv_automation.gui.animation_steuerung import Aktion, taste_zu_aktion

__all__ = ["aktion_aus_tastenereignis"]

_ZEICHEN_NAMEN: dict[int, str] = {
    int(Qt.Key.Key_Space): "Space",
    int(Qt.Key.Key_Left): "Left",
    int(Qt.Key.Key_Right): "Right",
    int(Qt.Key.Key_Up): "Up",
    int(Qt.Key.Key_Down): "Down",
    int(Qt.Key.Key_Plus): "+",
    int(Qt.Key.Key_Minus): "-",
    int(Qt.Key.Key_Home): "Home",
}
_PLUS_MINUS = frozenset({int(Qt.Key.Key_Plus), int(Qt.Key.Key_Minus)})


def _modifikatoren(ereignis: QKeyEvent) -> frozenset[str]:
    """Gedrückte Modifikatoren als Namen für ``taste_zu_aktion`` (Ziffernblock-Flag entfällt)."""
    mods = ereignis.modifiers()
    namen: set[str] = set()
    if mods & Qt.KeyboardModifier.ShiftModifier:
        namen.add("shift")
    if mods & Qt.KeyboardModifier.ControlModifier:
        namen.add("ctrl")
    if mods & Qt.KeyboardModifier.AltModifier:
        namen.add("alt")
    if mods & Qt.KeyboardModifier.MetaModifier:
        namen.add("meta")
    if ereignis.key() in _PLUS_MINUS:
        namen.discard("shift")  # „+“ liegt je nach Tastaturbelegung auf Umschalt
    return frozenset(namen)


def aktion_aus_tastenereignis(ereignis: QKeyEvent) -> Aktion | None:
    """Aktion der Animation zu einem Tastenereignis (``None`` = nicht belegt).

    Parameters
    ----------
    ereignis : QKeyEvent
        Tastendruck mit Fokus in Animationsfläche bzw. AH im Modus „Animation“.
    """
    name = _ZEICHEN_NAMEN.get(ereignis.key())
    if name is None:
        return None
    return taste_zu_aktion(name, _modifikatoren(ereignis), fokus=True, modus_animation=True)
