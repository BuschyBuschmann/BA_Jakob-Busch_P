"""Messskript für den Messrechner: Arbeitsspeicher je geöffneter Messung (R-058, P-AUSW2 S5).

Die Obergrenze :data:`~ldv_automation.gui.messungen.MESSUNGEN_MAX` beruht auf Zahlen eines
Linux-Containers (rund 115 MiB je Messung der Beispieldatei mit zwei Kanalpaaren). Dieses Skript
wiederholt die Messung am Messrechner: Es öffnet dieselben Dateien nacheinander (wie der Reiter
mit „Messung hinzufügen …“) und liest nach jedem Schritt den Arbeitsspeicher (RSS) des Prozesses.

Je Messung werden ausgegeben: Zuwachs durch das Laden (Stufe A), Zuwachs durch ``--paare``
ausgewertete Kanalpaare (``PaarCache``, Voreinstellung 2) und die Untergrenze aus den
NumPy-Feldern (:func:`~ldv_automation.gui.messungen.nbytes_von`) zum Vergleich. Der RSS kommt
unter Linux aus ``/proc/self/statm``, unter Windows aus ``GetProcessMemoryInfo`` (``ctypes``),
sonst aus ``resource``; es wird keine neue Abhängigkeit gebraucht.

Aufruf (aus ``software/``; am Messrechner mit dem Python der Installation)::

    python tools/auswertung/speicher_messen.py <datei.svd> [<weitere.svd> ...]
        [--wiederholen 4] [--paare 2] [--json ergebnis.json]

Mit nur einer Datei und ``--wiederholen 4`` wird sie viermal geöffnet. Das Skript liest die
Messdatei nur und schreibt nichts außer der angegebenen JSON-Datei. Die Zahlen gehören in das
Prüfprotokoll; danach wird ``MESSUNGEN_MAX`` angepasst (nicht als bestanden zu werten, sondern
zu lesen).
"""

from __future__ import annotations

import argparse
import json
import os
import platform
import sys
from collections.abc import Callable, Sequence
from pathlib import Path
from typing import Any

from ldv_automation.auswertung.laden import Geladen, lade_svd
from ldv_automation.darstellung.auswahl import PaarCache
from ldv_automation.gui.messungen import nbytes_von

MIB = 1024.0 * 1024.0


def rss_mib() -> float:
    """Arbeitsspeicher (RSS) des laufenden Prozesses in MiB."""
    statm = Path("/proc/self/statm")
    if statm.is_file():  # Linux: Seiten
        seiten = int(statm.read_text(encoding="ascii").split()[1])
        return seiten * os.sysconf("SC_PAGE_SIZE") / MIB
    if sys.platform == "win32":  # pragma: no cover - nur am Messrechner
        import ctypes
        from ctypes import wintypes

        class _Zaehler(ctypes.Structure):
            _fields_ = [
                ("cb", wintypes.DWORD),
                ("PageFaultCount", wintypes.DWORD),
                ("PeakWorkingSetSize", ctypes.c_size_t),
                ("WorkingSetSize", ctypes.c_size_t),
                ("QuotaPeakPagedPoolUsage", ctypes.c_size_t),
                ("QuotaPagedPoolUsage", ctypes.c_size_t),
                ("QuotaPeakNonPagedPoolUsage", ctypes.c_size_t),
                ("QuotaNonPagedPoolUsage", ctypes.c_size_t),
                ("PagefileUsage", ctypes.c_size_t),
                ("PeakPagefileUsage", ctypes.c_size_t),
            ]

        zaehler = _Zaehler()
        zaehler.cb = ctypes.sizeof(_Zaehler)
        handle = ctypes.windll.kernel32.GetCurrentProcess()  # type: ignore[attr-defined]
        ctypes.windll.psapi.GetProcessMemoryInfo(  # type: ignore[attr-defined]
            handle, ctypes.byref(zaehler), zaehler.cb
        )
        return float(zaehler.WorkingSetSize) / MIB
    import resource  # pragma: no cover - sonstige Systeme

    return float(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss) / 1024.0  # pragma: no cover


def messe(
    dateien: Sequence[str],
    *,
    paare: int = 2,
    rss: Callable[[], float] = rss_mib,
    lade: Callable[[str], Geladen] = lade_svd,
) -> list[dict[str, Any]]:
    """Öffnet die Dateien nacheinander und misst den Speicherzuwachs je Messung.

    Parameters
    ----------
    dateien : sequence of str
        ``.svd``-Dateien in der Reihenfolge des Öffnens (dieselbe Datei darf mehrfach stehen).
    paare : int
        Zahl der Kanalpaare je Messung, die ausgewertet werden (Voreinstellung 2, wie in
        Ansicht 1 mit mehreren Komponenten).
    rss, lade : callable
        Speichermessung und Leser (für Tests ersetzbar).

    Returns
    -------
    list of dict
        Je Messung ``nr``, ``datei``, ``zuwachs_laden_mib``, ``zuwachs_paare_mib``,
        ``rss_nach_mib``, ``untergrenze_mib`` und ``paare`` (tatsächlich ausgewertet).

    Raises
    ------
    ValueError
        ``paare`` kleiner als 0 oder keine Datei.
    """
    if paare < 0 or not dateien:
        raise ValueError("Mindestens eine Datei und paare >= 0 nötig.")
    gehalten: list[tuple[Geladen, PaarCache]] = []  # lebt weiter: der Reiter behält alle Messungen
    ergebnis: list[dict[str, Any]] = []
    for nr, datei in enumerate(dateien, start=1):
        vorher = rss()
        geladen = lade(datei)
        nach_laden = rss()
        cache = PaarCache(geladen.messdaten, groesse=max(paare, 1))
        gewaehlt = list(geladen.messdaten.cp)[:paare]
        for antwort, referenz in gewaehlt:
            cache.paar(antwort, referenz)
        nach_paaren = rss()
        gehalten.append((geladen, cache))
        ergebnis.append(
            {
                "nr": nr,
                "datei": str(datei),
                "zuwachs_laden_mib": nach_laden - vorher,
                "zuwachs_paare_mib": nach_paaren - nach_laden,
                "rss_nach_mib": nach_paaren,
                "untergrenze_mib": (
                    nbytes_von(geladen.messdaten) + nbytes_von(list(cache.alle_paare()))
                )
                / MIB,
                "paare": len(gewaehlt),
            }
        )
    return ergebnis


def tabelle(messwerte: Sequence[dict[str, Any]]) -> str:
    """Text der Ergebnistabelle (eine Zeile je Messung, Summe darunter)."""
    zeilen = [
        f"{'Nr':>2}  {'Laden':>9}  {'Paare':>9}  {'RSS nach':>9}  {'Untergrenze':>11}  Datei",
    ]
    for m in messwerte:
        zeilen.append(
            f"{m['nr']:>2}  {m['zuwachs_laden_mib']:>6.1f} MiB  {m['zuwachs_paare_mib']:>6.1f} MiB"
            f"  {m['rss_nach_mib']:>6.1f} MiB  {m['untergrenze_mib']:>8.1f} MiB  {m['datei']}"
        )
    summe = sum(m["zuwachs_laden_mib"] + m["zuwachs_paare_mib"] for m in messwerte)
    zeilen.append(f"Zuwachs insgesamt: {summe:.1f} MiB bei {len(messwerte)} Messung(en)")
    return "\n".join(zeilen)


def main(argv: Sequence[str] | None = None) -> int:
    """Einstieg: misst, druckt die Tabelle und schreibt optional JSON."""
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0] if __doc__ else "")
    parser.add_argument("dateien", nargs="+", help=".svd-Dateien in Reihenfolge des Öffnens")
    parser.add_argument("--wiederholen", type=int, default=1, help="alle Dateien so oft öffnen")
    parser.add_argument("--paare", type=int, default=2, help="ausgewertete Kanalpaare je Messung")
    parser.add_argument("--json", help="Ergebnis zusätzlich als JSON schreiben")
    args = parser.parse_args(argv)
    if args.wiederholen < 1:
        parser.error("--wiederholen muss >= 1 sein")
    dateien = [d for _ in range(args.wiederholen) for d in args.dateien]
    fehlend = [d for d in dateien if not Path(d).is_file()]
    if fehlend:
        parser.error(f"Datei nicht gefunden: {fehlend[0]}")
    werte = messe(dateien, paare=args.paare)
    print(tabelle(werte))
    if args.json:
        kopf = {"python": platform.python_version(), "system": platform.platform()}
        Path(args.json).write_text(
            json.dumps({"umgebung": kopf, "messungen": werte}, indent=2, ensure_ascii=False),
            encoding="utf-8",
        )
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
