"""Tests der Warteschlangendatei (U1-4, U1-5)."""

import json
from datetime import UTC, datetime, timedelta, timezone
from pathlib import Path
from typing import Any
from uuid import UUID

import pytest

from ldv_automation.domaene import Eintrag, Messung, MessungZustand, Pausenpunkt
from ldv_automation.persistenz.warteschlangendatei import (
    lade_warteschlange,
    speichere_warteschlange,
)

ID1 = UUID("11111111-1111-4111-8111-111111111111")
ID2 = UUID("22222222-2222-4222-8222-222222222222")
ID3 = UUID("33333333-3333-4333-8333-333333333333")
JETZT = datetime(2026, 10, 27, 12, 0, 0, tzinfo=UTC)


def _eintraege(einstellung: Path) -> list[Eintrag]:
    return [
        Messung(
            id=ID1,
            name="Messung 1",
            einstellungsdatei=str(einstellung),
            parameter={
                "fft.bandbreite_hz": 5000.0,
                "mittelung.anzahl": 10,
                "mittelung.typ": "Complex",
            },
            zeitlimit_s=120.5,
            notiz="Üben: ä ö ü",
        ),
        Pausenpunkt(id=ID2, text="Prüfling umbauen"),
        Messung(id=ID3, name="Messung 2", einstellungsdatei=str(einstellung)),
    ]


@pytest.fixture
def datei(tmp_path: Path) -> Path:
    return tmp_path / "test.warteschlange.json"


@pytest.fixture
def einstellung(tmp_path: Path) -> Path:
    pfad = tmp_path / "a.set"
    pfad.write_text("x", encoding="utf-8")
    return pfad


def _speichere(eintraege: list[Eintrag], pfad: Path, **kw: Any) -> None:
    speichere_warteschlange(
        eintraege, pfad, paket_version="0.1.0", git_hash="abc123", jetzt=lambda: JETZT, **kw
    )


def _schreibe(pfad: Path, daten: dict[str, Any]) -> Path:
    pfad.write_text(json.dumps(daten), encoding="utf-8")
    return pfad


def _gueltig(einstellung: Path) -> dict[str, Any]:
    daten = json.loads(
        json.dumps(
            {
                "schema_version": 1,
                "art": "ldv-warteschlange",
                "erstellt_utc": JETZT.isoformat(),
                "paket_version": "0.1.0",
                "git_hash": None,
                "eintraege": [
                    {
                        "art": "messung",
                        "id": str(ID1),
                        "name": "M",
                        "einstellungsdatei": str(einstellung),
                        "parameter": {"fft.linien": 400},
                        "zeitlimit_s": None,
                        "notiz": "",
                    },
                    {"art": "pausenpunkt", "id": str(ID2), "text": "P"},
                ],
            }
        )
    )
    assert isinstance(daten, dict)
    return daten


# --- U1-4 ----------------------------------------------------------------------------------


def test_u1_4_roundtrip_gleiche_eintraege(datei: Path, einstellung: Path) -> None:
    original = _eintraege(einstellung)
    _speichere(original, datei)
    ergebnis = lade_warteschlange(datei)
    assert ergebnis.eintraege == tuple(original)  # IDs, Reihenfolge, Parameter, Pausenpunkte
    assert [e.id for e in ergebnis.eintraege] == [ID1, ID2, ID3]
    assert ergebnis.warnungen == ()
    assert ergebnis.paket_version == "0.1.0"
    assert ergebnis.git_hash == "abc123"
    assert ergebnis.erstellt_utc == "2026-10-27T12:00:00+00:00"
    m = ergebnis.eintraege[0]
    assert isinstance(m, Messung)
    assert isinstance(m.parameter["fft.bandbreite_hz"], float)


def test_u1_4_geladene_eintraege_sind_alle_wartend(datei: Path, einstellung: Path) -> None:
    laeuft = Messung(name="L", einstellungsdatei=str(einstellung)).mit_zustand(
        MessungZustand.LAEUFT
    )
    fehler = laeuft.mit_zustand(MessungZustand.FEHLER).mit_zustand(MessungZustand.WARTEND)
    assert fehler.versuch == 2
    _speichere([Messung(name="W", einstellungsdatei=str(einstellung))], datei)
    ergebnis = lade_warteschlange(datei)
    for e in ergebnis.eintraege:
        assert e.bearbeitbar
        if isinstance(e, Messung):
            assert e.versuch == 1


def test_gespeichert_wird_nur_die_definition(datei: Path, einstellung: Path) -> None:
    laeuft = Messung(id=ID1, name="L", einstellungsdatei=str(einstellung)).mit_zustand(
        MessungZustand.LAEUFT
    )
    _speichere([laeuft], datei)
    rohdaten = json.loads(datei.read_text(encoding="utf-8"))
    assert set(rohdaten["eintraege"][0]) == {
        "art",
        "id",
        "name",
        "einstellungsdatei",
        "parameter",
        "zeitlimit_s",
        "notiz",
    }
    assert lade_warteschlange(datei).eintraege[0].bearbeitbar


def test_kopfdaten_und_format(datei: Path, einstellung: Path) -> None:
    _speichere(_eintraege(einstellung), datei)
    roh = json.loads(datei.read_text(encoding="utf-8"))
    assert roh["schema_version"] == 1
    assert roh["art"] == "ldv-warteschlange"
    assert roh["git_hash"] == "abc123"
    assert "Üben: ä ö ü" in datei.read_text(encoding="utf-8")  # UTF-8, nicht escaped


def test_zeitstempel_wird_nach_utc_umgerechnet(datei: Path) -> None:
    lokal = datetime(2026, 10, 27, 14, 0, tzinfo=timezone(timedelta(hours=2)))
    speichere_warteschlange([], datei, paket_version="0.1.0", git_hash=None, jetzt=lambda: lokal)
    assert (
        json.loads(datei.read_text(encoding="utf-8"))["erstellt_utc"] == "2026-10-27T12:00:00+00:00"
    )
    assert lade_warteschlange(datei).git_hash is None


def test_standarduhr_liefert_zeitzonenbehafteten_zeitstempel(datei: Path) -> None:
    speichere_warteschlange([], datei, paket_version="0.1.0", git_hash=None)
    stempel = json.loads(datei.read_text(encoding="utf-8"))["erstellt_utc"]
    assert datetime.fromisoformat(stempel).tzinfo is not None


def test_zeitzonenlose_uhr_wird_abgelehnt(datei: Path) -> None:
    with pytest.raises(ValueError, match="zeitzonenbehaftet"):
        speichere_warteschlange(
            [], datei, paket_version="0.1.0", git_hash=None, jetzt=lambda: datetime(2026, 1, 1)
        )
    assert not datei.exists()


def test_dateiendung_wird_erzwungen(tmp_path: Path) -> None:
    with pytest.raises(ValueError, match=r"\.warteschlange\.json"):
        _speichere([], tmp_path / "x.json")


def test_vorhandene_datei_wird_nicht_ueberschrieben(datei: Path, einstellung: Path) -> None:
    datei.write_text("ALT", encoding="utf-8")
    with pytest.raises(FileExistsError):
        _speichere(_eintraege(einstellung), datei)
    assert datei.read_text(encoding="utf-8") == "ALT"


def test_ueberschreiben_nur_auf_ausdruecklichen_wunsch(datei: Path, einstellung: Path) -> None:
    datei.write_text("ALT", encoding="utf-8")
    _speichere(_eintraege(einstellung), datei, ueberschreiben=True)
    assert len(lade_warteschlange(datei).eintraege) == 3
    assert not list(datei.parent.glob("*.tmp"))


def test_ueberschreiben_raeumt_temporaere_datei_bei_fehler_auf(
    datei: Path, einstellung: Path
) -> None:
    class Kaputt:  # nicht serialisierbar -> Fehler vor dem Schreiben, nichts bleibt liegen
        pass

    eintrag = Messung(name="M", einstellungsdatei=str(einstellung))
    object.__setattr__(eintrag, "notiz", Kaputt())
    with pytest.raises(TypeError):
        _speichere([eintrag], datei, ueberschreiben=True)
    assert not datei.exists()
    assert not list(datei.parent.glob("*.tmp"))


def test_fehlende_einstellungsdatei_ist_nur_warnung(datei: Path, tmp_path: Path) -> None:
    fehlend = tmp_path / "gibt_es_nicht.set"
    _speichere([Messung(id=ID1, name="M", einstellungsdatei=str(fehlend))], datei)
    ergebnis = lade_warteschlange(datei)
    assert len(ergebnis.eintraege) == 1
    assert len(ergebnis.warnungen) == 1
    assert "$.eintraege[0].einstellungsdatei" in ergebnis.warnungen[0]
    assert "gibt_es_nicht.set" in ergebnis.warnungen[0]


def test_fehlende_datei(tmp_path: Path) -> None:
    with pytest.raises(FileNotFoundError):
        lade_warteschlange(tmp_path / "nein.warteschlange.json")


# --- U1-5 ----------------------------------------------------------------------------------


def test_gueltige_handgeschriebene_datei(datei: Path, einstellung: Path) -> None:
    ergebnis = lade_warteschlange(_schreibe(datei, _gueltig(einstellung)))
    assert [e.id for e in ergebnis.eintraege] == [ID1, ID2]
    m = ergebnis.eintraege[0]
    assert isinstance(m, Messung) and m.zeitlimit_s is None


def _mutiere(einstellung: Path, aenderung: Any) -> dict[str, Any]:
    daten = _gueltig(einstellung)
    aenderung(daten)
    return daten


FEHLERFAELLE: list[tuple[str, Any, str]] = [
    ("version", lambda d: d.update(schema_version=2), r"\$.schema_version"),
    ("version_bool", lambda d: d.update(schema_version=True), r"\$.schema_version"),
    ("art", lambda d: d.update(art="x"), r"\$.art"),
    ("kopf_unbekannt", lambda d: d.update(extra=1), r"\$.extra"),
    ("kopf_fehlt", lambda d: d.pop("paket_version"), r"\$.paket_version"),
    ("zeitstempel", lambda d: d.update(erstellt_utc="gestern"), r"\$.erstellt_utc"),
    ("zeitstempel_typ", lambda d: d.update(erstellt_utc=5), r"\$.erstellt_utc"),
    ("git_typ", lambda d: d.update(git_hash=5), r"\$.git_hash"),
    ("eintraege_typ", lambda d: d.update(eintraege={}), r"\$.eintraege"),
    ("eintrag_typ", lambda d: d["eintraege"].append(5), r"\$.eintraege\[2\]"),
    ("eintrag_art", lambda d: d["eintraege"][0].update(art="x"), r"\$.eintraege\[0\].art"),
    (
        "messung_unbekannt",
        lambda d: d["eintraege"][0].update(foo=1),
        r"\$.eintraege\[0\].foo",
    ),
    (
        "messung_fehlt",
        lambda d: d["eintraege"][0].pop("notiz"),
        r"\$.eintraege\[0\].notiz",
    ),
    (
        "pausenpunkt_unbekannt",
        lambda d: d["eintraege"][1].update(name="x"),
        r"\$.eintraege\[1\].name",
    ),
    (
        "parameter_unbekannt",
        lambda d: d["eintraege"][0]["parameter"].update(foo=1),
        r"\$.eintraege\[0\].parameter.foo",
    ),
    (
        "parameter_bereich",
        lambda d: d["eintraege"][0]["parameter"].update({"mittelung.anzahl": 2}),
        r"\$.eintraege\[0\].*mittelung\.anzahl.*3 … 10000",
    ),
    (
        "parameter_typ",
        lambda d: d["eintraege"][0].update(parameter=[]),
        r"\$.eintraege\[0\].parameter",
    ),
    ("zeitlimit_typ", lambda d: d["eintraege"][0].update(zeitlimit_s="x"), r"zeitlimit_s"),
    ("zeitlimit_null", lambda d: d["eintraege"][0].update(zeitlimit_s=0), r"\$.eintraege\[0\]"),
    ("name_typ", lambda d: d["eintraege"][0].update(name=1), r"\$.eintraege\[0\].name"),
    ("id_typ", lambda d: d["eintraege"][0].update(id=1), r"\$.eintraege\[0\].id"),
    ("id_ungueltig", lambda d: d["eintraege"][0].update(id="x"), r"\$.eintraege\[0\].id"),
    ("pausenpunkt_id", lambda d: d["eintraege"][1].update(id="x"), r"\$.eintraege\[1\].id"),
    (
        "parameter_riesig",
        lambda d: d["eintraege"][0]["parameter"].update({"fft.bandbreite_hz": 10**400}),
        r"\$.eintraege\[0\].*fft\.bandbreite_hz",
    ),
    (
        "parameter_riesig_int",
        lambda d: d["eintraege"][0]["parameter"].update({"mittelung.anzahl": 10**400}),
        r"\$.eintraege\[0\].*mittelung\.anzahl",
    ),
    (
        "zeitlimit_riesig",
        lambda d: d["eintraege"][0].update(zeitlimit_s=10**400),
        r"\$.eintraege\[0\]",
    ),
    (
        "parameter_none",
        lambda d: d["eintraege"][0]["parameter"].update({"fft.linien": None}),
        r"\$.eintraege\[0\].*fft\.linien",
    ),
    ("id_doppelt", lambda d: d["eintraege"][1].update(id=str(ID1)), r"\$.eintraege\[1\].id"),
    ("pausenpunkt_leer", lambda d: d["eintraege"][1].update(text=""), r"\$.eintraege\[1\]"),
]


@pytest.mark.parametrize(
    ("aenderung", "muster"),
    [(a, m) for _, a, m in FEHLERFAELLE],
    ids=[n for n, _, _ in FEHLERFAELLE],
)
def test_u1_5_ungueltige_dateien_werfen_valueerror_mit_json_pfad(
    datei: Path, einstellung: Path, aenderung: Any, muster: str
) -> None:
    pfad = _schreibe(datei, _mutiere(einstellung, aenderung))
    with pytest.raises(ValueError, match=muster) as info:
        lade_warteschlange(pfad)
    assert str(info.value).startswith("test.warteschlange.json: ")


def test_u1_5_wurzel_ist_kein_objekt(datei: Path) -> None:
    datei.write_text("[]", encoding="utf-8")
    with pytest.raises(ValueError, match=r"\$: Objekt erwartet"):
        lade_warteschlange(datei)


def test_ungueltiges_json_und_doppelte_schluessel(datei: Path) -> None:
    datei.write_text("{nicht json", encoding="utf-8")
    with pytest.raises(ValueError, match=r"test\.warteschlange\.json"):
        lade_warteschlange(datei)
    datei.write_text('{"a": 1, "a": 2}', encoding="utf-8")
    with pytest.raises(ValueError, match="doppelter Schlüssel 'a'"):
        lade_warteschlange(datei)
