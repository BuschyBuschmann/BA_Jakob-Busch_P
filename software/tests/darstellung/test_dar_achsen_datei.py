"""Achsenfelder an ``Input/20261012_ref_Mitte.svd`` (K-AUSW2-A, Befund 1); ohne Datei übersprungen.

Die Auto-Werte der Betragsachse der echten Datei liegen im Bereich 1e-7 bis 1e-3 und müssen im
schmalen Eingabefeld lesbar stehen (Potenzschreibweise, höchstens 12 Zeichen) und die Rundreise
Feld, Wert, Feld unverändert überstehen.
"""

from __future__ import annotations

from pathlib import Path

import pytest
from matplotlib.figure import Figure

from ldv_automation.auswertung.laden import Geladen, lade_svd
from ldv_automation.darstellung.achsen import feld_text, parse_zahl
from ldv_automation.darstellung.auswahl import PaarCache, spektrum_daten
from ldv_automation.darstellung.spektrum import SpektrumOptionen, zeichne_spektrum
from ldv_automation.darstellung.stil import THESIS_STIL

DATEI = Path(__file__).resolve().parents[3] / "Input" / "20261012_ref_Mitte.svd"
pytestmark = pytest.mark.skipif(not DATEI.is_file(), reason="Messdatei nicht vorhanden")
MAX_ZEICHEN = 12  # „\u22121,234·10⁻¹²“ ist der längste Text von feld_text für Amplituden


@pytest.fixture(scope="module")
def geladen() -> Geladen:
    return lade_svd(DATEI)


def test_auto_werte_der_betragsachse_sind_lesbar_und_die_rundreise_ist_stabil(
    geladen: Geladen,
) -> None:
    cache = PaarCache(geladen.messdaten)
    sd = spektrum_daten(geladen.messdaten, cache, punkt=None)
    ax = zeichne_spektrum(Figure(), sd, SpektrumOptionen(), THESIS_STIL).achsen[0]
    unten, oben = (float(v) for v in ax.get_ylim())
    assert 0.0 < unten < oben < 1.0  # Beträge der Datei: weit unter 1 m/s
    for wert in (unten, oben):
        text = feld_text(wert)
        assert "\u00b710" in text or text.startswith("10"), text  # Potenz, nicht „0,000000…“
        assert len(text) <= MAX_ZEICHEN, text
        zurueck = parse_zahl(text)
        assert zurueck is not None and feld_text(zurueck) == text  # Feld → Wert → Feld
        assert zurueck == pytest.approx(wert, rel=5.1e-4)  # nur die Anzeige rundet
    kleinste = min(float(k.y.min()) for k in sd.kurven)
    assert unten <= kleinste and kleinste > 0.0


def test_frequenzachse_der_datei_steht_dezimal_im_feld(geladen: Geladen) -> None:
    f = geladen.messdaten.frequenz_hz
    assert feld_text(float(f[0])) == "0,625" and feld_text(float(f[-1])) == "1000"
    for wert in (float(f[0]), float(f[-1]), 1200.5):
        assert parse_zahl(feld_text(wert)) == pytest.approx(wert, rel=5.1e-4)
