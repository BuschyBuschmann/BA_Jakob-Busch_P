<!-- Fachanalyse I5-F (strukturdynamik-experte, sonnet): fachliche Stichprobe der COM-Referenz I5; unverändert übernommen. -->

# Fachanalyse I5-F: fachliche Stichprobe der COM-Referenz I5

Es wurden keine Repository-Dateien geändert. Hilfsdateien liegen im Scratchpad `/tmp/claude-0/-home-user/e6b61297-17fb-5003-91f8-95c4534d012c/scratchpad/i5f/`. Dazu gehören das Prüfskript `chk.py` und die Textextrakte der Handbücher.

**Geprüft.** Gelesen habe ich Abschnitt 1, 2, 3.1–3.2, 4, 6 und 9 der Referenz sowie KONVENTIONEN.md (Polytec-Konventionen) und I2 (Abschnitt 1–6). Gegengeprüft habe ich gegen die CHM-Textfassung (BEM, `Access_to_Data`, DataPoint, XAxis, PTC-Enums, FftAcqProperties, Waveforms, Channel-/Trigger-/Average-/General-Properties, Alignment3D) und gegen die PDFs. Bei den PDFs waren das SWA (Software Handbuch PSV) 7-5/6, 7-11/12, 7-16/17, 7-32 und 8-5, SWP Tab. 3.2, TM Kap. 6 und Tab. 6.1 sowie die Matlab-Folien 8 und 9. Die Gleichungen 7.1–7.4 habe ich als Bild der PDF-Seite 225 gelesen.

## 1. Gesamturteil

- **Keine BLOCKER.** Die geprüften Aussagen sind im Kern korrekt belegt.
  - Verschränkung von Real/Imag bzw. Betrag/Phase: gerade Indizes sind Real bzw. Betrag.
  - 3D-Layout x, dann y, dann z. Für komplexe Daten gilt `reshape(3, n, 2)`. Das ist belegt (BEM, Access to Data, Abschnitt „User-Defined Data“: RX0, IX0, …) und per Skript bestätigt.
  - Display-Enums: MagPhase = 2 (Grad), MagPhaseRad = 14, RealImag = 9.
  - Function-, Domain- und Build-Flag-Werte.
  - Frame-Semantik, Float32-Rückgabe, Punktmittel als Betragsmittel.
  - Phase intern in rad, 0-basierte Indizes, Umwandlung nach float64/complex128: konsistent zu KONVENTIONEN.
- **4 MAJOR-Befunde.** Sie betreffen Von/Bis, die fehlende Skalierungs- und Phasenbezugsbeschreibung, Lücken in der Metadatenliste und die Machbarkeitsaussage U6.
- **Zu I2:** Es gibt keinen Widerspruch zu I2. Die Referenz lässt aber die Skalierungs- und Phasenkonventionen aus I2 §1.2 und §3.8 weg.

## 2. Befunde (A1)

Zeilenangaben beziehen sich auf `2026-10-23_I5_com-referenz.md`.

### MAJOR

**M1. Frequenzachse bei eingeschränktem Bereich Von/Bis (Z. 743, 353, 763–774; betrifft KONVENTIONEN, Polytec-Konventionen)**
- *Soll:* SWA 7-16/7-17: „Von, Bis: Sie können den Frequenzbereich einschränken, der angezeigt und ausgewertet wird.“ Außerdem „Verwendet: Die angezeigte Anzahl von FFT-Linien entspricht dem Frequenzbereich zwischen Von und Bis.“ Gl. 7.4: Δf = 1/t_Mess = BW/n_FFT. Ich habe Gl. 7.1–7.4 als Bild gelesen: f_Abtast = 2,5·BW (Nicht-M-Systeme), 2,56·BW (M-Systeme), t_Mess = n_FFT/BW.
- *Ist:* Z. 743 sagt „ab Linie 1 (Index 0) bis Linie Lines (Index Lines−1)“, nach BEM. `Lines` ist dort die Gesamtzahl (Z. 353). Die Referenz verknüpft das nirgends mit Von/Bis. Auch die KONVENTIONEN-Formel k = 1…n_FFT setzt Von = 0 und Bis = BW voraus.
- *Auswirkung:* Bei Von/Bis ungleich Vollbereich kann die gespeicherte Datenlänge kleiner als `Lines` sein. Dann wäre `f = Δf·arange(1, n+1)` falsch (Frequenzversatz). Ob die Datei nur den Teilbereich enthält, ist aus der Doku nicht belegbar [U]. Ein Rechenbeispiel: BW = 5000 Hz, 400 Linien, Bereich 1000–4000 Hz ergibt 241 Linien von 1000 bis 4000 Hz.
- *Korrektur:*
  1. Die Achse immer aus `XAxis` bilden (Min, Max, `MaxCount`, `GetMidX`).
  2. Prüfen, dass `MaxCount` mal Δf plausibel zum Bereich passt.
  3. Δf aus `SampleResolution` bzw. BW/`Lines` bestimmen und den Linienindex k = f/Δf mitführen.
  4. Die KONVENTIONEN-Formel auf „k = k_min…k_max, Vollbereich: 1…n_FFT“ erweitern.
  5. Von/Bis (`StartFrequency`, `EndFrequency`) in die Metadaten aufnehmen.
- *Zusatz (Z. 766–770):* Der Beleg Matlab-Folie 8/9 (XMin 12,5, XMax 5000, XCount 400) ist konsistent. Ich habe es bestätigt: Δf = 12,5 Hz, f₁ = 12,5 Hz, f₄₀₀ = 5000 Hz, konstanter Abstand 12,5 Hz. Die BW ist auf der Folie aber nicht sichtbar, es gilt also nur „konsistent mit“, nicht „bewiesen“. Das bleibt zu Recht „vorläufig“.

**M2. Skalierung, Phasenbezug und Bedeutung der komplexen Daten fehlen in 4.4 (Z. 738–786)**
- *Soll (I2 §1.2/§3.3/§3.8, TM 3-3 und Tab. 6.1, Matlab-Folie 9):*
  - Die Spektren sind einseitig und auf die Spitzenamplitude (0-to-peak) skaliert, und zwar amplitudentreu (Fensterkorrektur). Die Matlab-Folie 9 zeigt „Amplitude in m/s“.
  - Real/Imag entsprechen A·e^{iφ₀} bei der Zeitabhängigkeit e^{+iωt}, also A·cos(ωt+φ₀).
  - AP hat die Einheit (Einheit)², PSD zusätzlich pro Hz, FRF den Quotienten der Einheiten.
  - Phase ist nur mit Referenz oder Trigger definiert (TM Tab. 6.1). Mit Referenz gilt die Phase relativ zur Referenz, mit Trigger ohne Referenz relativ zum Fensteranfang. Bei Betragsmittelung wird die Phase nachträglich aus dem Kreuzspektrum zugewiesen. `PhaseFromRef` steht in Z. 437 nur als Name.
- *Ist:* Die Tabelle in 4.4 nennt nur Datentyp, Layout und Einheit „aus YAxis lesen“. Eine falsch angenommene Skalierung (RMS statt Peak) oder ein fehlender Phasenbezug würde die ODS-Auswertung und alle Sollwert-Tests verfälschen.
- *Korrektur:* Einen Absatz „Skalierung und Phasenbezug“ ergänzen mit den oben genannten Punkten. Als Pflichtmetadaten je Messung ablegen: Mittelungstyp, Trigger, Referenzkanäle, `PhaseFromRef`, Fenster. Ohne Referenz und ohne Trigger darf der Adapter keine Phase als gültig kennzeichnen.

**M3. Aussage „Der COM-Weg reicht für eine vollständige Dokumentation“ ist zu stark (Z. 975, U3 in Z. 1137)**
- *Soll:* I2 §2.3 nennt weitere reproduzierbarkeitskritische Größen. Details stehen in Abschnitt 3 (A2).
- *Ist:* Z. 971–973 nennt nur Lizenzen, Seriennummer und Zeitzone als Lücken. Es fehlen die nicht per COM verfügbaren Versuchsgrößen (Generatorlast, Lagerung, Anregungsort, Oberflächenpräparation, Umgebung, Warmlaufbeginn, Kraftsensor-Empfindlichkeit). Außerdem fehlen mehrere per COM verfügbare, aber nicht gelistete Größen (SE-Modus, Trigger, Von/Bis, Alignment-Details, Referenzkanal- und Richtungszuordnung).
- *Korrektur:* Die Tabelle um die A2-Liste ergänzen. Den Satz ersetzen durch „COM/PolyFile liefert die Gerätekonfiguration; die Versuchsrandbedingungen sind manuell per Protokoll zu erfassen“.

**M4. U6 zu optimistisch bzw. unscharf (Z. 1140)**
- *Soll:* Absolute FRF (Mobilität in (m/s)/N) setzt eine Kraftmessung voraus (SWA 7-12: Kanal-Größe „Kraft“ und Kalibrierfaktor; vgl. I2 §3.4). Ohne Kraftreferenz ist die FRF V/R in (m/s)/V und enthält die Dynamik von Verstärker und Shaker. Phase und ODS brauchen Referenz oder Trigger (TM Tab. 6.1). Die Frequenzachse von H1/H2 stammt aus dem FFT-Modus.
- *Ist:* U6 listet „komplexe FRF (H1/H2), Kohärenz, 3D-Komponenten“ als verfügbar, ohne diese Bedingungen. „Zeitdaten nur mit Option TDD bzw. `SaveTimeDataForScan`“ suggeriert Alternativen. Die Quellen belegen aber nur: Der Modus Zeit braucht TDD (SWA 7-2, 7-34). `SaveTimeDataForScan` setzt SE automatisch auf „Fast“ (BEM, GeneralAcqProperties). Ob `SaveTimeDataForScan` ebenfalls lizenzpflichtig ist, ist [offen]. „Multi-Referenz-Modalanalyse nur mit PCA“ gilt nur für die Polytec-interne MIMO-Rechnung, nicht für eine externe Auswertung mehrerer Messungen.
- *Korrektur:* Die Machbarkeitstabelle aus Abschnitt 4 (A3) übernehmen.

### MINOR

**m1. Frames (Z. 748–751).** Nach BEM (DataPoint.GetData) gilt Frame 0 = „average frame“ nur im MultiFrame-Modus. Principal Inputs und Virtual Coherences (PCA) haben Frames 1…Anzahl der Referenzkanäle. Benutzersignale haben die Frames 1…12. `GetDataSection(Average)` liefert die Einzelblöcke nur für Zeitsignal-Displays von FFT-Messungen, also nur mit gespeicherten Zeitdaten. „Mittelwert-Frame“ ist kein Hinweis auf die FFT-Mittelung. Präzisieren.

**m2. 3D-Komponenten und Vorzeichen (Z. 783, KONVENTIONEN Z. 86).**
- Belegt ist das Layout für den Vektorkanal (`GetData` auf „Vib 3D“ und `Get3DData`). Ob die Displays Betrag/Phase auf einem Vektorkanal den Vektorbetrag oder je Komponente liefern, ist nicht belegt [U]. I2 behauptet A = √(Aₓ²+A_y²+A_z²) mit „Phase nicht verfügbar“. Eine Quelle dazu habe ich im Textextrakt nicht wiedergefunden [U]. Für 3D deshalb nur Real&Imag verwenden und den Betrag selbst berechnen.
- Der KONVENTIONEN-Satz „positive Geschwindigkeit = Bewegung in Richtung Scankopf“ (KA 2-32) gilt für die Kanäle je Kopf (1D-Modus). Für die Komponenten X/Y/Z gilt positiv = entlang der Achse des 3D-Koordinatensystems. Das ist nur über `PTCVibrationDirection` (+X/+Y/+Z) indirekt gestützt [U]. Den KONVENTIONEN-Satz so trennen.
- Die Mess-Koordinatendefinition (`CoordDefinitionMode`) gehört in die Metadaten.

**m3. FRF-Signale und Kombikanäle (Z. 716–719).** FRF, H1, H2, Kohärenz und CP liegen in Kombikanälen („Vib & Ref n“, „Vib 3D & Ref 1“; SWP Tab. 3.2, 3-31). Sie sind nur vorhanden, wenn ein Referenzkanal aktiv war. Die Signalnamen tragen die Einheit der Referenz (z. B. „H1 Geschwindigkeit/Spannung“). Ergänzen und Referenzgröße und -einheit aus `SignalDescription` prüfen.

**m4. Achsenarten (Z. 763–786).** Die Frequenzachse gilt nur für FFT. Zoom-FFT hat eine andere Achse (Mittenfrequenz). Für Zeitdaten gilt Δt = 1/f_Abtast mit f_Abtast = 2,5·BW (M-Systeme 2,56), `XAxis.Unit` ist s. Ergänzen.

**m5. FFT-Parameter in 2.5 (Z. 346–363).** Die Abhängigkeiten sind in Gl. 7.2–7.4 belegt und sollten stehen: f_Abtast = 2,5·BW (QTec-3D-H nicht M-System; Systemzuordnung bleibt [U]), t_Mess = n_FFT/BW, Δf = 1/t_Mess = BW/n_FFT. Prüfwerte: BW = 5000 Hz und 400 Linien ergeben Δf = 12,5 Hz, f_Abtast = 12 500 Hz, t = 0,08 s, N = 1000 Abtastwerte (nachgerechnet). `SampleFrequency` ist laut BEM rw, hängt aber von BW ab. Das Setzverhalten bleibt [offen]. Als Sollwert nur BW und Lines setzen und die abgeleiteten Größen zurücklesen und prüfen. Aus I2 offen: N = 2,5·n_FFT ist keine Zweierpotenz (TM 3-3), [U].

**m6. Generator-Signalformen (Z. 455–462).**
- `BurstStart` ist `Long` (ganzzahlige Prozent), `BurstStartEx` und `BurstLengthEx` sind `Double` (BEM). Die Referenz nennt nur die Nicht-Ex-Varianten. „In % der Messzeit“ ist in BEM nicht ausdrücklich, dort steht „in percent“.
- Die Liste „regen nur im Bereich Start…End an“ lässt Burst Random aus, obwohl SWA 7-16 es nennt. `WaveformBurstRandom` hat laut BEM keine eigenen Parameter.
- Amplitude als Spitzenwert bei hochohmigem Abschluss und 50-Ω-Halbierung sind korrekt (SWA 7-32).

**m7. Mittelung (Z. 374–382).** Typ „Magnitude“ heißt in der GUI „Amplitude“ und entspricht der Betragsmittelung ohne Phase. Das Verwerfen von Overrange-Spektren gilt mit einer Ausnahme (SWA 7-6): Haben alle bisher erfassten Spektren den Status Overrange, werden sie zunächst gemittelt, bis das erste Spektrum ohne Overrange kommt. Der Mittelungszähler wird dann zurückgesetzt. Überlappung nur ohne Trigger ist korrekt.

**m8. Kanalparameter (Z. 399–417; Kraftkanal).** Fehlende Punkte nach SWA 7-11/7-12:
- Der Vibrometerkanal ist fest DC-gekoppelt.
- IEPE an einem Referenzkanal schaltet auf AC-Kopplung mit analogem Hochpass um. Die Einschwingzeit beträgt bis zu 1 min, währenddessen wird Overrange angezeigt. Für Kraftkanäle ist das niederfrequenz-relevant.
- Der Kalibrierfaktor wird bei Vibrometerkanälen automatisch je Messbereich gesetzt. Negative Faktoren und die Option „Inv.“ (Kehrwert) sind erlaubt. Das ist vorzeichenrelevant für Kraft und Phase.

**m9. Pegelgrößen (Z. 259, 969).** `GetSignalAmplitudes` liefert die Aussteuerung der Kanäle vor der Koordinatentransformation (SWA 4.1.2.2 und Hinweis „Aussteuerung vor der Koordinatentransformation“). Der optische Signalpegel des Lasers ist `SensorHead.SignalLevel` (SWA, Feld „Optik“). Das sind zwei verschiedene Größen. Zeile 969 faltet sie zusammen: als „Signalpegel vor dem Scan“ zwei getrennte Zeilen führen. Zu P16: H-Systeme arbeiten mit 100 % Aussteuerungsreserve (SWA 8-5). Eine Anzeige über 100 % ist daher kein Clipping. Die 30–80 %-Regel stammt aus VFC [U].

**m10. Fensterparameter (Z. 411).** `ChannelAcqProperties.WindowFunctionParams` ist laut BEM read-only. Ob Parameter von Tapered Hanning, Kraft- und Exponentialfenster per COM setzbar sind (z. B. über den Properties-Container), ist [offen]. Als Prüfpunkt für den Messrechner aufnehmen.

**m11. 4.3 `Signal.Description`.** Das ist als Plausibilitätsmittel gut. `FunctionType` belegt: H1 = 300, H2 = 301, Kohärenz = 6, CP = 3, Zeit = 1, Spectrum = 12, FRF = 4. Außerdem gibt es PCA-Typen (302–304), die für U6 relevant sind. Ergänzen.

**m12. `ReferencePointIndex` (Z. 405).** Laut BEM wird er nur bei UFF-/ME'Scope-Export von FRF und CP benutzt. Für die Modalanalyse ist er die Bezugs-DOF der Anregung. Zusammen mit `DirectionOfVibration` des Referenzkanals zu den Metadaten (A2).

## 3. Ergänzungsliste für Abschnitt 6 (A2)

Verfügbarkeit: **COM** = per COM zur Laufzeit lesbar, **Datei** = per PolyFile/Messdatei lesbar, **nein** = nur manuelles Protokoll, **[U]** = nicht belegt.

| Größe | Warum (I2 §2.3 / Plausibilitätskriterium) | Verfügbarkeit laut Doku |
|---|---|---|
| Von/Bis (`StartFrequency`, `EndFrequency`), Bandbreite, Lines, abgeleitet f_Abtast, Δf, t_Mess, Overlap | Frequenzachse, P5 | COM und Datei (AcquisitionInfoModes), Z. 954, 2.5 |
| Mittelungstyp und -anzahl, `AverageCount` je Punkt, SE-Modus, Speckle Tracking, `SignalEnhancement` je Kanal (`SEActive`) | effektive Mittelungszahl (SWA 7-25), Phasenbezug | COM und Datei; je Punkt in der Datei: `MeasPoint.AverageCount` (Z. 965) |
| Fensterfunktion und Parameter je Kanal, RMS-Korrekturfaktor | P6, Skalierung | COM/Datei; Parameter schreiben [offen] (m10) |
| Trigger (Quelle, Flanke, Level, Pretrigger, `PhaseFromRef`) | Phasenbezug, P15 | COM und Datei |
| Referenzkanäle: `Reference`, `Active`, `Quantity`, `Calibration`, `InputRange`, Kopplung (IEPE/AC), `SignalDelay`, Kehrwert („Inv.“) | FRF-Einheit, Phase, Vorzeichen, Verzögerung | COM und Datei; „Inv.“ nicht als Property geprüft [U] |
| `ReferencePointIndex`, `DirectionOfVibration` je Kanal | Anregungs-DOF für die Modalanalyse | COM und Datei |
| Generator: Signalform und Parameter, Amplitude, Offset, `SteadyStateTime`, Generatorverstärker (`GeneratorAmplifierEnabled/Factor`), Amplitudenkorrektur | Anregungsreproduzierbarkeit | COM und Datei; Verstärkerfaktor in Z. 453 vorhanden, in der Tabelle 6 fehlend |
| Abschlussimpedanz des Generators (50 Ω/hochohmig) | Spannung am Shaker (SWA 7-32) | nein (nur manuell protokollieren); Eingangsimpedanz der Karte per COM (`InputImpedance`) |
| Messbereich und Filter der Vibrometer, `MaxVelocityRange`, `BandwidthRange`, Trackingfilter | Reproduzierbarkeit, Dropouts | COM und Datei; XML-Format [U] |
| Alignment-Details: `CoordDefinitionMode`, `Mirror`, Kopfpositionen (`GetScanHeadPosition`), `ScanHeadDistance`, Qualität je Abgleichpunkt (`Align3DPoint.Quality`) | P3, P4, Koordinatensystem | COM und Datei (Z. 961–962); Details fehlen in 6 |
| Koordinatensystem der Geometrie und Importeinheit (Skalierungsfaktor) | Geometrie | Importfaktor GUI [U] |
| Strahlgeometrie-Konditionszahl (P4) | Rauschverstärkung 3D | abgeleitet aus Kopfpositionen und Punktkoordinaten (beide COM/Datei); Zerlegungsmatrix selbst nicht dokumentiert [U] |
| Aussteuerung je Kanal und optischer Signalpegel je Kopf (getrennt) | P16, Signalqualität | COM live (`GetSignalAmplitudes`, `SignalLevel`), Datei nur über Status und `VibrometerRange` [U] |
| Modus und Kamera-/Zoom-Einstellungen | Alignment-Gültigkeit | nicht untersucht (Z. 336) |
| Zeitpunkt und Zeitzone der Messung; Warmlaufbeginn (30 min bzw. 120 min, KA S. 46) | P13 | `FileTime` ja, Zeitzone [offen]; Warmlaufbeginn nein |
| Lizenzierte Optionen (TDD, PCA …), PSV-Seriennummer | Rahmen | nein (nur GUI), Z. 971 |
| Versuchsrandbedingungen: Prüflingsbezeichnung, Lagerung, Befestigung, Anregungsort und -richtung, Shaker/Hammer-Typ, Kraftsensor-Typ und -Empfindlichkeit, Oberflächenpräparation, Messabstand, Umgebungstemperatur, Messung durch Glas oder Medium | I2 §2.3, §5.1 | nein, nur Protokoll (`protokoll.md`, versuchsplanung) |
| Scanzeit, Statusverteilung, Overrange-Anteil, Anzahl Nachmessungen | P2 | Status je Punkt: Datei ja; Scanzeit/Nachmessungen nicht belegt [U]; Meldungen: `SummaryInfo.Subject` (BEM belegt) |
| Kombinierte Dateien (`ContainedFiles`) | P14 | Datei, Einzelheiten [U] |

## 4. Machbarkeit der Auswertungen aus COM/PolyFile-Daten (A3)

Legende: **machbar** = mit den belegten Daten ohne weitere Hardware; **mit Voraussetzung** = nur, wenn die genannte Bedingung bei der Messung erfüllt war; **nicht machbar** = Daten fehlen.

| Auswertung | Einstufung | Begründung und Beleg |
|---|---|---|
| Spektren je Punkt (Real/Imag, Betrag), x/y/z oder Vib 3D, Einheit m/s, Amplitude 0-to-peak | machbar | `DataPoint.GetData`/`Get3DData` (BEM Access to Data); Skalierung TM 3-3, Matlab-Folie 9. Skalierung und Phasenbezug dokumentieren (M2). |
| Peak-Picking, Eigenfrequenzen, −3-dB-Dämpfung (SDOF), FG-04 | machbar | Aus dem Betragsspektrum. Auflösung begrenzt durch Δf (BW/n_FFT). Halbwertsbreite gilt für ζ ≪ 1 (I2 FG-04); Fenster-Scalloping beachten (I2 §3.2). |
| Integration und Differentiation (Weg, Beschleunigung) | machbar | Polytec berechnet die Größen aus der Auswahl in der Datei (SWA 7-12). Eigene Umrechnung im Frequenzbereich mit 1/(iω) möglich. |
| FRF H1/H2/Kohärenz aus der Datei | mit Voraussetzung | Nur, wenn ein Referenzkanal aktiv war (Kombikanäle, SWP 3-31). Mit Spannungsreferenz in (m/s)/V, relative FRF inklusive Verstärker/Shaker; Mobilität (m/s)/N nur mit Kraftsensor, `Quantity` Kraft und Kalibrierfaktor. Hv ist von Polytec nicht geliefert. |
| ODS und Animation (Re{A·e^{iωt}}) | mit Voraussetzung | Phase nur mit Referenz oder Trigger (TM Tab. 6.1). Besser deterministische Anregung mit Komplexmittelung, bei stochastischer Anregung Referenz und H1 (TM 3-6). Gültiger 3D-Abgleich, Punktstatus filtern. ODS ist nicht gleich Eigenform. Das Punktmittel (Betragsmittel) ist für ODS nicht geeignet. |
| Modalanalyse: Eigenfrequenzen, Dämpfung, unskalierte Formen (SDOF/MDOF, LSCF/PolyMAX, MAC) | mit Voraussetzung | Eine FRF-Spalte (fester Anregungspunkt, alle Messpunkte, 3 Komponenten) ist verfügbar. Mit Spannungsreferenz sind Frequenzen und Formen näherungsweise nutzbar, Genauigkeit durch Shaker-Struktur-Kopplung eingeschränkt [E]. Eigene MDOF-Schätzung ist extern in Python möglich (PSV hat nur SDOF-Peak-Fit, SWP 3-14). |
| Skalierte Modalparameter (Modalmasse, Residuen), absolute FRF | mit Voraussetzung (Kraftmessung) | Braucht Kraftsensor am Referenzkanal mit Kalibrierfaktor und Referenz-DOF (`ReferencePointIndex`, `DirectionOfVibration`). Ohne Kraft nicht machbar. |
| Mehrfachanregung (MIMO), nahe beieinander liegende Moden sicher trennen | mit Voraussetzung | Polytec-intern PCA-Option (SWA 7-7; TM Kap. 8); PSV unterstützt derzeit nur einen Generator (BEM `GeneratorsOn`). Extern: mehrere Messläufe mit verschiedenen Anregungspunkten, Gruppierung nur über eigene Metadaten [E]. |
| Plausibilität P1 Kohärenz | mit Voraussetzung | Referenzkanal und Kombikanal nötig. |
| P2 Status, P3 Alignment-Qualität, P5 Einstellungskonsistenz, P6 Signal-Fenster-Matrix, P8 Sweep-Parameter, P11 Auflösungsregel, P14 Stitching, P15 Phasenreferenz | machbar | Aus Status, Alignment, Properties und Metadaten (Abschnitt 6, A2); P11 aus Δf und der −3-dB-Breite. P14 [U] bei kombinierten Dateien. |
| P4 Strahlgeometrie (Konditionszahl) | machbar (abgeleitet) | Aus Kopf- und Punktkoordinaten; die Polytec-Zerlegungsmatrix ist nicht belegt [U]. |
| P9 Wiederholbarkeit, P10 Nichtlinearität | machbar | Zwei oder mehr Messdateien; `Generator.Amplitude` per COM stufbar. |
| P13 Aufwärmzeit | mit Voraussetzung | Zeitstempel `FileTime` plus manuelles Protokoll (Zeitzone [offen]). |
| P16 Aussteuerung | mit Voraussetzung | Nur live (`GetSignalAmplitudes`) bzw. über `VibrometerRange`/Overrange-Status; 30–80 % nicht für QTec belegt [U]. |
| P17 Niederfrequenz-Check | machbar | Aus dem Spektrum, nur bei Fußpunktanregung. |
| P7 Burst-Abklingen, P12 Parseval-Test, logarithmisches Dekrement, Hammer-Kraftfenster nachträglich, eigene Welch-/H1-Schätzung, Neu-Fensterung | mit Voraussetzung (Zeitdaten, TDD) | Der Modus Zeit braucht die Option TDD (SWA 7-2, 7-34). `SaveTimeDataForScan` setzt SE auf „Fast“. Lizenzbedarf [offen]. Ohne Zeitdaten nicht machbar, da Fenster und Mittelung bei der Erfassung festgelegt wurden. P12 nur gegen die Polytec-RMS-Domain wäre kein unabhängiger Zeitbereichstest. |
| Eigene Spektralschätzung mit Welch-Mittelung als Gegenprobe | mit Voraussetzung (Zeitdaten) | siehe oben; Speicher: Dateigröße > Kanäle · Abtastwerte · 4 Byte (SWA 7-34). |
| Impulshammer-Auswertung | mit Voraussetzung | Trigger extern/analog, IEPE-Kraftkanal, Kraft- und Exponentialfenster (F04 S. 18–23); Parameter per COM [offen] (m10); Hammer nicht über den PSV-Generator. |

## 5. Was nicht prüfbar war (A4)

- **Reale Messdatei:** Verhalten von `XAxis`, Datenlänge bei Von/Bis, DC-Linie, Bin-Konvention (Mitte oder Kante), Zeitzone `FileTime`. Die Matlab-Folie 8/9 stützt nur „konsistent“.
- **Python/pywin32, Threading, Casting auf Default-Interfaces:** nicht bewertet (Abgrenzung).
- **Die Zeilen 590–680 (3.3 ff.) sowie Abschnitte 5, 7, 8, 10 und 11 der Referenz** habe ich nicht gelesen. Von den Enum-Werten aus Abschnitt 8 habe ich nur Display-, Function-, Domain-, Build-Flag- und VibrationDirection-Typen gegengeprüft, nicht Acq-Mode, Scan-Status und weitere.
- **Quelle der 3D-Betragsformel in I2 (Tabelle 3.8):** im Textextrakt nicht wiedergefunden. Ob „Vib 3D“-Betrag/Phase-Displays den Vektorbetrag liefern, ist [U].
- **Rechengleichungen aus TM (H1/H2/Kohärenz)** wurden nicht neu abgeleitet. Ich habe auf I2 vertraut.
- **Systemtyp:** ob der QTec 3D als „kein M-System“ (also 2,5·BW) arbeitet, ist aus den Handbüchern nur indirekt (H-System) belegt. Gegenprobe am Gerät über `SampleFrequency`/`SampleResolution`.
- **Lizenz:** ob `SaveTimeDataForScan` TDD erfordert; welche Optionen am Messrechner installiert sind.
- **Nicht aus den Unterlagen ableitbar:** Aussteuerungsgrenzen des QTec (30–80 %), Strahlzerlegungsmatrix, Hardwaredaten des QTec (kein Spezifikationshandbuch im Input).

## Rückmeldung an den Orchestrator

**Paket:** I5-F · **Status:** ERLEDIGT

**Ergebnis:** Fachanalyse im Bericht oben (keine Dateien geändert). Geprüft wurde `/home/user/BA_Jakob-Busch_P/in_progress/analysen/2026-10-23_I5_com-referenz.md` gegen BEM-Textfassung und PDFs.
**Wie verifiziert:** Gegenlesen der Primärquellen (BEM-Text, SWA-PDF-Seite 225 als Bild, Matlab-Folien 8/9). Prüfskript `chk.py` (Scratchpad `/tmp/claude-0/-home-user/e6b61297-17fb-5003-91f8-95c4534d012c/scratchpad/i5f/chk.py`) bestätigt:
- Frequenzachse BW 5000 Hz, 400 Linien: Δf = 12,5 Hz, f₁ = 12,5 Hz, f₄₀₀ = 5000 Hz, konstanter Abstand.
- f_Abtast = 12 500 Hz, t = 0,08 s, N = 1000.
- Komplexes 3D-Layout RX0, IX0, …: `reshape(3, n, 2)` ergibt x/y/z korrekt.
- Von/Bis-Beispiel (1000–4000 Hz): 241 Linien statt 400.
**Akzeptanzkriterien:** A1 ✅ (0 BLOCKER, 4 MAJOR, 12 MINOR, mit Fundstelle, Soll mit Beleg, Ist, Korrektur) · A2 ✅ (Abschnitt 3) · A3 ✅ (Abschnitt 4) · A4 ✅ (Abschnitt 5).
**Befunde:** M1 Von/Bis und Frequenzachse (Z. 743, 353; KONVENTIONEN); M2 Skalierung und Phasenbezug fehlen (Z. 738–786); M3 Metadaten unvollständig (Z. 975, U3); M4 U6 ohne Voraussetzungen Kraft, Phase, TDD (Z. 1140). MINOR m1–m12 siehe Abschnitt 2.
**Annahmen:** Der QTec-3D-H wird als Nicht-M-System geführt (f_Abtast = 2,5·BW). Das ist über die H-System-Zuordnung nur indirekt belegt.
**Unsicherheiten:** siehe Abschnitt 5. Wichtigste: Datenlänge bei Von/Bis, Lizenzbedarf `SaveTimeDataForScan`, 3D-Betrag-/Phasen-Display auf Vektorkanälen, Setzbarkeit der Fensterparameter per COM.
**Rechercheaufträge:** keine neuen. Für die Thesis weiterhin allgemeine Quellen zu H1/H2, Fensterung und Modalanalyse (laut I2 §7).

**Rückfragen:**
- [nicht blockierend] Soll das Paket die Referenz in M1–M4 und m1–m12 korrigieren lassen (Korrekturpaket an `software-engineer`)? — *Annahme bis zur Klärung:* Die Referenz bleibt unverändert; Adapter und Tests lesen die Frequenzachse aus `XAxis`.

**Vorschlag für KONVENTIONEN.md:**
1. Frequenzachse: „Vorläufig: f_k = k·Δf mit k = k_min…k_max, Δf = BW/n_FFT. Der Vollbereich ist k = 1…n_FFT. Bei eingeschränktem Von/Bis enthält die Datei möglicherweise weniger Linien (SWA 7-17, [U]). Die Achse wird aus `XAxis` gebildet und gegen k·Δf geprüft.“
2. Spektren: „Polytec-Spektren sind einseitig, amplitudentreu auf 0-to-peak skaliert (TM 3-3). Real/Imag entsprechen A·e^{iφ₀} bei e^{+iωt}. Phase ist nur mit Referenz oder Trigger gültig (TM Tab. 6.1).“
3. Vorzeichen trennen: Kanäle je Scankopf (1D): positiv = Richtung Scankopf. X/Y/Z-Komponenten: positiv = entlang +Achse des 3D-Koordinatensystems.
**Thesis-Bezug:** Kapitel Methodik/Umsetzung (Datenzugriff, Konventionen, Metadaten), Analyse und Auswertung (Machbarkeit der Auswertungen).
**Empfehlung für den nächsten Schritt:**
1. Korrekturpaket für die Referenz (M1–M4, m1–m12).
2. KONVENTIONEN-Änderung nach Rückfrage beim Nutzer.
3. Am Messrechner prüfen: XAxis und Datenlänge bei Von/Bis, Fensterparameter per COM, Lizenz `SaveTimeDataForScan`, Vorzeichen und Betrag der 3D-Komponenten.
4. Der Experte erstellt als Nächstes die Fachgrundlage FG-01 (Spektralschätzung nach Polytec-Konvention), mit den Messdatei-Sollwerten aus der Prüfliste.