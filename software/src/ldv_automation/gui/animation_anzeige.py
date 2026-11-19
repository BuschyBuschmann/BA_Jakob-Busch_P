r"""Qt-freie Anzeigelogik der Animation in Ansicht 4 (R-071, Plan P-AUSW3 AN7).

Alles, was die Auswahlspalte (AD), die Bedienleiste (AH), den Kopf und die Meldezeile (AF) der
Animation entscheiden, aber ohne Qt prüfbar ist, steht hier und wird im Standardlauf gemessen:

- Abbildung der Regler auf Werte (Phase, Tempo, Überhöhung als Faktor der automatischen
  Skalierung, logarithmisch) und zurück;
- Eingabe der Skalierung und des Farbbereichs (Dezimalkomma, Potenzschreibweise, leer = Auto,
  Meldungen wie im Brief UI-5) mit der Umrechnung zwischen Anzeigeeinheit (µm, mm/s …) und SI;
- Kopfzeile ``lbl_plotkopf`` mit den Pflichtkennzeichen M8 und M12 (UI-28) und die Textalternative
  mit Datei, Winkel, Überhöhung, Blickrichtung und größter Auslenkung (UI-26).

Die Zeichnung selbst liegt in :mod:`ldv_automation.darstellung.animation3d`, der Winkel, die Uhr
und die Tasten in :mod:`ldv_automation.gui.animation_steuerung`; die Widgets in
:mod:`ldv_automation.gui.auswahl_auswerten` und :mod:`ldv_automation.gui.animationsflaeche`.
"""

from __future__ import annotations

import math
from collections.abc import Iterable, Sequence
from dataclasses import replace
from typing import Literal

from ldv_automation.darstellung.achsen import (
    TEXT_KEINE_ZAHL,
    TEXT_REIHENFOLGE,
    AchsenFehler,
    Bereich,
    feld_text,
    parse_zahl,
)
from ldv_automation.darstellung.animation3d import (
    AnimationsOptionen,
    Blick,
    effektive_ueberhoehung,
    farbskala,
    ist_bestaetigt,
    kennzeichen_texte,
    skaliere_einheit,
)
from ldv_automation.darstellung.animation_daten import TEXT_KEINE_PHASE, AnimationsDaten
from ldv_automation.darstellung.formate import frequenz_text, zahl_text
from ldv_automation.darstellung.stil import Plotstil
from ldv_automation.gui.animation_steuerung import (
    beschreibung_animation,
    phase_text,
    skalierung_text,
)
from ldv_automation.gui.anzeige_auswerten import ABHAENGIG_VON
from ldv_automation.gui.tokens import symbol

__all__ = [
    "BILDRATEN",
    "FAKTOR_MAX",
    "FAKTOR_MIN",
    "FAKTOR_REGLER_MAX",
    "FAKTOR_REGLER_MIN",
    "FARBE_SENKRECHT",
    "PHASE_REGLER_MAX",
    "TEMPO_MAX_HZ",
    "TEMPO_MIN_HZ",
    "TEMPO_REGLER_MAX",
    "TEMPO_REGLER_MIN",
    "TEXT_KEINE_PHASE",
    "TEXT_LANGSAM",
    "TEXT_SKALIERUNG_POSITIV",
    "absolut_text",
    "animations_beschreibung",
    "animations_kopf_text",
    "animations_stempel_zusatz",
    "animations_unbestaetigt",
    "bezug_automatisch_text",
    "bild_vorschlag_zusatz",
    "faktor_aus_regler",
    "farb_anzeige",
    "farb_feldtexte",
    "hinweise_text",
    "lese_farbfeld",
    "lese_skalierung",
    "pruefe_farbbereich",
    "regler_aus_faktor",
    "regler_aus_skalierung",
    "regler_aus_tempo",
    "regler_aus_theta_rad",
    "regler_namen",
    "skalierung_aus_regler",
    "tempo_aus_regler",
    "tempo_text",
    "theta_grad_aus_regler",
]

TEXT_LANGSAM = "Wiedergabe langsamer als eingestellt"
"""Meldung in AF, wenn die Soll-Bildrate nicht erreicht wird (Brief K1-AUSW2 Abschnitt 4)."""
TEXT_SKALIERUNG_POSITIV = "Bitte eine Zahl größer null eingeben (leer = Auto)."
"""Meldung bei einer Skalierung ≤ 0 oder einer Nicht-Zahl (analog UI-5)."""

BILDRATEN: tuple[int, ...] = (5, 10, 20)
"""Wählbare Soll-Bildraten in Bildern je Sekunde (Messpunkt M2, U-A2; vorläufig)."""

FARBE_SENKRECHT: dict[str, str] = {"xy": "Z", "xz": "Y", "yz": "X"}
"""Farbkomponente bei 3D je Projektionsebene: die Achse senkrecht zur Ebene (F-A9)."""

# --- Regler ------------------------------------------------------------------------------------

PHASE_REGLER_MAX = 3599
"""Phasenregler in 0,1°-Schritten: 0 bis 359,9° (UI-24)."""
TEMPO_MIN_HZ = 0.05
TEMPO_MAX_HZ = 2.0
TEMPO_REGLER_MIN = -130
TEMPO_REGLER_MAX = 30
"""Tempo in Perioden je Sekunde, logarithmisch: Regler ``w`` entspricht :math:`10^{w/100}`
(0,05 bis 2 Perioden/s; Zeitlupe, unabhängig von der Messfrequenz)."""
FAKTOR_MIN = 0.1
FAKTOR_MAX = 20.0
FAKTOR_REGLER_MIN = -100
FAKTOR_REGLER_MAX = 130
"""Überhöhung als Faktor der automatischen Skalierung, logarithmisch: Regler ``w`` entspricht
:math:`10^{w/100}` (Faktor 0,1 bis 20, Brief 3.3); ``0`` ist die automatische Skalierung selbst."""


def _regler(wert: float, minimum: int, maximum: int, ersatz: int) -> int:
    """Reglerstand ``round(100·log10(wert))``, begrenzt; ``ersatz`` bei ungültigem Wert."""
    if not math.isfinite(wert) or wert <= 0.0:
        return ersatz
    return min(max(round(100.0 * math.log10(wert)), minimum), maximum)


def theta_grad_aus_regler(wert: int) -> float:
    """Winkel in Grad zum Stand des Phasenreglers (0,1°-Schritte)."""
    return wert / 10.0


def regler_aus_theta_rad(theta_rad: float) -> int:
    """Stand des Phasenreglers zum Winkel; auf 0 bis :data:`PHASE_REGLER_MAX` begrenzt."""
    grad = math.degrees(theta_rad % (2.0 * math.pi))
    return min(max(round(grad * 10.0), 0), PHASE_REGLER_MAX)


def tempo_aus_regler(wert: int) -> float:
    """Tempo in Perioden je Sekunde zum Stand des Tempo-Reglers."""
    return float(10.0 ** (min(max(wert, TEMPO_REGLER_MIN), TEMPO_REGLER_MAX) / 100.0))


def regler_aus_tempo(tempo_hz: float) -> int:
    """Stand des Tempo-Reglers zum Tempo (begrenzt; ungültig: langsamste Stellung)."""
    return _regler(tempo_hz, TEMPO_REGLER_MIN, TEMPO_REGLER_MAX, TEMPO_REGLER_MIN)


def tempo_text(tempo_hz: float, *, kompakt: bool = False) -> str:
    """Anzeige des Tempos mit Dezimalkomma, z. B. „0,25 Perioden/s“ (zwei signifikante Stellen).

    Kompakt (Fenster unter 1200 px, UI-D3): „0,25/s“; die Einheit „Perioden“ steht im Tooltip.
    """
    stellen = 1 if tempo_hz >= 1.0 else 2
    einheit = "/s" if kompakt else " Perioden/s"
    return f"{zahl_text(tempo_hz, stellen, dezimalkomma=True)}{einheit}"


def faktor_aus_regler(wert: int) -> float:
    """Faktor der automatischen Skalierung zum Stand des Überhöhungsreglers."""
    return float(10.0 ** (min(max(wert, FAKTOR_REGLER_MIN), FAKTOR_REGLER_MAX) / 100.0))


def regler_aus_faktor(faktor: float) -> int:
    """Stand des Überhöhungsreglers zum Faktor (begrenzt; ungültig: Mitte = Auto)."""
    return _regler(faktor, FAKTOR_REGLER_MIN, FAKTOR_REGLER_MAX, 0)


def skalierung_aus_regler(wert: int, s_auto: float | None) -> float | None:
    """Skalierung zum Reglerstand: ``None`` (automatisch) bei Faktor 1 oder ohne Autowert.

    Ohne automatische Skalierung (ein einziger Punkt, kein Nachbarabstand) hat der Faktor keine
    Bezugsgröße; der Regler ist dann gesperrt und die Skalierung kommt aus dem Eingabefeld.
    """
    if wert == 0 or s_auto is None:
        return None
    return faktor_aus_regler(wert) * s_auto


def regler_aus_skalierung(skalierung: float | None, s_auto: float | None) -> int:
    """Reglerstand zur Skalierung (``0``, wenn automatisch oder ohne Autowert)."""
    if skalierung is None or s_auto is None or not s_auto > 0.0:
        return 0
    return regler_aus_faktor(skalierung / s_auto)


# --- Eingaben ----------------------------------------------------------------------------------


def lese_skalierung(text: str) -> float | None:
    r"""Liest das Feld „Skalierung“: leer = ``None`` (automatisch), sonst eine Zahl > 0.

    Auslenkung: Überhöhung :math:`s`; Schnelle: Skalierung :math:`\kappa` in s (FG-04 Nachtrag 2).

    Raises
    ------
    AchsenFehler
        Keine Zahl (:data:`~ldv_automation.darstellung.achsen.TEXT_KEINE_ZAHL`) oder Wert ≤ 0
        (:data:`TEXT_SKALIERUNG_POSITIV`).
    """
    wert = parse_zahl(text)
    if wert is None:
        return None
    if not wert > 0.0:
        raise AchsenFehler(TEXT_SKALIERUNG_POSITIV, "skalierung")
    return wert


def farb_anzeige(daten: AnimationsDaten, opt: AnimationsOptionen) -> tuple[float, str]:
    """Anzeigefaktor und Einheit der Farbfelder (``Wert in Einheit = SI-Wert · Faktor``).

    Der Faktor folgt der **automatischen** Grenze der Farbgröße (nicht der Eingabe), damit eine
    eingetippte Zahl ihre Einheit behält. Die Farbleiste im Bild wählt ihre Einheit nach der
    wirksamen Grenze selbst.
    """
    _komp, vmin, vmax = farbskala(daten, replace(opt, farbbereich=Bereich()))
    return skaliere_einheit(max(abs(vmin), abs(vmax)), daten.einheit_anim)


def lese_farbfeld(text: str, seite: str, alt: Bereich, faktor: float) -> Bereich:
    """Neuer Farbbereich (SI) aus dem Text eines Felds („von“ oder „bis“, Anzeigeeinheit).

    Parameters
    ----------
    text : str
        Eingabe des Felds; leer = Auto.
    seite : {"von", "bis"}
        Das Feld, aus dem der Text stammt.
    alt : Bereich
        Bisheriger Bereich in SI.
    faktor : float
        Anzeigefaktor (:func:`farb_anzeige`).

    Raises
    ------
    AchsenFehler
        Keine Zahl; beide Seiten gesetzt und „von“ ≥ „bis“
        (:data:`~ldv_automation.darstellung.achsen.TEXT_REIHENFOLGE`).
    """
    wert = parse_zahl(text)
    si = None if wert is None else wert / faktor
    if si is not None and not math.isfinite(si):
        raise AchsenFehler(TEXT_KEINE_ZAHL, "farbbereich")
    neu = Bereich(si, alt.bis) if seite == "von" else Bereich(alt.von, si)
    if neu.von is not None and neu.bis is not None and neu.von >= neu.bis:
        raise AchsenFehler(TEXT_REIHENFOLGE, "farbbereich")
    return neu


def pruefe_farbbereich(daten: AnimationsDaten, opt: AnimationsOptionen, bereich: Bereich) -> None:
    """Prüft den Bereich gegen die automatische Gegenseite (gemischter Bereich).

    Raises
    ------
    AchsenFehler
        Eine Seite gesetzt, die andere automatisch, und „von“ ≥ „bis“ (die Zeichenfunktion
        lehnt das ab).
    """
    try:
        farbskala(daten, replace(opt, farbbereich=bereich))
    except ValueError:
        raise AchsenFehler(TEXT_REIHENFOLGE, "farbbereich") from None


def farb_feldtexte(bereich: Bereich, faktor: float) -> tuple[str, str]:
    """Texte der Felder „von“ und „bis“ (Anzeigeeinheit, 4 signifikante Stellen; leer = Auto)."""

    def text(wert: float | None) -> str:
        return "" if wert is None else feld_text(wert * faktor)

    return text(bereich.von), text(bereich.bis)


# --- Texte -------------------------------------------------------------------------------------


def absolut_text(referenz: str, annahmen: Iterable[object]) -> str:
    """Beschriftung „Absolut gegen Ref1 (⚠ unbestätigt, M8)“; ohne Zusatz bei bestätigtem M8.

    Wie das Bild (:func:`~ldv_automation.darstellung.animation3d.kennzeichen_texte`) gilt ein
    Status nur mit ausdrücklichem Bestätigungsvermerk („bestätigt …“) als bestätigt.
    """
    phase_nr = {nr for nr, _text in ABHAENGIG_VON.get("phase", ())}
    offen = tuple(
        a
        for a in annahmen
        if getattr(a, "nr", None) in phase_nr and not ist_bestaetigt(a)  # type: ignore[arg-type]
    )
    if not offen:
        return f"Absolut gegen {referenz}"
    nummern = ", ".join(a.nr for a in offen)  # type: ignore[attr-defined]
    return f"Absolut gegen {referenz} ({symbol('warnung')} unbestätigt, {nummern})"


def bezug_automatisch_text(daten: AnimationsDaten | None) -> str:
    """Eintrag „Automatisch (Punkt 17)“ der Bezugspunktwahl nach den Daten der Animation."""
    if daten is None or daten.bezug_index is None:
        return "Automatisch (größtes |v|, γ² ≥ γ²_min)"
    return f"Automatisch (Punkt {int(daten.label[daten.bezug_index])})"


def hinweise_text(daten: AnimationsDaten, hinweise: Sequence[str]) -> str:
    """Hinweise der Animation für AD: Überlagerung, doppelte Punkte (zeilenweise)."""
    zeilen = [*hinweise]
    if daten.hinweis_duplikate:
        zeilen.append(daten.hinweis_duplikate)
    return "\n".join(zeilen)


def animations_kopf_text(
    dateiname: str,
    daten: AnimationsDaten,
    opt: AnimationsOptionen,
    stil: Plotstil,
    *,
    kompakt: bool = False,
) -> str:
    """Kopfzeile über der Animation: Datei · Linie · Größe/Quelle · Phasenbezug · Kennzeichen.

    Die Kennzeichen M8 (nur bei absolutem Bezug) und M12 (3D) stehen **dauerhaft** im Kopf, solange
    sie nicht als bestätigt geführt werden, und folgen derselben Regel wie das Bild
    (:func:`~ldv_automation.darstellung.animation3d.kennzeichen_texte`, UI-28). In der kompakten
    Darstellung (< 1200 px, KONVENTIONEN) stehen nur „⚠ M8“ und „⚠ M12“; der Langtext steht im
    Tooltip des Kopfes (:func:`animations_kopf_tooltip`) und vollständig im Kasten des Bildes.
    """
    komma = stil.dezimalkomma
    groesse = "Schnelle" if daten.groesse == "schnelle" else "Auslenkung"
    quelle = "H1" if daten.quelle == "h1" else "CPH"
    if daten.bezug_modus == "relativ" and daten.bezug_index is not None:
        bezug = f"Phase relativ zu Punkt {int(daten.label[daten.bezug_index])}"
    else:
        bezug = f"Phase gegen {daten.referenz or 'Referenz'}"
    teile = [
        dateiname,
        f"Linie {frequenz_text(daten.f_hz, 3, dezimalkomma=komma)}",
        f"Animation {groesse} {daten.komponente} ({quelle})",
        bezug,
    ]
    phase, koordinaten = kennzeichen_texte(daten, opt)
    if kompakt:
        teile.extend(
            f"{symbol('warnung')} {kurz}"
            for kurz, text in (("M8", phase), ("M12", koordinaten))
            if text
        )
    else:
        teile.extend(f"{symbol('warnung')} {t}" for t in (phase, koordinaten) if t)
    return " · ".join(teile)


def animations_kopf_tooltip(daten: AnimationsDaten, opt: AnimationsOptionen) -> str:
    """Langtext der Kennzeichen für den Tooltip des Kopfes (leer ohne Kennzeichen)."""
    return "\n".join(f"{symbol('warnung')} {t}" for t in kennzeichen_texte(daten, opt) if t)


def _blick_text(blick: Blick, stil: Plotstil) -> str:
    komma = stil.dezimalkomma
    return (
        f"Blickrichtung: Azimut {zahl_text(blick.azim_grad, 1, dezimalkomma=komma)}°, "
        f"Elevation {zahl_text(blick.elev_grad, 1, dezimalkomma=komma)}°, "
        f"Zoom {zahl_text(blick.zoom, 2, dezimalkomma=komma)}"
    )


def animations_beschreibung(
    dateiname: str,
    daten: AnimationsDaten,
    opt: AnimationsOptionen,
    stil: Plotstil,
    *,
    laeuft: bool = False,
) -> str:
    """Textalternative des 3D-Plots (``accessibleDescription``, UI-26).

    Nennt Datei, Frequenz, Phasenwinkel, Überhöhung bzw. Skalierung, größte Auslenkung, Bezug,
    Kennzeichen und die Blickrichtung (:func:`~.animation_steuerung.beschreibung_animation` plus
    Datei und Blick).
    """
    text = beschreibung_animation(
        daten,
        opt.theta_rad,
        opt.ueberhoehung,
        stil,
        laeuft=laeuft,
        kennzeichen_phase=opt.kennzeichen_phase,
        kennzeichen_koordinaten=opt.kennzeichen_koordinaten,
    )
    return f"Datei {dateiname}. {text} {_blick_text(opt.blick, stil)}."


# --- Standbild speichern (AN8, UI-31) ------------------------------------------------------------


def animations_stempel_zusatz(
    daten: AnimationsDaten, opt: AnimationsOptionen, stil: Plotstil
) -> tuple[str, ...]:
    """Zusatzzeilen des Bildstempels: Winkel, Frequenz, Überhöhung/Skalierung, Blick (UI-31).

    ``opt`` trägt den Winkel und den Blick des gespeicherten Standbilds
    (:attr:`.AnimationsFlaeche.standbild_optionen`). Die Zeilen ergänzen die Kopfzeile des
    Stempels (Datei, Ansicht, Git-Hash) in :func:`~ldv_automation.darstellung.bild.baue_stempel`.
    """
    komma = stil.dezimalkomma
    skalierung = skalierung_text(daten, effektive_ueberhoehung(daten, opt), stil)
    name = "Skalierung" if daten.groesse == "schnelle" else "Überhöhung"
    return (
        f"Animation · {phase_text(opt.theta_rad, stil)} · "
        f"f = {frequenz_text(daten.f_hz, 3, dezimalkomma=komma)} · {name} {skalierung}",
        _blick_text(opt.blick, stil),
    )


def animations_unbestaetigt(daten: AnimationsDaten, opt: AnimationsOptionen) -> tuple[str, ...]:
    """Nummern der offenen Annahmen, deren Kennzeichen im Bild stehen (M8, M12; UI-28).

    Dieselbe Quelle wie das Bild und der Kopf
    (:func:`~ldv_automation.darstellung.animation3d.kennzeichen_texte`): fail-closed, ein Status
    gilt nur mit Bestätigungsvermerk als bestätigt.
    """
    phase, koordinaten = kennzeichen_texte(daten, opt)
    return tuple(nr for nr, text in (("M8", phase), ("M12", koordinaten)) if text)


def bild_vorschlag_zusatz(theta_rad: float) -> str:
    """Namenszusatz des Dateivorschlags im Modus Animation, z. B. ``_animation_theta090``."""
    grad = round(math.degrees(theta_rad % (2.0 * math.pi))) % 360
    return f"_animation_theta{grad:03d}"


def regler_namen(art: Literal["abspielen", "pause"]) -> tuple[str, str]:
    """Text und ``accessibleName`` des Abspielen-Knopfs je Zustand (Text, nicht nur Symbol)."""
    if art == "pause":
        return "Pause", "Animation anhalten"
    return "Abspielen", "Animation abspielen"
