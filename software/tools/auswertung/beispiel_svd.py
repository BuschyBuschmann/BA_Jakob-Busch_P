"""Beispiel: PSV-Messdatei nach FG-02 Stufe 1 auswerten, exportieren, Abbildungen erzeugen.

Ablauf (Paket W5-1, A6):

1. SHA-256 der Messdatei bilden, Datei mit dem W2-Leser ``svd_lesen.lese_svd`` nur lesend
   einlesen (Werkzeug ``tools/svd_analyse``, unverändert).
2. Über :func:`ldv_automation.auswertung.svd_adapter.aus_svd_messung` in den Datenvertrag
   überführen und mit :func:`ldv_automation.auswertung.werte_aus` auswerten
   (Voreinstellungen M1–M11 aus FG-02; Gesamtband; Antriebspunkt für P-08 wählbar).
3. Betriebsschwingform an der höchsten Spitze des Betragsmittels |H1| von
   ``Vib Z/Ref1`` (oder bei ``--f-schwingform``).
4. Export ``<ausgabe>/<name>.npz`` + ``.json``; danach SHA-256 der Messdatei erneut
   prüfen (muss gleich sein).
5. Abbildungen aus dem gespeicherten Export (``abbildungen.erzeuge``).

Alle Ergebnisse gelten **vorbehaltlich der Annahmen M1–M11** (FG-02 Abschnitt 11).

Aufruf (aus ``software/``)::

    uv run python tools/auswertung/beispiel_svd.py ../Input/20261012_ref_Mitte.svd \
        --export <ordner> --abbildungen <ordner>
"""

from __future__ import annotations

import argparse
import dataclasses
import importlib
import sys
from collections.abc import Callable, Sequence
from pathlib import Path
from typing import Any

import abbildungen

from ldv_automation.auswertung import Annahmen, Auswertung, schwingform_aus, werte_aus
from ldv_automation.auswertung.export import exportiere, sha256_datei
from ldv_automation.auswertung.gesamt import hoechste_spitze
from ldv_automation.auswertung.svd_adapter import aus_svd_messung

SVD_WERKZEUG = Path(__file__).resolve().parents[1] / "svd_analyse"
PAAR_SCHWINGFORM = ("Vib Z", "Ref1")

Leser = Callable[[Path], Any]


def lese_svd_werkzeug(pfad: Path) -> Any:
    """Ruft ``svd_lesen.lese_svd`` aus ``tools/svd_analyse`` auf (Modul unverändert)."""
    if str(SVD_WERKZEUG) not in sys.path:
        sys.path.insert(0, str(SVD_WERKZEUG))
    modul = importlib.import_module("svd_lesen")
    return modul.lese_svd(pfad)


def zusammenfassung(auswertung: Auswertung, paar: tuple[str, str] = PAAR_SCHWINGFORM) -> str:
    """Textübersicht: Prüfungen, Spitzen eines Paars, Schwingform (vorbehaltlich M1–M11)."""
    zeilen = ["Ergebnisse vorbehaltlich der Annahmen M1–M11 (FG-02 Abschnitt 11)", ""]
    zeilen.append("Plausibilitätsprüfungen:")
    for e in auswertung.pruefungen:
        wert = "–" if e.wert is None else f"{e.wert:.6g}"
        bezug = f" [{e.bezug}]" if e.bezug else ""
        zeilen.append(f"  {e.id}{bezug}: {e.status} ({wert}) {e.grund}")
    if paar in auswertung.paare:
        sp = auswertung.paare[paar].spitzen
        zeilen += ["", f"Spitzen {sp.groesse} [{sp.einheit}], Δf = {sp.delta_f_hz:g} Hz:"]
        zeilen.append("  Nr  f_sp [Hz]   Höhe        B [Hz]    Q        ζ         Kennzeichen")
        for i, s in enumerate(sp.spitzen, start=1):
            zeilen.append(
                f"  {i:>2}  {s.f_sp_hz:9.3f}  {s.hoehe:.4e}  {s.breite_3db_hz:7.3f}  "
                f"{s.q:7.1f}  {s.zeta:.5f}  {', '.join(s.kennzeichen) or '–'}"
            )
    sf = auswertung.schwingform
    if sf is not None:
        zeilen += [
            "",
            f"Schwingform bei {sf.f_hz:g} Hz (gewählt {sf.f_wahl_hz:.4f} Hz, Linie {sf.linie}, "
            f"Quelle {sf.quelle}): max betrag_3d_psv {float(sf.betrag_3d_psv.max()):.4e} "
            f"{sf.einheit}",
        ]
    return "\n".join(zeilen)


def auswerten(
    datei: Path,
    *,
    leser: Leser = lese_svd_werkzeug,
    annahmen: Annahmen | None = None,
    f_schwingform_hz: float | None = None,
    antriebspunkt: tuple[str, str, Any] | None = ("Ref2", "Ref1", "akzeleranz"),
) -> tuple[Auswertung, str]:
    """Liest und wertet eine Datei aus; gibt Auswertung und SHA-256 (vorher) zurück."""
    sha_vorher = sha256_datei(datei)
    daten = aus_svd_messung(leser(datei), sha256=sha_vorher)
    paare = set(daten.cp)
    ap = antriebspunkt if antriebspunkt and antriebspunkt[:2] in paare else None
    f0 = float(daten.frequenz_hz[0])
    f1 = float(daten.frequenz_hz[-1])
    auswertung = werte_aus(daten, annahmen=annahmen, antriebspunkt=ap, baender=[(f0, f1)])
    f_sf = f_schwingform_hz
    if f_sf is None and PAAR_SCHWINGFORM in auswertung.paare:
        f_sf = hoechste_spitze(auswertung.paare[PAAR_SCHWINGFORM].spitzen)
    if f_sf is not None:
        auswertung = dataclasses.replace(
            auswertung, schwingform=schwingform_aus(daten, f_sf, annahmen=auswertung.annahmen)
        )
    return auswertung, sha_vorher


def main(argv: Sequence[str] | None = None, *, leser: Leser = lese_svd_werkzeug) -> int:
    """Kommandozeile; Rückgabe 0 bei Erfolg, 2 bei Eingabefehler, 3 bei veränderter Datei."""
    parser = argparse.ArgumentParser(description="PSV-Datei nach FG-02 Stufe 1 auswerten")
    parser.add_argument("datei", type=Path)
    parser.add_argument("--export", type=Path, required=True, help="Ordner für den Export")
    parser.add_argument("--abbildungen", type=Path, help="Ordner für die Abbildungen")
    parser.add_argument("--name", help="Basisname des Exports (Voreinstellung: Dateiname)")
    parser.add_argument("--f-schwingform", type=float, help="Frequenz der Schwingform in Hz")
    parser.add_argument("--ohne-antriebspunkt", action="store_true", help="P-08 nicht prüfen")
    parser.add_argument("--ueberschreiben", action="store_true")
    args = parser.parse_args(argv)
    datei: Path = args.datei
    if not datei.is_file():
        print(f"Fehler: Datei fehlt: {datei}", file=sys.stderr)
        return 2
    auswertung, sha_vorher = auswerten(
        datei,
        leser=leser,
        f_schwingform_hz=args.f_schwingform,
        antriebspunkt=None if args.ohne_antriebspunkt else ("Ref2", "Ref1", "akzeleranz"),
    )
    args.export.mkdir(parents=True, exist_ok=True)
    basis = args.export / (args.name or datei.stem)
    try:
        npz, js = exportiere(auswertung, basis, ueberschreiben=args.ueberschreiben)
    except FileExistsError as exc:
        print(f"Fehler: {exc}", file=sys.stderr)
        return 2
    if sha256_datei(datei) != sha_vorher:
        print("Fehler: Messdatei hat sich während der Auswertung verändert", file=sys.stderr)
        return 3
    print(zusammenfassung(auswertung))
    print(f"\nExport: {npz}\n        {js}\nMessdatei SHA-256 vor/nach: {sha_vorher} (gleich)")
    if args.abbildungen is not None:
        for pfad in abbildungen.erzeuge(basis, args.abbildungen):
            print(f"Abbildung: {pfad}")
    return 0


if __name__ == "__main__":  # pragma: no cover - Kommandozeileneinstieg
    raise SystemExit(main())
