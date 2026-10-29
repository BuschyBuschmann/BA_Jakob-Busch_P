"""Plausibilitätsprüfungen der Dekodierung einer PSV-Messdatei (Werkzeug, Paket W2).

Die Prüfungen rechnen nichts aus, was nicht schon in der Datei steht: Sie vergleichen die
dekodierten Punktspektren mit Größen, die PSV selbst in derselben Datei abgelegt hat
(Punktmittel ``AvgSeq_Data``, Bandwerte je Punkt ``Band_Data``), und prüfen
Ungleichungen, die für korrekt dekodierte gemittelte Spektren gelten müssen. Weil diese
Vergleiche gegen eine Vertauschung der Punkte unempfindlich sind, belegt
:func:`pruefe_punktzuordnung` die Zuordnung zur Geometrie getrennt. Sie sind
**keine** Auswertealgorithmen für die Arbeit (die folgen nach der Fachgrundlage in W5).

Toleranz: Die Datei speichert ``float32``. Relative Rundungsfehler eines Werts liegen bei
etwa 6e-8; Quotienten, Mittel über 135 Punkte und Summen über 1600 Linien vergrößern sie
auf wenige 1e-7. ``RTOL = 1e-5`` lässt dafür zwei Größenordnungen Reserve und deckt
trotzdem jeden Lese- oder Zuordnungsfehler auf (der läge bei 1e-2 und mehr).
"""

from __future__ import annotations

from dataclasses import dataclass
from itertools import pairwise

import numpy as np
import numpy.typing as npt
from svd_lesen import (
    ComplexArray,
    FloatArray,
    Signal,
    SvdFormatFehler,
    SvdMessung,
    teile_argumente,
)

__all__ = [
    "RTOL",
    "Auswerter",
    "Pruefergebnis",
    "pruefe",
    "pruefe_punktzuordnung",
    "teile_argumente",
]

#: Relative Toleranz der Vergleiche (Begründung im Moduldocstring).
RTOL = 1e-5


@dataclass(frozen=True)
class Pruefergebnis:
    """Ergebnis einer Einzelprüfung.

    Attributes
    ----------
    name : str
        Bezeichnung der Prüfung.
    wert : float
        Größte beobachtete Abweichung bzw. Kennwert.
    grenze : float
        Zulässige Grenze.
    grund : str or None
        Gesetzt, wenn die Prüfung **nicht durchführbar** war (z. B. fehlende Banddaten);
        dann ist ``wert`` NaN und die Prüfung gilt als nicht bestanden.
    """

    name: str
    wert: float
    grenze: float
    grund: str | None = None

    @property
    def durchgefuehrt(self) -> bool:
        """``False``, wenn die Prüfung mangels Daten nicht ausgeführt wurde."""
        return self.grund is None

    @property
    def bestanden(self) -> bool:
        """``True`` nur, wenn durchgeführt und der Kennwert die Grenze einhält."""
        return self.durchgefuehrt and bool(self.wert <= self.grenze)


def _nicht_durchfuehrbar(name: str, grund: str) -> Pruefergebnis:
    return Pruefergebnis(f"nicht durchführbar: {name}", float("nan"), float("nan"), grund)


class Auswerter:
    """Wertet Punktmittel-Formeln mit den dekodierten Punktsignalen aus."""

    def __init__(self, messung: SvdMessung) -> None:
        self._nach_formel: dict[str, Signal] = {s.formel: s for s in messung.signale.values()}

    def signal(self, formel: str) -> FloatArray | ComplexArray:
        """Liefert das Punktsignal mit genau dieser Formel."""
        if formel not in self._nach_formel:
            raise SvdFormatFehler(f"Kein Punktsignal zur Formel {formel!r}")
        return self._nach_formel[formel].werte

    def wert(self, formel: str) -> FloatArray | ComplexArray:
        """Liefert ``(n_punkte, n_linien)`` für eine Teilformel."""
        if formel in self._nach_formel:
            return self.signal(formel)
        op, args = teile_argumente(formel)
        if op == "ABS" and len(args) == 1:
            betrag: FloatArray = np.abs(self.wert(args[0]))
            return betrag
        if op == "FRF" and len(args) == 2:
            return self._frf(args[0], args[1])
        if op == "COH" and len(args) == 2:
            h1 = self.wert(args[0])
            h2 = self.wert(args[1])
            koh: FloatArray = np.abs(h1) / np.abs(h2)
            return koh
        raise SvdFormatFehler(f"Operator nicht unterstützt: {formel!r}")

    def _frf(self, auto: str, kreuz: str) -> ComplexArray:
        """Wertet ``FRF[AP, CP]`` aus.

        H1 = CP/AP_ref, wenn das AP zur Referenz gehört, sonst H2 = AP_antwort/conj(CP).
        Für die Betragsprüfung ist die Konjugation ohne Einfluss.
        """
        op_k, args_k = teile_argumente(kreuz.removeprefix("AVG[")[:-1])
        op_a, args_a = teile_argumente(auto.removeprefix("AVG[")[:-1])
        if op_k != "CP" or op_a != "AP" or len(args_k) != 2:
            raise SvdFormatFehler(f"FRF-Argumente unerwartet: {auto!r}, {kreuz!r}")
        cp = np.asarray(self.signal(kreuz), dtype=np.complex128)
        ap = np.asarray(self.signal(auto), dtype=np.float64)
        if args_a[0] == args_k[1]:
            h1: ComplexArray = cp / ap
            return h1
        if args_a[0] == args_k[0]:
            h2: ComplexArray = ap.astype(np.complex128) / np.conj(cp)
            return h2
        raise SvdFormatFehler(f"AP passt zu keinem CP-Kanal: {auto!r}, {kreuz!r}")


def _rel_abweichung(ist: FloatArray, soll: FloatArray) -> float:
    nenner = np.maximum(np.abs(soll), np.finfo(np.float64).tiny)
    return float(np.max(np.abs(ist - soll) / nenner))


#: Anzahl zufälliger Permutationen für die Geometrie-Gegenprobe der Punktzuordnung.
PERMUTATIONEN = 200
#: Grenze Verhältnis mittlere Schrittweite (Scanreihenfolge) / kleinste mittlere
#: Schrittweite über zufällige Reihenfolgen. Beispieldatei 0,15 (26 mm gegen ≥ 179 mm);
#: 0,5 verlangt mindestens halb so lange Wege wie jede Zufallsreihenfolge.
GEOMETRIE_GRENZE = 0.5


def _mittlerer_schritt(xyz: FloatArray, reihenfolge: npt.NDArray[np.int64]) -> float:
    """Mittlere Schrittweite zwischen in ``reihenfolge`` aufeinanderfolgenden Punkten."""
    return float(np.mean(np.linalg.norm(np.diff(xyz[reihenfolge], axis=0), axis=1)))


def pruefe_punktzuordnung(messung: SvdMessung, seed: int = 0) -> list[Pruefergebnis]:
    """Belegt die Zuordnung Datensatz-Punktindex ↔ MeasPoints-Zeile.

    Punktmittel und Ungleichungen sind gegen eine Permutation der Punkte unempfindlich;
    diese drei Prüfungen nicht vollständig:

    1. **Kennfeld (Anker):** Das Satzfeld +0x8C (``float64``) ist als ``float32``
       bitgleich mit dem Messpunktfeld +0x08 desselben Punkts; die 135 Werte der
       Beispieldatei sind paarweise verschieden. Kennwert: Anzahl Punkte ohne
       Übereinstimmung (Grenze 0). Erkennt jeden Versatz und jede Vertauschung, solange
       die Werte verschieden sind; die Bedeutung des Felds ist offen.
    2. **Geometrie (Gegenprobe):** Mittlere Schrittweite in Scanreihenfolge gegen die
       kleinste über ``PERMUTATIONEN`` zufällige Reihenfolgen (Seed fest). Erkennt grobe
       Fehlzuordnungen, aber weder einzelne Vertauschungen noch sicher einen Versatz um
       einen Index (verläuft der Scan quer zur Indexrichtung, bleibt ein Versatz
       geometrisch fast glatt).
    3. **Zeit:** ``zeit_a`` steigt in Scanreihenfolge streng monoton. Belegt nur die
       Scanreihenfolge der Datensätze, nicht den Bezug zur Geometrie.
    """
    namen = (
        "Punktzuordnung Kennfeld: Satz +0x8C ≠ MeasPoints +0x08 (Punkte)",
        "Punktzuordnung Geometrie: Schritt(Datei)/min Schritt(Permutation)",
        "Punktzuordnung Zeit: nicht steigende Schritte",
    )
    n = len(messung.punkte.index)
    ergebnisse: list[Pruefergebnis] = []
    feld = messung.punkte.statusfelder.get("feld_08")
    if feld is None or messung.satz_kennfeld.shape != (n,):
        ergebnisse.append(_nicht_durchfuehrbar(namen[0], "Kennfelder fehlen"))
    else:
        satz32 = messung.satz_kennfeld.astype(np.float32).astype(np.float64)
        ergebnisse.append(Pruefergebnis(namen[0], float(np.sum(satz32 != feld)), 0.0))
    if len(messung.scan_platz) != n or n < 4:
        grund = "Scanreihenfolge fehlt oder < 4 Punkte"
        return [
            *ergebnisse,
            _nicht_durchfuehrbar(namen[1], grund),
            _nicht_durchfuehrbar(namen[2], grund),
        ]
    reihenfolge = np.argsort(np.asarray(messung.scan_platz, dtype=np.int64))
    xyz = messung.punkte.koordinaten_m
    rng = np.random.default_rng(seed)
    zufall = min(_mittlerer_schritt(xyz, rng.permutation(n)) for _ in range(PERMUTATIONEN))
    datei = _mittlerer_schritt(xyz, reihenfolge)
    ergebnisse.append(
        Pruefergebnis(namen[1], datei / zufall if zufall > 0 else float("inf"), GEOMETRIE_GRENZE)
    )
    zeiten = next(iter(messung.signale.values())).zeit_a if messung.signale else []
    if len(zeiten) != n:
        ergebnisse.append(_nicht_durchfuehrbar(namen[2], "Zeitstempel fehlen"))
    else:
        sortiert = [zeiten[i] for i in reihenfolge]
        fehlschritte = sum(1 for a, b in pairwise(sortiert) if b <= a)
        ergebnisse.append(Pruefergebnis(namen[2], float(fehlschritte), 0.0))
    return ergebnisse


def pruefe(messung: SvdMessung) -> list[Pruefergebnis]:
    """Führt alle Plausibilitätsprüfungen aus.

    Nicht durchführbare Prüfungen (fehlende Banddaten oder Autospektren) erscheinen als
    Eintrag mit ``grund`` und gelten als nicht bestanden.

    Parameters
    ----------
    messung : SvdMessung
        Ergebnis von :func:`svd_lesen.lese_svd`.

    Returns
    -------
    list of Pruefergebnis
        Je Prüfung Kennwert und Grenze.
    """
    ergebnisse: list[Pruefergebnis] = []
    ausw = Auswerter(messung)
    ap_nach_kanal = {s.kanaele[0]: s.werte for s in messung.signale.values() if s.art == "AP"}
    for s in messung.signale.values():
        if s.art in ("AP", "ABS"):
            ergebnisse.append(
                Pruefergebnis(f"{s.name} {s.art} >= 0", float(-np.min(np.real(s.werte))), 0.0)
            )
        fehlende = [k for k in s.kanaele if k not in ap_nach_kanal]
        if s.art == "CP":
            name = f"{s.name} |CP|²/(AP·AP) <= 1"
            if fehlende:
                ergebnisse.append(_nicht_durchfuehrbar(name, f"AP fehlt für {fehlende}"))
            else:
                koh = np.abs(s.werte) ** 2 / (
                    ap_nach_kanal[s.kanaele[0]] * ap_nach_kanal[s.kanaele[1]]
                )
                ergebnisse.append(Pruefergebnis(name, float(np.max(koh)), 1.0 + RTOL))
        if s.art == "CPH":
            name = f"{s.name} |CPH|/sqrt(AP) <= 1"
            if s.kanaele[0] not in ap_nach_kanal:
                ergebnisse.append(_nicht_durchfuehrbar(name, f"AP fehlt für {s.kanaele[0]}"))
            else:
                # |Mittel(X·e^{-iφ_R})| <= sqrt(Mittel |X|²) (Cauchy-Schwarz)
                q = np.abs(s.werte) / np.sqrt(ap_nach_kanal[s.kanaele[0]])
                ergebnisse.append(Pruefergebnis(name, float(np.max(q)), 1.0 + RTOL))
        if s.art == "ABS":
            name = f"{s.name} AP/ABS² >= 1 (Jensen)"
            if s.kanaele[0] not in ap_nach_kanal:
                ergebnisse.append(_nicht_durchfuehrbar(name, f"AP fehlt für {s.kanaele[0]}"))
            else:
                v = ap_nach_kanal[s.kanaele[0]] / np.abs(s.werte) ** 2
                ergebnisse.append(Pruefergebnis(name, float(1.0 - np.min(v)), RTOL))
        band = messung.baender.get(f"S{s.name[1:]}")
        regel = "sqrt(Σ|A|²/2)" if s.art in ("ABS", "CPH") else "Σ|X|/2"
        name = f"{s.name} Band = {regel}"
        if band is None:
            ergebnisse.append(_nicht_durchfuehrbar(name, f"Banddaten S{s.name[1:]} fehlen"))
            continue
        betrag = np.abs(s.werte)
        if s.art in ("ABS", "CPH"):
            soll = np.sqrt(np.sum(betrag**2, axis=1) / 2.0)
        else:
            soll = np.sum(betrag, axis=1) / 2.0
        ergebnisse.append(Pruefergebnis(name, _rel_abweichung(band.werte, soll), RTOL))
    for pm in messung.punktmittel:
        op, args = teile_argumente(pm.formel)
        if op != "AVGSEQ" or len(args) != 1:
            raise SvdFormatFehler(f"Punktmittel-Formel unerwartet: {pm.formel!r}")
        soll_pm = np.mean(np.abs(ausw.wert(args[0])), axis=0)
        ergebnisse.append(
            Pruefergebnis(
                f"AvgSeq {pm.nummer} = Punktmittel", _rel_abweichung(pm.werte, soll_pm), RTOL
            )
        )
    ergebnisse.extend(pruefe_punktzuordnung(messung))
    return ergebnisse
