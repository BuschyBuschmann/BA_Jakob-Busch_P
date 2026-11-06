"""Darstellung an ``Input/20261012_ref_Mitte.svd`` (P-AUSW T2); ohne Datei übersprungen.

Referenzen: PSV-Punktmittel ``AVGSEQ[ABS[AVG[CPH[…]]]]`` der Datei (RF-UI-F2c; Toleranz
FG-02 Abschnitt 8: rtol 1e-5, atol 1e-6·max|Größe|, Annahme M11), PSV-CPH an Label 132
(= Punktindex 0, bitgleich zum Adapter) und die Projektionsebene xy der Beispieldatei (U-6).
"""

from __future__ import annotations

import json
import re
from collections.abc import Iterator
from dataclasses import replace
from pathlib import Path

import darstellung_beispiel as skript
import numpy as np
import pytest
from matplotlib.figure import Figure

from ldv_automation.auswertung import Toleranzen, werte_aus
from ldv_automation.auswertung.export import sha256_datei
from ldv_automation.auswertung.laden import Geladen, lade_svd
from ldv_automation.auswertung.mittel import HINWEIS_MITTEL_3D_LEISTUNG
from ldv_automation.auswertung.svd_lesen import lese_svd
from ldv_automation.darstellung.auswahl import (
    PaarCache,
    frf_daten,
    gesamtband,
    kanalpaare,
    schwingform_daten,
    spektrum_daten,
    spitzen_daten_frf,
    verfuegbare_groessen,
)
from ldv_automation.darstellung.frf import FrfOptionen, zeichne_frf
from ldv_automation.darstellung.schwingform import SchwingformOptionen, zeichne_schwingform
from ldv_automation.darstellung.spektrum import SpektrumOptionen, zeichne_spektrum
from ldv_automation.darstellung.spitzen import HINWEIS_ZETA, SpitzenOptionen, zeichne_spitzen
from ldv_automation.darstellung.stil import THESIS_STIL
from ldv_automation.protokoll.version import ermittle_build_info

DATEI = Path(__file__).resolve().parents[3] / "Input" / "20261012_ref_Mitte.svd"
pytestmark = pytest.mark.skipif(not DATEI.is_file(), reason="Messdatei nicht vorhanden")
TOL = Toleranzen()
NAMEN = {0: "Vib X", 1: "Vib Y", 2: "Vib Z", 3: "Ref1", 4: "Ref2"}


@pytest.fixture(scope="module")
def geladen() -> Geladen:
    return lade_svd(DATEI)


@pytest.fixture(scope="module")
def cache(geladen: Geladen) -> PaarCache:
    return PaarCache(geladen.messdaten)


def test_ui1_spektrum_nach_dem_oeffnen(geladen: Geladen, cache: PaarCache) -> None:
    sd = spektrum_daten(geladen.messdaten, cache, punkt=None)
    z = zeichne_spektrum(Figure(), sd, SpektrumOptionen(), THESIS_STIL)
    assert len(z.linien) == 4 and len(z.achsen[0].get_lines()) >= 1
    assert z.achsen[0].get_xlabel() == "Frequenz [Hz]"
    assert z.achsen[0].get_ylabel() == "Amplitude [m/s]"
    assert sd.bezeichnung == "Geschwindigkeit, kohärent mit Ref1" and sd.auswahl_text.startswith(
        "Mittel"
    )
    assert verfuegbare_groessen(geladen.messdaten) == {"kohaerent": None, "leistung": None}


def test_rf_ui_f2c_mittel_kohaerent_gegen_psv_avgseq(geladen: Geladen, cache: PaarCache) -> None:
    messung = lese_svd(DATEI)
    geprueft = 0
    for pm in messung.punktmittel:
        if not pm.formel.startswith("AVGSEQ[ABS[AVG[CPH["):
            continue
        t = [NAMEN[int(n)] for n in re.findall(r"T\[(\d+)\]", pm.formel)]
        antwort, referenz = t[0], t[-1]  # CPH[S[a], CP[S[a], S[b]]]
        if antwort not in ("Vib X", "Vib Y", "Vib Z") or referenz != "Ref1":
            continue
        komp = antwort[-1]
        sd = spektrum_daten(
            geladen.messdaten, cache, punkt=None, komponenten=(komp,), referenz="Ref1"
        )
        assert TOL.kurve_stimmt(sd.kurven[0].y, pm.werte), antwort
        geprueft += 1
    assert geprueft == 3  # Vib X, Y, Z gegen die PSV-Punktmittel


def test_rf_ui_f2c_label_132_ist_der_psv_cph(geladen: Geladen, cache: PaarCache) -> None:
    d = geladen.messdaten
    assert int(d.punkte.label[0]) == 132
    sd = spektrum_daten(d, cache, punkt=0, komponenten=("X", "Y", "Z"))
    for kurve in sd.kurven:
        psv_cph = d.cph[(f"Vib {kurve.schluessel}", "Ref1")][0]
        np.testing.assert_array_equal(kurve.y, np.abs(psv_cph))  # bitgleich: Betrag des PSV-CPH


def test_3d_mittel_leistung_ist_wurzel_der_summe_der_ap_mittel_an_der_datei(
    geladen: Geladen, cache: PaarCache
) -> None:
    """Fachabnahme m-9c: quadratisches Mittel der punktweisen 3D-Beträge = √(Σ_c Mittel AP_c).

    Unabhängig gerechnet aus ``ap`` der Datei über die gültigen Punkte (M6). Toleranz
    rtol 1e-10 (float64, Summe über 135 Punkte und 3 Komponenten; Rechenwege unterscheiden
    sich nur in der Summationsreihenfolge), atol 0.
    """
    d = geladen.messdaten
    gueltig = cache.gueltig()
    sd = spektrum_daten(d, cache, punkt=None, komponenten=("3D",), groesse="leistung")
    summe_der_mittel = sum(d.ap[f"Vib {c}"][gueltig].mean(axis=0) for c in "XYZ")
    np.testing.assert_allclose(sd.kurven[0].y, np.sqrt(summe_der_mittel), rtol=1e-10, atol=0.0)
    punktweise = np.sqrt(sum(d.ap[f"Vib {c}"][gueltig] for c in "XYZ"))  # |v|_3D je Punkt
    np.testing.assert_allclose(
        sd.kurven[0].y, np.sqrt(np.mean(punktweise**2, axis=0)), rtol=1e-10, atol=0.0
    )
    assert HINWEIS_MITTEL_3D_LEISTUNG.format(n=int(gueltig.sum())) in sd.hinweise


def test_projektionsebene_der_beispieldatei_ist_xy(geladen: Geladen, cache: PaarCache) -> None:
    ausdehnung = np.ptp(geladen.messdaten.punkte.koordinaten_m, axis=0)
    assert ausdehnung[2] < ausdehnung[0] < ausdehnung[1]  # z fast flach: 0,017 m
    sd = schwingform_daten(geladen.messdaten, cache, 167.5, komponente="Z")
    assert sd.ebene == "xy" and sd.f_hz == 167.5


def test_paarcache_gleich_werte_aus_an_der_datei(geladen: Geladen) -> None:
    """Identisch zur Gesamtauswertung (bitgleich), 2 Paare (Rechenzeit der Prüfungen ~10 s)."""
    kern = werte_aus(geladen.messdaten)
    c = PaarCache(geladen.messdaten)
    for paar in (("Vib Z", "Ref1"), ("Ref2", "Ref1")):
        ist, soll = c.paar(*paar), kern.paare[paar]
        np.testing.assert_array_equal(ist.frf.h1, soll.frf.h1)
        np.testing.assert_array_equal(ist.frf.kohaerenz, soll.frf.kohaerenz)
        np.testing.assert_array_equal(ist.mittel_h1.mittel_betrag, soll.mittel_h1.mittel_betrag)
        assert len(ist.spitzen.spitzen) == len(soll.spitzen.spitzen)
        for a, b in zip(ist.spitzen.spitzen, soll.spitzen.spitzen, strict=True):
            np.testing.assert_array_equal(  # NaN (Breite nicht bestimmt) gilt als gleich
                [a.f_sp_hz, a.hoehe, a.zeta, a.f_l_hz, a.f_r_hz],
                [b.f_sp_hz, b.hoehe, b.zeta, b.f_l_hz, b.f_r_hz],
            )
            assert a.kennzeichen == b.kennzeichen


def test_ansichten_2_bis_4_an_der_datei(geladen: Geladen, cache: PaarCache) -> None:
    d = geladen.messdaten
    assert kanalpaare(d)[0] == ("Vib X", "Ref1") and len(kanalpaare(d)) == 7
    f = zeichne_frf(
        Figure(),
        frf_daten(cache, "Vib Z", "Ref1", punkt=None),
        FrfOptionen(phase=True),
        THESIS_STIL,
    )
    assert "phase" not in f.linien  # Mittel: Platzhalter
    sp = spitzen_daten_frf(cache, "Vib Z", "Ref1", baender=gesamtband(d.frequenz_hz), gewaehlt=10)
    z = zeichne_spitzen(Figure(), sp, SpitzenOptionen(), THESIS_STIL)
    assert len(sp.spitzen) > 100 and len(z.marker["spitzen"].get_xdata()) == len(sp.spitzen)
    beschriftet = [t for t in z.alle_texte() if "ζ" in t]  # trotz >100 Spitzen nur eine
    assert len(beschriftet) == 1
    # Spitze 10 (65,121 Hz) ist auflösungsbegrenzt: ζ mit Bandgrenzen, Methode und Warnzeichen
    assert sp.spitzen[10].kennzeichen == ("aufloesungsbegrenzt",)
    assert beschriftet[0] == (
        "f = 65,121 Hz · ζ ≈ 0,0058\n-3dB-Breite, 64,768 … 65,526 Hz\n⚠ auflösungsbegrenzt"
    )
    assert HINWEIS_ZETA in z.hinweise
    sf = schwingform_daten(d, cache, 167.5, komponente="Z")
    s = zeichne_schwingform(
        Figure(), sf, SchwingformOptionen(darstellung="phase_relativ"), THESIS_STIL
    )
    assert (
        len(s.marker["punkte"].get_offsets())
        + len(s.marker["unsicher"].get_xdata() if "unsicher" in s.marker else [])
        == d.anzahl_punkte
    )  # alle 135 Punkte bleiben im Bild


# --- P-ABB-S1: Abbildungsskript an der Beispieldatei -------------------------------------------

BILDER = ("spektrum", "frf", "spitzen", "schwingform", "schwingform_phase")


@pytest.fixture(scope="module")
def sauberer_stand() -> Iterator[None]:
    """Fester Software-Stand mit echtem Hash (der Arbeitsbaum ist beim Testen oft nicht sauber)."""
    echt = ermittle_build_info()
    if echt.git_hash is None:
        pytest.skip("kein Git-Hash verfügbar")
    mp = pytest.MonkeyPatch()
    mp.setattr(skript, "ermittle_build_info", lambda: replace(echt, git_dirty=False))
    yield
    mp.undo()


def _lauf_main(ziel: Path) -> int:
    return skript.main(
        [str(DATEI), "--ausgabe", str(ziel), "--punkt-label", "132", "--format", "beide"]
    )


@pytest.fixture(scope="module")
def lauf_ordner(sauberer_stand: None, tmp_path_factory: pytest.TempPathFactory) -> Path:
    ziel = tmp_path_factory.mktemp("abb") / "ausgabe"
    vorher = sha256_datei(DATEI)
    assert _lauf_main(ziel) == 0
    assert sha256_datei(DATEI) == vorher  # A9: Rohdatei unverändert
    return ziel


def test_abbildungsskript_erzeugt_fuenf_abbildungen_als_png_und_pdf(lauf_ordner: Path) -> None:
    """A1, A3: Namensschema, Manifest mit 40-stelligem Hash und SHA-256 der Messdatei."""
    stem = DATEI.stem
    erwartet = {f"{stem}_{n}.{e}" for n in BILDER for e in ("png", "pdf", "json")}
    assert {p.name for p in lauf_ordner.iterdir()} == erwartet | {f"{stem}_manifest.json"}
    m = json.loads((lauf_ordner / f"{stem}_manifest.json").read_text("utf-8"))
    assert re.fullmatch(r"[0-9a-f]{40}", m["software_git_hash"])
    assert m["messdatei_sha256"] == sha256_datei(DATEI) and m["git_dirty"] is False
    assert m["erzeugung"]["punkt_label"] == 132 and m["ausgelassen"] == {}
    assert m["anzahl_m6_ungueltig"] == 0 and m["anzahl_gamma2_unter_min"] >= 0
    for n in BILDER:
        assert (lauf_ordner / f"{stem}_{n}.pdf").read_bytes()[:5] == b"%PDF-"
        assert (lauf_ordner / f"{stem}_{n}.png").read_bytes()[:8] == b"\x89PNG\r\n\x1a\n"


def test_abbildungsskript_zweiter_lauf_liefert_gleiche_dateien(
    lauf_ordner: Path, tmp_path: Path
) -> None:
    """Zweite Methode neben der PSV-Referenz: Reproduzierbarkeit (Bilder bitgleich)."""
    zweit = tmp_path / "zwei"
    assert _lauf_main(zweit) == 0
    for datei in sorted(lauf_ordner.iterdir()):
        if datei.name.endswith("_manifest.json"):
            continue  # Zeitstempel und Zielpfad (Aufruf) unterscheiden sich
        assert datei.read_bytes() == (zweit / datei.name).read_bytes(), datei.name


def test_thesis_spektrum_an_label_132_stimmt_mit_dem_psv_cph_ueberein(
    geladen: Geladen,
) -> None:
    """A12 und A2: Kurven der Thesis-Abbildung gegen |PSV-CPH| (rtol 1e-5, atol 1e-6·max)."""
    d = geladen.messdaten
    info: dict[str, object] = {}
    figuren = skript.erzeuge_figuren(d, punkt_label=132, info=info)
    z = figuren["spektrum"]
    for komp in ("X", "Y", "Z"):
        psv = np.abs(d.cph[(f"Vib {komp}", "Ref1")][0])
        ist = np.asarray(z.linien[komp].get_ydata(), dtype=np.float64)
        assert TOL.kurve_stimmt(ist, psv), komp
    assert all(not f.figure.texts for f in figuren.values())  # kein Arbeitsstempel
    assert info["referenz"] == "Ref1" and info["gamma2_min"] == pytest.approx(0.9)
