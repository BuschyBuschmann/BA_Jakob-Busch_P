"""Eigene Spiegelung der benötigten Polytec-Enum-Werte (ADR-003, Late Binding).

Quelle aller Werte: Analysebericht I5, Abschnitt 8 (Enum-Themen der Polytec-Hilfe [BEM]).
Am Messrechner werden sie mit dem Erkundungswerkzeug gegen ``win32com.client.constants``
abgeglichen (Prüfpunkt P1-4). Bis dahin gelten sie als **[ungeprüft am Gerät]**.
"""

from __future__ import annotations

from enum import IntEnum, IntFlag


class AcqState(IntEnum):
    """``PTCAcqState`` ([BEM] PSV~PTCAcqState)."""

    STOPPED = 0
    SINGLE = 1
    CONTINUOUS = 2
    SCAN_ALL = 3
    SCAN_CONTINUE = 4
    SCAN_REMEASURE = 5
    AUTO_FOCUS = 6
    PATH_LENGTH = 7


SCAN_ZUSTAENDE = frozenset({AcqState.SCAN_ALL, AcqState.SCAN_CONTINUE, AcqState.SCAN_REMEASURE})
"""Zustände, die als „Scan läuft“ gelten."""


class ScanMode(IntEnum):
    """``PTCScanMode`` ([BEM] PSV~PTCScanMode). Freigegeben ist nur ``ALL``."""

    ALL = 0
    CONTINUE = 1
    REMEASURE = 2
    REMEASURE_AUTO_RANGE = 3
    REMEASURE_FILE = 4


class ScanCaps(IntFlag):
    """``PTCScanCaps`` (Bitmaske, [BEM] PSV~PTCScanCaps). Freigegeben ist nur ``NONE``."""

    NONE = 0
    USE_ASSIGNED_FOCUS_VALUES_DURING_SCAN = 1
    VIDEO_TRIANGULATION = 2
    VIDEO_TRIANGULATION_FAST = 4
    AUTO_FOCUS_DURING_SCAN = 8
    ASYNCHRONOUS_SCAN_EVENT = 16


class SettingsMask(IntFlag):
    """``PTCSettings`` (Bitmaske für ``Settings.Load``, [BEM] PSV~PTCSettings)."""

    NONE = 0
    ACQUISITION = 2
    ALIGNMENT = 4
    CAMERA = 64
    CAMERA_AND_ALIGNMENT = 68
    WINDOWS = 128
    APS = 312
    ALIGNMENT_2D = 512
    ALIGNMENT_3D = 1024
    ALL = 65535


class ApplicationMode(IntEnum):
    """``PTCApplicationMode`` ([BEM] PSV~PTCApplicationMode)."""

    NORMAL = 0
    ACQUISITION = 1
    PRESENTATION = 2


class AcqMode(IntEnum):
    """``PTCAcqMode`` ([BEM] POLYPROPERTIESLib~PTCAcqMode)."""

    TIME = 0
    FFT = 1
    ZOOM_FFT = 2
    MULTI_FRAME = 3
    FAST_SCAN = 4
    ORDER_TRACKING = 5
    IQ = 6
    INPLANE = 7


ACQ_MODE_NAMEN: dict[AcqMode, str] = {
    AcqMode.TIME: "Time",
    AcqMode.FFT: "Fft",
    AcqMode.ZOOM_FFT: "ZoomFft",
    AcqMode.MULTI_FRAME: "MultiFrame",
    AcqMode.FAST_SCAN: "FastScan",
    AcqMode.ORDER_TRACKING: "OrderTracking",
    AcqMode.IQ: "IQ",
    AcqMode.INPLANE: "Inplane",
}
"""Polytec-Schreibweise der Modi (``EinstellungsStand.modus`` erwartet ``"Fft"``)."""


class AverageType(IntEnum):
    """``PTCAverageType`` ([BEM] POLYPROPERTIESLib~PTCAverageType)."""

    OFF = 0
    MAGNITUDE = 1
    COMPLEX = 2
    TIME = 3
    PEAKHOLD = 4


AVERAGE_TYPE_NAMEN: dict[str, AverageType] = {
    "Off": AverageType.OFF,
    "Magnitude": AverageType.MAGNITUDE,
    "Complex": AverageType.COMPLEX,
    "Time": AverageType.TIME,
    "Peakhold": AverageType.PEAKHOLD,
}
"""Katalogwerte von ``mittelung.typ`` (Namen nach ``PTCAverageType``) → Enum."""


class WarningLevel(IntEnum):
    """``PTCWarningLevel`` ([BEM] PSV~PTCWarningLevel)."""

    ALL = 0
    WARNINGS = 1
    ERRORS = 2
    NONE = 3


_LADEMASKE_NAMEN: tuple[tuple[SettingsMask, str], ...] = (
    (SettingsMask.ACQUISITION, "Acquisition"),
    (SettingsMask.ALIGNMENT, "Alignment"),
    (SettingsMask.CAMERA, "Camera"),
    (SettingsMask.WINDOWS, "Windows"),
    (SettingsMask.APS, "APS"),
    (SettingsMask.ALIGNMENT_2D, "2DAlignment"),
    (SettingsMask.ALIGNMENT_3D, "3DAlignment"),
)


def lademaske_text(maske: int) -> str:
    """``PTCSettings``-Maske als Namen, getrennt durch ``"|"`` (für das Messprotokoll).

    ``All`` (65535) heißt ``"All"``; nicht benannte Restbits erscheinen als Zahl.
    """
    if maske == SettingsMask.ALL:
        return "All"
    namen: list[str] = []
    rest = maske
    for wert, name in _LADEMASKE_NAMEN:
        if maske & wert == wert:
            namen.append(name)
            rest &= ~int(wert)
    if rest:
        namen.append(str(rest))
    return "|".join(namen) if namen else "None"
