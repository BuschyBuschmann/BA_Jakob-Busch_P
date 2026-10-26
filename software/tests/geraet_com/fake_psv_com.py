"""COM-Fake der PSV-Software für Adapter- und Proxy-Tests (nur Tests, Plan P2 5.3).

Vorlage ist der Fake des Erkundungswerkzeugs (``tests/tools/erkundung/fake_psv.py``), als
Kopie und erweitert um schreibende Abläufe (kein Import, ADR-009). Jeder Zugriff auf einen
Fake-Knoten steht in ``Welt.log``, unabhängig vom Aufrufprotokoll des Proxys.

Nachgebildet (Werte nach I5): Zustände, Scan per ``ScanEx`` mit Polling-Ende, ``Stop``,
Validator mit Einrasten, fehlender Validator, ``Settings.Load/Save``, COM-Ausnahmen mit
``hresult``/``excepinfo``, hängende Aufrufe.
"""

from __future__ import annotations

import threading
from collections.abc import Callable
from dataclasses import dataclass, field
from typing import Any


class FakeComError(Exception):
    """Ersatz für ``pywintypes.com_error`` (``hresult``, ``excepinfo``, ``strerror``)."""

    def __init__(self, message: str = "Fehler", hresult: int = -2147352567) -> None:
        super().__init__(message)
        self.hresult = hresult
        self.excepinfo = (0, "PSV", message, None, 0, hresult)
        self.strerror = "Ausnahmefehler aufgetreten."


@dataclass
class Welt:
    """Gemeinsamer Zustand: Zugriffsprotokoll, Dateien, Fehlerinjektion, Blockaden."""

    log: list[tuple[str, str, str, tuple[Any, ...]]] = field(default_factory=list)
    dateien: set[str] = field(default_factory=set)
    fehler: dict[tuple[str, str], Exception] = field(default_factory=dict)
    blockiert: dict[tuple[str, str], threading.Event] = field(default_factory=dict)
    blockade_erreicht: threading.Event = field(default_factory=threading.Event)
    dispatches: list[str] = field(default_factory=list)

    def ops(self) -> list[str]:
        """Protokoll als ``Typ.Name:op``."""
        return [f"{k}.{n}:{o}" for k, n, o, _ in self.log]

    def schreibende(self) -> list[str]:
        """Nur Zuweisungen und Methodenaufrufe (ohne Lesen)."""
        return [f"{k}.{n}:{o}" for k, n, o, _ in self.log if o != "get"]


class _Ole:
    def __init__(self, knoten: FakeKnoten) -> None:
        self._knoten = knoten

    def GetIDsOfNames(self, name: str) -> tuple[int, ...]:  # noqa: N802 - COM-Name
        if name in self._knoten._bekannt():
            return (1,)
        raise FakeComError(f"Unbekannter Name {name}", hresult=-2147352570)


class FakeKnoten:
    """Generisches COM-Objekt mit Properties, dynamischen Gettern/Settern und Methoden."""

    def __init__(
        self,
        typ: str,
        welt: Welt,
        props: dict[str, Any] | None = None,
        methoden: dict[str, Callable[..., Any]] | None = None,
        getter: dict[str, Callable[[], Any]] | None = None,
        setter: dict[str, Callable[[Any], None]] | None = None,
    ) -> None:
        object.__setattr__(self, "_typ", typ)
        object.__setattr__(self, "_welt", welt)
        object.__setattr__(self, "_props", dict(props or {}))
        object.__setattr__(self, "_methoden", dict(methoden or {}))
        object.__setattr__(self, "_getter", dict(getter or {}))
        object.__setattr__(self, "_setter", dict(setter or {}))

    def _bekannt(self) -> set[str]:
        return set(self._props) | set(self._methoden) | set(self._getter) | set(self._setter)

    @property
    def _oleobj_(self) -> _Ole:
        return _Ole(self)

    def _betrete(self, name: str, op: str, args: tuple[Any, ...]) -> None:
        welt: Welt = self._welt
        welt.log.append((self._typ, name, op, args))
        ereignis = welt.blockiert.get((self._typ, name))
        if ereignis is not None:
            welt.blockade_erreicht.set()
            ereignis.wait(timeout=10)
        fehler = welt.fehler.get((self._typ, name))
        if fehler is not None:
            raise fehler

    def __getattr__(self, name: str) -> Any:
        if name in self._getter:
            self._betrete(name, "get", ())
            return self._getter[name]()
        if name in self._props:
            self._betrete(name, "get", ())
            return self._props[name]
        if name in self._methoden:
            methode = self._methoden[name]

            def aufruf(*args: Any) -> Any:
                self._betrete(name, "call", args)
                return methode(*args)

            return aufruf
        raise AttributeError(name)

    def __setattr__(self, name: str, value: Any) -> None:
        self._betrete(name, "set", (value,))
        if name in self._setter:
            self._setter[name](value)
        else:
            self._props[name] = value


def _naechster(werte: tuple[Any, ...], wert: Any) -> Any:
    return min(werte, key=lambda w: abs(w - wert))


@dataclass
class FakePsv:
    """Zugriff auf die Knoten des Fakes und auf seinen Scan-Zustand."""

    welt: Welt
    inst: FakeKnoten
    app: FakeKnoten
    acq: FakeKnoten
    settings: FakeKnoten
    props: FakeKnoten
    fft: FakeKnoten
    avg: FakeKnoten
    zustand: int = 0
    scan_rest: int = 0
    stop_wirkt: bool = True
    scan_polls: int = 2
    geladen: list[tuple[str, int]] = field(default_factory=list)
    gespeichert: list[str] = field(default_factory=list)
    gestartet: bool = False


def baue_psv(
    welt: Welt,
    *,
    laeuft: bool = True,
    zustand: int = 0,
    app_modus: int = 1,
    unterdrueckt: bool = True,
    validator: bool = True,
    scan_polls: int = 2,
    hardware: bool = True,
    bandbreiten_hz: tuple[float, ...] = (1250.0, 2500.0, 5000.0, 6250.0, 10000.0),
    linien: tuple[int, ...] = (100, 200, 400, 800, 1600, 3200),
    dateiname_echo: Callable[[str], str] | None = None,
) -> FakePsv:
    """Baut einen Fake-PSV im Erfassungsmodus (FFT), Werte nach I5 Abschnitt 2/8."""
    fft_werte: dict[str, Any] = {
        "Bandwidth": 5000.0,
        "StartFrequency": 0.0,
        "EndFrequency": 5000.0,
        "Lines": 400,
        "Overlap": 0.0,
        "SampleFrequency": 12500.0,
        "SampleResolution": 12.5,
        "SampleTime": 0.08,
    }

    def validator_neu() -> FakeKnoten:
        staging = {"Bandwidth": fft_werte["Bandwidth"], "Lines": fft_werte["Lines"]}

        def setze_bw(wert: float) -> None:
            staging["Bandwidth"] = _naechster(bandbreiten_hz, wert)

        def setze_linien(wert: int) -> None:
            staging["Lines"] = _naechster(linien, wert)

        return FakeKnoten(
            "FftValidator",
            welt,
            props={"AvailableBandwidths": bandbreiten_hz, "AvailableLines": linien},
            getter={"Bandwidth": lambda: staging["Bandwidth"], "Lines": lambda: staging["Lines"]},
            setter={"Bandwidth": setze_bw, "Lines": setze_linien},
        )

    def uebernehme(v: FakeKnoten) -> None:
        fft_werte["Bandwidth"] = v.Bandwidth
        fft_werte["Lines"] = v.Lines

    def setze_fft(name: str, raster: tuple[Any, ...]) -> Callable[[Any], None]:
        def setzen(wert: Any) -> None:
            fft_werte[name] = _naechster(raster, wert)

        return setzen

    def lies_fft(name: str) -> Callable[[], Any]:
        return lambda: fft_werte[name]

    fft_getter: dict[str, Callable[[], Any]] = {n: lies_fft(n) for n in fft_werte}
    fft_setter: dict[str, Callable[[Any], None]] = {
        "Bandwidth": setze_fft("Bandwidth", bandbreiten_hz),
        "Lines": setze_fft("Lines", linien),
    }
    if validator:
        fft_getter["FftAcqPropertiesValidator"] = validator_neu
        fft_setter["FftAcqPropertiesValidator"] = uebernehme
    fft = FakeKnoten("FftProperties", welt, getter=fft_getter, setter=fft_setter)

    mittel: dict[str, Any] = {"Type": 2, "Count": 10}

    def setze_anzahl(wert: int) -> None:
        if not 3 <= wert <= 10000:
            raise FakeComError("Der Wert liegt außerhalb des gültigen Bereichs.")
        mittel["Count"] = wert

    def setze_typ(wert: int) -> None:
        mittel["Type"] = wert

    avg = FakeKnoten(
        "AverageProperties",
        welt,
        getter={"Type": lambda: mittel["Type"], "Count": lambda: mittel["Count"]},
        setter={"Type": setze_typ, "Count": setze_anzahl},
    )
    general = FakeKnoten(
        "GeneralProperties",
        welt,
        {
            "AutoRemeasure": False,
            "AutoRemeasureAutoRange": False,
            "SaveTimeDataForScan": False,
            "PrincipalComponentAnalysis": False,
        },
    )
    trigger = FakeKnoten(
        "TriggerProperties",
        welt,
        {
            "Source": 0,
            "Edge": 0,
            "Level": 10.0,
            "PreTrigger": 0.0,
            "PhaseFromRef": True,
            "AnalogSourceChannel": 1,
        },
    )
    se = FakeKnoten("SEProperties", welt, {"Mode": 0, "SpeckleTracking": False})
    kanal_werte = {
        "Active": True,
        "Reference": False,
        "Quantity": 13,
        "Unit": "m/s",
        "InputRange": 10.0,
        "Calibration": 0.05,
        "DirectionOfVibration": 6,
        "WindowFunction": 7,
    }
    kanaele_liste = [
        FakeKnoten("Channel", welt, {"Name": f"Vib {i}", **kanal_werte}) for i in (1, 2)
    ]

    def kanal(index: int) -> FakeKnoten:
        return kanaele_liste[index - 1]

    kanaele = FakeKnoten("ChannelsProperties", welt, {"Count": 2}, {"Item": kanal})
    waveform = FakeKnoten("Waveform", welt, {"Type": 7, "Name": "Periodic Chirp"})
    generator = FakeKnoten(
        "Generator", welt, {"Active": False, "Amplitude": 0.5, "Waveform": waveform}
    )
    generatoren = FakeKnoten(
        "GeneratorsProperties", welt, {"Count": 1}, {"Item": lambda i: generator}
    )
    props = FakeKnoten(
        "AcquisitionProperties",
        welt,
        {
            "HasGeneralProperties": True,
            "HasAverageProperties": True,
            "HasFftProperties": True,
            "HasChannelsProperties": True,
            "HasGeneratorsProperties": True,
            "HasTriggerProperties": True,
            "HasSignalEnhancementProperties": True,
            "FftProperties": fft,
            "AverageProperties": avg,
            "GeneralProperties": general,
            "TriggerProperties": trigger,
            "SignalEnhancementProperties": se,
            "ChannelsProperties": kanaele,
            "GeneratorsProperties": generatoren,
        },
    )
    hw = FakeKnoten(
        "Hardware",
        welt,
        {
            "AcqBoardName": "PCI-4461",
            "AcqBoardFirmwareVersion": "1.0",
            "FrontEnd": 124,
            "FrontEndFirmwareVersion": "2.1",
            "GeneratorName": "Gen",
            "ScanHeadType": 23,
            "SensorHeadNames": ("Top", "Left", "Right"),
            "SensorHeadSerialNumbers": ("1", "2", "3"),
            "SensorHeadVersions": ("a", "b", "c"),
        },
    )
    messpunkte = FakeKnoten("MeasPoints", welt, {"Count": 9})
    infos = FakeKnoten(
        "Infos",
        welt,
        {"HasHardware": hardware, "Hardware": hw, "HasMeasPoints": True, "MeasPoints": messpunkte},
    )
    psv_ref: list[FakePsv] = []

    def state() -> int:
        psv = psv_ref[0]
        if psv.zustand == 3 and psv.scan_rest > 0:
            psv.scan_rest -= 1
            if psv.scan_rest == 0:
                psv.zustand = 0
        return psv.zustand

    def scan_ex(modus: int, caps: int) -> None:
        psv = psv_ref[0]
        psv.zustand = 3
        psv.scan_rest = psv.scan_polls
        welt.dateien.add(acq_werte["ScanFileName"])

    def stop() -> None:
        psv = psv_ref[0]
        if psv.stop_wirkt:
            psv.zustand = 0

    acq_werte: dict[str, Any] = {"ScanFileName": "", "Mode": 1, "GeneratorsOn": False}

    def setze_dateiname(wert: str) -> None:
        acq_werte["ScanFileName"] = dateiname_echo(wert) if dateiname_echo else wert

    acq = FakeKnoten(
        "Acquisition",
        welt,
        {"ActiveProperties": props, "Infos": infos},
        {"ScanEx": scan_ex, "Stop": stop},
        getter={
            "State": state,
            "ScanFileName": lambda: acq_werte["ScanFileName"],
            "Mode": lambda: acq_werte["Mode"],
            "GeneratorsOn": lambda: acq_werte["GeneratorsOn"],
        },
        setter={"ScanFileName": setze_dateiname},
    )

    def load(pfad: str, maske: int) -> None:
        psv_ref[0].geladen.append((pfad, maske))

    def save(pfad: str) -> None:
        psv_ref[0].gespeichert.append(pfad)
        welt.dateien.add(pfad)

    settings = FakeKnoten("Settings", welt, methoden={"Load": load, "Save": save})
    app = FakeKnoten(
        "Application",
        welt,
        {
            "Version": "10.4.0.0-FAKE",
            "Mode": app_modus,
            "SuppressMessagesForAutomation": unterdrueckt,
            "WarningLevel": 1,
            "Acquisition": acq,
            "Settings": settings,
        },
    )

    def get_application(erzeugen: bool, zeitlimit_ms: int = 10000) -> FakeKnoten:
        if erzeugen:
            psv_ref[0].gestartet = True
        return app

    inst = FakeKnoten(
        "AcquisitionInstance", welt, {"IsRunning": laeuft}, {"GetApplication": get_application}
    )
    psv = FakePsv(
        welt=welt,
        inst=inst,
        app=app,
        acq=acq,
        settings=settings,
        props=props,
        fft=fft,
        avg=avg,
        zustand=zustand,
        scan_polls=scan_polls,
    )
    psv_ref.append(psv)
    return psv


class FakeBindung:
    """Attrappe der :class:`ComBindung`: Prozessprüfung und ``Dispatch`` gegen den Fake.

    ``prozess``: ``True`` = PSV-Treffer, ``False`` = keiner, ``None`` = nicht ermittelbar,
    oder ein Tupel von Abbildnamen. ``fehler`` ordnet Methodennamen eine Ausnahme zu.
    """

    def __init__(self, psv: FakePsv, *, prozess: bool | tuple[str, ...] | None = True) -> None:
        self.psv = psv
        self.prozess = prozess
        self.init = 0
        self.ende = 0
        self.fehler: dict[str, Exception] = {}
        self.beim_aufruf: Callable[[str], None] | None = None

    def _betrete(self, name: str) -> None:
        if self.beim_aufruf is not None:
            self.beim_aufruf(name)
        if name in self.fehler:
            raise self.fehler[name]

    def initialisiere_thread(self) -> None:
        self._betrete("initialisiere_thread")
        self.init += 1

    def beende_thread(self) -> None:
        self._betrete("beende_thread")
        self.ende += 1

    def psv_prozesse(self) -> tuple[str, ...] | None:
        self._betrete("psv_prozesse")
        if self.prozess is None or isinstance(self.prozess, tuple):
            return self.prozess
        return ("PSV.exe",) if self.prozess else ()

    def dispatch(self, progid: str) -> object:
        self.psv.welt.dispatches.append(progid)
        assert progid == "PSV.AcquisitionInstance"
        return self.psv.inst
