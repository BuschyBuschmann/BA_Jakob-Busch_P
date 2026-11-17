# Prüfanleitung Auswerten: Achsenleiste, Vergleich und eigenes Diagramm am Messrechner (UI-38)

Stand: 2026-11-14, Paket U-AUSW2-C. Grundlage: Plan `in_progress/planung/plaene/2026-11-09_P-AUSW2_umsetzungsplan.md`
(S3, S7, S9, S10, Abschnitt 12 Risiken), Brief `2026-11-09_K1-AUSW2_design-brief.md` (UI-4, UI-9 bis UI-21,
UI-34 bis UI-38), ADR-028, KONVENTIONEN (kompakte Anzeige unter 1200 px, Zahlenfelder). Ergänzt
`pruefanleitung_auswerten.md` (W1 bis W10); Voraussetzung ist dieselbe Installation (`installation_0.2.0.md`,
bei neuem Build mit dem Wheel dieses Stands).

**Kein Punkt gilt als bestanden, bevor Jakob ihn bestätigt hat** (danach `/laborbuch`; erst dann
setzt sich der Stand „am Gerät bestätigt“, UI-38). Die Spalte „Erwartet“ nennt den Sollwert aus der
Planung oder dem Test; Zeiten und Speicherzahlen stammen aus einem **Linux-Container** (4 Kerne, 16 GB,
offscreen) und sind am Messrechner **zu belegen oder zu widerlegen**. Eine Abweichung ist ein Befund,
kein Fehler der Anleitung: Zahl notieren, weitermachen, nichts vor Ort ändern.

**Nicht Teil dieser Anleitung:** Phasenregler und Animation (Ansicht 4, R-071) gehören zu UI-38, sind
aber noch nicht gebaut; ihre Prüfpunkte kommen mit dem Animationspaket dazu. UI-38 bleibt deshalb auch
nach diesem Dokument **offen**.

## Sicherheitsrahmen

- Reine Auswertung: Es wird **nichts gemessen**, kein PSV gestartet, keine COM-Verbindung genutzt und
  nichts an Messdateien geändert (die Software liest `.svd` nur).
- Es wird nur in den Ausgabeordner `$ARB` geschrieben (Bilder, `speicher.json`), nie in den Ordner der
  Messdaten. Als Messdatei dient eine **Kopie** der Beispieldatei `20261012_ref_Mitte.svd`; für
  den Vergleich eine zweite Datei (am besten eine andere echte Messung, sonst dieselbe Kopie unter
  anderem Namen, dann sind beide Messungen inhaltlich gleich und der Vergleich zeigt zwei deckungsgleiche
  Linien).
- Alles in `$PY`-Syntax wie im Ablaufplan. Fenstergröße und Windows-Skalierung vorher notieren.

## A Speicher und Messungsgrenze (R-058, Annahme zu OF-5)

| Nr | Prüfung | Erwartet | Ergebnis / Beobachtung | Jakob bestätigt |
|---|---|---|---|---|
| V1 | Freien Arbeitsspeicher notieren (Task-Manager, Leistung) und `& $PY tools\auswertung\speicher_messen.py "<Kopie1.svd>" "<Kopie2.svd>" --wiederholen 2 --json "$ARB\speicher.json"` (vier Öffnungen) | Läuft ohne Fehler; Tabelle mit Zuwachs je Messung, Summe darunter. Planungsrichtwert (Container, Beispieldatei, zwei Kanalpaare): rund 115 MiB je Messung, also rund 460 MiB bei vier Messungen; am Messrechner nur zu lesen, **[offen: Sollwert]** | | |
| V2 | Zahl aus V1 gegen den freien Speicher aus V1 legen | Summe der vier Messungen passt mit deutlichem Abstand in den freien Speicher (der Abstand ist dein Urteil, es gibt keinen Sollwert). Sonst Befund „Grenze 4 zu hoch“: Zahlen sichern, `MESSUNGEN_MAX` nicht vor Ort ändern | | |
| V3 | Im Reiter „Auswerten“ vier Messungen öffnen (`Messung hinzufügen …`, Datei 2 bis 4), danach Speicher im Task-Manager (Python-Prozess) ablesen | Wert in der Größenordnung von V1; die Oberfläche bleibt beim Laden bedienbar (Reiter „Messen“ per Alt+1 anklicken: Wechsel sofort) | | |
| V4 | Fünfte Messung versuchen | `Messung hinzufügen …` ist gesperrt, Tooltip nennt den Grund | | |

## B Achsenleiste (R-073) und Bedienung über Remotedesktop

Fenster auf die Größe bringen, in der später gearbeitet wird (Remotedesktop-Fenster, nicht nur die
physische Anzeige). Die Zeiten sind **Eindruck beim Bedienen**, kein Stoppuhrwert, außer die Spalte nennt
einen.

| Nr | Prüfung | Erwartet | Ergebnis / Beobachtung | Jakob bestätigt |
|---|---|---|---|---|
| B1 | Ansicht 1, Frequenz „von“ `5` tippen, **ohne** Enter, mehrere Ziffern nacheinander | Der Plot bleibt unverändert, während getippt wird (UI-37); erst Enter oder Wechsel in ein anderes Feld zeichnet neu | | |
| B2 | Dasselbe mit Enter: Neuzeichnen beobachten, ggf. mit Stoppuhr (Enter bis fertiges Bild) | Genau ein Neuzeichnen. **[offen: Sollwert]**; am Messrechner notieren (Vergleich: Paarrechnung Ziel unter 400 ms, W1e). Ein deutlich verzögertes Bild über Remotedesktop ist ein Befund | | |
| B3 | Zoom mit der Werkzeugleiste, danach ein Wert in „von“ ändern | Felder zeigen nach dem Zoom die sichtbaren Grenzen als feste Werte (hervorgehoben, „fest“ nicht nur an der Farbe erkennbar); Eingabe setzt den Bereich | | |
| B4 | `Alles auf Auto` | Felder grau mit Auto-Wert, Plot im Auto-Bereich | | |
| B5 | Ungültig: von größer als bis; bei logarithmisch 0; Text `abc` | Meldung am Feld (Symbol ✖ plus Wort), Plot bleibt unverändert, lesbar bei Remotedesktop | | |
| B6 | Wechsel Punkt, Komponente, Größe, aktive Messung in Ansicht 1 | Grenzen und Skalierung der Achsenleiste bleiben (UI-3) | | |
| B7 | Fenster auf 1100×680 verkleinern (Ansicht 1, 2, 3, 5) | Nichts überlappt oder ist abgeschnitten; unter 1200 px Breite steht kompakte Anzeige (Dateiname neben den Chips weg, kurze Achsenbeschriftungen); Achsenleiste in einer Zeile oder sauber umgebrochen | | |
| B8 | Dezimalkomma und Potenzschreibweise: `1,4·10⁻⁷` und `8,5e-4` in ein Betragsfeld | Beide werden gelesen, das Feld zeigt danach `8,5·10⁻⁴`; Hochzahlen sind lesbar (kein Kästchen) | | |
| B9 | Ansicht 5 mit vier Serien: Fenster zweimal zwischen 1100×680 und 1366×768 wechseln, danach auf 1100×680 stehen lassen | Die Auswahlspalte zeigt keinen überflüssigen Bildlauf: Bei 1100×680 und 1366×768 passt der Inhalt ohne Bildlaufleiste. Offscreen geprüft (Test `test_ui36_ansicht_5_vier_serien_kein_bildlauf_nach_groessenwechseln`); der frühere 12-px-Bildlauf ist behoben (Ursache: alte Höhe der Anordnungsknöpfe blieb nach dem Umschalten im Layout stehen). Am Messrechner bestätigen; erscheint doch eine Bildlaufleiste, fotografieren und notieren | | |

## C Mehrere Messungen und Ansicht 5 „Diagramm“ (R-058, R-059)

Zwei bis vier Messungen offen. Strg+5 wechselt zu Ansicht 5.

| Nr | Prüfung | Erwartet | Ergebnis / Beobachtung | Jakob bestätigt |
|---|---|---|---|---|
| C1 | Chips der Messungsleiste: Wechsel per Klick und Pfeiltasten, `×` am Chip, Entf mit Rückfrage, wenn Serien betroffen | Aktiver Chip ist an Rahmen, Symbol und Wort erkennbar (nicht nur Farbe); Rückfrage erscheint nur, wenn Serien der Messung betroffen sind (UI-14); `×` ist groß genug und sichtbar | | |
| C2 | Ansicht 5: `+ Serie`, danach `Bearbeiten` (auch per Doppelklick), Esc im Dialog | Dialog mit Vorbelegung der gewählten Serie; Esc schließt ohne Änderung; Linienart und Farbe der Serie bleiben nach dem Bearbeiten gleich | | |
| C3 | `Aus aktueller Ansicht übernehmen`: erst in Ansicht 1 zwei Komponenten wählen, in Ansicht 5 Knopf drücken; danach Ansicht 2 mit |H1| und noch einmal drücken | Ansicht 1 liefert je Komponente eine Serie, Größe und Teilgröße des Diagramms werden bei leerer Liste gesetzt; bei nicht passender Größe keine Änderung, Hinweis „… nicht übernommen“ in AD | | |
| C4 | Vier Serien anlegen, danach `+ Serie` und `Aus aktueller Ansicht übernehmen` prüfen | Beide gesperrt, Tooltip „Höchstens vier Serien; mehr Serien über „nebeneinander“.“ (UI-18); Linienarten der vier Serien lassen sich auch ohne Farbe unterscheiden | | |
| C5 | Anordnung „überlagert“ und „nebeneinander“ mit zwei Messungen und vier Serien umschalten | Zwei Teilbilder mit gekoppelter Frequenzachse bzw. eine Achse; Legende nennt Kurzname, Punkt oder Mittel, Komponente; Wechsel zeichnet ohne spürbares Warten (**[offen: Sollwert]**, Eindruck notieren) | | |
| C6 | Sichtbar-Häkchen einer Serie ausschalten und einschalten | Linie verschwindet und kommt wieder; Zoom und Achsenwerte ändern sich nicht (UI-21) | | |
| C7 | Größe „Phase“ wählen, eine Serie mit Punkt (nicht Mittel) | Phase in Grad, Kennzeichen „⚠ unbestätigt (M8)“ im Bild; bei Mittel erscheint eine Meldung in AF („Phase beim Mittel nicht darstellbar“), keine Linie | | |
| C8 | Datei ohne Referenz laden (falls vorhanden; sonst entfällt) | Größen |H1|, |H2|, Kohärenz, Phase gesperrt mit Begründung neben dem Knopf (UI-17) | | |
| C9 | Auswahlspalte bei 1100×680 mit vier Serien | Die Knopfzeilen und die Serienliste sind sichtbar, ohne dass eine Zeile abgeschnitten ist; die Spalte scrollt höchstens senkrecht | | |

## D Bild speichern in Ansicht 5 (UI-19)

| Nr | Prüfung | Erwartet | Ergebnis / Beobachtung | Jakob bestätigt |
|---|---|---|---|---|
| D1 | `Bild speichern …` (Strg+Umschalt+S) als PNG mit zwei Messungen und zwei Serien | Dateiname-Vorschlag `<Basisname der ersten Serie>_ansicht5.png`; Datei entsteht und lässt sich öffnen; Stempel im Bild: erste Zeile „Arbeitsansicht – nicht für die Thesis · Ansicht 5 Diagramm · <Git-Hash>“, darunter je beteiligter Datei eine Zeile `<Kurzname>: <Dateiname>`; Legende steht im Bild | | |
| D2 | Dasselbe als PDF | Datei beginnt mit `%PDF`, öffnet im PDF-Betrachter, Text im Stempel lesbar | | |
| D3 | Eine Serie ausblenden, erneut speichern | Die Datei der ausgeblendeten Serie steht **nicht** im Stempel | | |
| D4 | Phase-Serie mit Punkt speichern | Zusätzliche Zeile „⚠ enthält unbestätigte Größen (M8)“; ohne Phase fehlt sie | | |
| D5 | Git-Hash im Stempel gegen `_build_info.json` des Wheels (vgl. I6 im Protokoll) | Gleiche ersten 12 Zeichen; bei geändertem Arbeitsbaum steht „(Arbeitsbaum geändert)“ | | |
| D6 | Nur nicht darstellbare oder ausgeblendete Serien | `Bild speichern …` gesperrt, Tooltip nennt den Grund | | |

## E Tastatur und Lesbarkeit (UI-34, UI-35, UI-36)

| Nr | Prüfung | Erwartet | Ergebnis / Beobachtung | Jakob bestätigt |
|---|---|---|---|---|
| E1 | Mit Tab durch Ansicht 5 gehen: Dateileiste und Chips, Ansichtsknöpfe, Auswahlspalte (Größe, Anordnung, Serienknöpfe, Liste), Achsenleiste, Plot und Werkzeugleiste, Prüftext | Reihenfolge wie genannt; **kein** bedienbares Element wird übersprungen; der Fokus ist an jeder Stelle sichtbar (Rahmen), auch im Plot | | |
| E2 | Lesbarkeit über Remotedesktop: aktiver Chip, gesperrte Größe mit Begründung, gesperrte Knöpfe „+ Serie“ und „Aus aktueller Ansicht übernehmen“ bei vier Serien (der Grund steht nur im Tooltip), Meldung am Zahlenfeld | Text jeweils ohne Mühe lesbar (Kontrast), auch bei 125 % und 150 % Windows-Skalierung | | |
| E3 | Fenster 1366×768: Größe des Plotbereichs schätzen oder mit Bildschirmlineal messen; Auswahlspalte in Ansicht 5 mit vier Serien ansehen | Plotbereich mindestens 600×320 Pixel (UI-36); Tabellen in Ansicht 3 geben vor dem Plot nach; die Auswahlspalte hat keine Bildlaufleiste | | |
| E4 | Graustufen: Bildschirm in Graustufen schalten (Windows: Farbfilter) oder ein gespeichertes PNG in Graustufen ansehen | Vier Serien sind allein über Linienart und Legende zu unterscheiden (UI-20) | | |

## Hinweise zur Auswertung

- Befunde mit Nummer, Zahl und ggf. Foto in `protokoll.md` eintragen; Nachweise gehen über
  `/laborbuch` in die Nachverfolgung ein. Der Stand „am Gerät bestätigt“ gilt erst nach Jakobs
  Bestätigung der jeweiligen Zeile.
- Wird V2 verfehlt (Speicher knapp) oder B2 deutlich verzögert: `speicher.json` und die Zeitangabe sichern. Die
  Gegenmaßnahmen stehen im Plan (Abschnitt 12, Risiken: kleinere Messungsgrenze, Auflösung nur der
  gezeigten Serien); die Entscheidung trifft nicht der Test.
- Was nicht geprüft werden konnte (z. B. keine zweite Datei, keine Datei ohne Referenz), mit Grund
  als „entfällt“ eintragen.
- Alle Zahlen im Abschnitt „Erwartet“ mit „Container“ oder „Annahme“ sind Planungswerte, keine
  Messwerte vom Messrechner.
