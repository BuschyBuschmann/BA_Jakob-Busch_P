"""Tests des COM-Adapters gegen den COM-Fake (U3-2, U3-4, U3-5, U3-6 und Vertrag)."""

from __future__ import annotations

import threading
from typing import Any

import pytest
from fake_psv_com import FakeBindung, FakeComError, FakeKnoten, FakePsv, Welt, baue_psv

from ldv_automation.domaene.parameter import (
    KATALOG,
    Parameterkatalog,
    ParameterSpec,
    ParameterWert,
)
from ldv_automation.geraet.com.adapter import (
    MAX_KANAELE,
    ComBetriebsart,
    ComKonfiguration,
    PsvComGeraet,
)
from ldv_automation.geraet.com.richtlinie import PRODUKTIV
from ldv_automation.geraet.schnittstelle import (
    AbweichungFehler,
    GeraeteFehler,
    GeraeteZustand,
    GeraetNichtBereitFehler,
    Messgeraet,
    VerweigertFehler,
)

WURZEL = "/messdaten"
SET = "/vorlagen/platte_3x3.set"
ZIEL = "/messdaten/2026-11-02_120000_test/01_platte.svd"
NACHWEIS = "/messdaten/2026-11-02_120000_test/01_platte.einstellungen.set"


def _geraet(
    art: ComBetriebsart = ComBetriebsart.MESSEN,
    *,
    prozess: bool | tuple[str, ...] | None = True,
    start: bool = False,
    rueckfall: bool = False,
    katalog: Parameterkatalog = KATALOG,
    **psv: Any,
) -> tuple[PsvComGeraet, FakePsv, FakeBindung]:
    welt = Welt()
    welt.dateien.add(SET)
    fake = baue_psv(welt, **psv)
    bindung = FakeBindung(fake, prozess=prozess)
    geraet = PsvComGeraet(
        bindung,
        ComKonfiguration(
            betriebsart=art,
            messdaten_wurzel=WURZEL,
            start_psv_erlaubt=start,
            validator_rueckfall_direkt=rueckfall,
            katalog=katalog,
            existiert=lambda p: p in welt.dateien,
        ),
    )
    return geraet, fake, bindung


def _pfade(geraet: PsvComGeraet) -> list[str]:
    return [f"{a.pfad}:{a.op}" for a in geraet.aufrufe()]


PARAMETER: dict[str, ParameterWert] = {
    "fft.bandbreite_hz": 5000.0,
    "fft.linien": 800,
    "mittelung.typ": "Complex",
    "mittelung.anzahl": 20,
}

# fmt: off
ERWARTETE_FOLGE = [
    # V0 Verbinden (Prozessprüfung ohne COM, dann Dispatch)
    "Dispatch.PSV.AcquisitionInstance:dispatch",
    "AcquisitionInstance.IsRunning:get", "AcquisitionInstance.GetApplication:call",
    # V1 Version, Modus, Suppress, Zustand, Hardware
    "Application.Version:get", "Application.Mode:get",
    "Application.SuppressMessagesForAutomation:get", "Application.Acquisition:get",
    "Acquisition.State:get", "Acquisition.Infos:get", "Infos.HasHardware:get",
    "Infos.Hardware:get",
    "Hardware.AcqBoardName:get", "Hardware.AcqBoardFirmwareVersion:get",
    "Hardware.FrontEnd:get", "Hardware.FrontEndFirmwareVersion:get",
    "Hardware.GeneratorName:get", "Hardware.ScanHeadType:get",
    "Hardware.SensorHeadNames:get", "Hardware.SensorHeadSerialNumbers:get",
    "Hardware.SensorHeadVersions:get",
    # M2 Zustand (Steuerung)
    "Acquisition.State:get",
    # M3 Laden (Adapter prüft State erneut)
    "Acquisition.State:get", "Application.Settings:get", "Settings.Load:call",
    # M4 Parameter: Validator, dann Mittelung
    "Acquisition.ActiveProperties:get", "AcquisitionProperties.HasFftProperties:get",
    "AcquisitionProperties.FftProperties:get",
    "FftProperties.FftAcqPropertiesValidator:exists",
    "FftProperties.FftAcqPropertiesValidator:get",
    "FftValidator.Bandwidth:set", "FftValidator.Lines:set",
    "FftProperties.FftAcqPropertiesValidator:set",
    "AcquisitionProperties.HasAverageProperties:get",
    "AcquisitionProperties.AverageProperties:get",
    "AverageProperties.Type:set", "AverageProperties.Count:set",
    # M5 Zurücklesen
    "Acquisition.ActiveProperties:get", "AcquisitionProperties.HasFftProperties:get",
    "AcquisitionProperties.FftProperties:get", "FftProperties.Bandwidth:get",
    "FftProperties.Lines:get", "AcquisitionProperties.HasAverageProperties:get",
    "AcquisitionProperties.AverageProperties:get", "AverageProperties.Type:get",
    "AverageProperties.Count:get",
    # M5 Einstellungsstand (nur lesend)
    "Acquisition.Mode:get", "Acquisition.GeneratorsOn:get",
    "Acquisition.ActiveProperties:get",
    "AcquisitionProperties.HasFftProperties:get", "AcquisitionProperties.FftProperties:get",
    "FftProperties.Bandwidth:get", "FftProperties.StartFrequency:get",
    "FftProperties.EndFrequency:get", "FftProperties.Lines:get", "FftProperties.Overlap:get",
    "FftProperties.SampleFrequency:get", "FftProperties.SampleResolution:get",
    "FftProperties.SampleTime:get",
    "AcquisitionProperties.HasAverageProperties:get",
    "AcquisitionProperties.AverageProperties:get",
    "AverageProperties.Type:get", "AverageProperties.Count:get",
    "AcquisitionProperties.HasGeneralProperties:get",
    "AcquisitionProperties.GeneralProperties:get",
    "GeneralProperties.AutoRemeasure:get", "GeneralProperties.AutoRemeasureAutoRange:get",
    "GeneralProperties.SaveTimeDataForScan:get",
    "GeneralProperties.PrincipalComponentAnalysis:get",
    "AcquisitionProperties.HasTriggerProperties:get",
    "AcquisitionProperties.TriggerProperties:get",
    "TriggerProperties.Source:get", "TriggerProperties.Edge:get", "TriggerProperties.Level:get",
    "TriggerProperties.PreTrigger:get", "TriggerProperties.PhaseFromRef:get",
    "TriggerProperties.AnalogSourceChannel:get",
    "AcquisitionProperties.HasSignalEnhancementProperties:get",
    "AcquisitionProperties.SignalEnhancementProperties:get",
    "SEProperties.Mode:get", "SEProperties.SpeckleTracking:get",
    "AcquisitionProperties.HasChannelsProperties:get",
    "AcquisitionProperties.ChannelsProperties:get", "ChannelsProperties.Count:get",
    *[
        x
        for _ in (1, 2)
        for x in (
            "ChannelsProperties.Item:call", "Channel.Name:get", "Channel.Active:get",
            "Channel.Reference:get", "Channel.Quantity:get", "Channel.Unit:get",
            "Channel.InputRange:get", "Channel.Calibration:get",
            "Channel.DirectionOfVibration:get", "Channel.WindowFunction:get",
        )
    ],
    "AcquisitionProperties.HasGeneratorsProperties:get",
    "AcquisitionProperties.GeneratorsProperties:get", "GeneratorsProperties.Count:get",
    "GeneratorsProperties.Item:call", "Generator.Active:get", "Generator.Amplitude:get",
    "Generator.Waveform:get", "Waveform.Type:get",
    "Acquisition.Infos:get", "Infos.HasMeasPoints:get", "Infos.MeasPoints:get",
    "MeasPoints.Count:get",
    # M6 Nachweis
    "Application.Settings:get", "Settings.Save:call",
    # M7 Messfreigabe: kein COM; M8 Zieldatei, Zurücklesen, State unmittelbar vor ScanEx
    "Acquisition.State:get", "Acquisition.ScanFileName:set", "Acquisition.ScanFileName:get",
    "Acquisition.State:get", "Acquisition.ScanEx:call",
    # M9 Polling bis Stopped (M11 Ende)
    "Acquisition.State:get", "Acquisition.State:get",
]
# fmt: on


def test_u3_2_vollstaendiger_ablauf_erzeugt_genau_die_aufruffolge() -> None:
    geraet, fake, _ = _geraet()
    info = geraet.verbinde()
    assert info.zustand is GeraeteZustand.GESTOPPT
    assert geraet.zustand() is GeraeteZustand.GESTOPPT  # M2
    geraet.lade_einstellungen(SET)  # M3
    geraet.setze_parameter(PARAMETER)  # M4
    ist = geraet.lies_parameter(list(PARAMETER))  # M5
    for k, soll in PARAMETER.items():
        assert KATALOG.spec(k).stimmt_ueberein(soll, ist[k]), k
    stand = geraet.lies_einstellungsstand()  # M5
    geraet.speichere_einstellungen(NACHWEIS)  # M6
    geraet.setze_messfreigabe(True)  # M7
    geraet.starte_scan(ZIEL)  # M8
    zustaende = [geraet.zustand(), geraet.zustand()]  # M9
    assert zustaende == [GeraeteZustand.SCANNT, GeraeteZustand.GESTOPPT]  # M11
    assert ZIEL in fake.welt.dateien

    assert _pfade(geraet) == ERWARTETE_FOLGE
    assert geraet.verweigerungen() == ()
    for a in geraet.aufrufe():
        typ, name = a.pfad.split(".", 1)
        if typ == "Dispatch":
            assert name in PRODUKTIV.einstieg
        elif a.op == "set":
            assert name in PRODUKTIV.schreiben[typ]
        elif a.op == "exists":
            assert name in PRODUKTIV.existenz[typ]
        else:
            assert name in PRODUKTIV.objekte[typ]
        assert a.fehler is None
    assert fake.geladen == [(SET, geraet.lademaske)]
    assert fake.gespeichert == [NACHWEIS]
    assert stand.modus == "Fft"
    assert info.lademaske == "Acquisition|Alignment|APS|2DAlignment|3DAlignment"


def test_ist_ein_messgeraet_und_ohne_ereignisbetrieb() -> None:
    geraet, _, _ = _geraet()
    assert isinstance(geraet, Messgeraet)
    assert geraet.fortschritt() is None
    assert geraet.hole_meldungen() == ()
    assert geraet.haengender_aufruf_seit_s() is None
    assert geraet.betriebsart is ComBetriebsart.MESSEN


def test_verbinde_liest_info_und_ist_idempotent() -> None:
    geraet, _, bindung = _geraet()
    info = geraet.verbinde()
    assert info.psv_version == "10.4.0.0-FAKE"
    assert info.erfassungsmodus and info.meldungen_unterdrueckt
    assert info.hardware["sensorkopf_seriennummern"] == "('1', '2', '3')"
    assert info.hardware["erfassungskarte"] == "PCI-4461"
    anzahl = len(geraet.aufrufe())
    assert geraet.verbinde() is info
    assert len(geraet.aufrufe()) == anzahl
    assert bindung.init == 1


def test_trennen_ist_idempotent_und_gibt_thread_frei() -> None:
    geraet, _, bindung = _geraet()
    geraet.trenne()
    assert bindung.ende == 0
    geraet.verbinde()
    geraet.setze_messfreigabe(True)
    geraet.trenne()
    geraet.trenne()
    assert bindung.ende == 1
    with pytest.raises(GeraeteFehler, match="Nicht mit PSV verbunden"):
        geraet.zustand()


@pytest.mark.parametrize("prozess", [False, None])
def test_u3_4_ohne_psv_prozess_kein_dispatch(prozess: bool | None) -> None:
    geraet, fake, bindung = _geraet(prozess=prozess)
    with pytest.raises(GeraeteFehler, match="Prozessprüfung"):
        geraet.verbinde()
    assert fake.welt.dispatches == []
    assert fake.welt.log == []
    assert bindung.init == 0


def test_u3_4_psv_laeuft_nicht_ohne_start_freigabe() -> None:
    geraet, fake, _ = _geraet(laeuft=False)
    with pytest.raises(GeraeteFehler, match="IsRunning=False"):
        geraet.verbinde()
    assert "AcquisitionInstance.GetApplication:call" not in fake.welt.ops()
    assert not fake.gestartet


def test_u3_4_start_nur_mit_freigabe() -> None:
    geraet, fake, _ = _geraet(laeuft=False, prozess=False, start=True)
    geraet.verbinde()
    assert fake.gestartet
    aufruf = next(a for a in geraet.aufrufe() if a.pfad.endswith("GetApplication"))
    assert aufruf.argumente == ("True", "30000")


def test_verbinde_fehlende_objekte() -> None:
    geraet, fake, _ = _geraet()
    fake.inst._methoden["GetApplication"] = lambda *a: None
    with pytest.raises(GeraeteFehler, match="keine Anwendung"):
        geraet.verbinde()
    geraet, fake, _ = _geraet()
    fake.app._props["Acquisition"] = None
    with pytest.raises(GeraeteFehler, match="Acquisition nicht verfügbar"):
        geraet.verbinde()


def test_verbinde_raeumt_bei_fehler_im_zustand_auf() -> None:
    geraet, _fake, _ = _geraet(zustand=42)
    with pytest.raises(GeraeteFehler, match=r"Unbekannter Acquisition\.State"):
        geraet.verbinde()
    with pytest.raises(GeraeteFehler, match="Nicht mit PSV verbunden"):
        geraet.zustand()


def test_hardware_fehlend_oder_teilweise_lesbar() -> None:
    geraet, _, _ = _geraet(hardware=False)
    assert geraet.verbinde().hardware == {
        "hinweis": "Infos.Hardware nicht verfügbar",
        "psv_prozesse": "PSV.exe",
    }
    geraet, fake, _ = _geraet()
    fake.welt.fehler[("Hardware", "FrontEnd")] = FakeComError("nicht verfügbar")
    hw = geraet.verbinde().hardware
    assert hw["nicht_lesbar"] == "FrontEnd"
    assert "frontend" not in hw
    assert hw["frontend_firmware"] == "2.1"


@pytest.mark.parametrize(
    ("state", "erwartet"),
    [
        (0, GeraeteZustand.GESTOPPT),
        (3, GeraeteZustand.SCANNT),
        (4, GeraeteZustand.SCANNT),
        (5, GeraeteZustand.SCANNT),
        (1, GeraeteZustand.BESCHAEFTIGT),
        (6, GeraeteZustand.BESCHAEFTIGT),
    ],
)
def test_zustand_abbildung(state: int, erwartet: GeraeteZustand) -> None:
    geraet, fake, _ = _geraet()
    geraet.verbinde()
    fake.zustand = state
    assert geraet.zustand() is erwartet


@pytest.mark.parametrize("wert", [99, "Stopped", True, 1.5])
def test_zustand_unbekannte_werte_sind_fehler(wert: object) -> None:
    geraet, fake, _ = _geraet()
    geraet.verbinde()
    fake.acq._getter["State"] = lambda: wert
    with pytest.raises(GeraeteFehler):
        geraet.zustand()


def test_zustand_float_ganzzahl_wird_akzeptiert() -> None:
    geraet, fake, _ = _geraet()
    geraet.verbinde()
    fake.acq._getter["State"] = lambda: 3.0
    assert geraet.zustand() is GeraeteZustand.SCANNT


def test_u3_5_ohne_validator_und_ohne_schalter_validator_fehlt() -> None:
    geraet, fake, _ = _geraet(validator=False)
    geraet.verbinde()
    with pytest.raises(GeraeteFehler, match="Validator fehlt"):
        geraet.setze_parameter({"fft.bandbreite_hz": 2500.0})
    assert not [o for o in fake.welt.schreibende() if o.startswith("FftProperties")]


def test_u3_5_ohne_validator_mit_schalter_s4() -> None:
    geraet, fake, _ = _geraet(validator=False, rueckfall=True)
    geraet.verbinde()
    geraet.setze_parameter({"fft.bandbreite_hz": 2400.0, "fft.linien": 1600})
    assert "FftProperties.Bandwidth:set" in fake.welt.schreibende()
    assert "FftProperties.Lines:set" in fake.welt.schreibende()
    assert geraet.lies_parameter(["fft.bandbreite_hz", "fft.linien"]) == {
        "fft.bandbreite_hz": 2500.0,  # eingerastet
        "fft.linien": 1600,
    }


def test_u3_5_mit_validator_wird_s4_nicht_genutzt() -> None:
    geraet, fake, _ = _geraet(rueckfall=True)
    geraet.verbinde()
    geraet.setze_parameter({"fft.linien": 1600})
    assert "FftProperties.Lines:set" not in fake.welt.schreibende()
    assert "FftValidator.Lines:set" in fake.welt.schreibende()


def test_validator_liefert_nichts() -> None:
    geraet, fake, _ = _geraet()
    geraet.verbinde()
    fake.fft._getter["FftAcqPropertiesValidator"] = lambda: None
    with pytest.raises(GeraeteFehler, match="kein Objekt"):
        geraet.setze_parameter({"fft.linien": 800})


def test_einrasten_wird_beim_zuruecklesen_sichtbar() -> None:
    geraet, _, _ = _geraet()
    geraet.verbinde()
    geraet.setze_parameter({"fft.bandbreite_hz": 5600.0})
    ist = geraet.lies_parameter(["fft.bandbreite_hz"])
    assert ist == {"fft.bandbreite_hz": 5000.0}
    assert not KATALOG.spec("fft.bandbreite_hz").stimmt_ueberein(5600.0, ist["fft.bandbreite_hz"])


def test_lies_parameter_typen() -> None:
    geraet, fake, _ = _geraet()
    geraet.verbinde()
    fake.fft._getter["Lines"] = lambda: 800.0  # COM kann Ganzzahlen als Double liefern
    ist = geraet.lies_parameter(list(PARAMETER))
    assert type(ist["fft.bandbreite_hz"]) is float
    assert type(ist["fft.linien"]) is int and ist["fft.linien"] == 800
    assert type(ist["mittelung.anzahl"]) is int
    assert ist["mittelung.typ"] == "Complex"
    assert geraet.lies_parameter([]) == {}


@pytest.mark.parametrize(
    ("knoten", "name", "wert", "schluessel"),
    [
        ("fft", "Lines", 800.5, "fft.linien"),
        ("fft", "Bandwidth", "5000", "fft.bandbreite_hz"),
        ("avg", "Type", 9, "mittelung.typ"),
        ("avg", "Count", None, "mittelung.anzahl"),
    ],
)
def test_lies_parameter_ungueltige_werte(
    knoten: str, name: str, wert: object, schluessel: str
) -> None:
    geraet, fake, _ = _geraet()
    geraet.verbinde()
    getattr(fake, knoten)._getter[name] = lambda: wert
    with pytest.raises(GeraeteFehler):
        geraet.lies_parameter([schluessel])


def test_setze_parameter_ungueltig_ohne_geraetezugriff() -> None:
    geraet, fake, _ = _geraet()
    geraet.verbinde()
    vorher = len(fake.welt.log)
    with pytest.raises(GeraeteFehler, match=r"mittelung\.anzahl"):
        geraet.setze_parameter({"mittelung.anzahl": 2})
    with pytest.raises(GeraeteFehler, match="Unbekannter Parameter"):
        geraet.setze_parameter({"fft.von_hz": 1.0})
    with pytest.raises(GeraeteFehler, match="Unbekannter Parameter"):
        geraet.lies_parameter(["fft.von_hz"])
    geraet.setze_parameter({})
    assert len(fake.welt.log) == vorher


def test_katalogparameter_ohne_com_zuordnung() -> None:
    katalog = Parameterkatalog(KATALOG)
    katalog.registrieren(
        ParameterSpec(schluessel="fft.von_hz", typ="float", einheit="Hz", com_gruppe="fft")
    )
    geraet, _, _ = _geraet(katalog=katalog)
    geraet.verbinde()
    with pytest.raises(GeraeteFehler, match="keine COM-Zuordnung"):
        geraet.setze_parameter({"fft.von_hz": 10.0})


def test_gruppe_fehlt_im_aktiven_modus() -> None:
    geraet, fake, _ = _geraet()
    geraet.verbinde()
    fake.props._props["HasAverageProperties"] = False
    with pytest.raises(GeraeteFehler, match="AverageProperties"):
        geraet.setze_parameter({"mittelung.anzahl": 5})
    fake.props._props["HasAverageProperties"] = True
    fake.props._props["AverageProperties"] = None
    with pytest.raises(GeraeteFehler, match="AverageProperties nicht verfügbar"):
        geraet.lies_parameter(["mittelung.anzahl"])
    fake.acq._props["ActiveProperties"] = None
    with pytest.raises(GeraeteFehler, match="ActiveProperties"):
        geraet.lies_parameter(["mittelung.anzahl"])


def test_u3_6_com_ausnahme_wird_geraetefehler_mit_kontext() -> None:
    geraet, fake, _ = _geraet()
    geraet.verbinde()
    fake.welt.fehler[("Settings", "Load")] = FakeComError(
        "Die Datei passt nicht zur Erfassungskarte.", hresult=-2147024809
    )
    with pytest.raises(GeraeteFehler) as info:
        geraet.lade_einstellungen(SET)
    fehler = info.value
    assert type(fehler) is GeraeteFehler
    assert fehler.methode == "Settings.Load"
    assert fehler.argumente == (repr(SET), repr(geraet.lademaske))
    assert fehler.hresult == -2147024809
    assert fehler.excepinfo == "Die Datei passt nicht zur Erfassungskarte."
    assert fehler.text == "Die Datei passt nicht zur Erfassungskarte."
    assert isinstance(fehler.__cause__.__cause__, FakeComError)  # type: ignore[union-attr]


def test_u3_6_ungueltige_mittelung_meldet_geraetetext() -> None:
    geraet, fake, _ = _geraet()
    geraet.verbinde()
    fake.avg._setter["Count"] = lambda w: (_ for _ in ()).throw(FakeComError("ungültig"))
    with pytest.raises(GeraeteFehler) as info:
        geraet.setze_parameter({"mittelung.anzahl": 5})
    assert info.value.methode == "AverageProperties.Count"
    assert info.value.argumente == ("5",)
    assert info.value.excepinfo == "ungültig"


@pytest.mark.parametrize(
    "aktion",
    [
        lambda g: g.lade_einstellungen(SET),
        lambda g: g.setze_parameter({"fft.linien": 800}),
        lambda g: g.speichere_einstellungen(NACHWEIS),
        lambda g: g.starte_scan(ZIEL),
        lambda g: g.setze_messfreigabe(True),
    ],
)
def test_nur_lesen_verweigert_alle_schreibenden(aktion: Any) -> None:
    geraet, fake, _ = _geraet(ComBetriebsart.NUR_LESEN)
    geraet.verbinde()
    with pytest.raises(VerweigertFehler):
        aktion(geraet)
    assert [o for o in fake.welt.schreibende() if not o.endswith("GetApplication:call")] == []
    geraet.setze_messfreigabe(False)
    assert geraet.stoppe() is False


def test_trockenlauf_laedt_und_setzt_aber_scannt_nie() -> None:
    geraet, fake, _ = _geraet(ComBetriebsart.TROCKENLAUF)
    geraet.verbinde()
    geraet.lade_einstellungen(SET)
    geraet.setze_parameter(PARAMETER)
    geraet.speichere_einstellungen(NACHWEIS)
    with pytest.raises(VerweigertFehler, match="trockenlauf"):
        geraet.starte_scan(ZIEL)
    with pytest.raises(VerweigertFehler):
        geraet.setze_messfreigabe(True)
    assert geraet.stoppe() is False
    assert not [o for o in fake.welt.schreibende() if "Scan" in o or "Stop" in o]


def test_suppress_aus_oder_falscher_modus_sperrt_schreiben() -> None:
    geraet, fake, _ = _geraet(unterdrueckt=False)
    assert geraet.verbinde().meldungen_unterdrueckt is False
    with pytest.raises(VerweigertFehler, match="SuppressMessagesForAutomation"):
        geraet.lade_einstellungen(SET)
    geraet, fake, _ = _geraet(app_modus=0)
    assert geraet.verbinde().erfassungsmodus is False
    with pytest.raises(VerweigertFehler, match="Erfassungsmodus"):
        geraet.setze_parameter({"fft.linien": 800})
    assert fake.geladen == []


def test_laden_bei_fremder_messung_nicht_bereit() -> None:
    geraet, fake, _ = _geraet()
    geraet.verbinde()
    fake.zustand = 2
    with pytest.raises(GeraetNichtBereitFehler):
        geraet.lade_einstellungen(SET)
    assert fake.geladen == []


def test_laden_unbekannte_datei_verweigert_der_proxy() -> None:
    geraet, fake, _ = _geraet()
    geraet.verbinde()
    with pytest.raises(VerweigertFehler, match="existiert nicht") as info:
        geraet.lade_einstellungen("/vorlagen/fehlt.set")
    assert info.value.methode == "lade_einstellungen"
    assert fake.geladen == []
    assert geraet.verweigerungen()[-1].pfad == "Settings.Load"


def test_speichern_ueberschreibt_nie() -> None:
    geraet, fake, _ = _geraet()
    geraet.verbinde()
    fake.welt.dateien.add(NACHWEIS)
    with pytest.raises(VerweigertFehler, match="existiert bereits"):
        geraet.speichere_einstellungen(NACHWEIS)
    with pytest.raises(VerweigertFehler, match="Messdaten-Wurzelordner"):
        geraet.speichere_einstellungen("/anderswo/x.set")
    assert fake.gespeichert == []


def _bereit(**psv: Any) -> tuple[PsvComGeraet, FakePsv]:
    geraet, fake, _ = _geraet(**psv)
    geraet.verbinde()
    geraet.setze_messfreigabe(True)
    return geraet, fake


def test_starte_scan_ohne_freigabe() -> None:
    geraet, fake, _ = _geraet()
    geraet.verbinde()
    with pytest.raises(VerweigertFehler, match="Messfreigabe"):
        geraet.starte_scan(ZIEL)
    geraet.setze_messfreigabe(True)
    geraet.setze_messfreigabe(False)
    with pytest.raises(VerweigertFehler, match="Messfreigabe"):
        geraet.starte_scan(ZIEL)
    assert "Acquisition.ScanEx:call" not in fake.welt.ops()


def test_starte_scan_bei_fremder_messung_nicht_bereit() -> None:
    geraet, fake = _bereit(zustand=3)
    with pytest.raises(GeraetNichtBereitFehler):
        geraet.starte_scan(ZIEL)
    assert fake.welt.schreibende() == ["AcquisitionInstance.GetApplication:call"]


@pytest.mark.parametrize("ziel", ["/anderswo/x.svd", "/messdaten", "/messdaten/../x.svd"])
def test_starte_scan_ausserhalb_der_wurzel(ziel: str) -> None:
    geraet, fake = _bereit()
    with pytest.raises(VerweigertFehler, match="Wurzel"):
        geraet.starte_scan(ziel)
    assert "Acquisition.ScanFileName:set" not in fake.welt.ops()


def test_starte_scan_vorhandene_zieldatei() -> None:
    geraet, fake = _bereit()
    fake.welt.dateien.add(ZIEL)
    with pytest.raises(VerweigertFehler, match="existiert bereits"):
        geraet.starte_scan(ZIEL)
    assert "Acquisition.ScanFileName:set" not in fake.welt.ops()


def test_starte_scan_falsche_endung_verweigert_der_proxy() -> None:
    geraet, fake = _bereit()
    with pytest.raises(VerweigertFehler, match="Endung"):
        geraet.starte_scan("/messdaten/x.txt")
    assert "Acquisition.ScanEx:call" not in fake.welt.ops()


def test_starte_scan_abweichender_dateiname_kein_scanex() -> None:
    geraet, fake = _bereit(dateiname_echo=lambda p: p + ".anders.svd")
    with pytest.raises(AbweichungFehler, match="ScanFileName"):
        geraet.starte_scan(ZIEL)
    assert "Acquisition.ScanEx:call" not in fake.welt.ops()


def test_starte_scan_ohne_wurzel_konfiguration() -> None:
    welt = Welt()
    fake = baue_psv(welt)
    geraet = PsvComGeraet(
        FakeBindung(fake),
        ComKonfiguration(betriebsart=ComBetriebsart.MESSEN, existiert=lambda p: False),
    )
    geraet.verbinde()
    geraet.setze_messfreigabe(True)
    with pytest.raises(VerweigertFehler, match="Wurzel"):
        geraet.starte_scan(ZIEL)


def test_stoppe_nur_eigene_messung() -> None:
    geraet, fake = _bereit()
    assert geraet.stoppe() is False  # kein Scan
    fake.zustand = 3  # fremder Scan
    assert geraet.stoppe() is False
    assert "Acquisition.Stop:call" not in fake.welt.ops()
    assert geraet.verweigerungen() == ()


def test_stoppe_eigene_messung_blockiert_nicht() -> None:
    geraet, fake = _bereit(scan_polls=100)
    geraet.starte_scan(ZIEL)
    assert geraet.zustand() is GeraeteZustand.SCANNT
    assert geraet.stoppe() is True
    assert fake.welt.ops()[-1] == "Acquisition.Stop:call"  # kein Polling im Adapter
    assert geraet.zustand() is GeraeteZustand.GESTOPPT
    assert geraet.stoppe() is False  # eigener Scan beendet


def test_stoppe_wirkungslos_wird_nicht_im_adapter_erkannt() -> None:
    geraet, fake = _bereit(scan_polls=100)
    fake.stop_wirkt = False
    geraet.starte_scan(ZIEL)
    assert geraet.stoppe() is True
    assert geraet.zustand() is GeraeteZustand.SCANNT
    assert geraet.stoppe() is True  # Steuerung entscheidet über GERAET_UNKLAR


def test_stoppe_nach_natuerlichem_scanende() -> None:
    geraet, fake = _bereit(scan_polls=1)
    geraet.starte_scan(ZIEL)
    assert geraet.zustand() is GeraeteZustand.GESTOPPT
    assert geraet.stoppe() is False
    assert "Acquisition.Stop:call" not in fake.welt.ops()


def test_stoppe_com_fehler() -> None:
    geraet, fake = _bereit()
    geraet.starte_scan(ZIEL)
    fake.welt.fehler[("Acquisition", "Stop")] = FakeComError("busy")
    with pytest.raises(GeraeteFehler, match="busy") as info:
        geraet.stoppe()
    assert info.value.methode == "Acquisition.Stop"


def test_scanex_fehler_erlaubt_trotzdem_stop() -> None:
    geraet, fake = _bereit()
    fake.welt.fehler[("Acquisition", "ScanEx")] = FakeComError("Scan fehlgeschlagen")
    with pytest.raises(GeraeteFehler, match="Scan fehlgeschlagen"):
        geraet.starte_scan(ZIEL)
    fake.zustand = 3
    assert geraet.stoppe() is True


def test_einstellungsstand_inhalte() -> None:
    geraet, fake, _ = _geraet()
    geraet.verbinde()
    stand = geraet.lies_einstellungsstand()
    assert stand.modus == "Fft"
    assert stand.messpunkte_anzahl == 9
    assert stand.generator_aktiv is False
    assert stand.generator_amplitude_v == 0.5
    g = stand.gruppen
    assert g["fft"]["bandbreite_hz"] == 5000.0 and g["fft"]["messzeit_s"] == 0.08
    assert g["mittelung"] == {"typ": 2, "anzahl": 10}
    assert g["trigger"]["phase_aus_referenz"] is True
    assert g["kanaele"]["anzahl"] == 2
    assert g["kanaele"]["k0.name"] == "Vib 1" and g["kanaele"]["k1.name"] == "Vib 2"
    assert g["generator"]["signalform_typ"] == 7
    assert g["generator"]["generatoren_an"] is False
    assert set(g) == {"fft", "mittelung", "allgemein", "trigger", "se", "kanaele", "generator"}
    assert fake.welt.schreibende() == ["AcquisitionInstance.GetApplication:call"] + [
        "ChannelsProperties.Item:call"
    ] * 2 + ["GeneratorsProperties.Item:call"]


def test_einstellungsstand_generator_an_und_lesefehler() -> None:
    geraet, fake, _ = _geraet()
    geraet.verbinde()
    fake.acq._getter["GeneratorsOn"] = lambda: True
    fake.welt.fehler[("FftProperties", "Overlap")] = FakeComError("nicht unterstützt")
    fake.welt.fehler[("Generator", "Waveform")] = FakeComError("kein Waveform")
    fake.acq._getter["Mode"] = lambda: 42
    stand = geraet.lies_einstellungsstand()
    assert stand.generator_aktiv is True
    assert stand.modus == "unbekannt(42)"
    assert stand.gruppen["fft"]["ueberlappung_prozent"] is None
    assert stand.gruppen["fft"]["ueberlappung_prozent__fehler"] == "nicht unterstützt"
    assert stand.gruppen["generator"]["signalform_typ__fehler"] == "kein Waveform"


def test_einstellungsstand_ohne_optionale_gruppen() -> None:
    geraet, fake, _ = _geraet()
    geraet.verbinde()
    for has in (
        "HasGeneralProperties",
        "HasTriggerProperties",
        "HasSignalEnhancementProperties",
        "HasChannelsProperties",
        "HasGeneratorsProperties",
    ):
        fake.props._props[has] = False
    fake.acq._getter["GeneratorsOn"] = lambda: None
    fake.acq._props["Infos"] = None
    stand = geraet.lies_einstellungsstand()
    assert set(stand.gruppen) == {"fft", "mittelung"}
    assert stand.generator_aktiv is None and stand.generator_amplitude_v is None
    assert stand.messpunkte_anzahl is None


def test_einstellungsstand_grenzfaelle_kanaele_und_generator() -> None:
    geraet, fake, _ = _geraet()
    geraet.verbinde()
    welt = fake.welt
    kanal = FakeKnoten("Channel", welt, {"Name": "x"})
    viele = FakeKnoten(
        "ChannelsProperties",
        welt,
        {"Count": MAX_KANAELE + 2},
        {"Item": lambda i: None if i == 2 else kanal},
    )
    fake.props._props["ChannelsProperties"] = viele
    leer = FakeKnoten("GeneratorsProperties", welt, {"Count": 0}, {"Item": lambda i: None})
    fake.props._props["GeneratorsProperties"] = leer
    stand = geraet.lies_einstellungsstand()
    k = stand.gruppen["kanaele"]
    assert k["k1__fehler"] == "Item lieferte nichts"
    assert k["k0.aktiv"] is None and "k0.aktiv__fehler" in k
    assert "k16.name" not in k and k["hinweis"] == f"nur die ersten {MAX_KANAELE} Kanäle gelesen"
    assert stand.gruppen["generator"] == {"anzahl": 0, "generatoren_an": False}
    ohne = FakeKnoten("GeneratorsProperties", welt, {"Count": 1}, {"Item": lambda i: None})
    fake.props._props["GeneratorsProperties"] = ohne
    assert geraet.lies_einstellungsstand().gruppen["generator"]["__fehler"] == (
        "Item(1) lieferte nichts"
    )
    gen = FakeKnoten("Generator", welt, {"Active": True, "Amplitude": 1, "Waveform": None})
    fake.props._props["GeneratorsProperties"] = FakeKnoten(
        "GeneratorsProperties", welt, {"Count": 1}, {"Item": lambda i: gen}
    )
    stand = geraet.lies_einstellungsstand()
    assert stand.generator_aktiv is True and stand.generator_amplitude_v == 1.0
    assert stand.gruppen["generator"]["signalform_typ"] is None


def test_unerwarteter_rueckgabetyp_ist_geraetefehler() -> None:
    geraet, fake, _ = _geraet()
    geraet.verbinde()
    fake.fft._getter["Bandwidth"] = lambda: object()
    with pytest.raises(GeraeteFehler, match="unerwarteter Rückgabetyp"):
        geraet.lies_parameter(["fft.bandbreite_hz"])


def test_haengender_aufruf_wird_gemeldet() -> None:
    geraet, fake, _ = _geraet()
    geraet.verbinde()
    freigabe = threading.Event()
    fake.welt.blockiert[("Acquisition", "State")] = freigabe
    ergebnis: list[GeraeteZustand] = []
    faden = threading.Thread(target=lambda: ergebnis.append(geraet.zustand()))
    faden.start()
    try:
        assert fake.welt.blockade_erreicht.wait(timeout=5)
        dauer = geraet.haengender_aufruf_seit_s()
        assert dauer is not None and dauer >= 0.0
    finally:
        freigabe.set()
        faden.join(timeout=5)
    assert not faden.is_alive()
    assert ergebnis == [GeraeteZustand.GESTOPPT]
    assert geraet.haengender_aufruf_seit_s() is None


def test_erneutes_verbinden_nach_fehler_initialisiert_thread_einmal() -> None:
    geraet, fake, bindung = _geraet(laeuft=False)
    with pytest.raises(GeraeteFehler):
        geraet.verbinde()
    fake.inst._props["IsRunning"] = True
    geraet.verbinde()
    assert bindung.init == 1
    geraet.trenne()
    assert bindung.ende == 1


def test_nur_mittelungstyp_und_tupelwerte_im_stand() -> None:
    geraet, fake, _ = _geraet()
    geraet.verbinde()
    geraet.setze_parameter({"mittelung.typ": "Peakhold"})
    assert "AverageProperties.Count:set" not in fake.welt.schreibende()
    assert geraet.lies_parameter(["mittelung.typ"]) == {"mittelung.typ": "Peakhold"}
    fake.fft._getter["Overlap"] = lambda: (0.0, 50.0)
    stand = geraet.lies_einstellungsstand()
    assert stand.gruppen["fft"]["ueberlappung_prozent"] == "(0.0, 50.0)"


def test_pywin32_bindung_ist_ohne_pywin32_importierbar() -> None:
    from ldv_automation.geraet.com import pywin32_bindung

    for name in ("initialisiere_thread", "beende_thread", "psv_prozesse", "dispatch"):
        assert callable(getattr(pywin32_bindung.Pywin32Bindung, name))


def test_stoppe_nach_scanende_ohne_polling_liest_state_frisch() -> None:
    geraet, fake = _bereit(scan_polls=100)
    geraet.starte_scan(ZIEL)
    fake.zustand = 0  # Scan endet von selbst, kein zustand()-Aufruf dazwischen
    assert geraet.stoppe() is False
    assert "Acquisition.Stop:call" not in fake.welt.ops()
    assert fake.welt.ops()[-1] == "Acquisition.State:get"
    assert geraet.stoppe() is False  # Flag gelöscht: kein weiterer COM-Zugriff
    assert fake.welt.ops()[-1] == "Acquisition.State:get"


def test_stoppe_bei_fremder_aktivitaet_nach_eigenem_scan() -> None:
    geraet, fake = _bereit(scan_polls=100)
    geraet.starte_scan(ZIEL)
    fake.zustand = 1  # Einzelmessung (fremd), eigener Scan ist vorbei
    assert geraet.stoppe() is False
    assert "Acquisition.Stop:call" not in fake.welt.ops()


def test_stoppe_state_lesefehler_ist_geraetefehler() -> None:
    geraet, fake = _bereit(scan_polls=100)
    geraet.starte_scan(ZIEL)
    fake.welt.fehler[("Acquisition", "State")] = FakeComError("RPC-Server nicht verfügbar")
    with pytest.raises(GeraeteFehler, match="RPC") as info:
        geraet.stoppe()
    assert info.value.methode == "Acquisition.State"
    assert "Acquisition.Stop:call" not in fake.welt.ops()


def test_psv_treffer_werden_ausgegeben() -> None:
    geraet, _, _ = _geraet(prozess=("PSV.exe", "psvhelper.exe"))
    info = geraet.verbinde()
    assert geraet.psv_prozesse == ("PSV.exe", "psvhelper.exe")
    assert info.hardware["psv_prozesse"] == "PSV.exe, psvhelper.exe"
    geraet, _, _ = _geraet(prozess=None)
    with pytest.raises(GeraeteFehler, match="nicht ermittelbar"):
        geraet.verbinde()
    assert geraet.psv_prozesse is None


class _ComError(Exception):
    """Wie ``pywintypes.com_error`` (RPC_E_CHANGED_MODE)."""

    hresult = -2147417850
    excepinfo = None
    strerror = "Der Threadingmodus kann nach dem Festlegen nicht geändert werden."


@pytest.mark.parametrize(
    ("methode", "ausnahme", "hresult", "text"),
    [
        ("initialisiere_thread", ImportError("No module named 'pythoncom'"), None, "pythoncom"),
        ("initialisiere_thread", _ComError(), -2147417850, "Threadingmodus"),
        ("psv_prozesse", OSError("tasklist fehlt"), None, "tasklist fehlt"),
    ],
)
def test_rohe_ausnahmen_der_bindung_werden_geraetefehler(
    methode: str, ausnahme: Exception, hresult: int | None, text: str
) -> None:
    geraet, fake, bindung = _geraet()
    bindung.fehler[methode] = ausnahme
    with pytest.raises(GeraeteFehler, match=text) as info:
        geraet.verbinde()
    assert type(info.value) is GeraeteFehler
    assert info.value.methode == methode
    assert info.value.hresult == hresult
    assert info.value.__cause__ is ausnahme
    assert fake.welt.dispatches == []
    assert geraet.haengender_aufruf_seit_s() is None


def test_trenne_uebersetzt_fehler_von_couninitialize() -> None:
    geraet, _, bindung = _geraet()
    geraet.verbinde()
    bindung.fehler["beende_thread"] = _ComError()
    with pytest.raises(GeraeteFehler, match="Threadingmodus") as info:
        geraet.trenne()
    assert info.value.methode == "beende_thread"
    with pytest.raises(GeraeteFehler, match="Nicht mit PSV verbunden"):
        geraet.zustand()
    geraet.trenne()  # idempotent, kein zweites CoUninitialize


def test_waechter_sieht_bindungsaufrufe() -> None:
    geraet, _, bindung = _geraet()
    gesehen: dict[str, float | None] = {}
    bindung.beim_aufruf = lambda name: gesehen.__setitem__(name, geraet.haengender_aufruf_seit_s())
    geraet.verbinde()
    geraet.trenne()
    assert set(gesehen) == {"psv_prozesse", "initialisiere_thread", "beende_thread"}
    assert all(v is not None and v >= 0.0 for v in gesehen.values())
    assert geraet.haengender_aufruf_seit_s() is None


def test_proxy_nutzt_den_injizierten_katalog() -> None:
    katalog = Parameterkatalog(KATALOG)
    katalog.registrieren(
        ParameterSpec(
            schluessel="fft.bandbreite_hz",
            typ="float",
            einheit="Hz",
            com_gruppe="fft",
            minimum=0.0,
            minimum_exklusiv=True,
            maximum=1e6,
        ),
        ersetzen=True,
    )
    geraet, fake, _ = _geraet(katalog=katalog)
    geraet.verbinde()
    geraet.setze_parameter({"fft.bandbreite_hz": 10000.0})
    assert "FftValidator.Bandwidth:set" in fake.welt.schreibende()
