r"""Schreibt ausgewählte Spektren eines Scanpunkts über Polytec File Access als CSV (nur lesen).

Zweck: Golden File für den Vergleich mit dem eigenen .svd-Leser (Prüfschritte M1, M4, M8, M12):
Frequenzachse, Real- und Imaginärteil je Signal, wie PSV sie liefert. Die Datei wird mit
``ReadOnly = True`` geöffnet; nur eine Kopie verwenden, die nicht in PSV geöffnet ist. Dieses
Werkzeug nutzt den Whitelist-Proxy von ``erkundung.py`` nicht.

Aufruf (Windows, pywin32)::

    python daten_lesen.py "D:\...\kopie.svd" "D:\...\golden_punkt1.csv" [Punktnummer]
        [--ueberschreiben]

Annahmen (am Gerät nur durch Erkundung 1b vom 2026-11-02 belegt, hier nicht neu geprüft):

- Domäne 1 von ``GetPointDomains()`` ist die FFT-Domäne. Heißt sie nicht „FFT“, warnt das
  Skript und liest trotzdem.
- Display-Typ 7 ist der Realteil, Typ 8 der Imaginärteil.
- Kanal- und Signalnamen stehen in ``AUSWAHL`` (wie in der Datei benannt, Erkundung 1b).
- Die Länge der Frequenzachse ist über COM nicht abfragbar; sie wird aus ``len(Re)`` abgeleitet.
  Je Signal wird die Achse des eigenen Real-Displays gelesen und mit der des ersten
  übernommenen Signals verglichen (Werte, ``rtol`` 1e-12).

Ein Signal gilt als „fehlt“, wenn ein Lesefehler auftritt, ein Display fehlt, ``GetData`` für Re
oder Im keinen Wert liefert (Grund „keine Werte“), ``len(Re)``, ``len(Im)`` oder die Länge der
ersten Referenz abweichen oder die Achse abweicht.

Exit-Codes: 0 vollständig, 1 nichts gelesen (keine CSV), 2 Aufruffehler oder Zieldatei existiert
(ohne ``--ueberschreiben``), 3 unvollständig (CSV ohne die fehlenden Signale).

Unerwartete Ausnahmen außerhalb der Signalschleife (z. B. in ``Open``, ``GetPointDomains``)
werden nicht abgefangen: Das Skript gibt einen Traceback aus und endet mit Python-Exit-Code 1.
Dieser Exit-Code bedeutet dann also „Abbruch durch Ausnahme“ und nicht „nichts gelesen“; eine
CSV wird in diesem Fall nicht geschrieben. Bricht das Skript vor dem Schreiben ab, bleiben bei
``--ueberschreiben`` alte Ziel- und Begleitdatei stehen.

Begleitdatei bei Exit-Code 3: ``<ziel.csv>.fehlend.txt`` (UTF-8), erste Zeile
``# Fehlende Signale``, danach je Signal eine Zeile ``<Kanal> | <Signal><TAB><Grund>``.
Bei vollständigem Lauf mit ``--ueberschreiben`` wird eine alte Begleitdatei gelöscht.
"""

from __future__ import annotations

import argparse
import csv
import math
import sys
from pathlib import Path
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
DOMAENE_ERWARTET = "FFT"
ACHSE_RTOL = 1e-12  # Achsen desselben Displays müssen praktisch identisch sein
BEGLEIT_ENDUNG = ".fehlend.txt"


def display_nach_typ(signal: Any, typ: int) -> Any:
    """Liefert das erste Display des Signals mit dem Typ ``typ`` (``LookupError`` sonst)."""
    displays = signal.Displays
    for d in range(1, displays.Count + 1):
        disp = displays.Item(d)
        if disp.Type == typ:
            return disp
    raise LookupError(f"kein Display vom Typ {typ}")


def achsen_gleich(a: list[float], b: list[float]) -> bool:
    """Prüft gleiche Länge und elementweise ``isclose`` (``rtol`` ``ACHSE_RTOL``)."""
    return len(a) == len(b) and all(
        math.isclose(x, y, rel_tol=ACHSE_RTOL, abs_tol=0.0) for x, y in zip(a, b, strict=True)
    )


def lies_signal(domaene: Any, datenpunkt: Any, kanal: str, signal_name: str) -> dict[str, Any]:
    """Liest Re, Im und Achse eines Signals und prüft ``len(Re) == len(Im) == len(f)``.

    Returns
    -------
    dict
        ``re``, ``im``, ``f`` (je ``list[float]``) und ``einheit`` (``str``).

    Raises
    ------
    LookupError
        Display vom Typ 7 oder 8 fehlt.
    ValueError
        Re oder Im ist leer (``keine Werte``), oder Längen von Re, Im und Achse stimmen nicht
        überein.
    """
    signal = domaene.Channels.Item(kanal).Signals.Item(signal_name)
    d_re = display_nach_typ(signal, REAL)
    d_im = display_nach_typ(signal, IMAG)
    re = [float(v) for v in datenpunkt.GetData(d_re, 0)]
    im = [float(v) for v in datenpunkt.GetData(d_im, 0)]
    if not re or not im:
        raise ValueError("keine Werte")
    achse = domaene.GetXAxis(d_re)
    f = [float(achse.GetMidX(i)) for i in range(len(re))]
    if not len(re) == len(im) == len(f):
        raise ValueError(f"Längen Re={len(re)}, Im={len(im)}, Achse={len(f)} weichen ab")
    try:
        einheit = str(domaene.GetYAxes(d_re).Item(1).Unit)
    except Exception:  # Einheit nur zur Anzeige
        einheit = "(Einheit nicht lesbar)"
    return {"re": re, "im": im, "f": f, "einheit": einheit}


def schreibe_begleitdatei(ziel: Path, fehlend: list[tuple[str, str]]) -> Path:
    """Schreibt ``<ziel>.fehlend.txt`` mit ``<Signal><TAB><Grund>`` je fehlendem Signal."""
    pfad = ziel.with_name(ziel.name + BEGLEIT_ENDUNG)
    zeilen = ["# Fehlende Signale", *(f"{name}\t{grund}" for name, grund in fehlend)]
    pfad.write_text("\n".join(zeilen) + "\n", encoding="utf-8")
    return pfad


def main(pfad: str, ziel: str, punkt: int, ueberschreiben: bool = False) -> int:
    """Liest die Signale aus ``AUSWAHL`` und schreibt die CSV; Rückgabe ist der Exit-Code."""
    ziel_pfad = Path(ziel)
    begleit = ziel_pfad.with_name(ziel_pfad.name + BEGLEIT_ENDUNG)
    if not ueberschreiben:
        for vorhanden in (ziel_pfad, begleit):
            if vorhanden.exists():
                print(
                    f"Abbruch: {vorhanden} existiert bereits (--ueberschreiben erlaubt Ersetzen)."
                )
                return 2

    import win32com.client  # nur unter Windows mit pywin32

    pf = win32com.client.dynamic.Dispatch("PolyFile.PolyFile")
    pf.ReadOnly = True  # einzige Zuweisung: Schreibschutz vor dem Öffnen
    pf.Open(pfad)
    spalten: dict[str, list[float]] = {}
    fehlend: list[tuple[str, str]] = []
    frequenz: list[float] | None = None
    try:
        domaene = pf.GetPointDomains().Item(1)
        try:
            domaenenname = str(domaene.Name)
        except Exception as exc:  # nur Anzeige und Annahmeprüfung
            domaenenname = f"(nicht lesbar: {type(exc).__name__})"
        print(f"Domäne: {domaenenname}")
        if domaenenname != DOMAENE_ERWARTET:
            print(
                f"WARNUNG: Domäne 1 heißt nicht '{DOMAENE_ERWARTET}'; die Annahme "
                "'Domäne 1 = FFT' ist zu prüfen, die Daten werden trotzdem gelesen."
            )
        datenpunkt = domaene.DataPoints.Item(punkt)
        try:
            print(f"Punkt {punkt}: Label {datenpunkt.MeasPoint.Label}")
        except Exception as exc:  # Label nur zur Anzeige
            print(f"Punkt {punkt}: Label nicht lesbar ({type(exc).__name__})")
        for kanal_name, signal_name in AUSWAHL:
            schluessel = f"{kanal_name} | {signal_name}"
            try:
                daten = lies_signal(domaene, datenpunkt, kanal_name, signal_name)
                if frequenz is None:
                    frequenz = daten["f"]
                elif len(daten["f"]) != len(frequenz):
                    raise ValueError(
                        f"Frequenzachse hat {len(daten['f'])} Werte, das erste Signal hat "
                        f"{len(frequenz)}"
                    )
                elif not achsen_gleich(daten["f"], frequenz):
                    raise ValueError("Frequenzachse weicht von der des ersten Signals ab")
                spalten[f"{schluessel} | Re"] = daten["re"]
                spalten[f"{schluessel} | Im"] = daten["im"]
                print(f"ok    {schluessel}: {len(daten['re'])} Werte {daten['einheit']}")
            except Exception as exc:  # nur lesen, je Signal melden
                grund = f"{type(exc).__name__}: {exc}"
                fehlend.append((schluessel, grund))
                print(f"fehlt {schluessel}: {grund}")
    finally:
        pf.Close()
        print("Datei geschlossen.")
    if frequenz is None:
        print("Keine Daten gelesen.")
        return 1
    with open(ziel_pfad, "w" if ueberschreiben else "x", newline="", encoding="utf-8") as datei:
        w = csv.writer(datei, delimiter=";")
        w.writerow(["f_Hz", *spalten])
        for i, f in enumerate(frequenz):
            w.writerow([repr(f), *(repr(werte[i]) for werte in spalten.values())])
    print(f"CSV geschrieben: {ziel} ({len(frequenz)} Zeilen, {len(spalten)} Spalten)")
    if not fehlend:
        if ueberschreiben and begleit.exists():
            begleit.unlink()  # veraltete Begleitdatei eines früheren, unvollständigen Laufs
        return 0
    schreibe_begleitdatei(ziel_pfad, fehlend)
    print(f"HINWEIS: {len(fehlend)} von {len(AUSWAHL)} Signalen fehlen, CSV ist unvollständig:")
    for name, grund in fehlend:
        print(f"  - {name}: {grund}")
    print(f"Begleitdatei: {begleit}")
    return 3


def cli(argv: list[str]) -> int:
    """Wertet die Kommandozeile aus und ruft ``main`` auf."""
    parser = argparse.ArgumentParser(
        prog="daten_lesen.py", description="Spektren eines Scanpunkts als CSV (nur lesen)."
    )
    parser.add_argument("svd", help="Kopie der .svd-Datei (nicht in PSV geöffnet)")
    parser.add_argument("ziel", help="Ziel-CSV (darf nicht existieren)")
    parser.add_argument("punkt", nargs="?", type=int, default=1, help="Punktnummer (Standard 1)")
    parser.add_argument("--ueberschreiben", action="store_true", help="vorhandene Ziele ersetzen")
    try:
        args = parser.parse_args(argv)
    except SystemExit as exc:  # argparse beendet mit 2 (Aufruffehler) bzw. 0 (--help)
        return int(exc.code) if isinstance(exc.code, int) else 2
    return main(args.svd, args.ziel, args.punkt, args.ueberschreiben)


if __name__ == "__main__":
    sys.exit(cli(sys.argv[1:]))
