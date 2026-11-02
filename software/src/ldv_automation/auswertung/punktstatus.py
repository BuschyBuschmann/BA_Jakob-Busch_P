"""Punktstatus als benannte Bitmaske (Polytec ``PTCScanStatus``).

Quelle: Polytec PolyFile Type Library, Enumeration ``PTCScanStatus`` (Doku im Repo:
``in_progress/analysen/polytec-chm-text/basic-engine-manual/POLYFILELib/PTCScanStatus.md``).
Der Status eines Messpunkts (``MeasPoint.ScanStatus``, ``DataBand.ScanStatus``) ist eine
**Kombination** der Bitkonstanten; Prüfung nur mit Bitmaske, nie mit ``==``.

Die Tabelle enthält alle in der Doku genannten Mitglieder, auch die hier nicht erwarteten
(``UNGUELTIGE_FRAMES``, ``INTERPOLATION_FEHLGESCHLAGEN`` und die MPV-Zuordnungen), damit
dokumentierte Bits nicht als „unbekannt“ erscheinen. Bits ohne Eintrag werden von
:func:`statustexte` ausdrücklich gemeldet, nicht verschluckt.

Die Bedeutung der Bits ist die der Doku; ob PSV die Bits in ``.svd``-Dateien ebenso ablegt,
ist hier **nicht** geprüft (der Leser liest keine Statusfelder: ``punkte.statusfelder`` offen).
"""

from __future__ import annotations

import enum
import operator

__all__ = ["BITS_BEKANNT", "STATUS_TEXTE", "PunktStatus", "statustexte"]


class PunktStatus(enum.IntFlag):
    """Bits des Punktstatus nach ``PTCScanStatus`` (Wert = Polytec-Konstante)."""

    NICHT_GEMESSEN = 0
    GUELTIG = 1
    OPTIMAL = 2
    OVERRANGE = 4
    UNGUELTIG = 8
    GESPERRT = 16
    UNGUELTIGE_FRAMES = 32
    NICHT_ERREICHBAR = 64
    VERDECKT = 128
    VT_FEHLGESCHLAGEN = 256
    INTERPOLIERT = 512
    INTERPOLATION_FEHLGESCHLAGEN = 1024
    KANAL_1D_ZUGEORDNET = 2048
    KANAL_3D_ZUGEORDNET = 4096
    SENSOR_ZUGEORDNET = 8192


STATUS_TEXTE: dict[PunktStatus, str] = {
    PunktStatus.NICHT_GEMESSEN: "Nicht gemessen",
    PunktStatus.GUELTIG: "Gültig",
    PunktStatus.OPTIMAL: "Optimal",
    PunktStatus.OVERRANGE: "Overrange",
    PunktStatus.UNGUELTIG: "Ungültig",
    PunktStatus.GESPERRT: "Gesperrt",
    PunktStatus.UNGUELTIGE_FRAMES: "Ungültige Frames (nur MultiFrame)",
    PunktStatus.NICHT_ERREICHBAR: "Nicht erreichbar",
    PunktStatus.VERDECKT: "Verdeckt",
    PunktStatus.VT_FEHLGESCHLAGEN: "VT fehlgeschlagen",
    PunktStatus.INTERPOLIERT: "Interpoliert",
    PunktStatus.INTERPOLATION_FEHLGESCHLAGEN: "Interpolation fehlgeschlagen",
    PunktStatus.KANAL_1D_ZUGEORDNET: "1D-Kanal zugeordnet (nur MPV)",
    PunktStatus.KANAL_3D_ZUGEORDNET: "3D-Kanal zugeordnet (nur MPV)",
    PunktStatus.SENSOR_ZUGEORDNET: "Sensor zugeordnet (nur MPV)",
}
"""Deutscher Text je Statusbit (Schlüssel: alle Mitglieder von :class:`PunktStatus`)."""

BITS_BEKANNT = sum(int(b) for b in PunktStatus.__members__.values())
"""Oder-Verknüpfung aller dokumentierten Statusbits."""


def statustexte(code: int) -> tuple[str, ...]:
    """Übersetzt einen Punktstatus in die Texte seiner gesetzten Bits.

    Parameters
    ----------
    code : int
        Statuswert (Bitmaske, ``MeasPoint.ScanStatus``); NumPy-Ganzzahlen sind zulässig.

    Returns
    -------
    tuple of str
        Texte der gesetzten Bits, aufsteigend nach Bitwert. ``0`` ergibt
        ``("Nicht gemessen",)``. Jedes Bit ohne Eintrag erscheint als
        ``"unbekanntes Statusbit 0x…"``, damit nichts still verloren geht.

    Raises
    ------
    TypeError
        Wenn ``code`` keine Ganzzahl ist (auch ``bool`` und ``float`` werden abgelehnt).
    ValueError
        Wenn ``code`` negativ ist.
    """
    if isinstance(code, bool):
        raise TypeError("Statuscode muss eine Ganzzahl sein, nicht bool")
    wert = operator.index(code)  # TypeError bei float/str, akzeptiert numpy.integer
    if wert < 0:
        raise ValueError(f"Statuscode darf nicht negativ sein: {wert}")
    if wert == 0:
        return (STATUS_TEXTE[PunktStatus.NICHT_GEMESSEN],)
    texte: list[str] = []
    for bit in range(wert.bit_length()):
        maske = 1 << bit
        if not wert & maske:
            continue
        if maske & BITS_BEKANNT:
            texte.append(STATUS_TEXTE[PunktStatus(maske)])
        else:
            texte.append(f"unbekanntes Statusbit 0x{maske:X}")
    return tuple(texte)
