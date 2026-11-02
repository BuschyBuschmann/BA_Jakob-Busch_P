"""Tests für den Prototyp-Leser von PSV-Messdateien (Paket W2).

Synthetische Bytes: bekannte Werte rein, gleiche Werte raus. Die Werte durchlaufen wie in
der Datei float32; verglichen wird deshalb mit den auf float32 gerundeten Sollwerten und
``rtol=0``/``atol=0`` (die Dekodierung selbst darf nichts verändern, float32 -> float64 ist
exakt). Wo gerechnet wird (Plausibilitätsprüfung), gilt ``svd_pruefung.RTOL``.
"""

from __future__ import annotations

import datetime as dt
import hashlib
import struct
import zlib
from dataclasses import replace
from pathlib import Path

import kontrollplots as kp
import numpy as np
import olefile
import pytest
import svd_lesen as sl
import svd_pruefung as sp
import svd_synth as syn

ECHTE_DATEI = Path(__file__).resolve().parents[4] / "Input" / "20261012_ref_Mitte.svd"


def _messung() -> tuple[sl.SvdMessung, dict[str, np.ndarray]]:
    st, soll = syn.messung_stroeme()
    return sl.lese_container(syn.FakeOle(st), Path("synthetisch.svd")), soll


# --- Bausteine -------------------------------------------------------------------------


def test_filetime_bekannter_zeitpunkt() -> None:
    # FILETIME aus der echten Datei (Satz 0): 134362711867357552 · 100 ns ab 1601-01-01
    # = 2026-10-12 09:33:06.7357552 UTC; auf ganze µs abgeschnitten.
    assert sl.filetime_zu_datetime(0x01DD5A2CAFE97970) == dt.datetime(
        2026, 10, 12, 9, 33, 6, 735755
    )
    assert sl.filetime_zu_datetime(0).tzinfo is None  # Zeitzone offen: naiv
    for falsch in (-1, 2**63 - 1):  # 2**63-1: jenseits von datetime.max
        with pytest.raises(sl.SvdFormatFehler):
            sl.filetime_zu_datetime(falsch)


def test_utf16_zeichenketten_findet_texte_und_ueberspringt_rauschen() -> None:
    daten = b"\x01\x02" + syn.zk("Vib X") + struct.pack("<i", 2) + b"\x00\x00" + syn.zk("Ref1")
    daten += struct.pack("<i", 6) + "a\x00b".encode("utf-16-le")  # innere Null: kein Text
    daten += struct.pack("<i", 4) + b"\x00\xd8\x00\x00"  # ungültiges UTF-16
    assert [t for _, t in sl.utf16_zeichenketten(daten)] == ["Vib X", "Ref1"]


def test_signal_info() -> None:
    assert sl.dekodiere_signal_info(syn.signal_info(135, 12800)) == sl.SignalInfo(1, 135, 12800)
    for falsch in (b"\x00" * 11, syn.signal_info(1, 8, version=2), syn.signal_info(0, 8)):
        with pytest.raises(sl.SvdFormatFehler):
            sl.dekodiere_signal_info(falsch)


def test_strom_info_platzzuordnung() -> None:
    info = sl.dekodiere_strom_info(syn.strom_info(3, 1000, [2, 0, 1]))
    assert info == sl.StromInfo(1000, 3, (2, 0, 1))


@pytest.mark.parametrize(
    "daten",
    [
        b"\x00" * 7,
        struct.pack("<6i", 2, 1, -1, -1, 1, 0),
        struct.pack("<6i", 1, 1, -1, -1, 5, 0),
        struct.pack("<10i", 1, 9, -1, -1, 2, 1, 0, 2, 9, 0) + struct.pack("<4i", 9, 1, 2, -1),
        struct.pack("<11i", 1, 9, -1, -1, 2, 0, 1, 2, 9, 0, 9) + struct.pack("<3i", 0, 2, -1),
    ],
)
def test_strom_info_fehler(daten: bytes) -> None:
    with pytest.raises(sl.SvdFormatFehler):
        sl.dekodiere_strom_info(daten)


def test_punktdaten_ordnet_nach_punktindex() -> None:
    zeilen = np.arange(12, dtype=np.float32).reshape(3, 4) * np.float32(0.1)
    plaetze = [2, 0, 1]
    satz = sl.SATZ_DATEN + 16 + sl.SATZ_NACHSPANN
    daten = syn.punktdaten(zeilen, 2, plaetze, 10_000_000)
    pd = sl.dekodiere_punktdaten(
        daten, sl.StromInfo(satz, 3, tuple(plaetze)), sl.SignalInfo(1, 3, 16)
    )
    np.testing.assert_allclose(pd.werte, zeilen.astype(np.float64), rtol=0, atol=0)
    assert pd.werte.dtype == np.float64
    assert pd.linien == 2
    assert pd.zeit_a[1] - pd.zeit_a[0] == dt.timedelta(seconds=-2)  # Platz 0 vs. Platz 2
    assert pd.feld_34 == 0.64 and pd.platz == (2, 0, 1)


def _punktdaten_fall(aendern: str) -> tuple[bytes, sl.StromInfo, sl.SignalInfo]:
    zeilen = np.ones((2, 2), dtype=np.float32)
    plaetze = [0, 1]
    satz = sl.SATZ_DATEN + 8 + sl.SATZ_NACHSPANN
    daten = bytearray(syn.punktdaten(zeilen, 1, plaetze, 0))
    info = sl.StromInfo(satz, 2, (0, 1))
    sig = sl.SignalInfo(1, 2, 8)
    b1 = sl.DATENSTROM_KOPF + satz
    if aendern == "punkte":
        sig = sl.SignalInfo(1, 3, 8)
    elif aendern == "satzlaenge":
        info = sl.StromInfo(satz + 4, 2, (0, 1))
    elif aendern == "laenge":
        daten += b"\x00"
    elif aendern == "version":
        struct.pack_into("<i", daten, b1 + sl.SATZ_VERSION, 3)
    elif aendern == "nutzlaenge":
        struct.pack_into("<i", daten, b1 + sl.SATZ_NUTZLAENGE, 4)
    elif aendern == "linien":
        struct.pack_into("<i", daten, b1 + sl.SATZ_LINIEN, 7)
    elif aendern == "doppelt":
        struct.pack_into("<i", daten, b1 + sl.SATZ_PUNKT, 0)
    elif aendern == "platz":
        info = sl.StromInfo(satz, 2, (1, 0))
    elif aendern == "feld_34":
        struct.pack_into("<d", daten, b1 + sl.SATZ_FELD_34, 0.2)
    return bytes(daten), info, sig


@pytest.mark.parametrize(
    "aendern",
    [
        "punkte",
        "satzlaenge",
        "laenge",
        "version",
        "nutzlaenge",
        "linien",
        "doppelt",
        "platz",
        "feld_34",
    ],
)
def test_punktdaten_fehler(aendern: str) -> None:
    with pytest.raises(sl.SvdFormatFehler):
        sl.dekodiere_punktdaten(*_punktdaten_fall(aendern))


def test_verschraenkt_zu_komplex() -> None:
    z = sl.verschraenkt_zu_komplex(np.array([[1.0, -2.0, 3.5, 0.25]]))
    np.testing.assert_array_equal(z, np.array([[1 - 2j, 3.5 + 0.25j]]))
    assert z.dtype == np.complex128
    with pytest.raises(sl.SvdFormatFehler):
        sl.verschraenkt_zu_komplex(np.zeros((1, 3)))


def test_signalart_und_statische_info() -> None:
    assert sl.signalart(syn.F_CP) == "CP"
    assert sl.signalart("AVGSEQ[AVG[AP[S[T[3]]]]]") == "AP"
    with pytest.raises(sl.SvdFormatFehler):
        sl.signalart("XYZ")
    si = sl.dekodiere_statische_info(syn.static_info([syn.VIB, syn.REF], syn.F_CP))
    assert si == sl.StatischeInfo(("Vib X", "Ref1"), ("Vibrometer X", "Reference 1"), syn.F_CP)
    with pytest.raises(sl.SvdFormatFehler):
        sl.dekodiere_statische_info(syn.zk("Vib X"))
    with pytest.raises(sl.SvdFormatFehler):
        sl.dekodiere_statische_info(syn.zk("Vib X") + syn.zk(syn.F_CP))


def test_fft_einstellungen() -> None:
    """K-ACHSE: @4 = Abtastfrequenz 2500 Hz, N = 4000 -> Δf = 0,625 Hz, T = 1,6 s, BW 1000 Hz."""
    fft = sl.dekodiere_fft_einstellungen(syn.fft(2500.0, 1600, 4000))
    assert (fft.abtastfrequenz_hz, fft.linien, fft.abtastwerte) == (2500.0, 1600, 4000)
    assert (fft.startfrequenz_hz, fft.bandbreite_hz, fft.endfrequenz_hz) == (0.0, 1000.0, 1000.0)
    # 0,625 = 5/8 und 1,6 = 8/5 sind als Quotient zweier exakter Zahlen auf 1 ulp genau
    assert fft.delta_f_hz == pytest.approx(0.625, rel=1e-15, abs=0.0)
    assert fft.blockdauer_s == pytest.approx(1.6, rel=1e-15, abs=0.0)
    assert fft.delta_f_hz * fft.blockdauer_s == pytest.approx(1.0, rel=1e-15, abs=0.0)
    with pytest.raises(sl.SvdFormatFehler):
        sl.dekodiere_fft_einstellungen(b"\x00" * 52)
    with pytest.raises(sl.SvdFormatFehler, match="zu kurz"):
        sl.dekodiere_fft_einstellungen(syn.fft(2500.0, 1600, 4000)[:40])
    with pytest.raises(sl.SvdFormatFehler, match="unplausibel"):
        sl.dekodiere_fft_einstellungen(syn.fft(-1.0, 1600, 4000))


def test_fft_einstellungen_konsistenzpruefungen() -> None:
    with pytest.raises(sl.SvdFormatFehler, match="Startfrequenz"):  # Zoom ungeprüft
        sl.dekodiere_fft_einstellungen(syn.fft(2500.0, 1600, 4000, start_hz=100.0))
    with pytest.raises(sl.SvdFormatFehler, match="Endfrequenz"):
        sl.dekodiere_fft_einstellungen(syn.fft(2500.0, 1600, 4000, end_hz=1200.0))
    # Bandbreite/Linien (1250 Hz / 1600) passt nicht zu fs/N = 0,625 Hz
    with pytest.raises(sl.SvdFormatFehler, match="Bandbreite/Linien"):
        sl.dekodiere_fft_einstellungen(syn.fft(2500.0, 1600, 4000, bw_hz=1250.0))


def test_band_info_gegenprobe() -> None:
    fft = sl.dekodiere_fft_einstellungen(syn.fft(2500.0, 1600, 4000))
    assert sl.pruefe_band_info(syn.band_info(1600, 0.625, 1000.0), fft) == sl.BAND_INFO_GEPRUEFT
    # alte Fehldeutung 1,5625 / 2500, falsche Linienzahl, falsche Obergrenze: Widerspruch
    for fehl in (
        syn.band_info(1600, 1.5625, 2500.0),
        syn.band_info(7, 0.625, 1000.0),
        syn.band_info(1600, 0.625, 2500.0),
    ):
        assert sl.pruefe_band_info(fehl, fft) == sl.BAND_INFO_WIDERSPRUCH
    # Layout nicht erkannt -> nicht prüfbar, kein Fehler
    assert sl.pruefe_band_info(b"abc", fft) == sl.BAND_INFO_NICHT_PRUEFBAR
    unbekannt = struct.pack("<I", 4) + zlib.compress(b"abcd")
    assert sl.pruefe_band_info(unbekannt, fft) == sl.BAND_INFO_NICHT_PRUEFBAR
    assert (
        sl.pruefe_band_info(struct.pack("<I", 4) + b"kein zlib", fft) == sl.BAND_INFO_NICHT_PRUEFBAR
    )


def test_messpunkte() -> None:
    xyz = np.array([[0.1, 0.2, -0.3], [0.4, 0.5, -0.6]])
    mp = sl.dekodiere_messpunkte(syn.messpunkte([132, 161], xyz))
    np.testing.assert_array_equal(mp.index, [0, 1])
    np.testing.assert_array_equal(mp.label, [132, 161])
    np.testing.assert_allclose(mp.koordinaten_m, syn.f32(xyz), rtol=0, atol=0)
    np.testing.assert_array_equal(mp.statusfelder["geometrie_status"], [8193, 8193])
    for falsch in (b"\x00" * 10, syn.messpunkte([1], xyz[:1]) + b"\x00"):
        with pytest.raises(sl.SvdFormatFehler):
            sl.dekodiere_messpunkte(falsch)
    with pytest.raises(sl.SvdFormatFehler, match="eindeutig"):
        sl.dekodiere_messpunkte(syn.messpunkte([5, 5], xyz))


def test_elemente() -> None:
    assert sl.dekodiere_elemente(syn.elemente([(0, 1, 2, 3), (1, 2, 4)]), 5) == [
        (0, 1, 2, 3),
        (1, 2, 4),
    ]
    for falsch in (
        b"\x00" * 6,
        struct.pack("<2i", 2, 0),
        struct.pack("<2i", 1, 1),
        struct.pack("<4i", 1, 1, 1, 0),
        syn.elemente([(0, 1)]) + b"\x00" * 4,
    ):
        with pytest.raises(sl.SvdFormatFehler):
            sl.dekodiere_elemente(falsch)
    with pytest.raises(sl.SvdFormatFehler, match="außerhalb"):
        sl.dekodiere_elemente(syn.elemente([(0, 9)]), 5)


def test_punktmittel() -> None:
    werte = np.array([0.5, 1.25, 3.0])
    np.testing.assert_array_equal(sl.dekodiere_punktmittel(syn.punktmittel(werte), 3), werte)
    with pytest.raises(sl.SvdFormatFehler):
        sl.dekodiere_punktmittel(syn.punktmittel(werte), 4)


def test_band() -> None:
    werte = np.array([1.5, 2.5])
    b = sl.dekodiere_band(
        syn.band(
            "H1 Geschwindigkeit / Kraft",
            [("Vib X", "Geschwindigkeit", "m/s"), ("Ref1", "Kraft", "N")],
            "Geschwindigkeit / Kraft",
            "m/s / N",
            werte,
        ),
        2,
    )
    assert (b.titel, b.groesse, b.einheit) == (
        "H1 Geschwindigkeit / Kraft",
        "Geschwindigkeit / Kraft",
        "m/s / N",
    )
    assert b.kanaele == (("Vib X", "Geschwindigkeit", "m/s"), ("Ref1", "Kraft", "N"))
    np.testing.assert_array_equal(b.werte, werte)


@pytest.mark.parametrize("fall", ["kurz", "zlib", "laenge", "anzahl", "texte"])
def test_band_fehler(fall: str) -> None:
    gut = syn.band("T", [("K", "G", "E")], "G", "E", np.ones(2))
    daten = {
        "kurz": b"\x00\x00",
        "zlib": struct.pack("<I", 4) + b"kein zlib",
        "laenge": struct.pack("<I", 1) + gut[4:],
        "anzahl": gut,
        "texte": (lambda r: struct.pack("<I", len(r)) + zlib.compress(r))(
            syn.zk("nur") + struct.pack("<ii", 0x20, 2) + bytes(8)
        ),
    }[fall]
    with pytest.raises(sl.SvdFormatFehler):
        sl.dekodiere_band(daten, 3 if fall == "anzahl" else 2)


# --- Gesamter Leser mit synthetischem Container ---------------------------------------


def test_lese_container_liefert_bekannte_werte() -> None:
    m, soll = _messung()
    assert len(m.signale) == 5 and len(m.punktmittel) == 5 and len(m.baender) == 4
    np.testing.assert_array_equal(m.signale["M0"].werte, soll["cp"])
    np.testing.assert_array_equal(m.signale["M1"].werte, soll["cph"])
    np.testing.assert_array_equal(m.signale["M2"].werte, soll["apx"])
    np.testing.assert_array_equal(m.signale["M4"].werte, soll["abs"])
    assert m.signale["M0"].komplex and not m.signale["M2"].komplex
    assert m.signale["M0"].werte.dtype == np.complex128
    assert m.signale["M0"].einheit == "N * m/s"
    assert m.signale["M1"].einheit == "m/s"  # CPH: Banddaten nennen nur den Antwortkanal
    assert m.signale["M1"].kanaele == ("Vib X", "Ref1")
    assert m.signale["M3"].einheit is None  # keine Banddaten S3
    np.testing.assert_allclose(m.frequenz_hz, [10.0, 20.0, 30.0, 40.0], rtol=1e-15)
    np.testing.assert_array_equal(m.punkte.label, [100, 103, 106])
    assert m.elemente == [(0, 1, 2)]
    assert m.kanalgeraete_xml is not None and "50 mm/s" in m.kanalgeraete_xml
    assert m.hardware_texte == ("PSV-I-680", "1.13")
    text = sl.uebersicht(m)
    assert "Signale (Polytec_Data)" in text and "M0 CP" in text and "gesichert" in text


def test_lese_container_widerspruechliche_daten() -> None:
    st, _ = syn.messung_stroeme()
    st["Polytec_Data/M0/Static_Info"] = syn.static_info([syn.VIB], syn.F_APX)
    with pytest.raises(sl.SvdFormatFehler, match="widerspricht"):
        sl.lese_container(syn.FakeOle(st), Path("x"))
    st, _ = syn.messung_stroeme()
    st["Info/DAQ_Settings_Fft/Fft"] = syn.fft(
        125.0, 5, 10
    )  # in sich stimmig, aber 5 statt 4 Linien
    with pytest.raises(sl.SvdFormatFehler, match="Linien"):
        sl.lese_container(syn.FakeOle(st), Path("x"))
    st, _ = syn.messung_stroeme()
    del st["Polytec_Data/M0/Signal_Info"]
    with pytest.raises(sl.SvdFormatFehler, match="fehlt"):
        sl.lese_container(syn.FakeOle(st), Path("x"))


def test_lese_container_unerwartete_nutzlaenge() -> None:
    st, _ = syn.messung_stroeme(linien=4)
    zeilen = np.zeros((3, 12), dtype=np.float32)  # 3 Werte je Linie: weder reell noch komplex
    satz = sl.SATZ_DATEN + 48 + sl.SATZ_NACHSPANN
    st["Polytec_Data/M2/Signal_Info"] = syn.signal_info(3, 48)
    st["Polytec_Data/M2/ManyStreamsInfo"] = syn.strom_info(3, satz, [2, 1, 0])
    st["Polytec_Data/M2/ManyStreamsData-0"] = syn.punktdaten(zeilen, 4, [2, 1, 0], 0)
    with pytest.raises(sl.SvdFormatFehler, match="Nutzlänge"):
        sl.lese_container(syn.FakeOle(st), Path("x"))


def test_lese_container_ohne_optionale_stroeme() -> None:
    st, _ = syn.messung_stroeme()
    for p in (
        "Info/Geometry/Elements",
        "Info/DAQ_Settings_Fft/VibrometerControllers",
        "Info/ScanHead",
    ):
        del st[p]
    m = sl.lese_container(syn.FakeOle(st), Path("x"))
    assert m.elemente == [] and m.kanalgeraete_xml is None and m.hardware_texte == ()


def test_lese_svd_dateifehler(tmp_path: Path) -> None:
    with pytest.raises(FileNotFoundError):
        sl.lese_svd(tmp_path / "fehlt.svd")
    kein_ole = tmp_path / "kein.svd"
    kein_ole.write_bytes(b"kein OLE")
    with pytest.raises(sl.SvdFormatFehler):
        sl.lese_svd(kein_ole)
    assert sl.main([str(kein_ole)]) == 2


def test_main_gibt_uebersicht_aus(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    m, _ = _messung()
    monkeypatch.setattr(sl, "lese_svd", lambda _: m)
    assert sl.main(["egal.svd"]) == 0
    assert "Punktmittel (AvgSeq_Data): 5" in capsys.readouterr().out


# --- Plausibilitätsprüfung --------------------------------------------------------------


def test_pruefung_synthetisch_bestanden_und_meldet_fehlendes() -> None:
    m, _ = _messung()
    ergebnisse = sp.pruefe(m)
    durch = [e for e in ergebnisse if e.durchgefuehrt]
    nicht = {e.name: e.grund for e in ergebnisse if not e.durchgefuehrt}
    # 3 (>=0) + 1 CP + 1 CPH + 1 Jensen + 4 Band + 5 Punktmittel + 1 Kennfeld
    assert len(durch) == 16
    assert all(e.bestanden for e in durch), [e for e in durch if not e.bestanden]
    # sichtbar statt still weggelassen: Band S3 fehlt, 3 Punkte reichen nicht für Zuordnung
    assert nicht["nicht durchführbar: M3 Band = Σ|X|/2"] == "Banddaten S3 fehlen"
    assert any(k.startswith("nicht durchführbar: Punktzuordnung Geometrie") for k in nicht)
    assert not any(e.bestanden for e in ergebnisse if not e.durchgefuehrt)


def test_pruefung_ohne_autospektren_nicht_durchfuehrbar() -> None:
    m, _ = _messung()
    ohne_ap = {k: v for k, v in m.signale.items() if v.art != "AP"}
    namen = [
        e.name
        for e in sp.pruefe(replace(m, signale=ohne_ap, punktmittel=[]))
        if not e.durchgefuehrt
    ]
    assert "nicht durchführbar: M0 |CP|²/(AP·AP) <= 1" in namen
    assert "nicht durchführbar: M1 |CPH|/sqrt(AP) <= 1" in namen
    assert "nicht durchführbar: M4 AP/ABS² >= 1 (Jensen)" in namen


def test_pruefung_erkennt_blockablage_statt_verschraenkung() -> None:
    m, soll = _messung()
    cp = soll["cp"]
    falsch = sl.verschraenkt_zu_komplex(np.concatenate([cp.real, cp.imag], axis=1))
    signale = dict(m.signale)
    signale["M0"] = replace(m.signale["M0"], werte=falsch)
    erg = {e.name: e for e in sp.pruefe(replace(m, signale=signale))}
    assert not erg["M0 |CP|²/(AP·AP) <= 1"].bestanden
    assert erg["M0 |CP|²/(AP·AP) <= 1"].wert > 1.0


def _raster_messung() -> sl.SvdMessung:
    st, _ = syn.messung_stroeme(raster=(6, 8))  # 48 Punkte, Zickzack-Scan spaltenweise
    return sl.lese_container(syn.FakeOle(st), Path("x"))


def _messpunkte_umgeordnet(m: sl.SvdMessung, zeilen: np.ndarray) -> sl.SvdMessung:
    """MeasPoints-Zeilen (alle Felder) umordnen; Datensätze bleiben unverändert."""
    mp = m.punkte
    punkte = replace(
        mp,
        label=mp.label[zeilen],
        koordinaten_m=mp.koordinaten_m[zeilen],
        statusfelder={k: v[zeilen] for k, v in mp.statusfelder.items()},
    )
    return replace(m, punkte=punkte)


def test_punktzuordnung_richtig_bestanden() -> None:
    erg = sp.pruefe_punktzuordnung(_raster_messung())
    assert len(erg) == 3 and all(e.bestanden for e in erg), erg


@pytest.mark.parametrize("versatz", [1, -1, 9, -9])
def test_punktzuordnung_erkennt_versatz(versatz: int) -> None:
    m = _raster_messung()
    n = len(m.punkte.index)
    kenn, _, zeit = sp.pruefe_punktzuordnung(
        _messpunkte_umgeordnet(m, np.roll(np.arange(n), versatz))
    )
    assert not kenn.bestanden and kenn.wert == n
    assert zeit.bestanden  # die Zeitprüfung sieht den Geometriebezug nicht


def test_punktzuordnung_erkennt_einzelne_vertauschung_nur_ueber_kennfeld() -> None:
    m = _raster_messung()
    zeilen = np.arange(len(m.punkte.index))
    zeilen[[0, 1]] = [1, 0]
    kenn, geo, _ = sp.pruefe_punktzuordnung(_messpunkte_umgeordnet(m, zeilen))
    assert not kenn.bestanden and kenn.wert == 2
    assert geo.bestanden  # dokumentierte Grenze der Geometrie-Gegenprobe


def test_punktzuordnung_erkennt_permutation_und_zeitfehler() -> None:
    m = _raster_messung()
    perm = np.random.default_rng(3).permutation(len(m.punkte.index))
    kenn, geo, _ = sp.pruefe_punktzuordnung(_messpunkte_umgeordnet(m, perm))
    assert not kenn.bestanden and not geo.bestanden
    signale = dict(m.signale)
    signale["M0"] = replace(m.signale["M0"], zeit_a=list(reversed(m.signale["M0"].zeit_a)))
    assert not sp.pruefe_punktzuordnung(replace(m, signale=signale))[2].bestanden


def test_punktzuordnung_fehlende_daten_nicht_durchfuehrbar() -> None:
    m = _raster_messung()
    erg = sp.pruefe_punktzuordnung(replace(m, signale={}))
    assert erg[2].grund == "Zeitstempel fehlen" and erg[1].durchgefuehrt
    ohne_feld = replace(m, punkte=replace(m.punkte, statusfelder={}))
    assert sp.pruefe_punktzuordnung(ohne_feld)[0].grund == "Kennfelder fehlen"


def test_kennfeld_muss_in_allen_signalen_gleich_sein() -> None:
    st, _ = syn.messung_stroeme()
    daten = bytearray(st["Polytec_Data/M2/ManyStreamsData-0"])
    struct.pack_into("<d", daten, sl.DATENSTROM_KOPF + sl.SATZ_KENNFELD, 1.0)
    st["Polytec_Data/M2/ManyStreamsData-0"] = bytes(daten)
    with pytest.raises(sl.SvdFormatFehler, match="0x8C"):
        sl.lese_container(syn.FakeOle(st), Path("x"))


def test_pruefung_erkennt_vertauschte_punkte() -> None:
    m, _ = _messung()
    s = m.signale["M2"]
    m.signale["M2"] = sl.Signal(
        s.name, s.formel, s.art, s.kanaele, s.titel, s.einheit, s.werte[::-1], s.zeit_a, s.zeit_b
    )
    nicht = [e.name for e in sp.pruefe(m) if not e.bestanden]
    assert "M2 Band = Σ|X|/2" in nicht


def test_teile_argumente() -> None:
    assert sp.teile_argumente("FRF[AVG[AP[a]],AVG[CP[b,c]]]") == (
        "FRF",
        ["AVG[AP[a]]", "AVG[CP[b,c]]"],
    )
    for falsch in ("ohne", "OP[a]]", "OP[[a]", "OP[a]x"):
        with pytest.raises(sl.SvdFormatFehler):
            sp.teile_argumente(falsch)


def test_auswerter_fehlerfaelle() -> None:
    m, _ = _messung()
    a = sp.Auswerter(m)
    for formel in (
        "AVG[XX[S[T[9]]]]",
        "MUL[AVG[AP[S[T[3]]]]]",
        f"FRF[{syn.F_CP},{syn.F_CP}]",
        "FRF[AVG[AP[S[T[7]]]],AVG[CP[S[3DX[T[0]]],S[T[3]]]]]",
    ):
        with pytest.raises(sl.SvdFormatFehler):
            a.wert(formel)
    st, _ = syn.messung_stroeme()
    st["Polytec_Data/M5/Signal_Info"] = st["Polytec_Data/M2/Signal_Info"]
    st["Polytec_Data/M5/ManyStreamsInfo"] = st["Polytec_Data/M2/ManyStreamsInfo"]
    st["Polytec_Data/M5/ManyStreamsData-0"] = st["Polytec_Data/M2/ManyStreamsData-0"]
    st["Polytec_Data/M5/Static_Info"] = syn.static_info(
        [("Reference 7", "Ref7")], "AVG[AP[S[T[7]]]]"
    )
    a2 = sp.Auswerter(sl.lese_container(syn.FakeOle(st), Path("x")))
    with pytest.raises(sl.SvdFormatFehler, match="keinem CP"):
        a2.wert("FRF[AVG[AP[S[T[7]]]],AVG[CP[S[3DX[T[0]]],S[T[3]]]]]")


def test_pruefung_punktmittel_formel_unerwartet() -> None:
    m, _ = _messung()
    pm = m.punktmittel[0]
    m.punktmittel[0] = sl.Punktmittel(pm.nummer, "AVG[AP[S[T[3]]]]", pm.kanaele, pm.werte)
    with pytest.raises(sl.SvdFormatFehler):
        sp.pruefe(m)


# --- Kontrollplots ------------------------------------------------------------------------


def test_kontrollplots_synthetisch(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    m, _ = _messung()
    quelle = tmp_path / "q.svd"
    quelle.write_bytes(b"abc")
    monkeypatch.setattr(kp, "lese_svd", lambda _: m)
    pfade = kp.erzeuge(quelle, tmp_path / "bilder")
    assert [p.name for p in pfade] == [
        "w2_kontrolle_spektren_reell.png",
        "w2_kontrolle_spektren_komplex.png",
        "w2_kontrolle_punktmittel.png",
        "w2_kontrolle_geometrie_band.png",
    ]
    assert all(p.stat().st_size > 1000 for p in pfade)
    assert kp.sha256_datei(quelle) == hashlib.sha256(b"abc").hexdigest()
    assert kp.main([str(quelle), str(tmp_path / "b2")]) == 0
    assert kp.main([str(tmp_path / "fehlt.svd"), str(tmp_path / "b3")]) == 2


# --- Echte Datei (nur wenn vorhanden) -------------------------------------------------


@pytest.mark.skipif(not ECHTE_DATEI.is_file(), reason="Messdatei des Betreuers nicht vorhanden")
def test_echte_datei_plausibel_und_unveraendert() -> None:
    vorher = kp.sha256_datei(ECHTE_DATEI)
    m = sl.lese_svd(ECHTE_DATEI)
    assert kp.sha256_datei(ECHTE_DATEI) == vorher  # nur gelesen
    # K-ACHSE: Abtastfrequenz 2500 Hz (@4), Bandbreite 1000 Hz, Δf = 0,625 Hz, T = 1,6 s
    assert (m.fft.abtastfrequenz_hz, m.fft.bandbreite_hz, m.fft.linien) == (2500.0, 1000.0, 1600)
    assert m.fft.abtastwerte == 4000 and m.fft.startfrequenz_hz == 0.0
    assert m.fft.delta_f_hz == pytest.approx(0.625, rel=1e-15, abs=0.0)
    assert m.fft.blockdauer_s == pytest.approx(1.6, rel=1e-15, abs=0.0)
    np.testing.assert_allclose(m.frequenz_hz, 0.625 * np.arange(1, 1601), rtol=1e-15, atol=0.0)
    assert m.frequenz_hz[0] == 0.625 and m.frequenz_hz[-1] == 1000.0
    assert m.satz_feld_34 == pytest.approx(0.64)  # unbekanntes Feld, roh durchgereicht
    assert m.band_info == sl.BAND_INFO_GEPRUEFT
    assert len(m.signale) == 17 and len(m.punktmittel) == 35 and len(m.baender) == 29
    assert all(s.werte.shape == (135, 1600) for s in m.signale.values())
    assert len(m.elemente) == 112 and len(set(m.punkte.label.tolist())) == 135
    assert m.signale["M8"].einheit == "N" and m.signale["M9"].einheit == "(m/s)²"
    assert m.signale["M6"].kanaele == ("Ref2", "Ref1")
    assert m.signale["M7"].kanaele == ("Ref2", "Ref1")
    assert m.signale["M0"].kanaele == ("Vib X", "Ref1")
    assert m.signale["M0"].zeit_a[0].tzinfo is None
    erg = sp.pruefe(m)
    # 6 (>=0) + 7 CP + 4 CPH + 1 Jensen + 17 Band + 35 Punktmittel + 3 Punktzuordnung
    assert len(erg) == 73
    fehl = [e for e in erg if not e.bestanden]
    assert not fehl, fehl


def test_lesen_ueber_das_ende_wird_abgewiesen() -> None:
    with pytest.raises(sl.SvdFormatFehler, match="Ende"):
        sl._i32(b"\x00\x00", 0)
    with pytest.raises(sl.SvdFormatFehler, match="Ende"):
        sl._f64(b"\x00" * 8, 4)


# --- Rollen aus der Formel, Banddaten nur als Gegenprobe (K-W2, MAJOR) -------------------


@pytest.mark.parametrize(
    ("formel", "static", "soll"),
    [
        ("AVG[CP[S[T[4]],S[T[3]]]]", ("Ref1", "Ref2"), ("Ref2", "Ref1")),
        ("AVG[CPH[S[T[4]],CP[S[T[4]],S[T[3]]]]]", ("Ref1", "Ref2"), ("Ref2", "Ref1")),
        (syn.F_CP, ("Vib X", "Ref1"), ("Vib X", "Ref1")),
        ("AVG[CP[S[T[3]],S[3DY[T[1]]]]]", ("Vib Y", "Ref1"), ("Ref1", "Vib Y")),
        (syn.F_ABS, ("Ref1",), ("Ref1",)),
        (syn.F_APX, ("Vib X",), ("Vib X",)),
    ],
)
def test_rollen_aus_formel(formel: str, static: tuple[str, ...], soll: tuple[str, ...]) -> None:
    assert sl.rollen_aus_formel(formel, static) == soll


@pytest.mark.parametrize(
    ("formel", "static"),
    [
        ("CP[S[T[0]],S[T[3]]]", ("a", "b")),  # ohne AVG
        ("AVG[XX[S[T[0]]]]", ("a",)),  # unbekannte Art
        ("AVG[CPH[S[T[1]],CP[S[T[4]],S[T[3]]]]]", ("a", "b")),  # CPH-Antwort ≠ CP-Antwort
        ("AVG[CP[S[Q[0]],S[T[3]]]]", ("a", "b")),  # Kanalargument unbekannt
        ("AVG[CP[S[T[3]],S[T[3]]]]", ("Ref1", "Ref1")),  # doppelter Kanal
        ("AVG[CP[S[T[4]],S[T[3]]]]", ("Ref1",)),  # Kanalzahl
        ("AVG[AP[S[3DX[T[0]]]]]", ("Vib Y",)),  # Achse passt nicht zum Namen
    ],
)
def test_rollen_aus_formel_fehler(formel: str, static: tuple[str, ...]) -> None:
    with pytest.raises(sl.SvdFormatFehler):
        sl.rollen_aus_formel(formel, static)


def test_band_gegenprobe_titel_und_kanaele() -> None:
    def b(titel: str, kanaele: tuple[str, ...]) -> sl.Band:
        return sl.Band(titel, "", "", tuple((k, "", "") for k in kanaele), np.zeros(1))

    sl.pruefe_band_gegen_signal(b("CP Kraft * G", ("Vib X", "Ref1")), "CP", ("Vib X", "Ref1"), "M0")
    sl.pruefe_band_gegen_signal(b("Geschwindigkeit", ("Vib X",)), "CPH", ("Vib X", "Ref1"), "M1")
    for band, art, rollen in [
        (b("CP Kraft * G", ("Ref1", "Vib X")), "CP", ("Vib X", "Ref1")),  # Reihenfolge
        (b("AP Kraft²", ("Ref1",)), "ABS", ("Ref1",)),  # AP-Band am ABS-Signal
        (b("Kraft", ("Ref1",)), "AP", ("Ref1",)),  # ABS-Band am AP-Signal
    ]:
        with pytest.raises(sl.SvdFormatFehler):
            sl.pruefe_band_gegen_signal(band, art, rollen, "Mx")


def test_synthetisch_vertauschte_baender_fuehren_zum_abbruch() -> None:
    st, _ = syn.messung_stroeme()
    bk = "Band_Data/Entire_Bandwidth/FB0"
    st[f"{bk}/S2-0"], st[f"{bk}/S4-0"] = st[f"{bk}/S4-0"], st[f"{bk}/S2-0"]
    with pytest.raises(sl.SvdFormatFehler, match="Banddaten"):
        sl.lese_container(syn.FakeOle(st), Path("x"))


def test_synthetisch_fft_widerspricht_sich() -> None:
    st, _ = syn.messung_stroeme(linien=4)
    st["Info/DAQ_Settings_Fft/Fft"] = syn.fft(100.0, 4, 10, bw_hz=50.0)  # Δf 10 Hz ≠ 12,5 Hz
    with pytest.raises(sl.SvdFormatFehler, match="Bandbreite/Linien"):
        sl.lese_container(syn.FakeOle(st), Path("x"))


def test_synthetisch_band_info_status_und_uebersicht() -> None:
    """BandInfo-Gegenprobe: nur melden, kein Abbruch (Nutzerentscheidung 2026-11-02)."""
    st, _ = syn.messung_stroeme(linien=4)
    m = sl.lese_container(syn.FakeOle(st), Path("x"))
    assert m.band_info == sl.BAND_INFO_GEPRUEFT
    assert f"Gegenprobe BandInfo-0 (Δf 0,625 Hz / Obergrenze): {sl.BAND_INFO_GEPRUEFT}" in (
        sl.uebersicht(m)
    )
    bk = "Band_Data/Entire_Bandwidth/FB0/BandInfo-0"
    st[bk] = syn.band_info(4, 1.5625, 2500.0)
    m = sl.lese_container(syn.FakeOle(st), Path("x"))  # kein Abbruch
    assert m.band_info == sl.BAND_INFO_WIDERSPRUCH
    assert "WARNUNG Gegenprobe BandInfo-0" in sl.uebersicht(m)
    np.testing.assert_allclose(m.frequenz_hz, [10.0, 20.0, 30.0, 40.0])  # Achse aus Fft
    st[bk] = struct.pack("<I", 4) + zlib.compress(b"abcd")
    assert sl.lese_container(syn.FakeOle(st), Path("x")).band_info == sl.BAND_INFO_NICHT_PRUEFBAR
    del st[bk]
    m = sl.lese_container(syn.FakeOle(st), Path("x"))
    assert m.band_info == sl.BAND_INFO_FEHLT and "BandInfo-0 fehlt" in sl.uebersicht(m)


def test_synthetisch_frequenzachse_und_feld_34() -> None:
    """Achse k·Δf aus fs/N; das Feld +0x34 hat keinen Einfluss auf die Achse (K-ACHSE)."""
    st, _ = syn.messung_stroeme(linien=4)
    m = sl.lese_container(syn.FakeOle(st), Path("x"))
    np.testing.assert_allclose(m.frequenz_hz, [10.0, 20.0, 30.0, 40.0], rtol=1e-15, atol=0.0)
    assert m.satz_feld_34 == 0.64  # 1/Δf wäre 0,1 s: keine Prüfung "Blockdauer · Δf = 1" mehr
    st["Polytec_Data/M1/ManyStreamsData-0"] = syn.punktdaten(
        np.ones((3, 8), dtype=np.float32), 4, list(reversed(range(3))), 0, feld_34=0.5
    )
    with pytest.raises(sl.SvdFormatFehler, match="0x34"):
        sl.lese_container(syn.FakeOle(st), Path("x"))


def test_band_ueberspringt_fremde_texte_zwischen_kanaelen() -> None:
    werte = np.array([1.0])
    roh = struct.pack("<iii", 0, 2, 1) + syn.zk("Titel") + syn.zk("Zwischentext")
    roh += syn.zk("Ref1") + syn.zk("Ref1") + syn.zk("Kraft") + syn.zk("N")
    roh += syn.zk("Scanpunktnummer") + syn.zk("Kraft") + syn.zk("N")
    roh += struct.pack("<ii", 0x20, 1) + werte.astype("<f4").tobytes()
    b = sl.dekodiere_band(struct.pack("<I", len(roh)) + zlib.compress(roh), 1)
    assert b.kanaele == (("Ref1", "Kraft", "N"),)


def test_kontrollbild_ohne_cph_klare_meldung() -> None:
    m, _ = _messung()
    ohne = {k: v for k, v in m.signale.items() if v.art != "CPH"}
    with pytest.raises(sl.SvdFormatFehler, match="CPH"):
        kp.bild_komplex(replace(m, signale=ohne), "0" * 64)


# --- In-Memory-Kopie der echten Datei ----------------------------------------------------


@pytest.fixture(scope="module")
def echte_stroeme() -> dict[str, bytes]:
    if not ECHTE_DATEI.is_file():
        pytest.skip("Messdatei des Betreuers nicht vorhanden")
    with olefile.OleFileIO(str(ECHTE_DATEI)) as ole:
        return {"/".join(e): ole.openstream(e).read() for e in ole.listdir()}


def test_echte_kopie_ohne_banddaten_rollen_aus_formel(echte_stroeme: dict[str, bytes]) -> None:
    st = {k: v for k, v in echte_stroeme.items() if not k.startswith("Band_Data/")}
    m = sl.lese_container(syn.FakeOle(st), ECHTE_DATEI)
    assert m.signale["M6"].kanaele == ("Ref2", "Ref1")
    assert m.signale["M7"].kanaele == ("Ref2", "Ref1")
    assert m.signale["M6"].einheit is None  # ohne Banddaten keine Einheit
    erg = sp.pruefe(m)
    durch = [e for e in erg if e.durchgefuehrt]
    assert all(e.bestanden for e in durch), [e for e in durch if not e.bestanden]
    assert sum(not e.durchgefuehrt for e in erg) == 17  # je Signal „Band fehlt“


def test_echte_kopie_vertauschte_baender_s8_s12(echte_stroeme: dict[str, bytes]) -> None:
    st = dict(echte_stroeme)
    bk = "Band_Data/Entire_Bandwidth/FB0"
    st[f"{bk}/S8-0"], st[f"{bk}/S12-0"] = st[f"{bk}/S12-0"], st[f"{bk}/S8-0"]
    with pytest.raises(sl.SvdFormatFehler, match="M8"):
        sl.lese_container(syn.FakeOle(st), ECHTE_DATEI)


def test_echte_kopie_abtastfrequenz_5000_hz_bricht_ab(echte_stroeme: dict[str, bytes]) -> None:
    st = dict(echte_stroeme)
    fft = bytearray(st["Info/DAQ_Settings_Fft/Fft"])
    struct.pack_into("<d", fft, 4, 5000.0)  # Δf 1,25 Hz ≠ Bandbreite/Linien 0,625 Hz
    st["Info/DAQ_Settings_Fft/Fft"] = bytes(fft)
    with pytest.raises(sl.SvdFormatFehler, match="Bandbreite/Linien"):
        sl.lese_container(syn.FakeOle(st), ECHTE_DATEI)


def test_echte_kopie_band_info_gegenprobe(echte_stroeme: dict[str, bytes]) -> None:
    """BandInfo der Beispieldatei: 0,625 Hz und 1000 Hz bestätigen die Achse (Layout erkannt)."""
    fft = sl.dekodiere_fft_einstellungen(echte_stroeme["Info/DAQ_Settings_Fft/Fft"])
    info = echte_stroeme["Band_Data/Entire_Bandwidth/FB0/BandInfo-0"]
    assert sl.pruefe_band_info(info, fft) == sl.BAND_INFO_GEPRUEFT
    st = dict(echte_stroeme)
    st["Band_Data/Entire_Bandwidth/FB0/BandInfo-0"] = syn.band_info(1600, 1.5625, 2500.0)
    m = sl.lese_container(syn.FakeOle(st), ECHTE_DATEI)  # kein Abbruch, nur Meldung
    assert m.band_info == sl.BAND_INFO_WIDERSPRUCH


GOLDEN_CSV = (
    Path(__file__).resolve().parents[4]
    / "in_progress"
    / "versuche"
    / "2026-11-02_prototyp"
    / "golden_punkt1_label132.csv"
)


@pytest.mark.skipif(
    not (ECHTE_DATEI.is_file() and GOLDEN_CSV.is_file()),
    reason="Messdatei oder Golden File (PSV-Export, Label 132) nicht vorhanden",
)
def test_golden_file_label_132() -> None:
    """FG-02 9.9 (K-ACHSE): Leser gegen den PSV-Export (Polytec File Access), Label 132.

    Toleranzen nach FG-02 Abschnitt 8: Achse exakt (atol 1e-9 Hz), Spektren und H1 rtol 1e-5
    (float32-Daten; beobachtet CPH bitgleich, H1 rel. <= 5,8e-8). Bandnorm (50,478 mm/s/N) und
    3D-Gesamtwert (1,349 mm/s) sind PSV-Anzeigewerte mit drei Nachkommastellen; Toleranz = halbe
    letzte angezeigte Stelle = 0,0005 (beobachtet 50,4776 bzw. 1,34902: Abweichung 0,0004 bzw.
    0,00002). Vib Z allein (1,332454 mm/s) = Banddaten S5, rtol 1e-5.
    """
    g = np.genfromtxt(GOLDEN_CSV, delimiter=";", skip_header=1)
    assert g.shape == (1600, 13)

    def komplex(spalte: int) -> np.ndarray:  # Re bei spalte, Im bei spalte + 1
        return np.asarray(g[:, spalte] + 1j * g[:, spalte + 1])

    m = sl.lese_svd(ECHTE_DATEI)
    p = 0  # Label 132 = Punktindex 0
    assert int(m.punkte.label[p]) == 132
    np.testing.assert_allclose(g[:, 0], m.frequenz_hz, rtol=0.0, atol=1e-9)
    np.testing.assert_allclose(g[:, 0], 0.625 * np.arange(1, 1601), rtol=0.0, atol=1e-9)

    def w(name: str) -> np.ndarray:
        return np.asarray(m.signale[name].werte[p])

    zuordnung = {
        n: (m.signale[n].art, m.signale[n].kanaele[0])
        for n in ("M0", "M1", "M3", "M4", "M5", "M7", "M12")
    }
    assert zuordnung == {
        "M0": ("CP", "Vib X"),
        "M1": ("CPH", "Vib X"),
        "M3": ("CPH", "Vib Y"),
        "M4": ("CP", "Vib Z"),
        "M5": ("CPH", "Vib Z"),
        "M7": ("CPH", "Ref2"),
        "M12": ("AP", "Ref1"),
    }
    # CPH Vib X, Y, Z und Ref2 (Beschleunigung) gegen die Datei
    for spalte, signal in ((1, "M1"), (3, "M3"), (5, "M5"), (7, "M7")):
        np.testing.assert_allclose(w(signal), komplex(spalte), rtol=1e-5, atol=0.0)
    # H1 Vib X & Ref1 = CP/AP_Ref1, Vib Z & Ref1 (nicht konjugiert, M1 bestätigt)
    h1_x = w("M0") / w("M12")
    h1_z = w("M4") / w("M12")
    np.testing.assert_allclose(h1_x, komplex(9), rtol=1e-5, atol=0.0)
    np.testing.assert_allclose(h1_z, komplex(11), rtol=1e-5, atol=0.0)
    # bandnorm H1 Vib Z/Ref1, Band [158,75; 163,75] Hz geschlossen: 50,478 mm/s/N, 9 Linien
    df = 0.625
    maske = (m.frequenz_hz >= 158.75 - 1e-6 * df) & (m.frequenz_hz <= 163.75 + 1e-6 * df)
    assert int(maske.sum()) == 9
    bandnorm = np.sqrt(np.sum(np.abs(h1_z[maske]) ** 2) / 2.0) * 1e3
    assert abs(bandnorm - 50.478) <= 0.0005
    # 3D-Gesamtwert aus CPH X, Y, Z über alle Linien (Label 132): 1,349 mm/s; Vib Z allein
    # 1,332454 mm/s = Banddaten S5 der Datei
    rms = [np.sqrt(np.sum(np.abs(w(s)) ** 2) / 2.0) for s in ("M1", "M3", "M5")]
    assert abs(np.sqrt(sum(r**2 for r in rms)) * 1e3 - 1.349) <= 0.0005
    assert rms[2] * 1e3 == pytest.approx(1.332454, rel=1e-5, abs=0.0)
    np.testing.assert_allclose(rms[2], m.baender["S5"].werte[p], rtol=1e-5, atol=0.0)


def test_scanreihenfolge_muss_in_allen_signalen_gleich_sein() -> None:
    st, _ = syn.messung_stroeme(linien=4)
    zeilen = np.ones((3, 4), dtype=np.float32)
    satz = sl.SATZ_DATEN + 16 + sl.SATZ_NACHSPANN
    st["Polytec_Data/M2/ManyStreamsInfo"] = syn.strom_info(3, satz, [0, 1, 2])
    st["Polytec_Data/M2/ManyStreamsData-0"] = syn.punktdaten(zeilen, 4, [0, 1, 2], 0)
    with pytest.raises(sl.SvdFormatFehler, match="Scanreihenfolge"):
        sl.lese_container(syn.FakeOle(st), Path("x"))


# --- Kanalanker (K-W2b, MINOR B) ---------------------------------------------------------


def _channels(*kurz: str) -> bytes:
    return struct.pack("<3i", 10, 9, 11) + b"".join(syn.zk(k) + syn.zk(f"lang {k}") for k in kurz)


def test_kanalanker_aus_einstellungen() -> None:
    anker = sl.kanalanker_aus_einstellungen(_channels("Vib 3D", "Ref1", "Ref2"))
    assert anker == {"Vib X": 0, "Vib Y": 1, "Vib Z": 2, "Ref1": 3, "Ref2": 4}
    for falsch in (syn.zk("Ref1"), _channels("Ref1", "Ref1"), b""):
        with pytest.raises(sl.SvdFormatFehler):
            sl.kanalanker_aus_einstellungen(falsch)


def test_rollen_static_reihenfolge_ohne_bedeutung() -> None:
    # Reviewer-Fall: Static_Info-Reihenfolge vertauscht -> Rolle trotzdem richtig.
    f = "AVG[CP[S[T[4]],S[T[3]]]]"
    assert sl.rollen_aus_formel(f, ("Ref2", "Ref1")) == ("Ref2", "Ref1")
    anker = {"Ref1": 3, "Ref2": 4}
    assert sl.rollen_aus_formel(f, ("Ref2", "Ref1"), anker) == ("Ref2", "Ref1")


def test_rollen_anker_fehlt_oder_widerspricht() -> None:
    f = "AVG[CP[S[T[4]],S[T[3]]]]"
    with pytest.raises(sl.SvdFormatFehler, match="widersprechen"):
        sl.rollen_aus_formel(f, ("Ref1", "Ref2"), {"Ref1": 4, "Ref2": 3})
    with pytest.raises(sl.SvdFormatFehler, match="Kein Anker"):
        sl.rollen_aus_formel(f, ("Kraft", "Beschl"))
    with pytest.raises(sl.SvdFormatFehler, match="ohne Anker"):
        sl.rollen_aus_formel(f, ("Ref1", "Ref2"), {"Ref1": 3})
    with pytest.raises(sl.SvdFormatFehler, match="passen nicht"):
        sl.rollen_aus_formel(f, ("Kraft", "Beschl"), {"Kraft": 3, "Beschl": 5})
    # nur Anker aus den Einstellungen (Namen ohne Ordnung) genügt
    assert sl.rollen_aus_formel(f, ("Kraft", "Beschl"), {"Kraft": 3, "Beschl": 4}) == (
        "Beschl",
        "Kraft",
    )


def test_echte_kopie_static_vertauscht_ohne_banddaten(echte_stroeme: dict[str, bytes]) -> None:
    st = {k: v for k, v in echte_stroeme.items() if not k.startswith("Band_Data/")}
    for nr in (6, 7):  # Static_Info mit vertauschter Kanalreihenfolge (Ref2 vor Ref1)
        alt = sl.dekodiere_statische_info(st[f"Polytec_Data/M{nr}/Static_Info"])
        st[f"Polytec_Data/M{nr}/Static_Info"] = syn.static_info(
            [("Reference 2", "Ref2"), ("Reference 1", "Ref1")], alt.formel
        )
    m = sl.lese_container(syn.FakeOle(st), ECHTE_DATEI)
    assert m.signale["M6"].kanaele == ("Ref2", "Ref1")
    assert m.signale["M7"].kanaele == ("Ref2", "Ref1")


def test_echte_kopie_widerspruechlicher_kanalanker(echte_stroeme: dict[str, bytes]) -> None:
    st = dict(echte_stroeme)
    st["Info/DAQ_Settings_Fft/Channels"] = _channels("Vib 3D", "Ref2", "Ref1")
    with pytest.raises(sl.SvdFormatFehler, match="widersprechen"):
        sl.lese_container(syn.FakeOle(st), ECHTE_DATEI)


def test_kennfeld_nicht_trennscharf_bei_gleichen_werten() -> None:
    # Reviewer-Fall: alle Kennfeldwerte 0, Koordinaten um einen Index versetzt.
    m = _messpunkte_umgeordnet(_raster_messung(), np.roll(np.arange(48), 1))
    statusfelder = dict(m.punkte.statusfelder)
    statusfelder["feld_08"] = np.zeros(48)
    m = replace(
        m,
        punkte=replace(m.punkte, statusfelder=statusfelder),
        satz_kennfeld=np.zeros(48),
    )
    kenn = sp.pruefe_punktzuordnung(m)[0]
    assert not kenn.durchgefuehrt and not kenn.bestanden
    assert kenn.grund is not None and "nicht trennscharf" in kenn.grund


# --- Datei-Metadaten (K-2D Punkt 4) ----------------------------------------------------


def test_datei_zeit_aus_file_version() -> None:
    m, _ = _messung()
    assert m.datei_zeit == dt.datetime(2026, 10, 12, 9, 32, 52)
    assert "Dateizeit (FileVersion, naiv, vermutlich UTC): 2026-10-12 09:32:52" in sl.uebersicht(m)
    assert "Programmversion: nicht verfügbar" in sl.uebersicht(m)


@pytest.mark.parametrize(
    "stream",
    [
        syn.file_version(syn.FILETIME_2026_10_12, laenge=31),
        syn.file_version(syn.FILETIME_2026_10_12, laenge=40),
        syn.file_version(syn.FILETIME_2026_10_12, kopf=3),
        syn.file_version(-1 & 0xFFFFFFFFFFFFFFFF),
    ],
    ids=["zu_kurz", "zu_lang", "kopf_unbekannt", "filetime_unplausibel"],
)
def test_datei_zeit_nicht_verfuegbar_bei_abweichendem_layout(stream: bytes) -> None:
    assert sl.dekodiere_file_version(stream) is None


def test_datei_zeit_nicht_verfuegbar_ohne_stream() -> None:
    st, _ = syn.messung_stroeme()
    del st["FileVersion"]
    m = sl.lese_container(syn.FakeOle(st), Path("x"))
    assert m.datei_zeit is None
    assert "Dateizeit (FileVersion, naiv, vermutlich UTC): nicht verfügbar" in sl.uebersicht(m)


BEISPIELDATEI = Path(__file__).resolve().parents[4] / "Input" / "20261012_ref_Mitte.svd"


@pytest.mark.skipif(not BEISPIELDATEI.is_file(), reason="Beispieldatei nicht im Repository")
def test_datei_zeit_der_beispieldatei() -> None:
    """Gegenprobe: COM ``Version.FileTime`` 11:32:52 (MESZ) = 09:32:52 UTC (Faktenliste C8)."""
    m = sl.lese_svd(BEISPIELDATEI)
    assert m.datei_zeit == dt.datetime(2026, 10, 12, 9, 32, 52)
