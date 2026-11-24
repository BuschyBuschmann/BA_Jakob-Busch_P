"""BW-2: Start gesperrt bei Bandbreite außerhalb der PSV-Stufen (Sitzung, Simulator)."""

from __future__ import annotations

from pathlib import Path

import pytest
from test_sitzung_fassade import _set, _sitzung

from ldv_automation.ablauf.steuerung import DurchgangErgebnis
from ldv_automation.domaene.eintraege import Messung
from ldv_automation.geraet.simulator import SimulatorKonfiguration

STUFEN = (3125.0, 5000.0, 6250.0)


@pytest.mark.parametrize("soll_hz", [5600.0, 4000.0])
def test_a1_start_gesperrt_bei_nicht_stufe(tmp_path: Path, soll_hz: float) -> None:
    s, fabrik = _sitzung(tmp_path, konfiguration=SimulatorKonfiguration(bandbreiten_hz=STUFEN))
    assert s.zustandsbild().verbindung is not None
    assert s.zustandsbild().verbindung.bandbreiten_stufen_hz == STUFEN  # type: ignore[union-attr]
    s.einfuegen(
        0,
        Messung(
            name="M1",
            einstellungsdatei=_set(tmp_path),
            parameter={"fft.bandbreite_hz": soll_hz},
        ),
    )
    with pytest.raises(ValueError, match=rf"Bandbreite {soll_hz:g} Hz ist keine PSV-Stufe"):
        s.starte("sim")
    assert "lade_einstellungen" not in fabrik.erzeugt[0].aufgerufene_methoden()


def test_start_mit_stufe_6250_laeuft_durch(tmp_path: Path) -> None:
    s, _ = _sitzung(tmp_path, konfiguration=SimulatorKonfiguration(bandbreiten_hz=STUFEN))
    s.einfuegen(
        0,
        Messung(
            name="M1",
            einstellungsdatei=_set(tmp_path),
            parameter={"fft.bandbreite_hz": 6250.0},
        ),
    )
    s.starte("sim")
    s.verarbeite()
    assert s.zustandsbild().ergebnis is DurchgangErgebnis.VOLLSTAENDIG
