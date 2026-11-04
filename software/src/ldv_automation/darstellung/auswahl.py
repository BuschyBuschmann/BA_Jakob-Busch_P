"""Daten der Zeichenfunktionen aus dem Rechenkern (P-AUSW T2).

Keine neue Mathematik: Dieses Modul **setzt zusammen**, was :mod:`ldv_automation.auswertung`
liefert (Spektren, Punktmittel, FRF, Spitzen, Schwingform), und wählt aus (Punkt oder Mittel,
Komponenten, Kanalpaar). Die Tests vergleichen die Kurven mit dem Kern (``array_equal``).

Mittelformeln (FA-AUSW F-2, RF-UI-F2a/F2d): ``|CPH|`` mit dem Betragsmittel
(``mittel_betrag``), ``√AP`` mit dem quadratischen Mittel (``mittel_quadratisch``); das
Betragsmittel von ``√AP`` wird nie gebildet. Das 3D-Mittel ist das Mittel der punktweisen
3D-Beträge (bei ``√AP`` mit dem quadratischen Mittel, also ``√(Σ_c Mittel AP_c)``) und trägt das
Kennzeichen „nicht gegen PSV geprüft“.
"""

from __future__ import annotations

from collections import OrderedDict
from collections.abc import Sequence
from dataclasses import dataclass
from typing import Literal

import numpy as np

from ldv_automation.auswertung.annahmen import Annahmen, Schwellen
from ldv_automation.auswertung.daten import (
    BoolArray,
    ComplexArray,
    FloatArray,
    IntArray,
    Messdaten,
    bereite_paar,
)
from ldv_automation.auswertung.gesamt import (
    KOMPONENTEN_3D,
    PaarAuswertung,
    schwingform_aus,
    werte_paar_aus,
)
from ldv_automation.auswertung.mittel import (
    HINWEIS_MITTEL_3D,
    HINWEIS_MITTEL_3D_LEISTUNG,
    HINWEIS_MITTEL_KOHAERENT,
    HINWEIS_MITTEL_LEISTUNG,
    KENNZEICHEN_3D_MITTEL_UNGEPRUEFT,
    punktmittel_betrag,
)
from ldv_automation.auswertung.schwingform import Quelle, waehle_bezugspunkt
from ldv_automation.auswertung.spektren import (
    betrag_3d,
    betrag_3d_ap,
    spektrum_leistung,
    staple_3d,
)
from ldv_automation.auswertung.spitzen import Spitze

__all__ = [
    "BEZEICHNUNG_LEISTUNG",
    "KOMPONENTEN",
    "DarstellungsFehler",
    "Ebene",
    "FrfDaten",
    "Groesse",
    "PaarCache",
    "SchwingformDaten",
    "SpektrumDaten",
    "SpektrumKurve",
    "SpitzenDaten",
    "frf_daten",
    "gesamtband",
    "groessenname",
    "kanalpaare",
    "schwingform_daten",
    "spektrum_daten",
    "spitzen_daten_frf",
    "spitzen_daten_spektrum",
    "standard_bezug",
    "verfuegbare_groessen",
    "waehle_ebene",
]

KOMPONENTEN: tuple[str, ...] = ("X", "Y", "Z", "3D")
"""Komponenten in Anzeigereihenfolge; ``"3D"`` ist der 3D-Betrag."""

Groesse = Literal["kohaerent", "leistung"]
"""Größe von Ansicht 1: ``|CPH|`` (kohärent mit einer Referenz) oder ``√AP`` (Leistungsmittel)."""

Ebene = Literal["xy", "xz", "yz"]

BEZEICHNUNG_LEISTUNG = "Leistungsmittel √AP, mit Rauschen, ohne Phase"
"""Beschriftung der Größe ``√AP`` (Nutzerentscheidung F-2)."""

GRUND_KEINE_REFERENZ = "Die Datei enthält keinen Referenzkanal für diese Komponenten."

_ACHSE_VON_EBENE: dict[str, tuple[int, int]] = {"xy": (0, 1), "xz": (0, 2), "yz": (1, 2)}
_GLEICHSTAND_RTOL = 1e-9


class DarstellungsFehler(ValueError):  # noqa: N818  (fachlicher Name)
    """Die gewünschte Darstellung ist mit den Daten nicht möglich (Text für die Oberfläche)."""


def groessenname(einheit: str) -> str:
    """Name der physikalischen Größe aus der Einheit der Datei (keine Umrechnung).

    ``m/s`` → „Geschwindigkeit“, ``m`` → „Weg“, ``m/s²`` → „Beschleunigung“, sonst „Größe“.
    """
    return {"m/s": "Geschwindigkeit", "m": "Weg", "m/s²": "Beschleunigung"}.get(einheit, "Größe")


def kanal_der_komponente(komponente: str) -> str:
    """Kanalname einer Komponente (``"X"`` → ``"Vib X"``)."""
    if komponente not in ("X", "Y", "Z"):
        raise DarstellungsFehler(f"Komponente {komponente!r} ist keine Einzelkomponente X, Y, Z")
    return f"Vib {komponente}"


def kanalpaare(daten: Messdaten) -> tuple[tuple[str, str], ...]:
    """Kanalpaare (Antwort, Referenz) mit Kreuzspektrum in Dateireihenfolge (Ansichten 2 und 3)."""
    return tuple(daten.cp)


def gesamtband(frequenz_hz: FloatArray) -> tuple[tuple[float, float], ...]:
    """Ein Band über die ganze Frequenzachse (Nutzerentscheidung F-1)."""
    return ((float(frequenz_hz[0]), float(frequenz_hz[-1])),)


class PaarCache:
    """Auswertung eines Kanalpaars bei Bedarf (letzte ``groesse`` Paare im Speicher).

    Dieselben Kernfunktionen wie :func:`ldv_automation.auswertung.gesamt.werte_aus`
    (``bereite_paar``, ``werte_paar_aus``); das Ergebnis ist deshalb gleich (Test:
    ``array_equal`` gegen ``werte_aus(...).paare``). Ein Paar braucht etwa 250 ms beim ersten
    Aufruf, danach keine Rechenzeit.

    Parameters
    ----------
    daten : Messdaten
        Eingangsdaten.
    annahmen, schwellen : optional
        Wie bei ``werte_aus`` (Voreinstellungen FG-02).
    groesse : int, optional
        Anzahl der gehaltenen Paare (LRU), Voreinstellung 2.
    """

    def __init__(
        self,
        daten: Messdaten,
        *,
        annahmen: Annahmen | None = None,
        schwellen: Schwellen | None = None,
        groesse: int = 2,
    ) -> None:
        if groesse < 1:
            raise ValueError(f"groesse muss >= 1 sein: {groesse}")
        self.daten = daten
        self.annahmen = annahmen if annahmen is not None else Annahmen()
        self.schwellen = schwellen if schwellen is not None else Schwellen()
        self._groesse = groesse
        self._paare: OrderedDict[tuple[str, str], PaarAuswertung] = OrderedDict()

    def paar(self, antwort: str, referenz: str) -> PaarAuswertung:
        """Auswertung des Paars (berechnet bei Bedarf).

        Raises
        ------
        DarstellungsFehler
            Das Paar hat kein Kreuzspektrum.
        """
        schluessel = (antwort, referenz)
        if schluessel in self._paare:
            self._paare.move_to_end(schluessel)
            return self._paare[schluessel]
        if schluessel not in self.daten.cp:
            raise DarstellungsFehler(f"Kein Kreuzspektrum für {antwort}/{referenz} in der Datei.")
        ergebnis = werte_paar_aus(
            bereite_paar(self.daten, antwort, referenz, self.annahmen),
            self.schwellen,
            self.annahmen,
        )
        self._paare[schluessel] = ergebnis
        while len(self._paare) > self._groesse:
            self._paare.popitem(last=False)
        return ergebnis

    def gespeichert(self) -> tuple[tuple[str, str], ...]:
        """Paare im Speicher (ältestes zuerst)."""
        return tuple(self._paare)

    def gueltig(self) -> BoolArray:
        """Gültigkeit je Punkt (Annahme M6), ``(P,)``."""
        return self.annahmen.gueltig_je_punkt(self.daten.anzahl_punkte)


def _punkt_text(daten: Messdaten, punkt: int | None) -> str:
    if punkt is None:
        return "Mittel (alle Punkte)"
    if not 0 <= punkt < daten.anzahl_punkte:
        raise DarstellungsFehler(f"Punkt {punkt} existiert nicht (0 … {daten.anzahl_punkte - 1}).")
    return f"Punkt {int(daten.punkte.label[punkt])}"


# --- Ansicht 1: Spektrum ---------------------------------------------------------------------


@dataclass(frozen=True, kw_only=True, eq=False)
class SpektrumKurve:
    """Eine Kurve von Ansicht 1.

    Attributes
    ----------
    schluessel : str
        ``"X"``, ``"Y"``, ``"Z"`` oder ``"3D"``.
    beschriftung : str
        Legendentext (das 3D-Mittel trägt „nicht gegen PSV geprüft“).
    y : numpy.ndarray
        Werte ``(K,)`` in der Einheit der Datei.
    """

    schluessel: str
    beschriftung: str
    y: FloatArray


@dataclass(frozen=True, kw_only=True, eq=False)
class SpektrumDaten:
    """Daten von Ansicht 1 (Spektrum).

    Attributes
    ----------
    frequenz_hz : numpy.ndarray
        Frequenzachse der Datei ``(K,)``.
    kurven : tuple of SpektrumKurve
        Eine Kurve je gewählter Komponente.
    einheit : str
        Einheit der Amplitude (aus der Datei).
    groesse : {"kohaerent", "leistung"}
        Dargestellte Größe.
    bezeichnung : str
        „Geschwindigkeit, kohärent mit Ref1“ bzw. „Leistungsmittel √AP, mit Rauschen, ohne Phase“.
    auswahl_text : str
        „Mittel (alle Punkte)“ bzw. „Punkt <Label>“.
    ist_mittel : bool
        ``True`` bei „Mittel“.
    referenz : str or None
        Referenzkanal (nur ``"kohaerent"``).
    hinweise : tuple of str
        Formel des Mittels und Kennzeichen (nicht im Bild; die Oberfläche zeigt sie in AD).
    """

    frequenz_hz: FloatArray
    kurven: tuple[SpektrumKurve, ...]
    einheit: str
    groesse: Groesse
    bezeichnung: str
    auswahl_text: str
    ist_mittel: bool
    referenz: str | None
    hinweise: tuple[str, ...]


def _komponenten_pruefen(komponenten: Sequence[str]) -> tuple[str, ...]:
    if not komponenten:
        raise DarstellungsFehler("Mindestens eine Komponente muss gewählt sein.")
    unbekannt = [c for c in komponenten if c not in KOMPONENTEN]
    if unbekannt:
        raise DarstellungsFehler(f"Unbekannte Komponenten {unbekannt}; erlaubt sind {KOMPONENTEN}.")
    return tuple(c for c in KOMPONENTEN if c in komponenten)


def _standard_referenz(daten: Messdaten, komponenten: Sequence[str]) -> str | None:
    """Erste Referenz (Dateireihenfolge), zu der alle Komponenten ein Kreuzspektrum haben."""
    kanaele = [
        kanal
        for c in ("X", "Y", "Z")
        if c in komponenten or "3D" in komponenten
        for kanal in [f"Vib {c}"]
    ]
    referenzen = dict.fromkeys(b for _a, b in daten.cp)
    for referenz in referenzen:
        if all((kanal, referenz) in daten.cp for kanal in kanaele):
            return referenz
    return None


def verfuegbare_groessen(
    daten: Messdaten, komponenten: Sequence[str] = KOMPONENTEN, referenz: str | None = None
) -> dict[Groesse, str | None]:
    """Welche Größen von Ansicht 1 möglich sind (``None`` = möglich, sonst der Grund).

    ``leistung`` (``√AP``) ist immer möglich, ``kohaerent`` (``|CPH|``) nur, wenn zu allen
    gewählten Komponenten ein Kreuzspektrum mit der Referenz existiert (RF-UI-F2b).
    """
    komponenten = _komponenten_pruefen(komponenten)
    ref = referenz if referenz is not None else _standard_referenz(daten, komponenten)
    kanaele = [f"Vib {c}" for c in ("X", "Y", "Z") if c in komponenten or "3D" in komponenten]
    if ref is None or not all((k, ref) in daten.cp for k in kanaele):
        grund = (
            "Keine Referenz in der Datei: |CPH| braucht ein Kreuzspektrum mit einer Referenz."
            if not daten.cp
            else GRUND_KEINE_REFERENZ
        )
        return {"kohaerent": grund, "leistung": None}
    return {"kohaerent": None, "leistung": None}


def spektrum_daten(
    daten: Messdaten,
    cache: PaarCache,
    *,
    punkt: int | None,
    komponenten: Sequence[str] = KOMPONENTEN,
    groesse: Groesse = "kohaerent",
    referenz: str | None = None,
) -> SpektrumDaten:
    """Kurven von Ansicht 1 für einen Punkt oder das Mittel.

    Parameters
    ----------
    daten : Messdaten
        Eingangsdaten.
    cache : PaarCache
        Paarauswertungen (für ``|CPH|``).
    punkt : int or None
        0-basierter Punktindex; ``None`` = Mittel über die gültigen Punkte.
    komponenten : sequence of str
        Teilmenge von ``"X", "Y", "Z", "3D"`` (mindestens eine).
    groesse : {"kohaerent", "leistung"}
        ``|CPH|`` (Voreinstellung) oder ``√AP``.
    referenz : str, optional
        Referenzkanal für ``|CPH|``; Voreinstellung: erste Referenz der Datei, zu der alle
        gewählten Komponenten ein Kreuzspektrum haben.

    Raises
    ------
    DarstellungsFehler
        Leere oder unbekannte Komponentenwahl, ``|CPH|`` ohne Referenz, Punkt außerhalb.
    """
    komponenten = _komponenten_pruefen(komponenten)
    _punkt_text(daten, punkt)  # prüft den Bereich
    einzel = [c for c in ("X", "Y", "Z") if c in komponenten or "3D" in komponenten]
    ref: str | None = None
    if groesse == "kohaerent":
        grund = verfuegbare_groessen(daten, komponenten, referenz)["kohaerent"]
        if grund is not None:
            raise DarstellungsFehler(grund)
        ref = referenz if referenz is not None else _standard_referenz(daten, komponenten)
        assert ref is not None
        felder: dict[str, ComplexArray] = {c: cache.paar(f"Vib {c}", ref).paar.cph for c in einzel}
        werte: dict[str, FloatArray | ComplexArray] = dict(felder)
        if "3D" in komponenten:
            werte["3D"] = betrag_3d(staple_3d(*(felder[c] for c in ("X", "Y", "Z"))))
    else:
        ap = {c: daten.ap[f"Vib {c}"] for c in einzel}
        werte = {c: spektrum_leistung(ap[c]) for c in einzel}
        if "3D" in komponenten:
            werte["3D"] = betrag_3d_ap(staple_3d(*(ap[c] for c in ("X", "Y", "Z"))))
    gueltig = cache.gueltig()
    n = int(np.count_nonzero(gueltig))
    kurven: list[SpektrumKurve] = []
    hinweise: list[str] = []
    for c in komponenten:
        feld = werte[c]
        if punkt is None:
            mittel = punktmittel_betrag(feld, gueltig)
            y = mittel.mittel_betrag if groesse == "kohaerent" else mittel.mittel_quadratisch
            assert y is not None
        else:
            y = np.abs(feld[punkt]).astype(np.float64)
        name = "3D" if c == "3D" else f"Vib {c}"
        if c == "3D" and punkt is None:
            name = f"3D ({KENNZEICHEN_3D_MITTEL_UNGEPRUEFT})"
        kurven.append(SpektrumKurve(schluessel=c, beschriftung=name, y=y))
    if punkt is None:
        hinweise.append(
            (
                HINWEIS_MITTEL_KOHAERENT if groesse == "kohaerent" else HINWEIS_MITTEL_LEISTUNG
            ).format(n=n)
        )
        if "3D" in komponenten:
            hinweise.append(
                (
                    HINWEIS_MITTEL_3D if groesse == "kohaerent" else HINWEIS_MITTEL_3D_LEISTUNG
                ).format(n=n)
            )
    einheit = daten.einheiten[f"Vib {einzel[0]}"]
    bezeichnung = (
        f"{groessenname(einheit)}, kohärent mit {ref}"
        if groesse == "kohaerent"
        else BEZEICHNUNG_LEISTUNG
    )
    return SpektrumDaten(
        frequenz_hz=daten.frequenz_hz,
        kurven=tuple(kurven),
        einheit=einheit,
        groesse=groesse,
        bezeichnung=bezeichnung,
        auswahl_text=_punkt_text(daten, punkt),
        ist_mittel=punkt is None,
        referenz=ref,
        hinweise=tuple(hinweise),
    )


# --- Ansicht 2: H1/H2 und Kohärenz ------------------------------------------------------------


@dataclass(frozen=True, kw_only=True, eq=False)
class FrfDaten:
    """Daten von Ansicht 2 (Betrag, Phase, Kohärenz eines Kanalpaars).

    Attributes
    ----------
    frequenz_hz : numpy.ndarray
        Frequenzachse ``(K,)``.
    antwort, referenz : str
        Kanalpaar.
    einheit : str
        Einheit der FRF, z. B. ``(m/s)/N``.
    bezeichnung_h1 : str
        ``"H1"`` oder ``"FRF"`` (ohne Mittelung).
    betrag_h1, betrag_h2, kohaerenz : numpy.ndarray
        ``(K,)``; beim Mittel Betragsmittel bzw. arithmetisches Mittel von γ² (PSV-konform).
    phase_rad : numpy.ndarray or None
        arg H1 (= arg H2, FG-02 3.3) in rad; ``None`` beim Mittel (nicht definiert).
    ist_mittel : bool
        ``True`` bei „Mittel“.
    auswahl_text : str
        „Mittel (alle Punkte)“ bzw. „Punkt <Label>“.
    kohaerenz_min : float
        Schwelle γ²_min (Schwellen des Caches).
    """

    frequenz_hz: FloatArray
    antwort: str
    referenz: str
    einheit: str
    bezeichnung_h1: str
    betrag_h1: FloatArray
    betrag_h2: FloatArray
    kohaerenz: FloatArray
    phase_rad: FloatArray | None
    ist_mittel: bool
    auswahl_text: str
    kohaerenz_min: float


def frf_daten(cache: PaarCache, antwort: str, referenz: str, *, punkt: int | None) -> FrfDaten:
    """Kurven von Ansicht 2 für einen Punkt oder das Mittel.

    Raises
    ------
    DarstellungsFehler
        Kein Kreuzspektrum für das Paar oder Punkt außerhalb.
    """
    pa = cache.paar(antwort, referenz)
    text = _punkt_text(cache.daten, punkt)
    frf = pa.frf
    if punkt is None:
        h1 = pa.mittel_h1.mittel_betrag
        h2 = pa.mittel_h2.mittel_betrag
        g2 = pa.mittel_kohaerenz.mittel_arithmetisch
        assert h1 is not None and h2 is not None and g2 is not None
        phase = None
    else:
        h1 = np.abs(frf.h1[punkt])
        h2 = np.abs(frf.h2[punkt])
        g2 = frf.kohaerenz[punkt]
        phase = np.angle(frf.h1[punkt]).astype(np.float64)
    return FrfDaten(
        frequenz_hz=pa.paar.frequenz_hz,
        antwort=antwort,
        referenz=referenz,
        einheit=frf.einheit,
        bezeichnung_h1=frf.bezeichnung_h1,
        betrag_h1=h1,
        betrag_h2=h2,
        kohaerenz=g2,
        phase_rad=phase,
        ist_mittel=punkt is None,
        auswahl_text=text,
        kohaerenz_min=frf.kohaerenz_min,
    )


# --- Ansicht 3: Spitzen und Bänder ------------------------------------------------------------


@dataclass(frozen=True, kw_only=True, eq=False)
class SpitzenDaten:
    """Daten von Ansicht 3 (Kurve mit Spitzenmarkern und Bändern).

    Attributes
    ----------
    frequenz_hz, y : numpy.ndarray
        Kurve ``(K,)``: Betragsmittel ``|H1|`` (Grundlage der Spitzensuche) bzw. beim
        Spektrum ohne Referenz das Leistungsmittel ``√AP``.
    einheit : str
        Einheit der Kurve.
    groesse : str
        Achsengröße: ``"Betrag"`` (|H1|) oder ``"Amplitude"`` (Spektrum).
    beschriftung : str
        Legendentext der Kurve.
    spitzen : tuple of Spitze
        Alle Spitzen (nach Frequenz sortiert); leer ohne Referenz.
    baender : tuple of tuple of float
        Bänder ``(f_u, f_o)`` in Hz.
    gewaehlt : int or None
        Index der gewählten Spitze in ``spitzen``; nur sie wird beschriftet.
    hinweis : str
        Text für den Fall ohne Spitzen („Keine Spitzensuche: Referenzkanal fehlt.“ usw.).
    """

    frequenz_hz: FloatArray
    y: FloatArray
    einheit: str
    groesse: str
    beschriftung: str
    spitzen: tuple[Spitze, ...]
    baender: tuple[tuple[float, float], ...]
    gewaehlt: int | None
    hinweis: str


def spitzen_daten_frf(
    cache: PaarCache,
    antwort: str,
    referenz: str,
    *,
    baender: Sequence[tuple[float, float]] = (),
    gewaehlt: int | None = None,
) -> SpitzenDaten:
    """Betragsmittel ``|H1|`` mit den Spitzen des Kerns (Spitzensuche läuft auf dieser Kurve).

    Raises
    ------
    DarstellungsFehler
        Kein Kreuzspektrum oder ``gewaehlt`` außerhalb der Spitzenliste.
    """
    pa = cache.paar(antwort, referenz)
    spitzen = pa.spitzen.spitzen
    if gewaehlt is not None and not 0 <= gewaehlt < len(spitzen):
        raise DarstellungsFehler(f"Spitze {gewaehlt} existiert nicht (0 … {len(spitzen) - 1}).")
    y = pa.mittel_h1.mittel_betrag
    assert y is not None
    return SpitzenDaten(
        frequenz_hz=pa.paar.frequenz_hz,
        y=y,
        einheit=pa.frf.einheit,
        groesse="Betrag",
        beschriftung=f"Betragsmittel |{pa.frf.bezeichnung_h1}| {antwort}/{referenz}",
        spitzen=spitzen,
        baender=tuple((float(u), float(o)) for u, o in baender),
        gewaehlt=gewaehlt,
        hinweis="" if spitzen else "Keine Spitzen gefunden.",
    )


def spitzen_daten_spektrum(
    daten: Messdaten,
    cache: PaarCache,
    kanal: str,
    *,
    baender: Sequence[tuple[float, float]] = (),
) -> SpitzenDaten:
    """Leistungsmittel ``√AP`` eines Kanals ohne Spitzen (Datei ohne Referenz).

    Raises
    ------
    DarstellungsFehler
        Der Kanal fehlt in der Datei.
    """
    if kanal not in daten.ap:
        raise DarstellungsFehler(f"Kanal {kanal!r} fehlt in der Datei.")
    y = punktmittel_betrag(spektrum_leistung(daten.ap[kanal]), cache.gueltig()).mittel_quadratisch
    assert y is not None
    return SpitzenDaten(
        frequenz_hz=daten.frequenz_hz,
        y=y,
        einheit=daten.einheiten[kanal],
        groesse="Amplitude",
        beschriftung=f"{BEZEICHNUNG_LEISTUNG} ({kanal})",
        spitzen=(),
        baender=tuple((float(u), float(o)) for u, o in baender),
        gewaehlt=None,
        hinweis="Keine Spitzensuche: Referenzkanal fehlt.",
    )


# --- Ansicht 4: Schwingform -------------------------------------------------------------------


def waehle_ebene(koordinaten_m: FloatArray) -> Ebene:
    """Projektionsebene: die Achse mit der kleinsten Ausdehnung entfällt.

    Bei Gleichstand (relative Toleranz 1e-9 zur größten Ausdehnung) gilt xy vor xz vor yz
    (U-6). Beispieldatei: x 0,196 m, y 0,484 m, z 0,017 m → ``"xy"``.

    Parameters
    ----------
    koordinaten_m : numpy.ndarray
        Punktkoordinaten ``(P, 3)`` in m.
    """
    if koordinaten_m.ndim != 2 or koordinaten_m.shape[1] != 3 or koordinaten_m.shape[0] < 1:
        raise ValueError(f"koordinaten_m (P, 3) erwartet: {koordinaten_m.shape}")
    ausdehnung = np.ptp(koordinaten_m, axis=0)
    toleranz = _GLEICHSTAND_RTOL * max(float(ausdehnung.max()), 1e-300)
    kleinste = float(ausdehnung.min())
    # Ebene und die dabei entfallende Achse: xy (z), xz (y), yz (x)
    for ebene, entfaellt in (("xy", 2), ("xz", 1), ("yz", 0)):
        if ausdehnung[entfaellt] <= kleinste + toleranz:
            return ebene  # type: ignore[return-value]
    raise AssertionError("unerreichbar: eine Achse hat die kleinste Ausdehnung")  # pragma: no cover


@dataclass(frozen=True, kw_only=True, eq=False)
class SchwingformDaten:
    """Daten von Ansicht 4 (Schwingform bei einer Linie).

    Attributes
    ----------
    f_wahl_hz, f_hz : float
        Gewählte Frequenz und Frequenz der Linie (``f_k*`` der Datei).
    linie : int
        0-basierter Linienindex.
    koordinaten_m : numpy.ndarray
        ``(P, 3)``.
    label : numpy.ndarray
        Punktlabels ``(P,)``.
    ebene : {"xy", "xz", "yz"}
        Voreingestellte Projektionsebene (:func:`waehle_ebene`).
    komponente : str
        ``"X"``, ``"Y"``, ``"Z"`` oder ``"3D"`` (Betrag).
    betrag : numpy.ndarray
        Betrag der Komponente ``(P,)``.
    einheit : str
        Einheit des Betrags.
    quelle : {"cph", "h1", "leistung"}
        Herkunft der Amplitude.
    phase_gueltig : bool
        ``False`` ohne Referenz oder Trigger: nur Betrag.
    referenz : str or None
        Bezugskanal der Phase.
    amplitude : numpy.ndarray or None
        Komplexe Amplitude der Einzelkomponente ``(P,)``; ``None`` ohne Phase oder bei 3D.
    kohaerenz, kohaerenz_ok : numpy.ndarray or None
        γ² und Maske ``γ² ≥ γ²_min`` der Komponente an der Linie ``(P,)``.
    kohaerenz_min : float or None
        Schwelle γ²_min.
    gueltig : numpy.ndarray
        Gültigkeit je Punkt (M6).
    hinweise : tuple of str
        Hinweise des Kerns.
    """

    f_wahl_hz: float
    f_hz: float
    linie: int
    koordinaten_m: FloatArray
    label: IntArray
    ebene: Ebene
    komponente: str
    betrag: FloatArray
    einheit: str
    quelle: Quelle
    phase_gueltig: bool
    referenz: str | None
    amplitude: ComplexArray | None
    kohaerenz: FloatArray | None
    kohaerenz_ok: BoolArray | None
    kohaerenz_min: float | None
    gueltig: BoolArray
    hinweise: tuple[str, ...]


def standard_bezug(daten: SchwingformDaten) -> int | None:
    """Voreinstellung des Bezugspunkts: größtes ``|v|`` unter Punkten mit ``γ² ≥ γ²_min``.

    Returns
    -------
    int or None
        0-basierter Punktindex; ``None`` ohne Phase oder wenn kein Punkt die Bedingung erfüllt.
    """
    if daten.amplitude is None or daten.kohaerenz_ok is None:
        return None
    return waehle_bezugspunkt(np.abs(daten.amplitude), daten.kohaerenz_ok, daten.gueltig)


def schwingform_daten(
    daten: Messdaten,
    cache: PaarCache,
    f_wahl_hz: float,
    *,
    komponente: str = "3D",
    referenz: str | None = None,
    quelle: Quelle = "cph",
) -> SchwingformDaten:
    """Schwingform bei ``f_wahl_hz`` mit Betrag, Phase und Zuverlässigkeit der Komponente.

    Parameters
    ----------
    daten : Messdaten
        Eingangsdaten.
    cache : PaarCache
        Für γ² der Komponente an der Linie.
    f_wahl_hz : float
        Gewählte Frequenz in Hz (rastet auf die nächste Linie der Datei ein).
    komponente : str
        ``"X"``, ``"Y"``, ``"Z"`` oder ``"3D"``; die Phase gibt es nur für Einzelkomponenten.
    referenz : str, optional
        Referenzkanal; Voreinstellung: erste Referenz der Datei mit Kreuzspektren aller
        Komponenten, sonst ``"Ref1"`` (ohne Phase wird er nicht benutzt).
    quelle : {"cph", "h1"}
        Herkunft der Amplitude (Kern: ``schwingform_aus``).

    Raises
    ------
    DarstellungsFehler
        Unbekannte Komponente oder Frequenz außerhalb der Achse (Text des Kerns).
    """
    if komponente not in KOMPONENTEN:
        raise DarstellungsFehler(f"Unbekannte Komponente {komponente!r}.")
    ref = referenz or _standard_referenz(daten, ("3D",)) or "Ref1"
    try:
        sf = schwingform_aus(
            daten,
            f_wahl_hz,
            referenz=ref,
            quelle="h1" if quelle == "h1" else "cph",
            annahmen=cache.annahmen,
        )
    except ValueError as exc:
        raise DarstellungsFehler(str(exc)) from exc
    index = None if komponente == "3D" else ("X", "Y", "Z").index(komponente)
    betrag = sf.betrag_3d_psv if index is None else sf.betrag[:, index]
    amplitude = None
    g2 = ok = None
    g2_min = None
    if sf.phase_gueltig and sf.amplitude is not None and index is not None:
        amplitude = sf.amplitude[:, index]
        frf = cache.paar(KOMPONENTEN_3D[index], ref).frf
        g2 = frf.kohaerenz[:, sf.linie]
        ok = frf.kohaerenz_ok[:, sf.linie]
        g2_min = frf.kohaerenz_min
    return SchwingformDaten(
        f_wahl_hz=sf.f_wahl_hz,
        f_hz=sf.f_hz,
        linie=sf.linie,
        koordinaten_m=daten.punkte.koordinaten_m,
        label=daten.punkte.label,
        ebene=waehle_ebene(daten.punkte.koordinaten_m),
        komponente=komponente,
        betrag=betrag,
        einheit=sf.einheit,
        quelle=sf.quelle,
        phase_gueltig=sf.phase_gueltig,
        referenz=sf.referenz,
        amplitude=amplitude,
        kohaerenz=g2,
        kohaerenz_ok=ok,
        kohaerenz_min=g2_min,
        gueltig=cache.gueltig(),
        hinweise=sf.hinweise,
    )
