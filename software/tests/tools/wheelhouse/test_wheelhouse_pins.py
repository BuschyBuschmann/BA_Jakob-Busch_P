"""``PINS`` des Wheelhouse-Skripts gegen ``uv.lock`` (P-AUSW T1.1).

Die Laufzeitabhängigkeiten des Pakets (``dependencies`` plus Extra ``com``, transitiv über
``uv.lock``) müssen genau den Pins entsprechen: ein fehlendes Paket (wie früher ``numpy``)
oder eine veraltete Version würde den Messrechner-Install ohne Internet scheitern lassen.
Die Prüfung ist exakt (Versionsgleichheit als Text), es gibt keine Toleranz.
"""

from __future__ import annotations

import importlib.util
import re
import tomllib
from pathlib import Path
from types import ModuleType

SOFTWARE = Path(__file__).resolve().parents[3]


def _skript() -> ModuleType:
    pfad = SOFTWARE / "tools" / "wheelhouse" / "erzeuge_wheelhouse.py"
    spec = importlib.util.spec_from_file_location("erzeuge_wheelhouse", pfad)
    assert spec is not None
    assert spec.loader is not None
    modul = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modul)
    return modul


def _norm(name: str) -> str:
    return re.sub(r"[-_.]+", "-", name).lower()


def _laufzeit_pakete() -> dict[str, str]:
    """Name -> Version aller Laufzeitpakete (Hauptabhängigkeiten, Extra ``com``, transitiv)."""
    lock = tomllib.loads((SOFTWARE / "uv.lock").read_text(encoding="utf-8"))
    pakete = {_norm(p["name"]): p for p in lock["package"]}
    wurzel = pakete["ldv-automation"]
    offen = [d["name"] for d in wurzel["dependencies"]]
    offen += [d["name"] for d in wurzel["optional-dependencies"]["com"]]
    gesehen: dict[str, str] = {}
    while offen:
        name = _norm(offen.pop())
        if name in gesehen:
            continue
        gesehen[name] = pakete[name]["version"]
        offen += [d["name"] for d in pakete[name].get("dependencies", [])]
    return gesehen


def _pins() -> dict[str, str]:
    ergebnis: dict[str, str] = {}
    for pin in _skript().PINS:
        name, version = pin.split("==")
        assert _norm(name) not in ergebnis, f"{name} doppelt in PINS"
        ergebnis[_norm(name)] = version
    return ergebnis


def test_pins_entsprechen_den_laufzeitpaketen_der_lockdatei_exakt() -> None:
    assert _pins() == _laufzeit_pakete()


def test_pins_enthalten_numpy_matplotlib_und_olefile() -> None:
    """Regression: ``numpy`` fehlte, ``matplotlib``/``olefile`` sind seit T1.1 Hauptpakete."""
    pins = _pins()
    assert {"numpy", "matplotlib", "olefile", "six"} <= set(pins)


def test_wheelhouse_befehl_enthaelt_alle_pins() -> None:
    skript = _skript()
    befehl = skript.baue_befehl("ziel")
    assert set(skript.PINS) <= set(befehl)
