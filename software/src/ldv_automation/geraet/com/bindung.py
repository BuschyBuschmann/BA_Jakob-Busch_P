"""Schnittstelle des Adapters zur COM-Laufzeit (ohne pywin32-Import).

Die echte Umsetzung steht in :mod:`.pywin32_bindung` (nur Windows); Tests übergeben eine
Attrappe. Dekodierung und Auswertung der Prozessliste stehen hier, damit sie ohne Windows
testbar sind.
"""

from __future__ import annotations

import csv
import io
from typing import Protocol

PSV_PROZESS_KENNUNG = "psv"
"""Teilstring im Abbildnamen, der als laufende PSV gilt (wie Erkundung E1).

**Annahme [ungeprüft]:** Nur PSV selbst hat einen Abbildnamen mit „psv“. Ein anderer
Prozess mit „psv“ im Namen würde fälschlich als PSV gelten und den ``Dispatch`` freigeben.
Deshalb gibt der Adapter alle Treffer aus (``GeraeteInfo.hardware["psv_prozesse"]``,
:attr:`~.adapter.PsvComGeraet.psv_prozesse`); die Erkundung Stufe 0 (``psv_prozesse``)
prüft die Annahme am Messrechner."""


class ComBindung(Protocol):
    """Dünne Schicht zur COM-Laufzeit; alle Aufrufe aus dem Geräte-Thread."""

    def initialisiere_thread(self) -> None:
        """``CoInitialize`` für den aufrufenden Thread."""
        ...

    def beende_thread(self) -> None:
        """``CoUninitialize`` für den aufrufenden Thread."""
        ...

    def psv_prozesse(self) -> tuple[str, ...] | None:
        """Abbildnamen der PSV-Treffer in der Prozessliste; ``None``, wenn nicht ermittelbar."""
        ...

    def dispatch(self, progid: str) -> object:
        """Legt das COM-Objekt zu ``progid`` an (Late Binding)."""
        ...


def dekodiere_prozessliste(roh: bytes, codec: str) -> str | None:
    """Dekodiert die Rohausgabe von ``tasklist``; ``None`` bei Fehler (dann wird gesperrt).

    Parameters
    ----------
    roh : bytes
        Ausgabe von ``tasklist /FO CSV /NH``.
    codec : str
        Codepage der Konsole (unter Windows ``"oem"``, nicht cp1252).
    """
    try:
        return roh.decode(codec)
    except (UnicodeDecodeError, LookupError):
        return None


def psv_treffer(tasklist_csv: str) -> tuple[str, ...]:
    """Abbildnamen aus ``tasklist /FO CSV /NH``, die :data:`PSV_PROZESS_KENNUNG` enthalten."""
    return tuple(
        zeile[0]
        for zeile in csv.reader(io.StringIO(tasklist_csv))
        if zeile and PSV_PROZESS_KENNUNG in zeile[0].lower()
    )
