<!-- Plan E1 (software-engineer, sonnet), Status: PLAN ZUR FREIGABE; unverändert übernommen. -->

# Plan E1: Erkundungsskript für den PSV-Messrechner

Die Belegkürzel ([BEM], [PFA], [HB], [COM], [KA]) und Abschnittsnummern stammen aus der COM-Referenz I5. Eigene Folgerungen sind mit [Einschätzung] gekennzeichnet, alles, was am Messrechner noch unbestätigt ist, mit [ungeprüft].

Gelesen wurden KONVENTIONEN.md, I5 (Abschnitte 1–7, 10, 11), das Erwartungsmanagement (F4/F5) und die Textfassung der Polytec-Hilfe. Ich habe stichprobenartig geprüft, dass diese Namen in der Textfassung existieren:
- `GetApplication(vbCreate, lTimeOut)`, `IsRunning`, `GetLaserOn`
- `Has…Properties`, `HasPositionDevice`, `HasScanHeadDevicesInfo`, `HasAlignments`
- `Alignments3D`/`CurrentQuality`, `ScanHeadType`, `FrontEndFirmwareVersion`
- `ProgramVersionString`, `LabelToIndex`, `SuppressMessagesForAutomation`

Es wurde nichts am Repository geändert. `software/` enthält bisher nur `README.md`; `software/pyproject.toml` fehlt noch.

## Plan

**Ansatz:** Ein Skript in vier klar getrennten Stufen (0, 1, 1b, 2), von denen nur 0, 1 und 1b ohne weitere Freigabe laufen.
- Der gesamte COM-Zugriff läuft über einen Proxy, der nur ausdrücklich freigegebene Mitglieder durchlässt und alles andere mit Exception verweigert. Die Whitelist ist damit testbar, auch ohne Windows.
- Der Bericht entsteht schrittweise und fehlertolerant: Jeder Prüfpunkt wird einzeln gefangen, die JSON-Datei wird nach jedem Prüfpunkt geschrieben, und ein Fehler bricht nicht ab.
- Verworfene Alternative: ein „freies" Explorationsskript (REPL, `dir(obj)`). Es ist flexibler, aber nicht auditierbar, und es könnte Schreibzugriffe auslösen.
- Weiter verworfen: ein sofortiges Einzelmess- oder Scan-Skript. P1-7 und P1-9 bewegen Spiegel, benutzen den Laser und schreiben Dateien, gehören also nicht in die Erkundung.

### 1. Prüfpunkte, Reihenfolge, Risiko (Leitfrage 1)

| Stufe | Prüfpunkte | Inhalt | Risiko |
|---|---|---|---|
| **0** (nur Standardbibliothek, kein COM) | P1-1 (Teil), P1-2, P1-3 (Teil), P1-4 (Teil) | Windows-Version und Bitness, Python-Version und -Bitness. Registry lesen (`winreg`, nur Lesen): ProgIDs `PSV.AcquisitionInstance`, `PSV.PresentationInstance`, `PSV.Application`, `PolyFile.PolyFile`, `PolyWaveforms.WaveformSine` (I5 1.3) → CLSID → `LocalServer32`/`InprocServer32` (Pfad, Program Files vs. x86). Dateiversionen der Server-EXE/DLL. Verzeichnisliste `%ProgramFiles%\Polytec`, `%CommonProgramFiles%\Polytec\COM` ([PFA] Examples). Registrierte Typbibliotheken (HKCR\TypeLib, Namen mit „Polytec"/„Poly"). Ist pywin32 importierbar (Version)? Läuft PSV (Prozessliste, nur lesen)? | keines (reines Lesen) |
| **1** (COM, nur lesend; erfordert laufendes PSV) | P1-4, P1-5, P1-6; aus P2: P2-6 (lesender Teil), P2-12; aus P3: P3-2 (nur Existenz), P3-4 (nur `GetLaserOn`) | Verbinden, dann nur lesen: Version, Mode, Acquisition-Zustand, Properties-Gruppen, Hardware, Vibrometer, Messpunkte, Abgleich (Details in Abschnitt 2). `win32com.client.selecttlb.EnumTlbs()` und Vergleich der `constants` mit Abschnitt 8 (I5). | niedrig. Rest-Risiko: Der Zugriff auf ein beschäftigtes PSV kann blockieren (I5 5.4, [ungeprüft]); deshalb ein Watchdog-Timeout (siehe unten). |
| **1b** (optional, PolyFile; nur mit `--datei`) | P1-10 (nur lesender Teil), P2-8 (lesender Teil), Label/Index aus P2-6 | Eine vorhandene Messdatei (z. B. `Example.svd` aus der PSV-Installation, siehe `polytec-chm-text/README.md`) wird mit `ReadOnly=True` geöffnet. Gelesen werden: Datenlänge `GetData`, `XAxis.Min/Max/MaxCount`, `GetMidX(0)` gegen `SampleResolution`/`Bandwidth`/`Lines`, `YAxis.Unit`, Kanäle Vib X/Y/Z, `Version.*`, `SummaryInfo.*`, `MeasPoint.Label/Index/AverageCount/Sigma`. Das beantwortet die KONVENTIONEN-Frage zur Frequenzachse ($f_k=k\,\Delta f$). | niedrig. Die Datei darf nicht gleichzeitig in PSV geöffnet sein (Sharing Violation, I5 4.2); das ist hier nur ein Fehler, kein Schaden. |
| **2** (nicht in diesem Paket freigegeben; eigene Freigabe je Punkt) | P1-7, P1-8, UFF-Export aus P1-10, passives P2-1 | siehe Abschnitt 3 | mittel |
| **nicht enthalten** | P1-9 (Scan), P2-3, P2-4, P2-9, P2-10, P2-11, P3-1, P3-7, P3-8 | schreiben Einstellungen/Dateien, bewegen Spiegel oder Laser oder regen an | – |

Nach Stufe 1 und 1b entscheidet der Nutzer, ob Stufe 2 überhaupt nötig ist.

**Schutzmechanismen in Stufe 1:**
- Kein Start von PSV. Es wird zuerst `IsRunning` gelesen. Ist es `False`, wird `GetApplication(False)` gar nicht erst versucht, weil nichts da ist. Das Skript bricht Stufe 1 ab und sagt, dass PSV im Erfassungsmodus laufen muss. `GetApplication(True, …)` würde PSV starten ([BEM] AcquisitionInstance~GetApplication, Zeile „…start it by passing True…"), also ist `vbCreate=False` der Standard, und `True` gibt es nur über `--start-psv`. Offen: ob `GetApplication(False)` bei laufender Instanz sofort zurückkommt ([ungeprüft]; die Doku sagt nur, dass der Timeout bei `False` wirkungslos ist).
- Ist `Acquisition.State != Stopped`, protokolliert das Skript nur und bricht ab, wenn es nicht lesen kann. Es unterbricht niemals eine Messung (kein `Stop`).
- Ein Gesamt-Watchdog, den das Skript selbst setzt: COM-Aufrufe laufen in einem Worker-Thread, der Hauptthread bricht nach einem Timeout ab und schreibt „blockiert bei <Prüfpunkt>". Der Timeout ist ein Parameter (kein fester Wert von mir festgelegt). Ein hängender COM-Aufruf lässt sich in Python nicht abbrechen; der Prozess endet dann mit `os._exit` nach dem Schreiben des Teilberichts.
- Jeder Prüfpunkt steht in `try/except`; die Exception (`hresult`, `excepinfo`) landet im Bericht. Das ist zugleich ein Beitrag zu P3-7 (HRESULT-Form), ohne Fehler zu provozieren.

### 2. Whitelist und Blacklist der COM-Aufrufe (A2)

Konvention: Alle Namen sind VB-Namen aus [BEM]. Der Proxy arbeitet mit Pfadmustern (`Application.Version` usw.). Index-Argumente sind 1-basiert; die Umrechnung ist hier nicht nötig, weil das Skript nur protokolliert, was Polytec liefert (KONVENTIONEN: Originalindex mitführen).

**Whitelist Stufe 1 (lesen, mit Beleg):**

| Pfad | Zweck | Beleg |
|---|---|---|
| `Dispatch("PSV.AcquisitionInstance")` (erzeugt nur die Instanz) | Einstieg | [BEM] PSV~AcquisitionInstance; I5 1.3 |
| `AcquisitionInstance.IsRunning` | läuft PSV? | [BEM] PSV~AcquisitionInstance~IsRunning |
| `AcquisitionInstance.GetApplication(False)` | Anwendung holen, ohne zu starten | [BEM] ~GetApplication |
| `Application.Version`, `.Mode`, `.Visible`, `.WarningLevel`, `.SuppressMessagesForAutomation`, `.MessagesLoggingEnabled` (nur Lesen) | Versions- und Meldungsverhalten (P1-5) | [BEM] PSV~Application_members; I5 3.1, 5.1 |
| `Application.Acquisition` | Zugang zur Erfassung (nur im Modus Acquisition vorhanden) | [BEM] Access to General Information |
| `Acquisition.State`, `.Mode`, `.ScanCaps`, `.GeneratorsOn` (nur Lesen), `.ScanFileName` (nur Lesen) | Zustand (P1-6); Generatorstatus als Sicherheitsangabe | [BEM] PSV~Acquisition~State/Mode/ScanCaps/GeneratorsOn/ScanFileName |
| `Acquisition.GetLaserOn(-1)` und `(1..3)` | Laserstatus lesen (P3-4) | [BEM] PSV~Acquisition~GetLaserOn |
| `Acquisition.ActiveProperties.Has*Properties` (General, Average, Fft, Time, ZoomFft, Channels, Vibrometers, Generators, Trigger, SignalEnhancement, FrontEnd, MultiFrame, FastScans) | welche Gruppen es gibt (P1-6) | [BEM] PSV~AcquisitionProperties_members; I5 2.5 |
| Lesen einfacher Werte: `FftProperties.Bandwidth/StartFrequency/EndFrequency/Lines/SampleResolution/Overlap/SampleFrequency/SampleTime`, `AverageProperties.Type/Count`, `GeneralProperties.*` (nur Lesen) | Ist-Konfiguration (P1-6), Abgleich mit Datei in 1b | [BEM] PSV~FftAcqProperties_members, ~AverageAcqProperties |
| Existenz (nicht Zugriff) von `FftProperties.FftAcqPropertiesValidator` (z. B. `hasattr`/`dir` auf dem Typ, **kein Lesen oder Zuweisen des Validators**) | Validator in dieser Version vorhanden? (P1-5) | [BEM] POLYPROPERTIESLib~IFftAcqPropertiesValidator; I5 2.6 |
| `Acquisition.Infos.Hardware.*` (`AcqBoardName`, `AcqBoardFirmwareVersion`, `AcqBoardChannelCount`, `FrontEnd`, `FrontEndFirmwareVersion`, `GeneratorName/Type/FirmwareVersion`, `ScanHeadType`, `SensorHeadNames/SerialNumbers/Versions`, `CoherenceOptimizerVersions`) | Hardware (P1-6) | [BEM] PSV~HardwareAcq_members |
| `Infos.Has…` (Hardware, ScanHeadDevicesInfo, Alignments, MeasPoints, PositionDevice) | Existenzprüfung, vermeidet Item-Fehler | [BEM] PSV~InfosAcq_members; Access to General Information |
| `Infos.ScanHeadDevicesInfo.ScanHeadName/ScanHeadType`; `Infos.Vibrometers.Count` und je Controller `SensorHeadInfo`-Lesewerte (`SerialNumber`, `FirmwareVersion`, `LaserWavelength`, `LaserPower`) | Scan- und Sensorköpfe | [BEM] PSV~ScanHeadDevicesInfoAcq, ~VibrometerGroups, Polytec_IO_VibInterfaces~SensorHeadInfo |
| `Infos.MeasPoints.Count`, `.Item(i).Index/.Label/.CoordXYZ/.ScanStatus` für höchstens die ersten und letzten wenige Punkte (Anzahl als Parameter); `MeasPoints.LabelToIndex(label)` für ein vorhandenes Label | Index/Label (P2-6), ByRef-Verhalten (Teil von P2-5), Indexbasis (P2-12) | [BEM] POLYFILELib~MeasPoints, ~MeasPoint; I5 1.7 |
| `Infos.Alignments.Alignments3D.Count/Item(i).Valid/.CurrentQuality/.TargetQuality/.PositionUncertainty/.AngleUncertainty` | Abgleichstatus (P1-6) | [BEM] POLYALIGNMENTLib~Alignment3D; I5 2.7 |
| `Infos.Alignments.Alignments2D.Item(i).Valid` | 2D-Abgleich | [BEM] POLYALIGNMENTLib~Alignment2D |
| Existenz (`Has…`) von `PositionDevice`, `DigitalPorts` (**keine** Wertelesung, kein `Pulse`) | U7-Frage (P3-2) | [BEM] PSV~PositionDevice, ~DigitalPorts |
| pywin32-Seite: `gencache.EnsureDispatch` ist **nicht** Whitelist-Bestandteil, weil es Cache-Dateien schreibt (Stufe 1 benutzt `Dispatch` Late Binding; makepy nur auf ausdrücklichen Schalter `--makepy`, schreibt ins pywin32-gen_py-Verzeichnis, nicht in Polytec-Verzeichnisse) | P1-4 | I5 7.2 |

**Whitelist Stufe 1b (PolyFile, nur lesen):** `Dispatch("PolyFile.PolyFile")`; `ReadOnly = True` (Zuweisung vor dem Öffnen, I5 4.2: „immer ReadOnly"); `Open(pfad)`; `IsOpen`; `Close()`; `Version.*`; `SummaryInfo.Title/Author/Subject/Comments` (nur Lesen); `Infos.Hardware.*`; `Infos.MeasPoints…` wie oben; `GetPointDomains(...)`, `Channels/Signals/Displays` (Namen und Anzahl), `DataPoints(i).GetData(display, 0)` für den ersten Punkt, `GetXAxis(display)` mit `Min/Max/MaxCount/Unit/GetMidX(0)`; `GetYAxes`; `Signal.Description` (Lesen). Belege: [BEM] Access to Data, Opening and Closing Files, POLYFILELib~PolyFile, ~DataPoint, ~XAxis; I5 4.2–4.4. Die Zuweisung `ReadOnly = True` ist im Proxy eine **einzige** erlaubte Schreiboperation (nur der Wert `True`), weil sie nur die Objektreferenz betrifft; sie ist Testfall in der Proxy-Logik.

**Blacklist (Proxy verweigert, Test pro Eintrag):**
- Messung/Bewegung/Laser: `Acquisition.Start`, `.Stop`, `.Scan`, `.ScanEx`, `.SetLaserOn`, `.AutoFocusLaser`, `.AssignFocusAutomatically`, `.CalculateFocusValues`, `.GeometryScan`, `.SetSelectedMeasPoints` (fährt den Laser, [BEM] ~SetSelectedMeasPoints), `.GetData`, `.GetSignalAmplitudes` (Wirkung ungeprüft, Stufe 2), `.TakeReferenceSnapshot`/`FindPointMarkers`/`MatchPointMarkers`. `Stop` ist bewusst verboten, auch als „Aufräumen": Das Skript beendet keine fremde Messung.
- Zuweisungen: `Acquisition.Mode =`, `.ScanFileName =`, `.GeneratorsOn =`, jede Zuweisung auf `*Properties.*`, `Application.Mode =`, `.SuppressMessagesForAutomation =`, `.WarningLevel =`, `.Visible =`, jede Zuweisung auf `MeasPoint.*` (u. a. `Label`).
- Dateien und Zustand: `Settings.Load/Save/Delete`, `Documents.Open`, `Document.Save/SaveAs/Close`, `Application.Quit/QuitEx`, `Exporter` und `ExportParameters`, `ExportVideoSnapshot(Ex)`, `ControllerSettings.Save`, `PolyFile.Save/SaveAs/Create/CalcBands`, `PolyFile.ReadOnly = False`.
- Hardware: `PositionDevice.StartMove*`, `DigitalPort.Value =`, `DigitalPort.Pulse`, `Alignment3D.Calculate`, jedes `PolyScanHeadLib~ScanHeadControl.Write…` (KONVENTIONEN: nie), `Waveform`-Zuweisungen.
- Implementierungsprinzip: **Whitelist ist maßgeblich, die Blacklist ist nur ein Testkatalog** (Default deny). Der Proxy kennt die Namen nur über Pfadmuster und leitet nie ein nicht aufgeführtes Mitglied weiter, auch nicht lesend. Ausnahme: reine Introspektion über `type(obj)`/`dir()` auf dem Typ ist erlaubt, `getattr(obj, name)` nur für Whitelist-Namen.

### 3. Optionale Stufe 2 (klar getrennt; Leitfrage 3)

Technisch getrennte Datei oder Schalter `--stufe2 <punkt>`, der **nur** mit interaktiver Bestätigung („JA" getippt, Text nennt die Folgen) und nur, wenn Stufe 1 den Sicherheitszustand bestätigt hat, ausgeführt wird. Je Punkt eine eigene Freigabe durch den Nutzer, nicht durch den Orchestrator allein (Ablauf G). Keine Aufnahme in das erste Umsetzungspaket empfohlen, nur als Entwurf.

| Punkt | Inhalt | Voraussetzungen / Abbruch | Risiko |
|---|---|---|---|
| S2-a (P1-7) | `Start(ptcAcqStartSingle)` ohne Generator, Polling `State` bis Stopped mit Gesamt-Timeout, danach `GetSignalAmplitudes([])` | `GeneratorsOn = False` (aus Stufe 1), kein Shaker/Verstärker angeschlossen oder ausgeschaltet bestätigt, Laser an laut `GetLaserOn`, `State == Stopped` am Start; Abbruch bei Timeout → `Stop()` ist hier **als einziger Fall** zulässig (nur für die eigene Messung) | mittel: Laser/Messelektronik aktiv; Generator-Seiteneffekte [HB]-Hinweis in I5 3.3 |
| S2-b (P1-10, Export) | UFF-Export einer vorhandenen Datei **in einen neuen Ordner** (Eingabe nur lesen) als Golden File | `Application`-Cast für `Exporter` ist [ungeprüft] (I5 1.5, 7.3); Datei nicht in PSV geöffnet; Zielpfad darf nicht existieren | niedrig/mittel (schreibt Datei, nicht in Rohdaten) |
| S2-c (P1-8) | Meldungsverhalten mit absichtlich unzulässigem `ScanFileName` | verändert Zustand und kann Dialog öffnen; **nur auf ausdrückliche Anweisung** und nur in Anwesenheit des Nutzers am Rechner | mittel (blockierender Dialog möglich) |
| S2-d (P2-1 passiv) | `DispatchWithEvents` auf `Acquisition`, der Nutzer startet eine Messung selbst in PSV; das Skript protokolliert nur `AcqStateChanged`/`ScanStateChanged`, `MessageOccurred` wird **ohne Antwort** protokolliert (Rückgabewert würde eine Antwort simulieren) | `PumpWaitingMessages` nötig; ob ein Handler ohne Rückgabe den Dialog offen lässt, ist [ungeprüft] | niedrig/mittel |

Vorschlag: Das Umsetzungspaket enthält nur Stufe 0, 1 und 1b. Stufe 2 bleibt Folgepaket, abhängig von den Ergebnissen und von einem Versuchsplan (`/versuchsplanung`) für P1-9 (Scan).

### 4. Ausgabe (Leitfrage 2)

Vorschlag Ausgabeordner: `erkundung_<Rechnername>_<JJJJ-MM-TT_HHMMSS>/` neben dem Skript (Parameter `--out`), **neu angelegt, nie überschrieben** (existiert er, wird ein Suffix angehängt). Dateien:
1. `bericht.json`: strukturiert, UTF-8, Felder: `schema_version`, `skript_version`/Git-Hash des Skripts (SHA-256 der Skriptdatei, falls kein Git vorhanden), Zeitstempel (lokal und UTC mit Zeitzone), Rechnername (Hash oder Klartext nach Nutzerwahl; siehe Datenschutz unten), Kommandozeile; `umgebung` (Windows-Version, Bitness, Python-Version/-Bitness/-Pfad, pywin32-Version, `winreg`-Ergebnisse); `pruefpunkte[]` je mit `id` (P1-2 …), `stufe`, `status` (`ok` | `fehler` | `uebersprungen` | `blockiert`), `werte`, `dauer_s`, `exception` (Typ, `hresult`, `excepinfo`, Traceback gekürzt), `beleg_ref` (z. B. „I5 3.1"); `whitelist_aufrufe[]` (Protokoll **aller** tatsächlich weitergereichten Aufrufe in Reihenfolge, mit Dauer) und `verweigert[]` (blockierte Zugriffsversuche, sollte leer sein); `dateien` (Hash/Größe/mtime vor und nach, für 1b).
2. `zusammenfassung.md`: lesbar, Tabelle je Prüfpunkt (Status, Kernwert, Auffälligkeiten), Liste der Abweichungen von der Erwartung aus I5 mit Verweis auf die betroffene I5-Stelle, Zeitbedarf, offene [ungeprüft]-Punkte, die nun bestätigt/widerlegt sind.
3. `konsole.log`: vollständiges Log.
4. `registry.reg.txt` / `typelibs.txt`: Rohauszug (Text).
Alle Werte als Text/JSON, **keine** Binärdaten, keine Messdaten (nur Metadaten; bei 1b nur Kennzahlen und die ersten wenigen Datenwerte, die Anzahl ist Parameter).

Hochladen: Nutzer lädt den Ordner (oder ein ZIP) nach `in_progress/versuche/erkundung/` hoch (Ablageort mit Nutzer klären). **Datenschutz:** Der Bericht enthält Rechnername, Benutzername in Pfaden (`C:\Users\<Konto>`), evtl. Seriennummern. Das Skript ersetzt den Benutzernamen standardmäßig durch `<user>` (Schalter `--keep-user`); Seriennummern der Geräte bleiben im Bericht, weil sie für die Dokumentation nötig sind (I5 6); der Nutzer prüft vor dem Upload (Repository ist privat; Übergabe ans Institut: F18).

### 5. Laufzeitumgebung (Leitfrage 4; nur Optionen, keine Entscheidung)

| Option | Beschreibung | Vorteil | Nachteil / Risiko |
|---|---|---|---|
| **L1** Einzelnes `.py` ohne Installation, vorhandenes Python | Skript verwendet nur Standardbibliothek plus optional `win32com`. Läuft mit jedem vorhandenen Python (falls auf dem Messrechner schon eines liegt, z. B. durch Polytec-Software; **[offen]**, ob PFA-Python-Beispiele ein Python mitbringen, I5 7.1) | keine Installation, F4 nicht berührt | ohne pywin32 nur Stufe 0 |
| **L2** Portables Python (eingebettete Distribution, „embeddable zip") plus pywin32 aus Wheel in einem Benutzerordner | Entpacken in `%USERPROFILE%\erkundung\` ohne Setup, ohne Registry- oder PATH-Änderung; pywin32-Wheel offline mitgeliefert | keine Systeminstallation; Rückbau durch Löschen des Ordners | Polytec bittet bei „nicht von Polytec angebotenen Komponenten" um Rücksprache ([KA] 1-4); auch eine portable Installation ist Fremdsoftware, also F4 formal betroffen. pywin32 braucht Post-Install (`pywin32_postinstall`, DLL-Pfade) [ungeprüft] in der portablen Variante; Nutzerrechte prüfen |
| **L3** uv-Projekt (KONVENTIONEN: Python 3.11/uv) | `uv run` aus dem Repository-Klon auf dem Messrechner | gleiche Umgebung wie das Hauptpaket, reproduzierbar (Lockfile) | Installation von uv, Python, Internet-Zugang des Messrechners, Git: am stärksten von F4 betroffen |
| **L4** Kein Python auf dem Messrechner: PowerShell-Variante | `New-Object -ComObject PSV.AcquisitionInstance` usw. (Late Binding über IDispatch, wie Matlab `actxserver`, [PFA-M] Folie 4), Registry über `Get-ItemProperty`. Whitelist als Skriptlogik | PowerShell ist in Windows enthalten; keine Fremdinstallation; kein pywin32-Befund, aber ein Befund zu COM selbst | prüft **nicht** pywin32-Verhalten (ByRef, Safearray, Events, Enums, Casts); doppelter Pflegeaufwand; Execution-Policy; Tests im Repo schwierig. Eher als Fallback für Stufe 0/1 |
| **L5** Aus PSV heraus: WinWrap-Basic-Makro | PSV führt Basic selbst aus und ist selbst Controller ([BEM] Controlling an Object Model; vorhandene Makros F7) | läuft innerhalb der Polytec-Umgebung, keine Fremdinstallation | nicht Python; beantwortet die Python-Fragen nicht; Makro-Editor und Rechte nötig |
| **L6** Anderer Rechner mit PolyFile | PFA allein (Stufe 1b) auf dem Entwicklungsrechner/Laborarbeitsplatz mit PolyFile-Installation | entkoppelt Dateitests vom Messrechner; deckt P1-10 (Frequenzachse) ab | prüft nicht die Acquisition-Schnittstelle (P1-5/P1-6); PFA-Installation und Lizenz [offen] (F5) |

Einschätzung [Einschätzung]: Stufe 0 (Registry, Versionen) ist die billigste und braucht nur L1 oder L4; sie klärt Bitness und Servertyp, die über die Python-Variante entscheiden. L2 kommt dem Ziel (Python/pywin32 wirklich testen) am nächsten, ohne den Rechner zu verändern; trotzdem Fremdsoftware, also Antwort auf F4 abwarten. Wichtig: Skriptdateien selbst sind Text (keine Installation), das `.py` kann auch per USB oder Upload übertragen werden.

### 6. Ablage im Repo, Tests, KONVENTIONEN (Leitfrage 5)

**Ablageort (Vorschlag, Bestätigung nötig):** `software/tools/erkundung/` mit
- `erkundung.py` (Einstieg, Argumente, Orchestrierung; bewusst **eine Datei ohne Abhängigkeit zum Paket `software/src`**, damit sie als einzelne Datei auf den Messrechner kopierbar ist: **L1/L2/L3 gleichermaßen**),
- Tests unter `software/tests/tools/erkundung/`.

Falls das Skript in mehrere Module zerlegt wird, geht die Einzeldatei-Eigenschaft verloren; Alternative ist ein `zipapp`/Single-File-Build. Das entscheidet der Umsetzer im Rahmen des Pakets (Einzeldatei bevorzugt, Länge begrenzt).

**Zugehörigkeit:** eigenständiges Werkzeug, **nicht** Teil des Hauptpakets. Kein Import von `software/src`, der spätere Adapter kann die gewonnenen Erkenntnisse nutzen, aber nicht den Code. Der Whitelist-Proxy könnte später als Vorlage dienen: ADR-Kandidaten (keine Entscheidung hier): (a) Whitelist-Proxy auch im Produktiv-Adapter (Default deny auf COM-Ebene); (b) Early Binding (makepy) gegen Late Binding (`Dispatch`); (c) Einzeldatei-Werkzeug gegen Paket-interne Skripte.

**Test ohne Windows/PSV:** 
- COM-Zugriff wird über eine Fabrik (`dispatch: Callable[[str], object]`) injiziert; `winreg`, `pythoncom`, `win32com` werden nur in einer kleinen Adapterfunktion importiert (`# pragma: no cover` mit Begründung, KONVENTIONEN). Logik (Proxy, Prüfpunktausführung, Berichtsbau, Redaktion, Argumente, Ausgabeordner) ist plattformunabhängig und voll getestet.
- **Fake-PSV** als Test-Double mit der Objektstruktur aus I5 1.4 (nicht der geplante Gerätesimulator des Hauptpakets, damit keine Abhängigkeit entsteht; das kann später zusammengeführt werden, ADR-Kandidat). Der Fake protokolliert jeden Aufruf; Tests prüfen, dass **nur Whitelist-Aufrufe** erfolgen (Aufrufprotokoll gegen Whitelist).
- Fehlerinjektion: Fake wirft `com_error`-ähnliche Exception (Ersatzklasse mit `hresult`, `excepinfo`), Fake blockiert (Timeout-Test des Watchdogs), PSV läuft nicht (`IsRunning=False`), Modus nicht Acquisition (`Acquisition` fehlt), `Nothing`/`None`-Rückgaben.
- Marker: Ein Marker `hardware` (existiert gemäß KONVENTIONEN, falls noch nicht angelegt, legt ihn das Projektgerüst an) kennzeichnet einen optionalen Test, der auf dem Messrechner läuft (`pytest -m hardware`) und nur Stufe 0/1 ausführt.
- Prüfungen laut KONVENTIONEN aus `software/`: `uv run ruff check .`, `uv run ruff format --check .`, `uv run mypy --strict .`, `uv run pytest --cov --cov-fail-under=90`. `mypy --strict` mit Typ `Any` nur an der COM-Grenze, dort kapseln. Docstrings NumPy-Stil, Einheiten im Namen (`timeout_s`, `duration_s`). Voraussetzung: `software/pyproject.toml` existiert (KONVENTIONEN: erstes Paket); falls nicht, ist das Gerüst mitzuliefern oder das Paket ist davon abhängig. **Das muss vor der Umsetzung geklärt werden.**
- Das Skript muss unter **Python 3.11** laufen (auch auf dem Messrechner; falls dort eine andere Version vorhanden ist, nur Standardbibliothek in Stufe 0, Mindestversion dokumentieren).

### 7. Prüfanleitung für den Nutzer (A4, Entwurf)

> **Erkundung am PSV-Messrechner (nur Lesen)**
>
> **Wichtig vorab.** Das Skript misst nicht, schaltet keinen Laser, ändert keine Einstellungen und überschreibt keine Datei. Es liest nur Versionen, Registry-Einträge und den aktuellen Zustand von PSV. Es beendet PSV nie und startet PSV nur, wenn du es ausdrücklich mit `--start-psv` verlangst.
>
> **Vorbedingungen**
> 1. Zustimmung geklärt (Frage F4) bzw. du nutzt Variante L1/L4/L5 ohne Installation.
> 2. Bei Stufe 1: PSV läuft im **Datenerfassungsmodus**, Messsystem eingeschaltet wie für eine normale Messung, **keine laufende Messung**. Kein Prüfling nötig. Der Generator-Ausgang darf nicht an einen Shaker/Verstärker angeschlossen sein oder muss aus sein (nur Sicherheitsvorsicht; es wird nichts ausgegeben).
> 3. Für Stufe 1b: eine vorhandene Messdatei (z. B. `Example.svd`), **nicht** in PSV geöffnet. Besser eine Kopie (das Skript öffnet sie nur schreibgeschützt).
> 4. Ausgabeordner auf einem beschreibbaren Laufwerk (nicht auf Polytec-Verzeichnissen).
>
> **Schritte**
> 1. Skript auf den Rechner kopieren (z. B. `C:\Users\<du>\erkundung\`).
> 2. Eingabeaufforderung/PowerShell öffnen, in den Ordner wechseln.
> 3. Stufe 0: `python erkundung.py --stufe 0` (ca. 1 Minute).
> 4. PSV im Erfassungsmodus öffnen; **keine Dialoge offen lassen**. Stufe 1: `python erkundung.py --stufe 1` (erwartet: wenige Minuten, abhängig vom COM-Antwortverhalten; das Skript meldet pro Prüfpunkt seine Dauer).
> 5. Optional 1b: `python erkundung.py --stufe 1 --datei "<Pfad>\Example.svd"`.
> 6. Ausgabeordner prüfen (`zusammenfassung.md` öffnen) und an das Repository liefern (Ort mit dem Orchestrator abstimmen).
> 7. Zusätzlich manuell festhalten (ohne Skript): PSV-Version und Optionen laut *Hilfe > PSV Info* (P1-3, Screenshot oder Text; I5 6 nennt die Lizenzen als nicht per COM belegt). 
> 8. Ob irgendein Fenster in PSV aufgepoppt ist oder PSV sich anders verhielt, notieren.
>
> **Abbruchkriterien (sofort Strg+C, danach Ordner trotzdem hochladen)**
> - PSV zeigt unerwartet einen Dialog, einen Fehler oder reagiert nicht mehr.
> - Das Skript meldet „blockiert bei …" oder es ist länger als der angekündigte Timeout nichts passiert.
> - Der Laser schaltet sich ein/aus oder ein Spiegel bewegt sich (das darf nicht passieren; **wenn doch, Skript abbrechen und melden**, das wäre ein Befund zur Whitelist).
> - Eine Meldung im Skript, dass ein nicht freigegebener Aufruf verweigert wurde.
>
> **Erwartete Dauer:** Stufe 0 ca. 1 Minute, Stufe 1 und 1b ca. 5 bis 15 Minuten inklusive Vorbereitung [Einschätzung, nicht gemessen].
>
> **Was geht ins Repository:** der Ausgabeordner (JSON, Markdown, Logs, Registry-Text); keine Messdaten; Benutzername ist standardmäßig entfernt. Der Hardwaretest gilt erst als bestanden, wenn du das Ergebnis bestätigt hast (Ablauf G); das Ergebnis wird per `/laborbuch` festgehalten.

### 8. Akzeptanzkriterien für das Umsetzungspaket (A3)

- **K1:** Ein Whitelist-Proxy (Default deny) leitet nur die in Abschnitt 2 genannten Pfade weiter. Für **jeden** Eintrag der Blacklist gibt es einen Test, der `PermissionError` (oder die festgelegte Exception) erwartet. Ein nicht aufgeführter Pfad wird ebenfalls verweigert.
- **K2:** Ein Test gegen den Fake-PSV zeigt über dessen Aufrufprotokoll, dass in Stufe 0, 1 und 1b ausschließlich Whitelist-Aufrufe erfolgen und der Fake nach dem Lauf unverändert ist (Zustand vorher = nachher).
- **K3:** Ist `IsRunning == False`, startet das Skript PSV nicht (Fake: `GetApplication(True, …)` wird nie aufgerufen), bricht Stufe 1 sauber ab und liefert Status `uebersprungen` samt Hinweistext. `--start-psv` ändert das und steht nur nach Bestätigung zur Verfügung.
- **K4:** `State != Stopped` führt nie zu `Stop` oder einem Messbefehl; der Bericht enthält den Zustand.
- **K5:** Jeder Prüfpunkt ist gegen Ausnahmen gekapselt; eine Exception in einem Punkt lässt die übrigen laufen. Ein hängender Aufruf (Fake blockiert) führt nach dem Timeout zu einem Teilbericht mit Status `blockiert` und Prozessende.
- **K6:** `bericht.json` entspricht einem dokumentierten Schema (Felder aus Abschnitt 4), wird nach jedem Prüfpunkt geschrieben und enthält `whitelist_aufrufe` und `verweigert`. `zusammenfassung.md` entsteht aus dem JSON (ein Test vergleicht beide auf dieselben Prüfpunkt-IDs).
- **K7:** Ein vorhandener Ausgabeordner wird nie überschrieben (Test: zweiter Lauf legt neuen Ordner an). Eine Eingabedatei in 1b ist nach dem Lauf unverändert (Hash, Größe, mtime in Test mit temporärer Datei und Fake-PolyFile); `ReadOnly = True` wird vor `Open` gesetzt (Aufrufreihenfolge im Fake geprüft); `ReadOnly = False` wird verweigert.
- **K8:** Stufe 0 läuft mit der Standardbibliothek ohne pywin32; fehlt pywin32 oder `winreg` (Test unter Linux), liefert das Skript einen sauberen Hinweis statt Absturz.
- **K9:** Der Benutzername wird standardmäßig aus dem Bericht entfernt (Test mit künstlichem Pfad); `--keep-user` hebt das auf.
- **K10:** Die Standard-Prüfung (ruff check/format, `mypy --strict`, `pytest --cov --cov-fail-under=90`) läuft fehlerfrei; Ausnahmen für COM-Adapter nur per `# pragma: no cover` mit Begründung. Die Rückmeldung nennt nicht ausgeführte Prüfungen.
- **K11:** Das Skript trägt Hinweis auf Zweck, Version, Quelle (I5-Abschnitte) und die Benutzer-Prüfanleitung (`README.md` im Ordner oder Docstring). Kein Aufruf von `eval`/`exec`/`pickle`, kein Netzwerkzugriff, keine Schreibzugriffe außerhalb des Ausgabeordners.
- **K12:** Die Prüfanleitung (Abschnitt 7) liegt in der vom Nutzer abgenommenen Fassung bei; Stufe 2 ist **nicht** enthalten oder deaktiviert und hinter einer eigenen Bestätigung (falls im Paket gewünscht, dann eigene Tests mit Fake).
- **K13:** Der Umsetzer markiert in der Rückmeldung jeden Prüfpunkt aus I5 Abschnitt 10 als „am Gerät unbestätigt" (Hardwaretest nie als bestanden melden, Ablauf G).

### 9. Nicht enthalten

- Keine Messung, kein Scan, keine Anregung, kein Schreiben von Einstellungen (P1-7, P1-8, P1-9, P2-3, P2-4, P2-9, P2-10, P2-11, P3-1, P3-7 sowie P3-8; Stufe 2 nur als Entwurf).
- Keine Architekturentscheidungen für das Hauptpaket (nur ADR-Kandidaten, s. o.).
- Keine Installation auf dem Messrechner und keine Änderung der Polytec-Umgebung.
- P1-1 (Freigabe) und P1-3 (Lizenzen) sind teils manuell (F4/F5).

## Annahmen
1. Das Skript läuft zunächst nur für Stufe 0 und 1; die Erkundung folgt der Reihenfolge „lesen vor schreiben" aus I5 Abschnitt 10.
2. `GetApplication(False)` liefert bei laufender Instanz die Anwendung ohne Start. Die Doku sagt nur, dass der Timeout dann wirkungslos ist und `True` startet. **[ungeprüft]**
3. Das Lesen der aufgelisteten Properties löst keine Messung, keine Spiegelbewegung und keinen Dialog aus. Für reine Property-Reads ist das plausibel, **belegt ist es nicht** (die Doku nennt keine Seiteneffekte). Deshalb das Timeout-Konzept und der Abbruchhinweis in der Anleitung.
4. `Acquisition.Infos.Hardware` und `Alignments3D` sind im Erfassungsmodus lesbar (I5 2.8, 2.7).
5. Bitness und Servertyp der PSV-Installation sind bis Stufe 0 unbekannt; die Variante L2 hängt davon ab (In-Process-Server brauchen gleiche Bitness, I5 7.3).
6. Datenschutzgrundsatz: Rechner- und Benutzername sind nicht Teil der Arbeit; Standard ist Entfernen.

## Risiken
- **Seiteneffekt eines Reads** (siehe Annahme 3): Mitigation durch Whitelist, Watchdog und Abbruchhinweis; Erkennung durch Beobachtung am Gerät.
- **Hängender COM-Aufruf** durch einen modalen Dialog im PSV ([ungeprüft] I5 5.4): nicht abbrechbar; Teilbericht wird vorher geschrieben, Prozess wird hart beendet.
- **Rechte:** Läuft PSV mit erhöhten Rechten, kann ein nicht erhöhtes Python den COM-Zugriff verweigert bekommen ([ungeprüft], nicht in I5 behandelt).
- **Fremdsoftware ohne Rücksprache (F4)**: Auch portables Python ist Fremdsoftware ([KA] 1-4).
- **PFA-Version/Lizenz** unbekannt (F5): 1b kann an fehlender Registrierung scheitern; das ist dann selbst ein Befund.
- **Gefahr der „zu vollständigen" Erkundung:** viele Properties zu lesen kostet Zeit und erzeugt Rauschen; deshalb die feste Whitelist und begrenzte Punkteanzahl.
- **Sharing Violation** bei 1b, falls PSV die Datei offen hat: in der Anleitung als Vorbedingung, im Skript als klarer Fehlertext.

## Rückmeldung an den Orchestrator

**Paket:** E1 · **Status:** PLAN ZUR FREIGABE

**Was geändert wurde:** nichts (Planungspaket, kein Code, keine Dateien im Repository). Gelesen: `/home/user/BA_Jakob-Busch_P/KONVENTIONEN.md`, `/home/user/BA_Jakob-Busch_P/in_progress/analysen/2026-10-23_I5_com-referenz.md`, `/home/user/BA_Jakob-Busch_P/in_progress/planung/erwartungsmanagement.md` (F4/F5) und Auszüge aus `/home/user/BA_Jakob-Busch_P/in_progress/analysen/polytec-chm-text/`.

**Wie verifiziert:** Quellen gelesen und Namen in der Textfassung der Polytec-Hilfe nachgeschlagen (siehe oben). Kein Code ausgeführt, nichts am Gerät oder in der Cloud geprüft. Alle Aussagen zum Verhalten der Schnittstelle sind [ungeprüft], soweit nicht ausdrücklich mit [BEM]/[HB] belegt.

**Akzeptanzkriterien:**
- A1: ✅ Plan entlang der Leitfragen 1 bis 8 (Abschnitte 1 bis 9), API-Nutzung mit Belegen
- A2: ✅ Whitelist und Blacklist in Abschnitt 2
- A3: ✅ Akzeptanzkriterien K1 bis K13 in Abschnitt 8
- A4: ✅ Entwurf der Prüfanleitung in Abschnitt 7

**Annahmen:** siehe Abschnitt „Annahmen" (insbesondere: Reads lösen nichts aus [ungeprüft]; `GetApplication(False)` startet PSV nicht [ungeprüft]).

**Sichtbare Verhaltensänderungen und Risiken:** keine am Repository. Risiken siehe Abschnitt „Risiken".

**Unverifiziert:** alle Prüfpunkte aus I5 Abschnitt 10; erst nach Lauf am Gerät und Bestätigung durch den Nutzer bestätigt.

**Rückfragen:**
- [blockierend für die Umsetzung] F4: Darf Python (auch portabel, Variante L2) bzw. pywin32 auf dem Messrechner genutzt werden? Ohne Antwort ist nur Stufe 0 mit L1/L4 oder Variante L5/L6 möglich. Ausführung erst nach Klärung (Auftrag).
- [blockierend] Ist `software/pyproject.toml` bereits angelegt oder gehört das Projektgerüst zum Umsetzungspaket? (KONVENTIONEN: erstes Umsetzungspaket.) Aktuell enthält `software/` nur `README.md`. *Auswirkung:* ohne Gerüst sind die Standard-Prüfungen nicht ausführbar.
- [nicht blockierend] Ablageort `software/tools/erkundung/` und Upload-Ziel der Ergebnisse (z. B. `in_progress/versuche/erkundung/`). *Annahme:* wie im Vorschlag.
- [nicht blockierend] Soll Stufe 1b (Datei lesen) im ersten Umsetzungspaket sein? Gibt es eine geeignete Messdatei (F7: `.svd` mit UFF-Export, oder `Example.svd` aus der PSV-Installation)? *Annahme:* ja, optional per Schalter.
- [nicht blockierend] Soll der Rechnername im Bericht stehen? *Annahme:* Benutzername entfernt, Rechnername im Klartext.
- [nicht blockierend, an Betreuer/Polytec] Sicherheitsfreigabe: Darf der Nutzer PSV im Betrieb per COM nur lesend ansprechen, solange der Messrechner im Labor ist (Haftung/Garantie)? Zusammen mit F4 stellen.
- [nicht blockierend] Stufe 2: Welche Punkte (S2-a bis S2-d) sollen in einem Folgepaket entworfen werden, und in welcher Laborsituation (Aufsicht, Sicherheitseinweisung zum Laser)? *Annahme:* Stufe 2 bleibt außerhalb dieses Pakets.

**Vorschlag für KONVENTIONEN.md:**
- Zugriff auf COM-Objekte, auch in Hilfsskripten, nur über einen Whitelist-Proxy (Default deny).
- Hilfswerkzeuge für Erkundung liegen unter `software/tools/` und importieren nicht aus dem Hauptpaket.
- Berichte von Messrechner-Läufen enthalten standardmäßig keinen Benutzernamen und werden nie überschrieben.

**ADR-Kandidaten (keine Entscheidung):** Whitelist-Proxy im Produktiv-Adapter; Early gegen Late Binding; Einzeldatei-Werkzeug gegen Paket-interne Skripte; Fake-PSV im Werkzeug gegen Gerätesimulator des Hauptpakets.

**Review-Empfehlung:** Nach der Umsetzung Review mit Schwerpunkt Whitelist-Vollständigkeit (Default deny, keine Umgehung über `getattr`/Attributketten), Dateischutz (ReadOnly, kein Überschreiben) und Watchdog-Verhalten; Fachabnahme der Prüfliste nicht nötig, solange keine Auswertung erfolgt.