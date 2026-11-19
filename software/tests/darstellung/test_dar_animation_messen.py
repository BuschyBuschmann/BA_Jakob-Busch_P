"""Messskript ``tools/auswertung/animation_messen.py`` ohne Qt (R-071, P-AUSW3 AN9: M5, M6)."""

from __future__ import annotations

import math
from pathlib import Path
from types import SimpleNamespace
from typing import cast

import animation_messen as am
import dar_daten as dd
import pytest

from ldv_automation.auswertung.laden import Geladen
from ldv_automation.darstellung.animation3d import BLICK_VORGABEN
from ldv_automation.darstellung.animation_daten import animation_daten
from ldv_automation.darstellung.auswahl import PaarCache
from ldv_automation.darstellung.stil import THESIS_STIL


class _Uhr:
    """Zeitquelle, die bei jedem Aufruf um ``schritt`` s weiterläuft."""

    def __init__(self, schritt: float) -> None:
        self.t = 0.0
        self.schritt = schritt

    def __call__(self) -> float:
        self.t += self.schritt
        return self.t


def test_statistik_median_und_maximum_in_millisekunden() -> None:
    median, maximum = am.statistik([0.001, 0.003, 0.002, 0.010])
    assert median == pytest.approx(2.5, rel=1e-12)  # Median (2 ms, 3 ms) = 2,5 ms
    assert maximum == pytest.approx(10.0, rel=1e-12)
    with pytest.raises(ValueError, match="Keine Zeiten"):
        am.statistik([])


def test_messe_daten_m5_zeiten_aus_injizierter_uhr_und_speicher() -> None:
    md = dd.synthetische_messdaten()
    # Uhr mit 5 ms je Aufruf: jede Wiederholung liest sie zweimal, Dauer = 1 Schritt = 5 ms
    zeilen, anim = am.messe_daten(md, 10.0, 3, uhr=_Uhr(0.005), rss=_Uhr(2.0))
    assert [z.nr for z in zeilen] == ["M5", "M5", "M5"]
    kalt, warm, speicher = zeilen
    assert kalt.median_ms == pytest.approx(5.0, rel=1e-9) and kalt.n == 3
    assert warm.median_ms == pytest.approx(5.0, rel=1e-9) and warm.max_ms == pytest.approx(5.0)
    assert speicher.median_ms is None and "2,0 MiB" in speicher.notiz
    # die Daten sind die der Animation bei der gewählten Linie (Linie bei 10,0 Hz)
    assert anim.f_hz == pytest.approx(10.0)
    ref = animation_daten(md, PaarCache(md, groesse=3), 10.0)
    assert anim.d_ref == pytest.approx(ref.d_ref, rel=1e-12)
    with pytest.raises(ValueError, match="wiederholungen"):
        am.messe_daten(md, 10.0, 0)


def test_messe_speichern_m6_schreibt_png_und_pdf_und_meldet_die_groesse(tmp_path: Path) -> None:
    md = dd.synthetische_messdaten()
    _zeilen, anim = am.messe_daten(md, 10.0, 1)
    zeilen = am.messe_speichern(anim, THESIS_STIL, 2, ordner=tmp_path)
    assert [z.name for z in zeilen] == ["Standbild speichern (PNG)", "Standbild speichern (PDF)"]
    assert all(z.nr == "M6" and z.n == 2 and (z.median_ms or 0.0) > 0.0 for z in zeilen)
    assert (tmp_path / "animation_messen.png").read_bytes()[:4] == b"\x89PNG"
    assert (tmp_path / "animation_messen.pdf").read_bytes()[:4] == b"%PDF"
    assert "KiB" in zeilen[0].notiz


def test_waehle_frequenz_ist_die_mitte_der_achse() -> None:
    md = dd.synthetische_messdaten()
    assert am.waehle_frequenz(md) == pytest.approx(float(md.frequenz_hz[md.frequenz_hz.size // 2]))
    assert math.isfinite(am.waehle_frequenz(md))


def test_tabellen_text_und_markdown_nennen_kopf_und_alle_zeilen() -> None:
    md = dd.synthetische_messdaten()
    zeilen, _anim = am.messe_daten(md, 10.0, 1)
    kopf = am.umgebung("/x/messung.svd", "Messrechner", "remotedesktop", 10.0, mit_qt=False)
    assert kopf["datei"] == "messung.svd" and kopf["sitzungsart"] == "remotedesktop"
    assert {"python", "numpy", "matplotlib", "rechner", "frequenz_hz"} <= kopf.keys()
    text = am.tabelle_text(kopf, zeilen)
    assert "sitzungsart: remotedesktop" in text and text.count("M5") == 3
    md_text = am.tabelle_markdown(kopf, zeilen)
    assert "- **rechner:** Messrechner" in md_text
    assert md_text.count("| M5 |") == 3 and "| Nr | Messpunkt | Median [ms]" in md_text
    assert "–" in md_text  # Speicherzeile ohne Zeit


def test_messe_alles_ohne_qt_liefert_m5_und_m6_sortiert() -> None:
    md = dd.synthetische_messdaten()
    geladen = cast(Geladen, SimpleNamespace(messdaten=md))
    f, zeilen = am.messe_alles(geladen, THESIS_STIL, f_hz=10.0, wiederholungen=10, mit_qt=False)
    assert f == 10.0
    assert [z.nr for z in zeilen] == ["M5", "M5", "M5", "M6", "M6"]
    assert all(z.n == 3 for z in zeilen[:2])  # wiederholungen // 10, mindestens 3


def test_blick_fuer_schritt_ohne_drehung_ist_der_ausgangsblick() -> None:
    """Review MINOR 2: ohne Drehung bleibt der Blick, nicht Azimut 0° (Klammerfehler)."""
    basis = BLICK_VORGABEN["iso"]
    assert am.blick_fuer_schritt(basis, 17, drehen=False) == basis
    gedreht = am.blick_fuer_schritt(basis, 17, drehen=True)
    assert gedreht.azim_grad == pytest.approx(basis.azim_grad + 17.0)
    assert gedreht.elev_grad == basis.elev_grad and gedreht.zoom == basis.zoom
    assert am.blick_fuer_schritt(basis, 90, drehen=True) == basis  # i mod 90


def test_wiederhole_waermt_ausserhalb_der_zeitmessung_auf() -> None:
    aufrufe: list[int] = []
    zeiten = am._wiederhole(3, aufrufe.append, _Uhr(0.001), aufwaermen=True)
    assert aufrufe == [0, 0, 1, 2] and len(zeiten) == 3
    aufrufe.clear()
    am._wiederhole(3, aufrufe.append, _Uhr(0.001))
    assert aufrufe == [0, 1, 2]
