# Erkundung BEOWOLF (2026-11-23T15:41:25+01:00)

- Lauf: **vollstaendig**
- Skript 0.1.0 (SHA-256 a90d45f135fcfe2594f195191fc2ba48cb189e4a8e42431bc23ffa1616a148d7)
- Stufen: 0, 1; Zeitbedarf der Prüfpunkte: 2.2 s
- Alle Prüfpunkte gelten als **am Gerät unbestätigt**, bis der Nutzer das Ergebnis bestätigt hat.

## Prüfpunkte

| ID | Stufe | Status | Dauer s | Kernwert | Auffälligkeiten |
|---|---|---|---|---|---|
| P1-1-umgebung | 0 | ok | 0.06 | Windows 10, Python 3.11.9 (64 Bit) |  |
| P1-4-pywin32 | 0 | ok | 0.05 | pywin32 importierbar, Version 312 |  |
| P1-2-registry | 0 | ok | 0.00 | 5 von 5 ProgIDs registriert |  |
| P1-2-dateien | 0 | ok | 0.02 | 5 Serverdatei(en) geprüft |  |
| P1-4-typelibs-registry | 0 | ok | 0.22 | 188 Polytec-Typbibliothek(en) von 946 gesichtet |  |
| P1-3-verzeichnisse | 0 | ok | 0.06 | 4 Verzeichnis(se) vorhanden |  |
| P1-5-prozess | 0 | ok | 0.61 | 1 passende Prozesse |  |
| P1-5-verbinden | 1 | ok | 0.05 | verbunden |  |
| P1-5-application | 1 | ok | 0.08 | Version '10.4.0.1', Mode 1 |  |
| P1-6-zustand | 1 | ok | 0.08 | State 0, GeneratorsOn False |  |
| P1-6-eigenschaften | 1 | ok | 0.36 | Gruppen: General, Average, Fft, Channels, Vibrometers, Generators, Trigger, SignalEnhancement, FrontEnd |  |
| P1-6-hardware | 1 | ok | 0.23 | FrontEnd 124 |  |
| P1-6-scankopf | 1 | ok | 0.03 | ScanHeadType 23 |  |
| P1-6-vibrometer | 1 | ok | 0.06 | Vibrometers.Count 1 |  |
| P1-6-messpunkte | 1 | ok | 0.03 | MeasPoints.Count 153 |  |
| P1-6-abgleich | 1 | ok | 0.09 | 3D-Abgleiche: 3 |  |
| P3-2-existenz | 1 | ok | 0.00 | PositionDevice False, DigitalPorts True |  |
| P1-4-typelibs-com | 1 | ok | 0.14 | 94 Polytec-Typbibliotheken, 0 abweichende Konstanten | Keine win32com-Konstanten verfügbar. Die Ursache wurde nicht geprüft; der Vergleich mit I5 Abschnitt 8 ist damit nicht möglich (das Skript erzeugt keine Typbibliotheks-Wrapper). |

## Abweichungen von der Erwartung (COM-Referenz I5)

Keine festgestellt (soweit die Prüfpunkte gelaufen sind).

## Offene Fragen und der Prüfpunkt, der sie beantworten kann

| Frage | Prüfpunkt | Lauf des Prüfpunkts (nicht die Antwort) |
|---|---|---|
| Kehrt GetApplication(False) bei laufender Instanz ohne Start zurück? | P1-5-verbinden | ok |
| Bitness und Servertyp (LocalServer32/InprocServer32) der Polytec-Server | P1-2-registry | ok |
| Ist FftAcqPropertiesValidator in dieser Version vorhanden? | P1-6-eigenschaften | ok |
| Sind Infos.Hardware und Alignments3D im Erfassungsmodus lesbar? | P1-6-hardware | ok |
| Indexbasis und Label/Index bei MeasPoints.Item | P1-6-messpunkte | ok |
| Liefert CoordXYZ (ByRef) in pywin32 ein Tupel? | P1-6-messpunkte | ok |
| Frequenzachse: GetMidX(i) gegen k*df (KONVENTIONEN) | P1-10-daten | nicht ausgeführt |
| Form der HRESULT/excepinfo-Angaben bei COM-Fehlern | P1-6-zustand | ok |

Die Werte stehen in `bericht.json`; das Skript bewertet sie nicht. Beobachtungen am Gerät (Dialoge, Laser, Spiegel) bitte separat notieren.
