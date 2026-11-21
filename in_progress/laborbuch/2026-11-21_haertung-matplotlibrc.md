# 2026-11-20/21 – Oberfläche und Abbildungen gegen fremde matplotlibrc gehärtet

**Art:** Arbeitspaket (Folge mehrerer Pakete)
**Paket/Bezug:** K-GUI6, U-HAERTUNG, K-HAERTUNG, K2-HAERTUNG, K3-HAERTUNG, U-HAERTUNG-3D, K-HAERTUNG-3D mit Reviews; R-059, R-071; KONVENTIONEN 2026-11-20/21
**Commit:** e3e1a55 (Stand vor dem Abschluss-Commit; Zwischenstände 7b3e7ed, e5f6976, af68760, bdbf028, a5b1888, e3e1a55)
**Beteiligt:** software-engineer (sonnet), reviewer (opus); Entscheidungen Jakob Busch

## Ziel
Sechs GUI-Tests scheiterten in einem neuen Cloud-Container; Ursache klären und beheben. Danach auf Wunsch des Nutzers die App so härten, dass eine fremde `matplotlibrc` auf Messrechner oder privatem Rechner Oberfläche und Abbildungen nicht verändert.

## Vorgehen
1. Ursache belegt: `/etc/matplotlib/matplotlibrc` im Container mit `figure.dpi: 200`, `text.hinting: no_hinting`, `font.family: Inter…` – Plotschriften doppelt so groß, Plots bei 1100×680 zu klein. Nicht die Systemschrift (Gegenprobe). GUI-Tests laufen seither mit `rcdefaults()`.
2. App-Härtung: Figures der Oberfläche und des Exports mit fester DPI 100, PDF mit expliziter DPI; Schriftfamilie und Text-/Achsenfarben aus dem Stil; Animation zeichnet auf dem Bildschirm im Stil-Kontext (`_StilCanvas`); 3D-Animation mit Standardwerten für Gitter, Wände, Linien, Ticks, Hinting (`STANDARD_RC_SCHLUESSEL`); 3D-Gitterfarbe aus `Plotstil.gitter_3d` (App Token #E1E3E5, Thesis #b0b0b0, Nutzerentscheidung).
3. Nebenbei: flackernder Layouttest deterministisch gemacht (Testtiming), Einheitenlabel der Achsenleiste mit fester Breite und Kürzung mit Tooltip (volle Reservierung und 804-px-Einzeiligkeit gleichzeitig nicht möglich, gemessen), LabelMasse mit Renderertyp, Hinting und aufgelöster Schrift.
4. Reviews fanden u. a.: Export noch rc-abhängig (MAJOR), `tests/darstellung` fehlte im pytest-`pythonpath` (MAJOR, Gesamtlauf nur durch Sammelreihenfolge grün), Gitterfarbe in der App ungewollt geändert (MAJOR). Alle behoben; zusätzliche Runden vom Nutzer freigegeben.

## Ergebnis
Thesis-Abbildungen bei matplotlib-Standard über alle Runden byte-identisch (38 SHA-256). App-Bildpuffer der Animation identisch zum Stand vor der Härtung. Unter fremder rc (dpi, Schrift, Farben, Gitter, Hinting) bleiben Oberfläche und Exporte gleich.

## Verifikation
Letzter Stand (Umsetzer): ruff, Format, mypy --strict grün; 3065 passed, Abdeckung 98,38 %; `tests/darstellung` ohne GUI-conftest 807 passed; GUI 657 passed, 0 failed. Orchestrator: GUI-Gesamtlauf auf a5b1888 626 passed. Reviewer: Mutationsproben je Befund.

## Probleme und verworfene Ansätze
Vermutung „Systemschrift“ war falsch. Volle Reservierung der Einheitenbreite verworfen (bricht Kompaktlayout bzw. Tabellenhöhe). Voller `stil.rc()`-Kontext für die Animation verworfen (hätte Thesis-Hashes geändert). Mehrfach Unterbrechungen durch Nutzungslimit und Containerwechsel.

## Offene Punkte
2D-Ansichten: weitere rc-Abhängigkeiten (Gitterstil, Tick-Größen, Schriftgewicht, Hinting u. a.) – nach dem Termin (Nutzerentscheidung). HiDPI nur im Container gemessen. Am Messrechner: prüfen, ob eine `matplotlibrc` existiert; Schrift der Animation kurz sichten.

## Thesis-Bezug
4.5 Oberfläche, 5.1 Verifikation (Testumgebung), 5.4 Grenzen.
