# 2026-11-14 – Auswerten Etappe B: mehrere Messungen und Ansicht „Diagramm“ (R-058)

**Art:** Arbeitspaket
**Paket/Bezug:** U-AUSW2-B, K-AUSW2-B, K2-AUSW2-B; R-058 (Teile von R-059); Plan P-AUSW2 S4–S7; Brief K1-AUSW2; ADR-028
**Commit:** bc96597 (Stand vor dem Paket-Commit)
**Beteiligt:** software-engineer (sonnet), reviewer (opus), ui-designer (sonnet); Entscheidungen Jakob Busch

## Ziel
Mehrere Messungen gleichzeitig öffnen, aktiv wechseln und in einer neuen Ansicht 5 vergleichen (überlagert oder nebeneinander).

## Vorgehen
1. Umsetzung S4–S7: Qt-freie Messungsliste mit Delegation im Reiter, Messungsleiste mit Chips, Ladewarteschlange, Serienauflösung und `zeichne_diagramm` GUI-frei, Ansicht 5 mit Strg+5; Speicherskript `tools/auswertung/speicher_messen.py`. Mehrfach unterbrochen durch Nutzungslimits.
2. Review: NACHARBEIT NÖTIG – BLOCKER: bei „nebeneinander“ Kurven verschiedener Einheit auf einer Achse; MAJOR: Entfernen während „Öffnen …“ ersetzte die falsche Messung und ließ einen Prüfauftrag verwaist; MAJOR: y-Bereich nicht je Größe (Abweichung von der Freigabe). Design-Abnahme: NACHARBEIT NÖTIG – MAJOR: Kreuz am Chip unsichtbar.
3. Nutzer: y-Bereich je Größe wie freigegeben; alle kleinen Befunde zur Behebung; nachgeladene Messung wird aktiv.
4. Korrektur 1; Re-Review und Design-Re-Abnahme: je FREIGABE MIT AUFLAGEN; neu: Überschneidung mit offenen Dialogen.
5. Korrektur 2 (letzte Runde): Ziel von „Öffnen …“ beim Klick festgelegt, Aktivierung während Dialogen zurückgestellt; Auswahl der Betragsgröße für die Felder bei „nebeneinander“; kompakte Anzeige unter 1200 px Breite.

## Ergebnis
Bis zu vier Messungen; Ansicht 5 mit bis zu vier Serien, Einheitenregel je Teilbild, y-Bereich je Größe; Thesis-Abbildungen unverändert.

## Verifikation
K2 gemeldet: 2493 passed (Standard), 414 passed (GUI), Abdeckung 98,42 %, ruff/format/mypy ohne Befund. Re-Review nach Korrektur 1 hatte alle Läufe selbst ausgeführt. Orchestrator-Stichprobe nach K2: 52 Tests (Korrekturen, Diagramm) grün, ruff und mypy ohne Befund. Korrektur 2 nicht mehr gesondert reviewt (zweite Runde ausgeschöpft).

## Probleme und verworfene Ansätze
- Erste Fassung wandte die Einheitenregel nur bei „überlagert“ an.
- Gemeinsamer y-Bereich für alle Betragsgrößen widersprach der Freigabe F4/E11.

## Offene Punkte
- Fester Bereich je Größe gilt auch für Teilbilder gleicher Größe mit anderer Einheit (Folge von F4, zur Kenntnis).
- „Bild speichern“ in Ansicht 5 folgt mit S9; S8–S10 (R-059) offen.
- Speicher und Tempo am Messrechner (UI-38, `speicher_messen.py`).

## Thesis-Bezug
4.4/4.5 Auswertung und Oberfläche.
