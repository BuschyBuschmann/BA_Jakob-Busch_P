"""Uhr und vorläufige Fehlerstrategie."""

from __future__ import annotations

import math
from datetime import datetime, timedelta
from pathlib import Path

import pytest
from ablauf_hilfen import messung

from ldv_automation.ablauf.fehlerstrategie import (
    FehlerArt,
    FehlerEreignis,
    FehlerReaktion,
    Fehlerstrategie,
    PausierenUndNachfragen,
)
from ldv_automation.ablauf.uhr import TESTUHR_START, Echtzeituhr, Testuhr, Uhr


def test_testuhr_stellt_vor_ohne_zu_warten() -> None:
    uhr = Testuhr()
    assert isinstance(uhr, Uhr)
    uhr.sleep(2.5)
    uhr.sleep(-1.0)
    assert uhr.monotonic() == 2.5  # exakt: Summe binär darstellbarer Werte
    assert uhr.jetzt() == TESTUHR_START + timedelta(seconds=2.5)
    with pytest.raises(ValueError):
        uhr.vorstellen(-0.1)
    with pytest.raises(ValueError):
        uhr.vorstellen(math.nan)
    with pytest.raises(ValueError):
        Testuhr(datetime(2026, 1, 1))


def test_echtzeituhr() -> None:
    uhr = Echtzeituhr()
    assert isinstance(uhr, Uhr)
    t0 = uhr.monotonic()
    uhr.sleep(0.0)
    uhr.sleep(-1.0)
    assert uhr.monotonic() >= t0
    assert uhr.jetzt().tzinfo is not None


def test_vorlaeufige_strategie_fragt_immer(tmp_path: Path) -> None:
    strategie = PausierenUndNachfragen()
    assert isinstance(strategie, Fehlerstrategie)
    assert "vorläufig" in strategie.bezeichnung
    for art in FehlerArt:
        ereignis = FehlerEreignis(
            art=art, text="x", messung=messung(tmp_path, "M"), gestartet=False
        )
        assert strategie.entscheide(ereignis) is FehlerReaktion.ANHALTEN_UND_FRAGEN
