# ADR-019: Kennzeichen `moden_vertauscht` im Mehr-Moden-Fit

**Datum:** 2026-10-30 · **Status:** angenommen
**Bezug:** R-053; FG-03 3.4, 4.5, 7, RF-F9 (Korrektur K3); Pakete K-W5-2, K-W5-2b; Review R-W5-2 (M2), Fachabnahme RFA-W5-2

## Kontext
Im Mehr-Moden-Fit legt die Modellform keine Reihenfolge der Moden fest. Welche gefittete Mode zu
welcher Stufe-1-Spitze gehört, folgt nur aus den Startwerten. An der Beispieldatei liefen Moden
über ihre Nachbarin oder sprangen auf die Spitze einer weggelaufenen Partnermode und gingen ohne
Kennzeichen in die Zusammenfassung der falschen Spitze ein.

## Betrachtete Alternativen
| Alternative | Vorteile | Nachteile |
|---|---|---|
| Kennzeichen nach Rangregel und Näheregel, Ausschluss aus Zusammenfassung und Drift | erkennt beide beobachteten Fehlerarten; Zusammenfassungen werden nicht verfälscht | weniger Punkte je Spitze (z. B. 1329,35 Hz: N 12 → 10) |
| nur Rangregel | einfach | übersieht 20 Fehlzuordnungen ohne Rangwechsel an der Beispieldatei |
| Moden nach dem Fit umsortieren | kein Datenverlust | löst nur 3 von 22 Fällen; sonst zwei Pole an einer Spitze |
| nichts tun (Median ist robust) | kein Aufwand | Werte werden still der falschen Spitze zugeordnet |

## Entscheidung
`moden_vertauscht` je Mode bei n ≥ 2, nur unter Moden ohne `ausserhalb_band`: (a) Rangfolge der f_r
weicht von der der Startwerte ab, oder (b) die Mode liegt einem anderen Startwert der Gruppe echt
näher als dem eigenen (j über alle Startwerte, auch weggelaufene Partner). Kein Kennzeichen bei
Gleichstand. Ausschluss aus Zusammenfassung und Drift.

## Begründung
Vom Nutzer freigegeben (M2 und K3, 2026-10-30); Referenzfall RF-F9; Fachabnahme RFA-W5-2b.

## Konsequenzen
- An der Beispieldatei ändern sich die Zusammenfassungen bei 1006,41 und 1329,35 Hz; Drift und
  übrige Werte aus FG-03 Abschnitt 7 bleiben gleich.
- Bekannte Grenze (vom Nutzer am 2026-10-30 so festgelegt, Paket K-W5-2c): Laufen zwei Moden auf
  exakt dieselbe Fitfrequenz, regelt FG-03 den Ranggleichstand nicht. Bei aufsteigend sortierten
  Startwerten (so liefert sie `bilde_gruppen` immer) entsteht über Regel (a) kein Kennzeichen; bei
  direkt übergebenen unsortierten Startwerten hängt es von der Modenreihenfolge ab. Das Verhalten ist
  im Test `test_gleiche_fr_zweier_moden_verhalten_festgehalten` festgehalten.
