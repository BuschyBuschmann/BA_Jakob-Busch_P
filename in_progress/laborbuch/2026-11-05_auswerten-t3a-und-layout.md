# 2026-11-05 – Auswertungsoberfläche T3a (Reiter „Auswerten“, Ansicht 1) und Layout der Zeichenfunktionen (Zwischenstand)

**Art:** Arbeitspaket (Zwischenstand, vom Nutzer zum Commit freigegeben)
**Paket/Bezug:** U-AUSW-T3a mit Korrektur K-AUSW-T3a; K-AUSW-T2c (Layout, Pfeile, Mittelformel, M6, 3D-Punktmenge, Formate); Reviews R-AUSW-T3a, RR-AUSW-T3a, R-AUSW-T2c; Design-Abnahme DA-AUSW-LAYOUT; Fachabnahme FAB-AUSW-T2c; R-032, R-050–R-053, R-055; ADR-022, ADR-024, ADR-025
**Commit:** b69dda1 (Stand vor diesem Eintrag)
**Beteiligt:** software-engineer (sonnet), reviewer (haiku, opus), ui-designer (sonnet), strukturdynamik-experte (sonnet); Entscheidungen Jakob

## Ziel
Reiter „Auswerten“ mit Dateileiste, Parameterzeile, Zuständen, zweistufigem Laden und Ansicht 1; Zeichenfunktionen nach den freigegebenen Layout-Vorgaben und den Nutzerentscheidungen vom 05.11.

## Vorgehen
T3a nach Container-Neustart aus Teilergebnissen fortgesetzt; Ratenlimit unterbrochen und fortgesetzt; Review → Korrektur → Re-Review. Parallel: Layout-Vorgaben (ui-designer, freigegeben), Umsetzung in `darstellung/`, danach Code-Review, Design- und Fachabnahme.

## Ergebnis
- Reiter „Messen | Auswerten“, lazy Aufbau mit Fehlerrückfall; Ladesteuerung über `hintergrund` (Job-ID, Abbruch, Stufe A/B); P-08 mit Treibpunkt Ref2/Ref1; Ansicht 1 vollständig; Aktionssperre im Reiter „Auswerten“; Zoom bleibt bei Auswahlwechsel; Fehler der Aufbereitung im Fehlerband.
- Parameterzeile der Beispieldatei: 1000 Hz, 1600, 0,625 Hz, Mittelung „7 (komplex)“ (plausibel), Fenster „–“.
- Zeichenfunktionen: Beschriftungsstreifen Ansicht 3, Pfeile konstanter Länge, Betrag über Markerfläche, M6-Raute, Mittelformel und Punktzahl im Bild, feste Nachkommastellen bei Frequenzen, Thesis-Beispiel mit stärkster Spitze und relativer Phase im Hochformat.
- Abweichungen vom Layout, vom Nutzer bestätigt: Streifen bis 50 % (Thesis 4,9 × 3,8 Zoll), Thesis-Schwingform-Höhe aus Datenaspekt (11,5 × 11,9 cm), Methode „-3dB-Breite“ wie im Export.

## Verifikation
Volle Suite 1953 passed, 99 %; GUI 145 passed; ruff, mypy --strict sauber (vom Orchestrator nach Neustart erneut ausgeführt). Bei gültigen Daten Zahlen bitgleich zur Basis (Review R-AUSW-T2c). Re-Review T3a: FREIGABE MIT AUFLAGEN; Review T2c: FREIGABE MIT AUFLAGEN.

## Probleme und verworfene Ansätze
- **Offene MAJOR-Befunde (Korrekturpaket folgt):** Design-Abnahme – heller Pfeilrand zerschneidet die Marker (Pfeil unter Marker legen); Fachabnahme – Thesis-Phasenabbildung ohne Linie, γ²_min und Spitzen-Kennzeichen (N-2); dazu N-1: Punktmenge hängt von der Komponentenauswahl ab.
- Zwei Container-Neustarts und ein Ratenlimit unterbrachen die Arbeit; T3a-Teilergebnisse wurden geprüft übernommen.
- Erstes T3a-Review: Ausnahmen nach Stufe A ließen den Reiter im Zustand „Laden“ hängen (behoben).

## Offene Punkte
- Korrekturpaket: Pfeil unter Marker, N-1, N-2, Rückfallpfad T3a absichern, Neuzeichnen bei Größenänderung, unsichere Punkte auch bei Betrag, kein stilles `except` im Thesis-Skript, eigene Bezeichnung für NaN-Beträge, Punktzahl einheitlich, Testlücken, Hinweis bei unregelmäßigen Punktwolken.
- Ansicht 2–4 in der Oberfläche (T3b), Export/Bild/Tastatur (T4), Installation 0.3.0 und Messrechner-Prüfung (T5).

**Nachtrag (K-AUSW-T3a-2):** Rückfallpfad nach Qt-Aufbaufehlern schrittweise abgesichert; Ansicht 3/4 werden bei Größenänderung entprellt (150 ms) neu gezeichnet, x-Zoom bleibt. Re-Review RR-AUSW-T3a-2: FREIGABE MIT AUFLAGEN (2 MINOR: Startpfad von `oeffne_datei` ungeschützt; sekundäre Fehler im Rückfall ohne Spur) – nach Nutzerentscheidung in T3b. Allein in sauberem Arbeitsbaum geprüft: 1953 passed, GUI 152 passed.

**Nachtrag (K-AUSW-D3):** offene MAJOR behoben – Pfeil unter dem Marker (zorder Ring 2,4 < Pfeil 2,5 < Marker 3; Änderung gegenüber Layout-Vorgabe 4.4/4.6 aus der Design-Abnahme), Thesis-Phase mit Linie, γ²_min, Bezugspunkt und Kennzeichen in Bild bzw. Begleit-JSON; N-1 gemeinsame Punktmenge nur bei 3D; unsichere Punkte auch im Betragsbild; „kein Messwert“ (Quadrat) getrennt von M6 (Raute); Dichtehinweis bei unregelmäßiger Punktwolke; kein stilles `except` im Thesis-Skript. Re-Review RR-AUSW-D3: FREIGABE (1970 passed, bei gültigen Daten bitgleich); Design-Re-Abnahme: FREIGABE; Fach-Re-Abnahme: FREIGABE. Offen (MINOR): Bezugsring vom Pfeilrand unterbrochen, Linie fehlt im Betragsbild, Phasensprung-Hinweis bei allen Kennzeichen statt nur auflösungsbegrenzt, doppelte Koordinaten ohne Hinweis; Bildunterschrift muss Auflösungshinweis übernehmen.

## Thesis-Bezug
Umsetzung der Auswertungsoberfläche; Darstellung und Lesbarkeit der Auswertung; Nebenläufigkeit.
