# 2026-11-23 – Nachbesprechung mit Daniel und Florian: Skript-Steuerung

**Art:** Betreuertermin
**Paket/Bezug:** Messrechner-Termin 2026-11-23 ([Laborbuch](2026-11-23_messrechner-com-trockenlauf.md)); Lastenheft (neue Anforderungen folgen über `/anforderungs-analyst`)
**Commit:** 2cc36f3
**Beteiligt:** Jakob Busch, Daniel Alboldt (Betreuer), Florian (Betreuer)

## Ziel
Stand nach dem Messrechner-Termin besprechen und weitere Vorgaben aufnehmen.

## Vorgehen
Mündliche Besprechung im Anschluss an den Termin; Notizen von Jakob.

## Ergebnis
Rückmeldung zum Stand: „war alles super“, keine weiteren Anmerkungen.

| Nr. | Vorgabe |
|---|---|
| N1 | Die Software bzw. Schnittstelle soll sich über Python-Funktionen aus eigenen Skripten ansteuern lassen. Die Skripte schreiben Anwender. Umfang zunächst wie die Oberfläche: Warteschlange erstellen, Werte der Messungen ändern, Trockenlauf und Messen starten; keine direkten PSV-Einstellungen. |
| N1a | Eine echte Messung soll aus einem Skript heraus möglich sein, ohne Eingabe von `MESSEN` durch eine Person („ja, unbedingt“). |
| N2 | Automatischer Bericht als Jupyter-Notebook, gegen Ende der Arbeit. |

## Verifikation
Mündliche Vorgaben, Notizen von Jakob.

## Probleme und verworfene Ansätze
–

## Offene Punkte
- N1/N1a ins Lastenheft; Umfang und Sicherheitskonzept für Skript-Messungen (Ersatz der menschlichen Bestätigung) im Plan klären und freigeben lassen.
- N2 später einplanen.
- Fragen aus dem Messrechner-Termin (Abgleich-Werte, „Inv.“ bei Ref1) kamen laut Jakob nicht zur Sprache; weiter offen.

## Thesis-Bezug
3.4 Anforderungen; 3.5 Softwarekonzept; 4.2 Ansteuerung; 6.2 Ausblick (N2, falls nicht umgesetzt).
