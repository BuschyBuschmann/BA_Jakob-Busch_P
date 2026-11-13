"""Prüfung des Abgleichstatus vor der Messung (R-003b, Plan P-R003, Stufe 2).

Reine Funktionen ohne Geräteaufruf. Die Steuerung liest den Abgleich
(:class:`~ldv_automation.geraet.schnittstelle.Abgleichsleser`), ruft :func:`pruefe_abgleich`
und handelt nach dem Modus der :class:`AbgleichRegel`.

Modi
----
``aus`` (Voreinstellung)
    Es wird nicht geprüft und nie eingegriffen.
``warnen``
    Auffälligkeit erzeugt eine Warnung, die Messung läuft.
``verweigern``
    Ein nicht bestandener oder nicht prüfbarer Abgleich verhindert den Scan.

Kriterien
---------
* Mindestens ein gelesener 3D-Abgleich; alle gelesenen 3D-Abgleiche haben ``Valid == True``.
* Optionale Grenzen (nur aus der Konfigurationsdatei, **keine Standardwerte**, jede wäre
  erfunden): Ist-Qualität in m, Positionsunsicherheit in m, Winkelunsicherheit in rad. Ein
  Wert gleich der Grenze besteht (``<=``); die Grenze ist eine Vorgabe, keine Messgröße.
* Optional (``pruefe_2d``): mindestens ein 2D-Abgleich, alle ``Valid == True``.
* **Fail-closed:** Was nicht gelesen wurde, aber geprüft werden müsste (Wert fehlt trotz
  gesetzter Grenze, ``Valid`` unbekannt, Abgleich nicht lesbar), gilt als *nicht prüfbar*.
  Es wirkt nur im Modus ``verweigern``.

Die Werte stammen aus COM ``Infos.Alignments`` (Einheiten laut BEM) und sind am Gerät
unbestätigt.
"""

from __future__ import annotations

import math
from collections.abc import Mapping
from dataclasses import dataclass
from enum import Enum

from ldv_automation.geraet.schnittstelle import Abgleich2D, Abgleich3D, AbgleichStand


class AbgleichModus(Enum):
    """Wirkung der Prüfung (siehe Moduldokumentation)."""

    AUS = "aus"
    WARNEN = "warnen"
    VERWEIGERN = "verweigern"


NICHT_AUSGEFUEHRT = "nicht_ausgefuehrt"


class PruefErgebnis(Enum):
    """Ergebnis von :func:`pruefe_abgleich`."""

    NICHT_GEPRUEFT = "nicht_geprueft"
    BESTANDEN = "bestanden"
    NICHT_BESTANDEN = "nicht_bestanden"
    NICHT_PRUEFBAR = "nicht_pruefbar"


@dataclass(frozen=True, kw_only=True)
class AbgleichRegel:
    """Konfiguration der Prüfung (R-003b); Standard: aus, keine Grenzen.

    Parameters
    ----------
    modus : AbgleichModus
        Wirkung der Prüfung.
    qualitaet_max_m : float or None
        Obergrenze der Ist-Qualität (``CurrentQuality``) in m; ``None``: keine Grenze.
    position_max_m : float or None
        Obergrenze der Positionsunsicherheit in m; ``None``: keine Grenze.
    winkel_max_rad : float or None
        Obergrenze der Winkelunsicherheit in rad; ``None``: keine Grenze.
    pruefe_2d : bool
        2D-Abgleich in die Prüfung einbeziehen.

    Raises
    ------
    ValueError
        Wenn eine Grenze nicht endlich oder nicht > 0 ist. Eine Obergrenze nach oben gibt es
        bewusst nicht (jede wäre erfunden).
    """

    modus: AbgleichModus = AbgleichModus.AUS
    qualitaet_max_m: float | None = None
    position_max_m: float | None = None
    winkel_max_rad: float | None = None
    pruefe_2d: bool = False

    def __post_init__(self) -> None:
        for name in ("qualitaet_max_m", "position_max_m", "winkel_max_rad"):
            wert = getattr(self, name)
            if wert is None:
                continue
            if isinstance(wert, bool) or not isinstance(wert, int | float):
                raise ValueError(f"AbgleichRegel: {name} muss eine Zahl sein")
            if not math.isfinite(wert) or wert <= 0:
                raise ValueError(f"AbgleichRegel: {name} muss endlich und > 0 sein")


@dataclass(frozen=True, kw_only=True)
class AbgleichPruefung:
    """Ergebnis einer Prüfung.

    Parameters
    ----------
    ergebnis : PruefErgebnis
        Gesamtergebnis.
    befunde : tuple of str
        Lesbare Befunde (leer bei ``bestanden``/``nicht_geprueft``).
    """

    ergebnis: PruefErgebnis
    befunde: tuple[str, ...] = ()


def _mm(wert_m: float) -> str:
    return f"{wert_m * 1e3:.4g} mm ({wert_m:.6g} m)"


def _winkel(wert_rad: float) -> str:
    return f"{math.degrees(wert_rad):.4g} Grad ({wert_rad * 1e3:.4g} mrad)"


class _Sammler:
    def __init__(self) -> None:
        self.verletzt: list[str] = []
        self.unklar: list[str] = []

    def grenze(self, marke: str, wert: float | None, grenze: float | None, text: object) -> None:
        """Prüft ``wert <= grenze``; ohne Grenze geschieht nichts."""
        if grenze is None:
            return
        fmt = _winkel if "Winkel" in marke else _mm
        if wert is None or not math.isfinite(wert):
            lesbar = "nicht lesbar" if wert is None else f"nicht endlich ({wert!r})"
            self.unklar.append(f"{marke}: Wert {lesbar}, Grenze {fmt(grenze)} gesetzt ({text})")
        elif wert > grenze:
            self.verletzt.append(f"{marke}: {fmt(wert)} über Grenze {fmt(grenze)} ({text})")

    def gueltig(self, marke: str, gueltig: bool | None) -> None:
        if gueltig is False:
            self.verletzt.append(f"{marke}: ungültig (Valid = False)")
        elif gueltig is None:
            self.unklar.append(f"{marke}: Gültigkeit nicht lesbar")


def _pruefe_3d(eintraege: tuple[Abgleich3D, ...], regel: AbgleichRegel, s: _Sammler) -> None:
    for e in eintraege:
        marke = f"3D-Abgleich {e.index}"
        s.gueltig(marke, e.gueltig)
        s.grenze(f"{marke} Qualität", e.qualitaet_ist_m, regel.qualitaet_max_m, "Ist-Qualität")
        s.grenze(
            f"{marke} Positionsunsicherheit",
            e.positionsunsicherheit_m,
            regel.position_max_m,
            "Positionsunsicherheit",
        )
        s.grenze(
            f"{marke} Winkelunsicherheit",
            e.winkelunsicherheit_rad,
            regel.winkel_max_rad,
            "Winkelunsicherheit",
        )


def _pruefe_2d(eintraege: tuple[Abgleich2D, ...], s: _Sammler) -> None:
    for e in eintraege:
        s.gueltig(f"2D-Abgleich {e.index}", e.gueltig)


def _unvollstaendig(art: str, gelesen: int, anzahl: int) -> str:
    return f"{art}-Abgleich: nur {gelesen} von {anzahl} Einträgen gelesen, Rest ungeprüft"


def _fehlt(
    art: str, eintraege: tuple[object, ...], anzahl: int | None, stand: AbgleichStand, s: _Sammler
) -> None:
    """Keine Einträge gelesen: kein Abgleich vorhanden (Count 0) oder nicht lesbar."""
    if eintraege:
        if anzahl is not None and anzahl > len(eintraege):
            s.unklar.append(_unvollstaendig(art, len(eintraege), anzahl))
        return
    if anzahl == 0:
        s.verletzt.append(f"kein {art}-Abgleich vorhanden (Count = 0)")
        return
    gruende = "; ".join(
        f"{k}: {v}" for k, v in stand.nicht_lesbar.items() if art in k or "Infos" in k
    )
    s.unklar.append(f"{art}-Abgleich nicht lesbar" + (f" ({gruende})" if gruende else ""))


def pruefe_abgleich(
    stand: AbgleichStand | None, grund: str | None, regel: AbgleichRegel
) -> AbgleichPruefung:
    """Prüft den gelesenen Abgleich gegen ``regel``.

    Parameters
    ----------
    stand : AbgleichStand or None
        Gelesener Stand; ``None``, wenn nicht gelesen.
    grund : str or None
        Grund, warum nicht gelesen wurde (nur bei ``stand is None``).
    regel : AbgleichRegel
        Modus und Grenzen.

    Returns
    -------
    AbgleichPruefung
        ``nicht_geprueft`` im Modus ``aus``; sonst ``nicht_bestanden``, wenn ein Kriterium
        verletzt ist, ``nicht_pruefbar``, wenn Nötiges fehlt, sonst ``bestanden``.
    """
    if regel.modus is AbgleichModus.AUS:
        return AbgleichPruefung(ergebnis=PruefErgebnis.NICHT_GEPRUEFT)
    if stand is None:
        text = f"Abgleich nicht gelesen: {grund or 'ohne Angabe'}"
        return AbgleichPruefung(ergebnis=PruefErgebnis.NICHT_PRUEFBAR, befunde=(text,))
    s = _Sammler()
    _fehlt("3D", stand.abgleich_3d, stand.anzahl_3d, stand, s)
    _pruefe_3d(stand.abgleich_3d, regel, s)
    if regel.pruefe_2d:
        _fehlt("2D", stand.abgleich_2d, stand.anzahl_2d, stand, s)
        _pruefe_2d(stand.abgleich_2d, s)
    befunde = tuple(s.verletzt + s.unklar)
    if s.verletzt:
        return AbgleichPruefung(ergebnis=PruefErgebnis.NICHT_BESTANDEN, befunde=befunde)
    if s.unklar:
        return AbgleichPruefung(ergebnis=PruefErgebnis.NICHT_PRUEFBAR, befunde=befunde)
    return AbgleichPruefung(ergebnis=PruefErgebnis.BESTANDEN)


def abgleich_hinweise(stand: AbgleichStand | None, grund: str | None) -> tuple[str, ...]:
    """Auffälligkeiten des gelesenen Abgleichs, unabhängig vom Modus (für Ereignis-Hinweise).

    Auffällig sind: nicht gelesen, pauschal nicht lesbar, kein Eintrag, ``Valid`` nicht
    ``True``, nicht lesbare Einzelfelder.
    """
    if stand is None:
        return (f"Abgleich nicht gelesen: {grund or 'ohne Angabe'}",)
    ergebnis = [f"{k}: {v}" for k, v in stand.nicht_lesbar.items()]
    if stand.anzahl_3d == 0:
        ergebnis.append("kein 3D-Abgleich vorhanden (Count = 0)")
    for art, eintraege, anzahl in (
        ("3D", stand.abgleich_3d, stand.anzahl_3d),
        ("2D", stand.abgleich_2d, stand.anzahl_2d),
    ):
        if eintraege and anzahl is not None and anzahl > len(eintraege):
            ergebnis.append(_unvollstaendig(art, len(eintraege), anzahl))
    for e in stand.abgleich_3d:
        if e.gueltig is not True:
            ergebnis.append(f"3D-Abgleich {e.index}: Valid = {e.gueltig}")
        ergebnis.extend(f"3D-Abgleich {e.index} {k}: {v}" for k, v in e.nicht_lesbar.items())
    for e2 in stand.abgleich_2d:
        if e2.gueltig is not True:
            ergebnis.append(f"2D-Abgleich {e2.index}: Valid = {e2.gueltig}")
        ergebnis.extend(f"2D-Abgleich {e2.index} {k}: {v}" for k, v in e2.nicht_lesbar.items())
    return tuple(ergebnis)


def pruefung_zu_dict(regel: AbgleichRegel, pruefung: AbgleichPruefung) -> dict[str, object]:
    """Protokollfeld ``abgleich.pruefung`` (Modus, Ergebnis, Grenzen, Befunde)."""
    grenzen: Mapping[str, object] = {
        "qualitaet_max_m": regel.qualitaet_max_m,
        "position_max_m": regel.position_max_m,
        "winkel_max_rad": regel.winkel_max_rad,
        "pruefe_2d": regel.pruefe_2d,
    }
    return {
        "modus": regel.modus.value,
        "ergebnis": pruefung.ergebnis.value,
        "grenzen": dict(grenzen),
        "befunde": list(pruefung.befunde),
    }


def pruefung_nicht_ausgefuehrt_zu_dict(regel: AbgleichRegel) -> dict[str, object]:
    """Protokollfeld ``abgleich.pruefung`` für den Fall, dass das Gate nicht lief.

    Das Ergebnis ist ``nicht_ausgefuehrt`` (kein :class:`PruefErgebnis`): Die Messung endete
    vor der Prüfung (Vorprüfung, Abweichung, Modus, Abbruch, Hänger). Eine Aussage über den
    Abgleich ist damit nicht verbunden.
    """
    gesamt = pruefung_zu_dict(regel, AbgleichPruefung(ergebnis=PruefErgebnis.NICHT_GEPRUEFT))
    gesamt["ergebnis"] = NICHT_AUSGEFUEHRT
    gesamt["befunde"] = ["Prüfung nicht ausgeführt: Messung endete vor der Abgleichprüfung"]
    return gesamt
