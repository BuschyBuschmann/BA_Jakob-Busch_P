"""Kennzeichen „unbestätigt“ als Kopfzeile: im Bild, nie über Daten oder Rand (K-AUSW-T3b).

Der Kasten liegt vollständig in der Figure und überdeckt keine Achsenfläche (Ansicht 2:
Phasen-Teilbild, Ansicht 4: Kopfzeile über den Achsen).
"""

from __future__ import annotations

import dar_daten as dd
import pytest
from matplotlib.figure import Figure

from ldv_automation.auswertung.daten import Messdaten
from ldv_automation.darstellung.auswahl import PaarCache, frf_daten, schwingform_daten
from ldv_automation.darstellung.frf import FrfOptionen, zeichne_frf
from ldv_automation.darstellung.schwingform import SchwingformOptionen, zeichne_schwingform
from ldv_automation.darstellung.stil import THESIS_STIL, Plotstil
from ldv_automation.darstellung.zeichnung import kennzeichen_kopf

KURZ = "unbestätigt (M8: Polarität der Referenzkanäle offen)"
LANG = "unbestätigt (M8: " + "sehr langer Grund der Annahme, " * 8 + "Ende)"
MITTEL = "unbestätigt (M8: Polarität der Referenzkanäle offen, Formel s_c·s_a·s_b)"
UI = Plotstil(warn_bg="#FFF1CC", warn_rand="#8A5A00")
STILE = [UI, THESIS_STIL]


@pytest.fixture(scope="module")
def daten() -> Messdaten:
    return dd.synthetische_messdaten()


@pytest.fixture(scope="module")
def cache(daten: Messdaten) -> PaarCache:
    return PaarCache(daten)


def _kasten(z, symbol_text: str):  # type: ignore[no-untyped-def]
    treffer = [t for t in z.texte if "unbestätigt" in t.get_text() or "unsicher" in t.get_text()]
    assert treffer, [t.get_text() for t in z.texte]
    return treffer


def _pruefe_lage(z) -> None:  # type: ignore[no-untyped-def]
    fig = z.figure
    fig.draw_without_rendering()
    figbox = fig.bbox
    for t in z.texte:
        if "unbestätigt" not in t.get_text() and "unsicher" not in t.get_text():
            continue
        box = (
            t.get_bbox_patch().get_window_extent() if t.get_bbox_patch() else t.get_window_extent()
        )
        assert box.x0 >= figbox.x0 - 0.5 and box.x1 <= figbox.x1 + 0.5, (
            "Kasten ragt seitlich heraus"
        )
        assert box.y0 >= figbox.y0 - 0.5 and box.y1 <= figbox.y1 + 0.5, "Kasten ragt oben heraus"
        for ax in z.achsen:
            a = ax.get_window_extent()
            ueberlappt = box.x0 < a.x1 and a.x0 < box.x1 and box.y0 < a.y1 and a.y0 < box.y1
            assert not ueberlappt, "Kasten überdeckt eine Achsenfläche"


@pytest.mark.parametrize("stil", STILE)
@pytest.mark.parametrize("text", [KURZ, MITTEL])
def test_ansicht_2_kasten_in_figure_und_ausserhalb_der_achsen(
    daten: Messdaten, cache: PaarCache, stil: Plotstil, text: str
) -> None:
    fd = frf_daten(cache, "Vib Z", "Ref1", punkt=1)
    fig = Figure(figsize=(11.5 / 2.54, 7.0 / 2.54) if stil is THESIS_STIL else (12.0, 7.4))
    z = zeichne_frf(fig, fd, FrfOptionen(phase=True, kennzeichen_phase=text), stil)
    assert any(stil.warn_symbol in t.get_text() for t in _kasten(z, text))
    _pruefe_lage(z)


@pytest.mark.parametrize("stil", STILE)
@pytest.mark.parametrize("text", [KURZ, LANG])
@pytest.mark.parametrize("groesse", [(12.0, 7.4), (11.5 / 2.54, 15.0 / 2.54)])
def test_ansicht_4_kasten_in_kopfzeile_innerhalb_der_figure(
    daten: Messdaten, cache: PaarCache, stil: Plotstil, text: str, groesse: tuple[float, float]
) -> None:
    sd = schwingform_daten(daten, cache, 10.0, komponente="Z")
    z = zeichne_schwingform(
        Figure(figsize=groesse),
        sd,
        SchwingformOptionen(darstellung="phase_ref", kennzeichen_phase=text),
        stil,
    )
    assert any(stil.warn_symbol in t.get_text() for t in _kasten(z, text))
    _pruefe_lage(z)
    # der Kasten steht über der Plotachse (Kopfzeile), nicht daneben
    kasten = _kasten(z, text)[0].get_window_extent()
    assert kasten.y0 >= z.achsen[0].get_window_extent().y1 - 0.5


def test_kasten_text_enthaelt_kurztext_ohne_formel(daten: Messdaten, cache: PaarCache) -> None:
    sd = schwingform_daten(daten, cache, 10.0, komponente="Z")
    z = zeichne_schwingform(
        Figure(), sd, SchwingformOptionen(darstellung="phase_ref", kennzeichen_phase=KURZ), UI
    )
    assert f"{UI.warn_symbol} {KURZ}" in z.alle_texte()
    assert "s_c" not in " ".join(z.alle_texte())  # Vorzeichenformel der Annahme steht nicht im Bild


def test_kennzeichen_kopf_ohne_texte_aendert_nichts() -> None:
    fig = Figure()
    kaesten, rect = kennzeichen_kopf(fig, UI, [], (0.0, 0.1, 1.0, 0.9))
    assert kaesten == [] and rect == (0.0, 0.1, 1.0, 0.9)


def test_kennzeichen_kopf_mehrere_kaesten_stapeln_und_verkleinern_das_rechteck() -> None:
    fig = Figure(figsize=(6.0, 4.0))
    kaesten, rect = kennzeichen_kopf(fig, UI, ["eins", "zwei"], (0.0, 0.0, 1.0, 1.0))
    assert len(kaesten) == 2 and rect[3] < 1.0 and rect[1] == 0.0
    fig.draw_without_rendering()
    oben, unten = (k.get_window_extent() for k in kaesten)
    assert oben.y0 >= unten.y1 - 0.5  # untereinander, ohne Überlappung
    assert oben.y1 <= fig.bbox.y1
