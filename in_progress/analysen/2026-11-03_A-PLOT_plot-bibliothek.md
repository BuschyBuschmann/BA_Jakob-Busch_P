# A-PLOT: Plot-Bibliothek für den Bereich „Auswerten“ (Entscheidungsvorlage, Kurzfassung)

Analyse software-engineer (sonnet), 2026-11-03, read-only; Experimente im Scratchpad der Sitzung (nicht im Repo).
Kennzeichnung: [G] gemessen (Linux, Python 3.11.15, offscreen, PySide6 6.11.3, numpy 2.4.6, matplotlib 3.11.2, pyqtgraph 0.14.0; Daten `Input/20261012_ref_Mitte.svd`, 135 Punkte, 1600 Linien), [R] recherchiert (PyPI, 03.11.2026), [A] Annahme. Windows nicht gemessen.

## Messwerte [G] (Median, ms)
| Szenario | matplotlib | pyqtgraph |
|---|---|---|
| 1 Kurve, Punktwechsel | 42 | 5,7 |
| H1/H2 + Kohärenz, Punktwechsel | 52–69 | 7,6–13 |
| 100 Kurven, Daten tauschen | 404–478 | 77–90 |
| 100 Kurven, Zoom/Pan-Schritt | 202–236 | 39–45 |
| Cursor | 0,3 (Blitting) / 27 (ohne) | 1,1 |
| Schwingform, Frequenzwechsel | 32 (`tripcolor`) | 5,5 (eigenes Item) |

Refcount von None (1000 Schritte) mit PySide6 6.11.3: matplotlib 0, pyqtgraph +10 985 (Zuwachs, unerklärt); Repo-Regressionstest besteht. pyqtgraph-SVG-Export wirft `ValueError` [G]. mypy --strict: matplotlib 1 `no-untyped-call`; pyqtgraph ohne `py.typed`.

## Abhängigkeiten [R]
matplotlib ca. 19 MB inkl. Abhängigkeiten (bereits in `uv.lock` über Gruppe `werkzeuge`); pyqtgraph ca. 2 MB, neu. Pflege: matplotlib sehr aktiv; pyqtgraph 0.13.7 (04/2024) → 0.14.0 (11/2025).

## Empfehlung
matplotlib mit `FigureCanvasQTAgg`, ohne `pyplot`: eine Zeichenfunktion für Oberfläche und Thesis, Schwingform auf unregelmäßigem Netz fertig, Tempo für Stufe 1 ausreichend. Risiken: Ruckeln bei Zoom mit mehreren Kurven (Blitting), langsam bei vielen überlagerten Kurven (Fallback pyqtgraph hinter schmaler Schnittstelle), Wheelhouse +19 MB, Windows ungeprüft.
