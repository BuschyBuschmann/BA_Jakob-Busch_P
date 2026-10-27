# Handtest U4: Oberfläche der Mess-Warteschlange (Simulatorbetrieb)

**Bezug:** Paket U4, Plan P2 (U4-1 bis U4-5), Design-Brief P3 (UI-1 bis UI-28), R-010 bis R-018, R-021, R-030, R-031.
**Zweck:** Jede Funktion R-010 bis R-018 und R-021 einmal **ohne Kommandozeile** über die Oberfläche auslösen (U4-1, UI-19). Kein Hardwaretest: alles läuft gegen den Simulator.
**Durchführung:** Nutzer · **Datum:** ________ · **Rechner:** ________ · **Git-Hash:** ________

## Vorbereitung

1. Aus `software/`: `uv sync`, dann einen leeren Ordner für Messdaten anlegen, z. B. `C:\ldv-test\daten` (nicht im Repository, nicht in Polytec-Ordnern).
2. Eine beliebige Datei als Einstellungsdatei anlegen, z. B. `C:\ldv-test\basis.set` (Inhalt egal; der Simulator liest sie nicht).
3. Start: `uv run python -m ldv_automation gui --simulator`
   (Die Kommandozeile dient nur dem Programmstart. Der Messdaten-Ordner wird im Test über „Einstellungen …“ gesetzt.)
4. Ein Simulator-Scan dauert etwa 9 s (9 Punkte × 1 s).

Ergebnis je Zeile: ✔ = wie erwartet, ✖ = abweichend (Beobachtung notieren).

## A Anzeige und Grundzustand

| Nr | Schritt | Erwartet | Bezug | Ergebnis |
|---|---|---|---|---|
| A1 | Fenster ansehen | Statuszeile schwarz mit `SIMULATOR`, „Durchgang: Bereit“, „Simulator aktiv“, „Fehlerstrategie: vorläufig (O1)“. Fenstertitel „LDV-Warteschlange – SIMULATOR“. | UI-14, U4-3 | |
| A2 | Leere Tabelle ansehen | Text „Noch keine Messung. Mit „+ Messung“ anlegen oder eine Warteschlange laden.“; `Start` grau, Tooltip nennt den Grund. Hinweisband zeigt „Simulator: Es entstehen Platzhalterdateien, keine Messdaten.“ | UI-1 | |
| A3 | Maus über `Start` | Tooltip „Start nicht möglich: keine wartende Messung.“ | UI-1 | |
| A4 | `Einstellungen …` → Ordner `C:\ldv-test\daten` wählen → `Übernehmen` | Dialog schließt. Feld „Standard-Zeitlimit“ ist grau mit Hinweis „Noch nicht einstellbar …“. | UI-25 | |
| A5 | `Gerät …` | Version „10.x-SIM“, Modus „Erfassung (Acquisition)“, Zustand „gestoppt“, Meldungen unterdrückt „ja“, Hardware, Messpunkte „nicht verfügbar …“. | UI-25 | |

## B Warteschlange bearbeiten (R-011 bis R-015, R-017)

| Nr | Schritt | Erwartet | Bezug | Ergebnis |
|---|---|---|---|---|
| B1 | `Strg+N` | Editor rechts „Neue Messung“, „wird eingefügt am Anfang“, Cursor im Feld Name. | UI-2, R-012 | |
| B2 | Name `Platte/1` eintippen | Rote Meldung „✖ Name: unzulässige Zeichen /“; `Übernehmen` grau. | UI-5 | |
| B3 | Name `M1`, `Wählen …` → `basis.set`; `Übernehmen` | Zeile 1 Nr „(01)“ grau/kursiv (vorläufig, Tooltip), „○ wartend“, Name M1, Datei basis.set, Änderungen „–“, Limit „Std.“; Zeile ist gewählt. | UI-2, R-011, R-012 | |
| B4 | `+ Messung` → `M2`, `.set` wählen; bei „Mittelung Anzahl“ `ändern` anhaken und `2` eintippen | Sofort „✖ Mittelung Anzahl: 2 liegt außerhalb 3 … 10000.“; `Übernehmen` grau. | UI-5 | |
| B5 | `2` durch `10` ersetzen, `Strg+Enter` | Zeile 2 M2, Änderungen „Mittelung Anzahl 10“. | UI-5, R-011 | |
| B6 | `+ Messung` → `M3`, `.set`, „eigenes Limit“ anhaken, 120 → `Übernehmen` | Zeile 3 M3, Limit „120 s“. | R-012 | |
| B7 | `+ Messung` → `M4` eintippen, dann `Esc` | Nichts eingefügt, Fokus zurück in der Tabelle. | UI-2 | |
| B8 | Zeile M1 wählen, `Strg+Umschalt+N`, Text „Sensorkopf umsetzen“, `Übernehmen` | Zwischen M1 und M2 eine Zeile „⏸ Pausenpunkt“, Nr „–“, „Pausenpunkt: Sensorkopf umsetzen“ über die Breite. | UI-6, R-017 | |
| B9 | M3 wählen, `▲` zweimal | M3 steht vor M2, dann vor dem Pausenpunkt. Nr wird neu gezählt. | UI-3, R-015 | |
| B10 | M3 wählen, `Alt+↓` (Fokus in der Tabelle) | M3 eine Zeile tiefer. | UI-3, UI-21 | |
| B11 | M2 wählen, Name im Editor zu `M2b` ändern, `Übernehmen` | Tabellenzeile zeigt M2b. | UI-4, R-014 | |
| B12 | Messung `M5` anlegen, wählen, `Entf` | M5 ist entfernt (ohne Rückfrage). | UI-3, R-013 | |
| B13 | M1 wählen, Namen im Editor ändern (nicht übernehmen), dann andere Zeile anklicken | Rückfrage „Änderungen verwerfen?“, Standard „Zurück zum Editor“: Auswahl springt zurück, Eingabe bleibt. Mit „Verwerfen“ wird die andere Zeile geladen. | K-U4 | |

## C Durchgang (R-010, R-016 bis R-018, R-031)

| Nr | Schritt | Erwartet | Bezug | Ergebnis |
|---|---|---|---|---|
| C1 | `Start` (oder `F5`) | Kein Dialog (Simulator). Statuszeile „Läuft · Messung 01 von 03“; Nr der laufenden Zeile „01“ (Dateinummer, nicht mehr vorläufig); erste Zeile „▶ läuft“ mit farbigem Balken links; Fortschritt „ca. … % (geschätzt) · noch ca. … · Zeitlimit in …“. | UI-8, UI-15, R-010, R-031 | |
| C2 | Während M1 läuft: M2b wählen, Name zu `M2c` ändern und übernehmen; eine neue Messung `M6` ans Ende anlegen | Beides klappt im Lauf; laufende Zeile ist im Editor nur anzeigbar („Dieser Eintrag ist nicht mehr änderbar.“). | UI-4, R-016 | |
| C3 | Laufende Zeile wählen | Editor „Messung 1 (läuft)“, alle Felder grau. `Entfernen`, `▲`, `▼` grau mit Tooltip „Eintrag läuft bereits.“ | UI-3, UI-4 | |
| C4 | Warten bis Pausenpunkt | Band gelb mit Rand: „⏸ Pausenpunkt erreicht: Sensorkopf umsetzen. …“, Knopf `Bestätigen (F7)`; Zeile „⏸ wartet auf Bestätigung“; Fokus bleibt, wo er war. | UI-11, R-017 | |
| C5 | Einige Sekunden warten, dann `F7` | Vorher startet keine Messung; nach F7 läuft die nächste. | UI-11, R-017 | |
| C6 | Während einer Messung `Pausieren (F6)` | Knopf zeigt „Pause angefordert“ (grau), Band „⏸ Pause angefordert. Messung … läuft zu Ende …“. Nach Ende der Messung: „Pausiert“, Band mit `Fortsetzen (F6)`; keine neue Messung startet. | UI-13, R-018 | |
| C7 | `Fortsetzen (F6)` | Durchgang läuft weiter. | UI-13, R-018 | |
| C8 | Während einer Messung `Abbrechen …` | Dialog „Durchgang abbrechen?“, Standardknopf „Weiter messen“. `Esc` → nichts passiert. | UI-10 | |
| C9 | Erneut `F8` → `Durchgang abbrechen` | „Abbruch läuft …“, danach Band „■ Durchgang abgebrochen: … nicht gestartet (bleiben wartend).“; laufende Zeile „■ abgebrochen“, nicht gestartete bleiben „○ wartend“. | UI-10, UI-18, R-018 | |
| C10 | Band `Ordner öffnen` | Dateimanager öffnet den Durchgangsordner (Platzhalter-`.svd`, Protokolle, `durchgang.ereignisse.jsonl`). | UI-18 | |
| C11 | Band `Schließen`, dann `Start` | Neuer Durchgang nur mit den wartenden Einträgen; am Ende „✔ Durchgang beendet: … fertig.“ | UI-18, R-010 | |
| C12 | Ereignisprotokoll unten ansehen | Zeilen „HH:MM:SS  Text“, Fehler mit „Fehler:“, Warnungen mit „Warnung:“. | Zone G | |
| C13 | Fenster während eines laufenden Durchgangs schließen | Hinweis „Es läuft ein Durchgang. Bitte zuerst abbrechen oder warten.“; Fenster bleibt offen. | UI-26 | |

## D Betriebsarten (U4-3)

| Nr | Schritt | Erwartet | Bezug | Ergebnis |
|---|---|---|---|---|
| D1 | Betriebsart-Knopf → `NUR LESEN` | Ohne Dialog; Anzeige `NUR LESEN`; `Start` grau „… NUR LESEN führt keine Einträge aus.“ | UI-14 | |
| D2 | Betriebsart → `TROCKENLAUF`; `Verbinden` (außerhalb von SIMULATOR nötig, im Simulatorbetrieb wieder gegen den Simulator); `Start` | Hinweisdialog „Ein Trockenlauf ändert die aktuellen PSV-Einstellungen. Es wird nicht gescannt.“, Standard `Abbrechen`. Mit `Trockenlauf starten`: Messungen „✔ fertig (Trockenlauf)“. | UI-15 | |
| D3 | Betriebsart → `MESSEN` | Dialog „Messen freischalten“ mit fünf Zeilen ✔/✖; bei offenen Punkten ist `Freischalten` grau und unter der Zeile steht die Abhilfe. `Abbrechen` → Betriebsart bleibt. | UI-14 | |
| D4 | Nach D2 stehen alle Messungen auf „✔ fertig (Trockenlauf)“; Band (nach `Schließen` bzw. in Bereit) zeigt „Einträge sind bereits ausgeführt … auf wartend zurücksetzen.“ mit Knopf `Zurücksetzen` → klicken | Keine Rückfrage (nur Trockenlauf-Ergebnisse); alle Zeilen „○ wartend“, `Start` aktiv, Protokoll „Warteschlange zurückgesetzt: n Einträge wartend.“ Danach Betriebsart → `MESSEN`; falls alle Voraussetzungen erfüllt: `Freischalten`, danach `Verbinden`. Statuszeile invertiert (weiß mit schwarzem Text) `MESSEN`, Titel „… – MESSEN“. | UI-29, UI-14 | |
| D4b | Nach einem echten (Simulator-)Durchgang `Zurücksetzen` im Band | Rückfrage „Warteschlange zurücksetzen?“ („n Einträge wurden bereits gemessen …“), Standard `Abbrechen`; `Esc` ändert nichts. | UI-30 | |
| D5 | In `MESSEN`: `Start` | Dialog „Durchgang starten: echte Messung“ mit Messungsliste, Generator-Warnung in Rot, Eingabefeld. `Messung starten` erst aktiv bei exakt `MESSEN`; `messen` reicht nicht. `Abbrechen` → kein Start. | UI-15 | |
| D6 | Während eines Durchgangs Betriebsart-Knopf ansehen | Grau, Tooltip „Während eines Durchgangs nicht änderbar“. | UI-14 | |

## E Speichern und Laden (R-021)

| Nr | Schritt | Erwartet | Bezug | Ergebnis |
|---|---|---|---|---|
| E1 | `Speichern …` (`Strg+S`) als `serie` | Datei `serie.warteschlange.json`; Protokoll „Warteschlange gespeichert: …“. | UI-20, R-021 | |
| E2 | Ein paar Einträge ändern oder entfernen, dann `Laden …` (`Strg+O`) | Rückfrage „Die aktuelle Warteschlange (n Einträge) wird ersetzt. Fortfahren?“, Standard `Abbrechen`. Mit `Ersetzen`: gleiche Einträge in gleicher Reihenfolge, alle „○ wartend“. | UI-20, R-021 | |
| E3 | `basis.set` umbenennen, Datei erneut laden | Laden gelingt; Zeilen mit „⚠ basis.set“, Tooltip „Einstellungsdatei nicht gefunden“; Protokoll „Warnung: n Einstellungsdateien nicht gefunden“. | UI-20 | |
| E4 | In der `.json` einen Schlüssel umbenennen, laden | Fehlerdialog „Datei kann nicht geladen werden“ mit Pfadangabe; Warteschlange unverändert. | UI-20 | |
| E5 | Fenster mit ungespeicherten Änderungen schließen | Frage `Speichern` / `Verwerfen` / `Abbrechen`, Standard `Abbrechen`. | UI-26 | |

## F Tastatur und Darstellung

| Nr | Schritt | Erwartet | Bezug | Ergebnis |
|---|---|---|---|---|
| F1 | Nur mit Tastatur: `Tab` durch das Fenster | Reihenfolge Statuszeile → Werkzeugleiste → Hinweisband-Knöpfe → Tabelle → Editor → Protokoll; jedes Element zeigt einen 2-px-Rahmen in Petrol. | UI-21 | |
| F2 | In der Tabelle `↑`/`↓`/`Pos1`/`Ende`, `Enter`, im Editor `Strg+Enter`, `Esc` | Auswahl wandert; Enter springt in den Editor; Strg+Enter übernimmt; Esc verwirft und springt zurück. | UI-21 | |
| F3 | Fenster auf 1100 × 680 verkleinern | Kein Knopf abgeschnitten; Texte der Statuszeile mit „…“ gekürzt, Volltext im Tooltip. | UI-24 | |
| F4 | Symbole ○ ▶ ✔ ✖ ■ ⏸ ⚠ prüfen | Alle Zeichen sichtbar (am Messrechner T0 erneut prüfen; sonst Rückfall `ASCII_RUECKFALL` in `gui/tokens.py`). | Brief 2 | |

## G Wächter (U4-4)

Der hängende Aufruf lässt sich in der Oberfläche nicht auslösen (nur per Drehbuch des Simulators). Nachweis über den automatisierten Test `test_ui_16_waechter_und_bedienbarkeit_mit_haengendem_simulator` (Marker `gui`). Optional am Messrechner (T1/T2): Erscheint ein PSV-Dialog, muss das Band „⚠ PSV reagiert nicht seit N s …“ mit laufender Zahl zeigen, und die Oberfläche bleibt bedienbar.

## Nicht im Umfang

Drag-and-drop (UI-27, Kann) ist nicht umgesetzt. Zurücksetzen hat bewusst kein Tastenkürzel. Standard-Zeitlimit ist in der Oberfläche nicht einstellbar (Sitzung bietet keinen Befehl). Zieldateinamen, Messpunkte und Generatorzustand liefert die Sitzung noch nicht; die Dialoge zeigen „unbekannt“.

## Ergebnis

Bestanden: ☐ ja ☐ nein · Abweichungen: ____________________ · Unterschrift/Datum: ________
