"""Regression R-073 (P-AUSW2 S1): ohne ``achsen`` bleiben die Abbildungen unverändert (A5)."""

from __future__ import annotations

import json
from typing import Any

import matplotlib
import pytest
import regression_achsen_hilfen as rh

GOLDEN: dict[str, Any] = json.loads(rh.GOLDEN.read_text(encoding="utf-8"))


@pytest.mark.parametrize("name", sorted(GOLDEN["faelle"]))
def test_abbildung_ohne_achsen_ist_unveraendert(name: str) -> None:
    """Figure-Struktur (Grenzen, Skalen, Texte, Ticks, Daten-SHA) gleich der Referenz vor R-073.

    Die Referenz ``regression_achsen.json`` entstand vor der Änderung. Die PNG-Prüfsumme (bitgleich)
    gilt nur bei derselben matplotlib-Version, weil die Schriftdarstellung versionsabhängig ist.
    """
    with rh.isolierte_rc():  # unabhängig von rcParams anderer Tests
        ist = rh.fingerabdruck(rh.faelle()[name])
    soll = GOLDEN["faelle"][name]
    assert ist["achsen"] == soll["achsen"]  # Grenzen: exakt gleiche Gleitkommawerte (Toleranz 0)
    assert ist["texte"] == soll["texte"]
    if matplotlib.__version__ == GOLDEN["matplotlib"]:
        assert ist["png_sha256"] == soll["png_sha256"]
    else:  # pragma: no cover  (nur bei anderer matplotlib-Version)
        pytest.skip("PNG-Prüfsumme gilt nur für matplotlib " + GOLDEN["matplotlib"])
