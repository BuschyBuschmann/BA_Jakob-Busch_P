# Anleitung: kleine Test-Einstellungsdatei (.set) in PSV anlegen

Stand: 2026-10-27, Paket P6. Für Jakob, Mo 2026-11-02 (TODO: „kleine Test-Einstellungsdatei und Prüfling vorbereiten“).

**Grenzen dieser Anleitung.** Die Bedienung der PSV-Oberfläche ist im Repository nicht beschrieben.
Deshalb stehen hier **nur allgemeine Schritte**; wo die konkrete Bedienung unbekannt ist, steht
„in PSV die Funktion zum … verwenden; genaue Bezeichnung vor Ort“. Menüpfade, Schaltflächen und
Dialognamen sind bewusst nicht genannt. Wo etwas aus dem Handbuch bzw. der COM-Referenz belegt ist,
steht die Quelle; alles andere ist als Annahme oder Einschätzung markiert.

Quellen im Repository: COM-Referenz I5 (`in_progress/analysen/2026-10-23_I5_com-referenz.md`,
Abschnitte 2.4 `Settings`, 2.5 FFT und Mittelung), Fachprüfung I5-F
(`2026-10-23_I5F_fachpruefung-com-referenz.md`), Handbuch-Verweise [HB] darin, CHM-Textauszug
`in_progress/analysen/polytec-chm-text/` (z. B. `basic-engine-manual/PSV/`), Plan P2 Abschnitt 9.

## 1 Wozu die Datei gebraucht wird

| Prüfung | Verwendung der .set |
|---|---|
| T2 Trockenlauf | `lade_einstellungen(…)` lädt sie, danach werden `fft.bandbreite_hz` und `mittelung.anzahl` gesetzt, zurückgelesen und mit der PSV-Anzeige verglichen; Nachweis-`.set` wird gespeichert |
| T4 bis T6 | Messungen laden sie je Eintrag (`Messung.einstellungsdatei`); `ScanEx` scannt die darin definierten Messpunkte |
| T1 (indirekt) | nicht nötig; T1 liest nur den aktuellen Stand von PSV |

Was eine `.set` enthält (Handbuch [HB] 10-4, 10-10 laut I5 2.4): Erfassungsparameter, Scanpunkte,
2D-/3D-Abgleich, Optik (Zoom, Fokus) und Fensteranordnung, **keine Frequenzbänder**. Laden geht nur
bei gleicher Erfassungskarte und Anschlussbox (daher am Messrechner selbst anlegen). Scanpunkte und
Abgleich lassen sich laut I5 praktisch nur **interaktiv in PSV** vorbereiten und per `.set` laden.

## 2 Zielwerte für die Test-.set

| Nr | Einstellung | Zielwert | Zweck / Begründung | Bedienung in PSV |
|---|---|---|---|---|
| S1 | Messmodus | FFT | `stand.modus == "Fft"` (U3 1-3); die änderbaren Parameter `fft.*` gelten nur dort (I5 2.5: Zoom-FFT hat eine andere Frequenzachse) | in PSV die Funktion zum Einstellen des Messmodus verwenden; genaue Bezeichnung vor Ort |
| S2 | Messpunkte | wenige, z. B. 3 × 3 = 9 Punkte [Beispiel aus Plan 9; Zahl ist deine Wahl] | kurze Scandauer (der Simulator nimmt 9 × 1 s an, am Gerät unbekannt) | in PSV die Funktion zum Definieren der Scanpunkte (Gitter) verwenden; genaue Bezeichnung vor Ort |
| S3 | Messpunkte gültig | alle Punkte liegen auf dem Prüfling und sind erreichbar | sonst kann der Scan Punkte nicht anfahren [Einschätzung] | in PSV Punkte und ggf. den benötigten Abgleich prüfen; genaue Bezeichnung vor Ort |
| S4 | Abgleich (2D/3D) | falls PSV ihn für das Scannen verlangt: vor dem Speichern durchführen | steckt in der `.set` und wird mit `3DAlignment`/`2DAlignment` geladen (I5 2.4); per COM praktisch nicht herstellbar | in PSV die Funktion zum Abgleich verwenden; genaue Bezeichnung vor Ort |
| S5 | **Generator** | **aus** | Ein in der `.set` aktiver Generator wird von `ScanEx` automatisch gestartet ([HB] 8-3 laut Plan 6); der Prototyp setzt den Generator nie | in PSV die Funktion zum Ein-/Ausschalten des Generators verwenden; genaue Bezeichnung vor Ort |
| S6 | Bandbreite (FFT) | klein; **ungleich 5600 Hz**, z. B. 5000 Hz [I5-F-Prüfwert] | T2 setzt 5600 Hz und erwartet einen eingerasteten Ist-Wert (z. B. 6250 Hz, **nur Erwartung**, U3 2-2); hat die .set schon 5600 Hz, wäre ein Setzen nicht erkennbar | in PSV die Funktion zum Einstellen der FFT-Bandbreite verwenden; genaue Bezeichnung vor Ort |
| S7 | Linien (FFT) | wenige, z. B. 400 [I5-F-Prüfwert] | kurze Messzeit je Mittelung: $t_\mathrm{Mess} = n_\mathrm{FFT}/BW$ = 400 / 5000 Hz = 0,08 s (I5-F, Gl. 7.3); Auflösung $\Delta f = 12{,}5$ Hz | in PSV die Funktion zum Einstellen der Linienzahl verwenden; genaue Bezeichnung vor Ort |
| S8 | Mittelung Anzahl | **3** (Mindestwert im Katalog 3 bis 10000, I5 2.5) | T2 setzt 5 und erwartet eine sichtbare Änderung (U3 2-1, 2-3); kleinste Mittelung hält die Scandauer kurz | in PSV die Funktion zum Einstellen der Mittelung verwenden; genaue Bezeichnung vor Ort |
| S9 | Mittelung Art | beliebig; **festhalten, was gewählt wurde** | Komplexmittelung setzt Referenz/Trigger oder deterministische Anregung voraus (I5 2.5, [HB] 7-5/7-6); Phase ist ohne Referenz/Trigger ungültig (KONVENTIONEN) | in PSV die Funktion zur Wahl der Mittelungsart verwenden; genaue Bezeichnung vor Ort |
| S10 | Von/Bis | nicht einschränken (Vollbereich) | Der Prototyp setzt Von/Bis nicht; im Vollbereich gilt $k = 1 \dots n_\mathrm{FFT}$ (KONVENTIONEN) | Voreinstellung belassen; falls nötig, in PSV die entsprechende Funktion verwenden; genaue Bezeichnung vor Ort |
| S11 | Kanäle / Vibrometer | wie in PSV üblich für den Aufbau | werden von T1 nur gelesen (U3 1-4); nichts erfinden | unverändert lassen, wenn die Voreinstellung für den Aufbau passt |
| S12 | Trigger/Referenz | wie für den Prüfling vorgesehen; **notieren** | beeinflusst Mittelungsart und Phasengültigkeit | in PSV die entsprechende Funktion verwenden; genaue Bezeichnung vor Ort |

Weitere Werte (Zoom, Fokus, Fensteranordnung, Kamera) bleiben, wie sie sind. Die Lademaske des Adapters
lädt Acquisition, Alignment, APS, 2D- und 3D-Abgleich, aber **nicht** Camera und Windows
(Prüfanleitung U3). Anordnung und Optik der .set werden daher nicht übernommen.

## 3 Schritte (allgemein)

1. **PSV im Erfassungsmodus** (Datenerfassung), Laser- und Laborsicherheitsregeln des Instituts beachten.
   Starte in PSV **keine Messung**, solange du nicht ausdrücklich eine machen willst; die erste
   echte Messung ist T4 und eine bewusste Entscheidung.
2. Prüfling aufbauen (Lagerung, Position, Sichtbarkeit für den Scankopf). Shaker/Verstärker bleiben
   **getrennt**, solange der Betreuer die Anregung nicht freigegeben hat (Prüfanleitung U3).
3. Messmodus FFT wählen (S1), Bandbreite, Linien, Mittelung nach Tabelle einstellen (S6 bis S9).
   In PSV die jeweilige Funktion verwenden; genaue Bezeichnung vor Ort.
4. Generator **ausschalten** (S5) und im PSV-Bild kontrollieren, dass er aus ist.
5. Scanpunkte (S2) definieren, Abgleich ggf. herstellen (S4), Punkte prüfen (S3).
6. **Alles notieren**, was tatsächlich eingestellt wurde (Protokoll `protokoll_vor_ort.md`, Tabelle „Test-.set“):
   Anzahl Punkte, Bandbreite, Linien, Mittelung (Anzahl, Art), Generator, Trigger/Referenz.
7. Einstellungen als **.set speichern**: in PSV die Funktion zum Speichern der Einstellungen verwenden;
   genaue Bezeichnung vor Ort. Ziel: `C:\ldv\vorlagen\test_3x3.set` (lokal, kein Netzlaufwerk, nicht in einem
   Polytec-Ordner). Die Standardeinstellungsdateien der Software liegen unter
   `C:\Users\<Konto>\AppData\Local\Polytec\PSV\<Version>\` ([HB] 2-4 laut I5 2.4): **diese nicht überschreiben**.
8. **Kopie** der Datei anlegen (z. B. `test_3x3_kopie.set`), damit ein misslungenes Laden im Test das
   Original nicht gefährdet. Der Adapter schreibt nie auf die Quell-`.set` (Plan 6), die Kopie ist eine
   zusätzliche Vorsicht.
9. **Rückprobe** [Einschätzung]: Einstellungen in PSV ändern (z. B. Mittelung anders), dann die gespeicherte
   `.set` in PSV laden (in PSV die Funktion zum Laden von Einstellungen verwenden; genaue Bezeichnung vor Ort)
   und prüfen, dass Messmodus, Bandbreite, Linien, Mittelung, Generator-aus und Punktzahl wie notiert
   wiederkommen. Abweichungen im Protokoll vermerken.

## 4 Vor den Prüfungen kontrollieren

- [ ] Generator in der `.set` aus (S5); in T4 zusätzlich die Generatorzeile im Startdialog lesen.
- [ ] Bandbreite ≠ 5600 Hz und Mittelung ≠ 5 (damit T2 eine Wirkung zeigt).
- [ ] Punktzahl notiert (Vergleich mit „Messpunkte“ im Gerät-Dialog der Oberfläche, U5-Ergänzung).
- [ ] Datei liegt lokal, Name ohne Leerzeichen/Sonderzeichen [Annahme, Pfadprüfung des Adapters nicht eigens geprüft].
- [ ] Keine zweite Datei gleichen Namens im Messdaten-Ordner, wo die Nachweis-`.set` und `.svd` entstehen
  (Überschreiben wird abgelehnt, U3 2-4).

## 5 Annahmen und offene Punkte

- Zielwerte S2, S6, S7 sind Beispiele aus Plan 9 und I5-F, keine Vorgaben der Aufgabenstellung. Ändere sie,
  wenn der Aufbau etwas anderes verlangt, und trage die tatsächlichen Werte ein.
- Die Scandauer je Punkt hängt außer von $n_\mathrm{FFT}/BW \cdot$ Mittelungen auch von Laserpositionierung und
  Fokus ab ([HB] 8-2 laut I5); eine Zahl dafür steht im Repository nicht. Sie wird in T4 gemessen (Plan 9) und
  bestimmt das Zeitlimit (Startwert 600 s ist unbelegt).
- Ob PSV für das Scannen einen gültigen 3D-Abgleich verlangt und wie er hergestellt wird, ist hier
  nicht belegt (S4).
- Der Einfluss von Überlappung (laut I5 nur ohne Trigger wirksam) und Trigger auf die Messdauer ist hier
  nicht bewertet; die Formel in S7 ist nur die Messzeit einer Mittelung.
