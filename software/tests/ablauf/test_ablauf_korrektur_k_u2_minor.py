"""Korrekturpaket K-U2, Erweiterung: MINOR-5 (NaN/Inf) und Nitpicks (Steuerung, Protokoll)."""

from __future__ import annotations

import json
import math
from datetime import datetime, timedelta, timezone
from pathlib import Path

from ablauf_hilfen import aufbau, messung

from ldv_automation.ablauf.fehlerstrategie import FehlerEreignis, FehlerReaktion
from ldv_automation.ablauf.steuerung import DurchgangErgebnis, DurchgangZustand, Fehlerentscheidung
from ldv_automation.geraet.schnittstelle import EinstellungsStand
from ldv_automation.geraet.simulator import Haenger, StartFehler
from ldv_automation.protokoll.messprotokoll import Ereignisprotokoll, json_sicher

# --- MINOR-5 --------------------------------------------------------------------------


def test_json_sicher_ersetzt_nicht_endliche_werte() -> None:
    wert = {
        "a": math.nan,
        "b": [math.inf, -math.inf, 1.5, (2, math.nan)],
        "c": {"d": "Text", "e": None, "f": 3},
    }
    assert json_sicher(wert) == {
        "a": "NaN",
        "b": ["Infinity", "-Infinity", 1.5, [2, "NaN"]],
        "c": {"d": "Text", "e": None, "f": 3},
    }


def test_minor_5_nan_im_einstellungsstand_verhindert_protokoll_nicht(tmp_path: Path) -> None:
    a = aufbau(tmp_path, [messung(tmp_path, "M1")])
    original = a.sim.lies_einstellungsstand

    def mit_nan() -> EinstellungsStand:
        stand = original()
        return EinstellungsStand(
            modus=stand.modus,
            messpunkte_anzahl=stand.messpunkte_anzahl,
            generator_aktiv=False,
            generator_amplitude_v=math.nan,
            gruppen={"fft": {"start_frequenz_hz": math.inf, "linien": 800}},
        )

    a.sim.lies_einstellungsstand = mit_nan  # type: ignore[method-assign]
    a.starte()
    a.steuerung.bis_ruhe()
    assert a.steuerung.momentaufnahme().ergebnis is DurchgangErgebnis.VOLLSTAENDIG
    text = (a.ordner() / "01_M1.protokoll.json").read_text("utf-8")
    p = json.loads(text)  # gültiges JSON (kein nacktes NaN)
    assert p["status"] == "fertig"
    assert p["einstellungen_ist"]["generator_amplitude_v"] == "NaN"
    assert p["einstellungen_ist"]["gruppen"]["fft"]["start_frequenz_hz"] == "Infinity"
    assert not any(e.art == "fehler" for e in a.ereignisse)


def test_minor_5_ereignisprotokoll_bleibt_gueltiges_json(tmp_path: Path) -> None:
    pfad = tmp_path / "e.jsonl"
    protokoll = Ereignisprotokoll(pfad)
    protokoll.schreibe(
        datetime(2026, 11, 2, tzinfo=timezone(timedelta(hours=1))), "x", {"wert": -math.inf}
    )
    assert json.loads(pfad.read_text("utf-8"))["wert"] == "-Infinity"


# --- Nitpicks -------------------------------------------------------------------------


class Spion:
    def __init__(self) -> None:
        self.befragt = 0

    @property
    def bezeichnung(self) -> str:
        return "Spion"

    def entscheide(self, ereignis: FehlerEreignis) -> FehlerReaktion:
        self.befragt += 1
        return FehlerReaktion.ANHALTEN_UND_FRAGEN


def test_nitpick_fehler_waehrend_abbruch_entfaellt_entscheidung(tmp_path: Path) -> None:
    spion = Spion()
    a = aufbau(
        tmp_path,
        [messung(tmp_path, "M1", zeitlimit_s=2.0), messung(tmp_path, "M2")],
        drehbuch=[Haenger(vorgang=0)],
        strategie=spion,
    )
    a.starte()
    a.laufe_bis(lambda: "stoppe" in a.sim.aufgerufene_methoden())  # Zeitlimit-Stop läuft
    a.steuerung.brich_ab()
    a.steuerung.bis_ruhe()
    stand = a.steuerung.momentaufnahme()
    assert stand.durchgang is DurchgangZustand.BEENDET
    assert stand.ergebnis is DurchgangErgebnis.ABGEBROCHEN
    p = a.protokoll("01_M1")
    assert p["status"] == "fehler"
    assert p["fehlerentscheidung"] == "entfaellt_abbruch"
    assert spion.befragt == 0
    assert a.sim.aufgerufene_methoden().count("stoppe") == 1


def test_nitpick_zusammenfassung_wiederholung_nicht_gestartet(tmp_path: Path) -> None:
    a = aufbau(
        tmp_path,
        [messung(tmp_path, "M1"), messung(tmp_path, "M2")],
        drehbuch=[StartFehler(vorgang=0)],
    )
    a.starte()
    a.steuerung.bis_ruhe()
    # Wiederholen und Abbrechen im selben Takt: Messung 1 ist wieder WARTEND mit Versuch 2
    a.steuerung.entscheide(Fehlerentscheidung.WIEDERHOLEN)
    a.steuerung.brich_ab()
    a.steuerung.schritt()
    assert a.steuerung.zustand is DurchgangZustand.BEENDET
    ende = next(z for z in a.ereignisprotokoll() if z["art"] == "durchgang_beendet")
    eintraege = ende["eintraege"]
    assert isinstance(eintraege, list)
    hinweise = [e["hinweis"] for e in eintraege]
    assert hinweise[0].startswith("Wiederholung (Versuch 2) nicht gestartet")
    assert hinweise[1] == "nicht gestartet"
