# ADR-024: Zeichenschicht `darstellung/` für Oberfläche und Thesis (Nachtrag zu ADR-021)

**Datum:** 2026-11-05 · **Status:** angenommen
**Bezug:** ADR-021; KONVENTIONEN (gemeinsame Zeichenfunktion); Plan P-AUSW (T2); Laborbuch 2026-11-04_auswerten-t2-darstellung; Entscheidung des Nutzers vom 2026-11-05

## Kontext
Oberfläche und Thesis-Abbildungen sollen dieselbe Zeichenfunktion nutzen; die Oberfläche braucht Stempel „Arbeitsansicht“, die Thesis nicht.

## Betrachtete Alternativen
| Alternative | Vorteile | Nachteile |
|---|---|---|
| GUI-freie Schicht `ldv_automation/darstellung/`: Funktionen füllen eine übergebene `Figure`, Stil als Parameter (`Plotstil`, `THESIS_STIL`), Rückgabeobjekt `Zeichnung`; Arbeitsbild als neue Figure aus derselben Funktion plus Stempel | eine Quelle, ohne Qt testbar, kein globaler matplotlib-Zustand (`rc_context`) | zusätzliche Schicht, Stil muss durchgereicht werden |
| Zeichnen direkt in den Widgets | weniger Schichten | Thesis bräuchte zweite Implementierung |
| Stempel auf der Bildschirmfigur | kein Neuaufbau | verändert die Anzeige |

## Entscheidung
Schicht `darstellung/` ohne Qt und ohne `pyplot` (Importregel und Laufzeittest), keine eigene Mathematik (nur Zusammensetzung aus `auswertung/`); Arbeitsbild über `speichere_arbeitsbild` aus neuer Figure.

## Begründung
Plan P-AUSW, Umsetzung T2, Review R-AUSW-T2 und Fachabnahme FAB-AUSW-T2.

## Konsequenzen
`tools/auswertung/abbildungen.py` (pyplot, eigene Zeichenlogik) widerspricht der Regel und ist später zu migrieren. Tick-Schrift: `Plotstil.rc()` in der GUI beim Aufbau global setzen.
