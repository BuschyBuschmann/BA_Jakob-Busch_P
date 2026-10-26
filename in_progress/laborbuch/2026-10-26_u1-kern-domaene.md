# 2026-10-26 – U1 Kern-Domäne der Mess-Warteschlange

**Art:** Arbeitspaket
**Paket/Bezug:** U1, K-U1, R-U1, RR-U1; Plan P2 (`in_progress/planung/plaene/2026-10-26_P2_architektur-prototyp.md`); R-011–R-016, R-021
**Commit:** d397166 (Stand vor dem U1-Commit; der U1-Code liegt im Commit mit diesem Eintrag)
**Beteiligt:** software-engineer (sonnet), reviewer (opus), Orchestrator; Freigaben durch Jakob

## Ziel
Domänenkern der Warteschlange (Einträge, Zustände, Parameterkatalog, threadsichere Warteschlange), gemeinsame Geräteschnittstelle `Messgeraet` für Simulator (U2) und COM-Adapter (U3) sowie Speichern/Laden der Warteschlange.

## Vorgehen
1. Umsetzung U1 nach Plan P2 (Module `domaene/`, `geraet/schnittstelle.py`, `persistenz/warteschlangendatei.py`, Importrichtungstest).
2. Review R-U1: NACHARBEIT NÖTIG (MAJOR-1: Vertrag `Messgeraet` an vier Stellen offen; MINOR-1 bis -5; NITPICK-1 bis -5).
3. Vertragsfestlegung durch den Orchestrator aus Plan M10/2.6/6: `stoppe() -> bool` nicht blockierend (Polling mit Frist in der Steuerung), No-op ohne eigenen Scan, `GeraetNichtBereitFehler`, Betriebsart bei Konstruktion. U2 und U3 wurden sofort informiert.
4. Jakob gab MINOR-1, -2, -3, -5 zur Korrektur frei (MINOR-4 und NITPICKs bleiben offen).
5. Korrektur K-U1, Re-Review RR-U1: FREIGABE MIT AUFLAGEN. Jakob: Restbefunde so lassen, committen.

## Ergebnis
- `software/src/ldv_automation/domaene/` (parameter, eintraege, warteschlange), `geraet/schnittstelle.py`, `persistenz/warteschlangendatei.py`, Tests unter `software/tests/{domaene,geraet,persistenz}/`, `tests/test_importrichtung.py`.
- Parameterkatalog: `fft.bandbreite_hz` (> 0), `fft.linien` (≥ 1, ohne Obergrenze), `mittelung.anzahl` (3…10000, aus I5 [BEM], am Gerät unbestätigt), `mittelung.typ` (PTCAverageType-Namen).
- `GeraeteInfo.lademaske` für das Messprotokoll.

## Verifikation
- Re-Review auf U1-Pfaden: ruff, ruff format, mypy --strict sauber; 209 Tests, 100 % Zeilen- und Zweigabdeckung für domaene, persistenz, schnittstelle.
- Gesamtprüfung des Pakets (mit U2/U3-Dateien im Arbeitsstand) vom Orchestrator ausgeführt: 745 passed, 97,44 % Abdeckung, ruff/mypy grün.
- Keine Hardwareprüfung.

## Probleme und verworfene Ansätze
- Erste Fassung der Schnittstelle ließ Stop-Semantik, Fehlerklasse bei fremder Messung und Betriebsart offen; U2 und U3 hätten parallel unvereinbar gebaut. Festgelegt vor deren Fertigstellung.
- Der Umsetzer ließ in K-U1 `ruff --fix`/`ruff format` über ganz `software/` laufen, während U2/U3 schrieben; beide wurden zum Neueinlesen aufgefordert.
- Unterbrechungen durch das Nutzungslimit und einen Neustart des Containers; Arbeitsstände blieben erhalten.

## Offene Punkte
- MINOR (Re-Review): Ganzzahlen mit mehr als 4300 Stellen ergeben ValueError ohne Feld-/Dateibezug.
- NITPICK: `stimmt_ueberein(inf, inf)` ergibt True (über normale Pfade nicht erreichbar).
- MINOR-4 (Hashbarkeit/Mappings) und NITPICK-1 bis -5 aus R-U1.
- Obergrenze für `fft.linien`: nach der Erkundung am Messrechner festlegen.
- Pausenpunkt in einem zweiten Durchgang (derzeit übersprungen) nicht spezifiziert.

## Thesis-Bezug
Konzept/Architektur (Domänenmodell, Zustandsmodell, Geräteschnittstelle), Umsetzung, Verifikation (Teststrategie, Review).
