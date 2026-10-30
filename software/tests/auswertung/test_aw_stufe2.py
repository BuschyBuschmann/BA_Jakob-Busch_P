"""Stufe 2 gesamt (FG-03 6), Export, Adapter (Zeitstempel, Elemente), Werkzeug und Befunde an der
Beispieldatei (FG-03 Abschnitt 7, ohne Datei übersprungen)."""

from __future__ import annotations

import dataclasses
import datetime as dt
import json
import math
from pathlib import Path
from typing import Any

import aw_referenz as ref
import beispiel_svd
import numpy as np
import pytest

from ldv_automation.auswertung import Auswertung, werte_aus
from ldv_automation.auswertung.annahmen import AnnahmenStufe2
from ldv_automation.auswertung.export import exportiere, lese_export, sha256_datei
from ldv_automation.auswertung.modenfit import schaetze_daempfung
from ldv_automation.auswertung.stufe2 import (
    FORMAT_STUFE2,
    exportiere_stufe2,
    werte_stufe2_aus,
)
from ldv_automation.auswertung.svd_adapter import (
    aus_svd_messung,
    elemente_aus_svd_messung,
    zeit_s_aus_svd_messung,
)
from ldv_automation.auswertung.vergleich import vergleiche_messungen
from ldv_automation.protokoll.version import BuildInfo

BUILD = BuildInfo(paket_version="0.1.0", git_hash="b" * 40, git_dirty=False, quelle="git")
JETZT = dt.datetime(2026, 10, 30, 12, 0, tzinfo=dt.UTC)
DATEI = Path(__file__).resolve().parents[3] / "Input" / "20261012_ref_Mitte.svd"


@dataclasses.dataclass
class SignalZeit:
    zeit_a: list[dt.datetime]
    zeit_b: list[dt.datetime]


@dataclasses.dataclass
class MessungStufe2:
    signale: dict[str, Any]
    elemente: list[tuple[int, ...]]


def _messung(p: int) -> MessungStufe2:
    t0 = dt.datetime(2026, 10, 12, 9, 0)
    za = [t0 + dt.timedelta(seconds=17.5 * i) for i in range(p)]
    zb = [z + dt.timedelta(seconds=0.64) for z in za]
    return MessungStufe2({"M0": SignalZeit(za, zb), "M1": SignalZeit(za, zb)}, [(0, 1, 3, 2)])


@pytest.fixture
def aw(tmp_path: Path) -> Auswertung:
    pfad = tmp_path / "s.svd"
    pfad.write_bytes(b"s")
    daten = aus_svd_messung(ref.fake_svd_messung(pfad, p=12), sha256="1" * 64)
    a = werte_aus(daten, antriebspunkt=("Ref2", "Ref1", "akzeleranz"), f_schwingform_hz=100.0)
    return a


def test_adapter_zeit_und_elemente() -> None:
    m = _messung(4)
    np.testing.assert_allclose(zeit_s_aus_svd_messung(m), [0, 17.5, 35, 52.5], atol=0)
    zb = zeit_s_aus_svd_messung(m, annahmen2=AnnahmenStufe2(zeitstempel="zeit_b"))
    np.testing.assert_allclose(zb, [0, 17.5, 35, 52.5], atol=1e-9)
    assert elemente_aus_svd_messung(m) == ((0, 1, 3, 2),)
    m.signale["M1"] = SignalZeit(list(reversed(m.signale["M0"].zeit_a)), [])
    with pytest.raises(ValueError, match="stimmen nicht"):
        zeit_s_aus_svd_messung(m)
    with pytest.raises(ValueError, match="ohne Signale"):
        zeit_s_aus_svd_messung(MessungStufe2({}, []))


def test_stufe2_gesamt_und_export(aw: Auswertung, tmp_path: Path) -> None:
    m = _messung(12)
    h1_vorher = aw.paare[("Vib Z", "Ref1")].frf.h1.copy()
    exportiere(aw, tmp_path / "s1", build_info=BUILD, jetzt=lambda: JETZT)
    _, s1_meta = lese_export(tmp_path / "s1")
    e = werte_stufe2_aus(
        aw,
        paare=[("Vib Z", "Ref1"), ("Ref2", "Ref1")],
        spitzen={("Ref2", "Ref1"): [0]},
        zeit_s=zeit_s_aus_svd_messung(m),
        drift_paar=("Ref2", "Ref1"),
        drift_spitzen_hz=[100.0],
        elemente=m.elemente,
    )
    assert set(e.daempfung) == {("Vib Z", "Ref1"), ("Ref2", "Ref1")}
    z = e.daempfung[("Vib Z", "Ref1")].zusammenfassung_bei(100.0)
    assert math.isclose(z.fr_median_hz, 100.0, rel_tol=1e-3)
    assert e.drift[0].pruefbar and e.komponenten is not None
    assert [a.nr for a in e.annahmen_liste][-4:] == ["M12", "M13", "M14", "M15"]
    # Stufe 1 bleibt unverändert (FG-03 1)
    np.testing.assert_array_equal(aw.paare[("Vib Z", "Ref1")].frf.h1, h1_vorher)
    v = vergleiche_messungen(
        aw,
        aw,
        ("Vib Z", "Ref1"),
        baender=[(90.0, 110.0)],
        b1_a=e.daempfung[("Vib Z", "Ref1")],
        b1_b=e.daempfung[("Vib Z", "Ref1")],
    )
    npz, js = exportiere_stufe2(
        e,
        tmp_path / "s2",
        vergleich=v,
        vergleich_auswertung=aw,
        build_info=BUILD,
        jetzt=lambda: JETZT,
    )
    felder, meta = lese_export(tmp_path / "s2", FORMAT_STUFE2)
    assert meta["herkunft"]["software"]["git_hash"] == "b" * 40
    assert meta["herkunft"]["messdatei_sha256"] == "1" * 64
    assert meta["herkunft"]["vergleich_messdatei_sha256"] == "1" * 64
    assert meta["npz_sha256"] == sha256_datei(npz)
    assert [a["nr"] for a in meta["annahmen"]][-4:] == ["M12", "M13", "M14", "M15"]
    assert all(a["status"] == "Annahme" for a in meta["annahmen"][-4:])
    assert meta["schwellen_stufe2"]["rho_max"] == 0.1
    b1 = meta["b1"]["Vib_Z__Ref1"]
    assert b1["ergebnisse"] and len(b1["ergebnisse"][0]["residuum"]) == 2
    assert meta["b5"]["spitzenpaare"] and meta["drift"][0]["pruefbar"]
    assert "b8.v_normal.re" in felder and "b5.band0.frac" in felder
    np.testing.assert_allclose(felder["b5.mac"], 1.0, atol=1e-12)
    with pytest.raises(ValueError, match="kein Export"):
        lese_export(tmp_path / "s2")
    with pytest.raises(FileExistsError):
        exportiere_stufe2(e, tmp_path / "s2", build_info=BUILD)
    # Stufe-1-Export unverändert im Format
    assert s1_meta["format"] == "ldv_automation.auswertung.export" and "b1" not in s1_meta
    assert json.loads(js.read_text(encoding="utf-8"))["format"] == FORMAT_STUFE2
    leer = werte_stufe2_aus(aw)
    _, meta_leer = exportiere_stufe2(leer, tmp_path / "s3", build_info=BUILD)
    assert json.loads(meta_leer.read_text(encoding="utf-8"))["b8"] is None
    with pytest.raises(ValueError, match="zeit_s"):
        werte_stufe2_aus(aw, drift_spitzen_hz=[100.0])
    ohne_herkunft = dataclasses.replace(aw, daten=dataclasses.replace(aw.daten, herkunft=None))
    exportiere_stufe2(
        werte_stufe2_aus(ohne_herkunft),
        tmp_path / "s4",
        vergleich_auswertung=ohne_herkunft,
        build_info=BUILD,
    )
    assert lese_export(tmp_path / "s4", FORMAT_STUFE2)[1]["herkunft"]["messdatei"] is None


def test_werkzeug_stufe2(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    pfad = tmp_path / "w.svd"
    pfad.write_bytes(b"w")

    def leser(p: Path) -> Any:
        m = ref.fake_svd_messung(p, p=12)
        zeit = _messung(12).signale
        for name, s in list(m.signale.items()):
            m.signale[name] = dataclasses.make_dataclass(
                "S", [("zeit_a", list), ("zeit_b", list)], bases=(type(s),)
            )(**s.__dict__, zeit_a=zeit["M0"].zeit_a, zeit_b=zeit["M0"].zeit_b)
        m.elemente = [(0, 1, 3, 2)]  # type: ignore[attr-defined]
        return m

    argv = [str(pfad), "--export", str(tmp_path / "ex"), "--stufe2", "--drift-f", "100"]
    assert beispiel_svd.main(argv, leser=leser) == 0
    aus = capsys.readouterr().out
    assert "davon modell_passt_nicht" in aus
    schalter = [
        str(pfad),
        "--export",
        str(tmp_path / "ex_s"),
        "--stufe2",
        "--drift-f",
        "100",
        "--drift-ausschluss",
        "--drift-mit-nicht-konvergiert",
    ]
    assert beispiel_svd.main(schalter, leser=leser) == 0
    capsys.readouterr()
    meta = json.loads((tmp_path / "ex_s" / "w_stufe2.json").read_text(encoding="utf-8"))
    assert meta["schwellen_stufe2"]["drift_ausschluss"] == []
    assert meta["schwellen_stufe2"]["drift_nicht_konvergiert_einzelmode"] is False
    assert meta["drift"][0]["n_modell_passt_nicht"] == 0
    assert "M1–M15" in aus and "B-1 Vib Z/Ref1" in aus and "Drift (B-5)" in aus
    assert "B-8: 1 Elemente" in aus and "η 150–500 Hz" in aus
    assert (tmp_path / "ex" / "w_stufe2.npz").is_file()
    # Stufe-2-Export existiert schon: Fehler 2 (Stufe 1 wird überschrieben)
    (tmp_path / "ex" / "w.npz").unlink()
    (tmp_path / "ex" / "w.json").unlink()
    assert beispiel_svd.main(argv, leser=leser) == 2

    def veraendernd(p: Path) -> Any:
        m = leser(p)
        if (tmp_path / "ex2" / "w.npz").exists():
            p.write_bytes(b"anders")
        return m

    argv2 = [str(pfad), "--export", str(tmp_path / "ex2"), "--stufe2"]
    assert beispiel_svd.main(argv2, leser=veraendernd) == 3
    # ohne Elemente und ohne Vib Z: keine B-8-Zeilen, η leer
    m0 = ref.fake_svd_messung(pfad)
    a, _ = beispiel_svd.auswerten(pfad, leser=lambda _p: m0)
    e = beispiel_svd.stufe2_auswerten(a, m0)
    assert e.komponenten is None and beispiel_svd.eta_baender(e) == []
    e2 = dataclasses.replace(e, auswertung=dataclasses.replace(a, paare={}))
    assert beispiel_svd.eta_baender(dataclasses.replace(e2, komponenten=object())) == []  # type: ignore[arg-type]


@pytest.mark.skipif(not DATEI.is_file(), reason="Messdatei nicht vorhanden")
def test_befunde_beispieldatei() -> None:
    """FG-03 Abschnitt 7 [D] an der Beispieldatei (Vib Z/Ref1, 20 stärkste Punkte).

    Toleranzen: FG-03 nennt die Werte auf drei bzw. fünf Nachkommastellen; das Prüfskript sucht
    die Spitzenlinie je Punkt in ±2 Linien neu, die Umsetzung nutzt die Stufe-1-Linie (3.3).
    Daher f_r ±0,002 Hz, ζ ±5e-6, rho ±0,003.
    """
    vorher = sha256_datei(DATEI)
    messung = beispiel_svd.lese_svd_werkzeug(DATEI)
    aw = werte_aus(aus_svd_messung(messung, sha256=vorher))
    sp = aw.paare[("Vib Z", "Ref1")].spitzen.spitzen
    wahl = [int(np.argmin([abs(s.f_sp_hz - f) for s in sp])) for f in (401.6, 618.9, 262.6)]
    r = schaetze_daempfung(aw, ("Vib Z", "Ref1"), spitzen=wahl)
    for f, fr, zeta, rho in ((401.6, 401.324, 0.00142, 0.054), (618.9, 619.015, 0.00146, 0.078)):
        z = r.zusammenfassung_bei(f)
        assert abs(z.fr_median_hz - fr) <= 0.002
        assert abs(z.zeta_median - zeta) <= 5e-6
        assert abs(z.rho_median - rho) <= 0.003
    gruppe = [r.zusammenfassung_bei(f) for f in (262.6, 265.0, 270.0)]
    assert len({z.gruppe for z in gruppe}) == 1
    # FG-03 Abschnitt 7 nach K2-3 (Punktauswahl je Spitze, Bandkürzung, rho als Median der
    # verwendeten Punkte); Angaben auf 3 bzw. 5 Stellen → halbe letzte Stelle als Toleranz.
    for z, fr, zeta, rho in zip(
        gruppe,
        (262.720, 266.154, 270.267),
        (0.00214, 0.00116, 0.00190),
        (0.007, 0.012, 0.008),
        strict=True,
    ):
        assert abs(z.fr_median_hz - fr) <= 0.0005
        assert abs(z.zeta_median - zeta) <= 5e-6
        assert abs(z.rho_median - rho) <= 0.0005
        assert z.n_punkte == 20
    assert r.zusammenfassung_bei(618.9).n_punkte == 19
    kb = werte_stufe2_aus(aw, elemente=elemente_aus_svd_messung(messung)).komponenten
    assert kb is not None and len(kb.elemente.elemente) == 112
    w = np.degrees(np.arccos(np.clip(kb.normale_punkt[:, 2], -1, 1)))
    # FG-03 7 nennt 1,3° bis 5,0° (Median 3,2°), gerundet aus 1,25°/5,01°/3,22° → ±0,06°.
    assert abs(np.median(w) - 3.2) <= 0.06 and abs(w.min() - 1.3) <= 0.06
    assert abs(w.max() - 5.0) <= 0.06
    assert sha256_datei(DATEI) == vorher


@pytest.mark.skipif(not DATEI.is_file(), reason="Messdatei nicht vorhanden")
def test_drift_beispieldatei() -> None:
    """FG-03 Abschnitt 7 (K2-1): Drift Ref2/Ref1 mit Ausschluss je gewählter Mode.

    Sollwerte -0,129 ± 0,010 / -0,068 ± 0,010 / -0,482 ± 0,016 Hz/h, N 135/125/135, davon
    ``modell_passt_nicht`` 90/0/0. Toleranz 0,0005 Hz/h (halbe letzte angegebene Stelle,
    5 % des Standardfehlers); N exakt.
    """
    vorher = sha256_datei(DATEI)
    messung = beispiel_svd.lese_svd_werkzeug(DATEI)
    aw = werte_aus(aus_svd_messung(messung, sha256=vorher))
    e = werte_stufe2_aus(
        aw,
        zeit_s=zeit_s_aus_svd_messung(messung),
        drift_paar=("Ref2", "Ref1"),
        drift_spitzen_hz=(418.8, 631.2, 1507.8),
    )
    soll = ((-0.129, 0.010, 135, 90), (-0.068, 0.010, 125, 0), (-0.482, 0.016, 135, 0))
    for d, (b1, sd, n, mpn) in zip(e.drift, soll, strict=True):
        assert abs(d.steigung_hz_h - b1) <= 0.0005
        assert abs(d.sd_steigung_hz_h - sd) <= 0.0005
        assert d.n_punkte == n and d.n_modell_passt_nicht == mpn
        assert d.signifikant
    assert sha256_datei(DATEI) == vorher
