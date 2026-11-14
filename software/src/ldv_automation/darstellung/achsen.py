"""Achsenoptionen der Zeichenfunktionen: feste Bereiche und Skalen (R-073, P-AUSW2 S1).

Oberfläche, Arbeitsbild und Thesis-Skript steuern die Achsen über **dieselbe** Option
:class:`AchsenOptionen` (eine Quelle, ADR-028): ein Bereich je Achse (``None`` = automatisch,
je Seite) und die Skala der Frequenzachse. Die Skala der Amplitude bleibt in ``Optionen.skala``
der jeweiligen Zeichenfunktion. ``achsen=None`` (Voreinstellung) lässt das Verhalten der
Zeichenfunktionen unverändert (Thesis-Abbildungen bitgleich, Regressionstest).

Einheiten: Frequenz in Hz, Betrag in der Einheit der Größe, Phase in **Grad** (Anzeigegrenze,
KONVENTIONEN). Dieses Modul rechnet nichts Fachliches; es setzt nur Achsengrenzen und prüft
Eingaben.

Keine Qt-, keine ``pyplot``-Importe (ADR-021).
"""

from __future__ import annotations

import math
import re
from collections.abc import Mapping, Sequence
from dataclasses import dataclass, field
from decimal import Decimal

import matplotlib
import numpy as np
from matplotlib.axes import Axes
from matplotlib.ticker import Formatter

from .formate import MINUS, tick_text, zahl_text
from .zeichnung import Skala

__all__ = [
    "TEXT_KEINE_ZAHL",
    "TEXT_LOG_NUR_POSITIV",
    "TEXT_REIHENFOLGE",
    "AchsenFehler",
    "AchsenOptionen",
    "Bereich",
    "feld_text",
    "nebenticks_log",
    "parse_zahl",
    "pruefe_bereich",
    "sichtbare_y_grenzen",
    "uebernehme_eingabe",
    "wende_bereich_an",
    "wende_frequenz_an",
    "wende_y_an",
    "wende_y_gruppe_an",
]

TEXT_REIHENFOLGE = "Unterer Wert muss kleiner sein als der obere."
"""Meldung bei „von“ ≥ „bis“ (Brief 3.1, ohne Symbol; die Oberfläche setzt ✖ davor)."""
TEXT_LOG_NUR_POSITIV = "Bei logarithmischer Achse nur Werte größer null."
"""Meldung bei Wert ≤ 0 auf einer logarithmischen Achse (Brief 3.1)."""
TEXT_KEINE_ZAHL = "Bitte eine Zahl eingeben (leer = Auto)."
"""Meldung bei nicht-numerischer Eingabe (Text, NaN, Unendlich)."""


class AchsenFehler(ValueError):  # noqa: N818  (deutscher Projektname wie DarstellungsFehler)
    """Ungültiger Achsenbereich; ``str(fehler)`` ist die Meldung für die Oberfläche.

    Attributes
    ----------
    achse : str
        Name der betroffenen Achse (z. B. ``"Frequenz"``), leer wenn unbekannt.
    """

    def __init__(self, text: str, achse: str = "") -> None:
        super().__init__(text)
        self.achse = achse


@dataclass(frozen=True)
class Bereich:
    """Sichtbarer Bereich einer Achse; ``None`` = automatisch (je Seite).

    Attributes
    ----------
    von, bis : float or None
        Untere und obere Grenze in der Einheit der Achse (Hz, Einheit der Größe, Grad).
    """

    von: float | None = None
    bis: float | None = None

    @property
    def ist_auto(self) -> bool:
        """Beide Seiten automatisch."""
        return self.von is None and self.bis is None


@dataclass(frozen=True)
class AchsenOptionen:
    """Achsenwahl einer Zeichenfunktion (R-073).

    Attributes
    ----------
    frequenz : Bereich
        Sichtbarer Frequenzbereich in Hz (gemeinsame x-Achse aller Teilbilder).
    frequenz_skala : {"linear", "log"}
        Skala der Frequenzachse; logarithmisch nur mit positiven Grenzen.
    y : mapping of str to Bereich
        Bereich der y-Achse je Rolle (``"betrag"``, ``"phase"`` in Grad); fehlende Rolle =
        automatisch.
    """

    frequenz: Bereich = field(default_factory=Bereich)
    frequenz_skala: Skala = "linear"
    y: Mapping[str, Bereich] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if self.frequenz_skala not in ("linear", "log"):
            raise ValueError(f"unbekannte Skala {self.frequenz_skala!r}")

    def y_bereich(self, rolle: str) -> Bereich:
        """Bereich der y-Achse der Rolle (automatisch, wenn nicht gesetzt)."""
        return self.y.get(rolle, Bereich())


# --- Eingabe -----------------------------------------------------------------------------------


_HOCH = "⁰¹²³⁴⁵⁶⁷⁸⁹"
_POTENZ = re.compile(rf"^(?P<vz>[+-]?)10(?P<exp>[⁻⁺]?[{_HOCH}]+)$")
"""Zehnerpotenz in Hochzahlschreibweise („10⁻⁷“, optional mit Vorzeichen davor)."""
_MAL = chr(0xD7)  # Multiplikationszeichen
_HOCH_ZEICHEN = str.maketrans("0123456789-", "⁰¹²³⁴⁵⁶⁷⁸⁹⁻")
_MALZEICHEN = re.compile(rf"\s*[·{_MAL}*]\s*")
FELD_SIGNIFIKANT = 4
"""Signifikante Stellen der Anzeige im Feld, für Dezimal- und Potenzschreibweise einheitlich."""
_DEZIMAL_VON = Decimal("1e-3")
_DEZIMAL_BIS = Decimal("1e6")
"""Beträge in ``[1e-3, 1e6)`` stehen im Feld dezimal, alle anderen als Potenz (Feldbreite)."""
_GROESSTE_ANZEIGE = "1.797e+308"
"""Anzeige nahe dem Maximum: abgeschnitten statt gerundet, damit der Text einlesbar bleibt."""
_EXPONENT_STELLEN_MAX = 6
"""Mehr Ziffern hat kein gültiger Exponent (float reicht bis ±324); längere werden abgelehnt."""
_NICHT_NULL = frozenset("123456789")


def _dezimal_zahl(roh: str) -> float:
    """Zahl in Dezimalschreibweise (Komma oder Punkt, auch mit ``e``) als endlicher float.

    Nur ASCII-Ziffern (``float`` nähme auch Ziffern anderer Schriften und Vollbreite). Ein
    Betrag ungleich null, der zu 0 unterläuft („1e-400“), ist ungültig, kein stilles 0.
    """
    if "_" in roh or ("," in roh and "." in roh) or not roh.isascii():
        raise AchsenFehler(TEXT_KEINE_ZAHL)
    try:
        wert = float(roh.replace(",", "."))
    except ValueError:
        raise AchsenFehler(TEXT_KEINE_ZAHL) from None
    if not math.isfinite(wert):
        raise AchsenFehler(TEXT_KEINE_ZAHL)
    if wert == 0.0 and not _NICHT_NULL.isdisjoint(re.split("[eE]", roh)[0]):
        raise AchsenFehler(TEXT_KEINE_ZAHL)  # Unterlauf
    return wert


def _potenz_zahl(roh: str) -> float | None:
    """Zahl in Potenzschreibweise („1,4·10⁻⁷“, „10⁻⁵“) oder ``None``, wenn es keine ist.

    Raises
    ------
    AchsenFehler
        Mantisse keine Zahl, Ergebnis über- oder unterläuft (nicht darstellbar).
    """
    teile = _MALZEICHEN.split(roh, maxsplit=1)
    if len(teile) == 2:
        mantisse_text, potenz_text = teile
        potenz = _POTENZ.match(potenz_text)
        if potenz is None or "e" in mantisse_text.lower():
            return None
        if potenz["vz"]:
            return None  # „1,4·-10⁻⁷“ ist keine Zahl
        mantisse = _dezimal_zahl(mantisse_text)
        mantisse_text = mantisse_text.replace(",", ".")
    else:
        potenz = _POTENZ.match(roh)
        if potenz is None:
            return None
        mantisse_text = "-1" if potenz["vz"] == "-" else "1"
        mantisse = float(mantisse_text)
    zeichen = {"⁻": "-", "⁺": "+"}.get(potenz["exp"][0], "")
    ziffern = potenz["exp"][1:] if zeichen else potenz["exp"]
    ziffern = "".join(str(_HOCH.index(z)) for z in ziffern).lstrip("0") or "0"
    if mantisse == 0.0:
        return mantisse  # 0·10ⁿ ist 0, auch bei riesigem n
    if len(ziffern) > _EXPONENT_STELLEN_MAX:
        raise AchsenFehler(TEXT_KEINE_ZAHL)  # weit außerhalb von float
    # Dezimaltext statt 10.0**n: keine Rundung dazu; die Mantisse behält ihre Schreibweise.
    wert = float(f"{mantisse_text}e{zeichen}{ziffern}")
    if not math.isfinite(wert) or wert == 0.0:
        raise AchsenFehler(TEXT_KEINE_ZAHL)  # Über- bzw. Unterlauf
    return wert


def parse_zahl(text: str) -> float | None:
    """Liest eine Zahl aus einem Eingabefeld; leer ergibt ``None``.

    Erlaubt sind Dezimalkomma und -punkt („1200,5“), die Exponentenschreibweise („1,4e-7“) und
    die Potenzschreibweise des Felds („1,4·10⁻⁷“, auch mit Malzeichen oder „*“ statt „·“, und
    „10⁻⁵“ ohne Mantisse), also alles, was :func:`feld_text` ausgibt (Rundreise Feld, Wert, Feld).

    Parameters
    ----------
    text : str
        Eingabe; Leerraum am Rand und das typografische Minus (U+2212) sind erlaubt. Tausender-
        trennzeichen und Unterstriche gibt es nicht: Komma **und** Punkt zugleich sind ungültig.

    Raises
    ------
    AchsenFehler
        Keine endliche Zahl.
    """
    roh = text.strip().replace(MINUS, "-")
    if not roh:
        return None
    potenz = _potenz_zahl(roh)
    return potenz if potenz is not None else _dezimal_zahl(roh)


def feld_text(wert: float | None) -> str:
    """Wert für ein Eingabefeld: lesbar und umkehrbar durch :func:`parse_zahl`.

    ``None`` ergibt leer, ``0`` (auch ``-0``) ergibt „0“. Beträge von 10⁻³ bis unter 10⁶ stehen
    dezimal mit Dezimalkomma, alle übrigen als Potenz („1,4·10⁻⁷“, negativ mit typografischem
    Minus), beide mit höchstens :data:`FELD_SIGNIFIKANT` signifikanten Stellen („1200“,
    „0,01235“). Die Anzeige rundet nur; der gespeicherte Wert bleibt unverändert. Subnormale
    Werte stehen mit derselben Stellenzahl da, Werte nahe dem Maximum werden abgeschnitten
    statt gerundet („1,797·10³⁰⁸“), damit der Text einlesbar bleibt.
    """
    if wert is None:
        return ""
    zahl = float(wert)
    if not math.isfinite(zahl):
        return zahl_text(zahl, None, dezimalkomma=True)
    if zahl == 0.0:
        return "0"
    roh = f"{zahl:.{FELD_SIGNIFIKANT - 1}e}"
    if not math.isfinite(float(roh)):  # Aufrunden über das Maximum hinaus
        roh = ("-" if zahl < 0 else "") + _GROESSTE_ANZEIGE
    # Die Schreibweise folgt dem **gerundeten** Wert, damit Text, Wert und Text stabil bleiben
    # („9,9999·10⁻⁴“ wird zu „0,001“ und nicht zu „10⁻³“, das beim Einlesen „0,001“ ergäbe).
    gerundet = Decimal(roh)
    if _DEZIMAL_VON <= abs(gerundet) < _DEZIMAL_BIS:
        text = format(gerundet, "f")
        if "." in text:
            text = text.rstrip("0").rstrip(".")
    else:
        mantisse, exponent = roh.split("e")
        mantisse = mantisse.rstrip("0").rstrip(".")
        potenz = "10" + str(int(exponent)).translate(_HOCH_ZEICHEN)
        text = {"1": potenz, "-1": f"-{potenz}"}.get(mantisse, f"{mantisse}·{potenz}")
    return text.replace(".", ",").replace("-", MINUS)


def uebernehme_eingabe(
    text: str, seite: str, alt: Bereich, skala: Skala, name: str = ""
) -> Bereich:
    """Neuer Bereich aus dem Text eines Felds („von“ oder „bis“); prüft nur **gesetzte** Werte.

    Eine einseitig gesetzte Eingabe wird nicht gegen die automatische Gegenseite geprüft: Liegt
    sie jenseits davon, verschiebt die Zeichenschicht die Auto-Seite (:func:`_wirksam`), genau
    so, wie die Achsenleiste es danach anzeigt (eine Regel für Leiste und Zeichnung).

    Parameters
    ----------
    text : str
        Eingabe des Felds (leer = Auto).
    seite : {"von", "bis"}
        Das Feld, aus dem der Text stammt.
    alt : Bereich
        Bisheriger Bereich der Achse.
    skala : {"linear", "log"}
        Skala der Achse (log: nur Werte größer null).
    name : str, optional
        Name der Achse für :attr:`AchsenFehler.achse`.

    Raises
    ------
    AchsenFehler
        Keine Zahl; Wert ≤ 0 auf der Logarithmusachse; „von“ ≥ „bis“ bei zwei gesetzten Seiten.
    """
    try:
        wert = parse_zahl(text)
    except AchsenFehler as fehler:
        raise AchsenFehler(str(fehler), name) from None
    neu = Bereich(wert, alt.bis) if seite == "von" else Bereich(alt.von, wert)
    pruefe_bereich(neu, skala, name)
    return neu


def pruefe_bereich(bereich: Bereich, skala: Skala, name: str = "") -> None:
    """Prüft einen (teilweise) gesetzten Bereich.

    Parameters
    ----------
    bereich : Bereich
        Zu prüfender Bereich; ``None``-Seiten werden nicht geprüft.
    skala : {"linear", "log"}
        Skala der Achse.
    name : str, optional
        Name der Achse für :attr:`AchsenFehler.achse`.

    Raises
    ------
    AchsenFehler
        Wert keine endliche Zahl (:data:`TEXT_KEINE_ZAHL`); auf der Logarithmusachse Wert ≤ 0
        (:data:`TEXT_LOG_NUR_POSITIV`); „von“ ≥ „bis“ (:data:`TEXT_REIHENFOLGE`).
    """
    werte = [w for w in (bereich.von, bereich.bis) if w is not None]
    if not all(math.isfinite(w) for w in werte):
        raise AchsenFehler(TEXT_KEINE_ZAHL, name)
    if skala == "log" and any(w <= 0.0 for w in werte):
        raise AchsenFehler(TEXT_LOG_NUR_POSITIV, name)
    if bereich.von is not None and bereich.bis is not None and bereich.von >= bereich.bis:
        raise AchsenFehler(TEXT_REIHENFOLGE, name)


# --- Anwenden auf eine Achse -------------------------------------------------------------------


def _wirksam(
    bereich: Bereich, auto: tuple[float, float], skala: Skala, name: str
) -> tuple[float, float]:
    """Wirksame Grenzen aus gesetzten Seiten und den automatischen Grenzen ``auto``.

    Zwei gesetzte Seiten müssen gültig sein (:func:`pruefe_bereich`). Ist nur eine Seite gesetzt
    und läge sie jenseits der automatischen Gegenseite (z. B. nach einem Wechsel der Daten),
    wird die automatische Seite um die automatische Spanne verschoben (linear: Summe, log:
    Produkt), damit die gesetzte Seite erhalten bleibt und die Achse nie umgekehrt wird.
    """
    pruefe_bereich(bereich, skala, name)
    log = skala == "log"
    von = bereich.von if bereich.von is not None else auto[0]
    bis = bereich.bis if bereich.bis is not None else auto[1]
    if von >= bis and (bereich.von is None or bereich.bis is None):
        if log:
            faktor = auto[1] / auto[0] if auto[0] > 0 and auto[1] > auto[0] else 10.0
            if bereich.bis is None:
                bis = von * faktor
            else:
                von = bis / faktor
        else:
            spanne = auto[1] - auto[0] if auto[1] > auto[0] else 1.0
            if bereich.bis is None:
                bis = von + spanne
            else:
                von = bis - spanne
    if log and (von <= 0.0 or bis <= 0.0):
        raise AchsenFehler(TEXT_LOG_NUR_POSITIV, name)
    if not von < bis:
        raise AchsenFehler(TEXT_REIHENFOLGE, name)
    return von, bis


def _kleinste_positive_x(ax: Axes, f_max_hz: float) -> float:
    """Kleinste positive x-Koordinate der sichtbaren Linien (untere Auto-Grenze auf log-Achse).

    Beginnt die Frequenzachse bei 0 Hz (``k0 = 0``), gilt die automatische untere Grenze nur
    aus den positiven Frequenzen. Gibt es keine, dient ``f_max_hz / 1000`` (drei Dekaden).

    Raises
    ------
    AchsenFehler
        Auch ``f_max_hz`` ist nicht positiv (kein Logarithmus möglich).
    """
    kandidaten = []
    for linie in ax.get_lines():
        if not linie.get_visible():
            continue
        x = np.asarray(linie.get_xdata(), dtype=np.float64)
        positiv = x[np.isfinite(x) & (x > 0.0)]
        if positiv.size:
            kandidaten.append(float(positiv.min()))
    if kandidaten:
        return min(kandidaten)
    if f_max_hz > 0.0:
        return f_max_hz / 1000.0
    raise AchsenFehler(TEXT_LOG_NUR_POSITIV, "Frequenz")


def wende_frequenz_an(ax: Axes, achsen: AchsenOptionen, f_min_hz: float, f_max_hz: float) -> bool:
    """Setzt Skala und Grenzen der Frequenzachse (nach dem Zeichnen der Linien).

    Parameters
    ----------
    ax : Axes
        Achse (bei geteilter x-Achse genügt eine).
    achsen : AchsenOptionen
        Gewählte Achsen.
    f_min_hz, f_max_hz : float
        Datenbereich in Hz (Auto-Grenzen). Auf der Logarithmusachse mit ``f_min_hz <= 0`` gilt
        als untere Auto-Grenze die kleinste positive Frequenz der Linien.

    Returns
    -------
    bool
        ``True``, wenn mindestens eine Seite gesetzt ist (y-Auto folgt dann dem sichtbaren
        Frequenzbereich, siehe :func:`wende_y_an`).

    Raises
    ------
    AchsenFehler
        Ungültiger Bereich (siehe :func:`pruefe_bereich`).
    """
    auto = (f_min_hz, f_max_hz)
    if achsen.frequenz_skala == "log" and f_min_hz <= 0.0:
        auto = (_kleinste_positive_x(ax, f_max_hz), f_max_hz)  # 0 Hz hat keinen Logarithmus
    von, bis = _wirksam(achsen.frequenz, auto, achsen.frequenz_skala, "Frequenz")
    if achsen.frequenz_skala == "log":
        ax.set_xscale("log")
    ax.set_xlim(von, bis)
    return not achsen.frequenz.ist_auto


def sichtbare_y_grenzen(ax: Axes, *, log: bool) -> tuple[float, float] | None:
    """Automatische y-Grenzen über die Daten **im sichtbaren x-Bereich** (Annahme E6).

    Berücksichtigt alle sichtbaren Linien der Achse (auch Marker); auf der Logarithmusachse nur
    Werte > 0. Dazu kommt der Rand ``axes.ymargin`` (Voreinstellung 5 %) wie bei der
    Autoskalierung von matplotlib, auf der Logarithmusachse im Logarithmus.

    Returns
    -------
    tuple of float or None
        ``(unten, oben)`` oder ``None``, wenn im sichtbaren Bereich keine Daten liegen.
    """
    x_unten, x_oben = sorted(float(v) for v in ax.get_xlim())
    unten = math.inf
    oben = -math.inf
    for linie in ax.get_lines():
        if not linie.get_visible():
            continue
        x = np.asarray(linie.get_xdata(), dtype=np.float64)
        y = np.asarray(linie.get_ydata(), dtype=np.float64)
        if x.shape != y.shape:
            continue
        maske = np.isfinite(x) & np.isfinite(y) & (x >= x_unten) & (x <= x_oben)
        if log:
            maske &= y > 0.0
        if not maske.any():
            continue
        unten = min(unten, float(y[maske].min()))
        oben = max(oben, float(y[maske].max()))
    if not (math.isfinite(unten) and math.isfinite(oben)):
        return None
    rand = float(matplotlib.rcParams["axes.ymargin"])
    a, b = (math.log10(unten), math.log10(oben)) if log else (unten, oben)
    if b > a:
        pad = rand * (b - a)
    else:  # alle Werte gleich: symmetrischer Rand wie matplotlibs nonsingular
        pad = 0.05 * abs(a) if (a != 0.0 and not log) else (0.05 if log else 0.5)
    a, b = a - pad, b + pad
    return (10.0**a, 10.0**b) if log else (a, b)


def wende_y_an(ax: Axes, bereich: Bereich, *, log: bool, x_gesetzt: bool, name: str = "") -> None:
    """Setzt die y-Grenzen: gesetzte Seiten fest, die übrigen automatisch.

    Ist nichts gesetzt und der Frequenzbereich automatisch, bleibt die Autoskalierung der Achse
    unverändert. Ist der Frequenzbereich gesetzt, skaliert die automatische Seite über den
    sichtbaren Bereich (:func:`sichtbare_y_grenzen`).

    Raises
    ------
    AchsenFehler
        Ungültiger Bereich (siehe :func:`pruefe_bereich`).
    """
    skala: Skala = "log" if log else "linear"
    if bereich.ist_auto and not x_gesetzt:
        return
    auto = sichtbare_y_grenzen(ax, log=log) if x_gesetzt else None
    if auto is None:
        auto = (float(ax.get_ylim()[0]), float(ax.get_ylim()[1]))
    unten, oben = _wirksam(bereich, auto, skala, name)
    ax.set_ylim(unten, oben)


def wende_y_gruppe_an(
    achsen: Sequence[Axes], bereich: Bereich, *, log: bool, x_gesetzt: bool, name: str = ""
) -> None:
    """Wie :func:`wende_y_an` für Achsen mit **gemeinsamer** y-Achse (Teilbilder gleicher Größe).

    Die automatische Seite folgt den Daten aller Achsen der Gruppe (bei gesetztem
    Frequenzbereich über den sichtbaren Bereich), damit die gekoppelten Teilbilder dieselbe
    Spanne zeigen. Die Achsen müssen ``sharey`` verbinden; gesetzt wird einmal.

    Raises
    ------
    AchsenFehler
        Ungültiger Bereich (siehe :func:`pruefe_bereich`).
    """
    skala: Skala = "log" if log else "linear"
    if bereich.ist_auto and not x_gesetzt:
        return
    autos = [a for ax in achsen if (a := sichtbare_y_grenzen(ax, log=log)) is not None]
    if x_gesetzt and autos:
        auto = (min(a[0] for a in autos), max(a[1] for a in autos))
    else:
        auto = (float(achsen[0].get_ylim()[0]), float(achsen[0].get_ylim()[1]))
    unten, oben = _wirksam(bereich, auto, skala, name)
    achsen[0].set_ylim(unten, oben)


def wende_bereich_an(ax: Axes, bereich: Bereich, auto: tuple[float, float], name: str = "") -> None:
    """Setzt die linearen y-Grenzen einer Achse mit festem Auto-Bereich ``auto`` (z. B. Phase).

    Ist nichts gesetzt, bleibt die Achse unverändert.

    Raises
    ------
    AchsenFehler
        Ungültiger Bereich (siehe :func:`pruefe_bereich`).
    """
    if bereich.ist_auto:
        return
    unten, oben = _wirksam(bereich, auto, "linear", name)
    ax.set_ylim(unten, oben)


# --- Beschriftung der Logarithmusachse -----------------------------------------------------------


class _LogNebenticks(Formatter):
    """Beschriftung der Nebenstriche (2 … 9 · 10ⁿ) einer Logarithmusachse mit Dezimalkomma.

    Ohne sie hätte ein enger Ausschnitt (z. B. 20 bis 80 Hz) keine einzige Beschriftung. Je
    kleiner die sichtbare Spanne (Verhältnis oben/unten), desto mehr Nebenstriche tragen eine
    Zahl: unter 10 alle, unter 100 nur 2 und 5, darüber keine.
    """

    def __init__(self, *, dezimalkomma: bool) -> None:
        self._dezimalkomma = dezimalkomma

    def __call__(self, x: float, pos: int | None = None) -> str:
        if self.axis is None or x <= 0.0:
            return ""
        unten, oben = sorted(float(v) for v in self.axis.get_view_interval())
        if unten <= 0.0:
            return ""
        spanne = oben / unten
        mantisse = round(x / 10.0 ** math.floor(math.log10(x)))
        erlaubt = (2, 3, 4, 5, 6, 7, 8, 9) if spanne < 10 else (2, 5) if spanne < 100 else ()
        return tick_text(x, dezimalkomma=self._dezimalkomma) if mantisse in erlaubt else ""


def nebenticks_log(ax: Axes, *, dezimalkomma: bool = True) -> None:
    """Beschriftet die Nebenstriche der Logarithmusachsen von ``ax`` (x und y) mit Dezimalkomma."""
    for achse in (ax.xaxis, ax.yaxis):
        if achse.get_scale() == "log":
            achse.set_minor_formatter(_LogNebenticks(dezimalkomma=dezimalkomma))
