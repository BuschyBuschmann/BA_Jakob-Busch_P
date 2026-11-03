# ADR-021: Plot-Bibliothek der Auswertungsoberfläche

**Datum:** 2026-11-03 · **Status:** angenommen
**Bezug:** R-032, R-050–R-053, R-055; ADR-001 (PySide6 6.11.3); Grunddesign K-AUSW (freigegeben 2026-11-03); Analyse `in_progress/analysen/2026-11-03_A-PLOT_plot-bibliothek.md`; Entscheidung des Nutzers vom 2026-11-03

## Kontext
Der Bereich „Auswerten“ im Hauptfenster zeigt Spektren, H1/H2 mit Kohärenz, Spitzen und Bänder sowie die Schwingform auf dem Messgitter. `pyside6-essentials` enthält kein QtCharts; das Paket braucht eine Plot-Bibliothek als Laufzeitabhängigkeit. Thesis-Abbildungen entstehen per Skript mit matplotlib.

## Betrachtete Alternativen
| Alternative | Vorteile | Nachteile |
|---|---|---|
| matplotlib (`FigureCanvasQTAgg`) | eine Zeichenfunktion für Oberfläche und Thesis (PDF/SVG); Schwingform auf unregelmäßigem Netz mit Farbleiste fertig; bereits im Lockfile; typisiert; aktive Pflege | langsamer (42–52 ms bei 1–3 Kurven, ca. 400 ms bei 100 Kurven); Cursor nur mit Blitting flüssig; ca. 19 MB |
| pyqtgraph | 5–10× schneller; Interaktion eingebaut; ca. 2 MB | Schwingform-Netz Eigenbau; Thesis-Abbildungen doppelt; SVG-Export in dieser Kombination defekt; untypisiert; neue Abhängigkeit |
| Hybrid (pyqtgraph live, matplotlib Thesis) | Tempo und Druckqualität | doppelter Code, abweichende Darstellung |

## Entscheidung
matplotlib mit `Figure` und `FigureCanvasQTAgg`, ohne `pyplot`. Die Plot-Fläche liegt hinter einer schmalen Schnittstelle.

## Begründung
Empfehlung der Analyse A-PLOT (Messungen offscreen unter Linux mit der Beispieldatei), vom Nutzer gewählt. Tempo reicht für die erste Ausbaustufe; gemeinsame Zeichenfunktionen mit den Thesis-Abbildungen.

## Konsequenzen
- matplotlib wird Hauptabhängigkeit in `software/pyproject.toml`; `uv.lock` und Wheelhouse werden angepasst (ca. +19 MB); Paketversion steigt bei Auslieferung.
- In der Oberfläche kein `pyplot`; Cursor/Marker per Blitting.
- Windows-Verhalten (Tempo, HiDPI, Schrift) am Messrechner zu prüfen.
- Werden später viele überlagerte Kurven verlangt, ist pyqtgraph hinter derselben Schnittstelle der Rückfallweg.
