"""Animation, Korrektur K-AUSW3-7: Layout des Bildes (UI-A1, UI-A2, UI-A4, UI-A8).

Geprüft werden Fensterrechtecke (``get_window_extent``) der Bildteile: Pflichtangaben,
Zeichenerklärung, Farbleiste samt Ticks und Titel, z-Tick-Beschriftungen und Kennzeichenkopf
dürfen sich nicht überlappen und nicht aus der Figure ragen. Grundlage sind die beiden Größen
der Abnahme (8,06 x 3,26 in und 10,7 x 4,14 in), 0 und 1 unsichere Punkte, relativer und
absoluter Bezug sowie Auslenkung und Schnelle.
"""

from __future__ import annotations

import itertools
from typing import Any

import numpy as np
import pytest
from dar_animation_hilfen import KohaerenzCache, messdaten_mit_amplitude
from matplotlib.backends.backend_agg import FigureCanvasAgg
from matplotlib.figure import Figure
from matplotlib.patches import Rectangle
from matplotlib.transforms import Bbox

from ldv_automation.darstellung.animation3d import (
    BLICK_VORGABEN,
    AnimationsOptionen,
    zeichne_animation,
)
from ldv_automation.darstellung.animation_daten import AnimationsDaten, animation_daten
from ldv_automation.darstellung.stil import THESIS_STIL
from ldv_automation.darstellung.zeichnung import Zeichnung

GROESSEN = [(8.06, 3.26), (10.7, 4.14)]
"""Figure-Größen in Zoll, bei denen die Design-Abnahme Überlappungen fand (GUI 1100 px)."""
DPI = 100.0


def _daten(n_unsicher: int, modus: str, groesse: str, *, eben: bool = False) -> AnimationsDaten:
    """4 x 5 Punkte (Platte); die ersten ``n_unsicher`` haben zu geringe Kohärenz."""
    gx, gy = np.meshgrid(np.linspace(0.0, 0.4, 5), np.linspace(0.0, 0.3, 4))
    xs, ys = gx.ravel(), gy.ravel()
    z = np.zeros_like(xs) if eben else 0.002 * np.sin(7.0 * xs)
    koord = np.column_stack([xs, ys, z])
    muster = np.sin(1.5 * np.pi * xs / 0.4) * np.cos(0.7 * np.pi * ys / 0.3)
    amp = (muster + 0.1j) * 1e-3
    md = messdaten_mit_amplitude(
        np.column_stack([0.3 * amp, 0.2 * amp, amp]), koordinaten_m=koord, delta_f_hz=12.5
    )
    ok = np.ones((xs.size, 3), dtype=bool)
    ok[:n_unsicher, :] = False
    return animation_daten(
        md,
        KohaerenzCache(md, ok=ok),
        100.0,
        komponente="3D",
        groesse=groesse,  # type: ignore[arg-type]
        bezug_modus=modus,  # type: ignore[arg-type]
        bezug=12 if modus == "relativ" else None,
    )


def _zeichne(
    daten: AnimationsDaten, groesse_zoll: tuple[float, float], blick: str = "iso"
) -> tuple[Figure, Zeichnung]:
    fig = Figure(figsize=groesse_zoll, dpi=DPI)
    FigureCanvasAgg(fig)
    opt = AnimationsOptionen(theta_rad=1.0, blick=BLICK_VORGABEN[blick])
    z = zeichne_animation(fig, daten, opt, THESIS_STIL)
    fig.canvas.draw()
    return fig, z


def _flaechen(fig: Figure, z: Zeichnung) -> dict[str, Bbox]:
    """Fensterrechtecke der Bildteile (Farbleiste mit Ticks und Titel)."""
    renderer = fig.canvas.get_renderer()  # type: ignore[attr-defined]
    teile: dict[str, Bbox] = {
        "pflichtangaben": z.hilfsobjekte["pflichttext"].get_window_extent(renderer),
        "farbleiste": z.hilfsobjekte["farbleiste"].ax.get_tightbbox(renderer),
    }
    if "zeichenerklaerung" in z.hilfsobjekte:
        teile["zeichenerklaerung"] = z.hilfsobjekte["zeichenerklaerung"].get_window_extent(renderer)
    for i, kasten in enumerate(z.texte[: len(z.texte) - 1]):
        if kasten is not z.hilfsobjekte["pflichttext"]:
            teile[f"kennzeichen{i}"] = kasten.get_window_extent(renderer)
    return teile


def _ueberlappungen(teile: dict[str, Bbox]) -> list[tuple[str, str]]:
    return [(a, b) for a, b in itertools.combinations(teile, 2) if teile[a].overlaps(teile[b])]


@pytest.mark.parametrize("groesse_zoll", GROESSEN)
@pytest.mark.parametrize("n_unsicher", [0, 1])
@pytest.mark.parametrize("modus", ["relativ", "absolut"])
@pytest.mark.parametrize("groesse", ["auslenkung", "schnelle"])
def test_ui_a1_farbleiste_ueberlappt_weder_pflichtangaben_noch_legende(
    groesse_zoll: tuple[float, float], n_unsicher: int, modus: str, groesse: str
) -> None:
    fig, z = _zeichne(_daten(n_unsicher, modus, groesse), groesse_zoll)
    teile = _flaechen(fig, z)
    assert _ueberlappungen(teile) == []
    figur = fig.bbox
    for name, box in teile.items():
        assert box.x0 >= -0.5 and box.y0 >= -0.5, name  # Rundung der Fensterkoordinaten
        assert box.x1 <= figur.x1 + 0.5 and box.y1 <= figur.y1 + 0.5, name


@pytest.mark.parametrize("groesse_zoll", GROESSEN)
@pytest.mark.parametrize("blick", ["xy", "xz", "yz", "iso"])
def test_ui_a1_alle_blickvorgaben_ohne_ueberlappung(
    groesse_zoll: tuple[float, float], blick: str
) -> None:
    fig, z = _zeichne(_daten(1, "absolut", "schnelle"), groesse_zoll, blick)
    assert _ueberlappungen(_flaechen(fig, z)) == []


def _z_ticks(fig: Figure, z: Zeichnung) -> list[Bbox]:
    renderer = fig.canvas.get_renderer()  # type: ignore[attr-defined]
    ax: Any = z.achsen[0]
    unten, oben = sorted(ax.get_zlim3d())
    return [
        label.get_window_extent(renderer)
        for ort, label in zip(ax.zaxis.get_majorticklocs(), ax.zaxis.get_ticklabels(), strict=False)
        if label.get_text() and unten <= ort <= oben  # nur Ticks im Bild
    ]


@pytest.mark.parametrize("groesse_zoll", [*GROESSEN, (8.27, 5.83)])
@pytest.mark.parametrize("eben", [True, False])
def test_ui_a2_z_ticks_ueberlagern_sich_nicht_und_halten_abstand_zur_spalte(
    groesse_zoll: tuple[float, float], eben: bool
) -> None:
    fig, z = _zeichne(_daten(0, "relativ", "auslenkung", eben=eben), groesse_zoll)
    ticks = _z_ticks(fig, z)
    for a, b in itertools.combinations(ticks, 2):
        assert not a.overlaps(b)
    rechts = z.hilfsobjekte["rechts"].bbox
    ax: Any = z.achsen[0]
    renderer = fig.canvas.get_renderer()  # type: ignore[attr-defined]
    titel = ax.zaxis.label.get_window_extent(renderer) if ax.get_zlabel() else None
    for box in [*ticks, *([titel] if titel is not None else [])]:
        assert box.x1 < rechts.x0  # Lücke zur rechten Spalte, nicht nur kein Überlappen


def test_ui_a2_z_ticks_der_ebenen_platte_sind_hoechstens_so_viele_wie_platz_ist() -> None:
    fig, z = _zeichne(_daten(0, "relativ", "auslenkung", eben=True), (8.06, 3.26))
    ticks = _z_ticks(fig, z)
    assert len(ticks) <= 2  # 15 pt lange z-Achse im Bild: höchstens zwei Ticks (vorher drei)


def test_ui_a2_z_beschriftung_aktualisiert_sich_mit_dem_blick() -> None:
    """``aktualisiere_animation`` (Blickwechsel) bringt dieselben Ticks wie frisch zeichnen."""
    daten = _daten(0, "relativ", "auslenkung")
    fig, z = _zeichne(daten, (8.06, 3.26), "xy")
    ax: Any = z.achsen[0]
    assert _z_ticks(fig, z) == [] and ax.get_zlabel() == ""
    from dataclasses import replace

    from ldv_automation.darstellung.animation3d import aktualisiere_animation

    opt = replace(z.hilfsobjekte["optionen"], blick=BLICK_VORGABEN["iso"])
    aktualisiere_animation(z, daten, opt, THESIS_STIL)
    fig.canvas.draw()
    frisch_fig, frisch = _zeichne(daten, (8.06, 3.26), "iso")
    ax_neu: Any = z.achsen[0]
    ax_frisch: Any = frisch.achsen[0]
    assert [t.get_text() for t in ax_neu.zaxis.get_ticklabels() if t.get_text()] == [
        t.get_text() for t in ax_frisch.zaxis.get_ticklabels() if t.get_text()
    ]
    del frisch_fig


def test_ui_a4_pflichtangaben_stehen_getrennt_durch_leerzeilen() -> None:
    _fig, z = _zeichne(_daten(0, "relativ", "auslenkung"), (10.7, 4.14))
    text: str = z.hilfsobjekte["pflichttext"].get_text()
    angaben = z.hilfsobjekte["pflichtangaben"]
    bloecke = text.split("\n\n")
    assert len(bloecke) == len(angaben) == 4
    for block, angabe in zip(bloecke, angaben, strict=True):
        assert block.replace("\n", " ").split() == angabe.replace("\n", " ").split()


def test_ui_a8_kennzeichen_stehen_in_einem_gemeinsamen_rahmen() -> None:
    fig, z = _zeichne(_daten(0, "absolut", "auslenkung"), (10.7, 4.14))
    kaesten = [t for t in z.texte if t is not z.hilfsobjekte["pflichttext"]]
    assert len(kaesten) == 2  # M8 und M12 bleiben getrennte Texte (Textalternative, Tests)
    assert all(t.get_bbox_patch() is None for t in kaesten)  # kein eigener Kasten je Text
    rahmen = [a for a in fig.artists if isinstance(a, Rectangle)]
    assert len(rahmen) == 1
    renderer = fig.canvas.get_renderer()  # type: ignore[attr-defined]
    rahmenbox = rahmen[0].get_window_extent(renderer)
    for kasten in kaesten:
        box = kasten.get_window_extent(renderer)
        assert rahmenbox.x0 <= box.x0 and rahmenbox.x1 >= box.x1
        assert rahmenbox.y0 <= box.y0 and rahmenbox.y1 >= box.y1


def test_ui_a3_standardskala_ist_hellblau_grau_dunkelbraun() -> None:
    """Nutzerentscheidung 2026-11-18: Standard ``#A9D0EC / #8C8C8C / #5A2D0C``."""
    from matplotlib.colors import to_rgb

    from ldv_automation.darstellung.stil import Plotstil

    for stil in (Plotstil(), THESIS_STIL):
        assert (stil.div_negativ, stil.div_mitte, stil.div_positiv) == (
            "#A9D0EC",
            "#8C8C8C",
            "#5A2D0C",
        )
        karte = stil.divergierend()
        for anteil, farbe in ((0.0, "#A9D0EC"), (0.5, "#8C8C8C"), (1.0, "#5A2D0C")):
            assert tuple(karte(anteil)[:3]) == pytest.approx(
                to_rgb(farbe), abs=0.01
            )  # Wertetabelle mit 256 Stufen


# --- K2-AUSW3-7 UI-B1: 3D-Bild bei 8,06 x 3,26 in nicht zu klein --------------------------------


def _box_px(z: Zeichnung) -> tuple[float, float]:
    """Breite und Höhe des projizierten Würfels der 3D-Achse in Pixeln."""
    from mpl_toolkits.mplot3d import proj3d

    ax: Any = z.achsen[0]
    grenzen = [ax.get_xlim3d(), ax.get_ylim3d(), ax.get_zlim3d()]
    matrix = ax.get_proj()
    punkte = np.array(
        [
            ax.transData.transform(proj3d.proj_transform(x, y, w, matrix)[:2])
            for x, y, w in itertools.product(*grenzen)
        ]
    )
    return float(np.ptp(punkte[:, 0])), float(np.ptp(punkte[:, 1]))


@pytest.mark.parametrize(("blick", "breite_px", "hoehe_px"), [("xy", 235, 175), ("iso", 300, 200)])
@pytest.mark.parametrize("groesse", ["auslenkung", "schnelle"])
def test_ui_b1_3d_achse_hat_bei_8_06_x_3_26_zoll_eine_mindestgroesse(
    blick: str, breite_px: int, hoehe_px: int, groesse: str
) -> None:
    """Die Platte (4:3) ist in der Aufsicht höhenbegrenzt, in der Iso-Ansicht gilt 300 x 200 px."""
    fig, z = _zeichne(_daten(1, "absolut", groesse), (8.06, 3.26), blick)
    breite, hoehe = _box_px(z)
    assert breite >= breite_px and hoehe >= hoehe_px, (breite, hoehe)
    assert _ueberlappungen(_flaechen(fig, z)) == []
    renderer = fig.canvas.get_renderer()  # type: ignore[attr-defined]
    tight = z.achsen[0].get_tightbbox(renderer)
    assert (
        tight is not None and tight.x0 >= -0.5 and tight.y0 >= -0.5
    )  # Box samt Beschriftung bleibt im Bild


def test_ui_b1_kompakte_stufe_hat_hoechstens_9_pt_und_keine_leerzeilen() -> None:
    from ldv_automation.darstellung.stil import Plotstil

    stil = Plotstil(schrift_pt=10.0)
    fig = Figure(figsize=(8.06, 3.26), dpi=DPI)
    FigureCanvasAgg(fig)
    z = zeichne_animation(
        fig, _daten(0, "relativ", "auslenkung"), AnimationsOptionen(theta_rad=1.0), stil
    )
    text = z.hilfsobjekte["pflichttext"]
    assert text.get_fontsize() == 9.0 and z.hilfsobjekte["kompakt"]
    assert "\n\n" not in text.get_text()
    zeilen = text.get_text().split("\n")
    assert zeilen[0] and all(zeile.startswith("  ") or zeile[0] != " " for zeile in zeilen)
    # Beginn jeder Angabe ist linksbündig, Folgezeilen sind eingerückt
    assert sum(1 for zeile in zeilen if not zeile.startswith(" ")) >= 4
    # das Aktualisieren akzeptiert den ursprünglichen Stil
    from ldv_automation.darstellung.animation3d import aktualisiere_animation

    aktualisiere_animation(z, z.hilfsobjekte["daten"], AnimationsOptionen(theta_rad=2.0), stil)


def test_ui_b1_grosse_figure_bleibt_in_der_normalen_stufe() -> None:
    _fig, z = _zeichne(_daten(0, "relativ", "auslenkung"), (10.7, 5.0))
    assert not z.hilfsobjekte["kompakt"]
    assert "\n\n" in z.hilfsobjekte["pflichttext"].get_text()


@pytest.mark.parametrize(
    ("groesse_zoll", "kompakt"),
    [((8.27, 5.83), False), ((9.0, 5.6), False), ((10.7, 4.14), False), ((8.06, 3.26), True)],
)
def test_ui_c1_kompakt_nur_bei_geringer_hoehe(
    groesse_zoll: tuple[float, float], kompakt: bool
) -> None:
    """A5 (8,27 x 5,83 in) und 9 x 5,6 in sind schmal, aber hoch genug: normale Stufe."""
    fig, z = _zeichne(_daten(1, "absolut", "schnelle"), groesse_zoll)
    assert z.hilfsobjekte["kompakt"] is kompakt
    assert _ueberlappungen(_flaechen(fig, z)) == []


@pytest.mark.parametrize("blick", ["xy", "iso"])  # kantenparallele Blicke: Achse als Punkt
def test_ui_c1_a5_achsentitel_und_ticks_ueberlagern_sich_nicht(blick: str) -> None:
    fig, z = _zeichne(_daten(1, "absolut", "schnelle"), (8.27, 5.83), blick)
    renderer = fig.canvas.get_renderer()  # type: ignore[attr-defined]
    ax: Any = z.achsen[0]
    for achse in (ax.xaxis, ax.yaxis):
        titel = achse.label.get_window_extent(renderer)
        if not achse.label.get_text():
            continue
        for tick in achse.get_ticklabels():
            if tick.get_text() and tick.get_visible():
                assert not titel.overlaps(tick.get_window_extent(renderer)), (blick, achse)


def _zaehle_zoom(monkeypatch: pytest.MonkeyPatch) -> list[int]:
    from ldv_automation.darstellung import animation3d

    aufrufe: list[int] = []
    original = animation3d._passe_zoom_an

    def zaehler(*args: Any, **kwargs: Any) -> None:
        aufrufe.append(1)
        original(*args, **kwargs)

    monkeypatch.setattr(animation3d, "_passe_zoom_an", zaehler)
    return aufrufe


def test_ui_c3_volles_zeichnen_sucht_den_zoom_genau_einmal(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    aufrufe = _zaehle_zoom(monkeypatch)
    _zeichne(_daten(1, "absolut", "schnelle"), (10.7, 4.14))
    assert len(aufrufe) == 1


def test_ui_c2_zoom_bleibt_beim_ziehen_fest_und_wird_beim_loslassen_gemessen(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    from dataclasses import replace

    from ldv_automation.darstellung.animation3d import aktualisiere_animation

    daten = _daten(1, "absolut", "auslenkung")
    _fig, z = _zeichne(daten, (10.7, 4.14))
    zoom0 = z.hilfsobjekte["grund_zoom"]
    aufrufe = _zaehle_zoom(monkeypatch)
    opt = z.hilfsobjekte["optionen"]
    for faktor in (2.0, 4.0, 8.0):
        opt = replace(opt, ueberhoehung=faktor * float(daten.s_auto or 1.0))
        aktualisiere_animation(z, daten, opt, THESIS_STIL, zoom_fest=True)
    assert aufrufe == [] and z.hilfsobjekte["grund_zoom"] == zoom0  # Ziehen: keine Messung
    aktualisiere_animation(z, daten, opt, THESIS_STIL)
    assert len(aufrufe) == 1  # Loslassen: eine Messung
    aktualisiere_animation(z, daten, replace(opt, theta_rad=2.0), THESIS_STIL)
    assert len(aufrufe) == 1  # danach nicht erneut
