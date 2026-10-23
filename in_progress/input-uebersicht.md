# Input-Übersicht (Stand 2026-10-23)

Erste inhaltliche Sichtung des Materials unter `Input/`. Die Details mit Seiten- und
Zeilenbelegen stehen in den drei Analyseberichten unter `in_progress/analysen/`:

| Bericht | Inhalt | Erstellt von |
|---|---|---|
| `2026-10-23_I1_com-schnittstelle-software.md` | COM-Objektmodell der PSV-Software, Polytec File Access, Python-Zugriff, Beispielbibliothek STABCOOL, ADR-Vorschläge | `software-engineer` |
| `2026-10-23_I2_messtechnik-fachgrundlagen.md` | Messprinzip, Systemaufbau, Signalverarbeitung nach Polytec-Konvention, Plausibilitätskriterien, Fachgrundlagen mit nachgerechneten Referenzfällen, Rechercheaufträge | `strukturdynamik-experte` |
| `2026-10-23_I3_vorlagen-richtlinien.md` | LaTeX-Vorlage des SLA, Richtlinien-PDF, Plot- und Präsentationsvorlagen, Aufbau von `in_progress/thesis/` | `wissenschaftlicher-autor` |

Kennzeichnung unten: Belegtes ist mit Quelle im jeweiligen Bericht hinterlegt;
**Einschätzung** markiert nicht belegte Bewertungen.

---

## 1. Was im Input liegt

| Bereich | Inhalt | Relevanz |
|---|---|---|
| `Input/Softwarepaket für Luft- und Raumfahrt_Daniel.pdf` | Ausschreibung (Betreuer Daniel Alboldt, SLA) | Aufgabenstellung |
| `Input/literatur/polytec/06_Automatisierung_via_COM/` | Polytec-Anleitung „Automatisierung via COM“ mit Notiz des Betreuers: Zugriff auch per Python | Kern: Einstieg in die Schnittstelle |
| `Input/literatur/polytec/Windows Hilfedateien/` | CHM-Hilfen: **Basic Engine Manual** (COM-Objektmodell), **Polytec File Access** (Dateizugriff), PSV-Hilfen | Kern: API-Referenz |
| `Input/literatur/polytec/Handbücher/` | Software-Handbücher PSV und PSV Desktop (V 10.1, DE/EN), Theory Manual, Betriebsanleitung PSV-QTec-3D-H, VibroFlex-Einpunktvibrometer | Messablauf, Konventionen, Systemaufbau |
| `…/Handbücher/nicht vorhandene Systeme/` | MSA, MSA 3D, Stage, UHF | für den Kern nicht nötig |
| `Input/literatur/polytec/Schulungsunterlagen/` | 17 Polytec-Schulungsfoliensätze (Aufbau, Physik, FFT, Anregung, 3D-Abgleich, Messgitter, Auswertung, SignalProzessor, File Access) | Praxis, Grundlagen |
| `Input/literatur/Example_Library_STABCOOL/` | Python-Code eines anderen Institutsprojekts (AD-Karte, Traverse, PSD-Messung) | Vorbild und Gegenbeispiel |
| `Input/Templates/LaTeX-Vorlage Wissenschaftliche Arbeit/` | LaTeX-Vorlage des SLA (KOMA scrbook, pdfLaTeX, biber, glossaries) | Thesis |
| `Input/Templates/Richtlinien_fuer_wissenschaftliches_Arbeiten.pdf` | Richtlinie der **TIME Research Area (Wirtschaftswissenschaften)**, nicht des SLA | Gültigkeit klären |
| `Input/Templates/` sonst | MATLAB- und gnuplot-Plotvorlagen, Schrift ISONORM 3098, PowerPoint-Vorlage SLA | Abbildungen, Vorträge |
| Platzhalter | `HIER EIGENES DOKUMENT ERWARTUNGSMANAGEMENT EINFUEGEN.txt`, `HIER AKTUELLE LATEXVORLAGE EINFUEGEN.txt` | beide leer |

## 2. Das Messsystem

- Laut Betriebsanleitung ein **Polytec PSV-QTec-3D-H**: drei Scanköpfe (PSV-I-680 mit
  Kamera und Geometrielaser, 2 × PSV-I-690), Frontend PSV-F-600-3D-H mit acht
  Referenzeingängen und vier Generatorausgängen, Data Management System (Windows 10,
  64 Bit). Welche Variante im Labor steht, ist unbestätigt.
- Software **PSV 10.x** (Handbücher 10.1, COM-Beispiel meldet 10.2.1.1).
- Das Vibrometer misst die Geschwindigkeit entlang des Strahls; die PSV-Software setzt
  aus den drei Strahlrichtungen die 3D-Komponenten zusammen. Die Qualität hängt am
  3D-Abgleich und an der Strahlgeometrie.
- Für reproduzierbare Messungen kritisch: unveränderte Kopfpositionen und Abgleich,
  identische Einstellungen, gleiche Anregung und Generatorlast, Warmlaufzeit
  (30 min, für Winkelstabilität 120 min), gespeicherte Fokuswerte.

## 3. Die COM-Schnittstelle

- „COM“ meint hier das **Component Object Model** von Windows, nicht die serielle
  Schnittstelle. In der STABCOOL-Bibliothek bedeutet „COM“ dagegen einen seriellen Port;
  diese Verwechslung in Anforderungen und Thesis vermeiden.
- Das Objektmodell der PSV-Software ist umfassend dokumentiert. Einstieg:
  `AcquisitionInstance` → `Application` → `Acquisition`, `Settings`, `Exporter`.
- Der gesamte Ablauf ist belegt automatisierbar:
  1. **Verbinden** mit Timeout,
  2. **Einstellen** über gespeicherte Einstellungsdateien (`.set`) oder einzelne
     Eigenschaften (FFT, Mittelung, Generator, Kanäle, Trigger),
  3. **Scannen** mit Dateinamen und Zustandsabfrage bis „Stopped“,
  4. **Speichern**: die PSV-Software schreibt jeden Punkt sofort in die `.svd`-Datei,
  5. **Daten lesen** über **Polytec File Access** (ohne Dongle, nur Windows/COM) oder
     über Export (UFF, ASCII, ME'Scope, ATFX).
- Polytec liefert eigene **Python-Beispiele mit pywin32**; das ist der einzige belegte
  Python-Weg.
- **Stolpersteine:** 1-basierte Indizes, Phase standardmäßig in Grad, Daten als float32
  und verschränkt (Real/Imag bzw. Betrag/Phase), 3D-Daten erst alle x-, dann y-, dann
  z-Werte; eine Datei kann nicht gleichzeitig in PSV und Polytec File Access offen sein.
- **Kritischer Rahmen:** Laut Betriebsanleitung soll auf dem Messrechner keine
  Fremdsoftware ohne Rücksprache mit Polytec installiert werden. Das betrifft Python,
  uv und pywin32. Fernsteuerung per DCOM ist laut Polytec sehr aufwendig.

## 4. Was die PSV-Software selbst rechnet – und was unser Paket leisten kann

| PSV-Software (belegt) | Mehrwert eines eigenen Python-Pakets (Einschätzung) |
|---|---|
| FFT, Fenster, Mittelung, H1/H2, Kohärenz, PSD, RMS, 3D-Komponenten | Reproduzierbare, parametrisierte Messserien mit Protokoll und Git-Hash |
| Anzeige, Animation, Bänder, SDOF-Peak-Fit („Dämpfung“ = −3-dB-Breite) | Automatische Plausibilitätsprüfungen (17 Kandidaten P1–P17 im Bericht I2) |
| SignalProzessor (Formeln auf Messdaten), Export | Modalanalyse über SDOF hinaus (MDOF, Stabilisierungsdiagramm, MAC) |
| Mittelwertspektrum nur als Betragsmittel | Vergleich von Wiederholungen und Versuchen, Berichte und Abbildungen per Skript |

Eigene Spektralschätzung ist nur aus Zeitdaten möglich (Option „Time Domain Data“).
Sonst verarbeitet das Paket die Polytec-Ergebnisse weiter und kann sie als Gegenprobe
nachrechnen.

**Polytec-Konventionen (belegt, für Code und Thesis wichtig):** einseitige Spektren mit
Spitzenamplitude; Abtastrate = 2,5 × Bandbreite (H-System); Frequenzlinien bei k·Δf ab
k = 1 (indirekt belegt, an realer Datei zu prüfen); positive Geschwindigkeit = Bewegung
zum Scankopf; FRF-Definition wie im Lehrbuch.

## 5. Beispielbibliothek STABCOOL

- **Übernehmen:** eine Klasse je Gerät, Geräteerkennung, Endlagen- und Wertprüfung,
  Fehlercode-Tabellen, Dateinamen mit Zeitstempel.
- **Vermeiden** (nachgewiesen): Konfiguration als Skript-Variablen, `print` statt
  Fehlerbehandlung, Warteschleifen ohne Timeout, stilles Ausweichen auf andere
  Abtastraten, ein Signaturfehler, eine falsche Amplitudenskalierung (11,5 statt 1),
  Datenreduktion auf float16, veraltete NumPy-Aufrufe.

## 6. Thesis-Vorlage und Formalien

- Die **SLA-LaTeX-Vorlage** gibt die Struktur vor: Titelseite, KI-Erklärung,
  Kurzfassung, Abstract, Verzeichnisse, sechs Kapitel (Einleitung, Stand der Technik,
  Methodik, Umsetzung, Ergebnisse, Schluss), numerisches Zitieren mit biber.
- SLA-Regeln aus dem Anhang der Vorlage: Präsens, 3. Person, aktiv; unter 50 Seiten
  ohne Anhang; Zahlen eins bis zwölf ausgeschrieben; Farben dürfen im Graustufendruck
  keine Information tragen, kein Gelb; Diagramme auf A5 lesbar.
- **KI-Erklärung** (Vorlage, vom Prüfungsamt gefordert): Tabelle „Abschnitt der
  Arbeit / Einsatzzweck“ für jeden KI-Einsatz bei Text oder Bildern. Ungeprüft
  übernommene KI-Fehler gelten als Täuschungsversuch.
- Das **Richtlinien-PDF** stammt aus den Wirtschaftswissenschaften und widerspricht der
  SLA-Vorlage (Harvard- statt numerischem Zitieren, 40 statt unter 50 Seiten, Layout).
  Bis zur Klärung gilt die SLA-Vorlage (Annahme).
- Die Vorlage ist unvollständig: Ordner `PICTURES/` mit dem Logo fehlt; ohne Logo
  bricht die Titelseite ab. Das mitgelieferte Log endet mit einem Fehler.
- Plotstil aus den Vorlagen: Schrift ISONORM 3098, 16 cm Breite, Seitenverhältnis 0,71,
  schwarz mit Markern statt Farben, Gitter, Achsen „Größe [Einheit]“, kein Plot-Titel.
  Die Schrift ist lizenzpflichtig; Weitergabe im Repo ungeklärt.
- Im Cloud-Container ist kein LaTeX installiert.

## 7. Offene Fragen (gesammelt, Klärung über Erwartungsmanagement bzw. Betreuer)

**Entscheidend für Anforderungen und Architektur**
1. Darf auf dem PSV-Messrechner Python 3.11 mit pywin32 installiert werden
   (Rücksprache mit Polytec)? Sonst: anderer Rechner, DCOM oder Export-Weg.
2. Welche PSV-Version und welche Optionen sind lizenziert (Time Domain Data,
   Signalgenerator, Exporte, PCA)? Ist Polytec File Access installiert?
3. Ziel der Auswertung: nur Spektren und Betriebsschwingformen oder auch
   Modalparameter (Eigenfrequenzen, Dämpfung, Eigenformen)?
4. Wird die Anregungskraft gemessen (Kraftsensor/Hammer) oder ist die Referenz nur das
   Generatorsignal in Volt? Davon hängt ab, ob die FRF eine Mobilität ist.
5. Was heißt „reproduzierbar“ quantitativ (Toleranzen, MAC-Schwelle, Normen)?
6. Soll das Paket auch weiteres Versuchsequipment steuern (Generator, Positioniereinheit,
   Traverse)? Die Ausschreibung spricht von „Versuchsequipment“.

**Labor und Daten**
7. Zugang zum Laborrechner: vor Ort oder Fernzugriff? Werden Geometrie und
   3D-Abgleich weiterhin interaktiv in PSV vorbereitet?
8. Prüfling, Lagerung, Anregungsart, Frequenzbereich.
9. Kann der Betreuer vorhandene Makros (`SettingsandScan.bas`) und eine kleine
   Referenzmessung (`.svd` plus UFF-Export) bereitstellen?
10. Spezifikation des PSV-QTec-3D (Messbereiche, Rauschen, Bandbreite) fehlt im Input.

**Thesis-Formalien**
11. Gilt die SLA-Vorlage oder das Richtlinien-PDF (Zitierstil, Umfang, Layout)?
12. Ist die hochgeladene LaTeX-Vorlage die aktuelle? Logo bzw. `PICTURES/` nachreichen.
13. Genaue Form der KI-Erklärung und Umgang mit KI-unterstützten Rohfassungen, Code und
    Abbildungen.
14. Abgabeformalien (Termin, Exemplare, ein- oder zweiseitig), Quellenzahl.
15. Darf die Schrift ISONORM 3098 verwendet und ins Repo gelegt werden?

## 8. Wichtige Quellen für die Thesis

Polytec-Unterlagen sind für gerätespezifische Konventionen zitierfähig
(Herstellerdokumentation mit Dokumentnummer), nicht für allgemeine Theorie. Dafür sind
Fachbücher und begutachtete Artikel nötig; zwölf Rechercheaufträge (R1–R12) stehen im
Bericht I2, Abschnitt 7.3. Die Literaturkandidaten dort sind unverifiziert.

## 9. Was noch nicht ausgewertet ist

- Bildinhalte vieler Schulungsfolien und Formeln im Theory Manual (nur teilweise
  gerendert), Teile der Software-Handbücher, englische Duplikate.
- Kein realer COM-Zugriff und keine reale Messdatei; alle Aussagen zum Verhalten aus
  Python sind ungeprüft.
- Die entpackten CHM-Texte lagen nur im flüchtigen Arbeitsverzeichnis der
  Cloud-Sitzung und sind nicht im Repo.
