<!-- Vom Nutzer am 2026-11-09 freigegeben: Etappen A → B → C mit Prüfpunkten nach S3, S7, S9; F3 (Zoom schreibt feste Werte, Zurücksetzen = Auto) bestätigt; Annahmen F1, F2, F4–F11 übernommen; Arbeitsspeicher des Messrechners unbekannt, Grenze 4 Messungen als Annahme, am Messrechner prüfen. -->

<!-- Paket P-AUSW2 (software-engineer), Typ Planung. Status: PLAN ZUR FREIGABE (2026-11-09). Es wurde nichts am Repository geändert außer dieser Datei. Messungen: Linux-Container (4 Kerne, 16 GB, Python 3.11, Agg ohne Qt), am Messrechner nicht bestätigt. -->

## Plan: R-073 Achsen, R-058 Vergleich, R-059 eigene Diagramme (Paket P-AUSW2, Typ Planung)

Grundlage: freigegebener Brief `2026-11-09_K1-AUSW2_design-brief.md` (UI-1 bis UI-21, UI-34 bis UI-37 sind Akzeptanzkriterien dieses Plans; UI-38 ist Hardwaretest), Lastenheft R-058/R-059/R-073, KONVENTIONEN, ADR-021, 022, 024, 025, 026, 027. R-071 (Animation) ist nicht Teil; Abschnitt 8 nennt nur die Andockstellen.

### 0 Kernbefunde

1. **Der Reiter ist auf genau eine Messung gebaut.** `auswerten_reiter.py` (2127 Zeilen) hält `_geladen`, `_cache`, `_datei_pfad`, `_pruefung`, `_antrieb` je 1x und nutzt sie an rund 65 Stellen; Tests greifen an 8 Stellen darauf zu. Eine Neuschreibung wäre riskant, **Eigenschaften, die an die aktive Messung delegieren**, halten den Diff klein.
2. **Der Zoom hat heute zwei Quellen** (`PlotFlaeche._zoom` nur x, `_standard_grenzen`, `bild_grenzen()` für das Arbeitsbild). Der Brief verlangt eine Quelle (R-073). Das ist der **riskanteste Umbau**: er berührt Cursor, Werkzeugleiste (`push_current`, `home`), Neuzeichnen bei Größenänderung und das Arbeitsbild.
3. **Die Zeichenschicht kennt keine Achsenwahl.** `zeichne_spektrum`/`zeichne_frf`/`zeichne_spitzen` setzen x immer auf den Datenbereich, y per Autoskalierung, Skala nur über `Optionen.skala`. Frequenz logarithmisch, feste Grenzen und Phase in Grad (heute fest ±180°) fehlen.
4. **Speicher je Messung ist gemessen** (Abschnitt 3): rund 58 MiB für `Geladen` plus rund 28 MiB je gehaltenes Kanalpaar. Vier Messungen sind im Hauptprozess machbar, die LRU des `PaarCache` (2 Paare) ist für Ansicht 5 zu klein.
5. **Zeichnen ist schnell genug** (gemessen, Agg, constrained layout, Legende unten): 1 Teilbild/2–4 Linien 90–140 ms, 2 Teilbilder 120–150 ms, 4 Teilbilder/4 Linien 230–320 ms (erstes Zeichnen im Prozess ca. 1 s). Das Ziel der Oberfläche (unter 400 ms je Wechsel, ADR-022 Nachtrag) ist erreichbar; Qt-Canvas und Remotedesktop am Messrechner sind ungemessen.
6. **Der Brief ist an drei Stellen auslegungsbedürftig** (Abschnitt 9): Teilbild-Regel im Modus „nebeneinander“, Wirkung von Zoom/Zurücksetzen auf die Felder, y-Bereich je Größe in Ansicht 5. Für alle gibt es eine Annahme, keine Frage blockiert den Start von Etappe A.

### 1 Bestandsaufnahme (wiederverwendbar / zu ändern)

| Baustein | Stand | Verwendung |
|---|---|---|
| `darstellung/auswahl.py` (`PaarCache`, `spektrum_daten`, `frf_daten`, `kanalpaare`, `verfuegbare_groessen`, `DarstellungsFehler`) | GUI-frei, je Aufruf eine `Messdaten` | **wiederverwendet**: Serien werden daraus aufgelöst, keine neue Mathematik. Mittelformeln und Punktzahlen (`mittelformel`, `punktzahl_text`) liegen schon vor (UI-11). |
| `darstellung/zeichnung.py` (`Zeichnung`, `setze_achsenstil`, `constrained_layout`, `kennzeichen_*`) | gemeinsame Bausteine | erweitert: `Ansicht.DIAGRAMM = 5`, Feld `Zeichnung.rollen` (Rolle der y-Achse je Achse), Legende-unten hochgezogen |
| `darstellung/spitzen.py::_legende` | Legende unter der Achse (rect-treu im Arbeitsbild; `fig.legend(loc="outside lower center")` ignoriert den `rect`) | **Muster für Ansicht 5**; nach `zeichnung.py` hochziehen, `spitzen.py` ruft die gemeinsame Funktion (Verhalten gleich, vorhandene Tests sichern) |
| `darstellung/stil.py` (`Plotstil.linienart(i)`, `serienfarbe(i)`, 4 Linienarten) | paarweise verschieden | **wiederverwendet** (UI-18, UI-20) |
| `darstellung/bild.py` (`baue_stempel`, `speichere_arbeitsbild`) | Stempel mit einem Dateinamen | erweitert um mehrere Dateien (abwärtskompatibel) |
| `gui/plotflaeche.py` | `ZEICHNER`-Tabelle je Ansicht, `_zoom`, Toolbar, Cursor | erweitert um Ansicht 5, Zoom-Quelle ersetzt (Schritt 2) |
| `gui/arbeitsbild.py::bild_grenzen` | Zoom nur bei Abweichung übernehmen | entfällt, wenn Grenzen in den Optionen stehen (Schritt 2) |
| `gui/anzeige_auswerten.py` (`ANSICHT_NAMEN`, `FREIGESCHALTETE_ANSICHTEN`) | Ansichtsregister, Knopfzeile iteriert darüber | Eintrag 5; `_baue_ansichtswahl` braucht keine Änderung |
| `gui/anzeige_aktionen.py` (`AKTIONS_TASTEN`, `bild_unbestaetigt`, `stempel_ansicht`) | eine Quelle der Tasten | `ansicht_5: Strg+5`, `bild_unbestaetigt` für Ansicht 5 |
| `auswertung/jobs.py` (`lese_job`, `pruef_job`), `hintergrund.py`, ADR-022 | Stufe A je Datei, Stufe B 8–13 s | **wiederverwendet**: je Messung ein Stufe-A-Auftrag, Stufe B nur bei Bedarf |
| `gui/auswerten_reiter.py` `_abfrage`/`oeffne_datei`/`_uebernehme` | eine Job-ID für alles | `_abfrage` bekommt eine Auftragsliste (Schritt 5) |
| `gui/tokens.py` (`PLOT_SERIENFARBEN`, `PLOT_LINIENARTEN`, `KONTRAST_PAARE`) | Serienfarben und Kontrasttest | neue Paare für Feld „fest“, aktiven Chip |
| Tests: `tests/gui/gui_ausw_hilfen.py` (`synth_geladen`: P=4, K=64 fest, Attrappen-Ausführer) | | `synth_geladen` bekommt Parameter für Punktzahl, Linienzahl, Labels (UI-12/UI-13 brauchen zwei verschiedene Messungen) |

Importregeln (`tests/test_importrichtung.py`): `gui -> (auswertung, darstellung, hintergrund)`, `darstellung` ohne Qt und ohne `pyplot`. Neue Qt-freie Logik (`gui/messungen.py`, `gui/serien.py`, `gui/achsen_zustand.py`) fällt in den Standardlauf der 90-%-Abdeckung; neue Widget-Module kommen in `[tool.coverage] omit` mit Begründungskommentar (wie T3a/T4).

### 2 Prüfung der Brief-Annahmen

| Brief | Ergebnis |
|---|---|
| A-1 Ansichten 1–4 auf aktiver Messung, 5 auf allen | tragfähig; Wechsel der aktiven Messung nutzt den Aufbau von `_uebernehme` (Punktliste, Kanalpaar, Tabellen) mit vorhandenen Daten |
| A-2 Skala zieht aus AD in AG | tragfähig; `rb_skala_linear/log` werden durch AG-Umschalter ersetzt, dB bleibt in AD (Ansicht 1, derzeit deaktiviert: keine Referenzgröße) |
| A-3 gleiche Einheitenart je Größe | geprüft an der Beispieldatei: Einheiten `Vib X/Y/Z` m/s, `Ref1` N, `Ref2` m/s². |H1| mit Ref1 ist (m/s)/N, mit Ref2 (m/s)/(m/s²): **zwei Messungen mit verschiedenen Referenzkanälen sind nicht vergleichbar**. Regel: Die Einheit der ersten sichtbaren Serie gilt; Serien mit anderer Einheit sind „nicht darstellbar“ (UI-17), Grund in AF. Keine Umrechnung. |
| A-4 Punktzuordnung über Label | Beispieldatei: 135 Punkte, Labels `int64`, eindeutig (132…350, nicht lückenlos). Regel: Label in genau einer Zeile gefunden, sonst Serie nicht anlegen, Grund nennen (UI-12). Doppelte Labels in einer Datei werden als Fehler der Serie gemeldet, nicht still aufgelöst. |
| A-5 Geometrie aus `koordinaten_m` | betrifft nur Ansicht 4, nicht Teil |
| A-6, A-7 | nur R-071 |
| U-A1 Speicher/Ladezeit zweite Messung | **beantwortet** (Abschnitt 3), Messrechner offen (Skript in Schritt 5) |
| U-A2 Tempo über Remotedesktop | für diesen Plan nur Zeichnen von Ansicht 5/Achsen; Container-Werte in Kernbefund 5, Messrechner offen (UI-38). Wiedergabe-Tempo ist R-071. |
| U-A3 Auslenkung ohne Phase | nicht Teil (FG-04) |
| U-A4 Tastenkonflikte | für diesen Plan: Strg+5 ist frei; Pos1 (`act_plot_zuruecksetzen`, `WidgetWithChildrenShortcut`) gilt nur im Teilbaum der `PlotFlaeche`, **AG wird deshalb Geschwister, nicht Kind der Plotfläche**, sonst nähme Pos1 den Textfeldern den Zeilenanfang; ←/→ im Plot nur bei Fokus im Canvas (Chips liegen außerhalb); Leertaste/Pfeile der Animation später über `AKTIONS_TASTEN` |

### 3 Datenmodell für mehrere Messungen

**Messwerte** (Beispieldatei 135 Punkte × 1600 Linien, 27 MB, Linux, RSS aus `/proc/self/statm`, kalter Prozess; Messrechner offen):

| Vorgang | Zeit | RSS-Zuwachs |
|---|---|---|
| `lade_svd` (Stufe A) | 1,4 s kalt (ADR-022: 0,1–0,8 s warm) | +58 MiB (`Messdaten.ap`+`cp` = 31 MiB nbytes) |
| 1. Kanalpaar im `PaarCache` | 48 ms | +28 MiB |
| 2. Kanalpaar | n. g. | +28 MiB |
| zweite Messung inkl. 2 Paare | | +103 MiB |

Das ergibt rund **115 MiB je Messung** mit zwei Paaren (Ansicht 1 allein braucht 1 Paar bei X, Y, Z je ein Paar bei 3D). Stufe B (`werte_aus`) liegt nur im Worker (247 MiB, vorübergehend).

**Entscheidungen:**

- **Höchstens 4 geöffnete Messungen** (Konstante `MESSUNGEN_MAX`, Annahme zu OF-5; vier Serien zwingen nicht zu vier Messungen, aber bis zu vier Vergleichspartner genügen). Bei 4 Messungen sind es rund 700 MiB im Hauptprozess bei LRU 4 (siehe unten). Bei Erreichen der Grenze ist `Messung hinzufügen …` deaktiviert mit Tooltip. Die Konstante wird nach der Messung am Messrechner angepasst.
- **`PaarCache`-LRU je Messung:** `max(2, Zahl der verschiedenen Paare in den Serien dieser Messung)`, höchstens 4 (rund 112 MiB). Sonst rechnet jeder Wechsel der Serie 250 ms neu. Über `PaarCache` (neue Methode `setze_groesse`, kein Eingriff in die Rechnung).
- **Kurven werden aufgelöst und gehalten:** Eine Serie speichert ihre aufgelöste Kurve (1600 Werte) und löst nur bei Änderung der Auswahl neu auf, nicht bei Achsen-, Sichtbarkeits- oder Anordnungswechsel.
- **Speicherangabe:** `Messungen.speicher_mib(messung)` summiert `nbytes` der Datenfelder und des Caches (testbar, ohne `psutil`), im Tooltip des Chips. Kein Abbruchkriterium aus RAM (ohne neue Abhängigkeit nicht belastbar).
- **Stufe B (Prüfungen, 8–13 s, Annahmen):** nur für die **aktive** Messung, beim ersten Aktivieren (bzw. Öffnen des Prüfdialogs) gestartet, höchstens ein B-Auftrag gleichzeitig; ein Wechsel bricht den laufenden ab (`abbrechen()`, 2 ms) und verwirft nur diesen. Die Annahmen (M8) sind für alle Messungen dieselben `Annahmen()`-Voreinstellungen (`_annahmen()` fällt ohnehin auf `Annahmen().eintraege()` zurück), das Kennzeichen in Ansicht 5 braucht Stufe B nicht.
- **Laden zusätzlicher Messungen:** je Messung ein eigener Stufe-A-Auftrag (ADR-022), **höchstens einer gleichzeitig**, weitere warten (Speicherspitze und Kerne, einfach testbar). Job-IDs je Messung statt einer globalen; `Öffnen …` (Ersetzen) behält das heutige Verhalten.

**Klassen** (Qt-frei, `gui/messungen.py`, Standardlauf mit vollem Test):

```
MessungsZustand: LADEN | BEREIT | FEHLER
Messung (eq=False): id (stabil, nie wiederverwendet), kurzname, pfad, zustand, geladen, cache,
                    pruefung, pruef_fehler, antrieb, fehlertext
Messungen:          hinzufuegen(pfad) -> Messung (Kurzname "A", "B", ..., "Z", "AA")
                    ersetze(id, pfad)            # Öffnen: Kurzname bleibt, neue id
                    entferne(id) -> Serien-Folgen  # Aktive Messung rückt auf die vorige
                    setze_aktiv(id), aktive
                    umbenennen(id, text) -> Fehlertext | None   # Pflicht, eindeutig, ohne führende Leerzeichen
                    ist_voll, speicher_mib(m), naechster_ladeauftrag()
```

Kurzname-Regeln (`pruefe_kurzname`, UI-9 „eindeutig“): nicht leer, höchstens 12 Zeichen (Chip, Legende, Stempel), nicht doppelt (Vergleich ohne Groß-/Kleinschreibung), keine Zeilenumbrüche. Dieselbe Datei zweimal öffnen ist erlaubt (Prüfsumme gleich: Hinweis „Dieselbe Datei wie A.“ in AF); so ist ein Test am Messrechner mit nur einer Beispieldatei möglich.

**Anbindung an den Reiter:** `self._messungen: Messungen`; `_geladen`, `_cache`, `_datei_pfad`, `_pruefung`, `_pruef_fehler`, `_antrieb` werden **Eigenschaften** mit Lese- und Schreibzugriff auf die aktive Messung (bestehender Code und Tests bleiben unverändert). `_uebernehme` wird in „aufbereiten“ (Cache, Punktliste, Parameter, Kanalpaare, Antrieb: bleibt, scheitert wie heute als Lesefehler) und „zeigen“ (AD, AB, Plot) zerlegt; „zeigen“ dient auch dem Wechsel der aktiven Messung. Auswahl in AD (Punkt, Komponenten, Kanalpaar) wird beim Wechsel zurückgesetzt wie bei einer neuen Datei (kein Zustand je Messung, Annahme).

### 4 Zeichenschicht-Erweiterung (GUI-frei, `darstellung/`)

**4.1 Achsenoptionen** (`darstellung/achsen.py`, Schritt 1)

```
Bereich(von: float | None, bis: float | None)          # None = Auto, je Seite
AchsenOptionen(frequenz: Bereich, frequenz_skala: Skala = "linear",
               y: Mapping[str, Bereich])               # Rolle -> Bereich; Rollen "betrag", "phase" (Grad)
pruefe_bereich(bereich, skala, name) -> None | raise AchsenFehler   # Texte des Briefs 3.1
parse_zahl(text) -> float | None | raise AchsenFehler  # Dezimalkomma und -punkt, leer = None
```

- Jede der drei Zeichenfunktionen bekommt in ihren Optionen **ein neues Feld** `achsen: AchsenOptionen | None = None`. `None` heißt unverändertes Verhalten (öffentliche Signaturen und die Thesis-Abbildungen bleiben bitgleich, Test). Die **Amplitudenskala bleibt in `Optionen.skala`** (eine Quelle, keine Signaturänderung); neu ist nur `frequenz_skala`.
- Die Zeichenfunktion wendet die Bereiche an und prüft sie selbst (`AchsenFehler` ist ein `ValueError`; die Oberfläche prüft vorher mit `pruefe_bereich` und zeigt die Inline-Meldung).
- **Auto-y über den sichtbaren Frequenzbereich** (Annahme E6): Ist nur x gesetzt, skaliert y auf die Daten innerhalb von x (Hilfsfunktion in `zeichnung.py`, `dataLim` aus den sichtbaren Punkten, dann `autoscale_view`). Ohne das zeigt ein Ausschnitt um eine Resonanz die y-Achse der größten Spitze der ganzen Kurve.
- Phase in Ansicht 2: Rolle `"phase"` in Grad (Auto = ±180°, Ticks wie heute), Kohärenz bleibt fest 0 bis 1,05 (nicht in der Leiste, UI-1).
- Ansicht 3: **Datenbereich = Eingabe**, der Beschriftungsstreifen wird oberhalb ergänzt (`obere_grenze(unten, oben, anteil, log)`). In der Oberfläche (kein Streifen, ADR-026 Nachtrag 1) entspricht `get_ylim()` genau der Eingabe, im Bild und in der Thesis kommt der Streifen oben dazu. Spitzen außerhalb des x-Bereichs werden nicht beschriftet (UI-8).
- Die x-Achse hat zwei Skalen: logarithmisch nur mit `von > 0` (die Frequenzachse beginnt bei Δf > 0, Beispiel 0,625 Hz); Formatter mit Dezimalkomma auf Log-Achsen ist zu prüfen (Hauptticks und Nebenticks).

**4.2 Diagramm Ansicht 5** (`darstellung/diagramm.py`, `darstellung/serien_daten.py`, Schritte 6 und 8)

```
GroessenId: "spektrum" | "h1" | "h2" | "kohaerenz" | "phase"      # Teilgröße von "spektrum": "kohaerent" | "leistung"
SerienSpec (frozen): messung_id, punkt_label: int | None (None = Mittel), komponente | kanalpaar, groesse, slot, sichtbar
DiagrammSerie:       kurzname, dateiname, punkt_text, komponenten_text, frequenz_hz, y, einheit, groesse,
                     mittelformel, punktzahl_text, phase_unbestaetigt, slot, sichtbar
DiagrammDaten:       serien (aufgelöst), nicht_darstellbar (Spec -> Grund)
DiagrammOptionen:    anordnung: "ueberlagert" | "nebeneinander", achsen: AchsenOptionen, y_skala je Größe, kennzeichen_phase
loese_serie_auf(spec, messdaten, cache, kurzname) -> DiagrammSerie | raise DarstellungsFehler(Grund)
zeichne_diagramm(fig, daten, opt, stil) -> Zeichnung
```

- **Auflösung ohne neue Mathematik:** Spektrum aus `spektrum_daten(..., komponenten=(c,), groesse=...)`, |H1|, |H2|, γ² aus `frf_daten` (`betrag_h1`, `betrag_h2`, `kohaerenz`), Phase aus `phase_rad` in Grad über `ohne_umbruch(grad(...))` wie Ansicht 2. Beim Mittel liefert `frf_daten` bereits Betragsmittel (H1/H2), arithmetisches Mittel (γ²) und die Punktzahl; **Phase beim Mittel ist nicht darstellbar** (wie Ansicht 2, F-4b), Grund in AF.
- **Linienarten:** Jede Serie trägt einen festen `slot` 0 bis 3 (niedrigster freier beim Anlegen), Linienart `stil.linienart(slot)`, Farbe `stil.serienfarbe(slot)`. Damit bleibt eine Serie beim Entfernen einer anderen optisch gleich (UI-18, UI-20).
- **Überlagert:** eine Achse, eine Größe (alle Serien müssen die Größe des Diagramms und dieselbe Einheit haben, sonst „nicht darstellbar“), Legende unter der Achse mit Linienprobe, Eintrag `<Kurzname> · <Punkt/Mittel> · <Komponente|Kanalpaar>` und bei Mittel eine zweite Zeile `<Mittelformel> über <n> Punkte` (Text aus den Daten; UI-11).
- **Nebeneinander, Teilbild-Regel** (Annahme E10): Ein Teilbild je Gruppe (Größe, Messung), sortiert nach Größe, dann Messung, höchstens 4 Teilbilder, 2 Spalten, bei mehr als 2 Teilbildern in Zeilen umgebrochen. Eine Größe und zwei Messungen ergeben 2 Teilbilder (UI-10), eine Messung mit zwei Größen ebenfalls (UI-16). Teilbildkopf (Achsentitel-Zeile über dem Teilbild, kein Diagrammtitel) nennt Kurzname und Größe. **x immer gekoppelt** (`sharex`, gleicher sichtbarer Frequenzbereich), **y gekoppelt zwischen Teilbildern gleicher Größe**, getrennt zwischen verschiedenen Größen. Jedes Teilbild trägt „Größe [Einheit]“ als y-Titel; Legende einmal unter dem Gesamtbild.
- **Eigene Frequenzachse je Messung:** jede Linie mit ihren eigenen `frequenz_hz` (UI-13, keine Interpolation, keine Differenz). Auto-x = Vereinigung (kleinster Start, größtes Ende).
- **Sichtbarkeit (UI-21):** unsichtbare Serien werden in die Autoskalierung einbezogen, aber nicht gezeichnet und nicht in der Legende geführt. Achsengrenzen bleiben dadurch beim Ein-/Ausblenden gleich.
- Kennzeichen „⚠ unbestätigt (M8)“: Kasten im Phasen-Teilbild bzw. an der Achse wie `kennzeichen_anbringen` (Text aus `kennzeichen_text("phase", annahmen)`); die Zeichenfunktion ohne Stempel enthält nicht „Arbeitsansicht“ und nicht „enthält unbestätigte Größen“ (UI-19).
- `Ansicht.DIAGRAMM = 5` in `zeichnung.py`, `ZEICHNER[Ansicht.DIAGRAMM] = zeichne_diagramm`. `Zeichnung.rollen` (Tuple, Rolle je Achse, z. B. `("betrag",)`, `("betrag","phase","kohaerenz")`, `("h1","h1")`) erlaubt der Oberfläche die Zuordnung Achse → Feld, ohne Ansichten zu kennen.

**4.3 Stempel** (`darstellung/bild.py`): `baue_stempel` bekommt optional `dateien: Sequence[tuple[str, str]]` (Kurzname, Dateiname); mit Wert steht je Datei eine Zeile `A: ref_Mitte.svd`, die Kopfzeile nennt „Ansicht 5 Diagramm“ und den Git-Hash. Alte Aufrufe mit `dateiname=` bleiben gültig. `bild_unbestaetigt` für Ansicht 5: M8, wenn mindestens eine **sichtbare, darstellbare** Serie die Größe Phase hat.

### 5 Achsenleiste mit Zustand je Ansicht (R-073)

**Zustand** (Qt-frei, `gui/achsen_zustand.py`): `AchsenZustand` hält je Ansicht (1, 2, 3, 5) und Rolle den `Bereich`, die Skala und das Kennzeichen „fest“. Schlüssel in Ansicht 5: `(5, GroessenId)`. Methoden: `optionen(ansicht, rollen)` (baut `AchsenOptionen`), `setze_bereich`, `setze_skala`, `auf_auto(ansicht)`, `alles_auf_auto()`, `bei_neuer_datei()` (Bereiche zurück, Skalen bleiben, UI-6), `uebernehme_grenzen(ansicht, rolle, von, bis)` (aus der Werkzeugleiste). Voreinstellungen: Amplitude/Betrag `log`, Frequenz `linear` (UI-2), Phase nur linear.

- **Je Ansicht:** Ansicht 1 und 3 teilen die Rolle „betrag“ in je eigenem Zustand je Ansicht (Brief: „je Ansicht“). Wechsel von Punkt, Komponente, Mittel/Punkt, Größe (Ansicht 1: |CPH|/√AP, gleiche Einheitenart), aktiver Messung und Serienliste verändert den Zustand nie (UI-3, UI-21). Der Zustand wird beim Ansichtswechsel nicht verworfen (heute geht der y-Zoom verloren).
- **Ansicht 5, Größe-Wechsel (Abweichung zum Brieftext, E11):** Bereiche gelten **je Größe** (Spektrum in m/s und Kohärenz 0 bis 1 teilen keinen Zahlenbereich). Wechsel zurück zur ersten Größe stellt deren Bereich wieder her.
- **Zoom/Verschieben/Zurücksetzen der Werkzeugleiste (UI-4):** `PlotToolbar` meldet über ein Signal `bereich_geaendert`, nachdem Zoom oder Pan abgeschlossen sind (Überschreiben von `push_current`, ausgelöst durch `release_zoom/release_pan`) und nach `home/back/forward` (diese überschreibt die Klasse schon). Ein Schutz verhindert Meldungen aus dem eigenen `zeichne` (dort ruft `push_current` die Klasse selbst). **Annahme E12:** Zoom und Pan schreiben die sichtbaren Grenzen als „fest“ in den Zustand; **Zurücksetzen (Knopf, Pos1) heißt „Auto für die Ansicht“** (Felder grau mit Auto-Wert). Der Verlauf (Zurück/Vor) schreibt jeweils die gezeigten Grenzen.
- **Anzeige der Auto-Werte (Brief 3.1):** Nach jedem Zeichnen liest die Plotfläche die wirksamen Grenzen aus `Zeichnung.achsen` und meldet sie der Leiste (Signal `grenzen_gezeichnet`). Auto-Felder zeigen sie grau mit Wert, feste Felder sind hervorgehoben (Rahmen plus „fest“ im `accessibleDescription`, nicht nur Farbe).
- **Neuzeichnen:** nur bei Enter oder Fokuswechsel **und nur wenn sich der Wert ändert** (`QLineEdit.editingFinished` feuert auch bei Fokusverlust ohne Änderung: Vergleich mit dem letzten gültigen Wert); genau ein `PlotFlaeche.zeichne` je Übernahme (UI-37). Resize-Neuzeichnen (Ansichten 3, 4, jetzt auch 5) bleibt entprellt.
- **Gültigkeit (UI-5):** `pruefe_bereich` (von ≥ bis, log mit Wert ≤ 0, Text statt Zahl) liefert den Meldetext, die Leiste zeigt ihn als Label unter dem Feld (Symbol ✖ aus `tokens.symbol`), der Plot bleibt unverändert; Fokuswechsel auf ein anderes Feld stellt den alten Wert wieder her.
- **Widget** (`gui/achsenleiste.py`, Geschwister der `PlotFlaeche` in AE, `objectName`s nach Brief 7): je Achse Beschriftung, Felder von/bis als `QLineEdit` (Platzhalter „Auto“, Suffix als Beschriftung/Einheit), Umschalter linear/logarithmisch, `btn_achsen_auto`. Umbruch in zweite Zeile bei Platzmangel nach dem Muster `_Fusszeile`/`_fuss_verteilen` (Gruppen aus `sizeHint`, kein Abschneiden). Welche Achsen sichtbar sind, steht in einer Tabelle `ACHSEN_JE_ANSICHT` (Qt-frei in `gui/anzeige_auswerten.py`): 1/3 Frequenz, Betrag; 2 Frequenz, Betrag, Phase (nur bei „Phase anzeigen“); 5 Frequenz, y der Größe (bei „nebeneinander“ mit mehreren Größen zusätzlich Auswahl, auf welche Größe sich y bezieht); 4 keine.
- **Thesis:** `tools/auswertung/darstellung_beispiel.py` nutzt dieselben Optionen (`achsen=...`), wenn gewünscht; sonst unverändert.

### 6 Oberfläche Ansicht 5 und Messungsverwaltung (R-058, R-059)

**AA (`gui/messungsleiste.py`, Widget):** `btn_messung_hinzu` neben `btn_oeffnen`, Chips in einer horizontal scrollbaren Zeile, nicht umbrechend (Brief). Chip = Wechselknopf mit Text `(<Kurzname>) <Dateiname gekürzt>` (offen, Abschnitt 9) und ×-Knopf; aktiv: Rahmen 2 px `C_AKZENT`, Symbol und `accessibleName` „aktiv“. Doppelklick oder Feld in AD ändert den Kurznamen (`pruefe_kurzname`). Pfeiltasten wechseln zwischen Chips, Entf entfernt nach Bestätigung (nur wenn Serien betroffen, UI-14: Dialog `Bestätigung`). Der Bereich `lbl_datei`/`lbl_pfad` bleibt (aktive Messung, gekürzt), seine Breite gibt der Chipzeile nach (Stretchfaktoren), UI-36 prüft das bei 1100 Pixel.

**AD Ansicht 5 (`gui/auswahl_diagramm.py`):** Radioknöpfe `rb_groesse_*` (`rb_groesse_spektrum`, `_h1`, `_h2`, `_kohaerenz`, `_phase`) mit Begründungstext bei nicht verfügbaren Größen (`verfuegbare_groessen`, kein Referenzkanal: UI-17); bei „Spektrum“ eine Teilgröße |CPH| / √AP (Annahme E13, Voreinstellung wie Ansicht 1); `liste_serien` (`QListWidget` mit Linienprobe als `QIcon` aus `Plotstil`, höchstens 4); `btn_serie_neu`, Bearbeiten, Entfernen, Kontrollkasten „sichtbar“ je Zeile; `btn_serie_aus_ansicht`, `btn_serie_alle`; `rb_anordnung_ueberlagert`/`_nebeneinander`. Serien-Dialog (modal, Esc): Messung, Punkt (Label) oder Mittel, Komponente bzw. Kanalpaar, Größe (nur bei „nebeneinander“). **Logik Qt-frei in `gui/serien.py`**: `SerienListe` (maximal 4, Duplikatprüfung `Diese Serie gibt es bereits.`, Slot-Vergabe, Entfernen mit Messung), `serie_aus_ansicht(...)`, `serien_fuer_alle(messungen, auswahl)` mit Grundliste (fehlendes Label, UI-12), Legendentext, Teilbildregel, Beschreibungstext (`accessibleDescription`: Serien, Größe, Frequenzbereich).

- **„Aus aktueller Ansicht übernehmen“:** Quelle ist die zuletzt benutzte Ansicht 1 bis 3 (`_letzte_ansicht_1_3`). Ansicht 1: je gewählte Komponente eine Serie; Ansicht 2: |H1| (oder |H2|, wenn nur dieses gewählt) des Kanalpaars; Ansicht 3: die Kurve, die Ansicht 3 zeigt. Passt die Größe nicht zur Größe der vorhandenen Serien (überlagert), wird nicht gewechselt, sondern gemeldet; ist die Liste leer, setzt die Übernahme die Größe. Überschreitet es vier Serien, werden so viele übernommen wie passen und AF nennt den Rest.
- **Zeichnen:** `_zeichne_ansicht_5` löst nur Serien auf, deren Spec sich geändert hat (Cache je Serie), baut `DiagrammDaten`/`DiagrammOptionen` aus `SerienListe` und `AchsenZustand`, zeichnet über `plot.zeichne(Ansicht.DIAGRAMM, ...)`. Kopfzeile (`lbl_plotkopf`): Messungen, Größe, Anordnung. AF: Gründe nicht darstellbarer Serien (Symbol plus Wort, UI-17).
- **Bild speichern** (UI-19): `speichere` für Ansicht 5 mit Stempel über alle beteiligten Dateien; Zeichnung auf neuer Figure mit denselben Optionen, das Bild folgt den festen Bereichen automatisch. `btn_export` bleibt auf die aktive Messung bezogen und ist in Ansicht 5 aktiv (unveränderter Export, dokumentiert).
- **Zustände (Brief 4):** keine Datei, Laden einer weiteren Messung (Chip „lädt …“ mit unbestimmtem Balken, Serien dieser Messung erst nach Laden wählbar), Ladefehler der zweiten Datei (Fehlerband, bisherige Messungen unverändert), keine Serie (Hinweistext), unmögliche Serie, doppelte Serie, fünfte Serie.

### 7 Schritte (riskanteste zuerst innerhalb der Etappen; je Schritt lauffähig und getestet)

Reihenfolge der Etappen folgt der Nutzervorgabe (R-073, R-058, R-059). Aufwand in Personentagen eines Entwicklers (grobe Schätzung, ±40 %), zusammen rund 19 Tage. Nach **jedem** Schritt laufen `uv run ruff check .`, `ruff format --check .`, `mypy --strict .`, `pytest --cov --cov-fail-under=90` und `QT_QPA_PLATFORM=offscreen uv run pytest -m gui`; die Zahl der bestehenden Tests sinkt nie.

| Nr | Etappe | Schritt | Dateien | Verifikation | Tage | Risiko |
|---|---|---|---|---|---|---|
| S1 | A R-073 | **Sicherheitsnetz und Achsenoptionen in der Zeichenschicht.** (a) Charakterisierung: Thesis-Abbildungen aus `darstellung_beispiel.py` mit synthetischer Datei erzeugen und als Referenz (Figure-Struktur plus PNG-Hash auf derselben Maschine) ablegen; heutiges Zoom-Verhalten (`test_gui_cursor.py`) bleibt. (b) 30-Minuten-Spike: `push_current`-Überschreibung meldet Zoom/Pan/home genau einmal und schleift nicht (Skript im Scratchpad, Ergebnis in Rückmeldung). (c) `darstellung/achsen.py`; Feld `achsen` in `SpektrumOptionen`, `FrfOptionen`, `SpitzenOptionen`; Auto-y über sichtbares x; Ansicht-3-Streifen; Beschriftung nur im Bereich. | `darstellung/achsen.py` (neu), `spektrum.py`, `frf.py`, `spitzen.py`, `zeichnung.py`, `tests/darstellung/test_dar_achsen.py` (neu) | UI-1 (Figure), UI-2, UI-5 (Prüffunktion), UI-7 (Phase in Grad, Dezimalkomma), UI-8; Regression: Abbildungen unverändert bei `achsen=None`; Grenzwerte 1e-9 rel. | 1,5 | mittel (Ansicht 3, Log-Ticks) |
| S2 | A | **Zoom-Quelle ersetzen und Rückkopplung.** `PlotFlaeche`: Optionen mit `achsen` aus dem Zustand, `Zeichnung.rollen`, Signale `bereich_geaendert` und `grenzen_gezeichnet`; `_zoom`, `zoom_behalten`, `_standard_grenzen` und `bild_grenzen` entfallen (Parameter `zoom_behalten` bleibt bis S10 als wirkungsloser Alias, damit Tests und Aufrufer nicht brechen, und wird dort entfernt). `gui/achsen_zustand.py` (Qt-frei). Reiter reicht den Zustand durch. | `gui/plotflaeche.py`, `gui/achsen_zustand.py` (neu), `gui/arbeitsbild.py`, `gui/auswerten_reiter.py` (nur Aufrufstellen), `tests/gui/test_gui_cursor.py` | UI-3 (Wechsel Punkt/Komponente/Größe/Mittel: Grenzen gleich), UI-4 (Toolbar → Zustand, Zurücksetzen → Auto), UI-6, Arbeitsbild übernimmt feste Grenzen; Cursor und Klick unverändert (bestehende Tests grün) | 2 | **hoch** |
| S3 | A | **Achsenleiste (AG) in Ansichten 1 bis 3.** `gui/achsenleiste.py`; Einbau in AE als Geschwister der Plotfläche; `rb_skala_*` ziehen in AG (A-2), Voreinstellungen log/linear; Inline-Meldungen, Dezimalkomma-Anzeige, „Alles auf Auto“; Tab-Reihenfolge und `AKTIONS_TASTEN` (Pos1 unverändert). Neue Tokens und `KONTRAST_PAARE`. | `gui/achsenleiste.py` (neu), `gui/auswerten_reiter.py`, `gui/anzeige_auswerten.py`, `gui/tokens.py`, `gui/stil.py`, `pyproject.toml` (omit), `tests/gui/test_gui_achsen.py` (neu) | UI-1, UI-2, UI-3, UI-4, UI-5, UI-6, UI-7 (GUI), UI-37 (Zahl der Zeichenaufrufe), UI-35 (Kontrast), Teil UI-34/UI-36 (Leiste bei 1100×680 überlappungsfrei, Umbruch) | 2 | mittel |
| S4 | B R-058 | **Messungsliste und Delegation (Verhalten unverändert).** `gui/messungen.py`, Reiter mit Eigenschaften, `_uebernehme` in „aufbereiten“ und „zeigen“ zerlegt, `Ansicht`-Zustände (`_a3_*`, `_a4_*`) beim Wechsel zurücksetzen; noch eine Messung, keine neue Bedienung. | `gui/messungen.py` (neu), `gui/auswerten_reiter.py`, `tests/gui/test_messungen_logik.py` (neu, Standardlauf) | Alle bestehenden GUI-Tests grün (Regression, das ist die Messlatte); `Messungen`-Logik: Kurznamen (A…Z, AA), Eindeutigkeit, Ersetzen, Entfernen und Aktivrücken, Grenze | 2 | **hoch** (Refaktor) |
| S5 | B | **Weitere Messungen laden, Chips, Aktivwechsel, Speicher.** Auftragsliste in `_abfrage`, Warteschlange (einer gleichzeitig), Job-ID je Messung, Fehlerband je Messung, Stufe B nur für die aktive; `btn_messung_hinzu`, `gui/messungsleiste.py`; `PaarCache.setze_groesse`; Messskript `tools/auswertung/speicher_messen.py` (RSS je Messung am Messrechner, neu, ~40 Zeilen, nicht im Wheel). | `gui/auswerten_reiter.py`, `gui/messungsleiste.py` (neu), `darstellung/auswahl.py` (nur `setze_groesse`), `tools/auswertung/speicher_messen.py` (neu), `tests/gui/test_gui_messungen.py` (neu) | UI-9 (zwei Chips, eindeutige Kurznamen, **ein Klick auf einen anderen Reiter wird während des Ladens verarbeitet**, getestet mit nie fertigem Ausführer), Ladefehler der zweiten Datei, Wechsel der aktiven Messung ändert Achsenleiste nicht (UI-3, aktive Messung), Teil UI-14 (Entfernen) | 2,5 | mittel (Prozess, Aufträge) |
| S6 | B | **`zeichne_diagramm` und Serienauflösung (GUI-frei).** `darstellung/diagramm.py`, `serien_daten.py`, `Ansicht.DIAGRAMM`, Legende-unten nach `zeichnung.py` hochgezogen, Slot-Linienarten, überlagert und nebeneinander (Teilbild-Regel, `sharex`, `sharey` je Größe), Bereiche aus S1. | `darstellung/diagramm.py`, `serien_daten.py`, `zeichnung.py`, `spitzen.py` (ruft gemeinsame `_legende`), `tests/darstellung/test_dar_diagramm.py` (neu) | UI-10 (Figure: Linienzahl, Linienarten paarweise verschieden, gekoppelte Achsen `get_shared_x_axes`), UI-11 (Legendentext, Mittelformel, Punktzahl aus den Daten), UI-13 (Linienlänge je Serie), UI-15/UI-16 (Achse „Größe [Einheit]“, Einheit = Quotient), UI-18, UI-20, UI-21 (Grenzen vor/nach Sichtbarkeit gleich), Importtest ohne Qt/`pyplot`; **Referenz:** Kurven gegen `spektrum_daten`/`frf_daten` mit `array_equal` | 2 | mittel |
| S7 | B | **Ansicht 5 in der Oberfläche (Grundfunktion).** Knopf 5, Strg+5, `FREIGESCHALTETE_ANSICHTEN`, `ANSICHT_NAMEN`; AD-Seite mit Größe, Anordnung, `btn_serie_alle`, `btn_serie_neu` (zunächst Standarddialog), Serienliste Grundfunktion; AG für Ansicht 5; `_zeichne_ansicht_5`, Kopfzeile, Meldungen, Entfernen einer Messung mit Bestätigung. | `gui/auswerten_reiter.py`, `gui/auswahl_diagramm.py` (neu), `gui/serien.py` (neu, Qt-frei), `gui/anzeige_auswerten.py`, `gui/anzeige_aktionen.py` | UI-10 (GUI, beide Anordnungen mit zwei synthetischen Messungen verschiedener Linienzahl), UI-12 (fehlendes Label), UI-13, UI-14 (Bestätigung bei betroffenen Serien), UI-34 (Strg+5) | 2 | mittel |
| S8 | C R-059 | **Serienlisten-Bedienung, Größen und Übernahmen.** Dialog mit Esc, Bearbeiten/Entfernen, Sichtbar-Kästchen, `Aus aktueller Ansicht`, Größen-Radios mit Begründung, Duplikat- und Maximalregel mit Hinweistexten, Phase-Mittel- und Einheitenregel, Kennzeichen M8. | `gui/auswahl_diagramm.py`, `gui/serien.py`, `tests/gui/test_gui_diagramm.py` (neu), `tests/test_serien_logik.py` (neu, Standardlauf) | UI-15, UI-16 (Radio lässt genau eine Größe zu; nebeneinander: je Teilbild eigene Größe), UI-17 (ohne Referenzkanal: Größen deaktiviert mit Text; Serie nicht gezeichnet, Grund in AF), UI-18 (fünfte Serie deaktiviert, Text), UI-21 | 2 | mittel |
| S9 | C | **Bild speichern für Ansicht 5.** Stempel mit allen Dateien, `bild_unbestaetigt`, Dateiname-Vorschlag, PNG und PDF; Test, dass die Zeichenfunktion ohne Stempel die Stempeltexte nicht enthält. | `darstellung/bild.py`, `gui/anzeige_aktionen.py`, `gui/auswerten_reiter.py`, `tests/darstellung/test_dar_bild.py`, `tests/gui/test_gui_diagramm.py` | UI-19 (PNG und PDF existieren, Magic Bytes; Legende, alle Dateinamen, Git-Hash, „⚠ enthält unbestätigte Größen (M8)“ bei Phase, nicht ohne Phase) | 1,5 | niedrig |
| S10 | C | **Querschnitt und Hardware-Prüfanleitung.** Tab-Reihenfolge (AA → AC → AD → AG → AE → AF), `focusPolicy`, Layout bei 1100×680 und 1366×768, `accessibleName`/`-Description`, Kontrastpaare, Alias `zoom_behalten` entfernen, Prüfanleitung für den Messrechner (UI-38: Achsenfelder, Wechsel, zwei Messungen, Speicher mit `speicher_messen.py`, Remotedesktop) nach Ablauf G; Versionsnummer anheben (auf Anweisung bei Auslieferung). | `gui/auswerten_reiter.py`, `gui/tokens.py`, `tests/gui/*`, Prüfanleitung (Ablage nach Anweisung des Orchestrators) | UI-34, UI-35, UI-36, UI-37 gesamt; alle Prüfungen des Standardlaufs grün; UI-38 bleibt **offen bis zur Bestätigung durch den Nutzer** | 1,5 | niedrig |

Abhängigkeiten: S1 → S2 → S3; S4 → S5 → S7; S1 → S6 (Bereiche) und S6 → S7 → S8 → S9 → S10. S4 darf erst nach S3 beginnen (beide ändern `auswerten_reiter.py`; es schreibt immer nur ein Agent). **Nach S3** ist R-073 vollständig ausgeliefert (eigener Prüfpunkt, Nutzerabnahme möglich); **nach S7** ist R-058 grundsätzlich bedienbar; **nach S9** R-059.

### 8 Andockstellen für R-071 (nur Schnittstellen, kein Code für die Animation)

- **Ansichtsregister:** `ANSICHT_NAMEN`/`FREIGESCHALTETE_ANSICHTEN` und die Tabelle `ACHSEN_JE_ANSICHT` sind die einzigen Stellen, die eine neue Ansicht (R-072) bzw. Ansicht 4 mit „keine Achsenleiste“ kennen; `ZEICHNER` bleibt die einzige Zuordnung Ansicht → Zeichenfunktion.
- **Leistenbereich in AE:** AG (und später AH) liegen in einem eigenen Container mit festem Platz zwischen Werkzeugleiste und Plot bzw. darunter; AH muss nur hineinwandern. Die Umbruchlogik (Gruppen aus `sizeHint`) wird für AG so allgemein geschrieben, dass AH sie verwendet.
- **Aktive Messung als einzige Eingabe von Ansicht 4:** `Messungen.aktive` (S4); der spätere Modus „Animation“ ist ein weiterer Radioschalter auf der AD-Seite von Ansicht 4 (`rb_modus_*`) und ändert `_zeichne_ansicht_4`, nicht die Messungsverwaltung.
- **Plotfläche hinter schmaler Schnittstelle:** `PlotFlaeche.zeichne/speichere/leere` bleiben; ein 3D-Canvas (OE-A1) müsste nur dieselben drei Methoden und `Zeichnung`-ähnliche Rückgabe liefern. `Zeichnung.rollen` ist für 3D leer.
- **Stempel:** `baue_stempel` ist um beliebige Zusatzzeilen erweiterbar (Winkel, Überhöhung kommen später als `zusatz`).
- **Zustand je Ansicht ist schlüsselbasiert** (`AchsenZustand`), eine Ansicht 6 braucht keinen Umbau.

### 9 Entscheidungen mit Alternativen (ADR-Kandidaten, nach Freigabe)

| Nr | Entscheidung | Alternativen | Empfehlung |
|---|---|---|---|
| E1 | **Achsenbereiche als Option der Zeichenfunktion** (`AchsenOptionen`), eine Quelle für Oberfläche, Bild und Thesis | (a) Zoom wie heute in `PlotFlaeche` nachträglich setzen: Bild und Thesis brauchen Sonderwege (`bild_grenzen`), zwei Quellen | Optionen (Brief verlangt eine Quelle, Thesis profitiert) |
| E2 | **Messungsliste mit Delegation** an der aktiven Messung | (b) je Messung ein eigener `AuswertenReiter` in einem Stapel: dreifach duplizierte Oberfläche, Ansicht 5 braucht trotzdem eine Liste; (c) alles im Reiter umschreiben: großer Diff in 2127 Zeilen | Liste mit Eigenschaften (kleinster Diff, Tests bleiben gültig) |
| E3 | **Laden:** je Messung Stufe A, sequenziell, Stufe B nur für die aktive | Stufe B für alle (8–13 s und 247 MiB Worker je Messung, Annahmen ohnehin gleich); parallele Ladeaufträge (Speicherspitze) | wie vorgeschlagen |
| E4 | **Eine Zeichenfunktion `zeichne_diagramm`** für überlagert und nebeneinander, Serien aufgelöst und gehalten | zwei Funktionen (Doppelung); Auflösung bei jedem Zeichnen (jeder Achsenwechsel wäre bis zu 250 ms je Paar) | wie vorgeschlagen |
| E5 | **Eingabefelder `QLineEdit`** mit eigener Dezimalkomma-Auswertung, leer = Auto | `QDoubleSpinBox` (Tastendruck-Wirkung nur mit `setKeyboardTracking(False)`; „Auto“ nur über `specialValueText`, Leerzustand umständlich, Dezimalkomma nach Locale) | `QLineEdit` |
| E6 | **y-Auto über den sichtbaren x-Bereich** | y-Auto über die ganze Kurve (einfacher, aber Resonanzausschnitte unlesbar) | sichtbarer Bereich |
| E7 | **Legende unter der Achse** (Muster `_legende` aus Ansicht 3, nach `zeichnung.py` hochgezogen) | `fig.legend(loc="outside lower center")` (ignoriert den `rect` des Arbeitsbildes: Stempel kollidiert) | `_legende` |
| E8 | **`Ansicht.DIAGRAMM = 5`** in der gemeinsamen Enum | eigenes Register nur in der Oberfläche (Thesis müsste anders rufen) | Enum |
| E9 | **Chips in AA** (Grunddesign), Chipbereich scrollbar, Dateiname/Pfad werden schmaler | eigene Zeile unter AA (kostet rund 32 px Höhe von AE bei 1366×768, dort mindestens 600×320 Pflicht) | AA; falls UI-36 bei 1100 Pixel nicht ohne Abschneiden geht, Rückfall auf die Zeile (Messung in S5) |
| E10 | **Teilbild-Regel** (Größe, Messung), 2 Spalten, x gekoppelt, y gekoppelt je Größe | je Messung ein Teilbild nur bei einer Größe (Brief-Wortlaut), sonst je Größe: widerspricht sich bei zwei Größen und zwei Messungen | (Größe, Messung) |
| E11 | **y-Bereiche in Ansicht 5 je Größe** (Abweichung vom Brief-Wortlaut UI-3 „Größe“) | ein Bereich je Ansicht (bei Wechsel Spektrum → Kohärenz unbrauchbar) | je Größe |
| E12 | **Zoom/Pan schreibt „fest“, Zurücksetzen = Auto** | Zurücksetzen stellt den zuletzt eingegebenen Wert wieder her; Zoom schreibt nur Anzeige ohne „fest“ | wie vorgeschlagen |
| E13 | **Spektrum als eine Größe mit Teilgröße |CPH|/√AP** | sechs Radioknöpfe (Brief nennt fünf) | Teilgröße (Voreinstellung wie Ansicht 1) |

### 10 Testplan

**Ebenen.** (1) **Unit, Standardlauf** (ohne Qt, im 90-%-Pflichtlauf): `achsen.py`, `diagramm.py`, `serien_daten.py`, `bild.py`, `messungen.py`, `serien.py`, `achsen_zustand.py`, Anzeigehelfer. (2) **GUI offscreen** (`pytest -m gui`, wie T3a/T4, Attrappen-Ausführer, keine Pixelprüfung, sondern Figure-Struktur: `ax.get_xlim()/get_ylim()/get_xscale()/get_yscale()`, `Line2D`-Zahl, `get_linestyle`, `Legend`-Texte, `get_shared_x_axes`). (3) **Hardwaretest** nur UI-38 (nie als bestanden melden, bevor der Nutzer es bestätigt).

**Referenzen** (KONVENTIONEN „jede Auswertefunktion gegen einen analytischen Referenzfall“): Diese Pakete bilden Rechenergebnisse nur ab. Die Kurven jeder Serie werden mit `array_equal` gegen `spektrum_daten`/`frf_daten` der jeweiligen Messung verglichen (Toleranz null: identische Funktionen); die Mittelformeln und Punktzahlen aus den vorhandenen Referenzfällen (RF-UI-F2a… in FA-AUSW) bleiben unverändert getestet. Neue Zahlenwerte sind nur Achsengrenzen (rtol 1e-9, begründet: Eingabe → `float` → `set_xlim`, nur Rundung von Dezimaltext) und das Auto-y über sichtbaren x-Bereich (Handrechnung mit synthetischer Kurve, rtol 1e-12). Eine Fachabnahme ist nicht nötig (keine neue Mathematik); Stichprobe der Legendentexte durch den Reviewer genügt.

**Testdaten:** `synth_geladen(punkte, linien, labels, referenz, pfad)` parametrisiert (Test-Hilfe, Standardwerte wie heute); Messung B mit anderer Linienzahl und teilweise anderen Labels (UI-12/UI-13), Messung ohne Referenzkanal (UI-17), Messung mit Ref2 und einer Einheit, die nicht zu Ref1 passt (A-3). Beispieldatei `Input/20261012_ref_Mitte.svd` nur für einen langsamen Test je Etappe (Marker) und für `speicher_messen.py`.

| UI | Prüfung (Art) | Test (Datei) |
|---|---|---|
| UI-1 | Eingabe + Enter → `get_xlim/ylim` = Wert (rtol 1e-9) in Ansicht 1, 2, 3, 5; Felder vorhanden je sichtbarer Achse (GUI) | `test_dar_achsen.py`, `test_gui_achsen.py`, `test_gui_diagramm.py` |
| UI-2 | Umschalter → `get_xscale/get_yscale`; Voreinstellung y `log`, x `linear` (Unit + GUI) | dito |
| UI-3 | Eingabe, dann Wechsel Punkt, Komponente, Mittel/Punkt, Größe (Ansicht 1), aktive Messung; Grenzen und Skalen gleich; Ansicht 5: Serie hinzufügen/entfernen (GUI) | `test_gui_achsen.py`, `test_gui_messungen.py` |
| UI-4 | `NavigationToolbar2` Zoom/Pan simuliert (`canvas.toolbar.zoom()`, `release_zoom`) → Felder = sichtbare Grenzen; Feld → Plot; „Alles auf Auto“ → Felder leer, Autogrenzen (GUI) | `test_gui_achsen.py`, `test_gui_cursor.py` |
| UI-5 | `pruefe_bereich` (Unit, alle drei Fälle); GUI: Meldung am Feld sichtbar, Plot-Grenzen vorher = nachher, Alt-Wert nach Fokuswechsel | `test_dar_achsen.py`, `test_gui_achsen.py` |
| UI-6 | Datei ersetzen: Bereiche zurück, Skalen bleiben (GUI; Zustand Unit) | `test_gui_achsen.py`, `test_achsen_zustand.py` |
| UI-7 | Phasenfeld und y-Achse „Phase [°]“, Werte in Grad (Plot), Tickformat „1,5“ (Unit); Feldtext mit Dezimalkomma (GUI) | dito |
| UI-8 | Ansicht 3 mit `beschriftung_im_bild=True` und gesetzten Grenzen: alle Kasten-Boxen liegen im Achsenbereich (`get_window_extent` innerhalb `ax.bbox`), Spitzen außerhalb des x-Bereichs unbeschriftet (Unit) | `test_dar_achsen.py` (+ vorhandene L3-1…L3-3) |
| UI-9 | zwei Chips, Kurznamen eindeutig; Klick auf anderen Reiter während des Ladens (nie fertiger Ausführer) wird verarbeitet; Ladefehler lässt Messung A unverändert (GUI) | `test_gui_messungen.py` |
| UI-10 | zwei Messungen, Spektrum, |H1|, Kohärenz je überlagert (eine Achse, ≥2 Linien, Linienarten paarweise verschieden) und nebeneinander (2 Achsen, gekoppelt); Legende bzw. Teilbildkopf nennt Kurznamen (Unit + GUI) | `test_dar_diagramm.py`, `test_gui_diagramm.py` |
| UI-11 | Legendentext je Linie exakt, ohne Doppelungen; bei Mittel Formel und Punktzahl aus den Daten (Unit) | `test_dar_diagramm.py` |
| UI-12 | „Für alle Messungen“ legt je Messung eine Serie an; fehlendes Label → keine Serie, Grund in AF (Unit + GUI) | `test_serien_logik.py`, `test_gui_diagramm.py` |
| UI-13 | Zwei Messungen mit K = 64 und K = 48: `len(line.get_xdata())` je Serie = jeweilige Linienzahl, `array_equal` zur jeweiligen Frequenzachse (Unit) | `test_dar_diagramm.py` |
| UI-14 | Entfernen entfernt Serien; Bestätigung nur bei betroffenen Serien (GUI mit ersetztem Dialog) | `test_gui_diagramm.py` |
| UI-15 | zwei Punkte einer Messung und zwei Messungen: je 2 Linien, y-Titel „Größe [Einheit]“, Einheit = Quotient (`frf.einheit`) (Unit + GUI) | `test_dar_diagramm.py` |
| UI-16 | Radioknöpfe exklusiv (GUI); nebeneinander mit zwei Größen: Teilbildkopf nennt Größe, eigene y-Achse und Einheit (Unit) | dito |
| UI-17 | ohne Referenzkanal: Größen deaktiviert mit Begründung; Serie nicht gezeichnet, Meldung in AF (GUI); Einheit passt nicht (A-3) (Unit) | `test_gui_diagramm.py`, `test_serien_logik.py` |
| UI-18 | fünfte Serie: `btn_serie_neu` deaktiviert, Text exakt; Linienarten paarweise verschieden auch nach Entfernen und Anlegen (Slot) (Unit + GUI) | dito |
| UI-19 | PNG und PDF geschrieben (Magic Bytes `\x89PNG`, `%PDF`), Texte: Legende, alle Dateinamen, Git-Hash; „⚠ enthält unbestätigte Größen (M8)“ nur mit Phase; `zeichne_diagramm` allein enthält diese Texte nicht (Unit + GUI) | `test_dar_bild.py`, `test_gui_diagramm.py` |
| UI-20 | Figure-Struktur: bei vier Serien paarweise verschiedene `linestyle`; Test in Graustufen (Umsetzung `rgb2gray` der Linienfarben: Helligkeitsabstand dokumentiert, Linienart trägt allein); Sichtprüfung bei Abnahme (Unit) | `test_dar_diagramm.py` |
| UI-21 | Sichtbar aus/ein: `xlim/ylim` und Skalen gleich, Legende ohne unsichtbare Serie (GUI + Unit) | dito |
| UI-34 | Strg+5 wechselt zu Ansicht 5; `tab_kette` entspricht Abschnitt 6; alle bedienbaren Widgets `focusPolicy != NoFocus` (Durchlauf über `findChildren`); Fokusrahmen im Plot (GUI) | `test_gui_auswerten.py`, `test_gui_achsen.py` |
| UI-35 | vorhandener Kontrasttest über `KONTRAST_PAARE` besteht mit neuen Paaren (Feld „fest“, aktiver Chip) (Unit, Standardlauf) | `test_gui_anzeige*.py`/Tokentest |
| UI-36 | bei 1100×680: Geschwister-Rechtecke von AA (mit Chips), AG, AE überschneiden sich nicht, kein abgeschnittenes Feld (`sizeHint` ≤ Breite oder zweite Zeile); bei 1366×768: AE ≥ 600×320 (GUI) | `test_gui_achsen.py` |
| UI-37 | `PlotFlaeche.zeichne` per Zähler: Tippen im Feld (`QTest.keyClicks`) = 0 Aufrufe, Enter = 1, Fokuswechsel ohne Änderung = 0 (GUI) | `test_gui_achsen.py` |
| UI-38 | Hardwaretest nach Prüfanleitung (Remotedesktop, Achsenleiste, Wechsel, zwei Messungen, `speicher_messen.py`) | Nutzer |

Zusätzlich: Importtest (`darstellung` ohne Qt/`pyplot`, auch `diagramm.py`), `test_importrichtung.py`, Regression der Thesis-Abbildungen (S1), Abdeckung ≥ 90 % im Standardlauf (neue Qt-freie Module gehören dazu), `QT_QPA_PLATFORM=offscreen uv run pytest -m gui` mit `coverage_gui.toml` für die Widget-Module (ohne Mindestwert, wie bisher).

### 11 Akzeptanzkriterien dieses Plans

- **A1 (R-073):** UI-1 bis UI-8 erfüllt (Abschnitt 10, Etappe A abgeschlossen nach S3).
- **A2 (R-058):** UI-9 bis UI-14 erfüllt (nach S7, UI-14 vollständig nach S8).
- **A3 (R-059):** UI-15 bis UI-21 erfüllt (nach S9).
- **A4 (allgemein):** UI-34 bis UI-37 erfüllt; UI-38 liegt mit Prüfanleitung beim Nutzer, **offen bis zu seiner Bestätigung**.
- **A5 (Regression):** Alle bei Beginn bestehenden Tests laufen unverändert grün (Ausnahme: Tests zum entfallenden Zoomweg, mit Begründung ersetzt); `thesis`-Abbildungen bei `achsen=None` unverändert.
- **A6 (Qualität):** `ruff check`, `ruff format --check`, `mypy --strict`, `pytest --cov --cov-fail-under=90` fehlerfrei; `pytest -m gui` offscreen grün; Importregeln eingehalten; keine neue Abhängigkeit (Lockfile und `PINS` unverändert).
- **A7 (Andockstellen):** Ansicht 6 hinzufügen erfordert nur Registereinträge (Test: `ANSICHT_NAMEN` mit Dummy erweitern, Knopf entsteht); Ansicht 4 hat keine Achsenleiste.
- **A8 (Doku-Pflichten des Umsetzers):** Rückmeldung nennt je Schritt die ausgeführten Prüfbefehle und Ergebnisse; nicht ausgeführte (Messrechner) werden benannt.

### 12 Risiken

| Risiko | Auswirkung | Erkennung / Gegenmaßnahme |
|---|---|---|
| Rückkopplung Werkzeugleiste → Felder: `push_current` wird auch intern und bei `zeichne` gerufen, Schleifen oder doppelte Zeichnungen | Hänger, UI-37 verletzt | Spike in S1, Schutzflag, Zeichenzähler im Test; Rückfall: Callback `xlim_changed/ylim_changed` mit Entprellung (150 ms) |
| Umbau von `_uebernehme`/`_abfrage` bricht eines der rund 3500 Zeilen GUI-Tests | Regression | S4 ohne neue Bedienung, Eigenschaften-Delegation, Tests als Messlatte; Review nach S4 |
| Auto-y über sichtbares x ändert Verhalten bestehender Ansichten | sichtbare Änderung ohne Eingabe | nur wirksam, wenn x gesetzt (sonst gleich wie bisher); Test „ohne Eingabe bitgleich“ |
| Ansicht 3: Datenbereich = Eingabe plus Streifen weicht von der Eingabe im Bild ab | Verwirrung zwischen Oberfläche und Bild | dokumentiert (Brief UI-8), Arbeitsbild-Test, Hinweis in der Rückmeldung |
| Speicher bei vier Messungen (rund 700 MiB) am Messrechner unbekannt | Absturz/Swap | `MESSUNGEN_MAX` als Konstante, `speicher_messen.py` und Prüfanleitung; Anpassung nach Messung |
| Log-Frequenzachse: Tickformat und Nebenticks mit Dezimalkomma | falsche Beschriftung | Test in S1, Formatter prüfen |
| Platz bei 1100×680: AA mit Chips, AG und AH, AE mit mindestens 320 px bei 1366×768 | UI-36 | Messung in S3 und S5, Rückfall nach E9 |
| Verschiedene Referenzkanäle/Einheiten zwischen Messungen | leere Diagramme | A-3-Regel, deutlicher Grund in AF |
| Teilbildregel entspricht nicht dem Wunsch des Nutzers | Nacharbeit in S6/S7 | Frage F2, Entscheidung vor S6 |
| `PaarCache`-LRU größer: mehr Speicher je Messung | siehe oben | Obergrenze 4, Test der LRU-Größe |
| Windows/Remotedesktop-Verhalten (Zeichentempo, HiDPI, `QLineEdit`-Fokus) | nur am Messrechner prüfbar | UI-38, nie vorher „bestanden“ melden |

### 13 Nicht enthalten

R-071 (Animation, 3D, FG-04), R-070, R-072; Differenz- und Verhältniskurven; Interpolation auf gemeinsames Gitter; Umrechnung der Größen; Video oder GIF; Zustand der Auswahl je Messung (Punkt, Komponenten) über den Wechsel hinaus; Vektorisierung von P-07; Änderungen am Reiter „Messen“; Erweiterung von `tools/auswertung/darstellung_beispiel.py` um das Diagramm (nur auf Wunsch, kleines Zusatzpaket); Auslieferung (Versionsnummer, Wheelhouse) und Commits.

### 14 Offene Fragen an den Nutzer

**Nicht blockierend (Annahme gilt, bis geklärt; Etappe A kann starten):**

- **F1 Chip-Text.** Brief „(A) Kurzname ×“, Grunddesign „(A) ref_Mitte.svd ×“. *Annahme:* `(<Kurzname>) <gekürzter Dateiname> ×`, Voreinstellung Kurzname „A“, „B“, …; Dateiname und Pfad im Tooltip.
- **F2 Teilbild-Regel „nebeneinander“** (E10). *Annahme:* ein Teilbild je (Größe, Messung), 2 Spalten, höchstens 4 Teilbilder. Vor Beginn von S6 bestätigen.
- **F3 Zoom und Zurücksetzen** (E12). *Annahme:* Zoom/Pan setzen feste Werte, Zurücksetzen (Knopf und Pos1) heißt Auto für die Ansicht, „Alles auf Auto“ gilt für alle Achsen der Ansicht. Vor Beginn von S2 bestätigen.
- **F4 y-Bereiche in Ansicht 5 je Größe** (E11, weicht vom Wortlaut UI-3 ab). *Annahme:* je Größe.
- **F5 y-Auto folgt dem sichtbaren Frequenzbereich** (E6). *Annahme:* ja.
- **F6 Höchstzahl Messungen** (OF-5). *Annahme:* 4, nach Messung am Messrechner anpassen. *Bitte:* Arbeitsspeicher des Messrechners nennen, falls bekannt.
- **F7 Dieselbe Datei mehrfach öffnen.** *Annahme:* erlaubt mit Hinweis in AF (für Tests mit nur einer Beispieldatei).
- **F8 Spektrum-Teilgröße** (E13). *Annahme:* eine Größe „Spektrum (Amplitude)“ mit Teilgröße |CPH| oder √AP wie Ansicht 1.
- **F9 Phase in Ansicht 5:** absolut (gegen die Referenz, M8-gekennzeichnet) oder relativ zu einem Bezugspunkt wie in Ansicht 4? *Annahme:* absolut wie Ansicht 2 (H1-Phase), M8 gekennzeichnet, im Mittel nicht darstellbar.
- **F10 Auswahl je Messung** (Punkt, Komponenten, Kanalpaar) wird beim Wechsel der aktiven Messung zurückgesetzt. *Annahme:* ja (einfach); Merken je Messung wäre ein Zusatz (rund 0,5 Tage).
- **F11 Thesis:** Soll `darstellung_beispiel.py` ein Vergleichsdiagramm (Standbild) erzeugen? *Annahme:* nein, später.

**Blockierend:** keine. Zur Freigabe des Plans selbst: Reihenfolge der Etappen (A, B, C) und die Prüfpunkte nach S3, S7 und S9.

**Hinweis zum Review:** Reviewer nach S2 (Zoomumbau, Rückkopplung), S4 (Refaktor), S7 und am Ende (S10); Design-Abnahme `ui-designer` nach S3 (AG) und S9/S10 (Ansicht 5, Chips, Layout, Graustufen). Fachabnahme nur als Stichprobe der Legendentexte.
