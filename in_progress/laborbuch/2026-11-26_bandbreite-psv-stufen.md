# 2026-11-26 – Bandbreite nur als PSV-Stufe, Von/Bis mitsetzen

**Art:** Arbeitspaket
**Paket/Bezug:** BW-1 bis BW-9; ADR-031; Befund T2 aus Laborbuch 2026-11-23_messrechner-com-trockenlauf
**Commit:** 49ee69a
**Beteiligt:** Orchestrator; software-engineer (sonnet); reviewer (opus); Jakob Busch (Entscheidungen)

## Ziel
Bandbreite nur als von PSV angebotene Stufe zulassen und „Von/Bis“ mitsetzen, damit PSV mit dem eingestellten Bereich misst (Voraussetzung für jede echte Messung).

## Vorgehen
1. Aufbereitung und Entscheidungen des Nutzers (Stufen aus PSV, Von = 0/Bis = Bandbreite, nur Auswahlliste, Rückprobe fail-closed; offline gesperrt, Schema 2, Altdateien laden/Start sperren).
2. BW-1 Plan (Befund:  wurde nie gelesen, Von/Bis nie geschrieben), freigegeben.
3. BW-2 Umsetzung (27004a3); Review BW-3: Freigabe mit Auflagen, 4 MINOR, 3 NITPICK – alle vom Nutzer zur Umsetzung gewählt.
4. BW-4 Korrektur (be665fb); Re-Review BW-5: neuer MAJOR (Zeitlimit beim Nachlesen verschluckt, Widerspruch zu K-U2b), MINOR (Ist der Bandbreite im Fehlerpfad fehlte).
5. BW-6 Korrektur nach Entscheidung des Nutzers (96257ce); Re-Review BW-7: neuer MAJOR (Ergänzung überschrieb leeres Rückprobe-Ist, Messungszustand verändert), MINOR (zwei Handler ungetestet).
6. Dritte Korrekturrunde vom Nutzer freigegeben: BW-8 (49ee69a); Re-Review BW-9: Freigabe.

## Ergebnis
- Adapter liest die Stufen beim Verbinden und beim Setzen, lehnt Nicht-Stufen vor dem ersten Schreiben ab, setzt Bandwidth, Lines, StartFrequency = 0, EndFrequency = Soll, dann Übernahme.
- Steuerung prüft Bandbreite, Von und Bis nach dem Setzen; Abweichung = Fehler nach O1, kein Scan. Messprotokoll mit Soll/Ist für Bandbreite, Von, Bis, auch im Fehlerfall (Stand tolerant nachgelesen; Hänger beim Nachlesen → Gerät unklar nach K-U2b).
- Startsperre bei Nicht-Stufe in allen Betriebsarten; Editor mit Auswahlliste, offline gesperrt.
- Simulator bildet die T2-Fälle nach (ignorieren 5600, Fehler 4000, Bis bleibt).
- Prüfanleitung `in_progress/versuche/2026-11-23_messrechner/pruefanleitung_bandbreite.md`.

## Verifikation
Vom Reviewer selbst ausgeführt (BW-9): ruff, ruff format, mypy --strict ohne Befund; pytest 3115 bestanden, Abdeckung 98,35 %; GUI offscreen 667 bestanden. Hardwaretest steht aus, nicht bestanden gemeldet.

## Probleme und verworfene Ansätze
- Annahme im Auftrag, `AvailableBandwidths` werde schon gelesen, war falsch (nur auf der Leseliste).
- Erste Korrektur verwarf ein Zeitlimit beim Nachlesen bewusst; das widersprach K-U2b und wurde zurückgenommen.
- Zweite Korrektur erkannte „Rückprobe nicht gelaufen“ an `ist is None` und überschrieb so ein leeres Rückprobe-Ergebnis; ersetzt durch „keine Zeilen aus der Rückprobe“.
- Abdeckung 98,03 % aus einem Zwischenlauf des Umsetzers ließ sich nicht nachvollziehen; Reviewer maß 98,32 % bzw. zuletzt 98,35 %.

## Offene Punkte
- Prüfanleitung am Messrechner vor jeder echten Messung (Stufenliste lesbar? Von/Bis im Validator? Bis > neue Bandbreite?).
- Hinweis Reviewer: ohne Rückprobe wird nur das Ist der Bandbreite aus dem Stand ergänzt, andere Parameter bleiben null (so beschlossen).
- Vorschlag für KONVENTIONEN.md offen (Entscheidung des Nutzers).

## Thesis-Bezug
4.2 Ansteuerung und Warteschlange; 5.4 Fehler, Grenzen und Unsicherheiten.
