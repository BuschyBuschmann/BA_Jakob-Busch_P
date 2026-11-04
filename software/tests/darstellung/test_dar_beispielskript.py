"""Thesis-Beispielskript ``tools/auswertung/darstellung_beispiel.py`` (UI-18, P-AUSW T2)."""

from __future__ import annotations

import json
from pathlib import Path

import dar_daten as dd
import darstellung_beispiel as skript
import pytest

from ldv_automation.auswertung.export import sha256_datei
from ldv_automation.darstellung.auswahl import PaarCache, spektrum_daten
from ldv_automation.darstellung.bild import neue_figure
from ldv_automation.darstellung.spektrum import SpektrumOptionen, zeichne_spektrum
from ldv_automation.darstellung.stil import THESIS_STIL


def test_figuren_mit_referenz_haben_dieselben_linien_und_achsentexte_wie_die_oberflaeche() -> None:
    md = dd.synthetische_messdaten()
    figuren = skript.erzeuge_figuren(md)
    assert set(figuren) == {"spektrum", "frf", "spitzen", "schwingform"}
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
        assert z.figure.get_size_inches()[0] == pytest.approx(4.9)  # Satzspiegel A5


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
