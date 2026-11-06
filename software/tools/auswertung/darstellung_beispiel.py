"""Thesis-Abbildungen der vier Ansichten mit denselben Zeichenfunktionen (UI-18, P-ABB-S1).

Die Oberfläche (Reiter „Auswerten“) und dieses Skript rufen **dieselben** Zeichenfunktionen aus
:mod:`ldv_automation.darstellung` auf (``zeichne_spektrum``, ``zeichne_frf``, ``zeichne_spitzen``,
``zeichne_schwingform``). Das Skript nutzt :data:`~ldv_automation.darstellung.stil.THESIS_STIL`
(Graustufen, 9 pt), **keinen** Arbeitsstempel und keinen Diagrammtitel (KONVENTIONEN,
Abbildungsregeln). Aus denselben Daten entstehen deshalb dieselbe Linienzahl und dieselben
Achsenbeschriftungen wie in der Oberfläche. Es rechnet nichts Neues.

Anleitung: Abbildungen aus einer neuen ``.svd``
-----------------------------------------------
Aufruf (aus ``software/``; auf dem Messrechner mit dem Python der Umgebung, die das Paket
``ldv_automation`` enthält, und nicht unter ``PyCharmProject``)::

    uv run python tools/auswertung/darstellung_beispiel.py <messdatei.svd> --ausgabe <ordner> \
        [--antwort "Vib Z" --referenz Ref1] [--punkt-label N] [--frequenz-hz F] \
        [--komponente X|Y|Z] [--bezug-label N] [--format png|pdf|beide] [--erlaube-dirty]

Voreinstellungen: erstes Kanalpaar der Datei, Mittel aller Punkte, Frequenz der stärksten Spitze,
Phasenkomponente Z, Bezugspunkt = größtes |v| unter Punkten mit γ² ≥ γ²_min, Format ``beide``.
``--antwort`` und ``--referenz`` wählen das Kanalpaar (FRF und Spitzen);
``--komponente`` und ``--bezug-label`` betreffen nur ``schwingform_phase`` (die Phase der Komponente
gegen die Referenz wird relativ zum Bezugspunkt gezeigt, unabhängig von der offenen Annahme M8).
Die Schwingform (3D-Betrag und Phase) nutzt wie Ansicht 4 der Oberfläche die **erste Referenz mit
Kreuzspektren aller drei Vib-Kanäle** (sonst ``Ref1``), nicht die Referenz des gewählten Paars; das
Manifest nennt sie unter ``erzeugung.schwingform_referenz``.
Fehlt der Referenzkanal, entstehen ``spektrum``, ``spitzen`` und ``schwingform``; ``frf`` und
``schwingform_phase`` stehen dann mit Grund unter ``ausgelassen`` im Manifest.

Exit-Codes: **0** alles erzeugt (oder erwartungsgemäß ausgelassen); **2** Abbruch (unlesbare
Datei, unbekanntes Paar, Label oder Frequenz, Ausgabe unter ``Input`` oder ``PyCharmProject``,
vorhandene Zieldatei, Git-Regel: Vorprüfung, dabei entsteht **keine** Ausgabe; außerdem ein
Schreibfehler, siehe unten); **3** eine erwartete Phasenabbildung entfällt (z. B. Bezugspunkt nicht
darstellbar), die übrigen Abbildungen sind geschrieben. Fehler erscheinen als Klartext auf stderr,
ohne Traceback.

Schreibfehler (``Exception`` während des Schreibens, z. B. Datenträger voll oder ein Fehler beim
Speichern eines Bildes): Die Vorprüfung
garantiert nur, dass vor dem ersten Schreiben nichts Vorhandenes überschrieben wird. Bricht das
Schreiben ab, endet der Lauf mit Exit-Code 2 und einer Meldung ``Teilausgabe``, die die bereits
vollständig geschriebenen Dateien nennt und die gerade bearbeitete Datei als möglicherweise
unvollständig. Ein Manifest entsteht dann nicht; die Dateien sind zu löschen, bevor der Lauf
wiederholt wird (vorhandene Ziele werden nie überschrieben).

Repo-Wurzel: Liegt das Skript an seinem Platz (``<Repo>/software/tools/auswertung/``), ist
:data:`REPO_WURZEL` das Repo. Bei anderer (z. B. flacher) Ablage ist sie ``None`` (unbekannt); der
Import schlägt nie fehl. Dann entfallen die repo-bezogenen Prüfungen (Pfad unter ``<Repo>/Input``,
Warnung zum Arbeitsbaum). Die Sperre jeder Pfadkomponente ``Input`` und ``PyCharmProject`` gilt
unabhängig davon.

Ausgabe in ``<ordner>`` (Namensschema ``<Stem>_<abbildung>.<fmt>``, Stem = Name der Messdatei ohne
Endung): ``<Stem>_spektrum``, ``_frf``, ``_spitzen``, ``_schwingform``, ``_schwingform_phase`` als
``.png`` und/oder ``.pdf``, je Abbildung eine ``.json`` (Herkunft, Hinweise) und
``<Stem>_manifest.json`` (Aufruf, Messdatei mit SHA-256, Git-Hash und -Zustand, Parameter,
Annahmen mit Status, Zahl der M6-ungültigen Punkte und der Punkte mit γ² < γ²_min,
ausgelassene Abbildungen, Zeitstempel). Der Git-Hash steht nur in den Begleitdateien und in den
Bild-Metadaten, nicht sichtbar im Bild. Das PDF trägt kein Erstellungsdatum. Vorhandene Dateien
werden nie überschrieben; alle Ziele werden vor dem ersten Schreiben geprüft. Die Messdatei wird
nur gelesen. Endgültige Abbildungen für die Thesis gehören nach
``in_progress/thesis/abbildungen/<Stem>/``.

Git-Regel: Der Lauf bricht ab (Exit 2), wenn der Git-Hash fehlt (immer) oder ``git_dirty`` ``true``
bzw. unbekannt ist. ``--erlaube-dirty`` lässt den zweiten Fall zu (Warnung, Zustand im Manifest).
Liegt die Ausgabe im Git-Arbeitsbaum, meldet der nächste Lauf wegen der neuen, nicht
eingecheckten Bilder ``git_dirty = true``; Thesis-Abbildungen deshalb zuerst außerhalb des Repos
erzeugen und danach hineinkopieren, dann einchecken (Hinweis auf stderr).

Ansicht 3 beschriftet die stärkste Spitze (größte Kurvenhöhe). Ansicht 4 erscheint zweimal: als
3D-Betrag (``schwingform``) und, mit Referenz, als Phase der gewählten Komponente **relativ zum
Bezugspunkt** (``schwingform_phase``); beide im Hochformat 11,5 cm breit, die Höhe folgt aus dem
Seitenverhältnis der Punktwolke und sinkt nie so weit, dass der Punktabstand unter 12,5 pt fällt
(Pfeil 0,8·d ≥ 10 pt). M6-ungültige Punkte und Punkte mit γ² < γ²_min bleiben im Bild und sind
gekennzeichnet. Die Begleitdatei der Phasenabbildung nennt Linie (``f_hz``), Bezugspunkt,
γ²_min, Zahl unsicherer Punkte und die Kennzeichen der Spitze.
"""

from __future__ import annotations

import argparse
import json
import sys
from collections.abc import Sequence
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import numpy as np
from matplotlib.figure import Figure

from ldv_automation.auswertung.annahmen import Annahmen
from ldv_automation.auswertung.daten import Messdaten
from ldv_automation.auswertung.export import sha256_datei
from ldv_automation.auswertung.laden import LadeFehler, lade_svd
from ldv_automation.darstellung.auswahl import (
    DarstellungsFehler,
    Groesse,
    PaarCache,
    SchwingformDaten,
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
from ldv_automation.protokoll.version import BuildInfo, ermittle_build_info

SKRIPT = "software/tools/auswertung/darstellung_beispiel.py"
GROESSE_ZOLL = (4.9, 3.3)
"""Breite etwa 12,4 cm (Satzspiegel A5), damit Schrift und Linien im Druck lesbar bleiben."""
GROESSE_ZOLL_HOCH = (4.9, 4.4)
GROESSE_ZOLL_SPITZEN = (4.9, 3.8)
"""Höhe so, dass der Beschriftungsstreifen (drei Zeilen) die Kurve nicht staucht (Layout 3.1)."""
BREITE_SCHWINGFORM_CM = 11.5
"""Breite der Schwingform-Abbildungen; die Höhe folgt aus dem Datenaspekt (Hochformat, 4.2)."""
HOEHE_MAX_CM = 17.0
"""Obergrenze der Bildhöhe der Schwingform; sie wird überschritten, wenn der Datenaspekt es
braucht (d_pt ≥ :data:`D_PT_MIN`), statt die Punkte zu verkleinern."""
D_PT_MIN = 12.5
"""Kleinster Punktabstand d_NN im Bild in pt, bei dem der Pfeil (0,8·d) mindestens 10 pt misst."""
KOMPONENTE_PHASE = "Z"
"""Voreinstellung der Komponente der Phase relativ zum Bezugspunkt (Messrichtung des LDV)."""


def ermittle_repo_wurzel(skript: Path) -> Path | None:
    """Repo-Wurzel, wenn ``skript`` unter ``<Repo>/software/tools/auswertung/`` liegt, sonst None.

    Wirft nie (auch nicht bei flacher oder kurzer Pfadtiefe, z. B. auf dem Messrechner).
    """
    ordner = skript.resolve().parent
    if len(ordner.parents) >= 3 and ordner.parts[-3:] == ("software", "tools", "auswertung"):
        return ordner.parents[2]
    return None


REPO_WURZEL = ermittle_repo_wurzel(Path(__file__))
"""Wurzel des Repos, wenn das Skript an seinem Platz liegt; sonst ``None`` (unbekannt)."""
SPERR_ORDNER = ("pycharmproject",)
"""Pfadkomponenten (klein geschrieben), unter denen keine Ausgabe entstehen darf."""
FORMATE = ("png", "pdf", "beide")
EXIT_OK, EXIT_ABBRUCH, EXIT_ENTFALLEN = 0, 2, 3


class AbbruchFehler(Exception):  # noqa: N818  (fachlicher Name)
    """Eingabe-, Pfad- oder Git-Fehler: der Lauf endet mit Exit-Code 2, bevor etwas entsteht."""


class TeilausgabeFehler(OSError):  # noqa: N818  (fachlicher Name)
    """Schreibfehler mitten im Lauf: ein Teil der Ausgabe liegt schon im Ausgabeordner.

    Attributes
    ----------
    geschrieben : list of pathlib.Path
        Vollständig geschriebene Dateien (Bilder und Begleitdateien).
    unvollstaendig : pathlib.Path or None
        Datei, bei deren Schreiben der Fehler auftrat (kann unvollständig vorhanden sein).
    """

    def __init__(
        self, geschrieben: list[Path], unvollstaendig: Path | None, ursache: Exception
    ) -> None:
        self.geschrieben = geschrieben
        self.unvollstaendig = unvollstaendig
        liste = ", ".join(p.name for p in geschrieben) or "keine"
        offen = f" Möglicherweise unvollständig: {unvollstaendig.name}." if unvollstaendig else ""
        super().__init__(
            f"Teilausgabe: Schreiben fehlgeschlagen ({type(ursache).__name__}: {ursache}). "
            f"Bereits geschrieben: {liste}.{offen} "
            "Es gibt kein Manifest; die Dateien vor einem neuen Lauf löschen."
        )


def _labels_text(daten: Messdaten) -> str:
    """Verfügbare Punktlabels für Fehlermeldungen (die ersten zehn, sonst Bereich und Anzahl)."""
    labels = [int(w) for w in daten.punkte.label]
    zeigen = ", ".join(str(w) for w in labels[:10])
    mehr = (
        f", … ({len(labels)} Punkte, {min(labels)} bis {max(labels)})" if len(labels) > 10 else ""
    )
    return f"{zeigen}{mehr}"


def _punkt_index(
    daten: Messdaten, label: int | None, *, option: str = "--punkt-label"
) -> int | None:
    """0-basierter Punktindex zum Label (``None`` bleibt ``None``).

    Raises
    ------
    AbbruchFehler
        Das Label existiert nicht in der Datei; der Text nennt die vorhandenen Labels.
    """
    if label is None:
        return None
    treffer = [i for i, wert in enumerate(daten.punkte.label) if int(wert) == label]
    if not treffer:
        raise AbbruchFehler(
            f"{option} {label}: Punkt mit Label {label} existiert nicht in der Datei. "
            f"Vorhandene Labels: {_labels_text(daten)}."
        )
    return treffer[0]


def _waehle_paar(
    daten: Messdaten, antwort: str | None, referenz: str | None
) -> tuple[str, str] | None:
    """Kanalpaar (Antwort, Referenz): Voreinstellung erstes Paar der Datei, sonst die Wahl.

    Returns
    -------
    tuple or None
        ``None`` nur ohne Auswahl und ohne Kreuzspektrum in der Datei (FRF und Phase entfallen).

    Raises
    ------
    AbbruchFehler
        Zur Wahl gibt es kein Kreuzspektrum; der Text nennt die vorhandenen Paare.
    """
    paare = kanalpaare(daten)
    if antwort is None and referenz is None:
        return paare[0] if paare else None
    treffer = [
        p
        for p in paare
        if (antwort is None or p[0] == antwort) and (referenz is None or p[1] == referenz)
    ]
    if not treffer:
        vorhanden = ", ".join(f"{a}/{r}" for a, r in paare) or "keine (Datei ohne Kreuzspektren)"
        raise AbbruchFehler(
            f"Kein Kreuzspektrum für --antwort {antwort or '*'} --referenz {referenz or '*'}. "
            f"Vorhandene Paare (Antwort/Referenz): {vorhanden}."
        )
    return treffer[0]


def pruefe_ausgabe(ausgabe: Path) -> None:
    """Weist Ausgabeordner unter ``Input/`` und unter ``PyCharmProject`` ab.

    Abgelehnt wird ein Pfad, der unter ``<Repo>/Input`` liegt (nur bei bekannter Repo-Wurzel) oder
    eine Komponente ``Input`` bzw. ``PyCharmProject`` enthält (Groß-/Kleinschreibung egal,
    symbolische Links aufgelöst). Jeder Ordner namens ``Input`` ist gesperrt, auch außerhalb des
    Repos; nur unter ``<Repo>/Input`` handelt es sich nachweislich um die Rohdaten.

    Raises
    ------
    AbbruchFehler
        Der Ordner liegt in einem geschützten Bereich (Input, Projektordner des Messrechners).
    """
    ziel = ausgabe.resolve()
    teile = {t.lower() for t in ziel.parts}
    if teile & set(SPERR_ORDNER):
        raise AbbruchFehler(f"Ausgabe {ausgabe}: unter PyCharmProject wird nichts geschrieben.")
    if REPO_WURZEL is not None and ziel.is_relative_to((REPO_WURZEL / "Input").resolve()):
        raise AbbruchFehler(f"Ausgabe {ausgabe}: unter Input/ (Rohdaten) wird nichts geschrieben.")
    if "input" in teile:
        raise AbbruchFehler(
            f"Ausgabe {ausgabe}: Pfadkomponente „Input“ ist gesperrt (vorsorglich, "
            "Input/ enthält im Repo die Rohdaten); es wird nichts geschrieben. "
            "Anderen Ausgabeordner wählen."
        )


def pruefe_git(info: BuildInfo, *, erlaube_dirty: bool) -> list[str]:
    """Git-Regel (D2): Hash fehlt oder Zustand nicht sauber ergibt Abbruch.

    Parameters
    ----------
    info : BuildInfo
        Hash und Zustand der Software (``ermittle_build_info()``).
    erlaube_dirty : bool
        Lässt ``git_dirty`` ``True`` oder ``None`` zu; ein fehlender Hash bricht immer ab.

    Returns
    -------
    list of str
        Warnungen, wenn ``erlaube_dirty`` einen nicht sauberen Zustand zugelassen hat.

    Raises
    ------
    AbbruchFehler
        Kein Hash, oder ``git_dirty`` ist nicht ``False`` und ``erlaube_dirty`` fehlt.
    """
    if info.git_hash is None:
        raise AbbruchFehler(
            f"Kein Git-Hash der Software verfügbar ({info.grund}). Ohne Hash entstehen keine "
            "Abbildungen (auch nicht mit --erlaube-dirty)."
        )
    if info.git_dirty is False:
        return []
    zustand = "hat uncommittete Änderungen" if info.git_dirty else "Zustand unbekannt"
    if not erlaube_dirty:
        raise AbbruchFehler(
            f"Software-Stand {info.git_hash[:12]}: {zustand} "
            f"(git_dirty = {_json_bool(info.git_dirty)}, Quelle {info.quelle}). "
            "Änderungen einchecken oder --erlaube-dirty angeben."
        )
    return [
        f"WARNUNG: git_dirty = {_json_bool(info.git_dirty)} ({zustand}); die Abbildungen gehören "
        "zu keinem eindeutigen Software-Stand (--erlaube-dirty)."
    ]


def _json_bool(wert: bool | None) -> str:
    return "null" if wert is None else str(wert).lower()


def _im_arbeitsbaum(ausgabe: Path) -> bool:
    """Prüft, ob die Ausgabe im Git-Arbeitsbaum dieses Skripts liegt."""
    return (
        REPO_WURZEL is not None
        and (REPO_WURZEL / ".git").exists()
        and ausgabe.resolve().is_relative_to(REPO_WURZEL)
    )


def erzeuge_figuren(
    daten: Messdaten,
    *,
    punkt_label: int | None = None,
    frequenz_hz: float | None = None,
    fehlend: dict[str, str] | None = None,
    antwort: str | None = None,
    referenz: str | None = None,
    komponente: str = KOMPONENTE_PHASE,
    bezug_label: int | None = None,
    annahmen: Annahmen | None = None,
    info: dict[str, Any] | None = None,
) -> dict[str, Zeichnung]:
    """Zeichnet die Ansichten mit den Zeichenfunktionen der Oberfläche in neue Figures.

    Parameters
    ----------
    daten : Messdaten
        Eingangsdaten.
    punkt_label : int, optional
        Label des Punkts für Ansicht 1 und 2; ``None`` = Mittel aller Punkte.
    frequenz_hz : float, optional
        Frequenz der Schwingform; Voreinstellung: Frequenz der höchsten Spitze des gewählten
        Paars, ohne Referenz die Mitte der Achse.
    fehlend : dict, optional
        Wird mit ``{Abbildung: Grund}`` für jede Abbildung gefüllt, die nicht entsteht, obwohl sie
        erwartet wurde (Phase nicht darstellbar). Ohne Referenz entfällt die Phase ohne Eintrag.
    antwort, referenz : str, optional
        Kanalpaar für FRF und Spitzen; Voreinstellung: erstes Paar der Datei. Eine Angabe wählt das
        erste passende Paar. Die Schwingform nutzt davon unabhängig die Referenz der Oberfläche
        (erste Referenz mit Kreuzspektren aller Vib-Kanäle, sonst ``Ref1``).
    komponente : {"X", "Y", "Z"}
        Komponente der Phase relativ zum Bezugspunkt.
    bezug_label : int, optional
        Label des Bezugspunkts der Phase; ``None`` = größtes ``|v|`` unter Punkten mit
        ``γ² ≥ γ²_min``.
    annahmen : Annahmen, optional
        Annahmensatz (Voreinstellung FG-02); nur für Tests und Aufrufer, die M6 setzen.
    info : dict, optional
        Wird mit den Angaben für das Manifest gefüllt: ``antwort``, ``referenz``,
        ``schwingform_referenz``, ``punkt_label``, ``frequenz_gewaehlt_hz``,
        ``frequenz_linie_hz``, ``komponente_phase``,
        ``bezug_label_angefordert``, ``bezug_label_verwendet``, ``annahmen``, ``gamma2_min``,
        ``anzahl_m6_ungueltig``, ``anzahl_gamma2_unter_min`` (``None``, wenn die Phase nicht
        darstellbar ist; ohne M6-ungültige Punkte, wie im Bild), ``m6_hinweis`` und
        ``ausgelassen`` (alle fehlenden Abbildungen mit Grund, auch die erwarteten).

    Returns
    -------
    dict
        ``spektrum``, ``frf`` (nur mit Referenz), ``spitzen``, ``schwingform`` und mit Referenz
        ``schwingform_phase``.

    Raises
    ------
    AbbruchFehler
        Unbekanntes Label, Paar oder unzulässige Komponente.
    DarstellungsFehler
        Ansicht 1 bis 3 oder die 3D-Schwingform sind nicht darstellbar (z. B. Frequenz außerhalb
        der Achse). Die Phase meldet das über ``fehlend``.
    """
    if komponente not in ("X", "Y", "Z"):
        raise AbbruchFehler(f"--komponente muss X, Y oder Z sein: {komponente!r}")
    if info is None:
        info = {}
    ausgelassen: dict[str, str] = {}
    cache = PaarCache(daten, annahmen=annahmen)
    punkt = _punkt_index(daten, punkt_label)
    bezug = _punkt_index(daten, bezug_label, option="--bezug-label")
    paar = _waehle_paar(daten, antwort, referenz)
    ergebnis: dict[str, Zeichnung] = {}
    groesse: Groesse = (
        "kohaerent" if verfuegbare_groessen(daten)["kohaerent"] is None else "leistung"
    )
    sd = spektrum_daten(daten, cache, punkt=punkt, groesse=groesse)
    ergebnis["spektrum"] = zeichne_spektrum(
        neue_figure(THESIS_STIL, GROESSE_ZOLL), sd, SpektrumOptionen(), THESIS_STIL
    )
    band = gesamtband(daten.frequenz_hz)
    if paar is not None:
        antwort_kanal, referenz_kanal = paar
        fd = frf_daten(cache, antwort_kanal, referenz_kanal, punkt=punkt)
        ergebnis["frf"] = zeichne_frf(
            neue_figure(THESIS_STIL, GROESSE_ZOLL_HOCH), fd, FrfOptionen(), THESIS_STIL
        )
        pd = spitzen_daten_frf(cache, antwort_kanal, referenz_kanal, baender=band)
        if pd.spitzen:  # stärkste Spitze beschriften
            staerkste = max(range(len(pd.spitzen)), key=lambda n: pd.spitzen[n].hoehe)
            pd = spitzen_daten_frf(
                cache, antwort_kanal, referenz_kanal, baender=band, gewaehlt=staerkste
            )
    else:
        grund = "Kein Kreuzspektrum (Referenzkanal) in der Datei."
        ausgelassen["frf"] = ausgelassen["schwingform_phase"] = grund
        pd = spitzen_daten_spektrum(daten, cache, "Vib Z", baender=band)
    ergebnis["spitzen"] = zeichne_spitzen(
        neue_figure(THESIS_STIL, GROESSE_ZOLL_SPITZEN), pd, SpitzenOptionen(), THESIS_STIL
    )
    spitze = None
    gewaehlt_hz = frequenz_hz
    if frequenz_hz is None:
        if pd.spitzen:
            spitze = max(pd.spitzen, key=lambda s: s.hoehe)
            frequenz_hz = spitze.f_sp_hz
        else:
            frequenz_hz = float(daten.frequenz_hz[daten.anzahl_linien // 2])
    ref_kanal = paar[1] if paar is not None else None
    sf_referenz = _schwingform_referenz(daten)  # wie die Oberfläche, nicht die des Paars
    sf = schwingform_daten(daten, cache, frequenz_hz, komponente="3D", referenz=sf_referenz)
    if spitze is None and pd.spitzen:  # gewählte Frequenz: Spitze derselben Linie, falls vorhanden
        spitze = next(
            (s for s in pd.spitzen if abs(s.f_sp_hz - sf.f_hz) <= _halber_abstand(daten)), None
        )
    kennzeichen = tuple(spitze.kennzeichen) if spitze is not None else ()
    zeichnung, bild_zoll = _schwingform_hochformat(sf, SchwingformOptionen())
    ergebnis["schwingform"] = zeichnung
    anzahl_unter_min: int | None = None
    bezug_verwendet: int | None = None
    if paar is not None:
        try:
            sp = schwingform_daten(
                daten, cache, frequenz_hz, komponente=komponente, referenz=sf_referenz
            )
            phase = zeichne_schwingform(
                neue_figure(THESIS_STIL, bild_zoll),
                sp,
                SchwingformOptionen(
                    darstellung="phase_relativ", bezug=bezug, spitzen_kennzeichen=kennzeichen
                ),
                THESIS_STIL,
            )
        except DarstellungsFehler as fehler:  # keine Phase verfügbar: nur der Betrag, aber laut
            ausgelassen["schwingform_phase"] = str(fehler)
            if fehlend is not None:
                fehlend["schwingform_phase"] = str(fehler)
            print(f"Abbildung schwingform_phase entfällt: {fehler}", file=sys.stderr)
        else:
            anzahl_unter_min = phase.hilfsobjekte.get("anzahl_unsicher")
            bezug_verwendet = phase.hilfsobjekte.get("bezug_label")
            phase.hilfsobjekte["herkunft_zusatz"] = {
                "f_hz": sp.f_hz,
                "bezug_label": bezug_verwendet,
                "gamma2_min": sp.kohaerenz_min,
                "anzahl_unsicher": anzahl_unter_min,
                "kennzeichen": list(kennzeichen),
                "linien_text": phase.hilfsobjekte.get("linien_text"),
                "hinweise": list(phase.hinweise),
            }
            ergebnis["schwingform_phase"] = phase
    anzahl_ungueltig = int(np.sum(~cache.gueltig()))
    info.update(
        antwort=paar[0] if paar is not None else None,
        referenz=ref_kanal,
        schwingform_referenz=sf_referenz,
        punkt_label=punkt_label,
        frequenz_gewaehlt_hz=gewaehlt_hz,
        frequenz_linie_hz=sf.f_hz,
        komponente_phase=komponente,
        bezug_label_angefordert=bezug_label,
        bezug_label_verwendet=bezug_verwendet,
        annahmen=[
            {"nr": e.nr, "parameter": e.parameter, "wert": e.wert, "status": e.status}
            for e in cache.annahmen.eintraege()
        ],
        gamma2_min=cache.schwellen.kohaerenz_min,
        anzahl_m6_ungueltig=anzahl_ungueltig,
        anzahl_gamma2_unter_min=anzahl_unter_min,
        m6_hinweis=(
            "alle Punkte gültig (Annahme M6: Punktstatus der Datei nicht gedeutet)"
            if cache.annahmen.gueltig is None
            else f"M6 gesetzt: {anzahl_ungueltig} Punkte ungültig"
        ),
        ausgelassen=ausgelassen,
    )
    return ergebnis


def _schwingform_referenz(daten: Messdaten) -> str:
    """Referenz der Schwingform wie Ansicht 4 der Oberfläche (``_phase_referenz``).

    Erste Referenz (Dateireihenfolge) mit Kreuzspektren aller drei Vib-Kanäle, sonst ``Ref1``.
    """
    for referenz in dict.fromkeys(b for _a, b in daten.cp):
        if all((f"Vib {c}", referenz) in daten.cp for c in ("X", "Y", "Z")):
            return referenz
    return "Ref1"


def _halber_abstand(daten: Messdaten) -> float:
    """Halber Linienabstand in Hz (eine Spitze gehört zur Linie, wenn sie näher als das liegt)."""
    f = daten.frequenz_hz
    return 0.5 * float(f[1] - f[0]) if f.shape[0] > 1 else 0.0


def _schwingform_hochformat(
    sf: SchwingformDaten, opt: SchwingformOptionen
) -> tuple[Zeichnung, tuple[float, float]]:
    """Zeichnet die Schwingform im Hochformat; die Höhe folgt dem Datenaspekt.

    Die Höhe wird bei :data:`HOEHE_MAX_CM` begrenzt, aber nur so weit, dass der Punktabstand
    d_pt mindestens :data:`D_PT_MIN` bleibt. Sonst würde die Begrenzung die Punkte und Pfeile
    verkleinern (Pfeil 0,8·d_pt < 10 pt). Wird d_pt auch ohne Begrenzung nicht erreicht, steht
    der Hinweis des Zeichners in ``Zeichnung.hinweise``.

    Returns
    -------
    tuple
        Zeichnung und Bildgröße in Zoll (für weitere Abbildungen derselben Punkte).
    """
    hoehe_max = HOEHE_MAX_CM
    for _ in range(3):
        bild_zoll = bildgroesse_schwingform(
            sf, breite_cm=BREITE_SCHWINGFORM_CM, hoehe_max_cm=hoehe_max
        )
        zeichnung = zeichne_schwingform(neue_figure(THESIS_STIL, bild_zoll), sf, opt, THESIS_STIL)
        d_pt = float(zeichnung.hilfsobjekte["d_pt"])
        if d_pt >= D_PT_MIN:
            break
        hoehe_max *= 1.02 * D_PT_MIN / d_pt
    return zeichnung, bild_zoll


def schreibe_abbildungen(
    figuren: dict[str, Zeichnung],
    ausgabe: Path,
    *,
    messdatei: Path,
    format_: str = "png",
    dpi: int = 300,
    build_info: BuildInfo | None = None,
    lauf: dict[str, Any] | None = None,
) -> list[Path]:
    """Schreibt Bild, Herkunftsdatei (``.json``) je Abbildung und das Manifest.

    Dateinamen: ``<Stem>_<abbildung>.<fmt>``, ``<Stem>_<abbildung>.json`` und
    ``<Stem>_manifest.json`` (Stem = Name der Messdatei ohne Endung). Der Git-Hash steht in den
    Begleitdateien und in den Metadaten der Bilder; das PDF trägt kein Erstellungsdatum.

    Parameters
    ----------
    figuren : dict
        Aus :func:`erzeuge_figuren`.
    ausgabe : pathlib.Path
        Zielordner (wird angelegt); vorhandene Dateien werden nicht überschrieben.
    messdatei : pathlib.Path
        Quelle der Daten (SHA-256 in den Begleitdateien).
    format_ : {"png", "pdf", "beide"}
        Bildformat.
    dpi : int
        Auflösung für PNG.
    build_info : BuildInfo, optional
        Software-Stand; Voreinstellung ``ermittle_build_info()``.
        Die Git-Regel prüft :func:`pruefe_git`, nicht diese Funktion.
    lauf : dict, optional
        Angaben für das Manifest: ``aufruf``, ``parameter`` und die Schlüssel, die
        :func:`erzeuge_figuren` in ``info`` ablegt.

    Returns
    -------
    list of pathlib.Path
        Geschriebene Bilddateien (ohne ``.json``).

    Raises
    ------
    FileExistsError
        Eine Zieldatei (Bild, ``.json`` oder Manifest) existiert bereits; geprüft wird vor dem
        ersten Schreiben, dann entsteht nichts (Rohdaten und Ausgaben werden nie überschrieben).
    TeilausgabeFehler
        ``Exception`` (z. B. ``OSError`` oder ein Fehler beim Zeichnen des Bildes) während des
        Schreibens: ein Teil der Dateien liegt schon im Ordner, das Manifest fehlt; die Meldung
        nennt Typ und Text der Ursache, die geschriebenen Dateien und die möglicherweise
        unvollständige Datei. ``BaseException`` (z. B. ``KeyboardInterrupt``) wird nicht gefangen.
    """
    if format_ not in FORMATE:
        raise ValueError(f"format_ muss png, pdf oder beide sein: {format_!r}")
    formate = ("png", "pdf") if format_ == "beide" else (format_,)
    info = build_info if build_info is not None else ermittle_build_info()
    lauf = lauf if lauf is not None else {}
    sha = sha256_datei(messdatei)
    stem = messdatei.stem
    manifest_pfad = ausgabe / f"{stem}_manifest.json"
    ziele = {name: [ausgabe / f"{stem}_{name}.{fmt}" for fmt in formate] for name in figuren}
    begleit = {name: ausgabe / f"{stem}_{name}.json" for name in figuren}
    alle = [manifest_pfad, *begleit.values(), *(b for liste in ziele.values() for b in liste)]
    for ziel in alle:  # alle Ziele vor dem ersten Schreiben prüfen: keine Teilausgabe
        if ziel.exists():
            raise FileExistsError(f"{ziel} existiert bereits; wird nicht überschrieben.")
    beschreibung = (
        f"Messdatei-SHA-256 {sha}; Software-Git-Hash {info.git_hash or 'unbekannt'}; "
        f"git_dirty {_json_bool(info.git_dirty)}"
    )
    pfade: list[Path] = []
    geschrieben: list[Path] = []  # vollständig geschriebene Dateien (für die Meldung bei OSError)
    aktuell: Path | None = None  # Datei im Schreibvorgang
    abbildungen: dict[str, Any] = {}
    try:
        ausgabe.mkdir(parents=True, exist_ok=True)
        for name, zeichnung in figuren.items():
            fig: Figure = zeichnung.figure
            titel = f"{stem}_{name}"
            for bild in ziele[name]:
                aktuell = bild
                if bild.suffix == ".png":
                    meta: dict[str, Any] = {
                        "Title": titel,
                        "Software": SKRIPT,
                        "Description": beschreibung,
                    }
                    fig.savefig(bild, dpi=dpi, metadata=meta)
                else:  # PDF ohne CreationDate (reproduzierbar)
                    meta = {
                        "Title": titel,
                        "Creator": SKRIPT,
                        "Subject": beschreibung,
                        "CreationDate": None,
                    }
                    fig.savefig(bild, metadata=meta)
                geschrieben.append(bild)
                pfade.append(bild)
            herkunft: dict[str, Any] = {
                "skript": SKRIPT,
                "abbildung": name,
                "messdatei": messdatei.name,
                "messdatei_sha256": sha,
                "software_git_hash": info.git_hash,
                "software_git_dirty": info.git_dirty,
                "git_quelle": info.quelle,
                "paket_version": info.paket_version,
                "dateien": [b.name for b in ziele[name]],
                "linien": len(zeichnung.linien),
                "achsentitel": [(a.get_xlabel(), a.get_ylabel()) for a in zeichnung.achsen],
                "hinweise": list(zeichnung.hinweise),
            }
            herkunft.update(zeichnung.hilfsobjekte.get("herkunft_zusatz", {}))
            aktuell = begleit[name]
            begleit[name].write_text(
                json.dumps(herkunft, ensure_ascii=False, indent=2), encoding="utf-8"
            )
            geschrieben.append(begleit[name])
            abbildungen[name] = {
                "dateien": [b.name for b in ziele[name]],
                "begleitdatei": begleit[name].name,
                "linien": len(zeichnung.linien),
                "hinweise": list(zeichnung.hinweise),
            }
        manifest: dict[str, Any] = {
            "skript": SKRIPT,
            "aufruf": lauf.get("aufruf"),
            "erzeugt_utc": datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "messdatei": messdatei.name,
            "messdatei_groesse_bytes": messdatei.stat().st_size,
            "messdatei_sha256": sha,
            "software_git_hash": info.git_hash,
            "git_dirty": info.git_dirty,
            "git_quelle": info.quelle,
            "paket_version": info.paket_version,
            "parameter": lauf.get("parameter", {}),
            "erzeugung": {
                k: lauf.get(k)
                for k in (
                    "antwort",
                    "referenz",
                    "schwingform_referenz",
                    "punkt_label",
                    "frequenz_gewaehlt_hz",
                    "frequenz_linie_hz",
                    "komponente_phase",
                    "bezug_label_angefordert",
                    "bezug_label_verwendet",
                )
            },
            "annahmen": lauf.get("annahmen", []),
            "gamma2_min": lauf.get("gamma2_min"),
            "anzahl_m6_ungueltig": lauf.get("anzahl_m6_ungueltig"),
            "anzahl_gamma2_unter_min": lauf.get("anzahl_gamma2_unter_min"),
            "m6_hinweis": lauf.get("m6_hinweis"),
            "abbildungen": abbildungen,
            "ausgelassen": lauf.get("ausgelassen", {}),
        }
        aktuell = manifest_pfad
        manifest_pfad.write_text(
            json.dumps(manifest, ensure_ascii=False, indent=2, default=str), encoding="utf-8"
        )
    except Exception as fehler:  # BaseException (z. B. KeyboardInterrupt) bleibt unberührt
        raise TeilausgabeFehler(geschrieben, aktuell, fehler) from fehler
    return pfade


def _fuehre_aus(args: argparse.Namespace, argv: Sequence[str] | None) -> int:
    """Ein Lauf; Fehler der Eingabe werden als Ausnahme zur Meldung in :func:`main` gereicht."""
    ausgabe: Path = args.ausgabe
    pruefe_ausgabe(ausgabe)
    info = ermittle_build_info()
    for warnung in pruefe_git(info, erlaube_dirty=args.erlaube_dirty):
        print(warnung, file=sys.stderr)
    if _im_arbeitsbaum(ausgabe):
        print(
            "WARNUNG: Die Ausgabe liegt im Git-Arbeitsbaum; der nächste Lauf meldet wegen dieser "
            "Dateien git_dirty = true, bis sie eingecheckt sind. Thesis-Abbildungen zuerst "
            "außerhalb des Repos erzeugen und danach hineinkopieren.",
            file=sys.stderr,
        )
    daten = lade_svd(args.messdatei).messdaten
    fehlend: dict[str, str] = {}
    lauf: dict[str, Any] = {
        "aufruf": list(argv if argv is not None else sys.argv[1:]),
        "parameter": {
            "format": args.format,
            "dpi": 300,
            "erlaube_dirty": args.erlaube_dirty,
        },
    }
    figuren = erzeuge_figuren(
        daten,
        punkt_label=args.punkt_label,
        frequenz_hz=args.frequenz_hz,
        fehlend=fehlend,
        antwort=args.antwort,
        referenz=args.referenz,
        komponente=args.komponente,
        bezug_label=args.bezug_label,
        info=lauf,
    )
    pfade = schreibe_abbildungen(
        figuren,
        ausgabe,
        messdatei=args.messdatei,
        format_=args.format,
        build_info=info,
        lauf=lauf,
    )
    for pfad in pfade:
        print(pfad)
    print(ausgabe / f"{args.messdatei.stem}_manifest.json")
    return EXIT_ENTFALLEN if fehlend else EXIT_OK


def main(argv: Sequence[str] | None = None) -> int:
    """Kommandozeile: Messdatei lesen, Abbildungen schreiben.

    Returns
    -------
    int
        Exit-Code: 0 alles erzeugt, 2 Abbruch ohne Ausgabe, 3 eine erwartete Phasenabbildung
        entfällt (übrige geschrieben).
    """
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0] if __doc__ else None)
    parser.add_argument("messdatei", type=Path, help="PSV-Messdatei (.svd)")
    parser.add_argument("--ausgabe", type=Path, required=True, help="Zielordner")
    parser.add_argument("--antwort", default=None, help="Antwortkanal des Paars, z. B. 'Vib Z'")
    parser.add_argument("--referenz", default=None, help="Referenzkanal des Paars, z. B. Ref1")
    parser.add_argument("--punkt-label", type=int, default=None, help="Punktlabel (sonst Mittel)")
    parser.add_argument("--frequenz-hz", type=float, default=None, help="Frequenz der Schwingform")
    parser.add_argument(
        "--komponente",
        choices=("X", "Y", "Z"),
        default=KOMPONENTE_PHASE,
        help="Komponente der Phase",
    )
    parser.add_argument("--bezug-label", type=int, default=None, help="Bezugspunkt der Phase")
    parser.add_argument("--format", choices=FORMATE, default="beide")
    parser.add_argument(
        "--erlaube-dirty",
        action="store_true",
        help="Lauf trotz git_dirty true/unbekannt zulassen (fehlender Hash bricht immer ab)",
    )
    args = parser.parse_args(argv)
    try:
        return _fuehre_aus(args, argv)
    except (AbbruchFehler, LadeFehler, DarstellungsFehler, OSError) as fehler:  # inkl. Teilausgabe
        print(f"Fehler: {fehler}", file=sys.stderr)
        return EXIT_ABBRUCH


if __name__ == "__main__":
    sys.exit(main())
