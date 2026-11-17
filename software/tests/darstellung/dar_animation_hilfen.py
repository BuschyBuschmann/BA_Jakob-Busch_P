"""Hilfen der Tests von ``animation_daten`` und ``animation3d`` (R-071).

Synthetische Messdaten mit **vorgegebener** komplexer Amplitude je Punkt und Komponente (die
CPH ist dann genau diese Amplitude) und ein ``PaarCache`` mit **vorgegebener** Kohärenzmaske,
damit Masken, M6 und NaN ohne Rauschmodell prüfbar sind.
"""

from __future__ import annotations

from types import SimpleNamespace
from typing import Any

import dar_daten as dd
import numpy as np
import numpy.typing as npt

from ldv_automation.auswertung.daten import Messdaten
from ldv_automation.darstellung.auswahl import PaarCache

KANAELE = ("Vib X", "Vib Y", "Vib Z")


def messdaten_mit_amplitude(
    v: npt.ArrayLike,
    *,
    koordinaten_m: npt.ArrayLike | None = None,
    delta_f_hz: float = 12.5,
    k_linien: int = 16,
) -> Messdaten:
    """Messdaten, deren CPH und H1 an **jeder** Linie ``v`` ``(P, 3)`` bzw. ``(P,)`` ist.

    ``v`` ``(P,)`` füllt nur die Komponente Z (die anderen sind 0). Bei Δf = 12,5 Hz ist die
    achte Linie 100 Hz. Die Autospektren sind 1,
    die Referenz hat die Leistung 1: ``CPH = CP / AP_ref = v``.
    """
    a = np.asarray(v, dtype=np.complex128)
    if a.ndim == 1:
        a = np.column_stack([np.zeros_like(a), np.zeros_like(a), a])
    p = a.shape[0]
    f = delta_f_hz * np.arange(1, k_linien + 1, dtype=np.float64)
    ap = {k: np.ones((p, k_linien)) for k in (*KANAELE, "Ref1")}
    cp = {
        (kanal, "Ref1"): np.repeat(a[:, c : c + 1], k_linien, axis=1)
        for c, kanal in enumerate(KANAELE)
    }
    koord = None if koordinaten_m is None else np.asarray(koordinaten_m, dtype=np.float64)
    return dd.messdaten(
        frequenz_hz=f,
        ap=ap,
        cp=cp,
        delta_f_hz=delta_f_hz,
        phase_gueltig=True,
        koordinaten_m=koord,
    )


class KohaerenzCache(PaarCache):
    """``PaarCache`` mit vorgegebener Kohärenzmaske ``ok`` ``(P, 3)`` und Gültigkeit ``gueltig``.

    γ² ist 0,99 bei ``ok`` und 0,5 sonst (γ²_min = 0,9); der Rest ist der echte ``PaarCache``.
    """

    def __init__(
        self,
        daten: Messdaten,
        ok: npt.ArrayLike | None = None,
        gueltig: npt.ArrayLike | None = None,
        **kwargs: Any,
    ) -> None:
        super().__init__(daten, **kwargs)
        p = daten.anzahl_punkte
        self._ok = np.ones((p, 3), dtype=bool) if ok is None else np.asarray(ok, dtype=bool)
        self._gueltig = (
            np.ones(p, dtype=bool) if gueltig is None else np.asarray(gueltig, dtype=bool)
        )

    def paar(self, antwort: str, referenz: str) -> Any:
        """Kohärenz der Komponente ``antwort`` an allen Linien (Attrappe)."""
        c = KANAELE.index(antwort)
        k = self.daten.frequenz_hz.shape[0]
        ok = np.repeat(self._ok[:, c : c + 1], k, axis=1)
        g2 = np.where(ok, 0.99, 0.5)
        return SimpleNamespace(
            frf=SimpleNamespace(kohaerenz=g2, kohaerenz_ok=ok, kohaerenz_min=0.9)
        )

    def gueltig(self) -> Any:
        """Gültigkeit je Punkt (M6, Attrappe)."""
        return self._gueltig
