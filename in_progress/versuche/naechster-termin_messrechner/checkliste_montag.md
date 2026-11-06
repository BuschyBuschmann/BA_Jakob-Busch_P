# Checkliste Montag 2026-11-09 (Messrechner, ganzer Tag)

Zum Abhaken. Tagesreihenfolge: [Versuchsplan 5.3](../2026-11-09_pruefdateien-warteschlange/versuchsplan.md). Weiter, Abbruch und Ersatz: [ablaufplan.md](ablaufplan.md). Eintragen: [protokoll.md](protokoll.md) (Termin) und für R, A, B, T4 bis T6 zusätzlich [Warteschlangen-Protokoll](../2026-11-09_pruefdateien-warteschlange/protokoll.md), Abschnitte 2 und 3. Muss-Punkte sind **fett**. Dauern sind Annahmen [A].
Nichts gilt als bestanden, bevor Jakob es bestätigt hat. Ein Hardwaretest gilt erst nach dieser Bestätigung.

## Regeln (immer)
- Rohdaten nie überschreiben; neue Dateinamen; File Access nur auf Kopien.
- Messdaten nicht unter `PyCharmProject` und nicht in Polytec-Ordnern.
- Jede Messung nur nach **eigener** Entscheidung (Zeit, Grund ins Protokoll).
- Nur eine PSV-Instanz; PSV nie per Skript starten; PSV nicht beenden, solange eine Messung läuft.
- Hängt PSV oder steht ein Dialog: nichts hektisch klicken. Foto, Strg+C, Daniel (EP-5).
- Nach einem Abbruchkriterium keine weiteren Messtests.
- Shaker und Verstärker getrennt, solange für den Schritt keine Bestätigung vorliegt. Generator-Amplitude 0,02 V; 0,04 V ist offen (F2a).

## Block 1: Start und COM (100 bis 130 min)
- [ ] **A0** COM-Registrierung prüfen (`Get-Process PSV`, Stufe 0), PID notieren, Datum und Befehl ins Protokoll [A0]
- [ ] **A1** Wheel 0.2.0 installieren, I1 bis I7 (bei Zeitverlust I1 bis I4) [A1]
- [ ] N1 bis N7 Installationsprüfung Auswerten direkt nach A1; N1 bis N3 fehlgeschlagen: nichts weiter installieren (EP-3) [4.3]
- [ ] **C1** Kopien der Beispieldatei `20261012_ref_Mitte.svd` anlegen; C2, C3, N7 und `einstellungen_lesen.py` nur auf Kopien [Zweig C]
- [ ] **B1** Erkundung Stufe 1 über „PSV 10.4 Deutsch“ (`/Acquisition`). Verbinden scheitert: Fehlerbild sichern, dann EP-1
- [ ] **B2** Ergebnisse sichern, Konfigkopie mit SHA-256 [B2]
- [ ] **B3** Test-.set: Generator aus, Bandbreite ≠ 5600 Hz, Mittelung 3 [B3]
- [ ] **T1** NUR_LESEN, **T2** TROCKENLAUF; Einrastwert bei 5600 Hz notieren [B4]
- [ ] C4 Generator-Dialog nur ablesen (Soll; Voraussetzung für `mess_3x3.set` in Block 2, FG-V1)
- [ ] C2 (M11 an drei Spitzen) und C3 (Golden File v2) in Wartezeiten [Zweig C]

## Block 2: Prüfdateien R, A, B (ca. 50 min)
- [ ] **Freigabe** der Anregung im Protokoll (Daniel, Uhrzeit); R, A, B laufen direkt in PSV
- [ ] **`mess_3x3.set`** aus einer Kopie der Einstellungen vom 12.10.; Original unverändert; Rücklesen mit `einstellungen_lesen.py` [Versuchsplan 4]
- [ ] **R** messen, `20261109_ref3x3_01.svd`; Foto; Kopie und SHA-256
- [ ] **A** nur Fenster auf Hanning, `20261109_hann3x3_01.svd`; Foto; Fenster zurück auf Rechteck, Foto
- [ ] **B** nur Mittelung auf Betrag, Anzahl 10, `20261109_betrag10_3x3_01.svd`; Foto; zurück auf komplex 7, Foto
- [ ] Nach jeder Datei `einstellungen_lesen.py` auf der Kopie [Versuchsplan 5.1]

## Block 3: Anregung am Kopf (ca. 70 min)
- [ ] D2 Impedanzkopf: Sichtbarkeit höchstens 10 min. Folie nur mit Zustimmung Daniel (F6), sonst Ersatzpunkt Plattenvorderseite. Vorzeichen-Tabelle [D2]
- [ ] D3 A-B-A 0,02 / 0,04 / 0,02 V; 0,04 V nur nach Klärung (F2a). Kraft: Betrag/CPH ≈ 2, AP ≈ 4. Danach 0,02 V zurück [D3]
- [ ] Reihenfolge: D2 normal nach R, A, B (Versuchsplan 5.3); vorziehen nur, wenn die Sichtbarkeitsprüfung (höchstens 10 min) schnell gelingt (Versuchsplan 5.3, Ablaufplan 4.2)

## Block 4: Trockenlauf und Warteschlange (ca. 95 min) · Entscheidung vor Ort für T4 bis T6 (Voraussetzung: T1/T2 ohne Befund, Freigabe dokumentiert; Versuchsplan 5.2)
- [ ] Trockenlauf mit `mess_3x3.set` bis T4; Generatorzustand beobachten, Foto; Setter `mittelung.typ` rücklesen [H]
- [ ] T4 `konfig/T4_eine_messung.warteschlange.json`; .set-Pfad prüfen; Zeitlimit 600 s
- [ ] T5 Abbruch einer laufenden Messung [D5]
- [ ] T6 `konfig/T6_drei_messungen.warteschlange.json`; M3 mit 90 s muss auslösen [D5]

## Block 5: Zeitdaten-Scan (15 bis 20 min) [D1]
- [ ] SE-Einstellung fotografieren. `SaveTimeDataForScan` nur, wenn F4 geklärt ist
- [ ] 3×3-Scan mit Zeitdaten; Start und Ende nach Rechneruhr; SE zurückstellen (Foto)

## Block 6: Langscan oder Teilraster (40 bis 85 min)
- [ ] D4 nur mit Freigabe und eigener Entscheidung (Streichkandidat 1)
- [ ] E2 Handbücher kopieren, erst nach F8 (offen) [E2]
- [ ] In Wartezeiten (auch während D1 und T4 bis T6): C-Punkte und Auswerten-Prüfung W1 bis W10 [4.3, Dauer offen]

## Block 7: Abschluss (60 min)
- [ ] X1 Desktop-Modus einmal bewusst, nach T6 [X1]
- [ ] E1 Platte und Impedanzkopf wiegen, **erst nach allen Messungen**; Fotos vorher (F5 offen)
- [ ] **A2** Sicherung spätestens 30 min vor Ende: Ordner, Protokoll, Fotos; PSV sauber; Shaker getrennt

## Streichreihenfolge bei Zeitmangel (Versuchsplan 5.3, Ablaufplan 4)
1. D4, 2. D1, 3. T6
4. Kann: D5 Rest (T3, T7), C7, C6, B5, C8, C5
5. Soll niedrig: X1 (bei COM-Fehler vorziehen); C4 nicht mit D1 streichen, sondern vor `mess_3x3.set` sichern
6. Soll mittel: E2, D3, C3. 7. Soll hoch: E1, C2; D2 zuletzt
**Nie streichen:** A0, A1 (mind. I1 bis I4), B1 (bei COM), A2. **Nicht pauschal:** R, A, B (Block 2, bei Anregung-Freigabe), T4, T5 (Entscheidung vor Ort). **D2 und E2 nie zusammen streichen.**
