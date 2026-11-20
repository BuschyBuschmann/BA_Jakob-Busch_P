"""Zoom-Messung ohne Punkte und Zeichnen nur bei Bedarf (R-071, Plan P-AUSW3 4.2).

``_passe_zoom_an`` misst ohne Marker und Punktlabels; das Ergebnis muss gleich der alten Messung
mit vollem Zeichnen sein (Orakel: eigenständige Kopie der alten Intervallhalbierung). Die
Label-Dichte zeichnet nur, wenn sich Figure-Größe oder DPI seit dem letzten Zeichnen irgendeiner
Seite geändert haben; Rechtecke ohne Zeichnen müssen denen mit vollem Zeichnen gleichen.
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import replace
from typing import Any

import numpy as np
import pytest
from dar_animation_hilfen import lange_platte
from matplotlib.figure import Figure

from ldv_automation.darstellung import animation3d
from ldv_automation.darstellung.animation3d import (
    _ELEV_AUFSICHT_GRAD,
    _ZOOM_GRUND_MAX,
    _ZOOM_GRUND_MIN,
    BLICK_VORGABEN,
    AnimationsOptionen,
    Blick,
    _label_rechtecke_px,
    _ohne_punkte,
    _punktlabels_anwenden,
    _z_achse,
    aktualisiere_animation,
    label_schritt,
    zeichne_animation,
)
from ldv_automation.darstellung.stil import THESIS_STIL
from ldv_automation.darstellung.zeichnung import Zeichnung

DATEN = lange_platte(2.25, 15, 9)  # 135 Punkte
VIELE = lange_platte(2.25, 60, 25)  # 1500 Punkte (= _LABEL_MAX)
GROESSEN = [(11.0, 6.8), (9.0, 5.6), (7.0, 4.2), (5.0, 3.2)]


def _zeichnung(
    groesse: tuple[float, float], blick: Blick, daten: Any = DATEN, **opt: Any
) -> Zeichnung:
    o = AnimationsOptionen(punktlabels=True, blick=blick, **opt)
    return zeichne_animation(Figure(figsize=groesse), daten, o, THESIS_STIL)


def _orakel_grund_zoom(z: Zeichnung) -> float:
    """Alte Intervallhalbierung von ``_passe_zoom_an`` mit vollem Zeichnen (Kopie)."""
    fig = z.figure
    ax: Any = z.achsen[0]
    renderer = fig._get_renderer()  # type: ignore[attr-defined]
    aspekt = z.hilfsobjekte["box_aspekt"]
    links, unten, rechts, oben = z.hilfsobjekte["zoom_grenzen"]

    def passt(zoom: float) -> bool:
        ax.set_box_aspect(aspekt, zoom=zoom)
        _z_achse(ax, abs(ax.elev) < _ELEV_AUFSICHT_GRAD, THESIS_STIL)
        fig.draw_without_rendering()
        box = ax.get_tightbbox(renderer)
        assert box is not None
        return bool(
            box.x0 >= links - 0.5
            and box.y0 >= unten - 0.5
            and box.x1 <= rechts + 0.5
            and box.y1 <= oben + 0.5
        )

    if passt(_ZOOM_GRUND_MAX):
        return _ZOOM_GRUND_MAX
    klein, gross = _ZOOM_GRUND_MIN, _ZOOM_GRUND_MAX
    for _ in range(4):
        mitte = 0.5 * (klein + gross)
        if passt(mitte):
            klein = mitte
        else:
            gross = mitte
    return klein


@pytest.mark.parametrize("groesse", GROESSEN)
@pytest.mark.parametrize("blick", ["xy", "xz", "yz", "iso"])
def test_grund_zoom_gleich_orakel_mit_vollem_zeichnen(
    groesse: tuple[float, float], blick: str
) -> None:
    z = _zeichnung(groesse, BLICK_VORGABEN[blick])
    neu = z.hilfsobjekte["grund_zoom"]
    assert neu == _orakel_grund_zoom(z)
    # auch nach einem Blickwechsel über aktualisiere_animation
    opt = z.hilfsobjekte["optionen"]
    aktualisiere_animation(
        z, DATEN, replace(opt, blick=Blick(azim_grad=-120.0, elev_grad=25.0)), THESIS_STIL
    )
    assert z.hilfsobjekte["grund_zoom"] == _orakel_grund_zoom(z)


@pytest.mark.parametrize("zoom", [0.6, 1.0, 1.7])
def test_grund_zoom_gleich_orakel_bei_1500_punkten(zoom: float) -> None:
    blick = replace(BLICK_VORGABEN["iso"], zoom=zoom)
    z = _zeichnung((11.0, 6.8), blick, VIELE)
    assert len(z.hilfsobjekte["punktlabels"]) == 1500
    assert z.hilfsobjekte["grund_zoom"] == _orakel_grund_zoom(z)


def _kinder_ids(z: Zeichnung) -> list[int]:
    ax: Any = z.achsen[0]
    return [id(a) for a in ax._children]


def _punkt_ids(z: Zeichnung) -> set[int]:
    return {id(a) for a in (*z.marker.values(), *z.hilfsobjekte["punktlabels"])}


def test_waehrend_der_messung_fehlen_marker_und_labels_danach_unveraendert(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    z = _zeichnung((9.0, 5.6), BLICK_VORGABEN["iso"])
    ax: Any = z.achsen[0]
    liste = ax._children
    vorher = _kinder_ids(z)
    punkte = _punkt_ids(z)
    assert punkte <= set(vorher)
    gesehen: list[bool] = []
    echt = z.figure.draw_without_rendering

    def zeichne() -> None:
        gesehen.append(punkte.isdisjoint(_kinder_ids(z)))
        echt()

    monkeypatch.setattr(z.figure, "draw_without_rendering", zeichne)
    animation3d._passe_zoom_an(z.figure, ax, z, THESIS_STIL, z.hilfsobjekte["zoom_grenzen"])
    assert len(gesehen) >= 2
    assert all(gesehen)  # bei jeder Messung fehlten alle Punkte und Labels
    assert ax._children is liste  # dasselbe Listenobjekt
    assert _kinder_ids(z) == vorher  # Reihenfolge unverändert


def test_kinder_bleiben_auch_nach_exception_unveraendert() -> None:
    z = _zeichnung((9.0, 5.6), BLICK_VORGABEN["iso"])
    ax: Any = z.achsen[0]
    liste = ax._children
    vorher = _kinder_ids(z)
    with pytest.raises(RuntimeError, match="boom"), _ohne_punkte(z):
        assert _punkt_ids(z).isdisjoint(_kinder_ids(z))
        raise RuntimeError("boom")
    assert ax._children is liste
    assert _kinder_ids(z) == vorher
    # die Labels lassen sich danach weiter entfernen (``_remove_method`` bleibt gültig)
    t = z.hilfsobjekte["punktlabels"][0]
    t.remove()
    assert id(t) not in _kinder_ids(z)


def test_vereinfachter_modus_misst_nicht_und_das_loslassen_genau_einmal(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    z = _zeichnung((9.0, 5.6), BLICK_VORGABEN["iso"])
    opt = z.hilfsobjekte["optionen"]
    aufrufe: list[int] = []
    echt = animation3d._passe_zoom_an

    def zaehle(*args: Any, **kwargs: Any) -> None:
        aufrufe.append(1)
        echt(*args, **kwargs)

    monkeypatch.setattr(animation3d, "_passe_zoom_an", zaehle)
    neu = Blick(azim_grad=-100.0, elev_grad=20.0)
    for f in (0.25, 0.5, 1.0):  # Ziehen
        blick = Blick(azim_grad=-45.0 + f * (neu.azim_grad + 45.0), elev_grad=35.3 - 15.3 * f)
        aktualisiere_animation(z, DATEN, replace(opt, blick=blick, vereinfacht=True), THESIS_STIL)
    assert aufrufe == []
    aktualisiere_animation(z, DATEN, replace(opt, blick=neu), THESIS_STIL)  # Loslassen
    assert len(aufrufe) == 1


# --- Zeichnen nur bei Bedarf ---------------------------------------------------------------------


def _zaehle_zeichnen(z: Zeichnung, monkeypatch: pytest.MonkeyPatch) -> list[int]:
    n: list[int] = []
    echt = z.figure.draw_without_rendering

    def zeichne() -> None:
        n.append(1)
        echt()

    monkeypatch.setattr(z.figure, "draw_without_rendering", zeichne)
    return n


def _rechtecke(z: Zeichnung) -> Any:
    ax: Any = z.achsen[0]
    return _label_rechtecke_px(
        ax,
        z.hilfsobjekte["daten"].koordinaten_m,
        z.hilfsobjekte["punktlabels"],
        z.figure._get_renderer(),  # type: ignore[attr-defined]
    )


def test_zeichnen_bei_dpi_oder_groessenaenderung_ja_sonst_nein(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    z = _zeichnung((9.0, 5.6), BLICK_VORGABEN["iso"])
    n = _zaehle_zeichnen(z, monkeypatch)
    _punktlabels_anwenden(z, DATEN, THESIS_STIL)
    assert n == []  # unverändert: kein Zeichnen
    z.figure.set_dpi(120.0)
    _punktlabels_anwenden(z, DATEN, THESIS_STIL)
    assert len(n) == 1  # dpi geändert
    _punktlabels_anwenden(z, DATEN, THESIS_STIL)
    assert len(n) == 1
    z.figure.set_size_inches(6.0, 4.0)
    _punktlabels_anwenden(z, DATEN, THESIS_STIL)
    assert len(n) == 2  # Größe geändert


def _vergleiche_mit_vollem_zeichnen(
    stoere: Callable[[Figure], None], groesse: tuple[float, float] = (9.0, 5.6)
) -> float:
    """Größte Abweichung (px) der Rechtecke nach ``stoere`` gegenüber vollem Zeichnen."""
    z = _zeichnung(groesse, BLICK_VORGABEN["iso"])
    stoere(z.figure)
    _punktlabels_anwenden(z, DATEN, THESIS_STIL)
    ohne = _rechtecke(z)  # ohne weiteres Zeichnen
    z.figure.draw_without_rendering()
    voll = _rechtecke(z)
    return float(np.max(np.abs(ohne - voll)))


def test_groessenaenderung_ohne_zeichnen_ergibt_dieselben_rechtecke() -> None:
    assert _vergleiche_mit_vollem_zeichnen(lambda f: f.set_size_inches(4.0, 7.0)) < 1e-6
    assert _vergleiche_mit_vollem_zeichnen(lambda f: f.set_size_inches(12.0, 4.0)) < 1e-6


def test_fremdes_zeichnen_bei_anderer_groesse_taeuscht_den_stand_nicht() -> None:
    """MINOR 1: (9, 5.6) -> (4, 7) -> fremdes Zeichnen -> (9, 5.6) darf nicht als aktuell gelten."""

    def stoere(fig: Figure) -> None:
        fig.set_size_inches(4.0, 7.0)
        fig.draw_without_rendering()  # fremdes Zeichnen: die Achsenlage gilt jetzt für (4, 7)
        fig.set_size_inches(9.0, 5.6)

    assert _vergleiche_mit_vollem_zeichnen(stoere) < 1e-6


def test_fremdes_zeichnen_wird_im_stand_vermerkt(monkeypatch: pytest.MonkeyPatch) -> None:
    z = _zeichnung((9.0, 5.6), BLICK_VORGABEN["iso"])
    z.figure.set_size_inches(5.0, 3.0)
    z.figure.draw_without_rendering()  # fremd: danach ist (5, 3) der Stand
    n = _zaehle_zeichnen(z, monkeypatch)
    _punktlabels_anwenden(z, DATEN, THESIS_STIL)
    assert n == []  # schon gezeichnet, kein zweites Mal


# --- MINOR 2: Blick und Zoom ohne Zeichnen gegen voll gezeichnete Referenz -----------------------


@pytest.mark.parametrize("groesse", [(11.0, 6.8), (9.0, 5.6), (5.0, 3.2), (4.0, 7.0), (12.0, 4.0)])
def test_blick_und_zoomwechsel_ohne_zeichnen_gleichen_voll_gezeichneter_referenz(
    groesse: tuple[float, float],
) -> None:
    rng = np.random.default_rng(20261120)
    z = _zeichnung(groesse, BLICK_VORGABEN["iso"])
    opt = z.hilfsobjekte["optionen"]
    ax: Any = z.achsen[0]
    koord = DATEN.koordinaten_m
    labels = z.hilfsobjekte["punktlabels"]
    renderer = z.figure._get_renderer()  # type: ignore[attr-defined]
    for _ in range(6):
        blick = Blick(
            azim_grad=float(rng.uniform(-180.0, 180.0)),
            elev_grad=float(rng.uniform(-90.0, 90.0)),
            zoom=float(rng.uniform(0.5, 2.5)),
        )
        aktualisiere_animation(z, DATEN, replace(opt, blick=blick), THESIS_STIL)
        ohne = _label_rechtecke_px(ax, koord, labels, renderer)
        schritt_ohne = z.hilfsobjekte["punktlabels_schritt"]
        z.figure.draw_without_rendering()  # Referenz: voll gezeichnet
        voll = _label_rechtecke_px(ax, koord, labels, renderer)
        np.testing.assert_allclose(ohne, voll, rtol=0.0, atol=1e-6)
        assert label_schritt(ax, koord, labels, renderer) == schritt_ohne
