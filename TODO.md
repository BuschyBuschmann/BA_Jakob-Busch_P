# To-dos und nächste Schritte

Zentrale Übersicht über offene Aufgaben der Bachelorarbeit. Wird nach jedem Arbeitsschritt
und jedem Betreuertermin aktualisiert. Details stehen in den verlinkten Dateien.

**Stand:** 2026-10-26 (nach dem ersten Betreuertermin)
**Nächster fester Termin:** Mo 2026-11-02 – Arbeit am PSV-Messrechner

Legende: ☐ offen · ◐ in Arbeit · ☑ erledigt · ⏳ wartet auf andere

---

## 1 Organisatorisches

| | Aufgabe | Wer | Bis | Hinweis |
|---|---|---|---|---|
| ⏳ | Schreiben von Daniel Alboldt für die vorzeitige Anmeldung abwarten | Daniel | – | |
| ☐ | Antrag auf vorzeitige Anmeldung beim Prüfungsausschuss WIMB stellen (Situation erklären) | Jakob | nach Erhalt des Schreibens | |
| ☐ | Termin und Rhythmus der Betreuertermine festlegen (F2) | Jakob, Daniel | – | Erwartungsmanagement |

## 2 Vorbereitung Messrechner (Mo 2026-11-02)

Ziel: Schnittstellendaten am echten Gerät lesen und verstehen, ersten Prototyp testen.

| | Aufgabe | Wer | Bis | Hinweis |
|---|---|---|---|---|
| ☑ | P1 GUI-Technologie: PySide6/Qt (ADR-001) | – | – | `in_progress/entscheidungen/ADR-001_gui-technologie.md` |
| ☑ | P2 Architekturplan Prototyp freigegeben, ADR-002 bis ADR-012 angelegt | – | – | `in_progress/planung/plaene/2026-10-26_P2_architektur-prototyp.md` |
| ◐ | P3 GUI-Grunddesign und Design-Brief → Freigabe Jakob | ui-designer, Jakob | Mi 28.10. | |
| ◐ | P4 Umsetzung Prototyp in U1–U5 (U1 Kern-Domäne läuft) | software-engineer | Fr 30.10. | Lastenheft R-010–R-031 |
| ☐ | P5 Review und Design-Abnahme, Korrekturen | reviewer, ui-designer | Sa 31.10. | |
| ☐ | P6 Montags-Paket: Installationsanleitung (Python 3.11, pywin32, uv), Ablaufplan vor Ort, Protokollvorlage | software-engineer, Orchestrator | So 01.11. | |
| ☑ | Erkundungsskript (nur lesend) mit Prüfanleitung | – | – | `software/tools/erkundung/` |
| ☐ | Vor Ort in PSV: kleine Test-Einstellungsdatei (.set, z. B. 3×3 Punkte, Generator aus) und Prüfling vorbereiten | Jakob | Mo 02.11. | Anleitung im Montags-Paket |
| ☐ | Vor Ort: Python 3.11 + pywin32 installieren; Erkundung Stufe 0 → 1 → 1b; Prototyp testen (echte Messung nur nach Bestätigung) | Jakob | Mo 02.11. | Ergebnisse nach `in_progress/versuche/erkundung/`, danach `/laborbuch` |

## 3 Auswertung (Schritt 2)

| | Aufgabe | Wer | Bis | Hinweis |
|---|---|---|---|---|
| ⏳ | PSV-Datei einer fertigen Messung von Daniel erhalten und nach `Input/` hochladen | Daniel, Jakob | – | |
| ☐ | Datei am Messrechner mit Erkundung Stufe 1b lesen; zusätzlich in PSV als UFF exportieren | Jakob | Mo 02.11. | |
| ☐ | P7 Sichtung der Messdatei, Vorschlag: welche Auswertungen und wie | strukturdynamik-experte | nach Eingang | Lastenheft R-050–R-054 |
| ☐ | Fachgrundlage FG-01 Spektralauswertung nach Polytec-Konvention | strukturdynamik-experte | nach P7 | |

## 4 Thesis

| | Aufgabe | Wer | Bis | Hinweis |
|---|---|---|---|---|
| ⏳ | P8 Entwurf Inhaltsverzeichnis (Gliederung) – wartet auf die Orga-/To-do-Datei von Daniel | `/ba-planung`, Jakob | diese Woche | SLA-Vorlage |
| ⏳ | Orga-/To-do-Datei von Daniel erhalten (angefragt) und in `Input/` hochladen; danach Gliederung starten | Daniel, Jakob | – | |
| ☐ | P8 Zeitplan mit Meilensteinen (sobald Abgabetermin bekannt) | `/ba-planung`, Jakob | nach Anmeldung | |
| ☐ | P8 Glossar-Grundgerüst (Abkürzungen, Formelzeichen) | wissenschaftlicher-autor | nach Gliederung | |
| ☐ | Klären: aktuelle LaTeX-Vorlage und Logo (F14), gültige Formalien (F13) | Jakob, Daniel | – | |

## 5 Offene Fragen an den Betreuer (Auswahl)

| Nr. | Frage |
|---|---|
| **F20** | **Was passiert, wenn eine Messung der Warteschlange fehlschlägt?** (im Prototyp vorläufig: pausieren und nachfragen) |
| F1 | Bearbeitungszeit und Abgabetermin |
| F5 | PSV-Version, lizenzierte Optionen, Polytec File Access installiert? |
| F10 | Wird die Anregungskraft gemessen? |
| F11 | Zulässiger KI-Einsatz und Kennzeichnung |
| F13 | SLA-Vorlage oder Richtlinien-PDF? |

Vollständige Liste: `in_progress/planung/erwartungsmanagement.md`, Abschnitt 9.

## Wichtige Dateien

- Lastenheft: `in_progress/anforderungen/lastenheft.md`
- Erwartungsmanagement: `in_progress/planung/erwartungsmanagement.md`
- COM-Referenz: `in_progress/analysen/2026-10-23_I5_com-referenz.md`
- Laborbuch: `in_progress/laborbuch/`
- Software: `software/`
