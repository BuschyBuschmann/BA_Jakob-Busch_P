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
import ntpath
import os
import posixpath
import re
import tempfile
import unicodedata
from collections.abc import Callable, Mapping, Sequence
from datetime import datetime
from pathlib import Path, PurePath, PurePosixPath, PureWindowsPath

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


# --- Prüfung des Messdaten-Ordners (Brief P3, 3.11; Plan P2, 4.2; K-U5b) ----------------

POLYTEC_KENNUNG = "polytec"
"""Ein Ordnerteil mit diesem Text (Groß/Klein egal) direkt unter der Laufwerkswurzel gilt
als Polytec-Programm- oder Datenordner (z. B. ``D:/Polytec``). Tiefer liegende Teile, etwa
ein Benutzerkonto ``C:/Users/Polytec``, sind erlaubt."""

WINDOWS_PROGRAMMORDNER_VARIABLEN = (
    "ProgramFiles",
    "ProgramFiles(x86)",
    "ProgramW6432",
    "ProgramData",
    "SystemRoot",
)
"""Umgebungsvariablen der Windows-Programm-, Daten- und Systemordner (dort nie Messdaten;
darunter liegen auch die Polytec-Programm- und -Datenordner)."""

_LAUFWERK = re.compile(r"^[A-Za-z]:\\?$")
_KURZNAME = re.compile(r"~\d+(\.[^.]*)?$")
"""8.3-Kurzname wie ``PROGRA~3``; bleibt er nach dem Auflösen stehen, ist der Pfad unklar."""


def geschuetzte_ordner_aus_umgebung(umgebung: Mapping[str, str] | None = None) -> tuple[str, ...]:
    """Windows-Programm- und Datenordner aus den Umgebungsvariablen (fehlende entfallen)."""
    env = os.environ if umgebung is None else umgebung
    return tuple(env[n] for n in WINDOWS_PROGRAMMORDNER_VARIABLEN if env.get(n))


def _liegt_unter(pfad: PurePath, ordner: PurePath) -> bool:
    teile = [t.casefold() for t in pfad.parts]
    basis = [t.casefold() for t in ordner.parts]
    return len(basis) > 0 and teile[: len(basis)] == basis


def _git_wurzel(pfad: Path) -> Path | None:
    for kandidat in (pfad, *pfad.parents):
        if (kandidat / ".git").exists():
            return kandidat
    return None


def _standard_aufloesen(windows: bool) -> Callable[[str], str]:
    """Auflösen eines Pfads vor allen Regeln.

    Auf dem passenden System ``os.path.realpath`` (``..``, symbolische Links, unter Windows
    Junctions und 8.3-Kurznamen vorhandener Teile), sonst nur die Normalisierung der
    jeweiligen Pfadart (Tests der Windows-Regeln unter Linux).
    """
    if windows == (os.name == "nt"):
        return os.path.realpath
    return ntpath.normpath if windows else posixpath.normpath


def pruefe_messdaten_ordner(
    pfad: Path,
    *,
    windows: bool | None = None,
    geschuetzte_ordner: Sequence[str] | None = None,
    aufloesen: Callable[[str], str] | None = None,
) -> tuple[str, ...]:
    """Prüft, ob ``pfad`` als Messdaten-Ordner taugt; gibt alle Probleme als Text zurück.

    Vor allen Regeln wird der Pfad aufgelöst (``aufloesen``: ``..``, Links, Junctions,
    Kurznamen) und ohne Rücksicht auf Groß-/Kleinschreibung verglichen. Regeln:

    1. absoluter Pfad, unter Windows mit Laufwerksbuchstaben (z. B. ``D:/Messdaten``;
       keine Netzwerkpfade ``//server/freigabe``); unter Windows kein verbleibender
       8.3-Kurzname (z. B. ``PROGRA~3``, wenn er nicht aufgelöst werden konnte);
    2. nicht unter einem Windows-Programm-, Daten- oder Systemordner (ProgramFiles,
       ProgramW6432, ProgramData, SystemRoot; dort liegen auch die Polytec-Ordner);
    3. nicht in einem Ordner „…Polytec…“ direkt unter der Laufwerkswurzel; tiefer liegende
       Ordnerteile wie ``C:/Users/Polytec`` sind erlaubt;
    4. nicht in einem Git-Repository (insbesondere nicht im Projekt-Repository);
    5. existiert, ist ein Ordner und ist beschreibbar (Probe mit einer sofort wieder
       gelöschten temporären Datei, weil ``os.access`` unter Windows Zugriffslisten nicht
       berücksichtigt).

    Parameters
    ----------
    pfad : pathlib.Path
        Zu prüfender Ordner.
    windows : bool or None
        Windows-Regeln anwenden; ``None`` = laufendes System (``os.name == "nt"``).
    geschuetzte_ordner : sequence of str or None
        Ordner, unter denen keine Messdaten liegen dürfen; ``None`` = unter Windows
        :func:`geschuetzte_ordner_aus_umgebung`, sonst keine.
    aufloesen : callable or None
        Pfadauflösung; ``None`` = :func:`_standard_aufloesen`.

    Returns
    -------
    tuple of str
        Leer, wenn der Ordner geeignet ist.
    """
    ist_windows = os.name == "nt" if windows is None else windows
    klasse: type[PurePath] = PureWindowsPath if ist_windows else PurePosixPath
    text = str(pfad)
    roh = klasse(text)
    if not roh.is_absolute() or (ist_windows and not _LAUFWERK.match(roh.drive)):
        hinweis = " mit Laufwerksbuchstaben (z. B. D:\\Messdaten)" if ist_windows else ""
        return (f"Kein absoluter Pfad{hinweis}: {text}",)
    aufgeloest_text = (aufloesen or _standard_aufloesen(ist_windows))(text)
    aufgeloest = klasse(aufgeloest_text)
    anzeige = text if aufgeloest_text == text else f"{text} (aufgelöst: {aufgeloest_text})"
    probleme: list[str] = []
    if ist_windows and any(_KURZNAME.search(teil) for teil in aufgeloest.parts[1:]):
        probleme.append(f"Kurzname (8.3) nicht auflösbar, bitte den langen Pfad angeben: {anzeige}")
    if geschuetzte_ordner is None:
        geschuetzte_ordner = geschuetzte_ordner_aus_umgebung() if ist_windows else ()
    normieren = ntpath.normpath if ist_windows else posixpath.normpath
    for ordner in geschuetzte_ordner:
        if _liegt_unter(aufgeloest, klasse(normieren(ordner))):
            probleme.append(f"Liegt in einem Programm- oder Systemordner ({ordner}): {anzeige}")
            break
    teile = aufgeloest.parts
    if len(teile) > 1 and POLYTEC_KENNUNG in teile[1].casefold():
        probleme.append(f"Liegt in einem Polytec-Verzeichnis: {anzeige}")
    if probleme:
        return tuple(probleme)
    ordner_fs = Path(aufgeloest_text) if ist_windows == (os.name == "nt") else pfad
    if not ordner_fs.is_dir():
        return (f"Ordner existiert nicht: {anzeige}",)
    git = _git_wurzel(ordner_fs.resolve())
    if git is not None:
        probleme.append(f"Liegt in einem Git-Repository ({git}); Messdaten gehören nicht dorthin")
    try:
        with tempfile.TemporaryFile(dir=ordner_fs, prefix=".ldv_schreibprobe_"):
            pass
    except OSError as fehler:
        probleme.append(f"Ordner ist nicht beschreibbar: {fehler}")
    return tuple(probleme)
