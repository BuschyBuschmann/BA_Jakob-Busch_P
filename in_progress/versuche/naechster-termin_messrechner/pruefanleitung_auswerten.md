# Prüfanleitung Auswertungsoberfläche am Messrechner (Version 0.2.0, neuer Build)

Stand: 2026-11-05, Paket U-AUSW-T5. Voraussetzung: Installation nach `installation_0.2.0.md`
(N1 bis N7 durchlaufen). Grundlage: Plan P-AUSW (T5), Brief K-AUSW (UI-15, UI-23, UI-25),
ADR-022/023.

**Kein Punkt gilt als bestanden, bevor Jakob ihn bestätigt hat.** Die Spalte „Erwartet“ nennt
den Sollwert aus der Planung; Zeiten sind auf einem Linux-Container gemessen und am
Messrechner **zu belegen oder zu widerlegen**. Alles in `$PY`-Syntax wie im Ablaufplan.
Beispieldatei: Kopie von `20261012_ref_Mitte.svd`; es wird nur gelesen. Eine Abweichung ist
ein Befund, kein Fehler der Anleitung: Zahl notieren, weitermachen.

| Nr | Prüfung | Erwartet | Ergebnis / Beobachtung | Jakob bestätigt |
|---|---|---|---|---|
| W1 | Messskript aus dem Ordner mit dem Skript: `& $PY tools\auswertung\zeiten_messen.py "<Kopie.svd>" --wiederholungen 3 --json "$ARB\zeiten.json"` | Läuft ohne Fehler durch; JSON geschrieben | | |
| W1a | Spawn (`spawn_leer`) | Container: ca. 80 ms (Quelle: `in_progress/planung/plaene/2026-11-03_P-AUSW_umsetzungsplan.md`, Spawn-Messung); Planungsrichtwert, nicht am Messrechner gemessen; am Messrechner nur notieren [offen: Sollwert] | | |
| W1b | Lesen (`lesen`, `lese_job`) | Container: 0,1 bis 0,8 s (Quelle: ADR-022, Messung im Linux-Container); Planungsrichtwert, nicht am Messrechner gemessen; nur notieren | | |
| W1c | Abbruch (`abbrechen`) | Läuft durch, Prozess endet, kein hängender Prozess im Task-Manager | | |
| W1d | Längste Einzelabfrage `fertig()` bei `lese_job` | **< 200 ms** (UI-15) | | |
| W1e | Paarrechnung kalt und warm (`paar_kalt`, `paar_warm`) | Paar **< 400 ms** (Ziel nach Plan); Container ca. 250 ms (Quelle: `in_progress/planung/plaene/2026-11-03_P-AUSW_umsetzungsplan.md`, Abschnitt Ansichten 2–4); Planungsrichtwert, nicht am Messrechner gemessen. Das Laborbuch `2026-11-05_auswerten-t3b-ansichten.md` nennt 0,49 s beim ersten Paar (Ort der Messung dort nicht angegeben) | | |
| W1f | `import_matplotlib`, erster und zweiter Lauf | Erster Lauf baut den Schriftcache (länger), zweiter deutlich kürzer; beide Werte notieren | | |
| W2 | Reaktionszeit beim Laden: Datei im Reiter „Auswerten“ öffnen, währenddessen Reiter „Messen“ anklicken (Alt+1) und zurück (Alt+2) | Oberfläche bleibt bedienbar, Reiterwechsel sofort (< 200 ms gefühlt), „Prüfung: wird berechnet …“ danach Ergebnis | | |
| W3 | HiDPI: Windows-Skalierung 125 % und 150 % (Anzeige-Einstellungen, danach neu anmelden bzw. Programm neu starten) | Texte unverschnitten, Plot und Fußzeile scharf, nichts überlappt; je Skalierung ein Eintrag | | |
| W4 | Schriften und Glyphen: ⚠ (Warnung), Hochzahlen (z. B. 10⁻⁵ in der Cursorzeile), Consolas in Pfaden und Prüftext | Alle Zeichen sichtbar (kein Kästchen), Consolas statt Rückfall; falls Rückfall (Courier New) notieren | | |
| W5 | Fußzeile bei 1100×680 (kleinste Fenstergröße): lange Cursorzeile mit vier Kurven; Export mit langem Pfad; Prüfung mit Warnungen | Prüftext und Meldezeile beide sichtbar, Warnzahl nie gekürzt, Pfad mittig gekürzt, Volltext im Tooltip | | |
| W6 | Blitting-Cursor: Maus über den Plot ziehen (Ansicht 1 und 3), mit 1 und 4 Kurven | Fadenkreuz folgt der Maus ohne Ruckeln und Nachziehen, Cursorzeile aktualisiert sich mit | | |
| W7 | Export im Prozess: „Export“ (Strg+E) in einen Ordner unter `$ARB\daten\`, dabei Oberfläche bedienen | Fortschritt sichtbar, Oberfläche bleibt bedienbar, Dateien `.npz` und `.json` entstehen, Meldung nennt beide Namen | | |
| W7a | Export abbrechen: Fenster während des Exports schließen | Rückfrage „Export läuft – abbrechen und schließen?“ erscheint. Bei „Ja, abbrechen und schließen“ wird der Exportprozess hart beendet; dabei können `.<Name>.npz.tmp` bzw. `.<Name>.json.tmp` im Zielordner zurückbleiben. Der nächste Export zum selben Namen entfernt diese Reste und nennt sie in der Meldung. Eine einzelne `.npz` ohne `.json` wird nur gemeldet, nicht gelöscht; der Export startet dann nicht. Bei „Nein, offen lassen“ rechnet der Export weiter | | |
| W8 | „Bild speichern“ (Strg+Umschalt+S), PNG und PDF | Datei entsteht, Stempel „Arbeitsansicht – nicht für die Thesis“ mit Datei, Ansicht und Git-Hash; Datei lässt sich öffnen | | |
| W9 | Drag-and-drop einer `.svd` aus dem Explorer auf das Fenster | `.svd` wird geladen und im Reiter „Auswerten“ geöffnet (bei mehreren Dateien zählt die erste `.svd`). Andere Dateitypen werden abgewiesen: das Ablegen ist nicht möglich, es erscheint kein Hinweis (so vorgesehen; Befund notieren, falls doch eine Meldung kommt) | | |
| W10 | Lage der INI: `Get-ChildItem "$env:LOCALAPPDATA" -Recurse -Filter auswerten.ini` nach dem ersten Schließen | Datei `auswerten.ini` im Konfigurationsordner der Anwendung (Ort: `QStandardPaths.AppConfigLocation`, Windows laut Code `%LOCALAPPDATA%`-Unterordner, **[Annahme]** Ordnername nicht geprüft); gemerkter Ordner und „Zuletzt geöffnet“ beim nächsten Start vorhanden | | |

## Hinweise zur Auswertung

- Befunde mit Nummer, Zahl und ggf. Foto in `protokoll.md` eintragen; Nachweise gehen über
  `/laborbuch` in die Nachverfolgung ein.
- Wird W1d (200 ms) oder W1e (400 ms) überschritten: Messwerte (`zeiten.json`) sichern. Der Plan
  sieht dafür Gegenmaßnahmen vor (Rechnung in den Worker verlagern), das entscheidet nicht der
  Test.
- W3 bis W10 sind reine Handtests; es gibt keine automatische Gegenprobe außerhalb von Windows.
