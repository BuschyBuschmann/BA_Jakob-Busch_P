"""Plausibilitätsprüfungen beim Einlesen P-01 bis P-11 (FG-02 Abschnitt 4, B-4).

Jede Prüfung liefert ein :class:`Pruefergebnis` mit Status ``ok``, ``warnung``, ``fehler``,
``hinweis`` oder ``nicht_pruefbar``, Zahlenwert und Grund; nichts wird still weggelassen.
Die Schwellen sind die freigegebenen Werte aus :class:`~.annahmen.Schwellen`.

P-07 und P-08 prüfen verschiedene Fehler (W3 2.2): Eine Konjugation dreht den
Phasensinn, ein Vorzeichenwechsel nicht; ein Vorzeichenwechsel dreht das Vorzeichen von
Re{Y}, eine Konjugation nicht.
"""

from __future__ import annotations

import math
from collections.abc import Sequence
from dataclasses import dataclass
from typing import Any, Literal

import numpy as np
import numpy.typing as npt

from .annahmen import Annahmen, Schwellen
from .daten import BoolArray, ComplexArray, FloatArray, Messdaten, zaehle_negative
from .frf import FrfErgebnis
from .spitzen import kandidaten
from .umrechnung import akzeleranz_zu_mobilitaet

Status = Literal["ok", "warnung", "fehler", "hinweis", "nicht_pruefbar"]
Antriebsart = Literal["mobilitaet", "akzeleranz"]


@dataclass(frozen=True, kw_only=True)
class Pruefergebnis:
    """Ergebnis einer Plausibilitätsprüfung.

    Attributes
    ----------
    id : str
        ``"P-01"`` … ``"P-11"``.
    titel : str
        Kurzname der Prüfung.
    status : str
        ``ok``, ``warnung``, ``fehler``, ``hinweis`` oder ``nicht_pruefbar``.
    wert : float or None
        Kennzahl der Prüfung (z. B. größtes Verhältnis, Anteil q oder r).
    grund : str
        Begründung in Worten mit Zahlen.
    bezug : str
        Kanal oder Paar, auf das sich die Prüfung bezieht.
    """

    id: str
    titel: str
    status: Status
    wert: float | None
    grund: str
    bezug: str = ""


def _maximum_verhaeltnis(zaehler: FloatArray, nenner: FloatArray) -> tuple[float, int]:
    """Größtes Verhältnis zaehler/nenner und Anzahl der Linien mit nenner = 0 < zaehler."""
    with np.errstate(divide="ignore", invalid="ignore"):
        verhaeltnis = np.where(nenner > 0, zaehler / np.where(nenner > 0, nenner, 1.0), np.nan)
    unendlich = int(np.count_nonzero((nenner == 0) & (zaehler > 0)))
    maximum = float(np.nanmax(verhaeltnis)) if np.any(~np.isnan(verhaeltnis)) else math.nan
    return maximum, unendlich


def _ungleichung(
    pid: str, titel: str, zaehler: FloatArray, nenner: FloatArray, rtol: float, bezug: str
) -> Pruefergebnis:
    maximum, unendlich = _maximum_verhaeltnis(zaehler, nenner)
    if unendlich:
        return Pruefergebnis(
            id=pid,
            titel=titel,
            status="fehler",
            wert=math.inf,
            grund=f"{unendlich} Linien mit Nenner 0 und Zähler > 0",
            bezug=bezug,
        )
    if math.isnan(maximum):
        return Pruefergebnis(
            id=pid,
            titel=titel,
            status="nicht_pruefbar",
            wert=None,
            grund="keine Werte",
            bezug=bezug,
        )
    ok = maximum <= 1.0 + rtol
    return Pruefergebnis(
        id=pid,
        titel=titel,
        status="ok" if ok else "fehler",
        wert=maximum,
        grund=f"größtes Verhältnis {maximum:.9g} (Grenze 1 + {rtol:g})",
        bezug=bezug,
    )


def p01_kreuzspektrum(
    cp: ComplexArray, ap_a: FloatArray, ap_b: FloatArray, schwellen: Schwellen, bezug: str = ""
) -> Pruefergebnis:
    r"""P-01: :math:`|\mathrm{CP}_{ab}|^2 \le \mathrm{AP}_a\mathrm{AP}_b(1+10^{-5})` (Rohdaten)."""
    return _ungleichung(
        "P-01",
        "Kreuzspektrum-Ungleichung",
        np.abs(cp) ** 2,
        ap_a * ap_b,
        schwellen.ungleichung_rtol,
        bezug,
    )


def p02_cph(
    cph: ComplexArray, ap_a: FloatArray, schwellen: Schwellen, bezug: str = ""
) -> Pruefergebnis:
    r"""P-02: :math:`|\mathrm{CPH}|^2 \le \mathrm{AP}_a(1+10^{-5})` (Rohdaten)."""
    return _ungleichung(
        "P-02", "CPH-Ungleichung", np.abs(cph) ** 2, ap_a, schwellen.ungleichung_rtol, bezug
    )


def p03_vorzeichen(felder: dict[str, FloatArray]) -> Pruefergebnis:
    """P-03: AP >= 0 und ABS >= 0 (NaN ausgenommen)."""
    negative = {name: zaehle_negative(f) for name, f in felder.items()}
    summe = sum(negative.values())
    if summe:
        betroffen = ", ".join(f"{k}: {v}" for k, v in negative.items() if v)
        return Pruefergebnis(
            id="P-03",
            titel="Vorzeichen",
            status="fehler",
            wert=float(summe),
            grund=f"negative Werte ({betroffen})",
        )
    return Pruefergebnis(
        id="P-03",
        titel="Vorzeichen",
        status="ok",
        wert=0.0,
        grund=f"keine negativen Werte in {len(felder)} Feldern",
    )


def p04_jensen(
    abs_a: FloatArray, ap_a: FloatArray, schwellen: Schwellen, bezug: str = ""
) -> Pruefergebnis:
    r"""P-04: :math:`\mathrm{ABS}^2 \le \mathrm{AP}(1+10^{-5})`."""
    return _ungleichung("P-04", "Jensen", abs_a**2, ap_a, schwellen.ungleichung_rtol, bezug)


def p05_kohaerenz(frf: FrfErgebnis, schwellen: Schwellen) -> Pruefergebnis:
    r"""P-05: :math:`\gamma^2 \le 1 + 10^{-5}`; Werte darüber sind ein Fehler.

    Werte in :math:`(1, 1+10^{-5}]` hat :func:`~.frf.berechne_frf` auf 1 gesetzt und gezählt.
    """
    bezug = f"{frf.antwort}/{frf.referenz}"
    maximum = frf.kohaerenz_maximum_roh
    grenze = 1.0 + schwellen.ungleichung_rtol
    if math.isnan(maximum):
        return Pruefergebnis(
            id="P-05",
            titel="Kohärenzbereich",
            status="nicht_pruefbar",
            wert=None,
            grund="keine Kohärenzwerte",
            bezug=bezug,
        )
    status: Status = "fehler" if maximum > grenze else "ok"
    return Pruefergebnis(
        id="P-05",
        titel="Kohärenzbereich",
        status=status,
        wert=maximum,
        grund=(
            f"größtes γ² {maximum:.9g} (Grenze {grenze:.6g}); "
            f"{frf.anzahl_kohaerenz_begrenzt} Werte in (1, {grenze:.6g}] auf 1 gesetzt"
        ),
        bezug=bezug,
    )


def p06_frequenzachse(
    frequenz_hz: FloatArray, delta_f_hz: float, k0: int, schwellen: Schwellen
) -> Pruefergebnis:
    r"""P-06: :math:`|f_k - (k+k_0)\Delta f| \le 10^{-6}\Delta f` (Annahme M2)."""
    soll = (np.arange(frequenz_hz.size) + k0) * delta_f_hz
    abweichung = float(np.max(np.abs(frequenz_hz - soll)) / delta_f_hz)
    ok = abweichung <= schwellen.achse_rtol
    return Pruefergebnis(
        id="P-06",
        titel="Frequenzachse",
        status="ok" if ok else "fehler",
        wert=abweichung,
        grund=(
            f"größte Abweichung {abweichung:.3g}·Δf von (k + {k0})·Δf, Δf = {delta_f_hz:g} Hz "
            f"(Grenze {schwellen.achse_rtol:g}·Δf)"
        ),
    )


def _zeilen(werte: npt.NDArray[np.generic]) -> npt.NDArray[Any]:
    return werte[None, :] if werte.ndim == 1 else werte


def phasensinn_anteil(
    frequenz_hz: FloatArray,
    frf: ComplexArray,
    kohaerenz: FloatArray | None,
    schwellen: Schwellen,
    gueltig: BoolArray | None = None,
) -> tuple[float, int]:
    r"""Anteil q fallender Phase an Spitzen von |H| und Anzahl der Spitzen (P-07).

    Spitzen nach FG-02 3.9 Schritt 1 (Prominenz mit ``schwellen.prominenz_min``) je
    gültigem Punkt mit :math:`\gamma^2 \ge` ``p07_kohaerenz_min`` an der Spitzenlinie;
    Steigung als zentrale Differenz der entfalteten Phase
    :math:`\arg H_{k+1} - \arg H_{k-1}`. Die Spitzen aller Punkte werden zusammengezählt.
    """
    h = _zeilen(frf)
    g2 = None if kohaerenz is None else _zeilen(kohaerenz)
    zeilen = range(h.shape[0]) if gueltig is None else np.flatnonzero(gueltig)
    fallend = 0
    anzahl = 0
    for p in zeilen:
        betrag = np.abs(h[p]).astype(np.float64)
        for k in kandidaten(
            betrag,
            frequenz_hz,
            prominenz_min=schwellen.prominenz_min,
            fenster_linien=schwellen.fenster_linien,
            f_min_hz=schwellen.f_min_hz,
        ):
            if g2 is not None and not g2[p, k] >= schwellen.p07_kohaerenz_min:
                continue
            phase = np.unwrap(np.angle(h[p, k - 1 : k + 2]))
            anzahl += 1
            if phase[2] - phase[0] < 0:
                fallend += 1
    return (fallend / anzahl if anzahl else math.nan), anzahl


def p07_phasensinn(
    frequenz_hz: FloatArray,
    frf: ComplexArray,
    kohaerenz: FloatArray | None,
    schwellen: Schwellen,
    gueltig: BoolArray | None = None,
    bezug: str = "",
) -> Pruefergebnis:
    r"""P-07: Phasensinn an Resonanzen (A-1).

    :math:`q \ge 0{,}9` ok; :math:`q \le 0{,}1` fehler „Daten vermutlich konjugiert“;
    dazwischen warnung; weniger als ``p07_min_spitzen`` Spitzen: nicht prüfbar (der
    Rechenwert q steht trotzdem in ``wert``).
    """
    q, anzahl = phasensinn_anteil(frequenz_hz, frf, kohaerenz, schwellen, gueltig)
    wert = None if math.isnan(q) else q
    if anzahl < schwellen.p07_min_spitzen:
        return Pruefergebnis(
            id="P-07",
            titel="Phasensinn",
            status="nicht_pruefbar",
            wert=wert,
            grund=f"nur {anzahl} Spitzen (mindestens {schwellen.p07_min_spitzen})",
            bezug=bezug,
        )
    if q >= schwellen.p07_ok:
        status: Status = "ok"
        grund = f"Phase fällt an {q:.3f} der {anzahl} Spitzen"
    elif q <= schwellen.p07_fehler:
        status = "fehler"
        grund = f"Daten vermutlich konjugiert: Phase fällt nur an {q:.3f} der {anzahl} Spitzen"
    else:
        status = "warnung"
        grund = f"Phasensinn uneinheitlich: Phase fällt an {q:.3f} der {anzahl} Spitzen"
    return Pruefergebnis(
        id="P-07", titel="Phasensinn", status=status, wert=q, grund=grund, bezug=bezug
    )


def p08_passivitaet(
    frequenz_hz: FloatArray,
    frf: ComplexArray,
    kohaerenz: FloatArray | None,
    art: Antriebsart,
    schwellen: Schwellen,
    gueltig: BoolArray | None = None,
    bezug: str = "",
) -> Pruefergebnis:
    r"""P-08: Passivität am Antriebspunkt (nur für ein konfiguriertes Antriebspunkt-Paar).

    Anteil r der Linien mit :math:`\mathrm{Re}\{Y\} \ge 0` unter
    :math:`\gamma^2 \ge 0{,}9`, Y = Mobilität (aus Akzeleranz :math:`Y = H/(i\omega)`).
    Gezählt werden alle gültigen Punkte und Linien. :math:`r \ge 0{,}95` ok;
    :math:`r \le 0{,}05` warnung „Vorzeichen einer Referenz vermutlich gedreht“;
    dazwischen warnung „kein Antriebspunkt?“.
    """
    h = _zeilen(frf)
    if gueltig is not None:
        h = h[gueltig]
    y = akzeleranz_zu_mobilitaet(h, frequenz_hz) if art == "akzeleranz" else h
    auswahl = np.isfinite(y)
    if kohaerenz is not None:
        g2 = _zeilen(kohaerenz)
        if gueltig is not None:
            g2 = g2[gueltig]
        with np.errstate(invalid="ignore"):
            auswahl &= g2 >= schwellen.p08_kohaerenz_min
    anzahl = int(np.count_nonzero(auswahl))
    if anzahl == 0:
        return Pruefergebnis(
            id="P-08",
            titel="Passivität am Antriebspunkt",
            status="nicht_pruefbar",
            wert=None,
            grund="keine Linie mit ausreichender Kohärenz",
            bezug=bezug,
        )
    r = float(np.count_nonzero(np.real(y[auswahl]) >= 0) / anzahl)
    if r >= schwellen.p08_ok:
        status: Status = "ok"
        grund = f"Re{{Y}} >= 0 an {r:.3f} von {anzahl} Linien"
    elif r <= schwellen.p08_warnung:
        status = "warnung"
        grund = (
            "Vorzeichen einer Referenz vermutlich gedreht: "
            f"Re{{Y}} >= 0 an {r:.3f} von {anzahl} Linien"
        )
    else:
        status = "warnung"
        grund = f"kein Antriebspunkt? Re{{Y}} >= 0 an {r:.3f} von {anzahl} Linien"
    return Pruefergebnis(
        id="P-08",
        titel="Passivität am Antriebspunkt",
        status=status,
        wert=r,
        grund=grund,
        bezug=bezug,
    )


def p09_referenzstabilitaet(
    ap_referenz: FloatArray,
    kohaerenz: FloatArray,
    schwellen: Schwellen,
    gueltig: BoolArray | None = None,
    bezug: str = "",
) -> Pruefergebnis:
    r"""P-09: Referenzstabilität über den Scan.

    Kriterium: Median über Linien mit :math:`\bar\gamma^2 \ge 0{,}9` des
    Variationskoeffizienten von :math:`\sqrt{\mathrm{AP}_b}` über die gültigen Punkte <= 0,05.

    :math:`\bar\gamma^2` ist das arithmetische Punktmittel der Kohärenz des Paars; der
    Variationskoeffizient ist Standardabweichung (Populationsform, ``ddof = 0``) durch
    Mittelwert.
    """
    wurzel = np.sqrt(ap_referenz)
    g2 = kohaerenz
    if gueltig is not None:
        wurzel = wurzel[gueltig]
        g2 = g2[gueltig]
    if wurzel.shape[0] < 2:
        return Pruefergebnis(
            id="P-09",
            titel="Referenzstabilität",
            status="nicht_pruefbar",
            wert=None,
            grund="weniger als zwei gültige Punkte",
            bezug=bezug,
        )
    with np.errstate(invalid="ignore", divide="ignore"):
        mittel_g2 = np.mean(g2, axis=0)
        variation = np.std(wurzel, axis=0) / np.mean(wurzel, axis=0)
        auswahl = (mittel_g2 >= schwellen.p09_kohaerenz_min) & np.isfinite(variation)
    if not np.any(auswahl):
        return Pruefergebnis(
            id="P-09",
            titel="Referenzstabilität",
            status="nicht_pruefbar",
            wert=None,
            grund="keine Linie mit ausreichender Kohärenz",
            bezug=bezug,
        )
    median = float(np.median(variation[auswahl]))
    ok = median <= schwellen.p09_max_variation
    return Pruefergebnis(
        id="P-09",
        titel="Referenzstabilität",
        status="ok" if ok else "warnung",
        wert=median,
        grund=(
            f"Median des Variationskoeffizienten {median:.4f} über {int(np.sum(auswahl))} Linien "
            f"(Grenze {schwellen.p09_max_variation:g})"
        ),
        bezug=bezug,
    )


def p10_punktstatus(annahmen: Annahmen, anzahl_punkte: int) -> Pruefergebnis:
    """P-10: Anzahl ungültiger Punkte (Hinweis; Annahme M6)."""
    gueltig = annahmen.gueltig_je_punkt(anzahl_punkte)
    ungueltig = int(np.count_nonzero(~gueltig))
    status_m6 = annahmen.status_von("M6")
    if ungueltig:
        grund = f"{ungueltig} von {anzahl_punkte} Punkten ungültig (M6: {status_m6})"
        status: Status = "hinweis"
    else:
        grund = f"alle {anzahl_punkte} Punkte gültig (M6: {status_m6})"
        status = "hinweis" if status_m6 == "Annahme" else "ok"
    return Pruefergebnis(
        id="P-10", titel="Punktstatus", status=status, wert=float(ungueltig), grund=grund
    )


def p11_annahmen(annahmen: Annahmen) -> Pruefergebnis:
    """P-11: Liste aller Parameter mit Status „Annahme“ (Hinweis, immer ausgegeben)."""
    offen = [e for e in annahmen.eintraege() if e.ist_annahme]
    text = "; ".join(f"{e.nr} {e.parameter} = {e.wert}" for e in offen) or "keine"
    return Pruefergebnis(
        id="P-11",
        titel="Annahmen",
        status="hinweis",
        wert=float(len(offen)),
        grund=f"Annahmen: {text}",
    )


#: Titel je Prüfnummer (FG-02 Abschnitt 4).
TITEL: dict[str, str] = {
    "P-01": "Kreuzspektrum-Ungleichung",
    "P-02": "CPH-Ungleichung",
    "P-03": "Vorzeichen",
    "P-04": "Jensen",
    "P-05": "Kohärenzbereich",
    "P-06": "Frequenzachse",
    "P-07": "Phasensinn",
    "P-08": "Passivität am Antriebspunkt",
    "P-09": "Referenzstabilität",
    "P-10": "Punktstatus",
    "P-11": "Annahmen",
}


def nicht_pruefbar(pid: str, grund: str, bezug: str = "") -> Pruefergebnis:
    """Ergebnis „nicht prüfbar“ mit Grund (keine Prüfung fällt still weg)."""
    return Pruefergebnis(
        id=pid, titel=TITEL[pid], status="nicht_pruefbar", wert=None, grund=grund, bezug=bezug
    )


def pruefe_eingang(
    daten: Messdaten, schwellen: Schwellen, annahmen: Annahmen
) -> list[Pruefergebnis]:
    """P-01 bis P-04 und P-06 an den Rohdaten (ohne Vorzeichen und Konjugation).

    Fehlt eine Eingangsgröße, erscheint die Prüfung als ``nicht_pruefbar`` mit Grund, je
    betroffenem Paar bzw. Kanal.
    """
    ergebnisse: list[Pruefergebnis] = []
    for (a, b), cp in daten.cp.items():
        ergebnisse.append(p01_kreuzspektrum(cp, daten.ap[a], daten.ap[b], schwellen, f"{a}/{b}"))
    if not daten.cp:
        ergebnisse.append(nicht_pruefbar("P-01", "keine Kreuzspektren (keine Referenz)"))
    paare = list(dict.fromkeys([*daten.cp, *daten.cph]))
    for a, b in paare:
        name = f"{a}/{b}"
        if (a, b) not in daten.cph:
            ergebnisse.append(nicht_pruefbar("P-02", f"kein CPH für {name}", name))
        elif a not in daten.ap:
            ergebnisse.append(nicht_pruefbar("P-02", f"kein AP für {a}", name))
        else:
            ergebnisse.append(p02_cph(daten.cph[(a, b)], daten.ap[a], schwellen, name))
    if not paare:
        ergebnisse.append(nicht_pruefbar("P-02", "keine Kreuzspektren und kein CPH"))
    felder = {f"AP {k}": v for k, v in daten.ap.items()}
    felder.update({f"ABS {k}": v for k, v in daten.betrag.items()})
    ergebnisse.append(p03_vorzeichen(felder))
    kanaele = list(dict.fromkeys([*daten.ap, *daten.betrag]))
    for kanal in kanaele:
        if kanal not in daten.betrag:
            ergebnisse.append(nicht_pruefbar("P-04", f"kein ABS für {kanal}", kanal))
        elif kanal not in daten.ap:
            ergebnisse.append(nicht_pruefbar("P-04", f"kein AP für {kanal}", kanal))
        else:
            ergebnisse.append(p04_jensen(daten.betrag[kanal], daten.ap[kanal], schwellen, kanal))
    if not kanaele:
        ergebnisse.append(nicht_pruefbar("P-04", "weder AP noch ABS vorhanden"))
    ergebnisse.append(
        p06_frequenzachse(daten.frequenz_hz, daten.delta_f_hz, annahmen.k0, schwellen)
    )
    return ergebnisse


def sortiere(ergebnisse: Sequence[Pruefergebnis]) -> tuple[Pruefergebnis, ...]:
    """Sortiert nach Prüfnummer, innerhalb gleicher Nummer stabil."""
    return tuple(sorted(ergebnisse, key=lambda e: e.id))
