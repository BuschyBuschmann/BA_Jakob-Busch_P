"""Sicherheitsnetz für R-073 (P-AUSW2 S1): Fingerabdruck der Thesis-Abbildungen bei ``achsen=None``.

Die drei Zeichenfunktionen mit Frequenzachse bekommen ein neues Optionsfeld ``achsen``. Ohne
dieses Feld (``None``, Voreinstellung) muss das Ergebnis **unverändert** bleiben (Thesis-
Abbildungen, ADR-027). Der Fingerabdruck wurde **vor** der Änderung erzeugt
(``regression_achsen.json``) und besteht aus der Figure-Struktur (Grenzen, Skalen, Texte, Ticks,
Linien samt SHA-256 der Daten) und dem SHA-256 des PNG. Die PNG-Prüfsumme gilt nur für dieselbe
matplotlib-Version (Schriftdarstellung); bei anderer Version prüft der Test nur die Struktur.

Neu erzeugen (nur bewusst, bei beabsichtigter Änderung der Abbildungen)::

    uv run python tests/darstellung/regression_achsen_hilfen.py
"""

from __future__ import annotations

import hashlib
import io
import json
from collections.abc import Iterator
from contextlib import contextmanager
from pathlib import Path
from typing import Any

import dar_daten as dd
import matplotlib
import numpy as np
from matplotlib.figure import Figure

from ldv_automation.darstellung.auswahl import (
    PaarCache,
    frf_daten,
    gesamtband,
    spektrum_daten,
    spitzen_daten_frf,
)
from ldv_automation.darstellung.bild import neue_figure
from ldv_automation.darstellung.frf import FrfOptionen, zeichne_frf
from ldv_automation.darstellung.spektrum import SpektrumOptionen, zeichne_spektrum
from ldv_automation.darstellung.spitzen import SpitzenOptionen, zeichne_spitzen
from ldv_automation.darstellung.stil import THESIS_STIL
from ldv_automation.darstellung.zeichnung import Zeichnung

GOLDEN = Path(__file__).with_name("regression_achsen.json")
GROESSE_ZOLL = (6.0, 4.0)
DPI = 100


@contextmanager
def isolierte_rc() -> Iterator[None]:
    """Voreinstellungen von matplotlib, unabhängig von rcParams anderer Tests."""
    with matplotlib.rc_context(matplotlib.rcParamsDefault):
        yield


def _hash(a: Any) -> str:
    return hashlib.sha256(
        np.ascontiguousarray(np.asarray(a, dtype=np.float64)).tobytes()
    ).hexdigest()


def fingerabdruck(z: Zeichnung) -> dict[str, Any]:
    """Figure-Struktur plus PNG-Prüfsumme einer Zeichnung."""
    z.figure.draw_without_rendering()
    achsen = []
    for ax in z.achsen:
        achsen.append(
            {
                "xlim": [float(v) for v in ax.get_xlim()],
                "ylim": [float(v) for v in ax.get_ylim()],
                "xscale": ax.get_xscale(),
                "yscale": ax.get_yscale(),
                "xlabel": ax.get_xlabel(),
                "ylabel": ax.get_ylabel(),
                "xticks": [t.get_text() for t in ax.get_xticklabels()],
                "yticks": [t.get_text() for t in ax.get_yticklabels()],
                "linien": [
                    {
                        "stil": ln.get_linestyle(),
                        "farbe": str(ln.get_color()),
                        "x": _hash(ln.get_xdata()),
                        "y": _hash(ln.get_ydata()),
                    }
                    for ln in ax.get_lines()
                ],
            }
        )
    puffer = io.BytesIO()
    z.figure.savefig(puffer, format="png", dpi=DPI)
    return {
        "achsen": achsen,
        "texte": z.alle_texte(),
        "png_sha256": hashlib.sha256(puffer.getvalue()).hexdigest(),
    }


def faelle() -> dict[str, Zeichnung]:
    """Zeichnungen der Thesis-Abbildungen (Voreinstellungen, ``achsen`` nicht gesetzt)."""
    daten = dd.synthetische_messdaten()
    cache = PaarCache(daten)
    stil = THESIS_STIL

    def fig() -> Figure:
        return neue_figure(stil, GROESSE_ZOLL)

    pd = spitzen_daten_frf(
        cache, "Vib Z", "Ref1", baender=gesamtband(daten.frequenz_hz), gewaehlt=1
    )
    return {
        "spektrum_mittel_log": zeichne_spektrum(
            fig(), spektrum_daten(daten, cache, punkt=None), SpektrumOptionen(), stil
        ),
        "spektrum_punkt_linear": zeichne_spektrum(
            fig(), spektrum_daten(daten, cache, punkt=1), SpektrumOptionen(skala="linear"), stil
        ),
        "frf_punkt_mit_phase": zeichne_frf(
            fig(),
            frf_daten(cache, "Vib Z", "Ref1", punkt=1),
            FrfOptionen(phase=True, kennzeichen_phase="unbestätigt (M8)"),
            stil,
        ),
        "frf_mittel_ohne_phase": zeichne_frf(
            fig(), frf_daten(cache, "Vib Z", "Ref1", punkt=None), FrfOptionen(), stil
        ),
        "spitzen_gewaehlt": zeichne_spitzen(fig(), pd, SpitzenOptionen(), stil),
        "spitzen_ui_linear": zeichne_spitzen(
            fig(),
            spitzen_daten_frf(cache, "Vib Z", "Ref1"),
            SpitzenOptionen(skala="linear", beschriftung_im_bild=False, legende_im_bild=False),
            stil,
        ),
    }


def erzeuge() -> dict[str, Any]:
    """Alle Fingerabdrücke samt matplotlib-Version."""
    with isolierte_rc():
        return {
            "matplotlib": matplotlib.__version__,
            "faelle": {name: fingerabdruck(z) for name, z in faelle().items()},
        }


if __name__ == "__main__":
    GOLDEN.write_text(json.dumps(erzeuge(), indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"geschrieben: {GOLDEN}")
