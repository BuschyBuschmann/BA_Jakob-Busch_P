"""Importrichtungen der Paketschichten (U1-6).

Die Prüfung liest die Importe per ``ast`` und braucht keine zusätzliche Abhängigkeit.
Regeln (Plan P2, Abschnitt 1)::

    gui -> sitzung -> ablauf -> (domaene, geraet.schnittstelle, protokoll, persistenz)
    geraet.simulator / geraet.com -> geraet.schnittstelle -> domaene

Zusätzlich darf pywin32 nur in ``geraet/com/pywin32_bindung.py`` vorkommen.

Die Auswertung (``auswertung``, Paket W5-1) ist Qt-frei und importiert nur NumPy, ``olefile``
(der .svd-Leser liegt seit P-AUSW T1.1 im Paket), die Standardbibliothek und
``protokoll.version`` (Git-Hash im Export).

Auswertungsoberfläche (P-AUSW T1.1, ADR-020/ADR-021)::

    gui -> (auswertung, darstellung, hintergrund)
    darstellung -> auswertung      (nur NumPy und matplotlib ohne pyplot, pylab, Qt-Backends)
    hintergrund -> (nichts)        (nur Standardbibliothek, läuft im Worker-Prozess)

``darstellung`` und ``hintergrund`` sind noch nicht (alle) angelegt; die Regeln gelten, sobald
die Module existieren, und sind an synthetischen Bäumen geprüft.
"""

import ast
import re
import subprocess
import sys
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
AW = f"{PAKET}.auswertung"
DAR = f"{PAKET}.darstellung"
HG = f"{PAKET}.hintergrund"
VERSION = f"{PAKET}.protokoll.version"

#: Externe Pakete, die ``auswertung`` außer der Standardbibliothek importieren darf.
#: ``olefile``: der .svd-Leser (``svd_lesen``) liegt seit P-AUSW T1.1 im Paket.
AUSWERTUNG_EXTERN = ("numpy", "olefile")

#: Externe Pakete von ``darstellung`` (Zeichenfunktionen, UI-18: ohne Qt, ohne pyplot).
DARSTELLUNG_EXTERN = ("numpy", "matplotlib")

#: In ``darstellung`` verbotene Module trotz erlaubtem ``matplotlib`` (Namens-Präfix je
#: Pfadglied): globaler pyplot-Zustand, Qt-Backends, Qt-Pakete.
DARSTELLUNG_VERBOTEN = re.compile(r"^(pyplot|pylab|backend_qt\w*|PySide\d*|PyQt\d*|shiboken\d*)$")

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
    # Auswertungsoberfläche (P-AUSW): zusätzlich Auswertung, Zeichenfunktionen, Hintergrund.
    GUI: (D, SI, GUI, AW, DAR, HG),
    # Einstieg = Kompositionswurzel: setzt Simulator bzw. COM-Adapter für die Sitzung
    # zusammen (die Sitzung hat keine eigene Gerätefabrik), U4.
    # Selbsttest (U5): simulierte Zeit (ablauf.uhr.Testuhr), Domäne für die Testeinträge,
    # Ablage- und Protokollkonstanten für die Prüfung der Ergebnisse.
    f"{PAKET}.__main__": (SI, GUI, S, SIM, COM, AB, D, PR, f"{PAKET}.konfig"),
    # Konfigurationsdatei (K-U5): Werte für Steuerung (ablauf) und COM-Adapter (Lademaske
    # nur über die Richtlinie in geraet.com).
    f"{PAKET}.konfig": (AB, COM, S, D, f"{PAKET}.konfig"),
    # Auswertung (W5-1): nur eigene Module und der Git-Hash für den Export.
    AW: (AW, VERSION),
    # Zeichenfunktionen (P-AUSW T2): Daten aus der Auswertung, kein gui, kein hintergrund.
    DAR: (DAR, AW),
    # Hintergrundprozess (P-AUSW T1.4): importiert nichts aus dem Paket; die Aufträge
    # (``auswertung.jobs``) werden ihm als Funktionen übergeben.
    HG: (HG,),
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


def externe_verstoesse_auswertung(wurzel: Path) -> list[str]:
    """Importe in ``auswertung`` außerhalb von Standardbibliothek, NumPy und Paket."""
    verstoesse: list[str] = []
    for datei in sorted((wurzel / "auswertung").rglob("*.py")):
        modul = _modulname(datei, wurzel)
        baum = ast.parse(datei.read_text(encoding="utf-8"), filename=str(datei))
        for name in _importierte_module(baum, modul, datei.name == "__init__.py"):
            oben = name.split(".")[0]
            if oben in (PAKET, "__future__") or oben in sys.stdlib_module_names:
                continue
            if oben in AUSWERTUNG_EXTERN:
                continue
            verstoesse.append(f"{datei.relative_to(wurzel).as_posix()}: Import '{name}'")
    return verstoesse


def test_w5_auswertung_importiert_nur_numpy_stdlib_und_version() -> None:
    assert (SRC / "auswertung").is_dir()
    assert externe_verstoesse_auswertung(SRC) == []


@pytest.mark.parametrize(
    ("inhalt", "teil"),
    [
        ("from PySide6 import QtCore\n", "PySide6"),
        ("import scipy.signal\n", "scipy"),
        ("import matplotlib.pyplot as plt\n", "matplotlib"),
    ],
)
def test_w5_auswertung_externe_importe_werden_erkannt(
    tmp_path: Path, inhalt: str, teil: str
) -> None:
    wurzel = _baum(
        tmp_path, {"__init__.py": "", "auswertung/__init__.py": "", "auswertung/x.py": inhalt}
    )
    assert any(teil in v for v in externe_verstoesse_auswertung(wurzel))


@pytest.mark.parametrize(
    ("inhalt", "erlaubt"),
    [
        ("from ldv_automation.protokoll.version import ermittle_build_info\n", True),
        ("from ..protokoll.version import BuildInfo\n", True),
        ("from . import daten\n", True),
        ("from ldv_automation.protokoll import ablage\n", False),
        ("from ldv_automation.domaene import eintraege\n", False),
        ("from ldv_automation.gui import anzeige\n", False),
        ("from ..sitzung import Sitzung\n", False),
    ],
)
def test_w5_auswertung_interne_importe(tmp_path: Path, inhalt: str, erlaubt: bool) -> None:
    dateien = {
        "__init__.py": "",
        "auswertung/__init__.py": "",
        "auswertung/daten.py": "",
        "auswertung/x.py": inhalt,
        "protokoll/__init__.py": "",
        "protokoll/version.py": "",
        "protokoll/ablage.py": "",
        "domaene/__init__.py": "",
        "domaene/eintraege.py": "",
        "gui/__init__.py": "",
        "gui/anzeige.py": "",
        "sitzung.py": "",
    }
    assert (finde_verstoesse(_baum(tmp_path, dateien)) == []) is erlaubt


# --- Auswertungsoberfläche (P-AUSW T1.1): darstellung und hintergrund ----------------------


def externe_verstoesse(
    wurzel: Path, ziel: str, erlaubt: tuple[str, ...], verboten: re.Pattern[str] | None = None
) -> list[str]:
    """Importe in ``wurzel/ziel`` (Ordner oder ``.py``-Datei) außerhalb der erlaubten Pakete.

    Erlaubt sind Standardbibliothek, das Paket selbst (interne Regeln: :data:`REGELN`) und
    ``erlaubt``. ``verboten`` trifft auf jedes Pfadglied eines importierten Namens zu und gilt
    auch für sonst erlaubte Pakete (z. B. ``matplotlib.pyplot``).
    """
    pfad = wurzel / ziel
    if pfad.is_dir():
        dateien = sorted(pfad.rglob("*.py"))
    elif pfad.with_suffix(".py").is_file():
        dateien = [pfad.with_suffix(".py")]
    else:
        return []  # Modul noch nicht angelegt: die Regel greift, sobald es existiert
    verstoesse: list[str] = []
    for datei in dateien:
        modul = _modulname(datei, wurzel)
        baum = ast.parse(datei.read_text(encoding="utf-8"), filename=str(datei))
        for name in _importierte_module(baum, modul, datei.name == "__init__.py"):
            teile = name.split(".")
            oben = teile[0]
            stelle = f"{datei.relative_to(wurzel).as_posix()}: Import '{name}'"
            if verboten is not None and any(verboten.match(t) for t in teile):
                verstoesse.append(stelle)
            elif oben in (PAKET, "__future__") or oben in sys.stdlib_module_names:
                continue
            elif oben not in erlaubt:
                verstoesse.append(stelle)
    return verstoesse


def externe_verstoesse_darstellung(wurzel: Path) -> list[str]:
    """``darstellung``: nur NumPy und matplotlib, weder pyplot noch pylab noch Qt."""
    return externe_verstoesse(wurzel, "darstellung", DARSTELLUNG_EXTERN, DARSTELLUNG_VERBOTEN)


def externe_verstoesse_hintergrund(wurzel: Path) -> list[str]:
    """``hintergrund``: nur Standardbibliothek (läuft im Worker, ohne NumPy und Qt)."""
    return externe_verstoesse(wurzel, "hintergrund", ())


def test_ausw_darstellung_und_hintergrund_im_echten_quellbaum_regelkonform() -> None:
    assert externe_verstoesse_darstellung(SRC) == []
    assert externe_verstoesse_hintergrund(SRC) == []


@pytest.mark.parametrize(
    ("inhalt", "teil"),
    [
        ("import matplotlib.pyplot as plt\n", "pyplot"),
        ("from matplotlib import pyplot\n", "pyplot"),
        ("from matplotlib import pylab\n", "pylab"),
        ("from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg\n", "backend_qtagg"),
        ("from matplotlib.backends import backend_qt\n", "backend_qt"),
        ("from PySide6.QtWidgets import QWidget\n", "PySide6"),
        ("import shiboken6\n", "shiboken6"),
        ("import scipy.signal\n", "scipy"),
        ("import olefile\n", "olefile"),
    ],
)
def test_ausw_darstellung_verbotene_externe_importe_werden_erkannt(
    tmp_path: Path, inhalt: str, teil: str
) -> None:
    wurzel = _baum(
        tmp_path, {"__init__.py": "", "darstellung/__init__.py": "", "darstellung/x.py": inhalt}
    )
    verstoesse = externe_verstoesse_darstellung(wurzel)
    assert any(teil in v and v.startswith("darstellung/x.py") for v in verstoesse)


@pytest.mark.parametrize(
    "inhalt",
    [
        "import numpy as np\nfrom matplotlib.figure import Figure\n",
        "from matplotlib.backends.backend_agg import FigureCanvasAgg\n",
        "import matplotlib\nfrom matplotlib.ticker import FuncFormatter\nimport math\n",
        "from ldv_automation.auswertung import daten\n",
    ],
)
def test_ausw_darstellung_erlaubte_externe_importe(tmp_path: Path, inhalt: str) -> None:
    wurzel = _baum(
        tmp_path,
        {
            "__init__.py": "",
            "auswertung/__init__.py": "",
            "auswertung/daten.py": "",
            "darstellung/__init__.py": "",
            "darstellung/x.py": inhalt,
        },
    )
    assert externe_verstoesse_darstellung(wurzel) == []
    assert finde_verstoesse(wurzel) == []


@pytest.mark.parametrize(
    ("datei", "inhalt", "teil"),
    [
        ("darstellung/x.py", "from ldv_automation.gui import tokens\n", "gui"),
        ("darstellung/x.py", "from ldv_automation.hintergrund import Auftrag\n", "hintergrund"),
        ("darstellung/x.py", "from ldv_automation.protokoll import ablage\n", "protokoll"),
        ("darstellung/x.py", "from ..sitzung import Sitzung\n", "sitzung"),
        ("hintergrund.py", "from ldv_automation.auswertung import jobs\n", "auswertung"),
        ("hintergrund.py", "from ldv_automation.gui import tokens\n", "gui"),
        ("auswertung/x.py", "from ldv_automation.darstellung import stil\n", "darstellung"),
        ("auswertung/x.py", "from ldv_automation.hintergrund import Auftrag\n", "hintergrund"),
        ("domaene/x.py", "from ldv_automation.darstellung import stil\n", "darstellung"),
        ("ablauf/x.py", "from ldv_automation.hintergrund import Auftrag\n", "hintergrund"),
    ],
)
def test_ausw_interne_verstoesse_werden_erkannt(
    tmp_path: Path, datei: str, inhalt: str, teil: str
) -> None:
    dateien = {
        "__init__.py": "",
        "auswertung/__init__.py": "",
        "auswertung/jobs.py": "",
        "darstellung/__init__.py": "",
        "darstellung/stil.py": "",
        "domaene/__init__.py": "",
        "ablauf/__init__.py": "",
        "gui/__init__.py": "",
        "gui/tokens.py": "",
        "hintergrund.py": "",
        "protokoll/__init__.py": "",
        "protokoll/ablage.py": "",
        "sitzung.py": "",
    }
    dateien[datei] = inhalt
    verstoesse = finde_verstoesse(_baum(tmp_path, dateien))
    assert any(teil in v and v.startswith(datei) for v in verstoesse), verstoesse


@pytest.mark.parametrize(
    "inhalt",
    [
        "from ldv_automation.auswertung import jobs\n",
        "from ldv_automation.darstellung import stil\n",
        "from ldv_automation.hintergrund import Auftrag\n",
        "from ldv_automation.auswertung.jobs import lese_job\n",
    ],
)
def test_ausw_gui_darf_auswertung_darstellung_hintergrund_importieren(
    tmp_path: Path, inhalt: str
) -> None:
    dateien = {
        "__init__.py": "",
        "auswertung/__init__.py": "",
        "auswertung/jobs.py": "def lese_job(): ...\n",
        "darstellung/__init__.py": "",
        "darstellung/stil.py": "",
        "gui/__init__.py": "",
        "gui/x.py": inhalt,
        "hintergrund.py": "class Auftrag: ...\n",
    }
    assert finde_verstoesse(_baum(tmp_path, dateien)) == []


@pytest.mark.parametrize(
    "inhalt",
    [
        "import numpy\n",
        "import multiprocessing\nimport scipy\n",
        "from ldv_automation.auswertung import jobs\n",
        "import PySide6\n",
        "import matplotlib\n",
    ],
)
def test_ausw_hintergrund_darf_nur_die_standardbibliothek(tmp_path: Path, inhalt: str) -> None:
    wurzel = _baum(
        tmp_path,
        {
            "__init__.py": "",
            "auswertung/__init__.py": "",
            "auswertung/jobs.py": "",
            "hintergrund.py": inhalt,
        },
    )
    assert externe_verstoesse_hintergrund(wurzel) or finde_verstoesse(wurzel)


def test_ausw_hintergrund_standardbibliothek_ist_erlaubt(tmp_path: Path) -> None:
    wurzel = _baum(
        tmp_path,
        {
            "__init__.py": "",
            "hintergrund.py": "import multiprocessing\nfrom collections.abc import Callable\n",
        },
    )
    assert externe_verstoesse_hintergrund(wurzel) == []
    assert finde_verstoesse(wurzel) == []


def test_ausw_olefile_nur_in_auswertung_nicht_in_darstellung_erlaubt(tmp_path: Path) -> None:
    wurzel = _baum(
        tmp_path,
        {"__init__.py": "", "auswertung/__init__.py": "", "auswertung/x.py": "import olefile\n"},
    )
    assert externe_verstoesse_auswertung(wurzel) == []


# Laufzeitprüfung (Subprozess, frischer Interpreter): ein AST-Test sieht keine indirekten
# Importe über Drittpakete. ``sys.modules`` des Subprozesses zeigt, was wirklich geladen wird.
_LAUFZEIT_SKRIPT = """
import importlib, sys
importlib.import_module({modul!r})
verboten = {verboten!r}
geladen = sorted(m for m in verboten if m in sys.modules)
print("GELADEN:" + ",".join(geladen))
"""


def _geladene_verbotene(modul: str, verboten: tuple[str, ...]) -> list[str]:
    skript = _LAUFZEIT_SKRIPT.format(modul=modul, verboten=verboten)
    lauf = subprocess.run(
        [sys.executable, "-I", "-c", skript],
        check=True,
        capture_output=True,
        text=True,
        env={"PYTHONPATH": str(SRC.parent)},
    )
    zeile = next(z for z in lauf.stdout.splitlines() if z.startswith("GELADEN:"))
    rest = zeile.removeprefix("GELADEN:")
    return rest.split(",") if rest else []


def test_ausw_laufzeit_darstellung_laedt_weder_qt_noch_pyplot() -> None:
    if not (SRC / "darstellung" / "__init__.py").is_file():
        pytest.skip("darstellung/ noch nicht angelegt (kommt mit T2); Regel ist vorbereitet")
    geladen = _geladene_verbotene(
        f"{PAKET}.darstellung", ("PySide6", "shiboken6", "matplotlib.pyplot", "pylab")
    )
    assert geladen == []


def test_ausw_laufzeit_hintergrund_laedt_keine_drittpakete() -> None:
    if not (SRC / "hintergrund.py").is_file():
        pytest.skip("hintergrund.py noch nicht angelegt (kommt mit T1.4)")
    geladen = _geladene_verbotene(
        f"{PAKET}.hintergrund", ("PySide6", "shiboken6", "matplotlib", "numpy", "olefile")
    )
    assert geladen == []


def test_ausw_laufzeit_jobs_laden_kein_qt_und_kein_matplotlib() -> None:
    """Der Worker (spawn) importiert ``auswertung.jobs``: weder Qt noch matplotlib (Startzeit)."""
    if not (SRC / "auswertung" / "jobs.py").is_file():
        pytest.skip("auswertung/jobs.py noch nicht angelegt (kommt mit T1.4)")
    geladen = _geladene_verbotene(
        f"{PAKET}.auswertung.jobs", ("PySide6", "shiboken6", "matplotlib")
    )
    assert geladen == []
