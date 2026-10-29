# Exposé – Entwurf (im Interview mit Jakob, Stand 2026-10-28)

> Arbeitsstand. Grundlage: Vorgaben des Betreuers in `Input/20260416_Erwartungsmanagement.pdf` (S. 2):
> Titelvorschlag · Kurzfassung (Motivation, Ziel, Lösungsweg) · Gliederung · erste Quellensammlung · Zeitplan.
> Inhalte stammen aus den Antworten des Nutzers; Vorschläge des Orchestrators sind als solche gekennzeichnet.

## Rahmen (nicht Teil des Exposé-Textes)
- Betreuung: Daniel Alboldt (SLA) und Florian (SLA, zweiter Betreuer; Nachname noch eintragen).
- Anmeldung verzögert sich wegen eines Antrags an den Prüfungsausschuss (Stand 2026-10-28).
- Bearbeitungszeit und Abgabetermin hängen vom Ausgang des Antrags ab → Zeitplan relativ in Wochen ab Anmeldung; offener Punkt F1.

## 1 Titel
- Offen: wird nach Motivation und Ziel gemeinsam erarbeitet (Ausschreibungstitel als Ausgangspunkt).

## 2 Kurzfassung
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

## 3 Gliederung

## 4 Erste Quellensammlung
- Grundlage: `in_progress/literatur/literatur.bib`, `in_progress/literatur/leseliste.md` (Paket L1).

## 5 Zeitplan

## Offene Fragen an den Betreuer
