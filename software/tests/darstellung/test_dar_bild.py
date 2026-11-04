"""Arbeitsbild mit Stempel aus derselben Zeichenfunktion (UI-17, UI-18; P-AUSW T2)."""

from __future__ import annotations

from pathlib import Path

import dar_daten as dd
import pytest
from matplotlib.figure import Figure

from ldv_automation.darstellung.auswahl import PaarCache, SpektrumDaten, spektrum_daten
from ldv_automation.darstellung.bild import (
    ARBEITSANSICHT,
    baue_stempel,
    neue_figure,
    speichere_arbeitsbild,
)
from ldv_automation.darstellung.spektrum import SpektrumOptionen, zeichne_spektrum
from ldv_automation.darstellung.stil import THESIS_STIL, Plotstil

STIL = Plotstil(haupt="#0B5C73")


@pytest.fixture(scope="module")
def sd() -> SpektrumDaten:
    md = dd.synthetische_messdaten()
    return spektrum_daten(md, PaarCache(md), punkt=None)


def test_stempel_text_und_hinweis_unbestaetigt() -> None:
    s = baue_stempel(dateiname="a.svd", ansicht="Ansicht 4 Schwingform", git_hash="abc123")
    assert s.zeilen == (f"{ARBEITSANSICHT} · a.svd · Ansicht 4 Schwingform · abc123",)
    assert ARBEITSANSICHT == "Arbeitsansicht – nicht für die Thesis"
    m = baue_stempel(dateiname="a.svd", ansicht="x", git_hash=None, unbestaetigt=("M8",))
    assert m.zeilen[0].endswith("Git-Hash unbekannt")
    assert m.zeilen[1] == "⚠ enthält unbestätigte Größen (M8)"
    m2 = baue_stempel(
        dateiname="a", ansicht="x", git_hash="h", unbestaetigt=("M8", "M5"), warn_symbol="!"
    )
    assert m2.zeilen[1] == "! enthält unbestätigte Größen (M8, M5)"


def test_arbeitsbild_png_mit_stempel_thesis_variante_ohne(
    sd: SpektrumDaten, tmp_path: Path
) -> None:
    stempel = baue_stempel(
        dateiname="mess.svd", ansicht="Ansicht 1", git_hash="deadbeef", unbestaetigt=("M8",)
    )
    ziel = tmp_path / "arbeit.png"
    z = speichere_arbeitsbild(
        lambda fig: zeichne_spektrum(fig, sd, SpektrumOptionen(), STIL), ziel, stempel, STIL
    )
    assert ziel.read_bytes()[:8] == b"\x89PNG\r\n\x1a\n"
    texte = z.alle_texte()
    assert stempel.zeilen[0] in texte and stempel.zeilen[1] in texte  # UI-17: Stempel im Bild
    # Thesis-Variante: dieselbe Zeichenfunktion ohne Stempel (Test: Figure-Texte)
    thesis = zeichne_spektrum(neue_figure(THESIS_STIL), sd, SpektrumOptionen(), THESIS_STIL)
    assert not any("Arbeitsansicht" in t or "unbestätigt" in t for t in thesis.alle_texte())
    # gleiche Linienzahl und Achsentexte in beiden (UI-18)
    assert len(thesis.linien) == len(z.linien)
    assert [(a.get_xlabel(), a.get_ylabel()) for a in thesis.achsen] == [
        (a.get_xlabel(), a.get_ylabel()) for a in z.achsen
    ]


def test_arbeitsbild_pdf_und_bildschirmfigur_bleibt_unveraendert(
    sd: SpektrumDaten, tmp_path: Path
) -> None:
    bildschirm = Figure()
    vorher = zeichne_spektrum(bildschirm, sd, SpektrumOptionen(), STIL)
    texte_vorher = vorher.alle_texte()
    ziel = tmp_path / "arbeit.PDF"
    speichere_arbeitsbild(
        lambda fig: zeichne_spektrum(fig, sd, SpektrumOptionen(), STIL),
        ziel,
        baue_stempel(dateiname="a", ansicht="b", git_hash="c"),
        STIL,
    )
    assert ziel.read_bytes()[:5] == b"%PDF-"
    assert (
        vorher.alle_texte() == texte_vorher and not bildschirm.texts
    )  # kein Stempel am Bildschirm


def test_arbeitsbild_uebernimmt_den_zoom(sd: SpektrumDaten, tmp_path: Path) -> None:
    z = speichere_arbeitsbild(
        lambda fig: zeichne_spektrum(fig, sd, SpektrumOptionen(), STIL),
        tmp_path / "z.png",
        baue_stempel(dateiname="a", ansicht="b", git_hash="c"),
        STIL,
        grenzen={0: ((5.0, 12.0), (1e-4, 1e-1))},
        dpi=50,
    )
    assert z.achsen[0].get_xlim() == (5.0, 12.0)
    assert z.achsen[0].get_ylim() == (1e-4, 1e-1)
    teil = speichere_arbeitsbild(
        lambda fig: zeichne_spektrum(fig, sd, SpektrumOptionen(), STIL),
        tmp_path / "t.png",
        baue_stempel(dateiname="a", ansicht="b", git_hash="c"),
        STIL,
        grenzen={0: ((6.0, 7.0), None)},
        dpi=50,
    )
    assert teil.achsen[0].get_xlim() == (6.0, 7.0)
    assert teil.achsen[0].get_ylim() != (1e-4, 1e-1)  # y unverändert


def test_arbeitsbild_formatfehler(sd: SpektrumDaten, tmp_path: Path) -> None:
    with pytest.raises(ValueError, match="nicht unterstützt"):
        speichere_arbeitsbild(
            lambda fig: zeichne_spektrum(fig, sd, SpektrumOptionen(), STIL),
            tmp_path / "x.jpg",
            baue_stempel(dateiname="a", ansicht="b", git_hash="c"),
            STIL,
        )
    assert not (tmp_path / "x.jpg").exists()
