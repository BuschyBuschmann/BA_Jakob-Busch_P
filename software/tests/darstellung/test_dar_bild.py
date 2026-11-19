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
from ldv_automation.darstellung.diagramm import DiagrammOptionen, zeichne_diagramm
from ldv_automation.darstellung.serien_daten import SerienSpec, loese_alle_auf
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


def test_stempel_zusatzzeilen_stehen_nach_der_kopfzeile_und_vor_der_warnzeile() -> None:
    s = baue_stempel(
        dateiname="a.svd",
        ansicht="Ansicht 4 Schwingform",
        git_hash="abc",
        unbestaetigt=("M12",),
        zusatz=("Animation · θ = 90,0°", "Blickrichtung: Azimut 10,0°"),
    )
    assert s.zeilen[0].startswith(ARBEITSANSICHT)
    assert s.zeilen[1:] == (
        "Animation · θ = 90,0°",
        "Blickrichtung: Azimut 10,0°",
        "⚠ enthält unbestätigte Größen (M12)",
    )
    ohne = baue_stempel(dateiname="a.svd", ansicht="x", git_hash="abc")
    assert len(ohne.zeilen) == 1  # ohne Zusatz unverändert


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


def test_stempel_mit_mehreren_dateien_nennt_ansicht_hash_und_je_datei_eine_zeile() -> None:
    s = baue_stempel(
        ansicht="Ansicht 5 Diagramm",
        git_hash="abc123",
        dateien=(("A", "ref_Mitte.svd"), ("B", "ref_Rand.svd")),
        unbestaetigt=("M8",),
    )
    assert s.zeilen == (
        f"{ARBEITSANSICHT} · Ansicht 5 Diagramm · abc123",
        "A: ref_Mitte.svd",
        "B: ref_Rand.svd",
        "⚠ enthält unbestätigte Größen (M8)",
    )
    ohne_hash = baue_stempel(ansicht="x", git_hash=None, dateien=(("A", "a.svd"),))
    assert ohne_hash.zeilen[0].endswith("Git-Hash unbekannt")
    # alte Aufrufe mit dateiname= bleiben gültig, ``dateien`` hat Vorrang
    beide = baue_stempel(dateiname="x.svd", ansicht="x", git_hash="h", dateien=(("A", "a.svd"),))
    assert "x.svd" not in beide.zeilen[0] and beide.zeilen[1] == "A: a.svd"
    with pytest.raises(ValueError, match="Dateinamen"):
        baue_stempel(ansicht="x", git_hash="h")


def test_diagramm_bild_traegt_den_stempel_die_zeichenfunktion_allein_nicht(
    tmp_path: Path,
) -> None:
    md = dd.synthetische_messdaten()
    cache = PaarCache(md)
    messungen = {1: (md, cache, "A", "a.svd"), 2: (md, cache, "B", "b.svd")}
    daten = loese_alle_auf(
        [
            SerienSpec(1, None, "spektrum", komponente="Z", slot=0),
            SerienSpec(2, None, "spektrum", komponente="Z", slot=1),
        ],
        messungen.get,
        anordnung="ueberlagert",
    )
    stempel = baue_stempel(
        ansicht="Ansicht 5 Diagramm",
        git_hash="abc123",
        dateien=(("A", "a.svd"), ("B", "b.svd")),
        unbestaetigt=("M8",),
    )
    z = speichere_arbeitsbild(
        lambda fig: zeichne_diagramm(fig, daten, DiagrammOptionen(), STIL),
        tmp_path / "d.png",
        stempel,
        STIL,
    )
    texte = z.alle_texte()
    assert all(zeile in texte for zeile in stempel.zeilen)
    ohne = zeichne_diagramm(neue_figure(THESIS_STIL), daten, DiagrammOptionen(), THESIS_STIL)
    reines = ohne.alle_texte()
    assert not any("Arbeitsansicht" in t or "unbestätigte Größen" in t for t in reines)
    assert "A: a.svd" not in reines and "B: b.svd" not in reines
    assert len(ohne.linien) == len(z.linien) == 2  # dieselbe Zeichnung mit und ohne Stempel
