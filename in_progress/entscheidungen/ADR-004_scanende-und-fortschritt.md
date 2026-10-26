# ADR-004: Scanende und Fortschritt

**Datum:** 2026-10-26 · **Status:** angenommen
**Bezug:** Prototyp Mess-Warteschlange (Lastenheft R-001, R-010–R-031); Entscheidung des Nutzers vom 2026-10-26

## Kontext
Prototyp der Mess-Warteschlange, Test am PSV-Messrechner am 2026-11-02. Details und Belege: `in_progress/planung/plaene/2026-10-26_P2_architektur-prototyp.md`, Abschnitt 7.

## Betrachtete Alternativen
| Alternative | Vorteile | Nachteile |
|---|---|---|
| Polling | für externe Programme belegt (COM-Folie 12) | kein Punktfortschritt |
| Events | Punktfortschritt | aus Python ungeprüft, braucht Nachrichtenschleife |

## Entscheidung
Polling von `Acquisition.State` für das Scanende; Fortschritt als Zeitschätzung; Events nur als abschaltbares Experiment.

## Begründung
Empfehlung des Architekturplans bzw. der Entscheidungsvorlage, vom Nutzer übernommen. Belege siehe Quelle.

## Konsequenzen
Umsetzung in den Paketen U1–U5 des Plans P2; unbestätigte Annahmen erhalten Schalter bzw. Rückfallwege und werden am Messrechner geprüft.
