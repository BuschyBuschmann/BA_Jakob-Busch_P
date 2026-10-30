r"""Spitzensuche auf |H1| und -3-dB-Breite (FG-02 3.9, A-6, R-053).

Eingang :math:`y_k = |H_{1,k}|` eines Punkts oder eines Punktmittels, dazu γ².

1. **Kandidaten:** :math:`y_k > y_{k-1}` und :math:`y_k \ge y_{k+1}` für
   :math:`1 \le k \le K-2` (Randlinien nie); Prominenz
   :math:`y_k \ge p_\mathrm{min}\max(\min_{[k-W,k)} y,\ \min_{(k,k+W]} y)` (an den Rändern
   gekürzte Fenster); :math:`f_k \ge f_\mathrm{min}`.
2. **Parabel durch drei Linien:**
   :math:`\delta = \tfrac12 (y_{k-1}-y_{k+1})/(y_{k-1}-2y_k+y_{k+1})`,
   :math:`f_\mathrm{sp} = f_k + \delta\Delta f`,
   :math:`\hat y = y_k - \tfrac14 (y_{k-1}-y_{k+1})\delta`; Nenner >= 0 → δ = 0.
3. **-3-dB-Breite:** Schwelle :math:`\hat y/\sqrt2`; von k nach außen bis
   :math:`y_j` < Schwelle, lineare Interpolation; ein lokales Minimum über der Schwelle oder
   das Achsenende macht die Seite unbestimmt (``ueberlappend``, B = NaN).
   :math:`B = f_r - f_l`, :math:`Q = f_\mathrm{sp}/B`, :math:`\zeta = B/(2f_\mathrm{sp})`.

Für die Mobilität des Einmassenschwingers ist :math:`B = 2\zeta f_n` exakt [A]. Die
Ausgabe heißt ``breite_3db_hz``, nicht „Dämpfung“. Die Schritte folgen dem Prüfskript im
Anhang von FG-02 (``peak_est``).
"""

from __future__ import annotations

import math
from dataclasses import dataclass

import numpy as np
import numpy.typing as npt

from .annahmen import AnnahmeEintrag, Annahmen, Schwellen
from .daten import FloatArray

GRENZE_VERFAHREN = (
    "Zwei Moden, die enger als etwa B beieinander liegen, erscheinen als eine Spitze ohne "
    "Kennzeichen (RF-M1: 0,5 B Abstand ergibt +52 % Breite)"
)
GRENZE_LECKAGE = "Leckage durch nicht abgeklungene Antwort wird nicht erkannt"
HINWEIS_K_KLEIN = "weniger als drei Linien: keine Spitzensuche"
KOHAERENZ_NICHT_PRUEFBAR = "Kohärenz nicht prüfbar"
HINWEIS_OHNE_KOHAERENZ = f"{KOHAERENZ_NICHT_PRUEFBAR}: keine Kohärenz übergeben"
HINWEIS_PROMINENZ = "Prominenzauswahl ist eine Heuristik ohne Literaturbeleg (FG-02 Punkt 12.5)"

AUFLOESUNGSBEGRENZT = "aufloesungsbegrenzt"
UEBERLAPPEND = "ueberlappend"
NACHBARMODE = "nachbarmode"
KOHAERENZ_NIEDRIG = "kohaerenz_niedrig"
GUELTIGKEIT_OFFEN_M7 = "gueltigkeit_offen_m7"


@dataclass(frozen=True, kw_only=True)
class Spitze:
    r"""Eine gefundene Spitze (FG-02 Datenvertrag 6.2).

    Attributes
    ----------
    k : int
        0-basierter Linienindex der Spitzenlinie.
    f_k_hz : float
        Frequenz der Spitzenlinie in Hz.
    f_sp_hz : float
        Interpolierte Spitzenfrequenz in Hz.
    hoehe : float
        Interpolierte Höhe :math:`\hat y` in [a]/[b].
    breite_3db_hz : float
        -3-dB-Breite B in Hz (NaN, wenn nicht bestimmt).
    q, zeta : float
        :math:`f_\mathrm{sp}/B` und :math:`B/(2f_\mathrm{sp})`.
    f_l_hz, f_r_hz : float
        Interpolierte -3-dB-Kreuzungen in Hz (NaN, wenn nicht bestimmt).
    delta : float
        Parabelversatz δ in Linien.
    kennzeichen : tuple of str
        Warnkennzeichen nach FG-02 3.9.
    """

    k: int
    f_k_hz: float
    f_sp_hz: float
    hoehe: float
    breite_3db_hz: float
    q: float
    zeta: float
    f_l_hz: float
    f_r_hz: float
    delta: float
    kennzeichen: tuple[str, ...]


@dataclass(frozen=True, kw_only=True, eq=False)
class Spitzenergebnis:
    """Ergebnis der Spitzensuche.

    Attributes
    ----------
    spitzen : tuple of Spitze
        Nach Frequenz sortiert.
    groesse, einheit : str
        Beschriftung des Eingangs.
    delta_f_hz : float
        Linienabstand.
    hinweise : tuple of str
        Randfälle der Eingabe.
    grenzen : tuple of str
        Dokumentierte Grenzen des Verfahrens.
    annahmen : tuple of AnnahmeEintrag
        Geltende Annahmen (P-11).
    """

    spitzen: tuple[Spitze, ...]
    groesse: str
    einheit: str
    delta_f_hz: float
    hinweise: tuple[str, ...]
    grenzen: tuple[str, ...]
    annahmen: tuple[AnnahmeEintrag, ...]


def kandidaten(
    y: FloatArray,
    frequenz_hz: FloatArray,
    *,
    prominenz_min: float | None = 2.0,
    fenster_linien: int = 20,
    f_min_hz: float | None = None,
) -> list[int]:
    """Kandidatenlinien nach Schritt 1 (lokales Maximum, Prominenz, f >= f_min).

    ``prominenz_min=None`` schaltet die Prominenzauswahl ab. NaN an den Linien k-1, k, k+1
    ergibt keine Spitze. NaN im Prominenzfenster wird auf beiden Seiten gleich behandelt:
    NaN-Linien zählen nicht zum Minimum.
    """
    anzahl = y.shape[0]
    f_min = frequenz_hz[0] if f_min_hz is None else f_min_hz
    ergebnis: list[int] = []
    for k in range(1, anzahl - 1):
        if not (y[k] > y[k - 1] and y[k] >= y[k + 1]):
            continue
        if frequenz_hz[k] < f_min:
            continue
        if prominenz_min is not None:
            links = y[max(0, k - fenster_linien) : k]
            rechts = y[k + 1 : min(anzahl, k + fenster_linien + 1)]
            # NaN zählt auf beiden Seiten gleich nicht zum Minimum; jedes Fenster enthält
            # die Nachbarlinie k-1 bzw. k+1, die hier endlich ist.
            bezug = max(float(np.nanmin(links)), float(np.nanmin(rechts)))
            if not y[k] >= prominenz_min * bezug:
                continue
        ergebnis.append(k)
    return ergebnis


def parabel(y: FloatArray, k: int) -> tuple[float, float]:
    """Parabel durch drei Linien (Schritt 2): ``(delta, hoehe)``; Nenner >= 0 → δ = 0."""
    a, b, c = float(y[k - 1]), float(y[k]), float(y[k + 1])
    nenner = a - 2.0 * b + c
    if not nenner < 0:
        return 0.0, b
    delta = 0.5 * (a - c) / nenner
    return delta, b - 0.25 * (a - c) * delta


def breite_3db(
    y: FloatArray, frequenz_hz: FloatArray, k: int, hoehe: float, delta_f_hz: float
) -> tuple[float, float, bool]:
    """-3-dB-Kreuzungen (Schritt 3): ``(f_l, f_r, ueberlappend)``.

    Eine Seite ist unbestimmt (NaN, ``ueberlappend``), wenn vor dem Unterschreiten der
    Schwelle ein lokales Minimum über der Schwelle oder das Achsenende erreicht wird.
    """
    schwelle = hoehe / math.sqrt(2.0)
    anzahl = y.shape[0]
    f_l = f_r = math.nan
    j = k
    while j > 0 and y[j] >= schwelle:
        if j < k and y[j] < y[j - 1] and y[j] <= y[j + 1]:
            break  # lokales Minimum über der Schwelle
        j -= 1
    links_bestimmt = bool(y[j] < schwelle)
    if links_bestimmt:
        f_l = float(frequenz_hz[j] + (schwelle - y[j]) / (y[j + 1] - y[j]) * delta_f_hz)
    j = k
    while j < anzahl - 1 and y[j] >= schwelle:
        if j > k and y[j] < y[j + 1] and y[j] <= y[j - 1]:
            break  # lokales Minimum über der Schwelle
        j += 1
    rechts_bestimmt = bool(y[j] < schwelle)
    if rechts_bestimmt:
        f_r = float(frequenz_hz[j - 1] + (y[j - 1] - schwelle) / (y[j - 1] - y[j]) * delta_f_hz)
    return f_l, f_r, not (links_bestimmt and rechts_bestimmt)


def suche_spitzen(
    frequenz_hz: FloatArray,
    y: npt.ArrayLike,
    *,
    kohaerenz: npt.ArrayLike | None = None,
    schwellen: Schwellen | None = None,
    annahmen: Annahmen | None = None,
    delta_f_hz: float | None = None,
    groesse: str = "",
    einheit: str = "",
) -> Spitzenergebnis:
    r"""Spitzensuche mit -3-dB-Breite und Warnkennzeichen (FG-02 3.9).

    Parameters
    ----------
    frequenz_hz : numpy.ndarray
        Achse ``(K,)``, äquidistant.
    y : array_like
        :math:`|H_1|` ``(K,)``, reell und >= 0.
    kohaerenz : array_like, optional
        γ² ``(K,)`` für das Kennzeichen ``kohaerenz_niedrig``.
    schwellen : Schwellen, optional
        :math:`p_\mathrm{min}`, W, :math:`f_\mathrm{min}`, :math:`n_\mathrm{min}`, γ²_min,
        Faktor Nachbarmode.
    annahmen : Annahmen, optional
        M7-Grenze für ``gueltigkeit_offen_m7``.
    delta_f_hz : float, optional
        Linienabstand; Voreinstellung :math:`(f_{K-1} - f_0)/(K-1)`.
    groesse, einheit : str
        Beschriftung.

    Raises
    ------
    ValueError
        Bei falscher Form, komplexem Eingang oder negativen Werten.
    """
    schwellen = schwellen if schwellen is not None else Schwellen()
    annahmen = annahmen if annahmen is not None else Annahmen()
    werte = np.asarray(y)
    if np.iscomplexobj(werte):
        raise ValueError("Spitzensuche erwartet den Betrag |H1| (reell)")
    werte = werte.astype(np.float64)
    if frequenz_hz.ndim != 1 or werte.shape != frequenz_hz.shape:
        raise ValueError(f"y {werte.shape} passt nicht zur Achse {frequenz_hz.shape}")
    with np.errstate(invalid="ignore"):
        if np.any(werte < 0):
            raise ValueError("y muss >= 0 sein (Betrag)")
    g2: FloatArray | None = None
    if kohaerenz is not None:
        g2 = np.asarray(kohaerenz, dtype=np.float64)
        if g2.shape != werte.shape:
            raise ValueError(f"kohaerenz {g2.shape} passt nicht zu y {werte.shape}")
    grenzen: tuple[str, ...] = (GRENZE_VERFAHREN, GRENZE_LECKAGE)
    if schwellen.prominenz_min is not None:
        grenzen = (*grenzen, HINWEIS_PROMINENZ)
    anzahl = werte.shape[0]
    hinweise: list[str] = []
    if anzahl < 3:
        return Spitzenergebnis(
            spitzen=(),
            groesse=groesse,
            einheit=einheit,
            delta_f_hz=float(delta_f_hz) if delta_f_hz is not None else math.nan,
            hinweise=(HINWEIS_K_KLEIN,),
            grenzen=grenzen,
            annahmen=annahmen.eintraege(),
        )
    df = (
        float(delta_f_hz)
        if delta_f_hz is not None
        else float((frequenz_hz[-1] - frequenz_hz[0]) / (anzahl - 1))
    )
    if g2 is None:
        hinweise.append(HINWEIS_OHNE_KOHAERENZ)
    roh: list[dict[str, float | int | bool]] = []
    for k in kandidaten(
        werte,
        frequenz_hz,
        prominenz_min=schwellen.prominenz_min,
        fenster_linien=schwellen.fenster_linien,
        f_min_hz=schwellen.f_min_hz,
    ):
        delta, hoehe = parabel(werte, k)
        f_l, f_r, ueberlappend = breite_3db(werte, frequenz_hz, k, hoehe, df)
        roh.append(
            {"k": k, "delta": delta, "hoehe": hoehe, "f_l": f_l, "f_r": f_r, "ue": ueberlappend}
        )
    frequenzen = [float(frequenz_hz[int(r["k"])] + float(r["delta"]) * df) for r in roh]
    spitzen: list[Spitze] = []
    ohne_kohaerenz: list[str] = []
    for i, r in enumerate(roh):
        k = int(r["k"])
        f_sp = frequenzen[i]
        f_l, f_r = float(r["f_l"]), float(r["f_r"])
        breite = f_r - f_l
        kennzeichen: list[str] = []
        if breite / df < schwellen.n_min_linien:
            kennzeichen.append(AUFLOESUNGSBEGRENZT)
        if bool(r["ue"]):
            kennzeichen.append(UEBERLAPPEND)
        andere = [abs(f - f_sp) for j, f in enumerate(frequenzen) if j != i]
        if andere and min(andere) < schwellen.nachbar_faktor * breite:
            kennzeichen.append(NACHBARMODE)
        if g2 is not None:
            links = f_l if math.isfinite(f_l) else frequenz_hz[k]
            rechts = f_r if math.isfinite(f_r) else frequenz_hz[k]
            bereich = (frequenz_hz >= links) & (frequenz_hz <= rechts)
            bereich[k] = True
            if np.all(np.isnan(g2[bereich])):  # FG-02 K1-7b
                ohne_kohaerenz.append(f"{f_sp:.3f} Hz")
            with np.errstate(invalid="ignore"):
                if np.any(g2[bereich] < schwellen.kohaerenz_min):
                    kennzeichen.append(KOHAERENZ_NIEDRIG)
        if annahmen.m7_grenze_hz is not None and f_sp > annahmen.m7_grenze_hz:
            kennzeichen.append(GUELTIGKEIT_OFFEN_M7)
        spitzen.append(
            Spitze(
                k=k,
                f_k_hz=float(frequenz_hz[k]),
                f_sp_hz=f_sp,
                hoehe=float(r["hoehe"]),
                breite_3db_hz=breite,
                q=f_sp / breite if breite > 0 else math.nan,
                zeta=breite / (2.0 * f_sp) if f_sp > 0 else math.nan,
                f_l_hz=f_l,
                f_r_hz=f_r,
                delta=float(r["delta"]),
                kennzeichen=tuple(kennzeichen),
            )
        )
    if ohne_kohaerenz:
        hinweise.append(
            f"{KOHAERENZ_NICHT_PRUEFBAR}: γ² vollständig NaN bei {', '.join(ohne_kohaerenz)}"
        )
    return Spitzenergebnis(
        spitzen=tuple(spitzen),
        groesse=groesse,
        einheit=einheit,
        delta_f_hz=df,
        hinweise=tuple(hinweise),
        grenzen=grenzen,
        annahmen=annahmen.eintraege(),
    )
