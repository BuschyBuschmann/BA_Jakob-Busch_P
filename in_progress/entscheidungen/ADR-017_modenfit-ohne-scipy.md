# ADR-017: Modenfit mit NumPy statt scipy

**Datum:** 2026-10-30 · **Status:** angenommen
**Bezug:** R-053; FG-03 Abschnitt 3 (E1); Paket W5-2; Laborbuch 2026-10-30_w5-auswertung-stufe2

## Kontext
B-1 (parametrische Dämpfungsschätzung) verlangt einen komplexen Modenfit auf H1 mit
Variablenprojektion und Levenberg-Marquardt (FG-03 3.2). Die Fachgrundlage enthält dafür ein
Prüfskript (`fit.py`), das nur NumPy nutzt. scipy ist bisher keine Laufzeitabhängigkeit.

## Betrachtete Alternativen
| Alternative | Vorteile | Nachteile |
|---|---|---|
| Eigene Umsetzung mit NumPy nach dem Prüfskript | deckungsgleich mit FG-03 und deren Referenzfällen; Abbruchkriterium und Kennzeichen vollständig kontrollierbar; keine neue Abhängigkeit | eigener Optimierungscode muss getestet und gepflegt werden |
| `scipy.optimize.least_squares` | erprobter Löser | neue Laufzeitabhängigkeit auf dem Messrechner; Abbruchkriterium und Schrittlogik weichen vom Prüfskript ab, Referenzwerte müssten neu bestätigt werden |

## Entscheidung
Der Modenfit ist mit NumPy umgesetzt, eng nach dem Prüfskript aus FG-03.

## Begründung
Alle Referenzfälle RF-F1 bis RF-F9 werden mit den Sollwerten aus FG-03 erreicht; die Fachabnahme
hat Formeln, Abbruchkriterium (K2-2) und Kennzeichen bestätigt. Eine zusätzliche Abhängigkeit
brächte keinen belegten Vorteil.

## Konsequenzen
- Keine neue Laufzeitabhängigkeit für die Installation am Messrechner.
- Der Optimierungscode (`auswertung/modenfit.py`) ist Teil des Pakets und durch Tests abgesichert.
- In der Thesis wird der Fit als eigene Umsetzung des Verfahrens aus FG-03 beschrieben.
