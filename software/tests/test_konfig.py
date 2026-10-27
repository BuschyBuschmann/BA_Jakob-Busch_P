"""Konfigurationsdatei des Messrechners (K-U5): Prüfung, Verdrahtung, Protokoll."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

import pytest

import ldv_automation.__main__ as einstieg
from ldv_automation.geraet.com.adapter import PsvComGeraet
from ldv_automation.geraet.com.richtlinie import STANDARD_LADEMASKE
from ldv_automation.gui.anzeige import konfiguration_text
from ldv_automation.konfig import STANDARD, KonfigFehler, lade_konfig, pruefe_konfig
from ldv_automation.sitzung import Betriebsart

BEISPIEL = Path(__file__).resolve().parent.parent / "konfig" / "beispiel_messrechner.json"
KOPF: dict[str, Any] = {"art": "ldv-messrechner-konfig", "schema_version": 1}


def _datei(tmp_path: Path, **werte: Any) -> Path:
    pfad = tmp_path / "messrechner.json"
    pfad.write_text(json.dumps({**KOPF, **werte}), encoding="utf-8")
    return pfad


def test_beispieldatei_entspricht_den_standardwerten() -> None:
    k = lade_konfig(BEISPIEL)
    assert k.pfad == str(BEISPIEL) and k.sha256 == hashlib.sha256(BEISPIEL.read_bytes()).hexdigest()
    werte = {
        f: getattr(k, f)
        for f in (
            "validator_rueckfall_direkt",
            "lademaske",
            "aufruf_grenze_s",
            "aufruf_warnung_s",
            "stop_frist_s",
            "standard_zeitlimit_s",
        )
    }
    assert werte == {f: getattr(STANDARD, f) for f in werte}
    assert STANDARD.lademaske == STANDARD_LADEMASKE
    # Standards entsprechen den bisherigen Vorgaben von Steuerung und Sitzung
    ablauf = STANDARD.ablauf_konfiguration()
    assert (ablauf.aufruf_grenze_s, ablauf.stop_frist_s, ablauf.zeitlimit_s) == (60.0, 10.0, 600.0)


def test_nur_kopf_ergibt_standardwerte_und_werte_werden_uebernommen(tmp_path: Path) -> None:
    assert pruefe_konfig(dict(KOPF)) == STANDARD
    k = lade_konfig(
        _datei(
            tmp_path,
            validator_rueckfall_direkt=True,
            lademaske=["Acquisition", "APS"],
            aufruf_grenze_s=90,
            aufruf_warnung_s=8.5,
            stop_frist_s=20,
            standard_zeitlimit_s=1200,
        )
    )
    assert k.validator_rueckfall_direkt and k.lademaske == 2 | 312
    assert k.ablauf_konfiguration().aufruf_grenze_s == 90.0
    info = k.protokoll_info()
    assert info["werte"] == {
        "validator_rueckfall_direkt": True,
        "lademaske": "Acquisition|APS",
        "aufruf_grenze_s": 90.0,
        "aufruf_warnung_s": 8.5,
        "stop_frist_s": 20.0,
        "standard_zeitlimit_s": 1200.0,
    }


@pytest.mark.parametrize(
    ("werte", "teil"),
    [
        ({"tippfehler_s": 1}, "unbekannte Schlüssel ['tippfehler_s']"),
        ({"art": "x"}, "$.art"),
        ({"schema_version": 2}, "$.schema_version"),
        ({"schema_version": True}, "$.schema_version"),
        ({"validator_rueckfall_direkt": "ja"}, "$.validator_rueckfall_direkt"),
        ({"aufruf_grenze_s": "60"}, "$.aufruf_grenze_s: Zahl erwartet"),
        ({"aufruf_grenze_s": True}, "$.aufruf_grenze_s: Zahl erwartet"),
        ({"aufruf_grenze_s": 0}, "außerhalb 1 … 3600 s"),
        ({"stop_frist_s": 601}, "$.stop_frist_s"),
        ({"standard_zeitlimit_s": 1e9}, "$.standard_zeitlimit_s"),
        ({"aufruf_warnung_s": 70, "aufruf_grenze_s": 60}, "nicht größer als aufruf_grenze_s"),
        ({"lademaske": []}, "$.lademaske: nicht leere Liste"),
        ({"lademaske": "Acquisition"}, "$.lademaske: nicht leere Liste"),
        ({"lademaske": ["Acquisition", "Kamera"]}, "$.lademaske[1]: unbekannte Gruppe"),
        ({"lademaske": ["Camera"]}, "nicht freigegeben"),
        ({"lademaske": ["Acquisition", "Windows"]}, "nicht freigegeben"),
    ],
)
def test_strenge_pruefung(tmp_path: Path, werte: dict[str, Any], teil: str) -> None:
    with pytest.raises(KonfigFehler) as fehler:
        lade_konfig(_datei(tmp_path, **werte))
    assert teil in str(fehler.value) and "messrechner.json" in str(fehler.value)


def test_nan_und_kein_objekt(tmp_path: Path) -> None:
    pfad = tmp_path / "k.json"
    pfad.write_text(
        '{"art": "ldv-messrechner-konfig", "schema_version": 1, "stop_frist_s": NaN}',
        encoding="utf-8",
    )
    with pytest.raises(KonfigFehler, match="stop_frist_s"):
        lade_konfig(pfad)
    pfad.write_text("[]", encoding="utf-8")
    with pytest.raises(KonfigFehler, match="JSON-Objekt erwartet"):
        lade_konfig(pfad)
    pfad.write_text("{kaputt", encoding="utf-8")
    with pytest.raises(KonfigFehler, match="kein gültiges JSON"):
        lade_konfig(pfad)
    with pytest.raises(KonfigFehler, match="nicht lesbar"):
        lade_konfig(tmp_path / "fehlt.json")


def test_main_bricht_bei_ungueltiger_datei_ab(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    pfad = _datei(tmp_path, stop_frist_s=-1)
    assert einstieg.main(["selbsttest", "--konfig", str(pfad)]) == 2
    assert einstieg.main(["gui", "--konfig", str(pfad)]) == 2
    err = capsys.readouterr().err
    assert err.count("Abbruch: Konfigurationsdatei") == 2 and "$.stop_frist_s" in err


def test_selbsttest_mit_konfig_schreibt_sie_in_die_protokolle(tmp_path: Path) -> None:
    pfad = _datei(tmp_path, standard_zeitlimit_s=123, aufruf_grenze_s=30, aufruf_warnung_s=3)
    ordner = tmp_path / "ergebnis"
    ordner.mkdir()
    assert einstieg.main(["selbsttest", "--ordner", str(ordner), "--konfig", str(pfad)]) == 0
    protokolle = sorted(ordner.glob("*/*.protokoll.json"))
    assert len(protokolle) == 4
    k = json.loads(protokolle[0].read_text(encoding="utf-8"))["konfiguration"]
    assert k["pfad"] == str(pfad.resolve())
    assert k["sha256"] == hashlib.sha256(pfad.read_bytes()).hexdigest()
    assert k["werte"]["standard_zeitlimit_s"] == 123.0
    assert json.loads(protokolle[0].read_text(encoding="utf-8"))["zeitlimit_s"] == 123.0
    ereignisse = (protokolle[0].parent / "durchgang.ereignisse.jsonl").read_text("utf-8")
    start = json.loads(ereignisse.splitlines()[0])
    assert start["art"] == "durchgang_start" and start["konfiguration"] == k


def test_selbsttest_ohne_konfig_protokolliert_standardwerte(tmp_path: Path) -> None:
    assert einstieg.selbsttest(tmp_path, ausgabe=lambda _z: None) == 0
    p = next(tmp_path.glob("*/*.protokoll.json"))
    k = json.loads(p.read_text(encoding="utf-8"))["konfiguration"]
    assert k == STANDARD.protokoll_info()


def test_gui_sitzung_und_com_fabrik_uebernehmen_die_werte(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    pfad = _datei(
        tmp_path,
        validator_rueckfall_direkt=True,
        lademaske=["Acquisition"],
        aufruf_warnung_s=7,
        standard_zeitlimit_s=300,
    )
    k = lade_konfig(pfad)
    args = einstieg.baue_parser().parse_args(["gui", "--konfig", str(pfad)])
    s = einstieg.erzeuge_sitzung(args, konfig=k)
    bild = s.zustandsbild()
    assert bild.standard_zeitlimit_s == 300.0
    assert bild.konfiguration == k.protokoll_info()
    assert s._warnung_s == 7.0

    import ldv_automation.geraet.com.pywin32_bindung as pb

    class Attrappe:
        pass

    monkeypatch.setattr(pb, "Pywin32Bindung", Attrappe)
    fabrik = einstieg.erzeuge_fabrik(
        psv=True, start_psv_erlaubt=False, messdaten_wurzel=lambda: None, konfig=k
    )
    geraet = fabrik(Betriebsart.NUR_LESEN)
    assert isinstance(geraet, PsvComGeraet)
    assert geraet.lademaske == 2 and geraet._konf.validator_rueckfall_direkt


def test_konfiguration_text() -> None:
    assert konfiguration_text(None).startswith("keine Angabe")
    text = konfiguration_text(STANDARD.protokoll_info())
    assert text.startswith("Standardwerte (keine Konfigurationsdatei)")
    assert "standard_zeitlimit_s: 600.0" in text
    datei = konfiguration_text({"pfad": "D:/k.json", "sha256": "ab" * 32, "werte": None})
    assert datei == "Datei: D:/k.json (SHA-256 abababababab…)"
