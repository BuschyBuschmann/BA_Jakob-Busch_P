# Analyse A1-B13: Abgleich (R-003) und Benachrichtigung (R-025)

Stand: 2026-11-09 · Paket A1-B13 (Analyse, read-only) · Repo-Stand `204033e`
Grundlage: Lastenheft (R-003, R-025, O9, O10), I1, I5, I5-F, CHM-Textfassung
(`in_progress/analysen/polytec-chm-text/basic-engine-manual/`), Polytec-Schulungsunterlage 07
(3D-Abgleich) und Software-Handbuch PSV (Abschnitt 5, PDF-Text), Erkundungsberichte vom
2026-11-02, Faktenliste, Code unter `software/src/ldv_automation/`.

Kennzeichnung: **[belegt: Quelle]** steht in Dokumentation oder Code; **[Annahme]** meine
Schlussfolgerung; **[offen]** nicht belegt, am Gerät oder vom Betreuer zu klären;
**[Wissen]** allgemeines Wissen über Webex/SMTP, nicht im Repo belegt, vor der Umsetzung gegen
die aktuelle Dienstedokumentation zu prüfen.

---

## Kurzfassung

| | R-003 Abgleich | R-025 Benachrichtigung |
|---|---|---|
| Machbarkeit | **Status und Qualität lesen und protokollieren: machbar** (dokumentiert, am Gerät noch nie gelesen). **Abgleich per COM neu berechnen lassen (Abgleichscan): kein Beleg, dass das per COM startbar ist; als „nicht machbar mit vertretbarem Aufwand“ einzustufen.** Abgleich laden (aus `.set`): schon freigegeben. | **Machbar** mit Standardbibliothek (Webex per HTTPS, E-Mail per SMTP). Hängt von Institutszugang, Konto und Netzfreigabe ab (alles [offen]). |
| Größtes Risiko | Laser/Spiegel bewegen sich; GUI-Funktion ohne COM-Gegenstück; Aufsichtspflicht | Zugangsdaten auf gemeinsamem Messrechner; Nachrichtenflut; Zustellfehler dürfen Messung nie stören |
| Andockpunkt | `geraet/schnittstelle.py` (neue Leseschnittstelle), `geraet/com/richtlinie.py` (Lese-Freigabe), `ablauf/steuerung.py::_protokolliere` | `sitzung.py::_bei_ablauf` bzw. `Steuerung(bei_ereignis=…)` |
| Offene Entscheidung des Betreuers | Was heißt „Abgleich ausführen“ (lesen, laden, neu berechnen)? | Kanal, Konto, Empfänger, Netzfreigabe, Nachrichtenmenge |

Empfehlung: R-003 im Lastenheft von „führt den Abgleich aus“ auf **zwei Stufen** schneiden
(Stufe 1: Status/Qualität lesen und protokollieren, Stufe 2: gespeicherten Abgleich laden und
gegen Qualitätsgrenze prüfen), die Neuberechnung ausdrücklich als nicht per COM belegt
ausweisen und dem Betreuer als Entscheidung vorlegen (Fragen A1 bis A4).

---

## 1 R-003: 2D- und 3D-Abgleich über COM

### 1.1 Was die Dokumentation hergibt

**Objektpfad [belegt: BEM PSV~AlignmentsAcq, PSV~InfosAcq]:**
`Application.Acquisition.Infos.Alignments` liefert `AlignmentsAcq` mit den Eigenschaften
`Alignments2D`, `Alignments3D`, `AlignmentsCamera` und `GetVideoRect()`. Die Typen stammen aus
`POLYALIGNMENTLib`. In Dateien (`.svd`) gibt es dieselben Objekte über Polytec File Access
(`POLYFILELib~Alignments`, „Available in MPV/PSV files only“).

**Lesbare Größen [belegt: BEM POLYALIGNMENTLib~Alignment3D_members, Alignment2D_members,
AlignmentCamera_members; I5 2.7 und Abschnitt 6]:**

| Objekt | Lesbar | Einheit laut Doku |
|---|---|---|
| `Alignment3D` | `Valid`, `CurrentQuality`, `TargetQuality`, `PositionUncertainty`, `AngleUncertainty`, `CoordDefinitionMode`, `Mirror`, `ScanHeadType`, `ScanQuantity`, `Align3DPoints`/`Align3DPointsRef`, `GetScanHeadPosition(x,y,z)` | Qualität und Positionsunsicherheit in m, Winkelunsicherheit in rad |
| `Align3DPoint` | `Quality`, `PointType`, `Label`, `X/Y/Z`, `ScannerX/Y`, `VideoX/Y`, `Distance`, `Caps` | Qualität in m, Scannerwerte bei PSV in Grad |
| `Alignment2D` | `Valid`, `ScanHeadDistance`, `Align2DPoints`/`Align2DPointsRef`, `ScanHeadType`, `ScannerQuantity` | Abstand in m |
| `AlignmentCamera` | `Valid`, `CurrentQuality`, `TargetQuality`, `CamPos*`, `CamVec*`, `ViewUp*`, `ViewAngle`, `Mirror`, `Persistent` | ViewAngle in Grad |

Das Mindestpunktmaß für die Berechnung steht im Enum
`PTCAlignment3DMinMaxPointCount`: mindestens 4 Abgleichpunkte (3 Objektpunkte), höchstens 5000.

**Methoden, die einen Abgleich verändern [belegt: BEM]:**

- `Alignment3D.Calculate(Align3DPoints, PTCCoordDefinitionMode, Mirror, TargetQuality, IScanHeadScanner)`
  berechnet einen 3D-Abgleich **aus übergebenen Punkten**. Die Punkte müssen vorher mit
  Scannerwinkeln (`ScannerX/Y`), Videokoordinaten und je nach Modus Entfernung oder 3D-Koordinaten
  gefüllt sein. `Alignment3D.Invalidate()` verwirft den Abgleich.
- `Alignment2D.Calculate(Align2DPoints, IScanHeadScanner, TrapezoidCorrection)` und
  `Alignment2D.Invalidate()` analog.
- `AlignmentCamera.Calculate(...)`, `SetCamera`, `ResetCamera` für den Kameraabgleich.
- Der Hilfstyp `PolyMathLib.Transform3DProcessing` (`CalculateTransformation`,
  `CalculateTransformationAndQuality`, `Transform3DPoints`) rechnet eine Koordinatentransformation
  zwischen zwei Systemen. **Ein Objekt namens `Transformation3D` kommt in der CHM-Textfassung
  nicht vor** (Suche über `polytec-chm-text/`); gemeint ist vermutlich `Transform3DProcessing`
  (verwandt mit `Acquisition.FindPointMarkers`/`MatchPointMarkers`, die laut Doku zum Ausgleich
  einer Objektbewegung auf einen vorhandenen 3D-Abgleich angewendet werden können).
- Ein Abgleich lässt sich außerdem **laden**: `Settings.Load(pfad, ptcSettings2DAlignment |
  ptcSettings3DAlignment | ptcSettingsCameraAndAlignment)`; eine `.set` enthält Erfassungsparameter,
  Scanpunkte, 2D-/3D-Abgleich und Optik [belegt: I5 2.4, BEM PSV~PTCSettings].

### 1.2 Ist ein Abgleichscan per COM startbar?

Antwort: **Nein, ein COM-Aufruf dafür ist nicht belegt** (Aussage über die vorhandene
Dokumentation, kein Beweis der Nichtexistenz).

- Die Mitgliederlisten von `Acquisition` (Methoden: `AssignFocusAutomatically`, `AutoFocusLaser`,
  `CalculateFocusValues`, `ExportVideoSnapshot(Ex)`, `GeometryScan`, `GetData`, `GetLaserOn`,
  `GetSelectedMeasPoints`, `GetSignalAmplitudes`, `MatchPointMarkers`, `MeasurePathLength`,
  `PathLengthScan`, `Scan`, `ScanEx`, `SetLaserOn`, `SetSelectedMeasPoints`, `Start`, `Stop`,
  `TakeReferenceSnapshot`, `TakeSnapshotAndGetPixelCoordinates`), `Application` und `Settings`
  enthalten keine Methode für „2D-Abgleichscan“, „Automatischer 3D-Abgleich“ oder „Objektabgleich“.
  [belegt: BEM PSV~Acquisition_members, PSV~Application, PSV~Settings]
- Das Handbuch beschreibt alle Abgleichvorgänge als Dialogbedienung: 2D-Abgleichscan über
  „Scan > 2D-Abgleichscan“ (Dialog, mindestens 4 definierte Scanpunkte, Laser positioniert und
  fokussiert selbst), automatischer 2D-Abgleich per Mausklick auf das Videobild, 3D-Abgleich
  klassisch mit Geo-Laser oder Referenzobjekt, **automatischer 3D-Abgleichscan** mit dem optionalen
  Abgleichobjekt PSV-A-655 (QR-Codierung; Dialog „3D-Abgleichscan“, Autofokus, Soll-Genauigkeit,
  „Abgleichscan starten“). [belegt: Software-Handbuch PSV, Abschnitt 5.1.2 und 5.2.6;
  Schulungsunterlage 07, Folien 19 bis 23]
- Der automatische 3D-Abgleich **funktioniert nicht mit Koaxialeinheit** am Scankopf; er braucht
  das Abgleichobjekt PSV-A-655, gut zentriert vor den drei Scanköpfen, und setzt für die Auswertung
  ein gutes Videobild voraus. [belegt: Handbuch 5.2.6]
- Der **Selbstbau** über COM wäre möglich in dem Sinn, dass `Calculate` die Mathematik bereitstellt.
  Er verlangt aber, dass die Software selbst (a) die Spiegel positioniert (dafür gibt es
  `PolyScanHeadLib.ScannerControl.SetBeamPosition`; ob das Objekt aus dem PSV-Objektmodell
  erreichbar ist, ist **[offen]**; `Acquisition.SetLaserOn(…, moveLaser)` bewegt den Laser nur auf
  einen Rand bzw. schaltet), (b) den Laserpunkt im Videobild findet (Bildverarbeitung auf
  `ExportVideoSnapshot`; die kontrastreiche Laseranzeige ist eine GUI-Funktion), (c) Geo-Laser-
  Entfernungen oder Referenzkoordinaten liefert. Das wäre eine Nachbildung der Polytec-
  Abgleichalgorithmik. **[Einschätzung] Nicht empfehlenswert** innerhalb einer Bachelorarbeit,
  Genauigkeit und Gültigkeit wären nicht mit der PSV-Rechnung vergleichbar.
- **Zusatzbefund aus dem Code:** `Alignment3D.Calculate` steht heute im Testkatalog
  „Nie freigegeben“ (`geraet/com/richtlinie.py`, `NIE_KATALOG`, ebenso `SetLaserOn`,
  `AutoFocusLaser`, `GeometryScan`, `PositionDevice.StartMove*`). Jede Freigabe wäre eine neue,
  einzeln begründete schreibende Operation (S-Nummer, Prüfung, Test) mit Review (ADR-007).

**Daraus folgt:** Ein „Abgleich ausführen“ im Sinn von Neuberechnen bleibt Bedienung am Gerät
(Nutzer führt in PSV den Abgleichscan aus). Was die Software leisten kann, ist Status lesen,
Abgleich aus `.set` laden und das Ergebnis bewerten und protokollieren.

### 1.3 Was bereits im Projekt geschieht (wichtig für die Einordnung)

- Die Software lädt vor jeder Messung die `.set` mit der Lademaske
  `Acquisition|Alignment|APS|2DAlignment|3DAlignment` (Vorgabe, `konfig.py`, `richtlinie.py::
  STANDARD_LADEMASKE`; im Messprotokoll als `lademaske`). **Jedes `lade_einstellungen` ersetzt
  damit den aktuell in PSV eingestellten Abgleich durch den in der `.set` gespeicherten.**
  [belegt: Code, I5 2.4] Stimmt die `.set` nicht mit der realen Aufstellung überein (Objekt
  verschoben, anderer Abstand), misst der Scan mit falscher Geometrie. Das Messprotokoll
  hält heute weder Gültigkeit noch Qualität des Abgleichs fest. Das ist die eigentliche
  Lücke, die R-003 schließen kann.
- Der Versuchsplan `2026-11-09_pruefdateien-warteschlange` sagt ausdrücklich: „Koordinatensystem
  und Alignment wie Beispielmessung (in PSV; Software ändert nichts daran).“
- `software/tools/erkundung/erkundung.py` enthält bereits einen Leseversuch `P1-6-abgleich`
  (`Valid`, `CurrentQuality`, `TargetQuality`, `PositionUncertainty`, `AngleUncertainty`).
  **Er lief am 2026-11-02 nie**: Der Bericht 161125 zeigt `P1-6-abgleich` als „übersprungen
  (Acquisition nicht erreichbar)“, in den Berichten 143255 und 150024 steht „nicht ausgeführt“.
  Die Frage „Sind `Infos.Hardware` und `Alignments3D` im Erfassungsmodus lesbar?“ ist also
  **am Gerät [offen]**. Ebenso offen: Indexbasis von `Alignments3D.Item` (I5 P2-12) und Zahl der
  Einträge (Vermutung: je Scankopf eins, `MAX_ALIGNMENTS = 3` im Skript).

### 1.4 Ergebniswerte für das Messprotokoll (Vorschlag zu O9)

Alle Felder nur lesend. Einheit im Feldnamen (KONVENTIONEN), Phasen/Winkel in rad, Längen in m.
Nicht lesbar heißt `null` plus Grund in `nicht_lesbar` (wie bei `frequenzachse`).

| Feld (Vorschlag) | Quelle | Beleg |
|---|---|---|
| `abgleich_3d[i].gueltig` | `Alignment3D.Valid` | [belegt: BEM] |
| `abgleich_3d[i].qualitaet_ist_m`, `qualitaet_soll_m` | `CurrentQuality`, `TargetQuality` | [belegt: BEM] |
| `abgleich_3d[i].positionsunsicherheit_m`, `winkelunsicherheit_rad` | `PositionUncertainty`, `AngleUncertainty` | [belegt: BEM] |
| `abgleich_3d[i].koordinatenmodus`, `spiegel` | `CoordDefinitionMode`, `Mirror` | [belegt: BEM] |
| `abgleich_3d[i].kopfposition_m` | `GetScanHeadPosition` | [belegt: BEM]; Koordinatensystem = das des Abgleichs |
| `abgleich_3d[i].punkte_anzahl` | `Align3DPoints.Count` | [belegt: BEM]; Bedeutung bei automatischem Abgleich [offen] |
| `abgleich_2d[i].gueltig`, `scankopfabstand_m` | `Alignment2D.Valid`, `ScanHeadDistance` | [belegt: BEM] |
| `abgleich_kamera.gueltig`, `qualitaet_ist_m` | `AlignmentCamera.Valid`, `CurrentQuality` | [belegt: BEM] |
| `abgleich_herkunft` | SHA-256 der geladenen `.set` (liegt schon als `einstellungsdatei.sha256` vor), Lademaske | [belegt: Code] |
| Zeitpunkt des Lesens | `Uhr.jetzt()` | [belegt: Code] |

Nicht aufnehmen (zu aufwendig, kein Mehrwert für die Anforderung): Punktlisten je Abgleichpunkt
(`Align3DPoint.Quality` je Punkt) und eine „Konditionszahl“; letztere gibt die Doku nicht her
[offen: wäre Eigenrechnung aus den Punkten]. Als Wert zur Einordnung nennt Polytec für den
automatischen Abgleich die Winkelgenauigkeit als wichtigsten Indikator, Faustregel 0,1 mrad
entsprechen 0,1 mm auf 1 m. [belegt: Schulungsunterlage 07, Folie 22] Eine **Grenzwert**-Aussage
(„Abgleich gut genug“) braucht eine Vorgabe des Betreuers (Frage A3).

### 1.5 Passung in den Code

**Adapter und Schnittstelle**
- `geraet/schnittstelle.py::Messgeraet` ist ein `runtime_checkable` Protocol. Eine Methode
  anhängen ändert die strukturelle Prüfung für alle Implementierungen und Test-Fakes
  (`tests/geraet_com`, `tests/gui/gui_hilfen.py`). **Empfehlung:** ein eigenes kleines Protocol
  (z. B. `Abgleichsleser` mit `lies_abgleich() -> AbgleichStand`) neben `Messgeraet`, das Simulator
  und COM-Adapter zusätzlich erfüllen; die Steuerung prüft per `isinstance`. Alternative: Der
  Abgleich wird Teil von `EinstellungsStand` (dort liest der Adapter ohnehin nach `Settings.Load`).
  Das hält die Schnittstelle schmal, vermischt aber „Einstellungen“ und „Aufstellung“.
- `geraet/com/richtlinie.py`: reine **Lesefreigaben** analog `HARDWARE_LESEN`:
  `Infos` bekommt `Alignments` (derzeit nur `HasHardware`, `HasMeasPoints`, `Hardware`,
  `MeasPoints`), neue Typen `Alignments`, `Alignments3D`/`Alignment3D`, `Alignments2D`/
  `Alignment2D`, `AlignmentsCamera`. Lesefreigaben haben keine Wirkung auf das Gerät
  (Moduldoku der Richtlinie). Erkundungsskript und Proxy-Modell liegen schon vor
  (`erkundung.py`: `Alignments3D` mit `Count`/`Item`).
  Jede neue Freigabe braucht einen Test im Katalog `tests/geraet_com/`.
- `geraet/simulator.py`: `SimulatorKonfiguration` bekommt einen Abgleichzustand (z. B. gültig,
  Qualitäten, ein „Abgleich ungültig“-Drehbuchereignis wie bei den vorhandenen `LadeFehler`/
  `Haenger`). Die Pflicht „Simulator der Schnittstelle“ aus KONVENTIONEN gilt.
- Geladene `.set` und Abgleich hängen zusammen: Der Simulator sollte den Abgleichzustand **mit
  `lade_einstellungen`** wechseln lassen (jede `.set` bringt ihren eigenen), sonst bildet er den
  eigentlichen Fehlerfall (veralteter Abgleich in der `.set`) nicht ab.

**Steuerung und Protokoll**
- Lesepunkt: unmittelbar nach `Settings.Load` bzw. vor `starte_scan` in
  `ablauf/steuerung.py::_fuehre_messung_aus` (dort entsteht auch `einstellungen_ist`).
  [Annahme] Der Abgleichstand wird wie der Einstellungsstand je Messung erhoben und in
  `_Aktiv` mitgeführt.
- Ablage: neues Feld `abgleich` im Messprotokoll (`protokoll/messprotokoll.py`,
  `PFLICHTFELDER`, `_protokolliere` in `steuerung.py`). Das ist eine inhaltliche Änderung:
  nach KONVENTIONEN erhöht jede inhaltliche Änderung die `schema_version`, **außer** die Version 2
  ist noch nicht ausgeliefert (dann bleibt sie unter derselben Version; Stand dazu [offen],
  vor der Umsetzung prüfen).
- Je Messung Momentaufnahme ist sinnvoll, weil Abgleich und `.set` je Messung wechseln können.
  Alternative: ein eigener Warteschlangeneintrag „Abgleich prüfen“ (wie `Pausenpunkt`). Das ist
  deutlich größer (neuer Eintragstyp in `domaene/eintraege.py`, Persistenz, GUI) und für Stufe 1
  nicht nötig.
- Bewertung/Gate: Abgleich ungültig bzw. Qualität schlechter als Grenzwert führt zu
  `FehlerArt.VORPRUEFUNG` (Vorprüfung, kein Scan gestartet, die Fehlerstrategie greift wie bei
  O1). Ob die Messung nur gewarnt oder verweigert wird, entscheidet der Betreuer (A5).

### 1.6 Risiken R-003

| Risiko | Einschätzung |
|---|---|
| Laser/Spiegel bewegen sich bei jedem Neuberechnen am Gerät; Laserschutz | Betrifft nur Stufe 3 (Neuberechnen); Stufe 1 und 2 bewegen nichts [Annahme: Lesen bewegt nichts, am Gerät bestätigen; `Settings.Load` mit Kamera-Bits könnte die Optik bewegen, deshalb ist `Camera` nicht in der Lademaske, siehe `richtlinie.py`]. KONVENTIONEN „Service- und Kalibriermethoden werden nie aufgerufen“; I5: „Laser- und Generator-Aktionen nur bewusst und mit Bestätigung“. |
| Blockierende PSV-Dialoge während Abgleich | `SuppressMessagesForAutomation` ist gesetzt (ADR-010); wie PSV bei Abgleichfehlern reagiert, ist **[offen]**. |
| Abgleich aus `.set` passt nicht zur Aufstellung (still falsche Geometrie) | Real und heute unprotokolliert. Stufe 1 macht ihn sichtbar, entdeckt aber nur ungültige oder schlechte Abgleiche, nicht einen verschobenen Aufbau. Gegenmaßnahme am Gerät: Messung eines Referenzpunkts (außerhalb R-003). |
| Lesen von `Alignments3D` im Erfassungsmodus unbestätigt | **[offen]**, Test am Messrechner (Erkundung P1-6-abgleich). Bis dahin als „unverifiziert“ kennzeichnen. |
| Koordinatensystem: Achsrichtungen des 3D-Abgleichs | KONVENTIONEN: Vorzeichen X/Y/Z „vorläufig, am Gerät zu bestätigen“; Messpunkt M13 aus dem Ablaufplan ist die Prüfung. Das Protokoll sollte das Koordinatensystem nicht umdeuten, nur Werte tragen. |
| Mehrdeutiger Index (0/1-basiert) bei `Alignments3D.Item` | Umrechnung nur im Adapter (KONVENTIONEN); Index am Gerät klären (I5 P2-12). |
| Unbeaufsichtigter Betrieb mit Laser | Nur Stufe 3 betroffen; ohne Betreuervorgabe nicht umsetzen (Frage A4). |

### 1.7 Machbarkeit und Aufwand R-003 (Stufen)

| Stufe | Inhalt | Machbarkeit | Aufwand [Annahme] |
|---|---|---|---|
| 1 | Abgleichstatus und Qualität je Messung lesen und ins Messprotokoll schreiben; Simulator; Tests | machbar, am Gerät zu bestätigen | mittel |
| 2 | Wie 1, plus Bewertung gegen Qualitätsgrenze und Gate vor dem Scan (Vorprüfung) | machbar, Grenzwert vom Betreuer | mittel bis klein auf Stufe 1 |
| 3 | Abgleich per COM neu berechnen (2D-/3D-Abgleichscan auslösen oder nachbauen) | **nicht belegt**, hoher Aufwand, Laserbewegung | groß, nicht empfohlen |

---

## 2 R-025: Benachrichtigung

### 2.1 Wo die Ereignisse schon entstehen (Andockpunkt)

Kette: `Steuerung._melde(art, text, **daten)` ruft `bei_ereignis`
(`ablauf/steuerung.py`, `_melde`) → `Sitzung._bei_ablauf` → `Sitzung._neues_ereignis` legt ein
`SitzungsEreignis` (Felder `revision`, `art`, `text`, `daten`, `bild`) in eine Queue → die
Oberfläche holt sie mit `Sitzung.hole_ereignisse()` (`gui/hauptfenster.py::aktualisiere`).
[belegt: Code]

Zuordnung der vier Fälle aus R-025 (aus dem Code abgelesen):

| R-025-Fall | Ereignis (`art`, `daten`) | Fundstelle |
|---|---|---|
| Messung fertig | `eintrag_zustand`, `nach == "fertig"` (auch beim Trockenlauf) | `_schliesse_messung` → `_eintrag_zustand` |
| Durchgang fertig | `durchgang_beendet`, `ergebnis == "vollstaendig"` | `_beende_durchgang` |
| Messung Fehler | `fehler` (`eintrag_id`, `art_fehler`, `reaktion`) und danach `eintrag_zustand` `nach == "fehler"` | `_messung_fehler` |
| Fehler wartet auf Nutzerentscheidung (der wichtigste Fall im unbeaufsichtigten Betrieb) | `durchgang_zustand`, `nach == "wartet_auf_entscheidung"` | `_messung_fehler`, Strategie `PausierenUndNachfragen` (vorläufig, O1) |
| Abbruch | `eintrag_zustand` `nach == "abgebrochen"`; `durchgang_beendet`, `ergebnis == "abgebrochen"` | `_schliesse_messung`, `_abbrechen` |
| Gerät unklar / PSV hängt | `fehler` mit `art_fehler == "geraet_unklar"`; `durchgang_beendet` `ergebnis == "geraet_unklar"`; Sitzungsereignis `waechter` (PSV reagiert nicht seit n s), `waechter_fehler` | `_geraet_unklar`, `Sitzung.pruefe_waechter` |
| Pausenpunkt erreicht | `eintrag_zustand`, `nach == "erreicht"` (Text „Pausenpunkt erreicht: …“) und `durchgang_zustand` `nach == "wartet_auf_bestaetigung"` | `_starte_naechsten` |

Folgerungen für den Andockpunkt:
- Ein Fehler erscheint **mehrfach** (`fehler`, `eintrag_zustand`, ggf. `durchgang_zustand`,
  `durchgang_beendet`). Eine Abbildungstabelle Ereignis → Benachrichtigung muss entdoppeln
  (z. B. nur `eintrag_zustand` für Messungen, `durchgang_zustand`/`durchgang_beendet` für den
  Durchgang), sonst kommen mehrere Nachrichten je Vorfall.
- `SitzungsEreignis` trägt **keinen Zeitstempel und keinen Messungsnamen** (nur `eintrag_id`).
  Die Akzeptanz von R-025 („Messungsname, Ereignis, Uhrzeit“) braucht: Namen über
  `Warteschlange.hole(eintrag_id)` nachschlagen, Uhrzeit über die injizierbare `Uhr.jetzt()`.
- **`hole_ereignisse()` ist ein zerstörendes Abholen** (Queue, `get_nowait`) und gehört der
  Oberfläche. Ein zweiter Verbraucher würde der Oberfläche Ereignisse stehlen. Der Benachrichtiger
  darf **nicht** darüber lesen.
- Empfohlener Andockpunkt: ein zusätzlicher, nicht blockierender **Beobachter** in
  `Sitzung._bei_ablauf` (nach `_neues_ereignis`) oder ein kleiner Verteiler als
  `bei_ereignis` der Steuerung. Der Aufruf kommt im Thread, der `Steuerung.schritt` ausführt
  (Geräte-Thread), siehe Docstring von `Steuerung`. Dort darf **kein Netzwerkaufruf** stattfinden
  (Zeitlimits, Wächter, `aufruf_grenze_s`); der Beobachter legt nur eine Nachricht in eine eigene
  Queue, ein Sendethread arbeitet sie ab (Muster des Wächter-Threads in `sitzung.py`,
  `starte_threads`/`beende_threads`).
- Testbar ohne Dienst: Die Steuerung ist schon über `Testuhr`, Simulator und `Steuerung.bis_ruhe`
  deterministisch fahrbar (`tests/ablauf`, `tests/sitzung`). Der Beobachter lässt sich synchron
  mit einem Fake-Kanal prüfen.

Wo nicht andocken: im Messprotokoll (wird je Messung geschrieben, deckt Durchgang und Pausenpunkt
nicht ab) und in der GUI (Benachrichtigung muss auch ohne geöffnete Oberfläche funktionieren,
falls später ein Betrieb ohne GUI gewünscht ist [Annahme]).

### 2.2 Kanal Webex (technische Wege)

**[Wissen]** (nicht im Repo belegt, vor Umsetzung gegen developer.webex.com prüfen):

| Weg | Funktionsweise | Was das Institut liefern muss | Vorteile | Nachteile |
|---|---|---|---|---|
| **A: Bot** | Bot im Webex-Developer-Portal anlegen; Bot-Token (langlebig); `POST https://webexapis.com/v1/messages` mit `Authorization: Bearer <Token>`, Ziel `roomId` oder `toPersonEmail`, Text oder Markdown | Webex-Konto/Organisation, die Bots zulässt (Control-Hub-Richtlinie); jemand, der den Bot anlegt; Empfänger muss den Bot in einem Space haben bzw. Direktnachrichten erlaubt bekommen; ausgehender HTTPS-Zugang des Messrechners zu `webexapis.com` | Eigene Identität, gezielt an Person oder Space, Nachweis im Space, gut dokumentierte REST-API | Token ist ein dauerhaftes Geheimnis; Anlage und Freigabe kann Admin brauchen; Organisation kann Bots sperren |
| **B: Incoming Webhook** (Webex-App-Hub-Integration) | Pro Space eine URL; `POST` mit JSON `{"text": …}` an die URL | Admin muss die Integration „Incoming Webhooks“ zulassen; jemand legt sie im Ziel-Space an; ausgehender HTTPS-Zugang | Einfachster Aufbau, kein Token-Austausch, nur eine URL | Die URL ist das Geheimnis (wer sie hat, kann posten); nur Space, keine Direktnachricht; weniger Kontrolle; Verfügbarkeit im Institutstenant [offen] |
| **C: Persönliches Zugriffstoken** | Token des eigenen Kontos | – | – | **Nicht geeignet:** läuft nach kurzer Zeit ab und ist an die Person gebunden |
| **D: Integration (OAuth)** | Nutzerbezogene Tokens mit Refresh | Registrierung der Integration, Redirect, Freigabe | Handeln im Namen des Nutzers | Zu aufwendig für eine Benachrichtigung; Token-Erneuerung nötig |

Empfehlung (nicht endgültig): **A oder B**, je nachdem, was das Institut erlaubt. B ist
einfacher, A flexibler. Beide brauchen vor der Umsetzung eine Zusage zu Konto und Netzfreigabe
(Frage W1 bis W5).

Zustellung: HTTP-Fehler (Netz, 401, 429 Rate-Limit, 5xx) dürfen die Messung nie beeinflussen;
begrenzte Wiederholung mit Wartezeit (bei 429 den Header `Retry-After` beachten [Wissen]),
danach Eintrag im Ereignisprotokoll („Benachrichtigung fehlgeschlagen“) und weiterarbeiten.

### 2.3 Kanal E-Mail (technische Wege)

| Weg | Funktionsweise | Was das Institut liefern muss | Vorteile | Nachteile |
|---|---|---|---|---|
| **A: SMTP mit Anmeldung** | `smtplib.SMTP` mit STARTTLS (üblich Port 587) oder `SMTP_SSL` (465); Benutzer/Passwort | Servername, Port, Verschlüsselung, Konto (ggf. funktionsbezogenes Postfach) und Passwort/App-Passwort, Absender- und Empfängeradresse; Netzfreigabe zum Port | Standardbibliothek, keine Abhängigkeit, weit verbreitet | Zugangsdaten sind ein Geheimnis; viele Anbieter schalten einfache Passwortanmeldung ab (Modern Authentication) [Wissen], Institutsvorgabe [offen] |
| **B: SMTP-Relay ohne Anmeldung** (Freigabe nach IP) | wie A ohne `login` | Server, der Mails vom Messrechner (IP) annimmt | Kein Geheimnis im Code | Muss vom IT-Betrieb freigeschaltet werden; Zustellungsregeln unbekannt [offen] |
| **C: Outlook auf dem Messrechner (COM)** | `win32com` mit `Outlook.Application`, Mail über das angemeldete Profil | Outlook installiert und angemeldet auf dem Messrechner [offen] | Keine Server- und Zugangsdaten in der Software; pywin32 ist ohnehin installiert | Abhängig von der Sitzung des Nutzers auf dem Messrechner (gemeinsamer Rechner, A9), mögliche Sicherheitsabfragen von Outlook, Messrechner wird noch stärker an einen Nutzer gebunden |
| **D: Graph-/Exchange-API (OAuth)** | HTTPS-REST mit App-Registrierung | App-Registrierung im Mandanten, Admin-Zustimmung | Moderne Authentifizierung | Aufwand und Verwaltung zu hoch für diesen Zweck |

Hinweis: Eine Mail auf eine Handyadresse oder ein E-Mail-zu-Webex-Weg erfüllt „sofort sichtbar“
nur, wenn der Nutzer sie so liest; das ist Betreuer-/Nutzersache.

### 2.4 Sicherheit (Geheimnisse, Datenschutz, Messrechner)

- Der Messrechner ist ein **gemeinsamer Rechner** (Messdaten mehrerer Projekte, Faktenliste A9).
  Ein Token oder SMTP-Passwort im Klartext in einer Datei ist dort für andere Nutzer lesbar
  (Dateirechte prüfen, am Gerät [offen]).
- **Nie ins Repo, nie ins Protokoll:** Heute schreibt `konfig.py::protokoll_info` Pfad, SHA-256
  und **alle Werte** der Konfigurationsdatei in **jedes Messprotokoll** und in das Ereignis
  `durchgang_start`. Ein Token in der Konfigurationsdatei würde damit in alle Protokolle
  gelangen. Die Konfigurationsdatei hat zudem ein **strenges Schema** (unbekannte Schlüssel
  führen zu `KonfigFehler`). Deshalb: In der Konfigurationsdatei höchstens **Kanalart und
  Zieladresse ohne Geheimnis**; das Geheimnis selbst kommt aus einer Quelle außerhalb von
  Repo, Konfiguration und Protokoll.
- Quellen für Geheimnisse (Entwurfsentscheidung E7, siehe Abschnitt 3): Umgebungsvariable
  (einfach, im Prozess sichtbar, in der Sitzung des Nutzers); Datei außerhalb von
  `D:\Messdaten` und Repo mit eingeschränkten Rechten; Windows-Anmeldeinformationsverwaltung
  (bräuchte eine neue Abhängigkeit wie `keyring`, die ins Wheelhouse und in `uv.lock` müsste).
  Das Repo hat Secret-Scanning nicht vorgesehen [Annahme]; eine Prüfung auf Token-Muster im
  Test wäre eine billige Absicherung.
- Fehlertexte, Ereignisprotokoll und Exceptions dürfen das Token nicht enthalten (Header nicht
  protokollieren, URL des Incoming Webhooks maskieren).
- **Datenminimierung:** Webex und Mail sind externe Dienste. Nachrichteninhalt auf
  Messungsname, Ereignis, Uhrzeit begrenzen (R-025-Akzeptanz). Keine Pfade, keine Messwerte, keine
  Seriennummern. Der Messungsname kann ein Projekt verraten; ob das zulässig ist, ist **[offen]**
  (Betreuerfrage W4).
- Ausgehende Verbindung vom Messrechner: **Internet ist laut Faktenliste A9 vorhanden**, Proxy,
  Firewall und die offene Frage F30 (TODO) zum Internetzugang des Messrechners sind aber nicht
  geklärt.
- Wheelhouse-Zwang: Die Laufzeitpakete sind in `uv.lock` festgelegt, ein Test erzwingt, dass die
  Wheelhouse-`PINS` damit übereinstimmen (KONVENTIONEN). Jede neue Bibliothek (z. B. `requests`)
  erzeugt Zusatzarbeit; Standardbibliothek (`urllib.request`, `smtplib`, `email.message`) nicht.

### 2.5 Testbarkeit ohne echten Dienst

| Ebene | Vorgehen | Aussagekraft |
|---|---|---|
| Logik (Auswahl der Ereignisse, Entdoppeln, Texte, Reihenfolge, nie Messung stören) | Fake-Kanal im Speicher (Protocol `Benachrichtiger` mit `sende(nachricht)`), Simulator und `Testuhr` | Hoch, vollständig in der Standard-Prüfung |
| Webex-Format (URL, Header, JSON, Fehlerbehandlung 401/429/5xx) | lokaler `http.server` im Test oder injizierter `urlopen`-Ersatz; Token nur als Dummy | Mittel: prüft unser Format, nicht Webex-Verhalten |
| SMTP | injizierte `smtplib.SMTP`-Fabrik mit Fake; ein echter lokaler SMTP-Testserver bräuchte eine Dev-Abhängigkeit (`aiosmtpd`) oder das in Python 3.11 noch vorhandene, veraltete `smtpd` (entfällt ab Python 3.12) | Mittel |
| Ende-zu-Ende (echte Nachricht kommt an) | Nur am Messrechner mit echtem Konto; nach `/laborbuch` festhalten. **Nie als bestanden melden, bevor der Nutzer bestätigt hat** (Ablauf G). | Einziger Nachweis für R-025 |
| Nicht in der Standard-Prüfung | Tests, die Netz brauchen, per `pytest`-Marker kennzeichnen (KONVENTIONEN „Hardware“ analog) | – |

### 2.6 Risiken R-025

| Risiko | Einschätzung |
|---|---|
| Nachrichtenflut: „Messung fertig“ je Messung bei 50 bis 200 Messungen je Durchgang | Wortlaut von R-025 lässt das offen; Frage W6 an den Betreuer (je Messung oder nur Durchgang; Zusammenfassung; Mindestabstand). |
| Zustellfehler/Hänger blockiert Steuerung | Nur über entkoppelten Sendethread vermeidbar (Abschnitt 2.1). Verlust von Nachrichten bei Programmende: Warteschlange beim Beenden leeren, mit Zeitlimit. |
| Der „Fehler wartet auf Entscheidung“ wird nicht gemeldet, weil nur `fehler` abgebildet wird | Ohne ihn bleibt ein unbeaufsichtigter Durchgang unbemerkt stehen; in die Abbildung aufnehmen. |
| Nachricht gibt Interna preis | Datenminimierung (Abschnitt 2.4). |
| Webex-Ausfall, Netzausfall | Fehler im Ereignisprotokoll; Messungen laufen weiter; Rückfallkanal (Mail) nur auf Wunsch (Frage W7). |
| Verfälschte Uhrzeit | Zeitzone: `Uhr.jetzt()` ist zeitzonenbehaftet; in der Nachricht Lokalzeit mit Zone ausweisen. |
| Rechtlich/institutionell: Nutzung eines Cloud-Dienstes für Laborstatus | Institutsfrage (W3). |

### 2.7 Machbarkeit und Aufwand R-025

Machbar. Kern (Protocol `Benachrichtiger`, Fake, Ereigniszuordnung, Sendethread, Konfiguration
ohne Geheimnis) ist mittlerer Aufwand [Annahme]. Ein Kanal (Webex *oder* SMTP) kommt als klein
bis mittel hinzu, ein zweiter jeweils klein. Ohne Betreuerangaben zu Konto und Netz bleibt der
Kanal nur gegen Fakes prüfbar; das Lastenheft-Kriterium („Nachricht geht über den eingestellten
Kanal heraus“) ist dann nicht am Gerät nachweisbar.

---

## 3 Entwurfsentscheidungen mit Alternativen (für spätere ADR, noch nicht entschieden)

| Nr. | Entscheidung | Alternativen | Empfehlung (vorläufig) |
|---|---|---|---|
| E1 | Umfang R-003 | (a) nur lesen und protokollieren; (b) zusätzlich Gate gegen Qualitätsgrenze; (c) Abgleich per COM neu berechnen/auslösen | (b), (c) nur nach Betreuerentscheid und Gerätetest |
| E2 | Schnittstelle für den Abgleichstand | (a) eigenes Protocol `Abgleichsleser` neben `Messgeraet`; (b) Methode in `Messgeraet`; (c) Teil von `EinstellungsStand` | (a), da `Messgeraet` runtime-checkable ist und alle Fakes sonst brechen |
| E3 | Ablage des Ergebnisses | (a) Feld `abgleich` im Messprotokoll je Messung; (b) im Durchgangs-Ereignisprotokoll; (c) eigener Warteschlangeneintrag „Abgleich“ | (a); (b) ergänzend einmal je Durchgang denkbar |
| E4 | Verhalten bei ungültigem oder schlechtem Abgleich | (a) Warnung im Protokoll; (b) Vorprüfung verweigert die Messung; (c) einstellbar | (c) mit Voreinstellung (b) im Modus MESSEN, Betreuerentscheid A5 |
| E5 | Andockpunkt Benachrichtigung | (a) Beobachter in `Sitzung._bei_ablauf`; (b) Verteiler als `Steuerung(bei_ereignis=…)`; (c) Lesen von `hole_ereignisse` (**verworfen**, stiehlt der GUI die Ereignisse) | (a) oder (b), mit eigenem Sendethread |
| E6 | Kanalabstraktion | (a) ein Protocol `Benachrichtiger`, Implementierungen Webex, SMTP, Fake, ggf. Datei/Konsole; (b) fester Kanal im Code | (a) |
| E7 | Aufbewahrung des Geheimnisses | (a) Umgebungsvariable; (b) Datei außerhalb von Repo und Messdaten mit Rechten; (c) Windows-Anmeldeinformationsverwaltung (+ Abhängigkeit) | (a) oder (b), je nach Messrechner-Praxis; **nie** in `konfig`-Datei, da deren Werte in alle Protokolle gehen |
| E8 | HTTP-Bibliothek | (a) Standardbibliothek `urllib.request`/`http.client`; (b) `requests`/`httpx` (Abhängigkeit, `uv.lock`, Wheelhouse); (c) ein Webex-SDK (Pflege und Aktualität zu prüfen [offen]) | (a), weil nur ein einfacher POST nötig ist |
| E9 | Menge der Nachrichten | (a) je Ereignis wörtlich nach R-025; (b) Messung fertig nur zusammengefasst je Durchgang; (c) einstellbar | (c), Voreinstellung nach Betreuerantwort W6 |
| E10 | Verhalten bei Zustellfehler | (a) still ins Ereignisprotokoll, Messung läuft weiter; (b) Durchgang anhalten; (c) Rückfallkanal | (a) mit begrenzter Wiederholung, (c) optional |

Mehrere dieser Entscheidungen berühren ADR-007 (Whitelist), ADR-008 (Nebenläufigkeit) und
ADR-014 (Konfigurationsdatei); sie sollten dort nachgetragen oder neu verfasst werden, wenn
sie angenommen werden.

---

## 4 Fragenliste an den Betreuer (ersetzt und präzisiert O9 und O10)

### Zu R-003 (ersetzt O9)

**A1. Was soll „Abgleich ausführen“ heißen?** Drei Stufen zur Auswahl:
(1) Die Software liest nur Status und Qualität des in PSV vorhandenen Abgleichs und protokolliert
sie; (2) zusätzlich lädt sie einen gespeicherten Abgleich aus der Einstellungsdatei und prüft ihn
gegen eine Qualitätsgrenze; (3) die Software löst den Abgleichscan selbst aus.
*Auswirkung:* Stufe 3 ist nach heutigem Kenntnisstand per COM nicht auslösbar (kein COM-Gegenstück
zum 2D-/3D-Abgleichscan in der Dokumentation); es bliebe Bedienung in PSV. *Vorschlag/Annahme bis
zur Antwort:* Stufe 1 und 2.

**A2. Welche Abgleichmethode wird am Versuchsaufbau verwendet?** Automatischer 3D-Abgleich mit
Abgleichobjekt PSV-A-655, klassisch mit Geo-Laser, oder Referenzobjekt PSV-A-450? Ist eine
Koaxialeinheit montiert? Wer führt den Abgleich aus, wie oft, und wird er vor jeder Messreihe
neu gemacht oder aus der Einstellungsdatei geladen?
*Auswirkung:* bestimmt, welche Werte sinnvoll sind (Winkel- und Positionsunsicherheit bei
automatischem Abgleich) und ob die Software überhaupt einen Abgleich neu berechnen müsste.

**A3. Welche Ergebniswerte sollen ins Messprotokoll, und gibt es Grenzwerte?**
Vorschlag: Gültigkeit je Scankopf (2D, 3D, Kamera), Ist- und Soll-Qualität in m,
Positionsunsicherheit in m, Winkelunsicherheit in rad (Polytec nennt als Faustregel 0,1 mrad
entsprechen 0,1 mm auf 1 m), Koordinatendefinitionsmodus, Kopfpositionen, Punktanzahl,
2D-Scankopfabstand, Zeitpunkt. Welche zusätzlichen Werte (z. B. Konditionszahl, die die
PSV-Schnittstelle nicht liefert) und welche **Akzeptanzgrenzen** (z. B. Winkelfehler höchstens
x mrad) gelten?
*Auswirkung:* Akzeptanzkriterium von R-003 und Prüfung „Abgleich gut genug“.

**A4. Darf die Software Laser und Spiegel ohne Aufsicht bewegen?** Welche Laserschutzregeln
gelten im Labor (Laserschutzbeauftragter, Absperrung, Anwesenheitspflicht), und ist ein
unbeaufsichtigter Start eines Abgleichs oder Scans mit bewegtem Strahl zulässig?
*Auswirkung:* Nur relevant für Stufe 3 und für jede neue schreibende COM-Operation; ohne
Freigabe wird nichts bewegt (Stand der Software heute: alle Laser- und Fokusaufrufe sind nicht
freigegeben).

**A5. Was passiert bei ungültigem oder schlechtem Abgleich?** Messung verweigern, nur warnen oder
einstellbar? Soll der Abgleich vor jedem Durchgang, vor jeder Messung oder nach jedem Pausenpunkt
(Umbau) geprüft werden?
*Auswirkung:* Ablauf der Steuerung, Fehlerart „Vorprüfung“, Verhalten im unbeaufsichtigten Betrieb
(hängt mit O1 zusammen).

**A6. Reicht es, den Abgleich je Messung als Momentaufnahme zu protokollieren, oder soll er
zusätzlich je Durchgang einmal mit Vergleich zum Vorwert stehen?** (Ändert, ob ein Wechsel des
Abgleichs zwischen zwei Messungen gemeldet wird.)

### Zu R-025 (ersetzt O10)

**W1. Welcher Kanal ist bindend, welcher Rückfall?** Webex, E-Mail oder beides? (Lastenheft:
bevorzugt Webex.)

**W2. Webex: Darf in der Organisation ein Bot angelegt oder ein Incoming Webhook eingerichtet
werden? Wer legt ihn an (Konto/Organisation), an wen soll gesendet werden (Einzelperson per
Direktnachricht oder Space), und wer verwaltet das Zugriffsgeheimnis (Token bzw. Webhook-URL)?**
*Auswirkung:* ohne Zusage nicht am Gerät nachweisbar; entscheidet Weg A oder B.

**W3. E-Mail: Welcher SMTP-Server, Port, Verschlüsselung und Anmeldeverfahren (Passwort,
Modern Authentication, Relay nach IP-Freigabe)? Welche Absender- und welche Empfängeradresse?
Oder soll das auf dem Messrechner angemeldete Outlook verwendet werden?**

**W4. Datenschutz und Vorgaben:** Dürfen Messungsname, Ereignis und Uhrzeit über einen externen
Cloud-Dienst gehen? Ab welcher Information (Projektname, Prüflingsname) nicht?

**W5. Netz:** Darf der Messrechner ausgehend per HTTPS zu `webexapis.com` bzw. zum SMTP-Server
(Proxy, Firewall)? (Hängt mit der offenen Frage F30 zum Internetzugang des Messrechners zusammen.)

**W6. Menge:** Soll „Messung fertig“ für jede einzelne Messung eine Nachricht auslösen oder
zusammengefasst werden (nur Durchgang fertig, oder alle n Messungen, oder Mindestabstand)?
Gehören „Fehler wartet auf Entscheidung“ und „PSV reagiert nicht mehr“ ausdrücklich zu den
Fehlerfällen?

**W7. Zustellfehler:** Wie wichtig ist die Zustellung? Soll bei Webex-Ausfall automatisch auf
E-Mail ausgewichen werden, oder genügt ein Vermerk im Ereignisprotokoll? (Annahme: Messung läuft
immer weiter, Zustellfehler halten nie an.)

**W8. Wer erhält die Nachrichten, und braucht es eine Quittierung** (Nutzer bestätigt am
Messrechner, siehe Pausenpunkt)?

---

## 5 Vorschlag für neue Lastenheft-Fassung (zur Entscheidung durch den Nutzer, keine Änderung vorgenommen)

- R-003 aufteilen: **R-003a** (Muss): Die Software liest Status und Qualität des 2D-, 3D- und
  Kameraabgleichs über COM und schreibt sie je Messung ins Messprotokoll. **R-003b**
  (Soll bzw. nach A1/A5): Prüfung gegen Qualitätsgrenze. **R-003c** (offen, nach A1): Auslösen
  des Abgleichs; mit Hinweis, dass dafür in der Dokumentation kein COM-Aufruf belegt ist.
- R-025 um den Fall „Fehler wartet auf Entscheidung“ und „PSV reagiert nicht“ ergänzen
  (nach W6), und die Akzeptanz um „Zustellfehler halten die Messung nicht an“ erweitern.
- Nach der Erkundung am Messrechner: Lesen der `Alignments3D`/`Alignments2D` (Index, Anzahl,
  Werte) als Prüfpunkt eintragen, bis dahin Status „unverifiziert“.

---

## 6 Was nicht untersucht wurde

- Die Handbuchtexte zu 2D-/3D-Abgleich liegen als PDF vor; ich habe Abschnitt 5 per Textextraktion
  gelesen, aber keine Abbildungen (Bildschirmdialoge) ausgewertet. Das Lehrvideo
  `3DAlignmentScanManual.mp4` (Faktenliste A8) ist nicht ausgewertet.
- Die PDF „06 Automatisierung via COM“ enthält keinen Treffer zu Abgleich (Textsuche).
- Kein Gerätezugriff: Alle Aussagen zum Verhalten am Messrechner sind **[offen]**.
- Webex- und SMTP-Aussagen (Abschnitt 2.2 bis 2.3) sind allgemeines Wissen, nicht aus dem Repo
  und nicht aus einer Recherche im Paket belegt.
- Ob Polytec in der installierten Version (PSV 10.4.0.1, Erkundung 161125) einen COM-Aufruf für
  den Abgleichscan über die dokumentierten Typen hinaus anbietet, habe ich nicht gegen die
  tatsächlichen Typbibliotheken geprüft. `typelibs.txt` der Erkundung führt die PolyAlignment-
  Bibliothek nur als Registrierung (GUID, DLL-Pfad), nicht mit Mitgliedern; ein Auslesen der
  Mitglieder am Messrechner (z. B. per `pythoncom`/`makepy`) wäre der Nachweis.
