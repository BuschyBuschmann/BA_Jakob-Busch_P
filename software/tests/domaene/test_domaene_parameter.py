"""Tests des Parameterkatalogs (U1-3)."""

import pytest

from ldv_automation.domaene.parameter import KATALOG, Parameterkatalog, ParameterSpec


def test_standardkatalog_enthaelt_bestaetigte_parameter() -> None:
    assert {s.schluessel for s in KATALOG} == {
        "fft.bandbreite_hz",
        "fft.linien",
        "mittelung.anzahl",
        "mittelung.typ",
    }
    assert "generator.amplitude_v" not in KATALOG  # Generator bewusst ausgenommen
    assert len(KATALOG) == 4


@pytest.mark.parametrize(
    ("schluessel", "wert", "erwartet"),
    [
        ("mittelung.anzahl", 3, 3),
        ("mittelung.anzahl", 10000, 10000),
        ("fft.bandbreite_hz", 5000, 5000.0),  # int wird zu float
        ("fft.bandbreite_hz", 0.001, 0.001),
        ("fft.linien", 1, 1),
        ("mittelung.typ", "Complex", "Complex"),
    ],
)
def test_gueltige_werte(schluessel: str, wert: object, erwartet: object) -> None:
    ergebnis = KATALOG.spec(schluessel).pruefe(wert)
    assert ergebnis == erwartet
    assert type(ergebnis) is type(erwartet)


@pytest.mark.parametrize(
    ("schluessel", "wert", "teil"),
    [
        ("mittelung.anzahl", 2, "3 … 10000"),
        ("mittelung.anzahl", 10001, "3 … 10000"),
        ("mittelung.anzahl", 3.0, "Ganzzahl"),
        ("mittelung.anzahl", True, "bool"),
        ("mittelung.anzahl", "5", "Ganzzahl"),
        ("fft.bandbreite_hz", 0, "> 0"),
        ("fft.bandbreite_hz", -1.0, "> 0"),
        ("fft.bandbreite_hz", float("nan"), "nicht endlich"),
        ("fft.bandbreite_hz", float("inf"), "nicht endlich"),
        ("fft.bandbreite_hz", "5000", "Zahl"),
        ("fft.linien", 0, "≥ 1"),
        ("mittelung.typ", "Foo", "Peakhold"),
        ("mittelung.typ", 1, "Text"),
    ],
)
def test_ungueltige_werte_nennen_schluessel_und_bereich(
    schluessel: str, wert: object, teil: str
) -> None:
    with pytest.raises(ValueError, match=schluessel.replace(".", r"\.")) as info:
        KATALOG.spec(schluessel).pruefe(wert)
    assert teil in str(info.value)


def test_unbekannter_schluessel() -> None:
    with pytest.raises(ValueError, match="Unbekannter Parameter 'foo'"):
        KATALOG.pruefe({"foo": 1})
    with pytest.raises(ValueError, match=r"fft\.linien"):  # bekannte Schlüssel in der Meldung
        KATALOG.spec("foo")


def test_katalog_pruefe_normalisiert_mapping() -> None:
    assert KATALOG.pruefe({"fft.bandbreite_hz": 100, "fft.linien": 400}) == {
        "fft.bandbreite_hz": 100.0,
        "fft.linien": 400,
    }


def test_katalog_ist_erweiterbar() -> None:
    katalog = Parameterkatalog()
    spec = ParameterSpec(
        schluessel="trigger.pegel_v",
        typ="float",
        einheit="V",
        com_gruppe="trigger",
        minimum=-10.0,
        maximum=10.0,
    )
    katalog.registrieren(spec)
    assert katalog.pruefe({"trigger.pegel_v": 1}) == {"trigger.pegel_v": 1.0}
    with pytest.raises(ValueError, match="bereits"):
        katalog.registrieren(spec)
    katalog.registrieren(spec, ersetzen=True)
    assert [s.schluessel for s in katalog] == ["trigger.pegel_v"]
    with pytest.raises(ValueError, match="-10 … 10 V"):
        katalog.pruefe({"trigger.pegel_v": 11})


@pytest.mark.parametrize(
    ("spec", "text"),
    [
        (ParameterSpec(schluessel="a", typ="float", einheit="", com_gruppe="x"), "beliebig"),
        (
            ParameterSpec(schluessel="a", typ="float", einheit="s", com_gruppe="x", maximum=2.0),
            "≤ 2 s",
        ),
        (ParameterSpec(schluessel="a", typ="str", einheit="", com_gruppe="x"), "beliebiger Text"),
    ],
)
def test_bereich_text_varianten(spec: ParameterSpec, text: str) -> None:
    assert spec.bereich_text() == text


def test_stimmt_ueberein() -> None:
    bandbreite = KATALOG.spec("fft.bandbreite_hz")
    assert bandbreite.stimmt_ueberein(5000.0, 5000.0)
    # Einrasten 5000 -> 6250 Hz ist weit außerhalb von rel_tol=1e-9
    assert not bandbreite.stimmt_ueberein(5000.0, 6250.0)
    # Darstellungsunterschied unterhalb der Toleranz (rel 1e-12)
    assert bandbreite.stimmt_ueberein(5000.0, 5000.0 * (1 + 1e-12))
    assert KATALOG.spec("fft.linien").stimmt_ueberein(400, 400)
    assert not KATALOG.spec("fft.linien").stimmt_ueberein(400, 401)
    assert KATALOG.spec("mittelung.typ").stimmt_ueberein("Complex", "Complex")
    assert not KATALOG.spec("mittelung.typ").stimmt_ueberein("Complex", "Time")


@pytest.mark.parametrize(
    ("schluessel", "soll", "ist"),
    [
        ("fft.linien", 400, True),
        ("fft.linien", 1, True),
        ("fft.linien", 400, 400.0),  # Gleitkomma statt Ganzzahl
        ("fft.linien", 400, "400"),
        ("fft.linien", 400, None),
        ("fft.bandbreite_hz", 5000.0, True),
        ("fft.bandbreite_hz", 1.0, True),
        ("fft.bandbreite_hz", 5000.0, "5000"),
        ("fft.bandbreite_hz", 5000.0, None),
        ("fft.bandbreite_hz", 5000.0, float("nan")),
        ("fft.bandbreite_hz", 5000.0, float("inf")),
        ("fft.bandbreite_hz", 5000.0, 10**400),
        ("mittelung.typ", "Complex", 2),
        ("mittelung.typ", "Complex", None),
        ("mittelung.typ", "Complex", True),
        ("mittelung.typ", "Complex", b"Complex"),
    ],
)
def test_stimmt_ueberein_falscher_typ_ist_keine_uebereinstimmung(
    schluessel: str, soll: object, ist: object
) -> None:
    assert KATALOG.spec(schluessel).stimmt_ueberein(soll, ist) is False


def test_stimmt_ueberein_int_ist_bei_float_spec_zulaessig() -> None:
    assert KATALOG.spec("fft.bandbreite_hz").stimmt_ueberein(5000.0, 5000)


def test_parameterkatalog_pruefe_lehnt_nicht_mapping_ab() -> None:
    with pytest.raises(ValueError, match="Zuordnung"):
        KATALOG.pruefe(None)  # type: ignore[arg-type]
