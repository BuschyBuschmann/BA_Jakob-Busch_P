"""Daten der Ansichten: Vergleich gegen den Kern (``array_equal``), Referenzfälle F2a–F2d (T2).

Keine neue Mathematik im Darstellungsmodul: Jede Kurve muss **bitgleich** der entsprechenden
Kerngröße entsprechen; unabhängig nachgerechnete Werte (Mittel, 3D) mit rtol 1e-12 (reine
float64-Arithmetik, Rundung der Summationsreihenfolge).
"""

from __future__ import annotations

import dar_daten as dd
import numpy as np
import pytest

from ldv_automation.auswertung import Auswertung, werte_aus
from ldv_automation.auswertung.daten import Messdaten
from ldv_automation.auswertung.mittel import (
    HINWEIS_MITTEL_3D,
    HINWEIS_MITTEL_3D_LEISTUNG,
    HINWEIS_MITTEL_KOHAERENT,
    HINWEIS_MITTEL_LEISTUNG,
    KENNZEICHEN_3D_MITTEL_UNGEPRUEFT,
    punktmittel_betrag,
)
from ldv_automation.auswertung.schwingform import waehle_linie
from ldv_automation.darstellung.auswahl import (
    BEZEICHNUNG_LEISTUNG,
    HINWEIS_PUNKTMENGE_3D,
    DarstellungsFehler,
    PaarCache,
    frf_daten,
    gesamtband,
    groessenname,
    kanalpaare,
    schwingform_daten,
    spektrum_daten,
    spitzen_daten_frf,
    spitzen_daten_spektrum,
    standard_bezug,
    verfuegbare_groessen,
    waehle_ebene,
)


@pytest.fixture(scope="module")
def daten() -> Messdaten:
    return dd.synthetische_messdaten()


@pytest.fixture(scope="module")
def kern(daten: Messdaten) -> Auswertung:
    return werte_aus(daten)


@pytest.fixture
def cache(daten: Messdaten) -> PaarCache:
    return PaarCache(daten)


# --- PaarCache --------------------------------------------------------------------------------


def test_paarcache_gleich_werte_aus(daten: Messdaten, kern: Auswertung, cache: PaarCache) -> None:
    for paar, soll in kern.paare.items():
        ist = cache.paar(*paar)
        np.testing.assert_array_equal(ist.frf.h1, soll.frf.h1)
        np.testing.assert_array_equal(ist.frf.h2, soll.frf.h2)
        np.testing.assert_array_equal(ist.frf.kohaerenz, soll.frf.kohaerenz)
        np.testing.assert_array_equal(ist.paar.cph, soll.paar.cph)
        np.testing.assert_array_equal(ist.mittel_h1.mittel_betrag, soll.mittel_h1.mittel_betrag)
        np.testing.assert_array_equal(
            ist.mittel_spektrum_leistung.mittel_quadratisch,
            soll.mittel_spektrum_leistung.mittel_quadratisch,
        )
        assert [s.f_sp_hz for s in ist.spitzen.spitzen] == [s.f_sp_hz for s in soll.spitzen.spitzen]


def test_paarcache_lru_haelt_nur_die_letzten_paare(daten: Messdaten) -> None:
    c = PaarCache(daten, groesse=2)
    c.paar("Vib X", "Ref1")
    c.paar("Vib Y", "Ref1")
    erstes = c.paar("Vib X", "Ref1")  # Treffer: Vib X wird jüngstes
    assert c.gespeichert() == (("Vib Y", "Ref1"), ("Vib X", "Ref1"))
    assert c.paar("Vib X", "Ref1") is erstes  # kein Neurechnen
    c.paar("Vib Z", "Ref1")  # verdrängt das älteste (Vib Y)
    assert c.gespeichert() == (("Vib X", "Ref1"), ("Vib Z", "Ref1"))


def test_paarcache_fehler(daten: Messdaten) -> None:
    with pytest.raises(ValueError, match="groesse"):
        PaarCache(daten, groesse=0)
    with pytest.raises(DarstellungsFehler, match="Kein Kreuzspektrum für Vib Z/Ref2"):
        PaarCache(daten).paar("Vib Z", "Ref2")


def test_kanalpaare_und_gesamtband(daten: Messdaten) -> None:
    assert kanalpaare(daten) == (("Vib X", "Ref1"), ("Vib Y", "Ref1"), ("Vib Z", "Ref1"))
    assert gesamtband(daten.frequenz_hz) == ((0.5, 32.0),)
    assert kanalpaare(dd.synthetische_messdaten(referenz=False)) == ()


# --- Ansicht 1 --------------------------------------------------------------------------------


def test_spektrum_mittel_kohaerent_ist_das_betragsmittel_des_kerns(
    daten: Messdaten, kern: Auswertung, cache: PaarCache
) -> None:
    sd = spektrum_daten(daten, cache, punkt=None, komponenten=("X", "Y", "Z"))
    assert sd.ist_mittel and sd.groesse == "kohaerent" and sd.referenz == "Ref1"
    for kurve in sd.kurven:
        soll = kern.paare[(f"Vib {kurve.schluessel}", "Ref1")].mittel_spektrum_kohaerent
        np.testing.assert_array_equal(kurve.y, soll.mittel_betrag)


def test_spektrum_mittel_leistung_ist_das_quadratische_mittel_und_nie_das_betragsmittel(
    daten: Messdaten, kern: Auswertung, cache: PaarCache
) -> None:
    sd = spektrum_daten(daten, cache, punkt=None, komponenten=("X", "Y", "Z"), groesse="leistung")
    for kurve in sd.kurven:
        soll = kern.paare[(f"Vib {kurve.schluessel}", "Ref1")].mittel_spektrum_leistung
        np.testing.assert_array_equal(kurve.y, soll.mittel_quadratisch)
        # RF-UI-F2d: das Betragsmittel von √AP wäre eine andere Kurve und wird nie gezeichnet
        assert soll.mittel_betrag is not None and soll.mittel_arithmetisch is None
        assert not np.array_equal(kurve.y, soll.mittel_betrag)
        # Das Quadratmittel von √AP ist √(Mittel AP): PSV AVGSEQ[AVG[AP]] (rtol: Rundung)
        mittel_ap = kern.mittel_ap[f"Vib {kurve.schluessel}"].mittel_arithmetisch
        assert mittel_ap is not None
        np.testing.assert_allclose(kurve.y**2, mittel_ap, rtol=1e-12)


def test_spektrum_punkt_ist_die_zeile_des_kerns(
    daten: Messdaten, kern: Auswertung, cache: PaarCache
) -> None:
    sd = spektrum_daten(daten, cache, punkt=2, komponenten=("X", "Z", "3D"))
    assert not sd.ist_mittel and sd.auswahl_text == "Punkt 102"
    assert [k.schluessel for k in sd.kurven] == ["X", "Z", "3D"]  # feste Reihenfolge
    np.testing.assert_array_equal(sd.kurven[0].y, np.abs(kern.paare[("Vib X", "Ref1")].paar.cph[2]))
    np.testing.assert_array_equal(sd.kurven[1].y, np.abs(kern.paare[("Vib Z", "Ref1")].paar.cph[2]))
    cph = [kern.paare[(f"Vib {c}", "Ref1")].paar.cph[2] for c in "XYZ"]
    np.testing.assert_allclose(
        sd.kurven[2].y, np.sqrt(sum(np.abs(c) ** 2 for c in cph)), rtol=1e-12
    )
    assert sd.kurven[2].beschriftung == "3D"  # nur das Mittel trägt das Kennzeichen
    assert sd.hinweise == ()


def test_spektrum_leistung_punkt_ist_wurzel_ap_und_3d_wurzel_summe(
    daten: Messdaten, cache: PaarCache
) -> None:
    sd = spektrum_daten(daten, cache, punkt=4, groesse="leistung")
    np.testing.assert_array_equal(sd.kurven[0].y, np.sqrt(daten.ap["Vib X"][4]))
    np.testing.assert_allclose(
        sd.kurven[3].y,
        np.sqrt(sum(daten.ap[f"Vib {c}"][4] for c in "XYZ")),
        rtol=1e-12,
    )
    assert sd.bezeichnung == BEZEICHNUNG_LEISTUNG == "Leistungsmittel √AP, mit Rauschen, ohne Phase"
    assert sd.referenz is None


def test_spektrum_bezeichnung_kohaerent_nennt_groesse_und_referenz(
    daten: Messdaten, cache: PaarCache
) -> None:
    sd = spektrum_daten(daten, cache, punkt=0)
    assert sd.bezeichnung == "Geschwindigkeit, kohärent mit Ref1"
    assert sd.einheit == "m/s"


def test_3d_mittel_ist_mittel_der_punktweisen_3d_betraege_mit_kennzeichen(
    daten: Messdaten, cache: PaarCache
) -> None:
    n = dd.P
    sd = spektrum_daten(daten, cache, punkt=None, komponenten=("3D",))
    cph = np.stack([cache.paar(f"Vib {c}", "Ref1").paar.cph for c in "XYZ"], axis=1)  # (P,3,K)
    punktweise = np.sqrt(np.sum(np.abs(cph) ** 2, axis=1))
    np.testing.assert_allclose(sd.kurven[0].y, punktweise.mean(axis=0), rtol=1e-12)
    assert sd.kurven[0].beschriftung == f"3D ({KENNZEICHEN_3D_MITTEL_UNGEPRUEFT})"
    assert HINWEIS_MITTEL_KOHAERENT.format(n=n) in sd.hinweise
    assert HINWEIS_MITTEL_3D.format(n=n) in sd.hinweise
    # nicht das 3D-Betrag der Komponentenmittel (FA-AUSW: unterscheidet sich)
    komp = np.stack(
        [spektrum_daten(daten, cache, punkt=None, komponenten=(c,)).kurven[0].y for c in "XYZ"]
    )
    assert not np.allclose(sd.kurven[0].y, np.sqrt(np.sum(komp**2, axis=0)), rtol=1e-3)


def test_3d_mittel_leistung_ist_wurzel_aus_summe_der_ap_mittel(
    daten: Messdaten, kern: Auswertung, cache: PaarCache
) -> None:
    sd = spektrum_daten(daten, cache, punkt=None, komponenten=("3D",), groesse="leistung")
    summe = np.zeros(dd.K)
    for c in "XYZ":
        m = kern.mittel_ap[f"Vib {c}"].mittel_arithmetisch
        assert m is not None
        summe += m
    soll = np.sqrt(summe)
    np.testing.assert_allclose(sd.kurven[0].y, soll, rtol=1e-12)
    assert HINWEIS_MITTEL_LEISTUNG.format(n=dd.P) in sd.hinweise
    # eigener Text zur gerechneten Formel (nicht der |CPH|-Text √(Σ|X_c|²)) und weiter ungeprüft
    assert HINWEIS_MITTEL_3D_LEISTUNG.format(n=dd.P) in sd.hinweise
    assert HINWEIS_MITTEL_3D.format(n=dd.P) not in sd.hinweise
    assert KENNZEICHEN_3D_MITTEL_UNGEPRUEFT in HINWEIS_MITTEL_3D_LEISTUNG
    assert "quadratisches Mittel" in HINWEIS_MITTEL_3D_LEISTUNG
    assert "√(Σ_c AP_c)" in HINWEIS_MITTEL_3D_LEISTUNG  # punktweiser 3D-Betrag
    assert "√(Σ_c Mittel AP_c)" in HINWEIS_MITTEL_3D_LEISTUNG  # = gerechnete Kurve (oben)
    # Der Text beschreibt genau diese Rechnung: quadratisches Mittel der punktweisen 3D-Beträge
    punktweise = np.sqrt(sum(daten.ap[f"Vib {c}"] for c in "XYZ"))  # (P, K)
    np.testing.assert_allclose(
        sd.kurven[0].y, np.sqrt(np.mean(punktweise**2, axis=0)), rtol=1e-12, atol=0.0
    )  # rtol: float64-Summe über P Punkte; kein Betragsmittel (das wäre kleiner)
    assert not np.allclose(sd.kurven[0].y, punktweise.mean(axis=0), rtol=1e-6)


def test_rf_ui_f2a_referenzwerte_der_mittel() -> None:
    """CPH = (3, 4i, -5), AP = (16, 25, 36): Betragsmittel 4, √AP-Mittel √(77/3).

    Exakt rechenbar; rtol 1e-12 (float64-Rundung der Summe).
    """
    k = 5
    f = 0.5 * np.arange(1, k + 1, dtype=np.float64)
    cph = np.array([3.0, 4.0j, -5.0])[:, None] * np.ones(k)
    ap_a = np.array([16.0, 25.0, 36.0])[:, None] * np.ones(k)
    md = dd.messdaten(
        frequenz_hz=f,
        ap={"Vib X": ap_a, "Vib Y": ap_a, "Vib Z": ap_a, "Ref1": np.ones((3, k))},
        cp={(f"Vib {c}", "Ref1"): cph.astype(np.complex128) for c in "XYZ"},
        delta_f_hz=0.5,
    )
    c = PaarCache(md)
    koh = spektrum_daten(md, c, punkt=None, komponenten=("Z",)).kurven[0].y
    lei = spektrum_daten(md, c, punkt=None, komponenten=("Z",), groesse="leistung").kurven[0].y
    np.testing.assert_allclose(koh, 4.0, rtol=1e-12)
    np.testing.assert_allclose(lei, np.sqrt(77.0 / 3.0), rtol=1e-12)
    assert lei[0] == pytest.approx(5.06623, abs=5e-6)
    # Betragsmittel von √AP (5,0) und quadratisches Mittel von |CPH| (4,0825): nicht gezeichnet
    assert not np.allclose(lei, 5.0, rtol=1e-3)
    assert not np.allclose(koh, 4.0825, rtol=1e-4)
    quadr = punktmittel_betrag(cph).mittel_quadratisch
    assert quadr is not None
    np.testing.assert_allclose(quadr, 4.0825, atol=5e-5)


def test_rf_ui_f2b_ohne_referenz_nur_leistung_mit_grund() -> None:
    md = dd.synthetische_messdaten(referenz=False)
    grund = verfuegbare_groessen(md)
    assert grund["leistung"] is None
    assert grund["kohaerent"] is not None and "Keine Referenz" in grund["kohaerent"]
    c = PaarCache(md)
    with pytest.raises(DarstellungsFehler, match="Keine Referenz"):
        spektrum_daten(md, c, punkt=None, groesse="kohaerent")
    sd = spektrum_daten(md, c, punkt=None, groesse="leistung")  # funktioniert ohne Referenz
    assert len(sd.kurven) == 4 and sd.referenz is None


def test_verfuegbare_groessen_mit_referenz_und_teilreferenz(daten: Messdaten) -> None:
    assert verfuegbare_groessen(daten) == {"kohaerent": None, "leistung": None}
    assert verfuegbare_groessen(daten, referenz="Ref1")["kohaerent"] is None
    grund = verfuegbare_groessen(daten, referenz="Ref2")["kohaerent"]
    assert grund is not None and "keinen Referenzkanal" in grund


def test_spektrum_fehler(daten: Messdaten, cache: PaarCache) -> None:
    with pytest.raises(DarstellungsFehler, match="Mindestens eine Komponente"):
        spektrum_daten(daten, cache, punkt=None, komponenten=())
    with pytest.raises(DarstellungsFehler, match="Unbekannte"):
        spektrum_daten(daten, cache, punkt=None, komponenten=("W",))
    with pytest.raises(DarstellungsFehler, match="Punkt 99 existiert nicht"):
        spektrum_daten(daten, cache, punkt=99)
    with pytest.raises(DarstellungsFehler, match="Punkt -1"):
        spektrum_daten(daten, cache, punkt=-1)


def test_groessenname() -> None:
    assert [groessenname(e) for e in ("m/s", "m", "m/s²", "N")] == [
        "Geschwindigkeit",
        "Weg",
        "Beschleunigung",
        "Größe",
    ]


def test_frequenzachse_ist_die_der_datei_nicht_aus_bandbreite_und_linien_gebildet() -> None:
    """U-4: künstliche Achse Δf = 0,3125 Hz (statt 0,5 Hz) bleibt unverändert."""
    md = dd.synthetische_messdaten()
    achse = 0.3125 * np.arange(1, dd.K + 1, dtype=np.float64)
    md2 = Messdaten(
        frequenz_hz=achse,
        delta_f_hz=0.3125,
        punkte=md.punkte,
        einheiten=md.einheiten,
        ap=md.ap,
        cp=md.cp,
        phase_gueltig=True,
    )
    c = PaarCache(md2)
    assert spektrum_daten(md2, c, punkt=0).frequenz_hz is achse
    assert frf_daten(c, "Vib Z", "Ref1", punkt=0).frequenz_hz is achse
    assert spitzen_daten_frf(c, "Vib Z", "Ref1").frequenz_hz is achse
    assert schwingform_daten(md2, c, 1.0, komponente="Z").f_hz == achse[waehle_linie(achse, 1.0)]


# --- Ansicht 2 und 3 --------------------------------------------------------------------------


def test_frf_daten_mittel_und_punkt(daten: Messdaten, kern: Auswertung, cache: PaarCache) -> None:
    soll = kern.paare[("Vib Z", "Ref1")]
    m = frf_daten(cache, "Vib Z", "Ref1", punkt=None)
    np.testing.assert_array_equal(m.betrag_h1, soll.mittel_h1.mittel_betrag)
    np.testing.assert_array_equal(m.betrag_h2, soll.mittel_h2.mittel_betrag)
    np.testing.assert_array_equal(m.kohaerenz, soll.mittel_kohaerenz.mittel_arithmetisch)
    assert m.phase_rad is None and m.ist_mittel and m.einheit == "(m/s)/N"
    p = frf_daten(cache, "Vib Z", "Ref1", punkt=3)
    np.testing.assert_array_equal(p.betrag_h1, np.abs(soll.frf.h1[3]))
    np.testing.assert_array_equal(p.betrag_h2, np.abs(soll.frf.h2[3]))
    np.testing.assert_array_equal(p.kohaerenz, soll.frf.kohaerenz[3])
    np.testing.assert_array_equal(p.phase_rad, np.angle(soll.frf.h1[3]))
    assert p.auswahl_text == "Punkt 103" and p.kohaerenz_min == 0.9
    assert p.bezeichnung_h1 == soll.frf.bezeichnung_h1
    with pytest.raises(DarstellungsFehler, match="Punkt 6"):
        frf_daten(cache, "Vib Z", "Ref1", punkt=6)


def test_spitzen_daten_frf(daten: Messdaten, kern: Auswertung, cache: PaarCache) -> None:
    soll = kern.paare[("Vib Z", "Ref1")]
    sd = spitzen_daten_frf(cache, "Vib Z", "Ref1", baender=[(1.0, 5.0)], gewaehlt=0)
    assert sd.spitzen == soll.spitzen.spitzen and len(sd.spitzen) >= 2
    np.testing.assert_array_equal(sd.y, soll.mittel_h1.mittel_betrag)
    assert sd.baender == ((1.0, 5.0),) and sd.gewaehlt == 0 and sd.groesse == "Betrag"
    assert sd.beschriftung.endswith("Vib Z/Ref1") and sd.hinweis == ""
    with pytest.raises(DarstellungsFehler, match="Spitze 99"):
        spitzen_daten_frf(cache, "Vib Z", "Ref1", gewaehlt=99)


def test_spitzen_daten_spektrum_ohne_referenz() -> None:
    md = dd.synthetische_messdaten(referenz=False)
    c = PaarCache(md)
    sd = spitzen_daten_spektrum(md, c, "Vib Z", baender=[(1.0, 2.0)])
    assert sd.spitzen == () and sd.hinweis == "Keine Spitzensuche: Referenzkanal fehlt."
    assert sd.groesse == "Amplitude" and sd.einheit == "m/s"
    ap = punktmittel_betrag(np.sqrt(md.ap["Vib Z"])).mittel_quadratisch
    assert ap is not None
    np.testing.assert_allclose(sd.y, ap, rtol=1e-12)
    with pytest.raises(DarstellungsFehler, match="fehlt"):
        spitzen_daten_spektrum(md, c, "Vib Q")


# --- Ansicht 4 --------------------------------------------------------------------------------


@pytest.mark.parametrize(
    ("ausdehnung", "ebene"),
    [
        ((0.196, 0.484, 0.017), "xy"),  # Beispieldatei
        ((1.0, 1.0, 1.0), "xy"),  # Gleichstand: xy vor xz vor yz
        ((0.1, 0.5, 0.5), "yz"),  # x entfällt
        ((0.5, 0.1, 0.5), "xz"),  # y entfällt
        ((0.5, 0.5, 0.1), "xy"),  # z entfällt
        ((0.2, 0.2, 0.5), "xz"),  # x und y gleich klein: y entfällt vor x (xz vor yz)
        ((0.5, 0.2, 0.2), "xy"),  # y und z gleich klein: z entfällt zuerst (xy)
        ((0.2, 0.5, 0.2), "xy"),  # x und z gleich klein: xy
        ((0.2, 0.2 + 1e-12, 0.5), "xz"),  # Gleichstand mit Rundungsrest
    ],
)
def test_waehle_ebene(ausdehnung: tuple[float, float, float], ebene: str) -> None:
    koord = np.array([[0.0, 0.0, 0.0], list(ausdehnung)])
    assert waehle_ebene(koord) == ebene


def test_waehle_ebene_prueft_form() -> None:
    with pytest.raises(ValueError, match="koordinaten_m"):
        waehle_ebene(np.zeros((3, 2)))


def test_schwingform_daten_gegen_kern(daten: Messdaten, cache: PaarCache) -> None:
    from ldv_automation.auswertung.gesamt import schwingform_aus

    sd = schwingform_daten(daten, cache, 10.2, komponente="Z")
    soll = schwingform_aus(daten, 10.2)
    assert sd.linie == soll.linie and sd.f_hz == soll.f_hz == 10.0 and sd.f_wahl_hz == 10.2
    np.testing.assert_array_equal(sd.betrag, soll.betrag[:, 2])
    assert soll.amplitude is not None
    np.testing.assert_array_equal(sd.amplitude, soll.amplitude[:, 2])
    assert sd.ebene == "xy" and sd.phase_gueltig and sd.referenz == "Ref1" and sd.einheit == "m/s"
    paar = cache.paar("Vib Z", "Ref1")
    np.testing.assert_array_equal(sd.kohaerenz, paar.frf.kohaerenz[:, soll.linie])
    np.testing.assert_array_equal(sd.kohaerenz_ok, paar.frf.kohaerenz_ok[:, soll.linie])
    assert sd.kohaerenz_min == 0.9
    x = schwingform_daten(daten, cache, 10.2, komponente="X")
    np.testing.assert_array_equal(x.betrag, soll.betrag[:, 0])
    d3 = schwingform_daten(daten, cache, 10.2, komponente="3D")
    np.testing.assert_array_equal(d3.betrag, soll.betrag_3d_psv)
    assert d3.amplitude is None and d3.kohaerenz is None and standard_bezug(d3) is None


def test_schwingform_daten_ohne_referenz_nur_betrag() -> None:
    md = dd.synthetische_messdaten(referenz=False)
    c = PaarCache(md)
    sd = schwingform_daten(md, c, 10.0, komponente="Z")
    assert not sd.phase_gueltig and sd.amplitude is None and sd.quelle == "leistung"
    np.testing.assert_allclose(sd.betrag, np.sqrt(md.ap["Vib Z"][:, 19]), rtol=0)
    assert standard_bezug(sd) is None and sd.hinweise


def test_schwingform_daten_fehler(daten: Messdaten, cache: PaarCache) -> None:
    with pytest.raises(DarstellungsFehler, match="Unbekannte Komponente"):
        schwingform_daten(daten, cache, 10.0, komponente="Q")
    with pytest.raises(DarstellungsFehler, match="außerhalb"):
        schwingform_daten(daten, cache, 1200.0, komponente="Z")


def test_standard_bezug_groesster_betrag_unter_kohaerenten(
    daten: Messdaten, cache: PaarCache
) -> None:
    sd = schwingform_daten(daten, cache, 10.0, komponente="Z")
    assert sd.kohaerenz_ok is not None and sd.amplitude is not None
    assert standard_bezug(sd) == int(np.argmax(np.abs(sd.amplitude)))  # alle γ² ≥ γ²_min
    # Die Punkte 0 und 4 haben denselben Betrag (Formfaktor ±1); ist Punkt 0 unzuverlässig,
    # wird der kohärente Punkt 4 Bezugspunkt, obwohl Punkt 0 beim Betrag zuerst steht.
    schlecht = dd.synthetische_messdaten(
        n_vib_je_punkt=np.array([1.0, 1e-12, 1e-12, 1e-12, 1e-12, 1e-12])
    )
    sd2 = schwingform_daten(schlecht, PaarCache(schlecht), 10.0, komponente="Z")
    assert sd2.kohaerenz_ok is not None and sd2.amplitude is not None
    assert not sd2.kohaerenz_ok[0] and sd2.kohaerenz_ok[1:].all()
    assert np.isclose(abs(sd2.amplitude[0]), abs(sd2.amplitude[4]), rtol=1e-12)
    assert standard_bezug(sd2) == 4


# --- K-AUSW-T2c: gemeinsame Punktmenge von 3D- und Komponentenmittel, Punktzahl im Bild --------


def _mit_nan_in_x(punkt: int = 2) -> Messdaten:
    """Datei, in der Vib X an einem Punkt NaN trägt (Fall aus dem Review: AP_X = NaN)."""
    import dataclasses

    md = dd.synthetische_messdaten()
    ap = {k: v.copy() for k, v in md.ap.items()}
    cp = {k: v.copy() for k, v in md.cp.items()}
    ap["Vib X"][punkt, :] = np.nan
    cp[("Vib X", "Ref1")][punkt, :] = np.nan
    return dataclasses.replace(md, ap=ap, cp=cp)


def test_leistungsmittel_3d_und_komponenten_nutzen_dieselbe_punktmenge() -> None:
    md = _mit_nan_in_x()
    sd = spektrum_daten(md, PaarCache(md), punkt=None, groesse="leistung")
    y = {k.schluessel: k.y for k in sd.kurven}
    # 3D = √(Σ_c Mittel AP_c) gilt nur bei gleicher Punktmenge (Hinweistext des Kerns)
    np.testing.assert_allclose(y["3D"] ** 2, y["X"] ** 2 + y["Y"] ** 2 + y["Z"] ** 2, rtol=1e-12)
    # unabhängig nachgerechnet über die fünf Punkte ohne Punkt 2
    rest = [0, 1, 3, 4, 5]
    for c in ("X", "Y", "Z"):
        erwartet = np.sqrt(np.mean(md.ap[f"Vib {c}"][rest], axis=0))
        np.testing.assert_allclose(y[c], erwartet, rtol=1e-12)
    assert "über 5 Punkte" in sd.mittelformel and sd.mittelformel.startswith("Leistungsmittel √AP")
    assert all("über 5 Punkte" in h for h in sd.hinweise if h != HINWEIS_PUNKTMENGE_3D)
    assert (
        HINWEIS_PUNKTMENGE_3D == "3D-Mittel: je Linie nur Punkte mit endlichen Werten in X, Y und Z"
    )
    assert HINWEIS_PUNKTMENGE_3D in sd.hinweise  # die Regel steht im Hinweistext


def test_ohne_3d_nutzt_jede_komponente_ihre_eigene_punktmenge() -> None:
    md = _mit_nan_in_x(2)
    import dataclasses

    ap = {k: v.copy() for k, v in md.ap.items()}
    ap["Vib Y"][4, :] = np.nan  # zusätzlich NaN in Y an einem anderen Punkt
    md = dataclasses.replace(md, ap=ap)
    cache = PaarCache(md)
    nur_x = spektrum_daten(md, cache, punkt=None, groesse="leistung", komponenten=("X",))
    x_y = spektrum_daten(md, cache, punkt=None, groesse="leistung", komponenten=("X", "Y"))
    kx = {k.schluessel: k.y for k in nur_x.kurven}["X"]
    kxy = {k.schluessel: k.y for k in x_y.kurven}
    np.testing.assert_array_equal(kx, kxy["X"])  # X unabhängig von der Wahl von Y
    rest_x = [0, 1, 3, 4, 5]  # X: nur Punkt 2 ist NaN, Punkt 4 zählt (NaN in Y ist irrelevant)
    np.testing.assert_allclose(kx, np.sqrt(np.mean(md.ap["Vib X"][rest_x], axis=0)), rtol=1e-12)
    rest_y = [0, 1, 2, 3, 5]
    np.testing.assert_allclose(
        kxy["Y"], np.sqrt(np.mean(md.ap["Vib Y"][rest_y], axis=0)), rtol=1e-12
    )
    assert HINWEIS_PUNKTMENGE_3D not in x_y.hinweise
    # mit 3D gilt dagegen die gemeinsame Punktmenge (ohne Punkte 2 und 4)
    mit = spektrum_daten(md, cache, punkt=None, groesse="leistung", komponenten=("X", "3D"))
    kx3 = {k.schluessel: k.y for k in mit.kurven}["X"]
    np.testing.assert_allclose(
        kx3, np.sqrt(np.mean(md.ap["Vib X"][[0, 1, 3, 5]], axis=0)), rtol=1e-12
    )


def test_kohaerentes_3d_mittel_nutzt_dieselbe_punktmenge_wie_die_komponenten() -> None:
    md = _mit_nan_in_x()
    cache = PaarCache(md)
    sd = spektrum_daten(md, cache, punkt=None)
    y = {k.schluessel: k.y for k in sd.kurven}
    rest = [0, 1, 3, 4, 5]
    cph = {c: cache.paar(f"Vib {c}", "Ref1").paar.cph for c in ("X", "Y", "Z")}
    for c in ("X", "Y", "Z"):
        np.testing.assert_allclose(y[c], np.mean(np.abs(cph[c][rest]), axis=0), rtol=1e-12)
    drei_d = np.sqrt(sum(np.abs(cph[c][rest]) ** 2 for c in ("X", "Y", "Z")))
    np.testing.assert_allclose(y["3D"], np.mean(drei_d, axis=0), rtol=1e-12)
    assert sd.mittelformel == "Betragsmittel |CPH| über 5 Punkte"
    # ohne NaN bleibt alles beim Alten: alle Punkte, bitgleich zum Kern
    md0 = dd.synthetische_messdaten()
    ok = spektrum_daten(md0, PaarCache(md0), punkt=None)
    assert ok.mittelformel == f"Betragsmittel |CPH| über {dd.P} Punkte"
    assert spektrum_daten(md0, PaarCache(md0), punkt=1).mittelformel == ""


def test_punktzahl_in_den_beschriftungen_von_ansicht_2_und_3(daten: Messdaten) -> None:
    cache = PaarCache(daten)
    assert frf_daten(cache, "Vib Z", "Ref1", punkt=None).punktzahl == dd.P
    assert frf_daten(cache, "Vib Z", "Ref1", punkt=1).punktzahl is None
    sp = spitzen_daten_frf(cache, "Vib Z", "Ref1")
    assert sp.punktzahl == dd.P
    assert sp.beschriftung == f"Betragsmittel |H1| über {dd.P} Punkte, Vib Z/Ref1"
    ohne = dd.synthetische_messdaten(referenz=False)
    sl = spitzen_daten_spektrum(ohne, PaarCache(ohne), "Vib Z")
    assert sl.beschriftung.startswith(f"Leistungsmittel √AP über {dd.P} Punkte, Vib Z")
