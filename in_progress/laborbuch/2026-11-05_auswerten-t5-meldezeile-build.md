# 2026-11-05 – Auswerten T5: Meldezeile, Anleitungen, Build 0.2.0

**Art:** Arbeitspaket
**Paket/Bezug:** U-AUSW-T5, K-AUSW-T5, R-032, Plan P-AUSW, ADR-022
**Commit:** a0ee2fc6c870383b898611b7f4299ee15fb94416 (Build-Stand; Doku-Nachtrag mit Hash/SHA-256 im folgenden Commit)
**Beteiligt:** software-engineer (sonnet für T5, haiku für K-AUSW-T5), reviewer (haiku), Orchestrator (Build, Platzhalter); Entscheidungen Jakob Busch

## Ziel
Offenen MAJOR aus T4 beheben (Warnzahl der Fußzeile verschwindet bei langem Prüf-Fehlertext), Installations- und Prüfanleitung für den Reiter „Auswerten“ am Messrechner, neues Wheel für den nächsten Termin.

## Vorgehen
1. U-AUSW-T5: Prüftextbreite auf frei − 160 px begrenzt (`_MELDE_MIN_PX`), Kürzung nur für Zähltexte, Fehlertexte rechts gekürzt (`KuerzLabel.setze_teile`); Test `test_langer_pruef_fehler_verdraengt_die_meldezeile_nicht`. Anleitungen `installation_…md`, `pruefanleitung_auswerten.md`; Version auf 0.3.0 angehoben.
2. Review R-AUSW-T5: FREIGABE MIT AUFLAGEN. MAJOR: Anhebung auf 0.3.0 widerspricht KONVENTIONEN (0.2.0 nie installiert). MINOR: Dokufehler (W7a, W9, Quellen W1a/W1e, toter Verweis „Schritt 5.3“, LIESMICH/Ablaufplan „unverändert“).
3. Nutzerentscheidung: bei 0.2.0 bleiben, Doku korrigieren.
4. K-AUSW-T5: Version zurück auf 0.2.0 (`uv.lock` ohne Diff zu HEAD), Anleitung in `installation_0.2.0.md` umbenannt, Befunde behoben (W7a: `.tmp`-Reste nach Abbruch per `terminate()` möglich, nächster Export meldet und entfernt sie; W9: andere Dateien als `.svd` werden ohne Meldung abgewiesen).
5. Commit a0ee2fc, Build-Info (`git_dirty` false), Wheel gebaut, in frischer venv (Linux, `--no-deps`) installiert und Build-Info gelesen. Abhängigkeits-Wheels für Windows x64 / CPython 3.11 mit `tools/wheelhouse/erzeuge_wheelhouse.py` geladen; die 12 neuen Pakete und das Wheel nach `naechster-termin_messrechner/stick/wheelhouse/`.

## Ergebnis
- Wheel `ldv_automation-0.2.0-py3-none-any.whl`, 406 176 Byte, SHA-256 `68221a3c96f2e42ddc3c72b5f9e83a0b5846a1dc6876a2376f0d5a2dbf1e6bd7`, Build a0ee2fc. Ersetzt den nie installierten Stick-Build 6d84318 gleicher Versionsnummer.
- Neue Wheels: matplotlib 3.11.2, contourpy, cycler, fonttools, kiwisolver, packaging, pillow, pyparsing, python-dateutil, six, tzdata 2026.6, olefile 0.47; SHA-256 in `stick/LIESMICH.txt`.

## Verifikation
- Gemeldet von K-AUSW-T5 (cloud, offscreen): 2078 passed (Standard), 299 passed (`-m gui`), Abdeckung 98,57 %, ruff/format/mypy --strict ohne Befund.
- Review T5: Warnzahl in allen 15 Fällen bei 1100×680 sichtbar.
- Nicht am Messrechner geprüft; Installation N1–N7 und Prüfanleitung W1–W10 stehen aus.

## Probleme und verworfene Ansätze
- Versionsanhebung 0.3.0 verworfen (Regelverstoß, siehe Review).
- W7a/W9 aus dem Code abgeleitet, nicht per GUI-Test oder am Gerät belegt.
- Zeitangabe W1e: Plan nennt ca. 250 ms (Container), Laborbuch T3b 0,49 s für das erste Paar; beide mit Quelle in der Anleitung, Widerspruch nicht aufgelöst.

## Offene Punkte
- Installation und Prüfanleitung am Messrechner (nächster Termin).
- Zeiten am Messrechner mit `zeiten_messen.py` messen (klärt W1a/W1b/W1e).
- MINORs aus der T3b-Design-Abnahme (Textblock, Kennzeichenblock, Pfeile bei 1366×768).

## Thesis-Bezug
Umsetzung (Auswertungsoberfläche, Verteilung/Installation), Verifikation.
