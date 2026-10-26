"""Ablage, Versionsermittlung und Messprotokoll-Schema."""

from __future__ import annotations

import hashlib
import json
import subprocess
from collections.abc import Sequence
from datetime import UTC, datetime, timedelta, timezone
from pathlib import Path

import pytest

from ldv_automation import __version__
from ldv_automation.geraet.schnittstelle import EinstellungsStand, GeraeteFehler
from ldv_automation.protokoll.ablage import (
    dateibasis,
    haenge_an,
    lege_durchgangsordner,
    schreibe_neu,
    sha256_datei,
    sicherer_name,
)
from ldv_automation.protokoll.messprotokoll import (
    PFLICHTFELDER,
    Ereignisprotokoll,
    einstellungsstand_zu_dict,
    fehlende_pflichtfelder,
    fehler_zu_dict,
    schreibe_messprotokoll,
    zeitstempel,
)
from ldv_automation.protokoll.version import (
    BUILD_INFO_DATEI,
    Befehlsausfuehrer,
    ermittle_build_info,
)

HASH = "89abcdef0123456789abcdef0123456789abcdef"
MEZ = timezone(timedelta(hours=1))

# --- ablage ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    ("name", "erwartet"),
    [
        ("Platte oben", "Platte_oben"),
        ("Übergröße/ß", "Uebergroesse_ss"),
        ("  a..b  ", "a_b"),
        ("é-1", "e-1"),
    ],
)
def test_sicherer_name(name: str, erwartet: str) -> None:
    assert sicherer_name(name) == erwartet


def test_sicherer_name_leer_und_laenge() -> None:
    with pytest.raises(ValueError):
        sicherer_name("///")
    assert len(sicherer_name("x" * 200)) == 60


def test_durchgangsordner_wird_nie_wiederverwendet(tmp_path: Path) -> None:
    zeit = datetime(2026, 11, 2, 9, 5, 7, tzinfo=MEZ)
    erster = lege_durchgangsordner(tmp_path, "Lauf", zeit)
    zweiter = lege_durchgangsordner(tmp_path, "Lauf", zeit)
    assert erster.name == "2026-11-02_090507_Lauf"
    assert zweiter.name == "2026-11-02_090507_Lauf_2"
    with pytest.raises(FileNotFoundError):
        lege_durchgangsordner(tmp_path / "fehlt", "Lauf", zeit)


def test_dateibasis() -> None:
    assert dateibasis(3, "Platte", 1) == "03_Platte"
    assert dateibasis(3, "Platte", 2) == "03_Platte_v2"
    assert dateibasis(123, "P", 1) == "123_P"
    with pytest.raises(ValueError):
        dateibasis(0, "P", 1)


def test_schreiben_ohne_ueberschreiben(tmp_path: Path) -> None:
    pfad = tmp_path / "a.txt"
    schreibe_neu(pfad, "eins")
    with pytest.raises(FileExistsError):
        schreibe_neu(pfad, "zwei")
    assert pfad.read_text("utf-8") == "eins"
    haenge_an(pfad, "-x")
    assert pfad.read_text("utf-8") == "eins-x\n"
    with pytest.raises(ValueError):
        haenge_an(pfad, "a\nb")


def test_sha256_gegen_hashlib_und_bekannten_wert(tmp_path: Path) -> None:
    pfad = tmp_path / "abc"
    pfad.write_bytes(b"abc")
    # FIPS 180-2, Anhang B.1: SHA-256("abc")
    assert sha256_datei(pfad) == "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad"
    gross = tmp_path / "gross"
    daten = bytes(range(256)) * 10_000
    gross.write_bytes(daten)
    assert sha256_datei(gross) == hashlib.sha256(daten).hexdigest()


# --- version --------------------------------------------------------------------------


def _ausfuehrer(antworten: dict[str, str | Exception]) -> Befehlsausfuehrer:
    def ausfuehren(befehl: Sequence[str], ordner: Path) -> str:
        antwort = antworten[befehl[1]]
        if isinstance(antwort, Exception):
            raise antwort
        return antwort

    return ausfuehren


def test_version_aus_git(tmp_path: Path) -> None:
    info = ermittle_build_info(
        paketordner=tmp_path,
        ausfuehren=_ausfuehrer({"rev-parse": HASH + "\n", "status": " M datei.py\n"}),
    )
    assert (info.git_hash, info.git_dirty, info.quelle) == (HASH, True, "git")
    assert info.paket_version == __version__
    sauber = ermittle_build_info(
        paketordner=tmp_path, ausfuehren=_ausfuehrer({"rev-parse": HASH, "status": ""})
    )
    assert sauber.git_dirty is False


def test_version_aus_build_info(tmp_path: Path) -> None:
    (tmp_path / BUILD_INFO_DATEI).write_text(
        json.dumps({"git_hash": HASH, "git_dirty": False}), "utf-8"
    )
    info = ermittle_build_info(
        paketordner=tmp_path,
        ausfuehren=_ausfuehrer({"rev-parse": OSError("kein git"), "status": ""}),
    )
    assert (info.git_hash, info.git_dirty, info.quelle) == (HASH, False, "build_info")


@pytest.mark.parametrize(
    ("inhalt", "teil"),
    [
        (None, "fehlt"),
        ("{kaputt", "nicht lesbar"),
        (json.dumps({"git_hash": "zu-kurz"}), "ohne gültigen"),
        (json.dumps([1]), "ohne gültigen"),
    ],
)
def test_version_ohne_quelle_nennt_grund(tmp_path: Path, inhalt: str | None, teil: str) -> None:
    if inhalt is not None:
        (tmp_path / BUILD_INFO_DATEI).write_text(inhalt, "utf-8")
    info = ermittle_build_info(
        paketordner=tmp_path,
        ausfuehren=_ausfuehrer(
            {"rev-parse": subprocess.CalledProcessError(128, "git"), "status": ""}
        ),
    )
    assert info.git_hash is None and info.quelle == "keine"
    assert info.grund is not None and teil in info.grund and "git nicht verfügbar" in info.grund


def test_version_git_mit_ungueltigem_hash(tmp_path: Path) -> None:
    info = ermittle_build_info(
        paketordner=tmp_path, ausfuehren=_ausfuehrer({"rev-parse": "HEAD", "status": ""})
    )
    assert info.git_hash is None
    assert info.grund is not None and "keinen gültigen Hash" in info.grund


def test_version_im_echten_repository() -> None:
    info = ermittle_build_info()
    # In diesem Repository mit Git: Hash vorhanden; ohne Git: Grund vorhanden.
    assert (info.git_hash is not None) or (info.grund is not None)


# --- messprotokoll --------------------------------------------------------------------


def test_zeitstempel_lokal_und_utc() -> None:
    zeit = datetime(2026, 11, 2, 10, 0, 0, tzinfo=MEZ)
    assert zeitstempel(zeit) == {
        "lokal": "2026-11-02T10:00:00+01:00",
        "utc": "2026-11-02T09:00:00+00:00",
    }
    with pytest.raises(ValueError):
        zeitstempel(datetime(2026, 11, 2))
    assert zeitstempel(datetime(2026, 1, 1, tzinfo=UTC))["utc"].endswith("+00:00")


def test_fehler_zu_dict() -> None:
    geraet = GeraeteFehler("kaputt", methode="starte_scan", hresult=-1, excepinfo="info")
    assert fehler_zu_dict("geraet", "kaputt", geraet) == {
        "art": "geraet",
        "text": "kaputt",
        "hresult": -1,
        "excepinfo": "info",
        "methode": "starte_scan",
    }
    assert fehler_zu_dict("x", "y", ValueError())["hresult"] is None


def test_einstellungsstand_zu_dict() -> None:
    stand = EinstellungsStand(modus="Fft", gruppen={"fft": {"linien": 800}})
    assert einstellungsstand_zu_dict(stand) == {
        "modus": "Fft",
        "messpunkte_anzahl": None,
        "generator_aktiv": None,
        "generator_amplitude_v": None,
        "gruppen": {"fft": {"linien": 800}},
    }


def test_messprotokoll_schema_wird_erzwungen(tmp_path: Path) -> None:
    daten: dict[str, object] = dict.fromkeys(PFLICHTFELDER)
    daten["schema_version"] = 1
    assert fehlende_pflichtfelder(daten) == []
    pfad = tmp_path / "p.protokoll.json"
    schreibe_messprotokoll(pfad, daten)
    assert list(json.loads(pfad.read_text("utf-8"))) == list(PFLICHTFELDER)
    with pytest.raises(FileExistsError):
        schreibe_messprotokoll(pfad, daten)
    unvollstaendig = dict(daten)
    del unvollstaendig["git_hash"]
    with pytest.raises(ValueError, match="git_hash"):
        schreibe_messprotokoll(tmp_path / "b.json", unvollstaendig)
    with pytest.raises(ValueError, match="extra"):
        schreibe_messprotokoll(tmp_path / "c.json", {**daten, "extra": 1})
    with pytest.raises(ValueError, match="schema_version"):
        schreibe_messprotokoll(tmp_path / "d.json", {**daten, "schema_version": 2})


def test_ereignisprotokoll_nur_anhaengend(tmp_path: Path) -> None:
    pfad = tmp_path / "e.jsonl"
    protokoll = Ereignisprotokoll(pfad)
    zeit = datetime(2026, 11, 2, 9, 0, tzinfo=MEZ)
    protokoll.schreibe(zeit, "start", {"wert": 1})
    protokoll.schreibe(zeit, "ende", {"pfad": tmp_path})
    zeilen = [json.loads(z) for z in pfad.read_text("utf-8").splitlines()]
    assert [z["art"] for z in zeilen] == ["start", "ende"]
    assert zeilen[1]["pfad"] == str(tmp_path)
    with pytest.raises(FileExistsError):
        Ereignisprotokoll(pfad)
