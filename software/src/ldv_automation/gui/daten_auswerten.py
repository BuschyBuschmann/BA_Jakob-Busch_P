"""Daten und Tabellenzeilen der Ansichten 2 bis 4 (P-AUSW T3b), Qt-frei.

Keine neue Mathematik: Zahlen kommen aus den Ergebnisobjekten des Kerns
(:class:`~ldv_automation.auswertung.spitzen.Spitze`,
:class:`~ldv_automation.auswertung.baender.Bandwert`); dieses Modul formatiert sie für die
Tabellen und prüft die Vollständigkeit der Dämpfungsangaben (R-055). Das Modul importiert NumPy
und den Kern, deshalb nur der Reiter „Auswerten“ (nicht das Hauptfenster) darf es laden.
"""

from __future__ import annotations

import math
from collections.abc import Iterable, Sequence
from dataclasses import dataclass

import numpy as np

from ldv_automation.auswertung.baender import Bandwert
from ldv_automation.auswertung.daten import Messdaten, einheit_quadrat
from ldv_automation.auswertung.export import METHODE_SPITZEN
from ldv_automation.auswertung.gesamt import berechne_baender
from ldv_automation.auswertung.mittel import Punktmittel, punktmittel_arithmetisch
from ldv_automation.auswertung.schwingform import waehle_linie
from ldv_automation.auswertung.spitzen import Spitze
from ldv_automation.darstellung.auswahl import PaarCache, kanal_der_komponente
from ldv_automation.darstellung.formate import frequenz_text, zahl_signifikant_text, zahl_text
from ldv_automation.darstellung.spitzen import beschriftung_der_spitze
from ldv_automation.gui.anzeige_auswerten import (
    NICHT_LESBAR,
    TEXT_NAECHSTE_LINIE,
    TEXT_SPITZE_WAEHLEN,
)

__all__ = [
    "BAENDER_SPALTEN",
    "KENNZEICHEN_TEXT",
    "SPITZEN_SPALTEN",
    "FrequenzPruefung",
    "TabellenZeile",
    "baender_zeilen",
    "bandwerte_fuer",
    "frequenz_pruefen",
    "kanalpaar_text",
    "spitze_angaben_text",
    "spitze_der_linie",
    "spitzen_zeilen",
]

SPITZEN_SPALTEN: tuple[str, ...] = (
    "Nr",
    "f_sp [Hz]",
    "ζ",
    "band_u_hz [Hz]",
    "band_o_hz [Hz]",
    "Methode",
    "Kennzeichen",
)
"""Spalten der Spitzentabelle (Brief K-AUSW 3.3)."""
BAENDER_SPALTEN: tuple[str, ...] = ("Nr", "f_u [Hz]", "f_o [Hz]", "RMS", "Bezug")
"""Spalten der Bändertabelle (Brief K-AUSW 3.3)."""

KENNZEICHEN_TEXT = {
    "aufloesungsbegrenzt": "auflösungsbegrenzt",
    "ueberlappend": "überlappend",
    "nachbarmode": "Nachbarmode",
    "kohaerenz_niedrig": "Kohärenz niedrig",
}
"""Anzeigetexte der Warnkennzeichen (wie ``darstellung.spitzen``; ein Test vergleicht beide)."""


@dataclass(frozen=True)
class TabellenZeile:
    """Eine Zeile einer Tabelle.

    Attributes
    ----------
    zellen : tuple of str
        Anzeigetexte je Spalte.
    sortwerte : tuple of float or str
        Sortierwerte je Spalte (Zahlen als ``float``, NaN sortiert ans Ende).
    schluessel : int
        Index des Eintrags in der Quelle (Spitze ``i`` der Spitzenliste, Band ``i``).
    """

    zellen: tuple[str, ...]
    sortwerte: tuple[float | str, ...]
    schluessel: int


def kanalpaar_text(antwort: str, referenz: str) -> str:
    """Eintrag der Kanalpaarwahl „Vib X / Ref1“."""
    return f"{antwort} / {referenz}"


def _zahl(wert: float) -> str:
    return frequenz_text(wert, 3)[: -len(" Hz")]


def spitzen_zeilen(
    spitzen: Sequence[Spitze], *, warn_symbol: str = "⚠"
) -> tuple[tuple[TabellenZeile, ...], tuple[str, ...]]:
    """Zeilen der Spitzentabelle und Fehlermeldungen unvollständiger Spitzen.

    Jede angezeigte Zeile mit ζ trägt Bandgrenzen und Methode (R-055). Eine Spitze ohne
    bestimmte Breite (ζ NaN) bleibt sichtbar, ζ, Bandgrenzen und Methode stehen dann als „–“
    (Annahme N-4). Ist ζ endlich, fehlt aber eine Bandgrenze, wird die Zeile **nicht**
    angezeigt und als Fehler gemeldet.

    Parameters
    ----------
    spitzen : sequence of Spitze
        Spitzen des Kerns (nach Frequenz sortiert).
    warn_symbol : str, optional
        Symbol vor den Warnkennzeichen (Symbol plus Wort).

    Returns
    -------
    tuple
        ``(zeilen, fehler)``; ``fehler`` enthält je ausgelassene Spitze einen Text.
    """
    zeilen: list[TabellenZeile] = []
    fehler: list[str] = []
    for i, s in enumerate(spitzen):
        grenzen_ok = math.isfinite(s.f_l_hz) and math.isfinite(s.f_r_hz)
        zeta_ok = math.isfinite(s.zeta)
        if zeta_ok and not grenzen_ok:
            fehler.append(
                f"Spitze {i + 1} ({frequenz_text(s.f_sp_hz, 3)}): ζ ohne Bandgrenzen, "
                "Zeile nicht angezeigt"
            )
            continue
        bestimmt = zeta_ok and grenzen_ok
        kennzeichen = ", ".join(KENNZEICHEN_TEXT.get(k, k) for k in s.kennzeichen)
        zellen = (
            str(i + 1),
            _zahl(s.f_sp_hz),
            zahl_signifikant_text(s.zeta, 2) if bestimmt else NICHT_LESBAR,
            _zahl(s.f_l_hz) if bestimmt else NICHT_LESBAR,
            _zahl(s.f_r_hz) if bestimmt else NICHT_LESBAR,
            METHODE_SPITZEN if bestimmt else NICHT_LESBAR,
            f"{warn_symbol} {kennzeichen}" if kennzeichen else "",
        )
        nan = math.inf
        sortwerte: tuple[float | str, ...] = (
            float(i + 1),
            float(s.f_sp_hz),
            float(s.zeta) if bestimmt else nan,
            float(s.f_l_hz) if bestimmt else nan,
            float(s.f_r_hz) if bestimmt else nan,
            METHODE_SPITZEN if bestimmt else "￿",
            kennzeichen,
        )
        zeilen.append(TabellenZeile(zellen, sortwerte, i))
    return tuple(zeilen), tuple(fehler)


def mittel_ap_der_kanaele(daten: Messdaten, cache: PaarCache) -> dict[str, Punktmittel]:
    """Arithmetische Punktmittel von AP je Kanal (wie ``werte_aus``) für die Bänder."""
    gueltig = cache.gueltig()
    return {
        kanal: punktmittel_arithmetisch(
            ap,
            gueltig,
            groesse=f"AP {kanal}",
            einheit=einheit_quadrat(daten.einheiten[kanal]),
            annahmen=cache.annahmen,
        )
        for kanal, ap in daten.ap.items()
    }


def bandwerte_fuer(
    daten: Messdaten,
    cache: PaarCache,
    paar: tuple[str, str] | None,
    grenzen: Sequence[tuple[float, float]],
) -> tuple[Bandwert, ...]:
    """Bandwerte des Kerns für das gewählte Kanalpaar (ohne Referenz: für die Vib-Kanäle).

    Parameters
    ----------
    daten : Messdaten
        Eingangsdaten.
    cache : PaarCache
        Paarauswertungen.
    paar : tuple of str or None
        Gewähltes Kanalpaar; ``None`` = Datei ohne Referenz.
    grenzen : sequence of tuple of float
        Bandgrenzen ``(f_u, f_o)`` in Hz.
    """
    if not grenzen:
        return ()
    paare = {paar: cache.paar(*paar)} if paar is not None else {}
    mittel_ap = mittel_ap_der_kanaele(daten, cache)
    return berechne_baender(daten, paare, mittel_ap, grenzen, cache.annahmen)


def baender_zeilen(
    bandwerte: Iterable[Bandwert],
    grenzen: Sequence[tuple[float, float]],
    punkt: int | None,
    labels: Sequence[int] | None = None,
) -> tuple[TabellenZeile, ...]:
    """Zeilen der Bändertabelle: Band-RMS des Mittels, bei gewähltem Punkt zusätzlich seines.

    Es erscheinen die Effektivwerte der Amplitude des kohärenten Spektrums (Betragsmittel bzw.
    Punkt) und die der Autospektren der Vib-Kanäle (Punktmittel bzw. Punkt). Die Auswahl
    folgt den strukturierten Feldern ``art``, ``kanal`` und ``mittel`` des Kerns, nicht der
    Beschriftung. FRF-Bandnormen sind kein Effektivwert und stehen nicht darin.

    Parameters
    ----------
    bandwerte : iterable of Bandwert
        Ergebnis von :func:`bandwerte_fuer`.
    grenzen : sequence of tuple of float
        Bänder in der Reihenfolge ihrer Nummern.
    punkt : int or None
        0-basierter Punkt, dessen Wert zusätzlich erscheint; ``None`` = nur Mittel.
    labels : sequence of int, optional
        In der PSV angezeigte Punktnummern (``Punkte.label``) für die Beschriftung; ohne Angabe
        steht der Index.
    """
    vib = {kanal_der_komponente(c) for c in ("X", "Y", "Z")}
    zeilen: list[TabellenZeile] = []
    for b in bandwerte:
        if b.rms is None or b.art not in ("spektrum_kohaerent", "ap"):
            continue
        if b.art == "ap" and b.kanal not in vib:
            continue
        if not b.mittel and punkt is None:
            continue
        if b.mittel:
            wert = float(np.asarray(b.rms))
            zusatz = "Punktmittel" if b.art == "ap" else "Betragsmittel"
        else:
            assert punkt is not None
            wert = float(np.asarray(b.rms)[punkt])
            zusatz = f"Punkt {int(labels[punkt]) if labels is not None else punkt}"
        bezug = _bezug_text(b.art, b.kanal, zusatz)
        nr = _band_nummer(b, grenzen)
        zeilen.append(
            TabellenZeile(
                (
                    str(nr + 1),
                    _zahl(b.f_u_hz),
                    _zahl(b.f_o_hz),
                    f"{zahl_signifikant_text(wert, 4)} {b.einheit}",
                    bezug,
                ),
                (float(nr + 1), b.f_u_hz, b.f_o_hz, wert, bezug),
                nr,
            )
        )
    return tuple(zeilen)


def _bezug_text(art: str, kanal: str, zusatz: str) -> str:
    """Klartext des Bezugs einer Bandzeile (z. B. „kohärentes Spektrum Vib X/Ref1 (…)“)."""
    if art == "spektrum_kohaerent":
        return f"kohärentes Spektrum {kanal} ({zusatz})"
    if zusatz == "Punktmittel":
        return f"Leistungsmittel {kanal} ({zusatz})"
    return f"Autospektrum {kanal} ({zusatz})"


def _band_nummer(b: Bandwert, grenzen: Sequence[tuple[float, float]]) -> int:
    for i, (f_u, f_o) in enumerate(grenzen):
        if math.isclose(f_u, b.f_u_hz, rel_tol=1e-12) and math.isclose(
            f_o, b.f_o_hz, rel_tol=1e-12
        ):
            return i
    return 0


def spitze_angaben_text(spitze: Spitze | None, *, warn_symbol: str = "⚠") -> str:
    """Angaben der gewählten Spitze als Textblock für die Auswahlspalte (R-055 vollständig).

    Derselbe Text wie im Kasten der Zeichenfunktion (:func:`~ldv_automation.darstellung.spitzen.
    beschriftung_der_spitze`): Frequenz, ζ mit 2 signifikanten Stellen, Methode, Bandgrenzen
    und alle Warnkennzeichen; ohne bestimmte Breite „ζ = –“ ohne Methode. Ohne gewählte Spitze
    steht der Hinweis, wo sie zu wählen ist.

    Parameters
    ----------
    spitze : Spitze or None
        Gewählte Spitze.
    warn_symbol : str, optional
        Symbol vor den Warnkennzeichen.
    """
    if spitze is None:
        return TEXT_SPITZE_WAEHLEN
    return beschriftung_der_spitze(spitze, warn_symbol=warn_symbol)


def spitze_der_linie(spitzen: Sequence[Spitze], linie: int) -> Spitze | None:
    """Spitze, deren Spitzenlinie ``linie`` ist (``None`` = keine; Kennzeichen der Schwingform)."""
    return next((s for s in spitzen if s.k == linie), None)


@dataclass(frozen=True)
class FrequenzPruefung:
    """Ergebnis der Prüfung einer eingegebenen Frequenz (Ansicht 4).

    Attributes
    ----------
    gueltig : bool
        ``True``, wenn die Frequenz auf die Achse der Datei einrastet.
    linie : int or None
        0-basierter Linienindex (nur bei gültiger Frequenz).
    f_linie_hz : float or None
        Frequenz der nächsten Linie.
    naechste_linie : str
        Text „nächste Linie: 123,750 Hz“ (leer bei ungültiger Frequenz).
    fehler : str
        Text „✖ Frequenz 1200 Hz liegt außerhalb 0,625 … 1000 Hz.“ (leer bei gültiger).
    """

    gueltig: bool
    linie: int | None
    f_linie_hz: float | None
    naechste_linie: str
    fehler: str


def frequenz_pruefen(
    f_hz: float, frequenz_hz: np.ndarray, delta_f_hz: float, *, fehler_symbol: str = "✖"
) -> FrequenzPruefung:
    """Prüft ``f_hz`` gegen die Frequenzachse der Datei und rastet auf die nächste Linie ein.

    Zulässig ist von ``f_erste - Δf/2`` bis ``f_letzte + Δf/2`` (wie ``waehle_linie``); die
    Meldung nennt den Bereich ``f_erste … f_letzte`` der Datei, nicht neu aus Bandbreite und
    Linien gebildet (U-4).
    """
    try:
        k = waehle_linie(frequenz_hz, float(f_hz), delta_f_hz)
    except ValueError:
        unten = _zahl_kurz(float(frequenz_hz[0]))
        oben = _zahl_kurz(float(frequenz_hz[-1]))
        wert = _zahl_kurz(float(f_hz)) if math.isfinite(f_hz) else str(f_hz)
        return FrequenzPruefung(
            False,
            None,
            None,
            "",
            f"{fehler_symbol} Frequenz {wert} Hz liegt außerhalb {unten} … {oben} Hz.",
        )
    f_k = float(frequenz_hz[k])
    return FrequenzPruefung(True, k, f_k, TEXT_NAECHSTE_LINIE.format(f=frequenz_text(f_k, 3)), "")


def _zahl_kurz(wert: float) -> str:
    """Zahl mit Dezimalkomma ohne überflüssige Nullen (Meldungen, wie die Parameterzeile)."""
    return zahl_text(round(wert, 3) + 0.0, None)
