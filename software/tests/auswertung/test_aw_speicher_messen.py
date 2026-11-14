"""Messskript ``tools/auswertung/speicher_messen.py`` (R-058, P-AUSW2 S5)."""

from __future__ import annotations

import json
from pathlib import Path

import aw_referenz as ref
import numpy as np
import pytest
import speicher_messen as sm

from ldv_automation.auswertung.laden import Dateieinstellungen, Geladen, referenzen_aus
from ldv_automation.auswertung.svd_lesen import Mittelung

DATEI = Path(__file__).resolve().parents[3] / "Input" / "20261012_ref_Mitte.svd"


def synth_geladen(_pfad: str) -> Geladen:
    k = 16
    f = 0.5 * np.arange(1, k + 1, dtype=np.float64)
    kanaele = ("Vib X", "Vib Y", "Ref1")
    ap = {kk: np.ones((3, k)) for kk in kanaele}
    cp = {
        ("Vib X", "Ref1"): np.ones((3, k), dtype=np.complex128),
        ("Vib Y", "Ref1"): np.ones((3, k), dtype=np.complex128),
    }
    daten = ref.messdaten(frequenz_hz=f, ap=ap, cp=cp)
    einstellungen = Dateieinstellungen(
        bandbreite_hz=8.0,
        linien=k,
        delta_f_hz=0.5,
        abtastfrequenz_hz=20.0,
        mittelung=Mittelung(typ=2, anzahl=1),
        punkte=3,
        referenzen=referenzen_aus(daten),
    )
    return Geladen(messdaten=daten, einstellungen=einstellungen)


class _Zaehler:
    """Speicher, der bei jedem Aufruf um einen festen Betrag wächst (MiB)."""

    def __init__(self, schritt: float) -> None:
        self.wert = 100.0
        self.schritt = schritt

    def __call__(self) -> float:
        self.wert += self.schritt
        return self.wert


def test_messe_liefert_zuwachs_je_messung_und_untergrenze() -> None:
    werte = sm.messe(["a.svd", "b.svd"], paare=2, rss=_Zaehler(1.5), lade=synth_geladen)
    assert [w["nr"] for w in werte] == [1, 2] and [w["paare"] for w in werte] == [2, 2]
    for w in werte:
        assert w["zuwachs_laden_mib"] == pytest.approx(1.5, abs=1e-12)  # Zähler-Schritt
        assert w["zuwachs_paare_mib"] == pytest.approx(1.5, abs=1e-12)
        assert w["untergrenze_mib"] > 0.0
    assert werte[1]["rss_nach_mib"] > werte[0]["rss_nach_mib"]
    ohne = sm.messe(["a.svd"], paare=0, rss=_Zaehler(0.0), lade=synth_geladen)
    assert ohne[0]["paare"] == 0
    mehr = sm.messe(["a.svd"], paare=5, rss=_Zaehler(0.0), lade=synth_geladen)
    assert mehr[0]["paare"] == 2  # nur vorhandene Paare
    assert mehr[0]["untergrenze_mib"] > ohne[0]["untergrenze_mib"]


def test_messe_prueft_eingaben() -> None:
    with pytest.raises(ValueError, match="Mindestens eine Datei"):
        sm.messe([], lade=synth_geladen)
    with pytest.raises(ValueError, match="paare"):
        sm.messe(["a.svd"], paare=-1, lade=synth_geladen)


def test_tabelle_hat_zeile_je_messung_und_summe() -> None:
    werte = sm.messe(["a.svd", "b.svd"], rss=_Zaehler(2.0), lade=synth_geladen)
    text = sm.tabelle(werte)
    assert text.count("\n") == 3 and "a.svd" in text and "b.svd" in text
    assert "Zuwachs insgesamt: 8.0 MiB bei 2 Messung(en)" in text


def test_rss_ist_positiv() -> None:
    assert sm.rss_mib() > 1.0


@pytest.mark.skipif(not DATEI.is_file(), reason="Messdatei nicht vorhanden")
def test_main_mit_beispieldatei_schreibt_json(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    ziel = tmp_path / "speicher.json"
    assert sm.main([str(DATEI), "--wiederholen", "2", "--json", str(ziel)]) == 0
    aus = capsys.readouterr().out
    assert "Zuwachs insgesamt" in aus
    inhalt = json.loads(ziel.read_text(encoding="utf-8"))
    assert len(inhalt["messungen"]) == 2 and inhalt["messungen"][0]["paare"] == 2
    assert inhalt["messungen"][1]["untergrenze_mib"] > 20.0  # 135 Punkte, 1600 Linien


def test_main_prueft_argumente(tmp_path: Path) -> None:
    with pytest.raises(SystemExit):
        sm.main([str(tmp_path / "fehlt.svd")])
    with pytest.raises(SystemExit):
        sm.main(["x.svd", "--wiederholen", "0"])
