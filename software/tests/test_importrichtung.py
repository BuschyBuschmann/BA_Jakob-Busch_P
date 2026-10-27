"""Importrichtungen der Paketschichten (U1-6).

Die Prüfung liest die Importe per ``ast`` und braucht keine zusätzliche Abhängigkeit.
Regeln (Plan P2, Abschnitt 1)::

    gui -> sitzung -> ablauf -> (domaene, geraet.schnittstelle, protokoll, persistenz)
    geraet.simulator / geraet.com -> geraet.schnittstelle -> domaene

Zusätzlich darf pywin32 nur in ``geraet/com/pywin32_bindung.py`` vorkommen.
"""

import ast
from pathlib import Path

import pytest

import ldv_automation

PAKET = "ldv_automation"
SRC = Path(ldv_automation.__file__).resolve().parent

D = f"{PAKET}.domaene"
S = f"{PAKET}.geraet.schnittstelle"
SIM = f"{PAKET}.geraet.simulator"
COM = f"{PAKET}.geraet.com"
AB = f"{PAKET}.ablauf"
PR = f"{PAKET}.protokoll"
PE = f"{PAKET}.persistenz"
SI = f"{PAKET}.sitzung"
GUI = f"{PAKET}.gui"

# Modulpräfix -> erlaubte interne Importziele (Präfixe). Das längste passende Präfix gilt.
REGELN: dict[str, tuple[str, ...]] = {
    D: (D,),
    f"{PAKET}.geraet": (D, f"{PAKET}.geraet"),
    S: (D, S),
    SIM: (D, S, SIM),
    COM: (D, S, COM),
    PR: (D, S, PR),
    PE: (D, PE),
    AB: (D, S, PR, PE, AB),
    SI: (D, S, f"{PAKET}.geraet", AB, PR, PE, SI),
    GUI: (D, SI, GUI),
    # Einstieg = Kompositionswurzel: setzt Simulator bzw. COM-Adapter für die Sitzung
    # zusammen (die Sitzung hat keine eigene Gerätefabrik), U4.
    # Selbsttest (U5): simulierte Zeit (ablauf.uhr.Testuhr), Domäne für die Testeinträge,
    # Ablage- und Protokollkonstanten für die Prüfung der Ergebnisse.
    f"{PAKET}.__main__": (SI, GUI, S, SIM, COM, AB, D, PR, f"{PAKET}.konfig"),
    # Konfigurationsdatei (K-U5): Werte für Steuerung (ablauf) und COM-Adapter (Lademaske
    # nur über die Richtlinie in geraet.com).
    f"{PAKET}.konfig": (AB, COM, S, D, f"{PAKET}.konfig"),
}

PYWIN32_ERLAUBT = "geraet/com/pywin32_bindung.py"
PYWIN32_NAMEN = ("win32", "pythoncom", "pywintypes", "pythonwin")


def _modulname(datei: Path, wurzel: Path) -> str:
    teile = list(datei.relative_to(wurzel.parent).with_suffix("").parts)
    if teile[-1] == "__init__":
        teile.pop()
    return ".".join(teile)


def _importierte_module(baum: ast.AST, modul: str, ist_paket: bool) -> list[str]:
    """Alle importierten Modulnamen, relative Importe aufgelöst."""
    basis = modul.split(".") if ist_paket else modul.split(".")[:-1]
    ergebnis: list[str] = []
    for knoten in ast.walk(baum):
        if isinstance(knoten, ast.Import):
            ergebnis.extend(a.name for a in knoten.names)
        elif isinstance(knoten, ast.ImportFrom):
            if knoten.level:
                ziel = basis[: len(basis) - (knoten.level - 1)]
                name = ".".join([*ziel, *([knoten.module] if knoten.module else [])])
            else:
                name = knoten.module or ""
            ergebnis.append(name)
            # "from paket import untermodul" kann ein Untermodul meinen
            ergebnis.extend(f"{name}.{a.name}" for a in knoten.names)
        elif (
            isinstance(knoten, ast.Call)
            and isinstance(knoten.func, ast.Attribute | ast.Name)
            and getattr(knoten.func, "attr", getattr(knoten.func, "id", ""))
            in ("import_module", "__import__")
            and knoten.args
            and isinstance(knoten.args[0], ast.Constant)
            and isinstance(knoten.args[0].value, str)
        ):
            ergebnis.append(knoten.args[0].value)
    return ergebnis


def _regel(modul: str) -> tuple[str, ...] | None:
    passend = [p for p in REGELN if modul == p or modul.startswith(p + ".")]
    return REGELN[max(passend, key=len)] if passend else None


def finde_verstoesse(wurzel: Path) -> list[str]:
    """Gibt alle Verstöße gegen die Importregeln unterhalb von ``wurzel`` zurück."""
    verstoesse: list[str] = []
    for datei in sorted(wurzel.rglob("*.py")):
        modul = _modulname(datei, wurzel)
        baum = ast.parse(datei.read_text(encoding="utf-8"), filename=str(datei))
        importe = _importierte_module(baum, modul, datei.name == "__init__.py")
        relativ = datei.relative_to(wurzel).as_posix()
        for name in importe:
            if name.split(".")[0].startswith(PYWIN32_NAMEN) and relativ != PYWIN32_ERLAUBT:
                verstoesse.append(
                    f"{relativ}: pywin32-Import '{name}' außerhalb von {PYWIN32_ERLAUBT}"
                )
        erlaubt = _regel(modul)
        if erlaubt is None:
            continue
        for name in importe:
            if not (name == PAKET or name.startswith(PAKET + ".")):
                continue
            if name == PAKET:
                continue
            if not any(name == e or name.startswith(e + ".") for e in erlaubt):
                # "from a import b" erzeugt zusätzlich den Kandidaten "a.b"; ein Attribut
                # (kein Modul) darf nicht zum Fehlalarm führen.
                if _ist_attribut_import(name, wurzel):
                    continue
                verstoesse.append(f"{relativ}: verbotener Import '{name}'")
    return verstoesse


def _ist_attribut_import(name: str, wurzel: Path) -> bool:
    """``True``, wenn ``name`` kein Modul/Paket unter ``wurzel`` ist (also ein Attribut)."""
    teile = name.split(".")[1:]
    pfad = wurzel.joinpath(*teile)
    return not (pfad.with_suffix(".py").is_file() or (pfad / "__init__.py").is_file())


def test_u1_6_echter_quellbaum_hat_keine_verstoesse() -> None:
    assert finde_verstoesse(SRC) == []


def _baum(tmp_path: Path, dateien: dict[str, str]) -> Path:
    wurzel = tmp_path / PAKET
    for rel, inhalt in dateien.items():
        pfad = wurzel / rel
        pfad.parent.mkdir(parents=True, exist_ok=True)
        pfad.write_text(inhalt, encoding="utf-8")
    return wurzel


@pytest.mark.parametrize(
    ("datei", "inhalt", "teil"),
    [
        ("domaene/x.py", "from ldv_automation.ablauf import steuerung\n", "ablauf"),
        ("domaene/x.py", "import ldv_automation.geraet.schnittstelle\n", "geraet"),
        ("domaene/x.py", "from ldv_automation.geraet import schnittstelle\n", "geraet"),
        ("domaene/x.py", "from ..geraet.schnittstelle import Messgeraet\n", "geraet"),
        ("domaene/x.py", "from .. import ablauf\n", "ablauf"),
        ("domaene/__init__.py", "from ..persistenz import warteschlangendatei\n", "persistenz"),
        ("geraet/schnittstelle.py", "from ldv_automation.geraet import simulator\n", "simulator"),
        ("geraet/simulator.py", "from ldv_automation.ablauf import uhr\n", "ablauf"),
        ("persistenz/p.py", "from ldv_automation.geraet import schnittstelle\n", "geraet"),
        ("gui/g.py", "from ldv_automation.ablauf import steuerung\n", "ablauf"),
        ("domaene/x.py", "import win32com.client\n", "pywin32"),
        ("geraet/simulator.py", "from pythoncom import CoInitialize\n", "pywin32"),
        ("geraet/com/adapter.py", "import win32api\n", "pywin32"),
        ("domaene/x.py", "import importlib\nimportlib.import_module('win32com')\n", "pywin32"),
    ],
)
def test_u1_6_verstoesse_werden_erkannt(tmp_path: Path, datei: str, inhalt: str, teil: str) -> None:
    dateien = {
        "__init__.py": "",
        "domaene/__init__.py": "",
        "geraet/__init__.py": "",
        "geraet/schnittstelle.py": "",
        "geraet/simulator.py": "",
        "ablauf/__init__.py": "",
        "ablauf/steuerung.py": "",
        "ablauf/uhr.py": "",
        "persistenz/__init__.py": "",
        "persistenz/warteschlangendatei.py": "",
        "gui/__init__.py": "",
        "geraet/com/__init__.py": "",
    }
    dateien[datei] = inhalt
    verstoesse = finde_verstoesse(_baum(tmp_path, dateien))
    assert verstoesse, f"kein Verstoß erkannt für {inhalt!r}"
    assert any(teil in v for v in verstoesse)
    assert any(v.startswith(datei) for v in verstoesse)


@pytest.mark.parametrize(
    ("datei", "inhalt"),
    [
        ("domaene/x.py", "from ldv_automation.domaene.eintraege import Messung\nimport json\n"),
        ("domaene/x.py", "from . import eintraege\nfrom .parameter import KATALOG\n"),
        ("geraet/schnittstelle.py", "from ldv_automation.domaene.parameter import ParameterWert\n"),
        ("geraet/simulator.py", "from ldv_automation.geraet.schnittstelle import Messgeraet\n"),
        ("geraet/simulator.py", "from .schnittstelle import Messgeraet\n"),
        ("geraet/com/pywin32_bindung.py", "import win32com.client\nimport pythoncom\n"),
        ("ablauf/steuerung.py", "from ldv_automation.geraet.schnittstelle import Messgeraet\n"),
        ("persistenz/p.py", "from ldv_automation.domaene import Messung\n"),
    ],
)
def test_u1_6_erlaubte_importe_werden_nicht_beanstandet(
    tmp_path: Path, datei: str, inhalt: str
) -> None:
    dateien = {
        "__init__.py": "",
        "domaene/__init__.py": "",
        "domaene/eintraege.py": "",
        "domaene/parameter.py": "",
        "geraet/__init__.py": "",
        "geraet/schnittstelle.py": "",
        "geraet/com/__init__.py": "",
    }
    dateien[datei] = inhalt
    assert finde_verstoesse(_baum(tmp_path, dateien)) == []
