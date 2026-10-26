<!-- Paket P3 (ui-designer), Stufe 2. Status: FREIGEGEBEN vom Nutzer am 2026-10-26 (Annahmen aus Abschnitt 10 gelten). -->

## Design-Brief: Mess-Warteschlange (GUI, PySide6 / Qt Widgets, Paket U4)

**Bezug:** R-010 bis R-018, R-020 (nur Anzeige), R-021, R-030, R-031. Plan `2026-10-26_P2_architektur-prototyp.md` (Abschnitte 2, 6, 8 mit U4-1 bis U4-5). ADR-001 (PySide6 6.12.0), pytest-qt offscreen, Marker `gui`.
**Bestätigt vom Nutzer:** Grunddesign „Ja, passt so“. Editor fest rechts (kein Dialog). Abbrechen immer mit Bestätigung.

**Nutzerziel und wichtigste Aktionen:** Der Verfasser legt Messserien an, startet sie und lässt sie nacheinander laufen, teils unbeaufsichtigt, teils mit Umbau-Pausen. Kernaktionen in dieser Reihenfolge der Häufigkeit:
1. Messung und Pausenpunkt anlegen, bearbeiten, verschieben, entfernen (auch während des Laufs, nur für wartende Einträge).
2. Durchgang starten, pausieren, fortsetzen, abbrechen.
3. Auf Pausenpunkte und Fehler reagieren (ein Klick, am besten ohne Suchen).
4. Betriebsart erkennen und (selten) wechseln. Warteschlange speichern und laden.

---

### 1 Informationshierarchie und Layout

Ein Hauptfenster (`QMainWindow`), keine Menüleiste. Mindestgröße 1100×680, Zielauflösung 1366×768 und größer, Fenster frei skalierbar. Von oben nach unten:

| Zone | Inhalt | Verhalten beim Skalieren |
|---|---|---|
| A Statuszeile (schwarz, 44 px) | Betriebsart, Durchgangszustand, Verbindung/Gerät, Vermerk „Fehlerstrategie: vorläufig (O1)“, Knöpfe „Verbinden/Trennen“, „Gerät …“, „Einstellungen …“ | feste Höhe, Texte werden rechts gekürzt (Tooltip mit Volltext) |
| B Werkzeugleiste (48 px) | links Bearbeiten, rechts Ablauf | feste Höhe |
| C Hinweisband | genau ein Hinweis mit Aktionsknöpfen, sonst leer | feste Höhe 44 px, **Platz bleibt immer reserviert** (kein Springen) |
| D Warteschlangentabelle | links, Anteil 65 % | wächst mit |
| E Editor | rechts, Anteil 35 %, `QSplitter` zwischen D und E verschiebbar | wächst mit |
| F Fortschrittszeile (30 px) | Name der laufenden Messung, Balken, Text | feste Höhe |
| G Ereignisprotokoll | read-only, ca. 4 Zeilen, einklappbar nicht nötig | Mindesthöhe 4 Zeilen, wächst bis 8 |

Die Skizze liegt unter `/tmp/claude-0/-home-user/e6b61297-17fb-5003-91f8-95c4534d012c/scratchpad/p3/grunddesign.svg` (grob, nicht gerendert). Maßgeblich ist dieser Brief. Weicht die Skizze ab, gilt der Brief.

**Zone B, Anordnung links nach rechts:**
`+ Messung` · `+ Pausenpunkt` · `Entfernen` · `▲` · `▼` · `Speichern …` · `Laden …` ‖ (Abstand) ‖ `Start` · `Pausieren`/`Fortsetzen` · `Abbrechen …`.
Abbrechen steht räumlich getrennt rechts außen und hat roten Rand.

**Zone D, Spalten:** Nr (48 px) · Status (150 px) · Name (flexibel) · Einstellungsdatei (flexibel, Dateiname, Volltext im Tooltip) · Änderungen (flexibel, Kurzform) · Limit (70 px, „600 s“ bzw. „Std.“). Eine Zeile selektierbar (`SingleSelection`, ganze Zeile). Spaltenköpfe nicht sortierbar, die Reihenfolge der Warteschlange ist die Reihenfolge der Tabelle. Spaltenbreiten nicht benutzergesteuert speichern.

- **Nr** zählt nur Messungen (1, 2, 3 …) und entspricht dem Präfix `<nn>` des Dateinamens. Pausenpunkte zeigen „–“.
- **Pausenpunkt-Zeile:** Symbol ⏸ in Spalte Status, Text „Pausenpunkt: <Text>“ ab Spalte Name über die restliche Breite verbunden (`setSpan`).
- **Änderungen:** Kurzform aus dem Parameterkatalog, z. B. „Mittelung 10, Linien 1600“, „Bandbreite 1000 Hz“; „–“ wenn keine. Lange Texte mit „…“ gekürzt, Tooltip zeigt alle Parameter mit Einheit.
- **Laufende Zeile:** Hintergrund `--c-aktiv-bg`, 5 px Balken in `--c-akzent` am linken Rand, Name fett.
- **Zeile mit fehlender `.set`** (nach dem Laden): Zeichen „⚠“ vor dem Dateinamen und Tooltip „Einstellungsdatei nicht gefunden“. Start in dieser Zeile führt zu dem Fehlerfall der Vorprüfung, nicht zu einem GUI-Block.

**Zone E, Editor:** `QFormLayout`, Beschriftungen links über der Eingabe (Buddy gesetzt).

| Feld | Messung | Hinweis |
|---|---|---|
| Name | Textfeld | wird Teil des Dateinamens; unzulässig sind `\ / : * ? " < > \|` und führende/abschließende Leerzeichen; darunter schreibgeschützt „Zieldatei: 02_<Name>.svd“ |
| Einstellungsdatei (.set) | Textfeld (schreibgeschützt, Consolas) + `Wählen …` | `QFileDialog`, Filter „PSV-Einstellungen (*.set)“; zuletzt benutzter Ordner wird gemerkt |
| Geänderte Parameter | je Katalogparameter eine Zeile: Kontrollkästchen „ändern“ + Eingabe + Einheit/Bereich | nicht angehakt = Eingabe deaktiviert und zeigt „(aus .set)“; Zeilen werden **aus dem Parameterkatalog erzeugt** (`domaene/parameter.py`), nicht fest verdrahtet |
| Zeitlimit | Kontrollkästchen „eigenes Limit“ + Ganzzahlfeld + „s“ | nicht angehakt = „(Standard: 600 s)“ aus den Einstellungen |
| Notiz | mehrzeilig, 3 Zeilen | optional |

Parameter im Prototyp (Annahme aus Plan 10, O3): `fft.bandbreite_hz` (Gleitkomma, Hz), `fft.linien` (Ganzzahl), `mittelung.anzahl` (Ganzzahl, Bereich laut Katalog, erwartet 3…10000), `mittelung.typ` (Auswahlliste aus dem Katalog). Bereichsangaben immer aus dem Katalog lesen, nie in der GUI festschreiben.

**Editor für Pausenpunkt:** nur ein Textfeld „Text“ (z. B. „Sensorkopf umsetzen“), Pflichtfeld.

**Editor-Modi** (Titel in Fettdruck 11 pt):
- **Neu:** „Neue Messung“ bzw. „Neuer Pausenpunkt“ mit Zeile „wird eingefügt nach Nr 2“ (bzw. „am Anfang“, „am Ende“). Der Eintrag gelangt erst mit `Übernehmen` in die Warteschlange. Bis dahin steht nichts in der Tabelle, und `Verwerfen` bricht ohne Spur ab.
- **Bearbeiten:** „Messung 3 bearbeiten“ für Einträge im Zustand wartend.
- **Anzeigen (schreibgeschützt):** „Messung 2 (läuft)“, „… (fertig)“ usw. Alle Felder deaktiviert, zusätzlich Block mit Status, Versuch, Zeiten (soweit vorhanden), Pfad der Messdatei, bei Fehler Art und Text. `Übernehmen/Verwerfen` ausgeblendet. Hinweiszeile „Dieser Eintrag ist nicht mehr änderbar.“
- **Leer** (nichts gewählt): Text „Eintrag in der Liste wählen oder neu anlegen.“

**Einfügeposition:** direkt hinter der gewählten Zeile; ohne Auswahl am Ende. Liegt die Position vor oder in dem Bereich bereits gestarteter Einträge, wird sie auf die erste Position hinter dem letzten nicht wartenden Eintrag begrenzt (die Sitzung gibt den zulässigen Bereich an, die GUI rechnet nicht selbst).

**Zone F:** Beschriftung „Messung 2:“ (Name der laufenden Messung), `QProgressBar` (Text im Balken aus), rechts daneben der Text, siehe Zustände. Ohne Lauf: „Kein Durchgang läuft.“, Balken leer.

**Zone G:** `QPlainTextEdit`, schreibgeschützt, Consolas 9 pt, Format `HH:MM:SS  Text`. Warnungen und Fehler beginnen mit dem Wort „Warnung:“ bzw. „Fehler:“. Höchstens 1000 Zeilen. Folgt dem Ende, solange der Nutzer nicht nach oben gescrollt hat. Quelle ist die Ereigniswarteschlange der Sitzung.

---

### 2 Visuelle Richtung (Tokens)

Stil: werkzeughaft, hell, rechtwinklig. Qt-Stil `Fusion`, eigene `QPalette` plus knappes QSS (nur Farben, Fokus, Zeilenhöhen). Kein Dark Mode, keine Verläufe, keine Schatten, keine Animationen, keine Zusatzpakete oder Icon-Dateien (nur Text und Unicode-Symbole).

**Farben** (alle als benannte Konstanten in einem Modul, z. B. `gui/tokens.py`, nirgends als Literal verstreut):

| Token | Wert | Verwendung |
|---|---|---|
| `--c-bg` | `#F4F3EF` | Fensterhintergrund |
| `--c-flaeche` | `#FFFFFF` | Tabelle, Editor, Protokoll, Eingaben |
| `--c-leiste` | `#E7E5DF` | Werkzeugleiste, Tabellenkopf |
| `--c-linie` | `#C9CDD1` | Rahmen, Trennlinien (Zeilen: `#E1E3E5`) |
| `--c-rand-eingabe` | `#8A9199` | Rand von Eingaben und Knöpfen |
| `--c-text` | `#1D2327` | Haupttext |
| `--c-text-gedaempft` | `#5B6670` | Nebentext, Einheiten |
| `--c-akzent` | `#0B5C73` | Primäraktion, laufende Zeile, Fokus, Fortschritt |
| `--c-aktiv-bg` | `#DCEBF0` | Hintergrund der laufenden Zeile |
| `--c-ok` | `#1F6B3A` | Text „fertig“ |
| `--c-warn-bg` / `--c-warn-rand` | `#FFF1CC` / `#8A5A00` | Hinweisband Pausenpunkt/Warnung, Pausenpunkt-Zeile wartend |
| `--c-fehler` / `--c-fehler-bg` | `#9C1C1C` / `#FBE9E7` | Fehler, Abbrechen |
| `--c-statuszeile` | `#1D2327` mit Text `#FFFFFF` | Zone A |
| `--c-deaktiviert-text` / `-bg` | `#6B747C` / `#ECEBE6` | deaktivierte Knöpfe und Felder |

Kontrastvorgabe: Text zu Grund mindestens 4,5:1. Von Hand geschätzt (nicht mit Werkzeug gemessen): `--c-akzent` auf Weiß etwa 7,5:1, `--c-text-gedaempft` auf Weiß etwa 5,9:1, `--c-fehler` auf Weiß etwa 7,8:1. Ein Test rechnet die verwendeten Paare nach (UI-23).

**Typografie:** Fließtext Segoe UI 10 pt (Rückfall `Arial`, systemweit `QFont` mit Familienliste). Pfade und Protokoll Consolas 10 bzw. 9 pt (Rückfall `Courier New`). Titel im Editor und Dialogtitel 11 pt fett. Fett nur für Status, Titel, Primäraktionen und laufenden Namen. Ziffern in Tabelle und Fortschritt rechtsbündig. Keine Schrift unter 9 pt.

**Abstände und Maße:** 8-px-Raster. Zeilenhöhe Tabelle 32 px. Knöpfe mindestens 32 px hoch, Breite nach Text plus 16 px je Seite. Fensterrand 12 px. Eingaben 28 px hoch.

**Fokus:** Jedes bedienbare Widget zeigt bei Tastaturfokus einen 2-px-Rahmen in `--c-akzent` (QSS-Regel `:focus`). In der Tabelle zeigt die fokussierte Zeile zusätzlich eine Fokuslinie, die Auswahl bleibt auch ohne Fokus erkennbar.

**Knopfarten:**
- Primär: Rand und Text `--c-akzent` (2 px), z. B. Start, Übernehmen. Die Primäraktion im Hinweisband („Bestätigen“) ist gefüllt in `--c-akzent` mit weißem Text.
- Gefahr: Rand und Text `--c-fehler` (2 px), nur Abbrechen.
- Sekundär: Rand `--c-rand-eingabe`, Text `--c-text`.
- Deaktiviert: `--c-deaktiviert-*`, Text bleibt lesbar, **Tooltip nennt den Grund** (Beispiel: „Start nicht möglich: Betriebsart NUR LESEN führt keine Einträge aus.“).

**Symbole** (immer zusammen mit einem Wort): ○ wartend, ▶ läuft, ✔ fertig, ✖ Fehler, ■ abgebrochen, ⏸ Pausenpunkt, ⚠ Warnung. Fehlt ein Zeichen in Segoe UI, Rückfall auf die ASCII-Marken `[ ]`, `[>]`, `[ok]`, `[x]`, `[-]`, `[||]`, `[!]`. Der Rückfall ist über **eine** Tabelle in `tokens.py` umschaltbar. Ob die Zeichen am Messrechner erscheinen, wird dort geprüft (Montag, T0).

---

### 3 Komponenten, Zustände und Texte

#### 3.1 Betriebsart (Zone A, links)

Ein `QToolButton` mit Menü (`InstantPopup`) zeigt die aktuelle Betriebsart als Wort in Großbuchstaben: `SIMULATOR`, `NUR LESEN`, `TROCKENLAUF`, `MESSEN`. Menüeinträge sind die vier Betriebsarten, die aktuelle ist markiert.

| Betriebsart | Darstellung | Tooltip |
|---|---|---|
| `SIMULATOR` | weißer Text, weißer Rand 1 px auf Schwarz | „Alle Aktionen laufen gegen den Simulator. Keine Verbindung zur PSV.“ |
| `NUR LESEN` | wie oben | „Verbindung und Lesen. Es werden keine Einträge ausgeführt, nichts wird in die PSV geschrieben.“ |
| `TROCKENLAUF` | wie oben | „Einstellungen werden in die PSV geladen und gelesen, es wird nicht gescannt. Ändert die aktuellen PSV-Einstellungen.“ |
| `MESSEN` | **invertiert**: schwarzer Text auf weißer Fläche, fett | „Echte Messung. Die Freigabe gilt für diese Sitzung; jeder Durchgang braucht eine Bestätigung.“ |

- Zusätzlich steht die Betriebsart im Fenstertitel: „LDV-Warteschlange – MESSEN“.
- **Wechsel auf `MESSEN`** nur über Dialog 3.8 (Freischaltung). Bricht der Nutzer ab oder sind Voraussetzungen nicht erfüllt, bleibt die vorige Betriebsart.
- **Wechsel zwischen den anderen drei** direkt, ohne Dialog.
- **Wechsel gesperrt**, solange der Durchgangszustand nicht `BEREIT` oder `BEENDET` ist (Menü deaktiviert, Tooltip „Während eines Durchgangs nicht änderbar“).
- Nach Ende oder Abbruch eines Durchgangs in `MESSEN` fällt die Anzeige **nicht** automatisch zurück. Die Freigabe der Sitzung bleibt, die Bestätigung je Durchgang erlischt (Plan 6).

#### 3.2 Verbindung und Hilfsknöpfe (Zone A, rechts)

- Text „Simulator aktiv“ (bei `SIMULATOR`) oder „PSV <Version> verbunden · Gerät: <State>“ bzw. „PSV nicht verbunden“.
- `Verbinden` / `Trennen`: nur außerhalb von `SIMULATOR` aktiv, nicht während eines Durchgangs. In `GERAET_UNKLAR` ist `Trennen` die einzige Aktion am Gerät.
- `Gerät …` öffnet Dialog 3.10 (Anzeige), `Einstellungen …` Dialog 3.11.
- Der Vermerk „Fehlerstrategie: vorläufig (O1)“ ist immer sichtbar, Tooltip: „Verhalten bei Fehlern ist mit dem Betreuer noch zu klären (O1/F20).“

#### 3.3 Durchgangszustand und Bedienbarkeit

Statuszeile zeigt „Durchgang: <Text>“. Die Tabelle legt fest, was in jedem Zustand angezeigt wird und bedienbar ist (✓ = aktiv, – = deaktiviert mit Tooltip-Grund, ⌀ = ausgeblendet).

| Durchgangszustand | Statuszeilentext | Start | Pause/Fortsetzen | Abbrechen | Messung/Pausenpunkt anlegen | Entfernen, ▲▼, Editor-Übernehmen | Laden | Speichern | Betriebsart, Verbinden |
|---|---|---|---|---|---|---|---|---|---|
| `BEREIT` | „Bereit“ | ✓* | – (zeigt „Pausieren“) | – | ✓ | ✓ für wartende | ✓ | ✓ | ✓ |
| `LAEUFT` | „Läuft · Messung 2 von 5“ | – | ✓ „Pausieren“ | ✓ | ✓ | ✓ für wartende | – | ✓ | – |
| `PAUSE_ANGEFORDERT` | „Pause angefordert · Messung 2 läuft zu Ende“ | – | – (Beschriftung „Pause angefordert“) | ✓ | ✓ | ✓ für wartende | – | ✓ | – |
| `PAUSIERT` | „Pausiert“ | – | ✓ „Fortsetzen“ | ✓ | ✓ | ✓ für wartende | – | ✓ | – |
| `WARTET_AUF_BESTAETIGUNG` | „Wartet auf Bestätigung (Pausenpunkt)“ | – | – | ✓ | ✓ | ✓ für wartende | – | ✓ | – |
| `WARTET_AUF_ENTSCHEIDUNG` | „Wartet auf Entscheidung (Fehler)“ | – | – | ✓ | ✓ | ✓ für wartende | – | ✓ | – |
| `ABBRUCH_LAEUFT` | „Abbruch läuft …“ | – | – | – | – | – | – | ✓ | – |
| `GERAET_UNKLAR` | „Gerätezustand unklar“ | – | – | – | – | – | – | ✓ | nur `Trennen` ✓ |
| `BEENDET` | „Beendet (vollständig)“ bzw. „Beendet (abgebrochen)“ | ✓* | – | – | ✓ | ✓ für wartende | ✓ | ✓ | ✓ |

\* `Start` ist nur aktiv, wenn mindestens eine Messung wartend ist, die Betriebsart nicht `NUR LESEN` ist und (außer im `SIMULATOR`) eine Verbindung besteht. Sonst deaktiviert mit Grund im Tooltip. In `BEENDET` startet `Start` einen neuen Durchgang mit den noch wartenden Einträgen. Dafür muss die Sitzung `BEENDET → BEREIT` mit dem Start verbinden oder die GUI vorher quittieren (Abstimmung mit U2, siehe Abschnitt 8).

„✓ für wartende“: `Entfernen`, `▲`, `▼` und `Übernehmen` sind nur aktiv, wenn der gewählte Eintrag den Zustand wartend hat. `▲` ist zusätzlich deaktiviert, wenn die Zielposition vor oder in dem Bereich gestarteter Einträge läge, `▼` am Listenende. Tooltips nennen den Grund („Eintrag läuft bereits“, „Schon am Anfang der wartenden Einträge“).

**Pausieren-Knopf** wechselt die Beschriftung zwischen „Pausieren (F6)“ und „Fortsetzen (F6)“ je nach Zustand.

#### 3.4 Zeilenstatus

Spalte Status (Symbol, Leerzeichen, Wort):

| Eintrag | Zustand | Anzeige |
|---|---|---|
| Messung | wartend | `○ wartend` (bei Wiederholung `○ wartend (Versuch 2)`) |
| Messung | läuft | `▶ läuft` (fett, `--c-akzent`) |
| Messung | fertig | `✔ fertig` (`--c-ok`); im `TROCKENLAUF` `✔ fertig (Trockenlauf)` |
| Messung | Fehler | `✖ Fehler` (`--c-fehler`); nach Überspringen `✖ Fehler (übersprungen)` |
| Messung | abgebrochen | `■ abgebrochen` |
| Pausenpunkt | wartend | `⏸ Pausenpunkt` |
| Pausenpunkt | erreicht | `⏸ wartet auf Bestätigung` auf `--c-warn-bg` über die ganze Zeile |
| Pausenpunkt | erledigt | `✔ bestätigt` |

Nicht gestartete Einträge eines abgebrochenen Durchgangs bleiben `○ wartend` (Plan 2.1).

#### 3.5 Hinweisband (Zone C)

Genau **ein** Hinweis zur Zeit. Reihenfolge bei gleichzeitigen Fällen (höchste zuerst): 1 Gerät unklar, 2 Abbruch läuft, 3 PSV reagiert nicht, 4 Fehlerentscheidung, 5 Pausenpunkt, 6 Pause, 7 Durchgang beendet, 8 Betriebsart-Hinweis. Der Text trägt immer ein Symbol und ein Wort. Die Farbe verstärkt nur. Das Band ist ein eigenes Widget mit `accessibleName` „Hinweis“ und Rolle Alert (`setAccessibleDescription` mit dem Volltext). Beim Erscheinen von 4, 5 oder 1 ruft die GUI `QApplication.alert(window)` auf, damit die Taskleiste blinkt. **Der Fokus wird nie automatisch in das Band verschoben.**

| # | Fall | Aussehen | Text | Knöpfe |
|---|---|---|---|---|
| 1 | `GERAET_UNKLAR` | `--c-fehler-bg`, Rand `--c-fehler` 2 px | „✖ Gerätezustand unklar. Die PSV reagiert nicht wie erwartet. Bitte PSV am Gerät prüfen. Es werden keine weiteren Befehle an das Gerät gesendet.“ | `Verbindung trennen` |
| 2 | `ABBRUCH_LAEUFT` | `--c-warn-bg` | „⚠ Abbruch läuft … Die laufende Messung wird gestoppt.“ | – |
| 3 | Wächter (`waechter_s` im Zustandsbild gesetzt) | `--c-warn-bg` | „⚠ PSV reagiert nicht seit 45 s. Bitte am Gerät prüfen (Dialog in der PSV?).“ (Zahl live) | – |
| 4 | `WARTET_AUF_ENTSCHEIDUNG` | `--c-fehler-bg` | „✖ Messung 2 „Platte_Mitte“ fehlgeschlagen: <Fehlertext>. Vorläufiges Verhalten (O1): Durchgang angehalten.“ | `Wiederholen`, `Überspringen`, `Durchgang abbrechen …` (keiner mit Standardfokus) |
| 5 | `WARTET_AUF_BESTAETIGUNG` | `--c-warn-bg`, Rand `--c-warn-rand` 2 px | „⏸ Pausenpunkt erreicht: <Text>. Die nächste Messung startet erst nach Bestätigung.“ | `Bestätigen (F7)` (gefüllt, Akzent) |
| 6a | `PAUSE_ANGEFORDERT` | neutral `--c-leiste` | „⏸ Pause angefordert. Messung 2 läuft zu Ende, danach startet keine neue.“ | – |
| 6b | `PAUSIERT` | neutral | „⏸ Durchgang pausiert. Nächste wartende Messung: Nr 3 „Platte_Rand“.“ | `Fortsetzen (F6)` |
| 7 | `BEENDET` | neutral | vollständig: „✔ Durchgang beendet: 5 fertig.“ bzw. „… 3 fertig, 1 Fehler, 1 übersprungen.“ Abgebrochen: „■ Durchgang abgebrochen: 1 fertig, 1 abgebrochen, 3 nicht gestartet (bleiben wartend).“ | `Ordner öffnen`, `Schließen` |
| 8 | Betriebsart-Hinweis nur im `SIMULATOR` oder `TROCKENLAUF` vor dem Start | neutral | „Simulator: Es entstehen Platzhalterdateien, keine Messdaten.“ bzw. „Trockenlauf: Es wird nicht gescannt. Die aktuellen PSV-Einstellungen werden geändert.“ | – |

`Schließen` blendet den Fall 7 aus (die GUI merkt sich, dass er quittiert ist). `Ordner öffnen` ruft `QDesktopServices.openUrl` mit dem Durchgangsordner. Kein anderer Prozessaufruf.

#### 3.6 Fortschritt (Zone F)

| Zustand | Balken | Text rechts |
|---|---|---|
| kein Lauf | leer, deaktiviert | „Kein Durchgang läuft.“ |
| Messung läuft, Schätzung < 100 % | Anteil | „ca. 40 % (geschätzt) · noch ca. 2 min · Zeitlimit in 7:41“ |
| Schätzung ≥ 100 %, Messung läuft noch | 99 % | „Schätzung überschritten – Messung läuft noch · Zeitlimit in 2:10“ |
| Fortschritt nicht schätzbar (keine Punktdauer) | Balken im „unbestimmt“-Modus (Bereich 0…0) | „Fortschritt unbekannt · Zeitlimit in …“ |
| Quelle „Ereignisse“ (`--ereignisse`) | Anteil | „Punkt 4 von 9 · noch ca. …“ (dann **ohne** „geschätzt“) |
| Pausiert / wartet | letzter Stand, deaktiviert | „Zwischen den Messungen.“ |
| Messung fertig | 100 % | „Messung 2 fertig.“ |

„geschätzt“ steht in jedem Text, dessen Wert aus der Zeitschätzung stammt (U4-2). Das Wort „Zeitlimit in …“ erscheint nur, wenn die Messung ein Limit hat.

#### 3.7 Warteschlangendatei

- `Speichern …`: `QFileDialog.getSaveFileName`, Filter „Warteschlange (*.warteschlange.json)“, Standardendung ergänzt. Überschreiben fragt der Standarddialog ab (nicht deaktivieren). Nach Erfolg Protokollzeile „Warteschlange gespeichert: <Pfad>“.
- `Laden …`: `getOpenFileName`. Ist die Liste nicht leer: Rückfrage „Die aktuelle Warteschlange (n Einträge) wird ersetzt. Fortfahren?“ (`Ersetzen` / `Abbrechen`, Standard `Abbrechen`).
- Schemafehler: `QMessageBox.critical` „Datei kann nicht geladen werden“ mit dem Text der Sitzung (enthält den JSON-Pfad), Warteschlange bleibt unverändert.
- Fehlende `.set` beim Laden: Laden gelingt. Protokollzeile „Warnung: n Einstellungsdateien nicht gefunden“ und ⚠ in den betroffenen Zeilen (3.1).
- Nach dem Laden sind alle Einträge wartend (Plan 4.1).

#### 3.8 Dialog „Messen freischalten“ (Betriebsart `MESSEN`)

`QDialog`, modal, Titel „Messen freischalten“. Inhalt: Text „Damit werden echte Messungen an der PSV möglich. Jeder Durchgang braucht danach eine eigene Bestätigung.“ und eine Checkliste der Voraussetzungen (Plan 6), je Zeile Wort + Symbol:
- „✔/✖ Verbindung steht, Gerät gestoppt“
- „✔/✖ Meldungen unterdrückt (Suppress)“
- „✔/✖ Git-Hash bekannt“
- „✔/✖ Messdaten-Ordner gesetzt und beschreibbar“
- „✔/✖ Trockenlauf des ersten Eintrags ohne Abweichung in dieser Sitzung“

Sind nicht alle erfüllt, ist `Freischalten` deaktiviert, und unter jeder offenen Zeile steht die Abhilfe in einem Satz („In den Einstellungen setzen“, „Trockenlauf mit dem ersten Eintrag durchführen“). Knöpfe: `Abbrechen` (Standard, Fokus) und `Freischalten`. Die Voraussetzungen kommen aus der Sitzung, die GUI rechnet nicht selbst.

#### 3.9 Dialog „Durchgang starten“ (Bestätigung je Durchgang)

Erscheint bei `Start` in `MESSEN` (in `TROCKENLAUF` ein kurzer Hinweisdialog mit dem Satz „Ein Trockenlauf ändert die aktuellen PSV-Einstellungen. Es wird nicht gescannt.“ und den Knöpfen `Trockenlauf starten` / `Abbrechen (Standard)`; im `SIMULATOR` kein Dialog). Titel „Durchgang starten: echte Messung“.
Inhalt: „<n> Messungen, <m> Messpunkte insgesamt (soweit bekannt)“, darunter Tabelle: Nr · Einstellungsdatei · Zieldatei · Messpunkte. Danach Block „Generator (gelesen): GeneratorsOn: <ja/nein>, Aktiv: <…>, Amplitude: <… V>“. Ist der Generator aktiv: zusätzlich Zeile `--c-fehler`: „✖ Generator ist aktiv. Die Messung startet ihn automatisch. Nur fortfahren, wenn Shaker/Verstärker freigegeben sind.“
Bestätigung: Eingabefeld „Zur Bestätigung MESSEN eintippen“. `Messung starten` ist erst aktiv, wenn der Text genau `MESSEN` lautet (Groß-/Kleinschreibung exakt). Standardfokus auf `Abbrechen`. Der Dialog bleibt in der Reihenfolge der Tabelle konsistent mit der Warteschlange zum Startzeitpunkt (Schnappschuss).

#### 3.10 Dialog „Gerät“

Schreibgeschützte Anzeige in Form-Layout aus dem Zustandsbild: PSV-Version, Modus, Gerätezustand (State), Meldungen unterdrückt, Hardware-Kennungen, Messpunkte. Nicht verbunden: „Nicht verbunden.“ Knopf `Schließen`. Inhalt für T1 am Montag (NUR_LESEN).

#### 3.11 Dialog „Einstellungen“

Zwei Felder: „Messdaten-Ordner“ (Pfad + `Wählen …`, `QFileDialog.getExistingDirectory`) und „Standard-Zeitlimit“ (Ganzzahl, s; Startwert 600 laut Plan-Annahme). Knöpfe `Übernehmen` / `Abbrechen`. Der Ordner liegt nicht in Polytec-Verzeichnissen und nicht im Repository. Die Prüfung dazu macht die Sitzung, die GUI zeigt deren Meldung unter dem Feld (`✖ …`).

#### 3.12 Abbrechen-Dialog

Auslöser: Knopf `Abbrechen …`, F8, `Durchgang abbrechen …` im Band. `QMessageBox`, Standardknopf und Fokus auf dem sicheren Knopf.
- Läuft eine Messung: Titel „Durchgang abbrechen?“, Text „Die laufende Messung wird sofort gestoppt. Bereits gemessene Punkte bleiben in der Datei. Nicht gestartete Messungen bleiben wartend.“ Knöpfe `Durchgang abbrechen` (Rolle Destructive) und `Weiter messen` (Standard).
- Läuft keine Messung (pausiert, Pausenpunkt, Fehler): Text „Der Durchgang wird beendet. Nicht gestartete Messungen bleiben wartend.“ Knöpfe `Durchgang abbrechen` und `Zurück` (Standard).
Der Befehl wird erst nach der Bestätigung genau einmal an die Sitzung gegeben.

#### 3.13 Fenster schließen

Während `LAEUFT`, `PAUSE_ANGEFORDERT`, `ABBRUCH_LAEUFT` wird das Schließen verhindert (Hinweis: „Es läuft ein Durchgang. Bitte zuerst abbrechen oder warten.“). In `GERAET_UNKLAR` ist Schließen erlaubt, mit Warnung „PSV vorher prüfen.“ In allen anderen Zuständen: hat die Warteschlange ungespeicherte Änderungen (nicht leer, seit Speichern/Laden geändert), fragt ein Dialog `Speichern` / `Verwerfen` / `Abbrechen` (Standard `Abbrechen`).

---

### 4 Interaktion und Nebenläufigkeit

- Die GUI spricht **ausschließlich** mit der Sitzungsfassade. Sie holt `Zustandsbild` und Ereignisse mit einem `QTimer` (100 ms) **im GUI-Thread** ab und ruft nie selbst in den Geräte-Thread. Ein einziger Aktualisierungspfad schreibt alle Zonen aus dem gleichen `Zustandsbild` neu (kein verteilter Zustand in Widgets).
- Aktualisierung darf nicht ändern: Auswahl der Tabelle, Scrollposition, Fokus, ungespeicherte Eingaben im Editor. Der Editor merkt sich seine Eingaben als „geändert“, bis `Übernehmen`/`Verwerfen`.
- Ändert sich der gewählte Eintrag während der Bearbeitung zu „nicht wartend“ (Messung startete), wechselt der Editor in den Anzeigemodus. Ein roter Hinweis zeigt „✖ Der Eintrag wurde inzwischen gestartet. Deine Änderungen wurden nicht übernommen.“ mit Knopf `Eingaben verwerfen`. Das gilt auch, wenn `Übernehmen` an einem `ValueError` der Sitzung scheitert: Text der Sitzung im Editor anzeigen.
- Nicht erlaubte Operationen durch eine Race (Sitzung wirft `ValueError`/`IndexError`) zeigt die GUI als `QMessageBox.warning` mit dem Text der Sitzung. Es gibt keinen stillen Fehlschlag.
- Eingabevalidierung im Editor ist **sofort** (bei Eingabe) und **inline** unter dem Feld: „✖ Mittelung Anzahl: 2 liegt außerhalb 3 … 10000.“ in `--c-fehler`. `Übernehmen` ist bis zur Korrektur deaktiviert (Tooltip: „Eingaben prüfen: <erster Fehler>“). Maßgeblich ist der Katalog, die Sitzung validiert erneut.
- Drag-and-drop (Kann): internes Verschieben in der Tabelle, nur für wartende Einträge, nur an zulässige Positionen, Ergebnis identisch zu `▲/▼`. Fehlt die Zeit, entfällt es ersatzlos.
- Sitzungsbefehle werden pro Bedienung genau einmal abgesetzt (kein Doppelklick-Effekt: Knopf nach Klick bis zum nächsten Zustandsbild deaktivieren).

### 5 Tastaturbedienung

| Taste | Aktion | Bedingung |
|---|---|---|
| F5 | Start | wie Knopf |
| F6 | Pausieren / Fortsetzen | wie Knopf |
| F7 | Pausenpunkt bestätigen | nur wenn Fall 5 im Band steht |
| F8 | Abbrechen (mit Dialog 3.12) | wie Knopf |
| Strg+N | neue Messung (Editor „Neu“, Fokus auf Name) | wie Knopf |
| Strg+Umschalt+N | neuer Pausenpunkt | wie Knopf |
| Entf | gewählten Eintrag entfernen (ohne Rückfrage, siehe Annahmen) | Fokus in der Tabelle |
| Alt+↑ / Alt+↓ | Eintrag nach oben/unten | Fokus in der Tabelle |
| ↑ / ↓ / Pos1 / Ende | Auswahl in der Tabelle | Fokus in der Tabelle |
| Enter | Fokus in den Editor (erstes Feld) | Fokus in der Tabelle |
| Strg+Enter | `Übernehmen` | Fokus im Editor |
| Esc | `Verwerfen`, danach Fokus zurück zur Tabelle | Fokus im Editor |
| Strg+S / Strg+O | Speichern / Laden | wie Knöpfe |

Alle Knöpfe zeigen ihre Taste in der Beschriftung oder im Tooltip. Aktionen sind als `QAction` mit `Qt.WindowShortcut` angelegt, damit Knopf, Taste und Aktivierungszustand dieselbe Quelle haben. Tabulatorreihenfolge entspricht der visuellen: Zone A → B → C → D → E → G (F nicht fokussierbar). Dialoge: Tab-Reihenfolge von oben nach unten, Esc schließt wie `Abbrechen`, **kein** Dialog der Gefahr-Klasse hat den Gefahr-Knopf als Standard.

### 6 Responsives Verhalten

Desktop-Anwendung, kein Handy-Layout. Mindestgröße 1100×680. Unter 1366 Breite schrumpft zuerst die Spalte „Einstellungsdatei“, dann „Änderungen“ (Kürzen mit „…“, Tooltip). Der Editor hat Mindestbreite 340 px, ab dort wird der Teiler gesperrt. Bei 1366×768 sind in der Tabelle mindestens 10 Zeilen sichtbar, bei größerer Höhe wächst die Tabelle, nicht das Protokoll über 8 Zeilen. Skalierung (Windows 125/150 %) über Qt-Hochskalierung, Maße in logischen Pixeln.

### 7 Accessibility

- Jede Eingabe hat Beschriftung mit Buddy (`QLabel.setBuddy`). Knöpfe tragen sprechenden Text (keine reinen Symbole: `▲`/`▼` bekommen `accessibleName` „Eintrag nach oben/unten“ und Tooltip).
- Farbe ist nie alleiniger Träger (Symbol + Wort für Status, Betriebsart als Wort, Fehler mit „✖“ und Text).
- Kontrast 4,5:1 für Text, 3:1 für Rahmen und Fokus. Deaktivierte Elemente bleiben lesbar.
- Sichtbarer Fokus überall (2 px Akzent). Keine zeitgesteuerten Hinweise, die verschwinden (Hinweise bleiben bis zur Auflösung).
- Statusänderungen, die eine Entscheidung brauchen (Fälle 1, 4, 5), setzen `accessibleDescription` am Band und rufen `QApplication.alert` auf.
- Tooltips sind Ergänzung, nie einziger Ort für eine Information, die man zum Bedienen braucht (Ausnahme: Grund für deaktivierte Knöpfe, zusätzlich im Protokoll bei Klick-Versuch nicht nötig).
- Alle Texte Deutsch, „Sie“ wird vermieden (neutrale Formulierungen), Einheiten mit Leerzeichen („1000 Hz“, „600 s“).

### 8 Technische Hinweise für U4

- Ablage: `software/src/ldv_automation/gui/` (z. B. `hauptfenster.py`, `tabelle.py`, `editor.py`, `hinweisband.py`, `dialoge.py`, `tokens.py`, `stil.py` mit Palette und QSS). `__main__.py` startet `python -m ldv_automation gui`.
- Abhängigkeitsrichtung: `gui` importiert nur `sitzung` und `domaene`, kein `geraet`, `ablauf`, `protokoll`, `persistenz`, kein `win32com` (Plan 1; Importtest).
- Neue Abhängigkeit: nur `PySide6==6.12.0` (und für Tests `pytest-qt`), Marker `gui` in `pyproject.toml`, Tests laufen mit `QT_QPA_PLATFORM=offscreen` und werden standardmäßig nicht ausgeführt. Kein Qt Designer, keine `.ui`/`.qrc`-Dateien, keine Bilddateien.
- **Von der Sitzung benötigtes `Zustandsbild`** (mit U2 abstimmen, falls nicht vorhanden): Durchgangszustand; Betriebsart; Verbindungsinfo (Version, State, Suppress, Hardware, Messpunkte); je Eintrag Art, ID, Name, Einstellungsdatei, Parameter, Limit, Zustand, Versuchszähler, Fehlertext, Zeiten, Messdateipfad, Kennzeichen „übersprungen“, „Trockenlauf“, „.set fehlt“, Messungsnummer; Fortschritt (Anteil oder unbestimmt, Quelle, Restzeit, Zeitlimit-Rest, laufende Messung); `waechter_s` (None oder Sekunden); Fehlerentscheidung angeboten (ja/nein, Text); Durchgangsordner; Zusammenfassung bei `BEENDET`; Voraussetzungen für `MESSEN` einzeln; zulässiger Einfügebereich. Fehlen Felder, nennt der Umsetzer das als Rückfrage und baut keine Ersatzlogik in die GUI.
- **Befehle**, die die GUI braucht: Eintrag einfügen/ändern/entfernen/verschieben, Start, Pause, Fortsetzen, Abbrechen, Pausenpunkt bestätigen, Fehlerentscheidung (Wiederholen/Überspringen/Abbrechen), Betriebsart setzen (MESSEN nur nach Freischaltung), Durchgang bestätigen (Messfreigabe), Verbinden/Trennen, Warteschlange speichern/laden, Einstellungen setzen, Durchgang quittieren (`BEENDET → BEREIT`).
- Testbarkeit: stabile `objectName`s: `statuszeile`, `btn_betriebsart`, `lbl_durchgang`, `lbl_verbindung`, `werkzeugleiste`, `btn_messung_neu`, `btn_pausenpunkt_neu`, `btn_entfernen`, `btn_hoch`, `btn_runter`, `btn_speichern`, `btn_laden`, `btn_start`, `btn_pause`, `btn_abbrechen`, `hinweisband` (mit `property("fall")` = Nummer aus 3.5), `btn_band_*`, `tabelle`, `editor`, `btn_uebernehmen`, `btn_verwerfen`, `fortschritt_balken`, `fortschritt_text`, `protokoll`.
- Die GUI-Logik (Aktivierungstabelle 3.3, Bandfall-Auswahl 3.5, Fortschrittstext 3.6, Zeilenstatus 3.4, Kurzform der Änderungen) steht in **reinen Funktionen** ohne Qt-Abhängigkeit, die ein `Zustandsbild` auf Anzeigewerte abbilden. Sie lassen sich ohne Qt testen und vermeiden Zufallsabhängigkeit in den Widget-Tests.
- Kein neuer Stil als Zusatzabhängigkeit, keine Verwendung von `QThread` in der GUI.

**Streichreihenfolge bei Zeitnot** (konsistent mit Plan 8): 1 Drag-and-drop; 2 Speichern/Laden-Rückfragen und Schließen-Dialog (3.13, bis auf das Sperren im Lauf); 3 Einstellungsdialog, Messdaten-Ordner dann nur über Kommandozeilenoption/Konfiguration; 4 Hinweisband-Fall 7 (Zusammenfassung) auf eine Zeile ohne Knöpfe; 5 Fortschrittsvarianten „unbestimmt“. **Nie streichen:** Betriebsart-Anzeige, Dialoge 3.8/3.9/3.12, Hinweisband-Fälle 1 bis 5, Zeilenstatus mit Symbol und Wort, „geschätzt“-Kennzeichnung, Sperrlogik der Knöpfe.

---

### 9 UI-Akzeptanzkriterien

Priorität: M = muss für Montag, S = soll, K = kann. Alle gegen den `SIMULATOR` und `Zustandsbild`-Attrappen, ohne Hardware.

- **UI-1 (M, U4-5, R-030):** Bei leerer Warteschlange zeigt die Tabelle den Text „Noch keine Messung. Mit „+ Messung“ anlegen oder eine Warteschlange laden.“ ; `btn_start` ist deaktiviert mit Tooltip-Grund; Statuszeile zeigt „Bereit“; das Hinweisband ist leer, belegt aber weiterhin seine Höhe von 44 px.
- **UI-2 (M, R-012, R-030):** `Strg+N` öffnet den Editor im Modus „Neu“ mit Fokus im Feld Name. Mit gültigem Namen und gewählter `.set` fügt `Übernehmen` die Messung direkt hinter der gewählten Zeile (ohne Auswahl am Ende) ein, selektiert sie und zeigt `○ wartend`. `Verwerfen` bzw. `Esc` fügt nichts ein.
- **UI-3 (M, R-013, R-015):** `Entfernen`, `▲`, `▼` sind nur bei gewähltem wartendem Eintrag aktiv. Bei laufendem, fertigem, fehlerhaftem oder abgebrochenem Eintrag sind sie deaktiviert, und der Tooltip nennt den Grund. `▲` am Anfang des wartenden Bereichs und `▼` am Ende sind deaktiviert. `Alt+↑`/`Alt+↓` und `Entf` bewirken dasselbe wie die Knöpfe.
- **UI-4 (M, R-014, R-016):** Ein wartender Eintrag lässt sich im Editor ändern, und `Übernehmen` aktualisiert die Tabellenzeile (Name, Änderungen, Limit). Das gilt auch, während ein Durchgang läuft. Ein laufender oder abgeschlossener Eintrag öffnet den Editor im Anzeigemodus (alle Felder deaktiviert, Hinweis „Dieser Eintrag ist nicht mehr änderbar.“).
- **UI-5 (M, U1-3):** Die Eingabe `2` in „Mittelung Anzahl“ zeigt sofort unter dem Feld eine Meldung mit Schlüssel und Bereich aus dem Katalog („… liegt außerhalb 3 … 10000“), und `Übernehmen` ist deaktiviert. Unzulässige Zeichen im Namen (`\ / : * ? " < > |`) verhindern `Übernehmen` mit Meldung. Die Parameterzeilen entstehen aus dem Katalog: ein im Test ergänzter Katalogeintrag erscheint ohne GUI-Änderung.
- **UI-6 (M, R-017):** `Strg+Umschalt+N` legt einen Pausenpunkt mit Pflichttext an. Er erscheint als Zeile mit ⏸, ohne Nr, mit dem Text über die Breite, lässt sich bearbeiten, verschieben und entfernen wie eine Messung. Leerer Text deaktiviert `Übernehmen`.
- **UI-7 (M, R-031, U4-2):** Für jeden Zustand aus 3.4 enthält die Statuszelle Symbol und Wort (Textvergleich im Test, nicht Farbe). Alle fünf Messungszustände und die drei Pausenpunktzustände sind in einer Testwarteschlange gleichzeitig darstellbar.
- **UI-8 (M, R-031, U4-2):** Während `LAEUFT` zeigt `fortschritt_text` Prozent und das Wort „geschätzt“ (Quelle Zeitschätzung) und `fortschritt_balken` einen Wert > 0; Statuswechsel einer Zeile erscheinen spätestens 300 ms nach dem Zustandsbild. Ohne Lauf lautet der Text „Kein Durchgang läuft.“ Bei Schätzung ≥ 100 % lautet der Text „Schätzung überschritten – Messung läuft noch …“ und der Balken zeigt 99 %.
- **UI-9 (M, R-018, U4-5):** Die Aktivierung von Start, Pausieren/Fortsetzen und Abbrechen entspricht in allen neun Durchgangszuständen exakt der Tabelle 3.3 (parametrisierter Test). Der Pausieren-Knopf trägt in `PAUSIERT` die Beschriftung „Fortsetzen“ und in `PAUSE_ANGEFORDERT` „Pause angefordert“ (deaktiviert).
- **UI-10 (M, R-018):** `Abbrechen` (Knopf, F8, Band) öffnet Dialog 3.12 mit Standardfokus auf „Weiter messen“ bzw. „Zurück“. Erst nach „Durchgang abbrechen“ geht genau ein Abbruchbefehl an die Sitzung. Esc im Dialog sendet nichts.
- **UI-11 (M, R-017, U4-5):** Im Zustand `WARTET_AUF_BESTAETIGUNG` zeigt das Band Fall 5 mit dem Pausenpunkt-Text und dem Knopf `Bestätigen`; die Zeile ist `⏸ wartet auf Bestätigung`. Klick und F7 senden jeweils genau einen `bestaetigen`-Befehl. F7 hat außerhalb dieses Zustands keine Wirkung. Der Fokus wurde beim Erscheinen nicht verschoben.
- **UI-12 (M, R-019 vorläufig, U4-5):** Im Zustand `WARTET_AUF_ENTSCHEIDUNG` zeigt das Band Fall 4 mit Messungsnummer, Name, Fehlertext und den Knöpfen `Wiederholen`, `Überspringen`, `Durchgang abbrechen …`; jeder sendet die zugehörige Fehlerentscheidung (das dritte erst nach Dialog 3.12). Kein Knopf hat Standardfokus. „vorläufig (O1)“ ist im Band und in der Statuszeile sichtbar.
- **UI-13 (M, U4-5):** Zustände `PAUSE_ANGEFORDERT` und `PAUSIERT` zeigen die Bandfälle 6a bzw. 6b mit den Texten aus 3.5; `Fortsetzen` im Band entspricht F6.
- **UI-14 (M, U4-3):** Die Betriebsart ist in allen Durchgangszuständen als Wort in Zone A und im Fenstertitel sichtbar. `MESSEN` ist invertiert dargestellt. Die Wahl von `MESSEN` im Menü ändert die Betriebsart nicht, bevor Dialog 3.8 mit `Freischalten` bestätigt wurde. Bei unerfüllten Voraussetzungen ist `Freischalten` deaktiviert, und die Abhilfe steht unter der Zeile. Der Wechsel ist in laufenden Durchgängen gesperrt.
- **UI-15 (M, U4-3):** `Start` in `MESSEN` öffnet Dialog 3.9 mit Messungsliste (Einstellungsdatei, Zieldatei, Messpunkte) und Generatorangabe. `Messung starten` ist nur bei exakt `MESSEN` im Eingabefeld aktiv, Standardfokus liegt auf `Abbrechen`. Ohne Bestätigung wird kein Startbefehl gesendet. Ist der Generator aktiv, steht die rote Warnzeile im Dialog. In `SIMULATOR` erscheint kein Dialog, in `TROCKENLAUF` der Hinweisdialog.
- **UI-16 (M, U4-4):** Meldet das `Zustandsbild` `waechter_s` (simulierter hängender Aufruf), zeigt das Band innerhalb von 1 s „PSV reagiert nicht seit N s …“ mit laufender Zahl, und gleichzeitig verarbeitet die GUI weiter Eingaben (im Test: ein Klick auf `btn_messung_neu` öffnet den Editor in dieser Zeit).
- **UI-17 (M):** Im Zustand `GERAET_UNKLAR` zeigt das Band Fall 1 mit dem Knopf `Verbindung trennen`. Außer diesem Knopf und `Speichern …` ist alles deaktiviert. Fall 1 hat Vorrang vor allen anderen Hinweisen (Prioritätstest mit zwei gleichzeitigen Fällen).
- **UI-18 (S):** Im Zustand `BEENDET` zeigt das Band die Zusammenfassung mit den Zählern je Zustand; `Schließen` blendet es aus; `Ordner öffnen` nutzt den Durchgangsordner. `Start` startet nur noch die wartenden Einträge.
- **UI-19 (M, U4-1, R-030):** Alle Funktionen R-010 bis R-018 und R-021 sind ohne Kommandozeile über die Oberfläche erreichbar (Handtest-Checkliste im Simulatorbetrieb, jede Funktion einmal; ergänzt durch Smoke-Tests mit Marker `gui`).
- **UI-20 (S, R-021):** `Speichern …` und `Laden …` führen einen Rundlauf aus (gleiche Einträge, gleiche Reihenfolge, alle wartend). Eine Datei mit unbekanntem Schlüssel zeigt einen Fehlerdialog mit JSON-Pfad, die Warteschlange bleibt. Laden bei nicht leerer Liste fragt nach (Standard `Abbrechen`). Eine fehlende `.set` erzeugt ⚠ in der Zeile und eine Protokollzeile.
- **UI-21 (M):** Alle Kernaktionen sind ohne Maus ausführbar: Tastenbelegung aus Abschnitt 5 löst jeweils die Aktion aus (QTest-Tastendrücke), in der Tabelle sind ↑/↓ und Pos1/Ende wirksam, `Enter`/`Strg+Enter`/`Esc` wechseln zwischen Tabelle und Editor. Jedes bedienbare Widget hat `focusPolicy` ≠ `NoFocus`. Das QSS enthält eine `:focus`-Regel mit 2 px `--c-akzent`; die Tabulatorreihenfolge entspricht Abschnitt 5.
- **UI-22 (M):** Eine Aktualisierung des `Zustandsbild` (auch viele kurz hintereinander) ändert weder die Auswahl noch die Scrollposition noch ungespeicherte Eingaben im Editor. Ändert sich der gewählte Eintrag während der Bearbeitung auf „läuft“, wechselt der Editor in den Anzeigemodus und zeigt die Meldung aus Abschnitt 4 mit `Eingaben verwerfen`.
- **UI-23 (S, Barrierefreiheit):** Ein Test berechnet für die Paare Text/Hintergrund aus den Tokens (`--c-text`/`--c-flaeche`, `--c-text-gedaempft`/`--c-flaeche`, `--c-text-gedaempft`/`--c-bg`, `--c-akzent`/`--c-flaeche`, `--c-akzent`/`--c-aktiv-bg`, `--c-fehler`/`--c-fehler-bg`, `--c-ok`/`--c-flaeche`, `--c-text`/`--c-warn-bg`, Weiß/`--c-statuszeile`, Weiß/`--c-akzent`) ein Kontrastverhältnis ≥ 4,5:1.
- **UI-24 (M):** Fenster-Mindestgröße 1100×680. Bei 1366×768 sind mindestens 10 Tabellenzeilen sichtbar, und kein Bedienelement ist abgeschnitten (Offscreen-Prüfung der Widgetgeometrie).
- **UI-25 (S):** `Gerät …` zeigt Version, Modus, State, Suppress, Hardware und Messpunkte aus dem `Zustandsbild` bzw. „Nicht verbunden.“. `Einstellungen …` setzt Messdaten-Ordner und Standard-Zeitlimit; Fehlermeldungen der Sitzung erscheinen unter dem Feld.
- **UI-26 (S):** Beim Schließen des Fensters während `LAEUFT`, `PAUSE_ANGEFORDERT` oder `ABBRUCH_LAEUFT` bleibt das Fenster offen und zeigt den Hinweis aus 3.13. Bei ungespeicherter Warteschlange fragt der Dialog `Speichern`/`Verwerfen`/`Abbrechen`.
- **UI-27 (K):** Drag-and-drop in der Tabelle verschiebt wartende Einträge mit demselben Ergebnis wie `▲/▼`. Auf nicht wartende Einträge oder vor sie ist kein Ablegen möglich.
- **UI-28 (M, Architektur):** Importtest: `gui/*` importiert nur `sitzung` und `domaene` (plus Qt/stdlib); die GUI startet keinen eigenen Thread, ruft nie `geraet.*`/`ablauf.*` und nutzt für Aktualisierung nur den `QTimer`.

---

### 10 Annahmen

- Alle Anzeigewerte kommen aus dem `Zustandsbild` der Sitzung. Die Felder in Abschnitt 8 existieren oder werden in U2 ergänzt.
- Nr in der Tabelle = Messungsnummer = Dateipräfix `<nn>`; Pausenpunkte zählen nicht mit.
- Entfernen ohne Rückfrage ist akzeptabel (Wiederherstellung über Speichern/Laden bzw. Neuanlage).
- Laden ersetzt die Warteschlange (Anfügen nicht im Umfang).
- Standard-Zeitlimit 600 s stammt aus der Annahme des Plans (nicht belegt), Bereich des Zeitlimitfeldes: ganze Zahl ≥ 1.
- Fortschritt, Wächter und Bandfälle entsprechen dem freigegebenen Plan (Abschnitte 2.3, 2.5, 2.6, 5.3, 6).
- Segoe UI und die verwendeten Unicode-Symbole sind am Messrechner vorhanden. Sonst Rückfall auf ASCII-Marken über `tokens.py`.
- Kontrastwerte in Abschnitt 2 sind von Hand geschätzt, der Test UI-23 ist maßgeblich.

### 11 Offene Entscheidungen

1. **Entfernen ohne Rückfrage** (Annahme) oder mit Rückfrage? Auswirkung: ein Dialog mehr, dafür weniger Fehlbedienung.
2. **Betriebsart-Auswahl als Menü** (Annahme) oder als eigener Knopf je Betriebsart? Auswirkung nur Gestaltung.
3. **Start in `BEENDET`**: neuer Durchgang direkt oder erst Quittieren? Auswirkung auf U2/`sitzung.py` (ein Befehl).
4. **Anzeige „Trockenlauf“ als fertig** (`✔ fertig (Trockenlauf)`) oder eigener Status? Auswirkung auf Zustandsmodell (Plan 2.1 kennt nur fünf).
5. **Messdaten-Ordner**: Einstellungsdialog (Annahme) oder nur Konfiguration? Auswirkung: Aufwand U4.

### 12 Nicht enthalten

Dark Mode, Mehrsprachigkeit, Duplizieren von Einträgen, Mehrfachauswahl, Anfügen beim Laden, Rückgängig/Wiederholen, grafische Darstellung der Messdaten oder Spektren, Live-Anzeige einzelner Messpunkte, Erkundungs-/Konfigurationsoberfläche für COM-Schalter (Validator, Lademaske), Anzeige des Messprotokolls im Programm (nur Pfad), Benachrichtigungen per Ton, eigene Icons, Menüleiste.
