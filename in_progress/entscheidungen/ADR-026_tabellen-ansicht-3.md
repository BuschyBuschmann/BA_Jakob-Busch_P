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

## Nachtrag 2026-11-05: Beschriftung der gewählten Spitze in der Auswahlspalte
**Anlass:** Design-Re-Abnahme DA-AUSW-T3b-2: Mit Standardhöhe ≥ 6 Tabellenzeilen bleibt bei 1366×768 nur ca. 140 px Plot; Beschriftungsstreifen (bis 50 %) und Dreizeilen-Kasten quetschen die Kurve auf ca. 40 px.
**Alternativen:** Beschriftung in die Auswahlspalte AD (im Plot nur Ring, kein Streifen) · Tabelle einklappbar mit 4 Zeilen · zusätzlich Legende in den Plotkopf · nur Streifen begrenzen.
**Entscheidung des Nutzers (2026-11-05):** In der Oberfläche stehen die Angaben der gewählten Spitze (f, ζ, Methode, Band, Kennzeichen) als Textblock in der Auswahlspalte; im Plot bleibt der Ring, der Beschriftungsstreifen entfällt; Tabelle 5–6 Zeilen, Plotachse ca. 220 px. Die Thesis-Abbildung behält Kasten und Streifen. Abweichung von UI-8 („Marker mit Beschriftung im Plot“) bewusst. Kanalpaarwahl bleibt für alle Ansichten gemeinsam (Nutzerentscheidung).

## Nachtrag 2 2026-11-05: Legende in der Auswahlspalte, 4 Tabellenzeilen
**Anlass:** Nach Nachtrag 1 blieb bei 1366×768 mit 5 Tabellenzeilen nur eine Plotachse von 98 px (Legende, Ticks und Werkzeugleiste kosten ca. 170 px); 220 px Achse und 5 Zeilen passen nicht gleichzeitig.
**Alternativen:** Legende aus dem Plot und 4 Zeilen · 3 Zeilen Standard · unverändert (Splitter manuell).
**Entscheidung des Nutzers (2026-11-05):** In der Oberfläche steht die Kurvenlegende (mit Mittelformel und Punktzahl) in der Auswahlspalte, Standard 4 Tabellenzeilen. Gemessen: Achse 203 px bei 1366×768, 115 px bei 1100×680. Thesis und Arbeitsbild behalten Legende, Streifen und Kasten (Voreinstellung der Zeichenfunktion). Beim späteren „Bild speichern“ (T4) sind die Voreinstellungen zu verwenden, nicht die GUI-Optionen.
