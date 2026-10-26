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
