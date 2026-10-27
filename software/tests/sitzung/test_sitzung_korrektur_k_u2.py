"""Korrekturpaket K-U2, Erweiterung: MINOR-1, MINOR-2, Zurücksetzen, MINOR-4 (Sitzung)."""

from __future__ import annotations

import time
from pathlib import Path

import pytest

from ldv_automation.ablauf.steuerung import AblaufKonfiguration, DurchgangErgebnis, DurchgangZustand
from ldv_automation.ablauf.uhr import Echtzeituhr, Testuhr
from ldv_automation.domaene.eintraege import Messung, Pausenpunkt
from ldv_automation.geraet.schnittstelle import Messgeraet
from ldv_automation.geraet.simulator import Haenger, Simulator, StartFehler
from ldv_automation.protokoll.version import BuildInfo
from ldv_automation.sitzung import Betriebsart, Sitzung

GIT = BuildInfo(paket_version="0.1.0", git_hash="e" * 40, git_dirty=False, quelle="test")


class Fabrik:
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
    tmp_path: Path, betriebsart: Betriebsart = Betriebsart.SIMULATOR, **sim: object
) -> tuple[Sitzung, Fabrik]:
    uhr = Testuhr()
    fabrik = Fabrik(uhr, **sim)
    wurzel = tmp_path / "daten"
    wurzel.mkdir(exist_ok=True)
    s = Sitzung(
        geraete_fabrik=fabrik,
        betriebsart=betriebsart,
        uhr=uhr,
        build_info=GIT,
        messdaten_wurzel=wurzel,
    )
    s.verarbeite()
    s.verbinde()
    s.verarbeite()
    return s, fabrik


def _trockenlauf_ok(s: Sitzung) -> bool:
    return next(v for v in s.messen_voraussetzungen() if v.name == "trockenlauf").erfuellt


def _nach_trockenlauf(tmp_path: Path) -> tuple[Sitzung, Fabrik, Messung, Messung]:
    s, fabrik = _sitzung(tmp_path, Betriebsart.TROCKENLAUF)
    m1 = Messung(name="M1", einstellungsdatei=_set(tmp_path), parameter={"fft.linien": 800})
    m2 = Messung(name="M2", einstellungsdatei=_set(tmp_path))
    s.einfuegen(0, m1)
    s.einfuegen(1, m2)
    s.starte("trocken")
    s.verarbeite()
    assert _trockenlauf_ok(s)
    return s, fabrik, m1, m2


# --- MINOR-1: verlorenes Gerät wird neu erzeugt --------------------------------------


def test_minor_1_nach_geraet_unklar_wird_geraet_neu_erzeugt(tmp_path: Path) -> None:
    s, fabrik = _sitzung(tmp_path, drehbuch=[Haenger(vorgang=0, stop_wirkt=False)])
    s.einfuegen(0, Messung(name="M1", einstellungsdatei=_set(tmp_path), zeitlimit_s=1.0))
    s.starte("x")
    s.verarbeite()
    assert s.zustandsbild().durchgang is DurchgangZustand.GERAET_UNKLAR
    s.trenne()
    s.verarbeite()
    s.quittiere()
    s.verarbeite()
    alt = fabrik.erzeugt[0]
    anzahl = len(alt.aufrufe)

    s.verbinde()
    s.verarbeite()

    assert len(fabrik.erzeugt) == 2
    assert len(alt.aufrufe) == anzahl  # altes Gerät nicht mehr angesprochen
    # U5/B1: beim Verbinden wird zusätzlich der Gerätestand gelesen (nur lesend).
    assert fabrik.erzeugt[1].aufgerufene_methoden() == (
        "verbinde",
        "zustand",
        "lies_einstellungsstand",
    )
    bild = s.zustandsbild()
    assert bild.verbunden and bild.betriebsart is Betriebsart.SIMULATOR


def test_minor_1_ohne_verlust_kein_neues_geraet(tmp_path: Path) -> None:
    s, fabrik = _sitzung(tmp_path)
    s.trenne()
    s.verarbeite()
    s.verbinde()
    s.verarbeite()
    assert len(fabrik.erzeugt) == 1


# --- MINOR-2: Trockenlauf-Freischaltung an die Warteschlange gebunden ----------------


@pytest.mark.parametrize("aktion", ["bearbeiten", "entfernen", "verschieben", "einfuegen_vorn"])
def test_minor_2_freischaltung_erlischt_bei_aenderung_der_ersten_messung(
    tmp_path: Path, aktion: str
) -> None:
    s, _, m1, _ = _nach_trockenlauf(tmp_path)
    s.zuruecksetzen()  # damit Einträge wieder bearbeitbar sind
    assert _trockenlauf_ok(s)
    if aktion == "bearbeiten":
        s.bearbeiten(m1.id, parameter={"fft.linien": 1600})
        s.bearbeiten(m1.id, parameter={"fft.linien": 800})  # zurück: bleibt erloschen
    elif aktion == "entfernen":
        s.entfernen(m1.id)
    elif aktion == "verschieben":
        s.verschieben(m1.id, 1)
        s.verschieben(m1.id, 0)  # zurück: bleibt erloschen
    else:
        s.einfuegen(0, Messung(name="M0", einstellungsdatei=_set(tmp_path)))
    assert not _trockenlauf_ok(s)
    assert any(e.art == "trockenlauf_verworfen" for e in s.hole_ereignisse())


def test_minor_2_aenderung_spaeterer_eintraege_laesst_freischaltung(tmp_path: Path) -> None:
    s, _, _, m2 = _nach_trockenlauf(tmp_path)
    s.zuruecksetzen()
    s.bearbeiten(m2.id, notiz="anders")
    s.einfuegen(2, Pausenpunkt(text="Umbau"))
    s.entfernen(m2.id)
    assert _trockenlauf_ok(s)


def test_minor_2_laden_einer_warteschlange_entzieht_freischaltung(tmp_path: Path) -> None:
    s, _, _, _ = _nach_trockenlauf(tmp_path)
    datei = tmp_path / "q.warteschlange.json"
    s.speichere_warteschlange(datei)
    s.lade_warteschlange(datei)  # auch identischer Inhalt gilt als andere Warteschlange
    assert not _trockenlauf_ok(s)


# --- Zurücksetzen ---------------------------------------------------------------------


def test_zuruecksetzen_nach_trockenlauf_und_messen(tmp_path: Path) -> None:
    """Ablauf für Montag: Trockenlauf, Zurücksetzen, MESSEN mit denselben Einträgen."""
    s, fabrik, m1, m2 = _nach_trockenlauf(tmp_path)
    bild = s.zustandsbild()
    assert bild.zuruecksetzen_moeglich
    ordner = Path(str(bild.durchgangsordner))
    dateien_vorher = sorted(p.name for p in ordner.iterdir())

    s.zuruecksetzen()

    bild = s.zustandsbild()
    assert [(e.id, e.zustand, e.versuch, e.nummer) for e in bild.eintraege] == [
        (m1.id, "wartend", 1, None),
        (m2.id, "wartend", 1, None),
    ]
    assert bild.eintraege[0].parameter == {"fft.linien": 800}
    assert not bild.zuruecksetzen_moeglich
    assert sorted(p.name for p in ordner.iterdir()) == dateien_vorher
    assert _trockenlauf_ok(s)

    s.quittiere()
    s.verarbeite()
    s.setze_betriebsart(Betriebsart.MESSEN)
    s.verarbeite()
    s.verbinde()
    s.verarbeite()
    s.starte("echt", messen_bestaetigt=True)
    s.verarbeite()
    bild = s.zustandsbild()
    assert bild.ergebnis is DurchgangErgebnis.VOLLSTAENDIG
    assert [e.zustand for e in bild.eintraege] == ["fertig", "fertig"]
    assert fabrik.erzeugt[-1].aufgerufene_methoden().count("starte_scan") == 2


def test_zuruecksetzen_setzt_versuchszaehler_und_pausenpunkte_zurueck(tmp_path: Path) -> None:
    from ldv_automation.ablauf.steuerung import Fehlerentscheidung

    s, _ = _sitzung(tmp_path, drehbuch=[StartFehler(vorgang=0)])
    m = Messung(name="M1", einstellungsdatei=_set(tmp_path))
    pp = Pausenpunkt(text="Umbau")
    s.einfuegen(0, m)
    s.einfuegen(1, pp)
    s.starte("x")
    s.verarbeite()
    s.entscheide(Fehlerentscheidung.WIEDERHOLEN)
    s.verarbeite()
    s.bestaetige()
    s.verarbeite()
    vorher = s.zustandsbild()
    assert [(e.zustand, e.versuch) for e in vorher.eintraege] == [("fertig", 2), ("erledigt", None)]
    s.zuruecksetzen()
    nachher = s.zustandsbild()
    assert [(e.id, e.zustand, e.versuch) for e in nachher.eintraege] == [
        (m.id, "wartend", 1),
        (pp.id, "wartend", None),
    ]
    assert nachher.eintraege[1].text == "Umbau"


def test_zuruecksetzen_nur_in_ruhe(tmp_path: Path) -> None:
    s, _ = _sitzung(tmp_path)
    s.einfuegen(0, Messung(name="M1", einstellungsdatei=_set(tmp_path)))
    assert not s.zustandsbild().zuruecksetzen_moeglich  # nichts zurückzusetzen
    s.starte("x")
    s.steuerung.schritt()
    assert not s.zustandsbild().zuruecksetzen_moeglich
    with pytest.raises(ValueError, match="Zurücksetzen"):
        s.zuruecksetzen()


# --- MINOR-4: Wächter stirbt nicht still ----------------------------------------------


def test_minor_4_waechter_meldet_fehler_und_laeuft_weiter(tmp_path: Path) -> None:
    uhr = Echtzeituhr()
    zustand = {"kaputt": True, "aufrufe": 0}

    class Wackelig(Simulator):
        def haengender_aufruf_seit_s(self) -> float | None:
            zustand["aufrufe"] += 1
            if zustand["kaputt"]:
                raise RuntimeError("Wächterfehler")
            return None

    s = Sitzung(
        geraete_fabrik=lambda art: Wackelig(uhr.monotonic, betriebsart=art.value),
        uhr=uhr,
        build_info=GIT,
        konfiguration=AblaufKonfiguration(poll_s=0.005),
    )
    s.starte_threads(waechter_takt_s=0.005)
    try:
        frist = time.monotonic() + 5.0
        gesammelt: list[str] = []
        while "waechter_fehler" not in gesammelt:
            assert time.monotonic() < frist, "kein waechter_fehler gemeldet"
            gesammelt += [e.art for e in s.hole_ereignisse()]
            time.sleep(0.005)
        time.sleep(0.05)  # weitere fehlerhafte Takte: keine zusätzliche Meldung
        gesammelt += [e.art for e in s.hole_ereignisse()]
        assert gesammelt.count("waechter_fehler") == 1
        zustand["kaputt"] = False
        vorher = zustand["aufrufe"]
        while zustand["aufrufe"] < vorher + 3:
            assert time.monotonic() < frist, "Wächter läuft nicht weiter"
            time.sleep(0.005)
        assert s._waechter_thread is not None and s._waechter_thread.is_alive()
        assert s.steuerung.momentaufnahme().interner_fehler is None
    finally:
        assert s.beende_threads(timeout_s=5.0)


def test_minor_4_waechter_takt_synchron(tmp_path: Path) -> None:
    s, fabrik = _sitzung(tmp_path)

    def kaputt() -> float | None:
        raise RuntimeError("defekt")

    fabrik.erzeugt[0].haengender_aufruf_seit_s = kaputt  # type: ignore[method-assign]
    s.hole_ereignisse()
    s._waechter_takt()
    assert [e.art for e in s.hole_ereignisse()] == ["waechter_fehler"]
    assert s.zustandsbild().waechter_s is None  # Bild entsteht trotz Gerätefehler
