"""Synthetische Messdaten für die Tests von ``darstellung`` (Erwartungswerte nach FG-02 9.2).

Eine ebene Platte (x 0,3 m, y 0,2 m, z 0,01 m → Projektion xy) mit P = 6 Punkten; Punkt p trägt
den Formfaktor ``FORM_JE_KANAL[kanal][p]`` (Vorzeichen wechselt: gleich- und gegenphasige
Punkte; je Komponente anders). Mobilität
einer Zweimassenmode (10 Hz, 20 Hz); Δf = 0,5 Hz, K = 64 Linien.
"""

from __future__ import annotations

import numpy as np
import numpy.typing as npt

from ldv_automation.auswertung.daten import Messdaten, Punkte

P = 6
K = 64
DF_HZ = 0.5
FREQUENZ_HZ = DF_HZ * np.arange(1, K + 1, dtype=np.float64)
FORM = np.array([1.0, 0.8, -0.5, 0.2, -1.0, 0.6])
"""Formfaktor je Punkt (Vorzeichen: gleich-/gegenphasig zu Punkt 0)."""
FORM_JE_KANAL = {
    "Vib X": 0.3 * np.roll(FORM, 2),
    "Vib Y": 0.5 * FORM[::-1],
    "Vib Z": FORM,
}
"""Formfaktor je Komponente und Punkt (verschieden: 3D-Mittel und Komponentenmittel weichen ab)."""
KOORDINATEN_M = np.array(
    [[0.0, 0.0, 0.0], [0.1, 0.0, 0.002], [0.2, 0.0, 0.004],
     [0.0, 0.2, 0.006], [0.15, 0.2, 0.008], [0.3, 0.1, 0.01]]
)  # fmt: skip
S_X = 1.0
N_REF = 1e-4
N_VIB = 1e-12


def mobilitaet_moden(
    f_hz: npt.ArrayLike, moden_hz: list[float], zeta: float = 0.01
) -> npt.NDArray[np.complex128]:
    """Modale Mobilität (Summe über die Moden) in (m/s)/N.

    Wie ``tests/auswertung/aw_referenz.mobilitaet_moden`` (FG-02 9.4), hier eigenständig, damit
    die Tests von ``darstellung`` keinen fremden Testordner einbinden.
    """
    w = 2.0 * np.pi * np.asarray(f_hz, dtype=np.float64)
    ergebnis = np.zeros_like(w, dtype=np.complex128)
    for fr in moden_hz:
        wr = 2.0 * np.pi * fr
        ergebnis = ergebnis + 1j * w / (wr**2 - w**2 + 2j * zeta * wr * w)
    return ergebnis


def messdaten(
    *,
    frequenz_hz: npt.NDArray[np.float64],
    ap: dict[str, npt.NDArray[np.float64]],
    cp: dict[tuple[str, str], npt.NDArray[np.complex128]] | None = None,
    delta_f_hz: float,
    phase_gueltig: bool = True,
    koordinaten_m: npt.NDArray[np.float64] | None = None,
) -> Messdaten:
    """Messdaten mit P Punkten (Label 100 …) aus der Form der Felder; Einheiten m/s, N."""
    p = next(iter(ap.values())).shape[0]
    koord = (
        koordinaten_m
        if koordinaten_m is not None
        else np.column_stack([np.linspace(0.0, 0.1, p), np.zeros(p), np.zeros(p)])
    )
    return Messdaten(
        frequenz_hz=frequenz_hz,
        delta_f_hz=delta_f_hz,
        punkte=Punkte(
            index=np.arange(p, dtype=np.int64),
            label=np.arange(100, 100 + p, dtype=np.int64),
            koordinaten_m=koord.astype(np.float64),
        ),
        einheiten={"Vib X": "m/s", "Vib Y": "m/s", "Vib Z": "m/s", "Ref1": "N"},
        ap=ap,
        cp=cp or {},
        phase_gueltig=phase_gueltig,
    )


def synthetische_messdaten(
    *, referenz: bool = True, n_vib_je_punkt: np.ndarray | None = None
) -> Messdaten:
    """Messdaten mit Vib X/Y/Z und (optional) Ref1.

    Parameters
    ----------
    referenz : bool
        ``False`` = keine Kreuzspektren (Datei ohne Referenz, ``phase_gueltig = False``).
    n_vib_je_punkt : numpy.ndarray, optional
        Rauschleistung der Vib-Kanäle je Punkt ``(P,)`` (bestimmt γ² je Punkt).
    """
    nv = N_VIB * np.ones(P) if n_vib_je_punkt is None else n_vib_je_punkt
    h0 = mobilitaet_moden(FREQUENZ_HZ, [10.0, 20.0], zeta=0.02)
    ap: dict[str, np.ndarray] = {}
    cp: dict[tuple[str, str], np.ndarray] = {}
    for kanal, form in FORM_JE_KANAL.items():
        h = form[:, None] * h0[None, :]  # (P, K)
        ap[kanal] = (np.abs(h) ** 2 * S_X + nv[:, None]).astype(np.float64)
        if referenz:
            cp[(kanal, "Ref1")] = (h * S_X).astype(np.complex128)
    if referenz:
        ap["Ref1"] = np.full((P, K), S_X + N_REF)
    return messdaten(
        frequenz_hz=FREQUENZ_HZ,
        ap=ap,
        cp=cp,
        delta_f_hz=DF_HZ,
        phase_gueltig=referenz,
        koordinaten_m=KOORDINATEN_M,
    )
