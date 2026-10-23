"""Läufe von Stufe 0, 1 und 1b gegen Fake-PSV (K2-K9) einschließlich Fehlerinjektion."""

from __future__ import annotations

import hashlib
import json
import sys
import threading
from pathlib import Path
from typing import Any

import erkundung
import pytest
from erkundung import POLICY, main
from fake_psv import FakeComError, Harness, make_harness

STUFE0_IDS = [
    "P1-1-umgebung",
    "P1-4-pywin32",
    "P1-2-registry",
    "P1-2-dateien",
    "P1-4-typelibs-registry",
    "P1-3-verzeichnisse",
    "P1-5-prozess",
]


def run(tmp_path: Path, h: Harness, *argv: str) -> tuple[int, dict[str, Any], Path]:
    """Führt main() mit Fake-Umgebung aus und liest den Bericht des neuesten Ordners."""
    out = tmp_path / "out"
    code = main([*argv, "--out", str(out)], env=h.env, poll_s=0.01)
    folder = sorted(out.iterdir())[-1]
    report = json.loads((folder / "bericht.json").read_text(encoding="utf-8"))
    return code, report, folder


def status(report: dict[str, Any]) -> dict[str, str]:
    return {p["id"]: p["status"] for p in report["pruefpunkte"]}


def entry(report: dict[str, Any], step_id: str) -> dict[str, Any]:
    return next(p for p in report["pruefpunkte"] if p["id"] == step_id)


# --- Stufe 0 --------------------------------------------------------------------------


def test_stufe0_vollstaendig(tmp_path: Path) -> None:
    h = make_harness(tmp_path)
    code, report, folder = run(tmp_path, h, "--stufe", "0")
    assert code == 0
    assert [p["id"] for p in report["pruefpunkte"]] == STUFE0_IDS
    assert set(status(report).values()) == {"ok"}
    progids = entry(report, "P1-2-registry")["werte"]["progids"]
    ok64 = progids["PSV.AcquisitionInstance"]["64_bit"]
    assert ok64["vorhanden"] is True
    assert ok64["LocalServer32_pfad"].endswith("psv.exe")
    assert progids["PSV.AcquisitionInstance"]["32_bit"]["vorhanden"] is False
    assert ok64["InprocServer32_threadingmodel"] == "Apartment"
    assert ok64["AppID_name"] == "PSV AppID"
    files = entry(report, "P1-2-dateien")["werte"]["server_dateien"]
    assert files[0]["pe_maschine"] == "x64 (64 Bit)"
    assert files[0]["dateiversion"] == "10.4.0.1"
    assert any(not f["vorhanden"] for f in files)  # poly.dll existiert nicht
    typelibs = entry(report, "P1-4-typelibs-registry")["werte"]
    assert typelibs["gesamt_gesehen"] == 2
    assert [t["name"] for t in typelibs["treffer"]] == ["Polytec PSV Type Library"]
    dirs = entry(report, "P1-3-verzeichnisse")["werte"]["verzeichnisse"]
    present = [v for v in dirs.values() if v["vorhanden"]]
    assert [e["name"] for e in present[0]["eintraege"]] == ["PSV", "readme.txt"]
    assert entry(report, "P1-5-prozess")["werte"]["psv_prozesse"] == [
        {"name": "PSV.exe", "pid": "1234"}
    ]
    assert report["umgebung"]["python_bit"] in (32, 64)
    for name in ("bericht.json", "zusammenfassung.md", "konsole.log", "registry.reg.txt",
                 "typelibs.txt"):  # fmt: skip
        assert (folder / name).is_file(), name
    assert "(nicht vorhanden)" in (folder / "registry.reg.txt").read_text(encoding="utf-8")
    # Stufe 0 greift nicht auf COM zu.
    assert h.world.log == []
    assert report["whitelist_aufrufe"] == []


def test_stufe0_ohne_windows_und_registry_gibt_hinweise(tmp_path: Path) -> None:
    h = make_harness(tmp_path, with_registry=False, system="Linux", pywin32_ok=False)
    code, report, _ = run(tmp_path, h)
    assert code == 0
    st = status(report)
    assert st["P1-2-registry"] == "uebersprungen"
    assert st["P1-2-dateien"] == "uebersprungen"
    assert st["P1-4-typelibs-registry"] == "uebersprungen"
    assert st["P1-3-verzeichnisse"] == "uebersprungen"
    assert st["P1-5-prozess"] == "uebersprungen"
    assert "winreg" in entry(report, "P1-2-registry")["hinweis"]
    assert "pywin32" in entry(report, "P1-4-pywin32")["hinweis"]
    assert report["lauf"]["status"] == "vollstaendig"


@pytest.mark.skipif(sys.platform == "win32", reason="prüft das Verhalten ohne Windows")
def test_k8_echte_umgebung_unter_linux_liefert_saubere_hinweise(tmp_path: Path) -> None:
    out = tmp_path / "out"
    code = main(["--stufe", "1", "--out", str(out)], poll_s=0.01)
    assert code == 0
    report = json.loads((next(out.iterdir()) / "bericht.json").read_text(encoding="utf-8"))
    st = status(report)
    assert st["P1-1-umgebung"] == "ok"
    assert st["P1-2-registry"] == "uebersprungen"
    assert st["P1-4-typelibs-com"] == "uebersprungen"
    assert st["P1-5-verbinden"] == "uebersprungen"
    assert "pywin32" in entry(report, "P1-5-verbinden")["hinweis"]
    # Alle übrigen Stufe-1-Punkte werden mangels Verbindung übersprungen, nichts stürzt ab.
    assert all(v in ("ok", "uebersprungen") for v in st.values())


# --- Stufe 1 --------------------------------------------------------------------------


def test_k2_stufe1_nur_whitelist_und_zustand_unveraendert(tmp_path: Path) -> None:
    h = make_harness(tmp_path)
    before = h.world.snapshot()
    code, report, _ = run(tmp_path, h, "--stufe", "1")
    assert code == 0
    st = status(report)
    assert [k for k, v in st.items() if v not in ("ok",)] == []
    assert report["verweigert"] == []
    assert h.world.snapshot() == before
    # Unabhängiges Protokoll des Fakes: jeder Zugriff steht in der Whitelist, nichts wird gesetzt.
    for kind, name, op in h.world.log:
        assert op in ("get", "call"), (kind, name, op)
        assert name in POLICY[kind], (kind, name)
    assert not {n for _, n, _ in h.world.log} & {"Start", "Stop", "Scan", "ScanEx", "SetLaserOn"}
    assert [a for k, n, a in h.world.calls_args if n == "GetApplication"] == [(False,)]
    # Das Proxy-Protokoll im Bericht stimmt mit dem des Fakes überein (Dispatch zusätzlich).
    paths = [c["pfad"] for c in report["whitelist_aufrufe"] if c["op"] != "dispatch"]
    fake_paths = [f"{k}.{n}" for k, n, op in h.world.log if op != "set"]
    exists_calls = [c for c in report["whitelist_aufrufe"] if c["op"] == "exists"]
    assert len(paths) - len(exists_calls) == len(fake_paths)
    assert {c["pfad"] for c in exists_calls} == {
        "FftProperties.FftAcqPropertiesValidator",
        "Application.DigitalPorts",
    }


def test_stufe1_werte(tmp_path: Path) -> None:
    h = make_harness(tmp_path)
    _, report, _ = run(tmp_path, h, "--stufe", "1")
    app = entry(report, "P1-5-application")["werte"]
    assert app["Version"] == "10.4.0.1"
    assert app["Acquisition_erreichbar"] is True
    state = entry(report, "P1-6-zustand")["werte"]
    assert state["State"] == 0
    assert state["GetLaserOn"] == {"-1": True, "1": False, "2": False, "3": False}
    props = entry(report, "P1-6-eigenschaften")["werte"]
    assert props["gruppen_vorhanden"] == ["General", "Average", "Fft"]
    assert props["Fft"]["SampleResolution"] == pytest.approx(1.25, rel=1e-12)
    assert props["FftAcqPropertiesValidator_vorhanden"] is True
    assert entry(report, "P1-6-hardware")["werte"]["Hardware"]["AcqBoardChannelCount"] == 4
    assert entry(report, "P1-6-scankopf")["werte"]["ScanHeadType"] == 27
    vib = entry(report, "P1-6-vibrometer")["werte"]["gruppen"]
    assert vib[0]["SerialNumber"] == "SN1"
    mp = entry(report, "P1-6-messpunkte")["werte"]
    assert [p["item_position"] for p in mp["stichprobe"]] == [1, 2, 3, 4, 5]
    assert mp["stichprobe"][0]["CoordXYZ"] == [0.1, 0.2, 0.3]
    assert mp["LabelToIndex_erstes_Label"] == 1
    al = entry(report, "P1-6-abgleich")["werte"]
    assert al["Alignments3D"]["Count"] == 1
    assert al["Alignments3D"]["eintraege"][0]["CurrentQuality"] == pytest.approx(0.9, rel=1e-12)
    assert entry(report, "P3-2-existenz")["werte"]["DigitalPorts_vorhanden"] is True
    # Die Konstante ptcAcqStateSingle weicht im Fake bewusst ab.
    assert [d["pruefpunkt"] for d in report["abweichungen"]] == ["P1-4-typelibs-com"]
    assert "ptcAcqStateSingle" in report["abweichungen"][0]["text"]


def test_max_punkte_begrenzt_stichprobe(tmp_path: Path) -> None:
    h = make_harness(tmp_path)
    _, report, _ = run(tmp_path, h, "--stufe", "1", "--max-punkte", "1")
    mp = entry(report, "P1-6-messpunkte")["werte"]
    assert [p["item_position"] for p in mp["stichprobe"]] == [1, 5]


def test_k3_psv_laeuft_nicht_wird_nicht_gestartet(tmp_path: Path) -> None:
    h = make_harness(tmp_path, running=False)
    code, report, _ = run(tmp_path, h, "--stufe", "1")
    assert code == 0
    assert h.world.started is False
    assert not [c for c in h.world.calls_args if c[1] == "GetApplication"]
    st = status(report)
    assert st["P1-5-verbinden"] == "uebersprungen"
    assert "läuft nicht" in entry(report, "P1-5-verbinden")["hinweis"]
    for sid in ("P1-5-application", "P1-6-zustand", "P1-6-eigenschaften", "P1-6-hardware",
                "P1-6-messpunkte", "P1-6-abgleich", "P3-2-existenz"):  # fmt: skip
        assert st[sid] == "uebersprungen"
    assert h.inputs == []


def test_start_psv_nur_nach_bestaetigung(tmp_path: Path) -> None:
    h = make_harness(tmp_path, running=False, answer="nein")
    _, report, _ = run(tmp_path, h, "--stufe", "1", "--start-psv")
    assert h.world.started is False
    assert len(h.inputs) == 1
    assert status(report)["P1-5-verbinden"] == "uebersprungen"
    (tmp_path / "zwei").mkdir()
    h2 = make_harness(tmp_path / "zwei", running=False, answer="JA")
    code, report2, _ = run(tmp_path / "zwei", h2, "--stufe", "1", "--start-psv")
    assert code == 0
    assert h2.world.started is True
    assert entry(report2, "P1-5-verbinden")["werte"]["GetApplication_gestartet"] is True
    assert status(report2)["P1-6-zustand"] == "ok"


def test_start_psv_ohne_eingabekanal_gilt_als_nein(tmp_path: Path) -> None:
    h = make_harness(tmp_path, running=False)

    def no_input(prompt: str) -> str:
        raise EOFError

    h.env.input_fn = no_input
    run(tmp_path, h, "--stufe", "1", "--start-psv")
    assert h.world.started is False


def test_k4_laufende_messung_wird_nur_protokolliert(tmp_path: Path) -> None:
    h = make_harness(tmp_path, state=2)
    code, report, _ = run(tmp_path, h, "--stufe", "1")
    assert code == 0
    zustand = entry(report, "P1-6-zustand")
    assert zustand["werte"]["State"] == 2
    assert "nicht Stopped" in zustand["werte"]["warnung"]
    assert not {n for _, n, _ in h.world.log} & {"Stop", "Start"}
    assert h.world.started is False


def test_k5_fehler_in_einem_wert_stoppt_die_uebrigen_nicht(tmp_path: Path) -> None:
    h = make_harness(tmp_path)
    h.world.fail[("Hardware", "AcqBoardName")] = FakeComError("Boom", hresult=-2147352567)
    _, report, _ = run(tmp_path, h, "--stufe", "1")
    hw = entry(report, "P1-6-hardware")
    assert hw["status"] == "fehler"
    err = hw["werte"]["Hardware"]["AcqBoardName"]["fehler"]
    assert err["hresult"] == -2147352567
    assert err["hresult_hex"] == "0x80020009"
    assert err["excepinfo"][2] == "Boom"
    assert hw["werte"]["Hardware"]["FrontEnd"] == "FrontEnd-wert"  # übrige Werte vorhanden
    assert status(report)["P1-6-scankopf"] == "ok"
    assert report["lauf"]["status"] == "vollstaendig"


def test_k5_exception_im_punkt_laesst_andere_laufen(tmp_path: Path) -> None:
    h = make_harness(tmp_path)
    h.world.fail[("Acquisition", "Infos")] = FakeComError("Infos weg")
    _, report, _ = run(tmp_path, h, "--stufe", "1")
    st = status(report)
    assert st["P1-6-hardware"] == "fehler"
    assert entry(report, "P1-6-hardware")["exception"]["typ"] == "FakeComError"
    assert st["P1-6-zustand"] == "ok"
    assert st["P1-6-eigenschaften"] == "ok"


def test_modus_nicht_acquisition_ueberspringt_folgepunkte(tmp_path: Path) -> None:
    h = make_harness(tmp_path, mode=2)
    _, report, _ = run(tmp_path, h, "--stufe", "1")
    st = status(report)
    assert st["P1-5-application"] == "fehler"
    assert entry(report, "P1-5-application")["werte"]["Acquisition_erreichbar"] is False
    assert [d["text"] for d in report["abweichungen"] if d["pruefpunkt"] == "P1-5-application"]
    assert st["P1-6-zustand"] == "uebersprungen"
    assert st["P1-6-hardware"] == "uebersprungen"


def test_state_nicht_lesbar_bricht_stufe1_ab(tmp_path: Path) -> None:
    h = make_harness(tmp_path)
    h.world.fail[("Acquisition", "State")] = FakeComError("kein Zugriff")
    _, report, _ = run(tmp_path, h, "--stufe", "1")
    st = status(report)
    assert st["P1-6-zustand"] == "uebersprungen"
    assert st["P1-6-eigenschaften"] == "uebersprungen"
    assert st["P1-6-messpunkte"] == "uebersprungen"
    assert "State nicht lesbar" in entry(report, "P1-6-zustand")["hinweis"]


def test_hardware_nicht_vorhanden_wird_nicht_gelesen(tmp_path: Path) -> None:
    h = make_harness(tmp_path, has_hardware=False)
    _, report, _ = run(tmp_path, h, "--stufe", "1")
    assert entry(report, "P1-6-hardware")["status"] == "ok"
    assert "Hardware" not in entry(report, "P1-6-hardware")["werte"]
    assert ("Hardware", "FrontEnd", "get") not in h.world.log


def test_k5_haengender_aufruf_fuehrt_zu_teilbericht_und_prozessende(tmp_path: Path) -> None:
    h = make_harness(tmp_path)
    release = threading.Event()
    h.world.hang[("Hardware", "FrontEnd")] = release
    try:
        code, report, folder = run(tmp_path, h, "--stufe", "1", "--timeout-s", "0.3")
    finally:
        release.set()
    assert code == erkundung.EXIT_BLOCKED
    assert h.exits == [erkundung.EXIT_BLOCKED]
    st = status(report)
    assert st["P1-6-hardware"] == "blockiert"
    assert st["P1-6-zustand"] == "ok"  # frühere Punkte sind im Teilbericht
    assert st["P1-6-scankopf"] == "uebersprungen"
    blocked = entry(report, "P1-6-hardware")
    assert blocked["letzter_aufruf"]["pfad"] == "Hardware.FrontEnd"
    assert "blockiert bei P1-6-hardware" in blocked["hinweis"]
    assert report["lauf"]["status"] == "blockiert"
    assert "blockiert" in (folder / "zusammenfassung.md").read_text(encoding="utf-8")
    # Nach der Freigabe läuft der Worker nicht weiter und überschreibt nichts.
    threading.Event().wait(0.2)
    again = json.loads((folder / "bericht.json").read_text(encoding="utf-8"))
    assert status(again)["P1-6-hardware"] == "blockiert"
    assert "P1-6-scankopf" in status(again)


def test_strg_c_schreibt_teilbericht(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    h = make_harness(tmp_path)
    release = threading.Event()
    h.world.hang[("Hardware", "FrontEnd")] = release
    real_join = threading.Thread.join
    calls = {"n": 0}

    def join(self: threading.Thread, timeout: float | None = None) -> None:
        calls["n"] += 1
        if calls["n"] > 3:
            raise KeyboardInterrupt
        real_join(self, 0.2)

    monkeypatch.setattr(threading.Thread, "join", join)
    try:
        code, report, _ = run(tmp_path, h, "--stufe", "1", "--timeout-s", "50")
    finally:
        release.set()
    assert code == erkundung.EXIT_INTERRUPTED
    assert report["lauf"]["status"] == "abgebrochen"
    assert h.exits == [erkundung.EXIT_INTERRUPTED]


def test_verweigerter_zugriff_ist_befund_und_exit_code_1(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    # Ein (absichtlich fehlerhafter) Prüfpunkt greift auf ein nicht freigegebenes Mitglied zu.
    def bad_step(cx: erkundung.StepContext) -> None:
        app = cx.need("app", "x")
        cx.rd("Name", lambda: app.Name)

    monkeypatch.setattr(
        erkundung,
        "build_steps",
        lambda stufe, with_file: [
            erkundung.Step("P1-5-verbinden", "1", "v", "x", erkundung._step_verbinden),
            erkundung.Step("X-bad", "1", "bad", "x", bad_step),
        ],
    )
    h = make_harness(tmp_path)
    code, report, folder = run(tmp_path, h, "--stufe", "1")
    assert code == erkundung.EXIT_DENIED
    assert [d["pfad"] for d in report["verweigert"]] == ["Application.Name"]
    assert status(report)["X-bad"] == "fehler"
    assert "ACHTUNG: Zugriff verweigert" in (folder / "zusammenfassung.md").read_text(
        encoding="utf-8"
    )


def test_unbekannte_progid_wird_verweigert(tmp_path: Path) -> None:
    h = make_harness(tmp_path)
    runner = _runner(tmp_path, h)
    cx = erkundung.StepContext(runner, erkundung.Step("T", "1", "t", "x", lambda cx: None))
    with pytest.raises(PermissionError):
        cx.dispatch("PSV.Application")
    assert runner.proxy_ctx.snapshot()[1][0]["pfad"] == "Dispatch.PSV.Application"


def _runner(tmp_path: Path, h: Harness) -> erkundung.Runner:
    args = erkundung.build_parser().parse_args([])
    out = tmp_path / "r"
    out.mkdir()
    return erkundung.Runner(
        h.env, args, out, erkundung.Redactor("", False), erkundung.ProxyContext(), 0.01
    )


def test_rd_reicht_permissionerror_durch_und_need_ueberspringt(tmp_path: Path) -> None:
    runner = _runner(tmp_path, make_harness(tmp_path))
    cx = erkundung.StepContext(runner, erkundung.Step("T", "1", "t", "x", lambda cx: None))

    def deny() -> None:
        raise PermissionError("x")

    with pytest.raises(PermissionError):
        cx.rd("a", deny)
    with pytest.raises(erkundung.Skipped):
        cx.need("nichts", "Test")
    assert isinstance(cx.skip("x"), erkundung.Skipped)


# --- Stufe 1b -------------------------------------------------------------------------


def _datei(tmp_path: Path) -> Path:
    path = tmp_path / "Example.svd"
    path.write_bytes(b"\x00svd-inhalt" * 100)
    return path


def test_k7_stufe1b_liest_nur_und_laesst_datei_unveraendert(tmp_path: Path) -> None:
    h = make_harness(tmp_path)
    datei = _datei(tmp_path)
    digest = hashlib.sha256(datei.read_bytes()).hexdigest()
    mtime = datei.stat().st_mtime_ns
    code, report, _ = run(tmp_path, h, "--stufe", "1", "--datei", str(datei))
    assert code == 0
    st = status(report)
    assert [st[i] for i in ("P1-10-oeffnen", "P1-10-struktur", "P1-10-daten", "P1-10-schliessen")] \
        == ["ok"] * 4  # fmt: skip
    assert datei.stat().st_mtime_ns == mtime
    assert hashlib.sha256(datei.read_bytes()).hexdigest() == digest
    assert report["dateien"]["unveraendert"] is True
    assert report["dateien"]["eingabedatei_vorher"]["sha256"] == digest
    # ReadOnly = True kommt vor Open; nichts anderes wird gesetzt.
    pf_log = [(n, op) for k, n, op in h.world.log if k == "PolyFile"]
    assert pf_log.index(("ReadOnly", "set")) < pf_log.index(("Open", "call"))
    assert [(k, n) for k, n, op in h.world.log if op == "set"] == [("PolyFile", "ReadOnly")]
    assert pf_log[-1] == ("IsOpen", "get") and ("Close", "call") in pf_log
    daten = entry(report, "P1-10-daten")["werte"]
    assert daten["GetData_laenge"] == 16
    assert daten["GetData_erste_werte"] == [0.0, 1.0, 2.0, 3.0, 4.0, 5.0]
    assert daten["XAxis_Werte"]["MaxCount"] == 8
    assert daten["GetMidX"] == {"0": 1.25, "1": 2.5, "7": 10.0}
    derived = daten["abgeleitet"]
    assert derived["delta_f_aus_achse_hz"] == pytest.approx(1.25, rel=1e-12)
    assert derived["mid0_durch_delta_f"] == pytest.approx(1.0, rel=1e-12)
    assert derived["datenlaenge_durch_maxcount"] == pytest.approx(2.0, rel=1e-12)
    assert derived["rel_abw_delta_f_zu_SampleResolution"] == pytest.approx(0.0, abs=1e-12)
    assert derived["Bandwidth_durch_Lines_hz"] == pytest.approx(1.25, rel=1e-12)
    struktur = entry(report, "P1-10-struktur")["werte"]
    assert [d.get("gewaehlt_fuer_daten") for d in struktur["domaenen"]] == [None, True]
    assert [k["Name"] for k in struktur["kanaele"]] == [
        "Vib X",
        "Vib Y",
        "Vib Z",
    ]
    assert struktur["kanaele"][0]["signale"][0]["YAxis_Werte"]["Unit"] == "m/s"


def test_stufe1b_ohne_psv_laeuft_trotzdem(tmp_path: Path) -> None:
    h = make_harness(tmp_path, running=False)
    datei = _datei(tmp_path)
    _, report, _ = run(tmp_path, h, "--stufe", "1", "--datei", str(datei))
    st = status(report)
    assert st["P1-5-verbinden"] == "uebersprungen"
    assert st["P1-10-oeffnen"] == "ok"
    assert st["P1-10-schliessen"] == "ok"
    derived = entry(report, "P1-10-daten")["werte"]["abgeleitet"]
    assert "rel_abw_delta_f_zu_SampleResolution" not in derived  # keine Stufe-1-Werte


def test_stufe1b_sharing_violation_wird_klar_gemeldet(tmp_path: Path) -> None:
    h = make_harness(tmp_path)
    h.world.fail[("PolyFile", "Open")] = FakeComError("Sharing violation")
    datei = _datei(tmp_path)
    _, report, _ = run(tmp_path, h, "--stufe", "1", "--datei", str(datei))
    st = status(report)
    assert st["P1-10-oeffnen"] == "fehler"
    assert (
        "Sharing Violation" in entry(report, "P1-10-oeffnen")["hinweis"]
        or "Sharing" in (entry(report, "P1-10-oeffnen")["exception"]["meldung"])
    )
    assert st["P1-10-struktur"] == "uebersprungen"
    assert st["P1-10-daten"] == "uebersprungen"
    assert st["P1-10-schliessen"] == "uebersprungen"
    assert report["dateien"]["unveraendert"] is True


def test_veraenderte_eingabedatei_wird_gemeldet(tmp_path: Path) -> None:
    h = make_harness(tmp_path)
    datei = _datei(tmp_path)
    original_dispatch = h.env.dispatch

    def touching(progid: str) -> Any:
        if progid == "PolyFile.PolyFile":
            datei.write_bytes(b"veraendert")
        return original_dispatch(progid)

    h.env.dispatch = touching
    _, report, folder = run(tmp_path, h, "--stufe", "1", "--datei", str(datei))
    assert report["dateien"]["unveraendert"] is False
    assert "verändert" in (folder / "konsole.log").read_text(encoding="utf-8")


def test_stufe1b_ohne_daten_und_ohne_display(tmp_path: Path) -> None:
    h = make_harness(tmp_path)
    h.world.fail[("DataPoints", "Count")] = FakeComError("keine Daten")
    datei = _datei(tmp_path)
    _, report, _ = run(tmp_path, h, "--stufe", "1", "--datei", str(datei))
    assert status(report)["P1-10-daten"] in ("fehler", "uebersprungen")
    assert status(report)["P1-10-schliessen"] == "ok"


# --- Kommandozeile --------------------------------------------------------------------


@pytest.mark.parametrize(
    "argv",
    [
        ["--stufe", "0", "--datei", "x"],
        ["--stufe", "0", "--start-psv"],
        ["--stufe", "1", "--datei", "/gibt/es/nicht.svd"],
        ["--stufe", "1", "--timeout-s", "0"],
        ["--stufe", "1", "--max-punkte", "0"],
        ["--stufe", "2"],
    ],
)
def test_aufruffehler_enden_mit_exit_2_ohne_ausgabe(tmp_path: Path, argv: list[str]) -> None:
    h = make_harness(tmp_path)
    with pytest.raises(SystemExit) as exc:
        main([*argv, "--out", str(tmp_path / "out")], env=h.env)
    assert exc.value.code == 2
    assert not (tmp_path / "out").exists()
    assert h.world.log == []


def test_version_und_hilfe(capsys: pytest.CaptureFixture[str]) -> None:
    with pytest.raises(SystemExit) as exc:
        main(["--version"])
    assert exc.value.code == 0
    assert erkundung.SCRIPT_VERSION in capsys.readouterr().out


# --- Bericht, Datenschutz, Ablage -----------------------------------------------------


def test_k6_bericht_schema_und_zusammenfassung_gleiche_ids(tmp_path: Path) -> None:
    h = make_harness(tmp_path)
    datei = _datei(tmp_path)
    _, report, folder = run(tmp_path, h, "--stufe", "1", "--datei", str(datei))
    for key in ("schema_version", "skript_version", "skript_sha256", "zeitstempel_lokal",
                "zeitstempel_utc", "rechnername", "kommandozeile", "umgebung", "pruefpunkte",
                "whitelist_aufrufe", "verweigert", "dateien", "abweichungen", "parameter",
                "lauf", "stufen", "benutzername_entfernt"):  # fmt: skip
        assert key in report, key
    assert report["schema_version"] == erkundung.SCHEMA_VERSION
    assert report["zeitstempel_lokal"] == "2026-10-24T09:30:15+02:00"
    assert report["zeitstempel_utc"] == "2026-10-24T07:30:15+00:00"
    assert report["stufen"] == ["0", "1", "1b"]
    assert report["rechnername"] == "MESS-PC"
    assert (
        report["skript_sha256"] == hashlib.sha256(Path(erkundung.__file__).read_bytes()).hexdigest()
    )
    for p in report["pruefpunkte"]:
        for key in ("id", "stufe", "status", "werte", "dauer_s", "exception", "beleg_ref"):
            assert key in p, (p["id"], key)
        assert p["status"] in ("ok", "fehler", "uebersprungen", "blockiert")
    summary = (folder / "zusammenfassung.md").read_text(encoding="utf-8")
    table_ids = [line.split("|")[1].strip() for line in summary.splitlines()
                 if line.startswith("| P")]  # fmt: skip
    assert table_ids == [p["id"] for p in report["pruefpunkte"]]
    assert "am Gerät unbestätigt" in summary
    assert "| P1-10-daten | 1b | ok |" in summary
    # Strenges JSON: kein NaN/Infinity.
    json.loads((folder / "bericht.json").read_text(encoding="utf-8"),
               parse_constant=lambda c: (_ for _ in ()).throw(ValueError(c)))  # fmt: skip


def test_bericht_wird_nach_jedem_punkt_geschrieben(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    sizes: list[int] = []
    original = erkundung.Runner.flush

    def spy(self: erkundung.Runner) -> None:
        original(self)
        sizes.append(
            len(json.loads((self.out_dir / "bericht.json").read_text("utf-8"))["pruefpunkte"])
        )

    monkeypatch.setattr(erkundung.Runner, "flush", spy)
    run(tmp_path, make_harness(tmp_path), "--stufe", "0")
    assert sizes[0] == 0
    assert sizes[1 : len(STUFE0_IDS) + 1] == list(range(1, len(STUFE0_IDS) + 1))


def test_k7_ausgabeordner_wird_nie_ueberschrieben(tmp_path: Path) -> None:
    h = make_harness(tmp_path)
    _, _, first = run(tmp_path, h)
    marker = first / "bericht.json"
    content = marker.read_text(encoding="utf-8")
    _, _, second = run(tmp_path, h)
    assert first != second
    assert second.name == first.name + "_2"
    assert marker.read_text(encoding="utf-8") == content
    assert first.name == "erkundung_MESS-PC_2026-10-24_093015"


def test_k9_benutzername_wird_standardmaessig_entfernt(tmp_path: Path) -> None:
    server = "C:\\Users\\tester7\\AppData\\psv.exe"
    h = make_harness(tmp_path, server_path=server, hostname="TESTER7-PC", username="tester7")
    _, report, folder = run(tmp_path, h, "--stufe", "0")
    text = "".join(
        (folder / n).read_text(encoding="utf-8")
        for n in ("bericht.json", "zusammenfassung.md", "konsole.log", "registry.reg.txt")
    )
    assert "tester7" not in text.lower().replace("tester7-pc", "")
    assert "Users\\\\<user>\\\\AppData" in (folder / "bericht.json").read_text(encoding="utf-8")
    assert report["rechnername"] == "TESTER7-PC"  # Rechnername bleibt im Klartext
    assert report["benutzername_entfernt"] is True
    # --keep-user hebt es auf.
    (tmp_path / "k").mkdir()
    h2 = make_harness(tmp_path / "k", server_path=server, username="tester7")
    _, report2, folder2 = run(tmp_path / "k", h2, "--stufe", "0", "--keep-user")
    assert "Users\\\\tester7" in (folder2 / "bericht.json").read_text(encoding="utf-8")
    assert report2["benutzername_entfernt"] is False


def test_k11_keine_gefaehrlichen_aufrufe_und_schreiben_nur_im_ausgabeordner(
    tmp_path: Path,
) -> None:
    source = Path(erkundung.__file__).read_text(encoding="utf-8")
    for needle in ("eval(", "exec(", "pickle", "import socket", "urllib", "http.client",
                   "requests", "shell=True", "os.system"):  # fmt: skip
        assert needle not in source, needle
    h = make_harness(tmp_path)
    before = {p.name for p in tmp_path.iterdir()}
    run(tmp_path, h, "--stufe", "1")
    new = {p.name for p in tmp_path.iterdir()} - before
    assert new == {"out"}
    assert [p.name for p in (tmp_path / "out").iterdir()] == ["erkundung_MESS-PC_2026-10-24_093015"]
