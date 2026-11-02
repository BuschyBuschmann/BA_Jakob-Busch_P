# 2026-11-02 – Erster Termin am Messrechner (Installation, Erkundung, Auswertungs-Prüfungen)

**Art:** Hardwaretest (teilweise) und Laborversuch (Prüfung der Auswertung an PSV); 14:30–17:00
**Paket/Bezug:** P6 (Montags-Paket), Ablaufplan `in_progress/versuche/2026-11-02_prototyp/ablaufplan_vor_ort.md`; FG-02/FG-03 (M1–M15); R-001, R-022, R-050–R-053
**Commit:** Software am Messrechner: Wheel 530af41 (Build-Info `git_dirty: false`); Repo-Stand vor diesem Eintrag a5f73a9
**Beteiligt:** Jakob am Messrechner (Rechner BEOWOLF); Orchestrator direkt (Arbeitsweise „Termin vor Ort“, KONVENTIONEN); danach Prüfung durch reviewer (sonnet, P0a), strukturdynamik-experte (opus, P0b; sonnet, E-PSV-F), software-engineer (sonnet, E-PSV-S)

## Ziel
Laut Ablaufplan: Software installieren (I1–I7), Erkundung Stufe 0/1, Schalter und Konfigurationsdatei, Prototyp-Prüfung T0–T2 am Gerät; als Soll die Auswertungs-Prüfungen 7b (Annahmen M1–M15 aus FG-02/FG-03).

## Vorgehen
1. Installation über eine PyCharm-venv (`D:\Messdaten\DAL\BA Jakob Busch\PyCharmProject\.venv`), Pakete aus dem Internet statt vom Wheelhouse (Weg B); pywin32 312 zunächst vergessen, nachinstalliert. Prüfschritte I1–I7 (Selbsttest 14:47, GUI-Simulator).
2. Erkundung Stufe 0 (14:32 mit zwei PSV-Prozessen und ohne pywin32; 15:00 erneut).
3. Ursachensuche zur fehlenden COM-Registrierung (Registry, Programmordner, Startverknüpfungen, Release Notes PSV 10.4); Anleitung zur Registrierung erstellt.
4. PSV-Info und Optionen; Fotos von Aufbau, Impedanzkopf und Shaker.
5. Auswertungs-Prüfungen an Kopien von `20261012_ref_Mitte.svd`: Erkundung Stufe 1b (Polytec File Access, 16:11), Lese-Skripte `einstellungen_lesen.py` und `daten_lesen.py` (Golden File Label 132), PSV-Analysator (Einzelner Scanpunkt, Band-Cursor mit Peak-Anpassung).

## Ergebnis
- **Installation:** I1–I7 bestanden (Python 3.11.9, 64 Bit, alle Pakete, `win32com ok`, Selbsttest bestanden, Git-Hash 530af419, GUI-Simulator mit Symbolen; ⏸ als Windows-Emoji).
- **PSV-COM nicht registriert:** keine ProgID `PSV.AcquisitionInstance`/`PresentationInstance`/`Application`, keine „Polytec PSV Type Library“ (Erkundung 143255, 150024). Installiert sind PSV 10.2, 10.3, 10.4 parallel; laufend 10.4.0.1. Release Notes 10.4: bei parallel installierten Versionen `PSV.exe /regserver` als Administrator bzw. Reparaturinstallation. Anleitung: `in_progress/versuche/2026-11-02_prototyp/com_registrierung_psv104.md`. Lizenz für Automatisierung vorhanden (PSV-S-VBEng); weitere Optionen u. a. TDD (Zeitdaten), SIG, Acq3D; keine PCA.
- **Startmodi:** „PSV 10.4 Deutsch“ = `/Acquisition`, „PSV 10.4 Desktop Deutsch“ = `/Desktop`.
- **Frequenzachse der Auswertung falsch:** Datei hat Δf = 0,625 Hz, 0,625–1000 Hz, 1600 Linien, Abtastrate 2500 Hz, Blockdauer 1,6 s (File Access XAxis/GetMidX, Erfassungseinstellungen, PSV-Statusleiste „1 kHz · 1600 · 1.6 s · 625 mHz“). Der eigene Leser nahm 1,5625 Hz und 2500 Hz an (Faktor 2,5).
- **Eigener Leser gegen PSV bestätigt:** Spektren Vib X/Y/Z an Label 132 bitgleich, H1 auf ≤ 5,8·10⁻⁸ (Golden File `golden_punkt1_label132.csv`, 6 von 8 Signalen).
- **Annahmen:** M1, M2 (Achse korrigieren), M4, M5, M6, M10 bestätigt; M7 erledigt; M12 nur „Leser = PSV“; M8 offen (relative Polarität Ref1/Ref2 invertiert, achsunabhängig); M11 teilweise; M13 plausibel; M14, M15 offen. Einzelheiten: `in_progress/versuche/2026-11-02_prototyp/ergebnisse_7b.md`.
- **PSV-Peak-Anpassung (Label 132, Z):** 160,7 Hz / ζ 1,319·10⁻³ (Band 158,8–163,8 Hz) bzw. 1,242·10⁻³ (159,4–162,5 Hz); 247,7 Hz / ζ 1,321·10⁻³ (245,6–250,6 Hz). Eigener Fit am selben Punkt und Band (nachgerechnet, P0b): ζ +5 … +9 %. Beide Spitzen sind auflösungsbegrenzt.
- **Aufbau:** Blech frei an zwei Seilen, keine Berührung unten; drei PSV-Scanköpfe; Impedanzkopf PCB 288D01 SN 3853, richtig montiert, Kraft → Ref1 (40,31 N/V), Beschleunigung → Ref2 (97,85 (m/s²)/V); TMS Mini SmartShaker (Typschild teilweise lesbar) mit eingebautem Verstärker.
- **Nicht erreicht:** Erkundung Stufe 1 gegen PSV, Schalter/Konfigurationsdatei, Test-.set, T0–T2 und alle Messungen (blockiert durch fehlende COM-Registrierung bzw. nicht begonnen). Kein Hardwaretest der Software am Gerät bestanden.

## Verifikation
- Nachgeprüft durch Fachanalyse P0b (Achse mehrfach unabhängig bestätigt, u. a. Integration in PSV mit ω = 2π·0,625·k und Zeitstempel-Regression T = 1,600 ± 0,017 s) und Review P0a der Lese-Skripte (FREIGABE MIT AUFLAGEN, Korrektur läuft). Zusammenfassung: `in_progress/analysen/2026-11-02_nach-termin_uebersicht.md`.
- Erkundungsberichte: `in_progress/versuche/erkundung/erkundung_BEOWOLF_2026-11-02_143255`, `…_150024`, `…_161125`.

## Probleme und verworfene Ansätze
- Wheelhouse/Stick war nicht vorbereitet; die Wheels fehlten zunächst in Git (vom Build angelegte `.gitignore`), numpy fehlte in der Installationsanleitung.
- Installation wich von der Anleitung ab (PyCharm-venv, Internet, pywin32 vergessen).
- Die COM-Registrierung war vorher nicht geprüft; Daniel war beim Befund nicht verfügbar. Der Prototyp konnte deshalb nicht am Gerät getestet werden.
- Zeitweise liefen zwei PSV-Instanzen.
- Die Spektrumansicht in PSV zu finden kostete deutlich Zeit.
- Die Frequenzachse war in W2 nur „plausibel/vorläufig“ belegt (Zirkelschluss über das Feld „Blockdauer 0,64 s“) und wurde trotzdem in Stufe 1 und 2 übernommen.
- Meine Vermutung vor Ort, der Vorzeichenbefund (P-08) sei eine Folge der falschen Achse, hat sich als falsch erwiesen (P0b).
- Erkenntnis des Nutzers: Beim nächsten Termin muss variabler reagiert werden können, wenn etwas wie die COM-Schnittstelle nicht funktioniert.

## Offene Punkte
- COM-Registrierung: Jakob klärt mit Daniel; bis zum nächsten Live-Termin durchgeführt.
- Korrektur der Frequenzachse (K-ACHSE) läuft; M8-Polarität über Datenblatt PCB 288D01 und Kontrollversuch.
- Nächster Termin: Ablaufplan mit Ersatzplänen und Prüfzettel (u. a. Mini-Scan mit Zeitdaten, Messpunkt auf dem Impedanzkopf, Zwei-Amplituden-Test, Wiegen, Handbücher 10.4, M11 an Spitzen ohne Kennzeichen, M13–M15).
- Fragen an Daniel: `in_progress/versuche/2026-11-02_prototyp/rueckfragen_heute.md` (A1–A6).

## Dateien
- Fotos (Aufbau, Impedanzkopf, Shaker) und PSV-Screenshots: [fotos/](../versuche/2026-11-02_prototyp/fotos/)
- Tagesanalyse: [tagesanalyse.md](../versuche/2026-11-02_prototyp/tagesanalyse.md)
- Ergebnisse 7b: [ergebnisse_7b.md](../versuche/2026-11-02_prototyp/ergebnisse_7b.md), Golden File: [golden_punkt1_label132.csv](../versuche/2026-11-02_prototyp/golden_punkt1_label132.csv)

## Thesis-Bezug
Umsetzung und Inbetriebnahme am Messrechner; Bewertung der Schnittstelle (Registrierung, Startmodi); Verifikation des eigenen Datenwegs (Golden File); Achsenfehler als dokumentierter Fehlschlag; Grenzen der PSV-Dämpfungsschätzung; Versuchsaufbau.
