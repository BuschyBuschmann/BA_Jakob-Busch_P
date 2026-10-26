# 2026-10-26 – U3 COM-Adapter für die PSV-Software

**Art:** Arbeitspaket
**Paket/Bezug:** U3, R-U3, K-U3, K-U3b, RR-U3; Plan P2 Abschnitte 3, 6, 9; ADR-002, -003, -004, -005, -007, -008, -010; R-001
**Commit:** 1bca128 (Stand vor dem U3-Commit; der U3-Code liegt im Commit mit diesem Eintrag)
**Beteiligt:** software-engineer (opus), reviewer (opus), Orchestrator; Freigaben durch Jakob

## Ziel
Adapter `PsvComGeraet`, der die Schnittstelle `Messgeraet` über die COM-Schnittstelle der PSV-Software erfüllt, mit Whitelist-Proxy (Default deny), Richtlinie S1–S9, eigenen Enums, pywin32-Bindung und Prüfanleitung für den Test am Messrechner (Mo 2026-11-02).

## Vorgehen
1. Umsetzung U3 parallel zu U2 gegen den in K-U1 festgelegten Vertrag.
2. Review R-U3: FREIGABE MIT AUFLAGEN (MAJOR: `stoppe()` sendete nach natürlichem Scanende noch `Stop`; MINOR 1–7; Nitpicks).
3. Korrektur K-U3 (MAJOR), danach K-U3b (alle MINORs und Nitpicks, vom Nutzer freigegeben).
4. Re-Review RR-U3: FREIGABE.

## Ergebnis
- `software/src/ldv_automation/geraet/com/` (konstanten, whitelist, richtlinie, bindung, pywin32_bindung, adapter), Tests unter `software/tests/geraet_com/` mit COM-Fake.
- Prüfanleitung: `in_progress/versuche/2026-11-02_prototyp/pruefanleitung_U3_com-adapter.md` (u. a. T1 1-0 Prozesstreffer nur PSV, T4 4-1a erster State nach ScanEx, Abbruchkriterien).
- Vom Nutzer akzeptierte Planabweichungen: `Settings.Save` unter der Messdaten-Wurzel statt im Durchgangsordner; `GetApplication(False)` ohne Zeitlimit-Argument (Standard 10000 ms laut CHM); `win32com.client.dynamic.Dispatch`.

## Verifikation
- Orchestrator auf den U3-Pfaden: ruff, ruff format, mypy --strict sauber; `pytest tests/geraet_com tests/test_importrichtung.py`: 267 passed, `geraet/com` 100 % Zeilen- und Zweigabdeckung.
- Re-Review: alle Befunde am ursprünglichen Gegenbeispiel nachgeprüft; Richtlinie nach Umbau inhaltlich unverändert.
- **Nur gegen den COM-Fake geprüft, kein Hardwaretest.** Windows-Pfadlogik nur mit `ntpath` unter Linux geprüft.

## Probleme und verworfene Ansätze
- `stoppe()` las den Zustand zunächst nicht frisch und wich damit vom Simulator ab; die Tests gegen den Simulator (U2) konnten das nicht erkennen.
- Unterbrechungen durch das Nutzungslimit; Arbeitsstände blieben erhalten.

## Offene Punkte (Montag, Prüfanleitung)
- Validator-Zuweisung im dynamic-Modus, ob `ScanEx` blockiert, erster `State` nach `ScanEx`, Codec `oem` für `tasklist`, echter Prozessname von PSV.
- Gemeinsamer Typ für die Betriebsart (derzeit `ComBetriebsart` im Adapter, Abbildung durch die Sitzung).

## Thesis-Bezug
Umsetzung (Geräteanbindung, Sicherheitskonzept), Verifikation (Fake-Tests, Review), Versuche (Prüfanleitung).
