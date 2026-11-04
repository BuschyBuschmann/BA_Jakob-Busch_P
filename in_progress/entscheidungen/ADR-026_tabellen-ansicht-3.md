# ADR-026: Platzierung der Spitzen- und Bändertabelle in Ansicht 3

**Datum:** 2026-11-05 · **Status:** angenommen
**Bezug:** Design-Brief K-AUSW (Abschnitt 3.3, UI-7, UI-8), Umsetzung T3b, Design-Abnahme DA-AUSW-T3b; Entscheidung des Nutzers vom 2026-11-05

## Kontext
Der Brief sah die Tabellen in der 260 px breiten Auswahlspalte AD vor. Die Spitzentabelle hat sieben Spalten (Nr, f, ζ, band_u_hz, band_o_hz, Methode, Kennzeichen; R-055), die Beispieldatei 111 Spitzen. Plot und Tabelle müssen gleichzeitig sichtbar sein, damit der Klick auf eine Zeile die Spitze im Plot markiert (UI-8).

## Betrachtete Alternativen
| Alternative | Vorteile | Nachteile |
|---|---|---|
| Splitter unter dem Plot, Standardhöhe ≥ 6 Zeilen, Position gemerkt | alle Spalten, Plot und Tabelle gleichzeitig, kleiner Umbau | Plot niedriger (ca. 260–300 px bei 1366×768) |
| Tabelle rechts neben dem Plot (ca. 480 px) | Plot volle Höhe | Plot schmaler, Spitzenkurve dichter |
| Plot und Tabelle umschaltbar | beide groß | UI-8 nicht gleichzeitig sichtbar |
| AD auf ca. 480 px verbreitern, 4 Spalten + Detailzeile | Brief-Ort | widerspricht UI-7 (jede Zeile mit allen Dämpfungsfeldern) |
| Tabelle in der 260-px-Spalte (Brief) | wie geplant | sieben Spalten passen nicht |

## Entscheidung
Splitter unter dem Plot mit Reitern „Spitzen | Bänder“, Standardhöhe mindestens 6 Zeilen, Splitterposition je Sitzung gemerkt.

## Begründung
Empfehlung der Design-Abnahme DA-AUSW-T3b, vom Nutzer gewählt.

## Konsequenzen
Brief K-AUSW Abschnitt 3.3 gilt in diesem Punkt als geändert; Test auf sichtbare Zeilenzahl bei 1366×768.
