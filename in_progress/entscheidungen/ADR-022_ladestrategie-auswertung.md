# ADR-022: Ladestrategie der Auswertungsoberfläche (eigener Prozess)

**Datum:** 2026-11-05 · **Status:** angenommen
**Bezug:** Plan P-AUSW (U-2), Brief K-AUSW (UI-15), Laborbuch 2026-11-03_auswerten-t1-leser-prozess, 2026-11-04_auswerten-t2-darstellung; Entscheidungen des Nutzers vom 2026-11-03 (F-3 zweistufig) und 2026-11-05 (ADR)

## Kontext
Die Oberfläche darf beim Laden nicht einfrieren (UI-15). Gemessen (Linux-Container, Beispieldatei 135 Punkte × 1600 Linien): Lesen 0,1–0,8 s, SHA-256 0,1 s, `werte_aus` mit Plausibilitätsprüfungen 8–13 s (P-07 allein 12,4 s), ganze `Auswertung` 247 MB (Pickle je ca. 2 s), `Messdaten` 48 MB. Brief P3 schließt `QThread` aus.

## Betrachtete Alternativen
| Alternative | Vorteile | Nachteile |
|---|---|---|
| Blockierend im Hauptprozess | einfach | Oberfläche friert 8–13 s ein, UI-15 verletzt |
| `ProcessPoolExecutor` | Standardbibliothek | laufender Auftrag nicht abbrechbar; 983 ms Lücke beim Senden von 48 MB |
| `QThread` | Qt-nah | durch P3 ausgeschlossen, nicht abbrechbar, GIL |
| `multiprocessing.Process` + `Pipe` (spawn), Teile ≤ 4 MiB, zweistufig | abbrechbar (2 ms), längste Abfrage 20–56 ms, Fehlerkanal mit Typ/Text/Spur | eigener Code (`hintergrund.py`), Windows-Verhalten erst am Messrechner belegbar |

## Entscheidung
`multiprocessing.Process` mit `Pipe` im spawn-Kontext (`ldv_automation.hintergrund`), Pickle-Protokoll 5 mit getrennten Puffern in Teilen ≤ 4 MiB, Abfrage über `QTimer`. Zweistufig: Auftrag A liest die Datei (Ansicht 1 nach ca. 1 s), Auftrag B rechnet die Prüfungen und liefert nur kleine Ergebnisse. Abbruch: `terminate`, nach 0,3 s `kill`. Fehlerkanal als gepickeltes Tupel.

## Begründung
Messungen der Planung P-AUSW und von T1 (Prototypen beider Prozessvarianten), Review R-AUSW-T1 mit Spawn-Proben, vom Nutzer freigegeben.

## Konsequenzen
- Jeder Auftrag wird abgefragt oder abgebrochen; Fenster schließen ruft `beende()`.
- Am Messrechner `tools/auswertung/zeiten_messen.py` ausführen (Spawn, Pipe, Abbruch, Font-Cache).
- Optional später: Vektorisierung von P-07 (Prüfung ca. 2 s statt 8–13 s).
