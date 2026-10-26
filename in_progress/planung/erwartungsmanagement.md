# Erwartungsmanagement – Bachelorarbeit

**Thema (laut Ausschreibung):** Entwicklung eines Softwarepakets zur Automatisierung von
Luft- und Raumfahrt-Strukturtests in Python
**Verfasser:** Jakob Busch · **Betreuer:** Daniel Alboldt · **Institut:** Strukturmechanik
und Leichtbau (SLA), RWTH Aachen
**Stand:** Entwurf vom 2026-10-23, ergänzt am 2026-10-26 (Vorstellung Warteschlange, Lastenheft), zur gemeinsamen Abstimmung

> Zweck: Wir gehen das Dokument im Termin Punkt für Punkt durch. In der Spalte
> „Abgestimmt“ wird bestätigt (✔), geändert (✎) oder offen gelassen. Fragen an den
> Betreuer sind in Abschnitt 9 gesammelt und in den Abschnitten als **F-Nr.**
> verlinkt.

---

## 1. Ziel und Schwerpunkt

| Punkt | Inhalt | Abgestimmt |
|---|---|---|
| Ziel (Ausschreibung) | Vereinfachung und Beschleunigung reproduzierbarer Strukturtests durch ein Python-Softwarepaket, das ein 3D-Laser-Doppler-Vibrometer (Polytec PSV) über die vorhandene COM-Schnittstelle ansteuert und die aufgenommenen Daten auswertet und visualisiert | |
| Schwerpunkt | **Automatisierung des Messablaufs** steht an erster Stelle; die Auswertung baut darauf auf | |
| Kernfragestellung (Vorschlag) | Wie lässt sich der Messablauf mit dem PSV-System über die COM-Schnittstelle so automatisieren, dass Strukturtests reproduzierbar, nachvollziehbar dokumentiert und schneller durchführbar sind? | |

## 2. Umfang

| Nr. | Inhalt | Einordnung | Abgestimmt |
|---|---|---|---|
| U1 | Einarbeitung in die COM-Schnittstelle der PSV-Software | Muss | |
| U2 | Python-Paket (Python 3.11), das den Messablauf automatisiert: Verbindung zur PSV-Software, Einstellungen laden bzw. setzen, Scan starten und überwachen, Messdaten speichern | Muss | |
| U2a | **Mess-Warteschlange:** mehrere Messungen nacheinander automatisch; Messungen einfügen, entfernen, noch nicht gelaufene bearbeiten, Reihenfolge ändern – auch während des Laufs; Pausenpunkte für Umbauten (Lastenheft R-010 bis R-018) | Muss | |
| U2b | KI-Assistent, der Warteschlangen aus einer Beschreibung erstellen kann (R-040) | Kann | |
| U3 | Nachvollziehbare Dokumentation jeder Messung (Einstellungen, Softwareversion, Messdaten), damit Versuche reproduzierbar sind | Muss | |
| U4 | Übernahme der Messdaten nach Python und grundlegende Auswertung und Visualisierung | Muss | |
| U5 | Einfache grafische Oberfläche zur Bedienung der Mess-Warteschlange | **Muss** (geändert 2026-10-26, siehe Lastenheft R-030) | |
| U6 | Weitergehende Auswertung, z. B. automatische Plausibilitätsprüfungen, Vergleich von Messungen, Modalanalyse (Eigenfrequenzen, Dämpfung, Eigenformen) | **gestuft:** Umfang wird am Entscheidungspunkt nach Phase 1 festgelegt, abhängig vom Aufwand der Schnittstelle | |
| U7 | Ansteuerung weiteren Versuchsequipments (z. B. Signalgenerator, Positioniereinheit) | offen, **F6** | |
| U8 | Ausdrücklich nicht Teil der Arbeit | offen, im Termin festlegen | |

## 3. Vorgehen (Vorschlag)

| Phase | Inhalt | Ergebnis | Abgestimmt |
|---|---|---|---|
| 1 Einarbeitung und Machbarkeit | PSV-System und Laborbetrieb kennenlernen; Zugriff aus Python auf die COM-Schnittstelle am Messrechner nachweisen; Anforderungen festhalten | lauffähiger Prototyp „verbinden – einstellen – scannen – speichern“, Lastenheft | |
| **Entscheidungspunkt** | Gemeinsame Bewertung des Aufwands der Schnittstelle | Festlegung des Auswerteumfangs (U6) | |
| 2 Umsetzung | Softwarepaket mit Tests (auch ohne Gerät über einen Simulator), Datenübernahme, Auswertung, ggf. Oberfläche | getestetes Softwarepaket | |
| 3 Versuche und Validierung | Strukturtests im Labor mit der Software, Prüfung der Reproduzierbarkeit | Versuchsprotokolle und Ergebnisse | |
| 4 Ausarbeitung | Thesis nach SLA-Vorlage | Bachelorarbeit | |

Die Dokumentation (Laborbuch, Entscheidungen, Versuche) läuft über alle Phasen mit.

## 4. Erwartete Ergebnisse

| Ergebnis | Beschreibung | Abgestimmt |
|---|---|---|
| Softwarepaket | Python 3.11, getestet und dokumentiert; Tests auch ohne Gerät über einen Simulator | |
| Nachweis im Labor | Einsatz des Pakets an realen Strukturtests am PSV-System | |
| Thesis | Deutsch, LaTeX, SLA-Vorlage | |
| Vortrag | Ob und wann ein Zwischen- oder Abschlussvortrag vorgesehen ist: **F17** | |
| Weiterverwendung | Die Software soll nach der Arbeit im Institut weiter genutzt werden können: **F18** | |

## 5. Zeitrahmen

Die Arbeit ist noch nicht angemeldet. Beginn, Bearbeitungszeit und Abgabetermin werden
im Termin abgestimmt: **F1**. Danach wird ein Zeitplan mit Meilensteinen und Puffer
erstellt.

## 6. Betreuung und Zusammenarbeit

| Punkt | Wunsch des Verfassers | Abgestimmt |
|---|---|---|
| Termine | Regelmäßiger Termin mit kurzer Agenda; Rhythmus: **F2** | |
| Feedback | Frühes Feedback zu Gliederung und ersten Kapitelentwürfen vor der Abgabe | |
| Bewertung | Bewertungskriterien früh kennen: **F3** | |
| Einarbeitung | Unterstützung bei der Einarbeitung in das PSV-System und den Laborbetrieb | |
| Kommunikation zwischen den Terminen | Kanal und Reaktionszeit: **F2** | |

## 7. Labor, Software und Daten

| Punkt | Stand | Abgestimmt |
|---|---|---|
| Zugang zum PSV-Messrechner | vorhanden | |
| Fernzugriff auf den Messrechner | möglich | |
| Installation von Python 3.11 und COM-Bibliothek (pywin32) auf dem Messrechner | **geklärt 2026-10-26: darf installiert werden** (F4) | ✔ |
| PSV-Version und lizenzierte Optionen | **F5** | |
| Vorhandene Makros, Referenzmessung, Gerätespezifikation | **F7**, **F8** | |
| Prüfling, Lagerung, Anregung, Kraftmessung | **F9**, **F10** | |
| Ablage von Code und Messdaten | aktuell privates GitHub-Repository; Übergabe an das Institut: **F18** | |

## 8. Umgang mit KI-Werkzeugen

Ich setze KI-Werkzeuge offen und kontrolliert ein:
- **Wofür:** Unterstützung bei der Programmierung und beim Testen, Sichtung und
  Zusammenfassung von Unterlagen und Literatur, Rohfassungen einzelner Textabschnitte,
  die ich selbst überarbeite, sowie Prüfung von Code und Text.
- **Dokumentation:** Jeder Einsatz wird in einem KI-Nutzungsregister festgehalten
  (Abschnitt bzw. Artefakt, Einsatzzweck, Prüfung durch mich). Daraus entsteht die
  KI-Erklärung, die die SLA-Vorlage verlangt.
- **Verantwortung:** Ich prüfe alle Ergebnisse selbst und übernehme die Verantwortung
  für den Inhalt. Quellen werden nur übernommen, wenn ihre Existenz und ihr Inhalt
  geprüft sind.
- **Bitte:** Freigabe dieses Vorgehens bzw. Grenzen des zulässigen Einsatzes: **F11**.

| Abgestimmt | |
|---|---|

## 9. Fragen an den Betreuer

| Nr. | Frage | Auswirkung | Antwort |
|---|---|---|---|
| F1 | Wann wird die Arbeit angemeldet, wie lang ist die Bearbeitungszeit, wann ist die Abgabe? | Zeitplan und Meilensteine | |
| F2 | In welchem Rhythmus treffen wir uns, und wie erreiche ich Sie zwischen den Terminen? | Planung, Feedbackschleifen | |
| F3 | Nach welchen Kriterien wird die Arbeit bewertet? Gibt es ein Bewertungsraster des Instituts? | Schwerpunktsetzung | |
| F4 | Darf auf dem PSV-Messrechner Python 3.11 mit einer COM-Bibliothek (pywin32) installiert werden, oder ist dafür Rücksprache mit Polytec nötig? Alternativ: anderer Rechner? | Architektur, Phase 1 | Ja, darf installiert werden (Termin 2026-10-26) |
| F5 | Welche PSV-Version ist installiert, und welche Optionen sind lizenziert (z. B. Zeitdaten, Signalgenerator, Exportformate)? Ist Polytec File Access installiert? | Datenpfad, eigene Auswertung aus Zeitdaten | |
| F6 | Soll das Paket weiteres Versuchsequipment steuern (Signalgenerator, Positioniereinheit o. Ä.)? | Umfang U7 | |
| F7 | Gibt es vorhandene Makros (z. B. `SettingsandScan.bas`) und eine kleine Referenzmessung (`.svd` mit UFF-Export), die ich nutzen kann? | Tests mit realen Daten | |
| F8 | Gibt es die technische Spezifikation des PSV-QTec-3D (Messbereiche, Rauschen, Bandbreite)? | Versuchsplanung, Grundlagen | |
| F9 | An welchem Prüfling, mit welcher Lagerung und Anregung sollen die Strukturtests laufen, in welchem Frequenzbereich? | Versuche, Validierung | |
| F10 | Wird die Anregungskraft gemessen (Kraftsensor, Impulshammer) oder dient das Generatorsignal als Referenz? | Art der Übertragungsfunktion, Modalanalyse | |
| F11 | Ist der beschriebene KI-Einsatz (Abschnitt 8) zulässig, und wie genau soll er in der KI-Erklärung gekennzeichnet werden? | Arbeitsweise, Erklärung | |
| F12 | Was bedeutet „reproduzierbar“ quantitativ (Toleranzen, Vergleichskriterien), gibt es Normen oder Institutsvorgaben? | Validierung | |
| F13 | Gilt für die Formalien die SLA-LaTeX-Vorlage oder das Dokument „Richtlinien für wissenschaftliches Arbeiten“ (Wirtschaftswissenschaften; widerspricht u. a. bei Zitierweise und Umfang)? | Thesis-Formalien | |
| F14 | Ist die vorliegende LaTeX-Vorlage aktuell? Bitte Logo bzw. Ordner `PICTURES/` bereitstellen. | Thesis-Setup | |
| F15 | Abgabeformalien: Anzahl und Art der Exemplare, ein- oder zweiseitig, digitale Abgabe? | Planung | |
| F16 | Darf die Schrift ISONORM 3098 für Abbildungen verwendet werden (Lizenz)? | Abbildungen | |
| F17 | Ist ein Zwischen- oder Abschlussvortrag vorgesehen? | Planung | |
| F18 | Wo soll die Software nach der Arbeit liegen (z. B. Institutsrepository), und was braucht das Institut für die Weiterverwendung (Dokumentation, Sprache, Übergabe)? | Dokumentation, Übergabe | |
| F19 | Was ist ausdrücklich nicht Teil der Arbeit? | Abgrenzung U8 | |
| **F20** | **WICHTIG:** Was soll passieren, wenn eine Messung der Warteschlange fehlschlägt (Fehlermeldung von PSV, Zeitüberschreitung)? Pausieren und nachfragen, überspringen, abbrechen oder einstellbar? | Kern der Ablaufsteuerung (Lastenheft O1) | |
| F21 | Hat der Messrechner Internetzugang, und welcher KI-Dienst darf für einen KI-Assistenten genutzt werden? | Machbarkeit R-040 | |
