"""Zahlen- und Textformate der Darstellung: Dezimalkomma, Einheiten, Gradanzeige (P-AUSW T2).

Die Rechnung läuft in rad (KONVENTIONEN); die Umrechnung in Grad geschieht nur hier an der
Anzeigegrenze (:func:`grad`, :func:`winkel_text`).
"""

from __future__ import annotations

import math
from collections.abc import Sequence

import numpy as np
import numpy.typing as npt
from matplotlib.ticker import Formatter

__all__ = [
    "MINUS",
    "achsentitel",
    "dezimalkomma_formatter",
    "frequenz_text",
    "grad",
    "kennzeichen_unbestaetigt",
    "tick_text",
    "winkel_text",
    "zahl_signifikant_text",
    "zahl_text",
]

MINUS = chr(0x2212)
"""Typografisches Minuszeichen (wie ``axes.unicode_minus`` in matplotlib)."""

_DEZIMAL_GRENZE_UNTEN = 1e-3
_DEZIMAL_GRENZE_OBEN = 1e6
"""Zwischen diesen Beträgen steht die Dezimalschreibweise, sonst „m·10ⁿ“ (einheitliche Ticks)."""

_HOCH = str.maketrans("0123456789-", "⁰¹²³⁴⁵⁶⁷⁸⁹⁻")


def zahl_text(
    wert: float,
    stellen: int | None = None,
    *,
    dezimalkomma: bool = True,
    wissenschaftlich: bool | None = None,
) -> str:
    """Zahl als Text mit Dezimalkomma und typografischem Minus.

    Parameters
    ----------
    wert : float
        Zahl; NaN ergibt „–“, ±Inf ergibt „∞“ mit Vorzeichen.
    stellen : int, optional
        Nachkommastellen (fest); ``None`` = kürzeste Darstellung mit 6 signifikanten Stellen.
    dezimalkomma : bool, optional
        ``False`` behält den Dezimalpunkt.
    wissenschaftlich : bool, optional
        Nur ohne ``stellen``: ``True`` erzwingt „m·10ⁿ“ (0 bleibt „0“), ``False`` die
        Dezimalschreibweise, ``None`` entscheidet nach dem Betrag (Grenzen siehe Modul).
    """
    if math.isnan(wert):
        return "–"
    if math.isinf(wert):
        return ("" if wert > 0 else MINUS) + "∞"
    if stellen is not None:
        text = f"{wert:.{stellen}f}"
    elif wissenschaftlich is False:
        text = np.format_float_positional(wert, precision=6, fractional=False, trim="-")
    elif wert != 0.0 and (
        wissenschaftlich
        if wissenschaftlich is not None
        else not _DEZIMAL_GRENZE_UNTEN <= abs(wert) < _DEZIMAL_GRENZE_OBEN
    ):
        mantisse, exponent = f"{wert:.6e}".split("e")
        text = _wissenschaftlich(mantisse.rstrip("0").rstrip("."), int(exponent))
    else:
        text = f"{wert:.6g}"
    if "e" in text:
        mantisse, exponent = text.split("e")
        text = _wissenschaftlich(mantisse, int(exponent))
    if dezimalkomma:
        text = text.replace(".", ",")
    return text.replace("-", MINUS)


def _wissenschaftlich(mantisse: str, exponent: int) -> str:
    potenz = "10" + str(exponent).translate(_HOCH)
    return potenz if float(mantisse) == 1.0 else f"{mantisse}·{potenz}"


def tick_text(wert: float, *, dezimalkomma: bool = True) -> str:
    """Beschriftung eines Achsenstrichs („0,5“, „10⁻⁵“, „2·10⁻⁵“)."""
    return zahl_text(float(wert), None, dezimalkomma=dezimalkomma)


class _AchsenFormatter(Formatter):
    """Tickformat mit Dezimalkomma, **einheitlich je Achse** (kein „0,001“ neben „10⁻⁴“).

    Sobald die Achse die Tickpositionen meldet (``set_locs``), gilt für alle sichtbaren Ticks
    dieselbe Schreibweise: „m·10ⁿ“, wenn ein Tick ungleich null außerhalb von
    ``[10⁻³, 10⁶)`` liegt, sonst Dezimalschreibweise. Ohne Achse (Direktaufruf) entscheidet
    der Betrag je Wert (:func:`zahl_text`).
    """

    def __init__(self, *, dezimalkomma: bool) -> None:
        self._dezimalkomma = dezimalkomma
        self._wissenschaftlich: bool | None = None

    def set_locs(self, locs: list[float]) -> None:
        super().set_locs(locs)
        werte = [float(w) for w in np.asarray(locs, dtype=np.float64).ravel()]
        if self.axis is not None:
            unten, oben = sorted(float(w) for w in self.axis.get_view_interval())
            spanne = oben - unten
            werte = [w for w in werte if unten - 1e-9 * spanne <= w <= oben + 1e-9 * spanne]
        betraege = [abs(w) for w in werte if math.isfinite(w) and w != 0.0]
        ausserhalb = any(not _DEZIMAL_GRENZE_UNTEN <= b < _DEZIMAL_GRENZE_OBEN for b in betraege)
        self._wissenschaftlich = True if ausserhalb else None  # None: alle Ticks im Dezimalbereich

    def __call__(self, x: float, pos: int | None = None) -> str:
        return zahl_text(
            float(x), None, dezimalkomma=self._dezimalkomma, wissenschaftlich=self._wissenschaftlich
        )


def dezimalkomma_formatter(*, dezimalkomma: bool = True) -> Formatter:
    """Formatter für Achsenstriche mit Dezimalkomma, einheitlich je Achse (siehe Tests)."""
    return _AchsenFormatter(dezimalkomma=dezimalkomma)


def zahl_signifikant_text(wert: float, signifikant: int = 2, *, dezimalkomma: bool = True) -> str:
    """Zahl mit fester Anzahl signifikanter Stellen, z. B. ζ: 0,0058 bzw. 0,00012.

    Der Wert wird zuerst auf ``signifikant`` Stellen gerundet; die Nachkommastellen ergeben
    sich daraus (kleine Werte behalten ihre führenden Nullen, ohne Nullen am Ende zu verlieren).
    NaN ergibt „–“, ±Inf „∞“, null „0“ (auch ``-0.0``, nie ein Minus vor der Null).

    Parameters
    ----------
    wert : float
        Zahl, z. B. ein Dämpfungsgrad ζ (dimensionslos).
    signifikant : int, optional
        Anzahl signifikanter Stellen (≥ 1).
    dezimalkomma : bool, optional
        ``False`` behält den Dezimalpunkt.
    """
    if signifikant < 1:
        raise ValueError(f"signifikant muss ≥ 1 sein: {signifikant}")
    if wert == 0.0:
        return "0"  # auch -0.0: kein Minus vor der Null
    if not math.isfinite(wert):
        return zahl_text(wert, None, dezimalkomma=dezimalkomma)
    gerundet = float(f"{wert:.{signifikant - 1}e}")
    nach_komma = max(0, signifikant - 1 - math.floor(math.log10(abs(gerundet))))
    return zahl_text(gerundet, nach_komma, dezimalkomma=dezimalkomma)


def frequenz_text(f_hz: float, stellen: int = 3, *, dezimalkomma: bool = True) -> str:
    """Frequenz mit Einheit und fester Zahl Nachkommastellen, z. B. „123,750 Hz“.

    Die Stellenzahl gilt auf jeder Größenordnung (auch ab 1000 Hz: „1234,568 Hz“), damit
    Frequenzen untereinander vergleichbar sind (KONVENTIONEN, Zahlenformate).
    """
    text = zahl_text(round(f_hz, stellen) + 0.0, stellen, dezimalkomma=dezimalkomma)
    return f"{text} Hz"


def achsentitel(groesse: str, einheit: str) -> str:
    """Achsentitel „Größe [Einheit]“ (KONVENTIONEN); ``einheit`` ``"1"`` für dimensionslos."""
    return f"{groesse} [{einheit}]"


def grad(winkel_rad: npt.ArrayLike) -> npt.NDArray[np.float64]:
    """Winkel von rad in Grad (nur zur Anzeige)."""
    return np.degrees(np.asarray(winkel_rad, dtype=np.float64))


def winkel_text(winkel_rad: float, stellen: int = 1, *, dezimalkomma: bool = True) -> str:
    """Winkel in Grad als Text, z. B. „-12,3°“ (typografisches Minus)."""
    if math.isnan(winkel_rad):
        return "–"
    wert = round(float(np.degrees(winkel_rad)), stellen)
    return zahl_text(wert + 0.0, stellen, dezimalkomma=dezimalkomma) + "°"


def kennzeichen_unbestaetigt(gruende: Sequence[str]) -> str:
    """Kennzeichentext „unbestätigt (Grund; Grund)“ ohne Symbol (das setzt die Zeichenfunktion).

    Parameters
    ----------
    gruende : sequence of str
        Kurzbegründungen, in der Oberfläche aus ``AnnahmeEintrag.beschreibung``.
    """
    return "unbestätigt (" + "; ".join(gruende) + ")" if gruende else "unbestätigt"
