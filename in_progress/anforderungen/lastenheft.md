# Lastenheft – Softwarepaket zur Automatisierung von Strukturtests mit dem PSV

**Stand:** Entwurf vom 2026-10-26 · **Status:** zur Abstimmung mit dem Betreuer

**Quellen (Kürzel):**
- **A**: Ausschreibung (`Input/Softwarepaket für Luft- und Raumfahrt_Daniel.pdf`)
- **E**: Erwartungsmanagement (`in_progress/planung/erwartungsmanagement.md`, Antworten des Nutzers vom 2026-10-23)
- **N**: Entscheidung Nutzer vom 2026-10-26 (Vorstellung zu Schritt 1 und 2, Interview)
- **K**: `KONVENTIONEN.md` (vom Nutzer freigegeben)

**Priorität:** Muss (Kern der Arbeit) · Soll (wichtig) · Kann (falls Zeit bleibt).
**Status:** offen · abgestimmt · gestrichen.

Technischer Hintergrund zur Machbarkeit (keine Anforderungsquelle):
`in_progress/analysen/2026-10-23_I5_com-referenz.md`, Abschnitte 3 und 9.1.

---

## 1 Gerätesteuerung über die COM-Schnittstelle

| ID | Anforderung | Priorität | Quelle | Akzeptanzkriterium | Status |
|---|---|---|---|---|---|
| R-001 | Die Software steuert die PSV-Software über die COM-Schnittstelle: Verbindung herstellen, Einstellungen laden bzw. setzen, Scan starten, Fortschritt überwachen, Messdatei speichern. | Muss | A, N | Am Messrechner führt die Software eine Messung mit vorgegebener Einstellung aus; die Messdatei liegt danach am vorgegebenen Pfad. Derselbe Ablauf läuft automatisiert gegen den Simulator (siehe R-061). | offen |

## 2 Mess-Warteschlange (Schritt 1)

| ID | Anforderung | Priorität | Quelle | Akzeptanzkriterium | Status |
|---|---|---|---|---|---|
| R-010 | Mehrere Messungen lassen sich in einer Warteschlange anlegen und laufen nacheinander automatisch ab. | Muss | N | Eine Warteschlange mit mindestens drei Messungen läuft ohne Eingriff vollständig durch; je Messung entsteht eine Messdatei. | offen |
| R-011 | Eine Messung ist definiert durch eine in PSV vorbereitete Einstellungsdatei als Basis, optional mit einzelnen geänderten Parametern. | Muss | N | Eine Messung nur mit Einstellungsdatei und eine Messung mit Einstellungsdatei plus geändertem Parameter laufen; die geänderten Parameter stehen im Messprotokoll (R-020). Welche Parameter änderbar sind: offene Frage O3. | offen |
| R-012 | Messungen lassen sich in die Warteschlange einfügen (an beliebiger Position). | Muss | N | Nach dem Einfügen steht die Messung an der gewählten Position und wird dort ausgeführt. | offen |
| R-013 | Noch nicht gestartete Messungen lassen sich aus der Warteschlange entfernen. | Muss | N | Eine entfernte Messung wird nicht ausgeführt; die übrigen laufen unverändert. | offen |
| R-014 | Noch nicht gestartete Messungen lassen sich bearbeiten. | Muss | N | Eine geänderte Messung wird mit den geänderten Werten ausgeführt; laufende und abgeschlossene Messungen sind nicht bearbeitbar. | offen |
| R-015 | Die Reihenfolge noch nicht gestarteter Messungen lässt sich ändern. | Muss | N | Nach dem Umsortieren laufen die Messungen in der neuen Reihenfolge. | offen |
| R-016 | Einfügen, Entfernen, Bearbeiten und Umsortieren (R-012 bis R-015) sind auch während eines laufenden Durchgangs möglich, für alle noch nicht gestarteten Messungen. | Muss | N | Während eine Messung läuft, wird eine wartende Messung geändert und eine neue eingefügt; beide Änderungen werden im selben Durchgang wirksam, die laufende Messung bleibt unbeeinflusst. | offen |
| R-017 | Zwischen zwei Messungen lassen sich Pausenpunkte setzen (z. B. für einen Umbau am Versuchsaufbau); die Warteschlange läuft erst nach Bestätigung durch den Nutzer weiter. | Muss | N | Ein Pausenpunkt hält die Warteschlange an; ohne Bestätigung startet keine weitere Messung, nach Bestätigung läuft sie weiter. | offen |
| R-018 | Ein Durchgang lässt sich jederzeit pausieren, fortsetzen und abbrechen. | Muss | N | Pausieren: nach der laufenden Messung startet keine weitere, bis fortgesetzt wird. Abbrechen: der Durchgang endet, der Zustand jeder Messung ist im Protokoll nachvollziehbar. Verhalten der gerade laufenden Messung beim Abbrechen: offene Frage O1. | offen |
| R-019 | Verhalten bei einer fehlgeschlagenen Messung (z. B. Fehlermeldung der PSV-Software, Zeitüberschreitung). | – | N | **Mit dem Betreuer zu klären (O1).** | offen |

## 3 Datenhaltung und Dokumentation

| ID | Anforderung | Priorität | Quelle | Akzeptanzkriterium | Status |
|---|---|---|---|---|---|
| R-020 | Zu jeder Messung wird automatisch ein Messprotokoll erstellt: Einstellungen (wie von der PSV-Software übernommen), geänderte Parameter, Version der PSV-Software und des eigenen Pakets, Zeitstempel, Status, Pfad der Messdatei. | Muss | E (U3), N | Nach einem Durchgang existiert zu jeder Messung ein Protokoll mit allen genannten Angaben; ein Protokoll lässt sich einer Messdatei eindeutig zuordnen. | offen |
| R-021 | Eine Warteschlange lässt sich als Datei speichern und später wieder laden. | Soll | N | Eine gespeicherte und neu geladene Warteschlange enthält dieselben Messungen in derselben Reihenfolge mit denselben Einstellungen. | offen |
| R-022 | Die Messdaten werden aus den Messdateien nach Python übernommen. | Muss | A, E (U4) | Spektren einer Messdatei liegen in Python mit Frequenzachse und Einheiten vor und stimmen mit der Anzeige in der PSV-Software überein. | offen |

## 4 Oberfläche

| ID | Anforderung | Priorität | Quelle | Akzeptanzkriterium | Status |
|---|---|---|---|---|---|
| R-030 | Eine grafische Oberfläche ermöglicht die Bedienung der Warteschlange (R-010 bis R-018, R-021). | Muss | N, E (U5) | Alle genannten Funktionen sind über die Oberfläche bedienbar, ohne Skript oder Kommandozeile. | offen |
| R-031 | Die Oberfläche zeigt je Messung den Status (wartend, läuft, fertig, Fehler) und den Fortschritt der laufenden Messung. | Muss | N | Statuswechsel einer Messung erscheinen in der Oberfläche; während eines Scans ist der Fortschritt sichtbar. | offen |

## 5 KI-Assistent

| ID | Anforderung | Priorität | Quelle | Akzeptanzkriterium | Status |
|---|---|---|---|---|---|
| R-040 | Ein KI-Assistent kann aus einer Beschreibung in Alltagssprache eine Warteschlange erstellen. | Kann | N | Aus einer Beschreibung entsteht ein Vorschlag für eine Warteschlange. *Vorschlag:* Einträge werden erst nach Bestätigung durch den Nutzer übernommen und durchlaufen dieselbe Prüfung wie manuell angelegte Messungen. Rahmenbedingungen: offene Frage O2. | offen |

## 6 Auswertung (Schritt 2)

| ID | Anforderung | Priorität | Quelle | Akzeptanzkriterium | Status |
|---|---|---|---|---|---|
| R-050 | Spektren je Messpunkt (Komponenten x/y/z bzw. 3D) und das gemittelte Spektrum werden dargestellt. | Muss | A, N | Für eine Messdatei werden die Spektren dargestellt; Werte stimmen mit der PSV-Software überein. | offen |
| R-051 | Übertragungsfunktionen (H1/H2) und Kohärenz werden dargestellt, sofern die Messung einen aktiven Referenzkanal hatte. | Muss | A, N | Für eine Messung mit Referenzkanal werden H1, H2 und Kohärenz dargestellt; Werte stimmen mit der PSV-Software überein. Einheit hängt von der Referenz ab (O4). | offen |
| R-052 | Betriebsschwingformen werden bei gewählter Frequenz auf der Messgeometrie dargestellt. | Muss | A, N | Bei gewählter Frequenz wird die Schwingform auf der Geometrie dargestellt; ohne Referenz oder Trigger wird nur der Betrag gezeigt und das kenntlich gemacht. | offen |
| R-053 | Peak-Suche mit Resonanzfrequenz und Dämpfungsschätzung (−3-dB-Breite) sowie Frequenzbänder mit RMS-Werten. | Muss | A, N | Für eine Messdatei werden Peaks mit Frequenz und Dämpfungsschätzung sowie Band-RMS-Werte ausgegeben; Werte stimmen mit der PSV-Software bzw. mit analytischen Referenzfällen überein. | offen |
| R-054 | Weitergehende Auswertung (z. B. Plausibilitätsprüfungen, Vergleich von Messungen, Modalanalyse). | gestuft | E (U6) | Umfang wird am Entscheidungspunkt nach der Machbarkeitsphase festgelegt. | offen |

## 7 Qualität und Rahmen

| ID | Anforderung | Priorität | Quelle | Akzeptanzkriterium | Status |
|---|---|---|---|---|---|
| R-060 | Die Software ist in Python 3.11 umgesetzt. | Muss | N (2026-10-21), K | Projekt läuft mit Python 3.11; `requires-python = ">=3.11,<3.12"`. | offen |
| R-061 | Die Software ist ohne Messgerät testbar (Simulator der COM-Schnittstelle). | Muss | K | Alle Funktionen außer dem Gerätezugriff laufen in automatisierten Tests gegen den Simulator. | offen |
| R-062 | Die Prüfungen aus `KONVENTIONEN.md` sind erfüllt (Stil, Typprüfung, Tests mit mindestens 90 % Abdeckung). | Muss | K | Die Standard-Prüfung läuft fehlerfrei. | offen |

## 8 Nicht Teil der Arbeit

Noch nicht festgelegt; mit dem Betreuer zu klären (Erwartungsmanagement F19).

## 9 Offene Fragen

| Nr. | Frage | Auswirkung | Bezug |
|---|---|---|---|
| **O1** | **WICHTIG – mit dem Betreuer abzuklären:** Was soll passieren, wenn eine Messung fehlschlägt (Fehlermeldung von PSV, Zeitüberschreitung)? Pausieren und nachfragen, überspringen, ganz abbrechen oder einstellbar? Was passiert mit der gerade laufenden Messung beim Abbrechen? | Kern der Ablaufsteuerung und des unbeaufsichtigten Betriebs | R-018, R-019 |
| O2 | Hat der Messrechner Internetzugang, und welcher KI-Dienst darf genutzt werden (Datenschutz, Institutsvorgaben)? | Machbarkeit des KI-Assistenten | R-040 |
| O3 | Welche Parameter sollen je Messung gegenüber der Einstellungsdatei änderbar sein (z. B. Bandbreite, Linien, Mittelung, Anregung)? | Umfang von R-011 und der Oberfläche | R-011 |
| O4 | Wird die Anregungskraft gemessen (Kraftsensor, Impulshammer)? | Einheit und Aussagekraft der Übertragungsfunktionen | R-051, Erwartungsmanagement F10 |
| O5 | Wie sollen Messdateien und Protokolle benannt und abgelegt werden? | Datenhaltung, Wiederfinden | R-020 |
| O6 | Darf Python 3.11 mit pywin32 auf dem Messrechner installiert werden? | Voraussetzung für R-001 am Gerät | Erwartungsmanagement F4 |

## Änderungsprotokoll

| Datum | Änderung | Quelle |
|---|---|---|
| 2026-10-26 | Erstfassung (R-001 bis R-062, O1 bis O6) | A, E, N, K |
