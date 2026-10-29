<!-- Analysebericht W2: Aufbau der Polytec-PSV-Messdatei (.svd) und Prototyp-Leser ohne Polytec File Access; erstellt im Paket W2 von software-engineer. Stand 2026-10-29, überarbeitet nach Review R-W2 (Korrekturpaket K-W2). -->

# W2 – Aufbau einer PSV-Messdatei (`.svd`) und Prototyp-Leser

**Gegenstand.** `Input/20261012_ref_Mitte.svd` (27 115 520 Byte,
SHA-256 `7ef46262df0055f5a45470ae0fc5e6bde547624cdee6b5dc3838060a452e790b`), Messung des
Betreuers vom 12.10.2026. Die Datei wurde nur lesend geöffnet; der SHA-256 ist vor und nach
dem Lesen gleich (Test `test_echte_datei_plausibel_und_unveraendert`).

**Ergebnis in einem Satz.** Die Messdaten lassen sich ohne Polytec File Access vollständig
lesen: Die Datei enthält je Messpunkt 17 gemittelte Spektren (Kreuz-, Auto- und
Betragsspektren aus 3D-Vibrometer und zwei Referenzen), dazu von PSV gespeicherte Punktmittel
und Bandwerte je Punkt. An diesen PSV-eigenen Größen ist die Dekodierung auf float32-Genauigkeit
(relative Abweichung ≤ 9,3·10⁻⁷) nachgeprüft. Offen sind vor allem das Phasenvorzeichen der
Kreuzspektren, der genaue Bezug der Frequenzachse (Index 0 = Linie 1?) und mehrere
Einstellungsfelder.

> **Überarbeitet nach Review R-W2 (K-W2):** Rollen Antwort/Referenz jetzt aus der
> Signalformel, Banddaten nur Gegenprobe (2.1); Punktzuordnung zur Geometrie mit eigener
> Prüfung belegt (2.4); Prüfungsanzahl und -zusammensetzung korrigiert (72); Jensen-Prüfung
> implementiert; Skalierungsfolgerung eingeschränkt; Blockdauer-Abgleich (2.2); Zeitstempel
> naiv (Zeitzone offen).
>
> **Zweite Korrekturrunde (K-W2b):** Kanalzuordnung über unabhängige Anker statt
> Static_Info-Reihenfolge (2.1); Punktzuordnung über das Satzfeld +0x8C als Anker, die
> Geometrieprüfung ist nur noch Gegenprobe, ihre Grenzen sind benannt (2.4); 73 Prüfungen.

**Sicherheitsgrade.**
- **gesichert:** mindestens zwei unabhängige Belege an der echten Datei.
- **plausibel:** ein Beleg oder eine Konsistenzbeobachtung.
- **offen:** nicht dekodiert oder unbelegt.

Die Polytec-Doku (I5, CHM-Textfassung) dient nur als Hinweis, nicht als Formatspezifikation.

---

## 1 Container

| Aussage | Beleg | Grad |
|---|---|---|
| OLE-Verbunddokument (Compound File Binary V2), Codepage 1200 (UTF-16), Locale 1031 (de-DE) | `file`; `olefile` öffnet die Datei fehlerfrei | gesichert |
| 282 Streams, 62 Storages, Summe der Stream-Längen 26 896 839 Byte | `olefile.listdir` | gesichert |
| Zahlen little-endian; Zeichenketten UTF-16LE mit vorangestellter `int32`-Bytelänge inkl. Endnull | alle dekodierten Zahlen und Texte ergeben Sinn | gesichert |
| `SummaryInformation`: Autor „Messadmin“, sonst leer | `olefile.get_metadata` | gesichert |
| `Swol20jsF2qze5s51atq5xqvBh` (Property-Set): Eigenschaft „AvgCorrected“, Wert `0xFFFF` (VT_BOOL wahr) | Hexdump | plausibel; passt zu `IsAverageSpectrumCorrected` ([BEM] I5 4.4) |

### 1.1 Stream-Übersicht

| Stream (`<n>` = Nummer) | Anzahl | Länge [Byte] | Inhalt (Kurzfassung) | Grad |
|---|---|---|---|---|
| `SummaryInformation` | 1 | 184 | OLE-Zusammenfassung | gesichert |
| `Swol20jsF2qze5s51atq5xqvBh` | 1 | 152 | Property-Set „AvgCorrected“ | plausibel |
| `FileVersion` | 1 | 32 | `int32` 2, 4, 2624, 2, 1, `uint16` 4, 10, FILETIME 2026-10-12 09:32:52 | offen (4 = `ptcPSVFile`? „10.4“?) |
| `Polytec_Data/M<n>/Signal_Info` | 17 | 12 | Version 1, Punkte 135, Nutzbytes je Punkt (12 800 bzw. 6 400) | gesichert |
| `Polytec_Data/M<n>/ManyStreamsInfo` | 17 | 2188 | Satzlänge, Punktanzahl, Ablageplatz je Punkt | gesichert |
| `Polytec_Data/M<n>/ManyStreamsData-0` | 17 | 914 768 / 1 778 768 | 135 Punktdatensätze mit float32-Spektren | gesichert |
| `Polytec_Data/M<n>/Static_Info` | 17 | 336–560 | Kanalnamen (lang/kurz), Signalformel, zweimal | gesichert |
| `Polytec_Data/M<n>/Media_Type` | 17 | 120 | drei GUIDs `D8174C60…62-FE3D-11D2-8E84-00104BB924B2`, Zahlen (8 bzw. 4 = Bytes je Linie?) | offen |
| `AvgSeq_Data/<n>/Corrected_Signal` | 35 | 6434 | Punktmittel, 34 Byte Kopf + 1600 float32 | gesichert |
| `AvgSeq_Data/<n>/Static_Info` | 35 | 184–440 | Formel des Punktmittels | gesichert |
| `AvgSeq_Data/<n>/Media_Type`, `Signal_Info` | je 35 | 120, 12 | wie oben; `Signal_Info` hier 1, 0, 0 | offen |
| `Band_Data/Entire_Bandwidth/FB0/S<n>-0` | 29 | 552–763 | zlib; Signalbeschreibung **mit Namen und Einheiten** + 135 Bandwerte (ABS/CPH: Effektivwert √(Σ\|A\|²/2); AP/CP: Σ\|X\|/2) | gesichert |
| `Band_Data/Entire_Bandwidth/FB0/BandInfo-0` | 1 | 35 | zlib; 1600, 2, 29, float32 0,625 und 1000 | offen |
| `Info/DAQ_Settings_Fft/Fft` | 1 | 52 | Bandbreite 2500 Hz, 1600 Linien, 4000 Abtastwerte; zweimal float64 1000 | teils gesichert, Rest offen |
| `Info/DAQ_Settings_Fft/VibrometerControllers` | 1 | 7228 | Klartext-XML Controller/Sensorkopf + Binärteil | XML gesichert, Rest offen |
| `Info/DAQ_Settings_Fft/Channels` | 1 | 3436 | Kanäle Vib 3D, Ref1…Ref8, je Kanal Zahlenfelder (u. a. float64 40,306 bei Ref1, 97,85 bei Ref2) | Namen gesichert, Zahlen offen |
| `Info/DAQ_Settings_Fft/Average`, `Trigger`, `Generators`, `Global`, `FrontEnd`, `SignalEnhancement`, `Vibrometers` | je 1 | 13–206 | Einstellungen, siehe 3.4 | offen |
| `Info/Geometry/MeasPoints` | 1 | 8737 | 135 Punktsätze zu 64 Byte | teils plausibel |
| `Info/Geometry/Elements` | 1 | 2248 | 112 Vierecke, 0-basierte Punktindizes | plausibel |
| `Info/Geometry/Components` | 1 | 40 | Komponente „Ursprung“ | offen |
| `Info/HardwareConfig2`, `Info/ScanHead` | je 1 | 296, 267 | Seriennummern, Kopftypen, Firmware (Text) | Text gesichert, Zuordnung plausibel |
| `Info/HardwareConfig`, `CameraSettings`, `AlignmentsCamera`, `APS_Mixed/*` | je 1 | 8–5250 | Hardware-ID, Kamera, Abgleich, Mesh | offen |
| `Info/VideoBitmap` | 1 | 180 550 | JPEG (JFIF ab Byte 26) | plausibel, nicht ausgelesen |
| `Info/VideoSettings` | 1 | 1 322 481 | enthält BMP- und zlib-Blöcke | offen |

**Nicht enthalten:** Zeitdaten (keine Formel mit Zeitdomäne als Ergebnis, nur `AVG[...]`
über Spektren), Benutzersignale, gespeicherte FRF- oder Kohärenzspektren je Punkt.

---

## 2 Kodierung der Messdaten

### 2.1 Signale je Punkt (`Polytec_Data/M<n>`)

**Formelsprache (`Static_Info`).** `T[i]` = Zeitkanal i (0, 1, 2 = 3D-Komponenten X/Y/Z,
3 = Ref1, 4 = Ref2), `3DX[...]` = X-Komponente, `S[...]` = Spektrum, `AVG[...]` = Mittelung,
`CP[a,b]` = Kreuzspektrum, `AP[a]` = Autospektrum, `ABS[a]` = Betrag, `FRF`, `COH`,
`AVGSEQ[...]` = Mittel über Punkte. Gesichert über die Rechenprüfungen in 2.4.

| M | Art | Kanäle (Antwort/Referenz) | Formel | Bezeichnung und Einheit laut Banddaten |
|---|---|---|---|---|
| 0, 2, 4 | CP | Vib X/Y/Z – Ref1 | `AVG[CP[S[3DX[T[0]]],S[T[3]]]]` | „CP Kraft * Geschwindigkeit“, N · m/s |
| 1, 3, 5 | CPH | Vib X/Y/Z (– Ref1) | `AVG[CPH[S[3DX[T[0]]],CP[...]]]` | „Geschwindigkeit“, m/s |
| 6 | CP | Ref2 – Ref1 | `AVG[CP[S[T[4]],S[T[3]]]]` | „CP Kraft * Beschleunigung“, N · m/s² |
| 7 | CPH | Ref2 (– Ref1) | `AVG[CPH[S[T[4]],CP[...]]]` | „Beschleunigung“, m/s² |
| 8 | ABS | Ref1 | `AVG[ABS[S[T[3]]]]` | „Kraft“, N |
| 9, 10, 11 | AP | Vib X/Y/Z | `AVG[AP[S[3DX[T[0]]]]]` | „AP Geschwindigkeit²“, (m/s)² |
| 12 | AP | Ref1 | `AVG[AP[S[T[3]]]]` | „AP Kraft²“, N² |
| 13 | AP | Ref2 | `AVG[AP[S[T[4]]]]` | „AP Beschleunigung²“, (m/s²)² |
| 14, 15, 16 | CP | Vib X/Y/Z – Ref2 | `AVG[CP[S[3DX[T[0]]],S[T[4]]]]` | „CP Beschleunigung * Geschwindigkeit“, m/s² · m/s |

**Rollen Antwort/Referenz (aus der Formel).** `Static_Info` nennt die Kanäle nach
aufsteigender Zeitkanalnummer, **nicht nach Rolle** (M6/M7: „Ref1, Ref2“, Formel
`CP[S[T[4]],S[T[3]]]`, also Antwort Ref2). Der Leser leitet die Rolle deshalb aus der Formel
ab: `CP[Antwort, Referenz]`, `CPH[S[Antwort], CP[Antwort, Referenz]]`, `AP[Kanal]`,
`ABS[Kanal]`. Die Zuordnung Zeitkanalnummer `T[i]` ↔ Kanalname stützt sich **nicht** auf die
Static_Info-Reihenfolge, sondern auf zwei unabhängige Anker:

1. **Kanaleinstellungen** `Info/DAQ_Settings_Fft/Channels`: Kanäle in Kanalreihenfolge als
   Paare (Kurz-, Langname); ein 3D-Kanal belegt drei Zeitkanäle. Ergebnis an der Datei:
   Vib X/Y/Z = 0/1/2, Ref1 = 3, Ref2 = 4 (Ref3…Ref8 = 5…10), passend zu allen 17 Formeln
   (plausibel).
2. **Namensordnung** Vib X < Vib Y < Vib Z < Ref1 < Ref2 < … (relative Ordnung).

Liegen beide vor, müssen sie übereinstimmen, sonst `SvdFormatFehler`; fehlt jeder Anker
(z. B. Kanalnamen ohne Nummer und ohne Kanaleinstellungen), ebenfalls `SvdFormatFehler`.
Zusätzlich müssen 3D-Komponenten zum Namen passen („Vib X“ zu `3DX`). Tests: vertauschte
Static_Info-Reihenfolge (Ref2 vor Ref1) ohne Banddaten liefert M6/M7 = (Ref2, Ref1); ein
widersprüchlicher Kanalanker (Ref2 vor Ref1 in `Channels`) bricht ab; die echte Datei wird
unverändert gelesen.

**Kanäle und Einheiten.** Ref1 ist eine Kraft (N), Ref2 eine Beschleunigung (m/s²), die
Vibrometerkomponenten Geschwindigkeiten (m/s). Quelle sind die deutschen Klartexte in den
Banddaten („Kraft“, „N“, „Beschleunigung“, „m/s²“). Einheit und Titel übernimmt der Leser
aus `S<n>` nur nach einer **Gegenprobe**: Kanäle in Rollenreihenfolge gleich der Formel (bei
CPH nur die Antwort) und Titelanfang passend zur Signalart („CP …“, „AP …“, bei ABS/CPH ohne
Präfix). Widerspruch führt zu `SvdFormatFehler` (Test: vertauschte Bänder S8/S12 → Abbruch).
Fehlen Banddaten, bleibt die Einheit `None`. **Grad: Einheiten plausibel** (Text aus der
Datei, aber nicht aus dem Signal-Stream selbst).

**Bedeutung von CPH (plausibel).** Eine Regression über alle 216 000 Werte ergibt
|CPH| ≈ |CP| / √AP_Ref (Exponenten 0,9985 bzw. −0,4991, Streuung 3 %); die Phase von CPH
stimmt mit der von CP überein (Median der Differenz −3·10⁻⁷ rad). Zusammen mit der
Banddaten-Bezeichnung „Geschwindigkeit [m/s]“ heißt das: CPH ist das gemittelte
Antwortspektrum mit der Phase relativ zur Referenz, etwa Mittel(X · R*/|R|). Es erfüllt
|CPH| ≤ √AP_X an allen Punkten und Linien (Maximum 0,99999). Das entspricht dem in PSV
angezeigten „Geschwindigkeit“-Spektrum eines Vib-Kanals.

### 2.2 Layout `Signal_Info`, `ManyStreamsInfo`, `ManyStreamsData-0`

| Feld | Kodierung | Beleg | Grad |
|---|---|---|---|
| `Signal_Info` | `int32` Version 1, Punktanzahl 135 (0x87), Nutzbytes je Punkt 12 800 (komplex) bzw. 6 400 (reell) | 12 800 = 1600 · 2 · 4, 6 400 = 1600 · 4; passt zu Streamlängen | gesichert |
| `ManyStreamsInfo` | `int32`: 1, Satzlänge (13 176 bzw. 6 776), −1, −1, n, Nummern 0…n−1, n, n Paare (Satzlänge − 16, Ablageplatz von Punkt i), n, n × −1 | Ablageplätze sind exakt die Umkehrung der Punktindizes in den Datensätzen (alle 17 Signale) | gesichert |
| `ManyStreamsData-0` | 8 Byte Kopf (`FF FF FF FF 00 00 00 00`), dann n Datensätze in **Scanreihenfolge** (0, 41, 8, 70, …) | Streamlänge = 8 + 135 · Satzlänge exakt | gesichert |
| Satz +0x00 | `int32` 2 (Version) | alle Sätze | plausibel |
| Satz +0x04 | `int32` 3 | `PTCDomainType` Spectrum = 3 | offen (Hinweis) |
| Satz +0x08 | `int32` 1600 = Linien | = `Fft`-Linien, = Nutzbytes/4 bzw. /8 | gesichert |
| Satz +0x20 | `int32` Punktindex 0…134 | Permutation; Umkehrung der Ablageplätze in `ManyStreamsInfo`; Bandwerte je Punkt passen (2.4); Zuordnung zur MeasPoints-Zeile über das Kennfeld +0x8C (2.4) | gesichert |
| Satz +0x34 | `float64` 0,64 = Blockdauer in s | = 1/Δf = 4000/(2,5 · 2500 Hz); in allen Sätzen bitgleich. Der Leser gleicht es gegen die Bandbreite ab (rtol 10⁻⁹), Widerspruch → `SvdFormatFehler` | plausibel |
| Satz +0x3C…0x5C | `float64` 0,04962 / 1,0 / 0,02481 / 1,590 / 1,766 (bei M8: 0,002481 statt 0,04962) | – | offen (Skalier- oder Kalibrierwerte?) |
| Satz +0x6C, +0x74 | zwei FILETIME; Differenz stets genau 0,64 s | erster Punkt 2026-10-12 09:33:06, letzter 10:12:42; Abstand ≈ 17,7 s | plausibel (Bedeutung offen); Zeitzone offen, der Leser liefert **naive** `datetime` |
| Satz +0x8C | `float64` ≈ 10⁻¹⁰…10⁻⁸, je Punkt verschieden (135 verschiedene Werte), in allen 17 Signalen gleich | als `float32` **bitgleich** mit dem Messpunktfeld +0x08 desselben Punktindex, für alle 135 Punkte; bei Versatz um einen Index stimmt kein Punkt | Gleichheit gesichert, Bedeutung offen; dient als Zuordnungsanker |
| Satz +0xF4 | `int32` Nutzbytes | = `Signal_Info` | gesichert |
| Satz +0xF8 | Nutzdaten `float32` LE; komplex **verschränkt** Re₀, Im₀, Re₁, Im₁ … | siehe 2.4 | gesichert |
| Satz-Ende | 128 Byte Nachspann (wiederholt Kopffelder) | Satzlänge = 0xF8 + Nutzbytes + 128 | gesichert (Länge), Inhalt offen |

**Verschränkung gegen Blockablage.** Mit Re/Im verschränkt liegt |CP|²/(AP_X · AP_Ref) für
alle 216 000 Werte in [7·10⁻⁶; 0,99998]. Mit der Alternative „erst alle Re, dann alle Im“
liegen 52 % der Werte über 1 (Maximum 3·10⁷). Das ist mit Polytec File Access konsistent
(„gerade Indizes Real, ungerade Imag“, I5 4.4).

### 2.3 Punktmittel (`AvgSeq_Data`) und Banddaten (`Band_Data`)

- **Punktmittel:** 35 Signale, 34 Byte Kopf (u. a. `int32` 1600, 1599), dann 1600
  `float32`. Formeln: Betragsmittel der 17 Grundsignale sowie für X/Y/Z × Ref1/Ref2 je
  `ABS[FRF[AP_Ref, CP]]` (H1), `ABS[FRF[AP_Antwort, CP]]` (H2) und `COH[H1, H2]`.
- **Banddaten:** 29 Streams (17 Grundsignale + H1/H2 je Richtung und Referenz). Je Stream:
  `uint32` Länge, zlib-Daten. Inhalt: Beschreibung (Titel, je Kanal Name/Größe/Einheit,
  x-Achse „Scanpunktnummer“, y-Größe und y-Einheit), am Ende `int32` 135 und 135 `float32`.

### 2.4 Rechenprüfungen (verifizieren die Dekodierung, Werkzeug `svd_pruefung.py`)

Toleranz `RTOL = 1e-5`: float32-Rundung erzeugt ≈ 6·10⁻⁸ je Wert und nach Mittelung,
Quotienten und Summen wenige 10⁻⁷; ein Lese- oder Zuordnungsfehler läge bei 10⁻² und mehr.

| Prüfung | Ergebnis an der Datei | Was sie belegt |
|---|---|---|
| \|CP\|² ≤ AP_Antwort · AP_Ref (alle 7 CP, alle Punkte und Linien) | Maximum 0,99999 ≤ 1 + 10⁻⁵ | Verschränkung, Kanalzuordnung, AP = mittleres \|A\|² |
| \|CPH\| ≤ √AP_Antwort (4 CPH) | Maximum 0,99999 | CPH-Deutung |
| AP ≥ 0, ABS ≥ 0 (5 AP, 1 ABS) | Minimum 3,5·10⁻¹⁵ bzw. 6,3·10⁻⁴ | reelle Datenart |
| AP_Ref1 / ABS_Ref1² ≥ 1 (Jensen, implementiert) | Minimum 1 − 7,5·10⁻⁸ (≥ 1 − 10⁻⁵), Median 1,00001 | AP und ABS gleich skaliert |
| Band (CP, AP) = Σ\|X\|/2 je Punkt | max. rel. Abweichung 5,8·10⁻⁸ (12 Signale: 7 CP, 5 AP) | Werte; Punktindex der Datensätze = Punktindex der Banddaten |
| Band (ABS, CPH) = √(Σ\|A\|²/2) je Punkt | max. 5,6·10⁻⁸ (5 Signale: 1 ABS, 4 CPH) | Werte; Skalierung siehe unten |
| Punktmittel = Mittel über alle 135 Punkte von \|Signal\|, \|H1\| = \|CP/AP_Ref\|, \|H2\| = \|AP_Antwort/CP*\|, COH = \|CP\|²/(AP·AP) (35 Signale) | max. 9,3·10⁻⁷ | Signal- und Formelsemantik, H1/H2/Kohärenz-Definition wie in PSV, keine Punkte ausgeschlossen |
| Punktzuordnung Kennfeld: float32(Satz +0x8C) = MeasPoints +0x08 je Punktindex | 0 abweichende Punkte von 135; Grenze 0 | Datensatz-Punktindex i gehört zur MeasPoints-Zeile i; erkennt Versatz ±1/±9 (135 Abweichungen) und einzelne Vertauschungen (2 Abweichungen) |
| Punktzuordnung Geometrie (Gegenprobe): mittlere Schrittweite in Scanreihenfolge ÷ kleinste mittlere Schrittweite über 200 zufällige Reihenfolgen (Seed 0) | 0,147 (26 mm gegen ≥ 179 mm); Grenze 0,5 | grobe Fehlzuordnungen; **nicht** einzelne Vertauschungen und **nicht sicher** einen Versatz um einen Index |
| Punktzuordnung Zeit: `zeit_a` in Scanreihenfolge streng steigend | 0 nicht steigende Schritte | **nur** die Scanreihenfolge der Datensätze, nicht den Geometriebezug |

Insgesamt **73 Prüfungen** (6 ≥ 0 + 7 CP + 4 CPH + 1 Jensen + 17 Band + 35 Punktmittel
+ 3 Punktzuordnung), alle durchgeführt und bestanden. Nicht durchführbare Prüfungen (etwa bei
fehlenden Banddaten) meldet `pruefe` als Eintrag „nicht durchführbar: …“ mit Grund; sie gelten
als nicht bestanden.

**Was welche Prüfung belegt.** Ungleichungen und Punktmittel sind gegen eine Vertauschung
der Punkte unempfindlich; sie belegen Werte, Datentyp, Verschränkung und die Definitionen von
H1, H2 und Kohärenz, **nicht** die Punktzuordnung. Die Bandprüfung vergleicht je Punkt und
belegt, dass Datensätze und Banddaten denselben Punktindex verwenden. Die Zuordnung zur
Geometrie (MeasPoints-Zeile) belegt das **Kennfeld** (+0x8C ↔ +0x08): Es ist
permutationsempfindlich bis zur einzelnen Vertauschung, seine Bedeutung ist aber offen; es
belegt die Zuordnung nur, solange die Werte je Punkt verschieden sind (in der Datei: 135
verschiedene Werte).

Die Geometrieprüfung ist nur Gegenprobe. Ihre Grenzen: Zwei vertauschte Punkte ändern die
mittlere Schrittweite kaum (Reviewer-Beleg: 0,165 statt 0,164, bestanden). Ein Versatz um
einen Index ist geometrisch nur dann auffällig, wenn die Scanreihenfolge quer zur
Indexreihenfolge springt; in der Beispieldatei wäre er erkennbar (Mittelwert 26 mm gegen
70 mm), bei einem Raster mit spaltenweisem Zickzack-Scan und zeilenweisem Index dagegen kaum
(synthetischer Test). Ein eigener Versatzvergleich wurde deshalb nicht als Prüfung
aufgenommen; ein solches Kriterium hätte bei korrekten Dateien mit anderem Scanmuster falsch
angeschlagen. Die Zeitprüfung belegt nur die Scanreihenfolge der Datensätze. Tests: Versatz
±1 und ±9 sowie einzelne Vertauschung → Kennfeldprüfung schlägt an; zufällige Permutation →
Kennfeld- und Geometrieprüfung schlagen an; umgekehrte Zeitstempel → Zeitprüfung schlägt an.

**Skalierung (plausibel unter Annahme).** Unter der Annahme, dass der PSV-Bandwert
„Entire Bandwidth“ für Amplitudenspektren der Effektivwert ist, folgt aus
Band = √(Σ\|A\|²/2), dass die Spektren Spitzenwerte (0-to-peak, einseitig) sind, wie in
KONVENTIONEN angenommen. Belegt ist damit nur die Deutung innerhalb von PSV, nicht die
absolute Kalibrierung. Dafür fehlt ein Export mit bekannter Amplitude (M4).

**Phasenvorzeichen (offen).** Alle Prüfungen nutzen nur Beträge. Ob CP = Mittel(X · R*) oder
Mittel(X* · R) ist, ob also die Phase von H1 = CP/AP_Ref das Vorzeichen der PSV-Anzeige hat,
ist **nicht belegt** (Prüfschritt M1).

---

## 3 Inhalt der Messung

### 3.1 Frequenzachse

| Größe | Wert | Grad |
|---|---|---|
| Bandbreite | 2500 Hz (`Fft` +0x04, float64) | gesichert: 1600 Linien in Einstellung und Daten, Blockdauer 0,64 s = 1/Δf im Datensatz |
| Linien | 1600 | gesichert |
| Δf | 2500 Hz / 1600 = 1,5625 Hz | gesichert (folgt) |
| Abtastwerte je Block | 4000 (= 2,5 · 1600; f_s = 6250 Hz) | plausibel (passt zu f_s = 2,5 · BW, I5 4.4) |
| Achse | f_k = k · Δf, k = 1 … 1600 (1,5625 … 2500 Hz) | **plausibel/vorläufig**: Daten enthalten genau 1600 Linien (Vollbereich); ob Index 0 die Linie 1 (ohne DC) ist, belegt die Datei nicht. Die beiden float64 1000 in `Fft` und die float32 0,625/1000 in `BandInfo` sind nicht gedeutet |

Der Leser liefert die Achse nach KONVENTIONEN (k = 1 … n) und kennzeichnet sie als vorläufig.

### 3.2 Messpunkte und Geometrie

- **135 Punkte**, Raster 9 × 15, Labels 132 … 350 (nicht fortlaufend: 132–139, 161–168, …;
  Schrittweite 29 je Zeile). Label = in PSV angezeigte Nummer (plausibel, I5 1.7).
- **Koordinaten** (float32, `MeasPoints` +0x10): x 0,190 … 0,386, y −0,057 … 0,427,
  z −0,231 … −0,214. Einheit **m plausibel**: Kantenlängen der Elemente 23 … 37 mm
  (Median 29 mm), passend zu einem Plattenraster. Bezugssystem (3D-Abgleich) offen.
- **Elemente:** 112 Vierecke über 0-basierte Punktindizes; im Kontrollbild verbinden alle
  Kanten nur Nachbarpunkte (plausibel).
- **Punktsatz 64 Byte:** Label, `int32` (1 bei 18 Punkten, 3 bei 117 Punkten; Hypothese
  Scanstatus Valid bzw. Valid | Optimal, „Optimal“ gibt es nur mit Signal Enhancement,
  I5 4.5), `float32` klein (bitgleich mit Satzfeld +0x8C, Zuordnungsanker, Bedeutung offen), `uint32` 8193 (Hypothese Geometriestatus Valid | VideoTriangulated),
  xyz, zwei Videokoordinaten (0,61…0,69 / 0,34…0,60), `uint32` 129 (Hypothese Fokusstatus
  Valid | Auto), drei Fokuswerte 6441…7175 (Grenze laut XML 0…8000), 0, `float32`,
  `uint32` 7…25 (7 bei 102 Punkten; Hypothese Anzahl Mittelungen). **Alle Statusdeutungen
  offen**; der Leser reicht sie nur roh durch.

### 3.3 Geräte und Einstellungen (Klartext)

- Controller PSV-F-600-3D, Seriennummer 356929, Firmware 2.50, Decoder DV-03; Messbereich
  **50 mm/s**, **Bandbreitenbereich 1 kHz**, Filter Off/Tracking; Sensorkopf A PSV-I-680
  (SN 360783, Laserwellenlänge 1549,7 nm, `LaserPower` 3,33 ohne Einheit). `HardwareConfig2`: Köpfe 360783/360784/360785,
  PSV-I-680 und zweimal PSV-I-690. Das XML beschreibt nur Kopf A; die übrigen Köpfe stehen
  im Binärteil (offen).
- Hinweis zur Messung (nicht zur Dekodierung): Bandbreitenbereich 1 kHz am Decoder, aber
  FFT-Bandbreite 2500 Hz. Ob das Vibrometersignal oberhalb 1 kHz gedämpft ist, sollte der
  Betreuer bestätigen (Prüfschritt M7).

### 3.4 Nicht gedeutete Einstellungen (Hypothesen, offen)

| Stream | Rohwerte | Hypothese |
|---|---|---|
| `Average` | `int32` 1, 2, 0, 7 | Mittelungsart 2 = Complex (`PTCAverageType`), Anzahl 7 |
| `Trigger` | `int32` 4, 1, … 5 | Quelle 1 = External? |
| `Generators` | `int32` …, 5; float64 0,02 / 0,4 / 100 / 2000 / 2500 / 1000 | Signalform 5 = BurstChirp, 100–2000 Hz? Die Kraftspektren sind aber bis 2500 Hz breitbandig; widerspricht der Deutung teilweise |
| `SignalEnhancement` | 1, 1, 5, …, 10,0, 1,0 | aktiv? |
| `Channels` | je Kanal u. a. 10,0 und 40,306 (Ref1) bzw. 97,85 (Ref2), Codes 12/18/13 | Empfindlichkeiten der Aufnehmer? |
| `Media_Type` | GUID-Familie `D8174C6x-FE3D-11D2-8E84-00104BB924B2`, Feld 8 bzw. 4 | Bytes je Linie (komplex/reell) |

---

## 4 Einordnung gegen die Polytec-Dokumentation (nur Hinweis)

- PFA beschreibt Domänen/Kanäle/Signale/Displays (I5 4.3). In der Datei liegen nur die
  **Grundgrößen** der FFT-Domäne; Kanäle „Vib X/Y/Z“, „Ref1“, „Ref2“ entsprechen den
  Build-Flags `ptcBuildPointDataXYZ`. FRF (H1, H2) und Kohärenz liegen laut Doku in
  Kombikanälen „Vib & Ref n“ (I5 4.3); in der Datei werden sie nicht je Punkt gespeichert,
  sondern beim Lesen aus CP und AP gebildet. Unsere Rechnung reproduziert die von PSV
  gespeicherten Punktmittel von |H1|, |H2| und Kohärenz.
- PFA liefert Arrays als `Single` (float32) und verschränkt Real/Imag (I5 4.4); die Datei
  speichert genau so.
- Punktindex 0-basiert in den Datensätzen, PFA-Collections 1-basiert, Arrays 0-basiert
  (I5 1.6/1.7): Unser `index` = PFA-Index − 1 (Hypothese, Prüfschritt M3).
- „Bänder: ein Wert je Messpunkt, Band Entire Bandwidth“ (I5 4.4) stimmt mit `Band_Data`.
- `IsAverageSpectrumCorrected` (I5 4.4) entspricht vermutlich „AvgCorrected“ im Property-Set.

---

## 5 Prototyp-Leser (A2)

`software/tools/svd_analyse/`: `svd_lesen.py` (Dekodierung, `lese_svd`, Übersicht),
`svd_pruefung.py` (73 Plausibilitätsprüfungen), `kontrollplots.py` (Bilder), `README.md`.
Abhängigkeiten in der neuen uv-Gruppe `werkzeuge` (numpy, olefile, matplotlib).
Abweichungen vom Layout führen zu `SvdFormatFehler`. Ausgabe der Übersicht siehe Rückmeldung.

**Kontrollbilder** (`in_progress/analysen/abbildungen/`, Fußzeile mit Skript und SHA-256):

| Datei | Datenart | Beobachtung |
|---|---|---|
| `w2_kontrolle_spektren_reell.png` | AP (Vib X/Y/Z), ABS und √AP (Ref1) | Z-Komponente 1–2 Dekaden über X/Y (Platte, Anregung normal zur Fläche); ABS und √AP der Kraft decken sich |
| `w2_kontrolle_spektren_komplex.png` | CP, CPH an Punktindex 0 (Label 132) | gleiche Phasenverläufe; Phasensprünge an Resonanzen |
| `w2_kontrolle_punktmittel.png` | AvgSeq 0, 9, 17, 19 gegen eigenes Mittel | deckungsgleich; Kohärenz < 0,5 nur unter ≈ 150 Hz |
| `w2_kontrolle_geometrie_band.png` | Geometrie, Elemente, Band S1 (Effektivwert Geschwindigkeit X) | 9 × 15-Raster, glatte räumliche Verteilung |

---

## 6 Offene Punkte – Prüfschritte am Messrechner (A4)

Voraussetzung: dieselbe Datei `20261012_ref_Mitte.svd` in PSV (Auswertemodus) bzw. per
Polytec File Access, **nur lesend** (Kopie öffnen).

| Nr. | Frage | Prüfschritt | Erwartung, falls Hypothese stimmt |
|---|---|---|---|
| M1 | Phasenvorzeichen von CP/H1 | Punkt Label 132, Kanal „Vib X & Ref1“, Signal H1 Geschwindigkeit/Kraft, Display Real & Imag. bzw. Phase: drei Linien notieren (z. B. 100, 500, 1000 Hz) oder ASCII-Export; vergleichen mit `H1 = M0/M12` aus dem Leser | Phase gleich (CP = X·R*) oder gespiegelt (dann konjugieren) |
| M2 | Frequenzachse: ist Index 0 = 1,5625 Hz? | `XAxis` (Min, Max, Count) per PFA bzw. erste/letzte Frequenz im ASCII-Export; Von/Bis in den Einstellungen ablesen | Min 1,5625 Hz, Max 2500 Hz, Count 1600 |
| M3 | Index vs. Label | PSV-Punktnummer und PFA-`MeasPoint.Index` für Label 132 und 350; Koordinaten eines Punkts | Label 132 = Index 1 (unser 0), Koordinaten in m wie im Leser (0,19089 / 0,42602 / −0,23125 für Index 0) |
| M4 | Absolute Werte und Einheit | ASCII/UFF-Export „Vib X Geschwindigkeit“ (Betrag) für Label 132 bei drei Frequenzen; mit `abs(M1[0])` vergleichen | gleiche Zahlen in m/s (Spitzenwert); sonst Faktor √2 (RMS) o. ä. |
| M5 | Mittelung, Trigger, Generator, Signal Enhancement | Einstellungen in PSV ablesen (Mittelungsart/-anzahl, Triggerquelle, Signalform und Frequenzbereich, SE-Modus) | Average Complex, 7; Rest siehe Tabelle 3.4 |
| M6 | Statusfelder je Punkt | Scanstatus von Label 132 (Wert 3) und einem Punkt mit Wert 1; Anzahl Mittelungen eines Punkts mit Feldwert 25 | 3 = Valid+Optimal, 1 = Valid; Feld = Mittelungsanzahl |
| M7 | Bandbreitenbereich 1 kHz bei 2500 Hz FFT | Betreuer fragen bzw. Vibrometereinstellung ansehen | fachliche Klärung, nicht Dekodierung |
| M8 | Referenzaufnehmer | Typ und Empfindlichkeit von Ref1 (Kraft) und Ref2 (Beschleunigung) notieren | Vergleich mit 40,306 und 97,85 in `Channels` |
| M9 | Zeitstempel | Messzeit in PSV-Info gegen 09:33:06 (FILETIME) | gleich → UTC-Frage klärt die Ortszeit (+2 h) |

Hilfreich: ein ASCII- oder UFF-Export **derselben** Messung mit H1, Kohärenz und
Geschwindigkeit für alle Punkte. Damit wird der Leser gegen PSV als Golden-File testbar.

---

## 7 Grenzen

- Ein einziges Beispiel (FFT-Modus, 3D, zwei Referenzen). Andere Modi, gespeicherte
  Zeitdaten, eingeschränkter Frequenzbereich (Von/Bis), MultiFrame oder Benutzersignale
  können andere Streams oder Layouts haben. Der Leser bricht dann mit `SvdFormatFehler` ab.
- Nicht ausgelesen: Videobild (JPEG), Abgleich, Mesh-Objekte, Binärteil der
  Controller-Einstellungen.
- Die Formelsprache und die Satz-Offsets sind Reverse Engineering; Polytec kann sie mit
  einer neuen PSV-Version ändern (`FileVersion` mitführen).
