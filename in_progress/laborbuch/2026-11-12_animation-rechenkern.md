# 2026-11-12 – Animation der Schwingform: Rechenkern (R-071, AN1–AN2)

**Art:** Arbeitspaket
**Paket/Bezug:** U-AUSW3-1, FA-AN2, K-AN2; R-071; Plan P-AUSW3; FG-04 und Nachtrag 1; ADR-029
**Commit:** 0771f5a (Stand vor dem Paket-Commit)
**Beteiligt:** software-engineer (sonnet: Umsetzung; haiku: Korrektur), strukturdynamik-experte (sonnet: Fachabnahme); Entscheidungen Jakob Busch

## Ziel
Rechenkern für die 3D-Animation der Betriebsschwingform nach FG-04 und Nachtrag 1, ohne Oberfläche.

## Vorgehen
1. AN1 Spike (nur Scratchpad): `set_box_aspect(zoom=)` bleibt über `draw` erhalten; matplotlib-Maussteuerung abschaltbar; Standbild als Vektor-PDF möglich; 34 ms je Bild mit Achsen, 5,6 ms ohne (Linux-Container, Verhältniswerte).
2. AN2: neues Modul `auswertung/animation.py` (Auslenkung d̂ = −i·v̂/ω, relativer Bezug mit gemeinsamer Phase, D_ref, Überhöhung, Bildwinkel, Masken A-1), Referenzfälle RF-A1–A14 und RF-N1–N7 als Tests.
3. Fachabnahme: FREIGABE MIT AUFLAGEN (M-1 Bezugspunkt-Prüfung über den Haupteinstieg, M-2 Test-Sollwerte, M-3 Wertebereich, N-1–N-3). Nutzer wählte alle zur Behebung.
4. Korrektur K-AN2; bei M-2 wurden die in FG-04 gedruckten Werte (0,856 %, 0,095 %) übernommen, Toleranz halbe Einheit der letzten Stelle.

## Ergebnis
66 Tests grün, `animation.py` 100 % Zeilen- und Zweigabdeckung; `momentanwert` unverändert.

## Verifikation
Orchestrator nach K-AN2: `pytest tests/auswertung/test_aw_animation.py` 66 passed, ruff und mypy --strict ohne Befund. Fachabnahme mit eigenen Gegenbeispielen (Zeitverschiebung, Drehsinn, Pivot) bestätigt. Gesamtsuite wegen paralleler Pakete (Etappe B) zum Zeitpunkt nicht vollständig grün; dieser Commit enthält nur die zwei neuen Dateien.

## Probleme und verworfene Ansätze
- Fachabnahme nannte für M-2 Werte, die von FG-04 abwichen; maßgeblich ist die freigegebene Fachgrundlage.
- Coverage-Messung nur für das Einzelmodul scheitert an doppeltem numpy-Import; Messung über das Paket `auswertung`.

## Offene Punkte
- AN3 (Datenvertrag 3D) folgt nach Etappe B; Docstring-Zusatz „Schnelle“ in `schwingform.py`.
- Tempo am Messrechner und über Remotedesktop (UI-38).

## Thesis-Bezug
4.4 Auswertung und Darstellung (Animation), 3.3 Betriebsschwingformen.
