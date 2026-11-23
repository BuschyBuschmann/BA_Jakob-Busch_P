# 2026-11-23 – Messrechner-Termin: Installation, COM-Erkundung, Nur-Lesen, Trockenläufe

**Art:** Hardwaretest
**Paket/Bezug:** Ablaufplan Messrechner-Termin (freigegeben 2026-11-21); Prüfanleitungen Auswerten, Animation, Abgleich; Versuchsordner [`../versuche/2026-11-23_messrechner/`](../versuche/2026-11-23_messrechner/README.md); Erkundung [`erkundung_BEOWOLF_2026-11-23_154125`](../versuche/erkundung/erkundung_BEOWOLF_2026-11-23_154125/zusammenfassung.md); R-001, R-003a/b, R-010 ff., R-071
**Commit:** 16da17a (Repository-Stand am Termin); Software 0.2.0, Build `cebac63e5e9c25d66a76e3d87b073a64bbf1e177` (`git_dirty` false)
**Beteiligt:** Jakob Busch am Messrechner BEOWOLF (Windows 10, PSV 10.4.0.1); Anleitung und Auswertung live durch den Orchestrator

## Ziel
Software 0.2.0 installieren und gegen PSV 10.4 über COM prüfen (Erkundung, Nur-Lesen, Trockenlauf), Auswertung und Animation am Messrechner messen; keine echte Messung.

## Vorgehen
1. **A0:** Stufe 0 der Erkundung (14:34) ohne laufendes PSV; Registry: `Psv.AcquisitionInstance`, `PSV.Application`, `Psv.PresentationInstance` → `C:\Program Files\Polytec\PSV 10.4\PSV.exe`.
2. **A1:** Installation aus Wheelhouse (offline) in `D:\Messdaten\DAL\BA Jakob Busch\PyCharmProject\.venv` (Python 3.11.9). Eine zweite venv `BA Jakob Busch\.venv` (nur comtypes 1.4.17, pywin32 312) blieb unverändert. Wheel-SHA-256 `C193CAA7…687960D` geprüft.
3. PSV über „PSV 10.4 Datenerfassung“ gestartet: Dialog „Es wurden keine Messköpfe gefunden“. Stufe 1b (PolyFile, Kopie von `20261012_ref_Mitte.svd`, 14:43) und Stufe 1 (14:45) liefen in diesem Zustand; „Abbrechen“ im Dialog schloss PSV vollständig.
4. Animation M1–M6 (`animation_messen.py`, lokal, 105 Hz) und M7 (Sichtprüfung), Auswerten W1/W2.
5. Messköpfe wurden angeschlossen, Rechner neu gestartet; PSV lief danach mit `/Acquisition /RestartByRestartManager:…` (von Windows wieder geöffnet), eine Instanz.
6. **B1** Erkundung Stufe 1 (15:41), **B2** Konfiguration `konfig_termin.json`, **T0** Selbsttest, **T1** Oberfläche „Nur lesen“.
7. **B3** in einer privaten Kopie des PSV-Projekts: Test-Einstellungsdatei `test_5000Hz.set` angelegt, Rückprobe.
8. **T2** und Zusatztests (Test 1–3) als Trockenläufe über die Oberfläche; **Test 7** Abschluss.

## Ergebnis

| Schritt | Ergebnis | Bestätigt |
|---|---|---|
| A0 | Registrierung auf PSV 10.4; Stufe 0 alle 7 Prüfpunkte ok | ja |
| A1 (N1–N7) | 0.2.0 installiert (ersetzt 0.1.0), Build cebac63, numpy 2.4.6, PySide6 6.11.3, pywin32 312; matplotlibrc = mitgelieferte Datei, `figure.dpi` 100; erster Import Schriftcache 1,93 s; Oberfläche startet, Beispieldatei (Kopie) lädt (135 Punkte, 1600 Linien, Δf 0,625 Hz, komplex 7, Ref1 [N], Ref2 [m/s²]), Prüfung „1 Warnung, 1 Hinweis, 7 nicht prüfbar, 36 ok“ | ja |
| Ohne Messköpfe | `IsRunning=False`, COM im Erfassungsmodus nicht erreichbar; „Abbrechen“ schließt PSV; Stufe 1b: Datei über COM geöffnet (10.4.0.1), 2 Domänen, 12 Kanäle, `GetData` 1600 Werte; `AcqBoardName`/`GeneratorName` liefern `0x80004001` | – |
| B1 | alle Prüfpunkte ok: verbunden, Version 10.4.0.1, Mode 1, State 0, GeneratorsOn False, FrontEnd 124, ScanHeadType 23, 1 Vibrometer, 153 Messpunkte, 3 3D-Abgleiche, PositionDevice False, DigitalPorts True, `FftAcqPropertiesValidator` vorhanden | – |
| B2/T0 | `konfig_termin.json` = Vorlage (SHA-256 `db98f78e…5dba`); Selbsttest bestanden | – |
| **T1** Nur lesen | 318 Zugriffe, keine Verweigerung; Köpfe PSV-I-680/690/690 (SN 360783/360784/360785), Erfassungskarte FW 1.0302, Frontend FW 2.50; Generator aus, Amplitude 1 V | **bestanden** |
| B3 | `test_5000Hz.set` (SHA-256 `c6115fd5…05a8`): FFT 5 kHz (0–5 kHz), 400 Linien, Mittelung komplex 3, Rechteck, Trigger aus, Generator aus, 153 Punkte; Ref1 Beschleunigung, IEPE, AC, 1 V, „Inv.“ angehakt; Rückprobe ok | ja |
| **T2** Trockenlauf | 5600 Hz: von PSV still nicht übernommen (zurückgelesen 5000 Hz, zwei Versuche); 4000 Hz: PSV „Ungültiger Wert“ (HRESULT −2147352567); 6250 Hz + Mittelung 5: fertig, Werte in PSV gleich, **„Bis“ blieb 5 kHz** | **bestanden mit Befund** („Bis“ wird nicht gesetzt) |
| Test 1 | Linien 800, Pausenpunkt hält an, Mittelung Magnitude 10: in PSV wie gesetzt; drei Fehlversuche, solange der Einstellungsdialog in PSV offen war („Einstellungen … gesperrt“) | **bestanden** |
| Test 2 | Abgleich gelesen (3D-Qualität Index 0: 1,07·10⁻¹⁰ m; Index 1: 1,499 mm; Index 2: 1,527 mm; Soll 1,5 mm; 2D-Index 0 Scankopfabstand 1,0 m). Testgrenze 1,5 mm: „warnen“ → Warnung, Durchgang läuft; „verweigern“ → Eintrag abgelehnt, Durchgang angehalten | **bestanden** |
| Test 3 | „Messen freischalten“ ohne Verbindung/Trockenlauf gesperrt; nach Trockenlauf Startdialog mit 153 Punkten, Generator „aus (übernommen)“, „Messung starten“ ohne Eingabe `MESSEN` grau; abgebrochen | **bestanden** |
| Test 7 | PSV-Ausgangsstand zurückgeladen | **bestanden** |
| Animation M1–M6 | Bild voll 126 ms, vereinfacht 98 ms, Drehschritt voll 277 ms; effektiv 5,0 / 9,9 / 10,0 Bilder/s bei Soll 5 / 10 / 20, bei Soll 20 „langsam“ nicht gemeldet; Phasenregler 128 ms (max 1206 ms); Daten kalt/warm 241/17 ms; PNG 0,69 s, PDF 0,64 s (max 3,4 s) | – |
| Animation M7 | ruckelt leicht; M12-Kasten und Farbskala lesbar; Punktnummern überlappen Marker; x-Achsenticks und y-Beschriftung überlappen | **UI-38 nicht bestanden** |
| W1/W2 | `fertig()` max 18 ms, Paar kalt/warm 0,12/0,11 s, Lesen 0,14 s, `lese_job` 0,54 s, Spawn 0,28 s, Plausibilitätsprüfung 6,3 s; kein hängender Prozess; Reiterwechsel beim Laden sofort | bestanden |

Rohdaten und Protokolle: [`../versuche/2026-11-23_messrechner/`](../versuche/2026-11-23_messrechner/README.md).

## Verifikation
Jeder bestandene Hardwaretest wurde von Jakob am Gerät bestätigt; Werte stammen aus Terminal-Ausgaben, Screenshots und den Messprotokollen der Durchgänge.

## Probleme und verworfene Ansätze
- Messköpfe zunächst nicht angeschlossen; Abhilfe Neustart nach Anschluss.
- Terminal-Variablen gingen bei neuen Tabs bzw. nach Neustart verloren (Pfad fiel auf `D:\vorlagen`); versehentlich eingefügte Ausgabe brachte PowerShell in den Fortsetzungsmodus. Keine Auswirkung auf Daten.
- Die erste Test-.set trug einen Namen mit Umlaut und irreführendem Wortlaut; Kopie als `test_5000Hz.set` angelegt.
- Nachweis-.set (U3 2-4) entsteht über die Oberfläche nicht.

## Offene Punkte
- Software: Bandbreite nur in PSV-Stufen zulassen und „Von/Bis“ mitsetzen (vor jeder echten Messung); Abgleich-Warnung sichtbarer, Dezimalkomma und Wortlaut in Meldungen; Animation flüssiger, Punktnummern, Achsenticks, „langsam“ bei 20 Bildern/s; Plausibilitätsprüfung 6,3 s; Versionszähler zählt Fehlversuche.
- Fragen an Daniel: Bedeutung 3D-Abgleich Index 0 (≈ 0) und Index 2 (1,527 mm > 1,5 mm), sinnvolle Grenzwerte; „Inv.“ bei Ref1 (Polarität, M8).
- Nicht durchgeführt: echte Messungen T4–T6, Prüfdateien R/A/B, Anregung D1–D3, W3–W10, Remotedesktop, X1, B5, AV.

## Thesis-Bezug
4.1 Analyse der COM-Schnittstelle; 4.2 Ansteuerung und Warteschlange; 5.3 Erprobung am Messrechner; 5.4 Fehler, Grenzen und Unsicherheiten.
