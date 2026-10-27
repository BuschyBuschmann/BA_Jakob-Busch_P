"""Sitzung, Paket U5: Lücken B1 bis B8 (Simulator, Testuhr, ohne Oberfläche)."""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any

import pytest

from ldv_automation.ablauf.geraetestand import GeneratorStand
from ldv_automation.ablauf.steuerung import AblaufKonfiguration, DurchgangErgebnis
from ldv_automation.ablauf.uhr import Testuhr
from ldv_automation.domaene.eintraege import Messung, Pausenpunkt
from ldv_automation.geraet.schnittstelle import Messgeraet
from ldv_automation.geraet.simulator import (
    LadeFehler,
    LangsamerAufruf,
    Simulator,
    SimulatorKonfiguration,
)
from ldv_automation.protokoll.version import BuildInfo
from ldv_automation.sitzung import (
    ZIELORDNER_PLATZHALTER,
    Betriebsart,
    DurchgangZustand,
    Sitzung,
)

GIT = BuildInfo(paket_version="0.1.0", git_hash="c" * 40, git_dirty=False, quelle="test")


class Fabrik:
    def __init__(self, uhr: Testuhr, **sim: Any) -> None:
        self.uhr = uhr
        self.sim = sim
        self.erzeugt: list[Simulator] = []

    def __call__(self, art: Betriebsart) -> Messgeraet:
        geraet = Simulator(self.uhr.monotonic, betriebsart=art.value, **self.sim)
        self.erzeugt.append(geraet)
        return geraet


def _set(tmp_path: Path, name: str = "basis.set") -> str:
    pfad = tmp_path / name
    pfad.write_bytes(b"SET")
    return str(pfad)


def _sitzung(
    tmp_path: Path,
    *,
    ablauf: AblaufKonfiguration | None = None,
    verbinden: bool = True,
    **sim: Any,
) -> tuple[Sitzung, Fabrik, Path]:
    uhr = Testuhr()
    fabrik = Fabrik(uhr, **sim)
    wurzel = tmp_path / "messdaten"
    wurzel.mkdir()
    s = Sitzung(
        geraete_fabrik=fabrik,
        uhr=uhr,
        build_info=GIT,
        messdaten_wurzel=wurzel,
        konfiguration=ablauf,
    )
    s.verarbeite()
    if verbinden:
        s.verbinde()
        s.verarbeite()
    return s, fabrik, wurzel


def _trockenlauf(s: Sitzung) -> None:
    s.setze_betriebsart(Betriebsart.TROCKENLAUF)
    s.verarbeite()
    s.verbinde()
    s.verarbeite()
    s.starte("tl")
    s.verarbeite()


# --- B1 Startvorschau -----------------------------------------------------------------------


def test_b1_vorschau_vor_dem_laden_unbekannt_mit_zielpfad(tmp_path: Path) -> None:
    s, _f, wurzel = _sitzung(tmp_path)
    datei = _set(tmp_path)
    s.einfuegen(0, Messung(name="Platte oben", einstellungsdatei=datei))
    s.einfuegen(1, Pausenpunkt(text="Umbau"))
    s.einfuegen(2, Messung(name="Platte unten", einstellungsdatei=datei))
    v = s.zustandsbild().start_vorschau
    assert [x.nummer for x in v] == [1, 2]
    assert v[0].zielpfad == str(
        wurzel / f"{ZIELORDNER_PLATZHALTER}_simulator" / "01_Platte_oben.svd"
    )
    assert v[1].zielpfad is not None and v[1].zielpfad.endswith("02_Platte_unten.svd")
    assert v[0].messpunkte is None and v[0].generator is None
    assert not v[0].generator_unbedenklich
    assert "noch nicht geladen" in v[0].hinweis


def test_b1_vorschau_nach_trockenlauf_bekannt_und_veraltet_nach_aenderung(
    tmp_path: Path,
) -> None:
    s, _f, _w = _sitzung(tmp_path, konfiguration=SimulatorKonfiguration(punkte_anzahl=4))
    datei = _set(tmp_path)
    s.einfuegen(0, Messung(name="M1", einstellungsdatei=datei))
    _trockenlauf(s)
    s.zuruecksetzen()
    v = s.zustandsbild().start_vorschau[0]
    assert v.messpunkte == 4
    assert v.generator == GeneratorStand(
        generatoren_an=None, aktiv=False, amplitude_v=0.0, anzahl=None
    )
    assert v.generator_unbedenklich
    assert "gelesen nach Laden von" in v.hinweis
    # .set geändert (Größe und Zeit): Wissen gilt nicht mehr
    Path(datei).write_bytes(b"SET-GEAENDERT")
    st = os.stat(datei)
    os.utime(datei, ns=(st.st_atime_ns, st.st_mtime_ns + 10**9))
    v = s.zustandsbild().start_vorschau[0]
    assert v.messpunkte is None and v.generator is None
    assert "geändert" in v.hinweis


def test_b1_aktiver_generator_wird_gelesen_und_nicht_unbedenklich(tmp_path: Path) -> None:
    s, _f, _w = _sitzung(
        tmp_path,
        konfiguration=SimulatorKonfiguration(
            generator_aktiv=True, generator_amplitude_v=1.5, generatoren_an=True
        ),
    )
    stand = s.zustandsbild().geraete_stand
    assert stand is not None and stand.quelle == "beim Verbinden"
    assert stand.generator.aktiv is True and stand.generator.amplitude_v == 1.5
    assert not stand.generator.unbedenklich
    s.einfuegen(0, Messung(name="M1", einstellungsdatei=_set(tmp_path)))
    _trockenlauf(s)
    s.zuruecksetzen()
    v = s.zustandsbild().start_vorschau[0]
    assert v.generator is not None and v.generator.generatoren_an is True
    assert not v.generator_unbedenklich


def test_b1_nicht_lesbarer_generator_bleibt_unbekannt(tmp_path: Path) -> None:
    s, _f, _w = _sitzung(
        tmp_path,
        konfiguration=SimulatorKonfiguration(generator_aktiv=None, generator_amplitude_v=None),
    )
    stand = s.zustandsbild().geraete_stand
    assert stand is not None and stand.generator.aktiv is None
    assert not stand.generator.unbedenklich


def test_b1_kein_zielpfad_ohne_bildbaren_namen_und_ohne_ordner(tmp_path: Path) -> None:
    s, _f, _w = _sitzung(tmp_path)
    s.einfuegen(0, Messung(name="###", einstellungsdatei=_set(tmp_path)))
    v = s.zustandsbild().start_vorschau[0]
    assert v.zielpfad is None and "Zielpfad unbekannt" in v.hinweis
    ohne = Sitzung(geraete_fabrik=Fabrik(Testuhr()), uhr=Testuhr(), build_info=GIT)
    ohne.einfuegen(0, Messung(name="M", einstellungsdatei=_set(tmp_path, "b.set")))
    v = ohne.zustandsbild().start_vorschau[0]
    assert v.zielpfad is None and "kein Messdaten-Ordner" in v.hinweis


def test_b1_geraetestand_beim_verbinden_nicht_lesbar(tmp_path: Path) -> None:
    class OhneStand(Simulator):
        def lies_einstellungsstand(self) -> Any:
            from ldv_automation.geraet.schnittstelle import GeraeteFehler

            raise GeraeteFehler("nicht lesbar")

    uhr = Testuhr()
    wurzel = tmp_path / "m"
    wurzel.mkdir()
    s = Sitzung(
        geraete_fabrik=lambda art: OhneStand(uhr.monotonic, betriebsart=art.value),
        uhr=uhr,
        build_info=GIT,
        messdaten_wurzel=wurzel,
    )
    s.verbinde()
    s.verarbeite()
    bild = s.zustandsbild()
    assert bild.verbunden
    assert bild.geraete_stand is not None and bild.geraete_stand.fehler == "nicht lesbar"
    assert bild.geraete_stand.messpunkte is None
    assert any("Gerätestand beim Verbinden" in e.text for e in s.hole_ereignisse())


def test_b1_haenger_beim_lesen_des_geraetestands_verliert_das_geraet(tmp_path: Path) -> None:
    uhr = Testuhr()
    wurzel = tmp_path / "m"
    wurzel.mkdir()
    sims: list[Simulator] = []

    def fabrik(art: Betriebsart) -> Messgeraet:
        sim = Simulator(
            uhr.monotonic,
            betriebsart=art.value,
            drehbuch=[LangsamerAufruf(vorgang=-1, methode="lies_einstellungsstand", dauer_s=120.0)],
            schlafen=uhr.sleep,
        )
        sims.append(sim)
        return sim

    s = Sitzung(geraete_fabrik=fabrik, uhr=uhr, build_info=GIT, messdaten_wurzel=wurzel)
    s.verbinde()
    s.verarbeite()
    bild = s.zustandsbild()
    assert not bild.verbunden and bild.geraete_stand is None
    assert s.steuerung.momentaufnahme().geraet_verloren
    anzahl = len(sims[0].aufrufe)
    s.trenne()
    s.verarbeite()
    assert len(sims[0].aufrufe) == anzahl  # verlorenes Gerät wird nicht mehr angesprochen


def test_b1_trennen_loescht_den_geraetestand(tmp_path: Path) -> None:
    s, _f, _w = _sitzung(tmp_path)
    assert s.zustandsbild().geraete_stand is not None
    s.trenne()
    s.verarbeite()
    assert s.zustandsbild().geraete_stand is None


def test_b1_ladefehler_merkt_keinen_stand(tmp_path: Path) -> None:
    s, _f, _w = _sitzung(tmp_path, drehbuch=[LadeFehler(vorgang=0)])
    s.einfuegen(0, Messung(name="M1", einstellungsdatei=_set(tmp_path)))
    s.starte("x")
    s.verarbeite()
    assert s.zustandsbild().durchgang is DurchgangZustand.WARTET_AUF_ENTSCHEIDUNG
    assert s.steuerung.momentaufnahme().einstellungs_kenntnis == {}


# --- B2 Zusammenfassung nur des beendeten Durchgangs -----------------------------------------


def test_b2_zusammenfassung_zaehlt_nur_den_beendeten_durchgang(tmp_path: Path) -> None:
    s, _f, _w = _sitzung(tmp_path)
    datei = _set(tmp_path)
    s.einfuegen(0, Messung(name="A", einstellungsdatei=datei))
    s.einfuegen(1, Messung(name="B", einstellungsdatei=datei))
    s.starte("eins")
    s.verarbeite()
    assert s.zustandsbild().zusammenfassung == {"fertig": 2}
    s.einfuegen(2, Messung(name="C", einstellungsdatei=datei))
    s.einfuegen(3, Pausenpunkt(text="Halt"))
    s.einfuegen(4, Messung(name="D", einstellungsdatei=datei))
    s.starte("zwei")  # direkt aus BEENDET (B7)
    s.verarbeite()
    assert s.zustandsbild().durchgang is DurchgangZustand.WARTET_AUF_BESTAETIGUNG
    s.brich_ab()
    s.verarbeite()
    bild = s.zustandsbild()
    assert bild.ergebnis is DurchgangErgebnis.ABGEBROCHEN
    # A und B aus Durchgang 1 zählen nicht mit: C fertig, D nicht gestartet
    assert bild.zusammenfassung == {"fertig": 1, "wartend": 1}


# --- B3 Standard-Zeitlimit ------------------------------------------------------------------


def test_b3_standard_zeitlimit_setzen_und_wirken(tmp_path: Path) -> None:
    s, _f, _w = _sitzung(tmp_path)
    assert s.zustandsbild().standard_zeitlimit_s == 600.0
    s.setze_standard_zeitlimit(42)
    assert s.zustandsbild().standard_zeitlimit_s == 42.0
    s.einfuegen(0, Messung(name="M1", einstellungsdatei=_set(tmp_path)))
    s.einfuegen(1, Messung(name="M2", einstellungsdatei=_set(tmp_path), zeitlimit_s=7.0))
    s.starte("x")
    s.verarbeite()
    import json

    ordner = Path(s.zustandsbild().durchgangsordner or "")
    limits = sorted(
        json.loads(p.read_text(encoding="utf-8"))["zeitlimit_s"]
        for p in ordner.glob("*.protokoll.json")
    )
    assert limits == [7.0, 42.0]


@pytest.mark.parametrize("wert", [0, -1.0, float("nan"), float("inf"), True, "600"])
def test_b3_ungueltiges_zeitlimit(tmp_path: Path, wert: object) -> None:
    s, _f, _w = _sitzung(tmp_path)
    with pytest.raises(ValueError, match="Standard-Zeitlimit"):
        s.setze_standard_zeitlimit(wert)  # type: ignore[arg-type]
    assert s.zustandsbild().standard_zeitlimit_s == 600.0


def test_b3_zeitlimit_nur_in_ruhe(tmp_path: Path) -> None:
    s, _f, _w = _sitzung(tmp_path)
    s.einfuegen(0, Pausenpunkt(text="Halt"))
    s.starte("x")
    s.verarbeite()
    with pytest.raises(ValueError, match="nicht möglich"):
        s.setze_standard_zeitlimit(10.0)


# --- B4 Prüfung des Messdaten-Ordners -------------------------------------------------------


def test_b4_ungeeigneter_ordner_wird_abgelehnt_und_alter_bleibt(tmp_path: Path) -> None:
    s, _f, wurzel = _sitzung(tmp_path)
    with pytest.raises(ValueError, match="Ordner existiert nicht"):
        s.setze_messdaten_wurzel(tmp_path / "fehlt")
    repo = tmp_path / "repo"
    (repo / ".git").mkdir(parents=True)
    with pytest.raises(ValueError, match="Git-Repository"):
        s.setze_messdaten_wurzel(repo)
    bild = s.zustandsbild()
    assert bild.messdaten_wurzel == str(wurzel) and bild.messdaten_wurzel_probleme == ()
    # K-U5b: „Polytec“ tiefer im Pfad (z. B. Benutzerkonto) ist erlaubt
    polytec = tmp_path / "Polytec" / "daten"
    polytec.mkdir(parents=True)
    s.setze_messdaten_wurzel(polytec)
    assert s.zustandsbild().messdaten_wurzel == str(polytec)


def test_b4_ungeeigneter_ordner_beim_start_der_sitzung_sperrt_start(tmp_path: Path) -> None:
    uhr = Testuhr()
    s = Sitzung(
        geraete_fabrik=Fabrik(uhr),
        uhr=uhr,
        build_info=GIT,
        messdaten_wurzel=tmp_path / "fehlt",
    )
    s.verbinde()
    s.verarbeite()
    bild = s.zustandsbild()
    assert bild.messdaten_wurzel_probleme and "existiert nicht" in bild.messdaten_wurzel_probleme[0]
    wurzel_v = {v.name: v for v in bild.messen_voraussetzungen}["messdaten_wurzel"]
    assert not wurzel_v.erfuellt and "ungeeignet" in wurzel_v.text
    s.einfuegen(0, Messung(name="M", einstellungsdatei=_set(tmp_path)))
    with pytest.raises(ValueError, match="Messdaten-Ordner ungeeignet"):
        s.starte("x")
    # Mit einem geeigneten Ordner verschwindet die Meldung
    gut = tmp_path / "gut"
    gut.mkdir()
    s.setze_messdaten_wurzel(gut)
    assert s.zustandsbild().messdaten_wurzel_probleme == ()


def test_b4_eigene_ordnerpruefung_wird_benutzt(tmp_path: Path) -> None:
    gesehen: list[Path] = []

    def pruefung(p: Path) -> tuple[str, ...]:
        gesehen.append(p)
        return ("nein",)

    s = Sitzung(
        geraete_fabrik=Fabrik(Testuhr()),
        uhr=Testuhr(),
        build_info=GIT,
        messdaten_wurzel=tmp_path,
        ordner_pruefung=pruefung,
    )
    assert s.zustandsbild().messdaten_wurzel_probleme == ("nein",)
    with pytest.raises(ValueError, match="ungeeignet: nein"):
        s.setze_messdaten_wurzel(tmp_path)
    assert gesehen == [tmp_path, tmp_path]


# --- B5 Gerät übernimmt den neuen Ordner ----------------------------------------------------


def test_b5_neuer_ordner_erzeugt_geraet_neu_und_verbindet_wieder(tmp_path: Path) -> None:
    s, fabrik, wurzel = _sitzung(tmp_path)
    assert len(fabrik.erzeugt) == 1
    s.setze_messdaten_wurzel(wurzel)  # unverändert: kein Neuaufbau
    s.verarbeite()
    assert len(fabrik.erzeugt) == 1
    neu = tmp_path / "neu"
    neu.mkdir()
    s.setze_messdaten_wurzel(neu)
    s.verarbeite()
    assert len(fabrik.erzeugt) == 2
    assert fabrik.erzeugt[0].aufgerufene_methoden()[-1] == "trenne"
    assert s.zustandsbild().verbunden
    assert fabrik.erzeugt[1].aufgerufene_methoden()[0] == "verbinde"


def test_b5_ohne_verbindung_wird_nicht_verbunden(tmp_path: Path) -> None:
    s, fabrik, _w = _sitzung(tmp_path, verbinden=False)
    neu = tmp_path / "neu"
    neu.mkdir()
    s.setze_messdaten_wurzel(neu)
    s.verarbeite()
    assert len(fabrik.erzeugt) == 2
    assert not s.zustandsbild().verbunden
    assert fabrik.erzeugt[1].aufrufe == ()


# --- B7 Start aus BEENDET mit Schnappschuss -------------------------------------------------


def test_b7_start_aus_beendet_ohne_quittieren(tmp_path: Path) -> None:
    s, _f, _w = _sitzung(tmp_path)
    datei = _set(tmp_path)
    s.einfuegen(0, Messung(name="A", einstellungsdatei=datei))
    s.starte("eins")
    s.verarbeite()
    assert s.zustandsbild().durchgang is DurchgangZustand.BEENDET
    s.einfuegen(1, Messung(name="B", einstellungsdatei=datei))
    bild = s.zustandsbild()
    s.starte(
        "zwei",
        erwartete_betriebsart=bild.betriebsart,
        erwartete_kennung=bild.warteschlangen_kennung,
    )
    s.verarbeite()
    bild = s.zustandsbild()
    assert bild.durchgang is DurchgangZustand.BEENDET
    assert bild.durchgangsordner is not None and bild.durchgangsordner.endswith("_zwei")
    assert [e.zustand for e in bild.eintraege] == ["fertig", "fertig"]


def test_b7_schnappschuss_bindung(tmp_path: Path) -> None:
    s, _f, _w = _sitzung(tmp_path)
    datei = _set(tmp_path)
    s.einfuegen(0, Messung(name="A", einstellungsdatei=datei))
    alt = s.zustandsbild()
    s.bearbeiten(alt.eintraege[0].id, notiz="geändert")
    with pytest.raises(ValueError, match="Warteschlange oder Messdaten-Ordner"):
        s.starte("x", erwartete_kennung=alt.warteschlangen_kennung)
    with pytest.raises(ValueError, match="Betriebsart"):
        s.starte("x", erwartete_betriebsart=Betriebsart.TROCKENLAUF)
    assert s.zustandsbild().durchgang is DurchgangZustand.BEREIT
    # Ordnerwechsel ändert die Kennung (Zielpfade im Dialog)
    vorher = s.zustandsbild().warteschlangen_kennung
    neu = tmp_path / "neu"
    neu.mkdir()
    s.setze_messdaten_wurzel(neu)
    s.verarbeite()
    assert s.zustandsbild().warteschlangen_kennung != vorher


def test_b7_start_in_laufendem_durchgang_abgelehnt(tmp_path: Path) -> None:
    s, _f, _w = _sitzung(tmp_path)
    s.einfuegen(0, Pausenpunkt(text="Halt"))
    s.starte("x")
    s.verarbeite()
    with pytest.raises(ValueError, match="bereit oder beendet"):
        s.starte("y")


# --- B8 Einfügebereich ----------------------------------------------------------------------


def test_b8_einfuegebereich_aus_der_sitzung(tmp_path: Path) -> None:
    s, _f, _w = _sitzung(tmp_path)
    datei = _set(tmp_path)
    assert s.zustandsbild().einfuegen_ab == 0
    s.einfuegen(0, Messung(name="A", einstellungsdatei=datei))
    s.einfuegen(1, Pausenpunkt(text="Halt"))
    s.einfuegen(2, Messung(name="B", einstellungsdatei=datei))
    s.starte("x")
    s.verarbeite()
    assert s.zustandsbild().einfuegen_ab == 2  # A fertig, Pausenpunkt erreicht
    s.bestaetige()
    s.verarbeite()
    assert s.zustandsbild().einfuegen_ab == 3


# --- B6 öffentliche Namen -------------------------------------------------------------------


def test_b6_all_enthaelt_die_von_der_gui_genutzten_typen() -> None:
    import ldv_automation.sitzung as sitzung

    for name in (
        "Betriebsart",
        "DurchgangErgebnis",
        "DurchgangZustand",
        "EintragBild",
        "Fehlerentscheidung",
        "FortschrittStand",
        "GeneratorStand",
        "GeraeteDiagnose",
        "GeraeteInfo",
        "GeraeteStand",
        "SitzungsEreignis",
        "StartVorschau",
        "Voraussetzung",
        "Zustandsbild",
    ):
        assert name in sitzung.__all__
        assert hasattr(sitzung, name)


def test_diagnose_fehlt_beim_simulator(tmp_path: Path) -> None:
    s, _f, _w = _sitzung(tmp_path)
    assert s.zustandsbild().geraet_diagnose is None


def test_diagnose_fehler_verhindert_kein_zustandsbild(tmp_path: Path) -> None:
    class MitDiagnose(Simulator):
        def aufrufe_anzahl(self) -> int:
            raise RuntimeError("kaputt")

        def verweigerungen_text(self) -> tuple[str, ...]:
            return ()

    uhr = Testuhr()
    s = Sitzung(
        geraete_fabrik=lambda art: MitDiagnose(uhr.monotonic, betriebsart=art.value),
        uhr=uhr,
        build_info=GIT,
    )
    s.verarbeite()
    assert s.zustandsbild().geraet_diagnose is None


# --- Korrektur K-U5 ---------------------------------------------------------------------------


class ArtFabrik:
    """SIMULATOR: Standard-Simulator; jede andere Betriebsart: Simulator mit aktivem Generator."""

    def __init__(self, uhr: Testuhr) -> None:
        self.uhr = uhr
        self.erzeugt: list[Simulator] = []

    def __call__(self, art: Betriebsart) -> Messgeraet:
        konf = (
            SimulatorKonfiguration()
            if art is Betriebsart.SIMULATOR
            else SimulatorKonfiguration(generator_aktiv=True, generatoren_an=True)
        )
        sim = Simulator(self.uhr.monotonic, betriebsart=art.value, konfiguration=konf)
        self.erzeugt.append(sim)
        return sim


def _art_sitzung(tmp_path: Path) -> tuple[Sitzung, ArtFabrik]:
    uhr = Testuhr()
    fabrik = ArtFabrik(uhr)
    wurzel = tmp_path / "messdaten"
    wurzel.mkdir()
    s = Sitzung(geraete_fabrik=fabrik, uhr=uhr, build_info=GIT, messdaten_wurzel=wurzel)
    s.verbinde()
    s.verarbeite()
    return s, fabrik


def _wechsle(s: Sitzung, art: Betriebsart) -> None:
    s.setze_betriebsart(art)
    s.verarbeite()
    s.verbinde()
    s.verarbeite()


def test_k_u5_blocker_beleg_1_simulatorwissen_gilt_nicht_nach_geraetewechsel(
    tmp_path: Path,
) -> None:
    s, _f = _art_sitzung(tmp_path)
    s.einfuegen(0, Messung(name="A", einstellungsdatei=_set(tmp_path, "a.set")))
    s.starte("sim")
    s.verarbeite()
    s.zuruecksetzen()
    assert s.zustandsbild().start_vorschau[0].generator_unbedenklich  # im Simulator gelesen
    _wechsle(s, Betriebsart.TROCKENLAUF)
    bild = s.zustandsbild()
    assert bild.geraete_stand is not None and bild.geraete_stand.generator.aktiv is True
    v = bild.start_vorschau[0]
    assert v.generator is None and not v.generator_unbedenklich
    assert "aktuell verbundenen Gerät noch nicht geladen" in v.hinweis


def test_k_u5_blocker_beleg_2_messen_uebernimmt_kein_wissen(tmp_path: Path) -> None:
    s, _f = _art_sitzung(tmp_path)
    s.einfuegen(0, Messung(name="A", einstellungsdatei=_set(tmp_path, "a.set")))
    s.einfuegen(1, Pausenpunkt(text="Halt"))
    s.einfuegen(2, Messung(name="B", einstellungsdatei=_set(tmp_path, "b.set")))
    s.starte("sim")
    s.verarbeite()
    s.bestaetige()
    s.verarbeite()
    s.zuruecksetzen()
    _wechsle(s, Betriebsart.TROCKENLAUF)
    s.starte("tl")
    s.verarbeite()
    assert s.zustandsbild().durchgang is DurchgangZustand.WARTET_AUF_BESTAETIGUNG
    s.brich_ab()
    s.verarbeite()
    s.zuruecksetzen()
    a, b = s.zustandsbild().start_vorschau
    assert a.generator is not None and a.generator.aktiv is True  # im Trockenlauf gelesen
    assert b.generator is None  # B nie mit diesem Gerät geladen; Simulatorwert gilt nicht
    _wechsle(s, Betriebsart.MESSEN)
    assert s.zustandsbild().betriebsart is Betriebsart.MESSEN
    for v in s.zustandsbild().start_vorschau:
        assert v.generator is None and not v.generator_unbedenklich


def test_k_u5_trennen_verwirft_wissen(tmp_path: Path) -> None:
    s, _f, _w = _sitzung(tmp_path)
    s.einfuegen(0, Messung(name="A", einstellungsdatei=_set(tmp_path)))
    s.starte("x")
    s.verarbeite()
    s.zuruecksetzen()
    assert s.zustandsbild().start_vorschau[0].messpunkte == 9
    s.trenne()
    s.verarbeite()
    assert s.steuerung.momentaufnahme().einstellungs_kenntnis == {}
    s.verbinde()
    s.verarbeite()
    assert s.zustandsbild().start_vorschau[0].messpunkte is None


def test_k_u5_major_2_start_mit_veralteter_betriebsart_wird_verworfen(tmp_path: Path) -> None:
    s, fabrik, _w = _sitzung(tmp_path)
    s.einfuegen(0, Messung(name="A", einstellungsdatei=_set(tmp_path)))
    _trockenlauf(s)
    s.zuruecksetzen()
    s.setze_betriebsart(Betriebsart.SIMULATOR)
    s.verarbeite()
    s.verbinde()
    s.verarbeite()
    bild = s.zustandsbild()
    assert bild.betriebsart is Betriebsart.SIMULATOR and bild.verbunden
    s.hole_ereignisse()
    s.setze_betriebsart(Betriebsart.MESSEN)
    s.verbinde()
    s.starte(
        "x",
        erwartete_betriebsart=Betriebsart.SIMULATOR,
        erwartete_kennung=bild.warteschlangen_kennung,
    )
    s.verarbeite()
    messen = fabrik.erzeugt[-1]
    assert messen.betriebsart == "messen"
    assert "starte_scan" not in messen.aufgerufene_methoden()
    assert "setze_messfreigabe" not in messen.aufgerufene_methoden()
    assert s.zustandsbild().durchgang is DurchgangZustand.BEREIT
    assert any(
        e.art == "befehl_verworfen" and "aktives Gerät ist messen" in e.text
        for e in s.hole_ereignisse()
    )


def test_k_u5_major_2_messen_ohne_bestaetigung_im_geraete_thread_verworfen(
    tmp_path: Path,
) -> None:
    from ldv_automation.ablauf.steuerung import DurchgangsAuftrag

    s, fabrik, wurzel = _sitzung(tmp_path)
    s.einfuegen(0, Messung(name="A", einstellungsdatei=_set(tmp_path)))
    _trockenlauf(s)
    s.zuruecksetzen()
    s.quittiere()
    s.setze_betriebsart(Betriebsart.MESSEN)
    s.verarbeite()
    s.verbinde()
    s.verarbeite()
    assert s.zustandsbild().durchgang is DurchgangZustand.BEREIT
    s.hole_ereignisse()
    s.steuerung.starte(
        DurchgangsAuftrag(
            name="x",
            messdaten_wurzel=wurzel,
            betriebsart="messen",
            trockenlauf=False,
            messfreigabe=True,
        )
    )
    s.verarbeite()
    assert "starte_scan" not in fabrik.erzeugt[-1].aufgerufene_methoden()
    assert s.zustandsbild().durchgang is DurchgangZustand.BEREIT
    assert any("ohne ausdrückliche Bestätigung" in e.text for e in s.hole_ereignisse())


# --- K-U5b Punkt 3: Einstellungen gemeinsam oder gar nicht ------------------------------------


def test_k_u5b_einstellungen_beides_oder_nichts(tmp_path: Path) -> None:
    from ldv_automation.sitzung import EinstellungsFehler

    s, fabrik, wurzel = _sitzung(tmp_path)
    neu = tmp_path / "neu"
    neu.mkdir()
    # ungültiges Zeitlimit: Ordner bleibt, kein Geräteneubau
    with pytest.raises(EinstellungsFehler) as fehler:
        s.setze_einstellungen(neu, 0.0)
    assert fehler.value.ordner is None and "Standard-Zeitlimit" in str(fehler.value.zeitlimit)
    s.verarbeite()
    bild = s.zustandsbild()
    assert bild.messdaten_wurzel == str(wurzel) and bild.standard_zeitlimit_s == 600.0
    assert len(fabrik.erzeugt) == 1
    # ungültiger Ordner: Zeitlimit bleibt
    with pytest.raises(EinstellungsFehler) as fehler:
        s.setze_einstellungen(tmp_path / "fehlt", 30.0)
    assert fehler.value.zeitlimit is None and "existiert nicht" in str(fehler.value.ordner)
    assert s.zustandsbild().standard_zeitlimit_s == 600.0
    # beides ungültig: beide Texte
    with pytest.raises(EinstellungsFehler) as fehler:
        s.setze_einstellungen(tmp_path / "fehlt", float("nan"))
    assert fehler.value.ordner and fehler.value.zeitlimit
    # beides gültig: beides gesetzt, Gerät neu
    s.setze_einstellungen(neu, 30.0)
    s.verarbeite()
    bild = s.zustandsbild()
    assert bild.messdaten_wurzel == str(neu) and bild.standard_zeitlimit_s == 30.0
    assert len(fabrik.erzeugt) == 2


def test_k_u5b_einstellungen_nur_in_ruhe(tmp_path: Path) -> None:
    s, _f, wurzel = _sitzung(tmp_path)
    s.einfuegen(0, Pausenpunkt(text="Halt"))
    s.starte("x")
    s.verarbeite()
    with pytest.raises(ValueError, match="nicht möglich"):
        s.setze_einstellungen(wurzel, 30.0)
