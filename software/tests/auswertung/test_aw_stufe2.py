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
from ldv_automation.auswertung.modenfit import Gruppe, fitband_hz, schaetze_daempfung
from ldv_automation.auswertung.stufe2 import (
    FORMAT_STUFE2,
    _b1_meta,
    _paar_daempfung,
    exportiere_stufe2,
    werte_stufe2_aus,
)
from ldv_automation.auswertung.svd_adapter import (
    aus_svd_messung,
    elemente_aus_svd_messung,
    zeit_s_aus_svd_messung,
)
from ldv_automation.auswertung.vergleich import (
    SpitzenDaempfung,
    _spitzen_daempfung,
    vergleiche_messungen,
)
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


def test_b1_meta_unbekannte_gruppe_gibt_hinweis(aw: Auswertung) -> None:
    m = _messung(12)
    e = werte_stufe2_aus(
        aw,
        paare=[("Vib Z", "Ref1")],
        zeit_s=zeit_s_aus_svd_messung(m),
        elemente=m.elemente,
    )
    b1 = e.daempfung[("Vib Z", "Ref1")]
    f = aw.daten.frequenz_hz
    voll = _b1_meta(b1, f)
    assert not any("nicht in b1.gruppen" in h for h in voll["hinweise"])
    gekappt = dataclasses.replace(b1, gruppen=b1.gruppen[1:])
    meta = _b1_meta(gekappt, f)  # keine Ausnahme
    nummer = b1.gruppen[0].nummer
    assert any(f"Gruppe {nummer} nicht in b1.gruppen" in h for h in meta["hinweise"])
    betroffen = [x for x in meta["ergebnisse"] if x["gruppe"] == nummer]
    assert betroffen
    for x in betroffen:
        assert x["daempfung"]["band_u_hz"] is None and x["daempfung"]["band_o_hz"] is None
    assert len([h for h in meta["hinweise"] if f"Gruppe {nummer} " in h]) == 1


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
    # R-055: ζ mit Fitband in Hz (Frequenz an k_von/k_bis) und Methode
    f_achse = felder["frequenz_hz"]
    gr = {g["nummer"]: g for g in b1["gruppen"]}
    for erg in b1["ergebnisse"]:
        dp = erg["daempfung"]
        g = gr[erg["gruppe"]]
        assert dp["zeta"] == erg["zeta"] and dp["methode"].startswith("Modenfit B-1")
        assert dp["band_u_hz"] == f_achse[g["k_von"]] == g["f_von_hz"]
        assert dp["band_o_hz"] == f_achse[g["k_bis"]] == g["f_bis_hz"]
        assert dp["band_u_hz"] < dp["band_o_hz"]
    for z in b1["zusammenfassung"]:
        assert z["daempfung"]["zeta"] == z["zeta_median"]
        assert z["daempfung"]["band_o_hz"] == gr[z["gruppe"]]["f_bis_hz"]
    assert meta["format_version"] == 2
    assert meta["b5"]["spitzenpaare"] and meta["drift"][0]["pruefbar"]
    for sp in meta["b5"]["spitzenpaare"]:
        for seite in ("daempfung_a", "daempfung_b"):
            d = sp[seite]
            assert set(d) == {"zeta", "band_u_hz", "band_o_hz", "methode"}
            assert d["methode"].startswith("Modenfit B-1") and d["band_u_hz"] < d["band_o_hz"]
        assert sp["delta_zeta"] == sp["daempfung_b"]["zeta"] - sp["daempfung_a"]["zeta"]
    assert all("daempfung" not in d for d in meta["drift"])
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
    assert "B-8: 1 Elemente" in aus and "η 60–200 Hz" in aus
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
    """FG-03 Abschnitt 7 [D] mit korrigierter Achse (K-ACHSE, Δf = 0,625 Hz), Vib Z/Ref1.

    Sollwerte aus FG-03 Abschnitt 7 bzw. dem Prüfskript ``k_achse.py`` (Anhang; die Skriptausgabe
    hat vier Nachkommastellen bei f_r, die Tabelle drei). Toleranzen = halbe letzte angegebene
    Stelle des Sollwerts (Tabelle: 0,0005 Hz bei 3 Stellen; Skript: 0,00005 Hz bei 4 Stellen),
    ζ ±5e-6 und rho ±0,003 bzw. ±0,0005 (dimensionslos, unverändert). Beobachtete Abweichungen
    ≤ 0,0004 Hz bzw. ≤ 0,00004 Hz; die Rechnung ist auf ~1e-9 reproduzierbar.
    Das Prüfskript sucht die Spitzenlinie je Punkt in ±2 Linien neu,
    die Umsetzung nutzt die Stufe-1-Linie (3.3).
    """
    vorher = sha256_datei(DATEI)
    messung = beispiel_svd.lese_svd_werkzeug(DATEI)
    assert messung.fft.delta_f_hz == 0.625 and messung.frequenz_hz[-1] == 1000.0
    aw = werte_aus(aus_svd_messung(messung, sha256=vorher))
    sp = aw.paare[("Vib Z", "Ref1")].spitzen.spitzen
    # FG-03 7: 114 Spitzen, davon 67 aufloesungsbegrenzt; kein M7-Kennzeichen mehr (FG-02 3.9)
    assert len(sp) == 114 and sum("aufloesungsbegrenzt" in s.kennzeichen for s in sp) == 67
    assert not any("gueltigkeit_offen_m7" in s.kennzeichen for s in sp)
    wahl = [int(np.argmin([abs(s.f_sp_hz - f) for s in sp])) for f in (160.64, 247.56, 105.04)]
    r = schaetze_daempfung(aw, ("Vib Z", "Ref1"), spitzen=wahl)
    for f, f_sp, fr, zeta, rho in (
        (160.64, 160.627, 160.530, 0.00142, 0.054),
        (247.56, 247.572, 247.606, 0.00146, 0.078),
    ):
        z = r.zusammenfassung_bei(f)
        assert abs(z.f_sp_hz - f_sp) <= 0.0005
        assert abs(z.fr_median_hz - fr) <= 0.0005
        assert abs(z.zeta_median - zeta) <= 5e-6
        assert abs(z.rho_median - rho) <= 0.003
    gruppe = [r.zusammenfassung_bei(f) for f in (105.04, 106.0, 108.0)]
    assert len({z.gruppe for z in gruppe}) == 1
    # FG-03 Abschnitt 7 nach K2-3 (Punktauswahl je Spitze, Bandkürzung, rho als Median der
    # verwendeten Punkte); f_r aus der Skriptausgabe (4 Stellen: die Tabelle rundet 106,4615 auf
    # 106,462 und liegt damit um 0,0005 neben dem Skriptwert), Toleranz 0,00005 (halbe 4. Stelle).
    for z, fr, zeta, rho in zip(
        gruppe,
        (105.0881, 106.4615, 108.1067),
        (0.00214, 0.00116, 0.00190),
        (0.007, 0.012, 0.008),
        strict=True,
    ):
        assert abs(z.fr_median_hz - fr) <= 0.00005
        assert abs(z.zeta_median - zeta) <= 5e-6
        assert abs(z.rho_median - rho) <= 0.0005
        assert z.n_punkte == 20
    assert r.zusammenfassung_bei(247.56).n_punkte == 19
    # Fitband der Gruppe 101,875 ... 111,875 Hz, 17 Linien (FG-03 7)
    g = next(x for x in r.gruppen if any(abs(v - 105.03) < 0.1 for v in x.f_sp_hz))
    assert messung.frequenz_hz[g.k_von] == 101.875 and messung.frequenz_hz[g.k_bis] == 111.875
    assert g.k_bis - g.k_von + 1 == 17
    # N1-Tabelle, Spalte „nachher“ (Regeln a und b): N, f_r, ζ
    r_alle = schaetze_daempfung(aw, ("Vib Z", "Ref1"))
    for f, n, fr, zeta in (
        (402.564, 14, 402.640, 0.00135),
        (531.74, 10, 531.751, 0.00146),
        (338.02, 3, 338.144, 0.00303),
    ):
        z = r_alle.zusammenfassung_bei(f)
        assert z.n_punkte == n
        assert abs(z.fr_median_hz - fr) <= 0.0005
        assert abs(z.zeta_median - zeta) <= 5e-6
    mehr = [e for e in r_alle.ergebnisse if e.n_moden >= 2]
    assert len({(e.punkt, e.gruppe) for e in mehr}) == 801
    assert sum(any("moden_vertauscht" in k for k in e.kennzeichen) for e in mehr) == 61
    kb = werte_stufe2_aus(aw, elemente=elemente_aus_svd_messung(messung)).komponenten
    assert kb is not None and len(kb.elemente.elemente) == 112
    w = np.degrees(np.arccos(np.clip(kb.normale_punkt[:, 2], -1, 1)))
    # FG-03 7 nennt 1,3° bis 5,0° (Median 3,2°), gerundet aus 1,25°/5,01°/3,22° → ±0,06°.
    assert abs(np.median(w) - 3.2) <= 0.06 and abs(w.min() - 1.3) <= 0.06
    assert abs(w.max() - 5.0) <= 0.06
    assert sha256_datei(DATEI) == vorher


@pytest.mark.skipif(not DATEI.is_file(), reason="Messdatei nicht vorhanden")
def test_eta_baender_beispieldatei() -> None:
    """FG-03 Abschnitt 7 B-8: η in den umbenannten Bändern 60–200 / 200–400 / 400–1000 Hz.

    Gleiche Linien wie früher 150–500 / 500–1000 / 1000–2500 Hz (Nutzerentscheidung 2026-11-02),
    Werte unverändert. FG nennt Median auf drei, 10-%-Quantil auf zwei Stellen → halbe letzte
    Stelle als Toleranz.
    """
    messung = beispiel_svd.lese_svd_werkzeug(DATEI)
    aw = werte_aus(aus_svd_messung(messung, sha256="0" * 64))
    e = werte_stufe2_aus(aw, elemente=elemente_aus_svd_messung(messung))
    baender = beispiel_svd.eta_baender(e)
    soll = ((60.0, 200.0, 0.995, 0.90), (200.0, 400.0, 0.983, 0.71), (400.0, 1000.0, 0.967, 0.65))
    assert len(baender) == 3
    for (f_u, f_o, med, q10), (s_u, s_o, s_med, s_q10) in zip(baender, soll, strict=True):
        assert (f_u, f_o) == (s_u, s_o)
        assert abs(med - s_med) <= 0.0005 and abs(q10 - s_q10) <= 0.005


@pytest.mark.skipif(not DATEI.is_file(), reason="Messdatei nicht vorhanden")
def test_drift_beispieldatei() -> None:
    """FG-03 Abschnitt 7 (K2-1, K-ACHSE): Drift Ref2/Ref1 mit Ausschluss je gewählter Mode.

    Spitzen (167,52; 252,48; 603,12) Hz; Sollwerte -0,0517 ± 0,0041 / -0,0275 ± 0,0044 /
    -0,1930 ± 0,0062 Hz/h, N 135/122/135, davon ``modell_passt_nicht`` 90/0/0. Toleranz
    0,00005 Hz/h = halbe letzte angegebene (4.) Nachkommastelle der FG-Werte; beobachtete
    Abweichung ≤ 0,00004 Hz/h, die Rechnung ist auf ~1e-9 reproduzierbar. N exakt.
    Bei 252,7 Hz werden mit der korrigierten Achse 122 statt der früheren 125 Punkte verwendet
    (FG-03 7): Grenzfälle von ``unsicher`` im Gruppenfit mit weglaufender Partnermode.
    """
    vorher = sha256_datei(DATEI)
    messung = beispiel_svd.lese_svd_werkzeug(DATEI)
    aw = werte_aus(aus_svd_messung(messung, sha256=vorher))
    e = werte_stufe2_aus(
        aw,
        zeit_s=zeit_s_aus_svd_messung(messung),
        drift_paar=("Ref2", "Ref1"),
        drift_spitzen_hz=(167.52, 252.48, 603.12),
    )
    soll = ((-0.0517, 0.0041, 135, 90), (-0.0275, 0.0044, 122, 0), (-0.1930, 0.0062, 135, 0))
    for d, (b1, sd, n, mpn) in zip(e.drift, soll, strict=True):
        assert abs(d.steigung_hz_h - b1) <= 0.00005
        assert abs(d.sd_steigung_hz_h - sd) <= 0.00005
        assert d.n_punkte == n and d.n_modell_passt_nicht == mpn
        assert d.signifikant
    assert sha256_datei(DATEI) == vorher


def test_vergleich_daempfung_baender_beider_messungen(aw: Auswertung, tmp_path: Path) -> None:
    """R-055: daempfung_a/_b je Spitzenpaar; Bänder auf der Achse der jeweiligen Messung.

    B-1 der Messung B weicht bewusst ab (anderes ζ), damit ein Vertauschen von b1_a und b1_b
    an den Werten auffällt.
    """
    e = werte_stufe2_aus(aw, paare=[("Vib Z", "Ref1")])
    b1 = e.daempfung[("Vib Z", "Ref1")]
    b1_b = dataclasses.replace(
        b1,
        zusammenfassung=tuple(
            dataclasses.replace(z, zeta_median=z.zeta_median * 1.5) for z in b1.zusammenfassung
        ),
    )
    verschoben = dataclasses.replace(
        aw, daten=dataclasses.replace(aw.daten, frequenz_hz=aw.daten.frequenz_hz + 0.37)
    )
    v = vergleiche_messungen(aw, verschoben, ("Vib Z", "Ref1"), b1_a=b1, b1_b=b1_b)
    assert len(v.daempfung_a) == len(v.daempfung_b) == len(v.spitzen.paare) > 0
    ohne = vergleiche_messungen(aw, aw, ("Vib Z", "Ref1"))
    assert ohne.daempfung_a == ohne.daempfung_b == tuple(None for _ in ohne.spitzen.paare)
    gr_a = {g.nummer: g for g in b1.gruppen}
    gr_b = {g.nummer: g for g in b1_b.gruppen}
    za = {z.spitze: z for z in b1.zusammenfassung}
    zb = {z.spitze: z for z in b1_b.zusammenfassung}
    for n, p in enumerate(v.spitzen.paare):
        da, db = v.daempfung_a[n], v.daempfung_b[n]
        assert da is not None and db is not None
        ga, gb = gr_a[za[p.index_a].gruppe], gr_b[zb[p.index_b].gruppe]
        assert da.zeta == za[p.index_a].zeta_median and db.zeta == zb[p.index_b].zeta_median
        assert da.zeta != db.zeta  # B-1 der Messung B ist verschieden: Vertauschen fiele auf
        assert da.band_u_hz == aw.daten.frequenz_hz[ga.k_von]
        assert da.band_o_hz == aw.daten.frequenz_hz[ga.k_bis]
        assert db.band_u_hz == verschoben.daten.frequenz_hz[gb.k_von]
        assert db.band_o_hz == verschoben.daten.frequenz_hz[gb.k_bis]
        assert db.band_u_hz is not None and da.band_u_hz is not None
        assert math.isclose(db.band_u_hz - da.band_u_hz, 0.37, abs_tol=1e-9)
    _, js = exportiere_stufe2(
        e, tmp_path / "s5", vergleich=v, vergleich_auswertung=verschoben, build_info=BUILD
    )
    b5 = json.loads(js.read_text(encoding="utf-8"))["b5"]
    assert "delta_zeta = daempfung_b.zeta - daempfung_a.zeta" in b5["daempfung_beschreibung"]
    assert "daempfung_a" in b5["daempfung_beschreibung"]
    assert "daempfung_b" in b5["daempfung_beschreibung"]
    sp = b5["spitzenpaare"][0]
    assert sp["daempfung_b"]["band_u_hz"] == v.daempfung_b[0].band_u_hz  # type: ignore[union-attr]
    assert sp["daempfung_a"]["zeta"] == v.daempfung_a[0].zeta  # type: ignore[union-attr]
    assert sp["daempfung_b"]["zeta"] == v.daempfung_b[0].zeta  # type: ignore[union-attr]
    assert sp["daempfung_a"]["zeta"] != sp["daempfung_b"]["zeta"]


def test_export_paar_daempfung_none_wird_null(aw: Auswertung, tmp_path: Path) -> None:
    """Spitzen ohne B-1-Ergebnis erscheinen im Export als ``null`` (je Seite)."""
    e = werte_stufe2_aus(aw, paare=[("Vib Z", "Ref1")])
    b1 = e.daempfung[("Vib Z", "Ref1")]
    v = vergleiche_messungen(aw, aw, ("Vib Z", "Ref1"), b1_a=b1, b1_b=b1)
    n = len(v.spitzen.paare)
    assert n > 0 and v.daempfung_a[0] is not None
    gemischt = dataclasses.replace(v, daempfung_a=(None, *v.daempfung_a[1:]))
    _, js = exportiere_stufe2(
        e, tmp_path / "s6", vergleich=gemischt, vergleich_auswertung=aw, build_info=BUILD
    )
    sp = json.loads(js.read_text(encoding="utf-8"))["b5"]["spitzenpaare"]
    assert sp[0]["daempfung_a"] is None
    assert all(p["daempfung_b"] is not None for p in sp)
    assert all(p["daempfung_a"] is not None for p in sp[1:])
    assert _paar_daempfung((), 0) is None  # Index außerhalb der Liste


def test_fitband_hz_index_ausserhalb_der_achse() -> None:
    """Fitband: Linienindizes außerhalb der Frequenzachse ergeben ``(None, None)``."""
    f = np.linspace(0.0, 10.0, 11)
    g = Gruppe(nummer=0, spitzen=(0,), f_sp_hz=(5.0,), k_von=2, k_bis=4, kennzeichen=())
    u, o = fitband_hz(f, g)
    assert u is not None and o is not None
    assert math.isclose(u, 2.0, rel_tol=0.0, abs_tol=1e-12)
    assert math.isclose(o, 4.0, rel_tol=0.0, abs_tol=1e-12)
    assert fitband_hz(f, dataclasses.replace(g, k_bis=11)) == (None, None)
    assert fitband_hz(f, dataclasses.replace(g, k_von=-1)) == (None, None)


def test_spitzen_daempfung_ohne_b1_und_nicht_endlich(aw: Auswertung) -> None:
    """Spitze ohne B-1-Zusammenfassung oder mit nicht endlichem ``fr_median_hz`` hat keine ζ."""
    e = werte_stufe2_aus(aw, paare=[("Vib Z", "Ref1")])
    b1 = e.daempfung[("Vib Z", "Ref1")]
    f = aw.daten.frequenz_hz
    z0 = b1.zusammenfassung[0]
    assert _spitzen_daempfung(None, f, [0, 1]) == (None, None)
    fehlt = _spitzen_daempfung(b1, f, [10**6])
    assert fehlt == (None,)
    for wert in (math.nan, math.inf):
        kaputt = dataclasses.replace(
            b1,
            zusammenfassung=(dataclasses.replace(z0, fr_median_hz=wert), *b1.zusammenfassung[1:]),
        )
        assert _spitzen_daempfung(kaputt, f, [z0.spitze]) == (None,)
    ok = _spitzen_daempfung(b1, f, [z0.spitze])[0]
    assert isinstance(ok, SpitzenDaempfung)
    assert ok.zeta == z0.zeta_median
    ohne_gruppe = _spitzen_daempfung(dataclasses.replace(b1, gruppen=()), f, [z0.spitze])[0]
    assert ohne_gruppe == SpitzenDaempfung(zeta=z0.zeta_median, band_u_hz=None, band_o_hz=None)
