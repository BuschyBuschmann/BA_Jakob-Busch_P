# 2026-11-05 – Auswertungsoberfläche T3b: Ansichten 2 bis 4 im Reiter „Auswerten“

**Art:** Arbeitspaket
**Paket/Bezug:** U-AUSW-T3b, Korrekturen K-AUSW-T3b, -T3b-2, -T3b-3, -T3b-4; Reviews R-AUSW-T3b, RR-AUSW-T3b, RR-AUSW-T3b-2; Design-Abnahmen DA-AUSW-T3b, -T3b-2, -T3b-3; ADR-026 mit Nachträgen; R-032, R-050–R-053, R-055
**Commit:** f755307 (Stand vor diesem Eintrag)
**Beteiligt:** software-engineer (sonnet, haiku), reviewer (opus), ui-designer (sonnet); Entscheidungen Jakob

## Ziel
Ansichten 2 (H1/H2, Kohärenz, Phase), 3 (Spitzen und Bänder) und 4 (Schwingform) im Reiter bedienbar; alle Hinweise der Zeichenfunktionen sichtbar; Auflagen aus T3a.

## Vorgehen
Umsetzung; Review (NACHARBEIT: Ansicht 4 zeigte nach ungültiger Frequenz fremden Plot) und Design-Abnahme (Tabelle nur 2 Zeilen) parallel; Korrektur 1 (u. a. Kurztext M8, Kanalpaar in Ansicht 4, Segmentzeilen); Re-Review (NACHARBEIT: Zoom anderer Ansichten im Rückfall gelöscht) und Design-Re-Abnahme (Plot nur 140 px); Korrektur 2 (Spitzenangaben in der Auswahlspalte, kein Streifen in der GUI); Korrektur 3 (Legende in die Spalte, 4 Zeilen); abschließendes Re-Review und Design-Abnahme; Hinweistext korrigiert. Zwei Container-Neustarts und zwei Ratenlimits unterbrachen die Arbeit.

## Ergebnis
- Ansicht 2: Kanalpaarwahl (gemeinsam für alle Ansichten), H1/H2, Phase mit Kennzeichen „⚠ unbestätigt (M8: Polarität der Referenzkanäle offen)“, Formel nur im Tooltip; Platzhalter beim Mittel.
- Ansicht 3: Tabellen „Spitzen | Bänder“ im Splitter unter dem Plot (4 Zeilen, Position gemerkt), Angaben der gewählten Spitze und Kurvenlegende in der Auswahlspalte, im Plot nur Ring; Plotachse 203 px bei 1366×768, 115 px bei 1100×680; Bandzeilen über neue additive Kernfelder `Bandwert.art/kanal/mittel`.
- Ansicht 4: Frequenzfeld mit „nächste Linie“ (Start auf Linie der höchsten Spitze), Schnellwahl, Ebene und Komponente als Segmentzeilen, Betrag | Phase gegen Ref1 | Phase relativ, Kennzeichen aus der Spitze der Linie (Sprung-Hinweis), Hinweise sichtbar.
- Zoom je Ansicht erhalten, nur Dateiwechsel setzt zurück; Rückfallpfade abgesichert, Folgefehler protokolliert; Layout-Warnungen von matplotlib werden als Testfehler behandelt.

## Verifikation
Abschließend vom Orchestrator: 2021 passed, GUI 233 passed, ruff, format, mypy --strict sauber. Re-Review RR-AUSW-T3b-2: FREIGABE MIT AUFLAGEN (Hinweistext – behoben); Design-Abnahme DA-AUSW-T3b-3: FREIGABE MIT AUFLAGEN (Hinweistext – behoben).

## Probleme und verworfene Ansätze
- Tabelle in der 260-px-Spalte (Brief) passte nicht; 6 Zeilen unter dem Plot ließen nur 140 px Plot; Beschriftungsstreifen im kleinen Plot quetschte die Kurve (ADR-026, Nachträge 1 und 2).
- Der erste Fix für den fremden Plot löschte den Zoom anderer Ansichten.

## Offene Punkte
- MINOR (Design): längster Kennzeichen-Textblock nicht belegt; Angaben optisch kaum von der Legende abgesetzt; Pfeile in Ansicht 4 bei 1366×768 klein (Hinweis erscheint).
- Wechsel auf Ansicht 3 beim ersten Paar 0,49 s (Ziel < 400 ms), am Messrechner zu messen.
- T4: Export, Bild speichern (mit Thesis-Voreinstellungen), Tastatur, Cursor; T5: Installation 0.3.0 und Messrechner-Prüfung.

## Thesis-Bezug
Umsetzung der Auswertungsoberfläche; Gestaltungsentscheidungen mit Messwerten (ADR-026).
