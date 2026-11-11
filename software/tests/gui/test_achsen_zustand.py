"""Achsenzustand je Ansicht (R-073, P-AUSW2 S2; UI-3, UI-4, UI-6): Qt-frei, Standardlauf."""

from __future__ import annotations

import pytest

from ldv_automation.darstellung.achsen import AchsenOptionen, Bereich
from ldv_automation.gui.achsen_zustand import (
    ACHSEN_JE_ANSICHT,
    ACHSEN_NAMEN,
    AchsenZustand,
    ist_fest,
)


def test_voreinstellung_alles_auto_amplitude_log_frequenz_linear() -> None:
    z = AchsenZustand()
    for nr in ACHSEN_JE_ANSICHT:
        assert z.skala(nr, "betrag") == "log" and z.skala(nr, "frequenz") == "linear"  # UI-2
        assert all(z.bereich(nr, r).ist_auto for r in ACHSEN_JE_ANSICHT[nr])
        assert not z.hat_feste(nr)
    assert z.skala(2, "phase") == "linear"  # die Phase kennt nur linear
    assert set(ACHSEN_NAMEN) == {"frequenz", "betrag", "phase"}


def test_zustand_gilt_je_ansicht() -> None:
    z = AchsenZustand()
    z.setze_bereich(1, "frequenz", Bereich(5.0, 10.0))
    z.setze_skala(1, "betrag", "linear")
    assert z.bereich(2, "frequenz").ist_auto and z.bereich(3, "frequenz").ist_auto
    assert z.skala(2, "betrag") == "log" and z.skala(1, "betrag") == "linear"
    assert z.hat_feste(1) and not z.hat_feste(2)


def test_optionen_enthalten_bereiche_skala_und_rollen_der_ansicht() -> None:
    z = AchsenZustand()
    z.setze_bereich(2, "frequenz", Bereich(1.0, None))
    z.setze_bereich(2, "phase", Bereich(-90.0, 90.0))
    z.setze_skala(2, "frequenz", "log")
    opt = z.optionen(2)
    assert isinstance(opt, AchsenOptionen)
    assert opt.frequenz == Bereich(1.0, None) and opt.frequenz_skala == "log"
    assert opt.y_bereich("phase") == Bereich(-90.0, 90.0) and opt.y_bereich("betrag").ist_auto
    assert set(opt.y) == {"betrag", "phase"}  # Ansicht 2: Betrag und Phase
    assert set(z.optionen(1).y) == {"betrag"}
    assert z.optionen(4).y == {} and z.optionen(4).frequenz.ist_auto  # Ansicht 4: keine Achsenwahl


def test_uebernehme_grenzen_schreibt_feste_werte() -> None:
    z = AchsenZustand()
    z.uebernehme_grenzen(1, "betrag", 1e-6, 2.5)  # Zoom/Verschieben (F3)
    b = z.bereich(1, "betrag")
    assert b == Bereich(1e-6, 2.5) and ist_fest(b)
    assert isinstance(b.von, float)


def test_auf_auto_loescht_nur_die_bereiche_dieser_ansicht_und_behaelt_skalen() -> None:
    z = AchsenZustand()
    for nr in (1, 2):
        z.setze_bereich(nr, "frequenz", Bereich(1.0, 2.0))
        z.setze_bereich(nr, "betrag", Bereich(1.0, 2.0))
        z.setze_skala(nr, "frequenz", "log")
    z.auf_auto(1)  # „Alles auf Auto“ / Zurücksetzen (F3)
    assert not z.hat_feste(1) and z.hat_feste(2)
    assert z.skala(1, "frequenz") == "log"
    z.alles_auf_auto()
    assert not z.hat_feste(2) and z.skala(2, "frequenz") == "log"


def test_neue_datei_setzt_bereiche_zurueck_skalen_bleiben() -> None:
    z = AchsenZustand()
    z.setze_bereich(3, "betrag", Bereich(1.0, 9.0))
    z.setze_skala(3, "betrag", "linear")
    z.setze_skala(1, "frequenz", "log")
    z.bei_neuer_datei()  # UI-6
    assert z.bereich(3, "betrag").ist_auto
    assert z.skala(3, "betrag") == "linear" and z.skala(1, "frequenz") == "log"


def test_setze_skala_ungueltig() -> None:
    z = AchsenZustand()
    with pytest.raises(ValueError, match="keine wählbare Skala"):
        z.setze_skala(2, "phase", "log")
    with pytest.raises(ValueError, match="unbekannte Skala"):
        z.setze_skala(2, "betrag", "db")  # type: ignore[arg-type]
