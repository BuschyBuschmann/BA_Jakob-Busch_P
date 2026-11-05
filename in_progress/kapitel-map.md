# Kapitel-Zuordnung

Ordnet Laborbuch-Einträge, Entscheidungen (ADR), Versuche und Fachgrundlagen den
Kapiteln der Thesis zu. Die Gliederung wird mit `/ba-planung` festgelegt und an die
Institutsvorlage angepasst.

Gliederung: `in_progress/planung/gliederung.md` (Entwurf, vom Nutzer am 2026-11-05 freigegeben, Abstimmung mit dem Betreuer offen, Fragen G1–G4).

| Kapitel | Quellen im Repo | Stand |
|---|---|---|
| 1 Einleitung | Exposé 2; Erwartungsmanagement 2 | Material vorhanden |
| 2 Stand der Technik | I1, I2, I5; `literatur.bib` | Recherche zu 2.1 und 2.3 offen |
| 3.1 Messprinzip 3D-LDV (Platz offen, G2) | I2 2.1, 7.1 | Material teilweise |
| 3.2 Signalverarbeitung | FG-02 2–3; I2 3 | Material vorhanden |
| 3.3 Betriebsschwingformen und Dämpfungsschätzung | FG-02 8; FG-03; ADR-025 | Material vorhanden |
| 3.4 Anforderungen | Lastenheft; Nachverfolgung | Material vorhanden |
| 3.5 Softwarekonzept | ADR-001 ff., ADR-021, ADR-022, ADR-024 | Material vorhanden |
| 4.1 Analyse der COM-Schnittstelle | Laborbuch 2026-11-02_messrechner-erster-termin; Erkundungsberichte; Faktenliste 02.11. (Baustein „Bewertung der PSV-Schnittstelle“) | Material vorhanden |
| 4.2 Ansteuerung und Warteschlange | Lastenheft R-001, R-010–R-024; Prüfanleitung U3; `in_progress/versuche/2026-11-02_prototyp/` | Erprobung am Gerät offen |
| 4.3 Datenübernahme | ADR-020, ADR-023; Laborbuch 2026-11-03_r023-r055 | Material vorhanden |
| 4.4 Auswertung und Darstellung | FG-02, FG-03; ADR-021, ADR-024, ADR-025; Laborbuch 2026-11-04/05_auswerten-* | Material vorhanden |
| 4.5 Benutzeroberfläche | Design-Briefs; ADR-001, ADR-026 | Material vorhanden |
| 4.6 Versuchsaufbau und Durchführung | Laborbuch 2026-11-02; Fotos; `in_progress/versuche/` (Baustein „Versuchsaufbau“) | Datenblatt PCB offen |
| 5.1 Verifikation der Software | Referenzfälle FG-02/FG-03; Testberichte im Laborbuch | Material vorhanden |
| 5.2 Validierung gegen PSV | `ergebnisse_7b.md`; Golden File Label 132 (Baustein „Validierung“) | Material vorhanden |
| 5.3 Erprobung am Messrechner | Laborbuch der Termine; Protokolle | Termin 2026-11-09 offen |
| 5.4 Fehler, Grenzen und Unsicherheiten | Bausteine „Fehlschlag Frequenzachse“, „Polaritätsprüfung“, „Grenzen der PSV-Auswertung“ | teilweise (D2 offen) |
| 5.5 Bewertung | Exposé 3 | Zeitvergleich manuell/automatisch offen |
| 6 Schlussfolgerung und Ausblick | Lastenheft (Kann) | offen |

## Vorgemerkte Thesis-Bausteine (Übersicht 02.11., Abschnitt 2f; zugeordnet in der Tabelle oben)

| Baustein | Quellen im Repo | Stand |
|---|---|---|
| Bewertung der PSV-Schnittstelle (COM-Registrierung bei parallelen Versionen, Start-/Desktop-Modus, Late Binding und Cast, nicht lesbare Felder, File Access ohne Registrierung) | Laborbuch 2026-11-02_messrechner-erster-termin; Erkundungsberichte `in_progress/versuche/erkundung/erkundung_BEOWOLF_2026-11-02_*`; `com_registrierung_psv104.md`; Faktenliste 02.11.; Analyse E-PSV-S (Übersicht 02.11.) | Material vorhanden |
| Validierung des eigenen Datenwegs gegen PSV (Golden File Label 132, bitgleiche Spektren, H1 ≤ 5,8·10⁻⁸) | `ergebnisse_7b.md`; `golden_punkt1_label132.csv`; Test `test_golden_file_label_132`; FG-02 9.9 | Material vorhanden |
| Fehlschlag Frequenzachse (Zirkelschluss W2, Faktor 2,5, Nachweis und Korrektur) | Laborbuch 2026-11-02_k-achse-frequenzachse; Fachanalyse P0b (Übersicht 02.11.); FG-02 2.3; Korrekturvermerke W2/W5-1 | Material vorhanden |
| Grenzen der PSV-Auswertung (Peak-Anpassung handabhängig und an der Auflösungsgrenze ohne Warnung, keine PCA) | `ergebnisse_7b.md` M11; Recherche R-0211 (Handbuch V10.1, Peak-Fit); FG-02 Abschnitt 8 | Material teilweise (M11 an kennzeichenfreien Spitzen folgt) |
| Polaritätsprüfung der Referenzkanäle (P-08, Treibpunkt-Kriterium) | FG-02 4 (P-08); Fachanalysen P0b, E-PSV-F; Ablaufplan nächster Termin D2 | offen (Messung D2) |
| Versuchsaufbau (frei hängendes Blech, Impedanzkopf PCB 288D01, Mini SmartShaker, drei Scanköpfe) | Laborbuch 2026-11-02; Fotos `in_progress/versuche/2026-11-02_prototyp/fotos/` | Material vorhanden (Typschild Shaker, Datenblatt PCB offen) |
