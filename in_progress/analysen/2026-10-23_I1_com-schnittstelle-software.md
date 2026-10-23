<!-- Analysebericht I1 – COM-Schnittstelle, Polytec File Access, Beispielbibliothek STABCOOL; erstellt im Paket der Input-Sichtung von software-engineer (opus); unverändert übernommen. Pfadangaben zum Scratchpad verweisen auf flüchtige Hilfsdateien der Cloud-Sitzung. -->

## Analysebericht I1: Schnittstellen- und Softwaredokumentation Polytec PSV (COM)

### Quellen und Kürzel
Alle Pfade liegen unter `/home/user/BA_Jakob-Busch_P/Input/literatur/`.
- **[COM]** `polytec/06_Automatisierung_via_COM/06_Automatisierung_via_COM .pdf` (Polytec, 13 Folien, Stand 12/5/2025), Angabe als Folie n. Der Code ist dort nur als Bildschirmfoto enthalten; ich habe die Folien 10 bis 12 gerendert und abgelesen.
- **[BEM]** `polytec/Windows Hilfedateien/Basic Engine Manual.chm`, Angabe als CHM-Thema (Dateiname des Themas).
- **[PFA]** `polytec/Windows Hilfedateien/Polytec File Access_Object Model Reference.chm`, Angabe als CHM-Thema.
- **[HB]** `polytec/Handbücher/Software Handbuch PSV.pdf`: Handbuch zur Datenerfassung, „Version 10.1“ (PDF-S. 1), erstellt 2022. Angabe als gedruckte Seite mit PDF-Seite in Klammern.
- **[KA]** `polytec/Handbücher/Kurzanleitung psv_QTec-3d.pdf`: Das ist inhaltlich die Betriebsanleitung der Hardware PSV-QTec-3D-H (Dok.-Nr. 43695, 2023), keine Software-Anleitung.
- **[PFA-M]** `polytec/Schulungsunterlagen/11.2 Polytec-File-Access_Matlab.pdf` (13 Folien).
- **[TM]** `polytec/Handbücher/Theory Manual.pdf` (englisch, 2015), nur gezielt gelesen.
- **[PRES]** `PsvPres_deu.chm` (Auswertung). **[PSVH]** `Psv_deu.chm` (Datenerfassung, entspricht inhaltlich [HB]).
- **[STC]** `Example_Library_STABCOOL/…`, Angabe als Datei:Zeile.

**Entpacken der CHM-Dateien:** Das hat funktioniert. Ich habe per `apt-get` die Pakete `p7zip-full` und `libchm-bin` installiert, die Dateien mit `extract_chmLib` entpackt und das HTML mit einem eigenen Python-Skript in Text umgewandelt (alles im Scratchpad unter `…/scratchpad/i1/chm` und `…/i1/ctxt`). Entpackt wurden Basic Engine Manual (4734 Dateien), Polytec File Access (2663), Psv_deu, PsvPres_deu und PsvMsa100_3D_deu. Im Repository wurde nichts geändert.

---

### 1. Objektmodell und Ablauf „verbinden → einstellen → scannen → speichern → Daten lesen“

**Aufbau.** Das Objektmodell ist auf mehrere Typbibliotheken verteilt: PSV, PolyFile, PolyProperties, PolySignal, PolyWaveforms, PolyAcquisition, PolyScanHead, PolyAlignment, PolyBands, PolyFrontEnd, PolyMath und weitere ([BEM] Inhaltsverzeichnis).
- Einstieg ist das Objekt `Application`. Die Entwicklungsumgebung bindet die abhängigen Bibliotheken automatisch ein ([COM] Folien 6 bis 8).
- Für einen anderen Anregungstyp (z. B. Chirp statt Sinus) braucht man die PolyWaveforms-Bibliothek. Zum bloßen Einschalten des Generators reicht `GeneratorsOn` ([COM] Folie 7).

**Zentrale Objekte (alle belegt):**

| Objekt | Belegte Mitglieder und Fakten | Quelle |
|---|---|---|
| `AcquisitionInstance` (ProgID `"PSV.AcquisitionInstance"`) | `GetApplication(vbCreate, lTimeOut=10000)` gibt `IApplication5` zurück; `IsRunning`. Nicht verfügbar für VibSoft und für Desktop-Versionen von PSV. | [BEM] PSV~AcquisitionInstance, ~GetApplication |
| `PresentationInstance` (`"PSV.PresentationInstance"`) | Instanz im Auswertemodus, z. B. `oApp.Documents.Open(...)` | [BEM] PSV~PresentationInstance |
| `Application` (`"PSV.Application"`) | `Acquisition`, `Settings`, `Documents`, `ActiveDocument`, `Exporter`, `Mode`, `Version`, `Visible`, `Quit`, `SuppressMessagesForAutomation`, `MessagesLoggingEnabled`, `WarningLevel`; Events `MessageOccurred`, `Quit`, `QuitEx` | [BEM] PSV~Application_members |
| `Acquisition` | Methoden: `Scan(PTCScanMode)`, `ScanEx(Mode, Caps)`, `Start(PTCAcqStartMode)`, `Stop`, `GetData(Display)`, `GeometryScan`, `AutoFocusLaser`, `AssignFocusAutomatically`, `SetLaserOn`/`GetLaserOn`, `GetSignalAmplitudes`, `Get/SetSelectedMeasPoints`, `ExportVideoSnapshot`. Eigenschaften: `ScanFileName`, `State`, `Mode` (PTCAcqMode), `ActiveProperties`, `ModeProperties`, `Infos`, `PointDomains`, `GeneratorsOn`, `ScanCaps`. Events: `AcqStateChanged`, `ScanStateChanged` | [BEM] PSV~Acquisition_members |
| `Settings` | `Load(Datei, PTCSettings)`, `Save(Datei)`, `Delete`. PTCSettings umfasst u. a. Acquisition=2, APS (Scanpunkt-Definition)=312, 3DAlignment=1024, CameraAndAlignment=68, All=65535. Laden ist auch aus einer Messdatei möglich. | [BEM] PSV~Settings~Load, PSV~PTCSettings |
| `AcquisitionProperties` (typisierte Collection) | `FftProperties`, `AverageProperties`, `ChannelsProperties`, `GeneralProperties`, `GeneratorsProperties`, `TimeProperties`, `TriggerProperties`, `VibrometersProperties`, … jeweils mit `Has…` | [BEM] PSV~AcquisitionProperties_members |
| `FftAcqProperties` | `Bandwidth` [Hz], `StartFrequency`, `EndFrequency` [Hz], `Lines`, `Overlap` [%], `SampleFrequency` [Hz], `SampleResolution` [Hz], `Samples`, `SampleTime`, `FftAcqPropertiesValidator` | [BEM] PSV~FftAcqProperties_members |
| `AverageAcqProperties` | `Count`, `Type` (PTCAverageType: Off 0, Magnitude 1, Complex 2, Time 3, Peakhold 4) | [BEM] PSV~AverageAcqProperties_members, POLYPROPERTIESLib~PTCAverageType |
| `GeneralAcqProperties` | u. a. `SaveTimeDataForScan`, `AutoRemeasure`, `RealSampleFrequency` | [BEM] PSV~GeneralAcqProperties_members |
| `GeneratorAcqProperties` | `Active`, `Amplitude` [V], `Offset` [V], `SteadyStateTime` [s], `Waveform` (IWaveform); Waveform-Klassen mit ProgID `PolyWaveforms.WaveformSine`, `…Sweep`, `…PeriodicChirp`, `…BurstChirp`, `…PseudoRandom`, `…WhiteNoise` u. a. | [BEM] PSV~GeneratorAcqProperties_members, POLYWAVEFORMSLib |
| `ChannelAcqProperties` | u. a. `Active`, `Reference`, `ReferencePointIndex`, `InputRange` [V], `Calibration` (SI), `Quantity`, `Unit`, `WindowFunction`, `DirectionOfVibration` | [BEM] PSV~ChannelAcqProperties_members |
| `InfosAcq` | `MeasPoints` (IMeasPoints11), `Elements`, `Alignments`, `Hardware`, `ScanHeadDevicesInfo`, `Vibrometers`, `PositionDevice` | [BEM] PSV~InfosAcq_members |
| `Exporter` / `ExportParameters` | `Application.Exporter(Eingangsdatei, PTCExportType)`, `Export`/`ExportAsync`/`CancelAsync`, Events `ProgressChanged` und `ExportCompleted`; Exporttypen UFF=0, ME'Scope=1, ASAM ODS ATFX=2; `PointSignals` als Zeichenketten wie `"FFT \ Vib \ Displacement"` | [BEM] PSV~Exporter, PSV~PTCExportType |

Zustände und Modi:
- **PTCAcqState:** Stopped 0, Single 1, Continuous 2, ScanAll 3, ScanContinue 4, ScanRemeasure 5, AutoFocus 6, PathLength 7.
- **PTCScanMode:** All 0, Continue 1, Remeasure 2, RemeasureAutoRange 3, RemeasureFile 4.
- **PTCScanCaps:** None 0, UseAssignedFocusValues 1, VideoTriangulation 2, AutoFocusDuringScan 8, AsynchronousScanEvent 16.
- **PTCAcqMode:** Time 0, FFT 1, ZoomFFT 2, MultiFrame 3, FastScan 4.
- Quellen: [BEM] PSV~PTCAcqState, ~PTCScanMode, ~PTCScanCaps, POLYPROPERTIESLib~PTCAcqMode.

**Ablauf mit Belegen:**
1. **Verbinden.** `new AcquisitionInstance` → `GetApplication(true, 10000)` → `psv.Version` ([COM] Folie 10). Bei der Vorführung wurde „10.2.1.1“ ausgegeben ([COM] Folie 12). Laut [BEM] ~GetApplication läuft die Kommunikation eines externen Clients mit der Acquisition-Instanz über „inter-process communication (DCOM)“, auch lokal.
2. **Einstellen.**
   - Messparameter lassen sich im Dialog oder durch Laden einer Einstellungsdatei setzen ([HB] 7-1, PDF 209).
   - Eine `.set`-Datei enthält Erfassungsparameter, Scanpunkte, 2D-/3D-Abgleich und Optik, aber keine Frequenzbänder ([HB] 10-10, PDF 322).
   - Erfassungseinstellungen lassen sich nur bei gleicher Erfassungskarte und Anschlussbox laden ([HB] 10-4, PDF 316).
   - Per COM: `Settings.Load` sowie `Acquisition.ActiveProperties`/`ModeProperties`.
3. **Scannen.** `acquisition.ScanFileName = @"D:\Temp\Scan.svd"`, dann `ScanEx(ptcScanAll, ptcScanCapsNone)`, dann eine Warteschleife `while (State != ptcAcqStateStopped) Sleep(1000)` ([COM] Folie 12, inhaltlich gleich dem VBA-Makro `SettingsAndScan.bas`, [COM] Folie 11).
   - Event-Folge: `BeginScan(0)` → je Punkt `BeginScanPoint(n)`/`EndScanPoint(n)` → `EndScan(0)`. `n` ist 1-basiert, die Reihenfolge der Punkte legt die Software fest ([BEM] PSV~Acquisition~ScanStateChanged_EV).
   - Ist `ScanFileName` leer, fragt die Software beim Start per Dialog nach dem Dateinamen ([BEM] ~ScanFileName).
4. **Speichern.** Beim Scan speichert die Software jeden Punkt sofort in die `.svd`: Einstellungen, Spektren je vollständig gemessenem Punkt, gemitteltes Spektrum und Effektivwert über die gesamte Bandbreite. Auch bei Abbruch bleiben die gemessenen Punkte erhalten ([HB] 10-8, PDF 320; 8-3, PDF 249). Zeitsignale werden nur im Messmodus Zeit (Option TDD) bzw. über `SaveTimeDataForScan` gespeichert ([HB] 7-2/7-34, PDF 210/242; [BEM] GeneralAcqProperties).
5. **Daten lesen.**
   - Live während der Erfassung: `Acquisition.GetData(Display)` → `AcquisitionPointData.OpenDataStream` → `Read` ([BEM] PSV~Acquisition~GetData).
   - Aus der Datei über PolyFile (Abschnitt 3).

---

### 2. Zugriff aus Python 3.11

**Belegt:**
- Grundsätzlich kann jede COM-fähige Sprache genutzt werden ([PFA] Overview). Die Betreuernotiz sagt dasselbe für Python ([COM] Folie 2).
- Polytec liefert mit Polytec File Access eigene **Python-Beispiele** (`Examples\Python`, u. a. `band_average.py`, `calculate_fft.py`, `Enums.py`). Als Abhängigkeiten nennt Polytec `pip install -U numpy pywin32 pillow matplotlib` ([PFA] Examples). Das ist der einzige Beleg für eine konkrete Python-COM-Bibliothek (**pywin32**). comtypes erwähnt die Doku nirgends.
- **Early vs. Late Binding:** Beides ist möglich; Polytec empfiehlt early binding ([BEM] Access to Interfaces).
  - Methoden und Eigenschaften liefern teils ältere Interfaces (z. B. `IPolyFile8`). Dann muss man auf das Default-Interface casten.
  - Neue Interface-Versionen werden zum Default; ältere bleiben stabil.
- **Collections:** Indizes sind 1-basiert. Ausnahme: `Vibrometers` ist 1-basiert, `Controllers` und `SensorHeads` sind 0-basiert ([BEM] Access to General Information).
  - Typisierte Collections geben `Nothing` zurück, wenn ein Element fehlt.
  - Benannte Collections akzeptieren deutsche und englische Namen („Geschwindigkeit“/„Velocity“, „Zeit“/„Time“) ([BEM] Using Collections).
- **Meldungen und Fehler:**
  - `SuppressMessagesForAutomation` ist standardmäßig `True`. Statt eines Dialogs wird das Event `MessageOccurred(Style, Text, ByRef Answer)` ausgelöst; über `Answer` lässt sich eine Benutzerantwort simulieren ([BEM] ~SuppressMessagesForAutomation, ~MessageOccurred_EV).
  - Ohne Unterdrückung können Meldungen Makros unterbrechen. Meldungen lassen sich in die Windows-Ereignisanzeige protokollieren ([HB] 3-23, PDF 67).
- **Timeout:** Belegt ist nur `GetApplication(..., lTimeOut)` in ms, Standard 10000 ([BEM]).
- **Events:** Belegt sind sie nur für die Makrosprache (`WithEvents`, „effizienter als Warteschleife“, [BEM] Working with Objects). Das Polling von `State` ist der von Polytec selbst gezeigte Weg für externe Programme ([COM] Folie 12).
- **Lokal vs. DCOM:** Lokal läuft es ohne Weiteres. Für einen fremden PC braucht man DCOM mit Serverangabe und „sehr vielen aufwendigen Sicherheitseinstellungen“ ([COM] Folie 13).
- **Bitness / Betriebssystem:** Das Data Management System PSV-W-600 läuft unter Windows 10 Enterprise LTSB (64 Bit) ([KA] 3-5, PDF 51). Das Handbuch nennt Windows 10 (64 Bit) für Erfassungssysteme ([HB] PDF 18). Die Bitness der COM-Server ist nirgends dokumentiert.
- **Software auf dem Laborrechner:** „Falls Sie zusätzliche, nicht von Polytec angebotene Komponenten installieren möchten, setzen Sie sich mit Polytec in Verbindung“; außerdem keine optionalen Windows-Updates und keine Treiberupdates ([KA] 1-4, PDF 8). **Das betrifft direkt die Installation von Python, uv und pywin32 auf dem Messrechner.**

**Einschätzungen (nicht belegt, als solche gekennzeichnet):**
- Die Typbibliothek legt nahe, dass `AcquisitionInstance`/`Application` als Out-of-Process-Server laufen. Dann wäre die Bitness von Python für PSV egal. Für PolyFile (In-Process laut C++-Beispiel mit `#import`) muss Python vermutlich zur Bitness der installierten DLLs passen. Das muss am Laborrechner geprüft werden.
- pywin32 initialisiert im Hauptthread ein Single-Threaded Apartment (STA). Wenn COM in einem Hintergrundthread läuft (für die GUI nötig), braucht dieser Thread ein eigenes `CoInitialize`, und COM-Objekte dürfen nicht über Threads hinweg geteilt werden. Die Doku erwähnt `CoInitialize` nur im C++-Beispiel ([PFA] Examples, CplxPointAvg).
- Events aus Python (pywin32 `DispatchWithEvents`) erfordern vermutlich eine Nachrichtenschleife. Ein Polling von `State` mit eigenem Gesamt-Timeout ist robuster und für den ersten Stand ausreichend.
- `ByRef`-Ausgabeparameter (z. B. `MeasPoint.CoordXYZ(ByRef x, y, z)`, [PFA] POLYFILELib~MeasPoint~CoordXYZ) kommen in pywin32 voraussichtlich als Tupel zurück. Das ist am Gerät zu verifizieren.
- Fehler kommen in pywin32 voraussichtlich als `pywintypes.com_error`. Die Doku nennt keine Fehlercodes für Scan und Acquisition (gezielt gesucht, nichts gefunden).

---

### 3. Datenzugriff: Polytec File Access (PolyFile)

**Belegt:**
- PolyFile liest PSV-Messdateien (Einzelpunkt und Scan), MPV- und VibSoft-Dateien sowie Einstellungsdateien ([PFA] Overview), ab PSV 7.0 ([BEM] Opening and Closing Files). ProgID `"PolyFile.PolyFile"`.
- Polytec File Access braucht **keinen Dongle** und ist über „Polytec Update“ erhältlich ([PFA-M] Folie 2). Die Beispiele liegen unter `C:\Program Files\Polytec\Polytec File Access 5.6\Examples` ([PFA-M] Folie 3).
- **Exklusiver Dateizugriff:** Eine Datei kann nicht gleichzeitig von PolyFile und PSV geöffnet sein, sonst gibt es eine Sharing Violation ([BEM]/[PFA] Opening and Closing Files). Konsequenz: Das Scan-Dokument muss in PSV geschlossen werden, bevor es mit PolyFile gelesen wird (Folgerung).
- **Navigation:** `GetPointDomains(BuildFlags)` → Domäne („Time“, „FFT“, „RMS“, „1/3 Octave“) → `Channels("Vib")` → `Signals("Velocity")` → `Displays("Real")` → `DataPoints(i).GetData(Display, Frame)`. Daneben gibt es `GetPointAverageDomains` und `GetBandDomains` ([BEM]/[PFA] Access to Data).
- **Rückgabeformat:**
  - Ein 0-basiertes Array aus **Single (float32)**.
  - Zwei Größen in einer Anzeige (Real & Imag., Mag. & Phase) werden **verschränkt** geliefert: gerade Indizes enthalten Real bzw. Betrag, ungerade Imag. bzw. Phase.
  - Bei 3D-Kanälen kommen erst alle x-, dann alle y-, dann alle z-Werte.
  - Im FFT-Modus beginnen die Daten bei Linie 1 (Index 0).
  - Frame 0 ist der Mittelwert-Frame.
  - Quellen: [BEM] Access to Data; [PFA] POLYFILELib~DataPoint~GetData, ~Get3DData.
- **3D:** Standard-Flag ist `ptcBuildPointDataXYZ` (Kanäle Vib X/Y/Z); `ptcBuildPointData3d` erzeugt den Kanal „Vib 3D“ ([PFA] ~GetPointDomains). `Get3DData` füllt bei 1D-Daten mit Nullen auf.
- **Anzeigearten:** `ptcDisplayMagPhase` liefert die Phase **in Grad**, `ptcDisplayMagPhaseRad` (14) in rad, dazu gibt es `ptcDisplayRealImag` (9) ([PFA] POLYSIGNALLib~PTCDisplayType). Wichtig wegen der Konvention „Winkel in rad“.
- **Geometrie und Status:**
  - `MeasPoints` mit `CoordXYZ`, `CoordinatesToArray`, `VideoXY`, `ScanStatus`, `Label`.
  - `Elements` beschreibt die Vernetzung ([PFA] POLYFILELib~MeasPoints_members, ~MeasPoint_members).
  - Achtung bei geänderten Punktindizes: Die Matlab-Skripte arbeiten mit dem ursprünglichen Index ([PFA-M] Folie 6).
- **Schreiben:** Eigene Signale und Dateien lassen sich anlegen (Kanal „Usr“, `SignalDescription`, `SetData`, `Create`); die Ergebnisse sind in PSV darstellbar ([BEM] Access to Data, Creating New Files).
- **Exportalternativen:**
  - **UFF:** Datensätze 151, 164, 2411 (Knoten), 2412+82 (Elemente), 55 (Bänder), 58/58b (Punktdaten, Single Precision). Nicht im APS-Modus; Punkte „Nicht gemessen“ werden nicht exportiert ([HB] 10-15, PDF 327).
  - **ME'Scope** nur mit Option ExpME, **ATFX** nur mit Option ExpASAM ([HB] 10-8, PDF 320).
  - **ASCII-Export** von Messdaten in der Auswertung exportiert die *angezeigten* (ggf. gefilterten bzw. interpolierten) Daten ([PRES] 5_2_7).
  - Alle Exporte sind per COM über `Exporter` automatisierbar ([BEM] PSV~Exporter).
- **Proprietär:** `.svd`, `.pvd` und `.set` sind proprietäre Binärformate ([HB] 10-8, PDF 320).

**Was ohne PSV-Installation lesbar ist:**
- `.svd` nur mit installiertem Polytec File Access (Windows, COM, ohne Dongle). Auf Linux und in der Cloud gar nicht (Folgerung aus [PFA] Overview: COM-Komponenten).
- UFF, ASCII und STL sind offene bzw. textbasierte Formate. Dass sie unter Linux mit Python lesbar sind, ist eine Einschätzung; konkrete Leser habe ich nicht geprüft.

---

### 4. Was rechnet PSV selbst, was könnte oder müsste unser Paket leisten?

**PSV rechnet (belegt):**
- FFT, skaliert so, dass eine periodische Harmonische mit Amplitude 1 (Null-Spitze) eine Linie der Höhe 1 ergibt; die Anzahl der Abtastwerte ist eine Zweierpotenz ([TM] 3-3, PDF 13).
- AP, CP, FRF bzw. H1/H2 und Kohärenz ([TM] 3-4/3-5).
- FRF für alle Kombinationen Antwortkanal/Referenzkanal ([HB] 7-11, PDF 219).
- Mittelung: komplex, Betrag, Peak Hold, Zeit ([HB] 7-5, PDF 213).
- Fensterung, Filter, Integration/Differentiation ([HB] 7.2.3/7.2.5).
- Die 3D-Komponenten Vib X/Y/Z bei PSV-3D ([HB] 9-18, PDF 284).
- Mittelwertspektrum über alle Punkte, allerdings nur als Amplitudenmittel; ein komplexes Punktmittel bietet PSV nicht ([PFA] Examples, ComplexPointAverage).
- Bänder/RMS ([BEM] Access to Data).

**Was unser Paket voraussichtlich leisten müsste (Einschätzung, Abgrenzung durch Nutzer und Betreuer):**
- Ablaufsteuerung über mehrere Scans und Konfigurationen (Reproduzierbarkeit).
- Ablage mit Git-Hash nach KONVENTIONEN.
- Datenübernahme nach NumPy in SI-Einheiten und rad.
- Eigene Auswertung und Visualisierung, z. B. Peak-Picking, Betriebsschwingformen, Vergleich zwischen Versuchen, Kohärenzprüfung.
- Optional: eigene FFT/H1 aus Zeitdaten als unabhängiger Abgleich gegen PSV. Das setzt Zeitdaten voraus, also Option TDD bzw. `SaveTimeDataForScan`.
- Eine Multi-Referenz-Modalanalyse aus PSV-Frequenzgängen ist laut [HB] 7-10 nur mit Hauptkomponentenanalyse möglich (Option PCA, unkorrelierte Referenzen).

---

### 5. Konsequenzen für Simulator, Abstraktion und Cloud-Tests

- Die **Schnittstelle sollte sich am belegten Ablauf orientieren** (Einschätzung): `connect(timeout_s)`, `load_settings(path, parts)`, `configure(fft/average/generator…)`, `start_scan(file, mode)`, `state()` bzw. Fortschritt, `stop()`, `close()`. Getrennt davon ein **Leser** (`open(file)` → Punkte, Koordinaten, Spektren als float64, komplex, rad). Damit sind Simulator und PolyFile- bzw. UFF-Leser austauschbar.
- **Der Simulator muss modellieren:**
  - die Zustandsmaschine (PTCAcqState, Polling bis Stopped, Abbruch);
  - die 1-basierte Punktnummerierung und eine nicht fortlaufende Scanreihenfolge ([BEM] ScanStateChanged-Beispiel);
  - Timeout beim Verbinden;
  - Meldungen wie bei `MessageOccurred`;
  - Datenformate (float32, verschränkt, xyz nacheinander, Phase in Grad) als Adapterfälle;
  - synthetische Daten mit analytisch bekannter FRF (Referenzfall aus `in_progress/fachgrundlagen/`).
- Der **COM-Adapter bleibt dünn**: Er übersetzt nur Einheiten, Indizes und Formate, die Logik liegt testbar davor. Ausnahmen per `# pragma: no cover` nach KONVENTIONEN.
- pywin32 lässt sich unter Linux nicht importieren (Einschätzung). Der Import gehört daher nur in den Adapter, und Tests dazu bekommen einen Hardware-Marker.
- **Ohne echte `.svd`-Beispieldatei und daraus exportierte UFF- bzw. ASCII-Golden-Files** lässt sich der Leser in der Cloud nicht gegen reale Daten testen. Empfehlung: im Labor einen kleinen Referenzscan als `.svd` und UFF ablegen.
- Ein Hardwaretest ist erst nach Bestätigung durch den Nutzer bestanden (Ablauf G). Eine Prüfanleitung gehört ins jeweilige Umsetzungspaket.

---

### 6. STABCOOL-Beispielbibliothek: übernehmen bzw. vermeiden

**Wichtige Begriffsfalle:** In STABCOOL bedeutet „COM“ die *serielle* Schnittstelle (`com_port='COM4'`, pyserial; `isel_traverse.py:104`, `main_psd.py:72`). Bei Polytec meint „COM“ das *Component Object Model*. STABCOOL hat das Vibrometer offenbar analog über eine AD-Karte erfasst (`main_psd.py:205` „vibrometer only samples with 50kHz“), nicht über PSV. Das sollte in Anforderungen und Thesis klar unterschieden werden.

**Übernehmenswert:**
- Je Gerät eine Klasse (`GoldammerCard`, `Isel_Controller`/`Isel_Axis`).
- Eindeutige Geräteerkennung per Hash (`goldammer_card.py:24-48`).
- Software-Endlagen und Prüfung von Positionen und Geschwindigkeiten (`isel_traverse.py:86-97`, `:312`).
- Fehlercodes als Tabelle (`isel_traverse.py:14-30`).
- Plattformabhängiges Laden von Bibliotheken (`maiv2.py:822-838`).
- Dateinamen mit Zeitstempel und Position (`main_psd.py:229-231`).
- Prüfung der Messqualität mit Wiederholung (`main_psd.py:196-221`, als Idee).

**Vermeiden (belegt):**
- Konfiguration als Skript-Globals ohne Datei oder Schema (`main_psd.py:23-81`).
- `print` statt Logging bzw. Exception, z. B. bei Fehlercodes des Controllers (`isel_traverse.py:136-138`).
- Warteschleifen ohne Timeout (`isel_traverse.py:132-133`, `goldammer_card.py:259-261`).
- Stilles Ausweichen auf eine andere Abtastrate (`goldammer_card.py:146-151`).
- `update_properties` per `__dict__.update` ohne Validierung (`goldammer_card.py:82-83`).
- **Signaturfehler, nachgewiesen:** `main_psd.py:100` ruft `Isel_Axis(..., max_pos=590.)` ohne `min_pos` auf. Mit einem Stub-`serial` ausgeführt ergibt das `TypeError: Isel_Axis.__init__() missing 1 required positional argument: 'min_pos'`.
- **Amplitudenskalierung, nachgerechnet:** `main_psd.py:241` setzt die „FFT-Amplitude“ als `sqrt(psd)*2*df`. Für einen Sinus mit Amplitude 1 (fs = 192 kHz, 60 s, nperseg = 2880, Rechteckfenster) ergibt das 11,547 statt 1. `sqrt(2*psd*df)` liefert 1,000. Der Wert hängt also von df ab und ist keine Amplitude.
- Umwandlung in **float16** (`goldammer_card.py:112-113`) bei Daten, die `AD_ReadData` als double liefert. Die Genauigkeit fällt dadurch auf eps ≈ 9,8e-4; z. B. 3001 → 3000.
- `np.int` in `maiv2.py:201` gibt es ab NumPy 1.24 nicht mehr (AttributeError unter NumPy 2.5.4 geprüft).
- Der 32-Bit-Zweig lädt dieselbe x64-DLL (`maiv2.py:828-833`).
- Im Messordner werden PNG-Dateien gelöscht (`main_psd.py:270-272`). Rohdaten sind nicht betroffen, das Muster passt aber nicht zu „nie überschreiben“.

---

### 7. Handbücher unter `nicht vorhandene Systeme/`

Dort liegen nur Handbücher zu MSA, MSA 3D, Stage und UHF (je deutsch und englisch). Laut [KA] ist das vorhandene System PSV-QTec-3D-H mit den Scanköpfen PSV-I-680/690 und dem Frontend PSV-F-600-3D-H. **Für den Kern brauchen wir diese Handbücher nicht.**
- Ausnahme vielleicht „Stage“: Es gibt ein COM-Objekt `PositionDevice`/`PositioningStage` ([BEM] InfosAcq; PositioningStage gilt als veraltet). Das wird nur relevant, falls eine Positioniereinheit genutzt werden soll.
- Die MSA-Hilfe (`PsvMsa100_3D_deu.chm`) habe ich nur über das Inhaltsverzeichnis geprüft: Sie ist parallel zur PSV-Hilfe aufgebaut, mit Zusatz „Objektivkalibrierung/Übersichtsbild“. Für uns nicht relevant.

---

### A2: Wichtigste Quellen für die Thesis

| Datei | Kapitel/Seite | Wofür |
|---|---|---|
| [COM] 06_Automatisierung_via_COM .pdf | Folien 6–13 | Einstieg COM, Acquisition/PresentationInstance, Scan-Beispiel, DCOM-Aufwand |
| [BEM] Basic Engine Manual.chm | „Introduction to Automation“, „The PSV/VibSoft Object Model“, PSV Type Library (Application, AcquisitionInstance, Acquisition, Settings, Exporter, Enums) | Objektmodell, Binding, Collections, Events, Ablauf |
| [PFA] Polytec File Access….chm | Overview, Examples (inkl. Python/pywin32), Access to Data, PolyFile/DataPoint/MeasPoint | Datenzugriff, Formate, 3D-Daten |
| [HB] Software Handbuch PSV.pdf (V10.1) | Kap. 2.5 (S. 2-6), 3.6 (3-23), 7.1–7.2 (7-1…7-11, 7-34), 8.2 (8-2…8-4), 8.6/8.7 (8-11), 9.3 (9-18/9-19), 10.1.3, 10.2 (10-4…10-17) | Messablauf, Parameter, Optionen (TDD, Signalgenerator, ExpME/ExpASAM), Speichern/Export |
| [TM] Theory Manual.pdf | 3.2–3.5 (S. 3-3…3-5), 6 (Mittelung), 14.5 (14-7/14-8) | FFT-Skalierung, H1/H2/COH, 3D-Darstellung, für das Grundlagenkapitel |
| [KA] Kurzanleitung psv_QTec-3d.pdf | 1.3.6 (S. 1-4), 3.2 (S. 3-4/3-5) | Systembeschreibung, Laborrechner Windows 10 64 Bit, Hinweis zu Fremdsoftware |
| [PFA-M] 11.2 Polytec-File-Access_Matlab.pdf | Folien 2–6, 12 | PFA ohne Dongle, Punktindex-Falle, Koordinaten |
| [PRES] PsvPres_deu.chm | 5_2, 5_2_7 | Exportwege der Auswertung, ASCII-Export |
| [STC] STABCOOL | siehe Abschnitt 6 | Vorbild bzw. Gegenbeispiel Gerätesteuerung |

---

### A3: ADR-Vorschläge (nur Vorschlag)

1. **COM-Bibliothek:** pywin32 (`win32com.client`, von Polytec im PFA-Python-Beispiel genutzt) vs. comtypes (nicht in der Doku; Einschätzung: rein in Python, gute Typinformation) vs. .NET über pythonnet (Polytec zeigt C#/.NET). Kriterium u. a.: was auf dem Messrechner installiert werden darf ([KA] 1-4).
2. **Binding:** early binding (makepy/gencache, von Polytec empfohlen) vs. late binding (dynamisch, ohne Typbibliothek beim Build).
3. **Fortschritt und Ende des Scans:** Polling von `Acquisition.State` (belegt in [COM] Folie 12) vs. COM-Events `ScanStateChanged`/`AcqStateChanged` (belegt für Makros, für Python unverifiziert).
4. **Einstellen der Messparameter:** vorbereitete `.set`-Dateien laden (`Settings.Load`) vs. einzelne Properties per COM setzen vs. Mischform (Geometrie/Abgleich aus `.set`, Parameter per COM).
5. **Datenübernahme:** PolyFile/COM aus `.svd` vs. UFF-Export (`Exporter`, unter Linux lesbar) vs. Live-Abgriff `Acquisition.GetData`.
6. **Eigenes Ablageformat** für Messdaten und Metadaten inkl. Git-Hash: z. B. HDF5 vs. NPZ+JSON vs. nur Originaldateien plus Sidecar. Bibliothekswahl offen.
7. **Prozess- und Threading-Modell mit GUI:** eigener COM-Worker-Thread (STA) vs. separater Prozess für den Gerätezugriff.
8. **Wo die Software läuft:** lokal auf dem Data Management System vs. Fernsteuerung per DCOM. Laut [COM] Folie 13 ist DCOM aufwendig, daher eher lokal.

---

### A4: Nicht lesbar bzw. nicht prüfbar

- Keine reale COM-Interaktion möglich (keine PSV-Installation, kein Windows). Alle Aussagen zum Verhalten aus Python sind ungeprüft.
- Der Inhalt von `SettingsAndScan.bas` liegt nicht vor, nur ein Bildausschnitt der Zeilen 69–78 ([COM] Folie 11). Ebenso fehlen `RemoteAcquisition.bas`, `ComplexPointAverage.bas` und die PFA-Python-Beispiele (sie liegen in der Installation, nicht im Input).
- Die Versionen von Basic Engine Manual und PFA-CHM sind aus den Dateien nicht bestimmbar. Damit ist offen, ob sie zur installierten PSV-Version passen (Folie: 10.2.1.1; Handbuch: 10.1).
- Bitness und Threading-Modell der COM-Server sowie Fehlercodes (HRESULT) für Scan und Acquisition sind in der Doku nicht beschrieben.
- Ob `InfosAcq.MeasPoints` in der Datenerfassung per COM schreibbar ist (Scanpunkte erzeugen), ist nicht belegt. `MeasPoints.Add`/`Save` sind nur im Dateikontext beschrieben.
- Die Methode der 3D-Komponentenberechnung aus den drei Laserrichtungen ist im gelesenen Teil des [TM] nicht hergeleitet (nur die Darstellung, Gl. 14.1). Gleichungen in [TM] und Abbildungen in [HB] sind im Textauszug nicht lesbar (Formeln als Grafik).
- Nicht ausgewertet, aber möglicherweise relevant für die Thesis: Schulungsunterlagen 03, 04, 05.1, 06, 07, 10; Einpunkt-Vibrometer-Handbücher (VibroFlex); englische Manuals und Desktop-Handbücher (Duplikate); `MAIv2DLL_Help.chw` und Binärdateien von STABCOOL (nur Überblick).
- Die STABCOOL-Hardwarepfade sind nicht ausführbar. Geprüft habe ich nur die Signatur (mit Stub) und die Rechenformeln (synthetisch).

---

## Rückmeldung an den Orchestrator

**Paket:** I1 · **Status:** ERLEDIGT

**Ergebnis:** Analysebericht siehe oben (Abschnitte 1–7 und A2–A4). Im Repository wurde nichts geändert. Hilfsdateien liegen nur im Scratchpad unter `/tmp/claude-0/-home-user/e6b61297-17fb-5003-91f8-95c4534d012c/scratchpad/i1/`: `chm/` (entpackt), `ctxt/` (Text), `txt/` (PDF-Text), `img/` (gerenderte COM-Folien), `scripts/`, `venv/`. Installiert per apt: `p7zip-full`, `libchm-bin`.

**Belege und Verifikation:**
- Alle Aussagen zur API stammen direkt aus den CHM-Themen bzw. PDF-Seiten wie angegeben.
- Nachgerechnet bzw. ausgeführt: STABCOOL-Signaturfehler (TypeError), Amplitudenformel (11,547 statt 1,000), float16-Präzision, `np.int` unter NumPy 2.5.4.

**Akzeptanzkriterien:**
- A1 ✅ (alle Leitfragen mit Belegen)
- A2 ✅
- A3 ✅ (8 Vorschläge)
- A4 ✅

**Annahmen:**
- Das System im Labor ist das in [KA] beschriebene PSV-QTec-3D-H mit dem Data Management System PSV-W-600 oder -610. Die Kurzanleitung beschreibt beide Varianten; welche im Labor steht, ist nicht belegt.
- Die PSV-Version liegt bei 10.x (Folie 10.2.1.1, Handbuch 10.1).
- Mit „COM-Schnittstelle“ in der Aufgabenstellung ist das Component Object Model gemeint (Polytec-Doku), nicht die serielle Schnittstelle.

**Rückfragen:**
- [blockierend für Architekturentscheidungen] Darf auf dem PSV-Messrechner Python 3.11 samt uv und pywin32/comtypes installiert werden? [KA] 1-4 verlangt bei Fremdsoftware Rücksprache mit Polytec. *Auswirkung:* entscheidet zwischen lokaler Ausführung, DCOM oder einem anderen Rechner und damit ADR 1/8.
- [blockierend für Planung des Datenpfads] Welche Software-Optionen sind lizenziert (Hilfe > PSV Info > Optionen, [HB] 2-27): TDD (Zeitdaten), Signalgenerator, ExpME, ExpASAM, PCA? Gibt es eine Automatisierungsbeschränkung? Und welche PSV-Version ist installiert, 32 oder 64 Bit? *Auswirkung:* bestimmt, ob Zeitdaten und eigene FFT/H1 möglich sind und welche Exportwege es gibt.
- [nicht blockierend] Ist Polytec File Access auf dem Laborrechner installiert, und können wir eine eigene Kopie für einen Auswerte-PC bekommen (kein Dongle nötig, [PFA-M] Folie 2)? *Annahme bis zur Klärung:* `.svd` ist nur unter Windows lesbar; für die Cloud wird ein UFF- oder Simulatorpfad geplant.
- [nicht blockierend] Kann der Betreuer (DAL) `SettingsandScan.bas` und weitere vorhandene Makros sowie eine kleine Referenz-`.svd` mit UFF-Export bereitstellen? *Annahme:* Bis dahin gibt es keine realen Golden-Files.
- [nicht blockierend] Zugang zum Laborrechner: Fernzugriff oder nur vor Ort? Sollen Geometrie und 3D-Abgleich weiterhin interaktiv in PSV vorbereitet und als `.set` gespeichert werden? *Annahme:* ja; das Paket automatisiert Parameter, Scan, Speichern und Auswertung.
- [nicht blockierend] Soll der Funktionsgenerator (Anregung) per Software gesteuert werden („Versuchsequipment“ in der Ausschreibung)?

**Vorschlag für KONVENTIONEN.md:**
- „Daten aus Polytec-Schnittstellen werden an der Adaptergrenze nach float64 gewandelt, Phasen in rad (`ptcDisplayMagPhaseRad` bzw. Real/Imag), Punktindizes intern 0-basiert; die Umrechnung von bzw. zu den 1-basierten Polytec-Indizes erfolgt nur im Adapter.“
- „Der Begriff COM bezeichnet im Projekt das Component Object Model; serielle Ports heißen ‚serielle Schnittstelle‘.“

**Empfehlung nächster Schritt:**
- Die Rückfragen an Nutzer bzw. Betreuer klären.
- Danach `/anforderungs-analyst` mit diesem Bericht als Quelle und ADRs 1, 3 und 4 zur Entscheidung vorlegen.
- Dann ein Planungspaket für Schnittstelle und Simulator. Den analytischen Referenzfall für die Simulatordaten liefert der `strukturdynamik-experte` (Ablauf E).

**Review-Empfehlung:** Ein Code-Review ist nicht nötig, weil kein Code geändert wurde. Sinnvoll wäre eine fachliche Stichprobe der FRF- und 3D-Aussagen (Abschnitt 4) durch den `strukturdynamik-experte`.