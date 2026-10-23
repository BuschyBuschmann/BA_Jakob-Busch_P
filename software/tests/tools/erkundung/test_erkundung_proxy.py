"""Tests für den Whitelist-Proxy (K1): Default deny, Blacklist-Katalog, Argumentprüfung."""

from __future__ import annotations

from typing import Any

import erkundung
import pytest
from erkundung import (
    BLACKLIST,
    POLICY,
    WRITES,
    ProxyContext,
    WhitelistProxy,
)
from fake_psv import FakeNode, World, build_polyfile, build_psv


def _proxy(obj: Any, kind: str, *, allow_start: bool = False) -> WhitelistProxy:
    return WhitelistProxy(obj, kind, ProxyContext(allow_start=allow_start))


@pytest.mark.parametrize(("kind", "name", "op", "value"), BLACKLIST)
def test_blacklist_eintrag_wird_verweigert(kind: str, name: str, op: str, value: Any) -> None:
    ctx = ProxyContext()
    # object() hat keine COM-Mitglieder: Würde der Proxy etwas weiterleiten, käme AttributeError.
    proxy = WhitelistProxy(object(), kind, ctx)
    with pytest.raises(PermissionError):
        if op == "set":
            setattr(proxy, name, value)
        else:
            getattr(proxy, name)
    _calls, denied = ctx.snapshot()
    assert [d["pfad"] for d in denied] == [f"{kind}.{name}"]


def test_blacklist_enthaelt_keine_freigegebenen_lesezugriffe() -> None:
    for kind, name, op, _value in BLACKLIST:
        if op != "set":
            assert name not in POLICY.get(kind, {}), (kind, name)
        else:
            assert (kind, name) not in WRITES or kind == "PolyFile"


def test_nicht_aufgefuehrter_pfad_wird_verweigert() -> None:
    proxy = _proxy(object(), "Acquisition")
    with pytest.raises(PermissionError, match="nicht in der Whitelist"):
        _ = proxy.IrgendwasNeues
    with pytest.raises(PermissionError):
        _ = _proxy(object(), "UnbekannterTyp").Version


def test_private_und_dunder_mitglieder_sind_gesperrt() -> None:
    proxy = _proxy(FakeNode("Application", World(), {"Version": "1"}), "Application")
    for name in ("_oleobj_", "__class__x", "_obj_x"):
        with pytest.raises(PermissionError):
            getattr(proxy, name)
    with pytest.raises(PermissionError):
        del proxy.Version
    assert "Application" in repr(proxy)


def test_freigegebene_property_wird_gelesen_und_protokolliert() -> None:
    world = World()
    ctx = ProxyContext()
    ctx.current_step = "T"
    proxy = WhitelistProxy(FakeNode("Application", world, {"Version": "10.4"}), "Application", ctx)
    assert proxy.Version == "10.4"
    calls, denied = ctx.snapshot()
    assert denied == []
    assert calls[0]["pfad"] == "Application.Version"
    assert calls[0]["pruefpunkt"] == "T"
    assert calls[0]["fehler"] is None
    assert world.log == [("Application", "Version", "get")]


def test_fehler_im_com_objekt_wird_protokolliert_und_weitergereicht() -> None:
    world = World()
    node = FakeNode("Application", world, {"Version": "1"})
    from fake_psv import FakeComError

    world.fail[("Application", "Version")] = FakeComError("kaputt")
    ctx = ProxyContext()
    with pytest.raises(FakeComError):
        _ = WhitelistProxy(node, "Application", ctx).Version
    calls, _ = ctx.snapshot()
    assert calls[0]["fehler"].startswith("FakeComError")
    assert ctx.pending is None


def test_objekte_werden_gewrappt_none_bleibt_none_unbekannte_typen_werden_text() -> None:
    world = World()
    psv = build_psv(world)
    root = _proxy(psv, "AcquisitionInstance")
    app = root.GetApplication(False)
    assert isinstance(app, WhitelistProxy)
    assert app.kind == "Application"
    acq = app.Acquisition
    assert isinstance(acq, WhitelistProxy)
    # Tupel werden rekursiv bereinigt, Objekte nie nach außen gegeben.
    node = FakeNode("Hardware", world, {"SensorHeadNames": ("a", object())})
    value = _proxy(node, "Hardware").SensorHeadNames
    assert value[0] == "a"
    assert value[1].startswith("<nicht erwarteter Rückgabetyp")
    none_node = FakeNode("Infos", world, {"Hardware": None})
    assert _proxy(none_node, "Infos").Hardware is None
    item_node = FakeNode("Vibrometers", world, {}, {"Item": lambda i: None})
    assert _proxy(item_node, "Vibrometers").Item(1) is None


def test_get_application_start_nur_mit_freigabe() -> None:
    world = World()
    psv = build_psv(world, running=False)
    with pytest.raises(PermissionError, match="nicht freigegeben"):
        _proxy(psv, "AcquisitionInstance").GetApplication(True, 1000)
    assert world.started is False
    _proxy(psv, "AcquisitionInstance", allow_start=True).GetApplication(True, 1000)
    assert world.started is True
    for bad in [(), ("x",), (False, "t"), (False, 1, 2)]:
        with pytest.raises(PermissionError):
            _proxy(psv, "AcquisitionInstance").GetApplication(*bad)


@pytest.mark.parametrize(
    ("kind", "name", "args"),
    [
        ("Acquisition", "GetLaserOn", (5,)),
        ("Acquisition", "GetLaserOn", ()),
        ("Acquisition", "GetLaserOn", (True,)),
        ("MeasPoints", "Item", (0,)),
        ("MeasPoints", "Item", (True,)),
        ("MeasPoints", "Item", ("a",)),
        ("MeasPoints", "LabelToIndex", (1.5,)),
        ("MeasPoint", "CoordXYZ", (1,)),
        ("PolyFile", "Open", ("",)),
        ("PolyFile", "Open", (1,)),
        ("PolyFile", "Close", (1,)),
        ("PolyFile", "GetPointDomains", (1,)),
        ("PointDomain", "GetXAxis", (1,)),
        ("DataPoint", "GetData", (1, 0)),
        ("XAxis", "GetMidX", (-1,)),
        ("Controllers", "Item", (-1,)),
        ("SensorHeads", "Item", (True,)),
    ],
)
def test_argumentpruefung_verweigert_unzulaessige_aufrufe(
    kind: str, name: str, args: tuple[Any, ...]
) -> None:
    ctx = ProxyContext()
    proxy = WhitelistProxy(object(), kind, ctx)
    with pytest.raises(PermissionError):
        getattr(proxy, name)(*args)
    assert ctx.snapshot()[1]


def test_display_argument_wird_entpackt_und_nur_display_akzeptiert() -> None:
    world = World()
    pf = build_polyfile(world)
    ctx = ProxyContext()
    root = WhitelistProxy(pf, "PolyFile", ctx)
    root.ReadOnly = True
    root.Open("x.svd")
    domain = root.GetPointDomains().Item(2)
    display = domain.Channels.Item(1).Signals.Item(1).Displays.Item(2)
    assert display.kind == "Display"
    data = domain.DataPoints.Item(1).GetData(display, 0)
    assert len(data) == 16
    other = domain.Channels.Item(1)
    with pytest.raises(PermissionError):
        domain.GetXAxis(other)
    with pytest.raises(PermissionError):
        domain.DataPoints.Item(1).GetData(display, -1)
    assert domain.GetXAxis(display).GetMidX(0) == pytest.approx(1.25, rel=1e-12)


def test_nullbasierte_collections_erlauben_index_null() -> None:
    node = FakeNode("Controllers", World(), {}, {"Item": lambda i: None})
    assert _proxy(node, "Controllers").Item(0) is None


def test_readonly_nur_true_erlaubt() -> None:
    world = World()
    pf = build_polyfile(world)
    ctx = ProxyContext()
    proxy = WhitelistProxy(pf, "PolyFile", ctx)
    for bad in (False, 1, "True", None):
        with pytest.raises(PermissionError):
            proxy.ReadOnly = bad
    assert pf._props["ReadOnly"] is False
    proxy.ReadOnly = True
    assert pf._props["ReadOnly"] is True


def test_existenzpruefung_liest_nicht() -> None:
    world = World()
    fft = FakeNode(
        "FftProperties", world, {"Bandwidth": 1.0}, hidden=("FftAcqPropertiesValidator",)
    )
    proxy = _proxy(fft, "FftProperties")
    assert proxy.exists("FftAcqPropertiesValidator") is True
    assert world.log == []  # kein Lesezugriff auf das Mitglied selbst
    with pytest.raises(PermissionError):
        proxy.exists("Bandwidth")
    plain = FakeNode("FftProperties", world, {}, hidden=())
    assert _proxy(plain, "FftProperties").exists("FftAcqPropertiesValidator") is False


def test_member_exists_ohne_oleobj_nutzt_typ() -> None:
    class Plain:
        thing = 1

    assert erkundung._member_exists(Plain(), "thing") is True
    assert erkundung._member_exists(Plain(), "other") is False


def test_policy_ist_in_sich_konsistent() -> None:
    reachable = {"AcquisitionInstance", "PolyFile"}
    changed = True
    while changed:
        changed = False
        for kind in list(reachable):
            for member in POLICY[kind].values():
                if member.returns and member.returns not in reachable:
                    assert member.returns in POLICY, member.returns
                    reachable.add(member.returns)
                    changed = True
    assert reachable == set(POLICY), set(POLICY) - reachable
    assert set(erkundung.ALLOWED_PROGIDS.values()) == {"AcquisitionInstance", "PolyFile"}
    for kind, names in erkundung.EXISTS.items():
        assert kind in POLICY
        assert names.isdisjoint(POLICY[kind])
    # Keine einzige Whitelist-Methode mit schreibendem Namen.
    forbidden = ("Start", "Stop", "Save", "Set", "Write", "Add", "Remove", "Scan", "Quit")
    for kind, members in POLICY.items():
        for name, member in members.items():
            if member.access == "call":
                assert not name.startswith(forbidden), (kind, name)
