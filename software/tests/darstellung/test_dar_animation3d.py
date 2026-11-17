"""Zeichenfunktion der 3D-Animation (R-071, Plan P-AUSW3 AN4): UI-23, UI-25 bis UI-29, UI-33.

Die Tests prüfen die **Figure-Struktur** (Positionen der Scatter-Objekte, Texte, Grenzen, Blick),
keine Pixel. Sollwerte der Positionen stammen aus FG-04 Abschnitt 5 (RF-A1, A2, A4, A6, A7) mit
den dortigen Toleranzen (``rtol = 1e-12``, Nullwerte ``atol = 1e-12·a``).
"""

from __future__ import annotations

import math
from pathlib import Path
from typing import Any

import dar_daten as dd
import numpy as np
import pytest
from dar_animation_hilfen import KohaerenzCache, messdaten_mit_amplitude
from matplotlib.colors import Normalize, TwoSlopeNorm
from matplotlib.figure import Figure

from ldv_automation.darstellung.achsen import Bereich
from ldv_automation.darstellung.animation3d import (
    BLICK_VORGABEN,
    MINDESTHOEHE_ANTEIL,
    AnimationsOptionen,
    Blick,
    achsengrenzen_3d,
    aktualisiere_animation,
    effektive_ueberhoehung,
    farb_norm,
    farbskala,
    pflichttexte,
    scatter_positionen,
    skaliere_einheit,
    zeichne_animation,
)
from ldv_automation.darstellung.animation_daten import AnimationsDaten, animation_daten
from ldv_automation.darstellung.auswahl import PaarCache
from ldv_automation.darstellung.bild import baue_stempel, speichere_arbeitsbild
from ldv_automation.darstellung.stil import DIVERGIEREND_FARBEN_BUNT, THESIS_STIL, Plotstil
from ldv_automation.darstellung.zeichnung import Zeichnung

A_MM = 1e-3 / (2.0 * math.pi * 100.0)
KOORD_2 = [[0.0, 0.0, 0.0], [0.029, 0.0, 0.0]]
TH_N = (0.0, math.pi / 2.0, math.pi, 3.0 * math.pi / 2.0)
GROESSE = (9.0, 5.6)


def _zwei_punkte(**kw: Any) -> AnimationsDaten:
    """RF-A7: Punkt 1 mit 1 mm/s, Punkt 2 mit 0,5 mm/s, Abstand 29 mm, Linie 100 Hz."""
    md = messdaten_mit_amplitude(np.array([1e-3, 0.5e-3]), koordinaten_m=KOORD_2)
    return animation_daten(md, KohaerenzCache(md), 100.0, komponente="Z", **kw)


def _platte() -> AnimationsDaten:
    """Synthetische Platte der Darstellungstests (sechs Punkte, Linie 10 Hz, ein unsicherer)."""
    md = dd.synthetische_messdaten(
        n_vib_je_punkt=np.array([1e-12, 1e-12, 1e-3, 1e-12] + [1e-12] * 2)
    )
    return animation_daten(md, PaarCache(md), 10.0, komponente="3D")


def _zeichne(
    daten: AnimationsDaten, stil: Plotstil = THESIS_STIL, **opt: Any
) -> tuple[Figure, Zeichnung]:
    fig = Figure(figsize=GROESSE)
    z = zeichne_animation(fig, daten, AnimationsOptionen(**opt), stil)
    return fig, z


# --- UI-23: Blickvorgaben ----------------------------------------------------------------------


@pytest.mark.parametrize(
    ("name", "azim", "elev"),
    [("xy", -90.0, 90.0), ("xz", -90.0, 0.0), ("yz", 0.0, 0.0), ("iso", -45.0, 35.26438968)],
)
def test_ui_23_blickvorgaben_setzen_elev_und_azim(name: str, azim: float, elev: float) -> None:
    _, z = _zeichne(_platte(), blick=BLICK_VORGABEN[name])
    ax = _ax(z)
    assert ax.azim == pytest.approx(azim, abs=1e-8)
    assert ax.elev == pytest.approx(elev, abs=1e-8)
    # keine eingebaute Mausdrehung: die Oberfläche steuert selbst (E-A3)
    assert getattr(ax, "_rotate_btn", None) == []


def test_blick_pruefung() -> None:
    assert Blick(azim_grad=10.0, elev_grad=-20.0).zoom == 1.0
    for kw in (
        {"azim_grad": math.nan, "elev_grad": 0.0},
        {"azim_grad": 0.0, "elev_grad": math.inf},
        {"azim_grad": 0.0, "elev_grad": 0.0, "zoom": 0.0},
        {"azim_grad": 0.0, "elev_grad": 0.0, "zoom": math.nan},
    ):
        with pytest.raises(ValueError, match=r"zoom|endlich"):
            Blick(**kw)


def test_z_beschriftung_nur_ausserhalb_der_aufsicht() -> None:
    _, z = _zeichne(_platte(), blick=BLICK_VORGABEN["xy"])
    assert _ax(z).get_zlabel() == ""
    _, z2 = _zeichne(_platte(), blick=BLICK_VORGABEN["iso"])
    assert _ax(z2).get_zlabel() == "z [m]"


# --- UI-25: Positionen in der Figure = AnimationsDaten.positionen -----------------------------


def test_ui_25_positionen_gleich_daten_und_fg04_sollwerte() -> None:
    daten = _zwei_punkte()
    s = effektive_ueberhoehung(daten, AnimationsOptionen())
    for theta in TH_N:
        _, z = _zeichne(daten, theta_rad=theta)
        pos = scatter_positionen(z)
        assert np.array_equal(pos, daten.positionen(theta, s)[daten.bewegt])
    # RF-A1/A4: Punkt 1 (v = 1 mm/s): z(θ_n) = 0, +a, 0, -a (mit s = 1 sichtbar in m)
    ohne = AnimationsOptionen(ueberhoehung=1.0)
    for theta, soll in zip(TH_N, (0.0, A_MM, 0.0, -A_MM), strict=True):
        fig = Figure(figsize=GROESSE)
        z = zeichne_animation(
            fig, daten, AnimationsOptionen(theta_rad=theta, ueberhoehung=1.0), THESIS_STIL
        )
        assert scatter_positionen(z)[0, 2] == pytest.approx(soll, rel=1e-12, abs=1e-12 * A_MM)
        # Ruhelage der x- und y-Koordinaten bleibt: Einzelkomponente Z
        assert scatter_positionen(z)[0, :2] == pytest.approx([0.0, 0.0], abs=0)
    assert ohne.ueberhoehung == 1.0


def test_rf_a6_kreisbahn_in_der_figure() -> None:
    md = messdaten_mit_amplitude(np.array([[1e-3, 1e-3j, 0.0]]))
    daten = animation_daten(md, KohaerenzCache(md), 100.0, komponente="3D")
    soll = np.array([[0, 1, 0], [1, 0, 0], [0, -1, 0], [-1, 0, 0]], dtype=float)
    for theta, s in zip(TH_N, soll, strict=True):
        _, z = _zeichne(daten, theta_rad=theta, ueberhoehung=1.0)
        assert scatter_positionen(z)[0] == pytest.approx(s * A_MM, abs=1e-12 * A_MM)


def test_gekennzeichnete_punkte_stehen_in_der_ruhelage() -> None:
    daten = _platte()
    assert not daten.bewegt.all()
    for theta in (0.4, 2.2):
        _, z = _zeichne(daten, theta_rad=theta)
        xs, ys, zs = z.marker["unsicher"]._offsets3d
        gek = daten.koordinaten_m[~daten.bewegt]
        assert np.array_equal(np.column_stack([xs, ys, zs]), gek)  # exakt, keine Näherung
        assert len(scatter_positionen(z)) == int(daten.bewegt.sum())


# --- UI-26, UI-28, UI-29: Texte, Kennzeichen, Symbole und Anzahl ------------------------------


def test_ui_26_pflichtangaben_im_bild() -> None:
    daten = _zwei_punkte()
    fig, z = _zeichne(daten, theta_rad=math.pi / 2.0)
    text = " ".join(" ".join(z.alle_texte()).split())
    assert (
        "Überhöhung \N{MULTIPLICATION SIGN}4555" in text
    )  # (a) s = 4555,3093477 mit 4 signifikanten Stellen
    assert "größte reale Spitzenauslenkung" in text  # (b)
    assert "D_ref = 1,59 µm" in text
    assert "f = 100,000 Hz · Auslenkung Z (CPH)" in text  # (c) mit der Komponente
    assert "θ = 90,0° · Bezug: relativ zu Punkt 100 (Referenz Ref1)" in text  # (d) mit Referenz
    assert "θ = 0°: Auslenkung von Punkt 100, Komponente Z steigt durch null" in text
    assert "Arbeitsansicht" not in text  # den Stempel ergänzt nur speichere_arbeitsbild (ADR-024)
    assert fig is not None


def test_pflichttexte_je_quelle_groesse_und_bezug() -> None:
    md = messdaten_mit_amplitude(np.array([1.0, 0.5]), koordinaten_m=KOORD_2)
    h1 = animation_daten(md, KohaerenzCache(md), 100.0, komponente="Z", quelle="h1")
    a, b, c, d = pflichttexte(h1, 0.0, 2.0, THESIS_STIL)
    assert a == "Überhöhung \N{MULTIPLICATION SIGN}2,000" and "mm/N" in b
    assert c == "f = 100,000 Hz · Auslenkung Z (H1, je 1 N)"
    assert d.split("\n")[0] == "θ = 0,0° · Bezug: relativ zu Punkt 100 (Referenz Ref1)"
    md3 = messdaten_mit_amplitude(np.array([[1e-3, 2e-3j, 0.5e-3]]), koordinaten_m=[[0, 0, 0]])
    d3 = animation_daten(md3, KohaerenzCache(md3), 100.0, komponente="3D", groesse="schnelle")
    a, b, c, d = pflichttexte(d3, 2.0 * math.pi - 1e-4, 1.0, THESIS_STIL)
    assert "Spitzenschnelle" in b and "mm/s" in b and "Schnelle 3D (CPH)" in c
    # 359,994° rundet auf 0,0°
    assert (
        d.split("\n")[0] == "θ = 0,0° · Bezug: relativ zu Punkt 100, Komponente Y (Referenz Ref1)"
    )
    absolut = animation_daten(
        md3, KohaerenzCache(md3), 100.0, komponente="3D", bezug_modus="absolut"
    )
    assert pflichttexte(absolut, 0.0, 1.0, THESIS_STIL)[3] == (
        "θ = 0,0° · Bezug: absolut zu Ref1\nθ = 0°: Ref1 im positiven Maximum"
    )


def test_ui_28_kennzeichen_im_bild() -> None:
    daten = _platte()
    _, z = _zeichne(
        daten,
        kennzeichen_phase="unbestätigt (M8)",
        kennzeichen_koordinaten="Komponenten im Geometrie-KS unbestätigt (M12)",
    )
    texte = z.alle_texte()
    assert "⚠ unbestätigt (M8)" in texte
    assert any("M12" in t for t in texte)
    # Ohne Angabe setzt die Zeichenfunktion die Pflichtkennzeichen selbst (Nachtrag 2 5.2, 8):
    # 3D relativ: nur M12; Einzelkomponente relativ: keines (Tests in test_dar_animation_n3.py)
    _, ohne = _zeichne(daten)
    assert any("M12" in t for t in ohne.alle_texte())
    assert not any("M8" in t for t in ohne.alle_texte())


def test_ui_29_symbole_gleich_wie_standbild_und_anzahl() -> None:
    md = messdaten_mit_amplitude(
        np.array(
            [[1e-3, 2e-3j, 1e-3], [1e-3, 1e-3, 1e-3], [1e-3, 0.5e-3, 1e-3], [2e-3, 1e-3, 1e-3]]
        ),
        koordinaten_m=np.array([[0, 0, 0], [0.03, 0, 0], [0.06, 0, 0], [0.09, 0, 0]], dtype=float),
    )
    cache = KohaerenzCache(
        md, ok=[[1, 1, 1], [1, 0, 1], [1, 1, 1], [1, 1, 1]], gueltig=[1, 1, 0, 1]
    )
    daten = animation_daten(md, cache, 100.0, komponente="3D")
    _, z = _zeichne(daten)
    texte = z.alle_texte()
    assert z.hilfsobjekte["anzahl"] == {"unsicher": 1, "ungueltig": 1, "kein_wert": 0}
    assert any("3D unvollständig" in t and "(1)" in t for t in texte)
    assert any("ungültig (M6) (1)" in t for t in texte)
    assert "unsicher" in z.marker and "ungueltig" in z.marker and "kein_wert" not in z.marker
    # Symbole wie im Standbild (Ansicht 4): Kreuz, hohle Raute (Quadrat nur bei kein Wert)
    marker = {k: z.marker[k].get_paths()[0] for k in ("unsicher", "ungueltig")}
    assert marker["unsicher"] != marker["ungueltig"]


def test_ui_29_einzelkomponente_wort_unsicher_und_kein_wert_quadrat() -> None:
    koord = np.array([[0, 0, 0], [0.03, 0, 0], [0.06, 0, 0]], dtype=float)
    md = messdaten_mit_amplitude(np.array([1e-3, 0.5e-3, np.nan]), koordinaten_m=koord)
    daten = animation_daten(
        md, KohaerenzCache(md, ok=[[1, 1, 1], [1, 1, 0], [1, 1, 1]]), 100.0, komponente="Z"
    )
    _, z = _zeichne(daten)
    texte = z.alle_texte()
    assert any(t.startswith("γ² < 0,9: unsicher (1)") for t in texte)
    assert any("kein Messwert (1)" in t for t in texte)
    assert "kein_wert" in z.marker


def test_hinweis_ueberlagerung_in_zeichnung_hinweise() -> None:
    daten = _zwei_punkte()
    _, klein = _zeichne(daten)
    assert klein.hinweise == ()
    _, gross = _zeichne(daten, ueberhoehung=0.6 * 0.029 / daten.d_ref)
    assert gross.hinweise == ("Punkte können sich überlagern",)


# --- Teilaktualisierung = frisches Zeichnen ---------------------------------------------------


def _ax(z: Zeichnung) -> Any:
    """Die ``Axes3D`` der Zeichnung (mplot3d liefert keine Typen)."""
    return z.achsen[0]


def _texte(z: Zeichnung) -> list[str]:
    """Texte des Bildes ohne die Tickbeschriftung (sie existiert nur bei sichtbaren Achsen)."""
    ax = _ax(z)
    ticks = {t.get_text() for a in (ax.xaxis, ax.yaxis, ax.zaxis) for t in a.get_ticklabels()}
    if not _achse_an(z):
        return [t for t in z.alle_texte() if t not in ticks]
    return list(z.alle_texte())


def _achse_an(z: Zeichnung) -> bool:
    """``Axes3D`` kennt ``axison`` nicht (immer False); der Schalter ist ``_axis3don``."""
    return bool(_ax(z)._axis3don)


def _signatur(z: Zeichnung) -> dict[str, Any]:
    z.figure.draw_without_rendering()  # Tickbeschriftung aktualisieren
    ax = _ax(z)
    cb = z.hilfsobjekte["farbleiste"]
    return {
        "pos": scatter_positionen(z),
        "farbe": np.asarray(z.marker["punkte"].get_array()),
        "texte": _texte(z),
        "grenzen": (ax.get_xlim3d(), ax.get_ylim3d(), ax.get_zlim3d()),
        "aspekt": tuple(ax.get_box_aspect()),
        "blick": (ax.elev, ax.azim),
        "achse_an": _achse_an(z),
        "clim": z.marker["punkte"].get_clim(),
        "cb_label": cb.ax.get_ylabel(),
        "hinweise": z.hinweise,
    }


def _gleich(a: dict[str, Any], b: dict[str, Any]) -> None:
    for k in a:
        if isinstance(a[k], np.ndarray):
            assert np.array_equal(a[k], b[k]), k
        else:
            assert a[k] == b[k], k


@pytest.mark.parametrize(
    "aenderung",
    [
        {"theta_rad": 2.5},
        {"theta_rad": 1.0, "ueberhoehung": 123.0},
        {"theta_rad": 0.2, "blick": Blick(azim_grad=30.0, elev_grad=20.0, zoom=1.7)},
        {"theta_rad": 0.2, "blick": BLICK_VORGABEN["xy"].__class__(-90.0, 90.0, 2.0)},
        {"vereinfacht": True},
        {"farbbereich": Bereich(-1e-3, 2e-3)},
        {"theta_rad": 4.0, "farbbereich": Bereich(None, 5e-3), "vereinfacht": True},
    ],
)
def test_aktualisiere_gleich_frisch_gezeichnet(aenderung: dict[str, Any]) -> None:
    daten = _platte()
    fig = Figure(figsize=GROESSE)
    start = AnimationsOptionen(theta_rad=0.0, blick=BLICK_VORGABEN["iso"])
    z = zeichne_animation(fig, daten, start, THESIS_STIL)
    punkte_vorher = z.marker["punkte"]
    neu = AnimationsOptionen(**{"blick": BLICK_VORGABEN["iso"], **aenderung})
    aktualisiere_animation(z, daten, neu, THESIS_STIL)
    frisch = zeichne_animation(Figure(figsize=GROESSE), daten, neu, THESIS_STIL)
    _gleich(_signatur(z), _signatur(frisch))
    assert z.marker["punkte"] is punkte_vorher  # dieselben Artists, nur ihre Daten wurden gesetzt


def test_aktualisiere_ruft_weder_clear_noch_layout(monkeypatch: pytest.MonkeyPatch) -> None:
    daten = _platte()
    fig = Figure(figsize=GROESSE)
    z = zeichne_animation(fig, daten, AnimationsOptionen(), THESIS_STIL)
    anzahl_achsen = len(fig.axes)

    def verboten(*_a: object, **_k: object) -> None:
        raise AssertionError("fig.clear/Layout in aktualisiere_animation")

    monkeypatch.setattr(fig, "clear", verboten)
    monkeypatch.setattr(fig, "set_layout_engine", verboten)
    for theta in np.linspace(0.0, 2.0 * math.pi, 7):
        aktualisiere_animation(z, daten, AnimationsOptionen(theta_rad=float(theta)), THESIS_STIL)
    assert len(fig.axes) == anzahl_achsen


def test_aktualisiere_lehnt_aufbauaenderungen_ab() -> None:
    daten = _platte()
    z = zeichne_animation(Figure(figsize=GROESSE), daten, AnimationsOptionen(), THESIS_STIL)
    for kw in (
        {"farbe": "betrag"},
        {"farb_komponente": "X"},
        {"ruhelage": False},
        {"punktlabels": True},
        {"kennzeichen_phase": "unbestätigt (M8)"},
        {"kennzeichen_koordinaten": "M12"},
    ):
        with pytest.raises(ValueError, match="neu zeichnen"):
            aktualisiere_animation(z, daten, AnimationsOptionen(**kw), THESIS_STIL)
    with pytest.raises(ValueError, match="neu zeichnen"):
        aktualisiere_animation(z, _platte(), AnimationsOptionen(), THESIS_STIL)
    with pytest.raises(ValueError, match="neu zeichnen"):
        aktualisiere_animation(z, daten, AnimationsOptionen(), Plotstil(schrift_pt=11.0))
    fremd = Figure()
    fremd.add_axes((0, 0, 1, 1))
    with pytest.raises(ValueError, match="nicht von zeichne_animation"):
        aktualisiere_animation(
            Zeichnung(figure=fremd, achsen=()), daten, AnimationsOptionen(), THESIS_STIL
        )


# --- Achsengrenzen und z-Skalierung (E-A5) ----------------------------------------------------


def test_grenzen_unabhaengig_von_theta_und_enthalten_jede_bahn() -> None:
    daten = _platte()
    s = effektive_ueberhoehung(daten, AnimationsOptionen())
    grenzen = achsengrenzen_3d(daten, s)
    fig = Figure(figsize=GROESSE)
    z = zeichne_animation(fig, daten, AnimationsOptionen(), THESIS_STIL)
    ax = _ax(z)
    for theta in np.linspace(0.0, 2.0 * math.pi, 49):
        aktualisiere_animation(z, daten, AnimationsOptionen(theta_rad=float(theta)), THESIS_STIL)
        gesetzt = np.array([ax.get_xlim3d(), ax.get_ylim3d(), ax.get_zlim3d()])
        assert gesetzt == pytest.approx(np.array(grenzen), rel=1e-12)
        pos = daten.positionen(float(theta), s)
        for achse in range(3):
            assert (pos[:, achse] >= grenzen[achse][0]).all()
            assert (pos[:, achse] <= grenzen[achse][1]).all()


def test_ebene_platte_bekommt_mindesthoehe_und_z_enthaelt_s_d_ref() -> None:
    daten = _zwei_punkte()  # alle Punkte auf einer Linie: y und z haben Spanne 0 in der Ruhelage
    assert daten.s_auto is not None
    s = 2.0 * daten.s_auto
    (x0, x1), (y0, y1), (z0, z1) = achsengrenzen_3d(daten, s)
    gross = max(x1 - x0, y1 - y0, z1 - z0)
    assert (y1 - y0) >= MINDESTHOEHE_ANTEIL * (x1 - x0) * (1.0 - 1e-12)
    assert gross == pytest.approx(x1 - x0)
    assert z0 <= -s * daten.d_ref and z1 >= s * daten.d_ref
    assert (z0 + z1) / 2.0 == pytest.approx(0.0, abs=1e-15)  # symmetrisch um die Datenmitte
    # Gleichmaßstab: Box-Verhältnis = Verhältnis der Spannweiten
    fig = Figure(figsize=GROESSE)
    z = zeichne_animation(fig, daten, AnimationsOptionen(ueberhoehung=s), THESIS_STIL)
    aspekt = np.asarray(_ax(z).get_box_aspect())
    spannen = np.array([x1 - x0, y1 - y0, z1 - z0])
    assert aspekt[1] / aspekt[0] == pytest.approx(spannen[1] / spannen[0], rel=1e-9)
    assert aspekt[2] / aspekt[0] == pytest.approx(spannen[2] / spannen[0], rel=1e-9)


def test_grenzen_s_null_und_eingabepruefung() -> None:
    md = messdaten_mit_amplitude(np.array([1e-3]), koordinaten_m=[[0.0, 0.0, 0.0]])
    daten = animation_daten(md, KohaerenzCache(md), 100.0, komponente="Z")
    (x0, x1), _, (z0, z1) = achsengrenzen_3d(daten, 0.0)  # Ruhelage allein ist ein Punkt
    assert x1 > x0 and z1 > z0
    with pytest.raises(ValueError, match="ueberhoehung"):
        achsengrenzen_3d(daten, -1.0)
    with pytest.raises(ValueError, match="ueberhoehung"):
        achsengrenzen_3d(daten, math.nan)


def test_effektive_ueberhoehung() -> None:
    daten = _zwei_punkte()
    assert effektive_ueberhoehung(daten, AnimationsOptionen()) == daten.s_auto
    assert effektive_ueberhoehung(daten, AnimationsOptionen(ueberhoehung=7.0)) == 7.0
    md = messdaten_mit_amplitude(np.array([1e-3]))
    ein = animation_daten(md, KohaerenzCache(md), 100.0, komponente="Z")
    assert ein.s_auto is None
    assert effektive_ueberhoehung(ein, AnimationsOptionen()) == 1.0  # reale Auslenkung


# --- Farbe ----------------------------------------------------------------------------------


def test_farbskala_auto_eingabe_und_fehler() -> None:
    daten = _platte()
    komp, vmin, vmax = farbskala(daten, AnimationsOptionen())
    assert komp == 2  # Ebene xy: senkrechte Achse z
    assert vmin == -vmax and vmax == daten.farbgrenze("auslenkung", 2)
    assert farbskala(daten, AnimationsOptionen(farbe="betrag"))[1:] == (0.0, daten.d_ref)
    assert farbskala(daten, AnimationsOptionen(farb_komponente="X"))[0] == 0
    k, lo, hi = farbskala(daten, AnimationsOptionen(farbbereich=Bereich(-1.0, None)))
    assert (lo, hi) == (-1.0, vmax) and k == 2
    with pytest.raises(ValueError, match="von < bis"):
        farbskala(daten, AnimationsOptionen(farbbereich=Bereich(vmax * 2.0, None)))
    # Einzelkomponente: die gewählte, unabhängig von opt.farb_komponente
    z = _zwei_punkte()
    assert farbskala(z, AnimationsOptionen(farb_komponente="X"))[0] == 2


def test_ui_27_farbleiste_bereich_und_einheit() -> None:
    daten = _zwei_punkte()
    _, z = _zeichne(daten, farbbereich=Bereich(-2e-6, 3e-6))
    assert z.marker["punkte"].get_clim() == (-2e-6, 3e-6)
    assert z.hilfsobjekte["farbtitel"] == "Auslenkung Z [µm]"
    cb = z.hilfsobjekte["farbleiste"]
    cb.ax.figure.canvas.draw()
    ticks = [t.get_text() for t in cb.ax.get_yticklabels() if t.get_text()]
    assert "0" in ticks and any(t.endswith("2") or t.endswith("3") for t in ticks)
    _, betrag = _zeichne(daten, farbe="betrag")
    assert betrag.hilfsobjekte["farbtitel"].startswith("Betrag der Auslenkung [")
    assert betrag.marker["punkte"].get_clim() == (0.0, daten.d_ref)
    # Farbwerte: vorzeichenbehaftet (Auslenkung) bzw. nichtnegativ (Betrag)
    assert (np.asarray(betrag.marker["punkte"].get_array()) >= 0.0).all()


def test_divergierende_skala_helligkeit_streng_monoton() -> None:
    """Das Vorzeichen bleibt in Graustufen lesbar: Luma fällt streng von negativ nach positiv."""
    for stil in (
        THESIS_STIL,
        Plotstil(
            div_negativ=DIVERGIEREND_FARBEN_BUNT[0],
            div_mitte=DIVERGIEREND_FARBEN_BUNT[1],
            div_positiv=DIVERGIEREND_FARBEN_BUNT[2],
        ),
    ):
        rgb = np.asarray(stil.divergierend()(np.linspace(0.0, 1.0, 256)))[:, :3]
        luma = rgb @ np.array([0.2126, 0.7152, 0.0722])  # Rec. 709 auf sRGB-Werte
        assert (np.diff(luma) < 0.0).all()
        assert luma[0] - luma[-1] >= 0.5  # Abstand der Enden (Schwelle, Gestaltungsvorgabe)
    bunt = np.asarray(
        Plotstil(
            div_negativ=DIVERGIEREND_FARBEN_BUNT[0],
            div_mitte=DIVERGIEREND_FARBEN_BUNT[1],
            div_positiv=DIVERGIEREND_FARBEN_BUNT[2],
        ).divergierend()([0.0, 1.0])
    )
    assert bunt[0, 2] > bunt[0, 0]  # negativ: Blauanteil über Rotanteil
    assert bunt[1, 0] > bunt[1, 2]  # positiv: Braun (Rot über Blau); kein Gelb (Blau < Rot, Grün)


def test_farbe_ist_zusaetzlich_formkodiert_und_ruhelage_abschaltbar() -> None:
    daten = _platte()
    _, mit = _zeichne(daten)
    assert np.array_equal(
        np.column_stack(mit.marker["ruhelage"]._offsets3d),
        daten.koordinaten_m,
    )
    assert any(t == "Ruhelage" for t in mit.alle_texte())
    _, ohne = _zeichne(daten, ruhelage=False, punktlabels=True)
    assert "ruhelage" not in ohne.marker
    assert len(ohne.hilfsobjekte["punktlabels"]) == daten.anzahl_punkte
    assert not any(t == "Ruhelage" for t in ohne.alle_texte())


def test_ohne_ruhelage_und_ohne_kennzeichnung_keine_zeichenerklaerung() -> None:
    _, z = _zeichne(_zwei_punkte(), ruhelage=False)
    assert "zeichenerklaerung" not in z.hilfsobjekte
    assert z.hilfsobjekte["anzahl"] == {"unsicher": 0, "ungueltig": 0, "kein_wert": 0}


def test_vereinfachte_achsen() -> None:
    daten = _platte()
    _, z = _zeichne(daten, vereinfacht=True)
    assert not _achse_an(z)
    aktualisiere_animation(z, daten, AnimationsOptionen(vereinfacht=False), THESIS_STIL)
    assert _achse_an(z)


# --- Einheiten, Optionen ----------------------------------------------------------------------


@pytest.mark.parametrize(
    ("wert", "einheit", "faktor", "text"),
    [
        (1.59e-6, "m", 1e6, "µm"),
        (6.9e-3, "m", 1e3, "mm"),
        (2.0, "m", 1.0, "m"),
        (3e-9, "m", 1e9, "nm"),
        (5e-13, "m", 1e12, "pm"),
        (1.59e-3, "m/N", 1e3, "mm/N"),
        (1.59e-6, "m/s", 1e6, "µm/s"),
        (4e-3, "(m/s)/N", 1e3, "(mm/s)/N"),
        (0.0, "m", 1.0, "m"),
        (math.nan, "m", 1.0, "m"),
    ],
)
def test_skaliere_einheit(wert: float, einheit: str, faktor: float, text: str) -> None:
    f, e = skaliere_einheit(wert, einheit)
    assert (f, e) == (faktor, text)


def test_skaliere_einheit_ohne_meter() -> None:
    with pytest.raises(ValueError, match="Meter"):
        skaliere_einheit(1.0, "N")


def test_optionen_pruefung() -> None:
    AnimationsOptionen(theta_rad=7.0, ueberhoehung=0.0)  # θ über 2π ist erlaubt (zustandslos)
    for kw in (
        {"theta_rad": math.nan},
        {"farbe": "rot"},
        {"farb_komponente": "W"},
        {"ueberhoehung": -1.0},
        {"ueberhoehung": math.inf},
        {"farbbereich": Bereich(1.0, 1.0)},
        {"farbbereich": Bereich(math.nan, 1.0)},
        {"farbbereich": Bereich(0.0, math.inf)},
    ):
        with pytest.raises(ValueError, match=r"erwartet|endlich|unbekannt|muss"):
            AnimationsOptionen(**kw)


# --- Standbild speichern (PNG und PDF ohne Zusatz) ---------------------------------------------


def test_standbild_als_png_und_pdf_mit_stempel(tmp_path: Path) -> None:
    daten = _platte()
    opt = AnimationsOptionen(theta_rad=math.pi / 2.0, blick=BLICK_VORGABEN["iso"])
    stempel = baue_stempel(dateiname="probe.svd", ansicht="Animation", git_hash="abc1234")
    for name, magic in (("bild.png", b"\x89PNG"), ("bild.pdf", b"%PDF")):
        pfad = tmp_path / name
        z = speichere_arbeitsbild(
            lambda fig: zeichne_animation(fig, daten, opt, THESIS_STIL), pfad, stempel, THESIS_STIL
        )
        assert pfad.read_bytes()[:4] == magic and pfad.stat().st_size > 1000
        # dieselbe Zeichenfunktion: Positionen = Standbild bei θ
        s = effektive_ueberhoehung(daten, opt)
        assert np.array_equal(
            scatter_positionen(z), daten.positionen(opt.theta_rad, s)[daten.bewegt]
        )
        texte = z.alle_texte()
        assert any("Arbeitsansicht" in t for t in texte)  # nur durch den Stempel
        assert ["θ = 90,0°", "Bezug: relativ zu Punkt 100, Komponente Z"][0] in "\n".join(texte)


def test_zeichnung_ist_deterministisch_in_der_figure_struktur() -> None:
    daten = _platte()
    a = _signatur(_zeichne(daten, theta_rad=1.0)[1])
    b = _signatur(_zeichne(daten, theta_rad=1.0)[1])
    _gleich(a, b)


# --- Textalternative (UI-26, Qt-frei in gui/animation_steuerung) ---------------------------------


def test_textalternative_nennt_faktor_und_pflichtangaben() -> None:
    from ldv_automation.gui.animation_steuerung import beschreibung_animation

    daten = _platte()
    text = beschreibung_animation(daten, math.pi / 2.0, 12.0, THESIS_STIL)
    assert text.startswith(
        "Animation der Betriebsschwingform. Überhöhung \N{MULTIPLICATION SIGN}12,00."
    )
    assert "f = 10,000 Hz · Auslenkung 3D (CPH)" in text
    assert "θ = 90,0°" in text and "Bezug: relativ zu Punkt" in text
    assert f"{daten.anzahl_punkte} Messpunkte" in text
    assert "davon 1 stehend und gekennzeichnet" in text
    assert text.endswith("Standbild.")
    auto = beschreibung_animation(daten, 0.0, None, THESIS_STIL, laeuft=True)
    assert "Überhöhung \N{MULTIPLICATION SIGN}4,383" in auto and auto.endswith("Wiedergabe läuft.")
    ohne = beschreibung_animation(_zwei_punkte(), 0.0, None, THESIS_STIL)
    assert "gekennzeichnet" not in ohne


# --- K-AUSW3-2: Robustheit, Farbnorm, Beschriftung -------------------------------------------


def test_aktualisiere_laesst_das_bild_bei_fehler_unveraendert() -> None:
    """Review MINOR: ungültiger Farbbereich darf keinen halben Bildzustand hinterlassen."""
    daten = _platte()
    fig = Figure(figsize=GROESSE)
    z = zeichne_animation(fig, daten, AnimationsOptionen(theta_rad=0.0), THESIS_STIL)
    vorher = _signatur(z)
    gross = 2.0 * daten.farbgrenze("auslenkung", 2)
    with pytest.raises(ValueError, match="von < bis"):
        aktualisiere_animation(
            z,
            daten,
            AnimationsOptionen(theta_rad=1.5, ueberhoehung=7.0, farbbereich=Bereich(gross, None)),
            THESIS_STIL,
        )
    _gleich(vorher, _signatur(z))
    assert z.hilfsobjekte["optionen"].theta_rad == 0.0
    # zeichne_animation prüft ebenfalls vor dem Leeren der Figure
    with pytest.raises(ValueError, match="von < bis"):
        zeichne_animation(
            fig, daten, AnimationsOptionen(farbbereich=Bereich(gross, None)), THESIS_STIL
        )
    assert len(fig.axes) > 0  # nicht geleert


def test_farb_norm_null_bleibt_neutral_bei_asymmetrischem_bereich() -> None:
    assert isinstance(farb_norm(-1.0, 3.0, divergierend=True), TwoSlopeNorm)
    n = farb_norm(-1.0, 3.0, divergierend=True)
    assert n(0.0) == pytest.approx(0.5) and n(-1.0) == 0.0 and n(3.0) == 1.0
    for lo, hi, div in ((1.0, 3.0, True), (-3.0, -1.0, True), (-1.0, 3.0, False), (0.0, 2.0, True)):
        assert type(farb_norm(lo, hi, divergierend=div)) is Normalize


def test_farbnorm_in_figure_und_aktualisiere_gleich_frisch() -> None:
    daten = _platte()
    _, z = _zeichne(daten, farbbereich=Bereich(-1e-6, 3e-6))
    norm = z.marker["punkte"].norm
    assert isinstance(norm, TwoSlopeNorm) and norm(0.0) == pytest.approx(0.5)
    # Auto (symmetrisch): Null liegt ebenfalls in der Mitte
    _, auto = _zeichne(daten)
    assert auto.marker["punkte"].norm(0.0) == pytest.approx(0.5)
    # Wechsel auf einen Bereich ohne Null und zurück: dieselben Artists, Norm wie frisch
    start = AnimationsOptionen(farbbereich=Bereich(-1e-6, 3e-6))
    zz = zeichne_animation(Figure(figsize=GROESSE), daten, start, THESIS_STIL)
    for bereich in (Bereich(1e-6, 3e-6), Bereich(-2e-6, 1e-6), Bereich()):
        neu = AnimationsOptionen(farbbereich=bereich)
        aktualisiere_animation(zz, daten, neu, THESIS_STIL)
        frisch = zeichne_animation(Figure(figsize=GROESSE), daten, neu, THESIS_STIL)
        assert type(zz.marker["punkte"].norm) is type(frisch.marker["punkte"].norm)
        _gleich(_signatur(zz), _signatur(frisch))


def test_betrag_skala_bleibt_linear() -> None:
    daten = _platte()
    _, z = _zeichne(daten, farbe="betrag")
    assert type(z.marker["punkte"].norm) is Normalize


def test_zeichenerklaerung_gamma_min_mit_gleichheitszeichen() -> None:
    _, z = _zeichne(_platte())
    texte = " ".join(" ".join(z.alle_texte()).split())
    assert "unter γ²_min = 0,9) (1)" in texte


def test_pflichtangaben_der_schnelle_im_bild_und_h1() -> None:
    md = messdaten_mit_amplitude(np.array([1e-3, 0.5e-3]), koordinaten_m=KOORD_2)
    daten = animation_daten(md, KohaerenzCache(md), 100.0, komponente="Z", groesse="schnelle")
    _, z = _zeichne(daten)
    text = " ".join(" ".join(z.alle_texte()).split())
    assert "Skalierung 7,250 s (Bild = Skalierung · Schnelle)" in text
    assert (
        "Überhöhung \N{MULTIPLICATION SIGN}4555" in text
        and "Überhöhung \N{MULTIPLICATION SIGN}7,250" not in text
    )
    assert "Spitzenschnelle D_ref = 1,00 mm/s (Spitzenauslenkung 1,59 µm)" in text
    assert "θ = 0°: Schnelle von Punkt 100, Komponente Z im positiven Maximum" in text
    assert z.hilfsobjekte["skalierung"] == pytest.approx(7.25, abs=5e-7)  # κ in s
    assert z.hilfsobjekte["ueberhoehung"] == pytest.approx(4555.3093, abs=5e-5)  # dimensionslos
    assert z.hinweise == ()
    # H1: je 1 N
    h1 = animation_daten(md, KohaerenzCache(md), 100.0, komponente="Z", quelle="h1")
    assert (
        pflichttexte(h1, 0.0, 1.0, THESIS_STIL)[2] == "f = 100,000 Hz · Auslenkung Z (H1, je 1 N)"
    )
