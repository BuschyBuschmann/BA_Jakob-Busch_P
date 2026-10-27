# ADR-014: Konfigurationsdatei für den Messrechner

**Datum:** 2026-10-27 · **Status:** angenommen
**Bezug:** Paket U5 (Integration), Review R-U5/RR-U5; Laborbuch `in_progress/laborbuch/2026-10-27_u5-integration.md`; Entscheidung des Nutzers vom 2026-10-27

## Kontext
Die Erkundung am Messrechner liefert Werte, die der Prototyp übernehmen muss (Validator-Rückfall S4, Lademaske, Aufrufgrenze, Wächterwarnung, Stopp-Frist, Standard-Zeitlimit). Sie waren weder in der Oberfläche noch beim Start einstellbar; ein Eingriff in den installierten Code hätte den Git-Stand verfälscht.

## Betrachtete Alternativen
| Alternative | Vorteile | Nachteile |
|---|---|---|
| JSON-Konfigurationsdatei (`--konfig`) | Werte und SHA-256 im Protokoll nachvollziehbar, Git-Stand bleibt sauber | eine Datei mehr am Messrechner |
| Startoptionen auf der Kommandozeile | ohne Datei | lange Aufrufe, schlechter dokumentierbar |
| Nur ermitteln, Einbau nach Montag | kein Aufwand vor Montag | GUI-Test nur mit Standardwerten, Trockenlauf scheitert ggf. |

## Entscheidung
JSON-Datei, angegeben mit `--konfig` für `gui` und `selbsttest` (`src/ldv_automation/konfig.py`). Strenge Prüfung beim Start (unbekannte Schlüssel, Typen, Bereiche; Lademaske nur über die Richtlinie); ungültig → Abbruch. Pfad, SHA-256 und Werte stehen in jedem Messprotokoll und im Dialog „Gerät“. Beispiel: `software/konfig/beispiel_messrechner.json`.

## Begründung
Entscheidung des Nutzers; die Bereichsgrenzen sind Tippfehlerschutz, keine Gerätedaten.

## Konsequenzen
Am Montag werden die Werte aus der Erkundung in eine Kopie der Beispieldatei eingetragen. Die Konfiguration ist Teil der Versuchsdokumentation.
