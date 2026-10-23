"""Tests der plattformunabhängigen Hilfsfunktionen, der Adapter-Fallbacks und des Berichts."""

from __future__ import annotations

import datetime as dt
import importlib.util
import json
import math
import platform
import sys
from pathlib import Path
from typing import Any

import erkundung
import pytest
from fake_psv import FakeComError

# --- to_jsonable ------------------------------------------------------------------------


def test_to_jsonable_wandelt_sonderwerte_in_strenges_json() -> None:
    value = {
        "nan": math.nan,
        "inf": math.inf,
        "ok": 1.5,
        "bytes": b"\x01\xff",
        "zeit": dt.datetime(2026, 1, 2, 3, 4, 5, tzinfo=dt.UTC),
        "datum": dt.date(2026, 1, 2),
        "menge": {2},
        "tupel": (1, "a"),
        "pfad": Path("x/y"),
        "objekt": object,
        3: None,
    }
    result = erkundung.to_jsonable(value)
    text = json.dumps(result, allow_nan=False)
    loaded = json.loads(text)
    assert loaded["nan"] == "nan"
    assert loaded["inf"] == "inf"
    assert loaded["ok"] == pytest.approx(1.5, rel=1e-15)
    assert loaded["bytes"] == "01ff"
    assert loaded["zeit"] == "2026-01-02T03:04:05+00:00"
    assert loaded["datum"] == "2026-01-02"
    assert loaded["menge"] == [2]
    assert loaded["tupel"] == [1, "a"]
    assert loaded["pfad"] == str(Path("x/y"))
    assert loaded["3"] is None
    assert "object" in loaded["objekt"]


# --- Exceptions, Dateien, PE ------------------------------------------------------------


def test_describe_exception_com_error_und_normale_exception() -> None:
    info = erkundung.describe_exception(FakeComError("Text", hresult=-2147352567))
    assert info["typ"] == "FakeComError"
    assert info["hresult"] == -2147352567
    assert info["hresult_hex"] == "0x80020009"
    assert info["strerror"] == "Text"
    plain = erkundung.describe_exception(ValueError("x"))
    assert plain["hresult"] is None
    assert plain["hresult_hex"] is None
    assert "ValueError" in plain["traceback_gekuerzt"]


def test_describe_file(tmp_path: Path) -> None:
    path = tmp_path / "a.bin"
    path.write_bytes(b"abc")
    info = erkundung.describe_file(path)
    assert info["groesse_byte"] == 3
    assert info["sha256"] == "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad"


def _pe(machine: int, offset: int = 64, magic: bytes = b"MZ", sig: bytes = b"PE\x00\x00") -> bytes:
    header = bytearray(offset)
    header[:2] = magic
    header[60:64] = offset.to_bytes(4, "little")
    return bytes(header) + sig + machine.to_bytes(2, "little")


@pytest.mark.parametrize(
    ("content", "expected"),
    [
        (_pe(0x14C), "x86 (32 Bit)"),
        (_pe(0x8664), "x64 (64 Bit)"),
        (_pe(0xAA64), "ARM64"),
        (_pe(0x1234), "0x1234"),
        (_pe(0x8664, magic=b"XX"), None),
        (_pe(0x8664, sig=b"NE\x00\x00"), None),
        (b"MZ", None),
        (_pe(0x8664)[:66], None),
    ],
)
def test_pe_machine(tmp_path: Path, content: bytes, expected: str | None) -> None:
    path = tmp_path / "x.exe"
    path.write_bytes(content)
    assert erkundung.pe_machine(str(path)) == expected


def test_pe_machine_fehlende_datei(tmp_path: Path) -> None:
    assert erkundung.pe_machine(str(tmp_path / "gibt-es-nicht.exe")) is None


# --- Pfade, Umgebung, Auswahl -----------------------------------------------------------


def test_expand_env_und_parse_server_path() -> None:
    environ = {"SystemRoot": "C:\\Windows", "PF": "C:\\Program Files"}
    assert erkundung.expand_env("%SystemRoot%\\x.dll", environ) == "C:\\Windows\\x.dll"
    assert erkundung.expand_env("%UNBEKANNT%\\x", environ) == "%UNBEKANNT%\\x"
    assert erkundung.expand_env("%systemroot%", {"SYSTEMROOT": "C:\\W"}) == "C:\\W"
    parse = erkundung.parse_server_path
    assert parse('"C:\\Program Files\\P\\psv.exe" /Automation', environ) == (
        "C:\\Program Files\\P\\psv.exe"
    )
    assert parse("C:\\Program Files\\P\\psv.exe /Embedding", environ) == (
        "C:\\Program Files\\P\\psv.exe"
    )
    assert parse("%PF%\\x\\a.DLL", environ) == "C:\\Program Files\\x\\a.DLL"
    assert parse('"unvollständig', environ) == "unvollständig"
    assert parse("kein-dateiname", environ) == "kein-dateiname"


def test_collect_platform(monkeypatch: pytest.MonkeyPatch) -> None:
    info = erkundung.collect_platform({"PROCESSOR_ARCHITECTURE": "AMD64"})
    assert info["python_bit"] in (32, 64)
    assert info["python_version"].startswith("3.")
    monkeypatch.setattr(platform, "system", lambda: "Windows")
    assert (
        erkundung.collect_platform({"PROCESSOR_ARCHITECTURE": "AMD64"})["windows_bit_einschaetzung"]
        == 64
    )
    assert (
        erkundung.collect_platform({"PROCESSOR_ARCHITECTURE": "x86"})["windows_bit_einschaetzung"]
        == 32
    )
    assert (
        erkundung.collect_platform(
            {"PROCESSOR_ARCHITECTURE": "x86", "PROCESSOR_ARCHITEW6432": "AMD64"}
        )["windows_bit_einschaetzung"]
        == 64
    )


@pytest.mark.parametrize(
    ("count", "n", "expected"),
    [
        (5, 2, [1, 2, 4, 5]),
        (3, 5, [1, 2, 3]),
        (0, 3, []),
        (4, 0, []),
        (10, 1, [1, 10]),
        (1, 1, [1]),
    ],
)
def test_sample_indices(count: int, n: int, expected: list[int]) -> None:
    assert erkundung.sample_indices(count, n) == expected


def test_run_command_ohne_shell() -> None:
    out = erkundung.run_command([sys.executable, "-c", "print('hallo')"])
    assert out.strip() == "hallo"


def test_create_out_dir_vergibt_suffixe(tmp_path: Path) -> None:
    now = dt.datetime(2026, 1, 2, 3, 4, 5)
    first = erkundung.create_out_dir(tmp_path, "PC 1/x", now)
    second = erkundung.create_out_dir(tmp_path, "PC 1/x", now)
    third = erkundung.create_out_dir(tmp_path, "PC 1/x", now)
    assert first.name == "erkundung_PC_1_x_2026-01-02_030405"
    assert second.name == first.name + "_2"
    assert third.name == first.name + "_3"
    assert erkundung.create_out_dir(tmp_path, "", now).name.startswith("erkundung_rechner_")


# --- Adapter-Fallbacks ohne pywin32 / Windows -------------------------------------------

_HAS_PYWIN32 = importlib.util.find_spec("win32com") is not None


@pytest.mark.skipif(_HAS_PYWIN32, reason="prüft das Verhalten ohne pywin32")
def test_pywin32_info_ohne_pywin32() -> None:
    info = erkundung.pywin32_info()
    assert info["importierbar"] is False
    assert info["version"] is None
    assert "win32com" in info["fehler"]


@pytest.mark.skipif(_HAS_PYWIN32, reason="prüft das Verhalten ohne pywin32")
def test_com_adapter_ohne_pywin32_melden_sauber_com_unavailable() -> None:
    env = erkundung.build_env()
    for call in (
        lambda: env.dispatch("PSV.AcquisitionInstance"),
        env.enum_tlbs,
        lambda: env.read_constants(["ptcAcqStateStopped"]),
    ):
        with pytest.raises(erkundung.ComUnavailableError, match="pywin32"):
            call()
    env.thread_init()
    env.thread_done()


@pytest.mark.skipif(sys.platform == "win32", reason="prüft das Verhalten ohne Windows")
def test_build_env_unter_linux() -> None:
    env = erkundung.build_env()
    assert env.registry is None
    assert env.system != "Windows"
    assert env.file_version("/bin/sh") is None
    assert env.hostname
    assert env.now().tzinfo is not None
    assert env.monotonic() >= 0


# --- Zusammenfassung --------------------------------------------------------------------


def test_render_summary_minimal_und_mit_befunden() -> None:
    minimal = erkundung.render_summary({})
    assert "Keine festgestellt" in minimal
    assert "nicht ausgeführt" in minimal
    report: dict[str, Any] = {
        "rechnername": "PC",
        "lauf": {"status": "blockiert", "hinweis": "h"},
        "stufen": ["0", "1"],
        "verweigert": [{"pfad": "A.b", "op": "get", "pruefpunkt": "X"}],
        "abweichungen": [{"text": "T", "pruefpunkt": "X", "beleg_ref": "I5 8"}],
        "pruefpunkte": [
            {"id": "X", "stufe": "1", "status": "fehler", "dauer_s": 1.5, "kernwert": "a|b",
             "hinweis": "h", "auffaelligkeiten": ["e1"]},
            {"id": "P1-5-verbinden", "stufe": "1", "status": "ok", "dauer_s": 0.1},
        ],
    }  # fmt: skip
    text = erkundung.render_summary(report)
    assert "ACHTUNG: Zugriff verweigert" in text
    assert "`A.b`" in text
    assert "a\\|b" in text
    assert "- T (X; I5 8)" in text
    assert "| Kehrt GetApplication(False)" in text
    assert "| P1-5-verbinden | ok |" in text
    assert "1.6 s" in text
