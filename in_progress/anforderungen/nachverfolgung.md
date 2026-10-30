# Nachverfolgungsmatrix

Anforderung → Umsetzung → Test → Nachweis → Thesis-Kapitel. Wird nach jedem
abgeschlossenen Paket vom Orchestrator aktualisiert (CLAUDE.md, Abschnitt 12).
Stand: offen · in Arbeit · umgesetzt · getestet · am Gerät bestätigt · dokumentiert.

| ID | Umsetzung (Modul/Commit) | Test | Nachweis | Thesis-Kapitel | Stand |
|---|---|---|---|---|---|
| R-001 | `geraet/com/adapter.py` (U3) | `tests/geraet_com/*` (gegen COM-Fake) | Laborbuch 2026-10-26_u3; Prüfanleitung U3 | – | getestet (Fake), am Gerät offen |
| R-010 | `ablauf/steuerung.py` (U2) | `test_u2_1_*` | Laborbuch 2026-10-26_u2 | – | getestet (Simulator) |
| R-011 | `domaene/eintraege.py`, `domaene/parameter.py` (U1) | `tests/domaene/test_domaene_parameter.py`, `test_domaene_eintraege.py` | Laborbuch 2026-10-26_u1 | – | umgesetzt (Domäne; Ablauf in U2) |
| R-012 | `domaene/warteschlange.py` (U1) | `test_u1_1_*` | Laborbuch 2026-10-26_u1 | – | getestet (Domäne) |
| R-013 | `domaene/warteschlange.py` (U1) | `test_u1_2_*` | Laborbuch 2026-10-26_u1 | – | getestet (Domäne) |
| R-014 | `domaene/warteschlange.py` (U1) | `test_u1_2_*`, `test_u1_3_*` | Laborbuch 2026-10-26_u1 | – | getestet (Domäne) |
| R-015 | `domaene/warteschlange.py` (U1) | `test_u1_2_*` | Laborbuch 2026-10-26_u1 | – | getestet (Domäne) |
| R-016 | `domaene/warteschlange.py` (U1), `ablauf/steuerung.py` (U2) | `test_u2_2_*`, Mehr-Thread-Test U1 | Laborbuch 2026-10-26_u1, _u2 | – | getestet (Simulator) |
| R-017 | `ablauf/steuerung.py` (U2) | `test_u2_3_*` | Laborbuch 2026-10-26_u2 | – | getestet (Simulator) |
| R-018 | `ablauf/steuerung.py` (U2) | `test_u2_4_*` | Laborbuch 2026-10-26_u2 | – | getestet (Simulator) |
| R-019 | `ablauf/fehlerstrategie.py` (U2, vorläufig) | `test_u2_5_*`, `test_u2_6_*` | Laborbuch 2026-10-26_u2 | – | vorläufig umgesetzt (O1 offen) |
| R-020 | `protokoll/messprotokoll.py` (U2), Konfiguration und Build-Info (U5) | `test_u2_10_*`, `tests/test_konfig.py`, `test_build_info.py` | Laborbuch 2026-10-26_u2, 2026-10-27_u5 | – | getestet (Simulator) |
| R-021 | `persistenz/warteschlangendatei.py` (U1) | `test_u1_4_*`, `test_u1_5_*` | Laborbuch 2026-10-26_u1 | – | getestet (ohne GUI) |
| R-022 | `software/tools/svd_analyse/svd_lesen.py` (W2, Prototyp) | `tests/tools/svd_analyse/*` (72 Plausibilitätsprüfungen an der Beispieldatei) | Laborbuch 2026-10-29_w2 | – | in Arbeit (Gegenprobe gegen PSV am Messrechner offen) |
| R-030 | `gui/` (U4) | `tests/gui/*` (gui-Marker), Handtest-Checkliste U4 | Laborbuch 2026-10-27_u4 | – | umgesetzt (Handtest offen) |
| R-031 | `sitzung.py` (U2), `gui/anzeige.py`, `gui/tabelle.py` (U4) | `test_u2_12_*`, UI-7/UI-8 | Laborbuch 2026-10-26_u2, 2026-10-27_u4 | – | getestet (Simulator) |
| R-040 | – | – | – | – | offen |
| R-050 | `auswertung/spektren.py`, `mittel.py` (W5-1) | RF-S, RF-B, Golden File (Punktmittel 35/35) | Laborbuch 2026-10-30_w5 | – | getestet (Datei; PSV-Anzeige offen) |
| R-051 | `auswertung/frf.py` (W5-1) | RF-H, RF-U, RF-G, Bandnorm H1 | Laborbuch 2026-10-30_w5 | – | getestet (Datei; PSV-Anzeige offen) |
| R-052 | `auswertung/schwingform.py` (W5-1) | RF-3D, RF-W | Laborbuch 2026-10-30_w5 | – | getestet (Phasenbezug M1/M8 offen) |
| R-053 | `auswertung/spitzen.py`, `baender.py` (W5-1); Dämpfung zusätzlich per Modenfit `auswertung/modenfit.py` (W5-2) | RF-P, RF-M, RF-K, Golden File (Bänder 22/22); RF-F1–F9 | Laborbuch 2026-10-30_w5, 2026-10-30_w5-auswertung-stufe2 | – | getestet (Datei; PSV-Fit-Vergleich offen) |
| R-054 | Plausibilität P-01–P-11 (W5-1); Vergleich von Messungen und Drift `auswertung/vergleich.py`, 3D-Bezug `auswertung/bezug3d.py` (W5-2) | RF-V1–V7, RF-G1–G5 | Laborbuch 2026-10-30_w5-auswertung-stufe2 | – | in Arbeit (Umfang am Entscheidungspunkt; B-5 nur synthetisch, zweite Messung Mo 02.11.) |
| R-060 | `pyproject.toml` (`requires-python >=3.11,<3.12`) | gesamte Testsuite unter Python 3.11 | Laborbuch 2026-10-27_u4 | – | umgesetzt |
| R-061 | `geraet/simulator.py` (U2), COM-Fake (U3) | gesamte Testsuite | Laborbuch 2026-10-26_u2, _u3 | – | umgesetzt |
| R-062 | Standard-Prüfung aus KONVENTIONEN | ruff, mypy --strict, pytest ≥ 90 % (97,95 %) | Laborbuch 2026-10-27_u5 | – | umgesetzt |
