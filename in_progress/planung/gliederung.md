# Gliederung der Bachelorarbeit – Entwurf

**Stand:** 2026-11-05, vom Nutzer als Entwurf freigegeben; zur Abstimmung mit dem Betreuer (Richtlinie: „Gliederung unbedingt mit dem Betreuer besprechen“, Analyse I3).
**Grundlage:** Gliederung aus dem Exposé (`in_progress/planung/expose.md`, Abschnitt 3, vom Nutzer am 2026-10-29 übernommen), Kapitel 1–6 der SLA-Vorlage (I3), Thesis-Formalien in `KONVENTIONEN.md`, Lastenheft, `kapitel-map.md`, Grundlagenvorschlag I2 (7.1).
**Formalien:** unter 50 Seiten ohne Anhang; höchstens vierte Ebene, neue Ebene nur mit mindestens zwei Einträgen; jedes Kapitel mit ein bis zwei Sätzen Einleitung und Abschluss.
**Kennzeichnung:** **[neu]** = gegenüber dem Exposé ergänzt oder verschoben · **[offen]** = Entscheidung des Nutzers oder Betreuers nötig.

Die Seitenzahlen fehlen bewusst; einen Seitenplan legt der Zeitplan fest, sobald Umfang und Abgabetermin geklärt sind (F1).

## Gliederung

| Nr. | Abschnitt | Zweck (ein Satz) | Quellen im Repo |
|---|---|---|---|
| – | Kurzfassung / Abstract | Je höchstens eine Seite ohne Formeln und Literaturhinweise, etwa fünf Schlagwörter. | Exposé 2 |
| **1** | **Einleitung** | Führt in Problem, Ziel und Aufbau ein (Richtwert der Vorlage 1–2 Seiten). | Exposé 2 |
| 1.1 | Motivation | Beschreibt den heutigen manuellen Messablauf am PSV und seine Grenzen (Bindung an den Messrechner, keine Messreihen, feste Auswertungen). | Exposé „Motivation“; Laborbuch 2026-11-02_messrechner-erster-termin |
| 1.2 | Zielsetzung und Abgrenzung | Nennt die Ziele und grenzt aus, was die Arbeit nicht leistet (kein Ersatz der PSV-Software, keine vollständige Modalanalyse, keine weitere Hardware). | Exposé „Ziel“; Erwartungsmanagement 2 |
| 1.3 | Aufbau der Arbeit | Gibt einen Überblick über die Kapitel. | – |
| **2** | **Stand der Technik** | Ordnet die Arbeit ein und begründet den Handlungsbedarf. | Literatur (`literatur.bib`), I2 |
| 2.1 | Strukturtests in der Luft- und Raumfahrt | Zeigt, wofür Schwingungsmessungen an Strukturen eingesetzt werden. | Recherche offen |
| 2.2 | Laser-Doppler-Vibrometrie in der Strukturdynamik | Stellt das 3D-Scanning-Vibrometer und die Polytec-PSV-Software als Stand der Messtechnik vor. | I2 2; Polytec-Handbücher |
| 2.3 | Automatisierung von Messabläufen über Softwareschnittstellen | Beschreibt Ansätze zur Fernsteuerung von Messsoftware (COM, Skripting). | I1, I5; Recherche offen |
| 2.4 | Handlungsbedarf | Leitet aus 2.1–2.3 die Lücke ab, die die Arbeit schließt. | Exposé „Motivation“ |
| **3** | **Methodik** | Legt Grundlagen, Anforderungen und Konzept fest, soweit sie über die tägliche Arbeit eines Strukturmechanik-Ingenieurs hinausgehen (Vorlage `03_theory.tex`). | I3 A2 |
| 3.1 | Messprinzip des 3D-Laser-Doppler-Vibrometers **[neu] [offen]** | Erklärt Doppler-Effekt, Heterodyn-Interferometrie und die Vektorzerlegung aus drei Scanköpfen, soweit Auswertung und Fehlerquellen sie brauchen. | I2 2.1, 7.1 (1, 2) |
| 3.2 | Signalverarbeitung für Schwingungsmessungen | Definiert DFT, Frequenzachse, Fenster, Mittelung, H1/H2 und Kohärenz in den Konventionen der Arbeit. | FG-02 2–3; I2 3 |
| 3.3 | Betriebsschwingformen und Dämpfungsschätzung | Erklärt Betriebsschwingform, Spitzensuche und −3-dB-Dämpfungsschätzung mit ihren Grenzen. | FG-02 8; FG-03; ADR-025 |
| 3.4 | Anforderungen an das Softwarepaket | Fasst das Lastenheft zusammen (Muss/Soll/Kann, Quelle). | Lastenheft; Anhang B |
| 3.5 | Softwarekonzept | Beschreibt Architektur, Schichten (Gerät, Ablauf, Auswertung, Darstellung, Oberfläche) und Teststrategie mit Simulator. | ADR-001 ff.; ADR-021, -022, -024 |
| **4** | **Umsetzung** | Beschreibt die Umsetzung so, dass alle Einstellungen und Daten reproduzierbar sind (Vorlage `04_execution.tex`). | Laborbuch; Git-Historie |
| 4.1 | Analyse der COM-Schnittstelle | Zeigt Objektmodell, Erkundung am Messrechner und die Bewertung der Schnittstelle (Registrierung, Start-/Desktop-Modus, nicht lesbare Felder). | I1, I5; Erkundungsberichte 2026-11-02; Faktenliste 02.11.; kapitel-map „Bewertung der PSV-Schnittstelle“ |
| 4.2 | Ansteuerung und Mess-Warteschlange | Beschreibt Messablauf, Warteschlange, Betriebsarten und Messprotokoll. | Lastenheft R-001, R-010 bis R-024; Prüfanleitung U3 |
| 4.3 | Datenübernahme aus den Messdateien **[neu]** | Beschreibt den eigenen Leser für .svd-Dateien und die Prüfung der Frequenzachse. | ADR-020, ADR-023; `svd_lesen.py`; Laborbuch 2026-11-03_r023-r055 |
| 4.4 | Auswertung und Darstellung | Beschreibt Spektrum, FRF, Spitzen und Bänder, Schwingform und die gemeinsame Zeichenschicht für Oberfläche und Thesis. | FG-02, FG-03; ADR-021, -024, -025; Laborbuch 2026-11-04/05_auswerten-* |
| 4.5 | Benutzeroberfläche | Zeigt Bedienkonzept für Warteschlange und Auswertung (Reiter „Messen“ und „Auswerten“). | Design-Briefs; ADR-001, ADR-026 |
| 4.6 | Versuchsaufbau und Durchführung der Strukturtests | Nennt Prüfling, Lagerung, Anregung, Messgitter und Parameter in Tabellen. | Versuchspläne unter `in_progress/versuche/`; Fotos 02.11.; kapitel-map „Versuchsaufbau“ |
| **5** | **Analyse und Auswertung der Ergebnisse** | Prüft die Ergebnisse kritisch, mit Unsicherheiten und Fehlern (Vorlage `05_implementation.tex`). | – |
| 5.1 | Verifikation der Software | Belegt die Korrektheit ohne Gerät: Tests gegen den Simulator, analytische Referenzfälle, Abdeckung. | FG-02/FG-03 Referenzfälle; Testberichte; KONVENTIONEN „Standard-Prüfung“ |
| 5.2 | Validierung des Datenwegs gegen PSV **[neu]** | Vergleicht die eigene Datenübernahme und Auswertung mit PSV (Golden File Label 132). | `ergebnisse_7b.md`; `golden_punkt1_label132.csv`; kapitel-map „Validierung“ |
| 5.3 | Erprobung am Messrechner | Berichtet die Tests am Gerät (Erkundung, Prototyp T0 bis T6, Auswerten-Reiter). | Laborbuch der Termine; Protokolle |
| 5.4 | Fehler, Grenzen und Unsicherheiten **[neu]** | Dokumentiert Fehlschläge und Grenzen (Frequenzachse, Polarität der Referenzkanäle, Grenzen der PSV-Peak-Anpassung). | kapitel-map „Fehlschlag Frequenzachse“, „Polaritätsprüfung“, „Grenzen der PSV-Auswertung“ |
| 5.5 | Bewertung | Bewertet Reproduzierbarkeit, Zeitaufwand (gleiche Messreihe manuell und mit der Software) und Grenzen des Pakets. | Exposé 3 (5.4); Versuch offen |
| **6** | **Schlussfolgerung und Ausblick** | Beantwortet die Leitfragen der Vorlage: Was wurde gemacht, Hauptergebnisse, Ziel erreicht, Forschungsbedarf. | – |
| 6.1 | Zusammenfassung | Fasst Vorgehen und Hauptergebnisse zusammen. | – |
| 6.2 | Ausblick | Nennt offene Punkte und mögliche Erweiterungen (z. B. R-040, R-054, R-056). | Lastenheft (Kann) |
| – | Literaturverzeichnis | | `literatur.bib` |
| A | Anhang: Bedienungsanleitung | | Prüf- und Installationsanleitungen |
| B | Anhang: Lastenheft | | `lastenheft.md` |
| C | Anhang: Versuchsprotokolle | | `in_progress/versuche/` |

## Zuordnung der Muss-Anforderungen

| Anforderung | Kapitel |
|---|---|
| R-001 (COM-Steuerung) | 4.1, 4.2, 5.3 |
| R-010 bis R-018 (Warteschlange) | 4.2, 5.3 |
| R-020, R-023, R-024 (Messprotokoll, Frequenzachse) | 4.2, 4.3, 5.4 |
| R-022 (Datenübernahme) | 4.3, 5.2 |
| R-030, R-031 (Oberfläche Warteschlange) | 4.5, 5.3 |
| R-050 bis R-053, R-055 (Darstellung, Spitzen, Dämpfung) | 3.2, 3.3, 4.4, 5.2 |
| R-060 bis R-062 (Python, Simulator, Prüfungen) | 3.5, 5.1 |

Lücken: keine Muss-Anforderung ohne Kapitel. R-019 (Verhalten bei Fehlschlag) ist noch ohne Priorität (Frage F20) und steht vorläufig bei 4.2.

## Änderungen gegenüber dem Exposé

1. **3.1 Messprinzip neu [offen]:** I2 schlägt das LDV-Messprinzip für die Grundlagen vor; im Exposé steht es nur im Stand der Technik (2.2). Alternative: nur in 2.2 belassen und 3.1 streichen.
2. **4.3 Datenübernahme** als eigener Abschnitt, weil der eigene Leser (ADR-020) und die Frequenzachse eigenes Gewicht haben; vorher Teil von 4.4.
3. **Benutzeroberfläche** von 4.3 nach 4.5, damit Oberfläche nach den Funktionen kommt, die sie bedient.
4. **5.2 Validierung gegen PSV** und **5.4 Fehler, Grenzen und Unsicherheiten** neu aus den vorgemerkten Bausteinen der `kapitel-map.md`; die Vorlage verlangt Unsicherheiten und Fehler in Kapitel 5.
5. **3.3** „Grundlagen der Modalanalyse“ auf „Dämpfungsschätzung“ eingegrenzt, weil die vollständige Modalanalyse nicht Teil der Arbeit ist (R-054 gestuft).

## Offene Fragen an den Betreuer

| Nr. | Frage | Auswirkung |
|---|---|---|
| G1 | Passt der Kapitelzuschnitt der SLA-Vorlage für eine softwarelastige Arbeit, oder soll „Methodik“ in „Konzept“ umbenannt werden (I3 A3)? | Kapitelnamen 3 und 4 |
| G2 | Gehört das LDV-Messprinzip in den Stand der Technik oder in die Grundlagen (3.1)? | Umfang Kapitel 2/3 |
| G3 | Darf ein eigener Abschnitt Fehlschläge dokumentieren (5.4)? | Kapitel 5 |
| G4 | Umfang und Abgabetermin (F1) | Seitenplan, Zeitplan |
