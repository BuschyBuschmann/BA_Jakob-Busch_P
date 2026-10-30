<!-- Bericht W5-1 (Umsetzung): Auswertung Stufe 1 nach FG-02; erstellt im Paket W5-1 von software-engineer, Stand 2026-10-29; nachgeführt im Korrekturpaket K-W5-1 am 2026-10-30 (FG-02 mit K1). Nicht committet. -->

# W5-1 – Umsetzung der Auswertung Stufe 1 (FG-02)

**Grundlage.** Freigegebene Fachgrundlage `in_progress/fachgrundlagen/FG-02_auswertung-stufe1.md`
(Nutzerfreigabe 2026-10-29, Korrektur K1 eingearbeitet und freigegeben 2026-10-30), Lastenheft R-050 bis R-053, Nutzerwahl A-1 bis A-8 sowie
B-2, B-3, B-4, B-6, B-7, B-9, B-10 (W3). Stufe 2 (B-1, B-5, B-8) ist nicht enthalten.

**Vorbehalt.** Alle Ergebnisse an der Beispieldatei gelten **vorbehaltlich der Annahmen
M1–M11** (FG-02 Abschnitt 11). Jede Ausgabe und jeder Export führt die Annahmen mit Status
mit (P-11).

## 1 Aufbau

| Ort | Inhalt |
|---|---|
| `software/src/ldv_automation/auswertung/` | Qt-freies Paket, nur NumPy + Standardbibliothek + `protokoll.version` (Importrichtungstest) |
| `software/tools/auswertung/abbildungen.py` | Abbildungen **nur aus dem gespeicherten Export** (NumPy, JSON, matplotlib; kein Import aus dem Hauptpaket) |
| `software/tools/auswertung/beispiel_svd.py` | Beispiel: `.svd` lesen (W2-Leser, unverändert) → Adapter → Auswertung → Export → Abbildungen |
| `software/tests/auswertung/` | Referenzfälle FG-02 Abschnitt 9, Datenvertrag, Export, Werkzeuge, Golden-File-Test |

NumPy ist jetzt Paketabhängigkeit (`uv add "numpy>=2.4.6"`, Lock aktualisiert; die Version
war schon über die Gruppe `werkzeuge` im Lock). SciPy wird nicht gebraucht.

## 2 Zuordnung FG-02 → Modul/Funktion → Test

| FG-02 | Inhalt | Modul / Funktion | Tests (`tests/auswertung/`) |
|---|---|---|---|
| 2.3, 11 | Frequenzachse, k₀ (M2) | `annahmen.Annahmen.k0`; Prüfung `plausibilitaet.p06_frequenzachse` | `test_aw_rf_plausibilitaet::test_p06_frequenzachse` |
| 2.4 | s_b (M8), Konjugation (M1) | `daten.vorverarbeite`, `daten.bereite_paar` | RF-H8 `test_aw_rf_frf::test_rf_h8_…`, `test_aw_datenvertrag::test_bereite_paar_…` |
| 2.5, 6.1 | Datenvertrag, Formen, dtypes | `daten.Messdaten`, `daten.Punkte` | `test_aw_datenvertrag::test_messdaten_…`, `test_punkte_formen` |
| 3.1 | `spektrum_kohaerent`, `spektrum_leistung`, CPH-Ersatz, 3D-Betrag | `spektren.spektren_paar`, `spektren_kanal`, `betrag_3d`, `betrag_3d_ap`, `daten.cph_aus_cp` | RF-H6; `test_spektren_ohne_referenz_nur_leistung`; `test_3d_betrag_…` |
| 3.2 | Punktmittel Betrag/quadratisch/arithmetisch, n | `mittel.punktmittel_betrag`, `punktmittel_arithmetisch` | RF-G1 bis RF-G4; Golden (35 AvgSeq) |
| 3.3 | H1, H2, γ², n_d = 1 | `frf.h1_h2_kohaerenz`, `berechne_frf` | RF-H1 bis RF-H7, RF-U4 |
| 3.4 | Zufallsfehler, Fehlerband k_ε | `frf.zufallsfehler`, `FrfErgebnis.h1_band_*` | RF-U1 bis RF-U5, `test_fehlerband_um_h1` |
| 3.5 | Maske, Gewicht | `frf.kohaerenz_maske`, `frf.gewicht` | RF-U6, RF-U1 bis RF-U4 |
| 3.6 | Linienwahl, Schwingform, Ellipse, Momentanwert | `schwingform.*`, `gesamt.schwingform_aus` | RF-3D1 bis RF-3D7 |
| 3.7 | Weg/Schnelle/Beschleunigung | `umrechnung.*` | RF-W1 bis RF-W3 |
| 3.8 | Band-RMS, `rms_psv`, `bandnorm`, W_RBW, Bandregel (M10) | `baender.*` | RF-S3, RF-B1 bis RF-B9; Golden (22 Bänder, S17) |
| 3.9 | Spitzensuche, Parabel, −3-dB-Breite, Kennzeichen | `spitzen.*` | RF-P0 bis RF-P5, RF-M1 bis RF-M4 |
| 4 | P-01 bis P-11 | `plausibilitaet.*`, `gesamt.werte_aus` | RF-K1 bis RF-K4, `test_p01…` bis `test_p10_und_p11`, RF-H7 (P-05) |
| 5 | Export | `export.exportiere`, `lese_export` | `test_aw_export_werkzeuge::test_export_…` |
| 5 | Abbildungen | `tools/auswertung/abbildungen.py` | `test_abbildungen_aus_export`, `test_abbildung_mit_niedriger_…` |
| 8 | Toleranzen (M11) | `annahmen.Toleranzen` | `test_toleranzen_abschnitt_8`; Golden |
| 9.9 | Golden-File | – | `test_aw_golden_datei` |
| 11 | Annahmen M1–M11 | `annahmen.Annahmen.eintraege` | `test_voreinstellungen_nach_fg02`, `test_annahmen_status_…` |
| – | Anbindung W2-Leser (A6) | `svd_adapter.aus_svd_messung` (Protocol, kein Import des Lesers) | `test_adapter_…`, Golden |

### Referenzfall → Test

| Referenzfall | Test |
|---|---|
| RF-S1, RF-S2, RF-S3 | `test_aw_rf_band::test_rf_s1_…`, `test_rf_s2_…`, `test_rf_s3_…` |
| RF-B1 bis RF-B9 | `test_aw_rf_band::test_rf_b1_…` bis `test_rf_b9_…` |
| RF-H1 bis RF-H8 | `test_aw_rf_frf::test_rf_h1_bis_h4`, `test_rf_h5_…` bis `test_rf_h8_…` |
| RF-U1 bis RF-U6 | `test_aw_rf_frf::test_rf_u1_bis_u3_…`, `test_rf_u4_…` (2), `test_rf_u5_monte_carlo_…`, `test_rf_u6_…` |
| RF-P0 bis RF-P5 | `test_aw_rf_spitzen::test_rf_p0_…`, `test_rf_p1_bis_p4_…`, `test_rf_p1_gegen_physikalische_wahrheit`, `test_rf_p5_…` |
| RF-M1 bis RF-M4 | `test_aw_rf_spitzen::test_rf_m_zwei_moden[RF-M1…M4]` |
| RF-3D1 bis RF-3D7 | `test_aw_rf_schwingform::test_rf_3d1_bis_3d4_…`, `test_rf_3d3_gegen_brute_force`, `test_rf_3d5_…`, `test_rf_3d6_…` (2), `test_rf_3d7_…` |
| RF-W1 bis RF-W3 | `test_aw_rf_schwingform::test_rf_w1_…` bis `test_rf_w3_…` |
| RF-K1 bis RF-K4 | `test_aw_rf_plausibilitaet::test_rf_k1_bis_k3`, `test_rf_k4_zwoelf_moden_…` |
| RF-G1 bis RF-G4 | `test_aw_rf_frf::test_rf_g1_…` bis `test_rf_g4_…` |
| 9.9 Golden | `test_aw_golden_datei` (5 Tests) |

## 3 Abweichungen von FG-02-Zahlenangaben

In W5-1 gemeldet und mit FG-02-Korrektur K1 (2026-10-30) erledigt:

1. **RF-P5** (K1-2): Grenze jetzt +0,005364·2 Hz mit Toleranz 1e-6·2 Hz; der Test prüft genau
   diesen Wert.
2. **P-09** (K1-5): Linienauswahl über das arithmetische Punktmittel von γ², ddof = 0;
   Datei-Wert 0,0108 steht jetzt in FG-02.

Weiterhin gilt: Sollwerte mit weniger Stellen, als rtol verlangt (z. B. ζ = 0,006582400;
ε_γ² = 0,0028426762; RF-U7), werden zusätzlich mit atol = halbe letzte Stelle geprüft; exakt
bekannte, gerundet angegebene Werte (√2 = 1,4142135624) gegen die geschlossene Form.

## 4 Festlegungen dieser Umsetzung (Assumption Log)

| Nr | Festlegung | Grund |
|---|---|---|
| F1 | Export: `<basis>.npz` (Felder, float64 Real/Imag getrennt, ohne Pickle) + `<basis>.json` (Metadaten, striktes JSON, NaN → null, ±∞ → "inf") | keine neue Abhängigkeit (h5py nicht installiert); offen lesbar mit NumPy bzw. jedem JSON-Leser; SHA-256 der npz in der JSON |
| F2 | UFF-58 nicht umgesetzt | FG-02 5 und 12.3: Konventionen offen |
| F3 | Spitzensuche in `werte_aus` auf dem Betragsmittel von H1 mit arithmetischem Mittel γ̄² | jetzt FG-02 3.9 (K1-7a) |
| F4 | P-07 und P-09 je Kanalpaar; P-07 zählt Spitzen aller gültigen Punkte zusammen (wie W3) | FG-02 nennt kein Paar |
| F5 | P-08 zählt alle gültigen Punkte und Linien mit γ² ≥ 0,9 (W3 nutzte das komplexe Punktmittel und γ² > 0,95) | komplexes Punktmittel gehört nicht zu Stufe 1 |
| F6 | P-09: Linienauswahl über das arithmetische Punktmittel von γ², Standardabweichung mit ddof = 0, je Kanalpaar | jetzt FG-02 4 (K1-5) |
| F7 | `kohaerenz_niedrig`: bei unbestimmter Seite zählt der Bereich bis zur Spitzenlinie; γ² = NaN löst kein Kennzeichen aus; ist γ² im Bereich vollständig NaN oder fehlt γ², Hinweis „Kohärenz nicht prüfbar“ | jetzt FG-02 3.9 (K1-7b) |
| F8 | Achsenende ohne Unterschreiten der Schwelle → `ueberlappend` (FG-02 6.3), auch links | Prüfskript setzte dort kein Kennzeichen |
| F9 | Schwingform ohne Phase: `momentanwert` wirft `ValueError` (RF-3D7: „Entscheidung W5“) | lauter Fehler statt leerem Ergebnis |
| F10 | `phase_gueltig` = Datei enthält mindestens ein Kreuzspektrum | Leser liefert keinen Triggerstatus |
| F11 | *entfallen (K1-1):* Vorzeichen je Kanal `vorzeichen_kanal`, CP/CPH ← s_a·s_b·C(·); Vib X/Y/Z fest +1 (`ValueError` bei −1) | FG-02 2.4, 6.1 |
| F12 | Bandregel `"offen"` als zweite Variante (nur Prüfschritt M10) | FG-02 11 vergleicht [100, 200] mit (100, 200) |
| F13 | Bandwerte je Punkt und für die Punktmittelkurve; CP-Bänder nicht (in 3.8 nicht definiert) | FG-02 6.2 „je Punkt und Mittel“ |
| F15 | P-09 bleibt je Kanalpaar (Fachabnahme NITPICK-1 nicht umgesetzt) | FG-02 4 schreibt „je Kanalpaar“ vor |
| F16 | Messung ohne CP/CPH/ABS: jede Prüfung P-01 bis P-11 erscheint, fehlende Größen als `nicht_pruefbar` mit Grund je Paar bzw. Kanal | Review R-W5-1 (MAJOR) |
| F17 | M4 (`skalierung`) ist ein Parameter, zulässig nur „Spitzenwert (0-to-peak)“, sonst `ValueError` | FG-02 legt keine andere Skalierung fest |
| F18 | AP/ABS aus dem Leser: komplexes Feld nur mit Imaginärteil ≤ 1e-12 · größter Betrag, sonst `ValueError` | Review MINOR 5 |
| F14 | Abbildungen unter `in_progress/analysen/abbildungen/W5-1/` (Arbeitsstand, keine Thesis-Abbildung); Skriptpfad `software/tools/auswertung/` | KONVENTIONEN: Pfad mit dem ersten Abbildungspaket festlegen |

## 5 Ergebnisse an der Beispieldatei (vorbehaltlich M1–M11)

Lauf (nach K-W5-1 wiederholt, 2026-10-30; Zahlen der Spitzen, Mittel und Bänder unverändert, weil alle Vorzeichen +1): `uv run python tools/auswertung/beispiel_svd.py ../Input/20261012_ref_Mitte.svd --export <scratchpad>`
und `uv run python tools/auswertung/abbildungen.py <export> ../in_progress/analysen/abbildungen/W5-1 --paar Vib_Z__Ref1 --paar Ref2__Ref1`.
Messdatei SHA-256 vor und nach dem Lauf `7ef46262df0055f5a45470ae0fc5e6bde547624cdee6b5dc3838060a452e790b`
(gleich). Software: Git `6d5ad1d762f8…` mit nicht committeten Änderungen (`git_dirty = true`);
nach dem Commit neu erzeugen. Export 113 MB (npz) + 0,5 MB (json), nicht im Repository.

**Übereinstimmung mit PSV-Werten derselben Datei (Toleranzen FG-02 8):**
- 35 von 35 PSV-Punktmitteln (AvgSeq: |CP|, |CPH|, ABS, AP, |H1|, |H2|, γ²), größte Abweichung
  6,7·10⁻⁷ bezogen auf das Kurvenmaximum.
- 22 von 22 PSV-Banddaten des Gesamtbands je Punkt (`rms_psv` für CPH, ABS, AP; `bandnorm` für
  H1, H2); die 7 CP-Bänder sind in FG-02 nicht definiert und nicht geprüft.
- `bandnorm` H1 Vib X/Ref1 an Punkt 0: 0,018513758 gegen S17 = 0,018513758 (rel. 1,2·10⁻⁸;
  über alle Punkte ≤ 5,8·10⁻⁸).

**Plausibilitätsprüfungen** (P-11 listet alle zehn Annahmeneinträge M1–M11 als „Annahme“):

| Prüfung | Bezug | Status | Wert |
|---|---|---|---|
| P-01 | Vib X/Ref1 | ok | 1 |
| P-01 | Vib Y/Ref1 | ok | 1 |
| P-01 | Vib Z/Ref1 | ok | 1 |
| P-01 | Ref2/Ref1 | ok | 1 |
| P-01 | Vib X/Ref2 | ok | 1 |
| P-01 | Vib Y/Ref2 | ok | 1 |
| P-01 | Vib Z/Ref2 | ok | 1 |
| P-02 | Vib X/Ref1 | ok | 1 |
| P-02 | Vib Y/Ref1 | ok | 0,9999 |
| P-02 | Vib Z/Ref1 | ok | 1 |
| P-02 | Ref2/Ref1 | ok | 1 |
| P-02 | Vib X/Ref2 | nicht_pruefbar | – |
| P-02 | Vib Y/Ref2 | nicht_pruefbar | – |
| P-02 | Vib Z/Ref2 | nicht_pruefbar | – |
| P-03 | – | ok | 0 |
| P-04 | Vib X | nicht_pruefbar | – |
| P-04 | Vib Y | nicht_pruefbar | – |
| P-04 | Vib Z | nicht_pruefbar | – |
| P-04 | Ref1 | ok | 1 |
| P-04 | Ref2 | nicht_pruefbar | – |
| P-05 | Vib X/Ref1 | ok | 1 |
| P-05 | Vib Y/Ref1 | ok | 1 |
| P-05 | Vib Z/Ref1 | ok | 1 |
| P-05 | Ref2/Ref1 | ok | 1 |
| P-05 | Vib X/Ref2 | ok | 1 |
| P-05 | Vib Y/Ref2 | ok | 1 |
| P-05 | Vib Z/Ref2 | ok | 1 |
| P-06 | – | ok | 0 |
| P-07 | Vib X/Ref1 | ok | 0,975 |
| P-07 | Vib Y/Ref1 | ok | 0,9663 |
| P-07 | Vib Z/Ref1 | ok | 0,9809 |
| P-07 | Ref2/Ref1 | ok | 0,9772 |
| P-07 | Vib X/Ref2 | ok | 0,9784 |
| P-07 | Vib Y/Ref2 | ok | 0,969 |
| P-07 | Vib Z/Ref2 | ok | 0,9831 |
| P-08 | Ref2/Ref1 (akzeleranz) | warnung | 0,000321 |
| P-09 | Vib X/Ref1 | ok | 0,01282 |
| P-09 | Vib Y/Ref1 | ok | 0,01119 |
| P-09 | Vib Z/Ref1 | ok | 0,01079 |
| P-09 | Ref2/Ref1 | ok | 0,01079 |
| P-09 | Vib X/Ref2 | ok | 0,006949 |
| P-09 | Vib Y/Ref2 | ok | 0,004003 |
| P-09 | Vib Z/Ref2 | ok | 0,00431 |
| P-10 | – | hinweis | 0 |

P-08 (Antriebspunkt Ref2/Ref1 als Akzeleranz konfiguriert): r = 0,0003 → Warnung
„Vorzeichen einer Referenz vermutlich gedreht“, wie W3 2.3 (M8 offen).

**Spitzen** auf dem Betragsmittel |H1| Vib Z/Ref1, Δf = 1,5625 Hz: 114 Spitzen, **keine ohne
Kennzeichen**. Kennzeichen: A = `aufloesungsbegrenzt` (67), N = `nachbarmode` (27),
Ü = `ueberlappend` (23), M7 = `gueltigkeit_offen_m7` (42), K = `kohaerenz_niedrig` (0).
Die Breiten sind damit für einen PSV-Vergleich nach FG-02 8 nicht vergleichbar (B/Δf meist < 3).
In den übrigen Paaren gibt es höchstens eine Spitze ohne Kennzeichen (Ref2/Ref1: 865,62 Hz;
Vib X/Ref2: 960,94 Hz; Vib Z/Ref2: 960,97 Hz).

| Nr | f_sp [Hz] | Höhe [(m/s)/N] | B [Hz] | ζ | Kennzeichen |
|---|---|---|---|---|---|
| 1 | 40,538 | 3,631e-03 | 1,919 | 0,02367 | A |
| 2 | 53,052 | 1,203e-02 | 1,279 | 0,01205 | A |
| 3 | 77,870 | 5,481e-03 | 2,164 | 0,01390 | A, N |
| 4 | 81,024 | 3,552e-03 | 1,735 | 0,01071 | A, N |
| 5 | 92,257 | 8,190e-03 | 1,115 | 0,00604 | A |
| 6 | 99,983 | 1,217e-02 | 1,054 | 0,00527 | A |
| 7 | 111,134 | 2,305e-03 | 2,398 | 0,01079 | A |
| 8 | 121,661 | 3,949e-03 | 2,372 | 0,00975 | A |
| 9 | 131,251 | 1,850e-02 | 1,039 | 0,00396 | A |
| 10 | 142,258 | 1,371e-02 | 1,112 | 0,00391 | A |
| 11 | 162,803 | 1,061e-02 | 1,893 | 0,00581 | A |
| 12 | 182,885 | 3,992e-03 | 1,454 | 0,00398 | A |
| 13 | 190,646 | 5,667e-03 | 1,268 | 0,00332 | A |
| 14 | 198,549 | 5,938e-03 | 1,411 | 0,00355 | A |
| 15 | 207,349 | 4,458e-03 | 2,422 | 0,00584 | A |
| 16 | 221,883 | 1,848e-02 | 1,225 | 0,00276 | A |
| 17 | 231,215 | 2,006e-02 | 1,497 | 0,00324 | A |
| 18 | 253,197 | 9,443e-03 | 2,152 | 0,00425 | A |
| 19 | 262,584 | 7,653e-02 | 1,487 | 0,00283 | A, N |
| 20 | 264,990 | 3,738e-02 | – | – | Ü |
| 21 | 270,046 | 2,102e-02 | 1,898 | 0,00351 | A, N |
| 22 | 289,268 | 1,123e-02 | 1,721 | 0,00298 | A, N |
| 23 | 293,646 | 1,103e-02 | 1,849 | 0,00315 | A, N |
| 24 | 303,683 | 1,588e-02 | – | – | Ü |
| 25 | 305,621 | 1,569e-02 | – | – | Ü |
| 26 | 318,811 | 5,235e-03 | 1,885 | 0,00296 | A |
| 27 | 331,056 | 3,226e-03 | 2,656 | 0,00401 | A, N |
| 28 | 337,566 | 1,690e-02 | 1,358 | 0,00201 | A |
| 29 | 342,047 | 4,816e-03 | 2,552 | 0,00373 | A, N |
| 30 | 356,045 | 2,559e-02 | 1,739 | 0,00244 | A |
| 31 | 364,209 | 7,676e-03 | 1,742 | 0,00239 | A |
| 32 | 382,757 | 2,527e-02 | 1,532 | 0,00200 | A |
| 33 | 389,017 | 2,285e-02 | 1,400 | 0,00180 | A |
| 34 | 401,568 | 6,990e-02 | 1,429 | 0,00178 | A |
| 35 | 418,725 | 6,204e-02 | 1,701 | 0,00203 | A |
| 36 | 425,704 | 2,244e-02 | – | – | Ü |
| 37 | 428,072 | 4,251e-02 | 1,635 | 0,00191 | A, N |
| 38 | 436,303 | 4,876e-02 | 2,513 | 0,00288 | A |
| 39 | 451,543 | 2,138e-02 | 2,758 | 0,00305 | A, N |
| 40 | 457,737 | 3,133e-02 | 1,941 | 0,00212 | A |
| 41 | 470,171 | 1,568e-02 | 1,905 | 0,00203 | A |
| 42 | 478,239 | 5,253e-03 | 1,955 | 0,00204 | A |
| 43 | 488,236 | 6,704e-03 | 2,815 | 0,00288 | A |
| 44 | 511,189 | 1,210e-02 | 1,963 | 0,00192 | A |
| 45 | 528,822 | 1,433e-02 | 3,069 | 0,00290 | A, N |
| 46 | 536,582 | 6,058e-03 | 3,007 | 0,00280 | A, N |
| 47 | 559,024 | 1,106e-02 | 2,425 | 0,00217 | A |
| 48 | 589,822 | 4,384e-02 | 2,877 | 0,00244 | A |
| 49 | 602,855 | 2,455e-02 | 2,622 | 0,00217 | A |
| 50 | 618,929 | 6,040e-02 | 1,920 | 0,00155 | A |
| 51 | 631,467 | 3,476e-02 | 2,363 | 0,00187 | A |
| 52 | 649,593 | 4,150e-03 | 2,458 | 0,00189 | A |
| 53 | 658,181 | 5,430e-03 | – | – | Ü |
| 54 | 662,214 | 8,479e-03 | 1,757 | 0,00133 | A, N |
| 55 | 675,244 | 2,040e-02 | 2,142 | 0,00159 | A |
| 56 | 706,481 | 7,231e-03 | 2,632 | 0,00186 | A |
| 57 | 730,954 | 1,480e-02 | 2,691 | 0,00184 | A |
| 58 | 742,777 | 5,311e-03 | – | – | Ü |
| 59 | 746,496 | 4,364e-03 | – | – | Ü |
| 60 | 751,302 | 4,029e-03 | – | – | Ü |
| 61 | 762,547 | 5,760e-03 | 2,867 | 0,00188 | A |
| 62 | 788,328 | 7,759e-03 | 3,544 | 0,00225 | A, N |
| 63 | 797,551 | 3,148e-03 | 4,486 | 0,00281 | A, N |
| 64 | 817,453 | 6,388e-03 | 4,548 | 0,00278 | A |
| 65 | 834,948 | 4,880e-03 | 5,105 | 0,00306 | N |
| 66 | 845,052 | 2,414e-03 | – | – | Ü |
| 67 | 864,379 | 3,290e-03 | 3,702 | 0,00214 | A |
| 68 | 878,991 | 2,008e-03 | 4,219 | 0,00240 | A |
| 69 | 897,701 | 3,956e-03 | – | – | Ü |
| 70 | 907,687 | 1,846e-02 | 2,442 | 0,00134 | A |
| 71 | 934,878 | 8,238e-03 | 3,873 | 0,00207 | A |
| 72 | 964,131 | 1,900e-02 | 3,655 | 0,00190 | A |
| 73 | 1003,424 | 6,786e-03 | – | – | Ü, M7 |
| 74 | 1006,411 | 6,420e-03 | – | – | Ü, M7 |
| 75 | 1018,810 | 8,578e-03 | 3,389 | 0,00166 | A, M7 |
| 76 | 1031,689 | 6,903e-03 | 3,870 | 0,00188 | A, M7 |
| 77 | 1053,017 | 9,639e-03 | – | – | Ü, M7 |
| 78 | 1059,084 | 1,652e-02 | 4,714 | 0,00223 | N, M7 |
| 79 | 1065,077 | 1,172e-02 | – | – | Ü, M7 |
| 80 | 1085,760 | 8,700e-03 | 6,872 | 0,00316 | N, M7 |
| 81 | 1101,736 | 1,377e-02 | 3,598 | 0,00163 | A, M7 |
| 82 | 1141,431 | 6,962e-03 | 9,223 | 0,00404 | N, M7 |
| 83 | 1161,388 | 5,638e-03 | 3,799 | 0,00164 | A, M7 |
| 84 | 1192,815 | 5,707e-03 | 6,936 | 0,00291 | N, M7 |
| 85 | 1209,316 | 9,388e-03 | 5,529 | 0,00229 | N, M7 |
| 86 | 1265,633 | 2,402e-03 | 4,671 | 0,00185 | A, M7 |
| 87 | 1284,418 | 2,847e-03 | 11,529 | 0,00449 | N, M7 |
| 88 | 1325,549 | 8,973e-03 | – | – | Ü, M7 |
| 89 | 1329,352 | 9,627e-03 | – | – | Ü, M7 |
| 90 | 1348,233 | 1,314e-02 | 5,198 | 0,00193 | M7 |
| 91 | 1424,081 | 7,052e-03 | 7,785 | 0,00273 | N, M7 |
| 92 | 1446,462 | 7,070e-03 | 8,718 | 0,00301 | N, M7 |
| 93 | 1466,060 | 5,585e-03 | 7,628 | 0,00260 | N, M7 |
| 94 | 1508,379 | 8,850e-03 | – | – | Ü, M7 |
| 95 | 1513,996 | 7,539e-03 | – | – | Ü, M7 |
| 96 | 1544,669 | 7,330e-03 | 7,405 | 0,00240 | M7 |
| 97 | 1579,352 | 1,318e-02 | 8,546 | 0,00271 | M7 |
| 98 | 1612,074 | 1,334e-02 | 9,819 | 0,00305 | M7 |
| 99 | 1733,700 | 4,983e-03 | 9,375 | 0,00270 | M7 |
| 100 | 1764,373 | 5,528e-03 | 14,708 | 0,00417 | N, M7 |
| 101 | 1838,160 | 7,492e-03 | 6,566 | 0,00179 | M7 |
| 102 | 1893,286 | 6,159e-03 | 7,994 | 0,00211 | M7 |
| 103 | 1920,724 | 1,640e-02 | 13,083 | 0,00341 | N, M7 |
| 104 | 1973,724 | 6,401e-03 | – | – | Ü, M7 |
| 105 | 2008,959 | 7,741e-03 | 7,260 | 0,00181 | M7 |
| 106 | 2032,122 | 5,111e-03 | 4,606 | 0,00113 | A, M7 |
| 107 | 2071,816 | 5,390e-03 | – | – | Ü, M7 |
| 108 | 2075,252 | 5,569e-03 | – | – | Ü, M7 |
| 109 | 2169,876 | 6,934e-03 | 7,605 | 0,00175 | M7 |
| 110 | 2230,933 | 9,041e-03 | – | – | Ü, M7 |
| 111 | 2238,702 | 9,083e-03 | – | – | Ü, M7 |
| 112 | 2261,204 | 9,449e-03 | 5,277 | 0,00117 | M7 |
| 113 | 2302,952 | 8,635e-03 | 8,525 | 0,00185 | M7 |
| 114 | 2420,973 | 4,536e-03 | 8,294 | 0,00171 | M7 |

**Betriebsschwingform** an der höchsten Spitze (262,58 Hz → Linie 167, 262,5 Hz, Quelle CPH zu
Ref1): größter `betrag_3d_psv` 8,32·10⁻⁴ m/s (Spitzenwert).

**Abbildungen** (`in_progress/analysen/abbildungen/W5-1/`, je PDF und PNG; nach dem Commit mit sauberem Git-Hash neu erzeugen): `frf_Vib_Z__Ref1`,
`spektren_Vib_Z__Ref1`, `frf_Ref2__Ref1`, `spektren_Ref2__Ref1`, `schwingform`.

## 6 Offene Punkte

- Ablageort für Exporte realer Messungen (113 MB je Datei; nicht ins Git).
- KONVENTIONEN „Hilfswerkzeuge … importieren nicht aus dem Hauptpaket“: `beispiel_svd.py`
  verbindet Werkzeug (W2-Leser) und Hauptpaket und importiert deshalb aus beiden.
- Dezimalkomma in Achsbeschriftungen der Abbildungen ist nicht umgesetzt (Thesis-Formalien).

## 7 Korrekturpaket K-W5-1 (2026-10-30)

| Punkt | Umsetzung | Test (`tests/auswertung/`) |
|---|---|---|
| K1-1 Vorzeichen je Kanal | `Annahmen.vorzeichen_kanal`, `daten.bereite_paar` (s_a·s_b), `Paardaten.vorzeichen_antwort/_referenz`, Export | `test_aw_rf_frf::test_rf_h8_vorzeichen_je_kanal` (3 Fälle, inkl. `spektrum_kohaerent`), `test_rf_h8_kanal_in_zwei_rollen`, `test_rf_h8_konjugation_…`; `test_aw_korrektur_k1::test_k1_1_…` (Vib fest +1; gedrehter Ref2 → P-08 warnt, mit s_Ref2 = −1 ok) |
| K1-6 Fehlerband | `frf.fehlerband`, `FrfErgebnis.h1_band_aussagekraeftig`, Hinweis „Fehlerband nicht aussagekräftig“ | RF-U7 `test_rf_u7_…` (2) |
| K1-7 γ² vollständig NaN | `spitzen.suche_spitzen` Hinweis „Kohärenz nicht prüfbar“ | `test_k1_7_…` |
| K1-8 M7-Vergleich | `Toleranzen.spitze_stimmt`, `breite_stimmt` | `test_k1_8_…` |
| MAJOR fehlende Prüfungen | `plausibilitaet.pruefe_eingang`, `nicht_pruefbar`, `gesamt.werte_aus` | `test_major_…` (3) |
| MINOR 2 M4/M11 | `Annahmen.skalierung`, `Annahmen.toleranzen`, `Toleranzen.beschreibung` | `test_minor2_…` |
| MINOR 3 Pfad, Kennzeichen, Einheiten | `svd_adapter` (absoluter Pfad), `Bandwert.kennzeichen`, `daten.einheit_quadrat/_produkt` | `test_minor3_…` (3) |
| MINOR 4 NaN Prominenz | `spitzen.kandidaten` (`nanmin` beidseitig) | `test_minor4_…` (3) |
| MINOR 5 Imaginärteil | `svd_adapter._reell` | `test_minor5_…` |
| NITPICK 6 atomarer Export | temporäre Dateien, `os.replace` | `test_nitpick6_…` |
| NITPICK 7 Kohärenz in Spektren-Abbildung | `abbildungen.bild_spektren` | `test_abbildung_mit_niedriger_kohaerenz_…` |
| NITPICK-1 (FA) P-09 je Referenz | nicht umgesetzt (F15) | – |
