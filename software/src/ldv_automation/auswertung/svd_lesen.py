"""Prototyp-Leser für Polytec-PSV-Messdateien (``.svd``) ohne Polytec File Access.

Leser aus Paket W2 (Analyse mit Prototyp), seit P-AUSW T1.1 Teil des Pakets
(``ldv_automation.auswertung``, ADR-020; zuvor ``tools/svd_analyse``). Er liest eine
PSV-Messdatei **nur lesend** und liefert die Messdaten als NumPy-Arrays plus Metadaten. Er
importiert außer ``numpy`` und ``olefile`` nichts.

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
from collections.abc import Mapping, Sequence
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
    # M1 bestätigt 2026-11-02: Golden File, H1 aus CP/AP_Ref1 der Datei = PSV-H1 (nicht konjugiert)
    "signale.cp_phasenvorzeichen": "gesichert",
    "signale.cph_bedeutung": "plausibel",
    "signale.zeitstempel": "plausibel",
    # K-ACHSE (2026-11-02): Achse und Fft-Felder an der Datei mehrfach unabhängig belegt
    # (Polytec File Access XAxis Min 0,625 / Max 1000 Hz, GetMidX; Golden-File-Export, Spalte f
    # exakt 0,625·k; Erfassungseinstellungen am Messrechner; Regression Punktabstand gegen
    # Blockzahl (Feld +0x3C): Steigung 1,600 ± 0,017 s).
    "fft.abtastfrequenz_hz": "gesichert",
    "fft.bandbreite_hz": "gesichert",
    "fft.linien": "gesichert",
    "fft.abtastwerte": "gesichert",
    "fft.startfrequenz_hz": "plausibel",
    "fft.endfrequenz_hz": "plausibel",
    # P-AUSW T1.2: Mittelung (Typ und Anzahl) aus Info/DAQ_Settings_Fft/Average. An einer Datei
    # belegt: [1, 2, 0, 7] = Version 1, ptcAverageComplex, Feld 0 (offen), Anzahl 7 stimmt mit
    # den File-Access-Werten vom 2026-11-02 überein (ergebnisse_7b, M5). Eine zweite Datei mit
    # anderer Einstellung fehlt noch, daher nicht „gesichert“.
    "fft.mittelung": "plausibel",
    "frequenz_hz": "gesichert",
    "satz.feld_34": "offen",
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
#: ``float64``, Bedeutung **unbekannt** (an der Beispieldatei 0,64). Es ist **nicht** die
#: Blockdauer: diese ist T = N/f_s = 1,6 s = 1/Δf (K-ACHSE). Wird roh durchgereicht.
SATZ_FELD_34 = 0x34
#: ``float64`` je Punkt (Bedeutung offen). Als float32 bitgleich mit dem Messpunktfeld
#: +0x08 desselben Punkts; dient als Anker der Punktzuordnung (``svd_pruefung``).
SATZ_KENNFELD = 0x8C
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
    feld_34 : float
        Rohwert des Satzfeldes +0x34 (``float64``, **Bedeutung unbekannt**, in allen Sätzen
        bitgleich). Keine Blockdauer, nicht für Rechnungen verwenden.
    platz : tuple of int
        Ablageplatz (Scanreihenfolge) je Punktindex.
    kennfeld : numpy.ndarray
        ``float64`` aus Satz +0x8C je Punktindex (Bedeutung offen, Zuordnungsanker).
    """

    werte: FloatArray
    linien: int
    zeit_a: list[dt.datetime]
    zeit_b: list[dt.datetime]
    feld_34: float
    platz: tuple[int, ...]
    kennfeld: FloatArray


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
    feld_34: float | None = None
    kennfeld = np.full(n, np.nan, dtype=np.float64)
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
        satz_feld_34 = _f64(daten, basis + SATZ_FELD_34)
        if feld_34 is None:
            feld_34 = satz_feld_34
        elif satz_feld_34 != feld_34:  # Bitgleichheit: Kopffeld ist kopiert, nicht gerechnet
            raise SvdFormatFehler(f"Datensatz {platz}: Feld +0x34 {satz_feld_34} != {feld_34}")
        punkt = _i32(daten, basis + SATZ_PUNKT)
        if not 0 <= punkt < n or zeit_a[punkt] is not None:
            raise SvdFormatFehler(f"Datensatz {platz}: Punktindex {punkt} ungültig/doppelt")
        if info.platz_je_punkt[punkt] != platz:
            raise SvdFormatFehler(f"Punkt {punkt}: Platz {platz} widerspricht ManyStreamsInfo")
        roh = np.frombuffer(daten, dtype="<f4", count=n_float, offset=basis + SATZ_DATEN)
        werte[punkt] = roh.astype(np.float64)
        kennfeld[punkt] = _f64(daten, basis + SATZ_KENNFELD)
        ta, tb = struct.unpack_from("<QQ", daten, basis + SATZ_ZEIT_A)
        zeit_a[punkt] = filetime_zu_datetime(ta)
        zeit_b[punkt] = filetime_zu_datetime(tb)
    assert linien is not None and feld_34 is not None  # n > 0 durch StromInfo garantiert
    return Punktdaten(
        werte,
        linien,
        [z for z in zeit_a if z is not None],
        [z for z in zeit_b if z is not None],
        feld_34,
        info.platz_je_punkt,
        kennfeld,
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


def kanalanker_aus_einstellungen(daten: bytes) -> dict[str, int]:
    """Zeitkanalnummer ``T[i]`` je Kanalkurzname aus ``Info/DAQ_Settings_Fft/Channels``.

    Der Stream nennt die Kanäle in Kanalreihenfolge als Paare (Kurzname, Langname), z. B.
    ``Vib 3D``, ``Vibrometer 3D``, ``Ref1``, ``Reference 1`` … Ein 3D-Kanal belegt drei
    Zeitkanäle (``Vib X``, ``Vib Y``, ``Vib Z``), jeder andere einen. An der Beispieldatei
    ergibt das ``Vib X/Y/Z`` = 0/1/2, ``Ref1`` = 3, ``Ref2`` = 4, passend zu allen Formeln
    (plausibel).

    Raises
    ------
    SvdFormatFehler
        Wenn die Texte nicht paarweise vorliegen oder ein Name doppelt vorkommt.
    """
    texte = [t for _, t in utf16_zeichenketten(daten)]
    if not texte or len(texte) % 2:
        raise SvdFormatFehler(f"Channels: Kanalnamen nicht paarweise: {texte}")
    anker: dict[str, int] = {}
    nummer = 0
    for kurz in texte[0::2]:
        namen = [f"{kurz[:-3]} {a}" for a in "XYZ"] if kurz.endswith(" 3D") else [kurz]
        for name in namen:
            if name in anker:
                raise SvdFormatFehler(f"Channels: Kanalname doppelt: {name!r}")
            anker[name] = nummer
            nummer += 1
    return anker


_NAME_REF = re.compile(r"^Ref(\d+)$")
_NAME_VIB = re.compile(r"^Vib ([XYZ])$")


def _namensschluessel(name: str) -> tuple[int, int] | None:
    """Ordnungsschlüssel aus dem Namen: Vib X < Vib Y < Vib Z < Ref1 < Ref2 < usw."""
    if (t := _NAME_VIB.match(name)) is not None:
        return (0, "XYZ".index(t.group(1)))
    if (t := _NAME_REF.match(name)) is not None:
        return (1, int(t.group(1)))
    return None


def rollen_aus_formel(
    formel: str, kanaele: Sequence[str], anker: Mapping[str, int] | None = None
) -> tuple[str, ...]:
    """Ordnet die Kanäle nach Rolle (Antwort zuerst) anhand der Formel.

    Rollen laut Formel: ``CP[Antwort, Referenz]``, ``CPH[S[Antwort], CP[Antwort,
    Referenz]]``, ``AP[Kanal]``, ``ABS[Kanal]``. Die Formel nennt Zeitkanalnummern
    ``T[i]``; die Zuordnung Nummer ↔ Name stützt sich **nicht** auf die
    Static_Info-Reihenfolge, sondern auf unabhängige Anker:

    * ``anker`` aus :func:`kanalanker_aus_einstellungen` (absolute Nummer je Name) und
    * die Namensordnung ``Vib X < Vib Y < Vib Z < Ref1 < Ref2 …`` (relative Ordnung).

    Liegen beide vor, müssen sie übereinstimmen. Fehlt jeder Anker oder widersprechen sie
    sich, folgt ``SvdFormatFehler`` (kein stilles Raten). 3D-Komponenten müssen zum Namen
    passen (``Vib X`` zu ``3DX``).

    Parameters
    ----------
    formel : str
        Formel aus Static_Info, z. B. ``"AVG[CP[S[T[4]],S[T[3]]]]"``.
    kanaele : sequence of str
        Kurznamen der beteiligten Kanäle (Static_Info, Reihenfolge ohne Bedeutung).
    anker : mapping of str to int, optional
        Zeitkanalnummer je Kurzname aus den Kanaleinstellungen.

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
    if len(nummern) != len(schluessel) or len(nummern) != len(set(kanaele)):
        raise SvdFormatFehler(f"Kanalzahl passt nicht: {formel!r} gegen {list(kanaele)}")
    zuordnungen: list[dict[int, str]] = []
    if anker is not None:
        fehlt = [k for k in kanaele if k not in anker]
        if fehlt:
            raise SvdFormatFehler(f"Kanal ohne Anker in den Kanaleinstellungen: {fehlt}")
        zuordnungen.append({anker[k]: k for k in kanaele})
    namens_schluessel = [_namensschluessel(k) for k in kanaele]
    if all(ns is not None for ns in namens_schluessel):
        sortiert = [k for _, k in sorted(zip(namens_schluessel, kanaele, strict=True))]
        zuordnungen.append(dict(zip(nummern, sortiert, strict=True)))
    if not zuordnungen:
        raise SvdFormatFehler(f"Kein Anker für die Kanalzuordnung: {list(kanaele)}")
    if any(z != zuordnungen[0] for z in zuordnungen[1:]):
        raise SvdFormatFehler(f"Kanalanker widersprechen sich: {zuordnungen}")
    name_je_nummer = zuordnungen[0]
    if set(name_je_nummer) != set(nummern):
        raise SvdFormatFehler(f"Kanalnummern {nummern} passen nicht zum Anker {name_je_nummer}")
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
    r"""Inhalt von ``Info/DAQ_Settings_Fft/Fft`` (Auszug).

    Die Frequenzauflösung folgt aus Abtastfrequenz und Blocklänge, :math:`\Delta f = f_s/N = 1/T`
    mit :math:`T = N/f_s`. Das Feld bei +4 ist die **Abtastfrequenz**, nicht die Bandbreite
    (K-ACHSE, 2026-11-02; Beispieldatei: 2500 Hz, N = 4000, T = 1,6 s, Δf = 0,625 Hz, Bandbreite
    1000 Hz).

    Attributes
    ----------
    abtastfrequenz_hz : float
        Abtastfrequenz :math:`f_s` in Hz (+4).
    linien : int
        Anzahl FFT-Linien (+12).
    abtastwerte : int
        Abtastwerte :math:`N` je Block (+16).
    startfrequenz_hz : float
        Startfrequenz in Hz (+20); der Leser verlangt 0 (Zoom-FFT ungeprüft).
    bandbreite_hz : float
        Bandbreite in Hz (+28), = Linien · Δf.
    endfrequenz_hz : float
        Endfrequenz in Hz (+36), = Startfrequenz + Bandbreite.
    """

    abtastfrequenz_hz: float
    linien: int
    abtastwerte: int
    startfrequenz_hz: float
    bandbreite_hz: float
    endfrequenz_hz: float

    @property
    def delta_f_hz(self) -> float:
        """Frequenzauflösung in Hz, :math:`f_s/N = 1/T`."""
        return self.abtastfrequenz_hz / self.abtastwerte

    @property
    def blockdauer_s(self) -> float:
        """Blockdauer :math:`T = N/f_s` in s (Beispieldatei: 1,6 s)."""
        return self.abtastwerte / self.abtastfrequenz_hz


#: Relative Toleranz der Konsistenzprüfungen der Fft-Felder (float64 aus denselben
#: Einstellungen, Abweichung nur durch Rundung ~1e-16).
_FFT_RTOL = 1e-9


def dekodiere_fft_einstellungen(daten: bytes) -> FftEinstellungen:
    """Dekodiert ``Info/DAQ_Settings_Fft/Fft`` (Auszug).

    Layout: ``int32`` Version 2, ``float64`` Abtastfrequenz (+4), ``int32`` Linien (+12),
    ``int32`` Abtastwerte (+16), ``float64`` Startfrequenz (+20), ``float64`` Bandbreite (+28),
    ``float64`` Endfrequenz (+36); der Rest bleibt offen.

    Raises
    ------
    SvdFormatFehler
        Bei unbekannter Version, zu kurzem Stream, unplausiblen Werten, Startfrequenz ≠ 0
        (Zoom-FFT nicht geprüft) oder wenn Bandbreite/Endfrequenz nicht zu Linien · Δf passen.
    """
    if len(daten) < 44 or _i32(daten, 0) != 2:
        raise SvdFormatFehler("Fft-Einstellungen: unbekannte Version oder zu kurz")
    fs = _f64(daten, 4)
    linien = _i32(daten, 12)
    abtast = _i32(daten, 16)
    start = _f64(daten, 20)
    bw = _f64(daten, 28)
    ende = _f64(daten, 36)
    if not (
        np.isfinite(fs)
        and fs > 0
        and linien > 0
        and abtast > 0
        and np.isfinite(start)
        and np.isfinite(bw)
        and bw > 0
        and np.isfinite(ende)
    ):
        raise SvdFormatFehler(
            f"Fft-Einstellungen unplausibel: fs={fs}, Linien={linien}, N={abtast}, "
            f"Start={start}, Bandbreite={bw}, Ende={ende}"
        )
    if start != 0.0:
        raise SvdFormatFehler(
            f"Fft-Einstellungen: Startfrequenz {start} Hz ≠ 0 (Zoom-FFT ist nicht geprüft)"
        )
    if not np.isclose(ende, start + bw, rtol=_FFT_RTOL, atol=0.0):
        raise SvdFormatFehler(f"Fft-Einstellungen: Endfrequenz {ende} Hz ≠ Start + Bandbreite")
    delta_f = fs / abtast
    if not np.isclose(bw / linien, delta_f, rtol=_FFT_RTOL, atol=0.0):
        raise SvdFormatFehler(
            f"Fft-Einstellungen: Bandbreite/Linien = {bw / linien} Hz passt nicht zu "
            f"fs/N = {delta_f} Hz"
        )
    return FftEinstellungen(fs, linien, abtast, start, bw, ende)


#: Ob das Fenster (``WindowFunction``) aus der Datei lesbar ist. **Nein**: In File Access ist es
#: eine Kanaleigenschaft (``ChannelAcqProperties.WindowFunction``), vermutlich im Stream
#: ``Info/DAQ_Settings_Fft/Channels`` (je Kanal ein Satz). Das Fenster der Beispieldatei ist
#: Rechteck, also Code 0; dieser Wert steckt aber in allen Streams unter ``DAQ_Settings_Fft``
#: (``Average``, ``Fft``, ``Global``, ``SignalEnhancement``, ``Trigger``, ``FrontEnd``,
#: ``Channels``) in sehr vielen Nullfeldern, ein Feld lässt sich nicht herausgreifen. Eine
#: zweite Datei mit anderem Fenster (z. B. Hanning, Code 7) würde die Zuordnung per Diff
#: ermöglichen. Bis dahin liefert der Leser kein Fenster-Feld (kein toter Platzhalter); die
#: Oberfläche zeigt „–“ mit Tooltip (P-AUSW U-1).
FENSTER_IN_DATEI_LESBAR = False

MITTELUNG_LAENGE = 16
"""Länge des Streams ``Info/DAQ_Settings_Fft/Average`` an der Beispieldatei (vier ``int32``)."""

MITTELUNG_VERSION = 1
"""Erste ``int32`` des Streams ``Average`` (Layoutversion)."""

#: Mittelungsarten laut ``PTCAverageType`` (Polytec File Access / Basic Engine, Enum 0–4).
MITTELUNG_TYPEN: dict[int, str] = {
    0: "aus",
    1: "Betrag",
    2: "komplex",
    3: "Zeit",
    4: "Peak Hold",
}


@dataclass(frozen=True)
class Mittelung:
    """Mittelungseinstellung der Messung (``Info/DAQ_Settings_Fft/Average``).

    Sicherheitsgrad „plausibel“ (:data:`SICHERHEIT`, Schlüssel ``fft.mittelung``).

    Attributes
    ----------
    typ : int
        Mittelungsart nach ``PTCAverageType``: 0 aus, 1 Betrag, 2 komplex, 3 Zeit, 4 Peak Hold.
    anzahl : int
        Anzahl der Mittelungen (≥ 1).
    """

    typ: int
    anzahl: int

    @property
    def typ_name(self) -> str:
        """Name der Mittelungsart (Schlüssel von :data:`MITTELUNG_TYPEN`)."""
        return MITTELUNG_TYPEN[self.typ]


def dekodiere_mittelung(daten: bytes) -> Mittelung | None:
    """Dekodiert ``Info/DAQ_Settings_Fft/Average``; ``None``, wenn das Layout nicht passt.

    Layout (Beispieldatei, W2 3.4): vier ``int32`` ``[Version, Typ, Feld, Anzahl]`` mit
    Version 1, Typ nach :data:`MITTELUNG_TYPEN` (``PTCAverageType`` 0–4) und Anzahl ≥ 1; das
    dritte Feld (+8, Beispieldatei 0) ist offen und wird nicht gelesen. Die Prüfung ist
    **strikt**: Länge, Version, Typbereich und Anzahl müssen passen, sonst wird nichts
    geraten und ``None`` zurückgegeben (die Oberfläche zeigt dann „–“).

    Parameters
    ----------
    daten : bytes
        Inhalt des Streams.

    Returns
    -------
    Mittelung or None
        ``None`` bei abweichender Länge, Version ≠ 1, Typ außerhalb 0–4 oder Anzahl < 1.
    """
    if len(daten) != MITTELUNG_LAENGE or _i32(daten, 0) != MITTELUNG_VERSION:
        return None
    typ = _i32(daten, 4)
    anzahl = _i32(daten, 12)
    if typ not in MITTELUNG_TYPEN or anzahl < 1:
        return None
    return Mittelung(typ, anzahl)


#: Länge des entpackten ``Band_Data/.../BandInfo-0`` an der Beispieldatei.
_BANDINFO_LAENGE = 36

#: Ergebnisse der Gegenprobe gegen ``BandInfo-0`` (Feld :attr:`SvdMessung.band_info`).
BAND_INFO_GEPRUEFT = "geprüft"
BAND_INFO_NICHT_PRUEFBAR = "nicht prüfbar (Layout unbekannt)"
BAND_INFO_FEHLT = "nicht prüfbar (BandInfo-0 fehlt)"
BAND_INFO_WIDERSPRUCH = "Widerspruch (Linien, Δf oder Obergrenze weichen von Fft ab)"


def pruefe_band_info(daten: bytes, fft: FftEinstellungen) -> str:
    """Gegenprobe der Frequenzachse gegen ``Band_Data/Entire_Bandwidth/FB0/BandInfo-0``.

    Layout (an der Beispieldatei erschlossen, sonst offen): ``uint32`` Länge, zlib-Daten;
    entpackt 36 Byte mit ``int32`` Linien bei +2, ``float32`` untere Bandgrenze bzw. erste
    Linie bei +20 (hier = Δf, 0,625 Hz) und ``float32`` Obergrenze bei +28 (1000 Hz).

    Returns
    -------
    str
        :data:`BAND_INFO_GEPRUEFT`, :data:`BAND_INFO_NICHT_PRUEFBAR` (Layout nicht erkannt)
        oder :data:`BAND_INFO_WIDERSPRUCH`. Es gibt keinen Abbruch: der Leser meldet den
        Befund nur (Feld ``SvdMessung.band_info`` und Übersicht).
    """
    if len(daten) < 5:
        return BAND_INFO_NICHT_PRUEFBAR
    try:
        roh = zlib.decompress(daten[4:])
    except zlib.error:
        return BAND_INFO_NICHT_PRUEFBAR
    if len(roh) != _BANDINFO_LAENGE:
        return BAND_INFO_NICHT_PRUEFBAR
    linien = _i32(roh, 2)
    erste, obergrenze = struct.unpack_from("<f", roh, 20)[0], struct.unpack_from("<f", roh, 28)[0]
    # float32-Darstellung: relative Genauigkeit 6e-8, Toleranz 1e-6
    if not (
        linien == fft.linien
        and np.isclose(erste, fft.delta_f_hz, rtol=1e-6, atol=0.0)
        and np.isclose(obergrenze, fft.endfrequenz_hz, rtol=1e-6, atol=0.0)
    ):
        return BAND_INFO_WIDERSPRUCH
    return BAND_INFO_GEPRUEFT


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
        Abtastfrequenz, Linien, Abtastwerte, Start-/Bandbreite/Endfrequenz.
    frequenz_hz : numpy.ndarray
        Frequenzachse ``k · Δf``, ``k = 1 … Linien`` (gesichert; Beispieldatei
        0,625 … 1000 Hz, Δf = 0,625 Hz; Index 0 ist die Linie 1, DC fehlt).
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
    satz_kennfeld : numpy.ndarray
        Satzfeld +0x8C je Punktindex, in allen Signalen gleich (Bedeutung offen).
    satz_feld_34 : float or None
        Rohwert des Satzfeldes +0x34, in allen Sätzen und Signalen bitgleich (Bedeutung
        **unbekannt**, keine Blockdauer).
    band_info : str
        Ergebnis der Gegenprobe gegen ``BandInfo-0`` (:data:`BAND_INFO_GEPRUEFT`,
        :data:`BAND_INFO_NICHT_PRUEFBAR`, :data:`BAND_INFO_FEHLT`, :data:`BAND_INFO_WIDERSPRUCH`).
        Ein Widerspruch bricht nicht ab, wird aber in :func:`uebersicht` ausdrücklich gemeldet.
    mittelung : Mittelung or None
        Mittelungsart und -anzahl aus ``Info/DAQ_Settings_Fft/Average`` (Sicherheitsgrad
        „plausibel“). ``None`` = Stream fehlt oder weicht vom erwarteten Layout ab. Das Fenster
        ist nicht lesbar (:data:`FENSTER_IN_DATEI_LESBAR`), der Leser hat dafür kein Feld.
    datei_zeit : datetime.datetime or None
        FILETIME aus dem Stream ``FileVersion`` (Offset 24), naiv. Gegenprobe an der
        Beispieldatei: 09:32:52, die COM-Eigenschaft ``Version.FileTime`` meldet 11:32:52
        (Ortszeit MESZ), der Stream enthält also vermutlich UTC (Zeitzone nicht gesichert).
        ``None`` = nicht verfügbar (Stream fehlt oder weicht vom Layout ab).

    Notes
    -----
    Die Programmversion (z. B. „10.4.0.1“) ist **nicht** Teil des Ergebnisses: Der Stream
    ``FileVersion`` enthält nur zwei ``uint16`` (4, 10), deren Zuordnung zu Haupt- und
    Nebenversion offen ist; Revision und Build fehlen. Sie liefert nur die COM-Eigenschaft
    ``Version.ProgramVersionString``.
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
    satz_kennfeld: FloatArray = field(default_factory=lambda: np.zeros(0, dtype=np.float64))
    satz_feld_34: float | None = None
    band_info: str = BAND_INFO_NICHT_PRUEFBAR
    datei_zeit: dt.datetime | None = None
    mittelung: Mittelung | None = None


FILE_VERSION_LAENGE = 32
"""Länge des Streams ``FileVersion`` an der Beispieldatei (Byte)."""

FILE_VERSION_FILETIME_OFFSET = 24
"""Offset der FILETIME im Stream ``FileVersion`` (fünf ``int32`` und zwei ``uint16`` davor)."""

FILE_VERSION_UNTERGRENZE = dt.datetime(1601, 1, 2)
"""Früheste plausible Dateizeit aus ``FileVersion``. Werte davor (FILETIME 0 bzw. alles
auf 1601-01-01) gelten als nicht gesetzt und ergeben ``None``. Annahme, kein Mindestdatum."""


def dekodiere_file_version(daten: bytes) -> dt.datetime | None:
    """FILETIME aus dem Stream ``FileVersion``; ``None``, wenn das Layout nicht passt.

    Layout (Beispieldatei, W2 Abschnitt 1.1): ``int32`` 2, 4, 2624, 2, 1, ``uint16`` 4, 10,
    ``uint64`` FILETIME. Geprüft werden Länge und die erste ``int32`` (2); bei Abweichung
    oder unplausibler FILETIME wird nichts geraten. FILETIME 0 (und alles, was vor
    :data:`FILE_VERSION_UNTERGRENZE` fällt) ist „nicht gesetzt“ und ergibt ``None``.
    """
    if len(daten) != FILE_VERSION_LAENGE or _i32(daten, 0) != 2:
        return None
    (filetime,) = struct.unpack_from("<Q", daten, FILE_VERSION_FILETIME_OFFSET)
    try:
        zeit = filetime_zu_datetime(filetime)
    except SvdFormatFehler:
        return None
    if zeit < FILE_VERSION_UNTERGRENZE:
        return None
    return zeit


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
    pfad_band_info = "Band_Data/Entire_Bandwidth/FB0/BandInfo-0"
    band_info = (
        pruefe_band_info(_strom(ole, pfad_band_info), fft)
        if ole.exists(pfad_band_info)
        else BAND_INFO_FEHLT
    )
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
    pfad_kanaele = "Info/DAQ_Settings_Fft/Channels"
    anker = (
        kanalanker_aus_einstellungen(_strom(ole, pfad_kanaele))
        if ole.exists(pfad_kanaele)
        else None
    )
    scan_platz: tuple[int, ...] | None = None
    kennfeld: FloatArray = np.zeros(0, dtype=np.float64)
    feld_34: float | None = None
    for nr in _nummerierte_storages(ole, "Polytec_Data"):
        basis = f"Polytec_Data/M{nr}"
        sig = dekodiere_signal_info(_strom(ole, f"{basis}/Signal_Info"))
        info = dekodiere_strom_info(_strom(ole, f"{basis}/ManyStreamsInfo"))
        daten = dekodiere_punktdaten(_strom(ole, f"{basis}/ManyStreamsData-0"), info, sig)
        if scan_platz is None:
            scan_platz = daten.platz
            kennfeld = daten.kennfeld
            feld_34 = daten.feld_34
        elif daten.platz != scan_platz:
            raise SvdFormatFehler(f"M{nr}: Scanreihenfolge weicht von M0 ab")
        elif not np.array_equal(daten.kennfeld, kennfeld, equal_nan=True):
            raise SvdFormatFehler(f"M{nr}: Satzfeld +0x8C weicht von M0 ab")
        elif daten.feld_34 != feld_34:
            raise SvdFormatFehler(f"M{nr}: Satzfeld +0x34 weicht von M0 ab")
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
        kanaele = rollen_aus_formel(stat.formel, stat.kanaele, anker)
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
    datei_zeit = (
        dekodiere_file_version(_strom(ole, "FileVersion")) if ole.exists("FileVersion") else None
    )
    pfad_mittelung = "Info/DAQ_Settings_Fft/Average"
    mittelung = (
        dekodiere_mittelung(_strom(ole, pfad_mittelung)) if ole.exists(pfad_mittelung) else None
    )
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
        kennfeld,
        feld_34,
        band_info,
        datei_zeit,
        mittelung,
    )


def uebersicht(messung: SvdMessung) -> str:
    """Erzeugt eine Textübersicht mit Sicherheitsgraden."""
    f = messung.fft
    zeilen = [
        f"Datei: {messung.pfad.name}",
        f"FFT: Abtastfrequenz {f.abtastfrequenz_hz:g} Hz, Bandbreite {f.bandbreite_hz:g} Hz, "
        f"{f.linien} Linien, Δf = {f.delta_f_hz:g} Hz, {f.abtastwerte} Abtastwerte/Block "
        f"(T = {f.blockdauer_s:g} s) [{SICHERHEIT['fft.linien']}]",
        f"Frequenzachse: {messung.frequenz_hz[0]:g} … {messung.frequenz_hz[-1]:g} Hz "
        f"[{SICHERHEIT['frequenz_hz']}]",
        "Mittelung: "
        + (
            "nicht verfügbar"
            if messung.mittelung is None
            else f"{messung.mittelung.typ_name}, Anzahl {messung.mittelung.anzahl}"
        )
        + f" [{SICHERHEIT['fft.mittelung']}]; Fenster: nicht lesbar",
        ("WARNUNG " if messung.band_info == BAND_INFO_WIDERSPRUCH else "")
        + f"Gegenprobe BandInfo-0 (Δf 0,625 Hz / Obergrenze): {messung.band_info}",
        f"Messpunkte: {len(messung.punkte.index)} (Label {messung.punkte.label.min()} … "
        f"{messung.punkte.label.max()}), Elemente: {len(messung.elemente)}",
    ]
    lo = messung.punkte.koordinaten_m.min(axis=0)
    hi = messung.punkte.koordinaten_m.max(axis=0)
    zeilen.append(
        "Koordinaten [m, plausibel]: "
        + ", ".join(f"{a} {u:.4f} … {o:.4f}" for a, u, o in zip("xyz", lo, hi, strict=True))
    )
    zeilen.append(
        "Dateizeit (FileVersion, naiv, vermutlich UTC): "
        + (
            "nicht verfügbar"
            if messung.datei_zeit is None
            else f"{messung.datei_zeit:%Y-%m-%d %H:%M:%S}"
        )
        + "; Programmversion: nicht verfügbar (nur über COM)"
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
