# 2026-11-03 – Auswertungsoberfläche T1: Leser im Paket, Mittelung, Laden im eigenen Prozess

**Art:** Arbeitspaket
**Paket/Bezug:** U-AUSW-T1 (Plan P-AUSW, Brief K-AUSW), Review R-AUSW-T1; R-032, R-022; ADR-020, ADR-021
**Commit:** f916f38 (Stand vor diesem Paket)
**Beteiligt:** software-engineer (sonnet), reviewer (opus)

## Ziel
Grundlage der Auswertungsoberfläche ohne GUI: Leser ins Hauptpaket, Mittelung aus der Datei, Dateieinstellungen für die Parameterzeile, Laden und Prüfen in einem eigenen Prozess (Oberfläche darf nicht einfrieren).

## Vorgehen
Umsetzung T1.1–T1.4 nach dem freigegebenen Plan, danach Review mit eigener Testausführung und Spawn-Proben.

## Ergebnis
- `svd_lesen.py` liegt jetzt in `ldv_automation/auswertung/` (vorher nur Werkzeug, nicht im Wheel); `matplotlib` und `olefile` Hauptabhängigkeiten; Gruppe `werkzeuge` entfällt.
- Wheelhouse-Pins inkl. numpy und matplotlib-Kette; der neue Abgleichtest gegen `uv.lock` fand den im Plan fehlenden Folgepin `tzdata`.
- Mittelung aus Stream `Average`: Typ 2 (komplex), Anzahl 7 – deckt sich mit File Access vom 02.11.; Einstufung „plausibel“ (eine Datei). Fenster in der Datei nicht zuordenbar → „–“.
- `Dateieinstellungen`, `lade_svd`, Mittel-Hinweise nach Fachanalyse FA-AUSW (|CPH| Betragsmittel, √AP quadratisch, 3D-Mittel „nicht gegen PSV geprüft“).
- `hintergrund.py`: eigener spawn-Prozess mit Pipe, Übertragung in Teilen ≤ 4 MiB, Abbruch; Aufträge `lese_job`, `pruef_job`, `export_job`; Messskript `zeiten_messen.py` für den Messrechner.
- Gemessen (Linux-Container, nicht Messrechner): `lese_job` 0,76 s, Abbruch 2 ms, `pruef_job` 10–12 s, längste Abfrage 20–56 ms.

## Verifikation
Review R-AUSW-T1 (opus): FREIGABE MIT AUFLAGEN, kein BLOCKER/MAJOR. Vom Reviewer bestätigt: 1713 passed, 1 skipped, 98,6 %; GUI 95 passed; ruff, mypy --strict sauber; Spawn-Proben (Abbruch während Übertragung, Prozessende ohne Ergebnis, kein Leck, keine Zombies). Golden-File und Exporte unverändert.

## Probleme und verworfene Ansätze
- `ProcessPoolExecutor` verworfen (nicht abbrechbar, 983 ms Lücke beim Senden); blockierendes Laden bricht UI-15.
- Erste Fassung hatte Ausreißer 220–340 ms beim Empfang (Zielpuffer auf einmal, Warten auf Prozessende) – behoben.
- Review: MINOR Surrogat-Zeichen im Fehlertext lassen den Fehlerkanal scheitern; NITPICKs NUL-Trennzeichen, „Exitcode None“.

## Offene Punkte
- Windows: Spawn, Pipe, Abbruch, Font-Cache, Reaktionszeit – Prüfanleitung T5; nicht als bestanden werten.
- `abbrechen()` kann bis 2 s blockieren, kein `kill`-Nachlegen.
- Zweite Messdatei mit anderem Fenster/anderer Mittelung würde Fenster lesbar bzw. Mittelung „gesichert“ machen.

## Thesis-Bezug
Umsetzung (Architektur der Auswertungsoberfläche, Nebenläufigkeit ohne Einfrieren), Validierung des Lesers.
