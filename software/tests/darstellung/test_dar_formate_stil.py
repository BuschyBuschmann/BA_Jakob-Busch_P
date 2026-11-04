"""Formate (Dezimalkomma, Einheiten, Grad) und Plotstil (P-AUSW T2)."""

from __future__ import annotations

import math

import numpy as np
import pytest
from matplotlib.figure import Figure

from ldv_automation.darstellung.formate import (
    MINUS,
    achsentitel,
    dezimalkomma_formatter,
    frequenz_text,
    grad,
    kennzeichen_unbestaetigt,
    tick_text,
    winkel_text,
    zahl_signifikant_text,
    zahl_text,
)
from ldv_automation.darstellung.stil import LINIENARTEN, THESIS_STIL, ZYKLISCHE_SKALA, Plotstil

# --- formate ----------------------------------------------------------------------------------


@pytest.mark.parametrize(
    ("wert", "stellen", "soll"),
    [
        (0.5, None, "0,5"),
        (1234.5, None, "1234,5"),
        (0.0, None, "0"),
        (-1.25, 2, f"{MINUS}1,25"),
        (3.0, 2, "3,00"),
        (1e-5, None, "10⁻⁵"),
        (2e-5, None, "2·10⁻⁵"),
        (8.5e-5, None, "8,5·10⁻⁵"),
        (0.001, None, "0,001"),
        (1e-4, None, "10⁻⁴"),
        (1e6, None, "10⁶"),
        (float("nan"), None, "–"),
        (float("inf"), None, "∞"),
        (float("-inf"), None, f"{MINUS}∞"),
    ],
)
def test_zahl_text(wert: float, stellen: int | None, soll: str) -> None:
    assert zahl_text(wert, stellen) == soll


def test_zahl_text_dezimalpunkt_wenn_gewuenscht() -> None:
    assert zahl_text(0.5, dezimalkomma=False) == "0.5"


def test_tick_text_und_formatter_liefern_dezimalkomma() -> None:
    assert tick_text(0.25) == "0,25"
    fmt = dezimalkomma_formatter()
    assert fmt(0.75, 0) == "0,75"
    assert dezimalkomma_formatter(dezimalkomma=False)(0.75, 0) == "0.75"


def _tick_labels(grenzen: tuple[float, float], skala: str) -> list[str]:
    fig = Figure()
    ax = fig.subplots()
    ax.plot([1.0, 2.0], list(grenzen))
    ax.set_yscale(skala)
    ax.yaxis.set_major_formatter(dezimalkomma_formatter())
    fig.draw_without_rendering()
    unten, oben = ax.get_ylim()
    positionen = ax.get_yticks()
    return [
        t.get_text()
        for p, t in zip(positionen, ax.get_yticklabels(), strict=True)
        if unten <= p <= oben and t.get_text()
    ]


def test_tickformat_ist_je_achse_einheitlich() -> None:
    """Fachabnahme m-8: nicht „0,001“ neben „10⁻⁴“ an derselben Achse."""
    for grenzen, skala in (
        ((1e-4, 1.0), "log"),
        ((1e-12, 1e-3), "log"),
        ((0.0, 5e-4), "linear"),
        ((0.0, 0.0015), "linear"),
        ((1e-3, 10.0), "log"),
        ((0.0, 1.0), "linear"),
    ):
        texte = _tick_labels(grenzen, skala)
        potenz = ["10" in t and any(c in t for c in "⁰¹²³⁴⁵⁶⁷⁸⁹") for t in texte if t != "0"]
        assert texte and (all(potenz) or not any(potenz)), (grenzen, skala, texte)
    assert _tick_labels((1e-4, 1.0), "log")[0].startswith("10")  # Potenzschreibweise
    assert _tick_labels((1e-3, 10.0), "log") == ["0,001", "0,01", "0,1", "1", "10"]
    assert _tick_labels((0.0, 1.0), "linear")[1] == "0,2"


def test_zahl_text_erzwingt_schreibweise() -> None:
    assert zahl_text(0.005, None, wissenschaftlich=True) == "5·10⁻³"
    assert zahl_text(1.0, None, wissenschaftlich=True) == "10⁰"
    assert zahl_text(0.0, None, wissenschaftlich=True) == "0"
    assert zahl_text(2e-5, None, wissenschaftlich=False) == "0,00002"


@pytest.mark.parametrize(
    ("wert", "soll"),
    [
        (0.005814, "0,0058"),  # ζ der Referenzspitze
        (1.2345e-4, "0,00012"),  # MINOR-3: kein „0,0000“ für kleine Werte
        (0.5, "0,50"),
        (12.345, "12"),
        (0.0, "0"),
        (float("nan"), "–"),
        (float("inf"), "∞"),
    ],
)
def test_zahl_signifikant_text(wert: float, soll: str) -> None:
    assert zahl_signifikant_text(wert, 2) == soll
    assert zahl_signifikant_text(-0.005814, 2) == MINUS + "0,0058"
    assert zahl_signifikant_text(0.005814, 2, dezimalkomma=False) == "0.0058"
    with pytest.raises(ValueError, match="≥ 1"):
        zahl_signifikant_text(1.0, 0)


def test_frequenz_text_und_achsentitel() -> None:
    assert frequenz_text(123.75) == "123,75 Hz"
    assert frequenz_text(0.625) == "0,625 Hz"
    assert frequenz_text(1000.0) == "1000 Hz"
    assert achsentitel("Amplitude", "m/s") == "Amplitude [m/s]"
    assert achsentitel("Kohärenz", "1") == "Kohärenz [1]"


def test_grad_und_winkel_text() -> None:
    np.testing.assert_allclose(grad([0.0, math.pi / 2, -math.pi]), [0.0, 90.0, -180.0], rtol=1e-15)
    assert winkel_text(math.pi / 4) == "45,0°"
    assert winkel_text(-math.pi / 2) == f"{MINUS}90,0°"
    assert winkel_text(-1e-9) == "0,0°"  # kein negatives Null „-0,0°“
    assert winkel_text(float("nan")) == "–"
    assert winkel_text(0.1, 2) == "5,73°"


def test_kennzeichen_unbestaetigt() -> None:
    assert kennzeichen_unbestaetigt([]) == "unbestätigt"
    assert kennzeichen_unbestaetigt(["M8: Polarität offen"]) == "unbestätigt (M8: Polarität offen)"
    assert kennzeichen_unbestaetigt(["a", "b"]) == "unbestätigt (a; b)"


# --- stil -------------------------------------------------------------------------------------


def test_linienarten_paarweise_verschieden() -> None:
    assert len(set(LINIENARTEN)) == len(LINIENARTEN) == 4
    stil = Plotstil()
    assert len({stil.linienart(i) for i in range(4)}) == 4
    assert stil.linienart(4) == stil.linienart(0)  # zyklisch


def test_stil_prueft_eingaben() -> None:
    with pytest.raises(ValueError, match="paarweise verschieden"):
        Plotstil(linienarten=("-", "-"))
    with pytest.raises(ValueError, match="serienfarben"):
        Plotstil(serienfarben=())
    with pytest.raises(ValueError, match="schrift_pt"):
        Plotstil(schrift_pt=0.0)


def test_thesis_stil_ist_grau_und_neun_punkt() -> None:
    assert THESIS_STIL.schrift_pt == 9.0
    farben = (*THESIS_STIL.serienfarben, THESIS_STIL.haupt, THESIS_STIL.gitter, THESIS_STIL.band)
    for farbe in farben:
        r, g, b = farbe[1:3], farbe[3:5], farbe[5:7]
        assert r == g == b, f"{farbe} ist nicht grau (Graustufendruck, kein Gelb)"


def test_verlauf_geht_von_hell_nach_haupt() -> None:
    stil = Plotstil(haupt="#000000", verlauf_hell="#FFFFFF")
    cmap = stil.verlauf()
    assert cmap(0.0)[:3] == (1.0, 1.0, 1.0)
    assert cmap(1.0)[:3] == (0.0, 0.0, 0.0)


def test_zyklische_skala_ist_geschlossen_und_kein_regenbogen() -> None:
    assert ZYKLISCHE_SKALA not in ("hsv", "jet", "rainbow", "gist_rainbow")
    cmap = Plotstil().zyklisch()
    assert cmap.name == ZYKLISCHE_SKALA
    # gleiche Farbe bei -180° und +180°: keine Unstetigkeit am Umbruch (RF-UI-F4c)
    # twilight: Anfang und Ende unterscheiden sich um höchstens 3e-3 je Farbkanal
    # (gemessen 2,3e-3, nicht sichtbar)
    np.testing.assert_allclose(cmap(0.0), cmap(1.0), rtol=0, atol=3e-3)


def test_rc_enthaelt_schrift_und_ist_unabhaengig_vom_globalen_zustand() -> None:
    import matplotlib

    vorher = dict(matplotlib.rcParams)
    rc = Plotstil(schrift_pt=11.0, schriftfamilie=("Segoe UI", "DejaVu Sans")).rc()
    assert rc["font.size"] == 11.0
    assert rc["font.sans-serif"] == ["Segoe UI", "DejaVu Sans"]
    assert dict(matplotlib.rcParams) == vorher  # rc() ändert nichts global
