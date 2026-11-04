"""Hintergrundaufträge (P-AUSW T1.4): Ausführer, Fehlerkanal, Teile, Abbruch.

Zwei Ebenen: Der Rumpf des Prozesses (``_worker``) und der Empfang laufen hier in einem
Thread bzw. mit echten Pipes im Testprozess (nur so wird der Code von der Abdeckung erfasst);
die echten ``spawn``-Prozesse (Spawn, Pipe, ``terminate``) prüfen die Tests mit
``ProzessAusfuehrer`` darunter.
"""

from __future__ import annotations

import multiprocessing
import os
import pickle
import signal
import sys
import threading
import time
from collections.abc import Callable
from multiprocessing.connection import Connection
from pathlib import Path
from typing import Any

import hg_hilfsjobs as jobs
import numpy as np
import pytest

from ldv_automation import hintergrund as hg
from ldv_automation.hintergrund import (
    TEIL_BYTES,
    Auftrag,
    AuftragAbgebrochen,
    AuftragFehler,
    DirektAusfuehrer,
    ProzessAusfuehrer,
)

FRIST_S = 60.0


def warte(auftrag: Auftrag, frist_s: float = FRIST_S) -> None:
    """Wartet wie die Oberfläche: nicht blockierend abfragen, dazwischen schlafen."""
    ende = time.monotonic() + frist_s
    while not auftrag.fertig():
        assert time.monotonic() < ende, "Auftrag nicht rechtzeitig fertig"
        time.sleep(0.005)


# --- DirektAusfuehrer ------------------------------------------------------------------------


def test_direkt_liefert_ergebnis_sofort() -> None:
    auftrag = DirektAusfuehrer().starte(jobs.verdopple, 21)
    assert auftrag.fertig() is True
    assert auftrag.ergebnis() == 42


def test_direkt_fehler_mit_typ_text_und_ablaufverfolgung() -> None:
    auftrag = DirektAusfuehrer().starte(jobs.wirf, "kaputt")
    assert auftrag.fertig() is True
    with pytest.raises(AuftragFehler, match="kaputt") as info:
        auftrag.ergebnis()
    assert info.value.typ == "ValueError"
    assert info.value.meldung == "kaputt"
    assert "wirf" in info.value.traceback_text


def test_direkt_abbrechen_und_beende() -> None:
    ausfuehrer = DirektAusfuehrer()
    auftrag = ausfuehrer.starte(jobs.verdopple, 1)
    auftrag.abbrechen()
    with pytest.raises(AuftragAbgebrochen):
        auftrag.ergebnis()
    ausfuehrer.beende()  # nichts zu tun, wirft nicht


def test_importiere_ist_ein_leer_auftrag() -> None:
    assert DirektAusfuehrer().starte(hg.importiere, ("json", "ldv_automation")).ergebnis() is None
    fehler = DirektAusfuehrer().starte(hg.importiere, ("gibt_es_nicht_xyz",))
    with pytest.raises(AuftragFehler) as info:
        fehler.ergebnis()
    assert info.value.typ == "ModuleNotFoundError"


# --- Worker und Empfang im Testprozess (Thread) -----------------------------------------------


def _lauf_im_thread(
    funktion: Callable[..., Any],
    argumente: tuple[Any, ...],
    teil_bytes: int,
    monkeypatch: pytest.MonkeyPatch,
) -> hg._ProzessAuftrag:
    """Führt ``_worker`` in einem Thread aus und gibt den Empfangsauftrag zurück."""
    # signal.signal darf nur im Hauptthread laufen und würde pytest das Strg+C nehmen
    monkeypatch.setattr(signal, "signal", lambda *_: None)
    empfang, senden = multiprocessing.get_context("spawn").Pipe(duplex=False)
    worker = threading.Thread(
        target=hg._worker, args=(senden, funktion, argumente, teil_bytes), daemon=True
    )
    worker.start()
    auftrag = hg._ProzessAuftrag(empfang, _FremderProzess(worker))
    warte(auftrag)
    worker.join(5)
    return auftrag


class _FremderProzess:
    """Stellt einen Thread als Prozess dar (``exitcode``, ``join``, ``terminate``)."""

    def __init__(self, thread: threading.Thread) -> None:
        self._thread = thread
        self.beendet = False

    @property
    def exitcode(self) -> int | None:
        return None if self._thread.is_alive() else 0

    def join(self, timeout: float | None = None) -> None:
        self._thread.join(timeout)

    def terminate(self) -> None:
        self.beendet = True


@pytest.mark.parametrize("teil_bytes", [1, 7, 4096, TEIL_BYTES])
def test_worker_ergebnis_mit_feldern_in_teilen_ist_bitgleich(
    monkeypatch: pytest.MonkeyPatch, teil_bytes: int
) -> None:
    n = 3000 if teil_bytes < 100 else 40_000
    auftrag = _lauf_im_thread(jobs.felder, (n,), teil_bytes, monkeypatch)
    erg = auftrag.ergebnis()
    soll = jobs.felder(n)
    assert set(erg) == set(soll)
    for schluessel in ("gross", "komplex", "leer"):
        np.testing.assert_array_equal(erg[schluessel], soll[schluessel])
        assert erg[schluessel].dtype == soll[schluessel].dtype
    assert erg["zahl"] == 2.5 and erg["text"] == "ü"


def test_worker_ergebnis_ohne_felder_und_none(monkeypatch: pytest.MonkeyPatch) -> None:
    assert _lauf_im_thread(jobs.verdopple, (4,), 16, monkeypatch).ergebnis() == 8
    assert _lauf_im_thread(jobs.nichts, (), 16, monkeypatch).ergebnis() is None


def test_worker_fehler_kommt_als_auftragsfehler(monkeypatch: pytest.MonkeyPatch) -> None:
    auftrag = _lauf_im_thread(jobs.wirf, ("mit\ttab",), 1024, monkeypatch)
    with pytest.raises(AuftragFehler, match="mit\ttab") as info:
        auftrag.ergebnis()
    assert (info.value.typ, info.value.meldung) == ("ValueError", "mit\ttab")
    assert "wirf" in info.value.traceback_text


def test_worker_nicht_picklebares_ergebnis_ist_ein_fehler(monkeypatch: pytest.MonkeyPatch) -> None:
    auftrag = _lauf_im_thread(jobs.nicht_picklebar, (), 1024, monkeypatch)
    with pytest.raises(AuftragFehler) as info:
        auftrag.ergebnis()
    assert info.value.typ in {"PicklingError", "AttributeError"}  # je nach Python-Detail


def test_worker_ergebnis_das_beim_entpacken_scheitert(monkeypatch: pytest.MonkeyPatch) -> None:
    auftrag = _lauf_im_thread(jobs.boeses_ergebnis, (), 1024, monkeypatch)
    with pytest.raises(AuftragFehler, match="Ergebnis nicht lesbar: beim Entpacken") as info:
        auftrag.ergebnis()
    assert info.value.typ == "ValueError"


def test_worker_setzt_sigint_auf_ignorieren(monkeypatch: pytest.MonkeyPatch) -> None:
    aufrufe: list[tuple[Any, ...]] = []
    monkeypatch.setattr(signal, "signal", lambda *a: aufrufe.append(a))
    empfang, senden = multiprocessing.get_context("spawn").Pipe(duplex=False)
    hg._worker(senden, jobs.nichts, (), 1024)  # kleine Nachrichten passen in den Pipe-Puffer
    assert aufrufe == [(signal.SIGINT, signal.SIG_IGN)]
    empfang.close()


def test_sende_teile_nachrichten_hoechstens_teil_bytes() -> None:
    class Aufnahme:
        def __init__(self) -> None:
            self.laengen: list[int] = []

        def send_bytes(self, daten: memoryview) -> None:
            self.laengen.append(len(daten))

    a = Aufnahme()
    hg._sende_teile(a, memoryview(bytes(10)), 4)  # type: ignore[arg-type]
    assert a.laengen == [4, 4, 2]
    a = Aufnahme()
    hg._sende_teile(a, memoryview(bytes(0)), 4)  # type: ignore[arg-type]
    assert a.laengen == []  # leeres Stück: keine Nachricht
    a = Aufnahme()
    hg._sende_teile(a, memoryview(bytes(2 * TEIL_BYTES + 1)), TEIL_BYTES)  # type: ignore[arg-type]
    assert a.laengen == [TEIL_BYTES, TEIL_BYTES, 1]


# --- Empfangszustände mit echten Pipes (ohne Worker) ------------------------------------------


class _ProzessAttrappe:
    def __init__(self, exitcode: int | None = None) -> None:
        self.exitcode = exitcode
        self.aufrufe: list[str] = []

    def join(self, timeout: float | None = None) -> None:
        self.aufrufe.append("join")

    def terminate(self) -> None:
        self.aufrufe.append("terminate")
        self.exitcode = -15

    def kill(self) -> None:
        self.aufrufe.append("kill")
        self.exitcode = -9


def _pipe_paar() -> tuple[Connection, Connection]:
    return multiprocessing.get_context("spawn").Pipe(duplex=False)


def test_empfang_unerwartete_nachricht() -> None:
    empfang, senden = _pipe_paar()
    auftrag = hg._ProzessAuftrag(empfang, _ProzessAttrappe())
    senden.send_bytes(b"?was")
    assert auftrag.fertig() is True
    with pytest.raises(AuftragFehler, match="unerwartete Nachricht"):
        auftrag.ergebnis()


def test_empfang_fehlernachricht_ohne_ablaufverfolgung() -> None:
    empfang, senden = _pipe_paar()
    auftrag = hg._ProzessAuftrag(empfang, _ProzessAttrappe())
    senden.send_bytes(b"F" + pickle.dumps(("KeyError", "fehlt", ""), protocol=5))
    assert auftrag.fertig() is True
    with pytest.raises(AuftragFehler, match="fehlt") as info:
        auftrag.ergebnis()
    assert (info.value.typ, info.value.traceback_text) == ("KeyError", "")


@pytest.mark.parametrize("rahmen", [b"\x80kaputt", pickle.dumps((1, 2, 3)), pickle.dumps("x")])
def test_empfang_ungueltiger_fehlerrahmen_gibt_ersatzmeldung(rahmen: bytes) -> None:
    empfang, senden = _pipe_paar()
    auftrag = hg._ProzessAuftrag(empfang, _ProzessAttrappe())
    senden.send_bytes(b"F" + rahmen)
    assert auftrag.fertig() is True
    with pytest.raises(AuftragFehler, match="nicht lesbar"):
        auftrag.ergebnis()


def test_empfang_exitcode_unbekannt_statt_none() -> None:
    empfang, senden = _pipe_paar()
    auftrag = hg._ProzessAuftrag(empfang, _ProzessAttrappe(exitcode=None))
    senden.close()
    assert auftrag.fertig() is True
    with pytest.raises(AuftragFehler, match=r"\(Exitcode unbekannt\)") as info:
        auftrag.ergebnis()
    assert "None" not in info.value.meldung


def test_fehlerrahmen_mit_nicht_darstellbarem_str_hat_ersatztext() -> None:
    class KaputtError(Exception):
        def __str__(self) -> str:
            raise RuntimeError("str kaputt")

    try:
        raise KaputtError
    except KaputtError as exc:
        typ, meldung, _ = hg._fehlerrahmen_lesen(hg._fehlerrahmen(exc))
    assert typ == "KaputtError" and "nicht darstellbar" in meldung


def test_abbrechen_legt_kill_nach_wenn_terminate_nicht_reicht() -> None:
    class Stur(_ProzessAttrappe):
        def terminate(self) -> None:
            self.aufrufe.append("terminate")  # Prozess ignoriert SIGTERM

    empfang, senden = _pipe_paar()
    prozess = Stur(exitcode=None)
    auftrag = hg._ProzessAuftrag(empfang, prozess)
    auftrag.abbrechen()
    assert prozess.aufrufe == ["terminate", "join", "kill", "join"]
    senden.close()


def test_abbrechen_ohne_kill_wenn_terminate_wirkt() -> None:
    empfang, senden = _pipe_paar()
    prozess = _ProzessAttrappe(exitcode=None)
    hg._ProzessAuftrag(empfang, prozess).abbrechen()
    assert prozess.aufrufe == ["terminate", "join"]
    senden.close()


def test_empfang_pipe_zu_ohne_ergebnis_meldet_exitcode() -> None:
    empfang, senden = _pipe_paar()
    auftrag = hg._ProzessAuftrag(empfang, _ProzessAttrappe(exitcode=7))
    senden.close()
    assert auftrag.fertig() is True
    with pytest.raises(AuftragFehler, match=r"unerwartet beendet \(Exitcode 7\)"):
        auftrag.ergebnis()


def test_empfang_ohne_daten_ist_nicht_fertig_und_ergebnis_wirft() -> None:
    empfang, senden = _pipe_paar()
    auftrag = hg._ProzessAuftrag(empfang, _ProzessAttrappe())
    assert auftrag.fertig() is False
    with pytest.raises(RuntimeError, match="noch nicht fertig"):
        auftrag.ergebnis()
    auftrag.abbrechen()
    assert auftrag.fertig() is True  # abgebrochen gilt als fertig
    with pytest.raises(AuftragAbgebrochen):
        auftrag.ergebnis()
    auftrag.abbrechen()  # zweites Mal wirkungslos
    senden.close()


def test_empfang_abfrage_nimmt_hoechstens_den_zeitanteil_in_anspruch(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Mit vielen kleinen Teilen kehrt ``fertig`` nach dem Zeitanteil zurück (nicht fertig)."""
    monkeypatch.setattr(hg, "ZEITANTEIL_S", 0.0)  # sofort nach dem ersten Teil zurück
    empfang, senden = _pipe_paar()
    auftrag = hg._ProzessAuftrag(empfang, _ProzessAttrappe())
    senden.send_bytes(b"K" + (2).to_bytes(4, "little") + (3).to_bytes(8, "little") * 2)
    senden.send_bytes(b"abc")
    assert auftrag.fertig() is False  # Kopf empfangen, danach Zeitanteil aufgebraucht
    assert auftrag.fertig() is False  # erstes Stück (3 Byte): noch keine Pickle-Daten
    senden.close()


def test_aufraeumen_beendet_haengende_prozesse_nach_der_frist(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    empfang, senden = _pipe_paar()
    prozess = _ProzessAttrappe(exitcode=None)
    auftrag = hg._ProzessAuftrag(empfang, prozess)
    senden.send_bytes(b"?")
    assert auftrag.fertig() is True
    assert auftrag.aufraeumen() is False  # läuft noch, Frist nicht abgelaufen
    assert prozess.aufrufe == []
    monkeypatch.setattr(hg, "_ENDE_WARTEN_S", -1.0)
    assert auftrag.aufraeumen() is False  # Frist abgelaufen: terminate
    assert prozess.aufrufe == ["terminate"]
    assert auftrag.aufraeumen() is True  # jetzt beendet und eingesammelt
    assert prozess.aufrufe[-1] == "join"


# --- ProzessAusfuehrer: echte spawn-Prozesse -------------------------------------------------


@pytest.fixture
def ausfuehrer() -> Any:
    a = ProzessAusfuehrer()
    yield a
    a.beende()


def test_prozess_ergebnis_aus_anderem_prozess(ausfuehrer: ProzessAusfuehrer) -> None:
    auftrag = ausfuehrer.starte(jobs.kennung)
    warte(auftrag)
    pid = auftrag.ergebnis()
    assert isinstance(pid, int) and pid != os.getpid()
    assert ausfuehrer.starte(jobs.verdopple, 5).fertig() in (True, False)  # kehrt sofort zurück


def test_prozess_grosses_ergebnis_in_kleinen_teilen() -> None:
    a = ProzessAusfuehrer(teil_bytes=10_000)  # 400 kB Feld → etwa 40 Teile
    try:
        auftrag = a.starte(jobs.felder, 50_000)
        warte(auftrag)
        erg = auftrag.ergebnis()
        np.testing.assert_array_equal(erg["gross"], jobs.felder(50_000)["gross"])
        assert erg["leer"].shape == (0,) and erg["text"] == "ü"
    finally:
        a.beende()


def test_prozess_fehler_im_auftrag(ausfuehrer: ProzessAusfuehrer) -> None:
    auftrag = ausfuehrer.starte(jobs.wirf, "Datei x.svd fehlt")
    warte(auftrag)
    with pytest.raises(AuftragFehler, match=r"Datei x\.svd fehlt") as info:
        auftrag.ergebnis()
    assert info.value.typ == "ValueError" and "wirf" in info.value.traceback_text


def test_prozess_absturz_ohne_ergebnis(ausfuehrer: ProzessAusfuehrer) -> None:
    auftrag = ausfuehrer.starte(jobs.beende_hart, 7)
    warte(auftrag)
    with pytest.raises(AuftragFehler, match=r"unerwartet beendet \(Exitcode 7\)"):
        auftrag.ergebnis()


def test_prozess_abbrechen_beendet_sofort_ohne_zu_warten(ausfuehrer: ProzessAusfuehrer) -> None:
    auftrag = ausfuehrer.starte(jobs.schlafe, 60.0)
    time.sleep(0.3)  # Prozess ist gestartet
    assert auftrag.fertig() is False  # nicht blockierend, nichts da
    beginn = time.perf_counter()
    auftrag.abbrechen()
    dauer = time.perf_counter() - beginn
    assert dauer < 5.0  # nicht die 60 s des Auftrags (gemessen: ~2 ms; Spielraum für langsame CI)
    assert auftrag.fertig() is True
    with pytest.raises(AuftragAbgebrochen):
        auftrag.ergebnis()


def test_prozess_beende_bricht_alle_laufenden_auftraege_ab() -> None:
    a = ProzessAusfuehrer()
    auftraege = [a.starte(jobs.schlafe, 60.0) for _ in range(2)]
    time.sleep(0.2)
    beginn = time.perf_counter()
    a.beende()
    assert time.perf_counter() - beginn < 10.0
    for auftrag in auftraege:
        assert auftrag.fertig() is True
        with pytest.raises(AuftragAbgebrochen):
            auftrag.ergebnis()


def test_prozess_fertige_auftraege_werden_aufgeraeumt(ausfuehrer: ProzessAusfuehrer) -> None:
    erster = ausfuehrer.starte(jobs.verdopple, 1)
    warte(erster)
    assert erster.ergebnis() == 2
    assert isinstance(erster, hg._ProzessAuftrag)
    ende = time.monotonic() + 30
    while not erster.aufraeumen():  # Prozess endet kurz nach dem Ergebnis
        assert time.monotonic() < ende
        time.sleep(0.02)
    zweiter = ausfuehrer.starte(jobs.nichts)  # der Start räumt den beendeten Auftrag weg
    assert erster not in ausfuehrer._laufend
    assert zweiter in ausfuehrer._laufend
    warte(zweiter)


def test_prozess_teil_bytes_wird_geprueft() -> None:
    for falsch in (0, -1, TEIL_BYTES + 1):
        with pytest.raises(ValueError, match="teil_bytes"):
            ProzessAusfuehrer(teil_bytes=falsch)
    assert ProzessAusfuehrer(teil_bytes=TEIL_BYTES) is not None


def test_prozess_oberflaeche_bleibt_waehrend_langem_auftrag_bedienbar(
    ausfuehrer: ProzessAusfuehrer,
) -> None:
    """UI-15 (Kern): ``fertig()`` kehrt sofort zurück, solange der Auftrag läuft."""
    auftrag = ausfuehrer.starte(jobs.schlafe, 1.0)
    laengste = 0.0
    abfragen = 0
    ende = time.monotonic() + 0.6
    while time.monotonic() < ende:
        t0 = time.perf_counter()
        assert auftrag.fertig() is False
        laengste = max(laengste, time.perf_counter() - t0)
        abfragen += 1
        time.sleep(0.01)
    assert abfragen > 10
    assert laengste < 0.2  # gemessen < 1 ms; großzügig für langsame Rechner
    auftrag.abbrechen()


# --- Fehlerkanal mit beliebigem Text (echter Prozess) ----------------------------------------


@pytest.mark.parametrize(
    "text",
    ["/x/\udcff.svd: Datei nicht lesbar", "a\x00b", "a\x00b\x00c\x00d", "ü – 日本 \U0001f600", ""],
)
def test_prozess_fehlertext_beliebiger_inhalt_kommt_vollstaendig_an(
    ausfuehrer: ProzessAusfuehrer, text: str
) -> None:
    auftrag = ausfuehrer.starte(jobs.wirf, text)
    warte(auftrag)
    with pytest.raises(AuftragFehler) as info:
        auftrag.ergebnis()
    assert info.value.typ == "ValueError"
    assert info.value.meldung == text
    assert "wirf" in info.value.traceback_text


@pytest.mark.skipif(sys.platform == "win32", reason="SIGTERM ist unter Windows nicht abfangbar")
def test_prozess_abbrechen_beendet_auch_prozess_der_sigterm_ignoriert(
    ausfuehrer: ProzessAusfuehrer, tmp_path: Path
) -> None:
    """Der Auftrag ignoriert SIGTERM; ``abbrechen`` legt nach der Frist SIGKILL nach.

    Unter Windows ist ``terminate`` bereits ``TerminateProcess`` (hart); dort nicht prüfbar
    und als Risiko benannt (Messrechner).
    """
    bereit = tmp_path / "bereit"
    auftrag = ausfuehrer.starte(jobs.ignoriere_sigterm_und_schlafe, 60.0, str(bereit))
    ende = time.monotonic() + FRIST_S
    while not bereit.exists():  # Marke: SIGTERM ist im Worker bereits ignoriert
        assert time.monotonic() < ende, "Worker nicht rechtzeitig bereit"
        time.sleep(0.01)
    beginn = time.perf_counter()
    auftrag.abbrechen()
    dauer = time.perf_counter() - beginn
    assert dauer < hg._TERMINATE_WARTEN_S + hg._KILL_WARTEN_S + 2.0  # Frist + Spielraum
    assert dauer >= hg._TERMINATE_WARTEN_S * 0.9  # die Frist wurde abgewartet, dann kill
    assert auftrag.fertig() is True
    with pytest.raises(AuftragAbgebrochen):
        auftrag.ergebnis()
