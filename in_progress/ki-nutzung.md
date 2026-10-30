# KI-Nutzungsregister

Grundlage der KI-Erklärung der Thesis (Vorlage `CHAPTERS_REST/03_integrity.tex`:
Tabelle „Abschnitt der Arbeit / Einsatzzweck“). Erfasst wird jeder KI-Einsatz, der
Text, Abbildungen, Code oder Inhalte der Arbeit beeinflussen kann. Welche Einträge in
die Erklärung gehören, wird mit dem Betreuer geklärt; im Zweifel wird erfasst.

Prüfung: `offen` = vom Nutzer noch nicht inhaltlich geprüft; `geprüft (Datum)` =
Nutzer hat das Ergebnis geprüft und verantwortet es.

| Datum | Artefakt bzw. Abschnitt | Einsatzzweck | Agent (Modell) | Prüfung |
|---|---|---|---|---|
| 2026-10-23 | `in_progress/analysen/2026-10-23_I1_com-schnittstelle-software.md` | Sichtung und Zusammenfassung der COM- und Softwaredokumentation, Analyse Beispielcode | software-engineer (opus) | offen |
| 2026-10-23 | `in_progress/analysen/2026-10-23_I2_messtechnik-fachgrundlagen.md` | Fachliche Sichtung der Polytec-Unterlagen, nachgerechnete Referenzwerte | strukturdynamik-experte (sonnet) | offen |
| 2026-10-23 | `in_progress/analysen/2026-10-23_I3_vorlagen-richtlinien.md` | Sichtung von LaTeX-Vorlage und Richtlinien | wissenschaftlicher-autor (sonnet) | offen |
| 2026-10-23 | `in_progress/input-uebersicht.md` | Zusammenfassung der Sichtung | Orchestrator | offen |
| 2026-10-23 | `in_progress/planung/erwartungsmanagement.md` | Strukturierung und Formulierung aus den Interviewantworten des Nutzers (Skill /ba-planung) | Orchestrator | offen |
| 2026-10-23 | `in_progress/analysen/2026-10-23_I5_com-referenz.md`, `in_progress/analysen/polytec-chm-text/` | Vertiefte Analyse der COM-Schnittstelle, Textfassung der Polytec-Hilfen | software-engineer (opus) | offen |
| 2026-10-23 | `in_progress/analysen/2026-10-23_I5F_fachpruefung-com-referenz.md` | Fachliche Prüfung der COM-Referenz | strukturdynamik-experte (sonnet) | offen |
| 2026-10-23 | `in_progress/planung/plaene/2026-10-23_E1_erkundungsskript.md` | Plan für das Erkundungsskript | software-engineer (sonnet) | offen |
| 2026-10-23 | `in_progress/analysen/2026-10-23_I5_com-referenz.md` (Überarbeitung K1) | Einarbeitung der Fachprüfung in die COM-Referenz | software-engineer (sonnet) | offen |
| 2026-10-23 | `software/` (Projektgerüst, `tools/erkundung/`, Tests) | Umsetzung Erkundungsskript E1-U und Projektgerüst | software-engineer (sonnet) | offen |
| 2026-10-24 | `software/tools/erkundung/`, Tests (Korrekturen E1-K, E1-K2) | Korrekturen nach Reviews | software-engineer (sonnet) | offen |
| 2026-10-24 | `in_progress/analysen/2026-10-23_R-E1*`, `2026-10-24_R-E1-R2*` | Code-Reviews des Erkundungsskripts | reviewer (opus) | offen |
| 2026-10-26 | `in_progress/anforderungen/lastenheft.md`, `nachverfolgung.md`, Ergänzung Erwartungsmanagement | Strukturierung der Anforderungen aus dem Interview (Skill /anforderungs-analyst) | Orchestrator | offen |
| 2026-10-26 | `Output/2026-10-26_Betreuertermin_Stand_COM.docx` | Erstellung der Meeting-Unterlage | Orchestrator | offen |
| 2026-10-26 | `in_progress/planung/plaene/2026-10-26_P3_design-brief.md`, Skizze Grunddesign | GUI-Grunddesign und Design-Brief | ui-designer (sonnet) | Grunddesign und Brief vom Nutzer freigegeben |
| 2026-10-26 | `software/src/ldv_automation/{domaene,persistenz}/`, `geraet/schnittstelle.py`, Tests | Umsetzung U1 und Korrektur K-U1 | software-engineer (sonnet) | offen (Restbefunde vom Nutzer entschieden) |
| 2026-10-26 | Review R-U1, Re-Review RR-U1 | Code-Review U1 | reviewer (opus) | Befundauswahl durch den Nutzer |
| 2026-10-26 | `software/src/ldv_automation/geraet/com/`, `tests/geraet_com/`, Prüfanleitung U3 | Umsetzung COM-Adapter U3 und Korrekturen K-U3/K-U3b | software-engineer (opus) | offen (Befundauswahl durch den Nutzer; Hardwaretest ausstehend) |
| 2026-10-26 | Review R-U3, Re-Review RR-U3 | Code-Review COM-Adapter | reviewer (opus) | Befundauswahl durch den Nutzer |
| 2026-10-26 | `software/src/ldv_automation/{ablauf,protokoll}/`, `geraet/simulator.py`, `sitzung.py`, Tests | Umsetzung U2 und Korrektur K-U2 | software-engineer (opus) | offen (Befundauswahl und Entscheidungen durch den Nutzer) |
| 2026-10-26 | Review R-U2, Re-Review RR-U2 | Code-Review Ablaufsteuerung | reviewer (opus) | Befundauswahl durch den Nutzer |
| 2026-10-27 | `software/src/ldv_automation/gui/`, `__main__.py`, `tests/gui/`, Handtest-Checkliste U4 | Umsetzung der Oberfläche U4 | software-engineer (opus) | offen (Handtest durch den Nutzer ausstehend) |
| 2026-10-27 | Design-Brief Nachtrag „Zurücksetzen“, Design-Abnahme A-U4 | Konzept und Abnahme der Oberfläche | ui-designer (sonnet) | Nachtrag vom Nutzer freigegeben |
| 2026-10-27 | Review R-U4, Re-Reviews RR-U2b/RR-U2c | Code-Review | reviewer (opus) | Befundauswahl durch den Nutzer |
| 2026-10-27 | `software/` (U5: Integration, `konfig.py`, `hatch_build.py`, Selbsttest, GUI-Anpassungen) und Tests | Umsetzung U5 und Korrekturen K-U5/K-U5b | software-engineer (opus) | offen (Befunde und Entscheidungen durch den Nutzer; Windows-/Gerätetest ausstehend) |
| 2026-10-27 | `in_progress/versuche/2026-11-02_prototyp/` (README, Installation, Ablaufplan, Protokollvorlage, Anleitung Test-.set), `software/tools/wheelhouse/` | Montagspaket P6 | software-engineer (sonnet) | offen (Durchsicht durch den Nutzer vor Montag) |
| 2026-10-27 | Review R-U5, Re-Review RR-U5, Design-Abnahme A-U5 | Prüfung U5 | reviewer (opus), ui-designer (sonnet) | Befundauswahl durch den Nutzer |
| 2026-10-28 | `in_progress/literatur/literatur.bib`, `leseliste.md` | Erste Quellensammlung für das Exposé (Paket L1) | literatur-rechercheur (sonnet) | offen (Existenz über Suchtreffer geprüft; Volltexte und Prüfung durch den Nutzer ausstehend) |
| 2026-10-29 | `in_progress/literatur/literatur.bib`, `leseliste.md` (Ergänzung L2) | Recherche Messautomatisierung und Geschichte der Strukturtests | literatur-rechercheur (sonnet) | offen (Metadaten teils unbestätigt; Volltexte ausstehend) |
| 2026-10-29 | `in_progress/planung/expose.md`, Rohfassung Kurzfassung | Rohfassung Fließtext aus den Interview-Antworten | wissenschaftlicher-autor (sonnet) | offen (Überarbeitung durch den Nutzer) |
| 2026-10-29 | `in_progress/analysen/2026-10-29_W1_auswertung-heute.md`, Literatur-Ergänzung W1 | Bestandsaufnahme der Auswertung (PSV, andere Werkzeuge, Literatur) | literatur-rechercheur (sonnet) | offen |
| 2026-10-29 | `in_progress/analysen/2026-10-29_W3_verbesserungen-auswertung.md` | Fachanalyse: Verbesserungsmöglichkeiten der Auswertung, Prüfung der .svd-Deutung | strukturdynamik-experte (opus) | offen (Auswahl A-1…A-8, B-1…B-10 durch den Nutzer am 2026-10-29) |
| 2026-10-29 | `software/tools/svd_analyse/`, Tests, `in_progress/analysen/2026-10-29_W2_svd-format.md` | Reverse Engineering und Leser für .svd, Korrekturen K-W2 | software-engineer (opus) | offen (Gegenprobe am Messrechner ausstehend) |
| 2026-10-29 | Review R-W2, Re-Review RR-W2 | Code-Review Leser | reviewer (opus) | Befundauswahl durch den Nutzer |
| 2026-10-29 | `in_progress/fachgrundlagen/FG-02_auswertung-stufe1.md` | Fachgrundlage Auswertung Stufe 1 (Formeln, Referenzfälle, Toleranzen) | strukturdynamik-experte (opus) | vom Nutzer freigegeben (2026-10-29) |
| 2026-10-30 | `software/src/ldv_automation/auswertung/`, `tools/auswertung/`, Tests, Bericht W5-1 | Umsetzung Auswertung Stufe 1 und Korrektur K-W5-1 | software-engineer (opus) | offen (Gegenprobe am Messrechner ausstehend) |
| 2026-10-30 | FG-02 Korrektur K1, Fachabnahmen FA-W5-1/FA-W5-1b | Fachliche Prüfung der Auswertung | strukturdynamik-experte (opus) | K1 vom Nutzer freigegeben |
| 2026-10-30 | Review R-W5-1, Re-Review RR-W5-1 | Code-Review Auswertung | reviewer (opus) | Befundauswahl durch den Nutzer |
| 2026-10-30 | `in_progress/fachgrundlagen/FG-03_auswertung-stufe2.md` | Fachgrundlage Auswertung Stufe 2 (Moden-Fit, Mehrfachvergleich, Normal-/Tangentialanteil) | strukturdynamik-experte (opus) | vom Nutzer freigegeben (2026-10-30, E1–E6) |
| 2026-10-30 | FG-03 Korrekturen K2 und K3, Fachabnahmen FA-W5-2, RFA-W5-2, RFA-W5-2b | Fachliche Prüfung der Auswertung Stufe 2, Korrektur der Fachgrundlage | strukturdynamik-experte (opus) | K2 und K3 vom Nutzer freigegeben |
| 2026-10-30 | `software/src/ldv_automation/auswertung/{modenfit,vergleich,bezug3d,stufe2}.py`, Tests, `tools/auswertung/beispiel_svd.py` | Umsetzung Auswertung Stufe 2 und Korrekturen K-W5-2, K-W5-2b | software-engineer (opus) | offen (Gegenprobe am Messrechner ausstehend) |
| 2026-10-30 | Review R-W5-2, Re-Review RR-W5-2 | Code-Review Auswertung Stufe 2 | reviewer (sonnet) | Befundauswahl durch den Nutzer |
