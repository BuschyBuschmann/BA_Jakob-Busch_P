<!-- Analysebericht I2 – Messtechnik, Signalverarbeitung, Fachgrundlagen; erstellt im Paket der Input-Sichtung von strukturdynamik-experte (sonnet); unverändert übernommen. Pfadangaben zum Scratchpad verweisen auf flüchtige Hilfsdateien der Cloud-Sitzung. -->

# Fachanalyse I2: Messtechnik und Fachgrundlagen, Polytec PSV QTec 3D

Es wurden keine Dateien im Repository angelegt oder geändert. Hilfsskripte und Textextrakte liegen im Scratchpad `/tmp/claude-0/-home-user/e6b61297-17fb-5003-91f8-95c4534d012c/scratchpad/i2/`.

## 0. Lesehinweise

**Kennzeichnung der Aussagen**
- **[Q]**: in der Quelle belegt.
- **[H]**: eigene Herleitung, im Scratchpad numerisch nachgerechnet.
- **[E]**: eigene Einschätzung, nicht belegt.
- **[U]**: Unsicherheit oder nicht geprüft.

**Quellenkürzel.** "S." ist die PDF-Seite bzw. Folie. Bei Handbüchern steht die gedruckte Seite in Klammern. Alle Dateien liegen unter `Input/literatur/polytec/`.

| Kürzel | Datei |
|---|---|
| F01 bis F11.1 | `Schulungsunterlagen/NN …pdf`, Folien |
| TM | `Handbücher/Theory Manual.pdf` (Dok.-Nr. 41088-Man-Vib-PSV-Theorie-0515-11en, "As of Software 9.1") |
| KA | `Handbücher/Kurzanleitung psv_QTec-3d.pdf` (43695-…-0223-05de) |
| SWA | `Handbücher/Software Handbuch PSV.pdf`, Datenerfassung, Version 10.1 (41584-…) |
| SWP | `Handbücher/Software Handbuch PSV Desktop.pdf`, Auswertung, Version 10.1 (41596-…) |
| VFC / VFS / VFX | VibroFlex Connect Betriebsanleitung / SPECS / Xtra Betriebsanleitung |
| COM | `06_Automatisierung_via_COM/06_Automatisierung_via_COM .pdf` |

SWA und SWP gehörten nicht zum Auftrag. Ich habe sie gezielt herangezogen, weil sie die Konventionen des QTec-3D-Systems (Version 10.1) direkt belegen (siehe 10).

---

## 1. Kernergebnisse

1. **Rolle der Python-Seite.** Die gesamte Signalverarbeitung der Erfassung (FFT, Fenster, Mittelung, H1/H2, Kohärenz) läuft in der PSV-Software. Über COM steuert das Paket diese Software. Es berechnet das Spektrum nicht selbst (COM S.2, S.9). Eigene Spektralschätzung ist nur aus Zeitdaten möglich, und dafür ist die Option "Time Domain Data" nötig (SWA S.242, 7-34). Der eigene Code verarbeitet also Polytec-Ergebnisse weiter und kann Polytec-Werte als Gegenprobe nachrechnen.
2. **Spektren-Konvention.** Polytec skaliert einseitig, amplitudentreu auf die Spitzenamplitude (0-to-peak). Ein Sinus der Amplitude 1 ergibt eine Linie der Höhe 1, auch bei Hanning und Flat-Top (TM S.13, 3-3). Es gelten AP = |S|², PSD = AP/(2·RBW) und RMS = √(ΣAP/(2·W_RBW)) (TM S.14, 17, 18).
   - Das PSD entspricht dem Standard-Einseiten-PSD (Welch, `scaling='density'`) [H].
   - Der Zeitverlauf folgt $A\cos(\omega t+\varphi_0)$ mit komplexer Amplitude $Ae^{i\varphi_0}$ und Zeitabhängigkeit $e^{+i\omega t}$ (TM S.9–10, 2-1/2-2). Das ist konsistent zu `numpy.fft.rfft` [H].
3. **Frequenzachse.** Für Systeme außer M-Systemen gilt Abtastfrequenz = 2,5·Bandbreite (SWA S.225, 7-17, Gl. 7.2). Die Theory-Manual-Beispiele mit 2,56 gelten für M-Systeme. Block = n_FFT/BW, Δf = BW/n_FFT. Die DC-Linie wird nicht gespeichert; Linie k liegt bei k·Δf (indirekt belegt, siehe 3.1).
4. **FRF.** Polytec definiert CP_RV = R*·V, H1 = CP_RV/AP_RR, H2 = AP_VV/CP_VR und COH = H1/H2. Das ist identisch zur Lehrbuchdefinition mit V als Antwort und R als Referenz (TM S.14–15). Die Kohärenzformeln 3.12/3.13 sind Näherungen erster Ordnung. Exakt gilt γ² = (1−N_R/AP_RR)(1−N_V/AP_VV) [H].
5. **Gemitteltes Spektrum.** In der Auswertung ist das "Gemittelte Spektrum" ein Mittel der Beträge der gültigen Punkte und kein komplexes Mittel (SWP S.60, 3-24; S.103, 3-67). Auch "Dämpfung" im Band-Cursor ist ein Begriffs-Stolperstein. Gemeint ist die −3-dB-Breite Δf, mit Q = f_max/Δf und ζ = Δf/(2·f_max) (SWP S.50, 3-14).
6. **3D-Qualität.** Sie hängt am 3D-Abgleich und an der Strahlgeometrie. Die ausgewiesene "Ist-Qualität" allein reicht nicht (SWA S.147, 5-57). Kein Strahl darf in der Ebene der beiden anderen liegen (SWA S.144, 5-54). Für gleichmäßige Rauschverstärkung sind drei zueinander orthogonale Strahlen optimal (≈54,7° zur Flächennormalen) [H]. Polytec empfiehlt 40° bzw. 20° als Kompromiss mit der Rückstreuung (SWA 5-54).
7. **Reproduzierbarkeit.** Kritisch sind gleiche Einstellungen, gleiche Anregung, gleiches Koordinatensystem und gleiche Geometrie, Warmlaufzeit, Fokuswerte und Amplitude am Generatorausgang (siehe 2.3).
8. **Offene Hardwaredaten.** Das Spezifikationshandbuch zum PSV QTec 3D (Messbereiche, Rauschen, Bandbreiten, Signalverzögerung) liegt nicht im Input. Die Zahlen der Folien F01 stammen vom PSV-500, nicht vom QTec.
9. **Widersprüche in den Unterlagen** (siehe 9). Die wichtigsten sind der Faktor 2,5 gegen 2,56, die Fensterempfehlung für Sweep (Flat-Top gegen Hanning) und die Flat-Top-Fehlerangaben.
10. **Zitierbarkeit.** Polytec-Unterlagen sind für gerätespezifische Konventionen zitierfähig, nicht für allgemeine Theorie. Dafür braucht es Fachliteratur (siehe 7, Rechercheaufträge).

---

## 2. Leitfrage 1: Messprinzip und Systemaufbau

### 2.1 Messprinzip

- Die Frequenzverschiebung beträgt $\Delta f = \tfrac{2\,\vec v\cdot\vec e}{\lambda} = \tfrac{2v}{\lambda}\cos\theta$. Das Interferometer (Mach-Zehnder) detektiert die Schwebung (F02 S.16–17, S.22–23).
- Der Cosinus-Fehler 1−cosθ beträgt 1,52 % bei 10°, 6,03 % bei 20° und 13,4 % bei 30° [H]. Die Folie F02 S.17 zeigt die Kurve nur als Bild.
- Beim QTec ist der Messlaser ein IR-Laser mit 1549,7 nm (KA S.48, 3-2) und einer Trägerfrequenz von 40 MHz. Der Pilotlaser hat 520 nm. Ein Dopplershift von 1 m/s entspricht 1,29 MHz [H].
- Die PSV-QTec-Köpfe nutzen die QTec-Mehrkanal-Interferometer-Technologie (F01 S.10). Details zur Demodulation und zu Messbereichen sind für QTec in den Unterlagen nicht enthalten.
- Das Vibrometer liefert die Geschwindigkeit parallel zum Strahl (TM S.78, 13-2). Positive Geschwindigkeit bedeutet Bewegung in Richtung Scankopf (KA S.46, 2-32).
- Weg und Beschleunigung entstehen durch Integration bzw. Differentiation (TM S.56–59, Kap. 9.2). Im Frequenzbereich ist das eine Multiplikation mit $1/(i\omega)$ bzw. $i\omega$ (F03 S.6). Im Zeitbereich wirkt ein FIR-Filter mit einer Verzögerung von einem halben Abtastintervall.

### 2.2 Aufbau des Lab-Systems (laut KA, wahrscheinlich)

- **Komponenten.** 3 Scanköpfe: PSV-I-680 (Top, mit Kamera und Geometrie-Scaneinheit PSV-G-600) und 2× PSV-I-690 (Left/Right). Dazu kommen das Frontend PSV-F-600-3D-H, die Anschlussbox PSV-E-600 und ein Data Management System (PC) (KA S.15–16, 2-1/2-2).
- **Frontend-Anschlüsse.** REF1…REF8 mit IEPE, Generatorausgänge SIGNAL1…4, TRIG IN, SYNC, AUX IN/OUT (KA S.20, 2-6).
- **Optionales Zubehör.** Vibrationsaufnehmer A-VIB-ACC1 zur Kompensation von Umgebungsschwingungen (KA S.16 und S.40, 2-26).
- **Kanäle in der Software.** Der Kanal 1 "Vib 3D" ist immer ein Antwortkanal. Ref1…Ref8 sind wahlweise Referenz oder weiterer Antwortkanal (SWA S.55, 3-11 und S.218, 7-10).
- **Datenübertragung.** Das H-System überträgt voll digital per Ethernet (F01 S.12, KA S.41 und S.43).
- **Betriebsmodi.** Im 1D-Modus (PSV-3D (1D)) liefert jeder Kopf sein Signal ohne Koordinatentransformation (SWA S.50–51, 3-6/3-7). Polytec nennt das ausdrücklich als Plausibilitätstest für den 3D-Modus.
- **Transformation in 3D.** Die Koordinatentransformation geschieht erst beim Zusammenführen der Kanäle, in der Auswertung oder im Signalprozessor (SWA S.291, 9-25). Die Aussteuerungsanzeige im Messbetrieb zeigt die Köpfe einzeln, vor der Transformation (SWA S.78).
- **Zusätzliches Vibrometer.** VibroFlex Connect (VFX-F-110) oder ein anderes Polytec-Vibrometer lässt sich als zweites Vibrometer über Ethernet einbinden (SWA S.258–259, 8-12/13; F05 S.5–8). Die Rolle im Laboraufbau ist offen (siehe 8, Frage 6).
- **Messdaten zum Gerät.**

| Größe | Wert | Quelle |
|---|---|---|
| Aufwärmzeit | 30 min, bei Winkelstabilität 120 min | KA S.46 |
| Betriebstemperatur Scankopf | 0 bis +35 °C (bis +40 °C eingeschränkt) | KA S.47 |
| Geometrielaser | typ. ±2,5 mm | F01 S.11, F08 S.4 |
| Video-Triangulation | ~100–200 µm | F05.1 S.22, F07 S.30 |
| Laserstrahl-Winkel (Sicherheit) | ±25° | KA S.9 |

Die Angaben zum Aufbau stammen aus der Kurzanleitung. Sie gelten für den Gerätetyp PSV QTec 3D-H, die tatsächliche Konfiguration am Laborrechner ist unbestätigt [U].

### 2.3 Was der Nutzer einstellen muss, was fehleranfällig ist, was für Reproduzierbarkeit kritisch ist

| Schritt/Parameter | Wirkung und Risiko | Reproduzierbarkeit | Quelle |
|---|---|---|---|
| Positionierung der drei Köpfe | Gleichseitiges Dreieck. Jeder Strahl muss deutlich aus der Ebene der beiden anderen herausragen. Auftreffwinkel ca. 40° (diffus) bzw. ca. 20° (gerichtet). F05.1 nennt 45° als Empfindlichkeitsoptimum, das ist keine harte Grenze. | Köpfe nicht verändern oder neu abgleichen | SWA S.144 (5-54); F05.1 S.3; KA S.26 (2-12) |
| Kamera und Laser fokussieren, Oberfläche präparieren | Signalpegel. Spray, Glaskugeln oder Retrofolie verbessern den Pegel. Retrofolie bei Abstand < 0,5 m fehlerhaft. | Gleiche Präparation, Autofokus nach Geometrie | F05.1 S.4–5; F08 S.4 |
| 2D-Abgleich | Setzt den Bezug Video zu Spiegelwinkel. Arbeitsabstand und Zoom danach nicht mehr ändern. | Neuer Abgleich bei Änderung | F05.1 S.6–8 |
| 3D-Abgleich | Mindestens 4 Punkte ohne Geometrielaser, mindestens 3 mit. Mindestens 1 Punkt außerhalb der Ebene. Ab PSV 10: automatischer 3D-Abgleich mit Platte PSV-A-655, mindestens 10 QR-Codes sichtbar. | Qualität (Position mm, Winkel mrad) protokollieren. Faustregel 0,1 mrad ≈ 0,1 mm bei 1 m. | F07 S.5–7, S.22–23; SWA S.145–147 |
| Geometrie/Messgitter | Import von Punkten oder STL/UFF, Ausdünnen ist "in jedem Fall erforderlich". Punkte auf Ecken und Kanten schlecht messbar. Importkoordinaten ohne Einheit werden in Metern interpretiert (Faktor 1 = 1 m). | Geometrie als Datei archivieren. Import ändert 3D-Koordinaten der Messpunkte nicht. | F10 S.27–29, S.34, S.44, S.49 |
| Koordinatentransformation (Stitching) | Alle Messungen im gemeinsamen Koordinatensystem. Einstellungen müssen identisch sein, nur Mittelungsanzahl und Geschwindigkeitsbereich dürfen abweichen. Mindestens 4 Transferpunkte. | Prüfbar aus Metadaten | F09.1 S.3–5, S.11; F11 S.35 |
| Fokuswerte | Auto-Fokus an Stützpunkten, Rest aus Geometrie. Fokusschärfe 100 % Standard. | Fokuswerte speichern | F05.1 S.23; SWA S.59 (3-15), S.144–145 |
| Messbereich Vibrometer | Kleinster Bereich ohne Overrange. Aussteuerung ideal 30–80 % (Angabe VFC S.47, 5-3, Übertragbarkeit auf QTec [U]). | Bereich in Metadaten | F06 S.17; VFC S.46–47 |
| Trackingfilter | Überbrückt Dropouts. Bei gutem Signal ausschalten, da Frequenzgangfehler bis 0,25 dB möglich (VFC-Angabe, [U] für QTec). | Einstellung festhalten | F06 S.17; VFC S.47–48 |
| Referenz/Trigger | Phase nur mit Referenz oder Trigger. Das Vibrometersignal darf nicht Trigger sein. | Gleiche Trigger-Logik | TM S.35 (6-5); SWA S.230 |
| Generatoramplitude und Last | Peak-Amplitude in V für hochohmigen Abschluss. Bei 50 Ω Abschluss nur die halbe Spannung. | Last und Amplitude protokollieren | SWA S.240 (7-32) |
| Warten auf stationären Zustand | Verzögerung vor der Messung | Wert protokollieren | SWA S.240 |
| Signal Enhancement und Speckle Tracking | Bis zu 3× (Standard) bzw. 5× (Sehr gut) so viele Mittelungen wie eingestellt. Strahlposition wird um ca. 50 µm bei 1 m verschoben. | Auswirkung auf effektive Mittelungszahl | SWA S.233 (7-25) |
| Overrange-Spektren | Werden aus der Mittelung ausgenommen | Statusverteilung speichern | SWA S.214 (7-6) |

---

## 3. Leitfrage 2: Signalverarbeitung und Konventionen

### 3.1 FFT-Parameter und Frequenzachse

**Formeln [Q]**
- $f_s = 2{,}5\cdot BW$ für alle Systeme außer M-Systemen, $f_s = 2{,}56\cdot BW$ bei M-Systemen (SWA S.225, 7-17, Gl. 7.1/7.2; bestätigt durch SigPro-Parameter "Samplerate/Bandwidth: Standard 2,5; M-Systeme 2,56; VibSoft-20 2,4", SWA S.299, 9-33).
- Messzeit (Blocklänge) $t_{Mess} = n_{FFT}/BW$, Auflösung $\Delta f = 1/t_{Mess} = BW/n_{FFT}$ (SWA S.225, Gl. 7.3/7.4; F06 S.10).
- "Technisches Nyquist": $f_{Abtast} > 2{,}5\,f_{max}$ (F03 S.16).
- Anti-Alias-Filter eingebaut, keine Maßnahme nötig (TM S.21, 4-1).
- FFT-Linien bis 819 200; Von/Bis schränken den Bereich ein (SWA S.225).
- Standardbeispiel der Quick-Start-Tabelle: Bandbreite 10 kHz, 400 Linien, Rechteckfenster, Speckle Tracking, Trackingfilter Slow oder On (SWA S.12, 1-4). Daraus folgt Δf = 25 Hz, T = 40 ms, N = 1000 Samples [H].

**Abgeleitete Größen [H].** Bei n_FFT = 400 sind es N = 2,5·n_FFT = 1000 Samples pro Block; 800 Linien ergeben 2000, 1600 ergeben 4000.
- TM S.13 (3-3) sagt, die Sample-Zahl der FFT müsse eine Zweierpotenz sein. Das passt zu 2,56·n_FFT (M-System), aber nicht zu 2,5·n_FFT [U]. Ob H-Systeme intern anders rechnen, ist offen.
- Im SigPro gilt für die Funktion FFT: Länge mindestens 2·Linien, aufgerundet auf die nächste Zweierpotenz (SWA S.296, 9-30).

**Linienlage [Q indirekt].** Ich leite ab, dass die gespeicherten Linien bei k·Δf mit k = 1…n_FFT liegen und DC fehlt. Belege:
- F11.1 S.24: Formel mit "Gültig nur wenn die 1. Frequenz = Frequenzauflösung". Die alte Formel nutzte den Index f/Auflösung − 1.
- TM S.18 (3-8): "any DC component is disregarded (n starts at 1)".
- SWP S.130 (4-14): Bandgrenzen müssen auf FFT-Linien liegen.
Für Python entscheidend: Frequenzvektor `f = delta_f * np.arange(1, n+1)`. Eine Gegenprobe an einer realen Datei steht aus [U]. Dafür ist der Zugriff über Polytec File Access nötig (F11.2 S.5–9 zeigt Frequenz und Amplitude in m/s).

### 3.2 Fenster

Alle Fenster außer Exponential und Kraft sind amplitudentreu normiert (TM S.13 und S.27, 5-5).

**Vergleich Polytec-Tabelle (TM Tab. 5.1, S.29, 5-7) gegen eigene Nachrechnung [H]** (N = 4096, periodische Fenster; Bin-Versatz 0,5):

| Fenster | Max. Amplitudenfehler Polytec | Eigene Rechnung | W_RBW Polytec | ENBW eigene Rechnung |
|---|---|---|---|---|
| Rechteck | −36 % | −36,2 % (−3,90 dB) | 1,00 | 1,000 |
| Hanning | −15 % | −15,1 % (−1,42 dB) | 1,50 | 1,500 |
| Hamming | −18 % | −18,2 % | 1,36 | 1,363 |
| Blackman | −12 % | −11,9 % | 1,73 | 1,727 |
| Blackman-Harris | −9 % | −9,1 % (−0,83 dB) | 2,00 | 2,004 |
| Bartlett | −19 % | −18,9 % | 1,33 | 1,333 |
| Flat Top | −0,2 % (Text: Ripple 0,02 dB) | −0,11 % (scipy-flattop, 0,01 dB) | 3,77 | 3,770 |

- Die Polytec-Werte stimmen bis auf Flat Top mit Standardfenstern überein. Die Flat-Top-Koeffizienten von Polytec sind nicht dokumentiert; die Angaben sind widersprüchlich (F03 S.25/28: −0,1 %; TM: −0,2 % bzw. 0,02 dB).
- **Tapered Hanning** (Parameter = Anstiegs- und Abklingzeit in % der Messzeit; Standard 10, SWA S.228, 7-20): Die ENBW 1,08 aus der Polytec-Tabelle passt zu einem Tukey-Fenster mit α = 0,2 (10 % je Seite), ENBW 1,080 [H]. Der Fehler bei halbem Bin-Versatz ist bei mir −30 %, in der Tabelle −35 %. Die exakte Definition bleibt unbestätigt [U].
- **Kraftfenster** (Länge in % der Messzeit, Standard 5): lässt das Anregungssignal unverändert und setzt danach auf Null (F04 S.21). **Exponentialfenster** (Parameter = Fensterlänge/Abklingzeit, Standard 4): beeinflusst die Dämpfung und erzwingt Abklingen innerhalb des Fensters (F04 S.23, SWA S.228). Bei Anwendung gilt ζ_scheinbar ≈ ζ + 1/(ω_n·τ) mit τ = T/4 [H, analytisch].
- **Einsatzempfehlungen** (TM Tab. 7.1, S.40, 7-2; F04 S.17): Rechteck für periodische und transiente Signale, Hanning für Rauschen, Flat Top für Sinus und Sweep (F04 S.17, F04.1 S.9) bzw. Hanning für Sweep (TM Tab. 7.1) – **Widerspruch**.
- **Overlap** wirkt nur bei Mittelung ohne Trigger (TM S.84, 13-8; SWA S.225). Folie F03 S.31 nennt 2/3 für Hanning und 3/4 für Flat Top. Nachrechnung [H]: Bei Hanning ist die Summe der quadrierten Fenster bei 2/3 und 3/4 konstant, bei 50 % nicht. Bei Flat Top bleibt bei 3/4 ein Restwelligkeit von 6 % (Summe w) bzw. 87 % (Summe w²); erst bei 4/5 ist die Summe w konstant. Die Polytec-Aussage "gleiche Bewertung" gilt demnach nur für Hanning.

### 3.3 Mittelung

- **Komplex** (nur mit Referenz oder Trigger, deterministische Anregung): N Real- und Imaginärteile mitteln. Vorab werden alle Kanäle phasenmäßig auf den niedrigsten Referenzkanal bezogen (TM S.34, 6-4).
- **Betrag (Amplitude)** (stochastische Anregung): erst Beträge bilden, dann mitteln. Die Phase des Referenz-Kreuzspektrums wird nachträglich zugewiesen (TM S.35, 6-5). Kreuzleistungen werden immer komplex gemittelt, deshalb sind H1, H2 und COH vom Mittelungsmodus unabhängig (TM S.15, 3-5).
- **Zeitbereich**: arithmetisches Mittel, mit Signal Enhancement Median (TM S.33, 6-3).
- **Peak Hold**: Der Referenzkanal bestimmt, welche Werte aller Kanäle übernommen werden. Dropouts wirken nur lokal, FRF und Cross-Power bleiben konsistent (TM S.37, 6-7).
- **Phasenbezug** (TM Tab. 6.1, S.36, 6-6):
  - Ohne Trigger und ohne Referenz: Phase nicht vorhanden.
  - Mit Referenz: Phase relativ zur Referenz.
  - Mit Trigger: wahlweise relativ zum Fensteranfang oder zum Referenzkanal. Nur "relativ zum Fensteranfang" erlaubt eine Rekonstruktion per IFFT (TM S.36).
  - Standardverhalten ohne Trigger: Phase aus der Übertragungsfunktion zum ersten Referenzkanal (SWA S.230, 7-22).
- Overrange-Spektren werden nicht gemittelt (SWA S.214, 7-6).

### 3.4 FRF, Kohärenz, Referenz

- Definition und Einheiten [Q] (TM S.14–15):
  - AP_SS = S*·S = |S|², CP_RV = R*·V.
  - FRF_VR = CP_RV/AP_RR = V/R (ohne Mittelung).
  - H1 = mittleres CP_RV / mittleres AP_RR, H2 = mittleres AP_VV / mittleres CP_VR.
  - COH = H1/H2 = (mittleres CP_RV · mittleres CP_VR)/(mittleres AP_VV · mittleres AP_RR).
- Die Phase ist bei H1 und H2 gleich, der Betrag verschieden. H1 ist von Eingangsrauschen (Referenz) beeinflusst, H2 von Ausgangsrauschen (Vibrometer) (TM S.15). Für ODS rät Polytec zu H1, weil es gegen Vibrometerrauschen weniger empfindlich ist (TM S.16, 3-6).
- Die FRF-Einheit ist (Einheit der Antwort)/(Einheit der Referenz). Mit Kraftreferenz [N/V·Faktor] ergibt sich (m/s)/N, also Mobilität. Mit einer Spannungsreferenz ist es (m/s)/V und keine Mobilität (SWA S.220, 7-12, Spalte "Größe", "Faktor"). Bei mehreren Referenzkanälen bildet die Software jeweils Gesamtantwort/Referenzsignal. Für echte Multi-Referenz-Modalanalyse ist die PCA-Option nötig (SWA S.219).
- **Exakte Beziehungen [H].** Mit gemessenen Autoleistungen AP_RR = S_x + N_R und AP_VV = |H|²·S_x + N_V (Rauschen unkorreliert):
  - $H_1 = H\,(1 - N_R/AP_{RR})$ (Polytec Gl. 3.10 ist damit sogar exakt).
  - $H_2 = H/(1 - N_V/AP_{VV})$ (Polytec Gl. 3.11 ist die Näherung 1 + N_V/AP_VV).
  - $\gamma^2 = (1 - N_R/AP_{RR})(1 - N_V/AP_{VV})$ (Polytec Gl. 3.12/3.13 sind Näherungen erster Ordnung).
  - Zahlenbeispiel: S_x = 1, H = 0,8 + 0,3i, N_R = 0,05, N_V = 0,08 ergibt H1/H = 0,95238, H2/H = 1,10959, γ² = 0,858319 (Polytec 3.12: 0,8668; 3.13: 0,8536).
- Phasenvorzeichen: Ein Referenzkanal wird auf Phase 0 gesetzt. Die Antwortphase ist relativ dazu definiert.
- MIMO (Option PCA): lineares FRF-Matrixmodell. Voraussetzungen: unkorrelierte Referenzen, gleiche Fenster, mindestens M + 2 Mittelungen (TM S.48–49, 8-4/8-5).

### 3.5 Anregung und Trigger

**Signale und Eigenschaften** (TM Tab. 7.1, S.40, 7-2; F04 S.7–17):

| Signal | Klasse | RMS/Peak | Leakage | Fenster | MIMO |
|---|---|---|---|---|---|
| Sinus | harmonisch | 0,7 | nein (nur wenn Frequenz auf Linie) | Rechteck | nein |
| Sweep | pseudo-harmonisch | 0,7 | ja | Hanning (TM) / Flat Top (F04, F04.1) | nein |
| Pseudo Random | periodisch | 0,25 | nein | Rechteck | nein |
| Periodic Chirp | periodisch | 0,5 | nein | Rechteck | nein |
| Burst Chirp | transient | 0,35 | nein, wenn Antwort abklingt | Rechteck | nein |
| Weißes Rauschen | zufällig | 0,25 | ja | Hanning | ja |
| Burst Random | transient, zufällig | 0,2 | nein, wenn Antwort abklingt | Rechteck | ja |

- Burst Chirp und Burst Random: Der Datenerfassungsblock wird mit dem Burst getriggert. Das gesamte Signal ist 20 % länger als das Messfenster (TM S.42, 7-4). Burst Random ist auf 524 288 Samples beschränkt (SWA S.239).
- Weißes Rauschen: ca. 25 Mittelungen empfohlen, Hanning, 50 % Overlap (TM S.43, 7-5). Burst Random mit ca. 25 Mittelungen ist ebenfalls für lineare Näherung geeignet.
- Periodic Chirp und Pseudo Random: Die Energie verteilt sich auf alle FFT-Linien, die Amplitude je Linie hängt von der Linienzahl ab (F04 S.12). Das Verhältnis RMS zu Peak von 0,5 liefert eine Abschätzung der Amplitude je Linie $a \approx V_{peak}/\sqrt{2n}$ [H, Näherung]. Bei 1 V Peak und 400 Linien sind das ca. 0,035 V je Linie. Wartezeit bis zum stationären Zustand ist zu beachten.
- Periodic Chirp und Pseudo Random liefern bei linearen Systemen gleiche FRFs. Unterschiede deuten auf Nichtlinearität (TM S.41, 7-3).
- Nur Zufallssignale mitteln Nichtlinearitäten zu einer linearen Näherung heraus (TM S.40).
- Bei Scans mit gleicher Anregung kann das Vibrometersignal als Flächendaten dargestellt werden. Variiert die Anregung von Punkt zu Punkt, ist die FRF für die Flächendarstellung zu verwenden (TM S.39, 7-1).
- Die FastScan-Methode ist eine Regression im Zeitbereich an einer Frequenz und leckagefrei (SWA S.262, 8-16).
- Hammer: Amplitude und Pulsdauer hängen von Hammer, Spitze, Oberfläche und Schlag ab. Der automatische Hammer SAM ist reproduzierbar (F04 S.18–20; F01 S.23–24).
- Trigger: Quelle Aus/Intern/Extern (TTL, 0–5 V)/Analog, Pretrigger in % der Messzeit (SWA S.229–230, 7-21/22).

### 3.6 Sweep und Peak Hold (F04.1, TM 6.6)

Formeln [Q] (F04.1 S.11–12): Δf = BW/Linien. Sweep-Steilheit = Δf/Blocklänge = Δf². Sweepzeit = BW/Steilheit. Mittelungsanzahl = Sweepzeit/Blocklänge. Mit 75 % Overlap mal 4. Die Steilheit passt, wenn die Frequenzänderung im Block einer Linie entspricht.
- **Nachgerechnet** [H]: BW 1000 Hz, 200 Linien: Δf = 5 Hz, T = 0,2 s, 25 Hz/s, 40 s, 200 Mittelungen, 800 mit Overlap. Folie 15: 300 s ergibt 3,3 Hz/s, Δf = 1,82 Hz, 2184 Mittelungen (Folie: 2180 mit gerundetem Δf). Folie 16: 6 Oktaven, 8,33 Hz/s, Δf = 2,89 Hz, 4157 Mittelungen (Folie: 4176 mit Δf = 2,9).
- Peak Hold: Der Vergleich erfolgt im ersten als Referenz markierten Kanal. SE und Nachmessen müssen aus sein. Eine Triggerung des Sweepbeginns ist nicht möglich (F04.1 S.7, S.12).

### 3.7 PSD, ESD, RMS, Terz (TM S.17–19)

- RBW = (BW/n_FFT)·W_RBW. PSD = AP/(2·RBW). ESD = PSD·t_W, nur sinnvoll, wenn das transiente Signal abklingt.
- RMS = √(Σ AP_n/(2·W_RBW)), entspricht dem Zeit-RMS nach Parseval. DC wird bei Gesamtbandbreite ausgelassen.
- Terzbänder: f_m,n = 10^(0,1·n), Bandgrenzen f_m·10^(±0,05) (Basis 10).
- **Nachgerechnet** [H]: Das PSD entspricht scipy-`welch` mit `scaling='density'`. Die Gl. 3.17 ergibt für Sinus mit Hanning (A = 2) einen RMS von 1,4142 (A/√2). Für weißes Rauschen (σ = 0,7) ergibt sie 0,6256 gegen den erwarteten Wert 0,6261.

### 3.8 Abweichungen von Lehrbuchdefinitionen und Stolpersteine

| Thema | Polytec | Lehrbuch/typisch |
|---|---|---|
| Spektrumsskalierung | einseitig, Spitzenamplitude (0-to-peak), amplitudentreu | oft effektiv, einseitig; DFT/N zweiseitig |
| Fensternormierung | Kohärenter Gain, Σw (amplitudentreu) | teils Leistungsnormierung |
| Exponential-/Kraftfenster | keine Amplitudenkorrektur | – |
| Frequenzachse | k·Δf, k = 1…n_FFT (DC nicht gespeichert) | rfft: f_k = k·fs/N, k = 0… |
| fs/BW | 2,5 (H-System), 2,56 (M-System) | typisch 2 oder 2,56 |
| "Gemitteltes Spektrum" | Mittel der Beträge der gültigen Scanpunkte | oft komplexes Mittel |
| "Dämpfung" im Band-Cursor | −3-dB-Breite Δf | Dämpfungsgrad ζ |
| 3D-Betrag | $A=\sqrt{A_x^2+A_y^2+A_z^2}$, Phase nicht verfügbar | – |
| Richtung | positiv = Bewegung zum Scankopf | – |
| Phase | $A\cos(\omega t+\varphi_0)$, $e^{+i\omega t}$ | oft ebenso |
| Integration im Zeitbereich | FIR mit ½ Abtastintervall Verzögerung | – |

---

## 4. Leitfrage 3: Auswertung in PSV und Mehrwert eines Python-Pakets

### 4.1 Was PSV bereits liefert (Quellen: F11, F11.1, SWP, SWA)

- **Domänen/Signale:** FFT, Zeit, Terz, RMS; AP, CP, FRF, H1, H2, COH, PSD, ESD, MIMO-Größen (SWA S.285–287, 9-19/9-21).
- **Anzeige:** Flächen-, Draht-, Isolinien-, Pfeil-, Statuspunktansicht; 2D, 3D, Profil; Banddaten, Punktdaten, einzelner Scanpunkt, gemitteltes Spektrum (F11 S.5–8, SWP S.60).
- **Bänder:** manuelle und automatische Peak-Suche (Kriterien: minimale Amplitude, Prominenz, relative Höhe zu Breite, Mindestabstand), RMS je Band, Terzbänder (SWP S.131–133, 4-15–4-17).
- **Cursor:** Band-Cursor mit SDOF-Peak-Fit (f_max, −3-dB-Breite, Q, ζ), Differenz-Cursor, harmonischer Cursor mit THD, gedämpfte Sinusanpassung im Zeitsignal (SWP S.49–51, 3-13–3-15).
- **Animation:** phasenbezogen (nur mit Trigger oder Referenz), als AVI/GIF exportierbar (SWP S.139–142, 4-23–4-26).
- **Datenaufbereitung:** Filtern (Median plus Mittelwert benachbarter Scanpunkte), Interpolieren, Ungültig-Markierung, Status je Punkt (SWP S.118–125, 4-2–4-9).
- **Signalprozessor (SigPro):** tabellenartige Formeln, Funktionen u. a. FFT, IFFT, AP, CP, COH, AFFT, FRF, H1, H2, Filter, Resample, Statmean/Statstd, Extract, Point, PointUnion, Make3D, Scale; Ergebnisse als benutzerdefinierte Datensätze (Kanal Usr) in die Scan-Datei schreibbar (SWA S.294–301, 9-28–9-35; F11.1).
- **Export:** UFF (Datensätze 151, 164, 2411, 2412+82, 55, 58, 58b), ASCII, ME'Scope, ASAM ODS ATFX, STL, WAV, Zwischenablage (SWP S.177, 5-21; F10 S.45–48). Bei UFF, ME'Scope und ATFX sowie beim Zugriff über Polytec File Access werden die Originaldaten exportiert, nicht gefilterte oder interpolierte (SWP S.122–123).
- **Stitching** über kombinierte Dateien (F09.1).
- **Weitere Optionen:** MIMO/PCA, FastScan, MultiFrame, Zeitmodus (TDD). Welche am Labor installiert sind, ist offen.
- **Makros:** VBA-Makros und COM; auch Python ist über COM möglich (COM S.2, Anmerkung DAL).

### 4.2 Wo ein Python-Paket Mehrwert bringt [E, soweit nicht anders belegt]

| Bereich | Mehrwert | Begründung |
|---|---|---|
| Automatisierung | Parametrisierte, reproduzierbare Messserien. Settings, Alignment und Geometrie als Dateien archivieren. Wiederholmessungen mit Abbruch- und Nachmesslogik. | Reproduzierbarkeit (Ausschreibung). PSV bietet GUI und Makros, aber kein Versuchsprotokoll. |
| Qualitätsprüfung | Automatische Plausibilitätsprüfungen (siehe 5). | In PSV nur manuell. |
| Modalanalyse | MDOF-Parameterschätzung (z. B. LSCF/PolyMAX, Stabilisierungsdiagramm), MAC, Skalierung. | PSV enthält nur SDOF-Peak-Fit (SWP S.50). ME'Scope wird extern genutzt (F11 S.37; SWA S.220). |
| Berichte und Abbildungen | Skriptbasierte, nachvollziehbare Abbildungen und Berichte mit Git-Hash. | Anforderung aus `KONVENTIONEN.md` (Abbildungen per Skript). |
| Eigene Auswertungen | ODS-Metriken, Wiederholbarkeitsmetriken, Vergleich mit FE-Daten. | PSV kann nur Peak-Fit, RMS und Animation. |
| Gegenprobe | Eigene Implementierungen gegen Polytec-Werte prüfen. | Polytec-Werte dienen als Validierungsreferenz. |

Daten, die mit Polytec-Mitteln bereits sauber vorliegen (Spektren, H1, Kohärenz), sollten nicht doppelt implementiert werden, es sei denn als Gegenprobe oder für Zeitdaten.

---

## 5. Leitfrage 4: Praktische Hinweise, Fehlerquellen, Plausibilitätskriterien

### 5.1 Typische Fehlerquellen

- Dropouts durch dunkle Speckles. Abhilfe: Mittelung, Signal Enhancement, Speckle Tracking, Trackingfilter (F06 S.14–17; SWA S.248 und S.232; TM S.82–83).
- Overrange durch zu kleinen Messbereich. Overrange-Punkte werden ungültig gewertet bzw. nachgemessen (SWA S.214, S.256, 8-10).
- Aliasing/Nyquist. Der Anti-Alias-Filter ist eingebaut. Die Bandbreite sollte trotzdem die höchste interessierende Frequenz abdecken (TM S.21).
- Leckage bei falscher Fensterwahl (F04 S.17; F03 S.17–25).
- Nichtlinearität (TM S.40–41).
- Instabiler Trigger oder fehlende Referenz, damit keine Phase (TM S.35–36).
- Geometriefehler: fehlerhafter 3D-Abgleich, schlechte Videotriangulation, Laserspots decken sich nicht, importierte Geometrie im falschen Koordinatensystem (TM S.61–64; SWA S.145–147; F10 S.27).
- Kopfbewegung, Stativschwingungen. Optional A-VIB-ACC1 zur Kompensation (KA S.16 und S.40).
- Messung durch Glas oder in Flüssigkeit. Amplituden bei Flüssigkeit durch den Brechungsindex n teilen (F08 S.8–10; F11.1 S.29–30, Beispiel Wasser 1,33).
- Temperaturdrift und Aufwärmzeit (KA S.46).
- Kosinusfehler im 1D-Modus. Die Winkelkorrektur gilt nur für ebene Flächen senkrecht zum Scankopf und reine Out-of-plane-Schwingung (SWA S.59, 3-15; TM S.92, 14-8).
- Generatorlast 50 Ω (SWA S.240).
- Mehrere Scanpunkte mit gleichem Index beim Stitching (F09.1 S.25; F11 S.36).

### 5.2 Plausibilitätskriterien, die das Paket automatisch prüfen könnte

Schwellwerte sind, soweit nicht von Polytec genannt, konfigurierbar vorzusehen [E].

| ID | Kriterium | Datenbedarf | Beleg |
|---|---|---|---|
| P1 | Kohärenz je Linie und Punkt. 0,99 ≈ 1 % Rauschanteil, nahe 0 = schlechtes SNR. Auswertung nur in relevantem Band. | FRF und COH je Punkt | TM S.16 (3-6) |
| P2 | Scan-Status: Anteil Overrange, Ungültig, VT fehlgeschlagen, Verdeckt, Nicht erreichbar, nicht optimal | Statusliste | SWA S.251–252; SWP S.118–121 |
| P3 | 3D-Abgleichqualität: Position (mm) und Winkel (mrad) je Kopf, Faustregel 0,1 mrad ≈ 0,1 mm/m | Dialogwerte, falls über COM lesbar [U] | F07 S.22–23; SWA S.147 |
| P4 | Strahlgeometrie: Konditionszahl der Richtungsmatrix D, mindestens ein Strahl deutlich außerhalb der Ebene der beiden anderen. κ(D) = 1,685 bei 40°, 1,414 bei 45°, 1 bei 54,7° (symmetrische Anordnung). | Kopf- und Punktkoordinaten | SWA S.144; [H] |
| P5 | Konsistenz der Einstellungen: fs = 2,5·BW, Δf = BW/n_FFT, N = 2,5·n_FFT, Von/Bis ≤ BW, geschätzte Scanzeit t_T = t_W·n_p·n_a + t_add | Settings | SWA S.225; TM S.80 (13-4) |
| P6 | Signal-Fenster-Matrix: Rechteck für Periodic Chirp, Pseudo Random, Burst-Signale; Hanning für Rauschen; Flat Top für Sinus | Settings | TM S.40–43; F04 S.17 |
| P7 | Burst: Antwort muss am Fensterende abgeklungen sein (Restenergie letzter Fensteranteil) | Zeitdaten (TDD) oder Spektrum-Restwelligkeit [U] | TM S.42 |
| P8 | Sweep-Parameter: Sweeprate ≈ Δf², Mittelungszahl = Sweepzeit·Δf | Settings | F04.1 S.11–12 |
| P9 | Wiederholbarkeit: Referenzpunkt, Eigenfrequenzabweichung und MAC der Wiederholungen | Wiederholte Scans | [E] |
| P10 | Nichtlinearitätstest: Vergleich von Pseudo Random und Periodic Chirp, oder zwei Anregungsstufen | Zwei Messungen | TM S.41 |
| P11 | Resolutionsregel: Δf deutlich kleiner als die −3-dB-Breite des schmalsten Peaks [E, Richtwert, nicht belegt]. TM S.43 verlangt nur "ausreichend hohe Auflösung abhängig von der Dämpfung". | Spektrum | TM S.43 |
| P12 | Parseval-Test: RMS aus Gl. 3.17 = RMS im Zeitbereich | Zeitdaten | TM S.18 |
| P13 | Aufwärmzeit und Umgebungstemperatur laut Protokoll | Zeitstempel | KA S.46–47 |
| P14 | Stitching-Konsistenz: gleiche Settings (nur Mittelungen und Bereich dürfen abweichen), eindeutige Indizes | Metadaten | F09.1 S.5 |
| P15 | Phasenreferenz: Referenzkanal aktiv und Trigger oder Referenz vorhanden, sonst keine ODS-Animation | Settings | SWP S.139 |
| P16 | Aussteuerung 30–80 % des Messbereichs (VFC-Angabe, Übertragbarkeit [U]) | Signalpegel | VFC S.47 |
| P17 | Niederfrequenz-Check: bei niedrigen Anregefrequenzen bewegen sich alle Punkte gemeinsam (nur bei Fußpunktanregung) | Spektrum | F04.1 S.27 |

---

## 6. Leitfrage 5: Priorisierte Fachgrundlagen und Referenzfälle (Ablauf E, A2)

Alle Sollwerte sind mit den Skripten `check1.py` bis `check4.py` nachgerechnet, soweit nicht anders vermerkt.

### 6.1 Priorisierte Liste

| Prio | ID | Fachgrundlage | Inhalt | Referenzfälle (Sollwert) | Status |
|---|---|---|---|---|---|
| 1 | FG-01 | Spektralschätzung nach Polytec-Konvention | Einseitig, Spitzenamplitude; Fensternormierung; ENBW; Frequenzachse k·Δf; fs = 2,5·BW; PSD, RMS, Parseval | (a) Sinus A auf Linie: Amplitude A, rtol ≈ 1e-12 (Rechteck, Hanning, Flat Top). (b) Halber Bin-Versatz, N = 4096: Rechteck −36,2 %, Hanning −15,1 %, Hamming −18,2 %, Blackman −11,9 %, Blackman-Harris −9,1 %, Bartlett −18,9 %, Flat Top −0,11 % (scipy). Polytec-Tabelle als Gegenprobe (±0,5 Prozentpunkte). (c) RMS = A/√2 für Sinus (rtol 1e-12). (d) Weißes Rauschen σ = 0,7, BW = 1000 Hz, fs = 2500 Hz: RMS = 0,626 (statistisch). | Nachgerechnet |
| 1 | FG-02 | FRF-Schätzer H1/H2/Hv, Kohärenz | Polytec-Definition (CP_RV = R*V); exakte Beziehungen zu Rauschen; Randfälle | S_x = 1, H = 0,8 + 0,3i, N_R = 0,05, N_V = 0,08: H1/H = 0,95238; H2/H = 1,10959; γ² = 0,858319. Monte-Carlo-Gegenprobe im Rahmen der Statistik. Hv nur aus Literatur. | Nachgerechnet; Hv offen |
| 1 | FG-03 | 3D-Rekonstruktion | u_k = d_k·v (d_k Einheitsvektor Objekt → Kopf k), v = D⁻¹u; Vorzeichenkonvention; Konditionszahl; Rauschverstärkung | Symmetrische Anordnung, θ = 40° zur Normalen: κ = 1,685; σ_x/σ = σ_y/σ = 1,270; σ_z/σ = 0,754. θ = 45°: κ = 1,414. θ ≈ 54,74°: κ = 1. Koplanar: det = 0. Reiner z-Anteil ergibt u_k = cosθ. | Nachgerechnet; Polytec dokumentiert die Matrix nicht [U] |
| 1 | FG-04 | SDOF-Peak: Halbwertsbreite, Q, ζ, Circle-/LSCF-Ansatz | Polytec-Band-Cursor (Δf, Q = f/Δf, ζ = Δf/(2f)); Gültigkeit für kleine Dämpfung | m = 1 kg, f_n = 100 Hz, ζ = 0,01: c = 12,566 Ns/m, k = 394 784,2 N/m, \|H_v(ω_n)\| = 0,07958 (m/s)/N. −3-dB-Breite der Mobilität exakt 2ζf_n = 2,000 Hz; Receptance 2,0002 Hz (f_max 99,99 Hz), Akzeleranz 2,001 Hz (f_max 100,01 Hz). ζ = 0,05: Mobilität 10,000 Hz; Receptance 10,025 Hz; Akzeleranz 10,127 Hz. | Nachgerechnet |
| 2 | FG-05 | Mittelungsarten und Phasenbezug | Komplex, Betrag, Peak Hold, Zeit-Mittel; Tabelle 6.1; Overrange-Ausschluss | Komplexes Mittel von S1, S2 kürzt Rauschen, Betragsmittel nicht (TM Abb. 6.2). Deterministische Testfälle mit bekannter Phasenverschiebung. | Analytisch |
| 2 | FG-06 | Sweep/Peak-Hold-Parameter | Δf², Sweepzeit, Mittelungszahl | BW 1000, 200 Linien: Δf = 5 Hz, T = 0,2 s, 25 Hz/s, 40 s, 200 Mittelungen (800 mit 75 % Overlap). 300 s Sweep 10–1000 Hz: Δf = 1,817 Hz, 2184 Mittelungen. 1 Oktave/min, 15,6–1000 Hz: 6,002 Oktaven, 8,33 Hz/s, Δf = 2,887 Hz, 4157 Mittelungen. | Nachgerechnet |
| 2 | FG-07 | ODS-Darstellung und Animation | Komplexe Amplitude, Momentanwert Re{A e^{iωt}}, 3D-Betrag, Betragsmittel gegen komplexes Mittel | Phasor A = 1 e^{i·60°}: Momentanwert A cos(ωt + 60°). 3D: A = √(A_x²+A_y²+A_z²). Mobilität gegen Receptance: Phasenversatz 90°. | Analytisch |
| 2 | FG-08 | Reproduzierbarkeits- und Wiederholbarkeitsmetriken | Δf_n/f_n, MAC, FRF-Differenznorm | Identische Daten: MAC = 1; skalierte Daten: MAC = 1; orthogonale Moden: MAC = 0. Freier Balken: λ_n L = 4,730041; 7,853205; 10,995608; 14,137165 (Eigenformen als analytische Referenz für MAC); f_n = λ²/(2πL²)·√(EI/(ρA)) | λ nachgerechnet; Formel aus Literatur zu prüfen |
| 3 | FG-09 | Zeit-Frequenz-Konsistenz und Integration | Integration/Differentiation (½-Sample-Verzögerung), fs/BW | v = A cos(ωt): Weg-Amplitude A/ω, Beschleunigung ωA. Folie F03 S.5: ω = 1000 rad/s bei 159,15 Hz. Berechnung: Sinus von 40 % fs mit < 0,5 % Fehler (TM S.57). | Teilweise belegt |
| 3 | FG-10 | Anregung und Fensterwahl | Zuordnung Signal–Fenster, Leckage, Exponentialfenster-Dämpfungsfehler | ζ_scheinbar = ζ + 1/(ω_n τ), τ = T/4; Beispiel T = 1 s, f = 100 Hz: Zusatz 0,64 %. | Analytisch |
| 3 | FG-11 | LDV-Messunsicherheit | Doppler, Cosinus-Fehler, Speckle, Brechungsindex, Winkelfehler | Δf_D = 2v/λ: 1,2907 MHz pro m/s bei 1549,7 nm. Cosinus-Fehler 1,52/6,03/13,40 % bei 10/20/30°. 0,1 mrad bei 1 m = 0,1 mm. | Nachgerechnet |
| 4 | FG-12 | MIMO/PCA | Multi-Referenz-Modell, Eigenwerte der Referenz-Matrix | Nur falls Mehrfachanregung geplant | Offen |
| 4 | FG-13 | Terz und A-Bewertung | f_m = 10^(0,1n) | Nur falls akustisch relevant | Offen |

**Toleranzen (Vorschlag)**
- Numerische Identitäten (Skalierung, on-bin, Parseval): rtol 1e-10 bis 1e-12.
- Fenster-Scalloping gegen Polytec-Tabelle: ±0,5 Prozentpunkte (Tabelle ganzzahlig gerundet).
- Statistische Schätzer (Rauschen, MC): Toleranz aus der Standardabweichung 1/√M ableiten (z. B. 3σ).
- Flat-Top-Koeffizienten von Polytec sind unbekannt, daher Toleranz ≥ 0,3 % bei Betragsvergleich.

---

## 7. Leitfrage 6: Thesis-Bezug, Zitierbarkeit, Rechercheaufträge

### 7.1 Inhalte für das Grundlagenkapitel (Vorschlag)

1. LDV-Messprinzip: Doppler-Effekt, Interferometrie, Heterodyn-Demodulation, Speckle und Dropouts.
2. 3D-Scanning-LDV: Alignment, Triangulation, Vektorzerlegung, Konditionszahl, Koordinatensysteme.
3. Signalverarbeitung: DFT, Leckage, Fenster (ENBW, Scalloping), Mittelung, Spektralschätzung, H1/H2/Hv, Kohärenz.
4. Strukturdynamik: SDOF/MDOF, FRF-Größen, ODS, Modalanalyse, MAC.
5. Anregung und Versuchsführung: Lagerung, Shaker/Hammer, Signalarten, Randbedingungen.
6. Messunsicherheit und Reproduzierbarkeit.

Gerätespezifische Konventionen (Skalierung, Frequenzachse, Phasenbezug, Datenformate) gehören ins Methodik- oder Implementierungskapitel mit Verweis auf die Polytec-Handbücher.

### 7.2 Zitierfähigkeit der Input-Quellen und ihre Grenzen

| Quelle | Eignung | Zitierart | Grenzen |
|---|---|---|---|
| TM (Dok.-Nr. 41088, Stand Software 9.1) | gerätespezifische Definitionen: Skalierung, Mittelung, Fenster, H1/H2, MIMO, Triangulation | Herstellerhandbuch mit Dok.-Nr., Seite | nicht begutachtet; Stand 9.1, Software ist 10.x; Gleichungen nur als Bild; Flat-Top-Angaben widersprüchlich |
| SWA/SWP (41584, 41596, Version 10.1) | Parameter, Statuswerte, Export, SigPro-Funktionen, Peak-Fit | Herstellerhandbuch | keine mathematischen Herleitungen; Gleichungen als Bild |
| KA (43695) | Aufbau, Anschlüsse, Richtungskonvention, Warmlaufzeit | Herstellerhandbuch | keine Messbereiche oder Rauschwerte |
| VFC/VFS/VFX | Hintergrund zum Einpunkt-Vibrometer, Decoder, Trackingfilter, Signalverzögerung | Herstellerhandbuch | nicht QTec 3D selbst |
| Schulungsfolien F01–F11.2 | praktische Hinweise, Beispiele | Folien mit Datum ("Polytec-Schulungsunterlage, 05.04.2023") | Marketing-Anteil, teils veraltete Versionen (z. B. "bis PSV 9.5"), Bilder; Rechenfehler in Beispielen |
| COM | Hinweise zur COM-Nutzung | Persönliche Mitteilung / Betreuerunterlage (Anmerkung DAL 04.08.2026) | Intern, kein publiziertes Dokument |

Für allgemeine Theorie (DFT, Fenster, H1/H2, Modalanalyse, LDV-Fehler) sind Lehrbücher und begutachtete Artikel zu zitieren.

### 7.3 Rechercheaufträge (A3) für den `literatur-rechercheur`

Alle genannten Titel sind Kandidaten aus dem Gedächtnis und unverifiziert [U]. Existenz und bibliografische Daten sind zu prüfen, nichts davon ist als belegt zu übernehmen.

| Nr. | Thema | Zweck | Kandidaten (zu verifizieren) |
|---|---|---|---|
| R1 | FRF-Schätzer H1/H2/Hv, Kohärenz, Fehleranalyse | FG-02 | Bendat/Piersol, *Random Data*; Brandt, *Noise and Vibration Analysis*; Pintelon/Schoukens, *System Identification* |
| R2 | DFT, Fensterfunktionen, ENBW, Scalloping, Flat-Top-Fenster | FG-01 | Harris (1978), Proc. IEEE 66(1); Heinzel/Rüdiger/Schilling (2002), AEI-Bericht; Welch (1967); Oppenheim/Schafer |
| R3 | Experimentelle Modalanalyse, SDOF/MDOF-Fits, MAC | FG-04, FG-08 | Ewins, *Modal Testing*; Heylen/Lammens/Sas; Maia/Silva; Allemang/Brown (1982), MAC; Allemang (2003), "MAC twenty years"; Guillaume et al. (2003), LSCF; Peeters et al., PolyMAX; Richardson/Formenti (1982) |
| R4 | LDV-Grundlagen, Speckle, Pseudovibration, Cosinus-Fehler | FG-11 | Rothberg et al. (2017), Optics and Lasers in Engineering 99; Castellini/Martarelli/Tomasini; Rothberg-Veröffentlichungen zu Pseudovibration und Speckle; Drain (1980) |
| R5 | 3D-Scanning-LDV: Vektorzerlegung, Fehlerfortpflanzung, Konditionierung | FG-03 | keine Kandidaten gesichert; Recherche ohne Vorgabe |
| R6 | Luft- und Raumfahrt-Strukturtests, Normen (Modal Survey, GVT, Sinus-Sweep) | Kontext, Anforderungen | z. B. ECSS-E-ST-10-03C; Literatur zu Ground Vibration Testing; In-Haus-Referenzen des SLA beim Betreuer erfragen |
| R7 | Messunsicherheit und Kalibrierung von Laser-Vibrometern | FG-11, Unsicherheit | JCGM 100 (GUM); ISO 16063-41 (Kalibrierung Laser-Vibrometer) |
| R8 | Anregungssignale mit niedrigem Scheitelfaktor (Periodic Chirp, Multisine), Burst Random | FG-10 | Schroeder (1970), IEEE Trans. Inf. Theory; Pintelon/Schoukens |
| R9 | ODS gegenüber Eigenformen, ODS-Messanforderungen | FG-07 | Schwarz/Richardson (Veröffentlichungen zu ODS) |
| R10 | Freier Balken: Eigenwerte und Formen (analytische Referenz) | FG-08 | Blevins, *Formulas for Natural Frequency and Mode Shape* |
| R11 | Datenformate: UFF (Dataset 58), Polytec File Access | Datenzugriff | UFF-Spezifikation; Polytec File Access Object Model Reference (im Input als CHM) |
| R12 | Herstellerunterlagen, die im Input fehlen | Messbereiche, Rauschen | PSV QTec 3D technische Spezifikation (Messbereiche, Bandbreite, Signalverzögerung, Rauschen). "Volltext benötigt": Nutzer um die Datei bitten (`Input/literatur/`). |

---

## 8. Leitfrage 7: Offene fachliche Fragen an Nutzer/Betreuer

1. **[blockierend für die Priorisierung von FG-04]** Soll die Auswertung nur Betriebsschwingformen (ODS) und Spektren liefern oder auch Modalparameter (Eigenformen, Dämpfung)? *Auswirkung:* Umfang der Modalanalyse (SDOF-Peak-Fit gegen MDOF-Verfahren), Notwendigkeit einer Kraftmessung.
2. **[blockierend für FG-02/FRF-Definition]** Wird die Anregungskraft gemessen (Kraftsensor, Impedanzkopf, Hammer mit Kraftaufnehmer), oder ist die Referenz nur das Generatorsignal in Volt? *Auswirkung:* FRF = Mobilität in (m/s)/N gegenüber (m/s)/V; Modalskalierung nur mit Kraft.
3. [nicht blockierend] Prüfling (Material, Abmessungen, erwartete Eigenfrequenzen und Dämpfung), Lagerung (frei-frei, eingespannt), Frequenzbereich. *Annahme bis zur Klärung:* keine Annahmen im Code, Parameter konfigurierbar.
4. [nicht blockierend] Anregung: Shaker, SAM-Hammer, Piezo oder Lautsprecher? Signalform (Chirp, Burst Random, Sweep)? *Auswirkung:* Fensterwahl und Mittelungsstrategie.
5. [nicht blockierend] Software-Version und installierte Optionen am Laborrechner (GeoPro/ImpGeo, TDD, PCA, FastScan, Signalgenerator, ExpME, ASAM ODS ATFX). Ist es wirklich PSV-F-600-3D-H? *Annahme:* Version 10.1, H-System.
6. [nicht blockierend] Gibt es ein VibroFlex-Connect-Gerät oder anderes Einpunktvibrometer im Labor, und ist es als Referenz oder Kontrollmessung vorgesehen? Werden die Signalverzögerungen (VFS S.29) in diesem Fall kompensiert? *Annahme:* kein zusätzliches Vibrometer.
7. [nicht blockierend] Was bedeutet "reproduzierbar" quantitativ (Toleranz der Eigenfrequenz, MAC-Schwelle, Amplitudentoleranz)? Gibt es Normbezüge oder Vorgaben des Instituts?
8. [nicht blockierend] Welcher Datenpfad ist vorgesehen: Polytec File Access (`svd`/`pvd`) oder UFF-Export? Ist die Time-Domain-Option (TDD) verfügbar, damit Spektren selbst aus Zeitdaten gerechnet werden können? *Auswirkung:* ob eigene Spektralschätzung und der Parseval-Test (P12) möglich sind.
9. [nicht blockierend] Liegt das Spezifikationshandbuch zum PSV QTec 3D (Messbereiche, Rauschen, Bandbreite) vor?

---

## 9. Auffälligkeiten und Widersprüche in den Unterlagen

1. **fs = 2,5·BW gegen 2,56·BW.** SWA 7-17 und F06 S.10: 2,5 für alle Nicht-M-Systeme. TM 3-3 und 13-8: Beispiel mit 100 Linien und 256 Samples (2,56, M-System). TM 3-3 verlangt eine Zweierpotenz, 2,5·n_FFT ist das im Allgemeinen nicht.
2. **Sweep-Fenster.** F04 S.17 und F04.1 S.9: Flat Top (75 % Overlap). TM Tab. 7.1: Hanning.
3. **Flat-Top-Fehler.** F03 S.25 und S.28: −0,1 %. TM Tab. 5.1: −0,2 %. TM-Text: Ripple 0,02 dB (−0,23 %). Meine scipy-Nachrechnung: −0,11 % (0,01 dB).
4. **Rechenfehler in Folien.** F04.1 S.15: 2180 statt 2160 (mit gerundetem Δf). S.16: 4176 statt 4157 (Δf gerundet).
5. **Overlap-Aussage.** F03 S.31 "Flat Top 3/4" stimmt für die Summe der Fenster nicht exakt (siehe 3.2).
6. **Kopfwinkel.** F05.1 S.3 nennt 45° für beste Empfindlichkeit, SWA 5-54 nennt 40° bzw. 20° zur Normalen. Mathematisch minimiert die orthogonale Anordnung (≈54,7° zur Normalen) die Rauschverstärkung [H]; Polytec bewertet zusätzlich die Rückstreuung.
7. **Laserklasse.** KA S.10 beschreibt Klasse 2 für das Gerät, KA S.48 Klasse 1 für den Messlaser (< 10 mW) und Klasse 2 für den Pilotlaser. Für die Fachanalyse nicht entscheidend.
8. **Aktualität.** TM "As of Software 9.1", Handbücher Version 10.1, Folien 2021–2023.
9. **F08 S.18** "Keine Kohärenzminima": Spalte nicht eindeutig (vermutlich Xtra). F08 S.3 und SWA 5-54 (204 mm Sichtbarkeitsmaxima) gelten für HeNe-Köpfe, für QTec nicht belegt.
10. **F01 S.13–15** (Bandbreite 100 kHz, Messbereiche, Auflösung) betrifft PSV-500, nicht QTec.

---

## 10. Was nicht lesbar war oder nur überflogen wurde (A4)

**Allgemein.** Alle PDFs wurden per `pdftotext` auf Textebene gelesen. Gleichungen und Abbildungen liegen in den Handbüchern als Bilder vor.

- **Schulungsunterlagen F01–F11.1:** nur Textebene. Reine Bildfolien und Screenshots (z. B. F02 S.14–15, F03 S.19–23, F07 S.17/18, F10 S.9–25 und S.36–48, F11 S.4–19) nicht ausgewertet. Bildfolien F07 S.20 und S.23 habe ich gerendert und gelesen. Stark durch Layout verstümmelte Folien (F03 S.4–6, F04.1 S.6) nur sinngemäß.
- **F11.2:** nur Text überflogen, Matlab-Skripte und Screenshots nicht gelesen.
- **Theory Manual (105 S.):** Text vollständig gelesen. Gleichungen als Bild nur gerendert und geprüft für Gl. 2.1–2.7, 3.2–3.19, 13.1 und 14.1. Nicht gerendert und nicht geprüft: Gl. 5.1, 6.1–6.3, 8.1–8.2, 9.1–9.2, 11.x, 12.x. Kapitel 11 und 12 (UHF, VDD) nur überflogen. Abbildungen nicht ausgewertet.
- **Kurzanleitung (55 S.):** Text gelesen, Kapitel 1 (Sicherheit) und Verkabelungsabbildungen nur überflogen. Keine Messbereiche, Rauschwerte oder Bandbreiten für QTec enthalten.
- **Einpunkt-Laservibrometer:** VibroFlex Connect Betriebsanleitung: Kap. 1–4 überflogen, Kap. 5 (Einstellungen) und 7 (Spezifikationen) gelesen. SPECS: Inhaltsverzeichnis und Signalverzögerung (S.29) gelesen, Rauschwerte und Decoderdaten nicht ausgewertet. VibroFlex Xtra: nur Kap. 4.5, 4.6 und 6 gelesen. SI-Dokumente (Sicherheit) nicht gelesen.
- **Über den Auftrag hinaus, gezielt und nicht vollständig:**
  - SWA (347 S.): gelesen: Kap. 1, 3.1.2, 3.2.2, 3.3, 5.3, 7 (komplett), 8, 9.3, 9.4.2. Nicht gelesen: Kap. 2, 4, 5.1–5.2 (Abgleich im Detail), 6, 9.1–9.2, 10.
  - SWP (197 S.): gelesen: 3.2.1 (Cursor), 3.3.1, 3.7.10.1, 4.1, 4.2, 4.4, 5.2.7–5.2.10 teilweise. Übrige Kapitel nicht gelesen.
  - Die englischen Versionen (Software Manual PSV, PSV Desktop) nicht separat gelesen, inhaltsgleich angenommen [U].
- **Nicht gelesen:** Windows-Hilfedateien (`.chm`: Basic Engine Manual, Polytec File Access Object Model Reference, Psv_deu.chm), maßgeblich für COM-API und Datenformate. `Handbücher/nicht vorhandene Systeme/`. `Input/literatur/Example_Library_STABCOOL/`. COM-Dokument nur überflogen (Zuständigkeit `software-engineer`).
- Keine Messdaten und keine Hardware bewertet. Die Schulungsfolien, Handbücher und alle Sollwerte beziehen sich auf die Dokumentation, nicht auf eine Messung am Laborgerät.

---

## 11. Verifikation

Skripte im Scratchpad `/tmp/claude-0/-home-user/e6b61297-17fb-5003-91f8-95c4534d012c/scratchpad/i2/`, ausgeführt mit numpy 2.5.3 und scipy:

| Skript | Prüft | Ergebnis |
|---|---|---|
| `check1.py` | ENBW und Scalloping der Standardfenster | Polytec-Tabelle 5.1 bestätigt (bis auf Flat-Top-Detail) |
| `check2.py` | RMS-Gl. 3.17 (Sinus, Rauschen); H1/H2/COH exakt gegen Polytec-Näherungen; Monte-Carlo-Gegenprobe | H1 exakt wie Gl. 3.10; H2 und COH exakt abweichend von 3.11/3.12 erster Ordnung |
| `check3.py` | −3-dB-Breiten von SDOF-Mobilität, Receptance, Akzeleranz; 3D-Rauschverstärkung und Konditionszahl; Sweep-Zahlen; Doppler-Zahlen | Mobilität exakt 2ζf_n; κ = 1,685 bei 40°; Sweep-Zahlen reproduziert |
| `check4.py` | Overlap-Summen (Hann, Flat Top, Rechteck) | Hann: Σw² konstant bei 2/3 und 3/4; Flat Top bei 3/4 nicht |
| (Inline) | PSD gegen scipy-welch; Tukey α = 0,2 gegen Tapered Hanning; Eigenwerte freier Balken | PSD identisch; ENBW 1,080 bestätigt; λ_n L bestätigt |
| `pg.py`, `txt/` | Text-Extrakte der PDFs mit Seitenmarken | Grundlage der Zitate |

---

## Rückmeldung an den Orchestrator

**Paket:** I2 · **Status:** ERLEDIGT

**Ergebnis:** Fachbericht entlang der Leitfragen (Abschnitte 2–8) in dieser Nachricht, keine Datei im Repository.
Teilantwort Kapitel 4: Das Paket steuert die PSV-Software über COM, die Signalverarbeitung der Erfassung bleibt bei Polytec. Eigene Spektralschätzung ist nur aus Zeitdaten (Option TDD) möglich.

**Wie verifiziert:** Quellenbelege je Aussage (PDF-Seite und gedruckte Seite). Gleichungen der Handbücher als Bild gerendert und gelesen (TM Kap. 2, 3, 13.1, 14.1; SWA Gl. 7.1–7.4). Sollwerte nachgerechnet mit `check1.py` bis `check4.py` im Scratchpad `/tmp/claude-0/-home-user/e6b61297-17fb-5003-91f8-95c4534d012c/scratchpad/i2/` (siehe Abschnitt 11).

**Akzeptanzkriterien:**
- A1 Fachbericht mit Belegen: ✅
- A2 Priorisierte Liste Fachgrundlagen/Referenzfälle: ✅ (Abschnitt 6, 13 Einträge, Sollwerte nachgerechnet)
- A3 Rechercheaufträge: ✅ (Abschnitt 7.3, R1–R12, Kandidaten unverifiziert)
- A4 Nicht Gelesenes explizit: ✅ (Abschnitt 10)

**Befunde (nur Fachabnahme):** entfällt.

**Annahmen:**
- Gerät ist PSV QTec 3D-H mit Frontend PSV-F-600-3D-H (laut Kurzanleitung). Wirkung: Formeln 2,5·BW und H-System-Verhalten gelten.
- Software-Version am Laborrechner ist 10.1 (Handbuchstand). Wirkung: Parameter und Statuswerte wie dokumentiert.
- Die DC-Linie wird nicht gespeichert, Linie k liegt bei k·Δf (indirekt belegt). Wirkung: Frequenzvektor im Python-Code; Gegenprobe an einer realen Datei nötig.
- Angaben der VibroFlex-Anleitung (Trackingfilter, Aussteuerung 30–80 %) gelten sinngemäß auch für QTec. Wirkung: nur als Hinweis, nicht als harte Grenze verwenden.
- PSV-500-spezifische Angaben (Bandbreite 100 kHz, Sichtbarkeitsmaxima 204 mm) werden nicht auf QTec übertragen.

**Unsicherheiten:**
- Exakte Definition von Tapered Hanning und die Flat-Top-Koeffizienten von Polytec sind nicht dokumentiert (ENBW passt, Fehler bei Halb-Bin weicht ab).
- Ob H-Systeme intern Blöcke mit 2,5·n_FFT Samples (nicht Zweierpotenz) verarbeiten.
- Wie Polytec die 3D-Richtungsmatrix intern bildet; die Herleitung u = D·v ist meine eigene.
- Welche Größen (Alignment-Qualität, Signalpegel/RSSI, Overrange) über COM abrufbar sind (Zuständigkeit `software-engineer`).
- Verfügbarkeit der Optionen TDD, PCA, GeoPro am Labor.
- Gleichungen 5.1, 6.1–6.3, 8.x, 9.x des Theory Manual nicht im Bild geprüft.
- Alle Literaturkandidaten in 7.3 unverifiziert.

**Rechercheaufträge:** R1–R12 (Abschnitt 7.3). Besonders dringlich: R12 (Spezifikation PSV QTec 3D, "Volltext benötigt"), R1 (H1/H2/Hv und Kohärenz), R2 (Fenster/ENBW), R3 (Modalanalyse, MAC), R4 (LDV-Fehler).

**Rückfragen:**
- [blockierend] Soll die Auswertung nur ODS und Spektren liefern oder auch Modalparameter? — *Auswirkung:* Umfang von FG-04 (SDOF gegen MDOF), Notwendigkeit einer Kraftmessung.
- [blockierend] Wird die Anregungskraft gemessen, oder ist die Referenz nur das Generatorsignal in Volt? — *Auswirkung:* FRF als Mobilität (m/s)/N oder (m/s)/V; Modalskalierung.
- [nicht blockierend] Prüfling, Lagerung, Frequenzbereich, Anregungsart und Signalform. — *Annahme bis zur Klärung:* alles konfigurierbar, keine festen Werte.
- [nicht blockierend] Software-Version und installierte Optionen am Laborrechner. — *Annahme:* 10.1, H-System.
- [nicht blockierend] Existiert ein VibroFlex-Connect oder anderes Einpunktvibrometer im Labor, und welche Rolle soll es spielen? — *Annahme:* nicht vorhanden.
- [nicht blockierend] Quantitative Anforderung an Reproduzierbarkeit (Eigenfrequenztoleranz, MAC-Schwelle) und etwaige Normen. — *Annahme:* Schwellwerte konfigurierbar.
- [nicht blockierend] Gewünschter Datenpfad (Polytec File Access oder UFF) und Verfügbarkeit der Time-Domain-Option. — *Annahme:* Polytec File Access, TDD unbekannt.
- [nicht blockierend] Liegt das Spezifikationshandbuch zum PSV QTec 3D vor?

**Vorschlag für KONVENTIONEN.md** (nicht angelegt, Entscheidung beim Nutzer):
- FRF-Definition: H(f) = V/R (Antwort/Referenz), H1 = CP_RV/AP_RR mit CP_RV = R*·V; Einheiten SI, Antwort in m/s, Referenz in N oder V; bei Kraftreferenz Mobilität in (m/s)/N.
- Spektren: einseitig, Spitzenamplitude (0-to-peak), amplitudentreue Fensternormierung wie Polytec; Phase φ0 in rad für $A\cos(\omega t + \varphi_0)$; Zeitabhängigkeit $e^{+i\omega t}$ (entspricht `numpy.fft.rfft`).
- Frequenzachse von Polytec-Spektren: f_k = k·Δf, k = 1…n_FFT, DC nicht enthalten (nach Prüfung an realer Datei bestätigen).
- Abtastung: fs = 2,5·BW (H-System); Messzeit T = n_FFT/BW; Δf = BW/n_FFT.
- Vorzeichen: positive Geschwindigkeit = Bewegung zum Scankopf; 3D-Komponenten im Objektkoordinatensystem (Alignment).
- "Gemitteltes Spektrum" (Betragsmittel) nicht mit komplexem Mittel verwechseln; "Dämpfung" (Polytec) = −3-dB-Breite Δf, Dämpfungsgrad ζ = Δf/(2f).

**Thesis-Bezug:** Grundlagenkapitel (LDV-Prinzip, 3D-Vektorzerlegung, Signalverarbeitung, Modalanalyse/ODS, Messunsicherheit) und Methodik-/Implementierungskapitel (Polytec-Konventionen, Validierungsstrategie gegen analytische Referenzfälle).

**Empfehlung für den nächsten Schritt:**
1. Beide blockierenden Fragen (Ziel der Auswertung, Kraftreferenz) per AskUserQuestion klären.
2. Fachgrundlage FG-01 (Spektralschätzung nach Polytec-Konvention) und FG-02 (FRF, Kohärenz) als Pakete an `strukturdynamik-experte` vergeben. FG-03 (3D-Rekonstruktion) und FG-04 (SDOF-Peak, Modalparameter) danach, abhängig von den Antworten.
3. Parallel Recherchepaket R1–R4 und R12 an `literatur-rechercheur`; den Nutzer um das Spezifikationshandbuch zum PSV QTec 3D bitten.
4. Dem `software-engineer` die Konventionen aus dem KONVENTIONEN-Vorschlag weitergeben, vor allem Frequenzachse (k·Δf ab k = 1) und die Frage, welche Größen (Alignment-Qualität, Status, Settings) über COM bzw. Polytec File Access lesbar sind.
