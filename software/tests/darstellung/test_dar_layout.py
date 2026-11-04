"""Layout-Kriterien L3-1 … L3-7 und L4-1 … L4-9 (K-AUSW-LAYOUT) per Geometrie der Artists.

Geprüft wird nicht gegen Pixel, sondern über ``get_window_extent`` und ``transData``: Kasten,
Marker, Pfeile, Labels und Legenden werden in pt umgerechnet und gegeneinander geprüft.
Ansicht 3 läuft an ``Input/20261012_ref_Mitte.svd`` (ohne Datei übersprungen), Ansicht 4 zusätzlich
mit synthetischen Rastern (Hoch- und Querformat, dünn besetzt für die Punktlabels).
"""

from __future__ import annotations

import dataclasses
import io
import math
from collections.abc import Callable
from pathlib import Path

import dar_daten as dd
import numpy as np
import numpy.typing as npt
import pytest
from matplotlib.figure import Figure
from matplotlib.transforms import Bbox, BboxBase

from ldv_automation.auswertung.daten import Messdaten
from ldv_automation.auswertung.laden import lade_svd
from ldv_automation.darstellung.auswahl import (
    PaarCache,
    SchwingformDaten,
    SpitzenDaten,
    schwingform_daten,
    spitzen_daten_frf,
)
from ldv_automation.darstellung.bild import baue_stempel, neue_figure, speichere_arbeitsbild
from ldv_automation.darstellung.schwingform import (
    HINWEIS_DICHTE_UNREGELMAESSIG,
    HINWEIS_LABELS_AUS,
    HINWEIS_PFEILE_KURZ,
    Darstellung,
    SchwingformOptionen,
    bildgroesse_schwingform,
    zeichne_schwingform,
)
from ldv_automation.darstellung.spitzen import (
    KASTEN_ABSTAND_OBEN_PT,
    SpitzenOptionen,
    zeichne_spitzen,
)
from ldv_automation.darstellung.stil import THESIS_STIL, Plotstil
from ldv_automation.darstellung.zeichnung import Zeichnung

DATEI = Path(__file__).resolve().parents[3] / "Input" / "20261012_ref_Mitte.svd"
UI_STIL = Plotstil(
    haupt="#0B5C73",
    serienfarben=("#0B5C73", "#1D2327", "#5B6670", "#8A949C"),
    verlauf_hell="#E7F1F4",
    band="#E7E5DF",
)
ARBEIT = (12.0, 7.4)
THESIS_3 = (11.5 / 2.54, 7.0 / 2.54)
THESIS_4 = (11.5 / 2.54, 15.0 / 2.54)
Floats = npt.NDArray[np.float64]


# --- Hilfen -----------------------------------------------------------------------------------


def _pt(fig: Figure) -> float:
    return 72.0 / fig.dpi


def _ext(artist: object) -> Bbox:
    return artist.get_window_extent()  # type: ignore[attr-defined, no-any-return]


def _in(innen: BboxBase, aussen: BboxBase, tol: float = 0.51) -> bool:
    return bool(
        innen.x0 >= aussen.x0 - tol
        and innen.x1 <= aussen.x1 + tol
        and innen.y0 >= aussen.y0 - tol
        and innen.y1 <= aussen.y1 + tol
    )


def _punkt_im(bb: Bbox, xy: Floats) -> Floats:
    return np.asarray(
        (xy[:, 0] >= bb.x0) & (xy[:, 0] <= bb.x1) & (xy[:, 1] >= bb.y0) & (xy[:, 1] <= bb.y1)
    )


def _abstand_rechteck(bb: Bbox, xy: Floats) -> Floats:
    dx = np.maximum(np.maximum(bb.x0 - xy[:, 0], xy[:, 0] - bb.x1), 0.0)
    dy = np.maximum(np.maximum(bb.y0 - xy[:, 1], xy[:, 1] - bb.y1), 0.0)
    return np.asarray(np.hypot(dx, dy))


# --- Ansicht 3 --------------------------------------------------------------------------------


@pytest.fixture(scope="module")
def datei_daten() -> tuple[Messdaten, PaarCache]:
    if not DATEI.is_file():
        pytest.skip("Messdatei nicht vorhanden")
    md = lade_svd(DATEI).messdaten
    return md, PaarCache(md)


def _spitzen(datei: tuple[Messdaten, PaarCache], gewaehlt: int | None) -> SpitzenDaten:
    md, cache = datei
    from ldv_automation.darstellung.auswahl import gesamtband

    return spitzen_daten_frf(
        cache, "Vib Z", "Ref1", baender=gesamtband(md.frequenz_hz), gewaehlt=gewaehlt
    )


def _pruefe_ansicht3(z: Zeichnung, sd: SpitzenDaten, hoehe_min_pt: float = 12.0) -> None:
    fig = z.figure
    fig.draw_without_rendering()
    k = _pt(fig)
    ax = z.achsen[0]
    kasten = z.texte[0]
    kasten_bb = kasten.get_bbox_patch().get_window_extent()  # type: ignore[union-attr]
    # L3-1: Kasten vollständig in der Achse
    assert _in(kasten_bb, ax.bbox)
    # Oberkante 4 pt unter der Achsenoberkante
    assert (ax.bbox.y1 - kasten_bb.y1) * k == pytest.approx(KASTEN_ABSTAND_OBEN_PT, abs=0.8)
    # L3-2: kein Kurven- oder Markerpunkt im Kasten
    kurve = np.column_stack([sd.frequenz_hz, sd.y])
    kurve = kurve[np.isfinite(kurve).all(axis=1) & (kurve[:, 1] > 0)]
    kurve_px = ax.transData.transform(kurve)
    marker_px = ax.transData.transform([[s.f_sp_hz, s.hoehe] for s in sd.spitzen])
    assert not _punkt_im(kasten_bb, kurve_px).any()
    assert not _punkt_im(kasten_bb, marker_px).any()
    # auch die Kurvensegmente zwischen den Stützstellen (nicht nur die Punkte) bleiben draußen
    tt = np.linspace(0.0, 1.0, 25)[None, :, None]
    segmente = (kurve_px[:-1, None, :] * (1 - tt) + kurve_px[1:, None, :] * tt).reshape(-1, 2)
    assert not _punkt_im(kasten_bb, segmente).any()
    # Leitlinie plus Ring: Rechteck der Leitlinie ohne die Umgebung des Rings
    assert sd.gewaehlt is not None
    spitze = sd.spitzen[sd.gewaehlt]
    spitze_px = ax.transData.transform([[spitze.f_sp_hz, spitze.hoehe]])[0]
    linie = z.hilfsobjekte["leitlinie"].arrow_patch.get_window_extent()
    ring = 5.5 / k  # Ringradius in px
    fern = np.hypot(*(kurve_px - spitze_px).T) > ring + 1.0
    assert not _punkt_im(linie, kurve_px[fern]).any()
    fern_m = np.hypot(*(marker_px - spitze_px).T) > ring + 1.0
    assert not _punkt_im(linie, marker_px[fern_m]).any()
    # die Leitlinie endet vor dem Ring (7 pt vor der Markermitte) und beginnt am Kasten
    assert linie.y0 - spitze_px[1] >= 6.0 / k
    assert abs(linie.y1 - kasten_bb.y0) <= 1.0 / k
    # L3-3: Streifen: Achsenoberkante mindestens 12 pt über dem höchsten Markerrand (Ring 5,5 pt)
    hoechster = float(marker_px[:, 1].max())
    assert (ax.bbox.y1 - hoechster) * k - 5.5 >= hoehe_min_pt
    # L3-4: Legende unterhalb der Achse, im Bild, ohne Überlappung mit Achsentitel und Stempel
    legende = _ext(z.hilfsobjekte["legende"])
    assert legende.y1 <= ax.bbox.y0 + 0.5 and _in(legende, fig.bbox)
    assert legende.y1 <= _ext(ax.xaxis.label).y0 + 0.5
    for t in fig.texts:
        stempel = _ext(t)
        assert (
            legende.y0 >= stempel.y1 - 0.5 or legende.x1 <= stempel.x0 or legende.x0 >= stempel.x1
        )
    # L3-5: Mittelformel und Punktzahl
    assert f"Betragsmittel |H1| über {sd.punktzahl} Punkte" in sd.beschriftung
    assert any(
        f"über {sd.punktzahl} Punkte" in t.get_text() for t in z.hilfsobjekte["legende"].texts
    )
    # L3-6: höchstens 3 Zeilen; ζ (2 signifikante Stellen), Methode, Bandgrenzen, alle Kennzeichen
    zeilen = kasten.get_text().split("\n")
    assert len(zeilen) <= 3
    if not math.isnan(spitze.zeta):
        text = kasten.get_text()
        assert f"{spitze.f_l_hz:.3f}".replace(".", ",") in text
        assert f"{spitze.f_r_hz:.3f}".replace(".", ",") in text
        assert "dB-Breite" in text and f"{spitze.zeta:.2g}".replace(".", ",") in text
    if spitze.kennzeichen:
        assert zeilen[-1].startswith(THESIS_STIL.warn_symbol)


@pytest.mark.parametrize("index", [10, 19, 0, -1])
@pytest.mark.parametrize(
    ("stil", "groesse"), [(UI_STIL, ARBEIT), (THESIS_STIL, THESIS_3)], ids=["arbeit", "thesis"]
)
def test_ansicht3_layout_kriterien(
    datei_daten: tuple[Messdaten, PaarCache],
    index: int,
    stil: Plotstil,
    groesse: tuple[float, float],
    tmp_path: Path,
) -> None:
    n = len(_spitzen(datei_daten, None).spitzen)
    sd = _spitzen(datei_daten, index % n)  # 0 und n-1: Spitze am linken bzw. rechten Rand
    stempel = baue_stempel(
        dateiname="x.svd", ansicht="Ansicht 3", git_hash="abc", unbestaetigt=("M8",)
    )
    # Arbeitsbild mit Stempel (L3-4); die Thesis-Größe ohne Stempel
    if stil is UI_STIL:
        z = speichere_arbeitsbild(
            lambda f: zeichne_spitzen(f, sd, SpitzenOptionen(), stil),
            tmp_path / "a.png",
            stempel,
            stil,
            dpi=50,
            groesse_zoll=groesse,
        )
    else:
        z = zeichne_spitzen(neue_figure(stil, groesse), sd, SpitzenOptionen(), stil)
    _pruefe_ansicht3(z, sd)


def test_ansicht3_y_skala_springt_nicht_beim_wechsel_der_spitze(
    datei_daten: tuple[Messdaten, PaarCache],
) -> None:
    grenzen = []
    for wahl in (None, 0, 10, 19, 100):
        z = zeichne_spitzen(
            neue_figure(UI_STIL, ARBEIT), _spitzen(datei_daten, wahl), SpitzenOptionen(), UI_STIL
        )
        grenzen.append(z.achsen[0].get_ylim())
        assert z.hilfsobjekte["streifen"] > 0  # auch ohne gewählte Spitze reserviert
    assert len(set(grenzen)) == 1
    # linear: derselbe Streifen
    lin = {
        zeichne_spitzen(
            neue_figure(UI_STIL, ARBEIT),
            _spitzen(datei_daten, w),
            SpitzenOptionen(skala="linear"),
            UI_STIL,
        )
        .achsen[0]
        .get_ylim()
        for w in (None, 10)
    }
    assert len(lin) == 1


def test_ansicht3_ohne_spitzen_hat_keinen_streifen_und_legende_unten() -> None:
    md = dd.synthetische_messdaten(referenz=False)
    from ldv_automation.darstellung.auswahl import spitzen_daten_spektrum

    sd = spitzen_daten_spektrum(md, PaarCache(md), "Vib Z")
    z = zeichne_spitzen(neue_figure(UI_STIL, ARBEIT), sd, SpitzenOptionen(), UI_STIL)
    assert "streifen" not in z.hilfsobjekte and "leitlinie" not in z.hilfsobjekte
    assert f"über {dd.P} Punkte" in sd.beschriftung and sd.punktzahl == dd.P
    z.figure.draw_without_rendering()
    assert _ext(z.hilfsobjekte["legende"]).y1 <= z.achsen[0].bbox.y0 + 0.5


# --- Ansicht 4 --------------------------------------------------------------------------------


def _raster(
    nx: int,
    ny: int,
    dx: float = 0.025,
    ndx: float = 0.0,
    aendere: Callable[[Floats], None] | None = None,
) -> Messdaten:
    """Messdaten auf einem Raster ``nx mal ny`` (Abstand ``dx`` in m), Formfaktoren wechseln.

    ``aendere`` darf die Koordinaten ``(P, 3)`` vor dem Aufbau der Messdaten verändern.
    """
    p = nx * ny
    gx, gy = np.meshgrid(np.arange(nx) * dx, np.arange(ny) * dx)
    koord = np.column_stack([gx.ravel(), gy.ravel(), np.zeros(p)]) + ndx
    if aendere is not None:
        aendere(koord)
    rng = np.random.default_rng(3)
    form = np.cos(np.linspace(0.0, 5.0, p)) * (0.4 + rng.random(p))
    h0 = dd.mobilitaet_moden(dd.FREQUENZ_HZ, [10.0, 20.0], zeta=0.02)
    ap: dict[str, np.ndarray] = {}
    cp: dict[tuple[str, str], np.ndarray] = {}
    for kanal in ("Vib X", "Vib Y", "Vib Z"):
        h = form[:, None] * h0[None, :]
        ap[kanal] = (np.abs(h) ** 2 + dd.N_VIB).astype(np.float64)
        cp[(kanal, "Ref1")] = h.astype(np.complex128)
    ap["Ref1"] = np.full((p, dd.K), 1.0 + dd.N_REF)
    return dd.messdaten(
        frequenz_hz=dd.FREQUENZ_HZ, ap=ap, cp=cp, delta_f_hz=dd.DF_HZ, koordinaten_m=koord
    )


@pytest.fixture(scope="module")
def hochformat() -> SchwingformDaten:
    """9 mal 15 Punkte (Verhältnis 0,6), mit einigen unsicheren Punkten (γ² < γ²_min)."""
    md = _raster(9, 15)
    rauschen = np.full(md.anzahl_punkte, dd.N_VIB)
    rauschen[[4, 20, 44]] = 1.0
    ap = {k: v.copy() for k, v in md.ap.items()}
    for kanal in ("Vib X", "Vib Y", "Vib Z"):
        ap[kanal] = ap[kanal] - dd.N_VIB + rauschen[:, None]
    md = dataclasses.replace(md, ap=ap)
    return schwingform_daten(md, PaarCache(md), 10.0, komponente="Z")


@pytest.fixture(scope="module")
def datei_sf(datei_daten: tuple[Messdaten, PaarCache]) -> SchwingformDaten:
    md, cache = datei_daten
    return schwingform_daten(md, cache, 18.0, komponente="Z")


def _d_nn(sd: SchwingformDaten, ebene: tuple[int, int] = (0, 1)) -> float:
    xy = sd.koordinaten_m[:, list(ebene)]
    d = np.hypot(*(xy[:, None, :] - xy[None, :, :]).transpose(2, 0, 1))
    d[d <= 0] = np.inf
    return float(np.median(d.min(axis=1)))


def _zentren_px(z: Zeichnung, sd: SchwingformDaten) -> Floats:
    ax = z.achsen[0]
    return np.asarray(ax.transData.transform(sd.koordinaten_m[:, :2]))


def _pruefe_ansicht4(
    z: Zeichnung,
    sd: SchwingformDaten,
    groesse: tuple[float, float],
    *,
    phase: bool,
    hoehe_gefuellt: bool = True,
) -> None:
    fig = z.figure
    fig.draw_without_rendering()
    k = _pt(fig)
    ax = z.achsen[0]
    zentren = _zentren_px(z, sd)
    d_nn = _d_nn(sd)
    d_pt = z.hilfsobjekte["d_pt"]
    r_max = z.hilfsobjekte["r_max_pt"]
    radius = z.hilfsobjekte["radius_pt"]
    # L4-1: Achsenbox füllt die verfügbare Höhe (Hochformat) und die längere Richtung ist genutzt
    assert d_pt == pytest.approx(d_nn * z.hilfsobjekte["pt_je_m"], rel=1e-9)
    if hoehe_gefuellt:
        assert ax.bbox.height * k >= 0.85 * groesse[1] * 72.0
    lang = int(np.argmax(np.ptp(zentren, axis=0)))
    belegt = float(np.ptp(zentren[:, lang])) / float(ax.bbox.height if lang == 1 else ax.bbox.width)
    kurze_seite = max(
        int(np.ptp(sd.koordinaten_m[:, 0]) / d_nn), int(np.ptp(sd.koordinaten_m[:, 1]) / d_nn)
    )
    assert belegt >= (0.8 if kurze_seite >= 8 else 0.5)
    breite_ok = np.all(
        (zentren >= [ax.bbox.x0, ax.bbox.y0]) & (zentren <= [ax.bbox.x1, ax.bbox.y1])
    )
    assert breite_ok  # keine Überstände der Daten
    for r in radius:
        assert (
            zentren[:, 0].min() - r / k >= ax.bbox.x0 and zentren[:, 0].max() + r / k <= ax.bbox.x1
        )
    # L4-4: Radien und keine Überlappung
    if phase:
        assert r_max <= max(0.22 * d_pt, 2.5) + 1e-9 and r_max <= 5.5
    dist = np.hypot(*(zentren[:, None, :] - zentren[None, :, :]).transpose(2, 0, 1)) * k
    np.fill_diagonal(dist, np.inf)
    assert np.all(dist > radius[:, None] + radius[None, :])
    # L4-5: Ring überdeckt keinen Nachbarmarker
    if "bezug" in z.marker:
        ring_r = r_max + 3.0
        assert z.marker["bezug"].get_markersize() == pytest.approx(2 * ring_r)
        b = int(
            np.argmin(
                np.hypot(*(zentren - ax.transData.transform(z.marker["bezug"].get_xydata()[0])).T)
            )
        )
        andere = np.delete(np.arange(len(radius)), b)
        assert np.all(dist[b, andere] > ring_r + radius[andere])
    # L4-7/L4-8: Zeichenerklärung außerhalb der Achse, Punktzahl im Bild
    text = z.hilfsobjekte["punktzahl"]
    assert f"{len(sd.label)} Messpunkte" in text.get_text()
    assert not Bbox.intersection(_ext(text), ax.bbox)
    erkl = z.hilfsobjekte.get("zeichenerklaerung")
    if erkl is not None:
        assert not Bbox.intersection(_ext(erkl), ax.bbox)
        assert _in(_ext(erkl), fig.bbox)
    assert _in(_ext(text), fig.bbox)
    for ax_extra in fig.axes:
        assert _in(_ext(ax_extra), fig.bbox) or ax_extra is ax


def _pfeil_geometrie(z: Zeichnung) -> tuple[Floats, Floats, Floats]:
    pf = z.hilfsobjekte["pfeile"]
    u, v, _ = pf.get_UVC() if hasattr(pf, "get_UVC") else (pf.U, pf.V, None)
    return np.asarray(pf.X), np.asarray(pf.Y), np.hypot(np.asarray(u), np.asarray(v))


@pytest.mark.parametrize("modus", ["phase_ref", "phase_relativ"])
@pytest.mark.parametrize("groesse_art", ["arbeit", "thesis_datenaspekt", "thesis_15cm"])
def test_ansicht4_hochformat_kriterien(
    hochformat: SchwingformDaten, modus: Darstellung, groesse_art: str
) -> None:
    sd = hochformat
    stil = UI_STIL if groesse_art == "arbeit" else THESIS_STIL
    groesse = {
        "arbeit": ARBEIT,
        "thesis_datenaspekt": bildgroesse_schwingform(sd),
        "thesis_15cm": THESIS_4,
    }[groesse_art]
    assert sd.kohaerenz_ok is not None and list(np.flatnonzero(~sd.kohaerenz_ok)) == [4, 20, 44]
    z = zeichne_schwingform(
        neue_figure(stil, groesse),
        sd,
        SchwingformOptionen(darstellung=modus),
        stil,
    )
    # 11,5 mal 15 cm ist für dieses Raster (q ≈ 0,6) zu schmal: die Plotspalte begrenzt die Höhe
    _pruefe_ansicht4(z, sd, groesse, phase=True, hoehe_gefuellt=groesse_art != "thesis_15cm")
    # L4-2: alle Pfeile gleich lang = 0,8 · d_NN, Winkel = Phase
    x, y, laenge = _pfeil_geometrie(z)
    d_nn = _d_nn(sd)
    assert np.ptp(laenge) <= 1e-9 * float(laenge.max())
    assert laenge[0] == pytest.approx(0.8 * d_nn, rel=1e-9)
    if z.hilfsobjekte["d_pt"] >= 12.5:
        assert laenge[0] * z.hilfsobjekte["pt_je_m"] >= 10.0
    pf = z.hilfsobjekte["pfeile"]
    u, v = pf.U, pf.V
    ok = np.ones(len(sd.label), bool)
    ok[[4, 20, 44]] = False
    winkel = np.degrees(np.arctan2(v, u))
    soll = z.hilfsobjekte["winkel_grad"][ok]
    np.testing.assert_allclose((winkel - soll + 180.0) % 360.0 - 180.0, 0.0, atol=1e-9)
    # L4-3: kein Pfeil an den unsicheren Punkten
    unsicher_xy = sd.koordinaten_m[[4, 20, 44], :2]
    for ux, uy in unsicher_xy:
        assert not np.any(np.isclose(x, ux) & np.isclose(y, uy))
    assert len(x) == len(sd.label) - 3
    # L4-7: Kreuze und Erklärung mit Anzahl
    assert len(z.marker["unsicher"].get_xdata()) == 3
    erkl = " ".join(t.get_text() for t in z.hilfsobjekte["zeichenerklaerung"].texts)
    assert "Phase unsicher (3)" in erkl.replace("\n", " ")
    assert "davon 3 gekennzeichnet" in z.hilfsobjekte["punktzahl"].get_text()


def test_ansicht4_pfeil_und_marker_masse_in_pt(hochformat: SchwingformDaten) -> None:
    z = zeichne_schwingform(
        neue_figure(UI_STIL, ARBEIT),
        hochformat,
        SchwingformOptionen(darstellung="phase_ref"),
        UI_STIL,
    )
    z.figure.draw_without_rendering()
    k = _pt(z.figure)
    ax = z.achsen[0]
    pf = z.hilfsobjekte["pfeile"]
    # gemessen in pt über transData: Länge = 0,8 · d_pt, unabhängig vom Winkel
    kopf = ax.transData.transform(np.column_stack([pf.X + pf.U, pf.Y + pf.V]))
    fuss = ax.transData.transform(np.column_stack([pf.X, pf.Y]))
    laengen = np.hypot(*(kopf - fuss).T) * k
    np.testing.assert_allclose(laengen, 0.8 * z.hilfsobjekte["d_pt"], rtol=1e-9)
    # Markerfläche ∝ |v|: sizes = (2r)² und r = r_max·√(|v|/|v|max) (mindestens 0,35 r_max)
    sd = hochformat
    assert sd.amplitude is not None
    betrag = np.abs(sd.amplitude)
    sizes = np.asarray(z.marker["punkte"].get_sizes())
    r = np.sqrt(sizes) / 2
    r_max = z.hilfsobjekte["r_max_pt"]
    unsicher = ~sd.kohaerenz_ok  # type: ignore[operator]
    b = betrag[~unsicher]
    erwartet = np.maximum(r_max * np.sqrt(b / b.max()), max(0.35 * r_max, 1.5))
    np.testing.assert_allclose(r, erwartet, rtol=1e-9)
    # Schaftbreite und heller Rand
    assert pf.width == pytest.approx(1.4 / 72.0) and pf.units == "inches"
    # der Pfeil liegt unter den Markern: sein heller Rand schneidet sie nicht an
    assert pf.get_zorder() < z.marker["punkte"].get_zorder()
    effekt = pf.get_path_effects()
    assert effekt and effekt[0]._gc["linewidth"] == pytest.approx(1.6)


def test_ansicht4_betrag_einheitlicher_radius_und_unsichere_punkte_markiert(
    hochformat: SchwingformDaten,
) -> None:
    z = zeichne_schwingform(
        neue_figure(UI_STIL, ARBEIT), hochformat, SchwingformOptionen(), UI_STIL
    )
    r = np.sqrt(np.asarray(z.marker["punkte"].get_sizes())) / 2
    assert np.ptp(r) == 0 and r[0] == pytest.approx(
        max(min(0.35 * z.hilfsobjekte["d_pt"], 6.5), 2.5)
    )
    assert "pfeile" not in z.hilfsobjekte
    # unsichere Punkte (4, 20, 44) tragen auch hier das Kreuz und zählen nicht zur Farbskala
    assert len(z.marker["unsicher"].get_xdata()) == 3
    assert len(z.marker["punkte"].get_offsets()) == len(hochformat.label) - 3
    erkl = " ".join(t.get_text() for t in z.hilfsobjekte["zeichenerklaerung"].texts)
    assert "γ² < 0,9: unsicher (3)" in erkl.replace("\n", " ")  # im Betragsbild nicht „Phase“
    _pruefe_ansicht4(z, hochformat, ARBEIT, phase=False)


def test_ansicht4_beispieldatei_arbeitsgroesse_und_thesis(datei_sf: SchwingformDaten) -> None:
    for modus in ("phase_ref", "phase_relativ"):
        z = zeichne_schwingform(
            neue_figure(UI_STIL, ARBEIT),
            datei_sf,
            SchwingformOptionen(darstellung=modus),
            UI_STIL,
        )
        _pruefe_ansicht4(z, datei_sf, ARBEIT, phase=True)
        assert 14.0 < z.hilfsobjekte["d_pt"] < 30.0  # Spezifikation: d ≈ 16 … 26 pt
        # Dichtebedingung 4.7: Labels im Standardbild aus, Hinweis statt Labels
        assert "punktlabels" not in z.hilfsobjekte and HINWEIS_LABELS_AUS in z.hinweise
    groesse = bildgroesse_schwingform(datei_sf)
    assert groesse[0] == pytest.approx(11.5 / 2.54) and groesse[1] > groesse[0]  # Hochformat
    z = zeichne_schwingform(
        neue_figure(THESIS_STIL, groesse),
        datei_sf,
        SchwingformOptionen(darstellung="phase_relativ"),
        THESIS_STIL,
    )
    _pruefe_ansicht4(z, datei_sf, groesse, phase=True)
    assert z.hilfsobjekte["d_pt"] >= 12.5  # Pfeile ≥ 10 pt
    assert HINWEIS_PFEILE_KURZ not in z.hinweise


def test_ansicht4_labels_bei_ausreichendem_abstand_ohne_ueberlappung() -> None:
    md = _raster(5, 7, dx=0.1)
    sd = schwingform_daten(md, PaarCache(md), 10.0, komponente="Z")
    for modus in ("betrag", "phase_relativ"):
        z = zeichne_schwingform(
            neue_figure(UI_STIL, ARBEIT),
            sd,
            SchwingformOptionen(darstellung=modus),
            UI_STIL,
        )
        z.figure.draw_without_rendering()
        labels = z.hilfsobjekte["punktlabels"]
        assert len(labels) == len(sd.label) and HINWEIS_LABELS_AUS not in z.hinweise
        k = _pt(z.figure)
        zentren = _zentren_px(z, sd)
        radius = z.hilfsobjekte["radius_pt"] / k
        boxen = [_ext(t) for t in labels]
        ax = z.achsen[0]
        for i, bb in enumerate(boxen):
            assert _in(bb, ax.bbox, tol=1.0)
            assert np.all(_abstand_rechteck(bb, zentren) >= radius)  # kein Marker unter dem Text
            for j in range(i + 1, len(boxen)):
                assert not Bbox.intersection(bb, boxen[j]) or (
                    bb.x1 <= boxen[j].x0
                    or bb.x0 >= boxen[j].x1
                    or bb.y1 <= boxen[j].y0
                    or bb.y0 >= boxen[j].y1
                )
        if modus == "phase_relativ":
            x, y, _ = _pfeil_geometrie(z)
            pf = z.hilfsobjekte["pfeile"]
            for s in np.linspace(0, 1, 9):
                punkt = ax.transData.transform(np.column_stack([x + s * pf.U, y + s * pf.V]))
                for bb in boxen:
                    assert np.all(_abstand_rechteck(bb, punkt) > 0.0)
            ring = ax.transData.transform(z.marker["bezug"].get_xydata())[0]
            ring_r = (z.hilfsobjekte["r_max_pt"] + 3.0) / k
            for bb in boxen:
                assert _abstand_rechteck(bb, ring[None, :])[0] >= ring_r
    # Label gegenüber dem Pfeil: Mittelpunkt des Labels liegt auf der Pfeilgegenseite
    z = zeichne_schwingform(
        neue_figure(UI_STIL, ARBEIT), sd, SchwingformOptionen(darstellung="phase_relativ"), UI_STIL
    )
    z.figure.draw_without_rendering()
    zentren = _zentren_px(z, sd)
    pf = z.hilfsobjekte["pfeile"]
    mitte = np.array(
        [
            [_ext(t).x0 + _ext(t).width / 2, _ext(t).y0 + _ext(t).height / 2]
            for t in z.hilfsobjekte["punktlabels"]
        ]
    )
    # alle Punkte haben hier einen Pfeil (kohärent, |v| > 0): Label-Richtung · Pfeil ≤ 0
    assert sd.amplitude is not None
    winkel = z.hilfsobjekte["winkel_grad"] * np.pi / 180.0
    richtung = np.column_stack([np.cos(winkel), np.sin(winkel)])
    assert np.mean(np.sum((mitte - zentren) * richtung, axis=1) <= 0) > 0.9
    assert len(pf.X) == len(sd.label)


def test_ansicht4_labels_werden_abgeschaltet_wenn_punkte_zu_dicht(
    datei_sf: SchwingformDaten,
) -> None:
    z = zeichne_schwingform(
        neue_figure(UI_STIL, ARBEIT), datei_sf, SchwingformOptionen(punktlabels=False), UI_STIL
    )
    assert HINWEIS_LABELS_AUS not in z.hinweise  # vom Nutzer abgeschaltet: kein Dichtehinweis


def test_ansicht4_kurze_pfeile_melden_hinweis(hochformat: SchwingformDaten) -> None:
    z = zeichne_schwingform(
        neue_figure(UI_STIL, (3.0, 3.0)),
        hochformat,
        SchwingformOptionen(darstellung="phase_ref"),
        UI_STIL,
    )
    assert 0.8 * z.hilfsobjekte["d_pt"] < 10.0 and HINWEIS_PFEILE_KURZ in z.hinweise
    # der Pfeil wird trotzdem mit 0,8·d gezeichnet
    _, _, laenge = _pfeil_geometrie(z)
    assert laenge[0] == pytest.approx(0.8 * _d_nn(hochformat), rel=1e-9)


def test_ansicht4_m6_ungueltige_punkte_sind_hohle_rauten_ohne_pfeil(
    hochformat: SchwingformDaten,
) -> None:
    sd = hochformat
    ungueltig = np.ones(len(sd.label), bool)
    ungueltig[[2, 4]] = False  # Punkt 4 ist zugleich unsicher: die Raute gilt
    gesetzt = dataclasses.replace(sd, gueltig=ungueltig)
    z = zeichne_schwingform(
        neue_figure(UI_STIL, ARBEIT), gesetzt, SchwingformOptionen(darstellung="phase_ref"), UI_STIL
    )
    raute = z.marker["ungueltig"]
    np.testing.assert_array_equal(raute.get_offsets(), sd.koordinaten_m[[2, 4], :2])
    assert raute.get_paths()[0].vertices.shape[0] >= 4
    assert not np.any(raute.get_facecolors()[:, 3] == 0)  # Füllung = Flächenfarbe, hohl wirkend
    x, y, _ = _pfeil_geometrie(z)
    for i in (2, 4):
        assert not np.any(
            np.isclose(x, sd.koordinaten_m[i, 0]) & np.isclose(y, sd.koordinaten_m[i, 1])
        )
    assert len(z.marker["unsicher"].get_xdata()) == 2  # 20 und 44; Punkt 4 zählt nur als Raute
    erkl = " ".join(t.get_text() for t in z.hilfsobjekte["zeichenerklaerung"].texts).replace(
        "\n", " "
    )
    assert "ungültig (M6) (2)" in erkl and "Phase unsicher (2)" in erkl
    assert "davon 4 gekennzeichnet" in z.hilfsobjekte["punktzahl"].get_text()
    # Betragsdarstellung: ungültige Punkte zählen nicht zur Farbskala
    huge = dataclasses.replace(gesetzt, betrag=np.where(~ungueltig, 1e6, sd.betrag))
    zb = zeichne_schwingform(neue_figure(UI_STIL, ARBEIT), huge, SchwingformOptionen(), UI_STIL)
    assert zb.marker["punkte"].norm.vmax < 1e5
    assert len(zb.marker["punkte"].get_offsets()) == len(sd.label) - 4  # 2 M6, 2 unsicher (20, 44)


def test_ansicht4_randfaelle_stuerzen_nicht_ab() -> None:
    md = _raster(1, 1)
    sd = schwingform_daten(md, PaarCache(md), 10.0, komponente="Z")
    for modus in ("betrag", "phase_ref"):
        zeichne_schwingform(
            neue_figure(UI_STIL, ARBEIT),
            sd,
            SchwingformOptionen(darstellung=modus),
            UI_STIL,
        )
    md2 = _raster(3, 2, dx=0.0)  # alle Punkte identisch
    sd2 = schwingform_daten(md2, PaarCache(md2), 10.0, komponente="Z")
    zeichne_schwingform(neue_figure(UI_STIL, ARBEIT), sd2, SchwingformOptionen(), UI_STIL)
    alle = dataclasses.replace(sd, gueltig=np.zeros(1, bool))
    zeichne_schwingform(neue_figure(UI_STIL, ARBEIT), alle, SchwingformOptionen(), UI_STIL)
    zeichne_schwingform(
        neue_figure(UI_STIL, ARBEIT), alle, SchwingformOptionen(darstellung="phase_ref"), UI_STIL
    )


def test_arbeitsbild_mit_stempel_laesst_ansicht4_im_nutzbaren_bereich(
    hochformat: SchwingformDaten, tmp_path: Path
) -> None:
    stempel = baue_stempel(dateiname="x", ansicht="a", git_hash="h", unbestaetigt=("M8",))
    z = speichere_arbeitsbild(
        lambda f: zeichne_schwingform(
            f, hochformat, SchwingformOptionen(darstellung="phase_ref"), UI_STIL
        ),
        tmp_path / "a.png",
        stempel,
        UI_STIL,
        dpi=50,
        groesse_zoll=ARBEIT,
    )
    fig = z.figure
    fig.draw_without_rendering()
    oberkante_stempel = max(_ext(t).y1 for t in fig.texts)
    for a in fig.axes:
        assert _ext(a).y0 >= oberkante_stempel - 0.5
    _pruefe_ansicht4(z, hochformat, (ARBEIT[0], ARBEIT[1] * (1 - 0.028 * 2 - 0.012)), phase=True)


# --- K-AUSW-D3: Pfeil unter dem Marker, Labels (Ausweichen, Abbruch, Pfeilkopf), Randfälle ------


def _pfeilpunkte_px(z: Zeichnung, anteile: int = 17) -> Floats:
    """Punkte entlang aller Pfeile (Schaft und Kopf) in Pixeln."""
    ax = z.achsen[0]
    pf = z.hilfsobjekte["pfeile"]
    s = np.linspace(0.0, 1.0, anteile)
    return np.vstack(
        [ax.transData.transform(np.column_stack([pf.X + a * pf.U, pf.Y + a * pf.V])) for a in s]
    )


def _label_boxen(z: Zeichnung) -> list[Bbox]:
    z.figure.draw_without_rendering()
    return [_ext(t) for t in z.hilfsobjekte["punktlabels"]]


def _pruefe_labels_frei(z: Zeichnung, sd: SchwingformDaten) -> None:
    """L4-6 mit Pfeilkopf: unter keinem Label liegt ein Marker, Pfeil (mit Kopf) oder Label."""
    k = _pt(z.figure)
    boxen = _label_boxen(z)
    zentren = _zentren_px(z, sd)
    radius = z.hilfsobjekte["radius_pt"] / k
    ax = z.achsen[0]
    for i, bb in enumerate(boxen):
        assert _in(bb, ax.bbox, tol=1.0)
        assert np.all(_abstand_rechteck(bb, zentren) >= radius - 0.5)
        if "pfeile" in z.hilfsobjekte:
            # halbe Kopfbreite (4 · 1,4 pt / 2 = 2,8 pt) muss frei bleiben, nicht nur die Achse
            assert np.all(_abstand_rechteck(bb, _pfeilpunkte_px(z)) >= 2.8 / k - 0.5)
        for bb2 in boxen[i + 1 :]:
            assert bb.x1 <= bb2.x0 or bb.x0 >= bb2.x1 or bb.y1 <= bb2.y0 or bb.y0 >= bb2.y1


def test_ansicht4_pfeil_liegt_unter_dem_marker_und_der_rand_schneidet_ihn_nicht() -> None:
    md = _raster(5, 7, dx=0.1)
    sd = schwingform_daten(md, PaarCache(md), 10.0, komponente="Z")
    z = zeichne_schwingform(
        neue_figure(UI_STIL, ARBEIT),
        sd,
        SchwingformOptionen(darstellung="phase_relativ", punktlabels=False),
        UI_STIL,
    )
    pf, punkte = z.hilfsobjekte["pfeile"], z.marker["punkte"]
    assert pf.get_zorder() == pytest.approx(2.5) and punkte.get_zorder() == 3
    # Ring über dem Pfeil (sein heller Rand unterbricht den Ring nicht), unter dem Marker
    assert pf.get_zorder() < z.marker["bezug"].get_zorder() < punkte.get_zorder()
    # Pixelprobe: in der Markermitte, wo der Pfeil beginnt, steht die Markerfüllung (kein
    # weißer Rand und kein schwarzer Schaft)
    fig = z.figure
    puffer = io.BytesIO()
    fig.savefig(puffer, format="rgba", dpi=fig.dpi)
    breite_px, hoehe_px = (round(float(v)) for v in fig.bbox.size)
    bild = np.frombuffer(puffer.getvalue(), dtype=np.uint8).reshape(hoehe_px, breite_px, 4)
    bild = bild[:, :, :3].astype(float)
    ax = z.achsen[0]
    zentren = _zentren_px(z, sd)
    farben = punkte.get_facecolors()[:, :3] * 255.0
    bezug = int(
        np.flatnonzero(
            np.isclose(sd.koordinaten_m[:, 0], z.marker["bezug"].get_xdata()[0])
            & np.isclose(sd.koordinaten_m[:, 1], z.marker["bezug"].get_ydata()[0])
        )[0]
    )
    gepruft = 0
    for i in range(len(sd.label)):
        if i == bezug:
            continue
        px = zentren[i]
        zeile = round(float(fig.bbox.height - px[1]))
        spalte = round(float(px[0]))
        ist = bild[zeile, spalte]
        assert np.max(np.abs(ist - farben[i])) < 3.0, (i, ist, farben[i])
        gepruft += 1
    assert gepruft == len(sd.label) - 1 and ax.bbox.width > 0


def test_ansicht4_labels_weichen_aus_und_lassen_den_pfeilkopf_frei() -> None:
    md = _raster(5, 7, dx=0.1)
    sd = schwingform_daten(md, PaarCache(md), 10.0, komponente="Z")
    z = zeichne_schwingform(
        neue_figure(UI_STIL, (4.8, 4.8)),
        sd,
        SchwingformOptionen(darstellung="phase_relativ"),
        UI_STIL,
    )
    assert "punktlabels" in z.hilfsobjekte and HINWEIS_LABELS_AUS not in z.hinweise
    boxen = _label_boxen(z)
    zentren = _zentren_px(z, sd)
    mitte = np.array([[b.x0 + b.width / 2, b.y0 + b.height / 2] for b in boxen])
    richtung = np.arctan2(*(mitte - zentren).T[::-1])
    soll = np.radians(z.hilfsobjekte["winkel_grad"]) + np.pi
    abweichung = np.abs((richtung - soll + np.pi) % (2 * np.pi) - np.pi)
    assert np.any(abweichung > 0.8)  # mindestens ein Label ist ausgewichen
    _pruefe_labels_frei(z, sd)


def test_ansicht4_labels_alle_aus_bei_zu_dichten_punkten_mit_hinweis() -> None:
    md = _raster(5, 7, dx=0.1)
    sd = schwingform_daten(md, PaarCache(md), 10.0, komponente="Z")
    z = zeichne_schwingform(
        neue_figure(UI_STIL, (4.2, 4.2)),
        sd,
        SchwingformOptionen(darstellung="phase_relativ"),
        UI_STIL,
    )
    assert "punktlabels" not in z.hilfsobjekte and HINWEIS_LABELS_AUS in z.hinweise
    assert not [t for t in z.achsen[0].texts if t.get_text().isdigit()]  # keine Reste im Bild


def _nahes_paar(koord: Floats) -> None:
    """Neun Punkte als dichter Block (Abstand 0,003 m) um Punkt 16.

    Der Median von d_NN bleibt der des Rasters (26 von 35 Punkten), die Dichteregel erlaubt also
    Labels; der Punkt in der Mitte des Blocks hat aber keine freie Richtung.
    """
    mitte = koord[16, :2].copy()
    for n, idx in enumerate([10, 11, 12, 15, 16, 17, 20, 21, 22]):
        koord[idx, :2] = mitte + 0.003 * np.array([n % 3 - 1, n // 3 - 1])


@pytest.mark.parametrize("modus", ["betrag", "phase_relativ"])
def test_ansicht4_labels_abbruch_wenn_ein_label_keinen_platz_findet(modus: Darstellung) -> None:
    md = _raster(5, 7, dx=0.1, aendere=_nahes_paar)
    sd = schwingform_daten(md, PaarCache(md), 10.0, komponente="Z")
    z = zeichne_schwingform(
        neue_figure(UI_STIL, ARBEIT), sd, SchwingformOptionen(darstellung=modus), UI_STIL
    )
    # die Dichteregel (Median) lässt Labels zu; das nahe Paar findet keinen Platz: alle entfallen
    assert z.hilfsobjekte["d_pt"] > 40.0
    assert "punktlabels" not in z.hilfsobjekte and HINWEIS_LABELS_AUS in z.hinweise
    assert not [t for t in z.achsen[0].texts if t.get_text().isdigit()]
    # dasselbe Raster ohne das Paar zeigt Labels
    ok = zeichne_schwingform(
        neue_figure(UI_STIL, ARBEIT),
        schwingform_daten(
            _raster(5, 7, dx=0.1), PaarCache(_raster(5, 7, dx=0.1)), 10.0, komponente="Z"
        ),
        SchwingformOptionen(darstellung=modus),
        UI_STIL,
    )
    assert "punktlabels" in ok.hilfsobjekte


def test_ansicht4_unregelmaessige_punktwolke_meldet_hinweis() -> None:
    reg = _raster(5, 7, dx=0.1)
    sd_reg = schwingform_daten(reg, PaarCache(reg), 10.0, komponente="Z")
    z_reg = zeichne_schwingform(
        neue_figure(UI_STIL, ARBEIT), sd_reg, SchwingformOptionen(), UI_STIL
    )
    assert not any("Unregelmäßige Punktwolke" in h for h in z_reg.hinweise)
    md = _raster(5, 7, dx=0.1, aendere=_nahes_paar)
    sd = schwingform_daten(md, PaarCache(md), 10.0, komponente="Z")
    z = zeichne_schwingform(neue_figure(UI_STIL, ARBEIT), sd, SchwingformOptionen(), UI_STIL)
    # kleinster Abstand 0,003 m bei Median 0,1 m: 3 %
    erwartet = HINWEIS_DICHTE_UNREGELMAESSIG.format(anteil="3")
    assert erwartet in z.hinweise

    # knapp über der Schwelle (0,5·Median) gibt es keinen Hinweis
    def halb(koord: Floats) -> None:
        koord[17, :2] = koord[16, :2] + np.array([0.055, 0.0])

    md2 = _raster(5, 7, dx=0.1, aendere=halb)
    sd2 = schwingform_daten(md2, PaarCache(md2), 10.0, komponente="Z")
    z2 = zeichne_schwingform(neue_figure(UI_STIL, ARBEIT), sd2, SchwingformOptionen(), UI_STIL)
    assert not any("Unregelmäßige Punktwolke" in h for h in z2.hinweise)


def test_ansicht4_nan_koordinate_stuerzt_nicht_ab_und_zeichnet_den_rest() -> None:
    md = _raster(5, 7, dx=0.1)
    sd0 = schwingform_daten(md, PaarCache(md), 10.0, komponente="Z")
    koord = sd0.koordinaten_m.copy()
    koord[3, 0] = np.nan  # fehlende Koordinate (der Kern wählt die Ebene vorher)
    sd = dataclasses.replace(sd0, koordinaten_m=koord)
    for modus in ("betrag", "phase_ref", "phase_relativ"):
        z = zeichne_schwingform(
            neue_figure(UI_STIL, ARBEIT), sd, SchwingformOptionen(darstellung=modus), UI_STIL
        )
        z.figure.draw_without_rendering()
        xy = np.asarray(z.marker["punkte"].get_offsets())
        assert len(xy) == len(sd.label)  # der Punkt bleibt in der Datenliste, nur ohne Position
        endlich = np.isfinite(xy).all(axis=1)
        assert endlich.sum() == len(sd.label) - 1
        xlim = z.achsen[0].get_xlim()
        assert all(np.isfinite(xlim))  # die Achsengrenzen kommen aus den endlichen Punkten
        assert z.hilfsobjekte["d_pt"] > 0
