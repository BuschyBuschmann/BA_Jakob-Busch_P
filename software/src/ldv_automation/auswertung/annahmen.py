"""Einstellbare Annahmen M1–M11, Schwellen und Toleranzen der Auswertung (FG-02).

Quelle: Fachgrundlage ``in_progress/fachgrundlagen/FG-02_auswertung-stufe1.md``,
Abschnitte 2.3, 2.4, 3.2, 3.4, 3.5, 3.8, 3.9, 4, 8 und 11 (vom Nutzer am 2026-10-29
freigegeben). Jeder Parameter, dessen Wert bis zur Prüfung am Messrechner nur angenommen
ist, trägt die Nummer aus FG-02 Abschnitt 11 und einen Status (``"Annahme"`` oder z. B.
``"bestätigt am 2026-11-02"``). Jede Ausgabe der Auswertung führt die Liste
:meth:`Annahmen.eintraege` mit (Prüfung P-11).
"""

from __future__ import annotations

import math
from collections.abc import Mapping, Sequence
from dataclasses import dataclass, field
from typing import Literal

import numpy as np
import numpy.typing as npt

ANNAHME = "Annahme"
"""Status eines nicht bestätigten Parameters."""

#: Nummern der einstellbaren Annahmen nach FG-02 Abschnitt 11.
ANNAHME_NUMMERN: tuple[str, ...] = ("M1", "M2", "M4", "M5", "M6", "M7", "M8", "M10", "M11")

#: Kanäle mit festem Vorzeichen +1 (Richtungskonvention KONVENTIONEN, FG-02 2.4/6.1).
KANAELE_VORZEICHEN_FEST: tuple[str, ...] = ("Vib X", "Vib Y", "Vib Z")

#: Skalierung der Spektren (M4); bis zur Festlegung in FG-02 nur der Spitzenwert.
SKALIERUNG_SPITZENWERT = "Spitzenwert (0-to-peak)"
SKALIERUNGEN: tuple[str, ...] = (SKALIERUNG_SPITZENWERT,)

Bandregel = Literal["geschlossen", "offen"]
"""Bandzugehörigkeit der Grenzlinien (M10): ``"geschlossen"`` zählt beide Grenzlinien mit
(Voreinstellung FG-02 3.8), ``"offen"`` keine (Vergleichsvariante aus dem Prüfschritt M10)."""


@dataclass(frozen=True, kw_only=True)
class AnnahmeEintrag:
    """Ein Eintrag der Annahmenliste (P-11).

    Attributes
    ----------
    nr : str
        Nummer nach FG-02 Abschnitt 11, z. B. ``"M1"``.
    parameter : str
        Name des Parameters im Code.
    wert : str
        Eingestellter Wert als Text.
    status : str
        ``"Annahme"`` oder Bestätigungsvermerk.
    beschreibung : str
        Bedeutung in einem Satz.
    """

    nr: str
    parameter: str
    wert: str
    status: str
    beschreibung: str

    @property
    def ist_annahme(self) -> bool:
        """``True``, solange der Wert nicht bestätigt ist."""
        return self.status == ANNAHME


@dataclass(frozen=True, kw_only=True, eq=False)
class Annahmen:
    r"""Parametersatz der einstellbaren Annahmen (FG-02 Abschnitt 11).

    Parameters
    ----------
    k0 : int
        Versatz der Frequenzachse, :math:`f_k = (k + k_0)\,\Delta f` (M2). Voreinstellung 1.
    konjugieren : bool
        Kreuzspektren vor der Rechnung komplex konjugieren (M1). Voreinstellung ``False``.
    vorzeichen_kanal : Mapping[str, int]
        Vorzeichen :math:`s_c \in \{+1, -1\}` je Kanal (M8, FG-02 2.4 nach Korrektur K1-1):
        :math:`\mathrm{CP}_{ab} \leftarrow s_a s_b\,\mathcal C(\mathrm{CP}^\mathrm{roh}_{ab})`
        in jedem Kreuzspektrum, in dem der Kanal vorkommt. Fehlende Kanäle +1; Vib X/Y/Z
        sind fest +1 (Richtungskonvention KONVENTIONEN, ``ValueError`` bei -1).
    w_rbw : float
        Bandbreitenfaktor des Fensters :math:`W_\mathrm{RBW} \ge 1` (M5). Voreinstellung 1
        (Rechteck).
    n_d : int or sequence of int
        Mittelungsanzahl je Messung oder je Punkt (M5), ``>= 1``. Voreinstellung 7.
    gueltig : sequence of bool or None
        Gültigkeit je Punktindex (M6). ``None``: alle Punkte gültig (Voreinstellung).
    m7_grenze_hz : float or None
        Oberhalb dieser Frequenz in Hz ist die Gültigkeit offen (M7), Kennzeichen
        ``gueltigkeit_offen_m7``. ``None`` schaltet das Kennzeichen ab. Voreinstellung 1000.
    bandregel : {"geschlossen", "offen"}
        Bandzugehörigkeit der Grenzlinien (M10). Voreinstellung ``"geschlossen"``.
    skalierung : str
        Skalierung der Spektren in der Datei (M4). Einziger zulässiger Wert bis zur
        Festlegung in FG-02: ``"Spitzenwert (0-to-peak)"``; die Rechnung setzt ihn voraus.
    toleranzen : Toleranzen
        Toleranzen für den PSV-Vergleich (M11, FG-02 Abschnitt 8).
    status : Mapping[str, str]
        Status je Annahmennummer (``"M1"`` …). Fehlende Nummern haben den Status
        ``"Annahme"``.

    Raises
    ------
    ValueError
        Bei ungültigen Werten (z. B. ``w_rbw < 1``, ``n_d < 1``, Vorzeichen nicht ±1,
        unbekannte Annahmennummer).
    """

    k0: int = 1
    konjugieren: bool = False
    vorzeichen_kanal: Mapping[str, int] = field(default_factory=dict)
    w_rbw: float = 1.0
    n_d: int | Sequence[int] = 7
    gueltig: Sequence[bool] | None = None
    m7_grenze_hz: float | None = 1000.0
    bandregel: Bandregel = "geschlossen"
    skalierung: str = SKALIERUNG_SPITZENWERT
    toleranzen: Toleranzen = field(default_factory=lambda: Toleranzen())
    status: Mapping[str, str] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if isinstance(self.k0, bool) or not isinstance(self.k0, int) or self.k0 < 0:
            raise ValueError(f"k0 muss eine ganze Zahl >= 0 sein, nicht {self.k0!r}")
        if not math.isfinite(self.w_rbw) or self.w_rbw < 1.0:
            raise ValueError(f"w_rbw muss endlich und >= 1 sein, nicht {self.w_rbw!r}")
        n_d = (self.n_d,) if isinstance(self.n_d, int) else tuple(self.n_d)
        if not n_d or any(isinstance(n, bool) or int(n) != n or n < 1 for n in n_d):
            raise ValueError(f"n_d muss ganzzahlig und >= 1 sein, nicht {self.n_d!r}")
        if not isinstance(self.n_d, int):
            object.__setattr__(self, "n_d", tuple(int(n) for n in n_d))
        for kanal, s in self.vorzeichen_kanal.items():
            if s not in (1, -1):
                raise ValueError(f"Vorzeichen des Kanals {kanal!r} muss +1 oder -1 sein: {s!r}")
            if kanal in KANAELE_VORZEICHEN_FEST and s != 1:
                raise ValueError(f"Vorzeichen von {kanal!r} ist fest +1 (FG-02 2.4, KONVENTIONEN)")
        if self.skalierung not in SKALIERUNGEN:
            raise ValueError(
                f"Skalierung {self.skalierung!r} nicht unterstützt (M4); zulässig: {SKALIERUNGEN}"
            )
        object.__setattr__(self, "vorzeichen_kanal", dict(self.vorzeichen_kanal))
        if self.gueltig is not None:
            object.__setattr__(self, "gueltig", tuple(bool(g) for g in self.gueltig))
        if self.m7_grenze_hz is not None and not (self.m7_grenze_hz > 0):
            raise ValueError(f"m7_grenze_hz muss > 0 sein: {self.m7_grenze_hz!r}")
        if self.bandregel not in ("geschlossen", "offen"):
            raise ValueError(f"unbekannte Bandregel {self.bandregel!r}")
        unbekannt = set(self.status) - set(ANNAHME_NUMMERN)
        if unbekannt:
            raise ValueError(f"unbekannte Annahmennummern im Status: {sorted(unbekannt)}")
        if any(not str(s).strip() for s in self.status.values()):
            raise ValueError("Status darf nicht leer sein")
        object.__setattr__(self, "status", dict(self.status))

    def vorzeichen(self, kanal: str) -> int:
        """Vorzeichen :math:`s_c` des Kanals (M8), Voreinstellung +1."""
        return self.vorzeichen_kanal.get(kanal, 1)

    def status_von(self, nr: str) -> str:
        """Status der Annahme ``nr`` (``"Annahme"``, solange nicht bestätigt)."""
        if nr not in ANNAHME_NUMMERN:
            raise ValueError(f"unbekannte Annahmennummer {nr!r}")
        return self.status.get(nr, ANNAHME)

    def n_d_je_punkt(self, anzahl_punkte: int) -> npt.NDArray[np.int64]:
        """Mittelungsanzahl als Feld der Form ``(P,)``.

        Raises
        ------
        ValueError
            Wenn eine Folge angegeben ist, deren Länge nicht ``anzahl_punkte`` ist.
        """
        if isinstance(self.n_d, int):
            return np.full(anzahl_punkte, self.n_d, dtype=np.int64)
        werte = np.asarray(self.n_d, dtype=np.int64)
        if werte.shape != (anzahl_punkte,):
            raise ValueError(f"n_d hat {werte.size} Einträge, erwartet {anzahl_punkte} (P)")
        return werte

    def gueltig_je_punkt(self, anzahl_punkte: int) -> npt.NDArray[np.bool_]:
        """Gültigkeitsmaske der Form ``(P,)`` (M6).

        Raises
        ------
        ValueError
            Wenn die Länge nicht ``anzahl_punkte`` ist.
        """
        if self.gueltig is None:
            return np.ones(anzahl_punkte, dtype=np.bool_)
        maske = np.asarray(self.gueltig, dtype=np.bool_)
        if maske.shape != (anzahl_punkte,):
            raise ValueError(f"gueltig hat {maske.size} Einträge, erwartet {anzahl_punkte} (P)")
        return maske

    def eintraege(self) -> tuple[AnnahmeEintrag, ...]:
        """Alle Annahmen mit Wert und Status (Inhalt von P-11)."""
        if self.vorzeichen_kanal:
            vz = ", ".join(f"{k}: {v:+d}" for k, v in sorted(self.vorzeichen_kanal.items()))
            vz += "; übrige +1"
        else:
            vz = "+1 für alle Kanäle"
        if isinstance(self.n_d, int):
            nd = str(self.n_d)
        else:
            nd = f"je Punkt {min(self.n_d)} … {max(self.n_d)}"
        gueltig = (
            "alle Punkte gültig"
            if self.gueltig is None
            else f"{sum(1 for g in self.gueltig if not g)} von {len(self.gueltig)} ungültig"
        )
        m7 = "aus" if self.m7_grenze_hz is None else f"{self.m7_grenze_hz:g} Hz"
        zeilen = (
            ("M1", "konjugieren", str(self.konjugieren), "Kreuzspektren konjugieren (PSV-Anzeige)"),
            ("M2", "k0", str(self.k0), "Frequenzachse f_k = (k + k0)·Δf"),
            ("M4", "skalierung", self.skalierung, "Skalierung der Spektren"),
            ("M5", "w_rbw", f"{self.w_rbw:g}", "Bandbreitenfaktor des Fensters W_RBW"),
            ("M5", "n_d", nd, "Mittelungsanzahl (Blöcke je Punkt)"),
            ("M6", "gueltig", gueltig, "Punktstatus (Statusbits nicht gedeutet)"),
            ("M7", "m7_grenze_hz", m7, "Gültigkeit oberhalb dieser Frequenz offen"),
            ("M8", "vorzeichen_kanal", vz, "Vorzeichen s_c je Kanal (CP ← s_a·s_b·C(CP))"),
            ("M10", "bandregel", self.bandregel, "Bandgrenzen: Grenzlinien zählen mit"),
            (
                "M11",
                "toleranzen",
                self.toleranzen.beschreibung(),
                "Toleranzen für den PSV-Vergleich",
            ),
        )
        return tuple(
            AnnahmeEintrag(nr=nr, parameter=p, wert=w, status=self.status_von(nr), beschreibung=b)
            for nr, p, w, b in zeilen
        )


@dataclass(frozen=True, kw_only=True)
class Schwellen:
    r"""Freigegebene Schwellen der Auswertung (FG-02 Abschnitte 3.4, 3.5, 3.9, 4).

    Attributes
    ----------
    kohaerenz_min : float
        :math:`\gamma^2_\mathrm{min}`; Maske ``kohaerenz_ok = γ² >= γ²_min`` (3.5).
    prominenz_min : float or None
        :math:`p_\mathrm{min}` der Spitzenauswahl (3.9). ``None`` schaltet die
        Prominenzauswahl ab (so in den Referenzfällen RF-M und RF-K1 bis RF-K3).
    fenster_linien : int
        Fenster :math:`W` der Prominenz in Linien (3.9).
    f_min_hz : float or None
        Kleinste Spitzenfrequenz in Hz; ``None`` bedeutet :math:`f_0` (3.9).
    n_min_linien : float
        Kennzeichen ``aufloesungsbegrenzt`` bei :math:`B/\Delta f < n_\mathrm{min}` (3.9).
    k_eps : float
        Faktor des Fehlerbands :math:`|H_1|(1 \pm k_\varepsilon\varepsilon)` (3.4).
    nachbar_faktor : float
        Kennzeichen ``nachbarmode`` bei Abstand < Faktor · B (3.9).
    ungleichung_rtol : float
        Relative Reserve der Ungleichungen P-01, P-02, P-04 und der Kohärenzgrenze P-05.
    achse_rtol : float
        Zulässige Abweichung der Frequenzachse relativ zu Δf (P-06); auch Reserve der
        Bandgrenzen (3.8).
    gewicht_kohaerenz_max : float
        Obergrenze von γ² für das Gewicht (3.5): :math:`1 - 10^{-6}`.
    p07_min_spitzen, p07_ok, p07_fehler, p07_kohaerenz_min
        Phasensinn P-07: Mindestanzahl Spitzen, Schwelle ok (``q >= 0,9``), Schwelle fehler
        (``q <= 0,1``), Kohärenz an der Spitzenlinie.
    p08_ok, p08_warnung, p08_kohaerenz_min
        Passivität P-08: ``r >= 0,95`` ok, ``r <= 0,05`` Vorzeichenwarnung, Kohärenz.
    p09_max_variation, p09_kohaerenz_min
        Referenzstabilität P-09: Median des Variationskoeffizienten <= 0,05.
    """

    kohaerenz_min: float = 0.9
    prominenz_min: float | None = 2.0
    fenster_linien: int = 20
    f_min_hz: float | None = None
    n_min_linien: float = 3.0
    k_eps: float = 2.0
    nachbar_faktor: float = 3.0
    ungleichung_rtol: float = 1e-5
    achse_rtol: float = 1e-6
    gewicht_kohaerenz_max: float = 1.0 - 1e-6
    p07_min_spitzen: int = 10
    p07_ok: float = 0.9
    p07_fehler: float = 0.1
    p07_kohaerenz_min: float = 0.9
    p08_ok: float = 0.95
    p08_warnung: float = 0.05
    p08_kohaerenz_min: float = 0.9
    p09_max_variation: float = 0.05
    p09_kohaerenz_min: float = 0.9

    def __post_init__(self) -> None:
        if not 0.0 <= self.kohaerenz_min <= 1.0:
            raise ValueError(f"kohaerenz_min muss in [0, 1] liegen: {self.kohaerenz_min}")
        if self.prominenz_min is not None and not self.prominenz_min > 0:
            raise ValueError(f"prominenz_min muss > 0 sein: {self.prominenz_min}")
        if self.fenster_linien < 1:
            raise ValueError(f"fenster_linien muss >= 1 sein: {self.fenster_linien}")
        if self.p07_min_spitzen < 1:
            raise ValueError(f"p07_min_spitzen muss >= 1 sein: {self.p07_min_spitzen}")
        if not 0.0 < self.gewicht_kohaerenz_max < 1.0:
            raise ValueError("gewicht_kohaerenz_max muss in (0, 1) liegen")


@dataclass(frozen=True, kw_only=True)
class Toleranzen:
    r"""Toleranzen für „stimmt mit PSV überein“ (FG-02 Abschnitt 8, Annahme M11).

    Attributes
    ----------
    rtol : float
        Relative Toleranz für Spektren, FRF, Kohärenz, Punktmittel und Bandwerte aus
        derselben Datei (float32-Daten, W2 erreicht <= 9,3·10⁻⁷).
    atol_relativ_zum_maximum : float
        Absolute Toleranz als Anteil von ``max|Referenz|`` der Kurve (fängt Werte nahe 0).
    f_spitze_df : float
        :math:`|f_\mathrm{sp} - f_\mathrm{PSV}| \le 0{,}25\,\Delta f` ohne Warnkennzeichen.
    f_spitze_df_aufloesung : float
        :math:`\le 0{,}5\,\Delta f` mit Kennzeichen ``aufloesungsbegrenzt``.
    breite_rel : float
        :math:`|B/B_\mathrm{PSV} - 1| \le 0{,}10` ohne Warnkennzeichen.
    """

    rtol: float = 1e-5
    atol_relativ_zum_maximum: float = 1e-6
    f_spitze_df: float = 0.25
    f_spitze_df_aufloesung: float = 0.5
    breite_rel: float = 0.10

    def kurve_stimmt(self, wert: npt.ArrayLike, referenz: npt.ArrayLike) -> bool:
        """Vergleicht eine Kurve mit PSV-Werten aus derselben Datei (Abschnitt 8, Zeile 1)."""
        w = np.asarray(wert)
        r = np.asarray(referenz)
        atol = self.atol_relativ_zum_maximum * float(np.nanmax(np.abs(r))) if r.size else 0.0
        return bool(np.allclose(w, r, rtol=self.rtol, atol=atol, equal_nan=True))

    def beschreibung(self) -> str:
        """Kurztext der verwendeten Werte (für P-11 und den Export)."""
        return (
            f"rtol {self.rtol:g}, atol {self.atol_relativ_zum_maximum:g}·max; f_sp "
            f"{self.f_spitze_df:g}·Δf ({self.f_spitze_df_aufloesung:g}·Δf aufloesungsbegrenzt); "
            f"B ±{self.breite_rel:g}"
        )

    def spitze_stimmt(
        self, f_sp_hz: float, f_psv_hz: float, delta_f_hz: float, kennzeichen: Sequence[str]
    ) -> bool | None:
        """Vergleich der Spitzenfrequenz; ``None`` = kein Vergleich (anderes Warnkennzeichen).

        ``gueltigkeit_offen_m7`` verhindert den Vergleich nicht (FG-02 K1-8): M7 betrifft die
        physikalische Gültigkeit, nicht die Übereinstimmung mit PSV an denselben Daten.
        """
        andere = set(kennzeichen) - {"aufloesungsbegrenzt", "gueltigkeit_offen_m7"}
        if andere:
            return None
        grenze = (
            self.f_spitze_df_aufloesung
            if "aufloesungsbegrenzt" in kennzeichen
            else self.f_spitze_df
        )
        return abs(f_sp_hz - f_psv_hz) <= grenze * delta_f_hz

    def breite_stimmt(
        self, breite_hz: float, breite_psv_hz: float, kennzeichen: Sequence[str]
    ) -> bool | None:
        """Vergleich der -3-dB-Breite; mit einem Warnkennzeichen kein Vergleich (``None``).

        Ausnahme: nur ``gueltigkeit_offen_m7`` (FG-02 K1-8).
        """
        if set(kennzeichen) - {"gueltigkeit_offen_m7"}:
            return None
        return abs(breite_hz / breite_psv_hz - 1.0) <= self.breite_rel


# --- Stufe 2 (FG-03, Paket W5-2) ----------------------------------------------------------

#: Nummern der in Stufe 2 neuen einstellbaren Annahmen (FG-03 Abschnitt 11).
ANNAHME_NUMMERN_STUFE2: tuple[str, ...] = ("M12", "M13", "M14", "M15")

Zeitstempelfeld = Literal["zeit_a", "zeit_b"]
"""Zeitstempel je Punkt im Datensatz (M15); beide Felder unterscheiden sich in der
Beispieldatei um eine Blockdauer, ihre Differenzen zwischen Punkten sind gleich."""

#: Grenze der Orthogonalitätsprüfung der Komponentendrehung (M12), absolut.
DREHUNG_ATOL = 1e-9


@dataclass(frozen=True, kw_only=True, eq=False)
class AnnahmenStufe2:
    r"""Einstellbare Annahmen M12–M15 der Stufe 2 (FG-03 Abschnitte 2 und 11).

    Parameters
    ----------
    drehung_komponenten : sequence of sequence of float
        Drehmatrix :math:`D` (3x3), die die 3D-Komponenten X/Y/Z in das Koordinatensystem
        der Geometrie überführt: :math:`v_\mathrm{geo} = D\,v` (M12). Voreinstellung
        Einheitsmatrix (Komponenten liegen im Geometrie-KS). Muss orthogonal mit
        :math:`\det D = +1` sein.
    e_ref : sequence of float
        Bezugsrichtung der Normalen (M13, Entscheidung E5), Voreinstellung (0, 0, 1);
        wird normiert.
    elemente_index_basis : int
        Basis der Punktindizes in den Elementen (M14): 0 (Voreinstellung) oder 1. Intern
        wird immer 0-basiert gerechnet.
    zeitstempel : {"zeit_a", "zeit_b"}
        Zeitstempelfeld je Punkt, das als Messzeitpunkt gilt (M15). Verwendet werden nur
        Differenzen in s.
    status : Mapping[str, str]
        Status je Annahmennummer (``"M12"`` …); fehlende Nummern haben den Status
        ``"Annahme"``.

    Raises
    ------
    ValueError
        Bei nicht orthogonaler Drehung, Bezugsrichtung der Länge 0, unbekannter
        Indexbasis, unbekanntem Zeitstempelfeld oder unbekannter Annahmennummer.
    """

    drehung_komponenten: Sequence[Sequence[float]] = (
        (1.0, 0.0, 0.0),
        (0.0, 1.0, 0.0),
        (0.0, 0.0, 1.0),
    )
    e_ref: Sequence[float] = (0.0, 0.0, 1.0)
    elemente_index_basis: int = 0
    zeitstempel: Zeitstempelfeld = "zeit_a"
    status: Mapping[str, str] = field(default_factory=dict)

    def __post_init__(self) -> None:
        d = np.asarray(self.drehung_komponenten, dtype=np.float64)
        if d.shape != (3, 3) or not np.all(np.isfinite(d)):
            raise ValueError(f"drehung_komponenten muss eine endliche 3x3-Matrix sein: {d.shape}")
        if not np.allclose(d @ d.T, np.eye(3), rtol=0.0, atol=DREHUNG_ATOL) or not (
            np.linalg.det(d) > 0
        ):
            raise ValueError("drehung_komponenten muss eine Drehung sein (D·Dᵀ = I, det D = +1)")
        object.__setattr__(self, "drehung_komponenten", tuple(tuple(map(float, z)) for z in d))
        e = np.asarray(self.e_ref, dtype=np.float64)
        laenge = float(np.linalg.norm(e)) if e.shape == (3,) else math.nan
        if not (math.isfinite(laenge) and laenge > 0):
            raise ValueError(f"e_ref muss ein endlicher 3-Vektor mit Länge > 0 sein: {e}")
        object.__setattr__(self, "e_ref", tuple(float(x) for x in e / laenge))
        if self.elemente_index_basis not in (0, 1) or isinstance(self.elemente_index_basis, bool):
            raise ValueError(
                f"elemente_index_basis muss 0 oder 1 sein: {self.elemente_index_basis}"
            )
        if self.zeitstempel not in ("zeit_a", "zeit_b"):
            raise ValueError(f"unbekanntes Zeitstempelfeld {self.zeitstempel!r}")
        unbekannt = set(self.status) - set(ANNAHME_NUMMERN_STUFE2)
        if unbekannt:
            raise ValueError(f"unbekannte Annahmennummern im Status: {sorted(unbekannt)}")
        if any(not str(s).strip() for s in self.status.values()):
            raise ValueError("Status darf nicht leer sein")
        object.__setattr__(self, "status", dict(self.status))

    @property
    def drehung(self) -> npt.NDArray[np.float64]:
        """Drehmatrix :math:`D` als Feld ``(3, 3)`` (M12)."""
        return np.asarray(self.drehung_komponenten, dtype=np.float64)

    @property
    def e_ref_vektor(self) -> npt.NDArray[np.float64]:
        """Normierte Bezugsrichtung ``(3,)`` (M13)."""
        return np.asarray(self.e_ref, dtype=np.float64)

    def status_von(self, nr: str) -> str:
        """Status der Annahme ``nr`` (``"Annahme"``, solange nicht bestätigt)."""
        if nr not in ANNAHME_NUMMERN_STUFE2:
            raise ValueError(f"unbekannte Annahmennummer {nr!r}")
        return self.status.get(nr, ANNAHME)

    def eintraege(self) -> tuple[AnnahmeEintrag, ...]:
        """Annahmen M12–M15 mit Wert und Status (Kennzeichnung im Export)."""
        d = self.drehung
        drehung = (
            "Einheitsmatrix (Komponenten im Geometrie-KS)"
            if np.array_equal(d, np.eye(3))
            else "; ".join(" ".join(f"{x:.9g}" for x in z) for z in d)
        )
        zeilen = (
            ("M12", "drehung_komponenten", drehung, "3D-Komponenten → Geometrie-KS: v_geo = D·v"),
            (
                "M13",
                "e_ref",
                "(" + ", ".join(f"{x:g}" for x in self.e_ref) + ")",
                "Bezugsrichtung der Normalen und des Drehsinns",
            ),
            (
                "M14",
                "elemente_index_basis",
                str(self.elemente_index_basis),
                "Basis der Punktindizes in den Elementen",
            ),
            ("M15", "zeitstempel", self.zeitstempel, "Zeitstempel je Punkt = Messzeitpunkt"),
        )
        return tuple(
            AnnahmeEintrag(nr=nr, parameter=p, wert=w, status=self.status_von(nr), beschreibung=b)
            for nr, p, w, b in zeilen
        )


Gewichtung = Literal["keine", "fehler"]
r"""Gewichtung des Moden-Fits (E3): ``"keine"`` (Voreinstellung) oder
:math:`1/(|H_1|\varepsilon)^2` nach FG-02 3.4/3.5."""

Punktauswahl = Literal["staerkste", "alle"]
r"""Punkte, an denen B-1 fittet: nur die :math:`n_\mathrm{P}` stärksten je Spitze
(Voreinstellung, genügt für die Zusammenfassung) oder alle gültigen Punkte."""

Zuordnungsvariante = Literal["label", "koordinaten"]
"""Punktzuordnung in B-5 (E4)."""


@dataclass(frozen=True, kw_only=True)
class SchwellenStufe2:
    r"""Freigegebene Parameter und Schwellen der Stufe 2 (FG-03 3.3–3.5, 4, 5, 6.1, E6).

    Attributes
    ----------
    n_fit : int
        Linien beidseits der Spitzenlinie im Fitband (3.3), Voreinstellung 6.
    n_max : int
        Größte Modenzahl einer Gruppe (3.3), Voreinstellung 4; größere Gruppen bekommen
        ``gruppe_zu_gross``.
    rho_max : float
        Schwelle von rho für ``modell_passt_nicht`` (3.4), Voreinstellung 0,10.
    sd_zeta_rel_max : float
        Schwelle von :math:`\sigma_\zeta/\zeta` für ``unsicher`` (3.4), Voreinstellung 0,2.
    sd_fr_df_max : float
        Schwelle von :math:`\sigma_{f_r}/\Delta f` für ``unsicher`` (3.4), 0,5.
    n_punkte : int
        Anzahl :math:`n_\mathrm{P}` der stärksten Punkte der Zusammenfassung (3.5), 20.
    gewichtung : {"keine", "fehler"}
        Gewichtung des Fits (E3), Voreinstellung ``"keine"``.
    punktauswahl : {"staerkste", "alle"}
        Punkte, an denen gefittet wird.
    max_iter : int
        Höchstzahl der Levenberg-Marquardt-Schritte (3.4), 200.
    tol_rel : float
        Abbruch bei relativer Änderung von S kleiner als dieser Wert (3.2), 1e-12.
    lambda_max : float
        Abbruch ohne Konvergenz bei λ größer als dieser Wert (3.4), 1e12.
    zeta_max, zeta_min : float
        Grenzen für ``ausserhalb_band`` (3.4): ζ >= 0,2 oder ζ < 1e-5.
    zuordnung : {"label", "koordinaten"}
        Punktzuordnung (E4), Voreinstellung ``"label"``.
    d_tol_faktor : float
        :math:`d_\mathrm{tol} = \text{Faktor}\cdot d_\mathrm{min}` (4.1), 0,5.
    df_tol_faktor : float
        :math:`\Delta f_\mathrm{tol} = \text{Faktor}\cdot\Delta f` (4.2), 2.
    unsicherheit_ohne_b1_df : float
        Unsicherheit einer Spitzenfrequenz ohne B-1 in Δf (4.2, FG-02 3.9), 0,0508.
    signifikanz_faktor : float
        ``signifikant`` bei :math:`|\Delta f| > \text{Faktor}\sqrt{\sigma_A^2+\sigma_B^2}`, 2.
    achse_rtol : float
        Gleiche Achsen bei :math:`|f^A_k - f^B_k| \le \text{rtol}\cdot\Delta f` (4), 1e-6.
    frac_min_linien : int
        Mindestzahl gemeinsamer Linien des FRF-Vergleichs (4.3), 3.
    kollinear_min : float
        Passpunkte kollinear bei :math:`\sigma_2/\sigma_1` kleiner als dieser Wert (6.3), 1e-6.
    drift_min_punkte : int
        Mindestzahl brauchbarer Punkte der Drift (4.5), 10.
    drift_anteil : float
        Punktauswahl der Drift ohne Antriebspunkt-Paar: :math:`|H_1| \ge` Anteil·max (4.5), 0,3.
    drift_faktor : float
        ``drift_signifikant`` bei :math:`|b_1| > \text{Faktor}\cdot\sigma_{b_1}` (4.5), 3.
    drift_ausschluss : tuple of str
        Kennzeichen der gewählten Mode, mit denen ein Punkt nicht in die Drift eingeht
        (FG-03 4.5, K2-1 Option A: ``ausserhalb_band``, ``unsicher``; dazu
        ``moden_vertauscht``, Korrektur K-W5-2).
    drift_nicht_konvergiert_einzelmode : bool
        ``nicht_konvergiert`` schließt nur bei n = 1 aus (FG-03 4.5, K2-1), Voreinstellung
        ``True``; ``False`` schaltet diesen Ausschluss ab.
    orientierung_min : float
        ``orientierung_unsicher`` bei :math:`|n_e\cdot e_\mathrm{ref}|` kleiner (5.1), 0,1.
    entartet_rel : float
        Element entartet bei Fläche < Faktor·Median der Flächen (6.3), 1e-12.
    kreis_rel : float
        Kreisbahn bei :math:`|\sum\hat v_i^2| < \text{Faktor}\sum|\hat v_i|^2` (5.3), 1e-12.
    linear_rel : float
        Lineare Bahn bei :math:`b_\mathrm{min}/a_\mathrm{max}` kleiner (5.3), 1e-6.
    """

    n_fit: int = 6
    n_max: int = 4
    rho_max: float = 0.10
    sd_zeta_rel_max: float = 0.2
    sd_fr_df_max: float = 0.5
    n_punkte: int = 20
    gewichtung: Gewichtung = "keine"
    punktauswahl: Punktauswahl = "staerkste"
    max_iter: int = 200
    tol_rel: float = 1e-12
    lambda_max: float = 1e12
    zeta_max: float = 0.2
    zeta_min: float = 1e-5
    zuordnung: Zuordnungsvariante = "label"
    d_tol_faktor: float = 0.5
    df_tol_faktor: float = 2.0
    unsicherheit_ohne_b1_df: float = 0.0508
    signifikanz_faktor: float = 2.0
    achse_rtol: float = 1e-6
    frac_min_linien: int = 3
    kollinear_min: float = 1e-6
    drift_min_punkte: int = 10
    drift_anteil: float = 0.3
    drift_faktor: float = 3.0
    drift_ausschluss: tuple[str, ...] = ("ausserhalb_band", "unsicher", "moden_vertauscht")
    drift_nicht_konvergiert_einzelmode: bool = True
    orientierung_min: float = 0.1
    entartet_rel: float = 1e-12
    kreis_rel: float = 1e-12
    linear_rel: float = 1e-6

    def __post_init__(self) -> None:
        for name in ("n_fit", "n_max", "n_punkte", "max_iter", "frac_min_linien"):
            wert = getattr(self, name)
            if isinstance(wert, bool) or not isinstance(wert, int) or wert < 1:
                raise ValueError(f"{name} muss eine ganze Zahl >= 1 sein: {wert!r}")
        if self.drift_min_punkte < 3:
            raise ValueError("drift_min_punkte muss >= 3 sein (Regression mit Streuung)")
        for name in (
            "rho_max",
            "sd_zeta_rel_max",
            "sd_fr_df_max",
            "tol_rel",
            "lambda_max",
            "zeta_max",
            "zeta_min",
            "d_tol_faktor",
            "df_tol_faktor",
            "unsicherheit_ohne_b1_df",
            "signifikanz_faktor",
            "achse_rtol",
            "kollinear_min",
            "drift_anteil",
            "drift_faktor",
            "orientierung_min",
            "entartet_rel",
            "kreis_rel",
            "linear_rel",
        ):
            wert = getattr(self, name)
            if not (math.isfinite(wert) and wert > 0):
                raise ValueError(f"{name} muss endlich und > 0 sein: {wert!r}")
        if not self.zeta_min < self.zeta_max:
            raise ValueError("zeta_min muss kleiner als zeta_max sein")
        if self.gewichtung not in ("keine", "fehler"):
            raise ValueError(f"unbekannte Gewichtung {self.gewichtung!r}")
        if self.punktauswahl not in ("staerkste", "alle"):
            raise ValueError(f"unbekannte Punktauswahl {self.punktauswahl!r}")
        if self.zuordnung not in ("label", "koordinaten"):
            raise ValueError(f"unbekannte Zuordnung {self.zuordnung!r}")
