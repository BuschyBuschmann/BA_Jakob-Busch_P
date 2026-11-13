"""Konfigurationsdatei des Messrechners (Korrektur K-U5, Nutzerentscheidung).

Die Schalter, die nach der Erkundung am Gerät eingestellt werden, stehen in einer
JSON-Datei, die beim Start mit ``--konfig PFAD`` angegeben wird. Die Datei liegt außerhalb
des Pakets und beeinflusst den Git-Hash nicht. Ohne Datei gelten die Standardwerte
(:data:`STANDARD`).

Format (UTF-8)::

    {
      "art": "ldv-messrechner-konfig",
      "schema_version": 1,
      "validator_rueckfall_direkt": false,
      "lademaske": ["Acquisition", "Alignment", "APS", "2DAlignment", "3DAlignment"],
      "aufruf_grenze_s": 60,
      "aufruf_warnung_s": 5,
      "stop_frist_s": 10,
      "standard_zeitlimit_s": 600,
      "abgleich_pruefung": "aus"
    }

``art`` und ``schema_version`` sind Pflicht, jeder weitere Schlüssel ist optional (sonst
Standardwert). Die Prüfung ist streng: Unbekannte Schlüssel, falsche Typen und Werte
außerhalb der Bereiche (:data:`BEREICHE`) führen zu :class:`KonfigFehler` mit JSON-Pfad.
Prüfung des Abgleichs vor der Messung (R-003b, alle optional): ``abgleich_pruefung``
(``"aus"`` Voreinstellung, ``"warnen"``, ``"verweigern"``), die Grenzen
``abgleich_qualitaet_max_m`` (m), ``abgleich_position_max_m`` (m),
``abgleich_winkel_max_rad`` (rad) und ``abgleich_2d_pruefen`` (true/false). Grenzen haben
**keinen Standardwert und keine Obergrenze** (jede wäre erfunden); sie müssen endlich und
> 0 sein und stehen nur hier, nie in der Oberfläche. Das Schema der Datei bleibt 1.
Die Lademaske wird nur über die Richtlinie des COM-Adapters
(``richtlinie.lademaske_freigegeben``) zugelassen. Die Bereichsgrenzen sind Annahmen
(Schutz vor Tippfehlern), keine Gerätedaten.
"""

from __future__ import annotations

import hashlib
import json
import math
from collections.abc import Mapping
from dataclasses import dataclass, field
from pathlib import Path

from ldv_automation.ablauf.abgleich import AbgleichModus, AbgleichRegel
from ldv_automation.ablauf.steuerung import AblaufKonfiguration
from ldv_automation.geraet.com.konstanten import SettingsMask, lademaske_text
from ldv_automation.geraet.com.richtlinie import STANDARD_LADEMASKE, lademaske_freigegeben

ART = "ldv-messrechner-konfig"
SCHEMA_VERSION = 1

LADEGRUPPEN_NAMEN: Mapping[str, SettingsMask] = {
    "Acquisition": SettingsMask.ACQUISITION,
    "Alignment": SettingsMask.ALIGNMENT,
    "Camera": SettingsMask.CAMERA,
    "Windows": SettingsMask.WINDOWS,
    "APS": SettingsMask.APS,
    "2DAlignment": SettingsMask.ALIGNMENT_2D,
    "3DAlignment": SettingsMask.ALIGNMENT_3D,
}
"""Namen der ``PTCSettings``-Gruppen; ob eine Gruppe erlaubt ist, entscheidet die Richtlinie."""

BEREICHE: Mapping[str, tuple[float, float]] = {
    "aufruf_grenze_s": (1.0, 3600.0),
    "aufruf_warnung_s": (0.5, 3600.0),
    "stop_frist_s": (1.0, 600.0),
    "standard_zeitlimit_s": (1.0, 864_000.0),
}
"""Zulässige Bereiche in s (einschließlich); zusätzlich gilt Warnung ≤ Grenze."""


class KonfigFehler(ValueError):  # noqa: N818  (fachlicher Name)
    """Die Konfigurationsdatei ist nicht lesbar oder ungültig."""


@dataclass(frozen=True, kw_only=True)
class MessrechnerKonfig:
    """Werte der Konfiguration samt Herkunft.

    Parameters
    ----------
    validator_rueckfall_direkt : bool
        Schalter S4 des COM-Adapters.
    lademaske : int
        ``PTCSettings``-Maske für ``Settings.Load``.
    aufruf_grenze_s, aufruf_warnung_s, stop_frist_s, standard_zeitlimit_s : float
        Zeiten in s für Steuerung und Sitzung.
    abgleich : AbgleichRegel
        Prüfung des Abgleichs vor der Messung (Standard: aus, keine Grenzen).
    pfad : str or None
        Absoluter Pfad der Datei; ``None`` bei Standardwerten.
    sha256 : str or None
        SHA-256 des Dateiinhalts; ``None`` bei Standardwerten.
    """

    validator_rueckfall_direkt: bool = False
    lademaske: int = STANDARD_LADEMASKE
    aufruf_grenze_s: float = 60.0
    aufruf_warnung_s: float = 5.0
    stop_frist_s: float = 10.0
    standard_zeitlimit_s: float = 600.0
    abgleich: AbgleichRegel = field(default_factory=AbgleichRegel)
    pfad: str | None = None
    sha256: str | None = None

    def ablauf_konfiguration(self) -> AblaufKonfiguration:
        """Einstellungen der Ablaufsteuerung aus dieser Konfiguration."""
        return AblaufKonfiguration(
            zeitlimit_s=self.standard_zeitlimit_s,
            stop_frist_s=self.stop_frist_s,
            aufruf_grenze_s=self.aufruf_grenze_s,
            abgleich=self.abgleich,
        )

    def protokoll_info(self) -> dict[str, object]:
        """Angaben für Mess- und Ereignisprotokolle sowie den Dialog „Gerät“."""
        return {
            "pfad": self.pfad,
            "sha256": self.sha256,
            "werte": {
                "validator_rueckfall_direkt": self.validator_rueckfall_direkt,
                "lademaske": lademaske_text(self.lademaske),
                "aufruf_grenze_s": self.aufruf_grenze_s,
                "aufruf_warnung_s": self.aufruf_warnung_s,
                "stop_frist_s": self.stop_frist_s,
                "standard_zeitlimit_s": self.standard_zeitlimit_s,
                "abgleich_pruefung": self.abgleich.modus.value,
                "abgleich_qualitaet_max_m": self.abgleich.qualitaet_max_m,
                "abgleich_position_max_m": self.abgleich.position_max_m,
                "abgleich_winkel_max_rad": self.abgleich.winkel_max_rad,
                "abgleich_2d_pruefen": self.abgleich.pruefe_2d,
            },
        }


STANDARD = MessrechnerKonfig()
"""Standardwerte (bisherige Vorgaben aus Plan P2 und K-U2b)."""

ABGLEICH_SCHLUESSEL = (
    "abgleich_pruefung",
    "abgleich_qualitaet_max_m",
    "abgleich_position_max_m",
    "abgleich_winkel_max_rad",
    "abgleich_2d_pruefen",
)
"""Optionale Schlüssel der Abgleichprüfung (R-003b)."""

_ERLAUBT = frozenset(
    {
        "art",
        "schema_version",
        "validator_rueckfall_direkt",
        "lademaske",
        *BEREICHE,
        *ABGLEICH_SCHLUESSEL,
    }
)


def _zahl(daten: Mapping[str, object], schluessel: str, standard: float) -> float:
    if schluessel not in daten:
        return standard
    wert = daten[schluessel]
    if isinstance(wert, bool) or not isinstance(wert, int | float):
        raise KonfigFehler(f"$.{schluessel}: Zahl erwartet, erhalten {wert!r}")
    unten, oben = BEREICHE[schluessel]
    if not math.isfinite(wert) or not unten <= wert <= oben:
        raise KonfigFehler(f"$.{schluessel}: {wert!r} liegt außerhalb {unten:g} … {oben:g} s")
    return float(wert)


def _abgleich_grenze(daten: Mapping[str, object], schluessel: str) -> float | None:
    """Grenze > 0, endlich, ohne Obergrenze; fehlt der Schlüssel oder ist er ``null``: ``None``.

    ``null`` bedeutet keine Grenze (so gibt es ``protokoll_info()`` aus).
    """
    wert = daten.get(schluessel)
    if wert is None:
        return None
    if isinstance(wert, bool) or not isinstance(wert, int | float):
        raise KonfigFehler(f"$.{schluessel}: Zahl erwartet, erhalten {wert!r}")
    try:
        grenze = float(wert)  # sehr große Ganzzahlen: OverflowError
    except OverflowError:
        raise KonfigFehler(f"$.{schluessel}: Zahl zu groß für eine Gleitkommazahl") from None
    if not math.isfinite(grenze) or grenze <= 0:
        raise KonfigFehler(f"$.{schluessel}: {wert!r} muss endlich und > 0 sein")
    return grenze


def _abgleich_regel(daten: Mapping[str, object]) -> AbgleichRegel:
    modus_text = daten.get("abgleich_pruefung", AbgleichModus.AUS.value)
    modi = [m.value for m in AbgleichModus]
    if not isinstance(modus_text, str) or modus_text not in modi:
        raise KonfigFehler(
            f"$.abgleich_pruefung: eine von {', '.join(modi)} erwartet, erhalten {modus_text!r}"
        )
    pruefe_2d = daten.get("abgleich_2d_pruefen", False)
    if not isinstance(pruefe_2d, bool):
        raise KonfigFehler(f"$.abgleich_2d_pruefen: true/false erwartet, erhalten {pruefe_2d!r}")
    return AbgleichRegel(
        modus=AbgleichModus(modus_text),
        qualitaet_max_m=_abgleich_grenze(daten, "abgleich_qualitaet_max_m"),
        position_max_m=_abgleich_grenze(daten, "abgleich_position_max_m"),
        winkel_max_rad=_abgleich_grenze(daten, "abgleich_winkel_max_rad"),
        pruefe_2d=pruefe_2d,
    )


def _lademaske(daten: Mapping[str, object]) -> int:
    if "lademaske" not in daten:
        return STANDARD_LADEMASKE
    namen = daten["lademaske"]
    if not isinstance(namen, list) or not namen or not all(isinstance(n, str) for n in namen):
        raise KonfigFehler("$.lademaske: nicht leere Liste von Gruppennamen erwartet")
    maske = 0
    for i, name in enumerate(namen):
        if name not in LADEGRUPPEN_NAMEN:
            raise KonfigFehler(
                f"$.lademaske[{i}]: unbekannte Gruppe {name!r} "
                f"(bekannt: {', '.join(LADEGRUPPEN_NAMEN)})"
            )
        maske |= int(LADEGRUPPEN_NAMEN[name])
    if not lademaske_freigegeben(maske):
        raise KonfigFehler(
            f"$.lademaske: {lademaske_text(maske)} ist von der Richtlinie nicht freigegeben"
        )
    return maske


def pruefe_konfig(daten: object) -> MessrechnerKonfig:
    """Prüft den Inhalt einer Konfigurationsdatei streng (ohne Herkunft).

    Raises
    ------
    KonfigFehler
        Bei jedem Verstoß, mit JSON-Pfad.
    """
    if not isinstance(daten, dict):
        raise KonfigFehler("$: JSON-Objekt erwartet")
    unbekannt = sorted(set(daten) - _ERLAUBT)
    if unbekannt:
        raise KonfigFehler(f"$: unbekannte Schlüssel {unbekannt}")
    if daten.get("art") != ART:
        raise KonfigFehler(f"$.art: {ART!r} erwartet, erhalten {daten.get('art')!r}")
    version = daten.get("schema_version")
    if isinstance(version, bool) or version != SCHEMA_VERSION:
        raise KonfigFehler(f"$.schema_version: {SCHEMA_VERSION} erwartet, erhalten {version!r}")
    rueckfall = daten.get("validator_rueckfall_direkt", False)
    if not isinstance(rueckfall, bool):
        raise KonfigFehler(f"$.validator_rueckfall_direkt: true/false erwartet, {rueckfall!r}")
    grenze = _zahl(daten, "aufruf_grenze_s", STANDARD.aufruf_grenze_s)
    warnung = _zahl(daten, "aufruf_warnung_s", STANDARD.aufruf_warnung_s)
    if warnung > grenze:
        raise KonfigFehler(
            f"$.aufruf_warnung_s: {warnung:g} s darf nicht größer als aufruf_grenze_s "
            f"({grenze:g} s) sein"
        )
    return MessrechnerKonfig(
        validator_rueckfall_direkt=rueckfall,
        lademaske=_lademaske(daten),
        aufruf_grenze_s=grenze,
        aufruf_warnung_s=warnung,
        stop_frist_s=_zahl(daten, "stop_frist_s", STANDARD.stop_frist_s),
        standard_zeitlimit_s=_zahl(daten, "standard_zeitlimit_s", STANDARD.standard_zeitlimit_s),
        abgleich=_abgleich_regel(daten),
    )


def lade_konfig(pfad: Path) -> MessrechnerKonfig:
    """Liest und prüft eine Konfigurationsdatei; merkt Pfad und SHA-256.

    Raises
    ------
    KonfigFehler
        Wenn die Datei fehlt, nicht lesbar, kein gültiges JSON oder inhaltlich ungültig ist.
    """
    try:
        roh = pfad.read_bytes()
    except OSError as fehler:
        raise KonfigFehler(f"Konfigurationsdatei nicht lesbar: {pfad}: {fehler}") from fehler
    try:
        daten = json.loads(roh.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as fehler:
        raise KonfigFehler(f"Konfigurationsdatei kein gültiges JSON: {pfad}: {fehler}") from None
    try:
        konfig = pruefe_konfig(daten)
    except KonfigFehler as fehler:
        raise KonfigFehler(f"Konfigurationsdatei {pfad}: {fehler}") from None
    return MessrechnerKonfig(
        validator_rueckfall_direkt=konfig.validator_rueckfall_direkt,
        lademaske=konfig.lademaske,
        aufruf_grenze_s=konfig.aufruf_grenze_s,
        aufruf_warnung_s=konfig.aufruf_warnung_s,
        stop_frist_s=konfig.stop_frist_s,
        standard_zeitlimit_s=konfig.standard_zeitlimit_s,
        abgleich=konfig.abgleich,
        pfad=str(pfad.resolve()),
        sha256=hashlib.sha256(roh).hexdigest(),
    )
