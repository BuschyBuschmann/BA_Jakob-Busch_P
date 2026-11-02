"""Punktstatus-Tabelle (K-2D Punkt 3): Werte gegen die Polytec-Doku, Bitmaske, unbekannte Bits."""

from __future__ import annotations

import re
from pathlib import Path

import numpy as np
import pytest

from ldv_automation.auswertung.punktstatus import (
    BITS_BEKANNT,
    STATUS_TEXTE,
    PunktStatus,
    statustexte,
)

DOKU = (
    Path(__file__).resolve().parents[3]
    / "in_progress/analysen/polytec-chm-text/basic-engine-manual/POLYFILELib/PTCScanStatus.md"
)

# Auftrag K-2D (Nutzerangabe) – unabhängig von der Doku-Datei notiert
AUFTRAGSWERTE = {
    "Nicht gemessen": 0,
    "Gültig": 1,
    "Optimal": 2,
    "Overrange": 4,
    "Ungültig": 8,
    "Gesperrt": 16,
    "Nicht erreichbar": 64,
    "Verdeckt": 128,
    "VT fehlgeschlagen": 256,
    "Interpoliert": 512,
}


def test_werte_wie_im_auftrag() -> None:
    for text, wert in AUFTRAGSWERTE.items():
        assert STATUS_TEXTE[PunktStatus(wert)] == text


@pytest.mark.skipif(not DOKU.is_file(), reason="Polytec-Doku nicht im Repository")
def test_tabelle_stimmt_mit_der_polytec_doku_ueberein() -> None:
    """Alle Mitglieder der Doku-Enumeration, mit gleichem Wert (Gegenprobe der Quelle)."""
    doku = {
        m.group(1): int(m.group(2))
        for m in re.finditer(r"^\| ptcScanStatus(\w+) \| (\d+) \|", DOKU.read_text("utf-8"), re.M)
    }
    assert len(doku) == 15
    assert sorted(doku.values()) == sorted(int(b) for b in PunktStatus.__members__.values())
    assert doku["Valid"] == PunktStatus.GUELTIG
    assert doku["VideoTriangulationFailed"] == PunktStatus.VT_FEHLGESCHLAGEN
    assert doku["Disabled"] == PunktStatus.GESPERRT
    assert doku["InterpolationFailed"] == PunktStatus.INTERPOLATION_FEHLGESCHLAGEN


def test_bits_sind_verschiedene_zweierpotenzen_und_alle_haben_text() -> None:
    werte = [int(b) for b in PunktStatus.__members__.values() if b != 0]
    assert len(set(werte)) == len(werte)
    assert all(w & (w - 1) == 0 for w in werte)
    assert set(STATUS_TEXTE) == set(PunktStatus.__members__.values())
    assert sum(werte) == BITS_BEKANNT


def test_einzelne_codes_und_kombinationen() -> None:
    assert statustexte(0) == ("Nicht gemessen",)
    assert statustexte(1) == ("Gültig",)
    assert statustexte(1 | 2) == ("Gültig", "Optimal")
    assert statustexte(1 | 4 | 512) == ("Gültig", "Overrange", "Interpoliert")
    assert statustexte(64 | 128) == ("Nicht erreichbar", "Verdeckt")


def test_unbekannte_bits_werden_sichtbar_gemeldet() -> None:
    assert statustexte(1 | 0x4000) == ("Gültig", "unbekanntes Statusbit 0x4000")
    assert statustexte(0x10000 | 0x4000) == (
        "unbekanntes Statusbit 0x4000",
        "unbekanntes Statusbit 0x10000",
    )


def test_numpy_ganzzahlen_zulaessig() -> None:
    assert statustexte(np.int32(9)) == ("Gültig", "Ungültig")  # type: ignore[arg-type]
    assert statustexte(int(np.uint16(8))) == ("Ungültig",)


def test_ungueltige_eingaben() -> None:
    with pytest.raises(ValueError, match="negativ"):
        statustexte(-1)
    with pytest.raises(TypeError):
        statustexte(True)
    with pytest.raises(TypeError):
        statustexte(1.0)  # type: ignore[arg-type]
