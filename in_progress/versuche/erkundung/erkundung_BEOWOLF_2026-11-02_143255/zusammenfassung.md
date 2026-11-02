# Erkundung BEOWOLF (2026-11-02T14:32:55+01:00)

- Lauf: **vollstaendig**
- Skript 0.1.0 (SHA-256 a90d45f135fcfe2594f195191fc2ba48cb189e4a8e42431bc23ffa1616a148d7)
- Stufen: 0; Zeitbedarf der Prüfpunkte: 0.6 s
- Alle Prüfpunkte gelten als **am Gerät unbestätigt**, bis der Nutzer das Ergebnis bestätigt hat.

## Prüfpunkte

| ID | Stufe | Status | Dauer s | Kernwert | Auffälligkeiten |
|---|---|---|---|---|---|
| P1-1-umgebung | 0 | ok | 0.00 | Windows 10, Python 3.11.9 (64 Bit) |  |
| P1-4-pywin32 | 0 | ok | 0.00 | pywin32 nicht importierbar | Stufe 1 braucht pywin32; Stufe 0 läuft trotzdem. |
| P1-2-registry | 0 | ok | 0.00 | 2 von 5 ProgIDs registriert |  |
| P1-2-dateien | 0 | ok | 0.02 | 4 Serverdatei(en) geprüft |  |
| P1-4-typelibs-registry | 0 | ok | 0.25 | 186 Polytec-Typbibliothek(en) von 946 gesichtet |  |
| P1-3-verzeichnisse | 0 | ok | 0.08 | 4 Verzeichnis(se) vorhanden |  |
| P1-5-prozess | 0 | ok | 0.27 | 2 passende Prozesse |  |

## Abweichungen von der Erwartung (COM-Referenz I5)

Keine festgestellt (soweit die Prüfpunkte gelaufen sind).

## Offene Fragen und der Prüfpunkt, der sie beantworten kann

| Frage | Prüfpunkt | Lauf des Prüfpunkts (nicht die Antwort) |
|---|---|---|
| Kehrt GetApplication(False) bei laufender Instanz ohne Start zurück? | P1-5-verbinden | nicht ausgeführt |
| Bitness und Servertyp (LocalServer32/InprocServer32) der Polytec-Server | P1-2-registry | ok |
| Ist FftAcqPropertiesValidator in dieser Version vorhanden? | P1-6-eigenschaften | nicht ausgeführt |
| Sind Infos.Hardware und Alignments3D im Erfassungsmodus lesbar? | P1-6-hardware | nicht ausgeführt |
| Indexbasis und Label/Index bei MeasPoints.Item | P1-6-messpunkte | nicht ausgeführt |
| Liefert CoordXYZ (ByRef) in pywin32 ein Tupel? | P1-6-messpunkte | nicht ausgeführt |
| Frequenzachse: GetMidX(i) gegen k*df (KONVENTIONEN) | P1-10-daten | nicht ausgeführt |
| Form der HRESULT/excepinfo-Angaben bei COM-Fehlern | P1-6-zustand | nicht ausgeführt |

Die Werte stehen in `bericht.json`; das Skript bewertet sie nicht. Beobachtungen am Gerät (Dialoge, Laser, Spiegel) bitte separat notieren.
