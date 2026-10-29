"""Kontrollplots zur Plausibilität der Dekodierung einer PSV-Messdatei (Werkzeug, Paket W2).

Je Datenart ein Bild: Autospektren und Betragsspektren, komplexe Spektren (CP, CPH),
Punktmittel im Vergleich mit den dekodierten Punktspektren, Banddaten auf der Geometrie.
Die Bilder sind Arbeitsmittel, keine Thesis-Abbildungen. Jede Ausgabe nennt das Skript
und den SHA-256 der Eingangsdatei (die Messdatei liegt nicht im Git).

Aufruf (aus ``software/``)::

    uv run python tools/svd_analyse/kontrollplots.py ../Input/<datei>.svd <ausgabeordner>
"""

from __future__ import annotations

import argparse
import hashlib
import sys
from collections.abc import Sequence
from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.figure import Figure
from svd_lesen import SvdFormatFehler, SvdMessung, lese_svd
from svd_pruefung import Auswerter, teile_argumente

SKRIPT = "software/tools/svd_analyse/kontrollplots.py"


def sha256_datei(pfad: Path) -> str:
    """SHA-256 einer Datei (nur lesend, blockweise)."""
    h = hashlib.sha256()
    with pfad.open("rb") as datei:
        for block in iter(lambda: datei.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def _fusszeile(fig: Figure, quelle: str) -> None:
    fig.text(0.01, 0.005, f"{SKRIPT} · Eingang SHA-256 {quelle[:16]}…", fontsize=6)


def bild_spektren(messung: SvdMessung, quelle: str) -> Figure:
    """Reelle Datenarten: AP der Vibrometerkanäle und ABS/AP der Kraftreferenz."""
    f = messung.frequenz_hz
    fig, (oben, unten) = plt.subplots(2, 1, figsize=(7, 6), sharex=True)
    stile = ["-", "--", ":"]
    aps = [s for s in messung.signale.values() if s.art == "AP" and s.kanaele[0].startswith("Vib")]
    for stil, s in zip(stile, aps, strict=False):
        oben.semilogy(f, np.median(np.real(s.werte), axis=0), stil, lw=0.8, label=s.kanaele[0])
    oben.set_ylabel("AP, Median über Punkte [(m/s)²]")
    oben.legend(fontsize=7)
    for s in messung.signale.values():
        if s.art == "ABS":
            ap = next(
                (a for a in messung.signale.values() if a.art == "AP" and a.kanaele == s.kanaele),
                None,
            )
            unten.semilogy(
                f,
                np.median(np.real(s.werte), axis=0),
                "-",
                lw=0.8,
                label=f"ABS {s.kanaele[0]} [{s.einheit}]",
            )
            if ap is not None:
                unten.semilogy(
                    f,
                    np.median(np.sqrt(np.real(ap.werte)), axis=0),
                    "--",
                    lw=0.8,
                    label=f"sqrt(AP {ap.kanaele[0]})",
                )
    unten.set_xlabel("Frequenz (vorläufige Achse k·Δf) [Hz]")
    unten.set_ylabel("Betrag, Median [Einheit lt. Datei]")
    unten.legend(fontsize=7)
    _fusszeile(fig, quelle)
    fig.tight_layout(rect=(0, 0.02, 1, 1))
    return fig


def bild_komplex(messung: SvdMessung, quelle: str, punkt: int = 0) -> Figure:
    """Komplexe Datenarten (CP, CPH) an einem Punkt: Betrag und Phase in rad."""
    f = messung.frequenz_hz
    fig, (oben, unten) = plt.subplots(2, 1, figsize=(7, 6), sharex=True)
    for stil, art in (("-", "CPH"), ("--", "CP")):
        s = next((x for x in messung.signale.values() if x.art == art), None)
        if s is None:
            plt.close(fig)
            raise SvdFormatFehler(f"Kontrollbild komplex: kein Signal der Art {art} vorhanden")
        z = s.werte[punkt]
        oben.semilogy(f, np.abs(z), stil, lw=0.8, label=f"{s.name} {art} {'/'.join(s.kanaele)}")
        unten.plot(f, np.angle(z), stil, lw=0.6, label=f"{s.name} {art}")
    label = int(messung.punkte.label[punkt])
    oben.set_ylabel(f"Betrag, Punktindex {punkt} (Label {label}) [lt. Datei]")
    oben.legend(fontsize=7)
    unten.set_ylabel("Phase (Vorzeichen offen) [rad]")
    unten.set_xlabel("Frequenz (vorläufige Achse k·Δf) [Hz]")
    _fusszeile(fig, quelle)
    fig.tight_layout(rect=(0, 0.02, 1, 1))
    return fig


def bild_punktmittel(messung: SvdMessung, quelle: str, nummern: Sequence[int]) -> Figure:
    """Punktmittel laut Datei (AvgSeq) gegen Mittel der dekodierten Punktspektren."""
    f = messung.frequenz_hz
    ausw = Auswerter(messung)
    fig, achsen = plt.subplots(len(nummern), 1, figsize=(7, 2.4 * len(nummern)), sharex=True)
    achsen_liste = np.atleast_1d(achsen)
    pm_nach_nr = {p.nummer: p for p in messung.punktmittel}
    for ax, nr in zip(achsen_liste, nummern, strict=True):
        pm = pm_nach_nr[nr]
        _, args = teile_argumente(pm.formel)
        eigen = np.mean(np.abs(ausw.wert(args[0])), axis=0)
        ax.semilogy(f, pm.werte, "-", lw=1.4, color="0.6", label="Datei (AvgSeq)")
        ax.semilogy(f, eigen, "--", lw=0.7, color="k", label="aus Punktspektren")
        ax.set_ylabel(f"AvgSeq {nr} [Einheit lt. Formel]", fontsize=8)
        ax.set_title(pm.formel, fontsize=6, loc="left")
        ax.legend(fontsize=6)
    achsen_liste[-1].set_xlabel("Frequenz (vorläufige Achse k·Δf) [Hz]")
    _fusszeile(fig, quelle)
    fig.tight_layout(rect=(0, 0.02, 1, 1))
    return fig


def bild_geometrie(messung: SvdMessung, quelle: str, band: str) -> Figure:
    """Messpunkte, Elementkanten und Bandwerte (Farbe) in der x-y-Ebene."""
    xyz = messung.punkte.koordinaten_m
    b = messung.baender[band]
    fig, ax = plt.subplots(figsize=(6, 7))
    for elem in messung.elemente:
        ring = [*elem, elem[0]]
        ax.plot(xyz[ring, 0], xyz[ring, 1], "-", lw=0.4, color="0.7")
    sc = ax.scatter(xyz[:, 0], xyz[:, 1], c=b.werte, cmap="viridis", s=25, zorder=3)
    for i in range(0, len(xyz), 9):
        ax.annotate(str(int(messung.punkte.label[i])), (xyz[i, 0], xyz[i, 1]), fontsize=6)
    fig.colorbar(sc, label=f"{band} Effektivwert {b.titel} [{b.einheit}]")
    ax.set_xlabel("x (Bezugssystem offen) [m]")
    ax.set_ylabel("y [m]")
    ax.set_aspect("equal")
    _fusszeile(fig, quelle)
    fig.tight_layout(rect=(0, 0.02, 1, 1))
    return fig


def erzeuge(datei: Path, ausgabe: Path) -> list[Path]:
    """Liest die Datei und schreibt alle Kontrollplots als PNG nach ``ausgabe``."""
    messung = lese_svd(datei)
    quelle = sha256_datei(datei)
    ausgabe.mkdir(parents=True, exist_ok=True)
    pm_nr = [p.nummer for p in messung.punktmittel]
    auswahl = [n for n in (0, 9, 17, 19) if n in pm_nr] or pm_nr[:1]
    band = next(
        (n for n, b in messung.baender.items() if b.einheit == "m/s"), next(iter(messung.baender))
    )
    bilder = {
        "w2_kontrolle_spektren_reell.png": bild_spektren(messung, quelle),
        "w2_kontrolle_spektren_komplex.png": bild_komplex(messung, quelle),
        "w2_kontrolle_punktmittel.png": bild_punktmittel(messung, quelle, auswahl),
        "w2_kontrolle_geometrie_band.png": bild_geometrie(messung, quelle, band),
    }
    pfade = []
    for name, fig in bilder.items():
        pfad = ausgabe / name
        fig.savefig(pfad, dpi=150)
        plt.close(fig)
        pfade.append(pfad)
    return pfade


def main(argv: Sequence[str] | None = None) -> int:
    """Kommandozeile: Kontrollplots erzeugen."""
    parser = argparse.ArgumentParser(description="Kontrollplots einer PSV-Messdatei")
    parser.add_argument("datei", type=Path)
    parser.add_argument("ausgabe", type=Path)
    args = parser.parse_args(argv)
    try:
        for pfad in erzeuge(args.datei, args.ausgabe):
            print(pfad)
    except (SvdFormatFehler, FileNotFoundError) as exc:
        print(f"Fehler: {exc}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":  # pragma: no cover - Kommandozeileneinstieg
    raise SystemExit(main())
