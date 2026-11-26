"""BW-2: Rückprobe von Bandbreite, Von und Bis im Ablauf (Simulator; Fälle vom 23.11.)."""

from __future__ import annotations

from dataclasses import replace
from pathlib import Path
from types import SimpleNamespace
from typing import Any, Literal

import pytest
from ablauf_hilfen import Aufbau, aufbau, messung

from ldv_automation.ablauf.steuerung import DurchgangErgebnis, DurchgangZustand, Steuerung
from ldv_automation.domaene.eintraege import Messung, MessungZustand
from ldv_automation.domaene.parameter import ParameterWert
from ldv_automation.geraet.schnittstelle import (
    EinstellungsStand,
    GeraeteFehler,
    GeraetNichtBereitFehler,
    VerweigertFehler,
)
from ldv_automation.geraet.simulator import LangsamerAufruf, Simulator, SimulatorKonfiguration

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
        {"schluessel": "fft.bandbreite_hz", "einheit": "Hz", "soll": 4000.0, "ist": 3125.0},
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


def test_4000_nachlesen_ueber_der_aufrufgrenze_ist_ein_haenger(tmp_path: Path) -> None:
    # K-U2b gilt auch beim Nachlesen im Fehlerpfad: GERAET_UNKLAR, keine weiteren Aufrufe.
    a = aufbau(
        tmp_path,
        [messung(tmp_path, "M1", {"fft.bandbreite_hz": 4000.0})],
        sim_konfiguration=SimulatorKonfiguration(
            bandbreiten_hz=STUFEN, bandbreite_ausserhalb="fehler"
        ),
        drehbuch=[LangsamerAufruf(vorgang=0, methode="lies_einstellungsstand", dauer_s=61.0)],
    )
    a.starte()
    a.steuerung.bis_ruhe()
    assert a.steuerung.zustand is DurchgangZustand.GERAET_UNKLAR
    assert a.steuerung._aufruf_haengt is True
    assert "starte_scan" not in a.sim.aufgerufene_methoden()
    p = a.protokoll("01_M1")
    fehler = p["fehler"]
    assert isinstance(fehler, dict)
    assert fehler["art"] == "geraet_unklar"
    assert "lies_einstellungsstand" in str(fehler["text"])
    assert "hängt" in str(fehler["text"])
    assert "Ungültiger Wert für Bandbreite" in str(fehler["text"])  # ursprünglicher Fehler
    assert any("hängt" in e.text for e in a.ereignisse if e.art == "fehler")
    assert p["einstellungen_ist"] is None


class _SetzenScheitert:
    """Hülle um den Simulator: ``setze_parameter`` wirft einen vorgegebenen Gerätefehler."""

    def __init__(self, sim: Simulator, fehler: GeraeteFehler) -> None:
        self._sim = sim
        self._fehler = fehler

    def __getattr__(self, name: str) -> Any:
        return getattr(self._sim, name)

    def setze_parameter(self, parameter: Any) -> None:
        raise self._fehler


@pytest.mark.parametrize(
    "fehler",
    [
        GeraetNichtBereitFehler("Simulator: nicht bereit (Test)", methode="setze_parameter"),
        VerweigertFehler("Simulator: verweigert (Test)", methode="setze_parameter"),
    ],
)
def test_nachlesen_haengt_nach_nicht_bereit_und_verweigert_ist_geraet_unklar(
    tmp_path: Path, fehler: GeraeteFehler
) -> None:
    a = aufbau(
        tmp_path,
        [messung(tmp_path, "M1", {"fft.bandbreite_hz": 6250.0})],
        sim_konfiguration=SimulatorKonfiguration(bandbreiten_hz=STUFEN),
        drehbuch=[LangsamerAufruf(vorgang=0, methode="lies_einstellungsstand", dauer_s=61.0)],
        huelle=lambda sim: _SetzenScheitert(sim, fehler),
    )
    a.starte()
    a.steuerung.bis_ruhe()
    assert a.steuerung.zustand is DurchgangZustand.GERAET_UNKLAR
    assert a.steuerung._aufruf_haengt is True
    fehler_feld = a.protokoll("01_M1")["fehler"]
    assert isinstance(fehler_feld, dict)
    assert fehler_feld["art"] == "geraet_unklar"  # nicht die Art des ursprünglichen Fehlers
    assert "hängt" in str(fehler_feld["text"])
    assert fehler.text in str(fehler_feld["text"])


class _OhneBandbreiteImRueckgabewert:
    """Hülle um den Simulator: ``lies_parameter`` lässt ``fft.bandbreite_hz`` weg."""

    def __init__(self, sim: Simulator) -> None:
        self._sim = sim

    def __getattr__(self, name: str) -> Any:
        return getattr(self._sim, name)

    def lies_parameter(self, schluessel: Any) -> dict[str, ParameterWert]:
        ist = dict(self._sim.lies_parameter(schluessel))
        ist.pop("fft.bandbreite_hz", None)
        return ist


def test_rueckprobe_ohne_ist_bleibt_none_und_wird_nicht_aus_dem_stand_ergaenzt(
    tmp_path: Path,
) -> None:
    a = aufbau(
        tmp_path,
        [messung(tmp_path, "M1", {"fft.bandbreite_hz": 5000.0})],
        sim_konfiguration=SimulatorKonfiguration(bandbreiten_hz=STUFEN),
        huelle=_OhneBandbreiteImRueckgabewert,
    )
    a.starte()
    a.steuerung.bis_ruhe()
    p = a.protokoll("01_M1")
    fehler = p["fehler"]
    assert isinstance(fehler, dict)
    assert fehler["art"] == "abweichung"
    assert "fft.bandbreite_hz: Soll 5000.0, Ist None" in str(fehler["text"])
    zeilen = p["geaenderte_parameter"]
    assert isinstance(zeilen, list)
    bandbreite = next(z for z in zeilen if z["schluessel"] == "fft.bandbreite_hz")
    assert bandbreite["ist"] is None  # der Stand zeigt 5000, die Rückprobe aber nichts


def test_geaenderte_zeilen_veraendert_den_messungszustand_nicht() -> None:
    messung_ = Messung(
        name="M1", einstellungsdatei="x.set", parameter={"fft.bandbreite_hz": 5000.0}
    )
    zeile = {"schluessel": "fft.bandbreite_hz", "einheit": "Hz", "soll": 5000.0, "ist": None}
    aktiv = SimpleNamespace(
        messung=messung_,
        geaenderte=[zeile],
        einstellungen_ist={"gruppen": {"fft": {"bandbreite_hz": 5000.0, "start_frequenz_hz": 0.0}}},
    )
    zeilen = Steuerung._geaenderte_zeilen(aktiv)  # type: ignore[arg-type]
    assert zeile == {
        "schluessel": "fft.bandbreite_hz",
        "einheit": "Hz",
        "soll": 5000.0,
        "ist": None,
    }
    assert len(aktiv.geaenderte) == 1  # Von/Bis nur in der Rückgabe ergänzt
    assert zeilen[0] is not zeile
    assert zeilen[0]["ist"] is None
    assert [z["schluessel"] for z in zeilen[1:]] == [
        "fft.start_frequenz_hz",
        "fft.end_frequenz_hz",
    ]
    assert zeilen[1]["ist"] == 0.0 and zeilen[2]["ist"] is None


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
