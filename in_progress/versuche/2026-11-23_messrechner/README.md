# Messrechner-Termin 2026-11-23 (BEOWOLF) – Ablage

Termin nach freigegebenem Ablaufplan (`../naechster-termin_messrechner/ablaufplan.md`), Software 0.2.0, Build `cebac63e5e9c25d66a76e3d87b073a64bbf1e177`, PSV 10.4.0.1. Am Rechner lagen die Dateien unter `D:\Messdaten\DAL\BA Jakob Busch\termin_2026-11-23\`; hochgeladen von Jakob am 2026-11-23, hier einsortiert. Hardwaretests gelten nur, soweit Jakob sie bestätigt hat (siehe Protokoll/Laborbuch, folgt nach der Nachbesprechung).

## Inhalt

| Datei | Herkunft | Inhalt |
|---|---|---|
| `../erkundung/erkundung_BEOWOLF_2026-11-23_154125/` (`bericht.json`, `zusammenfassung.md`, `konsole.log`, `registry.reg.txt`, `typelibs.txt`) | `stick/erkundung/erkundung.py --stufe 1`, 15:41, Messköpfe angeschlossen, PSV `/Acquisition` | B1: alle Prüfpunkte Stufe 0 und 1 ok (Verbinden, Version 10.4.0.1, Eigenschaften, Hardware, 153 Messpunkte, 3 3D-Abgleiche, `FftAcqPropertiesValidator` vorhanden) |
| `konfig/konfig_termin.json` | Kopie von `stick/konfig/beispiel_messrechner.json` (B2) | Betriebskonfiguration des Tages; SHA-256 `db98f78ee5b7ec78be4910c9803e7b2ad65c56d785a122c59fab4437735b5dba`, identisch zur Vorlage |
| `konfig/konfig_abgleich_warnen.json` | Kopie mit `abgleich_qualitaet_max_m = 0.0015`, Modus `warnen` | **nur für den Test** AB9; Grenzwert kein Betriebswert |
| `konfig/konfig_abgleich_verweigern.json` | wie oben, Modus `verweigern` | **nur für den Test** AB7/AB8 |
| `messungen/zeiten.json` | `tools/auswertung/zeiten_messen.py`, Kopie von `20261012_ref_Mitte.svd`, 3 Wiederholungen | W1 (Spawn, Lesen, Paar, Prüfjob, Import) |
| `messungen/animation_lokal.md`, `.json` | `tools/auswertung/animation_messen.py`, lokal, 105 Hz | Animation M1 bis M6 |

## Nicht hochgeladen (liegt nur am Messrechner bzw. in den Chat-Ausgaben)

- Erkundungsläufe 14:34 (Stufe 0), 14:43 (Stufe 1b ohne Messköpfe, PolyFile), 14:45 (Stufe 1 ohne Messköpfe); Ergebnisse als Konsolenausgabe dokumentiert.
- Durchgangsordner `D:\…\daten\2026-11-23_*_trockenlauf\` (Messprotokolle T2/T3/t4_test, T6/T7, AB_warnen, AB_verweigern, D_test) und `D:\…\vorlagen\` (`test_5000Hz.set`, SHA-256 `c6115fd514ae96b1f610e56234b5a9c0a693e8653a69d3a7b96fe39f356605a8`; `sicherung_ausgangsstand_2026-11-23.set`, SHA-256 `34a86025cfba182dc1989e7ef2446a0ea5f855c0b1d8d8e05b4add0e10293332`).
