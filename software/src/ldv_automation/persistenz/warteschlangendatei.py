"""Warteschlange als JSON-Datei speichern und streng geprüft laden (R-021).

Format (``schema_version`` 1, UTF-8, Endung ``.warteschlange.json``)::

    {"schema_version": 1, "art": "ldv-warteschlange", "erstellt_utc": "...",
     "paket_version": "...", "git_hash": "..." | null,
     "eintraege": [
        {"art": "messung", "id": "<uuid>", "name": "...", "einstellungsdatei": "...",
         "parameter": {"<schluessel>": <wert>}, "zeitlimit_s": <zahl> | null, "notiz": "..."},
        {"art": "pausenpunkt", "id": "<uuid>", "text": "..."}]}

Gespeichert werden nur Definitionen. Nach dem Laden sind alle Einträge ``WARTEND`` mit
Versuchszähler 1. Die Datei ist kein Rohdatum; Überschreiben ist daher möglich, muss aber
ausdrücklich verlangt werden.
"""

from __future__ import annotations

import json
import os
from collections.abc import Callable, Sequence
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from uuid import UUID

from ldv_automation.domaene.eintraege import Eintrag, Messung, Pausenpunkt
from ldv_automation.domaene.parameter import KATALOG

SCHEMA_VERSION = 1
ART_DATEI = "ldv-warteschlange"
DATEIENDUNG = ".warteschlange.json"

_KOPF_SCHLUESSEL = {
    "schema_version",
    "art",
    "erstellt_utc",
    "paket_version",
    "git_hash",
    "eintraege",
}
_MESSUNG_SCHLUESSEL = {
    "art",
    "id",
    "name",
    "einstellungsdatei",
    "parameter",
    "zeitlimit_s",
    "notiz",
}
_PAUSENPUNKT_SCHLUESSEL = {"art", "id", "text"}


@dataclass(frozen=True, kw_only=True)
class LadeErgebnis:
    """Ergebnis von :func:`lade_warteschlange`.

    Parameters
    ----------
    eintraege : tuple
        Geladene Einträge, alle ``WARTEND``.
    warnungen : tuple of str
        Hinweise, die den Ladevorgang nicht abbrechen (z. B. fehlende Einstellungsdatei,
        weil die Datei auf einem anderen Rechner entstanden sein kann).
    erstellt_utc, paket_version : str
        Kopfdaten der Datei.
    git_hash : str or None
        Git-Hash des erzeugenden Stands, falls bekannt.
    """

    eintraege: tuple[Eintrag, ...]
    warnungen: tuple[str, ...]
    erstellt_utc: str
    paket_version: str
    git_hash: str | None


def _jetzt_utc() -> datetime:
    return datetime.now(UTC)


def eintrag_zu_dict(eintrag: Eintrag) -> dict[str, object]:
    """Wandelt einen Eintrag in seine Dateidarstellung (nur Definition, ohne Zustand)."""
    if isinstance(eintrag, Messung):
        return {
            "art": "messung",
            "id": str(eintrag.id),
            "name": eintrag.name,
            "einstellungsdatei": eintrag.einstellungsdatei,
            "parameter": dict(eintrag.parameter),
            "zeitlimit_s": eintrag.zeitlimit_s,
            "notiz": eintrag.notiz,
        }
    return {"art": "pausenpunkt", "id": str(eintrag.id), "text": eintrag.text}


def speichere_warteschlange(
    eintraege: Sequence[Eintrag],
    pfad: Path,
    *,
    paket_version: str,
    git_hash: str | None,
    ueberschreiben: bool = False,
    jetzt: Callable[[], datetime] = _jetzt_utc,
) -> None:
    """Schreibt die Warteschlange als JSON.

    Parameters
    ----------
    eintraege : sequence of Messung or Pausenpunkt
        Zu speichernde Einträge in Reihenfolge (Zustände werden nicht gespeichert).
    pfad : pathlib.Path
        Zieldatei, muss auf ``.warteschlange.json`` enden.
    paket_version : str
        Version des Pakets (Kopfdaten).
    git_hash : str or None
        Git-Hash des Stands, ``None`` wenn unbekannt.
    ueberschreiben : bool
        Ohne ``True`` wird eine vorhandene Datei nie angetastet. Mit ``True`` wird atomar
        ersetzt (temporäre Datei, dann ``os.replace``).
    jetzt : callable
        Uhr (injizierbar); muss eine zeitzonenbehaftete ``datetime`` liefern.

    Raises
    ------
    ValueError
        Bei falscher Dateiendung oder zeitzonenloser Uhr.
    FileExistsError
        Wenn die Datei existiert und ``ueberschreiben`` nicht gesetzt ist.
    """
    if not pfad.name.endswith(DATEIENDUNG):
        raise ValueError(f"Dateiname muss auf '{DATEIENDUNG}' enden: {pfad.name}")
    zeitpunkt = jetzt()
    if zeitpunkt.tzinfo is None:
        raise ValueError("Uhr muss eine zeitzonenbehaftete datetime liefern")
    daten = {
        "schema_version": SCHEMA_VERSION,
        "art": ART_DATEI,
        "erstellt_utc": zeitpunkt.astimezone(UTC).isoformat(),
        "paket_version": paket_version,
        "git_hash": git_hash,
        "eintraege": [eintrag_zu_dict(e) for e in eintraege],
    }
    text = json.dumps(daten, ensure_ascii=False, indent=2, allow_nan=False) + "\n"
    if not ueberschreiben:
        with open(pfad, "x", encoding="utf-8", newline="\n") as datei:
            datei.write(text)
        return
    temporaer = pfad.with_name(pfad.name + ".tmp")
    try:
        with open(temporaer, "w", encoding="utf-8", newline="\n") as datei:
            datei.write(text)
        os.replace(temporaer, pfad)
    finally:
        temporaer.unlink(missing_ok=True)


class _LadeError(ValueError):
    """Ladefehler mit JSON-Pfad (intern, wird als ValueError mit Dateiname weitergereicht)."""


def _doppelte_schluessel_ablehnen(paare: list[tuple[str, object]]) -> dict[str, object]:
    ergebnis: dict[str, object] = {}
    for schluessel, wert in paare:
        if schluessel in ergebnis:
            raise _LadeError(f"doppelter Schlüssel '{schluessel}'")
        ergebnis[schluessel] = wert
    return ergebnis


def _objekt(
    wert: object, pfad: str, *, erlaubt: set[str], pflicht: set[str] | None = None
) -> dict[str, object]:
    if not isinstance(wert, dict):
        raise _LadeError(f"{pfad}: Objekt erwartet, erhalten {type(wert).__name__}")
    for schluessel in sorted(wert):
        if schluessel not in erlaubt:
            raise _LadeError(f"{pfad}.{schluessel}: unbekannter Schlüssel")
    for schluessel in sorted(pflicht if pflicht is not None else erlaubt):
        if schluessel not in wert:
            raise _LadeError(f"{pfad}.{schluessel}: Pflichtschlüssel fehlt")
    return wert


def _text(wert: object, pfad: str, *, oder_null: bool = False) -> str | None:
    if wert is None and oder_null:
        return None
    if not isinstance(wert, str):
        raise _LadeError(f"{pfad}: Text erwartet, erhalten {type(wert).__name__}")
    return wert


def _pflichttext(wert: object, pfad: str) -> str:
    text = _text(wert, pfad)
    assert text is not None  # für mypy; _text liefert ohne oder_null nie None
    return text


def _uuid(wert: object, pfad: str) -> UUID:
    try:
        return UUID(_pflichttext(wert, pfad))
    except ValueError as exc:
        if isinstance(exc, _LadeError):
            raise
        raise _LadeError(f"{pfad}: keine gültige UUID ({wert!r})") from None


def _eintrag_aus_dict(wert: object, pfad: str) -> Eintrag:
    if not isinstance(wert, dict):
        raise _LadeError(f"{pfad}: Objekt erwartet, erhalten {type(wert).__name__}")
    art = wert.get("art")
    if art == "messung":
        d = _objekt(wert, pfad, erlaubt=_MESSUNG_SCHLUESSEL)
        eid = _uuid(d["id"], f"{pfad}.id")
        parameter = d["parameter"]
        if not isinstance(parameter, dict):
            raise _LadeError(
                f"{pfad}.parameter: Objekt erwartet, erhalten {type(parameter).__name__}"
            )
        for schluessel in parameter:
            if schluessel not in KATALOG:
                raise _LadeError(f"{pfad}.parameter.{schluessel}: unbekannter Parameter")
        zeitlimit = d["zeitlimit_s"]
        if zeitlimit is not None and (
            isinstance(zeitlimit, bool) or not isinstance(zeitlimit, int | float)
        ):
            raise _LadeError(f"{pfad}.zeitlimit_s: Zahl oder null erwartet")
        try:
            return Messung(
                id=eid,
                name=_pflichttext(d["name"], f"{pfad}.name"),
                einstellungsdatei=_pflichttext(d["einstellungsdatei"], f"{pfad}.einstellungsdatei"),
                parameter=parameter,
                zeitlimit_s=zeitlimit,
                notiz=_pflichttext(d["notiz"], f"{pfad}.notiz"),
            )
        except ValueError as exc:
            if isinstance(exc, _LadeError):
                raise
            raise _LadeError(f"{pfad}: {exc}") from None
    if art == "pausenpunkt":
        d = _objekt(wert, pfad, erlaubt=_PAUSENPUNKT_SCHLUESSEL)
        try:
            return Pausenpunkt(
                id=_uuid(d["id"], f"{pfad}.id"), text=_pflichttext(d["text"], f"{pfad}.text")
            )
        except ValueError as exc:
            if isinstance(exc, _LadeError):
                raise
            raise _LadeError(f"{pfad}: {exc}") from None
    raise _LadeError(f"{pfad}.art: 'messung' oder 'pausenpunkt' erwartet, erhalten {art!r}")


def lade_warteschlange(pfad: Path) -> LadeErgebnis:
    """Lädt und prüft eine Warteschlangendatei streng.

    Parameters
    ----------
    pfad : pathlib.Path
        Zu ladende Datei.

    Returns
    -------
    LadeErgebnis
        Einträge (alle ``WARTEND``) und Warnungen.

    Raises
    ------
    FileNotFoundError
        Wenn die Datei nicht existiert.
    ValueError
        Bei ungültigem JSON, falscher ``schema_version`` oder ``art``, unbekannten oder
        fehlenden Schlüsseln, Parametern außerhalb des Katalogs und doppelten IDs. Die
        Meldung beginnt mit dem Dateinamen und nennt den JSON-Pfad (z. B.
        ``$.eintraege[1].parameter.foo``).
    """
    text = pfad.read_text(encoding="utf-8")
    try:
        return _lade_aus_text(text)
    except (_LadeError, json.JSONDecodeError) as exc:
        raise ValueError(f"{pfad.name}: {exc}") from None


def _lade_aus_text(text: str) -> LadeErgebnis:
    daten = json.loads(text, object_pairs_hook=_doppelte_schluessel_ablehnen)
    kopf = _objekt(daten, "$", erlaubt=_KOPF_SCHLUESSEL)
    version = kopf["schema_version"]
    if isinstance(version, bool) or version != SCHEMA_VERSION:
        raise _LadeError(f"$.schema_version: {SCHEMA_VERSION} erwartet, erhalten {version!r}")
    if kopf["art"] != ART_DATEI:
        raise _LadeError(f"$.art: {ART_DATEI!r} erwartet, erhalten {kopf['art']!r}")
    erstellt = _pflichttext(kopf["erstellt_utc"], "$.erstellt_utc")
    try:
        datetime.fromisoformat(erstellt)
    except ValueError:
        raise _LadeError(f"$.erstellt_utc: kein ISO-8601-Zeitstempel ({erstellt!r})") from None
    paket_version = _pflichttext(kopf["paket_version"], "$.paket_version")
    git_hash = _text(kopf["git_hash"], "$.git_hash", oder_null=True)

    roh = kopf["eintraege"]
    if not isinstance(roh, list):
        raise _LadeError(f"$.eintraege: Liste erwartet, erhalten {type(roh).__name__}")
    eintraege: list[Eintrag] = []
    ids: set[UUID] = set()
    warnungen: list[str] = []
    for i, element in enumerate(roh):
        pfad_i = f"$.eintraege[{i}]"
        eintrag = _eintrag_aus_dict(element, pfad_i)
        if eintrag.id in ids:
            raise _LadeError(f"{pfad_i}.id: doppelte ID {eintrag.id}")
        ids.add(eintrag.id)
        if isinstance(eintrag, Messung) and not Path(eintrag.einstellungsdatei).is_file():
            warnungen.append(
                f"{pfad_i}.einstellungsdatei: Datei nicht gefunden: {eintrag.einstellungsdatei}"
            )
        eintraege.append(eintrag)
    return LadeErgebnis(
        eintraege=tuple(eintraege),
        warnungen=tuple(warnungen),
        erstellt_utc=erstellt,
        paket_version=paket_version,
        git_hash=git_hash,
    )
