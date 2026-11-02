r"""Schreibt ausgewählte Spektren eines Scanpunkts über Polytec File Access als CSV (nur lesen).

Zweck: Golden File für den Vergleich mit dem eigenen .svd-Leser (Prüfschritte M1, M4, M8, M12):
Frequenzachse, Real- und Imaginärteil je Signal, wie PSV sie liefert. Die Datei wird mit
``ReadOnly = True`` geöffnet; nur eine Kopie verwenden, die nicht in PSV geöffnet ist. Dieses
Werkzeug nutzt den Whitelist-Proxy von ``erkundung.py`` nicht.

Aufruf (Windows, pywin32)::

    python daten_lesen.py "D:\...\kopie.svd" "D:\...\golden_punkt1.csv" [Punktnummer]
        [--ueberschreiben] [--signal "Kanal|Signal" ...] [--auswahl DATEI] [--domaene NAME]
        [--amplitude]
    python daten_lesen.py "D:\...\kopie.svd" --liste [--domaene NAME]

Signalauswahl: ohne ``--signal``/``--auswahl`` gilt ``AUSWAHL``. ``--auswahl`` liest eine
UTF-8-Textdatei (eine Zeile je Paar ``Kanal | Signal``, ganze Zeilen mit ``#`` am Anfang und
Leerzeilen werden ignoriert); ``--signal`` darf mehrfach stehen und wird hinten angehängt.
``--domaene NAME`` sucht die Domäne nach Namen (Exit 2 mit Liste der vorhandenen, wenn nicht
gefunden); ohne die Option gilt Domäne 1 mit Warnung, falls sie nicht „FFT“ heißt.
Signale ohne Real-/Imaginärteil (Display 7/8), aber mit Amplitude-Display (Typ 1), werden
automatisch als Betragsgröße gelesen (CSV-Spalte ``| Abs``); ``--amplitude`` erzwingt das für
alle gewählten Signale. ``--liste`` gibt Domänen, Kanäle, Signale und Display-Typen der
gewählten Domäne vollständig aus und schreibt keine CSV (nur lesend).

Annahmen (am Gerät nur durch Erkundung 1b vom 2026-11-02 belegt, hier nicht neu geprüft):

- Domäne 1 von ``GetPointDomains()`` ist die FFT-Domäne. Heißt sie nicht „FFT“, warnt das
  Skript und liest trotzdem.
- Display-Typ 7 ist der Realteil, Typ 8 der Imaginärteil, Typ 1 die Amplitude (Erkundung 1b).
- Kanal- und Signalnamen stehen in ``AUSWAHL`` (wie in der Datei benannt, Erkundung 1b).
- Die Länge der Frequenzachse ist über COM nicht abfragbar; sie wird aus ``len(Re)`` abgeleitet.
  Je Signal wird die Achse des eigenen ersten Displays (Real bzw. Amplitude) gelesen und mit
  der des ersten übernommenen Signals verglichen (Werte, ``rtol`` 1e-12).

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
REAL, IMAG, AMPLITUDE = 7, 8, 1  # Display-Typen laut Erkundung 1b (Real, Imaginär, Amplitude)
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


def _finde_display(signal: Any, typ: int) -> Any | None:
    """Wie ``display_nach_typ``, liefert aber ``None`` statt ``LookupError``."""
    try:
        return display_nach_typ(signal, typ)
    except LookupError:
        return None


def lies_signal(
    domaene: Any, datenpunkt: Any, kanal: str, signal_name: str, amplitude: bool = False
) -> dict[str, Any]:
    """Liest Werte und Achse eines Signals und prüft gleiche Längen.

    Normalfall: Real (Typ 7) und Imaginär (Typ 8), Spalten ``Re``/``Im``. Hat das Signal weder
    Typ 7 noch Typ 8, aber Typ 1 (Amplitude), oder ist ``amplitude`` gesetzt, wird nur die
    Amplitude gelesen (Spalte ``Abs``).

    Returns
    -------
    dict
        ``spalten`` (``dict[str, list[float]]``, Suffix -> Werte), ``f`` (``list[float]``) und
        ``einheit`` (``str``).

    Raises
    ------
    LookupError
        Ein benötigtes Display fehlt.
    ValueError
        Ein Wert ist leer (``keine Werte``), oder Längen der Werte und der Achse stimmen nicht
        überein.
    """
    signal = domaene.Channels.Item(kanal).Signals.Item(signal_name)
    displays: list[tuple[str, Any]] | None = None
    if amplitude:
        displays = [("Abs", display_nach_typ(signal, AMPLITUDE))]
    elif _finde_display(signal, REAL) is None and _finde_display(signal, IMAG) is None:
        d_abs = _finde_display(signal, AMPLITUDE)
        if d_abs is not None:
            displays = [("Abs", d_abs)]
    if displays is None:
        displays = [("Re", display_nach_typ(signal, REAL)), ("Im", display_nach_typ(signal, IMAG))]
    spalten = {suffix: [float(v) for v in datenpunkt.GetData(disp, 0)] for suffix, disp in displays}
    if not all(spalten.values()):
        raise ValueError("keine Werte")
    erstes = displays[0][1]
    achse = domaene.GetXAxis(erstes)
    n_werte = [len(v) for v in spalten.values()]
    f = [float(achse.GetMidX(i)) for i in range(n_werte[0])]
    if len({*n_werte, len(f)}) != 1:
        beschreibung = ", ".join(f"{k}={len(v)}" for k, v in spalten.items())
        raise ValueError(f"Längen {beschreibung}, Achse={len(f)} weichen ab")
    try:
        einheit = str(domaene.GetYAxes(erstes).Item(1).Unit)
    except Exception:  # Einheit nur zur Anzeige
        einheit = "(Einheit nicht lesbar)"
    return {"spalten": spalten, "f": f, "einheit": einheit}


def parse_paar(text: str) -> tuple[str, str]:
    """Zerlegt ``Kanal | Signal`` am ersten ``|``; ``ValueError`` bei leerem Teil oder ohne."""
    kanal, trenner, signal = text.partition("|")
    kanal, signal = kanal.strip(), signal.strip()
    if not trenner or not kanal or not signal:
        raise ValueError(f"'{text}' ist kein Paar 'Kanal | Signal'")
    return kanal, signal


def lies_auswahl_datei(pfad: Path) -> list[tuple[str, str]]:
    """Liest Paare aus einer UTF-8-Textdatei (``#``-Zeilen und Leerzeilen werden ignoriert)."""
    paare = []
    for nr, zeile in enumerate(pfad.read_text(encoding="utf-8-sig").splitlines(), start=1):
        zeile = zeile.strip()
        if not zeile or zeile.startswith("#"):
            continue
        try:
            paare.append(parse_paar(zeile))
        except ValueError as exc:
            raise ValueError(f"{pfad} Zeile {nr}: {exc}") from exc
    return paare


def waehle_domaene(pf: Any, name: str | None) -> Any | None:
    """Domäne nach Namen (``name``) oder Domäne 1 (``None``, mit Warnung); ``None`` wenn fehlt."""
    domaenen = pf.GetPointDomains()
    if name is None:
        domaene = domaenen.Item(1)
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
        return domaene
    vorhanden: list[str] = []
    for i in range(1, int(domaenen.Count) + 1):
        domaene = domaenen.Item(i)
        try:
            domaenenname = str(domaene.Name)
        except Exception as exc:  # Name nur zur Suche; nicht lesbare Domäne überspringen
            vorhanden.append(f"(nicht lesbar: {type(exc).__name__})")
            continue
        vorhanden.append(domaenenname)
        if domaenenname == name:
            print(f"Domäne: {domaenenname} (Nr. {i})")
            return domaene
    print(f"Domäne '{name}' nicht gefunden. Vorhanden: {', '.join(vorhanden) or '(keine)'}")
    return None


def _name(objekt: Any) -> str:
    try:
        return str(objekt.Name)
    except Exception as exc:  # nur Anzeige
        return f"(nicht lesbar: {type(exc).__name__})"


def liste_domaene(domaene: Any) -> None:
    """Gibt alle Kanäle, Signale und Display-Typen der Domäne aus (nur lesend)."""
    kanaele = domaene.Channels
    for c in range(1, int(kanaele.Count) + 1):
        kanal = kanaele.Item(c)
        print(f"Kanal {c}: {_name(kanal)}")
        signale = kanal.Signals
        for s in range(1, int(signale.Count) + 1):
            signal = signale.Item(s)
            displays = signal.Displays
            texte = []
            for d in range(1, int(displays.Count) + 1):
                disp = displays.Item(d)
                try:
                    typ = str(disp.Type)
                except Exception as exc:  # nur Anzeige
                    typ = f"? ({type(exc).__name__})"
                texte.append(f"Typ {typ} {_name(disp)}")
            print(f"  Signal {s}: {_name(signal)}  [{'; '.join(texte)}]")


def oeffne_readonly(pfad: str) -> Any:
    """Öffnet die Datei über PolyFile mit ``ReadOnly = True`` (einzige Zuweisung des Moduls)."""
    import win32com.client  # nur unter Windows mit pywin32

    pf = win32com.client.dynamic.Dispatch("PolyFile.PolyFile")
    pf.ReadOnly = True  # Schreibschutz vor dem Öffnen
    pf.Open(pfad)
    return pf


def liste(pfad: str, domaene_name: str | None = None) -> int:
    """Gibt für ``--liste`` Domänen und Struktur der gewählten Domäne aus, ohne CSV (Exit 0/2)."""
    pf = oeffne_readonly(pfad)
    try:
        domaenen = pf.GetPointDomains()
        namen = [f"{i}: {_name(domaenen.Item(i))}" for i in range(1, int(domaenen.Count) + 1)]
        print(f"Domänen: {'; '.join(namen) or '(keine)'}")
        domaene = waehle_domaene(pf, domaene_name)
        if domaene is None:
            return 2
        liste_domaene(domaene)
    finally:
        pf.Close()
        print("Datei geschlossen.")
    return 0


def schreibe_begleitdatei(ziel: Path, fehlend: list[tuple[str, str]]) -> Path:
    """Schreibt ``<ziel>.fehlend.txt`` mit ``<Signal><TAB><Grund>`` je fehlendem Signal."""
    pfad = ziel.with_name(ziel.name + BEGLEIT_ENDUNG)
    zeilen = ["# Fehlende Signale", *(f"{name}\t{grund}" for name, grund in fehlend)]
    pfad.write_text("\n".join(zeilen) + "\n", encoding="utf-8")
    return pfad


def main(
    pfad: str,
    ziel: str,
    punkt: int,
    ueberschreiben: bool = False,
    auswahl: list[tuple[str, str]] | None = None,
    domaene_name: str | None = None,
    amplitude: bool = False,
) -> int:
    """Liest die Signale (``auswahl`` oder ``AUSWAHL``) und schreibt die CSV; Exit-Code."""
    auswahl = list(AUSWAHL) if auswahl is None else auswahl
    ziel_pfad = Path(ziel)
    begleit = ziel_pfad.with_name(ziel_pfad.name + BEGLEIT_ENDUNG)
    if not ueberschreiben:
        for vorhanden in (ziel_pfad, begleit):
            if vorhanden.exists():
                print(
                    f"Abbruch: {vorhanden} existiert bereits (--ueberschreiben erlaubt Ersetzen)."
                )
                return 2

    pf = oeffne_readonly(pfad)
    spalten: dict[str, list[float]] = {}
    fehlend: list[tuple[str, str]] = []
    frequenz: list[float] | None = None
    try:
        domaene = waehle_domaene(pf, domaene_name)
        if domaene is None:
            return 2
        datenpunkt = domaene.DataPoints.Item(punkt)
        try:
            print(f"Punkt {punkt}: Label {datenpunkt.MeasPoint.Label}")
        except Exception as exc:  # Label nur zur Anzeige
            print(f"Punkt {punkt}: Label nicht lesbar ({type(exc).__name__})")
        for kanal_name, signal_name in auswahl:
            schluessel = f"{kanal_name} | {signal_name}"
            try:
                daten = lies_signal(domaene, datenpunkt, kanal_name, signal_name, amplitude)
                if frequenz is None:
                    frequenz = daten["f"]
                elif len(daten["f"]) != len(frequenz):
                    raise ValueError(
                        f"Frequenzachse hat {len(daten['f'])} Werte, das erste Signal hat "
                        f"{len(frequenz)}"
                    )
                elif not achsen_gleich(daten["f"], frequenz):
                    raise ValueError("Frequenzachse weicht von der des ersten Signals ab")
                for suffix, werte in daten["spalten"].items():
                    spalten[f"{schluessel} | {suffix}"] = werte
                print(f"ok    {schluessel}: {len(daten['f'])} Werte {daten['einheit']}")
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
    print(f"HINWEIS: {len(fehlend)} von {len(auswahl)} Signalen fehlen, CSV ist unvollständig:")
    for name, grund in fehlend:
        print(f"  - {name}: {grund}")
    print(f"Begleitdatei: {begleit}")
    return 3


def cli(argv: list[str]) -> int:
    """Wertet die Kommandozeile aus und ruft ``main`` bzw. ``liste`` auf."""
    parser = argparse.ArgumentParser(
        prog="daten_lesen.py", description="Spektren eines Scanpunkts als CSV (nur lesen)."
    )
    parser.add_argument("svd", help="Kopie der .svd-Datei (nicht in PSV geöffnet)")
    parser.add_argument("ziel", nargs="?", help="Ziel-CSV (darf nicht existieren)")
    parser.add_argument("punkt", nargs="?", type=int, default=1, help="Punktnummer (Standard 1)")
    parser.add_argument("--ueberschreiben", action="store_true", help="vorhandene Ziele ersetzen")
    parser.add_argument(
        "--signal", action="append", default=[], metavar="KANAL|SIGNAL", help="Paar (mehrfach)"
    )
    parser.add_argument("--auswahl", metavar="DATEI", help="Textdatei, je Zeile 'Kanal | Signal'")
    parser.add_argument("--domaene", metavar="NAME", help="Domäne nach Namen (Standard: Nr. 1)")
    parser.add_argument(
        "--amplitude", action="store_true", help="alle Signale als Amplitude (Typ 1) lesen"
    )
    parser.add_argument(
        "--liste", action="store_true", help="Kanäle/Signale/Display-Typen ausgeben, keine CSV"
    )
    try:
        args = parser.parse_args(argv)
    except SystemExit as exc:  # argparse beendet mit 2 (Aufruffehler) bzw. 0 (--help)
        return int(exc.code) if isinstance(exc.code, int) else 2
    if args.liste:
        return liste(args.svd, args.domaene)
    if args.ziel is None:
        print("Aufruffehler: Ziel-CSV fehlt (oder --liste verwenden).")
        return 2
    auswahl: list[tuple[str, str]] | None = None
    if args.signal or args.auswahl:
        try:
            auswahl = lies_auswahl_datei(Path(args.auswahl)) if args.auswahl else []
            auswahl += [parse_paar(t) for t in args.signal]
        except (OSError, ValueError) as exc:
            print(f"Aufruffehler: {exc}")
            return 2
        if not auswahl:
            print("Aufruffehler: Signalauswahl ist leer.")
            return 2
        if len(set(auswahl)) != len(auswahl):
            print("Aufruffehler: Signalauswahl enthält doppelte Paare.")
            return 2
    return main(
        args.svd, args.ziel, args.punkt, args.ueberschreiben, auswahl, args.domaene, args.amplitude
    )


if __name__ == "__main__":
    sys.exit(cli(sys.argv[1:]))
