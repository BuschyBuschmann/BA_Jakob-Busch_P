# ADR-016: Abbildung der Betriebsart in der Kompositionswurzel

**Datum:** 2026-10-27 · **Status:** angenommen
**Bezug:** Paket U5 (Integration), Review R-U5/RR-U5; Laborbuch `in_progress/laborbuch/2026-10-27_u5-integration.md`; Rückfragen aus U2/U3

## Kontext
Sitzung (`sitzung.Betriebsart`), COM-Adapter (`ComBetriebsart`) und Simulator (Text) führten die Betriebsart getrennt. Ein gemeinsamer Typ hätte eine Änderung der fest vereinbarten Geräteschnittstelle (`geraet/schnittstelle.py`) erfordert.

## Betrachtete Alternativen
| Alternative | Vorteile | Nachteile |
|---|---|---|
| Gemeinsamer Aufzählungstyp in `geraet/schnittstelle.py` | ein Typ für alle | Änderung des festen Vertrags, betrifft U2 und U3 |
| Gemeinsamer Typ in `domaene` | fachlich zentral | Domäne kennt sonst keine Geräteaspekte |
| Abbildung an einer Stelle in der Kompositionswurzel (`__main__.py`) | Vertrag unverändert, eine geprüfte Stelle | Abbildung muss bei neuen Betriebsarten nachgezogen werden |

## Entscheidung
Abbildung `sitzung.Betriebsart` → `ComBetriebsart` bzw. Simulator-Text ausschließlich in `__main__.py` (Gerätefabrik); ein Test deckt jede Betriebsart ab. Zusätzlich prüft die Steuerung beim Start im Geräte-Thread, dass die Betriebsart des Auftrags zum aktiven Gerät passt und MESSEN bestätigt ist (Korrektur MAJOR 2 aus R-U5).

## Begründung
Entscheidung des Orchestrators im Rahmen von U5 (Vertrag unverändert lassen); vom Nutzer als ADR freigegeben.

## Konsequenzen
`__main__.py` ist Kompositionswurzel und darf Gerät, Ablauf, Domäne und Protokoll importieren (Importrichtungstest angepasst).
