# ADR-028: Achsenbereiche, mehrere Messungen und Ansicht „Diagramm“

**Datum:** 2026-11-09 · **Status:** angenommen (Nutzer, Freigabe Plan P-AUSW2)
**Bezug:** R-073, R-058, R-059; Brief `in_progress/planung/plaene/2026-11-09_K1-AUSW2_design-brief.md`; Plan `2026-11-09_P-AUSW2_umsetzungsplan.md` (Abschnitt 9: Alternativen je Entscheidung E1–E13); ADR-021, ADR-022, ADR-024

## Kontext
Der Reiter „Auswerten“ hält genau eine Messung und kennt Zoom nur auf der x-Achse. Neu verlangt sind einstellbare Achsenbereiche je Ansicht, mehrere offene Messungen und eine Ansicht für Vergleiche und eigene Diagramme.

## Betrachtete Alternativen
Die Alternativen zu E1–E13 stehen mit Vor- und Nachteilen im Plan P-AUSW2, Abschnitt 9. Die wichtigsten:

| Frage | Gewählt | Verworfen |
|---|---|---|
| E1 Ort der Achsenbereiche | Option `achsen` der Zeichenfunktion in `darstellung/` | Nachbearbeitung in `PlotFlaeche` |
| E2 Mehrere Messungen | Qt-freie Messungsliste, Reiter delegiert an die aktive Messung | ein Reiter je Messung |
| E4 Überlagert/nebeneinander | eine Zeichenfunktion für beide | getrennte Funktionen |
| E12 Zoom und Zurücksetzen | Zoom schreibt feste Werte, Zurücksetzen = Auto | Zurücksetzen auf letzte Ausgangsansicht |

## Entscheidung
E1–E13 wie im Plan empfohlen; F3 vom Nutzer bestätigt. Höchstens vier offene Messungen (Annahme; Arbeitsspeicher des Messrechners unbekannt, am Gerät mit `speicher_messen.py` prüfen).

## Begründung
Kleinster Eingriff in den bestehenden Reiter; mit `achsen=None` bleiben Thesis-Abbildungen bitgleich (ADR-024, ADR-027); gemessen ≈ 115 MiB je Messung und 90–320 ms Zeichenzeit (Linux, ohne Qt).

## Konsequenzen
Die Skalenwahl wandert in die Achsenleiste; y-Bereiche bleiben beim Ansichtswechsel erhalten; Messungen mit unterschiedlichen Referenzkanälen sind nicht gemeinsam darstellbar (Einheit der ersten Serie gilt). Speicher und Tempo am Messrechner und über Remotedesktop sind offen (UI-38).
