"""Bildexport ist unabhängig von ``rcParams["figure.dpi"]`` (Paket K-HAERTUNG).

Zeichenfunktionen messen Beschriftungen in Pixeln bei der Figure-DPI (Punktlabels, Zoom der
Animation); ohne feste DPI der Export-Figures änderte eine fremde ``matplotlibrc`` (Container:
200 dpi) Label-Dichte und Bildinhalt. Je Ansicht und Format wird bei 100 und 200 dpi exportiert
und verglichen. PNG: byteidentisch. PDF: ``SOURCE_DATE_EPOCH`` legt ``CreationDate`` fest
(matplotlib liest die Variable), sonst enthält die Datei die Erstellzeit; danach ebenfalls
byteidentisch.
"""

from __future__ import annotations

from collections.abc import Callable
from pathlib import Path

import dar_daten as dd
import matplotlib
import pytest
from dar_animation_hilfen import lange_platte
from matplotlib.figure import Figure

from ldv_automation.darstellung.animation3d import (
    BLICK_VORGABEN,
    AnimationsOptionen,
    zeichne_animation,
)
from ldv_automation.darstellung.auswahl import (
    PaarCache,
    schwingform_daten,
    spektrum_daten,
    spitzen_daten_frf,
)
from ldv_automation.darstellung.bild import baue_stempel, speichere_arbeitsbild
from ldv_automation.darstellung.diagramm import DiagrammOptionen, zeichne_diagramm
from ldv_automation.darstellung.schwingform import SchwingformOptionen, zeichne_schwingform
from ldv_automation.darstellung.serien_daten import SerienSpec, loese_alle_auf
from ldv_automation.darstellung.spektrum import SpektrumOptionen, zeichne_spektrum
from ldv_automation.darstellung.spitzen import SpitzenOptionen, zeichne_spitzen
from ldv_automation.darstellung.stil import Plotstil
from ldv_automation.darstellung.zeichnung import Zeichnung

STIL = Plotstil(haupt="#0B5C73")
Zeichner = Callable[[Figure], Zeichnung]


def _faelle() -> dict[str, Zeichner]:
    md = dd.synthetische_messdaten()
    cache = PaarCache(md)
    sd = spektrum_daten(md, cache, punkt=None)
    pd = spitzen_daten_frf(cache, "Vib Z", "Ref1")
    sf = schwingform_daten(md, cache, 10.0, komponente="3D", referenz="Ref1")
    messungen = {1: (md, cache, "A", "a.svd"), 2: (md, cache, "B", "b.svd")}
    serien = loese_alle_auf(
        [
            SerienSpec(1, None, "spektrum", komponente="Z", slot=0),
            SerienSpec(2, None, "spektrum", komponente="Z", slot=1),
        ],
        messungen.get,
        anordnung="ueberlagert",
    )
    platte = lange_platte(2.25, 45, 9)
    opt_anim = AnimationsOptionen(punktlabels=True, blick=BLICK_VORGABEN["iso"])
    return {
        "ansicht1_spektrum": lambda f: zeichne_spektrum(f, sd, SpektrumOptionen(), STIL),
        "ansicht3_spitzen": lambda f: zeichne_spitzen(f, pd, SpitzenOptionen(), STIL),
        "ansicht4_schwingform": lambda f: zeichne_schwingform(f, sf, SchwingformOptionen(), STIL),
        "ansicht5_diagramm": lambda f: zeichne_diagramm(f, serien, DiagrammOptionen(), STIL),
        "animation_standbild": lambda f: zeichne_animation(f, platte, opt_anim, STIL),
    }


FAELLE = _faelle()


@pytest.mark.parametrize("endung", ["png", "pdf"])
@pytest.mark.parametrize("name", list(FAELLE))
def test_export_ist_bei_rc_figure_dpi_100_und_200_gleich(
    name: str, endung: str, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setenv("SOURCE_DATE_EPOCH", "1700000000")  # PDF: festes CreationDate
    inhalte: dict[float, bytes] = {}
    schritte: dict[float, object] = {}
    for dpi in (100.0, 200.0):
        monkeypatch.setitem(matplotlib.rcParams, "figure.dpi", dpi)
        ziel = tmp_path / f"{name}_{int(dpi)}.{endung}"
        z = speichere_arbeitsbild(
            FAELLE[name],
            ziel,
            baue_stempel(dateiname="a.svd", ansicht=name, git_hash="abc"),
            STIL,
        )
        inhalte[dpi] = ziel.read_bytes()
        schritte[dpi] = z.hilfsobjekte.get("punktlabels_schritt")
    assert schritte[100.0] == schritte[200.0]
    if name == "animation_standbild":
        assert schritte[100.0] not in (None, 0)  # Labels an und in Dichte-Rechnung beteiligt
    assert inhalte[100.0] == inhalte[200.0]
