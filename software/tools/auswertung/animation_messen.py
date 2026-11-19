"""Messskript für den Messrechner: Leistung der 3D-Animation (R-071, Plan P-AUSW3 Abschnitt 6).

Die Rückfallstufen der Animation (ADR-029: L0 vereinfachte Achsen in Bewegung, L1 auch beim
Ziehen des Reglers, L2 Neuzeichnen beim Loslassen) und die Voreinstellungen von Bildrate, Tempo und
Stufe beruhen auf Zahlen eines Linux-Containers (Agg, ohne Fenster, ohne Remotedesktop). Dieses
Skript wiederholt die Messungen am Messrechner, **lokal und in der Remotedesktop-Sitzung**; die
Zahlen gehören in das Prüfprotokoll und sind **keine Bestanden-Aussage** (UI-38 bestätigt allein der
Nutzer nach der Prüfanleitung ``pruefanleitung_animation.md``).

Gemessen werden (Median und Maximum von ``--wiederholungen`` Wiederholungen, Voreinstellung 100):

``M1``
    Zeit je Bild: voll (Teilaktualisierung mit Achsen, Panes, Ticks), mit vereinfachten Achsen,
    Drehschritt (``view_init`` und Zeichnen), vereinfacht und voll. Wahl der Stufe L0 bis L2.
``M2``
    Effektive Bildrate der Wiedergabe bei Soll 5, 10 und 20 Bildern/s (``--dauer`` s je Rate) und
    Zahl der ausgelassenen Bilder (Voreinstellung der Bildrate).
``M3``
    Zeit vom Mausziehen (synthetische Ereignisse) bis zum sichtbaren Neuzeichnen.
``M4``
    Phasenregler ziehen (Teilaktualisierung je Schritt) und Loslassen (Voll-Neuzeichnen).
``M5``
    Zeit von ``animation_daten`` (drei Kanalpaare) kalt und warm und Zuwachs des Arbeitsspeichers.
``M6``
    Zeit, das Standbild als PNG und als PDF zu speichern (gleicher Pfad wie ``Bild speichern …``:
    ``speichere_arbeitsbild`` mit ``zeichne_animation``; Dateien nur in einem Temp-Ordner).

``M7`` (Nutzerurteil über Remotedesktop: flüssig? lesbar?) ist nicht automatisch messbar und steht
in der Prüfanleitung.

Aufruf (aus ``software/``; am Messrechner mit dem Python der Installation)::

    python tools/auswertung/animation_messen.py <datei.svd> [--sitzung lokal|remotedesktop]
        [--rechner "Name"] [--wiederholungen 100] [--dauer 10] [--frequenz 100.0]
        [--tabelle ergebnis.md] [--json ergebnis.json] [--ohne-qt]

Die Tabelle (Datei, Rechner, Sitzungsart, Versionen von Python, NumPy, matplotlib, PySide6) wird
ausgegeben und mit ``--tabelle`` als Markdown, mit ``--json`` als JSON geschrieben. Mit
``--ohne-qt`` laufen nur M5 und M6. Das Skript liest die Messdatei nur und schreibt nichts außer den
angegebenen Dateien. Es gehört nicht ins Wheel.
"""

from __future__ import annotations

import argparse
import json
import math
import platform
import statistics
import sys
import tempfile
import time
from collections.abc import Callable, Sequence
from dataclasses import dataclass, replace
from pathlib import Path

import matplotlib
import numpy as np
from speicher_messen import rss_mib

from ldv_automation.auswertung.annahmen import AnnahmenStufe2
from ldv_automation.auswertung.daten import Messdaten
from ldv_automation.auswertung.laden import Geladen, lade_svd
from ldv_automation.darstellung.animation3d import (
    AnimationsOptionen,
    Blick,
    aktualisiere_animation,
    zeichne_animation,
)
from ldv_automation.darstellung.animation_daten import AnimationsDaten, animation_daten
from ldv_automation.darstellung.auswahl import PaarCache
from ldv_automation.darstellung.bild import baue_stempel, speichere_arbeitsbild
from ldv_automation.darstellung.stil import Plotstil

__all__ = [
    "BILDRATEN",
    "Messwert",
    "blick_fuer_schritt",
    "main",
    "messe_daten",
    "messe_flaeche",
    "messe_speichern",
    "statistik",
    "tabelle_markdown",
    "tabelle_text",
]

BILDRATEN: tuple[int, ...] = (5, 10, 20)
"""Soll-Bildraten der Messung M2 (wie die Auswahl in Ansicht 4)."""

_MS = 1000.0
Zeit = Callable[[], float]


@dataclass(frozen=True)
class Messwert:
    """Eine Zeile der Ergebnistabelle.

    Attributes
    ----------
    nr, name : str
        Messpunkt (``"M1"`` …) und Beschreibung der Teilmessung.
    median_ms, max_ms : float or None
        Median und Maximum in Millisekunden; ``None``, wenn die Größe keine Zeit ist.
    n : int
        Zahl der Wiederholungen.
    notiz : str
        Weitere Kennzahl, z. B. „effektiv 9,8 Bilder/s, 3 ausgelassen“.
    """

    nr: str
    name: str
    median_ms: float | None
    max_ms: float | None
    n: int
    notiz: str = ""


def statistik(zeiten_s: Sequence[float]) -> tuple[float, float]:
    """Median und Maximum von Zeiten in s als Millisekunden.

    Raises
    ------
    ValueError
        Keine Zeiten.
    """
    if not zeiten_s:
        raise ValueError("Keine Zeiten zum Auswerten.")
    return statistics.median(zeiten_s) * _MS, max(zeiten_s) * _MS


def _wiederhole(
    n: int, aktion: Callable[[int], object], uhr: Zeit, *, aufwaermen: bool = False
) -> list[float]:
    """Führt ``aktion(i)`` ``n``-mal aus und gibt die Dauer jeder Ausführung in s zurück.

    Mit ``aufwaermen`` läuft vorher ein Schritt ``aktion(0)`` **außerhalb** der Zeitmessung
    (Schriftcache, erster Aufbau), damit er nicht als Maximum in die Zeile eingeht.
    """
    if aufwaermen:
        aktion(0)
    zeiten: list[float] = []
    for i in range(n):
        start = uhr()
        aktion(i)
        zeiten.append(uhr() - start)
    return zeiten


def blick_fuer_schritt(basis: Blick, i: int, *, drehen: bool) -> Blick:
    """Blick des ``i``-ten Schritts von M1: Azimut um ``i mod 90`` Grad gedreht, sonst gleich."""
    if not drehen:
        return basis
    return replace(basis, azim_grad=basis.azim_grad + float(i % 90))


def _zeile(nr: str, name: str, zeiten_s: Sequence[float], notiz: str = "") -> Messwert:
    median, maximum = statistik(zeiten_s)
    return Messwert(nr, name, median, maximum, len(zeiten_s), notiz)


def _zahl(wert: float, stellen: int = 1) -> str:
    return f"{wert:.{stellen}f}".replace(".", ",")


# --- M5 und M6 (ohne Qt) -----------------------------------------------------------------------


def waehle_frequenz(daten: Messdaten) -> float:
    """Mitte der Frequenzachse (wie ``zeiten_messen.py``), wenn ``--frequenz`` fehlt."""
    return float(daten.frequenz_hz[daten.frequenz_hz.size // 2])


def messe_daten(
    daten: Messdaten,
    f_hz: float,
    wiederholungen: int,
    *,
    uhr: Zeit = time.perf_counter,
    rss: Callable[[], float] = rss_mib,
) -> tuple[list[Messwert], AnimationsDaten]:
    """M5: Zeit von :func:`animation_daten` mit drei Kanalpaaren, kalt und warm, und Speicher.

    Kalt: neuer :class:`PaarCache` je Wiederholung (Paare werden berechnet); warm: derselbe Cache
    (Paare im Cache, nur die Zusammenstellung). Der Speicherzuwachs ist der RSS-Unterschied
    zwischen leerem und gefülltem Cache der letzten kalten Wiederholung.

    Returns
    -------
    tuple
        Die Tabellenzeilen und die Animationsdaten der letzten Wiederholung (für M1 bis M4, M6).
    """
    if wiederholungen < 1:
        raise ValueError("wiederholungen >= 1 erwartet")
    annahmen2 = AnnahmenStufe2()
    ergebnis: list[AnimationsDaten] = []
    speicher: list[float] = []

    def kalt(_i: int) -> None:
        vorher = rss()
        cache = PaarCache(daten, groesse=3)
        ergebnis.append(animation_daten(daten, cache, f_hz, annahmen2=annahmen2))
        speicher.append(rss() - vorher)

    kalt_s = _wiederhole(wiederholungen, kalt, uhr)
    cache = PaarCache(daten, groesse=3)
    animation_daten(daten, cache, f_hz, annahmen2=annahmen2)  # füllt den Cache
    warm_s = _wiederhole(
        wiederholungen, lambda _i: animation_daten(daten, cache, f_hz, annahmen2=annahmen2), uhr
    )
    zuwachs = max(speicher)
    zeilen = [
        _zeile("M5", "animation_daten, drei Kanalpaare, kalt", kalt_s),
        _zeile("M5", "animation_daten, drei Kanalpaare, warm", warm_s),
        Messwert(
            "M5",
            "Arbeitsspeicher-Zuwachs der drei Kanalpaare (RSS)",
            None,
            None,
            len(speicher),
            f"größter Zuwachs {_zahl(zuwachs)} MiB",
        ),
    ]
    return zeilen, ergebnis[-1]


def messe_speichern(
    daten: AnimationsDaten,
    stil: Plotstil,
    wiederholungen: int,
    *,
    ordner: Path | None = None,
    uhr: Zeit = time.perf_counter,
) -> list[Messwert]:
    """M6: Zeit, das Standbild als PNG und als PDF zu schreiben (UI-31).

    Gleicher Pfad wie ``Bild speichern …`` im Modus Animation (:func:`speichere_arbeitsbild` mit
    :func:`zeichne_animation`, Stempel mit Winkel); die Dateien entstehen in einem Temp-Ordner
    (oder ``ordner``) und werden nicht aufbewahrt, wenn kein Ordner angegeben ist.
    """
    opt = AnimationsOptionen(theta_rad=math.pi / 2.0)
    stempel = baue_stempel(
        dateiname="messung.svd",
        ansicht="Ansicht 4 Schwingform",
        git_hash=None,
        zusatz=("Animation · θ = 90,0°",),
    )
    zeilen: list[Messwert] = []
    with tempfile.TemporaryDirectory() as temp:
        ziel = ordner if ordner is not None else Path(temp)
        for endung, name in ((".png", "PNG"), (".pdf", "PDF")):
            pfad = ziel / f"animation_messen{endung}"

            def schreibe(_i: int, pfad: Path = pfad) -> None:
                speichere_arbeitsbild(
                    lambda fig: zeichne_animation(fig, daten, opt, stil), pfad, stempel, stil
                )

            zeiten = _wiederhole(wiederholungen, schreibe, uhr)
            zeilen.append(
                _zeile(
                    "M6",
                    f"Standbild speichern ({name})",
                    zeiten,
                    f"{_zahl(pfad.stat().st_size / 1024.0)} KiB",
                )
            )
    return zeilen


# --- M1 bis M4 (mit Qt) ------------------------------------------------------------------------


def messe_flaeche(  # pragma: no cover - braucht Qt und ein Fenster (Test: pytest -m gui)
    daten: AnimationsDaten,
    stil: Plotstil,
    wiederholungen: int,
    dauer_s: float,
    *,
    bildraten: Sequence[int] = BILDRATEN,
    uhr: Zeit = time.perf_counter,
) -> list[Messwert]:
    """M1 bis M4 an der :class:`~ldv_automation.gui.animationsflaeche.AnimationsFlaeche`.

    Die Fläche steht sichtbar (1000 mal 600 px) auf dem Bildschirm bzw. in der
    Remotedesktop-Sitzung; gezeichnet wird mit dem Canvas der Oberfläche, nicht mit einem
    Agg-Ersatz.

    Parameters
    ----------
    daten : AnimationsDaten
        Daten der Animation (3D).
    stil : Plotstil
        Stil der Oberfläche.
    wiederholungen : int
        Wiederholungen je Messpunkt (M1, M3, M4); vor jeder Zeile läuft ein Aufwärm-Schritt
        außerhalb der Zeitmessung. M5 und M6 (:func:`messe_alles`) laufen mit
        ``wiederholungen // 10`` Wiederholungen, mindestens 3.
    dauer_s : float
        Dauer der Wiedergabe je Soll-Bildrate in s (M2).
    bildraten : sequence of int
        Soll-Bildraten für M2.
    uhr : callable
        Zeitquelle in s.
    """
    from PySide6.QtCore import QEventLoop, QPoint, Qt, QTimer
    from PySide6.QtTest import QTest
    from PySide6.QtWidgets import QApplication

    from ldv_automation.gui.animationsflaeche import AnimationsFlaeche

    app = QApplication.instance() or QApplication(sys.argv[:1])
    flaeche = AnimationsFlaeche(stil, bildrate=float(bildraten[0]))
    flaeche.resize(1000, 600)
    flaeche.show()
    app.processEvents()
    basis = AnimationsOptionen()
    zeichnung = flaeche.zeichne(daten, basis)
    canvas = flaeche.canvas
    winkel = [2.0 * math.pi * i / max(wiederholungen, 1) for i in range(wiederholungen)]

    def bild(opt: AnimationsOptionen) -> None:
        aktualisiere_animation(zeichnung, daten, opt, stil)
        canvas.draw()  # type: ignore[no-untyped-call]

    zeilen: list[Messwert] = []
    # M1: Zeit je Bild
    for name, vereinfacht, drehen in (
        ("Bild voll (Achsen, Panes, Ticks)", False, False),
        ("Bild mit vereinfachten Achsen", True, False),
        ("Drehschritt (view_init und Zeichnen), vereinfacht", True, True),
        ("Drehschritt (view_init und Zeichnen), voll", False, True),
    ):

        def schritt(i: int, v: bool = vereinfacht, d: bool = drehen) -> None:
            blick = blick_fuer_schritt(basis.blick, i, drehen=d)
            bild(replace(basis, theta_rad=winkel[i], vereinfacht=v, blick=blick))

        zeiten_m1 = _wiederhole(wiederholungen, schritt, uhr, aufwaermen=True)
        zeilen.append(_zeile("M1", name, zeiten_m1))
    zeichnung = flaeche.zeichne(daten, basis)  # zurück in den Ausgangszustand (voll)

    # M2: effektive Bildrate
    for rate in bildraten:
        flaeche.setze_bildrate(float(rate))
        gezaehlt = [0]
        flaeche.phase_geaendert.connect(lambda _t, z=gezaehlt: z.__setitem__(0, z[0] + 1))
        flaeche.abspielen()
        schleife = QEventLoop()
        QTimer.singleShot(round(dauer_s * _MS), schleife.quit)
        schleife.exec()
        median_s = flaeche.bildzeit_median_s
        flaeche.pausiere()
        flaeche.phase_geaendert.disconnect()
        effektiv = gezaehlt[0] / dauer_s
        ausgelassen = max(0, round(rate * dauer_s) - gezaehlt[0])
        zeilen.append(
            Messwert(
                "M2",
                f"Wiedergabe bei Soll {rate} Bildern/s",
                None if median_s is None else median_s * _MS,
                None,
                gezaehlt[0],
                f"effektiv {_zahl(effektiv)} Bilder/s, {ausgelassen} von {round(rate * dauer_s)} "
                f"Bildern ausgelassen; Median = Zeichenzeit je Bild; "
                f"„langsam“ gemeldet: {'ja' if flaeche.langsam else 'nein'}",
            )
        )

    # M3: Mausziehen bis zum sichtbaren Neuzeichnen
    mitte = QPoint(canvas.width() // 2, canvas.height() // 2)
    QTest.mousePress(canvas, Qt.MouseButton.LeftButton, Qt.KeyboardModifier.NoModifier, mitte)

    def ziehe(i: int) -> None:
        QTest.mouseMove(canvas, mitte + QPoint(2 * (i % 100) + 1, (i % 40) + 1))
        app.processEvents()
        canvas.repaint()

    zeiten = _wiederhole(wiederholungen, ziehe, uhr, aufwaermen=True)
    QTest.mouseRelease(canvas, Qt.MouseButton.LeftButton, Qt.KeyboardModifier.NoModifier, mitte)
    zeilen.append(_zeile("M3", "Mausziehen bis sichtbares Neuzeichnen", zeiten))
    flaeche.ansicht_zuruecksetzen()

    # M4: Phasenregler ziehen (Teilaktualisierung) und Loslassen (Voll-Neuzeichnen)
    def regler(i: int) -> None:
        flaeche.setze_theta_grad(math.degrees(winkel[i]), ziehend=True)
        app.processEvents()

    zeilen.append(
        _zeile(
            "M4",
            "Phasenregler ziehen, je Schritt",
            _wiederhole(wiederholungen, regler, uhr, aufwaermen=True),
        )
    )
    zeilen.append(
        _zeile(
            "M4",
            "Phasenregler loslassen (Voll-Neuzeichnen)",
            _wiederhole(
                wiederholungen, lambda _i: flaeche.phase_losgelassen(), uhr, aufwaermen=True
            ),
        )
    )
    flaeche.beende()
    flaeche.close()
    return zeilen


# --- Ausgabe -----------------------------------------------------------------------------------


def umgebung(
    datei: str, rechner: str, sitzung: str, f_hz: float, *, mit_qt: bool
) -> dict[str, str]:
    """Kopf der Tabelle: Datei, Rechner, Sitzungsart, Frequenz und Versionen."""
    kopf = {
        "datei": Path(datei).name,
        "rechner": rechner,
        "sitzungsart": sitzung,
        "system": platform.platform(),
        "frequenz_hz": _zahl(f_hz, 3),
        "python": platform.python_version(),
        "numpy": np.__version__,
        "matplotlib": matplotlib.__version__,
    }
    if mit_qt:  # pragma: no cover - nur mit Qt
        import PySide6
        from PySide6.QtGui import QGuiApplication

        kopf["pyside6"] = PySide6.__version__
        kopf["qt_plattform"] = QGuiApplication.platformName()
    return kopf


def _wert(m: Messwert) -> tuple[str, str]:
    median = "–" if m.median_ms is None else _zahl(m.median_ms)
    maximum = "–" if m.max_ms is None else _zahl(m.max_ms)
    return median, maximum


def tabelle_text(kopf: dict[str, str], messwerte: Sequence[Messwert]) -> str:
    """Ergebnistabelle als Text (Konsole)."""
    zeilen = [f"{k}: {v}" for k, v in kopf.items()]
    zeilen.append("")
    zeilen.append(f"{'Nr':<3} {'Median ms':>10} {'Max ms':>10} {'n':>5}  Messpunkt")
    for m in messwerte:
        median, maximum = _wert(m)
        zusatz = f" ({m.notiz})" if m.notiz else ""
        zeilen.append(f"{m.nr:<3} {median:>10} {maximum:>10} {m.n:>5}  {m.name}{zusatz}")
    return "\n".join(zeilen)


def tabelle_markdown(kopf: dict[str, str], messwerte: Sequence[Messwert]) -> str:
    """Ergebnistabelle als Markdown (für das Prüfprotokoll)."""
    zeilen = [f"- **{k}:** {v}" for k, v in kopf.items()]
    zeilen += [
        "",
        "| Nr | Messpunkt | Median [ms] | Max [ms] | n | Notiz |",
        "|---|---|---|---|---|---|",
    ]
    for m in messwerte:
        median, maximum = _wert(m)
        zeilen.append(f"| {m.nr} | {m.name} | {median} | {maximum} | {m.n} | {m.notiz} |")
    return "\n".join(zeilen) + "\n"


def messe_alles(
    geladen: Geladen,
    stil: Plotstil,
    *,
    f_hz: float | None = None,
    wiederholungen: int = 100,
    dauer_s: float = 10.0,
    mit_qt: bool = True,
) -> tuple[float, list[Messwert]]:
    """Alle Messpunkte nacheinander (M5, M6, dann M1 bis M4); gibt Frequenz und Zeilen zurück."""
    daten = geladen.messdaten
    f = waehle_frequenz(daten) if f_hz is None else f_hz
    zeilen, anim = messe_daten(daten, f, max(3, wiederholungen // 10))
    zeilen += messe_speichern(anim, stil, max(3, wiederholungen // 10))
    if mit_qt:  # pragma: no cover - nur mit Qt
        zeilen = messe_flaeche(anim, stil, wiederholungen, dauer_s) + zeilen
    return f, sorted(zeilen, key=lambda m: m.nr)


def main(argv: Sequence[str] | None = None) -> int:  # pragma: no cover - Einstieg
    """Einstieg: misst, druckt die Tabelle und schreibt optional Markdown und JSON."""
    parser = argparse.ArgumentParser(description=(__doc__ or "").split("\n\n")[0])
    parser.add_argument("datei", help=".svd-Datei (3D-Messung mit Referenz)")
    parser.add_argument("--sitzung", choices=("lokal", "remotedesktop"), default="lokal")
    parser.add_argument("--rechner", default=platform.machine(), help="Bezeichnung des Rechners")
    parser.add_argument("--wiederholungen", type=int, default=100)
    parser.add_argument("--dauer", type=float, default=10.0, help="Sekunden je Bildrate (M2)")
    parser.add_argument("--frequenz", type=float, help="Frequenz in Hz (Voreinstellung: Mitte)")
    parser.add_argument("--tabelle", help="Ergebnis als Markdown schreiben")
    parser.add_argument("--json", help="Ergebnis als JSON schreiben")
    parser.add_argument("--ohne-qt", action="store_true", help="nur M5 und M6")
    args = parser.parse_args(argv)
    if args.wiederholungen < 1 or args.dauer <= 0.0:
        parser.error("--wiederholungen >= 1 und --dauer > 0 erwartet")
    if not Path(args.datei).is_file():
        parser.error(f"Datei nicht gefunden: {args.datei}")
    from ldv_automation.gui.plotstil import baue_plotstil

    geladen = lade_svd(args.datei)
    f, werte = messe_alles(
        geladen,
        baue_plotstil(),
        f_hz=args.frequenz,
        wiederholungen=args.wiederholungen,
        dauer_s=args.dauer,
        mit_qt=not args.ohne_qt,
    )
    kopf = umgebung(args.datei, args.rechner, args.sitzung, f, mit_qt=not args.ohne_qt)
    print(tabelle_text(kopf, werte))
    if args.tabelle:
        Path(args.tabelle).write_text(tabelle_markdown(kopf, werte), encoding="utf-8")
    if args.json:
        Path(args.json).write_text(
            json.dumps(
                {"umgebung": kopf, "messungen": [m.__dict__ for m in werte]},
                indent=2,
                ensure_ascii=False,
            ),
            encoding="utf-8",
        )
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
