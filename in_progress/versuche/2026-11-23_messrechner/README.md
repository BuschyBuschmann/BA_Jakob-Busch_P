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
| `durchgaenge/2026-11-23_<Zeit>_trockenlauf/` | Durchgangsordner der Oberfläche (`D:\…\daten\`), je Ordner `*.protokoll.json` je Versuch, `durchgang.ereignisse.jsonl`, `durchgang.warteschlange.json`; hochgeladen als ZIP | Trockenläufe, Übersicht unten |

## Trockenläufe (aus den Messprotokollen)

| Ordner | Eintrag (Versuch) | Status | Fehler / Abgleich | Test |
|---|---|---|---|---|
| 160721 | T2_test, T2_test_v2 (Bandbreite 5600 Hz) | fehler | Abweichung beim Zurücklesen: Soll 5600, Ist 5000 | T2, Befund 2-2 |
| 161100 | T3_test (Bandbreite 4000 Hz) | fehler | „Ungültiger Wert“ (PSV, HRESULT −2147352567) | T2, Befund |
| 161429 | t4_test (Bandbreite 6250 Hz, Mittelung 5) | trockenlauf (fertig) | Abgleich gelesen, Prüfung bestanden (ohne Grenzen) | T2; „Bis“ blieb 5 kHz |
| 162409 | T6_Linien v1–v3 | fehler | „Die Einstellungen der Datenerfassung sind gesperrt …“ (PSV-Einstellungsdialog offen) | Test 1, Befund |
| 162409 | T6_Linien v4 (Linien 800), Pausenpunkt, T7_typ (Magnitude, 10) | trockenlauf (fertig) | – | Test 1 |
| 162916 | AB_warnen (Grenze 1,5 mm) | trockenlauf (fertig) | Abgleich nicht_bestanden: 3D-Abgleich 2, 1,527 mm (Warnung) | Test 2, AB9 |
| 163221 | AB_verweigern (Grenze 1,5 mm) | fehler | Abgleich nicht_bestanden, Durchgang angehalten | Test 2, AB7/AB8 |
| 163509, 163842 | D_test | trockenlauf (fertig) | – | Test 3 (Voraussetzung Freischaltung) |

## Nicht hochgeladen (liegt nur am Messrechner bzw. in den Chat-Ausgaben)

- Erkundungsläufe 14:34 (Stufe 0), 14:43 (Stufe 1b ohne Messköpfe, PolyFile), 14:45 (Stufe 1 ohne Messköpfe); Ergebnisse als Konsolenausgabe dokumentiert.
- `D:\…\vorlagen\` (`test_5000Hz.set`, SHA-256 `c6115fd514ae96b1f610e56234b5a9c0a693e8653a69d3a7b96fe39f356605a8`; `sicherung_ausgangsstand_2026-11-23.set`, SHA-256 `34a86025cfba182dc1989e7ef2446a0ea5f855c0b1d8d8e05b4add0e10293332`).
