# To-dos und nächste Schritte

Zentrale Übersicht über offene Aufgaben der Bachelorarbeit. Wird nach jedem Arbeitsschritt
und jedem Betreuertermin aktualisiert. Details stehen in den verlinkten Dateien.

**Stand:** 2026-11-06
**Nächster fester Termin:** 12. oder 13.11.2026 am PSV-Messrechner (Termin 09.11. ausgefallen, Rechner nicht verfügbar)

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
| ✔ | P3 GUI-Grunddesign und Design-Brief → Freigabe Jakob | ui-designer, Jakob | Mi 28.10. | Grunddesign und Design-Brief freigegeben 26.10. |
| ✔ | P4 Umsetzung Prototyp in U1–U5 (U1–U5 fertig und committet) | software-engineer | Fr 30.10. | Lastenheft R-010–R-031 |
| ✔ | P5 Review und Design-Abnahme, Korrekturen | reviewer, ui-designer | Sa 31.10. | U1–U5 reviewt und abgenommen (27.10.) |
| ◐ | P6 Montags-Paket: Installationsanleitung (Python 3.11, pywin32, uv), Ablaufplan vor Ort, Protokollvorlage | software-engineer, Orchestrator | So 01.11. | Dokumente unter `in_progress/versuche/2026-11-02_prototyp/`, Durchsicht durch Jakob offen; Wheel nach letztem Commit bauen |
| ☑ | Erkundungsskript (nur lesend) mit Prüfanleitung | – | – | `software/tools/erkundung/` |
| ☐ | Vor Ort in PSV: kleine Test-Einstellungsdatei (.set, z. B. 3×3 Punkte, Generator aus) und Prüfling vorbereiten | Jakob | Mo 02.11. | Anleitung im Montags-Paket |
| ☐ | Vor Ort: Python 3.11 + pywin32 installieren; Erkundung Stufe 0 → 1 → 1b; Prototyp testen (echte Messung nur nach Bestätigung) | Jakob | Mo 02.11. | Ergebnisse nach `in_progress/versuche/erkundung/`, danach `/laborbuch` |
| ☐ | Update-Skript für den Messrechner (Version aus Git ziehen, in `C:\ldv\venv` installieren, nur Tests ohne PSV-Zugriff, Protokoll) – erst nach Klärung F30, als Paket mit Plan und Review | software-engineer | nach F30 | Wunsch Jakob 2026-11-02 |

## 3 Auswertung (Schritt 2)

| | Aufgabe | Wer | Bis | Hinweis |
|---|---|---|---|---|
| ☑ | Beispiel-Messdatei `Input/20261012_ref_Mitte.svd` erhalten; eigener .svd-Leser (W2) | – | – | `software/tools/svd_analyse/`, Laborbuch 2026-10-29 |
| ☑ | W1/W3 Auswertung heute und Verbesserungen; FG-02 (Stufe 1) freigegeben | – | – | `in_progress/analysen/`, `in_progress/fachgrundlagen/FG-02_auswertung-stufe1.md` |
| ☑ | W5-1 Auswertung Stufe 1 umgesetzt, reviewt | – | – | `software/src/ldv_automation/auswertung/`, Laborbuch 2026-10-30 |
| ☑ | FG-03 (Stufe 2: Modenfit B-1, Vergleich B-5, 3D-Bezug B-8) freigegeben mit E1–E6 | – | – | `in_progress/fachgrundlagen/FG-03_auswertung-stufe2.md` |
| ☑ | W5-2 Auswertung Stufe 2 nach FG-03 (mit Korrekturen K2, K3), Fachabnahme und Review | – | – | Laborbuch 2026-10-30_w5-auswertung-stufe2 |
| ☐ | Vor Ort: Auswertungs-Prüfungen M1–M15, Golden-File-Export, Band-Cursor-Fit 401,6/618,9 Hz | Jakob | Mo 02.11. | Ablaufplan 7b, Protokoll 6b |
| ☐ | Vor Ort: Wiederholungsmessung (T8) für B-5, möglichst auch mit neu abgeglichenem Raster | Jakob | Mo 02.11. | Ablaufplan 8, nur nach eigener Entscheidung |
| ❗ | **Frequenzachse korrigieren:** Polytec File Access liefert für `20261012_ref_Mitte.svd` Δf = 0,625 Hz, 0,625 … 1000 Hz (1600 Linien), nicht 1,5625 … 2500 Hz. Leser (`svd_lesen.py`), FG-02/FG-03 (Sollwerte in Hz, Abschnitt 7), Befunde W5 neu; ζ, MAC, Amplituden unverändert | strukturdynamik-experte, software-engineer | nach 02.11. | Erkundung 1b 2026-11-02 16:11, PSV-RMS 1,349 mm/s = CPH über alle 1600 Linien |
| ☑ | PSV-Einblicke vom 02.11. ausgewertet; Übersicht und Entscheidungen | – | – | `in_progress/analysen/2026-11-02_nach-termin_uebersicht.md` |
| ☑ | P1 Laborbuch 02.11., Tagesanalyse, Register | – | – | 1ed1172 |
| ☑ | P2 K-ACHSE abgeschlossen (Fachabnahme, Review, Auflagen) | – | – | Laborbuch 2026-11-02_k-achse-frequenzachse |
| ◐ | Recherche R-0211: Peak-Anpassung und SE belegt; **PCB 288D01 und Decoder: Volltext von Jakob benötigt** (Input/literatur/pcb/, Leseliste) | Jakob, literatur-rechercheur | – | M8 bis dahin offen |
| ☑ | P4/P4b Lese-Skripte korrigiert und reviewt | – | – | 4279382, 0129b75 |
| ☑ | P3 Ablaufplan nächster Termin mit Ersatzplänen und Prüfzettel, fachlich durchgesehen und freigegeben (`in_progress/versuche/naechster-termin_messrechner/`) (Übersicht 2a: Registrierung, Mini-Scan mit Zeitdaten, Messpunkt Impedanzkopf, Zwei-Amplituden-Test, Wiegen, Handbücher, M11 ohne Kennzeichen, Golden v2 …) | software-engineer, `/versuchsplanung` | nach P1 | |
| ☑ | Wheel 0.2.0 gebaut (f66af80, sauber; ersetzt durch Build a0ee2fc), mit Skripten und SHA-256 abgelegt | – | – | `in_progress/versuche/naechster-termin_messrechner/stick/LIESMICH.txt` |
| ☐ | Fragen F1–F8 an Daniel (Ablaufplan 3.2) | Jakob | vor Termin | |
| ☑ | R-023 (Frequenzachse im Protokoll) und R-055 (Dämpfung mit Band und Methode) umgesetzt, reviewt | – | – | Laborbuch 2026-11-03_r023-r055 |
| ◐ | Auswertungsoberfläche (R-032, Ablauf C): Brief K-AUSW und Plan P-AUSW freigegeben; T1–T5 fertig in der Cloud (letzter Stand a0ee2fc); Prüfung am Messrechner offen | ui-designer, software-engineer | – | Plan P-AUSW |
| ☑ | T5: Meldezeile behoben, Installationsweg (`installation_0.2.0.md`) und Prüfanleitung, Wheel 0.2.0 neu gebaut (a0ee2fc, SHA-256 68221a3c…) mit 12 neuen Abhängigkeits-Wheels auf dem Stick | Orchestrator, software-engineer | – | Laborbuch 2026-11-05_auswerten-t5 |
| ☐ | Am Messrechner: `installation_0.2.0.md` N1–N7, `pruefanleitung_auswerten.md` W1–W10, `zeiten_messen.py` | Jakob | nächster Termin | `naechster-termin_messrechner/` |
| ☐ | Am Gerät: Einheiten SampleResolution/SampleTime, `Lines` bei Von/Bis (für R-023/R-024) | Jakob | nächster Termin | |
| ☑ | Anforderungsvorschläge aus PSV-Einblicken ins Lastenheft (R-002, R-023, R-024, R-032, R-055–R-057; O7, O8 neu) | – | – | Nutzerentscheidung 03.11. |
| ☑ | Datenweg entschieden: ADR-020 (eigener Leser, File Access als Gegenprobe), ersetzt ADR-006 | – | – | Nutzerentscheidung 03.11. |
| ☑ | Kleine Code-Aufgaben aus PSV-Einblicken (Übersicht 2d), reviewt; MINORs zur Entscheidung, Gerätetest offen | – | – | Laborbuch 2026-11-02_k2d-psv-einblicke-code |
| ☑ | KONVENTIONEN-Vorschläge übernommen (Achse, Polarität vorläufig, Proxy-Ausnahme, Termine, Version); Thesis-Bausteine in kapitel-map | – | – | b29584e |
| ☐ | Nach Montag: M1–M15 in FG-02/FG-03 nachführen, Golden-File-Test, Abbildungen mit sauberem Git-Hash neu erzeugen | Orchestrator, strukturdynamik-experte | nach 02.11. | |
| ☑ | Abbildungsskript für Thesis-Abbildungen (alle 4 Ansichten, Manifest, Git-Regel; ADR-027) | software-engineer | – | Laborbuch 2026-11-06_abbildungsskript |
| ☐ | Nach 09.11.: .svd-Dateien R/A/B und T4–T6 ins Repo, Abbildungen in der Cloud erzeugen (`darstellung_beispiel.py`), Sichtprüfung durch Jakob | Jakob, Orchestrator | nach 09.11. | ADR-027 |
| ☐ | Möglicher Auftrag: Hash-Quelle in `protokoll/version.py` robust machen (venv in fremdem Git-Repo) | software-engineer | nach Prüfung am 09.11. | Laborbuch 2026-11-06 |
| ☐ | Versuch Prüfdateien/Warteschlange durchführen (09.11. ausgefallen; Ordner beim Termin umbenennen) | Jakob | 12./13.11. | `in_progress/versuche/2026-11-09_pruefdateien-warteschlange/`, `checkliste_montag.md` |
| ☐ | Vorgaben B1–B10 aus dem Betreuertermin 09.11. ins Lastenheft (`/anforderungs-analyst`), dann planen | Orchestrator, Jakob | – | Laborbuch 2026-11-09_betreuertermin-daniel |
| ◐ | B10 Recherche erledigt (FA-B10: Empfehlung V1–V7; R-B10: 24 Quellen, Prüfstand metadaten); mit Daniel klären: FE-Modell vorhanden (V6)? Fremdbibliothek als Gegenprobe (V7)? Danach Lastenheft | Jakob, Orchestrator | 12./13.11. | `in_progress/analysen/2026-11-09_FA-B10_auswertung-ueber-psv-hinaus.md` |
| ☐ | Volltexte nach `Input/literatur/` (mind. Priorität A: peeters2004polymax, rohe2020alignment; Liste in leseliste.md) | Jakob | – | Leseliste R-B10 |
| ☐ | Fragen an Daniel: A1–A6 (Abgleich), W1–W8 (Benachrichtigung), O11 (KOS-Transformation), O12 (PSV-Ansichten) | Jakob | 12./13.11. | Analyse A1-B13, Lastenheft |
| ☐ | Am Messrechner: Abgleich einmal lesen (`P1-6-abgleich`), Typbibliothek der PolyAlignment-Typen auslesen | Jakob | 12./13.11. | Analyse A1-B13 |
| ◐ | Auswerten-Erweiterung: Etappe A (R-073), Etappe B (R-058), Abgleich (R-003a/b) und Animations-Rechenkern fertig; Etappe C (R-059, S8–S10) und Animation AN3–AN9 folgen | Orchestrator | – | Pläne P-AUSW2, P-AUSW3, P-R003 |

## 4 Thesis

| | Aufgabe | Wer | Bis | Hinweis |
|---|---|---|---|---|
| ◐ | P8 Gliederung: Entwurf freigegeben (`in_progress/planung/gliederung.md`), Abstimmung mit Daniel offen (Fragen G1–G4) | `/ba-planung`, Jakob | nächster Betreuertermin | Kapitel-Zuordnung aktualisiert |
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
| **F30** | **Fernzugriff auf den Messrechner (VPN + Remotedesktop) erlaubt? Darf der Messrechner ins Internet bzw. auf GitHub?** (Voraussetzung für Updates aus der Ferne) |

Vollständige Liste: `in_progress/planung/erwartungsmanagement.md`, Abschnitt 9.

## Wichtige Dateien

- Lastenheft: `in_progress/anforderungen/lastenheft.md`
- Erwartungsmanagement: `in_progress/planung/erwartungsmanagement.md`
- COM-Referenz: `in_progress/analysen/2026-10-23_I5_com-referenz.md`
- Laborbuch: `in_progress/laborbuch/`
- Software: `software/`
