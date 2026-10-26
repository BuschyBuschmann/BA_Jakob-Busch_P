"""Tests der Produktiv-Richtlinie: „Nie“-Katalog (U3-1), S1 bis S9 (U3-3, U3-4), Konstanten."""

from __future__ import annotations

import ntpath
from typing import Any

import pytest
from fake_psv_com import FakeKnoten, Welt

from ldv_automation.domaene.parameter import KATALOG, Parameterkatalog, ParameterSpec
from ldv_automation.geraet.com.bindung import dekodiere_prozessliste, psv_treffer
from ldv_automation.geraet.com.konstanten import (
    AcqState,
    SettingsMask,
    lademaske_text,
)
from ldv_automation.geraet.com.richtlinie import (
    NIE_KATALOG,
    PRODUKTIV,
    STANDARD_LADEMASKE,
    erstelle_richtlinie,
    ganzzahl_oder_none,
    lademaske_freigegeben,
    pfad_absolut,
    pfad_unter,
    schreibbegruendungen,
)
from ldv_automation.geraet.com.whitelist import ProxyKontext, WhitelistProxy, oeffne

WURZEL = "/messdaten"
SET = "/vorlagen/a.set"


def _kontext(**ueberschreiben: Any) -> ProxyKontext:
    """Kontext mit allen Freigaben: Verweigerungen kommen dann nur aus der Richtlinie."""
    dateien = {SET, "/messdaten/da.svd"}
    kontext = ProxyKontext(
        start_erlaubt=True,
        schreiben_erlaubt=True,
        messen_erlaubt=True,
        direkt_setzen_erlaubt=True,
        messdaten_wurzel=WURZEL,
        existiert=lambda p: p in dateien,
    )
    kontext.messfreigabe = True
    kontext.eigene_messung_aktiv = True
    for name, wert in ueberschreiben.items():
        setattr(kontext, name, wert)
    return kontext


def _state_gestoppt(kontext: ProxyKontext) -> None:
    kontext.letzter_aufruf = ("Acquisition.State", "get", int(AcqState.STOPPED))


@pytest.mark.parametrize(
    ("typ", "name", "op", "wert"), NIE_KATALOG, ids=[f"{t}.{n}-{o}" for t, n, o, _ in NIE_KATALOG]
)
def test_u3_1_nie_katalog_wird_verweigert_und_protokolliert(
    typ: str, name: str, op: str, wert: Any
) -> None:
    kontext = _kontext()
    _state_gestoppt(kontext)
    welt = Welt()
    # Ein Fake ohne Mitglieder: Würde der Proxy weiterreichen, käme AttributeError statt
    # PermissionError, und das Fake-Protokoll wäre nicht leer.
    leer = FakeKnoten(typ, welt)
    proxy = WhitelistProxy(leer, typ, PRODUKTIV, kontext)
    with pytest.raises(PermissionError, match=r"Default deny"):
        if op == "dispatch":
            oeffne(name, lambda p: pytest.fail("Dispatch darf nicht erfolgen"), PRODUKTIV, kontext)
        elif op == "set":
            setattr(proxy, name, wert)
        elif op == "args":
            getattr(proxy, name)(*wert)
        else:
            getattr(proxy, name)
    verweigert = kontext.verweigerungen()
    assert len(verweigert) == 1
    assert verweigert[0].pfad == f"{typ}.{name}"
    assert kontext.aufrufe() == ()
    assert welt.log == []


def test_u3_1_katalog_ist_nicht_versehentlich_freigegeben() -> None:
    for typ, name, op, _ in NIE_KATALOG:
        if op in ("call", "get"):
            assert name not in PRODUKTIV.objekte.get(typ, {}), (typ, name)
        elif op == "set":
            assert name not in PRODUKTIV.schreiben.get(typ, {}), (typ, name)
        elif op == "dispatch":
            assert name not in PRODUKTIV.einstieg


def test_jede_schreibende_operation_hat_eine_begruendung() -> None:
    begruendungen = schreibbegruendungen()
    erwartet = {
        "AcquisitionInstance.GetApplication": "S1",
        "Settings.Load": "S2",
        "FftValidator.Bandwidth=": "S3",
        "FftValidator.Lines=": "S3",
        "FftProperties.FftAcqPropertiesValidator=": "S3",
        "FftProperties.Bandwidth=": "S4",
        "FftProperties.Lines=": "S4",
        "AverageProperties.Type=": "S5",
        "AverageProperties.Count=": "S5",
        "Acquisition.ScanFileName=": "S6",
        "Acquisition.ScanEx": "S7",
        "Acquisition.Stop": "S8",
        "Settings.Save": "S9",
    }
    assert set(begruendungen) == set(erwartet)
    for pfad, nr in erwartet.items():
        assert begruendungen[pfad].startswith(nr), pfad
    for typ, mitglieder in PRODUKTIV.objekte.items():
        for name, m in mitglieder.items():
            if m.zugriff == "call" and m.liefert is None:
                assert m.begruendung, f"{typ}.{name}"


# --- S1 GetApplication (U3-4) ------------------------------------------------------------


def _aufruf(typ: str, name: str, *args: Any, kontext: ProxyKontext | None = None) -> Any:
    kontext = kontext or _kontext()
    welt = Welt()
    knoten = FakeKnoten(typ, welt, methoden={name: lambda *a: None})
    return getattr(WhitelistProxy(knoten, typ, PRODUKTIV, kontext), name)(*args)


def test_u3_4_get_application_true_ohne_start_psv_verweigert() -> None:
    kontext = _kontext(start_erlaubt=False)
    with pytest.raises(PermissionError, match="--start-psv"):
        _aufruf("AcquisitionInstance", "GetApplication", True, 30000, kontext=kontext)
    assert kontext.verweigerungen()[0].pfad == "AcquisitionInstance.GetApplication"
    _aufruf("AcquisitionInstance", "GetApplication", False, kontext=kontext)
    _aufruf("AcquisitionInstance", "GetApplication", True, 30000)


@pytest.mark.parametrize("args", [(), (1,), ("ja",), (False, 0), (False, True), (False, 1, 2)])
def test_s1_argumentpruefung(args: tuple[Any, ...]) -> None:
    with pytest.raises(PermissionError):
        _aufruf("AcquisitionInstance", "GetApplication", *args)


# --- S2 Settings.Load --------------------------------------------------------------------


def test_s2_settings_load_erlaubt() -> None:
    _aufruf("Settings", "Load", SET, STANDARD_LADEMASKE)
    _aufruf("Settings", "Load", SET, int(SettingsMask.ACQUISITION))


@pytest.mark.parametrize(
    ("args", "grund"),
    [
        ((SET,), "erwartet"),
        ((SET, int(SettingsMask.ALL)), "Lademaske"),
        ((SET, int(SettingsMask.CAMERA)), "Lademaske"),
        ((SET, int(SettingsMask.WINDOWS | SettingsMask.ACQUISITION)), "Lademaske"),
        ((SET, 0), "Lademaske"),
        ((SET, True), "Lademaske"),
        (("/vorlagen/a.svd", 2), r"\.set"),
        (("/vorlagen/fehlt.set", 2), "existiert nicht"),
        (("relativ.set", 2), "absolut"),
        (("", 2), "nicht leeren"),
        ((None, 2), "nicht leeren"),
    ],
)
def test_s2_settings_load_verweigert(args: tuple[Any, ...], grund: str) -> None:
    with pytest.raises(PermissionError, match=grund):
        _aufruf("Settings", "Load", *args)


def test_s2_bis_s5_und_s9_brauchen_schreibfreigabe() -> None:
    kontext = _kontext(schreiben_erlaubt=False)
    with pytest.raises(PermissionError, match="Betriebsart"):
        _aufruf("Settings", "Load", SET, 2, kontext=kontext)
    with pytest.raises(PermissionError, match="Betriebsart"):
        _aufruf("Settings", "Save", "/messdaten/neu.set", kontext=kontext)
    for typ, name, wert in (
        ("FftValidator", "Bandwidth", 5000.0),
        ("FftValidator", "Lines", 400),
        ("FftProperties", "Bandwidth", 5000.0),
        ("AverageProperties", "Type", 1),
        ("AverageProperties", "Count", 10),
    ):
        with pytest.raises(PermissionError, match="Betriebsart"):
            _setze(typ, name, wert, kontext=kontext)
    validator = WhitelistProxy(object(), "FftValidator", PRODUKTIV, kontext)
    with pytest.raises(PermissionError, match="Betriebsart"):
        _setze("FftProperties", "FftAcqPropertiesValidator", validator, kontext=kontext)


# --- S3/S4/S5 Zuweisungen ----------------------------------------------------------------


def _setze(typ: str, name: str, wert: Any, *, kontext: ProxyKontext | None = None) -> Welt:
    kontext = kontext or _kontext()
    welt = Welt()
    setattr(WhitelistProxy(FakeKnoten(typ, welt), typ, PRODUKTIV, kontext), name, wert)
    return welt


@pytest.mark.parametrize(
    ("typ", "name", "wert"),
    [
        ("FftValidator", "Bandwidth", 5000.0),
        ("FftValidator", "Lines", 400),
        ("FftProperties", "Bandwidth", 6250.0),
        ("FftProperties", "Lines", 1600),
        ("AverageProperties", "Type", 2),
        ("AverageProperties", "Count", 3),
        ("AverageProperties", "Count", 10000),
    ],
)
def test_s3_s4_s5_gueltige_werte(typ: str, name: str, wert: Any) -> None:
    assert _setze(typ, name, wert).log == [(typ, name, "set", (wert,))]


@pytest.mark.parametrize(
    ("typ", "name", "wert"),
    [
        ("FftValidator", "Bandwidth", 0.0),
        ("FftValidator", "Bandwidth", -1.0),
        ("FftValidator", "Bandwidth", float("nan")),
        ("FftValidator", "Bandwidth", float("inf")),
        ("FftValidator", "Bandwidth", 5000),
        ("FftValidator", "Bandwidth", True),
        ("FftValidator", "Lines", 0),
        ("FftValidator", "Lines", 400.0),
        ("FftValidator", "Lines", True),
        ("AverageProperties", "Type", 5),
        ("AverageProperties", "Type", "Complex"),
        ("AverageProperties", "Count", 2),
        ("AverageProperties", "Count", 10001),
        ("AverageProperties", "Count", 10.0),
    ],
)
def test_s3_s5_ungueltige_werte(typ: str, name: str, wert: Any) -> None:
    with pytest.raises(PermissionError):
        _setze(typ, name, wert)


def test_s3_validator_uebernahme_nur_mit_validator_proxy() -> None:
    kontext = _kontext()
    validator = WhitelistProxy(object(), "FftValidator", PRODUKTIV, kontext)
    welt = _setze("FftProperties", "FftAcqPropertiesValidator", validator, kontext=kontext)
    assert welt.log[0][:3] == ("FftProperties", "FftAcqPropertiesValidator", "set")
    for falsch in (object(), WhitelistProxy(object(), "FftProperties", PRODUKTIV, kontext)):
        with pytest.raises(PermissionError, match="FftValidator"):
            _setze("FftProperties", "FftAcqPropertiesValidator", falsch, kontext=kontext)


def test_s4_nur_mit_schalter() -> None:
    kontext = _kontext(direkt_setzen_erlaubt=False)
    for name, wert in (("Bandwidth", 5000.0), ("Lines", 400)):
        with pytest.raises(PermissionError, match="Rückfall S4"):
            _setze("FftProperties", name, wert, kontext=kontext)
    _setze("FftValidator", "Lines", 400, kontext=kontext)


# --- S6/S7/S8 (U3-3) ---------------------------------------------------------------------


def test_s6_scan_dateiname_erlaubt() -> None:
    _setze("Acquisition", "ScanFileName", "/messdaten/lauf/01_a.svd")
    _setze("Acquisition", "ScanFileName", "/messdaten/lauf/01_A.SVD")


@pytest.mark.parametrize(
    ("ueberschreiben", "pfad", "grund"),
    [
        ({}, "/messdaten/da.svd", "existiert bereits"),
        ({}, "/anderswo/x.svd", "nicht unter"),
        ({}, "/messdaten/../x.svd", "nicht unter"),
        ({}, "/messdaten", "Endung"),
        ({}, "/messdaten/x.set", "Endung"),
        ({}, "", "nicht leeren"),
        ({"messdaten_wurzel": None}, "/messdaten/x.svd", "kein Messdaten-Wurzelordner"),
        ({"messfreigabe": False}, "/messdaten/x.svd", "Messfreigabe"),
        ({"messen_erlaubt": False}, "/messdaten/x.svd", "keine Messung"),
    ],
)
def test_u3_3_scan_dateiname_verweigert(
    ueberschreiben: dict[str, Any], pfad: str, grund: str
) -> None:
    kontext = _kontext(**ueberschreiben)
    with pytest.raises(PermissionError, match=grund):
        _setze("Acquisition", "ScanFileName", pfad, kontext=kontext)
    assert kontext.verweigerungen()[0].pfad == "Acquisition.ScanFileName"


def test_u3_3_scanex_ohne_messfreigabe_verweigert() -> None:
    kontext = _kontext(messfreigabe=False, eigene_messung_aktiv=False)
    _state_gestoppt(kontext)
    with pytest.raises(PermissionError, match="Messfreigabe"):
        _aufruf("Acquisition", "ScanEx", 0, 0, kontext=kontext)
    assert not kontext.eigene_messung_aktiv


@pytest.mark.parametrize(
    "letzter",
    [
        None,
        ("Acquisition.State", "get", 3),
        ("Acquisition.State", "get", False),
        ("Acquisition.ScanFileName", "get", 0),
    ],
)
def test_s7_state_muss_unmittelbar_davor_stopped_sein(letzter: Any) -> None:
    kontext = _kontext(eigene_messung_aktiv=False, letzter_aufruf=letzter)
    with pytest.raises(PermissionError, match="unmittelbar"):
        _aufruf("Acquisition", "ScanEx", 0, 0, kontext=kontext)


@pytest.mark.parametrize("args", [(), (0,), (0, 0, 0), (False, 0), (0.0, 0)])
def test_s7_argumente(args: tuple[Any, ...]) -> None:
    kontext = _kontext()
    _state_gestoppt(kontext)
    with pytest.raises(PermissionError, match="ScanEx"):
        _aufruf("Acquisition", "ScanEx", *args, kontext=kontext)


def test_s7_erlaubt_setzt_eigene_messung() -> None:
    kontext = _kontext(eigene_messung_aktiv=False)
    _state_gestoppt(kontext)
    _aufruf("Acquisition", "ScanEx", 0, 0, kontext=kontext)
    assert kontext.eigene_messung_aktiv
    kontext = _kontext(messen_erlaubt=False)
    _state_gestoppt(kontext)
    with pytest.raises(PermissionError, match="keine Messung"):
        _aufruf("Acquisition", "ScanEx", 0, 0, kontext=kontext)


def test_u3_3_stop_ohne_eigene_messung_verweigert() -> None:
    kontext = _kontext(eigene_messung_aktiv=False)
    with pytest.raises(PermissionError, match="fremde Messung"):
        _aufruf("Acquisition", "Stop", kontext=kontext)
    with pytest.raises(PermissionError, match="keine Messung"):
        _aufruf("Acquisition", "Stop", kontext=_kontext(messen_erlaubt=False))
    with pytest.raises(PermissionError, match="keine Argumente"):
        _aufruf("Acquisition", "Stop", 1)
    _aufruf("Acquisition", "Stop")


# --- S9 Settings.Save --------------------------------------------------------------------


def test_s9_settings_save() -> None:
    _aufruf("Settings", "Save", "/messdaten/lauf/01.einstellungen.set")
    for args, grund in (
        (("/messdaten/da.svd",), "Endung"),
        (("/vorlagen/a.set",), "nicht unter"),
        ((), "erwartet"),
    ):
        with pytest.raises(PermissionError, match=grund):
            _aufruf("Settings", "Save", *args)


# --- Hilfen ------------------------------------------------------------------------------


def test_pfad_unter() -> None:
    assert pfad_unter("/a/b/c.svd", "/a")
    assert pfad_unter("/a/b/../c.svd", "/a")
    assert not pfad_unter("/a", "/a")
    assert not pfad_unter("/ab/c.svd", "/a")
    assert not pfad_unter("/a/../b.svd", "/a")


def test_pfad_unter_mit_symlink(tmp_path: Any) -> None:
    wurzel = tmp_path / "wurzel"
    wurzel.mkdir()
    draussen = tmp_path / "draussen"
    draussen.mkdir()
    (wurzel / "link").symlink_to(draussen)
    assert not pfad_unter(str(wurzel / "link" / "x.svd"), str(wurzel))


def test_pfad_unter_verschiedene_laufwerke(monkeypatch: pytest.MonkeyPatch) -> None:
    import os.path

    def boom(_: list[str]) -> str:
        raise ValueError("Paths don't have the same drive")

    monkeypatch.setattr(os.path, "commonpath", boom)
    assert not pfad_unter("/a/b", "/a")


@pytest.mark.parametrize(
    ("maske", "text"),
    [
        (STANDARD_LADEMASKE, "Acquisition|Alignment|APS|2DAlignment|3DAlignment"),
        (2, "Acquisition"),
        (65535, "All"),
        (0, "None"),
        (64 | 2, "Acquisition|Camera"),
        (2 | 1, "Acquisition|1"),
    ],
)
def test_lademaske_text(maske: int, text: str) -> None:
    assert lademaske_text(maske) == text


def test_prozessliste() -> None:
    assert psv_treffer('"explorer.exe","1"\n"PSV.exe","4711","Console"\n') == ("PSV.exe",)
    assert psv_treffer('"explorer.exe","1"\n\n"python.exe","2"\n') == ()
    assert psv_treffer("") == ()
    assert psv_treffer('"PSV.exe","1"\n"mypsvtool.exe","2"\n') == ("PSV.exe", "mypsvtool.exe")


def test_prozessliste_dekodierung() -> None:
    roh = '"Übersicht.exe","1"\n"PSV.exe","2"\n'.encode("cp850")
    text = dekodiere_prozessliste(roh, "cp850")
    assert text is not None and psv_treffer(text) == ("PSV.exe",)
    assert dekodiere_prozessliste(b"\xff\xfe\xfa", "utf-8") is None
    assert dekodiere_prozessliste(b"x", "gibt-es-nicht") is None


@pytest.mark.parametrize("index", [0, -1, "1", True])
def test_collection_index_ist_1_basiert(index: Any) -> None:
    with pytest.raises(PermissionError, match="1-basierten"):
        _aufruf("ChannelsProperties", "Item", index)


@pytest.mark.parametrize(
    ("pfad", "absolut"),
    [
        (r"D:\ldv_messdaten\x.svd", True),
        (r"\\server\freigabe\x.svd", True),
        (r"\daten\x.svd", False),
        ("/daten/x.svd", False),
        (r"D:daten\x.svd", False),
        (r"daten\x.svd", False),
    ],
)
def test_windows_pfade_brauchen_laufwerk_oder_unc(pfad: str, absolut: bool) -> None:
    assert pfad_absolut(pfad, ntpath) is absolut


def test_pfad_unter_windows() -> None:
    w = r"D:\ldv_messdaten"
    assert pfad_unter(r"D:\ldv_messdaten\lauf\01.svd", w, ntpath)
    assert pfad_unter(r"d:\LDV_MESSDATEN\01.svd", w, ntpath)
    assert not pfad_unter(r"\ldv_messdaten\01.svd", w, ntpath)
    assert not pfad_unter(r"E:\ldv_messdaten\01.svd", w, ntpath)
    assert not pfad_unter(r"D:\ldv_messdaten\..\01.svd", w, ntpath)
    assert not pfad_unter(r"\ldv_messdaten\01.svd", r"\ldv_messdaten", ntpath)


def test_wurzel_ohne_laufwerk_bzw_relativ_wird_verweigert() -> None:
    kontext = _kontext(messdaten_wurzel="messdaten")
    with pytest.raises(PermissionError, match="Wurzelordner ist kein absoluter Pfad"):
        _setze("Acquisition", "ScanFileName", "/messdaten/x.svd", kontext=kontext)


@pytest.mark.parametrize(
    ("maske", "frei"),
    [
        (STANDARD_LADEMASKE, True),
        (312, True),
        (2 | 312, True),
        (8, False),
        (256, False),
        (2 | 8, False),
        (312 & ~8, False),
        (64, False),
        (0, False),
        (-2, False),
    ],
)
def test_s2_nur_ganze_ladegruppen(maske: int, frei: bool) -> None:
    assert lademaske_freigegeben(maske) is frei
    if not frei:
        with pytest.raises(PermissionError, match="Lademaske"):
            _aufruf("Settings", "Load", SET, maske)


def test_s7_ganzzahliger_float_wie_im_adapter() -> None:
    kontext = _kontext(eigene_messung_aktiv=False, letzter_aufruf=("Acquisition.State", "get", 0.0))
    _aufruf("Acquisition", "ScanEx", 0, 0, kontext=kontext)
    assert ganzzahl_oder_none(0.0) == 0 and ganzzahl_oder_none(0.5) is None
    assert ganzzahl_oder_none(False) is None and ganzzahl_oder_none("0") is None


def test_s3_bereich_aus_dem_uebergebenen_katalog() -> None:
    katalog = Parameterkatalog(KATALOG)
    katalog.registrieren(
        ParameterSpec(
            schluessel="fft.linien", typ="int", einheit="", com_gruppe="fft", minimum=1, maximum=800
        ),
        ersetzen=True,
    )
    eigene = erstelle_richtlinie(katalog)
    kontext = _kontext()
    proxy = WhitelistProxy(FakeKnoten("FftValidator", Welt()), "FftValidator", eigene, kontext)
    with pytest.raises(PermissionError, match=r"fft\.linien"):
        proxy.Lines = 1600
    _setze("FftValidator", "Lines", 1600)  # Standardkatalog erlaubt es
    direkt = WhitelistProxy(FakeKnoten("FftProperties", Welt()), "FftProperties", eigene, kontext)
    with pytest.raises(PermissionError, match=r"fft\.linien"):
        direkt.Lines = 1600
