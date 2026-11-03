"""Hintergrundaufträge der Oberfläche in einem eigenen Prozess (P-AUSW T1.4).

Rechnungen wie das Lesen einer ``.svd``-Datei (0,1 bis 0,8 s) oder die Plausibilitätsprüfung
(8 bis 13 s) dürfen die Oberfläche nicht einfrieren (UI-15). Ein Qt-Thread scheidet aus
(Importzeit, GIL, nicht abbrechbar); jeder Auftrag läuft deshalb in einem eigenen
Python-Prozess (``spawn``, plattformgleich zu Windows) und liefert sein Ergebnis über eine
``Pipe``.

Gemessene Eigenschaften (Linux, 4 Kerne, Beispieldatei; am Messrechner nicht bestätigt, siehe
``tools/auswertung/zeiten_messen.py``): ``terminate`` dauert etwa 2 ms; ein einzelnes
``recv`` von höchstens 4 MiB dauert 13 bis 17 ms; die Gesamtübertragung von 48 MB dauert
134 bis 313 ms. Große NumPy-Felder gehen deshalb **ohne Kopie am Ende** in Teilen über die
Pipe (Pickle-Protokoll 5 mit getrennten Puffern), die Oberfläche nimmt je Abfrage nur einen
kleinen Zeitanteil.

Dieses Modul importiert nur die Standardbibliothek (Importtest) und weder NumPy noch Qt: Es
muss im frischen Worker schnell geladen sein, und die Aufträge selbst (z. B.
:mod:`ldv_automation.auswertung.jobs`) werden ihm als Funktionen übergeben.

Ablauf::

    ausfuehrer = ProzessAusfuehrer()
    auftrag = ausfuehrer.starte(lese_job, "datei.svd")   # Funktion auf Modulebene, kein Lambda
    ...
    if auftrag.fertig():          # nicht blockierend, z. B. alle 50 ms aus einem QTimer
        daten = auftrag.ergebnis()  # AuftragFehler, wenn der Auftrag eine Ausnahme warf
    auftrag.abbrechen()           # beendet den Prozess sofort (terminate)

``DirektAusfuehrer`` führt den Auftrag synchron im aufrufenden Prozess aus (Tests ohne Prozess).
"""

from __future__ import annotations

import importlib
import multiprocessing
import pickle
import signal
import struct
import time
import traceback
from collections.abc import Callable, Sequence
from multiprocessing.connection import Connection
from typing import Any, Protocol

__all__ = [
    "TEIL_BYTES",
    "Auftrag",
    "AuftragAbgebrochen",
    "AuftragFehler",
    "Ausfuehrer",
    "DirektAusfuehrer",
    "ProzessAusfuehrer",
    "importiere",
]

TEIL_BYTES = 4 * 1024 * 1024
"""Größte Nachricht über die Pipe (4 MiB): Ein ``recv`` blockiert die Oberfläche höchstens so
lange, wie diese Teilmenge zum Lesen braucht (gemessen 13 bis 17 ms)."""

ZEITANTEIL_S = 0.015
"""Höchste Zeit, die eine Abfrage :meth:`Auftrag.fertig` mit dem Empfang weiterer Teile
verbringt (zusätzlich zu dem gerade laufenden Teil)."""

_ENDE_WARTEN_S = 2.0
"""Zeit, die ein Prozess nach dem Ergebnis (bzw. nach ``terminate``) enden darf; danach wird er
beendet."""

_EOF_WARTEN_S = 0.2
"""Kurze Wartezeit auf den Exitcode eines Prozesses, dessen Pipe abgebrochen ist."""

_KOPF = b"K"
_FEHLER = b"F"
_TRENNER = "\x00"


class AuftragFehler(Exception):  # noqa: N818  (fachlicher Name)
    """Der Auftrag ist fehlgeschlagen (im Prozess oder mit dem Prozess).

    Attributes
    ----------
    meldung : str
        Text der Ausnahme im Auftrag bzw. Beschreibung des Prozessendes.
    typ : str
        Klassenname der ursprünglichen Ausnahme (leer, wenn der Prozess ohne Ausnahme endete).
    traceback_text : str
        Ablaufverfolgung aus dem Prozess (für Protokolle, nicht für den Nutzer).
    """

    def __init__(self, meldung: str, typ: str = "", traceback_text: str = "") -> None:
        super().__init__(meldung)
        self.meldung = meldung
        self.typ = typ
        self.traceback_text = traceback_text


class AuftragAbgebrochen(Exception):  # noqa: N818  (fachlicher Name)
    """Das Ergebnis eines abgebrochenen Auftrags wurde abgefragt."""


class Auftrag(Protocol):
    """Ein gestarteter Hintergrundauftrag."""

    def fertig(self) -> bool:
        """Nicht blockierend: ``True``, wenn Ergebnis oder Fehler vorliegen oder abgebrochen.

        Jeder Aufruf nimmt bereits gesendete Teile des Ergebnisses entgegen (begrenzte Zeit).
        """
        ...

    def ergebnis(self) -> Any:
        """Ergebnis des Auftrags; erst nach ``fertig() == True`` aufrufen.

        Raises
        ------
        AuftragFehler
            Der Auftrag warf eine Ausnahme oder der Prozess endete unerwartet.
        AuftragAbgebrochen
            Der Auftrag wurde abgebrochen.
        RuntimeError
            Der Auftrag ist noch nicht fertig.
        """
        ...

    def abbrechen(self) -> None:
        """Beendet den Auftrag sofort; wirkungslos, wenn er schon fertig ist."""
        ...


class Ausfuehrer(Protocol):
    """Startet Aufträge (Funktion auf Modulebene mit einfachen, picklebaren Argumenten)."""

    def starte(self, funktion: Callable[..., Any], *argumente: Any) -> Auftrag:
        """Startet ``funktion(*argumente)`` und kehrt sofort zurück."""
        ...

    def beende(self) -> None:
        """Bricht alle noch laufenden Aufträge ab (z. B. beim Schließen des Fensters)."""
        ...


def importiere(modulnamen: Sequence[str]) -> None:
    """Leer-Auftrag zum Vorwärmen: importiert die Module (füllt den Dateicache des Systems).

    Parameters
    ----------
    modulnamen : sequence of str
        Vollständige Modulnamen, z. B. ``("ldv_automation.auswertung.jobs",)``.
    """
    for name in modulnamen:
        importlib.import_module(name)


# --- Direkter Ausführer (Tests) --------------------------------------------------------------


class _DirekterAuftrag:
    """Bereits ausgeführter Auftrag (Ergebnis oder Fehler stehen fest)."""

    def __init__(self, funktion: Callable[..., Any], argumente: tuple[Any, ...]) -> None:
        self._ergebnis: Any = None
        self._fehler: AuftragFehler | None = None
        self._abgebrochen = False
        try:
            self._ergebnis = funktion(*argumente)
        except Exception as exc:
            self._fehler = AuftragFehler(str(exc), type(exc).__name__, traceback.format_exc())

    def fertig(self) -> bool:
        return True

    def ergebnis(self) -> Any:
        if self._abgebrochen:
            raise AuftragAbgebrochen
        if self._fehler is not None:
            raise self._fehler
        return self._ergebnis

    def abbrechen(self) -> None:
        self._abgebrochen = True


class DirektAusfuehrer:
    """Führt Aufträge synchron im aufrufenden Prozess aus (für Tests, ohne Prozess)."""

    def starte(self, funktion: Callable[..., Any], *argumente: Any) -> Auftrag:
        """Führt ``funktion(*argumente)`` sofort aus; das Ergebnis liegt dann vor."""
        return _DirekterAuftrag(funktion, argumente)

    def beende(self) -> None:
        """Nichts zu beenden."""


# --- Prozess-Ausführer -----------------------------------------------------------------------


def _sende_teile(verbindung: Connection, daten: memoryview, teil_bytes: int) -> None:
    """Sendet ``daten`` in Nachrichten von höchstens ``teil_bytes``."""
    for anfang in range(0, len(daten), teil_bytes):
        verbindung.send_bytes(daten[anfang : anfang + teil_bytes])


def _worker(
    verbindung: Connection,
    funktion: Callable[..., Any],
    argumente: tuple[Any, ...],
    teil_bytes: int,
) -> None:
    """Rumpf des Prozesses: Auftrag ausführen, Ergebnis in Teilen oder Fehlertext senden."""
    # Strg+C geht an die ganze Prozessgruppe; die Oberfläche beendet den Worker selbst.
    signal.signal(signal.SIGINT, signal.SIG_IGN)
    try:
        ergebnis = funktion(*argumente)
        puffer: list[pickle.PickleBuffer] = []
        haupt = pickle.dumps(ergebnis, protocol=5, buffer_callback=puffer.append)
        stuecke = [memoryview(haupt)] + [b.raw() for b in puffer]
        kopf = (
            _KOPF
            + struct.pack("<I", len(stuecke))
            + b"".join(struct.pack("<Q", len(s)) for s in stuecke)
        )
    except Exception as exc:
        text = _TRENNER.join((type(exc).__name__, str(exc), traceback.format_exc()))
        verbindung.send_bytes(_FEHLER + text.encode("utf-8"))
        verbindung.close()
        return
    verbindung.send_bytes(kopf)
    for stueck in stuecke:
        _sende_teile(verbindung, stueck, teil_bytes)
    verbindung.close()


class _ProzessAuftrag:
    """Auftrag in eigenem Prozess; empfängt das Ergebnis stückweise in :meth:`fertig`."""

    def __init__(self, empfang: Connection, prozess: Any) -> None:
        self._empfang = empfang
        self._prozess = prozess
        self._groessen: list[int] | None = None  # Größe je Stück (None: Kopf fehlt noch)
        self._puffer: list[bytearray] = []  # Zielpuffer je Stück, in Reihenfolge angelegt
        self._stueck = 0  # Index des Stücks, das gerade gefüllt wird
        self._gefuellt = 0  # bereits empfangene Bytes im aktuellen Stück
        self._ergebnis: Any = None
        self._fehler: AuftragFehler | None = None
        self._fertig = False
        self._abgebrochen = False
        self._ende_s = 0.0

    # -- Empfang ------------------------------------------------------------------------------

    def _fehler_setzen(self, meldung: str, typ: str = "", traceback_text: str = "") -> None:
        self._fehler = AuftragFehler(meldung, typ, traceback_text)
        self._abschliessen()

    def _abschliessen(self) -> None:
        """Verbindung schließen; der Prozess wird nicht abgewartet (das kostet bis 250 ms).

        Sein Ende (Freigabe der großen Felder) räumt :meth:`aufraeumen` später ein.
        """
        self._fertig = True
        self._ende_s = time.monotonic()
        self._empfang.close()

    def aufraeumen(self) -> bool:
        """Sammelt den beendeten Prozess ein, ohne zu warten.

        Returns
        -------
        bool
            ``True``, wenn der Prozess beendet und eingesammelt ist. Ein Prozess, der
            :data:`_ENDE_WARTEN_S` nach dem Ergebnis noch läuft, wird beendet.
        """
        if self._prozess.exitcode is not None:
            self._prozess.join(0)
            return True
        if time.monotonic() - self._ende_s > _ENDE_WARTEN_S:
            self._prozess.terminate()
        return False

    def _kopf_lesen(self, nachricht: bytes) -> None:
        anzahl = struct.unpack_from("<I", nachricht, 1)[0]
        self._groessen = list(struct.unpack_from(f"<{anzahl}Q", nachricht, 5))
        self._puffer = []
        self._stueck = 0
        self._gefuellt = 0

    def _stueck_weiter(self) -> None:
        """Nächstes Stück anwählen; leere Stücke (kein Teil auf der Pipe) werden übersprungen."""
        assert self._groessen is not None
        self._stueck += 1
        self._gefuellt = 0
        while self._stueck < len(self._groessen) and self._groessen[self._stueck] == 0:
            self._puffer.append(bytearray(0))
            self._stueck += 1

    def _ergebnis_bauen(self) -> None:
        try:
            self._ergebnis = pickle.loads(self._puffer[0], buffers=self._puffer[1:])
        except Exception as exc:
            self._fehler_setzen(
                f"Ergebnis nicht lesbar: {exc}", type(exc).__name__, traceback.format_exc()
            )
            return
        self._puffer = []
        self._abschliessen()

    def _teil_empfangen(self) -> None:
        """Genau eine Nachricht (höchstens :data:`TEIL_BYTES`) entgegennehmen."""
        if self._groessen is None:
            nachricht = self._empfang.recv_bytes()
            if nachricht[:1] == _KOPF:
                self._kopf_lesen(nachricht)  # das Hauptstück (Pickle) ist nie leer
            elif nachricht[:1] == _FEHLER:
                typ, meldung, spur = (nachricht[1:].decode("utf-8") + _TRENNER * 2).split(
                    _TRENNER, 2
                )
                self._fehler_setzen(meldung, typ, spur.rstrip(_TRENNER))
            else:
                self._fehler_setzen("unerwartete Nachricht vom Hintergrundprozess")
            return
        if self._gefuellt == 0:
            # Zielpuffer erst beim ersten Teil anlegen: das Nullen großer Puffer auf einmal
            # kostete gemessen bis 340 ms am Stück; je Stück sind es wenige Millisekunden.
            self._puffer.append(bytearray(self._groessen[self._stueck]))
        ziel = self._puffer[self._stueck]
        self._gefuellt += self._empfang.recv_bytes_into(ziel, self._gefuellt)
        if self._gefuellt >= len(ziel):
            self._stueck_weiter()
            if self._stueck >= len(self._groessen):
                self._ergebnis_bauen()

    def _prozess_ohne_ergebnis(self) -> None:
        code = self._prozess.exitcode
        self._fehler_setzen(f"Hintergrundprozess unerwartet beendet (Exitcode {code})")

    # -- Schnittstelle ------------------------------------------------------------------------

    @property
    def aktiv(self) -> bool:
        """``True``, solange der Auftrag weder fertig noch abgebrochen ist."""
        return not (self._fertig or self._abgebrochen)

    def fertig(self) -> bool:
        if self._fertig or self._abgebrochen:
            return True
        beginn = time.perf_counter()
        try:
            while True:
                if self._empfang.poll(0):
                    self._teil_empfangen()
                    if self._fertig:
                        return True
                    if time.perf_counter() - beginn >= ZEITANTEIL_S:
                        return False
                    continue
                return False
        except (EOFError, OSError):
            # Pipe zu: der Prozess ist ohne vollständiges Ergebnis beendet (Absturz, ``os._exit``,
            # Speichermangel); sein Exitcode steht kurz darauf fest.
            self._prozess.join(_EOF_WARTEN_S)
            self._prozess_ohne_ergebnis()
            return True

    def ergebnis(self) -> Any:
        if self._abgebrochen:
            raise AuftragAbgebrochen
        if not self._fertig:
            raise RuntimeError("Auftrag noch nicht fertig")
        if self._fehler is not None:
            raise self._fehler
        return self._ergebnis

    def abbrechen(self) -> None:
        if self._fertig or self._abgebrochen:
            return
        self._abgebrochen = True
        self._prozess.terminate()
        self._prozess.join(_ENDE_WARTEN_S)
        self._empfang.close()
        self._puffer = []


class ProzessAusfuehrer:
    """Startet jeden Auftrag in einem eigenen ``spawn``-Prozess (``Process`` plus ``Pipe``).

    Die Funktion und ihre Argumente müssen sich ``pickle``n lassen (Funktion auf Modulebene
    eines importierbaren Moduls). Das Ergebnis wird in Teilen von höchstens ``teil_bytes``
    übertragen.

    Parameters
    ----------
    teil_bytes : int, optional
        Größe der Teile in Byte, 1 bis :data:`TEIL_BYTES` (Voreinstellung 4 MiB; kleinere Werte
        nur für Tests).

    Raises
    ------
    ValueError
        Wenn ``teil_bytes`` außerhalb von 1 bis :data:`TEIL_BYTES` liegt.
    """

    def __init__(self, teil_bytes: int = TEIL_BYTES) -> None:
        if not 1 <= teil_bytes <= TEIL_BYTES:
            raise ValueError(f"teil_bytes muss in 1 … {TEIL_BYTES} liegen: {teil_bytes}")
        self._teil_bytes = teil_bytes
        self._kontext = multiprocessing.get_context("spawn")
        self._laufend: list[_ProzessAuftrag] = []

    def starte(self, funktion: Callable[..., Any], *argumente: Any) -> Auftrag:
        """Startet den Prozess und kehrt sofort zurück (Spawn dauert nur wenige 10 ms)."""
        self._laufend = [a for a in self._laufend if a.aktiv or not a.aufraeumen()]
        empfang, senden = self._kontext.Pipe(duplex=False)
        prozess = self._kontext.Process(
            target=_worker, args=(senden, funktion, argumente, self._teil_bytes), daemon=True
        )
        prozess.start()
        senden.close()  # nur der Worker hält das Sendeende offen: so meldet EOF sein Ende
        auftrag = _ProzessAuftrag(empfang, prozess)
        self._laufend.append(auftrag)
        return auftrag

    def beende(self) -> None:
        """Bricht alle laufenden Aufträge ab."""
        for auftrag in self._laufend:
            auftrag.abbrechen()
            auftrag.aufraeumen()
        self._laufend = []
