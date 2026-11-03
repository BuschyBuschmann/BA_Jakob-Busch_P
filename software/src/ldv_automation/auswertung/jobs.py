"""Aufträge für den Hintergrundprozess der Auswertungsoberfläche (P-AUSW T1.4).

Funktionen auf Modulebene mit einfachen, ``pickle``baren Argumenten (Pfade als Text), damit sie
über :class:`ldv_automation.hintergrund.ProzessAusfuehrer` im ``spawn``-Prozess laufen. Dieses
Modul importiert weder Qt noch matplotlib (Startzeit des Prozesses, Importtest).

Zweistufiges Laden (Nutzerentscheidung F-3):

``lese_job``
    Stufe A: Leser, SHA-256, Adapter, Dateieinstellungen (:func:`~.laden.lade_svd`). Liefert
    :class:`~.laden.Geladen` (Messdaten, etwa 48 MB, in Teilen über die Pipe).
``pruef_job``
    Stufe B: liest die Datei erneut, vergleicht die SHA-256 mit der aus Stufe A und rechnet
    :func:`~.gesamt.werte_aus`. Liefert nur Prüfungen und Annahmen (etwa 0,5 MB); so muss
    keine große Datenmenge in den Prozess gesendet werden.
``export_job``
    Rechnet im Prozess neu (Pfad und Bänder) und schreibt mit :func:`~.export.exportiere`.
    Zustandslos, ohne Übertragung. Das Ziel wird vorab geprüft, damit ein vorhandenes Ziel
    sofort (nicht erst nach etwa 10 s Rechenzeit) gemeldet wird.

Alle Fehler (:class:`~.laden.LadeFehler` und die Ausnahmen des Kerns) erreichen die Oberfläche
als :class:`ldv_automation.hintergrund.AuftragFehler` mit dem Text der Ausnahme.
"""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass
from pathlib import Path

from .annahmen import AnnahmeEintrag
from .daten import Messdaten
from .export import exportiere, pruefe_ziel
from .gesamt import werte_aus
from .laden import Geladen, LadeFehler, lade_svd
from .plausibilitaet import Antriebsart, Pruefergebnis

__all__ = ["PruefErgebnis", "export_job", "lese_job", "pruef_job"]


@dataclass(frozen=True, kw_only=True, eq=False)
class PruefErgebnis:
    """Ergebnis von :func:`pruef_job` (klein genug für die Pipe).

    Attributes
    ----------
    pruefungen : tuple of Pruefergebnis
        Plausibilitätsprüfungen P-01 bis P-11, nach Prüfnummer sortiert.
    annahmen : tuple of AnnahmeEintrag
        Geltende Annahmen (``Auswertung.annahmen_liste``).
    sha256 : str
        SHA-256 der geprüften Datei (gleich der aus Stufe A).
    """

    pruefungen: tuple[Pruefergebnis, ...]
    annahmen: tuple[AnnahmeEintrag, ...]
    sha256: str


def _lade_unveraendert(pfad: str, sha256_erwartet: str | None) -> Geladen:
    """Lädt die Datei und verlangt, dass sie seit Stufe A unverändert ist.

    Raises
    ------
    LadeFehler
        Beim Laden oder wenn die SHA-256 von ``sha256_erwartet`` abweicht.
    """
    geladen = lade_svd(pfad)
    herkunft = geladen.messdaten.herkunft
    assert herkunft is not None  # lade_svd setzt die Herkunft immer
    if sha256_erwartet is not None and herkunft.sha256 != sha256_erwartet:
        raise LadeFehler(
            f"{pfad}: Messdatei hat sich seit dem ersten Laden verändert "
            f"(SHA-256 {herkunft.sha256[:12]}… statt {sha256_erwartet[:12]}…)"
        )
    return geladen


def _gesamtband(daten: Messdaten) -> tuple[tuple[float, float], ...]:
    """Ein Band über die ganze Frequenzachse der Datei (Nutzerentscheidung F-1)."""
    return ((float(daten.frequenz_hz[0]), float(daten.frequenz_hz[-1])),)


def lese_job(pfad: str) -> Geladen:
    """Stufe A: Messdatei laden (Leser, SHA-256, Adapter, Dateieinstellungen).

    Parameters
    ----------
    pfad : str
        Pfad der ``.svd``-Datei.

    Raises
    ------
    LadeFehler
        Datei fehlt, ist keine gültige PSV-Datei oder verletzt den Datenvertrag.
    """
    return lade_svd(pfad)


def pruef_job(
    pfad: str,
    sha256_erwartet: str | None = None,
    antriebspunkt: tuple[str, str, Antriebsart] | None = None,
) -> PruefErgebnis:
    """Stufe B: Plausibilitätsprüfungen (etwa 8 bis 13 s) und Annahmen.

    Parameters
    ----------
    pfad : str
        Pfad der ``.svd``-Datei.
    sha256_erwartet : str, optional
        SHA-256 aus Stufe A; weicht die jetzt gelesene Datei ab, wird abgebrochen.
    antriebspunkt : tuple of str, optional
        ``(antwort, referenz, art)`` für P-08; ohne Angabe ist P-08 „nicht prüfbar“.

    Raises
    ------
    LadeFehler
        Beim Laden oder bei veränderter Datei.
    ValueError
        Wenn das Antriebspunkt-Paar kein Kreuzspektrum hat.
    """
    geladen = _lade_unveraendert(pfad, sha256_erwartet)
    auswertung = werte_aus(geladen.messdaten, antriebspunkt=antriebspunkt)
    herkunft = geladen.messdaten.herkunft
    assert herkunft is not None
    return PruefErgebnis(
        pruefungen=auswertung.pruefungen,
        annahmen=auswertung.annahmen_liste,
        sha256=herkunft.sha256,
    )


def export_job(
    pfad: str,
    basis: str,
    sha256_erwartet: str | None = None,
    baender: Sequence[tuple[float, float]] | None = None,
    ueberschreiben: bool = False,
    antriebspunkt: tuple[str, str, Antriebsart] | None = None,
) -> tuple[str, str]:
    """Rechnet die Auswertung und schreibt ``<basis>.npz`` und ``<basis>.json``.

    Parameters
    ----------
    pfad : str
        Pfad der ``.svd``-Datei.
    basis : str
        Zielpfad ohne Endung; der Ordner muss existieren.
    sha256_erwartet : str, optional
        SHA-256 aus Stufe A; weicht die Datei ab, wird abgebrochen.
    baender : sequence of tuple of float, optional
        Bandgrenzen ``(f_u, f_o)`` in Hz; ``None`` = ein Gesamtband über die Frequenzachse.
    ueberschreiben : bool
        Vorhandene Exportdateien ersetzen.
    antriebspunkt : tuple of str, optional
        Wie bei :func:`pruef_job`.

    Returns
    -------
    tuple of str
        Pfade der ``.npz``- und ``.json``-Datei.

    Raises
    ------
    FileNotFoundError
        Zielordner fehlt.
    FileExistsError
        Zieldatei existiert und ``ueberschreiben`` ist falsch (vor der Rechnung geprüft).
    LadeFehler
        Beim Laden oder bei veränderter Datei.
    """
    ziel = Path(basis)
    pruefe_ziel(ziel, ueberschreiben)  # schnell scheitern, bevor gerechnet wird
    geladen = _lade_unveraendert(pfad, sha256_erwartet)
    daten = geladen.messdaten
    auswertung = werte_aus(
        daten,
        antriebspunkt=antriebspunkt,
        baender=_gesamtband(daten) if baender is None else baender,
    )
    npz, js = exportiere(auswertung, ziel, ueberschreiben=ueberschreiben)
    return str(npz), str(js)
