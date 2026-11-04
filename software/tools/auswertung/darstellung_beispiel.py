"""Beispiel: Thesis-Abbildungen der vier Ansichten mit denselben Zeichenfunktionen (UI-18).

Die Oberfläche (Reiter „Auswerten“) und dieses Skript rufen **dieselben** Zeichenfunktionen aus
:mod:`ldv_automation.darstellung` auf (``zeichne_spektrum``, ``zeichne_frf``, ``zeichne_spitzen``,
``zeichne_schwingform``). Das Skript nutzt :data:`~ldv_automation.darstellung.stil.THESIS_STIL`
(Graustufen, 9 pt), **keinen** Arbeitsstempel und keinen Diagrammtitel (KONVENTIONEN,
Abbildungsregeln). Aus denselben Daten entstehen deshalb dieselbe Linienzahl und dieselben
Achsenbeschriftungen wie in der Oberfläche.

Je Abbildung entsteht neben der Bilddatei eine gleichnamige ``.json`` mit dem erzeugenden Skript,
SHA-256 der Messdatei und Git-Hash der Software (KONVENTIONEN: „Jede Ausgabe nennt das erzeugende
Skript und den Git-Hash der Eingangsdaten“). Ausgabeordner für die Thesis:
``in_progress/thesis/abbildungen/``.

Aufruf (aus ``software/``)::

    uv run python tools/auswertung/darstellung_beispiel.py ../Input/20261012_ref_Mitte.svd \
        --ausgabe <ordner> [--punkt-label 132] [--frequenz-hz 167.5] [--format pdf]

Ohne ``--punkt-label`` zeigt Ansicht 1 das Mittel aller Punkte. Die Phase gegen die Referenz wird
in den Thesis-Abbildungen nicht gezeigt, solange die Annahme M8 offen ist (Ansicht 2 ohne Phase).
Ansicht 3 beschriftet die stärkste Spitze (größte Kurvenhöhe). Ansicht 4 erscheint zweimal: als
3D-Betrag (``schwingform``) und, mit Referenz, als Phase der Komponente Z **relativ zum
Bezugspunkt** (``schwingform_phase``, unabhängig von M8); beide im Hochformat 11,5 cm breit, die
Höhe folgt aus dem Seitenverhältnis der Punktwolke.
"""

from __future__ import annotations

import argparse
import json
import sys
from collections.abc import Sequence
from pathlib import Path
from typing import Any

from matplotlib.figure import Figure

from ldv_automation.auswertung.daten import Messdaten
from ldv_automation.auswertung.export import sha256_datei
from ldv_automation.auswertung.laden import lade_svd
from ldv_automation.darstellung.auswahl import (
    DarstellungsFehler,
    Groesse,
    PaarCache,
    frf_daten,
    gesamtband,
    kanalpaare,
    schwingform_daten,
    spektrum_daten,
    spitzen_daten_frf,
    spitzen_daten_spektrum,
    verfuegbare_groessen,
)
from ldv_automation.darstellung.bild import neue_figure
from ldv_automation.darstellung.frf import FrfOptionen, zeichne_frf
from ldv_automation.darstellung.schwingform import (
    SchwingformOptionen,
    bildgroesse_schwingform,
    zeichne_schwingform,
)
from ldv_automation.darstellung.spektrum import SpektrumOptionen, zeichne_spektrum
from ldv_automation.darstellung.spitzen import SpitzenOptionen, zeichne_spitzen
from ldv_automation.darstellung.stil import THESIS_STIL
from ldv_automation.darstellung.zeichnung import Zeichnung
from ldv_automation.protokoll.version import ermittle_build_info

SKRIPT = "software/tools/auswertung/darstellung_beispiel.py"
GROESSE_ZOLL = (4.9, 3.3)
"""Breite etwa 12,4 cm (Satzspiegel A5), damit Schrift und Linien im Druck lesbar bleiben."""
GROESSE_ZOLL_HOCH = (4.9, 4.4)
GROESSE_ZOLL_SPITZEN = (4.9, 3.8)
"""Höhe so, dass der Beschriftungsstreifen (drei Zeilen) die Kurve nicht staucht (Layout 3.1)."""
BREITE_SCHWINGFORM_CM = 11.5
"""Breite der Schwingform-Abbildungen; die Höhe folgt aus dem Datenaspekt (Hochformat, 4.2)."""
KOMPONENTE_PHASE = "Z"
"""Komponente der Phase relativ zum Bezugspunkt (Messrichtung des Vibrometers)."""


def _punkt_index(daten: Messdaten, label: int | None) -> int | None:
    if label is None:
        return None
    treffer = [i for i, wert in enumerate(daten.punkte.label) if int(wert) == label]
    if not treffer:
        raise SystemExit(f"Punkt mit Label {label} existiert nicht in der Datei.")
    return treffer[0]


def erzeuge_figuren(
    daten: Messdaten,
    *,
    punkt_label: int | None = None,
    frequenz_hz: float | None = None,
) -> dict[str, Zeichnung]:
    """Zeichnet die Ansichten mit den Zeichenfunktionen der Oberfläche in neue Figures.

    Parameters
    ----------
    daten : Messdaten
        Eingangsdaten.
    punkt_label : int, optional
        Label des Punkts für Ansicht 1 und 2; ``None`` = Mittel aller Punkte.
    frequenz_hz : float, optional
        Frequenz der Schwingform; Voreinstellung: Frequenz der höchsten Spitze des ersten
        Paars, ohne Referenz die Mitte der Achse.

    Returns
    -------
    dict
        ``spektrum``, ``frf`` (nur mit Referenz), ``spitzen``, ``schwingform`` und mit Referenz
        ``schwingform_phase``.
    """
    cache = PaarCache(daten)
    punkt = _punkt_index(daten, punkt_label)
    paare = kanalpaare(daten)
    ergebnis: dict[str, Zeichnung] = {}
    groesse: Groesse = (
        "kohaerent" if verfuegbare_groessen(daten)["kohaerent"] is None else "leistung"
    )
    sd = spektrum_daten(daten, cache, punkt=punkt, groesse=groesse)
    ergebnis["spektrum"] = zeichne_spektrum(
        neue_figure(THESIS_STIL, GROESSE_ZOLL), sd, SpektrumOptionen(), THESIS_STIL
    )
    band = gesamtband(daten.frequenz_hz)
    if paare:
        antwort, referenz = paare[0]
        fd = frf_daten(cache, antwort, referenz, punkt=punkt)
        ergebnis["frf"] = zeichne_frf(
            neue_figure(THESIS_STIL, GROESSE_ZOLL_HOCH), fd, FrfOptionen(), THESIS_STIL
        )
        pd = spitzen_daten_frf(cache, antwort, referenz, baender=band)
        if pd.spitzen:  # stärkste Spitze beschriften
            staerkste = max(range(len(pd.spitzen)), key=lambda n: pd.spitzen[n].hoehe)
            pd = spitzen_daten_frf(cache, antwort, referenz, baender=band, gewaehlt=staerkste)
    else:
        pd = spitzen_daten_spektrum(daten, cache, "Vib Z", baender=band)
    ergebnis["spitzen"] = zeichne_spitzen(
        neue_figure(THESIS_STIL, GROESSE_ZOLL_SPITZEN), pd, SpitzenOptionen(), THESIS_STIL
    )
    if frequenz_hz is None:
        if pd.spitzen:
            frequenz_hz = max(pd.spitzen, key=lambda s: s.hoehe).f_sp_hz
        else:
            frequenz_hz = float(daten.frequenz_hz[daten.anzahl_linien // 2])
    sf = schwingform_daten(daten, cache, frequenz_hz, komponente="3D")
    bild_zoll = bildgroesse_schwingform(sf, breite_cm=BREITE_SCHWINGFORM_CM)
    ergebnis["schwingform"] = zeichne_schwingform(
        neue_figure(THESIS_STIL, bild_zoll), sf, SchwingformOptionen(), THESIS_STIL
    )
    if paare:
        try:
            sp = schwingform_daten(daten, cache, frequenz_hz, komponente=KOMPONENTE_PHASE)
            ergebnis["schwingform_phase"] = zeichne_schwingform(
                neue_figure(THESIS_STIL, bild_zoll),
                sp,
                SchwingformOptionen(darstellung="phase_relativ"),
                THESIS_STIL,
            )
        except DarstellungsFehler:
            pass  # keine Phase verfügbar (keine Referenz): nur der Betrag
    return ergebnis


def schreibe_abbildungen(
    figuren: dict[str, Zeichnung],
    ausgabe: Path,
    *,
    messdatei: Path,
    format_: str = "png",
    dpi: int = 300,
) -> list[Path]:
    """Schreibt Bild und Herkunftsdatei (``.json``) je Abbildung.

    Parameters
    ----------
    figuren : dict
        Aus :func:`erzeuge_figuren`.
    ausgabe : pathlib.Path
        Zielordner (wird angelegt); vorhandene Dateien werden nicht überschrieben.
    messdatei : pathlib.Path
        Quelle der Daten (SHA-256 im Begleitfile).
    format_ : {"png", "pdf"}
        Bildformat.
    dpi : int
        Auflösung für PNG.

    Returns
    -------
    list of pathlib.Path
        Geschriebene Bilddateien.

    Raises
    ------
    FileExistsError
        Eine Zieldatei (Bild oder ``.json``) existiert bereits; geprüft wird vor dem ersten
        Schreiben, es entsteht keine Teilausgabe (Rohdaten und Ausgaben werden nie überschrieben).
    """
    if format_ not in ("png", "pdf"):
        raise ValueError(f"format_ muss png oder pdf sein: {format_!r}")
    info = ermittle_build_info()
    sha = sha256_datei(messdatei)
    bilder = {name: ausgabe / f"darstellung_{name}.{format_}" for name in figuren}
    for bild in bilder.values():  # alle Ziele vor dem ersten Schreiben prüfen: keine Teilausgabe
        for ziel in (bild, bild.with_suffix(".json")):
            if ziel.exists():
                raise FileExistsError(f"{ziel} existiert bereits; wird nicht überschrieben.")
    ausgabe.mkdir(parents=True, exist_ok=True)
    pfade: list[Path] = []
    for name, zeichnung in figuren.items():
        bild = bilder[name]
        begleit = bild.with_suffix(".json")
        fig: Figure = zeichnung.figure
        fig.savefig(bild, dpi=dpi if format_ == "png" else None)
        herkunft: dict[str, Any] = {
            "skript": SKRIPT,
            "abbildung": name,
            "messdatei": messdatei.name,
            "messdatei_sha256": sha,
            "software_git_hash": info.git_hash,
            "software_git_dirty": info.git_dirty,
            "linien": len(zeichnung.linien),
            "achsentitel": [(a.get_xlabel(), a.get_ylabel()) for a in zeichnung.achsen],
        }
        begleit.write_text(json.dumps(herkunft, ensure_ascii=False, indent=2), encoding="utf-8")
        pfade.append(bild)
    return pfade


def main(argv: Sequence[str] | None = None) -> int:
    """Kommandozeile: Messdatei lesen, Abbildungen schreiben."""
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0] if __doc__ else None)
    parser.add_argument("messdatei", type=Path, help="PSV-Messdatei (.svd)")
    parser.add_argument("--ausgabe", type=Path, required=True, help="Zielordner")
    parser.add_argument("--punkt-label", type=int, default=None, help="Punktlabel (sonst Mittel)")
    parser.add_argument("--frequenz-hz", type=float, default=None, help="Frequenz der Schwingform")
    parser.add_argument("--format", choices=("png", "pdf"), default="png")
    args = parser.parse_args(argv)
    daten = lade_svd(args.messdatei).messdaten
    figuren = erzeuge_figuren(daten, punkt_label=args.punkt_label, frequenz_hz=args.frequenz_hz)
    for pfad in schreibe_abbildungen(
        figuren, args.ausgabe, messdatei=args.messdatei, format_=args.format
    ):
        print(pfad)
    return 0


if __name__ == "__main__":
    sys.exit(main())
