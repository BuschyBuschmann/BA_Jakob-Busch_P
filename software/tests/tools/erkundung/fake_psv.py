"""Test-Doubles für das Erkundungsskript: Fake-PSV, Fake-PolyFile, Fake-Umgebung.

Kein Gerätesimulator des Hauptpakets (bewusst unabhängig, siehe Plan E1, Abschnitt 6).
Jeder Zugriff auf einen Fake-Knoten wird in ``World.log`` protokolliert, unabhängig vom
Whitelist-Proxy des Skripts.
"""

from __future__ import annotations

import copy
import datetime as dt
import threading
from collections.abc import Callable
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import erkundung


class FakeComError(Exception):
    """Ersatz für ``pywintypes.com_error`` (hresult/excepinfo/strerror)."""

    def __init__(self, message: str = "Fehler", hresult: int = -2147352567) -> None:
        super().__init__(message)
        self.hresult = hresult
        self.excepinfo = (0, "PSV", message, None, 0, hresult)
        self.strerror = message
        self.argerror = -1


class _Ole:
    def __init__(self, node: FakeNode) -> None:
        self._node = node

    def GetIDsOfNames(self, name: str) -> tuple[int, ...]:  # noqa: N802 - COM-Name
        if name in self._node._known():
            return (1,)
        raise FakeComError(f"Unbekannter Name {name}")


@dataclass
class World:
    """Gemeinsamer Zustand des Fakes: Aufrufprotokoll, Fehlerinjektion, Blockaden."""

    log: list[tuple[str, str, str]] = field(default_factory=list)
    nodes: list[FakeNode] = field(default_factory=list)
    fail: dict[tuple[str, str], Exception] = field(default_factory=dict)
    hang: dict[tuple[str, str], threading.Event] = field(default_factory=dict)
    calls_args: list[tuple[str, str, tuple[Any, ...]]] = field(default_factory=list)
    started: bool = False

    def snapshot(self) -> list[dict[str, Any]]:
        """Zustand aller Knoten (Properties); Kinder als Objektkennung."""
        out: list[dict[str, Any]] = []
        for node in self.nodes:
            props = {
                k: (f"<{v._kind}>" if isinstance(v, FakeNode) else copy.deepcopy(v))
                for k, v in node._props.items()
            }
            out.append(props)
        return out


class FakeNode:
    """Generisches COM-Objekt: Properties, Methoden und versteckte (nur existente) Namen."""

    def __init__(
        self,
        kind: str,
        world: World,
        props: dict[str, Any] | None = None,
        methods: dict[str, Callable[..., Any]] | None = None,
        hidden: tuple[str, ...] = (),
    ) -> None:
        object.__setattr__(self, "_kind", kind)
        object.__setattr__(self, "_world", world)
        object.__setattr__(self, "_props", dict(props or {}))
        object.__setattr__(self, "_methods", dict(methods or {}))
        object.__setattr__(self, "_hidden", hidden)
        world.nodes.append(self)

    def _known(self) -> set[str]:
        return set(self._props) | set(self._methods) | set(self._hidden)

    @property
    def _oleobj_(self) -> _Ole:
        return _Ole(self)

    def _enter(self, name: str, op: str) -> None:
        world: World = self._world
        world.log.append((self._kind, name, op))
        key = (self._kind, name)
        event = world.hang.get(key)
        if event is not None:
            event.wait(timeout=30)
        error = world.fail.get(key)
        if error is not None:
            raise error

    def __getattr__(self, name: str) -> Any:
        if name in self._props:
            self._enter(name, "get")
            return self._props[name]
        if name in self._methods:
            method = self._methods[name]

            def call(*args: Any) -> Any:
                self._world.calls_args.append((self._kind, name, args))
                self._enter(name, "call")
                return method(*args)

            return call
        raise AttributeError(name)

    def __setattr__(self, name: str, value: Any) -> None:
        self._enter(name, "set")
        self._props[name] = value


def _collection(world: World, kind: str, items: list[FakeNode], base: int = 1) -> FakeNode:
    def item(index: int) -> FakeNode:
        pos = index - base
        if not isinstance(index, int) or pos < 0 or pos >= len(items):
            raise FakeComError(f"Index {index} ungültig")
        return items[pos]

    return FakeNode(kind, world, {"Count": len(items)}, {"Item": item})


def build_psv(
    world: World,
    *,
    running: bool = True,
    state: int = 0,
    mode: int = 1,
    n_points: int = 5,
    point_label_offset: int = 100,
    has_hardware: bool = True,
) -> FakeNode:
    """Baut ``PSV.AcquisitionInstance`` samt Objektbaum nach I5 1.4."""
    points = [
        FakeNode(
            "MeasPoint",
            world,
            {
                "Index": i,
                "Label": point_label_offset + i,
                "ScanStatus": 1,
                "AverageCount": 3,
                "Sigma": 0.25,
            },
            {"CoordXYZ": lambda: (0.1, 0.2, 0.3)},
        )
        for i in range(1, n_points + 1)
    ]
    labels = {p._props["Label"]: p._props["Index"] for p in points}
    meas_points = _collection(world, "MeasPoints", points)
    meas_points._methods["LabelToIndex"] = lambda label: labels[label]
    align3d = _collection(
        world,
        "Alignments3D",
        [
            FakeNode(
                "Alignment3D",
                world,
                {
                    "Valid": True,
                    "CurrentQuality": 0.9,
                    "TargetQuality": 0.8,
                    "PositionUncertainty": 1e-3,
                    "AngleUncertainty": 2e-3,
                },
            )
        ],
    )
    align2d = _collection(world, "Alignments2D", [FakeNode("Alignment2D", world, {"Valid": True})])
    head_info = FakeNode(
        "SensorHeadInfo",
        world,
        {
            "Name": "OFV-505",
            "SerialNumber": "SH1",
            "FirmwareVersion": "2.0",
            "LaserWavelength": 6.328e-7,
            "LaserPower": 1.0,
        },
    )
    sensor_heads = _collection(
        world, "SensorHeads", [FakeNode("SensorHead", world, {"SensorHeadInfo": head_info})], 0
    )
    controllers = _collection(
        world, "Controllers", [FakeNode("Controller", world, {"SensorHeads": sensor_heads})], 0
    )
    controller = FakeNode(
        "ControllerGroup",
        world,
        {
            "Controllers": controllers,
            "ControllerInfo": FakeNode(
                "ControllerInfo",
                world,
                {
                    "DeviceName": "OFV-5000",
                    "FirmwareVersion": "1.2",
                    "Name": "Ctrl",
                    "SerialNumber": "SN1",
                },
            ),
        },
    )
    hardware = FakeNode(
        "Hardware",
        world,
        {
            name: f"{name}-wert"
            for name in erkundung.HARDWARE_PROPS
            if name not in ("AcqBoardChannelCount",)
        }
        | {"AcqBoardChannelCount": 4},
    )
    infos = FakeNode(
        "Infos",
        world,
        dict.fromkeys(erkundung.INFOS_HAS, True)
        | {"HasHardware": has_hardware}
        | {
            "Hardware": hardware,
            "ScanHeadDevicesInfo": FakeNode(
                "ScanHeadDevicesInfo",
                world,
                {"ScanHeadName": "PSV-I-680", "ScanHeadType": 27},
            ),
            "Vibrometers": _collection(world, "Vibrometers", [controller]),
            "MeasPoints": meas_points,
            "Alignments": FakeNode(
                "Alignments", world, {"Alignments3D": align3d, "Alignments2D": align2d}
            ),
        },
    )
    fft = FakeNode(
        "FftProperties",
        world,
        {
            "Bandwidth": 1000.0,
            "StartFrequency": 0.0,
            "EndFrequency": 1000.0,
            "Lines": 800,
            "SampleResolution": 1.25,
            "Overlap": 0,
            "SampleFrequency": 2560.0,
            "SampleTime": 0.8,
        },
        hidden=("FftAcqPropertiesValidator",),
    )
    props = FakeNode(
        "AcquisitionProperties",
        world,
        {name: name in ("HasFftProperties", "HasAverageProperties", "HasGeneralProperties")
         for name in erkundung.HAS_PROPS}
        | {
            "FftProperties": fft,
            "AverageProperties": FakeNode("AverageProperties", world, {"Type": 1, "Count": 5}),
            "GeneralProperties": FakeNode(
                "GeneralProperties", world, dict.fromkeys(erkundung.GENERAL_PROPS, False)
            ),
        },
    )  # fmt: skip
    acq = FakeNode(
        "Acquisition",
        world,
        {
            "State": state,
            "Mode": 1,
            "ScanCaps": 0,
            "GeneratorsOn": False,
            "ScanFileName": "",
            "ActiveProperties": props,
            "Infos": infos,
        },
        {"GetLaserOn": lambda i: i == -1},
    )
    app_props: dict[str, Any] = {
        "Version": "10.4.0.1",
        "Mode": mode,
        "Visible": True,
        "WarningLevel": 0,
        "SuppressMessagesForAutomation": False,
        "MessagesLoggingEnabled": False,
        "Acquisition": acq,
    }
    app = FakeNode("Application", world, app_props, hidden=("DigitalPorts",))
    if mode != 1:
        world.fail[("Application", "Acquisition")] = FakeComError("nur im Erfassungsmodus")

    def get_application(create: bool, timeout_ms: int = 10000) -> FakeNode:
        if create:
            world.started = True
        return app

    return FakeNode(
        "AcquisitionInstance",
        world,
        {"IsRunning": running},
        {"GetApplication": get_application},
    )


def build_polyfile(world: World, path_seen: list[str] | None = None) -> FakeNode:
    """Baut ``PolyFile.PolyFile`` mit zwei Domänen (Time, FFT) und 3 Kanälen."""
    n_lines = 8
    delta_f = 1.25

    def make_display() -> list[FakeNode]:
        return [
            FakeNode("Display", world, {"Name": "Mag", "Type": 1}),
            FakeNode("Display", world, {"Name": "Real&Imag", "Type": 9}),
        ]

    def make_channel(name: str) -> FakeNode:
        yaxis = FakeNode("YAxis", world, {"Name": "v", "Unit": "m/s", "Min": 0.0, "Max": 1.0})
        desc = FakeNode(
            "SignalDescription",
            world,
            {"DomainType": 3, "FunctionType": 12, "Complex": True, "Name": "Velocity",
             "YAxis": yaxis},
        )  # fmt: skip
        signal = FakeNode(
            "Signal",
            world,
            {"Name": "Velocity", "Description": desc,
             "Displays": _collection(world, "Displays", make_display())},
        )  # fmt: skip
        return FakeNode(
            "Channel",
            world,
            {"Name": name, "Signals": _collection(world, "Signals", [signal])},
        )

    def make_domain(name: str) -> FakeNode:
        axis = FakeNode(
            "XAxis",
            world,
            {"Min": delta_f, "Max": delta_f * n_lines, "MaxCount": n_lines,
             "Name": "Frequency", "Unit": "Hz"},
            {"GetMidX": lambda i: delta_f * (i + 1)},
        )  # fmt: skip
        data_point = FakeNode(
            "DataPoint",
            world,
            {"AverageCount": 3},
            {"GetData": lambda display, frame: tuple(float(i) for i in range(2 * n_lines))},
        )
        return FakeNode(
            "PointDomain",
            world,
            {
                "Name": name,
                "Type": 3,
                "Channels": _collection(
                    world, "Channels", [make_channel(c) for c in ("Vib X", "Vib Y", "Vib Z")]
                ),
                "DataPoints": _collection(world, "DataPoints", [data_point, data_point]),
            },
            {"GetXAxis": lambda display: axis},
        )

    domains = _collection(world, "PointDomains", [make_domain("Time"), make_domain("FFT")])
    version = FakeNode("FileVersion", world, {n: f"{n}-wert" for n in erkundung.FILE_VERSION_PROPS})
    summary = FakeNode("SummaryInfo", world, {n: f"{n}-text" for n in erkundung.SUMMARY_PROPS})
    file_infos = FakeNode(
        "Infos",
        world,
        dict.fromkeys(erkundung.INFOS_HAS, False)
        | {"HasMeasPoints": True, "MeasPoints": _collection(world, "MeasPoints", [])},
    )

    pf = FakeNode(
        "PolyFile",
        world,
        {"ReadOnly": False, "IsOpen": False, "Version": version, "SummaryInfo": summary,
         "Infos": file_infos},
        {},
    )  # fmt: skip

    def open_file(path: str) -> None:
        if pf._props["ReadOnly"] is not True:
            raise FakeComError("Datei nicht schreibgeschützt geöffnet (Test-Double)")
        if path_seen is not None:
            path_seen.append(path)
        pf._props["IsOpen"] = True

    def close_file() -> None:
        pf._props["IsOpen"] = False

    pf._methods.update({"Open": open_file, "Close": close_file, "GetPointDomains": lambda: domains})
    return pf


class FakeRegistry:
    """Registry-Double: ``{(view, pfad, name): wert}`` und Unterschlüssel."""

    def __init__(
        self, values: dict[tuple[int, str, str], str], subkeys: dict[tuple[int, str], list[str]]
    ):
        self.values = values
        self.sub = subkeys

    def get_value(self, path: str, name: str, view: int) -> str | None:
        return self.values.get((view, path, name))

    def subkeys(self, path: str, view: int) -> list[str]:
        return list(self.sub.get((view, path), []))


def make_registry(server_path: str) -> FakeRegistry:
    """Registry mit allen ProgIDs in der 64-Bit-Sicht; ``PSV.AcquisitionInstance`` mit Server."""
    values: dict[tuple[int, str, str], str] = {}
    for n, progid in enumerate(erkundung.PROGIDS, start=1):
        clsid = f"{{0000000{n}-0000-0000-0000-000000000000}}"
        values[(64, f"{progid}\\CLSID", "")] = clsid
        values[(64, f"CLSID\\{clsid}", "")] = f"{progid} Beschreibung"
        values[(64, f"CLSID\\{clsid}\\LocalServer32", "")] = f'"{server_path}" /Automation'
        values[(64, f"CLSID\\{clsid}\\TypeLib", "")] = "{AAAA}"
        values[(64, f"CLSID\\{clsid}", "AppID")] = "{APP}"
    values[(64, "AppID\\{APP}", "")] = "PSV AppID"
    values[(64, "CLSID\\{00000001-0000-0000-0000-000000000000}\\InprocServer32", "")] = (
        "%SystemRoot%\\poly.dll"
    )
    values[
        (64, "CLSID\\{00000001-0000-0000-0000-000000000000}\\InprocServer32", "ThreadingModel")
    ] = "Apartment"
    values[(64, "TypeLib\\{AAAA}\\1.0", "")] = "Polytec PSV Type Library"
    values[(64, "TypeLib\\{AAAA}\\1.0\\0\\win64", "")] = "C:\\Program Files\\Polytec\\psv.tlb"
    values[(64, "TypeLib\\{BBBB}\\2.0", "")] = "Anderes"
    values[(64, "TypeLib\\{BBBB}\\2.0\\0\\win32", "")] = "C:\\x\\other.tlb"
    subkeys = {
        (64, "TypeLib"): ["{AAAA}", "{BBBB}"],
        (64, "TypeLib\\{AAAA}"): ["1.0"],
        (64, "TypeLib\\{BBBB}"): ["2.0"],
        (64, "TypeLib\\{AAAA}\\1.0"): ["0"],
        (64, "TypeLib\\{BBBB}\\2.0"): ["0"],
    }
    return FakeRegistry(values, subkeys)


@dataclass
class Harness:
    """Fake-Umgebung samt Beobachtungspunkten."""

    env: erkundung.Env
    world: World
    exits: list[int]
    inputs: list[str]


def make_harness(
    tmp_path: Path,
    *,
    running: bool = True,
    state: int = 0,
    mode: int = 1,
    answer: str = "JA",
    with_registry: bool = True,
    system: str = "Windows",
    pywin32_ok: bool = True,
    username: str = "jakob",
    hostname: str = "MESS-PC",
    server_path: str | None = None,
    has_hardware: bool = True,
) -> Harness:
    """Baut eine :class:`erkundung.Env` mit Fakes."""
    world = World()
    psv = build_psv(world, running=running, state=state, mode=mode, has_hardware=has_hardware)
    opened: list[str] = []
    polyfile = build_polyfile(world, opened)
    exits: list[int] = []
    inputs: list[str] = []
    program_files = tmp_path / "pf"
    (program_files / "Polytec" / "PSV").mkdir(parents=True)
    (program_files / "Polytec" / "readme.txt").write_text("x")
    server = server_path or str(tmp_path / "psv.exe")
    if server_path is None:
        header = bytearray(64)
        header[:2] = b"MZ"
        header[60:64] = (64).to_bytes(4, "little")
        (tmp_path / "psv.exe").write_bytes(
            bytes(header) + b"PE\x00\x00" + (0x8664).to_bytes(2, "little")
        )

    def dispatch(progid: str) -> FakeNode:
        if progid == "PSV.AcquisitionInstance":
            return psv
        if progid == "PolyFile.PolyFile":
            return polyfile
        raise FakeComError(f"Unbekannte ProgID {progid}")

    def input_fn(prompt: str) -> str:
        inputs.append(prompt)
        return answer

    csv_text = '"System","4","Services","0","10 K"\n"PSV.exe","1234","Console","1","99 K"\n'
    env = erkundung.Env(
        dispatch=dispatch,
        registry=make_registry(server) if with_registry else None,
        enum_tlbs=lambda: [
            {"desc": "Polytec PSV", "dll": "psv.tlb", "clsid": "{A}", "major": 1, "minor": 0},
            {"desc": "Anderes", "dll": "x.tlb", "clsid": "{B}", "major": 1, "minor": 0},
        ],
        read_constants=lambda names: {
            n: (erkundung.EXPECTED_CONSTANTS[n] if n != "ptcAcqStateSingle" else 99) for n in names
        },
        file_version=lambda path: "10.4.0.1",
        run_command=lambda cmd: csv_text,
        pywin32_info=lambda: {"importierbar": pywin32_ok, "version": "306", "fehler": None},
        thread_init=lambda: None,
        thread_done=lambda: None,
        hard_exit=exits.append,
        input_fn=input_fn,
        now=lambda: dt.datetime(2026, 10, 24, 9, 30, 15, tzinfo=dt.timezone(dt.timedelta(hours=2))),
        monotonic=__import__("time").monotonic,
        environ={
            "ProgramFiles": str(program_files),
            "SystemRoot": "C:\\Windows",
            "PROCESSOR_ARCHITECTURE": "AMD64",
        },
        hostname=hostname,
        username=username,
        system=system,
    )
    return Harness(env, world, exits, inputs)
