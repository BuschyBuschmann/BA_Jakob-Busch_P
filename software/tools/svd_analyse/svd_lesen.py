"""Prototyp-Leser für Polytec-PSV-Messdateien (``.svd``) ohne Polytec File Access.

Werkzeug aus Paket W2 (Analyse mit Prototyp). Es liest eine PSV-Messdatei **nur lesend**
und liefert die Messdaten als NumPy-Arrays plus Metadaten. Es gehört nicht zum Hauptpaket
``ldv_automation`` und importiert nichts daraus.

Grundlage
---------
Das Format ist nicht offengelegt. Die Kodierung wurde an der Datei
``Input/20261012_ref_Mitte.svd`` erschlossen; Belege und Sicherheitsgrade stehen im
Analysebericht ``in_progress/analysen/2026-10-29_W2_svd-format.md``. Die Datei ist ein
OLE-Verbunddokument (Compound File Binary), gelesen mit ``olefile``.

Jedes Ergebnisfeld trägt einen Sicherheitsgrad (:data:`SICHERHEIT`):

``gesichert``
    Durch mindestens zwei unabhängige Prüfungen an der echten Datei belegt
    (z. B. Kohärenz in [0, 1], Übereinstimmung mit den von PSV selbst gespeicherten
    Punktmitteln und Bandwerten je Punkt).
``plausibel``
    Mit einer Prüfung oder einer Konsistenzbeobachtung gestützt.
``offen``
    Nicht dekodiert oder nicht belegt; wird nur roh durchgereicht.

Konventionen (KONVENTIONEN.md): float64/complex128 an der Grenze, Indizes 0-basiert,
``index`` und ``label`` getrennt, Frequenz in Hz. Phasen liefert der Leser nicht als Zahl,
sondern komplex (Real/Imag); Winkel daraus mit ``numpy.angle`` sind in rad.
"""

from __future__ import annotations

import argparse
import datetime as dt
import re
import struct
import sys
import zlib
from collections.abc import Sequence
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Literal

import numpy as np
import numpy.typing as npt
import olefile

FloatArray = npt.NDArray[np.float64]
ComplexArray = npt.NDArray[np.complex128]

Sicherheit = Literal["gesichert", "plausibel", "offen"]

#: Sicherheitsgrad je Ergebnisfeld (Begründung im Analysebericht W2).
SICHERHEIT: dict[str, Sicherheit] = {
    "signale.werte": "gesichert",
    "signale.komplex_verschraenkt": "gesichert",
    "signale.punktreihenfolge": "gesichert",
    "signale.formel": "gesichert",
    "signale.einheit": "plausibel",
    "signale.skalierung_spitzenwert": "plausibel",
    "signale.cp_phasenvorzeichen": "offen",
    "signale.cph_bedeutung": "plausibel",
    "signale.zeitstempel": "plausibel",
    "fft.bandbreite_hz": "gesichert",
    "fft.linien": "gesichert",
    "fft.abtastwerte": "plausibel",
    "frequenz_hz": "plausibel",
    "punkte.label": "plausibel",
    "punkte.koordinaten_m": "plausibel",
    "punkte.statusfelder": "offen",
    "elemente": "plausibel",
    "punktmittel.werte": "gesichert",
    "baender.effektivwert": "gesichert",
    "kanalgeraete_xml": "gesichert",
}

# --- Layout-Konstanten (am Beispiel erschlossen, siehe Analysebericht) -------------------
#: Länge des Kopfes von ``ManyStreamsData-0`` vor dem ersten Punktdatensatz in Byte.
DATENSTROM_KOPF = 8
#: Offsets im Punktdatensatz (relativ zum Datensatzanfang) in Byte.
SATZ_VERSION = 0x00
SATZ_LINIEN = 0x08
SATZ_PUNKT = 0x20
SATZ_ZEIT_A = 0x6C
SATZ_ZEIT_B = 0x74
#: Blockdauer ``float64`` in s (beobachtet 0,64 s = 1/Δf).
SATZ_BLOCKDAUER = 0x34
SATZ_NUTZLAENGE = 0xF4
SATZ_DATEN = 0xF8
#: Nachspann nach den Nutzdaten in Byte.
SATZ_NACHSPANN = 128
#: Länge des Kopfes von ``AvgSeq_Data/<n>/Corrected_Signal`` in Byte.
PUNKTMITTEL_KOPF = 34
#: Messpunkt-Datensätze in ``Info/Geometry/MeasPoints``.
MESSPUNKT_ANZAHL_OFFSET = 0x5D
MESSPUNKT_ERSTER = 0x61
MESSPUNKT_SATZ = 64

#: Art des gespeicherten Signals (oberster Operator in der Formel unter ``AVG[...]``).
ART_KOMPLEX: dict[str, bool] = {"CP": True, "CPH": True, "AP": False, "ABS": False}

#: Bezugszeitpunkt von FILETIME; bewusst ohne ``tzinfo`` (Zeitzone der Datei offen).
_FILETIME_NULL = dt.datetime(1601, 1, 1)


class SvdFormatFehler(ValueError):  # noqa: N818  (fachlicher Name)
    """Die Datei weicht vom erschlossenen Layout ab (lieber Abbruch als Falschwert)."""


# ---------------------------------------------------------------------------------------
# Dekodierfunktionen auf Bytes (ohne Dateizugriff, mit synthetischen Bytes testbar)
# ---------------------------------------------------------------------------------------


def _i32(daten: bytes, offset: int) -> int:
    if offset < 0 or offset + 4 > len(daten):
        raise SvdFormatFehler(f"Lesen über das Ende hinaus (Offset {offset}, Länge {len(daten)})")
    wert: int = struct.unpack_from("<i", daten, offset)[0]
    return wert


def _f64(daten: bytes, offset: int) -> float:
    if offset < 0 or offset + 8 > len(daten):
        raise SvdFormatFehler(f"Lesen über das Ende hinaus (Offset {offset}, Länge {len(daten)})")
    wert: float = struct.unpack_from("<d", daten, offset)[0]
    return wert


def filetime_zu_datetime(wert: int) -> dt.datetime:
    """Wandelt einen Windows-FILETIME (100-ns-Schritte seit 1601-01-01) in ``datetime``.

    Parameters
    ----------
    wert : int
        FILETIME als vorzeichenlose 64-Bit-Zahl.

    Returns
    -------
    datetime.datetime
        **Naiver** Zeitpunkt (ohne ``tzinfo``), auf ganze µs abgeschnitten. Ob PSV UTC
        oder Ortszeit schreibt, ist offen; der Wert wird unverändert umgerechnet.

    Raises
    ------
    SvdFormatFehler
        Bei negativem oder nicht als ``datetime`` darstellbarem Wert.
    """
    if wert < 0:
        raise SvdFormatFehler(f"FILETIME negativ: {wert}")
    try:
        return _FILETIME_NULL + dt.timedelta(microseconds=wert // 10)
    except OverflowError as exc:
        raise SvdFormatFehler(f"FILETIME unplausibel: {wert}") from exc


def utf16_zeichenketten(daten: bytes, max_bytes: int = 65536) -> list[tuple[int, str]]:
    """Findet längenpräfixierte UTF-16LE-Zeichenketten.

    Kodierung (gesichert an Static_Info und Banddaten): ``int32`` Bytelänge inklusive
    abschließender Null (2 Byte), danach UTF-16LE-Text. Leere Zeichenketten werden
    übersprungen.

    Parameters
    ----------
    daten : bytes
        Zu durchsuchende Bytes.
    max_bytes : int
        Größte zulässige Bytelänge einer Zeichenkette.

    Returns
    -------
    list of tuple of (int, str)
        Startoffset des Längenfelds und Text.
    """
    gefunden: list[tuple[int, str]] = []
    i = 0
    while i + 4 <= len(daten):
        laenge = struct.unpack_from("<i", daten, i)[0]
        ende = i + 4 + laenge
        if (
            4 <= laenge <= max_bytes
            and laenge % 2 == 0
            and ende <= len(daten)
            and daten[ende - 2 : ende] == b"\x00\x00"
        ):
            try:
                text = daten[i + 4 : ende - 2].decode("utf-16-le")
            except UnicodeDecodeError:
                text = ""
            if text and text.isprintable():
                gefunden.append((i, text))
                i = ende
                continue
        i += 1
    return gefunden


@dataclass(frozen=True)
class SignalInfo:
    """Inhalt von ``Signal_Info`` (12 Byte).

    Attributes
    ----------
    version : int
        Formatversion (beobachtet: 1).
    anzahl_punkte : int
        Anzahl Messpunkte.
    bytes_je_punkt : int
        Nutzdatenlänge je Punkt in Byte.
    """

    version: int
    anzahl_punkte: int
    bytes_je_punkt: int


def dekodiere_signal_info(daten: bytes) -> SignalInfo:
    """Dekodiert ``Polytec_Data/M<n>/Signal_Info``: drei ``int32``."""
    if len(daten) != 12:
        raise SvdFormatFehler(f"Signal_Info: 12 Byte erwartet, {len(daten)} gefunden")
    version, punkte, nbytes = struct.unpack("<3i", daten)
    if version != 1:
        raise SvdFormatFehler(f"Signal_Info: unbekannte Version {version}")
    if punkte <= 0 or nbytes <= 0 or nbytes % 4:
        raise SvdFormatFehler(f"Signal_Info unplausibel: Punkte={punkte}, Bytes={nbytes}")
    return SignalInfo(version, punkte, nbytes)


@dataclass(frozen=True)
class StromInfo:
    """Inhalt von ``ManyStreamsInfo``.

    Attributes
    ----------
    satzlaenge : int
        Länge eines Punktdatensatzes in ``ManyStreamsData-0`` in Byte.
    anzahl_punkte : int
        Anzahl Punktdatensätze.
    platz_je_punkt : tuple of int
        Für Punktindex ``i`` (0-basiert) die Position des Datensatzes im Datenstrom
        (Speicher- bzw. Scanreihenfolge).
    """

    satzlaenge: int
    anzahl_punkte: int
    platz_je_punkt: tuple[int, ...]


def dekodiere_strom_info(daten: bytes) -> StromInfo:
    """Dekodiert ``ManyStreamsInfo``.

    Layout (``int32``): ``1, satzlaenge, -1, -1, n``, dann ``n`` laufende Nummern
    ``0..n-1``, dann ``n`` und ``n`` Paare ``(nutzlaenge, platz)``, Rest ``n`` und ``-1``.
    Ausgewertet werden Satzlänge, Anzahl und die Platzzuordnung.
    """
    if len(daten) % 4 or len(daten) < 24:
        raise SvdFormatFehler(f"ManyStreamsInfo: ungültige Länge {len(daten)}")
    werte = struct.unpack(f"<{len(daten) // 4}i", daten)
    version, satzlaenge, _, _, n = werte[:5]
    if version != 1:
        raise SvdFormatFehler(f"ManyStreamsInfo: unbekannte Version {version}")
    paare_start = 5 + n + 1
    if n <= 0 or len(werte) < paare_start + 2 * n:
        raise SvdFormatFehler(f"ManyStreamsInfo: Länge passt nicht zu n={n}")
    if tuple(werte[5 : 5 + n]) != tuple(range(n)) or werte[5 + n] != n:
        raise SvdFormatFehler("ManyStreamsInfo: Nummernliste weicht vom bekannten Layout ab")
    plaetze = tuple(werte[paare_start + 1 : paare_start + 2 * n : 2])
    if sorted(plaetze) != list(range(n)):
        raise SvdFormatFehler("ManyStreamsInfo: Platzzuordnung ist keine Permutation")
    return StromInfo(satzlaenge, n, plaetze)


@dataclass(frozen=True)
class Punktdaten:
    """Dekodierte Punktdatensätze eines Signals.

    Attributes
    ----------
    werte : numpy.ndarray
        float64, Form ``(n_punkte, n_float)``; Zeile = Punktindex (0-basiert).
    linien : int
        Anzahl FFT-Linien laut Datensatzkopf.
    zeit_a, zeit_b : list of datetime.datetime
        Zwei FILETIME-Felder je Punkt, naiv (Zeitzone offen; Bedeutung plausibel).
    blockdauer_s : float
        Blockdauer laut Datensatzkopf in s (in allen Sätzen gleich).
    platz : tuple of int
        Ablageplatz (Scanreihenfolge) je Punktindex.
    """

    werte: FloatArray
    linien: int
    zeit_a: list[dt.datetime]
    zeit_b: list[dt.datetime]
    blockdauer_s: float
    platz: tuple[int, ...]


def dekodiere_punktdaten(daten: bytes, info: StromInfo, sig: SignalInfo) -> Punktdaten:
    """Dekodiert ``ManyStreamsData-0`` in eine Matrix je Punktindex.

    Jeder Datensatz trägt seinen Punktindex (0-basiert) selbst; die Zeilen werden danach
    sortiert. Die Nutzdaten sind ``float32`` little-endian.
    """
    n = info.anzahl_punkte
    if sig.anzahl_punkte != n:
        raise SvdFormatFehler(f"Punktanzahl uneinheitlich: {sig.anzahl_punkte} != {n}")
    if info.satzlaenge != SATZ_DATEN + sig.bytes_je_punkt + SATZ_NACHSPANN:
        raise SvdFormatFehler(f"Satzlänge {info.satzlaenge} passt nicht zu Nutzlänge")
    if len(daten) != DATENSTROM_KOPF + n * info.satzlaenge:
        raise SvdFormatFehler(f"ManyStreamsData: Länge {len(daten)} passt nicht zu {n} Sätzen")
    n_float = sig.bytes_je_punkt // 4
    werte = np.full((n, n_float), np.nan, dtype=np.float64)
    zeit_a: list[dt.datetime | None] = [None] * n
    zeit_b: list[dt.datetime | None] = [None] * n
    linien: int | None = None
    blockdauer: float | None = None
    for platz in range(n):
        basis = DATENSTROM_KOPF + platz * info.satzlaenge
        if _i32(daten, basis + SATZ_VERSION) != 2:
            raise SvdFormatFehler(f"Datensatz {platz}: unbekannte Version")
        if _i32(daten, basis + SATZ_NUTZLAENGE) != sig.bytes_je_punkt:
            raise SvdFormatFehler(f"Datensatz {platz}: Nutzlänge weicht ab")
        satz_linien = _i32(daten, basis + SATZ_LINIEN)
        if linien is None:
            linien = satz_linien
        elif satz_linien != linien:
            raise SvdFormatFehler(f"Datensatz {platz}: Linienzahl {satz_linien} != {linien}")
        satz_dauer = _f64(daten, basis + SATZ_BLOCKDAUER)
        if blockdauer is None:
            blockdauer = satz_dauer
        elif satz_dauer != blockdauer:  # Bitgleichheit: Kopffeld ist kopiert, nicht gerechnet
            raise SvdFormatFehler(f"Datensatz {platz}: Blockdauer {satz_dauer} != {blockdauer}")
        punkt = _i32(daten, basis + SATZ_PUNKT)
        if not 0 <= punkt < n or zeit_a[punkt] is not None:
            raise SvdFormatFehler(f"Datensatz {platz}: Punktindex {punkt} ungültig/doppelt")
        if info.platz_je_punkt[punkt] != platz:
            raise SvdFormatFehler(f"Punkt {punkt}: Platz {platz} widerspricht ManyStreamsInfo")
        roh = np.frombuffer(daten, dtype="<f4", count=n_float, offset=basis + SATZ_DATEN)
        werte[punkt] = roh.astype(np.float64)
        ta, tb = struct.unpack_from("<QQ", daten, basis + SATZ_ZEIT_A)
        zeit_a[punkt] = filetime_zu_datetime(ta)
        zeit_b[punkt] = filetime_zu_datetime(tb)
    assert linien is not None and blockdauer is not None  # n > 0 durch StromInfo garantiert
    return Punktdaten(
        werte,
        linien,
        [z for z in zeit_a if z is not None],
        [z for z in zeit_b if z is not None],
        blockdauer,
        info.platz_je_punkt,
    )


def verschraenkt_zu_komplex(werte: FloatArray) -> ComplexArray:
    """Wandelt ``[re0, im0, re1, im1, ...]`` (letzte Achse) in ``complex128``."""
    if werte.shape[-1] % 2:
        raise SvdFormatFehler("Verschränkte Daten brauchen eine gerade Anzahl Werte")
    ergebnis: ComplexArray = werte[..., 0::2] + 1j * werte[..., 1::2]
    return ergebnis


_FORMEL = re.compile(r"^(?:AVGSEQ\[)?AVG\[([A-Z]+)\[")


def signalart(formel: str) -> str:
    """Liefert den obersten Operator unter ``AVG[...]`` (z. B. ``CP``, ``AP``)."""
    treffer = _FORMEL.match(formel)
    if treffer is None:
        raise SvdFormatFehler(f"Formel nicht erkannt: {formel!r}")
    return treffer.group(1)


def teile_argumente(text: str) -> tuple[str, list[str]]:
    """Zerlegt ``OP[a,b]`` in ``("OP", ["a", "b"])`` unter Beachtung der Klammertiefe."""
    start = text.find("[")
    if start <= 0 or not text.endswith("]"):
        raise SvdFormatFehler(f"Formel nicht zerlegbar: {text!r}")
    innen = text[start + 1 : -1]
    teile: list[str] = []
    tiefe = 0
    letzter = 0
    for i, zeichen in enumerate(innen):
        if zeichen == "[":
            tiefe += 1
        elif zeichen == "]":
            tiefe -= 1
            if tiefe < 0:
                raise SvdFormatFehler(f"Klammern unausgeglichen: {text!r}")
        elif zeichen == "," and tiefe == 0:
            teile.append(innen[letzter:i])
            letzter = i + 1
    if tiefe != 0:
        raise SvdFormatFehler(f"Klammern unausgeglichen: {text!r}")
    teile.append(innen[letzter:])
    return text[:start], teile


_KANAL = re.compile(r"^S\[(?:3D([XYZ])\[)?T\[(\d+)\]\]?\]$")


def _kanal_schluessel(argument: str) -> tuple[int, str | None]:
    """``S[3DX[T[0]]]`` -> ``(0, "X")``, ``S[T[3]]`` -> ``(3, None)``."""
    treffer = _KANAL.match(argument)
    if treffer is None:
        raise SvdFormatFehler(f"Kanalargument nicht erkannt: {argument!r}")
    return int(treffer.group(2)), treffer.group(1)


def rollen_aus_formel(formel: str, kanaele: Sequence[str]) -> tuple[str, ...]:
    """Ordnet die Static_Info-Kanäle nach Rolle (Antwort zuerst) anhand der Formel.

    Rollen laut Formel: ``CP[Antwort, Referenz]``, ``CPH[S[Antwort], CP[Antwort,
    Referenz]]``, ``AP[Kanal]``, ``ABS[Kanal]``. Static_Info nennt die Kanäle nach
    aufsteigender Zeitkanalnummer ``T[i]`` (an der Beispieldatei beobachtet, plausibel);
    darüber werden Kanalnamen den Argumenten zugeordnet. 3D-Komponenten müssen im Namen
    auf ihre Achse enden (``Vib X`` zu ``3DX``), sonst ``SvdFormatFehler``.

    Parameters
    ----------
    formel : str
        Formel aus Static_Info, z. B. ``"AVG[CP[S[T[4]],S[T[3]]]]"``.
    kanaele : sequence of str
        Kurznamen in Static_Info-Reihenfolge.

    Returns
    -------
    tuple of str
        Kurznamen, Antwort zuerst.
    """
    op_avg, args_avg = teile_argumente(formel)
    if op_avg != "AVG" or len(args_avg) != 1:
        raise SvdFormatFehler(f"Formel ohne AVG[...]: {formel!r}")
    op, args = teile_argumente(args_avg[0])
    if op == "CP" and len(args) == 2:
        rollen = args
    elif op == "CPH" and len(args) == 2:
        op_innen, args_innen = teile_argumente(args[1])
        if op_innen != "CP" or len(args_innen) != 2 or args_innen[0] != args[0]:
            raise SvdFormatFehler(f"CPH-Formel unerwartet: {formel!r}")
        rollen = args_innen
    elif op in ("AP", "ABS") and len(args) == 1:
        rollen = args
    else:
        raise SvdFormatFehler(f"Signalart nicht unterstützt: {formel!r}")
    schluessel = [_kanal_schluessel(a) for a in rollen]
    nummern = sorted({k[0] for k in schluessel})
    if len(nummern) != len(schluessel) or len(nummern) != len(kanaele):
        raise SvdFormatFehler(f"Kanalzahl passt nicht: {formel!r} gegen {list(kanaele)}")
    name_je_nummer = dict(zip(nummern, kanaele, strict=True))
    ergebnis = []
    for nummer, achse in schluessel:
        name = name_je_nummer[nummer]
        if achse is not None and not name.endswith(f" {achse}"):
            raise SvdFormatFehler(f"Kanal {name!r} passt nicht zur Komponente 3D{achse}")
        ergebnis.append(name)
    return tuple(ergebnis)


#: Erwarteter Titelanfang der Banddaten je Signalart (``None``: ohne Präfix).
_BAND_PRAEFIX: dict[str, str | None] = {"CP": "CP ", "AP": "AP ", "ABS": None, "CPH": None}
_BAND_PRAEFIXE_ALLE = ("CP ", "AP ", "H1 ", "H2 ")


def pruefe_band_gegen_signal(band: Band, art: str, rollen: Sequence[str], name: str) -> None:
    """Gegenprobe Banddaten gleicher Nummer gegen das Signal; Widerspruch ist ein Fehler.

    Geprüft werden Kanäle in Rollenreihenfolge (bei ``CPH`` nennt das Band nur die
    Antwort) und der Titelanfang je Signalart (``CP …``, ``AP …``, bei ``ABS``/``CPH``
    ohne Präfix).
    """
    band_kanaele = tuple(k[0] for k in band.kanaele)
    soll = tuple(rollen[:1]) if art == "CPH" else tuple(rollen)
    if band_kanaele != soll:
        raise SvdFormatFehler(f"{name}: Banddaten-Kanäle {band_kanaele} != Formel {soll}")
    praefix = _BAND_PRAEFIX.get(art)
    passt = (
        band.titel.startswith(praefix)
        if praefix is not None
        else not band.titel.startswith(_BAND_PRAEFIXE_ALLE)
    )
    if not passt:
        raise SvdFormatFehler(f"{name}: Banddaten-Titel {band.titel!r} passt nicht zu {art}")


@dataclass(frozen=True)
class StatischeInfo:
    """Kanalnamen und Formel aus ``Static_Info``.

    Attributes
    ----------
    kanaele : tuple of str
        Kurznamen der beteiligten Kanäle in Dateireihenfolge (z. B. ``("Vib X", "Ref1")``).
    kanaele_lang : tuple of str
        Langnamen (z. B. ``"Vibrometer X"``).
    formel : str
        Signalformel, z. B. ``"AVG[CP[S[3DX[T[0]]],S[T[3]]]]"``.
    """

    kanaele: tuple[str, ...]
    kanaele_lang: tuple[str, ...]
    formel: str


def dekodiere_statische_info(daten: bytes) -> StatischeInfo:
    """Liest Kanalnamen (Lang/Kurz abwechselnd) und die erste Formel aus ``Static_Info``."""
    texte = [t for _, t in utf16_zeichenketten(daten)]
    formel_pos = next((i for i, t in enumerate(texte) if t.startswith("AVG")), None)
    if formel_pos is None:
        raise SvdFormatFehler("Static_Info: keine Formel gefunden")
    namen = texte[:formel_pos]
    if len(namen) % 2:
        raise SvdFormatFehler(f"Static_Info: Kanalnamen nicht paarweise: {namen}")
    return StatischeInfo(tuple(namen[1::2]), tuple(namen[0::2]), texte[formel_pos])


@dataclass(frozen=True)
class FftEinstellungen:
    """Inhalt von ``Info/DAQ_Settings_Fft/Fft`` (Auszug).

    Attributes
    ----------
    bandbreite_hz : float
        Bandbreite in Hz.
    linien : int
        Anzahl FFT-Linien.
    abtastwerte : int
        Abtastwerte je Block (plausibel: 2,5 · Linien).
    """

    bandbreite_hz: float
    linien: int
    abtastwerte: int

    @property
    def delta_f_hz(self) -> float:
        """Frequenzauflösung in Hz (Bandbreite / Linien)."""
        return self.bandbreite_hz / self.linien


def dekodiere_fft_einstellungen(daten: bytes) -> FftEinstellungen:
    """Dekodiert ``Info/DAQ_Settings_Fft/Fft`` (Auszug).

    Layout: ``int32`` Version 2, ``float64`` Bandbreite, ``int32`` Linien, ``int32``
    Abtastwerte; der Rest bleibt offen.
    """
    if len(daten) < 20 or _i32(daten, 0) != 2:
        raise SvdFormatFehler("Fft-Einstellungen: unbekannte Version oder zu kurz")
    bw = _f64(daten, 4)
    linien = _i32(daten, 12)
    abtast = _i32(daten, 16)
    if not (np.isfinite(bw) and bw > 0 and linien > 0 and abtast > 0):
        raise SvdFormatFehler(f"Fft-Einstellungen unplausibel: {bw}, {linien}, {abtast}")
    return FftEinstellungen(bw, linien, abtast)


@dataclass(frozen=True)
class Messpunkte:
    """Geometrie aus ``Info/Geometry/MeasPoints``.

    Attributes
    ----------
    index : numpy.ndarray
        0-basierter Punktindex (Dateireihenfolge).
    label : numpy.ndarray
        In PSV angezeigte Punktnummer („Index“ in der Oberfläche).
    koordinaten_m : numpy.ndarray
        Form ``(n, 3)``, x/y/z; Einheit m plausibel, Bezugssystem offen.
    statusfelder : dict of str to numpy.ndarray
        Roh durchgereichte, nicht gesicherte Felder.
    """

    index: npt.NDArray[np.int64]
    label: npt.NDArray[np.int64]
    koordinaten_m: FloatArray
    statusfelder: dict[str, npt.NDArray[Any]] = field(default_factory=dict)


_MESSPUNKT_DTYPE = np.dtype(
    [
        ("label", "<i4"),
        ("feld_04", "<i4"),
        ("feld_08", "<f4"),
        ("geometrie_status", "<u4"),
        ("xyz", "<f4", (3,)),
        ("video_uv", "<f4", (2,)),
        ("fokus_status", "<u4"),
        ("fokus", "<i4", (3,)),
        ("feld_34", "<i4"),
        ("feld_38", "<f4"),
        ("feld_3c", "<u4"),
    ]
)


def dekodiere_messpunkte(daten: bytes) -> Messpunkte:
    """Dekodiert ``MeasPoints``: Kopf (Version 7), Anzahl bei 0x5D, Sätze zu 64 Byte."""
    if len(daten) < MESSPUNKT_ERSTER or _i32(daten, 0) != 7:
        raise SvdFormatFehler("MeasPoints: unbekannte Version oder zu kurz")
    n = _i32(daten, MESSPUNKT_ANZAHL_OFFSET)
    if n <= 0 or len(daten) != MESSPUNKT_ERSTER + n * MESSPUNKT_SATZ:
        raise SvdFormatFehler(f"MeasPoints: Länge {len(daten)} passt nicht zu n={n}")
    assert _MESSPUNKT_DTYPE.itemsize == MESSPUNKT_SATZ
    saetze = np.frombuffer(daten, dtype=_MESSPUNKT_DTYPE, count=n, offset=MESSPUNKT_ERSTER)
    label = saetze["label"].astype(np.int64)
    if len(set(label.tolist())) != n:
        raise SvdFormatFehler("MeasPoints: Labels nicht eindeutig")
    roh = {
        name: saetze[name].astype(np.float64 if saetze[name].dtype.kind == "f" else np.int64)
        for name in _MESSPUNKT_DTYPE.names or ()
        if name not in ("label", "xyz")
    }
    return Messpunkte(np.arange(n, dtype=np.int64), label, saetze["xyz"].astype(np.float64), roh)


def dekodiere_elemente(daten: bytes, anzahl_punkte: int | None = None) -> list[tuple[int, ...]]:
    """Dekodiert ``Info/Geometry/Elements``.

    Layout (``int32``): 1, Anzahl, je Element Eckenzahl und 0-basierte Punktindizes.
    """
    if len(daten) < 8 or len(daten) % 4 or _i32(daten, 0) != 1:
        raise SvdFormatFehler("Elements: unbekannte Version oder Länge")
    werte = struct.unpack(f"<{len(daten) // 4}i", daten)
    n = werte[1]
    elemente: list[tuple[int, ...]] = []
    pos = 2
    for _ in range(n):
        if pos >= len(werte):
            raise SvdFormatFehler("Elements: Daten enden zu früh")
        ecken = werte[pos]
        if not 2 <= ecken <= 64 or pos + 1 + ecken > len(werte):
            raise SvdFormatFehler(f"Elements: Eckenzahl {ecken} unplausibel")
        elem = tuple(werte[pos + 1 : pos + 1 + ecken])
        if anzahl_punkte is not None and not all(0 <= p < anzahl_punkte for p in elem):
            raise SvdFormatFehler(f"Elements: Punktindex außerhalb 0..{anzahl_punkte - 1}")
        elemente.append(elem)
        pos += 1 + ecken
    if pos != len(werte):
        raise SvdFormatFehler("Elements: überzählige Daten")
    return elemente


def dekodiere_punktmittel(daten: bytes, linien: int) -> FloatArray:
    """Dekodiert ``AvgSeq_Data/<n>/Corrected_Signal``: 34 Byte Kopf, ``float32``-Werte."""
    if len(daten) != PUNKTMITTEL_KOPF + 4 * linien or _i32(daten, 4) != linien:
        raise SvdFormatFehler(f"Corrected_Signal: Länge {len(daten)} passt nicht zu {linien}")
    werte: FloatArray = np.frombuffer(
        daten, dtype="<f4", count=linien, offset=PUNKTMITTEL_KOPF
    ).astype(np.float64)
    return werte


@dataclass(frozen=True)
class Band:
    """Band ``Entire_Bandwidth`` eines Signals.

    Attributes
    ----------
    titel : str
        Signalname laut Datei (deutsch), z. B. ``"H1 Geschwindigkeit / Kraft"``.
    groesse, einheit : str
        Größe und Einheit der Bandwerte, z. B. ``"Kraft"``, ``"N"``.
    kanaele : tuple of tuple of str
        Je beteiligtem Kanal ``(kanal, größe, einheit)``, Antwort zuerst (plausibel).
    werte : numpy.ndarray
        Ein Wert je Punktindex (0-basiert). Für ``ABS``/``CPH`` (Amplituden) der
        Effektivwert √(Σ|A|²/2), für ``AP``/``CP`` Σ|X|/2 (quadratischer Mittelwert bzw.
        Kreuzleistung über die Bandbreite); belegt in ``svd_pruefung``.
    """

    titel: str
    groesse: str
    einheit: str
    kanaele: tuple[tuple[str, str, str], ...]
    werte: FloatArray


def dekodiere_band(daten: bytes, anzahl_punkte: int) -> Band:
    """Dekodiert ``Band_Data/.../S<n>-0``: ``uint32`` Länge, zlib-Daten.

    Im entpackten Inhalt stehen Beschreibungstexte, am Ende ``int32 n`` und ``n``
    ``float32``-Werte.
    """
    if len(daten) < 5:
        raise SvdFormatFehler("Banddaten zu kurz")
    soll = struct.unpack_from("<I", daten, 0)[0]
    try:
        roh = zlib.decompress(daten[4:])
    except zlib.error as exc:
        raise SvdFormatFehler(f"Banddaten nicht entpackbar: {exc}") from exc
    if len(roh) != soll:
        raise SvdFormatFehler(f"Banddaten: Länge {len(roh)} != angegeben {soll}")
    werte_start = len(roh) - 4 * anzahl_punkte
    if werte_start < 4 or _i32(roh, werte_start - 4) != anzahl_punkte:
        raise SvdFormatFehler("Banddaten: Punktanzahl vor den Werten fehlt")
    werte = np.frombuffer(roh, dtype="<f4", count=anzahl_punkte, offset=werte_start)
    texte = [t for _, t in utf16_zeichenketten(roh[: werte_start - 4])]
    if len(texte) < 3:
        raise SvdFormatFehler("Banddaten: Beschreibung fehlt")
    kanaele: list[tuple[str, str, str]] = []
    i = 1
    while i + 3 < len(texte) - 2:
        if texte[i] == texte[i + 1]:
            kanaele.append((texte[i], texte[i + 2], texte[i + 3]))
            i += 4
        else:
            i += 1
    return Band(texte[0], texte[-2], texte[-1], tuple(kanaele), werte.astype(np.float64))


# ---------------------------------------------------------------------------------------
# Datei lesen
# ---------------------------------------------------------------------------------------


@dataclass(frozen=True)
class Signal:
    """Ein gespeichertes Punktsignal (``Polytec_Data/M<n>``).

    Attributes
    ----------
    name : str
        Storage-Name, z. B. ``"M0"``.
    formel : str
        Formel laut ``Static_Info``.
    art : str
        ``CP`` (Kreuzspektrum, komplex), ``CPH`` (Antwortspektrum mit Phase zur Referenz,
        komplex; Bedeutung plausibel), ``AP`` (Autospektrum, reell),
        ``ABS`` (betragsgemitteltes Spektrum, reell).
    kanaele : tuple of str
        Beteiligte Kanäle (Kurzname), Antwort zuerst; Rolle aus der Formel
        (:func:`rollen_aus_formel`).
    titel, einheit : str or None
        Aus den Banddaten gleicher Nummer nach bestandener Gegenprobe
        (:func:`pruefe_band_gegen_signal`); ``None`` ohne Banddaten. Bei ``CPH`` nennen
        die Banddaten nur den Antwortkanal und dessen Einheit.
    werte : numpy.ndarray
        Form ``(n_punkte, n_linien)``, ``complex128`` bzw. ``float64``.
    zeit_a, zeit_b : list of datetime.datetime
        Zeitstempel je Punkt (plausibel).
    """

    name: str
    formel: str
    art: str
    kanaele: tuple[str, ...]
    titel: str | None
    einheit: str | None
    werte: FloatArray | ComplexArray
    zeit_a: list[dt.datetime]
    zeit_b: list[dt.datetime]

    @property
    def komplex(self) -> bool:
        """``True`` bei komplexen Werten."""
        return bool(np.iscomplexobj(self.werte))


@dataclass(frozen=True)
class Punktmittel:
    """Von PSV gespeichertes Mittel über alle Punkte (``AvgSeq_Data/<n>``)."""

    nummer: int
    formel: str
    kanaele: tuple[str, ...]
    werte: FloatArray


@dataclass(frozen=True)
class SvdMessung:
    """Gesamtergebnis des Lesers.

    Attributes
    ----------
    pfad : pathlib.Path
        Gelesene Datei.
    fft : FftEinstellungen
        Bandbreite, Linien, Abtastwerte.
    frequenz_hz : numpy.ndarray
        **Vorläufige** Frequenzachse ``k · Δf``, ``k = 1 … Linien`` (KONVENTIONEN; ob
        Index 0 die Linie 1 ist, ist an der Datei nicht belegt).
    punkte : Messpunkte
        Geometrie.
    elemente : list of tuple of int
        Elemente als 0-basierte Punktindizes.
    signale : dict of str to Signal
        Punktsignale nach Storage-Name.
    punktmittel : list of Punktmittel
        Gespeicherte Punktmittel.
    baender : dict of str to Band
        Banddaten nach Streamname (``S0`` …).
    kanalgeraete_xml : str or None
        Klartext-XML der Vibrometer-Controller-Einstellungen.
    hardware_texte : tuple of str
        Texte aus ``HardwareConfig2`` und ``ScanHead`` (Seriennummern, Typen, Firmware).
    scan_platz : tuple of int
        Ablageplatz (Scanreihenfolge) je Punktindex, in allen Signalen gleich.
    """

    pfad: Path
    fft: FftEinstellungen
    frequenz_hz: FloatArray
    punkte: Messpunkte
    elemente: list[tuple[int, ...]]
    signale: dict[str, Signal]
    punktmittel: list[Punktmittel]
    baender: dict[str, Band]
    kanalgeraete_xml: str | None
    hardware_texte: tuple[str, ...]
    scan_platz: tuple[int, ...] = ()


def _strom(ole: Any, pfad: str) -> bytes:
    if not ole.exists(pfad):
        raise SvdFormatFehler(f"Stream fehlt: {pfad}")
    daten: bytes = ole.openstream(pfad).read()
    return daten


def _nummerierte_storages(ole: Any, wurzel: str) -> list[int]:
    nummern = {
        int(e[1][1:] if e[1][:1] == "M" else e[1])
        for e in ole.listdir(streams=True, storages=False)
        if len(e) >= 2 and e[0] == wurzel and re.fullmatch(r"M?\d+", e[1])
    }
    return sorted(nummern)


def lese_svd(pfad: str | Path) -> SvdMessung:
    """Liest eine PSV-Messdatei nur lesend.

    Parameters
    ----------
    pfad : str or pathlib.Path
        Pfad zur ``.svd``-Datei. Sie wird nur zum Lesen geöffnet.

    Returns
    -------
    SvdMessung
        Gelesene Daten und Metadaten.

    Raises
    ------
    SvdFormatFehler
        Wenn die Datei vom erschlossenen Layout abweicht.
    FileNotFoundError
        Wenn die Datei fehlt.
    """
    pfad = Path(pfad)
    if not pfad.is_file():
        raise FileNotFoundError(pfad)
    if not olefile.isOleFile(str(pfad)):
        raise SvdFormatFehler(f"Kein OLE-Verbunddokument: {pfad}")
    with olefile.OleFileIO(str(pfad)) as ole:
        return lese_container(ole, pfad)


def lese_container(ole: Any, pfad: Path) -> SvdMessung:
    """Liest die Messung aus einem geöffneten OLE-Container.

    Parameters
    ----------
    ole : Any
        Objekt mit der Schnittstelle von ``olefile.OleFileIO`` (``exists``,
        ``openstream``, ``listdir``); in Tests ein Ersatzobjekt.
    pfad : pathlib.Path
        Pfad der Datei (nur für die Ausgabe).

    Returns
    -------
    SvdMessung
        Gelesene Daten und Metadaten.
    """
    fft = dekodiere_fft_einstellungen(_strom(ole, "Info/DAQ_Settings_Fft/Fft"))
    punkte = dekodiere_messpunkte(_strom(ole, "Info/Geometry/MeasPoints"))
    n = len(punkte.index)
    elemente = (
        dekodiere_elemente(_strom(ole, "Info/Geometry/Elements"), n)
        if ole.exists("Info/Geometry/Elements")
        else []
    )
    baender: dict[str, Band] = {}
    band_wurzel = "Band_Data/Entire_Bandwidth/FB0"
    for e in ole.listdir():
        if "/".join(e[:-1]) == band_wurzel and re.fullmatch(r"S\d+-0", e[-1]):
            baender[e[-1][:-2]] = dekodiere_band(ole.openstream(e).read(), n)
    signale: dict[str, Signal] = {}
    scan_platz: tuple[int, ...] | None = None
    for nr in _nummerierte_storages(ole, "Polytec_Data"):
        basis = f"Polytec_Data/M{nr}"
        sig = dekodiere_signal_info(_strom(ole, f"{basis}/Signal_Info"))
        info = dekodiere_strom_info(_strom(ole, f"{basis}/ManyStreamsInfo"))
        daten = dekodiere_punktdaten(_strom(ole, f"{basis}/ManyStreamsData-0"), info, sig)
        # Blockdauer im Datensatz muss 1/Δf sein (rtol 1e-9: beide Werte sind float64
        # aus denselben Einstellungen, Abweichung nur durch Rundung ~1e-16).
        if not np.isclose(daten.blockdauer_s * fft.delta_f_hz, 1.0, rtol=1e-9, atol=0.0):
            raise SvdFormatFehler(
                f"M{nr}: Blockdauer {daten.blockdauer_s} s passt nicht zu Δf {fft.delta_f_hz} Hz"
            )
        if scan_platz is None:
            scan_platz = daten.platz
        elif daten.platz != scan_platz:
            raise SvdFormatFehler(f"M{nr}: Scanreihenfolge weicht von M0 ab")
        stat = dekodiere_statische_info(_strom(ole, f"{basis}/Static_Info"))
        art = signalart(stat.formel)
        if daten.linien != fft.linien or sig.anzahl_punkte != n:
            raise SvdFormatFehler(f"M{nr}: Linien/Punkte passen nicht zu den Einstellungen")
        komplex = sig.bytes_je_punkt == 8 * fft.linien
        if not komplex and sig.bytes_je_punkt != 4 * fft.linien:
            raise SvdFormatFehler(f"M{nr}: Nutzlänge {sig.bytes_je_punkt} unerwartet")
        if art in ART_KOMPLEX and ART_KOMPLEX[art] != komplex:
            raise SvdFormatFehler(f"M{nr}: Art {art} widerspricht Datentyp")
        werte: FloatArray | ComplexArray = (
            verschraenkt_zu_komplex(daten.werte) if komplex else daten.werte
        )
        # Rolle (Antwort zuerst) aus der Formel; Banddaten gleicher Nummer nur als Gegenprobe.
        kanaele = rollen_aus_formel(stat.formel, stat.kanaele)
        band = baender.get(f"S{nr}")
        if band is not None:
            pruefe_band_gegen_signal(band, art, kanaele, f"M{nr}")
        signale[f"M{nr}"] = Signal(
            f"M{nr}",
            stat.formel,
            art,
            kanaele,
            band.titel if band is not None else None,
            band.einheit if band is not None else None,
            werte,
            daten.zeit_a,
            daten.zeit_b,
        )
    punktmittel: list[Punktmittel] = []
    for nr in _nummerierte_storages(ole, "AvgSeq_Data"):
        basis = f"AvgSeq_Data/{nr}"
        stat = dekodiere_statische_info(_strom(ole, f"{basis}/Static_Info"))
        werte_pm = dekodiere_punktmittel(_strom(ole, f"{basis}/Corrected_Signal"), fft.linien)
        punktmittel.append(Punktmittel(nr, stat.formel, stat.kanaele, werte_pm))
    xml = None
    pfad_vc = "Info/DAQ_Settings_Fft/VibrometerControllers"
    if ole.exists(pfad_vc):
        texte = [t for _, t in utf16_zeichenketten(_strom(ole, pfad_vc), 1 << 20)]
        xml = next((t for t in texte if t.startswith("<")), None)
    hw: list[str] = []
    for p in ("Info/HardwareConfig2", "Info/ScanHead"):
        if ole.exists(p):
            hw.extend(t for _, t in utf16_zeichenketten(_strom(ole, p)))
    freq = fft.delta_f_hz * np.arange(1, fft.linien + 1, dtype=np.float64)
    return SvdMessung(
        pfad,
        fft,
        freq,
        punkte,
        elemente,
        signale,
        punktmittel,
        baender,
        xml,
        tuple(hw),
        scan_platz or (),
    )


def uebersicht(messung: SvdMessung) -> str:
    """Erzeugt eine Textübersicht mit Sicherheitsgraden."""
    f = messung.fft
    zeilen = [
        f"Datei: {messung.pfad.name}",
        f"FFT: Bandbreite {f.bandbreite_hz:g} Hz, {f.linien} Linien, Δf = {f.delta_f_hz:g} Hz, "
        f"{f.abtastwerte} Abtastwerte/Block [{SICHERHEIT['fft.linien']}]",
        f"Frequenzachse (vorläufig): {messung.frequenz_hz[0]:g} … {messung.frequenz_hz[-1]:g} Hz "
        f"[{SICHERHEIT['frequenz_hz']}]",
        f"Messpunkte: {len(messung.punkte.index)} (Label {messung.punkte.label.min()} … "
        f"{messung.punkte.label.max()}), Elemente: {len(messung.elemente)}",
    ]
    lo = messung.punkte.koordinaten_m.min(axis=0)
    hi = messung.punkte.koordinaten_m.max(axis=0)
    zeilen.append(
        "Koordinaten [m, plausibel]: "
        + ", ".join(f"{a} {u:.4f} … {o:.4f}" for a, u, o in zip("xyz", lo, hi, strict=True))
    )
    alle_zeiten = [z for s in messung.signale.values() for z in s.zeit_a]
    if alle_zeiten:
        zeilen.append(
            "Zeitstempel [plausibel, Zeitzone offen, naiv]: "
            f"{min(alle_zeiten):%Y-%m-%d %H:%M:%S} … "
            f"{max(alle_zeiten):%Y-%m-%d %H:%M:%S}"
        )
    zeilen.append("Signale (Polytec_Data):")
    for s in messung.signale.values():
        typ = "complex128" if s.komplex else "float64"
        zeilen.append(
            f"  {s.name:>4} {s.art:<4} {'/'.join(s.kanaele):<14} {typ:<10} {s.werte.shape} "
            f"Einheit={s.einheit or 'offen'}  {s.titel or ''}  {s.formel}"
        )
    zeilen.append(f"Punktmittel (AvgSeq_Data): {len(messung.punktmittel)}")
    for p in messung.punktmittel:
        zeilen.append(f"  {p.nummer:>3} {p.formel}")
    zeilen.append(f"Bänder (Entire_Bandwidth): {len(messung.baender)}")
    for name, b in sorted(messung.baender.items(), key=lambda x: int(x[0][1:])):
        zeilen.append(f"  {name:>4} {b.titel} [{b.einheit}]")
    if messung.hardware_texte:
        zeilen.append("Hardware: " + ", ".join(messung.hardware_texte))
    zeilen.append("Sicherheitsgrade: " + ", ".join(f"{k}={v}" for k, v in SICHERHEIT.items()))
    return "\n".join(zeilen)


def main(argv: Sequence[str] | None = None) -> int:
    """Kommandozeile: Übersicht einer ``.svd``-Datei ausgeben."""
    parser = argparse.ArgumentParser(description="PSV-Messdatei (.svd) nur lesend auswerten")
    parser.add_argument("datei", type=Path)
    args = parser.parse_args(argv)
    try:
        messung = lese_svd(args.datei)
    except (SvdFormatFehler, FileNotFoundError) as exc:
        print(f"Fehler: {exc}", file=sys.stderr)
        return 2
    print(uebersicht(messung))
    return 0


if __name__ == "__main__":  # pragma: no cover - Kommandozeileneinstieg
    raise SystemExit(main())
