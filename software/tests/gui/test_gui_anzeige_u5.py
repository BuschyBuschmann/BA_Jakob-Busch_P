"""Qt-freie Anzeigelogik für Startdialog, Gerät und Zeitlimit (U5/B1, B3): Standardlauf."""

from __future__ import annotations

from datetime import UTC, datetime
from uuid import uuid4

from ldv_automation.gui import anzeige as a
from ldv_automation.sitzung import GeneratorStand, GeraeteDiagnose, GeraeteStand, StartVorschau

AUS = GeneratorStand(generatoren_an=False, aktiv=False, amplitude_v=0.5, anzahl=1)
AN = GeneratorStand(generatoren_an=True, aktiv=True, amplitude_v=1.0, anzahl=1)


def _v(nr: int, *, punkte: int | None = None, g: GeneratorStand | None = None) -> StartVorschau:
    return StartVorschau(
        eintrag_id=uuid4(),
        nummer=nr,
        name=f"M{nr}",
        einstellungsdatei="D:/v.set",
        zielpfad=None if nr > 2 else f"D:/m/x/{nr:02d}_M{nr}.svd",
        messpunkte=punkte,
        generator=g,
        hinweis="h",
    )


def test_generator_texte() -> None:
    assert a.generator_text(AUS) == "GeneratorsOn: nein, Aktiv: nein, Amplitude: 0.5 V"
    assert a.generator_text(None).count("unbekannt") == 3
    mehr = GeneratorStand(generatoren_an=None, aktiv=False, amplitude_v=None, anzahl=3)
    assert a.generator_text(mehr) == (
        "GeneratorsOn: unbekannt, Aktiv: nein, Amplitude: unbekannt (nur Generator 1 von 3 gelesen)"
    )
    assert [a.generator_kurz(g) for g in (AUS, AN, None, mehr)] == [
        "aus",
        "AKTIV",
        "unbekannt",
        "unbekannt",
    ]


def test_geraet_texte() -> None:
    zeit = datetime(2026, 11, 2, tzinfo=UTC)
    stand = GeraeteStand(messpunkte=9, generator=AUS, quelle="beim Verbinden", zeit=zeit)
    assert a.messpunkte_text(stand) == "9 (gelesen beim Verbinden)"
    assert a.geraet_generator_text(stand).startswith("Generator (gelesen beim Verbinden): ")
    kaputt = GeraeteStand(
        messpunkte=None, generator=AUS, quelle="beim Verbinden", zeit=zeit, fehler="weg"
    )
    assert a.messpunkte_text(kaputt) == "unbekannt (weg)"
    assert a.geraet_generator_text(kaputt) == "Generator (gelesen beim Verbinden): unbekannt (weg)"
    assert a.messpunkte_text(None) == "unbekannt"
    assert "kein Gerätestand" in a.geraet_generator_text(None)


def test_diagnose_text_fuer_t1() -> None:
    assert a.diagnose_text(None) == "nicht verfügbar (Simulator)"
    assert a.diagnose_text(GeraeteDiagnose(aufrufe_anzahl=12, verweigerungen=())) == (
        "12 Zugriffe, keine Verweigerung"
    )
    text = a.diagnose_text(GeraeteDiagnose(aufrufe_anzahl=3, verweigerungen=("X.Y (set): nein",)))
    assert text == "3 Zugriffe, 1 Verweigerungen:\nX.Y (set): nein"


def test_start_texte_und_warnung() -> None:
    bekannt = [_v(1, punkte=9, g=AUS), _v(2, punkte=4, g=AUS)]
    assert a.start_anzahl_text(bekannt) == "2 Messungen, 13 Messpunkte insgesamt (soweit bekannt)"
    assert a.generator_warnung(bekannt) is None
    assert a.start_zeile(bekannt[0]) == ("01", "D:/v.set", "01_M1.svd", "9", "aus")
    assert a.start_tooltip(bekannt[0], 2) == "D:/m/x/01_M1.svd\nh"
    assert a.start_tooltip(bekannt[0], 3) == "9\nh"
    assert a.start_tooltip(bekannt[0], 4).startswith("GeneratorsOn: nein")
    assert a.start_tooltip(bekannt[0], 0) == "01"
    unklar = [*bekannt, _v(3)]
    assert a.start_anzahl_text(unklar) == (
        "3 Messungen, 13 Messpunkte insgesamt (soweit bekannt; bei 1 Messungen unbekannt)"
    )
    assert a.start_zeile(unklar[2])[2:] == ("unbekannt", "unbekannt", "unbekannt")
    warnung = a.generator_warnung(unklar)
    assert warnung is not None and warnung.startswith("✖ Generatorzustand unbekannt (Nr 03;")
    aktiv = [*unklar, _v(4, punkte=1, g=AN)]
    warnung = a.generator_warnung(aktiv)
    assert warnung is not None
    assert warnung.startswith("✖ Generator ist aktiv (Nr 04); Generatorzustand unbekannt (Nr 03;")
    nur_aktiv = a.generator_warnung([_v(1, punkte=1, g=AN)])
    assert nur_aktiv is not None and "unbekannt" not in nur_aktiv


def test_k_u5b_messpunkte_unbekannt_statt_null_und_uebernahme() -> None:
    assert a.start_anzahl_text([_v(3), _v(4)]) == "2 Messungen, Messpunkte insgesamt: unbekannt"
    v = StartVorschau(
        eintrag_id=uuid4(),
        nummer=1,
        name="M",
        einstellungsdatei="D:/v.set",
        zielpfad="D:\\m\\<JJJJ-MM-TT_HHMMSS>_messen\\01_M.svd",
        messpunkte=9,
        generator=AUS,
        hinweis="gelesen in Betriebsart TROCKENLAUF vom …; übernommen",
        uebernommen=True,
    )
    assert a.start_zeile(v)[2:] == ("01_M.svd", "9", "aus (übernommen)")
    assert "TROCKENLAUF" in a.start_tooltip(v, 4)


def test_k_u5b_generatorzeile_im_startdialog_gilt_nur_fuer_diese_datei() -> None:
    zeit = datetime(2026, 11, 2, tzinfo=UTC)
    stand = GeraeteStand(messpunkte=9, generator=AUS, quelle="nach Laden von D:/a.set", zeit=zeit)
    text = a.geraet_generator_text(stand, startdialog=True)
    assert text.startswith("Generator (gelesen nach Laden von D:/a.set): GeneratorsOn: nein")
    assert "gilt nur für diese Datei" in text
    assert "gilt nur" not in a.geraet_generator_text(stand)


def test_b3_standard_limit_hinweis() -> None:
    assert a.standard_limit_hinweis(600.0) == "(Standard: 600 s)"
    assert a.standard_limit_hinweis(42.5) == "(Standard: 42.5 s)"
