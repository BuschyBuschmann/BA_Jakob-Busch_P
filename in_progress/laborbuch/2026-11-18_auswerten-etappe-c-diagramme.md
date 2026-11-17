# 2026-11-18 – Auswerten Etappe C: eigene Diagramme, Bild speichern in Ansicht 5, Abschluss (R-059)

**Art:** Arbeitspaket
**Paket/Bezug:** U-AUSW2-C, K-AUSW2-C, K-AUSW2-C-E; R-059; Plan P-AUSW2 S8–S10; Brief K1-AUSW2; ADR-027, ADR-028
**Commit:** 95e56e9 (Stand vor dem Paket-Commit)
**Beteiligt:** software-engineer (sonnet: Umsetzung; haiku: Korrektur; opus: Eskalation), reviewer (opus), ui-designer (sonnet); Entscheidungen Jakob Busch

## Ziel
Serienliste vervollständigen, „Aus aktueller Ansicht übernehmen“, „Bild speichern“ in Ansicht 5 mit Stempel aller Dateien, Querschnitt (Tastatur, Layout, Kontrast), Prüfanleitung für den Messrechner.

## Vorgehen
1. Umsetzung S8–S10 (mehrfach durch Nutzungslimits unterbrochen).
2. Design-Abnahme: FREIGABE; Code-Review: FREIGABE MIT AUFLAGEN (Teilgrößenregel zu streng, Wirkung der Neuvermessung unbelegt, Fokuswechsel-Test fehlte, Kleinigkeiten). Nutzer wählte alle Befunde sowie dunkleren Text für deaktivierte Knöpfe und das Entfernen des Hinweistexts.
3. Korrektur (haiku): drei Punkte erledigt, Punkt Layout BLOCKIERT – nach Entfernen des Hinweistexts scrollte die Auswahlspalte bei 1100×680, Ursache nicht gefunden.
4. Eskalation an opus: Ursache gefunden – beim Umschalten auf die kompakte Anzeige behielt das Spaltenlayout die alte Höhe der Anordnungsknöpfe (27 px); Behebung mit `updateGeometry()`, Hilfsmethode `_ad_neu_vermessen` entfällt, Regressionstest ergänzt.

## Ergebnis
Serie bearbeiten, Übernahme aus Ansicht 1–3, Bild speichern in Ansicht 5 (Stempel je Datei, Git-Hash, M8-Zeile), Text deaktivierter Knöpfe `#626B72` (≥ 4,5:1), keine Bildlaufleiste bei 1366×768 und 1100×680 mit vier Serien; Prüfanleitung `in_progress/versuche/naechster-termin_messrechner/pruefanleitung_auswerten_vergleich.md`.

## Verifikation
Eskalation gemeldet: 2702 passed (Standard), 436 passed (GUI), Abdeckung 98,50 %. Orchestrator nach dem letzten Stand: ruff, ruff format, mypy --strict ohne Befund; 86 Tests der Etappe-C-Dateien grün. Korrekturen (nur MINOR) nicht erneut reviewt.

## Probleme und verworfene Ansätze
Mehrere Versuche, die Spaltenhöhe per Timer/Neuvermessung zu korrigieren, scheiterten; Ursache war ein veralteter Layout-Zwischenwert.

## Offene Punkte
UI-38 am Messrechner (Prüfanleitung, u. a. B9); Plan P-AUSW2 damit abgeschlossen bis auf Hardwareprüfung.

## Thesis-Bezug
4.4/4.5 Auswertung und Oberfläche.
