"""Simulator der Geräteschnittstelle (Plan P2, Abschnitt 5)."""

from __future__ import annotations

import threading
from collections.abc import Callable
from pathlib import Path

import pytest

from ldv_automation.ablauf.uhr import Testuhr
from ldv_automation.geraet.schnittstelle import (
    GeraeteFehler,
    GeraeteZustand,
    GeraetNichtBereitFehler,
    Messgeraet,
    VerweigertFehler,
    ZeitlimitFehler,
)
from ldv_automation.geraet.simulator import (
    SIMULATOR_KENNUNG,
    HaengenderAufruf,
    Haenger,
    MeldungBeiPunkt,
    Simulator,
    SimulatorKonfiguration,
)


def _sim(uhr: Testuhr, betriebsart: str = "simulator", **konf: object) -> Simulator:
    sim = Simulator(
        uhr.monotonic,
        betriebsart=betriebsart,
        konfiguration=SimulatorKonfiguration(**konf),  # type: ignore[arg-type]
    )
    sim.verbinde()
    return sim


def _set(tmp_path: Path) -> str:
    pfad = tmp_path / "a.set"
    pfad.write_bytes(b"x")
    return str(pfad)


def test_erfuellt_protocol() -> None:
    assert isinstance(Simulator(Testuhr().monotonic), Messgeraet)


def test_unbekannte_betriebsart_und_drehbuch() -> None:
    with pytest.raises(ValueError, match="Betriebsart"):
        Simulator(Testuhr().monotonic, betriebsart="volle_kraft")
    with pytest.raises(ValueError, match="Vorgang"):
        Simulator(Testuhr().monotonic, drehbuch=[Haenger(vorgang=-1)])


@pytest.mark.parametrize(
    ("feld", "wert"),
    [("punkte_anzahl", 0), ("punktdauer_s", 0.0), ("bandbreiten_hz", ())],
)
def test_konfiguration_prueft(feld: str, wert: object) -> None:
    with pytest.raises(ValueError):
        SimulatorKonfiguration(**{feld: wert})  # type: ignore[arg-type]


def test_verbinden_startet_psv_nie() -> None:
    sim = Simulator(Testuhr().monotonic, konfiguration=SimulatorKonfiguration(psv_laeuft=False))
    with pytest.raises(GeraeteFehler, match="läuft nicht"):
        sim.verbinde()
    with pytest.raises(GeraeteFehler, match="nicht verbunden"):
        sim.zustand()


def test_info_beim_verbinden() -> None:
    sim = Simulator(
        Testuhr().monotonic,
        konfiguration=SimulatorKonfiguration(meldungen_unterdrueckt=False),
    )
    info = sim.verbinde()
    assert info.psv_version == "10.x-SIM"
    assert info.zustand is GeraeteZustand.GESTOPPT
    assert not info.meldungen_unterdrueckt
    assert info.lademaske == ""


def test_einrasten_und_ganzzahlen(tmp_path: Path) -> None:
    sim = _sim(Testuhr(), bandbreiten_hz=(3125.0, 6250.0, 12500.0))
    sim.lade_einstellungen(_set(tmp_path))
    sim.setze_parameter({"fft.bandbreite_hz": 5000.0, "fft.linien": 700, "mittelung.typ": "Off"})
    ist = sim.lies_parameter(["fft.bandbreite_hz", "fft.linien", "mittelung.typ"])
    assert ist == {"fft.bandbreite_hz": 6250.0, "fft.linien": 800, "mittelung.typ": "Off"}
    assert type(ist["fft.linien"]) is int
    with pytest.raises(GeraeteFehler, match="unbekannte"):
        sim.lies_parameter(["gibt.es_nicht"])
    with pytest.raises(GeraeteFehler, match="unbekannter Parameter"):
        sim.setze_parameter({"gibt.es_nicht": 1})


def test_einrasten_bei_gleichem_abstand_nach_oben(tmp_path: Path) -> None:
    sim = _sim(Testuhr(), bandbreiten_hz=(1000.0, 3000.0))
    sim.lade_einstellungen(_set(tmp_path))
    sim.setze_parameter({"fft.bandbreite_hz": 2000.0})
    assert sim.lies_parameter(["fft.bandbreite_hz"]) == {"fft.bandbreite_hz": 3000.0}


def test_ungueltige_mittelung(tmp_path: Path) -> None:
    sim = _sim(Testuhr())
    sim.lade_einstellungen(_set(tmp_path))
    with pytest.raises(GeraeteFehler, match="Mittelungsanzahl 2"):
        sim.setze_parameter({"mittelung.anzahl": 2})


def test_validator_fehlt_und_rueckfall(tmp_path: Path) -> None:
    ohne = _sim(Testuhr(), validator_vorhanden=False)
    ohne.lade_einstellungen(_set(tmp_path))
    with pytest.raises(GeraeteFehler, match="Validator fehlt"):
        ohne.setze_parameter({"fft.linien": 800})
    ohne.setze_parameter({"mittelung.anzahl": 4})  # ohne FFT-Parameter kein Validator nötig
    rueck = _sim(Testuhr(), validator_vorhanden=False, rueckfall_direkt=True)
    rueck.lade_einstellungen(_set(tmp_path))
    rueck.setze_parameter({"fft.linien": 800})
    assert rueck.lies_parameter(["fft.linien"]) == {"fft.linien": 800}


def test_unbekannte_einstellungsdatei(tmp_path: Path) -> None:
    sim = _sim(Testuhr())
    with pytest.raises(GeraeteFehler, match="unbekannt"):
        sim.lade_einstellungen(str(tmp_path / "fehlt.set"))


@pytest.mark.parametrize("art", ["nur_lesen", "trockenlauf"])
def test_betriebsart_wird_durchgesetzt(tmp_path: Path, art: str) -> None:
    sim = _sim(Testuhr(), betriebsart=art)
    with pytest.raises(VerweigertFehler):
        sim.setze_messfreigabe(True)
    with pytest.raises(VerweigertFehler, match="starte_scan"):
        sim.starte_scan(str(tmp_path / "x.svd"))
    if art == "nur_lesen":
        aufrufe: tuple[Callable[[], None], ...] = (
            lambda: sim.lade_einstellungen(_set(tmp_path)),
            lambda: sim.setze_parameter({"fft.linien": 800}),
            lambda: sim.speichere_einstellungen(str(tmp_path / "e.set")),
        )
        for aufruf in aufrufe:
            with pytest.raises(VerweigertFehler):
                aufruf()
    else:
        sim.lade_einstellungen(_set(tmp_path))
        sim.speichere_einstellungen(str(tmp_path / "e.set"))
        with pytest.raises(VerweigertFehler, match="existiert"):
            sim.speichere_einstellungen(str(tmp_path / "e.set"))
    sim.setze_messfreigabe(False)
    assert sim.stoppe() is False


def test_scan_ablauf_datei_und_zustaende(tmp_path: Path) -> None:
    uhr = Testuhr()
    sim = _sim(uhr, punkte_anzahl=4, punktdauer_s=2.0)
    ziel = str(tmp_path / "m.svd")
    with pytest.raises(VerweigertFehler, match="Messfreigabe"):
        sim.starte_scan(ziel)
    sim.setze_messfreigabe(True)
    with pytest.raises(VerweigertFehler, match="leer"):
        sim.starte_scan("")
    sim.lade_einstellungen(_set(tmp_path))
    sim.starte_scan(ziel)
    assert Path(ziel).read_bytes().startswith(SIMULATOR_KENNUNG)
    assert sim.zustand() is GeraeteZustand.SCANNT
    assert sim.fortschritt() is None
    with pytest.raises(GeraetNichtBereitFehler):
        sim.starte_scan(str(tmp_path / "n.svd"))
    uhr.vorstellen(8.0)
    assert sim.zustand() is GeraeteZustand.GESTOPPT
    assert sim.stoppe() is False  # natürliches Ende: No-op
    with pytest.raises(VerweigertFehler, match="existiert"):
        sim.starte_scan(ziel)


def test_stop_eigener_scan_und_ohne_scan(tmp_path: Path) -> None:
    sim = _sim(Testuhr())
    assert sim.stoppe() is False
    sim.setze_messfreigabe(True)
    sim.lade_einstellungen(_set(tmp_path))
    sim.starte_scan(str(tmp_path / "m.svd"))
    assert sim.stoppe() is True
    assert sim.zustand() is GeraeteZustand.GESTOPPT


def test_fremde_messung(tmp_path: Path) -> None:
    sim = _sim(Testuhr(), fremde_messung=True)
    sim.setze_messfreigabe(True)
    assert sim.zustand() is GeraeteZustand.BESCHAEFTIGT
    with pytest.raises(GeraetNichtBereitFehler):
        sim.starte_scan(str(tmp_path / "m.svd"))
    assert sim.stoppe() is False  # fremden Scan nie stoppen
    sim.fremde_messung_beenden()
    assert sim.zustand() is GeraeteZustand.GESTOPPT


def test_fortschritt_und_meldungen(tmp_path: Path) -> None:
    uhr = Testuhr()
    sim = Simulator(
        uhr.monotonic,
        konfiguration=SimulatorKonfiguration(fortschritt_ereignisse=True),
        drehbuch=[
            MeldungBeiPunkt(vorgang=0, nach_punkten=1, stil=16, text="eins"),
            MeldungBeiPunkt(vorgang=0, nach_punkten=3, stil=48, text="drei"),
        ],
    )
    sim.verbinde()
    sim.setze_messfreigabe(True)
    sim.lade_einstellungen(_set(tmp_path))
    sim.starte_scan(str(tmp_path / "m.svd"))
    uhr.vorstellen(1.5)
    f = sim.fortschritt()
    assert f is not None and (f.punkte_erledigt, f.punkte_gesamt) == (1, 9)
    assert [m.text for m in sim.hole_meldungen()] == ["eins"]
    assert sim.hole_meldungen() == ()
    uhr.vorstellen(5.0)
    assert [m.text for m in sim.hole_meldungen()] == ["drei"]


def test_haengender_aufruf_fuer_waechter(tmp_path: Path) -> None:
    uhr = Testuhr()
    sim = Simulator(
        uhr.monotonic, drehbuch=[HaengenderAufruf(vorgang=0, methode="lade_einstellungen")]
    )
    sim.verbinde()
    assert sim.haengender_aufruf_seit_s() is None
    fertig = threading.Event()

    def laden() -> None:
        sim.lade_einstellungen(_set(tmp_path))
        fertig.set()

    thread = threading.Thread(target=laden)
    thread.start()
    for _ in range(500):
        if sim.haengender_aufruf_seit_s() is not None:
            break
        threading.Event().wait(0.01)
    uhr.vorstellen(7.0)
    dauer = sim.haengender_aufruf_seit_s()
    assert dauer is not None and dauer == pytest.approx(7.0, rel=1e-12)
    assert not fertig.is_set()
    sim.haenger_loesen()
    thread.join(5.0)
    assert fertig.is_set()
    assert sim.haengender_aufruf_seit_s() is None


def test_haengender_aufruf_mit_zeitlimit(tmp_path: Path) -> None:
    sim = Simulator(
        Testuhr().monotonic,
        drehbuch=[HaengenderAufruf(vorgang=0, methode="lade_einstellungen", max_echtzeit_s=0.01)],
    )
    sim.verbinde()
    with pytest.raises(ZeitlimitFehler):
        sim.lade_einstellungen(_set(tmp_path))


def test_aufrufprotokoll_und_trennen(tmp_path: Path) -> None:
    sim = _sim(Testuhr())
    sim.trenne()
    sim.trenne()
    assert sim.aufgerufene_methoden() == ("verbinde", "zustand", "trenne", "trenne")
    assert sim.aufrufe[0] == ("verbinde", ())
    with pytest.raises(GeraeteFehler):
        sim.lies_einstellungsstand()


def test_langsamer_aufruf_braucht_schlafen_und_vorgang_minus_eins() -> None:
    from ldv_automation.geraet.simulator import LangsamerAufruf

    with pytest.raises(ValueError, match="schlafen"):
        Simulator(
            Testuhr().monotonic,
            drehbuch=[LangsamerAufruf(vorgang=0, methode="verbinde", dauer_s=1.0)],
        )
    uhr = Testuhr()
    sim = Simulator(
        uhr.monotonic,
        drehbuch=[LangsamerAufruf(vorgang=-1, methode="verbinde", dauer_s=7.0)],
        schlafen=uhr.sleep,
    )
    sim.verbinde()
    assert uhr.monotonic() == 7.0  # exakt: eine Vorstellung um 7,0 s
    with pytest.raises(ValueError, match="≥ 0"):
        Simulator(Testuhr().monotonic, drehbuch=[Haenger(vorgang=-1)])
