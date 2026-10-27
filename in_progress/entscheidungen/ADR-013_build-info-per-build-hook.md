# ADR-013: Build-Info per Build-Hook

**Datum:** 2026-10-27 · **Status:** angenommen (präzisiert ADR-012)
**Bezug:** Paket U5 (Integration), Review R-U5/RR-U5; Laborbuch `in_progress/laborbuch/2026-10-27_u5-integration.md`; ADR-012

## Kontext
ADR-012 legt fest, dass der Git-Stand über eine Build-Info-Datei im Wheel auf den Messrechner kommt. Die erste Umsetzung (Skript vor dem Bau, Datei per `artifacts` gepackt) ließ zu, dass ein veralteter Hash im Wheel landet: bei fehlgeschlagenem Skript oder neuen Commits ohne erneuten Skriptlauf (Review R-U5, MAJOR 1). Messprotokolle hätten dann eine falsche Softwareversion getragen.

## Betrachtete Alternativen
| Alternative | Vorteile | Nachteile |
|---|---|---|
| Skript vor dem Bau + `artifacts` | einfach | veralteter Hash möglich, hängt an der Disziplin beim Bauen |
| Hatch-Build-Hook erzeugt die Datei beim Bau | Hash gehört immer zum gebauten Stand; Bau bricht ohne Git ab | zusätzliche Dev-Abhängigkeit `hatchling`; normales `uv build` (sdist) bricht ab |
| Abgleich der Datei gegen HEAD beim Bau | behält das Skript | zwei Schritte, Fehlerquelle bleibt |

## Entscheidung
Build-Hook `software/hatch_build.py` schreibt die Build-Info beim Wheel-Bau aus dem aktuellen Git-Stand und packt sie per `force_include`; ohne Git bricht der Bau ab. Eine Datei im Quellbaum wird nie gepackt (`.gitignore`). `tools/build_info/build_info.py` bleibt als Werkzeug und löscht bei Fehlschlag eine vorhandene Datei.

## Begründung
Korrektur von MAJOR 1 aus R-U5, im Re-Review RR-U5 mit gefälschter Datei im Quellbaum nachgeprüft (Wheel enthält den echten Stand).

## Konsequenzen
Wheel für den Messrechner nur mit `uv build --wheel` und erst nach dem letzten Commit bauen (`git_dirty` false). Siehe `in_progress/versuche/2026-11-02_prototyp/installation_messrechner.md`.
