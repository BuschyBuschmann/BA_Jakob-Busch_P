"""Abbildungen der Auswertung Stufe 1 aus einem gespeicherten Export (Paket W5-1, B-6).

Liest ausschließlich den Export ``<basis>.npz`` + ``<basis>.json`` (FG-02 Abschnitt 5) mit
NumPy und JSON und importiert nichts aus dem Hauptpaket. Erzeugt je Kanalpaar:

- ``frf_<paar>``: Betragsmittel |H1| (logarithmisch) mit gefundenen Spitzen und
  Kennzeichnung der Linien mit Kohärenz-Punktmittel unter der Schwelle (Marker, nicht nur
  Farbe); darunter das arithmetische Punktmittel der Kohärenz mit Schwelle.
- ``spektren_<paar>``: Betragsmittel ``spektrum_kohaerent`` und quadratisches Mittel
  ``spektrum_leistung`` (Spitzenwerte), Linien mit Kohärenz unter der Schwelle markiert.

und, falls im Export enthalten, ``schwingform``: 3D-Betrag je Punkt und Momentanwert
der Z-Komponente bei θ = 0 auf den Punktkoordinaten (Graustufen).

Stil nach KONVENTIONEN (Abbildungen): Achsen „Größe [Einheit]“, kein Diagrammtitel, keine
Information nur über Farbe, kein Gelb, auf A5 lesbar. Die Fußzeile nennt Skript,
Git-Hash der Software, SHA-256 der Messdatei und des Exports sowie die offenen Annahmen.

Aufruf (aus ``software/``)::

    uv run python tools/auswertung/abbildungen.py <basis ohne Endung> <ausgabeordner>
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from collections.abc import Sequence
from pathlib import Path
from typing import Any

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
import numpy.typing as npt
from cycler import cycler
from matplotlib.figure import Figure

SKRIPT = "software/tools/auswertung/abbildungen.py"
BREITE_IN = 5.8  # etwa 14,7 cm: Satzspiegel A4, auf A5 verkleinert noch lesbar
SCHRIFT_PT = 9
FORMATE = ("pdf", "png")

plt.rcParams.update(
    {
        "font.size": SCHRIFT_PT,
        "axes.labelsize": SCHRIFT_PT,
        "legend.fontsize": SCHRIFT_PT - 1,
        "xtick.labelsize": SCHRIFT_PT - 1,
        "ytick.labelsize": SCHRIFT_PT - 1,
        "axes.prop_cycle": cycler(color=["black", "0.45"]),
    }
)


class ExportFehler(ValueError):  # noqa: N818  (fachlicher Name)
    """Der Export ist unvollständig oder beschädigt."""


def _sha256(pfad: Path) -> str:
    h = hashlib.sha256()
    with pfad.open("rb") as datei:
        for block in iter(lambda: datei.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def lese(basis: Path) -> tuple[dict[str, npt.NDArray[Any]], dict[str, Any]]:
    """Liest Felder und Metadaten eines Exports und prüft den SHA-256 der ``.npz``-Datei."""
    npz = basis.with_name(basis.name + ".npz")
    js = basis.with_name(basis.name + ".json")
    meta: dict[str, Any] = json.loads(js.read_text(encoding="utf-8"))
    if meta.get("format") != "ldv_automation.auswertung.export":
        raise ExportFehler(f"kein Auswertungsexport: {js}")
    if _sha256(npz) != meta.get("npz_sha256"):
        raise ExportFehler(f"SHA-256 von {npz.name} passt nicht zu den Metadaten")
    with np.load(npz, allow_pickle=False) as archiv:
        felder = {name: archiv[name] for name in archiv.files}
    return felder, meta


def fusszeile(meta: dict[str, Any]) -> str:
    """Herkunftszeile: Skript, Git-Hash, SHA-256 von Messdatei und Export, offene Annahmen."""
    herkunft = meta.get("herkunft", {})
    software = herkunft.get("software", {})
    git_hash = software.get("git_hash") or "ohne Git-Hash"
    git_hash = f"{git_hash[:10]}+Änderungen" if software.get("git_dirty") else git_hash[:10]
    quelle = (herkunft.get("messdatei_sha256") or "unbekannt")[:12]
    offen = [a["nr"] for a in meta.get("annahmen", []) if a.get("status") == "Annahme"]
    offen_text = ", ".join(dict.fromkeys(offen)) or "keine"
    return (
        f"{SKRIPT} · Software {git_hash} · Messdatei SHA-256 {quelle}…\n"
        f"Export SHA-256 {meta.get('npz_sha256', '')[:12]}… · Annahmen offen: {offen_text}"
    )


def _fusszeile(fig: Figure, meta: dict[str, Any]) -> None:
    fig.text(0.01, 0.005, fusszeile(meta), fontsize=5.5, ha="left", va="bottom", linespacing=1.3)


def _einheit_klammer(einheit: str) -> str:
    return einheit.replace("^2", "²")


def bild_frf(felder: dict[str, npt.NDArray[Any]], meta: dict[str, Any], schluessel: str) -> Figure:
    """Betragsmittel |H1| mit Spitzen und Kohärenzkennzeichnung, darunter die Kohärenz."""
    paar = meta["paare"][schluessel]
    f = felder["frequenz_hz"]
    h1 = felder[f"abgeleitet.{schluessel}.mittel_betrag_h1"]
    g2 = felder[f"abgeleitet.{schluessel}.mittel_kohaerenz"]
    g2_min = float(paar["kohaerenz_min"])
    name = paar["bezeichnung_h1"]
    einheit = _einheit_klammer(paar["einheit_frf"])
    fig, (oben, unten) = plt.subplots(
        2, 1, figsize=(BREITE_IN, 5.0), sharex=True, gridspec_kw={"height_ratios": [2.2, 1.0]}
    )
    oben.semilogy(f, h1, "-", color="black", lw=0.7, label=f"|{name}|, Betragsmittel")
    with np.errstate(invalid="ignore"):
        niedrig = g2 < g2_min
    if np.any(niedrig):
        oben.semilogy(
            f[niedrig],
            h1[niedrig],
            "x",
            color="0.45",
            ms=2.5,
            mew=0.6,
            label=rf"Linien mit $\bar{{\gamma}}^2 < {g2_min:g}$",
        )
    spitzen = paar["spitzen"]["spitzen"]
    ohne = [s for s in spitzen if not s["kennzeichen"]]
    mit = [s for s in spitzen if s["kennzeichen"]]
    if ohne:
        oben.plot(
            [s["f_sp_hz"] for s in ohne],
            [s["hoehe"] * 1.35 for s in ohne],
            "v",
            color="black",
            ms=4,
            label="Spitze ohne Kennzeichen",
        )
    if mit:
        oben.plot(
            [s["f_sp_hz"] for s in mit],
            [s["hoehe"] * 1.35 for s in mit],
            "v",
            mfc="white",
            mec="black",
            ms=4,
            mew=0.7,
            label="Spitze mit Kennzeichen",
        )
    oben.set_ylabel(f"|{name}|, Betragsmittel [{einheit}]")
    oben.legend(loc="lower center", bbox_to_anchor=(0.5, 1.0), frameon=False, ncol=2)
    unten.plot(f, g2, "-", color="black", lw=0.7, label=r"$\bar{\gamma}^2$, Punktmittel")
    unten.axhline(
        g2_min, color="0.45", ls="--", lw=0.8, label=rf"$\gamma^2_\mathrm{{min}} = {g2_min:g}$"
    )
    unten.set_ylim(0.0, 1.05)
    unten.set_ylabel(r"$\bar{\gamma}^2$ [1]")
    unten.set_xlabel("Frequenz f [Hz]")
    unten.legend(loc="lower right", frameon=False, ncol=2)
    unten.set_xlim(float(f[0]), float(f[-1]))
    fig.tight_layout(rect=(0, 0.045, 1, 1))
    _fusszeile(fig, meta)
    return fig


def bild_spektren(
    felder: dict[str, npt.NDArray[Any]], meta: dict[str, Any], schluessel: str
) -> Figure:
    """Punktmittel von spektrum_kohaerent (Betragsmittel) und spektrum_leistung (quadratisch)."""
    paar = meta["paare"][schluessel]
    f = felder["frequenz_hz"]
    kohaerent = felder[f"abgeleitet.{schluessel}.mittel_betrag_spektrum_kohaerent"]
    leistung = felder[f"abgeleitet.{schluessel}.mittel_quadratisch_spektrum_leistung"]
    einheit = _einheit_klammer(meta["konventionen"]["einheiten"][paar["antwort"]])
    fig, ax = plt.subplots(figsize=(BREITE_IN, 3.6))
    ax.semilogy(
        f,
        leistung,
        "--",
        color="0.45",
        lw=0.7,
        label=f"spektrum_leistung √AP, quadratisches Mittel ({paar['antwort']})",
    )
    ax.semilogy(
        f,
        kohaerent,
        "-",
        color="black",
        lw=0.7,
        label=f"spektrum_kohaerent |CPH|, Betragsmittel (zu {paar['referenz']})",
    )
    g2 = felder[f"abgeleitet.{schluessel}.mittel_kohaerenz"]
    g2_min = float(paar["kohaerenz_min"])
    with np.errstate(invalid="ignore"):
        niedrig = g2 < g2_min
    if np.any(niedrig):
        ax.semilogy(
            f[niedrig],
            kohaerent[niedrig],
            "x",
            color="0.45",
            ms=2.5,
            mew=0.6,
            label=rf"Linien mit $\bar{{\gamma}}^2 < {g2_min:g}$",
        )
    ax.set_xlabel("Frequenz f [Hz]")
    ax.set_ylabel(f"{paar['antwort']}, Spitzenwert [{einheit}]")
    ax.set_xlim(float(f[0]), float(f[-1]))
    ax.legend(loc="lower center", bbox_to_anchor=(0.5, 1.0), frameon=False)
    fig.tight_layout(rect=(0, 0.06, 1, 1))
    _fusszeile(fig, meta)
    return fig


def bild_schwingform(felder: dict[str, npt.NDArray[Any]], meta: dict[str, Any]) -> Figure:
    """3D-Betrag je Punkt und Momentanwert u_z(θ = 0) auf den Koordinaten x, y."""
    sf = meta["schwingform"]
    xyz = felder["punkte.koordinaten_m"]
    gueltig = felder["punkte.gueltig"].astype(bool)
    betrag = felder["schwingform.betrag_3d_psv"]
    einheit = _einheit_klammer(sf["einheit"])
    mit_phase = "schwingform.amplitude.re" in felder
    spalten = 2 if mit_phase else 1
    fig, achsen = plt.subplots(1, spalten, figsize=(BREITE_IN, 2.9), squeeze=False)
    ax = achsen[0][0]
    bild = ax.scatter(
        xyz[gueltig, 0],
        xyz[gueltig, 1],
        c=betrag[gueltig],
        cmap="Greys",
        s=18,
        edgecolors="black",
        linewidths=0.3,
    )
    fig.colorbar(bild, ax=ax, label=f"betrag_3d_psv [{einheit}]")
    if np.any(~gueltig):
        ax.plot(xyz[~gueltig, 0], xyz[~gueltig, 1], "x", color="black", ms=4, label="ungültig")
        ax.legend(frameon=False)
    ax.set_xlabel("x [m]")
    ax.set_ylabel("y [m]")
    ax.set_aspect("equal")
    if mit_phase:
        u_z = felder["schwingform.amplitude.re"][:, 2]  # Re{v̂_z e^{i·0}}
        grenze = float(np.max(np.abs(u_z[gueltig]))) or 1.0
        ax2 = achsen[0][1]
        bild2 = ax2.scatter(
            xyz[gueltig, 0],
            xyz[gueltig, 1],
            c=u_z[gueltig],
            cmap="gray",
            vmin=-grenze,
            vmax=grenze,
            s=18,
            edgecolors="black",
            linewidths=0.3,
        )
        fig.colorbar(bild2, ax=ax2, label=f"u_z(θ = 0) [{einheit}]")
        ax2.set_xlabel("x [m]")
        ax2.set_aspect("equal")
    fig.text(
        0.01,
        0.06,
        f"f = {sf['f_hz']:.4g} Hz, Quelle {sf['quelle']}, Referenz {sf['referenz'] or 'keine'}",
        fontsize=7,
    )
    fig.tight_layout(rect=(0, 0.1, 1, 1))
    _fusszeile(fig, meta)
    return fig


def _speichere(fig: Figure, ziel: Path, name: str) -> list[Path]:
    pfade = []
    for endung in FORMATE:
        pfad = ziel / f"{name}.{endung}"
        fig.savefig(pfad, dpi=200)
        pfade.append(pfad)
    plt.close(fig)
    return pfade


def erzeuge(basis: Path, ziel: Path, paare: Sequence[str] | None = None) -> list[Path]:
    """Erzeugt alle Abbildungen eines Exports in ``ziel`` (Ordner wird angelegt).

    Parameters
    ----------
    basis : pathlib.Path
        Exportbasis ohne Endung.
    ziel : pathlib.Path
        Ausgabeordner.
    paare : sequence of str, optional
        Paarschlüssel (z. B. ``"Vib_Z__Ref1"``); Voreinstellung alle.

    Returns
    -------
    list of pathlib.Path
        Geschriebene Dateien.
    """
    felder, meta = lese(basis)
    ziel.mkdir(parents=True, exist_ok=True)
    auswahl = list(meta["paare"]) if paare is None else list(paare)
    unbekannt = [p for p in auswahl if p not in meta["paare"]]
    if unbekannt:
        raise ExportFehler(f"Paare nicht im Export: {unbekannt}")
    pfade: list[Path] = []
    for schluessel in auswahl:
        pfade += _speichere(bild_frf(felder, meta, schluessel), ziel, f"frf_{schluessel}")
        pfade += _speichere(bild_spektren(felder, meta, schluessel), ziel, f"spektren_{schluessel}")
    if meta.get("schwingform") is not None:
        pfade += _speichere(bild_schwingform(felder, meta), ziel, "schwingform")
    return pfade


def main(argv: Sequence[str] | None = None) -> int:
    """Kommandozeile: Abbildungen aus einem Export erzeugen."""
    parser = argparse.ArgumentParser(description="Abbildungen aus einem Auswertungsexport")
    parser.add_argument("basis", type=Path, help="Exportbasis ohne Endung")
    parser.add_argument("ziel", type=Path, help="Ausgabeordner")
    parser.add_argument("--paar", action="append", help="Paarschlüssel, z. B. Vib_Z__Ref1")
    args = parser.parse_args(argv)
    try:
        pfade = erzeuge(args.basis, args.ziel, args.paar)
    except (ExportFehler, FileNotFoundError, KeyError) as exc:
        print(f"Fehler: {exc}", file=sys.stderr)
        return 2
    for p in pfade:
        print(p)
    return 0


if __name__ == "__main__":  # pragma: no cover - Kommandozeileneinstieg
    raise SystemExit(main())
