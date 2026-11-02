# Ergebnisse 7b – Auswertungs-Prüfungen am Messrechner (Mo 2026-11-02)

> Nachgeprüft durch Fachanalyse P0b und E-PSV-F (2026-11-02); Korrekturen in M1, M4, M5, M7, M8, M11, M12 eingearbeitet.

Rechner BEOWOLF, PSV 10.4.0.1 (Auswertung). Datei: Kopien von `20261012_ref_Mitte.svd`
(`pruefung_7b\…_KOPIE.svd` in PSV, `…_KOPIE_KOPIE2.svd` für File-Access-Skripte; Größe gleich
dem Original im Repo, 27 115 520 Byte). Nichts gespeichert. Bezugspunkt Label 132 (= Scanpunkt 1).

Werkzeuge: `erkundung.py --stufe 1 --datei` (1b), `einstellungen_lesen.py`, `daten_lesen.py`
(Golden File `golden_punkt1_label132.csv`), PSV-Analysator (Band-Cursor).
Rechnung zum Vergleich: eigener Leser (`svd_lesen.py`) gegen Golden File, Orchestrator 2026-11-02.

| Nr. | Annahme | Befund | Quelle | Stand |
|---|---|---|---|---|
| M1 | `konjugieren = False` | H1 Vib X/Z & Ref1 aus PSV = CP/AP_Ref1 aus eigenem Leser, rel. ≤ 5,8·10⁻⁸, Phase ≤ 4,7·10⁻⁸ rad (float32-Rundung; P0b); konjugiert passt nicht | Golden File | bestätigt |
| M2 | k₀ = 1, Δf = 1,5625 Hz, bis 2500 Hz | **k₀ = 1 bestätigt; Δf = 0,625 Hz, 0,625 … 1000 Hz** (XAxis Min 0,625, Max 1000, Count 1600; GetMidX(0/1/1599) = 0,625/1,25/1000). PSV-Statusleiste „1 kHz · 1600 · 1.6 s · 625 mHz“. FFT-Einstellung: Bandwidth 1000, SampleFrequency 2500 (= bisher als Bandbreite gedeutet), Samples 4000, SampleTime 1,6 s | 1b, einstellungen_lesen, PSV | **Achse falsch → Korrektur** |
| M4 | 0-to-peak | Vib X/Y/Z Geschwindigkeit aus PSV = CPH des Lesers bitgleich; Band-RMS 50,48 mm/s/N = √(Σ\|H\|²/2); Gesamtwert 1,349 mm/s = 3D-Gesamtwert √(Σ_X+Σ_Y+Σ_Z) (Vib Z allein 1,3325) | Golden File, PSV | bestätigt (PSV-interne Spitzenwertdeutung; absolute Kalibrierung nicht geprüft) |
| M5 | Rechteck (W_RBW = 1), n_d = 7 | WindowFunction 0 = `ptcWindowFctRectangle` (Doku-Enum PTCWindowFunction); Mittelung komplex (Type 2), Count 7; SE am Vibrometer an; Trigger aus; Generator aktiv 0,02 V (Burst-Parameter nicht lesbar). Feld +0x3C je Punkt (7…25) = Zahl erfasster Blöcke (Zeitstempel-Regression T = 1,600 s, P0b); ob bei SE nur 7 gemittelt werden, offen | einstellungen_lesen, Doku | Fenster und Count bestätigt; n_d je Punkt offen |
| M6 | alle Punkte gültig | Statusfeld 1 (18 Punkte) = „Gültig“, 3 (117) = „Optimal“; PSV 13,3 % / 86,7 % | PSV, Leser | bestätigt |
| M7 | Gültigkeit > 1 kHz offen | Messung reicht nur bis 1000 Hz; Kennzeichen `gueltigkeit_offen_m7` gegenstandslos. Ob der Amplitudengang („Bandbreitenbereich 1 kHz“) bis 1000 Hz flach ist, nicht belegt (Datenblatt) | wie M2 | Frage > 1 kHz erledigt; Amplitudengang offen |
| M8 | s = +1 für Ref1, Ref2 | Impedanzkopf PCB 288D01 (SN 3853) richtig montiert; Force → Ref1 (N, 40,31 N/V, IEPE), Beschl. → Ref2 (m/s², 97,85 (m/s²)/V, IEPE); Kalibrierfaktoren positiv; DirectionOfVibration 0 = `ptcZPos` bei beiden. **P-08 ist achsunabhängig** (Re{H/(iω)} = Im{H}/ω) und nicht durch SignalDelay erklärbar (P0b): relative Polarität Ref1/Ref2 invertiert. Starrkörperbereich < 20 Hz: Vib Z/Ref1 −90° (konsistent), Vib Z/Ref2 +90° → Deutung Ref2 gedreht (E-PSV-F, [V]) | Fotos, einstellungen_lesen, P0b, E-PSV-F | **offen**: welcher Kanal, entscheidet Datenblatt PCB 288D01 / Kontrollversuch |
| M10 | Band geschlossen | Band-Cursor 158,8–163,8 Hz RMS 50,48 mm/s/N = beide Grenzlinien eingeschlossen (50,478); andere Varianten 49,69–50,43 | PSV, Golden File | bestätigt |
| M11 | PSV-Toleranzen | PSV-Band-Cursor „Peak-Anpassung“ (Label 132, H1 Vib 3D & Ref1, Z), siehe Tabelle unten. Beide Spitzen `aufloesungsbegrenzt` (B < Δf) → Toleranzzeilen für Spitzen ohne Kennzeichen (FG-02 Abschnitt 8) **nicht geprüft** | PSV, P0b | teilweise |
| M12 | 3D-Komponenten im Geometrie-KS | Vib X/Y/Z aus PSV = Komponenten des Lesers bitgleich; Koordinaten Label 132 identisch (0,19089 / 0,42602 / −0,23125 m). Dass die Komponenten im Geometrie-KS liegen, belegt das nicht (Indiz η ≈ 0,995) | Golden File, PSV | Leser = PSV bestätigt; Geometrie-KS weiter Indiz |
| M13 | Normalen +z | Z-Achse in PSV zeigt aus dem Bild zu den Scanköpfen; D = 2,82 m | PSV | plausibel, nicht formal geprüft |
| M14, M15 | Elementindizes, Messzeit | – | – | offen |

## M11 – PSV-Peak-Anpassung (Band-Cursor), Label 132, Z

| Spitze | Band (Hz) | Max (Hz; mm/s/N) | f max (Hz) | −3 dB (Hz) | Q | ζ |
|---|---|---|---|---|---|---|
| 1 | 158,8 – 163,8 | 160,6; 59,09 | 160,7 | 0,4 | 379,19 | 1,319·10⁻³ |
| 1 | 159,4 – 162,5 | 160,6; 59,09 | 160,7 | 0,4 | 402,56 | 1,242·10⁻³ |
| 2 | 245,6 – 250,6 | 247,5; 6,40 | 247,7 | 0,7 | 378,52 | 1,321·10⁻³ |

B-1 an Label 132 mit gleichen Bandgrenzen (P0b, korrigierte Achse): Spitze 1 160,563 Hz / ζ 1,435·10⁻³ (+8,8 % gg. PSV), Spitze 2 247,669 Hz / ζ 1,387·10⁻³ (+5,0 %); das engere PSV-Band (6 Linien) ist nach FG-03 nicht fitbar (`zu_wenig_linien`).

Vergleich (nur zur Einordnung, nicht gleichwertig): eigener B-1-Fit, Median über 20 Punkte,
Achse korrigiert (×0,4): 160,53 Hz / ζ 1,42·10⁻³ und 247,61 Hz / ζ 1,46·10⁻³.
PSV-ζ hängt von den Bandgrenzen ab (−6 % bei engerem Band). Für den Vergleich nach FG-02
Abschnitt 8 ist B-1 an Label 132 mit denselben Bandgrenzen zu rechnen.

## Weitere Befunde
- Geom.-Status „Video-trianguliert“ = Statusfeld 8193, Fokus „Automatisch zugewiesen“ = 129.
- Polytec File Access 6.6 registriert und lizenziert (PSV-S-VBEng); ReadOnly-Lesen funktioniert.
- `Ref1 | Kraft` hat in der Datei keine Real/Imag-Darstellung; „Ref2 & Ref1“ unter diesem Namen
  nicht lesbar.
