<!-- Analysebericht W3 (Fachanalyse): Was bei der Auswertung von PSV-QTec-3D-Messungen anders oder besser gemacht werden könnte; erstellt im Paket W3 von strukturdynamik-experte. Stand 2026-10-29. Kein Code, keine Sollwerte (das ist W4). -->

# W3 – Verbesserungsmöglichkeiten bei der Auswertung von PSV-Messungen

**Zweck.** Diese Analyse ist eine Entscheidungsgrundlage für den Nutzer. Sie trennt das, was
für die Muss-Anforderungen R-050 bis R-053 nötig ist, von echten Erweiterungen (R-054 und
darüber hinaus). Sie entscheidet nichts. Grundlage sind die Bestandsaufnahme W1, die
Formatanalyse W2, der Fachbericht I2 und eigene Stichproben an der Messdatei
`Input/20261012_ref_Mitte.svd` (nur lesend, über den W2-Leser).

## 0 Kennzeichnung

| Kürzel | Bedeutung |
|---|---|
| **[H]** | Herstellerangabe (Polytec), Beleg in W1/I2 mit Seite |
| **[W2]** | Befund aus W2 an der echten Datei |
| **[D]** | eigene Stichprobe an der echten Datei in W3 (Skripte im Anhang) |
| **[A]** | eigene analytische Herleitung (im Text vollständig) |
| **[E]** | eigene fachliche Einschätzung, nicht belegt |
| **[L-m]** | Fachliteratur aus `literatur.bib`, Prüfstand **metadaten**: Inhalt nicht gelesen, Aussage noch nicht belegt |

Alle Literaturstellen außer den Polytec-Dokumenten haben heute nur den Prüfstand
`metadaten`. Wo eine Zeile sich auf ein Lehrbuch stützen soll, ist das ein
Rechercheauftrag und kein Beleg.

---

## 1 Kernaussagen

1. **Phasensinn der Kreuzspektren ist physikalisch gestützt [D, A].** An 17 391 Resonanzspitzen
   von H1 (Vib Z / Ref1, alle 135 Punkte, γ² > 0,9) fällt die Phase in 98,2 % der Fälle mit
   steigender Frequenz. Das passt zu einem kausalen System bei Zeitabhängigkeit $e^{+i\omega t}$,
   wenn $H_1 = \mathrm{CP}/\mathrm{AP}_\mathrm{Ref}$ mit den gespeicherten CP gebildet wird, also
   $\mathrm{CP} = \langle V\,R^{*}\rangle$ (Mittel über die Blöcke von Antwort mal konjugierter Referenz, $\langle\cdot\rangle$ = Mittelwert). Eine Konjugation ist
   damit nicht nötig. Ob PSV die Phase genauso **anzeigt**, bleibt Prüfschritt M1.
2. **Vorzeichen der Referenzkanäle auffällig [D, A].** Ref2/Ref1 (Beschleunigung/Kraft) verhält
   sich wie eine Antriebspunkt-Akzeleranz: Spitzen und Senken wechseln sich ab, die Streuung
   über die Punkte beträgt 1 %. Die Wirkleistung aus diesen Daten ist aber an **allen** 1 590
   Linien mit γ² > 0,95 negativ, $\mathrm{Re}\{Y\} < 0$. Ein passiver Antriebspunkt verlangt
   $\mathrm{Re}\{Y\} \ge 0$. Wahrscheinlich ist eines der beiden Referenzsignale im Vorzeichen
   gedreht (Einbaurichtung oder Sensorkonvention), oder Ref2 sitzt nicht am Kraftangriffspunkt.
   Das muss mit dem Betreuer geklärt werden. Ist die Kraft gedreht, sind alle H1-Phasen um π
   versetzt.
3. **Dämpfung über die −3-dB-Breite ist bei dieser Messung durch die Auflösung begrenzt [D].**
   Bis etwa 700 Hz ist die −3-dB-Breite der Spitzen im Punktmittel von |H1_Z| meist nur
   0,7 bis 2 Linien breit (Δf = 1,5625 Hz). Eine Breitenschätzung aus so wenigen Linien ist
   stark verzerrt. Das gilt für PSV wie für eigenen Code. Mit „stimmt mit PSV überein“ ist
   deshalb nicht gezeigt, dass der Wert physikalisch stimmt.
4. **Abklingen im Messfenster ist fraglich [A, E].** Die Blockdauer beträgt T = 0,64 s. Für
   schwach gedämpfte Moden ist die freie Schwingung am Blockende noch nicht abgeklungen. Bei
   f = 100 Hz und ζ = 0,005 bleiben exp(−ζωT) = 13 % übrig. Bei Burst-Anregung mit
   Rechteckfenster erzeugt das Leckage und verbreitert die Spitzen. Die Kohärenz zeigt solche
   Fehler **nicht** an, weil sie bei deterministischer Anregung kohärent sind.
5. **„Echte komplexe Mittelung“ über Punkte ist kein allgemeiner Ersatz für das Betragsmittel
   [D, A].** An Moden mit Knotenlinien löscht sich das komplexe Punktmittel aus: Es erreicht
   an den Spitzen nur 19 bis 100 % des Betragsmittels. Es ist eine eigene Größe (Netto- oder
   Volumenschnelle). Energetisch begründet ist das quadratische Mittel; es liegt 2 bis 28 %
   über dem Betragsmittel.
6. **CPH ist der kohärente Anteil des Antwortspektrums [D].** In dieser Datei gilt
   |CPH| = |CP|/√AP_Ref auf 0,6 % genau (1-%- bis 99-%-Quantil). Damit ist
   $|\mathrm{CPH}|^2 \approx \gamma^2\,\mathrm{AP}_\mathrm{Antwort}$. Das von PSV gezeigte
   „Geschwindigkeit“-Spektrum ist also nicht √AP. Für R-050 muss festgelegt werden, welches
   der beiden Spektren gemeint ist.
7. **Zur Bandbreitenfrage (M7)** geben die Daten keine Entscheidung. Ein Tiefpass im Decoder
   würde H1 oberhalb 1 kHz in Betrag und Phase verfälschen, die Kohärenz aber nicht senken.
   Das lässt sich nur über das Datenblatt oder den Betreuer klären.

---

## 2 Fachliche Prüfung der W2-Deutungen (A3)

### 2.1 Tabelle

| W2-Deutung | Prüfung in W3 | Urteil | Für W4 noch zu klären |
|---|---|---|---|
| **CP** = gemitteltes Kreuzspektrum Antwort/Referenz, `CP[S_a, S_b]` | Kausalitätstest (2.2): Phase von CP/AP_Ref fällt an 98,2 % der Spitzen. Das entspricht $\mathrm{CP} = \langle A\,B^{*}\rangle$ bei $e^{+i\omega t}$. Es passt zu $\mathrm{CP}_{RV} = R^{*}V$ aus TM S. 14 (I2 3.4 [H]) | **gestützt**: Phase physikalisch konsistent; Anzeige in PSV offen | M1 bleibt für „stimmt mit PSV überein“ nötig. Vorschlag: Konvention $\mathrm{CP}_{ab} = \langle a\,b^{*}\rangle$ mit a = Antwort |
| **AP** = $\langle\lvert S\rvert^2\rangle$, Einheit (Größe)² | Ungleichungen W2; Jensen AP ≥ ABS² [W2] | **bestätigt** | Wegen der Spitzenwert-Skalierung ist der quadratische Mittelwert $\mathrm{AP}/2$. Daraus folgen RMS und PSD: $\mathrm{PSD} = \mathrm{AP}/(2\,\mathrm{RBW})$ (TM S. 17, I2 3.7 [H]) |
| **ABS** = Betragsmittel | Jensen-Prüfung [W2] | **bestätigt** | – |
| **CPH** = Antwort mit Phase relativ zur Referenz | Auf 0,6 % gilt |CPH| = |CP|/√AP_Ref [D]; die Phase ist gleich [W2]. Die Deutung als Mittel von $X\,R^{*}/\lvert R\rvert$ passt zur komplexen Mittelung „auf Referenzkanal bezogen“ (TM S. 34, I2 3.3 [H]) | **plausibel**. Gleichheit mit CP/√AP_Ref gilt nur, solange die Referenzamplitude von Mittelung zu Mittelung konstant ist | Für R-050 festlegen: Ist das „Spektrum“ |CPH| (kohärent, wie PSV-Anzeige) oder √AP (Leistungsmittel inkl. Rauschen)? |
| **H1** = CP/AP_Ref, **H2** = AP_Antwort/CP*, **COH** = \|CP\|²/(AP·AP) | Punktmittel der Beträge von PSV reproduziert [W2]. H2 hat dieselbe Phase wie H1 [A]: $\arg(\mathrm{AP}/\mathrm{CP}^{*}) = \arg \mathrm{CP}$ | **bestätigt** (Beträge), Phase wie CP | In dieser Datei gilt H1 ≈ H2 oberhalb 150 Hz (γ²: Median 1,000; 10-%-Quantil ≥ 0,998 [D]). Darunter fällt das 10-%-Quantil bis 0,83. Die Wahl zwischen H1 und H2 ist hier nur unter 150 Hz relevant |
| **Skalierung 0-to-peak** | Band-Effektivwerte = √(Σ\|A\|²/2) [W2] | **plausibel**. Der Bandwert enthält **keinen** Fensterfaktor $W_\mathrm{RBW}$ | TM Gl. 3.17: $\mathrm{RMS} = \sqrt{\sum \mathrm{AP}/(2 W_\mathrm{RBW})}$ (I2 3.7 [H]). Entweder war das Fenster ein Rechteck ($W_\mathrm{RBW} = 1$) oder PSV korrigiert im Band nicht. **Fensterart der Messung ist unbekannt** (M5 erweitern). Absolute Kalibrierung: M4 |
| **Einheiten** Ref1 N, Ref2 m/s², Vib m/s | Größenordnungen plausibel: √AP_F ≈ 0,006 bis 0,03 N, √AP_A ≈ 0,007 bis 0,4 m/s², √AP_Vz ≈ 2 bis 5·10⁻⁵ m/s [D] | **plausibel** | Daraus folgen: H1_Vib/Ref1 in (m/s)/N (Mobilität), Ref2/Ref1 in (m/s²)/N (Akzeleranz), Vib/Ref2 in s. Vorzeichen der Referenzen klären (2.3) |
| **Frequenzachse** $f_k = k\,\Delta f$, k = 1…1600 | Aus den Daten nicht prüfbar. Ein Versatz um eine Linie verschiebt alle Frequenzen um 1,5625 Hz; dafür fehlt eine Referenz mit bekannter Frequenz | **offen** (wie W2) | M2 ist **vor** den Sollwerten in W4 nötig, weil Spitzenfrequenz und Bandgrenzen davon abhängen |
| **Blockdauer** 0,64 s, $f_s$ = 6 250 Hz | Passt zu $f_s = 2{,}5\,BW$ (I2 3.1 [H]) | **plausibel** | Für das Abklingkriterium (2.5) ist die Burstlänge nötig (Generator-Einstellung, M5) |
| **Bandbreitenbereich 1 kHz bei BW 2 500 Hz** | siehe 2.6 | **offen**, fachlich relevant | Gültigkeitsbereich der Auswertung oberhalb 1 kHz festlegen |

### 2.2 Herleitung: Phasensinn an einer Resonanz [A]

Konvention: $x(t) = \mathrm{Re}\{\hat x\,e^{i\omega t}\}$. Ein Pol des kausalen Systems liefert
den Anteil $\dfrac{r}{i\omega - p}$ mit $p = -\sigma + i\omega_d$, $\sigma > 0$. Nahe
$\omega_d$ gilt

$$\frac{r}{\sigma + i(\omega - \omega_d)}, \qquad
\arg = \arg r - \arctan\frac{\omega - \omega_d}{\sigma},$$

die Phase **fällt** also beim Durchlaufen der Resonanz um etwa π, unabhängig vom Vorzeichen
von r. Konjugiert man die FRF ($e^{-i\omega t}$ oder vertauschte Konjugation im
Kreuzspektrum), **steigt** die Phase. Ein Vorzeichenwechsel eines Kanals (Faktor −1) ändert
den Phasensinn **nicht**. Nullstellen eines Antriebspunkts liegen ebenfalls in der stabilen
Halbebene; dort steigt die Phase.

Datenbefund [D]: H1_Z an allen Punkten: Phase steigend an 1,8 % der Spitzen (17 391 Spitzen).
Ref2/Ref1: steigend an 5 % der 134 Spitzen und an 98 % der 127 Senken. Beides ist konsistent
mit „nicht konjugiert“. Die Restanteile erklären sich durch dicht liegende Moden und die
Auswertung über nur zwei Linien.

### 2.3 Herleitung: Passivität am Antriebspunkt [A]

Mittlere eingeleitete Leistung bei harmonischer Kraft $\hat F$ und Schnelle $\hat v$ am
selben Ort und in derselben Richtung:

$$\bar P = \tfrac12\,\mathrm{Re}\{\hat F^{*}\hat v\} = \tfrac12\,\lvert\hat F\rvert^2\,\mathrm{Re}\{Y\} \ge 0,
\qquad Y = \hat v/\hat F\ \ [\mathrm{(m/s)/N}].$$

Mit $\hat a = i\omega\,\hat v$ folgt $\mathrm{Im}\{\hat a/\hat F\} = \omega\,\mathrm{Re}\{Y\} \ge 0$.

Datenbefund [D]: $Y = (\mathrm{CP}_{6}/\mathrm{AP}_{12})/(i\omega)$ hat an allen 1 590 Linien
mit γ² > 0,95 einen **negativen** Realteil. Die Phase von $\hat a/\hat F$ liegt zwischen −3°
und −178° (Stichproben 50 Hz bis 2,4 kHz). Nach 2.2 ist das keine Konjugation. Es bleiben
zwei Deutungen:
- ein Kanal mit umgekehrtem Vorzeichen (Kraftsensor, Beschleunigungsaufnehmer oder
  Einbaurichtung), oder
- Ref2 misst nicht am Kraftangriffspunkt bzw. nicht in Kraftrichtung. Das ist weniger
  wahrscheinlich, weil eine Übertragungsstelle Vorzeichenwechsel von Re{Y} zeigen würde.

Kein Messpunkt des Rasters verhält sich wie ein Antriebspunkt: Im Punkt nahe der
Rastermitte ist Re{H1_Z} an 52 % der Linien positiv [D]. Ob der Shaker auf der Rückseite,
außerhalb des Rasters oder anders angekoppelt war, ist offen.

**Auswirkung:** Die Form einer Betriebsschwingform bleibt gleich, ihr globales Vorzeichen
und das Vorzeichen von Residuen und Realteilen nicht. Für R-052 genügt eine dokumentierte
Konvention. Für einen späteren Vergleich mit Rechnung oder Modalanalyse ist das Vorzeichen
wesentlich.

### 2.4 3D-Betrag und Schwingform [A]

PSV gibt für den 3D-Kanal $A = \sqrt{A_x^2 + A_y^2 + A_z^2}$ ohne Phase an (I2 3.8 [H]).
Für eine Bewegung $\vec x(t) = \mathrm{Re}\{\hat{\vec a}\,e^{i\omega t}\}$ gilt

$$\lvert\vec x\rvert^2 = \tfrac12\sum_i \lvert\hat a_i\rvert^2 + \tfrac12\,\mathrm{Re}\Big\{\sum_i \hat a_i^2\,e^{2i\omega t}\Big\}
\;\Rightarrow\;
\max_t \lvert\vec x\rvert = \sqrt{\tfrac12\Big(\sum_i\lvert\hat a_i\rvert^2 + \Big\lvert\sum_i \hat a_i^2\Big\rvert\Big)}.$$

Der PSV-Betrag ist also eine obere Schranke für die größte Auslenkung. Gleichheit gilt nur,
wenn alle Komponenten gleichphasig sind. Bei kreisförmiger Bewegung, z. B. $\hat{\vec a} = (1, i, 0)$,
ist die größte Auslenkung 1, der PSV-Betrag √2. Da alle drei Komponenten in dieser Datei
auf Ref1 bezogen sind, ist eine vollständige 3D-Schwingform mit Phase möglich.

### 2.5 Auflösung und Abklingen [A]

- Für den Einmassenschwinger ist die −3-dB-Breite der Mobilität exakt $B = 2\zeta f_n$
  (I2 6.1, FG-04, nachgerechnet). Pro Halbwertsbreite liegen $B/\Delta f$ Linien.
- Abklingen der freien Schwingung: Hüllkurve $e^{-\zeta\omega_n t}$. Rest am Blockende
  $e^{-\zeta\omega_n T}$.

| Beispiel | $B/\Delta f$ | Rest nach T = 0,64 s | Rest nach 0,6·T (falls der Burst 40 % belegt) |
|---|---|---|---|
| 100 Hz, ζ = 0,005 | 0,64 | 0,134 | 0,299 |
| 200 Hz, ζ = 0,004 | 1,02 | 0,040 | 0,145 |
| 1 000 Hz, ζ = 0,002 | 2,56 | < 0,001 | 0,008 |

Die ζ-Werte sind Größenordnungen aus den Daten, keine Messwerte. Die Burstlänge 40 % ist
**nur ein Rechenbeispiel**. Das W2-Feld 0,4 im Generator-Stream ist nicht gedeutet.

Befund an der Datei [D]: Im Punktmittel |H1_Z| haben die Spitzen bis etwa 700 Hz eine
interpolierte −3-dB-Breite von 0,7 bis 2 Linien. Werte unter einer Linie zeigen, dass die
Breite nicht aufgelöst ist. Zudem liegen Spitzen eng beieinander (z. B. 262,5 / 265,6 /
270,3 Hz; 303,1 / 306,3 Hz). Dort ist die Halbwertsbreite einer einzelnen Mode nicht
definiert.

### 2.6 Bedeutung der Bandbreitenfrage (M7) [E]

- Ist „Bandbreitenbereich 1 kHz“ ein Tiefpass im Geschwindigkeitspfad, dann werden die
  Vibrometerkanäle oberhalb von etwa 1 kHz in Betrag und Phase verändert, die Referenzen
  nicht. H1, H2 und die Schwingformen wären dort verzerrt. Die Kohärenz bliebe nahe 1, weil
  ein lineares Filter kohärent ist.
- An der Datei ist nichts Eindeutiges zu sehen [D]: Das räumlich quadratisch gemittelte
  |H1_Z| ist oberhalb etwa 700 Hz kleiner (0,005 bis 0,008 gegen 0,014 bis 0,019 (m/s)/N),
  zeigt aber keine Kante bei 1 kHz. Das kann auch an der Struktur oder an der Dämpfung
  liegen.
- Für W4 folgt daraus: Sollwerte aus analytischen Fällen sind davon nicht betroffen. Die
  **Gültigkeit** der Auswertung realer Daten oberhalb 1 kHz muss aber als offener Punkt
  geführt werden, bis Datenblatt oder Betreuer die Bedeutung klären.

### 2.7 Weitere Beobachtungen an der Datei [D]

- **Referenzstabilität:** √AP_F und |A/F| schwanken über die 135 Punkte nur um 1 %
  (Median über 150 bis 2 400 Hz). Die Anregung war über den Scan gleichmäßig.
- **Drift:** Die Resonanzfrequenzen von Ref2/Ref1 fallen über die 40 min Scandauer leicht
  (z. B. 418,8 Hz: −0,05 Hz; 1 507,8 Hz: −0,23 Hz; 2 240,6 Hz: −0,69 Hz; Parabel durch drei
  Linien, linearer Trend über die Zeitstempel der Punkte). Das sind relativ 1 bis 3·10⁻⁴,
  kleiner als Δf, aber systematisch (Temperatur? [E]). Für den Vergleich mehrerer Messungen
  ist das relevant.
- **Kohärenz:** unter 150 Hz niedriger (10-%-Quantil 0,83), darüber praktisch 1. Die Ursache
  (wenig Kraft, Umgebung, Vibrometerrauschen) ist eine Versuchsfrage.

---

## 3 Verbesserungsmöglichkeiten (A1)

Aufwand: gering (Tage), mittel (bis zwei Wochen), hoch (mehr), grob geschätzt [E].
„Heute“ beschreibt den PSV-Weg laut W1/W2.

### 3.1 Teil A – nötig zur Erfüllung von R-050 bis R-053

| Nr. | Thema | Heute (Beleg) | Anders / besser | Fachlicher Nutzen | Aufwand | Risiko / Voraussetzung | Bezug | Quelle, Prüfstand |
|---|---|---|---|---|---|---|---|---|
| A-1 | Phasen- und Vorzeichenkonvention | Phasenvorzeichen offen (W2 2.4, M1); Konvention $e^{+i\omega t}$ in KONVENTIONEN aus TM | Konvention $\mathrm{CP}_{ab} = \langle a\,b^{*}\rangle$, $H_1 = \mathrm{CP}/\mathrm{AP}_\mathrm{Ref}$ festschreiben; automatische Prüfung des Phasensinns an Resonanzen (2.2) beim Einlesen | ODS-Phase und spätere Modalgrößen physikalisch richtig; Fehler beim Einlesen fallen sofort auf | gering | M1 für die PSV-Anzeige; Vorzeichen der Referenzen (2.3) | R-051, R-052 | TM S. 14 über I2 [H]; [A]; [D] |
| A-2 | Spektrum je Punkt eindeutig benennen | PSV zeigt „Geschwindigkeit“ = CPH (W2 2.1); daneben AP, ABS | Zwei Größen getrennt anbieten: $\lvert\mathrm{CPH}\rvert$ (kohärent, phasenbezogen) und $\sqrt{\mathrm{AP}}$ (Leistungsmittel inkl. Rauschen); Einheit 0-to-peak im Achsentitel; Effektivwert = Spitze/√2 | Kein stiller Unterschied von bis zu γ zwischen beiden Spektren; Vergleichbarkeit mit PSV | gering | Festlegung, welche Größe R-050 meint | R-050 | [W2], [D] |
| A-3 | Gemitteltes Spektrum PSV-konform | PSV: Betragsmittel der gültigen Punkte (W1 1.5, PFA-Beispiel) | Betragsmittel über **gültige** Punkte wie PSV; Punktstatus aus der Datei auswerten | Übereinstimmung mit PSV (Akzeptanzkriterium) | gering | Statusfelder sind noch nicht gedeutet (W2 3.2, M6); in dieser Datei sind alle Punkte enthalten | R-050 | [H] W1; [W2] |
| A-4 | H1, H2, Kohärenz aus CP/AP | PSV bildet sie beim Anzeigen (W2 2.4) | Aus CP/AP der Datei nach den bestätigten Formeln; Linien mit niedriger Kohärenz kennzeichnen statt verwerfen | Gleiche Werte wie PSV; Qualität sichtbar | gering | Schwelle für „niedrige Kohärenz“ legt der Nutzer fest | R-051 | [W2]; TM über I2 [H] |
| A-5 | Betriebsschwingform | Animation bei gewählter Frequenz, Betrag 3D ohne Phase (W1 1.1, I2 3.8) | Komplexe Amplitude je Komponente relativ Ref1 auf der nächsten Linie; Momentanwert $\mathrm{Re}\{\hat a\,e^{i\omega t}\}$; ohne Referenz/Trigger nur Betrag mit Kennzeichnung; 3D-Betrag wie PSV **und** als Hinweis die echte größte Auslenkung (2.4) | Lastenheft-Vorgabe; 3D-Betrag überschätzt bei elliptischer Bewegung bis Faktor √2 | gering bis mittel | Vorzeichen der Kraft (2.3); Frequenzachse (M2) | R-052 | [H]; [A] |
| A-6 | Spitzensuche und −3-dB-Breite | 1-DOF-Kleinste-Quadrate-Fit im Band-Cursor, Algorithmus unbeschrieben (W1 1.2, 1.5) | Spitzen auf **H1** statt auf dem Antwortspektrum suchen (die Kraft ist nicht flach: √AP_F 0,006 bis 0,03 N [D]); −3-dB-Schnittpunkte linear interpoliert; $Q = f/B$, $\zeta = B/(2f)$ wie PSV; Warnhinweis, wenn $B$ nur wenige Linien umfasst oder Nachbarspitzen innerhalb der Breite liegen | Ergebnis ehrlich gekennzeichnet; Fehldeutung als „genaue Dämpfung“ vermieden | mittel | Exakte Übereinstimmung mit dem PSV-Fit ist nicht erreichbar, weil der Algorithmus unbekannt ist: Toleranz nötig (Frage F4) | R-053 | HB 9-11 [H]; [A] 2.5; Ewins [L-m] |
| A-7 | Band-RMS physikalisch eindeutig | Bandwert = √(Σ\|A\|²/2) ohne Fensterfaktor (W2 2.4); TM Gl. 3.17 mit $W_\mathrm{RBW}$ | $\mathrm{RMS} = \sqrt{\sum \mathrm{AP}/(2 W_\mathrm{RBW})}$ mit dokumentiertem Fenster; Regel für Linien auf den Bandgrenzen; Band-„RMS“ einer FRF als Bandnorm in (m/s)/N kennzeichnen, nicht als physikalischen Effektivwert | Effektivwert unabhängig von der Fensterwahl; keine Einheitenverwechslung | gering | Fensterart der Messung (M5) | R-053 | TM über I2 [H]; [W2] |
| A-8 | Frequenzachse und Linienzuordnung | vorläufig $k\,\Delta f$, k = 1…n (KONVENTIONEN) | Prüfschritt M2 vor W4; Achse immer aus der Datei | Sonst alle Spitzenfrequenzen um eine Linie falsch | gering | Zugriff auf PSV oder PFA am Messrechner | R-050 bis R-053 | KONVENTIONEN; W2 3.1 |

### 3.2 Teil B – Erweiterungen (R-054 oder darüber hinaus)

| Nr. | Thema | Heute (Beleg) | Anders / besser | Fachlicher Nutzen | Aufwand | Risiko / Voraussetzung | Bezug | Quelle, Prüfstand |
|---|---|---|---|---|---|---|---|---|
| B-1 | Parametrische Dämpfungsschätzung | Nur 1-DOF-Fit (W1 1.2); Halbwertsbreite auflösungsbegrenzt (2.5) | Kreisfit (Nyquist-Kreis) oder komplexer 1-DOF-Fit an H1 mit mehreren Linien und Phase; für eng liegende Moden ein Mehr-DOF-Fit (rationale Funktion, LSCF/LSFD) | Nutzt Phase und alle Linien um die Resonanz; trennt benachbarte Moden | mittel (Kreisfit) bis hoch (Mehr-DOF) | Bei < 2 Linien je Halbwertsbreite stößt auch ein Fit an Grenzen; besser wäre eine feinere Auflösung bei der Messung (Versuchsfrage); Abklingen im Fenster (2.5) | R-053, R-054 | Ewins, Maia/Silva, Peeters [L-m]; [A] |
| B-2 | Unsicherheitsangaben | Keine (W1) | Zufallsfehler von \|H1\| und γ² aus Mittelungsanzahl $n_d$ und γ² als Band um die Kurve; Kennzeichnung systematischer Fehler (Auflösung, Leckage), die die Kohärenz nicht zeigt | Aussagekraft der Werte erkennbar; wichtig für Vergleiche | mittel | Formeln erst nach Lesen von Bendat/Piersol übernehmen; $n_d$ je Punkt ist noch nicht sicher gedeutet (W2: „7“ und Feld 7 bis 25) | R-051, R-054 | Bendat/Piersol [L-m] |
| B-3 | Kohärenzgewichtete Auswertung | Kohärenz nur angezeigt (W1 1.2) | Linien mit niedriger Kohärenz in Fits und Bandwerten heruntergewichten oder ausblenden | Robustere Fits, besonders unter 150 Hz | gering bis mittel | Gewichtung verändert die Vergleichbarkeit mit PSV; nur als Option | R-053, R-054 | [E] |
| B-4 | Automatische Plausibilitätsprüfungen | Manuell in PSV (I2 4.2, 5.2) | Beim Einlesen: W2-Ungleichungen; Phasensinn (2.2); Passivität an einem Antriebspunkt (2.3); Stabilität der Referenzen über den Scan (2.7); Drift der Resonanzfrequenzen über die Scanzeit (2.7); Auflösungshinweis (2.5); Punktstatus | Fehler in Daten, Konvention oder Aufbau werden sichtbar, bevor ausgewertet wird | gering bis mittel | Schwellen legt der Nutzer fest; Passivitätstest nur bei bekanntem Antriebspunkt | R-054 | [A], [D]; I2 5.2 |
| B-5 | Vergleich mehrerer Messungen | Koppeln/kombinierte Datei in PSV (W1 1.2) | Gleiche Punkte über Label/Koordinaten zuordnen; Spitzenfrequenzen, FRF-Differenz, MAC der Schwingformen; Drift innerhalb einer Messung mitführen | Wiederholbarkeit quantifizierbar (I2 P9) | mittel | Gleiche Geometrie und Einstellungen; Kraftbezug (H1) statt roher Antwort | R-054 | Allemang (MAC) [L-m]; [D] 2.7 |
| B-6 | Skriptbasierte Abbildungen | GUI-Export in PSV (W1 1.3) | Abbildungen per Skript aus gespeicherten Daten mit Git-Hash | Nachvollziehbarkeit; ohnehin in KONVENTIONEN gefordert | gering bis mittel | – | alle | KONVENTIONEN |
| B-7 | Export in offene Formate | ASCII nur angezeigte Daten, UFF einfach genau (W1 1.3) | Export von CP, AP, H1, H2, γ², Geometrie, Einheiten und Konvention in ein offenes Format; zusätzlich UFF 58 für Modalsoftware | Weiterverarbeitung ohne PSV; mit CP/AP lässt sich alles nachrechnen | gering bis mittel | UFF-Konventionen (Vorzeichen, Einheitenfelder) prüfen; pyuff nur [L-m] | R-054 | pyuff [L-m]; W1 1.3 |
| B-8 | 3D-Komponentenbezug | X/Y/Z im Koordinatensystem des 3D-Abgleichs (KONVENTIONEN, vorläufig) | Zerlegung in Normalen- und Tangentialanteil je Element aus der Geometrie; Bahnellipse je Punkt (2.4) | Biegung (aus der Ebene) und Längsbewegung (in der Ebene) getrennt; Z ist nur bei ebener, achsparalleler Platte die Normale | mittel | Elementnormalen aus `Elements`; Bezugssystem offen (W2 3.2) | R-052, R-054 | [A] |
| B-9 | Physikalisch begründetes Punktmittel | Nur Betragsmittel (W1 1.5) | Zusätzlich quadratisches (und flächengewichtetes) Mittel; komplexes Mittel nur als ausgewiesene Netto-Größe | Quadratisches Mittel steht in Bezug zur kinetischen Energie bei gleichmäßiger Massenbelegung [E]; das komplexe Mittel löscht sich an Knotenlinien aus (19 bis 100 % [D]) | gering | Flächengewichte aus der Geometrie | R-050 (Zusatz) | [A], [D] |
| B-10 | Umrechnung Weg/Beschleunigung | In PSV als Signalwahl (W1 1.1) | Division bzw. Multiplikation mit $i\omega$ im Frequenzbereich; Phasenbezug bleibt | Darstellung in der gewünschten Größe | gering | Linie k = 0 (DC) nicht vorhanden; Vorzeichenkonvention | R-050, R-052 | I2 2.1 [H] |
| B-11 | Modalanalyse | Nicht in PSV (W1 1.2) | Nur falls in R-054 beschlossen: Stabilisierungsdiagramm, Modalparameter | Vollständige Modalgrößen | hoch | Nicht Teil der Arbeit (R-054 gestuft) | R-054 | Ewins, Peeters [L-m] |

---

## 4 Trennung und mögliche Reihenfolge (A2)

**Für R-050 bis R-053 nötig:** A-1 bis A-8. Davon hängen A-1, A-5, A-6, A-7 und A-8 an
offenen Prüfschritten (M1, M2, M4, M5, Vorzeichen der Referenzen).

**Erweiterungen:** B-1 bis B-11. Klein und mit großem Nutzen sind B-4, B-6, B-7 und B-9.
Sie folgen größtenteils aus Daten, die für Teil A ohnehin gelesen werden.

**Mögliche Reihenfolge** (Vorschlag, keine Entscheidung):
1. Klärungen vor W4: M1, M2, M4, Fensterart und Generator (M5), Vorzeichen und Ort der
   Referenzen, Toleranz „stimmt mit PSV überein“ (Fragen in Abschnitt 6).
2. W4-Fachgrundlage für A-1 bis A-8 mit analytischen Referenzfällen.
3. Umsetzung von Teil A; dabei die Plausibilitätsprüfungen aus B-4 mitnehmen, die ohne
   Zusatzdaten auskommen (Phasensinn, W2-Ungleichungen, Referenzstabilität).
4. Am Entscheidungspunkt R-054: B-6, B-7, B-9, dann B-2/B-3, dann B-1, dann B-5, B-8.
   B-11 nur, wenn der Umfang erweitert wird.

---

## 5 Hinweise für W4

1. **Konventionen festlegen** (Vorschlag für KONVENTIONEN, Entscheidung beim Nutzer):
   $\mathrm{CP}_{ab} = \langle a\,b^{*}\rangle$ mit a = Antwort, b = Referenz;
   $H_1 = \mathrm{CP}/\mathrm{AP}_\mathrm{Ref}$, $H_2 = \mathrm{AP}_\mathrm{Antwort}/\mathrm{CP}^{*}$,
   $\gamma^2 = \lvert\mathrm{CP}\rvert^2/(\mathrm{AP}_\mathrm{Antwort}\,\mathrm{AP}_\mathrm{Ref})$;
   AP in (Einheit, Spitzenwert)², quadratischer Mittelwert = AP/2.
2. **Referenzfälle**, die W4 abdecken sollte (Inhalt, keine Sollwerte hier):
   1-DOF mit bekannter Dämpfung, auch mit $B < 2\Delta f$, um die Auflösungsgrenze zu zeigen;
   zwei eng liegende Moden; Sinus auf und zwischen Linien für Band-RMS mit Rechteck und Hann
   ($W_\mathrm{RBW}$); Rauschen am Eingang bzw. Ausgang für H1/H2/γ²; elliptische
   3D-Bewegung für den 3D-Betrag; Vorzeichen- und Konjugationstest (2.2) als Referenzfall.
3. **PSV-Übereinstimmung** braucht einen Export derselben Datei aus PSV (M4, W2 Abschnitt 6).
   Für Spektren, H1, H2 und γ² ist float32-Genauigkeit erreichbar (W2: ≤ 9,3·10⁻⁷). Für den
   Peak-Fit nicht, weil der Algorithmus unbekannt ist.
4. **Gültigkeitsgrenzen** in der Fachgrundlage ausdrücklich nennen: schwache Dämpfung,
   getrennte Moden, ausreichend Linien je Halbwertsbreite, abgeklungene Antwort im Fenster,
   Frequenzbereich unter der Decoder-Grenze (falls M7 das bestätigt).

---

## 6 Offene Fragen an Nutzer und Betreuer

**Ergebnisentscheidend für W4:**
1. **Referenzaufnehmer:** Typ, Einbauort und Richtung von Ref1 (Kraft) und Ref2
   (Beschleunigung), z. B. Impedanzkopf am Shaker? — *Auswirkung:* globales Vorzeichen aller
   H1-Phasen und Schwingformen (2.3).
2. **Fensterart, Generator, Burstlänge, Mittelungsart und -anzahl** der Messung (M5
   erweitern). — *Auswirkung:* Band-RMS-Korrektur $W_\mathrm{RBW}$, Bewertung der Leckage,
   Unsicherheitsangaben.
3. **Golden File:** ASCII- oder UFF-Export derselben Messung mit Geschwindigkeit, H1 und
   Kohärenz sowie Ablesen von Frequenzachse und Phase (M1, M2, M4). — *Auswirkung:* ohne ihn
   ist „stimmt mit PSV überein“ nicht prüfbar.
4. **Toleranz** für „stimmt mit PSV überein“ bei Spitzenfrequenz und Dämpfung, da der
   PSV-Fit nicht nachbaubar ist. — *Auswirkung:* Akzeptanzkriterium R-053.
5. **Welches Spektrum** meint R-050: |CPH| wie die PSV-Anzeige oder √AP, und welches
   Punktmittel (nur Betragsmittel wie PSV oder zusätzlich quadratisch)? — *Auswirkung:*
   Werte unterscheiden sich um den Faktor γ bzw. bis 28 %.

**Nicht blockierend:**
6. Bedeutung von „Bandbreitenbereich 1 kHz“ (M7) und Datenblatt PSV-QTec-3D. — *Annahme:*
   Auswertung oberhalb 1 kHz bis zur Klärung als „Gültigkeit offen“ kennzeichnen.
7. Werden Dämpfungswerte für diese Platte überhaupt gebraucht, oder genügen
   Spitzenfrequenzen? Falls ja: Ist eine feinere Auflösung bei künftigen Messungen möglich?
   — *Annahme:* Dämpfung wird PSV-konform ausgegeben und bei Auflösungsgrenze gewarnt.
8. Ursache der niedrigen Kohärenz unter 150 Hz und der Drift über 40 min (Temperatur?).
   — *Annahme:* nur dokumentieren.
9. Schwingformen als Schnelle oder als Weg darstellen? — *Annahme:* Schnelle wie gemessen.

---

## 7 Grenzen und Unsicherheiten

- Alle Datenbefunde stammen aus **einer** Datei. Die Spitzenliste ist ein einfacher lokaler
  Maximumsucher (Prominenz relativ zu ±20 Linien), keine validierte Peak-Suche. Die
  ζ-Angaben sind Größenordnungen und keine Messergebnisse.
- Der Kausalitätstest belegt den Phasensinn der **Daten**. Wie PSV die Phase anzeigt, ist
  nicht geprüft (M1).
- Die Vorzeichenauffälligkeit der Referenzen (2.3) setzt voraus, dass Ref2 am
  Kraftangriffspunkt und in Kraftrichtung misst. Das ist aus dem Verhalten erschlossen, nicht
  dokumentiert.
- Literatur außer Polytec ist nicht gelesen (Prüfstand `metadaten`). Aussagen zu
  Zufallsfehlern, Kreisfit, LSCF und MAC sind daher als Recherche markiert und nicht belegt.
- Aussagen zum Aufwand sind grobe Einschätzungen.

---

## Anhang: Prüfskripte

Die Skripte lagen im Scratchpad
`/tmp/claude-0/-home-user/e6b61297-17fb-5003-91f8-95c4534d012c/scratchpad/w3/`
(`w3_daten.py` bis `w3_daten4.py`; das Scratchpad ist flüchtig). Aufruf aus `software/`
mit `uv run --group werkzeuge python <skript>`. Kern der Prüfungen:

```python
import sys, numpy as np
sys.path.insert(0, "/home/user/BA_Jakob-Busch_P/software/tools/svd_analyse")
from svd_lesen import lese_svd
m = lese_svd("/home/user/BA_Jakob-Busch_P/Input/20261012_ref_Mitte.svd")
f = m.frequenz_hz; S = {k: v.werte for k, v in m.signale.items()}; w = 2*np.pi*f

# Passivitaet Ref2/Ref1 (2.3): Y = (A/F)/(i w), Re(Y) >= 0 am Antriebspunkt erwartet
HAF = S["M6"]/S["M12"]; coh = np.abs(S["M6"])**2/(S["M12"]*S["M13"])
Y = HAF.mean(0)/(1j*w); g = coh.mean(0) > 0.95
print(np.mean(Y.real[g] > 0))            # Ergebnis: 0.0 bei 1590 Linien

# Phasensinn an Resonanzen (2.2): zentrale Differenz der entfalteten Phase an lokalen Maxima
def slope(H, k):
    ph = np.unwrap(np.angle(H[k-2:k+3])); return ph[3]-ph[1]
H1z = S["M4"]/S["M12"]                   # Vib Z / Ref1
# lokale Maxima von |H1z[i]| mit Faktor 2 ueber dem kleineren Minimum in +-20 Linien,
# nur Linien mit gamma^2 > 0.9: Anteil slope > 0 = 0.018 (17391 Spitzen)

# CPH gegen CP/sqrt(AP_Ref) (2.1)
r = np.abs(S["M5"])/(np.abs(S["M4"])/np.sqrt(S["M12"]))
print(np.quantile(r, [0.01, 0.5, 0.99]))  # [0.9943 1.0 1.0007]

# Punktmittel-Varianten an Spitzen (B-9)
cm = np.abs(H1z.mean(0)); am = np.abs(H1z).mean(0); qm = np.sqrt((np.abs(H1z)**2).mean(0))
# cm/am an Spitzen 0.19 ... 1.00; qm/am 1.02 ... 1.28
```

Weitere Ausgaben: γ² nach Bändern, −3-dB-Breiten im Punktmittel (lineare Interpolation der
Schnittpunkte), Streuung der Referenzen über die Punkte und Frequenzdrift über die
Zeitstempel (`zeit_a`) der Punkte. Zahlenwerte stehen in den Abschnitten 1 und 2.
