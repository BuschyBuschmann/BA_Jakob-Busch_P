"""Synthetische Bytes im erschlossenen PSV-Layout (nur für Tests von svd_analyse).

Die Bausteine schreiben bekannte Werte im selben Layout, das ``svd_lesen`` dekodiert.
``FakeOle`` ersetzt ``olefile.OleFileIO`` (Pfad -> Bytes).
"""

from __future__ import annotations

import io
import struct
import zlib
from collections.abc import Sequence

import numpy as np
import numpy.typing as npt
import svd_lesen as sl

SATZ_KOPF_REST = 16  # ManyStreamsInfo nennt Satzlänge - 16 als Nutzlänge (unbenutzt)


def zk(text: str) -> bytes:
    """Längenpräfixierte UTF-16LE-Zeichenkette mit Null."""
    roh = (text + "\x00").encode("utf-16-le")
    return struct.pack("<i", len(roh)) + roh


def kennwert(punkt: int) -> float:
    """Synthetisches Kennfeld je Punkt (paarweise verschieden, in float32 exakt)."""
    return float(np.float32(1e-9 * (punkt + 1) * 1.37))


def signal_info(n: int, nbytes: int, version: int = 1) -> bytes:
    return struct.pack("<3i", version, n, nbytes)


def strom_info(n: int, satzlaenge: int, plaetze: Sequence[int]) -> bytes:
    werte = [1, satzlaenge, -1, -1, n, *range(n), n]
    for p in plaetze:
        werte += [satzlaenge - SATZ_KOPF_REST, p]
    werte += [n] + [-1] * n
    return struct.pack(f"<{len(werte)}i", *werte)


def punktdaten(
    zeilen: npt.NDArray[np.float32],
    linien: int,
    plaetze: Sequence[int],
    filetime0: int,
    blockdauer_s: float = 0.1,
) -> bytes:
    """``zeilen[p]`` = float32-Nutzdaten von Punkt ``p``; Ablage an ``plaetze[p]``.

    Zeitstempel steigen je Ablageplatz um 1 s (Scanreihenfolge).
    """
    n, n_float = zeilen.shape
    nbytes = 4 * n_float
    satz = sl.SATZ_DATEN + nbytes + sl.SATZ_NACHSPANN
    daten = bytearray(b"\xff\xff\xff\xff\x00\x00\x00\x00" + bytes(n * satz))
    for p in range(n):
        b = sl.DATENSTROM_KOPF + plaetze[p] * satz
        struct.pack_into("<i", daten, b + sl.SATZ_VERSION, 2)
        struct.pack_into("<i", daten, b + sl.SATZ_LINIEN, linien)
        struct.pack_into("<i", daten, b + sl.SATZ_PUNKT, p)
        t = filetime0 + plaetze[p] * 10_000_000
        struct.pack_into("<QQ", daten, b + sl.SATZ_ZEIT_A, t, t + 1_000_000)
        struct.pack_into("<d", daten, b + sl.SATZ_BLOCKDAUER, blockdauer_s)
        struct.pack_into("<d", daten, b + sl.SATZ_KENNFELD, kennwert(p))
        struct.pack_into("<i", daten, b + sl.SATZ_NUTZLAENGE, nbytes)
        daten[b + sl.SATZ_DATEN : b + sl.SATZ_DATEN + nbytes] = zeilen[p].astype("<f4").tobytes()
    return bytes(daten)


def static_info(kanaele: Sequence[tuple[str, str]], formel: str) -> bytes:
    teil = b"".join(zk(lang) + zk(kurz) for lang, kurz in kanaele) + zk(formel)
    return struct.pack("<i", 2) + bytes(20) + teil + teil


def fft(bw_hz: float, linien: int, abtast: int) -> bytes:
    return struct.pack("<idii", 2, bw_hz, linien, abtast) + bytes(32)


def messpunkte(labels: Sequence[int], xyz: npt.NDArray[np.float64]) -> bytes:
    kopf = bytearray(sl.MESSPUNKT_ERSTER)
    struct.pack_into("<i", kopf, 0, 7)
    struct.pack_into("<i", kopf, sl.MESSPUNKT_ANZAHL_OFFSET, len(labels))
    saetze = np.zeros(len(labels), dtype=sl._MESSPUNKT_DTYPE)
    saetze["label"] = labels
    saetze["xyz"] = xyz
    saetze["geometrie_status"] = 8193
    saetze["feld_08"] = [kennwert(p) for p in range(len(labels))]
    return bytes(kopf) + saetze.tobytes()


def elemente(elem: Sequence[Sequence[int]]) -> bytes:
    werte = [1, len(elem)]
    for e in elem:
        werte += [len(e), *e]
    return struct.pack(f"<{len(werte)}i", *werte)


def punktmittel(werte: npt.NDArray[np.float64]) -> bytes:
    kopf = struct.pack("<4i", 1, len(werte), 1, 2) + bytes(sl.PUNKTMITTEL_KOPF - 16)
    return kopf + werte.astype("<f4").tobytes()


def band(
    titel: str,
    kanaele: Sequence[tuple[str, str, str]],
    groesse: str,
    einheit: str,
    werte: npt.NDArray[np.float64],
) -> bytes:
    roh = struct.pack("<iii", 0, 2, 1) + zk(titel)
    for k, g, e in kanaele:
        roh += zk(k) + struct.pack("<i", 0) + zk(k) + zk(g) + zk(e)
    roh += zk("Scanpunktnummer") + zk(groesse) + zk(einheit)
    roh += struct.pack("<ii", 0x20, len(werte)) + werte.astype("<f4").tobytes()
    return struct.pack("<I", len(roh)) + zlib.compress(roh)


class FakeOle:
    """Ersatz für ``olefile.OleFileIO`` über ein Wörterbuch Pfad -> Bytes."""

    def __init__(self, stroeme: dict[str, bytes]) -> None:
        self.stroeme = stroeme

    def exists(self, pfad: str) -> bool:
        return pfad in self.stroeme

    def openstream(self, pfad: str | list[str]) -> io.BytesIO:
        schluessel = pfad if isinstance(pfad, str) else "/".join(pfad)
        return io.BytesIO(self.stroeme[schluessel])

    def listdir(self, streams: bool = True, storages: bool = False) -> list[list[str]]:
        return [p.split("/") for p in self.stroeme]


VIB = ("Vibrometer X", "Vib X")
REF = ("Reference 1", "Ref1")
F_CP = "AVG[CP[S[3DX[T[0]]],S[T[3]]]]"
F_CPH = "AVG[CPH[S[3DX[T[0]]],CP[S[3DX[T[0]]],S[T[3]]]]]"
F_APX = "AVG[AP[S[3DX[T[0]]]]]"
F_APR = "AVG[AP[S[T[3]]]]"
F_ABS = "AVG[ABS[S[T[3]]]]"


def f32(a: npt.NDArray[np.float64]) -> npt.NDArray[np.float64]:
    """Rundet wie die Datei auf float32 (und zurück nach float64)."""
    return np.asarray(a, dtype=np.float32).astype(np.float64)


def raster_scan(zeilen: int, spalten: int) -> tuple[list[int], npt.NDArray[np.float64]]:
    """Raster mit Index zeilenweise, Scan spaltenweise im Zickzack (wie in PSV-Dateien
    weicht die Scanreihenfolge von der Indexreihenfolge ab). Abstand 0,03 m.

    Returns ``(plaetze, xyz)``: Ablageplatz je Punktindex und Koordinaten.
    """
    folge: list[int] = []
    for sp in range(spalten):
        zeilen_folge = range(zeilen) if sp % 2 == 0 else reversed(range(zeilen))
        folge.extend(z * spalten + sp for z in zeilen_folge)
    plaetze = [0] * (zeilen * spalten)
    for platz, punkt in enumerate(folge):
        plaetze[punkt] = platz
    idx = np.arange(zeilen * spalten)
    xyz = np.column_stack([idx % spalten, idx // spalten, np.zeros(idx.size)]).astype(np.float64)
    return plaetze, xyz * 0.03


def messung_stroeme(
    n: int = 3,
    linien: int = 4,
    bloecke: int = 5,
    seed: int = 7,
    raster: tuple[int, int] | None = None,
) -> tuple[dict[str, bytes], dict[str, npt.NDArray[np.float64] | npt.NDArray[np.complex128]]]:
    """Baut eine vollständige kleine Messung aus zufälligen Blockspektren.

    Mit ``raster=(zeilen, spalten)`` liegen die Punkte auf einem Raster mit
    Zickzack-Scan (:func:`raster_scan`); ``n`` wird dann ``zeilen · spalten``.

    Die gemittelten Größen werden aus denselben Blöcken gebildet, damit alle
    Ungleichungen der Plausibilitätsprüfung erfüllt sind.
    """
    if raster is not None:
        n = raster[0] * raster[1]
    rng = np.random.default_rng(seed)
    form = (bloecke, n, linien)
    r = 1.0 + 0.1 * (rng.normal(size=form) + 1j * rng.normal(size=form))
    # Antwort = Übertragung · Referenz + Rauschen: hohe Kohärenz wie in einer echten Messung
    h = rng.normal(size=(n, linien)) + 1j * rng.normal(size=(n, linien))
    x = h * r + 0.05 * (rng.normal(size=form) + 1j * rng.normal(size=form))
    cp = (x * np.conj(r)).mean(0)
    cph = (x * np.conj(r) / np.abs(r)).mean(0)
    apx = (np.abs(x) ** 2).mean(0)
    apr = (np.abs(r) ** 2).mean(0)
    abs_r = np.abs(r).mean(0)
    cp32 = f32(cp.real) + 1j * f32(cp.imag)
    cph32 = f32(cph.real) + 1j * f32(cph.imag)
    apx32, apr32, abs32 = f32(apx), f32(apr), f32(abs_r)

    def verschraenkt(z: npt.NDArray[np.complex128]) -> npt.NDArray[np.float32]:
        aus = np.empty((z.shape[0], 2 * z.shape[1]), dtype=np.float32)
        aus[:, 0::2] = z.real
        aus[:, 1::2] = z.imag
        return aus

    plaetze = list(reversed(range(n)))
    xyz = np.column_stack([np.arange(n) / 10, np.zeros(n), np.zeros(n)])
    if raster is not None:
        plaetze, xyz = raster_scan(*raster)
    st: dict[str, bytes] = {
        "Info/DAQ_Settings_Fft/Fft": fft(10.0 * linien, linien, int(2.5 * linien)),
        # Ohne Raster: Punkte auf einer Linie, 0,1 m Abstand, Scan in umgekehrter Folge.
        "Info/Geometry/MeasPoints": messpunkte([100 + 3 * i for i in range(n)], xyz),
        "Info/Geometry/Elements": elemente([tuple(range(n))]),
        "Info/DAQ_Settings_Fft/VibrometerControllers": struct.pack("<3i", 2, 2, 4)
        + zk("<ControllerSettings><Range>50 mm/s</Range></ControllerSettings>"),
        "Info/ScanHead": zk("PSV-I-680") + zk("1.13"),
    }
    sigs: list[tuple[str, list[tuple[str, str]], npt.NDArray[np.float32]]] = [
        (F_CP, [VIB, REF], verschraenkt(cp32)),
        (F_CPH, [VIB, REF], verschraenkt(cph32)),
        (F_APX, [VIB], apx32.astype(np.float32)),
        (F_APR, [REF], apr32.astype(np.float32)),
        (F_ABS, [REF], abs32.astype(np.float32)),
    ]
    for nr, (formel, kan, zeilen) in enumerate(sigs):
        nbytes = 4 * zeilen.shape[1]
        satz = sl.SATZ_DATEN + nbytes + sl.SATZ_NACHSPANN
        b = f"Polytec_Data/M{nr}"
        st[f"{b}/Signal_Info"] = signal_info(n, nbytes)
        st[f"{b}/ManyStreamsInfo"] = strom_info(n, satz, plaetze)
        st[f"{b}/ManyStreamsData-0"] = punktdaten(zeilen, linien, plaetze, 133_000_000_000_000_000)
        st[f"{b}/Static_Info"] = static_info(kan, formel)
    bk = "Band_Data/Entire_Bandwidth/FB0"
    st[f"{bk}/S0-0"] = band(
        "CP Kraft * Geschwindigkeit",
        [("Vib X", "Geschwindigkeit", "m/s"), ("Ref1", "Kraft", "N")],
        "Kraft * Geschwindigkeit",
        "N * m/s",
        np.abs(cp32).sum(1) / 2,
    )
    st[f"{bk}/S1-0"] = band(
        "Geschwindigkeit",
        [("Vib X", "Geschwindigkeit", "m/s")],
        "Geschwindigkeit",
        "m/s",
        np.sqrt((np.abs(cph32) ** 2).sum(1) / 2),
    )
    st[f"{bk}/S2-0"] = band(
        "AP Geschwindigkeit²",
        [("Vib X", "Geschwindigkeit", "m/s")],
        "Geschwindigkeit²",
        "(m/s)²",
        apx32.sum(1) / 2,
    )
    st[f"{bk}/S4-0"] = band(
        "Kraft", [("Ref1", "Kraft", "N")], "Kraft", "N", np.sqrt((abs32**2).sum(1) / 2)
    )
    h1 = cp32 / apr32
    h2 = apx32 / np.conj(cp32)
    pm = {
        f"AVGSEQ[ABS[{F_CP}]]": np.abs(cp32).mean(0),
        f"AVGSEQ[{F_APX}]": apx32.mean(0),
        f"AVGSEQ[ABS[FRF[{F_APR},{F_CP}]]]": np.abs(h1).mean(0),
        f"AVGSEQ[ABS[FRF[{F_APX},{F_CP}]]]": np.abs(h2).mean(0),
        f"AVGSEQ[COH[FRF[{F_APR},{F_CP}],FRF[{F_APX},{F_CP}]]]": (np.abs(h1) / np.abs(h2)).mean(0),
    }
    for nr, (formel, werte) in enumerate(pm.items()):
        st[f"AvgSeq_Data/{nr}/Static_Info"] = static_info([VIB, REF], formel)
        st[f"AvgSeq_Data/{nr}/Corrected_Signal"] = punktmittel(werte)
    soll = {"cp": cp32, "cph": cph32, "apx": apx32, "apr": apr32, "abs": abs32}
    return st, soll
