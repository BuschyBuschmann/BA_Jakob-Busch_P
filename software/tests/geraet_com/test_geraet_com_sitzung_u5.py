"""Abgleich Sitzung <-> COM-Adapter gegen den COM-Fake (U5; Prüfung T1 in NUR_LESEN)."""

from __future__ import annotations

import json
import os
from pathlib import Path

from fake_psv_com import FakeBindung, Welt, baue_psv

from ldv_automation.ablauf.uhr import Testuhr
from ldv_automation.domaene.eintraege import Messung
from ldv_automation.geraet.com.adapter import ComBetriebsart, ComKonfiguration, PsvComGeraet
from ldv_automation.geraet.com.konstanten import SettingsMask
from ldv_automation.geraet.com.richtlinie import STANDARD_LADEMASKE
from ldv_automation.geraet.schnittstelle import Messgeraet
from ldv_automation.geraet.simulator import Simulator
from ldv_automation.protokoll.version import BuildInfo
from ldv_automation.sitzung import Betriebsart, Sitzung

GIT = BuildInfo(paket_version="0.1.0", git_hash="c" * 40, git_dirty=False, quelle="test")


class ComFabrik:
    """Wie die Fabrik im Einstieg, aber mit Fake-Bindung; merkt sich die Adapter."""

    def __init__(self, sitzung_wurzel: list[Sitzung]) -> None:
        self.welt = Welt()
        self.erzeugt: list[PsvComGeraet] = []
        self._halter = sitzung_wurzel

    def __call__(self, art: Betriebsart) -> Messgeraet:
        wurzel = self._halter[0].zustandsbild().messdaten_wurzel if self._halter else None
        geraet = PsvComGeraet(
            FakeBindung(baue_psv(self.welt)),
            ComKonfiguration(
                betriebsart=ComBetriebsart[art.name],
                messdaten_wurzel=wurzel,
                existiert=lambda p: p in self.welt.dateien,
            ),
        )
        self.erzeugt.append(geraet)
        return geraet


def _sitzung(tmp_path: Path) -> tuple[Sitzung, ComFabrik]:
    halter: list[Sitzung] = []
    fabrik = ComFabrik(halter)
    wurzel = tmp_path / "messdaten"
    wurzel.mkdir()
    s = Sitzung(
        geraete_fabrik=fabrik,
        betriebsart=Betriebsart.NUR_LESEN,
        uhr=Testuhr(),
        build_info=GIT,
        messdaten_wurzel=wurzel,
    )
    halter.append(s)
    s.verarbeite()
    return s, fabrik


def test_t1_nur_lesen_aufrufprotokoll_ohne_verweigerung(tmp_path: Path) -> None:
    s, fabrik = _sitzung(tmp_path)
    s.verbinde()
    s.verarbeite()
    bild = s.zustandsbild()
    assert bild.verbunden and bild.betriebsart is Betriebsart.NUR_LESEN
    diagnose = bild.geraet_diagnose
    assert diagnose is not None
    assert diagnose.verweigerungen == ()
    assert diagnose.aufrufe_anzahl == len(fabrik.erzeugt[0].aufrufe()) > 0
    # Lademaske und Prozessprüfung kommen im Zustandsbild (Gerät-Dialog, Protokoll) an
    assert bild.verbindung is not None
    assert bild.verbindung.lademaske
    assert bild.verbindung.hardware["psv_prozesse"] == "PSV.exe"
    # Gerätestand nur lesend: Messpunkte und Generator aus dem Fake
    stand = bild.geraete_stand
    assert stand is not None and stand.fehler is None
    assert stand.messpunkte == 9
    assert stand.generator.generatoren_an is False and stand.generator.aktiv is False
    assert stand.generator.amplitude_v == 0.5 and stand.generator.unbedenklich
    # keine schreibenden COM-Zugriffe
    assert not [a for a in fabrik.erzeugt[0].aufrufe() if a.op == "set"]


def test_verweigerung_wird_im_zustandsbild_sichtbar(tmp_path: Path) -> None:
    s, fabrik = _sitzung(tmp_path)
    s.verbinde()
    s.verarbeite()
    adapter = fabrik.erzeugt[0]
    adapter._kontext.protokolliere_verweigerung("Acquisition.Mode", "set", "Default deny")
    diagnose = s.zustandsbild().geraet_diagnose
    assert diagnose is not None
    assert diagnose.verweigerungen == ("Acquisition.Mode (set): Default deny",)
    assert adapter.verweigerungen_text() == diagnose.verweigerungen


def test_b5_adapter_uebernimmt_neuen_messdaten_ordner(tmp_path: Path) -> None:
    s, fabrik = _sitzung(tmp_path)
    s.verbinde()
    s.verarbeite()
    neu = tmp_path / "neu"
    neu.mkdir()
    s.setze_messdaten_wurzel(neu)
    s.verarbeite()
    assert len(fabrik.erzeugt) == 2
    assert fabrik.erzeugt[-1]._konf.messdaten_wurzel == str(neu)
    assert s.zustandsbild().verbunden


# --- K-U5b: Übernahme gelesenen Wissens TROCKENLAUF -> MESSEN --------------------------------


class VarFabrik:
    """COM-Fake je Betriebsart; Prozess-Treffer und Lademaske je Betriebsart einstellbar."""

    def __init__(self, halter: list[Sitzung], uhr: Testuhr) -> None:
        self.welt = Welt()
        self.halter = halter
        self.uhr = uhr
        self.prozess: dict[Betriebsart, tuple[str, ...]] = {}
        self.lademaske: dict[Betriebsart, int] = {}
        self.erzeugt: list[Messgeraet] = []

    def __call__(self, art: Betriebsart) -> Messgeraet:
        if art is Betriebsart.SIMULATOR:
            geraet: Messgeraet = Simulator(self.uhr.monotonic, betriebsart="simulator")
        else:
            wurzel = self.halter[0].zustandsbild().messdaten_wurzel if self.halter else None
            geraet = PsvComGeraet(
                FakeBindung(baue_psv(self.welt), prozess=self.prozess.get(art, ("PSV.exe",))),
                ComKonfiguration(
                    betriebsart=ComBetriebsart[art.name],
                    messdaten_wurzel=wurzel,
                    lademaske=self.lademaske.get(art, STANDARD_LADEMASKE),
                    existiert=os.path.lexists,
                ),
            )
        self.erzeugt.append(geraet)
        return geraet


def _trockenlauf_com(
    tmp_path: Path, anfang: Betriebsart = Betriebsart.TROCKENLAUF
) -> tuple[Sitzung, VarFabrik, Path]:
    halter: list[Sitzung] = []
    uhr = Testuhr()
    fabrik = VarFabrik(halter, uhr)
    wurzel = tmp_path / "messdaten"
    wurzel.mkdir()
    s = Sitzung(
        geraete_fabrik=fabrik, betriebsart=anfang, uhr=uhr, build_info=GIT, messdaten_wurzel=wurzel
    )
    halter.append(s)
    datei = tmp_path / "platte.set"
    datei.write_bytes(b"SET")
    s.verbinde()
    s.verarbeite()
    s.einfuegen(0, Messung(name="A", einstellungsdatei=str(datei)))
    s.starte("lauf")
    s.verarbeite()
    s.zuruecksetzen()
    return s, fabrik, datei


def _nach(s: Sitzung, art: Betriebsart) -> None:
    s.setze_betriebsart(art)
    s.verarbeite()
    s.verbinde()
    s.verarbeite()


def test_k_u5b_uebernahme_trockenlauf_nach_messen_bei_gleichheit(tmp_path: Path) -> None:
    s, _f, _d = _trockenlauf_com(tmp_path)
    v = s.zustandsbild().start_vorschau[0]
    assert v.messpunkte == 9 and v.generator_unbedenklich and not v.uebernommen
    _nach(s, Betriebsart.MESSEN)
    bild = s.zustandsbild()
    assert bild.betriebsart is Betriebsart.MESSEN
    v = bild.start_vorschau[0]
    assert v.uebernommen and v.messpunkte == 9 and v.generator_unbedenklich
    assert "gelesen in Betriebsart TROCKENLAUF vom" in v.hinweis and "übernommen" in v.hinweis
    # Herkunft steht im Ereignisprotokoll des Durchgangs (Startangaben)
    s.starte(
        "messen",
        messen_bestaetigt=True,
        erwartete_betriebsart=Betriebsart.MESSEN,
        erwartete_kennung=bild.warteschlangen_kennung,
    )
    s.verarbeite(max_schritte=200)
    ordner = Path(s.zustandsbild().durchgangsordner or "")
    erste = json.loads(
        (ordner / "durchgang.ereignisse.jsonl").read_text(encoding="utf-8").splitlines()[0]
    )
    assert erste["art"] == "durchgang_start"
    assert erste["startangaben"][0]["uebernommen"] is True
    assert "TROCKENLAUF" in erste["startangaben"][0]["hinweis"]


def test_k_u5b_verfall_bei_geaenderter_set(tmp_path: Path) -> None:
    s, _f, datei = _trockenlauf_com(tmp_path)
    datei.write_bytes(b"SET-NEU")
    st = os.stat(datei)
    os.utime(datei, ns=(st.st_atime_ns, st.st_mtime_ns + 10**9))
    _nach(s, Betriebsart.MESSEN)
    v = s.zustandsbild().start_vorschau[0]
    assert v.generator is None and not v.uebernommen and "geändert" in v.hinweis


def test_k_u5b_verfall_bei_anderer_lademaske(tmp_path: Path) -> None:
    s, fabrik, _d = _trockenlauf_com(tmp_path)
    fabrik.lademaske[Betriebsart.MESSEN] = int(SettingsMask.ACQUISITION)
    _nach(s, Betriebsart.MESSEN)
    v = s.zustandsbild().start_vorschau[0]
    assert v.generator is None and not v.generator_unbedenklich


def test_k_u5b_verfall_bei_anderem_prozess(tmp_path: Path) -> None:
    s, fabrik, _d = _trockenlauf_com(tmp_path)
    fabrik.prozess[Betriebsart.MESSEN] = ("PSV.exe", "PSV-Zweitinstanz.exe")
    _nach(s, Betriebsart.MESSEN)
    assert s.zustandsbild().start_vorschau[0].generator is None


def test_k_u5b_simulator_nach_com_nie_uebernommen(tmp_path: Path) -> None:
    s, _f, _d = _trockenlauf_com(tmp_path, anfang=Betriebsart.SIMULATOR)
    assert s.zustandsbild().start_vorschau[0].generator_unbedenklich  # im Simulator gelesen
    _nach(s, Betriebsart.TROCKENLAUF)
    v = s.zustandsbild().start_vorschau[0]
    assert v.generator is None and not v.uebernommen


def test_k_u5b_trennen_verwirft_auch_com_wissen(tmp_path: Path) -> None:
    s, _f, _d = _trockenlauf_com(tmp_path)
    s.trenne()
    s.verarbeite()
    s.verbinde()
    s.verarbeite()
    _nach(s, Betriebsart.MESSEN)
    assert s.zustandsbild().start_vorschau[0].generator is None
