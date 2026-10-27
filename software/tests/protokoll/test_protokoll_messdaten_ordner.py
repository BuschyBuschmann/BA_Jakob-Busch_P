"""Prüfung des Messdaten-Ordners (U5/B4, Brief 3.11)."""

from __future__ import annotations

import os
import tempfile
from pathlib import Path

import pytest

from ldv_automation.protokoll.ablage import (
    geschuetzte_ordner_aus_umgebung,
    pruefe_messdaten_ordner,
)


def test_geeigneter_ordner_ohne_probleme(tmp_path: Path) -> None:
    assert pruefe_messdaten_ordner(tmp_path, windows=False) == ()
    assert list(tmp_path.iterdir()) == []  # Schreibprobe hinterlässt nichts


@pytest.mark.parametrize(
    ("pfad", "teil"),
    [
        ("Messdaten", "Laufwerksbuchstaben"),
        ("D:Messdaten", "Laufwerksbuchstaben"),
        ("\\\\server\\freigabe\\daten", "Laufwerksbuchstaben"),
        ("D:\\Polytec\\Daten", "Polytec"),
        ("E:\\POLYTEC PSV\\x", "Polytec"),
        ("C:\\Daten\\..\\ProgramData\\x", "Programm- oder Systemordner"),
        ("C:\\daten\\.\\..\\PROGRAM FILES\\Polytec\\x", "Programm- oder Systemordner"),
        ("C:\\PROGRA~3\\x", "Kurzname (8.3) nicht auflösbar"),
        ("C:\\Program Files\\Ablage", "Programm- oder Systemordner"),
        ("c:\\programdata\\x", "Programm- oder Systemordner"),
    ],
)
def test_windows_regeln_ohne_dateisystem(pfad: str, teil: str) -> None:
    probleme = pruefe_messdaten_ordner(
        Path(pfad),
        windows=True,
        geschuetzte_ordner=("C:\\Program Files", "C:\\ProgramData"),
    )
    assert any(teil in p for p in probleme), probleme


def test_windows_laufwerkspfad_geht_weiter_zur_dateipruefung() -> None:
    probleme = pruefe_messdaten_ordner(Path("D:\\Messdaten"), windows=True, geschuetzte_ordner=())
    assert probleme == ("Ordner existiert nicht: D:\\Messdaten",)


def test_posix_relativer_pfad(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.chdir(tmp_path)
    assert pruefe_messdaten_ordner(Path("relativ"), windows=False) == (
        "Kein absoluter Pfad: relativ",
    )


def test_git_repository_und_fehlender_ordner(tmp_path: Path) -> None:
    (tmp_path / ".git").mkdir()
    innen = tmp_path / "a" / "b"
    innen.mkdir(parents=True)
    probleme = pruefe_messdaten_ordner(innen, windows=False)
    assert len(probleme) == 1 and "Git-Repository" in probleme[0] and str(tmp_path) in probleme[0]
    assert pruefe_messdaten_ordner(tmp_path / "fehlt", windows=False)[0].startswith(
        "Ordner existiert nicht"
    )


def test_nicht_beschreibbar(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    def verweigert(**_k: object) -> object:
        raise PermissionError("Zugriff verweigert")

    monkeypatch.setattr(tempfile, "TemporaryFile", verweigert)
    probleme = pruefe_messdaten_ordner(tmp_path, windows=False)
    assert probleme == ("Ordner ist nicht beschreibbar: Zugriff verweigert",)


def test_geschuetzte_ordner_aus_umgebung() -> None:
    env = {"ProgramFiles": "C:\\Program Files", "ProgramData": "", "SystemRoot": "C:\\Windows"}
    assert geschuetzte_ordner_aus_umgebung(env) == ("C:\\Program Files", "C:\\Windows")
    assert isinstance(geschuetzte_ordner_aus_umgebung(), tuple)


def test_standard_folgt_dem_laufenden_system(tmp_path: Path) -> None:
    erwartet = () if os.name != "nt" else pruefe_messdaten_ordner(tmp_path, windows=True)
    assert pruefe_messdaten_ordner(tmp_path) == erwartet


GESCHUETZT = ("C:\\Program Files", "C:\\ProgramData")


@pytest.mark.parametrize(
    "pfad",
    [
        "C:\\Users\\Polytec\\Messungen",
        "D:\\Messdaten\\Polytec-Vergleich",
        "C:\\Users\\Public\\Documents\\POLYTEC PSV\\x",
    ],
)
def test_k_u5b_polytec_nur_unter_laufwerkswurzel_benutzerkonten_erlaubt(pfad: str) -> None:
    # Regeln bestanden; nur die Dateiprüfung schlägt unter Linux fehl
    probleme = pruefe_messdaten_ordner(Path(pfad), windows=True, geschuetzte_ordner=GESCHUETZT)
    assert len(probleme) == 1 and probleme[0].startswith("Ordner existiert nicht")


def test_k_u5b_kurzname_wird_ueber_aufloesen_erkannt() -> None:
    # Unter Windows löst os.path.realpath den Kurznamen auf; hier simuliert.
    def aufloesen(text: str) -> str:
        return text.replace("PROGRA~3", "ProgramData")

    probleme = pruefe_messdaten_ordner(
        Path("C:\\PROGRA~3\\x"),
        windows=True,
        geschuetzte_ordner=GESCHUETZT,
        aufloesen=aufloesen,
    )
    assert probleme == (
        "Liegt in einem Programm- oder Systemordner (C:\\ProgramData): "
        "C:\\PROGRA~3\\x (aufgelöst: C:\\ProgramData\\x)",
    )


def test_k_u5b_symbolischer_link_wird_aufgeloest(tmp_path: Path) -> None:
    ziel = tmp_path / "Polytec"
    ziel.mkdir()
    link = tmp_path / "harmlos"
    link.symlink_to(ziel, target_is_directory=True)
    # /tmp/.../Polytec liegt nicht direkt unter der Wurzel: erlaubt; aber Git-Regel greift
    # auf das aufgelöste Ziel
    (ziel / ".git").mkdir()
    probleme = pruefe_messdaten_ordner(link, windows=False)
    assert len(probleme) == 1 and str(ziel) in probleme[0] and "Git-Repository" in probleme[0]


def test_k_u5b_posix_polytec_unter_wurzel() -> None:
    probleme = pruefe_messdaten_ordner(Path("/polytec_daten/x"), windows=False)
    assert probleme == ("Liegt in einem Polytec-Verzeichnis: /polytec_daten/x",)
