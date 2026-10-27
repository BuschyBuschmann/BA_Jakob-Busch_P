"""Gelesener Gerätestand und Generatorbewertung (U5/B1)."""

from __future__ import annotations

import os
from datetime import UTC, datetime
from pathlib import Path

import pytest

from ldv_automation.ablauf.geraetestand import (
    DateiKennung,
    EinstellungsKenntnis,
    GeneratorStand,
    GeraeteStand,
    Herkunft,
    generator_aus_stand,
    noch_gueltig,
    pfad_schluessel,
    uebertragbar,
)
from ldv_automation.geraet.schnittstelle import EinstellungsStand


@pytest.mark.parametrize(
    ("an", "aktiv", "anzahl", "ok"),
    [
        (False, False, 1, True),
        (None, False, None, True),
        (True, False, 1, False),
        (False, True, 1, False),
        (False, None, 1, False),
        (False, False, 2, False),
    ],
)
def test_unbedenklich_nur_wenn_gelesen_aus(
    an: bool | None, aktiv: bool | None, anzahl: int | None, ok: bool
) -> None:
    g = GeneratorStand(generatoren_an=an, aktiv=aktiv, amplitude_v=0.1, anzahl=anzahl)
    assert g.unbedenklich is ok


def test_generator_aus_stand_nimmt_rohwerte_nicht_zusammenfassung() -> None:
    # Adapter fasst ein unlesbares Active bei GeneratorsOn=False zu False zusammen; das
    # darf nicht als "aus" gelten.
    stand = EinstellungsStand(
        modus="Fft",
        generator_aktiv=False,
        gruppen={"generator": {"aktiv": None, "generatoren_an": False, "anzahl": 1}},
    )
    g = generator_aus_stand(stand)
    assert g.aktiv is None and g.generatoren_an is False and not g.unbedenklich
    voll = generator_aus_stand(
        EinstellungsStand(
            modus="Fft",
            gruppen={"generator": {"aktiv": False, "amplitude_v": 2, "anzahl": True}},
        )
    )
    assert voll.amplitude_v == 2.0 and voll.anzahl is None
    leer = generator_aus_stand(EinstellungsStand(modus="Fft"))
    assert leer == GeneratorStand(generatoren_an=None, aktiv=None, amplitude_v=None, anzahl=None)


def test_noch_gueltig_nach_stat(tmp_path: Path) -> None:
    datei = tmp_path / "a.set"
    datei.write_bytes(b"x")
    st = os.stat(datei)
    k = EinstellungsKenntnis(
        einstellungsdatei=str(datei),
        kennung=DateiKennung(sha256="0", groesse_b=st.st_size, mtime_ns=st.st_mtime_ns),
        stand=GeraeteStand(
            messpunkte=1,
            generator=GeneratorStand(generatoren_an=None, aktiv=False, amplitude_v=0, anzahl=1),
            quelle="t",
            zeit=datetime.now(UTC),
        ),
        herkunft=Herkunft(geraet_nr=1, betriebsart="simulator", lademaske=""),
    )
    assert noch_gueltig(k)
    datei.write_bytes(b"xy")
    assert not noch_gueltig(k)
    datei.unlink()
    assert not noch_gueltig(k)
    assert pfad_schluessel(str(tmp_path / "x" / ".." / "a.set")) == pfad_schluessel(str(datei))


def test_k_u5b_uebertragbar() -> None:
    com = Herkunft(geraet_nr=1, betriebsart="trockenlauf", lademaske="A", psv_prozesse="PSV.exe")
    messen = Herkunft(geraet_nr=2, betriebsart="messen", lademaske="A", psv_prozesse="PSV.exe")
    sim = Herkunft(geraet_nr=1, betriebsart="simulator", lademaske="")
    assert uebertragbar(com, com) and uebertragbar(sim, sim)
    assert uebertragbar(com, messen)
    assert not uebertragbar(Herkunft(geraet_nr=3, betriebsart="simulator", lademaske=""), messen)
    assert not uebertragbar(
        com, Herkunft(geraet_nr=2, betriebsart="messen", lademaske="B", psv_prozesse="PSV.exe")
    )
    assert not uebertragbar(
        com,
        Herkunft(geraet_nr=2, betriebsart="messen", lademaske="A", psv_prozesse="PSV.exe, PSV.exe"),
    )
    leer = Herkunft(geraet_nr=1, betriebsart="trockenlauf", lademaske="A", psv_prozesse="")
    assert not uebertragbar(
        leer, Herkunft(geraet_nr=2, betriebsart="messen", lademaske="A", psv_prozesse="")
    )
    # gleiche Nummer, aber andere Angaben (kann nicht vorkommen): nicht übertragbar
    assert not uebertragbar(com, Herkunft(geraet_nr=1, betriebsart="messen", lademaske="A"))
