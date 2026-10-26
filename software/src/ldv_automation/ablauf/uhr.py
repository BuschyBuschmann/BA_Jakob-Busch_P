"""Injizierbare Uhr für die Ablaufsteuerung (Plan P2, Abschnitt 1).

Die Steuerung liest Zeit nur über :class:`Uhr`. Im Betrieb ist das :class:`Echtzeituhr`,
in Tests :class:`Testuhr`, deren ``sleep`` die Zeit sofort vorstellt. So laufen Zeitlimits,
Polling und Fortschrittsschätzung ohne echtes Warten.
"""

from __future__ import annotations

import math
import time
from datetime import datetime, timedelta, timezone
from typing import Protocol, runtime_checkable


@runtime_checkable
class Uhr(Protocol):
    """Zeitquelle der Ablaufsteuerung."""

    def monotonic(self) -> float:
        """Monotone Zeit in s (Nullpunkt beliebig, nur Differenzen sind sinnvoll)."""
        ...

    def sleep(self, dauer_s: float) -> None:
        """Wartet ``dauer_s`` Sekunden."""
        ...

    def jetzt(self) -> datetime:
        """Aktuelle Uhrzeit, zeitzonenbehaftet (für Protokolle und Ordnernamen)."""
        ...


class Echtzeituhr:
    """Uhr des Betriebs: ``time.monotonic``, ``time.sleep`` und lokale Zeit mit Zone."""

    def monotonic(self) -> float:
        """Monotone Zeit in s."""
        return time.monotonic()

    def sleep(self, dauer_s: float) -> None:
        """Wartet ``dauer_s`` Sekunden (negative Werte werden wie 0 behandelt)."""
        time.sleep(max(dauer_s, 0.0))

    def jetzt(self) -> datetime:
        """Lokale Uhrzeit mit Zeitzone."""
        return datetime.now().astimezone()


TESTUHR_START = datetime(2026, 11, 2, 9, 0, 0, tzinfo=timezone(timedelta(hours=1)))
"""Startzeitpunkt der Testuhr (fest, damit Ordnernamen in Tests vorhersagbar sind)."""


class Testuhr:
    """Deterministische Uhr für Tests: ``sleep`` stellt die Zeit sofort vor.

    Parameters
    ----------
    start : datetime
        Wanduhrzeit bei ``monotonic() == 0``; muss zeitzonenbehaftet sein.

    Raises
    ------
    ValueError
        Bei zeitzonenloser Startzeit.
    """

    __test__ = False  # Name beginnt mit "Test": pytest soll die Klasse nicht sammeln.

    def __init__(self, start: datetime = TESTUHR_START) -> None:
        if start.tzinfo is None:
            raise ValueError("Testuhr: Startzeit muss zeitzonenbehaftet sein")
        self._start = start
        self._t_s = 0.0

    def monotonic(self) -> float:
        """Bisher vergangene Testzeit in s."""
        return self._t_s

    def sleep(self, dauer_s: float) -> None:
        """Stellt die Zeit um ``dauer_s`` vor (ohne zu warten)."""
        self.vorstellen(max(dauer_s, 0.0))

    def vorstellen(self, dauer_s: float) -> None:
        """Stellt die Zeit um ``dauer_s`` ≥ 0 vor.

        Raises
        ------
        ValueError
            Bei negativer oder nicht endlicher Dauer.
        """
        if not math.isfinite(dauer_s) or dauer_s < 0:
            raise ValueError(f"Testuhr: Dauer muss endlich und ≥ 0 sein, erhalten {dauer_s!r}")
        self._t_s += dauer_s

    def jetzt(self) -> datetime:
        """Startzeit plus vergangene Testzeit."""
        return self._start + timedelta(seconds=self._t_s)
