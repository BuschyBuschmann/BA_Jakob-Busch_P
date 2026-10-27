"""Messprotokoll je Messung und Ereignisprotokoll je Durchgang (R-020, Plan P2 4.3).

Messprotokoll: JSON, ``schema_version`` 1, eine Datei je Messversuch, Modus ``"x"``.
Pflichtfelder siehe :data:`PFLICHTFELDER`; jedes Feld ist immer vorhanden, auch bei
``fehler`` und ``abgebrochen`` (dann ggf. mit ``null``). Einheiten stehen im Feldnamen.

Nicht endliche Gleitkommawerte (NaN, ±Inf), etwa aus dem Einstellungsstand des Geräts,
verhindern das Protokoll nicht: Sie werden als Text ``"NaN"``, ``"Infinity"`` bzw.
``"-Infinity"`` geschrieben (gültiges JSON, Wert erkennbar). Auswertende Programme müssen
diese Texte an numerischen Stellen erwarten.

Zeitstempel sind Objekte ``{"lokal": "<ISO 8601 mit Zone>", "utc": "<ISO 8601, UTC>"}``.

Ereignisprotokoll: JSON Lines, eine Zeile je Ereignis, nur anhängend.
"""

from __future__ import annotations

import json
import math
from collections.abc import Mapping
from datetime import UTC, datetime
from pathlib import Path

from ldv_automation.geraet.schnittstelle import EinstellungsStand, GeraeteFehler
from ldv_automation.protokoll.ablage import haenge_an, schreibe_neu

SCHEMA_VERSION = 1

PFLICHTFELDER: tuple[str, ...] = (
    "schema_version",
    # Zuordnung
    "messung_id",
    "name",
    "versuch",
    "durchgang_id",
    "position",
    "messdatei",
    "messdatei_sha256",
    "messdatei_sha256_grund",
    # Status
    "status",
    "fehler",
    "fehlerstrategie",
    "fehlerentscheidung",
    # Zeit
    "zeit_start",
    "zeit_ende",
    "dauer_s",
    "zeitlimit_s",
    # Versionen
    "paket_version",
    "git_hash",
    "git_hash_grund",
    "git_dirty",
    "psv_version",
    "betriebsart",
    # Gerät
    "hardware",
    "messpunkte_anzahl",
    # Einstellungen
    "einstellungsdatei",
    "lademaske",
    "geaenderte_parameter",
    "einstellungen_ist",
    # Meldungen, Fortschritt, Einschränkungen
    "meldungen",
    "meldungen_hinweis",
    "fortschritt_quelle",
    "einschraenkungen",
    # Konfigurationsdatei des Messrechners (K-U5): Pfad, SHA-256, verwendete Werte
    "konfiguration",
)
"""Felder, die jedes Messprotokoll enthält (Plan P2, 4.3)."""

MELDUNGEN_HINWEIS = (
    "Ohne Ereignisbetrieb werden Meldungen nicht empfangen; sie stehen in der Messdatei "
    "(SummaryInfo.Subject)."
)


def zeitstempel(zeitpunkt: datetime) -> dict[str, str]:
    """ISO-8601-Zeitstempel lokal (mit Zone) und in UTC.

    Raises
    ------
    ValueError
        Bei zeitzonenloser ``datetime``.
    """
    if zeitpunkt.tzinfo is None:
        raise ValueError("zeitstempel: datetime muss zeitzonenbehaftet sein")
    return {"lokal": zeitpunkt.isoformat(), "utc": zeitpunkt.astimezone(UTC).isoformat()}


def fehler_zu_dict(art: str, text: str, fehler: BaseException | None = None) -> dict[str, object]:
    """Fehlerobjekt für das Protokollfeld ``fehler`` (mit ``hresult``/``excepinfo``)."""
    ergebnis: dict[str, object] = {
        "art": art,
        "text": text,
        "hresult": None,
        "excepinfo": None,
        "methode": None,
    }
    if isinstance(fehler, GeraeteFehler):
        ergebnis["hresult"] = fehler.hresult
        ergebnis["excepinfo"] = fehler.excepinfo
        ergebnis["methode"] = fehler.methode
    return ergebnis


def einstellungsstand_zu_dict(stand: EinstellungsStand) -> dict[str, object]:
    """Wandelt einen :class:`EinstellungsStand` in JSON-fähige Daten."""
    return {
        "modus": stand.modus,
        "messpunkte_anzahl": stand.messpunkte_anzahl,
        "generator_aktiv": stand.generator_aktiv,
        "generator_amplitude_v": stand.generator_amplitude_v,
        "gruppen": {name: dict(werte) for name, werte in stand.gruppen.items()},
    }


def json_sicher(wert: object) -> object:
    """Ersetzt nicht endliche ``float`` rekursiv durch Text (``"NaN"``, ``"[-]Infinity"``).

    Durchläuft ``dict`` (Schlüssel bleiben), ``list`` und ``tuple`` (werden zu ``list``);
    alle anderen Werte bleiben unverändert.
    """
    if isinstance(wert, float) and not math.isfinite(wert):
        if math.isnan(wert):
            return "NaN"
        return "Infinity" if wert > 0 else "-Infinity"
    if isinstance(wert, Mapping):
        return {k: json_sicher(v) for k, v in wert.items()}
    if isinstance(wert, list | tuple):
        return [json_sicher(v) for v in wert]
    return wert


def fehlende_pflichtfelder(daten: Mapping[str, object]) -> list[str]:
    """Pflichtfelder, die in ``daten`` fehlen (leer = vollständig)."""
    return [feld for feld in PFLICHTFELDER if feld not in daten]


def schreibe_messprotokoll(pfad: Path, daten: Mapping[str, object]) -> None:
    """Schreibt ein Messprotokoll neu (nie überschreiben).

    Raises
    ------
    ValueError
        Wenn Pflichtfelder fehlen oder unbekannte Felder enthalten sind.
    FileExistsError
        Wenn die Datei schon existiert.
    """
    fehlend = fehlende_pflichtfelder(daten)
    unbekannt = sorted(set(daten) - set(PFLICHTFELDER))
    if fehlend or unbekannt:
        raise ValueError(f"Messprotokoll: fehlend {fehlend}, unbekannt {unbekannt}")
    if daten["schema_version"] != SCHEMA_VERSION:
        raise ValueError(f"Messprotokoll: schema_version muss {SCHEMA_VERSION} sein")
    geordnet = {feld: json_sicher(daten[feld]) for feld in PFLICHTFELDER}
    text = json.dumps(geordnet, ensure_ascii=False, indent=2, allow_nan=False) + "\n"
    schreibe_neu(pfad, text)


class Ereignisprotokoll:
    """Nur anhängendes Ereignisprotokoll eines Durchgangs (JSON Lines).

    Parameters
    ----------
    pfad : pathlib.Path
        Datei ``durchgang.ereignisse.jsonl``; darf beim Anlegen noch nicht existieren.

    Raises
    ------
    FileExistsError
        Wenn die Datei schon existiert (ein neuer Durchgang beginnt nie in einer alten Datei).
    """

    def __init__(self, pfad: Path) -> None:
        schreibe_neu(pfad, "")
        self.pfad = pfad

    def schreibe(self, zeitpunkt: datetime, art: str, daten: Mapping[str, object]) -> None:
        """Hängt ein Ereignis an."""
        zeile = json_sicher({"zeit": zeitstempel(zeitpunkt), "art": art, **daten})
        haenge_an(self.pfad, json.dumps(zeile, ensure_ascii=False, default=str, allow_nan=False))
