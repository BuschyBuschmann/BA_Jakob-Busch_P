# Nach dem Messrechner-Termin 02.11.: Prüfergebnisse und nützliche PSV-Punkte (zur Entscheidung)

Zusammengeführt vom Orchestrator aus vier Paketen (alle read-only):
P0a Review Lese-Skripte (reviewer, sonnet) · P0b Fachprüfung Befunde 7b (strukturdynamik-experte, opus) ·
E-PSV-S Nutzen für Software (software-engineer, sonnet) · E-PSV-F fachlicher Nutzen (strukturdynamik-experte, sonnet).
Grundlage: `2026-11-02_PSV-beobachtungen_faktenliste.md`, `ergebnisse_7b.md` (inzwischen nach P0b korrigiert).

## 1 Prüfergebnisse zu den Vor-Ort-Ergebnissen

| Thema | Ergebnis | Quelle |
|---|---|---|
| Frequenzachse | **Mehrfach unabhängig bestätigt**: Δf = 0,625 Hz, 0,625…1000 Hz, k = 1…1600; 2500 Hz = Abtastrate. Zusätzlich: PSV integriert mit ω = 2π·0,625·k (Abweichung 1e-7, bei 1,5625 −60 %); Zeitstempel ergeben Blockdauer 1,600 ± 0,017 s. Fehlerursache: Zirkelschluss über das Feld „Blockdauer 0,64 s“ in W2. Die Formel Δf = BW/n_FFT in KONVENTIONEN war richtig | P0b |
| Was sich ändert | Frequenzen, Drift (Hz/h), Modalkonstante, Beträge aus Akzeleranz/B-10, alle Bänder in Hz. **Unverändert**: ζ, Q, MAC, γ², ρ, Kennzeichen relativ zu Δf. M7-Kennzeichen fällt weg (42 → 0 Spitzen) | P0b |
| Leser | Blockdauerprüfung bricht nach Korrektur ab → muss entfallen | P0b |
| **Vorzeichen (M8)** | **Meine Vermutung „Folge der falschen Achse“ ist widerlegt.** P-08 ist achsunabhängig und nicht durch Laufzeiten erklärbar: relative Polarität Ref1/Ref2 invertiert. E-PSV-F deutet aus dem Starrkörperbereich < 20 Hz, dass **Ref2** gedreht ist; P0b hält die Zuordnung ohne Datenblatt für nicht entscheidbar. Einbau und PSV-Einstellungen sind in Ordnung | P0b, E-PSV-F |
| M11 (PSV-Fit) | B-1 an Label 132 mit gleichen Bandgrenzen: ζ +5…+9 % über PSV, f_r −0,03…−0,14 Hz. Beide Spitzen sind `aufloesungsbegrenzt` → die Toleranzen für Spitzen ohne Kennzeichen (FG-02 §8) sind **nicht geprüft**. PSV zeigt nur 0,1 Hz Auflösung | P0b |
| Weitere Korrekturen an 7b | 1,349 mm/s ist der 3D-Gesamtwert; M5 Rechteck jetzt per Doku-Enum belegt; M12 nur „Leser = PSV“; DirectionOfVibration 0 = +z | P0b (eingearbeitet) |
| Lese-Skripte | FREIGABE MIT AUFLAGEN: nur lesend ✔; MAJOR: Spaltenlängen ungeprüft, fehlende Signale ohne Exit-Code/Vermerk (Golden File hat 6 von 8 Signalen), ruff 21 Fehler; 4 MINOR; 8 Testvorschläge; einfacher Weg ohne Whitelist-Proxy vertretbar (Hinweis + statischer Test) | P0a |

## 2 Nützliche Punkte aus den PSV-Einblicken (Auswahl, entdoppelt)

### 2a Für den nächsten Termin (Prüfzettel)
1. COM-Registrierung (mit Daniel), dann Stufe 0/1; **nur eine PSV-Instanz** (PID notieren); einmal bewusst Desktop-Modus starten und Fehlerbild notieren.
2. **Mini-Scan 3×3 mit Zeitdaten** (TDD lizenziert, bisher nicht gespeichert): eigene FFT/H1, Leckage, Streuung je Block, Dateigröße, Wirkung auf SE.
3. **Messpunkt auf dem Impedanzkopf**: Vorzeichen (M8), SignalDelay-Kompensation und Kalibrierung in einem Versuch.
4. **Zwei-Amplituden-Test** (0,02 / 0,04 V) an Label 132: Linearität, Kohärenz < 60 Hz.
5. **Platte und Impedanzkopf wiegen** (Massenlinie als Kalibrierprobe).
6. **Handbücher 10.4 kopieren** (Theory Manual, Software Manual, Handbuch) nach `Input/literatur/polytec/`.
7. M11 an drei Spitzen **ohne** Kennzeichen wiederholen; PSV-Werte möglichst mit voller Stellenzahl.
8. Golden File v2 (H2, Kohärenz, PSD/ESD, H1 Ref2/Ref1, Terzen); Generator-Wellenform per Cast; `PolyMath.PeakFit` per COM probieren (PSV-Fit mit bekannten Testdaten prüfen); UFF-Export als Gegenprobe, ATFX/ME'scope wählbar?; Verhalten von File Access bei in PSV geöffneter Datei.

### 2b Anforderungsvorschläge (über `/anforderungs-analyst`)
- Messprotokoll enthält Δf, f_max, SampleTime ausdrücklich; nach dem Scan Abgleich der Frequenzachse der Datei mit der Einstellung (hätte den Achsenfehler gefunden) – zu R-020.
- Warnung bei mehr als einem PSV-Prozess, PIDs im Protokoll.
- Auswertungsoberfläche: Spektrum direkt sichtbar, Parameterzeile aus den Dateieinstellungen (Konzeptpaket, Ablauf C).
- Dämpfungsausgabe mit Bandgrenzen und Methode.
- Zeitdaten lesen und Spektren/H1 unabhängig von PSV rechnen (Kann).
- Masse aus Massenlinie als Plausibilitätsprüfung (Kann).
- Lastenheft O2/O5/O6 mit den Befunden vom Termin beantworten (Python, Internet vorhanden).

### 2c Entscheidungen/ADR
- **ADR-006 abschließen:** Datenweg des Hauptpakets – eigener Leser (jetzt gegen PSV bestätigt), File Access oder beides (File Access als Gegenprobe).
- Generator-Wellenform: gezielter Cast vs. Early Binding.

### 2d Kleine Code-Aufgaben
Verständliche Meldung bei fehlender COM-Registrierung bzw. Desktop-Modus; SignalDelay in Whitelist/Einstellungsstand/Protokoll; Statuscode-Tabelle (Bitmaske nach Polytec-Enum); Datei-Metadaten (FileTime, ProgramVersion) im Export; Namensauflösung aus der Dateistruktur statt fest verdrahtet; Hinweis „Datei in PSV geöffnet?“.

### 2e Recherche
Datenblatt PCB 288D01 (Polarität – entscheidet M8, zuerst); PSV-Handbuch 10.x zum Modell der Peak-Anpassung; Datenblatt Decoder (Amplitudengang „1 kHz“); Signal Enhancement (welche Blöcke gemittelt).

### 2f Konventionen und Thesis
- KONVENTIONEN: Frequenzachse „bestätigt“ statt „vorläufig“, Hinweis „Abtastfrequenz ≠ Bandbreite, Achse immer gegen XAxis/Golden File prüfen“; Polarität der Referenzen je neuem Aufbau physikalisch prüfen (P-08).
- Thesis-Bausteine (kapitel-map): Bewertung der Schnittstelle (Registrierung, Desktop-Modus, Late Binding), Validierung des Datenwegs (Golden File), Achsenfehler als dokumentierter Fehlschlag, Grenzen von PSV (handabhängiger Fit an der Auflösungsgrenze, keine PCA).

## 3 Offene Rückfragen aus den Paketen
- Bänder in Hz (B-8, Beispielskript): bei gleichen Linien umbenennen (60–200/200–400/400–1000 Hz) oder neue Hz-Bänder festlegen? Annahme: umbenennen.
- Kennzeichen `gueltigkeit_offen_m7`: entfernen? Annahme: ja.
- PSV-Vergleich bei Spitzen mit B < 3 Δf: nur berichten (Empfehlung) oder eigene Toleranz?
- Darf beim Mini-Scan `SaveTimeDataForScan` an sein (setzt SE auf „Fast“)? Annahme: ja, nur Testscan.
- Lizenzlage ATFX/ME'scope beim Betreuer klären?
