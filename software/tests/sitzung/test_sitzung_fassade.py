"""Sitzungsfassade: U2-11, U2-12, Wächter, Bearbeitung, Befehle und Betriebsarten."""

from __future__ import annotations

import threading
import time
from pathlib import Path

import pytest

from ldv_automation.ablauf.steuerung import (
    DurchgangErgebnis,
    DurchgangZustand,
    Fehlerentscheidung,
)
from ldv_automation.ablauf.uhr import Testuhr
from ldv_automation.domaene.eintraege import Messung, Pausenpunkt
from ldv_automation.geraet.schnittstelle import Messgeraet
from ldv_automation.geraet.simulator import (
    HaengenderAufruf,
    Simulator,
    SimulatorKonfiguration,
    StartFehler,
)
from ldv_automation.protokoll.version import BuildInfo
from ldv_automation.sitzung import Betriebsart, Sitzung

GIT = BuildInfo(paket_version="0.1.0", git_hash="c" * 40, git_dirty=False, quelle="test")
OHNE_GIT = BuildInfo(
    paket_version="0.1.0", git_hash=None, git_dirty=None, quelle="keine", grund="git fehlt"
)


class Fabrik:
    """Erzeugt Simulatoren je Betriebsart und merkt sie sich."""

    def __init__(self, uhr: Testuhr, **sim: object) -> None:
        self.uhr = uhr
        self.sim = sim
        self.erzeugt: list[Simulator] = []

    def __call__(self, art: Betriebsart) -> Messgeraet:
        geraet = Simulator(self.uhr.monotonic, betriebsart=art.value, **self.sim)  # type: ignore[arg-type]
        self.erzeugt.append(geraet)
        return geraet


def _set(tmp_path: Path) -> str:
    pfad = tmp_path / "basis.set"
    pfad.write_bytes(b"SET")
    return str(pfad)


def _sitzung(
    tmp_path: Path,
    *,
    build: BuildInfo = GIT,
    betriebsart: Betriebsart = Betriebsart.SIMULATOR,
    **sim: object,
) -> tuple[Sitzung, Fabrik]:
    uhr = Testuhr()
    fabrik = Fabrik(uhr, **sim)
    wurzel = tmp_path / "daten"
    wurzel.mkdir(exist_ok=True)
    sitzung = Sitzung(
        geraete_fabrik=fabrik,
        betriebsart=betriebsart,
        uhr=uhr,
        build_info=build,
        messdaten_wurzel=wurzel,
    )
    sitzung.verarbeite()
    sitzung.verbinde()
    sitzung.verarbeite()
    return sitzung, fabrik


# --- U2-11 ----------------------------------------------------------------------------


def test_u2_11_ohne_git_hash_kein_messen(tmp_path: Path) -> None:
    s, fabrik = _sitzung(tmp_path, build=OHNE_GIT)
    s.einfuegen(0, Messung(name="M1", einstellungsdatei=_set(tmp_path)))
    with pytest.raises(ValueError, match="Git-Hash unbekannt: git fehlt"):
        s.setze_betriebsart(Betriebsart.MESSEN)
    assert s.betriebsart is Betriebsart.SIMULATOR

    # SIMULATOR funktioniert
    s.starte("sim")
    s.verarbeite()
    assert s.zustandsbild().ergebnis is DurchgangErgebnis.VOLLSTAENDIG
    s.quittiere()
    s.verarbeite()

    # TROCKENLAUF funktioniert (Gerät wird neu erzeugt)
    s.einfuegen(1, Messung(name="M2", einstellungsdatei=_set(tmp_path)))
    s.setze_betriebsart(Betriebsart.TROCKENLAUF)
    s.verarbeite()
    assert s.zustandsbild().betriebsart is Betriebsart.TROCKENLAUF
    assert [g.betriebsart for g in fabrik.erzeugt] == ["simulator", "trockenlauf"]
    assert fabrik.erzeugt[0].aufgerufene_methoden()[-1] == "trenne"
    s.verbinde()
    s.verarbeite()
    s.starte("trocken")
    s.verarbeite()
    bild = s.zustandsbild()
    assert bild.ergebnis is DurchgangErgebnis.VOLLSTAENDIG
    assert bild.eintraege[1].trockenlauf
    assert "starte_scan" not in fabrik.erzeugt[1].aufgerufene_methoden()
    # Trotz gelungenem Trockenlauf bleibt MESSEN wegen des Git-Hashs gesperrt
    with pytest.raises(ValueError, match="Git-Hash"):
        s.setze_betriebsart(Betriebsart.MESSEN)


def test_messen_freischaltung_und_bestaetigung(tmp_path: Path) -> None:
    s, fabrik = _sitzung(tmp_path, betriebsart=Betriebsart.TROCKENLAUF)
    s.einfuegen(0, Messung(name="M1", einstellungsdatei=_set(tmp_path)))
    offen = {v.name for v in s.messen_voraussetzungen() if not v.erfuellt}
    assert offen == {"trockenlauf"}
    s.starte("trocken")
    s.verarbeite()
    assert all(v.erfuellt for v in s.messen_voraussetzungen())
    s.quittiere()
    s.verarbeite()

    s.setze_betriebsart(Betriebsart.MESSEN)
    s.verarbeite()
    assert s.betriebsart is Betriebsart.MESSEN
    s.verbinde()
    s.verarbeite()
    s.einfuegen(1, Messung(name="M2", einstellungsdatei=_set(tmp_path)))
    with pytest.raises(ValueError, match="bestätigt"):
        s.starte("echt")
    s.starte("echt", messen_bestaetigt=True)
    s.verarbeite()
    messgeraet = fabrik.erzeugt[-1]
    assert messgeraet.betriebsart == "messen"
    freigaben = [a for n, a in messgeraet.aufrufe if n == "setze_messfreigabe"]
    assert freigaben == [(True,), (False,)]
    assert s.zustandsbild().eintraege[1].zustand == "fertig"


def test_messen_nicht_als_anfangsbetriebsart(tmp_path: Path) -> None:
    with pytest.raises(ValueError, match="MESSEN"):
        Sitzung(geraete_fabrik=Fabrik(Testuhr()), betriebsart=Betriebsart.MESSEN, build_info=GIT)


def test_voraussetzungen_einzeln(tmp_path: Path) -> None:
    s, _ = _sitzung(
        tmp_path,
        konfiguration=SimulatorKonfiguration(meldungen_unterdrueckt=False, fremde_messung=True),
    )
    s.setze_messdaten_wurzel(tmp_path / "fehlt")
    status = {v.name: v.erfuellt for v in s.messen_voraussetzungen()}
    assert status == {
        "verbindung": True,
        "geraet_gestoppt": False,
        "meldungen_unterdrueckt": False,
        "git_hash": True,
        "messdaten_wurzel": False,
        "trockenlauf": False,
    }
    with pytest.raises(ValueError) as fehler:
        s.setze_betriebsart(Betriebsart.MESSEN)
    assert "Suppress" in str(fehler.value) and "Messdaten-Wurzel" in str(fehler.value)


# --- U2-12 ----------------------------------------------------------------------------


def test_u2_12_zustandsbild_aendert_sich_mit_jedem_wechsel(tmp_path: Path) -> None:
    s, _ = _sitzung(tmp_path)
    m1 = Messung(name="M1", einstellungsdatei=_set(tmp_path))
    pp = Pausenpunkt(text="Umbau")
    s.einfuegen(0, m1)
    s.einfuegen(1, pp)
    s.hole_ereignisse()
    s.starte("lauf")
    s.verarbeite()
    s.bestaetige()
    s.verarbeite()

    ereignisse = s.hole_ereignisse()
    revisionen = [e.revision for e in ereignisse]
    assert revisionen == sorted(revisionen) and len(set(revisionen)) == len(revisionen)
    wechsel = [e for e in ereignisse if e.art in ("durchgang_zustand", "eintrag_zustand")]
    assert [(e.art, e.daten["nach"]) for e in wechsel] == [
        ("durchgang_zustand", "laeuft"),
        ("eintrag_zustand", "laeuft"),
        ("eintrag_zustand", "fertig"),
        ("eintrag_zustand", "erreicht"),
        ("durchgang_zustand", "wartet_auf_bestaetigung"),
        ("eintrag_zustand", "erledigt"),
        ("durchgang_zustand", "laeuft"),
        ("durchgang_zustand", "beendet"),
    ]
    vorher = None
    for e in wechsel:
        bild = e.bild
        assert bild is not None
        assert bild.revision == e.revision
        if e.art == "durchgang_zustand":
            assert bild.durchgang.value == e.daten["nach"]
        else:
            eintrag = next(x for x in bild.eintraege if str(x.id) == e.daten["eintrag_id"])
            assert eintrag.zustand == e.daten["nach"]
        assert bild != vorher
        vorher = bild
    ende = s.zustandsbild()
    assert ende.zusammenfassung == {"fertig": 1}
    assert ende.durchgangsordner is not None


def test_zustandsbild_felder_einer_messung(tmp_path: Path) -> None:
    s, _ = _sitzung(tmp_path)
    fehlt = Messung(name="Fehlt", einstellungsdatei=str(tmp_path / "weg.set"))
    m = Messung(
        name="M1",
        einstellungsdatei=_set(tmp_path),
        parameter={"mittelung.anzahl": 4},
        zeitlimit_s=30.0,
        notiz="n",
    )
    s.einfuegen(0, m)
    s.einfuegen(1, fehlt)
    bild = s.zustandsbild()
    assert not bild.eintraege[0].set_fehlt and bild.eintraege[1].set_fehlt
    assert bild.verbunden and bild.verbindung is not None
    s.starte("x")
    s.verarbeite()
    bild = s.zustandsbild()
    e = bild.eintraege[0]
    assert (e.nummer, e.versuch, e.zustand, e.parameter) == (
        1,
        1,
        "fertig",
        {"mittelung.anzahl": 4},
    )
    assert e.messdatei is not None and e.messdatei.endswith("01_M1.svd")
    assert e.zeit_start is not None and e.zeit_ende is not None
    assert bild.fehlerentscheidung_offen
    assert bild.fehler_eintrag_id == fehlt.id
    assert bild.fehlertext is not None and "fehlt" in bild.fehlertext
    assert bild.eintraege[1].fehlerart == "vorpruefung"
    assert "vorläufig" in bild.fehlerstrategie
    s.entscheide(Fehlerentscheidung.UEBERSPRINGEN)
    s.verarbeite()
    bild = s.zustandsbild()
    assert bild.eintraege[1].uebersprungen
    assert bild.zusammenfassung == {"fertig": 1, "fehler": 1, "uebersprungen": 1}


# --- Bearbeitung, Speichern, Laden ----------------------------------------------------


def test_bearbeitung_meldet_ereignisse_und_fehler_mit_grund(tmp_path: Path) -> None:
    s, _ = _sitzung(tmp_path)
    m = Messung(name="M1", einstellungsdatei=_set(tmp_path))
    s.einfuegen(0, m)
    s.bearbeiten(m.id, name="M1b")
    s.einfuegen(1, Pausenpunkt(text="p"))
    s.verschieben(m.id, 1)
    s.entfernen(m.id)
    arten = [e.text for e in s.hole_ereignisse() if e.art == "warteschlange"]
    assert arten == [
        "Eintrag eingefügt",
        "Eintrag geändert",
        "Eintrag eingefügt",
        "Eintrag verschoben",
        "Eintrag entfernt",
    ]
    with pytest.raises(IndexError):
        s.einfuegen(5, Pausenpunkt(text="q"))
    with pytest.raises(ValueError, match=r"mittelung\.anzahl"):
        s.einfuegen(
            0, Messung(name="x", einstellungsdatei="a.set", parameter={"mittelung.anzahl": 2})
        )


def test_speichern_und_laden(tmp_path: Path) -> None:
    s, _ = _sitzung(tmp_path)
    m = Messung(name="M1", einstellungsdatei=str(tmp_path / "anderswo.set"))
    s.einfuegen(0, m)
    datei = tmp_path / "q.warteschlange.json"
    s.speichere_warteschlange(datei)
    with pytest.raises(FileExistsError):
        s.speichere_warteschlange(datei)
    s.speichere_warteschlange(datei, ueberschreiben=True)
    s.entfernen(m.id)
    warnungen = s.lade_warteschlange(datei)
    assert warnungen and "anderswo.set" in warnungen[0]
    assert [e.id for e in s.warteschlange.eintraege()] == [m.id]


def test_befehle_pruefen_vorbedingungen(tmp_path: Path) -> None:
    s, _ = _sitzung(tmp_path)
    for befehl in (s.pausiere, s.setze_fort, s.brich_ab, s.bestaetige, s.quittiere):
        with pytest.raises(ValueError, match="nicht möglich"):
            befehl()
    with pytest.raises(ValueError):
        s.entscheide(Fehlerentscheidung.WIEDERHOLEN)
    s.einfuegen(0, Messung(name="M1", einstellungsdatei=_set(tmp_path)))
    s.starte("a")
    s.steuerung.schritt()
    with pytest.raises(ValueError, match="bereit"):
        s.starte("b")
    with pytest.raises(ValueError, match="nicht möglich"):
        s.setze_betriebsart(Betriebsart.TROCKENLAUF)
    with pytest.raises(ValueError):
        s.setze_messdaten_wurzel(tmp_path)
    with pytest.raises(ValueError):
        s.verbinde()
    with pytest.raises(ValueError):
        s.trenne()
    with pytest.raises(ValueError):
        s.lade_warteschlange(tmp_path / "x.warteschlange.json")
    s.pausiere()
    s.verarbeite()
    s.setze_fort()
    s.verarbeite()
    assert s.zustandsbild().ergebnis is DurchgangErgebnis.VOLLSTAENDIG


def test_start_vorbedingungen(tmp_path: Path) -> None:
    s, _ = _sitzung(tmp_path, betriebsart=Betriebsart.NUR_LESEN)
    with pytest.raises(ValueError, match="NUR_LESEN"):
        s.starte("x")
    s.trenne()
    s.verarbeite()
    with pytest.raises(ValueError, match="keine Verbindung"):
        s.starte("x")
    ohne = Sitzung(geraete_fabrik=Fabrik(Testuhr()), uhr=Testuhr(), build_info=GIT)
    ohne.verarbeite()
    ohne.verbinde()
    ohne.verarbeite()
    with pytest.raises(ValueError, match="Messdaten-Wurzel"):
        ohne.starte("x")
    assert ohne.zustandsbild().messdaten_wurzel is None


def test_abbrechen_und_entscheiden_ueber_sitzung(tmp_path: Path) -> None:
    s, _ = _sitzung(tmp_path, drehbuch=[StartFehler(vorgang=0)])
    s.einfuegen(0, Messung(name="M1", einstellungsdatei=_set(tmp_path)))
    s.starte("x")
    s.verarbeite()
    assert s.zustandsbild().fehlerentscheidung_offen
    s.brich_ab()
    s.verarbeite()
    assert s.zustandsbild().ergebnis is DurchgangErgebnis.ABGEBROCHEN


def test_trennen_in_geraet_unklar_und_neues_geraet(tmp_path: Path) -> None:
    from ldv_automation.geraet.simulator import Haenger

    s, fabrik = _sitzung(tmp_path, drehbuch=[Haenger(vorgang=0, stop_wirkt=False)])
    s.einfuegen(0, Messung(name="M1", einstellungsdatei=_set(tmp_path), zeitlimit_s=1.0))
    s.starte("x")
    s.verarbeite()
    assert s.zustandsbild().durchgang is DurchgangZustand.GERAET_UNKLAR
    s.setze_betriebsart(Betriebsart.SIMULATOR)  # neues Gerät, altes wird nicht angesprochen
    anzahl = len(fabrik.erzeugt[0].aufrufe)
    s.verarbeite()
    assert len(fabrik.erzeugt) == 2
    assert len(fabrik.erzeugt[0].aufrufe) == anzahl
    assert s.zustandsbild().ergebnis is DurchgangErgebnis.GERAET_UNKLAR


def test_trennen_in_geraet_unklar(tmp_path: Path) -> None:
    from ldv_automation.geraet.simulator import Haenger

    s, _ = _sitzung(tmp_path, drehbuch=[Haenger(vorgang=0, stop_wirkt=False)])
    s.einfuegen(0, Messung(name="M1", einstellungsdatei=_set(tmp_path), zeitlimit_s=1.0))
    s.starte("x")
    s.verarbeite()
    s.trenne()
    s.verarbeite()
    bild = s.zustandsbild()
    assert bild.durchgang is DurchgangZustand.BEENDET and not bild.verbunden


# --- Wächter und Threads --------------------------------------------------------------


def test_waechter_meldet_haengenden_aufruf_einmal(tmp_path: Path) -> None:
    uhr = Testuhr()
    fabrik = Fabrik(uhr, drehbuch=[HaengenderAufruf(vorgang=0, methode="lade_einstellungen")])
    wurzel = tmp_path / "daten"
    wurzel.mkdir()
    s = Sitzung(
        geraete_fabrik=fabrik,
        uhr=uhr,
        build_info=GIT,
        messdaten_wurzel=wurzel,
        aufruf_warnung_s=5.0,
    )
    s.verarbeite()
    s.verbinde()
    s.verarbeite()
    s.einfuegen(0, Messung(name="M1", einstellungsdatei=_set(tmp_path)))
    s.starte("x")
    s.steuerung.schritt()  # Start
    geraete_thread = threading.Thread(target=s.steuerung.schritt)  # blockiert im Laden
    geraete_thread.start()
    sim = fabrik.erzeugt[0]
    frist = time.monotonic() + 5.0
    while sim.haengender_aufruf_seit_s() is None and time.monotonic() < frist:
        time.sleep(0.005)
    s.hole_ereignisse()
    assert s.pruefe_waechter() is None  # noch unter der Grenze
    uhr.vorstellen(6.0)
    assert s.zustandsbild().waechter_s == pytest.approx(6.0, rel=1e-12)
    assert s.pruefe_waechter() == pytest.approx(6.0, rel=1e-12)
    assert s.pruefe_waechter() is not None
    meldungen = [e for e in s.hole_ereignisse() if e.art == "waechter"]
    assert len(meldungen) == 1 and "PSV reagiert nicht seit 6 s" in meldungen[0].text
    sim.haenger_loesen()
    geraete_thread.join(5.0)
    assert not geraete_thread.is_alive()
    assert s.pruefe_waechter() is None


def test_threads_starten_und_beenden(tmp_path: Path) -> None:
    from ldv_automation.ablauf.steuerung import AblaufKonfiguration
    from ldv_automation.ablauf.uhr import Echtzeituhr

    uhr = Echtzeituhr()

    def fabrik(art: Betriebsart) -> Messgeraet:
        return Simulator(
            uhr.monotonic,
            betriebsart=art.value,
            konfiguration=SimulatorKonfiguration(punkte_anzahl=2, punktdauer_s=0.01),
        )

    wurzel = tmp_path / "daten"
    wurzel.mkdir()
    s = Sitzung(
        geraete_fabrik=fabrik,
        uhr=uhr,
        build_info=GIT,
        messdaten_wurzel=wurzel,
        konfiguration=AblaufKonfiguration(poll_s=0.005),
    )
    s.starte_threads(waechter_takt_s=0.01)
    s.einfuegen(0, Messung(name="M1", einstellungsdatei=_set(tmp_path)))
    frist = time.monotonic() + 5.0
    while not s.zustandsbild().verbunden and time.monotonic() < frist:
        if s.steuerung.hat_geraet and s.zustandsbild().durchgang is DurchgangZustand.BEREIT:
            s.verbinde()
        time.sleep(0.02)
    s.starte("thread")
    while s.zustandsbild().durchgang is not DurchgangZustand.BEENDET and time.monotonic() < frist:
        time.sleep(0.01)
    assert s.beende_threads(timeout_s=5.0)
    assert s.zustandsbild().ergebnis is DurchgangErgebnis.VOLLSTAENDIG


def test_standardwerte_echtzeituhr_und_build_info(tmp_path: Path) -> None:
    s = Sitzung(geraete_fabrik=Fabrik(Testuhr()))
    bild = s.zustandsbild()
    assert bild.paket_version == "0.1.0"
    assert bild.betriebsart is Betriebsart.SIMULATOR
    assert bild.waechter_s is None  # Gerät noch nicht erzeugt
    assert s.beende_threads()
