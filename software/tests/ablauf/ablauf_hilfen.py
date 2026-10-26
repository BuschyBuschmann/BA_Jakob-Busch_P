"""Gemeinsame Hilfen der Ablauftests (Simulator, Testuhr, Steuerung)."""

from __future__ import annotations

import json
from collections.abc import Callable, Sequence
from dataclasses import dataclass, field
from pathlib import Path

from ldv_automation.ablauf.fehlerstrategie import Fehlerstrategie
from ldv_automation.ablauf.steuerung import (
    AblaufEreignis,
    AblaufKonfiguration,
    DurchgangsAuftrag,
    DurchgangZustand,
    Steuerung,
)
from ldv_automation.ablauf.uhr import Testuhr
from ldv_automation.domaene.eintraege import Eintrag, Messung
from ldv_automation.domaene.parameter import ParameterWert
from ldv_automation.domaene.warteschlange import Warteschlange
from ldv_automation.geraet.simulator import (
    DrehbuchEreignis,
    Simulator,
    SimulatorKonfiguration,
)
from ldv_automation.protokoll.version import BuildInfo

GIT_HASH = "0123456789abcdef0123456789abcdef01234567"
BUILD = BuildInfo(paket_version="0.1.0", git_hash=GIT_HASH, git_dirty=False, quelle="test")

SCHREIBAUFRUFE = frozenset(
    {
        "lade_einstellungen",
        "setze_parameter",
        "speichere_einstellungen",
        "starte_scan",
        "stoppe",
        "setze_messfreigabe",
    }
)


def set_datei(ordner: Path, name: str = "basis.set") -> str:
    pfad = ordner / name
    if not pfad.exists():
        pfad.write_bytes(b"SET-PLATZHALTER")
    return str(pfad)


def messung(
    ordner: Path,
    name: str,
    parameter: dict[str, ParameterWert] | None = None,
    zeitlimit_s: float | None = None,
) -> Messung:
    return Messung(
        name=name,
        einstellungsdatei=set_datei(ordner),
        parameter=parameter or {},
        zeitlimit_s=zeitlimit_s,
    )


@dataclass
class Aufbau:
    steuerung: Steuerung
    sim: Simulator
    uhr: Testuhr
    wurzel: Path
    ereignisse: list[AblaufEreignis] = field(default_factory=list)

    @property
    def ws(self) -> Warteschlange:
        return self.steuerung.warteschlange

    def starte(self, *, trockenlauf: bool = False, freigabe: bool = True) -> None:
        self.steuerung.starte(
            DurchgangsAuftrag(
                name="Test",
                messdaten_wurzel=self.wurzel,
                betriebsart="trockenlauf" if trockenlauf else "simulator",
                trockenlauf=trockenlauf,
                messfreigabe=freigabe,
            )
        )

    def laufe_bis(self, bedingung: Callable[[], bool], max_schritte: int = 10_000) -> None:
        for _ in range(max_schritte):
            if bedingung():
                return
            self.steuerung.schritt()
            if self.steuerung.braucht_takt():
                self.uhr.sleep(AblaufKonfiguration().poll_s)
        raise AssertionError("Bedingung nicht erreicht")

    def ordner(self) -> Path:
        ordner = self.steuerung.momentaufnahme().durchgangsordner
        assert ordner is not None
        return ordner

    def protokoll(self, basis: str) -> dict[str, object]:
        daten = json.loads((self.ordner() / f"{basis}.protokoll.json").read_text("utf-8"))
        assert isinstance(daten, dict)
        return daten

    def ereignisprotokoll(self) -> list[dict[str, object]]:
        zeilen = (self.ordner() / "durchgang.ereignisse.jsonl").read_text("utf-8").splitlines()
        return [json.loads(z) for z in zeilen]

    def durchgang_wechsel(self) -> list[str]:
        return [str(e.daten["nach"]) for e in self.ereignisse if e.art == "durchgang_zustand"]


def aufbau(
    tmp_path: Path,
    eintraege: Sequence[Eintrag],
    *,
    drehbuch: Sequence[DrehbuchEreignis] = (),
    sim_konfiguration: SimulatorKonfiguration | None = None,
    konfiguration: AblaufKonfiguration | None = None,
    strategie: Fehlerstrategie | None = None,
    build: BuildInfo = BUILD,
    betriebsart: str = "simulator",
    verbinden: bool = True,
) -> Aufbau:
    uhr = Testuhr()
    sim = Simulator(
        uhr.monotonic,
        betriebsart=betriebsart,
        konfiguration=sim_konfiguration,
        drehbuch=drehbuch,
        schlafen=uhr.sleep,
    )
    wurzel = tmp_path / "messdaten"
    wurzel.mkdir(exist_ok=True)
    ereignisse: list[AblaufEreignis] = []
    steuerung = Steuerung(
        warteschlange=Warteschlange(eintraege),
        geraet=sim,
        betriebsart=betriebsart,
        uhr=uhr,
        build_info=build,
        fehlerstrategie=strategie,
        konfiguration=konfiguration,
        bei_ereignis=ereignisse.append,
    )
    ergebnis = Aufbau(steuerung=steuerung, sim=sim, uhr=uhr, wurzel=wurzel, ereignisse=ereignisse)
    if verbinden:
        steuerung.verbinde()
        steuerung.schritt()
        assert steuerung.momentaufnahme().verbindung is not None
    return ergebnis


def ist_zustand(a: Aufbau, zustand: DurchgangZustand) -> Callable[[], bool]:
    return lambda: a.steuerung.zustand is zustand
