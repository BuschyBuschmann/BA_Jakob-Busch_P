"""Tests des allgemeinen Whitelist-Proxys (Default deny, Protokoll, Fehler, Hänger)."""

from __future__ import annotations

import datetime as dt
from typing import Any

import pytest
from fake_psv_com import FakeComError, FakeKnoten, Welt

from ldv_automation.geraet.com.whitelist import (
    ComFehler,
    Mitglied,
    ProxyKontext,
    Richtlinie,
    Schreibrecht,
    WhitelistProxy,
    com_details,
    oeffne,
)


def _nur_eins(args: tuple[Any, ...], kontext: ProxyKontext) -> str | None:
    return None if args == (1,) else "nur 1"


def _positiv(wert: Any, kontext: ProxyKontext) -> str | None:
    return None if isinstance(wert, int) and wert > 0 else "nur > 0"


RICHTLINIE = Richtlinie(
    objekte={
        "Wurzel": {
            "Wert": Mitglied(zugriff="get"),
            "Kind": Mitglied(zugriff="get", liefert="Kind"),
            "Liste": Mitglied(zugriff="call", liefert="Kind", pruefung=_nur_eins),
            "Ohne": Mitglied(zugriff="call"),
        },
        "Kind": {"Name": Mitglied(zugriff="get")},
    },
    schreiben={"Wurzel": {"Zahl": Schreibrecht(pruefung=_positiv, begruendung="Test")}},
    existenz={"Wurzel": frozenset({"Versteckt", "Fehlt"})},
    einstieg={"Test.Objekt": "Wurzel"},
)


class _Uhr:
    def __init__(self) -> None:
        self.t = 100.0

    def __call__(self) -> float:
        return self.t


def _wurzel(**props: Any) -> tuple[WhitelistProxy, ProxyKontext, Welt]:
    welt = Welt()
    kind = FakeKnoten("Kind", welt, {"Name": "k"})
    knoten = FakeKnoten(
        "Wurzel",
        welt,
        {"Wert": 1, "Kind": kind, "Zahl": 0, **props},
        {"Liste": lambda i: kind, "Ohne": lambda: None},
        getter={"Versteckt": lambda: 0},
    )
    kontext = ProxyKontext()
    return WhitelistProxy(knoten, "Wurzel", RICHTLINIE, kontext), kontext, welt


def test_lesen_und_objekte_werden_verpackt_und_protokolliert() -> None:
    proxy, kontext, welt = _wurzel()
    assert proxy.Wert == 1
    kind = proxy.Kind
    assert (
        isinstance(kind, WhitelistProxy)
        and kind.typ == "Kind"
        and repr(kind) == ("<WhitelistProxy Kind>")
    )
    assert kind.Name == "k"
    assert isinstance(proxy.Liste(1), WhitelistProxy)
    assert proxy.Ohne() is None
    pfade = [(a.pfad, a.op, a.argumente) for a in kontext.aufrufe()]
    assert pfade == [
        ("Wurzel.Wert", "get", ()),
        ("Wurzel.Kind", "get", ()),
        ("Kind.Name", "get", ()),
        ("Wurzel.Liste", "call", ("1",)),
        ("Wurzel.Ohne", "call", ()),
    ]
    assert [a.nr for a in kontext.aufrufe()] == [1, 2, 3, 4, 5]
    assert kontext.verweigerungen() == ()
    assert len(welt.log) == 5


def test_default_deny_fuer_alles_nicht_genannte() -> None:
    proxy, kontext, welt = _wurzel(Geheim=1)
    for zugriff in (
        lambda: proxy.Geheim,
        lambda: proxy._oleobj_,
        lambda: proxy.__dict__,
        lambda: proxy.Liste(2),
        lambda: proxy.Ohne(1),
        lambda: setattr(proxy, "Wert", 2),
        lambda: setattr(proxy, "Zahl", -1),
        lambda: delattr(proxy, "Wert"),
        lambda: proxy.existiert("Wert"),
        lambda: WhitelistProxy(object(), "Unbekannt", RICHTLINIE, kontext).Wert,
    ):
        with pytest.raises(PermissionError, match="Default deny"):
            zugriff()
    assert len(kontext.verweigerungen()) == 10
    assert kontext.aufrufe() == ()
    assert welt.log == []


def test_erlaubte_zuweisung_mit_proxy_wert_wird_ausgepackt() -> None:
    proxy, kontext, welt = _wurzel()
    proxy.Zahl = 5
    assert welt.log[-1] == ("Wurzel", "Zahl", "set", (5,))
    assert kontext.letzter_aufruf == ("Wurzel.Zahl", "set", None)
    recht = Schreibrecht(pruefung=lambda w, k: None, begruendung="x")
    r2 = Richtlinie(objekte=RICHTLINIE.objekte, schreiben={"Wurzel": {"Kind": recht}})
    welt2 = Welt()
    ziel = FakeKnoten("Wurzel", welt2)
    kind_roh = FakeKnoten("Kind", welt2)
    WhitelistProxy(ziel, "Wurzel", r2, kontext).Kind = WhitelistProxy(kind_roh, "Kind", r2, kontext)
    assert ziel._props["Kind"] is kind_roh


def test_com_fehler_mit_hresult_und_excepinfo() -> None:
    proxy, kontext, welt = _wurzel()
    welt.fehler[("Wurzel", "Liste")] = FakeComError("Index ungültig", hresult=-5)
    kontext.letzter_aufruf = ("x", "get", 0)
    with pytest.raises(ComFehler) as info:
        proxy.Liste(1)
    fehler = info.value
    assert (fehler.pfad, fehler.op, fehler.argumente) == ("Wurzel.Liste", "call", ("1",))
    erwartet = (-5, "Index ungültig", "Index ungültig")
    assert (fehler.hresult, fehler.excepinfo, fehler.text) == erwartet
    assert "Wurzel.Liste [call] fehlgeschlagen" in str(fehler)
    assert kontext.aufrufe()[-1].fehler == "Index ungültig"
    assert kontext.letzter_aufruf is None
    assert kontext.haengender_aufruf_seit_s() is None


def test_com_details_varianten() -> None:
    assert com_details(ValueError("x")) == (None, None, "x")
    assert com_details(ValueError()) == (None, None, "ValueError")

    class OhneError(Exception):
        hresult = True
        excepinfo = (0, "q", "", None)
        strerror = "Ausnahme"

    assert com_details(OhneError()) == (None, None, "Ausnahme")


def test_unerwarteter_rueckgabetyp_und_tupel() -> None:
    proxy, _, _ = _wurzel(Wert=[1, (2.0, "a"), dt.datetime(2026, 1, 1)])
    assert proxy.Wert == (1, (2.0, "a"), dt.datetime(2026, 1, 1))
    proxy, _, _ = _wurzel(Wert=object())
    with pytest.raises(ComFehler, match="unerwarteter Rückgabetyp"):
        _ = proxy.Wert


def test_objekt_none_bleibt_none() -> None:
    proxy, _, _ = _wurzel(Kind=None)
    assert proxy.Kind is None


def test_existenzpruefung() -> None:
    proxy, kontext, _ = _wurzel()
    assert proxy.existiert("Versteckt") is True
    assert proxy.existiert("Fehlt") is False
    ohne_ole = WhitelistProxy(object(), "Wurzel", RICHTLINIE, kontext)
    assert ohne_ole.existiert("Fehlt") is False
    assert [a.op for a in kontext.aufrufe()] == ["exists"] * 3


def test_haengender_aufruf_mit_testuhr() -> None:
    uhr = _Uhr()
    kontext = ProxyKontext(uhr=uhr)
    gemessen: list[float | None] = []

    def langsam() -> int:
        uhr.t += 2.5
        gemessen.append(kontext.haengender_aufruf_seit_s())
        uhr.t += 0.5
        return 1

    knoten = FakeKnoten("Wurzel", Welt(), getter={"Wert": langsam})
    assert WhitelistProxy(knoten, "Wurzel", RICHTLINIE, kontext).Wert == 1
    assert gemessen == [2.5]
    assert kontext.haengender_aufruf_seit_s() is None
    assert kontext.aufrufe()[0].dauer_s == 3.0


def test_oeffne() -> None:
    kontext = ProxyKontext()
    welt = Welt()
    knoten = FakeKnoten("Wurzel", welt, {"Wert": 7})
    proxy = oeffne("Test.Objekt", lambda p: knoten, RICHTLINIE, kontext)
    assert proxy.typ == "Wurzel" and proxy.Wert == 7
    with pytest.raises(PermissionError, match="ProgID nicht freigegeben"):
        oeffne("Anderes.Objekt", lambda p: pytest.fail("kein Dispatch"), RICHTLINIE, kontext)

    def scheitert(progid: str) -> object:
        raise FakeComError("Klasse nicht registriert", hresult=-2147221005)

    with pytest.raises(ComFehler) as info:
        oeffne("Test.Objekt", scheitert, RICHTLINIE, kontext)
    assert info.value.hresult == -2147221005 and info.value.op == "dispatch"
    assert [a.pfad for a in kontext.aufrufe()] == [
        "Dispatch.Test.Objekt",
        "Wurzel.Wert",
        "Dispatch.Test.Objekt",
    ]
    assert kontext.verweigerungen()[0].pfad == "Dispatch.Anderes.Objekt"


def test_standard_existiert_nutzt_dateisystem(tmp_path: Any) -> None:
    datei = tmp_path / "a.txt"
    kontext = ProxyKontext()
    assert not kontext.existiert(str(datei))
    datei.write_text("x")
    assert kontext.existiert(str(datei))
