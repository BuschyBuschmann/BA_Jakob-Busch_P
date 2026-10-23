<!-- Referenzdokument I5: COM-Automatisierungsschnittstelle der Polytec-PSV-Software und Polytec File Access; erstellt im Paket I5 von software-engineer; vertieft Analysebericht I1. Stand 2026-10-23. -->

# Referenz: COM-Schnittstelle der PSV-Software und Polytec File Access

> **Überarbeitet am 2026-10-23 nach Fachprüfung I5-F** (`2026-10-23_I5F_fachpruefung-com-referenz.md`,
> Korrekturpaket K1): M1 Frequenzachse bei Von/Bis (2.5, 4.4); M2 Skalierung und Phasenbezug (4.4);
> M3 Metadaten-Ergänzungsliste und Ersatz der Aussage zur vollständigen Dokumentation (6);
> M4 Machbarkeitstabelle und Voraussetzungen für U6 (9, 9.1); m1–m12 an den jeweiligen Stellen
> (2.5, 4.3, 4.4, 6); neue Prüfpunkte für den Messrechner (10). Die
> Polytec-Konventionen in `KONVENTIONEN.md` (Frequenzachse aus `XAxis`, Spektrenskalierung und
> Phasengültigkeit, getrennte Vorzeichenregel) sind berücksichtigt. Neu belegte Aussagen sind mit
> „(I5-F)“ gekennzeichnet, wenn der Beleg aus der Fachprüfung übernommen und nicht selbst
> nachgeprüft wurde; stichprobenartig nachgeprüft sind die Aussagen zu Von/Bis ([HB] 7-16/7-17),
> Frame-Semantik, `WindowFunctionParams` (read-only), `BurstStart` (Long) / `BurstStartEx`
> (Double), `PhaseFromRef`, `SaveTimeDataForScan`, Overrange-Mittelung ([HB] 7-6), IEPE/Inv.
> ([HB] 7-11/7-12).

**Zweck.** Dieses Dokument ist die Arbeitsgrundlage für Anforderungen, Architektur und
Umsetzung des Python-3.11-Pakets, das den Messablauf eines PSV-QTec-3D automatisiert.
Es soll ohne die CHM-Dateien nutzbar sein. Es vertieft den Analysebericht I1
(`2026-10-23_I1_com-schnittstelle-software.md`) und wiederholt dessen Inhalt nur, wo er für
die Vollständigkeit nötig ist.

**Kennzeichnung.**
- Jede API-Aussage trägt einen Beleg in eckigen Klammern (Kürzel siehe Abschnitt 11).
- **[ungeprüft]** heißt: Das Verhalten ist aus der Doku abgeleitet oder stammt aus
  allgemeinem Wissen über pywin32 bzw. COM. Am Messrechner ist es noch nicht bestätigt.
  Python, Bitness und Threading gehören immer dazu.
- **[Einschätzung]** heißt: eigene Folgerung ohne direkte Fundstelle.
- **[offen]** heißt: Die Doku sagt dazu nichts oder widerspricht sich.
- Alle Belege stammen aus den Quellen unter `Input/literatur/polytec/`. In der Cloud wurde
  nichts gegen eine echte PSV-Installation ausgeführt (kein Windows, keine PSV-Software).

**Belegformat.** `[BEM] PSV~Acquisition~ScanEx` bezeichnet das CHM-Thema
`PSV~Acquisition~ScanEx.html` im Basic Engine Manual. Die Textfassung steht in
`in_progress/analysen/polytec-chm-text/basic-engine-manual/PSV/Acquisition.md`: Ordner =
Bibliothek, Datei = Objekt. Dort ist jedes Thema mit seinem Dateinamen überschrieben.
`[PFA] …` verweist entsprechend auf `polytec-file-access/`.

---

## Inhalt

1. Architektur des Objektmodells
2. Datenerfassung (Acquisition, Settings, Properties, Infos)
3. Ablaufsequenzen
4. Auswertung und Dateizugriff (PolyFile, Presentation, Export)
5. Meldungen, Fehler, Events, Timeouts, Nebenläufigkeit
6. Reproduzierbarkeits-Metadaten
7. Zugriff aus Python 3.11 (pywin32)
8. Enum-Referenz
9. Abgleich mit dem Erwartungsmanagement (U1–U7)
10. Prüfliste für den Messrechner
11. Quellenverzeichnis

---

## 1 Architektur des Objektmodells

### 1.1 Grundprinzip

- Die PSV-Software ist ein **Automation-Server**. Andere Programme steuern sie als
  Automation-Controller über COM (ActiveX/OLE Automation). PSV kann über sein eingebautes
  Basic (WinWrap Basic) auch selbst Controller sein ([BEM] Controlling an Object Model).
- Polytec File Access (PFA) ist eine Sammlung von COM-Objekten. Sie liest und schreibt
  PSV-, MPV- und VibSoft-Mess- und Einstellungsdateien. Da COM ein Binärstandard ist,
  funktioniert jede COM-fähige Sprache ([PFA] Overview).
- Der Zugriff folgt der Objekthierarchie mit dem Punktoperator. Die Doku warnt davor,
  sich auf das „aktive“ Dokument zu verlassen; Objekte sollen explizit referenziert
  werden ([BEM] Controlling an Object Model).

### 1.2 Typbibliotheken

Das Objektmodell ist auf mehrere Typbibliotheken verteilt. Entwicklungsumgebungen binden
abhängige Bibliotheken meist automatisch ein, sonst sind die Verweise von Hand zu setzen
([PFA] Model Overview; [COM] Folie 8).

| Typbibliothek (Ordner der Textfassung) | Inhalt (relevant für uns) | Beleg |
|---|---|---|
| `PSV` (Polytec PSV Type Library) | Application, AcquisitionInstance, PresentationInstance, Acquisition, Settings, Acquisition-Properties, InfosAcq, Exporter, Documents/Windows, Enums des Ablaufs | [BEM] PSV_P |
| `PolyAcquisitionLib` | AcquisitionPointData(Stream), Live-Daten während der Erfassung | [BEM] PolyAcquisitionLib_P |
| `POLYFILELib` (PolyFile) | PolyFile, Infos, MeasPoints, Elements, Domains, DataPoint, Version, SummaryInfo | [BEM]/[PFA] POLYFILELib_P |
| `POLYPROPERTIESLib` | *Container der Acquisition-Properties in Dateien, Validatoren, Enums (Modi, Mittelung, Kanaltyp) | [BEM] POLYPROPERTIESLib_P |
| `POLYSIGNALLib` | Domain/Channel/Signal/Display, SignalDescription, Enums (Display, Domain, BuildFlags, InfoType, PhysicalQuantity) | [BEM] POLYSIGNALLib_P |
| `POLYWAVEFORMSLib` | Generator-Signalformen (Sinus, Sweep, Chirp, Rauschen …) | [BEM] POLYWAVEFORMSLib_P |
| `POLYALIGNMENTLib` | 2D-/3D-/Kamera-Abgleich mit Qualitätsgrößen | [BEM] POLYALIGNMENTLib_P |
| `PolyScanHeadLib` | Scankopf, Fokus, Scanner, IComTask (asynchrone Aufgaben) | [BEM] PolyScanHeadLib_P |
| `PolyFrontEndLib` | Frontend, Kanäle, Erfassungskarten-Enums | [BEM] PolyFrontEndLib_P |
| `Polytec_IO_VibInterfaces` | Vibrometer-Controller, Sensorköpfe, Messbereiche, Filter | [BEM] Polytec_IO_VibInterfaces_P |
| `PolyBandsLib`, `POLYDIGITALFILTERSLib`, `PolyMathLib`, `PolyScopeLib`, `POLYSIGNALGENERATORLib` | Bänder, digitale Filter, Fensterfunktionen, Trigger-Enums, Generator-Enums | jeweilige `_P`-Seite |

- Dateinamen, GUIDs und Versionen der Typbibliotheken nennt die Doku nicht; die
  „References“-Seiten sind leer ([BEM] PSV_references). **[offen]**
- Das C++-Beispiel nennt als Include-Pfade der installierten Komponenten
  `%CommonProgramFiles%\Polytec\COM`, `%CommonProgramFiles%\Polytec\PDx` und eine
  .NET-Assembly `Polytec.IO.Vibrometer` im GAC ([PFA] Examples, CplxPointAvg). Daraus folgt
  **[Einschätzung]**: `Polytec_IO_VibInterfaces` ist eine COM-sichtbare .NET-Bibliothek.
- Im C#-Beispiel heißt der Interop-Namensraum `Polytec.Interop.Psv` ([COM] Folie 12).

### 1.3 Einstiegsobjekte und ProgIDs

| Einstieg | ProgID (belegt) | Zweck | Beleg |
|---|---|---|---|
| `AcquisitionInstance` | `"PSV.AcquisitionInstance"` | PSV-Instanz im Datenerfassungsmodus; Methode `GetApplication(vbCreate, lTimeOut=10000)` → `IApplication5`; Property `IsRunning` | [BEM] PSV~AcquisitionInstance, ~GetApplication, ~IsRunning |
| `PresentationInstance` | `"PSV.PresentationInstance"` | PSV-Instanz im Auswertemodus; gleiche Mitglieder | [BEM] PSV~PresentationInstance, ~GetApplication |
| `Application` | `"PSV.Application"` (bzw. `"VibSoft.Application"`) | Anwendung; Wurzel des PSV-Objektmodells | [BEM] PSV~Application; [COM] Folie 6 |
| `PolyFile` | `"PolyFile.PolyFile"` | Datei öffnen, lesen, schreiben; Einstieg in PFA | [BEM] POLYFILELib~PolyFile; [PFA] Type Libraries Overview; [PFA-M] Folie 4 (`actxserver('PolyFile.PolyFile')`) |
| Signalformen | `"PolyWaveforms.WaveformSine"`, `…Sweep`, `…PeriodicChirp`, `…BurstChirp`, `…BurstRandom`, `…PseudoRandom`, `…WhiteNoise`, `…Square`, `…Triangle`, `…Ramp`, `…SteppedSineSweep`, `…MultiCarrierCW`, `…UserDefined` | Generator-Signalform erzeugen und zuweisen | [BEM] POLYWAVEFORMSLib~Waveform* |
| `PTCTimer` | `"Psv.PTCTimer"` | Periodischer Timer (Event `Timer`, `Interval` in ms) | [BEM] PSV~PTCTimer |
| `CameraSize`, `LensCalibrations` | `"PolyFile.CameraSize"`, `"PolyFile.LensCalibrations"` | (für uns nicht relevant) | [BEM] POLYFILELib~CameraSize |

Weitere Objekte erzeugen die Beispiele mit `New`, ohne dass die Doku eine ProgID nennt:
`ExportParameters` ([BEM] PSV~Exporter, Beispiel), `SignalDescription` ([BEM] Access to
Data), `DigitalFilterLowpass`/`DigitalFilterNone` ([BEM]
POLYPROPERTIESLib~ChannelAcqPropertiesContainer, Beispiel). Ob und wie diese Objekte aus
Python erzeugt werden können, ist **[ungeprüft]** (siehe 7.3).

Wichtige Randbedingungen:
- `AcquisitionInstance` gibt es nicht für VibSoft und nicht für die
  **Desktop-Versionen** von PSV ([BEM] PSV~AcquisitionInstance).
- Aus der Presentation-Instanz oder aus einem externen Client läuft die Kommunikation mit
  der Acquisition-Instanz über Interprozesskommunikation (DCOM), auch lokal
  ([BEM] PSV~AcquisitionInstance~GetApplication). Für einen fremden Rechner sind ein
  Serverparameter und „sehr viele aufwendige Sicherheitseinstellungen“ nötig
  ([COM] Folie 13).
- Das Acquisition-Objekt steht nur zur Verfügung, wenn PSV im Datenerfassungsmodus ist
  ([BEM] Access to General Information).
- Der Bemerkungstext zu `PresentationInstance.GetApplication` spricht ebenfalls von der
  „acquisition instance“. Das ist vermutlich ein Kopierfehler der Doku
  ([BEM] PSV~PresentationInstance~GetApplication). **[offen]**

### 1.4 Hierarchie (Auszug, nur für uns relevante Zweige)

```
AcquisitionInstance ("PSV.AcquisitionInstance")
└─ GetApplication(vbCreate, lTimeOut) → IApplication5 (Application)
   ├─ Version, Mode, Visible, WarningLevel, SuppressMessagesForAutomation, MessagesLoggingEnabled
   ├─ Events: MessageOccurred(Style, Text, ByRef Answer), Quit, QuitEx(ByRef stopQuitting)
   ├─ Settings ─ Load(datei, PTCSettings) · Save(datei) · Delete(datei)
   ├─ Exporter(eingabedatei, PTCExportType) → Exporter      (nur Default-Interface, nicht IApplication5)
   ├─ Documents ─ Open(datei) → Document/VibDocument ─ Close, Save, SaveAs, Exporter(typ), AcquisitionProperties
   ├─ DigitalPorts(PTCDigitalPort) → DigitalPort ─ Value, Pulse
   └─ Acquisition
      ├─ Mode (PTCAcqMode, rw) · State (PTCAcqState, r) · ScanFileName (rw) · ScanCaps · GeneratorsOn (rw)
      ├─ Start(PTCAcqStartMode) · Stop() · Scan(PTCScanMode) · ScanEx(PTCScanMode, PTCScanCaps)
      ├─ SetLaserOn/GetLaserOn · AutoFocusLaser · AssignFocusAutomatically · GeometryScan
      ├─ Get/SetSelectedMeasPoints · GetSignalAmplitudes · ExportVideoSnapshot(Ex)
      ├─ Events: AcqStateChanged(PTCAcqState) · ScanStateChanged(PTCScanState, ScanPoint)
      ├─ ActiveProperties → AcquisitionProperties (IAcquisitionProperties3, typisierte Collection)
      │  ├─ GeneralProperties · AverageProperties · FftProperties · TimeProperties · ZoomFftProperties
      │  ├─ ChannelsProperties(i) → ChannelAcqProperties
      │  ├─ VibrometersProperties(i) → VibrometerAcqProperties ─ VibControllerSettings
      │  ├─ GeneratorsProperties(i) → GeneratorAcqProperties ─ Waveform (IWaveform)
      │  ├─ TriggerProperties · SignalEnhancementProperties · FrontEndProperties
      │  └─ MultiFrameProperties · FastScansProperties
      ├─ ModeProperties(PTCAcqMode) → AcquisitionProperties je Messmodus
      ├─ Infos → InfosAcq (IInfos8, benannt+typisiert)
      │  ├─ Hardware (HardwareAcq) · Vibrometers (VibrometerGroups) · ScanHeadDevicesInfo
      │  ├─ MeasPoints (IMeasPoints11) · Elements · MeasurementLocations · Alignments (AlignmentsAcq)
      │  └─ PositionDevice · Textures
      ├─ PointDomains → Domains → Channels → Signals → Displays (Live-Daten)
      └─ GetData(Display) → AcquisitionPointData ─ OpenDataStream(block, frame) → Read(...)

PolyFile ("PolyFile.PolyFile")
├─ Open(pfad) · Close() · ReadOnly (rw) · IsOpen · Create(pfad, flags) · Save() · SaveAs(...)
├─ Version (FileID, FileTime, ProgramVersionString …) · SummaryInfo (Title, Author, Subject, Comments)
├─ Infos (benannt+typisiert)
│  ├─ AcquisitionInfoModes ─ ActiveMode · ActiveProperties → AcquisitionPropertiesContainer
│  ├─ Hardware · MeasPoints (MeasPoint …) · Elements · Alignments · ScanHeadDevicesInfo · VideoBitmap
├─ GetPointDomains(BuildFlags) → PointDomains → PointDomain
│  ├─ Channels("Vib") → Signals("Velocity") → Displays("Real & Imag.") → Display
│  ├─ DataPoints(i) → DataPoint ─ GetData(Display, Frame) · Get3DData · GetScanStatus · MeasPoint
│  └─ GetXAxis(Display) → XAxis (Min, Max, MaxCount, Unit, GetMidX(i)) · GetYAxes(Display)
├─ GetPointAverageDomains(...) → PointAverageDomain ─ GetData(Display, Frame)
├─ GetBandDomains(...) → BandDomain ─ GetDataBands(Signal) → DataBand ─ GetData
└─ ContainedFiles (kombinierte Dateien)
```

Belege: [BEM] PSV~Application_members, PSV~Acquisition_members,
PSV~AcquisitionProperties_members, PSV~InfosAcq_members, POLYFILELib~PolyFile_members,
Access to Data, Using Collections.

### 1.5 Interfaces, Versionierung und Casting

- Jedes Objekt besteht aus einem oder mehreren Interfaces. Standardmäßig liefert es das
  **Default-Interface**, meist das neueste ([BEM] Access to Interfaces).
- Polytec ändert bestehende Interfaces nicht, sondern legt neue Versionen an (z. B.
  `IPolyFile8` bleibt stabil). Neue Versionen werden zum Default. Wer mit
  Default-Interfaces arbeitet, bekommt neue Mitglieder automatisch ([BEM] Access to Interfaces).
- Methoden und Properties liefern teilweise **ältere Interface-Versionen**. In der Doku
  erkennt man das am führenden „I“, z. B. `GetApplication → IApplication5`,
  `Acquisition.ActiveProperties → IAcquisitionProperties3`, `Infos → IInfos8`. Polytec
  empfiehlt, dann auf das Default-Interface zu casten ([BEM] Access to Interfaces).
- **Für uns wichtig:** `IApplication5` enthält **kein** `Exporter`; das
  Default-Interface `Application` hat es ([BEM] PSV~IApplication5_members gegenüber
  PSV~Application_members). Wer den Exporter über das Ergebnis von `GetApplication`
  nutzen will, muss casten. Wie das in pywin32 geht, ist **[ungeprüft]** (siehe 7.3).
- Gemeinsame Interfaces: `IWaveform` ist die Basis aller Signalformen. `Waveform`
  liefert und akzeptiert `IWaveform`; für die Parameter muss auf das konkrete Objekt
  gecastet werden ([BEM] Access to Interfaces; POLYWAVEFORMSLib~IWaveform;
  PSV~GeneratorAcqProperties~Waveform).
- Polytec empfiehlt **Early Binding** in allen Fällen. Late Binding ist möglich
  ([BEM] Access to Interfaces; Using Object Variables).

### 1.6 Collections

Es gibt vier Arten von Collections ([BEM] Using Collections):

| Art | Zugriff | Index | Beispiele |
|---|---|---|---|
| Standard | `Item(Long)`, `Count`, `For Each` | **1-basiert** | Elements, MeasPoints, DataPoints, Documents |
| Typisiert | `Item(Enum)`; fehlende Elemente liefern `Nothing`; `Count` zählt auch fehlende | Enum | AcquisitionProperties, AcquisitionInfoModes, DigitalPorts |
| Benannt | `Item(Long oder String)`, `Exists(String)`, `Count` | 1-basiert bzw. Name | Channels, Signals, DataBands |
| Benannt und typisiert | zusätzlich `Type(Enum)`, `Exists(Enum oder String)` | 1-basiert, Name oder Enum | Infos, Displays, PointDomains |

- Namen sind sprachabhängig. `Item` und `Exists` akzeptieren aber deutsche und englische
  Namen, z. B. „Geschwindigkeit“/„Velocity“ und „Zeit“/„Time“ ([BEM] Using Collections).
- Ausnahmen von der 1-Basierung: Bei `Vibrometers(i)` beginnt der Index bei 1, bei
  `Controllers(i)` und `SensorHeads(i)` bei 0 ([BEM] Access to General Information).
  `SensorHeadSettingsCollection(0)` wird ebenfalls 0-basiert benutzt ([BEM]
  Polytec_IO_VibInterfaces~SensorHeadSettings, Beispiel).
- 1-basiert benutzt werden auch `ChannelsProperties(1)` ([BEM]
  POLYPROPERTIESLib~ChannelAcqPropertiesContainer, Beispiel), `GeneratorsProperties(1)`
  ([BEM] POLYPROPERTIESLib~GeneratorAcqPropertiesContainer, Beispiel) und
  `VibrometersAcqProperties` („1-based index“, [BEM] PSV~VibrometersAcqProperties~Item).
  Für `ChannelsAcqProperties.Item` steht die Basis nicht ausdrücklich in der Doku. **[offen]**
- Bei `Elements`, `MeasPoints` und `Alignments3D` nennt die Doku die Indexbasis ebenfalls
  nicht ausdrücklich. Es gilt die Regel „Standard-Collection = 1-basiert“ ([BEM] Using
  Collections).
- Arrays, die als Rückgabewerte geliefert werden (`GetData`, `CoordinatesToArray`,
  `SensorHeadNames` …), sind **0-basiert** ([BEM] POLYFILELib~DataPoint~GetData;
  POLYFILELib~MeasPoints~CoordinatesToArray; PSV~HardwareAcq~SensorHeadNames).

### 1.7 Index und Label von Scanpunkten (Begriffsfalle)

- In der Oberfläche der PSV-Software heißen **Labels „Index“** und **Indizes „Nummer“**
  ([BEM] POLYFILELib~Elements~Add, Remarks).
- `MeasPoint.Index` ist die Position in der MeasPoints-Collection. `MeasPoint.Label` ist
  die in PSV angezeigte Punktnummer; sie ist les- und schreibbar
  ([BEM] POLYFILELib~MeasPoint~Index, ~Label). Umrechnen mit
  `MeasPoints.LabelToIndex(label)` ([BEM] POLYFILELib~MeasPoints~LabelToIndex).
- Die Matlab-Beispiele arbeiten mit dem ursprünglichen Index. Vorsicht bei in PSV
  geänderten Punkt-Indizes ([PFA-M] Folie 6).
- Für `ScanStateChanged(…, ScanPoint)` („1-based index of the current scan point“,
  [BEM] PSV~Acquisition~ScanStateChanged_EV) und für
  `ChannelAcqProperties.ReferencePointIndex` („one-based scan point index“,
  [BEM] PSV~ChannelAcqProperties~ReferencePointIndex) ist nicht klar, ob Index oder
  Label gemeint ist. **[offen]**, Prüfpunkt P2-6.
- **Konsequenz für den Adapter [Einschätzung]:** Intern 0-basiert (KONVENTIONEN), dazu
  immer sowohl `index` (COM, 1-basiert) als auch `label` mitführen.

---

## 2 Datenerfassung

### 2.1 Acquisition: Methoden

| Mitglied | Signatur (VB) | Bedeutung, Randbedingungen | Beleg |
|---|---|---|---|
| `Start` | `Start(StartMode As PTCAcqStartMode)` | Einpunktmessung; `ptcAcqStartSingle`=0, `ptcAcqStartContinuous`=1 | [BEM] PSV~Acquisition~Start; PSV~PTCAcqStartMode |
| `Stop` | `Stop()` | stoppt jede Messung (auch Scan) | [BEM] PSV~Acquisition~Stop |
| `Scan` | `Scan(ScanMode As PTCScanMode)` | Scan starten; nur PSV | [BEM] PSV~Acquisition~Scan |
| `ScanEx` | `ScanEx(ScanMode As PTCScanMode, ScanCaps As PTCScanCaps)` | Scan mit Zusatzoptionen (Fokus, VideoTriangulation, asynchrone Events) | [BEM] PSV~Acquisition~ScanEx |
| `GetData` | `GetData(pIDisplay As IDisplay2) As IPointData` | Live-Daten zum aktuellen Punkt; Freigabe vor neuer Erfassung nötig (Kommentar im Beispiel) | [BEM] PSV~Acquisition~GetData |
| `SetLaserOn` | `SetLaserOn(scanHeadIndex As Long, laserOn As Boolean, moveLaser As Boolean)` | Index 1 = oben, 2 = links, 3 = rechts, −1 = alle | [BEM] PSV~Acquisition~SetLaserOn |
| `GetLaserOn` | `GetLaserOn(scanHeadIndex As Long) As Boolean` | −1: True nur, wenn alle an | [BEM] PSV~Acquisition~GetLaserOn |
| `AutoFocusLaser` | `AutoFocusLaser(scanHeadIndex As Long, fullRange As Boolean) As Boolean` | Index 1-basiert, −1 = alle | [BEM] PSV~Acquisition~AutoFocusLaser |
| `AssignFocusAutomatically` | `AssignFocusAutomatically(caps As PTCAssignFocusAutomaticallyCaps)` | Fokuswerte für alle bzw. ausgewählte Punkte bestimmen und mit der Geometrie speichern | [BEM] PSV~Acquisition~AssignFocusAutomatically |
| `CalculateFocusValues` | `CalculateFocusValues(laserPositions() As Double, scanHeadIndex() As Long) As Long()` | Positionen als xyz-Tripel **in Meter**; Scankopf-Indizes hier **0-basiert** | [BEM] PSV~Acquisition~CalculateFocusValues |
| `GeometryScan` | `GeometryScan(caps As PTCGeometryScanCaps)` | Geometrie-Laser misst die Entfernung zu jedem Punkt, daraus x, y, z | [BEM] PSV~Acquisition~GeometryScan |
| `GetSelectedMeasPoints` / `SetSelectedMeasPoints` | `(Optional labels As Boolean = True)` | Auswahl in der Datenerfassung; bei einem Punkt fährt der Laser dorthin, nicht während einer Messung | [BEM] PSV~Acquisition~GetSelectedMeasPoints, ~SetSelectedMeasPoints |
| `GetSignalAmplitudes` | `GetSignalAmplitudes(channelIndices() As Long) As Double()` | Signalamplitude in **% des Maximalpegels**; Kanalindizes 1-basiert; leeres Array = alle; Vib3D liefert Top, Left, Right | [BEM] PSV~Acquisition~GetSignalAmplitudes |
| `ExportVideoSnapshot(Ex)` | `(bstrFileName [, snapshotType])` | Videobild als bmp/jpg/tif/png/gif | [BEM] PSV~Acquisition~ExportVideoSnapshot, ~ExportVideoSnapshotEx |
| `FindPointMarkers`/`MatchPointMarkers`, `TakeReferenceSnapshot` … | – | Bewegungskompensation per Marker bzw. Mustervergleich | [BEM] PSV~Acquisition~MatchPointMarkers |
| `MeasurePathLength`, `PathLengthScan` | – | nur MSA-650, für uns irrelevant | [BEM] PSV~Acquisition~MeasurePathLength |

### 2.2 Acquisition: Properties und Events

| Mitglied | Typ, Zugriff | Bedeutung | Beleg |
|---|---|---|---|
| `Mode` | `PTCAcqMode`, rw | aktiver Messmodus (Time 0, FFT 1, ZoomFFT 2, MultiFrame 3, FastScan 4, …) | [BEM] PSV~Acquisition~Mode; POLYPROPERTIESLib~PTCAcqMode |
| `State` | `PTCAcqState`, r | Zustand (Stopped 0 … PathLength 7) | [BEM] PSV~Acquisition~State |
| `ScanFileName` | String, rw | Zieldatei des Scans; **leer = PSV fragt per Dialog** | [BEM] PSV~Acquisition~ScanFileName |
| `ScanCaps` | `PTCScanCaps`, r | verfügbare Scan-Optionen für `ScanEx` | [BEM] PSV~Acquisition~ScanCaps |
| `GeneratorsOn` | Boolean, rw | Signalgeneratoren an/aus; es wird derzeit nur ein Generator unterstützt | [BEM] PSV~Acquisition~GeneratorsOn |
| `ActiveProperties` | `IAcquisitionProperties3`, r | Properties des aktiven Modus | [BEM] PSV~Acquisition~ActiveProperties |
| `ModeProperties` | `AcqModeProperties`, r | Properties je Modus, `Item(PTCAcqMode)` | [BEM] PSV~Acquisition~ModeProperties; PSV~AcqModeProperties~Item |
| `Infos` | `IInfos8`, r | InfosAcq (Hardware, Vibrometer, Punkte, Abgleich) | [BEM] PSV~Acquisition~Infos |
| `PointDomains` | `IDomains2`, r | Auswahl Domain/Kanal/Signal/Display für `GetData` | [BEM] PSV~Acquisition~PointDomains |
| `Document` | `VibDocument`, r | das Erfassungsdokument | [BEM] PSV~Acquisition~Document |
| `AvailableSnapshotTypes` | `PTCSnapshotType()`, r | verfügbare Kamerabilder | [BEM] PSV~Acquisition~AvailableSnapshotTypes |
| Event `AcqStateChanged` | `(AcqState As PTCAcqState)` | Zustandswechsel | [BEM] PSV~Acquisition~AcqStateChanged_EV |
| Event `ScanStateChanged` | `(ScanState As PTCScanState, ScanPoint As Long)` | BeginScan(0) → je Punkt BeginScanPoint(n)/EndScanPoint(n) → EndScan(0) | [BEM] PSV~Acquisition~ScanStateChanged_EV |

Zur Event-Folge ([BEM] PSV~Acquisition~ScanStateChanged_EV):
- Die Reihenfolge der Punkte bestimmen die Geometrie und die Voreinstellung zur
  Scanrichtung. Im Beispiel mit neun Punkten lautet sie 3, 2, 1, 4, 5, 6, 9, 8, 7.
- Bei PSV-500-H/-NB/-3D-H ohne VideoTriangulation kommt `BeginScanPoint` *vor* der
  Spiegelbewegung. Ob das beim PSV-QTec-3D genauso ist, ist **[offen]**.
- Laut Handbuch fährt die Software je Scanpunkt: Laser positionieren, Fokus einstellen
  (nur mit Option APS Professional), Einschwingzeit abwarten, Einzelmessung,
  Status zuweisen, speichern ([HB] 8-2, PDF 248).

### 2.3 Messmodi und Zustände

- Verfügbare Modi beim PSV-1D/3D: FFT und FastScan Standard (FastScan beim PSV-B
  optional), Zeit und MultiFrame optional ([HB] 7-3, PDF 211).
- Der Messmodus Zeit speichert für Scans Zeitsignale statt Spektren und braucht die
  **Option TDD** ([HB] 7-2, 7-34; PDF 210, 242).
- Zustände und Modi stehen als Tabelle in Abschnitt 8.
- `Application.Mode` (`PTCApplicationMode`: Normal 0, Acquisition 1, Presentation 2) ist
  rw und nur für PSV relevant ([BEM] PSV~Application~Mode; PSV~PTCApplicationMode).

### 2.4 Settings (Einstellungen laden und speichern)

| Mitglied | Signatur | Bedeutung | Beleg |
|---|---|---|---|
| `Settings.Load` | `Load(bstrFileName As String, PTCSettings As PTCSettings)` | Teile einer `.set`-Datei **oder einer Messdatei** laden | [BEM] PSV~Settings~Load |
| `Settings.Save` | `Save(bstrFileName As String)` | aktuelle Einstellungen speichern | [BEM] PSV~Settings~Save |
| `Settings.Delete` | `Delete(bstrFileName As String)` | Einstellungsdatei löschen | [BEM] PSV~Settings~Delete |

`PTCSettings` (Bitmaske, [BEM] PSV~PTCSettings): None 0, Acquisition 2, Alignment 4,
Camera 64, CameraAndAlignment 68, Windows 128, APS (Scanpunkt-Definition) 312,
2DAlignment 512, 3DAlignment 1024, All 65535.

Aus dem Handbuch ([HB] 10-4, 10-10; PDF 316, 322):
- Eine `.set`-Datei enthält Erfassungsparameter, Scanpunkte, 2D-/3D-Abgleich,
  Optik (Zoom, Fokus) und Fensteranordnung, aber **keine Frequenzbänder**.
- Aus Scandateien lassen sich auch Bänder laden, aber keine Fensteranordnung.
- Erfassungsparameter lassen sich nur bei **gleicher Erfassungskarte und Anschlussbox**
  laden.
- Bei Problemen meldet PSV, welche Teile nicht geladen wurden; der Rest wird geladen.
  Bei Automatisierung kommt diese Meldung als Event bzw. wird unterdrückt (siehe 5.1).
  **[ungeprüft]**, ob dabei eine Exception entsteht.
- Die Standard-Einstellungsdateien der Software liegen unter
  `C:\Users\<Konto>\AppData\Local\Polytec\PSV\<Version>\` (`<FrontEnd>_Ch<n>.set`,
  `AcquisitionSettings.set`) ([HB] 2-4, PDF 20).

**Was per COM, was nur per `.set`?** Belegte Lage:

| Bereich | per COM lesbar | per COM schreibbar | nur über `.set`/GUI |
|---|---|---|---|
| Messmodus, FFT/Zeit/Zoom-FFT, Mittelung, Allgemein, Trigger, SE, Kanäle, Generator | ja (2.5) | ja, meist rw (2.5) | – |
| Vibrometer-Messbereich, Filter | ja (`VibControllerSettings`, Controller-Objekte) | `QuantitySettings.Range` ist rw; ob das in der Erfassung wirkt: **[ungeprüft]** | – |
| Scanpunkte (Gitter) | ja (`Infos.MeasPoints`, Koordinaten, Status) | **[offen]**: `MeasPoints.Add`/`SetCoordXYZ` sind nur für Dateien belegt; `SetCoordXYZ` nur für Einstellungsdateien im APS-Punktmodus ([BEM] POLYFILELib~MeasPoint~SetCoordXYZ) | Definition in der GUI, laden per `Settings.Load(…, ptcSettingsAPS)` |
| 2D-/3D-Abgleich | ja (`Infos.Alignments`, Qualität) | theoretisch `Alignment3D.Calculate(...)` ([BEM] POLYALIGNMENTLib~Alignment3D~Calculate), praktisch aufwendig | interaktiv, laden per `ptcSettings3DAlignment` |
| Fokuswerte | ja (`MeasPoint.FocusValues`) | `AssignFocusAutomatically`, `AutoFocusLaser`; `FocusValues` setzen nur in `.set` ([BEM] POLYFILELib~MeasPoint~FocusValues) | – |
| Frequenzbänder | in Dateien (`BandDomains`) | `PolyFile.CalcBands` in Dateien | nicht in `.set` |
| Optik (Zoom, Kamera) | nicht untersucht | nicht untersucht | `ptcSettingsCamera` |

### 2.5 AcquisitionProperties-Gruppen

Die Collection `AcquisitionProperties` (typisiert) enthält je nach Messmodus andere Objekte.
Zugriff über `Item(PTCAcqPropertiesType)` oder die typisierten Properties mit `Has…`
([BEM] PSV~AcquisitionProperties_members, ~Item). Gruppen-Enum: General 0, Average 1,
Channels 2, FastScans 3, Fft 4, Generators 5, MultiFrame 6, SignalEnhancement 8, Time 9,
Trigger 10, Vibrometers 11, ZoomFft 12, FrontEnd 14 ([BEM] POLYPROPERTIESLib~PTCAcqPropertiesType).

**FFT** (`FftAcqProperties`, [BEM] PSV~FftAcqProperties_members und Einzelthemen)

| Property | Typ | Zugriff | Einheit, Bereich |
|---|---|---|---|
| `Bandwidth` | Double | rw | Hz |
| `StartFrequency` | Double | rw | „Von“ der GUI; Doku nennt keine Einheit („The start frequency of the FFT“); Hz [Einschätzung, analog `EndFrequency`]. Schränkt den ausgewerteten Bereich ein ([HB] 7-16/7-17) |
| `EndFrequency` | Double | rw | „Bis“ der GUI, Hz |
| `Lines` | Long | rw | Anzahl FFT-Linien im **Vollbereich** (Gesamtzahl); in der GUI bis 819 200 ([HB] 7-17, PDF 225). Bei eingeschränktem Von/Bis entspricht die angezeigte Linienzahl nur dem Bereich zwischen Von und Bis ([HB] 7-17), siehe 4.4 |
| `Overlap` | Long | rw | % ; nur bei Mittelung ohne Trigger wirksam ([HB] 7-17) |
| `SampleFrequency` | Double | rw | Hz; laut BEM rw, hängt aber von der Bandbreite ab (Gl. 7.1/7.2). Setzverhalten **[offen]** |
| `SampleResolution` | Double | r | Frequenzauflösung Δf in Hz |
| `Samples` | Long | rw | setzen nur im Modus MultiFrame |
| `SampleTime` | Double | r | Messzeit (s laut Zoom-FFT-Thema; hier ohne Einheit) |
| `FftAcqPropertiesValidator` | `FftAcqPropertiesValidator` | rw | siehe 2.6 |

Die Formeln für Abtastfrequenz, Messzeit und Auflösung stehen in [HB] 7-17 (Gl. 7.1–7.4).
Sie sind dort nur als Grafik enthalten und im Textauszug nicht lesbar; die Fachprüfung I5-F
hat sie als Bild der PDF-Seite 225 gelesen (I5-F):
- Abtastfrequenz $f_\mathrm{Abtast} = 2{,}5\cdot BW$ für alle Systeme außer den M-Systemen,
  $2{,}56\cdot BW$ für die M-Systeme (Gl. 7.1/7.2).
- Messzeit $t_\mathrm{Mess} = n_\mathrm{FFT}/BW$ (Gl. 7.3).
- Auflösung $\Delta f = 1/t_\mathrm{Mess} = BW/n_\mathrm{FFT}$ (Gl. 7.4).
- Prüfwerte (nachgerechnet in I5-F): $BW = 5000$ Hz, 400 Linien ergeben $\Delta f = 12{,}5$ Hz,
  $f_\mathrm{Abtast} = 12\,500$ Hz, $t_\mathrm{Mess} = 0{,}08$ s, $N = 1000$ Abtastwerte.
- Ob der PSV-QTec-3D(-H) als Nicht-M-System (2,5·BW) arbeitet, ist nur indirekt über die
  H-System-Zuordnung belegt **[ungeprüft]**; Gegenprobe am Gerät über `SampleFrequency` und
  `SampleResolution` (P1-11).
- $N = 2{,}5\cdot n_\mathrm{FFT}$ ist keine Zweierpotenz (TM 3-3) **[offen]**.
- **Sollwert-Strategie [Einschätzung]:** Nur `Bandwidth` und `Lines` (bzw. Von/Bis) setzen und die
  abgeleiteten Größen (`SampleFrequency`, `SampleResolution`, `SampleTime`) zurücklesen und gegen
  die Formeln prüfen. Die Werte liefert die Schnittstelle direkt.
- Bei **Zoom-FFT** gilt eine andere Frequenzachse (Mittenfrequenz `CenterFrequency`); die
  Formeln oben und die Achsenregel in 4.4 gelten nur für den Modus FFT (m4).

**Zeit** (`TimeAcqProperties`, [BEM] PSV~TimeAcqProperties_members): `SampleFrequency`
(Hz, rw), `Samples` (rw), `SampleResolution` (s, r), `SampleTime` (s, r),
`TimeAcqPropertiesValidator` (rw). Bis 64 Megasamples (67 108 864 Abtastpunkte);
Dateigröße > aktive Kanäle · Abtastpunkte · 4 Byte ([HB] 7-34, PDF 242).

**Zoom-FFT** (`ZoomFftAcqProperties`): `Bandwidth`, `CenterFrequency`, `Lines`, `Overlap`,
`SampleFrequency`, `Samples`, `SampleResolution`, `SampleTime` (s)
([BEM] PSV~ZoomFftAcqProperties_members).

**Mittelung** (`AverageAcqProperties`, [BEM] PSV~AverageAcqProperties~Count, ~Type)
- `Count` rw. Laut Doku liegen die erlaubten Werte zwischen 3 und 10000. Im FastScan
  sind höchstens 100 Mittelungen möglich, im Zeitmodus mit Signal Enhancement weniger.
  Das Handbuch nennt keine Untergrenze ([HB] 7-5). Ob Werte unter 3 abgewiesen werden,
  ist am Gerät zu prüfen. **[offen]**
- `Type` rw (`PTCAverageType`: Off 0, Magnitude 1, Complex 2, Time 3, Peakhold 4).
- `Magnitude` heißt in der GUI „Amplitude“ und ist die Betragsmittelung ohne Phase (I5-F).
- Fachliche Hinweise aus der GUI: Komplexmittelung bei Referenz oder Trigger bzw.
  deterministischer Anregung; Mittelung Zeit nur getriggert; Overrange-Spektren werden
  bei der Mittelung nicht berücksichtigt ([HB] 7-5/7-6, PDF 213/214). **Ausnahme** ([HB] 7-6):
  Haben alle bisher erfassten Spektren den Status Overrange, werden sie zunächst gemittelt
  und angezeigt. Beim ersten Spektrum ohne Overrange wird der Mittelungszähler zurückgesetzt
  und die bisherigen Overrange-Spektren werden verworfen. Überlappung wirkt nur ohne Trigger.

**Allgemein** (`GeneralAcqProperties`, [BEM] PSV~GeneralAcqProperties_members)

| Property | Zugriff | Bedeutung |
|---|---|---|
| `AutoRemeasure` | rw | automatisches Nachmessen nach dem Scan |
| `AutoRemeasureAutoRange` | rw | bei Overrange Vibrometerbereich anpassen; braucht `AutoRemeasure = True`; verwendeter Bereich je Punkt in `MeasPoint.VibrometerRange` |
| `IsAutoRemeasurePossible` | r | ob Nachmessen möglich ist |
| `SaveTimeDataForScan` | rw | Zeitdaten zusätzlich speichern (FFT, FastScan); setzt SE auf „Fast“. Ob diese Property wie der Messmodus Zeit die Option TDD voraussetzt, ist **[offen]** (Prüfpunkt P3-6) |
| `PrincipalComponentAnalysis` | rw | MIMO/PCA (Option PCA, [HB] 7-7) |
| `RealSampleFrequency` | rw | Roh-Abtastrate vor Dezimierung, Hz [Einschätzung] |
| `BandWidthExtension` | rw | nur UHF |

Reihenfolge beim automatischen Nachmessen: Nicht gemessen, Ungültig, VT fehlgeschlagen,
Overrange, bei aktivem SE auch Gültig ([HB] 7-6, PDF 214).

**Kanäle** (`ChannelsAcqProperties.Item(i)` → `IChannelAcqProperties8`,
[BEM] PSV~ChannelsAcqProperties~Item; PSV~ChannelAcqProperties_members)

| Property | Zugriff | Einheit/Bedeutung |
|---|---|---|
| `Active`, `Reference` | rw | Kanal aktiv; Kanal ist Referenz |
| `ReferencePointIndex` | rw | 1-basierter Scanpunkt der Referenz; laut BEM nur beim UFF-/ME'Scope-Export von FRF und CP benutzt. Für die Modalanalyse ist er die Bezugs-DOF der Anregung, zusammen mit `DirectionOfVibration` des Referenzkanals in die Metadaten aufnehmen (I5-F, Abschnitt 6) |
| `InputRange` | rw | **V** |
| `Calibration` | rw | Kalibrierfaktor in SI (Messwert je 1 V, [HB] 7-12). Bei Vibrometerkanälen automatisch je Messbereich gesetzt. Negative Faktoren und die GUI-Option „Inv.“ (Kehrwert) sind erlaubt ([HB] 7-12, selbst geprüft); beides ist vorzeichenrelevant für Kraft und Phase. Ob „Inv.“ eine eigene Property ist, ist **[ungeprüft]** |
| `Quantity` / `Unit` | rw / r | physikalische Größe (`PTCPhysicalQuantity`), Einheit als Text |
| `IntDiffPhysicalQuantity` | rw | Größe nach Integration/Differentiation; gleich `Quantity` = keine |
| `DirectionOfVibration` | rw | `PTCVibrationDirection` (+Z 0 … 3D-Vektor 6) |
| `WindowFunction`, `WindowFunctionParams`, `WindowFunctionRMSCorrection` | rw, **r**, r | Fensterfunktion (nur FFT, Zoom-FFT, MultiFrame). `WindowFunctionParams` ist laut BEM read-only (Double-Array, [BEM] PSV~ChannelAcqProperties~WindowFunctionParams, selbst geprüft). Ob Parameter von Tapered Hanning, Kraft- und Exponentialfenster per COM setzbar sind (z. B. über den Properties-Container), ist **[offen]**, Prüfpunkt P2-13 |
| `DigitalFilter` | rw | `DigitalFilterLowpass/Highpass/Bandpass/Notch/None` |
| `InputCoupling`, `InputImpedance` (Ω), `ICPInput`, `DifferentialInput` | rw | Hardware-Eingang. Der Vibrometerkanal ist fest DC-gekoppelt. IEPE an einem Referenzkanal schaltet automatisch auf AC-Kopplung mit analogem Hochpass um; die Einschwingzeit beträgt bis zu 1 min, währenddessen wird Overrange angezeigt, relevant für Kraftkanäle bei tiefen Frequenzen ([HB] 7-11/7-12, selbst geprüft für IEPE/AC) |
| `SignalDelay` | rw | s; Phasenkorrektur zwischen Vibrometer- und Referenzkanälen |
| `SEActive` | rw | Signal Enhancement je Kanal |
| `Name`, `ShortName` (≤ 4 Zeichen), `Type` (`PTCChannelType`), `VibrometerIndex` (r, 1-basiert, 0 = kein Vibrometer) | – | Beschreibung |
| `Encoder…` | rw | Drehgeber, für uns nicht relevant |

**Vibrometer** (`VibrometersAcqProperties.Item(i)`, 1-basiert →
`VibrometerAcqProperties.VibControllerSettings` → `IControllerSettings`,
[BEM] PSV~VibrometersAcqProperties~Item; PSV~VibrometerAcqProperties~VibControllerSettings)
- `ControllerSettings`: `ControllerInfo`, `QuantitySettingsCollection`,
  `SensorHeadSettingsCollection`, `FilterSettingsCollection`, `DecoderClearMode`,
  dazu `Save()` und `Load(xml)`. `Save()` liefert den Zustand als XML-Fragment, dessen
  Format **nicht dokumentiert** ist ([BEM] Polytec_IO_VibInterfaces~ControllerSettings, ~Save, ~Load).
- `QuantitySettings`: `Range` (Name des aktiven Messbereichs, rw), `BandwidthRange`,
  `MaxVelocityRange`, `Overrun`, `OutputActive` ([BEM] Polytec_IO_VibInterfaces~QuantitySettings).
- `SensorHeadInfo`: `Name`, `SerialNumber`, `FirmwareVersion`, `LaserWavelength` (nm),
  `LaserPower` (mW) u. a. ([BEM] Polytec_IO_VibInterfaces~SensorHeadInfo).
- Live-Signalpegel: `Acquisition.Infos.Vibrometers(1).Controllers(0).SensorHeads(0).SignalLevel`
  in % ([BEM] Access to General Information; Polytec_IO_VibInterfaces~ISensorHead~SignalLevel).
- Der Geschwindigkeitsmessbereich hängt von der Bandbreite ab ([HB] 7-26, PDF 234).

**Trigger** (`TriggerAcqProperties`, [BEM] PSV~TriggerAcqProperties_members): `Source`
(`PTCTriggerSource`: Off 0, External 1, Analog 2, Internal 3), `Edge` (Rising 0,
Falling 1), `Level` (% von −99 bis 99), `AnalogSourceChannel`, `PreTrigger` (% im
Bereich `PreTriggerMin`…`PreTriggerMax`), `PreTriggerPossible`, `PhaseFromRef` (rw; legt
fest, ob bei aktivem Trigger die Phase der Antwortkanäle aus der Phase der FRF zum ersten
Referenzkanal bestimmt wird, [BEM] PSV~TriggerAcqProperties~PhaseFromRef, selbst geprüft;
Bedeutung für den Phasenbezug siehe 4.4). Externer Trigger 0 bis 5 V TTL ([HB] 7-22, PDF 230).

**Generator** (`GeneratorsAcqProperties.Item(1)` → `GeneratorAcqProperties`;
höchstens ein Generator, [BEM] PSV~GeneratorsAcqProperties~Count;
PSV~GeneratorAcqProperties_members)

| Property/Methode | Zugriff | Einheit/Bedeutung |
|---|---|---|
| `Active` | rw | Generator aktiv |
| `Amplitude` | rw | **V** (Spitzenwert bei hochohmigem Abschluss, [HB] 7-32) |
| `Offset` | rw | V |
| `SteadyStateTime` | rw | s, Einschwingzeit vor der Erfassung |
| `Waveform` | rw | `IWaveform`; für Parameter casten |
| `ActiveChannels`, `MultipleChannels`, `SupportsMultipleChannels` | rw/r | Mehrkanal |
| `AmplitudeCorrectionData`, `UseAmplitudeCorrection`, `LoadAmplitudeCorrectionData(datei)` | rw | Amplitudenkorrektur (Chirp, Pseudo Random) |
| `FrontEndAcqProperties.GeneratorAmplifierEnabled/Factor` | rw | Generatorverstärker des Frontends ([BEM] PSV~FrontEndAcqProperties) |

Signalformen ([BEM] POLYWAVEFORMSLib; Parameter in Hz bzw. s):
- `WaveformSine.Frequency`
- `WaveformSweep.StartFrequency`, `EndFrequency`, `SweepTime`
- `WaveformBurstChirp.StartFrequency`, `EndFrequency`, `BurstStart`, `BurstLength`
  (Typ `Long`, ganzzahlige Prozent) sowie `BurstStartEx`, `BurstLengthEx` (Typ `Double`,
  „in percent“; [BEM] POLYWAVEFORMSLib~WaveformBurstChirp, selbst geprüft). „In % der Messzeit“
  nennt das BEM nicht ausdrücklich **[ungeprüft]**.
- `WaveformPeriodicChirp`, `WaveformPseudoRandom`, `WaveformWhiteNoise` und
  `WaveformBurstRandom` haben laut BEM keine eigenen Parameter (BurstRandom: I5-F). Sie regen
  nur im Bereich `StartFrequency`…`EndFrequency` der FFT-Einstellung an ([HB] 7-16, 7-31;
  PDF 224, 239).
- Im Modus FastScan wird immer mit Sinus auf der FastScan-Frequenz angeregt ([HB] 7-30).
- Die Amplitude ist der Spitzenwert bei hochohmigem Abschluss; bei 50-Ω-Abschluss ist die
  Ausgangsspannung nur halb so groß wie eingestellt ([HB] 7-32, PDF 240). Der Abschluss ist
  per COM nicht lesbar und gehört ins manuelle Protokoll (Abschnitt 6).

**Signal Enhancement** (`SEAcqProperties`): `Mode` (`PTCSignalEnhancementMode`: Fast 0,
FastStandard 1, Standard 2, StandardBest 3, Best 4), `SpeckleTracking`
([BEM] PSV~SEAcqProperties). Mit SE werden bis zu drei- bzw. fünfmal so viele
Mittelungen gemacht wie eingestellt ([HB] 7-25, PDF 233). Die Punktdauer ist dann also
nicht fest. **[Einschätzung]** Für Zeitabschätzungen und Timeouts ist das relevant.

**MultiFrame** (`AverageType`, `FrameCount`, `Mode`, `PulsesPerCycle`) und **FastScan**
(`Bandwidth`, `Frequency`, `SampleFrequency`, `Samples`, `SampleTime`) sind für unsere
Strukturtests voraussichtlich nicht nötig ([BEM] PSV~MultiFrameAcqProperties;
PSV~FastScanAcqProperties). **[Einschätzung]**

### 2.6 Validatoren

- `IFftAcqPropertiesValidator` und `ITimeAcqPropertiesValidator` sind „Staging“-Puffer.
  Man liest den Validator (vorbelegt mit den aktuellen Live-Einstellungen), ändert ihn
  und ruft `Validate()` auf. Alternativ weist man ihn der Property
  `FftAcqPropertiesValidator` bzw. `TimeAcqPropertiesValidator` zu. Diese prüft und
  übernimmt **alle Einstellungen atomar** ([BEM]
  POLYPROPERTIESLib~IFftAcqPropertiesValidator, ~ITimeAcqPropertiesValidator).
- Der FFT-Validator bietet `AvailableBandwidths` (Hz), `AvailableLines` (für die aktuelle
  Bandbreite), `GetMinMaxFrequencyRange(ByRef min, ByRef max)` (erst `Bandwidth` und
  `Lines` setzen), `GetMinMaxOverlap` (0/0 = nicht unterstützt) und `GetMinMaxSamples`.
  `Bandwidth` und `Lines` **rasten beim Setzen auf den nächsten gültigen Wert ein**
  ([BEM] POLYPROPERTIESLib~IFftAcqPropertiesValidator~*).
- Der Zeit-Validator bietet `AvailableSampleFrequencies` (Hz), `AvailableSamples` und
  `GetMinMaxSamplesRange`. `Validate()` prüft auch SE und externen Trigger. Im Modus IQ
  sind die Zeiteinstellungen schreibgeschützt ([BEM]
  POLYPROPERTIESLib~ITimeAcqPropertiesValidator).
- Ungültige Kombinationen erzeugen eine Exception; das Beispiel fängt sie mit
  `Catch oExc As Exception … oExc.Message` ab ([BEM] PSV~FftAcqProperties~FftAcqPropertiesValidator,
  Beispiel).
- **Folgerung [Einschätzung]:**
  - Das Einrasten bedeutet, dass ein geschriebener Wert nicht dem gelesenen entsprechen
    muss. Der Adapter muss nach dem Setzen zurücklesen und Abweichungen melden statt
    still zu übernehmen.
  - Ob die Validatoren in der installierten PSV-Version vorhanden sind, ist **[offen]**.
    Die Hilfe beschreibt mindestens 10.4, die Folien zeigen 10.2.1.1. → Prüfpunkt P1-5.

### 2.7 Scanpunkte, Geometrie, Fokus, Abgleich

- `Acquisition.Infos.MeasPoints` (IMeasPoints11), `Elements`, `MeasurementLocations`
  ([BEM] PSV~InfosAcq_members).
- `MeasPoint` liefert u. a. folgende Daten ([BEM] POLYFILELib~MeasPoint_members):
  - `CoordXYZ(ByRef x, y, z)`; Einheit nicht angegeben, Meter [Einschätzung, da alle
    Abgleich-Methoden Meter nutzen]
  - `VideoXY`, `Label`, `Index`
  - `ScanStatus` (Bitmaske `PTCScanStatus`), `GeometryStatus`, `FocusStatus`, `FocusValues`
  - `AverageCount`, `Sigma`, `MinSigma`, `VibrometerRange`
  - `ScanQuantitiesX/Y` (Scannerwinkel je Kopf) und `ScanDistances`
- `MeasPoints.CoordinatesToArray` liefert alle xyz-Koordinaten als **Single**-Array.
  Das ist schneller als eine Schleife über `CoordXYZ`
  ([BEM] POLYFILELib~MeasPoints~CoordinatesToArray). Wegen `Single` gilt: Genauigkeit
  ca. 7 Stellen. **[Einschätzung]** Für Koordinaten im Meterbereich genügt das.
- **2D/3D-Abgleich** (`Infos.Alignments` → `AlignmentsAcq`: `Alignments2D`,
  `Alignments3D`, `AlignmentsCamera`, [BEM] PSV~AlignmentsAcq). `Alignment3D` liefert
  ([BEM] POLYALIGNMENTLib~Alignment3D_members):
  - `Valid`
  - `CurrentQuality` und `TargetQuality` in **m**
  - `PositionUncertainty` in **m**, `AngleUncertainty` in **rad**
  - `CoordDefinitionMode`, `Mirror`
  - `GetScanHeadPosition(ByRef x, y, z)`
  - Umrechnungen `Coord3DToScanner`/`ScannerToCoord3D`. Scannerwinkel dabei in **Grad**
    (PSV) bzw. m (MSA).
  - `Align3DPoint.Quality` in m je Abgleichpunkt ([BEM] POLYALIGNMENTLib~Align3DPoint~Quality).
- **Fokus:** `AutoFocusLaser`, `AssignFocusAutomatically`, Scan mit
  `ptcScanCapsUseAssignedFocusValuesDuringScan` bzw. `…AutoFocusDuringScan`
  ([BEM] PSV~Acquisition~ScanEx).
- **Geometrie-Scan:** `GeometryScan(ptcGeometryScanCapsNone | …RefineWithAutoFocus | …Selected)`
  ([BEM] PSV~Acquisition~GeometryScan).
- **Vorsicht:** `PolyScanHeadLib~ScanHeadControl` enthält Service-Methoden wie
  `WriteFocusDataFactorySettings`, `WriteMirrorAdjustmentData` und
  `WriteLaserIntensityData`. Sie schreiben Werkskalibrierdaten in den Scankopf
  ([BEM] PolyScanHeadLib~ScanHeadControl). **Diese Methoden dürfen nie benutzt werden.**
  Der Adapter sollte nur freigegebene Methoden kapseln (Whitelist). **[Einschätzung]**

### 2.8 Hardware- und Infos-Objekte (Datenerfassung)

| Objekt | Inhalt | Beleg |
|---|---|---|
| `InfosAcq.Hardware` (`IHardware7`/`HardwareAcq`) | `AcqBoard`, `AcqBoardName`, `AcqBoardFirmwareVersion`, `AcqBoardChannelCount`, `AcqBoardMaxFrequency`, `FrontEnd` (`PTCFrontEndType`, z. B. `ptcFrontEndPSV_F_600_3D` = 124), `FrontEndFirmwareVersion`, `ActiveFrontEnd`, `GeneratorName/Type/FirmwareVersion/ChannelCount`, `ScanHeadType`, `SensorHeadNames/SerialNumbers/Versions` (Top, Left, Right), `CoherenceOptimizerVersions`, `TedsSensors` (XML) | [BEM] PSV~HardwareAcq_members; PolyFrontEndLib~PTCFrontEndType |
| `InfosAcq.Vibrometers` (`VibrometerGroups`) | Controller-Gruppen; beim PSV-3D steuert eine Gruppe die drei Controller gemeinsam | [BEM] PSV~VibrometerGroups; Polytec_IO_VibInterfaces~IControllerGroup |
| `InfosAcq.ScanHeadDevicesInfo` | `ScanHeadName`, `ScanHeadType`, `ScanHeadDevices` (Fokus, Scanner, Video) | [BEM] PSV~ScanHeadDevicesInfoAcq |
| `InfosAcq.PositionDevice` | XY-/Z-Achsen von Polytec: `GetPositionXY/Z` (m), `StartMoveXY/Z` (m), `IsMoving…`, `IsReferenced…`, Min/Max (m) | [BEM] PSV~PositionDevice |
| `Application.DigitalPorts` | Aux In/Aux Out der Anschlussbox: `Value` (rw), `Pulse(Value, Length µs)` | [BEM] PSV~DigitalPorts; PSV~DigitalPort |

`AcquisitionInfoModes`, `CameraSettings`, `VideoBitmap`, `DbReferences` und `Profiles`
gibt es **nicht** in `InfosAcq`, nur in Dateien ([BEM] PSV~InfosAcq~HasAcquisitionInfoModes u. a.).
In der Erfassung liest man die Einstellungen über `Acquisition.ActiveProperties`.

---

## 3 Ablaufsequenzen

Die Sequenzen geben den belegten Weg an. Die Python-Umsetzung ist **[ungeprüft]** (Abschnitt 7).

### 3.1 Verbinden und prüfen

| Schritt | Objekt/Methode | Beleg | Fehlerquellen |
|---|---|---|---|
| 1 | `AcquisitionInstance` erzeugen (ProgID `PSV.AcquisitionInstance`) | [BEM] PSV~AcquisitionInstance | ProgID nicht registriert (PSV nicht installiert, Desktop-Version) |
| 2 | `IsRunning` lesen | [BEM] PSV~AcquisitionInstance~IsRunning | – |
| 3 | `app = GetApplication(True, timeout_ms)` | [BEM] ~GetApplication; [COM] Folie 10 | Start dauert („This can take some time“); bei Ablauf des Timeouts „returns with an error“; Dongle/Lizenz fehlt [Einschätzung] |
| 4 | `app.Version` lesen und protokollieren | [BEM] PSV~Application~Version; [COM] Folie 12 („10.2.1.1“) | – |
| 5 | `app.SuppressMessagesForAutomation` prüfen bzw. setzen (Standard True) | [BEM] PSV~Application~SuppressMessagesForAutomation | GUI-Dialog blockiert den Ablauf, falls False |
| 6 | `app.Mode` prüfen (Acquisition) | [BEM] PSV~Application~Mode | Acquisition nur im Erfassungsmodus ([BEM] Access to General Information) |
| 7 | `acq = app.Acquisition`; `acq.State == ptcAcqStateStopped` prüfen | [BEM] PSV~Acquisition~State | laufende Messung eines Benutzers |
| 8 | Hardware lesen: `acq.Infos.Hardware`, `HasScanHeadDevicesInfo`, `Vibrometers.Count` | [BEM] Access to General Information | Item fehlt → `Nothing` |

### 3.2 Einstellungen laden und gezielt ändern

| Schritt | Objekt/Methode | Beleg | Fehlerquellen |
|---|---|---|---|
| 1 | `app.Settings.Load(pfad_set, ptcSettingsAll)` oder Teilmaske, z. B. `ptcSettingsAcquisition Or ptcSettingsAPS Or ptcSettings3DAlignment` | [BEM] PSV~Settings~Load; PSV~PTCSettings | andere Erfassungskarte/Anschlussbox → Erfassungsteil wird nicht geladen ([HB] 10-4) |
| 2 | `acq.Mode = ptcAcqModeFft` (falls nötig) | [BEM] PSV~Acquisition~Mode | – |
| 3 | `props = acq.ActiveProperties`; `props.HasFftProperties` prüfen | [BEM] PSV~AcquisitionProperties~HasFftProperties | Item fehlt |
| 4 | `v = props.FftProperties.FftAcqPropertiesValidator`; `v.Bandwidth = …`; `v.Lines = …`; `v.GetMinMaxFrequencyRange(min, max)`; `v.StartFrequency/EndFrequency = …` | [BEM] POLYPROPERTIESLib~IFftAcqPropertiesValidator | Einrasten auf andere Werte; Exception bei ungültiger Kombination |
| 5 | `props.FftProperties.FftAcqPropertiesValidator = v` (atomar übernehmen) | [BEM] ebd.; PSV~FftAcqProperties~FftAcqPropertiesValidator, Beispiel | Validator in älteren Versionen evtl. nicht vorhanden [offen] |
| 6 | Mittelung: `props.AverageProperties.Type = ptcAverageComplex`; `.Count = n` | [BEM] PSV~AverageAcqProperties | Bereich 3…10000 |
| 7 | Kanäle, Trigger, Generator, `GeneralProperties.AutoRemeasure` etc. | 2.5 | – |
| 8 | **Zurücklesen** aller Sollwerte und Vergleich; Abweichung = Fehler | [Einschätzung] | Einrasten, stilles Ändern des Offsets beim Generator ([HB] 7-32) |
| 9 | Optional `app.Settings.Save(pfad_set_snapshot)` als Nachweis | [BEM] PSV~Settings~Save | Pfad nicht beschreibbar |

### 3.3 Einzelmessung

1. `acq.Start(ptcAcqStartSingle)` ([BEM] PSV~Acquisition~Start).
2. Warten, bis `acq.State == ptcAcqStateStopped`. Polling-Intervall in den Beispielen
   0,1 s ([BEM] PSV~FftAcqProperties, Beispiel). Ein eigenes Gesamt-Timeout ist nötig,
   da die Doku keines vorsieht [Einschätzung].
3. Daten live: `acq.PointDomains.Type(ptcDomainSpectrum).Channels.Item("Vib")…Displays.Type(…)`
   → `acq.GetData(display)` → `OpenDataStream(BlockCount, 0)` → `Read(0, -1, data)`
   ([BEM] PSV~Acquisition~GetData, Beispiel). `Stride` ist 1 oder 2; bei Real/Imag ist
   er 2 und die Werte sind verschränkt ([BEM] PolyAcquisitionLib~AcquisitionPointDataStream~Stride).
4. Alternativ als Datei speichern: `acq.Document.SaveAs(pfad.pvd)`. **[ungeprüft]**:
   `VibDocument.SaveAs` ist belegt ([BEM] PSV~VibDocument), aber nicht ausdrücklich für das
   Erfassungsdokument. Laut Handbuch speichert die GUI Einpunktmessungen mit Zeitsignalen,
   Spektren und Parametern ([HB] 10-9).
- Fehlerquellen: Generator aktiv startet Signalausgabe; Overrange; Stop bei Continuous nötig.

### 3.4 Scan (alle, fortsetzen, nachmessen)

| Schritt | Objekt/Methode | Beleg | Fehlerquellen |
|---|---|---|---|
| 1 | Zielpfad prüfen: Datei darf nicht existieren (Rohdaten nie überschreiben) | KONVENTIONEN; Verhalten von PSV bei vorhandener Datei **[offen]** | Überschreiben oder Rückfrage-Dialog |
| 2 | `acq.ScanFileName = pfad.svd` (nie leer lassen, sonst Dialog) | [BEM] PSV~Acquisition~ScanFileName | Dialog blockiert den Ablauf |
| 3 | `acq.ScanEx(ptcScanAll, ptcScanCapsNone)` bzw. `acq.Scan(ptcScanAll)` | [BEM] ~ScanEx; [COM] Folie 12 | Scanpunkte/Abgleich fehlen; Generator startet automatisch ([HB] 8-3) |
| 4 | Überwachen: `State` pollen (≠ Stopped) und/oder Events `ScanStateChanged` | [COM] Folie 12; [BEM] ~ScanStateChanged_EV | Event-Empfang aus Python [ungeprüft] |
| 5 | Ende: `State == ptcAcqStateStopped` | ebd. | Scan bricht nach drei Fehlversuchen an einem Punkt ab ([HB] 2-23) |
| 6 | Fortsetzen nach Stopp: `ScanEx(ptcScanContinue, …)` | [BEM] PSV~PTCScanMode; [HB] 8-4 | – |
| 7 | Nachmessen: `ptcScanRemeasure` (Overrange, Ungültig, Nicht gemessen), `ptcScanRemeasureAutoRange`, `ptcScanRemeasureFile` (Datei aus `ScanFileName`, Punkte zuvor in der Auswertung markiert) | [BEM] PSV~Acquisition~Scan; [HB] 8-4 | – |
| 8 | Automatisch statt manuell: `GeneralProperties.AutoRemeasure(=True)`, `AutoRemeasureAutoRange` | [BEM] PSV~GeneralAcqProperties | – |

- Laut Handbuch wird jeder Scanpunkt **sofort gespeichert**. Bei Abbruch bleiben alle
  gemessenen Punkte in der `.svd` ([HB] 8-3, 10-8).
- Scanmodi mit Werten: All 0, Continue 1, Remeasure 2, RemeasureAutoRange 3,
  RemeasureFile 4. ScanCaps: None 0, UseAssignedFocusValuesDuringScan 1,
  VideoTriangulation 2, VideoTriangulationFast 4, AutoFocusDuringScan 8,
  AsynchronousScanEvent 16 ([BEM] PSV~PTCScanMode, PSV~PTCScanCaps).

### 3.5 Fortschritt und Abbruch

- **Fortschritt:** Mit Events zählt man `EndScanPoint` gegen `Infos.MeasPoints.Count`.
  Gesperrte oder nicht erreichbare Punkte werden vermutlich nicht gemessen; der Nenner
  ist dann zu groß. **[Einschätzung]**
- **Ohne Events:** Die Doku nennt keine Fortschritts-Property. Möglich wäre ein Blick auf
  den Punktstatus in der Datei, aber das kollidiert mit dem exklusiven Dateizugriff
  ([BEM] Opening and Closing Files). **[offen]**
- **Abbruch:** `acq.Stop()` ([BEM] PSV~Acquisition~Stop). Danach `State` bis Stopped
  pollen. Gemessene Punkte bleiben erhalten ([HB] 10-8).
- **Timer:** `PTCTimer` (Interval in ms, Event `Timer`) ist für Makros gedacht
  ([BEM] PSV~PTCTimer). Für Python ist er nicht nötig.

### 3.6 Speichern

- **Scan:** automatisch während des Scans nach `ScanFileName` (siehe 3.4).
- **Einstellungen:** `Settings.Save(pfad.set)` ([BEM] PSV~Settings~Save).
- **Dokument:** `Document.Save()` / `SaveAs(datei)` ([BEM] PSV~Document).
- Den Dateinamen nach einem Scan mit Dialog liefert
  `app.ActiveDocument.Name` ([BEM] PSV~Acquisition~ScanFileName, Remarks).
- **Videobild:** `ExportVideoSnapshotEx(datei, ptcSnapshotTypeMainCamera)`
  ([BEM] PSV~Acquisition~ExportVideoSnapshotEx).

### 3.7 Export (UFF, ASCII u. a.)

| Schritt | Objekt/Methode | Beleg |
|---|---|---|
| 1 | `exp = app.Exporter(eingabe.svd, ptcExportTypeUniversalFile)` (Default-Interface `Application`, siehe 1.5) oder `VibDocument.Exporter(typ)` | [BEM] PSV~Application~Exporter; PSV~VibDocument~Exporter |
| 2 | `params = New ExportParameters`; optional `exp.LoadParameters(params)` (letzte GUI-Einstellung übernehmen) | [BEM] PSV~Exporter~LoadParameters, Beispiel |
| 3 | `params.FileName`, `PointSignals` (z. B. `"FFT \ Vib \ Displacement"`, `"FFT \ Vib & Ref1 \ H1 Displacement / Voltage"`), `BandSignals`, `ReferencePointIndices`, `ExportBinary` (UFF 58b), `ExportInvalidatedPoints`, `ExportOverrangePoints`, `ExportFilteredData`, `ExportInterpolatedPoints`; `params.Validate()` | [BEM] PSV~ExportParameters_members; PSV~Exporter, Beispiel |
| 4 | `exp.Export(params)` synchron oder `ExportAsync` mit Events `ProgressChanged(%)`, `ExportCompleted(cancelled, errorOccurred, errorMessage)`, `IsBusyChanged`; `CancelAsync()` | [BEM] PSV~Exporter_members |

- Exporttypen: UFF 0, ME'Scope 1, ASAM ODS ATFX 2 ([BEM] PSV~PTCExportType).
  ME'Scope braucht die Option ExpME, ATFX die Option ExpASAM ([HB] 10-8).
- Eingabe kann `.pvd`, `.svd`, `.mvd` oder `.set` sein ([BEM] PSV~Application~Exporter).
- UFF exportiert Punkte mit Status „Nicht gemessen“ nicht und funktioniert nicht im
  APS-Modus ([HB] 10-15). Punktdaten als Datensatz 58/58b in einfacher Genauigkeit
  (I1, [HB] 10-15).
- **ASCII-Export** von Messdaten ist nur in der Auswertung (GUI) beschrieben und exportiert
  die *angezeigten* Daten ([PRES] 5_2_7). Ein COM-Exporttyp „ASCII“ existiert nicht
  ([BEM] PSV~PTCExportType). → Für ASCII-ähnliche Daten ist PolyFile der Weg (Abschnitt 4).

### 3.8 Beenden

- Verbindung lösen: Referenzen freigeben (`Set obj = Nothing`), damit Ressourcen frei
  werden ([BEM] Using Object Variables). Aus Python: Referenzen löschen. **[ungeprüft]**,
  ob PSV dann offen bleibt.
- PSV beenden: `app.Quit()` ([BEM] PSV~Application~Quit). Events `QuitEx(ByRef stopQuitting)`
  und `Quit` ([BEM] PSV~Application~QuitEx_EV). **[Einschätzung]** Das Paket sollte PSV
  nur beenden, wenn es PSV selbst gestartet hat (`IsRunning` vor dem Verbinden merken).
- Laser ausschalten: `SetLaserOn(-1, False, True)` (Laser aus und an den Rand fahren)
  ([BEM] PSV~Acquisition~SetLaserOn).
- Generator aus: `acq.GeneratorsOn = False` ([BEM] PSV~Acquisition~GeneratorsOn).

---

## 4 Auswertung und Dateizugriff

### 4.1 Wege zu den Daten

| Weg | Voraussetzung | Stärken | Grenzen | Beleg |
|---|---|---|---|---|
| **PolyFile** (`PolyFile.PolyFile`) | PFA installiert (ohne Dongle), Windows | alle Domänen, Kanäle, Signale, Geometrie, Status, Metadaten; komplexe Daten | Datei darf nicht gleichzeitig in PSV offen sein; nur Windows | [PFA] Overview; [PFA-M] Folie 2; [BEM] Opening and Closing Files |
| **PresentationInstance** | PSV installiert | `Documents.Open`, Exporter, Fenster | GUI-gebunden; für Datenzugriff gedacht ist PolyFile | [BEM] PSV~PresentationInstance |
| **Live** `Acquisition.GetData` | Erfassung läuft | Daten des aktuellen Punkts | nur Momentaufnahme; Freigabe nötig | [BEM] PSV~Acquisition~GetData |
| **UFF-Export** | PSV (Exporter) | offenes Format, plattformunabhängig | Single Precision; Auswahl über Signalstrings | [BEM] PSV~Exporter; [HB] 10-15 |

### 4.2 Datei öffnen und schließen

- `f = PolyFile` erzeugen, dann `f.Open(pfad)`. Lesbar sind PSV-Dateien ab Version 7.0
  sowie Einstellungsdateien ([BEM] Opening and Closing Files).
- Je PolyFile-Objekt ist nur eine Datei offen. Eine Datei kann nicht gleichzeitig mehrfach
  geöffnet werden, weder von PFA noch von PSV; sonst **Sharing Violation**
  ([BEM] Opening and Closing Files; POLYFILELib~PolyFile~Open).
- `Close()` vor dem nächsten `Open`. Freigeben des Objekts schließt die Datei
  ([BEM] POLYFILELib~PolyFile~Close).
- `ReadOnly` ist rw. Ändert man die Property, werden alle bisherigen Referenzen auf
  PFA-Objekte ungültig ([BEM] POLYFILELib~PolyFile~ReadOnly). Der Standardwert ist
  nicht angegeben; die Beispiele setzen `ReadOnly = False` vor dem Schreiben
  ([BEM] Creating New Files). → Für Rohdaten **immer** mit `ReadOnly = True` öffnen
  [Einschätzung].
- `IsDataPossible(ptcDataPoint | ptcDataAverage | ptcDataBand)` prüft, welche Datenart es
  gibt ([BEM] POLYFILELib~PolyFile~IsDataPossible).

### 4.3 Domänen, Kanäle, Signale, Displays

- Weg: `GetPointDomains(BuildFlags)` → `PointDomain` → `Channels` → `Signals` →
  `Displays` → `Display`. Dazu `DataPoints(i).GetData(Display, Frame)`
  ([BEM] Access to Data).
- Domänennamen: „Time“, „FFT“, „RMS“, „1/3 Octave“; Enum `PTCDomainType`
  ([BEM] Access to Data; POLYSIGNALLib~PTCDomainType).
- Kanäle: „Vib“, „Ref1“, „Vib & Ref1“, beim 3D zusätzlich „Vib X/Y/Z“ bzw. „Vib 3D“,
  Benutzerkanal „Usr“.
- Signale: „Velocity“, „Displacement“, „FRF Velocity/Voltage“, H1/H2, Kohärenz u. a.
  ([BEM] Access to Data).
- **FRF-Signale und Kombikanäle (I5-F, SWP Tab. 3.2, 3-31):** FRF, H1, H2, Kohärenz und
  Kreuzspektrum (CP) liegen in Kombikanälen („Vib & Ref n“, „Vib 3D & Ref 1“) und sind nur
  vorhanden, wenn ein Referenzkanal aktiv war. Die Signalnamen tragen die Einheit der Referenz
  (z. B. „H1 Geschwindigkeit/Spannung“). Referenzgröße und -einheit sind über
  `SignalDescription` (`ReferenceDOFs`, `YAxis.Unit`) zu prüfen, nicht aus dem Namen zu raten.
- **Build-Flags:** Standard bei `GetPointDomains` ist `ptcBuildPointDataXYZ` (723775) mit
  den Kanälen Vib X/Y/Z. `ptcBuildPointData3d` (722751) erzeugt „Vib 3D“
  ([BEM] POLYFILELib~PolyFile~GetPointDomains; POLYSIGNALLib~PTCSignalBuildFlags).
- `Display.Type` ist vom Typ `PTCDisplayType`. Für uns relevant:
  - `ptcDisplayRealImag` (9)
  - `ptcDisplayMagPhase` (2, Phase in Grad)
  - `ptcDisplayMagPhaseRad` (14)
  - `ptcDisplayReal` (7), `ptcDisplayImag` (8), `ptcDisplayMag` (1)
  - `ptcDisplaySamples` (12, Zeitdaten)
  - Quelle: [BEM] POLYSIGNALLib~PTCDisplayType.
- `Signal.Description` (`SignalDescription`) liefert: `DomainType`, `FunctionType` (z. B.
  H1 = 300, H2 = 301, Kohärenz = 6, Kreuzspektrum = 3, Zeit = 1, Spectrum = 12, FRF = 4;
  dazu die PCA-Typen 302–304, relevant für U6, siehe Abschnitt 8), `Complex`, `XAxis`
  (Name, Unit, Min, Max, MaxCount), `YAxis` (Name, Unit), `ResponseDOFs`/`ReferenceDOFs`
  mit `Node`, `Direction`, `Quantity`, `Unit`, `RMSCorrectionFactor`
  ([BEM] POLYSIGNALLib~SignalDescription; POLYSIGNALLib~PTCFunctionType; POLYSIGNALLib~DegreeOfFreedomID).
  Damit lässt sich die Signalbedeutung maschinell prüfen, statt sie aus Namen zu raten
  [Einschätzung].

### 4.4 Datenformat und Umrechnung in unsere Konventionen

Belegt ([BEM] Access to Data; POLYFILELib~DataPoint~GetData, ~Get3DData, ~GetDataSection):
- Rückgabe ist ein **0-basiertes Array aus Single (float32)**.
- **Zeitmodus:** Abtastwerte der letzten Mittelung, Index 0 … Samples−1.
- **FFT:** gemitteltes Spektrum ab **Linie 1 (Index 0)** bis Linie Lines (Index Lines−1)
  ([BEM] Access to Data). `Lines` ist dort die Gesamtzahl der Linien im Vollbereich. Bei
  eingeschränktem Frequenzbereich (Von/Bis) siehe die Regel unter „Frequenzachse“ unten:
  die Datenlänge kann kleiner als `Lines` sein.
- **Zwei Größen** (Real & Imag., Mag. & Phase) liegen **verschränkt**: gerade Indizes
  Real bzw. Betrag, ungerade Imag bzw. Phase.
- **3D-Kanal** (`ptcChannelCapsVector`): erst alle x-, dann alle y-, dann alle z-Werte.
  `Get3DData` füllt bei 1D-Quellen die fehlenden Richtungen mit Nullen.
- **Frame:** Der Frame ist 0, außer in folgenden Fällen ([BEM] POLYFILELib~DataPoint~GetData,
  selbst geprüft):
  - **MultiFrame-Modus:** Frame 0 ist der „average frame“, die weiteren Frames sind 1…Anzahl
    der Frames. „Mittelwert-Frame“ hat nichts mit der FFT-Mittelung zu tun.
  - **PCA-Signale:** Principal Inputs und Virtual Coherences haben die Frames
    1…Anzahl der Referenzkanäle.
  - **Benutzersignale:** Frames 1…12.
  Fehlt der Frame, kommt ein leeres Array ohne Fehler ([BEM] Access to Data, „Access to
  User-Defined Data“). → Leeres Array im Adapter als Fehler behandeln [Einschätzung].
- `GetDataSection(Display, Frame, Average, First, Last)` liefert einen Ausschnitt. Mit
  `Average` (1…`AverageCount`) liefert sie die Einzelblöcke (Zeitspuren) der FFT-Mittelung,
  aber nur für Zeitsignal-Displays von FFT-Messungen, also nur, wenn Zeitdaten gespeichert
  wurden (`SaveTimeDataForScan`/Modus Zeit). Ein Average > 1 ist nur für Zeitspuren aus einem
  Messmodus mit FFT-Mittelung gültig ([BEM] POLYFILELib~DataPoint~GetDataSection, selbst
  geprüft).
- **Punktmittel:** `GetPointAverageDomains` → `PointAverageDomain.GetData`. Es ist das
  Mittel über alle gültigen Punkte, laut PFA nur als Amplitudenmittel; ein komplexes
  Punktmittel fehlt in PSV ([BEM] Access to Data; [PFA] Examples, ComplexPointAverage).
  Ist `IsAverageSpectrumCorrected` gesetzt, wurden invalidierte Punkte berücksichtigt
  ([BEM] POLYFILELib~PolyFile~IsAverageSpectrumCorrected).
- **Bänder:** `DataBand.GetData` liefert einen Wert je Messpunkt; `Data(0)` gehört zu
  Punkt 1. Die Domain „RMS“ hat zusätzlich das Band „Entire Bandwidth“
  ([BEM] Access to Data).

**Frequenzachse:**
- `PointDomain.GetXAxis(Display)` → `XAxis` mit `Min`, `Max`, `MaxCount`, `Unit` und
  `GetLeftX/GetMidX/GetRightX(i)` ([BEM] POLYFILELib~PointDomain~GetXAxis; POLYFILELib~XAxis).
- **Von/Bis-Regel (M1, KONVENTIONEN):**
  - Die Frequenzachse wird **immer aus `XAxis`** gebildet (`Min`, `Max`, `MaxCount`,
    `GetMidX(i)`), nie aus $\Delta f\cdot\mathrm{arange}(1, n+1)$ angenommen.
  - Begründung: Mit eingeschränktem Bereich ($\mathrm{Von} \ne 0$ oder $\mathrm{Bis} \ne BW$)
    kann die gespeicherte Datenlänge kleiner als `Lines` sein ([HB] 7-16/7-17: „Von, Bis: Sie
    können den Frequenzbereich einschränken, der angezeigt und ausgewertet wird“; „Die
    angezeigte Anzahl von FFT-Linien entspricht dem Frequenzbereich zwischen Von und Bis“,
    selbst geprüft). Dann wäre die angenommene Achse um den Index der ersten Linie
    verschoben. Ob die Datei nur den Teilbereich enthält, ist aus der Doku nicht belegbar
    **[offen]**, Prüfpunkt P1-11.
  - Rechenbeispiel (I5-F): $BW = 5000$ Hz, 400 Linien ($\Delta f = 12{,}5$ Hz), Bereich
    1000–4000 Hz ergibt 241 Linien von 1000 bis 4000 Hz ($k_\mathrm{min} = 80$,
    $k_\mathrm{max} = 320$).
  - Prüfregel im Adapter: Die Datenlänge (Anzahl komplexer Werte) muss `XAxis.MaxCount`
    entsprechen; $\Delta f$ aus `SampleResolution` (bzw. $BW/\mathrm{Lines}$) bestimmen; der
    Linienindex $k = f/\Delta f$ wird mitgeführt, `MaxCount` mal $\Delta f$ muss zum Bereich
    passen; Abweichungen sind ein Fehler, keine stille Korrektur.
  - Von/Bis (`StartFrequency`, `EndFrequency`) gehören in die Metadaten (Abschnitt 6).
  - Die KONVENTIONEN-Formel lautet entsprechend $k = k_\mathrm{min}\dots k_\mathrm{max}$, im
    Vollbereich $1\dots n_\mathrm{FFT}$.
- **Achsenarten (m4):** Diese Frequenzachse gilt nur für den Modus FFT. Zoom-FFT hat eine
  andere Achse (Mittenfrequenz `CenterFrequency`). Für Zeitdaten gilt
  $\Delta t = 1/f_\mathrm{Abtast}$ mit $f_\mathrm{Abtast} = 2{,}5\cdot BW$ (M-Systeme 2,56·BW,
  siehe 2.5); `XAxis.Unit` ist dann s [Einschätzung; Einheit am Gerät prüfen].
- **Neuer Beleg zur KONVENTIONEN-Annahme:** Das Matlab-Beispiel zeigt für ein FFT-Signal
  `XMin = 12.5`, `XMax = 5000`, `XCount = 400`, Einheit Hz ([PFA-M] Folie 8; x als
  1×400 mit Minimum 12,5 auf Folie 9). Das passt genau zu $f_k = k\,\Delta f$ mit
  $k = 1\dots400$ und $\Delta f = 5000/400 = 12{,}5$ Hz: $(5000-12{,}5)/399 = 12{,}5$
  (nachgerechnet, in I5-F bestätigt). DC ist nicht enthalten. Die Bandbreite ist auf der Folie
  nicht sichtbar; es gilt daher nur „konsistent mit“, nicht „bewiesen“.
- Ob `XMin`/`XMax` Bin-Mitten sind, sagt die Doku nicht. **Empfehlung [Einschätzung]:**
  Die Achse im Adapter aus `GetMidX(i)` bzw. `Min/Max/MaxCount` bilden und gegen
  $k\,\Delta f$ mit `rtol` prüfen, statt sie zu berechnen. Die Konvention bleibt
  „vorläufig“, bis eine reale Datei vorliegt (P1-11).

**Skalierung und Phasenbezug (M2).** Die folgenden Punkte stammen aus I5-F (Quellen dort:
I2 §1.2/§3.3/§3.8, TM 3-3 und Tab. 6.1, Matlab-Folie 9) und sind **nicht** von mir an der
Originalquelle nachgeprüft; an einer realen Datei zu bestätigen:
- **Skalierung:** Die Spektren sind einseitig und amplitudentreu auf die Spitzenamplitude
  (0-to-peak, Fensterkorrektur) skaliert. Die Matlab-Folie 9 zeigt „Amplitude in m/s“. Eine
  falsch angenommene Skalierung (RMS statt Spitzenwert) würde ODS-Auswertung und alle
  Sollwert-Tests verfälschen.
- **Bedeutung der komplexen Daten:** Real/Imag entsprechen $A\,e^{i\varphi_0}$ bei der
  Zeitabhängigkeit $e^{+i\omega t}$, also $A\cos(\omega t + \varphi_0)$ (KONVENTIONEN).
- **Einheiten je Spektrenart:** Autospektrum (AP) hat die Einheit (Einheit)², PSD zusätzlich
  pro Hz, FRF den Quotienten der Einheiten. Die Einheit wird aus `YAxis.Unit` gelesen.
- **Phasenbezug:** Phase ist nur mit Referenz oder Trigger definiert (TM Tab. 6.1). Mit
  Referenz gilt die Phase relativ zur Referenz, mit Trigger ohne Referenz relativ zum
  Fensteranfang. Bei Betragsmittelung wird die Phase nachträglich aus dem Kreuzspektrum
  zugewiesen. Mit `PhaseFromRef` (bei aktivem Trigger) wird die Phase der Antwortkanäle aus
  der FRF zum ersten Referenzkanal bestimmt ([BEM] PSV~TriggerAcqProperties~PhaseFromRef).
- **Pflichtmetadaten je Messung:** Mittelungstyp, Trigger, Referenzkanäle, `PhaseFromRef`,
  Fenster (Abschnitt 6). **Ohne Referenz und ohne Trigger darf der Adapter keine Phase als
  gültig kennzeichnen** (KONVENTIONEN).

**Umrechnung (Vorschlag für den Adapter [Einschätzung], konform zu KONVENTIONEN):**

| Polytec | intern |
|---|---|
| Single-Array (float32) | `np.asarray(x, dtype=np.float32).astype(np.float64)`; die Umwandlung float32→float64 ist exakt, mehr Genauigkeit entsteht aber nicht |
| Real&Imag verschränkt | `z = a[0::2] + 1j*a[1::2]` → `complex128` |
| Mag&Phase (Grad) | vermeiden; falls nötig `ptcDisplayMagPhaseRad` oder Real/Imag verwenden |
| 3D xyz hintereinander | `a.reshape(3, n)` bzw. bei komplex `a.reshape(3, n, 2)` → Achse 0 = x, y, z im Objektkoordinatensystem des 3D-Abgleichs (KONVENTIONEN). Belegt ist das Layout für den Vektorkanal (`GetData` auf „Vib 3D“, `Get3DData`). Für 3D nur Real&Imag verwenden und den Betrag selbst berechnen (siehe unten) |
| 1-basierte Punkte | interner Index `i0 = index - 1`; `label` und `index` mitführen |
| Einheit | aus `YAxis.Unit`/`Signal.Description.YAxis.Unit` lesen und prüfen (z. B. „m/s“), nicht annehmen |
| Frequenzachse | aus `XAxis` (Hz), Abgleich gegen $k\,\Delta f$; Datenlänge gegen `MaxCount` prüfen (Von/Bis, siehe oben) |
| Phase | nur mit Referenz oder Trigger als gültig kennzeichnen (siehe „Skalierung und Phasenbezug“) |

**3D-Komponenten, Betrag und Vorzeichen (m2).**
- Ob die Displays Betrag/Phase auf einem Vektorkanal den Vektorbetrag oder je Komponente
  liefern, ist nicht belegt **[offen]**. I2 nennt $A=\sqrt{A_x^2+A_y^2+A_z^2}$ mit „Phase nicht
  verfügbar“; eine Quelle dazu fand die Fachprüfung im Textextrakt nicht (I5-F). Deshalb für 3D
  nur Real&Imag lesen und den Betrag im Adapter selbst berechnen.
- **Vorzeichen getrennt** (KONVENTIONEN): Bei Kanälen je Scankopf (1D) bedeutet positive
  Geschwindigkeit Bewegung in Richtung Scankopf (KA 2-32). Für X/Y/Z gilt positiv = entlang
  der Achse des 3D-Koordinatensystems; das ist nur über `PTCVibrationDirection` (+X/+Y/+Z)
  indirekt gestützt **[ungeprüft]**, am Gerät zu bestätigen (P1-12).
- Die Mess-Koordinatendefinition (`CoordDefinitionMode`, Abschnitt 8) gehört in die
  Metadaten (Abschnitt 6).

### 4.5 Geometrie, Punktstatus und Mesh

- Koordinaten: `MeasPoints.CoordinatesToArray` (Single, xyz hintereinander),
  `MeasPoint.CoordXYZ`, `Has3DCoordinates` ([BEM] POLYFILELib~MeasPoints).
- Punktstatus: `DataPoint.GetScanStatus(Display)` je Signal oder
  `DataPoints.GetScanStatus(Signal)` für alle Punkte. Array-Index = Messpunkt-Index − 1
  ([BEM] POLYFILELib~DataPoints~GetScanStatus). `MeasPoint.ScanStatus` ist eine
  Bitmaske (Abschnitt 8).
- Elemente: `Elements(i).MeasPointIndices` bzw. `MeasPointLabels`; `Elements.ToArray(labels)`
  liefert pro Element die Punktanzahl und danach die Indizes ([BEM] POLYFILELib~Element; ~Elements~ToArray).
- Videobild: `Infos.VideoBitmap` (Beispiel „Save Bitmap to File“, [BEM] POLYFILELib~VideoBitmap).
- Statusbedeutung laut GUI ([HB] 8-5/8-6):
  - Overrange: Eingangsbereich der Erfassungskarte überschritten. Aussteuerungsreserve
    25 % bzw. 100 %; durch Oversampling ist Overrange auch bei unauffälligem Zeitsignal
    möglich.
  - Optimal: nur mit Signal Enhancement.
  - Weitere Status: Gesperrt, Nicht erreichbar, Verdeckt, VT fehlgeschlagen.

### 4.6 Eigene Daten schreiben

- Benutzersignale gibt es nur im Kanal „Usr“ (bzw. „Usr 3D“) der Domänen „Time“ und
  „FFT“. Ablauf ([BEM] Access to Data; POLYFILELib~PointDomains~AddSignal;
  POLYFILELib~DataPoint~SetData):
  1. `SignalDescription` anlegen (Name, DomainType, DataType, FunctionType,
     ResponseDOFs, XAxis/YAxis).
  2. `GetPointDomains(...)` → `AddSignal(desc)` → `DataPoint.SetData(signal, frame ≥ 1, data)`.
- Komplexe Daten müssen doppelt so lang und verschränkt sein; Frames sind 1…12 und
  werden aufsteigend befüllt ([BEM] Access to Data).
- Neue Dateien: `PolyFile.Create(pfad, ptcCreateAlways)` (**überschreibt** vorhandene
  Dateien!), `Version.FileID = ptcFileIDPSVFile`, MeasPoints/Elements hinzufügen,
  Signale anlegen, `Save()` ([BEM] Creating New Files; POLYFILELib~PolyFile~Create).
- Die Polytec-Beispiele (`band_average.py`, Matlab `CalculateFFT`) **verändern die
  Messdatei** ([PFA] Examples). Das widerspricht „Rohdaten nie überschreiben“
  (KONVENTIONEN). → Schreiben nur in Kopien, z. B. über `SaveAs`/`SaveAsEx` oder eine
  Dateikopie mit Prüfsumme [Einschätzung].
- Kombinierte Dateien (`ContainedFiles`, `.svd`) bündeln mehrere 3D-Messungen; die Infos
  stammen aus der ersten enthaltenen Datei ([BEM] Operating on Combined Files).

### 4.7 Performance

- `DataPointReader` (über `PointDomain.CreateDataPointReaderAsync(displays, statusFilter, progress)`
  → `IComTask`) liest große Blöcke für mehrere Displays, Punkte und Frames. Polytec
  nennt das „advanced“ und empfiehlt es nur, wenn Leseleistung kritisch ist
  ([BEM] POLYFILELib~DataPointReader; POLYFILELib~PointDomain~CreateDataPointReaderAsync).
- Für den ersten Stand reicht `GetData` je Punkt. Ob das bei großen Scans schnell genug
  ist, ist **[ungeprüft]** (P3-3).

---

## 5 Meldungen, Fehler, Events, Timeouts, Nebenläufigkeit

### 5.1 Meldungen

- `Application.SuppressMessagesForAutomation` (rw, Standard **True**): Statt eines
  Meldungsfensters wird das Event `MessageOccurred(MessageStyle, MessageText, ByRef pVal)`
  ausgelöst. Über `pVal` (`PTCMessageAnswer`) simuliert man die Antwort des Benutzers
  ([BEM] PSV~Application~SuppressMessagesForAutomation, ~MessageOccurred_EV).
- In der GUI heißt die Option „Meldungen für Automation (Scripting) unterdrücken“. Ohne
  sie können Meldungen Makros unterbrechen. Meldungen mit Abfragen oder Hinweisen auf
  fehlerhafte Eingaben werden laut GUI-Text „in jedem Fall“ angezeigt
  ([HB] 3-23, PDF 67; [PSVH] 3_7).
  - Ob das auch bei Automation gilt, ist **[offen]**.
  - Das ist ein Risiko für unbeaufsichtigte Abläufe (P1-8).
- `WarningLevel` (`PTCWarningLevel`: All 0, Warnings 1, Errors 2, None 3) und
  `MessagesLoggingEnabled` (Protokoll in der Windows-Ereignisanzeige unter
  „Anwendungs- und Dienstprotokolle > Polytec“, exportierbar als evtx/xml/txt/csv)
  ([BEM] PSV~Application~WarningLevel, ~MessagesLoggingEnabled; [HB] 3-23/3-24).
- Der Inhalt des Meldungsfensters wird **automatisch in der Messdatei gespeichert**
  ([HB] 2-24, PDF 40). PolyFile: `SummaryInfo.Subject` speichert „warnings, errors and
  informational messages that occurred during data taking“
  ([BEM] POLYFILELib~SummaryInfo~Subject). Das ist eine wichtige Metadatenquelle (6).

### 5.2 Fehler

- Die Doku nennt **keine HRESULT-Fehlercodes** für Acquisition, Settings oder PolyFile
  (gezielt gesucht nach HRESULT, error, exception, thread, apartment, timeout). Belegt
  sind nur einzelne Fehlerfälle:
  - `ActiveDocument`/`ActiveWindow` ohne offenes Dokument bzw. Fenster →
    „an error occurs“ ([BEM] PSV~Application~ActiveDocument, ~ActiveWindow)
  - `ExportAsync` bei `IsBusy` → Fehler ([BEM] PSV~Exporter~ExportAsync)
  - `GetApplication`-Timeout → „returns with an error“ ([BEM] PSV~AcquisitionInstance~GetApplication)
  - Sharing Violation bei Mehrfachöffnung ([BEM] Opening and Closing Files)
  - ungültige Validator-Kombination → Exception mit `Message` ([BEM] PSV~FftAcqProperties, Beispiel)
- Typisierte Collections liefern bei fehlendem Element `Nothing` statt eines Fehlers
  ([BEM] Using Collections). → In Python ist `None` zu prüfen [ungeprüft].
- Scan: Bei kritischen Fehlern wiederholt PSV die Messung an einem Punkt bis zu
  dreimal, dann stoppt der Scan. Bei Ethernet-Datenerfassung gilt das nicht; der Scan
  läuft weiter ([HB] 2-23, PDF 39). Ob das PSV-F-600 dazu zählt, ist **[offen]**.
- **pywin32 [ungeprüft]:** COM-Fehler kommen als `pywintypes.com_error` mit `hresult`
  und `excepinfo`; Beschreibung in `excepinfo[2]`. Der Adapter sollte sie in eigene
  Exceptions mit Kontext übersetzen (Methode, Parameter).

### 5.3 Events

| Event | Quelle | Belegt für | Aus Python |
|---|---|---|---|
| `AcqStateChanged(AcqState)` | Acquisition | Makros (`WithEvents`), WWB.NET | **[ungeprüft]** |
| `ScanStateChanged(ScanState, ScanPoint)` | Acquisition | Makros | **[ungeprüft]** |
| `MessageOccurred(Style, Text, ByRef Answer)` | Application | Makros/Automation | **[ungeprüft]**, ByRef-Rückgabe besonders unsicher |
| `Quit`, `QuitEx(ByRef stop)` | Application | – | **[ungeprüft]** |
| `ProgressChanged`, `ExportCompleted`, `IsBusyChanged` | Exporter | WWB.NET-Beispiel | **[ungeprüft]** |
| `Start/Step/Finished`, `StartHint/StepHint/FinishedHint` | PolyFile (Bänder, kombinierte Dateien) | – | **[ungeprüft]** |
| `OnCOMPropertyChanged` | Controller-/Sensorkopf-Einstellungen | – | **[ungeprüft]** |

- Polytec schreibt, Events seien „effizienter“ als eine Warteschleife
  ([BEM] Working with Objects). Ein Makro muss aber weiterlaufen, sonst kommen keine
  Events mehr an ([BEM] PSV~Acquisition~ScanStateChanged_EV, Beispieltext).
- Mit `ptcScanCapsAsynchronousScanEvent` werden Scan-Events asynchron gefeuert
  ([BEM] PSV~Acquisition~ScanEx). Ob das das Zustellverhalten an einen externen Client
  ändert, ist **[offen]**.
- Polytec selbst zeigt für externe Programme das **Polling von `State`** (C#, 1 s;
  [COM] Folie 12).

### 5.4 Timeouts

- Belegt sind nur:
  - `GetApplication(…, lTimeOut)` in ms, Standard 10000; ohne Wirkung bei `vbCreate = False`
    ([BEM] PSV~AcquisitionInstance~GetApplication)
  - `IComTask.WaitWithTimeout/TryWaitWithTimeout(ms)` ([BEM] PolyScanHeadLib~IComTask)
- Für Scan, Einzelmessung, Settings.Load, Export und Autofokus gibt es **keine**
  Timeout-Parameter. → Eigene Gesamt-Timeouts aus der erwarteten Dauer bilden
  [Einschätzung]:
  - Erwartete Dauer ≈ Punktanzahl · (Messzeit · Mittelungen · SE-Faktor + Einschwingzeit
    + Positionierung)
  - Der SE-Faktor ist bis 3 bzw. 5 ([HB] 7-25).
  - Die Positionierzeit ist unbekannt (P2-9).
- Ein Aufruf über DCOM kann blockieren, solange PSV beschäftigt ist (z. B. modaler Dialog).
  Ob das vorkommt, ist **[ungeprüft]**.

### 5.5 Nebenläufigkeit

- **Belegt:**
  - `ExportAsync` rechnet in einem Worker-Thread ([BEM] PSV~Exporter~ExportAsync).
  - Das C++-Beispiel ruft `CoInitialize()`/`CoUninitialize()` beim Start bzw. Ende auf
    ([PFA] Examples, CplxPointAvg).
  - Externe Clients sprechen die Acquisition-Instanz per Interprozesskommunikation an
    ([BEM] ~GetApplication).
- **Nicht dokumentiert [offen]:** Threading-Modell (STA/MTA) der Server; ob PSV
  gleichzeitige Clients zulässt; Bitness der Server (Out-of-Process: egal; In-Process
  PFA-DLL: Python muss gleiche Bitness haben [Einschätzung]).
- **Einschätzung [ungeprüft]:**
  - COM-Objekte gehören zum Thread, der sie erzeugt hat (STA). Für eine GUI läuft der
    COM-Zugriff am besten in **einem** eigenen Worker-Thread mit `pythoncom.CoInitialize()`;
    die GUI spricht nur über Queues mit ihm.
  - Objekte nicht über Threads hinweg teilen, sonst marshallen
    (`CoMarshalInterThreadInterfaceInStream`).
- PolyFile und PSV dürfen dieselbe Datei nicht gleichzeitig öffnen. → Nach dem Scan
  zuerst sicherstellen, dass das Dokument in PSV geschlossen ist (z. B.
  `Document.Close()` oder Wechsel zur nächsten Messung), dann PolyFile. Wann PSV die Datei
  freigibt, ist **[offen]** (P1-9).

---

## 6 Reproduzierbarkeits-Metadaten

Ziel (U3): Jede Messung soll vollständig dokumentiert sein. Die erste Tabelle nennt, was per
COM bzw. PolyFile auslesbar ist; die Ergänzungsliste danach (Fachprüfung I5-F) führt weitere
reproduzierbarkeitskritische Größen mit ihrer Verfügbarkeit. Ergänzend kommen Git-Hash und Paketversion aus unserer
Software dazu (KONVENTIONEN).

| Information | Quelle zur Laufzeit (COM) | Quelle in der Datei (PolyFile) | Beleg |
|---|---|---|---|
| PSV-Programmversion | `Application.Version` (String) | `Version.ProgramVersionString`, `ProgramVersionMajor/Minor/Revision/Build`, `ProgramID` | [BEM] PSV~Application~Version; POLYFILELib~Version |
| Dateiformat-Version, Dateityp | – | `Version.FileVersion` (hex, 0x860 = 8.6), `Version.FileID` (`PTCFileID`), `PolyFile.CurrentFileVersionNumber` | [BEM] POLYFILELib~Version~FileVersion, ~FileID |
| Zeitpunkt der Messung | – | `Version.FileTime` (Date, „time of measurement“); Zeitzone **[offen]** | [BEM] POLYFILELib~Version~FileTime |
| Titel, Autor, Kommentar | (Speichern-Dialog der GUI, [HB] 8-3/10-9) | `SummaryInfo.Title/Author/Comments` (rw) | [BEM] POLYFILELib~SummaryInfo |
| Meldungen während der Messung | Event `MessageOccurred`; Ereignisanzeige | `SummaryInfo.Subject` | [BEM] POLYFILELib~SummaryInfo~Subject; [HB] 2-24 |
| Erfassungseinstellungen komplett | `Acquisition.ActiveProperties` (alle Gruppen), `ModeProperties` | `Infos.AcquisitionInfoModes.ActiveMode/ActiveProperties` (Messdateien enthalten nur den aktiven Modus) | [BEM] POLYFILELib~AcquisitionInfoModes |
| Einstellungen als Datei | `Settings.Save(snapshot.set)` | Messdatei selbst ist als Settings-Quelle ladbar | [BEM] PSV~Settings~Save, ~Load |
| Vibrometer-Einstellungen (Messbereich, Filter) | `VibrometersProperties(1).VibControllerSettings` → `QuantitySettings.Range`, `ControllerSettings.Save()` (XML, Format undokumentiert) | über `AcquisitionInfoModes.ActiveProperties.VibrometersProperties` (Beispiel Laserwellenlänge) | [BEM] Polytec_IO_VibInterfaces~ControllerSettings~Save; Access to General Information |
| Messbereich je Punkt | – | `MeasPoint.VibrometerRange` (bei AutoRange) | [BEM] POLYFILELib~MeasPoint~VibrometerRange |
| Hardware | `Infos.Hardware` | `Infos.Hardware`: `AcqBoard`, `FrontEnd`, Firmware-Versionen, `SensorHeadNames/SerialNumbers/Versions`, `CoherenceOptimizerVersions`, `GeneratorType`, `TedsSensors` | [BEM] PSV~HardwareAcq; POLYFILELib~Hardware |
| Sensorköpfe | `SensorHeadInfo.SerialNumber`, `FirmwareVersion`, `LaserWavelength` (nm), `LaserPower` (mW) | (über VibControllerSettings) | [BEM] Polytec_IO_VibInterfaces~SensorHeadInfo |
| Scankopf | `Infos.ScanHeadDevicesInfo.ScanHeadName/Type` | `Infos.ScanHeadDevicesInfo` | [BEM] PSV~ScanHeadDevicesInfoAcq; POLYFILELib~ScanHeadDevicesInfo |
| 3D-Abgleich-Qualität | `Infos.Alignments.Alignments3D(i)`: `Valid`, `CurrentQuality` (m), `TargetQuality` (m), `PositionUncertainty` (m), `AngleUncertainty` (rad), `GetScanHeadPosition` | `Infos.Alignments` gleich | [BEM] POLYALIGNMENTLib~Alignment3D |
| 2D-Abgleich | `Alignment2D.Valid`, `ScanHeadDistance` (m) | gleich | [BEM] POLYALIGNMENTLib~Alignment2D |
| Scanpunkte, Geometrie | `Infos.MeasPoints` (Koordinaten, Labels, GeometryStatus) | gleich + `Elements` | [BEM] POLYFILELib~MeasPoint, ~MeasPoints |
| Scanstatus je Punkt | (Events: Punkt gemessen) | `MeasPoint.ScanStatus`, `DataPoints.GetScanStatus(signal)` | [BEM] POLYFILELib~DataPoints~GetScanStatus |
| Mittelungen je Punkt, Rauschindikator | – | `MeasPoint.AverageCount`, `Sigma`, `MinSigma`, `MeasPoints.AverageSigma` | [BEM] POLYFILELib~MeasPoint~AverageCount, ~Sigma |
| Fokus | `MeasPoint.FocusValues/FocusStatus` | gleich | [BEM] POLYFILELib~MeasPoint~FocusStatus |
| Generator, Signalform | `GeneratorsProperties(1)`: `Amplitude` (V), `Offset`, `SteadyStateTime`, `Waveform` + Parameter | `AcquisitionInfoModes.ActiveProperties.GeneratorsProperties(1).Waveform` | [BEM] POLYPROPERTIESLib~GeneratorAcqPropertiesContainer, Beispiel |
| Kanalkalibrierung | `ChannelAcqProperties.Calibration`, `Unit`, `InputRange`, `Quantity`, `SignalDelay`, `WindowFunction` | Container gleich | [BEM] PSV~ChannelAcqProperties |
| Aussteuerung je Kanal vor dem Scan | `GetSignalAmplitudes([])` (% des Maximalpegels; Aussteuerung vor der Koordinatentransformation) | – | [BEM] PSV~Acquisition~GetSignalAmplitudes; [HB] 4.1.2.2 (I5-F) |
| Optischer Signalpegel des Lasers je Kopf (andere Größe als die Aussteuerung) | `Infos.Vibrometers(1).Controllers(0).SensorHeads(0).SignalLevel` (%) | – | [BEM] Access to General Information; Polytec_IO_VibInterfaces~ISensorHead~SignalLevel |
| Videobild | `ExportVideoSnapshotEx` | `Infos.VideoBitmap` | [BEM] POLYFILELib~VideoBitmap |
| Lizenzierte Optionen, Seriennummer PSV | **nicht per COM belegt**; GUI: Hilfe > PSV Info > Optionen | – | [HB] 2-28 |
| Dateiinformation als Text | **nicht per COM belegt**; GUI: Datei > Info > ASCII-Export (`ScanInfo.txt`) | – | [HB] 10-2 |

### Ergänzungsliste (nach Fachprüfung I5-F, M3)

Verfügbarkeit: **COM** = per COM zur Laufzeit lesbar, **Datei** = per PolyFile/Messdatei
lesbar, **nein** = nur manuelles Protokoll, **[U]** = in der Doku nicht belegt (entspricht
[ungeprüft]/[offen]). Spalte „Warum“: I2 §2.3 bzw. Plausibilitätskriterium P1–P17 aus I2. Belege
mit „(I5-F)“ stammen aus der Fachprüfung und sind nicht erneut nachgeprüft.

| Größe | Warum | Verfügbarkeit laut Doku | Beleg |
|---|---|---|---|
| Von/Bis (`StartFrequency`, `EndFrequency`), Bandbreite, Lines; abgeleitet $f_\mathrm{Abtast}$, $\Delta f$, $t_\mathrm{Mess}$, Overlap | Frequenzachse, P5 | COM und Datei (`AcquisitionInfoModes`) | [BEM] PSV~FftAcqProperties; [HB] 7-16/7-17; 2.5 |
| Mittelungstyp und -anzahl, `AverageCount` je Punkt, SE-Modus, Speckle Tracking, `SignalEnhancement` je Kanal (`SEActive`) | effektive Mittelungszahl ([HB] 7-25), Phasenbezug | COM und Datei; je Punkt in der Datei `MeasPoint.AverageCount` | [BEM] PSV~AverageAcqProperties, ~SEAcqProperties; POLYFILELib~MeasPoint~AverageCount |
| Fensterfunktion und Parameter je Kanal, RMS-Korrekturfaktor | P6, Skalierung | COM/Datei lesbar; Parameter schreiben **[offen]** (`WindowFunctionParams` read-only, P2-13) | [BEM] PSV~ChannelAcqProperties |
| Trigger (Quelle, Flanke, Level, Pretrigger, `PhaseFromRef`) | Phasenbezug, P15 | COM und Datei | [BEM] PSV~TriggerAcqProperties |
| Referenzkanäle: `Reference`, `Active`, `Quantity`, `Calibration`, `InputRange`, Kopplung (IEPE/AC), `SignalDelay`, Kehrwert („Inv.“) | FRF-Einheit, Phase, Vorzeichen, Verzögerung | COM und Datei; „Inv.“ als Property **[U]** | [BEM] PSV~ChannelAcqProperties; [HB] 7-11/7-12 |
| `ReferencePointIndex`, `DirectionOfVibration` je Kanal | Anregungs-DOF für die Modalanalyse | COM und Datei | [BEM] PSV~ChannelAcqProperties~ReferencePointIndex |
| Generator: Signalform und Parameter, Amplitude, Offset, `SteadyStateTime`, Generatorverstärker (`GeneratorAmplifierEnabled/Factor`), Amplitudenkorrektur | Anregungsreproduzierbarkeit | COM und Datei; Verstärkerfaktor in 2.5 (Generator), in der ersten Tabelle oben fehlend | [BEM] PSV~GeneratorAcqProperties, ~FrontEndAcqProperties |
| Abschlussimpedanz des Generators (50 Ω/hochohmig) | Spannung am Shaker | **nein** (nur manuell protokollieren); Eingangsimpedanz der Karte per COM (`InputImpedance`) | [HB] 7-32 |
| Messbereich und Filter der Vibrometer, `MaxVelocityRange`, `BandwidthRange`, Trackingfilter | Reproduzierbarkeit, Dropouts | COM und Datei; XML-Format **[U]** | [BEM] Polytec_IO_VibInterfaces~QuantitySettings |
| Alignment-Details: `CoordDefinitionMode`, `Mirror`, Kopfpositionen (`GetScanHeadPosition`), `ScanHeadDistance`, Qualität je Abgleichpunkt (`Align3DPoint.Quality`) | P3, P4, Koordinatensystem | COM und Datei; in der ersten Tabelle oben nur teilweise | [BEM] POLYALIGNMENTLib~Alignment3D, ~Align3DPoint |
| Koordinatensystem der Geometrie und Importeinheit (Skalierungsfaktor) | Geometrie | Importfaktor GUI **[U]** | (I5-F) |
| Strahlgeometrie-Konditionszahl (P4) | Rauschverstärkung 3D | abgeleitet aus Kopfpositionen und Punktkoordinaten (beide COM/Datei); Zerlegungsmatrix selbst nicht dokumentiert **[U]** | (I5-F) |
| Aussteuerung je Kanal und optischer Signalpegel je Kopf (getrennt) | P16, Signalqualität | COM live (`GetSignalAmplitudes`, `SignalLevel`); Datei nur über Status und `VibrometerRange` **[U]**. H-Systeme arbeiten mit 100 % Aussteuerungsreserve, eine Anzeige über 100 % ist daher kein Clipping ([HB] 8-5, I5-F); die 30–80 %-Regel stammt aus VFC und ist für QTec **[U]** | [BEM] PSV~Acquisition~GetSignalAmplitudes; [HB] 8-5 |
| Modus und Kamera-/Zoom-Einstellungen | Alignment-Gültigkeit | nicht untersucht (2.4) | – |
| Zeitpunkt und Zeitzone der Messung; Warmlaufbeginn (30 min bzw. 120 min, KA S. 46) | P13 | `FileTime` ja, Zeitzone **[offen]**; Warmlaufbeginn **nein** | [BEM] POLYFILELib~Version~FileTime; [KA] 46 (I5-F) |
| Lizenzierte Optionen (TDD, PCA …), PSV-Seriennummer | Rahmen | **nein** (nur GUI) | [HB] 2-28 |
| Versuchsrandbedingungen: Prüflingsbezeichnung, Lagerung, Befestigung, Anregungsort und -richtung, Shaker/Hammer-Typ, Kraftsensor-Typ und -Empfindlichkeit, Oberflächenpräparation, Messabstand, Umgebungstemperatur, Messung durch Glas oder Medium | I2 §2.3, §5.1 | **nein**, nur Protokoll (`protokoll.md`, `/versuchsplanung`) | (I5-F) |
| Scanzeit, Statusverteilung, Overrange-Anteil, Anzahl Nachmessungen | P2 | Status je Punkt: Datei ja; Scanzeit/Nachmessungen **[U]**; Meldungen in `SummaryInfo.Subject` | [BEM] POLYFILELib~SummaryInfo~Subject |
| Kombinierte Dateien (`ContainedFiles`) | P14 | Datei, Einzelheiten **[U]** | [BEM] Operating on Combined Files |

**Folgerung [Einschätzung]:**
- COM/PolyFile liefert die Gerätekonfiguration; die Versuchsrandbedingungen sind manuell per
  Protokoll zu erfassen. Nicht per COM belegt sind lizenzierte Optionen, Seriennummer des
  Systems, Zeitzone von `FileTime`, Abschlussimpedanz des Generators, Warmlaufbeginn und
  alle Versuchsrandbedingungen der letzten Zeile der Liste.
- Vorschlag für eine Sidecar-Datei je Messung:
  - Hash der `.svd`
  - Snapshot der `.set`
  - JSON mit den Feldern oben
  - `ControllerSettings.Save()`-XML
  - Git-Hash und Paketversion

---

## 7 Zugriff aus Python 3.11 (pywin32)

### 7.1 Was belegt ist

- PFA liefert eigene Python-Beispiele (`band_average.py`, `calculate_fft.py`,
  `Enums.py`, Paket `examples`). Als Abhängigkeiten nennt Polytec
  `pip install -U numpy pywin32 pillow matplotlib`. `Enums.py` zeigt, „how to use COM
  Enums in the python code“ ([PFA] Examples). Der Code der Beispiele liegt nicht im
  Input (nur in der PFA-Installation).
- Laut Betreuernotiz ist der Zugriff per Python möglich ([COM] Folie 2).
- Matlab nutzt `actxserver('PolyFile.PolyFile')`, `file.Open(filename)` ([PFA-M] Folie 4).
  Das ist ein Beleg, dass Late Binding über IDispatch für PolyFile funktioniert.
- In der CHM gibt es **nur VB/WinWrap-Basic-Beispiele** (Classic und WWB.NET). C#, C++
  und Python sind nur in der Beispielbeschreibung erwähnt ([PFA] Examples). Das
  C#-Beispiel steht in [COM] Folie 12.

### 7.2 Abbildung VB/C# → pywin32 (alles **[ungeprüft]**)

| VB/C# (belegt) | pywin32 (Vorschlag, ungeprüft) | Anmerkung |
|---|---|---|
| `Dim i As New AcquisitionInstance` / `new AcquisitionInstance()` | `i = win32com.client.Dispatch("PSV.AcquisitionInstance")` (late) oder `win32com.client.gencache.EnsureDispatch("PSV.AcquisitionInstance")` (early, makepy) | Polytec empfiehlt Early Binding |
| `Set app = i.GetApplication(True, 10000)` | `app = i.GetApplication(True, 10000)` | liefert `IApplication5` |
| `acq.ScanEx(ptcScanAll, ptcScanCapsNone)` | `acq.ScanEx(c.ptcScanAll, c.ptcScanCapsNone)` mit `c = win32com.client.constants` (nach makepy) **oder** eigene `IntEnum` mit den Werten aus Abschnitt 8 | Enums aus abhängigen Typbibliotheken (POLYPROPERTIES, POLYSIGNAL …) sind evtl. erst nach eigener makepy-Generierung als Konstanten da |
| `While acq.State <> ptcAcqStateStopped : Wait 0.1 : Wend` | `while acq.State != 0: time.sleep(0.1)` plus Gesamt-Timeout | Polling ist der von Polytec gezeigte Weg |
| `props.FftProperties.Bandwidth = 5000` | `props.FftProperties.Bandwidth = 5000.0` | Properties ohne Parameter wie Attribute |
| parametrisierte Property `app.Exporter(file, type)` | `app.Exporter(file, 0)`; bei makepy u. U. `app.GetExporter(...)` | pywin32-Namensregeln für parametrisierte Properties prüfen |
| `oSignals("Velocity")`, `oInfos(ptcInfoHardware)` | `signals.Item("Velocity")`, `infos.Item(1)` bzw. `infos.Type(1)` | `Item` explizit aufrufen ist robuster |
| `For Each p In coll` | `for p in coll:` | braucht `_NewEnum`; sonst `for i in range(1, coll.Count+1): coll.Item(i)` |
| `If x Is Nothing` | `if x is None:` | typisierte Collections |
| `CoordXYZ(ByRef x, y, z)` | `x, y, z = mp.CoordXYZ()` (makepy) | ByRef-Ausgaben kommen bei Early Binding als Tupel; bei Late Binding evtl. Platzhalter nötig |
| `GetMinMaxFrequencyRange(min, max)` | `fmin, fmax = v.GetMinMaxFrequencyRange()` | wie oben |
| `Data = dp.GetData(disp, 0)` (Single()) | `data = np.asarray(dp.GetData(disp, 0), dtype=np.float32)` | SAFEARRAY → Tupel aus Python-floats |
| `dp.SetData(sig, 1, data)` (Single()) | `VARIANT(pythoncom.VT_ARRAY \| pythoncom.VT_R4, list(data))` | sonst wird VT_R8 übergeben |
| `Set oContained = poly.ContainedFiles(1).File` (Cast auf Default-Interface) | `win32com.client.CastTo(obj, "PolyFile")` bzw. `Dispatch(obj._oleobj_.QueryInterface(IID, pythoncom.IID_IDispatch))` | Cast IApplication5 → Application für `Exporter` |
| `Dim WithEvents oAcq As Acquisition` | `win32com.client.DispatchWithEvents(acq, Handler)` mit `def OnScanStateChanged(self, ScanState, ScanPoint)` und `pythoncom.PumpWaitingMessages()` in einer Schleife | Events brauchen eine Nachrichtenschleife im STA-Thread |
| `MessageOccurred(…, ByRef pVal)` | Handler gibt den Antwortwert zurück (`return 6` für Yes) | pywin32-Konvention für ByRef in Events |
| `New ExportParameters`, `New SignalDescription`, `New DigitalFilterNone` | über makepy-Modul `mod.ExportParameters()` (CLSID aus der Typbibliothek) | ProgID nicht dokumentiert |
| `New WaveformPeriodicChirp` | `Dispatch("PolyWaveforms.WaveformPeriodicChirp")` | ProgID belegt |
| `Version.FileTime` (Date) | `pywintypes.datetime`, in `datetime` umwandeln | Zeitzone prüfen |
| `CoInitialize()` (C++) | `pythoncom.CoInitialize()` je Thread, `CoUninitialize()` am Ende | im Hauptthread erledigt pywin32 das beim Import |

### 7.3 Weitere Punkte und Empfehlungen [Einschätzung]

- **pywin32 nur im Adapter importieren.** Unter Linux und in der Cloud ist es nicht
  importierbar. Tests gegen den Simulator laufen ohne pywin32 (KONVENTIONEN).
- **Enums:** Eine eigene, im Simulator nutzbare `IntEnum`-Spiegelung der Werte aus
  Abschnitt 8 ist testbar und unabhängig von makepy. Beim Verbinden gleicht ein Test am
  Gerät sie gegen `win32com.client.constants` ab (P1-4).
- **Bitness:** Out-of-Process-Server (`LocalServer32`) gehen mit 32- und 64-Bit-Python;
  In-Process-Server (`InprocServer32`, vermutlich PFA) brauchen gleiche Bitness.
  Prüfen per Registry (P1-2).
  - Die PFA-Pfade liegen unter `C:\Program Files\…` ([PFA-M] Folie 3). Das deutet auf
    eine 64-Bit-Installation hin, ist aber kein Beweis.
  - Polytec Update heißt `Setup32.exe` ([HB] 2-4); das betrifft nur das Update-Werkzeug.
- **Installation:** Python, uv und pywin32 auf dem Messrechner fallen unter „nicht von
  Polytec angebotene Komponenten“ ([KA] 1-4). → F4 klären.
- **Kein DCOM über das Netz** im ersten Stand ([COM] Folie 13).
- **Robustheit:** Jeder Schreibzugriff wird zurückgelesen (Einrasten, stilles Anpassen).
  Jeder Wartevorgang braucht einen Timeout. Jede COM-Exception wird mit Kontext
  weitergereicht.
- **Startpunkt aus PSV:** Über *Werkzeuge > Externe Werkzeuge* lassen sich eigene
  ausführbare Dateien ins PSV-Menü hängen ([PSVH] 2_7). Damit könnte das Paket aus PSV
  heraus gestartet werden. Optional.

---

## 8 Enum-Referenz

Alle Werte stammen aus den Enumerationsthemen (Ordner der Textfassung in Klammern).

**Ablauf (PSV)**

| Enum | Werte | Beleg |
|---|---|---|
| `PTCAcqState` | Stopped 0, Single 1, Continuous 2, ScanAll 3, ScanContinue 4, ScanRemeasure 5, AutoFocus 6, PathLength 7 | [BEM] PSV~PTCAcqState |
| `PTCAcqStartMode` | Single 0, Continuous 1 | [BEM] PSV~PTCAcqStartMode |
| `PTCScanMode` | All 0, Continue 1, Remeasure 2, RemeasureAutoRange 3, RemeasureFile 4 | [BEM] PSV~PTCScanMode |
| `PTCScanCaps` (Bitmaske) | None 0, UseAssignedFocusValuesDuringScan 1, VideoTriangulation 2, VideoTriangulationFast 4, AutoFocusDuringScan 8, AsynchronousScanEvent 16 | [BEM] PSV~PTCScanCaps |
| `PTCScanState` | BeginScan 0, EndScan 1, BeginScanPoint 2, EndScanPoint 3 | [BEM] PSV~PTCScanState |
| `PTCSettings` (Bitmaske) | None 0, Acquisition 2, Alignment 4, Camera 64, CameraAndAlignment 68, Windows 128, APS 312, 2DAlignment 512, 3DAlignment 1024, All 65535 | [BEM] PSV~PTCSettings |
| `PTCApplicationMode` | Normal 0, Acquisition 1, Presentation 2 | [BEM] PSV~PTCApplicationMode |
| `PTCExportType` | UniversalFile 0, MEScope 1, AsamOdsAtfx 2 | [BEM] PSV~PTCExportType |
| `PTCMessageStyle` | OK 0, OKCANCEL 1, ABORTRETRYIGNORE 2, YESNOCANCEL 3, YESNO 4, RETRYCANCEL 5, ICONHAND 16, ICONQUESTION 32, ICONEXCLAMATION 48, ICONASTERISK 64 | [BEM] PSV~PTCMessageStyle |
| `PTCMessageAnswer` | Ok 1, Cancel 2, Abort 3, Retry 4, Ignore 5, Yes 6, No 7 | [BEM] PSV~PTCMessageAnswer |
| `PTCWarningLevel` | All 0, Warnings 1, Errors 2, None 3 | [BEM] PSV~PTCWarningLevel |
| `PTCGeometryScanCaps` | None 0, Selected 1, RefineWithAutoFocus 2 | [BEM] PSV~PTCGeometryScanCaps |
| `PTCAssignFocusAutomaticallyCaps` | None 0, Selected 1 | [BEM] PSV~PTCAssignFocusAutomaticallyCaps |
| `PTCSnapshotType` | MainCamera 0, AuxCamera 1, OverviewImage 2 | [BEM] PSV~PTCSnapshotType |
| `PTCDigitalPort` | Gate 0, Out1 1, In1 2 | [BEM] PSV~PTCDigitalPort |

**Eigenschaften (POLYPROPERTIESLib, PolyScopeLib, PolyMathLib)**

| Enum | Werte | Beleg |
|---|---|---|
| `PTCAcqMode` | Time 0, Fft 1, ZoomFft 2, MultiFrame 3, FastScan 4, OrderTracking 5, IQ 6, Inplane 7 | [BEM] POLYPROPERTIESLib~PTCAcqMode |
| `PTCAcqPropertiesType` | General 0, Average 1, Channels 2, FastScans 3, Fft 4, Generators 5, MultiFrame 6, SignalEnhancement 8, Time 9, Trigger 10, Vibrometers 11, ZoomFft 12, FrontEnd 14 | [BEM] POLYPROPERTIESLib~PTCAcqPropertiesType |
| `PTCAverageType` | Off 0, Magnitude 1, Complex 2, Time 3, Peakhold 4 | [BEM] POLYPROPERTIESLib~PTCAverageType |
| `PTCSignalEnhancementMode` | Fast 0, FastStandard 1, Standard 2, StandardBest 3, Best 4 | [BEM] POLYPROPERTIESLib~PTCSignalEnhancementMode |
| `PTCVibrationDirection` | ZPos 0, ZNeg 1, XPos 2, XNeg 3, YPos 4, YNeg 5, 3DVector 6 | [BEM] POLYPROPERTIESLib~PTCVibrationDirection |
| `PTCChannelType` | Analog 0, AnalogFixed 1, FringeCounter 2, Logical 3, Modulated 4, DigitalVib 5, MultiPointVib 6, LoopBack 7, AnalogHF 8, Encoder 9 | [BEM] POLYPROPERTIESLib~PTCChannelType |
| `PTCMultiFrameMode` | Automatic 0, Regular 1, Manual 2 | [BEM] POLYPROPERTIESLib~PTCMultiFrameMode |
| `PTCTriggerSource` | Off 0, External 1, Analog 2, Internal 3 | [BEM] PolyScopeLib~PTCTriggerSource |
| `PTCTriggerEdge` | Rising 0, Falling 1 | [BEM] PolyScopeLib~PTCTriggerEdge |
| `PTCInputCoupling` | AC 0, DC 1, Unknown 2 | [BEM] PolyScopeLib~PTCInputCoupling |
| `PTCWindowFunction` | Rectangle 0, Bartlett 1, BlackmanHarris 2, Exponential 3, FlatTop 4, Force 5, Hamming 6, Hanning 7, TaperedHanning 8 | [BEM] PolyMathLib~PTCWindowFunction |

**Signale (POLYSIGNALLib)**

| Enum | Werte | Beleg |
|---|---|---|
| `PTCDomainType` | NotAvail 0, Time 1, AngleSync 2, Spectrum 3, 3rdOctave 4, OrderSpectrum 5, RMS 6 | [BEM] POLYSIGNALLib~PTCDomainType |
| `PTCDisplayType` | NotAvail 0, Mag 1, MagPhase 2, MagDb 3, MagDbPhase 4, MagDbA 5, Phase 6, Real 7, Imag 8, RealImag 9, Nyquist 10, InstVal 11, Samples 12, IQFitted 13, MagPhaseRad 14, MagDbPhaseRad 15 | [BEM] POLYSIGNALLib~PTCDisplayType |
| `PTCSignalBuildFlags` | Nothing 0, DomainTime 1, DomainSpectrum 2, DomainRms 4, DomainAngleSync 8, DomainOrderSpectrum 16, Domain3rdOctave 32, DomainAll 63, ChannelOriginal 256, ChannelUser 512, Channel3d 1024, ChannelXYZ 2048, DisplayComplex 65536, DisplayNyquist 131072, DisplayInstVal 262144, DisplayPhase 524288, BandData3d 591679, BandDataXYZ 592703, PointData3d 722751, PointDataXYZ 723775 | [BEM] POLYSIGNALLib~PTCSignalBuildFlags |
| `PTCChannelCapsType` | None 0, Scalar 1, Vector 2, User 4, X 8, Y 16, Z 32, 3d1d 64, Response 128 | [BEM] POLYSIGNALLib~PTCChannelCapsType |
| `PTCDataType` | Unknown 0, Point 1, Average 2, Band 3 | [BEM] POLYSIGNALLib~PTCDataType |
| `PTCInfoType` | Acquisition 0, Hardware 1, Elements 2, Video 3, APS 4, MeasPoints 5, Profiles 6, CameraSettings 7, ScanHead 8, VideoBitmap 9, DbReferences 11, ScanHeadDevices 12, Alignments 13, VideoMapping 14, PositioningStage 15, Vibrometers 16, PositionDevice 17, MeasurementLocations 18, Textures 19, Spectrogram 20 | [BEM] POLYSIGNALLib~PTCInfoType |
| `PTCFunctionType` (Auszug) | Unknown 0, TimeResponse 1, AutoSpectrum 2, CrossSpectrum 3, FrequencyResponseFunction 4, Transmissibility 5, Coherence 6, Spectrum 12, ImpulseResponse 100, FRF H1 300, FRF H2 301, FRF PCA H1 302, PCA PrincipalInputs 303, PCA VirtualCoherences 304, Band 306 | [BEM] POLYSIGNALLib~PTCFunctionType |
| `PTCPhysicalQuantity` (Auszug) | Acceleration 0, Angle 1, Displacement 4, Force 6, Time 22, Frequency 23, Velocity 13, Voltage 14 | [BEM] POLYSIGNALLib~PTCPhysicalQuantity |
| `PTCFunctionAtNodeDirection` | ScalarDir 0, ±X/Y/Z-Translation ±1/±2/±3, ±X/Y/Z-Rotation ±4/±5/±6, Vector 7 | [BEM] POLYSIGNALLib~PTCFunctionAtNodeDirection |

**Datei (POLYFILELib)**

| Enum | Werte | Beleg |
|---|---|---|
| `PTCScanStatus` (Bitmaske) | None 0 (nicht gemessen), Valid 1, Optimal 2, Overrange 4, Invalidated 8, Disabled 16, InvalidFrames 32, NotReachable 64, Hidden 128, VideoTriangulationFailed 256, Interpolate 512, InterpolationFailed 1024, AssignedChannel1D 2048, AssignedChannel3D 4096, AssignedSensor 8192 | [BEM] POLYFILELib~PTCScanStatus |
| `PTCGeometryStatus` (Bitmaske) | None 0, Valid 1, Measured 4, Imported 8, Triangulation 16, Interpolated 32, Modified 64, TooBright 128, TooDark 256, Failed 512, OptimalMeasured 1024, Calculated3dFrom2d 2048, Calculated2dFrom3d 4096, VideoTriangulated 8192, Calculated3dFrom2dAndDistance 16384 | [BEM] POLYFILELib~PTCGeometryStatus |
| `PTCFocusStatus` (Bitmaske) | None 0, Valid 1, Manual 2, Fast 4, Best 8, Interpolated 16, Failed 32, Calculated 64, Auto 128 | [BEM] POLYFILELib~PTCFocusStatus |
| `PTCFileID` | Unknown 0, VibSoftSettings 1, VibSoftFile 2, PSVSettings 3, PSVFile 4, PMAFile 5, SigProFile 6, CombinedFile 7, MPVSettings 8, MPVFile 9, SCDFile 10, SCSFile 11 | [BEM] POLYFILELib~PTCFileID |
| `PTCCreateFlags` | None 0, Always 1 | [BEM] POLYFILELib~PTCCreateFlags |
| `PTCSaveAs` | All 0, Bands 1, SinglePoint 2, AverageSpectrum 3, TypeInfos 4, TypeBands 8, TypeSinglePoint 16, TypeSinglePointUser 32, TypeAverageSpectrum 64, TypeAllNoUser 92, TypeAverageSpectrumUser 128, TypeBandsUser 256, TypeAllNoOriginal 420, TypeAllNoSinglePoint 460, TypeAll 508 | [BEM] POLYFILELib~PTCSaveAs |

**Generator und Hardware**

| Enum | Werte | Beleg |
|---|---|---|
| `PTCWaveformType` | Sine 0, Square 1, Triangle 2, Ramp 3, Sweep 4, BurstChirp 5, BurstRandom 6, PeriodicChirp 7, PseudoRandom 8, WhiteNoise 9, UserDefined 10, Pulse 11, MultiCarrierCW 12, SteppedSineSweep 13 | [BEM] POLYWAVEFORMSLib~PTCWaveformType |
| `PTCGeneratorActiveChannelType` | Channel1 1, Channel2 2, Channel3 4, Channel4 8, Channel5 16, All 15, AllPsv7003D 31 | [BEM] POLYSIGNALGENERATORLib~PTCGeneratorActiveChannelType |
| `PTCFrontEndType` (Auszug PSV-F-600) | PSV_F_600 123, PSV_F_600_3D 124, PSV_F_600_3D_1D 125, PSV_F_600_1D 126, PSV_F_600_V 127, PSV_F_600_3D_V 128, PSV_F_600_3D_1D_V 129, PSV_F_600_1D_V 130 | [BEM] PolyFrontEndLib~PTCFrontEndType |
| `PTCScanHeadType` (Auszug) | None 0, PSV500 17, PSV6xx 23, PSVI7xx 27; welcher Wert für PSV-I-680/690 gilt, ist **[offen]** | [BEM] PolyScanHeadLib~PTCScanHeadType |
| `PTCProgramID` | Unknown 0, VibSoft 1, PSV 2, ScannerControl 3, PMA/MSVInplane 4, TMS 5, PolyFile 6, MPV 7, VideoPanel 8 | [BEM] PolyFrontEndLib~PTCProgramID |
| `PTCCoordDefinitionMode` | Off 0, OrigPointOnAxisPointOnPlane 1, ThreePointsOnAxes 2, FreePoints 3 | [BEM] POLYALIGNMENTLib~PTCCoordDefinitionMode |
| `PTCBandType` | None 0, Entire 1, Rms 2, Time 4, Spectrum 8, 3rdOctave 16, All 65535 | [BEM] PolyBandsLib~PTCBandType |

---

## 9 Abgleich mit dem Erwartungsmanagement (U1–U7)

| Nr. | Inhalt | Per COM machbar? | Begründung, Grenzen | Risiko |
|---|---|---|---|---|
| U1 | Einarbeitung COM | ja, dokumentarisch abgeschlossen | dieses Dokument; Verhalten aus Python offen (Abschnitt 10) | gering |
| U2 | Messablauf automatisieren | **ja, belegt** für Verbinden, Settings laden, Parameter setzen (Validator), Scan starten/fortsetzen/nachmessen, Zustand überwachen, Stoppen, Speichern (automatisch), Export | Scanpunkte und 3D-Abgleich nur **eingeschränkt**: praktisch interaktiv in PSV vorbereiten und per `.set` laden (2.4); Event-Empfang aus Python offen; Meldungsdialoge als Blocker | mittel |
| U3 | Dokumentation jeder Messung | **teilweise**: Gerätekonfiguration ja, Versuchsrandbedingungen nein | Die Gerätekonfiguration kommt per COM/PolyFile (Abschnitt 6). Die Versuchsrandbedingungen (Generatorlast, Lagerung, Anregungsort, Oberflächenpräparation, Umgebung, Warmlaufbeginn, Kraftsensor-Empfindlichkeit) sind manuell per Protokoll zu erfassen. Nicht per COM belegt außerdem: lizenzierte Optionen, System-Seriennummer, Zeitzone der Messzeit, Format des Controller-XML | mittel |
| U4 | Daten nach Python, Auswertung, Visualisierung | **ja**, über PolyFile (Windows) oder UFF-Export (plattformunabhängig) | float32-Quelle; exklusiver Dateizugriff; FFT-Achse vorläufig, neuer Beleg [PFA-M] Folie 8 | gering bis mittel |
| U5 | Einfache Oberfläche | ja, indirekt | COM im Worker-Thread; Threading-Modell undokumentiert | mittel |
| U6 | Weitergehende Auswertung | **nur mit Voraussetzungen**, Einstufung je Auswertung in 9.1. Spektren, Peak-Picking und 3D-Komponenten sind ohne Zusatz machbar. Komplexe FRF (H1/H2) und Kohärenz brauchen einen aktiven Referenzkanal. Eine absolute FRF (Mobilität in (m/s)/N) und skalierte Modalparameter brauchen eine **Kraftmessung** (Kraftsensor am Referenzkanal mit Größe „Kraft“ und Kalibrierfaktor, [HB] 7-12). ODS und Phase brauchen **Referenz oder Trigger** (TM Tab. 6.1). Zeitdaten-Auswertungen brauchen den Messmodus Zeit und damit die Option **TDD** ([HB] 7-2, 7-34) | Der Messmodus Zeit braucht TDD. `SaveTimeDataForScan` setzt SE auf „Fast“; ob es ebenfalls TDD voraussetzt, ist **[offen]**. „Multi-Referenz“ mit PCA gilt nur für die Polytec-interne MIMO-Rechnung, nicht für eine externe Auswertung mehrerer Messungen. Messtechnische Bewertung durch den strukturdynamik-experte | fachlich |
| U7 | Weiteres Equipment | **teilweise**: interner/angeschlossener Generator per COM (Signalform, Amplitude, an/aus); Polytec-Positioniereinheit per `PositionDevice`; digitale Ein-/Ausgänge (Aux In/Out, `Pulse`) für einfache Synchronisation | Fremdgeräte (externer Verstärker, Shaker-Regelung, fremde Achsen) **nicht** über PSV-COM, sondern nur über eigene Treiber | offen (F6) |

### 9.1 Machbarkeit der Auswertungen aus COM/PolyFile-Daten (Fachprüfung I5-F, M4)

Legende: **machbar** = mit den belegten Daten ohne weitere Hardware; **mit Voraussetzung** = nur,
wenn die genannte Bedingung bei der Messung erfüllt war; **nicht machbar** = Daten fehlen.
Belege mit „(I5-F)“ stammen aus der Fachprüfung (TM = Theoriehandbuch, SWP/SWA = Software
Handbuch PSV).

| Auswertung | Einstufung | Begründung und Beleg |
|---|---|---|
| Spektren je Punkt (Real/Imag, Betrag), x/y/z oder Vib 3D, Einheit m/s, Amplitude 0-to-peak | machbar | `DataPoint.GetData`/`Get3DData` ([BEM] Access to Data); Skalierung TM 3-3, Matlab-Folie 9 (I5-F). Skalierung und Phasenbezug dokumentieren (4.4) |
| Peak-Picking, Eigenfrequenzen, −3-dB-Dämpfung (SDOF), FG-04 | machbar | Aus dem Betragsspektrum. Auflösung begrenzt durch $\Delta f = BW/n_\mathrm{FFT}$; Halbwertsbreite gilt für $\zeta \ll 1$ (I2 FG-04); Fenster-Scalloping beachten (I2 §3.2) |
| Integration und Differentiation (Weg, Beschleunigung) | machbar | Polytec berechnet die Größen aus der Auswahl in der Datei ([HB] 7-12); eigene Umrechnung im Frequenzbereich mit $1/(i\omega)$ möglich |
| FRF H1/H2/Kohärenz aus der Datei | mit Voraussetzung | Nur, wenn ein Referenzkanal aktiv war (Kombikanäle, SWP 3-31). Mit Spannungsreferenz in (m/s)/V, relative FRF inklusive Verstärker/Shaker; Mobilität (m/s)/N nur mit Kraftsensor, `Quantity` Kraft und Kalibrierfaktor ([HB] 7-12). Hv liefert Polytec nicht |
| ODS und Animation ($\mathrm{Re}\{A\,e^{i\omega t}\}$) | mit Voraussetzung (Referenz oder Trigger) | Phase nur mit Referenz oder Trigger (TM Tab. 6.1). Besser deterministische Anregung mit Komplexmittelung, bei stochastischer Anregung Referenz und H1 (TM 3-6). Gültigen 3D-Abgleich und Punktstatus filtern. ODS ist nicht gleich Eigenform. Das Punktmittel (Betragsmittel) ist für ODS nicht geeignet |
| Modalanalyse: Eigenfrequenzen, Dämpfung, unskalierte Formen (SDOF/MDOF, LSCF/PolyMAX, MAC) | mit Voraussetzung (FRF-Spalte) | Eine FRF-Spalte (fester Anregungspunkt, alle Messpunkte, 3 Komponenten) ist verfügbar. Mit Spannungsreferenz sind Frequenzen und Formen näherungsweise nutzbar, Genauigkeit durch Shaker-Struktur-Kopplung eingeschränkt [Einschätzung]. Eigene MDOF-Schätzung ist extern in Python möglich (PSV hat nur SDOF-Peak-Fit, SWP 3-14) |
| Skalierte Modalparameter (Modalmasse, Residuen), absolute FRF | mit Voraussetzung (**Kraftmessung**) | Braucht Kraftsensor am Referenzkanal mit Kalibrierfaktor und Referenz-DOF (`ReferencePointIndex`, `DirectionOfVibration`). Ohne Kraft nicht machbar |
| Mehrfachanregung (MIMO), nahe beieinander liegende Moden sicher trennen | mit Voraussetzung | Polytec-intern PCA-Option ([HB] 7-7; TM Kap. 8); PSV unterstützt derzeit nur einen Generator ([BEM] PSV~Acquisition~GeneratorsOn). Extern: mehrere Messläufe mit verschiedenen Anregungspunkten, Gruppierung nur über eigene Metadaten [Einschätzung] |
| Plausibilität P1 Kohärenz | mit Voraussetzung | Referenzkanal und Kombikanal nötig |
| P2 Status, P3 Alignment-Qualität, P5 Einstellungskonsistenz, P6 Signal-Fenster-Matrix, P8 Sweep-Parameter, P11 Auflösungsregel, P14 Stitching, P15 Phasenreferenz | machbar | Aus Status, Alignment, Properties und Metadaten (Abschnitt 6); P11 aus $\Delta f$ und der −3-dB-Breite; P14 bei kombinierten Dateien **[ungeprüft]** |
| P4 Strahlgeometrie (Konditionszahl) | machbar (abgeleitet) | Aus Kopf- und Punktkoordinaten; die Polytec-Zerlegungsmatrix ist nicht belegt |
| P9 Wiederholbarkeit, P10 Nichtlinearität | machbar | Zwei oder mehr Messdateien; `Generator.Amplitude` per COM stufbar |
| P13 Aufwärmzeit | mit Voraussetzung | Zeitstempel `FileTime` plus manuelles Protokoll (Zeitzone **[offen]**) |
| P16 Aussteuerung | mit Voraussetzung | Nur live (`GetSignalAmplitudes`) bzw. über `VibrometerRange`/Overrange-Status; 30–80 % nicht für QTec belegt |
| P17 Niederfrequenz-Check | machbar | Aus dem Spektrum, nur bei Fußpunktanregung |
| P7 Burst-Abklingen, P12 Parseval-Test, logarithmisches Dekrement, Hammer-Kraftfenster nachträglich, eigene Welch-/H1-Schätzung, Neu-Fensterung | mit Voraussetzung (**Zeitdaten, TDD**) | Der Modus Zeit braucht die Option TDD ([HB] 7-2, 7-34). `SaveTimeDataForScan` setzt SE auf „Fast“; Lizenzbedarf **[offen]**. Ohne Zeitdaten nicht machbar, da Fenster und Mittelung bei der Erfassung festgelegt wurden. P12 nur gegen die Polytec-RMS-Domain wäre kein unabhängiger Zeitbereichstest. Speicher: Dateigröße > Kanäle · Abtastwerte · 4 Byte ([HB] 7-34) |
| Impulshammer-Auswertung | mit Voraussetzung | Trigger extern/analog, IEPE-Kraftkanal, Kraft- und Exponentialfenster (F04 S. 18–23, I5-F); Fensterparameter per COM **[offen]** (P2-13); Hammer nicht über den PSV-Generator |

**Weitere Risiken und Grenzen**
- **Versionsabhängigkeit:** Die Hilfe beschreibt mindestens PSV 10.4, die Folien zeigen
  10.2.1.1, das Handbuch 10.1. Neuere Mitglieder wie die Validatoren könnten fehlen.
  → Versionsprüfung beim Verbinden.
- **Installation auf dem Messrechner:** [KA] 1-4 verlangt Rücksprache mit Polytec (F4).
- **Kein Test ohne Gerät:** Simulator ist Pflicht (KONVENTIONEN). Er muss die
  Zustandsmaschine, Event-Folge, nicht fortlaufende Punktreihenfolge, Einrasten von
  Parametern, verschränkte float32-Daten und Fehler nachbilden.
- **Rohdaten:** PSV und PFA können Dateien überschreiben (`Create` mit
  `ptcCreateAlways`, Schreib-Beispiele). Der Adapter muss Zielpfade vorher prüfen.
- **Sicherheit:** Laser- und Generator-Aktionen nur bewusst und mit Bestätigung. Service-
  Methoden des Scankopfs nie aufrufen (2.7).
- **Benutzerinteraktion:** Ein Benutzer kann parallel in der PSV-GUI arbeiten. Die Doku
  sagt nichts dazu, ob das stört. **[offen]**

---

## 10 Prüfliste für den Messrechner

Grundlage für Prüfanleitung bzw. Erkundungsskript. Reihenfolge nach Risiko. Erst lesen,
dann schreiben, zuletzt Hardware bewegen bzw. anregen. Ein Punkt gilt erst als bestätigt,
wenn der Nutzer das Ergebnis meldet (Ablauf G).

### P1 – blockierend für den Prototyp (nur lesend bzw. ungefährlich)

| ID | Prüfung | Erwartung/Beleg | Ergebnis festhalten |
|---|---|---|---|
| P1-1 | Darf Python 3.11 + pywin32 (+ uv) installiert werden? Welche Bitness hat Windows? | [KA] 1-4, F4 | Freigabe, Version |
| P1-2 | Registry: `HKCR\PSV.AcquisitionInstance`, `PSV.PresentationInstance`, `PSV.Application`, `PolyFile.PolyFile`, `PolyWaveforms.WaveformSine` → CLSID → `LocalServer32` oder `InprocServer32`, Pfad (Program Files vs. x86) | ProgIDs aus 1.3 | Servertyp, Pfad, Bitness |
| P1-3 | PSV-Version (Hilfe > PSV Info), installierte Optionen (TDD, PCA, ExpME, ExpASAM, APS Professional, Generator), PFA-Version | [HB] 2-28; F5 | Screenshot/Text |
| P1-4 | `python -c "import win32com.client"`; makepy für PSV, PolyFile und abhängige Typbibliotheken; Liste der Typbibliotheken (`win32com.client.selecttlb.EnumTlbs()`); Vergleich `constants` ↔ Abschnitt 8 | 1.2, 7.2 | Abweichungen |
| P1-5 | Verbinden: `Dispatch("PSV.AcquisitionInstance")`, `IsRunning`, `GetApplication(True, 30000)`; Dauer messen; `Version`, `Mode`, `SuppressMessagesForAutomation`, `WarningLevel`; Existenz von `FftAcqPropertiesValidator` | 3.1, 2.6 | Werte, Dauer |
| P1-6 | Nur lesen: `Acquisition.State`, `Mode`, alle `ActiveProperties`-Gruppen mit `Has…`, `Infos.Hardware` (FrontEnd-Typ), `ScanHeadDevicesInfo.ScanHeadType`, `Vibrometers.Count`, `Infos.MeasPoints.Count`, `Alignments3D` (Count, Valid, CurrentQuality) | 2.2–2.8 | Wertetabelle |
| P1-7 | Einzelmessung `Start(ptcAcqStartSingle)` ohne Generator, Polling bis Stopped mit Timeout; danach `GetSignalAmplitudes` | 3.3 | Dauer, Zustände |
| P1-8 | Meldungsverhalten: Was passiert bei einer typischen Meldung (z. B. ungültiger `ScanFileName`-Pfad, vorhandene Zieldatei) mit `SuppressMessagesForAutomation=True`? Blockiert ein Dialog? Exception? | 5.1 | Verhalten, Text |
| P1-9 | Kleiner Scan (z. B. 3×3 Punkte, vorbereitete `.set`): `ScanFileName`, `ScanEx(ptcScanAll, ptcScanCapsNone)`, Polling; danach Datei in PSV schließen; `PolyFile.Open` mit `ReadOnly=True`; Sharing Violation wann? | 3.4, 4.2 | Dauer, Freigabezeitpunkt |
| P1-10 | Datenformat an dieser Datei: Länge von `GetData` (Real&Imag), `XAxis.Min/Max/MaxCount`, `GetMidX(0)`, Vergleich mit `SampleResolution`/`Bandwidth`/`Lines`; Einheiten aus `YAxis.Unit`; 3D-Kanäle Vib X/Y/Z; Zeitstempel `Version.FileTime`; zusätzlich UFF-Export derselben Datei als Golden File ablegen | 4.4; KONVENTIONEN „vorläufig“ | Werte, Dateien |
| P1-11 | **XAxis und Datenlänge bei Von/Bis:** dieselbe Messung einmal mit Vollbereich (Von = 0, Bis = BW) und einmal mit eingeschränktem Bereich (z. B. 1000–4000 Hz bei 5000 Hz/400 Linien, erwartet 241 Linien, falls die Datei nur den Teilbereich enthält); `GetData`-Länge, `XAxis.Min/Max/MaxCount`, Bin-Konvention (Mitte oder Kante), DC-Linie; Abgleich `SampleFrequency`/`SampleResolution` mit 2,5·BW bzw. $BW/n_\mathrm{FFT}$ (Nicht-M-System?) | 2.5, 4.4 (M1) | Datenlängen, Achsenwerte |
| P1-12 | **Vorzeichen und Betrag 3D:** Vorzeichen der X/Y/Z-Komponenten gegen die Achsen des 3D-Koordinatensystems (z. B. definierte Bewegung in +X) und Vorzeichen der Kanäle je Kopf (1D, Richtung Scankopf); ob „Vib 3D“-Betrag/Phase-Displays den Vektorbetrag oder je Komponente liefern, im Vergleich zu $\sqrt{A_x^2+A_y^2+A_z^2}$ aus Real&Imag; Skalierung 0-to-peak gegen bekannte Anregung | 4.4 (m2, M2) | Vorzeichen, Zahlenwerte |

### P2 – wichtig für die Architektur

| ID | Prüfung | Bezug |
|---|---|---|
| P2-1 | Events per `DispatchWithEvents`: `ScanStateChanged`, `AcqStateChanged` mit und ohne `ptcScanCapsAsynchronousScanEvent`; braucht es `PumpWaitingMessages`? | 5.3 |
| P2-2 | `MessageOccurred` empfangen und Antwort über Rückgabewert setzen | 5.1 |
| P2-3 | `Settings.Load` mit Teilmasken (Acquisition, APS, 3DAlignment, All); Verhalten bei fremder `.set`; `Settings.Save` | 2.4 |
| P2-4 | Parameter setzen: FFT über Validator (Bandbreite, Linien, Bereich), Mittelung Typ/Anzahl (auch Count < 3), Trigger; Zurücklesen; Exception-Text bei ungültigen Werten | 2.5, 2.6 |
| P2-5 | ByRef-Ausgaben (`CoordXYZ`, `GetMinMaxFrequencyRange`) mit Early und Late Binding | 7.2 |
| P2-6 | Label vs. Index: Punkt-Labels in einer Testdatei ändern; prüfen, was `ScanStateChanged` liefert und was `ReferencePointIndex` bedeutet | 1.7 |
| P2-7 | Exporter: Cast `IApplication5` → `Application`; `New ExportParameters` aus Python; UFF-Export synchron | 3.7, 1.5 |
| P2-8 | Metadaten: `SummaryInfo.Subject/Title/Author/Comments` nach einem Scan; `ControllerSettings.Save()`; `MeasPoint.AverageCount/Sigma/VibrometerRange`; Zeitzone `FileTime` | 6 |
| P2-9 | Zeitbedarf je Punkt (Positionieren, Einschwingen) für Timeout-Modell; Stop mitten im Scan, danach `ptcScanContinue`; Verhalten `ptcScanRemeasure` | 3.4, 5.4 |
| P2-10 | Threading: Verbindung und Scan aus einem Worker-Thread (`CoInitialize`), GUI-Thread blockiert nicht | 5.5 |
| P2-11 | Verhalten bei vorhandenem `ScanFileName` (Überschreiben? Rückfrage?) | 3.4 |
| P2-12 | Typ und Indexbasis von `ChannelsProperties.Item`, `Alignments3D.Item`; Punktreihenfolge im Scan | 1.6 |
| P2-13 | **Fensterparameter per COM:** `ChannelAcqProperties.WindowFunctionParams` ist read-only; Setzbarkeit der Parameter von Tapered Hanning, Kraft- und Exponentialfenster (z. B. über den Properties-Container) prüfen; `WindowFunction` und RMS-Korrekturfaktor zurücklesen | 2.5 (m10) |
| P2-14 | Phasengültigkeit: Messung mit Referenz, mit Trigger ohne Referenz und ohne beides; `PhaseFromRef`; Phase relativ zu Referenz bzw. Fensteranfang prüfen; Kombikanäle (`Vib & Ref n`) und Signalnamen/Einheiten über `SignalDescription` | 4.3, 4.4 (M2, m3) |

### P3 – Ausbau und Komfort

| ID | Prüfung | Bezug |
|---|---|---|
| P3-1 | Generator: `GeneratorsOn`, Signalform per `Dispatch("PolyWaveforms.WaveformPeriodicChirp")` zuweisen, `Amplitude` sehr klein, zunächst **ohne angeschlossenen Shaker/Verstärker** | 2.5, U7 |
| P3-2 | `PositionDevice` vorhanden? `DigitalPorts` (Aux In/Out) | 2.8, U7 |
| P3-3 | Lesedauer `GetData` je Punkt vs. `DataPointReader` bei großem Scan | 4.7 |
| P3-4 | Laser/Fokus: `GetLaserOn`, `SetLaserOn(-1, False, True)`, `AutoFocusLaser`, `AssignFocusAutomatically` | 2.1 |
| P3-5 | Gleichzeitige Bedienung der PSV-GUI während der Automation; `QuitEx` | 9 |
| P3-6 | **Lizenz `SaveTimeDataForScan`:** Setzen mit und ohne Option TDD (Fehlermeldung/Exception?); falls möglich Zeitdaten in `.svd` lesbar (`GetDataSection` mit `Average`)? Welche Optionen am Messrechner installiert sind (TDD, PCA …) | 2.5, 4.4, U6 |
| P3-7 | Fehler provozieren (ungültiger Pfad, ungültige Bandbreite, PolyFile auf offene Datei) und HRESULT sowie `excepinfo` protokollieren | 5.2 |
| P3-8 | Start des Pakets aus PSV über *Werkzeuge > Externe Werkzeuge* | 7.3 |

---

## 11 Quellenverzeichnis

| Kürzel | Datei (unter `Input/literatur/polytec/`) | Zitierweise | Textfassung |
|---|---|---|---|
| [BEM] | `Windows Hilfedateien/Basic Engine Manual.chm` (SHA-256 87bddc36…c33a) | CHM-Thema = Dateiname ohne `.html` | `in_progress/analysen/polytec-chm-text/basic-engine-manual/` |
| [PFA] | `Windows Hilfedateien/Polytec File Access_Object Model Reference.chm` (SHA-256 a6333106…fad) | CHM-Thema | `…/polytec-chm-text/polytec-file-access/` |
| [PSVH] | `Windows Hilfedateien/Psv_deu.chm` | Thema (z. B. `2_7.htm`, `3_7.htm`) | nicht abgelegt |
| [PRES] | `Windows Hilfedateien/PsvPres_deu.chm` | Thema (z. B. `5_2_7.htm`) | nicht abgelegt |
| [HB] | `Handbücher/Software Handbuch PSV.pdf` (Version 10.1) | gedruckte Seite (PDF-Seite) | – |
| [COM] | `06_Automatisierung_via_COM/06_Automatisierung_via_COM .pdf` (Stand 12/5/2025) | Folie | – |
| [PFA-M] | `Schulungsunterlagen/11.2 Polytec-File-Access_Matlab.pdf` (10.11.2021) | Folie | – |
| [KA] | `Handbücher/Kurzanleitung psv_QTec-3d.pdf` | Seite (über I1) | – |

**Wichtigste CHM-Themen nach Abschnitt**
- Abschnitt 1:
  - Konzepte: Controlling an Object Model; Using Object Variables; Working with
    Objects; Access to Interfaces; Using Collections; Access to General Information
  - Objekte: PSV~AcquisitionInstance (~GetApplication, ~IsRunning);
    PSV~PresentationInstance; PSV~Application_members; PSV~IApplication5_members;
    POLYFILELib~PolyFile
  - PFA: Overview; Model Overview; Type Libraries Overview; Examples
- Abschnitt 2:
  - PSV~Acquisition (alle Mitglieder, ~ScanStateChanged_EV, ~AcqStateChanged_EV)
  - PSV~Settings (~Load, ~Save); PSV~PTCSettings
  - Properties: PSV~AcquisitionProperties; PSV~AcqModeProperties; PSV~FftAcqProperties;
    PSV~TimeAcqProperties; PSV~ZoomFftAcqProperties; PSV~AverageAcqProperties;
    PSV~GeneralAcqProperties; PSV~ChannelAcqProperties; PSV~ChannelsAcqProperties;
    PSV~VibrometersAcqProperties; PSV~VibrometerAcqProperties;
    PSV~TriggerAcqProperties; PSV~GeneratorAcqProperties; PSV~GeneratorsAcqProperties;
    PSV~FrontEndAcqProperties; PSV~SEAcqProperties
  - Validatoren: POLYPROPERTIESLib~IFftAcqPropertiesValidator;
    POLYPROPERTIESLib~ITimeAcqPropertiesValidator
  - Signalformen: POLYWAVEFORMSLib~*
  - Infos und Hardware: PSV~InfosAcq; PSV~HardwareAcq; PSV~AlignmentsAcq;
    PSV~ScanHeadDevicesInfoAcq; PSV~VibrometerGroups; PSV~PositionDevice;
    PSV~DigitalPort(s)
  - Abgleich: POLYALIGNMENTLib~Alignment3D; POLYALIGNMENTLib~Alignment2D
  - Scankopf: PolyScanHeadLib~ScanHeadControl
  - Vibrometer: Polytec_IO_VibInterfaces~ControllerSettings; ~QuantitySettings;
    ~SensorHeadInfo; ~ISensorHead; ~IControllerGroup
- Abschnitt 3: PSV~Exporter (Beispiel); PSV~ExportParameters; PSV~PTCExportType;
  PSV~VibDocument; PSV~Documents; PSV~Document;
  PolyAcquisitionLib~AcquisitionPointData; PolyAcquisitionLib~AcquisitionPointDataStream
- Abschnitt 4:
  - Konzepte: Access to Data; Opening and Closing Files; Creating New Files;
    Operating on Combined Files
  - POLYFILELib~PolyFile (~Open, ~Close, ~ReadOnly, ~GetPointDomains, ~Create,
    ~IsAverageSpectrumCorrected)
  - POLYFILELib~DataPoint; ~DataPoints; ~PointDomain; ~PointDomains; ~XAxis; ~YAxis;
    ~MeasPoint; ~MeasPoints; ~Elements; ~DataPointReader
  - POLYSIGNALLib~SignalDescription; POLYSIGNALLib~DegreeOfFreedomID
- Abschnitt 5: PSV~Application~SuppressMessagesForAutomation, ~MessageOccurred_EV,
  ~QuitEx_EV, ~WarningLevel, ~MessagesLoggingEnabled; PolyScanHeadLib~IComTask
- Abschnitt 6: POLYFILELib~Version; ~SummaryInfo; ~Hardware; ~AcquisitionInfoModes;
  POLYPROPERTIESLib~GeneratorAcqPropertiesContainer (Beispiel)
- Abschnitt 8: alle `PTC…`-Themen der genannten Bibliotheken

**Handbuch [HB], verwendete Seiten:**
- 2-4 (PDF 20), 2-23/2-24 (PDF 39/40), 2-28 (PDF 44), 3-23/3-24 (PDF 67/68)
- 7-1 bis 7-34 (PDF 209–242)
- 8-2 bis 8-7 (PDF 248–253)
- 10-1 bis 10-11 (PDF 313–323)
- 10-15 (über I1)

**Folien:**
- [COM] Folien 2, 6–13 (Folien 11 und 12 als gerenderte Bilder gelesen)
- [PFA-M] Folien 2–4, 6, 8, 9 (Folien 4, 8, 9 als gerenderte Bilder gelesen)

**Nicht ausgewertet:** `PsvMsa*`, `PsvStage_deu`, `PsvUhf_deu` und `PsvVibroScan_deu`
(andere Systeme); englische und Desktop-Handbücher (Duplikate); Schulungsunterlagen
außer 11.2. Die PFA-Python-Beispiele und `SettingsAndScan.bas` liegen nicht im Input.
