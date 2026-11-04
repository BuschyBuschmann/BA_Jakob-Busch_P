# 2026-11-04 – Auswertungsoberfläche T2: Zeichenfunktionen (darstellung/) und Korrekturen am Hintergrundprozess

**Art:** Arbeitspaket
**Paket/Bezug:** U-AUSW-T2, Korrekturen K-AUSW-T2/T2b; Review R-AUSW-T2, RR-AUSW-T2, RR-AUSW-T2b; Fachabnahme FAB-AUSW-T2, FAB-AUSW-T2b; R-050–R-053, R-055; ADR-021; Fachanalyse FA-AUSW
**Commit:** c4889a6 (Stand vor diesem Paket)
**Beteiligt:** software-engineer (sonnet, haiku), reviewer (opus, haiku), strukturdynamik-experte (sonnet)

## Ziel
GUI-freie Zeichenfunktionen für die vier Ansichten (Spektrum, H1/H2+Kohärenz, Spitzen/Bänder, Schwingform), gemeinsam für Oberfläche und Thesis; Arbeitsbild mit Stempel; Korrekturen aus dem T1-Review.

## Vorgehen
Umsetzung nach Plan P-AUSW mit Nutzerentscheidungen F-1 bis F-4; Review (opus) und Fachabnahme (sonnet) parallel; Korrekturrunde 1 (ζ-Beschriftung, 3D-√AP-Hinweis, Bezugspunkt, Vorzeichentexte, Tickformat u. a.); Re-Review und Re-Abnahme; Korrekturrunde 2 (Vorzeichentext Ansicht 4 ohne Subjekt, Nullbezug, ζ-Stellen); Re-Review.

## Ergebnis
- `ldv_automation/darstellung/` (stil, formate, zeichnung, auswahl, spektrum, frf, spitzen, schwingform, bild) ohne Qt und ohne pyplot; Beispielskript `tools/auswertung/darstellung_beispiel.py` mit denselben Funktionen.
- Ansicht 1: |CPH| voreingestellt, √AP wählbar; Betragsmittel bzw. quadratisches Mittel je Größe; 3D-Mittel „nicht gegen PSV geprüft“.
- Ansicht 2: Phase in Grad mit Vorzeichentext, Platzhalter beim Mittel.
- Ansicht 3: Spitzenmarker, nur gewählte Spitze beschriftet mit ζ, Band, Methode und Warnkennzeichen (KONVENTIONEN hatte Vorrang vor Brief UI-8 „f und ζ“).
- Ansicht 4: Betrag; Phase gegen Ref1 oder relativ zum Bezugspunkt (Kern-Hilfen `phase_relativ_rad`, `waehle_bezugspunkt`), Pfeile + `twilight`, Maske γ² < 0,9.
- `hintergrund.py`: Fehlerkanal als gepickeltes Tupel (Surrogate, NUL), „Exitcode unbekannt“, kill nach terminate (0,3 s / 1,0 s).

## Verifikation
Zuletzt 1862 passed, 99 %, GUI 95 passed, ruff, mypy --strict sauber (vom Reviewer bestätigt). Referenzfälle RF-UI-F2a…F4d als Tests; `PaarCache` bitgleich zu `werte_aus`. Re-Abnahme: Korrekturen freigegeben; Re-Review RR-AUSW-T2b: FREIGABE.

## Probleme und verworfene Ansätze
- Fachabnahme M-1 (MAJOR, offen): Pfeile in Ansicht 4 kaum lesbar (zu kurz, schwarz auf dunklem twilight-Bereich) – Ansicht 4 als Ganzes nicht freigegeben, Nutzerentscheidung ausstehend.
- Zwei Korrekturrunden nötig; ein Vorzeichentext war ohne Subjekt im Deutschen umgekehrt lesbar.
- Zwei Umsetzungsagenten meldeten nach ihrem Bericht weitere Hintergrundarbeit und wurden gestoppt.

## Offene Punkte
- Nutzerentscheidungen: Pfeildarstellung (M-1), Mittelformel/Punktzahl im Bild, M6-ungültige Punkte, Layout (Beschriftungskasten, Punktausdehnung), Thesis-Spitzenbeschriftung, 3D-Hinweis bei NaN, Frequenzformat ≥ 1000 Hz, ζ-Rundung.
- MINOR: `zahl_signifikant_text(-0.0)` → „−0“.
- Windows: Schriften/Glyphen (⚠, Hochzahlen), HiDPI, SIGTERM/kill.

**Nachtrag 2026-11-05 (Entscheidungen Jakob):** Pfeile konstanter Länge mit hellem Rand, Betrag über Markergröße (ADR-025); Mittelformel und Punktzahl im Bild (KONVENTION); M6-ungültige Punkte kennzeichnen; Thesis-Beispiel mit relativer Phase; 3D-Leistungsmittel: Rechnung auf gemeinsame Punktmenge angleichen; Thesis-Spitzenbild beschriftet die stärkste Spitze; Frequenzen mit fester Nachkommastellenzahl, ζ 2 signifikante Stellen; Layout Ansicht 3/4 über den ui-designer; ADR-022 bis ADR-025 angelegt; KONVENTIONEN ergänzt.

## Thesis-Bezug
Umsetzung und Darstellung der Auswertung; Phasendarstellung in Graustufen; gemeinsame Zeichenfunktionen für Thesis-Abbildungen.
