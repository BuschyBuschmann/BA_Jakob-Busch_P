"""Achsenoptionen der Zeichenfunktionen (R-073, P-AUSW2 S1; UI-1, UI-2, UI-5, UI-7, UI-8).

Geprüft wird die Figure-Struktur (Grenzen, Skalen, Ticktexte), nicht Pixel. Toleranz der
Grenzen: ``rtol = 1e-9`` (Eingabe → ``float`` → ``set_xlim``: nur Rundung von Dezimaltext). Das
Auto-y über den sichtbaren Bereich wird gegen Handrechnung mit ``rtol = 1e-12`` geprüft.
"""

from __future__ import annotations

import math
from dataclasses import replace

import dar_daten as dd
import numpy as np
import pytest
from matplotlib.axes import Axes
from matplotlib.figure import Figure

from ldv_automation.auswertung.daten import Messdaten
from ldv_automation.darstellung.achsen import (
    TEXT_KEINE_ZAHL,
    TEXT_LOG_NUR_POSITIV,
    TEXT_REIHENFOLGE,
    AchsenFehler,
    AchsenOptionen,
    Bereich,
    feld_text,
    parse_zahl,
    pruefe_bereich,
    sichtbare_y_grenzen,
    uebernehme_eingabe,
    wende_frequenz_an,
)
from ldv_automation.darstellung.auswahl import (
    PaarCache,
    frf_daten,
    gesamtband,
    spektrum_daten,
    spitzen_daten_frf,
)
from ldv_automation.darstellung.bild import neue_figure
from ldv_automation.darstellung.frf import FrfOptionen, zeichne_frf
from ldv_automation.darstellung.spektrum import SpektrumOptionen, zeichne_spektrum
from ldv_automation.darstellung.spitzen import SpitzenOptionen, zeichne_spitzen
from ldv_automation.darstellung.stil import THESIS_STIL

STIL = THESIS_STIL
RTOL = 1e-9


@pytest.fixture(scope="module")
def daten() -> Messdaten:
    return dd.synthetische_messdaten()


@pytest.fixture(scope="module")
def cache(daten: Messdaten) -> PaarCache:
    return PaarCache(daten)


def _fig() -> Figure:
    return neue_figure(STIL, (6.0, 4.0))


def _opt(**kw: object) -> AchsenOptionen:
    return AchsenOptionen(**kw)  # type: ignore[arg-type]


# --- Eingabe und Prüfung (UI-5) -----------------------------------------------------------------


@pytest.mark.parametrize(
    ("text", "soll"),
    [("", None), ("  ", None), ("1,5", 1.5), ("1.5", 1.5), (" \u22122,5 ", -2.5), ("1e3", 1000.0)],
)
def test_parse_zahl_dezimalkomma_und_punkt(text: str, soll: float | None) -> None:
    assert parse_zahl(text) == soll  # exakt: gleiche float-Umwandlung


@pytest.mark.parametrize(
    "text", ["abc", "1,2,3", "1.234,5", "nan", "inf", "\u2212", "1_000", "1_0,5", "1e400", "1e"]
)
def test_parse_zahl_ungueltig(text: str) -> None:
    with pytest.raises(AchsenFehler) as info:
        parse_zahl(text)
    assert str(info.value) == TEXT_KEINE_ZAHL


MAL = chr(0xD7)  # Multiplikationszeichen
MINUS = chr(0x2212)


@pytest.mark.parametrize(
    ("text", "soll"),
    [
        ("1,4e-7", 1.4e-7),
        ("1.4E-7", 1.4e-7),
        ("1,4\u00b710\u207b\u2077", 1.4e-7),  # „1,4·10⁻⁷“
        (f"1,4{MAL}10\u207b\u2077", 1.4e-7),
        ("1,4*10\u207b\u2077", 1.4e-7),
        (f"{MINUS}8,5\u00b710\u207b\u2074", -8.5e-4),
        ("10\u207b\u2075", 1e-5),
        (f"{MINUS}10\u207b\u2075", -1e-5),
        ("2,5\u00b710\u00b9\u00b2", 2.5e12),
        ("1,5\u00b710\u207a\u00b3", 1500.0),
    ],
)
def test_parse_zahl_potenzschreibweise_und_exponent(text: str, soll: float) -> None:
    assert parse_zahl(text) == soll  # exakt: Dezimaltext → float, keine 10.0**n-Rundung


@pytest.mark.parametrize(
    "text",
    [
        "1,4\u00b710-7",
        "1,4\u00b7-10\u207b\u2077",
        "1e3\u00b710\u207b\u2077",
        "1,4\u00b710",
        "\u00b710\u207b\u2077",
    ],
)
def test_parse_zahl_kaputte_potenz_ist_ungueltig(text: str) -> None:
    with pytest.raises(AchsenFehler):
        parse_zahl(text)


def test_feld_text_dezimalkomma_und_potenz_fuer_kleine_und_grosse_betraege() -> None:
    assert feld_text(None) == ""
    assert feld_text(1.5) == "1,5"
    assert feld_text(1200.5) == "1200"  # 4 signifikante Stellen
    assert feld_text(0.625) == "0,625"
    assert feld_text(0.0123456789) == "0,01235"  # 4 signifikante Stellen im Dezimalbereich
    assert feld_text(1e-3) == "0,001"  # untere Grenze der Dezimalschreibweise
    assert feld_text(2e-5) == "2\u00b710\u207b\u2075"  # „2·10⁻⁵“
    assert feld_text(1.4e-7) == "1,4\u00b710\u207b\u2077"
    assert feld_text(8.54e-4) == "8,54\u00b710\u207b\u2074"  # Grenzwert 8,5·10⁻⁴ des Betrags
    assert feld_text(-8.5e-4) == f"{MINUS}8,5\u00b710\u207b\u2074"
    assert feld_text(1.23456789e-7) == "1,235\u00b710\u207b\u2077"  # ebenfalls 4 Stellen
    assert feld_text(1e-300) == "10\u207b\u00b3\u2070\u2070"
    assert feld_text(2.5e7) == "2,5\u00b710\u2077"
    assert feld_text(1e6) == "10\u2076"


def test_feld_text_minus_null_und_nicht_endliche_werte() -> None:
    assert feld_text(-0.0) == "0" and feld_text(0.0) == "0"
    assert feld_text(float("nan")) == "\u2013" and feld_text(float("inf")) == "\u221e"


def test_feld_text_grenzen_wechseln_die_schreibweise_nach_dem_gerundeten_wert() -> None:
    # 9,99999e-4 rundet auf 0,001 (nicht „10⁻³“, das beim Einlesen „0,001“ ergäbe)
    assert feld_text(9.99999e-4) == "0,001"
    assert feld_text(999999.9) == "10\u2076"  # rundet auf 10⁶, nicht „1000000“


def test_feld_text_rundreise_feld_wert_feld_ist_stabil_und_rundet_nur_in_der_anzeige() -> None:
    rng = np.random.default_rng(20261110)  # fester Seed: reproduzierbar
    betraege = 10.0 ** rng.uniform(-14.0, 9.0, 5000) * rng.choice([-1.0, 1.0], 5000)
    for wert in betraege:
        text = feld_text(float(wert))
        zurueck = parse_zahl(text)
        assert zurueck is not None and feld_text(zurueck) == text, (wert, text)
        # Anzeige rundet höchstens auf 4 signifikante Stellen (Potenz wie dezimal)
        assert zurueck == pytest.approx(wert, rel=5.1e-4), (wert, text)


def test_feld_text_laenge_bleibt_im_feld() -> None:
    langste = max(
        len(feld_text(v)) for v in (-1.234e-12, 1.234e-300, -0.01235, -123457.0, -9.999e-4, 1.5e8)
    )
    assert langste <= 12  # „\u22121,234·10⁻¹²“; die Feldbreite misst ein GUI-Test mit der Schrift


def test_feld_text_einheitlich_vier_stellen_in_beiden_schreibweisen() -> None:
    assert feld_text(123456.0) == "123500" and feld_text(1234567.0) == "1,235\u00b710\u2076"
    assert feld_text(-1.2344e-7) == f"{MINUS}1,234\u00b710\u207b\u2077"
    assert feld_text(0.00123456) == "0,001235" and feld_text(1.0) == "1"


def test_feld_text_extremwerte_subnormal_und_nahe_dem_maximum() -> None:
    assert feld_text(5e-324) == "4,941\u00b710\u207b\u00b3\u00b2\u2074"  # 4 Stellen, nicht 6
    maximum = float(np.finfo(np.float64).max)
    for wert in (maximum, -maximum, np.nextafter(maximum, 0.0), 1.7975e308):
        text = feld_text(float(wert))
        assert "\u221e" not in text, wert  # kein „∞“
        zurueck = parse_zahl(text)  # wieder einlesbar (nicht aufgerundet über das Maximum)
        assert zurueck is not None and math.isfinite(zurueck)
        assert feld_text(zurueck) == text and zurueck == pytest.approx(wert, rel=1e-3)
    assert feld_text(maximum) == "1,797\u00b710\u00b3\u2070\u2078"
    for wert in (5e-324, 1e-320, 2.2250738585072014e-308):  # subnormal bis kleinste normale Zahl
        zurueck = parse_zahl(feld_text(wert))
        assert zurueck is not None and feld_text(zurueck) == feld_text(wert)


@pytest.mark.parametrize(
    ("text", "soll"),
    [
        ("0,00005\u00b710\u00b3", 0.05),
        ("0.00005\u00b710\u00b3", 0.05),
        ("12345678901234567890\u00b710\u00b2", 1.2345678901234567890e21),
        ("5e-324", 5e-324),
        ("0\u00b710" + "\u2079" * 5000, 0.0),  # 0·10ⁿ ist 0, auch bei riesigem Exponenten
    ],
)
def test_parse_zahl_mantissen_beliebiger_schreibweise(text: str, soll: float) -> None:
    assert parse_zahl(text) == pytest.approx(soll, rel=1e-15, abs=0.0)


@pytest.mark.parametrize(
    "text",
    [
        "1\u00b710\u207b\u2074\u2070\u2070",  # „1·10⁻⁴⁰⁰“: Unterlauf auf 0
        "1e-400",
        "1,5\u00b710\u207b\u00b3\u00b2\u2074",  # Unterlauf
        "1\u00b710\u00b3\u2070\u2079",  # „1·10³⁰⁹“: Überlauf
        "1\u00b710" + "\u2079" * 5000,  # Exponent mit > 4300 Ziffern
        "1\u00b710\u207b" + "\u2079" * 5000,
        "0,00005\u00b710" + "\u2079" * 5000,
        "\u0661\u0662",  # arabisch-indische Ziffern
        "\uff11\uff12",  # Vollbreite-Ziffern
        "\uff11,\uff15",
        "\u0661,\u0665\u00b710\u00b2",
        "1e\u0663",
    ],
)
def test_parse_zahl_unlesbares_ist_achsenfehler_mit_meldung(text: str) -> None:
    with pytest.raises(AchsenFehler) as info:
        parse_zahl(text)
    assert str(info.value) == TEXT_KEINE_ZAHL
    with pytest.raises(AchsenFehler) as info2:  # derselbe Weg wie in der Leiste
        uebernehme_eingabe(text, "von", Bereich(), "linear", "Frequenz")
    assert str(info2.value) == TEXT_KEINE_ZAHL and info2.value.achse == "Frequenz"


# --- eine Regel für Leiste und Zeichnung: Eingabe ------------------------------------------------


def test_uebernehme_eingabe_schreibt_nur_die_gewaehlte_seite() -> None:
    alt = Bereich(2.0, 10.0)
    assert uebernehme_eingabe("3,5", "von", alt, "linear") == Bereich(3.5, 10.0)
    assert uebernehme_eingabe("", "bis", alt, "linear") == Bereich(2.0, None)  # leer = Auto
    assert uebernehme_eingabe("1,4\u00b710\u207b\u2077", "von", Bereich(), "log") == Bereich(
        1.4e-7, None
    )


def test_uebernehme_eingabe_einseitig_jenseits_der_autogegenseite_ist_keine_meldung() -> None:
    # Nur „von“ gesetzt: die Auto-Gegenseite ist hier unbekannt und wird nie geprüft;
    # die Zeichenschicht verschiebt sie (siehe test_einseitige_eingabe_..._verschiebt_die_autoseite)
    assert uebernehme_eingabe("500", "von", Bereich(), "linear") == Bereich(500.0, None)
    assert uebernehme_eingabe("0,001", "bis", Bereich(), "linear") == Bereich(None, 0.001)


@pytest.mark.parametrize(
    ("text", "seite", "alt", "skala", "meldung"),
    [
        ("abc", "von", Bereich(), "linear", TEXT_KEINE_ZAHL),
        ("1_0", "von", Bereich(), "linear", TEXT_KEINE_ZAHL),
        ("20", "von", Bereich(None, 12.0), "linear", TEXT_REIHENFOLGE),
        ("0,1", "bis", Bereich(0.5, None), "linear", TEXT_REIHENFOLGE),
        ("0", "von", Bereich(), "log", TEXT_LOG_NUR_POSITIV),
        (f"{MINUS}1", "bis", Bereich(), "log", TEXT_LOG_NUR_POSITIV),
    ],
)
def test_uebernehme_eingabe_ungueltig(
    text: str, seite: str, alt: Bereich, skala: str, meldung: str
) -> None:
    with pytest.raises(AchsenFehler) as info:
        uebernehme_eingabe(text, seite, alt, skala, "Frequenz")  # type: ignore[arg-type]
    assert str(info.value) == meldung and info.value.achse == "Frequenz"


def test_pruefe_bereich_alle_faelle() -> None:
    pruefe_bereich(Bereich(), "log")
    pruefe_bereich(Bereich(1.0, None), "log")
    pruefe_bereich(Bereich(1.0, 2.0), "linear")
    pruefe_bereich(Bereich(-2.0, 2.0), "linear")
    for bereich, skala, text in [
        (Bereich(2.0, 1.0), "linear", TEXT_REIHENFOLGE),
        (Bereich(2.0, 2.0), "linear", TEXT_REIHENFOLGE),
        (Bereich(0.0, 5.0), "log", TEXT_LOG_NUR_POSITIV),
        (Bereich(None, -1.0), "log", TEXT_LOG_NUR_POSITIV),
        (Bereich(float("nan"), None), "linear", TEXT_KEINE_ZAHL),
    ]:
        with pytest.raises(AchsenFehler) as info:
            pruefe_bereich(bereich, skala, "Frequenz")  # type: ignore[arg-type]
        assert str(info.value) == text and info.value.achse == "Frequenz"
    assert issubclass(AchsenFehler, ValueError)


def test_achsenoptionen_unbekannte_skala_und_voreinstellung() -> None:
    with pytest.raises(ValueError, match="unbekannte Skala"):
        AchsenOptionen(frequenz_skala="db")  # type: ignore[arg-type]
    o = AchsenOptionen()
    assert o.frequenz.ist_auto and o.frequenz_skala == "linear" and o.y_bereich("betrag").ist_auto


# --- Auto-y über den sichtbaren Frequenzbereich (Handrechnung) ---------------------------------


def _linie(x: list[float], y: list[float]) -> Axes:
    ax = Figure().subplots()
    ax.plot(x, y)
    return ax


def test_sichtbare_y_grenzen_linear_handrechnung() -> None:
    ax = _linie([1, 2, 3, 4], [10.0, 20.0, 5.0, 40.0])
    ax.set_xlim(1.5, 3.5)  # sichtbar: (2, 20) und (3, 5)
    unten, oben = sichtbare_y_grenzen(ax, log=False) or (0.0, 0.0)
    # Spanne 15, Rand 5 % = 0,75 (axes.ymargin 0,05)
    assert unten == pytest.approx(5.0 - 0.75, rel=1e-12)
    assert oben == pytest.approx(20.0 + 0.75, rel=1e-12)


def test_sichtbare_y_grenzen_log_handrechnung() -> None:
    ax = _linie([1, 2, 3, 4], [10.0, 20.0, 5.0, 40.0])
    ax.set_xlim(1.5, 3.5)
    unten, oben = sichtbare_y_grenzen(ax, log=True) or (0.0, 0.0)
    pad = 0.05 * (math.log10(20.0) - math.log10(5.0))  # Rand im Logarithmus
    assert unten == pytest.approx(10.0 ** (math.log10(5.0) - pad), rel=1e-12)
    assert oben == pytest.approx(10.0 ** (math.log10(20.0) + pad), rel=1e-12)


def test_sichtbare_y_grenzen_randfaelle() -> None:
    ax = _linie([1, 2, 3], [4.0, 4.0, 4.0])  # alle gleich → symmetrischer Rand
    assert sichtbare_y_grenzen(ax, log=False) == pytest.approx((4.0 - 0.2, 4.0 + 0.2))
    ax.set_xlim(10.0, 20.0)  # kein Datum im Bereich
    assert sichtbare_y_grenzen(ax, log=False) is None
    leer = _linie([1, 2], [0.0, -1.0])  # auf der Logarithmusachse nichts darstellbar
    assert sichtbare_y_grenzen(leer, log=True) is None
    null = _linie([1, 2], [0.0, 0.0])
    assert sichtbare_y_grenzen(null, log=False) == pytest.approx((-0.5, 0.5))
    konst_log = _linie([1, 2], [100.0, 100.0])
    unten, oben = sichtbare_y_grenzen(konst_log, log=True) or (0.0, 0.0)
    assert unten == pytest.approx(100.0 * 10**-0.05) and oben == pytest.approx(100.0 * 10**0.05)


# --- Ansicht 1 ----------------------------------------------------------------------------------


def test_ansicht1_ohne_eingabe_wie_none(daten: Messdaten, cache: PaarCache) -> None:
    sd = spektrum_daten(daten, cache, punkt=1)
    a = zeichne_spektrum(_fig(), sd, SpektrumOptionen(), STIL).achsen[0]
    b = zeichne_spektrum(_fig(), sd, SpektrumOptionen(achsen=AchsenOptionen()), STIL).achsen[0]
    assert a.get_xlim() == b.get_xlim() and a.get_ylim() == b.get_ylim()  # alles auto: gleich
    assert b.get_xscale() == "linear" and b.get_yscale() == "log"  # UI-2 Voreinstellung


def test_ui1_ansicht1_grenzen_entsprechen_der_eingabe(daten: Messdaten, cache: PaarCache) -> None:
    sd = spektrum_daten(daten, cache, punkt=1)
    achsen = _opt(frequenz=Bereich(5.0, 12.5), y={"betrag": Bereich(1e-7, 3e-4)})
    z = zeichne_spektrum(_fig(), sd, SpektrumOptionen(achsen=achsen), STIL)
    ax = z.achsen[0]
    assert ax.get_xlim() == pytest.approx((5.0, 12.5), rel=RTOL)
    assert ax.get_ylim() == pytest.approx((1e-7, 3e-4), rel=RTOL)
    assert z.rollen == ("betrag",)


def test_ui2_skalen_umschalten(daten: Messdaten, cache: PaarCache) -> None:
    sd = spektrum_daten(daten, cache, punkt=1)
    lin = zeichne_spektrum(_fig(), sd, SpektrumOptionen(skala="linear", achsen=_opt()), STIL)
    assert lin.achsen[0].get_yscale() == "linear" and lin.achsen[0].get_xscale() == "linear"
    log = zeichne_spektrum(
        _fig(), sd, SpektrumOptionen(achsen=_opt(frequenz_skala="log")), STIL
    ).achsen[0]
    assert log.get_xscale() == "log" and log.get_yscale() == "log"
    assert log.get_xlim() == pytest.approx((float(sd.frequenz_hz[0]), float(sd.frequenz_hz[-1])))


def _linie_ab_null() -> Axes:
    ax = Figure().subplots()
    ax.plot([0.0, 0.5, 1.0, 2.0, 4.0], [1.0, 2.0, 3.0, 2.0, 1.0])  # Frequenzachse beginnt bei 0 Hz
    return ax


def test_logarithmische_frequenzachse_mit_0_hz_nimmt_die_kleinste_positive_frequenz() -> None:
    ax = _linie_ab_null()
    fest = wende_frequenz_an(ax, _opt(frequenz_skala="log"), 0.0, 4.0)
    assert not fest and ax.get_xscale() == "log"  # kein AchsenFehler, nichts gesetzt
    assert ax.get_xlim() == pytest.approx((0.5, 4.0), rel=RTOL)
    ax2 = _linie_ab_null()  # nur „bis“ gesetzt: Auto-Seite unten bleibt positiv
    wende_frequenz_an(ax2, _opt(frequenz=Bereich(None, 2.0), frequenz_skala="log"), 0.0, 4.0)
    assert ax2.get_xlim() == pytest.approx((0.5, 2.0), rel=RTOL)
    ax3 = _linie_ab_null()  # lineare Achse: 0 Hz bleibt die untere Grenze
    wende_frequenz_an(ax3, _opt(), 0.0, 4.0)
    assert ax3.get_xlim() == pytest.approx((0.0, 4.0))


@pytest.mark.filterwarnings("ignore:Data has no positive values")
def test_logarithmische_frequenzachse_ohne_positive_linie_und_ohne_positiven_bereich() -> None:
    ax = Figure().subplots()
    ax.plot([0.0], [1.0])  # nur 0 Hz: drei Dekaden unter der oberen Grenze
    wende_frequenz_an(ax, _opt(frequenz_skala="log"), 0.0, 4.0)
    assert ax.get_xlim() == pytest.approx((4e-3, 4.0), rel=RTOL)
    with pytest.raises(AchsenFehler) as info:
        wende_frequenz_an(Figure().subplots(), _opt(frequenz_skala="log"), 0.0, 0.0)
    assert str(info.value) == TEXT_LOG_NUR_POSITIV


def test_spektrum_log_frequenz_bei_k0_gleich_0(daten: Messdaten, cache: PaarCache) -> None:
    sd = spektrum_daten(daten, cache, punkt=1)
    f = np.asarray(sd.frequenz_hz) - float(sd.frequenz_hz[0])  # f[0] = 0 (k0 = 0)
    sd0 = replace(sd, frequenz_hz=f)
    z = zeichne_spektrum(_fig(), sd0, SpektrumOptionen(achsen=_opt(frequenz_skala="log")), STIL)
    ax = z.achsen[0]
    assert ax.get_xscale() == "log" and ax.get_lines()  # gezeichnet, kein Fehler
    assert ax.get_xlim() == pytest.approx((float(f[1]), float(f[-1])), rel=RTOL)


def test_einseitig_gesetzt_nur_diese_seite_fest(daten: Messdaten, cache: PaarCache) -> None:
    sd = spektrum_daten(daten, cache, punkt=1)
    ax = zeichne_spektrum(
        _fig(), sd, SpektrumOptionen(achsen=_opt(frequenz=Bereich(8.0, None))), STIL
    ).achsen[0]
    assert ax.get_xlim() == pytest.approx((8.0, float(sd.frequenz_hz[-1])), rel=RTOL)


def test_y_auto_folgt_dem_sichtbaren_frequenzbereich(daten: Messdaten, cache: PaarCache) -> None:
    sd = spektrum_daten(daten, cache, punkt=1)
    voll = zeichne_spektrum(_fig(), sd, SpektrumOptionen(), STIL).achsen[0]
    z = zeichne_spektrum(
        _fig(), sd, SpektrumOptionen(achsen=_opt(frequenz=Bereich(25.0, 30.0))), STIL
    )
    ax = z.achsen[0]
    sichtbar = [
        y for k in sd.kurven for f, y in zip(sd.frequenz_hz, k.y, strict=True) if 25.0 <= f <= 30.0
    ]
    # Auto-y rechnet über die Linien im Ausschnitt (log: Rand im Logarithmus), nicht über alle
    erwartet = sichtbare_y_grenzen(ax, log=True)
    assert erwartet is not None
    assert ax.get_ylim() == pytest.approx(erwartet, rel=1e-12)
    assert ax.get_ylim()[1] < voll.get_ylim()[1]  # Resonanz bei 10/20 Hz liegt außerhalb
    assert min(sichtbar) >= ax.get_ylim()[0] and max(sichtbar) <= ax.get_ylim()[1]


def test_gesetzte_seite_jenseits_der_autoseite_erhaelt_die_eingabe() -> None:
    from ldv_automation.darstellung.achsen import wende_y_an

    ax = _linie([1, 2, 3], [1.0, 2.0, 3.0])
    wende_y_an(ax, Bereich(10.0, None), log=False, x_gesetzt=False, name="Betrag")
    unten, oben = ax.get_ylim()
    assert unten == 10.0 and oben > unten  # obere Seite um die Autospanne verschoben
    wende_y_an(ax, Bereich(None, 0.5), log=True, x_gesetzt=False, name="Betrag")
    assert ax.get_ylim()[1] == 0.5 and ax.get_ylim()[0] < 0.5
    with pytest.raises(AchsenFehler):  # beide Seiten gesetzt und verkehrt
        wende_y_an(ax, Bereich(5.0, 1.0), log=False, x_gesetzt=False)


def test_einseitige_eingabe_jenseits_der_gegenseite_verschiebt_die_autoseite(
    daten: Messdaten, cache: PaarCache
) -> None:
    sd = spektrum_daten(daten, cache, punkt=1)
    f_ende = float(sd.frequenz_hz[-1])
    spanne = f_ende - float(sd.frequenz_hz[0])
    achsen = _opt(frequenz=Bereich(f_ende + 10.0, None))  # „von“ hinter dem Datenende
    ax = zeichne_spektrum(_fig(), sd, SpektrumOptionen(achsen=achsen), STIL).achsen[0]
    assert ax.get_xlim() == pytest.approx((f_ende + 10.0, f_ende + 10.0 + spanne), rel=RTOL)
    nur_bis = _opt(frequenz=Bereich(None, 0.1))  # „bis“ vor dem Datenanfang
    ax = zeichne_spektrum(_fig(), sd, SpektrumOptionen(achsen=nur_bis), STIL).achsen[0]
    assert ax.get_xlim() == pytest.approx((0.1 - spanne, 0.1), rel=RTOL)


def test_ungueltige_eingabe_wirft_achsenfehler(daten: Messdaten, cache: PaarCache) -> None:
    sd = spektrum_daten(daten, cache, punkt=1)
    for achsen, text in [
        (_opt(frequenz=Bereich(10.0, 5.0)), TEXT_REIHENFOLGE),
        (_opt(frequenz=Bereich(0.0, 5.0), frequenz_skala="log"), TEXT_LOG_NUR_POSITIV),
        (_opt(y={"betrag": Bereich(-1.0, 2.0)}), TEXT_LOG_NUR_POSITIV),  # y ist logarithmisch
    ]:
        with pytest.raises(AchsenFehler) as info:
            zeichne_spektrum(_fig(), sd, SpektrumOptionen(achsen=achsen), STIL)
        assert str(info.value) == text


# --- Ansicht 2 und UI-7 --------------------------------------------------------------------------


def test_ansicht2_phase_in_grad_betrag_und_kohaerenz(daten: Messdaten, cache: PaarCache) -> None:
    fd = frf_daten(cache, "Vib Z", "Ref1", punkt=1)
    opt = FrfOptionen(
        phase=True,
        achsen=_opt(
            frequenz=Bereich(4.0, 24.0),
            y={"betrag": Bereich(1e-3, 1.0), "phase": Bereich(-90.0, 45.5)},
        ),
    )
    z = zeichne_frf(_fig(), fd, opt, STIL)
    betrag, phase, koh = z.achsen
    assert z.rollen == ("betrag", "phase", "kohaerenz")
    assert betrag.get_xlim() == pytest.approx((4.0, 24.0), rel=RTOL)
    assert koh.get_xlim() == betrag.get_xlim()  # gemeinsame Frequenzachse
    assert betrag.get_ylim() == pytest.approx((1e-3, 1.0), rel=RTOL)
    assert phase.get_ylim() == pytest.approx((-90.0, 45.5), rel=RTOL)  # Grad, nie rad
    assert phase.get_ylabel() == "Phase [°]"
    assert koh.get_ylim() == (0.0, 1.05)  # Kohärenz bleibt fest
    z.figure.draw_without_rendering()
    xt = [t.get_text() for t in koh.get_xticklabels() if t.get_text()]
    assert xt and not any("." in t for t in xt)  # Frequenz mit Dezimalkomma (UI-7)
    pt = [t.get_text() for t in phase.get_yticklabels() if t.get_text()]
    assert pt and not any("." in t for t in pt)


def test_ansicht2_phase_auto_bleibt_plusminus_180(daten: Messdaten, cache: PaarCache) -> None:
    fd = frf_daten(cache, "Vib Z", "Ref1", punkt=1)
    z = zeichne_frf(
        _fig(), fd, FrfOptionen(phase=True, achsen=_opt(frequenz=Bereich(5.0, 15.0))), STIL
    )
    assert z.achsen[1].get_ylim() == (-180.0, 180.0)
    ohne = zeichne_frf(_fig(), fd, FrfOptionen(achsen=_opt()), STIL)
    assert ohne.rollen == ("betrag", "kohaerenz") and len(ohne.achsen) == 2


def test_ansicht2_logarithmische_frequenzachse_mit_komma(
    daten: Messdaten, cache: PaarCache
) -> None:
    fd = frf_daten(cache, "Vib Z", "Ref1", punkt=1)
    z = zeichne_frf(
        _fig(), fd, FrfOptionen(achsen=_opt(frequenz=Bereich(4.0, 9.0), frequenz_skala="log")), STIL
    )
    ax = z.achsen[-1]
    assert ax.get_xscale() == "log" and z.achsen[0].get_xscale() == "log"  # geteilte Achse
    z.figure.draw_without_rendering()
    haupt = [t.get_text() for t in ax.get_xticklabels(minor=False) if t.get_text()]
    neben = [t.get_text() for t in ax.get_xticklabels(minor=True) if t.get_text()]
    assert neben, "enger Logarithmusausschnitt braucht beschriftete Nebenstriche"
    assert not any("." in t for t in [*haupt, *neben])  # Dezimalkomma auch auf der Log-Achse


# --- Ansicht 3 und UI-8 --------------------------------------------------------------------------


def test_ansicht3_oberflaeche_ylim_entspricht_genau_der_eingabe(
    daten: Messdaten, cache: PaarCache
) -> None:
    sd = spitzen_daten_frf(
        cache, "Vib Z", "Ref1", baender=gesamtband(daten.frequenz_hz), gewaehlt=0
    )
    achsen = _opt(frequenz=Bereich(6.0, 25.0), y={"betrag": Bereich(1e-3, 5.0)})
    opt = SpitzenOptionen(beschriftung_im_bild=False, legende_im_bild=False, achsen=achsen)
    z = zeichne_spitzen(_fig(), sd, opt, STIL)
    assert z.achsen[0].get_ylim() == pytest.approx((1e-3, 5.0), rel=RTOL)
    assert z.achsen[0].get_xlim() == pytest.approx((6.0, 25.0), rel=RTOL)
    assert "streifen" not in z.hilfsobjekte


def test_ansicht3_bild_ergaenzt_den_streifen_oberhalb_der_eingabe(
    daten: Messdaten, cache: PaarCache
) -> None:
    sd = spitzen_daten_frf(
        cache, "Vib Z", "Ref1", baender=gesamtband(daten.frequenz_hz), gewaehlt=0
    )
    achsen = _opt(y={"betrag": Bereich(1e-3, 5.0)})
    z = zeichne_spitzen(_fig(), sd, SpitzenOptionen(achsen=achsen), STIL)
    unten, oben = z.achsen[0].get_ylim()
    assert unten == pytest.approx(1e-3, rel=RTOL)
    assert oben > 5.0  # Streifen kommt oberhalb der gewählten oberen Grenze dazu
    anteil = z.hilfsobjekte["streifen"]
    assert math.log(5.0 / 1e-3) / math.log(oben / unten) == pytest.approx(1.0 - anteil, rel=1e-9)


@pytest.mark.parametrize("von_bis", [(6.0, 25.0), (12.0, 22.0), (15.0, 40.0)])
def test_ui8_kasten_bleibt_im_achsenbereich(
    daten: Messdaten, cache: PaarCache, von_bis: tuple[float, float]
) -> None:
    pd = spitzen_daten_frf(cache, "Vib Z", "Ref1", baender=gesamtband(daten.frequenz_hz))
    for index in range(len(pd.spitzen)):
        sd = spitzen_daten_frf(
            cache, "Vib Z", "Ref1", baender=gesamtband(daten.frequenz_hz), gewaehlt=index
        )
        achsen = _opt(frequenz=Bereich(*von_bis))
        z = zeichne_spitzen(_fig(), sd, SpitzenOptionen(achsen=achsen), STIL)
        ax = z.achsen[0]
        z.figure.draw_without_rendering()
        s = sd.spitzen[index]
        innen = von_bis[0] <= s.f_sp_hz <= von_bis[1]
        if not innen:
            assert not any("ζ" in t.get_text() for t in z.texte)
            assert "leitlinie" not in z.hilfsobjekte
            continue
        assert z.texte and "ζ" in z.texte[-1].get_text()  # innerhalb: Kasten der gewählten Spitze
        kasten = z.texte[-1].get_window_extent()
        box = ax.bbox
        assert box.x0 - 1 <= kasten.x0 and kasten.x1 <= box.x1 + 1
        assert box.y0 - 1 <= kasten.y0 and kasten.y1 <= box.y1 + 1


def test_ansicht3_ohne_eingabe_wie_none(daten: Messdaten, cache: PaarCache) -> None:
    sd = spitzen_daten_frf(
        cache, "Vib Z", "Ref1", baender=gesamtband(daten.frequenz_hz), gewaehlt=1
    )
    a = zeichne_spitzen(_fig(), sd, SpitzenOptionen(), STIL).achsen[0]
    b = zeichne_spitzen(_fig(), sd, SpitzenOptionen(achsen=AchsenOptionen()), STIL).achsen[0]
    assert a.get_xlim() == b.get_xlim() and a.get_ylim() == b.get_ylim()


def test_zeichnung_rollen_ohne_achsenwahl_sind_leer() -> None:
    from ldv_automation.darstellung.zeichnung import Zeichnung

    assert Zeichnung(figure=Figure(), achsen=()).rollen == ()


def test_numpy_werte_als_grenzen_gehen_durch(daten: Messdaten, cache: PaarCache) -> None:
    sd = spektrum_daten(daten, cache, punkt=1)
    achsen = _opt(frequenz=Bereich(float(np.float64(5.0)), float(np.float64(9.0))))
    ax = zeichne_spektrum(_fig(), sd, SpektrumOptionen(achsen=achsen), STIL).achsen[0]
    assert ax.get_xlim() == (5.0, 9.0)
