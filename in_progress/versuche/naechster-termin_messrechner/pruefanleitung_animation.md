# Prüfanleitung Animation der Betriebsschwingform am Messrechner (R-071, UI-38)

Stand: 2026-11-19, Paket U-AUSW3-89 (AN8, AN9). Grundlage: Plan
`in_progress/planung/plaene/2026-11-11_P-AUSW3_animation-plan.md` (Abschnitte 5, 6, 8), Brief
`2026-11-09_K1-AUSW2_design-brief.md` (UI-22 bis UI-38), ADR-029, KONVENTIONEN. Ergänzt
`pruefanleitung_auswerten.md` (W1 bis W10) und `pruefanleitung_auswerten_vergleich.md` (AV).

**Kein Punkt gilt als bestanden, bevor Jakob ihn bestätigt hat** (danach `/laborbuch`; erst dann setzt
sich der Stand „am Gerät bestätigt“). **UI-38 (Bedienung der Animation über Remotedesktop flüssig und
lesbar) ist offen, bis Jakob sie ausdrücklich bestätigt**; die Zahlen aus dem Messskript sind
Messwerte, **keine Bestanden-Aussage**. Die Spalte „Erwartet“ nennt den Sollwert aus Plan und Tests;
Zeiten stammen aus einem **Linux-Container** (4 Kerne, Qt `offscreen`, ohne Fenster und ohne
Remotedesktop) und sind am Messrechner **zu belegen oder zu widerlegen**. Eine Abweichung ist ein
Befund, kein Fehler der Anleitung: Zahl notieren, weitermachen, nichts vor Ort ändern.

## Voraussetzungen

- Installation nach `installation_0.2.0.md` mit dem Build cebac63 (enthält AN8 und AN9; Version bleibt
  0.2.0). Erkennbar: In der Animationsleiste unter dem Bild steht der Knopf „Werte als Tabelle“
  (unter 1200 px Fensterbreite „Tabelle“).
- Eine **Kopie** von `20261012_ref_Mitte.svd` (3D-Messung mit Referenz, 135 Punkte); es wird nur gelesen.
  Nie das Original, nie im PSV-Ordner.
- Für Block B: `animation_messen.py` **und** `speicher_messen.py` (es importiert daraus die
  Speicherabfrage) im selben Ordner `$ARB\tools\auswertung\` (Kopie vom Stick,
  `stick/tools/auswertung/`; beide Skripte liegen im Stand dieses Builds auf dem Stick, SHA-256 in `stick/LIESMICH.txt`). Das Messskript gehört **nicht** ins Wheel.
- Alles in `$PY`-Syntax wie im Ablaufplan. Fenstergröße und Windows-Skalierung vorher notieren.

## Sicherheitsrahmen

- Reine Auswertung: Es wird **nichts gemessen**, kein PSV gestartet, keine COM-Verbindung genutzt und
  nichts an Messdateien geändert.
- Geschrieben wird nur nach `$ARB` (Standbilder, Messtabellen). Das Messskript legt ein Fenster
  (1000 × 600 px) an und zeichnet darin selbst: **Maus und Tastatur während des Laufs nicht benutzen**
  und das Fenster nicht verdecken oder minimieren, sonst sind die Zeiten verfälscht.

## A Sichtprüfung am Messrechner (lokal, danach in der Remotedesktop-Sitzung wiederholen)

Datei im Reiter „Auswerten“ öffnen, Ansicht 4 (Strg+4). Je Punkt Ergebnis und, wo gefragt, Zahl notieren.
Jeder Punkt gilt zunächst lokal; die Remotedesktop-Wiederholung steht in M7 (Block B).

| Nr | Prüfung | Erwartet | Ergebnis / Beobachtung | Jakob bestätigt |
|---|---|---|---|---|
| AN-1 | Datei öffnen, Ansicht 4 | Modus „Standbild“ gewählt, nichts läuft; Frequenz wechseln: der Modus springt (falls „Animation“ gewählt war) zurück auf „Standbild“ (UI-22) | | |
| AN-2 | Modus „Animation“ wählen | 3D-Bild der Messpunkte; Wiedergabe pausiert, θ = 0,0°; im Bild und im Kopf: Überhöhung ×…, größte reale Spitzenauslenkung D_ref, Frequenz, θ und Bezug, Kennzeichen „Komponenten im Geometrie-KS unbestätigt (M12)“ bei 3D (UI-26, UI-28) | | |
| AN-3 | „Abspielen“ (Knopf und Leertaste), „Pause“, Tempo-Regler | Punkte schwingen; Pause hält an; Tempo ändert die Geschwindigkeit; startet nie von selbst (UI-22, UI-24) | | |
| AN-4 | Phase: ← und → (Fokus im Bild oder im Phasenregler), Phasenregler ziehen, Schrittweite 10° | θ in Grad mit Dezimalkomma; je Tastendruck ±10,0°; ohne Wiedergabe bedienbar (UI-24, UI-32) | | |
| AN-5 | Drehen: linke Maustaste ziehen; Mausrad; Doppelklick; Pos1; Knöpfe xy, xz, yz, Iso; ↑ ↓; Umschalt+← →; + − | Bild dreht und zoomt; Doppelklick und Pos1 setzen Blick und Zoom zurück (nicht θ und Überhöhung); Wiedergabe pausiert beim Ziehen (UI-23). **Notieren:** Rad zu träge oder zu sprunghaft (HiDPI, Touchpad) | | |
| AN-6 | Überhöhung (Regler und Feld), Farbbereich „von“/„bis“ (Zahl tippen) | Bild folgt; ein Farbbereich wirkt erst bei Enter oder Fokuswechsel, nicht beim Tippen (UI-26, UI-27, UI-37) | | |
| AN-7 | Phasenbezug „Absolut“ | Kopf zeigt dauerhaft „⚠ Phase unbestätigt (M8)“ (kurz „⚠ M8“ unter 1200 px, Langtext im Tooltip) (UI-28) | | |
| AN-8 | Komponente, Bezug, Größe, Farbe wechseln | Blick und θ bleiben erhalten; Frequenzwechsel setzt zurück ins Standbild | | |
| AN-9 | Tab-Reihenfolge und Fokus (Tab, Umschalt+Tab) | Reihenfolge AD → Bild → Leiste → Meldezeile; Fokus überall sichtbar, auch im 3D-Bild (UI-34) | | |
| AN-10 | **Bild speichern …** (Strg+Umschalt+S) im Modus Animation bei θ = 90,0° und gewähltem Blick, als PNG und als PDF; einmal während die Wiedergabe läuft | Dateivorschlag `…_ansicht4_animation_theta090.png`; Dialog bietet nur PNG und PDF (kein Video, kein GIF); Wiedergabe hält vor dem Dialog an; Datei lässt sich öffnen; im Stempel unten: „Arbeitsansicht – nicht für die Thesis“, Datei, „Ansicht 4 Schwingform“, Git-Hash, Zeile „Animation · θ = 90,0° · f = … Hz · Überhöhung ×…“, Zeile „Blickrichtung: Azimut …, Elevation …, Zoom …“, bei offenem M12 (und bei absolutem Bezug M8) Zeile „⚠ enthält unbestätigte Größen (…)“; Stempel überdeckt nichts, die Pflichttexte (Überhöhung, D_ref, f, θ) stehen im Bild (UI-31) | | |
| AN-11 | **Werte als Tabelle** | Dialog „Werte als Tabelle“: Titel mit θ, f und Überhöhung; eine Zeile je Messpunkt mit Status und Auslenkung x, y, z und Betrag bei dem Winkel, bei dem er geöffnet wurde; Esc oder „Schließen“ beendet; Wiedergabe hält an (UI-26) | | |
| AN-12 | Fenster 1100 × 680 und 1366 × 768 (und Skalierung 125 %, 150 %) | Kein Element überlappt; das Bild ist bei 1366 × 768 mindestens 600 × 320 px groß; Leiste bricht um statt abzuschneiden; Texte unverschnitten (UI-36) | | |
| AN-13 | Textalternative (nur wenn Sprachausgabe verfügbar, z. B. Windows-Sprachausgabe; sonst „entfällt“) | Beim Fokus im Bild liest sie Datei, Frequenz, θ, Überhöhung, Blickrichtung, größte Auslenkung, Kennzeichen (UI-26). Annahme: Sprachausgabe liest `accessibleDescription` des Bildes | | |

## B Messskript M1 bis M6 und Nutzerurteil M7 (lokal **und** in der Remotedesktop-Sitzung)

Das Skript misst die Zeiten der Animation und schreibt eine Tabelle mit Datei, Rechner, Sitzungsart und
Versionen. Zwei Läufe, mit demselben Aufruf bis auf `--sitzung`: erst am Messrechner selbst, dann
innerhalb der Remotedesktop-Sitzung (Fensterfläche wie im Alltag, Farbtiefe notieren). Laufzeit etwa 2 bis
5 Minuten **[Annahme]**; im Container: etwa 35 s für 30 Wiederholungen und 3 s je Bildrate.

```powershell
& $PY tools\auswertung\animation_messen.py "<Kopie.svd>" --sitzung lokal --rechner "<Name>" `
    --wiederholungen 100 --dauer 10 --tabelle "$ARB\animation_lokal.md" --json "$ARB\animation_lokal.json"
& $PY tools\auswertung\animation_messen.py "<Kopie.svd>" --sitzung remotedesktop --rechner "<Name>" `
    --wiederholungen 100 --dauer 10 --tabelle "$ARB\animation_rdp.md" --json "$ARB\animation_rdp.json"
```

Die Tabelle erscheint auch in der Konsole; die `.md`-Dateien kommen ins Prüfprotokoll. Ohne Qt-Fenster
(nur M5 und M6) mit `--ohne-qt`. Die Frequenz ist die Mitte der Achse; `--frequenz <Hz>` wählt eine
andere Linie. **Die Messwerte sind Zahlen zum Lesen.** Die Voreinstellungen (Bildrate 10 Bilder/s, Tempo
0,25 Perioden/s, Stufe L0) bleiben bis dahin **vorläufig** und werden **nach** dieser Messung vom
Orchestrator mit Jakob angepasst, nicht vor Ort.

| Nr | Messpunkt (Zeile der Tabelle) | Zweck | Erwartet (Container, offscreen, Median; Planungsrichtwert, am Messrechner zu belegen) | Ergebnis lokal | Ergebnis Remotedesktop |
|---|---|---|---|---|---|
| M1 | Bild voll (Achsen, Panes, Ticks) | Wahl der Rückfallstufe L0 bis L2 | ca. 74 ms | | |
| M1 | Bild mit vereinfachten Achsen | dto. | ca. 53 ms | | |
| M1 | Drehschritt (`view_init` und Zeichnen), vereinfacht und voll | Drehen flüssig? | ca. 53 ms vereinfacht, ca. 254 ms voll | | |
| M2 | Wiedergabe bei Soll 5, 10, 20 Bildern/s: effektive Bildrate, ausgelassene Bilder, „langsam“ gemeldet | Voreinstellung der Bildrate | effektiv ca. 5,0 / 9,7 / 15,7 Bilder/s; bei 20/s werden Bilder ausgelassen (die Bewegung bleibt zeitrichtig) | | |
| M3 | Mausziehen bis sichtbares Neuzeichnen | Drehen flüssig | ca. 55 ms | | |
| M4 | Phasenregler ziehen, je Schritt; Loslassen (Voll-Neuzeichnen) | Regler-Verhalten | ca. 77 ms ziehen, ca. 69 ms loslassen | | |
| M5 | `animation_daten`, drei Kanalpaare, kalt und warm; Arbeitsspeicher-Zuwachs | Zeit beim Wechsel in den Modus, Speicher | kalt ca. 159 ms (Ziel unter 400 ms, ADR-022), warm ca. 13 ms; Zuwachs ca. 89 MiB | | |
| M6 | Standbild speichern PNG und PDF | UI-31 | PNG ca. 0,5 s, PDF ca. 0,7 s | | |
| M7 | **Nutzerurteil über Remotedesktop** (nicht automatisch messbar): Drehen mit der Maus, Phasenregler ziehen, Wiedergabe bei 5, 10 und 20 Bildern/s, Zoom per Rad: flüssig genug? Texte und Farbleiste lesbar? Erscheint „Wiedergabe langsamer als eingestellt“? | UI-38 | **Urteil von Jakob** (flüssig / ruckelt, aber bedienbar / unbrauchbar; je Bildrate) | | |

Vorgehen bei M7: AN-3 bis AN-6 und AN-10 in der Remotedesktop-Sitzung wiederholen und je Punkt „flüssig“,
„ruckelt, aber bedienbar“ oder „unbrauchbar“ eintragen. Ist die Bildrate 10/s zu langsam, 5/s wählen
(Auswahl „Bildrate“ in der Auswahlspalte) und notieren; nichts am Programm ändern.

## Hinweise zur Auswertung

- Befunde mit Nummer, Zahl und ggf. Foto in `protokoll.md` (Abschnitt 10.17) eintragen; Nachweise gehen
  über `/laborbuch` in die Nachverfolgung ein. Die Tabellen (`animation_lokal.md`, `animation_rdp.md`,
  JSON) sichern.
- Zeiten vom Container sind Richtwerte (andere Hardware, ohne Fenster, ohne Remotedesktop); über 2× so
  langsam am Messrechner ist ein Befund, kein Fehler.
- Erst Jakobs ausdrückliche Bestätigung setzt UI-38 auf „bestanden“.
