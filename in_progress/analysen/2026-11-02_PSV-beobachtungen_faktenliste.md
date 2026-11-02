# Beobachtungen zur PSV-Software am Messrechner (2026-11-02) – Faktenliste

Zusammengestellt vom Orchestrator aus dem Termin am Messrechner (BEOWOLF, 14:30–17:00).
Nur Beobachtungen mit Beleg; **[V]** = Vermutung/Deutung. Belege: Screenshots/Fotos im Chat
(werden mit dem Laborbuch unter `in_progress/versuche/2026-11-02_prototyp/fotos/` abgelegt),
Dateien unter `in_progress/versuche/erkundung/erkundung_BEOWOLF_2026-11-02_*`,
`in_progress/versuche/2026-11-02_prototyp/ergebnisse_7b.md`, `golden_punkt1_label132.csv`.

## A Installation und Programmumgebung

| Nr | Beobachtung | Beleg |
|---|---|---|
| A1 | PSV 10.2, 10.3, 10.4 parallel installiert; laufend 10.4 (`C:\Program Files\Polytec\PSV 10.4\PSV.exe`, Datei vom 01.10.2026), Version 10.4.0.1 | Erkundung 150024 (Verzeichnisse, Prozess), Screenshot PSV-Info |
| A2 | Weitere Polytec-Programme: File Access 6.3–6.6, Scan Viewer 3.1, Strain Processor 2.9–3.1, TMS 4.5/4.6, TMS Viewer, Configuration Tool, Diagnostic Report, Vibrometer Service Tool, Polytec Update | Erkundung 150024 (P1-3) |
| A3 | Zwei Verknüpfungen je Sprache: „PSV 10.4 Deutsch“ = `PSV.exe /Acquisition /german`, „PSV 10.4 Desktop Deutsch“ = `PSV.exe /Desktop /german`. Fenstertitel im Auswertebetrieb: „PSV Auswertung“ | PowerShell-Ausgabe .lnk, Screenshots |
| A4 | Laut Basic Engine Manual ist `AcquisitionInstance` in Desktop-Versionen nicht verfügbar | I1-Analyse, [BEM] |
| A5 | **Keine PSV-COM-Registrierung** (`PSV.AcquisitionInstance`, `PresentationInstance`, `Application` fehlen; keine „Polytec PSV Type Library“). Registriert: `PolyFile.PolyFile` (In-Process, 32/64 Bit), `PolyWaveforms`. 186 Polytec-Typbibliotheken | Erkundung 143255/150024 |
| A6 | Release Notes 10.4: bei parallel installierten Versionen `PSV.exe /regserver` als Admin im Installationsordner bzw. Reparaturinstallation; Fehlermeldung „basic engine is not available, because the software is not registered as COM-server“ | Release Notes deu.htm (Ausschnitt im Chat) |
| A7 | Programmordner enthält `Polytec.COM.Manifest`, `Polytec.PDx.Manifest` (registrierungsfreie COM-Komponenten **[V]**), viele `PDx*.dll` (u. a. PDxFRF, PDxCoherence, PDxPCA, PDxSineFit, PDxResample, PDxDigitalFilter), `PolyUFFExport.dll`, `PolyAtfxExport.dll`, `PolyMEScopeExport.dll`, ONNX-Modelle (`sam_vit_h…onnx`) | `dir` des Programmordners |
| A8 | Doku im Programmordner: Basic Engine Manual.chm, Software Handbuch/Manual PSV (PDF), Theory Manual.pdf, MSA/MSA 3D/Stage/UHF/VibroScan-Handbücher, Release Notes, 3DAlignmentScanManual.mp4, Lizenztexte | `dir …\Doc` |
| A9 | Messrechner: Windows 10, Python 3.11.9 vorhanden, Internet vorhanden, PyCharm installiert; Messdaten mehrerer Projekte/Personen unter `D:\Messdaten\…` (gemeinsamer Rechner) | Chat, Screenshots Projekt-Browser |
| A10 | Zeitweise zwei PSV-Prozesse gleichzeitig (14:32) | Erkundung 143255 |

## B Lizenzen und Hardware

| Nr | Beobachtung | Beleg |
|---|---|---|
| B1 | Optionen: PSV-S-100K, Acq3D, Ch4, Ch8, FaScn, GeoPro, ImpGeo, SIG, SigPro, Strain, **TDD (Zeitdaten)**, **VBEng (Basic Engine und File Access)**; Hardware: Polytec Frontend, PolyEthernet, WDM Video; **keine PCA**; Wartung/Ablauf unbegrenzt | Screenshot Optionen |
| B2 | File Access liest Hardware: AcqBoardFirmwareVersion 1.0302, AcqBoardChannelCount 11, FrontEnd 124, FrontEndFirmwareVersion 2.50; AcqBoardName und GeneratorName nicht lesbar (com_error) | Erkundung 161125 |
| B3 | Aufbau: drei PSV-Scanköpfe auf Stativen; Blech frei an zwei Seilen, weiß besprüht, Kreuzmarkierung; Impedanzkopf PCB 288D01 SN 3853 (richtig montiert), TMS Mini SmartShaker (Typschild teilweise „K2…“, **[V]** K2007E01) mit eingebautem Verstärker, Stinger mit Kunststoffkupplungen | Fotos |

## C Datei und Messeinstellungen (File Access, Beispieldatei 20261012_ref_Mitte)

| Nr | Beobachtung | Beleg |
|---|---|---|
| C1 | FFT: Bandwidth 1000 Hz, 0–1000 Hz, 1600 Linien, SampleFrequency 2500 Hz, Δf 0,625 Hz, SampleTime 1,6 s, 4000 Samples, Overlap 0; XAxis 0,625…1000 Hz | einstellungen_lesen, Erkundung 161125 |
| C2 | Mittelung komplex, 7; SE am Vibrometerkanal an; Trigger aus, PhaseFromRef True; SaveTimeDataForScan False; RealSampleFrequency 250 000; AutoRemeasure aus | einstellungen_lesen |
| C3 | Generator aktiv, 0,02 V, MultipleChannels True; Wellenform-Parameter per dynamischem Dispatch nicht lesbar (Cast nötig) | einstellungen_lesen |
| C4 | Kanäle: Vib 3D (0,05 (m/s)/V, DirectionOfVibration 6, SignalDelay 1,3336 ms); Ref1 Kraft 40,306 N/V ICP (SignalDelay 0,13076 ms); Ref2 Beschl. 97,847 (m/s²)/V ICP; Ref3–Ref8 inaktiv (Ref5 mit 937 (m/s²)/V, Richtung 4 voreingestellt); Fenster 0, RMS-Korrektur 1,0 | einstellungen_lesen |
| C5 | Domänen in der Datei: „FFT“ und „Terzen“; Kanäle je Domäne u. a. Vib X/Y/Z, Ref1, Ref2, Vib X/Y/Z & Ref1/Ref2, Ref2 & Ref1; Signale Weg/Geschwindigkeit/Beschleunigung, AP, PSD, ESD, CP, H1, H2; Displays Amplitude, dB, dB(A), Ampl.&Phase, Phase, Real, Imaginär | Erkundung 161125 (P1-10-struktur) |
| C6 | „Ref1 | Kraft“ hat keine Real/Imag-Darstellung; „Ref2 & Ref1 | H1 Beschleunigung / Kraft“ nicht über diesen Namen lesbar | daten_lesen |
| C7 | File Access liefert dieselben Werte wie der eigene Leser (Spektren bitgleich, H1 auf 1e-8) und arbeitet ohne PSV-COM-Registrierung, solange die Datei nicht in PSV offen ist | ergebnisse_7b.md |
| C8 | SummaryInfo/Version: FileTime 2026-10-12T11:32:52, ProgramVersion 10.4.0.1 | Erkundung 161125 |

## D Bedienung der PSV-Auswertung (Analysator)

| Nr | Beobachtung | Beleg |
|---|---|---|
| D1 | Ansichten-Menü (Symbol links in der zweiten Symbolleiste): Banddaten (Alt+5) / Punktdaten (Alt+6); Messobjekt (Alt+1), Einzelner Scanpunkt (Alt+2), Gemitteltes Spektrum (Alt+3), Profil (Alt+4) | Screenshot |
| D2 | Kanalwahl: Vib 3D, Ref1, Ref2, Vib 3D & Ref1, Vib 3D & Ref2, Ref2 & Ref1; Komponenten X/Y/Z einzeln zuschaltbar | Screenshots |
| D3 | Menü Analysator: Domäne, Kanal, Signal, Anzeigeart; Cursor, Differenz-Cursor, Band-Cursor, Harmonischer Cursor, Bänder auswählen; Cursor-Eigenschaften; Zoomen, Verschieben, Autoskalieren (Strg+K); Bänder anzeigen/löschen | Screenshot |
| D4 | Band-Cursor-Eigenschaften: Anzeige X/Y der Cursor, Minimum/Maximum, Statistik (Mittelwert, RMS, Standardabweichung), **Peak-Anpassung** (f max, −3 dB, Q-Faktor, Zeta), angepasste Kurve | Screenshot |
| D5 | Peak-Anpassung hängt von den Hand-Bandgrenzen ab (ζ 1,319e-3 → 1,242e-3 bei engerem Band) | ergebnisse_7b.md |
| D6 | Statusleiste zeigt Messparameter („FFT · Mittelung Komplex 7 · 1 kHz · 1600 · 1.6 s · 625 mHz · 50 mm/s“) | Screenshot |
| D7 | Domäne RMS „Gesamte Bandbreite“ = alle Linien; Einzelklick auf Punkt zeigt Index (Label), Scanpunktnummer, Status (Scan, Geom., Fokus, Interp.), 3D-Koordinaten, Abstand D | Screenshots |
| D8 | Punktstatus-Kategorien: Nicht gemessen, Gültig, Optimal, Overrange, Ungültig, Gesperrt, Nicht erreichbar, Verdeckt, VT fehlgeschlagen | Screenshots |
| D9 | Menü „Neu“: Signalprozessor, Kombinierte Datei, Scandatei; Doppelklick ins Bild öffnet Anzeigeeigenschaften | Screenshots |
| D10 | Die Spektrumansicht zu finden kostete deutlich Zeit (mehrere Versuche) | Chatverlauf |
| D11 | Projekt-Browser zeigt Ordner und Dateien (auch .py, .csv, .json) direkt in PSV | Screenshots |
