"""BW-2: Bandbreite nur als PSV-Stufe, Von/Bis mitsetzen (Adapter und Richtlinie, COM-Fake)."""

from __future__ import annotations

import math
from typing import Any

import pytest
from fake_psv_com import FakeBindung, Welt, baue_psv
from test_geraet_com_adapter import SET, WURZEL, _geraet

from ldv_automation.geraet.com.adapter import ComBetriebsart, ComKonfiguration, PsvComGeraet
from ldv_automation.geraet.com.richtlinie import PRODUKTIV, frequenzbereich_pruefung
from ldv_automation.geraet.com.whitelist import ProxyKontext
from ldv_automation.geraet.schnittstelle import GeraeteFehler

STUFEN = (1250.0, 2500.0, 5000.0, 6250.0, 10000.0)
"""Fake-Stufen (erfunden; am Gerät unbestätigt)."""


def test_verbinde_liest_stufenliste() -> None:
    geraet, _, _ = _geraet()
    info = geraet.verbinde()
    assert info.bandbreiten_stufen_hz == STUFEN
    assert info.bandbreiten_stufen_fehler == ""


@pytest.mark.parametrize(
    "roh",
    [(), "5000", 5000.0, (5000.0, "x"), (5000.0, True), (5000.0, math.nan), (0.0,), (-1.0,)],
)
def test_verbinde_unlesbare_stufenliste_ist_none_mit_grund(roh: Any) -> None:
    geraet, _, _ = _geraet(stufen_roh=roh)
    info = geraet.verbinde()
    assert info.bandbreiten_stufen_hz is None
    assert info.bandbreiten_stufen_fehler


@pytest.mark.parametrize("roh", [(), "5000", (5000.0, "x")])
def test_setzen_mit_unlesbarer_liste_ist_fail_closed(roh: Any) -> None:
    geraet, fake, _ = _geraet(stufen_roh=roh)
    geraet.verbinde()
    with pytest.raises(GeraeteFehler):
        geraet.setze_parameter({"fft.bandbreite_hz": 5000.0})
    assert not [o for o in fake.welt.schreibende() if o.startswith("Fft")]


def test_stufenliste_als_liste_wird_akzeptiert() -> None:
    geraet, _, _ = _geraet(stufen_roh=[5000.0, 6250])
    assert geraet.verbinde().bandbreiten_stufen_hz == (5000.0, 6250.0)


@pytest.mark.parametrize("soll", [5600.0, 4000.0])
def test_a1_nicht_stufe_wird_vor_dem_schreiben_abgelehnt(soll: float) -> None:
    geraet, fake, _ = _geraet()
    geraet.verbinde()
    with pytest.raises(GeraeteFehler, match="keine PSV-Stufe"):
        geraet.setze_parameter({"fft.bandbreite_hz": soll, "fft.linien": 800})
    assert not [o for o in fake.welt.schreibende() if o.startswith("Fft")]


def test_a2_stufe_6250_setzt_von_bis_und_liest_zurueck() -> None:
    geraet, fake, _ = _geraet()
    geraet.verbinde()
    geraet.setze_parameter({"fft.bandbreite_hz": 6250.0})
    folge = fake.welt.schreibende()
    assert folge.index("FftValidator.Bandwidth:set") < folge.index(
        "FftValidator.StartFrequency:set"
    )
    assert folge.index("FftValidator.StartFrequency:set") < folge.index(
        "FftProperties.FftAcqPropertiesValidator:set"
    )
    gruppe = geraet.lies_einstellungsstand().gruppen["fft"]
    assert gruppe["bandbreite_hz"] == 6250.0
    assert gruppe["start_frequenz_hz"] == 0.0
    assert gruppe["end_frequenz_hz"] == 6250.0


def test_von_bis_folgt_nach_linien_im_validator() -> None:
    geraet, fake, _ = _geraet()
    geraet.verbinde()
    geraet.setze_parameter({"fft.bandbreite_hz": 6250.0, "fft.linien": 800})
    folge = fake.welt.schreibende()
    assert folge.index("FftValidator.Lines:set") < folge.index("FftValidator.EndFrequency:set")


def test_ohne_bandbreite_bleiben_von_bis_unberuehrt() -> None:
    geraet, fake, _ = _geraet()
    geraet.verbinde()
    geraet.setze_parameter({"fft.linien": 800})
    assert not [o for o in fake.welt.schreibende() if "Frequency" in o]


def test_bis_bleibt_wird_zurueckgelesen_sichtbar() -> None:
    # Verhalten vom 23.11.: Bis folgt nicht; der Adapter meldet es nicht selbst, die Rückprobe
    # (Steuerung) wertet den Einstellungsstand aus.
    geraet, _, _ = _geraet(end_ignorieren=True)
    geraet.verbinde()
    geraet.setze_parameter({"fft.bandbreite_hz": 6250.0})
    gruppe = geraet.lies_einstellungsstand().gruppen["fft"]
    assert gruppe["bandbreite_hz"] == 6250.0
    assert gruppe["end_frequenz_hz"] == 5000.0


def test_stufenliste_wird_beim_setzen_erneut_gelesen() -> None:
    geraet, fake, _ = _geraet()
    geraet.verbinde()
    vorher = sum(1 for a in geraet.aufrufe() if a.pfad == "FftValidator.AvailableBandwidths")
    geraet.setze_parameter({"fft.bandbreite_hz": 5000.0})
    nachher = sum(1 for a in geraet.aufrufe() if a.pfad == "FftValidator.AvailableBandwidths")
    assert nachher == vorher + 1
    assert fake.welt.schreibende()


def test_nur_lesen_liest_stufen_schreibt_aber_nichts() -> None:
    welt = Welt()
    welt.dateien.add(SET)
    fake = baue_psv(welt)
    geraet = PsvComGeraet(
        FakeBindung(fake, prozess=True),
        ComKonfiguration(
            betriebsart=ComBetriebsart.NUR_LESEN,
            messdaten_wurzel=WURZEL,
            existiert=lambda p: p in welt.dateien,
        ),
    )
    assert geraet.verbinde().bandbreiten_stufen_hz == STUFEN
    assert not [o for o in welt.schreibende() if o.startswith(("Fft", "Average"))]


def _kontext(schreiben: bool = True) -> ProxyKontext:
    return ProxyKontext(schreiben_erlaubt=schreiben)


@pytest.mark.parametrize("typ", ["FftValidator", "FftProperties"])
@pytest.mark.parametrize("name", ["StartFrequency", "EndFrequency"])
def test_richtlinie_frequenz_schreibrecht_pruefung(typ: str, name: str) -> None:
    recht = PRODUKTIV.schreiben[typ][name]
    assert recht.begruendung.startswith(("S3", "S4"))
    von, bis = frequenzbereich_pruefung()
    pruefe = von if name == "StartFrequency" else bis
    kontext = _kontext()
    assert pruefe(0.0, kontext) is None
    assert pruefe(6250.0, kontext) is None
    assert pruefe(-1.0, kontext) is not None
    assert pruefe(math.inf, kontext) is not None
    assert pruefe(math.nan, kontext) is not None
    assert pruefe(0, kontext) is not None  # int statt float
    assert pruefe(True, kontext) is not None
    assert pruefe("5000", kontext) is not None
    assert pruefe(5000.0, _kontext(schreiben=False)) is not None
