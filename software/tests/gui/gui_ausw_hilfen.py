"""Hilfen der Tests des Reiters „Auswerten“: synthetische Datei und Ausführer-Attrappen."""

from __future__ import annotations

from collections.abc import Callable
from pathlib import Path
from typing import Any

import numpy as np

from ldv_automation.auswertung.annahmen import Annahmen
from ldv_automation.auswertung.daten import Herkunft, Messdaten, Punkte
from ldv_automation.auswertung.jobs import PruefErgebnis
from ldv_automation.auswertung.laden import Dateieinstellungen, Geladen, referenzen_aus
from ldv_automation.auswertung.plausibilitaet import Pruefergebnis
from ldv_automation.auswertung.svd_lesen import Mittelung
from ldv_automation.hintergrund import (
    Auftrag,
    AuftragAbgebrochen,
    AuftragFehler,
    DirektAusfuehrer,
)

P = 4
K = 64
DF_HZ = 0.5
SHA = "a" * 64
PFAD = "C:\\messungen\\probe.svd"


def synth_geladen(
    *, referenz: bool = True, mit_ref2: bool = False, resonanz: bool = True, pfad: str = PFAD
) -> Geladen:
    """Kleine Datei: 4 Punkte, 64 Linien (Δf 0,5 Hz), Vib X/Y/Z, optional Ref1 (N), Ref2 (m/s²)."""
    f = DF_HZ * np.arange(1, K + 1, dtype=np.float64)
    h0 = (
        1.0 / (1.0 + 1j * (f - 16.0) / 2.0)
        if resonanz
        else 1.0 / (1.0 + 0.05 * f).astype(np.complex128)
    )
    form = {"Vib X": 0.3, "Vib Y": 0.5, "Vib Z": 1.0}
    ap: dict[str, Any] = {}
    cp: dict[tuple[str, str], Any] = {}
    for kanal, faktor in form.items():
        h = faktor * np.linspace(1.0, 0.4, P)[:, None] * h0[None, :]
        ap[kanal] = (np.abs(h) ** 2 + 1e-12).astype(np.float64)
        if referenz:
            cp[(kanal, "Ref1")] = h.astype(np.complex128)
    einheiten = {"Vib X": "m/s", "Vib Y": "m/s", "Vib Z": "m/s"}
    if referenz:
        ap["Ref1"] = np.full((P, K), 1.0 + 1e-4)
        einheiten["Ref1"] = "N"
        if mit_ref2:
            ap["Ref2"] = (np.abs(h0) ** 2)[None, :] * np.ones((P, 1))
            cp[("Ref2", "Ref1")] = (h0[None, :] * np.ones((P, 1))).astype(np.complex128)
            einheiten["Ref2"] = "m/s²"
    daten = Messdaten(
        frequenz_hz=f,
        delta_f_hz=DF_HZ,
        punkte=Punkte(
            index=np.arange(P, dtype=np.int64),
            label=np.arange(10, 10 + P, dtype=np.int64),
            koordinaten_m=np.column_stack(
                [np.linspace(0.0, 0.3, P), np.linspace(0.0, 0.1, P), np.zeros(P)]
            ),
        ),
        einheiten=einheiten,
        ap=ap,
        cp=cp,
        phase_gueltig=referenz,
        herkunft=Herkunft(pfad=pfad, sha256=SHA, dateizeit=None, programmversion=None),
    )
    einstellungen = Dateieinstellungen(
        bandbreite_hz=K * DF_HZ,
        linien=K,
        delta_f_hz=DF_HZ,
        abtastfrequenz_hz=2.56 * K * DF_HZ,
        mittelung=Mittelung(typ=2, anzahl=7),
        punkte=P,
        referenzen=referenzen_aus(daten),
    )
    return Geladen(messdaten=daten, einstellungen=einstellungen)


def synth_pruefung() -> PruefErgebnis:
    """Ergebnis von Stufe B: zwei Prüfungen (ok, Warnung) und die Annahmen mit Voreinstellung."""
    return PruefErgebnis(
        pruefungen=(
            Pruefergebnis(id="P-01", titel="a", status="ok", wert=None, grund="g"),
            Pruefergebnis(id="P-02", titel="b", status="warnung", wert=None, grund="g"),
        ),
        annahmen=tuple(Annahmen().eintraege()),
        sha256=SHA,
    )


class Protokoll:
    """Merkt die Aufrufe der Aufträge ``lese`` und ``pruef`` (Argumente und Reihenfolge)."""

    def __init__(self) -> None:
        self.lese: list[str] = []
        self.pruef: list[tuple[Any, ...]] = []
        self.fehler_lese: dict[str, str] = {}
        self.geladen: dict[str, Geladen] = {}
        self.pruef_fehler: str | None = None
        self.export: list[tuple[Any, ...]] = []
        self.export_fehler: str | None = None

    def lese_job(self, pfad: str) -> Geladen:
        self.lese.append(pfad)
        if pfad in self.fehler_lese:
            raise ValueError(self.fehler_lese[pfad])
        return self.geladen.get(pfad) or synth_geladen(pfad=pfad)

    def export_job(self, *args: Any) -> tuple[str, str]:
        """Attrappe von ``export_job``: schreibt Dateien, wirft wie der Kern bei Vorhandenem."""
        self.export.append(args)
        if self.export_fehler is not None:
            raise ValueError(self.export_fehler)
        basis = Path(args[1])
        npz, js = Path(f"{basis}.npz"), Path(f"{basis}.json")
        for pfad in (npz, js):
            if pfad.exists():
                raise FileExistsError(f"Exportdatei existiert bereits: {pfad}")
        npz.write_bytes(b"npz")
        js.write_text("{}", encoding="utf-8")
        return str(npz), str(js)

    def pruef_job(self, *args: Any) -> PruefErgebnis:
        self.pruef.append(args)
        if self.pruef_fehler is not None:
            raise ValueError(self.pruef_fehler)
        return synth_pruefung()


class _NieFertig:
    """Auftrag, der nie fertig wird; merkt ``abbrechen``."""

    def __init__(self, funktion: Callable[..., Any], argumente: tuple[Any, ...]) -> None:
        self.funktion = funktion
        self.argumente = argumente
        self.abgebrochen = False

    def fertig(self) -> bool:
        return self.abgebrochen

    def ergebnis(self) -> Any:
        raise AuftragAbgebrochen

    def abbrechen(self) -> None:
        self.abgebrochen = True


class NieFertigAusfuehrer:
    """Ausführer, dessen Aufträge nie fertig werden (UI-15: Oberfläche bleibt bedienbar)."""

    def __init__(self) -> None:
        self.auftraege: list[_NieFertig] = []
        self.beendet = False

    def starte(self, funktion: Callable[..., Any], *argumente: Any) -> Auftrag:
        auftrag = _NieFertig(funktion, argumente)
        self.auftraege.append(auftrag)
        return auftrag

    def beende(self) -> None:
        self.beendet = True
        for a in self.auftraege:
            a.abbrechen()


class SteuerbarerAusfuehrer:
    """Ausführer, bei dem der Test bestimmt, wann ein Auftrag fertig wird (Job-ID-Tests)."""

    def __init__(self) -> None:
        self.auftraege: list[_Steuerbar] = []
        self.beendet = False

    def starte(self, funktion: Callable[..., Any], *argumente: Any) -> Auftrag:
        auftrag = _Steuerbar(funktion, argumente)
        self.auftraege.append(auftrag)
        return auftrag

    def beende(self) -> None:
        self.beendet = True


class _Steuerbar:
    def __init__(self, funktion: Callable[..., Any], argumente: tuple[Any, ...]) -> None:
        self.funktion = funktion
        self.argumente = argumente
        self.freigegeben = False
        self.abgebrochen = False

    def fertig(self) -> bool:
        return self.freigegeben or self.abgebrochen

    def ergebnis(self) -> Any:
        if self.abgebrochen:
            raise AuftragAbgebrochen
        try:
            return self.funktion(*self.argumente)
        except Exception as exc:
            raise AuftragFehler(str(exc), type(exc).__name__) from exc

    def abbrechen(self) -> None:
        self.abgebrochen = True


Bauer = Callable[..., tuple[Any, "Protokoll"]]
"""Fixture ``baue(ausfuehrer=None, *, sitzung=None, aktiv=True)``: Fenster und Protokoll."""

__all__ = [
    "PFAD",
    "SHA",
    "Bauer",
    "DirektAusfuehrer",
    "NieFertigAusfuehrer",
    "Protokoll",
    "PruefErgebnis",
    "SteuerbarerAusfuehrer",
    "synth_geladen",
    "synth_pruefung",
]
