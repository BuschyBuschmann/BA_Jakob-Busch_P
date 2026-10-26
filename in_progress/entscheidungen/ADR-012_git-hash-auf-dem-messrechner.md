# ADR-012: Git-Hash auf dem Messrechner

**Datum:** 2026-10-26 · **Status:** angenommen
**Bezug:** Prototyp Mess-Warteschlange (Lastenheft R-001, R-010–R-031); Entscheidung des Nutzers vom 2026-10-26

## Kontext
Prototyp der Mess-Warteschlange, Test am PSV-Messrechner am 2026-11-02. Details und Belege: `in_progress/planung/plaene/2026-10-26_P2_architektur-prototyp.md`, Abschnitt 7.

## Betrachtete Alternativen
| Alternative | Vorteile | Nachteile |
|---|---|---|
| Build-Info | kein Git am Messrechner nötig | Bau-Schritt nötig |
| Git voraussetzen | direkt | nicht freigegeben |
| nur SHA-256 | einfach | kein Bezug zum Repo-Stand |

## Entscheidung
Build-Info-Datei beim Wheel-Bau (Rückfall: Git, falls vorhanden).

## Begründung
Empfehlung des Architekturplans bzw. der Entscheidungsvorlage, vom Nutzer übernommen. Belege siehe Quelle.

## Konsequenzen
Umsetzung in den Paketen U1–U5 des Plans P2; unbestätigte Annahmen erhalten Schalter bzw. Rückfallwege und werden am Messrechner geprüft.
