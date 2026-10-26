# ADR-001: GUI-Technologie

**Datum:** 2026-10-26 · **Status:** angenommen
**Bezug:** Prototyp Mess-Warteschlange (Lastenheft R-001, R-010–R-031); Entscheidung des Nutzers vom 2026-10-26

## Kontext
Prototyp der Mess-Warteschlange, Test am PSV-Messrechner am 2026-11-02. Details und Belege: Entscheidungsvorlage `in_progress/analysen/2026-10-26_P1_gui-technologie.md`.

## Betrachtete Alternativen
| Alternative | Vorteile | Nachteile |
|---|---|---|
| PySide6/Qt | beste Eignung für Warteschlange (Model/View), Thread-Brücke per Signal geprobt, matplotlib einbettbar, offline installierbar | Lernkurve, ~84 MB, Systembibliotheken für Tests im Container |
| NiceGUI | schnell gebaut, stark für Web-Auswertung, Tests ohne Display | Browser am Messrechner nötig, viele Web-Abhängigkeiten |
| Tkinter | Standardbibliothek, kein Installationsrisiko | veraltet, kein Drag-and-drop, schwach für Auswertung |

## Entscheidung
PySide6 (`pyside6-essentials==6.12.0`, Qt Widgets) als dünne Schicht über einem GUI-freien Kern; Tests mit `pytest-qt`, Marker `gui`, offscreen.

## Begründung
Empfehlung des Architekturplans bzw. der Entscheidungsvorlage, vom Nutzer übernommen. Belege siehe Quelle.

## Konsequenzen
Umsetzung in den Paketen U1–U5 des Plans P2; unbestätigte Annahmen erhalten Schalter bzw. Rückfallwege und werden am Messrechner geprüft.
