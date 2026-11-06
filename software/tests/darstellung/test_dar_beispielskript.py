"""Thesis-Beispielskript ``tools/auswertung/darstellung_beispiel.py`` (UI-18, P-AUSW T2)."""

from __future__ import annotations

import ast
import importlib.util
import json
import re
import sys
from dataclasses import replace
from pathlib import Path
from typing import Any

import dar_daten as dd
import darstellung_beispiel as skript
import numpy as np
import pytest
from matplotlib.figure import Figure

from ldv_automation.auswertung.annahmen import Annahmen
from ldv_automation.auswertung.export import sha256_datei
from ldv_automation.auswertung.laden import lade_svd
from ldv_automation.darstellung.auswahl import (
    DarstellungsFehler,
    PaarCache,
    schwingform_daten,
    spektrum_daten,
)
from ldv_automation.darstellung.bild import neue_figure
from ldv_automation.darstellung.schwingform import (
    HINWEIS_PHASE_SPRUNG,
    SchwingformOptionen,
    zeichne_schwingform,
)
from ldv_automation.darstellung.spektrum import SpektrumOptionen, zeichne_spektrum
from ldv_automation.darstellung.stil import THESIS_STIL
from ldv_automation.protokoll.version import BuildInfo

HASH = "0123456789abcdef0123456789abcdef01234567"
SAUBER = BuildInfo(paket_version="0.2.0", git_hash=HASH, git_dirty=False, quelle="git")
BILDER = ("spektrum", "frf", "spitzen", "schwingform", "schwingform_phase")


@pytest.fixture(autouse=True)
def _sauberer_git_stand(monkeypatch: pytest.MonkeyPatch) -> None:
    """Der Arbeitsbaum des Repos ist beim Testen oft nicht sauber: ein fester Stand genügt."""
    monkeypatch.setattr(skript, "ermittle_build_info", lambda: SAUBER)


def _messdatei(tmp_path: Path, name: str = "mess.svd") -> Path:
    quelle = tmp_path / name
    quelle.write_bytes(b"kein echter Container")
    return quelle


def _lauf(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
    *args: str,
    daten: Any = None,
    ausgabe: Path | None = None,
    name: str = "mess.svd",
) -> tuple[int, Path]:
    """Ruft ``main`` mit synthetischen Messdaten statt der Datei auf (kleine Bilder, dpi fest)."""

    class _Geladen:
        messdaten = daten if daten is not None else dd.synthetische_messdaten()

    monkeypatch.setattr(skript, "lade_svd", lambda pfad: _Geladen())
    ziel = ausgabe if ausgabe is not None else tmp_path / "abb"
    quelle = tmp_path / name
    if not quelle.exists():
        quelle.write_bytes(b"kein echter Container")
    return skript.main([str(quelle), "--ausgabe", str(ziel), *args]), ziel


def test_figuren_mit_referenz_haben_dieselben_linien_und_achsentexte_wie_die_oberflaeche() -> None:
    md = dd.synthetische_messdaten()
    figuren = skript.erzeuge_figuren(md)
    assert set(figuren) == {"spektrum", "frf", "spitzen", "schwingform", "schwingform_phase"}
    # „Oberfläche“: dieselbe Zeichenfunktion und dieselben Daten
    cache = PaarCache(md)
    ui = zeichne_spektrum(
        neue_figure(THESIS_STIL),
        spektrum_daten(md, cache, punkt=None),
        SpektrumOptionen(),
        THESIS_STIL,
    )
    s = figuren["spektrum"]
    assert len(s.linien) == len(ui.linien) == 4
    assert (s.achsen[0].get_xlabel(), s.achsen[0].get_ylabel()) == (
        ui.achsen[0].get_xlabel(),
        ui.achsen[0].get_ylabel(),
    )
    for z in figuren.values():
        assert not z.figure.texts  # kein Arbeitsstempel
        assert not any("Arbeitsansicht" in t for t in z.alle_texte())
    for name, z in figuren.items():
        breite, hoehe = z.figure.get_size_inches()
        if name.startswith("schwingform"):  # Hochformat 11,5 cm, Höhe aus dem Datenaspekt
            assert breite == pytest.approx(11.5 / 2.54) and hoehe >= 0.5 * breite
        else:
            assert breite == pytest.approx(4.9)  # Satzspiegel A5


def test_figuren_ohne_referenz_nur_leistung_und_keine_frf() -> None:
    md = dd.synthetische_messdaten(referenz=False)
    figuren = skript.erzeuge_figuren(md)
    assert set(figuren) == {"spektrum", "spitzen", "schwingform"}
    assert figuren["spektrum"].hilfsobjekte["legende"].get_title().get_text().startswith("Leistung")
    assert "Keine Spitzensuche: Referenzkanal fehlt." in figuren["spitzen"].alle_texte()


def test_figuren_punkt_und_frequenz_waehlbar() -> None:
    md = dd.synthetische_messdaten()
    figuren = skript.erzeuge_figuren(md, punkt_label=103, frequenz_hz=20.0)
    assert len(figuren["spektrum"].linien) == 4
    assert "kohaerenz" in figuren["frf"].linien
    with pytest.raises(skript.AbbruchFehler, match=r"Label 999.*Vorhandene Labels: 100, 101"):
        skript.erzeuge_figuren(md, punkt_label=999)


def test_schreibe_abbildungen_mit_herkunft_und_ueberschreibschutz(tmp_path: Path) -> None:
    md = dd.synthetische_messdaten()
    quelle = _messdatei(tmp_path)
    figuren = skript.erzeuge_figuren(md)
    ziel = tmp_path / "abb"
    pfade = skript.schreibe_abbildungen(figuren, ziel, messdatei=quelle, dpi=40)
    assert [p.name for p in pfade] == [f"mess_{n}.png" for n in figuren]
    herkunft = json.loads((ziel / "mess_spektrum.json").read_text(encoding="utf-8"))
    assert herkunft["skript"].endswith("darstellung_beispiel.py")
    assert herkunft["messdatei"] == "mess.svd"
    assert herkunft["messdatei_sha256"] == sha256_datei(quelle)
    assert (
        herkunft["linien"] == 4 and ["Frequenz [Hz]", "Amplitude [m/s]"] in herkunft["achsentitel"]
    )
    assert "software_git_hash" in herkunft
    with pytest.raises(FileExistsError, match="nicht überschrieben"):
        skript.schreibe_abbildungen(figuren, ziel, messdatei=quelle, dpi=40)
    # eine spätere Datei existiert schon: nichts wird geschrieben (keine Teilausgabe)
    teil = tmp_path / "teil"
    teil.mkdir()
    (teil / "mess_schwingform.png").write_bytes(b"alt")
    with pytest.raises(FileExistsError, match=r"mess_schwingform\.png"):
        skript.schreibe_abbildungen(figuren, teil, messdatei=quelle, dpi=40)
    assert [p.name for p in teil.iterdir()] == ["mess_schwingform.png"]
    assert (teil / "mess_schwingform.png").read_bytes() == b"alt"
    pdf = skript.schreibe_abbildungen(figuren, tmp_path / "pdf", messdatei=quelle, format_="pdf")
    assert pdf[0].read_bytes()[:5] == b"%PDF-"
    with pytest.raises(ValueError, match="png, pdf oder beide"):
        skript.schreibe_abbildungen(figuren, tmp_path / "x", messdatei=quelle, format_="svg")


def test_main_liest_die_datei_ueber_lade_svd(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    md = dd.synthetische_messdaten()
    quelle = tmp_path / "mess.svd"
    quelle.write_bytes(b"x")

    class _Geladen:
        messdaten = md

    monkeypatch.setattr(skript, "lade_svd", lambda pfad: _Geladen())
    monkeypatch.setattr(
        skript, "schreibe_abbildungen", lambda figuren, ausgabe, **kw: [ausgabe / "a.png"]
    )
    rc = skript.main([str(quelle), "--ausgabe", str(tmp_path / "o"), "--punkt-label", "100"])
    assert rc == 0
    assert str(tmp_path / "o" / "a.png") in capsys.readouterr().out


def test_fehlende_phasenabbildung_wird_mit_grund_gemeldet_nicht_verschluckt(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    md = dd.synthetische_messdaten()
    echte = zeichne_schwingform

    def zeichne(fig, sd, opt, stil):  # type: ignore[no-untyped-def]
        if opt.darstellung != "betrag":
            raise DarstellungsFehler("Phase nicht verfügbar: keine Referenz.")
        return echte(fig, sd, opt, stil)

    monkeypatch.setattr(skript, "zeichne_schwingform", zeichne)
    fehlend: dict[str, str] = {}
    figuren = skript.erzeuge_figuren(md, fehlend=fehlend)
    assert "schwingform" in figuren and "schwingform_phase" not in figuren
    assert fehlend == {"schwingform_phase": "Phase nicht verfügbar: keine Referenz."}
    assert "schwingform_phase entfällt: Phase nicht verfügbar: keine Referenz." in (
        capsys.readouterr().err
    )
    # ohne Referenz entfällt die Phase erwartungsgemäß ohne Eintrag und ohne Meldung
    monkeypatch.setattr(skript, "zeichne_schwingform", echte)
    leer: dict[str, str] = {}
    skript.erzeuge_figuren(dd.synthetische_messdaten(referenz=False), fehlend=leer)
    assert leer == {} and capsys.readouterr().err == ""


def test_begleitdatei_der_phasenabbildung_nennt_linie_bezug_schwelle_und_spitzenkennzeichen(
    tmp_path: Path,
) -> None:
    md = dd.synthetische_messdaten()
    quelle = tmp_path / "mess.svd"
    quelle.write_bytes(b"x")
    figuren = skript.erzeuge_figuren(md)  # Spitze mit Kennzeichen „auflösungsbegrenzt“
    skript.schreibe_abbildungen(figuren, tmp_path / "abb", messdatei=quelle, dpi=40)
    j = json.loads((tmp_path / "abb" / "mess_schwingform_phase.json").read_text("utf-8"))
    assert j["f_hz"] == pytest.approx(10.0) and j["bezug_label"] == 100
    assert j["gamma2_min"] == pytest.approx(0.9) and j["anzahl_unsicher"] == 0
    assert j["kennzeichen"] == ["aufloesungsbegrenzt"]
    assert j["linien_text"] == "Linie 10,000 Hz · γ² ≥ 0,9 an allen Punkten"
    assert HINWEIS_PHASE_SPRUNG in j["hinweise"]
    # ohne Spitze an der gewählten Linie: kein Kennzeichen, kein Phasenhinweis
    ohne = skript.erzeuge_figuren(md, frequenz_hz=15.0)["schwingform_phase"]
    assert ohne.hilfsobjekte["herkunft_zusatz"]["kennzeichen"] == []
    assert HINWEIS_PHASE_SPRUNG not in ohne.hinweise
    # jede Begleitdatei trägt die Hinweise der Zeichnung
    spektrum = json.loads((tmp_path / "abb" / "mess_spektrum.json").read_text("utf-8"))
    assert isinstance(spektrum["hinweise"], list) and spektrum["hinweise"]


def test_thesis_schwingform_hoehe_folgt_dem_datenaspekt_d_pt_mindestens_12_5(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    datei = Path(__file__).resolve().parents[3] / "Input" / "20261012_ref_Mitte.svd"
    if not datei.is_file():
        pytest.skip("Messdatei nicht vorhanden")
    md = lade_svd(datei).messdaten
    sf = schwingform_daten(md, PaarCache(md), 18.0, komponente="3D")
    z, zoll = skript._schwingform_hochformat(sf, SchwingformOptionen())
    assert z.hilfsobjekte["d_pt"] >= skript.D_PT_MIN
    # eine zu knappe Obergrenze würde d_pt drücken: die Höhe wächst darüber hinaus
    monkeypatch.setattr(skript, "HOEHE_MAX_CM", 8.0)
    z2, zoll2 = skript._schwingform_hochformat(sf, SchwingformOptionen())
    assert zoll2[1] * 2.54 > 8.0 and z2.hilfsobjekte["d_pt"] >= skript.D_PT_MIN
    assert zoll2[0] == pytest.approx(zoll[0]) and zoll2[1] == pytest.approx(zoll[1], rel=0.2)


# --- P-ABB-S1: Bedienung, Herkunft und Schutzregeln -------------------------------------------


def test_main_beide_formate_namensschema_und_manifest(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    quelle = _messdatei(tmp_path)
    vorher = sha256_datei(quelle)
    rc, ziel = _lauf(monkeypatch, tmp_path, "--punkt-label", "102")
    assert rc == 0 and capsys.readouterr().err == ""
    erwartet = {f"mess_{n}.{e}" for n in BILDER for e in ("png", "pdf", "json")}
    assert {p.name for p in ziel.iterdir()} == erwartet | {"mess_manifest.json"}  # Voreinst. beide
    m = json.loads((ziel / "mess_manifest.json").read_text("utf-8"))
    assert re.fullmatch(r"[0-9a-f]{40}", m["software_git_hash"]) and m["git_dirty"] is False
    assert m["messdatei_sha256"] == sha256_datei(quelle) == vorher  # Rohdatei unverändert
    assert m["messdatei"] == "mess.svd" and m["messdatei_groesse_bytes"] == quelle.stat().st_size
    assert m["skript"].endswith("darstellung_beispiel.py") and m["git_quelle"] == "git"
    assert m["paket_version"] == "0.2.0" and m["aufruf"][-2:] == ["--punkt-label", "102"]
    assert m["parameter"] == {"format": "beide", "dpi": 300, "erlaube_dirty": False}
    assert m["erzeugung"]["antwort"] == "Vib X" and m["erzeugung"]["punkt_label"] == 102
    assert m["erzeugung"]["komponente_phase"] == "Z" and m["ausgelassen"] == {}
    assert {a["nr"]: a["status"] for a in m["annahmen"]}["M8"] == "Annahme"  # M8 offen
    assert m["gamma2_min"] == pytest.approx(0.9) and m["anzahl_m6_ungueltig"] == 0
    assert m["anzahl_gamma2_unter_min"] == 0 and "alle Punkte gültig" in m["m6_hinweis"]
    assert re.fullmatch(r"\d{4}-\d\d-\d\dT\d\d:\d\d:\d\dZ", m["erzeugt_utc"])
    assert set(m["abbildungen"]) == set(BILDER)
    assert m["abbildungen"]["frf"]["dateien"] == ["mess_frf.png", "mess_frf.pdf"]


@pytest.mark.parametrize(("wahl", "endungen"), [("png", {"png"}), ("pdf", {"pdf"})])
def test_main_ein_format(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, wahl: str, endungen: set[str]
) -> None:
    rc, ziel = _lauf(monkeypatch, tmp_path, "--format", wahl)
    assert rc == 0
    assert {p.suffix[1:] for p in ziel.iterdir()} == endungen | {"json"}


def test_zwei_messdateien_im_selben_ordner_kollidieren_nicht(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    ziel = tmp_path / "abb"
    for name in ("a.svd", "b.svd"):
        rc, _ = _lauf(monkeypatch, tmp_path, "--format", "png", ausgabe=ziel, name=name)
        assert rc == 0
    assert (ziel / "a_manifest.json").is_file() and (ziel / "b_manifest.json").is_file()


def test_bild_metadaten_tragen_hash_und_das_pdf_kein_erstellungsdatum(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    rc, ziel = _lauf(monkeypatch, tmp_path)
    assert rc == 0
    png = (ziel / "mess_spektrum.png").read_bytes()
    pdf = (ziel / "mess_spektrum.pdf").read_bytes()
    assert HASH.encode() in png and HASH.encode() in pdf
    assert sha256_datei(tmp_path / "mess.svd").encode() in png
    assert b"CreationDate" not in pdf and b"ModDate" not in pdf


def test_zwei_laeufe_liefern_gleiche_dateien(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    (rc1, a), (rc2, b) = (
        _lauf(monkeypatch, tmp_path, ausgabe=tmp_path / "eins"),
        _lauf(monkeypatch, tmp_path, ausgabe=tmp_path / "zwei"),
    )
    assert rc1 == rc2 == 0
    namen = sorted(p.name for p in a.iterdir())
    assert namen == sorted(p.name for p in b.iterdir())
    for name in namen:
        if name == "mess_manifest.json":
            ma = json.loads((a / name).read_text("utf-8"))
            mb = json.loads((b / name).read_text("utf-8"))
            for m in (ma, mb):
                del m["erzeugt_utc"], m["aufruf"]  # Zeitstempel und Zielpfad
            assert ma == mb
        else:
            assert (a / name).read_bytes() == (b / name).read_bytes(), name  # bitgleich


def test_paar_komponente_und_bezug_sind_waehlbar() -> None:
    md = dd.synthetische_messdaten()
    info: dict[str, Any] = {}
    z = skript.erzeuge_figuren(md, frequenz_hz=10.0, info=info)["schwingform_phase"]
    assert info["antwort"] == "Vib X" and info["referenz"] == "Ref1"
    assert z.hilfsobjekte["bezug_label"] == info["bezug_label_verwendet"] == 100
    x = skript.erzeuge_figuren(
        md, frequenz_hz=10.0, antwort="Vib Z", referenz="Ref1", komponente="X", bezug_label=102,
        info=info,
    )["schwingform_phase"]  # fmt: skip
    assert info["antwort"] == "Vib Z" and info["komponente_phase"] == "X"
    assert info["bezug_label_angefordert"] == 102 == x.hilfsobjekte["bezug_label"]
    # gleiche Zeichenfunktion und Daten wie direkt gerufen (Komponente X, Bezug Label 102)
    sp = schwingform_daten(md, PaarCache(md), 10.0, komponente="X", referenz="Ref1")
    direkt = zeichne_schwingform(
        neue_figure(THESIS_STIL),
        sp,
        SchwingformOptionen(darstellung="phase_relativ", bezug=2),
        THESIS_STIL,
    )
    np.testing.assert_array_equal(x.hilfsobjekte["winkel_grad"], direkt.hilfsobjekte["winkel_grad"])
    assert not np.array_equal(x.hilfsobjekte["winkel_grad"], z.hilfsobjekte["winkel_grad"])
    # nur Antwort oder nur Referenz wählt das erste passende Paar
    skript.erzeuge_figuren(md, antwort="Vib Y", info=info)
    assert info["antwort"] == "Vib Y"
    skript.erzeuge_figuren(md, referenz="Ref1", info=info)
    assert info["antwort"] == "Vib X"
    with pytest.raises(skript.AbbruchFehler, match="--komponente"):
        skript.erzeuge_figuren(md, komponente="3D")


@pytest.mark.parametrize(
    ("args", "muster"),
    [
        (["--antwort", "Vib Q"], r"Vib Q.*Vorhandene Paare.*Vib X/Ref1, Vib Y/Ref1, Vib Z/Ref1"),
        (["--referenz", "Ref9"], r"Ref9.*Vorhandene Paare"),
        (["--punkt-label", "999"], r"--punkt-label 999.*Vorhandene Labels: 100, 101"),
        (["--bezug-label", "999"], r"--bezug-label 999.*Vorhandene Labels"),
        (["--frequenz-hz", "1e6"], r"Frequenz|Achse|außerhalb"),
    ],
)
def test_fehlerfaelle_enden_mit_exit_2_ohne_traceback_und_ohne_ausgabe(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
    args: list[str],
    muster: str,
) -> None:
    rc, ziel = _lauf(monkeypatch, tmp_path, *args)
    err = capsys.readouterr().err
    assert rc == 2 and err.startswith("Fehler: ") and "Traceback" not in err
    assert re.search(muster, err), err
    assert not ziel.exists()  # nichts geschrieben


def test_unlesbare_oder_fehlende_datei_ist_exit_2(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    kaputt = tmp_path / "kaputt.svd"
    kaputt.write_bytes(b"das ist keine PSV-Datei")
    for datei in (kaputt, tmp_path / "fehlt.svd"):
        rc = skript.main([str(datei), "--ausgabe", str(tmp_path / "o")])
        err = capsys.readouterr().err
        assert rc == 2 and err.startswith("Fehler: ") and str(datei) in err
        assert "Traceback" not in err and not (tmp_path / "o").exists()


def test_ohne_referenz_entfallen_frf_und_phase_mit_grund_exit_0(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    md = dd.synthetische_messdaten(referenz=False)
    rc, ziel = _lauf(monkeypatch, tmp_path, "--format", "png", daten=md)
    assert rc == 0 and capsys.readouterr().err == ""
    assert {p.name for p in ziel.glob("*.png")} == {
        "mess_spektrum.png", "mess_spitzen.png", "mess_schwingform.png"
    }  # fmt: skip
    m = json.loads((ziel / "mess_manifest.json").read_text("utf-8"))
    assert set(m["ausgelassen"]) == {"frf", "schwingform_phase"}
    assert "Kreuzspektrum" in m["ausgelassen"]["frf"] and m["erzeugung"]["referenz"] is None
    assert m["anzahl_gamma2_unter_min"] is None and m["anzahl_m6_ungueltig"] == 0
    # ausdrücklich gewählte Referenz ohne Kreuzspektren: Abbruch
    rc2, _ = _lauf(monkeypatch, tmp_path, "--referenz", "Ref1", daten=md, ausgabe=tmp_path / "o2")
    assert rc2 == 2 and "keine (Datei ohne Kreuzspektren)" in capsys.readouterr().err


def test_nicht_darstellbarer_bezug_ist_exit_3_die_uebrigen_bilder_entstehen(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    md = dd.synthetische_messdaten()
    md.cp[("Vib Z", "Ref1")][2, :] = 0.0  # Punkt 102: |v| = 0, Phase relativ zu ihm undefiniert
    rc, ziel = _lauf(monkeypatch, tmp_path, "--bezug-label", "102", "--format", "png", daten=md)
    err = capsys.readouterr().err
    assert rc == 3 and "schwingform_phase entfällt" in err and "Betrag null" in err
    assert {p.name for p in ziel.glob("*.png")} == {f"mess_{n}.png" for n in BILDER[:-1]}
    m = json.loads((ziel / "mess_manifest.json").read_text("utf-8"))
    assert "Betrag null" in m["ausgelassen"]["schwingform_phase"]
    assert m["anzahl_gamma2_unter_min"] is None


@pytest.mark.parametrize("teil", ["Input", "PyCharmProject", "pycharmprojects/../PYCHARMPROJECT"])
def test_ausgabe_unter_input_oder_pycharmproject_wird_abgelehnt(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
    teil: str,
) -> None:
    ziel = tmp_path / teil / "abb"
    rc, _ = _lauf(monkeypatch, tmp_path, ausgabe=ziel)
    assert rc == 2 and "wird nichts geschrieben" in capsys.readouterr().err
    assert not ziel.exists()
    # Input/ des Repos, auch wenn der Pfad nicht so heißt (Wurzel des Skripts)
    monkeypatch.setattr(skript, "REPO_WURZEL", tmp_path / "repo")
    rc, _ = _lauf(monkeypatch, tmp_path, ausgabe=tmp_path / "repo" / "Input" / "x")
    assert rc == 2 and not (tmp_path / "repo").exists()


def test_vorhandene_ausgabe_wird_nicht_ueberschrieben_exit_2(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    rc, ziel = _lauf(monkeypatch, tmp_path, "--format", "png")
    assert rc == 0
    inhalt = {p.name: p.read_bytes() for p in ziel.iterdir()}
    capsys.readouterr()
    rc, _ = _lauf(monkeypatch, tmp_path, "--format", "png")
    assert rc == 2 and "nicht überschrieben" in capsys.readouterr().err
    assert {p.name: p.read_bytes() for p in ziel.iterdir()} == inhalt
    # nur das Manifest ist schon da: keine Teilausgabe
    teil = tmp_path / "teil"
    teil.mkdir()
    (teil / "mess_manifest.json").write_text("alt", encoding="utf-8")
    rc, _ = _lauf(monkeypatch, tmp_path, ausgabe=teil)
    assert rc == 2 and [p.name for p in teil.iterdir()] == ["mess_manifest.json"]


def test_git_regel_vier_faelle(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    def stand(info: BuildInfo) -> None:
        monkeypatch.setattr(skript, "ermittle_build_info", lambda: info)

    # sauber, Quelle build_info (Wheel auf dem Messrechner)
    stand(replace(SAUBER, quelle="build_info"))
    rc, ziel = _lauf(monkeypatch, tmp_path, "--format", "png", ausgabe=tmp_path / "wheel")
    m = json.loads((ziel / "mess_manifest.json").read_text("utf-8"))
    assert rc == 0 and m["git_quelle"] == "build_info" and capsys.readouterr().err == ""
    # dirty und unbekannt: Abbruch, nichts geschrieben; mit --erlaube-dirty Warnung und Eintrag
    for dirty, wort in ((True, "uncommittete"), (None, "unbekannt")):
        stand(replace(SAUBER, git_dirty=dirty))
        rc, ziel = _lauf(monkeypatch, tmp_path, ausgabe=tmp_path / f"d_{dirty}")
        err = capsys.readouterr().err
        assert rc == 2 and wort in err and "--erlaube-dirty" in err and not ziel.exists()
        rc, ziel = _lauf(monkeypatch, tmp_path, "--erlaube-dirty", "--format", "png", ausgabe=ziel)
        m = json.loads((ziel / "mess_manifest.json").read_text("utf-8"))
        j = json.loads((ziel / "mess_spektrum.json").read_text("utf-8"))
        assert rc == 0 and "WARNUNG: git_dirty" in capsys.readouterr().err
        assert m["git_dirty"] is dirty and j["software_git_dirty"] is dirty
        assert m["parameter"]["erlaube_dirty"] is True
    # Hash fehlt: immer Abbruch, auch mit --erlaube-dirty
    stand(
        BuildInfo(paket_version="0.2.0", git_hash=None, git_dirty=None, quelle="keine", grund="x")
    )
    for extra in ([], ["--erlaube-dirty"]):
        rc, ziel = _lauf(monkeypatch, tmp_path, *extra, ausgabe=tmp_path / "ohne_hash")
        assert rc == 2 and "Kein Git-Hash" in capsys.readouterr().err and not ziel.exists()


def test_warnung_wenn_die_ausgabe_im_arbeitsbaum_liegt(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    repo = tmp_path / "repo"
    (repo / ".git").mkdir(parents=True)
    monkeypatch.setattr(skript, "REPO_WURZEL", repo.resolve())
    rc, _ = _lauf(monkeypatch, tmp_path, "--format", "png", ausgabe=repo / "out")
    assert rc == 0 and "im Git-Arbeitsbaum" in capsys.readouterr().err
    rc, _ = _lauf(monkeypatch, tmp_path, "--format", "png", ausgabe=tmp_path / "ausserhalb")
    assert rc == 0 and capsys.readouterr().err == ""


def test_m6_ungueltige_und_unsichere_punkte_bleiben_im_bild_und_im_manifest(
    tmp_path: Path,
) -> None:
    nv = dd.N_VIB * np.ones(dd.P)
    nv[3] = 1.0  # Punkt 103: Rauschen gleich Signal, γ² weit unter 0,9
    md = dd.synthetische_messdaten(n_vib_je_punkt=nv)
    info: dict[str, Any] = {}
    figuren = skript.erzeuge_figuren(
        md,
        frequenz_hz=10.0,
        annahmen=Annahmen(gueltig=[True, False, True, True, True, True]),  # Punkt 101 ungültig
        info=info,
    )
    z = figuren["schwingform_phase"]
    assert len(z.marker["ungueltig"].get_offsets()) == 1  # Raute, ohne Pfeil
    assert len(z.marker["unsicher"].get_xdata()) == 1  # Kreuz an Punkt 103
    assert info["anzahl_m6_ungueltig"] == 1 and info["anzahl_gamma2_unter_min"] == 1
    assert info["m6_hinweis"] == "M6 gesetzt: 1 Punkte ungültig"
    assert z.hilfsobjekte["herkunft_zusatz"]["anzahl_unsicher"] == 1
    quelle = _messdatei(tmp_path)
    skript.schreibe_abbildungen(
        figuren, tmp_path / "o", messdatei=quelle, dpi=40, build_info=SAUBER, lauf=info
    )
    m = json.loads((tmp_path / "o" / "mess_manifest.json").read_text("utf-8"))
    assert m["anzahl_m6_ungueltig"] == 1 and m["anzahl_gamma2_unter_min"] == 1


def test_skript_importiert_nur_erlaubte_pakete_und_kein_pyplot() -> None:
    quelle = Path(skript.__file__).read_text(encoding="utf-8")
    module: set[str] = set()
    for knoten in ast.walk(ast.parse(quelle)):
        if isinstance(knoten, ast.Import):
            module |= {a.name for a in knoten.names}
        elif isinstance(knoten, ast.ImportFrom) and knoten.module:
            module.add(knoten.module)
    wurzeln = {m.split(".")[0] for m in module}
    fremd = wurzeln - set(sys.stdlib_module_names) - {"__future__"}
    assert fremd <= {"numpy", "matplotlib", "olefile", "ldv_automation"}, fremd
    assert not any("pyplot" in m for m in module)


# --- K-ABB-S1: Befunde des Reviews ----------------------------------------------------------------


def test_schwingform_nutzt_die_referenz_der_oberflaeche_nicht_die_des_paars(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    basis = dd.synthetische_messdaten()
    k = basis.ap["Vib Z"].shape[0]
    drehung = np.exp(1j * 0.3 * np.arange(k))[:, None]
    # Ref2 nur für Z: keine Referenz mit Kreuzspektren aller drei Vib-Kanäle
    md = replace(
        basis,
        cp={**basis.cp, ("Vib Z", "Ref2"): basis.cp[("Vib Z", "Ref1")] * drehung},
        ap={**basis.ap, "Ref2": basis.ap["Ref1"].copy()},
        einheiten={**basis.einheiten, "Ref2": basis.einheiten["Ref1"]},
    )
    rc, ziel = _lauf(
        monkeypatch,
        tmp_path,
        "--antwort", "Vib Z", "--referenz", "Ref2", "--format", "png",
        daten=md,
    )  # fmt: skip
    assert rc == 0
    assert skript._schwingform_referenz(md) == "Ref1"  # wie _phase_referenz der Oberfläche
    m = json.loads((ziel / "mess_manifest.json").read_text("utf-8"))
    assert m["erzeugung"]["referenz"] == "Ref2" and m["erzeugung"]["schwingform_referenz"] == "Ref1"
    assert {p.name for p in ziel.glob("*.png")} == {f"mess_{n}.png" for n in BILDER}
    info: dict[str, Any] = {}
    z = skript.erzeuge_figuren(md, antwort="Vib Z", referenz="Ref2", frequenz_hz=10.0, info=info)

    def direkt(referenz: str) -> Any:
        sp = schwingform_daten(md, PaarCache(md), 10.0, komponente="Z", referenz=referenz)
        return zeichne_schwingform(
            neue_figure(THESIS_STIL),
            sp,
            SchwingformOptionen(darstellung="phase_relativ"),
            THESIS_STIL,
        ).hilfsobjekte["winkel_grad"]

    winkel = z["schwingform_phase"].hilfsobjekte["winkel_grad"]
    np.testing.assert_array_equal(winkel, direkt("Ref1"))
    # mit der Referenz des Paars (nur Z) wäre die Phase nicht darstellbar (alter Stand: Exit 3)
    with pytest.raises(DarstellungsFehler, match="keine Referenz"):
        direkt("Ref2")
    assert info["schwingform_referenz"] == "Ref1" and info["referenz"] == "Ref2"


def test_schwingform_referenz_ohne_vollstaendige_referenz_ist_ref1() -> None:
    assert skript._schwingform_referenz(dd.synthetische_messdaten(referenz=False)) == "Ref1"


def test_import_und_repo_wurzel_bei_flacher_ablage_ohne_ausnahme(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    assert skript.ermittle_repo_wurzel(Path("/darstellung_beispiel.py")) is None
    assert skript.ermittle_repo_wurzel(Path("/opt/tools/darstellung_beispiel.py")) is None
    assert skript.ermittle_repo_wurzel(Path("/a/b/c/auswertung/x.py")) is None
    repo = tmp_path / "repo"
    assert skript.ermittle_repo_wurzel(repo / "software/tools/auswertung/x.py") == repo.resolve()
    # echter Import einer Kopie an flachem Pfad (parents[3] würde hier fehlen)
    flach = tmp_path / "flach"
    flach.mkdir()
    kopie = flach / "darstellung_beispiel_flach.py"
    kopie.write_text(Path(skript.__file__).read_text("utf-8"), encoding="utf-8")
    spec = importlib.util.spec_from_file_location("darstellung_beispiel_flach", kopie)
    assert spec is not None and spec.loader is not None
    modul = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modul)
    assert modul.REPO_WURZEL is None
    # repo-bezogene Prüfungen greifen nicht, die Namenssperren schon
    monkeypatch.setattr(skript, "REPO_WURZEL", None)
    assert skript._im_arbeitsbaum(tmp_path / "out") is False
    skript.pruefe_ausgabe(tmp_path / "out")
    rc, _ = _lauf(monkeypatch, tmp_path, "--format", "png", ausgabe=tmp_path / "out")
    assert rc == 0 and capsys.readouterr().err == ""
    with pytest.raises(skript.AbbruchFehler, match="PyCharmProject"):
        skript.pruefe_ausgabe(tmp_path / "PyCharmProject" / "x")
    with pytest.raises(skript.AbbruchFehler, match="Input"):
        skript.pruefe_ausgabe(tmp_path / "Input" / "x")


def test_schreibfehler_nennt_die_bereits_geschriebenen_dateien_exit_2_kein_manifest(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    echt = Figure.savefig
    aufrufe = [0]

    def fehlerhaft(self: Figure, *args: Any, **kwargs: Any) -> None:
        aufrufe[0] += 1
        if aufrufe[0] == 3:  # dritte Bilddatei: Datenträger voll
            raise OSError(28, "No space left on device")
        echt(self, *args, **kwargs)

    monkeypatch.setattr(Figure, "savefig", fehlerhaft)
    rc, ziel = _lauf(monkeypatch, tmp_path, "--format", "png")
    err = capsys.readouterr().err
    assert rc == 2 and "Traceback" not in err
    assert "Teilausgabe" in err and "No space left" in err
    assert "mess_spektrum.png" in err and "mess_spektrum.json" in err and "mess_frf.png" in err
    assert "Möglicherweise unvollständig: mess_spitzen.png" in err and "kein Manifest" in err
    assert not (ziel / "mess_manifest.json").exists()
    assert (ziel / "mess_spektrum.png").exists() and (ziel / "mess_frf.json").exists()
    # Schreibfehler beim Manifest: alle Bilder vorhanden, Manifest fehlt und wird genannt
    monkeypatch.setattr(Figure, "savefig", echt)
    echt_text = Path.write_text

    def manifest_fehler(self: Path, *args: Any, **kwargs: Any) -> int:
        if self.name.endswith("_manifest.json"):
            raise OSError(13, "Permission denied")
        return echt_text(self, *args, **kwargs)

    monkeypatch.setattr(Path, "write_text", manifest_fehler)
    rc, ziel2 = _lauf(monkeypatch, tmp_path, "--format", "png", ausgabe=tmp_path / "m")
    err = capsys.readouterr().err
    assert rc == 2 and "Möglicherweise unvollständig: mess_manifest.json" in err
    assert "mess_schwingform_phase.png" in err and not (ziel2 / "mess_manifest.json").exists()


def test_meldung_input_ausserhalb_des_repos_behauptet_keine_rohdaten(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    monkeypatch.setattr(skript, "REPO_WURZEL", tmp_path / "repo")
    rc, _ = _lauf(monkeypatch, tmp_path, ausgabe=tmp_path / "input" / "x")
    err = capsys.readouterr().err
    assert rc == 2 and "Pfadkomponente „Input“ ist gesperrt" in err and "wird nichts" in err
    assert "(Rohdaten)" not in err
    # im Repo bleibt die Rohdaten-Meldung
    rc, _ = _lauf(monkeypatch, tmp_path, ausgabe=tmp_path / "repo" / "Input" / "x")
    assert rc == 2 and "unter Input/ (Rohdaten)" in capsys.readouterr().err


# --- K2-ABB-S1: andere Ausnahmen beim Schreiben (Re-Review RR-ABB-S1) -----------------------------


def test_fremde_ausnahme_beim_speichern_wird_teilausgabe_mit_ursache_exit_2(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    echt = Figure.savefig
    aufrufe = [0]

    def fehlerhaft(self: Figure, *args: Any, **kwargs: Any) -> None:
        aufrufe[0] += 1
        if aufrufe[0] == 3:  # dritte Bilddatei: matplotlib lehnt das Bild mit ValueError ab
            raise ValueError("simulierter Zeichenfehler: Bildgröße ungültig")
        echt(self, *args, **kwargs)

    monkeypatch.setattr(Figure, "savefig", fehlerhaft)
    rc, ziel = _lauf(monkeypatch, tmp_path, "--format", "png")
    err = capsys.readouterr().err
    assert rc == 2 and "Traceback" not in err
    assert err.startswith("Fehler: Teilausgabe: ")
    assert "ValueError: simulierter Zeichenfehler: Bildgröße ungültig" in err
    assert "mess_spektrum.png" in err and "mess_spektrum.json" in err and "mess_frf.png" in err
    assert "Möglicherweise unvollständig: mess_spitzen.png" in err and "kein Manifest" in err
    assert not (ziel / "mess_manifest.json").exists()
    assert (ziel / "mess_spektrum.png").exists() and (ziel / "mess_frf.json").exists()


def test_keyboardinterrupt_wird_nicht_in_teilausgabe_verpackt(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    figuren = skript.erzeuge_figuren(dd.synthetische_messdaten())

    def abbruch(self: Figure, *args: Any, **kwargs: Any) -> None:
        raise KeyboardInterrupt

    monkeypatch.setattr(Figure, "savefig", abbruch)
    with pytest.raises(KeyboardInterrupt):
        skript.schreibe_abbildungen(figuren, tmp_path / "abb", messdatei=_messdatei(tmp_path))
