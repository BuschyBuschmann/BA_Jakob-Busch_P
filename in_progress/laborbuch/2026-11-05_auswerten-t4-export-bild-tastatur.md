# 2026-11-05 – Auswertungsoberfläche T4: Export, Bild speichern, Cursor, Tastatur (Zwischenstand)

**Art:** Arbeitspaket (vom Nutzer als Zwischenstand zum Commit freigegeben)
**Paket/Bezug:** U-AUSW-T4, Korrekturen K-AUSW-T4, K-AUSW-T4-2; Review R-AUSW-T4, Re-Reviews RR-AUSW-T4, RR-AUSW-T4-2; Design-Abnahmen DA-AUSW-T4, DA-AUSW-T4-2; R-032, R-050–R-055; ADR-022, ADR-026
**Commit:** 6157d61 (Stand vor diesem Eintrag)
**Beteiligt:** software-engineer (sonnet), reviewer (opus), ui-designer (sonnet); Entscheidungen Jakob

## Ziel
Bedienung vervollständigen: Daten exportieren, Arbeitsbild speichern, Fadenkreuz-Cursor, Klick-Frequenz, Tastenkürzel, Prüfdialog, „Zuletzt geöffnet“, Drag-and-drop.

## Vorgehen
Umsetzung (durch Ratenlimit unterbrochen); Review (FREIGABE MIT AUFLAGEN) und Design-Abnahme (NACHARBEIT: Fußzeile bei 1100×680) parallel; Korrektur 1; Re-Review (NACHARBEIT: Warnzahl im Prüftext ausgeblendet) und Design-Re-Abnahme (gleicher Befund); Korrektur 2; Re-Review RR-AUSW-T4-2: neuer MAJOR (siehe Offene Punkte).

## Ergebnis
- Export als Hintergrundauftrag C mit Überschreibschutz; Vorschlag aus Ordner und Basisname der angezeigten Messdatei; verwaiste .tmp-Dateien eines abgebrochenen Exports werden beim nächsten Export gemeldet und entfernt (Export-Kern rein additiv, bytegleich); Rückfrage beim Schließen während eines Exports.
- Bild speichern (PNG/PDF) mit Stempel „Arbeitsansicht – nicht für die Thesis“, Git-Hash und M8-Zusatz nur bei gezeichneter Phase; Voreinstellungen der Zeichenfunktion (ADR-026 Nachtrag 2), Zoom übernommen (Ansicht 3 nur x).
- Fadenkreuz-Cursor mit Blitting, Cursorzeile mit Werten in 3 signifikanten Stellen (m·10ⁿ außerhalb 10⁻³…10⁶), Einheit hinter der Kurvenliste; Meldezeile kürzt Pfade mittig, Volltext im Tooltip.
- Tastenkürzel aus einer Quelle (`AKTIONS_TASTEN`), F5–F8 im Reiter „Auswerten“ wirkungslos; Prüfdialog springt zur ersten Auffälligkeit; Prüftext nach Auffälligkeit geordnet („1 Warnung, …, 36 ok“); Zuletzt-Liste (32 px, „nicht gefunden“ 5,87:1), Drag-and-drop mit Hinweis.

## Verifikation
Nach Container-Neustart vom Orchestrator: 2078 passed, GUI 298 passed, ruff, format, mypy --strict sauber.

## Probleme und verworfene Ansätze
- Breitenverteilung der Fußzeile brauchte zwei Runden; die erste Lösung gab der Meldezeile Vorrang und blendete die Warnzahl aus.
- Mehrere Ratenlimits und ein Container-Neustart unterbrachen Umsetzung und Review.

## Offene Punkte
- **Offener MAJOR (RR-AUSW-T4-2), nach Nutzerentscheidung erster Punkt in T5:** Ein langer Fehlertext der Prüfung (z. B. mit Pfad) hat keine Obergrenze in `_fuss_verteilen`; der Prüftext wird breiter als die Fußzeile und die Meldezeile verschwindet (UI-25, Brief Abschnitt 10).
- Windows/Messrechner: Blitting-Tempo, echte Dialoge, Prozess-Export, Explorer-Drag-and-drop, INI-Ort, Consolas-Breiten.

## Thesis-Bezug
Umsetzung und Bedienkonzept der Auswertungsoberfläche.
