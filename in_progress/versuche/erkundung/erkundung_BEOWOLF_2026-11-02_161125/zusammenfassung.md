# Erkundung BEOWOLF (2026-11-02T16:11:25+01:00)

- Lauf: **vollstaendig**
- Skript 0.1.0 (SHA-256 a90d45f135fcfe2594f195191fc2ba48cb189e4a8e42431bc23ffa1616a148d7)
- Stufen: 0, 1, 1b; Zeitbedarf der Prüfpunkte: 1.2 s
- Alle Prüfpunkte gelten als **am Gerät unbestätigt**, bis der Nutzer das Ergebnis bestätigt hat.

## Prüfpunkte

| ID | Stufe | Status | Dauer s | Kernwert | Auffälligkeiten |
|---|---|---|---|---|---|
| P1-1-umgebung | 0 | ok | 0.06 | Windows 10, Python 3.11.9 (64 Bit) |  |
| P1-4-pywin32 | 0 | ok | 0.02 | pywin32 importierbar, Version 312 |  |
| P1-2-registry | 0 | ok | 0.00 | 2 von 5 ProgIDs registriert |  |
| P1-2-dateien | 0 | ok | 0.02 | 4 Serverdatei(en) geprüft |  |
| P1-4-typelibs-registry | 0 | ok | 0.19 | 186 Polytec-Typbibliothek(en) von 946 gesichtet |  |
| P1-3-verzeichnisse | 0 | ok | 0.03 | 4 Verzeichnis(se) vorhanden |  |
| P1-5-prozess | 0 | ok | 0.17 | 0 passende Prozesse |  |
| P1-5-verbinden | 1 | uebersprungen | 0.00 |  | Sperre: Stufe 0 hat keinen laufenden PSV-Prozess gefunden (oder die Prozessliste war nicht lesbar). Das Objekt PSV.AcquisitionInstance wird deshalb nicht angelegt, weil COM bei einer als Server registrierten PSV-EXE diese beim Anlegen selbst starten könnte. PSV im Erfassungsmodus starten und erneut ausführen, oder --start-psv mit Bestätigung verwenden. |
| P1-5-application | 1 | uebersprungen | 0.00 |  | Voraussetzung fehlt (P1-5-verbinden) |
| P1-6-zustand | 1 | uebersprungen | 0.00 |  | Voraussetzung fehlt (P1-5-application: Acquisition nicht erreichbar) |
| P1-6-eigenschaften | 1 | uebersprungen | 0.00 |  | Voraussetzung fehlt (P1-5-application: Acquisition nicht erreichbar) |
| P1-6-hardware | 1 | uebersprungen | 0.00 |  | Voraussetzung fehlt (P1-5-application: Acquisition nicht erreichbar) |
| P1-6-scankopf | 1 | uebersprungen | 0.00 |  | Voraussetzung fehlt (P1-5-application: Acquisition nicht erreichbar) |
| P1-6-vibrometer | 1 | uebersprungen | 0.00 |  | Voraussetzung fehlt (P1-5-application: Acquisition nicht erreichbar) |
| P1-6-messpunkte | 1 | uebersprungen | 0.00 |  | Voraussetzung fehlt (P1-5-application: Acquisition nicht erreichbar) |
| P1-6-abgleich | 1 | uebersprungen | 0.00 |  | Voraussetzung fehlt (P1-5-application: Acquisition nicht erreichbar) |
| P3-2-existenz | 1 | uebersprungen | 0.00 |  | Voraussetzung fehlt (P1-5-application: Acquisition nicht erreichbar) |
| P1-4-typelibs-com | 1 | ok | 0.16 | 93 Polytec-Typbibliotheken, 0 abweichende Konstanten | Keine win32com-Konstanten verfügbar. Die Ursache wurde nicht geprüft; der Vergleich mit I5 Abschnitt 8 ist damit nicht möglich (das Skript erzeugt keine Typbibliotheks-Wrapper). |
| P1-10-oeffnen | 1b | fehler | 0.38 | geöffnet, Programmversion '10.4.0.1' | AcqBoardName: com_error: (-2147352567, 'Ausnahmefehler aufgetreten.', (0, None, None, None, 0, -2147467263), None); GeneratorName: com_error: (-2147352567, 'Ausnahmefehler aufgetreten.', (0, None, None, None, 0, -2147467263), None) |
| P1-10-struktur | 1b | ok | 0.11 | 2 Domäne(n), 12 Kanäle in der gewählten Domäne |  |
| P1-10-daten | 1b | ok | 0.02 | GetData-Länge 1600, MaxCount 1600 |  |
| P1-10-schliessen | 1b | ok | 0.02 | geschlossen |  |

## Abweichungen von der Erwartung (COM-Referenz I5)

Keine festgestellt (soweit die Prüfpunkte gelaufen sind).

## Offene Fragen und der Prüfpunkt, der sie beantworten kann

| Frage | Prüfpunkt | Lauf des Prüfpunkts (nicht die Antwort) |
|---|---|---|
| Kehrt GetApplication(False) bei laufender Instanz ohne Start zurück? | P1-5-verbinden | uebersprungen |
| Bitness und Servertyp (LocalServer32/InprocServer32) der Polytec-Server | P1-2-registry | ok |
| Ist FftAcqPropertiesValidator in dieser Version vorhanden? | P1-6-eigenschaften | uebersprungen |
| Sind Infos.Hardware und Alignments3D im Erfassungsmodus lesbar? | P1-6-hardware | uebersprungen |
| Indexbasis und Label/Index bei MeasPoints.Item | P1-6-messpunkte | uebersprungen |
| Liefert CoordXYZ (ByRef) in pywin32 ein Tupel? | P1-6-messpunkte | uebersprungen |
| Frequenzachse: GetMidX(i) gegen k*df (KONVENTIONEN) | P1-10-daten | ok |
| Form der HRESULT/excepinfo-Angaben bei COM-Fehlern | P1-6-zustand | uebersprungen |

Die Werte stehen in `bericht.json`; das Skript bewertet sie nicht. Beobachtungen am Gerät (Dialoge, Laser, Spiegel) bitte separat notieren.
