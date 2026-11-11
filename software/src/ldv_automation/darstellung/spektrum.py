"""Ansicht 1: Spektrum (eine Zeichenfunktion für Oberfläche und Thesis, P-AUSW T2).

Eine Kurve je gewählter Komponente (X, Y, Z, 3D), Linienart je Kurve paarweise verschieden,
Legende mit Linienprobe und der Größe als Legendentitel („Geschwindigkeit, kohärent mit Ref1“
bzw. „Leistungsmittel √AP, mit Rauschen, ohne Phase“). Skala logarithmisch voreingestellt;
„dB“ gibt es nicht, weil die Datei keine Referenzgröße (0 dB) enthält.
"""

from __future__ import annotations

from dataclasses import dataclass

from matplotlib import rc_context
from matplotlib.figure import Figure

from .achsen import AchsenOptionen, nebenticks_log, wende_frequenz_an, wende_y_an
from .auswahl import SpektrumDaten
from .formate import achsentitel
from .stil import Plotstil
from .zeichnung import Skala, Zeichnung, constrained_layout, setze_achsenstil

__all__ = ["DB_GRUND", "SpektrumOptionen", "zeichne_spektrum"]

DB_GRUND = "keine Referenzgröße (0 dB) in der Datei"
"""Grund, aus dem „dB“ deaktiviert ist (Nutzerentscheidung, Annahme N-2)."""


@dataclass(frozen=True, kw_only=True)
class SpektrumOptionen:
    """Darstellungsoptionen von Ansicht 1.

    Attributes
    ----------
    skala : {"linear", "log"}
        Amplitudenskala (Voreinstellung logarithmisch, OE-2). ``"db"`` ist nicht möglich
        (:data:`DB_GRUND`).
    achsen : AchsenOptionen or None
        Feste Bereiche und Frequenzskala (R-073, Rolle ``"betrag"``); ``None`` (Voreinstellung)
        lässt die Achsen unverändert (Frequenz = Datenbereich, y automatisch).
    """

    skala: Skala = "log"
    achsen: AchsenOptionen | None = None

    def __post_init__(self) -> None:
        if self.skala == "db":  # type: ignore[comparison-overlap]
            raise ValueError(f"dB ist nicht verfügbar: {DB_GRUND}")
        if self.skala not in ("linear", "log"):
            raise ValueError(f"unbekannte Skala {self.skala!r}")


def zeichne_spektrum(
    fig: Figure, daten: SpektrumDaten, opt: SpektrumOptionen, stil: Plotstil
) -> Zeichnung:
    """Zeichnet das Spektrum der Auswahl in ``fig`` (ohne Diagrammtitel, ohne Stempel).

    Parameters
    ----------
    fig : Figure
        Wird geleert und neu gefüllt.
    daten : SpektrumDaten
        Kurven aus :func:`~ldv_automation.darstellung.auswahl.spektrum_daten`.
    opt : SpektrumOptionen
        Skala.
    stil : Plotstil
        Farben, Linienarten, Schrift.

    Returns
    -------
    Zeichnung
        ``linien`` je Komponentenschlüssel; ``achsen`` mit einer Achse.
    """
    with rc_context(stil.rc()):
        fig.clear()
        constrained_layout(fig)
        ax = fig.subplots()
        zeichnung = Zeichnung(figure=fig, achsen=(ax,), hinweise=daten.hinweise, rollen=("betrag",))
        for i, kurve in enumerate(daten.kurven):
            (linie,) = ax.plot(
                daten.frequenz_hz,
                kurve.y,
                linestyle=stil.linienart(i),
                color=stil.serienfarbe(i),
                linewidth=stil.linienbreite_pt,
                label=kurve.beschriftung,
            )
            zeichnung.linien[kurve.schluessel] = linie
        if opt.skala == "log":
            ax.set_yscale("log", nonpositive="mask")
        f_min, f_max = float(daten.frequenz_hz[0]), float(daten.frequenz_hz[-1])
        if opt.achsen is None:
            ax.set_xlim(f_min, f_max)
        else:
            x_fest = wende_frequenz_an(ax, opt.achsen, f_min, f_max)
            wende_y_an(
                ax,
                opt.achsen.y_bereich("betrag"),
                log=opt.skala == "log",
                x_gesetzt=x_fest,
                name="Amplitude",
            )
        ax.set_xlabel(achsentitel("Frequenz", "Hz"))
        ax.set_ylabel(achsentitel("Amplitude", daten.einheit))
        setze_achsenstil(ax, stil)
        if opt.achsen is not None:
            nebenticks_log(ax, dezimalkomma=stil.dezimalkomma)
        titel = daten.bezeichnung
        if daten.mittelformel:  # Mittelformel und Punktzahl im Bild (KONVENTIONEN)
            titel += f"\n{daten.mittelformel}"
        legende = ax.legend(
            title=titel, loc="upper right", fontsize=stil.schrift_pt, framealpha=0.9
        )
        legende.get_title().set_fontsize(stil.schrift_pt)
        zeichnung.hilfsobjekte["legende"] = legende
    return zeichnung
