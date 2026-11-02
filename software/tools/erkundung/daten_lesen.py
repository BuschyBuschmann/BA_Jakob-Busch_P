"""Schreibt ausgewählte Spektren eines Scanpunkts über Polytec File Access als CSV (nur lesen).

Zweck: Golden File für den Vergleich mit dem eigenen .svd-Leser (Prüfschritte M1, M4, M8, M12):
Frequenzachse, Real- und Imaginärteil je Signal, wie PSV sie liefert. Die Datei wird mit
``ReadOnly = True`` geöffnet; nur eine Kopie verwenden, die nicht in PSV geöffnet ist.

Aufruf (Windows, pywin32)::

    python daten_lesen.py "D:\\...\\kopie.svd" "D:\\...\\golden_punkt1.csv" [Punktnummer, Standard 1]
"""

from __future__ import annotations

import csv
import sys
from typing import Any

# (Kanal, Signal) wie in der Datei benannt (Erkundung 1b, 2026-11-02); fehlende werden gemeldet.
AUSWAHL = [
    ("Vib X", "Geschwindigkeit"),
    ("Vib Y", "Geschwindigkeit"),
    ("Vib Z", "Geschwindigkeit"),
    ("Ref1", "Kraft"),
    ("Ref2", "Beschleunigung"),
    ("Vib X & Ref1", "H1 Geschwindigkeit / Kraft"),
    ("Vib Z & Ref1", "H1 Geschwindigkeit / Kraft"),
    ("Ref2 & Ref1", "H1 Beschleunigung / Kraft"),
]
REAL, IMAG = 7, 8  # Display-Typen laut Erkundung 1b (Real, Imaginär)


def display_nach_typ(signal: Any, typ: int) -> Any:
    displays = signal.Displays
    for d in range(1, displays.Count + 1):
        disp = displays.Item(d)
        if disp.Type == typ:
            return disp
    raise LookupError(f"kein Display vom Typ {typ}")


def main(pfad: str, ziel: str, punkt: int) -> int:
    import win32com.client  # nur unter Windows mit pywin32

    pf = win32com.client.dynamic.Dispatch("PolyFile.PolyFile")
    pf.ReadOnly = True  # einzige Zuweisung: Schreibschutz vor dem Öffnen
    pf.Open(pfad)
    try:
        domaene = pf.GetPointDomains().Item(1)
        print(f"Domäne: {domaene.Name}")
        datenpunkt = domaene.DataPoints.Item(punkt)
        try:
            print(f"Punkt {punkt}: Label {datenpunkt.MeasPoint.Label}")
        except Exception as exc:  # noqa: BLE001
            print(f"Punkt {punkt}: Label nicht lesbar ({type(exc).__name__})")
        spalten: dict[str, list[float]] = {}
        frequenz: list[float] | None = None
        for kanal_name, signal_name in AUSWAHL:
            schluessel = f"{kanal_name} | {signal_name}"
            try:
                signal = domaene.Channels.Item(kanal_name).Signals.Item(signal_name)
                d_re = display_nach_typ(signal, REAL)
                d_im = display_nach_typ(signal, IMAG)
                re = list(datenpunkt.GetData(d_re, 0))
                im = list(datenpunkt.GetData(d_im, 0))
                if frequenz is None:
                    achse = domaene.GetXAxis(d_re)
                    frequenz = [float(achse.GetMidX(i)) for i in range(len(re))]
                try:
                    einheit = str(domaene.GetYAxes(d_re).Item(1).Unit)
                except Exception:  # noqa: BLE001 - Einheit nur zur Anzeige
                    einheit = "(Einheit nicht lesbar)"
                spalten[f"{schluessel} | Re"] = [float(v) for v in re]
                spalten[f"{schluessel} | Im"] = [float(v) for v in im]
                print(f"ok    {schluessel}: {len(re)} Werte {einheit}")
            except Exception as exc:  # noqa: BLE001 - nur lesen, je Signal melden
                print(f"fehlt {schluessel}: {type(exc).__name__}: {exc}")
    finally:
        pf.Close()
        print("Datei geschlossen.")
    if frequenz is None:
        print("Keine Daten gelesen.")
        return 1
    with open(ziel, "w", newline="", encoding="utf-8") as datei:
        w = csv.writer(datei, delimiter=";")
        w.writerow(["f_Hz", *spalten])
        for i, f in enumerate(frequenz):
            w.writerow([repr(f), *(repr(werte[i]) for werte in spalten.values())])
    print(f"CSV geschrieben: {ziel} ({len(frequenz)} Zeilen, {len(spalten)} Spalten)")
    return 0


if __name__ == "__main__":
    if len(sys.argv) not in (3, 4):
        print("Aufruf: python daten_lesen.py <kopie.svd> <ziel.csv> [Punktnummer]")
        sys.exit(2)
    sys.exit(main(sys.argv[1], sys.argv[2], int(sys.argv[3]) if len(sys.argv) == 4 else 1))
