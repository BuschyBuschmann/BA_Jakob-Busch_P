"""Tests der Einträge und ihrer Zustandsübergänge."""

import dataclasses
from uuid import uuid4

import pytest

from ldv_automation.domaene import Messung, MessungZustand, Pausenpunkt, PausenpunktZustand


def _messung(**kw: object) -> Messung:
    return Messung(name="M1", einstellungsdatei="a.set", **kw)  # type: ignore[arg-type]


def test_standardwerte() -> None:
    m = _messung()
    assert m.zustand is MessungZustand.WARTEND
    assert m.versuch == 1
    assert m.zeitlimit_s is None
    assert m.bearbeitbar
    assert dict(m.parameter) == {}
    assert _messung().id != m.id


def test_parameter_werden_beim_anlegen_geprueft_und_normalisiert() -> None:
    m = _messung(parameter={"fft.bandbreite_hz": 5000, "mittelung.anzahl": 10})
    assert m.parameter["fft.bandbreite_hz"] == 5000.0
    assert isinstance(m.parameter["fft.bandbreite_hz"], float)
    with pytest.raises(ValueError, match=r"mittelung\.anzahl.*3 … 10000"):
        _messung(parameter={"mittelung.anzahl": 2})
    with pytest.raises(ValueError, match="Unbekannter Parameter"):
        _messung(parameter={"foo": 1})


def test_parameter_sind_schreibgeschuetzt_und_vom_aufrufer_entkoppelt() -> None:
    quelle = {"fft.linien": 400}
    m = _messung(parameter=quelle)
    quelle["fft.linien"] = 800
    assert m.parameter["fft.linien"] == 400
    with pytest.raises(TypeError):
        m.parameter["fft.linien"] = 1  # type: ignore[index]
    with pytest.raises(dataclasses.FrozenInstanceError):
        m.name = "x"  # type: ignore[misc]


@pytest.mark.parametrize("limit", [0.0, -1.0, float("nan"), float("inf"), True])
def test_ungueltiges_zeitlimit(limit: float) -> None:
    with pytest.raises(ValueError, match="zeitlimit_s"):
        _messung(zeitlimit_s=limit)


def test_ungueltige_stammdaten() -> None:
    with pytest.raises(ValueError, match="Name"):
        Messung(name="  ", einstellungsdatei="a.set")
    with pytest.raises(ValueError, match="Einstellungsdatei"):
        Messung(name="x", einstellungsdatei="")
    with pytest.raises(ValueError, match="versuch"):
        _messung(versuch=0)
    with pytest.raises(ValueError, match="Text"):
        Pausenpunkt(text="")


def test_gleichheit_ueber_alle_felder() -> None:
    eid = uuid4()
    a = _messung(id=eid, parameter={"fft.linien": 400})
    b = _messung(id=eid, parameter={"fft.linien": 400})
    assert a == b


def test_messung_zustandsuebergaenge() -> None:
    m = _messung()
    laeuft = m.mit_zustand(MessungZustand.LAEUFT)
    assert not laeuft.bearbeitbar
    assert m.zustand is MessungZustand.WARTEND  # Original unverändert
    fehler = laeuft.mit_zustand(MessungZustand.FEHLER)
    nochmal = fehler.mit_zustand(MessungZustand.WARTEND)
    assert nochmal.versuch == 2
    assert nochmal.id == m.id
    assert laeuft.mit_zustand(MessungZustand.FERTIG).zustand is MessungZustand.FERTIG
    assert laeuft.mit_zustand(MessungZustand.ABGEBROCHEN).versuch == 1


@pytest.mark.parametrize(
    ("start", "ziel"),
    [
        (MessungZustand.WARTEND, MessungZustand.FERTIG),
        (MessungZustand.WARTEND, MessungZustand.WARTEND),
        (MessungZustand.LAEUFT, MessungZustand.WARTEND),
        (MessungZustand.FERTIG, MessungZustand.WARTEND),
        (MessungZustand.ABGEBROCHEN, MessungZustand.LAEUFT),
        (MessungZustand.FEHLER, MessungZustand.FERTIG),
    ],
)
def test_messung_unerlaubte_uebergaenge(start: MessungZustand, ziel: MessungZustand) -> None:
    m = dataclasses.replace(_messung(), zustand=start)
    with pytest.raises(ValueError, match="nicht erlaubt"):
        m.mit_zustand(ziel)


def test_messung_falsche_zustandsart() -> None:
    with pytest.raises(ValueError, match="nicht erlaubt"):
        _messung().mit_zustand(PausenpunktZustand.ERREICHT)  # type: ignore[arg-type]
    with pytest.raises(ValueError, match="nicht erlaubt"):
        _messung().mit_zustand("laeuft")  # type: ignore[arg-type]


def test_pausenpunkt_zustaende() -> None:
    p = Pausenpunkt(text="Prüfling umbauen")
    erreicht = p.mit_zustand(PausenpunktZustand.ERREICHT)
    assert not erreicht.bearbeitbar
    assert erreicht.mit_zustand(PausenpunktZustand.WARTEND).bearbeitbar  # Rücksetzen bei Abbruch
    erledigt = erreicht.mit_zustand(PausenpunktZustand.ERLEDIGT)
    for ziel in PausenpunktZustand:
        with pytest.raises(ValueError, match="nicht erlaubt"):
            erledigt.mit_zustand(ziel)
    with pytest.raises(ValueError, match="nicht erlaubt"):
        p.mit_zustand(PausenpunktZustand.ERLEDIGT)
    with pytest.raises(ValueError, match="nicht erlaubt"):
        p.mit_zustand(MessungZustand.LAEUFT)  # type: ignore[arg-type]
    with pytest.raises(ValueError, match="nicht erlaubt"):
        p.mit_zustand(None)  # type: ignore[arg-type]


# --- Review-Korrekturen (MINOR-1) ----------------------------------------------------------------


@pytest.mark.parametrize(
    "kw",
    [
        {"name": None},
        {"einstellungsdatei": 5},
        {"notiz": None},
        {"id": "abc"},
        {"zustand": "wartend"},
        {"versuch": True},
        {"versuch": 1.0},
        {"versuch": "1"},
        {"versuch": 0},
        {"parameter": None},
        {"parameter": 5},
        {"zeitlimit_s": "x"},
        {"zeitlimit_s": 10**400},
        {"zeitlimit_s": float("nan")},
        {"parameter": {"fft.bandbreite_hz": 10**400}},
        {"parameter": {"mittelung.anzahl": 10**400}},
        {"parameter": {"mittelung.anzahl": -(10**400)}},
        {"parameter": {None: 1}},
    ],
)
def test_ungueltige_typen_ergeben_valueerror(kw: dict[str, object]) -> None:
    args: dict[str, object] = {"name": "M", "einstellungsdatei": "a.set"}
    args.update(kw)
    with pytest.raises(ValueError, match=r"\S"):
        Messung(**args)  # type: ignore[arg-type]


def test_riesige_ganzzahl_meldung_ist_begrenzt() -> None:
    with pytest.raises(ValueError, match=r"mittelung\.anzahl") as info:
        _messung(parameter={"mittelung.anzahl": 10**400})
    assert len(str(info.value)) < 200


def test_zeitlimit_ganzzahl_wird_float() -> None:
    assert isinstance(_messung(zeitlimit_s=30).zeitlimit_s, float)


def test_pausenpunkt_ungueltige_typen() -> None:
    for kw in ({"text": None}, {"text": 3}, {"id": 1}, {"zustand": "x"}):
        with pytest.raises(ValueError, match=r"\S"):
            Pausenpunkt(**{"text": "t", **kw})  # type: ignore[arg-type]
