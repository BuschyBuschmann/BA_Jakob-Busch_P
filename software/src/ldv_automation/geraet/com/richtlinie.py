"""Produktiv-Richtlinie des COM-Adapters (Plan P2, Abschnitt 3.3; ADR-007).

Lesende Freigaben haben keine Wirkung auf das Gerät. Jede **schreibende** Operation steht
einzeln mit Nummer (S1-S9), Begründung und Prüfung in dieser Datei; jede hat einen eigenen
Test (``tests/geraet_com/test_geraet_com_richtlinie.py``).

S10 (Antwort auf ``MessageOccurred``) ist **nicht** freigegeben: Der Ereignisbetrieb
(``--ereignisse``) ist laut Streichliste (Plan P2, Abschnitt 8) das erste entfallende
Experiment und in U3 nicht umgesetzt.

:data:`NIE_KATALOG` ist ein **Testkatalog** (kein Schutzmechanismus): Jeder Eintrag muss
vom Proxy verweigert werden; der Schutz selbst ist Default deny.
"""

from __future__ import annotations

import math
import os.path
from collections.abc import Callable
from types import ModuleType
from typing import Any, TypeGuard

from ldv_automation.domaene.parameter import KATALOG, Parameterkatalog
from ldv_automation.geraet.com.konstanten import (
    AcqState,
    AverageType,
    ScanCaps,
    ScanMode,
    SettingsMask,
)
from ldv_automation.geraet.com.whitelist import (
    Mitglied,
    ProxyKontext,
    Richtlinie,
    Schreibrecht,
    WhitelistProxy,
)

PROGID_ACQUISITION_INSTANCE = "PSV.AcquisitionInstance"

ERLAUBTE_LADEBITS = (
    SettingsMask.ACQUISITION
    | SettingsMask.ALIGNMENT
    | SettingsMask.APS
    | SettingsMask.ALIGNMENT_2D
    | SettingsMask.ALIGNMENT_3D
)
"""Alle Bits der freigegebenen Gruppen (siehe :data:`LADEGRUPPEN`)."""

LADEGRUPPEN: tuple[SettingsMask, ...] = (
    SettingsMask.ACQUISITION,
    SettingsMask.ALIGNMENT,
    SettingsMask.APS,
    SettingsMask.ALIGNMENT_2D,
    SettingsMask.ALIGNMENT_3D,
)
"""Freigegebene ``PTCSettings``-Gruppen; eine Lademaske ist eine Vereinigung ganzer Gruppen
(``APS`` = 312 nur vollständig, keine Teilbits wie 8 oder 256). Ohne ``Camera`` (könnte
Optik bewegen, [Einschätzung]) und ohne ``Windows`` (Plan P2, S2, offene Frage Lademaske)."""

STANDARD_LADEMASKE = int(ERLAUBTE_LADEBITS)
"""Vorgabe: Acquisition, APS, Alignment, 2D- und 3D-Abgleich (Annahme Plan P2, 10)."""

MITTELUNG_MIN = 3
MITTELUNG_MAX = 10000
"""Bereich von ``AverageProperties.Count`` nach [BEM] (Untergrenze am Gerät offen)."""


# --- Hilfsprüfungen ------------------------------------------------------------------------


def _ist_int(wert: object) -> TypeGuard[int]:
    return isinstance(wert, int) and not isinstance(wert, bool)


def ganzzahl_oder_none(wert: object) -> int | None:
    """``int`` bzw. ganzzahliger ``float`` als ``int``; sonst (auch ``bool``) ``None``.

    COM kann Ganzzahlen als Double liefern; Adapter und S7 behandeln das gleich.
    """
    if isinstance(wert, bool):
        return None
    if isinstance(wert, int):
        return wert
    if isinstance(wert, float) and wert.is_integer():
        return int(wert)
    return None


def _ist_float(wert: object) -> bool:
    return isinstance(wert, float) and math.isfinite(wert)


def pfad_absolut(pfad: str, pfadmodul: ModuleType = os.path) -> bool:
    r"""Prüft, ob ``pfad`` absolut ist; unter Windows (``ntpath``) mit Laufwerk oder UNC.

    ``ntpath.isabs(r"\daten\x.svd")`` ist unter Python 3.11 ``True``, obwohl der Pfad vom
    aktuellen Laufwerk abhängt. Solche Pfade werden deshalb abgelehnt.
    """
    if not pfadmodul.isabs(pfad):
        return False
    if pfadmodul.__name__ == "ntpath":
        return bool(pfadmodul.splitdrive(pfad)[0])
    return True


def _normiert(pfad: str, pfadmodul: ModuleType) -> str:
    return str(pfadmodul.normcase(pfadmodul.realpath(pfad)))


def pfad_unter(pfad: str, wurzel: str, pfadmodul: ModuleType = os.path) -> bool:
    """Prüft, ob ``pfad`` (normalisiert, Links aufgelöst) echt unter ``wurzel`` liegt.

    Beide müssen absolut sein (siehe :func:`pfad_absolut`), sonst ``False``.
    """
    if not (pfad_absolut(pfad, pfadmodul) and pfad_absolut(wurzel, pfadmodul)):
        return False
    p, w = _normiert(pfad, pfadmodul), _normiert(wurzel, pfadmodul)
    try:
        return p != w and pfadmodul.commonpath([p, w]) == w
    except ValueError:  # z. B. verschiedene Laufwerke unter Windows
        return False


def _pfadtext(wert: object) -> str | None:
    if not isinstance(wert, str) or not wert or "\x00" in wert:
        return "erwartet einen nicht leeren Pfad (str)"
    if not pfad_absolut(wert):
        return "erwartet einen absoluten Pfad (unter Windows mit Laufwerk oder UNC)"
    return None


def _neue_datei_unter_wurzel(wert: object, kontext: ProxyKontext, endung: str) -> str | None:
    problem = _pfadtext(wert)
    if problem is not None:
        return problem
    assert isinstance(wert, str)
    if not wert.lower().endswith(endung):
        return f"Endung {endung} erwartet"
    if kontext.messdaten_wurzel is None:
        return "kein Messdaten-Wurzelordner konfiguriert"
    if not pfad_absolut(kontext.messdaten_wurzel):
        return "Messdaten-Wurzelordner ist kein absoluter Pfad mit Laufwerk"
    if not pfad_unter(wert, kontext.messdaten_wurzel):
        return "Pfad liegt nicht unter dem Messdaten-Wurzelordner"
    if kontext.existiert(wert):
        return "Datei existiert bereits (nie überschreiben)"
    return None


# --- S1: GetApplication ------------------------------------------------------------------


def pruefe_get_application(args: tuple[Any, ...], kontext: ProxyKontext) -> str | None:
    """S1: ``GetApplication(vbCreate[, timeout_ms])``; ``True`` nur mit ``--start-psv``."""
    if not 1 <= len(args) <= 2 or not isinstance(args[0], bool):
        return "erwartet (vbCreate: bool[, lTimeOut_ms: int])"
    if len(args) == 2 and not (_ist_int(args[1]) and args[1] > 0):
        return "lTimeOut_ms muss int > 0 sein"
    if args[0] and not kontext.start_erlaubt:
        return "Start von PSV (vbCreate=True) ist nicht freigegeben (--start-psv)"
    return None


# --- S2: Settings.Load -------------------------------------------------------------------


def pruefe_settings_load(args: tuple[Any, ...], kontext: ProxyKontext) -> str | None:
    """S2: ``Settings.Load(pfad, maske)``; ``.set``, existiert, Maske aus der Freigabe."""
    if not kontext.schreiben_erlaubt:
        return "Betriebsart erlaubt keine Schreibzugriffe"
    if len(args) != 2:
        return "erwartet (pfad: str, maske: int)"
    pfad, maske = args
    problem = _pfadtext(pfad)
    if problem is not None:
        return problem
    if not pfad.lower().endswith(".set"):
        return "nur Einstellungsdateien (.set)"
    if not kontext.existiert(pfad):
        return "Einstellungsdatei existiert nicht"
    if not lademaske_freigegeben(maske):
        return f"Lademaske {maske!r} nicht freigegeben (nur ganze Gruppen aus LADEGRUPPEN)"
    return None


def lademaske_freigegeben(maske: object) -> bool:
    """Prüft, ob ``maske`` eine nicht leere Vereinigung ganzer :data:`LADEGRUPPEN` ist."""
    if not _ist_int(maske) or maske <= 0:
        return False
    rest = maske
    for gruppe in LADEGRUPPEN:
        if maske & gruppe == gruppe:
            rest &= ~int(gruppe)
    return rest == 0


# --- S3/S4: FFT-Parameter ----------------------------------------------------------------


def _pruefe_katalog(
    katalog: Parameterkatalog, schluessel: str, wert: object, typ_ok: bool
) -> str | None:
    if not typ_ok:
        return f"falscher Typ {type(wert).__name__} für {schluessel}"
    try:
        katalog.spec(schluessel).pruefe(wert)
    except ValueError as exc:
        return str(exc)
    return None


def _schreiben(kontext: ProxyKontext) -> str | None:
    return None if kontext.schreiben_erlaubt else "Betriebsart erlaubt keine Schreibzugriffe"


WertPruefung = Callable[[object, ProxyKontext], "str | None"]


def bandbreiten_pruefung(katalog: Parameterkatalog) -> WertPruefung:
    """S3: ``Bandwidth`` (float, Bereich aus ``katalog``)."""

    def pruefe(wert: object, kontext: ProxyKontext) -> str | None:
        return _schreiben(kontext) or _pruefe_katalog(
            katalog, "fft.bandbreite_hz", wert, _ist_float(wert)
        )

    return pruefe


def linien_pruefung(katalog: Parameterkatalog) -> WertPruefung:
    """S3: ``Lines`` (int, Bereich aus ``katalog``)."""

    def pruefe(wert: object, kontext: ProxyKontext) -> str | None:
        return _schreiben(kontext) or _pruefe_katalog(katalog, "fft.linien", wert, _ist_int(wert))

    return pruefe


def pruefe_validator_uebernahme(wert: object, kontext: ProxyKontext) -> str | None:
    """S3: ``FftProperties.FftAcqPropertiesValidator = v`` nur mit eigenem Validator-Proxy."""
    if not kontext.schreiben_erlaubt:
        return "Betriebsart erlaubt keine Schreibzugriffe"
    if not (isinstance(wert, WhitelistProxy) and wert.typ == "FftValidator"):
        return "erwartet ein FftValidator-Objekt (über den Proxy gelesen)"
    return None


def _direkt(kontext: ProxyKontext) -> str | None:
    if not kontext.direkt_setzen_erlaubt:
        return "Rückfall S4 (direkte FFT-Properties) ist nicht eingeschaltet"
    return None


def nur_mit_rueckfall(pruefung: WertPruefung) -> WertPruefung:
    """S4: direkte ``FftProperties``-Zuweisung nur mit Rückfall-Schalter."""

    def pruefe(wert: object, kontext: ProxyKontext) -> str | None:
        return _direkt(kontext) or pruefung(wert, kontext)

    return pruefe


# --- S5: Mittelung -----------------------------------------------------------------------


def pruefe_mittelungstyp(wert: object, kontext: ProxyKontext) -> str | None:
    """S5: ``AverageProperties.Type`` aus ``PTCAverageType``."""
    if not kontext.schreiben_erlaubt:
        return "Betriebsart erlaubt keine Schreibzugriffe"
    if not _ist_int(wert) or wert not in {int(t) for t in AverageType}:
        return f"Mittelungsart {wert!r} nicht in PTCAverageType"
    return None


def pruefe_mittelungsanzahl(wert: object, kontext: ProxyKontext) -> str | None:
    """S5: ``AverageProperties.Count`` 3…10000 ([BEM])."""
    if not kontext.schreiben_erlaubt:
        return "Betriebsart erlaubt keine Schreibzugriffe"
    if not _ist_int(wert) or not MITTELUNG_MIN <= wert <= MITTELUNG_MAX:
        return f"Mittelungsanzahl {wert!r} außerhalb {MITTELUNG_MIN}…{MITTELUNG_MAX}"
    return None


# --- S6-S8: Messen -----------------------------------------------------------------------


def _messen(kontext: ProxyKontext) -> str | None:
    if not kontext.messen_erlaubt:
        return "Betriebsart erlaubt keine Messung"
    if not kontext.messfreigabe:
        return "keine Messfreigabe für diesen Durchgang"
    return None


def pruefe_scan_dateiname(wert: object, kontext: ProxyKontext) -> str | None:
    """S6: ``ScanFileName``: Messfreigabe, unter der Wurzel, existiert nicht, ``.svd``."""
    return _messen(kontext) or _neue_datei_unter_wurzel(wert, kontext, ".svd")


def pruefe_scan_ex(args: tuple[Any, ...], kontext: ProxyKontext) -> str | None:
    """S7: ``ScanEx(ptcScanAll, ptcScanCapsNone)``; State == Stopped unmittelbar davor."""
    problem = _messen(kontext)
    if problem is not None:
        return problem
    if (
        len(args) != 2
        or not all(_ist_int(a) for a in args)
        or args[0] != ScanMode.ALL
        or args[1] != ScanCaps.NONE
    ):
        return "nur ScanEx(ptcScanAll=0, ptcScanCapsNone=0) freigegeben"
    letzter = kontext.letzter_aufruf
    if (
        letzter is None
        or letzter[:2] != ("Acquisition.State", "get")
        or ganzzahl_oder_none(letzter[2]) != AcqState.STOPPED
    ):
        return "Acquisition.State == Stopped wurde nicht unmittelbar davor geprüft"
    return None


def _merke_eigene_messung(kontext: ProxyKontext) -> None:
    # Vor dem Aufruf gesetzt: Scheitert ScanEx mit Ausnahme, kann der Scan trotzdem laufen;
    # Stop gilt dann einem von uns angestoßenen Scan.
    kontext.eigene_messung_aktiv = True


def pruefe_stop(args: tuple[Any, ...], kontext: ProxyKontext) -> str | None:
    """S8: ``Stop()`` nur, wenn diese Sitzung den Scan gestartet hat."""
    if not kontext.messen_erlaubt:
        return "Betriebsart erlaubt keine Messung"
    if args:
        return "keine Argumente erlaubt"
    if not kontext.eigene_messung_aktiv:
        return "keine eigene Messung aktiv (fremde Messung wird nie gestoppt)"
    return None


# --- S9: Settings.Save -------------------------------------------------------------------


def pruefe_settings_save(args: tuple[Any, ...], kontext: ProxyKontext) -> str | None:
    """S9: ``Settings.Save(pfad)``: unter der Wurzel, existiert nicht, ``.set``."""
    if not kontext.schreiben_erlaubt:
        return "Betriebsart erlaubt keine Schreibzugriffe"
    if len(args) != 1:
        return "erwartet (pfad: str)"
    return _neue_datei_unter_wurzel(args[0], kontext, ".set")


# --- Richtlinie --------------------------------------------------------------------------


def _lesen(*namen: str) -> dict[str, Mitglied]:
    return {n: Mitglied(zugriff="get") for n in namen}


def _objekt(typ: str) -> Mitglied:
    return Mitglied(zugriff="get", liefert=typ)


def _pruefe_index(args: tuple[Any, ...], kontext: ProxyKontext) -> str | None:
    if len(args) == 1 and _ist_int(args[0]) and args[0] >= 1:
        return None
    return "erwartet genau einen 1-basierten Index (int >= 1)"


def _element(typ: str) -> Mitglied:
    return Mitglied(zugriff="call", liefert=typ, pruefung=_pruefe_index)


FFT_LESEN = (
    "Bandwidth",
    "StartFrequency",
    "EndFrequency",
    "Lines",
    "Overlap",
    "SampleFrequency",
    "SampleResolution",
    "SampleTime",
)
HAS_LESEN = (
    "HasGeneralProperties",
    "HasAverageProperties",
    "HasFftProperties",
    "HasChannelsProperties",
    "HasGeneratorsProperties",
    "HasTriggerProperties",
    "HasSignalEnhancementProperties",
)
ALLGEMEIN_LESEN = (
    "AutoRemeasure",
    "AutoRemeasureAutoRange",
    "SaveTimeDataForScan",
    "PrincipalComponentAnalysis",
)
TRIGGER_LESEN = ("Source", "Edge", "Level", "PreTrigger", "PhaseFromRef", "AnalogSourceChannel")
SE_LESEN = ("Mode", "SpeckleTracking")
KANAL_LESEN = (
    "Name",
    "Active",
    "Reference",
    "Quantity",
    "Unit",
    "InputRange",
    "Calibration",
    "DirectionOfVibration",
    "WindowFunction",
)
HARDWARE_LESEN = (
    "AcqBoardName",
    "AcqBoardFirmwareVersion",
    "FrontEnd",
    "FrontEndFirmwareVersion",
    "GeneratorName",
    "ScanHeadType",
    "SensorHeadNames",
    "SensorHeadSerialNumbers",
    "SensorHeadVersions",
)


def erstelle_richtlinie(katalog: Parameterkatalog = KATALOG) -> Richtlinie:
    """Produktiv-Richtlinie; Wertebereiche von S3/S4 aus ``katalog`` (Adapterkonfiguration)."""
    bandbreite = bandbreiten_pruefung(katalog)
    linien = linien_pruefung(katalog)
    return _richtlinie(bandbreite, linien)


def _richtlinie(pruefe_bandbreite: WertPruefung, pruefe_linien: WertPruefung) -> Richtlinie:
    return Richtlinie(
        objekte={
            "AcquisitionInstance": {
                "IsRunning": Mitglied(zugriff="get"),
                "GetApplication": Mitglied(
                    zugriff="call",
                    liefert="Application",
                    pruefung=pruefe_get_application,
                    begruendung="S1: Verbinden; Start von PSV nur mit --start-psv und JA",
                ),
            },
            "Application": {
                **_lesen("Version", "Mode", "SuppressMessagesForAutomation", "WarningLevel"),
                "Acquisition": _objekt("Acquisition"),
                "Settings": _objekt("Settings"),
            },
            "Settings": {
                "Load": Mitglied(
                    zugriff="call",
                    pruefung=pruefe_settings_load,
                    begruendung="S2: R-011, Messung beruht auf einer Einstellungsdatei",
                ),
                "Save": Mitglied(
                    zugriff="call",
                    pruefung=pruefe_settings_save,
                    begruendung="S9: Nachweis der übernommenen Einstellungen (R-020, optional)",
                ),
            },
            "Acquisition": {
                **_lesen("State", "Mode", "ScanFileName", "GeneratorsOn"),
                "ActiveProperties": _objekt("AcquisitionProperties"),
                "Infos": _objekt("Infos"),
                "ScanEx": Mitglied(
                    zugriff="call",
                    pruefung=pruefe_scan_ex,
                    vor_aufruf=_merke_eigene_messung,
                    begruendung="S7: R-001, Scan starten",
                ),
                "Stop": Mitglied(
                    zugriff="call",
                    pruefung=pruefe_stop,
                    begruendung="S8: R-018 Abbruch und Zeitlimit, nur eigene Messung",
                ),
            },
            "AcquisitionProperties": {
                **_lesen(*HAS_LESEN),
                "FftProperties": _objekt("FftProperties"),
                "AverageProperties": _objekt("AverageProperties"),
                "GeneralProperties": _objekt("GeneralProperties"),
                "TriggerProperties": _objekt("TriggerProperties"),
                "SignalEnhancementProperties": _objekt("SEProperties"),
                "ChannelsProperties": _objekt("ChannelsProperties"),
                "GeneratorsProperties": _objekt("GeneratorsProperties"),
            },
            "FftProperties": {
                **_lesen(*FFT_LESEN),
                "FftAcqPropertiesValidator": _objekt("FftValidator"),
            },
            "FftValidator": _lesen(
                "AvailableBandwidths",
                "AvailableLines",
                "Bandwidth",
                "Lines",
                "StartFrequency",
                "EndFrequency",
            ),
            "AverageProperties": _lesen("Type", "Count"),
            "GeneralProperties": _lesen(*ALLGEMEIN_LESEN),
            "TriggerProperties": _lesen(*TRIGGER_LESEN),
            "SEProperties": _lesen(*SE_LESEN),
            "ChannelsProperties": {"Count": Mitglied(zugriff="get"), "Item": _element("Channel")},
            "Channel": _lesen(*KANAL_LESEN),
            "GeneratorsProperties": {
                "Count": Mitglied(zugriff="get"),
                "Item": _element("Generator"),
            },
            "Generator": {**_lesen("Active", "Amplitude"), "Waveform": _objekt("Waveform")},
            "Waveform": _lesen("Type", "Name"),
            "Infos": {
                **_lesen("HasHardware", "HasMeasPoints"),
                "Hardware": _objekt("Hardware"),
                "MeasPoints": _objekt("MeasPoints"),
            },
            "Hardware": _lesen(*HARDWARE_LESEN),
            "MeasPoints": _lesen("Count"),
        },
        schreiben={
            "FftValidator": {
                "Bandwidth": Schreibrecht(
                    pruefung=pruefe_bandbreite, begruendung="S3: R-011, nur Staging im Validator"
                ),
                "Lines": Schreibrecht(
                    pruefung=pruefe_linien, begruendung="S3: R-011, nur Staging im Validator"
                ),
            },
            "FftProperties": {
                "FftAcqPropertiesValidator": Schreibrecht(
                    pruefung=pruefe_validator_uebernahme,
                    begruendung="S3: R-011, atomare Übernahme des Validators",
                ),
                "Bandwidth": Schreibrecht(
                    pruefung=nur_mit_rueckfall(pruefe_bandbreite),
                    begruendung="S4: Rückfall ohne Validator (ADR-005)",
                ),
                "Lines": Schreibrecht(
                    pruefung=nur_mit_rueckfall(pruefe_linien),
                    begruendung="S4: Rückfall ohne Validator (ADR-005)",
                ),
            },
            "AverageProperties": {
                "Type": Schreibrecht(pruefung=pruefe_mittelungstyp, begruendung="S5: R-011"),
                "Count": Schreibrecht(pruefung=pruefe_mittelungsanzahl, begruendung="S5: R-011"),
            },
            "Acquisition": {
                "ScanFileName": Schreibrecht(
                    pruefung=pruefe_scan_dateiname,
                    begruendung="S6: R-001; leer würde PSV per Dialog fragen",
                ),
            },
        },
        existenz={"FftProperties": frozenset({"FftAcqPropertiesValidator"})},
        einstieg={PROGID_ACQUISITION_INSTANCE: "AcquisitionInstance"},
    )


PRODUKTIV = erstelle_richtlinie(KATALOG)
"""Produktiv-Richtlinie mit dem Standardkatalog."""


def _aufrufe(typ: str, *namen: str) -> list[tuple[str, str, str, Any]]:
    return [(typ, n, "call", None) for n in namen]


NIE_KATALOG: tuple[tuple[str, str, str, Any], ...] = (
    # Start, Scan ohne Ex, andere Scanmodi bzw. Optionen
    *_aufrufe("Acquisition", "Start", "Scan"),
    ("Acquisition", "ScanEx", "args", (int(ScanMode.CONTINUE), 0)),
    ("Acquisition", "ScanEx", "args", (int(ScanMode.REMEASURE), 0)),
    ("Acquisition", "ScanEx", "args", (int(ScanMode.REMEASURE_AUTO_RANGE), 0)),
    ("Acquisition", "ScanEx", "args", (int(ScanMode.REMEASURE_FILE), 0)),
    ("Acquisition", "ScanEx", "args", (0, int(ScanCaps.USE_ASSIGNED_FOCUS_VALUES_DURING_SCAN))),
    ("Acquisition", "ScanEx", "args", (0, int(ScanCaps.VIDEO_TRIANGULATION))),
    ("Acquisition", "ScanEx", "args", (0, int(ScanCaps.VIDEO_TRIANGULATION_FAST))),
    ("Acquisition", "ScanEx", "args", (0, int(ScanCaps.ASYNCHRONOUS_SCAN_EVENT))),
    ("Acquisition", "ScanEx", "args", (0, int(ScanCaps.AUTO_FOCUS_DURING_SCAN))),
    # Laser, Fokus, Geometrie, Punktauswahl
    *_aufrufe(
        "Acquisition",
        "SetLaserOn",
        "AutoFocusLaser",
        "AssignFocusAutomatically",
        "GeometryScan",
        "SetSelectedMeasPoints",
    ),
    # Generator
    ("Acquisition", "GeneratorsOn", "set", True),
    ("Acquisition", "GeneratorsOn", "set", False),
    ("Generator", "Active", "set", True),
    ("Generator", "Amplitude", "set", 0.1),
    ("Generator", "Offset", "set", 0.0),
    ("Generator", "Waveform", "set", None),
    ("Waveform", "Type", "set", 0),
    # Modus und Application-Einstellungen
    ("Acquisition", "Mode", "set", 1),
    ("Application", "Mode", "set", 1),
    ("Application", "SuppressMessagesForAutomation", "set", True),
    ("Application", "WarningLevel", "set", 0),
    # Dateien, Dokumente, Export, Beenden
    *_aufrufe("Settings", "Delete"),
    ("Application", "Documents", "get", None),
    ("Application", "Exporter", "get", None),
    *_aufrufe("Application", "Quit", "QuitEx"),
    # Positioniereinheit, Digitalports, Abgleich
    ("Infos", "PositionDevice", "get", None),
    *_aufrufe("PositionDevice", "StartMove", "StartMoveRelative", "StartMoveAbsolute"),
    ("Application", "DigitalPorts", "get", None),
    *_aufrufe("Alignment3D", "Calculate"),
    # Service- und Kalibriermethoden des Scankopfs
    *_aufrufe(
        "ScanHeadControl",
        "WriteFocusDataFactorySettings",
        "WriteFocusDataFocalLength",
        "WriteFocusDataInfinitePos",
        "WriteLaserIntensityData",
        "WriteMirrorAdjustmentData",
    ),
    # PolyFile (jede Schreiboperation; schon das Einstiegsobjekt ist nicht freigegeben)
    ("Dispatch", "PolyFile.PolyFile", "dispatch", None),
    *_aufrufe("PolyFile", "Save", "SaveAs", "SaveAsEx", "Create"),
    ("PolyFile", "ReadOnly", "set", False),
    # Mittelung/FFT außerhalb des Bereichs bzw. direkt ohne Schalter: siehe S3-S5-Tests
)
"""Testkatalog „Nie freigegeben“ (Plan P2, 3.3). Operation ``"args"`` heißt: Methode ist
freigegeben, aber genau diese Argumente nicht."""


def schreibbegruendungen() -> dict[str, str]:
    """Alle schreibenden Operationen mit Begründung (für Tests und Dokumentation)."""
    ergebnis: dict[str, str] = {}
    for typ, mitglieder in PRODUKTIV.objekte.items():
        for name, m in mitglieder.items():
            if m.zugriff == "call" and m.begruendung:
                ergebnis[f"{typ}.{name}"] = m.begruendung
    for typ, rechte in PRODUKTIV.schreiben.items():
        for name, r in rechte.items():
            ergebnis[f"{typ}.{name}="] = r.begruendung
    return ergebnis
