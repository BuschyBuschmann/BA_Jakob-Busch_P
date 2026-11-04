"""Ansicht 2: H1/H2 und Kohärenz (eine Zeichenfunktion für Oberfläche und Thesis, P-AUSW T2).

Drei Teilbilder mit gemeinsamer Frequenzachse (Betrag 45 %, Phase 30 %, Kohärenz 25 %; ohne
Phase Betrag 65 %, Kohärenz 35 %). Die Phase steht in Grad (Rechnung in rad). Beim „Mittel“
gibt es keine Phase (Betragsmittel hat keine Phase): das Phasen-Teilbild zeigt dann einen
Platzhaltertext statt Daten. Ein übergebenes Kennzeichen (Oberfläche: „unbestätigt“, Annahme
M8) steht im Kopf des Phasen-Teilbilds.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from matplotlib import rc_context
from matplotlib.axes import Axes
from matplotlib.figure import Figure

from .auswahl import FrfDaten
from .formate import achsentitel, grad
from .stil import Plotstil
from .zeichnung import (
    Skala,
    Zeichnung,
    kennzeichen_anbringen,
    platzhalter_anbringen,
    setze_achsenstil,
)

__all__ = [
    "HINWEIS_PHASE_VORZEICHEN",
    "PLATZHALTER_PHASE_MITTEL",
    "FrfOptionen",
    "zeichne_frf",
]

HINWEIS_PHASE_VORZEICHEN = "positiv = {antwort} eilt {referenz} voraus"
"""Vorzeichenkonvention der Phase arg H1 (Zeitabhängigkeit e^{+iωt}); Text im Phasen-Teilbild."""

PLATZHALTER_PHASE_MITTEL = "Phase: für das Mittel nicht definiert (Betragsmittel hat keine Phase)"
"""Text im Phasen-Teilbild bei „Mittel“ (Nutzerentscheidung F-4b, RF-UI-F4b)."""

HOEHEN_MIT_PHASE = (45, 30, 25)
HOEHEN_OHNE_PHASE = (65, 35)


@dataclass(frozen=True, kw_only=True)
class FrfOptionen:
    """Darstellungsoptionen von Ansicht 2.

    Attributes
    ----------
    h1, h2 : bool
        Betragskurven einzeln einblendbar (mindestens eine).
    phase : bool
        Phasen-Teilbild (arg H1 = arg H2, FG-02 3.3).
    skala : {"linear", "log"}
        Betragsskala.
    kennzeichen_phase : str or None
        Kennzeichentext im Kopf des Phasen-Teilbilds (z. B. „unbestätigt (M8: …)“); ``None``
        = kein Kennzeichen. Die Zuordnung Annahme → Größe liegt in der Oberfläche.
    """

    h1: bool = True
    h2: bool = True
    phase: bool = False
    skala: Skala = "log"
    kennzeichen_phase: str | None = None

    def __post_init__(self) -> None:
        if not (self.h1 or self.h2):
            raise ValueError("Mindestens H1 oder H2 muss gewählt sein.")
        if self.skala not in ("linear", "log"):
            raise ValueError(f"unbekannte Skala {self.skala!r}")


def ohne_umbruch(phase_grad: np.ndarray) -> np.ndarray:
    """Fügt NaN an den ±180°-Umbrüchen ein, damit keine senkrechten Linien entstehen (Anzeige).

    Zwischen zwei Linien mit Sprung über 180° wird die Kurve unterbrochen; die Daten bleiben
    sonst unverändert. Die Länge ändert sich nicht: Je Sprung zwischen den Linien ``i`` und
    ``i + 1`` wird die **erste Probe nach dem Sprung** (Index ``i + 1``) auf NaN gesetzt; sie
    entfällt in der gezeichneten Linie (eine Probe je Umbruch), die Linie bricht davor ab und
    beginnt mit Probe ``i + 2`` neu. Nur die Anzeigekopie ist betroffen; ein Cursor liest aus
    ``FrfDaten.phase_rad`` (nicht aus den ydata der Linie), dort fehlt keine Probe.
    """
    ergebnis = np.array(phase_grad, dtype=np.float64, copy=True)
    sprung = np.flatnonzero(np.abs(np.diff(ergebnis)) > 180.0)
    ergebnis[sprung + 1] = np.nan
    return ergebnis


def zeichne_frf(fig: Figure, daten: FrfDaten, opt: FrfOptionen, stil: Plotstil) -> Zeichnung:
    """Zeichnet Betrag, optional Phase und Kohärenz in ``fig`` (ohne Titel, ohne Stempel).

    Parameters
    ----------
    fig : Figure
        Wird geleert und neu gefüllt.
    daten : FrfDaten
        Kurven aus :func:`~ldv_automation.darstellung.auswahl.frf_daten`.
    opt : FrfOptionen
        H1/H2, Phase, Skala, Kennzeichen.
    stil : Plotstil
        Farben, Linienarten, Schrift.

    Returns
    -------
    Zeichnung
        ``linien`` mit ``"H1"``, ``"H2"`` (je nach Wahl), ``"phase"`` (nur mit Phasendaten),
        ``"kohaerenz"``; ``achsen`` von oben nach unten.
    """
    hoehen = HOEHEN_MIT_PHASE if opt.phase else HOEHEN_OHNE_PHASE
    with rc_context(stil.rc()):
        fig.clear()
        fig.set_layout_engine("constrained")
        achsen = fig.subplots(
            len(hoehen), 1, sharex=True, gridspec_kw={"height_ratios": list(hoehen)}
        )
        achsen_liste: tuple[Axes, ...] = tuple(np.atleast_1d(achsen).tolist())
        z = Zeichnung(figure=fig, achsen=achsen_liste)
        f = daten.frequenz_hz
        ax_betrag = achsen_liste[0]
        zusatz = " (Betragsmittel)" if daten.ist_mittel else ""
        reihe = 0
        for schluessel, name, werte, aktiv in (
            ("H1", f"|{daten.bezeichnung_h1}|", daten.betrag_h1, opt.h1),
            ("H2", "|H2|", daten.betrag_h2, opt.h2),
        ):
            if not aktiv:
                continue
            (linie,) = ax_betrag.plot(
                f,
                werte,
                linestyle=stil.linienart(reihe),
                color=stil.serienfarbe(reihe),
                linewidth=stil.linienbreite_pt,
                label=name + zusatz,
            )
            z.linien[schluessel] = linie
            reihe += 1
        if opt.skala == "log":
            ax_betrag.set_yscale("log", nonpositive="mask")
        ax_betrag.set_ylabel(achsentitel("Betrag", daten.einheit))
        legende = ax_betrag.legend(loc="upper right", fontsize=stil.schrift_pt, framealpha=0.9)
        z.hilfsobjekte["legende"] = legende
        if opt.phase:
            ax_phase = achsen_liste[1]
            ax_phase.set_ylabel(achsentitel("Phase", "°"))
            ax_phase.set_ylim(-180.0, 180.0)
            ax_phase.set_yticks([-180, -90, 0, 90, 180])
            if daten.phase_rad is None:
                z.texte.append(platzhalter_anbringen(ax_phase, stil, PLATZHALTER_PHASE_MITTEL))
            else:
                (linie,) = ax_phase.plot(
                    f,
                    ohne_umbruch(grad(daten.phase_rad)),
                    linestyle=stil.linienart(0),
                    color=stil.haupt,
                    linewidth=stil.linienbreite_pt,
                    label=f"arg {daten.bezeichnung_h1}",
                )
                z.linien["phase"] = linie
                vorzeichen = HINWEIS_PHASE_VORZEICHEN.format(
                    antwort=daten.antwort, referenz=daten.referenz
                )
                z.texte.append(
                    ax_phase.text(
                        1.0,
                        1.0,
                        vorzeichen,
                        transform=ax_phase.transAxes,
                        ha="right",
                        va="bottom",
                        fontsize=stil.schrift_pt * 0.8,
                        color=stil.text_gedaempft,
                    )
                )
                z.hinweise = (*z.hinweise, f"Phase: {vorzeichen}")
                if opt.kennzeichen_phase is not None:
                    z.texte.append(kennzeichen_anbringen(ax_phase, stil, opt.kennzeichen_phase))
        ax_koh = achsen_liste[-1]
        (linie,) = ax_koh.plot(
            f,
            daten.kohaerenz,
            linestyle=stil.linienart(0),
            color=stil.haupt,
            linewidth=stil.linienbreite_pt,
            label="γ²",
        )
        z.linien["kohaerenz"] = linie
        ax_koh.set_ylim(0.0, 1.05)
        ax_koh.set_yticks([0.0, 0.5, 1.0])
        ax_koh.set_ylabel(achsentitel("Kohärenz", "1"))
        ax_koh.set_xlabel(achsentitel("Frequenz", "Hz"))
        ax_koh.set_xlim(float(f[0]), float(f[-1]))
        for ax in achsen_liste:
            setze_achsenstil(ax, stil)
    return z
