"""Tests der Datentypen und Fehler der Geräteschnittstelle."""

import dataclasses
from collections.abc import Collection, Mapping

import pytest

from ldv_automation.domaene import ParameterWert
from ldv_automation.geraet.schnittstelle import (
    AbweichungFehler,
    EinstellungsStand,
    Fortschritt,
    GeraeteFehler,
    GeraeteInfo,
    GeraeteZustand,
    GeraetNichtBereitFehler,
    Meldung,
    Messgeraet,
    VerweigertFehler,
    ZeitlimitFehler,
)


def test_fehlerhierarchie_und_attribute() -> None:
    f = GeraeteFehler("kaputt", methode="Load", argumente=("a.set", 1), hresult=-1, excepinfo="x")
    assert str(f) == "kaputt"
    assert (f.methode, f.argumente, f.hresult, f.excepinfo) == ("Load", ("a.set", 1), -1, "x")
    plain = GeraeteFehler("nur text")
    assert (plain.methode, plain.argumente, plain.hresult, plain.excepinfo) == (
        None,
        (),
        None,
        None,
    )
    for klasse in (ZeitlimitFehler, VerweigertFehler, GeraetNichtBereitFehler):
        assert issubclass(klasse, GeraeteFehler)
        assert isinstance(klasse("t"), GeraeteFehler)


def test_abweichungfehler() -> None:
    f = AbweichungFehler("fft.bandbreite_hz", 5000.0, 6250.0)
    assert isinstance(f, GeraeteFehler)
    assert (f.schluessel, f.soll, f.ist) == ("fft.bandbreite_hz", 5000.0, 6250.0)
    assert "fft.bandbreite_hz" in str(f) and "5000.0" in str(f) and "6250.0" in str(f)


def test_datentypen_sind_unveraenderlich_mit_defaults() -> None:
    info = GeraeteInfo(
        psv_version="10.x-SIM",
        erfassungsmodus=True,
        meldungen_unterdrueckt=True,
        zustand=GeraeteZustand.GESTOPPT,
    )
    assert dict(info.hardware) == {}
    with pytest.raises(dataclasses.FrozenInstanceError):
        info.psv_version = "x"  # type: ignore[misc]
    stand = EinstellungsStand(modus="Fft")
    assert stand.messpunkte_anzahl is None and dict(stand.gruppen) == {}
    assert Meldung(stil=0, text="t").antwort is None
    assert Fortschritt(punkte_erledigt=1, punkte_gesamt=9, quelle="ereignisse").punkte_gesamt == 9


class _Attrappe:
    """Minimale Umsetzung aller Protocol-Methoden (prüft Vollständigkeit der Schnittstelle)."""

    def verbinde(self) -> GeraeteInfo:
        return GeraeteInfo(
            psv_version="t",
            erfassungsmodus=True,
            meldungen_unterdrueckt=True,
            zustand=GeraeteZustand.GESTOPPT,
        )

    def trenne(self) -> None: ...
    def zustand(self) -> GeraeteZustand:
        return GeraeteZustand.GESTOPPT

    def setze_messfreigabe(self, freigegeben: bool) -> None: ...
    def lade_einstellungen(self, pfad: str) -> None: ...
    def setze_parameter(self, parameter: Mapping[str, ParameterWert]) -> None: ...
    def lies_parameter(self, schluessel: Collection[str]) -> Mapping[str, ParameterWert]:
        return {}

    def lies_einstellungsstand(self) -> EinstellungsStand:
        return EinstellungsStand(modus="Fft")

    def speichere_einstellungen(self, pfad: str) -> None: ...
    def starte_scan(self, zieldatei: str) -> None: ...
    def stoppe(self) -> bool:
        return False

    def fortschritt(self) -> Fortschritt | None:
        return None

    def hole_meldungen(self) -> tuple[Meldung, ...]:
        return ()

    def haengender_aufruf_seit_s(self) -> float | None:
        return None


def test_protocol_ist_strukturell_erfuellbar() -> None:
    geraet: Messgeraet = _Attrappe()
    assert isinstance(geraet, Messgeraet)
    assert geraet.verbinde().psv_version == "t"
    assert not isinstance(object(), Messgeraet)


def test_vertrag_stoppe_gibt_bool_zurueck_und_nicht_bereit_ist_eigene_klasse() -> None:
    assert _Attrappe().stoppe() is False
    assert not issubclass(GeraetNichtBereitFehler, (VerweigertFehler, ZeitlimitFehler))
    assert "nicht bereit" in (GeraetNichtBereitFehler.__doc__ or "")
    assert "hängender" in (ZeitlimitFehler.__doc__ or "")
    import ldv_automation.geraet.schnittstelle as modul

    assert modul.GeraetNichtBereitFehler is GeraetNichtBereitFehler
    assert modul.Messgeraet.stoppe.__annotations__["return"] in (bool, "bool")


def test_lademaske_ist_teil_von_geraeteinfo() -> None:
    ohne = GeraeteInfo(
        psv_version="t",
        erfassungsmodus=True,
        meldungen_unterdrueckt=True,
        zustand=GeraeteZustand.GESTOPPT,
    )
    assert ohne.lademaske == ""
    mit = dataclasses.replace(ohne, lademaske="Acquisition|APS")
    assert mit.lademaske == "Acquisition|APS"
