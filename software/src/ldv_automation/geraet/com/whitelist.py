"""Allgemeiner Whitelist-Proxy für COM-Objekte (Default deny, ADR-007).

Konzept übernommen aus ``tools/erkundung/erkundung.py`` (Plan P2, Abschnitt 1, ADR-07
„eigener Proxy im Hauptpaket“), hier mit der Richtlinie als Parameter statt modulweit:

* Nur Mitglieder, die die :class:`Richtlinie` ausdrücklich nennt, werden an das COM-Objekt
  weitergereicht. Alles andere wird mit ``PermissionError`` „verweigert (Default deny)“
  abgelehnt und im :class:`ProxyKontext` protokolliert.
* Methodenaufrufe und Zuweisungen laufen durch eine Prüffunktion (Argumente, Wertebereich,
  Freigaben im Kontext). Die Prüfung liegt **vor** jedem Zugriff auf das COM-Objekt.
* Jeder weitergereichte Zugriff steht im Aufrufprotokoll (Pfad, Operation, Argumente, Dauer,
  Fehler). Ein laufender Zugriff ist als „hängend“ abfragbar (Wächter-Thread, Plan P2 2.5).
* Fehler des COM-Objekts werden als :class:`ComFehler` mit Pfad, Argumenten, ``hresult`` und
  ``excepinfo`` weitergereicht; der Adapter übersetzt sie in ``GeraeteFehler``.
* COM-Objekte verlassen den Proxy nie: Rückgaben sind entweder einfache Werte oder wieder
  ein Proxy.

Das Modul nutzt nur die Standardbibliothek.
"""

from __future__ import annotations

import datetime as dt
import threading
import time
from collections.abc import Callable, Iterator, Mapping
from contextlib import contextmanager
from dataclasses import dataclass, field
from typing import Any, Literal

Pruefung = Callable[[tuple[Any, ...], "ProxyKontext"], "str | None"]
"""Prüft die Argumente eines Aufrufs; liefert den Ablehnungsgrund oder ``None``."""

WertPruefung = Callable[[Any, "ProxyKontext"], "str | None"]
"""Prüft den Wert einer Zuweisung; liefert den Ablehnungsgrund oder ``None``."""

Wirkung = Callable[["ProxyKontext"], None]
"""Wird nach bestandener Prüfung unmittelbar vor dem COM-Zugriff ausgeführt."""


@dataclass(frozen=True, kw_only=True)
class Mitglied:
    """Freigegebenes lesendes Mitglied oder freigegebene Methode eines COM-Objekttyps.

    Parameters
    ----------
    zugriff : {"get", "call"}
        Property lesen oder Methode aufrufen.
    liefert : str or None
        Typname des zurückgegebenen Objekts (Schlüssel der Richtlinie) oder ``None`` für
        einfache Werte.
    pruefung : callable or None
        Argumentprüfung bei ``"call"``. Ohne Prüfung sind nur Aufrufe ohne Argumente erlaubt.
    vor_aufruf : callable or None
        Wirkung auf den Kontext nach bestandener Prüfung (z. B. „eigene Messung aktiv“).
    begruendung : str
        Begründung (Pflicht für Methoden mit Wirkung auf das Gerät).
    """

    zugriff: Literal["get", "call"]
    liefert: str | None = None
    pruefung: Pruefung | None = None
    vor_aufruf: Wirkung | None = None
    begruendung: str = ""


@dataclass(frozen=True, kw_only=True)
class Schreibrecht:
    """Freigegebene Zuweisung an eine Property.

    Parameters
    ----------
    pruefung : callable
        Wertprüfung (Typ, Bereich, Freigaben im Kontext).
    begruendung : str
        Begründung der Schreiboperation (Plan P2, 3.3).
    """

    pruefung: WertPruefung
    begruendung: str


@dataclass(frozen=True, kw_only=True)
class Richtlinie:
    """Vollständige Freigabeliste. Was fehlt, ist verboten (Default deny).

    Parameters
    ----------
    objekte : mapping
        Typname → Mitgliedsname → :class:`Mitglied` (Lesen und Methoden).
    schreiben : mapping
        Typname → Property-Name → :class:`Schreibrecht`.
    existenz : mapping
        Typname → Namen, deren Existenz geprüft werden darf (ohne sie zu lesen).
    einstieg : mapping
        Freigegebene ProgIDs → Typname des Einstiegsobjekts.
    """

    objekte: Mapping[str, Mapping[str, Mitglied]]
    schreiben: Mapping[str, Mapping[str, Schreibrecht]] = field(default_factory=dict)
    existenz: Mapping[str, frozenset[str]] = field(default_factory=dict)
    einstieg: Mapping[str, str] = field(default_factory=dict)


@dataclass(frozen=True, kw_only=True)
class Aufruf:
    """Eintrag im Aufrufprotokoll (tatsächlich weitergereichter Zugriff)."""

    nr: int
    pfad: str
    op: str
    argumente: tuple[str, ...]
    dauer_s: float
    fehler: str | None


@dataclass(frozen=True, kw_only=True)
class Verweigerung:
    """Eintrag im Protokoll der verweigerten Zugriffe."""

    pfad: str
    op: str
    grund: str


class ComFehler(Exception):  # noqa: N818  (Gegenstück zu pywintypes.com_error)
    """Ein weitergereichter COM-Zugriff ist gescheitert.

    Parameters
    ----------
    pfad : str
        ``Typ.Mitglied`` des Zugriffs, z. B. ``"Settings.Load"``.
    op : str
        ``"get"``, ``"call"``, ``"set"``, ``"exists"`` oder ``"dispatch"``.
    argumente : tuple of str
        Argumente als Text (Objekte als ``<Typ>``).
    text : str
        Beschreibung (aus ``excepinfo``, sonst Ausnahmetext).
    hresult : int or None
        HRESULT der COM-Ausnahme, falls vorhanden.
    excepinfo : str or None
        Beschreibungstext aus ``excepinfo`` (Index 2), falls vorhanden.
    """

    def __init__(
        self,
        pfad: str,
        op: str,
        argumente: tuple[str, ...],
        text: str,
        *,
        hresult: int | None = None,
        excepinfo: str | None = None,
    ) -> None:
        super().__init__(f"{pfad} [{op}] fehlgeschlagen: {text}")
        self.pfad = pfad
        self.op = op
        self.argumente = argumente
        self.text = text
        self.hresult = hresult
        self.excepinfo = excepinfo


def com_details(exc: BaseException) -> tuple[int | None, str | None, str]:
    """Liest ``hresult``, ``excepinfo``-Text und Beschreibung aus einer COM-Ausnahme.

    ``pywintypes.com_error`` hat die Attribute ``hresult``, ``strerror`` und ``excepinfo``
    (Tupel, Beschreibung an Index 2, I5 5.2 [ungeprüft]); andere Ausnahmen liefern
    ``(None, None, str(exc))``.
    """
    hresult = getattr(exc, "hresult", None)
    if not isinstance(hresult, int) or isinstance(hresult, bool):
        hresult = None
    info = getattr(exc, "excepinfo", None)
    beschreibung: str | None = None
    if isinstance(info, tuple) and len(info) > 2 and isinstance(info[2], str) and info[2]:
        beschreibung = info[2]
    strerror = getattr(exc, "strerror", None)
    text = beschreibung or (strerror if isinstance(strerror, str) and strerror else "")
    return hresult, beschreibung, text or str(exc) or type(exc).__name__


class ProxyKontext:
    """Gemeinsamer Zustand aller Proxys einer Verbindung.

    Freigaben (vom Adapter gesetzt, nur aus dem Geräte-Thread):

    Parameters
    ----------
    start_erlaubt : bool
        ``GetApplication(True, …)`` erlaubt (``--start-psv`` mit bestätigtem ``JA``).
    schreiben_erlaubt : bool
        Schreibende Einstellungsoperationen S2-S5, S9 (Trockenlauf und Messen).
    messen_erlaubt : bool
        Messende Operationen S6-S8 (Betriebsart Messen).
    direkt_setzen_erlaubt : bool
        Rückfall S4 (direkte FFT-Properties, wenn kein Validator vorhanden ist).
    messdaten_wurzel : str or None
        Wurzelordner für Scandateien und Einstellungs-Nachweise.
    existiert : callable
        Existenzprüfung für Pfade (injizierbar für Tests).
    uhr : callable
        Monotone Uhr in s (für Dauer und Hänger-Erkennung).

    Notes
    -----
    ``messfreigabe`` (Durchgangsbestätigung) und ``eigene_messung_aktiv`` werden zur
    Laufzeit gesetzt. ``letzter_aufruf`` ist der zuletzt weitergereichte Zugriff samt
    Ergebnis; S7 verlangt, dass unmittelbar davor ``Acquisition.State == Stopped`` gelesen
    wurde.
    """

    def __init__(
        self,
        *,
        start_erlaubt: bool = False,
        schreiben_erlaubt: bool = False,
        messen_erlaubt: bool = False,
        direkt_setzen_erlaubt: bool = False,
        messdaten_wurzel: str | None = None,
        existiert: Callable[[str], bool] | None = None,
        uhr: Callable[[], float] = time.monotonic,
    ) -> None:
        import os.path

        self.start_erlaubt = start_erlaubt
        self.schreiben_erlaubt = schreiben_erlaubt
        self.messen_erlaubt = messen_erlaubt
        self.direkt_setzen_erlaubt = direkt_setzen_erlaubt
        self.messdaten_wurzel = messdaten_wurzel
        self.existiert: Callable[[str], bool] = existiert or os.path.lexists
        self.uhr = uhr
        self.messfreigabe = False
        self.eigene_messung_aktiv = False
        self.letzter_aufruf: tuple[str, str, object] | None = None
        self._lock = threading.Lock()
        self._aufrufe: list[Aufruf] = []
        self._verweigerungen: list[Verweigerung] = []
        self._haengt_seit: float | None = None

    def protokolliere_aufruf(
        self, pfad: str, op: str, argumente: tuple[str, ...], dauer_s: float, fehler: str | None
    ) -> None:
        """Hängt einen weitergereichten Zugriff an das Aufrufprotokoll an."""
        with self._lock:
            self._aufrufe.append(
                Aufruf(
                    nr=len(self._aufrufe) + 1,
                    pfad=pfad,
                    op=op,
                    argumente=argumente,
                    dauer_s=dauer_s,
                    fehler=fehler,
                )
            )

    def protokolliere_verweigerung(self, pfad: str, op: str, grund: str) -> None:
        """Hängt einen verweigerten Zugriffsversuch an."""
        with self._lock:
            self._verweigerungen.append(Verweigerung(pfad=pfad, op=op, grund=grund))

    def aufrufe(self) -> tuple[Aufruf, ...]:
        """Kopie des Aufrufprotokolls."""
        with self._lock:
            return tuple(self._aufrufe)

    def verweigerungen(self) -> tuple[Verweigerung, ...]:
        """Kopie der Verweigerungen."""
        with self._lock:
            return tuple(self._verweigerungen)

    def anzahl_aufrufe(self) -> int:
        """Anzahl der weitergereichten Zugriffe (ohne Kopie des Protokolls)."""
        with self._lock:
            return len(self._aufrufe)

    def _beginne(self) -> float:
        start = self.uhr()
        with self._lock:
            self._haengt_seit = start
        return start

    def _beende(self) -> None:
        with self._lock:
            self._haengt_seit = None

    @contextmanager
    def ueberwache(self) -> Iterator[None]:
        """Meldet einen Aufruf außerhalb des Proxys (z. B. ``tasklist``) an den Wächter."""
        self._beginne()
        try:
            yield
        finally:
            self._beende()

    def haengender_aufruf_seit_s(self) -> float | None:
        """Dauer des laufenden COM-Zugriffs in s, sonst ``None`` (thread-sicher)."""
        with self._lock:
            start = self._haengt_seit
        return None if start is None else max(0.0, self.uhr() - start)


_EINFACH = (type(None), bool, int, float, str, bytes, dt.datetime, dt.date)


def _text(arg: object) -> str:
    if isinstance(arg, WhitelistProxy):
        return f"<{arg.typ}>"
    return repr(arg)[:200]


def _als_text(args: tuple[Any, ...]) -> tuple[str, ...]:
    return tuple(_text(a) for a in args)


def _roh(value: object) -> object:
    return value._obj if isinstance(value, WhitelistProxy) else value


def _einfacher_wert(value: object, pfad: str) -> object:
    """Lässt nur einfache Werte (und Tupel davon) durch; ein Objekt ist ein Fehler."""
    if isinstance(value, _EINFACH):
        return value
    if isinstance(value, tuple | list):
        return tuple(_einfacher_wert(v, pfad) for v in value)
    raise ComFehler(pfad, "get", (), f"unerwarteter Rückgabetyp {type(value).__name__}")


def _mitglied_existiert(obj: object, name: str) -> bool:
    """Existenzprüfung ohne Lesezugriff (COM: ``GetIDsOfNames``)."""
    ole = getattr(obj, "_oleobj_", None)
    if ole is None:
        return hasattr(type(obj), name)
    try:
        ole.GetIDsOfNames(name)
    except Exception:  # COM meldet unbekannte Namen als Ausnahme: das *ist* die Antwort
        return False
    return True


class WhitelistProxy:
    """Reicht nur freigegebene Mitglieder an ein COM-Objekt weiter.

    Parameters
    ----------
    obj : object
        Das umhüllte COM-Objekt (wird nie herausgegeben).
    typ : str
        Typname in der Richtlinie.
    richtlinie : Richtlinie
        Freigabeliste.
    kontext : ProxyKontext
        Gemeinsamer Protokoll- und Freigabezustand.
    """

    __slots__ = ("_kontext", "_obj", "_richtlinie", "_typ")

    def __init__(
        self, obj: object, typ: str, richtlinie: Richtlinie, kontext: ProxyKontext
    ) -> None:
        object.__setattr__(self, "_obj", obj)
        object.__setattr__(self, "_typ", typ)
        object.__setattr__(self, "_richtlinie", richtlinie)
        object.__setattr__(self, "_kontext", kontext)

    @property
    def typ(self) -> str:
        """Typname des umhüllten Objekts."""
        return str(self._typ)

    def __repr__(self) -> str:
        return f"<WhitelistProxy {self._typ}>"

    def _verweigere(self, name: str, op: str, grund: str) -> PermissionError:
        pfad = f"{self._typ}.{name}"
        self._kontext.protokolliere_verweigerung(pfad, op, grund)
        return PermissionError(f"verweigert (Default deny): {pfad} [{op}]: {grund}")

    def _fuehre_aus(
        self, name: str, op: str, args: tuple[Any, ...], fn: Callable[[], object]
    ) -> object:
        kontext: ProxyKontext = self._kontext
        pfad = f"{self._typ}.{name}"
        texte = _als_text(args)
        start = kontext._beginne()
        try:
            ergebnis = fn()
        except Exception as exc:
            dauer = kontext.uhr() - start
            kontext._beende()
            hresult, excepinfo, text = com_details(exc)
            kontext.letzter_aufruf = None
            kontext.protokolliere_aufruf(pfad, op, texte, dauer, text)
            raise ComFehler(pfad, op, texte, text, hresult=hresult, excepinfo=excepinfo) from exc
        dauer = kontext.uhr() - start
        kontext._beende()
        kontext.protokolliere_aufruf(pfad, op, texte, dauer, None)
        kontext.letzter_aufruf = (pfad, op, ergebnis if isinstance(ergebnis, _EINFACH) else None)
        return ergebnis

    def __getattr__(self, name: str) -> Any:
        if name.startswith("_"):
            raise self._verweigere(name, "get", "private/dunder Mitglieder sind nie freigegeben")
        mitglied = self._richtlinie.objekte.get(self._typ, {}).get(name)
        if mitglied is None:
            raise self._verweigere(name, "get", "nicht in der Whitelist")
        obj = self._obj
        if mitglied.zugriff == "get":
            wert = self._fuehre_aus(name, "get", (), lambda: getattr(obj, name))
            return self._verpacke(name, wert, mitglied.liefert)

        def aufruf(*args: Any) -> Any:
            if mitglied.pruefung is None:
                problem = None if not args else "keine Argumente erlaubt"
            else:
                problem = mitglied.pruefung(args, self._kontext)
            if problem is not None:
                raise self._verweigere(name, "call", problem)
            if mitglied.vor_aufruf is not None:
                mitglied.vor_aufruf(self._kontext)
            roh = tuple(_roh(a) for a in args)
            wert = self._fuehre_aus(name, "call", args, lambda: getattr(obj, name)(*roh))
            return self._verpacke(name, wert, mitglied.liefert)

        return aufruf

    def _verpacke(self, name: str, wert: object, liefert: str | None) -> Any:
        if liefert is None:
            return _einfacher_wert(wert, f"{self._typ}.{name}")
        if wert is None:
            return None
        return WhitelistProxy(wert, liefert, self._richtlinie, self._kontext)

    def __setattr__(self, name: str, value: Any) -> None:
        recht = self._richtlinie.schreiben.get(self._typ, {}).get(name)
        if recht is None:
            raise self._verweigere(name, "set", "Schreibzugriff nicht freigegeben")
        problem = recht.pruefung(value, self._kontext)
        if problem is not None:
            raise self._verweigere(name, "set", problem)
        obj = self._obj
        roh = _roh(value)
        self._fuehre_aus(name, "set", (value,), lambda: setattr(obj, name, roh))

    def __delattr__(self, name: str) -> None:
        raise self._verweigere(name, "del", "Löschen ist nie freigegeben")

    def existiert(self, name: str) -> bool:
        """Prüft nur die Existenz eines Mitglieds (ohne es zu lesen), falls freigegeben."""
        if name not in self._richtlinie.existenz.get(self._typ, frozenset()):
            raise self._verweigere(name, "exists", "Existenzprüfung nicht freigegeben")
        obj = self._obj
        return bool(self._fuehre_aus(name, "exists", (), lambda: _mitglied_existiert(obj, name)))


def oeffne(
    progid: str,
    dispatch: Callable[[str], object],
    richtlinie: Richtlinie,
    kontext: ProxyKontext,
) -> WhitelistProxy:
    """Legt ein freigegebenes Einstiegsobjekt an und gibt es nur als Proxy heraus.

    Raises
    ------
    PermissionError
        Wenn die ProgID nicht freigegeben ist (es gibt dann keinen ``Dispatch``).
    ComFehler
        Wenn ``dispatch`` scheitert.
    """
    typ = richtlinie.einstieg.get(progid)
    pfad = f"Dispatch.{progid}"
    if typ is None:
        grund = "ProgID nicht freigegeben"
        kontext.protokolliere_verweigerung(pfad, "dispatch", grund)
        raise PermissionError(f"verweigert (Default deny): {pfad} [dispatch]: {grund}")
    start = kontext._beginne()
    try:
        obj = dispatch(progid)
    except Exception as exc:
        dauer = kontext.uhr() - start
        kontext._beende()
        hresult, excepinfo, text = com_details(exc)
        kontext.protokolliere_aufruf(pfad, "dispatch", (), dauer, text)
        raise ComFehler(pfad, "dispatch", (), text, hresult=hresult, excepinfo=excepinfo) from exc
    dauer = kontext.uhr() - start
    kontext._beende()
    kontext.protokolliere_aufruf(pfad, "dispatch", (), dauer, None)
    kontext.letzter_aufruf = (pfad, "dispatch", None)
    return WhitelistProxy(obj, typ, richtlinie, kontext)
