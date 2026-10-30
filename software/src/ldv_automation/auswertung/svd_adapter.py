r"""Schmale Anbindung an das Ergebnis des W2-Lesers für PSV-Dateien (``.svd``).

Der Leser liegt als Werkzeug unter ``software/tools/svd_analyse/svd_lesen.py``
(:func:`lese_svd` → ``SvdMessung``) und gehört nicht zum Hauptpaket. Dieses Modul
importiert ihn deshalb **nicht**, sondern beschreibt die benötigten Attribute als
:class:`typing.Protocol` (strukturelle Typisierung). Der Leser bleibt unverändert.

Abbildung (Datenvertrag FG-02 6.1):

- ``Signal.art == "CP"`` → ``cp[(antwort, referenz)]``, ``"CPH"`` → ``cph[…]``,
  ``"AP"`` → ``ap[kanal]``, ``"ABS"`` → ``betrag[kanal]``; Rollen (Antwort zuerst) aus
  ``Signal.kanaele``.
- Einheiten je Kanal aus den Banddaten (``Band.kanaele``: Kanal, Größe, Einheit).
- Frequenzachse und Δf aus dem Leser (Achse :math:`k\,\Delta f`, :math:`k = 1 …`).
- ``phase_gueltig`` ist wahr, wenn die Datei mindestens ein Kreuzspektrum enthält
  (Referenzkanal vorhanden).
- SHA-256 der Datei als Herkunft (Datei wird nur lesend geöffnet).
"""

from __future__ import annotations

import datetime as dt
from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import Any, Protocol

import numpy as np
import numpy.typing as npt

from .annahmen import AnnahmenStufe2
from .daten import ComplexArray, FloatArray, Herkunft, Messdaten, Punkte
from .export import sha256_datei


class _Fft(Protocol):
    @property
    def delta_f_hz(self) -> float: ...


class _Punkte(Protocol):
    @property
    def index(self) -> npt.NDArray[np.int64]: ...
    @property
    def label(self) -> npt.NDArray[np.int64]: ...
    @property
    def koordinaten_m(self) -> npt.NDArray[np.float64]: ...


class _Signal(Protocol):
    @property
    def name(self) -> str: ...
    @property
    def art(self) -> str: ...
    @property
    def kanaele(self) -> tuple[str, ...]: ...
    @property
    def werte(self) -> npt.NDArray[Any]: ...


class _Band(Protocol):
    @property
    def kanaele(self) -> tuple[tuple[str, str, str], ...]: ...


class SvdMessungArtig(Protocol):
    """Benötigte (nur gelesene) Attribute von ``svd_lesen.SvdMessung``."""

    @property
    def pfad(self) -> Path:
        """Pfad der gelesenen Datei."""
        ...

    @property
    def fft(self) -> _Fft:
        """FFT-Einstellungen (Δf)."""
        ...

    @property
    def frequenz_hz(self) -> npt.NDArray[np.float64]:
        """Frequenzachse in Hz."""
        ...

    @property
    def punkte(self) -> _Punkte:
        """Messpunkte."""
        ...

    @property
    def signale(self) -> Mapping[str, _Signal]:
        """Punktsignale nach Storage-Name."""
        ...

    @property
    def baender(self) -> Mapping[str, _Band]:
        """Banddaten (Einheiten je Kanal)."""
        ...


def _einheiten(baender: Mapping[str, _Band]) -> dict[str, str]:
    einheiten: dict[str, str] = {}
    for band in baender.values():
        for kanal, _groesse, einheit in band.kanaele:
            alt = einheiten.setdefault(kanal, einheit)
            if alt != einheit:
                raise ValueError(f"widersprüchliche Einheiten für {kanal}: {alt!r} / {einheit!r}")
    return einheiten


#: Zulässiger Imaginärteil reeller Größen relativ zu max|Wert| (Rundungsreserve).
IMAG_RTOL = 1e-12


def _reell(werte: npt.NDArray[Any], name: str) -> FloatArray:
    """Wandelt AP/ABS nach float64; ein komplexes Feld nur bei Imaginärteil ≈ 0.

    Raises
    ------
    ValueError
        Wenn ein Imaginärteil größer als ``IMAG_RTOL``·max|Wert| ist.
    """
    feld = np.asarray(werte)
    if np.iscomplexobj(feld):
        grenze = IMAG_RTOL * float(np.nanmax(np.abs(feld))) if feld.size else 0.0
        if np.any(np.abs(feld.imag) > grenze):
            raise ValueError(f"{name}: reelle Größe (AP/ABS) mit Imaginärteil != 0")
        feld = feld.real
    return np.asarray(feld, dtype=np.float64)


def _einmal(ziel: dict[Any, Any], schluessel: Any, wert: Any, signal: str) -> None:
    if schluessel in ziel:
        raise ValueError(f"{signal}: Größe {schluessel!r} kommt doppelt vor")
    ziel[schluessel] = wert


def aus_svd_messung(
    messung: SvdMessungArtig,
    *,
    sha256: str | None = None,
    einheiten: Mapping[str, str] | None = None,
) -> Messdaten:
    """Erzeugt :class:`~.daten.Messdaten` aus dem Ergebnis von ``lese_svd``.

    Parameters
    ----------
    messung : SvdMessungArtig
        Ergebnis des W2-Lesers.
    sha256 : str, optional
        SHA-256 der Datei; ohne Angabe wird er aus ``messung.pfad`` berechnet (nur lesend).
    einheiten : Mapping[str, str], optional
        Einheiten je Kanal, die die Banddaten ergänzen oder ersetzen.

    Returns
    -------
    Messdaten

    Raises
    ------
    ValueError
        Bei unbekannter Signalart, falscher Kanalzahl, doppelten Größen oder fehlenden
        Einheiten.
    """
    ap: dict[str, FloatArray] = {}
    betrag: dict[str, FloatArray] = {}
    cp: dict[tuple[str, str], ComplexArray] = {}
    cph: dict[tuple[str, str], ComplexArray] = {}
    for signal in messung.signale.values():
        kanaele: Sequence[str] = signal.kanaele
        if signal.art in ("CP", "CPH"):
            if len(kanaele) != 2:
                raise ValueError(f"{signal.name}: {signal.art} braucht zwei Kanäle: {kanaele}")
            ziel_c = cp if signal.art == "CP" else cph
            werte_c = np.asarray(signal.werte, dtype=np.complex128)
            _einmal(ziel_c, (kanaele[0], kanaele[1]), werte_c, signal.name)
        elif signal.art in ("AP", "ABS"):
            if len(kanaele) != 1:
                raise ValueError(f"{signal.name}: {signal.art} braucht einen Kanal: {kanaele}")
            ziel_r = ap if signal.art == "AP" else betrag
            werte_r = _reell(signal.werte, signal.name)
            _einmal(ziel_r, kanaele[0], werte_r, signal.name)
        else:
            raise ValueError(f"{signal.name}: unbekannte Signalart {signal.art!r}")
    alle_einheiten = _einheiten(messung.baender)
    if einheiten:
        alle_einheiten.update(einheiten)
    pfad = Path(messung.pfad).resolve()  # absoluter Pfad für die Herkunft im Export
    pruefsumme = sha256 if sha256 is not None else sha256_datei(pfad)
    return Messdaten(
        frequenz_hz=np.asarray(messung.frequenz_hz, dtype=np.float64),
        delta_f_hz=float(messung.fft.delta_f_hz),
        punkte=Punkte(
            index=np.asarray(messung.punkte.index, dtype=np.int64),
            label=np.asarray(messung.punkte.label, dtype=np.int64),
            koordinaten_m=np.asarray(messung.punkte.koordinaten_m, dtype=np.float64),
        ),
        einheiten=alle_einheiten,
        ap=ap,
        betrag=betrag,
        cp=cp,
        cph=cph,
        phase_gueltig=bool(cp),
        herkunft=Herkunft(pfad=str(pfad), sha256=pruefsumme),
    )


# --- Stufe 2 (FG-03, Paket W5-2): Zeitstempel und Elemente ----------------------------------


class _SignalMitZeit(Protocol):
    @property
    def zeit_a(self) -> Sequence[dt.datetime]: ...
    @property
    def zeit_b(self) -> Sequence[dt.datetime]: ...


class SvdStufe2Artig(Protocol):
    """Für Stufe 2 zusätzlich gelesene Attribute von ``svd_lesen.SvdMessung``."""

    @property
    def signale(self) -> Mapping[str, _SignalMitZeit]:
        """Punktsignale mit Zeitstempeln je Punkt."""
        ...

    @property
    def elemente(self) -> Sequence[Sequence[int]]:
        """Elemente als Punktindizes."""
        ...


def zeit_s_aus_svd_messung(
    messung: SvdStufe2Artig, *, annahmen2: AnnahmenStufe2 | None = None
) -> FloatArray:
    """Zeit je Punkt in s relativ zum frühesten Punkt (FG-03 2, Annahme M15).

    Verwendet wird das Zeitstempelfeld ``annahmen2.zeitstempel`` (``zeit_a`` oder
    ``zeit_b``); nur Differenzen gehen ein, die Zeitzone spielt keine Rolle.

    Raises
    ------
    ValueError
        Ohne Signale oder wenn die Zeitstempel der Signale nicht übereinstimmen.
    """
    annahmen2 = annahmen2 if annahmen2 is not None else AnnahmenStufe2()
    feld = annahmen2.zeitstempel
    reihen = [list(getattr(s, feld)) for s in messung.signale.values()]
    if not reihen or not reihen[0]:
        raise ValueError("keine Zeitstempel: Messung ohne Signale")
    if any(r != reihen[0] for r in reihen[1:]):
        raise ValueError(f"Zeitstempel {feld} der Signale stimmen nicht überein")
    start = min(reihen[0])
    return np.asarray([(z - start).total_seconds() for z in reihen[0]], dtype=np.float64)


def elemente_aus_svd_messung(messung: SvdStufe2Artig) -> tuple[tuple[int, ...], ...]:
    """Elemente der Geometrie unverändert (Indexbasis nach M14 wendet B-8 an)."""
    return tuple(tuple(int(i) for i in e) for e in messung.elemente)
