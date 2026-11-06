# Protokoll: nächster Termin am Messrechner (zum Ausfüllen)

Zum Ausfüllen am Messrechner (Ausdruck oder Datei). Ablauf und Ersatzpläne: [ablaufplan.md](ablaufplan.md); Kurzliste: [pruefzettel.md](pruefzettel.md).
Struktur vom [alten Protokoll](../2026-11-02_prototyp/protokoll_vor_ort.md) übernommen und um Entscheidungsprotokoll, Ersatzpläne und die Prüfzettelpunkte erweitert.
Ein Befund gilt erst als „am Gerät bestätigt“, wenn du ihn bestätigt hast. Vorgabewerte sind **Annahmen**, keine Messwerte. Nichts nachträglich schönen; Fehlschläge eintragen.
Uhrzeiten immer mit eintragen. Nicht Zutreffendes mit „entfällt“ und Grund (z. B. „EP-4“) kennzeichnen.

## 1 Kopf

| Feld | Eintrag |
|---|---|
| Datum (JJJJ-MM-TT) / Uhrzeit Beginn / geplantes Ende | |
| Bearbeiter | Jakob (mit Orchestrator) |
| Daniel anwesend / erreichbar (Telefon)? | |
| **Antwort F1:** COM-Registrierung erfolgt (wer, wann, Befehl)? 10.2/10.3 noch in Gebrauch? | |
| **Antwort F2: Freigabe der Anregung** (ja/nein, durch wen, Uhrzeit, Bedingungen: Amplitude, Dauer, Aufsicht) | |
| Antwort F3: Mo 2026-11-09, ganzer Tag (Nutzer, 2026-11-05); tatsächlich: ____ min, Ende | |
| Zeitverlust am Tag? (Streichreihenfolge Ablaufplan 4, Fall 4.2) | ☐ ja ☐ nein |
| Antwort F4: `SaveTimeDataForScan` beim Mini-Scan erlaubt? Ablage der Zeitdaten | |
| Antwort F5: Waage vorhanden (Typ, Auflösung)? Abbau des Aufbaus für Wiegen erlaubt? | |
| Antwort F6: Laser auf Impedanzkopf erlaubt? **Reflexfolie auf der Stirnfläche erlaubt (Zustimmung Daniel)** / Spray / keine; Ersatzpunkt Plattenvorderseite nötig? | |
| Antwort F7: Internet/GitHub erlaubt? Stick erlaubt? | |
| Antwort F8: Handbücher kopieren erlaubt? | |
| Rechnername | BEOWOLF (bestätigen) |
| Windows-Version | |
| PSV-Version und Optionen (*Hilfe > PSV Info*; Foto) | |
| Python-Version (`& $PY --version`) / Bitness (soll 64) | |
| Installationsweg (G Git / S Stick / R Bestand) | |
| Wheel (erwartet `ldv_automation-0.2.0-py3-none-any.whl`): Dateiname / **SHA-256** (`Get-FileHash`) / erwarteter SHA-256 (vorab notiert) | |
| **Git-Hash des Wheels** (`_build_info.json`, I6) / `git_dirty` (soll false) | |
| Hash stimmt mit dem Stand auf dem Branch überein (ja/nein) | |
| Skriptordner `$ARB` / Ausgabeordner `$T` | |
| `erkundung.py` Version / `skript_sha256` (aus `bericht.json`); `einstellungen_lesen.py`, `daten_lesen.py`: Stand | |
| `pip list`: PySide6_Essentials / shiboken6 / pywin32 / ldv-automation | |
| Konfigurationsdatei: Pfad der Kopie / SHA-256 / gleich der Angabe im Dialog „Gerät …“ und im Messprotokoll (ja/nein) | |
| Messdaten-Ordner (nicht im Repository; `PyCharmProject` ist Git-Repository ja/nein/unbekannt) | |

## 2 Entscheidungsprotokoll (Knoten des Entscheidungsbaums)

Je Knoten: Uhrzeit, Beobachtung, gewählter Pfad. Pfad A = COM an, Pfad B = COM aus. Ersatzplan (EP-1 bis EP-7) angeben, wenn ausgelöst.

| Knoten | Frage | Uhrzeit | Ergebnis / Beobachtung | Entscheidung / Pfad / EP |
|---|---|---|---|---|
| K1 | Nur 0 oder 1 PSV-Prozess? (`Get-Process PSV`) | | | |
| K2 | `PSV.AcquisitionInstance` registriert? Zeigt `LocalServer32` auf 10.4? | | | |
| K3 | Registrierung nachgeholt (nur mit Zustimmung Daniel)? Ergebnis, Zeitlimit 30 min eingehalten? | | | |
| K4 | Installation/Update: I1 bis I4 ok? | | | |
| K5 | Stufe 1: Verbinden ok? | | | |
| K6 | Anregung freigegeben (siehe F2)? | | | |
| K7 | PSV hängt / Dialog / Laser unerwartet? | | | |
| K8 | Zeitstand (Rest in Minuten); gestrichene Punkte; Entscheidung Zeitverlust (Ablaufplan 4.2) | | | |
| K9 | Sicherung (A2) begonnen | | | |

## 3 Schritt 0 (A0): Registrierung, Stufe 0, PSV-Instanz

| Feld | Eintrag |
|---|---|
| `Get-Process PSV` vor Start: Anzahl, PID, StartTime | |
| Stufe 0: Ausgabeordner / Exit-Code | |
| `P1-2-registry`: `PSV.AcquisitionInstance` / `PresentationInstance` / `Application` registriert (ja/nein) | |
| `LocalServer32` (Pfad, Version 10.4?) | |
| Weitere PSV-Prozesse in `psv_prozesse` (Fehltreffer?) | |
| `P1-4-pywin32` | |
| `PolyFile.PolyFile`, PolyMath-Typbibliothek vorhanden (ja/nein) | |
| Registrierung durchgeführt: Befehl, ausgeführt von, Zeit, Ergebnis; Reparaturinstallation nötig | |
| PSV gestartet über „PSV 10.4 Deutsch“; **PID**, StartTime | |
| CommandLine enthält `/Acquisition` (ja/nein; Befehl `Get-CimInstance Win32_Process …`) | |
| Keine Dialoge offen, keine Messung | ☐ |

Fürs Protokoll der Registrierung:

| Zeit | Befehl / Aktion | ausgeführt von | Ergebnis |
|---|---|---|---|
| | `PSV.exe /regserver` in `C:\Program Files\Polytec\PSV 10.4` (Admin) | | |

## 4 Installation/Update (A1), Prüfschritte I1 bis I7

| Nr | Ergebnis (ok/Abweichung) | Meldung / Abweichung | Dateien |
|---|---|---|---|
| Installationsbefehl (Weg; `pip install --upgrade --no-deps`, Rückfall `--force-reinstall` nur falls nötig: ja/nein), Ausgabe von pip | | | |
| I1 Python-Version | | | |
| I2 Bitness | | | |
| I3 `pip list` (`ldv-automation 0.2.0`?) | | | |
| I4 `import win32com.client` (gen_py-Cache angelegt?) | | | |
| I5 `selbsttest` („Selbsttest bestanden“?) | | | |
| I6 Build-Info (`git_hash`, `git_dirty`) | | | |
| I7 GUI im Simulator (Titel, Symbole ○ ▶ ✔ ✖ ■ ⏸ ⚠ sichtbar) | | | |
| Skripte neu geholt (Name, SHA-256); alte als `*_alt.py` beiseite | | | |

Ersatzplan EP-3 ausgelöst? ☐ ja ☐ nein. Welcher Stand wurde stattdessen genutzt (z. B. 530af419)? ____

## 5 Erkundung Stufe 1 / 1b (B1)

| Stufe | Ausgabeordner | Exit-Code | Ergebnis / Auffälligkeit | Fenster in PSV aufgepoppt? |
|---|---|---|---|---|
| 1 | | | | |
| 1b (Datei: ) | | | | |

| Befund | Eintrag |
|---|---|
| `P1-5-verbinden`: Status, Dauer; bei Fehler `hresult_hex`, `excepinfo` | |
| `Mode` / `State` beim Verbinden | |
| PSV-Prozessname(n) mit „psv“ (nur PSV selbst?) | |
| Validator `FftAcqPropertiesValidator` vorhanden (ja/nein) | |
| Konstanten wie I5 §8 (ja/Abweichung) | |
| `SuppressMessagesForAutomation` (True/False; Bezeichnung in PSV: ) | |
| Durchsicht vor Upload erledigt (Pfade, Kontonamen) | ☐ |

## 6 Desktop-Modus bewusst testen (X1)

| Feld | Eintrag |
|---|---|
| Zeitpunkt (nach B4 / früh als Diagnose) und Grund | |
| PSV beendet (Speichern: Nein), `Get-Process PSV` leer | ☐ |
| Start „PSV 10.4 Desktop Deutsch“; PID; CommandLine `/Desktop`; Fenstertitel | |
| Stufe 1 im Desktop-Modus: Ausgabeordner / Exit-Code | |
| **Fehlerbild** (`P1-5-verbinden`-Status, Meldung, `hresult_hex`, `excepinfo`, Dauer) | |
| Fenster in PSV aufgepoppt (ja/nein, Foto) | |
| Neustart „PSV 10.4 Deutsch“; neue PID; Stufe 1 erneut (Gegenprobe): Ergebnis | |
| Unterschied der Fehlerbilder (Registrierung vs. Modus) in einem Satz | |

## 7 Schalter und Werte (B2)

Die Vorgaben sind Annahmen; „Ermittelt“ nach dem Test eintragen. Werte in eine Kopie von `beispiel_messrechner.json`.

| Größe | Vorgabe (Annahme) | Ermittelt / eingestellt | Wie ermittelt (Schritt) | in Konfig eingetragen |
|---|---|---|---|---|
| `aufruf_grenze_s` | 60 s, unbelegt | | | |
| `aufruf_warnung_s` | 5 s | | | |
| `stop_frist_s` | 10 s | | 5-1 / T5 | |
| Zeitlimit je Messung (`standard_zeitlimit_s`) | 600 s, unbelegt | | T4 | |
| Dauer je Messpunkt | Schätzung 1 s | | T4 | |
| Lademaske | Acquisition, Alignment, APS, 2DAlignment, 3DAlignment | | T2 | |
| Prozessname (`PSV_PROZESS_KENNUNG`) | enthält „psv“ | Abbildname: | T1 1-0 | |
| Codec der Prozessliste | `oem` | Umlaute korrekt (ja/nein): | T1 | |
| `validator_rueckfall_direkt` | False | | Erkundung | |
| Blockiert `ScanEx` bis zum Scanende? | unbekannt | | T4 / U3 4-2 | |
| **Erster `State` nach `ScanEx`** | erwartet ScanAll = 3 | | T4 / U3 4-1a | |
| **Einrastwert bei 5600 Hz** | Erwartung z. B. 6250 Hz | | T2 / U3 2-2 | |
| Ordner, in denen PSV selbst Daten ablegt | – | | Pfadregeln der Sitzung | |

## 8 Test-.set und Prüfling (B3)

| Feld | Eintrag |
|---|---|
| Datei (Pfad, SHA-256) / Kopie | |
| Messmodus | |
| Messpunkte (Anzahl, Gitter) | |
| Abgleich nötig / durchgeführt (Bezeichnung in PSV) | |
| **Generator aus** (kontrolliert im PSV-Bild) | |
| Bandbreite (Hz) / Linien | |
| Mittelung Anzahl / Art | |
| Trigger / Referenz | |
| Rückprobe (Laden zeigt dieselben Werte?) | |
| Gefundene Menüpfade (für spätere Anleitung) | |
| Prüfling (Beschreibung, Lagerung); Shaker/Verstärker getrennt/aus (ja/nein); Freigabe durch Daniel (siehe Kopf) | |

## 9 Prototyp-Prüfungen T0 bis T2 (B4)

Je Zeile: ✔ (wie erwartet) / ✖ (abweichend), Abweichung, Dateien. Erwartungen in der [Prüfanleitung U3](../2026-11-02_prototyp/pruefanleitung_U3_com-adapter.md).

| Schritt | Beginn (Uhrzeit) | Ergebnis | Abweichung / Beobachtung | Dateien |
|---|---|---|---|---|
| T0 Selbsttest und GUI (Simulator), Handtest F4 Symbole | | | | |
| T1 `NUR_LESEN`: 1-0 Prozesstreffer nur PSV | | | | |
| 1-1 Version/Modus/Hardware | | | | |
| 1-2 `GESTOPPT` | | | | |
| 1-3 `modus == Fft`, FFT-Werte | | | | |
| 1-4 Kanäle/Generator | | | | |
| 1-5 `verweigert` leer | | | | |
| 1-6 kein Dialog, keine Laser-/Spiegelbewegung | | | | |
| U5: Dialog „Gerät …“ (Zugriffe ohne Verweigerung, Messpunkte, Generator, `psv_prozesse`, Lademaske) | | | | |
| T2 `TROCKENLAUF`: 2-1 Laden ohne Dialog | | | | |
| 2-2 Einrasten bei 5600 Hz (Wert) | | | | |
| 2-3 Werte = PSV-Anzeige | | | | |
| 2-4 Nachweis-.set; zweites Speichern abgelehnt | | | | |
| 2-5/2-6 `starte_scan` abgelehnt, `verweigert` leer | | | | |
| 2-7 keine Laser-/Spiegel-/Generatoraktivität | | | | |
| PSV-Einstellungen nach T2 wieder auf Stand vorher gebracht (Foto) | | | | |
| Simulator-Vorführung statt T1/T2 (nur bei EP-1) | | | | |

**Entscheidung echte Messung über das Programm (T4 ff.):** ☐ ja ☐ nein · Uhrzeit ____ · Grund ____ · T1/T2 ohne Befund ☐ · Anregung freigegeben ☐

| Schritt (D5, nur nach Entscheidung) | Beginn | Ergebnis | Abweichung / Beobachtung | Dateien |
|---|---|---|---|---|
| Startdialog T4: Messpunkte/Generator „aus (übernommen)“ ja/nein (sonst rote Warnung, Generator von Hand geprüft: ja/nein); Trockenlauf mit derselben .set, kein PSV-Neustart | | | | |
| T4: 4-1, 4-1a (erster State), 4-2 (blockiert?), 4-3 (Dauer) | | | | |
| T5: 5-1 `Stop` genau einmal, `Stopped` innerhalb Frist; 5-2 Teilpunkte-Datei | | | | |
| 6-1 vorhandene Zieldatei: kein PSV-Aufruf | | | | |
| T6: drei Messungen, Pausenpunkt, Bearbeiten im Lauf | | | | |
| T7 (optional) | | | | |

Zuordnung Messung ↔ Datei (**über Name/ID im Messprotokoll**, nicht über Tabellen-Nr):

| Name/ID im Protokoll | Tabellen-Nr (vorläufig) | Dateinummer | Zieldatei `.svd` | Status |
|---|---|---|---|---|
| | | | | |

## 10 Prüfzettelpunkte (Zweig C, D, E, B5)

Zu jedem Punkt: Entscheidung (Zeit, Grund) vor Messungen in D. Dateien immer mit Name, Ort und SHA-256 bzw. Größe.

### 10.1 C1 Kopien und C5 Beobachtung `einstellungen_lesen.py`

| Feld | Eintrag |
|---|---|
| Original `20261012_ref_Mitte.svd` (Ort); Größe soll 27 115 520 Byte sein | |
| Kopie für PSV (Name) / Kopie für File Access (Name) / Größe gleich | |
| `einstellungen_lesen.py` lief; Datei: | |
| **Zeilen mit „übersprungen (aufrufbar, keine Eigenschaft)“** (Name; ist es in PSV/Doku eine Eigenschaft? ja/nein) | |
| Nicht lesbare / nicht vorhandene Einträge (Auffälligkeiten) | |

### 10.2 C2 M11 an drei Spitzen ohne Kennzeichen (H1 Vib Z & Ref1, Label 132 bzw. gewählter Punkt: ____)

Kandidaten (FG-02 Abschnitt 8, Hz der korrigierten Achse): 617,9 · 631,7 · 644,8 · **693,5 · 757,3 · 867,9** (am aussichtsreichsten, Vorabrechnung der Fachprüfung [N]; B ≥ 3Δf = 1,875 Hz erst ab ca. 670 Hz). **Vorab geprüft (V2):** an Label 132 kennzeichenfrei und im ±2B-Band sauber: **921,5 · 632,5 · 483,8 Hz** (Reserve 949,3 · 644,8); Bandgrenzen und eigene Vergleichswerte in Ablaufplan C2.
Bandregel: Grenzen als Vielfache von Δf = 0,625 Hz, mindestens 7 Linien, mehrere B breit, **zwei Bänder je Spitze** (z. B. ±2 B und ±4 B). **Q und ζ mit voller angezeigter Stellenzahl** ablesen (ζ = 1/(2Q)); f max nur 0,1 Hz (Grenze vermerken).

| Spitze (Hz) | Band (1 oder 2) | Kennzeichen in Stufe 1 am Punkt (keins?) | Cursorgrenze links (Hz) | rechts (Hz) | Linien im Band | f max (Hz) | −3 dB (Hz) | Q (volle Stellen) | ζ (volle Stellen) | Screenshot |
|---|---|---|---|---|---|---|---|---|---|---|
| | 1 | nein | | | | | | | | |
| | 2 | nein | | | | | | | | |
| | 1 | nein | | | | | | | | |
| | 2 | nein | | | | | | | | |
| | 1 | nein | | | | | | | | |
| | 2 | nein | | | | | | | | |

Klickpfad bestätigt (Alt+2, Analysator → Band-Cursor, Cursor-Eigenschaften → Peak-Anpassung, Strg+K): ☐ · Abweichung: ____ · Mehr Nachkommastellen für f max einstellbar: ja/nein, wie: ____

### 10.3 C3 Golden File v2

| Feld | Eintrag |
|---|---|
| Punkt (Label/Nummer) | |
| Kanal-/Signalnamen aus PSV abgelesen (H2, Kohärenz, PSD/ESD, H1 Ref2/Ref1, Terzen) | |
| Aufruf, Ausgabedatei, **Exit-Code** (0/1/2/3) | |
| Begleitdatei `.fehlend.txt` (fehlende Signale) | |
| Ersatz: ASCII-Export aus PSV (Format, Optionen, Dateien) | |
| **H1 Ref2/Ref1** zuerst: gelesen (File Access) oder im Analysator Kanal „Ref2 & Ref1“ abgelesen/exportiert; Phase 0°/180° bei 1 bis 6 Hz; Betrag m = \|F/a\| (kg) bei 1 bis 6 Hz | |
| **Skalierung:** einseitig/zweiseitig; PSD/ESD RMS oder Spitze; Fensterkorrektur; Terzbasis (10 oder 2); Mittenfrequenzen; Mittelungsart | |

### 10.4 C4 Generator-Dialog ablesen (Soll; nur lesen, nichts ändern)

| Feld | Eintrag |
|---|---|
| Quelle (Beispieldatei-Einstellung / aktuelle PSV-Einstellung), Foto | |
| Signalform | |
| Burstlänge / weitere Parameter | |
| Amplitude (V) | |
| Optional: Cast im Skript versucht (wie), Ergebnis | |

### 10.5 B5 `PolyMath.PeakFit` per COM (Testdaten mit Sollwerten)

| Feld | Eintrag |
|---|---|
| ProgID/Objekt angelegt (ja/nein, Meldung); Methode (`Fit`/`FitXY`), fittet auf \|H\| oder komplex (offen) | |
| Fall 1: f_n = 700 Hz, ζ = 0,01, m = 1 kg, Raster 0,625 Hz bis 1000 Hz, Band 665 bis 735 Hz. Soll f = 700,0 Hz (±0,01), ζ = 0,0100 (±1 %). Ist f / ζ | |
| Fall 2: f_n = 670 Hz, ζ = 1,4·10⁻³ (B/Δf = 3,0), zwei Bänder. Soll: Modellfit nahe exakt (Bias −3-dB-Schätzer +2,6 % bis +5,2 %). Ist f / ζ je Band | |
| Reale Daten: gleiche Bandgrenzen wie C2, f / ζ im Vergleich zur PSV-Peak-Anpassung | |
| Auffälligkeiten (Dialog, Dauer) | |

### 10.6 C6 UFF-Export / Exportformate

| Feld | Eintrag |
|---|---|
| UFF-Export (Datei, Signale, Optionen) | |
| ATFX wählbar (ja/nein) / ME'scope wählbar (ja/nein) / Lizenzhinweis in PSV | |
| Weitere Formate in der Liste (Foto) | |

### 10.7 C7 File Access bei in PSV geöffneter Datei

| Feld | Eintrag |
|---|---|
| Kopie in PSV geöffnet; Skript, Aufruf | |
| Ergebnis (Fehlermeldung, Werte vorhanden, Werte aktuell?) | |
| Dialog/Reaktion in PSV | |

### 10.8 C8 Restpunkte M13 bis M15

| Nr. | Annahme | Abgelesen / gerechnet | Bestätigt / abweichend |
|---|---|---|---|
| M13 | Normalen +z; 3D-Abgleich-Achsen im Geometrie-KS | Achsenbezeichnungen im Abgleich-Dialog: ___ · Kopfpositionen im Geometrie-KS: ___ · +z zeigt zu den Scanköpfen (ja/nein) · offline: \|n_z\| der Plattenebene (Soll ≈ 1) ___ | |
| M14 | Elementindizes 0-basiert (nur wenn Elemente vorhanden) | Datei enthält Elemente (ja/nein) · Element ___: Eckpunkt-Labels ___ | |
| M15 | Zeitstempel je Punkt = Messzeit | Scan-Start/-Ende nach Rechneruhr (aus D1): ___ · Zeitstempel je Punkt: ___ · Offset konstant, Differenzen = Uhrzeit auf ±1 s (ja/nein) | |

### 10.9 D1 Mini-Scan 3×3 mit Zeitdaten

| Feld | Eintrag |
|---|---|
| Freigabe (F2/F4) und Entscheidung (Zeit, Grund) | |
| Einstellungen vorher (Foto): Signal Enhancement ___ · `SaveTimeDataForScan` aus | |
| `SaveTimeDataForScan` an; Bezeichnung in PSV: ___ | |
| **Signal Enhancement auf „Fast“ gesetzt?** (ja/nein); danach zurückgestellt auf ___ | |
| Generator (Amplitude, Signalform, Burstlänge aus C4), Verstärkerstellung | |
| Raster (3×3, Punkte, Abgleich) | |
| Zieldatei (neuer Name, Ordner) / Dateigröße / Beginn–Ende (**Rechneruhr**) / Dauer je Punkt | |
| **Referenzscan:** entfällt, R aus Block 2 (`20261109_ref3x3_01.svd`) ist Referenz, wenn SE und sonstige Einstellungen gleich blieben (Versuchsplan 5.3). Hier von R notieren: Dauer, SE-Einstellung, Zahl erfasster Blöcke je Punkt | |
| Zeitdaten mit File Access auf der Kopie lesbar (ja/nein, Namen) | |
| Auswertung später: (a) eigene FFT je Block gegen PSV-Spektren (rtol 1e-5); (b) n_d aus Mittelung über n Blöcke; (c) Streuung je Block gegen FG-02 3.4; (d) Zeitstempel gegen Uhr (M15) | |
| Auffälligkeiten | |

### 10.10 D2 Messpunkt auf dem Impedanzkopf

| Feld | Eintrag |
|---|---|
| Freigabe (F2/F6) und Entscheidung (Zeit, Grund); Sichtbarkeitsprüfung (Dauer, Kopf von allen drei Scanköpfen einsehbar ja/nein); Ersatzpunkt Plattenvorderseite genutzt ja/nein | |
| Messdatei (neuer Name, Ordner), Wiederholungsmessung (Name) | |
| Winkel θ Kraftachse gegen Laser-Z (Foto); Vib X / Vib Y mit aufgezeichnet (ja/nein) | |
| Folie / Spray / keine; Fläche; Punktstatus („Optimal“/„Gültig“) | |
| Einstellungen wie Beispieldatei (Bandbreite 1000 Hz, f_s 2500 Hz, 4000 Samples, Rechteck, komplexe Mittelung, n_d ≥ 7 (≥ 10 angestrebt), Decoder-Bereich, SE-Einstellung) | |
| SignalDelay Vib / Ref1 / **Ref2** vor der Messung | |
| SignalDelay Vib / Ref1 / **Ref2** nach der Messung (SE-Wirkung?) | |
| Mittlere Kohärenz 20 bis 50 Hz / 100 bis 1000 Hz (Vib Z & Ref2; Vib Z & Ref1) | |
| φ(Vib Z / Ref2) bei 20 Hz / 30 Hz / 50 Hz (Vor-Ort-Schnellprüfung) | |
| φ(Vib Z / Ref1) bei 20 / 30 / 50 Hz | |
| **τ_res aus Fit** (φ(f) = φ₀ − 360°·f·τ_res, nach dem Termin; Akzeptanz-Arbeitswert ≤ 14 µs) | |
| φ₀ aus Fit: +90° / −90° (nach Entscheidungstabelle im Ablaufplan: Schluss) | |
| \|H1\|·ω bei 100 / 500 / 900 Hz (Soll 1; Arbeitswert 0,95 bis 1,05) | |
| Vib Z / Ref1 am Treibpunkt: Anteil Linien mit Re ≥ 0 (nur γ² ≥ 0,9) / Phase in [−90°, +90°] ja/nein | |
| Schluss nach Entscheidungstabelle (Ref2 gedreht / beide konsistent / Ref1 gedreht / Ref1 und Ref2 gedreht) | |
| Datenblatt PCB 288D01 gefunden/gelesen (Polarität; erklärt die Ursache, ersetzt die Messung nicht) | |

### 10.11 D3 Zwei-Amplituden-Test A-B-A (Label 132 oder Kopfpunkt aus D2)

| Feld | Eintrag |
|---|---|
| Freigabe (F2: auch 0,04 V, ggf. 0,01 V) und Entscheidung (Zeit, Grund) | |
| Punkt (Label 132 bzw. Koordinaten bzw. Kopfpunkt), Raster/.set | |
| Messung A1 0,02 V: Datei, Beginn–Ende, Verstärkerstellung | |
| Messung B 0,04 V: Datei, Beginn–Ende, Verstärkerstellung | |
| Messung A2 0,02 V: Datei, Beginn–Ende, Verstärkerstellung | |
| Optional 0,01 V: Datei | |
| Sonstige Einstellungen identisch (Fenster, Mittelung, Bandbreite) | |
| Ref1-Autospektrum: Verhältnis B/A (Soll ≈ 2 im Betrag der Amplitude; sonst Sättigung) | |
| Kohärenz < 60 Hz: A1 / B / A2 (rauschbegrenzt: 1−γ² sinkt bei B etwa um Faktor 4) | |
| Auswertung später: A-A (Drift) gegen A-B (Nichtlinearität); \|H1\| und Phase abseits der Spitzen; f_r, ζ der Spitzen 160,6 / 247,7 Hz über B-1 | |
| Auffälligkeiten (Übersteuerung, Overrange) | |

### 10.12 D4 Wiederholungsmessung T8 (Kann; nur nach Freigabe und eigener Entscheidung; Scandauer ca. 40 min; sonst Folgetermin)

| Punkt | Eintrag |
|---|---|
| Entscheidung (Zeit, Grund), über Programm oder direkt in PSV | |
| Dateiname(n) `.svd` | |
| gleicher Aufbau / Raster neu abgeglichen bzw. verschoben? | |
| Temperatur Anfang / Ende | |
| Beginn / Ende (Uhrzeit) | |
| Änderungen am Aufbau, Auffälligkeiten | |

### 10.13 E1 Wiegen

Erwartung grob **4,5 bis 6,7 kg** für die Masse auf der Plattenseite des Kraftsensors (aus dem Golden File, [N], ±20 %). Gemeint: Platte + plattenseitige Kopfhälfte + Schrauben, Folie, anteilige Kabel; **Stinger und Shaker nicht**. Gültiger Bereich der Massenlinie nur bis ca. 5 Hz.

| Feld | Eintrag |
|---|---|
| Fotos vor dem Abbau; Zustimmung Daniel | |
| Waage (Typ, Auflösung, Kalibrierstand) | |
| Platte: Masse (3 Ablesungen) / Maße (L × B × H) / Material | |
| Impedanzkopf: Masse (3 Ablesungen) / Datenblattwert | |
| Weitere Teile (Kopplung, Stinger, Seile, Folie, Markierung), Zuordnung zur Plattenseite ja/nein | |
| Summe Plattenseite (kg) / im Bereich 4,5 bis 6,7 kg (ja/nein) / Vergleich mit m = \|F/a\| aus C3 (H1 Ref2/Ref1, 1 bis 6 Hz) | |
| Aufbau wieder hergestellt wie vorher (Foto) | ☐ |

### 10.14 E2 Handbücher 10.4

| Datei | Größe | SHA-256 | gleich der vorhandenen Fassung in `Input/literatur/polytec/Handbücher/` (ja/nein/unbekannt) | Ziel |
|---|---|---|---|---|
| Theory Manual.pdf | | | | |
| Software Handbuch PSV.pdf | | | | |
| Software Manual PSV.pdf | | | | |
| Software Handbuch / Manual PSV Desktop | | | | |
| Basic Engine Manual.chm | | | | |
| Release Notes | | | | |

## 11 Ersatzpläne, Abbruch und Auffälligkeiten

| Uhrzeit | Ersatzplan (EP-1 bis EP-7) bzw. Kriterium | Auslöser / Beobachtung | Maßnahme | Gesichert (Dateien, Foto) |
|---|---|---|---|---|
| | | | | |

Abbruchkriterien (aus dem alten Plan): unerwarteter Dialog; Laser/Spiegel bewegt sich unerwartet; „verweigert“ in der Oberfläche (nicht bewusst provoziert); GUI/PSV reagiert über die Wächtergrenze nicht; eine vorhandene Datei wurde verändert; Generator gibt unerwartet aus;
`psv_prozesse` enthält etwas anderes als PSV; **4-1a:** erster Poll nach `ScanEx` liefert `Stopped`, obwohl der Scan danach läuft (sofort aufhören, PSV manuell stoppen); `State` wird nach `Stop` nicht `Stopped` (`GERAET_UNKLAR`); Konstanten weichen von I5 §8 ab.
Danach: Programm/Konsole schließen, **PSV nicht beenden, solange eine Messung läuft**, Zustand in PSV selbst prüfen.

## 12 Gestrichene Punkte (Zeitmangel, EP-6)

| Punkt (Nr) | Grund | Folgetermin? |
|---|---|---|
| | | |

## 13 Abschluss

| Punkt | Erledigt |
|---|---|
| Erkundungsordner, Durchgangsordner, Konsolenausgaben, Protokoll gesichert; Pfade/Kontonamen geprüft | ☐ |
| Test-.set, Nachweis-.set gesichert | ☐ |
| Neue `.svd`, Exporte, Golden File v2, Handbücher gesichert | ☐ |
| PSV in sauberem Zustand (keine Messung, kein Dialog); eine Instanz oder beendet | ☐ |
| Shaker/Verstärker aus bzw. getrennt, Aufbau wie vorher (Fotos) | ☐ |
| PSV-Einstellungen zurückgestellt (SE, Generator, Modus) | ☐ |
| Ende (Uhrzeit) | |
| Was ich als „am Gerät bestätigt“ gelten lasse (je Schritt): | |
| Offene Punkte / Fragen für `/laborbuch`, Daniel und Betreuer | |
