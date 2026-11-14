"""Ansicht 5 „Diagramm“ (R-058/R-059, P-AUSW2 S6; UI-10, 11, 13, 15, 16, 18, 20, 21).

Geprüft wird die Figure-Struktur (Linienzahl, Linienarten, Achsen, Legendentext), nicht Pixel.
Referenz der Auflösung: dieselben Kurven wie ``spektrum_daten`` und ``frf_daten`` (``array_equal``,
es gibt keine neue Mathematik).
"""

from __future__ import annotations

import subprocess
import sys

import dar_daten as dd
import numpy as np
import pytest
from matplotlib.figure import Figure

from ldv_automation.auswertung.daten import Messdaten
from ldv_automation.darstellung import Ansicht
from ldv_automation.darstellung.achsen import AchsenFehler, AchsenOptionen, Bereich
from ldv_automation.darstellung.auswahl import (
    DarstellungsFehler,
    PaarCache,
    frf_daten,
    spektrum_daten,
)
from ldv_automation.darstellung.diagramm import (
    PLATZHALTER_KEINE_SERIE,
    TEILBILDER_MAX,
    DiagrammOptionen,
    teilbilder,
    zeichne_diagramm,
)
from ldv_automation.darstellung.serien_daten import (
    GRUND_ANDERE_EINHEIT,
    GRUND_ANDERE_GROESSE,
    GRUND_PHASE_MITTEL,
    DiagrammDaten,
    GroessenId,
    MessungsZugriff,
    SerienSpec,
    loese_alle_auf,
    loese_serie_auf,
    verfuegbare_diagramm_groessen,
)
from ldv_automation.darstellung.stil import THESIS_STIL

PAAR = ("Vib X", "Ref1")
K2 = 32
DF2_HZ = 1.0


def messdaten_zwei() -> Messdaten:
    """Zweite Messung: 32 Linien, Δf 1 Hz, nur 4 Punkte (Labels 100 … 103)."""
    f = DF2_HZ * np.arange(1, K2 + 1, dtype=np.float64)
    h0 = dd.mobilitaet_moden(f, [8.0, 18.0], zeta=0.03)
    p = 4
    ap: dict[str, np.ndarray] = {}
    cp: dict[tuple[str, str], np.ndarray] = {}
    for kanal, form in dd.FORM_JE_KANAL.items():
        h = form[:p, None] * h0[None, :]
        ap[kanal] = (np.abs(h) ** 2 * dd.S_X + dd.N_VIB).astype(np.float64)
        cp[(kanal, "Ref1")] = (h * dd.S_X).astype(np.complex128)
    ap["Ref1"] = np.full((p, K2), dd.S_X + dd.N_REF)
    return dd.messdaten(frequenz_hz=f, ap=ap, cp=cp, delta_f_hz=DF2_HZ)


@pytest.fixture(scope="module")
def messungen() -> dict[int, tuple[Messdaten, PaarCache, str, str]]:
    a, b = dd.synthetische_messdaten(), messdaten_zwei()
    return {
        1: (a, PaarCache(a), "A", "a.svd"),
        2: (b, PaarCache(b), "B", "b.svd"),
    }


@pytest.fixture(scope="module")
def zugriff(messungen: dict[int, tuple[Messdaten, PaarCache, str, str]]) -> MessungsZugriff:
    return messungen.get


def h1(messung: int, punkt: int | None, slot: int = 0, **kw: object) -> SerienSpec:
    return SerienSpec(messung, punkt, "h1", kanalpaar=PAAR, slot=slot, **kw)  # type: ignore[arg-type]


def zeichne(daten: DiagrammDaten, **opt: object) -> tuple[Figure, object]:
    fig = Figure(figsize=(8.0, 5.0), dpi=100)
    z = zeichne_diagramm(fig, daten, DiagrammOptionen(**opt), THESIS_STIL)  # type: ignore[arg-type]
    return fig, z


# --- Auflösung (keine neue Mathematik) ---------------------------------------------------------


def test_aufloesung_stimmt_bitgleich_mit_den_kernfunktionen(zugriff: MessungsZugriff) -> None:
    daten, cache, kurz, datei = zugriff(1)  # type: ignore[misc]
    punkt_idx = 2
    label = int(daten.punkte.label[punkt_idx])
    sp = loese_serie_auf(
        SerienSpec(1, label, "spektrum", komponente="Z", teilgroesse="kohaerent"),
        daten,
        cache,
        kurz,
        datei,
    )
    ref = spektrum_daten(daten, cache, punkt=punkt_idx, komponenten=("Z",), groesse="kohaerent")
    assert np.array_equal(sp.y, ref.kurven[0].y) and np.array_equal(
        sp.frequenz_hz, daten.frequenz_hz
    )
    assert sp.einheit == "m/s" and sp.punkt_text == f"Punkt {label}"
    f = frf_daten(cache, *PAAR, punkt=None)
    for groesse, erwartet in (("h1", f.betrag_h1), ("h2", f.betrag_h2), ("kohaerenz", f.kohaerenz)):
        s = loese_serie_auf(
            SerienSpec(1, None, groesse, kanalpaar=PAAR),  # type: ignore[arg-type]
            daten,
            cache,
            kurz,
        )
        assert np.array_equal(s.y, erwartet), groesse
    h = loese_serie_auf(h1(1, None), daten, cache, kurz)
    assert h.punkt_text == "Mittel" and h.punktzahl_text == f.punktzahl_text != ""
    assert h.mittelformel == f"Betragsmittel |H1| über {f.punktzahl_text} Punkte"  # aus den Daten
    assert h.legende == f"A · Mittel · Vib X / Ref1\n{h.mittelformel}"  # UI-11
    assert h.einheit == f.einheit


def test_phase_in_grad_wie_ansicht_2_und_beim_mittel_nicht_darstellbar(
    zugriff: MessungsZugriff,
) -> None:
    daten, cache, kurz, _ = zugriff(1)  # type: ignore[misc]
    label = int(daten.punkte.label[0])
    s = loese_serie_auf(SerienSpec(1, label, "phase", kanalpaar=PAAR), daten, cache, kurz)
    phase_rad = frf_daten(cache, *PAAR, punkt=0).phase_rad
    assert phase_rad is not None
    ref = np.degrees(phase_rad)
    gueltig = np.isfinite(s.y)
    assert np.allclose(s.y[gueltig], ref[gueltig], rtol=1e-12, atol=0.0)  # Umbrüche sind NaN
    assert s.einheit == "°" and s.phase_unbestaetigt and np.nanmax(np.abs(s.y)) <= 180.0
    with pytest.raises(DarstellungsFehler, match="Phase beim Mittel"):
        loese_serie_auf(SerienSpec(1, None, "phase", kanalpaar=PAAR), daten, cache, kurz)


def test_unbekanntes_label_und_fehlende_angaben_sind_darstellungsfehler(
    zugriff: MessungsZugriff,
) -> None:
    daten, cache, kurz, _ = zugriff(2)  # type: ignore[misc]
    with pytest.raises(DarstellungsFehler, match="Punkt 105 gibt es in Messung B nicht"):
        loese_serie_auf(h1(2, 105), daten, cache, kurz)
    with pytest.raises(DarstellungsFehler, match="Komponente"):
        loese_serie_auf(SerienSpec(2, None, "spektrum"), daten, cache, kurz)
    with pytest.raises(DarstellungsFehler, match="Kanalpaar"):
        loese_serie_auf(SerienSpec(2, None, "h1"), daten, cache, kurz)


def test_ohne_referenz_sind_nur_spektrum_und_leistung_moeglich() -> None:
    ohne = dd.synthetische_messdaten(referenz=False)
    g = verfuegbare_diagramm_groessen(ohne)
    assert g["spektrum"] is None
    assert all(g[k] and "Referenz" in str(g[k]) for k in ("h1", "h2", "kohaerenz", "phase"))
    cache = PaarCache(ohne)
    s = loese_serie_auf(
        SerienSpec(1, None, "spektrum", komponente="X", teilgroesse="leistung"), ohne, cache, "A"
    )
    assert s.mittelformel.startswith("Leistungsmittel √AP über")
    with pytest.raises(DarstellungsFehler):  # |CPH| ohne Referenz
        loese_serie_auf(
            SerienSpec(1, None, "spektrum", komponente="X", teilgroesse="kohaerent"),
            ohne,
            cache,
            "A",
        )
    ungueltig = dd.synthetische_messdaten()
    from dataclasses import replace

    assert "nicht gültig" in str(
        verfuegbare_diagramm_groessen(replace(ungueltig, phase_gueltig=False))["phase"]
    )


def test_nicht_darstellbare_serien_werden_mit_grund_gemeldet(zugriff: MessungsZugriff) -> None:
    daten = loese_alle_auf(
        [
            h1(1, None, 0),
            h1(3, None, 1),  # Messung gibt es nicht
            SerienSpec(2, None, "phase", kanalpaar=PAAR, slot=2),  # Mittel: keine Phase
            h1(2, 999, 3),  # Label fehlt (UI-12)
        ],
        zugriff,
        anordnung="nebeneinander",
    )
    assert [s.slot for s in daten.serien] == [0]
    gruende = {spec.slot: text for spec, text in daten.nicht_darstellbar}
    assert "nicht mehr geöffnet" in gruende[1]
    assert gruende[2] == GRUND_PHASE_MITTEL and "Punkt 999" in gruende[3]


def test_ueberlagert_nur_eine_groesse_und_eine_einheit(zugriff: MessungsZugriff) -> None:
    daten = loese_alle_auf(
        [h1(1, None, 0), SerienSpec(2, None, "kohaerenz", kanalpaar=PAAR, slot=1)],
        zugriff,
        anordnung="ueberlagert",
    )
    assert len(daten.serien) == 1
    assert daten.nicht_darstellbar[0][1] == GRUND_ANDERE_GROESSE
    nebeneinander = loese_alle_auf(
        [h1(1, None, 0), SerienSpec(2, None, "kohaerenz", kanalpaar=PAAR, slot=1)],
        zugriff,
        anordnung="nebeneinander",
    )
    assert len(nebeneinander.serien) == 2 and not nebeneinander.nicht_darstellbar
    # gleiche Größe, andere Einheit
    a = loese_alle_auf([h1(1, None, 0), h1(2, None, 1)], zugriff).serien
    b = loese_alle_auf(
        [h1(1, None, 0), h1(2, None, 1)],
        lambda i: _mit_einheit(zugriff(i), i),
    )
    assert len(a) == 2 and len(b.serien) == 1
    assert b.nicht_darstellbar[0][1] == GRUND_ANDERE_EINHEIT.format(
        einheit="(m/s²)/N", erste="(m/s)/N"
    )


def _mit_einheit(
    t: tuple[Messdaten, PaarCache, str, str] | None, i: int
) -> tuple[Messdaten, PaarCache, str, str] | None:
    """Messung 2 mit Beschleunigung als Antwortgröße (Einheit der FRF ändert sich)."""
    assert t is not None
    if i == 1:
        return t
    from dataclasses import replace

    daten = replace(t[0], einheiten={**t[0].einheiten, "Vib X": "m/s²"})
    return daten, PaarCache(daten), t[2], t[3]


def test_bereits_aufgeloeste_serie_wird_wiederverwendet(zugriff: MessungsZugriff) -> None:
    erste = loese_alle_auf([h1(1, None, 0)], zugriff).serien[0]
    neu_spec = h1(1, None, 2, sichtbar=False)  # nur Slot und Sichtbarkeit anders
    daten = loese_alle_auf([neu_spec], zugriff, bereits={neu_spec.aufloesung_schluessel(): erste})
    s = daten.serien[0]
    assert s.y is erste.y and s.slot == 2 and not s.sichtbar


def messdaten_ref2() -> Messdaten:
    """Messung wie A, zusätzlich mit Ref2 (Beschleunigung, m/s²): |H1| hat dann (m/s)/(m/s²)."""
    a = dd.synthetische_messdaten()
    cp = {**a.cp, **{(k, "Ref2"): v.copy() for (k, r), v in a.cp.items() if r == "Ref1"}}
    ap = {**a.ap, "Ref2": a.ap["Ref1"].copy()}
    from dataclasses import replace

    return replace(a, cp=cp, ap=ap, einheiten={**a.einheiten, "Ref2": "m/s²"})


@pytest.fixture(scope="module")
def zugriff_ref() -> MessungsZugriff:
    """Messung 1 mit Ref1 und Ref2, Messung 2 (B) nur mit Ref2."""
    a = messdaten_ref2()
    b = messdaten_ref2()
    t = {1: (a, PaarCache(a), "A", "a.svd"), 2: (b, PaarCache(b), "B", "b.svd")}
    return t.get


PAAR1 = ("Vib Z", "Ref1")
PAAR2 = ("Vib Z", "Ref2")
EINHEIT1 = "(m/s)/N"
EINHEIT2 = "(m/s)/(m/s²)"


def h1p(messung: int, paar: tuple[str, str], slot: int, **kw: object) -> SerienSpec:
    return SerienSpec(messung, None, "h1", kanalpaar=paar, slot=slot, **kw)  # type: ignore[arg-type]


@pytest.mark.parametrize("anordnung", ["ueberlagert", "nebeneinander"])
def test_einheit_gilt_je_teilbild_in_jeder_anordnung(
    zugriff_ref: MessungsZugriff, anordnung: str
) -> None:
    """A-3 (Review-Blocker): Ref1 und Ref2 derselben Messung teilen kein Teilbild."""
    daten = loese_alle_auf(
        [h1p(1, PAAR1, 0), h1p(1, PAAR2, 1), h1p(2, PAAR2, 2)],
        zugriff_ref,
        anordnung=anordnung,  # type: ignore[arg-type]
    )
    grund = GRUND_ANDERE_EINHEIT.format(einheit=EINHEIT2, erste=EINHEIT1)
    assert [(s.spec.messung_id, s.einheit) for s in daten.serien] == (
        [(1, EINHEIT1)]
        if anordnung == "ueberlagert"
        else [(1, EINHEIT1), (2, EINHEIT2)]  # B ist ein eigenes Teilbild: andere Messung
    )
    erwartet = [(1, 1)] if anordnung == "nebeneinander" else [(1, 1), (2, 2)]
    assert [(spec.messung_id, spec.slot) for spec, _ in daten.nicht_darstellbar] == erwartet
    assert all(text == grund for _, text in daten.nicht_darstellbar if _.slot == 1)


def test_nebeneinander_y_nur_bei_gleicher_groesse_und_einheit_gekoppelt(
    zugriff_ref: MessungsZugriff,
) -> None:
    daten = loese_alle_auf(
        [h1p(1, PAAR1, 0), h1p(2, PAAR2, 1)], zugriff_ref, anordnung="nebeneinander"
    )
    assert not daten.nicht_darstellbar  # je ein Teilbild, je eine Einheit
    _, z = zeichne(daten, anordnung="nebeneinander")
    a, b = z.achsen  # type: ignore[attr-defined]
    assert a.get_ylabel() == f"|H1| [{EINHEIT1}]" and b.get_ylabel() == f"|H1| [{EINHEIT2}]"
    assert a.get_shared_x_axes().joined(a, b)
    assert not a.get_shared_y_axes().joined(a, b)  # gleiche Größe, andere Einheit
    gleich = loese_alle_auf(
        [h1p(1, PAAR2, 0), h1p(2, PAAR2, 1)], zugriff_ref, anordnung="nebeneinander"
    )
    _, z2 = zeichne(gleich, anordnung="nebeneinander")
    c, d = z2.achsen  # type: ignore[attr-defined]
    assert c.get_shared_y_axes().joined(c, d)  # gleiche Größe und Einheit: gekoppelt


def test_referenz_ist_die_erste_sichtbare_serie(zugriff_ref: MessungsZugriff) -> None:
    """Die erste Serie ist unsichtbar: die sichtbare zweite bestimmt die Einheit (Plan A-3)."""
    daten = loese_alle_auf(
        [h1p(1, PAAR1, 0, sichtbar=False), h1p(1, PAAR2, 1), h1p(2, PAAR2, 2)],
        zugriff_ref,
        anordnung="ueberlagert",
    )
    assert [s.slot for s in daten.serien] == [1, 2]
    assert [(spec.slot, text) for spec, text in daten.nicht_darstellbar] == [
        (0, GRUND_ANDERE_EINHEIT.format(einheit=EINHEIT1, erste=EINHEIT2))
    ]
    _, z = zeichne(daten)
    assert z.achsen[0].get_ylabel() == f"|H1| [{EINHEIT2}]"  # type: ignore[attr-defined]
    # nebeneinander: dasselbe je Teilbild (Messung A mit unsichtbarer Ref1-Serie)
    neben = loese_alle_auf(
        [h1p(1, PAAR1, 0, sichtbar=False), h1p(1, PAAR2, 1)], zugriff_ref, anordnung="nebeneinander"
    )
    assert [s.slot for s in neben.serien] == [1]
    assert [spec.slot for spec, _ in neben.nicht_darstellbar] == [0]


def test_nebeneinander_bereich_und_skala_je_groesse(zugriff: MessungsZugriff) -> None:
    """E11: Spektrum und |H1| bekommen je ihren Bereich und ihre Skala."""
    daten = loese_alle_auf(
        [SerienSpec(1, None, "spektrum", komponente="X", slot=0), h1(1, None, 1)],
        zugriff,
        anordnung="nebeneinander",
    )
    achsen = AchsenOptionen(y={"spektrum": Bereich(1e-4, 1e-1), "h1": Bereich(2.0, 5.0)})
    _, z = zeichne(
        daten,
        anordnung="nebeneinander",
        achsen=achsen,
        skalen={"spektrum": "log", "h1": "linear"},
    )
    a_sp, a_h1 = z.achsen  # type: ignore[attr-defined]
    assert z.rollen == ("spektrum", "h1")  # type: ignore[attr-defined]
    assert a_sp.get_ylim() == pytest.approx((1e-4, 1e-1), rel=1e-9)
    assert a_h1.get_ylim() == pytest.approx((2.0, 5.0), rel=1e-9)
    assert a_sp.get_yscale() == "log" and a_h1.get_yscale() == "linear"
    with pytest.raises(ValueError, match="Skala"):
        DiagrammOptionen(skalen={"h1": "db"})  # type: ignore[dict-item]


# --- Zeichnen ------------------------------------------------------------------------------------


def test_ueberlagert_zwei_messungen_eigene_frequenzachse_und_legende(
    zugriff: MessungsZugriff,
) -> None:
    daten = loese_alle_auf([h1(1, 100, 0), h1(2, 100, 1)], zugriff)
    fig, z = zeichne(daten)
    achse = z.achsen[0]  # type: ignore[attr-defined]
    assert len(z.achsen) == 1 and len(achse.get_lines()) == 2  # type: ignore[attr-defined]
    l1, l2 = achse.get_lines()
    assert len(l1.get_xdata()) == dd.K and len(l2.get_xdata()) == K2  # UI-13, keine Interpolation
    assert np.array_equal(l1.get_xdata(), dd.FREQUENZ_HZ)
    assert l1.get_linestyle() != l2.get_linestyle()  # UI-10: paarweise verschieden
    assert z.hilfsobjekte["legende_eintraege"] == [  # type: ignore[attr-defined]
        "A · Punkt 100 · Vib X / Ref1",
        "B · Punkt 100 · Vib X / Ref1",
    ]
    legende_texte = [t.get_text() for t in z.hilfsobjekte["legende"].get_texts()]  # type: ignore[attr-defined]
    assert legende_texte == z.hilfsobjekte["legende_eintraege"]  # type: ignore[attr-defined]
    assert achse.get_ylabel() == "|H1| [(m/s)/N]" and achse.get_xlabel() == "Frequenz [Hz]"
    assert fig.get_suptitle() == "" and achse.get_title() == ""  # kein Diagrammtitel
    assert achse.get_xlim() == (0.5, dd.FREQUENZ_HZ[-1])  # Vereinigung beider Achsen
    assert z.rollen == ("h1",)  # type: ignore[attr-defined]  # Größe = Schlüssel des y-Bereichs


def test_nebeneinander_eine_groesse_zwei_messungen_zwei_teilbilder_gekoppelt(
    zugriff: MessungsZugriff,
) -> None:
    daten = loese_alle_auf([h1(1, None, 0), h1(2, None, 1)], zugriff, anordnung="nebeneinander")
    _, z = zeichne(daten, anordnung="nebeneinander")
    a1, a2 = z.achsen  # type: ignore[attr-defined]
    assert a1.get_title(loc="left") == "A · |H1|" and a2.get_title(loc="left") == "B · |H1|"
    assert a1.get_shared_x_axes().joined(a1, a2) and a1.get_shared_y_axes().joined(a1, a2)
    assert a1.get_xlim() == a2.get_xlim() and a1.get_ylim() == a2.get_ylim()
    assert a1.get_ylabel() == a2.get_ylabel() == "|H1| [(m/s)/N]"
    assert a1.get_position().y0 == pytest.approx(a2.get_position().y0)  # eine Zeile
    assert len(z.hilfsobjekte["legende"].get_texts()) == 2  # type: ignore[attr-defined]  # einmal


def test_nebeneinander_verschiedene_groessen_y_getrennt_x_gekoppelt(
    zugriff: MessungsZugriff,
) -> None:
    daten = loese_alle_auf(
        [
            SerienSpec(1, None, "kohaerenz", kanalpaar=PAAR, slot=1),
            h1(1, None, 0),
        ],
        zugriff,
        anordnung="nebeneinander",
    )
    _, z = zeichne(daten, anordnung="nebeneinander")
    a_h1, a_koh = z.achsen  # type: ignore[attr-defined]  # sortiert nach Größe: |H1| vor γ²
    assert a_h1.get_ylabel() == "|H1| [(m/s)/N]" and a_koh.get_ylabel() == "Kohärenz γ² [1]"
    assert a_h1.get_shared_x_axes().joined(a_h1, a_koh)
    assert not a_h1.get_shared_y_axes().joined(a_h1, a_koh)
    assert a_koh.get_ylim() == (0.0, 1.05) and z.rollen == ("h1", "kohaerenz")  # type: ignore[attr-defined]


def test_teilbildregel_sortierung_und_raster(zugriff: MessungsZugriff) -> None:
    daten = loese_alle_auf(
        [
            SerienSpec(2, None, "kohaerenz", kanalpaar=PAAR, slot=0),
            h1(2, None, 1),
            h1(1, None, 2),
            h1(1, 100, 3),
        ],
        zugriff,
        anordnung="nebeneinander",
    )
    teile = teilbilder(daten.serien, "nebeneinander")
    assert [(t.groesse, t.messung_id, len(t.serien)) for t in teile] == [
        ("h1", 1, 2),
        ("h1", 2, 1),
        ("kohaerenz", 2, 1),
    ]
    assert len(teile) <= TEILBILDER_MAX
    _, z = zeichne(daten, anordnung="nebeneinander")
    achsen = z.achsen  # type: ignore[attr-defined]
    assert len(achsen) == 3  # mehr als zwei: zwei Spalten, in Zeilen umgebrochen
    p = [a.get_position() for a in achsen]
    assert (
        p[0].y0 == pytest.approx(p[1].y0)
        and p[2].y0 < p[0].y0
        and p[2].x0 == pytest.approx(p[0].x0)
    )
    assert teilbilder([], "ueberlagert") == []


def test_slot_haelt_linienart_beim_entfernen_einer_anderen_serie(zugriff: MessungsZugriff) -> None:
    beide = loese_alle_auf([h1(1, 100, 0), h1(2, 100, 1)], zugriff)
    nur_b = loese_alle_auf([h1(2, 100, 1)], zugriff)  # A entfernt, B behält Slot 1
    _, z2 = zeichne(beide)
    _, z1 = zeichne(nur_b)
    b_vorher = z2.achsen[0].get_lines()[1]  # type: ignore[attr-defined]
    b_nachher = z1.achsen[0].get_lines()[0]  # type: ignore[attr-defined]
    assert b_vorher.get_linestyle() == b_nachher.get_linestyle()  # UI-18, UI-20
    assert b_vorher.get_color() == b_nachher.get_color()


def test_vier_serien_vier_verschiedene_linienarten(zugriff: MessungsZugriff) -> None:
    specs = [h1(1, 100 + i, i) for i in range(4)]
    _, z = zeichne(loese_alle_auf(specs, zugriff))
    arten = [linie.get_linestyle() for linie in z.achsen[0].get_lines()]  # type: ignore[attr-defined]
    assert len(set(arten)) == 4


def test_sichtbarkeit_aendert_achsengrenzen_nicht(zugriff: MessungsZugriff) -> None:
    achsen = AchsenOptionen(frequenz=Bereich(5.0, 20.0))  # x gesetzt: y folgt den Daten im Bereich
    alle = [h1(1, 100, 0), h1(2, 100, 1), h1(1, 103, 2)]
    sicht = loese_alle_auf(alle, zugriff)
    versteckt = loese_alle_auf(
        [h1(1, 100, 0), h1(2, 100, 1, sichtbar=False), h1(1, 103, 2)], zugriff
    )
    _, z_an = zeichne(sicht, achsen=achsen)
    _, z_aus = zeichne(versteckt, achsen=achsen)
    a_an, a_aus = z_an.achsen[0], z_aus.achsen[0]  # type: ignore[attr-defined]
    assert a_an.get_xlim() == a_aus.get_xlim() == (5.0, 20.0)
    assert a_an.get_ylim() == pytest.approx(a_aus.get_ylim(), rel=1e-12)  # UI-21
    assert not a_aus.get_lines()[1].get_visible()  # nicht gezeichnet
    assert len(z_aus.hilfsobjekte["legende"].get_texts()) == 2  # type: ignore[attr-defined]
    assert all("B ·" not in t for t in z_aus.hilfsobjekte["legende_eintraege"])  # type: ignore[attr-defined]


def test_feste_achsen_frequenz_linear_und_log_und_betrag(zugriff: MessungsZugriff) -> None:
    daten = loese_alle_auf([h1(1, None, 0), h1(2, None, 1)], zugriff)
    achsen = AchsenOptionen(
        frequenz=Bereich(2.0, 25.0),
        frequenz_skala="log",
        y={"h1": Bereich(1e-3, 1.0)},
    )
    _, z = zeichne(daten, achsen=achsen, skala="log")
    ax = z.achsen[0]  # type: ignore[attr-defined]
    assert ax.get_xscale() == "log" and ax.get_yscale() == "log"
    assert ax.get_xlim() == pytest.approx((2.0, 25.0), rel=1e-9)  # UI-1, UI-2
    assert ax.get_ylim() == pytest.approx((1e-3, 1.0), rel=1e-9)
    _, lin = zeichne(daten, achsen=AchsenOptionen(y={"h1": Bereich(0.0, 0.5)}), skala="linear")
    assert lin.achsen[0].get_yscale() == "linear"  # type: ignore[attr-defined]
    assert lin.achsen[0].get_ylim() == (0.0, 0.5)  # type: ignore[attr-defined]
    with pytest.raises(AchsenFehler):
        zeichne(daten, achsen=AchsenOptionen(frequenz=Bereich(10.0, 5.0)))


def test_betragsbereich_gilt_fuer_gekoppelte_teilbilder_gemeinsam(zugriff: MessungsZugriff) -> None:
    daten = loese_alle_auf([h1(1, None, 0), h1(2, None, 1)], zugriff, anordnung="nebeneinander")
    achsen = AchsenOptionen(frequenz=Bereich(4.0, 28.0))  # y auto über den sichtbaren Bereich
    _, z = zeichne(daten, anordnung="nebeneinander", achsen=achsen)
    a1, a2 = z.achsen  # type: ignore[attr-defined]
    assert a1.get_ylim() == a2.get_ylim()
    y_max = max(
        float(np.max(s.y[(s.frequenz_hz >= 4.0) & (s.frequenz_hz <= 28.0)])) for s in daten.serien
    )
    assert a1.get_ylim()[1] >= y_max  # die Daten beider Teilbilder liegen im Bild


def test_phase_in_grad_mit_vorzeichenkonvention_und_kennzeichen(zugriff: MessungsZugriff) -> None:
    daten = loese_alle_auf(
        [SerienSpec(1, 100, "phase", kanalpaar=PAAR, slot=0)], zugriff, anordnung="ueberlagert"
    )
    _, z = zeichne(daten, kennzeichen_phase="unbestätigt (M8: Phasenbezug)")
    ax = z.achsen[0]  # type: ignore[attr-defined]
    assert ax.get_ylim() == (-180.0, 180.0) and ax.get_ylabel() == "Phase [°]"
    texte = z.alle_texte()  # type: ignore[attr-defined]
    assert any("positiv = Vib X eilt Ref1 voraus" in t for t in texte)
    assert any("unbestätigt (M8: Phasenbezug)" in t for t in texte)  # Kennzeichen im Kopf
    _, ohne = zeichne(daten)
    assert not any("unbestätigt" in t for t in ohne.alle_texte())  # type: ignore[attr-defined]
    _, fest = zeichne(daten, achsen=AchsenOptionen(y={"phase": Bereich(-90.0, 90.0)}))
    assert fest.achsen[0].get_ylim() == (-90.0, 90.0)  # type: ignore[attr-defined]


def test_zeichenfunktion_ohne_stempeltexte_und_ohne_serie_mit_platzhalter(
    zugriff: MessungsZugriff,
) -> None:
    daten = loese_alle_auf([h1(1, None, 0)], zugriff)
    _, z = zeichne(daten)
    texte = " ".join(z.alle_texte())  # type: ignore[attr-defined]
    assert "Arbeitsansicht" not in texte and "enthält unbestätigte Größen" not in texte  # UI-19
    _, leer = zeichne(DiagrammDaten(serien=()))
    assert PLATZHALTER_KEINE_SERIE in leer.alle_texte()  # type: ignore[attr-defined]
    assert leer.rollen == ()  # type: ignore[attr-defined]


def test_zu_viele_teilbilder_werden_gekuerzt_mit_hinweis(zugriff: MessungsZugriff) -> None:
    gr: list[GroessenId] = ["h1", "h2", "kohaerenz", "phase"]
    specs = [SerienSpec(1, 100, g, kanalpaar=PAAR, slot=i) for i, g in enumerate(gr)]
    specs.append(SerienSpec(2, 100, "h1", kanalpaar=PAAR, slot=0))
    daten = loese_alle_auf(specs, zugriff, anordnung="nebeneinander")
    _, z = zeichne(daten, anordnung="nebeneinander")
    assert len(z.achsen) == TEILBILDER_MAX  # type: ignore[attr-defined]
    assert any("Höchstens" in h for h in z.hinweise)  # type: ignore[attr-defined]


def test_optionen_pruefen_ihre_werte() -> None:
    with pytest.raises(ValueError, match="Anordnung"):
        DiagrammOptionen(anordnung="quer")  # type: ignore[arg-type]
    with pytest.raises(ValueError, match="Skala"):
        DiagrammOptionen(skala="db")  # type: ignore[arg-type]


def test_ansicht_5_und_importtest_ohne_qt_und_pyplot() -> None:
    assert Ansicht.DIAGRAMM.value == 5
    code = (
        "import sys, ldv_automation.darstellung.diagramm, ldv_automation.darstellung.serien_daten;"
        "bad=[m for m in sys.modules if m.startswith(('PySide6','PyQt','matplotlib.pyplot'))];"
        "print(bad)"
    )
    aus = subprocess.run(
        [sys.executable, "-I", "-c", code], capture_output=True, text=True, check=True
    )
    assert aus.stdout.strip() == "[]"
