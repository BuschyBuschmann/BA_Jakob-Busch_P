"""Gelesener Gerätestand für die Bestätigung eines Durchgangs (Plan P2, 6; Brief P3, 3.9).

Der Dialog „Durchgang starten“ soll je Messung Messpunkte und den Generatorzustand zeigen.
Beides ist erst bekannt, nachdem PSV die Einstellungsdatei geladen hat (``Settings.Load``
übernimmt Scanpunkte und Generator aus der ``.set``). Die Steuerung merkt sich deshalb je
Einstellungsdatei, was sie nach dem Laden **gelesen** hat (Trockenlauf oder Messung in
dieser Sitzung), zusammen mit SHA-256, Größe und Änderungszeit der Datei. Ändert sich die
Datei, gilt das Wissen als veraltet und die Anzeige lautet „unbekannt“.

Zusätzlich hält die Steuerung den zuletzt gelesenen Stand des Geräts (beim Verbinden bzw.
nach dem letzten Laden), für den Dialog „Gerät“.

Herkunft (Korrekturen K-U5, K-U5b): Jedes Wissen trägt das Gerät, das es gelesen hat
(:class:`Herkunft`: laufende Nummer der Geräte-Erzeugung, Betriebsart, Lademaske,
PSV-Prozess). Es gilt für das aktuell verbundene Gerät, wenn

* es dasselbe Gerät ist, oder
* beide COM-Geräte sind (nie Simulator), mit gleichem PSV-Prozess-Treffer und gleicher
  Lademaske (:func:`uebertragbar`, Nutzerentscheidung K-U5b: Übernahme z. B. von
  TROCKENLAUF nach MESSEN).

Die ``.set`` muss in beiden Fällen unverändert sein (:func:`noch_gueltig`). Beim Trennen
und nach einem verlorenen Gerät verwirft die Steuerung das Wissen.

Es wird nichts geraten: Was nicht gelesen wurde, bleibt ``None`` und gilt als bedenklich
(:attr:`GeneratorStand.unbedenklich` ist dann ``False``).
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from datetime import datetime

from ldv_automation.geraet.schnittstelle import EinstellungsStand


@dataclass(frozen=True, kw_only=True)
class GeneratorStand:
    """Gelesener Generatorzustand (nur lesend erhoben).

    Parameters
    ----------
    generatoren_an : bool or None
        ``Acquisition.GeneratorsOn``; ``None``, wenn nicht gelesen (z. B. Simulator).
    aktiv : bool or None
        ``Generator.Active`` des ersten Generators; ``None``, wenn nicht lesbar.
    amplitude_v : float or None
        ``Generator.Amplitude`` in V; ``None``, wenn nicht lesbar.
    anzahl : int or None
        Anzahl der Generatoren laut PSV; ``None``, wenn nicht gelesen.
    """

    generatoren_an: bool | None
    aktiv: bool | None
    amplitude_v: float | None
    anzahl: int | None

    @property
    def unbedenklich(self) -> bool:
        """``True`` nur, wenn gelesen ist, dass kein Generator ausgibt.

        Bedingungen: Generator 1 ist ausdrücklich nicht aktiv, ``GeneratorsOn`` ist nicht
        ``True`` und es gibt höchstens einen Generator (der Adapter liest nur den ersten).
        Ein unbekanntes ``aktiv`` oder eine unbekannte Anzahl > 1 macht den Stand bedenklich.

        ``generatoren_an = None`` (nicht gemeldet) ist zulässig: Entscheidend ist ``aktiv``,
        weil ``ScanEx`` einen in der Einstellung aktiven Generator selbst startet ([HB] 8-3);
        ``GeneratorsOn`` ist nur ein zusätzlicher Hinweis. Der Simulator meldet ihn nicht;
        der COM-Adapter liest ihn immer mit, dort ist er also nie ``None``, wenn das Lesen
        gelang. Ist er ``True``, gilt der Stand als bedenklich.
        """
        return (
            self.aktiv is False
            and self.generatoren_an is not True
            and (self.anzahl is None or self.anzahl <= 1)
        )


def generator_aus_stand(stand: EinstellungsStand) -> GeneratorStand:
    """Liest den Generatorzustand aus der Gruppe ``generator`` eines Einstellungsstands.

    Verwendet werden nur die Rohwerte der Gruppe (``aktiv``, ``amplitude_v``,
    ``generatoren_an``, ``anzahl``), nicht das zusammengefasste
    :attr:`EinstellungsStand.generator_aktiv`: Dort wird ein unlesbares ``Active`` bei
    ``GeneratorsOn = False`` zu ``False`` (Adapter), das wäre geraten.
    """
    gruppe = stand.gruppen.get("generator", {})
    aktiv = gruppe.get("aktiv")
    an = gruppe.get("generatoren_an")
    amplitude = gruppe.get("amplitude_v")
    anzahl = gruppe.get("anzahl")
    return GeneratorStand(
        generatoren_an=an if isinstance(an, bool) else None,
        aktiv=aktiv if isinstance(aktiv, bool) else None,
        amplitude_v=(
            float(amplitude)
            if isinstance(amplitude, int | float) and not isinstance(amplitude, bool)
            else None
        ),
        anzahl=anzahl if isinstance(anzahl, int) and not isinstance(anzahl, bool) else None,
    )


@dataclass(frozen=True, kw_only=True)
class GeraeteStand:
    """Zuletzt gelesener Stand des Geräts (Messpunkte und Generator).

    Parameters
    ----------
    messpunkte : int or None
        ``Infos.MeasPoints.Count`` der geladenen Einstellung; ``None``, wenn unbekannt.
    generator : GeneratorStand
        Generatorzustand.
    quelle : str
        Wann gelesen, z. B. ``"beim Verbinden"`` oder ``"nach Laden von <Datei>"``.
    zeit : datetime
        Zeitpunkt des Lesens.
    fehler : str or None
        Grund, wenn das Lesen scheiterte (dann sind alle Werte unbekannt).
    """

    messpunkte: int | None
    generator: GeneratorStand
    quelle: str
    zeit: datetime
    fehler: str | None = None


UNBEKANNTER_GENERATOR = GeneratorStand(
    generatoren_an=None, aktiv=None, amplitude_v=None, anzahl=None
)
"""Generatorzustand, wenn nichts gelesen werden konnte."""


@dataclass(frozen=True, kw_only=True)
class DateiKennung:
    """Kennung einer Einstellungsdatei zum Zeitpunkt des Ladens.

    Parameters
    ----------
    sha256 : str
        SHA-256 des Inhalts (hex).
    groesse_b : int
        Größe in Byte.
    mtime_ns : int
        Änderungszeit in ns (``os.stat``).
    """

    sha256: str
    groesse_b: int
    mtime_ns: int


@dataclass(frozen=True, kw_only=True)
class Herkunft:
    """Woher gelesenes Wissen stammt.

    Parameters
    ----------
    geraet_nr : int
        Laufende Nummer der Geräte-Erzeugung in der Steuerung (jeder Tausch zählt hoch).
    betriebsart : str
        Betriebsart des Geräts.
    lademaske : str
        Lademaske des Geräts (``GeraeteInfo.lademaske``; leer beim Simulator).
    psv_prozesse : str or None
        Treffer der PSV-Prozessprüfung (``GeraeteInfo.hardware["psv_prozesse"]``, nur der
        COM-Adapter meldet ihn); ``None`` = kein COM-Gerät (Simulator).
    """

    geraet_nr: int
    betriebsart: str
    lademaske: str
    psv_prozesse: str | None = None


def uebertragbar(von: Herkunft, nach: Herkunft) -> bool:
    """Prüft, ob Wissen von Gerät ``von`` für Gerät ``nach`` gilt (ohne Dateiprüfung).

    Dasselbe Gerät immer; ein anderes nur COM -> COM mit gleichem, nicht leerem
    PSV-Prozess-Treffer und gleicher Lademaske. Simulatorwerte gelten nie für COM.
    """
    if von.geraet_nr == nach.geraet_nr:
        return von == nach
    return (
        bool(von.psv_prozesse)
        and von.psv_prozesse == nach.psv_prozesse
        and von.lademaske == nach.lademaske
    )


@dataclass(frozen=True, kw_only=True)
class EinstellungsKenntnis:
    """Was nach dem Laden einer Einstellungsdatei gelesen wurde.

    Parameters
    ----------
    einstellungsdatei : str
        Pfad wie in der Messung angegeben.
    kennung : DateiKennung
        Kennung der Datei beim Laden.
    stand : GeraeteStand
        Nach dem Laden gelesener Stand.
    herkunft : Herkunft
        Gerät, das den Stand gelesen hat.
    """

    einstellungsdatei: str
    kennung: DateiKennung
    stand: GeraeteStand
    herkunft: Herkunft


def pfad_schluessel(pfad: str) -> str:
    """Vergleichsschlüssel eines Pfads (absolut, normalisiert, Groß/Klein nach Plattform)."""
    return os.path.normcase(os.path.abspath(pfad))


def noch_gueltig(kenntnis: EinstellungsKenntnis) -> bool:
    """Prüft billig (ohne Hash), ob die Datei seit dem Laden unverändert scheint.

    Verglichen werden Größe und Änderungszeit. Fehlt die Datei oder ist sie nicht lesbar,
    gilt die Kenntnis als ungültig.
    """
    try:
        st = os.stat(kenntnis.einstellungsdatei)
    except OSError:
        return False
    return st.st_size == kenntnis.kennung.groesse_b and st.st_mtime_ns == kenntnis.kennung.mtime_ns
