# Lastenheft – Softwarepaket zur Automatisierung von Strukturtests mit dem PSV

**Stand:** Entwurf vom 2026-10-26 · **Status:** zur Abstimmung mit dem Betreuer

**Quellen (Kürzel):**
- **A**: Ausschreibung (`Input/Softwarepaket für Luft- und Raumfahrt_Daniel.pdf`)
- **E**: Erwartungsmanagement (`in_progress/planung/erwartungsmanagement.md`, Antworten des Nutzers vom 2026-10-23)
- **N**: Entscheidung Nutzer vom 2026-10-26 (Vorstellung zu Schritt 1 und 2, Interview)
- **K**: `KONVENTIONEN.md` (vom Nutzer freigegeben)
- **L**: Laborbuch `2026-11-02_messrechner-erster-termin` und Übersicht `in_progress/analysen/2026-11-02_nach-termin_uebersicht.md` (Abschnitt 2b)
- **N3**: Entscheidung Nutzer vom 2026-11-03 (Lastenheft-Ergänzung)
- **B**: Betreuertermin mit Daniel am 2026-11-09 (Laborbuch `2026-11-09_betreuertermin-daniel`, Vorgaben B1–B10)
- **N4**: Entscheidung Nutzer vom 2026-11-09 (Lesart der Vorgaben B1, B3, B5; Priorität aller Vorgaben: Muss)

**Priorität:** Muss (Kern der Arbeit) · Soll (wichtig) · Kann (falls Zeit bleibt).
**Status:** offen · abgestimmt · gestrichen.

Technischer Hintergrund zur Machbarkeit (keine Anforderungsquelle):
`in_progress/analysen/2026-10-23_I5_com-referenz.md`, Abschnitte 3 und 9.1.

---

## 1 Gerätesteuerung über die COM-Schnittstelle

| ID | Anforderung | Priorität | Quelle | Akzeptanzkriterium | Status |
|---|---|---|---|---|---|
| R-001 | Die Software steuert die PSV-Software über die COM-Schnittstelle: Verbindung herstellen, Einstellungen laden bzw. setzen, Scan starten, Fortschritt überwachen, Messdatei speichern. | Muss | A, N | Am Messrechner führt die Software eine Messung mit vorgegebener Einstellung aus; die Messdatei liegt danach am vorgegebenen Pfad. Derselbe Ablauf läuft automatisiert gegen den Simulator (siehe R-061). | offen |
| R-002 | Vor dem Start eines Durchgangs warnt die Software, wenn mehr als ein PSV-Prozess läuft; die Prozess-IDs stehen im Messprotokoll. | Soll | L, N3 | Bei zwei laufenden PSV-Prozessen erscheint vor dem Start eine Warnung und beide PIDs stehen im Protokoll; bei genau einem Prozess erscheint keine Warnung. | offen |
| R-003 | Die Software führt den 2D- und den 3D-Abgleich (Alignment) der PSV über die COM-Schnittstelle aus und schreibt Status und Ergebnis des Abgleichs ins Messprotokoll. | Muss | B (B1), N4 | Am Messrechner wird ein 2D- und ein 3D-Abgleich aus der Software gestartet; das Messprotokoll enthält danach Zeitpunkt, Art und Ergebnis des Abgleichs (welche Ergebniswerte: O9). | aufgeteilt in R-003a bis R-003c (Nutzer, 2026-11-09) |
| R-003a | Die Software liest vor jeder Messung Gültigkeit und Qualität des 3D- und 2D-Abgleichs über COM und schreibt sie ins Messprotokoll; nicht lesbare Werte werden mit Grund als nicht lesbar protokolliert. | Muss | B (B1), N4 | Im Messprotokoll jeder Messung steht der Block `abgleich` mit den gelesenen Werten bzw. „nicht lesbar“ und Grund; am Messrechner stimmen die Werte mit der PSV-Anzeige überein. | offen |
| R-003b | Die Software prüft vor der Messung den Abgleich gegen konfigurierbare Grenzen (Modus aus, warnen oder verweigern). | Muss | B (B1), N4 | Mit Modus „verweigern“ und ungültigem Abgleich startet kein Scan und die Messung endet mit Fehler „Abgleich“; mit „warnen“ erscheint eine Warnung; Grenzwerte: O9. | offen |
| R-003c | Die Software löst den 2D- bzw. 3D-Abgleich in PSV aus. | Muss | B (B1), N4 | offen bis zur Klärung mit dem Betreuer (O9); laut Analyse A1-B13 ist ein COM-Aufruf dafür nicht belegt. | offen |

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
| R-023 | Das Messprotokoll (R-020) enthält ausdrücklich Δf, f_max, Linienzahl und Blockdauer (SampleTime). | Muss | L, N3 | Die vier Angaben stehen mit Einheit in jedem Protokoll. | offen |
| R-024 | Nach jedem Scan wird die Frequenzachse der Messdatei mit der Einstellung abgeglichen; Abweichungen werden gemeldet. | Muss | L, N3 | Linienzahl und Δf der Datei werden mit der Einstellung verglichen; bei Abweichung steht eine Warnung im Protokoll, bei Übereinstimmung der Vermerk „Achse geprüft“. Toleranz für Δf: offene Frage O7. | offen |
| R-025 | Die Software benachrichtigt den Nutzer, wenn eine Messung fertig ist, ein Durchgang abgeschlossen ist, eine Messung fehlschlägt oder abbricht und wenn ein Pausenpunkt erreicht ist; Kanal bevorzugt Webex, alternativ E-Mail. | Muss | B (B3), N4 | In jedem der vier Fälle geht eine Nachricht mit Messungsname, Ereignis und Uhrzeit über den eingestellten Kanal heraus (Kanal und Zugang: O10). | offen |

## 4 Oberfläche

| ID | Anforderung | Priorität | Quelle | Akzeptanzkriterium | Status |
|---|---|---|---|---|---|
| R-030 | Eine grafische Oberfläche ermöglicht die Bedienung der Warteschlange (R-010 bis R-018, R-021). | Muss | N, E (U5) | Alle genannten Funktionen sind über die Oberfläche bedienbar, ohne Skript oder Kommandozeile. | offen |
| R-031 | Die Oberfläche zeigt je Messung den Status (wartend, läuft, fertig, Fehler) und den Fortschritt der laufenden Messung. | Muss | N | Statuswechsel einer Messung erscheinen in der Oberfläche; während eines Scans ist der Fortschritt sichtbar. | offen |
| R-032 | Die Auswertungsoberfläche zeigt das Spektrum direkt an, dazu eine Parameterzeile aus den Einstellungen der Datei. | Soll | L, N3 | Nach dem Öffnen einer Messdatei ist ohne weitere Bedienschritte ein Spektrum sichtbar; die Parameterzeile zeigt mindestens Bandbreite, Linien, Δf, Mittelung und Fenster. Gestaltung über Ablauf C. | offen |

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
| R-054 | Weitergehende Auswertung (z. B. Plausibilitätsprüfungen, Vergleich von Messungen, Modalanalyse). | gestuft | E (U6) | Umfang wird am Entscheidungspunkt nach der Machbarkeitsphase festgelegt. | offen; Vergleich von Messungen als Muss in R-058 (B, 2026-11-09); weitere Verfahren nach Recherche B10 |
| R-055 | Jede Dämpfungsangabe nennt die Bandgrenzen und die Methode (z. B. −3-dB-Breite, Modenfit). | Muss | L, N3 | Zu jedem ausgegebenen ζ stehen untere und obere Bandgrenze in Hz und der Name der Methode. | offen |
| R-056 | Gespeicherte Zeitdaten werden gelesen; Spektren und H1 werden unabhängig von PSV berechnet. | Kann | L, N3 | Für eine Messdatei mit Zeitdaten stimmen die eigenen Spektren bzw. H1 mit PSV überein. Toleranz: offene Frage O8. | offen |
| R-057 | Plausibilitätsprüfung: Masse aus der Massenlinie geschätzt und gegen die gewogene Masse gestellt. | Kann | L, N3 | Geschätzte und gewogene Masse werden gemeinsam mit ihrer Abweichung ausgegeben. Toleranz: offene Frage O8. | offen |
| R-058 | Zwei oder mehr Messungen lassen sich vergleichen; ihre Auswertungen lassen sich nebeneinander darstellen. | Muss | B (B4) | Zwei Messdateien sind gleichzeitig geöffnet; dieselbe Ansicht (z. B. Spektrum oder FRF) erscheint für beide nebeneinander bzw. überlagert und eindeutig beschriftet. | offen |
| R-059 | Der Nutzer kann eigene Diagramme zusammenstellen: frei wählbare Größen, Messpunkte und Messungen in einem Diagramm. | Muss | B (B5), N4 | Aus mindestens zwei Messpunkten oder Messungen entsteht ein gemeinsames Diagramm mit gewählter Größe (z. B. \|H1\| oder Kohärenz) und Legende; es lässt sich als Bild speichern. | offen |
| R-070 | Messwerte lassen sich in ein lokales Koordinatensystem der Messfläche transformieren (Komponente normal zur Oberfläche und tangential, z. B. bei kugelförmigen Formen). | Muss | B (B6) | Für eine Messgeometrie mit gekrümmter Fläche zeigt die Software die Normalkomponente je Punkt; an einem Referenzfall mit bekannter Normale stimmt sie mit dem Sollwert überein (Formen, Normale, Toleranz: O11). | offen |
| R-071 | Betriebsschwingformen lassen sich als Animation darstellen. | Muss | B (B7) | Bei gewählter Frequenz zeigt die Software eine animierte Schwingform auf der Messgeometrie; die Phase der Bewegung entspricht der dargestellten Phase. | offen |
| R-072 | Die Visualisierungen der PSV-Software werden in der Software nachgebildet. | Muss | B (B8) | Für jede Ansicht der Liste aus O12 gibt es eine Entsprechung in der Software. | offen |
| R-073 | Ausschnitte lassen sich einfach darstellen: Achsenbereiche (Frequenz, Betrag, Phase) und Skalierung (linear/logarithmisch) sind direkt einstellbar. | Muss | B (B9) | In jeder Diagrammansicht lassen sich unterer und oberer Achsenwert eingeben und die Skalierung umschalten; die Einstellung bleibt beim Wechsel des Messpunkts erhalten. | offen |

## 7 Qualität und Rahmen

| ID | Anforderung | Priorität | Quelle | Akzeptanzkriterium | Status |
|---|---|---|---|---|---|
| R-060 | Die Software ist in Python 3.11 umgesetzt. | Muss | N (2026-10-21), K | Projekt läuft mit Python 3.11; `requires-python = ">=3.11,<3.12"`. | offen |
| R-061 | Die Software ist ohne Messgerät testbar (Simulator der COM-Schnittstelle). | Muss | K | Alle Funktionen außer dem Gerätezugriff laufen in automatisierten Tests gegen den Simulator. | offen |
| R-062 | Die Prüfungen aus `KONVENTIONEN.md` sind erfüllt (Stil, Typprüfung, Tests mit mindestens 90 % Abdeckung). | Muss | K | Die Standard-Prüfung läuft fehlerfrei. | offen |

## 8 Nicht Teil der Arbeit

Noch nicht festgelegt; mit dem Betreuer zu klären (Erwartungsmanagement F19).

- Bedienung von einem anderen Rechner über eine eigene Netzsteuerung; Fernbedienung erfolgt über Remotedesktop (B, B2).

## 9 Offene Fragen

| Nr. | Frage | Auswirkung | Bezug |
|---|---|---|---|
| **O1** | **WICHTIG – mit dem Betreuer abzuklären:** Was soll passieren, wenn eine Messung fehlschlägt (Fehlermeldung von PSV, Zeitüberschreitung)? Pausieren und nachfragen, überspringen, ganz abbrechen oder einstellbar? Was passiert mit der gerade laufenden Messung beim Abbrechen? | Kern der Ablaufsteuerung und des unbeaufsichtigten Betriebs | R-018, R-019 |
| O2 | Hat der Messrechner Internetzugang, und welcher KI-Dienst darf genutzt werden (Datenschutz, Institutsvorgaben)? **Teilweise beantwortet (L, 02.11.):** Internet vorhanden (Pakete aus dem Internet installiert); zulässiger KI-Dienst offen. | Machbarkeit des KI-Assistenten | R-040 |
| O3 | Welche Parameter sollen je Messung gegenüber der Einstellungsdatei änderbar sein (z. B. Bandbreite, Linien, Mittelung, Anregung)? | Umfang von R-011 und der Oberfläche | R-011 |
| O4 | Wird die Anregungskraft gemessen (Kraftsensor, Impulshammer)? **Beantwortet (L, 02.11.):** ja, Impedanzkopf PCB 288D01, Kraft auf Ref1 (40,31 N/V), Beschleunigung auf Ref2; Polarität offen (M8). | Einheit und Aussagekraft der Übertragungsfunktionen | R-051, Erwartungsmanagement F10 |
| O5 | Wie sollen Messdateien und Protokolle benannt und abgelegt werden? **Teilweise beantwortet (L, K):** Ablage unter `D:\Messdaten\DAL\BA Jakob Busch`, nicht unter `PyCharmProject`; Benennung offen. | Datenhaltung, Wiederfinden | R-020 |
| O6 | Darf Python 3.11 mit pywin32 auf dem Messrechner installiert werden? **Beantwortet (L, 02.11.):** ja, Python 3.11.9 und pywin32 312 installiert, I1–I7 bestanden. | Voraussetzung für R-001 am Gerät | Erwartungsmanagement F4 |
| O7 | Mit welcher Toleranz gilt Δf aus der Datei als gleich der Einstellung? | Prüfkriterium von R-024 | R-024 |
| O8 | Welche Abweichung ist bei R-056 (Spektren/H1 gegen PSV) und R-057 (Masse) zulässig? | Prüfkriterien der Kann-Anforderungen | R-056, R-057 |
| O9 | Fragen A1–A6 an den Betreuer zum Abgleich (Umfang lesen/prüfen/auslösen, Methode, Ergebnis- und Grenzwerte, Bewegung ohne Aufsicht, Verhalten bei ungültigem Abgleich, Protokollierung), Wortlaut in `in_progress/analysen/2026-11-09_A1-B13_alignment-benachrichtigung.md`. Laut Analyse ist das Auslösen per COM nicht belegt; geplant werden zunächst Lesen und Prüfen (Nutzer, 2026-11-09). | Akzeptanzkriterium und Ablauf von R-003 | R-003 |
| O10 | Fragen W1–W8 an den Betreuer zur Benachrichtigung (Kanal, Webex Bot/Webhook und Konto, E-Mail-Server, Datenschutz, Netzfreigabe, Menge, Fehlerfälle, Zustellfehler), Wortlaut in `in_progress/analysen/2026-11-09_A1-B13_alignment-benachrichtigung.md`. | Machbarkeit und Kanal von R-025 | R-025 |
| O11 | Welche Formen für die Transformation (Kugel, Zylinder, Freiform)? Woher kommt die Normale (PSV-Geometrie oder vorgegebene Form)? Welche Toleranz? | Umfang und Prüfkriterium von R-070 | R-070 |
| O12 | Welche PSV-Visualisierungen genau sollen übernommen werden (z. B. Farbdarstellung auf der Geometrie, Kurvenansichten, Mittelwertansicht, Animation)? | Prüfliste von R-072 | R-072 |

## Änderungsprotokoll

| Datum | Änderung | Quelle |
|---|---|---|
| 2026-10-26 | Erstfassung (R-001 bis R-062, O1 bis O6) | A, E, N, K |
| 2026-11-03 | R-002, R-023, R-024, R-032, R-055, R-056, R-057 ergänzt; O2, O5 teilweise und O4, O6 beantwortet; O7, O8 neu | L, N3 |
| 2026-11-09 | R-003, R-025, R-058, R-059, R-070–R-073 ergänzt (Muss); R-054 Status ergänzt; Abgrenzung Netzsteuerung; O9–O12 neu | B, N4 |
| 2026-11-09 | R-003 aufgeteilt in R-003a (lesen), R-003b (prüfen), R-003c (auslösen, offen) | N4, Analyse A1-B13 |
