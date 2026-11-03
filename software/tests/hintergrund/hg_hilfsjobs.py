"""Aufträge für die Tests von ``hintergrund`` (müssen im Worker-Prozess importierbar sein)."""

from __future__ import annotations

import os
import time
from typing import Any

import numpy as np


def verdopple(x: int) -> int:
    return 2 * x


def kennung() -> int:
    """Prozesskennung des ausführenden Prozesses."""
    return os.getpid()


def nichts() -> None:
    return None


def wirf(text: str) -> None:
    raise ValueError(text)


def schlafe(sekunden: float) -> str:
    time.sleep(sekunden)
    return "wach"


def beende_hart(code: int) -> None:
    """Prozessende ohne Ergebnis und ohne Aufräumen (Absturz)."""
    os._exit(code)


def felder(n: int) -> dict[str, Any]:
    """Ergebnis mit großen, einem leeren und einem 0-dimensionalen Feld sowie Text."""
    rng = np.random.default_rng(3)
    return {
        "gross": rng.normal(size=n),
        "komplex": rng.normal(size=(n // 4, 2)) + 1j * rng.normal(size=(n // 4, 2)),
        "leer": np.zeros(0),
        "zahl": np.float64(2.5),
        "text": "ü",
    }


def nicht_picklebar() -> Any:
    return lambda: 1


def _wirft_beim_laden() -> None:
    raise ValueError("beim Entpacken")


class Boese:
    """Lässt sich senden, aber nicht entpacken (Fehler im Hauptprozess beim Laden)."""

    def __reduce__(self) -> tuple[Any, tuple[()]]:
        return (_wirft_beim_laden, ())


def boeses_ergebnis() -> Boese:
    return Boese()
