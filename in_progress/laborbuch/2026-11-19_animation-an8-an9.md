# 2026-11-19 – Animation AN8/AN9: Standbild speichern, Werte als Tabelle, Messskript, Prüfanleitung

**Art:** Arbeitspaket
**Paket/Bezug:** U-AUSW3-89, R-/DA-AUSW3-89, K-AUSW3-89, RR-/DRA-AUSW3-89, K2-AUSW3-89, RR2-AUSW3-89; R-071; Plan P-AUSW3 (AN8, AN9); ADR-021, ADR-029
**Commit:** b102af9 (Stand vor dem Paket-Commit)
**Beteiligt:** software-engineer (sonnet), reviewer (opus), ui-designer (sonnet); Entscheidungen Jakob Busch

## Ziel
Standbild im Animationsmodus speichern (AN8) und den Querschnitt abschließen (AN9: Tabelle, Messskript M1–M6, Prüfanleitung für den Messrechner), vor dem Termin 2026-11-23.

## Vorgehen
1. Nutzer wählte „AN8 + AN9 komplett“ vor Montag. Umsetzung (einmal durch das Nutzungslimit unterbrochen).
2. Review FREIGABE MIT AUFLAGEN (Tabelle ohne Potenzschreibweise, Klammerfehler und fehlendes Aufwärmen im Messskript); Design-Abnahme NACHARBEIT NÖTIG (MAJOR: Farbleiste überdeckt bei 1366×768 und länglicher Platte die x-Beschriftung; MINOR: Punktlabels überlagern sich, Leiste dreizeilig bei 1100×680). Nutzer: alles beheben; Version bleibt 0.2.0, Hash nachziehen; Konvention zum Stempel aufgenommen.
3. Korrektur 1. Design-Re-Abnahme FREIGABE; Re-Review NACHARBEIT NÖTIG – MAJOR: nach Drehen per Maus wurde der Zoom nicht neu gemessen (Fehler seit AN7 Korrektur 2, dort übersehen), Box überdeckte wieder Farbleiste/Textspalte (bis 138 px).
4. Korrektur 2 (letzte Runde): Messung gegen den Blick der letzten Messung, Achsen vor der Messung eingeschaltet, Label-Dichte über tatsächliche Textrechtecke mit weißem Halo, Achsenrand 7 %. Re-Review FREIGABE MIT AUFLAGEN.

## Ergebnis
Standbild PNG/PDF mit Stempel (θ, f, Überhöhung/Skalierung, Blick, M8/M12), Dateivorschlag `…_ansicht4_animation_theta<Grad>`; Dialog „Werte als Tabelle“; `software/tools/auswertung/animation_messen.py` (M1–M6); Prüfanleitung `in_progress/versuche/naechster-termin_messrechner/pruefanleitung_animation.md`. Nebenbei behoben: Stempelrand wurde in `zeichne_animation` ignoriert (seit AN4).

## Verifikation
Umsetzer: 2913 passed, Abdeckung 98,36 %. Orchestrator nach dem letzten Stand: ruff, Format, mypy --strict ohne Befund; GUI-Suite 581 passed (Einzellauf). Containermessungen der Bildzeiten sind nur Richtwerte.

## Probleme und verworfene Ansätze
Erste Dichteprüfung der Punktlabels nutzte unprojizierte Textmaße und war unzuverlässig. Der Zoom-Fehler nach dem Drehen blieb zwei Reviews lang unentdeckt, weil kein Test den Pfad „ziehen, dann loslassen“ abdeckte.

## Offene Punkte
Label-Dichte kostet bei 1500 Punkten ca. 0,5 s je Blick-/Zoomänderung; Labels der Beispieldatei je nach Blick ganz ausgeblendet; Zahl der Labels kann zwischen Bildschirm und Standbild abweichen (dem Nutzer vorgelegt). UI-38 und M1–M7 am Messrechner. Neuer Build mit AN8/AN9 folgt.

## Thesis-Bezug
4.4/4.5 Auswertung und Oberfläche (Animation), 5.3 Erprobung (Bildzeiten).
