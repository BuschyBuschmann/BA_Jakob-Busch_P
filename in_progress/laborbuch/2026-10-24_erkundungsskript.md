# 2026-10-24 – Projektgerüst und Erkundungsskript für den PSV-Messrechner

**Art:** Arbeitspaket
**Paket/Bezug:** I5-F, K1, E1 (Plan), E1-U, E1-K, E1-K2, Reviews R-E1, R-E1-R, R-E1-R2; Erwartungsmanagement U1/U2, F4/F5
**Commit:** 0bf9a14 (Code-Stand des freigegebenen Skripts vor der README-Ergänzung)
**Beteiligt:** `strukturdynamik-experte` (I5-F, sonnet), `software-engineer` (K1, E1, E1-U, E1-K, E1-K2, sonnet), `reviewer` (R-E1 bis R-E1-R2, opus), Orchestrator (Nachprüfung der Tests)

## Ziel
Fachliche Absicherung der COM-Referenz und ein schreibgeschütztes Erkundungsskript, das
am Messrechner die blockierenden Prüfpunkte der COM-Referenz klärt, bevor die eigentliche
Software entworfen wird.

## Vorgehen
1. Fachprüfung der COM-Referenz (I5-F: 0 BLOCKER, 4 MAJOR, 12 MINOR), alle Befunde in der
   Referenz eingearbeitet (K1); neue Polytec-Konventionen nach Nutzerfreigabe.
2. Plan E1 (Stufen 0/1/1b, Whitelist-Proxy mit Default deny, Prüfanleitung), vom Nutzer
   freigegeben.
3. Umsetzung E1-U inklusive Projektgerüst `software/` (Python 3.11, uv, ruff, mypy, pytest).
4. Review R-E1 (NACHARBEIT: falsche Erfolgsmeldung bei Schreibfehler, nicht gemeldete
   Planabweichungen, sieben MINOR) → Korrektur E1-K inkl. technischer Sperre gegen
   ungewollten PSV-Start.
5. Re-Review R-E1-R (neuer MAJOR: Überschwärzung bei Kontonamen wie „Polytec“) →
   Korrektur E1-K2.
6. Letztes Re-Review R-E1-R2: FREIGABE MIT AUFLAGEN; Restlücke der Schwärzung per
   Durchsichtsliste im README adressiert (Nutzerentscheidung).

## Ergebnis
- `software/tools/erkundung/erkundung.py` mit Prüfanleitung `README.md`; liest nur, jeder
  COM-Zugriff über eine Whitelist; startet PSV nicht ohne laufenden PSV-Prozess bzw.
  Bestätigung; Bericht als JSON und Markdown.
- 217 Tests, 95 % Abdeckung, ruff/mypy --strict grün (vom Orchestrator nachgefahren).
- Plan E1 mit Nachtrag der Nutzerentscheidungen.

## Verifikation
Standard-Prüfungen aus `KONVENTIONEN.md` nach jeder Runde nachgefahren; Reviews mit
reproduzierbaren Gegenproben. **Kein Test am Messrechner**: alle Prüfpunkte gelten als am
Gerät unbestätigt (Ablauf G).

## Probleme und verworfene Ansätze
- Erste Fassung meldete bei einem Schreibfehler „vollständig“ mit Exit 0.
- Freie-Wort-Schwärzung des Benutzernamens zerstörte bei sprechenden Kontonamen die
  Kerninhalte; ersetzt durch Schwärzung nur in personenbezogenen Kontexten.
- Option `--makepy` verworfen (schreibt außerhalb des Ausgabeordners).
- Zwei Arbeitspakete wurden durch ein Nutzungslimit unterbrochen und danach mit ihrem
  gespeicherten Stand fortgesetzt.

## Offene Punkte
- Ausführung am Messrechner erst nach Klärung von F4 (Installation von Python/pywin32).
- Ergebnis des ersten Laufs per `/laborbuch` festhalten; Upload nach
  `in_progress/versuche/erkundung/`.
- ADR-Kandidaten aus I1, I5 und E1 (COM-Bibliothek, Binding, Whitelist im Produktiv-Adapter,
  Datenpfad) vor dem Architekturentwurf entscheiden.

## Thesis-Bezug
Methodik/Umsetzung (Schnittstellenerkundung, Sicherheitskonzept, Teststrategie mit
Fake-Objekten), Anhang (Prüfanleitung).
