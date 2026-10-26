# Nachverfolgungsmatrix

Anforderung → Umsetzung → Test → Nachweis → Thesis-Kapitel. Wird nach jedem
abgeschlossenen Paket vom Orchestrator aktualisiert (CLAUDE.md, Abschnitt 12).
Stand: offen · in Arbeit · umgesetzt · getestet · am Gerät bestätigt · dokumentiert.

| ID | Umsetzung (Modul/Commit) | Test | Nachweis | Thesis-Kapitel | Stand |
|---|---|---|---|---|---|
| R-001 | `geraet/com/adapter.py` (U3) | `tests/geraet_com/*` (gegen COM-Fake) | Laborbuch 2026-10-26_u3; Prüfanleitung U3 | – | getestet (Fake), am Gerät offen |
| R-010 | – | – | – | – | offen |
| R-011 | `domaene/eintraege.py`, `domaene/parameter.py` (U1) | `tests/domaene/test_domaene_parameter.py`, `test_domaene_eintraege.py` | Laborbuch 2026-10-26_u1 | – | umgesetzt (Domäne; Ablauf in U2) |
| R-012 | `domaene/warteschlange.py` (U1) | `test_u1_1_*` | Laborbuch 2026-10-26_u1 | – | getestet (Domäne) |
| R-013 | `domaene/warteschlange.py` (U1) | `test_u1_2_*` | Laborbuch 2026-10-26_u1 | – | getestet (Domäne) |
| R-014 | `domaene/warteschlange.py` (U1) | `test_u1_2_*`, `test_u1_3_*` | Laborbuch 2026-10-26_u1 | – | getestet (Domäne) |
| R-015 | `domaene/warteschlange.py` (U1) | `test_u1_2_*` | Laborbuch 2026-10-26_u1 | – | getestet (Domäne) |
| R-016 | `domaene/warteschlange.py` (U1, Sperre/atomares Beanspruchen) | Mehr-Thread-Test in `test_domaene_warteschlange.py` | Laborbuch 2026-10-26_u1 | – | in Arbeit (Ablauf in U2) |
| R-017 | – | – | – | – | offen |
| R-018 | – | – | – | – | offen |
| R-019 | – | – | – | – | offen |
| R-020 | – | – | – | – | offen |
| R-021 | `persistenz/warteschlangendatei.py` (U1) | `test_u1_4_*`, `test_u1_5_*` | Laborbuch 2026-10-26_u1 | – | getestet (ohne GUI) |
| R-022 | – | – | – | – | offen |
| R-030 | – | – | – | – | offen |
| R-031 | – | – | – | – | offen |
| R-040 | – | – | – | – | offen |
| R-050 | – | – | – | – | offen |
| R-051 | – | – | – | – | offen |
| R-052 | – | – | – | – | offen |
| R-053 | – | – | – | – | offen |
| R-054 | – | – | – | – | offen |
| R-060 | – | – | – | – | offen |
| R-061 | – | – | – | – | offen |
| R-062 | – | – | – | – | offen |
