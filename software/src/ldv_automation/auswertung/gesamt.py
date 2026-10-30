r"""Gesamtauswertung einer Messung nach FG-02 (Stufe 1).

:func:`werte_aus` führt für alle Kanalpaare mit Kreuzspektrum die Auswertungen 3.1 bis 3.5,
3.8 und 3.9 aus, bildet die Punktmittel (3.2), auf Wunsch eine Betriebsschwingform (3.6)
und die Plausibilitätsprüfungen P-01 bis P-11 (Abschnitt 4).

Festlegungen dieser Umsetzung (im Bericht W5-1 als Annahmen geführt):

- Die Spitzensuche läuft auf dem PSV-konformen Betragsmittel :math:`M^\mathrm{Betrag}` von
  |H1| mit dem arithmetischen Punktmittel von γ² als Kohärenz.
- Bandwerte werden je Punkt ``(P,)`` und für die Punktmittelkurve (Betragsmittel bzw.
  arithmetisches Mittel bei AP) gebildet.
- P-07 und P-09 laufen je Kanalpaar; P-08 nur für das konfigurierte Antriebspunkt-Paar.
"""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass

import numpy as np

from .annahmen import AnnahmeEintrag, Annahmen, Schwellen
from .baender import Bandwert, band_amplitude, band_ap, band_frf
from .daten import Messdaten, Paardaten, bereite_paar, einheit_quadrat
from .frf import FrfErgebnis, berechne_frf
from .mittel import Punktmittel, punktmittel_arithmetisch, punktmittel_betrag
from .plausibilitaet import (
    Antriebsart,
    Pruefergebnis,
    nicht_pruefbar,
    p05_kohaerenz,
    p07_phasensinn,
    p08_passivitaet,
    p09_referenzstabilitaet,
    p10_punktstatus,
    p11_annahmen,
    pruefe_eingang,
    sortiere,
)
from .schwingform import Quelle, Schwingform, betriebsschwingform
from .spektren import Spektren, spektren_kanal, spektren_paar, spektrum_leistung, staple_3d
from .spitzen import Spitzenergebnis, suche_spitzen

#: Komponentenreihenfolge der 3D-Größen (FG-02 2.5).
KOMPONENTEN_3D: tuple[str, str, str] = ("Vib X", "Vib Y", "Vib Z")


@dataclass(frozen=True, kw_only=True, eq=False)
class PaarAuswertung:
    """Auswertung eines Kanalpaars a/b.

    Attributes
    ----------
    paar : Paardaten
        Vorverarbeitete Eingangsgrößen.
    spektren : Spektren
        ``spektrum_kohaerent`` und ``spektrum_leistung`` der Antwort.
    frf : FrfErgebnis
        H1, H2, γ², Zufallsfehler, Maske, Gewichte.
    mittel_h1, mittel_h2 : Punktmittel
        Betrags- und quadratisches Mittel von |H1| bzw. |H2|.
    mittel_kohaerenz : Punktmittel
        Arithmetisches Mittel von γ².
    mittel_spektrum_kohaerent, mittel_spektrum_leistung : Punktmittel
        Punktmittel von |CPH| und √AP.
    spitzen : Spitzenergebnis
        Spitzen auf dem Betragsmittel von |H1|.
    """

    paar: Paardaten
    spektren: Spektren
    frf: FrfErgebnis
    mittel_h1: Punktmittel
    mittel_h2: Punktmittel
    mittel_kohaerenz: Punktmittel
    mittel_spektrum_kohaerent: Punktmittel
    mittel_spektrum_leistung: Punktmittel
    spitzen: Spitzenergebnis


@dataclass(frozen=True, kw_only=True, eq=False)
class Auswertung:
    """Gesamtergebnis einer Messung.

    Attributes
    ----------
    daten : Messdaten
        Eingangsdaten (roh).
    annahmen : Annahmen
        Verwendete Annahmen.
    schwellen : Schwellen
        Verwendete Schwellen.
    paare : dict
        Auswertung je Paar ``(a, b)``.
    kanaele : dict
        Spektren der Kanäle ohne Kreuzspektrum (nur √AP, FG-02 3.1 „ohne Referenz“).
    mittel_ap, mittel_betrag : dict
        Arithmetisches Punktmittel von AP bzw. Betragsmittel von ABS je Kanal.
    baender : tuple of Bandwert
        Bandwerte für die angeforderten Bänder.
    schwingform : Schwingform or None
        Betriebsschwingform, falls angefordert.
    pruefungen : tuple of Pruefergebnis
        P-01 bis P-11.
    annahmen_liste : tuple of AnnahmeEintrag
        Geltende Annahmen (P-11).
    """

    daten: Messdaten
    annahmen: Annahmen
    schwellen: Schwellen
    paare: dict[tuple[str, str], PaarAuswertung]
    kanaele: dict[str, Spektren]
    mittel_ap: dict[str, Punktmittel]
    mittel_betrag: dict[str, Punktmittel]
    baender: tuple[Bandwert, ...]
    schwingform: Schwingform | None
    pruefungen: tuple[Pruefergebnis, ...]
    annahmen_liste: tuple[AnnahmeEintrag, ...]


def werte_paar_aus(paar: Paardaten, schwellen: Schwellen, annahmen: Annahmen) -> PaarAuswertung:
    """Spektren, FRF, Punktmittel und Spitzensuche eines Paars."""
    frf = berechne_frf(paar, schwellen)
    name = paar.bezeichnung
    g = paar.gueltig
    m_h1 = punktmittel_betrag(
        frf.h1, g, groesse=f"|{frf.bezeichnung_h1}| {name}", einheit=frf.einheit, annahmen=annahmen
    )
    m_g2 = punktmittel_arithmetisch(
        frf.kohaerenz, g, groesse=f"γ² {name}", einheit="1", annahmen=annahmen
    )
    assert m_h1.mittel_betrag is not None and m_g2.mittel_arithmetisch is not None
    spitzen = suche_spitzen(
        paar.frequenz_hz,
        m_h1.mittel_betrag,
        kohaerenz=m_g2.mittel_arithmetisch,
        schwellen=schwellen,
        annahmen=annahmen,
        groesse=f"Betragsmittel |{frf.bezeichnung_h1}| {name}",
        einheit=frf.einheit,
    )
    return PaarAuswertung(
        paar=paar,
        spektren=spektren_paar(paar),
        frf=frf,
        mittel_h1=m_h1,
        mittel_h2=punktmittel_betrag(
            frf.h2, g, groesse=f"|H2| {name}", einheit=frf.einheit, annahmen=annahmen
        ),
        mittel_kohaerenz=m_g2,
        mittel_spektrum_kohaerent=punktmittel_betrag(
            paar.cph,
            g,
            groesse=f"spektrum_kohaerent {name}",
            einheit=paar.einheit_antwort,
            annahmen=annahmen,
        ),
        mittel_spektrum_leistung=punktmittel_betrag(
            spektrum_leistung(paar.ap_antwort),
            g,
            groesse=f"spektrum_leistung {paar.antwort}",
            einheit=paar.einheit_antwort,
            annahmen=annahmen,
        ),
        spitzen=spitzen,
    )


def _baender(
    daten: Messdaten,
    paare: dict[tuple[str, str], PaarAuswertung],
    mittel_ap: dict[str, Punktmittel],
    grenzen: Sequence[tuple[float, float]],
    annahmen: Annahmen,
) -> tuple[Bandwert, ...]:
    f = daten.frequenz_hz
    df = daten.delta_f_hz
    werte: list[Bandwert] = []
    for f_u, f_o in grenzen:
        for (a, b), pa in paare.items():
            name = f"{a}/{b}"
            assert pa.mittel_h1.mittel_betrag is not None
            assert pa.mittel_spektrum_kohaerent.mittel_betrag is not None
            for wert, bezug in (
                (pa.frf.h1, f"|{pa.frf.bezeichnung_h1}| {name} je Punkt"),
                (pa.mittel_h1.mittel_betrag, f"|{pa.frf.bezeichnung_h1}| {name} Betragsmittel"),
            ):
                werte.append(
                    band_frf(
                        wert,
                        f,
                        f_u,
                        f_o,
                        annahmen=annahmen,
                        delta_f_hz=df,
                        bezug=bezug,
                        einheit=pa.frf.einheit,
                    )
                )
            for wert, bezug in (
                (pa.paar.cph, f"spektrum_kohaerent {name} je Punkt"),
                (
                    pa.mittel_spektrum_kohaerent.mittel_betrag,
                    f"spektrum_kohaerent {name} Betragsmittel",
                ),
            ):
                werte.append(
                    band_amplitude(
                        wert,
                        f,
                        f_u,
                        f_o,
                        annahmen=annahmen,
                        delta_f_hz=df,
                        bezug=bezug,
                        einheit=pa.paar.einheit_antwort,
                    )
                )
        for kanal, ap in daten.ap.items():
            einheit = daten.einheiten[kanal]  # Kanaleinheit [a]; Art je Ausgabe im Bandwert
            m = mittel_ap[kanal].mittel_arithmetisch
            assert m is not None
            werte.append(
                band_ap(
                    ap,
                    f,
                    f_u,
                    f_o,
                    annahmen=annahmen,
                    delta_f_hz=df,
                    bezug=f"AP {kanal} je Punkt",
                    einheit=einheit,
                )
            )
            werte.append(
                band_ap(
                    m,
                    f,
                    f_u,
                    f_o,
                    annahmen=annahmen,
                    delta_f_hz=df,
                    bezug=f"AP {kanal} Punktmittel",
                    einheit=einheit,
                )
            )
        for kanal, betrag in daten.betrag.items():
            werte.append(
                band_amplitude(
                    betrag,
                    f,
                    f_u,
                    f_o,
                    annahmen=annahmen,
                    delta_f_hz=df,
                    bezug=f"ABS {kanal} je Punkt",
                    einheit=daten.einheiten[kanal],
                )
            )
    return tuple(werte)


def schwingform_aus(
    daten: Messdaten,
    f_wahl_hz: float,
    *,
    referenz: str = "Ref1",
    quelle: Quelle = "cph",
    komponenten: tuple[str, str, str] = KOMPONENTEN_3D,
    annahmen: Annahmen | None = None,
) -> Schwingform:
    """Betriebsschwingform der Komponenten X, Y, Z bei ``f_wahl_hz`` (FG-02 3.6).

    Mit gültiger Phase und vorhandenen Kreuzspektren aller Komponenten zur ``referenz``:
    komplexe Amplitude aus CPH (``quelle="cph"``) oder H1 (``quelle="h1"``), beide mit
    :math:`s_a s_b` und Konjugation. Sonst nur √AP mit ``phase_gueltig = False``.
    """
    annahmen = annahmen if annahmen is not None else Annahmen()
    fehlend = [c for c in komponenten if c not in daten.ap]
    if fehlend:
        raise ValueError(f"Schwingform: Komponenten {fehlend} fehlen in den Messdaten")
    f = daten.frequenz_hz
    mit_phase = daten.phase_gueltig and all((c, referenz) in daten.cp for c in komponenten)
    if mit_phase:
        paare = [bereite_paar(daten, c, referenz, annahmen) for c in komponenten]
        if quelle == "h1":
            felder = [berechne_frf(p).h1 for p in paare]
            einheit = paare[0].einheit_frf
        else:
            felder = [p.cph for p in paare]
            einheit = paare[0].einheit_antwort
        return betriebsschwingform(
            f,
            f_wahl_hz,
            amplitude_3d=staple_3d(*felder),
            phase_gueltig=True,
            quelle=quelle,
            referenz=referenz,
            einheit=einheit,
            delta_f_hz=daten.delta_f_hz,
            annahmen=annahmen,
        )
    leistung = staple_3d(*(spektrum_leistung(daten.ap[c]) for c in komponenten))
    return betriebsschwingform(
        f,
        f_wahl_hz,
        leistung_3d=leistung,
        phase_gueltig=False,
        einheit=daten.einheiten[komponenten[0]],
        delta_f_hz=daten.delta_f_hz,
        annahmen=annahmen,
    )


def werte_aus(
    daten: Messdaten,
    *,
    annahmen: Annahmen | None = None,
    schwellen: Schwellen | None = None,
    antriebspunkt: tuple[str, str, Antriebsart] | None = None,
    baender: Sequence[tuple[float, float]] = (),
    f_schwingform_hz: float | None = None,
    schwingform_referenz: str = "Ref1",
    schwingform_quelle: Quelle = "cph",
) -> Auswertung:
    """Wertet eine Messung nach FG-02 Stufe 1 aus.

    Parameters
    ----------
    daten : Messdaten
        Eingangsdaten.
    annahmen : Annahmen, optional
        M1–M11, Voreinstellungen aus FG-02.
    schwellen : Schwellen, optional
        Freigegebene Schwellen.
    antriebspunkt : tuple, optional
        ``(antwort, referenz, art)`` für P-08, z. B. ``("Ref2", "Ref1", "akzeleranz")``.
    baender : sequence of tuple of float
        Bandgrenzen ``(f_u, f_o)`` in Hz.
    f_schwingform_hz : float, optional
        Frequenz der Betriebsschwingform; ``None`` = keine.
    schwingform_referenz, schwingform_quelle
        Referenz und Quelle der Schwingform.

    Returns
    -------
    Auswertung
    """
    annahmen = annahmen if annahmen is not None else Annahmen()
    schwellen = schwellen if schwellen is not None else Schwellen()
    p = daten.anzahl_punkte
    gueltig = annahmen.gueltig_je_punkt(p)
    paare: dict[tuple[str, str], PaarAuswertung] = {}
    for a, b in daten.cp:
        paare[(a, b)] = werte_paar_aus(bereite_paar(daten, a, b, annahmen), schwellen, annahmen)
    mit_kreuzspektrum = {k for paar in daten.cp for k in paar}
    kanaele = {
        k: spektren_kanal(daten, k, annahmen) for k in daten.ap if k not in mit_kreuzspektrum
    }
    mittel_ap = {
        k: punktmittel_arithmetisch(
            v,
            gueltig,
            groesse=f"AP {k}",
            einheit=einheit_quadrat(daten.einheiten[k]),
            annahmen=annahmen,
        )
        for k, v in daten.ap.items()
    }
    mittel_betrag = {
        k: punktmittel_betrag(
            v, gueltig, groesse=f"ABS {k}", einheit=daten.einheiten[k], annahmen=annahmen
        )
        for k, v in daten.betrag.items()
    }
    pruefungen = pruefe_eingang(daten, schwellen, annahmen)
    for (a, b), pa in paare.items():
        name = f"{a}/{b}"
        pruefungen.append(p05_kohaerenz(pa.frf, schwellen))
        pruefungen.append(
            p07_phasensinn(daten.frequenz_hz, pa.frf.h1, pa.frf.kohaerenz, schwellen, gueltig, name)
        )
        pruefungen.append(
            p09_referenzstabilitaet(pa.paar.ap_referenz, pa.frf.kohaerenz, schwellen, gueltig, name)
        )
    if not paare:
        for pid in ("P-05", "P-07", "P-09"):
            pruefungen.append(nicht_pruefbar(pid, "keine Kreuzspektren (keine Referenz)"))
    if antriebspunkt is None:
        pruefungen.append(nicht_pruefbar("P-08", "kein Antriebspunkt-Paar konfiguriert"))
    else:
        a, b, art = antriebspunkt
        if (a, b) not in paare:
            raise ValueError(f"Antriebspunkt-Paar {a}/{b} hat kein Kreuzspektrum")
        frf = paare[(a, b)].frf
        pruefungen.append(
            p08_passivitaet(
                daten.frequenz_hz,
                frf.h1,
                frf.kohaerenz,
                art,
                schwellen,
                gueltig,
                f"{a}/{b} ({art})",
            )
        )
    pruefungen.append(p10_punktstatus(annahmen, p))
    pruefungen.append(p11_annahmen(annahmen))
    schwingform = (
        None
        if f_schwingform_hz is None
        else schwingform_aus(
            daten,
            f_schwingform_hz,
            referenz=schwingform_referenz,
            quelle=schwingform_quelle,
            annahmen=annahmen,
        )
    )
    return Auswertung(
        daten=daten,
        annahmen=annahmen,
        schwellen=schwellen,
        paare=paare,
        kanaele=kanaele,
        mittel_ap=mittel_ap,
        mittel_betrag=mittel_betrag,
        baender=_baender(daten, paare, mittel_ap, baender, annahmen),
        schwingform=schwingform,
        pruefungen=sortiere(pruefungen),
        annahmen_liste=annahmen.eintraege(),
    )


def hoechste_spitze(ergebnis: Spitzenergebnis) -> float | None:
    """Frequenz der höchsten Spitze in Hz oder ``None`` ohne Spitzen."""
    if not ergebnis.spitzen:
        return None
    hoehen = np.array([s.hoehe for s in ergebnis.spitzen])
    return ergebnis.spitzen[int(np.argmax(hoehen))].f_sp_hz
