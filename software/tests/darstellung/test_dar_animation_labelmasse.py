"""Speicher der Textmaße der Punktlabels (``LabelMasse``, R-071, Plan P-AUSW3 4.2).

Der Speicher darf das Ergebnis nie ändern (bitgleich zu ohne Speicher) und muss bei geänderter
Schrift, DPI oder geänderten Labeltexten verwerfen.
"""

from __future__ import annotations

from dataclasses import replace
from typing import Any

import numpy as np
from dar_animation_hilfen import lange_platte
from matplotlib.figure import Figure

from ldv_automation.darstellung.animation3d import (
    BLICK_VORGABEN,
    AnimationsOptionen,
    Blick,
    LabelMasse,
    _label_rechtecke_px,
    _punktlabels_anwenden,
    aktualisiere_animation,
    label_schritt,
    zeichne_animation,
)
from ldv_automation.darstellung.animation_daten import AnimationsDaten
from ldv_automation.darstellung.stil import THESIS_STIL
from ldv_automation.darstellung.zeichnung import Zeichnung

GROESSEN = [(11.0, 6.8), (9.0, 5.6), (7.0, 4.2), (5.0, 3.2)]
DATEN = lange_platte(2.25, 45, 9)  # 405 Punkte: je nach Ansicht verdichtet oder ausgeblendet
LOCKER = lange_platte(2.25, 6, 3)  # 18 Punkte: alle Labels passen


def _zeichnung(groesse: tuple[float, float], daten: AnimationsDaten = DATEN) -> Zeichnung:
    opt = AnimationsOptionen(punktlabels=True, blick=BLICK_VORGABEN["iso"])
    return zeichne_animation(Figure(figsize=groesse), daten, opt, THESIS_STIL)


def _renderer(z: Zeichnung) -> Any:
    return z.figure._get_renderer()  # type: ignore[attr-defined]


def _rechtecke(z: Zeichnung, masse: LabelMasse | None) -> Any:
    return _label_rechtecke_px(
        z.achsen[0],
        z.hilfsobjekte["daten"].koordinaten_m,
        z.hilfsobjekte["punktlabels"],
        _renderer(z),
        masse,
    )


def _ansicht(z: Zeichnung, elev: float, azim: float, zoom: float) -> None:
    ax: Any = z.achsen[0]
    ax.view_init(elev=elev, azim=azim)
    ax.set_box_aspect(z.hilfsobjekte["box_aspekt"], zoom=zoom * z.hilfsobjekte["grund_zoom"])
    z.figure.draw_without_rendering()


# Blicke (elev, azim) in Grad, Zoom 0,5 bis 2,5; Azimute über den ganzen Bereich
ANSICHTEN = [
    (90.0, -90.0, 1.0),
    (0.0, 0.0, 1.0),
    (35.3, -45.0, 0.5),
    (35.3, 135.0, 2.5),
    (-60.0, 170.0, 1.0),
    (10.0, -170.0, 1.7),
]


def test_ergebnis_mit_speicher_ist_bitgleich_ohne_speicher_und_deckt_alle_dichten_ab() -> None:
    schritte: set[int] = set()
    for groesse, daten in [(g, d) for g in GROESSEN for d in (DATEN, LOCKER)]:
        z = _zeichnung(groesse, daten)
        masse = LabelMasse()
        labels = z.hilfsobjekte["punktlabels"]
        for elev, azim, zoom in ANSICHTEN:
            _ansicht(z, elev, azim, zoom)
            # zweimal: erst gemessen, dann aus dem Speicher
            for _ in range(2):
                assert np.array_equal(_rechtecke(z, masse), _rechtecke(z, None))
                koord = daten.koordinaten_m
                mit = label_schritt(z.achsen[0], koord, labels, _renderer(z), masse)
                ohne = label_schritt(z.achsen[0], koord, labels, _renderer(z))
                assert mit == ohne
            schritte.add(mit)
    assert 1 in schritte  # alle gezeigt
    assert any(2 <= n <= 8 for n in schritte)  # verdichtet
    assert 0 in schritte  # ausgeblendet


def test_blick_und_zoomwechsel_messen_keinen_text_neu() -> None:
    z = _zeichnung((9.0, 5.6))
    masse: LabelMasse = z.hilfsobjekte["label_masse"]
    anzahl = len(z.hilfsobjekte["punktlabels"])
    assert masse.anzahl_messungen == len(masse) == anzahl  # alle Texte verschieden
    opt = z.hilfsobjekte["optionen"]
    for blick in (
        BLICK_VORGABEN["xy"],
        BLICK_VORGABEN["xz"],
        Blick(azim_grad=-45.0, elev_grad=35.3, zoom=2.0),
        Blick(azim_grad=100.0, elev_grad=-20.0, zoom=0.6),
    ):
        aktualisiere_animation(z, DATEN, replace(opt, blick=blick), THESIS_STIL)
    assert masse.anzahl_messungen == anzahl


def test_speicher_verworfen_bei_anderer_schriftgroesse_auch_in_place() -> None:
    z = _zeichnung((9.0, 5.6))
    masse: LabelMasse = z.hilfsobjekte["label_masse"]
    labels = z.hilfsobjekte["punktlabels"]
    vorher = masse.anzahl_messungen
    for t in labels:
        t.set_fontsize(2.0 * t.get_fontsize())  # ändert das Schriftobjekt des Textes in place
    assert np.array_equal(_rechtecke(z, masse), _rechtecke(z, None))
    assert masse.anzahl_messungen == vorher + len(labels)  # neu gemessen
    assert len(masse) == len(labels)  # nichts Veraltetes behalten


def test_speicher_verworfen_bei_anderer_dpi() -> None:
    z = _zeichnung((9.0, 5.6))
    masse: LabelMasse = z.hilfsobjekte["label_masse"]
    vorher = masse.anzahl_messungen
    z.figure.set_dpi(150.0)
    z.figure.draw_without_rendering()
    assert np.array_equal(_rechtecke(z, masse), _rechtecke(z, None))
    assert masse.anzahl_messungen == vorher + len(z.hilfsobjekte["punktlabels"])
    assert len(masse) == len(z.hilfsobjekte["punktlabels"])


def test_speicher_verworfen_bei_anderen_labeltexten() -> None:
    z = _zeichnung((9.0, 5.6))
    masse: LabelMasse = z.hilfsobjekte["label_masse"]
    labels = z.hilfsobjekte["punktlabels"]
    vorher = masse.anzahl_messungen
    for i, t in enumerate(labels):
        t.set_text(f" {i}-{i % 7}")
    assert np.array_equal(_rechtecke(z, masse), _rechtecke(z, None))
    assert masse.anzahl_messungen == vorher + len(labels)
    assert len(masse) == len(labels)  # die alten Texte sind entfernt


def test_leere_labelliste_leert_den_speicher() -> None:
    z = _zeichnung((9.0, 5.6))
    masse: LabelMasse = z.hilfsobjekte["label_masse"]
    assert len(masse) > 0
    assert masse.abmessungen(_renderer(z), []) == []
    assert len(masse) == 0
    leer = _label_rechtecke_px(z.achsen[0], np.empty((0, 3)), [], _renderer(z), masse)
    assert leer.shape == (0, 4)


def test_punktlabels_anwenden_haelt_den_speicher_in_den_hilfsobjekten() -> None:
    z = _zeichnung((9.0, 5.6))
    masse = z.hilfsobjekte["label_masse"]
    _punktlabels_anwenden(z, DATEN, THESIS_STIL)
    assert z.hilfsobjekte["label_masse"] is masse
