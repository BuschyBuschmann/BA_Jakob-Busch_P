"""Thesis-Beispielskript ``tools/auswertung/darstellung_beispiel.py`` (UI-18, P-AUSW T2)."""

from __future__ import annotations

import json
from pathlib import Path

import dar_daten as dd
import darstellung_beispiel as skript
import pytest

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
    with pytest.raises(SystemExit, match="Label 999"):
        skript.erzeuge_figuren(md, punkt_label=999)


def test_schreibe_abbildungen_mit_herkunft_und_ueberschreibschutz(tmp_path: Path) -> None:
    md = dd.synthetische_messdaten()
    quelle = tmp_path / "mess.svd"
    quelle.write_bytes(b"kein echter Container")
    figuren = skript.erzeuge_figuren(md)
    ziel = tmp_path / "abb"
    pfade = skript.schreibe_abbildungen(figuren, ziel, messdatei=quelle, dpi=40)
    assert [p.name for p in pfade] == [f"darstellung_{n}.png" for n in figuren]
    herkunft = json.loads((ziel / "darstellung_spektrum.json").read_text(encoding="utf-8"))
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
    (teil / "darstellung_schwingform.png").write_bytes(b"alt")
    with pytest.raises(FileExistsError, match=r"darstellung_schwingform\.png"):
        skript.schreibe_abbildungen(figuren, teil, messdatei=quelle, dpi=40)
    assert [p.name for p in teil.iterdir()] == ["darstellung_schwingform.png"]
    assert (teil / "darstellung_schwingform.png").read_bytes() == b"alt"
    pdf = skript.schreibe_abbildungen(figuren, tmp_path / "pdf", messdatei=quelle, format_="pdf")
    assert pdf[0].read_bytes()[:5] == b"%PDF-"
    with pytest.raises(ValueError, match="png oder pdf"):
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
    j = json.loads((tmp_path / "abb" / "darstellung_schwingform_phase.json").read_text("utf-8"))
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
    spektrum = json.loads((tmp_path / "abb" / "darstellung_spektrum.json").read_text("utf-8"))
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
