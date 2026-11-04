"""Figure-Struktur der vier Zeichenfunktionen (P-AUSW T2; nicht Pixel).

Geprüft werden Linienzahl, Linienarten, Achsentexte, Skalen, Ticktexte mit Dezimalkomma
(``draw_without_rendering``), Platzhalter und Kennzeichen sowie die Referenzfälle
RF-UI-F4b/F4c/F4d der Fachanalyse.
"""

from __future__ import annotations

import dataclasses
import math
from typing import Any

import dar_daten as dd
import numpy as np
import pytest
from matplotlib.axes import Axes
from matplotlib.figure import Figure
from matplotlib.lines import Line2D

from ldv_automation.auswertung.daten import Messdaten
from ldv_automation.auswertung.export import METHODE_SPITZEN
from ldv_automation.auswertung.spitzen import Spitze
from ldv_automation.darstellung.auswahl import (
    DarstellungsFehler,
    PaarCache,
    SchwingformDaten,
    frf_daten,
    gesamtband,
    schwingform_daten,
    spektrum_daten,
    spitzen_daten_frf,
    spitzen_daten_spektrum,
    standard_bezug,
)
from ldv_automation.darstellung.bild import neue_figure
from ldv_automation.darstellung.formate import MINUS, kennzeichen_unbestaetigt
from ldv_automation.darstellung.frf import (
    HINWEIS_PHASE_VORZEICHEN,
    HOEHEN_MIT_PHASE,
    HOEHEN_OHNE_PHASE,
    PLATZHALTER_PHASE_MITTEL,
    FrfOptionen,
    ohne_umbruch,
    zeichne_frf,
)
from ldv_automation.darstellung.schwingform import (
    HINWEIS_DUBLETTEN,
    HINWEIS_LABELS_AUS,
    HINWEIS_PHASE_SPRUNG,
    KEIN_BEZUGSPUNKT,
    PHASE_KEINE_REFERENZ,
    PHASE_NUR_EINZELKOMPONENTE,
    SchwingformOptionen,
    linien_zeilen,
    winkel_zu_skalenwert,
    zeichne_schwingform,
)
from ldv_automation.darstellung.spektrum import DB_GRUND, SpektrumOptionen, zeichne_spektrum
from ldv_automation.darstellung.spitzen import (
    HINWEIS_ZETA,
    SpitzenOptionen,
    beschriftung_der_spitze,
    zeichne_spitzen,
)
from ldv_automation.darstellung.stil import THESIS_STIL, Plotstil
from ldv_automation.darstellung.zeichnung import Zeichnung

UI_STIL = Plotstil(
    haupt="#0B5C73",
    serienfarben=("#0B5C73", "#1D2327", "#5B6670", "#8A949C"),
    verlauf_hell="#E7F1F4",
    band="#E7E5DF",
    warn_bg="#FFF1CC",
    warn_rand="#8A5A00",
)
STILE = [UI_STIL, THESIS_STIL]


@pytest.fixture(scope="module")
def daten() -> Messdaten:
    return dd.synthetische_messdaten()


@pytest.fixture(scope="module")
def cache(daten: Messdaten) -> PaarCache:
    return PaarCache(daten)


def _tick_texte(achse: Axes, richtung: str = "y") -> list[str]:
    figur = achse.figure
    assert isinstance(figur, Figure)
    figur.draw_without_rendering()
    labels = achse.get_yticklabels() if richtung == "y" else achse.get_xticklabels()
    return [t.get_text() for t in labels if t.get_text()]


def _hoehen(achse: Axes) -> list[float]:
    spec = achse.get_subplotspec()
    assert spec is not None
    ratios = spec.get_gridspec().get_height_ratios()
    assert ratios is not None
    return list(np.asarray(ratios, dtype=np.float64).tolist())


def _komma(texte: list[str]) -> None:
    assert texte, "keine Ticktexte"
    assert not any("." in t for t in texte), texte  # Dezimalpunkt statt -komma


# --- Ansicht 1 --------------------------------------------------------------------------------


@pytest.mark.parametrize("stil", STILE)
def test_spektrum_linienzahl_linienarten_achsentexte(
    daten: Messdaten, cache: PaarCache, stil: Plotstil
) -> None:
    sd = spektrum_daten(daten, cache, punkt=None)
    z = zeichne_spektrum(Figure(), sd, SpektrumOptionen(), stil)
    ax = z.achsen[0]
    assert len(ax.get_lines()) == len(sd.kurven) == 4 == len(z.linien)  # UI-4: eine je Komponente
    arten = [ln.get_linestyle() for ln in z.linien.values()]
    assert len(set(arten)) == 4  # paarweise verschieden
    assert ax.get_xlabel() == "Frequenz [Hz]" and ax.get_ylabel() == "Amplitude [m/s]"  # UI-1
    assert ax.get_yscale() == "log" and ax.get_xscale() == "linear"
    assert ax.get_title() == "" and not z.figure.texts  # kein Diagrammtitel, kein Stempel
    np.testing.assert_array_equal(next(iter(z.linien.values())).get_xdata(), daten.frequenz_hz)
    legende = z.hilfsobjekte["legende"]
    assert legende.get_title().get_text() == (
        f"Geschwindigkeit, kohärent mit Ref1\nBetragsmittel |CPH| über {dd.P} Punkte"
    )  # Mittelformel und Punktzahl im Bild
    assert [t.get_text() for t in legende.get_texts()][-1] == "3D (nicht gegen PSV geprüft)"
    assert z.hinweise == sd.hinweise and len(z.hinweise) == 3  # Formel, 3D-Formel, Punktmenge


def test_spektrum_komponentenwahl_bestimmt_die_linienzahl(
    daten: Messdaten, cache: PaarCache
) -> None:
    for wahl in (("Z",), ("X", "3D"), ("X", "Y", "Z")):
        z = zeichne_spektrum(
            Figure(),
            spektrum_daten(daten, cache, punkt=1, komponenten=wahl),
            SpektrumOptionen(),
            UI_STIL,
        )
        assert len(z.achsen[0].get_lines()) == len(wahl)


def test_spektrum_skala_linear_und_db_nicht_moeglich(daten: Messdaten, cache: PaarCache) -> None:
    sd = spektrum_daten(daten, cache, punkt=0, groesse="leistung")
    z = zeichne_spektrum(Figure(), sd, SpektrumOptionen(skala="linear"), UI_STIL)
    assert z.achsen[0].get_yscale() == "linear"
    assert z.hilfsobjekte["legende"].get_title().get_text() == sd.bezeichnung
    with pytest.raises(ValueError, match="dB ist nicht verfügbar") as info:
        SpektrumOptionen(skala="db")  # type: ignore[arg-type]
    assert DB_GRUND in str(info.value) and "Referenzgröße" in DB_GRUND
    with pytest.raises(ValueError, match="unbekannte Skala"):
        SpektrumOptionen(skala="foo")  # type: ignore[arg-type]


def test_spektrum_ticktexte_mit_dezimalkomma(daten: Messdaten, cache: PaarCache) -> None:
    sd = spektrum_daten(daten, cache, punkt=None, komponenten=("Z",))
    z = zeichne_spektrum(Figure(), sd, SpektrumOptionen(skala="linear"), UI_STIL)
    _komma(_tick_texte(z.achsen[0], "y"))
    assert any("," in t for t in _tick_texte(z.achsen[0], "y"))  # z. B. „0,005“
    # logarithmische Achse: Potenzschreibweise statt „1e-05“
    zl = zeichne_spektrum(Figure(), sd, SpektrumOptionen(), UI_STIL)
    texte = _tick_texte(zl.achsen[0], "y")
    assert not any("e-" in t for t in texte) and not any("." in t for t in texte)


def test_spektrum_wiederholtes_zeichnen_leert_die_figure(
    daten: Messdaten, cache: PaarCache
) -> None:
    fig = Figure()
    sd = spektrum_daten(daten, cache, punkt=None)
    zeichne_spektrum(fig, sd, SpektrumOptionen(), UI_STIL)
    z = zeichne_spektrum(fig, sd, SpektrumOptionen(), UI_STIL)
    assert len(fig.axes) == 1 and len(z.achsen[0].get_lines()) == 4


def test_spektrum_dezimalpunkt_wenn_stil_es_verlangt(daten: Messdaten, cache: PaarCache) -> None:
    stil = Plotstil(dezimalkomma=False)
    sd = spektrum_daten(daten, cache, punkt=0, komponenten=("Z",))
    z = zeichne_spektrum(Figure(), sd, SpektrumOptionen(skala="linear"), stil)
    texte = _tick_texte(z.achsen[0], "y")
    assert any("." in t for t in texte) and not any("," in t for t in texte)


# --- Ansicht 2 --------------------------------------------------------------------------------


@pytest.mark.parametrize("stil", STILE)
def test_frf_betrag_und_koharenz_ohne_phase(
    daten: Messdaten, cache: PaarCache, stil: Plotstil
) -> None:
    fd = frf_daten(cache, "Vib Z", "Ref1", punkt=2)
    z = zeichne_frf(Figure(), fd, FrfOptionen(), stil)
    assert len(z.achsen) == 2 and set(z.linien) == {"H1", "H2", "kohaerenz"}
    assert z.achsen[0].get_ylabel() == "Betrag [(m/s)/N]"  # UI-5: Quotient der Einheiten
    assert (
        z.achsen[1].get_ylabel() == "Kohärenz [1]" and z.achsen[1].get_xlabel() == "Frequenz [Hz]"
    )
    assert z.achsen[1].get_ylim() == (0.0, 1.05)
    assert z.achsen[0].get_yscale() == "log"
    assert z.achsen[0].get_xlabel() == ""  # gemeinsame Achse: nur unten beschriftet
    assert _hoehen(z.achsen[0]) == list(HOEHEN_OHNE_PHASE)
    assert HOEHEN_OHNE_PHASE == (65, 35)
    assert {ln.get_linestyle() for ln in (z.linien["H1"], z.linien["H2"])} == {"-", "--"}
    np.testing.assert_array_equal(z.linien["kohaerenz"].get_ydata(), fd.kohaerenz)
    np.testing.assert_array_equal(z.linien["H1"].get_ydata(), fd.betrag_h1)
    _komma(_tick_texte(z.achsen[1], "y"))
    assert _tick_texte(z.achsen[1], "y") == ["0", "0,5", "1"]


def test_frf_mit_phase_in_grad_und_hoehenverhaeltnis(daten: Messdaten, cache: PaarCache) -> None:
    fd = frf_daten(cache, "Vib Z", "Ref1", punkt=2)
    z = zeichne_frf(Figure(), fd, FrfOptionen(phase=True), UI_STIL)
    assert len(z.achsen) == 3 and HOEHEN_MIT_PHASE == (45, 30, 25)
    assert _hoehen(z.achsen[0]) == [45, 30, 25]
    phase = z.achsen[1]
    assert phase.get_ylabel() == "Phase [°]" and phase.get_ylim() == (-180.0, 180.0)
    assert fd.phase_rad is not None
    ist = z.linien["phase"].get_ydata()
    assert np.nanmax(np.abs(ist)) <= 180.0
    np.testing.assert_array_equal(ist, ohne_umbruch(np.degrees(fd.phase_rad)))  # Anzeige in Grad
    assert [t for t in _tick_texte(phase, "y") if t] == [
        f"{MINUS}180", f"{MINUS}90", "0", "90", "180"
    ]  # fmt: skip


def test_frf_phase_nennt_die_vorzeichenkonvention(daten: Messdaten, cache: PaarCache) -> None:
    fd = frf_daten(cache, "Vib Z", "Ref1", punkt=2)
    z = zeichne_frf(Figure(), fd, FrfOptionen(phase=True), UI_STIL)
    soll = "positiv = Vib Z eilt Ref1 voraus"
    assert HINWEIS_PHASE_VORZEICHEN.format(antwort="Vib Z", referenz="Ref1") == soll
    assert soll in z.alle_texte() and f"Phase: {soll}" in z.hinweise
    assert z.texte[-1].axes is z.achsen[1]  # steht im Phasen-Teilbild
    mittel = zeichne_frf(
        Figure(), frf_daten(cache, "Vib Z", "Ref1", punkt=None), FrfOptionen(phase=True), UI_STIL
    )
    assert not any("positiv" in t for t in mittel.alle_texte())  # ohne Phase keine Konvention
    assert mittel.hinweise == ()


def test_frf_h1_h2_einzeln_abschaltbar(daten: Messdaten, cache: PaarCache) -> None:
    fd = frf_daten(cache, "Vib Z", "Ref1", punkt=0)
    assert set(zeichne_frf(Figure(), fd, FrfOptionen(h2=False), UI_STIL).linien) == {
        "H1",
        "kohaerenz",
    }
    assert set(zeichne_frf(Figure(), fd, FrfOptionen(h1=False), UI_STIL).linien) == {
        "H2",
        "kohaerenz",
    }
    with pytest.raises(ValueError, match="H1 oder H2"):
        FrfOptionen(h1=False, h2=False)
    with pytest.raises(ValueError, match="unbekannte Skala"):
        FrfOptionen(skala="db")  # type: ignore[arg-type]


def test_rf_ui_f4b_mittel_phase_ist_platzhalter_ohne_daten(
    daten: Messdaten, cache: PaarCache
) -> None:
    fd = frf_daten(cache, "Vib Z", "Ref1", punkt=None)
    z = zeichne_frf(
        Figure(), fd, FrfOptionen(phase=True, kennzeichen_phase="unbestätigt (M8)"), UI_STIL
    )
    assert "phase" not in z.linien  # keine Daten im Phasen-Teilbild
    assert PLATZHALTER_PHASE_MITTEL in z.alle_texte()
    assert PLATZHALTER_PHASE_MITTEL == (
        "Phase: für das Mittel nicht definiert (Betragsmittel hat keine Phase)"
    )
    assert not z.achsen[1].get_lines()
    assert {"H1", "H2", "kohaerenz"} <= set(z.linien)  # Betrag und γ² vorhanden
    assert not any("unbestätigt" in t for t in z.alle_texte())  # kein Kennzeichen ohne Phase
    labels = [str(ln.get_label()) for ln in z.achsen[0].get_lines()]
    assert labels == [
        f"Betragsmittel |H1| über {dd.P} Punkte",
        f"Betragsmittel |H2| über {dd.P} Punkte",
    ]
    assert f"γ²: arithmetisches Mittel über {dd.P} Punkte" in z.alle_texte()


def test_frf_kennzeichen_unbestaetigt_nur_mit_text(daten: Messdaten, cache: PaarCache) -> None:
    fd = frf_daten(cache, "Vib Z", "Ref1", punkt=1)
    text = kennzeichen_unbestaetigt(["M8: Polarität der Referenzkanäle offen"])
    mit = zeichne_frf(Figure(), fd, FrfOptionen(phase=True, kennzeichen_phase=text), UI_STIL)
    assert f"{UI_STIL.warn_symbol} {text}" in mit.alle_texte()  # Symbol plus Wort
    ohne = zeichne_frf(Figure(), fd, FrfOptionen(phase=True), UI_STIL)  # ist_annahme False → None
    assert not any("unbestätigt" in t for t in ohne.alle_texte())


def test_ohne_umbruch_unterbricht_nur_an_spruengen() -> None:
    ergebnis = ohne_umbruch(np.array([170.0, 175.0, -175.0, -170.0, 0.0]))
    assert np.isnan(ergebnis[2]) and np.isfinite(ergebnis[[0, 1, 3, 4]]).all()
    glatt = np.array([0.0, 10.0, 20.0])
    np.testing.assert_array_equal(ohne_umbruch(glatt), glatt)
    assert ohne_umbruch(np.array([1.0])).shape == (1,)


def test_ohne_umbruch_laesst_die_erste_probe_nach_dem_sprung_entfallen() -> None:
    """Je Sprung wird die Probe i+1 NaN (Doku): die Linie bricht ab und setzt bei i+2 neu an."""
    eingang = np.array([100.0, 170.0, -170.0, -160.0, 150.0, 160.0])
    ergebnis = ohne_umbruch(eingang)
    assert np.isnan(ergebnis[2]) and np.isnan(ergebnis[4])  # Sprünge bei 1→2 und 3→4
    np.testing.assert_array_equal(ergebnis[[0, 1, 3, 5]], eingang[[0, 1, 3, 5]])
    assert eingang[2] == -170.0  # die Eingabe bleibt unverändert (Kopie)


# --- Ansicht 3 --------------------------------------------------------------------------------


def test_spitzen_marker_band_und_nur_gewaehlte_beschriftung(
    daten: Messdaten, cache: PaarCache
) -> None:
    sd = spitzen_daten_frf(
        cache, "Vib Z", "Ref1", baender=gesamtband(daten.frequenz_hz), gewaehlt=1
    )
    z = zeichne_spitzen(Figure(), sd, SpitzenOptionen(), UI_STIL)
    assert len(sd.spitzen) >= 2
    assert len(z.marker["spitzen"].get_xdata()) == len(sd.spitzen)  # alle Spitzen markiert
    np.testing.assert_array_equal(z.marker["spitzen"].get_xdata(), [s.f_sp_hz for s in sd.spitzen])
    beschriftungen = [t for t in z.alle_texte() if "ζ" in t]  # nur eine Spitze beschriftet
    s = sd.spitzen[1]
    assert beschriftungen == [beschriftung_der_spitze(s, warn_symbol=UI_STIL.warn_symbol)]
    assert "," in beschriftungen[0] and "." not in beschriftungen[0]
    assert METHODE_SPITZEN in beschriftungen[0] and "ζ ≈" in beschriftungen[0]
    assert HINWEIS_ZETA in z.hinweise
    assert len(z.hilfsobjekte["baender"]) == 1  # schattierte Fläche, UI-8
    assert z.achsen[0].get_ylabel() == "Betrag [(m/s)/N]" and len(z.achsen[0].get_lines()) == 3
    assert z.marker["gewaehlt"].get_xdata()[0] == s.f_sp_hz
    kurve = z.linien["kurve"]
    assert kurve.get_zorder() > z.hilfsobjekte["baender"][0].get_zorder()  # Kurve nicht verdeckt


def test_spitzen_ohne_auswahl_keine_beschriftung(daten: Messdaten, cache: PaarCache) -> None:
    z = zeichne_spitzen(
        Figure(),
        spitzen_daten_frf(cache, "Vib Z", "Ref1"),
        SpitzenOptionen(skala="linear"),
        UI_STIL,
    )
    assert not any("ζ" in t for t in z.alle_texte()) and "gewaehlt" not in z.marker
    assert z.achsen[0].get_yscale() == "linear" and z.hilfsobjekte["baender"] == []
    with pytest.raises(ValueError, match="unbekannte Skala"):
        SpitzenOptionen(skala="x")  # type: ignore[arg-type]


def test_spitzen_ohne_referenz_nennt_den_grund() -> None:
    md = dd.synthetische_messdaten(referenz=False)
    sd = spitzen_daten_spektrum(md, PaarCache(md), "Vib Z", baender=gesamtband(md.frequenz_hz))
    z = zeichne_spitzen(Figure(), sd, SpitzenOptionen(), UI_STIL)
    assert "Keine Spitzensuche: Referenzkanal fehlt." in z.alle_texte()
    assert "spitzen" not in z.marker and z.achsen[0].get_ylabel() == "Amplitude [m/s]"
    assert z.hinweise == ()  # ohne Spitzen keine ζ-Angabe, also kein ζ-Hinweis


def _spitze(**felder: Any) -> Spitze:
    werte: dict[str, Any] = {
        "k": 10,
        "f_k_hz": 65.0,
        "f_sp_hz": 65.121278,
        "hoehe": 1.0,
        "breite_3db_hz": 0.757,
        "q": 86.0,
        "zeta": 0.005814,
        "f_l_hz": 64.7683,
        "f_r_hz": 65.5256,
        "delta": 0.1,
        "kennzeichen": (),
    }
    werte.update(felder)
    return Spitze(**werte)


def test_beschriftung_zeta_hat_signifikante_stellen_statt_fester_nachkommastellen() -> None:
    """MINOR-3: ζ = 1,2345e-4 zeigt zwei signifikante Stellen, nicht „0,0001“ oder „0,0000“."""
    text = beschriftung_der_spitze(_spitze(zeta=1.2345e-4))
    assert text.splitlines()[0].endswith("ζ ≈ 0,00012")


def test_beschriftung_der_spitze_nennt_zeta_bandgrenzen_und_methode() -> None:
    text = beschriftung_der_spitze(_spitze())
    assert text == "f = 65,121 Hz · ζ ≈ 0,0058\n-3dB-Breite, 64,768 … 65,526 Hz"
    assert METHODE_SPITZEN == "-3dB-Breite"  # dieselbe Methode wie im Export (R-055)
    assert (
        beschriftung_der_spitze(_spitze(), dezimalkomma=False)
        == "f = 65.121 Hz · ζ ≈ 0.0058\n-3dB-Breite, 64.768 … 65.526 Hz"
    )


def test_beschriftung_der_spitze_zeigt_warnkennzeichen_mit_symbol_und_wort() -> None:
    kz = ("aufloesungsbegrenzt", "nachbarmode", "ueberlappend", "kohaerenz_niedrig", "neu")
    text = beschriftung_der_spitze(_spitze(kennzeichen=kz))
    erste, methode, zweite = text.split("\n")  # höchstens drei Zeilen, Kennzeichen in einer
    assert erste.endswith("0,0058") and methode.startswith(METHODE_SPITZEN)
    assert zweite.startswith("⚠ ")
    assert zweite == "⚠ auflösungsbegrenzt, Nachbarmode, überlappend, Kohärenz niedrig, neu"
    assert beschriftung_der_spitze(_spitze(kennzeichen=("nachbarmode",)), warn_symbol="!") == (
        beschriftung_der_spitze(_spitze()) + "\n! Nachbarmode"
    )


def test_beschriftung_der_spitze_mit_unbestimmter_breite_ohne_zahl() -> None:
    nan = float("nan")
    text = beschriftung_der_spitze(_spitze(zeta=nan, f_l_hz=nan, f_sp_hz=10.0))
    assert text == "f = 10,000 Hz · ζ = –"  # keine Dämpfungsangabe, also keine Methode
    teil = beschriftung_der_spitze(_spitze(zeta=nan, f_r_hz=nan, kennzeichen=("ueberlappend",)))
    assert teil.startswith("f = 65,121 Hz · ζ = –") and teil.endswith("⚠ überlappend")
    assert METHODE_SPITZEN not in teil


def test_spitzen_hinweis_nennt_die_bedeutung_von_zeta(cache: PaarCache) -> None:
    z = zeichne_spitzen(
        Figure(), spitzen_daten_frf(cache, "Vib Z", "Ref1"), SpitzenOptionen(), UI_STIL
    )
    assert z.hinweise == (HINWEIS_ZETA,)
    assert f"{MINUS}3-dB-Breite" in HINWEIS_ZETA and "Betragsmittels |H1|" in HINWEIS_ZETA
    assert "kein Modaldämpfungswert" in HINWEIS_ZETA


# --- Ansicht 4 --------------------------------------------------------------------------------


def _sf(
    daten: Messdaten, cache: PaarCache, komponente: str = "Z", f: float = 10.0
) -> SchwingformDaten:
    return schwingform_daten(daten, cache, f, komponente=komponente)


@pytest.mark.parametrize("stil", STILE)
def test_schwingform_betrag_fuellung_und_farbleiste(
    daten: Messdaten, cache: PaarCache, stil: Plotstil
) -> None:
    sd = _sf(daten, cache)
    z = zeichne_schwingform(Figure(), sd, SchwingformOptionen(), stil)
    punkte = z.marker["punkte"]
    np.testing.assert_array_equal(punkte.get_offsets(), sd.koordinaten_m[:, :2])  # Ebene xy (UI-9)
    np.testing.assert_array_equal(punkte.get_array(), sd.betrag)
    assert z.achsen[0].get_xlabel() == "x [m]" and z.achsen[0].get_ylabel() == "y [m]"
    assert z.hilfsobjekte["farbleiste"].ax.get_ylabel() == "Betrag Z [m/s]"
    assert len(z.hilfsobjekte["punktlabels"]) == dd.P
    assert z.achsen[0].get_aspect() == 1.0
    assert "kreislegende" not in z.hilfsobjekte  # Kreislegende nur bei Phase
    assert z.figure.texts == []


def test_schwingform_ebene_und_punktlabels_waehlbar(daten: Messdaten, cache: PaarCache) -> None:
    sd = _sf(daten, cache)
    z = zeichne_schwingform(
        Figure(), sd, SchwingformOptionen(ebene="xz", punktlabels=False), UI_STIL
    )
    np.testing.assert_array_equal(z.marker["punkte"].get_offsets(), sd.koordinaten_m[:, [0, 2]])
    assert z.achsen[0].get_ylabel() == "z [m]" and "punktlabels" not in z.hilfsobjekte
    with pytest.raises(ValueError, match="Ebene"):
        SchwingformOptionen(ebene="ab")  # type: ignore[arg-type]
    with pytest.raises(ValueError, match="Darstellung"):
        SchwingformOptionen(darstellung="x")  # type: ignore[arg-type]


def test_schwingform_phase_ref_pfeil_je_punkt_kennzeichen_und_legende(
    daten: Messdaten, cache: PaarCache
) -> None:
    sd = _sf(daten, cache)
    text = kennzeichen_unbestaetigt(["M8"])
    z = zeichne_schwingform(
        Figure(), sd, SchwingformOptionen(darstellung="phase_ref", kennzeichen_phase=text), UI_STIL
    )
    assert f"{UI_STIL.warn_symbol} {text}" in z.alle_texte()
    pfeile = z.hilfsobjekte["pfeile"]
    assert len(pfeile.X) == dd.P  # alle Punkte kohärent: ein Pfeil je Punkt
    assert "kreislegende" in z.hilfsobjekte and "unsicher" not in z.marker
    assert z.hilfsobjekte["farbleiste"].ax.get_ylabel().replace("\n", " ") == "Phase gegen Ref1 [°]"
    assert sd.amplitude is not None
    phase = np.angle(sd.amplitude)
    np.testing.assert_allclose(z.hilfsobjekte["winkel_grad"], np.degrees(phase), rtol=1e-12)
    ohne = zeichne_schwingform(Figure(), sd, SchwingformOptionen(darstellung="phase_ref"), UI_STIL)
    assert not any("unbestätigt" in t for t in ohne.alle_texte())
    assert not np.array_equal(z.marker["punkte"].get_array(), sd.betrag)  # Füllung zeigt die Phase


def test_schwingform_phase_relativ_ist_unabhaengig_vom_vorzeichen_der_referenz(
    daten: Messdaten,
) -> None:
    """Gedrehte Referenz (M8): -CPH ergibt dieselbe relative Phase, die absolute springt um π."""
    c = PaarCache(daten)
    sd = _sf(daten, c)
    z = zeichne_schwingform(Figure(), sd, SchwingformOptionen(darstellung="phase_relativ"), UI_STIL)
    bezug = standard_bezug(sd)
    assert bezug == 0  # größter Betrag (Tie mit Punkt 4: kleinster Index), alle kohärent
    assert z.marker["bezug"].get_xdata()[0] == sd.koordinaten_m[bezug, 0]
    relativ = z.hilfsobjekte["winkel_grad"]
    assert relativ[bezug] == pytest.approx(0.0, abs=1e-9)
    # gedrehte Referenz: alle Amplituden mit -1 multipliziert
    assert sd.amplitude is not None
    gedreht = dataclasses.replace(sd, amplitude=-sd.amplitude)
    z2 = zeichne_schwingform(
        Figure(), gedreht, SchwingformOptionen(darstellung="phase_relativ"), UI_STIL
    )
    kreis = (z2.hilfsobjekte["winkel_grad"] - relativ + 180.0) % 360.0 - 180.0
    np.testing.assert_allclose(kreis, 0.0, atol=1e-9)  # modulo 360°: identisch
    assert z.hilfsobjekte["farbleiste"].ax.get_ylabel().replace("\n", " ") == (
        "Phase relativ zu Punkt 100 [°]"
    )
    absolut = zeichne_schwingform(
        Figure(), sd, SchwingformOptionen(darstellung="phase_ref"), UI_STIL
    ).hilfsobjekte["winkel_grad"]
    absolut_gedreht = zeichne_schwingform(
        Figure(), gedreht, SchwingformOptionen(darstellung="phase_ref"), UI_STIL
    ).hilfsobjekte["winkel_grad"]
    abstand = (absolut_gedreht - absolut) % 360.0
    np.testing.assert_allclose(abstand, 180.0, atol=1e-9)


def test_schwingform_bezugspunkt_waehlbar_und_ohne_bezug_platzhalter(
    daten: Messdaten, cache: PaarCache
) -> None:
    sd = _sf(daten, cache)
    z = zeichne_schwingform(
        Figure(), sd, SchwingformOptionen(darstellung="phase_relativ", bezug=3), UI_STIL
    )
    assert z.marker["bezug"].get_xdata()[0] == sd.koordinaten_m[3, 0]
    # alle Punkte unzuverlässig → kein Bezugspunkt
    schlecht = dd.synthetische_messdaten(n_vib_je_punkt=np.ones(dd.P))
    s2 = schwingform_daten(schlecht, PaarCache(schlecht), 10.0, komponente="Z")
    assert standard_bezug(s2) is None
    z2 = zeichne_schwingform(
        Figure(), s2, SchwingformOptionen(darstellung="phase_relativ"), UI_STIL
    )
    assert KEIN_BEZUGSPUNKT in z2.alle_texte() and "bezug" not in z2.marker


def test_schwingform_vorzeichen_hinweise_der_kreislegende(
    daten: Messdaten, cache: PaarCache
) -> None:
    """Fachabnahme m-1: „eilt <Ziel> voraus“ mit Ref1 bzw. dem Label des Bezugspunkts."""
    sd = _sf(daten, cache)
    ref = zeichne_schwingform(Figure(), sd, SchwingformOptionen(darstellung="phase_ref"), UI_STIL)
    assert "φ > 0: Vib Z eilt Ref1 voraus" in ref.alle_texte()
    rel = zeichne_schwingform(
        Figure(), sd, SchwingformOptionen(darstellung="phase_relativ", bezug=3), UI_STIL
    )
    assert "Δφ > 0: Punkt eilt Punkt 103 voraus" in rel.alle_texte()  # Label = 100 + Index
    assert "Δφ > 0: eilt dem Bezug vor" not in rel.alle_texte()


def test_schwingform_manueller_bezug_wird_geprueft(daten: Messdaten, cache: PaarCache) -> None:
    sd = _sf(daten, cache)
    for falsch in (-1, dd.P, 99):
        fig = Figure()
        with pytest.raises(DarstellungsFehler, match="existiert nicht"):
            zeichne_schwingform(
                fig, sd, SchwingformOptionen(darstellung="phase_relativ", bezug=falsch), UI_STIL
            )
        assert not fig.axes  # vor dem Zeichnen abgelehnt: die Figure bleibt unverändert
    assert sd.amplitude is not None
    for name, wert in (("null", 0.0 + 0.0j), ("nan", complex("nan+nanj")), ("inf", complex("inf"))):
        amplitude = sd.amplitude.copy()
        amplitude[2] = wert
        kaputt = dataclasses.replace(sd, amplitude=amplitude)
        with pytest.raises(DarstellungsFehler, match="Betrag null oder nicht endlich") as info:
            zeichne_schwingform(
                Figure(), kaputt, SchwingformOptionen(darstellung="phase_relativ", bezug=2), UI_STIL
            )
        assert "Bezugspunkt 102" in str(info.value), name
        # derselbe Punkt als Nicht-Bezug ist kein Fehler (nur der Bezug muss definiert sein)
        zeichne_schwingform(
            Figure(), kaputt, SchwingformOptionen(darstellung="phase_relativ", bezug=0), UI_STIL
        )


def test_schwingform_bezug_unter_gamma2_min_ist_im_bild_gekennzeichnet() -> None:
    rauschen = np.array([1e-12, 1.0, 1e-12, 1.0, 1e-12, 1e-12])  # Punkte 1 und 3: γ² < γ²_min
    md = dd.synthetische_messdaten(n_vib_je_punkt=rauschen)
    sd = schwingform_daten(md, PaarCache(md), 10.0, komponente="Z")
    assert sd.kohaerenz is not None and sd.kohaerenz_ok is not None
    assert list(np.flatnonzero(~sd.kohaerenz_ok)) == [1, 3]
    unsicher = zeichne_schwingform(
        Figure(), sd, SchwingformOptionen(darstellung="phase_relativ", bezug=1), UI_STIL
    )
    g2 = sd.kohaerenz[1]
    text = next(t for t in unsicher.alle_texte() if "Bezugspunkt 101 unsicher" in t)
    assert text.startswith(UI_STIL.warn_symbol) and "γ²_min = 0,9" in text and "γ² = " in text
    assert g2 < sd.kohaerenz_min
    assert "bezug" in unsicher.marker  # der Bezug wird trotzdem gezeichnet
    sicher = zeichne_schwingform(
        Figure(), sd, SchwingformOptionen(darstellung="phase_relativ", bezug=0), UI_STIL
    )
    assert not any("unsicher:" in t for t in sicher.alle_texte())
    standard = zeichne_schwingform(
        Figure(), sd, SchwingformOptionen(darstellung="phase_relativ"), UI_STIL
    )
    assert not any("unsicher:" in t for t in standard.alle_texte())  # Voreinstellung ist sicher


def test_schwingform_gamma2_min_wird_nicht_falsch_gerundet() -> None:
    rauschen = np.array([1e-12, 1.0, 1e-12, 1.0, 1e-12, 1e-12])
    md = dd.synthetische_messdaten(n_vib_je_punkt=rauschen)
    sd = dataclasses.replace(
        schwingform_daten(md, PaarCache(md), 10.0, komponente="Z"), kohaerenz_min=0.995
    )
    z = zeichne_schwingform(Figure(), sd, SchwingformOptionen(darstellung="phase_ref"), UI_STIL)
    assert any(t.startswith("γ² < 0,995") for t in z.alle_texte())  # nicht „1,00“ oder „0,99“


def test_schwingform_legende_ohne_doppelmarker(daten: Messdaten) -> None:
    rauschen = np.array([1e-12, 1.0, 1e-12, 1.0, 1e-12, 1e-12])
    md = dd.synthetische_messdaten(n_vib_je_punkt=rauschen)
    sd = schwingform_daten(md, PaarCache(md), 10.0, komponente="Z")
    z = zeichne_schwingform(Figure(), sd, SchwingformOptionen(darstellung="phase_ref"), UI_STIL)
    z.figure.draw_without_rendering()
    legende = z.hilfsobjekte["zeichenerklaerung"]
    assert legende is not None and legende.numpoints == 1
    markers = [ln for ln in legende.findobj(Line2D) if ln.get_marker() == "x"]
    assert len(markers) == 1  # ein Kreuz, nicht zwei


def test_rf_ui_f4d_unzuverlaessige_punkte_bleiben_im_bild_markiert(daten: Messdaten) -> None:
    rauschen = np.array([1e-12, 1.0, 1e-12, 1.0, 1e-12, 1e-12])  # Punkte 1 und 3 mit γ² < γ²_min
    md = dd.synthetische_messdaten(n_vib_je_punkt=rauschen)
    sd = schwingform_daten(md, PaarCache(md), 10.0, komponente="Z")
    assert sd.kohaerenz_ok is not None and list(np.flatnonzero(~sd.kohaerenz_ok)) == [1, 3]
    for modus in ("phase_ref", "phase_relativ"):
        z = zeichne_schwingform(Figure(), sd, SchwingformOptionen(darstellung=modus), UI_STIL)
        kreuz = z.marker["unsicher"]
        np.testing.assert_array_equal(kreuz.get_xdata(), sd.koordinaten_m[[1, 3], 0])
        punkte = z.marker["punkte"].get_offsets()
        assert len(punkte) + len(kreuz.get_xdata()) == dd.P  # nichts gelöscht
        assert len(z.hilfsobjekte["pfeile"].X) == dd.P - 2  # keine Pfeile für unsichere Punkte
        assert any(t.startswith("γ² < 0,9:") for t in z.alle_texte())
    # auch im Betragsbild bleiben unsichere Punkte gekennzeichnet (Layout 4.5, beide Darstellungen)
    zb = zeichne_schwingform(Figure(), sd, SchwingformOptionen(), UI_STIL)
    np.testing.assert_array_equal(zb.marker["unsicher"].get_xdata(), sd.koordinaten_m[[1, 3], 0])
    assert len(zb.marker["punkte"].get_offsets()) == dd.P - 2  # nicht in der Farbskala
    assert any(t.startswith("γ² < 0,9:") for t in zb.alle_texte())
    assert "pfeile" not in zb.hilfsobjekte  # kein Pfeil im Betragsbild


def test_schwingform_phase_fehler(daten: Messdaten, cache: PaarCache) -> None:
    drei_d = _sf(daten, cache, "3D")
    with pytest.raises(DarstellungsFehler, match="Einzelkomponente") as info:
        zeichne_schwingform(Figure(), drei_d, SchwingformOptionen(darstellung="phase_ref"), UI_STIL)
    assert str(info.value) == PHASE_NUR_EINZELKOMPONENTE
    md = dd.synthetische_messdaten(referenz=False)
    ohne_ref = schwingform_daten(md, PaarCache(md), 10.0, komponente="Z")
    with pytest.raises(DarstellungsFehler) as info2:
        zeichne_schwingform(
            Figure(), ohne_ref, SchwingformOptionen(darstellung="phase_ref"), UI_STIL
        )
    assert str(info2.value) == PHASE_KEINE_REFERENZ == "Phase nicht verfügbar: keine Referenz."
    # Betrag geht auch ohne Referenz
    z = zeichne_schwingform(Figure(), ohne_ref, SchwingformOptionen(), UI_STIL)
    assert len(z.marker["punkte"].get_offsets()) == dd.P


def test_rf_ui_f4c_winkelskala_ist_zyklisch_und_pfeilwinkel_stetig() -> None:
    skala = winkel_zu_skalenwert(np.array([-math.pi, math.pi]))
    assert skala[0] == skala[1]  # f(-π) = f(+π), exakt
    a, b = np.radians([179.0, -179.0])
    s = winkel_zu_skalenwert(np.array([a, b]))
    abstand = min(abs(s[0] - s[1]), 1.0 - abs(s[0] - s[1]))
    assert abstand == pytest.approx(2.0 / 360.0, abs=1e-12)  # 2° auf der Skala


def test_keine_zyklische_skala_im_betragsbild_und_umgekehrt(
    daten: Messdaten, cache: PaarCache
) -> None:
    sd = _sf(daten, cache)
    betrag = zeichne_schwingform(Figure(), sd, SchwingformOptionen(), UI_STIL).marker["punkte"]
    phase = zeichne_schwingform(
        Figure(), sd, SchwingformOptionen(darstellung="phase_ref"), UI_STIL
    ).marker["punkte"]
    assert betrag.get_cmap().name == "ldv_verlauf"
    assert phase.get_cmap().name == "twilight"
    assert phase.get_cmap().name not in ("hsv", "jet")


def test_zeichnung_alle_texte_enthaelt_nur_sichtbares(daten: Messdaten, cache: PaarCache) -> None:
    z = zeichne_spektrum(
        neue_figure(UI_STIL), spektrum_daten(daten, cache, punkt=0), SpektrumOptionen(), UI_STIL
    )
    assert isinstance(z, Zeichnung)
    texte = z.alle_texte()
    assert "Frequenz [Hz]" in texte and "" not in texte


# --- K-AUSW-D3: Linie und Zuverlässigkeit im Bild (N-2), kein Messwert, ±180°, Punktzahl ----------


def _unsicher_daten() -> SchwingformDaten:
    rauschen = np.array([1e-12, 1.0, 1e-12, 1.0, 1e-12, 1e-12])  # Punkte 1 und 3: γ² < γ²_min
    md = dd.synthetische_messdaten(n_vib_je_punkt=rauschen)
    return schwingform_daten(md, PaarCache(md), 10.0, komponente="Z")


def test_n2_phasenbild_nennt_linie_und_kohaerenz_an_allen_punkten(
    daten: Messdaten, cache: PaarCache
) -> None:
    sd = _sf(daten, cache)
    f_text = f"{sd.f_hz:.3f}".replace(".", ",")
    for modus in ("phase_ref", "phase_relativ"):
        z = zeichne_schwingform(Figure(), sd, SchwingformOptionen(darstellung=modus), UI_STIL)
        text = z.hilfsobjekte["punktzahl"].get_text().replace("\n", " ")
        assert f"Linie {f_text} Hz" in text and "γ² ≥ 0,9 an allen Punkten" in text
        assert z.hilfsobjekte["linien_text"] == f"Linie {f_text} Hz · γ² ≥ 0,9 an allen Punkten"
        assert z.hilfsobjekte["anzahl_unsicher"] == 0
    assert linien_zeilen(sd, 0, UI_STIL) == (f"Linie {f_text} Hz", "γ² ≥ 0,9 an allen Punkten")
    # im Betragsbild steht die Linie ebenso, die γ²-Zeile wegen der Kohärenz der Komponente
    betrag = zeichne_schwingform(Figure(), sd, SchwingformOptionen(), UI_STIL)
    text = betrag.hilfsobjekte["punktzahl"].get_text().replace("\n", " ")
    assert f"Linie {f_text} Hz" in text and "γ² ≥ 0,9 an allen Punkten" in text
    assert "linien_text" not in betrag.hilfsobjekte  # die Begleitdatei bleibt phasenbezogen
    # 3D hat keine Kohärenz je Komponente: nur die Linie
    sd3d = _sf(daten, cache, komponente="3D")
    text3d = zeichne_schwingform(Figure(), sd3d, SchwingformOptionen(), UI_STIL)
    text3d = text3d.hilfsobjekte["punktzahl"].get_text().replace("\n", " ")
    assert f"Linie {f_text} Hz" in text3d and "γ²" not in text3d


def test_n2_phasenbild_nennt_anzahl_unsicherer_punkte_statt_an_allen_punkten() -> None:
    sd = _unsicher_daten()
    z = zeichne_schwingform(Figure(), sd, SchwingformOptionen(darstellung="phase_ref"), UI_STIL)
    assert z.hilfsobjekte["anzahl_unsicher"] == 2
    assert z.hilfsobjekte["linien_text"].endswith("γ² < 0,9 an 2 Punkten")
    assert "an allen Punkten" not in z.hilfsobjekte["punktzahl"].get_text()


def test_n2_spitzenkennzeichen_melden_phasensprung_zwischen_linien(
    daten: Messdaten, cache: PaarCache
) -> None:
    sd = _sf(daten, cache)
    mit = SchwingformOptionen(darstellung="phase_ref", spitzen_kennzeichen=("aufloesungsbegrenzt",))
    assert HINWEIS_PHASE_SPRUNG == "Phase wechselt bei B < Δf stark von Linie zu Linie"
    assert HINWEIS_PHASE_SPRUNG in zeichne_schwingform(Figure(), sd, mit, UI_STIL).hinweise
    ohne = SchwingformOptionen(darstellung="phase_ref")
    assert HINWEIS_PHASE_SPRUNG not in zeichne_schwingform(Figure(), sd, ohne, UI_STIL).hinweise
    betrag = SchwingformOptionen(spitzen_kennzeichen=("aufloesungsbegrenzt",))
    assert HINWEIS_PHASE_SPRUNG not in zeichne_schwingform(Figure(), sd, betrag, UI_STIL).hinweise
    # nur „aufloesungsbegrenzt“ löst den Hinweis aus, andere Kennzeichen nicht
    nach = SchwingformOptionen(darstellung="phase_ref", spitzen_kennzeichen=("nachbarmode",))
    assert HINWEIS_PHASE_SPRUNG not in zeichne_schwingform(Figure(), sd, nach, UI_STIL).hinweise
    beide = ("nachbarmode", "aufloesungsbegrenzt")
    kz = SchwingformOptionen(darstellung="phase_ref", spitzen_kennzeichen=beide)
    assert HINWEIS_PHASE_SPRUNG in zeichne_schwingform(Figure(), sd, kz, UI_STIL).hinweise


def test_nicht_endlicher_betrag_heisst_kein_messwert_und_nicht_m6(
    daten: Messdaten, cache: PaarCache
) -> None:
    sd = _sf(daten, cache)
    gueltig = sd.gueltig.copy()
    gueltig[4] = False  # M6
    betrag = sd.betrag.copy()
    betrag[2] = np.nan  # kein Messwert, aber nicht M6
    gesetzt = dataclasses.replace(sd, gueltig=gueltig, betrag=betrag)
    z = zeichne_schwingform(Figure(), gesetzt, SchwingformOptionen(), UI_STIL)
    np.testing.assert_array_equal(z.marker["kein_wert"].get_offsets(), sd.koordinaten_m[[2], :2])
    np.testing.assert_array_equal(z.marker["ungueltig"].get_offsets(), sd.koordinaten_m[[4], :2])
    erkl = " ".join(t.get_text() for t in z.hilfsobjekte["zeichenerklaerung"].texts)
    erkl = erkl.replace("\n", " ")
    assert "kein Messwert (1)" in erkl and "ungültig (M6) (1)" in erkl  # je ein eigener Eintrag
    assert "davon 2 gekennzeichnet" in z.hilfsobjekte["punktzahl"].get_text()
    assert len(z.marker["punkte"].get_offsets()) == dd.P - 2
    # ohne M6-Punkt darf „ungültig (M6)“ nicht erscheinen
    nur_nan = dataclasses.replace(sd, betrag=betrag)
    z2 = zeichne_schwingform(Figure(), nur_nan, SchwingformOptionen(), UI_STIL)
    assert "ungueltig" not in z2.marker and "kein_wert" in z2.marker
    assert not any("M6" in t for t in z2.alle_texte())
    # Phasendarstellung: nicht endliche Amplitude
    assert sd.amplitude is not None
    amp = sd.amplitude.copy()
    amp[3] = np.nan
    zp = zeichne_schwingform(
        Figure(),
        dataclasses.replace(sd, amplitude=amp),
        SchwingformOptionen(darstellung="phase_ref"),
        UI_STIL,
    )
    assert "kein_wert" in zp.marker and "ungueltig" not in zp.marker
    assert len(zp.hilfsobjekte["pfeile"].X) == dd.P - 1


def test_phase_am_sprung_bei_plusminus_180_grad_ist_stetig(
    daten: Messdaten, cache: PaarCache
) -> None:
    """+179° und -179° liegen 2° auseinander: Pfeilwinkel und Farbe ebenso (RF-UI-F4c)."""
    sd = _sf(daten, cache)
    assert sd.amplitude is not None
    winkel = np.radians([179.0, -179.0, 0.0, 180.0, 90.0, -90.0])
    amp = np.abs(sd.amplitude) * np.exp(1j * winkel)
    gesetzt = dataclasses.replace(sd, amplitude=amp)
    z = zeichne_schwingform(
        Figure(), gesetzt, SchwingformOptionen(darstellung="phase_ref"), UI_STIL
    )
    z.marker["punkte"].update_scalarmappable()
    pf = z.hilfsobjekte["pfeile"]
    pfeil_grad = np.degrees(np.arctan2(pf.V, pf.U))
    diff = (pfeil_grad[0] - pfeil_grad[1] + 180.0) % 360.0 - 180.0
    assert abs(diff) == pytest.approx(2.0, abs=1e-9)  # kein Sprung von 358° im Pfeilwinkel
    farben = np.asarray(z.marker["punkte"].get_facecolors())[:, :3]
    d_sprung = np.linalg.norm(farben[0] - farben[1])
    d_gegen = np.linalg.norm(farben[2] - farben[3])  # 0° gegen 180°: weit auseinander
    assert d_sprung < 0.1 * d_gegen
    np.testing.assert_allclose(farben[3], farben[0], atol=0.05)  # 180° ≈ 179° ≈ -179°


def test_punktzahl_min_bis_max_in_ansicht_2_und_3_bei_ungleicher_zahl_je_linie() -> None:
    md = dd.synthetische_messdaten()
    cp = {k: v.copy() for k, v in md.cp.items()}
    cp[("Vib Z", "Ref1")][2, 5] = np.nan  # Punkt 2 fehlt an einer Linie
    md = dataclasses.replace(md, cp=cp)
    cache = PaarCache(md)
    fd = frf_daten(cache, "Vib Z", "Ref1", punkt=None)
    assert fd.punktzahl == dd.P and fd.punktzahl_text == f"{dd.P - 1} … {dd.P}"
    z = zeichne_frf(neue_figure(UI_STIL), fd, FrfOptionen(), UI_STIL)
    assert any(f"über {dd.P - 1} … {dd.P} Punkte" in t for t in z.alle_texte())
    sp = spitzen_daten_frf(cache, "Vib Z", "Ref1")
    assert sp.punktzahl_text == f"{dd.P - 1} … {dd.P}"
    assert sp.beschriftung == f"Betragsmittel |H1| über {dd.P - 1} … {dd.P} Punkte, Vib Z/Ref1"
    # gleiche Zahl je Linie: eine Zahl wie bisher
    ok = PaarCache(dd.synthetische_messdaten())
    assert frf_daten(ok, "Vib Z", "Ref1", punkt=None).punktzahl_text == str(dd.P)
    assert frf_daten(ok, "Vib Z", "Ref1", punkt=1).punktzahl_text == ""


def test_n2_bezugsring_liegt_ueber_dem_pfeil_und_unter_dem_marker(
    daten: Messdaten, cache: PaarCache
) -> None:
    sd = _sf(daten, cache)
    z = zeichne_schwingform(Figure(), sd, SchwingformOptionen(darstellung="phase_relativ"), UI_STIL)
    ring = z.marker["bezug"]
    pfeile = z.hilfsobjekte["pfeile"]
    punkte = z.marker["punkte"]
    # der helle Rand des Pfeils darf den Ring nicht unterbrechen, der Marker bleibt darüber
    assert pfeile.get_zorder() < ring.get_zorder() < punkte.get_zorder()


def test_n2_dubletten_melden_hinweis_und_labels_bleiben_getrennt(
    daten: Messdaten, cache: PaarCache
) -> None:
    sd = _sf(daten, cache)
    assert (
        HINWEIS_DUBLETTEN.format(n=2)
        not in zeichne_schwingform(Figure(), sd, SchwingformOptionen(), UI_STIL).hinweise
    )
    k = sd.koordinaten_m.copy()
    k[1] = k[0]  # Punkte 100 und 101 liegen übereinander
    doppelt = dataclasses.replace(sd, koordinaten_m=k)
    for modus in ("betrag", "phase_relativ"):
        fig = neue_figure(UI_STIL, (12.0, 7.4))
        z = zeichne_schwingform(fig, doppelt, SchwingformOptionen(darstellung=modus), UI_STIL)
        assert HINWEIS_DUBLETTEN.format(n=2) in z.hinweise
        labels = z.hilfsobjekte.get("punktlabels")
        if labels is None:  # zu dicht: nur mit Hinweis, nicht still
            assert HINWEIS_LABELS_AUS in z.hinweise
            continue
        fig.draw_without_rendering()
        boxen = [lab.get_window_extent() for lab in labels]
        assert not boxen[0].overlaps(boxen[1])  # beide Labels nicht deckungsgleich
        assert [lab.get_text() for lab in labels[:2]] == ["100", "101"]
    # betrag mit Labels muss hier gelingen, sonst prüft der Test nichts
    z = zeichne_schwingform(
        neue_figure(UI_STIL, (12.0, 7.4)), doppelt, SchwingformOptionen(), UI_STIL
    )
    assert z.hilfsobjekte.get("punktlabels") is not None
    # drei identische Koordinaten: Zahl im Hinweis
    k3 = k.copy()
    k3[2] = k[0]
    dreifach = dataclasses.replace(sd, koordinaten_m=k3)
    z3 = zeichne_schwingform(Figure(), dreifach, SchwingformOptionen(), UI_STIL)
    assert HINWEIS_DUBLETTEN.format(n=3) in z3.hinweise
