"""Messskript für den Messrechner: Zeiten beim Laden und Auswerten einer ``.svd``-Datei.

Die Planung der Auswertungsoberfläche (P-AUSW, U-2/U-7) stützt sich auf Zeiten, die auf einem
Linux-Container gemessen wurden (Lesen 0,1 bis 0,8 s, Paarrechnung etwa 250 ms, Spawn etwa
80 ms). Dieses Skript wiederholt die Messungen am Messrechner (Windows), damit die Annahmen
(UI-15: Oberfläche bleibt bedienbar, Reaktion unter 200 ms) dort belegt oder widerlegt werden.

Gemessen werden (je ``--wiederholungen`` Läufe, ausgegeben als Minimum / Median / Maximum):

``lesen``
    Leser :func:`~ldv_automation.auswertung.svd_lesen.lese_svd` im Hauptprozess.
``sha256``
    SHA-256 der Datei.
``lade_svd``
    Leser, SHA-256 und Adapter (:func:`~ldv_automation.auswertung.laden.lade_svd`).
``spawn_leer``
    Leer-Auftrag im neuen Prozess (Spawn und Import der Auftragsmodule).
``lese_job``
    Gesamtdauer des Auftrags ``lese_job`` im Prozess bis zum Ergebnis, dazu die **längste
    Einzelabfrage** ``fertig()`` im Hauptprozess (so lange blockiert die Oberfläche höchstens
    je Abfrage) und die Dauer von ``ergebnis()``.
``abbrechen``
    ``abbrechen()`` (terminate) kurz nach dem Start von ``lese_job``.
``paar_kalt`` / ``paar_warm``
    Erste und zweite Auswertung eines Kanalpaars (``bereite_paar``, ``berechne_frf``,
    ``werte_paar_aus``) im Hauptprozess.
``schwingform``
    ``schwingform_aus`` in der Mitte der Frequenzachse, erster und zweiter Aufruf.
``pruef_job``
    Plausibilitätsprüfung im Prozess (8 bis 13 s auf dem Container); mit ``--ohne-pruefung``
    ausgelassen.
``import_matplotlib``
    Import von matplotlib in einem frischen Prozess (erster Lauf baut den Schrift-Cache).

Aufruf (aus ``software/``; am Messrechner mit dem Python der Installation)::

    python tools/auswertung/zeiten_messen.py <datei.svd> [--wiederholungen 3]
        [--json ergebnis.json] [--ohne-pruefung] [--ohne-matplotlib]

Das Skript liest die Messdatei nur und schreibt nichts außer der angegebenen JSON-Datei.
Die Zahlen gehören in die Prüfprotokolle (nicht als bestanden zu werten, sondern zu lesen).
"""

from __future__ import annotations

import argparse
import json
import os
import platform
import statistics
import subprocess
import sys
import time
from collections.abc import Callable, Sequence
from pathlib import Path
from typing import Any

import numpy as np

from ldv_automation.auswertung.annahmen import Annahmen, Schwellen
from ldv_automation.auswertung.daten import Messdaten, bereite_paar
from ldv_automation.auswertung.export import sha256_datei
from ldv_automation.auswertung.frf import berechne_frf
from ldv_automation.auswertung.gesamt import schwingform_aus, werte_paar_aus
from ldv_automation.auswertung.jobs import lese_job, pruef_job
from ldv_automation.auswertung.laden import lade_svd
from ldv_automation.auswertung.svd_lesen import lese_svd
from ldv_automation.hintergrund import (
    Auftrag,
    Ausfuehrer,
    ProzessAusfuehrer,
    importiere,
)

TAKT_S = 0.01
"""Abfrageabstand der Warteschleife (die Oberfläche fragt mit 50 ms; kleiner = strenger)."""

ZEIT_GRENZE_S = 600.0
"""Abbruch einer Warteschleife nach dieser Zeit (nie unbegrenzt warten)."""

Uhr = Callable[[], float]


def statistik(werte: Sequence[float]) -> dict[str, float]:
    """Minimum, Median und Maximum einer nicht leeren Messreihe in s.

    Raises
    ------
    ValueError
        Bei leerer Reihe.
    """
    if not werte:
        raise ValueError("leere Messreihe")
    return {
        "min_s": float(min(werte)),
        "median_s": float(statistics.median(werte)),
        "max_s": float(max(werte)),
        "n": float(len(werte)),
    }


def _wiederhole(n: int, funktion: Callable[[], Any], uhr: Uhr) -> list[float]:
    dauern: list[float] = []
    for _ in range(n):
        beginn = uhr()
        funktion()
        dauern.append(uhr() - beginn)
    return dauern


def warte_auf(
    auftrag: Auftrag, uhr: Uhr, schlafe: Callable[[float], None] = time.sleep
) -> tuple[Any, dict[str, float]]:
    """Wartet wie die Oberfläche (Abfrage im Takt) und misst, wie lange jede Abfrage blockiert.

    Returns
    -------
    tuple
        ``(ergebnis, messwerte)`` mit ``gesamt_s``, ``max_abfrage_s`` (längste Einzelabfrage
        ``fertig()``), ``abfragen`` und ``ergebnis_s`` (Dauer von ``ergebnis()``).

    Raises
    ------
    TimeoutError
        Wenn der Auftrag nach :data:`ZEIT_GRENZE_S` nicht fertig ist.
    """
    beginn = uhr()
    laengste = 0.0
    abfragen = 0
    while True:
        t0 = uhr()
        fertig = auftrag.fertig()
        laengste = max(laengste, uhr() - t0)
        abfragen += 1
        if fertig:
            break
        if uhr() - beginn > ZEIT_GRENZE_S:
            auftrag.abbrechen()
            raise TimeoutError(f"Auftrag nach {ZEIT_GRENZE_S:g} s nicht fertig")
        schlafe(TAKT_S)
    t1 = uhr()
    ergebnis = auftrag.ergebnis()
    return ergebnis, {
        "gesamt_s": t1 - beginn,
        "max_abfrage_s": laengste,
        "abfragen": float(abfragen),
        "ergebnis_s": uhr() - t1,
    }


def _paar_zeit(daten: Messdaten, uhr: Uhr) -> tuple[float, float, str]:
    """Erste und zweite Auswertung des ersten Kanalpaars; Name des Paars."""
    paar = next(iter(daten.cp), None)
    if paar is None:
        raise ValueError("Datei ohne Kreuzspektrum: keine Paarrechnung messbar")
    annahmen, schwellen = Annahmen(), Schwellen()

    def einmal() -> None:
        p = bereite_paar(daten, paar[0], paar[1], annahmen)
        berechne_frf(p)
        werte_paar_aus(p, schwellen, annahmen)

    kalt = _wiederhole(1, einmal, uhr)[0]
    warm = _wiederhole(1, einmal, uhr)[0]
    return kalt, warm, f"{paar[0]}/{paar[1]}"


def _matplotlib_import_s() -> float:
    """Dauer des Imports von matplotlib in einem frischen Prozess (erster Lauf: Schriftcache)."""
    code = (
        "import time; t = time.perf_counter(); "
        "import matplotlib.figure, matplotlib.backends.backend_agg; "
        "print(time.perf_counter() - t)"
    )
    lauf = subprocess.run([sys.executable, "-c", code], check=True, capture_output=True, text=True)
    return float(lauf.stdout.strip().splitlines()[-1])


def messe(
    pfad: Path,
    *,
    wiederholungen: int = 3,
    ausfuehrer_fabrik: Callable[[], Ausfuehrer] = ProzessAusfuehrer,
    mit_pruefung: bool = True,
    mit_matplotlib: bool = True,
    uhr: Uhr = time.perf_counter,
    schlafe: Callable[[float], None] = time.sleep,
) -> dict[str, Any]:
    """Führt alle Messungen aus (siehe Moduldocstring).

    Parameters
    ----------
    pfad : pathlib.Path
        ``.svd``-Datei (wird nur gelesen).
    wiederholungen : int
        Läufe je Messung (mindestens 1).
    ausfuehrer_fabrik : callable
        Erzeugt den Ausführer (Voreinstellung ``ProzessAusfuehrer``; Tests: ``DirektAusfuehrer``).
    mit_pruefung : bool
        ``pruef_job`` mitmessen (8 bis 13 s).
    mit_matplotlib : bool
        Import von matplotlib in einem frischen Prozess mitmessen.
    uhr, schlafe : callable
        Zeitquelle und Schlaffunktion (für Tests ersetzbar).

    Returns
    -------
    dict
        ``umgebung`` (System, Python, Pakete), ``datei`` (Pfad, Größe) und ``messungen``
        (je Messung ``statistik``-Werte, ``lese_job`` und ``abbrechen`` mit Zusatzwerten).

    Raises
    ------
    ValueError
        Bei ``wiederholungen < 1`` oder Datei ohne Kreuzspektrum.
    """
    if wiederholungen < 1:
        raise ValueError(f"wiederholungen muss >= 1 sein: {wiederholungen}")
    n = wiederholungen
    ausfuehrer = ausfuehrer_fabrik()
    messungen: dict[str, Any] = {}
    try:
        messungen["lesen"] = statistik(_wiederhole(n, lambda: lese_svd(pfad), uhr))
        messungen["sha256"] = statistik(_wiederhole(n, lambda: sha256_datei(pfad), uhr))
        messungen["lade_svd"] = statistik(_wiederhole(n, lambda: lade_svd(pfad), uhr))
        leer = []
        for _ in range(n):
            beginn = uhr()
            warte_auf(
                ausfuehrer.starte(importiere, ("ldv_automation.auswertung.jobs",)), uhr, schlafe
            )
            leer.append(uhr() - beginn)
        messungen["spawn_leer"] = statistik(leer)
        laeufe = []
        for _ in range(n):
            beginn = uhr()
            geladen, mess = warte_auf(ausfuehrer.starte(lese_job, str(pfad)), uhr, schlafe)
            mess["gesamt_s"] = uhr() - beginn
            laeufe.append(mess)
        messungen["lese_job"] = {
            **statistik([m["gesamt_s"] for m in laeufe]),
            "max_abfrage_s": max(m["max_abfrage_s"] for m in laeufe),
            "max_ergebnis_s": max(m["ergebnis_s"] for m in laeufe),
        }
        abbruch = []
        for _ in range(n):
            auftrag = ausfuehrer.starte(lese_job, str(pfad))
            beginn = uhr()
            auftrag.abbrechen()
            abbruch.append(uhr() - beginn)
        messungen["abbrechen"] = statistik(abbruch)
        daten = geladen.messdaten
        kalt, warm, paar_name = _paar_zeit(daten, uhr)
        messungen["paar_kalt"] = {"s": kalt, "paar": paar_name}
        messungen["paar_warm"] = {"s": warm, "paar": paar_name}
        f_mitte = float(daten.frequenz_hz[daten.frequenz_hz.size // 2])
        sf = _wiederhole(2, lambda: schwingform_aus(daten, f_mitte), uhr)
        messungen["schwingform"] = {"kalt_s": sf[0], "warm_s": sf[1]}
        if mit_pruefung:
            _, mess = warte_auf(
                ausfuehrer.starte(
                    pruef_job, str(pfad), daten.herkunft.sha256 if daten.herkunft else None
                ),
                uhr,
                schlafe,
            )
            messungen["pruef_job"] = {
                "gesamt_s": mess["gesamt_s"],
                "max_abfrage_s": mess["max_abfrage_s"],
            }
        if mit_matplotlib:
            messungen["import_matplotlib"] = {"s": _matplotlib_import_s()}
    finally:
        ausfuehrer.beende()
    return {
        "umgebung": {
            "system": platform.platform(),
            "python": platform.python_version(),
            "cpu_anzahl": os.cpu_count(),
            "numpy": np.__version__,
            "ausfuehrer": type(ausfuehrer).__name__,
        },
        "datei": {"pfad": str(pfad), "groesse_byte": pfad.stat().st_size},
        "messungen": messungen,
    }


def formatiere(ergebnis: dict[str, Any]) -> str:
    """Lesbare Textausgabe (Millisekunden bzw. Sekunden) für das Prüfprotokoll."""
    u = ergebnis["umgebung"]
    zeilen = [
        f"System: {u['system']}, Python {u['python']}, {u['cpu_anzahl']} Kerne, NumPy {u['numpy']}",
        f"Ausführer: {u['ausfuehrer']}",
        f"Datei: {ergebnis['datei']['pfad']} ({ergebnis['datei']['groesse_byte'] / 1e6:.1f} MB)",
        "",
        f"{'Messung':<18}{'min':>10}{'Median':>10}{'max':>10}  Bemerkung",
    ]
    for name, m in ergebnis["messungen"].items():
        if "median_s" in m:
            bem = ""
            if "max_abfrage_s" in m:
                bem = (
                    f"längste fertig()-Abfrage {m['max_abfrage_s'] * 1e3:.0f} ms, "
                    f"ergebnis() {m['max_ergebnis_s'] * 1e3:.0f} ms"
                )
            zeilen.append(
                f"{name:<18}{m['min_s']:>9.3f}s{m['median_s']:>9.3f}s{m['max_s']:>9.3f}s  {bem}"
            )
        else:
            teile = ", ".join(
                f"{k} = {v:.3f} s" if isinstance(v, float) else f"{k} = {v}" for k, v in m.items()
            )
            zeilen.append(f"{name:<18}{teile}")
    return "\n".join(zeilen)


def main(argv: Sequence[str] | None = None) -> int:
    """Kommandozeile; gibt 0 bei Erfolg und 2 bei Fehler zurück."""
    parser = argparse.ArgumentParser(description="Zeiten beim Laden und Auswerten messen")
    parser.add_argument("datei", type=Path, help="PSV-Messdatei (.svd)")
    parser.add_argument("--wiederholungen", type=int, default=3)
    parser.add_argument("--json", type=Path, help="Ergebnis zusätzlich als JSON schreiben")
    parser.add_argument("--ohne-pruefung", action="store_true", help="pruef_job auslassen")
    parser.add_argument(
        "--ohne-matplotlib", action="store_true", help="matplotlib-Import auslassen"
    )
    args = parser.parse_args(argv)
    if not args.datei.is_file():
        print(f"Fehler: Datei fehlt: {args.datei}", file=sys.stderr)
        return 2
    try:
        ergebnis = messe(
            args.datei,
            wiederholungen=args.wiederholungen,
            mit_pruefung=not args.ohne_pruefung,
            mit_matplotlib=not args.ohne_matplotlib,
        )
    except (ValueError, OSError, TimeoutError) as exc:
        print(f"Fehler: {exc}", file=sys.stderr)
        return 2
    print(formatiere(ergebnis))
    if args.json is not None:
        args.json.write_text(
            json.dumps(ergebnis, ensure_ascii=False, indent=1) + "\n", encoding="utf-8"
        )
    return 0


if __name__ == "__main__":  # pragma: no cover - Kommandozeileneinstieg (spawn braucht den Guard)
    raise SystemExit(main())
