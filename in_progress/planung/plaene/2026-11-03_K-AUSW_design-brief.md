<!-- Paket K-AUSW (ui-designer, sonnet), Stufe 2. Status: FREIGEGEBEN vom Nutzer am 2026-11-03. Entscheidungen: OE-1 Leser um Mittelung/Fenster erweitern (Gegenprobe File-Access-Werte vom 02.11.), OE-2 logarithmisch, OE-3 Auswahl beim Dateiwechsel zurücksetzen. -->

## Design-Brief: Auswertungsoberfläche „Auswerten“ (Paket K-AUSW, Stufe 2)

**Bezug:** R-032 (Soll), R-050 bis R-053, R-055; ADR-001 (PySide6/Qt Widgets), ADR-021 (matplotlib, `Figure` + `FigureCanvasQTAgg`, nie `pyplot`); KONVENTIONEN.md (Einheiten, Dämpfungsangaben mit `zeta`/`band_u_hz`/`band_o_hz`/`methode`, Abbildungsregeln, gemeinsame Zeichenfunktion); Brief P3 (Designsystem, Tokens).
**Bestätigt vom Nutzer (2026-11-03):** Grunddesign „Ja, passt so“; Reiter „Messen | Auswerten“ unter der Statuszeile; Schwingform als 2D-Aufsicht mit wählbarer Projektionsebene; Ansicht 1 mit X/Y/Z gleichzeitig (Mehrfachauswahl), Punkte einzeln plus Mittel; Plausibilitätszusammenfassung in der Fußzeile; nur die Größe aus der Datei (keine Umrechnung); Export der Auswertungsdaten und „Bild speichern“.

**Nutzerziel und wichtigste Aktionen:** Der Verfasser (fachkundig, Deutsch, Messrechner Windows und eigener Laptop) öffnet eine `.svd`-Datei und sieht ohne weiteren Bedienschritt das Spektrum samt Parameterzeile. In Reihenfolge der Häufigkeit:
1. Datei öffnen, Spektrum prüfen (Punkt, Komponente wechseln).
2. Zwischen den vier Ansichten wechseln, Frequenz wählen, Werte ablesen.
3. Spitzen, ζ, Band und Methode sowie Band-RMS einsehen.
4. Unbestätigtes erkennen (Phase, M8).
5. Auswertungsdaten exportieren, Arbeitsansicht als Bild speichern.

---

### 1 Informationshierarchie und Layout

Das Hauptfenster behält Zone A (Statuszeile, 44 px, immer sichtbar). Darunter liegt eine Reiterleiste (`QTabWidget`, Reiter „Messen“ und „Auswerten“). Der Reiter „Messen“ enthält unverändert die Zonen B bis G aus P3. Der Reiter „Auswerten“:

| Zone | Inhalt | Verhalten |
|---|---|---|
| AA Dateileiste (48 px) | `Öffnen …`, Dateiname fett und Pfad (Consolas, links gekürzt, Tooltip Volltext), rechts `Daten exportieren …` und `Bild speichern …`, daneben dezent „Arbeitsansicht“ | feste Höhe |
| AB Parameterzeile (44 px, Platz immer reserviert) | Zellen mit kleiner Beschriftung über dem Wert (Consolas): Bandbreite, Linien, Δf, Mittelung, Fenster, Punkte, Referenz (Name und Einheit) | feste Höhe, Zellen werden rechts ausgeblendet, wenn zu schmal (Tooltip in AB nennt alle Werte) |
| AC Ansichtswahl (32 px) | vier umschaltbare Knöpfe „1 Spektrum“ · „2 H1/H2 und Kohärenz“ · „3 Spitzen und Bänder“ · „4 Schwingform“ | feste Höhe |
| AD Auswahlspalte | links, 260 px fest, scrollbar bei Überlänge; Inhalt wechselt mit der Ansicht (Abschnitt 3) | Höhe wächst |
| AE Darstellung | rechts, wächst | Plot oder Tabelle |
| AF Fußzeile (30 px) | links Cursor-/Meldezeile (Consolas), rechts Prüfzusammenfassung „Prüfung: 9 ok, 1 Warnung“ (klickbar) | feste Höhe |

- Mindestgröße wie P3 (1100×680). Bei 1366×768 hat AE mindestens 600×320 px.
- Dateileiste, Parameterzeile und Ansichtswahl bleiben bei jedem Wechsel stehen. Nur AD, AE und AF ändern sich.
- AB zeigt Werte aus den Einstellungen der Datei, nichts Berechnetes. Ist ein Wert in der Datei nicht lesbar, steht „–“ mit Tooltip „in der Datei nicht lesbar“ (kein Raten). Siehe Umsetzerfragen U-1.

**Reiter und Statuszeile:**
- Zone A bleibt oberhalb der Reiter und zeigt auch beim Auswerten Betriebsart, Durchgang und Verbindung.
- Tritt im „Messen“-Reiter ein Hinweisband mit Handlungsbedarf auf (Fälle 1, 4, 5 aus P3 3.5), erhält der Reiterkopf „Messen“ das Zusatzwort mit Symbol: „Messen ⚠ Entscheidung nötig“ (Fall 4), „Messen ⚠ Bestätigung nötig“ (Fall 5), „Messen ✖ Gerät unklar“ (Fall 1). `QApplication.alert` wie bisher. Der Reiter wird nie automatisch gewechselt, der Fokus nie verschoben.
- Läuft ein Durchgang, steht im Reiterkopf „Messen ▶ läuft“.
- Der Reiter „Auswerten“ greift nicht in die Sitzung ein und ist in allen Betriebsarten und Durchgangszuständen bedienbar. Datei lesen und Rechnen belasten den Messbetrieb nicht (siehe U-2).

### 2 Visuelle Richtung

Aus P3 übernommen: Fusion-Stil, Palette und QSS aus `tokens.py`/`stil.py`, hell, rechtwinklig, flach, 8-px-Raster, Fokusrahmen 2 px `C_AKZENT`, Tabellenzeilen 32 px, Segoe UI 10 pt, Consolas für Zahlen. Keine Verläufe, Schatten, Animationen.

**Neue Tokens (nur in `tokens.py`):**
- Plot: `C_PLOT_HAUPT` = `C_AKZENT`; `C_PLOT_GITTER` = `C_LINIE_ZEILE`; `C_PLOT_ACHSE` = `C_TEXT`; `C_PLOT_FLAECHE` = `C_FLAECHE`; `C_PLOT_BAND` (Bandschattierung, hellgrau, z. B. `#E7E5DF`; Kontrast der Kurve darauf prüfen).
- Linienarten statt Farbe als Unterscheidung: durchgezogen, gestrichelt, punktiert, Strichpunkt (Tabelle `PLOT_LINIENARTEN`). Je Serie zusätzlich Direktbeschriftung am Kurvenende oder Legende mit Linienprobe.
- Weitere Serienfarben nur aus einer kurzen Liste, die im Graustufendruck unterscheidbar bleibt (Helligkeitsstufen von `C_AKZENT` bis `C_TEXT_GEDAEMPFT`). Kein Gelb, kein Rot-Grün-Paar.
- Rolle „unbestätigt“: Hintergrund `C_WARN_BG`, Rand `C_WARN_RAND`, Symbol ⚠ plus Wort „unbestätigt“ (Symbol über `tokens.symbol("warnung")`, ASCII-Rückfall gilt).

**Achsen:** „Größe [Einheit]“ (KONVENTIONEN.md), Dezimalkomma auf den Achsenbeschriftungen der Oberfläche, Frequenz in Hz. Die Oberfläche setzt in der Arbeitsansicht über dem Plot eine Kopfzeile (Datei, Punkt, Komponente) als **Qt-Label**, nicht im Plot. Die gemeinsame Zeichenfunktion selbst zeichnet keinen Diagrammtitel.

**Gemeinsame Zeichenfunktion (ADR-021, KONVENTIONEN.md):**
- Je Ansicht gibt es genau eine Zeichenfunktion, die eine übergebene `matplotlib.figure.Figure` füllt. Sie ist GUI-frei (kein Qt-Import, kein `pyplot`), bekommt nur Daten und Darstellungsoptionen und gibt Hilfsobjekte (Achsen, Linien) zurück.
- Der Stempel „Arbeitsansicht – nicht für die Thesis“, Dateiname, Ansicht, Hinweis „unbestätigt“ und Git-Hash gehören **nicht** in diese Funktion. Sie liegen in der Bild-speichern-Variante (eigene Funktion, die auf derselben Figure einen Fußstempel ergänzt).
- Die Oberfläche hält die Fläche hinter einer schmalen Schnittstelle (z. B. `PlotFlaeche` mit `zeichne(ansicht, daten, optionen)`, `speichere(pfad)`, `setze_cursor(x)`), damit pyqtgraph als Rückfallweg möglich bleibt (ADR-021).

### 3 Komponenten und Inhalte je Ansicht

#### 3.0 Dateileiste und Öffnen
- `Öffnen …` (`QFileDialog`, Filter „PSV-Messdatei (*.svd)“, zuletzt benutzter Ordner wird gemerkt). Die Liste „Zuletzt geöffnet“ (höchstens fünf, nur im Leerzustand) steht in AE.
- Nach erfolgreichem Lesen: Ansicht 1 mit „Mittel (alle Punkte)“ und 3D ist gewählt (Option siehe 3.1), Parameterzeile gefüllt, `Daten exportieren …` und `Bild speichern …` aktiv.
- Drag-and-drop einer `.svd` auf das Fenster (Kann, K).

#### 3.1 Ansicht 1: Spektrum
- AD: Punktliste (`QListWidget`, Einfachauswahl): erster Eintrag „Mittel (alle Punkte)“, danach je Messpunkt „Punkt <Label> (x, y, z in m)“. Komponente: Kontrollkästchen „X“, „Y“, „Z“, „3D“ (Mehrfachauswahl, mindestens eines gewählt). Skala: „Amplitude: linear | logarithmisch | dB“ (Auswahl aus drei Radioknöpfen; dB nur, wenn die Größe in der Datei dafür eine Referenz hat, sonst deaktiviert mit Grund). Unter „Mittel“ und „3D“ ein Hinweis aus dem Rechenkern, wie gemittelt bzw. der 3D-Betrag gebildet wird.
- AE: Spektrum der Auswahl, Frequenz [Hz] über Amplitude [Einheit der Datei]. Mehrfachauswahl zeichnet jeweils eine Kurve je Komponente (Linienart je Komponente). 3D wird als eigene Kurve gezeichnet.
- Voreinstellung nach dem Öffnen: „Mittel (alle Punkte)“, Komponenten X, Y, Z und 3D alle gewählt.
- AF: Cursorwerte (siehe 4).

#### 3.2 Ansicht 2: H1/H2 und Kohärenz
- AD: Punktliste wie 3.1; Kanalpaar-Auswahl (Antwort/Referenz) nur sichtbar, wenn mehr als ein Paar existiert; Kontrollkästchen „H1“ und „H2“; Kontrollkästchen „Phase anzeigen“.
- AE: drei Teilbilder mit gemeinsamer Frequenzachse: Betrag (oben), Phase (Mitte, nur bei „Phase anzeigen“), Kohärenz γ² (unten, 0 … 1). Der Einheitenquotient der FRF steht an der Achse (aus `einheit_quotient`, hängt vom Referenzkanal ab, O4: Kraft auf Ref1).
- Die Phase trägt das Kennzeichen „unbestätigt“ (Abschnitt 5) im Teilbildkopf; Kohärenz und Betrag tragen es nicht.
- Fehlt der Referenzkanal: Platzhalter (Abschnitt 6).

#### 3.3 Ansicht 3: Spitzen und Bänder
- AD: keine Auswahlliste, stattdessen zwei Tabellen (`QTableView`, nicht sortierbar außer per Klick auf den Spaltenkopf, Zeilenhöhe 32 px):
  - **Spitzen:** Nr · f_sp [Hz] · ζ · band_u_hz [Hz] · band_o_hz [Hz] · Methode · Kennzeichen. Jede Zeile hat alle fünf Dämpfungsfelder; ohne Bandgrenzen und Methode wird ζ nicht ausgegeben (R-055). Modenfit-Werte (optional) stehen als zusätzliche Zeilen mit Methode „Modenfit“ (nicht ersetzend).
  - **Bänder:** Nr · f_u [Hz] · f_o [Hz] · RMS [Einheit] · Bezug (Punkt bzw. Mittel).
- AE: Spektrum bzw. |H1| der Auswahl mit Spitzenmarkern (Marker plus Beschriftung f, ζ), Bänder als schattierte Flächen (`C_PLOT_BAND`). Ein Klick auf eine Tabellenzeile markiert die Spitze bzw. das Band im Plot und umgekehrt (Klick auf einen Marker, Soll).
- Schnittstelle: Zahlen aus den Ergebnisobjekten (`Spitzenergebnis`, `Bandwert`, Modenfit), die GUI rechnet nicht.

#### 3.4 Ansicht 4: Schwingform
- AD: Frequenzfeld „Frequenz [Hz]“ (`QDoubleSpinBox`, Dezimalkomma) mit Zeile „nächste Linie: 123,75 Hz“; Schnellwahl „Spitze …“ (Liste der Spitzen aus Ansicht 3, falls vorhanden); Projektionsebene „xy | xz | yz“ (Radioknöpfe); Auswahl „Betrag | Phase (unbestätigt)“.
- AE: Aufsicht auf die Messpunkte in der gewählten Ebene (Koordinaten aus `Punkte.koordinaten_m`, Punktlabels klein daneben, abschaltbar), Betrag als Füllung eines Einfarbverlaufs (Graustufen taugen) plus Farbleiste mit Einheit; optional Dreiecksnetz über `tripcolor`.
- Die Phase ist anwählbar, aber **nie Voreinstellung**. Solange M8 offen ist, trägt die Phase-Ansicht das Kennzeichen „unbestätigt“ im Kopf und im Bildstempel.
- Ohne Referenz oder Trigger: nur Betrag, Hinweis „Phase nicht verfügbar: keine Referenz.“ (Option „Phase“ deaktiviert mit Text im Plotkopf, nicht nur Tooltip).

### 4 Interaktionen und Einstufung (Zoom, Cursor, Klick)

| Interaktion | Stufe | Anmerkung |
|---|---|---|
| Zoom und Verschieben per `NavigationToolbar2QT` (Lupe, Hand, Zurücksetzen/Home) über AE, Ansichten 1 bis 3 | **Muss** | Toolbar nur mit Text- bzw. Unicode-Beschriftung, keine Bilddateien (P3: keine Icon-Dateien); falls die Standardsymbole der Toolbar mitgeliefert werden, bleibt das dem Umsetzer überlassen, es darf aber keine zusätzliche Dateiabhängigkeit entstehen (U-5) |
| Frequenzfeld und Zahlenfelder (Frequenz in Ansicht 4, Skala) | **Muss** | Hauptweg der Frequenzwahl; wirkt ohne jede Plotinteraktion |
| Fadenkreuz-Cursor (vertikale Linie mit Wertanzeige in AF) | **Soll** | nur mit Blitting (ADR-021: 0,3 ms gegen 27 ms ohne); fällt der Blitting-Pfad aus, bleibt der Cursor aus, die Zahlenfelder genügen |
| Klick in den Plot setzt die Frequenz der Schwingform (Ansichten 1 bis 3 → Feld in AD, Ansicht 4 nutzt den Wert) | **Soll** | rastet auf die nächste Linie ein |
| Klick auf Spitzenmarker markiert Tabellenzeile | **Soll** | |
| Doppelklick = Zurücksetzen der Ansicht | **Kann** | gleichwertig zum Home-Knopf der Toolbar |
| Drag-and-drop der Datei aufs Fenster | **Kann** | |
| Verschieben von Bandgrenzen per Maus | nicht vorgesehen | |

**Cursorzeile AF:** „f = 123,75 Hz · Amplitude = 1,23 mm/s · Punkt 12 · Vib Z“ (Consolas, rechtsbündige Ziffern, feste Breite, damit nichts springt). Ohne Cursor: Meldezeile mit letzter Aktion (z. B. „Export geschrieben: <Pfad>“).

**Aktualisierung:** Wechsel von Punkt, Komponente oder Ansicht zeichnet die betroffene Figur neu (Ziel < 100 ms bei der Beispieldatei; ADR-021: 42 bis 52 ms offscreen/Linux, am Messrechner zu prüfen). Auswahl, Zoomzustand und Scrollposition der Auswahlspalte bleiben bei Wechsel der Ansicht je Ansicht erhalten. Ein neuer Dateiaufruf setzt Zoom zurück.

### 5 Kennzeichnung unbestätigter Größen

- Muster überall gleich: Symbol ⚠, Wort „unbestätigt“, Rolle „unbestätigt“ (Token), kurze Begründung (z. B. „M8: Polarität der Referenzkanäle offen“).
- Wo: Kopf des Phasen-Teilbilds (Ansicht 2); Schalter und Plotkopf der Phase (Ansicht 4); Spalte „Kennzeichen“ der Spitzentabelle (Ansicht 3, mit den `kennzeichen` aus `Spitze.kennzeichen`); in `Bild speichern` im Fußstempel.
- Quelle: `annahmen.AnnahmeEintrag.ist_annahme` aus `Auswertung.annahmen_liste`. Der Text kommt aus `AnnahmeEintrag.beschreibung`, die GUI schreibt keine Annahmen fest. Wird M8 bestätigt, verschwindet das Kennzeichen ohne GUI-Änderung.
- Welche Annahme welche Größe betrifft (Zuordnung M8 → Phase), steht in einer **einzigen** Zuordnungstabelle in der GUI-Schicht (z. B. `ABHAENGIG_VON = {"phase": ("M8",)}`), nicht verstreut.
- Im Export (JSON) stehen die Annahmen bereits aus dem Rechenkern; die GUI ändert dort nichts.

### 6 Zustände

| Zustand | Darstellung |
|---|---|
| Keine Datei | AE: zentriert „Noch keine Messdatei geöffnet.“, Knopf `Messdatei (.svd) öffnen …`, Liste „Zuletzt geöffnet“. AB zeigt „–“. `Daten exportieren …`, `Bild speichern …`, Ansichtswahl und AD deaktiviert (Tooltip: „Zuerst eine Messdatei öffnen.“) |
| Laden | AA, AC, AD deaktiviert; AE zeigt „Lese <Dateiname> …“ mit unbestimmtem Balken; die bisherige Datei bleibt bis zum Erfolg sichtbar (ausgegraut). Die Oberfläche bleibt bedienbar (Reiter, Fenster verschieben) und friert nicht ein (U-2) |
| Fehler beim Lesen | Fehlerband (`C_FEHLER_BG`, `C_FEHLER` 2 px, ✖ und Wort „Fehler“) oberhalb AE: „✖ Datei kann nicht gelesen werden: <Text des Lesers, enthält den Pfad>“, Knopf `Schließen`. Die vorher geladene Datei bleibt unverändert. Bei Fehler ohne vorherige Datei: Zustand „Keine Datei“ plus Band |
| Unvollständige Datei (z. B. fehlende Punkte) | Wie Fehler, aber mit Text des Lesers; keine halb geladene Darstellung |
| Fehlende Referenz → keine FRF | Ansicht 2: statt Plot der Text „Keine Übertragungsfunktion: Die Datei enthält keinen aktiven Referenzkanal. H1, H2 und Kohärenz brauchen eine Referenz.“ Ansicht 1 bleibt voll. Ansicht 3: Spitzentabelle zeigt „Keine Spitzensuche: Referenzkanal fehlt.“ (falls Spitzen nur auf FRF möglich, U-3); Bandtabelle zeigt vorhandene Band-RMS. Ansicht 4: nur Betrag (3.4) |
| Eingabe außerhalb | Frequenz außerhalb des Frequenzbereichs der Datei (z. B. 0,625 … 1000 Hz): Inline-Meldung unter dem Feld „✖ Frequenz 1200 Hz liegt außerhalb 0,625 … 1000 Hz.“, Plot unverändert |
| Berechnung ohne Ergebnis | Keine Spitze gefunden: Tabelle zeigt „Keine Spitzen gefunden.“; keine Bänder: „Keine Bänder angegeben.“ |
| Export/Bild | Nach Erfolg Meldung in AF mit Pfad; Fehler als `QMessageBox.warning` mit dem Text des Rechenkerns. Existiert das Ziel, greift der Überschreibschutz aus dem Rechenkern (`pruefe_ziel`), die GUI zeigt dessen Meldung |
| Prüfzusammenfassung | Text in AF: „Prüfung: 9 ok, 1 Warnung“ (Wörter, nie nur Farbe). Klick öffnet einen schreibgeschützten Dialog mit der Liste P-01 bis P-11 (Nr, Ergebnis, Text aus `Pruefergebnis`); Esc schließt |

### 7 Speichern

- `Daten exportieren …`: Ruft die vorhandenen Exporte (`exportiere`/`schreibe_export`, JSON + NPZ) an. `QFileDialog.getSaveFileName` bzw. Ordnerwahl mit Basisnamen. Voreinstellung: Ordner und Basisname der Messdatei. Ergebnis: Meldung mit beiden Pfaden.
- `Bild speichern …`: Dialog mit Filter „PNG (*.png)“ und „PDF (*.pdf)“. Speichert die aktuelle Ansicht (die Figur, mit Stempel). Der Stempel steht unten im Bild: „Arbeitsansicht – nicht für die Thesis · <Dateiname> · <Ansicht> · <Git-Hash>“ und, falls zutreffend, „⚠ enthält unbestätigte Größen (M8)“. Auflösung bei PNG: wählbar nur über Einstellung im Code (Voreinstellung 200 dpi), kein Dialogfeld.
- Thesis-Abbildungen entstehen nur per Skript, das dieselben Zeichenfunktionen ohne Stempel nutzt.

### 8 Tastaturbedienung

| Taste | Aktion |
|---|---|
| Strg+Umschalt+O | Messdatei öffnen (nur im Reiter „Auswerten“ aktiv) |
| Alt+1 / Alt+2 | Reiter „Messen“ / „Auswerten“ |
| Strg+1 … Strg+4 | Ansicht 1 bis 4 |
| Strg+E | Daten exportieren |
| Strg+Umschalt+S | Bild speichern |
| Pos1 | Zoom zurücksetzen (Fokus im Plot) |
| ← / → | Cursor um eine Linie bewegen (Fokus im Plot, Soll) |
| Umschalt+← / → | Cursor um 10 Linien |
| Enter (Fokus im Plot, Ansichten 1 bis 3) | aktuelle Cursorfrequenz als Schwingformfrequenz übernehmen (Soll) |
| Strg+Enter (Fokus Frequenzfeld) | Frequenz übernehmen |
| Tab | Reihenfolge: AA → AB (nicht fokussierbar) → AC → AD → AE (Plot, Toolbar) → AF-Prüftext |

- F5 bis F8 und Strg+N, Strg+S, Strg+O (Warteschlange) bleiben Reiter „Messen“ vorbehalten und tun im Reiter „Auswerten“ nichts.
- Aktionen sind als `QAction` mit `Qt.WindowShortcut` angelegt (eine Quelle für Knopf, Taste, Aktivierung). Alle Knöpfe zeigen ihre Taste im Tooltip.
- Die Reihenfolge der Tabulatortaste führt in den Plot (fokussierbar, `focusPolicy` ≠ `NoFocus`) und die Toolbar.

### 9 Responsives Verhalten

Desktop, kein Handy-Layout. Mindestgröße 1100×680. AD fest 260 px; schrumpft AE unter 600×320 px, werden zuerst die Beschriftungen in AB gekürzt, dann AD scrollbar. Teilbilder in Ansicht 2 teilen sich die Höhe (Betrag 45 %, Phase 30 %, Kohärenz 25 %), bei abgeschalteter Phase 65 %/35 %. Windows-Skalierung 125/150 % über Qt-HiDPI (Plotgröße in logischen Pixeln; `Figure` mit `devicePixelRatio` des Canvas).

### 10 Accessibility

- Alle Eingaben mit Beschriftung und Buddy. Segmentleiste: `accessibleName` je Knopf („Ansicht 1: Spektrum“ …), Auswahlzustand als `checked`.
- Der Plot hat `accessibleName` „Diagramm: <Ansicht>“ und eine **Textalternative**: `accessibleDescription` fasst Datei, Punkt, Komponenten, Frequenzbereich und bei Spitzen die gefundenen Werte zusammen. Die Tabellen in Ansicht 3 sind die barrierefreie Entsprechung der Spitzen und Bänder.
- Farbe trägt nie allein Information: Linienarten, Direktbeschriftung, Symbol + Wort für Unbestätigtes und Fehler.
- Kontraste: Text 4,5:1, Plotlinien und Fokus 3:1 gegen Plotfläche. Die neuen Paare kommen in `KONTRAST_PAARE` (Test UI-23-Verfahren).
- Sichtbarer Fokus überall (2 px `C_AKZENT`), auch im Plot (Rahmen um AE).
- Alle Texte Deutsch, Einheiten mit Leerzeichen („0,625 Hz“), Dezimalkomma in der Oberfläche. Keine Meldung verschwindet selbsttätig, die Meldezeile in AF behält den letzten Text bis zur nächsten Aktion.

### 11 Technische Hinweise

- Ablage unter `software/src/ldv_automation/gui/`, neue Dateien z. B. `auswerten_reiter.py`, `plotflaeche.py`, `auswahl.py`, `tabellen.py`; `hauptfenster.py` erhält nur den Reiterrahmen. Zeichenfunktionen GUI-frei in einem eigenen Modul außerhalb von `gui/` (z. B. `ldv_automation/darstellung/`), damit die Skripte der Thesis sie importieren können. Importregel: `gui` darf zusätzlich `auswertung` und die Zeichenmodule importieren, sonst weiter nur `sitzung` und `domaene` (Importtest anpassen, nicht aufweichen).
- Anzeige-Logik in **reinen Funktionen** ohne Qt (analog `anzeige.py`): Parameterzeile (Zellen aus Dateieinstellungen), Ansichtsverfügbarkeit (welche Ansicht, welcher Platzhaltertext), Spitzen-/Bandzeilen, Kennzeichnung (Zuordnung Annahme → Größe), Prüfzusammenfassung, Cursortext. Sie sind ohne Qt testbar.
- matplotlib nur als `Figure` und `FigureCanvasQTAgg`; `pyplot` ist nirgends in `gui/` und `darstellung/` importiert (Importtest). Blitting für den Cursor; fällt es aus, bleibt der Cursor aus.
- Plot-Test nicht über Pixel, sondern über die Figure-Struktur (Achsenbeschriftungen, Zahl der Linien, Linienarten, Text der Kennzeichnung).
- Neue Abhängigkeit: matplotlib (ADR-021), Marker `gui`, Tests offscreen. Sonst keine.
- Stabile `objectName`s: `reiter`, `auswerten`, `btn_oeffnen`, `lbl_datei`, `btn_export`, `btn_bild`, `parameterzeile`, `par_bandbreite`, `par_linien`, `par_delta_f`, `par_mittelung`, `par_fenster`, `par_punkte`, `par_referenz`, `ansichtswahl`, `btn_ansicht_1` … `btn_ansicht_4`, `liste_punkte`, `chk_x`, `chk_y`, `chk_z`, `chk_3d`, `rb_skala_*`, `chk_h1`, `chk_h2`, `chk_phase`, `tabelle_spitzen`, `tabelle_baender`, `feld_frequenz`, `rb_ebene_*`, `rb_groesse_betrag`, `rb_groesse_phase`, `plot`, `plot_platzhalter`, `fusszeile`, `lbl_cursor`, `lbl_pruefung`, `band_fehler`.

**Streichreihenfolge bei Zeitnot:** 1 Drag-and-drop; 2 Doppelklick-Zurücksetzen; 3 Klick-Frequenzwahl; 4 Cursor und Cursortasten (Soll); 5 Prüfdialog (Zusammenfassung bleibt als Text); 6 „Zuletzt geöffnet“. **Nie streichen:** Parameterzeile (R-032), Spektrum nach dem Öffnen, Zustände „Keine Datei“, „Fehler“, „Keine Referenz“, Kennzeichnung „unbestätigt“, ζ nur mit Bandgrenzen und Methode, Zoom/Pan, Export und Bild speichern.

### 12 UI-Akzeptanzkriterien

Priorität: M = muss, S = soll, K = kann. Alle gegen die Beispieldatei `Input/20261012_ref_Mitte.svd` und synthetische Dateien bzw. Attrappen, ohne Hardware, offscreen (`gui`-Marker).

- **UI-1 (M, R-032):** Nach dem Öffnen von `20261012_ref_Mitte.svd` ist ohne weitere Bedienung Ansicht 1 aktiv und `plot` enthält mindestens eine Kurve; Achsenbeschriftung „Frequenz [Hz]“ und „Amplitude [<Einheit der Datei>]“.
- **UI-2 (M, R-032):** Die Parameterzeile zeigt „1000 Hz“ (Bandbreite), „1600“ (Linien) und „0,625 Hz“ (Δf) für die Beispieldatei. Für Mittelung und Fenster steht der Wert aus der Datei bzw. „–“ mit Tooltip „in der Datei nicht lesbar“, nie ein geratener Wert.
- **UI-3 (M):** Ohne geladene Datei zeigt AE „Noch keine Messdatei geöffnet.“ und `btn_oeffnen`; `btn_export`, `btn_bild` und die Ansichtsknöpfe sind deaktiviert (Tooltip nennt den Grund); `parameterzeile` belegt weiterhin 44 px.
- **UI-4 (M, R-050):** In Ansicht 1 stellt die Auswahl „Mittel“ und „Punkt n“, jeweils mit X, Y, Z, 3D einzeln und gemeinsam ein; die Zahl der gezeichneten Linien entspricht der Zahl der gewählten Komponenten; mindestens eine Komponente bleibt gewählt (letztes Kontrollkästchen lässt sich nicht abwählen). Die Linienarten der Serien sind paarweise verschieden.
- **UI-5 (M, R-051):** Für eine Datei mit Referenzkanal zeigt Ansicht 2 Betrag und Kohärenz (Achse „Kohärenz [1]“ bzw. γ² von 0 bis 1) und mit „Phase anzeigen“ zusätzlich die Phase; H1 und H2 sind einzeln abschaltbar. Die Betrags-Einheit entspricht dem Quotienten aus Antwort- und Referenzeinheit.
- **UI-6 (M, R-051):** Für eine Datei ohne Referenzkanal zeigt Ansicht 2 den Text „Keine Übertragungsfunktion: …“ statt eines Plots; Ansicht 1 bleibt unverändert nutzbar.
- **UI-7 (M, R-053, R-055):** Ansicht 3 listet jede Spitze mit Frequenz, ζ, band_u_hz, band_o_hz und Methode; keine Zeile hat ein ζ ohne Bandgrenzen und Methode (Test: Zeilen mit fehlenden Feldern werden nicht angezeigt, sondern als Fehler gemeldet). Die Bandtabelle zeigt für jedes Band f_u, f_o und RMS mit Einheit; Werte stimmen im Test mit den Ergebnisobjekten überein.
- **UI-8 (M, R-053):** Ein Klick auf eine Zeile der Spitzentabelle markiert im Plot die zugehörige Spitze (Marker mit Beschriftung f und ζ); Bänder erscheinen als schattierte Flächen, ohne dass die Kurve verdeckt wird.
- **UI-9 (M, R-052):** Ansicht 4 zeigt bei gewählter Frequenz den Betrag der Schwingform auf den Messpunkten in der gewählten Projektionsebene mit Farbleiste und Einheit; die Frequenz rastet auf die nächste Linie ein und dies steht in der Zeile „nächste Linie: … Hz“. Eine Frequenz außerhalb des Bereichs zeigt die Inline-Meldung und ändert den Plot nicht.
- **UI-10 (M, R-052, M8):** Die Phase-Ansicht ist nicht voreingestellt. Wird sie gewählt, steht im Plotkopf „⚠ Phase unbestätigt“ (mit dem Text der Annahme M8). Ohne Referenz oder Trigger ist die Option „Phase“ deaktiviert und im Plotkopf steht „Phase nicht verfügbar: keine Referenz.“
- **UI-11 (M, M8):** Ansicht 2 trägt am Kopf des Phasen-Teilbilds „⚠ unbestätigt“. Wird im Test `ist_annahme` für M8 auf `False` gesetzt, verschwindet das Kennzeichen ohne Codeänderung in der GUI. Es gibt genau eine Zuordnungstabelle Annahme → Größe.
- **UI-12 (M):** Zoom und Verschieben per Toolbar wirken in Ansichten 1 bis 3; „Home“ bzw. Pos1 stellt den Ausgangsbereich wieder her. Ein neuer Dateiaufruf setzt den Zoom zurück, ein Wechsel zwischen Ansichten behält ihn je Ansicht.
- **UI-13 (S):** Der Fadenkreuz-Cursor folgt der Maus (Test über Aufruf von `setze_cursor`) und die Cursorzeile zeigt „f = … Hz · … · Punkt … · Vib …“; ohne Blitting-Unterstützung bleibt der Cursor aus, und es erscheint kein Fehler. Cursor links/rechts verschiebt um eine Linie (← / →), Umschalt+← / → um zehn.
- **UI-14 (S):** Ein Klick im Plot (Ansichten 1 bis 3) setzt das Frequenzfeld auf die nächste Linie; Enter im Plot übernimmt die Cursorfrequenz.
- **UI-15 (M):** Beim Lesen sind AA, AC, AD deaktiviert, AE zeigt „Lese <Dateiname> …“, und die Oberfläche reagiert weiter (ein Klick auf den Reiter „Messen“ wird währenddessen verarbeitet). Ein Fehler beim Lesen zeigt das Fehlerband mit dem Text des Lesers und lässt die zuvor geladene Datei unverändert.
- **UI-16 (M):** `Daten exportieren …` erzeugt über den vorhandenen Export die JSON- und NPZ-Datei im gewählten Ordner; die Meldung nennt beide Pfade; ein vorhandenes Ziel wird nicht überschrieben (Meldung des Rechenkerns).
- **UI-17 (M):** `Bild speichern …` schreibt PNG bzw. PDF der aktuellen Ansicht; im Bild steht der Stempel „Arbeitsansicht – nicht für die Thesis“ mit Dateiname, Ansicht und Git-Hash, bei unbestätigter Phase zusätzlich „enthält unbestätigte Größen (M8)“. Die Zeichenfunktion ohne Stempel (Thesis-Variante) enthält diesen Text nicht (Test: Figure-Texte).
- **UI-18 (M):** Die Zeichenfunktionen der vier Ansichten importieren weder Qt noch `pyplot` (Importtest); die Oberfläche und das Skript-Beispiel erzeugen aus denselben Daten dieselbe Linienzahl und dieselben Achsenbeschriftungen.
- **UI-19 (M):** Strg+1 … Strg+4 wechseln die Ansicht, Alt+1/Alt+2 den Reiter, Strg+Umschalt+O öffnet den Dateidialog, Strg+E exportiert, Strg+Umschalt+S speichert das Bild (QTest-Tastendrücke, Dialoge per Attrappe). F5 bis F8 sind im Reiter „Auswerten“ ohne Wirkung.
- **UI-20 (M):** Die Reiterköpfe zeigen „Messen ▶ läuft“ im Durchgang, und bei Fall 1, 4, 5 aus P3 das Zusatzwort mit Symbol („⚠ Entscheidung nötig“, „⚠ Bestätigung nötig“, „✖ Gerät unklar“); der Reiter wird nie automatisch gewechselt und der Fokus nie verschoben.
- **UI-21 (M):** Jedes bedienbare Widget hat `focusPolicy` ≠ `NoFocus`; Tab-Reihenfolge entspricht Abschnitt 8; der Fokus ist in allen Widgets (auch Plot) sichtbar (QSS-Regel `:focus`, 2 px `C_AKZENT`).
- **UI-22 (M):** Die neuen Kontrastpaare (Plotlinie/Plotfläche mindestens 3:1, Text/Hintergrund 4,5:1, `C_WARN_RAND`/`C_WARN_BG`) stehen in `KONTRAST_PAARE` und der vorhandene Kontrasttest besteht.
- **UI-23 (S):** Die Prüfzusammenfassung nennt Zählungen als Wörter („9 ok, 1 Warnung“); ein Klick öffnet die Liste P-01 bis P-11, Esc schließt.
- **UI-24 (M):** Zustände aus Abschnitt 6 sind einzeln testbar: Keine Datei, Laden, Fehler, Keine Referenz, Eingabe außerhalb, Keine Spitze gefunden. Jeder zeigt den im Brief angegebenen Text.
- **UI-25 (M):** Bei 1100×680 überlappt kein Element (Parameterzeile, Ansichtswahl, AD, AE, AF); AE ist bei 1366×768 mindestens 600×320 px groß.

### 13 Zu klärende Punkte für den Umsetzer (nicht als Annahme einführen)

- **U-1 Parameterzeile:** Der Leser (`svd_lesen.py`, `FftEinstellungen`) liefert nur `bandbreite_hz`, `linien`, `abtastfrequenz_hz`, `abtastwerte`, `delta_f_hz`; der Adapter (`svd_adapter.py`) reicht nur `fft.delta_f_hz` durch. **Mittelung** (Anzahl, Typ) und **Fenster** sind in beiden nicht belegt (im Leser keine Fundstelle). Der Umsetzer prüft, ob Mittelung und Fenster in der Datei lesbar sind. Falls nein, stehen „–“ mit Tooltip, und R-032 („mindestens Mittelung und Fenster“) ist **nicht erfüllbar**; das geht als Befund an den Nutzer (Option: Werte aus der zugehörigen `.set` oder aus dem Messprotokoll, falls vorhanden; nicht ohne Freigabe).
- **U-2 Laden ohne Einfrieren:** P3 verbietet `QThread` in der GUI. Der Umsetzer misst die Lesezeit der Beispieldatei am Messrechner und schlägt vor: (a) blockierend mit Busy-Cursor, wenn < 200 ms; (b) sonst ein Lese-Worker in einem eigenen Prozess (`concurrent.futures.ProcessPoolExecutor`) mit Abfrage per `QTimer`, ohne `QThread`. Die Entscheidung geht als Plan zur Freigabe an den Nutzer (ADR-Kandidat).
- **U-3 Spitzen und Bänder ohne Referenz:** Nach Docstring `gesamt.py` laufen Spitzensuche und Bänder je Kanalpaar mit Kreuzspektrum (|H1|). Der Umsetzer klärt, ob Band-RMS aus Amplitudenspektren (`band_amplitude`/`band_ap`) auch ohne Referenz existiert und ob die Auswertung ohne Referenz überhaupt gestartet werden kann. Vorläufige Annahme: Spitzen nur mit FRF, Band-RMS aus Amplituden bleibt.
- **U-4 Frequenzachse und Linien:** Beispieldatei laut Kontext 1600 Linien, Δf = 0,625 Hz, 0,625 … 1000 Hz; der Umsetzer prüft, ob die Anzeige bei allen Dateien die Achse des Lesers nutzt und nicht aus Bandbreite/Linien neu bildet.
- **U-5 Toolbar-Symbole:** `NavigationToolbar2QT` bringt Symboldateien mit matplotlib mit. Klären, ob das für die Auslieferung auf dem Messrechner (Wheelhouse) unproblematisch ist; sonst Textknöpfe („Zoom“, „Verschieben“, „Zurücksetzen“) als eigene Leiste über denselben Funktionen.
- **U-6 Schwingform-Ebene:** Die Voreinstellung der Projektionsebene folgt aus den Koordinaten (Ebene mit der größten Ausdehnung); Umsetzer prüft gegen die Beispieldatei, ob das stimmt.
- **U-7 Windows-Verhalten:** Tempo, HiDPI und Schriften am Messrechner prüfen (ADR-021, Hardwaretest nie als bestanden melden, bevor der Nutzer bestätigt).
- **U-8 Dämpfung aus Modenfit:** Nur ausgeben, wenn `modenfit` Bandgrenzen und Methode mitliefert; fehlen sie, bleibt die Zeile weg (R-055).

**Annahmen:**
- A-1 Die Einheit der Amplitude kommt aus der Datei bzw. dem Adapter (`einheiten`) und wird nicht umgerechnet.
- A-2 3D-Betrag und Mittel werden vom Rechenkern geliefert.
- A-3 `Auswertung.annahmen_liste` ist vor der ersten Darstellung vorhanden.
- A-4 Der Lesevorgang liefert zusammen mit den Messdaten eine `Herkunft` (Dateipfad, SHA-256).
- A-5 Die Voreinstellung der Skala ist logarithmisch für die Amplitude; Umstellung per AD.

**Offene Entscheidungen (Nutzer):**
- OE-1 Falls U-1 ergibt, dass Mittelung/Fenster nicht lesbar sind: weiter mit „–“, oder zusätzliche Quelle (.set, Protokoll)? Auswirkung: R-032 ist sonst nur teilweise erfüllt.
- OE-2 Standardskala des Spektrums: linear, logarithmisch oder dB? Auswirkung: erste Darstellung nach dem Öffnen.
- OE-3 Soll die Darstellung beim Wechsel der Datei die Auswahl (Punkt, Komponenten) behalten oder zurückstellen? Annahme: zurückstellen.

**Nicht enthalten:** Umrechnung Weg/Schnelle/Beschleunigung; Vergleich zweier Messungen; Modalanalyse über den vorhandenen Modenfit hinaus (R-054); 3D-drehbare Schwingform; Animation der Schwingform; Thesis-Abbildungen (Skripte); Bearbeiten von Messdaten; Änderungen am Reiter „Messen“ außer dem Reiterkopf-Zusatz.
