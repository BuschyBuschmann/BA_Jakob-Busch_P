"""Tests zum Korrekturpaket E1-K (Review R-E1): Worker-Fehler, Sperre, Schwärzung, Races."""

from __future__ import annotations

import json
import os
import subprocess
import sys
import threading
from pathlib import Path
from typing import Any

import erkundung
import pytest
from erkundung import Redactor
from fake_psv import FakeComError, Harness, make_harness
from test_erkundung_lauf import entry, run, status

# --- MAJOR 1: Fehler außerhalb von step.func ------------------------------------------------


def test_schreibfehler_im_worker_fuehrt_zu_fehlerstatus_und_exit_4(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    original = erkundung.Runner._write
    calls = {"n": 0}

    def flaky(self: erkundung.Runner, name: str, text: str) -> None:
        calls["n"] += 1
        if calls["n"] == 12:
            raise PermissionError(32, "gesperrt")
        original(self, name, text)

    monkeypatch.setattr(erkundung.Runner, "_write", flaky)
    h = make_harness(tmp_path)
    code, report, folder = run(tmp_path, h, "--stufe", "1")
    assert code == erkundung.EXIT_ERROR
    assert report["lauf"]["status"] == "fehler"
    assert "PermissionError" in report["lauf"]["hinweis"]
    assert report["lauf"]["exception"]["typ"] == "PermissionError"
    st = status(report)
    assert "uebersprungen" in st.values()
    assert len(st) == len(erkundung.build_steps("1", False))  # nichts fehlt kommentarlos
    last_ok = [k for k, v in st.items() if v != "uebersprungen"]
    assert last_ok  # die vor dem Fehler gelaufenen Punkte bleiben erhalten
    assert "!!!" in (folder / "konsole.log").read_text(encoding="utf-8")


def test_kurzzeitige_sperre_beim_ersetzen_wird_wiederholt(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    real_replace = os.replace
    calls = {"n": 0}

    def flaky_replace(src: Any, dst: Any) -> None:
        calls["n"] += 1
        if calls["n"] in (5, 6):
            raise PermissionError(5, "Zugriff verweigert")
        real_replace(src, dst)

    monkeypatch.setattr(os, "replace", flaky_replace)
    monkeypatch.setattr(erkundung, "WRITE_RETRY_WAIT_S", 0.0)
    code, report, _ = run(tmp_path, make_harness(tmp_path), "--stufe", "0")
    assert code == 0
    assert report["lauf"]["status"] == "vollstaendig"
    assert len(report["pruefpunkte"]) == len(erkundung.build_steps("0", False))


def test_dauerhafter_schreibfehler_beendet_mit_exit_4_ohne_absturz(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    real_replace = os.replace
    calls = {"n": 0}

    def broken(src: Any, dst: Any) -> None:
        calls["n"] += 1
        if calls["n"] > 8:
            raise PermissionError(32, "dauerhaft gesperrt")
        real_replace(src, dst)

    monkeypatch.setattr(os, "replace", broken)
    monkeypatch.setattr(erkundung, "WRITE_RETRY_WAIT_S", 0.0)
    code, report, _ = run(tmp_path, make_harness(tmp_path), "--stufe", "0")
    assert code == erkundung.EXIT_ERROR
    assert "Teilbericht konnte nicht geschrieben werden" in capsys.readouterr().err
    assert report["lauf"]["status"] == "laeuft"  # der zuletzt schreibbare Stand liegt vor


@pytest.mark.filterwarnings("ignore::pytest.PytestUnhandledThreadExceptionWarning")
def test_worker_ohne_regulaeren_abschluss_wird_erkannt(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    def die(self: erkundung.Runner, step: erkundung.Step) -> None:
        raise SystemExit  # beendet den Thread still, ohne Exception

    monkeypatch.setattr(erkundung.Runner, "execute", die)
    code, report, _ = run(tmp_path, make_harness(tmp_path), "--stufe", "0")
    assert code == erkundung.EXIT_ERROR
    assert "unerwartet beendet" in report["lauf"]["hinweis"]
    assert set(status(report).values()) == {"uebersprungen"}


# --- MINOR 3: Race beim Serialisieren ----------------------------------------------------------


class _FlakyDict(dict[str, Any]):
    def __init__(self, failures: int) -> None:
        super().__init__(a=1)
        self.failures = failures

    def items(self) -> Any:
        if self.failures > 0:
            self.failures -= 1
            raise RuntimeError("dictionary changed size during iteration")
        return super().items()


def test_snapshot_wiederholt_bei_race_und_gibt_notfalls_hinweis() -> None:
    assert erkundung._snapshot(_FlakyDict(2)) == {"a": 1}
    assert "nicht lesbar" in erkundung._snapshot(_FlakyDict(99), attempts=2)["hinweis"]


# --- MINOR 5: COM-Referenzen vor thread_done -----------------------------------------------------


def test_com_referenzen_werden_vor_thread_done_freigegeben(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    created: list[erkundung.Runner] = []

    class Spy(erkundung.Runner):
        def __init__(self, *args: Any, **kwargs: Any) -> None:
            super().__init__(*args, **kwargs)
            created.append(self)

    monkeypatch.setattr(erkundung, "Runner", Spy)
    h = make_harness(tmp_path)
    seen: list[int] = []
    h.env.thread_done = lambda: seen.append(len(created[0].state))
    run(tmp_path, h, "--stufe", "1")
    assert seen == [0]


# --- MINOR 6: Versions-Check ---------------------------------------------------------------------


def test_zu_altes_python_wird_vor_jeder_ausgabe_abgewiesen(
    capsys: pytest.CaptureFixture[str],
) -> None:
    with pytest.raises(SystemExit) as exc:
        erkundung._require_python((3, 10, 9))
    assert exc.value.code == 2
    err = capsys.readouterr().err
    assert "Python 3.11" in err
    assert "3.10.9" in err
    erkundung._require_python((3, 11, 0))
    erkundung._require_python((3, 13, 1))


def test_skript_laeuft_als_datei(tmp_path: Path) -> None:
    done = subprocess.run(
        [sys.executable, "-I", erkundung.__file__, "--version"],
        capture_output=True,
        text=True,
        check=True,
    )
    assert erkundung.SCRIPT_VERSION in done.stdout


# --- MINOR 7: Schwärzung über Profilpfad ---------------------------------------------------------


def test_redactor_profilordner_weicht_vom_anmeldenamen_ab() -> None:
    red = Redactor("jbusch", True, profile_dirs=["C:\\Users\\Jakob.Busch"])
    assert red.text("C:\\Users\\Jakob.Busch\\x") == "C:\\Users\\<user>\\x"
    assert red.text("C:\\Users\\jbusch_000\\x") == "C:\\Users\\<user>\\x"  # generische Regel
    assert red.text("C:\\Users\\JAKOBB~1\\AppData") == "C:\\Users\\<user>\\AppData"  # 8.3
    assert red.text("D:/Users/jbusch.RWTH/x") == "D:/Users/<user>/x"
    assert red.text("C:\\Users\\jbusch\\x") == "C:\\Users\\<user>\\x"


def test_redactor_laesst_systemprofile_stehen_und_ist_idempotent() -> None:
    red = Redactor("jbusch", True, profile_dirs=["C:\\Users\\jbusch"])
    for keep in ("C:\\Users\\Public\\Documents", "C:\\Users\\Default\\x", "C:\\Users\\All Users"):
        assert red.text(keep) == keep
    once = red.text("C:\\Users\\jbusch\\x")
    assert red.text(once) == once == "C:\\Users\\<user>\\x"
    assert red.apply({"a": [once]}) == {"a": [once]}


@pytest.mark.parametrize("account", ["Polytec", "Labor", "Messung", "PSV"])
def test_redactor_zerstoert_keine_fachbegriffe_bei_sprechendem_kontonamen(account: str) -> None:
    red = Redactor(account, True, protected=["MESS-PC"], profile_dirs=[f"C:\\Users\\{account}"])
    technical = [
        "C:\\Program Files\\Polytec\\PSV\\PSV.exe",
        "Polytec PSV Type Library | %ProgramFiles%\\Polytec | Labor 3 Messung PSV",
        '[HKCR(64-Bit-Sicht)\\CLSID\\{1}\\LocalServer32] @ = "C:\\Polytec\\psv.exe"',
        "HKCU\\Software\\Users\\Settings",
    ]
    for line in technical:
        assert red.text(line) == line, line
    report = {"SummaryInfo": {"Title": "Labor 3 Messung", "Comments": f"{account} PSV"}}
    assert red.apply(report) == report
    assert red.text(f"C:\\Users\\{account}\\AppData\\x") == "C:\\Users\\<user>\\AppData\\x"


def test_redactor_schwaerzt_personenfelder_auch_als_freies_wort() -> None:
    red = Redactor("jbusch", True, protected=["JBUSCH-PC"], profile_dirs=["C:\\Users\\Jakob.Busch"])
    out = red.apply(
        {"SummaryInfo": {"Author": "jbusch (Jakob.Busch) auf JBUSCH-PC", "Title": "jbusch-Test"}}
    )
    assert out["SummaryInfo"]["Author"] == "<user> (<user>) auf JBUSCH-PC"
    assert out["SummaryInfo"]["Title"] == "jbusch-Test"  # kein Personenfeld
    assert Redactor("ab", True).apply({"Author": "ab"}) == {"Author": "<user>"}
    assert Redactor("ab", True).apply({"Author": "abc"}) == {"Author": "abc"}


def test_redactor_randfaelle() -> None:
    red = Redactor("jbusch", True, profile_dirs=["C:\\Users\\Max Mustermann"])
    # Registry-Pfad mit "Users" bleibt, Dateipfade nur mit Laufwerk.
    assert red.text("HKCU\\Software\\Users\\Settings") == "HKCU\\Software\\Users\\Settings"
    # Profilname mit Leerzeichen vollständig, wenn bekannt.
    assert red.text("C:\\Users\\Max Mustermann\\x") == "C:\\Users\\<user>\\x"
    # Klammern gehören zum Ordnernamen, ein schließendes ")" nicht.
    assert red.text("C:\\Users\\jbusch(1)\\x") == "C:\\Users\\<user>\\x"
    assert red.text("(siehe C:\\Users\\jbusch)") == "(siehe C:\\Users\\<user>)"
    # Ein fremdes Profil mit Leerzeichen wird nur bis zum Leerzeichen erkannt (dokumentiert).
    assert red.text("C:\\Users\\Anna Beispiel\\x") == "C:\\Users\\<user> Beispiel\\x"
    assert red.text("/home/jbusch/x") == "/home/<user>/x"
    assert red.text("/Users/jbusch/x") == "/Users/<user>/x"
    assert Redactor("", True).active is False
    assert Redactor("x", False).text("C:\\Users\\x") == "C:\\Users\\x"


def test_redactor_nur_profil_ohne_anmeldename() -> None:
    red = Redactor("", True, profile_dirs=["/home/ab"])
    assert red.active is True
    assert red.text("/home/ab/x") == "/home/<user>/x"


def test_bericht_schwaerzt_abweichenden_profilordner(tmp_path: Path) -> None:
    server = "C:\\Users\\Jakob.Busch\\AppData\\psv.exe"
    h = make_harness(tmp_path, server_path=server, username="jbusch")
    h.env.profile_dirs = ("C:\\Users\\Jakob.Busch",)
    _, _, folder = run(tmp_path, h, "--stufe", "0")
    for name in ("bericht.json", "registry.reg.txt", "konsole.log"):
        text = (folder / name).read_text(encoding="utf-8")
        assert "Jakob.Busch" not in text, name
    assert "<user>" in (folder / "bericht.json").read_text(encoding="utf-8")


def test_build_env_liefert_profilpfade() -> None:
    env = erkundung.build_env()
    assert str(Path.home()) in env.profile_dirs


# --- MINOR 4: Konstantenprüfung ------------------------------------------------------------------


def test_konstantenpruefung_laeuft_nach_dem_verbinden_und_nennt_keine_unbelegte_ursache(
    tmp_path: Path,
) -> None:
    h = make_harness(tmp_path)
    h.env.read_constants = lambda names: dict.fromkeys(names)
    _, report, _ = run(tmp_path, h, "--stufe", "1")
    ids = [p["id"] for p in report["pruefpunkte"]]
    assert ids.index("P1-4-typelibs-com") > ids.index("P1-5-verbinden")
    hint = entry(report, "P1-4-typelibs-com")["hinweis"]
    assert "Ursache wurde nicht geprüft" in hint
    assert "gen_py-Cache für PSV" not in hint


# --- MINOR 8: Herkunft der 1b-Kennzahlen ---


def test_1b_kennzahlen_aus_live_psv_sind_gekennzeichnet(tmp_path: Path) -> None:
    datei = tmp_path / "Example.svd"
    datei.write_bytes(b"x")
    _, report, _ = run(tmp_path, make_harness(tmp_path), "--stufe", "1", "--datei", str(datei))
    derived = entry(report, "P1-10-daten")["werte"]["abgeleitet"]
    live = [k for k in derived if k.endswith("_LIVE_PSV")]
    assert len(live) == 3
    assert "nicht aus der Datei" in derived["hinweis_LIVE_PSV"]
    assert "delta_f_aus_achse_hz" in derived  # Dateikennzahlen bleiben ohne Zusatz


# --- MINOR 9: ReadOnly-Fehler verhindert Open ---


def test_fehler_bei_readonly_true_verhindert_open(tmp_path: Path) -> None:
    h = make_harness(tmp_path)
    h.world.fail[("PolyFile", "ReadOnly")] = FakeComError("ReadOnly nicht setzbar")
    datei = tmp_path / "Example.svd"
    datei.write_bytes(b"x")
    _, report, _ = run(tmp_path, h, "--stufe", "1", "--datei", str(datei))
    assert ("PolyFile", "Open", "call") not in h.world.log
    st = status(report)
    assert st["P1-10-oeffnen"] == "fehler"
    assert st["P1-10-struktur"] == "uebersprungen"
    assert st["P1-10-schliessen"] == "uebersprungen"
    assert report["dateien"]["unveraendert"] is True


# --- Sperre gegen ungewollten PSV-Start ---


def _count_dispatch(h: Harness) -> list[str]:
    seen: list[str] = []
    original = h.env.dispatch

    def counting(progid: str) -> Any:
        seen.append(progid)
        return original(progid)

    h.env.dispatch = counting
    return seen


def test_ohne_psv_prozess_wird_acquisitioninstance_nicht_angelegt(tmp_path: Path) -> None:
    h = make_harness(tmp_path)
    h.env.run_command = lambda cmd: '"System","4","Services","0","10 K"\n'
    seen = _count_dispatch(h)
    code, report, _ = run(tmp_path, h, "--stufe", "1")
    assert code == 0
    assert "PSV.AcquisitionInstance" not in seen
    assert h.world.log == []
    st = status(report)
    assert st["P1-5-verbinden"] == "uebersprungen"
    assert "Sperre" in entry(report, "P1-5-verbinden")["hinweis"]
    assert st["P1-6-zustand"] == "uebersprungen"
    assert entry(report, "P1-5-prozess")["werte"]["psv_prozesse"] == []


def test_fremder_polytec_prozess_oeffnet_die_sperre_nicht(tmp_path: Path) -> None:
    h = make_harness(tmp_path)
    h.env.run_command = lambda cmd: '"PolytecLicense.exe","77","Services","0","1 K"\n'
    seen = _count_dispatch(h)
    _, report, _ = run(tmp_path, h, "--stufe", "1")
    assert seen == []
    assert status(report)["P1-5-verbinden"] == "uebersprungen"
    assert len(entry(report, "P1-5-prozess")["werte"]["psv_prozesse"]) == 1


def test_nicht_lesbare_prozessliste_sperrt_ebenfalls(tmp_path: Path) -> None:
    h = make_harness(tmp_path)

    def broken(cmd: list[str]) -> str:
        raise FileNotFoundError("tasklist")

    h.env.run_command = broken
    seen = _count_dispatch(h)
    _, report, _ = run(tmp_path, h, "--stufe", "1")
    assert status(report)["P1-5-prozess"] == "fehler"
    assert seen == []


def test_start_psv_mit_bestaetigung_hebt_die_sperre_auf(tmp_path: Path) -> None:
    h = make_harness(tmp_path, running=False, answer="JA")
    h.env.run_command = lambda cmd: ""
    code, report, _ = run(tmp_path, h, "--stufe", "1", "--start-psv")
    assert code == 0
    assert h.world.started is True
    assert status(report)["P1-6-zustand"] == "ok"


def test_start_psv_ohne_bestaetigung_laesst_sperre_bestehen(tmp_path: Path) -> None:
    h = make_harness(tmp_path, running=False, answer="nein")
    h.env.run_command = lambda cmd: ""
    seen = _count_dispatch(h)
    _, report, _ = run(tmp_path, h, "--stufe", "1", "--start-psv")
    assert seen == []
    assert status(report)["P1-5-verbinden"] == "uebersprungen"


def test_stufe_1b_ist_von_der_sperre_nicht_betroffen(tmp_path: Path) -> None:
    h = make_harness(tmp_path)
    h.env.run_command = lambda cmd: ""
    seen = _count_dispatch(h)
    datei = tmp_path / "Example.svd"
    datei.write_bytes(b"x")
    _, report, _ = run(tmp_path, h, "--stufe", "1", "--datei", str(datei))
    assert seen == ["PolyFile.PolyFile"]
    assert status(report)["P1-10-daten"] == "ok"


# --- SensorHeadInfo (Plan-Nachtrag 1a) ---


def test_laserwellenlaenge_und_leistung_ueber_sensorheadinfo(tmp_path: Path) -> None:
    h = make_harness(tmp_path)
    _, report, _ = run(tmp_path, h, "--stufe", "1")
    vib = entry(report, "P1-6-vibrometer")
    assert vib["status"] == "ok"
    group = vib["werte"]["gruppen"][0]
    assert group["SerialNumber"] == "SN1"  # ControllerInfo bleibt
    head = group["controller"][0]["sensorkoepfe"][0]
    assert head["LaserWavelength"] == pytest.approx(632.8, rel=1e-12)
    assert head["LaserPower"] == pytest.approx(1.0, rel=1e-12)
    assert head["SerialNumber"] == "SH1"
    pf_log = {(k, n) for k, n, _ in h.world.log}
    assert ("SensorHeadInfo", "LaserWavelength") in pf_log
    assert report["verweigert"] == []


def test_sensorheadinfo_fehler_bleibt_auf_den_punkt_beschraenkt(tmp_path: Path) -> None:
    h = make_harness(tmp_path)
    h.world.fail[("SensorHeadInfo", "LaserPower")] = FakeComError("n/a")
    _, report, _ = run(tmp_path, h, "--stufe", "1")
    assert status(report)["P1-6-vibrometer"] == "fehler"
    head = entry(report, "P1-6-vibrometer")["werte"]["gruppen"][0]["controller"][0]
    assert head["sensorkoepfe"][0]["LaserWavelength"] == pytest.approx(632.8, rel=1e-12)
    assert status(report)["P1-6-messpunkte"] == "ok"


# --- NITPICKs ---


def test_haengender_dispatch_nennt_den_letzten_aufruf(tmp_path: Path) -> None:
    h = make_harness(tmp_path)
    release = threading.Event()
    original = h.env.dispatch

    def hanging(progid: str) -> Any:
        release.wait(timeout=30)
        return original(progid)

    h.env.dispatch = hanging
    try:
        code, report, _ = run(tmp_path, h, "--stufe", "1", "--timeout-s", "0.3")
    finally:
        release.set()
    assert code == erkundung.EXIT_BLOCKED
    blocked = entry(report, "P1-5-verbinden")
    assert blocked["status"] == "blockiert"
    assert blocked["letzter_aufruf"]["pfad"] == "Dispatch.PSV.AcquisitionInstance"


def test_stop_run_ignoriert_veralteten_punkt(tmp_path: Path) -> None:
    h = make_harness(tmp_path)
    args = erkundung.build_parser().parse_args([])
    out = tmp_path / "r"
    out.mkdir()
    runner = erkundung.Runner(h.env, args, out, Redactor("", False), erkundung.ProxyContext(), 0.01)
    runner.data.update({"pruefpunkte": [], "lauf": {}})
    step = erkundung.Step("T", "0", "t", "x", lambda cx: None)
    stale = erkundung._Running(step, 0.0, erkundung.StepContext(runner, step))
    runner.current = erkundung._Running(step, 1.0, erkundung.StepContext(runner, step))
    assert runner._stop_run([step], "blockiert", "h", 3, expected=stale) is False
    assert h.exits == []
    assert runner.blocked is False
    assert runner._stop_run([step], "blockiert", "h", 3, expected=runner.current) is True
    assert h.exits == [3]
    assert json.loads((out / "bericht.json").read_text("utf-8"))["pruefpunkte"][0]["status"] == (
        "blockiert"
    )


def test_blacklist_enthaelt_dokumentierte_scanhead_namen() -> None:
    names = {n for k, n, _op, _v in erkundung.BLACKLIST if k == "ScanHeadControl"}
    assert names == {
        "WriteFocusDataFactorySettings",
        "WriteFocusDataFocalLength",
        "WriteFocusDataInfinitePos",
        "WriteLaserIntensityData",
        "WriteMirrorAdjustmentData",
    }


def test_lauf_mit_konto_polytec_behaelt_polytec_pfade_und_typbibliotheken(tmp_path: Path) -> None:
    h = make_harness(tmp_path, username="Polytec", hostname="MESS-PC")
    h.env.profile_dirs = ("C:\\Users\\Polytec",)
    _, report, folder = run(tmp_path, h, "--stufe", "0")
    text = (folder / "bericht.json").read_text(encoding="utf-8")
    assert "Polytec PSV Type Library" in text
    assert "Program Files\\\\Polytec\\\\psv.tlb" in text
    assert "Polytec PSV Type Library" in (folder / "typelibs.txt").read_text(encoding="utf-8")
    assert report["benutzername_entfernt"] is True


def test_schreiben_von_umgebung_und_rohdaten_nimmt_den_runner_lock(tmp_path: Path) -> None:
    h = make_harness(tmp_path)
    args = erkundung.build_parser().parse_args([])
    out = tmp_path / "r"
    out.mkdir()
    runner = erkundung.Runner(h.env, args, out, Redactor("", False), erkundung.ProxyContext(), 0.01)
    runner.data.update({"umgebung": {}, "abweichungen": []})
    step = erkundung.Step("T", "0", "t", "x", lambda cx: None)
    cx = erkundung.StepContext(runner, step)
    done = threading.Event()

    def writer() -> None:
        cx.raw("a.txt", ["x"])
        cx.deviation("t", "r")
        done.set()

    with runner.lock:
        thread = threading.Thread(target=writer)
        thread.start()
        assert not done.wait(0.2)  # blockiert, solange der Flush den Lock hält
    assert done.wait(5)
    thread.join()
    assert runner.raw_files == {"a.txt": ["x"]}
