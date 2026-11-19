# Checkliste Montag 2026-11-23 (Messrechner, ganzer Tag)

> **Verschoben auf Montag 2026-11-23, ganzer Tag. Der Termin am 2026-11-09 ist ausgefallen (Messrechner nicht verfügbar); keiner seiner Punkte wurde durchgeführt.** Aktualisiert am 2026-11-18 (Paket P-TERMIN-23). Neu eingehängt: Abgleich lesen (Block 4a), Auswerten-Prüfungen und bedingte Animation (Block 6a). Ordner- und Dateinamen mit `2026-11-09` (Versuchsplan, Laborbuch) bleiben unverändert.

Zum Abhaken. Tagesreihenfolge: [Versuchsplan 5.3](../2026-11-09_pruefdateien-warteschlange/versuchsplan.md). Weiter, Abbruch und Ersatz: [ablaufplan.md](ablaufplan.md). Eintragen: [protokoll.md](protokoll.md) (Termin) und für R, A, B, T4 bis T6 zusätzlich [Warteschlangen-Protokoll](../2026-11-09_pruefdateien-warteschlange/protokoll.md), Abschnitte 2 und 3. Muss-Punkte sind **fett**. Dauern sind Annahmen [A]. Anleitungen der neuen Prüfungen: `pruefanleitung_abgleich.md` (AB), `pruefanleitung_auswerten.md` (W), `pruefanleitung_auswerten_vergleich.md` (**AV**, Abschnitte A bis E mit Zeilen V1 bis V4, B1 bis B9, C1 bis C9, D1 bis D6, E1 bis E4; zur Unterscheidung von den Ablaufplan-Punkten B1, C1, D1, E1 immer mit Präfix AV).
Nichts gilt als bestanden, bevor Jakob es bestätigt hat. Ein Hardwaretest gilt erst nach dieser Bestätigung.

## Regeln (immer)
- Rohdaten nie überschreiben; neue Dateinamen; File Access nur auf Kopien.
- Messdaten nicht unter `PyCharmProject` und nicht in Polytec-Ordnern.
- Jede Messung nur nach **eigener** Entscheidung (Zeit, Grund ins Protokoll).
- Nur eine PSV-Instanz; PSV nie per Skript starten; PSV nicht beenden, solange eine Messung läuft.
- Hängt PSV oder steht ein Dialog: nichts hektisch klicken. Foto, Strg+C, Daniel (EP-5).
- Nach einem Abbruchkriterium keine weiteren Messtests.
- Shaker und Verstärker getrennt, solange für den Schritt keine Bestätigung vorliegt. Generator-Amplitude 0,02 V; 0,04 V ist offen (F2a).
- Abgleich: nur **lesen**, nichts auslösen oder ungültig machen; Modus **warnen**, nie eine Messung verweigern; Prüfgrenzen nur in der Konfigurationsdatei, ohne Standardwerte, nichts erfinden (Nutzerentscheidung 2026-11-18, KONVENTIONEN).

## Block 1: Start und COM (100 bis 130 min)
- [ ] **A0** COM-Registrierung prüfen (`Get-Process PSV`, Stufe 0), PID notieren, Datum und Befehl ins Protokoll [A0]
- [ ] **Notieren:** Arbeitsspeicher gesamt und frei (Task-Manager, Leistung) und `git -C "D:\Messdaten\DAL\BA Jakob Busch\PyCharmProject" status` (Ausgabe ins Protokoll; nur lesen; Hash-Quelle der Build-Info, Laborbuch 2026-11-06; ist `git` nicht vorhanden: „kein git“ notieren)
- [ ] **A1** Wheel 0.2.0 installieren (neuer Build, Hash und SHA-256 laut `stick/LIESMICH.txt`; Build 1208ea2be20a5a45a9475f5acb7c6cb9151bbfad, SHA-256 1947897ee964cf10f2754a7b3e9db817487dc2018c446c3131adf5619f189552), I1 bis I7 (bei Zeitverlust I1 bis I4) [A1]
- [ ] N1 bis N7 Installationsprüfung Auswerten direkt nach A1; N1 bis N3 fehlgeschlagen: nichts weiter installieren (EP-3) [4.3]
- [ ] **C1** Kopien der Beispieldatei `20261012_ref_Mitte.svd` anlegen; C2, C3, N7 und `einstellungen_lesen.py` nur auf Kopien [Zweig C]
- [ ] **B1** Erkundung Stufe 1 über „PSV 10.4 Deutsch“ (`/Acquisition`). Verbinden scheitert: Fehlerbild sichern, dann EP-1. Ergebnis `P1-6-abgleich` (`Alignments3D.Count`, `Valid`, `CurrentQuality`, Fehlerbild) notieren (Voraussetzung für Block 4a)
- [ ] **B2** Ergebnisse sichern, Konfigkopie mit SHA-256 [B2]; Konfig mit `abgleich_pruefung` = `warnen`, **keine** Grenzwerte eingetragen (Vorlage `stick/konfig/beispiel_messrechner.json`)
- [ ] **B3** Test-.set: Generator aus, Bandbreite ≠ 5600 Hz, Mittelung 3 [B3]
- [ ] **T1** NUR_LESEN, **T2** TROCKENLAUF; Einrastwert bei 5600 Hz notieren [B4]. Vor T2: Abgleichstatus in PSV notieren (Foto); die Lademaske enthält `Alignment`, der Trockenlauf ersetzt den geladenen Abgleich durch den der Test-.set (Prüfanleitung Abgleich, Sicherheitsrahmen)
- [ ] C4 Generator-Dialog nur ablesen (Soll; Voraussetzung für `mess_3x3.set` in Block 2, FG-V1)
- [ ] C2 (M11 an drei Spitzen) und C3 (Golden File v2) in Wartezeiten [Zweig C]

## Block 2: Prüfdateien R, A, B (ca. 50 min)
- [ ] **Freigabe** der Anregung im Protokoll (Daniel, Uhrzeit); R, A, B laufen direkt in PSV
- [ ] **`mess_3x3.set`** aus einer Kopie der Einstellungen vom 12.10.; Original unverändert; Rücklesen mit `einstellungen_lesen.py` [Versuchsplan 4]
- [ ] **R** messen, `20261123_ref3x3_01.svd`; Foto; Kopie und SHA-256
- [ ] **A** nur Fenster auf Hanning, `20261123_hann3x3_01.svd`; Foto; Fenster zurück auf Rechteck, Foto
- [ ] **B** nur Mittelung auf Betrag, Anzahl 10, `20261123_betrag10_3x3_01.svd`; Foto; zurück auf komplex 7, Foto
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

## Block 4a: Abgleich lesen (R-003a, `pruefanleitung_abgleich.md`, Dauer offen, [A] ca. 30 min)
Voraussetzungen der Anleitung: `P1-6-abgleich` notiert (Block 1), Wheel mit dieser Funktion (neuer Build), I5 grün, keine Datei mit `"schema_version": 2` unter `$ARB\daten`. Nur lesen: Laser und Spiegel bewegen sich nicht, kein Scan, Generator aus. Eine Abweichung ist ein Befund, keine Korrektur vor Ort.
- [ ] **AB1** Start mit Konfig-Kopie `konfig_abgleich_aus.json` (Modus `aus`, keine Grenze; in der Kopie `abgleich_pruefung` auf `aus` setzen, die Stick-Vorlage steht auf `warnen`), `Get-FileHash` notieren
- [ ] **AB2** Trockenlauf mit einer Test-.set (T2, Generator aus): keine Bewegung, keine Dialogmeldung von PSV
- [ ] **AB3** Feld `abgleich` im Messprotokoll lesen (gelesen, Grund, Anzahl 3D/2D, je Eintrag gültig, Qualität, Unsicherheiten, `nicht_lesbar`)
- [ ] **AB4** Einheit und Größenordnung gegen die PSV-Anzeige des 3D-Abgleichs (Software: m und rad)
- [ ] **AB5** Ereignisprotokoll und Protokollfenster: Hinweis „Abgleich auffällig“ nur bei ungültigem oder unvollständig gelesenem Abgleich
- [ ] **AB6** Indexbasis: `Item(1)` liefert den ersten Abgleich; **nicht** `Item(0)` probieren
- [ ] AB9 (Soll) Modus `warnen` mit strenger Prüfgrenze aus dem gelesenen Messwert (Prüfwert der Anleitung, keine fachliche Grenze); nur wenn AB3 `qualitaet_ist_m` > 0 liefert, sonst entfällt AB9 mit Vermerk
- [ ] AB10 (Kann) ungültige Konfig (`abgleich_qualitaet_max_m` = 0): Start bricht mit Rückgabewert 2 ab
- [ ] AB7, AB8, AB11 (Modus `verweigern`, Kann): nur im Trockenlauf auf einer Konfig-Kopie (Nutzerentscheidung 2026-11-18); Betrieb bleibt `warnen`
- [ ] Befunde und `abgleich`-Blöcke der Protokolle (AB3, AB9) auf den Stick sichern; Dauer des Abgleich-Lesens aus dem Zugriffsprotokoll notieren

## Block 5: Zeitdaten-Scan (15 bis 20 min) [D1]
- [ ] SE-Einstellung fotografieren. `SaveTimeDataForScan` nur, wenn F4 geklärt ist
- [ ] 3×3-Scan mit Zeitdaten; Start und Ende nach Rechneruhr; SE zurückstellen (Foto)

## Block 6: Langscan oder Teilraster (40 bis 85 min)
- [ ] D4 nur mit Freigabe und eigener Entscheidung (Streichkandidat 1)
- [ ] E2 Handbücher kopieren, erst nach F8 (offen) [E2]
- [ ] In Wartezeiten (auch während D1 und T4 bis T6): C-Punkte und Auswerten-Prüfung W1 bis W10 [4.3, Dauer offen]

## Block 6a: Auswerten-Prüfungen (ohne PSV, nur Kopien; in Wartezeiten oder nach Block 6, Dauer offen)
- [ ] Vorab: Fenstergröße und Windows-Skalierung notieren; `tools\auswertung\speicher_messen.py` muss auf dem Stick liegen (siehe `stick/LIESMICH.txt`, **[offen]**)
- [ ] `pruefanleitung_auswerten.md` W1 bis W10 (Messskript, HiDPI, Cursor, Export, Bild, Drag-and-drop, INI) nach N1 bis N7
- [ ] `pruefanleitung_auswerten_vergleich.md` **AV-A V1, V2** (Speicher und Messungsgrenze; Soll): freien Arbeitsspeicher notieren, `speicher_messen.py` mit zwei Kopien, Summe gegen den freien Speicher; V3, V4 im Reiter „Auswerten“ mit vier bzw. fünf Messungen
- [ ] AV-B B1 bis B9 (Achsenleiste, Remotedesktop), AV-C C1 bis C9 (mehrere Messungen, Ansicht 5), AV-D D1 bis D6 (Bild speichern), AV-E E1 bis E4 (Tastatur, Lesbarkeit; Etappen B/C, UI-38 bleibt offen)
- [ ] **Animation (der Build enthält AN7 bis AN9, Wheel geprüft)** (Animation in Ansicht 4; erkennbar am Modusschalter „Standbild/Animation“ in Ansicht 4, fehlt er, entfällt der Block): Sichtprüfung nach Plan `in_progress/planung/plaene/2026-11-11_P-AUSW3_animation-plan.md` (Modus „Standbild“/„Animation“, Wiedergabe, Drehen, Zoom, Phase per ←/→, Pflichttexte im Bild, Kennzeichen M8, Modus gesperrt ohne Phase). Prüfanleitung `pruefanleitung_animation.md` (AN-1 bis AN-13). Messungen M1 bis M6 (Bildzeit, Bildrate, Maus-Ziehen, Phasenregler, `animation_daten`, Standbild speichern) mit `tools\auswertung\animation_messen.py` **durchführbar** (Skript samt `speicher_messen.py` auf dem Stick); M7 (Nutzerurteil über Remotedesktop) gehört dazu. UI-38 bleibt offen bis zur Bestätigung durch Jakob

## Block 7: Abschluss (60 min)
- [ ] X1 Desktop-Modus einmal bewusst, nach T6 [X1]
- [ ] E1 Platte und Impedanzkopf wiegen, **erst nach allen Messungen**; Fotos vorher (F5 offen)
- [ ] **A2** Sicherung spätestens 30 min vor Ende: Ordner, Protokoll, Fotos; PSV sauber; Shaker getrennt

## Streichreihenfolge bei Zeitmangel (Versuchsplan 5.3, Ablaufplan 4)
1. D4, 2. D1, 3. T6
4. Kann: D5 Rest (T3, T7), C7, C6, B5, C8, C5; neu: Animation (bedingt, Block 6a), AB10, W1 bis W10
5. Soll niedrig: X1 (bei COM-Fehler vorziehen); C4 nicht mit D1 streichen, sondern vor `mess_3x3.set` sichern
6. Soll mittel: E2, D3, C3; neu (Rang untereinander offen): AV (V1 bis E4), AB9. 7. Soll hoch: E1, C2; D2 zuletzt
**Nie streichen:** A0, A1 (mind. I1 bis I4), B1 (bei COM), A2. **Neu Muss:** AB1 bis AB6 (Abgleich lesen) wie B4 spät streichen. **Nicht pauschal:** R, A, B (Block 2, bei Anregung-Freigabe), T4, T5 (Entscheidung vor Ort). **D2 und E2 nie zusammen streichen.**
