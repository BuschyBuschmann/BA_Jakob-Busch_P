"""``lade_svd`` an ``Input/20261012_ref_Mitte.svd`` (P-AUSW T1.3); ohne Datei übersprungen.

Sollwerte der Dateieinstellungen (Beispieldatei, Fft-Stream und File-Access-Gegenprobe vom
2026-11-02): Bandbreite 1000 Hz, 1600 Linien, Δf = 0,625 Hz, Abtastfrequenz 2500 Hz,
Mittelung Typ 2 (komplex) Anzahl 7, 135 Punkte, Referenzen Ref1 [N] und Ref2 [m/s²].
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pytest

from ldv_automation.auswertung.export import sha256_datei
from ldv_automation.auswertung.laden import Geladen, lade_svd
from ldv_automation.auswertung.svd_adapter import aus_svd_messung
from ldv_automation.auswertung.svd_lesen import Mittelung, lese_svd

DATEI = Path(__file__).resolve().parents[3] / "Input" / "20261012_ref_Mitte.svd"
SHA256_DATEI = "7ef46262df0055f5a45470ae0fc5e6bde547624cdee6b5dc3838060a452e790b"

pytestmark = pytest.mark.skipif(not DATEI.is_file(), reason="Messdatei nicht vorhanden")


@pytest.fixture(scope="module")
def geladen() -> Geladen:
    return lade_svd(DATEI)


def test_einstellungen_der_beispieldatei(geladen: Geladen) -> None:
    e = geladen.einstellungen
    assert e.bandbreite_hz == 1000.0
    assert e.linien == 1600
    assert e.delta_f_hz == 0.625
    assert e.abtastfrequenz_hz == 2500.0
    assert e.mittelung == Mittelung(typ=2, anzahl=7)
    assert e.punkte == 135
    assert e.referenzen == (("Ref1", "N"), ("Ref2", "m/s²"))


def test_messdaten_identisch_zum_bisherigen_weg_und_datei_unveraendert(geladen: Geladen) -> None:
    herkunft = geladen.messdaten.herkunft
    assert herkunft is not None and herkunft.sha256 == SHA256_DATEI
    erwartet = aus_svd_messung(lese_svd(DATEI), sha256=SHA256_DATEI)
    ist = geladen.messdaten
    np.testing.assert_array_equal(ist.frequenz_hz, erwartet.frequenz_hz)
    assert list(ist.cp) == list(erwartet.cp)
    for paar, werte in erwartet.cp.items():
        np.testing.assert_array_equal(ist.cp[paar], werte)
    for kanal, werte_ap in erwartet.ap.items():
        np.testing.assert_array_equal(ist.ap[kanal], werte_ap)
    assert ist.phase_gueltig is erwartet.phase_gueltig is True
    assert sha256_datei(DATEI) == SHA256_DATEI


def test_frequenzachse_ist_k_mal_delta_f_aus_der_datei(geladen: Geladen) -> None:
    f = geladen.messdaten.frequenz_hz
    np.testing.assert_allclose(f, 0.625 * np.arange(1, 1601), rtol=1e-15, atol=0.0)
    assert f[0] == 0.625 and f[-1] == 1000.0
