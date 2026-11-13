"""Steuerung und Abgleichstatus (R-003a/b, Plan P-R003 Schritt 5, A1-A8).

Simulator mit Drehbuch; alle Zahlen sind erfundene Testwerte, keine Gerätewerte.
"""

from __future__ import annotations

from pathlib import Path

import pytest
from ablauf_hilfen import Aufbau, aufbau, messung

from ldv_automation.ablauf.abgleich import AbgleichModus, AbgleichRegel
from ldv_automation.ablauf.steuerung import (
    AblaufKonfiguration,
    DurchgangErgebnis,
    DurchgangZustand,
)
from ldv_automation.domaene.eintraege import MessungZustand
from ldv_automation.geraet.schnittstelle import Abgleich2D, Abgleich3D, AbgleichStand
from ldv_automation.geraet.simulator import (
    AbgleichBeiLaden,
    AbgleichNichtLesbar,
    HaengenderAufruf,
    LadeFehler,
    LangsamerAufruf,
    Simulator,
    SimulatorKonfiguration,
)

SCHLECHT = AbgleichStand(
    abgleich_3d=(Abgleich3D(index=0, gueltig=False, qualitaet_ist_m=0.5),), anzahl_3d=1
)
GUT = AbgleichStand(
    abgleich_3d=(Abgleich3D(index=0, gueltig=True, qualitaet_ist_m=0.5),),
    abgleich_2d=(Abgleich2D(index=0, gueltig=True, scankopfabstand_m=1.0),),
    anzahl_3d=1,
    anzahl_2d=1,
)


class OhneLeser:
    """Gerät ohne ``lies_abgleich``: reicht alles andere an den Simulator durch."""

    def __init__(self, sim: Simulator) -> None:
        self._sim = sim

    def __getattr__(self, name: str) -> object:
        if name == "lies_abgleich":
            raise AttributeError(name)
        return getattr(self._sim, name)


def _unter(tmp_path: Path, name: str) -> Path:
    ordner = tmp_path / name
    ordner.mkdir()
    return ordner


def _konf(modus: AbgleichModus, **kw: object) -> AblaufKonfiguration:
    return AblaufKonfiguration(abgleich=AbgleichRegel(modus=modus, **kw))  # type: ignore[arg-type]


def _abgleich(a: Aufbau, basis: str = "01_M1") -> dict[str, object]:
    feld = a.protokoll(basis)["abgleich"]
    assert isinstance(feld, dict)
    return feld


def _pruefung(a: Aufbau, basis: str = "01_M1") -> dict[str, object]:
    pruefung = _abgleich(a, basis)["pruefung"]
    assert isinstance(pruefung, dict)
    return pruefung


def _art(a: Aufbau, art: str) -> list[str]:
    return [e.text for e in a.ereignisse if e.art == art]


def _fehlerart(a: Aufbau, basis: str = "01_M1") -> str:
    fehler = a.protokoll(basis)["fehler"]
    assert isinstance(fehler, dict)
    return str(fehler["art"])


def _lauf(a: Aufbau, **auftrag: bool) -> None:
    a.starte(**auftrag)
    a.steuerung.bis_ruhe()


def test_aufrufreihenfolge_lies_abgleich_nach_dem_einstellungsstand(tmp_path: Path) -> None:
    a = aufbau(tmp_path, [messung(tmp_path, "M1", {"fft.linien": 1600})])
    _lauf(a)
    methoden = list(a.sim.aufgerufene_methoden())
    i = methoden.index("lies_abgleich")
    assert methoden[i - 1] == "lies_einstellungsstand"
    assert methoden.index("lade_einstellungen") < methoden.index("setze_parameter") < i
    assert methoden[i + 1] == "starte_scan" and methoden.count("lies_abgleich") == 1


def test_a1_a2_protokoll_traegt_den_abgleich(tmp_path: Path) -> None:
    stand = AbgleichStand(
        abgleich_3d=(
            Abgleich3D(
                index=0,
                gueltig=True,
                qualitaet_ist_m=0.5,
                qualitaet_soll_m=1.5,
                positionsunsicherheit_m=0.25,
                winkelunsicherheit_rad=0.125,
            ),
        ),
        abgleich_2d=(Abgleich2D(index=0, gueltig=True, scankopfabstand_m=2.0),),
        anzahl_3d=1,
        anzahl_2d=1,
    )
    a = aufbau(
        tmp_path,
        [messung(tmp_path, "M1")],
        sim_konfiguration=SimulatorKonfiguration(abgleich=stand),
    )
    _lauf(a)
    feld = _abgleich(a)
    assert feld["gelesen"] is True and feld["grund"] is None
    assert feld["zeit"] is not None and feld["nicht_lesbar"] == {}
    assert feld["abgleich_3d"] == [
        {
            "index": 0,
            "gueltig": True,
            "qualitaet_ist_m": 0.5,
            "qualitaet_soll_m": 1.5,
            "positionsunsicherheit_m": 0.25,
            "winkelunsicherheit_rad": 0.125,
            "nicht_lesbar": {},
        }
    ]
    assert feld["abgleich_2d"] == [
        {"index": 0, "gueltig": True, "scankopfabstand_m": 2.0, "nicht_lesbar": {}}
    ]
    assert _pruefung(a) == {
        "modus": "aus",
        "ergebnis": "nicht_geprueft",
        "grenzen": {
            "qualitaet_max_m": None,
            "position_max_m": None,
            "winkel_max_rad": None,
            "pruefe_2d": False,
        },
        "befunde": [],
    }


def test_a4_modus_aus_blockiert_nie_und_aendert_den_ablauf_nicht(tmp_path: Path) -> None:
    """Invariante: Aufrufverlauf = Bestandsverlauf (ohne Leser) plus ``lies_abgleich``."""
    sim_schlecht = SimulatorKonfiguration(abgleich=SCHLECHT)
    oa, ob = _unter(tmp_path, "a"), _unter(tmp_path, "b")
    a = aufbau(oa, [messung(oa, "M1")], sim_konfiguration=sim_schlecht)
    _lauf(a)
    assert a.steuerung.momentaufnahme().ergebnis is DurchgangErgebnis.VOLLSTAENDIG
    assert a.protokoll("01_M1")["status"] == "fertig"
    assert "starte_scan" in a.sim.aufgerufene_methoden()
    assert _pruefung(a)["ergebnis"] == "nicht_geprueft"

    b = aufbau(ob, [messung(ob, "M1")], huelle=OhneLeser)  # type: ignore[arg-type]
    _lauf(b)
    ohne = [(n, x) for n, x in b.sim.aufrufe]
    mit = [(n, x) for n, x in a.sim.aufrufe if n != "lies_abgleich"]
    assert [n for n, _ in mit] == [n for n, _ in ohne]


def test_modus_aus_meldet_auffaelligkeit_als_hinweis(tmp_path: Path) -> None:
    a = aufbau(
        tmp_path,
        [messung(tmp_path, "M1")],
        sim_konfiguration=SimulatorKonfiguration(abgleich=SCHLECHT),
    )
    _lauf(a)
    (hinweis,) = _art(a, "abgleich_hinweis")
    assert "3D-Abgleich 0: Valid = False" in hinweis
    assert _art(a, "abgleich_warnung") == []
    zeilen = [z for z in a.ereignisprotokoll() if z["art"] == "abgleich_hinweis"]
    assert len(zeilen) == 1


def test_gueltiger_abgleich_erzeugt_keine_ereignisse(tmp_path: Path) -> None:
    a = aufbau(tmp_path, [messung(tmp_path, "M1")])
    _lauf(a)
    assert _art(a, "abgleich_hinweis") == [] and _art(a, "abgleich_warnung") == []


def test_a5_verweigern_ungueltiger_abgleich_startet_keinen_scan(tmp_path: Path) -> None:
    a = aufbau(
        tmp_path,
        [messung(tmp_path, "M1")],
        sim_konfiguration=SimulatorKonfiguration(abgleich=SCHLECHT),
        konfiguration=_konf(AbgleichModus.VERWEIGERN),
    )
    _lauf(a)
    assert "starte_scan" not in a.sim.aufgerufene_methoden()
    assert a.steuerung.zustand is DurchgangZustand.WARTET_AUF_ENTSCHEIDUNG
    assert a.protokoll("01_M1")["status"] == "fehler"
    assert _fehlerart(a) == "abgleich"
    fehler = a.protokoll("01_M1")["fehler"]
    assert isinstance(fehler, dict)
    assert "Abgleich nicht_bestanden" in str(fehler["text"])
    assert "3D-Abgleich 0: ungültig (Valid = False)" in str(fehler["text"])
    feld = _abgleich(a)
    assert feld["gelesen"] is True and _pruefung(a)["ergebnis"] == "nicht_bestanden"
    assert _pruefung(a)["befunde"] == ["3D-Abgleich 0: ungültig (Valid = False)"]
    assert a.ws.eintraege()[0].zustand is MessungZustand.FEHLER
    ereignis = [e for e in a.ereignisse if e.art == "fehler"]
    assert ereignis and ereignis[0].daten["art_fehler"] == "abgleich"


def test_a5_verweigern_grenze_ueberschritten_und_grenzfall(tmp_path: Path) -> None:
    def stand(q: float) -> AbgleichStand:
        return AbgleichStand(
            abgleich_3d=(Abgleich3D(index=0, gueltig=True, qualitaet_ist_m=q),), anzahl_3d=1
        )

    for q, erwartet in ((2.0, "fertig"), (2.0000000000000004, "fehler")):
        o = _unter(tmp_path, erwartet)
        a = aufbau(
            o,
            [messung(o, "M1")],
            sim_konfiguration=SimulatorKonfiguration(abgleich=stand(q)),
            konfiguration=_konf(AbgleichModus.VERWEIGERN, qualitaet_max_m=2.0),
        )
        _lauf(a)
        assert a.protokoll("01_M1")["status"] == erwartet
        grenzen = _pruefung(a)["grenzen"]
        assert isinstance(grenzen, dict) and grenzen["qualitaet_max_m"] == 2.0  # A6
    assert "über Grenze" in str(a.protokoll("01_M1")["fehler"])


def test_a5_verweigern_nicht_pruefbar_bei_gesetzter_grenze(tmp_path: Path) -> None:
    stand = AbgleichStand(abgleich_3d=(Abgleich3D(index=0, gueltig=True),), anzahl_3d=1)
    a = aufbau(
        tmp_path,
        [messung(tmp_path, "M1")],
        sim_konfiguration=SimulatorKonfiguration(abgleich=stand),
        konfiguration=_konf(AbgleichModus.VERWEIGERN, position_max_m=1.0),
    )
    _lauf(a)
    assert _fehlerart(a) == "abgleich" and _pruefung(a)["ergebnis"] == "nicht_pruefbar"


def test_verweigern_ohne_grenze_blockiert_nicht_bei_fehlendem_wert(tmp_path: Path) -> None:
    stand = AbgleichStand(abgleich_3d=(Abgleich3D(index=0, gueltig=True),), anzahl_3d=1)
    a = aufbau(
        tmp_path,
        [messung(tmp_path, "M1")],
        sim_konfiguration=SimulatorKonfiguration(abgleich=stand),
        konfiguration=_konf(AbgleichModus.VERWEIGERN),
    )
    _lauf(a)
    assert a.protokoll("01_M1")["status"] == "fertig"
    assert _pruefung(a)["ergebnis"] == "bestanden"


def test_verweigern_2d_nur_mit_schalter(tmp_path: Path) -> None:
    stand = AbgleichStand(
        abgleich_3d=GUT.abgleich_3d,
        abgleich_2d=(Abgleich2D(index=0, gueltig=False),),
        anzahl_3d=1,
        anzahl_2d=1,
    )
    sim = SimulatorKonfiguration(abgleich=stand)
    o1, o2 = _unter(tmp_path, "ohne"), _unter(tmp_path, "mit")
    a = aufbau(
        o1,
        [messung(o1, "M1")],
        sim_konfiguration=sim,
        konfiguration=_konf(AbgleichModus.VERWEIGERN),
    )
    _lauf(a)
    assert a.protokoll("01_M1")["status"] == "fertig"
    b = aufbau(
        o2,
        [messung(o2, "M1")],
        sim_konfiguration=sim,
        konfiguration=_konf(AbgleichModus.VERWEIGERN, pruefe_2d=True),
    )
    _lauf(b)
    assert _fehlerart(b) == "abgleich"


def test_warnen_misst_weiter_und_meldet_warnung(tmp_path: Path) -> None:
    a = aufbau(
        tmp_path,
        [messung(tmp_path, "M1")],
        sim_konfiguration=SimulatorKonfiguration(abgleich=SCHLECHT),
        konfiguration=_konf(AbgleichModus.WARNEN),
    )
    _lauf(a)
    assert a.protokoll("01_M1")["status"] == "fertig"
    assert "starte_scan" in a.sim.aufgerufene_methoden()
    (warnung,) = _art(a, "abgleich_warnung")
    assert "Abgleich nicht_bestanden" in warnung and "Messung 'M1'" in warnung
    assert _pruefung(a)["ergebnis"] == "nicht_bestanden"


def test_trockenlauf_wertet_das_gate_aus(tmp_path: Path) -> None:
    og = _unter(tmp_path, "gut")
    a = aufbau(
        tmp_path,
        [messung(tmp_path, "M1")],
        sim_konfiguration=SimulatorKonfiguration(abgleich=SCHLECHT),
        konfiguration=_konf(AbgleichModus.VERWEIGERN),
        betriebsart="trockenlauf",
    )
    _lauf(a, trockenlauf=True, freigabe=False)
    assert _fehlerart(a) == "abgleich"
    assert not a.steuerung.momentaufnahme().trockenlauf_ok  # Voraussetzung für MESSEN bleibt aus
    b = aufbau(
        og,
        [messung(og, "M1")],
        sim_konfiguration=SimulatorKonfiguration(abgleich=GUT),
        konfiguration=_konf(AbgleichModus.VERWEIGERN),
        betriebsart="trockenlauf",
    )
    _lauf(b, trockenlauf=True, freigabe=False)
    assert b.steuerung.momentaufnahme().trockenlauf_ok
    assert b.protokoll("01_M1")["status"] == "trockenlauf"


def test_a8_geraet_ohne_leser_modus_aus(tmp_path: Path) -> None:
    a = aufbau(tmp_path, [messung(tmp_path, "M1")], huelle=OhneLeser)  # type: ignore[arg-type]
    _lauf(a)
    assert a.protokoll("01_M1")["status"] == "fertig"
    feld = _abgleich(a)
    assert feld["gelesen"] is False and "kein Lesen des Abgleichs" in str(feld["grund"])
    assert feld["zeit"] is None and feld["abgleich_3d"] == []
    assert any("nicht gelesen" in t for t in _art(a, "abgleich_hinweis"))


@pytest.mark.parametrize(
    ("modus", "erwartet"),
    [(AbgleichModus.WARNEN, "fertig"), (AbgleichModus.VERWEIGERN, "fehler")],
)
def test_geraet_ohne_leser_je_modus(tmp_path: Path, modus: AbgleichModus, erwartet: str) -> None:
    a = aufbau(
        tmp_path,
        [messung(tmp_path, "M1")],
        konfiguration=_konf(modus),
        huelle=OhneLeser,  # type: ignore[arg-type]
    )
    _lauf(a)
    assert a.protokoll("01_M1")["status"] == erwartet
    assert bool(_art(a, "abgleich_warnung")) is (modus is AbgleichModus.WARNEN)
    if erwartet == "fehler":
        assert _fehlerart(a) == "abgleich"


def test_abgleich_nicht_lesbar_geraetefehler(tmp_path: Path) -> None:
    a = aufbau(
        tmp_path,
        [messung(tmp_path, "M1")],
        drehbuch=[AbgleichNichtLesbar(vorgang=0, text="Infos.Alignments im Modus nicht da")],
    )
    _lauf(a)
    assert a.protokoll("01_M1")["status"] == "fertig"
    feld = _abgleich(a)
    assert feld["gelesen"] is False
    assert "lies_abgleich fehlgeschlagen: Infos.Alignments im Modus nicht da" in str(feld["grund"])
    os_ = _unter(tmp_path, "streng")
    b = aufbau(
        os_,
        [messung(os_, "M1")],
        drehbuch=[AbgleichNichtLesbar(vorgang=0)],
        konfiguration=_konf(AbgleichModus.VERWEIGERN),
    )
    _lauf(b)
    assert _fehlerart(b) == "abgleich" and "starte_scan" not in b.sim.aufgerufene_methoden()


def test_pauschal_nicht_lesbarer_stand_aus_dem_geraet(tmp_path: Path) -> None:
    stand = AbgleichStand(nicht_lesbar={"Infos.HasAlignments": "Infos.HasAlignments ist False"})
    a = aufbau(
        tmp_path,
        [messung(tmp_path, "M1")],
        sim_konfiguration=SimulatorKonfiguration(abgleich=stand),
        konfiguration=_konf(AbgleichModus.VERWEIGERN),
    )
    _lauf(a)
    assert _fehlerart(a) == "abgleich"
    feld = _abgleich(a)
    assert feld["gelesen"] is True
    assert feld["nicht_lesbar"] == {"Infos.HasAlignments": "Infos.HasAlignments ist False"}


@pytest.mark.parametrize("modus", list(AbgleichModus))
def test_a7_haenger_beim_lesen_ist_geraet_unklar_in_jedem_modus(
    tmp_path: Path, modus: AbgleichModus
) -> None:
    a = aufbau(
        tmp_path,
        [messung(tmp_path, "M1")],
        drehbuch=[HaengenderAufruf(vorgang=0, methode="lies_abgleich", max_echtzeit_s=0.01)],
        konfiguration=_konf(modus),
    )
    _lauf(a)
    assert a.steuerung.zustand is DurchgangZustand.GERAET_UNKLAR
    assert "starte_scan" not in a.sim.aufgerufene_methoden()
    assert _fehlerart(a) == "geraet_unklar"
    feld = _abgleich(a)
    assert feld["gelesen"] is False and "beim Lesen des Abgleichs" in str(feld["grund"])
    assert "Hänger" in str(feld["grund"]) and "nicht erreicht" not in str(feld["grund"])
    assert _pruefung(a)["ergebnis"] == "nicht_ausgefuehrt"


def test_a7_langsames_lesen_ueber_der_aufrufgrenze_ist_ein_haenger(tmp_path: Path) -> None:
    a = aufbau(
        tmp_path,
        [messung(tmp_path, "M1")],
        drehbuch=[LangsamerAufruf(vorgang=0, methode="lies_abgleich", dauer_s=61.0)],
    )
    _lauf(a)
    assert a.steuerung.zustand is DurchgangZustand.GERAET_UNKLAR


def test_abgleich_wechselt_zwischen_zwei_messungen(tmp_path: Path) -> None:
    a = aufbau(
        tmp_path,
        [messung(tmp_path, "M1"), messung(tmp_path, "M2")],
        drehbuch=[AbgleichBeiLaden(vorgang=1, stand=SCHLECHT)],
        konfiguration=_konf(AbgleichModus.VERWEIGERN),
    )
    _lauf(a)
    assert a.protokoll("01_M1")["status"] == "fertig"
    assert _pruefung(a, "01_M1")["ergebnis"] == "bestanden"
    assert a.protokoll("02_M2")["status"] == "fehler"
    assert _abgleich(a, "02_M2")["abgleich_3d"][0]["gueltig"] is False  # type: ignore[index]
    assert _fehlerart(a, "02_M2") == "abgleich"


def test_hinweis_nur_bei_geaendertem_befundtext(tmp_path: Path) -> None:
    a = aufbau(
        tmp_path,
        [messung(tmp_path, n) for n in ("M1", "M2", "M3", "M4")],
        drehbuch=[
            AbgleichBeiLaden(vorgang=0, stand=SCHLECHT),
            AbgleichBeiLaden(vorgang=1, stand=SCHLECHT),
            AbgleichBeiLaden(vorgang=3, stand=SCHLECHT),
        ],
    )
    _lauf(a)
    # M1 und M2 gleicher Text: ein Hinweis; M3 in Ordnung; M4 wieder auffällig: neuer Hinweis
    assert len(_art(a, "abgleich_hinweis")) == 2


def test_vorpruefung_vor_dem_lesen_schreibt_gelesen_false(tmp_path: Path) -> None:
    m = messung(tmp_path, "M1")
    a = aufbau(tmp_path, [m])
    (tmp_path / "basis.set").unlink()
    _lauf(a)
    assert _fehlerart(a) == "vorpruefung"
    feld = _abgleich(a)
    assert feld["gelesen"] is False and "nicht erreicht" in str(feld["grund"])
    assert "lies_abgleich" not in a.sim.aufgerufene_methoden()
    pruefung = _pruefung(a)
    assert pruefung["ergebnis"] == "nicht_ausgefuehrt" and pruefung["modus"] == "aus"
    assert "nicht ausgeführt" in str(pruefung["befunde"])


def test_ladefehler_vor_dem_lesen(tmp_path: Path) -> None:
    a = aufbau(tmp_path, [messung(tmp_path, "M1")], drehbuch=[LadeFehler(vorgang=0)])
    _lauf(a)
    assert _fehlerart(a) == "geraet"
    assert _abgleich(a)["gelesen"] is False


def test_abweichung_nach_dem_lesen_traegt_den_abgleich(tmp_path: Path) -> None:
    konf = SimulatorKonfiguration(bandbreiten_hz=(3125.0, 6250.0))
    a = aufbau(
        tmp_path,
        [messung(tmp_path, "M1", {"fft.bandbreite_hz": 5000.0})],
        sim_konfiguration=konf,
    )
    _lauf(a)
    assert _fehlerart(a) == "abweichung"
    assert _abgleich(a)["gelesen"] is True  # gelesen vor den Fehlerprüfungen
    # das Gate lief nicht: kein Ergebnis, das als Ablehnung gelesen werden könnte
    assert _pruefung(a)["ergebnis"] == "nicht_ausgefuehrt"


def test_abbruch_schreibt_das_feld(tmp_path: Path) -> None:
    a = aufbau(tmp_path, [messung(tmp_path, "M1")])
    a.starte()
    a.laufe_bis(lambda: a.steuerung.braucht_takt() and a.sim.vorgang == 0)
    a.steuerung.brich_ab()
    a.steuerung.bis_ruhe()
    assert a.protokoll("01_M1")["status"] == "abgebrochen"
    assert _abgleich(a)["gelesen"] is True


def test_konfiguration_standard_ist_aus() -> None:
    assert AblaufKonfiguration().abgleich == AbgleichRegel()
    assert AblaufKonfiguration().abgleich.modus is AbgleichModus.AUS


def test_mehr_als_16_abgleiche_ist_nicht_pruefbar_mit_hinweis(tmp_path: Path) -> None:
    gueltig = Abgleich3D(index=0, gueltig=True)
    stand = AbgleichStand(abgleich_3d=(gueltig,), anzahl_3d=20)
    a = aufbau(
        tmp_path,
        [messung(tmp_path, "M1")],
        sim_konfiguration=SimulatorKonfiguration(abgleich=stand),
        konfiguration=_konf(AbgleichModus.VERWEIGERN),
    )
    _lauf(a)
    assert _fehlerart(a) == "abgleich"
    assert _pruefung(a)["ergebnis"] == "nicht_pruefbar"
    hinweise = _art(a, "abgleich_hinweis")
    assert len(hinweise) == 1 and "nur 1 von 20" in str(hinweise[0])
