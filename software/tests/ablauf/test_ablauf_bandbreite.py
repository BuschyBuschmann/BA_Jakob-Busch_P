"""BW-2: Rückprobe von Bandbreite, Von und Bis im Ablauf (Simulator; Fälle vom 23.11.)."""

from __future__ import annotations

from dataclasses import replace
from pathlib import Path
from typing import Any, Literal

import pytest
from ablauf_hilfen import Aufbau, aufbau, messung

from ldv_automation.ablauf.steuerung import DurchgangErgebnis
from ldv_automation.domaene.eintraege import MessungZustand
from ldv_automation.domaene.parameter import ParameterWert
from ldv_automation.geraet.schnittstelle import EinstellungsStand, GeraeteFehler
from ldv_automation.geraet.simulator import Simulator, SimulatorKonfiguration

STUFEN = (3125.0, 5000.0, 6250.0, 12500.0)
"""Simulator-Stufen für die Tests (erfunden, keine Gerätewerte)."""


def _lauf(
    tmp_path: Path,
    soll_hz: float,
    *,
    ausserhalb: Literal["einrasten", "ignorieren", "fehler"] = "einrasten",
    von_bis_folgt: bool = True,
) -> tuple[Aufbau, dict[str, object]]:
    a = aufbau(
        tmp_path,
        [messung(tmp_path, "M1", {"fft.bandbreite_hz": soll_hz})],
        sim_konfiguration=SimulatorKonfiguration(
            bandbreiten_hz=STUFEN, bandbreite_ausserhalb=ausserhalb, von_bis_folgt=von_bis_folgt
        ),
    )
    a.starte()
    a.steuerung.bis_ruhe()
    return a, a.protokoll("01_M1")


def test_a2_a3_stufe_6250_von_bis_gesetzt_und_protokolliert(tmp_path: Path) -> None:
    a, p = _lauf(tmp_path, 6250.0)
    assert a.ws.eintraege()[0].zustand is MessungZustand.FERTIG
    assert "starte_scan" in a.sim.aufgerufene_methoden()
    assert p["geaenderte_parameter"] == [
        {"schluessel": "fft.bandbreite_hz", "einheit": "Hz", "soll": 6250.0, "ist": 6250.0},
        {"schluessel": "fft.start_frequenz_hz", "einheit": "Hz", "soll": 0.0, "ist": 0.0},
        {"schluessel": "fft.end_frequenz_hz", "einheit": "Hz", "soll": 6250.0, "ist": 6250.0},
    ]
    ist = p["einstellungen_ist"]
    assert isinstance(ist, dict)
    fft = ist["gruppen"]["fft"]
    assert (fft["bandbreite_hz"], fft["start_frequenz_hz"], fft["end_frequenz_hz"]) == (
        6250.0,
        0.0,
        6250.0,
    )


def test_5600_still_nicht_uebernommen_ist_abweichung_ohne_scan(tmp_path: Path) -> None:
    # 23.11.: PSV behielt 5000 Hz (hier: Standard 3125 Hz); die Rückprobe stoppt vor dem Scan.
    a, p = _lauf(tmp_path, 5600.0, ausserhalb="ignorieren")
    assert a.ws.eintraege()[0].zustand is MessungZustand.FEHLER
    assert "starte_scan" not in a.sim.aufgerufene_methoden()
    fehler = p["fehler"]
    assert isinstance(fehler, dict)
    assert fehler["art"] == "abweichung"
    assert "fft.bandbreite_hz" in str(fehler["text"])


def test_4000_ungueltiger_wert_ist_geraetefehler_ohne_scan(tmp_path: Path) -> None:
    a, p = _lauf(tmp_path, 4000.0, ausserhalb="fehler")
    assert a.ws.eintraege()[0].zustand is MessungZustand.FEHLER
    assert "starte_scan" not in a.sim.aufgerufene_methoden()
    fehler = p["fehler"]
    assert isinstance(fehler, dict)
    assert "Ungültiger Wert" in str(fehler["text"])
    # A3 im Fehlerfall: Von/Bis-Zeilen mit Soll, Ist aus dem danach gelesenen Stand
    assert fehler["art"] == "geraet"
    ist = p["einstellungen_ist"]
    assert isinstance(ist, dict)
    fft = ist["gruppen"]["fft"]
    assert fft["bandbreite_hz"] == 3125.0  # nicht übernommen (Standard des Simulators)
    assert p["geaenderte_parameter"] == [
        {"schluessel": "fft.bandbreite_hz", "einheit": "Hz", "soll": 4000.0, "ist": None},
        {
            "schluessel": "fft.start_frequenz_hz",
            "einheit": "Hz",
            "soll": 0.0,
            "ist": fft["start_frequenz_hz"],
        },
        {
            "schluessel": "fft.end_frequenz_hz",
            "einheit": "Hz",
            "soll": 4000.0,
            "ist": fft["end_frequenz_hz"],
        },
    ]
    assert fft["start_frequenz_hz"] == 0.0
    assert fft["end_frequenz_hz"] == 3125.0


class _StandKaputt:
    """Hülle um den Simulator: ``lies_einstellungsstand`` schlägt fehl."""

    def __init__(self, sim: Simulator) -> None:
        self._sim = sim

    def __getattr__(self, name: str) -> Any:
        return getattr(self._sim, name)

    def lies_einstellungsstand(self) -> EinstellungsStand:
        raise GeraeteFehler("Stand nicht lesbar", methode="lies_einstellungsstand")


def test_4000_fehler_und_stand_nicht_lesbar_behaelt_urspruenglichen_fehler(
    tmp_path: Path,
) -> None:
    a = aufbau(
        tmp_path,
        [messung(tmp_path, "M1", {"fft.bandbreite_hz": 4000.0})],
        sim_konfiguration=SimulatorKonfiguration(
            bandbreiten_hz=STUFEN, bandbreite_ausserhalb="fehler"
        ),
        huelle=_StandKaputt,
    )
    a.starte()
    a.steuerung.bis_ruhe()
    assert a.ws.eintraege()[0].zustand is MessungZustand.FEHLER
    p = a.protokoll("01_M1")
    fehler = p["fehler"]
    assert isinstance(fehler, dict)
    assert "Ungültiger Wert" in str(fehler["text"])  # nicht durch das Lesen überdeckt
    assert p["einstellungen_ist"] is None
    assert p["geaenderte_parameter"] == [
        {"schluessel": "fft.bandbreite_hz", "einheit": "Hz", "soll": 4000.0, "ist": None},
        {"schluessel": "fft.start_frequenz_hz", "einheit": "Hz", "soll": 0.0, "ist": None},
        {"schluessel": "fft.end_frequenz_hz", "einheit": "Hz", "soll": 4000.0, "ist": None},
    ]


def test_bis_bleibt_ist_abweichung_wie_am_23_11(tmp_path: Path) -> None:
    a, p = _lauf(tmp_path, 6250.0, von_bis_folgt=False)
    assert a.ws.eintraege()[0].zustand is MessungZustand.FEHLER
    assert "starte_scan" not in a.sim.aufgerufene_methoden()
    fehler = p["fehler"]
    assert isinstance(fehler, dict)
    assert fehler["art"] == "abweichung"
    assert "fft.end_frequenz_hz: Soll 6250.0, Ist 3125.0" in str(fehler["text"])
    assert "fft.start_frequenz_hz" not in str(fehler["text"])  # Von = 0 stimmt
    # der Ist-Stand steht trotzdem im Protokoll (Nachweis)
    ist = p["einstellungen_ist"]
    assert isinstance(ist, dict)
    assert ist["gruppen"]["fft"]["end_frequenz_hz"] == 3125.0


class _OhneBis:
    """Hülle um den Simulator: ``EndFrequency`` ist nicht lesbar (``None``)."""

    def __init__(self, sim: Simulator) -> None:
        self._sim = sim

    def __getattr__(self, name: str) -> Any:
        return getattr(self._sim, name)

    def lies_einstellungsstand(self) -> EinstellungsStand:
        stand = self._sim.lies_einstellungsstand()
        fft = {**stand.gruppen["fft"], "end_frequenz_hz": None}
        return replace(stand, gruppen={**stand.gruppen, "fft": fft})


def test_nicht_lesbares_bis_ist_abweichung(tmp_path: Path) -> None:
    a = aufbau(
        tmp_path,
        [messung(tmp_path, "M1", {"fft.bandbreite_hz": 6250.0})],
        sim_konfiguration=SimulatorKonfiguration(bandbreiten_hz=STUFEN),
        huelle=_OhneBis,
    )
    a.starte()
    a.steuerung.bis_ruhe()
    assert a.ws.eintraege()[0].zustand is MessungZustand.FEHLER
    assert "starte_scan" not in a.sim.aufgerufene_methoden()
    fehler = a.protokoll("01_M1")["fehler"]
    assert isinstance(fehler, dict)
    assert "fft.end_frequenz_hz: Soll 6250.0, Ist None" in str(fehler["text"])


@pytest.mark.parametrize("parameter", [{}, {"fft.linien": 400}, {"mittelung.anzahl": 5}])
def test_ohne_bandbreite_keine_von_bis_pruefung(
    tmp_path: Path, parameter: dict[str, ParameterWert]
) -> None:
    a = aufbau(
        tmp_path,
        [messung(tmp_path, "M1", parameter)],
        sim_konfiguration=SimulatorKonfiguration(bandbreiten_hz=STUFEN, von_bis_folgt=False),
    )
    a.starte()
    a.steuerung.bis_ruhe()
    assert a.steuerung.momentaufnahme().ergebnis is DurchgangErgebnis.VOLLSTAENDIG
    p = a.protokoll("01_M1")
    zeilen = p["geaenderte_parameter"]
    assert isinstance(zeilen, list)
    assert not any("frequenz" in z["schluessel"] for z in zeilen)
