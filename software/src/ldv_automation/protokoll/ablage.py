"""Ordner- und Dateinamen eines Durchgangs, Schutz gegen Überschreiben, SHA-256.

Ablage (Plan P2, 4.2; ADR-011, vorläufig bis O5)::

    <messdaten_wurzel>/<JJJJ-MM-TT_HHMMSS>_<durchgangsname>/
        durchgang.ereignisse.jsonl
        durchgang.warteschlange.json
        <nn>_<messungsname>[_v<k>].svd
        <nn>_<messungsname>[_v<k>].protokoll.json
        <nn>_<messungsname>[_v<k>].einstellungen.set   (optional)

``nn`` ist die laufende Nummer der Messung im Durchgang (ab 01, in der Reihenfolge des
ersten Starts; eine Wiederholung behält ihre Nummer). ``_v<k>`` erscheint ab dem zweiten
Versuch. Eigene Dateien entstehen mit Modus ``"x"``; das Ereignisprotokoll wird nur
ergänzt.
"""

from __future__ import annotations

import hashlib
import re
import unicodedata
from datetime import datetime
from pathlib import Path

EREIGNISPROTOKOLL = "durchgang.ereignisse.jsonl"
WARTESCHLANGENKOPIE = "durchgang.warteschlange.json"
ENDUNG_MESSDATEI = ".svd"
ENDUNG_PROTOKOLL = ".protokoll.json"
ENDUNG_EINSTELLUNGEN = ".einstellungen.set"

_MAX_NAMENSLAENGE = 60
_MAX_ORDNERVERSUCHE = 1000


def sicherer_name(name: str) -> str:
    """Bildet aus einem Anzeigenamen einen Datei- und ordnertauglichen Namen.

    Umlaute werden umschrieben (ä → ae, ß → ss), alles außer ``A-Z a-z 0-9 - _`` wird zu
    ``_``, Länge höchstens 60 Zeichen.

    Raises
    ------
    ValueError
        Wenn nach der Umwandlung nichts übrig bleibt.
    """
    ersetzt = (
        name.replace("ä", "ae")
        .replace("ö", "oe")
        .replace("ü", "ue")
        .replace("Ä", "Ae")
        .replace("Ö", "Oe")
        .replace("Ü", "Ue")
        .replace("ß", "ss")
    )
    ascii_text = unicodedata.normalize("NFKD", ersetzt).encode("ascii", "ignore").decode("ascii")
    sicher = re.sub(r"[^A-Za-z0-9_-]+", "_", ascii_text).strip("_")[:_MAX_NAMENSLAENGE]
    if not sicher:
        raise ValueError(f"Aus dem Namen {name!r} lässt sich kein Dateiname bilden")
    return sicher


def lege_durchgangsordner(wurzel: Path, name: str, zeitpunkt: datetime) -> Path:
    """Legt den Durchgangsordner neu an (nie einen vorhandenen wiederverwenden).

    Existiert der Name schon, wird ``_2``, ``_3`` … angehängt.

    Raises
    ------
    FileNotFoundError
        Wenn ``wurzel`` nicht existiert.
    RuntimeError
        Wenn nach 1000 Versuchen kein freier Name gefunden wurde.
    """
    if not wurzel.is_dir():
        raise FileNotFoundError(f"Messdaten-Wurzel existiert nicht: {wurzel}")
    basis = f"{zeitpunkt:%Y-%m-%d_%H%M%S}_{sicherer_name(name)}"
    for nummer in range(1, _MAX_ORDNERVERSUCHE + 1):
        ordner = wurzel / (basis if nummer == 1 else f"{basis}_{nummer}")
        try:
            ordner.mkdir(exist_ok=False)
        except FileExistsError:
            continue
        return ordner
    raise RuntimeError(f"Kein freier Durchgangsordner für {basis!r}")


def dateibasis(nummer: int, name: str, versuch: int) -> str:
    """Gemeinsamer Dateiname ohne Endung, z. B. ``03_Platte_oben_v2``.

    Raises
    ------
    ValueError
        Bei ``nummer < 1`` oder ``versuch < 1``.
    """
    if nummer < 1 or versuch < 1:
        raise ValueError("nummer und versuch müssen ≥ 1 sein")
    zusatz = f"_v{versuch}" if versuch > 1 else ""
    return f"{nummer:02d}_{sicherer_name(name)}{zusatz}"


def schreibe_neu(pfad: Path, text: str) -> None:
    """Schreibt eine neue Textdatei (UTF-8); wirft ``FileExistsError``, statt zu überschreiben."""
    with open(pfad, "x", encoding="utf-8", newline="\n") as datei:
        datei.write(text)


def haenge_an(pfad: Path, zeile: str) -> None:
    """Hängt eine Zeile an (legt die Datei bei Bedarf an); überschreibt nie."""
    if "\n" in zeile:
        raise ValueError("haenge_an: Zeile darf keinen Zeilenumbruch enthalten")
    with open(pfad, "a", encoding="utf-8", newline="\n") as datei:
        datei.write(zeile + "\n")


def sha256_datei(pfad: Path) -> str:
    """SHA-256 einer Datei als Hex-Text (liest blockweise; ``OSError`` wird weitergereicht)."""
    pruefsumme = hashlib.sha256()
    with open(pfad, "rb") as datei:
        for block in iter(lambda: datei.read(1 << 20), b""):
            pruefsumme.update(block)
    return pruefsumme.hexdigest()
