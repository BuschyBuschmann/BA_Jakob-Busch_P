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

Mit ``--stufe2`` folgt die Auswertung Stufe 2 nach FG-03 (Paket W5-2): B-1 an
``Vib Z/Ref1`` und ``Ref2/Ref1``, Drift an ``Ref2/Ref1`` bei den Frequenzen aus ``--drift-f``
(Zeitstempel M15), B-8 mit den Elementen der Datei (M14) und Anteil der Normalenbewegung η
von CPH zu Ref1 in drei Bändern (FG-03 Abschnitt 7); Export ``<name>_stufe2.npz`` + ``.json``.

Alle Ergebnisse gelten **vorbehaltlich der Annahmen M1–M11** (FG-02 Abschnitt 11) bzw.
**M1–M15** (FG-03 Abschnitt 11).

Aufruf (aus ``software/``)::

    uv run python tools/auswertung/beispiel_svd.py ../Input/20261012_ref_Mitte.svd \
        --export <ordner> --abbildungen <ordner>
    uv run python tools/auswertung/beispiel_svd.py ../Input/20261012_ref_Mitte.svd \
        --export <ordner> --stufe2 --drift-f 418.8 631.2 1507.8
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
import numpy as np

from ldv_automation.auswertung import Annahmen, Auswertung, schwingform_aus, werte_aus
from ldv_automation.auswertung.annahmen import AnnahmenStufe2, SchwellenStufe2
from ldv_automation.auswertung.bezug3d import zerlege
from ldv_automation.auswertung.export import exportiere, sha256_datei
from ldv_automation.auswertung.gesamt import hoechste_spitze
from ldv_automation.auswertung.stufe2 import Stufe2Ergebnis, exportiere_stufe2, werte_stufe2_aus
from ldv_automation.auswertung.svd_adapter import (
    aus_svd_messung,
    elemente_aus_svd_messung,
    zeit_s_aus_svd_messung,
)
from ldv_automation.auswertung.vergleich import amplituden

SVD_WERKZEUG = Path(__file__).resolve().parents[1] / "svd_analyse"
PAAR_SCHWINGFORM = ("Vib Z", "Ref1")
PAARE_STUFE2: tuple[tuple[str, str], ...] = (("Vib Z", "Ref1"), ("Ref2", "Ref1"))
DRIFT_PAAR = ("Ref2", "Ref1")
BAENDER_ETA_HZ: tuple[tuple[float, float], ...] = (
    (150.0, 500.0),
    (500.0, 1000.0),
    (1000.0, 2500.0),
)

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


def stufe2_auswerten(
    auswertung: Auswertung,
    messung: Any,
    *,
    drift_f_hz: Sequence[float] = (),
    annahmen2: AnnahmenStufe2 | None = None,
    schwellen2: SchwellenStufe2 | None = None,
) -> Stufe2Ergebnis:
    """Stufe 2 (FG-03) an einer Stufe-1-Auswertung; Elemente und Zeitstempel aus der Messung.

    Ohne Elemente entfällt B-8, ohne ``drift_f_hz`` oder ohne Antriebspunkt-Paar die Drift.
    """
    annahmen2 = annahmen2 if annahmen2 is not None else AnnahmenStufe2()
    paare = [p for p in PAARE_STUFE2 if p in auswertung.paare]
    elemente = elemente_aus_svd_messung(messung) if getattr(messung, "elemente", None) else None
    mit_drift = bool(drift_f_hz) and DRIFT_PAAR in auswertung.paare
    zeit = zeit_s_aus_svd_messung(messung, annahmen2=annahmen2) if mit_drift else None
    return werte_stufe2_aus(
        auswertung,
        paare=paare,
        zeit_s=zeit,
        drift_paar=DRIFT_PAAR if mit_drift else None,
        drift_spitzen_hz=tuple(drift_f_hz) if mit_drift else (),
        elemente=elemente,
        annahmen2=annahmen2,
        schwellen2=schwellen2,
    )


def eta_baender(
    ergebnis: Stufe2Ergebnis, baender: Sequence[tuple[float, float]] = BAENDER_ETA_HZ
) -> list[tuple[float, float, float, float]]:
    """Median und 10-%-Quantil von η (CPH zu Ref1) je Band ``(f_u, f_o]`` (FG-03 7, B-8)."""
    kb = ergebnis.komponenten
    aw = ergebnis.auswertung
    if kb is None or PAAR_SCHWINGFORM not in aw.paare:
        return []
    amp, ist_3d = amplituden(aw, PAAR_SCHWINGFORM, ergebnis.annahmen2)
    if not ist_3d:
        return []
    eta = zerlege(np.moveaxis(amp, 1, 2), kb.normale_punkt[:, None, :]).anteil_normal
    f = aw.daten.frequenz_hz
    werte = []
    for f_u, f_o in baender:
        b = (f > f_u) & (f <= f_o)
        if np.any(b):
            auswahl = eta[:, b]
            auswahl = auswahl[np.isfinite(auswahl)]
            werte.append((f_u, f_o, float(np.median(auswahl)), float(np.quantile(auswahl, 0.1))))
    return werte


def zusammenfassung_stufe2(ergebnis: Stufe2Ergebnis) -> str:
    """Textübersicht der Stufe 2 (vorbehaltlich M1–M15)."""
    zeilen = ["", "Stufe 2 (FG-03), vorbehaltlich der Annahmen M1–M15 (FG-03 Abschnitt 11)"]
    for e in ergebnis.annahmen2.eintraege():
        zeilen.append(f"  {e.nr} {e.parameter} = {e.wert} [{e.status}]")
    for (a, b), r in ergebnis.daempfung.items():
        zeilen += ["", f"B-1 {a}/{b} ({r.frf_art}), {len(r.ergebnisse)} Fits, je Spitze:"]
        zeilen.append("  f_sp [Hz]  n  f_r Median [Hz] (IQR)   ζ Median (IQR)        rho   Punkte")
        for z in r.zusammenfassung:
            n = len(r.gruppen[z.gruppe].spitzen)
            zeilen.append(
                f"  {z.f_sp_hz:9.3f}  {n}  {z.fr_median_hz:10.3f} ({z.fr_iqr_hz:.3f})  "
                f"{z.zeta_median:.5f} ({z.zeta_iqr:.5f})  {z.rho_median:.3f}  {z.n_punkte}"
            )
    if ergebnis.drift:
        zeilen += ["", "Drift (B-5):"]
        for d in ergebnis.drift:
            zeilen.append(
                f"  {d.f_spitze_hz:9.3f} Hz: b1 = {d.steigung_hz_h:+.4f} ± "
                f"{d.sd_steigung_hz_h:.4f} Hz/h, über {d.dauer_s / 60:.1f} min "
                f"{d.gesamt_hz:+.4f} Hz ({d.gesamt_rel:+.2e}), Streuung {d.streuung_hz:.4f} Hz, "
                f"N = {d.n_punkte} (davon modell_passt_nicht {d.n_modell_passt_nicht}), "
                f"{'signifikant' if d.signifikant else 'nicht signifikant'}"
                f"{'' if d.pruefbar else ' (nicht prüfbar)'}"
            )
    kb = ergebnis.komponenten
    if kb is not None:
        en = kb.elemente
        roh_neg = int(np.sum(en.normale[:, 2] > 0))
        winkel = np.degrees(
            np.arccos(np.clip(kb.normale_punkt @ ergebnis.annahmen2.e_ref_vektor, -1, 1))
        )
        zeilen += [
            "",
            f"B-8: {len(en.elemente)} Elemente ({roh_neg} nach Ausrichtung mit n_z > 0), "
            f"Punktnormalen gegen e_ref: min {np.nanmin(winkel):.2f}°, Median "
            f"{np.nanmedian(winkel):.2f}°, max {np.nanmax(winkel):.2f}°",
        ]
        for f_u, f_o, med, q10 in eta_baender(ergebnis):
            zeilen.append(f"  η {f_u:g}–{f_o:g} Hz: Median {med:.4f}, 10-%-Quantil {q10:.4f}")
        zeilen.extend(f"  Hinweis: {h}" for h in kb.hinweise)
    return "\n".join(zeilen)


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
    parser.add_argument("--stufe2", action="store_true", help="zusätzlich Stufe 2 (FG-03)")
    parser.add_argument(
        "--drift-f", type=float, nargs="*", default=[], help="Spitzen der Drift in Hz (Stufe 2)"
    )
    parser.add_argument(
        "--drift-ausschluss",
        nargs="*",
        default=None,
        help="Kennzeichen der gewählten Mode, die einen Punkt aus der Drift ausschließen "
        "(Voreinstellung FG-03 4.5: ausserhalb_band unsicher moden_vertauscht; leer = keins)",
    )
    parser.add_argument(
        "--drift-mit-nicht-konvergiert",
        action="store_true",
        help="nicht_konvergiert bei n = 1 nicht ausschließen (Voreinstellung: ausschließen)",
    )
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
    if args.stufe2:
        messung = leser(datei)  # nur lesend; Elemente und Zeitstempel für Stufe 2
        schwellen2 = SchwellenStufe2(
            drift_nicht_konvergiert_einzelmode=not args.drift_mit_nicht_konvergiert
        )
        if args.drift_ausschluss is not None:
            schwellen2 = dataclasses.replace(
                schwellen2, drift_ausschluss=tuple(args.drift_ausschluss)
            )
        ergebnis = stufe2_auswerten(
            auswertung, messung, drift_f_hz=args.drift_f, schwellen2=schwellen2
        )
        basis2 = basis.with_name(basis.name + "_stufe2")
        try:
            npz2, js2 = exportiere_stufe2(ergebnis, basis2, ueberschreiben=args.ueberschreiben)
        except FileExistsError as exc:
            print(f"Fehler: {exc}", file=sys.stderr)
            return 2
        if sha256_datei(datei) != sha_vorher:
            print("Fehler: Messdatei hat sich während der Auswertung verändert", file=sys.stderr)
            return 3
        print(zusammenfassung_stufe2(ergebnis))
        print(f"\nExport Stufe 2: {npz2}\n                {js2}")
    return 0


if __name__ == "__main__":  # pragma: no cover - Kommandozeileneinstieg
    raise SystemExit(main())
