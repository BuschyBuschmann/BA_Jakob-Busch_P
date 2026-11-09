<!-- Vom Nutzer am 2026-11-09 freigegeben (Grunddesign: „Ja, passt so“; Animation 3D drehbar; eine Größe je Diagramm; Annahmen 3–7 übernommen). -->

<!-- Paket K1-AUSW2 (ui-designer), Stufe 1. Status: GRUNDDESIGN ZUR FREIGABE (2026-11-09). Erweitert Brief K-AUSW und K-AUSW-LAYOUT. -->

## Grunddesign: Erweiterung „Auswerten“ (R-073, R-058, R-059, R-071)

**Charakter in einem Satz:** Das bestehende, ruhige Werkzeug-Layout bleibt; die vier neuen Funktionen setzen dort an, wo der Nutzer sie erwartet (Achsen am Plot, Vergleich als eigene Ansicht, Animation in der Schwingform).
**Farbwelt, Typografie, Dichte, Formensprache:** unverändert aus `tokens.py`/`stil.py` (hell, flach, rechtwinklig, Segoe UI/Consolas, Fokus 2 px `C_AKZENT`). Serien unterscheiden sich über Linienart plus Direktbeschriftung, Farbe nur zusätzlich (vier Serienfarben, vier Linienarten, Graustufentauglichkeit, kein Gelb).
**Woran es sich orientiert:** Brief K-AUSW, Layout-Vorgaben, ADR-021/024/025/026, KONVENTIONEN (Winkel in Grad, ζ mit Methode und Band, Mittelformel und Punktzahl im Bild).
**Bewusst vermieden:** Live-Neuzeichnen bei jedem Tastendruck oder Schieberzug, Dauer-Animationen der Oberfläche, frei schwebende Fenster, ein zweiter Reiter nur für Vergleiche.

### 1 Wo die Funktionen sitzen

| Funktion | Ort | Art |
|---|---|---|
| R-073 Achsen | neue schmale **Achsenleiste (AG)** zwischen Werkzeugleiste und Plot, in Ansicht 1, 2, 3 und 5 | Erweiterung bestehender Ansichten |
| R-058 Vergleich und R-059 eigenes Diagramm | **neue Ansicht 5 „Diagramm“** (fünfter Knopf in AC, Strg+5) plus **Messungsleiste** in AA (mehrere Messungen offen) | neue Ansicht; Vergleich ist der häufigste Sonderfall des Diagramms |
| R-071 Animation | **Modus „Animation“ in Ansicht 4** (Schwingform), Bedienleiste unter dem Plot | Erweiterung |

Ansichten 1 bis 4 arbeiten weiter auf der **aktiven Messung**; nur Ansicht 5 greift auf alle geöffneten Messungen zu. Die Skalenwahl „linear/logarithmisch“ zieht aus AD (Ansicht 1) in die Achsenleiste, damit es nur einen Ort gibt (dB bleibt in AD).

### 2 Grobskizze

```
+-AA---------------------------------------------------------------------------------+
| [Öffnen …] [Messung hinzufügen …]  (A) ref_Mitte.svd  x   (B) versuch2.svd  x   [Daten exportieren] [Bild speichern] |
+-AB Parameterzeile (aktive Messung) ------------------------------------------------+
+-AC [1 Spektrum] [2 H1/H2, Kohärenz] [3 Spitzen, Bänder] [4 Schwingform] [5 Diagramm] +
+-AD 260 px---------+-AE-------------------------------------------------------------+
| Auswahl der       | [Zoom][Hand][Zurücksetzen]                                      |
| Ansicht           | AG Frequenz [von] [bis] (lin|log)  Betrag [von] [bis] (lin|log) |
|                   |    Phase [von] [bis] (nur Ansicht 2)         [Alles auf Auto]   |
| Ansicht 5:        | +-------------------------------------------------------+       |
| Serien  [+ Serie] | |  Plot (überlagert) oder Teilbilder nebeneinander      |       |
|  1 —  A Mittel Z  | |  Legende mit Linienprobe unten außerhalb der Achse    |       |
|  2 -- B Mittel Z  | +-------------------------------------------------------+       |
| Größe: (|H1|)     |                                                                 |
| Anordnung: (über- |  Ansicht 4 im Modus Animation:                                  |
| lagert|neben-    |  [> Abspielen] Phase [====o======] 135° [Tempo] [Überhöhung]    |
| einander)         |                                                                 |
+-AF Cursorzeile --------------------------------------------- Prüfung: 9 ok, 1 Warnung +
```

### 3 Bedienablauf je Funktion

**R-073 Ausschnitte und Skalierung**
1. Im Feld „Frequenz von/bis“ (oder Betrag, Phase) Wert tippen, mit Enter oder Fokuswechsel übernehmen; der Plot zeichnet einmal neu.
2. Je Achse umschaltbar linear/logarithmisch; leeres Feld bedeutet „Auto“, „Alles auf Auto“ setzt zurück.
3. Zoom und Hand der Werkzeugleiste schreiben ihren Ausschnitt in dieselben Felder zurück (eine Wahrheit, zwei Wege).
4. Beim Wechsel von Messpunkt, Komponente oder Messung bleiben Bereiche und Skalierung je Ansicht erhalten; ungültige Eingaben (unten ≥ oben, Null oder negativ bei log) zeigen eine Inline-Meldung am Feld, der Plot bleibt unverändert.

**R-058 Messungen vergleichen**
1. „Messung hinzufügen …“ öffnet eine zweite Datei (Laden wie bisher im Hintergrund, Oberfläche bleibt bedienbar); sie erscheint als Chip „(B) Dateiname“ mit Kurzname (änderbar).
2. In Ansicht 5 „Aus aktueller Ansicht übernehmen“ legt die Auswahl der Ansicht 1 bis 3 als Serie an; „Für alle Messungen“ erzeugt dieselbe Auswahl je geöffneter Messung.
3. Anordnung „überlagert“ (eine Achse, Linienart je Serie) oder „nebeneinander“ (Teilbilder mit gekoppelten Achsen).
4. Achsenleiste wirkt auch hier; „Bild speichern“ nennt im Stempel alle Dateien und den Git-Hash.

**R-059 Eigene Diagramme**
1. Ansicht 5 wählen, „+ Serie“: Messung, Punkt oder Mittel, Komponente bzw. Kanalpaar wählen.
2. Eine **Größe** für das Diagramm wählen (Spektrum, |H1|, |H2|, Kohärenz, Phase); die y-Achse trägt deren Einheit.
3. Legende nennt je Serie Messung, Punkt/Mittel (mit Mittelformel und Punktzahl) und Komponente.
4. Serien lassen sich ein-/ausblenden und löschen; „Bild speichern …“ wie bisher (PNG/PDF).

**R-071 Betriebsschwingform animieren**
1. Ansicht 4, Frequenz wie bisher wählen (Feld oder Spitze), dann Modus „Animation“ (Betrag ist Voreinstellung, Animation nie automatisch gestartet).
2. Der Phasenregler (0 bis 360°, Anzeige in Grad) zeigt die momentane Auslenkung; „Abspielen“ lässt die Phase umlaufen, „Pause“ hält an, Einzelschritte per Tasten.
3. Bewegung: Punkte verschieben sich in der Bildebene um Auslenkung × Überhöhung (Regler), Komponente senkrecht zur Ebene als Größe und Hell/Dunkel (divergierend, graustufentauglich). Das Phasen-Standbild des Reglers entspricht exakt der Phasendarstellung bei gleichem Winkel (ADR-025).
4. Das Kennzeichen „⚠ unbestätigt (M8)“ steht dauerhaft im Kopf der Animation und im gespeicherten Standbild.

### 4 Zusammenspiel

- Achsenleiste gilt je Ansicht (1, 2, 3, 5) und im Vergleich für alle Teilbilder gemeinsam; in „nebeneinander“ sind die Achsen standardmäßig gekoppelt.
- Eine Serie in Ansicht 5 entspricht genau den Daten der Ansichten 1 bis 3 (gleiche Zeichenfunktionen aus `darstellung/`, Oberfläche und Thesis-Skript nutzen dasselbe).
- Verschiedene Messungen behalten ihre eigene Frequenzachse (keine Interpolation); Einheiten werden nie umgerechnet.
- **Remotedesktop (B2):** Eingaben wirken erst bei Enter oder Fokuswechsel; Schieber zeichnen nur die geänderten Objekte neu (kein Voll-Neuzeichnen), die Animation startet pausiert und ist per Phasenregler auch ohne Wiedergabe voll nutzbar; die Bildrate ist einstellbar. Geeignete Voreinstellungen sind am Messrechner über Remotedesktop zu messen, nicht zu schätzen.
- **Andockstellen später:** R-070 als Auswahl „Koordinatensystem: global | lokal“ in AD der Ansicht 4 und bei Komponenten (n, t1, t2 neben X, Y, Z); R-072 als weitere Ansichten in AC (Knopfleiste wird dann zur Liste). Heute nichts davon gestaltet.

### 5 Bewusst nicht gemacht

Differenz- oder Verhältniskurven zwischen Messungen; Interpolation auf gemeinsames Gitter; Umrechnung der Größen; drehbare 3D-Ansicht (außer Antwort auf Frage 1); Speichern der Animation als Video/GIF; Änderungen am Reiter „Messen“.

### 6 Offene Fragen

**Blockierend (für den Brief)**
1. **Animation: 2D oder 3D?** Freigegeben ist eine 2D-Aufsicht mit Projektionsebene. R-071 verlangt „auf der Messgeometrie“. Vorschlag: 2D wie oben beschrieben. Eine räumliche, drehbare Ansicht ist deutlich aufwendiger und über Remotedesktop zäher. *Auswirkung:* Darstellungsart, Aufwand, Tempo.
2. **Verschiedene Größen in einem Diagramm (R-059)?** Vorschlag: eine Größe pro Diagramm; verschiedene Größen nur über „nebeneinander“ (je Teilbild eine Größe). Alternative: zwei y-Achsen (links/rechts). *Auswirkung:* Komplexität der Serienliste, Lesbarkeit im Graustufendruck.

**Nicht blockierend**
3. Bis zu **vier Serien** pro Diagramm (vier unterscheidbare Linienarten)? *Annahme:* ja; mehr Serien über „nebeneinander“.
4. Beim **Öffnen einer neuen Datei** Achsenbereiche zurücksetzen, Skalierung behalten? *Annahme:* ja.
5. **Punktzuordnung zwischen Messungen** mit unterschiedlichem Messgitter: über das Punktlabel; Mittel immer möglich. *Annahme:* ja.
6. Animation als **Bilderserie/Video speichern**? *Annahme:* nein, nur Standbild je Phasenwinkel per „Bild speichern“.
7. Farbbereich (Min/Max) der Schwingform in Ansicht 4 einstellbar? *Annahme:* ja, als Kann in der Achsenleiste.

### 7 Empfehlung

Die Phasen-/Vorzeichenkonvention der Animation (Zeiger mal Phasenfaktor, Bezug) vor der Umsetzung kurz vom `strukturdynamik-experte` absichern lassen (Ablauf E), da „Phase der Bewegung = dargestellte Phase“ prüfbar sein muss.
