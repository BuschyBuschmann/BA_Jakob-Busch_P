"""Korrekturpaket K-U2: hängender Geräteaufruf (MAJOR-1) und interner Fehler (MAJOR-2)."""

from __future__ import annotations

import json
import time
from pathlib import Path

import pytest
from ablauf_hilfen import SCHREIBAUFRUFE, Aufbau, aufbau, messung

from ldv_automation.ablauf.fehlerstrategie import FehlerEreignis, FehlerReaktion
from ldv_automation.ablauf.steuerung import (
    AblaufKonfiguration,
    DurchgangErgebnis,
    DurchgangZustand,
    Fehlerentscheidung,
)
from ldv_automation.ablauf.uhr import Echtzeituhr
from ldv_automation.domaene.eintraege import Messung, MessungZustand
from ldv_automation.geraet.schnittstelle import Messgeraet
from ldv_automation.geraet.simulator import HaengenderAufruf, Simulator, SimulatorKonfiguration
from ldv_automation.protokoll.version import BuildInfo
from ldv_automation.sitzung import Betriebsart, Sitzung

GIT = BuildInfo(paket_version="0.1.0", git_hash="d" * 40, git_dirty=False, quelle="test")


class SpionStrategie:
    """Zeichnet auf, ob die Fehlerstrategie befragt wird."""

    def __init__(self) -> None:
        self.befragt: list[FehlerEreignis] = []

    @property
    def bezeichnung(self) -> str:
        return "Spion"

    def entscheide(self, ereignis: FehlerEreignis) -> FehlerReaktion:
        self.befragt.append(ereignis)
        return FehlerReaktion.ANHALTEN_UND_FRAGEN


def _fehler(a: Aufbau, basis: str) -> dict[str, object]:
    fehler = a.protokoll(basis)["fehler"]
    assert isinstance(fehler, dict)
    return fehler


# --- MAJOR-1: hängender Geräteaufruf -------------------------------------------------


@pytest.mark.parametrize(
    ("methode", "phase"),
    [
        ("lade_einstellungen", "vorbereitung"),
        ("hole_meldungen", "scan"),
    ],
)
def test_haenger_fuehrt_zu_geraet_unklar_ohne_strategie_und_stop(
    tmp_path: Path, methode: str, phase: str
) -> None:
    spion = SpionStrategie()
    a = aufbau(
        tmp_path,
        [messung(tmp_path, "M1"), messung(tmp_path, "M2")],
        drehbuch=[HaengenderAufruf(vorgang=0, methode=methode, max_echtzeit_s=0.01)],
        strategie=spion,
    )
    a.starte()
    a.steuerung.bis_ruhe()

    assert a.durchgang_wechsel() == ["laeuft", "geraet_unklar"]
    assert spion.befragt == []
    assert [e.zustand.value for e in a.ws.eintraege()] == ["fehler", "wartend"]
    fehler = _fehler(a, "01_M1")
    assert fehler["art"] == "geraet_unklar"
    assert fehler["methode"] == methode
    methoden = a.sim.aufgerufene_methoden()
    assert methoden[-1] == methode  # danach kein einziger Geräteaufruf mehr
    assert "stoppe" not in methoden
    if phase == "scan":
        assert "starte_scan" in methoden
    else:
        assert "starte_scan" not in methoden

    # Kein Wiederholen, keine weiteren Geräteaufrufe, auch nach langer Zeit
    anzahl = len(a.sim.aufrufe)
    a.steuerung.entscheide(Fehlerentscheidung.WIEDERHOLEN)
    a.uhr.vorstellen(10_000.0)
    for _ in range(20):
        a.steuerung.schritt()
    assert len(a.sim.aufrufe) == anzahl
    assert a.steuerung.zustand is DurchgangZustand.GERAET_UNKLAR
    assert any(e.art == "befehl_verworfen" for e in a.ereignisse)

    # Trennen spricht das hängende Gerät nicht an; Verbinden bleibt gesperrt
    a.steuerung.trenne()
    a.steuerung.schritt()
    stand = a.steuerung.momentaufnahme()
    assert stand.durchgang is DurchgangZustand.BEENDET
    assert stand.ergebnis is DurchgangErgebnis.GERAET_UNKLAR
    a.steuerung.verbinde()
    a.steuerung.schritt()
    assert len(a.sim.aufrufe) == anzahl
    assert "verloren" in [e.text for e in a.ereignisse if e.art == "befehl_verworfen"][-1]

    # Erst ein neues Gerät (Gerätetausch) gibt Verbinden wieder frei
    neu = Simulator(a.uhr.monotonic)
    a.steuerung.tausche_geraet(lambda: neu, "simulator")
    a.steuerung.schritt()
    a.steuerung.verbinde()
    a.steuerung.schritt()
    assert a.steuerung.momentaufnahme().verbindung is not None
    assert len(a.sim.aufrufe) == anzahl


def test_haenger_beim_stop_fuehrt_zu_geraet_unklar(tmp_path: Path) -> None:
    from ldv_automation.geraet.simulator import Haenger

    a = aufbau(
        tmp_path,
        [messung(tmp_path, "M1", zeitlimit_s=2.0)],
        drehbuch=[
            Haenger(vorgang=0),
            HaengenderAufruf(vorgang=0, methode="stoppe", max_echtzeit_s=0.01),
        ],
    )
    a.starte()
    a.steuerung.bis_ruhe()
    assert a.steuerung.zustand is DurchgangZustand.GERAET_UNKLAR
    assert _fehler(a, "01_M1")["methode"] == "stoppe"
    methoden = a.sim.aufgerufene_methoden()
    assert methoden[-1] == "stoppe"
    assert not SCHREIBAUFRUFE & set(methoden[methoden.index("stoppe") + 1 :])


def test_anzeige_waehrend_blockiertem_aufruf(tmp_path: Path) -> None:
    """Solange der Aufruf blockiert, bleibt der Durchgang im bisherigen Zustand; der Wächter
    zeigt die Dauer. Löst sich der Aufruf ohne Zeitlimitfehler, läuft die Messung weiter."""
    uhr = Echtzeituhr()
    erzeugt: list[Simulator] = []

    def fabrik(art: Betriebsart) -> Messgeraet:
        sim = Simulator(
            uhr.monotonic,
            betriebsart=art.value,
            konfiguration=SimulatorKonfiguration(punkte_anzahl=2, punktdauer_s=0.01),
            drehbuch=[HaengenderAufruf(vorgang=0, methode="lade_einstellungen")],
        )
        erzeugt.append(sim)
        return sim

    wurzel = tmp_path / "daten"
    wurzel.mkdir()
    s = Sitzung(
        geraete_fabrik=fabrik,
        uhr=uhr,
        build_info=GIT,
        messdaten_wurzel=wurzel,
        konfiguration=AblaufKonfiguration(poll_s=0.005),
        aufruf_warnung_s=0.05,
    )
    s.starte_threads(waechter_takt_s=0.01)
    try:
        frist = time.monotonic() + 10.0
        while not s.steuerung.hat_geraet and time.monotonic() < frist:
            time.sleep(0.005)
        s.verbinde()
        while not s.zustandsbild().verbunden and time.monotonic() < frist:
            time.sleep(0.005)
        s.einfuegen(0, Messung(name="M1", einstellungsdatei=str(_set(tmp_path))))
        s.starte("haenger")
        while s.zustandsbild().waechter_s is None and time.monotonic() < frist:
            time.sleep(0.005)
        bild = s.zustandsbild()
        assert bild.waechter_s is not None and bild.waechter_s >= 0.05
        assert bild.durchgang is DurchgangZustand.LAEUFT
        assert bild.eintraege[0].zustand == "laeuft"
        while not any(e.art == "waechter" for e in s.hole_ereignisse()):
            assert time.monotonic() < frist
            time.sleep(0.005)
        erzeugt[0].haenger_loesen()
        while s.zustandsbild().durchgang is not DurchgangZustand.BEENDET:
            assert time.monotonic() < frist
            time.sleep(0.005)
        assert s.zustandsbild().eintraege[0].zustand == "fertig"
    finally:
        erzeugt[0].haenger_loesen()
        assert s.beende_threads(timeout_s=5.0)


def _set(tmp_path: Path) -> Path:
    pfad = tmp_path / "basis.set"
    pfad.write_bytes(b"SET")
    return pfad


# --- MAJOR-2a: nicht darstellbarer Name ----------------------------------------------


@pytest.mark.parametrize("name", ["测量", "???", "…"])
def test_nicht_darstellbarer_name_ist_vorpruefungsfehler(tmp_path: Path, name: str) -> None:
    m1 = Messung(name=name, einstellungsdatei=str(_set(tmp_path)))
    a = aufbau(tmp_path, [m1, messung(tmp_path, "M2")])
    a.starte()
    a.steuerung.schritt()  # Start
    anzahl = len(a.sim.aufrufe)
    a.steuerung.bis_ruhe()

    assert a.steuerung.zustand is DurchgangZustand.WARTET_AUF_ENTSCHEIDUNG
    assert a.sim.aufrufe[anzahl:] == ()
    assert a.ws.hole(m1.id).zustand is MessungZustand.FEHLER
    basis = f"01_messung_{m1.id.hex[:8]}"
    p = a.protokoll(basis)
    assert p["name"] == name
    assert p["status"] == "fehler"
    fehler = p["fehler"]
    assert isinstance(fehler, dict)
    assert fehler["art"] == "vorpruefung"
    assert "Dateiname" in str(fehler["text"])
    assert not list(a.ordner().glob("*.svd"))
    assert a.steuerung.momentaufnahme().interner_fehler is None

    a.steuerung.entscheide(Fehlerentscheidung.UEBERSPRINGEN)
    a.steuerung.bis_ruhe()
    assert a.steuerung.momentaufnahme().ergebnis is DurchgangErgebnis.VOLLSTAENDIG
    assert (a.ordner() / "02_M2.svd").is_file()


# --- MAJOR-2b: interner Fehler ist keine Sackgasse -----------------------------------


def test_interner_fehler_synchron_bleibt_bedienbar(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    a = aufbau(tmp_path, [messung(tmp_path, "M1"), messung(tmp_path, "M2")])

    def kaputt(*_: object) -> None:
        raise RuntimeError("Programmierfehler")

    monkeypatch.setattr(a.steuerung, "_vorpruefung", kaputt)
    a.starte()
    a.steuerung.bis_ruhe()

    stand = a.steuerung.momentaufnahme()
    assert stand.durchgang is DurchgangZustand.GERAET_UNKLAR
    assert stand.interner_fehler is not None and "Programmierfehler" in stand.interner_fehler
    assert [e.zustand.value for e in a.ws.eintraege()] == ["fehler", "wartend"]
    assert _fehler(a, "01_M1")["art"] == "geraet_unklar"
    freigaben = [args for name, args in a.sim.aufrufe if name == "setze_messfreigabe"]
    assert freigaben == [(True,), (False,)]
    zeilen = (a.ordner() / "durchgang.ereignisse.jsonl").read_text("utf-8").splitlines()
    assert any(json.loads(z)["art"] == "interner_fehler" for z in zeilen)

    # Trennen, Quittieren und Gerätetausch werden weiter verarbeitet
    a.steuerung.trenne()
    a.steuerung.schritt()
    assert a.steuerung.zustand is DurchgangZustand.BEENDET
    a.steuerung.quittiere()
    a.steuerung.schritt()
    assert a.steuerung.momentaufnahme().durchgang is DurchgangZustand.BEREIT
    neu = Simulator(a.uhr.monotonic)
    a.steuerung.tausche_geraet(lambda: neu, "simulator")
    a.steuerung.schritt()
    assert a.steuerung.geraet is neu


def test_interner_fehler_mit_thread_und_sitzung(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    uhr = Echtzeituhr()
    erzeugt: list[Simulator] = []

    def fabrik(art: Betriebsart) -> Messgeraet:
        sim = Simulator(
            uhr.monotonic,
            betriebsart=art.value,
            konfiguration=SimulatorKonfiguration(punkte_anzahl=2, punktdauer_s=0.01),
        )
        erzeugt.append(sim)
        return sim

    wurzel = tmp_path / "daten"
    wurzel.mkdir()
    s = Sitzung(
        geraete_fabrik=fabrik,
        uhr=uhr,
        build_info=GIT,
        messdaten_wurzel=wurzel,
        konfiguration=AblaufKonfiguration(poll_s=0.005),
    )

    def kaputt(*_: object) -> None:
        raise RuntimeError("Programmierfehler im Thread")

    monkeypatch.setattr(s.steuerung, "_vorpruefung", kaputt)
    s.starte_threads(waechter_takt_s=0.01)
    frist = time.monotonic() + 10.0

    def warte(bedingung: object) -> None:
        assert callable(bedingung)
        while not bedingung():
            assert time.monotonic() < frist, "Zeitüberschreitung"
            time.sleep(0.005)

    try:
        warte(lambda: s.steuerung.hat_geraet)
        s.verbinde()
        warte(lambda: s.zustandsbild().verbunden)
        s.einfuegen(0, Messung(name="M1", einstellungsdatei=str(_set(tmp_path))))
        s.starte("intern")
        warte(lambda: s.zustandsbild().durchgang is DurchgangZustand.GERAET_UNKLAR)
        bild = s.zustandsbild()
        assert bild.interner_fehler is not None
        assert bild.eintraege[0].zustand == "fehler"

        # Geräte-Thread lebt und verarbeitet Befehle
        s.trenne()
        warte(lambda: s.zustandsbild().durchgang is DurchgangZustand.BEENDET)
        s.quittiere()
        warte(lambda: s.zustandsbild().durchgang is DurchgangZustand.BEREIT)
        s.setze_betriebsart(Betriebsart.TROCKENLAUF)
        warte(lambda: s.zustandsbild().betriebsart is Betriebsart.TROCKENLAUF)
        assert len(erzeugt) == 2
    finally:
        assert s.beende_threads(timeout_s=5.0)


def test_folgefehler_im_internen_fehler_werden_gemeldet(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    a = aufbau(tmp_path, [messung(tmp_path, "M1")])

    def kaputt(*_: object, **__: object) -> None:
        raise RuntimeError("defekt")

    monkeypatch.setattr(a.steuerung, "_vorpruefung", kaputt)
    monkeypatch.setattr(a.steuerung, "_protokolliere", kaputt)
    monkeypatch.setattr(a.sim, "setze_messfreigabe", kaputt)
    a.steuerung.starte(  # Freigabe nicht über das Gerät, damit der Start gelingt
        __import__(
            "ldv_automation.ablauf.steuerung", fromlist=["DurchgangsAuftrag"]
        ).DurchgangsAuftrag(
            name="x",
            messdaten_wurzel=a.wurzel,
            betriebsart="simulator",
            trockenlauf=False,
            messfreigabe=False,
        )
    )
    a.steuerung.schritt()
    a.steuerung._freigabe_gesetzt = True  # Freigabe als gesetzt annehmen
    a.steuerung.schritt()
    ereignis = next(e for e in a.ereignisse if e.art == "interner_fehler")
    folge = ereignis.daten["folgefehler"]
    assert isinstance(folge, list)
    assert any("Messprotokoll" in str(f) for f in folge)
    assert any("Messfreigabe" in str(f) for f in folge)
    assert a.steuerung.zustand is DurchgangZustand.GERAET_UNKLAR
