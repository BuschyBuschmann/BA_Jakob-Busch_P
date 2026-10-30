# Protokoll vor Ort: PSV-Messrechner, Mo 2026-11-02 (zum Ausfüllen)

Zum Ausfüllen am Messrechner (Ausdruck oder Datei). Ablauf: [ablaufplan_vor_ort.md](ablaufplan_vor_ort.md).
Ein Befund gilt erst als „am Gerät bestätigt“, wenn du ihn bestätigt hast. Vorgabewerte in der Spalte
„Vorgabe“ sind **Annahmen**, keine Messwerte. Nichts nachträglich schönen; Fehlschläge eintragen.

## 1 Kopf

| Feld | Eintrag |
|---|---|
| Datum / Uhrzeit Beginn | |
| Bearbeiter | Jakob |
| Rechnername (Messrechner) | |
| Windows-Version | |
| PSV-Version und Optionen (Hilfe > PSV Info; Foto/Text sichern) | |
| Python-Version (`python --version`) | |
| Python-Bitness (soll 64) | |
| Installationsweg (A ohne Internet / B mit Internet) | |
| Wheel: Dateiname | `ldv_automation-0.1.0-py3-none-any.whl` |
| Wheel: SHA-256 (`Get-FileHash`) | |
| **Git-Hash des Wheels** (`_build_info.json`, Prüfschritt I6) | |
| `git_dirty` (soll false) | |
| Konfigurationsdatei: Pfad der Kopie (Vorlage `beispiel_messrechner.json`) | |
| Konfigurationsdatei: SHA-256 (`Get-FileHash`), gleich der Angabe im Dialog „Gerät …“ und im Messprotokoll (ja/nein) | |
| Hash stimmt mit dem Stand auf dem Branch überein (ja/nein) | |
| Version `erkundung.py` / `skript_sha256` aus `bericht.json` | |
| `pip list`: PySide6_Essentials / shiboken6 / pywin32 | |

## 2 Installation (Prüfschritte I1 bis I7, [Installation](installation_messrechner.md), Abschnitt 6)

| Nr | Ergebnis (ok/Abweichung) | Meldung / Abweichung | Dateien |
|---|---|---|---|
| I1 Python-Version | | | |
| I2 Bitness | | | |
| I3 `pip list` | | | |
| I4 `import win32com.client` (gen_py-Cache angelegt?) | | | |
| I5 `selbsttest` („Selbsttest bestanden“?) | | | |
| I6 Build-Info | | | |
| I7 GUI im Simulator (Titel, Symbole sichtbar) | | | |

## 3 Erkundung

| Stufe | Ausgabeordner | Exit-Code | Ergebnis / Auffälligkeit | Fenster in PSV aufgepoppt? |
|---|---|---|---|---|
| 0 | | | | |
| 1 | | | | |
| 1b (Datei: ) | | | | |

Zusätzlich aus Erkundung / PSV:

| Befund | Eintrag |
|---|---|
| `PSV.AcquisitionInstance` Server-Art (`LocalServer32`?) | |
| Prozessname(n) mit „psv“ (`psv_prozesse`; nur PSV selbst?) | |
| Validator `FftAcqPropertiesValidator` vorhanden (ja/nein) | |
| Konstanten wie I5 §8 (ja/Abweichung) | |
| `SuppressMessagesForAutomation` (True/False; Bezeichnung in PSV vor Ort: ) | |
| Mode / State beim Verbinden | |
| Durchsicht vor Upload erledigt (Pfade, Kontonamen) | ☐ |

## 4 Schalter und Werte, die am Montag zu bestimmen sind

Die Vorgaben sind Annahmen; „Ist/Ermittelt“ nach dem Test eintragen. Die Werte werden in eine Kopie von
`beispiel_messrechner.json` eingetragen und mit `--konfig` gestartet (Ablaufplan, Abschnitt 4). Spalte
„in Konfig eingetragen“: Schlüssel und Wert, den die Kopie enthält (leer = Vorgabe belassen).

| Größe | Vorgabe (Annahme) | Ermittelt / eingestellt | Wie ermittelt (Schritt) | in Konfig eingetragen |
|---|---|---|---|---|
| `aufruf_grenze_s` (Dauer eines Geräteaufrufs bis `GERAET_UNKLAR`) | 60 s, unbelegt | | | |
| `aufruf_warnung_s` (Wächterhinweis) | 5 s | | | |
| `stop_frist_s` (Stopped nach `Stop`) | 10 s | | 5-1 / T5: Dauer bis `Stopped` | |
| Zeitlimit je Messung (`zeitlimit_s`, global) | 600 s, unbelegt | | T4: gemessene Dauer | |
| Dauer je Messpunkt | Schätzung 1 s | | T4 | |
| Lademaske (`Settings.Load`) | Acquisition, Alignment, APS, 2DAlignment, 3DAlignment (ohne Camera, Windows) | | T2: Teil-Laden bemerkt? | |
| Prozessname (`PSV_PROZESS_KENNUNG`) | enthält „psv“ | Abbildname: | T1 1-0 | |
| Codec der Prozessliste (`TASKLIST_CODEC`) | `oem` | Umlaute/Prozessliste korrekt dekodiert (ja/nein): | T1 | |
| Validator-Schalter `validator_rueckfall_direkt` | False (Validator vorhanden) | | Erkundung 3 | |
| Blockiert `ScanEx` bis zum Scanende? | unbekannt | | T4, U3 4-2 (Wächterhinweis „reagiert nicht seit … s“ während des Scans) | |
| **Erster `State` nach `ScanEx`** | erwartet ScanAll = 3 | | T4, U3 4-1a (Abbruch bei `Stopped`) | |
| **Einrastwert bei 5600 Hz** (`fft.bandbreite_hz` zurückgelesen) | Erwartung z. B. 6250 Hz (nur Erwartung) | | T2, U3 2-2 | |
| Symbole / Schrift (○ ▶ ✔ ✖ ■ ⏸ ⚠ alle sichtbar?) | Unicode | ja/nein; ggf. `ASCII_RUECKFALL` nötig? | I7, Handtest F4 | |
| Ordner, in denen PSV selbst Daten ablegt | – | | Handtest-Einstellungen, Pfadregeln der Sitzung (K-U5b) | |

## 5 Test-.set und Prüfling

(Zielwerte und Hinweise: [anleitung_test_set.md](anleitung_test_set.md))

| Feld | Eintrag |
|---|---|
| Datei (Pfad, SHA-256) | |
| Messmodus | |
| Messpunkte (Anzahl, Gitter) | |
| Abgleich nötig / durchgeführt (Bezeichnung in PSV) | |
| Generator (aus?) | |
| Bandbreite (Hz) / Linien | |
| Mittelung Anzahl / Art | |
| Trigger / Referenz | |
| Rückprobe (Laden zeigt dieselben Werte?) | |
| Prüfling (Beschreibung, Lagerung) | |
| Shaker/Verstärker angeschlossen? Freigabe durch Betreuer? | |

## 6 Prototyp-Prüfungen

Je Zeile: Ergebnis ✔ (wie erwartet) / ✖ (abweichend), Abweichung, erzeugte Dateien. Erwartungen in der
[Prüfanleitung U3](pruefanleitung_U3_com-adapter.md) und im [Plan P2 §9](../../planung/plaene/2026-10-26_P2_architektur-prototyp.md).

| Schritt | Beginn (Uhrzeit) | Ergebnis | Abweichung / Beobachtung | Dateien |
|---|---|---|---|---|
| T0 Selbsttest und GUI (Simulator) | | | | |
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
| Handtest U4 Teilmenge (welche Nr, Ergebnis) | | | | |
| T3 Meldungsprobe (optional) | | | | |
| **Entscheidung echte Messung: ja/nein, Uhrzeit, Grund** | | | | |
| Startdialog T4: Messpunkte/Generator „aus (übernommen)“ ja/nein (sonst „unbekannt“, rote Warnung, Generator von Hand geprüft: ja/nein); Trockenlauf mit derselben .set, kein PSV-Neustart: ja/nein | | | | |
| T4: 4-1, 4-1a (erster State), 4-2 (blockiert?), 4-3 (Dauer) | | | | |
| T5: 5-1 `Stop` genau einmal, `Stopped` innerhalb Frist; 5-2 Teilpunkte-Datei | | | | |
| 6-1 vorhandene Zieldatei: kein PSV-Aufruf | | | | |
| T6: drei Messungen, Pausenpunkt, Bearbeiten im Lauf | | | | |
| T7 (optional) | | | | |

Zuordnung Messung ↔ Datei (**über Name/ID im Messprotokoll**, nicht über Tabellen-Nr):

| Name/ID im Protokoll | Tabellen-Nr (vorläufig) | Dateinummer | Zieldatei `.svd` | Status |
|---|---|---|---|---|
| | | | | |

## 6b Auswertungs-Prüfungen (Ablaufplan 7b) und Wiederholungsmessung (T8)

Kopie von `20261012_ref_Mitte.svd` verwendet: ☐ · Label 132 · Screenshots: ________

| Nr. | Annahme (Voreinstellung) | Abgelesen in PSV | Bestätigt / abweichend |
|---|---|---|---|
| M1 | `konjugieren = False` | Phase H1 Vib X & Ref1: 100 Hz ___ · 500 Hz ___ · 1000 Hz ___ | |
| M2 | k₀ = 1 (1,5625 … 2500 Hz) | erste ___ Hz · letzte ___ Hz | |
| M4 | 0-to-peak | Vib X Geschw.: 100 Hz ___ · 500 Hz ___ · 1000 Hz ___ · Skalierung ___ | |
| M5 | Rechteck, n_d = 7 | Fenster ___ · Signalform ___ · Burstlänge ___ · Mittelung ___ · Enhancement ___ | |
| M6 | alle Punkte gültig | Status der Punkte mit Wert 1/3: | |
| M7 | Gültigkeit > 1 kHz offen | „Bandbreitenbereich 1 kHz“ bedeutet: | |
| M8 | s = +1 für Ref1, Ref2 | Kraftsensor: Typ ___ Ort ___ Richtung ___ · Beschl.-Aufnehmer: Typ ___ Ort ___ Richtung ___ · Shaker ___ | |
| M10 | Band geschlossen | RMS Vib Z Geschw. 100–200 Hz: ___ | |
| M11 | Toleranzen FG-02 Abschn. 8 | siehe Tabelle unten | |
| M12 | 3D-Komponenten im Geometrie-KS | | |
| M13 | Normalenbezug +z | | |
| M14 | Elementindizes 0-basiert | Element ___: Labels ___ | |
| M15 | Zeitstempel je Punkt = Messzeit | | |
| Export | Golden File | Format/Optionen: ___ · Dateien: ___ | |

Band-Cursor-Fit (M11), H1 „Vib Z & Ref1“, Label 132:

| Spitze (Hz, ungefähr) | Warnkennzeichen? | Cursorgrenzen (Hz) | f_max (Hz) | Dämpfung (Angabe wie PSV) |
|---|---|---|---|---|
| 401,6 | | | | |
| 618,9 | | | | |
| | nein | | | |
| | nein | | | |
| | nein | | | |
| | ja | | | |

Wiederholungsmessung T8 (nur nach eigener Entscheidung):

| Punkt | Eintrag |
|---|---|
| Entscheidung (Zeit, Grund), über Programm oder direkt in PSV | |
| Dateiname(n) `.svd` | |
| gleicher Aufbau / Raster neu abgeglichen bzw. verschoben? | |
| Temperatur Anfang / Ende | |
| Beginn / Ende (Uhrzeit) | |
| Änderungen am Aufbau, Auffälligkeiten | |

## 7 Abbruch / Auffälligkeiten

| Uhrzeit | Kriterium aus dem Ablaufplan | Beobachtung | Gesichert (Dateien, Foto) |
|---|---|---|---|
| | | | |

## 8 Abschluss

| Punkt | Erledigt |
|---|---|
| Erkundungsordner, Durchgangsordner, Konsolenausgaben, Protokoll gesichert und Pfade/Kontonamen geprüft | ☐ |
| Nachweis-.set, Test-.set gesichert | ☐ |
| Ergebnisse 7b und `.svd` aus T8 gesichert | ☐ |
| PSV in sauberem Zustand (keine Messung, kein Dialog) | ☐ |
| Ende (Uhrzeit) | |
| Was ich als „am Gerät bestätigt“ gelten lasse (je Schritt): | |
| Offene Punkte / Fragen für `/laborbuch` und Betreuer | |
