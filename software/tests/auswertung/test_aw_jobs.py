"""Aufträge ``lese_job``, ``pruef_job``, ``export_job`` (P-AUSW T1.4) an synthetischen Daten.

``lade_svd`` wird durch eine Funktion ersetzt, die synthetische Messdaten (Einmassenschwinger,
FG-02 9.4) liefert; so laufen die Aufträge ohne Messdatei. Mit der echten Beispieldatei und
echtem ``spawn`` laufen sie in ``test_aw_jobs_datei.py``.
"""

from __future__ import annotations

import dataclasses
import pickle
from pathlib import Path

import aw_referenz as ref
import numpy as np
import pytest

from ldv_automation.auswertung import Messdaten, werte_aus
from ldv_automation.auswertung import jobs as jobmodul
from ldv_automation.auswertung.daten import Herkunft
from ldv_automation.auswertung.export import exportiere, lese_export
from ldv_automation.auswertung.jobs import PruefErgebnis, export_job, lese_job, pruef_job
from ldv_automation.auswertung.laden import Dateieinstellungen, Geladen, LadeFehler
from ldv_automation.hintergrund import AuftragFehler, DirektAusfuehrer

SHA = "ab" * 32
PFAD = "/daten/messung.svd"


def _daten() -> Messdaten:
    k, p = 800, 3
    f = 0.5 * np.arange(1, k + 1, dtype=np.float64)
    y = ref.mobilitaet_moden(f, [100.0, 150.0, 260.0])
    h = np.broadcast_to(y, (p, k)).astype(np.complex128)
    akz = np.broadcast_to(1j * 2 * np.pi * f * y, (p, k)).astype(np.complex128)
    daten = ref.messdaten(
        frequenz_hz=f,
        ap={
            "Vib Z": (np.abs(h) ** 2 * 1.0001).astype(np.float64),
            "Ref1": np.ones((p, k)),
            "Ref2": (np.abs(akz) ** 2).astype(np.float64),
        },
        cp={("Vib Z", "Ref1"): h, ("Ref2", "Ref1"): akz},
    )
    return dataclasses.replace(daten, herkunft=Herkunft(pfad=PFAD, sha256=SHA))


@pytest.fixture
def daten(monkeypatch: pytest.MonkeyPatch) -> Messdaten:
    d = _daten()
    einstellungen = Dateieinstellungen(
        bandbreite_hz=400.0,
        linien=800,
        delta_f_hz=0.5,
        abtastfrequenz_hz=1000.0,
        mittelung=None,
        punkte=3,
        referenzen=(("Ref1", "N"),),
    )

    def fake(_pfad: str) -> Geladen:
        return Geladen(messdaten=d, einstellungen=einstellungen)

    monkeypatch.setattr(jobmodul, "lade_svd", fake)
    return d


def test_lese_job_liefert_geladen(daten: Messdaten) -> None:
    geladen = lese_job(PFAD)
    assert geladen.messdaten is daten
    assert geladen.einstellungen.punkte == 3


def test_pruef_job_entspricht_werte_aus(daten: Messdaten) -> None:
    ergebnis = pruef_job(PFAD, SHA)
    soll = werte_aus(daten)
    assert ergebnis.sha256 == SHA
    assert [(e.id, e.status, e.grund, e.bezug) for e in ergebnis.pruefungen] == [
        (e.id, e.status, e.grund, e.bezug) for e in soll.pruefungen
    ]
    assert ergebnis.annahmen == soll.annahmen_liste
    assert len(ergebnis.pruefungen) >= 11  # P-01 … P-11 (P-05/07/09 je Paar)


def test_pruef_job_ohne_erwartete_summe_und_mit_antriebspunkt(daten: Messdaten) -> None:
    ohne = pruef_job(PFAD)
    p08_ohne = next(e for e in ohne.pruefungen if e.id == "P-08")
    assert p08_ohne.status == "nicht_pruefbar"
    mit = pruef_job(PFAD, SHA, ("Ref2", "Ref1", "akzeleranz"))
    p08_mit = next(e for e in mit.pruefungen if e.id == "P-08")
    assert p08_mit.status != "nicht_pruefbar"


def test_pruef_job_antriebspunkt_ohne_kreuzspektrum(daten: Messdaten) -> None:
    with pytest.raises(ValueError, match="kein Kreuzspektrum"):
        pruef_job(PFAD, SHA, ("Vib Z", "Ref2", "akzeleranz"))


@pytest.mark.parametrize("job", ["pruef", "export"])
def test_veraenderte_datei_wird_abgewiesen(daten: Messdaten, tmp_path: Path, job: str) -> None:
    falsch = "cd" * 32
    with pytest.raises(LadeFehler, match="verändert") as info:
        if job == "pruef":
            pruef_job(PFAD, falsch)
        else:
            export_job(PFAD, str(tmp_path / "e"), falsch)
    assert PFAD in str(info.value)
    assert not list(tmp_path.iterdir())  # nichts geschrieben


def test_pruef_ergebnis_ist_picklebar_und_klein(daten: Messdaten) -> None:
    roh = pickle.dumps(pruef_job(PFAD, SHA), protocol=5)
    zurueck = pickle.loads(roh)
    assert isinstance(zurueck, PruefErgebnis)
    assert zurueck.annahmen == werte_aus(daten).annahmen_liste
    assert len(roh) < 1_000_000  # Prüfjob-Ergebnis < 1 MB (Plan: 0,5 MB)


def test_export_job_schreibt_export_mit_gesamtband(daten: Messdaten, tmp_path: Path) -> None:
    basis = tmp_path / "ergebnis"
    npz, js = export_job(PFAD, str(basis), SHA)
    assert (npz, js) == (str(basis) + ".npz", str(basis) + ".json")
    felder, meta = lese_export(basis)
    assert meta["herkunft"]["messdatei_sha256"] == SHA
    baender = meta["baender"]
    assert baender and {(b["f_u_hz"], b["f_o_hz"]) for b in baender} == {(0.5, 400.0)}
    assert felder  # der Export enthält Felder


def test_export_job_gleich_exportiere_mit_denselben_baendern(
    daten: Messdaten, tmp_path: Path
) -> None:
    grenzen = [(50.0, 200.0), (200.0, 400.0)]
    export_job(PFAD, str(tmp_path / "job"), SHA, grenzen)
    exportiere(werte_aus(daten, baender=grenzen), tmp_path / "direkt")
    f_job, m_job = lese_export(tmp_path / "job")
    f_dir, m_dir = lese_export(tmp_path / "direkt")
    assert set(f_job) == set(f_dir)
    for name in f_job:
        np.testing.assert_array_equal(f_job[name], f_dir[name])  # bitgleich: dieselbe Rechnung
    assert m_job["baender"] == m_dir["baender"]
    assert m_job["pruefungen"] == m_dir["pruefungen"]


def test_export_job_vorhandenes_ziel_scheitert_vor_der_rechnung(
    daten: Messdaten, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    basis = tmp_path / "da"
    (tmp_path / "da.npz").write_bytes(b"alt")

    def nicht_aufrufen(_: str) -> Geladen:
        raise AssertionError("Die Datei darf bei vorhandenem Ziel nicht geladen werden")

    monkeypatch.setattr(jobmodul, "lade_svd", nicht_aufrufen)
    with pytest.raises(FileExistsError, match=r"da\.npz"):
        export_job(PFAD, str(basis))
    assert (tmp_path / "da.npz").read_bytes() == b"alt"


def test_export_job_ueberschreiben(daten: Messdaten, tmp_path: Path) -> None:
    basis = tmp_path / "da"
    (tmp_path / "da.npz").write_bytes(b"alt")
    (tmp_path / "da.json").write_text("{}", encoding="utf-8")
    export_job(PFAD, str(basis), SHA, None, True)
    _, meta = lese_export(basis)
    assert meta["format"].startswith("ldv_automation.auswertung.export")


def test_export_job_zielordner_fehlt(daten: Messdaten, tmp_path: Path) -> None:
    with pytest.raises(FileNotFoundError, match="Zielordner fehlt"):
        export_job(PFAD, str(tmp_path / "gibt_es_nicht" / "e"))


def test_fehler_der_auftraege_erreichen_die_oberflaeche_als_auftragsfehler(
    tmp_path: Path,
) -> None:
    fehlt = tmp_path / "fehlt.svd"
    auftrag = DirektAusfuehrer().starte(lese_job, str(fehlt))
    with pytest.raises(AuftragFehler) as info:
        auftrag.ergebnis()
    assert info.value.typ == "LadeFehler"
    assert str(fehlt) in info.value.meldung
