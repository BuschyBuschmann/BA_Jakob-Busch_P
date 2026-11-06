# Protokoll 2026-11-09: Prüfdateien Fenster/Mittelung und Messung über die Warteschlange (zum Ausfüllen)

Gehört zu [versuchsplan.md](versuchsplan.md). Allgemeine Punkte des Tages (Kopf, Installation, Erkundung, D2, D3, D1, D4, E1) stehen im [Protokoll des Termins](../naechster-termin_messrechner/protokoll.md). Abschluss über `/laborbuch`.

## 1 Kopf

| Feld | Eintrag |
|---|---|
| Datum, Beginn, Ende | |
| Personen | |
| Software (Git-Hash aus Build-Info, Soll a0ee2fc…, `git_dirty` false) | |
| PSV-Version | |
| Raumtemperatur Beginn / Ende [°C] | |
| Änderungen am Aufbau seit 12.10. | |
| Freigabe Anregung (Name, Uhrzeit), höchste Amplitude [V] | |
| Pfad der 12.10.-Einstellungsdatei (Original, nicht verändert) | |
| Pfad und SHA-256 von `mess_3x3.set` | |
| Rückprobe `einstellungen_lesen.py` gegen Beispieldatei (Abweichungen) | |
| Raster: Labels / Koordinaten der 9 Punkte | |

## 2 Prüfdateien R, A, B

| Datei | Soll | Ist (Fenster, Mittelung, Anzahl) | Uhrzeit Start/Ende | Dauer [min] | Größe [MB] | SHA-256 | Foto-Nr. | Bemerkung |
|---|---|---|---|---|---|---|---|---|
| R `20261109_ref3x3_01.svd` | Rechteck, komplex, 7 | | | | | | | |
| A `20261109_hann3x3_01.svd` | Hanning, komplex, 7 | | | | | | | |
| B `20261109_betrag10_3x3_01.svd` | Rechteck, Betrag, 10 | | | | | | | |

- Fenster nach A zurück auf Rechteck (Foto): ☐ · Mittelung nach B zurück auf komplex 7 (Foto): ☐
- COM-Rücklesewerte `WindowFunction`, `WindowFunctionRMSCorrection` (A): ____ · `Type`, `Count` (B): ____
- Signal-Enhancement-Stufe: ____ · Generator-Signalform (C4): ____

## 3 Messung über die Warteschlange

Entscheidung vor Ort (Uhrzeit, Grund, ja/nein): ____

| Schritt | Soll | Ist | Uhrzeit | Bestanden (nur nach Bestätigung durch Jakob) |
|---|---|---|---|---|
| Trockenlauf mit `mess_3x3.set` | keine Bewegung, Werte wie .set; Generatorzustand notieren | | | |
| Rücklesen `mittelung.typ` im Trockenlauf | Magnitude | | | |
| T4 `T4_eine_messung.warteschlange.json` | Zustand FERTIG, Datei am Zielpfad | | | |
| T5 Abbruch | Abbruch ohne Hängen, Zustand korrekt | | | |
| T6-M1 | FERTIG, vergleichbar mit T4 | | | |
| T6 Pausenpunkt | hält an, läuft erst nach Bestätigung | | | |
| T6-M2 Betrag/10 | FERTIG, Datei mit Betrag 10 | | | |
| T6-M3 Zeitlimit 90 s | Zeitlimit löst aus, Fehlerzustand, Meldung | | | |

Pfad der .set in den Warteschlangendateien angepasst? (alt → neu): ____

## 4 Plausibilität (K1–K10, nach dem Termin aus den Rohdaten)

| Nr | Soll | T4 | T6-M1 | T6-M2 | Bemerkung |
|---|---|---|---|---|---|
| K1 | FERTIG, 9 Punkte, ≈ 3,5 MB | | | | |
| K2 | 2500 Hz, 4000, 1600, 1000 Hz, 0,625 Hz, komplex 7 (M2: Betrag 10) | | | | |
| K3 | alle 9 gültig/optimal | | | | |
| K4 | P-01–P-06 ok, P-07 ≥ 0,9, P-09 ≤ 0,05 | | | | |
| K5 | Median γ² ≥ 0,99 | | | | |
| K6 | Ref1 0,43 N ± 10 %, gegenüber R ± 3 % | | | | |
| K7 | Spitzen 160,625 / 247,5 Hz in ≥ 7 von 9 | | | | |
| K8 | Vib Z 0,3–10 mm/s, kein Übersteuern | | | | |
| K9 | gegen R: ± 1 Linie, ≥ 90 % der Linien | | | | |
| K10 | 100,8–504 s | | | | |

## 5 Beobachtungen, Abweichungen

| Uhrzeit | Beobachtung / Abweichung vom Plan | Folge |
|---|---|---|
| | | |

## 6 Ablage der Rohdaten

| Datei | Ort am Messrechner (außerhalb PyCharmProject) | Kopie für die Auswertung (Ort) | SHA-256 geprüft nach Kopie |
|---|---|---|---|
| | | | |
