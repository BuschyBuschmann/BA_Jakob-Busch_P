r"""Eingangsdaten der Auswertung nach Datenvertrag FG-02 Abschnitt 6.1.

Die Datenquelle (z. B. der Leser für ``.svd``-Dateien über
:mod:`ldv_automation.auswertung.svd_adapter`) liefert :class:`Messdaten`. Daraus bildet
:func:`bereite_paar` für ein Kanalpaar Antwort a / Referenz b die vorverarbeiteten
Größen nach FG-02 2.4:

.. math::

    \mathrm{CP}_{ab} \leftarrow s_a s_b\,\mathcal C(\mathrm{CP}^\mathrm{roh}_{ab}),\qquad
    \mathrm{CPH}_{ab} \leftarrow s_a s_b\,\mathcal C(\mathrm{CPH}^\mathrm{roh}_{ab}),

AP und ABS bleiben unverändert. Konventionen (FG-02 2.1, 2.5): Zeitabhängigkeit
:math:`e^{+i\omega t}`, einseitige Spektren auf den Spitzenwert skaliert,
:math:`\mathrm{CP}_{ab} = \langle \hat A\,\hat B^{*}\rangle` mit a = Antwort,
b = Referenz; Felder ``(P, K)`` mit 0-basiertem Punkt- und Linienindex; ``float64`` bzw.
``complex128``; Frequenz in Hz.
"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass, field

import numpy as np
import numpy.typing as npt

from .annahmen import AnnahmeEintrag, Annahmen

FloatArray = npt.NDArray[np.float64]
ComplexArray = npt.NDArray[np.complex128]
BoolArray = npt.NDArray[np.bool_]
IntArray = npt.NDArray[np.int64]


@dataclass(frozen=True, kw_only=True)
class Herkunft:
    """Herkunft der Messdaten.

    Attributes
    ----------
    pfad : str
        Pfad der Messdatei.
    sha256 : str
        SHA-256 der Messdatei (Hex).
    """

    pfad: str
    sha256: str


@dataclass(frozen=True, kw_only=True, eq=False)
class Punkte:
    """Messpunkte.

    Attributes
    ----------
    index : numpy.ndarray
        0-basierter Punktindex, Form ``(P,)``.
    label : numpy.ndarray
        In PSV angezeigte Punktnummer, Form ``(P,)``.
    koordinaten_m : numpy.ndarray
        Koordinaten x, y, z in m, Form ``(P, 3)``.
    """

    index: IntArray
    label: IntArray
    koordinaten_m: FloatArray

    def __post_init__(self) -> None:
        p = self.index.shape[0] if self.index.ndim == 1 else -1
        if p < 1 or self.label.shape != (p,) or self.koordinaten_m.shape != (p, 3):
            raise ValueError(
                "Punkte: index (P,), label (P,) und koordinaten_m (P, 3) erwartet, erhalten "
                f"{self.index.shape}, {self.label.shape}, {self.koordinaten_m.shape}"
            )
        if self.koordinaten_m.dtype != np.float64:
            raise TypeError(f"koordinaten_m muss float64 sein: {self.koordinaten_m.dtype}")


def _pruefe_feld(
    name: str, feld: npt.NDArray[np.generic], dtype: type, form: tuple[int, int]
) -> None:
    if feld.dtype != dtype:
        raise TypeError(f"{name}: dtype {feld.dtype}, erwartet {np.dtype(dtype)}")
    if feld.shape != form:
        raise ValueError(f"{name}: Form {feld.shape}, erwartet {form} (P, K)")


def zaehle_negative(feld: FloatArray) -> int:
    """Zählt negative Werte (NaN ausgenommen); Grundlage von P-03."""
    with np.errstate(invalid="ignore"):
        return int(np.count_nonzero(feld < 0))


@dataclass(frozen=True, kw_only=True, eq=False)
class Messdaten:
    r"""Eingangsdaten nach FG-02 Abschnitt 6.1 (Rohdaten, noch ohne Vorzeichen und Konjugation).

    Parameters
    ----------
    frequenz_hz : numpy.ndarray
        Frequenzachse aus der Datei, Form ``(K,)``, ``float64``, streng steigend.
    delta_f_hz : float
        Linienabstand :math:`\Delta f = BW/n_\mathrm{FFT}` in Hz aus den Einstellungen.
    punkte : Punkte
        Messpunkte.
    einheiten : Mapping[str, str]
        SI-Einheit je Kanal, z. B. ``{"Vib Z": "m/s", "Ref1": "N"}``.
    ap : Mapping[str, numpy.ndarray]
        Autospektren :math:`\mathrm{AP}_a` je Kanal, ``(P, K)``, ``float64``, Einheit
        ``[a]²`` (Spitzenwert²), >= 0.
    betrag : Mapping[str, numpy.ndarray]
        Betragsgemittelte Spektren :math:`\mathrm{ABS}_a`, ``(P, K)``, ``float64``, >= 0.
    cp : Mapping[tuple[str, str], numpy.ndarray]
        Kreuzspektren :math:`\mathrm{CP}_{ab}` je Paar ``(a, b)``, ``(P, K)``, ``complex128``.
    cph : Mapping[tuple[str, str], numpy.ndarray]
        Antwortspektren mit Phase zur Referenz, ``(P, K)``, ``complex128`` (optional).
    phase_gueltig : bool
        ``True``, wenn die Messung eine Referenz oder einen Trigger hatte.
    herkunft : Herkunft or None
        Pfad und SHA-256 der Quelldatei.

    Raises
    ------
    TypeError
        Bei falschem dtype.
    ValueError
        Bei falscher Form, nicht steigender Achse, fehlender Einheit, fehlendem
        Autospektrum eines Paars oder negativen AP/ABS-Werten (P-03).
    """

    frequenz_hz: FloatArray
    delta_f_hz: float
    punkte: Punkte
    einheiten: Mapping[str, str]
    ap: Mapping[str, FloatArray]
    betrag: Mapping[str, FloatArray] = field(default_factory=dict)
    cp: Mapping[tuple[str, str], ComplexArray] = field(default_factory=dict)
    cph: Mapping[tuple[str, str], ComplexArray] = field(default_factory=dict)
    phase_gueltig: bool = True
    herkunft: Herkunft | None = None

    def __post_init__(self) -> None:
        f = self.frequenz_hz
        if f.dtype != np.float64 or f.ndim != 1 or f.size < 1:
            raise ValueError(f"frequenz_hz muss (K,) float64 mit K >= 1 sein: {f.dtype}, {f.shape}")
        if not np.all(np.isfinite(f)) or np.any(np.diff(f) <= 0):
            raise ValueError("frequenz_hz muss endlich und streng steigend sein")
        if not (np.isfinite(self.delta_f_hz) and self.delta_f_hz > 0):
            raise ValueError(f"delta_f_hz muss endlich und > 0 sein: {self.delta_f_hz}")
        form = (self.punkte.index.shape[0], f.shape[0])
        for kanal, ap in self.ap.items():
            _pruefe_feld(f"ap[{kanal}]", ap, np.float64, form)
            if zaehle_negative(ap):
                raise ValueError(f"P-03: AP[{kanal}] enthält negative Werte")
        for kanal, betrag in self.betrag.items():
            _pruefe_feld(f"abs[{kanal}]", betrag, np.float64, form)
            if zaehle_negative(betrag):
                raise ValueError(f"P-03: ABS[{kanal}] enthält negative Werte")
        for paar, cp in self.cp.items():
            _pruefe_feld(f"cp[{paar[0]},{paar[1]}]", cp, np.complex128, form)
            for kanal in paar:
                if kanal not in self.ap:
                    raise ValueError(f"cp{paar}: Autospektrum AP[{kanal}] fehlt")
        for paar, cph in self.cph.items():
            _pruefe_feld(f"cph[{paar[0]},{paar[1]}]", cph, np.complex128, form)
        kanaele = set(self.ap) | set(self.betrag)
        for paar in (*self.cp, *self.cph):
            kanaele.update(paar)
        fehlend = sorted(k for k in kanaele if not self.einheiten.get(k))
        if fehlend:
            raise ValueError(f"Einheit fehlt für Kanäle {fehlend}")

    @property
    def anzahl_punkte(self) -> int:
        """Anzahl der Punkte P."""
        return int(self.punkte.index.shape[0])

    @property
    def anzahl_linien(self) -> int:
        """Anzahl der Linien K."""
        return int(self.frequenz_hz.shape[0])


@dataclass(frozen=True, kw_only=True, eq=False)
class Paardaten:
    r"""Vorverarbeitete Größen eines Kanalpaars a/b nach FG-02 2.4.

    Attributes
    ----------
    antwort, referenz : str
        Kanalnamen a und b.
    einheit_antwort, einheit_referenz : str
        SI-Einheiten [a] und [b].
    frequenz_hz : numpy.ndarray
        Frequenzachse ``(K,)``.
    cp : numpy.ndarray
        :math:`s_a s_b\,\mathcal C(\mathrm{CP}^\mathrm{roh})`, ``(P, K)``.
    cph : numpy.ndarray
        :math:`s_a s_b\,\mathcal C(\mathrm{CPH}^\mathrm{roh})` bzw. Ersatz
        :math:`\mathrm{CP}/\sqrt{\mathrm{AP}_b}`.
    cph_berechnet : bool
        ``True``, wenn CPH aus CP/√AP_b berechnet wurde (exakt nur bei konstanter
        Referenzamplitude über die Blöcke).
    ap_antwort, ap_referenz : numpy.ndarray
        Autospektren ``(P, K)``.
    betrag_antwort : numpy.ndarray or None
        ABS der Antwort, falls vorhanden.
    n_d : numpy.ndarray
        Mittelungsanzahl je Punkt ``(P,)`` (M5).
    gueltig : numpy.ndarray
        Gültigkeit je Punkt ``(P,)`` (M6).
    vorzeichen_antwort, vorzeichen_referenz : int
        Angewandte Vorzeichen :math:`s_a` und :math:`s_b` (M8, FG-02 K1-1).
    konjugiert : bool
        Angewandte Konjugation (M1).
    annahmen : tuple of AnnahmeEintrag
        Geltende Annahmen (P-11).
    """

    antwort: str
    referenz: str
    einheit_antwort: str
    einheit_referenz: str
    frequenz_hz: FloatArray
    cp: ComplexArray
    cph: ComplexArray
    cph_berechnet: bool
    ap_antwort: FloatArray
    ap_referenz: FloatArray
    betrag_antwort: FloatArray | None
    n_d: IntArray
    gueltig: BoolArray
    vorzeichen_antwort: int
    vorzeichen_referenz: int
    konjugiert: bool
    annahmen: tuple[AnnahmeEintrag, ...]

    @property
    def bezeichnung(self) -> str:
        """Paarname ``"a/b"``."""
        return f"{self.antwort}/{self.referenz}"

    @property
    def einheit_frf(self) -> str:
        """Einheit [a]/[b] als Text, z. B. ``"(m/s)/N"``."""
        return einheit_quotient(self.einheit_antwort, self.einheit_referenz)


def einheit_klammer(einheit: str) -> str:
    """Setzt eine zusammengesetzte Einheit in Klammern (``m/s`` → ``(m/s)``, ``N`` bleibt)."""
    return f"({einheit})" if any(z in einheit for z in "/*· ^") else einheit


def einheit_quotient(zaehler: str, nenner: str) -> str:
    """Einheitentext ``[a]/[b]``, z. B. ``(m/s)/N``."""
    return f"{einheit_klammer(zaehler)}/{einheit_klammer(nenner)}"


def einheit_produkt(a: str, b: str) -> str:
    """Einheitentext ``[a]·[b]``, z. B. ``(m/s)·N``."""
    return f"{einheit_klammer(a)}·{einheit_klammer(b)}"


def einheit_quadrat(einheit: str) -> str:
    """Einheitentext ``[a]^2``, z. B. ``(m/s)^2``, ``N^2``."""
    return f"{einheit_klammer(einheit)}^2"


def vorverarbeite(roh: ComplexArray, vorzeichen: int, konjugieren: bool) -> ComplexArray:
    r"""Wendet :math:`s\,\mathcal C(\cdot)` mit :math:`s = s_a s_b` an (FG-02 2.4, K1-1)."""
    werte = np.conj(roh) if konjugieren else roh
    ergebnis: ComplexArray = (vorzeichen * werte).astype(np.complex128)
    return ergebnis


def cph_aus_cp(cp: ComplexArray, ap_referenz: FloatArray) -> ComplexArray:
    r"""Ersatz :math:`\mathrm{CPH} = \mathrm{CP}/\sqrt{\mathrm{AP}_b}`; NaN bei AP_b = 0."""
    wurzel = np.sqrt(ap_referenz)
    with np.errstate(divide="ignore", invalid="ignore"):
        ergebnis: ComplexArray = np.where(
            wurzel > 0, cp / np.where(wurzel > 0, wurzel, 1.0), np.nan + 1j * np.nan
        )
    return ergebnis.astype(np.complex128)


def bereite_paar(
    daten: Messdaten, antwort: str, referenz: str, annahmen: Annahmen | None = None
) -> Paardaten:
    """Bildet die vorverarbeiteten Größen des Paars ``antwort``/``referenz`` (FG-02 2.4).

    Parameters
    ----------
    daten : Messdaten
        Eingangsdaten.
    antwort, referenz : str
        Kanalnamen a und b; ``daten.cp[(a, b)]`` muss existieren.
    annahmen : Annahmen, optional
        Parametersatz (Voreinstellungen FG-02).

    Returns
    -------
    Paardaten
        CP und CPH mit :math:`s_a s_b` und Konjugation, AP/ABS unverändert.

    Raises
    ------
    KeyError
        Wenn das Paar kein Kreuzspektrum hat.
    """
    annahmen = annahmen if annahmen is not None else Annahmen()
    schluessel = (antwort, referenz)
    if schluessel not in daten.cp:
        raise KeyError(f"kein Kreuzspektrum für {antwort}/{referenz}")
    s_a = annahmen.vorzeichen(antwort)
    s_b = annahmen.vorzeichen(referenz)
    cp = vorverarbeite(daten.cp[schluessel], s_a * s_b, annahmen.konjugieren)
    ap_b = daten.ap[referenz]
    if schluessel in daten.cph:
        cph = vorverarbeite(daten.cph[schluessel], s_a * s_b, annahmen.konjugieren)
        berechnet = False
    else:
        cph = cph_aus_cp(cp, ap_b)
        berechnet = True
    p = daten.anzahl_punkte
    return Paardaten(
        antwort=antwort,
        referenz=referenz,
        einheit_antwort=daten.einheiten[antwort],
        einheit_referenz=daten.einheiten[referenz],
        frequenz_hz=daten.frequenz_hz,
        cp=cp,
        cph=cph,
        cph_berechnet=berechnet,
        ap_antwort=daten.ap[antwort],
        ap_referenz=ap_b,
        betrag_antwort=daten.betrag.get(antwort),
        n_d=annahmen.n_d_je_punkt(p),
        gueltig=annahmen.gueltig_je_punkt(p),
        vorzeichen_antwort=s_a,
        vorzeichen_referenz=s_b,
        konjugiert=annahmen.konjugieren,
        annahmen=annahmen.eintraege(),
    )
