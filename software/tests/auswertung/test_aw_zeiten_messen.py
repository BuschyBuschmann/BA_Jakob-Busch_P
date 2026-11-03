"""Messskript ``tools/auswertung/zeiten_messen.py`` (P-AUSW T1.4)."""

from __future__ import annotations

import json
import time
from pathlib import Path
from typing import Any

import aw_referenz as ref
import numpy as np
import pytest
import zeiten_messen as zm

from ldv_automation.auswertung.jobs import PruefErgebnis
from ldv_automation.hintergrund import DirektAusfuehrer

DATEI = Path(__file__).resolve().parents[3] / "Input" / "20261012_ref_Mitte.svd"
braucht_datei = pytest.mark.skipif(not DATEI.is_file(), reason="Messdatei nicht vorhanden")


def test_statistik_min_median_max() -> None:
    assert zm.statistik([3.0, 1.0, 2.0]) == {"min_s": 1.0, "median_s": 2.0, "max_s": 3.0, "n": 3.0}
    assert zm.statistik([1.0, 2.0, 3.0, 10.0])["median_s"] == 2.5
    assert zm.statistik([0.5])["max_s"] == 0.5
    with pytest.raises(ValueError, match="leer"):
        zm.statistik([])


class _Uhr:
    """Zeitquelle, die bei jedem Aufruf um ``schritt`` weiterläuft."""

    def __init__(self, schritt: float) -> None:
        self.t = 0.0
        self.schritt = schritt

    def __call__(self) -> float:
        self.t += self.schritt
        return self.t


class _Auftrag:
    def __init__(self, fertig_nach: int | None, ergebnis: Any = "erg") -> None:
        self.aufrufe = 0
        self.fertig_nach = fertig_nach
        self._ergebnis = ergebnis
        self.abgebrochen = False

    def fertig(self) -> bool:
        self.aufrufe += 1
        return self.fertig_nach is not None and self.aufrufe >= self.fertig_nach

    def ergebnis(self) -> Any:
        return self._ergebnis

    def abbrechen(self) -> None:
        self.abgebrochen = True


def test_warte_auf_misst_abfragen_und_ergebnis() -> None:
    auftrag = _Auftrag(fertig_nach=3)
    uhr = _Uhr(0.5)
    schlaefe: list[float] = []
    erg, mess = zm.warte_auf(auftrag, uhr, schlaefe.append)
    assert erg == "erg" and auftrag.aufrufe == 3
    assert schlaefe == [zm.TAKT_S, zm.TAKT_S]  # zwischen den drei Abfragen
    assert mess["abfragen"] == 3.0
    assert mess["max_abfrage_s"] == pytest.approx(0.5)  # je Abfrage zwei Uhrablesungen: 0,5 s
    assert mess["ergebnis_s"] == pytest.approx(0.5)
    assert mess["gesamt_s"] > 0


def test_warte_auf_bricht_nach_der_zeitgrenze_ab() -> None:
    auftrag = _Auftrag(fertig_nach=None)
    with pytest.raises(TimeoutError, match="nicht fertig"):
        zm.warte_auf(auftrag, _Uhr(100.0), lambda _: None)
    assert auftrag.abgebrochen


def test_paar_zeit_ohne_kreuzspektrum() -> None:
    daten = ref.messdaten(
        frequenz_hz=0.5 * np.arange(1, 9, dtype=np.float64), ap={"Vib Z": np.ones((2, 8))}
    )
    with pytest.raises(ValueError, match="Kreuzspektrum"):
        zm._paar_zeit(daten, time.perf_counter)


def test_paar_zeit_synthetisch() -> None:
    k = 200
    f = 0.5 * np.arange(1, k + 1, dtype=np.float64)
    h = np.broadcast_to(ref.mobilitaet_sdof(f, 20.0), (2, k)).astype(np.complex128)
    daten = ref.messdaten(
        frequenz_hz=f,
        ap={"Vib Z": (np.abs(h) ** 2).astype(np.float64), "Ref1": np.ones((2, k))},
        cp={("Vib Z", "Ref1"): h},
    )
    kalt, warm, name = zm._paar_zeit(daten, time.perf_counter)
    assert name == "Vib Z/Ref1" and kalt > 0 and warm > 0


def test_messe_wiederholungen_pruefen(tmp_path: Path) -> None:
    with pytest.raises(ValueError, match="wiederholungen"):
        zm.messe(tmp_path / "x.svd", wiederholungen=0)


def test_matplotlib_import_wird_in_frischem_prozess_gemessen() -> None:
    assert zm._matplotlib_import_s() > 0.0


def test_formatiere_zeigt_statistik_und_einzelwerte() -> None:
    ergebnis = {
        "umgebung": {
            "system": "Testsystem",
            "python": "3.11.0",
            "cpu_anzahl": 4,
            "numpy": "2.4.6",
            "ausfuehrer": "ProzessAusfuehrer",
        },
        "datei": {"pfad": "a.svd", "groesse_byte": 27_000_000},
        "messungen": {
            "lesen": zm.statistik([0.1, 0.2]),
            "lese_job": {**zm.statistik([1.0]), "max_abfrage_s": 0.04, "max_ergebnis_s": 0.0},
            "paar_kalt": {"s": 0.25, "paar": "Vib X/Ref1"},
        },
    }
    text = zm.formatiere(ergebnis)
    assert "Testsystem" in text and "27.0 MB" in text
    assert "lesen" in text and "0.150s" in text  # Median
    assert "längste fertig()-Abfrage 40 ms" in text
    assert "s = 0.250 s" in text and "paar = Vib X/Ref1" in text


@braucht_datei
def test_messe_an_beispieldatei_mit_direktem_ausfuehrer(monkeypatch: pytest.MonkeyPatch) -> None:
    """Alle Messungen laufen durch; die Prüfung wird durch einen schnellen Ersatz gestellt."""
    aufrufe: list[str] = []

    def schnelle_pruefung(pfad: str, sha: str | None = None) -> PruefErgebnis:
        aufrufe.append(pfad)
        return PruefErgebnis(pruefungen=(), annahmen=(), sha256=sha or "")

    monkeypatch.setattr(zm, "pruef_job", schnelle_pruefung)
    ergebnis = zm.messe(DATEI, wiederholungen=1, ausfuehrer_fabrik=DirektAusfuehrer)
    m = ergebnis["messungen"]
    erwartet = {
        "lesen",
        "sha256",
        "lade_svd",
        "spawn_leer",
        "lese_job",
        "abbrechen",
        "paar_kalt",
        "paar_warm",
        "schwingform",
        "pruef_job",
        "import_matplotlib",
    }
    assert set(m) == erwartet
    assert aufrufe == [str(DATEI)]
    assert m["lesen"]["n"] == 1.0 and m["lesen"]["min_s"] > 0
    assert m["lese_job"]["max_abfrage_s"] >= 0 and m["paar_kalt"]["paar"] == "Vib X/Ref1"
    assert ergebnis["umgebung"]["ausfuehrer"] == "DirektAusfuehrer"
    assert ergebnis["datei"]["groesse_byte"] == DATEI.stat().st_size
    json.dumps(ergebnis)  # JSON-fähig
    assert "lese_job" in zm.formatiere(ergebnis)


@braucht_datei
def test_main_mit_echtem_prozess_schreibt_json(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    ziel = tmp_path / "zeiten.json"
    code = zm.main(
        [
            str(DATEI),
            "--wiederholungen",
            "1",
            "--ohne-pruefung",
            "--ohne-matplotlib",
            "--json",
            str(ziel),
        ]
    )
    assert code == 0
    assert "lese_job" in capsys.readouterr().out
    daten = json.loads(ziel.read_text(encoding="utf-8"))
    assert daten["umgebung"]["ausfuehrer"] == "ProzessAusfuehrer"
    assert "pruef_job" not in daten["messungen"] and "import_matplotlib" not in daten["messungen"]
    assert daten["messungen"]["lese_job"]["median_s"] > 0
    assert daten["messungen"]["abbrechen"]["max_s"] < 5.0


def test_main_fehlende_datei(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    assert zm.main([str(tmp_path / "fehlt.svd")]) == 2
    assert "Datei fehlt" in capsys.readouterr().err


def test_main_meldet_fehler_der_messung(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    datei = tmp_path / "x.svd"
    datei.write_bytes(b"x")

    def kaputt(*_: Any, **__: Any) -> dict[str, Any]:
        raise ValueError("Messung unmöglich")

    monkeypatch.setattr(zm, "messe", kaputt)
    assert zm.main([str(datei)]) == 2
    assert "Messung unmöglich" in capsys.readouterr().err
