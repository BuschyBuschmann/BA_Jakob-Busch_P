"""Tabellenzeilen und Prüfungen der Ansichten 2 bis 4 (P-AUSW T3b), ohne Qt (UI-7, UI-9, UI-24)."""

from __future__ import annotations

import math
from typing import Any

import numpy as np
import pytest
from gui_ausw_hilfen import synth_geladen

from ldv_automation.auswertung.baender import band_amplitude
from ldv_automation.auswertung.spitzen import Spitze
from ldv_automation.darstellung import spitzen as dar_spitzen
from ldv_automation.darstellung.auswahl import PaarCache, gesamtband, kanalpaare
from ldv_automation.gui import daten_auswerten as da


def spitze(**felder: object) -> Spitze:
    werte: dict[str, object] = {
        "k": 12,
        "f_k_hz": 6.0,
        "f_sp_hz": 6.0123456,
        "hoehe": 2.0,
        "breite_3db_hz": 0.4,
        "q": 15.0,
        "zeta": 0.0333333,
        "f_l_hz": 5.8,
        "f_r_hz": 6.2,
        "delta": 0.1,
        "kennzeichen": (),
    }
    werte.update(felder)
    return Spitze(**werte)  # type: ignore[arg-type]


# --- Spitzentabelle (UI-7, R-055) ---------------------------------------------------------------


def test_ui_7_spitzenzeile_hat_zeta_bandgrenzen_und_methode() -> None:
    zeilen, fehler = da.spitzen_zeilen([spitze()])
    assert fehler == ()
    z = zeilen[0]
    assert da.SPITZEN_SPALTEN == (
        "Nr",
        "f_sp [Hz]",
        "ζ",
        "band_u_hz [Hz]",
        "band_o_hz [Hz]",
        "Methode",
        "Kennzeichen",
    )
    assert z.zellen == ("1", "6,012", "0,033", "5,800", "6,200", "-3dB-Breite", "")
    assert z.schluessel == 0
    assert z.sortwerte[:5] == (1.0, 6.0123456, 0.0333333, 5.8, 6.2)


def test_spitzenzeile_kennzeichen_mit_symbol_und_wort() -> None:
    zeilen, _ = da.spitzen_zeilen(
        [spitze(kennzeichen=("aufloesungsbegrenzt", "kohaerenz_niedrig"))], warn_symbol="[!]"
    )
    assert zeilen[0].zellen[-1] == "[!] auflösungsbegrenzt, Kohärenz niedrig"


def test_n4_spitze_ohne_bestimmte_breite_bleibt_sichtbar_mit_strichen() -> None:
    nan = math.nan
    zeilen, fehler = da.spitzen_zeilen(
        [spitze(zeta=nan, f_l_hz=nan, f_r_hz=nan, breite_3db_hz=nan, q=nan)]
    )
    assert fehler == ()
    assert zeilen[0].zellen[2:6] == ("–", "–", "–", "–")
    assert zeilen[0].zellen[1] == "6,012"


def test_ui_7_zeta_ohne_bandgrenzen_wird_nicht_angezeigt_sondern_gemeldet() -> None:
    zeilen, fehler = da.spitzen_zeilen([spitze(), spitze(f_r_hz=math.nan, f_sp_hz=9.0), spitze()])
    assert [z.schluessel for z in zeilen] == [0, 2]
    assert len(fehler) == 1 and "Spitze 2" in fehler[0] and "9,000 Hz" in fehler[0]
    assert "ζ ohne Bandgrenzen" in fehler[0]


def test_spitzen_zeilen_leer() -> None:
    assert da.spitzen_zeilen([]) == ((), ())


def test_kennzeichentexte_stimmen_mit_der_zeichenfunktion_ueberein() -> None:
    assert da.KENNZEICHEN_TEXT == dar_spitzen._KENNZEICHEN_TEXT


def test_spitze_der_linie() -> None:
    s = [spitze(k=3), spitze(k=9)]
    assert da.spitze_der_linie(s, 9) is s[1]
    assert da.spitze_der_linie(s, 4) is None
    assert da.spitze_der_linie([], 0) is None


# --- Bändertabelle (UI-7) -------------------------------------------------------------------------


@pytest.fixture(scope="module")
def datei():  # type: ignore[no-untyped-def]
    g = synth_geladen(mit_ref2=True)
    return g.messdaten, PaarCache(g.messdaten)


def test_ui_7_bandwerte_stimmen_mit_dem_kern_ueberein(datei) -> None:  # type: ignore[no-untyped-def]
    daten, cache = datei
    paar = kanalpaare(daten)[0]
    grenzen = gesamtband(daten.frequenz_hz)
    werte = da.bandwerte_fuer(daten, cache, paar, grenzen)
    zeilen = da.baender_zeilen(werte, grenzen, None)
    # Kohärentes Spektrum des Paars: eine Zeile für das Mittel
    pa = cache.paar(*paar)
    erwartet = band_amplitude(
        pa.mittel_spektrum_kohaerent.mittel_betrag,
        daten.frequenz_hz,
        grenzen[0][0],
        grenzen[0][1],
        annahmen=cache.annahmen,
        delta_f_hz=daten.delta_f_hz,
        bezug="x",
        einheit="m/s",
    )
    koh = next(z for z in zeilen if "kohärentes Spektrum" in z.zellen[4])
    assert koh.sortwerte[3] == float(np.asarray(erwartet.rms))  # bitgleich: derselbe Kern
    assert koh.zellen[:3] == ("1", "0,500", "32,000")
    assert koh.zellen[3].endswith(" m/s") and koh.sortwerte[1:3] == grenzen[0]
    assert koh.zellen[4] == "kohärentes Spektrum Vib X/Ref1 (Betragsmittel)"  # Klartext
    # Leistungsmittel der Vib-Kanäle, keine Referenzkanäle, keine FRF-Bandnorm
    bezuege = [z.zellen[4] for z in zeilen]
    assert sum(b.startswith("Leistungsmittel Vib") for b in bezuege) == 3
    assert "Leistungsmittel Vib X (Punktmittel)" in bezuege
    assert not any(b.startswith("Leistungsmittel Ref") for b in bezuege)
    assert not any("|H1|" in b for b in bezuege)


def test_baender_zeile_fuer_gewaehlten_punkt(datei) -> None:  # type: ignore[no-untyped-def]
    daten, cache = datei
    paar = kanalpaare(daten)[0]
    grenzen = gesamtband(daten.frequenz_hz)
    werte = da.bandwerte_fuer(daten, cache, paar, grenzen)
    ohne = da.baender_zeilen(werte, grenzen, None)
    mit = da.baender_zeilen(werte, grenzen, 2)
    zusatz = [z for z in mit if "Punkt 2" in z.zellen[4]]
    assert len(mit) > len(ohne) and zusatz
    assert all(float(z.sortwerte[3]) > 0 for z in zusatz)


def test_bandwerte_ohne_grenzen_und_ohne_referenz() -> None:
    g = synth_geladen(referenz=False)
    cache = PaarCache(g.messdaten)
    assert da.bandwerte_fuer(g.messdaten, cache, None, ()) == ()
    grenzen = gesamtband(g.messdaten.frequenz_hz)
    zeilen = da.baender_zeilen(da.bandwerte_fuer(g.messdaten, cache, None, grenzen), grenzen, None)
    assert len(zeilen) == 3 and all(z.zellen[4].startswith("Leistungsmittel Vib") for z in zeilen)
    assert da.baender_zeilen([], grenzen, None) == ()


def test_kanalpaar_text() -> None:
    assert da.kanalpaar_text("Vib X", "Ref1") == "Vib X / Ref1"


# --- Frequenzprüfung (UI-9) ---------------------------------------------------------


F = 0.625 * np.arange(1, 1601, dtype=np.float64)


def test_ui_9_frequenz_rastet_auf_die_naechste_linie() -> None:
    p = da.frequenz_pruefen(123.7, F, 0.625)
    assert p.gueltig and p.linie == 197 and p.f_linie_hz == pytest.approx(123.75)
    assert p.naechste_linie == "nächste Linie: 123,750 Hz" and p.fehler == ""


@pytest.mark.parametrize("f", [0.625 - 0.3125, 1000.0 + 0.3125, 500.0])
def test_ui_9_randwerte_sind_gueltig(f: float) -> None:
    assert da.frequenz_pruefen(f, F, 0.625).gueltig


@pytest.mark.parametrize("f", [0.3, 1000.4, 1200.0, -5.0, math.nan, math.inf])
def test_ui_24_eingabe_ausserhalb(f: float) -> None:
    p = da.frequenz_pruefen(f, F, 0.625)
    assert not p.gueltig and p.linie is None and p.naechste_linie == ""
    assert p.fehler.startswith("✖ Frequenz ") and p.fehler.endswith(
        "liegt außerhalb 0,625 … 1000 Hz."
    )


def test_ui_24_meldung_nennt_die_eingegebene_frequenz_wie_im_brief() -> None:
    assert da.frequenz_pruefen(1200.0, F, 0.625).fehler == (
        "✖ Frequenz 1200 Hz liegt außerhalb 0,625 … 1000 Hz."
    )


def test_u4_bereich_stammt_aus_der_achse_der_datei() -> None:
    achse = 0.3125 * np.arange(1, 101, dtype=np.float64)
    assert da.frequenz_pruefen(40.0, achse, 0.3125).fehler.endswith("außerhalb 0,312 … 31,25 Hz.")


def test_band_nummer_faellt_auf_null_zurueck_wenn_das_band_nicht_in_den_grenzen_steht(
    datei: Any,
) -> None:
    daten, cache = datei
    paar = kanalpaare(daten)[0]
    grenzen = gesamtband(daten.frequenz_hz)
    werte = da.bandwerte_fuer(daten, cache, paar, grenzen)
    zeilen = da.baender_zeilen(werte, [(1.0, 2.0)], None)
    assert zeilen and all(z.schluessel == 0 for z in zeilen)


def test_baender_zeilen_ueberspringt_frf_bandnormen_und_referenzkanaele(datei) -> None:  # type: ignore[no-untyped-def]
    daten, cache = datei
    grenzen = gesamtband(daten.frequenz_hz)
    werte = da.bandwerte_fuer(daten, cache, kanalpaare(daten)[0], grenzen)
    assert any(w.groesse == "frf" for w in werte) and any(
        w.bezug == "AP Ref1 Punktmittel" for w in werte
    )
    bezuege = " ".join(z.zellen[4] for z in da.baender_zeilen(werte, grenzen, 0))
    assert "|H1|" not in bezuege and "Ref1 Punktmittel" not in bezuege


def test_bandzeile_nennt_den_punkt_mit_der_nummer_aus_den_labels(datei: Any) -> None:
    daten, cache = datei
    paar = kanalpaare(daten)[0]
    grenzen = gesamtband(daten.frequenz_hz)
    werte = da.bandwerte_fuer(daten, cache, paar, grenzen)
    zeilen = da.baender_zeilen(werte, grenzen, 2, daten.punkte.label.tolist())
    bezuege = [z.zellen[4] for z in zeilen]
    assert "kohärentes Spektrum Vib X/Ref1 (Punkt 12)" in bezuege  # label 12, nicht Index 2
    assert "Autospektrum Vib Y (Punkt 12)" in bezuege
    assert not any("Punkt 2)" in b for b in bezuege)
    ohne_labels = da.baender_zeilen(werte, grenzen, 2)
    assert "kohärentes Spektrum Vib X/Ref1 (Punkt 2)" in [z.zellen[4] for z in ohne_labels]


def test_kern_markiert_bandwerte_strukturiert(datei: Any) -> None:
    daten, cache = datei
    paar = kanalpaare(daten)[0]
    werte = da.bandwerte_fuer(daten, cache, paar, gesamtband(daten.frequenz_hz))
    koh = [w for w in werte if w.art == "spektrum_kohaerent"]
    assert {(w.kanal, w.mittel) for w in koh} == {("Vib X/Ref1", True), ("Vib X/Ref1", False)}
    assert {w.art for w in werte} == {"frf", "spektrum_kohaerent", "ap"}
    ap = {(w.kanal, w.mittel) for w in werte if w.art == "ap"}
    assert ("Vib Z", True) in ap and ("Ref1", False) in ap
    assert all(
        np.ndim(w.rms) == 0 for w in koh if w.mittel and w.rms is not None
    )  # Mittel: ein Wert je Band
    assert all(w.kanal == "Vib X/Ref1" and w.art == "frf" for w in werte if w.groesse == "frf")


def test_zeilenauswahl_haengt_nicht_an_der_kernbeschriftung(datei: Any) -> None:
    from dataclasses import replace

    daten, cache = datei
    paar = kanalpaare(daten)[0]
    grenzen = gesamtband(daten.frequenz_hz)
    werte = da.bandwerte_fuer(daten, cache, paar, grenzen)
    umbenannt = tuple(replace(w, bezug="beliebig umbenannt") for w in werte)
    assert [z.zellen for z in da.baender_zeilen(umbenannt, grenzen, None)] == [
        z.zellen for z in da.baender_zeilen(werte, grenzen, None)
    ]
