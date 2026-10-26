"""Akzeptanzkriterien U2-1 bis U2-10 (Plan P2, Abschnitt 8), gegen Simulator und Testuhr.

Der "Schrittmodus" ist hier das taktweise Weiterschalten der Steuerung per
``schritt()``: Zwischen zwei Takten steht die Steuerung, und der Test kann die
Warteschlange bearbeiten, während der Simulator mitten im Scan ist.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import pytest
from ablauf_hilfen import SCHREIBAUFRUFE, Aufbau, aufbau, ist_zustand, messung

from ldv_automation.ablauf.fehlerstrategie import FehlerEreignis, FehlerReaktion
from ldv_automation.ablauf.steuerung import (
    DurchgangErgebnis,
    DurchgangZustand,
    Fehlerentscheidung,
)
from ldv_automation.domaene.eintraege import MessungZustand, Pausenpunkt, PausenpunktZustand
from ldv_automation.geraet.simulator import (
    SIMULATOR_KENNUNG,
    Haenger,
    ScanFehler,
    SimulatorKonfiguration,
    StartFehler,
)
from ldv_automation.protokoll.messprotokoll import PFLICHTFELDER, fehlende_pflichtfelder
from ldv_automation.protokoll.version import BuildInfo


def _zustaende(a: Aufbau) -> list[str]:
    return [e.zustand.value for e in a.ws.eintraege()]


# --- U2-1 -----------------------------------------------------------------------------


def test_u2_1_drei_messungen_laufen_vollstaendig_durch(tmp_path: Path) -> None:
    a = aufbau(tmp_path, [messung(tmp_path, f"M{i}") for i in (1, 2, 3)])
    a.starte()
    a.steuerung.bis_ruhe()

    stand = a.steuerung.momentaufnahme()
    assert stand.durchgang is DurchgangZustand.BEENDET
    assert stand.ergebnis is DurchgangErgebnis.VOLLSTAENDIG
    assert _zustaende(a) == ["fertig"] * 3
    ordner = a.ordner()
    svd = sorted(p.name for p in ordner.glob("*.svd"))
    assert svd == ["01_M1.svd", "02_M2.svd", "03_M3.svd"]
    for name in svd:
        assert (ordner / name).read_bytes().startswith(SIMULATOR_KENNUNG)
    protokolle = sorted(p.name for p in ordner.glob("*.protokoll.json"))
    assert protokolle == ["01_M1.protokoll.json", "02_M2.protokoll.json", "03_M3.protokoll.json"]
    assert all(a.protokoll(f"0{i}_M{i}")["status"] == "fertig" for i in (1, 2, 3))
    assert a.sim.aufgerufene_methoden().count("starte_scan") == 3
    # Messfreigabe gesetzt und am Ende entzogen
    freigaben = [args for name, args in a.sim.aufrufe if name == "setze_messfreigabe"]
    assert freigaben == [(True,), (False,)]


# --- U2-2 -----------------------------------------------------------------------------


def test_u2_2_bearbeiten_und_einfuegen_waehrend_messung_1(tmp_path: Path) -> None:
    m1 = messung(tmp_path, "M1", {"mittelung.anzahl": 5})
    m2 = messung(tmp_path, "M2", {"mittelung.anzahl": 5})
    m3 = messung(tmp_path, "M3")
    a = aufbau(tmp_path, [m1, m2, m3])
    a.starte()
    # Schrittweise bis Messung 1 mitten im Scan ist
    a.laufe_bis(lambda: a.steuerung.braucht_takt() and a.uhr.monotonic() >= 2.0)
    assert a.ws.hole(m1.id).zustand is MessungZustand.LAEUFT
    assert a.sim.aufgerufene_methoden().count("starte_scan") == 1

    a.ws.bearbeiten(m2.id, parameter={"mittelung.anzahl": 10})
    m4 = messung(tmp_path, "M4", {"mittelung.anzahl": 7})
    a.ws.einfuegen(len(a.ws), m4)
    with pytest.raises(ValueError, match="LAEUFT"):
        a.ws.bearbeiten(m1.id, parameter={"mittelung.anzahl": 99})

    a.steuerung.bis_ruhe()
    assert a.steuerung.momentaufnahme().ergebnis is DurchgangErgebnis.VOLLSTAENDIG
    assert _zustaende(a) == ["fertig"] * 4
    p1 = a.protokoll("01_M1")
    p2 = a.protokoll("02_M2")
    p4 = a.protokoll("04_M4")
    assert p1["geaenderte_parameter"] == [
        {"schluessel": "mittelung.anzahl", "einheit": "", "soll": 5, "ist": 5}
    ]
    assert p2["geaenderte_parameter"] == [
        {"schluessel": "mittelung.anzahl", "einheit": "", "soll": 10, "ist": 10}
    ]
    assert p4["durchgang_id"] == p1["durchgang_id"]
    gesetzt = [args[0] for name, args in a.sim.aufrufe if name == "setze_parameter"]
    assert gesetzt == [
        {"mittelung.anzahl": 5},
        {"mittelung.anzahl": 10},
        {"mittelung.anzahl": 7},
    ]


# --- U2-3 -----------------------------------------------------------------------------


def test_u2_3_pausenpunkt_haelt_bis_bestaetigung(tmp_path: Path) -> None:
    m1 = messung(tmp_path, "M1")
    pp = Pausenpunkt(text="Umbau Prüfling")
    m2 = messung(tmp_path, "M2")
    a = aufbau(tmp_path, [m1, pp, m2])
    a.starte()
    a.steuerung.bis_ruhe()

    assert a.steuerung.zustand is DurchgangZustand.WARTET_AUF_BESTAETIGUNG
    assert a.steuerung.momentaufnahme().pausenpunkt_id == pp.id
    a.uhr.vorstellen(3600.0)
    for _ in range(100):
        a.steuerung.schritt()
    a.steuerung.bis_ruhe()
    assert a.ws.hole(m2.id).zustand is MessungZustand.WARTEND
    assert a.sim.aufgerufene_methoden().count("starte_scan") == 1

    a.steuerung.bestaetige()
    a.steuerung.bis_ruhe()
    assert a.ws.hole(pp.id).zustand is PausenpunktZustand.ERLEDIGT
    assert a.ws.hole(m2.id).zustand is MessungZustand.FERTIG
    assert a.steuerung.momentaufnahme().ergebnis is DurchgangErgebnis.VOLLSTAENDIG


# --- U2-4 -----------------------------------------------------------------------------


def test_u2_4_pause_waehrend_messung_1(tmp_path: Path) -> None:
    m1, m2 = messung(tmp_path, "M1"), messung(tmp_path, "M2")
    a = aufbau(tmp_path, [m1, m2])
    a.starte()
    a.laufe_bis(lambda: a.steuerung.braucht_takt())
    a.steuerung.pausiere()
    a.steuerung.bis_ruhe()

    assert a.steuerung.zustand is DurchgangZustand.PAUSIERT
    assert a.ws.hole(m1.id).zustand is MessungZustand.FERTIG
    assert a.ws.hole(m2.id).zustand is MessungZustand.WARTEND
    a.uhr.vorstellen(1000.0)
    a.steuerung.schritt()
    assert a.ws.hole(m2.id).zustand is MessungZustand.WARTEND

    a.steuerung.setze_fort()
    a.steuerung.bis_ruhe()
    assert a.ws.hole(m2.id).zustand is MessungZustand.FERTIG
    assert a.durchgang_wechsel() == [
        "laeuft",
        "pause_angefordert",
        "pausiert",
        "laeuft",
        "beendet",
    ]


def test_u2_4_abbrechen_waehrend_messung_1(tmp_path: Path) -> None:
    m1, m2, m3 = (messung(tmp_path, f"M{i}") for i in (1, 2, 3))
    pp = Pausenpunkt(text="Pause")
    a = aufbau(tmp_path, [m1, m2, pp, m3])
    a.starte()
    a.laufe_bis(lambda: a.steuerung.braucht_takt() and a.uhr.monotonic() >= 3.0)
    a.steuerung.brich_ab()
    a.steuerung.bis_ruhe()

    stand = a.steuerung.momentaufnahme()
    assert stand.durchgang is DurchgangZustand.BEENDET
    assert stand.ergebnis is DurchgangErgebnis.ABGEBROCHEN
    assert a.sim.aufgerufene_methoden().count("stoppe") == 1
    assert _zustaende(a) == ["abgebrochen", "wartend", "wartend", "wartend"]
    assert a.protokoll("01_M1")["status"] == "abgebrochen"
    # Die Datei mit Teilpunkten bleibt erhalten
    assert (a.ordner() / "01_M1.svd").is_file()

    ende = [z for z in a.ereignisprotokoll() if z["art"] == "durchgang_beendet"]
    assert len(ende) == 1
    eintraege = ende[0]["eintraege"]
    assert isinstance(eintraege, list)
    assert [e["eintrag_id"] for e in eintraege] == [str(x.id) for x in (m1, m2, pp, m3)]
    assert [e["hinweis"] for e in eintraege] == [None] + ["nicht gestartet"] * 3


# --- U2-5 -----------------------------------------------------------------------------


def _scanfehler_aufbau(tmp_path: Path) -> Aufbau:
    m1, m2 = messung(tmp_path, "M1"), messung(tmp_path, "M2")
    a = aufbau(tmp_path, [m1, m2], drehbuch=[ScanFehler(vorgang=0, nach_s=2.0)])
    a.starte()
    a.steuerung.bis_ruhe()
    return a


def test_u2_5_fehler_fuehrt_zu_entscheidung_wiederholen_v2(tmp_path: Path) -> None:
    a = _scanfehler_aufbau(tmp_path)
    stand = a.steuerung.momentaufnahme()
    assert stand.durchgang is DurchgangZustand.WARTET_AUF_ENTSCHEIDUNG
    assert stand.fehler_offen is not None
    erste = a.ordner() / "01_M1.svd"
    hash_vorher = hashlib.sha256(erste.read_bytes()).hexdigest()
    p1 = a.protokoll("01_M1")
    assert p1["status"] == "fehler"
    assert "vorläufig" in str(p1["fehlerstrategie"])
    assert p1["fehlerentscheidung"] == "ausstehend"
    assert p1["messdatei_sha256"] == hash_vorher

    a.steuerung.entscheide(Fehlerentscheidung.WIEDERHOLEN)
    a.steuerung.bis_ruhe()

    assert (a.ordner() / "01_M1_v2.svd").is_file()
    assert hashlib.sha256(erste.read_bytes()).hexdigest() == hash_vorher
    p1v2 = a.protokoll("01_M1_v2")
    assert p1v2["versuch"] == 2
    assert p1v2["status"] == "fertig"
    assert "vorläufig" in str(p1v2["fehlerstrategie"])
    assert _zustaende(a) == ["fertig", "fertig"]
    entscheidungen = [z for z in a.ereignisprotokoll() if z["art"] == "fehlerentscheidung"]
    assert [z["entscheidung"] for z in entscheidungen] == ["wiederholen"]
    assert entscheidungen[0]["versuch"] == 1


def test_u2_5_ueberspringen_setzt_fort(tmp_path: Path) -> None:
    a = _scanfehler_aufbau(tmp_path)
    a.steuerung.entscheide(Fehlerentscheidung.UEBERSPRINGEN)
    a.steuerung.bis_ruhe()
    stand = a.steuerung.momentaufnahme()
    assert stand.ergebnis is DurchgangErgebnis.VOLLSTAENDIG
    assert _zustaende(a) == ["fehler", "fertig"]
    assert stand.laufinfo[a.ws.eintraege()[0].id].uebersprungen
    arten = [z["art"] for z in a.ereignisprotokoll()]
    assert "uebersprungen_nach_fehler" in arten


def test_u2_5_abbrechen_beendet(tmp_path: Path) -> None:
    a = _scanfehler_aufbau(tmp_path)
    a.steuerung.entscheide(Fehlerentscheidung.ABBRECHEN)
    a.steuerung.bis_ruhe()
    stand = a.steuerung.momentaufnahme()
    assert stand.durchgang is DurchgangZustand.BEENDET
    assert stand.ergebnis is DurchgangErgebnis.ABGEBROCHEN
    assert _zustaende(a) == ["fehler", "wartend"]


def test_u2_5_startfehler_ebenfalls_entscheidung(tmp_path: Path) -> None:
    a = aufbau(
        tmp_path,
        [messung(tmp_path, "M1")],
        drehbuch=[StartFehler(vorgang=0, hresult=-2147352567)],
    )
    a.starte()
    a.steuerung.bis_ruhe()
    assert a.steuerung.zustand is DurchgangZustand.WARTET_AUF_ENTSCHEIDUNG
    p = a.protokoll("01_M1")
    fehler = p["fehler"]
    assert isinstance(fehler, dict)
    assert fehler["art"] == "geraet"
    assert fehler["hresult"] == -2147352567
    assert fehler["methode"] == "starte_scan"
    assert p["messdatei_sha256"] is None
    assert p["messdatei_sha256_grund"]


# --- U2-6 -----------------------------------------------------------------------------


class ImmerUeberspringen:
    """Test-Strategie: nie anhalten."""

    @property
    def bezeichnung(self) -> str:
        return "ImmerUeberspringen (Test)"

    def entscheide(self, ereignis: FehlerEreignis) -> FehlerReaktion:
        return FehlerReaktion.UEBERSPRINGEN


class ImmerAbbrechen:
    @property
    def bezeichnung(self) -> str:
        return "ImmerAbbrechen (Test)"

    def entscheide(self, ereignis: FehlerEreignis) -> FehlerReaktion:
        return FehlerReaktion.ABBRECHEN


def test_u2_6_austauschbare_strategie_laeuft_ohne_halt(tmp_path: Path) -> None:
    eintraege = [messung(tmp_path, f"M{i}") for i in (1, 2, 3)]
    a = aufbau(
        tmp_path,
        eintraege,
        drehbuch=[StartFehler(vorgang=0), ScanFehler(vorgang=1, nach_s=1.0)],
        strategie=ImmerUeberspringen(),
    )
    a.starte()
    a.steuerung.bis_ruhe()
    assert a.steuerung.momentaufnahme().ergebnis is DurchgangErgebnis.VOLLSTAENDIG
    assert "wartet_auf_entscheidung" not in a.durchgang_wechsel()
    assert _zustaende(a) == ["fehler", "fehler", "fertig"]
    p = a.protokoll("01_M1")
    assert p["fehlerstrategie"] == "ImmerUeberspringen (Test)"
    assert p["fehlerentscheidung"] == "ueberspringen"


def test_u2_6_strategie_abbrechen_beendet_sofort(tmp_path: Path) -> None:
    a = aufbau(
        tmp_path,
        [messung(tmp_path, "M1"), messung(tmp_path, "M2")],
        drehbuch=[StartFehler(vorgang=0)],
        strategie=ImmerAbbrechen(),
    )
    a.starte()
    a.steuerung.bis_ruhe()
    assert a.steuerung.momentaufnahme().ergebnis is DurchgangErgebnis.ABGEBROCHEN
    assert _zustaende(a) == ["fehler", "wartend"]


# --- U2-7 -----------------------------------------------------------------------------


def test_u2_7_eingerasteter_wert_ist_fehler_vor_scan(tmp_path: Path) -> None:
    konf = SimulatorKonfiguration(bandbreiten_hz=(3125.0, 6250.0, 12500.0))
    a = aufbau(
        tmp_path,
        [messung(tmp_path, "M1", {"fft.bandbreite_hz": 5000.0})],
        sim_konfiguration=konf,
    )
    a.starte()
    a.steuerung.bis_ruhe()
    assert a.ws.eintraege()[0].zustand is MessungZustand.FEHLER
    assert "starte_scan" not in a.sim.aufgerufene_methoden()
    p = a.protokoll("01_M1")
    fehler = p["fehler"]
    assert isinstance(fehler, dict)
    assert fehler["art"] == "abweichung"
    assert p["geaenderte_parameter"] == [
        {"schluessel": "fft.bandbreite_hz", "einheit": "Hz", "soll": 5000.0, "ist": 6250.0}
    ]


# --- U2-8 -----------------------------------------------------------------------------


def test_u2_8_vorhandene_zieldatei_fehler_ohne_geraeteaufruf(tmp_path: Path) -> None:
    a = aufbau(tmp_path, [messung(tmp_path, "M1")])
    a.starte()
    a.steuerung.schritt()  # Start verarbeiten (Ordner, Freigabe)
    assert a.steuerung.zustand is DurchgangZustand.LAEUFT
    ziel = a.ordner() / "01_M1.svd"
    ziel.write_bytes(b"FREMDE DATEN")
    aufrufe_vorher = len(a.sim.aufrufe)

    a.steuerung.schritt()  # Messung 1 beanspruchen und vorprüfen

    assert a.ws.eintraege()[0].zustand is MessungZustand.FEHLER
    assert a.sim.aufrufe[aufrufe_vorher:] == ()
    assert ziel.read_bytes() == b"FREMDE DATEN"
    p = a.protokoll("01_M1")
    fehler = p["fehler"]
    assert isinstance(fehler, dict)
    assert fehler["art"] == "vorpruefung"
    assert p["messdatei_sha256"] is None


# --- U2-9 -----------------------------------------------------------------------------


def test_u2_9_haenger_zeitlimit_stoppt_und_fehler(tmp_path: Path) -> None:
    a = aufbau(
        tmp_path,
        [messung(tmp_path, "M1", zeitlimit_s=5.0)],
        drehbuch=[Haenger(vorgang=0)],
    )
    a.starte()
    a.steuerung.bis_ruhe()
    assert a.sim.aufgerufene_methoden().count("stoppe") == 1
    assert a.ws.eintraege()[0].zustand is MessungZustand.FEHLER
    assert a.steuerung.zustand is DurchgangZustand.WARTET_AUF_ENTSCHEIDUNG
    fehler = a.protokoll("01_M1")["fehler"]
    assert isinstance(fehler, dict)
    assert fehler["art"] == "zeitlimit"
    # Stop erst nach Ablauf des Zeitlimits (Testuhr), höchstens einen Takt später
    assert 5.0 <= a.uhr.monotonic() <= 5.0 + 2 * 0.5 + 1e-9


def test_u2_9_stop_wirkt_nicht_geraet_unklar_ohne_schreibaufrufe(tmp_path: Path) -> None:
    a = aufbau(
        tmp_path,
        [messung(tmp_path, "M1", zeitlimit_s=5.0), messung(tmp_path, "M2")],
        drehbuch=[Haenger(vorgang=0, stop_wirkt=False)],
    )
    a.starte()
    a.steuerung.bis_ruhe()

    assert a.steuerung.zustand is DurchgangZustand.GERAET_UNKLAR
    methoden = a.sim.aufgerufene_methoden()
    index_stop = methoden.index("stoppe")
    assert methoden.count("stoppe") == 1
    assert not SCHREIBAUFRUFE & set(methoden[index_stop + 1 :])
    assert _zustaende(a) == ["fehler", "wartend"]
    fehler = a.protokoll("01_M1")["fehler"]
    assert isinstance(fehler, dict)
    assert fehler["art"] == "geraet_unklar"

    # Danach keinerlei Geräteaufrufe mehr, auch nicht nach langer Zeit
    anzahl = len(a.sim.aufrufe)
    a.uhr.vorstellen(10_000.0)
    for _ in range(50):
        a.steuerung.schritt()
    assert len(a.sim.aufrufe) == anzahl

    # Nur Trennen ist möglich und beendet den Durchgang
    a.steuerung.pausiere()
    a.steuerung.schritt()
    assert a.steuerung.zustand is DurchgangZustand.GERAET_UNKLAR
    a.steuerung.trenne()
    a.steuerung.schritt()
    stand = a.steuerung.momentaufnahme()
    assert stand.durchgang is DurchgangZustand.BEENDET
    assert stand.ergebnis is DurchgangErgebnis.GERAET_UNKLAR
    assert a.sim.aufgerufene_methoden()[anzahl:] == ("trenne",)


# --- U2-10 ----------------------------------------------------------------------------


def _alle_protokolle(ordner: Path) -> list[dict[str, object]]:
    return [json.loads(p.read_text("utf-8")) for p in sorted(ordner.glob("*.protokoll.json"))]


def _pruefe_schema(daten: dict[str, object]) -> None:
    assert fehlende_pflichtfelder(daten) == []
    assert tuple(daten) == PFLICHTFELDER
    assert daten["schema_version"] == 1
    assert (daten["messdatei_sha256"] is None) != (daten["messdatei_sha256_grund"] is None)
    for feld in ("zeit_start", "zeit_ende"):
        zeit = daten[feld]
        assert isinstance(zeit, dict)
        assert set(zeit) == {"lokal", "utc"}
        assert str(zeit["utc"]).endswith("+00:00")


def test_u2_10_schema_bei_fertig_fehler_abgebrochen(tmp_path: Path) -> None:
    a = aufbau(
        tmp_path,
        [messung(tmp_path, "M1"), messung(tmp_path, "M2"), messung(tmp_path, "M3")],
        drehbuch=[StartFehler(vorgang=1)],
    )
    a.starte()
    a.steuerung.bis_ruhe()
    a.steuerung.entscheide(Fehlerentscheidung.UEBERSPRINGEN)
    a.laufe_bis(lambda: a.steuerung.braucht_takt() and a.sim.vorgang == 2)
    a.steuerung.brich_ab()
    a.steuerung.bis_ruhe()

    protokolle = _alle_protokolle(a.ordner())
    assert [p["status"] for p in protokolle] == ["fertig", "fehler", "abgebrochen"]
    for p in protokolle:
        _pruefe_schema(p)
        assert p["git_hash"] == "0123456789abcdef0123456789abcdef01234567"
        assert p["git_hash_grund"] is None
        assert p["psv_version"] == "10.x-SIM"
        assert p["betriebsart"] == "simulator"
        assert p["einstellungsdatei"] == {
            "pfad": str(tmp_path / "basis.set"),
            "sha256": hashlib.sha256(b"SET-PLATZHALTER").hexdigest(),
        }
    assert protokolle[0]["einstellungen_ist"] is not None
    assert protokolle[0]["messpunkte_anzahl"] == 9


def test_u2_10_ohne_git_hash_steht_der_grund_im_protokoll(tmp_path: Path) -> None:
    ohne = BuildInfo(
        paket_version="0.1.0", git_hash=None, git_dirty=None, quelle="keine", grund="git fehlt"
    )
    a = aufbau(tmp_path, [messung(tmp_path, "M1")], build=ohne)
    a.starte()
    a.steuerung.bis_ruhe()
    p = a.protokoll("01_M1")
    _pruefe_schema(p)
    assert p["git_hash"] is None
    assert p["git_hash_grund"] == "git fehlt"


def test_u2_10_dirty_stand_wird_als_einschraenkung_genannt(tmp_path: Path) -> None:
    dirty = BuildInfo(paket_version="0.1.0", git_hash="a" * 40, git_dirty=True, quelle="git")
    a = aufbau(tmp_path, [messung(tmp_path, "M1")], build=dirty)
    a.starte()
    a.steuerung.bis_ruhe()
    einschraenkungen = a.protokoll("01_M1")["einschraenkungen"]
    assert isinstance(einschraenkungen, list)
    assert any("git_dirty" in str(e) for e in einschraenkungen)


def test_hilfsfunktion_ist_zustand(tmp_path: Path) -> None:
    a = aufbau(tmp_path, [messung(tmp_path, "M1")])
    a.starte()
    a.laufe_bis(ist_zustand(a, DurchgangZustand.BEENDET))
    assert a.steuerung.momentaufnahme().ergebnis is DurchgangErgebnis.VOLLSTAENDIG
