"""Fake-COM-Objekte für ``daten_lesen`` und ``einstellungen_lesen`` (PolyFile, nur lesend).

Alle Zugriffe auf Namen, Zuweisungen und das Öffnen/Schließen werden in ``Protokoll``
festgehalten, unabhängig vom Code der Skripte.
"""

from __future__ import annotations

import sys
import types
from collections.abc import Callable
from dataclasses import dataclass, field
from typing import Any

import pytest


@dataclass
class Protokoll:
    """Zugriffe auf die Fake-Objekte."""

    zugriffe: list[str] = field(default_factory=list)
    zuweisungen: list[tuple[str, Any, bool]] = field(default_factory=list)  # (Name, Wert, offen)
    offen: bool = False
    geschlossen: bool = False
    pfade: list[str] = field(default_factory=list)


class Knoten:
    """Generisches COM-Objekt; unbekannte Namen lösen ``AttributeError`` aus."""

    def __init__(
        self,
        log: Protokoll,
        werte: dict[str, Any] | None = None,
        methoden: dict[str, Callable[..., Any]] | None = None,
        fehler: dict[str, Exception] | None = None,
    ) -> None:
        object.__setattr__(self, "_log", log)
        object.__setattr__(self, "_werte", dict(werte or {}))
        object.__setattr__(self, "_methoden", dict(methoden or {}))
        object.__setattr__(self, "_fehler", dict(fehler or {}))

    def __getattr__(self, name: str) -> Any:
        self._log.zugriffe.append(name)
        if name in self._fehler:
            raise self._fehler[name]
        if name in self._werte:
            return self._werte[name]
        if name in self._methoden:
            return self._methoden[name]
        raise AttributeError(name)

    def __setattr__(self, name: str, wert: Any) -> None:
        self._log.zuweisungen.append((name, wert, self._log.offen))
        self._werte[name] = wert


def sammlung(log: Protokoll, eintraege: list[Any]) -> Knoten:
    """1-basierte Collection mit ``Count`` und ``Item(i)``."""
    return Knoten(
        log,
        {"Count": len(eintraege)},
        {"Item": lambda i: eintraege[i - 1]},
    )


def polyfile(
    log: Protokoll,
    werte: dict[str, Any] | None = None,
    methoden: dict[str, Callable[..., Any]] | None = None,
) -> Knoten:
    """PolyFile mit protokolliertem ``Open``/``Close``."""

    def open_(pfad: str) -> None:
        log.pfade.append(pfad)
        log.offen = True

    def close() -> None:
        log.geschlossen = True

    return Knoten(log, werte, {"Open": open_, "Close": close, **(methoden or {})})


def installiere_fake_win32(monkeypatch: pytest.MonkeyPatch, pf: Knoten) -> None:
    """Setzt ``sys.modules['win32com.client']`` so, dass ``Dispatch`` ``pf`` liefert."""
    client = types.ModuleType("win32com.client")
    dispatch = types.SimpleNamespace(Dispatch=lambda prog_id: pf)
    client.dynamic = dispatch  # type: ignore[attr-defined]
    paket = types.ModuleType("win32com")
    paket.client = client  # type: ignore[attr-defined]
    monkeypatch.setitem(sys.modules, "win32com", paket)
    monkeypatch.setitem(sys.modules, "win32com.client", client)


Signaldaten = dict[str, Any]  # re, im, abs (Listen), df (float), typen (Display-Typen)


def _domaene(log: Protokoll, signale: dict[tuple[str, str], Signaldaten], name: str) -> Knoten:
    """Baut eine Domäne mit einem Datenpunkt und den angegebenen Signalen."""
    kanaele: dict[str, dict[str, Knoten]] = {}
    for (kanal, signal_name), s in signale.items():
        displays = []
        for typ in s.get("typen", (7, 8)):
            d = Knoten(log, {"Type": typ, "Name": f"Display{typ}"})
            daten = {7: s.get("re", []), 8: s.get("im", []), 1: s.get("abs", [])}
            object.__setattr__(d, "_daten", daten.get(typ, []))
            object.__setattr__(d, "_df", s.get("df", 0.5))
            displays.append(d)
        kanaele.setdefault(kanal, {})[signal_name] = Knoten(
            log, {"Displays": sammlung(log, displays), "Name": signal_name}
        )

    def kanal_knoten(kanal: str) -> Knoten:
        eintraege = kanaele[kanal]
        namen = list(eintraege)

        def signal_item(ref: int | str) -> Knoten:
            return eintraege[namen[ref - 1] if isinstance(ref, int) else ref]

        signals = Knoten(log, {"Count": len(namen)}, {"Item": signal_item})
        return Knoten(log, {"Signals": signals, "Name": kanal})

    def kanal_item(ref: int | str) -> Knoten:
        kanal_namen = list(kanaele)
        return kanal_knoten(kanal_namen[ref - 1] if isinstance(ref, int) else ref)

    def get_x_axis(disp: Knoten) -> Knoten:
        df = disp._df
        return Knoten(log, methoden={"GetMidX": lambda i: i * df})

    einheit = Knoten(log, {"Unit": "m/s"})
    datenpunkt = Knoten(
        log,
        {"MeasPoint": Knoten(log, {"Label": 132})},
        {"GetData": lambda disp, _x: tuple(disp._daten)},
    )
    return Knoten(
        log,
        {
            "Name": name,
            "Channels": Knoten(log, {"Count": len(kanaele)}, {"Item": kanal_item}),
            "DataPoints": Knoten(log, methoden={"Item": lambda i: datenpunkt}),
        },
        {
            "GetXAxis": get_x_axis,
            "GetYAxes": lambda disp: Knoten(log, methoden={"Item": lambda i: einheit}),
        },
    )


def daten_datei(
    log: Protokoll,
    signale: dict[tuple[str, str], Signaldaten],
    domaenenname: str = "FFT",
    weitere: dict[str, dict[tuple[str, str], Signaldaten]] | None = None,
) -> Knoten:
    """Baut ein PolyFile mit Domäne 1 (``signale``) und optional weiteren benannten Domänen."""
    domaenen = [_domaene(log, signale, domaenenname)]
    domaenen += [_domaene(log, sig, name) for name, sig in (weitere or {}).items()]
    return polyfile(
        log,
        methoden={
            "GetPointDomains": lambda: Knoten(
                log, {"Count": len(domaenen)}, {"Item": lambda i: domaenen[i - 1]}
            )
        },
    )


def einstellungen_datei(
    log: Protokoll,
    abschnitte: dict[str, dict[str, Any] | None],
    fehler: dict[str, dict[str, Exception]] | None = None,
) -> Knoten:
    """PolyFile für ``einstellungen_lesen``.

    ``abschnitte`` ordnet dem Abschnittsnamen (``FftProperties`` usw.) seine Werte zu oder
    ``None`` (``Has…`` ist dann ``False``).
    """
    fehler = fehler or {}
    werte: dict[str, Any] = {}
    for name, inhalt in abschnitte.items():
        werte[f"Has{name}"] = inhalt is not None
        if inhalt is not None:
            werte[name] = Knoten(log, inhalt, fehler=fehler.get(name))
    props = Knoten(log, werte)
    modes = Knoten(log, {"ActiveMode": 1, "ActiveProperties": props})
    return polyfile(
        log,
        {
            "Version": Knoten(log, {"ProgramVersionString": "9.9"}),
            "Infos": Knoten(log, {"AcquisitionInfoModes": modes}),
        },
    )
