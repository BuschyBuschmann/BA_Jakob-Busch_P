# 2026-10-23 – Sichtung des Inputs (Polytec-Unterlagen, Beispielcode, Vorlagen)

**Art:** Arbeitspaket
**Paket/Bezug:** I1–I4 (Input-Sichtung)
**Commit:** 21e7fb1 (letzter Stand vor der Sichtung; noch kein Code unter `software/`)
**Beteiligt:** `software-engineer` (I1, opus), `strukturdynamik-experte` (I2, sonnet), `wissenschaftlicher-autor` (I3, sonnet), Orchestrator (I4)

## Ziel
Den vom Nutzer hochgeladenen Input inhaltlich erschließen, eine Übersicht erstellen
und prüfen, ob Agenten oder Skills ergänzt bzw. umgebaut werden müssen.

## Vorgehen
Drei parallele, nur lesende Analysepakete:
- I1: COM-Anleitung, CHM-Hilfen (Basic Engine Manual, Polytec File Access), Software-
  Handbuch PSV, Beispielbibliothek STABCOOL.
- I2: Schulungsunterlagen, Theory Manual, Betriebsanleitung PSV-QTec-3D-H, VibroFlex.
- I3: LaTeX-Vorlage, Richtlinien-PDF, Plot- und Präsentationsvorlagen.
Die CHM-Dateien wurden im Container mit `libchm-bin` entpackt (Pakete per apt
installiert). Fachliche Sollwerte hat der `strukturdynamik-experte` mit eigenen
Skripten nachgerechnet; Signatur- und Rechenfehler im STABCOOL-Code hat der
`software-engineer` mit Testaufrufen nachgewiesen.

## Ergebnis
- Analyseberichte unter `in_progress/analysen/2026-10-23_I1…I3_*.md`.
- Übersicht unter `in_progress/input-uebersicht.md` mit 15 offenen Fragen.
- Kernaussagen: Der Messablauf ist per COM vollständig automatisierbar; Polytec belegt
  Python-Zugriff mit pywin32. Die Signalverarbeitung läuft in der PSV-Software; der
  Mehrwert des Pakets liegt bei Ablaufsteuerung, Reproduzierbarkeit,
  Plausibilitätsprüfung, erweiterter Auswertung und Dokumentation.
- Das Richtlinien-PDF stammt aus den Wirtschaftswissenschaften und widerspricht der
  SLA-Vorlage. Die SLA-Vorlage verlangt eine KI-Erklärung je Abschnitt.

## Verifikation
Alle Aussagen der Berichte mit Datei und Seite bzw. CHM-Thema belegt; Einschätzungen
gekennzeichnet. Kein realer COM-Zugriff und keine reale Messdatei geprüft.

## Probleme und verworfene Ansätze
- In den Unterlagen widersprüchliche Angaben (z. B. Abtastfaktor 2,5 gegen 2,56,
  Fensterempfehlung für Sweep, Flat-Top-Fehler); dokumentiert in Bericht I2, Abschnitt 9.
- Die LaTeX-Vorlage ist unvollständig (Logo fehlt), ihr Log endet mit einem Fehler.

## Offene Punkte
Siehe `in_progress/input-uebersicht.md`, Abschnitt 7; insbesondere Installation von
Python auf dem Messrechner, lizenzierte PSV-Optionen, Ziel der Auswertung,
Kraftreferenz, gültige Formalien. Erwartungsmanagement mit dem Betreuer steht aus.

## Thesis-Bezug
Grundlagen (LDV, Signalverarbeitung), Stand der Technik (PSV-Automatisierung),
Methodik und Umsetzung (Polytec-Konventionen, Architektur).
