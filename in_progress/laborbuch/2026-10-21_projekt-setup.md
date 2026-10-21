# 2026-10-21 – Projekt-Setup: Arbeitsgruppe, Konventionen, Dokumentationsstruktur

**Art:** Arbeitspaket
**Paket/Bezug:** Setup-Pakete S1–S5
**Commit:** – (noch kein Code unter `software/`)
**Beteiligt:** Orchestrator (Hauptsession), `software-engineer` (S2, Modell sonnet), `reviewer` (S5, sonnet; Re-Review haiku); Nutzer per Interview und Freigaben

## Ziel
Das Repository für die Bachelorarbeit „Entwicklung eines Softwarepakets zur
Automatisierung von Luft- und Raumfahrt-Strukturtests in Python“ (SLA, RWTH Aachen)
so vorbereiten, dass Software (Python 3.11), Versuche und Thesis (Deutsch, LaTeX)
koordiniert entstehen und Zwischenstände für die Thesis nachvollziehbar dokumentiert
werden.

## Vorgehen
1. Orchestrator-Setup (`CLAUDE.md`, Agenten, Skills) aus einem früheren Projekt-Repo
   übernommen; projektfremde Teile (Flutter-Agent, App-Skills) entfernt.
2. Ausschreibung (`Input/Softwarepaket für Luft- und Raumfahrt_Daniel.pdf`) gesichtet und
   daraus eine Struktur aus Agenten und Skills abgeleitet; Plan vom Nutzer freigegeben.
3. S1: Ordnerstruktur `in_progress/` mit Laborbuch, Entscheidungen (ADR), Versuchen,
   Fachgrundlagen, Literatur, Thesis; Vorlagen; `CLAUDE.md` um Projektkontext,
   Abläufe und Dokumentationspflicht ergänzt.
4. S2: `KONVENTIONEN.md` (Python 3.11 mit uv, ruff, mypy --strict, pytest mit 90 %
   Mindestabdeckung, Hardware nur über Schnittstelle plus Simulator, Referenzfälle,
   Messdaten, Einheiten) und SessionStart-Hook für die Python-Umgebung.
5. S3: Agenten per Interview angelegt: `strukturdynamik-experte`,
   `literatur-rechercheur`, `wissenschaftlicher-autor`, `thesis-gutachter`.
6. S4: Skills per Interview angelegt: `/laborbuch`, `/anforderungs-analyst`,
   `/versuchsplanung`, `/ba-planung`.
7. S5: Konsistenzreview des Gesamtsetups, Korrektur der Befunde, Re-Review.

## Ergebnis
Arbeitsgruppe aus 7 Agenten und 5 Skills mit abgegrenzten Rollen und
Schreibbereichen. Dokumentationskette: Laborbuch → ADR → Versuche → Nachverfolgungsmatrix
→ Kapitel-Zuordnung. Wesentliche Nutzerentscheidungen:
- Thesis auf Deutsch in LaTeX, Institutsvorlage folgt.
- Einfache grafische Oberfläche gewünscht; GUI-Technologie wird per ADR festgelegt.
- KI-Unterstützung beim Text nur als gekennzeichnete Rohfassung, die der Nutzer selbst
  überarbeitet; zulässiger KI-Einsatz ist mit dem Betreuer zu klären.
- Volltexte der Literatur stellt der Nutzer als PDF unter `Input/literatur/` bereit.
- Testabdeckung 90 %; Ausnahmen nur für dünnen COM-/GUI-Code mit Begründung.
- Freigegebene Stände werden ohne weitere Nachfrage committet und gepusht.

## Verifikation
- Frontmatter aller Agenten und Skills per YAML-Parse geprüft (gültig, ohne `model`).
- SessionStart-Hook mit und ohne `CLAUDE_CODE_REMOTE` ausgeführt (Exit 0), mit
  Test-`pyproject.toml` `uv sync` mit Python 3.11 erfolgreich; `shellcheck` nicht verfügbar.
- Review S5: „Freigabe mit Auflagen“ (5 MAJOR, 11 MINOR, 2 NITPICK); alle bis auf die
  bewusst nicht umgesetzte optionale `tools:`-Beschränkung korrigiert; Re-Review siehe
  Offene Punkte.

## Probleme und verworfene Ansätze
- Erster Push nach Anlegen der Ordner abgelehnt, weil parallel auf GitHub Commits
  entstanden waren; per Merge zusammengeführt, ohne Historie umzuschreiben.
- Ordnername „In Progress“ wegen Leerzeichen (LaTeX, Kommandozeile) in `in_progress`
  umbenannt.

## Offene Punkte
- Details der COM-Schnittstelle zum Vibrometer (Unterlagen folgen vom Nutzer).
- Institutsvorlage für LaTeX und ggf. Bewertungsraster.
- Zulässiger KI-Einsatz und Kennzeichnung mit dem Betreuer klären.
- LaTeX ist im Cloud-Container nicht installiert; Kompilieren dort nicht möglich.
- Lastenheft (`/anforderungs-analyst`), Gliederung und Zeitplan (`/ba-planung`) stehen aus.

## Thesis-Bezug
Methodik/Vorgehen (Arbeitsorganisation, Reproduzierbarkeit); ggf. Anhang.
