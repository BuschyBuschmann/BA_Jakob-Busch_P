"""Messskript ``tools/auswertung/animation_messen.py``: M1 bis M4 an der Animationsfläche."""

from __future__ import annotations

from typing import Any

import animation_messen as am
import pytest
from gui_ausw_hilfen import synth_geladen

from ldv_automation.auswertung.annahmen import AnnahmenStufe2
from ldv_automation.darstellung.animation_daten import animation_daten
from ldv_automation.darstellung.auswahl import PaarCache
from ldv_automation.gui.plotstil import baue_plotstil

pytestmark = pytest.mark.gui


def test_messe_flaeche_liefert_m1_bis_m4_mit_zeiten(
    qtbot: object, monkeypatch: pytest.MonkeyPatch
) -> None:
    aufrufe: list[int] = []
    original = vars(am)["aktualisiere_animation"]

    def zaehle(*args: Any, **kwargs: Any) -> None:
        aufrufe.append(1)
        original(*args, **kwargs)

    monkeypatch.setattr(am, "aktualisiere_animation", zaehle)
    md = synth_geladen().messdaten
    daten = animation_daten(md, PaarCache(md, groesse=3), 16.0, annahmen2=AnnahmenStufe2())
    zeilen = am.messe_flaeche(daten, baue_plotstil(), 3, 0.3, bildraten=(10,))
    nummern = [z.nr for z in zeilen]
    assert nummern == ["M1"] * 4 + ["M2"] + ["M3"] + ["M4"] * 2
    for z in zeilen:
        if z.nr != "M2":
            assert z.n == 3 and z.median_ms is not None and z.median_ms > 0.0
            assert z.max_ms is not None and z.max_ms >= z.median_ms
    m2 = next(z for z in zeilen if z.nr == "M2")
    assert "Soll 10 Bildern/s" in m2.name and "effektiv" in m2.notiz
    assert len(aufrufe) == 4 * (3 + 1)  # vier M1-Zeilen mit je einem Aufwärm-Schritt davor
