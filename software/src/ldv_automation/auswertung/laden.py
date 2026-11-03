"""Messdatei laden: Leser, Prüfsumme, Adapter und Dateieinstellungen (P-AUSW T1.3).

:func:`lade_svd` fasst zusammen, was die Oberfläche (und der Hintergrundauftrag
:func:`~.jobs.lese_job`) für eine ``.svd``-Datei braucht:

1. SHA-256 der Datei (Herkunft im Export; die Datei wird nur lesend geöffnet),
2. Leser :func:`~.svd_lesen.lese_svd` (W2),
3. Adapter :func:`~.svd_adapter.aus_svd_messung` (Datenvertrag :class:`~.daten.Messdaten`),
4. :class:`Dateieinstellungen` für die Parameterzeile der Oberfläche (UI-2).

:class:`~.daten.Messdaten` bleiben unverändert; die zusätzlichen Einstellungen reisen im
eigenen Objekt, damit sich keine Exportformate ändern.

Fehler beim Laden werden als :class:`LadeFehler` mit lesbarem Text und Dateipfad
weitergereicht (kein stiller Ersatzwert).
"""

from __future__ import annotations

import struct
import zlib
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path

from .daten import Messdaten
from .export import sha256_datei
from .svd_adapter import aus_svd_messung
from .svd_lesen import FENSTER_IN_DATEI_LESBAR, Mittelung, SvdMessung, lese_svd

__all__ = [
    "FENSTER_IN_DATEI_LESBAR",
    "Dateieinstellungen",
    "Geladen",
    "LadeFehler",
    "einstellungen_aus",
    "lade_svd",
    "referenzen_aus",
]


class LadeFehler(Exception):  # noqa: N818  (fachlicher Name)
    """Eine Messdatei konnte nicht geladen werden; der Text nennt Datei und Grund."""


@dataclass(frozen=True, kw_only=True)
class Dateieinstellungen:
    """Einstellungen der Messdatei für die Parameterzeile (UI-2).

    Das Fenster fehlt bewusst: Es ist in der Datei nicht lesbar
    (:data:`FENSTER_IN_DATEI_LESBAR`); die Oberfläche zeigt „–“.

    Attributes
    ----------
    bandbreite_hz : float
        Bandbreite in Hz (Beispieldatei 1000 Hz).
    linien : int
        Anzahl FFT-Linien (Beispieldatei 1600).
    delta_f_hz : float
        Linienabstand Δf in Hz (Beispieldatei 0,625 Hz).
    abtastfrequenz_hz : float
        Abtastfrequenz in Hz (Beispieldatei 2500 Hz).
    mittelung : Mittelung or None
        Mittelungsart und -anzahl (Sicherheitsgrad „plausibel“); ``None`` = nicht lesbar.
    punkte : int
        Anzahl der Messpunkte.
    referenzen : tuple of tuple of str
        Referenzkanäle als ``(Name, Einheit)``, in der Reihenfolge ihres ersten Auftretens als
        zweiter Kanal eines Kreuzspektrums; leer, wenn die Datei keine Referenz hat.
    """

    bandbreite_hz: float
    linien: int
    delta_f_hz: float
    abtastfrequenz_hz: float
    mittelung: Mittelung | None
    punkte: int
    referenzen: tuple[tuple[str, str], ...]


@dataclass(frozen=True, kw_only=True, eq=False)
class Geladen:
    """Ergebnis von :func:`lade_svd`.

    Attributes
    ----------
    messdaten : Messdaten
        Eingangsdaten der Auswertung (mit Herkunft: Pfad, SHA-256, Dateizeit).
    einstellungen : Dateieinstellungen
        Einstellungen der Datei für die Parameterzeile.
    """

    messdaten: Messdaten
    einstellungen: Dateieinstellungen


def referenzen_aus(daten: Messdaten) -> tuple[tuple[str, str], ...]:
    """Referenzkanäle ``(Name, Einheit)``: die eindeutigen zweiten Kanäle der Kreuzspektren.

    Parameters
    ----------
    daten : Messdaten
        Eingangsdaten; ``daten.cp`` hat die Schlüssel ``(Antwort, Referenz)``.

    Returns
    -------
    tuple of tuple of str
        In Reihenfolge des ersten Auftretens; ohne Kreuzspektrum leer.
    """
    namen: dict[str, None] = {}
    for _antwort, referenz in daten.cp:
        namen.setdefault(referenz)
    return tuple((name, daten.einheiten[name]) for name in namen)


def einstellungen_aus(messung: SvdMessung, daten: Messdaten) -> Dateieinstellungen:
    """Dateieinstellungen aus Leserergebnis und Datenvertrag.

    Parameters
    ----------
    messung : SvdMessung
        Ergebnis des Lesers.
    daten : Messdaten
        Daraus gebildete Eingangsdaten.
    """
    return Dateieinstellungen(
        bandbreite_hz=float(messung.fft.bandbreite_hz),
        linien=int(messung.fft.linien),
        delta_f_hz=float(messung.fft.delta_f_hz),
        abtastfrequenz_hz=float(messung.fft.abtastfrequenz_hz),
        mittelung=messung.mittelung,
        punkte=daten.anzahl_punkte,
        referenzen=referenzen_aus(daten),
    )


def lade_svd(pfad: str | Path, *, leser: Callable[[Path], SvdMessung] = lese_svd) -> Geladen:
    """Lädt eine ``.svd``-Datei (nur lesend) und bildet Messdaten und Dateieinstellungen.

    Parameters
    ----------
    pfad : str or pathlib.Path
        Pfad der Messdatei.
    leser : callable, optional
        Leser ``Path -> SvdMessung`` (für Tests austauschbar; Voreinstellung
        :func:`~.svd_lesen.lese_svd`).

    Returns
    -------
    Geladen
        Messdaten (SHA-256 vor dem Lesen gebildet) und Einstellungen.

    Raises
    ------
    LadeFehler
        Datei fehlt oder ist nicht lesbar, ist keine gültige PSV-Datei (Leser meldet
        ``SvdFormatFehler``) oder ihre Daten verletzen den Datenvertrag. Der Text nennt den
        Dateipfad.
    """
    datei = Path(pfad)
    try:
        pruefsumme = sha256_datei(datei)
        messung = leser(datei)
        daten = aus_svd_messung(messung, sha256=pruefsumme)
    except FileNotFoundError as exc:
        raise LadeFehler(f"{datei}: Datei nicht gefunden") from exc
    except (OSError, ValueError, TypeError, struct.error, zlib.error) as exc:
        # SvdFormatFehler ist ein ValueError; olefile meldet „keine OLE-Datei“ als OSError.
        grund = str(exc)
        # Der Leser nennt den Pfad teils selbst („Kein OLE-Verbunddokument: <Pfad>“).
        raise LadeFehler(grund if str(datei) in grund else f"{datei}: {grund}") from exc
    return Geladen(messdaten=daten, einstellungen=einstellungen_aus(messung, daten))
