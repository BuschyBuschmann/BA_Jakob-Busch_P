"""Serien von Ansicht 5 „Diagramm“: Beschreibung und Auflösung zu Kurven (R-058/R-059, S6).

Eine **Serie** ist eine Linie im Diagramm: eine Messung, ein Punkt (über sein Label) oder das
Mittel, eine Komponente bzw. ein Kanalpaar und eine Größe. :class:`SerienSpec` beschreibt sie,
:func:`loese_serie_auf` macht daraus die Kurve. Es gibt **keine neue Mathematik**: Die Werte
kommen aus :func:`~ldv_automation.darstellung.auswahl.spektrum_daten` und
:func:`~ldv_automation.darstellung.auswahl.frf_daten` (Test: ``array_equal``); die Phase wird wie
in Ansicht 2 in Grad umgerechnet und an ±180°-Umbrüchen unterbrochen.

Jede Messung behält ihre eigene Frequenzachse (keine Interpolation, keine Differenz, UI-13).
Keine Qt-, keine ``pyplot``-Importe (ADR-021).
"""

from __future__ import annotations

from collections.abc import Callable, Mapping, Sequence
from dataclasses import dataclass, field
from typing import Literal

import numpy as np

from ldv_automation.auswertung.daten import FloatArray, Messdaten

from .auswahl import (
    DarstellungsFehler,
    Groesse,
    PaarCache,
    frf_daten,
    spektrum_daten,
)
from .formate import grad
from .frf import ohne_umbruch

__all__ = [
    "GROESSEN",
    "GROESSEN_NAMEN",
    "GRUND_ANDERE_EINHEIT",
    "GRUND_ANDERE_GROESSE",
    "GRUND_PHASE_MITTEL",
    "DiagrammDaten",
    "DiagrammSerie",
    "GroessenId",
    "MessungsZugriff",
    "SerienSpec",
    "betrag_groesse",
    "loese_alle_auf",
    "loese_serie_auf",
    "referenz_serie",
    "verfuegbare_diagramm_groessen",
]

GroessenId = Literal["spektrum", "h1", "h2", "kohaerenz", "phase"]
"""Größe einer Serie: Spektrum (Amplitude), |H1|, |H2|, Kohärenz γ², Phase."""

GROESSEN: tuple[GroessenId, ...] = ("spektrum", "h1", "h2", "kohaerenz", "phase")
"""Reihenfolge der Größen (Sortierung der Teilbilder, Reihenfolge der Auswahl)."""
GROESSEN_NAMEN: Mapping[GroessenId, str] = {
    "spektrum": "Spektrum (Amplitude)",
    "h1": "|H1|",
    "h2": "|H2|",
    "kohaerenz": "Kohärenz γ²",
    "phase": "Phase",
}
"""Anzeigename je Größe (Auswahl, Teilbildkopf, Kopfzeile)."""

GRUND_PHASE_MITTEL = "Phase beim Mittel nicht darstellbar (das Betragsmittel hat keine Phase)."
GRUND_ANDERE_GROESSE = "Überlagert nur eine Größe; weitere Größen über „nebeneinander“."
GRUND_ANDERE_EINHEIT = "Andere Einheit als die übrigen Serien ({einheit} statt {erste})."
GRUND_KEINE_REFERENZ_GROESSE = (
    "Keine Referenz in der Datei: {groesse} braucht ein Kreuzspektrum mit einer Referenz."
)


def betrag_groesse(groesse: GroessenId) -> bool:
    """Betragsgrößen (Spektrum, |H1|, |H2|): y-Achse mit wählbarer Skala (je Größe, E11)."""
    return groesse in ("spektrum", "h1", "h2")


@dataclass(frozen=True)
class SerienSpec:
    """Beschreibung einer Serie.

    Attributes
    ----------
    messung_id : int
        Kennung der Messung (stabil, Kurzname und Position ändern sich).
    punkt_label : int or None
        Label des Messpunkts (nicht der Index; Zuordnung zwischen Messungen über das Label);
        ``None`` = Mittel über die gültigen Punkte.
    groesse : GroessenId
        Dargestellte Größe.
    komponente : str or None
        ``"X"``, ``"Y"``, ``"Z"`` oder ``"3D"`` (nur ``groesse="spektrum"``).
    kanalpaar : tuple of str or None
        ``(Antwort, Referenz)`` (|H1|, |H2|, Kohärenz, Phase).
    teilgroesse : {"kohaerent", "leistung"}
        Spektrum als ``|CPH|`` (kohärent mit Referenz) oder ``√AP`` (nur ``"spektrum"``).
    slot : int
        Fester Platz 0 bis 3: bestimmt Linienart und Farbe, bleibt beim Entfernen einer anderen
        Serie unverändert (UI-18, UI-20).
    sichtbar : bool
        Unsichtbare Serien zählen für die Achsenwahl, werden aber weder gezeichnet noch in der
        Legende geführt (UI-21).
    """

    messung_id: int
    punkt_label: int | None
    groesse: GroessenId
    komponente: str | None = None
    kanalpaar: tuple[str, str] | None = None
    teilgroesse: Groesse = "kohaerent"
    slot: int = 0
    sichtbar: bool = True

    def schluessel(self) -> tuple[object, ...]:
        """Identität der Serie ohne Slot und Sichtbarkeit (Duplikatprüfung)."""
        return (
            self.messung_id,
            self.punkt_label,
            self.groesse,
            self.komponente,
            self.kanalpaar,
            self.teilgroesse if self.groesse == "spektrum" else None,
        )

    def aufloesung_schluessel(self) -> tuple[object, ...]:
        """Alles, was die Kurve bestimmt (ohne Slot und Sichtbarkeit); gleich = Kurve behalten."""
        return self.schluessel()


@dataclass(frozen=True, eq=False)
class DiagrammSerie:
    """Eine aufgelöste Serie: Kurve und Beschriftung.

    Attributes
    ----------
    spec : SerienSpec
        Beschreibung der Serie.
    kurzname, dateiname : str
        Kurzname und Dateiname der Messung.
    punkt_text : str
        ``"Punkt <Label>"`` oder ``"Mittel"``.
    komponenten_text : str
        Komponente (z. B. ``"Vib X"``) bzw. Kanalpaar (``"Vib X / Ref1"``).
    frequenz_hz, y : numpy.ndarray
        Eigene Frequenzachse der Messung und Kurve (Phase in Grad, mit NaN an den Umbrüchen).
    einheit : str
        Einheit der Größe (aus der Datei bzw. Quotient der Einheiten, ``"1"`` bei γ², ``"°"``).
    groesse_name : str
        Name der Größe für den Achsentitel (z. B. ``"Amplitude"``, ``"|H1|"``).
    mittelformel : str
        Beim Mittel „Betragsmittel |H1| über 135 Punkte“ (Formel und Punktzahl aus den Daten),
        sonst leer.
    punktzahl_text : str
        Punktzahl des Mittels (eine Zahl oder „min … max“), sonst leer.
    phase_unbestaetigt : bool
        Die Serie zeigt die Phase gegen die Referenz (Annahme M8 offen, solange die Oberfläche
        ein Kennzeichen übergibt).
    """

    spec: SerienSpec
    kurzname: str
    dateiname: str
    punkt_text: str
    komponenten_text: str
    frequenz_hz: FloatArray
    y: FloatArray
    einheit: str
    groesse_name: str
    mittelformel: str = ""
    punktzahl_text: str = ""
    phase_unbestaetigt: bool = False

    @property
    def slot(self) -> int:
        """Slot der Serie (Linienart und Farbe)."""
        return self.spec.slot

    @property
    def sichtbar(self) -> bool:
        """Serie wird gezeichnet."""
        return self.spec.sichtbar

    @property
    def groesse(self) -> GroessenId:
        """Größe der Serie."""
        return self.spec.groesse

    @property
    def legende(self) -> str:
        """Legendentext „<Kurzname> · <Punkt/Mittel> · <Komponente>“ (UI-11).

        Beim Mittel folgt in einer zweiten Zeile Mittelformel und Punktzahl.
        """
        zeile = f"{self.kurzname} · {self.punkt_text} · {self.komponenten_text}"
        return f"{zeile}\n{self.mittelformel}" if self.mittelformel else zeile


@dataclass(frozen=True, eq=False)
class DiagrammDaten:
    """Aufgelöste Serien eines Diagramms.

    Attributes
    ----------
    serien : tuple of DiagrammSerie
        Darstellbare Serien in Reihenfolge der Liste.
    nicht_darstellbar : tuple
        ``(Spec, Grund)`` der Serien, die nicht gezeichnet werden können (Meldung in AF).
    """

    serien: tuple[DiagrammSerie, ...]
    nicht_darstellbar: tuple[tuple[SerienSpec, str], ...] = field(default=())


MessungsZugriff = Callable[[int], "tuple[Messdaten, PaarCache, str, str] | None"]
"""``messung_id`` → ``(Messdaten, PaarCache, Kurzname, Dateiname)``, ``None`` = Messung fehlt."""


def verfuegbare_diagramm_groessen(daten: Messdaten) -> dict[GroessenId, str | None]:
    """Welche Größen eine Messung liefert (``None`` = möglich, sonst der Grund).

    Das Spektrum geht immer (``√AP`` braucht keine Referenz); |H1|, |H2|, Kohärenz und Phase
    brauchen ein Kreuzspektrum mit einer Referenz, die Phase zusätzlich eine gültige Phase.
    """
    ohne_ref = not daten.cp
    ergebnis: dict[GroessenId, str | None] = {"spektrum": None}
    for g in ("h1", "h2", "kohaerenz", "phase"):
        if ohne_ref:
            ergebnis[g] = GRUND_KEINE_REFERENZ_GROESSE.format(groesse=GROESSEN_NAMEN[g])
        elif g == "phase" and not daten.phase_gueltig:
            ergebnis[g] = "Die Phase ist in dieser Messung nicht gültig (keine Referenz/Trigger)."
        else:
            ergebnis[g] = None
    return ergebnis


def _punkt_index(daten: Messdaten, label: int | None, kurzname: str) -> int | None:
    if label is None:
        return None
    treffer = np.flatnonzero(daten.punkte.label == label)
    if treffer.size == 0:
        raise DarstellungsFehler(f"Punkt {label} gibt es in Messung {kurzname} nicht.")
    return int(treffer[0])


def loese_serie_auf(
    spec: SerienSpec, daten: Messdaten, cache: PaarCache, kurzname: str, dateiname: str = ""
) -> DiagrammSerie:
    """Löst eine Serie zu ihrer Kurve auf.

    Parameters
    ----------
    spec : SerienSpec
        Beschreibung.
    daten : Messdaten
        Daten der Messung ``spec.messung_id``.
    cache : PaarCache
        Paarauswertungen dieser Messung.
    kurzname, dateiname : str
        Beschriftung der Messung.

    Returns
    -------
    DiagrammSerie
        Kurve mit der Frequenzachse der Messung.

    Raises
    ------
    DarstellungsFehler
        Punkt, Komponente oder Kanalpaar gibt es nicht; keine Referenz; Phase beim Mittel.
    """
    punkt = _punkt_index(daten, spec.punkt_label, kurzname)
    punkt_text = "Mittel" if punkt is None else f"Punkt {spec.punkt_label}"
    if spec.groesse == "spektrum":
        if spec.komponente is None:
            raise DarstellungsFehler("Spektrum braucht eine Komponente (X, Y, Z oder 3D).")
        sd = spektrum_daten(
            daten,
            cache,
            punkt=punkt,
            komponenten=(spec.komponente,),
            groesse=spec.teilgroesse,
        )
        kurve = sd.kurven[0]
        formel = sd.mittelformel
        return DiagrammSerie(
            spec=spec,
            kurzname=kurzname,
            dateiname=dateiname,
            punkt_text=punkt_text,
            komponenten_text=kurve.beschriftung,
            frequenz_hz=sd.frequenz_hz,
            y=kurve.y,
            einheit=sd.einheit,
            groesse_name="Amplitude",
            mittelformel=formel,
            punktzahl_text=formel.rsplit(" über ", 1)[1].removesuffix(" Punkte") if formel else "",
        )
    if spec.kanalpaar is None:
        raise DarstellungsFehler(f"{GROESSEN_NAMEN[spec.groesse]} braucht ein Kanalpaar.")
    antwort, referenz = spec.kanalpaar
    fd = frf_daten(cache, antwort, referenz, punkt=punkt)
    paar_text = f"{antwort} / {referenz}"
    mittel = fd.ist_mittel
    formel = ""
    y: FloatArray
    if spec.groesse in ("h1", "h2"):
        y = fd.betrag_h1 if spec.groesse == "h1" else fd.betrag_h2
        name = f"|{fd.bezeichnung_h1}|" if spec.groesse == "h1" else "|H2|"
        einheit = fd.einheit
        if mittel:
            formel = f"Betragsmittel {name} über {fd.punktzahl_text} Punkte"
    elif spec.groesse == "kohaerenz":
        y, name, einheit = fd.kohaerenz, "Kohärenz γ²", "1"
        if mittel:
            formel = f"Arithmetisches Mittel γ² über {fd.punktzahl_text} Punkte"
    else:
        if fd.phase_rad is None:
            raise DarstellungsFehler(GRUND_PHASE_MITTEL)
        y, name, einheit = ohne_umbruch(grad(fd.phase_rad)), "Phase", "°"
    return DiagrammSerie(
        spec=spec,
        kurzname=kurzname,
        dateiname=dateiname,
        punkt_text=punkt_text,
        komponenten_text=paar_text,
        frequenz_hz=fd.frequenz_hz,
        y=y,
        einheit=einheit,
        groesse_name=name,
        mittelformel=formel,
        punktzahl_text=fd.punktzahl_text if mittel else "",
        phase_unbestaetigt=spec.groesse == "phase",
    )


def referenz_serie(serien: Sequence[DiagrammSerie]) -> DiagrammSerie:
    """Maßgebliche Serie eines Teilbilds: die erste sichtbare, sonst die erste (A-3).

    Raises
    ------
    ValueError
        Keine Serie.
    """
    if not serien:
        raise ValueError("Teilbild ohne Serie")
    return next((s for s in serien if s.sichtbar), serien[0])


def _pruefe_einheiten(
    serien: list[DiagrammSerie],
    anordnung: Literal["ueberlagert", "nebeneinander"],
    fehler: list[tuple[SerienSpec, str]],
) -> list[DiagrammSerie]:
    """Wendet A-3 je Teilbild an; abweichende Serien kommen mit Grund in ``fehler``."""
    if not serien:
        return serien
    gruppen: dict[object, list[DiagrammSerie]] = {}
    for serie in serien:
        schluessel: object = (
            0
            if anordnung == "ueberlagert"
            else (GROESSEN.index(serie.groesse), serie.spec.messung_id)
        )
        gruppen.setdefault(schluessel, []).append(serie)
    verworfen: set[int] = set()
    for inhalt in gruppen.values():
        erste = referenz_serie(inhalt)
        for serie in inhalt:
            if serie.groesse != erste.groesse:
                fehler.append((serie.spec, GRUND_ANDERE_GROESSE))
                verworfen.add(id(serie))
            elif serie.einheit != erste.einheit:
                fehler.append(
                    (
                        serie.spec,
                        GRUND_ANDERE_EINHEIT.format(einheit=serie.einheit, erste=erste.einheit),
                    )
                )
                verworfen.add(id(serie))
    return [s for s in serien if id(s) not in verworfen]


def loese_alle_auf(
    specs: Sequence[SerienSpec],
    zugriff: MessungsZugriff,
    *,
    anordnung: Literal["ueberlagert", "nebeneinander"] = "ueberlagert",
    bereits: Mapping[tuple[object, ...], DiagrammSerie] | None = None,
) -> DiagrammDaten:
    """Löst alle Serien auf; nicht darstellbare werden mit Grund gemeldet (kein Abbruch).

    Je Teilbild gilt **eine** Einheit (A-3), unabhängig von der Anordnung: Die erste *sichtbare*
    darstellbare Serie des Teilbilds bestimmt sie (gibt es keine sichtbare, die erste); abweichende
    Serien sind nicht darstellbar, mit Grund. Überlagert ist das ganze Diagramm ein Teilbild und
    zusätzlich gilt **eine** Größe; nebeneinander ist ein Teilbild eine Gruppe (Größe, Messung).

    Parameters
    ----------
    specs : sequence of SerienSpec
        Serien in Reihenfolge der Liste.
    zugriff : callable
        Liefert Daten, Cache und Namen einer Messung (``None`` = Messung gibt es nicht mehr).
    anordnung : {"ueberlagert", "nebeneinander"}
        Bestimmt, was ein Teilbild ist (alle Serien bzw. eine Gruppe aus Größe und Messung).
    bereits : mapping, optional
        Schon aufgelöste Serien nach :meth:`SerienSpec.aufloesung_schluessel`: sie werden
        wiederverwendet (nur ``slot`` und ``sichtbar`` kommen aus der neuen Spec).

    Returns
    -------
    DiagrammDaten
        Darstellbare Serien und die Gründe der übrigen.
    """
    serien: list[DiagrammSerie] = []
    fehler: list[tuple[SerienSpec, str]] = []
    for spec in specs:
        zugang = zugriff(spec.messung_id)
        if zugang is None:
            fehler.append((spec, "Die Messung dieser Serie ist nicht mehr geöffnet."))
            continue
        daten, cache, kurzname, dateiname = zugang
        alt = bereits.get(spec.aufloesung_schluessel()) if bereits is not None else None
        try:
            if alt is not None and alt.kurzname == kurzname:
                serie = DiagrammSerie(
                    **{
                        **{f: getattr(alt, f) for f in _FELDER_ALT},
                        "spec": spec,
                    }
                )
            else:
                serie = loese_serie_auf(spec, daten, cache, kurzname, dateiname)
        except DarstellungsFehler as grund:
            fehler.append((spec, str(grund)))
            continue
        serien.append(serie)
    serien = _pruefe_einheiten(serien, anordnung, fehler)
    return DiagrammDaten(serien=tuple(serien), nicht_darstellbar=tuple(fehler))


_FELDER_ALT = (
    "kurzname",
    "dateiname",
    "punkt_text",
    "komponenten_text",
    "frequenz_hz",
    "y",
    "einheit",
    "groesse_name",
    "mittelformel",
    "punktzahl_text",
    "phase_unbestaetigt",
)
