"""Qt-freie Steuerung der 3D-Animation (R-071, Plan P-AUSW3 AN5): UI-22, UI-24, UI-32, F-A3, F-A4.

Der Standardlauf prüft die Logik ohne Qt; Zeit kommt aus einer injizierten Uhr, nichts hängt von
der echten Zeit ab. Winkel intern in rad, Anzeige in Grad.
"""

from __future__ import annotations

import math

import pytest

from ldv_automation.darstellung.animation3d import BLICK_VORGABEN
from ldv_automation.darstellung.stil import THESIS_STIL
from ldv_automation.gui.animation_steuerung import (
    ANIMATIONS_TASTEN,
    DREH_SCHRITT_GRAD,
    GRAD_JE_PIXEL,
    STUFE_VORGABE,
    ZOOM_MAX,
    ZOOM_MIN,
    Aktion,
    Blickzustand,
    Ereignis,
    Phasenuhr,
    Stufe,
    frequenzwechsel,
    optionen_stufe,
    phase_text,
    taste_zu_aktion,
    ueberhoehung_text,
    verhalten,
    wende_an,
)


class Uhr:
    """Von Hand gestellte Zeitquelle (s)."""

    def __init__(self) -> None:
        self.t = 100.0

    def __call__(self) -> float:
        return self.t


def _uhr(tempo_hz: float = 1.0) -> tuple[Phasenuhr, Uhr]:
    z = Uhr()
    return Phasenuhr(z, tempo_hz=tempo_hz), z


# --- Phasenuhr: Umlauf aus der Uhr (UI-24) -----------------------------------------------------


def test_nach_einer_viertelperiode_ist_theta_90_grad() -> None:
    p, z = _uhr(1.0)
    p.start()
    z.t += 0.25
    assert p.tick() == pytest.approx(math.pi / 2.0, abs=1e-12)
    assert p.theta_grad == pytest.approx(90.0, abs=1e-9)
    z.t += 0.25
    assert p.tick() == pytest.approx(math.pi, abs=1e-12)


def test_ausgelassene_bilder_aendern_die_phase_nicht() -> None:
    """E-A4: θ folgt der Uhr, nicht der Zahl der Takte."""
    a, za = _uhr(0.25)
    b, zb = _uhr(0.25)
    a.start()
    b.start()
    for _ in range(50):  # a: 50 Takte à 0,1 s
        za.t += 0.1
        a.tick()
    zb.t += 5.0  # b: ein einziges Bild nach 5 s (alle anderen ausgelassen)
    assert b.tick() == pytest.approx(a.tick(), abs=1e-9)
    assert b.tick() == pytest.approx(2.0 * math.pi * 0.25 * 5.0 % (2.0 * math.pi), abs=1e-9)


def test_umlauf_bleibt_im_wertebereich_und_pause_haelt_an() -> None:
    p, z = _uhr(1.0)
    p.start()
    z.t += 3.3  # drei volle Perioden und 0,3
    theta = p.pause()
    assert 0.0 <= theta < 2.0 * math.pi
    assert theta == pytest.approx(2.0 * math.pi * 0.3, abs=1e-9)
    assert not p.laeuft
    z.t += 10.0  # die Uhr läuft weiter, der Winkel nicht
    assert p.tick() == theta
    p.start()
    z.t += 0.2
    assert p.tick() == pytest.approx(2.0 * math.pi * 0.5, abs=1e-9)  # setzt fort, kein Sprung


def test_umschalten_leertaste() -> None:
    p, z = _uhr()
    assert p.umschalten() is True and p.laeuft
    z.t += 0.1
    assert p.umschalten() is False and not p.laeuft
    assert p.theta_rad == pytest.approx(2.0 * math.pi * 0.1, abs=1e-12)
    p.start()
    p.start()  # doppeltes Starten setzt die Bezugszeit nicht neu
    z.t += 0.1
    assert p.tick() == pytest.approx(2.0 * math.pi * 0.2, abs=1e-12)


def test_tick_ohne_wiedergabe_aendert_nichts() -> None:
    p, z = _uhr()
    z.t += 5.0
    assert p.tick() == 0.0


# --- Einzelschritte (UI-24, UI-32) -------------------------------------------------------------


def test_einzelschritt_ist_die_schrittweite() -> None:
    p, _ = _uhr()
    assert p.schritt_grad == 10.0
    p.schritt(+1)
    assert p.theta_grad == pytest.approx(10.0, abs=1e-12)
    p.schritt(+1)
    p.schritt(-1)
    assert p.theta_grad == pytest.approx(10.0, abs=1e-12)
    # 36 Schritte à 10° ergeben genau einen Umlauf (E3: 36 Bilder je Periode)
    q, _ = _uhr()
    for _ in range(36):
        q.schritt(+1)
    assert q.theta_rad == pytest.approx(0.0, abs=1e-12) or q.theta_rad == pytest.approx(
        2.0 * math.pi, abs=1e-12
    )


def test_schritt_zurueck_umbricht_bei_null_und_schrittweite_aenderbar() -> None:
    p, _ = _uhr()
    p.schritt(-1)
    assert p.theta_grad == pytest.approx(350.0, abs=1e-12)
    p.setze_schritt_grad(25.0)
    assert p.schritt_grad == 25.0
    p.schritt(+1)
    assert p.theta_grad == pytest.approx(15.0, abs=1e-12)
    p.schritt(+1, 90.0)  # Strg+Pfeil: grob
    assert p.theta_grad == pytest.approx(105.0, abs=1e-12)


def test_schritt_haelt_die_wiedergabe_an() -> None:
    p, z = _uhr()
    p.start()
    z.t += 0.1
    p.schritt(+1)
    assert not p.laeuft
    assert p.theta_grad == pytest.approx(36.0 + 10.0, abs=1e-9)


# --- Regler, Tempo, Zurücksetzen --------------------------------------------------------------


def test_regler_setzt_winkel_und_wiedergabe_laeuft_von_dort_weiter() -> None:
    p, z = _uhr(1.0)
    p.start()
    z.t += 0.1
    p.setze_theta_grad(180.0)
    assert p.theta_grad == pytest.approx(180.0, abs=1e-9)
    z.t += 0.25
    assert p.tick() == pytest.approx(math.pi + math.pi / 2.0, abs=1e-9)
    p.setze_theta_rad(-math.pi / 2.0)  # negativ → 270°
    assert p.theta_grad == pytest.approx(270.0, abs=1e-9)
    with pytest.raises(ValueError, match="endlich"):
        p.setze_theta_rad(math.nan)


def test_tempoaenderung_bewahrt_den_verlauf() -> None:
    p, z = _uhr(1.0)
    p.start()
    z.t += 0.25
    p.setze_tempo(2.0)  # bis hierher 90°
    assert p.tempo_hz == 2.0
    z.t += 0.125  # 0,125 s bei 2 Hz = 90°
    assert p.tick() == pytest.approx(math.pi, abs=1e-9)


def test_zuruecksetzen() -> None:
    p, z = _uhr()
    p.start()
    z.t += 0.3
    p.zuruecksetzen()
    assert not p.laeuft and p.theta_rad == 0.0


@pytest.mark.parametrize("tempo", [0.0, -1.0, math.nan, math.inf])
def test_ungueltiges_tempo(tempo: float) -> None:
    with pytest.raises(ValueError, match="tempo_hz"):
        Phasenuhr(Uhr(), tempo_hz=tempo)
    p, _ = _uhr()
    with pytest.raises(ValueError, match="tempo_hz"):
        p.setze_tempo(tempo)


@pytest.mark.parametrize("grad", [0.0, -5.0, 360.5, math.nan])
def test_ungueltige_schrittweite(grad: float) -> None:
    with pytest.raises(ValueError, match="Schrittweite"):
        Phasenuhr(Uhr(), schritt_grad=grad)
    p, _ = _uhr()
    with pytest.raises(ValueError, match="Schrittweite"):
        p.setze_schritt_grad(grad)
    with pytest.raises(ValueError, match="Schrittweite"):
        p.schritt(+1, grad)


def test_schritt_vorzeichen_pruefung() -> None:
    p, _ = _uhr()
    with pytest.raises(ValueError, match="vorzeichen"):
        p.schritt(2)


def test_voreinstellungen_der_uhr() -> None:
    p = Phasenuhr()  # echte monotone Uhr, ohne sie abzufragen
    assert p.tempo_hz == 0.25 and p.schritt_grad == 10.0 and not p.laeuft


# --- Blickzustand (UI-23) ----------------------------------------------------------------------


def test_blickvorgaben_und_zuruecksetzen() -> None:
    b = Blickzustand()
    assert b.blick == BLICK_VORGABEN["xy"] and b.vorgabe == "xy"
    for name in ("xz", "yz", "iso", "xy"):
        assert b.waehle_vorgabe(name) == BLICK_VORGABEN[name]
    b.waehle_vorgabe("iso")
    b.drehen_grad(40.0, -10.0)
    b.zoomen(5.0)
    assert b.blick != BLICK_VORGABEN["iso"]
    assert b.zuruecksetzen() == BLICK_VORGABEN["iso"]  # Pos1: Blick und Zoom zurück
    with pytest.raises(ValueError, match="Blickvorgabe"):
        b.waehle_vorgabe("oben")


def test_drehen_mit_der_maus_vorzeichen_und_grenzen() -> None:
    b = Blickzustand("iso")
    start = b.blick
    b.drehen_pixel(100.0, 0.0)
    assert b.blick.azim_grad == pytest.approx(start.azim_grad + 100.0 * GRAD_JE_PIXEL)
    assert b.blick.elev_grad == start.elev_grad
    b.drehen_pixel(0.0, 10.0)  # Ziehen nach unten verkleinert die Elevation
    assert b.blick.elev_grad == pytest.approx(start.elev_grad - 10.0 * GRAD_JE_PIXEL)
    b.drehen_pixel(0.0, -1e6)
    assert b.blick.elev_grad == 90.0
    b.drehen_pixel(0.0, 1e6)
    assert b.blick.elev_grad == -90.0


def test_azimut_wird_normiert() -> None:
    b = Blickzustand("xy")  # -90°
    b.drehen_grad(-100.0, 0.0)
    assert b.blick.azim_grad == pytest.approx(170.0)
    b.drehen_grad(360.0 * 3 + 20.0, 0.0)
    assert -180.0 < b.blick.azim_grad <= 180.0
    assert b.blick.azim_grad == pytest.approx(-170.0)
    b.drehen_grad(10.0, 0.0)
    assert b.blick.azim_grad == pytest.approx(-160.0)
    c = Blickzustand("yz")  # azim 0
    c.drehen_grad(180.0, 0.0)
    assert c.blick.azim_grad == pytest.approx(180.0)  # 180 statt -180: Bereich (-180, 180]


def test_zoom_grenzen_und_faktor() -> None:
    b = Blickzustand()
    assert b.zoomen(1.0).zoom == pytest.approx(1.1)
    assert b.zoomen(-1.0).zoom == pytest.approx(1.0)
    assert b.zoomen(1e3).zoom == ZOOM_MAX
    assert b.zoomen(-1e3).zoom == ZOOM_MIN
    with pytest.raises(ValueError, match="rasten"):
        b.zoomen(math.nan)
    with pytest.raises(ValueError, match="endlich"):
        b.drehen_grad(math.inf, 0.0)


# --- Tasten (F-A3, UI-32) ----------------------------------------------------------------------


@pytest.mark.parametrize(
    ("taste", "mods", "aktion"),
    [
        ("Space", frozenset(), Aktion.ABSPIELEN),
        ("Left", frozenset(), Aktion.PHASE_ZURUECK),
        ("Right", frozenset(), Aktion.PHASE_VOR),
        ("Up", frozenset(), Aktion.ELEVATION_PLUS),
        ("Down", frozenset(), Aktion.ELEVATION_MINUS),
        ("Left", frozenset({"shift"}), Aktion.AZIMUT_MINUS),
        ("Right", frozenset({"shift"}), Aktion.AZIMUT_PLUS),
        ("Left", frozenset({"ctrl"}), Aktion.PHASE_ZURUECK_GROB),
        ("Right", frozenset({"ctrl"}), Aktion.PHASE_VOR_GROB),
        ("+", frozenset(), Aktion.ZOOM_PLUS),
        ("-", frozenset(), Aktion.ZOOM_MINUS),
        ("Home", frozenset(), Aktion.ANSICHT_ZURUECK),
    ],
)
def test_ui_32_tastenabbildung(taste: str, mods: frozenset[str], aktion: Aktion) -> None:
    assert taste_zu_aktion(taste, mods) is aktion


def test_pfeiltasten_aendern_die_phase_nicht_den_blick() -> None:
    """F-A3: ←/→ gehören der Phase; das Drehen bekommt Umschalt+Pfeile und ↑/↓."""
    assert taste_zu_aktion("Left") is Aktion.PHASE_ZURUECK
    assert taste_zu_aktion("Left", frozenset({"shift"})) is Aktion.AZIMUT_MINUS


@pytest.mark.parametrize(
    ("taste", "mods"),
    [
        ("Left", frozenset({"alt"})),
        ("Left", frozenset({"shift", "ctrl"})),
        ("Up", frozenset({"shift"})),
        ("Space", frozenset({"ctrl"})),
        ("x", frozenset()),
        ("F5", frozenset()),
    ],
)
def test_nicht_belegte_tasten(taste: str, mods: frozenset[str]) -> None:
    assert taste_zu_aktion(taste, mods) is None


def test_tasten_nur_mit_fokus_und_im_modus_animation() -> None:
    assert taste_zu_aktion("Space", fokus=False) is None
    assert taste_zu_aktion("Space", modus_animation=False) is None
    assert taste_zu_aktion("Space", fokus=False, modus_animation=False) is None


def test_tooltip_tabelle_vollstaendig_und_eindeutig() -> None:
    assert set(ANIMATIONS_TASTEN) == set(Aktion)
    tasten = [t for t, _ in ANIMATIONS_TASTEN.values()]
    assert len(set(tasten)) == len(tasten)
    assert ANIMATIONS_TASTEN[Aktion.ANSICHT_ZURUECK] == ("Home", "Pos1")
    assert ANIMATIONS_TASTEN[Aktion.PHASE_VOR][1] == "→"


def test_wende_an_wirkt_auf_phase_und_blick_pos1_nur_auf_den_blick() -> None:
    p, z = _uhr()
    b = Blickzustand("iso")
    wende_an(Aktion.ABSPIELEN, p, b)
    assert p.laeuft
    wende_an(Aktion.ABSPIELEN, p, b)
    assert not p.laeuft
    wende_an(Aktion.PHASE_VOR, p, b)
    wende_an(Aktion.PHASE_VOR, p, b)
    wende_an(Aktion.PHASE_ZURUECK, p, b)
    assert p.theta_grad == pytest.approx(10.0)
    wende_an(Aktion.PHASE_VOR_GROB, p, b)
    assert p.theta_grad == pytest.approx(100.0)
    wende_an(Aktion.PHASE_ZURUECK_GROB, p, b)
    assert p.theta_grad == pytest.approx(10.0)
    start = b.blick
    wende_an(Aktion.ELEVATION_PLUS, p, b)
    assert b.blick.elev_grad == pytest.approx(start.elev_grad + DREH_SCHRITT_GRAD)
    wende_an(Aktion.ELEVATION_MINUS, p, b)
    wende_an(Aktion.AZIMUT_PLUS, p, b)
    assert b.blick.azim_grad == pytest.approx(start.azim_grad + DREH_SCHRITT_GRAD)
    wende_an(Aktion.AZIMUT_MINUS, p, b)
    wende_an(Aktion.ZOOM_PLUS, p, b)
    assert b.blick.zoom == pytest.approx(1.1)
    wende_an(Aktion.ZOOM_MINUS, p, b)
    assert b.blick == start
    wende_an(Aktion.AZIMUT_PLUS, p, b)
    wende_an(Aktion.ZOOM_PLUS, p, b)
    theta_vorher = p.theta_rad
    wende_an(Aktion.ANSICHT_ZURUECK, p, b)
    assert b.blick == BLICK_VORGABEN["iso"]
    assert p.theta_rad == theta_vorher  # Pos1 setzt weder Winkel noch Überhöhung zurück
    assert z.t == 100.0


# --- Rückfallstufen (ADR-029, Plan 4.3) --------------------------------------------------------


def test_stufen_tabelle() -> None:
    assert STUFE_VORGABE is Stufe.L0
    # L0: vereinfachte Achsen nur in Bewegung (Wiedergabe, Drehen), im Stand nie
    assert optionen_stufe(Stufe.L0, Ereignis.WIEDERGABE)
    assert optionen_stufe(Stufe.L0, Ereignis.DREHEN)
    assert not optionen_stufe(Stufe.L0, Ereignis.REGLER)
    assert not optionen_stufe(Stufe.L0, Ereignis.STAND)
    # L1: auch beim Ziehen des Reglers
    assert optionen_stufe(Stufe.L1, Ereignis.REGLER)
    assert not optionen_stufe(Stufe.L1, Ereignis.STAND)
    # L2: zusätzlich Neuzeichnen beim Loslassen, keine Wiedergabe
    assert optionen_stufe(Stufe.L2, Ereignis.REGLER)
    assert not optionen_stufe(Stufe.L2, Ereignis.STAND)
    assert verhalten(Stufe.L0).wiedergabe and verhalten(Stufe.L1).wiedergabe
    assert not verhalten(Stufe.L2).wiedergabe
    assert [verhalten(s).neuzeichnen_beim_loslassen for s in Stufe] == [False, False, True]


def test_stufen_nur_l0_bis_l2() -> None:
    assert [s.name for s in Stufe] == ["L0", "L1", "L2"]  # L3 gehört nicht zum Umfang


# --- Zustände (F-A4, UI-22) und Anzeigeformate -------------------------------------------------


def test_frequenzwechsel_fuehrt_ins_standbild_und_startet_nie_selbst() -> None:
    p, z = _uhr()
    p.start()
    z.t += 0.3
    assert frequenzwechsel(p) == "standbild"
    assert not p.laeuft and p.theta_rad == 0.0
    z.t += 5.0
    assert p.tick() == 0.0  # läuft nicht von allein weiter (UI-22)


@pytest.mark.parametrize(
    ("theta", "text"),
    [
        (0.0, "θ = 0,0°"),
        (math.pi / 2.0, "θ = 90,0°"),
        (math.radians(12.34), "θ = 12,3°"),
        (-math.pi / 2.0, "θ = 270,0°"),
        (2.0 * math.pi + 0.1, "θ = 5,7°"),
        (math.radians(359.96), "θ = 0,0°"),  # rundet auf 360 → 0
    ],
)
def test_phase_text_grad_mit_dezimalkomma(theta: float, text: str) -> None:
    assert phase_text(theta) == text
    assert phase_text(theta, THESIS_STIL) == text


def test_phase_text_mit_dezimalpunkt() -> None:
    from ldv_automation.darstellung.stil import Plotstil

    assert phase_text(math.pi / 2.0, Plotstil(dezimalkomma=False)) == "θ = 90.0°"


def test_ueberhoehung_text_vier_signifikante_stellen() -> None:
    assert ueberhoehung_text(4555.3093477) == "\N{MULTIPLICATION SIGN}4555"
    assert ueberhoehung_text(2.0) == "\N{MULTIPLICATION SIGN}2,000"
    assert ueberhoehung_text(1.5e7, THESIS_STIL) == "\N{MULTIPLICATION SIGN}1,500·10⁷"
