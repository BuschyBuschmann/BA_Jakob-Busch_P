"""Erkundungsskript für den PSV-Messrechner (nur lesend).

Zweck
-----
Das Skript sammelt auf dem Messrechner Fakten, die für den Entwurf des COM-Adapters
nötig sind (Registry, Bitness, Python/pywin32, PSV-Zustand, Hardware, Messpunkte,
Dateiformat). Es **misst nicht**, schaltet keinen Laser, ändert keine Einstellungen und
überschreibt keine Datei. Es beendet PSV nie und startet PSV nur mit ``--start-psv`` nach
ausdrücklicher Bestätigung.

Stufen (jede höhere Stufe führt die niedrigeren mit aus)
--------------------------------------------------------
``0``
    Nur Standardbibliothek, kein COM: Windows/Python-Version und Bitness, Registry
    (nur Lesen), Dateiversionen, Verzeichnislisten, Prozessliste.
``1``
    COM, nur lesend; erfordert laufendes PSV im Erfassungsmodus: Verbinden, Version,
    Zustand, Eigenschaften-Gruppen, Hardware, Messpunkte, Abgleich.
``1b``
    Optional mit ``--datei``: eine vorhandene Messdatei wird mit ``ReadOnly = True`` über
    Polytec File Access geöffnet und nur gelesen.

Sicherheitsprinzip
------------------
Stufe 1 legt ``PSV.AcquisitionInstance`` nur an, wenn Stufe 0 einen laufenden PSV-Prozess
gefunden hat (oder ``--start-psv`` bestätigt wurde): COM könnte beim Anlegen einer als
Server registrierten EXE diese sonst selbst starten.
Jeder COM-Zugriff läuft über :class:`WhitelistProxy` (Default deny): Nur Mitglieder, die in
:data:`POLICY` stehen, werden weitergereicht. Alles andere löst ``PermissionError`` aus und
landet im Bericht unter ``verweigert``. :data:`BLACKLIST` ist nur ein Testkatalog.

Quellen
-------
Abschnittsnummern verweisen auf die COM-Referenz I5 (``in_progress/analysen``): 1.3 ProgIDs,
1.7 Index/Label, 2.5/2.6 Eigenschaften und Validatoren, 2.7/2.8 Abgleich und Hardware, 3.1
Verbinden, 4.2-4.4 Datei und Frequenzachse, 5.4 Timeouts, 8 Enum-Werte, 10 Prüfliste.
Belegkürzel: [BEM] Basic Engine Manual, [PFA] Polytec File Access.

Ausgabe
-------
Ein neuer Ordner ``erkundung_<Rechnername>_<JJJJ-MM-TT_HHMMSS>`` (nie überschrieben) mit
``bericht.json`` (Schema siehe README.md), ``zusammenfassung.md``, ``konsole.log``,
``registry.reg.txt`` und ``typelibs.txt``. Keine Messdaten, keine Binärdaten.

Voraussetzung: Python 3.11 (Projektvorgabe). Ältere Versionen werden gleich zu Beginn mit einem
Hinweis abgewiesen (Syntax bewusst so gehalten, dass die Datei bis dahin parsebar ist).
Das Skript hängt nicht vom Hauptpaket ab und lässt sich als Einzeldatei kopieren.
Nur die Adapterfunktionen am Ende importieren ``winreg``, ``ctypes`` und ``win32com``.

Exit-Codes: 0 normal, 1 Zugriff verweigert (Befund zur Whitelist), 2 Aufruffehler oder
Python zu alt, 3 blockiert (Teilbericht geschrieben), 4 interner Fehler außerhalb eines
Prüfpunkts (z. B. Schreibfehler; Teilbericht soweit möglich), 130 Abbruch mit Strg+C.
"""

from __future__ import annotations

import sys

MIN_PYTHON = (3, 11)


def _require_python(version_info: tuple[int, ...] = tuple(sys.version_info[:3])) -> None:
    """Bricht vor jeder Ausgabe mit klarem Hinweis ab, wenn Python zu alt ist."""
    if tuple(version_info[:2]) < MIN_PYTHON:
        sys.stderr.write(
            "erkundung.py braucht Python 3.11 oder neuer (gefunden: "
            + ".".join(str(v) for v in version_info[:3])
            + "). Es wurde nichts angelegt und nichts gelesen.\n"
        )
        raise SystemExit(2)


_require_python()

import argparse
import contextlib
import csv
import datetime as dt
import gc
import hashlib
import importlib
import importlib.metadata
import io
import json
import math
import os
import platform
import re
import struct
import subprocess
import sys
import threading
import time
import traceback
from collections.abc import Callable, Mapping, Sequence
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Protocol, TypeGuard

SCRIPT_VERSION = "0.1.0"
SCHEMA_VERSION = 1

EXIT_OK = 0
EXIT_DENIED = 1
EXIT_BLOCKED = 3
EXIT_ERROR = 4
EXIT_INTERRUPTED = 130

DEFAULT_TIMEOUT_S = 60.0  # Annahme des Umsetzers: Plan nennt nur "Parameter", keinen Wert.
DEFAULT_MAX_POINTS = 3  # Messpunkte vorn und hinten (Plan: "wenige", Anzahl ist Parameter)
DEFAULT_MAX_VALUES = 6  # Datenwerte aus GetData (Plan: "die ersten wenigen")
START_TIMEOUT_MS = 30000  # GetApplication(True, ...) nur mit --start-psv; Wert aus I5 10 (P1-5)
MAX_DIR_ENTRIES = 200
MAX_VIBROMETERS = 4
MAX_CONTROLLERS = 3
MAX_SENSORHEADS = 2
WRITE_RETRIES = 5
WRITE_RETRY_WAIT_S = 0.05
MAX_ALIGNMENTS = 3
MAX_DOMAINS = 6
MAX_CHANNELS = 8
MAX_SIGNALS = 6
MAX_DISPLAYS = 8
PSV_ACQUISITION_STOPPED = 0  # PTCAcqState.Stopped, I5 8

# fmt: off
PROGIDS: tuple[str, ...] = (
    "PSV.AcquisitionInstance", "PSV.PresentationInstance", "PSV.Application",
    "PolyFile.PolyFile", "PolyWaveforms.WaveformSine",
)
# fmt: on
PROCESS_KEYWORDS: tuple[str, ...] = ("psv", "polytec", "vibsoft")
TYPELIB_KEYWORDS: tuple[str, ...] = ("poly", "psv", "vibsoft")

# Enum-Werte aus I5 Abschnitt 8 (aus den Enum-Themen der Polytec-Hilfe). Vergleich gegen
# win32com.client.constants, sofern ein gen_py-Cache existiert (das Skript erzeugt keinen).
# fmt: off
EXPECTED_CONSTANTS: dict[str, int] = {
    "ptcAcqStateAutoFocus": 6, "ptcAcqStateContinuous": 2, "ptcAcqStatePathLength": 7,
    "ptcAcqStateScanAll": 3, "ptcAcqStateScanContinue": 4, "ptcAcqStateScanRemeasure": 5,
    "ptcAcqStateSingle": 1, "ptcAcqStateStopped": 0, "ptcAcqStartContinuous": 1,
    "ptcAcqStartSingle": 0, "ptcScanAll": 0, "ptcScanContinue": 1, "ptcScanRemeasure": 2,
    "ptcScanRemeasureAutoRange": 3, "ptcScanRemeasureFile": 4,
    "ptcApplicationModeAcquisition": 1, "ptcApplicationModeNormal": 0,
    "ptcApplicationModePresentation": 2, "ptcWarningLevelAll": 0, "ptcWarningLevelErrors": 2,
    "ptcWarningLevelNone": 3, "ptcWarningLevelWarnings": 1,
    "ptcScanCapsAsynchronousScanEvent": 16, "ptcScanCapsAutoFocusDuringScan": 8,
    "ptcScanCapsNone": 0, "ptcScanCapsUseAssignedFocusValuesDuringScan": 1,
    "ptcScanCapsVideoTriangulation": 2, "ptcScanCapsVideoTriangulationFast": 4,
    "ptcAcqPropertiesTypeAverage": 1, "ptcAcqPropertiesTypeChannels": 2,
    "ptcAcqPropertiesTypeFastScans": 3, "ptcAcqPropertiesTypeFft": 4,
    "ptcAcqPropertiesTypeFrontEnd": 14, "ptcAcqPropertiesTypeGeneral": 0,
    "ptcAcqPropertiesTypeGenerators": 5, "ptcAcqPropertiesTypeMultiFrame": 6,
    "ptcAcqPropertiesTypeSignalEnhancement": 8, "ptcAcqPropertiesTypeTime": 9,
    "ptcAcqPropertiesTypeTrigger": 10, "ptcAcqPropertiesTypeVibrometers": 11,
    "ptcAcqPropertiesTypeZoomFft": 12, "ptcAverageComplex": 2, "ptcAverageMagnitude": 1,
    "ptcAverageOff": 0, "ptcAveragePeakhold": 4, "ptcAverageTime": 3, "ptcDomain3rdOctave": 4,
    "ptcDomainAngleSync": 2, "ptcDomainNotAvail": 0, "ptcDomainOrderSpectrum": 5,
    "ptcDomainRMS": 6, "ptcDomainSpectrum": 3, "ptcDomainTime": 1, "ptcDisplayImag": 8,
    "ptcDisplayInstVal": 11, "ptcDisplayIQFitted": 13, "ptcDisplayMag": 1, "ptcDisplayMagDb": 3,
    "ptcDisplayMagDbA": 5, "ptcDisplayMagDbPhase": 4, "ptcDisplayMagDbPhaseRad": 15,
    "ptcDisplayMagPhase": 2, "ptcDisplayMagPhaseRad": 14, "ptcDisplayNotAvail": 0,
    "ptcDisplayNyquist": 10, "ptcDisplayPhase": 6, "ptcDisplayReal": 7, "ptcDisplayRealImag": 9,
    "ptcDisplaySamples": 12,
}
# fmt: on


# ---------------------------------------------------------------------------------------
# Whitelist-Proxy (Default deny)
# ---------------------------------------------------------------------------------------


class ComUnavailableError(RuntimeError):
    """COM ist auf diesem Rechner nicht nutzbar (z. B. pywin32 fehlt oder kein Windows)."""


class Skipped(Exception):  # noqa: N818 - kein Fehler, sondern ein Steuerfluss-Signal
    """Ein Prüfpunkt wird mit Hinweis übersprungen (Voraussetzung nicht erfüllt)."""


class ProxyContext:
    """Gemeinsamer Zustand aller Proxys: Aufrufprotokoll, Verweigerungen, Startfreigabe."""

    def __init__(self, allow_start: bool = False) -> None:
        self.allow_start = allow_start
        self.current_step = ""
        self.pending: dict[str, Any] | None = None
        self._lock = threading.Lock()
        self._calls: list[dict[str, Any]] = []
        self._denied: list[dict[str, Any]] = []

    def record_call(
        self,
        kind: str,
        name: str,
        op: str,
        args: tuple[Any, ...],
        duration_s: float,
        error: str | None,
    ) -> None:
        """Protokolliert einen tatsächlich weitergereichten Zugriff."""
        with self._lock:
            self._calls.append(
                {
                    "nr": len(self._calls) + 1,
                    "pruefpunkt": self.current_step,
                    "pfad": f"{kind}.{name}",
                    "op": op,
                    "argumente": [_repr_arg(a) for a in args],
                    "dauer_s": round(duration_s, 6),
                    "fehler": error,
                }
            )

    def record_denied(self, kind: str, name: str, op: str, reason: str) -> None:
        """Protokolliert einen verweigerten Zugriffsversuch."""
        with self._lock:
            self._denied.append(
                {
                    "pruefpunkt": self.current_step,
                    "pfad": f"{kind}.{name}",
                    "op": op,
                    "grund": reason,
                }
            )

    def snapshot(self) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
        """Liefert Kopien von Aufrufprotokoll und Verweigerungen."""
        with self._lock:
            return list(self._calls), list(self._denied)


CheckFn = Callable[[tuple[Any, ...], ProxyContext], "str | None"]


@dataclass(frozen=True)
class Member:
    """Freigegebenes Mitglied eines COM-Objekttyps.

    Parameters
    ----------
    access
        ``"get"`` (Property lesen) oder ``"call"`` (Methode aufrufen).
    returns
        Typname (Schlüssel in :data:`POLICY`), falls ein Objekt zurückkommt; sonst ``None``
        (einfacher Wert).
    check
        Prüft die Argumente eines Aufrufs; liefert eine Fehlermeldung oder ``None``.
    """

    access: str
    returns: str | None = None
    check: CheckFn | None = None


def _is_int(value: Any) -> TypeGuard[int]:
    return isinstance(value, int) and not isinstance(value, bool)


def _chk_no_args(args: tuple[Any, ...], ctx: ProxyContext) -> str | None:
    return None if not args else "keine Argumente erlaubt"


def _chk_index(args: tuple[Any, ...], ctx: ProxyContext) -> str | None:
    if len(args) == 1 and _is_int(args[0]) and args[0] >= 1:
        return None
    return "erwartet genau einen 1-basierten Index (int >= 1)"


def _chk_laser(args: tuple[Any, ...], ctx: ProxyContext) -> str | None:
    if len(args) == 1 and _is_int(args[0]) and args[0] in (-1, 1, 2, 3):
        return None
    return "erwartet scanHeadIndex in (-1, 1, 2, 3)"


def _chk_get_application(args: tuple[Any, ...], ctx: ProxyContext) -> str | None:
    if not 1 <= len(args) <= 2 or not isinstance(args[0], bool):
        return "erwartet (vbCreate: bool[, lTimeOut: int])"
    if len(args) == 2 and not _is_int(args[1]):
        return "lTimeOut muss int sein"
    if args[0] and not ctx.allow_start:
        return "Start von PSV (vbCreate=True) ist nicht freigegeben (--start-psv)"
    return None


def _chk_label(args: tuple[Any, ...], ctx: ProxyContext) -> str | None:
    if len(args) == 1 and (_is_int(args[0]) or isinstance(args[0], str)):
        return None
    return "erwartet genau ein Label (int oder str)"


def _chk_path(args: tuple[Any, ...], ctx: ProxyContext) -> str | None:
    if len(args) == 1 and isinstance(args[0], str) and args[0]:
        return None
    return "erwartet genau einen Dateipfad (str)"


def _is_display(arg: Any) -> bool:
    return isinstance(arg, WhitelistProxy) and arg.kind == "Display"


def _chk_display(args: tuple[Any, ...], ctx: ProxyContext) -> str | None:
    if len(args) == 1 and _is_display(args[0]):
        return None
    return "erwartet genau ein Display-Objekt"


def _chk_display_frame(args: tuple[Any, ...], ctx: ProxyContext) -> str | None:
    if len(args) == 2 and _is_display(args[0]) and _is_int(args[1]) and args[1] >= 0:
        return None
    return "erwartet (Display, Frame: int >= 0)"


def _chk_nonneg_int(args: tuple[Any, ...], ctx: ProxyContext) -> str | None:
    if len(args) == 1 and _is_int(args[0]) and args[0] >= 0:
        return None
    return "erwartet genau einen Index (int >= 0)"


def _values(*names: str) -> dict[str, Member]:
    return {name: Member("get") for name in names}


def _obj(kind: str) -> Member:
    return Member("get", kind)


def _item(kind: str) -> Member:
    return Member("call", kind, _chk_index)


def _item0(kind: str) -> Member:
    return Member("call", kind, _chk_nonneg_int)


# Namen aus [BEM]; Zuordnung und Belege siehe Plan E1, Abschnitt 2.
# fmt: off
APP_PROPS = (
    "Version", "Mode", "Visible", "WarningLevel", "SuppressMessagesForAutomation",
    "MessagesLoggingEnabled",
)
# fmt: on
ACQ_PROPS = ("State", "Mode", "ScanCaps", "GeneratorsOn", "ScanFileName")
# fmt: off
HAS_PROPS = (
    "HasGeneralProperties", "HasAverageProperties", "HasFftProperties", "HasTimeProperties",
    "HasZoomFftProperties", "HasChannelsProperties", "HasVibrometersProperties",
    "HasGeneratorsProperties", "HasTriggerProperties", "HasSignalEnhancementProperties",
    "HasFrontEndProperties", "HasMultiFrameProperties", "HasFastScansProperties",
)
# fmt: on
# fmt: off
FFT_PROPS = (
    "Bandwidth", "StartFrequency", "EndFrequency", "Lines", "SampleResolution", "Overlap",
    "SampleFrequency", "SampleTime",
)
# fmt: on
AVG_PROPS = ("Type", "Count")
# fmt: off
GENERAL_PROPS = (
    "AutoRemeasure", "AutoRemeasureAutoRange", "BandWidthExtension", "IsAutoRemeasurePossible",
    "PrincipalComponentAnalysis", "RealSampleFrequency", "SaveTimeDataForScan",
)
# fmt: on
# fmt: off
HARDWARE_PROPS = (
    "AcqBoardName", "AcqBoardFirmwareVersion", "AcqBoardChannelCount", "FrontEnd",
    "FrontEndFirmwareVersion", "GeneratorName", "GeneratorType", "GeneratorFirmwareVersion",
    "ScanHeadType", "SensorHeadNames", "SensorHeadSerialNumbers", "SensorHeadVersions",
    "CoherenceOptimizerVersions",
)
# fmt: on
# fmt: off
INFOS_HAS = (
    "HasHardware", "HasScanHeadDevicesInfo", "HasAlignments", "HasMeasPoints",
    "HasPositionDevice", "HasVibrometers",
)
# fmt: on
SCANHEAD_PROPS = ("ScanHeadName", "ScanHeadType")
SENSORHEAD_PROPS = ("Name", "SerialNumber", "FirmwareVersion", "LaserWavelength", "LaserPower")
CONTROLLER_PROPS = ("DeviceName", "FirmwareVersion", "Name", "SerialNumber")
MEASPOINT_PROPS = ("Index", "Label", "ScanStatus", "AverageCount", "Sigma")
ALIGN3D_PROPS = (
    "Valid",
    "CurrentQuality",
    "TargetQuality",
    "PositionUncertainty",
    "AngleUncertainty",
)
# fmt: off
FILE_VERSION_PROPS = (
    "FileID", "FileTime", "FileVersion", "ProgramID", "ProgramVersion", "ProgramVersionString",
    "ProgramVersionMajor", "ProgramVersionMinor", "ProgramVersionRevision",
    "ProgramVersionBuild",
)
# fmt: on
SUMMARY_PROPS = ("Title", "Author", "Subject", "Comments")
XAXIS_PROPS = ("Min", "Max", "MaxCount", "Name", "Unit")
YAXIS_PROPS = ("Name", "Unit", "Min", "Max")
SIGNAL_DESC_PROPS = ("DomainType", "FunctionType", "Complex", "Name")

# Typname -> Mitgliedsname -> Freigabe. Was hier fehlt, wird verweigert (Default deny).
POLICY: dict[str, dict[str, Member]] = {
    "AcquisitionInstance": {
        "IsRunning": Member("get"),
        "GetApplication": Member("call", "Application", _chk_get_application),
    },
    "Application": {**_values(*APP_PROPS), "Acquisition": _obj("Acquisition")},
    "Acquisition": {
        **_values(*ACQ_PROPS),
        "GetLaserOn": Member("call", None, _chk_laser),
        "ActiveProperties": _obj("AcquisitionProperties"),
        "Infos": _obj("Infos"),
    },
    "AcquisitionProperties": {
        **_values(*HAS_PROPS),
        "FftProperties": _obj("FftProperties"),
        "AverageProperties": _obj("AverageProperties"),
        "GeneralProperties": _obj("GeneralProperties"),
    },
    "FftProperties": _values(*FFT_PROPS),
    "AverageProperties": _values(*AVG_PROPS),
    "GeneralProperties": _values(*GENERAL_PROPS),
    "Infos": {
        **_values(*INFOS_HAS),
        "Hardware": _obj("Hardware"),
        "ScanHeadDevicesInfo": _obj("ScanHeadDevicesInfo"),
        "Vibrometers": _obj("Vibrometers"),
        "MeasPoints": _obj("MeasPoints"),
        "Alignments": _obj("Alignments"),
    },
    "Hardware": _values(*HARDWARE_PROPS),
    "ScanHeadDevicesInfo": _values(*SCANHEAD_PROPS),
    "Vibrometers": {"Count": Member("get"), "Item": _item("ControllerGroup")},
    "ControllerGroup": {
        "ControllerInfo": _obj("ControllerInfo"),
        "Controllers": _obj("Controllers"),
    },
    "ControllerInfo": _values(*CONTROLLER_PROPS),
    # [BEM] "Access to General Information": Vibrometers(1).Controllers(0).SensorHeads(0);
    # Controllers und SensorHeads sind 0-basiert (Vibrometers 1-basiert).
    "Controllers": {"Count": Member("get"), "Item": _item0("Controller")},
    "Controller": {"SensorHeads": _obj("SensorHeads")},
    "SensorHeads": {"Count": Member("get"), "Item": _item0("SensorHead")},
    "SensorHead": {"SensorHeadInfo": _obj("SensorHeadInfo")},
    "SensorHeadInfo": _values(*SENSORHEAD_PROPS),
    "MeasPoints": {
        "Count": Member("get"),
        "Item": _item("MeasPoint"),
        "LabelToIndex": Member("call", None, _chk_label),
    },
    "MeasPoint": {
        **_values(*MEASPOINT_PROPS),
        "CoordXYZ": Member("call", None, _chk_no_args),
    },
    "Alignments": {
        "Alignments3D": _obj("Alignments3D"),
        "Alignments2D": _obj("Alignments2D"),
    },
    "Alignments3D": {"Count": Member("get"), "Item": _item("Alignment3D")},
    "Alignment3D": _values(*ALIGN3D_PROPS),
    "Alignments2D": {"Count": Member("get"), "Item": _item("Alignment2D")},
    "Alignment2D": _values("Valid"),
    # Stufe 1b (PolyFile, nur lesen)
    "PolyFile": {
        "IsOpen": Member("get"),
        "Open": Member("call", None, _chk_path),
        "Close": Member("call", None, _chk_no_args),
        "Version": _obj("FileVersion"),
        "SummaryInfo": _obj("SummaryInfo"),
        "Infos": _obj("Infos"),
        "GetPointDomains": Member("call", "PointDomains", _chk_no_args),
    },
    "FileVersion": _values(*FILE_VERSION_PROPS),
    "SummaryInfo": _values(*SUMMARY_PROPS),
    "PointDomains": {"Count": Member("get"), "Item": _item("PointDomain")},
    "PointDomain": {
        **_values("Name", "Type"),
        "Channels": _obj("Channels"),
        "DataPoints": _obj("DataPoints"),
        "GetXAxis": Member("call", "XAxis", _chk_display),
    },
    "DataPoints": {"Count": Member("get"), "Item": _item("DataPoint")},
    "DataPoint": {
        "AverageCount": Member("get"),
        "GetData": Member("call", None, _chk_display_frame),
    },
    "Channels": {"Count": Member("get"), "Item": _item("Channel")},
    "Channel": {"Name": Member("get"), "Signals": _obj("Signals")},
    "Signals": {"Count": Member("get"), "Item": _item("Signal")},
    "Signal": {
        "Name": Member("get"),
        "Description": _obj("SignalDescription"),
        "Displays": _obj("Displays"),
    },
    "Displays": {"Count": Member("get"), "Item": _item("Display")},
    "Display": _values("Name", "Type"),
    "SignalDescription": {**_values(*SIGNAL_DESC_PROPS), "YAxis": _obj("YAxis")},
    "YAxis": _values(*YAXIS_PROPS),
    "XAxis": {
        **_values(*XAXIS_PROPS),
        "GetMidX": Member("call", None, _chk_nonneg_int),
    },
}

# Erlaubte Schreibzugriffe: (Typ, Name) -> zulässige Werte (Vergleich mit ``is``).
# Einzige Schreiboperation: ReadOnly = True verhindert Schreiben in die Messdatei.
WRITES: dict[tuple[str, str], tuple[Any, ...]] = {("PolyFile", "ReadOnly"): (True,)}

# Reine Existenzprüfung über GetIDsOfNames, ohne das Mitglied zu lesen oder zu setzen.
EXISTS: dict[str, frozenset[str]] = {
    "FftProperties": frozenset({"FftAcqPropertiesValidator"}),
    "Application": frozenset({"DigitalPorts"}),
}

# Freigegebene Einstiegsobjekte (Dispatch). Alles andere wird verweigert.
ALLOWED_PROGIDS: dict[str, str] = {
    "PSV.AcquisitionInstance": "AcquisitionInstance",
    "PolyFile.PolyFile": "PolyFile",
}

_PRIMITIVES = (type(None), bool, int, float, str, bytes, dt.datetime, dt.date)


def _call_members(kind: str, *names: str) -> list[tuple[str, str, str, Any]]:
    return [(kind, name, "call", None) for name in names]


# Testkatalog (kein Schutzmechanismus): Jeder Eintrag muss verweigert werden.
# Eintrag: (Typ, Mitglied, Operation "get"/"call"/"set", Wert bei "set").
BLACKLIST: tuple[tuple[str, str, str, Any], ...] = (
    # Messung, Bewegung, Laser
    *_call_members(
        "Acquisition",
        "Start",
        "Stop",
        "Scan",
        "ScanEx",
        "SetLaserOn",
        "AutoFocusLaser",
        "AssignFocusAutomatically",
        "CalculateFocusValues",
        "GeometryScan",
        "SetSelectedMeasPoints",
        "GetData",
        "GetSignalAmplitudes",
        "TakeReferenceSnapshot",
        "FindPointMarkers",
        "MatchPointMarkers",
        "MeasurePathLength",
        "PathLengthScan",
        "TakeSnapshotAndGetPixelCoordinates",
        "ExportVideoSnapshot",
        "ExportVideoSnapshotEx",
    ),
    # Zuweisungen
    ("Acquisition", "Mode", "set", 1),
    ("Acquisition", "ScanFileName", "set", "x.svd"),
    ("Acquisition", "GeneratorsOn", "set", True),
    ("FftProperties", "Bandwidth", "set", 1.0),
    ("FftProperties", "Lines", "set", 1),
    ("AverageProperties", "Count", "set", 1),
    ("GeneralProperties", "SaveTimeDataForScan", "set", True),
    ("AcquisitionProperties", "FftProperties", "set", None),
    ("Application", "Mode", "set", 1),
    ("Application", "SuppressMessagesForAutomation", "set", True),
    ("Application", "WarningLevel", "set", 0),
    ("Application", "Visible", "set", False),
    ("MeasPoint", "Label", "set", 1),
    ("MeasPoint", "Index", "set", 1),
    # Dateien und Zustand
    ("Application", "Settings", "get", None),
    *_call_members("Settings", "Load", "Save", "Delete"),
    ("Application", "Documents", "get", None),
    *_call_members("Documents", "Open"),
    *_call_members("Document", "Save", "SaveAs", "Close"),
    *_call_members("Application", "Quit", "QuitEx"),
    ("Application", "Exporter", "get", None),
    *_call_members("Exporter", "Export"),
    ("ExportParameters", "FileName", "set", "x.uff"),
    *_call_members("ControllerSettings", "Save"),
    *_call_members("PolyFile", "Save", "SaveAs", "SaveAsEx", "Create", "CalcBands"),
    *_call_members("PolyFile", "CalcBandsFromSignal", "CorrectAverageSpectrum"),
    ("PolyFile", "ReadOnly", "set", False),
    ("PolyFile", "FileName", "set", "x.svd"),
    ("SummaryInfo", "Title", "set", "x"),
    *_call_members("SummaryInfo", "Save"),
    *_call_members("FileVersion", "Save"),
    *_call_members("Hardware", "Save"),
    *_call_members("MeasPoints", "Add", "AddPoints", "Clear", "Remove", "SetLabels", "Save"),
    *_call_members("MeasPoints", "Calculate3DCoordinates"),
    *_call_members("Infos", "Add"),
    *_call_members("MeasPoint", "SetCoordXYZ", "SetVideoXY", "ToggleValidInvalidated"),
    *_call_members("DataPoint", "SetData", "SetScanStatus"),
    # Hardware
    *_call_members("PositionDevice", "StartMove", "StartMoveRelative", "StartMoveAbsolute"),
    ("DigitalPort", "Value", "set", 1),
    *_call_members("DigitalPort", "Pulse"),
    *_call_members("Alignment3D", "Calculate", "Invalidate"),
    *_call_members(
        "ScanHeadControl",
        "WriteFocusDataFactorySettings",
        "WriteFocusDataFocalLength",
        "WriteFocusDataInfinitePos",
        "WriteLaserIntensityData",
        "WriteMirrorAdjustmentData",
    ),
    ("Waveform", "Amplitude", "set", 1.0),
)


def _repr_arg(arg: Any) -> str:
    if isinstance(arg, WhitelistProxy):
        return f"<{arg.kind}>"
    return repr(arg)[:120]


def _sanitize(value: Any) -> Any:
    """Lässt nur einfache Werte (und Tupel/Listen davon) durch; Objekte nie."""
    if isinstance(value, _PRIMITIVES):
        return value
    if isinstance(value, (tuple, list)):
        return tuple(_sanitize(item) for item in value)
    return f"<nicht erwarteter Rückgabetyp {type(value).__name__}>"


def _unwrap(value: Any) -> Any:
    return value._obj if isinstance(value, WhitelistProxy) else value


def _member_exists(obj: Any, name: str) -> bool:
    """Existenzprüfung ohne Lesezugriff (COM: GetIDsOfNames, sonst Typ-Introspektion)."""
    ole = getattr(obj, "_oleobj_", None)
    if ole is not None:
        try:
            ole.GetIDsOfNames(name)
        except Exception:
            return False
        return True
    return hasattr(type(obj), name)


class WhitelistProxy:
    """Reicht nur Mitglieder aus :data:`POLICY` an ein COM-Objekt weiter.

    Parameters
    ----------
    obj
        Das umhüllte COM-Objekt (wird nie nach außen gegeben).
    kind
        Typname in :data:`POLICY`.
    ctx
        Gemeinsamer Protokoll- und Freigabezustand.
    """

    __slots__ = ("_ctx", "_kind", "_obj")

    def __init__(self, obj: Any, kind: str, ctx: ProxyContext) -> None:
        object.__setattr__(self, "_obj", obj)
        object.__setattr__(self, "_kind", kind)
        object.__setattr__(self, "_ctx", ctx)

    @property
    def kind(self) -> str:
        """Typname des umhüllten Objekts."""
        return str(self._kind)

    def __repr__(self) -> str:
        return f"<WhitelistProxy {self._kind}>"

    def _deny(self, name: str, op: str, reason: str) -> PermissionError:
        self._ctx.record_denied(self._kind, name, op, reason)
        return PermissionError(f"verweigert (Default deny): {self._kind}.{name} [{op}]: {reason}")

    def _invoke(self, name: str, op: str, args: tuple[Any, ...], fn: Callable[[], Any]) -> Any:
        ctx: ProxyContext = self._ctx
        ctx.pending = {"pfad": f"{self._kind}.{name}", "op": op, "argumente": _repr_args(args)}
        start = time.perf_counter()
        try:
            result = fn()
        except Exception as exc:
            ctx.pending = None
            ctx.record_call(
                self._kind, name, op, args, time.perf_counter() - start, _short_error(exc)
            )
            raise
        ctx.pending = None
        ctx.record_call(self._kind, name, op, args, time.perf_counter() - start, None)
        return result

    def __getattr__(self, name: str) -> Any:
        if name.startswith("_"):
            raise self._deny(name, "get", "private/dunder Mitglieder sind nie freigegeben")
        member = POLICY.get(self._kind, {}).get(name)
        if member is None:
            raise self._deny(name, "get", "nicht in der Whitelist")
        obj = self._obj
        if member.access == "get":
            value = self._invoke(name, "get", (), lambda: getattr(obj, name))
            return self._finish(value, member.returns)

        def call(*args: Any) -> Any:
            problem = member.check(args, self._ctx) if member.check else None
            if problem is not None:
                raise self._deny(name, "call", problem)
            raw_args = tuple(_unwrap(a) for a in args)
            value = self._invoke(name, "call", args, lambda: getattr(obj, name)(*raw_args))
            return self._finish(value, member.returns)

        return call

    def _finish(self, value: Any, returns: str | None) -> Any:
        if returns is None:
            return _sanitize(value)
        if value is None:
            return None
        return WhitelistProxy(value, returns, self._ctx)

    def __setattr__(self, name: str, value: Any) -> None:
        allowed = WRITES.get((self._kind, name))
        if allowed is None:
            raise self._deny(name, "set", "Schreibzugriffe sind nicht freigegeben")
        if not any(value is ok for ok in allowed):
            raise self._deny(name, "set", f"Wert {value!r} ist nicht freigegeben")
        obj = self._obj
        self._invoke(name, "set", (value,), lambda: setattr(obj, name, value))

    def __delattr__(self, name: str) -> None:
        raise self._deny(name, "del", "Löschen ist nie freigegeben")

    def exists(self, name: str) -> bool:
        """Prüft nur die Existenz eines Mitglieds (ohne es zu lesen), falls freigegeben."""
        if name not in EXISTS.get(self._kind, frozenset()):
            raise self._deny(name, "exists", "Existenzprüfung nicht freigegeben")
        obj = self._obj
        return bool(self._invoke(name, "exists", (), lambda: _member_exists(obj, name)))


def _repr_args(args: tuple[Any, ...]) -> list[str]:
    return [_repr_arg(a) for a in args]


def _short_error(exc: BaseException) -> str:
    return f"{type(exc).__name__}: {exc}"[:300]


# ---------------------------------------------------------------------------------------
# Hilfsfunktionen (plattformunabhängig, voll getestet)
# ---------------------------------------------------------------------------------------


def to_jsonable(value: Any) -> Any:
    """Wandelt beliebige Werte in streng gültiges JSON (NaN/Inf und Objekte als Text)."""
    if value is None or isinstance(value, (bool, int, str)):
        return value
    if isinstance(value, float):
        return value if math.isfinite(value) else repr(value)
    if isinstance(value, Mapping):
        return {str(k): to_jsonable(v) for k, v in value.items()}
    if isinstance(value, (list, tuple, set, frozenset)):
        return [to_jsonable(v) for v in value]
    if isinstance(value, (dt.datetime, dt.date)):
        return value.isoformat()
    if isinstance(value, bytes):
        return value.hex()
    if isinstance(value, Path):
        return str(value)
    return repr(value)


def _snapshot(value: Any, attempts: int = 5) -> Any:
    """Kopiert Daten, die ein anderer Thread gerade beschreiben kann (Wiederholung bei Race)."""
    for _ in range(attempts):
        try:
            return to_jsonable(value)
        except RuntimeError:  # z. B. "dictionary changed size during iteration"
            time.sleep(0.01)
    return {"hinweis": "Werte wegen gleichzeitigen Schreibens nicht lesbar"}


class Redactor:
    """Entfernt den Benutzernamen aus Texten (Rechnername bleibt im Klartext).

    Parameters
    ----------
    username
        Zu entfernender Anmeldename.
    active
        ``False`` bei ``--keep-user``.
    protected
        Texte, die unverändert bleiben müssen (z. B. der Rechnername).
    profile_dirs
        Tatsächliche Profilpfade (z. B. ``USERPROFILE``); ihr Ordnername wird wie der
        Anmeldename behandelt, weil er davon abweichen kann (Domänenkonten, ``jbusch.RWTH``).

    Notes
    -----
    Ersetzt werden (1) jedes Pfadsegment direkt unter ``Users`` außer den Systemprofilen
    (``Public``, ``Default``, ``All Users``), das deckt auch 8.3-Kurznamen wie ``JAKOBB~1``
    ab, (2) Anmeldename und Profilordnername als freies Wort ab vier Zeichen, in
    ``Users``-Pfaden auch kürzere. Profilnamen mit Leerzeichen werden nur über
    ``profile_dirs`` erkannt.
    """

    _SYSTEM_PROFILES = r"(?:Public|Default(?: User)?|All Users)"

    def __init__(
        self,
        username: str,
        active: bool,
        protected: Sequence[str] = (),
        profile_dirs: Sequence[str] = (),
    ) -> None:
        names = {username} if username else set()
        for profile in profile_dirs:
            last = re.split(r"[\\/]", profile.rstrip("\\/"))[-1]
            if last:
                names.add(last)
        self.active = active and bool(names)
        self._protected = [p for p in protected if p]
        self._patterns: list[re.Pattern[str]] = []
        if self.active:
            for name in sorted(names, key=len, reverse=True):
                esc = re.escape(name)
                self._patterns.append(re.compile(rf"(?i)(?<=[\\/]Users[\\/]){esc}[^\\/\s\"',;:)]*"))
                if len(name) >= 4:
                    self._patterns.append(
                        re.compile(rf"(?i)(?<![A-Za-z0-9_]){esc}(?![A-Za-z0-9_])")
                    )
            self._patterns.append(
                re.compile(
                    rf"(?i)(?<=[\\/]Users[\\/])(?!{self._SYSTEM_PROFILES}(?![^\\/\s\"',;:)]))"
                    r"(?!<user>)[^\\/\s\"',;:)]+"
                )
            )

    def text(self, value: str) -> str:
        """Ersetzt den Benutzernamen in einem Text durch ``<user>``."""
        if not self.active:
            return value
        for i, keep in enumerate(self._protected):
            value = value.replace(keep, f"\x00{i}\x00")
        for pattern in self._patterns:
            value = pattern.sub("<user>", value)
        for i, keep in enumerate(self._protected):
            value = value.replace(f"\x00{i}\x00", keep)
        return value

    def apply(self, value: Any) -> Any:
        """Wendet :meth:`text` rekursiv auf alle Zeichenketten an."""
        if not self.active:
            return value
        if isinstance(value, str):
            return self.text(value)
        if isinstance(value, list):
            return [self.apply(v) for v in value]
        if isinstance(value, dict):
            return {self.text(str(k)): self.apply(v) for k, v in value.items()}
        return value


def describe_exception(exc: BaseException) -> dict[str, Any]:
    """Beschreibt eine Exception einschließlich ``hresult``/``excepinfo`` (com_error)."""
    hresult = getattr(exc, "hresult", None)
    info: dict[str, Any] = {
        "typ": type(exc).__name__,
        "meldung": str(exc)[:500],
        "hresult": hresult,
        "hresult_hex": f"0x{hresult & 0xFFFFFFFF:08X}" if _is_int(hresult) else None,
        "excepinfo": getattr(exc, "excepinfo", None),
        "strerror": getattr(exc, "strerror", None),
        "argerror": getattr(exc, "argerror", None),
    }
    text = "".join(traceback.format_exception(type(exc), exc, exc.__traceback__))
    info["traceback_gekuerzt"] = text[-1200:]
    return info


def describe_file(path: Path) -> dict[str, Any]:
    """Größe, Änderungszeit und SHA-256 einer Datei (nur Lesen)."""
    stat = path.stat()
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return {
        "pfad": str(path),
        "groesse_byte": stat.st_size,
        "mtime_ns": stat.st_mtime_ns,
        "sha256": digest.hexdigest(),
    }


def pe_machine(path: str) -> str | None:
    """Liest den Maschinentyp aus dem PE-Header (32/64 Bit); ``None`` bei Nicht-PE/Fehler."""
    try:
        with open(path, "rb") as handle:
            head = handle.read(64)
            if len(head) < 64 or head[:2] != b"MZ":
                return None
            handle.seek(int.from_bytes(head[60:64], "little"))
            sig = handle.read(6)
    except OSError:
        return None
    if len(sig) < 6 or sig[:4] != b"PE\x00\x00":
        return None
    machine = int.from_bytes(sig[4:6], "little")
    names = {0x14C: "x86 (32 Bit)", 0x8664: "x64 (64 Bit)", 0xAA64: "ARM64"}
    return names.get(machine, f"0x{machine:04X}")


def expand_env(value: str, environ: Mapping[str, str]) -> str:
    """Ersetzt ``%NAME%`` aus ``environ`` (unbekannte Namen bleiben stehen)."""

    def repl(match: re.Match[str]) -> str:
        name = match.group(1)
        return environ.get(name, environ.get(name.upper(), match.group(0)))

    return re.sub(r"%([^%]+)%", repl, value)


def parse_server_path(value: str, environ: Mapping[str, str]) -> str:
    """Extrahiert den Dateipfad aus einem ``LocalServer32``/``InprocServer32``-Wert."""
    text = expand_env(value.strip(), environ)
    if text.startswith('"'):
        end = text.find('"', 1)
        return text[1:end] if end > 0 else text[1:]
    match = re.match(r"(.+?\.(?:exe|dll|ocx))(?:\s|$)", text, re.IGNORECASE)
    return match.group(1) if match else text


def collect_platform(environ: Mapping[str, str]) -> dict[str, Any]:
    """Windows-/Python-Version und Bitness (nur Standardbibliothek)."""
    arch = environ.get("PROCESSOR_ARCHITECTURE")
    arch_w6432 = environ.get("PROCESSOR_ARCHITEW6432")
    info: dict[str, Any] = {
        "system": platform.system(),
        "release": platform.release(),
        "version": platform.version(),
        "machine": platform.machine(),
        "win32_ver": list(platform.win32_ver()),
        "python_version": platform.python_version(),
        "python_implementierung": platform.python_implementation(),
        "python_bit": struct.calcsize("P") * 8,
        "python_pfad": sys.executable,
        "processor_architecture": arch,
        "processor_architew6432": arch_w6432,
    }
    if platform.system() == "Windows":
        is64 = bool(arch_w6432) or (arch or "").upper() in ("AMD64", "ARM64", "IA64")
        info["windows_bit_einschaetzung"] = 64 if is64 else 32
    return info


def sample_indices(count: int, n: int) -> list[int]:
    """Die ersten und letzten ``n`` 1-basierten Positionen aus ``count`` (ohne Doppelte)."""
    if count <= 0 or n <= 0:
        return []
    first = list(range(1, min(n, count) + 1))
    last = list(range(max(count - n + 1, 1), count + 1))
    return sorted(set(first + last))


def pywin32_info() -> dict[str, Any]:
    """Prüft, ob pywin32 importierbar ist (``import win32com.client``) und welche Version."""
    result: dict[str, Any] = {"importierbar": False, "version": None, "fehler": None}
    try:
        import win32com.client  # noqa: F401
    except Exception as exc:
        result["fehler"] = _short_error(exc)
        return result
    # Nur mit installiertem pywin32 erreichbar; unter Linux nicht testbar.
    result["importierbar"] = True  # pragma: no cover
    with contextlib.suppress(importlib.metadata.PackageNotFoundError):  # pragma: no cover
        result["version"] = importlib.metadata.version("pywin32")
    return result  # pragma: no cover


def run_command(command: list[str]) -> str:
    """Führt einen festen Befehl ohne Shell aus (z. B. ``tasklist``) und liefert stdout."""
    done = subprocess.run(command, capture_output=True, text=True, timeout=20, check=True)
    return done.stdout


# ---------------------------------------------------------------------------------------
# Umgebung (injizierbar) und Windows-Adapter
# ---------------------------------------------------------------------------------------


class RegistryReader(Protocol):
    """Lesender Zugriff auf HKEY_CLASSES_ROOT (``view``: 64 oder 32 Bit)."""

    def get_value(self, path: str, name: str, view: int) -> str | None:
        """Wert ``name`` (``""`` = Standardwert) oder ``None``, wenn nicht vorhanden."""
        ...

    def subkeys(self, path: str, view: int) -> list[str]:
        """Namen der Unterschlüssel (leer, wenn der Schlüssel fehlt)."""
        ...


@dataclass
class Env:
    """Alle Berührungspunkte zur Außenwelt; in Tests durch Doubles ersetzt."""

    dispatch: Callable[[str], Any]
    registry: RegistryReader | None
    enum_tlbs: Callable[[], list[dict[str, Any]]]
    read_constants: Callable[[list[str]], dict[str, Any]]
    file_version: Callable[[str], str | None]
    run_command: Callable[[list[str]], str]
    pywin32_info: Callable[[], dict[str, Any]]
    thread_init: Callable[[], None]
    thread_done: Callable[[], None]
    hard_exit: Callable[[int], None]
    input_fn: Callable[[str], str]
    now: Callable[[], dt.datetime]
    monotonic: Callable[[], float]
    environ: Mapping[str, str]
    hostname: str
    username: str
    system: str
    profile_dirs: tuple[str, ...] = ()
    extras: dict[str, Any] = field(default_factory=dict)


def _unavailable(what: str) -> ComUnavailableError:
    return ComUnavailableError(
        f"{what} nicht verfügbar: pywin32 fehlt oder dies ist kein Windows-Rechner "
        "(Stufe 0 funktioniert trotzdem)."
    )


def _com_dispatch(progid: str) -> Any:  # pragma: no cover - braucht pywin32 und PSV
    try:
        import win32com.client
    except ImportError as exc:
        raise _unavailable("COM-Zugriff") from exc
    return win32com.client.Dispatch(progid)


def _com_enum_tlbs() -> list[dict[str, Any]]:  # pragma: no cover - braucht pywin32
    try:
        from win32com.client import selecttlb
    except ImportError as exc:
        raise _unavailable("EnumTlbs") from exc
    out: list[dict[str, Any]] = []
    for spec in selecttlb.EnumTlbs():
        out.append(
            {
                "desc": str(getattr(spec, "desc", "")),
                "clsid": str(getattr(spec, "clsid", "")),
                "major": getattr(spec, "major", None),
                "minor": getattr(spec, "minor", None),
                "lcid": getattr(spec, "lcid", None),
                "dll": str(getattr(spec, "dll", "")),
            }
        )
    return out


def _com_read_constants(names: list[str]) -> dict[str, Any]:  # pragma: no cover - pywin32
    try:
        import win32com.client
    except ImportError as exc:
        raise _unavailable("win32com.client.constants") from exc
    consts = win32com.client.constants
    return {name: getattr(consts, name, None) for name in names}


def _com_thread_init() -> None:  # pragma: no cover - braucht pywin32
    try:
        import pythoncom
    except ImportError:
        return
    pythoncom.CoInitialize()


def _com_thread_done() -> None:  # pragma: no cover - braucht pywin32
    try:
        import pythoncom
    except ImportError:
        return
    pythoncom.CoUninitialize()


def _winreg() -> Any:  # pragma: no cover - nur Windows
    # Über import_module, damit mypy unter Linux (ohne winreg-Stubs) nicht scheitert.
    return importlib.import_module("winreg")


class WinRegistryReader:  # pragma: no cover - braucht winreg (nur Windows); dünner Adapter
    """Liest HKEY_CLASSES_ROOT über ``winreg`` (nur ``KEY_READ``)."""

    def _open(self, path: str, view: int) -> Any:
        winreg = _winreg()
        flag = winreg.KEY_WOW64_64KEY if view == 64 else winreg.KEY_WOW64_32KEY
        return winreg.OpenKey(winreg.HKEY_CLASSES_ROOT, path, 0, winreg.KEY_READ | flag)

    def get_value(self, path: str, name: str, view: int) -> str | None:
        """Liest einen Wert."""
        winreg = _winreg()

        try:
            with self._open(path, view) as key:
                value, _type = winreg.QueryValueEx(key, name)
        except OSError:
            return None
        return str(value)

    def subkeys(self, path: str, view: int) -> list[str]:
        """Listet Unterschlüssel."""
        winreg = _winreg()

        names: list[str] = []
        try:
            with self._open(path, view) as key:
                index = 0
                while True:
                    try:
                        names.append(winreg.EnumKey(key, index))
                    except OSError:
                        break
                    index += 1
        except OSError:
            return []
        return names


def _win_file_version(path: str) -> str | None:  # pragma: no cover - nur Windows (version.dll)
    if sys.platform != "win32":
        return None
    import ctypes
    from ctypes import wintypes

    version = ctypes.WinDLL("version")
    size = version.GetFileVersionInfoSizeW(path, None)
    if not size:
        return None
    buffer = ctypes.create_string_buffer(size)
    if not version.GetFileVersionInfoW(path, 0, size, buffer):
        return None
    pointer = ctypes.c_void_p()
    length = wintypes.UINT()
    if not version.VerQueryValueW(buffer, "\\", ctypes.byref(pointer), ctypes.byref(length)):
        return None

    class FixedFileInfo(ctypes.Structure):
        _fields_ = (
            ("signature", wintypes.DWORD),
            ("struc_version", wintypes.DWORD),
            ("file_version_ms", wintypes.DWORD),
            ("file_version_ls", wintypes.DWORD),
        )

    info = ctypes.cast(pointer, ctypes.POINTER(FixedFileInfo)).contents
    ms, ls = info.file_version_ms, info.file_version_ls
    return f"{ms >> 16}.{ms & 0xFFFF}.{ls >> 16}.{ls & 0xFFFF}"


def _hard_exit(code: int) -> None:  # pragma: no cover - beendet den Prozess hart
    sys.stdout.flush()
    sys.stderr.flush()
    os._exit(code)


def build_env() -> Env:
    """Baut die echte Umgebung. Unter Linux fehlen Registry und COM (saubere Hinweise)."""
    import getpass

    def real_registry() -> RegistryReader | None:
        if sys.platform == "win32":  # pragma: no cover - nur Windows
            return WinRegistryReader()
        return None

    return Env(
        dispatch=_com_dispatch,
        registry=real_registry(),
        enum_tlbs=_com_enum_tlbs,
        read_constants=_com_read_constants,
        file_version=_win_file_version,
        run_command=run_command,
        pywin32_info=pywin32_info,
        thread_init=_com_thread_init,
        thread_done=_com_thread_done,
        hard_exit=_hard_exit,
        input_fn=input,
        now=lambda: dt.datetime.now().astimezone(),
        monotonic=time.monotonic,
        environ=os.environ,
        hostname=platform.node(),
        username=getpass.getuser(),
        system=platform.system(),
        profile_dirs=tuple(
            dict.fromkeys(p for p in (os.environ.get("USERPROFILE"), str(Path.home())) if p)
        ),
    )


# ---------------------------------------------------------------------------------------
# Prüfpunkte, Ausführung und Bericht
# ---------------------------------------------------------------------------------------

# Offene [ungeprüft]-Fragen aus Plan E1 / I5 10 und der Prüfpunkt, der sie beantworten kann.
OPEN_QUESTIONS: tuple[tuple[str, str], ...] = (
    ("Kehrt GetApplication(False) bei laufender Instanz ohne Start zurück?", "P1-5-verbinden"),
    ("Bitness und Servertyp (LocalServer32/InprocServer32) der Polytec-Server", "P1-2-registry"),
    ("Ist FftAcqPropertiesValidator in dieser Version vorhanden?", "P1-6-eigenschaften"),
    ("Sind Infos.Hardware und Alignments3D im Erfassungsmodus lesbar?", "P1-6-hardware"),
    ("Indexbasis und Label/Index bei MeasPoints.Item", "P1-6-messpunkte"),
    ("Liefert CoordXYZ (ByRef) in pywin32 ein Tupel?", "P1-6-messpunkte"),
    ("Frequenzachse: GetMidX(i) gegen k*df (KONVENTIONEN)", "P1-10-daten"),
    ("Form der HRESULT/excepinfo-Angaben bei COM-Fehlern", "P1-6-zustand"),
)


@dataclass
class Step:
    """Ein Prüfpunkt: Kennung, Stufe, Titel, Beleg und die auszuführende Funktion."""

    id: str
    stufe: str
    titel: str
    beleg: str
    func: Callable[[StepContext], None]


@dataclass
class _Running:
    step: Step
    started: float
    cx: StepContext


class StepContext:
    """Arbeitsumgebung eines Prüfpunkts: Werte sammeln, fehlertolerant lesen, COM holen."""

    def __init__(self, runner: Runner, step: Step) -> None:
        self.runner = runner
        self.step = step
        self.env = runner.env
        self.args = runner.args
        self.state = runner.state
        self.w: dict[str, Any] = {}
        self.sub_errors: list[str] = []
        self.errors = 0
        self.kern = ""
        self.hint = ""
        self.exception: dict[str, Any] | None = None

    def skip(self, reason: str) -> Skipped:
        """Erzeugt die Ausnahme zum Überspringen (``raise cx.skip(...)``)."""
        return Skipped(reason)

    def need(self, key: str, because: str) -> Any:
        """Liefert einen Wert aus früheren Prüfpunkten oder überspringt den Punkt."""
        value = self.state.get(key)
        if value is None:
            raise Skipped(f"Voraussetzung fehlt ({because})")
        return value

    def com(self, fn: Callable[..., Any], *args: Any) -> Any:
        """Ruft eine COM-nahe Funktion auf; fehlendes pywin32 wird zum Überspringen."""
        try:
            return fn(*args)
        except ComUnavailableError as exc:
            raise Skipped(str(exc)) from exc

    def dispatch(self, progid: str) -> WhitelistProxy:
        """Erzeugt ein freigegebenes Einstiegsobjekt (nur ProgIDs aus der Whitelist)."""
        ctx = self.runner.proxy_ctx
        kind = ALLOWED_PROGIDS.get(progid)
        if kind is None:
            ctx.record_denied("Dispatch", progid, "dispatch", "ProgID nicht in der Whitelist")
            raise PermissionError(f"verweigert (Default deny): Dispatch({progid!r})")
        start = time.perf_counter()
        error: str | None = None
        ctx.pending = {"pfad": f"Dispatch.{progid}", "op": "dispatch", "argumente": []}
        try:
            obj = self.com(self.env.dispatch, progid)
        except Exception as exc:
            error = _short_error(exc)
            raise
        finally:
            ctx.pending = None
            ctx.record_call("Dispatch", progid, "dispatch", (), time.perf_counter() - start, error)
        return WhitelistProxy(obj, kind, ctx)

    def rd(
        self,
        key: str,
        fn: Callable[..., Any],
        *,
        optional: bool = False,
        into: dict[str, Any] | None = None,
        keep: bool = True,
    ) -> Any:
        """Liest einen Wert fehlertolerant; Fehler landen unter ``key`` im Bericht.

        Mit ``keep=False`` wird ein Erfolg nicht im Bericht abgelegt (für Objekte/Rohdaten).
        """
        target = self.w if into is None else into
        try:
            value = fn()
        except PermissionError:
            raise
        except Exception as exc:
            info = describe_exception(exc)
            target[key] = {"fehler": info}
            self.sub_errors.append(f"{key}: {info['typ']}: {info['meldung']}"[:240])
            if not optional:
                self.errors += 1
            return None
        if keep:
            target[key] = value
        return value

    def read_all(
        self, proxy: WhitelistProxy, names: Sequence[str], into: dict[str, Any] | None = None
    ) -> dict[str, Any]:
        """Liest mehrere Properties; liefert die gelesenen Werte (Fehler: ``None``)."""
        values: dict[str, Any] = {}
        for name in names:
            values[name] = self.rd(name, lambda n=name: getattr(proxy, n), into=into)
        return values

    def raw(self, filename: str, lines: list[str]) -> None:
        """Legt Rohtext für eine Datei im Ausgabeordner ab."""
        self.runner.raw_files[filename] = lines

    def deviation(self, text: str, ref: str) -> None:
        """Hält eine Abweichung von der Erwartung aus I5 fest."""
        self.runner.data["abweichungen"].append(
            {"pruefpunkt": self.step.id, "text": text, "beleg_ref": ref}
        )


class Runner:
    """Führt Prüfpunkte aus, schreibt den Bericht fortlaufend und überwacht Blockaden."""

    def __init__(
        self,
        env: Env,
        args: argparse.Namespace,
        out_dir: Path,
        redactor: Redactor,
        proxy_ctx: ProxyContext,
        poll_s: float = 0.25,
    ) -> None:
        self.env = env
        self.args = args
        self.out_dir = out_dir
        self.redactor = redactor
        self.proxy_ctx = proxy_ctx
        self.poll_s = poll_s
        self.timeout_s: float = args.timeout_s
        self.state: dict[str, Any] = {}
        self.raw_files: dict[str, list[str]] = {}
        self.data: dict[str, Any] = {}
        self.current: _Running | None = None
        self.blocked = False
        self.exit_code = EXIT_OK
        self.worker_error: Exception | None = None
        self._completed = False
        self._lock = threading.RLock()
        self._console_lines: list[str] = []

    # -- Ausgabe ------------------------------------------------------------------------
    def say(self, text: str) -> None:
        """Schreibt eine Zeile auf die Konsole und ins Log (ohne Benutzername)."""
        line = self.redactor.text(text)
        encoding = sys.stdout.encoding or "utf-8"
        print(line.encode(encoding, "replace").decode(encoding), flush=True)
        with self._lock:
            self._console_lines.append(line)
            self._write("konsole.log", "\n".join(self._console_lines) + "\n")

    def _write(self, name: str, text: str) -> None:
        """Einzige Schreibstelle: schreibt atomar in eine Datei des Ausgabeordners."""
        target = self.out_dir / name
        temp = self.out_dir / (name + ".tmp")
        for attempt in range(WRITE_RETRIES):
            try:
                temp.write_text(text, encoding="utf-8", newline="\n")
                os.replace(temp, target)
            except OSError:
                # z. B. kurzzeitig gesperrt durch einen Virenscanner (WinError 5/32)
                if attempt == WRITE_RETRIES - 1:
                    raise
                time.sleep(WRITE_RETRY_WAIT_S)
            else:
                return

    def flush(self) -> None:
        """Schreibt bericht.json, zusammenfassung.md und die Rohdateien."""
        with self._lock:
            calls, denied = self.proxy_ctx.snapshot()
            self.data["whitelist_aufrufe"] = calls
            self.data["verweigert"] = denied
            report = self.redactor.apply(to_jsonable(self.data))
            self._write(
                "bericht.json",
                json.dumps(report, ensure_ascii=False, indent=2, allow_nan=False) + "\n",
            )
            self._write("zusammenfassung.md", render_summary(report))
            for name, lines in self.raw_files.items():
                self._write(name, self.redactor.text("\n".join(lines)) + "\n")

    # -- Ausführung ---------------------------------------------------------------------
    def _finish_entry(self, step: Step, cx: StepContext, status: str, started: float) -> None:
        entry: dict[str, Any] = {
            "id": step.id,
            "stufe": step.stufe,
            "titel": step.titel,
            "beleg_ref": step.beleg,
            "status": status,
            "kernwert": cx.kern,
            "hinweis": cx.hint,
            "werte": cx.w,
            "auffaelligkeiten": cx.sub_errors,
            "dauer_s": round(self.env.monotonic() - started, 4),
            "exception": cx.exception,
        }
        with self._lock:
            if self.blocked:
                return
            self.data["pruefpunkte"].append(entry)
            self.current = None
        self.say(f"[{step.id}] {status} ({entry['dauer_s']:.2f} s) {cx.kern} {cx.hint}".rstrip())
        self.flush()

    def execute(self, step: Step) -> None:
        """Führt einen Prüfpunkt aus; jede Exception bleibt auf diesen Punkt beschränkt."""
        cx = StepContext(self, step)
        started = self.env.monotonic()
        self.proxy_ctx.current_step = step.id
        with self._lock:
            if self.blocked:
                return
            self.current = _Running(step, started, cx)
        status = "ok"
        try:
            step.func(cx)
            if cx.errors:
                status = "fehler"
        except Skipped as skipped:
            status = "uebersprungen"
            cx.hint = str(skipped)
        except Exception as exc:
            status = "fehler"
            cx.hint = f"{type(exc).__name__}: {exc}"[:300]
            cx.exception = describe_exception(exc)
        self._finish_entry(step, cx, status, started)

    def _worker(self, steps: Sequence[Step]) -> None:
        try:
            self.env.thread_init()
        except Exception as exc:  # COM-Initialisierung ist Voraussetzung, kein Absturz
            self.say(f"Hinweis: Thread-Initialisierung fehlgeschlagen: {_short_error(exc)}")
        try:
            for step in steps:
                if self.blocked:
                    return
                try:
                    self.execute(step)
                except Exception as exc:  # Fehler außerhalb von step.func (z. B. Schreiben)
                    self.worker_error = exc
                    return
            self._completed = True
        finally:
            # COM-Referenzen im Apartment des Workers freigeben, bevor es endet.
            self.state.clear()
            gc.collect()
            try:
                self.env.thread_done()
            except Exception as exc:
                self.say(f"Hinweis: Thread-Abschluss fehlgeschlagen: {_short_error(exc)}")

    def _mark_remaining(self, steps: Sequence[Step], reason: str) -> None:
        done = {p["id"] for p in self.data["pruefpunkte"]}
        for step in steps:
            if step.id not in done:
                self.data["pruefpunkte"].append(
                    {
                        "id": step.id,
                        "stufe": step.stufe,
                        "titel": step.titel,
                        "beleg_ref": step.beleg,
                        "status": "uebersprungen",
                        "kernwert": "",
                        "hinweis": reason,
                        "werte": {},
                        "auffaelligkeiten": [],
                        "dauer_s": 0.0,
                        "exception": None,
                    }
                )

    def _stop_run(
        self,
        steps: Sequence[Step],
        run_status: str,
        hint: str,
        code: int,
        expected: _Running | None = None,
    ) -> bool:
        with self._lock:
            running = self.current
            if expected is not None and running is not expected:
                return False  # der Prüfpunkt hat inzwischen gewechselt: kein falscher Alarm
            self.blocked = True
            self.exit_code = code
            self.data["lauf"] = {"status": run_status, "hinweis": hint}
            if running is not None:
                pending = self.proxy_ctx.pending
                self.data["pruefpunkte"].append(
                    {
                        "id": running.step.id,
                        "stufe": running.step.stufe,
                        "titel": running.step.titel,
                        "beleg_ref": running.step.beleg,
                        "status": "blockiert",
                        "kernwert": "",
                        "hinweis": hint,
                        "werte": _snapshot(running.cx.w),
                        "auffaelligkeiten": list(running.cx.sub_errors),
                        "dauer_s": round(self.env.monotonic() - running.started, 4),
                        "exception": None,
                        "letzter_aufruf": pending,
                    }
                )
            self._mark_remaining(steps, f"Lauf beendet: {run_status}")
        try:
            self.say(f"!!! {run_status}: {hint}")
            self.flush()
        except Exception as exc:
            sys.stderr.write(f"Teilbericht konnte nicht geschrieben werden: {_short_error(exc)}\n")
        finally:
            self.env.hard_exit(code)
        return True

    def _fail_run(self, steps: Sequence[Step]) -> None:
        """Der Worker ist ohne regulären Abschluss beendet (z. B. Schreibfehler)."""
        exc = self.worker_error
        hint = (
            f"Interner Fehler außerhalb eines Prüfpunkts: {_short_error(exc)}"
            if exc is not None
            else "Der Worker-Thread wurde unerwartet beendet."
        )
        with self._lock:
            self.exit_code = EXIT_ERROR
            self.data["lauf"] = {
                "status": "fehler",
                "hinweis": hint,
                "exception": describe_exception(exc) if exc is not None else None,
            }
            self._mark_remaining(steps, "Lauf beendet: fehler")
        try:
            self.say(f"!!! {hint}")
            self.flush()
        except Exception as exc2:
            sys.stderr.write(f"Teilbericht konnte nicht geschrieben werden: {_short_error(exc2)}\n")

    def run_guarded(self, steps: Sequence[Step]) -> bool:
        """Führt alle Prüfpunkte in einem Worker-Thread aus und überwacht den Timeout.

        Returns
        -------
        bool
            ``True``, wenn alle Prüfpunkte regulär durchgelaufen sind; ``False`` nach
            Blockade, Abbruch oder einem Fehler außerhalb der Prüfpunkte (Teilbericht
            geschrieben, soweit möglich; ``exit_code`` gesetzt).
        """
        worker = threading.Thread(target=self._worker, args=(steps,), daemon=True)
        worker.start()
        try:
            while worker.is_alive():
                worker.join(self.poll_s)
                running = self.current
                if running is None or self.blocked:
                    continue
                if self.env.monotonic() - running.started > self.timeout_s:
                    pending = self.proxy_ctx.pending
                    hint = (
                        f"blockiert bei {running.step.id} (kein Ergebnis nach "
                        f"{self.timeout_s:g} s; letzter Aufruf: "
                        f"{pending['pfad'] if pending else 'keiner'}). "
                        "Teilbericht geschrieben, Prozess wird beendet."
                    )
                    if self._stop_run(steps, "blockiert", hint, EXIT_BLOCKED, expected=running):
                        return False
        except KeyboardInterrupt:
            self._stop_run(steps, "abgebrochen", "Abbruch mit Strg+C", EXIT_INTERRUPTED)
            return False
        if not self._completed and not self.blocked:
            self._fail_run(steps)
            return False
        return True


# ---------------------------------------------------------------------------------------
# Stufe 0: Standardbibliothek, kein COM
# ---------------------------------------------------------------------------------------


def _step_umgebung(cx: StepContext) -> None:
    info = collect_platform(cx.env.environ)
    cx.w.update(info)
    cx.runner.data["umgebung"].update(info)
    cx.kern = (
        f"{info['system']} {info['release']}, Python {info['python_version']} "
        f"({info['python_bit']} Bit)"
    )


def _step_pywin32(cx: StepContext) -> None:
    info = cx.env.pywin32_info()
    cx.w.update(info)
    cx.runner.data["umgebung"]["pywin32"] = info
    cx.state["pywin32_ok"] = bool(info.get("importierbar"))
    if info.get("importierbar"):
        cx.kern = f"pywin32 importierbar, Version {info.get('version')}"
    else:
        cx.kern = "pywin32 nicht importierbar"
        cx.hint = "Stufe 1 braucht pywin32; Stufe 0 läuft trotzdem."


def _reg_get(reg: RegistryReader, path: str, name: str, view: int, lines: list[str]) -> str | None:
    value = reg.get_value(path, name, view)
    shown = "(nicht vorhanden)" if value is None else f'"{value}"'
    lines.append(f"[HKCR({view}-Bit-Sicht)\\{path}] {name or '@'} = {shown}")
    return value


def _read_progid(
    reg: RegistryReader, progid: str, view: int, lines: list[str], environ: Mapping[str, str]
) -> dict[str, Any]:
    result: dict[str, Any] = {"vorhanden": False}
    clsid = _reg_get(reg, f"{progid}\\CLSID", "", view, lines)
    if clsid is None:
        return result
    result["vorhanden"] = True
    result["clsid"] = clsid
    base = f"CLSID\\{clsid}"
    result["beschreibung"] = _reg_get(reg, base, "", view, lines)
    for key in ("LocalServer32", "InprocServer32"):
        value = _reg_get(reg, f"{base}\\{key}", "", view, lines)
        result[key] = value
        if value is not None:
            result[key + "_pfad"] = parse_server_path(value, environ)
        threading_model = _reg_get(reg, f"{base}\\{key}", "ThreadingModel", view, lines)
        if threading_model is not None:
            result[key + "_threadingmodel"] = threading_model
    result["TypeLib"] = _reg_get(reg, f"{base}\\TypeLib", "", view, lines)
    appid = _reg_get(reg, base, "AppID", view, lines)
    result["AppID"] = appid
    if appid is not None:
        result["AppID_name"] = _reg_get(reg, f"AppID\\{appid}", "", view, lines)
    return result


def _step_registry(cx: StepContext) -> None:
    reg = cx.env.registry
    if reg is None:
        raise Skipped("Registry nicht lesbar: winreg fehlt (kein Windows-Rechner).")
    lines: list[str] = []
    progids: dict[str, Any] = {}
    paths: list[str] = []
    for progid in PROGIDS:
        per_view = {
            f"{view}_bit": _read_progid(reg, progid, view, lines, cx.env.environ)
            for view in (64, 32)
        }
        progids[progid] = per_view
        for entry in per_view.values():
            for key in ("LocalServer32_pfad", "InprocServer32_pfad"):
                path = entry.get(key)
                if path and path not in paths:
                    paths.append(path)
    cx.w["progids"] = progids
    cx.state["server_pfade"] = paths
    cx.raw("registry.reg.txt", lines)
    found = [p for p, v in progids.items() if any(e["vorhanden"] for e in v.values())]
    cx.kern = f"{len(found)} von {len(PROGIDS)} ProgIDs registriert"


def _step_dateien(cx: StepContext) -> None:
    paths = cx.state.get("server_pfade")
    if paths is None:
        raise Skipped("Voraussetzung fehlt (P1-2-registry lieferte keine Serverpfade)")
    files: list[dict[str, Any]] = []
    for path in paths:
        item: dict[str, Any] = {"pfad": path, "vorhanden": os.path.isfile(path)}
        lowered = path.lower()
        if "(x86)" in lowered:
            item["ordner_hinweis"] = "Program Files (x86): spricht für 32-Bit-Installation"
        if item["vorhanden"]:
            stat = os.stat(path)
            item["groesse_byte"] = stat.st_size
            item["pe_maschine"] = pe_machine(path)
            item["dateiversion"] = cx.env.file_version(path)
        files.append(item)
    cx.w["server_dateien"] = files
    cx.kern = f"{len(files)} Serverdatei(en) geprüft"


def _step_typelibs_registry(cx: StepContext) -> None:
    reg = cx.env.registry
    if reg is None:
        raise Skipped("Registry nicht lesbar: winreg fehlt (kein Windows-Rechner).")
    lines: list[str] = []
    matches: list[dict[str, Any]] = []
    total = 0
    for view in (64, 32):
        for guid in reg.subkeys("TypeLib", view):
            for version in reg.subkeys(f"TypeLib\\{guid}", view):
                total += 1
                base = f"TypeLib\\{guid}\\{version}"
                name = reg.get_value(base, "", view) or ""
                dlls: dict[str, str] = {}
                for lcid in reg.subkeys(base, view):
                    for arch in ("win32", "win64"):
                        dll = reg.get_value(f"{base}\\{lcid}\\{arch}", "", view)
                        if dll:
                            dlls[f"{lcid}/{arch}"] = dll
                haystack = (name + " " + " ".join(dlls.values())).lower()
                if any(key in haystack for key in TYPELIB_KEYWORDS):
                    matches.append(
                        {"sicht": f"{view}_bit", "guid": guid, "version": version,
                         "name": name, "dateien": dlls}
                    )  # fmt: skip
                    lines.append(f"({view}-Bit-Sicht) {guid} v{version} {name!r} {dlls}")
    cx.w["gesamt_gesehen"] = total
    cx.w["treffer"] = matches
    cx.raw("typelibs.txt", lines)
    cx.kern = f"{len(matches)} Polytec-Typbibliothek(en) von {total} gesichtet"


def _step_verzeichnisse(cx: StepContext) -> None:
    if cx.env.system != "Windows":
        raise Skipped("Nur unter Windows sinnvoll (Program-Files-Verzeichnisse).")
    listing: dict[str, Any] = {}
    candidates = (
        ("ProgramFiles", ("Polytec",)),
        ("ProgramFiles(x86)", ("Polytec",)),
        ("CommonProgramFiles", ("Polytec", "COM")),
        ("CommonProgramFiles(x86)", ("Polytec", "COM")),
    )
    for var, rel in candidates:
        base = cx.env.environ.get(var)
        key = f"%{var}%\\" + "\\".join(rel)
        if not base:
            listing[key] = {"vorhanden": False, "hinweis": "Umgebungsvariable nicht gesetzt"}
            continue
        listing[key] = _list_dir(Path(base).joinpath(*rel))
    cx.w["verzeichnisse"] = listing
    cx.kern = f"{sum(1 for v in listing.values() if v['vorhanden'])} Verzeichnis(se) vorhanden"


def _list_dir(path: Path) -> dict[str, Any]:
    if not path.is_dir():
        return {"vorhanden": False}
    entries: list[dict[str, Any]] = []
    for item in sorted(path.iterdir(), key=lambda p: p.name.lower())[:MAX_DIR_ENTRIES]:
        entry: dict[str, Any] = {"name": item.name, "ordner": item.is_dir()}
        if item.is_file():
            entry["groesse_byte"] = item.stat().st_size
        entries.append(entry)
    return {"vorhanden": True, "eintraege": entries}


def _step_prozess(cx: StepContext) -> None:
    if cx.env.system != "Windows":
        raise Skipped("Prozessliste nur unter Windows (tasklist).")
    output = cx.env.run_command(["tasklist", "/FO", "CSV", "/NH"])
    found: list[dict[str, str]] = []
    for row in csv.reader(io.StringIO(output)):
        if len(row) >= 2 and any(key in row[0].lower() for key in PROCESS_KEYWORDS):
            found.append({"name": row[0], "pid": row[1]})
    cx.w["psv_prozesse"] = found
    cx.state["psv_prozess_laeuft"] = any("psv" in p["name"].lower() for p in found)
    cx.kern = f"{len(found)} passende Prozesse"


# ---------------------------------------------------------------------------------------
# Stufe 1: COM, nur lesend
# ---------------------------------------------------------------------------------------


def _step_typelibs_com(cx: StepContext) -> None:
    specs = cx.com(cx.env.enum_tlbs)
    keep = [
        s
        for s in specs
        if any(
            k in (str(s.get("desc", "")) + str(s.get("dll", ""))).lower() for k in TYPELIB_KEYWORDS
        )
    ]
    cx.w["typbibliotheken_gesamt"] = len(specs)
    cx.w["typbibliotheken_polytec"] = keep
    expected = EXPECTED_CONSTANTS
    got = cx.com(cx.env.read_constants, list(expected))
    missing = sorted(n for n in expected if got.get(n) is None)
    wrong = {n: {"erwartet": v, "gefunden": got[n]} for n, v in expected.items()
             if got.get(n) is not None and got[n] != v}  # fmt: skip
    cx.w["constants"] = {
        "geprueft": len(expected),
        "nicht_verfuegbar": len(missing),
        "abweichend": wrong,
    }
    if len(missing) == len(expected):
        cx.hint = (
            "Keine win32com-Konstanten verfügbar. Die Ursache wurde nicht geprüft; der "
            "Vergleich mit I5 Abschnitt 8 ist damit nicht möglich (das Skript erzeugt "
            "keine Typbibliotheks-Wrapper)."
        )
    for name, pair in wrong.items():
        cx.deviation(f"{name}: erwartet {pair['erwartet']}, gefunden {pair['gefunden']}", "I5 8")
    cx.kern = f"{len(keep)} Polytec-Typbibliotheken, {len(wrong)} abweichende Konstanten"


def _step_verbinden(cx: StepContext) -> None:
    if not (cx.state.get("psv_prozess_laeuft") or cx.state.get("start_erlaubt")):
        raise Skipped(
            "Sperre: Stufe 0 hat keinen laufenden PSV-Prozess gefunden (oder die Prozessliste "
            "war nicht lesbar). Das Objekt PSV.AcquisitionInstance wird deshalb nicht angelegt, "
            "weil COM bei einer als Server registrierten PSV-EXE diese beim Anlegen selbst "
            "starten könnte. PSV im Erfassungsmodus starten und erneut ausführen, oder "
            "--start-psv mit Bestätigung verwenden."
        )
    inst = cx.dispatch("PSV.AcquisitionInstance")
    running = bool(cx.rd("IsRunning", lambda: inst.IsRunning))
    if cx.errors:
        raise Skipped("IsRunning nicht lesbar; Stufe 1 wird nicht fortgesetzt.")
    if not running and not cx.state.get("start_erlaubt"):
        raise Skipped(
            "PSV läuft nicht (IsRunning=False). Bitte PSV im Datenerfassungsmodus starten und "
            "Stufe 1 erneut ausführen. Das Skript startet PSV nicht (nur mit --start-psv)."
        )
    start = time.perf_counter()
    if running:
        app = inst.GetApplication(False)
    else:
        cx.runner.say("PSV läuft nicht: Start mit --start-psv (bestätigt) ...")
        app = inst.GetApplication(True, START_TIMEOUT_MS)
    cx.w["GetApplication_dauer_s"] = round(time.perf_counter() - start, 4)
    cx.w["GetApplication_gestartet"] = not running
    if app is None:
        raise RuntimeError("GetApplication lieferte keine Anwendung (Nothing).")
    cx.state["app"] = app
    cx.kern = "verbunden" if running else "PSV gestartet und verbunden"


def _step_application(cx: StepContext) -> None:
    app = cx.need("app", "P1-5-verbinden")
    values = cx.read_all(app, APP_PROPS)
    mode = values.get("Mode")
    if mode is not None and mode != 1:
        cx.deviation(f"Application.Mode = {mode!r}, erwartet 1 (Acquisition)", "I5 8")
    acq = cx.rd("Acquisition", lambda: app.Acquisition, keep=False)
    cx.w["Acquisition_erreichbar"] = acq is not None
    if acq is not None:
        cx.state["acq"] = acq
    cx.kern = f"Version {values.get('Version')!r}, Mode {mode!r}"


def _step_zustand(cx: StepContext) -> None:
    acq = cx.need("acq", "P1-5-application: Acquisition nicht erreichbar")
    state = cx.rd("State", lambda: acq.State)
    if state is None:
        cx.state["acq"] = None
        raise Skipped("Acquisition.State nicht lesbar; weitere Lesezugriffe werden unterlassen.")
    if state != PSV_ACQUISITION_STOPPED:
        cx.w["warnung"] = (
            f"State = {state!r}, nicht Stopped: Es läuft evtl. eine Messung. Das Skript "
            "liest nur und greift nie ein (kein Stop)."
        )
        cx.hint = cx.w["warnung"]
    cx.read_all(acq, ("Mode", "ScanCaps", "GeneratorsOn", "ScanFileName"))
    lasers: dict[str, Any] = {}
    for index in (-1, 1, 2, 3):
        cx.rd(str(index), lambda i=index: acq.GetLaserOn(i), optional=True, into=lasers)
    cx.w["GetLaserOn"] = lasers
    cx.kern = f"State {state!r}, GeneratorsOn {cx.w.get('GeneratorsOn')!r}"


def _infos(cx: StepContext) -> WhitelistProxy:
    acq = cx.need("acq", "P1-5-application: Acquisition nicht erreichbar")
    if cx.state.get("infos") is None:
        cx.state["infos"] = acq.Infos
    infos: WhitelistProxy = cx.state["infos"]
    return infos


def _step_eigenschaften(cx: StepContext) -> None:
    acq = cx.need("acq", "P1-5-application: Acquisition nicht erreichbar")
    props = acq.ActiveProperties
    flags = cx.read_all(props, HAS_PROPS)
    cx.w["gruppen_vorhanden"] = [n[3:-10] for n, v in flags.items() if v is True]
    if flags.get("HasFftProperties") is True:
        fft = props.FftProperties
        cx.read_all(fft, FFT_PROPS, into=cx.w.setdefault("Fft", {}))
        found = cx.rd("FftAcqPropertiesValidator_vorhanden", lambda: fft.exists(
            "FftAcqPropertiesValidator"), optional=True)  # fmt: skip
        if found is False:
            cx.deviation("FftAcqPropertiesValidator fehlt in dieser Version", "I5 2.6")
        cx.state["fft"] = {k: v for k, v in cx.w["Fft"].items() if not isinstance(v, dict)}
    if flags.get("HasAverageProperties") is True:
        cx.read_all(props.AverageProperties, AVG_PROPS, into=cx.w.setdefault("Average", {}))
    if flags.get("HasGeneralProperties") is True:
        cx.read_all(props.GeneralProperties, GENERAL_PROPS, into=cx.w.setdefault("General", {}))
    cx.kern = f"Gruppen: {', '.join(cx.w['gruppen_vorhanden']) or 'keine'}"


def _step_hardware(cx: StepContext) -> None:
    infos = _infos(cx)
    has = cx.read_all(infos, INFOS_HAS, into=cx.w.setdefault("Infos_Has", {}))
    if has.get("HasHardware") is True:
        cx.read_all(infos.Hardware, HARDWARE_PROPS, into=cx.w.setdefault("Hardware", {}))
    else:
        cx.hint = "Infos.HasHardware ist nicht True; Hardware wird nicht gelesen."
    cx.kern = f"FrontEnd {cx.w.get('Hardware', {}).get('FrontEnd')!r}"


def _step_scankopf(cx: StepContext) -> None:
    infos = _infos(cx)
    if cx.rd("HasScanHeadDevicesInfo", lambda: infos.HasScanHeadDevicesInfo) is True:
        cx.read_all(infos.ScanHeadDevicesInfo, SCANHEAD_PROPS)
    else:
        cx.hint = "Infos.HasScanHeadDevicesInfo ist nicht True."
    cx.kern = f"ScanHeadType {cx.w.get('ScanHeadType')!r}"


def _step_vibrometer(cx: StepContext) -> None:
    infos = _infos(cx)
    if cx.rd("HasVibrometers", lambda: infos.HasVibrometers) is not True:
        cx.hint = "Infos.HasVibrometers ist nicht True."
        return
    vib = infos.Vibrometers
    count = cx.rd("Count", lambda: vib.Count)
    groups: list[dict[str, Any]] = []
    if isinstance(count, int):
        for i in range(1, min(count, MAX_VIBROMETERS) + 1):
            sec: dict[str, Any] = {"item": i}
            group = cx.rd("Item", lambda i=i: vib.Item(i), into=sec, keep=False)
            if group is not None:
                info = cx.rd(
                    "ControllerInfo", lambda g=group: g.ControllerInfo, into=sec, keep=False
                )
                if info is not None:
                    cx.read_all(info, CONTROLLER_PROPS, into=sec)
                _read_controllers(cx, group, sec)
            groups.append(sec)
    cx.w["gruppen"] = groups
    cx.kern = f"Vibrometers.Count {count!r}"


def _read_controllers(cx: StepContext, group: WhitelistProxy, sec: dict[str, Any]) -> None:
    """Sensorkopf-Infos über Controllers(c).SensorHeads(s).SensorHeadInfo (0-basiert, nur lesen)."""
    controllers = cx.rd("Controllers", lambda: group.Controllers, into=sec, keep=False)
    if controllers is None:
        return
    ccount = cx.rd("Controllers_Count", lambda: controllers.Count, into=sec)
    listing: list[dict[str, Any]] = []
    if isinstance(ccount, int):
        for c in range(min(ccount, MAX_CONTROLLERS)):
            csec: dict[str, Any] = {"controller": c}
            ctrl = cx.rd("Item", lambda c=c: controllers.Item(c), into=csec, keep=False)
            heads = (
                cx.rd("SensorHeads", lambda ct=ctrl: ct.SensorHeads, into=csec, keep=False)
                if ctrl is not None
                else None
            )
            hcount = (
                cx.rd("SensorHeads_Count", lambda h=heads: h.Count, into=csec)
                if heads is not None
                else None
            )
            infos: list[dict[str, Any]] = []
            if heads is not None and isinstance(hcount, int):
                for h in range(min(hcount, MAX_SENSORHEADS)):
                    hsec: dict[str, Any] = {"sensorkopf": h}
                    head = cx.rd("Item", lambda h=h, hs=heads: hs.Item(h), into=hsec, keep=False)
                    info = (
                        cx.rd("SensorHeadInfo", lambda hd=head: hd.SensorHeadInfo, into=hsec,
                              keep=False)
                        if head is not None
                        else None
                    )  # fmt: skip
                    if info is not None:
                        cx.read_all(info, SENSORHEAD_PROPS, into=hsec)
                    infos.append(hsec)
            csec["sensorkoepfe"] = infos
            listing.append(csec)
    sec["controller"] = listing


def read_measpoints(cx: StepContext, infos: WhitelistProxy, max_points: int) -> None:
    """Liest Anzahl und wenige Messpunkte (Index/Label/Koordinaten); gemeinsam für 1 und 1b."""
    if cx.rd("HasMeasPoints", lambda: infos.HasMeasPoints) is not True:
        cx.hint = "Infos.HasMeasPoints ist nicht True."
        return
    pts = infos.MeasPoints
    count = cx.rd("Count", lambda: pts.Count)
    samples: list[dict[str, Any]] = []
    first_label: Any = None
    first_index: Any = None
    if isinstance(count, int):
        for i in sample_indices(count, max_points):
            sec: dict[str, Any] = {"item_position": i}
            point = cx.rd("Item", lambda i=i: pts.Item(i), into=sec, keep=False)
            if point is not None:
                values = cx.read_all(point, MEASPOINT_PROPS, into=sec)
                cx.rd("CoordXYZ", lambda p=point: p.CoordXYZ(), optional=True, into=sec)
                index = values.get("Index")
                if _is_int(index) and index != i:
                    cx.deviation(f"MeasPoints.Item({i}).Index = {index}, erwartet {i}", "I5 1.7")
                if first_label is None:
                    first_label, first_index = values.get("Label"), index
            samples.append(sec)
    cx.w["stichprobe"] = samples
    if first_label is not None:
        result = cx.rd("LabelToIndex_erstes_Label", lambda: pts.LabelToIndex(first_label))
        cx.w["LabelToIndex_label"] = first_label
        cx.w["LabelToIndex_index_des_punkts"] = first_index
        if _is_int(result) and _is_int(first_index) and result != first_index:
            cx.deviation(
                f"LabelToIndex({first_label!r}) = {result}, aber Index des Punkts = {first_index}",
                "I5 1.7",
            )
    cx.kern = f"MeasPoints.Count {count!r}"


def _step_messpunkte(cx: StepContext) -> None:
    read_measpoints(cx, _infos(cx), cx.args.max_punkte)


def _step_abgleich(cx: StepContext) -> None:
    infos = _infos(cx)
    if cx.rd("HasAlignments", lambda: infos.HasAlignments) is not True:
        cx.hint = "Infos.HasAlignments ist nicht True."
        return
    alignments = infos.Alignments
    for key, props in (("Alignments3D", ALIGN3D_PROPS), ("Alignments2D", ("Valid",))):
        sec: dict[str, Any] = cx.w.setdefault(key, {})
        coll = cx.rd(key, lambda k=key: getattr(alignments, k), optional=True, into=sec, keep=False)
        if coll is None:
            continue
        count = cx.rd("Count", lambda c=coll: c.Count, into=sec)
        items: list[dict[str, Any]] = []
        if isinstance(count, int):
            for i in range(1, min(count, MAX_ALIGNMENTS) + 1):
                item: dict[str, Any] = {"item": i}
                elem = cx.rd("Item", lambda i=i, c=coll: c.Item(i), into=item, keep=False)
                if elem is not None:
                    cx.read_all(elem, props, into=item)
                items.append(item)
        sec["eintraege"] = items
    cx.kern = f"3D-Abgleiche: {cx.w.get('Alignments3D', {}).get('Count')!r}"


def _step_existenz(cx: StepContext) -> None:
    infos = _infos(cx)
    cx.rd("HasPositionDevice", lambda: infos.HasPositionDevice)
    app = cx.need("app", "P1-5-verbinden")
    cx.rd("DigitalPorts_vorhanden", lambda: app.exists("DigitalPorts"), optional=True)
    cx.kern = (
        f"PositionDevice {cx.w.get('HasPositionDevice')!r}, "
        f"DigitalPorts {cx.w.get('DigitalPorts_vorhanden')!r}"
    )


# ---------------------------------------------------------------------------------------
# Stufe 1b: PolyFile, nur lesend (--datei)
# ---------------------------------------------------------------------------------------


def _step_datei_oeffnen(cx: StepContext) -> None:
    pf = cx.dispatch("PolyFile.PolyFile")
    pf.ReadOnly = True  # vor Open (I5 4.2); die einzige freigegebene Schreiboperation
    cx.w["ReadOnly_gesetzt"] = True
    path = str(cx.args.datei)
    try:
        pf.Open(path)
    except Exception as exc:
        cx.hint = (
            "Open fehlgeschlagen. Falls 'Sharing Violation': Datei darf nicht in PSV "
            "geöffnet sein (I5 4.2)."
        )
        cx.state["polyfile"] = pf
        raise RuntimeError(f"PolyFile.Open fehlgeschlagen: {_short_error(exc)}") from exc
    cx.state["polyfile"] = pf
    cx.state["polyfile_offen"] = True
    cx.rd("IsOpen", lambda: pf.IsOpen)
    cx.read_all(pf.Version, FILE_VERSION_PROPS, into=cx.w.setdefault("Version", {}))
    cx.read_all(pf.SummaryInfo, SUMMARY_PROPS, into=cx.w.setdefault("SummaryInfo", {}))
    infos = pf.Infos
    if cx.rd("HasHardware", lambda: infos.HasHardware) is True:
        cx.read_all(infos.Hardware, HARDWARE_PROPS, into=cx.w.setdefault("Hardware", {}))
    read_measpoints(cx, infos, cx.args.max_punkte)
    cx.kern = f"geöffnet, Programmversion {cx.w['Version'].get('ProgramVersionString')!r}"


def _step_datei_struktur(cx: StepContext) -> None:
    pf = cx.need("polyfile", "P1-10-oeffnen")
    if not cx.state.get("polyfile_offen"):
        raise Skipped("Datei ist nicht geöffnet.")
    domains = pf.GetPointDomains()
    count = cx.rd("Count", lambda: domains.Count)
    listing: list[dict[str, Any]] = []
    proxies: list[WhitelistProxy] = []
    if isinstance(count, int):
        for i in range(1, min(count, MAX_DOMAINS) + 1):
            sec: dict[str, Any] = {"item": i}
            dom = cx.rd("Item", lambda i=i: domains.Item(i), into=sec, keep=False)
            if dom is not None:
                cx.read_all(dom, ("Name", "Type"), into=sec)
                proxies.append(dom)
                listing.append(sec)
    cx.w["domaenen"] = listing
    if not proxies:
        raise Skipped("Keine Domäne lesbar.")
    # Domäne "FFT" bevorzugen, sonst die erste (Auswahl ist im Bericht markiert).
    pick = next((k for k, sec in enumerate(listing) if sec.get("Name") == "FFT"), 0)
    listing[pick]["gewaehlt_fuer_daten"] = True
    chosen = proxies[pick]
    cx.state["domaene"] = chosen
    channels = chosen.Channels
    ccount = cx.rd("Kanaele_Count", lambda: channels.Count)
    tree: list[dict[str, Any]] = []
    if isinstance(ccount, int):
        for c in range(1, min(ccount, MAX_CHANNELS) + 1):
            csec: dict[str, Any] = {"kanal": c}
            ch = cx.rd("Item", lambda c=c: channels.Item(c), into=csec, keep=False)
            if ch is not None:
                cx.rd("Name", lambda ch=ch: ch.Name, into=csec)
                display = _walk_signals(cx, ch, csec, deep=c == 1)
                if display is not None:
                    cx.state["display"] = display
            tree.append(csec)
    cx.w["kanaele"] = tree
    cx.kern = f"{count!r} Domäne(n), {ccount!r} Kanäle in der gewählten Domäne"


def _walk_signals(
    cx: StepContext, channel: WhitelistProxy, sec: dict[str, Any], *, deep: bool
) -> WhitelistProxy | None:
    signals = channel.Signals
    count = cx.rd("Signale_Count", lambda: signals.Count, into=sec)
    listing: list[dict[str, Any]] = []
    display: WhitelistProxy | None = None
    if isinstance(count, int):
        for s in range(1, min(count, MAX_SIGNALS) + 1):
            ssec: dict[str, Any] = {"signal": s}
            sig = cx.rd("Item", lambda s=s: signals.Item(s), into=ssec, keep=False)
            if sig is not None:
                cx.rd("Name", lambda sg=sig: sg.Name, into=ssec)
                if deep and s == 1:
                    display = _read_signal_detail(cx, sig, ssec)
            listing.append(ssec)
    sec["signale"] = listing
    return display


def _read_signal_detail(
    cx: StepContext, sig: WhitelistProxy, ssec: dict[str, Any]
) -> WhitelistProxy | None:
    desc = cx.rd("Description", lambda: sig.Description, optional=True, into=ssec, keep=False)
    if desc is not None:
        cx.read_all(desc, SIGNAL_DESC_PROPS, into=ssec)
        yaxis = cx.rd("YAxis", lambda: desc.YAxis, optional=True, into=ssec, keep=False)
        if yaxis is not None:
            cx.read_all(yaxis, YAXIS_PROPS, into=ssec.setdefault("YAxis_Werte", {}))
    displays = sig.Displays
    dcount = cx.rd("Displays_Count", lambda: displays.Count, into=ssec)
    shown: list[dict[str, Any]] = []
    best: WhitelistProxy | None = None
    if isinstance(dcount, int):
        for d in range(1, min(dcount, MAX_DISPLAYS) + 1):
            dsec: dict[str, Any] = {"display": d}
            disp = cx.rd("Item", lambda d=d: displays.Item(d), into=dsec, keep=False)
            if disp is not None:
                values = cx.read_all(disp, ("Name", "Type"), into=dsec)
                if best is None or values.get("Type") == 9:  # ptcDisplayRealImag, I5 8
                    best = disp
            shown.append(dsec)
    ssec["displays"] = shown
    return best


def _step_datei_daten(cx: StepContext) -> None:
    if not cx.state.get("polyfile_offen"):
        raise Skipped("Datei ist nicht geöffnet.")
    domain = cx.need("domaene", "P1-10-struktur")
    display = cx.need("display", "P1-10-struktur: kein Display gefunden")
    points = domain.DataPoints
    count = cx.rd("DataPoints_Count", lambda: points.Count)
    if not isinstance(count, int) or count < 1:
        raise Skipped("Keine Datenpunkte vorhanden.")
    first = points.Item(1)
    cx.rd("AverageCount", lambda: first.AverageCount)
    start = time.perf_counter()
    data = cx.rd("GetData", lambda: first.GetData(display, 0), keep=False)
    cx.w["GetData_dauer_s"] = round(time.perf_counter() - start, 4)
    if data is not None:
        cx.w["GetData_laenge"] = len(data)
        cx.w["GetData_erste_werte"] = [float(v) for v in data[: cx.args.max_werte]]
    axis = domain.GetXAxis(display)
    ax = cx.read_all(axis, XAXIS_PROPS, into=cx.w.setdefault("XAxis_Werte", {}))
    max_count = ax.get("MaxCount")
    mids: dict[str, Any] = {}
    cx.rd("0", lambda: axis.GetMidX(0), optional=True, into=mids)
    if _is_int(max_count) and max_count > 1:
        cx.rd("1", lambda: axis.GetMidX(1), optional=True, into=mids)
        last = max_count - 1
        cx.rd(str(last), lambda: axis.GetMidX(last), optional=True, into=mids)
    cx.w["GetMidX"] = mids
    cx.w["abgeleitet"] = _derive_axis(mids, ax, cx.w.get("GetData_laenge"), cx.state.get("fft"))
    cx.kern = f"GetData-Länge {cx.w.get('GetData_laenge')!r}, MaxCount {max_count!r}"


def _num(value: Any) -> float | None:
    return float(value) if isinstance(value, (int, float)) and not isinstance(value, bool) else None


def _derive_axis(
    mids: Mapping[str, Any], axis: Mapping[str, Any], length: Any, fft: Mapping[str, Any] | None
) -> dict[str, Any]:
    """Kennzahlen zur Frequenzachse (nur Zahlen, kein Urteil); Vergleich mit k*df (KONVENTIONEN)."""
    out: dict[str, Any] = {}
    mid0, mid1 = _num(mids.get("0")), _num(mids.get("1"))
    if mid0 is not None and mid1 is not None and mid1 != mid0:
        delta_f = mid1 - mid0
        out["delta_f_aus_achse_hz"] = delta_f
        out["mid0_durch_delta_f"] = mid0 / delta_f
    max_count = axis.get("MaxCount")
    if _is_int(length) and _is_int(max_count) and max_count > 0:
        out["datenlaenge_durch_maxcount"] = length / max_count
    if fft:
        out["hinweis_LIVE_PSV"] = (
            "Felder *_LIVE_PSV stammen aus der aktuellen PSV-Konfiguration (P1-6-eigenschaften), "
            "nicht aus der Datei; sie gelten nur, wenn die Datei mit denselben Einstellungen "
            "gemessen wurde."
        )
        res, bw, lines = _num(fft.get("SampleResolution")), _num(fft.get("Bandwidth")), _num(
            fft.get("Lines"))  # fmt: skip
        if res is not None and "delta_f_aus_achse_hz" in out and res != 0:
            out["rel_abw_delta_f_zu_SampleResolution_LIVE_PSV"] = (
                out["delta_f_aus_achse_hz"] / res - 1.0
            )
        if bw is not None and lines:
            out["Bandwidth_durch_Lines_hz_LIVE_PSV"] = bw / lines
    return out


def _step_datei_schliessen(cx: StepContext) -> None:
    pf = cx.state.get("polyfile")
    if pf is None or not cx.state.get("polyfile_offen"):
        raise Skipped("Keine geöffnete Datei zu schließen.")
    pf.Close()
    cx.state["polyfile_offen"] = False
    cx.rd("IsOpen_nach_Close", lambda: pf.IsOpen)
    cx.kern = "geschlossen"


# ---------------------------------------------------------------------------------------
# Zusammenfassung und Kommandozeile
# ---------------------------------------------------------------------------------------


def _cell(value: Any) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ").strip()


def render_summary(report: Mapping[str, Any]) -> str:
    """Erzeugt ``zusammenfassung.md`` ausschließlich aus dem Berichts-JSON."""
    steps: list[Mapping[str, Any]] = list(report.get("pruefpunkte", []))
    lauf = report.get("lauf", {})
    out = [
        f"# Erkundung {report.get('rechnername', '?')} ({report.get('zeitstempel_lokal', '?')})",
        "",
        f"- Lauf: **{lauf.get('status', '?')}** {lauf.get('hinweis', '')}".rstrip(),
        f"- Skript {report.get('skript_version')} (SHA-256 {report.get('skript_sha256')})",
        f"- Stufen: {', '.join(report.get('stufen', []))}; Zeitbedarf der Prüfpunkte: "
        f"{sum(float(s.get('dauer_s', 0.0)) for s in steps):.1f} s",
        "- Alle Prüfpunkte gelten als **am Gerät unbestätigt**, bis der Nutzer das Ergebnis "
        "bestätigt hat.",
        "",
    ]
    if report.get("verweigert"):
        out += [
            "## ACHTUNG: Zugriff verweigert",
            "",
            "Der Whitelist-Proxy hat Zugriffe blockiert. Das ist ein Befund (Skriptfehler):",
            "",
        ]
        out += [f"- `{d.get('pfad')}` [{d.get('op')}] bei {d.get('pruefpunkt')}" for d in
                report["verweigert"]]  # fmt: skip
        out.append("")
    out += [
        "## Prüfpunkte",
        "",
        "| ID | Stufe | Status | Dauer s | Kernwert | Auffälligkeiten |",
        "|---|---|---|---|---|---|",
    ]
    for s in steps:
        notes = "; ".join([str(s.get("hinweis", "")), *map(str, s.get("auffaelligkeiten", []))])
        out.append(
            f"| {s['id']} | {s.get('stufe')} | {s.get('status')} | {float(s.get('dauer_s', 0)):.2f}"
            f" | {_cell(s.get('kernwert', ''))} | {_cell(notes.strip('; '))} |"
        )
    out += ["", "## Abweichungen von der Erwartung (COM-Referenz I5)", ""]
    deviations = report.get("abweichungen", [])
    if deviations:
        out += [f"- {d['text']} ({d['pruefpunkt']}; {d['beleg_ref']})" for d in deviations]
    else:
        out.append("Keine festgestellt (soweit die Prüfpunkte gelaufen sind).")
    status = {s["id"]: s.get("status") for s in steps}
    out += [
        "",
        "## Offene Fragen und der Prüfpunkt, der sie beantworten kann",
        "",
        "| Frage | Prüfpunkt | Lauf des Prüfpunkts (nicht die Antwort) |",
        "|---|---|---|",
    ]
    out += [f"| {q} | {sid} | {status.get(sid, 'nicht ausgeführt')} |" for q, sid in OPEN_QUESTIONS]
    out += [
        "",
        "Die Werte stehen in `bericht.json`; das Skript bewertet sie nicht. Beobachtungen am "
        "Gerät (Dialoge, Laser, Spiegel) bitte separat notieren.",
        "",
    ]
    return "\n".join(out)


def build_parser() -> argparse.ArgumentParser:
    """Kommandozeile des Skripts."""
    parser = argparse.ArgumentParser(
        prog="erkundung.py",
        description="Erkundung des PSV-Messrechners (nur lesend). Siehe README.md.",
    )
    parser.add_argument(
        "--stufe",
        choices=("0", "1"),
        default="0",
        help="0: ohne COM; 1: zusätzlich COM lesend (führt Stufe 0 mit aus). Standard: 0.",
    )
    parser.add_argument(
        "--datei", help="Stufe 1b: vorhandene Messdatei, wird nur schreibgeschützt gelesen."
    )
    parser.add_argument(
        "--start-psv",
        action="store_true",
        help="PSV starten, falls es nicht läuft (verlangt eine Bestätigung mit JA).",
    )
    parser.add_argument("--out", help="Ordner, in dem der Ausgabeordner angelegt wird.")
    parser.add_argument(
        "--keep-user", action="store_true", help="Benutzernamen im Bericht NICHT entfernen."
    )
    parser.add_argument(
        "--timeout-s",
        type=float,
        default=DEFAULT_TIMEOUT_S,
        help=f"Watchdog je Prüfpunkt in Sekunden (Standard {DEFAULT_TIMEOUT_S:g}).",
    )
    parser.add_argument(
        "--max-punkte",
        type=int,
        default=DEFAULT_MAX_POINTS,
        help=f"Messpunkte am Anfang und am Ende (Standard {DEFAULT_MAX_POINTS}).",
    )
    parser.add_argument(
        "--max-werte",
        type=int,
        default=DEFAULT_MAX_VALUES,
        help=f"Datenwerte aus GetData im Bericht (Standard {DEFAULT_MAX_VALUES}).",
    )
    parser.add_argument("--version", action="version", version=f"erkundung {SCRIPT_VERSION}")
    return parser


def build_steps(stufe: str, with_file: bool) -> list[Step]:
    """Stellt die Prüfpunkte der gewählten Stufen zusammen."""
    steps = [
        Step("P1-1-umgebung", "0", "Windows, Python, Bitness", "I5 10 P1-1/P1-2", _step_umgebung),
        Step("P1-4-pywin32", "0", "pywin32 importierbar?", "I5 10 P1-4; 7.1", _step_pywin32),
        Step("P1-2-registry", "0", "ProgIDs, CLSID, Server", "I5 1.3; 10 P1-2", _step_registry),
        Step("P1-2-dateien", "0", "Serverdateien", "I5 7.3; 10 P1-2", _step_dateien),
        Step("P1-4-typelibs-registry", "0", "Typbibliotheken (Registry)", "I5 1.2; 10 P1-4",
             _step_typelibs_registry),
        Step("P1-3-verzeichnisse", "0", "Polytec-Verzeichnisse", "I5 10 P1-3", _step_verzeichnisse),
        Step("P1-5-prozess", "0", "Läuft PSV (Prozessliste)?", "I5 10 P1-5", _step_prozess),
    ]  # fmt: skip
    if stufe == "1":
        steps += [
            Step("P1-5-verbinden", "1", "Verbinden (ohne Start)", "I5 3.1; 10 P1-5",
                 _step_verbinden),
            Step("P1-5-application", "1", "Application: Version, Mode", "I5 3.1; 10 P1-5",
                 _step_application),
            Step("P1-6-zustand", "1", "Acquisition: Zustand, Laser", "I5 2.2; 10 P1-6, P3-4",
                 _step_zustand),
            Step("P1-6-eigenschaften", "1", "Eigenschaften-Gruppen, FFT", "I5 2.5, 2.6; 10 P1-5/6",
                 _step_eigenschaften),
            Step("P1-6-hardware", "1", "Hardware", "I5 2.8; 10 P1-6", _step_hardware),
            Step("P1-6-scankopf", "1", "Scankopf", "I5 2.8; 10 P1-6", _step_scankopf),
            Step("P1-6-vibrometer", "1", "Vibrometer/Controller", "I5 2.8; 10 P1-6",
                 _step_vibrometer),
            Step("P1-6-messpunkte", "1", "Messpunkte, Index/Label", "I5 1.7; 10 P1-6, P2-6, P2-12",
                 _step_messpunkte),
            Step("P1-6-abgleich", "1", "Abgleich (3D/2D)", "I5 2.7; 10 P1-6, P2-12",
                 _step_abgleich),
            Step("P3-2-existenz", "1", "PositionDevice, DigitalPorts (Existenz)", "I5 10 P3-2",
                 _step_existenz),
            # Zuletzt: win32com.client.constants wird erst nach dem Laden von
            # Typbibliotheks-Wrappern (frühestens beim Dispatch) gefüllt [ungeprüft].
            Step("P1-4-typelibs-com", "1", "EnumTlbs und Konstanten", "I5 10 P1-4; 8",
                 _step_typelibs_com),
        ]  # fmt: skip
        if with_file:
            steps += [
                Step("P1-10-oeffnen", "1b", "Datei schreibgeschützt öffnen", "I5 4.2; 10 P1-10",
                     _step_datei_oeffnen),
                Step("P1-10-struktur", "1b", "Domänen, Kanäle, Signale", "I5 4.3; 10 P1-10",
                     _step_datei_struktur),
                Step("P1-10-daten", "1b", "GetData und Frequenzachse", "I5 4.4; 10 P1-10",
                     _step_datei_daten),
                Step("P1-10-schliessen", "1b", "Datei schließen", "I5 4.2", _step_datei_schliessen),
            ]  # fmt: skip
    return steps


def create_out_dir(base: Path, host: str, now: dt.datetime) -> Path:
    """Legt einen neuen Ausgabeordner an; ein vorhandener wird nie wiederverwendet."""
    safe_host = re.sub(r"[^A-Za-z0-9._-]", "_", host) or "rechner"
    name = f"erkundung_{safe_host}_{now.strftime('%Y-%m-%d_%H%M%S')}"
    number = 1
    candidate = base / name
    while True:
        try:
            candidate.mkdir()
        except FileExistsError:
            number += 1
            candidate = base / f"{name}_{number}"
        else:
            return candidate


def _initial_report(
    env: Env, args: argparse.Namespace, argv: Sequence[str], redactor: Redactor
) -> dict[str, Any]:
    now = env.now()
    return {
        "schema_version": SCHEMA_VERSION,
        "skript_version": SCRIPT_VERSION,
        "skript_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "zeitstempel_lokal": now.isoformat(timespec="seconds"),
        "zeitstempel_utc": now.astimezone(dt.UTC).isoformat(timespec="seconds"),
        "rechnername": env.hostname,
        "benutzername_entfernt": redactor.active,
        "kommandozeile": list(argv),
        "stufen": (["0", "1"] if args.stufe == "1" else ["0"]) + (["1b"] if args.datei else []),
        "parameter": {
            "timeout_s": args.timeout_s,
            "max_punkte": args.max_punkte,
            "max_werte": args.max_werte,
            "start_psv": bool(args.start_psv),
            "datei": args.datei,
        },
        "lauf": {"status": "laeuft", "hinweis": ""},
        "umgebung": {},
        "pruefpunkte": [],
        "abweichungen": [],
        "whitelist_aufrufe": [],
        "verweigert": [],
        "dateien": {},
    }


def main(argv: Sequence[str] | None = None, env: Env | None = None, poll_s: float = 0.25) -> int:
    """Einstiegspunkt. Gibt den Exit-Code zurück (siehe Modul-Docstring)."""
    parser = build_parser()
    arguments = list(sys.argv[1:] if argv is None else argv)
    args = parser.parse_args(arguments)
    env = env if env is not None else build_env()
    if args.datei and args.stufe != "1":
        parser.error("--datei gehört zu Stufe 1b: bitte --stufe 1 --datei <Pfad> verwenden.")
    if args.start_psv and args.stufe != "1":
        parser.error("--start-psv wirkt nur in Stufe 1.")
    if args.timeout_s <= 0 or args.max_punkte < 1 or args.max_werte < 1:
        parser.error("--timeout-s, --max-punkte und --max-werte müssen positiv sein.")
    file_path: Path | None = None
    file_before: dict[str, Any] | None = None
    if args.datei:
        file_path = Path(args.datei).resolve()
        if not file_path.is_file():
            parser.error(f"Datei nicht gefunden: {args.datei}")
        args.datei = str(file_path)
        try:
            file_before = describe_file(file_path)
        except OSError as exc:
            parser.error(f"Datei nicht lesbar: {exc}")
    start_allowed = False
    if args.start_psv:
        try:
            answer = env.input_fn(
                "ACHTUNG: --start-psv startet PSV (Messsoftware, ggf. Hardware-Initialisierung). "
                "Zum Fortfahren JA eingeben: "
            )
        except EOFError:
            answer = ""
        start_allowed = answer.strip() == "JA"
    base = Path(args.out) if args.out else Path(__file__).resolve().parent
    base.mkdir(parents=True, exist_ok=True)
    out_dir = create_out_dir(base, env.hostname, env.now())
    redactor = Redactor(
        env.username, not args.keep_user, protected=[env.hostname], profile_dirs=env.profile_dirs
    )
    proxy_ctx = ProxyContext(allow_start=start_allowed)
    runner = Runner(env, args, out_dir, redactor, proxy_ctx, poll_s)
    runner.state["start_erlaubt"] = start_allowed
    runner.data.update(_initial_report(env, args, arguments, redactor))
    runner.say(f"erkundung {SCRIPT_VERSION}: Stufe {args.stufe}, Ausgabe in {out_dir}")
    runner.say(
        f"Nur Lesen. Watchdog {args.timeout_s:g} s je Prüfpunkt. Strg+C bricht ab "
        "(der Teilbericht bleibt erhalten)."
    )
    if args.start_psv and not start_allowed:
        runner.say("Start von PSV nicht bestätigt: --start-psv wird ignoriert.")
    runner.flush()
    if not runner.run_guarded(build_steps(args.stufe, file_path is not None)):
        return runner.exit_code
    if file_path is not None and file_before is not None:
        after = describe_file(file_path)
        runner.data["dateien"] = {
            "eingabedatei_vorher": file_before,
            "eingabedatei_nachher": after,
            "unveraendert": file_before == after,
        }
        if file_before != after:
            runner.say("!!! Eingabedatei hat sich verändert (Größe/Zeit/Hash)!")
    runner.data["lauf"] = {"status": "vollstaendig", "hinweis": ""}
    runner.flush()
    _calls, denied = proxy_ctx.snapshot()
    runner.say(f"Fertig. Ergebnis: {out_dir}")
    return EXIT_DENIED if denied else EXIT_OK


if __name__ == "__main__":  # pragma: no cover - Einstiegspunkt
    sys.exit(main())
