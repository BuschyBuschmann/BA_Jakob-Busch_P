"""Gemeinsame Hilfen der Oberflächentests: Zustandsbild-Attrappen und Sitzungsattrappe."""

from __future__ import annotations

import dataclasses
import time
from collections.abc import Mapping
from pathlib import Path
from typing import Any
from uuid import UUID, uuid4

from ldv_automation.ablauf.steuerung import (
    DurchgangErgebnis,
    DurchgangZustand,
    Fehlerentscheidung,
    FortschrittStand,
)
from ldv_automation.ablauf.uhr import Testuhr
from ldv_automation.domaene import Eintrag, Messung, Pausenpunkt
from ldv_automation.geraet.schnittstelle import GeraeteInfo, GeraeteZustand, Messgeraet
from ldv_automation.geraet.simulator import DrehbuchEreignis, Simulator, SimulatorKonfiguration
from ldv_automation.protokoll.version import BuildInfo
from ldv_automation.sitzung import (
    Betriebsart,
    EintragBild,
    GeneratorStand,
    Sitzung,
    SitzungsEreignis,
    StartVorschau,
    Voraussetzung,
    Zustandsbild,
)

Z = DurchgangZustand
INFO = GeraeteInfo(
    psv_version="10.x-SIM",
    erfassungsmodus=True,
    meldungen_unterdrueckt=True,
    zustand=GeraeteZustand.GESTOPPT,
    hardware={"frontend": "SIM-FE"},
    lademaske="Acquisition|APS",
)
GIT = BuildInfo(paket_version="0.1.0", git_hash="c" * 40, git_dirty=False, quelle="test")


def eintrag(
    art: str = "messung",
    zustand: str = "wartend",
    *,
    name: str = "Platte_Mitte",
    text: str = "",
    **felder: Any,
) -> EintragBild:
    """Ein EintragBild mit sinnvollen Vorgaben."""
    werte: dict[str, Any] = {
        "art": art,
        "id": uuid4(),
        "name": name if art == "messung" else "",
        "text": text or ("Sensorkopf umsetzen" if art == "pausenpunkt" else ""),
        "einstellungsdatei": "C:/psv/platte.set" if art == "messung" else None,
        "parameter": {},
        "zeitlimit_s": None,
        "notiz": "",
        "zustand": zustand,
        "versuch": 1 if art == "messung" else None,
        "nummer": None,
        "fehlerart": None,
        "fehlertext": None,
        "zeit_start": None,
        "zeit_ende": None,
        "messdatei": None,
        "protokolldatei": None,
        "uebersprungen": False,
        "trockenlauf": False,
        "set_fehlt": False,
    }
    werte.update(felder)
    return EintragBild(**werte)


VORAUSSETZUNGEN_ERFUELLT = tuple(
    Voraussetzung(name=n, erfuellt=True, text=f"{n} ok")
    for n in (
        "verbindung",
        "geraet_gestoppt",
        "meldungen_unterdrueckt",
        "git_hash",
        "messdaten_wurzel",
        "trockenlauf",
    )
)


GENERATOR_AUS = GeneratorStand(generatoren_an=False, aktiv=False, amplitude_v=0.5, anzahl=1)
GENERATOR_AN = GeneratorStand(generatoren_an=True, aktiv=True, amplitude_v=0.5, anzahl=1)


def vorschau_zu(
    eintraege: Any,
    *,
    messpunkte: int | None = None,
    generator: GeneratorStand | None = None,
) -> tuple[StartVorschau, ...]:
    """Startvorschau wie die Sitzung sie für die wartenden Messungen liefert (Attrappe)."""
    wartend = [e for e in eintraege if e.art == "messung" and e.zustand == "wartend"]
    return tuple(
        StartVorschau(
            eintrag_id=e.id,
            nummer=n,
            name=e.name,
            einstellungsdatei=e.einstellungsdatei or "",
            zielpfad=f"/tmp/messdaten/<JJJJ-MM-TT_HHMMSS>_messen/{n:02d}_{e.name}.svd",
            messpunkte=messpunkte,
            generator=generator,
            hinweis="Attrappe",
        )
        for n, e in enumerate(wartend, start=1)
    )


def bild(**felder: Any) -> Zustandsbild:
    """Ein Zustandsbild (Attrappe) mit Vorgaben: BEREIT, SIMULATOR, verbunden, leer."""
    werte: dict[str, Any] = {
        "revision": 1,
        "durchgang": Z.BEREIT,
        "ergebnis": None,
        "betriebsart": Betriebsart.SIMULATOR,
        "verbindung": INFO,
        "eintraege": (),
        "fortschritt": None,
        "waechter_s": None,
        "fehlerentscheidung_offen": False,
        "fehlertext": None,
        "fehler_eintrag_id": None,
        "pausenpunkt_id": None,
        "durchgangsordner": None,
        "zusammenfassung": None,
        "messen_voraussetzungen": VORAUSSETZUNGEN_ERFUELLT,
        "fehlerstrategie": "PausierenUndNachfragen (vorläufig, O1)",
        "messdaten_wurzel": "/tmp/messdaten",
        "paket_version": "0.1.0",
        "git_hash": "c" * 40,
        "git_dirty": False,
        "interner_fehler": None,
        "zuruecksetzen_moeglich": False,
    }
    werte.update(felder)
    werte["eintraege"] = tuple(werte["eintraege"])
    _ableiten(werte, felder)
    return Zustandsbild(**werte)


def _einfuegen_ab(eintraege: tuple[EintragBild, ...]) -> int:
    anfang = 0
    for i, e in enumerate(eintraege):
        if e.zustand != "wartend":
            anfang = i + 1
    return anfang


def _ableiten(werte: dict[str, Any], gesetzt: Mapping[str, Any]) -> None:
    """Leitet Felder ab, die die echte Sitzung berechnet (wenn der Test sie nicht setzt)."""
    if "einfuegen_ab" not in gesetzt:
        werte["einfuegen_ab"] = _einfuegen_ab(werte["eintraege"])
    if "durchgangsname" not in gesetzt:
        werte["durchgangsname"] = werte["betriebsart"].value


def fortschritt(
    messung_id: UUID,
    anteil: float | None = 0.4,
    *,
    geschaetzt: bool = True,
    quelle: str = "zeitschaetzung",
    restzeit_s: float | None = 120.0,
    zeitlimit_rest_s: float = 461.0,
) -> FortschrittStand:
    """Ein FortschrittStand."""
    return FortschrittStand(
        messung_id=messung_id,
        anteil=anteil,
        geschaetzt=geschaetzt,
        quelle=quelle,
        restzeit_s=restzeit_s,
        zeitlimit_rest_s=zeitlimit_rest_s,
    )


def _als_bild(e: Eintrag) -> EintragBild:
    if isinstance(e, Messung):
        return eintrag(
            "messung",
            e.zustand.value,
            id=e.id,
            name=e.name,
            einstellungsdatei=e.einstellungsdatei,
            parameter=dict(e.parameter),
            zeitlimit_s=e.zeitlimit_s,
            notiz=e.notiz,
        )
    return eintrag("pausenpunkt", e.zustand.value, id=e.id, text=e.text)


class AttrappenSitzung:
    """Sitzungsattrappe: liefert ein einstellbares Zustandsbild und zeichnet Befehle auf.

    Warteschlangenbefehle ändern das Bild wie die Sitzung (nur wartende Einträge).
    """

    def __init__(self, anfang: Zustandsbild | None = None) -> None:
        self.bild = anfang or bild()
        self.befehle: list[tuple[Any, ...]] = []
        self.ereignisse: list[SitzungsEreignis] = []
        self.fehler: dict[str, Exception] = {}
        self.voraussetzungen = VORAUSSETZUNGEN_ERFUELLT
        self.ladeergebnis: tuple[EintragBild, ...] = ()
        self.ladewarnungen: tuple[str, ...] = ()
        self.letzter_start: tuple[Betriebsart | None, str | None] | None = None

    # Hilfen für Tests
    def setze(self, **felder: Any) -> Zustandsbild:
        """Ersetzt Felder des Bilds und erhöht die Revision."""
        felder.setdefault("revision", self.bild.revision + 1)
        if "eintraege" in felder:
            felder["eintraege"] = tuple(felder["eintraege"])
        werte = {f.name: getattr(self.bild, f.name) for f in dataclasses.fields(self.bild)}
        werte.update(felder)
        _ableiten(werte, felder)
        self.bild = Zustandsbild(**werte)
        return self.bild

    def _befehl(self, *befehl: Any) -> None:
        self.befehle.append(befehl)
        fehler = self.fehler.get(befehl[0])
        if fehler is not None:
            raise fehler

    def namen(self) -> list[str]:
        """Nur die Befehlsnamen in Reihenfolge."""
        return [b[0] for b in self.befehle]

    # SitzungsFassade
    def zustandsbild(self) -> Zustandsbild:
        return self.bild

    def hole_ereignisse(self) -> list[SitzungsEreignis]:
        e, self.ereignisse = self.ereignisse, []
        return e

    def _wartend(self, eintrag_id: UUID) -> int:
        for i, e in enumerate(self.bild.eintraege):
            if e.id == eintrag_id:
                if e.zustand != "wartend":
                    raise ValueError(f"Eintrag {eintrag_id} ist nicht wartend")
                return i
        raise KeyError(f"Unbekannte Eintrags-ID {eintrag_id}")

    def einfuegen(self, position: int, eintrag_: Eintrag) -> None:
        self._befehl("einfuegen", position, eintrag_)
        liste = list(self.bild.eintraege)
        if not 0 <= position <= len(liste):
            raise IndexError(f"Position {position} außerhalb")
        liste.insert(position, _als_bild(eintrag_))
        self.setze(eintraege=liste)

    def bearbeiten(self, eintrag_id: UUID, **aenderungen: object) -> Eintrag:
        self._befehl("bearbeiten", eintrag_id, aenderungen)
        i = self._wartend(eintrag_id)
        liste = list(self.bild.eintraege)
        liste[i] = dataclasses.replace(liste[i], **aenderungen)  # type: ignore[arg-type]
        self.setze(eintraege=liste)
        return Pausenpunkt(text="x")

    def entfernen(self, eintrag_id: UUID) -> Eintrag:
        self._befehl("entfernen", eintrag_id)
        i = self._wartend(eintrag_id)
        liste = list(self.bild.eintraege)
        del liste[i]
        self.setze(eintraege=liste)
        return Pausenpunkt(text="x")

    def verschieben(self, eintrag_id: UUID, neue_position: int) -> None:
        self._befehl("verschieben", eintrag_id, neue_position)
        i = self._wartend(eintrag_id)
        liste = list(self.bild.eintraege)
        e = liste.pop(i)
        liste.insert(neue_position, e)
        self.setze(eintraege=liste)

    def speichere_warteschlange(self, pfad: Path, *, ueberschreiben: bool = False) -> None:
        self._befehl("speichern", pfad, ueberschreiben)

    def lade_warteschlange(self, pfad: Path) -> tuple[str, ...]:
        self._befehl("laden", pfad)
        self.setze(eintraege=self.ladeergebnis)
        return self.ladewarnungen

    def setze_messdaten_wurzel(self, pfad: Path) -> None:
        self._befehl("wurzel", pfad)
        self.setze(messdaten_wurzel=str(pfad))

    def messen_voraussetzungen(self) -> tuple[Voraussetzung, ...]:
        return self.voraussetzungen

    def setze_betriebsart(self, neu: Betriebsart) -> None:
        self._befehl("betriebsart", neu)
        self.setze(betriebsart=neu)

    def verbinde(self) -> None:
        self._befehl("verbinde")

    def trenne(self) -> None:
        self._befehl("trenne")

    def starte(
        self,
        name: str,
        *,
        messen_bestaetigt: bool = False,
        erwartete_betriebsart: Betriebsart | None = None,
        erwartete_kennung: str | None = None,
    ) -> None:
        self.letzter_start = (erwartete_betriebsart, erwartete_kennung)
        self._befehl("starte", name, messen_bestaetigt)

    def setze_einstellungen(self, messdaten_wurzel: Path, standard_zeitlimit_s: float) -> None:
        self._befehl("einstellungen", messdaten_wurzel, standard_zeitlimit_s)
        self.setze(
            messdaten_wurzel=str(messdaten_wurzel), standard_zeitlimit_s=standard_zeitlimit_s
        )

    def setze_standard_zeitlimit(self, zeitlimit_s: float) -> None:
        self._befehl("zeitlimit", zeitlimit_s)
        self.setze(standard_zeitlimit_s=zeitlimit_s)

    def pausiere(self) -> None:
        self._befehl("pausiere")

    def setze_fort(self) -> None:
        self._befehl("setze_fort")

    def brich_ab(self) -> None:
        self._befehl("brich_ab")

    def bestaetige(self) -> None:
        self._befehl("bestaetige")

    def entscheide(self, entscheidung: Fehlerentscheidung) -> None:
        self._befehl("entscheide", entscheidung)

    def quittiere(self) -> None:
        self._befehl("quittiere")

    def zuruecksetzen(self) -> None:
        self._befehl("zuruecksetzen")
        neu = [
            dataclasses.replace(
                e,
                zustand="wartend",
                versuch=1 if e.art == "messung" else None,
                trockenlauf=False,
                uebersprungen=False,
            )
            for e in self.bild.eintraege
        ]
        self.setze(eintraege=neu, zuruecksetzen_moeglich=False)


class Fabrik:
    """Erzeugt Simulatoren je Betriebsart (Testuhr) und merkt sie sich."""

    def __init__(self, uhr: Testuhr, **sim: Any) -> None:
        self.uhr = uhr
        self.sim = sim
        self.erzeugt: list[Simulator] = []

    def __call__(self, art: Betriebsart) -> Messgeraet:
        geraet = Simulator(self.uhr.monotonic, betriebsart=art.value, **self.sim)
        self.erzeugt.append(geraet)
        return geraet


def echte_sitzung(
    tmp_path: Path,
    *,
    drehbuch: tuple[DrehbuchEreignis, ...] = (),
    konfiguration: SimulatorKonfiguration | None = None,
    verbinden: bool = True,
    **sitzung: Any,
) -> tuple[Sitzung, Fabrik, Testuhr]:
    """Echte Sitzung mit Simulator und Testuhr, ohne Threads (``verarbeite`` treibt sie)."""
    uhr = Testuhr()
    fabrik = Fabrik(uhr, drehbuch=drehbuch, konfiguration=konfiguration)
    wurzel = tmp_path / "daten"
    wurzel.mkdir(exist_ok=True)
    s = Sitzung(geraete_fabrik=fabrik, uhr=uhr, build_info=GIT, messdaten_wurzel=wurzel, **sitzung)
    s.verarbeite()
    if verbinden:
        s.verbinde()
        s.verarbeite()
    return s, fabrik, uhr


def set_datei(tmp_path: Path, name: str = "basis.set") -> str:
    """Legt eine Einstellungsdatei an und gibt den Pfad zurück."""
    pfad = tmp_path / name
    pfad.write_bytes(b"SET")
    return str(pfad)


def zusammenfassung(**zaehler: int) -> Mapping[str, int]:
    """Zusammenfassung wie in der Sitzung (Zustand -> Anzahl)."""
    return dict(zaehler)


def warte_bis(bedingung: Any, frist_s: float = 5.0) -> bool:
    """Wartet in Echtzeit, bis ``bedingung()`` wahr ist (nur für Thread-Tests)."""
    ende = time.monotonic() + frist_s
    while time.monotonic() < ende:
        if bedingung():
            return True
        time.sleep(0.005)
    return bool(bedingung())


__all__ = [
    "INFO",
    "VORAUSSETZUNGEN_ERFUELLT",
    "AttrappenSitzung",
    "DurchgangErgebnis",
    "Fabrik",
    "bild",
    "echte_sitzung",
    "eintrag",
    "fortschritt",
    "set_datei",
    "warte_bis",
    "zusammenfassung",
]
