# Versuchsplan 2026-11-09: Prüfdateien Fenster/Mittelung und erste Messung über die Warteschlange

**Stand:** 2026-11-06, Entwurf · **Fachgrundlage:** [FG-V1](../../fachgrundlagen/FG-V1_pruefdateien-fenster-mittelung.md) (Fachanalyse FA-V1, strukturdynamik-experte, vom Nutzer am 2026-11-05 freigegeben) · **Ablauf des Tages:** [Ablaufplan nächster Termin](../naechster-termin_messrechner/ablaufplan.md) (D2, D3, D1, D4, E1 sind dort beschrieben und hier nur eingeordnet)
**Kennzeichen:** [N] nachgerechnet · [D] aus der Beispieldatei `20261012_ref_Mitte.svd` · [A] Annahme · [H] am Gerät zu prüfen · [offen] zu klären

## 1 Ziel und Bezug

| Nr. | Fragestellung | Bezug |
|---|---|---|
| Z1 | Lassen sich Fensterfunktion und Mittelungsart/-anzahl aus der .svd-Datei sicher lesen? (Leser: Fenster bisher nicht lesbar, Mittelung „plausibel“) | R-022, R-023, R-032; ADR-020 |
| Z2 | Läuft eine echte Messung über die Warteschlange des Prototyps (T4), mit Abbruch (T5) und drei Messungen inkl. Pausenpunkt und Fehlerpfad (T6)? | R-001, R-010–R-020, R-030, R-031 |
| Z3 | Liefern die automatisch erzeugten Messungen plausible Daten (Kriterien K1–K10)? | R-024, R-054 |

Ob T4 bis T6 stattfinden, entscheidet der Nutzer vor Ort (Nutzerentscheidung 2026-11-05). Die Hardwaretests gelten erst nach seiner Bestätigung.

## 2 Prüfling, Lagerung, Anregung

| Punkt | Angabe | Quelle |
|---|---|---|
| Prüfling | Blech wie bei der Beispielmessung vom 12.10.; Material und Dicke [offen] (E1: messen) | Laborbuch 2026-11-02 |
| Lagerung | frei hängend wie bei der Beispielmessung; Änderungen am Aufbau seit 12.10. notieren | Laborbuch 2026-11-02 |
| Anregung | Mini SmartShaker über Impedanzkopf PCB 288D01; Freigabe durch Daniel (Nutzer, 2026-11-05) | Nutzer |
| Generator | wie Beispielmessung: an, 0,02 V, Signalform aus dem Generator-Dialog (C4, vorher ablesen) | Faktenliste C3; FG-V1 |
| Höhere Amplitude (0,04 V, D3) | nur nach Zustimmung Daniel [offen] | FA-V1 |
| Sicherheit | Laserschutz und Shakerbetrieb nach Vorgaben des Instituts (Daniel); dieser Plan ersetzt sie nicht | – |

## 3 Messgitter

- **3×3-Raster (9 Punkte)**, identisch für alle Dateien R, A, B und die Warteschlangen-Messungen.
- Wenn PSV es zulässt: Teilraster der Beispielmessung, Labels 132/133/134, 161/162/163, 190/191/192; Label 132 bei (0,19089 / 0,42602 / −0,23125) m; Abstände ≈ 69,2 mm (Label +1) und 48 bis 50 mm (Label +29) [D]. Labels gelten je Scan; tatsächliche Koordinaten ins Protokoll.
- Koordinatensystem und Alignment wie Beispielmessung (in PSV; Software ändert nichts daran).

## 4 Messparameter

Die Einstellungsdatei der Beispielmessung vom 12.10. liegt am Messrechner (Nutzer, 2026-11-05). Sie wird als **Kopie** geladen, auf das 3×3-Raster reduziert und als `mess_3x3.set` gespeichert (Ordner `$ARB\vorlagen\` [A]); das Original bleibt unverändert. Danach Rückprobe mit `einstellungen_lesen.py` gegen die Beispieldatei.

| Parameter | R | A | B | Einheit | Quelle |
|---|---|---|---|---|---|
| Messmodus | FFT | = | = | – | Faktenliste C1 |
| Bandbreite / Linien | 1000 / 1600 | = | = | Hz / – | C1 |
| f_s / Abtastwerte / Δf / Blockdauer | 2500 / 4000 / 0,625 / 1,6 | = | = | Hz / – / Hz / s | C1 |
| Überlappung | 0 | = | = | % | C1 (nicht verstellen) |
| **Fenster** | Rechteck | **Hanning** (alle aktiven Kanäle gleich) | Rechteck | – | FG-V1 2 |
| **Mittelung** | komplex, 7 | komplex, 7 | **Betrag, 10** | – | FG-V1 3 |
| Signal Enhancement | wie Beispiel (Stufe ablesen) | = | = | – | C2 |
| Trigger / Phase von Referenz | aus / ein | = | = | – | C2 |
| Zeitdaten speichern | aus | = | = | – | C2 |
| Kanäle | Vib 3D 0,05 (m/s)/V, Messbereich 50 mm/s; Ref1 40,306 N/V; Ref2 97,847 (m/s²)/V | = | = | – | C4, W2 |

**Erwartete Scandauer** [N, A: 17,8 s je Punkt aus der Beispieldatei]: R und A ≈ 2,7 min (höchstens ≈ 8,4 min), B ≈ 3,8 min (höchstens ≈ 12 min); je Datei ≈ 10 min mit Umstellen, Foto und Speichern.

## 5 Ablauf

### 5.1 Prüfdateien R, A, B (direkt in PSV)
1. `mess_3x3.set` laden, Dialoge fotografieren, Messung **R** → `20261109_ref3x3_01.svd`.
2. Nur Fenster auf Hanning (alle aktiven Kanäle), Foto, Messung **A** → `20261109_hann3x3_01.svd`. Fenster zurück auf Rechteck, Foto.
3. Nur Mittelung auf Betrag, Anzahl 10, Foto, Messung **B** → `20261109_betrag10_3x3_01.svd`. Mittelung zurück auf komplex 7, Foto.
4. Nach jeder Datei: Kopie anlegen, `einstellungen_lesen.py` auf der Kopie, SHA-256 der Rohdatei ins Protokoll.
R → A → B kurz hintereinander, Aufbau und Verstärker unverändert. Rohdaten nie überschreiben, Ablage außerhalb von PyCharmProject.

### 5.2 Erste Messung über die Warteschlange (Entscheidung vor Ort)
1. Voraussetzung: T1 und T2 ohne Befund (Ablaufplan B4), Freigabe der Anregung dokumentiert.
2. Trockenlauf mit genau `mess_3x3.set`, ohne PSV-Neustart bis T4; Generatorzustand beobachten [H]. Den Setter `mittelung.typ` im Trockenlauf mit Rücklesen prüfen (vor T6-M2).
3. **T4:** Warteschlange `konfig/T4_eine_messung.warteschlange.json` laden, Pfad der .set prüfen bzw. anpassen, eine Messung ohne Parameteränderung (vergleichbar mit R), Zeitlimit 600 s.
4. **T5:** Abbruch einer laufenden Messung (Ablaufplan D5).
5. **T6:** `konfig/T6_drei_messungen.warteschlange.json`: M1 unverändert (600 s) → Pausenpunkt → M2 Betrag/10 (900 s, erzeugt B per Programm) → M3 Zeitlimit 90 s (unter dem Minimum von 100,8 s [N]; das Zeitlimit muss auslösen).
Nach jedem Abbruchkriterium keine weiteren Messtests.

### 5.3 Einordnung in den Tag (Vorschlag FA-V1, Details im Ablaufplan)

| Block | Inhalt | Dauer [A] |
|---|---|---|
| 1 | A0, A1, B1, B2, B3 (Test-.set Generator aus), T1, T2; nebenher C1, C4, C3, C2 | 100–130 min |
| 2 | Freigabe dokumentieren, `mess_3x3.set` aus der Kopie der 12.10.-Einstellungen, R, A, B | 20 + 3 × 10 min |
| 3 | D2 (Impedanzkopf), D3 (am Kopfpunkt), Amplitude zurück auf 0,02 V | ≈ 70 min |
| 4 | Trockenlauf, T4 → T5 → T6 | ≈ 95 min |
| 5 | D1 (nur Zeitdaten-Scan; R dient als Referenzscan; SE zurückstellen) | 15–20 min |
| 6 | D4 (Langscan) oder Teilraster-Vergleich; nebenher C-Punkte, E2 | 40–85 min |
| 7 | E1 (erst nach allen Messungen), X1 (nach T6), A2 | 60 min |

Bei Zeitmangel entfällt zuerst D4, dann D1, dann T6. D2 nur vor R/A/B, wenn die Sichtbarkeitsprüfung (höchstens 10 min) schnell gelingt.

## 6 Erwartete Ergebnisse und Plausibilitätskriterien

### 6.1 Prüfdateien (FG-V1 2, 3)
- **Fenster gesichert**, wenn im Einstellungsstream `Info/DAQ_Settings_Fft/Channels` in mindestens drei Kanalrecords am gleichen Offset 0 → 7 steht und der COM-Rücklesewert `WindowFunction` = 7 ist.
- **Mittelung gesichert**, wenn `Average` von `[1,2,0,7]` auf `[1,1,0,10]` wechselt und COM `Type` = 1, `Count` = 10 liefert.
- Gegenprobe Fenster: Ref1-Gesamtleistung A/R = 4·⟨w²⟩ (gleichmäßige Energie 1,5) [N]; Rauschboden +1,76 dB.
- Gegenprobe Mittelung: H1, H2 und Kohärenz zeigen den Typ **nicht** (Theory Manual 6.4); nur ρ = |CPH_B|/(|CP|/√AP_Ref) an Linien mit γ² < 0,9 (z. B. 1,022 bei γ² = 0,9, n = 10: 1,024) [N].
- Alle drei Dateien laden ohne Formatfehler; Prüfungen P-01 bis P-06 ok.

### 6.2 Messung über die Warteschlange (K1–K10, FG-V1 5; Schwellen teils [A])

| Nr | Kriterium | Soll |
|---|---|---|
| K1 | Zustand FERTIG, Datei lesbar, 9 Punkte | ≈ 3,5 MB (2,8–4,2 MB) [A] |
| K2 | FFT und Mittelung aus der Datei = Einstellungsdatei | 2500 Hz, 4000, 1600, 1000 Hz, 0,625 Hz, komplex 7 |
| K3 | Punktstatus | alle 9 gültig oder optimal |
| K4 | Leser-Prüfungen | P-01–P-06 ok, P-07 q ≥ 0,9, P-09 ≤ 0,05 |
| K5 | Anregung wirksam | Median γ²(Vib Z/Ref1) 60–1000 Hz je Punkt ≥ 0,99; 0,9–0,99 Hinweis; < 0,9 Befund |
| K6 | Kraft | Ref1-Effektivwert 0,43 N ± 10 %, gegenüber R ± 3 % [A] |
| K7 | Spitzen | lokales Maximum von \|H1\| bei 160,625 ± 0,625 Hz und 247,5 ± 0,625 Hz in mindestens 7 von 9 Punkten [A] |
| K8 | Pegel | Vib-Z-Effektivwert 0,3–10 mm/s, kein Übersteuern [A] |
| K9 | Gegenprobe T4 gegen R | Spitzen ± 1 Linie; Linien mit γ² ≥ 0,99: \|ΔH\|/\|H\| ≤ 3·√(ε_R²+ε_T²) in ≥ 90 % der Linien [A] |
| K10 | Dauer 3×3 | 100,8 s (Minimum) bis 504 s, typisch 160 s [N] |

Eine Abweichung bei K7 ist ein Befund (Lagerung, Temperatur), kein Messfehler.

## 7 Messkonfiguration

Warteschlangendateien im Format des Pakets (`ldv_automation.persistenz.warteschlangendatei`, Schema-Version 1), erzeugt mit `speichere_warteschlange` und geprüft mit `lade_warteschlange` (beide Dateien laden ohne Fehler, 1 bzw. 4 Einträge):
- `konfig/T4_eine_messung.warteschlange.json`
- `konfig/T6_drei_messungen.warteschlange.json`

Der Pfad der Einstellungsdatei `D:\Messdaten\DAL\BA Jakob Busch\vorlagen\mess_3x3.set` ist eine Annahme und wird nach dem Laden in der Oberfläche geprüft bzw. angepasst (R-014). Die Dateien R, A, B entstehen direkt in PSV und brauchen keine Konfigurationsdatei.

## 8 Risiken

| Risiko | Gegenmaßnahme |
|---|---|
| Fensterwechsel ändert weitere Felder (z. B. RMS-Korrektur) | jedes geänderte Feld über den COM-Rücklesewert erklären |
| PSV speichert bei Betragsmittelung das Antwortspektrum nicht betragsgemittelt | Befund dokumentieren (ρ ≈ 1 überall) |
| Setter `mittelung.typ` am Gerät ungeprüft | im Trockenlauf rücklesen; B von Hand ist der Hauptweg |
| Trockenlauf startet den Generator [H] | Generatorzustand beobachten, Foto |
| Teilraster der Beispielmessung nicht reproduzierbar | eigenes 3×3, Koordinaten notieren |
| Handbücher beschreiben PSV 9.1/10.1, nicht 10.4 | E2 (Handbücher 10.4 kopieren) |

## 9 Offene Fragen

| Nr. | Frage | Auswirkung |
|---|---|---|
| F2a | Bis zu welcher Generator-Amplitude ist die Anregung freigegeben (0,04 V für D3)? | D3 |
| F4 | Darf „Zeitdaten speichern“ an sein, wo dürfen die Dateien liegen? | D1 |
| F6 | Laser auf den Impedanzkopf, Reflexfolie erlaubt? | D2 |
| V1 | Ordner der Einstellungsdatei `mess_3x3.set` am Messrechner | Pfad in den Warteschlangendateien |
| V2 | Material und Dicke des Blechs | Versuchsdokumentation, E1 |
