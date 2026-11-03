# 2026-11-03 – Frequenzachse im Messprotokoll und Dämpfungsangaben mit Band und Methode (R-023, R-055)

**Art:** Arbeitspaket
**Paket/Bezug:** U-R023-R055, Review R-U023, Korrektur K-U023, Re-Review RR-U023; R-020, R-023, R-053, R-055; KONVENTIONEN (Messdaten)
**Commit:** ad2a8e7 (Stand vor diesem Paket)
**Beteiligt:** software-engineer (sonnet), reviewer (haiku); Entscheidungen Jakob

## Ziel
Δf, f_max, Linienzahl und Blockdauer stehen ausdrücklich im Messprotokoll (R-023). Jede Dämpfungsangabe nennt Bandgrenzen in Hz und die Methode (R-055).

## Vorgehen
Aufbereitung mit Code-Sichtung. Nutzerentscheidungen: Δf sowohl von PSV (SampleResolution) als auch berechnet (Bandbreite/Linien); f_max als Bandbreite und als Endfrequenz; eigener Pflichtblock `frequenzachse` (schema_version 2); Bandgrenzen der −3-dB-Methode = −3-dB-Kreuzungen. Umsetzung, Review, Korrektur, Re-Review.

## Ergebnis
- Messprotokoll `schema_version` 2 mit Pflichtblock `frequenzachse`: `delta_f_psv_hz`, `delta_f_berechnet_hz`, `f_max_bandbreite_hz`, `f_max_end_hz`, `linien_anzahl`, `blockdauer_s`, `nicht_lesbar` (Feld → Grund), `hinweis`. Werte ≤ 0, NaN, COM-Fehler oder fehlend → `null` mit Grund.
- Export Stufe 1: je Spitze `daempfung` {zeta, band_u_hz = f_l_hz, band_o_hz = f_r_hz, methode „-3dB-Breite“}.
- Export Stufe 2 (B-1): je Ergebnis `daempfung` {zeta je Mode, Fitband in Hz aus k_von/k_bis, methode}; Gruppen mit `f_von_hz`/`f_bis_hz`; Hinweis bei unbekannter Gruppennummer.
- `format_version` beider Exporte 2 (neue KONVENTIONEN-Regel: jede inhaltliche Änderung erhöht die Version). Keine numerische Änderung an ζ, Fit oder Spitzen.

## Verifikation
Review R-U023: FREIGABE MIT AUFLAGEN (MAJOR: Bandbreite ≤ 0 als Wert statt null). Nach Korrektur Re-Review RR-U023: FREIGABE; 1561 passed, 99 %, ruff, mypy --strict sauber; Fuzz-Test mit 20 002 Eingaben gegen `frequenzachse_zu_dict` ohne Befund. GUI-Tests (Marker gui) vom Orchestrator offscreen ausgeführt: 95 passed.

## Probleme und verworfene Ansätze
- Der erste Umsetzungsstand setzte die Regel „> 0“ nur für Δf berechnet durch; der Reviewer fand das über ein eigenes Prüfskript.
- Der Umsetzer ließ nach seiner letzten Testkorrektur die volle Suite nicht erneut laufen; erst das Review bestätigte sie.
- Format-Version: Die Dateizeit-Felder aus K-2D kamen noch ohne Versionserhöhung (Version 1) hinzu, das ist im Docstring vermerkt.

**Nachtrag (Restpunkte K-U023b/c/d):** Einheiten-Vorbehalt für `blockdauer_s`; Unterlauf des Quotienten Bandbreite/Linien → null mit Grund. Der Restpunkt „Drift-Δζ“ beruhte auf einer falschen Prämisse des Orchestrators: Der Drift-Block enthält nur Frequenzdrift, die ζ-Differenz steht im B-5-Vergleich (`delta_zeta`). Dort tragen die Spitzenpaare jetzt `daempfung_a`/`daempfung_b` mit den Fitbändern beider Messungen. Nutzerentscheidungen: Schema und Stufe-2-Format bleiben 2 (nicht ausgeliefert); ζ-Differenz gilt über beide Ausgangswerte als belegt (beides in KONVENTIONEN). Review R-U023c: NACHARBEIT NÖTIG (Auslegungsfrage, Testlücken); nach Korrektur Re-Review RR-U023d: FREIGABE, 1566 passed, 99 %, Mutationstests gegen Vertauschen A/B bestanden. Ein Agent wiederholte seinen Bericht mehrfach und wurde gestoppt.

## Offene Punkte
- MINOR aus RR-U023d: Null-Fitband in B-5 ohne Hinweis (nur bei nicht zusammenpassenden B-1-Ergebnissen erreichbar); NITPICK in `test_export_paar_daempfung_none_wird_null`.
- Am Gerät: Einheit von SampleResolution (Hz) und SampleTime (s) bestätigen; Verhalten von `Lines` bei eingeschränktem Von/Bis (gilt Δf = Bandbreite/Linien dann?).
- Zur Entscheidung: `band_u_hz`/`band_o_hz` bedeuten in Stufe 1 die −3-dB-Kreuzungen, in Stufe 2 das Fitband; Drift-`delta_zeta` ohne Band und Methode; Vorbehalt zur Einheit von `blockdauer_s`; Unterlauf-NITPICK.
- R-024 (Achsabgleich) wartet auf O7.

## Thesis-Bezug
Umsetzung (Messprotokoll, Rückverfolgbarkeit, Exportformate); Bewertung der Dämpfungsschätzung (Methode und Bandabhängigkeit).
