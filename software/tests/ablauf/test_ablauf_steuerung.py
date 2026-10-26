"""Weitere Pfade der Ablaufsteuerung (Fehlerarten, Befehle, Fortschritt, Thread)."""

from __future__ import annotations

import math
import time
from pathlib import Path

import pytest
from ablauf_hilfen import BUILD, Aufbau, aufbau, messung

from ldv_automation.ablauf.steuerung import (
    AblaufKonfiguration,
    DurchgangErgebnis,
    DurchgangsAuftrag,
    DurchgangZustand,
    Fehlerentscheidung,
    Steuerung,
)
from ldv_automation.ablauf.uhr import Echtzeituhr
from ldv_automation.domaene.eintraege import Messung, MessungZustand, Pausenpunkt
from ldv_automation.domaene.warteschlange import Warteschlange
from ldv_automation.geraet.simulator import (
    KeineDatei,
    LadeFehler,
    MeldungBeiPunkt,
    Simulator,
    SimulatorKonfiguration,
    StartFehler,
    TeilLaden,
    VorzeitigesEnde,
)


def _fehlerart(a: Aufbau, basis: str = "01_M1") -> str:
    fehler = a.protokoll(basis)["fehler"]
    assert isinstance(fehler, dict)
    return str(fehler["art"])


def test_trockenlauf_ohne_scan_status_trockenlauf(tmp_path: Path) -> None:
    a = aufbau(
        tmp_path,
        [messung(tmp_path, "M1", {"fft.linien": 1600}), messung(tmp_path, "M2")],
        betriebsart="trockenlauf",
    )
    a.starte(trockenlauf=True, freigabe=False)
    a.steuerung.bis_ruhe()
    stand = a.steuerung.momentaufnahme()
    assert stand.ergebnis is DurchgangErgebnis.VOLLSTAENDIG
    assert stand.trockenlauf_ok
    assert "starte_scan" not in a.sim.aufgerufene_methoden()
    assert "setze_messfreigabe" not in a.sim.aufgerufene_methoden()
    p = a.protokoll("01_M1")
    assert p["status"] == "trockenlauf"
    assert p["betriebsart"] == "trockenlauf"
    assert stand.laufinfo[a.ws.eintraege()[0].id].trockenlauf


def test_trockenlauf_mit_abweichung_ist_nicht_ok(tmp_path: Path) -> None:
    """Maßgeblich ist der erste Eintrag; eine spätere fehlerfreie Messung schaltet nicht frei."""
    konf = SimulatorKonfiguration(bandbreiten_hz=(3125.0, 6250.0))
    a = aufbau(
        tmp_path,
        [messung(tmp_path, "M1", {"fft.bandbreite_hz": 5000.0}), messung(tmp_path, "M2")],
        sim_konfiguration=konf,
        betriebsart="trockenlauf",
    )
    a.starte(trockenlauf=True, freigabe=False)
    a.steuerung.bis_ruhe()
    a.steuerung.entscheide(Fehlerentscheidung.UEBERSPRINGEN)
    a.steuerung.bis_ruhe()
    assert [e.zustand.value for e in a.ws.eintraege()] == ["fehler", "fertig"]
    assert not a.steuerung.momentaufnahme().trockenlauf_ok


def test_fremde_messung_geraet_nicht_bereit(tmp_path: Path) -> None:
    a = aufbau(
        tmp_path,
        [messung(tmp_path, "M1")],
        sim_konfiguration=SimulatorKonfiguration(fremde_messung=True),
    )
    a.starte()
    a.steuerung.bis_ruhe()
    assert _fehlerart(a) == "geraet_nicht_bereit"
    assert "lade_einstellungen" not in a.sim.aufgerufene_methoden()
    assert "stoppe" not in a.sim.aufgerufene_methoden()


def test_ladefehler_und_teil_laden(tmp_path: Path) -> None:
    a = aufbau(
        tmp_path,
        [messung(tmp_path, "M1"), messung(tmp_path, "M2")],
        drehbuch=[LadeFehler(vorgang=0), TeilLaden(vorgang=1)],
    )
    a.starte()
    a.steuerung.bis_ruhe()
    assert _fehlerart(a) == "geraet"
    a.steuerung.entscheide(Fehlerentscheidung.UEBERSPRINGEN)
    a.steuerung.bis_ruhe()
    assert _fehlerart(a, "02_M2") == "abweichung"
    assert "Modus" in str(a.steuerung.momentaufnahme().fehler_offen)


def test_keine_datei_nach_scan(tmp_path: Path) -> None:
    a = aufbau(tmp_path, [messung(tmp_path, "M1")], drehbuch=[KeineDatei(vorgang=0)])
    a.starte()
    a.steuerung.bis_ruhe()
    assert _fehlerart(a) == "keine_datei"
    assert a.protokoll("01_M1")["messdatei_sha256_grund"] == "Messdatei nicht vorhanden"


def test_vorzeitiges_ende_gilt_als_fertig_mit_einschraenkung(tmp_path: Path) -> None:
    a = aufbau(
        tmp_path, [messung(tmp_path, "M1")], drehbuch=[VorzeitigesEnde(vorgang=0, nach_punkten=3)]
    )
    a.starte()
    a.steuerung.bis_ruhe()
    p = a.protokoll("01_M1")
    assert p["status"] == "fertig"
    einschraenkungen = p["einschraenkungen"]
    assert isinstance(einschraenkungen, list)
    assert any("Vollständigkeit" in str(e) for e in einschraenkungen)


@pytest.mark.parametrize(
    ("datei", "teil"),
    [("fehlt.set", "fehlt"), ("falsch.txt", "Endung")],
)
def test_vorpruefung_einstellungsdatei(tmp_path: Path, datei: str, teil: str) -> None:
    m = Messung(name="M1", einstellungsdatei=str(tmp_path / datei))
    if datei.endswith(".txt"):
        (tmp_path / datei).write_text("x")
    a = aufbau(tmp_path, [m])
    a.starte()
    a.steuerung.bis_ruhe()
    assert _fehlerart(a) == "vorpruefung"
    assert teil in str(a.steuerung.momentaufnahme().fehler_offen)


def test_einstellungen_sichern_und_meldungen(tmp_path: Path) -> None:
    a = aufbau(
        tmp_path,
        [messung(tmp_path, "M1")],
        konfiguration=AblaufKonfiguration(einstellungen_sichern=True),
        drehbuch=[MeldungBeiPunkt(vorgang=0, nach_punkten=2, stil=48, text="Achtung")],
    )
    a.starte()
    a.steuerung.bis_ruhe()
    assert (a.ordner() / "01_M1.einstellungen.set").is_file()
    assert a.protokoll("01_M1")["meldungen"] == [{"stil": 48, "text": "Achtung", "antwort": None}]


def test_fortschritt_geschaetzt_ueber_zeit(tmp_path: Path) -> None:
    a = aufbau(tmp_path, [messung(tmp_path, "M1"), messung(tmp_path, "M2")])
    a.starte()
    a.laufe_bis(lambda: a.steuerung.braucht_takt() and a.uhr.monotonic() >= 3.0)
    f = a.steuerung.momentaufnahme().fortschritt
    assert f is not None and f.geschaetzt and f.quelle == "zeitschaetzung"
    # 9 Punkte zu 1 s (Konfigurationsschätzung); Stand nach dem letzten Takt bei 2,5 s.
    # Toleranz: exakte Arithmetik auf Vielfachen von 0,5 s, nur Rundung.
    assert f.anteil is not None and math.isclose(f.anteil, 2.5 / 9, rel_tol=1e-12)
    assert f.restzeit_s is not None and math.isclose(f.restzeit_s, 6.5, rel_tol=1e-12)
    assert math.isclose(f.zeitlimit_rest_s, 600.0 - 2.5, rel_tol=1e-12)
    # Zweite Messung nutzt die gemessene Punktdauer der ersten (9 s Scan / 9 Punkte)
    a.steuerung.bis_ruhe()
    assert a.steuerung.momentaufnahme().fortschritt is None


def test_fortschritt_aus_ereignissen(tmp_path: Path) -> None:
    a = aufbau(
        tmp_path,
        [messung(tmp_path, "M1")],
        sim_konfiguration=SimulatorKonfiguration(fortschritt_ereignisse=True),
    )
    a.starte()
    a.laufe_bis(lambda: a.steuerung.braucht_takt() and a.uhr.monotonic() >= 3.0)
    f = a.steuerung.momentaufnahme().fortschritt
    assert f is not None and not f.geschaetzt and f.quelle == "ereignisse"
    assert f.anteil is not None and math.isclose(f.anteil, 2 / 9, rel_tol=1e-12)
    a.steuerung.bis_ruhe()
    assert a.protokoll("01_M1")["fortschritt_quelle"] == "ereignisse"


def test_befehle_im_falschen_zustand_werden_verworfen_und_gemeldet(tmp_path: Path) -> None:
    a = aufbau(tmp_path, [messung(tmp_path, "M1")])
    for befehl in (
        a.steuerung.pausiere,
        a.steuerung.setze_fort,
        a.steuerung.brich_ab,
        a.steuerung.bestaetige,
        a.steuerung.quittiere,
    ):
        befehl()
    a.steuerung.entscheide(Fehlerentscheidung.WIEDERHOLEN)
    a.steuerung.schritt()
    verworfen = [e.daten["befehl"] for e in a.ereignisse if e.art == "befehl_verworfen"]
    assert verworfen == [
        "pause",
        "fortsetzen",
        "abbrechen",
        "bestaetigen",
        "quittieren",
        "wiederholen",
    ]
    assert a.steuerung.zustand is DurchgangZustand.BEREIT


def test_start_ohne_verbindung_und_doppelter_start(tmp_path: Path) -> None:
    a = aufbau(tmp_path, [messung(tmp_path, "M1")], verbinden=False)
    a.starte()
    a.steuerung.schritt()
    assert a.steuerung.zustand is DurchgangZustand.BEREIT
    a.steuerung.verbinde()
    a.steuerung.schritt()
    a.starte()
    a.starte()
    a.steuerung.schritt()
    verworfen = [e.text for e in a.ereignisse if e.art == "befehl_verworfen"]
    assert "keine Verbindung" in verworfen[0]
    assert "Zustand laeuft" in verworfen[1]


def test_start_mit_fehlender_wurzel_wird_verworfen(tmp_path: Path) -> None:
    a = aufbau(tmp_path, [messung(tmp_path, "M1")])
    a.wurzel = tmp_path / "gibt_es_nicht"
    a.starte()
    a.steuerung.schritt()
    assert a.steuerung.zustand is DurchgangZustand.BEREIT
    assert any("Durchgangsordner" in e.text for e in a.ereignisse if e.art == "befehl_verworfen")


def test_messfreigabe_verweigert_beendet_durchgang(tmp_path: Path) -> None:
    a = aufbau(tmp_path, [messung(tmp_path, "M1")], betriebsart="nur_lesen")
    a.starte()
    a.steuerung.bis_ruhe()
    stand = a.steuerung.momentaufnahme()
    assert stand.ergebnis is DurchgangErgebnis.ABGEBROCHEN
    assert a.ws.eintraege()[0].zustand is MessungZustand.WARTEND


def test_verbinden_scheitert(tmp_path: Path) -> None:
    a = aufbau(
        tmp_path,
        [],
        sim_konfiguration=SimulatorKonfiguration(psv_laeuft=False),
        verbinden=False,
    )
    a.steuerung.verbinde()
    a.steuerung.schritt()
    assert a.steuerung.momentaufnahme().verbindung is None
    assert any("Verbinden fehlgeschlagen" in e.text for e in a.ereignisse)


def test_quittieren_und_zweiter_durchgang_nummeriert_neu(tmp_path: Path) -> None:
    a = aufbau(tmp_path, [messung(tmp_path, "M1")])
    a.starte()
    a.steuerung.bis_ruhe()
    erster = a.ordner()
    a.steuerung.quittiere()
    a.steuerung.schritt()
    assert a.steuerung.zustand is DurchgangZustand.BEREIT
    a.ws.einfuegen(1, messung(tmp_path, "M2"))
    a.uhr.vorstellen(1.0)
    a.starte()
    a.steuerung.bis_ruhe()
    assert a.ordner() != erster
    assert (a.ordner() / "01_M2.svd").is_file()


def test_abbrechen_im_pausenpunkt_setzt_ihn_zurueck(tmp_path: Path) -> None:
    pp = Pausenpunkt(text="Umbau")
    a = aufbau(tmp_path, [pp, messung(tmp_path, "M1")])
    a.starte()
    a.steuerung.bis_ruhe()
    a.steuerung.brich_ab()
    a.steuerung.bis_ruhe()
    assert [e.zustand.value for e in a.ws.eintraege()] == ["wartend", "wartend"]


def test_abbrechen_pausiert_und_pause_vor_fehler(tmp_path: Path) -> None:
    a = aufbau(
        tmp_path,
        [messung(tmp_path, "M1"), messung(tmp_path, "M2")],
        drehbuch=[KeineDatei(vorgang=0)],
    )
    a.starte()
    a.laufe_bis(lambda: a.steuerung.braucht_takt())
    a.steuerung.pausiere()
    a.steuerung.bis_ruhe()
    # Fehler während Pause angefordert: erst entscheiden, dann pausiert
    assert a.steuerung.momentaufnahme().durchgang is DurchgangZustand.WARTET_AUF_ENTSCHEIDUNG
    a.steuerung.entscheide(Fehlerentscheidung.UEBERSPRINGEN)
    a.steuerung.bis_ruhe()
    assert a.steuerung.momentaufnahme().durchgang is DurchgangZustand.PAUSIERT
    a.steuerung.brich_ab()
    a.steuerung.bis_ruhe()
    assert a.steuerung.momentaufnahme().ergebnis is DurchgangErgebnis.ABGEBROCHEN


def test_abbrechen_waehrend_zeitlimit_stop_sendet_kein_zweites_stop(tmp_path: Path) -> None:
    from ldv_automation.geraet.simulator import Haenger

    a = aufbau(
        tmp_path,
        [messung(tmp_path, "M1", zeitlimit_s=2.0)],
        drehbuch=[Haenger(vorgang=0, stop_wirkt=False)],
    )
    a.starte()
    a.laufe_bis(lambda: "stoppe" in a.sim.aufgerufene_methoden())
    a.steuerung.brich_ab()
    a.steuerung.bis_ruhe()
    assert a.sim.aufgerufene_methoden().count("stoppe") == 1
    assert a.steuerung.zustand is DurchgangZustand.GERAET_UNKLAR


def test_abbruch_waehrend_natuerlichem_ende_gilt_als_fertig(tmp_path: Path) -> None:
    a = aufbau(tmp_path, [messung(tmp_path, "M1"), messung(tmp_path, "M2")])
    a.starte()
    # bis kurz vor Scanende (9 s), dann Zeit über das Ende stellen und abbrechen
    a.laufe_bis(lambda: a.steuerung.braucht_takt() and a.uhr.monotonic() >= 8.5)
    a.uhr.vorstellen(5.0)
    a.steuerung.brich_ab()
    a.steuerung.bis_ruhe()
    assert [e.zustand.value for e in a.ws.eintraege()] == ["fertig", "wartend"]
    assert a.steuerung.momentaufnahme().ergebnis is DurchgangErgebnis.ABGEBROCHEN


def test_geraet_tauschen(tmp_path: Path) -> None:
    a = aufbau(tmp_path, [])
    neu = Simulator(a.uhr.monotonic, betriebsart="trockenlauf")
    a.steuerung.tausche_geraet(lambda: neu, "trockenlauf")
    a.steuerung.schritt()
    assert a.steuerung.geraet is neu
    assert a.steuerung.betriebsart == "trockenlauf"
    assert a.steuerung.momentaufnahme().verbindung is None
    assert a.sim.aufgerufene_methoden()[-1] == "trenne"

    def kaputt() -> Simulator:
        raise ValueError("nicht erzeugbar")

    a.steuerung.tausche_geraet(kaputt, "messen")
    a.steuerung.schritt()
    assert not a.steuerung.hat_geraet
    with pytest.raises(RuntimeError):
        _ = a.steuerung.geraet
    a.steuerung.verbinde()
    a.steuerung.schritt()
    assert any("kein Gerät" in e.text for e in a.ereignisse)


def test_warteschlange_ersetzen_nur_in_ruhe(tmp_path: Path) -> None:
    a = aufbau(tmp_path, [messung(tmp_path, "M1")])
    neu = Warteschlange()
    a.steuerung.setze_warteschlange(neu)
    assert a.steuerung.warteschlange is neu
    a.steuerung.pausiere()
    with pytest.raises(ValueError, match="ausstehenden"):
        a.steuerung.setze_warteschlange(Warteschlange())


def test_konfiguration_prueft_werte() -> None:
    with pytest.raises(ValueError, match="poll_s"):
        AblaufKonfiguration(poll_s=0.0)
    with pytest.raises(ValueError, match="zeitlimit_s"):
        AblaufKonfiguration(zeitlimit_s=math.inf)


def test_bis_ruhe_hat_obergrenze(tmp_path: Path) -> None:
    a = aufbau(tmp_path, [messung(tmp_path, "M1")])
    a.starte()
    with pytest.raises(RuntimeError, match="keine Ruhe"):
        a.steuerung.bis_ruhe(max_schritte=3)


def test_geraete_thread_durchgang_ohne_verklemmung(tmp_path: Path) -> None:
    """Echter Thread mit Echtzeituhr: Start, Durchgang, Ende, Join mit Zeitlimit."""
    uhr = Echtzeituhr()
    sim = Simulator(
        uhr.monotonic,
        konfiguration=SimulatorKonfiguration(punkte_anzahl=3, punktdauer_s=0.01),
    )
    wurzel = tmp_path / "daten"
    wurzel.mkdir()
    steuerung = Steuerung(
        warteschlange=Warteschlange([messung(tmp_path, "M1"), messung(tmp_path, "M2")]),
        geraet=sim,
        betriebsart="simulator",
        uhr=uhr,
        build_info=BUILD,
        konfiguration=AblaufKonfiguration(poll_s=0.005),
    )
    steuerung.starte_thread()
    with pytest.raises(RuntimeError, match="läuft bereits"):
        steuerung.starte_thread()
    steuerung.verbinde()
    steuerung.starte(
        DurchgangsAuftrag(
            name="Thread",
            messdaten_wurzel=wurzel,
            betriebsart="simulator",
            trockenlauf=False,
            messfreigabe=True,
        )
    )
    frist = time.monotonic() + 10.0
    while steuerung.zustand is not DurchgangZustand.BEENDET and time.monotonic() < frist:
        time.sleep(0.01)
    assert steuerung.beende_thread(timeout_s=5.0)
    assert steuerung.momentaufnahme().ergebnis is DurchgangErgebnis.VOLLSTAENDIG


def test_interner_fehler_im_thread_wird_sichtbar(tmp_path: Path) -> None:
    uhr = Echtzeituhr()

    class Kaputt(Simulator):
        def verbinde(self):  # type: ignore[no-untyped-def]
            raise RuntimeError("unerwartet")

    steuerung = Steuerung(
        warteschlange=Warteschlange(),
        geraet=Kaputt(uhr.monotonic),
        betriebsart="simulator",
        uhr=uhr,
        build_info=BUILD,
        konfiguration=AblaufKonfiguration(poll_s=0.005),
    )
    steuerung.starte_thread()
    steuerung.verbinde()
    frist = time.monotonic() + 5.0
    while steuerung.momentaufnahme().interner_fehler is None and time.monotonic() < frist:
        time.sleep(0.01)
    assert steuerung.beende_thread(timeout_s=5.0)
    stand = steuerung.momentaufnahme()
    assert stand.durchgang is DurchgangZustand.GERAET_UNKLAR
    assert "unerwartet" in str(stand.interner_fehler)


def test_beende_thread_ohne_thread() -> None:
    uhr = Echtzeituhr()
    steuerung = Steuerung(
        warteschlange=Warteschlange(),
        geraet=None,
        betriebsart="simulator",
        uhr=uhr,
        build_info=BUILD,
    )
    assert steuerung.beende_thread()


def test_startfehler_mit_wiederholen_zaehlt_versuch(tmp_path: Path) -> None:
    a = aufbau(tmp_path, [messung(tmp_path, "M1")], drehbuch=[StartFehler(vorgang=0)])
    a.starte()
    a.steuerung.bis_ruhe()
    a.steuerung.entscheide(Fehlerentscheidung.WIEDERHOLEN)
    a.steuerung.bis_ruhe()
    m = a.ws.eintraege()[0]
    assert isinstance(m, Messung) and m.versuch == 2 and m.zustand is MessungZustand.FERTIG
    assert a.steuerung.momentaufnahme().laufinfo[m.id].nummer == 1
