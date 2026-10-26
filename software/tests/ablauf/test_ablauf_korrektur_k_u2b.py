"""Korrekturpaket K-U2b: Aufrufgrenze, Hänger außerhalb der Messung, Trennen nach Fehler."""

from __future__ import annotations

from pathlib import Path

import pytest
from ablauf_hilfen import SCHREIBAUFRUFE, Aufbau, aufbau, messung

from ldv_automation.ablauf.fehlerstrategie import FehlerEreignis, FehlerReaktion
from ldv_automation.ablauf.steuerung import (
    AblaufKonfiguration,
    DurchgangErgebnis,
    DurchgangZustand,
)
from ldv_automation.ablauf.uhr import Testuhr
from ldv_automation.domaene.eintraege import Messung
from ldv_automation.geraet.schnittstelle import GeraeteInfo, Messgeraet
from ldv_automation.geraet.simulator import (
    HaengenderAufruf,
    LadeFehler,
    LangsamerAufruf,
    Simulator,
)
from ldv_automation.protokoll.version import BuildInfo
from ldv_automation.sitzung import Betriebsart, Sitzung

GIT = BuildInfo(paket_version="0.1.0", git_hash="f" * 40, git_dirty=False, quelle="test")


class Spion:
    def __init__(self) -> None:
        self.befragt = 0

    @property
    def bezeichnung(self) -> str:
        return "Spion"

    def entscheide(self, ereignis: FehlerEreignis) -> FehlerReaktion:
        self.befragt += 1
        return FehlerReaktion.ANHALTEN_UND_FRAGEN


def _fehler(a: Aufbau, basis: str = "01_M1") -> dict[str, object]:
    fehler = a.protokoll(basis)["fehler"]
    assert isinstance(fehler, dict)
    return fehler


def _durchgang_beendet(a: Aufbau) -> list[str]:
    return [str(e.daten["ergebnis"]) for e in a.ereignisse if e.art == "durchgang_beendet"]


# --- Punkt 1: Aufrufgrenze aus der Aufrufdauer --------------------------------------


def test_aufrufgrenze_standard_und_pruefung() -> None:
    assert AblaufKonfiguration().aufruf_grenze_s == 60.0
    with pytest.raises(ValueError, match="aufruf_grenze_s"):
        AblaufKonfiguration(aufruf_grenze_s=0.0)


@pytest.mark.parametrize(
    ("methode", "phase"),
    [
        ("lade_einstellungen", "vorbereitung"),
        ("setze_parameter", "vorbereitung"),
        ("lies_einstellungsstand", "vorbereitung"),
        ("zustand", "scan"),
        ("hole_meldungen", "scan"),
        ("fortschritt", "scan"),
    ],
)
def test_langer_aber_normaler_aufruf_fuehrt_zu_geraet_unklar(
    tmp_path: Path, methode: str, phase: str
) -> None:
    spion = Spion()
    a = aufbau(
        tmp_path,
        [messung(tmp_path, "M1", {"mittelung.anzahl": 4}), messung(tmp_path, "M2")],
        drehbuch=[LangsamerAufruf(vorgang=0, methode=methode, dauer_s=61.0)],
        strategie=spion,
    )
    a.starte()
    a.steuerung.bis_ruhe()

    assert a.durchgang_wechsel() == ["laeuft", "geraet_unklar"]
    assert spion.befragt == 0
    assert [e.zustand.value for e in a.ws.eintraege()] == ["fehler", "wartend"]
    fehler = _fehler(a)
    assert fehler["art"] == "geraet_unklar"
    assert fehler["methode"] == methode
    assert "dauerte 61.0 s (Grenze 60 s)" in str(fehler["text"])
    methoden = a.sim.aufgerufene_methoden()
    assert methoden[-1] == methode  # danach kein Geräteaufruf mehr
    assert ("starte_scan" in methoden) is (phase == "scan")
    assert "stoppe" not in methoden
    stand = a.steuerung.momentaufnahme()
    assert stand.geraet_verloren
    anzahl = len(a.sim.aufrufe)
    a.uhr.vorstellen(1000.0)
    for _ in range(10):
        a.steuerung.schritt()
    assert len(a.sim.aufrufe) == anzahl


def test_aufruf_knapp_unter_grenze_ist_normal(tmp_path: Path) -> None:
    a = aufbau(
        tmp_path,
        [messung(tmp_path, "M1")],
        drehbuch=[LangsamerAufruf(vorgang=0, methode="lade_einstellungen", dauer_s=59.0)],
    )
    a.starte()
    a.steuerung.bis_ruhe()
    assert a.steuerung.momentaufnahme().ergebnis is DurchgangErgebnis.VOLLSTAENDIG


def test_aufrufgrenze_ist_konfigurierbar(tmp_path: Path) -> None:
    a = aufbau(
        tmp_path,
        [messung(tmp_path, "M1")],
        drehbuch=[LangsamerAufruf(vorgang=0, methode="lade_einstellungen", dauer_s=11.0)],
        konfiguration=AblaufKonfiguration(aufruf_grenze_s=10.0),
    )
    a.starte()
    a.steuerung.bis_ruhe()
    assert a.steuerung.zustand is DurchgangZustand.GERAET_UNKLAR


def test_langer_aufruf_mit_geraetefehler_gilt_ebenfalls_als_haenger(tmp_path: Path) -> None:
    a = aufbau(
        tmp_path,
        [messung(tmp_path, "M1")],
        drehbuch=[
            LangsamerAufruf(vorgang=0, methode="lade_einstellungen", dauer_s=61.0),
            LadeFehler(vorgang=0),
        ],
    )
    a.starte()
    a.steuerung.bis_ruhe()
    assert a.steuerung.zustand is DurchgangZustand.GERAET_UNKLAR
    assert "scheiterte" in str(_fehler(a)["text"])


def test_starte_scan_misst_gegen_zeitlimit_nicht_gegen_aufrufgrenze(tmp_path: Path) -> None:
    """ScanEx darf bis zum Scanende blockieren: 100 s > 60 s Aufrufgrenze, < 600 s Zeitlimit."""
    a = aufbau(
        tmp_path,
        [messung(tmp_path, "M1")],
        drehbuch=[LangsamerAufruf(vorgang=0, methode="starte_scan", dauer_s=100.0)],
    )
    a.starte()
    a.steuerung.bis_ruhe()
    assert a.steuerung.momentaufnahme().ergebnis is DurchgangErgebnis.VOLLSTAENDIG
    assert a.protokoll("01_M1")["status"] == "fertig"


def test_starte_scan_ueber_zeitlimit_fuehrt_zu_geraet_unklar(tmp_path: Path) -> None:
    a = aufbau(
        tmp_path,
        [messung(tmp_path, "M1", zeitlimit_s=50.0)],
        drehbuch=[LangsamerAufruf(vorgang=0, methode="starte_scan", dauer_s=100.0)],
    )
    a.starte()
    a.steuerung.bis_ruhe()
    assert a.steuerung.zustand is DurchgangZustand.GERAET_UNKLAR
    fehler = _fehler(a)
    assert fehler["methode"] == "starte_scan"
    assert "Grenze 50 s" in str(fehler["text"])
    assert "stoppe" not in a.sim.aufgerufene_methoden()


def test_langer_stop_fuehrt_zu_geraet_unklar(tmp_path: Path) -> None:
    from ldv_automation.geraet.simulator import Haenger

    a = aufbau(
        tmp_path,
        [messung(tmp_path, "M1", zeitlimit_s=5.0)],
        drehbuch=[Haenger(vorgang=0), LangsamerAufruf(vorgang=0, methode="stoppe", dauer_s=61.0)],
    )
    a.starte()
    a.steuerung.bis_ruhe()
    assert a.steuerung.zustand is DurchgangZustand.GERAET_UNKLAR
    assert _fehler(a)["methode"] == "stoppe"
    methoden = a.sim.aufgerufene_methoden()
    assert methoden.count("stoppe") == 1 and methoden[-1] == "stoppe"


# --- Punkt 2: Hänger außerhalb der Messung ------------------------------------------


@pytest.mark.parametrize(
    "ereignis",
    [
        HaengenderAufruf(vorgang=-1, methode="verbinde", max_echtzeit_s=0.01),
        LangsamerAufruf(vorgang=-1, methode="verbinde", dauer_s=61.0),
    ],
)
def test_haenger_beim_verbinden(
    tmp_path: Path, ereignis: HaengenderAufruf | LangsamerAufruf
) -> None:
    a = aufbau(tmp_path, [messung(tmp_path, "M1")], drehbuch=[ereignis], verbinden=False)
    a.steuerung.verbinde()
    a.steuerung.schritt()
    stand = a.steuerung.momentaufnahme()
    assert stand.verbindung is None and stand.geraet_verloren
    assert stand.durchgang is DurchgangZustand.BEREIT
    anzahl = len(a.sim.aufrufe)
    a.steuerung.trenne()
    a.steuerung.verbinde()
    a.steuerung.schritt()
    assert len(a.sim.aufrufe) == anzahl  # kein erneuter Aufruf am hängenden Gerät
    assert any("verloren" in e.text for e in a.ereignisse if e.art == "befehl_verworfen")


def test_haenger_beim_setzen_der_messfreigabe(tmp_path: Path) -> None:
    a = aufbau(
        tmp_path,
        [messung(tmp_path, "M1")],
        drehbuch=[HaengenderAufruf(vorgang=-1, methode="setze_messfreigabe", max_echtzeit_s=0.01)],
    )
    a.starte()
    a.steuerung.bis_ruhe()
    assert a.steuerung.zustand is DurchgangZustand.GERAET_UNKLAR
    assert [e.zustand.value for e in a.ws.eintraege()] == ["wartend"]
    methoden = a.sim.aufgerufene_methoden()
    assert methoden[-1] == "setze_messfreigabe"
    anzahl = len(a.sim.aufrufe)
    a.steuerung.trenne()
    a.steuerung.schritt()
    stand = a.steuerung.momentaufnahme()
    assert stand.durchgang is DurchgangZustand.BEENDET
    assert stand.ergebnis is DurchgangErgebnis.GERAET_UNKLAR
    assert len(a.sim.aufrufe) == anzahl
    ende = [z for z in a.ereignisprotokoll() if z["art"] == "durchgang_beendet"]
    assert [z["ergebnis"] for z in ende] == ["geraet_unklar", "geraet_unklar"]


def test_haenger_beim_entziehen_der_messfreigabe(tmp_path: Path) -> None:
    a = aufbau(
        tmp_path,
        [messung(tmp_path, "M1")],
        drehbuch=[LangsamerAufruf(vorgang=0, methode="setze_messfreigabe", dauer_s=61.0)],
    )
    a.starte()
    a.steuerung.bis_ruhe()
    assert a.steuerung.zustand is DurchgangZustand.GERAET_UNKLAR
    assert a.protokoll("01_M1")["status"] == "fertig"  # Messung selbst war fertig
    anzahl = len(a.sim.aufrufe)
    a.steuerung.trenne()
    a.steuerung.schritt()
    assert a.steuerung.momentaufnahme().ergebnis is DurchgangErgebnis.GERAET_UNKLAR
    assert len(a.sim.aufrufe) == anzahl


def test_haenger_beim_trennen_in_bereit(tmp_path: Path) -> None:
    a = aufbau(
        tmp_path,
        [],
        drehbuch=[HaengenderAufruf(vorgang=-1, methode="trenne", max_echtzeit_s=0.01)],
    )
    a.steuerung.trenne()
    a.steuerung.schritt()
    stand = a.steuerung.momentaufnahme()
    assert stand.verbindung is None and stand.geraet_verloren
    anzahl = len(a.sim.aufrufe)
    a.steuerung.verbinde()
    a.steuerung.trenne()
    a.steuerung.schritt()
    assert len(a.sim.aufrufe) == anzahl


def test_haenger_beim_trennen_des_alten_geraets_im_tausch(tmp_path: Path) -> None:
    a = aufbau(
        tmp_path,
        [],
        drehbuch=[LangsamerAufruf(vorgang=-1, methode="trenne", dauer_s=61.0)],
    )
    neu = Simulator(a.uhr.monotonic)
    a.steuerung.tausche_geraet(lambda: neu, "simulator")
    a.steuerung.schritt()
    assert a.steuerung.geraet is neu
    assert any("hängt" in e.text for e in a.ereignisse if e.art == "fehler")
    a.steuerung.verbinde()
    a.steuerung.schritt()
    assert a.steuerung.momentaufnahme().verbindung is not None
    assert not a.steuerung.momentaufnahme().geraet_verloren


def test_sitzung_baut_geraet_nach_haenger_beim_verbinden_neu(tmp_path: Path) -> None:
    uhr = Testuhr()
    erzeugt: list[Simulator] = []

    def fabrik(art: Betriebsart) -> Messgeraet:
        drehbuch = (
            [LangsamerAufruf(vorgang=-1, methode="verbinde", dauer_s=61.0)] if not erzeugt else []
        )
        sim = Simulator(uhr.monotonic, betriebsart=art.value, drehbuch=drehbuch, schlafen=uhr.sleep)
        erzeugt.append(sim)
        return sim

    s = Sitzung(geraete_fabrik=fabrik, uhr=uhr, build_info=GIT)
    s.verarbeite()
    s.verbinde()
    s.verarbeite()
    assert not s.zustandsbild().verbunden
    s.verbinde()
    s.verarbeite()
    assert len(erzeugt) == 2
    verbindung = s.zustandsbild().verbindung
    assert isinstance(verbindung, GeraeteInfo)
    # Nur der eine (langsame, intern mit zustand) Verbindungsaufruf, danach nichts mehr
    assert erzeugt[0].aufgerufene_methoden() == ("verbinde", "zustand")


# --- Punkt 3: Trennen nach internem Fehler ohne Durchgang ---------------------------


def test_trennen_nach_internem_fehler_in_bereit_ohne_durchgang_beendet(tmp_path: Path) -> None:
    a = aufbau(tmp_path, [messung(tmp_path, "M1")], verbinden=False)

    def kaputt() -> GeraeteInfo:
        raise RuntimeError("Programmierfehler")

    a.sim.verbinde = kaputt  # type: ignore[method-assign]
    a.steuerung.verbinde()
    a.steuerung.schritt()
    assert a.steuerung.zustand is DurchgangZustand.GERAET_UNKLAR
    a.steuerung.trenne()
    a.steuerung.schritt()
    stand = a.steuerung.momentaufnahme()
    assert stand.durchgang is DurchgangZustand.BEREIT
    assert stand.ergebnis is None and stand.fehler_offen is None
    assert _durchgang_beendet(a) == []
    assert not SCHREIBAUFRUFE & set(a.sim.aufgerufene_methoden())


def test_tausch_nach_internem_fehler_in_bereit_ohne_durchgang_beendet(tmp_path: Path) -> None:
    a = aufbau(tmp_path, [Messung(name="M1", einstellungsdatei="x.set")], verbinden=False)

    def kaputt() -> GeraeteInfo:
        raise RuntimeError("Programmierfehler")

    a.sim.verbinde = kaputt  # type: ignore[method-assign]
    a.steuerung.verbinde()
    a.steuerung.schritt()
    a.steuerung.tausche_geraet(lambda: Simulator(a.uhr.monotonic), "simulator")
    a.steuerung.schritt()
    assert a.steuerung.zustand is DurchgangZustand.BEREIT
    assert _durchgang_beendet(a) == []


def test_interner_fehler_mit_langem_freigabe_entzug_spricht_geraet_nicht_mehr_an(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """K-U2c: Messfreigabe entziehen im internen Fehlerpfad läuft über die Aufrufgrenze."""
    a = aufbau(
        tmp_path,
        [messung(tmp_path, "M1")],
        drehbuch=[LangsamerAufruf(vorgang=-1, methode="setze_messfreigabe", dauer_s=61.0)],
        konfiguration=AblaufKonfiguration(aufruf_grenze_s=100.0),
    )
    a.starte()
    a.steuerung.schritt()  # Start: setze_messfreigabe(True) dauert 61 s < 100 s Grenze
    assert a.steuerung.zustand is DurchgangZustand.LAEUFT
    # Grenze für den Fehlerpfad herabsetzen, damit der Entzug (ebenfalls 61 s) sie überschreitet
    monkeypatch.setattr(a.steuerung, "_konf", AblaufKonfiguration(aufruf_grenze_s=60.0))

    def kaputt(*_: object) -> None:
        raise RuntimeError("Programmierfehler")

    monkeypatch.setattr(a.steuerung, "_vorpruefung", kaputt)
    a.steuerung.schritt()

    stand = a.steuerung.momentaufnahme()
    assert stand.durchgang is DurchgangZustand.GERAET_UNKLAR
    assert stand.geraet_verloren
    folge = next(e for e in a.ereignisse if e.art == "interner_fehler").daten["folgefehler"]
    assert isinstance(folge, list) and any("hängt" in str(f) for f in folge)
    assert a.sim.aufgerufene_methoden()[-1] == "setze_messfreigabe"
    anzahl = len(a.sim.aufrufe)
    a.steuerung.trenne()
    a.steuerung.schritt()
    assert len(a.sim.aufrufe) == anzahl  # Trennen spricht das Gerät nicht mehr an
    assert a.steuerung.momentaufnahme().ergebnis is DurchgangErgebnis.GERAET_UNKLAR
