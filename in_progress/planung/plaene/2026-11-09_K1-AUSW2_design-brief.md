<!-- Vom Nutzer am 2026-11-09 freigegeben; Annahmen A-1 bis A-7 und OF-3 bis OF-5 wie vorgeschlagen. OE-A1 (3D-Technik) offen, Analysepaket folgt. Reihenfolge: R-073, R-058, R-059 zuerst, R-071 nach Technikentscheidung. -->

<!-- Paket K1-AUSW2 (ui-designer), Stufe 2. Status: BRIEF ZUR FREIGABE (2026-11-09). Ergänzt Brief K-AUSW und K-AUSW-LAYOUT. Grunddesign vom Nutzer am 2026-11-09 bestätigt. -->

## Design-Brief: Erweiterung „Auswerten“ (R-073, R-058, R-059, R-071)

**Bezug:** Lastenheft R-073, R-058, R-059, R-071 (Quelle Betreuertermin 2026-11-09); Brief K-AUSW (`2026-11-03_K-AUSW_design-brief.md`), K-AUSW-LAYOUT; ADR-021 (matplotlib `Figure` + `FigureCanvasQTAgg`, nie `pyplot`), ADR-024 (Zeichenschicht `darstellung/`), ADR-025 (Phasendarstellung), ADR-026 (Tabellen), ADR-022 (Hintergrundladen); KONVENTIONEN (Winkel in Grad, ζ mit Methode und Band, Graustufentauglichkeit, kein Gelb, Mittelformel und Punktzahl im Bild, Achsen „Größe [Einheit]“, kein Diagrammtitel). Fachgrundlage zur Animation: **FG-04** (entsteht beim `strukturdynamik-experte`); der Brief verweist nur darauf.
**Bestätigt vom Nutzer (2026-11-09):** Grunddesign „Ja, passt so“. Animation **3D drehbar**. **Eine Größe je Diagramm**, verschiedene Größen nur nebeneinander als Teilbilder. Bis zu **vier Serien** je Diagramm. Neue Datei: Achsenbereiche zurücksetzen, Skalierung behalten. Punktzuordnung zwischen Messungen über das Punktlabel. Kein Video, nur Standbild. Farbbereich der Schwingform einstellbar.

**Nutzerziel und wichtigste Aktionen:** Jakob (fachkundig, Messrechner und Laptop, häufig per Remotedesktop, Lastenheft B2) will (1) Ausschnitte schnell einstellen, (2) zwei oder mehr Messungen nebeneinander oder überlagert prüfen, (3) eigene Diagramme zusammenstellen und als Bild speichern, (4) die Betriebsschwingform räumlich animiert ansehen.

---

### 1 Informationshierarchie und Layout

Das Zonenraster aus K-AUSW (AA bis AF) bleibt. Neu oder erweitert:

| Zone | Änderung |
|---|---|
| AA Dateileiste | Neben `Öffnen …` der Knopf `Messung hinzufügen …`. Je geöffneter Messung ein Chip „(A) Kurzname ×“; der aktive Chip ist hervorgehoben (Rahmen 2 px `C_AKZENT`, zusätzlich Wort/Symbol, nicht nur Farbe). Dateiname und Pfad der aktiven Messung wie bisher (Tooltip). Chips umbrechen nicht, bei Platzmangel wird die Chipzeile scrollbar. |
| AB Parameterzeile | Zeigt die Werte der aktiven Messung. |
| AC Ansichtswahl | Fünfter Knopf „5 Diagramm“ (Strg+5). Die Leiste muss um weitere Knöpfe erweiterbar bleiben (Andockstelle R-072). |
| AD Auswahlspalte | Ansicht 1 bis 3: wie K-AUSW, die Skalenwahl linear/logarithmisch entfällt dort (zieht in AG); dB bleibt in AD Ansicht 1. Ansicht 4: Abschnitt „Darstellung: Standbild \| Animation“ und Farbbereich. Ansicht 5: Serienliste, Größe, Anordnung (Abschnitt 3.2). |
| AE Darstellung | Werkzeugleiste, darunter **Achsenleiste AG**, darunter Plot; in Ansicht 4 im Modus Animation darunter die **Bedienleiste AH**. |
| AG Achsenleiste (neu, eine Zeile, Höhe nach dem 8-px-Raster) | Je sichtbarer Achse: Beschriftung, Feld „von“, Feld „bis“, Umschalter linear/logarithmisch; Knopf „Alles auf Auto“. |
| AH Bedienleiste Animation (neu, nur Ansicht 4, Modus Animation) | Abspielen/Pause, Einzelschritt zurück/vor, Phasenregler mit Gradanzeige, Tempo, Überhöhung, „Ansicht zurücksetzen“. |

- Ansichten 1 bis 4 arbeiten auf der **aktiven Messung**. Wechsel der aktiven Messung per Klick auf den Chip. Ansicht 5 greift auf alle geöffneten Messungen zu.
- Mindestgröße 1100×680 wie K-AUSW; AE bleibt bei 1366×768 mindestens 600×320 px **einschließlich** AG und AH. Reicht der Platz nicht, schrumpft zuerst der Plot, nicht die Leisten. AG und AH brechen bei Platzmangel in eine zweite Zeile um, kein Abschneiden von Feldern.

### 2 Visuelle Richtung

Unverändert aus K-AUSW: Fusion-Stil, Tokens aus `tokens.py`/`stil.py`, hell, flach, rechtwinklig, 8-px-Raster, Segoe UI, Consolas für Zahlen, Fokus 2 px `C_AKZENT`. Keine Verläufe und Schatten.
- **Serien (Ansicht 5):** Unterscheidung primär über Linienart (`LINIENARTEN`: durchgezogen, gestrichelt, punktiert, Strichpunkt), zusätzlich Serienfarbe aus `PLOT_SERIENFARBEN`. Höchstens vier Serien, Linienarten paarweise verschieden.
- **Legende:** unterhalb der Achse außerhalb des Plotbereichs, mit Linienprobe (Muster K-AUSW-LAYOUT 3.4); optional Direktbeschriftung am Kurvenende.
- **Animation:** Die Oberfläche selbst bleibt animationsfrei (K-AUSW Abschnitt 2); die Schwingform-Animation ist die einzige Ausnahme, und nur auf Anforderung des Nutzers. Auslenkungsfarbe: divergierende Skala, die in Graustufen nach Helligkeit trennt (Vorzeichen zusätzlich über die Form der Bewegung lesbar, nicht allein über Farbe); keine `hsv`/`jet`-Skalen (ADR-025).
- **Neue Tokens** nur in `tokens.py`; neue Kontrastpaare in `KONTRAST_PAARE`.

### 3 Komponenten und Inhalte

#### 3.1 Achsenleiste AG (R-073)

- **Achsen je Ansicht:** Ansicht 1 und 3: Frequenz, Betrag (Amplitude). Ansicht 2: Frequenz, Betrag, Phase (nur wenn „Phase anzeigen“ aktiv), Kohärenz bleibt fest 0 bis 1. Ansicht 5: Frequenz und y-Achse der gewählten Größe. Ansicht 4: keine Achsenleiste, stattdessen Farbbereich (3.3).
- **Felder:** `QDoubleSpinBox` bzw. Textfeld mit Dezimalkomma, Einheit als Suffix (Hz, Einheit der Größe, Grad bei Phase). Leeres Feld bedeutet „Auto“ (Platzhaltertext „Auto“). Phase in **Grad** (KONVENTIONEN).
- **Übernahme:** Wert wirkt bei Enter oder Fokuswechsel (kein Neuzeichnen bei jedem Tastendruck, Remotedesktop). Der Plot wird danach genau einmal neu gezeichnet.
- **Skalierung:** Umschalter „linear | logarithmisch“ je Achse (Frequenz und Betrag; Phase nur linear). Die Voreinstellung der Amplitude bleibt logarithmisch (OE-2 aus K-AUSW).
- **Rückkopplung:** Zoom und Verschieben der Werkzeugleiste und „Zurücksetzen“ schreiben den sichtbaren Bereich in die Felder; Eingabe in die Felder setzt den Plotbereich. Ein von Hand eingetragener Wert ist als „fest“ erkennbar (Feld hervorgehoben), automatische Grenzen stehen grau mit Wert.
- **Gültigkeit:** „von“ ≥ „bis“, bei logarithmischer Achse Werte ≤ 0, und nicht-numerische Eingaben zeigen eine Inline-Meldung unter dem Feld („✖ Unterer Wert muss kleiner sein als der obere.“, „✖ Bei logarithmischer Achse nur Werte größer null.“); der Plot bleibt unverändert, der alte Wert bleibt im Feld erhalten, sobald die Meldung quittiert wird (Fokuswechsel auf anderes Feld).
- **Persistenz:** Bereiche und Skalierung gelten **je Ansicht** und bleiben beim Wechsel von Messpunkt, Komponente, Größe, Mittel/Punkt, aktiver Messung und bei Hinzufügen/Entfernen einer Serie erhalten. Beim **Öffnen einer neuen Datei** (Ersetzen, nicht Hinzufügen einer weiteren Messung) werden die Bereiche zurückgesetzt, die Skalierung bleibt. Der Zoomzustand aus K-AUSW Abschnitt 4 geht in dieser Einstellung auf (eine Quelle).
- **Gemeinsame Zeichenschicht:** `darstellung/` bekommt Achsenoptionen (Grenzen, Skalierung je Achse) als Darstellungsoption; Oberfläche und Thesis-Skript nutzen sie gleich.
- **Ansicht 3:** Der Beschriftungsstreifen für Spitzenkästen (K-AUSW-LAYOUT 3.1) bleibt über der gewählten oberen Grenze reserviert; Spitzen außerhalb des Bereichs werden nicht beschriftet.

#### 3.2 Ansicht 5 „Diagramm“ (R-058, R-059)

**Messungsverwaltung (AA):**
- `Messung hinzufügen …` öffnet eine weitere `.svd` (Dateidialog wie `Öffnen …`, Ladevorgang nach ADR-022 im Hintergrund, Oberfläche bleibt bedienbar, Zustand „Laden“ je Messung). `Öffnen …` ersetzt wie bisher die aktive Datei oder die Messung (offene Frage OF-3).
- Kurzname je Messung: Voreinstellung „A“, „B“, …; per Doppelklick auf den Chip oder Feld in AD änderbar (Pflichtfeld, eindeutig); der volle Dateiname steht im Tooltip und im Bildstempel.
- Entfernen per × am Chip; Serien dieser Messung werden mit Hinweis entfernt (Bestätigung, wenn Serien betroffen sind).
- Eine Messung ist auch ohne Vergleichspartner in Ansicht 5 nutzbar (eigenes Diagramm mit mehreren Punkten einer Messung).

**Auswahl (AD, Ansicht 5):**
- **Größe** (Radioknöpfe, eine für das gesamte Diagramm): Spektrum (Amplitude), |H1|, |H2|, Kohärenz γ², Phase. Nicht verfügbare Größen (z. B. ohne Referenzkanal) deaktiviert mit Begründungstext neben dem Knopf. Die y-Achse trägt „Größe [Einheit]“ (Einheit aus Datei bzw. Quotient der Einheiten, nie umgerechnet).
- **Serienliste** (`QListWidget` mit Linienprobe, höchstens vier Einträge): je Zeile Linienprobe, Kurzname der Messung, Punkt bzw. „Mittel“, Komponente bzw. Kanalpaar. Knöpfe: `+ Serie`, `Bearbeiten`, `Entfernen`, Kontrollkästchen „sichtbar“. Ist die Grenze erreicht, ist `+ Serie` deaktiviert mit Text „Höchstens vier Serien; mehr Serien über ‚nebeneinander‘.“
- `+ Serie`/`Bearbeiten` öffnet einen kleinen Dialog (modal, mit Esc schließbar): Messung, Punkt oder „Mittel (alle Punkte)“, Komponente (X, Y, Z, 3D) bzw. Kanalpaar; nur zur Größe passende Angaben sind wählbar.
- `Aus aktueller Ansicht übernehmen`: Übernimmt die Auswahl der zuletzt benutzten Ansicht 1 bis 3 (aktive Messung, Punkt, Komponenten) als Serie(n), ersetzt keine vorhandenen.
- `Für alle Messungen`: Legt je geöffneter Messung eine Serie mit derselben Auswahl an (Punktzuordnung über das Label, Mittel immer möglich). Fehlt ein Label in einer Messung, wird diese Serie nicht angelegt und der Grund in AF gemeldet.
- **Anordnung:** „überlagert | nebeneinander“. Nebeneinander: je **Größe** ein Teilbild; bei einer Größe pro Diagramm heißt das: je **Messung** ein Teilbild mit gleicher Größe und gekoppelten Achsen (Kopplung abschaltbar nicht vorgesehen, vgl. OF-4). Verschiedene Größen in einem Diagramm sind nur über „nebeneinander“ möglich: dazu erlaubt die Serienliste im Modus „nebeneinander“ je Serie die Wahl der Größe, jedes Teilbild trägt eine Größe (Teilbild-Kopf nennt die Größe, y-Achse hat deren Einheit).

**Plot (AE):**
- Zeichenfunktion in `darstellung/`: GUI-frei, `Figure`-basiert, kein `pyplot`, Linienarten paarweise verschieden, Legende außerhalb der Achse, kein Diagrammtitel. Die Kopfzeile (Qt-Label) nennt Messungen, Größe und Anordnung.
- Legendeneintrag je Serie: „<Kurzname> · <Punkt/Mittel> · <Komponente>“ und, falls Mittel, Mittelformel und Punktzahl (z. B. „Betragsmittel |H1| über 135 Punkte“).
- Verschiedene Messungen behalten ihre eigene Frequenzachse (keine Interpolation, keine Differenzkurve).
- **Bild speichern:** wie K-AUSW 7; Stempel nennt Kurzname und Dateiname jeder beteiligten Messung, Ansicht, Git-Hash und bei unbestätigter Größe (Phase) „⚠ enthält unbestätigte Größen (M8)“.
- Textalternative des Plots (`accessibleDescription`) nennt Serien, Größe, Frequenzbereich.

#### 3.3 Ansicht 4 Animation (R-071)

- **Modus:** „Darstellung: Standbild | Animation“ in AD (Radioknöpfe). Voreinstellung Standbild (wie K-AUSW-LAYOUT); die Animation startet nie von selbst und ist pausiert, wenn der Modus gewählt wird.
- **Räumliche Darstellung:** Messpunkte (und, wo vorhanden, die Geometrie aus der Datei) im Raum, **drehbar und zoombar**. Drehen per Maus (Ziehen), Zoom per Mausrad und per Knöpfen, voreingestellte Ansichten per Knopf („Aufsicht xy“, „xz“, „yz“, „Isometrisch“, „Zurücksetzen“), alles auch per Tastatur (Pfeiltasten drehen, `+`/`-` zoomen, Pos1 setzt zurück). Die Standardblickrichtung folgt der gewählten Projektionsebene aus dem Standbild.
- **Bewegung:** Phase des Zeigers umlaufend nach FG-04; der Phasenregler zeigt den Winkel in Grad (0 bis 360°, einstellbare Schrittweite für Einzelschritte). Die dargestellte Phase und die Bewegung gehören zusammen: Der Standbildstand bei Winkel φ ist identisch mit dem Zustand der Animation bei φ.
- **Überhöhung:** Regler „Überhöhung“ skaliert die Auslenkung; der aktuelle Faktor steht als Zahl im Bild (damit Standbilder nicht als wahre Auslenkung gelesen werden). Wahrheitsgemäß „Überhöhung ×<Faktor>“ in Bild und Textalternative.
- **Farbbereich:** Min/Max der Farbleiste einstellbar (Felder „von/bis“ mit Einheit, „Auto“ bei leer); Farbleiste mit Einheit sichtbar. Auslenkung divergierend, Betrag einfarbig; die Wahl „Farbe zeigt: Betrag | Auslenkung“ ist in AD.
- **Gekennzeichnete Punkte** (unsicher γ² < γ²_min, ungültig M6) bleiben sichtbar und gekennzeichnet wie in ADR-025 und K-AUSW-LAYOUT 4.5, bewegen sich aber nicht mit unbestimmter Phase: Sie erscheinen im Ruhezustand (bzw. gemäß FG-04) und sind in der Zeichenerklärung aufgeführt.
- **Bedienleiste AH:** Abspielen/Pause (Leertaste bei Fokus im Plot), Einzelschritt (←/→), Phasenregler, Tempo, Überhöhung. Tempo einstellbar; Standardwert und Mindest-Bildrate werden am Messrechner und über Remotedesktop gemessen, nicht geschätzt (U-A2).
- **Kennzeichen:** „⚠ unbestätigt (M8)“ mit Begründung im Kopf der Animation (Qt-Label), dauerhaft sichtbar und im gespeicherten Standbild im Stempel.
- **Standbild speichern:** `Bild speichern …` speichert den aktuellen Phasenstand und die aktuelle Blickrichtung als PNG/PDF mit Stempel inkl. Winkel in Grad, Überhöhung, Frequenz, Datei und Git-Hash. Kein Video, kein GIF.
- **Darstellungstechnik (offene Entscheidung):** Der Brief legt die Technik nicht fest (siehe Abschnitt 13, OE-A1). Die gestalterischen Anforderungen sind unabhängig davon verbindlich.

### 4 Interaktionen und Zustände

| Zustand | Darstellung |
|---|---|
| Keine Datei | Wie K-AUSW; „Messung hinzufügen …“ deaktiviert (Tooltip „Zuerst eine Messdatei öffnen.“); Ansicht 5 zeigt „Noch keine Messdatei geöffnet.“ |
| Laden einer weiteren Messung | Chip mit Text „lädt …“ und Fortschrittsanzeige unbestimmt; bereits geöffnete Messungen bleiben bedienbar; Serien dieser Messung sind bis zum Laden nicht wählbar |
| Fehler beim Laden der zweiten Datei | Fehlerband (✖, Wort „Fehler“) mit Text des Lesers; bereits geöffnete Messungen unverändert |
| Ansicht 5 ohne Serie | Hinweis „Noch keine Serie. Mit ‚+ Serie‘ oder ‚Aus aktueller Ansicht übernehmen‘ beginnen.“ |
| Serie unmöglich (z. B. Größe |H1| ohne Referenzkanal in einer Messung) | Serie wird nicht gezeichnet, Meldung in AF mit Grund; in der Serienliste markiert (Symbol + Wort) |
| Gleiche Auswahl zweimal | Hinweis „Diese Serie gibt es bereits.“, keine zweite Linie |
| Fünfte Serie | `+ Serie` deaktiviert, Text siehe 3.2 |
| Achseneingabe ungültig | Siehe 3.1 |
| Animation | Zustände Pause, Läuft, Einzelschritt, mit Beschriftung der Abspielen-Taste („Abspielen“/„Pause“, nicht nur Symbol) |
| Animation, keine Referenz/Phase | Phase nicht verfügbar: Modus „Animation“ deaktiviert mit Text „Animation braucht eine Phase: keine Referenz.“ |
| Animation, Rechner zu langsam | Bildrate sinkt sichtbar nie unbemerkt: Hinweis in AF „Wiedergabe langsamer als eingestellt“; der Phasenregler bleibt unabhängig davon voll nutzbar |

**Neuzeichnen und Remotedesktop:**
- Eingaben in Zahlenfeldern lösen erst bei Enter/Fokuswechsel ein Neuzeichnen aus.
- Regler (Phase, Überhöhung): Während des Ziehens werden nur die betroffenen Zeichenobjekte aktualisiert (kein Voll-Neuzeichnen der Figur); sind Teilaktualisierungen am Messrechner/Remotedesktop nicht tragfähig, wird erst beim Loslassen neu gezeichnet (Rückfall, U-A2).
- Wiedergabe: Bildrate begrenzt und einstellbar; beim Ziehen oder Drehen pausiert die Wiedergabe.
- Das Verhalten ist am Messrechner über Remotedesktop zu prüfen und wird nie vor Bestätigung des Nutzers als bestanden gemeldet.

### 5 Responsives Verhalten

Desktop, kein Handy-Layout. AD bleibt 260 px. AG und AH brechen in eine zweite Zeile um, wenn AE zu schmal ist (kein Abschneiden). Nebeneinander (Ansicht 5): Teilbilder teilen die Breite gleichmäßig, bei mehr als zwei Teilbildern wird in Zeilen umbrochen; jedes Teilbild behält mindestens die Breite, in der Achsenbeschriftung und Zahlen lesbar sind (Testwert aus dem Raster, nicht geschätzt). HiDPI wie K-AUSW.

### 6 Accessibility

- Alle neuen Eingaben mit Beschriftung und Buddy, `accessibleName` je Knopf („Achsenbereich Frequenz von“, „Animation abspielen“ …). Chips sind per Tab und Tastatur wechselbar (Pfeiltasten, Entf entfernt nach Bestätigung).
- Farbe trägt nie allein Information: Serien über Linienart plus Legende; Animation divergierend nur zusammen mit Beschriftung der Farbleiste und Betrag der Auslenkung als Zahl in AF.
- Textalternative des 3D-Plots: Datei, Frequenz, Phasenwinkel, Überhöhung, Blickrichtung, größte Auslenkung (Zahl aus dem Rechenkern); die Tabelle der Auslenkungen je Punkt ist als Ersatz abrufbar (Knopf „Werte als Tabelle“, Soll).
- Kontraste: Text 4,5:1, Linien und Fokus 3:1; neue Paare in `KONTRAST_PAARE`.
- Sichtbarer Fokus überall, auch im 3D-Plot (Rahmen um AE). Tab-Reihenfolge: AA → AC → AD → AG → AE (Werkzeugleiste, Plot) → AH → AF.
- Tastaturkürzel: Strg+5 Ansicht 5; Alt+1/Alt+2 Reiter wie bisher; Leertaste Abspielen/Pause (Fokus im Plot oder AH); ←/→ Phase in Einzelschritten (Fokus im Animationsplot); Pfeiltasten drehen nur bei Fokus im 3D-Plot und wenn der Modus „Animation“ aktiv ist, sonst gilt die Cursorbelegung aus K-AUSW. Doppelbelegungen werden in `AKTIONS_TASTEN` an einer Stelle gelöst.

### 7 Technische Hinweise

- Neue Zeichenmodule in `darstellung/` (z. B. `diagramm.py`), GUI-frei, ohne `pyplot`; Achsenoptionen als gemeinsame Option für Ansicht 1 bis 3 und 5. Reine Anzeige-Logik (Serienverwaltung, Legendentexte, Gültigkeit der Achseneingaben, Kurzname-Eindeutigkeit, Wahl der aktiven Messung) als Funktionen ohne Qt, testbar.
- Mehrere Messungen: der Reiter muss mehrere geladene Messungen mit eigenem Cache halten; ADR-022 (Hintergrundprozess) gilt je Messung. Speicherbedarf der zweiten Messung ist am Messrechner zu prüfen (U-A1).
- Importregel unverändert: `gui` darf `auswertung` und `darstellung` importieren; `darstellung/` bleibt ohne Qt/`pyplot`. Keine neue Abhängigkeit ohne Freigabe (siehe OE-A1).
- Stabile `objectName`s (Vorschlag): `btn_messung_hinzu`, `chip_messung_<n>`, `achsenleiste`, `achse_f_von`, `achse_f_bis`, `achse_f_skala`, `achse_y_von`, `achse_y_bis`, `achse_y_skala`, `achse_phase_von`, `achse_phase_bis`, `btn_achsen_auto`, `btn_ansicht_5`, `liste_serien`, `btn_serie_neu`, `btn_serie_aus_ansicht`, `btn_serie_alle`, `rb_groesse_*`, `rb_anordnung_ueberlagert`, `rb_anordnung_nebeneinander`, `rb_modus_standbild`, `rb_modus_animation`, `animationsleiste`, `btn_abspielen`, `regler_phase`, `lbl_phase_grad`, `regler_ueberhoehung`, `feld_farbe_von`, `feld_farbe_bis`.
- Plot-Tests über die Figure-Struktur (Linienzahl, Linienarten, Achsengrenzen, Skalierung, Legendentext), nicht über Pixel.
- Betroffene Dateien (Vorschlag): `software/src/ldv_automation/gui/auswerten_reiter.py` (Messungsliste, Ansicht 5, AG, AH), `plotflaeche.py` (Achsen), `tokens.py`, `stil.py`, neue Dateien in `gui/` und `darstellung/`.

### 8 UI-Akzeptanzkriterien

Priorität M/S/K. Alle gegen die Beispieldatei `Input/20261012_ref_Mitte.svd` und synthetische Messungen, offscreen, ohne Hardware, wenn nicht anders vermerkt.

**R-073 Achsen**
- **UI-1 (M):** In Ansicht 1, 2, 3 und 5 gibt es je sichtbarer Achse ein Feld „von“ und „bis“ und einen Umschalter linear/logarithmisch (Frequenz, Betrag; in Ansicht 2 zusätzlich Phase in Grad). Nach Eingabe von Werten und Enter entsprechen `ax.get_xlim()`/`get_ylim()` den eingegebenen Werten (Toleranz 1e-9 relativ).
- **UI-2 (M):** Der Umschalter ändert `ax.get_xscale()`/`get_yscale()` zwischen `linear` und `log`; die Voreinstellung der Amplitude ist `log`, die der Frequenz `linear`.
- **UI-3 (M):** Wechsel von Messpunkt, Komponente, Mittel/Punkt, Größe oder aktiver Messung ändert Grenzen und Skalierung der Achsenleiste nicht (Test: Eingabe, Wechsel, Vergleich der Grenzen und Skalen).
- **UI-4 (M):** Ein Zoom oder Verschieben per Werkzeugleiste aktualisiert die Felder auf die sichtbaren Grenzen; ein Eintrag in die Felder setzt den Plotbereich. „Alles auf Auto“ stellt Autoskalierung her (Felder leer).
- **UI-5 (M):** Ungültige Eingaben (von ≥ bis; bei log Wert ≤ 0; Text statt Zahl) zeigen eine Inline-Meldung am Feld und lassen den Plot unverändert.
- **UI-6 (M):** Beim Öffnen einer neuen Datei (Ersetzen) sind die Bereiche zurückgesetzt, die Skalierung (linear/log) bleibt erhalten.
- **UI-7 (M):** Die Phase erscheint in der Achsenleiste und im Plot in Grad (nie in rad); Frequenz in Hz mit Dezimalkomma.
- **UI-8 (M):** In Ansicht 3 bleiben Spitzenkästen im Achsenbereich (K-AUSW-LAYOUT L3-1 bis L3-3 gelten für beliebige gesetzte Grenzen, soweit Spitzen im Bereich liegen).

**R-058 Vergleich**
- **UI-9 (M):** `Messung hinzufügen …` öffnet eine zweite `.svd`; danach gibt es zwei Chips mit eindeutigen Kurznamen, die Oberfläche bleibt während des Ladens bedienbar (ein Klick auf einen anderen Reiter wird verarbeitet).
- **UI-10 (M):** In Ansicht 5 lässt sich dieselbe Ansicht (Spektrum, |H1| oder Kohärenz) für beide Messungen **überlagert** (eine Achse, mindestens zwei Linien, Linienarten paarweise verschieden) und **nebeneinander** (zwei Teilbilder mit gekoppelten Achsen) zeigen; in beiden Fällen nennt die Legende bzw. der Teilbildkopf je Linie den Kurznamen der Messung.
- **UI-11 (M):** Jede Linie ist eindeutig beschriftet: Legendeneintrag „<Kurzname> · <Punkt/Mittel> · <Komponente>“ ohne Doppelungen; bei Mittel zusätzlich Mittelformel und Punktzahl (Zahl aus den Daten).
- **UI-12 (M):** `Für alle Messungen` legt je geöffneter Messung eine Serie mit gleicher Auswahl an; bei fehlendem Label einer Messung wird die Serie nicht angelegt und der Grund in AF gemeldet.
- **UI-13 (M):** Verschiedene Messungen werden mit ihrer eigenen Frequenzachse gezeichnet (Test: Linienlänge je Serie gleich der jeweiligen Linienzahl, keine Interpolation).
- **UI-14 (M):** Entfernen einer Messung entfernt ihre Serien und zeigt vorher eine Bestätigung, wenn Serien betroffen sind.

**R-059 Eigene Diagramme**
- **UI-15 (M):** Aus mindestens zwei Messpunkten **oder** zwei Messungen entsteht in Ansicht 5 ein gemeinsames Diagramm mit gewählter Größe und Legende (zwei Linien, Achse „<Größe> [<Einheit>]“, Einheit stimmt mit dem Quotienten der Einheiten überein).
- **UI-16 (M):** Das Diagramm hat genau eine Größe; die Radioknöpfe lassen nur eine zu. Im Modus „nebeneinander“ trägt jedes Teilbild eine eigene Größe, im Teilbildkopf genannt, mit eigener y-Achse und Einheit.
- **UI-17 (M):** Nicht verfügbare Größen (z. B. ohne Referenzkanal) sind deaktiviert mit Begründungstext; eine nicht darstellbare Serie wird nicht gezeichnet und in AF begründet gemeldet.
- **UI-18 (M):** Höchstens vier Serien; bei vier ist `+ Serie` deaktiviert mit dem im Brief genannten Text; die Linienarten der Serien sind paarweise verschieden (Test: Figure-Struktur).
- **UI-19 (M):** `Bild speichern …` in Ansicht 5 schreibt PNG und PDF; im Bild stehen Legende, alle beteiligten Dateinamen und Git-Hash im Stempel; Größen mit unbestätigter Phase zeigen „⚠ enthält unbestätigte Größen (M8)“. Die Zeichenfunktion ohne Stempel enthält diese Texte nicht.
- **UI-20 (M):** Das Diagramm ist graustufentauglich: die Linien sind allein über Linienart und Legende unterscheidbar (Test: Figure-Struktur; Sichtprüfung nach Graustufenumsetzung bei der Abnahme).
- **UI-21 (S):** Serien lassen sich per Kontrollkästchen aus- und einblenden, ohne den Zoom oder die Achsenwerte zu ändern.

**R-071 Animation**
- **UI-22 (M):** In Ansicht 4 gibt es den Modus „Animation“. Voreinstellung nach dem Öffnen und bei Frequenzwechsel ist „Standbild“, und die Animation läuft nie ohne Nutzeraktion.
- **UI-23 (M):** Bei gewähltem Modus und gewählter Frequenz zeigt die Oberfläche die Messpunkte im Raum (drehbar); Drehen (Mausziehen), Zoom (Mausrad) und die Knöpfe „Aufsicht xy“, „xz“, „yz“, „Isometrisch“, „Zurücksetzen“ ändern die Blickrichtung bzw. stellen sie wieder her (Test über Aufruf der Zeichen- bzw. Ansichtsschnittstelle, nicht Pixel).
- **UI-24 (M):** Der Phasenregler zeigt den Winkel in Grad (0 bis 360°); „Abspielen“ lässt den Winkel umlaufen, „Pause“ hält ihn an, Einzelschritte ändern ihn um die eingestellte Schrittweite.
- **UI-25 (M):** **Phase = dargestellte Phase:** Für einen Winkel φ sind Auslenkungen im Animationszustand und im Standbild (Phasendarstellung nach ADR-025/FG-04) identisch (Test: Zustand bei φ stimmt mit Referenzwerten aus FG-04 an mindestens zwei Winkeln und zwei Punkten mit bekannter Phase überein; Toleranz aus FG-04).
- **UI-26 (M):** Die Überhöhung ist einstellbar; der Faktor steht als Zahl im Bild, in der Textalternative und im gespeicherten Standbild.
- **UI-27 (M):** Der Farbbereich (von/bis mit Einheit) ist einstellbar; die Farbleiste mit Einheit ist sichtbar; Eingabe ungültiger Werte zeigt die Inline-Meldung wie UI-5.
- **UI-28 (M):** „⚠ unbestätigt (M8)“ mit Begründung steht im Kopf der Animation, solange M8 offen ist; es verschwindet ohne GUI-Änderung, wenn `ist_annahme` für M8 `False` ist (wie K-AUSW UI-11); dasselbe Kennzeichen steht im gespeicherten Standbild.
- **UI-29 (M):** Gekennzeichnete Punkte (unsicher, M6-ungültig) sind in der Animation sichtbar, mit demselben Symbol wie im Standbild, und in der Zeichenerklärung mit Anzahl aufgeführt.
- **UI-30 (M):** Ohne Phase (keine Referenz) ist der Modus „Animation“ deaktiviert mit Text „Animation braucht eine Phase: keine Referenz.“
- **UI-31 (M):** `Bild speichern …` im Modus Animation schreibt den aktuellen Phasenstand und die aktuelle Blickrichtung als PNG/PDF; im Stempel stehen Winkel in Grad, Überhöhung, Frequenz, Datei und Git-Hash. Es gibt keine Funktion zum Speichern als Video oder GIF.
- **UI-32 (S):** Die Animation ist ohne Wiedergabe voll bedienbar: alle Aussagen (Phasenstand, Auslenkungen) sind über den Phasenregler und die Tastatur (←/→) zugänglich.
- **UI-33 (M):** Die Zeichenfunktion der Animation importiert weder Qt noch `pyplot` (Importtest), soweit die Technikentscheidung (OE-A1) dies zulässt; weicht sie ab, wird die Abweichung als ADR festgehalten.

**Allgemein**
- **UI-34 (M):** Strg+5 wechselt zu Ansicht 5; Tab-Reihenfolge entspricht Abschnitt 6; jedes bedienbare Widget hat `focusPolicy` ≠ `NoFocus`; der Fokus ist überall (auch im 3D-Plot) sichtbar.
- **UI-35 (M):** Neue Kontrastpaare stehen in `KONTRAST_PAARE` und der vorhandene Kontrasttest besteht.
- **UI-36 (M):** Bei 1100×680 überlappt kein Element (AA mit Chips, AG, AH, AE); AE ist bei 1366×768 mindestens 600×320 px groß.
- **UI-37 (M):** Eingaben in Zahlenfeldern lösen kein Neuzeichnen vor Enter oder Fokuswechsel aus (Test: Zahl der Zeichenaufrufe).
- **UI-38 (nicht prüfbar offscreen, Hardwaretest):** Bedienung der Achsenleiste, des Phasenreglers und der Animation über Remotedesktop am Messrechner ist flüssig und lesbar; Ergebnis vom Nutzer bestätigt (nie vor Bestätigung als bestanden melden).

### 9 Annahmen

- A-1 Ansichten 1 bis 4 laufen auf der aktiven Messung; Ansicht 5 auf allen geöffneten.
- A-2 Die Skala linear/logarithmisch der Amplitude zieht aus AD in AG; dB bleibt in AD.
- A-3 Mehrere Messungen haben dieselbe Einheitenart je Größe; sonst Serie nicht darstellbar (UI-17).
- A-4 Punktzuordnung zwischen Messungen über das Punktlabel; fehlt das Label, wird die Serie nicht angelegt.
- A-5 Die Geometrie der Messpunkte kommt aus `Punkte.koordinaten_m` (wie Ansicht 4); eine Flächengeometrie aus der Datei ist nur Kann.
- A-6 Die Zeigerbewegung (Vorzeichen, Bezug, Amplitudenskala) wird von FG-04 festgelegt; die Oberfläche rechnet nicht selbst.
- A-7 Bei Thesis-Abbildungen genügt weiterhin das Standbild (Phasen-Pfeile, ADR-025); die Animation selbst ist nur ein Oberflächenwerkzeug.

### 10 Offene Entscheidungen und Umsetzerfragen

**Offene Entscheidung (Entwurfsentscheidung mit Alternativen, nicht im Brief entschieden):**
- **OE-A1 Darstellungstechnik der 3D-Animation:** Alternativen z. B. matplotlib `mplot3d` innerhalb ADR-021 (keine neue Abhängigkeit, aber begrenztes Tempo, `Figure` und `FigureCanvasQTAgg`) gegenüber einer zusätzlichen 3D-Bibliothek (anderes Tempo, neue Abhängigkeit, Wheelhouse am Messrechner, `darstellung/`-Regel ohne Qt). Die Bewertung erfolgt in einem Analysepaket (`software-engineer`), anschließend legt der Nutzer fest und die ADR entsteht. Gestalterische Anforderungen an jede Lösung: Drehen und Zoomen per Maus und Tastatur, Bedienbarkeit und Lesbarkeit über Remotedesktop (Bildrate einstellbar, Teilaktualisierungen oder Neuzeichnen beim Loslassen), Graustufentauglichkeit (divergierende Skala mit Helligkeitstrennung, Formkennzeichnung gekennzeichneter Punkte), Standbild identisch mit der Phasendarstellung, dauerhaftes Kennzeichen M8, gespeichertes Standbild mit Stempel (UI-31). Diese Anforderungen sind die Prüfgrundlage der Analyse.
- **OE-A2 Nach Analyse:** Ist das 3D-Tempo über Remotedesktop mit der gewählten Technik vertretbar? Wenn nicht, was gibt der Nutzer vor (z. B. nur Einzelschrittbetrieb)? Auswirkung: Umfang der Wiedergabefunktion.

**Offene Fragen mit Annahme:**
- OF-3 `Öffnen …` ersetzt die aktive Messung; `Messung hinzufügen …` ergänzt. *Annahme:* ja.
- OF-4 Achsenkopplung im Modus „nebeneinander“ ist nicht abschaltbar. *Annahme:* ja, vorerst fest gekoppelt.
- OF-5 Höchstzahl gleichzeitig geöffneter Messungen: *Annahme:* durch Speicher begrenzt, am Messrechner zu prüfen (U-A1).

**Zu klären durch den Umsetzer (nicht als Annahme einführen):**
- U-A1 Speicherbedarf und Ladezeit einer zweiten Messung (ADR-022: Ansicht 1 nach etwa einer Sekunde, Prüfung mehrere Sekunden); Verhalten am Messrechner.
- U-A2 Tempo von Zeichnen, Teilaktualisierung und Wiedergabe über Remotedesktop; Mindest-Bildrate und Voreinstellung durch Messung am Messrechner festlegen.
- U-A3 Auslenkungsdarstellung der Punkte ohne Phase (unsicher/M6) nach FG-04.
- U-A4 Konflikte der Tastenbelegung (Pfeile, Leertaste) mit Cursortasten aus K-AUSW 8.

**Nicht enthalten:** Differenz- oder Verhältniskurven; Interpolation auf gemeinsames Gitter; Umrechnung der Größen; Speichern der Animation als Video oder GIF; R-070 (Koordinatentransformation) und R-072 (PSV-Visualisierungen), die nur Andockstellen haben (Auswahl „Koordinatensystem“ in AD der Ansicht 4, weitere Ansichten in AC); Änderungen am Reiter „Messen“; Thesis-Abbildungen der Animation (Standbilder per Skript, ADR-027).
