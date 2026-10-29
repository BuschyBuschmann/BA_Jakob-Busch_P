# Exposé – Entwurf (im Interview mit Jakob, Stand 2026-10-28)

> Arbeitsstand. Grundlage: Vorgaben des Betreuers in `Input/20260416_Erwartungsmanagement.pdf` (S. 2):
> Titelvorschlag · Kurzfassung (Motivation, Ziel, Lösungsweg) · Gliederung · erste Quellensammlung · Zeitplan.
> Inhalte stammen aus den Antworten des Nutzers; Vorschläge des Orchestrators sind als solche gekennzeichnet.

## Rahmen (nicht Teil des Exposé-Textes)
- Betreuung: Daniel Alboldt (SLA) und Florian (SLA, zweiter Betreuer; Nachname noch eintragen).
- Anmeldung verzögert sich wegen eines Antrags an den Prüfungsausschuss (Stand 2026-10-28).
- Bearbeitungszeit und Abgabetermin hängen vom Ausgang des Antrags ab → Zeitplan relativ in Wochen ab Anmeldung; offener Punkt F1.

## 1 Titel
- Zurückgestellt (Nutzer, 2026-10-29: „Titel lassen wir bitte erstmal weg“). Vorschläge A–C aus dem Interview liegen vor, nicht ausgewählt.

## 2 Kurzfassung
### Rohfassung Fließtext (KI, zu überarbeiten)
<!-- ROHFASSUNG (KI-unterstützt) – vom Verfasser zu überarbeiten -->
<!-- Unterlagen: ausschließlich die Interview-Antworten in den Stichpunkt-Abschnitten darunter (Motivation, Ziel, Lösungsweg); Stil nach Analysebericht I3 / KONVENTIONEN.md. Keine Literaturhinweise (Kurzfassung ohne Zitate). -->

Am Institut für Strukturmechanik und Leichtbau werden Strukturtests an Luft- und Raumfahrtstrukturen mit einem Laser-Doppler-Vibrometer (LDV) und der zugehörigen PSV-Software von Polytec durchgeführt. Eine Messung läuft nach derzeitigem Stand so ab: Der Messpunkt wird eingegeben, Kameras und Laser werden auf ihn ausgerichtet, die Struktur wird angeregt und die Messung wird gestartet. Die Bedienung ist an die Software am Messrechner gebunden, und die Messungen werden manuell eingegeben. Messungen können nicht automatisch hintereinander ausgeführt werden. Jede Messung muss einzeln eingegeben und gestartet werden, wofür Anwesenheit am Messrechner nötig ist. Weitere Themen sind die Reproduzierbarkeit und die Dokumentation der verwendeten Einstellungen und Dateien. Die Auswertung erfolgt über die vorgegebenen Auswertungen der PSV-Software. Diese sind nicht für alle Fälle ideal geeignet. Eine Weiterverarbeitung der Daten in Python ist wünschenswert. Automatisierte, unbeaufsichtigte Messreihen sind für Strukturtests am Institut und für die Weiterverwendung in Forschungsprojekten von Bedeutung. Künftig betrifft dies auch Messungen für die Luft- und Raumfahrtindustrie.

Ziel der Arbeit ist die Entwicklung eines Softwarepakets in Python, das Strukturtests mit dem LDV automatisiert. Es führt Messungen über eine Warteschlange automatisch nacheinander aus. Eine Oberfläche dient vor allem der Verwaltung der Warteschlange und der Auswertungen und ist intuitiver bedienbar als die bisherige Bedienung. Das Softwarepaket unterstützt die Reproduzierbarkeit und die Dokumentation der Messungen und stellt eigene Auswertungen in Python bereit. Seine Eignung wird an einem realen Strukturtest nachgewiesen. Die PSV-Software wird dabei nicht ersetzt. Die Arbeit greift über die vorhandene Schnittstelle, das Component Object Model (COM), auf sie zu. Einrichtung, Geometrie und Ausrichtung bleiben in der PSV-Software. Eine vollständige Modalanalyse sowie die Ansteuerung weiterer Hardware sind nicht Teil der Arbeit.

Die Arbeit geht in vier Schritten vor. Zunächst wird die COM-Schnittstelle der PSV-Software anhand der Dokumentation und anschließend lesend am Messrechner untersucht. Dabei wird auch der heutige Ablauf einer Messung präzisiert. Danach werden die Anforderungen an das Softwarepaket mit den Betreuern in einem Lastenheft festgelegt und gegeneinander abgegrenzt. Dabei wird ermittelt, welche Schwächen der bisherigen Bedienung die Oberfläche adressiert und welche individuellen Auswertungen benötigt werden. Anschließend wird das Softwarepaket iterativ entwickelt: Architektur, Prototyp mit Warteschlange und Oberfläche, Tests ohne Gerät gegen einen Simulator der Schnittstelle sowie Reviews. Schließlich wird das Softwarepaket am Messrechner und in Strukturtests an einem Prüfling erprobt. Die eigenen Auswertungen werden mit der Auswertung der PSV-Software und mit analytischen Referenzfällen verglichen. Zusätzlich wird der Zeitaufwand verglichen: Dieselbe Messreihe wird einmal manuell und einmal mit dem Softwarepaket durchgeführt. Als theoretische Grundlagen dienen die Laser-Doppler-Vibrometrie einschließlich Scanning- und 3D-Vibrometern, die Strukturdynamik und der Modaltest, die Signalverarbeitung (Fourier-Transformation, Fensterung, Mittelung, Frequenzgangschätzung und Kohärenz) sowie die Softwaretechnik und Automatisierung (COM, Architektur, Teststrategie mit Simulator, Reproduzierbarkeit).

### Motivation
- Heutiger Ablauf (Nutzer, 2026-10-29, ausdrücklich noch ungenau; Präzisierung am Messrechner Mo 2026-11-02): Messpunkt eingeben → Kameras/Laser auf den Messpunkt ausrichten → Blech anregen → Messung starten.
- Problemkern (Nutzer, 2026-10-29): Bindung an die Software am Messrechner und manuelle Eingabe der Messungen; Messungen können nicht automatisch hintereinander ausgeführt werden.
- Weiteres Problem (Nutzer): Auswertung nur über die vorgegebenen Auswertungen der PSV-Software, die nicht für alle Fälle ideal geeignet sind; welche individuellen Auswertungen benötigt werden, wird während der Arbeit mit Daniel und Florian erarbeitet.
- Ebenfalls genannt (Nutzer): viele Messungen nacheinander (Anwesenheit am Rechner, Umbauten), Reproduzierbarkeit, Dokumentation der Einstellungen/Dateien, Auswertung/Weiterverarbeitung in Python.
- Praktische Bedeutung (Nutzer, 2026-10-29): Strukturtests am Institut; Luft- und Raumfahrtstrukturen; Weiterverwendung in Forschungsprojekten; unbeaufsichtigte Messreihen; künftige Messungen für die Luft- und Raumfahrt auch für die Industrie (Airbus nur als Beispiel genannt, keine belegte Kooperation → im Text allgemein „Luft- und Raumfahrtindustrie“, Entscheidung des Nutzers 2026-10-29).
### Ziel
- Bausteine (Nutzer, 2026-10-29): automatisierte Messdurchführung (PSV über COM, Mess-Warteschlange); bessere Oberfläche/GUI; Reproduzierbarkeit und Dokumentation; eigene Auswertung in Python; Nachweis am realen Strukturtest.
- Oberfläche (Nutzer, 2026-10-29): vor allem für Warteschlange und Auswertungen, zudem intuitiver als die bisherige Bedienung; welche Schwächen der bisherigen Bedienung konkret adressiert werden, wird erst während der Arbeit ermittelt.
- Nicht Teil der Arbeit (Nutzer, 2026-10-29):
  - Kein Ersatz der PSV-Software („das können wir gar nicht“) – die Arbeit nutzt nur die vorhandene COM-Schnittstelle, um auf die PSV-Software zuzugreifen; Einrichtung, Geometrie und Ausrichtung bleiben in PSV.
  - Keine vollständige Modalanalyse (Modalparameter-Identifikation nur gestuft/optional, R-054).
  - Keine Ansteuerung weiterer Hardware (Shaker, externer Signalgenerator, Positioniereinheit).
  - KI-Assistent für Warteschlangen nur optional (R-040, Kann).
### Lösungsweg
- Vorgehen (Nutzer, 2026-10-29, Reihenfolge wie Vorschlag):
  1. Analyse der Schnittstelle: COM-Schnittstelle und Objektmodell der PSV-Software aus der Dokumentation, danach lesende Erkundung am Messrechner.
  2. Anforderungen: Lastenheft mit den Betreuern (Muss/Soll/Kann), Abgrenzung.
  3. Iterative Entwicklung: Architektur, Prototyp mit Warteschlange und Oberfläche, Tests ohne Gerät gegen einen Simulator, Reviews.
  4. Erprobung und Validierung: Tests am Messrechner, Strukturtests am Prüfling, Vergleich eigener Auswertungen mit der PSV-Auswertung bzw. analytischen Referenzfällen.
- Theoretische Grundlagen (Nutzer, 2026-10-29): Laser-Doppler-Vibrometrie (Messprinzip, Scanning- und 3D-LDV); Strukturdynamik und Modaltest (inkl. Strukturtests in der Luft- und Raumfahrt); Signalverarbeitung (FFT, Fensterung, Mittelung, H1/H2, Kohärenz); Softwaretechnik und Automatisierung (COM, Architektur, Teststrategie mit Simulator, Reproduzierbarkeit). Quellen: siehe Abschnitt 4.

## 3 Gliederung
Vom Nutzer am 2026-10-29 übernommen (Vorschlag des Orchestrators nach SLA-Vorlage, Kapitel 1–6; höchstens drei Ebenen).

1 Einleitung
- 1.1 Motivation
- 1.2 Zielsetzung und Abgrenzung
- 1.3 Aufbau der Arbeit

2 Stand der Technik
- 2.1 Strukturtests in der Luft- und Raumfahrt
- 2.2 Laser-Doppler-Vibrometrie in der Strukturdynamik (3D-Scanning-Vibrometer, Polytec PSV)
- 2.3 Automatisierung von Messabläufen über Softwareschnittstellen
- 2.4 Handlungsbedarf

3 Methodik
- 3.1 Grundlagen der Signalverarbeitung für Schwingungsmessungen
- 3.2 Betriebsschwingformen und Grundlagen der Modalanalyse
- 3.3 Anforderungen an das Softwarepaket
- 3.4 Softwarekonzept

4 Umsetzung
- 4.1 Analyse der COM-Schnittstelle
- 4.2 Ansteuerung und Mess-Warteschlange
- 4.3 Benutzeroberfläche
- 4.4 Datenübernahme und Auswertung in Python
- 4.5 Versuchsaufbau und Durchführung der Strukturtests

5 Analyse und Auswertung der Ergebnisse
- 5.1 Verifikation der Software
- 5.2 Erprobung am Messrechner
- 5.3 Vergleich der Auswertungen mit der PSV-Software und mit Referenzfällen
- 5.4 Bewertung (Reproduzierbarkeit, Aufwand, Grenzen) – inkl. eigenem Vergleich des Zeitaufwands: gleiche Messreihe einmal manuell, einmal mit der Software (Nutzer, 2026-10-29)

6 Schlussfolgerung und Ausblick
- 6.1 Zusammenfassung
- 6.2 Ausblick

Anhang (Vorschlag): Bedienungsanleitung, Lastenheft, Versuchsprotokolle.

## 4 Erste Quellensammlung
- Grundlage: `in_progress/literatur/literatur.bib`, `in_progress/literatur/leseliste.md` (Paket L1).
- Für das Exposé (Nutzer, 2026-10-29): die 12 empfohlenen Quellen der Leseliste, als vorläufig gekennzeichnet (Existenz über Suchtreffer geprüft, Volltexte noch nicht gelesen).
- Volltexte Priorität A besorgt der Nutzer (Rothberg 2017, Ewins, Bendat/Piersol, Göge 2007) → `Input/literatur/`.
- Ergänzende Recherche (Nutzer): (a) Prüfstands-/Messautomatisierung; (b) wie Strukturtests bisher und in der Vergangenheit durchgeführt wurden (historische Entwicklung, klassische Verfahren) – Inhalt soll in der Arbeit behandelt werden (passt zu 2.1).

## 5 Zeitplan
Phasen ohne Dauer (Nutzer, 2026-10-29: Bearbeitungszeit hängt vom Antrag an den Prüfungsausschuss ab). Reihenfolge nach dem Lösungsweg; Phasen überlappen teilweise.

| Phase | Inhalt | Meilenstein |
|---|---|---|
| 0 Einarbeitung (vor Anmeldung) | Ausschreibung, PSV-System, COM-Dokumentation, Anforderungen, Prototyp Mess-Warteschlange | Exposé mit Betreuern abgestimmt → Anmeldung |
| 1 Analyse der Schnittstelle | Erkundung am Messrechner (ab Mo 2026-11-02), Abgleich mit der Dokumentation | Zugriff aus Python am Gerät nachgewiesen |
| 2 Anforderungen und Konzept | Lastenheft mit Daniel und Florian abstimmen, offene Fragen (u. a. Fehlerverhalten), Festlegung der individuellen Auswertungen | Lastenheft abgestimmt |
| 3 Iterative Entwicklung | Ansteuerung, Mess-Warteschlange, Oberfläche, Datenübernahme und Auswertung; Tests gegen Simulator | Softwarestand für Strukturtests |
| 4 Erprobung und Validierung | Strukturtests am Prüfling, Vergleich mit PSV-Auswertung und Referenzfällen, Vergleich des Zeitaufwands manuell vs. automatisiert | Ergebnisse ausgewertet |
| 5 Ausarbeitung | Thesis nach SLA-Vorlage (laufend begleitet durch Laborbuch), Erstversion an Daniel | Erstversion spätestens 2, besser 3 Wochen vor Abgabefrist (Vorgabe Betreuer) |
| 6 Abschluss | Einarbeitung der Korrektur, Abgabe über RWTHOnline, Archivordner, Vortrag (max. 20 min + ca. 10 min Diskussion, Probevortrag möglich) | Abgabe, Vortrag |

Laufend: wöchentliche Treffen mit Fortschrittsbericht und kurzem Protokoll (Vorgabe Betreuer).

## Offene Fragen an den Betreuer
Gesammelt aus Interview und Recherche (nicht Teil des Exposé-Textes; Auswahl durch den Nutzer):
1. Bearbeitungszeit und Abgabetermin nach Entscheidung über den Antrag (F1).
2. Gewichtung der vier Bereiche im Bewertungsraster (F3).
3. Fehlerverhalten der Mess-Warteschlange (F20, WICHTIG).
4. Welche individuellen Auswertungen werden benötigt (mit Daniel und Florian)?
5. Gibt es SLA-Hausreferenzen zu Ground Vibration Test, 3D-LDV und Automatisierung von Modaltests? Volltext DLR-Übersicht (Göge 2006)?
6. Datenblatt des PSV QTec 3D (Messbereiche, Bandbreite, Rauschen) (F8).
7. Langform bzw. korrekte Bezeichnung „PSV“ (Polytec-Produktname) für den Text.
8. Weiterverwendung der Software am Institut (F18).
