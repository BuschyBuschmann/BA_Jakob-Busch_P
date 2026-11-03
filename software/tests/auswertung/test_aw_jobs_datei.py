"""Echter ``spawn``-Test der Aufträge an ``Input/20261012_ref_Mitte.svd`` (P-AUSW T1.4).

Prüft den ganzen Weg: neuer Prozess, Leser, Übertragung von etwa 48 MB in Teilen, Abbruch
(``terminate``) und Fehlerfälle. Ohne Messdatei übersprungen. Die gemessenen Zeiten gelten
für diesen Rechner; die Schranken unten sind großzügige Regressionsgrenzen, keine
Messrechner-Werte (dort misst ``tools/auswertung/zeiten_messen.py``).
"""

from __future__ import annotations

import time
from collections.abc import Iterator
from pathlib import Path

import numpy as np
import pytest

from ldv_automation.auswertung.export import sha256_datei
from ldv_automation.auswertung.jobs import PruefErgebnis, lese_job, pruef_job
from ldv_automation.auswertung.laden import Geladen, LadeFehler, lade_svd
from ldv_automation.hintergrund import (
    Auftrag,
    AuftragAbgebrochen,
    AuftragFehler,
    ProzessAusfuehrer,
)

DATEI = Path(__file__).resolve().parents[3] / "Input" / "20261012_ref_Mitte.svd"
SHA256_DATEI = "7ef46262df0055f5a45470ae0fc5e6bde547624cdee6b5dc3838060a452e790b"

pytestmark = pytest.mark.skipif(not DATEI.is_file(), reason="Messdatei nicht vorhanden")


@pytest.fixture
def ausfuehrer() -> Iterator[ProzessAusfuehrer]:
    a = ProzessAusfuehrer()
    yield a
    a.beende()


def _warte(auftrag: Auftrag, frist_s: float = 120.0) -> float:
    """Wartet im 10-ms-Takt wie die Oberfläche; gibt die längste Einzelabfrage zurück."""
    ende = time.monotonic() + frist_s
    laengste = 0.0
    while True:
        t0 = time.perf_counter()
        fertig = auftrag.fertig()
        laengste = max(laengste, time.perf_counter() - t0)
        if fertig:
            return laengste
        assert time.monotonic() < ende, "Auftrag nicht rechtzeitig fertig"
        time.sleep(0.01)


def test_lese_job_im_prozess_ist_gleich_dem_lesen_im_hauptprozess(
    ausfuehrer: ProzessAusfuehrer,
) -> None:
    auftrag = ausfuehrer.starte(lese_job, str(DATEI))
    laengste_abfrage = _warte(auftrag)
    ergebnis = auftrag.ergebnis()
    assert isinstance(ergebnis, Geladen)
    soll = lade_svd(DATEI)
    assert ergebnis.einstellungen == soll.einstellungen
    ist, erwartet = ergebnis.messdaten, soll.messdaten
    np.testing.assert_array_equal(ist.frequenz_hz, erwartet.frequenz_hz)
    assert list(ist.cp) == list(erwartet.cp) and list(ist.ap) == list(erwartet.ap)
    for paar, werte in erwartet.cp.items():
        np.testing.assert_array_equal(ist.cp[paar], werte)
    for kanal, werte_ap in erwartet.ap.items():
        np.testing.assert_array_equal(ist.ap[kanal], werte_ap)
    for paar, werte_cph in erwartet.cph.items():
        np.testing.assert_array_equal(ist.cph[paar], werte_cph)
    assert ist.einheiten == erwartet.einheiten
    assert ist.herkunft is not None and ist.herkunft.sha256 == SHA256_DATEI
    np.testing.assert_array_equal(ist.punkte.koordinaten_m, erwartet.punkte.koordinaten_m)
    assert sha256_datei(DATEI) == SHA256_DATEI  # Datei nur gelesen
    # UI-15: eine Abfrage blockiert nie lange (gemessen 20 bis 60 ms; Regressionsgrenze)
    assert laengste_abfrage < 0.5


def test_lese_job_abbrechen_waehrend_des_lesens(ausfuehrer: ProzessAusfuehrer) -> None:
    auftrag = ausfuehrer.starte(lese_job, str(DATEI))
    time.sleep(0.05)
    beginn = time.perf_counter()
    auftrag.abbrechen()
    assert time.perf_counter() - beginn < 5.0  # terminate: gemessen etwa 2 ms
    assert auftrag.fertig() is True
    with pytest.raises(AuftragAbgebrochen):
        auftrag.ergebnis()
    assert sha256_datei(DATEI) == SHA256_DATEI


def test_lese_job_fehler_fehlende_datei(ausfuehrer: ProzessAusfuehrer, tmp_path: Path) -> None:
    fehlt = tmp_path / "fehlt.svd"
    auftrag = ausfuehrer.starte(lese_job, str(fehlt))
    _warte(auftrag)
    with pytest.raises(AuftragFehler) as info:
        auftrag.ergebnis()
    assert info.value.typ == LadeFehler.__name__
    assert str(fehlt) in info.value.meldung and "nicht gefunden" in info.value.meldung


def test_lese_job_fehler_keine_psv_datei(ausfuehrer: ProzessAusfuehrer, tmp_path: Path) -> None:
    text = tmp_path / "notizen.svd"
    text.write_text("keine Messdatei", encoding="utf-8")
    auftrag = ausfuehrer.starte(lese_job, str(text))
    _warte(auftrag)
    with pytest.raises(AuftragFehler, match="OLE") as info:
        auftrag.ergebnis()
    assert str(text) in info.value.meldung


def test_pruef_job_im_prozess_liefert_45_pruefungen_und_9_annahmen(
    ausfuehrer: ProzessAusfuehrer,
) -> None:
    """Stufe B an der Beispieldatei: 45 Prüfergebnisse (Plan P-AUSW: 36 ok, 8 nicht prüfbar,
    1 Hinweis), 9 Annahmen; Rechenzeit etwa 10 s."""
    auftrag = ausfuehrer.starte(pruef_job, str(DATEI), SHA256_DATEI)
    laengste_abfrage = _warte(auftrag)
    ergebnis = auftrag.ergebnis()
    assert isinstance(ergebnis, PruefErgebnis)
    assert ergebnis.sha256 == SHA256_DATEI
    assert len(ergebnis.pruefungen) == 45
    stati = [e.status for e in ergebnis.pruefungen]
    assert (stati.count("ok"), stati.count("nicht_pruefbar"), stati.count("hinweis")) == (36, 8, 1)
    assert [e.id for e in ergebnis.pruefungen] == sorted(e.id for e in ergebnis.pruefungen)
    assert len(ergebnis.annahmen) == 9
    assert laengste_abfrage < 0.5  # UI-15: die Oberfläche blockiert während der Rechnung nicht


def test_pruef_job_veraenderte_datei_wird_abgewiesen(ausfuehrer: ProzessAusfuehrer) -> None:
    auftrag = ausfuehrer.starte(pruef_job, str(DATEI), "00" * 32)
    _warte(auftrag)
    with pytest.raises(AuftragFehler, match="verändert"):
        auftrag.ergebnis()
