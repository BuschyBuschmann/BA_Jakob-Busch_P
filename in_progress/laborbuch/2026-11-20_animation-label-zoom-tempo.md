# 2026-11-20 – Animation: Punktlabels und Zoom-Messung beschleunigt

**Art:** Arbeitspaket
**Paket/Bezug:** U-LABEL, R-LABEL, K-LABEL-ZOOM, R-LABEL-ZOOM (verloren), U-LABEL-ZOOM-2, R-LABEL-ZOOM-2; R-071; Plan P-AUSW3 4.2 (≤ 400 ms je Wechsel)
**Commit:** 7eaf3df (Stand vor dem Paket-Commit)
**Beteiligt:** software-engineer (sonnet), reviewer (opus); Entscheidungen Jakob Busch

## Ziel
Blick- und Zoomwechsel der 3D-Animation bei vielen Punkten mit eingeschalteten Punktlabels unter 400 ms, ohne sichtbare Verhaltensänderung.

## Vorgehen
1. Review AN8/AN9 meldete ca. 0,5 s je Blick-/Zoomwechsel bei 1500 Punkten durch die Label-Dichte. Nutzer: „Beheben bitte“.
2. U-LABEL: Textmaße zwischenspeichern, Zeichnen vor der Label-Bewertung weglassen. Review: FREIGABE MIT AUFLAGEN (nach Größenänderung ohne Zeichnen bis 54 px falsch, Kommentar falsch; Schlüssel über Hash). Blickwechsel weiter ca. 0,55 s durch die Zoom-Messung; Nutzer: „Jetzt angehen“.
3. K-LABEL-ZOOM: Zeichnen nur bei geänderter Größe/DPI, Schlüssel über die Schrift, Zoom-Messung ohne Punkte (`_ohne_punkte`). Review: FREIGABE MIT AUFLAGEN (vier kleine Punkte), Nutzer: alle beheben.
4. Vor dem Commit wurde der Container ersetzt; die nicht committeten, reviewten Änderungen und die Sicherungen im Scratchpad gingen verloren.
5. U-LABEL-ZOOM-2: Neuaufbau nach den Berichten, mit den vier Auflagen (Zeichenstand über `draw_event`, unveränderlicher Schlüssel, Docstring, Referenztest gegen volles Zeichnen). Review: FREIGABE MIT AUFLAGEN, Orakelvergleich ohne Abweichung.

## Ergebnis
Sandbox (Agg, 11×6,8 in, 100 dpi): 1500 Punkte 869 → 232 ms, 135 Punkte 518 → 174 ms je Blickwechsel; Reviewer 145–149 ms ohne Canvas-Zeichnen. Zoom und Labelauswahl bitgleich zu vorher.

## Verifikation
Umsetzer: ruff, Format, mypy --strict grün; 2951 passed, Abdeckung 98,37 %; GUI 575 passed, 6 failed – dieselben 6 Layout-Tests der 2D-Ansichten scheitern auch auf unverändertem HEAD 7eaf3df (Reviewer per `git stash` bestätigt); vermutete Ursache Schriftumgebung des neuen Containers (Qt-Standardschrift „Inter 9 pt“), nicht bewiesen. Reviewer: 284 gezielte Tests grün, Mutationsproben, kein Callback-Leck.

## Probleme und verworfene Ansätze
Verlust nicht committeter Arbeit durch Containerwechsel. Erste Fassung zeichnete nach Größenänderung nicht neu (falsche Label-Rechtecke).

## Offene Punkte
MINOR: Reihenfolgetest von `_ohne_punkte` ohne fremde Artists nicht trennscharf; NITPICK: Gültigkeit von `LabelMasse` nur an DPI gekoppelt; HiDPI unter Qt ungeprüft; 6 GUI-Tests im neuen Container rot (Umgebung); Messung am Messrechner (M1).

## Thesis-Bezug
4.4 Darstellung (Animation), 5.3/5.4 Leistung und Grenzen.
