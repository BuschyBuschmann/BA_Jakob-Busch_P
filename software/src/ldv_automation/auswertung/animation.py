r"""Rechenkern der Animation der Betriebsschwingform (R-071, FG-04, FG-04 Nachtrag 1).

Reine NumPy-Funktionen ohne Daten- und Darstellungsbezug. Die Größe ist die **Auslenkung**
:math:`\hat d = \hat v/(i\omega)` (FG-04 3.1, E1) mit der Kreisfrequenz
:math:`\omega = 2\pi f_{k^\ast}` der **gewählten Linie** (nicht der eingegebenen Frequenz,
RF-A9). Wahlweise wird die Schnelle :math:`\hat v` selbst animiert.

Konventionen (FG-04 2, KONVENTIONEN): Zeitabhängigkeit :math:`e^{+i\omega t}`, Spitzenwert-
Spektrum, Animationswinkel :math:`\theta = \omega t` in rad, positives :math:`\varphi` heißt
"eilt voraus". Einheiten: :math:`\hat v` in m/s (CPH) bzw. (m/s)/N (H1), :math:`\hat d` in m
bzw. m/N, Koordinaten in m, Überhöhung dimensionslos.

Bildposition (FG-04 3.2)

.. math:: \vec x_p(\theta) = \vec X_p + s \sum_c \vec e_c\,\mathrm{Re}\{\hat d_{pc}\,e^{i\theta}\}

mit **einem** Faktor :math:`s` für alle Punkte, Komponenten und Bilder. Nicht bewegte Punkte
(:math:`\gamma^2 < \gamma^2_\mathrm{min}`, M6 ungültig, nicht endlich, bei 3D auch nur eine
Komponente betroffen, A-1) stehen **exakt** in der Ruhelage und gehen nicht in
:math:`D_\mathrm{ref}` ein (E5, RF-A8).

Relativer Phasenbezug: Alle Amplituden werden mit **einem** Skalar
:math:`\overline{u_b}` multipliziert, :math:`u_b = \hat v_{b,c_b}/|\hat v_{b,c_b}|`
(FG-04 3.2 bzw. Nachtrag 1, Mechanismus C, Voreinstellung A). Das ist eine reine
Verschiebung des Zeitnullpunkts; Form, Phasendifferenzen zwischen Punkten **und** Komponenten
sowie Bahnellipsen bleiben erhalten. Komponentenweises Drehen ist verboten (Nachtrag 1 3.2).

Die Schnelle :math:`u(\theta)` bleibt in
:func:`ldv_automation.auswertung.schwingform.momentanwert` (unverändert).
"""

from __future__ import annotations

import math
from typing import Literal

import numpy as np
import numpy.typing as npt

from .daten import ComplexArray, FloatArray
from .schwingform import ellipse_kennwerte

__all__ = [
    "ALPHA_VORGABE",
    "BILDER_JE_PERIODE_VORGABE",
    "Groesse",
    "animierte_amplitude",
    "auslenkung_amplitude",
    "bewegt_maske",
    "bezugsgroesse",
    "bezugsphase",
    "bildwinkel",
    "kreisfrequenz_rad_s",
    "maximum_theta",
    "phasenfehler_grenze",
    "positionen_m",
    "relativ_gedreht",
    "ueberhoehung_auto",
    "ueberhoehung_hinweis",
    "verschiebung",
    "waehle_bezugskomponente",
    "waehle_bezugspunkt_3d",
]

Groesse = Literal["auslenkung", "schnelle"]

#: Gestaltungsvorschlag der Überhöhung, ``alpha`` = größte Auslenkung / Nachbarabstand
#: (FG-04 3.5, keine fachliche Größe).
ALPHA_VORGABE = 0.25

#: Empfehlung E3: Bilder je Periode im Export (Vielfaches von 4 und 12, FG-04 3.7).
BILDER_JE_PERIODE_VORGABE = 36

#: Text des Hinweises bei zu großer Überhöhung (FG-04 3.5).
HINWEIS_UEBERLAGERUNG = "Punkte können sich überlagern"

_KOMPONENTEN_3D = 3


def kreisfrequenz_rad_s(f_hz: float) -> float:
    r""":math:`\omega = 2\pi f` in rad/s; NaN bei :math:`f \le 0` oder nicht endlichem :math:`f`.

    Parameters
    ----------
    f_hz : float
        **Linienfrequenz** :math:`f_{k^\ast}` in Hz (nicht die eingegebene Frequenz, RF-A9).
    """
    f = float(f_hz)
    if not (math.isfinite(f) and f > 0.0):
        return math.nan
    return 2.0 * math.pi * f


def auslenkung_amplitude(v: npt.ArrayLike, f_hz: float) -> ComplexArray:
    r"""Auslenkungsamplitude :math:`\hat d = \hat v/(i\omega) = -i\,\hat v/\omega` (FG-04 3.1).

    Parameters
    ----------
    v : array_like
        Komplexe Amplitude beliebiger Form, m/s (CPH) bzw. (m/s)/N (H1).
    f_hz : float
        Linienfrequenz :math:`f_{k^\ast}` in Hz.

    Returns
    -------
    numpy.ndarray
        :math:`\hat d` in m bzw. m/N, gleiche Form. Bei :math:`f \le 0` oder nicht endlichem
        :math:`f` (:math:`\omega` undefiniert) NaN, nie eine Division durch null.
    """
    a = np.asarray(v, dtype=np.complex128)
    omega = kreisfrequenz_rad_s(f_hz)
    if math.isnan(omega):
        return np.full(a.shape, complex(math.nan, math.nan), dtype=np.complex128)
    with np.errstate(invalid="ignore", divide="ignore"):  # NaN/Inf-Zeilen: Ergebnis bleibt NaN
        ergebnis: ComplexArray = -1j * a / omega
    return ergebnis


def verschiebung(d: npt.ArrayLike, theta_rad: npt.ArrayLike) -> FloatArray:
    r""":math:`\mathrm{Re}\{\hat d\,e^{i\theta}\}` (FG-04 3.2), reelle Auslenkung bzw. Schnelle.

    Parameters
    ----------
    d : array_like
        Komplexe Amplitude beliebiger Form.
    theta_rad : float or array_like
        :math:`\theta = \omega t` in rad; ein Feld wird als neue letzte Achse angehängt.
    """
    a = np.asarray(d, dtype=np.complex128)
    theta = np.asarray(theta_rad, dtype=np.float64)
    with np.errstate(invalid="ignore"):  # NaN/Inf-Zeilen: Ergebnis bleibt NaN
        produkt = a * np.exp(1j * theta) if theta.ndim == 0 else a[..., None] * np.exp(1j * theta)
    ergebnis: FloatArray = np.real(produkt)
    return ergebnis


def waehle_bezugskomponente(v_bezug: npt.ArrayLike) -> int:
    r"""Voreinstellung der Bezugskomponente: betragsgrößte Komponente (Nachtrag 1, A).

    Parameters
    ----------
    v_bezug : array_like
        Komplexe Amplitude des Bezugspunkts, ``(3,)``.

    Returns
    -------
    int
        :math:`c_b = \arg\max_c |\hat v_{bc}|`; bei Gleichstand der kleinste Index (X<Y<Z).

    Raises
    ------
    ValueError
        Bei falscher Form, nicht endlichen Komponenten oder :math:`\hat{\vec v}_b = 0`
        (kein gültiger Bezugspunkt).
    """
    v = np.asarray(v_bezug, dtype=np.complex128)
    if v.shape != (_KOMPONENTEN_3D,):
        raise ValueError(f"v_bezug (3,) erwartet: {v.shape}")
    betrag = np.abs(v)
    if not np.all(np.isfinite(betrag)):
        raise ValueError("Bezugspunkt hat nicht endliche Komponenten")
    if not np.any(betrag > 0.0):
        raise ValueError("Bezugspunkt mit v = 0 liefert keine Bezugsphase")
    return int(np.argmax(betrag))


def bezugsphase(v_bezug: npt.ArrayLike, komponente: int | None = None) -> tuple[int, complex]:
    r"""Pivot-Komponente :math:`c_b` und Phasenfaktor :math:`u_b` (Nachtrag 1, Abschnitt 5).

    :math:`u_b = \hat v_{b,c_b}/|\hat v_{b,c_b}|`, :math:`\psi_b = \arg u_b`.

    Parameters
    ----------
    v_bezug : array_like
        Skalar (Einzelkomponente) oder ``(3,)`` (3D) des Bezugspunkts.
    komponente : int, optional
        Vom Nutzer gewählte Bezugskomponente 0..2 (Mechanismus C); ``None`` = Voreinstellung
        :func:`waehle_bezugskomponente`. Bei einem Skalar nicht erlaubt (Pivot ist 0).

    Returns
    -------
    c_b : int
    u_b : complex
        Betrag 1.

    Raises
    ------
    ValueError
        Wenn :math:`|\hat v_{b,c_b}|` 0 oder nicht endlich ist, bei ungültiger Komponente
        oder Form.
    """
    v = np.asarray(v_bezug, dtype=np.complex128)
    if v.ndim == 0:
        if komponente not in (None, 0):
            raise ValueError("bei einer Einzelkomponente gibt es keine Bezugskomponente")
        c_b = 0
        pivot = complex(v)
    else:
        if v.shape != (_KOMPONENTEN_3D,):
            raise ValueError(f"v_bezug Skalar oder (3,) erwartet: {v.shape}")
        if komponente is None:
            c_b = waehle_bezugskomponente(v)
        elif 0 <= komponente < _KOMPONENTEN_3D:
            c_b = int(komponente)
        else:
            raise ValueError(f"Bezugskomponente 0..2 erwartet: {komponente}")
        pivot = complex(v[c_b])
    betrag = abs(pivot)
    if not (math.isfinite(betrag) and betrag > 0.0):
        raise ValueError(
            "Bezugskomponente hat Betrag 0 oder ist nicht endlich; "
            "andere Komponente oder 'automatisch' wählen"
        )
    return c_b, pivot / betrag


def relativ_gedreht(
    v: npt.ArrayLike,
    bezug: int,
    komponente: int | None = None,
    *,
    bewegt: npt.ArrayLike | None = None,
) -> ComplexArray:
    r"""Relativ zum Bezugspunkt gedrehte Amplitude :math:`\hat w = \hat v\,\overline{u_b}`.

    Einzelkomponente (FG-04 3.2): :math:`\hat w_p = \hat v_p\,\hat v_b^*/|\hat v_b|`.
    3D (Nachtrag 1): **ein** Skalar :math:`\overline{u_b}` für alle Punkte und **alle**
    Komponenten; die Pivot-Komponente des Bezugspunkts ist danach (bis auf Rundung) reell
    und positiv. Gedreht wird nie komponentenweise.

    Parameters
    ----------
    v : array_like
        ``(P,)`` (Einzelkomponente) oder ``(P, 3)`` (3D), komplex.
    bezug : int
        0-basierter Index des Bezugspunkts.
    komponente : int, optional
        Nur 3D: Bezugskomponente 0..2; ``None`` = betragsgrößte Komponente von ``bezug``.
    bewegt : array_like of bool, optional
        ``(P,)`` Maske der bewegten Punkte (:func:`bewegt_maske`). Ist sie gegeben, muss der
        Bezugspunkt bewegt sein (Annahme A-2: ein stehender Punkt hat keinen Nulldurchgang).

    Returns
    -------
    numpy.ndarray
        :math:`\hat w`, gleiche Form wie ``v``, Einheit wie ``v``.

    Raises
    ------
    ValueError
        Bei falscher Form, ``bezug`` außerhalb ``0 … P-1``, nicht bewegtem Bezugspunkt oder
        ungültiger Bezugskomponente (Betrag 0, nicht endlich).
    """
    a = np.asarray(v, dtype=np.complex128)
    if a.ndim not in (1, 2) or (a.ndim == 2 and a.shape[1] != _KOMPONENTEN_3D):
        raise ValueError(f"v (P,) oder (P, 3) erwartet: {a.shape}")
    if not isinstance(bezug, (int, np.integer)):
        raise ValueError(f"bezug als ganze Zahl erwartet: {bezug!r}")
    if not 0 <= bezug < a.shape[0]:
        raise ValueError(f"0 <= bezug < P erwartet: bezug={bezug}, P={a.shape[0]}")
    if a.ndim == 1 and komponente not in (None, 0):
        raise ValueError("bei einer Einzelkomponente gibt es keine Bezugskomponente")
    if bewegt is not None:
        maske = np.asarray(bewegt, dtype=bool)
        if maske.shape != (a.shape[0],):
            raise ValueError(f"bewegt (P,) erwartet: {maske.shape}")
        if not maske[bezug]:
            raise ValueError("Bezugspunkt ist nicht animiert (maskiert oder ungültig)")
    _, u_b = bezugsphase(a[bezug], komponente if a.ndim == 2 else None)
    with np.errstate(invalid="ignore", divide="ignore"):  # NaN/Inf-Zeilen wie in der Eingabe
        ergebnis: ComplexArray = a * np.conj(u_b)
    return ergebnis


def animierte_amplitude(
    amplitude: npt.ArrayLike | None,
    f_hz: float,
    *,
    groesse: Groesse = "auslenkung",
    bezug: int | None = None,
    komponente: int | None = None,
    phase_gueltig: bool = True,
    bewegt: npt.ArrayLike | None = None,
) -> ComplexArray:
    r"""Zu animierende Amplitude: optional relativ gedreht, dann :math:`/(i\omega)`.

    Parameters
    ----------
    amplitude : array_like or None
        :math:`\hat v` ``(P,)`` oder ``(P, 3)`` (z. B. ``Schwingform.amplitude``).
    f_hz : float
        Linienfrequenz :math:`f_{k^\ast}` (``Schwingform.f_hz``).
    groesse : {"auslenkung", "schnelle"}
        Animierte Größe (E1); bei ``"schnelle"`` entfällt die Division durch :math:`i\omega`.
    bezug : int, optional
        Bezugspunkt für den relativen Phasenbezug; ``None`` = absolut gegen Ref1 (M8).
    komponente : int, optional
        3D: Bezugskomponente, siehe :func:`relativ_gedreht`.
    phase_gueltig : bool
        ``Schwingform.phase_gueltig``.
    bewegt : array_like of bool, optional
        ``(P,)`` Maske der bewegten Punkte (:func:`bewegt_maske`). Wirkt nur zusammen mit
        ``bezug``: dann muss der Bezugspunkt animiert sein (A-2, siehe :func:`relativ_gedreht`).

    Raises
    ------
    ValueError
        Ohne gültige Phase (RF-A14, wie ``Schwingform.momentanwert``, RF-3D7): Es werden
        keine Phasen erfunden. Außerdem Fehler von :func:`relativ_gedreht`.
    """
    if not phase_gueltig or amplitude is None:
        raise ValueError("ohne Referenz oder Trigger keine Animation mit Vorzeichen (R-071)")
    if groesse not in ("auslenkung", "schnelle"):
        raise ValueError(f"groesse 'auslenkung' oder 'schnelle' erwartet: {groesse!r}")
    a = np.asarray(amplitude, dtype=np.complex128)
    if bezug is not None:
        a = relativ_gedreht(a, bezug, komponente, bewegt=bewegt)
    if groesse == "schnelle":
        return a
    return auslenkung_amplitude(a, f_hz)


def bewegt_maske(
    amplitude: npt.ArrayLike,
    kohaerenz_ok: npt.ArrayLike,
    gueltig: npt.ArrayLike | None = None,
) -> npt.NDArray[np.bool_]:
    r"""Punkte, die sich bewegen (FG-04 3.6, E5, A-1).

    Ein Punkt bewegt sich, wenn :math:`\gamma^2 \ge \gamma^2_\mathrm{min}`, M6 gültig und die
    Amplitude endlich ist. Bei ``(P, 3)`` muss das für **alle drei** Komponenten gelten
    (A-1: keine Teilbewegung, sie verfälschte die Bahnellipse). :math:`|\hat v| = 0` zählt als
    bewegt (Auslenkung 0, gültig).

    Parameters
    ----------
    amplitude : array_like
        ``(P,)`` oder ``(P, 3)``, komplex.
    kohaerenz_ok : array_like of bool
        Maske :math:`\gamma^2 \ge \gamma^2_\mathrm{min}`, gleiche Form wie ``amplitude``.
    gueltig : array_like of bool, optional
        M6-Gültigkeit, ``(P,)`` oder gleiche Form wie ``amplitude``; ``None`` = alle gültig.

    Returns
    -------
    numpy.ndarray
        ``(P,)`` bool.

    Raises
    ------
    ValueError
        Bei unverträglichen Formen.
    """
    a = np.asarray(amplitude, dtype=np.complex128)
    ok = np.asarray(kohaerenz_ok, dtype=bool)
    if a.ndim not in (1, 2) or (a.ndim == 2 and a.shape[1] != _KOMPONENTEN_3D):
        raise ValueError(f"amplitude (P,) oder (P, 3) erwartet: {a.shape}")
    if ok.shape != a.shape:
        raise ValueError(f"kohaerenz_ok braucht die Form der Amplitude: {ok.shape} != {a.shape}")
    maske = ok & np.isfinite(a)
    if gueltig is not None:
        g = np.asarray(gueltig, dtype=bool)
        if g.shape == (a.shape[0],) and a.ndim == 2:
            g = g[:, None]
        elif g.shape != a.shape:
            raise ValueError(f"gueltig braucht (P,) oder die Form der Amplitude: {g.shape}")
        maske = maske & g
    if a.ndim == 2:
        alle: npt.NDArray[np.bool_] = np.all(maske, axis=1)
        return alle
    return maske


def bezugsgroesse(d: npt.ArrayLike, bewegt: npt.ArrayLike) -> float | None:
    r""":math:`D_\mathrm{ref}`: größte Spitzenauslenkung unter den bewegten Punkten (FG-04 3.5).

    Einzelkomponente ``(P,)``: :math:`\max_p |\hat d_p|`. 3D ``(P, 3)``:
    :math:`\max_p` ``auslenkung_max`` der Bahnellipse von :math:`\hat d_p`, d. h.
    :math:`\max_p \texttt{auslenkung\_max}(\hat v_p)/\omega`. Nicht bewegte, nicht endliche
    Punkte gehen nicht ein (RF-A8).

    Parameters
    ----------
    d : array_like
        Auslenkungsamplitude (oder animierte Schnelle) ``(P,)`` bzw. ``(P, 3)``.
    bewegt : array_like of bool
        ``(P,)`` Maske, :func:`bewegt_maske`.

    Returns
    -------
    float or None
        ``None``, wenn kein bewegter Punkt vorhanden ist oder alle Beträge 0 sind (kein
        :math:`s`, FG-04 6; keine Division durch null).
    """
    a = np.asarray(d, dtype=np.complex128)
    maske = np.asarray(bewegt, dtype=bool)
    if a.ndim not in (1, 2) or (a.ndim == 2 and a.shape[1] != _KOMPONENTEN_3D):
        raise ValueError(f"d (P,) oder (P, 3) erwartet: {a.shape}")
    if maske.shape != (a.shape[0],):
        raise ValueError(f"bewegt (P,) erwartet: {maske.shape}")
    ausgewaehlt = a[maske]
    if ausgewaehlt.shape[0] == 0:
        return None
    groesse = np.abs(ausgewaehlt) if a.ndim == 1 else ellipse_kennwerte(ausgewaehlt)[1]
    groesse = groesse[np.isfinite(groesse)]
    if groesse.size == 0:
        return None
    maximum = float(np.max(groesse))
    return maximum if maximum > 0.0 else None


def waehle_bezugspunkt_3d(amplitude: npt.ArrayLike, bewegt: npt.ArrayLike) -> int | None:
    r"""Voreinstellung des 3D-Bezugspunkts (Nachtrag 1, A-3).

    Der bewegte Punkt mit der größten ``auslenkung_max`` (große Halbachse der Bahn); bei
    Gleichstand der kleinste Index. Punkte mit :math:`\hat{\vec v} = 0` scheiden aus.

    Parameters
    ----------
    amplitude : array_like
        ``(P, 3)``, komplex.
    bewegt : array_like of bool
        ``(P,)`` Maske, :func:`bewegt_maske`.

    Returns
    -------
    int or None
        ``None``, wenn kein bewegter Punkt mit :math:`\hat{\vec v} \neq 0` existiert.
    """
    a = np.asarray(amplitude, dtype=np.complex128)
    maske = np.asarray(bewegt, dtype=bool)
    if a.ndim != 2 or a.shape[1] != _KOMPONENTEN_3D:
        raise ValueError(f"amplitude (P, 3) erwartet: {a.shape}")
    if maske.shape != (a.shape[0],):
        raise ValueError(f"bewegt (P,) erwartet: {maske.shape}")
    with np.errstate(invalid="ignore", divide="ignore"):  # nicht endliche Zeilen scheiden aus
        gross = ellipse_kennwerte(a)[1]
    kandidaten = maske & np.isfinite(gross) & (gross > 0.0)
    if not np.any(kandidaten):
        return None
    return int(np.argmax(np.where(kandidaten, gross, -np.inf)))


def positionen_m(
    koordinaten_m: npt.ArrayLike,
    d: npt.ArrayLike,
    theta_rad: float,
    ueberhoehung: float,
    bewegt: npt.ArrayLike,
) -> FloatArray:
    r"""Bildpositionen :math:`\vec x_p(\theta) = \vec X_p + s\,\mathrm{Re}\{\hat d_p e^{i\theta}\}`.

    Nicht bewegte Punkte liefern **exakt** :math:`\vec X_p` (Gleichheit, nicht Näherung;
    NaN in :math:`\hat d` dieser Zeilen wirkt sich nicht aus, RF-A8).

    Parameters
    ----------
    koordinaten_m : array_like
        Ruhelage ``(P, 3)`` in m.
    d : array_like
        Animierte Amplitude ``(P, 3)`` (Auslenkung in m bzw. m/N). Eine Einzelkomponente
        wird mit 0 in den anderen Spalten übergeben.
    theta_rad : float
        Animationswinkel in rad (Skalar).
    ueberhoehung : float
        Faktor :math:`s` (dimensionslos), für alle Punkte gleich.
    bewegt : array_like of bool
        ``(P,)`` Maske der bewegten Punkte.
    """
    x = np.asarray(koordinaten_m, dtype=np.float64)
    a = np.asarray(d, dtype=np.complex128)
    maske = np.asarray(bewegt, dtype=bool)
    if x.ndim != 2 or x.shape[1] != _KOMPONENTEN_3D or a.shape != x.shape:
        raise ValueError(f"koordinaten_m und d brauchen die Form (P, 3): {x.shape}, {a.shape}")
    if maske.shape != (x.shape[0],):
        raise ValueError(f"bewegt (P,) erwartet: {maske.shape}")
    if np.ndim(theta_rad) != 0:
        raise ValueError("theta_rad muss ein Skalar sein")
    auslenkung = np.zeros(x.shape, dtype=np.float64)
    auslenkung[maske] = verschiebung(a[maske], theta_rad)
    ergebnis: FloatArray = np.where(maske[:, None], x + ueberhoehung * auslenkung, x)
    return ergebnis


def ueberhoehung_auto(
    d_nn_m: float | None, d_ref: float | None, alpha: float = ALPHA_VORGABE
) -> float | None:
    r"""Automatische Überhöhung :math:`s = \alpha\,d_\mathrm{NN}/D_\mathrm{ref}` (FG-04 3.5).

    Parameters
    ----------
    d_nn_m : float or None
        Median der Abstände zum nächsten Nachbarn in m; ``None`` bei nur einem Punkt.
    d_ref : float or None
        Bezugsgröße :func:`bezugsgroesse`.
    alpha : float
        Größte angezeigte Auslenkung in Einheiten von :math:`d_\mathrm{NN}`.

    Returns
    -------
    float or None
        :math:`s`; ``None``, wenn :math:`d_\mathrm{NN}` oder :math:`D_\mathrm{ref}` fehlt oder
        nicht positiv ist (dann nur durch Nutzereingabe).

    Raises
    ------
    ValueError
        Bei ``alpha`` nicht positiv oder nicht endlich, auch wenn sonst kein :math:`s` berechnet
        wird.
    """
    if not (math.isfinite(alpha) and alpha > 0.0):
        raise ValueError(f"alpha > 0 erwartet: {alpha}")
    if d_nn_m is None or d_ref is None:
        return None
    if not (math.isfinite(d_nn_m) and math.isfinite(d_ref) and d_nn_m > 0.0 and d_ref > 0.0):
        return None
    return alpha * d_nn_m / d_ref


def _nicht_negativ(wert: float) -> bool:
    """Prüft, ob ``wert`` endlich und nicht negativ ist."""
    return math.isfinite(wert) and wert >= 0.0


def ueberhoehung_hinweis(ueberhoehung: float, d_ref: float, d_nn_min_m: float) -> str | None:
    r"""Hinweis, wenn :math:`s\,D_\mathrm{ref} \ge d_\mathrm{NN,min}/2` (FG-04 3.5).

    Nur ein Hinweis, keine Sperre: Ab dieser Grenze können sich zwei Nachbarn in der
    Bildebene treffen.

    Returns
    -------
    str or None
        :data:`HINWEIS_UEBERLAGERUNG` oder ``None``.

    Raises
    ------
    ValueError
        Wenn ``ueberhoehung``, ``d_ref`` oder ``d_nn_min_m`` NaN, nicht endlich oder negativ
        ist; ein Eingabefehler wird nicht still als „kein Hinweis“ gewertet.
    """
    if not (_nicht_negativ(ueberhoehung) and _nicht_negativ(d_ref) and _nicht_negativ(d_nn_min_m)):
        raise ValueError(
            "ueberhoehung, d_ref und d_nn_min_m endlich und nicht negativ erwartet: "
            f"{ueberhoehung}, {d_ref}, {d_nn_min_m}"
        )
    if ueberhoehung * d_ref >= 0.5 * d_nn_min_m:
        return HINWEIS_UEBERLAGERUNG
    return None


def maximum_theta(phase_rad: npt.ArrayLike, groesse: Groesse = "auslenkung") -> FloatArray:
    r"""Winkel des positiven Maximums :math:`\theta_{\max}` (FG-04 3.3).

    Auslenkung :math:`\pi/2 - \varphi`, Schnelle :math:`-\varphi`, jeweils mod :math:`2\pi`.

    Parameters
    ----------
    phase_rad : array_like
        Dargestellte Phase :math:`\varphi` in rad (absolut :math:`\arg\hat v` bzw. relativ
        :math:`\arg\hat w`).
    groesse : {"auslenkung", "schnelle"}

    Returns
    -------
    numpy.ndarray
        :math:`\theta_{\max} \in [0, 2\pi)` in rad.
    """
    if groesse not in ("auslenkung", "schnelle"):
        raise ValueError(f"groesse 'auslenkung' oder 'schnelle' erwartet: {groesse!r}")
    phi = np.asarray(phase_rad, dtype=np.float64)
    versatz = math.pi / 2.0 if groesse == "auslenkung" else 0.0
    with np.errstate(invalid="ignore"):  # NaN/Inf-Phase ergibt NaN
        ergebnis: FloatArray = np.mod(versatz - phi, 2.0 * math.pi)
    # Rundung kann nahe einem Vielfachen von 2π genau 2π ergeben; der Wertebereich ist [0, 2π)
    ergebnis = np.where(ergebnis >= 2.0 * math.pi, 0.0, ergebnis)
    return ergebnis


def bildwinkel(n: int) -> FloatArray:
    r"""Bildwinkel :math:`\theta_j = 2\pi j/N`, :math:`j = 0 \dots N-1` (FG-04 3.7).

    Das Bild bei :math:`2\pi` kommt **nicht** vor (Duplikat von :math:`j = 0`).

    Raises
    ------
    ValueError
        Bei ``n`` kein ganzzahliger Wert (auch kein ganzzahliger Float) oder ``n < 1``.
    """
    if not isinstance(n, (int, np.integer)) or n < 1:
        raise ValueError(f"ganzzahliges n >= 1 erwartet: {n!r}")
    ergebnis: FloatArray = 2.0 * math.pi * np.arange(n, dtype=np.float64) / n
    return ergebnis


def phasenfehler_grenze(n: int) -> tuple[float, float]:
    r"""Fehler durch :math:`N` Bilder je Periode (FG-04 3.7).

    Returns
    -------
    delta_phi_rad : float
        Größter dargestellter Phasenfehler :math:`\pi/N`.
    amplitude_rel : float
        Größte Unterschreitung der Spitzenauslenkung :math:`\Delta A/A = 1 - \cos(\pi/N)`
        (hier als :math:`2\sin^2(\pi/2N)` ausgewertet, gegen Auslöschung bei großem ``n``).

    Raises
    ------
    ValueError
        Bei ``n < 1``.
    """
    if n < 1:
        raise ValueError(f"n >= 1 Bilder je Periode erwartet: {n}")
    halb = math.pi / (2.0 * n)
    return math.pi / n, 2.0 * math.sin(halb) ** 2
