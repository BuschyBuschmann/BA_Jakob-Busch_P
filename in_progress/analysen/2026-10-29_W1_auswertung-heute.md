# W1: Wie Auswertungen von LDV-Schwingungsmessungen heute ablaufen (Bestandsaufnahme)

Paket W1 (Recherche), Stand 2026-10-29. Reine Bestandsaufnahme, keine Bewertung "besser/schlechter" (das ist Paket W3). Bezug: Lastenheft R-050 bis R-053 (`in_progress/anforderungen/lastenheft.md`).

## 0 Kennzeichnung der Belege

| Kürzel | Bedeutung |
|---|---|
| **[H]** | **Herstellerangabe** (Polytec bzw. Siemens), keine unabhängige Fachquelle |
| **[Repo]** | Dokumentation im Repo, mit Datei und Abschnitt/Seite. Gelesen wurde der Text; Abbildungen und Formelbilder der PDFs wurden nicht ausgewertet |
| **[Lit-S]** | Literatur oder Software-Dokumentation nur über Suchtreffer (Prüfstand `metadaten`), Inhalt nicht gelesen |
| **[Volltext]** | gelesener Volltext (in W1 nur die Repo-Dokumente) |

Seitenangaben: gedruckte Seitenzahl der Handbücher (z. B. "HB 9-11"), bei Folien die Foliennummer im Fuß.

Quellenkürzel im Repo:
- **HB** = Polytec Software-Handbuch PSV-Datenerfassung 10.1 (DE), `Input/literatur/polytec/Handbücher/Software Handbuch PSV.pdf`, Dok. 41584 (`polytec2022psvhandbuch`)
- **HB-A** = Polytec Software-Handbuch Auswertung 10.1 (DE), `Software Handbuch PSV Desktop.pdf`, Dok. 41596 (`polytec2022psvdesktop`)
- **SM** = Software Manual PSV 10.1 (EN), `Software Manual PSV.pdf`, Dok. 41585 (`polytec2022psvsoftware`)
- **TM** = Theory Manual, `Theory Manual.pdf` (`polytec2015theory`, Stand Software 9.1)
- **F11 / F11.1 / F11.2** = Schulungsfolien `11 PSV_Auswertung_komplett`, `11.1 SignalProzessor`, `11.2 Polytec-File-Access_Matlab`
- **COM** = Folien `06_Automatisierung_via_COM` (`polytec2025com`)
- **BEM / PFA** = Textauszug der CHM-Hilfen unter `in_progress/analysen/polytec-chm-text/basic-engine-manual/` bzw. `.../polytec-file-access/`
- **I5** = `in_progress/analysen/2026-10-23_I5_com-referenz.md` (Abschnittsnummer dort)

Grenze der Prüfung: In der Cloud-Sitzung waren polytec.com, pyuff.readthedocs.io, community.sw.siemens.com u. a. nicht abrufbar (Netzfreigabe fehlt); nur WebSearch und github.com funktionierten. Alle Web-Angaben unten sind daher Suchtreffer oder die GitHub-Seite.

---

## 1 Bereich A: Polytec-PSV-Software

### 1.1 Ablauf der Auswertung in Schritten

PSV kennt zwei Betriebsarten: Datenerfassung und Auswertung (Präsentationsmodus) [Repo: F11 Folie 4, HB 2-5]. Die Auswertung arbeitet auf gespeicherten Dateien. Der Ablauf, soweit die Dokumente ihn beschreiben:

1. **Datei öffnen** (`.svd` Scan, `.pvd` Einpunkt, `.mvd` MPV; `.set` Einstellungen) [Repo: HB 9-45, 10-8; HB 10-8 nennt `.svd`/`.pvd`/`.set` als "proprietäres Binärformat"].
2. **Darstellung wählen.** Standardmäßig zeigt PSV Banddaten und Messobjekt, "kein Spektrum zu sehen"; Umstellung auf Punktdaten mit "Einzelner Scanpunkt" oder "Gemitteltes Spektrum" [Repo: F11 Folien 5-6].
3. **Datensatz wählen:** Domäne (Zeit, FFT, RMS, Terzen), Kanal (Vib, Vib 3D, Ref 1..3, Kombikanäle wie "Vib & Ref 1"), Signal (Weg, Geschwindigkeit, Beschleunigung, Spannung, FRF, AP, CP, H1, H2, Kohärenz, PSD, ESD) und Anzeigeart (Amplitude, dB, dB(A), Phase, Real, Imag, Nyquist, Momentanwert) [Repo: HB 9-19 bis 9-21, Tab. 9.1/9.2].
4. **3D-Ansicht und Animation:** Darstellung auf der Messgeometrie als Isolinien, Fläche, Pfeile, Drahtgitter oder Scanpunkte; Animation bei gewählter Frequenz über Cursor im Spektrum [Repo: F11 Folien 7-10].
5. **Bänder:** Band-Cursor oder Banddefinition legt einen Frequenzbereich fest, der einen Peak enthält; der Peak wird "automatisch detektiert", die Animation der Peakfrequenz erscheint im Scan Viewer, der RMS-Wert je Band über Domäne RMS und Ansicht Banddaten [Repo: F11 Folien 27-29].
6. **Kennwerte am Band-Cursor:** Minimum, Maximum, Mittelwert, Effektivwert (RMS), Standardabweichung; Peak-Anpassung eines eindimensionalen harmonischen Oszillators (Methode der kleinsten Quadrate) an ein reales oder komplexes Spektrum mit Ausgabe von f_max, "Dämpfung (−3 dB)", Q-Faktor, Dämpfungsgrad ζ [Repo: HB 9-10/9-11; HB-A 3-13/3-14].
7. **Nachbearbeitung** mit dem Signalprozessor (tabellenartig, Excel-ähnlich), Ergebnis als `.spd` oder als Usr-Datensatz zurück in die `.svd` [Repo: F11.1 Folien 2-15, HB 10-8].
8. **Export/Weitergabe** (siehe 1.3).

### 1.2 Verfügbare Auswertearten (Herstellerangaben)

| Auswerteart | Was Polytec dokumentiert | Beleg |
|---|---|---|
| **Spektren** (R-050) | Einzelspektrum je Scanpunkt, gemitteltes Spektrum aller Punkte; Skalierung so, dass eine harmonische Schwingung mit Amplitude 1 (Null-Spitze) eine Linie der Amplitude 1 ergibt, wenn sie im Zeitfenster periodisch ist (Fenster Rechteck, Bartlett, Blackman-Harris, FlatTop, Hamming, Hanning, Tapered Hanning); Exponential- und Kraftfenster ohne Zusatzskalierung | [H][Repo] TM 3-3; HB 9-21; F11 Folien 5-6 |
| **Mittelung** | Betragsmittelung (Phase geht zunächst verloren, wird aus dem Kreuzspektrum mit der Referenz mit niedrigster Nummer zugewiesen), komplexe Mittelung, Peak-Hold; Phasenbezug je Kombination aus Mittelung, Trigger, Referenz in Tabelle 6.1 | [H][Repo] TM 6-5 bis 6-7 |
| **FRF, H1, H2, Kohärenz** (R-051) | nur mit Referenzkanal; berechnet aus AP/CP-Spektren je Kombination Vibrometer/Referenz; H1 "hauptsächlich" von Rauschen im Eingang (Referenz), H2 von Rauschen im Ausgang (Vibrometer) beeinflusst; Phase gleich, Betrag verschieden; ohne Mittelung wird FRF statt H1/H2 gezeigt und die Kohärenz nicht angezeigt; H1/H2/COH sind unabhängig von der Mittelungsart; für Betriebsschwingformen sei H1 die bessere Wahl, weil weniger empfindlich gegen Ausgangsrauschen | [H][Repo] TM 3-4 bis 3-6, 6-5; HB 9-19, 9-21. Gleichungen 3.2-3.13 stehen im PDF als Bilder und wurden nicht gelesen |
| **Betriebsschwingformen** (R-052) | Animation der Banddaten bzw. der Daten bei gewählter Frequenz auf der Geometrie (Abschnitt 1.1, Schritt 4); in PSV ist der Begriff "Betriebsschwingform/ODS" im Handbuch nicht als Menüpunkt gefunden (Suche "Betriebsschwing" ohne Treffer in HB). Das Wort "Operational Deflection Shapes" kommt im SM nur beim MAC-Beispiel vor (SM 9-38) | [Repo] F11 Folien 7-10; SM 9-38 |
| **Peak/Dämpfung** (R-053) | Peak-Anpassung per Kleinste-Quadrate am 1-DOF-Oszillator; "Dämpfung" = volle Breite der angepassten Kurve bei 3 dB unter dem Maximum; Q = f_max/Dämpfung (Gl. 9.1); ζ = Dämpfung/(2 f_max) (Gl. 9.2), "nur für kleine Dämpfungen gültig"; nur für Spektren verfügbar. Folie nennt für das Maximum Â und die Höhe Â/√2 | [H][Repo] HB 9-11; HB-A 3-14; F11 Folie 34 |
| **Band-RMS** (R-053) | Effektivwert über den Bandcursor-Bereich (Statistik); Domäne "RMS" mit Banddaten und zusätzlichem Band "Entire Bandwidth"; ein Wert je Messpunkt; gespeichert werden RMS der Amplitude über die gesamte Bandbreite (Scan) | [H][Repo] HB 9-11, 10-8; F11 Folie 28; BEM `Access to Data` (nach I5 4.4) |
| **Eigene Rechnung im Signalprozessor** | Funktionen u. a. FFT, IFFT, Filter, Integrate/Differentiate, Resample, Statistik, CP, COH, FRF, H1, H2, AFFT mit Parametern Lines, Average, OverlapPercent, Window; Polytec-Beispiel für Band-RMS: abs, Extrakt des Bereichs, Quadrat, mean·N, RMS = (Summe/2)^0,5, "gültig nur wenn die 1. Frequenz = Frequenzauflösung" (erste Lösung) | [H][Repo] F11.1 Folien 13, 23-26; HB 9-33, 9-34 |
| **Punktbearbeitung** | Punkte ungültig setzen (ungültige Punkte werden im gemittelten Spektrum nicht berücksichtigt), interpolieren; Filterung/Interpolation der Animation: "für Rohdaten sollte Filterung und Interpolation abgeschaltet sein" | [H][Repo] F11 Folien 18, 31 |
| **Vergleich von Moden/Formen** | MAC-Beispiel im Signalprozessor (Beispielformel, "< 0,9 verschieden, > 0,9 ähnlich") | [H][Repo] SM 9-38 |
| **Mehrere Messungen** | Koppeln/Animieren, Kombinierte Datei (gleiches Koordinatensystem und gleiche Erfassungseinstellungen nötig) | [Repo] F11 Folien 35-38 |
| **Modalanalyse** | Nicht in PSV; Polytec verweist auf Export an Modalanalyse-Software; MIMO-FRF-Hinweis zur Multireferenz-Weitergabe (PCA-Option) | [H][Repo] SM 7-10/7-11; HB 10-15 |

### 1.3 Ein- und Ausgabeformate

| Format | Inhalt/Einschränkung | Beleg |
|---|---|---|
| `.svd` | proprietäres Binärformat, Scandaten: Einstellungen, Einzelspektren aller vollständig gemessenen Punkte, gemitteltes Spektrum, RMS über die gesamte Bandbreite; bei Abbruch bleiben gemessene Punkte erhalten | [H][Repo] HB 10-8 |
| `.pvd` | proprietäres Binärformat Einpunktdaten: Zeitsignale, Spektren, Parameter | [H][Repo] HB 10-9 |
| `.set` | proprietäres Binärformat Einstellungen | [H][Repo] HB 10-8 |
| `.spd` | Signalprozessor-Dokument | [Repo] HB 10-8; F11.1 |
| **ASCII** | Messdaten nur in der Auswertung, es werden die *angezeigten* Daten exportiert; "für ASCII Export Anzeige auf Punktdaten und Einzelner Scanpunkt, für jeden Punkt wird eine einzelne Textdatei erstellt"; Zwischenablage (Strg+C) | [Repo] F11 Folien 11-13; HB 10-12; I5 3.7 |
| **Universal File (UFF)** | Datensätze 151, 164, 2411, 2412+82, 55 (Bänder), 58 und 58b (Scanpunkte); Messwerte in einfacher Genauigkeit, Koordinaten doppelt; nicht im APS-Modus; Punkte "Nicht gemessen" werden nicht exportiert; MultiFrame in einer Datei; Dateiendungen `.unv`, `.uff`, `.asc` | [H][Repo] HB 10-15 |
| **UFF-Import** | Import in die Auswertung als Usr-Kanal, "Sinn bei Vergleich von Modalanalyse-Ergebnissen mit der Messung" | [Repo] F11 Folie 39 |
| ME'scope | `*.str, *.blk, *.shp`, nur mit Option ExpME | [H][Repo] HB 10-8 (Aufzählung), 10-19 (Index); I5 3.7 |
| ASAM ODS ATFX | `*.atfx`, nur mit Option ExpASAM | [H][Repo] HB 10-21; I5 3.7 |
| STL, Geometrie-ASCII | Geometrien | [Repo] HB 10-14, 10-18 |
| Release 10.1: Binary UFF | Binär-UFF "beschleunigt Import/Export"; PSV-Seite nennt "Open interface ... with Polytec File Access" | [H][Lit-S] polytec.com PSV-Software-Seite (Suchtreffer, nicht abgerufen) |

Per COM kann der Export automatisiert werden (`Exporter`, `ExportParameters` mit `PointSignals`, `BandSignals`, `ExportBinary` u. a.; Eingabedatei `.pvd/.svd/.mvd/.set`) [Repo: BEM `PSV~Application~Exporter`, `PSV~ExportParameters_members`, I5 3.7]. Ein COM-Exporttyp "ASCII" existiert nicht (BEM `PSV~PTCExportType`, I5 3.7).

### 1.4 Datenzugriff ohne PSV-Oberfläche: Polytec File Access (PFA)

- **Funktion** [H][Repo: PFA `_Konzept/Overview`]: COM-Objektsammlung für den Zugriff auf "most of the information" in PSV-, MPV- und VibSoft-Messdateien und Einstellungsdateien; sprachunabhängig über COM (VBA, VBS, Delphi, C++ genannt); Beispiele in VBA (Excel, PSV/VibSoft Basic Engine) und Visual C++; Zielgruppe "programmers who have experience ... in the access to COM objects"; die Dateien werden "Polytecs proprietary file formats" genannt.
- **Lesbare Dateien:** PSV-Dateien ab Version 7.0, VibSoft ab 3.0 [Repo: PFA `Opening and Closing Files`].
- **Datenmodell** [Repo: BEM `Access to Data`, I5 4.3/4.4]: Domänen (Time, FFT, RMS, 1/3 Octave) → Kanäle → Signale → Displays → Datenpunkte; Rückgabe als 0-basiertes Single-Array; komplexe Größen verschränkt; 3D-Kanal erst alle x, dann y, dann z; Frame-Semantik; gemitteltes Spektrum über `GetPointAverageDomains`; Bänder über `DataBand.GetData`; Geometrie über `MeasPoints.CoordinatesToArray`; Punktstatus als Bitmaske; Videobild über `Infos.VideoBitmap`.
- **Schreiben:** Benutzersignale (Kanal "Usr") und neue Dateien möglich (`PolyFile.Create`, überschreibt vorhandene Dateien); Polytec-Beispiele verändern die Messdatei [Repo: I5 4.6].
- **Plattform:** COM ist Windows-Technik; die Dokumente nennen keine andere Plattform. Die CHM nennt als Beispielpfad `C:\Program Files\Polytec\File Access` [Repo: PFA Overview]; F11.2 nennt `C:\Program Files\Polytec\Polytec File Access 5.6\Examples\Matlab` [Repo: F11.2 Folie 3]. Eine ausdrückliche Aussage "nur Windows" steht in den Dokumenten nicht; I5 4.1 trägt diese Folgerung als eigene Einordnung.
- **Lizenz/Bezug** [H][Repo: F11.2 Folien 2]: "Kein Dongle erforderlich", "Direkter Zugriff auf .pvd und .svd Dateien (z. B. mit Matlab)", "Über 'Polytec-Update' verfügbar". Weitere Lizenzbedingungen (Weitergabe, Lizenztext, EULA) stehen **weder in der PFA-CHM noch im BEM** (Suche nach "licen/dongle" im Textauszug ohne Treffer). PFA-Installation: "as described in Release Notes.doc on your Polytec File Access CD" [Repo: PFA Overview], diese Datei liegt nicht im Repo.
  Zusätzlich [H][Lit-S]: Suchtreffer zur Polytec-Update-Seite nennen "Polytec File Access Software (release 5.0 or higher)" als über Polytec Update beziehbar; Seite nicht abgerufen.
- **Einschränkung** [Repo: PFA `Opening and Closing Files`]: Eine Datei darf nicht gleichzeitig mehrfach geöffnet werden (nicht doppelt durch PFA und nicht zugleich in PSV), sonst Sharing Violation; je PolyFile-Objekt nur eine Datei.
- **Matlab/Excel-Beispiele** [Repo: F11.2 Folien 4-13]: `GetPointData.m` mit Parametern Dateiname, Domäne, Kanal, Signal, Display, Punkt, Frame (Groß-/Kleinschreibung beachten, deutsche Schreibweise geht auch), `GetVideoImage.m`, `GetXYZCoordinates.m`; Warnung: Im Skript wird der ursprüngliche Punktindex angegeben, Vorsicht bei in PSV geänderten Indizes. Das Beispiel zeigt eine FFT-Achse 12,5 bis 5000 Hz mit 400 Linien (I5 4.4).
- **Ausstattung der Hilfe zur Auswertung:** Neben dem Datenzugriff liegen in `PolyMathLib` Rechenobjekte, die dieselben Rechnungen wie die GUI anbieten: `SignalProcessing` (u. a. `H1FromTimeSignal`, `H2FromTimeSignal`, `CoherenceFromTimeSignal`, `AverageFFTFromTimeSignal`, `WindowFunction`), `PeakFinder` (lokale Maxima mit `MinimumAmplitude`, `MinimumDistance`, `MinimumProminence`, `RelativeHeightForWidth`; `DataPeak.PeakWidth/PeakProminence`), `PeakFit` (1-DOF-Oszillator an reales oder komplexes Spektrum, `GetPeak`, `GetWidth(dHeightDb, vbDbA)`, "does not support logarithmic spectra") [Repo: BEM `PolyMathLib/SignalProcessing`, `PeakFinder`, `DataPeak`, `PeakFit`]. Der Algorithmus (Fitfunktion, Fenster der Anpassung, Gewichtung) ist dort nicht beschrieben.

### 1.5 Grenzen bzw. bekannte Einschränkungen (nur belegte)

- Phase nur mit Referenz oder Trigger definiert; ohne beides gilt Phase 0 bzw. "not available" (TM 6-6, Tab. 6.1); bei Betragsmittelung wird die Phase aus dem Kreuzspektrum nachträglich zugewiesen und "makes sense only if there is some phase correlation" (TM 6-5) [H][Repo].
- Das Vibrometersignal darf nicht als Trigger dienen, da die Phasenlage ortsabhängig ist (TM 6-5) [H][Repo].
- Ohne Mittelung: keine H1/H2, Kohärenz 1 und nicht angezeigt (TM 3-5) [H][Repo].
- Dämpfung/ζ aus Peak-Anpassung nur für kleine Dämpfungen gültig (HB 9-11) [H][Repo]. Zur Genauigkeit der Anpassung macht Polytec keine Angabe.
- PSV bildet das Punktmittel nur als Amplitudenmittel, ein komplexes Punktmittel gibt es nicht ("This functionality is not built into PSV", Beispiel `ComplexPointAverage.bas`) [H][Repo: PFA `Examples`].
- Der ASCII-Export liefert nur die angezeigte Darstellung, eine Datei je Punkt [Repo: F11 Folie 13].
- UFF-Export: einfache Genauigkeit der Messwerte, Punkte "Nicht gemessen" fehlen, nicht im APS-Modus [H][Repo: HB 10-15].
- Mehrfachreferenz-FRFs sind nicht ohne weiteres in Multireferenz-Verfahren der Modalsoftware einsetzbar; nötig ist die Zerlegung (PCA-Option, nur für unkorrelierte Referenzen) [H][Repo: SM 7-10, 7-11].
- Gleichungen 3.2-3.13 des TM sind **nicht** als Text verfügbar. Sie sind in der Fachgrundlage gegen Bendat/Piersol zu belegen, nicht aus dem TM-Text.
- Versionsbezug: HB/SM = PSV 10.1, TM = Stand Software 9.1; CHM-Hilfen mindestens PSV 10.4 (I5-Vorwort). Die Dokumente sind nicht auf Übereinstimmung geprüft.

---

## 2 Bereich B: Andere Werkzeuge

**Gesamtlage:** Für diesen Bereich wurde nur über Suchtreffer recherchiert (Hersteller-/Projektseiten waren nicht abrufbar, Ausnahme GitHub). Jede Aussage hier hat Prüfstand [Lit-S], sofern nicht anders vermerkt.

### 2.1 MATLAB (Signal Processing Toolbox)

- `tfestimate` schätzt Übertragungsfunktionen, Schätzer wählbar 'H1' oder 'H2', 'mimo' für Matrixeingänge; Überlappung `noverlap`, Abtastrate `fs` [Lit-S: `mathworkstfestimate`, Spiegel einer R2020b-Hilfe, nicht mathworks.com].
- `modalfit` schätzt Eigenfrequenzen, Dämpfungsgrade und Moden aus FRF in Receptance-Form (FRF aus `modalfrf`); Option `'FitMethod','PP'` (Peak-Picking), außerdem u. a. `'lsrf'`; auch aus identifizierten Modellen (`tfest`). Vollständige Methodenliste nicht bestätigt [Lit-S: `mathworksmodalfit`].
- `mscohere` (Kohärenz): nur Hinweis in einem Octave-Forge-Changelog, keine Dokumentation gefunden.
- Polytec-Dateien in MATLAB: **[H][Repo]** Polytec-Beispielskripte über PFA (`GetPointData.m` usw.), siehe 1.4.
- Ein-/Ausgabeformate: nicht ermittelt (UFF-Leser in MATLAB nicht recherchiert).

### 2.2 Python

- **scipy.signal**: `coherence` schätzt die Magnitude-Squared-Coherence nach Welch, Cxy = |Pxy|²/(Pxx·Pyy); `csd`, `welch` als verwandte Funktionen; die Voreinstellungen des Fensters und von `nperseg` ändern sich zwischen Versionen (ältere: 'hanning', 256; 1.17: 'hann_periodic', `nperseg=None`); 50 % Überlappung beim Hann-Fenster empfohlen [Lit-S: `scipycoherence`]. Welch-Methode als Primärliteratur: `welch1967periodogram` (nur `metadaten`).
  `scipy.signal` enthält nach den Treffern keinen fertigen H1/H2-Schätzer; aus `csd` und `welch` lassen sie sich zusammensetzen. Diese Folgerung ist nicht belegt, ein Beleg in der SciPy-Dokumentation für "kein H1/H2" wurde nicht gesucht.
- **pyuff / sdypy-io**: Lesen und Schreiben von UFF-Datensätzen 15, 55, 58, 58b, 82, 151, 164 und 24xx (Listung auf PyPI, Version 2.5.1 laut Treffer); `read_sets()`, Datensatz 58 mit Feldern `x` (Abszisse) und `data` (Ordinate, komplex); `prepare_58(...)` und `write_set(...)` zum Schreiben; sdypy-io ist ein Wrapper um pyuff [Lit-S: `pyuff`].
- **pyEMA / sdypy-EMA** (Experimentelle und operationelle Modalanalyse): Ablauf aus FRF-Matrix und Frequenzachse → Pole berechnen → stabile Pole im Stabilitätsdiagramm wählen → Modalkonstanten (LSFD, proportionale Dämpfung angenommen); wählbare FRF-Art (Beschleunigung, Geschwindigkeit, Weg). Ob LSCF enthalten ist, ist nicht bestätigt. Kein begutachteter Fachartikel gefunden [Lit-S: `sdypyema`].
- **Open-Source-Leser für Polytec-Dateien:** siehe Abschnitt 4.

### 2.3 Siemens Simcenter Testlab

- ODS-Auswertung: Geometrie aus Testknoten und Verbindungen (CAD-Import möglich), Verbindungen nur zur Anschauung; Knotennamen der Geometrie müssen zu den Messdaten passen (Alias-Mapping); ODS-Animation setzt erhaltene Phase voraus (alle Kanäle gleichzeitig oder Phasenreferenzkanal) [H][Lit-S: Siemens-Knowledge-Artikel, Suchtreffer-Zusammenfassungen, Seiten nicht abgerufen].
- Polytec-Anbindung: Einzelpunkt-Vibrometer (VibroGo) analog über SCADAS-Hardware; scannende Vibrometer über eine "universal file"; bei Polytec-Empfindlichkeit 25 mm/s/V soll Testlab 40 mV/(mm/s) eingestellt werden [H][Lit-S: `siemenstestlabpolytec`].
- Ob Testlab das PSV-UFF direkt als Geometrie samt Messdaten importiert, ist nicht bestätigt.

### 2.4 Vibrant ME'scope

- Importiert nach Herstellerseiten Mehrkanal-Zeit- oder Frequenzdaten aus Dateien; zeigt 3D-Animation von Betriebsschwingformen und Moden [H][Lit-S: rms-reliability.com, acsoft.co.uk, etesters.com (Händlerseiten)].
- Polytec selbst bietet den ME'scope-Export (Option ExpME) [H][Repo: HB 10-8, 10-19]. Welche Importfilter ME'scope für Polytec-Dateien besitzt, ist nicht belegt.

### 2.5 Polytec-eigene weitere Software (Herstellerangaben)

- **ScanViewer**: kostenlose, vereinfachte Auswertung, die nur Banddaten animiert; öffnet auch normale Scandateien mit Banddefinitionen; keine Animation von Zeitdaten [H][Repo: F11 Folie 29].
- PolyWave-Suite mit ODS-Modul (Zeit- und Frequenzbereich) [H][Lit-S: Polytec-Broschüre PolyWave, nur Suchtreffer]; RoboVib-Broschüre: Software kann Geometrie- und Schwingungsdaten in gängigen Formaten importieren/exportieren, einschließlich ASAM ODS [H][Lit-S].

---

## 3 Bereich C: Verfahren in der Fachliteratur

**Wichtig:** Für diesen Bereich wurde in W1 **kein Volltext gelesen**. Die Literatur aus `literatur.bib` hat nur den Prüfstand `metadaten`. Die folgende Tabelle ordnet nur zu, *welche* Quelle für *welches* Verfahren als Beleg vorgesehen ist, und welche Aussage heute **ohne Volltext** nur aus den Polytec-Dokumenten oder Suchtreffern kommt. Keine der Zuordnungen ist ein inhaltlicher Beleg.

| Verfahren | Vorgesehene Primärquelle (`bibkey`) | Prüfstand | Heute belegte Aussage aus anderer Quelle |
|---|---|---|---|
| Spektrumschätzung, Fenster, Leckage, Mittelung (Welch) | `welch1967periodogram`, `harris1978windows`, `heinzel2002spectrum`, `bendat2010random`, `brandt2011noise` | metadaten | Polytec-Skalierung und Fensterliste: TM 3-3 [H][Repo] (Fensterkapitel 5 nicht ausgewertet). SciPy-Welch-Methode: Suchtreffer |
| FRF H1/H2, Kohärenz | `bendat2010random`, `brandt2011noise`, `pintelon2012system` | metadaten | Verhalten bei Eingangs-/Ausgangsrauschen und Wahl von H1 für ODS: nur TM 3-4 bis 3-6 [H][Repo]. Aussage zum Verhalten in Bendat/Piersol **nicht geprüft** |
| Betriebsschwingform (ODS) vs. Mode Shape | `schwarz1999ods` (neu, `metadaten`, unsicher) | metadaten | Nur Suchtreffer-Auszug: ODS enthält erzwungene *und* resonante Schwingungsanteile, Mode Shape nur resonante [Lit-S] |
| Peak-Picking, Halbwertsbreite (−3 dB), Dämpfungsschätzung | `ewins2000modal` (Standardwerk, `metadaten`), `maia1997theoretical` | metadaten | Die Aussage, dass −3 dB bei Amplitude A/√2 liegt, stammt aus F11 Folie 34 [H][Repo], nicht aus Ewins. Ewins' Halbwertsmethode ist nicht gelesen, ihre Herleitung steht noch aus |
| Band-RMS | `bendat2010random` (Parseval-Zusammenhang) | metadaten | Polytec-Rechenweg: RMS = (Summe |X|²/2)^0,5 über Linien des Bands bei Null-Spitze-Skalierung (F11.1 Folien 24-26) [H][Repo] |
| Modalparameter-Identifikation (Ausblick) | `ewins2000modal`, `maia1997theoretical`, `allemang1986survey`, `allemang2003mac`; Software: `sdypyema`, `mathworksmodalfit` | metadaten | Software-Beschreibungen nur aus Suchtreffern; kein Fachartikel zu pyEMA gefunden |
| Scanning-LDV: 3D-Zerlegung, Unsicherheit | `rothberg2017ldvreview`, `rothberg2012framework`, `chen2021threesldv` | metadaten | Einordnung der Messunsicherheit aus der Hersteller-Theorie nicht ausgewertet |

Weitere Hinweise:
- Die Leseliste (Feld 3) und Bericht I2 nennen die Verfahren; die W1-Recherche hat keine neue begutachtete Quelle für H1/H2, ODS oder Peak-Picking hinzugefügt, weil die bestehenden Standardwerke bereits die vorgesehenen Quellen sind.
- Neu aufgenommen wurde nur `schwarz1999ods` (graue Literatur, unsicher, siehe `.bib`-Note). Als Fachquelle ist sie nur mit Vermerk "Herstellerbeitrag/Konferenzvortrag" zitierfähig.

---

## 4 Antworten auf die Schlüsselfragen zu `.svd` und Polytec File Access

**4.1 Was dokumentiert Polytec zum Dateiformat `.svd`?**

- `.svd` ist ein "proprietäres Binärformat" für Scandaten; Inhalt grob: Einstellungen, Einzelspektren, gemitteltes Spektrum, RMS über die Bandbreite (HB 10-8) [H][Repo]. Außerdem können Zeitdaten gespeichert werden (nur, wenn dies eingestellt war; vgl. I5 4.4 zu `SaveTimeDataForScan`) und Benutzerdaten (Usr-Kanal) angefügt werden [Repo: F11.1 Folie 10/14].
- PFA nennt die Formate "Polytecs proprietary file formats" [H][Repo: PFA Overview].
- **Eine Formatspezifikation (Byte-Layout, Header, Struktur) ist in keinem ausgewerteten Repo-Dokument enthalten.** Geprüft: Textsuche nach "Dateiformat/file format/proprietary/binary" in HB (nur Treffer zu Protokolldatei, Bild- und UFF-Formaten) und in den CHM-Textauszügen (nur PFA-Overview-Satz). Die öffentliche Zugänglichkeit einer Spezifikation außerhalb des Repos wurde nicht prüfbar (polytec.com nicht abrufbar). Eine Aussage "es gibt keine öffentliche Spezifikation" ist daher **nicht belegt**; belegt ist nur "keine in den Repo-Dokumenten".
- Fileinfo.com listet `.svd` als Polytec-Datei mit kurzer Beschreibung [Lit-S, nur Suchtreffer, keine Spezifikation]. Es gibt eine Namensgleichheit mit CMSIS-SVD (Mikrocontroller-Registerbeschreibungen), die hier **nichts** mit Polytec zu tun hat; PyPI-Pakete wie `svd2py` und `svdsuite` betreffen dieses andere Format [Lit-S].
- Parallel läuft die Entschlüsselung einer `.svd` durch einen anderen Agenten; W1 hat sich damit nicht befasst.

**4.2 Was dokumentiert Polytec zu Polytec File Access (Funktionen, Plattform, Lizenz)?**

| Aspekt | Belegte Angabe | Beleg |
|---|---|---|
| Funktionen | Lesen (und Schreiben von Benutzerdaten/neuen Dateien) aller Domänen, Kanäle, Signale, Displays, Punkte, Frames, Bänder, Geometrie, Status, Metadaten, Videobild; Objektmodell mit Typbibliotheken POLYFILELib, POLYSIGNALLib, POLYMATHLib u. a. | [H][Repo] PFA Overview, `_Konzept/*`, I5 Abschn. 1, 4 |
| Technik | COM-Objekte "according to the standard Component Object Model of Microsoft"; Zugriff aus jeder COM-fähigen Sprache; Basic Engine von PSV/VibSoft kann sie auch nutzen | [H][Repo] PFA Overview |
| Plattform | COM = Windows; Beispielpfade unter `C:\Program Files\...`; eine ausdrückliche Plattformliste (Windows-Versionen, Bitness) steht nicht im Textauszug | [Repo] PFA Overview; F11.2; I5 4.1/7 |
| Lizenz | "Kein Dongle erforderlich"; bezogen über "Polytec-Update". Lizenztext/Nutzungsbedingungen nicht im Repo; Release Notes (CD) nicht im Repo | [H][Repo] F11.2 Folie 2; PFA Overview |
| Versionen | Beispiel PFA 5.6 (F11.2); Suchtreffer: über Polytec Update ab Release 5.0 | [Repo] F11.2 Folie 3; [Lit-S] |
| Dateiversionen | PSV-Dateien ab 7.0, VibSoft ab 3.0 | [H][Repo] PFA `Opening and Closing Files` |
| Einschränkung | Sharing Violation bei mehrfachem Öffnen; kein Zugriff, solange PSV die Datei offen hat | [H][Repo] PFA `Opening and Closing Files` |

**4.3 Gibt es öffentliche Hinweise/Projekte, die `.svd` ohne Polytec-Software lesen?**

- Gefunden wurde **ein** Projekt, das `.svd` aus Python liest: **imec-int/PolytecController** (GitHub, MIT-Lizenz). Es liest `.svd/.pvd` aber **über Polytec File Access** (`polyfile.py`, Klasse `Svd` mit `print_available_data()`, `get_point_data(...)`, `plot_image(...)`, `get_image()`), ist also kein eigenständiger Leser. README: PFA muss installiert sein (bezogen über Polytec Update), PSV Acquisition/VibSoft (Lizenz/Dongle) werden nur für die Gerätesteuerung gebraucht, nicht für das Lesen von Dateien; inoffizielles Projekt ohne Polytec-Support; Windows-Bezug über Pfade und `win32com` (Troubleshooting) erkennbar, aber nicht ausdrücklich verlangt [Volltext der GitHub-Seite per Abruf, Quellcode nicht geprüft; Eintrag `imecpolytec`].
- Ein Open-Source-Leser, der das Binärformat **selbst** ohne PFA/COM dekodiert, wurde **nicht gefunden** (Suchanfrage auf Deutsch/Englisch nach .svd-Leser in Python). Das ist ein negativer Suchbefund, kein Beweis der Nichtexistenz; nur eine Suchmaschinenanfrage wurde gemacht, GitHub-Codesuche (`search_code`) wurde nicht ausgeführt.
- Ein Suchtreffer nennt eine MATLAB-Toolbox der RTU Riga (vct.rtu.lv/software.html), die "SVD-Dateien" für Knickanalysen einliest; sie bezieht sich laut Beschreibung auf Singulärwertzerlegung, nicht auf Polytec, und ist für diese Frage unbrauchbar [Lit-S].
- Der UFF-Export ist der dokumentierte plattformneutrale Weg ohne PFA (mit PSV im Besitz): pyuff liest Datensatz 58/58b, 55, 151, 164, 2411/2412 [Lit-S: `pyuff`; Repo: HB 10-15, I5 4.1]. Voraussetzung ist der Export aus PSV (Einschränkungen siehe 1.3).

---

## 5 Zuordnung der Lastenheft-Anforderungen zu den Belegen (nur Bestandsaufnahme)

| Anforderung | Was PSV laut Hersteller dafür bietet | Belegstelle | Was zusätzlich zu klären ist (offen, kein Urteil) |
|---|---|---|---|
| R-050 Spektren | Einzelspektrum, gemitteltes Spektrum; Amplitudenskalierung Null-Spitze | TM 3-3, F11 5-6 | Ob die Datei Spitzen- oder Effektivwerte liefert, ist laut I5 4.4 an einer realen Datei zu bestätigen; gemitteltes Spektrum = Amplitudenmittel der gültigen Punkte (PFA Examples) |
| R-051 H1/H2/Kohärenz | in der Datei als Kombikanal-Signale, wenn Referenz aktiv war | TM 3-4 bis 3-6; I5 4.3 | Referenzgröße/Einheit (O4); Gleichungen des TM nur als Bilder, nicht lesbar |
| R-052 ODS | Animation auf Geometrie; Phase nur mit Referenz/Trigger | TM 6-6; F11 7-10 | Zuordnung Real/Imag zu 3D-Vektor und Vorzeichen (I5 4.4 [offen]) |
| R-053 Peaks/Dämpfung | Band-Cursor-Peak-Anpassung, Gl. 9.1/9.2; Band-RMS | HB 9-11; F11 28, 34; F11.1 24-26 | Algorithmus der Anpassung unbeschrieben (BEM `PeakFit` nennt nur "least squares"); Fenster der Anpassung und Gewichtung unbekannt; Erwartung "Werte stimmen mit PSV überein" ist daher nur im Rahmen der Beschreibung prüfbar |

---

## 6 Lücken (keine belastbare Quelle gefunden)

1. Formatspezifikation `.svd`: nicht in den Repo-Dokumenten; öffentliche Verfügbarkeit nicht prüfbar (polytec.com gesperrt).
2. PFA-Lizenztext, Plattformliste und Bitness: nicht in den Repo-Dokumenten. Nur "kein Dongle", "Polytec Update". Release Notes (CD) fehlen.
3. Polytec-Seiten (PSV-Software, Polytec Update, Downloads): nur Suchtreffer-Zusammenfassungen, nicht abgerufen.
4. Gleichungen 3.2-3.13 (AP, CP, FRF, H1, H2, COH) und Fensterkenngrößen (Tab. 5.1) des Theory Manual stehen als Bilder und wurden nicht gelesen. Für die Fachgrundlage ist Bendat/Piersol maßgeblich (Volltext nötig).
5. Algorithmus der PSV-Peak-Anpassung (PeakFit/Band-Cursor): nur Kurzbeschreibung; kein Quelltext, keine Gleichung für die Fitfunktion.
6. Wie PSV-Anzeigewerte für Betrag/Phase auf einem Vektorkanal 3D definiert sind: weiterhin offen (I5 4.4).
7. Betriebsschwingform als Begriff in PSV: im HB nicht gefunden; Begriffsverwendung am Gerät bzw. in HB-A prüfen (HB-A nur teilweise gelesen).
8. Andere Werkzeuge: Testlab-Importpfad für PSV-UFF, ME'scope-Importfilter für Polytec, MATLAB-UFF-Leser, Python-`scipy.signal` H1/H2: nicht belegt.
9. Begutachtete Quelle zu pyEMA/sdypy: keine gefunden. Zitierfähig nur als Software mit Version.
10. Mathworks-Dokumentation: offizielle Seiten nicht abgerufen; `tfestimate` nur über Spiegel.
11. Open-Source-Leser für `.svd` ohne PFA: nicht gefunden (siehe 4.3), GitHub-Codesuche nicht ausgeführt.
12. Keine Quelle zu Ergebnisvergleichen zwischen PSV-Auswertung und eigener Python-Auswertung (z. B. Abweichungen bei Fensterkorrektur und Mittelung) gefunden.

## 7 Quellenverzeichnis W1 (Schlüssel in `literatur.bib`)

| bibkey | Quelle | Prüfstand |
|---|---|---|
| polytec2022psvhandbuch | Software-Handbuch PSV-Datenerfassung 10.1 (DE), 41584 | volltext teilweise |
| polytec2022psvdesktop | Software-Handbuch Auswertung 10.1 (DE), 41596 | volltext teilweise |
| polytec2022psvsoftware | Software Manual PSV 10.1 (EN), 41585 | volltext teilweise (SM 7-10, 7-11, 9-38 gelesen) |
| polytec2015theory | Theory Manual (Stand 9.1) | volltext teilweise (Kap. 3, 6, 7 gelesen) |
| polytec2023psvauswertung, polytec2021signalprozessor, polytec2021fileaccessmatlab | Schulungsfolien 11, 11.1, 11.2 | volltext (Folientext) |
| polytecbem, polytecpfa | CHM-Hilfen, Textauszug im Repo | Dokumentation im Repo |
| polytec2025com | COM-Folien | wie bisher |
| imecpolytec | GitHub imec-int/PolytecController | metadaten (README gelesen) |
| pyuff, sdypyema, scipycoherence, mathworksmodalfit, mathworkstfestimate, siemenstestlabpolytec | Softwaredokumentation/Hersteller | metadaten (nur Suchtreffer) |
| schwarz1999ods | Schwarz/Richardson 1999 | metadaten, unsicher |
