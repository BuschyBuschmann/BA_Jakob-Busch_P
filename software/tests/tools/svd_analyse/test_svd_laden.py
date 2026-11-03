"""``lade_svd`` an synthetischen Streams (P-AUSW T1.3): Leser, SHA-256, Adapter, Einstellungen."""

from __future__ import annotations

import hashlib
from dataclasses import replace
from pathlib import Path

import numpy as np
import pytest
import svd_synth as syn

from ldv_automation.auswertung import svd_lesen as sl
from ldv_automation.auswertung.laden import (
    FENSTER_IN_DATEI_LESBAR,
    Dateieinstellungen,
    LadeFehler,
    lade_svd,
)
from ldv_automation.auswertung.svd_adapter import aus_svd_messung


def _datei(tmp_path: Path) -> Path:
    pfad = tmp_path / "synthetisch.svd"
    pfad.write_bytes(b"kein echter OLE-Container, nur Bytes fuer die SHA-256")
    return pfad


def _leser(strom: dict[str, bytes]):  # type: ignore[no-untyped-def]
    def lese(pfad: Path) -> sl.SvdMessung:
        return sl.lese_container(syn.FakeOle(strom), pfad)

    return lese


def test_lade_svd_einstellungen_aus_synthetischer_messung(tmp_path: Path) -> None:
    pfad = _datei(tmp_path)
    st, _ = syn.messung_stroeme(n=3, linien=4)
    geladen = lade_svd(pfad, leser=_leser(st))
    # fft(25·4, 4, 10): fs = 100 Hz, N = 10 → Δf = 10 Hz, Bandbreite 4 · 10 = 40 Hz
    assert geladen.einstellungen == Dateieinstellungen(
        bandbreite_hz=40.0,
        linien=4,
        delta_f_hz=10.0,
        abtastfrequenz_hz=100.0,
        mittelung=sl.Mittelung(2, 7),
        punkte=3,
        referenzen=(("Ref1", "N"),),
    )
    assert not FENSTER_IN_DATEI_LESBAR


def test_lade_svd_herkunft_mit_sha256_vor_dem_lesen_und_datei_unveraendert(
    tmp_path: Path,
) -> None:
    pfad = _datei(tmp_path)
    vorher = hashlib.sha256(pfad.read_bytes()).hexdigest()
    st, _ = syn.messung_stroeme()
    geladen = lade_svd(pfad, leser=_leser(st))
    herkunft = geladen.messdaten.herkunft
    assert herkunft is not None
    assert herkunft.sha256 == vorher
    assert herkunft.pfad == str(pfad.resolve())
    assert hashlib.sha256(pfad.read_bytes()).hexdigest() == vorher


def test_lade_svd_messdaten_entsprechen_dem_adapter(tmp_path: Path) -> None:
    pfad = _datei(tmp_path)
    st, _ = syn.messung_stroeme()
    messung = _leser(st)(pfad)
    erwartet = aus_svd_messung(messung, sha256="0" * 64)
    ist = lade_svd(pfad, leser=lambda _: messung).messdaten
    np.testing.assert_array_equal(ist.frequenz_hz, erwartet.frequenz_hz)
    assert ist.delta_f_hz == erwartet.delta_f_hz
    assert ist.einheiten == erwartet.einheiten
    for paar, werte in erwartet.cp.items():
        np.testing.assert_array_equal(ist.cp[paar], werte)
    for kanal, werte_ap in erwartet.ap.items():
        np.testing.assert_array_equal(ist.ap[kanal], werte_ap)


def test_lade_svd_ohne_mittelung_stream_ergibt_none(tmp_path: Path) -> None:
    st, _ = syn.messung_stroeme()
    del st["Info/DAQ_Settings_Fft/Average"]
    geladen = lade_svd(_datei(tmp_path), leser=_leser(st))
    assert geladen.einstellungen.mittelung is None


def test_lade_svd_datei_fehlt_meldet_pfad(tmp_path: Path) -> None:
    pfad = tmp_path / "gibt_es_nicht.svd"
    with pytest.raises(LadeFehler, match="nicht gefunden") as info:
        lade_svd(pfad)
    assert str(pfad) in str(info.value)


def test_lade_svd_verzeichnis_statt_datei(tmp_path: Path) -> None:
    with pytest.raises(LadeFehler) as info:
        lade_svd(tmp_path)
    assert str(tmp_path) in str(info.value)


def test_lade_svd_keine_ole_datei_meldet_pfad_und_grund(tmp_path: Path) -> None:
    pfad = _datei(tmp_path)
    with pytest.raises(LadeFehler) as info:
        lade_svd(pfad)  # echter Leser (olefile): „not an OLE2 structured storage file“
    text = str(info.value)
    assert "OLE" in text and text.count(str(pfad)) == 1  # Pfad genannt, nicht doppelt
    assert isinstance(info.value.__cause__, sl.SvdFormatFehler)


def test_lade_svd_formatfehler_des_lesers_wird_zu_ladefehler(tmp_path: Path) -> None:
    pfad = _datei(tmp_path)

    def kaputt(_: Path) -> sl.SvdMessung:
        raise sl.SvdFormatFehler("Stream fehlt: Info/Geometry/MeasPoints")

    with pytest.raises(LadeFehler, match="Stream fehlt: Info/Geometry/MeasPoints") as info:
        lade_svd(pfad, leser=kaputt)
    assert str(info.value).startswith(str(pfad))
    assert isinstance(info.value.__cause__, sl.SvdFormatFehler)


def test_lade_svd_verletzung_des_datenvertrags_wird_zu_ladefehler(tmp_path: Path) -> None:
    pfad = _datei(tmp_path)
    st, _ = syn.messung_stroeme()
    messung = replace(_leser(st)(pfad), baender={})  # ohne Banddaten keine Einheiten
    with pytest.raises(LadeFehler, match="Einheit fehlt"):
        lade_svd(pfad, leser=lambda _: messung)


def test_lade_svd_programmierfehler_werden_nicht_verschluckt(tmp_path: Path) -> None:
    def fehlerhaft(_: Path) -> sl.SvdMessung:
        raise KeyError("Programmierfehler")

    with pytest.raises(KeyError):
        lade_svd(_datei(tmp_path), leser=fehlerhaft)
