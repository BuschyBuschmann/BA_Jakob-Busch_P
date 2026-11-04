# ADR-025: Darstellung der Phase in der Schwingform

**Datum:** 2026-11-05 · **Status:** angenommen
**Bezug:** Fachanalyse FA-AUSW (F-4), Fachabnahme FAB-AUSW-T2 (M-1); Entscheidungen des Nutzers vom 2026-11-03 (F-4) und 2026-11-05 (E-1, E-3)

## Kontext
Eine zyklische Größe (−180° … +180°) lässt sich in Graustufen nicht eindeutig über Helligkeit darstellen (jeder Grauwert tritt mindestens zweimal auf). Die erste Umsetzung (Pfeillänge ∝ |v|, schwarz) war im Bild kaum lesbar: 49 % der Pfeile kürzer als der Markerradius, auf `twilight` bei 0° unsichtbar.

## Betrachtete Alternativen
| Alternative | Vorteile | Nachteile |
|---|---|---|
| Pfeil konstanter Länge (ca. 0,8 Punktabstand) mit hellem Rand, Betrag über Markergröße, Füllung `twilight`, Kreislegende | Winkel immer lesbar, graustufentauglich | Betrag nur über Markergröße |
| Mindestlänge + Rest ∝ |v| | Betrag auch im Pfeil | kurze Pfeile weiter schwer lesbar |
| Pfeil ∝ |v|, nur Kontrast | wenig Änderung | Lesbarkeitsproblem bleibt |
| Nur Farbe/Helligkeit | einfach | in Graustufen mehrdeutig |

## Entscheidung
Pfeil konstanter Länge mit hellem Rand, Betrag über Markergröße, Punktfüllung in `twilight`, Kreislegende mit Vorzeichentext; Phase nur für eine Einzelkomponente, absolut gegen Ref1 (⚠ unbestätigt, M8) oder relativ zu einem Bezugspunkt (M8-unabhängig). Punkte mit γ² < γ²_min und von PSV ungültig markierte Punkte bleiben im Bild, gekennzeichnet, ohne Pfeil.

## Begründung
Herleitung in FA-AUSW F-4c, Befund M-1 der Fachabnahme, Vorschlag des strukturdynamik-experte, vom Nutzer gewählt.

## Konsequenzen
Umsetzung im Korrekturpaket zu T2; Test auf Mindestlänge im Bildschirmmaß; Thesis-Abbildung nur mit relativer Phase, solange M8 offen ist.
