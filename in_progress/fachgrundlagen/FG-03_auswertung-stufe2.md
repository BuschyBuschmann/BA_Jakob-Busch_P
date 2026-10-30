<!-- Fachgrundlage FG-03: Auswertung Stufe 2 (B-1 parametrische Dämpfungsschätzung, B-5 Vergleich mehrerer Messungen, B-8 3D-Komponentenbezug). Erstellt im Paket W4-2 von strukturdynamik-experte, Stand 2026-10-30. Status: FACHGRUNDLAGE ZUR FREIGABE. -->

> **Status:** Vom Nutzer am 2026-10-30 freigegeben, einschließlich der Entscheidungen E1–E6 wie empfohlen (Abschnitt 8). Annahmen M12–M15 und die Wiederholungsmessung für B-5 werden am Messrechner (Mo 2026-11-02) geprüft bzw. aufgenommen. Korrektur K2-1 (Option A) bis K2-4 am 2026-10-30 freigegeben und eingearbeitet (Fachabnahme FA-W5-2; Abschnitte 3.2, 4.2, 4.5, 6.2, 6.3, 7, 9.1, 9.2).

# FG-03 – Auswertung von PSV-Messdaten, Stufe 2

> **Status:** Entwurf zur Freigabe (Paket W4-2, 2026-10-30). Baut auf FG-02 in der Fassung
> mit K1 (Commit e9c7700) und auf der Umsetzung W5-1 (Commit 9e6303f) auf. Entscheidungen
> für den Nutzer stehen in Abschnitt 8.

## 1 Zweck und Umfang

| Punkt | Inhalt | Abschnitt |
|---|---|---|
| B-1 | Parametrische Schätzung von Eigenfrequenz und Dämpfungsgrad aus der komplexen H1 (Moden-Fit), auch für eng liegende Moden | 3 |
| B-5 | Vergleich mehrerer Messungen: Punktzuordnung, Spitzenpaarung, FRF-Vergleich, MAC, Drift innerhalb einer Messung | 4 |
| B-8 | 3D-Komponentenbezug: Normalen je Element und Punkt, Normal- und Tangentialanteil, Bahnellipse | 5 |

**Grundsatz:** Stufe 2 liest die Ergebnisse von Stufe 1 (FG-02, Abschnitt 6.2) und ändert
sie nicht. Alle Ausgaben von Stufe 2 sind zusätzliche Größen mit eigenen Namen.

**Nicht enthalten:**
- Vollständige Modalanalyse (R-054): kein Stabilisierungsdiagramm, keine Modellordnungswahl,
  kein globaler Fit mit gemeinsamen Polen über alle Punkte, keine Modalmassen-Normierung.
- Kreisfit (siehe 8, E1).
- Flächengewichtete Punktmittel.

**Kennzeichnung der Belege:** wie FG-02.
- **[H]**: Herstellerangabe Polytec.
- **[D]**: an `Input/20261012_ref_Mitte.svd` geprüft.
- **[A]**: eigene Herleitung.
- **[N]**: numerisch nachgerechnet (Prüfskripte im Anhang).
- **[L-m]**: Literatur nur mit Prüfstand `metadaten`, Inhalt nicht gelesen.
- **[ANN]**: einstellbare Annahme.

---

## 2 Konventionen (Ergänzung zu FG-02 Abschnitt 2)

Es gelten alle Konventionen von FG-02: Zeitabhängigkeit $e^{+i\omega t}$, Spektren einseitig
mit Spitzenwert, $\mathrm{CP}_{ab} = \langle A\,B^{*}\rangle$, Vorzeichen je Kanal $s_a s_b$,
Frequenzachse aus der Datei, Indizes 0-basiert, SI-Einheiten. Hinzu kommen:

- **Modellform der FRF (B-1).** Für eine Mobilität $Y$ in (m/s)/N gilt nahe den Resonanzen
  im Fitband
  $$\hat Y(\omega) = \sum_{r=1}^{n}\frac{i\omega\,R_r}{\omega_r^2-\omega^2+2i\zeta_r\omega_r\omega} + C .$$
  - $\omega_r = 2\pi f_r$ in rad/s, $\zeta_r$ dimensionslos.
  - $R_r$ ist die komplexe Modalkonstante in kg⁻¹. Für die Mobilität des Einmassenschwingers
    gilt $R = 1/m$.
  - $C$ ist ein komplexes, konstantes Residuum in (m/s)/N. Es nimmt den Einfluss der Moden
    außerhalb des Bands auf.
- **Gültigkeit der Modellform.** Die Pole $f_r$ und $\zeta_r$ hängen nicht von $s_a s_b$ ab.
  $R_r$ und $C$ wechseln mit $s_a s_b$ das Vorzeichen. Eine fälschlich konjugierte FRF passt
  nicht zur Modellform; ρ wird dann groß (siehe 3.4).
- **Andere FRF-Arten.** Akzeleranz (z. B. Ref2/Ref1) wird vor dem Fit nach FG-02 3.7 in
  Mobilität umgerechnet ($Y = H/(i\omega)$). Für Vib/Ref2 (Einheit s) gilt die Modellform nur
  als lokale Näherung; Kennzeichen `kein_mobilitaetsbezug`.
- **Geometrie (B-8).**
  - Koordinaten in m im Koordinatensystem des 3D-Abgleichs.
  - Elemente sind Tupel 0-basierter Punktindizes (Dreiecke oder Vierecke) **[ANN M14]**.
  - Die 3D-Komponenten X/Y/Z liegen im selben Koordinatensystem wie die Koordinaten
    **[ANN M12]**. Indiz [D]: In der Beispieldatei liegt der Median des Anteils der
    Normalenbewegung zwischen 150 und 500 Hz bei 0,995 (Abschnitt 7).
- **Zeit (B-5, Drift).** Zeit je Punkt aus dem Zeitstempel des Datensatzes (W2: naive
  FILETIME, Zeitzone offen). Verwendet werden nur Differenzen in s, die Zeitzone spielt dafür
  keine Rolle.

---

## 3 B-1: Parametrische Dämpfungsschätzung

### 3.1 Begründung der Verfahrenswahl

Befunde aus W3, FG-02 und dieser Prüfung:

1. Die −3-dB-Breite (FG-02 3.9) ist bei $B/\Delta f < 3$ stark verzerrt (bis +178 %). In der
   Beispieldatei tragen 67 von 114 Spitzen das Kennzeichen `aufloesungsbegrenzt` (W5-1).
2. Ein komplexer Fit nutzt Betrag **und** Phase aller Linien im Fitband. Ist die Modellform
   exakt, liefert er ζ auch bei $B/\Delta f = 0{,}64$ exakt (RF-F1 [N]). Die Information steckt
   im Verhältnis von Spitzenwert zu Flanken und im Phasenverlauf, nicht in der Breite allein.
3. Bei Impulsanregung bleiben die Pole trotz abgeschnittener Antwort exakt [A, N] (RF-F4).
   Herleitung: Auf den Linien $\omega_k = 2\pi k/T$ gilt für einen Pol $p$ mit
   $a = e^{p\Delta t}$
   $$\sum_{n=0}^{N-1} a^n e^{-i\omega_k n\Delta t} = \frac{1 - a^N e^{-i2\pi k}}{1 - a\,e^{-i\omega_k\Delta t}} = \frac{1 - e^{pT}}{1 - a\,e^{-i\omega_k\Delta t}} .$$
   Die Abschneidung wirkt nur als konstanter Faktor $1 - e^{pT}$ auf die Modalkonstante.
4. Bei Burst-Anregung wird der Abschneideterm durch das Kraftspektrum $X_k$ geteilt. Die
   Polform gilt dann nur näherungsweise. Im Burst-Chirp-Fall (RF-F5 [N]) bleibt der Fit
   trotzdem auf ≤ 2,4 % genau, die Halbwertsbreite liegt bis +32 % daneben. Die Abweichung
   zeigt sich im Residuum ρ.
5. Für eng liegende Moden ist ein gemeinsamer Fit mehrerer Moden nötig.
   - RF-F3 [N]: Bei 2 % Frequenzabstand liegt ein Ein-Moden-Fit um +106 % daneben, der
     Zwei-Moden-Fit ist exakt.
   - Datei [D] (Gruppe um 262,5 Hz): ρ sinkt von 0,22 bei einer Mode auf 0,015 bei drei Moden.

**Gewähltes Verfahren** (Empfehlung, Entscheidung E1): komplexer Moden-Fit nach 2 mit
Variablenprojektion. Für isolierte Spitzen gilt n = 1, für Gruppen von Spitzen aus Stufe 1
n = Gruppengröße. Kreisfit und LSCF siehe Abschnitt 8.

### 3.2 Schätzer

Gegeben ist die komplexe H1 (Stufe 1, nach $s_a s_b$ und Konjugation) eines Punkts auf den
Fitlinien $k \in \mathcal K$ mit Kohärenzmaske $\gamma^2_k \ge \gamma^2_\mathrm{min}$ (FG-02 3.5).
Linien unter der Schwelle fallen aus dem Fit heraus.

**Linien mit γ² = NaN (K2-4).** γ² = NaN bedeutet „nicht prüfbar“ (z. B. $n_d = 1$, FG-02 3.3),
nicht „zu klein“. Solche Linien bleiben im Fit, sofern H endlich ist. Ist γ² im Fitband an
mindestens einer Linie NaN, erhält das Ergebnis den Hinweis „Kohärenz nicht prüfbar“; ein
Kennzeichen entsteht daraus nicht. Nur Linien mit endlichem $\gamma^2_k < \gamma^2_\mathrm{min}$
werden entfernt.

1. **Lineare Teilaufgabe.** Für feste nichtlineare Parameter $\theta = (f_r, \ln\zeta_r)_{r=1..n}$
   sind $R_r$ und $C$ linear. Sie folgen aus dem komplexen Kleinste-Quadrate-Problem
   $\min\lVert H - \Phi(\theta)\,c\rVert_2$. Dabei ist $\Phi$ die Matrix der Basisfunktionen
   (je Mode eine Spalte nach 2, eine Spalte 1 für $C$).
2. **Nichtlineare Teilaufgabe.** Minimiert wird die Residuenquadratsumme
   $S(\theta) = \lVert H - \Phi(\theta)\,c^\ast(\theta)\rVert_2^2$ über θ mit
   Levenberg-Marquardt. Die Jacobi-Matrix wird über Real- und Imaginärteil gestapelt, mit
   finiten Differenzen; Abbruch bei relativer Änderung von S < 10⁻¹².
   - **Abbruchkriterium (K2-2):** Der Fit gilt als konvergiert, sobald ein Versuchsschritt S
     relativ um höchstens 10⁻¹² ändert, gleich ob der Schritt angenommen oder verworfen
     wird: $\lvert S(\theta + \delta) - S(\theta)\rvert \le 10^{-12}\,S(\theta)$. Ein verworfener
     Schritt mit so kleiner Änderung zeigt, dass der Gradient auf Rundungsniveau liegt
     (S stationär im Rahmen der Differenzen-Jacobi-Matrix). Ohne diese Lesart enden exakte
     Daten (RF-F1, RF-F4) über λ > 10¹² und würden fälschlich `nicht_konvergiert`.
     `nicht_konvergiert` bleibt für: 200 Schritte ohne Abbruch, λ > 10¹² oder singuläre
     Normalgleichung (3.4).
   - Der Ansatz über ln ζ hält ζ > 0.
   - Startwerte: $f_r^{(0)} = f_\mathrm{sp}$ aus Stufe 1; $\zeta_r^{(0)} = \zeta$ aus Stufe 1,
     falls endlich, sonst $\Delta f/(2f_\mathrm{sp})$.
3. **Ausgaben je Mode:**
   - $f_r$ in Hz und $\zeta_r$.
   - $B_\mathrm{fit} = 2\zeta_r f_r$ in Hz, vergleichbar mit FG-02.
   - $R_r$ in kg⁻¹ (für Mobilität) und $C$.
   - Standardabweichungen aus der Gauss-Newton-Kovarianz
     $\mathrm{Cov}(\theta) = s^2 (J^\mathsf{T}J)^{-1}$ mit $s^2 = S/(2\lvert\mathcal K\rvert - p)$ und
     $p = 4n + 2$ reellen Parametern. Daraus folgen $\sigma_{f_r}$ in Hz und
     $\sigma_{\zeta}/\zeta = \sigma_{\ln\zeta}$.
4. **Gütemaß:** $\rho = \lVert H - \hat H\rVert_2/\lVert H\rVert_2$ über $\mathcal K$.

**Gewichtung** (Entscheidung E3): ungewichtet über die maskierten Linien (Empfehlung).
Option: Gewichte $1/(\lvert H_{1,k}\rvert\,\varepsilon_k)^2$ aus FG-02 3.4.

### 3.3 Fitband und Gruppenbildung

- **Einzelspitze:** Linien $k^\ast - n_\mathrm{fit} \dots k^\ast + n_\mathrm{fit}$ um die
  Spitzenlinie aus Stufe 1. Vorschlag $n_\mathrm{fit} = 6$ (13 Linien).
  - Das Band wird am nächsten lokalen Minimum von $\lvert H_1\rvert$ beidseitig gekürzt, wenn
    dahinter eine andere Spitze aus Stufe 1 liegt.
- **Gruppe:** Spitzen aus Stufe 1 gehören zu einer Gruppe, wenn
  $\lvert f_{\mathrm{sp},i} - f_{\mathrm{sp},j}\rvert < 3B$ gilt (Kennzeichen `nachbarmode`)
  oder wenn eine Spitze `ueberlappend` trägt und die andere innerhalb $n_\mathrm{fit}\,\Delta f$
  liegt. Die Gruppe wird transitiv gebildet.
  - Fitband: von der ersten Spitze $-n_\mathrm{fit}$ bis zur letzten $+n_\mathrm{fit}$ Linien.
  - Modenzahl n = Zahl der Spitzen der Gruppe; Vorschlag $n_\mathrm{max} = 4$. Größere
    Gruppen bekommen das Kennzeichen `gruppe_zu_gross` und werden nicht gefittet.
- **Mindestzahl Linien:** $\lvert\mathcal K\rvert \ge 4n + 3$ nach der Kohärenzmaske, sonst
  `zu_wenig_linien` ohne Fit. Der Grund ist $p = 4n + 2$ reelle Parameter.
- **Grenze:** Moden, die Stufe 1 nicht als getrennte Spitzen findet (Abstand ≲ B, FG-02
  RF-M1), erkennt auch Stufe 2 nicht. ρ zeigt einen solchen Fall nur an, wenn das Modell
  merklich abweicht.

### 3.4 Kennzeichen und Schwellen (Vorschläge, einstellbar)

| Kennzeichen | Bedingung | Begründung |
|---|---|---|
| `modell_passt_nicht` | ρ > ρ_max, **Vorschlag ρ_max = 0,10** | Synthetisch: ρ ≤ 0,04 bei ≤ 2,4 % Fehler von ζ (RF-F5); erzwungener Ein-Moden-Fit an zwei Moden: ρ = 0,096 bis 0,112 bei Fehlern −12 % bis +106 % (RF-F3). Datei: isolierte Spitzen ρ = 0,05 bis 0,08, unaufgelöste Gruppe 0,22 [D] |
| `unsicher` | $\sigma_\zeta/\zeta > 0{,}2$ oder $\sigma_{f_r} > \Delta f/2$ | Die Unsicherheit der Schätzung übersteigt die Aussage |
| `nicht_konvergiert` | Levenberg-Marquardt ohne Abbruch nach 200 Schritten, λ > 10¹² oder singuläre Normalgleichung | Beispiel: konjugierte Daten treiben ζ gegen 0 (RF-F6) |
| `ausserhalb_band` | $f_r$ außerhalb des Fitbands, oder ζ ≥ 0,2, oder ζ < 10⁻⁵ | Schwache Dämpfung ist Voraussetzung der lokalen Modellform |
| `kein_mobilitaetsbezug` | FRF ist weder Mobilität noch Akzeleranz | 2 |
| `gueltigkeit_offen_m7` | $f_r > 1000$ Hz, solange M7 offen | FG-02 3.9 |

Ergebnisse mit `modell_passt_nicht`, `nicht_konvergiert` oder `ausserhalb_band` werden
ausgegeben, aber nicht in die Zusammenfassung nach 3.5 übernommen.

### 3.5 Ort des Fits und Zusammenfassung (Entscheidung E2)

Empfehlung: Fit **je Punkt** auf H1 des Paars. Zusammengefasst werden die $n_\mathrm{P}$
Punkte mit dem größten $\lvert H_1\rvert$ an der Spitzenlinie, Vorschlag $n_\mathrm{P} = 20$.
Daraus ohne gekennzeichnete Ergebnisse:
- Median und Interquartilsabstand (IQR) von $f_r$ und $\zeta$,
- Anzahl der verwendeten Punkte.

Begründung: Der Pol ist eine Eigenschaft der Struktur. Die Streuung über die Punkte zeigt,
wie zuverlässig der Wert ist. In der Datei liegt der IQR von ζ bei 401 Hz unter 2 % des
Medians [D]. Das Punktmittel von |H1| eignet sich nicht, weil es keine Phase hat.
Alternativ ist der Fit an einem konfigurierten Antriebspunkt-Paar (z. B. Ref2/Ref1) möglich.

### 3.6 Gültigkeitsgrenzen

- Linearität, schwache Dämpfung (ζ < 0,2), Fitband mit nur den Moden der Gruppe und einem
  konstanten Residuum.
- **Auflösung:** Ohne Rauschen und Leckage ist der Fit für $B/\Delta f \ge 0{,}64$ exakt
  (RF-F1). Mit Rauschen wächst die Unsicherheit. Bei 1 % Rauschen bezogen auf den Spitzenwert
  und $B/\Delta f = 0{,}64$ beträgt sie $\sigma_\zeta/\zeta$ = 1,35 %, bei 3 % Rauschen 4,2 %
  (RF-F2). Die vom Fit gemeldete Standardabweichung stimmt mit der Monte-Carlo-Streuung auf
  ±6 % überein.
- **Leckage:**
  - Impulsanregung: Pole unverfälscht (RF-F4).
  - Burst-Chirp mit Rechteckfenster: ζ-Fehler ≤ 2,4 % bis zu einem Rest von 0,67 der
    Hüllkurve am Blockende (RF-F5).
  - Bei Hann-Fenster auf transienten Daten ist die Modellform nicht geprüft (M5).
- **Vorzeichen und Konjugation:** ohne Einfluss auf $f_r$ und ζ. Sind die Daten konjugiert,
  passt die Modellform nicht; P-07 aus Stufe 1 erkennt das vorher.
- **Frequenzachse:** Ein Linienversatz (M2) verschiebt $f_r$ um $\Delta f$.

---

## 4 B-5: Vergleich mehrerer Messungen

Eingang: zwei Auswertungen nach Stufe 1, **A** (Bezug) und **B** (Vergleich), mit gleichem
Kanalpaar. Für den FRF-Vergleich müssen beide Frequenzachsen gleich sein: gleiche Linien,
$\lvert f_k^A - f_k^B\rvert \le 10^{-6}\Delta f$ (wie P-06). Andernfalls werden nur Spitzen
verglichen (Hinweis „Achsen verschieden“). Eine Interpolation zwischen Linien gibt es nicht.

### 4.1 Punktzuordnung (Entscheidung E4)

- **Variante `label` (Voreinstellung):** Punkte mit gleichem Label werden einander
  zugeordnet. Punkte ohne Partner werden aufgelistet.
- **Variante `koordinaten`:** für Messungen mit anders gelegtem Raster oder anderem Abgleich.
  1. Optional eine starre Transformation $x_B = R\,x_A + t$ aus mindestens drei nicht
     kollinearen Passpunkten (Paare von Labels oder Indizes, vom Nutzer angegeben).
     - Schätzung nach dem SVD-Verfahren von Kabsch [A]: $H = \sum (x_A - \bar x_A)(x_B - \bar x_B)^\mathsf{T} = U\Sigma V^\mathsf{T}$,
       $R = V\,\mathrm{diag}(1, 1, \det(VU^\mathsf{T}))\,U^\mathsf{T}$, $t = \bar x_B - R\bar x_A$.
     - Kennwert: RMS-Restabstand der Passpunkte in m.
  2. Zuordnung über den **gegenseitig** nächsten Nachbarn nach der Transformation, mit
     Toleranz $d_\mathrm{tol} = 0{,}5\,d_\mathrm{min}$. $d_\mathrm{min}$ ist der kleinste
     Punktabstand in A. Punkte ohne gegenseitigen Partner innerhalb $d_\mathrm{tol}$ bleiben
     unzugeordnet.
  3. **Komponenten mitdrehen:** Eine 3D-Größe aus B wird vor jedem Vergleich in das System A
     gedreht: $v_{B\to A} = R^\mathsf{T} v_B$ [A]. Ohne diese Drehung sinkt der MAC
     identischer Schwingformen bei 10° Drehung von 1 auf 0,9965 (RF-V2).
- Kennzeichen `passpunkte_ungenau`, wenn der RMS-Restabstand der Passpunkte größer als
  $d_\mathrm{tol}/2$ ist.

### 4.2 Spitzenpaarung

- Spitzen aus Stufe 1, falls vorhanden mit B-1-Ergebnis, werden gegenseitig-nächste Paare,
  wenn $\lvert f^B - f^A\rvert \le \Delta f_\mathrm{tol}$. **Vorschlag $\Delta f_\mathrm{tol} = 2\,\Delta f$**,
  einstellbar.
- Ausgabe je Paar: $\Delta f = f^B - f^A$ in Hz und $\Delta f/f^A$. Ist B-1 vorhanden, auch
  $\Delta\zeta$ sowie das Kennzeichen `signifikant`, wenn
  $\lvert\Delta f\rvert > 2\sqrt{\sigma_A^2 + \sigma_B^2}$ (Fit-Standardabweichungen nach 3.2).
  Ohne B-1 dient als Unsicherheit die Diskretisierungsgrenze 0,0508 Δf aus FG-02 3.9.
- **Festlegung (K2-3):** $f^A$, $f^B$ sind mit B-1 der Median von $f_r$ der Zusammenfassung
  (3.5); $\sigma_A$, $\sigma_B$ sind der **Median der Fit-Standardabweichungen**
  $\sigma_{f_r}$ der dort verwendeten Punkte. Sie werden nicht durch $\sqrt{N}$ geteilt: Die
  Fit-Standardabweichung enthält Modellfehler, die allen Punkten gemeinsam sind (Abschnitt 7:
  sie ist größer als die Streuung um die Driftgerade). Ein Maß aus der Streuung über die Punkte
  (z. B. IQR 0,007 Hz bei 401 Hz) würde fast jede Verschiebung als `signifikant` melden.
  Das Maß ist damit konservativ gegenüber Zufallsfehlern.
- **Hinweis zur Deutung:** Die Drift innerhalb einer Messung (4.5; in der Beispieldatei bis
  −0,32 Hz bei 1508 Hz in 40 min) hat dieselbe Größenordnung wie σ. Ein `signifikant` zwischen
  zwei Messungen kann daher auch von Temperatur oder Zeit herrühren, nicht nur von einer
  Strukturänderung.
- Spitzen ohne Partner werden aufgelistet.

### 4.3 FRF-Vergleich je Punkt und Band

Über die Linien eines Bands $[f_u, f_o]$ (Bandregel FG-02 3.8), nur Linien mit
$\gamma^2 \ge \gamma^2_\mathrm{min}$ in **beiden** Messungen [A]:

| Größe | Formel | Einheit | Bedeutung |
|---|---|---|---|
| `frac` | $\dfrac{\lvert\sum_k H_k^{A*} H_k^B\rvert^2}{\sum_k\lvert H_k^A\rvert^2\,\sum_k\lvert H_k^B\rvert^2}$ | 1 | Formgleichheit der FRF im Band (1 = gleich bis auf einen komplexen Faktor) |
| `pegel_db` | $10\log_{10}\dfrac{\sum_k\lvert H_k^B\rvert^2}{\sum_k\lvert H_k^A\rvert^2}$ | dB | Pegelunterschied |
| `diff_rel` | $\lVert H^B - H^A\rVert_2/\lVert H^A\rVert_2$ | 1 | Gesamtabweichung |

`frac` ist analog zum MAC gebildet. In der Literatur heißt eine solche Größe „FRAC“; diese
Quelle ist nicht beschafft (Rechercheauftrag). Weniger als 3 gemeinsame Linien → NaN mit
Hinweis.

### 4.4 MAC der Schwingformen

$$\mathrm{MAC}(\phi_A, \phi_B) = \frac{\lvert\phi_A^\mathsf{H}\phi_B\rvert^2}{(\phi_A^\mathsf{H}\phi_A)(\phi_B^\mathsf{H}\phi_B)} \in [0, 1] .$$

- $\phi$ ist der gestapelte komplexe Vektor über alle **zugeordneten** Punkte. Bei 3D liegen
  die Komponenten X, Y, Z je Punkt hintereinander (Länge 3·P). Die Werte stammen aus
  `amplitude` der Schwingform (FG-02 3.6); B ist vorher nach 4.1 gedreht.
- Linie je Messung: die Spitzenlinie des jeweiligen Spitzenpaars (4.2). Es zählt nicht
  dieselbe Frequenz, weil sich die Spitze verschieben kann.
- Eigenschaften [A]: Der MAC hängt nicht von einem komplexen Faktor ab; er ist 1 für gleiche
  Form und 0 für orthogonale Vektoren.
- Ohne gültige Phase ist der MAC nicht definiert (Hinweis).
- **Auto-MAC** innerhalb einer Messung: Matrix über die Spitzen. Sie zeigt, ob zwei Spitzen
  dieselbe Form haben.
- Interpretation: Polytec nennt im MAC-Beispiel „< 0,9 verschieden, > 0,9 ähnlich“
  (SM 9-38 über W1 [H]). Eine Schwelle wird hier nicht festgelegt, nur ausgegeben.
  Literatur: Allemang [L-m].

### 4.5 Drift innerhalb einer Messung

- **Datengrundlage (Vorschlag):** ein Paar, dessen FRF an jedem Punkt dasselbe misst. Das
  ist das konfigurierte Antriebspunkt-Paar (z. B. Ref2/Ref1). Ist keins konfiguriert, wird
  H1 an den Punkten verwendet, an denen $\lvert H_1\rvert \ge 0{,}3\cdot\max$ an der
  Spitzenlinie ist.
- Je Punkt p liefert der Fit nach 3.2 für eine ausgewählte Spitze $f_{r,p}$. Gefittet wird
  die Gruppe der Spitze nach 3.3 (Gruppenfit mit allen Moden der Gruppe); verwendet wird nur
  $f_r$ der gewählten Mode. Dazu kommt die Zeit $t_p$ in s relativ zum ersten Punkt.
- Lineare Regression $f_{r,p} = b_0 + b_1 t_p$. Ausgabe:
  - $b_1$ in Hz/h,
  - Gesamtdrift $b_1(t_\mathrm{max} - t_\mathrm{min})$ in Hz und relativ zu $b_0$,
  - Standardfehler $\sigma_{b_1}$ **aus der Streuung um die Gerade** (nicht aus den
    Fit-Standardabweichungen, siehe 7),
  - Kennzeichen `drift_signifikant`, wenn $\lvert b_1\rvert > 3\sigma_{b_1}$.
- **Punktausschluss (K2-1, Option A).** Ausgeschlossen wird nach den Kennzeichen **der
  gewählten Mode** an diesem Punkt:
  - `ausserhalb_band` und `unsicher` (beide je Mode nach 3.4),
  - `nicht_konvergiert` nur bei n = 1. Im Gruppenfit (n ≥ 2) gilt das Kennzeichen für alle
    Moden gemeinsam und stammt oft von einer schwach ausgeprägten Partnermode; über die
    gewählte Mode entscheiden dann `ausserhalb_band` und `unsicher`,
  - Punkte ohne Fit (`zu_wenig_linien`, `gruppe_zu_gross`, ‖H‖ = 0).

  **Nicht** ausgeschlossen werden `modell_passt_nicht`, `gueltigkeit_offen_m7`,
  `kohaerenz_niedrig` und `kein_mobilitaetsbezug`. Die Anzahl der verwendeten Punkte mit
  `modell_passt_nicht` wird ausgegeben.
- Mindestens 10 verwendete Punkte, sonst „nicht prüfbar“.
- **Begründung [D, N].** ρ hängt mit der Zeit zusammen, weil der Pol durch die Drift gegen das
  feste Linienraster wandert (Korrelation ρ–t in der Beispieldatei −0,42 bei 419 Hz, +0,94 bei
  1508 Hz). Eine Auswahl nach ρ wählt also nach einer Größe aus, die mit dem Regressor
  zusammenhängt, und verzerrt $b_1$: Bei 419 Hz liegt ρ fast überall zwischen 0,099 und 0,102
  (10- bis 90-%-Quantil); die Teilmengen ρ ≤ 0,10 und ρ > 0,10 ergeben −0,097 bzw.
  −0,138 Hz/h, alle Punkte −0,129 Hz/h. Bei 631,7 Hz trägt die Gruppe mit 640,6 Hz an
  95 von 135 Punkten `nicht_konvergiert`, weil die in Ref2/Ref1 kaum vorhandene Partnermode
  wegläuft (ζ bis 8·10³); die Streuung von $f_r$ der gewählten Mode ist in beiden Teilmengen
  gleich (0,024 Hz). Prüfskripte `drift_var.py`, `drift_631.py` und `drift_k2.py` im Anhang.

---

## 5 B-8: 3D-Komponentenbezug

### 5.1 Normalen

- **Element** mit Knoten $p_0 \dots p_3$ (Viereck):
  $\tilde n_e = (p_2 - p_0)\times(p_3 - p_1)$ (Kreuzprodukt der Diagonalen). Fläche
  $A_e = \tfrac12\lVert\tilde n_e\rVert$.
  - Für ebene Vierecke ist das exakt. Für verwundene Vierecke ist es eine mittlere Normale
    (RF-G2).
  - Dreieck: $\tilde n_e = (p_1 - p_0)\times(p_2 - p_0)$.
  - $n_e = \tilde n_e/\lVert\tilde n_e\rVert$.
- **Orientierung:** Die Knotenreihenfolge legt das Vorzeichen fest. Alle Normalen werden auf
  einen Bezugsvektor $e_\mathrm{ref}$ ausgerichtet: $n_e \leftarrow n_e\,\mathrm{sign}(n_e\cdot e_\mathrm{ref})$.
  - Voreinstellung $e_\mathrm{ref} = (0, 0, 1)$ **[ANN M13]**, Entscheidung E5.
  - Kennzeichen `orientierung_unsicher` bei $\lvert n_e\cdot e_\mathrm{ref}\rvert < 0{,}1$.
- **Punkt:** flächengewichtetes Mittel der ausgerichteten Normalen aller Elemente, die den
  Punkt enthalten: $n_p = \sum_e A_e n_e/\lVert\sum_e A_e n_e\rVert$. Punkte ohne Element
  bekommen NaN und einen Hinweis.
- Gültigkeit: An gekrümmten Flächen ist $n_p$ an Innenpunkten eines gleichmäßigen Rasters
  exakt, am Rand um den halben Winkelschritt geneigt (RF-G3).

### 5.2 Normal- und Tangentialanteil

Für eine komplexe Amplitude $\hat v$ (3-Vektor, z. B. `amplitude` der Schwingform oder je
Linie CPH bzw. H1) und die reelle Einheitsnormale $n$ [A]:

$$\hat v_n = n\cdot\hat v\ \ [\text{Einheit von }\hat v],\qquad \hat v_t = \hat v - n\,\hat v_n,\qquad n\cdot\hat v_t = 0 .$$

Ausgaben:
- $\hat v_n$ (komplex) und $\lvert\hat v_n\rvert$.
- $\hat v_t$ (komplexer 3-Vektor) und $\lvert\hat v_t\rvert_\mathrm{psv} = \sqrt{\sum_i\lvert\hat v_{t,i}\rvert^2}$.
- Anteil der Normalenbewegung $\eta = \lvert\hat v_n\rvert^2/\sum_i\lvert\hat v_i\rvert^2$.

Die Zerlegung ist vorzeichengetreu für $\hat v_n$ bezogen auf $n$. Wird die Orientierung
umgekehrt, wechselt $\hat v_n$ das Vorzeichen, $\eta$ bleibt gleich.

### 5.3 Bahnellipse

Bahn: $x(\theta) = \mathrm{Re}\{\hat v\,e^{i\theta}\} = a\cos\theta - b\sin\theta$ mit
$a = \mathrm{Re}\,\hat v$, $b = \mathrm{Im}\,\hat v$ [A].
- **Halbachsen:** `auslenkung_max` und `auslenkung_min` wie FG-02 3.6.
- **Richtung der großen Halbachse:**
  $\theta^\ast = -\tfrac12\arg\big(\sum_i\hat v_i^2\big)$ und
  $e_\mathrm{max} = \mathrm{Re}\{\hat v\,e^{i\theta^\ast}\}/\lVert\cdot\rVert$.
  - Das Vorzeichen ist frei; festgelegt wird $e_\mathrm{max}\cdot e_\mathrm{ref} \ge 0$, bei 0
    die erste von null verschiedene Komponente positiv.
  - Kleine Halbachse: $\theta^\ast + \pi/2$.
  - Bei Kreisbahn ($\lvert\sum\hat v_i^2\rvert < 10^{-12}\sum_i\lvert\hat v_i\rvert^2$) ist die Richtung unbestimmt: NaN mit Hinweis.
- **Ebene und Drehsinn:**
  - Normale der Bahnebene: $m = b\times a$, d. h. $\mathrm{Im}\,\hat v\times\mathrm{Re}\,\hat v$.
  - Drehsinn bezogen auf die Flächennormale: $\sigma = \mathrm{sign}(n\cdot m)$.
    +1 bedeutet mathematisch positiv um n.
  - Herleitung: $x \times \mathrm{d}x/\mathrm{d}\theta = a\times(-b) = b\times a$ bei θ = 0, und
    der Ausdruck ist konstant in θ.
  - Lineare Bahn mit $b_\mathrm{min}/a_\mathrm{max} < 10^{-6}$: σ = 0.

---

## 6 Datenvertrag (Ergänzung zu FG-02 Abschnitt 6)

### 6.1 Eingaben

| Name | Form | Typ | Einheit | Bedingung |
|---|---|---|---|---|
| Stufe-1-Auswertung A (und B) | – | `Auswertung` (W5-1) | – | unverändert gelesen |
| `elemente` | Liste von Tupeln mit 3 oder 4 Indizes | int | – | 0-basiert [ANN M14] |
| `zeit_s` | (P,) | float64 | s | relativ, aus den Zeitstempeln |
| Parameter B-1 | – | – | – | $n_\mathrm{fit}$ = 6; $n_\mathrm{max}$ = 4; ρ_max = 0,10; $\sigma_\zeta/\zeta$ max = 0,2; $n_\mathrm{P}$ = 20; Gewichtung `keine` |
| Parameter B-5 | – | – | – | Zuordnung `label`; Passpunkte (optional); $d_\mathrm{tol} = 0{,}5\,d_\mathrm{min}$; $\Delta f_\mathrm{tol} = 2\Delta f$; Driftpaar (optional) |
| Parameter B-8 | – | – | – | $e_\mathrm{ref}$ = (0, 0, 1) [ANN M13] |

### 6.2 Ausgaben

| Größe | Form / Typ | Einheit |
|---|---|---|
| B-1 je Punkt und Spitze bzw. Gruppe: `fr_hz`, `sd_fr_hz`, `zeta`, `sd_zeta_rel`, `breite_fit_hz`, `modalkonstante`, `residuum`, `rho`, `n_linien`, `n_moden`, Kennzeichen | Liste | Hz, Hz, 1, 1, Hz, kg⁻¹ (Mobilität), [H], 1 |
| B-1 Zusammenfassung je Spitze: Median und IQR von `fr_hz` und `zeta`, Anzahl Punkte | Liste | Hz, 1 |
| B-5 Zuordnung: Indexpaare, Abstände, $R$ (3×3), $t$ (3,), RMS Passpunkte, Listen ohne Partner | – | m |
| B-5 Spitzenpaare: $f^A$, $f^B$, Δf, Δf/f, Δζ, `signifikant` | Liste | Hz, 1 |
| B-5 FRF-Vergleich je Punkt und Band: `frac`, `pegel_db`, `diff_rel`, `n_linien` | (P_zug,) | 1, dB, 1 |
| B-5 MAC je Spitzenpaar; Auto-MAC | Skalar; Matrix | 1 |
| B-5 Drift: $b_1$ in Hz/h, Gesamtdrift in Hz und relativ, $\sigma_{b_1}$, `drift_signifikant`, Anzahl Punkte, davon mit `modell_passt_nicht` (K2-1) | je Spitze | Hz/h, Hz, 1 |
| B-8: `normale_element` (E, 3), `flaeche_element` (E,), `normale_punkt` (P, 3); je Schwingform `v_normal` (P,) complex, `v_tangential` (P, 3) complex, `anteil_normal` (P,), `achse_max` (P, 3), `drehsinn` (P,) | – | 1, m², 1, [v], [v], 1, 1, 1 |

### 6.3 Randfälle

| Fall | Verhalten |
|---|---|
| Fitband mit weniger als $4n + 3$ Linien nach Maske | kein Fit, `zu_wenig_linien` |
| γ² der Spitzenlinie unter der Schwelle | Fit mit den übrigen Linien; Kennzeichen `kohaerenz_niedrig` aus Stufe 1 wird übernommen |
| γ² = NaN im Fitband (z. B. $n_d = 1$) | Linien bleiben im Fit (K2-4); Hinweis „Kohärenz nicht prüfbar“, kein Kennzeichen |
| Gruppe größer als $n_\mathrm{max}$ | kein Fit, `gruppe_zu_gross` |
| $\lVert H\rVert = 0$ im Fitband | kein Fit, Hinweis |
| Achsen von A und B verschieden | nur Spitzenpaarung, Hinweis |
| weniger als 3 Passpunkte oder kollinear ($\sigma_2/\sigma_1 < 10^{-6}$ der Matrix $H$) | `ValueError` |
| keine zugeordneten Punkte | MAC, FRF-Vergleich NaN, Hinweis |
| MAC mit Nullvektor | NaN |
| weniger als 3 gemeinsame Linien im Band | `frac`, `pegel_db`, `diff_rel` NaN |
| Drift mit weniger als 10 brauchbaren Punkten (nach Ausschluss je Mode, 4.5) | nicht prüfbar |
| Drift: Gruppenfit mit `nicht_konvergiert` | Punkt bleibt, wenn die gewählte Mode weder `ausserhalb_band` noch `unsicher` trägt (K2-1) |
| entartetes Element (Fläche < 10⁻¹²·Median) | ignoriert, Hinweis |
| Punkt ohne Element | Normale NaN, Zerlegung NaN |
| Kreisbahn | `achse_max` NaN, Hinweis |

---

## 7 Befunde an der Beispieldatei [D]

Vorbehaltlich M1–M14; Prüfskripte `datei.py` und `gruppe.py` im Anhang.

**B-1:**

Festlegung für die Zusammenfassung (K2-3): Punktauswahl **je Spitze** (die 20 Punkte mit dem
größten $\lvert H_1\rvert$ an der Spitzenlinie dieser Spitze, 3.5), Fitband nach 3.3 mit
Kürzung am lokalen Minimum, ρ als **Median über die verwendeten Punkte** (ohne
`modell_passt_nicht`, `nicht_konvergiert`, `ausserhalb_band`). Die Werte stammen aus der
Umsetzung W5-2 und wurden in der Fachabnahme FA-W5-2 nachgerechnet.

| Spitze | Stufe 1 (Betragsmittel, W5-1) | B-1 je Punkt (20 stärkste je Spitze, Vib Z/Ref1) | ρ (Median der verwendeten Punkte) |
|---|---|---|---|
| ≈ 401,6 Hz | B = 1,429 Hz, ζ = 0,00178, `aufloesungsbegrenzt` | $f_r$ = 401,324 Hz (IQR 0,007), ζ = 0,00142 (IQR 0,00003), 20 Punkte | 0,054 |
| ≈ 618,9 Hz | B = 1,920 Hz, ζ = 0,00155, `aufloesungsbegrenzt` | $f_r$ = 619,015 Hz (IQR 0,015), ζ = 0,00146 (IQR 0,00004), 19 Punkte (1 × `modell_passt_nicht`) | 0,078 (über alle 20: 0,080) |
| ≈ 262,6 Hz (Gruppe 262,6/265,0/270,0) | B = 1,487 Hz, `aufloesungsbegrenzt`, `nachbarmode`; 265,0 Hz `ueberlappend` | 3 Moden, Fitband 254,69–279,69 Hz (17 Linien): $f_r$ = 262,720 / 266,154 / 270,267 Hz, ζ = 0,00214 / 0,00116 / 0,00190, je 20 Punkte | 0,007 / 0,012 / 0,008 |

- Vergleich mit dem ersten Prüfskript (`gruppe.py`, Erstfassung): Es nahm für alle drei Moden
  die 20 stärksten Punkte bei 262,5 Hz und kürzte das Band nicht (253,1–279,7 Hz, die Linie
  253,1 Hz liegt an der Nachbarspitze 253,2 Hz). Damit ergaben sich ζ₃ = 0,00187 und ρ = 0,015.
  Mit der Punktauswahl des Skripts liefert die Umsetzung 270,270 Hz und ζ₃ = 0,00188; der
  Unterschied in ρ kommt von der Bandkürzung nach 3.3.
- Erzwungener Ein-Moden-Fit an der Gruppe (nur zur Einordnung, Prüfskript): ζ = 0,00223,
  ρ = 0,224.

- Die Halbwertsbreite von Stufe 1 liegt an der Auflösungsgrenze 6 bis 25 % über dem Fit.
  Das entspricht der Tabelle in FG-02 3.9 (positiver Bias).
- Ref2/Ref1 als Mobilität, Fit am Punktmittel: ρ = 0,09 bis 0,16 bei ζ = 0,0012 bis 0,0017.
  Die höheren ρ zeigen, dass die Modellform dort schlechter passt; das Vorzeichen M8 ist
  dafür nicht verantwortlich, es ändert nur R.

**B-5 (Drift, Ref2/Ref1 als Mobilität, Pol je Punkt; Gruppenfit nach 3.3, Ausschluss je
gewählter Mode nach 4.5, K2-1):**

| Spitze | Gruppe (n) | $b_1$ | Dauer | Gesamtdrift | relativ | N (davon `modell_passt_nicht`) |
|---|---|---|---|---|---|---|
| ≈ 418,9 Hz | allein (1) | −0,129 ± 0,010 Hz/h | 39,6 min | −0,085 Hz | −2,0·10⁻⁴ | 135 (90) |
| ≈ 631,7 Hz | mit 640,6 Hz (2) | −0,068 ± 0,010 Hz/h | 39,1 min | −0,044 Hz | −0,7·10⁻⁴ | 125 (0) |
| ≈ 1508,1 Hz | mit 1491,8 Hz (2) | −0,482 ± 0,016 Hz/h | 39,6 min | −0,318 Hz | −2,1·10⁻⁴ | 135 (0) |

- Alle drei Steigungen sind signifikant und bestätigen W3 2.7.
- Die Streuung um die Gerade (0,022 bis 0,035 Hz) ist kleiner als die mittlere
  Fit-Standardabweichung der verwendeten Punkte (0,036 bis 0,082 Hz). Die
  Fit-Standardabweichung enthält also auch Modellfehler. Deshalb kommt der Standardfehler der
  Drift aus der Streuung um die Gerade (4.5).
- Die Erstfassung dieser Tabelle (−0,132 / −0,079 / −0,520 Hz/h) stammte aus einem
  vereinfachten Prüfskript mit Einzelmodenfit und ohne Ausschluss. Sie ist durch die Werte
  oben ersetzt. Der Gruppenfit passt besser: bei 1508 Hz ρ = 0,040 statt 0,069 und Streuung
  0,035 statt 0,040 Hz.
- Bei 631,7 Hz trägt der Gruppenfit an 95 Punkten `nicht_konvergiert` (Partnermode 640,6 Hz
  läuft weg); 10 Punkte fallen über `unsicher` der gewählten Mode heraus.

**B-8:**
- 112 Elemente; alle Knotenreihenfolgen ergeben eine Normale mit negativer z-Komponente.
  Nach Ausrichtung auf +z sind die Punktnormalen 1,3° bis 5,0° gegen z geneigt (Median 3,2°).
- Anteil der Normalenbewegung η (CPH zu Ref1) als Median über Punkte und Linien:

  | Band | Median | 10-%-Quantil |
  |---|---|---|
  | 150–500 Hz | 0,995 | 0,90 |
  | 500–1000 Hz | 0,983 | 0,71 |
  | 1000–2500 Hz | 0,967 | 0,65 |

  Das ist plausibel für eine Platte in Biegung und stützt M12. Bewiesen ist M12 damit nur
  für die z-Richtung; die Lage von X und Y prüft dieser Befund nicht.

---

## 8 Entscheidungen für den Nutzer (Optionen mit Empfehlung)

| Nr. | Frage | Optionen | Empfehlung |
|---|---|---|---|
| E1 | Fit-Verfahren B-1 | (a) komplexer Moden-Fit mit Variablenprojektion, n = 1 bzw. Gruppengröße; (b) Kreisfit (Nyquist); (c) LSCF/PolyMAX mit Stabilisierungsdiagramm | **(a).** (b) braucht mehrere Punkte auf dem Kreis nahe der Resonanz; bei $B/\Delta f \approx 1$ gibt es nur 1 bis 2, deshalb ungeeignet. (c) verlangt Modellordnungswahl und Polauswahl und gehört zur Modalanalyse (R-054) |
| E2 | Ort des Fits | (a) je Punkt, Zusammenfassung über die stärksten Punkte; (b) nur am Antriebspunkt-Paar; (c) globaler Fit mit gemeinsamen Polen | **(a)**, (b) als Option. (c) gehört zur Modalanalyse |
| E3 | Gewichtung | (a) ungewichtet mit Kohärenzmaske; (b) $1/(\lvert H\rvert\varepsilon)^2$ | **(a).** (b) betont Linien mit kleinem Betrag; bei $n_d$ = 7 sind die ε-Schätzungen selbst unsicher (FG-02 3.4) |
| E4 | Punktzuordnung | (a) Label; (b) Koordinaten mit Passpunkten | **(a) als Voreinstellung, (b) wählbar** |
| E5 | Bezugsrichtung der Normalen | (a) +z des Abgleichs; (b) Richtung zu den Scanköpfen (Kopfpositionen nicht in der Datei dekodiert) | **(a)** bis M13 geklärt |
| E6 | Schwellen | ρ_max = 0,10; $\sigma_\zeta/\zeta$ ≤ 0,2; $n_\mathrm{fit}$ = 6; $n_\mathrm{max}$ = 4; $n_\mathrm{P}$ = 20; $\Delta f_\mathrm{tol}$ = 2 Δf; $d_\mathrm{tol}$ = 0,5 $d_\mathrm{min}$ | wie angegeben, freigeben oder ändern |

---

## 9 Referenzfälle (Tests)

Bezeichnungen und Toleranzlogik wie FG-02 Abschnitt 9. Mobilität
$Y = i\omega/(m(\omega_n^2 - \omega^2 + 2i\zeta\omega_n\omega))$ mit m = 1 kg. Raster
$f_j = (k_0 + j + \mathrm{off})\,\Delta f$.

### 9.1 B-1

| ID | Eingang | Sollwert | Toleranz, Begründung |
|---|---|---|---|
| RF-F1 | SDOF $f_n$ = 100 Hz, ζ = 0,005; Δf = 1,5625 Hz ($B/\Delta f$ = 0,64); 17 Linien um Linie 64; off = 0 und 0,37; Start $f^{(0)}$ = 100,3 Hz, $\zeta^{(0)}$ = 0,01 | $f_r$ = 100 Hz, ζ = 0,005, R = 1 kg⁻¹, C = 0, ρ ≈ 0; konvergiert, ohne Kennzeichen (Abbruchkriterium K2-2) | $f_r$: atol 1e-7 Hz; ζ, R: rtol 1e-6; \|C\| ≤ 1e-12; ρ ≤ 1e-12 (exakte Modellform) |
| RF-F2 (statistisch) | wie RF-F1, off = 0,37, komplexes Rauschen σ = 0,01·max\|Y\| (bzw. 0,03), 400 Wiederholungen, `default_rng(20261030)` | Mittelwert ζ ≈ 0,005; Streuung σ_ζ/ζ ≈ 0,0135 (bzw. 0,0415); mittlere Fit-sd ≈ 0,0131 (0,0392) | Bias \|·\| ≤ 0,01; Fit-sd innerhalb ±20 % der MC-Streuung |
| RF-F3 | zwei Moden 100 Hz und 102 bzw. 103 Hz, ζ = 0,01, Modalmasse 1 kg; Δf = 0,5 Hz, Linien 90 … 114,5 Hz | n = 2: $f_r$ = (100, $f_2$), ζ = (0,01; 0,01), ρ ≈ 0. Erzwungen n = 1 (±4 Linien um das Maximum): bei 102 Hz ζ = 0,020565 (+106 %), ρ = 0,112, $\sigma_{f_r}$ = 0,371 Hz > Δf/2 = 0,25 Hz, $\sigma_\zeta/\zeta$ = 0,18 → `modell_passt_nicht`, `unsicher` (K2-3); bei 103 Hz ζ = 0,008775 (−12 %), ρ = 0,096, $\sigma_{f_r}$ = 0,108 Hz, $\sigma_\zeta/\zeta$ = 0,124 → kein Kennzeichen (bekannte Grenze, 3.3) | n = 2: rtol 1e-6. n = 1: rtol 1e-3 (Algorithmus-Sollwert, Konvergenzschwelle); Kennzeichen exakt |
| RF-F3b (Gruppenbildung) | Spitzen aus Stufe 1 bei 100 und 102 Hz mit `nachbarmode` | eine Gruppe, n = 2 | exakt |
| RF-F3c (Gruppenfit mit weglaufender Partnermode, Hinweis) | Kein eigener Sollwert; Befund [D] bei 631,7 Hz (Abschnitt 7): Partnermode endet `ausserhalb_band`, Fit `nicht_konvergiert`, gewählte Mode brauchbar. Die Wirkung auf die Drift prüft RF-V6 | – | – |
| RF-F4 | Impulsantwort $h_v(t) = e^{-\zeta\omega_n t}(\cos\omega_d t - \tfrac{\zeta\omega_n}{\omega_d}\sin\omega_d t)$, $h_v(0)$ halb gewichtet, $f_s$ = 6250 Hz, N = 4000 (T = 0,64 s), $\hat H_k$ = rfft(h)/f_s; 17 Linien um $f_n$. Fälle (100 Hz; 0,005), (100; 0,01), (100; 0,02), (400; 0,002), (100; 0,05) | ζ und $f_r$ wie Eingabe (Pole unverfälscht trotz Rest 0,134 am Blockende) | ζ: rtol 1e-4; $f_r$: atol 1e-3 Hz (Abtastfehler der Faltungssumme; bei 100 T gemessen ≤ 1,4e-5) |
| RF-F5 | Burst-Chirp 20 → 2500 Hz linear, Dauer 0,4 T bzw. 0,8 T, Amplitude 1; $y = (x * h_v)\,\Delta t$, Block [0, T), Rechteck; $H_1 = Y_k/X_k$ (ein Block, ohne Rauschen); Fälle wie RF-F4 ohne ζ = 0,05 | Fit: \|ζ/ζ_wahr − 1\| ≤ 0,025 und ρ ≤ 0,05 in allen Fällen; Halbwertsbreite (FG-02 3.9) bei (100 Hz; 0,005): +0,316 bzw. +0,317 | Toleranz begründet durch die Modellabweichung (Leckage); Halbwertsbreite nur zur Dokumentation |
| RF-F6 (Kennzeichen) | RF-F1 mit nur 6 Linien → `zu_wenig_linien`; Fit an `np.conj(Y)` (off = 0,37, 17 Linien) → ρ = 0,454, ζ → 0: `modell_passt_nicht`, `nicht_konvergiert`, `ausserhalb_band`; Gruppe mit 5 Spitzen → `gruppe_zu_gross` | Kennzeichen; ρ > 0,4 | exakt |
| RF-F7 (Vorzeichen) | RF-F1 mit −Y | $f_r$, ζ wie RF-F1; R = −1 | wie RF-F1 |
| RF-F8 (γ² = NaN, K2-4) | RF-F1 (off = 0,37, 17 Linien) mit (a) γ² = NaN auf allen Linien ($n_d$ = 1); (b) γ² = NaN auf allen Linien außer der dritten Linie mit γ² = 0,5 < γ²_min | (a) Fit mit 17 Linien, Werte wie RF-F1, Hinweis „Kohärenz nicht prüfbar“, keine Kennzeichen (insbesondere nicht `zu_wenig_linien`). (b) Fit mit 16 Linien, Werte wie RF-F1, derselbe Hinweis | wie RF-F1; Linienzahl und Kennzeichen exakt |

### 9.2 B-5

Raster 9 × 15, Abstand d = 0,029 m, z = 0. Formen
$\phi_{mn} = \sin\!\big(m\pi\frac{x+d}{L_x+2d}\big)\sin\!\big(n\pi\frac{y+d}{L_y+2d}\big)$ mit
$L_x = 8d$, $L_y = 14d$.

| ID | Eingang | Sollwert | Toleranz |
|---|---|---|---|
| RF-V1 | MAC($\phi_{11}$, $\phi_{11}$); MAC($\phi_{11}$, (2 − 3i)$\phi_{11}$); MAC($\phi_{11}$, $\phi_{21}$), MAC($\phi_{11}$, $\phi_{12}$), MAC($\phi_{21}$, $\phi_{12}$); MAC($\phi_{11}$, $\phi_{11}$ + 0,5 $\phi_{21}$) | 1; 1; 0; 0; 0; 0,8 | atol 1e-12 |
| RF-V1b | 3D: $v$ = (0,1 $\phi_{21}$, 0,05i $\phi_{11}$, $\phi_{11}$) gegen (0, 0, $\phi_{11}$) | 0,9876543210 | rtol 1e-9 |
| RF-V2 | B = R·A + t mit R = Drehung um z um 10°, t = (0,05; −0,02; 0,01) m; Passpunkte: vier Eckpunkte | R, t exakt; alle 135 Punkte zugeordnet | R, t: atol 1e-12 |
| RF-V2b (statistisch) | wie V2, Koordinaten von B mit Rauschen σ = 0,5 mm, `default_rng(20261030)` | alle 135 gegenseitig zugeordnet; Winkel 10° | Winkel ±0,2°; größter Abstand ≤ $d_\mathrm{tol}$ = 14,5 mm (beobachtet 2,0 mm) |
| RF-V2c | $v_A$ = (0,3 $\phi_{21}$, 0,2 $\phi_{11}$, $\phi_{11}$), $v_B = R\,v_A$ | MAC ohne Drehung 0,9965074935; mit $R^\mathsf{T}v_B$ = 1 | rtol 1e-6; atol 1e-12 |
| RF-V2d | drei kollineare Passpunkte | `ValueError` | – |
| RF-V3 | $f^A$ = (100,0; 150,2; 260,5) Hz, $f^B$ = (100,3; 149,9; 261,4; 300,0) Hz, $\Delta f_\mathrm{tol}$ = 1,5 Hz | Paare (0,0; +0,3), (1,1; −0,3), (2,2; +0,9); 300 Hz ohne Partner | atol 1e-12 |
| RF-V4 | SDOF 100 Hz, ζ = 0,01, Linien 90 … 110 Hz, Δf = 0,25 Hz; (a) $H_B$ = 1,1 $H_A$; (b) $f_n^B$ = 101 Hz; (c) $\zeta^B$ = 0,012 | (a) frac = 1, pegel_db = 0,8278537032, diff_rel = 0,1. (b) 0,8024872570; −0,0518051640; 0,6489671289. (c) 0,9917806594; −0,8499289122; 0,1271162285 | rtol 1e-9 |
| RF-V5 | $f_r(t)$ = 418,9 Hz − 2·10⁻⁵ Hz/s · t, 135 Punkte gleichverteilt über 0 … 2376 s | $b_1$ = −0,072 Hz/h; Gesamtdrift −0,04752 Hz; relativ −1,1344·10⁻⁴; σ_b1 = 0 → `drift_signifikant` | rtol 1e-9 |
| RF-V6 (Drift-Ausschluss je Mode, K2-1) | Vorgegebene Fit-Ergebnisse je Punkt (Prüfung der Ausschlusslogik, ohne Fit): 20 Punkte, $t_p = 120\,p$ s ($p = 0 \dots 19$), $f_{r,p}$ der gewählten Mode = 631,7 Hz − 2·10⁻⁵ Hz/s · $t_p$; jeder Punkt, der ausgeschlossen werden muss, trägt stattdessen $f_{r,p}$ + 1,0 Hz. **(a) Gruppe n = 2, gewählte Mode 1:** Punkte 0–9 `nicht_konvergiert` (gemeinsam) und Mode 2 `ausserhalb_band`; Punkte 10, 11 Mode 1 `unsicher`; Punkt 12 Mode 1 `ausserhalb_band`; Punkte 13–19 `modell_passt_nicht`; zusätzlich Punkt 5 `gueltigkeit_offen_m7`, Punkt 6 `kohaerenz_niedrig`. Ausgeschlossen (+1,0 Hz): 10, 11, 12. **(b) n = 1:** Punkte 0–2 `nicht_konvergiert`, 10–12 wie (a), 13–19 `modell_passt_nicht`. Ausgeschlossen (+1,0 Hz): 0, 1, 2, 10, 11, 12 | (a) N = 17, davon `modell_passt_nicht` 7; $b_1$ = −0,072 Hz/h; Gesamtdrift −0,0456 Hz; relativ −7,2186164318·10⁻⁵; $b_0$ = 631,7 Hz; `drift_signifikant`. (b) N = 14, davon `modell_passt_nicht` 7; $b_1$ = −0,072 Hz/h; Gesamtdrift −0,0384 Hz; relativ −6,0789041762·10⁻⁵; $b_0$ = 631,6928 Hz (Zeit auf den ersten verwendeten Punkt bezogen); `drift_signifikant` | rtol 1e-9; N exakt. Ein falsch einbezogener Punkt verschiebt $b_1$ um mehr als 1e-3 relativ und fällt sicher auf |
| RF-V7 (σ der Spitzenpaarung, K2-3) | Zusammenfassung A: $f^A$ = 100,00 Hz, $\sigma_{f_r}$ der verwendeten Punkte (0,02; 0,04; 0,05) Hz. B: (i) $f^B$ = 100,15 Hz, (ii) $f^B$ = 100,09 Hz, jeweils $\sigma_{f_r}$ (0,03; 0,03; 0,09) Hz; $\Delta f_\mathrm{tol}$ = 1 Hz | $\sigma_A$ = 0,04 Hz, $\sigma_B$ = 0,03 Hz (Mediane), $\sqrt{\sigma_A^2+\sigma_B^2}$ = 0,05 Hz, Grenze 0,10 Hz. (i) Δf = +0,15 Hz → `signifikant`; (ii) Δf = +0,09 Hz → nicht `signifikant` | atol 1e-12 |

### 9.3 B-8

| ID | Eingang | Sollwert | Toleranz |
|---|---|---|---|
| RF-G1 | Ebene um 30° um y geneigt: $x = u\cos30°$, $y = v$, $z = -u\sin30°$; Raster u = 0 … 0,06 m (Schritt 0,02), v = 0 … 0,12 m (Schritt 0,03); 12 Vierecke | alle $n_e$ = (0,5; 0; 0,8660254038); $A_e$ = 6,0·10⁻⁴ m². Mit $\hat v$ = (0,3 + 0,1i; 0,2i; 1,0): $\hat v_n$ = 1,0160254038 + 0,05i, $\lvert\hat v_t\rvert_\mathrm{psv}$ = 0,3243337461, $n\cdot\hat v_t$ = 0 | atol 1e-12 |
| RF-G2 | verwundenes Viereck (0,0,0), (1,0,0), (1,1,0,1), (0,1,0) | $n$ = (−0,1; −0,1; 2)/√4,02 = (−0,0498754668; −0,0498754668; 0,9975093361); A = 1,0024968828; umgekehrte Knotenfolge ergibt −n, nach Ausrichtung auf +z wieder n | atol 1e-10 |
| RF-G3 | Zylinder R = 0,1 m um die y-Achse, 7 Stützwinkel im Abstand 10°, 3 Höhen (0, 0,02, 0,04 m) | Innenpunkte: Winkel zur radialen Normalen 0; Randwinkel: 5,0° (halber Schritt) | innen ≤ 1e-5° (Rundung von arccos); Rand atol 1e-9° |
| RF-G4 | Ellipsen: (a) $\hat v$ = (1, i, 0); (b) (1; 0,5e^{iπ/3}; 0,2i); (c) (1, −i, 0); n = (0, 0, 1) | (a) a = b = 1, `achse_max` NaN (Kreis), σ = −1. (b) θ* = −0,1268510019 rad, a = 1,0374517607, b = 0,4622703151, $e_\mathrm{max}$ = ±(0,9561554879; 0,2918421984; 0,0243888118), σ = −1 (n·m = −0,4330127019). (c) σ = +1 | rtol 1e-9; Achse über \|e·e_soll\| ≥ 1 − 1e-6 (Brute-Force mit 400 001 Winkeln liefert 1e-6 genau) |
| RF-G5 | Punkt ohne Element; entartetes Element (drei gleiche Knoten) | NaN mit Hinweis; Element ignoriert | exakt |

---

## 10 Quellen

| Quelle | Prüfstand | Verwendet für |
|---|---|---|
| FG-02 (mit K1), W3, W5-1 | Repo | Konventionen, Stufe-1-Größen, Datenbefunde |
| Polytec SM 9-38 (MAC-Beispiel), HB 9-11 (1-DOF-Fit) über W1 | Herstellerangabe, volltext teilweise | MAC-Interpretation, Vergleich mit PSV-Fit |
| Ewins, *Modal Testing* (`ewins2000modal`) | **metadaten** | Kreisfit, Kurvenanpassung, Residuen außerhalb des Bands: nicht gelesen; hier eigene Herleitung |
| Maia/Silva (`maia1997theoretical`) | **metadaten** | rationale Funktionen und Mehr-Moden-Fit: nicht gelesen |
| Allemang (`allemang2003mac`) | **metadaten** | MAC: Definition hier eigene, Quelle für den Thesis-Text nötig |
| Peeters et al. (`peeters2009modern`) | **metadaten** | Einordnung LSCF/PolyMAX (Option E1c) |
| Kabsch-Verfahren, Variablenprojektion (Golub/Pereyra), FRAC | **nicht in literatur.bib** | Rechercheauftrag; hier vollständig hergeleitet bzw. numerisch geprüft |

---

## 11 Einstellbare Annahmen und Prüfschritte

Es gelten M1–M11 aus FG-02. Neu bzw. für Stufe 2 relevant:

| Nr. | Annahme | Prüfung | Folge |
|---|---|---|---|
| M2 | erste Linie bei Δf | Montag | $f_r$ verschiebt sich um Δf bei falscher Annahme |
| M5 | Rechteckfenster, $n_d$ = 7 | Montag | bei Hann auf Burst-Daten: Modellform nicht geprüft, RF-F5 nicht übertragbar |
| M8 | Vorzeichen je Kanal | Montag | nur R und Schwingformvorzeichen, nicht $f_r$, ζ, MAC |
| M11 | PSV-Toleranzen | Montag: Band-Cursor-Fit an 401,6 Hz und 618,9 Hz zusätzlich mit B-1 vergleichen | Einordnung des PSV-Fits gegen B-1; keine Toleranz für B-1 gegen PSV festgelegt |
| **M12** (neu) | 3D-Komponenten im Koordinatensystem der Geometrie | Montag: Achsen des 3D-Abgleichs in PSV ansehen; Indiz [D] η ≈ 0,99 | B-8 und gedrehte Vergleiche in B-5 |
| **M13** (neu) | Bezugsrichtung der Normalen +z | Montag: Lage der Scanköpfe zum Prüfling | Vorzeichen von $\hat v_n$ und Drehsinn |
| **M14** (neu) | Elementindizes 0-basiert (W2 plausibel) | Montag: Element in PSV ansehen, Eckpunkt-Labels gegen Indizes | B-8 |
| **M15** (neu) | Zeitstempel je Punkt = Messzeitpunkt | Montag: PSV-Info zur Messzeit (W2 M9) | B-5 Drift; nur Differenzen nötig |
| **Zweite Messdatei** | – | Wiederholungsmessung mit gleichem Aufbau, möglichst eine mit verschobenem bzw. neu abgeglichenem Raster | erst damit ist B-5 an realen Daten prüfbar (Golden-File-Vergleich, Punktzuordnung über Koordinaten) |

---

## 12 Offene Punkte

1. Annahmen M1–M15 bis Montag.
2. Wie sich der Fit bei Hann-Fenster auf transienten Daten verhält, ist nicht geprüft (M5).
3. Eine B-1-Toleranz gegen den PSV-Fit ist nicht festgelegt. Erst M11 liefert Werte.
4. Rechercheaufträge: Volltexte von Ewins und Maia/Silva (Kurvenanpassung, Residuen),
   Allemang (MAC), dazu Quellen für Kabsch, Variablenprojektion und FRAC.
5. Drift: Ursache (Temperatur?) ist eine Versuchsfrage. Ein Temperaturprotokoll würde helfen.
6. B-5 mit zwei realen Messungen ist erst mit einer zweiten Datei prüfbar.

---

## Anhang: Prüfskripte

Ausgeführt mit numpy aus `software/` (`uv run --group werkzeuge python <skript>`); die
Dateiprüfungen nutzen den W2-Leser nur lesend. Die Skripte lagen im Scratchpad unter `fg03/`.

### fit.py – Moden-Fit (Variablenprojektion, Levenberg-Marquardt)

```python
"""Komplexer Moden-Fit (Variablenprojektion, Levenberg-Marquardt), nur numpy. FG-03 B-1."""
import numpy as np

def basis(f, fr, z):
    """Spalten: Mobilitaetsmoden i w/(wr^2 - w^2 + 2 i z wr w) je Mode, plus Konstante."""
    w = 2*np.pi*np.asarray(f)[:, None]; wr = 2*np.pi*np.asarray(fr)[None, :]; z = np.asarray(z)[None, :]
    cols = 1j*w/(wr**2 - w**2 + 2j*z*wr*w)
    return np.hstack([cols, np.ones((len(f), 1))])

def projektion(f, H, fr, z, gew=None):
    Phi = basis(f, fr, z)
    W = np.ones(len(f)) if gew is None else np.sqrt(gew)
    R, *_ = np.linalg.lstsq(Phi*W[:, None], H*W, rcond=None)
    r = (H - Phi @ R)*W
    return R, r

def fit(f, H, fr0, z0, gew=None, it=200, tol=1e-12):
    """theta = (fr_1..fr_n, ln z_1..ln z_n). Rueckgabe fr, z, R (Modalkonst.), C (Residuum), Info."""
    th = np.concatenate([np.asarray(fr0, float), np.log(np.asarray(z0, float))])
    n = len(fr0)
    def res(th):
        _, r = projektion(f, H, th[:n], np.exp(th[n:]), gew); return np.concatenate([r.real, r.imag])
    lam = 1e-3; r0 = res(th); s0 = r0 @ r0
    for i in range(it):
        J = np.empty((len(r0), len(th)))
        for j in range(len(th)):
            h = 1e-7*max(1.0, abs(th[j])); d = th.copy(); d[j] += h
            J[:, j] = (res(d) - r0)/h
        A = J.T @ J; g = J.T @ r0
        while True:
            try:
                step = -np.linalg.solve(A + lam*np.diag(np.diag(A)), g)
            except np.linalg.LinAlgError:       # singulaer: Abbruch, Kennzeichen nicht_konvergiert
                lam = 1e13; break
            r1 = res(th+step); s1 = r1 @ r1
            if s1 < s0: th = th+step; lam = max(lam/10, 1e-12); break
            lam *= 10
            if lam > 1e12: break
        if lam > 1e12 or abs(s0 - s1) <= tol*max(s0, 1e-300):
            r0 = res(th); s0 = r0 @ r0; break
        r0, s0 = r1, s1
    fr, z = th[:n], np.exp(th[n:])
    R, r = projektion(f, H, fr, z, gew)
    # Kovarianz der nichtlinearen Parameter (Gauss-Newton-Naeherung)
    m = len(r0); p = 2*n + 2*(n+1)
    s2 = s0/max(m - p, 1)
    J = np.empty((m, len(th)))
    for j in range(len(th)):
        h = 1e-7*max(1.0, abs(th[j])); d = th.copy(); d[j] += h
        J[:, j] = (res(d) - r0)/h
    try:
        cov = s2*np.linalg.inv(J.T @ J)
        sd = np.sqrt(np.diag(cov))
    except np.linalg.LinAlgError:
        sd = np.full(len(th), np.nan)
    rho = np.linalg.norm(r)/np.linalg.norm(H*(1 if gew is None else np.sqrt(gew)))
    return dict(fr=fr, z=z, R=R[:n], C=R[n], sd_fr=sd[:n], sd_z_rel=sd[n:], rho=rho, it=i+1,
                konvergiert=bool(lam <= 1e12 and i + 1 < it))
```

### rf_b1.py – RF-F1 bis RF-F3

```python
import numpy as np, sys
sys.path.insert(0, "/tmp/claude-0/-home-user/e6b61297-17fb-5003-91f8-95c4534d012c/scratchpad/fg03")
from fit import fit
def Y(f, fn=100., z=0.005, m=1.0):
    w = 2*np.pi*f; wn = 2*np.pi*fn; return 1j*w/(m*(wn**2 - w**2 + 2j*z*wn*w))
DF = 1.5625
def raster(off, n=8, f0=100.):  # +-n Linien um die Linie bei f0
    k0 = int(round(f0/DF)); return (np.arange(k0-n, k0+n+1) + off)*DF
print("== RF-F1: exaktes SDOF, B/df = 0,64 ==")
for off in [0.0, 0.37]:
    f = raster(off); H = Y(f)
    r = fit(f, H, [100.0 + 0.3], [0.01])
    print(f"off={off}: fr={r['fr'][0]:.10f} z={r['z'][0]:.10e} R={r['R'][0]:.8f} C={r['C']:.2e} rho={r['rho']:.2e} it={r['it']}")
print("== RF-F2: mit Rauschen (MC) ==")
rng = np.random.default_rng(20261030)
for zt, rel in [(0.005, 0.01), (0.005, 0.03), (0.02, 0.01)]:
    f = raster(0.37); H0 = Y(f, z=zt); sig = rel*np.abs(H0).max()
    zs, frs, sds = [], [], []
    for _ in range(400):
        H = H0 + sig/np.sqrt(2)*(rng.standard_normal(len(f)) + 1j*rng.standard_normal(len(f)))
        r = fit(f, H, [100.3], [2*zt]); zs.append(r['z'][0]); frs.append(r['fr'][0]); sds.append(r['sd_z_rel'][0])
    zs = np.array(zs); frs = np.array(frs)
    print(f"z={zt} sigma={rel}*max: z mean rel bias {zs.mean()/zt-1:+.4f}, std rel {zs.std()/zt:.4f}, mittl. sd_rel(Fit) {np.mean(sds):.4f}; fr bias {frs.mean()-100:+.5f} Hz std {frs.std():.5f} Hz")
print("== RF-F3: zwei eng liegende Moden ==")
def Y2(f, f1, f2, z=0.01):
    return Y(f, f1, z) + Y(f, f2, z)
df = 0.5
f = np.arange(180, 230)*df   # 90 .. 114.5 Hz
for f2 in [102.0, 103.0]:
    H = Y2(f, 100.0, f2)
    r2 = fit(f, H, [99.8, f2+0.2], [0.015, 0.015])
    print(f"f2={f2}: 2-Moden: fr={np.round(r2['fr'],9)} z={np.round(r2['z'],10)} rho={r2['rho']:.1e}")
    # 1-Moden-Fit nur um die erste Spitze (+-4 Linien)
    k = np.argmax(np.abs(H)); sel = slice(k-4, k+5)
    r1 = fit(f[sel], H[sel], [f[k]], [0.01])
    print(f"   1-Mode um {f[k]} Hz: fr={r1['fr'][0]:.6f} z={r1['z'][0]:.6f} (rel {r1['z'][0]/0.01-1:+.3f}) rho={r1['rho']:.3e}")
```

### rf_leck.py – RF-F4 (Impulsantwort, abgeschnitten)

```python
"""RF-F4: Leckage durch abgeschnittene Impulsantwort (Rechteckfenster, T = 0,64 s)."""
import numpy as np, sys
sys.path.insert(0, "/tmp/claude-0/-home-user/e6b61297-17fb-5003-91f8-95c4534d012c/scratchpad/fg03")
from fit import fit
FS, N = 6250.0, 4000; T = N/FS; DF = 1/T
def hv(t, fn, z, m=1.0):
    wn = 2*np.pi*fn; wd = wn*np.sqrt(1-z*z)
    return np.exp(-z*wn*t)*(np.cos(wd*t) - z*wn/wd*np.sin(wd*t))/m
def H_mess(fn, z, Tlen):
    n = int(round(Tlen*FS)); t = np.arange(n)/FS
    h = hv(t, fn, z); h[0] *= 0.5            # Trapez an der Sprungstelle t = 0
    Hk = np.fft.rfft(h)/FS                   # = sum h(t_n) e^{-i w t_n} dt  (e^{+iwt}-Konvention)
    f = np.arange(len(Hk))*FS/n
    return f, Hk
def Ywahr(f, fn, z):
    w = 2*np.pi*f; wn = 2*np.pi*fn; return 1j*w/(wn**2 - w**2 + 2j*z*wn*w)
for fn, z in [(100.0, 0.005), (100.0, 0.01), (100.0, 0.02), (400.0, 0.002), (100.0, 0.05)]:
    rT = np.exp(-z*2*np.pi*fn*T)
    f, H = H_mess(fn, z, T)
    k0 = int(round(fn/DF)); sel = slice(k0-8, k0+9)
    r = fit(f[sel], H[sel], [fn+0.3], [2*z])
    # Kontrolle Diskretisierung: lange Messzeit (100 s), gleiche Linien-Lage
    fl, Hl = H_mess(fn, z, 100*T); kl = int(round(fn*100*T)); sl = slice(kl-800, kl+801, 100)
    rl = fit(fl[sl], Hl[sl], [fn+0.3], [2*z])
    # Halbwertsbreite (Stufe 1) auf |H| zum Vergleich
    y = np.abs(H); k = int(np.argmax(y[1:]))+1
    print(f"fn={fn} z={z}: r_T=exp(-z w T)={rT:.4f}  Fit-z rel {r['z'][0]/z-1:+.4f} fr {r['fr'][0]-fn:+.4f} Hz rho={r['rho']:.3f} | ohne Leckage (100 T): z rel {rl['z'][0]/z-1:+.2e}")
```

### rf_burst.py – RF-F5 (Burst-Chirp)

```python
"""RF-F5: Burst-Chirp (40 % des Blocks), Rechteckfenster, Antwort im Block abgeschnitten."""
import numpy as np, sys
sys.path.insert(0, "/tmp/claude-0/-home-user/e6b61297-17fb-5003-91f8-95c4534d012c/scratchpad/fg03")
from fit import fit
FS, N = 6250.0, 4000; T = N/FS; DF = 1/T; dt = 1/FS
def hv(t, fn, z):
    wn = 2*np.pi*fn; wd = wn*np.sqrt(1-z*z)
    return np.exp(-z*wn*t)*(np.cos(wd*t) - z*wn/wd*np.sin(wd*t))
def burst_chirp(anteil, f0=20.0, f1=2500.0):
    t = np.arange(N)*dt; Tb = anteil*T; x = np.zeros(N); m = t < Tb
    x[m] = np.sin(2*np.pi*(f0*t[m] + 0.5*(f1-f0)/Tb*t[m]**2)); return x
def H1_block(fn, z, anteil):
    x = burst_chirp(anteil)
    th = np.arange(int(30*FS))*dt; h = hv(th, fn, z); h[0] *= 0.5
    y = np.convolve(x, h)[:N]*dt                 # Antwort im Block (System vorher in Ruhe)
    X = np.fft.rfft(x); Yk = np.fft.rfft(y)
    return np.arange(len(X))*DF, Yk/X
def Ywahr(f, fn, z):
    w = 2*np.pi*f; wn = 2*np.pi*fn; return 1j*w/(wn**2 - w**2 + 2j*z*wn*w)
for anteil in [0.4, 0.8]:
    for fn, z in [(100.0, 0.005), (100.0, 0.01), (100.0, 0.02), (400.0, 0.002), (400.0, 0.005)]:
        f, H = H1_block(fn, z, anteil)
        rT = np.exp(-z*2*np.pi*fn*(1-anteil)*T)
        k0 = int(round(fn/DF)); sel = slice(k0-8, k0+9)
        r = fit(f[sel], H[sel], [fn+0.3], [2*z])
        # Halbwertsbreite (FG-02 3.9, Parabel + lineare Interpolation) auf |H|
        y = np.abs(H); k = k0-3+int(np.argmax(y[k0-3:k0+4])); a, b, c = y[k-1], y[k], y[k+1]
        d = 0.5*(a-c)/(a-2*b+c); A = b-0.25*(a-c)*d; s = A/np.sqrt(2)
        j = k
        while y[j] >= s: j -= 1
        fl = f[j]+(s-y[j])/(y[j+1]-y[j])*DF
        j = k
        while y[j] >= s: j += 1
        fr_ = f[j-1]+(y[j-1]-s)/(y[j-1]-y[j])*DF
        zhp = (fr_-fl)/(2*(f[k]+d*DF))
        err = np.max(np.abs(H[sel]-Ywahr(f[sel], fn, z)))/np.max(np.abs(Ywahr(f[sel], fn, z)))
        print(f"Burst {anteil:.1f}T fn={fn} z={z}: Rest am Blockende r={rT:.3f}; max|H1-Y|/max|Y|={err:.3f}; Fit z rel {r['z'][0]/z-1:+.3f}, fr {r['fr'][0]-fn:+.3f} Hz, rho={r['rho']:.3f}; Halbwertsbreite z rel {zhp/z-1:+.3f} (B/df={2*z*fn/DF:.2f})")
```

### rf_f6.py – RF-F6 und RF-F7

```python
import numpy as np, sys
sys.path.insert(0, ".")
from fit import fit
DF = 1.5625
def Y(f, fn=100., z=0.005): w = 2*np.pi*f; wn = 2*np.pi*fn; return 1j*w/(wn**2-w**2+2j*z*wn*w)
f = (np.arange(64-8, 64+9) + 0.37)*DF
r = fit(f, np.conj(Y(f)), [100.3], [0.01]); print("konjugiert: rho", r['rho'], "z", r['z'][0], "fr", r['fr'][0])
r = fit(f, -Y(f), [100.3], [0.01]); print("negiert: fr", r['fr'][0], "z", r['z'][0], "R", r['R'][0], "rho", r['rho'])
```

### rf_b5_b8.py – RF-V1 bis RF-V5, RF-G1 bis RF-G4

```python
import numpy as np
np.set_printoptions(precision=10, suppress=False)
def mac(a, b):
    a = np.ravel(a); b = np.ravel(b)
    return abs(np.vdot(a, b))**2/(np.vdot(a, a).real*np.vdot(b, b).real)
# Raster 9 x 15 wie Beispieldatei, Abstand 0,029 m (Lx = 0,232, Ly = 0,406)
nx, ny, d = 9, 15, 0.029
gx, gy = np.meshgrid(np.arange(nx)*d, np.arange(ny)*d, indexing="ij")
P = np.column_stack([gx.ravel(), gy.ravel(), np.zeros(gx.size)])
Lx, Ly = (nx-1)*d, (ny-1)*d
def form(m, n): return np.sin(m*np.pi*(P[:, 0]+d)/(Lx+2*d))*np.sin(n*np.pi*(P[:, 1]+d)/(Ly+2*d))
print("== RF-V1 MAC ==")
p11, p21, p12 = form(1, 1), form(2, 1), form(1, 2)
print("MAC(p11,p11)", mac(p11, p11), " MAC(p11,(2-3i)p11)", mac(p11, (2-3j)*p11))
print("MAC(p11,p21)", mac(p11, p21), " MAC(p11,p12)", mac(p11, p12), " MAC(p21,p12)", mac(p21, p12))
mix = p11 + 0.5*p21
print("MAC(p11, p11+0,5 p21)", mac(p11, mix))
# 3D-Form: Komponenten stapeln
v3 = np.column_stack([0.1*p21, 0.05j*p11, p11])
print("MAC 3D identisch", mac(v3, v3), " MAC 3D vs nur Z", mac(v3, np.column_stack([0*p11, 0*p11, p11])))
print("== RF-V2 Punktzuordnung, starre Transformation (Kabsch) ==")
a = np.radians(10.0); R = np.array([[np.cos(a), -np.sin(a), 0], [np.sin(a), np.cos(a), 0], [0, 0, 1]])
t = np.array([0.05, -0.02, 0.01])
Q = P @ R.T + t
def kabsch(A, B):
    ca, cb = A.mean(0), B.mean(0); Hm = (A-ca).T @ (B-cb); U, S, Vt = np.linalg.svd(Hm)
    D = np.diag([1, 1, np.sign(np.linalg.det(Vt.T @ U.T))]); Rr = Vt.T @ D @ U.T; return Rr, cb - Rr @ ca
idx = [0, nx*ny-1, ny-1, (nx-1)*ny]  # vier Eckpunkte als Passpunkte
Re, te = kabsch(P[idx], Q[idx])
print("R-Fehler", np.abs(Re-R).max(), " t-Fehler", np.abs(te-t).max(), " Winkel", np.degrees(np.arctan2(Re[1, 0], Re[0, 0])))
rng = np.random.default_rng(20261030)
Qn = Q + rng.normal(0, 0.0005, Q.shape)
Re2, te2 = kabsch(P[idx], Qn[idx])
Pt = P @ Re2.T + te2
dist = np.linalg.norm(Pt[:, None, :]-Qn[None, :, :], axis=2)
nn = dist.argmin(1); nn_r = dist.argmin(0)
gegenseitig = np.array([nn_r[nn[i]] == i for i in range(len(P))])
print("Rauschen 0,5 mm: richtige Zuordnung", np.sum(nn == np.arange(len(P))), "von", len(P), " gegenseitig", gegenseitig.sum(), " max Abstand", dist[np.arange(len(P)), nn].max(), " Toleranz 0,5*d", 0.5*d, " Winkel", np.degrees(np.arctan2(Re2[1, 0], Re2[0, 0])))
# Komponenten drehen
vA = np.column_stack([0.3*p21, 0.2*p11, p11])        # Messung A, Komponenten im System A
vB = vA @ R.T                                          # Messung B: dieselbe Bewegung, Komponenten im System B
print("MAC ohne Drehung der Komponenten", mac(vA, vB), " mit v_B R^T", mac(vA, vB @ R))
print("== RF-V3 Spitzenpaarung ==")
fa = np.array([100.0, 150.2, 260.5]); fb = np.array([100.3, 149.9, 261.4, 300.0]); tol = 1.5
paare = []
for i, x in enumerate(fa):
    j = int(np.argmin(abs(fb-x)))
    if abs(fb[j]-x) <= tol and int(np.argmin(abs(fa-fb[j]))) == i: paare.append((i, j, fb[j]-x))
print(paare)
print("== RF-V4 FRF-Vergleich ==")
def Y(f, fn=100., z=0.01): w = 2*np.pi*f; wn = 2*np.pi*fn; return 1j*w/(wn**2-w**2+2j*z*wn*w)
f = np.arange(90, 110.0001, 0.25)
Ha = Y(f); Hb = 1.1*Ha
def frac(a, b): return abs(np.vdot(a, b))**2/(np.vdot(a, a).real*np.vdot(b, b).real)
def pegel(a, b): return 10*np.log10(np.sum(abs(b)**2)/np.sum(abs(a)**2))
def reldiff(a, b): return np.linalg.norm(b-a)/np.linalg.norm(a)
print("skaliert 1,1: FRAC", frac(Ha, Hb), " Pegel dB", pegel(Ha, Hb), " rel. Diff", reldiff(Ha, Hb))
Hc = Y(f, 101.0)
print("verschoben 101 Hz: FRAC", frac(Ha, Hc), " Pegel dB", pegel(Ha, Hc), " rel. Diff", reldiff(Ha, Hc))
Hd = Y(f, 100.0, 0.012)
print("zeta 0,012: FRAC", frac(Ha, Hd), " Pegel dB", pegel(Ha, Hd), " rel. Diff", reldiff(Ha, Hd))
print("== RF-V5 Drift ==")
tt = np.linspace(0, 2376.0, 135); fr = 418.9 - 2.0e-5*tt
A = np.vstack([tt, np.ones_like(tt)]).T; b1, b0 = np.linalg.lstsq(A, fr, rcond=None)[0]
print("Steigung Hz/s", b1, " Hz/h", b1*3600, " gesamt", b1*tt.max(), " rel", b1*tt.max()/b0)
print("== RF-G1 geneigte Ebene ==")
al = np.radians(30.0); n_soll = np.array([np.sin(al), 0, np.cos(al)])
u, v = np.meshgrid(np.arange(4)*0.02, np.arange(5)*0.03, indexing="ij")
G = np.column_stack([(u*np.cos(al)).ravel(), v.ravel(), (-u*np.sin(al)).ravel()])
def idxp(i, j): return i*5+j
E = [(idxp(i, j), idxp(i+1, j), idxp(i+1, j+1), idxp(i, j+1)) for i in range(3) for j in range(4)]
def normale_el(X, e):
    p = X[list(e)]; c = np.cross(p[2]-p[0], p[3]-p[1]) if len(e) == 4 else np.cross(p[1]-p[0], p[2]-p[0])
    return c/np.linalg.norm(c), 0.5*np.linalg.norm(c)
nE = np.array([normale_el(G, e)[0] for e in E])
print("Elementnormalen max Abweichung", np.abs(nE - n_soll).max(), " Flaeche Element", normale_el(G, E[0])[1], "soll", 0.02*0.03)
vv = np.array([0.3+0.1j, 0.2j, 1.0])
vn = n_soll @ vv; vt = vv - n_soll*vn
print("v_n", vn, " |v_n|", abs(vn), " v_t", vt, " |v_t|_psv", np.sqrt(np.sum(abs(vt)**2)), " Kontrolle n.v_t", n_soll @ vt)
print("== RF-G2 verwundenes Viereck ==")
h = 0.1; W = np.array([[0, 0, 0], [1, 0, 0], [1, 1, h], [0, 1, 0.]])
n, A_ = normale_el(W, (0, 1, 2, 3)); print("n", n, " soll", np.array([-h, -h, 2])/np.sqrt(4+2*h*h), " Flaeche (halbes Diagonalenkreuzprodukt)", A_)
print("Umkehr der Knotenreihenfolge:", normale_el(W, (0, 3, 2, 1))[0])
print("== RF-G3 Zylinder, Punktnormalen ==")
Rz, nphi, nz = 0.1, 7, 3; dphi = np.radians(10.0)
phi = (np.arange(nphi)-3)*dphi; zz = np.arange(nz)*0.02
C = np.array([[Rz*np.sin(p), z, Rz*np.cos(p)] for p in phi for z in zz])
def ic(i, j): return i*nz+j
EC = [(ic(i, j), ic(i+1, j), ic(i+1, j+1), ic(i, j+1)) for i in range(nphi-1) for j in range(nz-1)]
nP = np.zeros_like(C)
for e in EC:
    n_, a_ = normale_el(C, e); n_ = n_*np.sign(n_ @ np.array([0, 0, 1.0])); 
    for i in e: nP[i] += a_*n_
nP /= np.linalg.norm(nP, axis=1)[:, None]
soll = np.array([[np.sin(p), 0, np.cos(p)] for p in phi for z in zz])
fehler = np.degrees(np.arccos(np.clip(np.sum(nP*soll, 1), -1, 1)))
print("Winkelfehler innen (phi-Index 1..5):", fehler.reshape(nphi, nz)[1:-1].max(), " Rand:", fehler.reshape(nphi, nz)[[0, -1]].max(), " halber Schritt", np.degrees(dphi/2))
print("== RF-G4 Bahnellipse ==")
th = np.linspace(0, 2*np.pi, 400001)
for v in [np.array([1, 1j, 0]), np.array([1, 0.5*np.exp(1j*np.pi/3), 0.2j]), np.array([1, -1j, 0])]:
    s2 = np.sum(v**2); ths = -0.5*np.angle(s2)
    e_max = np.real(v*np.exp(1j*ths)); e_min = np.real(v*np.exp(1j*(ths+np.pi/2)))
    xt = np.real(v[:, None]*np.exp(1j*th[None, :])); r = np.linalg.norm(xt, axis=0)
    kb = np.argmax(r)
    ebene = np.cross(np.imag(v), np.real(v)); nz_ = np.array([0, 0, 1.0])
    print(v, "theta* =", ths, " a=", np.linalg.norm(e_max), " brute", r.max(), " Achse", e_max/np.linalg.norm(e_max), " brute-Achse", xt[:, kb]/r[kb], " b=", np.linalg.norm(e_min), " Drehsinn (Im x Re).n =", ebene @ nz_)
```

### datei.py – Befunde an der Datei: B-1, B-8, Drift

```python
"""FG-03 [D]: B-1-Fit, B-8-Normalen und B-5-Drift an 20261012_ref_Mitte.svd (nur lesend)."""
import sys, numpy as np
sys.path.insert(0, "/home/user/BA_Jakob-Busch_P/software/tools/svd_analyse")
sys.path.insert(0, "/tmp/claude-0/-home-user/e6b61297-17fb-5003-91f8-95c4534d012c/scratchpad/fg03")
from svd_lesen import lese_svd
from fit import fit
m = lese_svd("/home/user/BA_Jakob-Busch_P/Input/20261012_ref_Mitte.svd")
f = m.frequenz_hz; DF = f[1]-f[0]; w = 2*np.pi*f
sig = {}
for s in m.signale.values():
    sig[(s.art, s.kanaele)] = s.werte
def get(art, *k): return sig[(art, tuple(k))]
cpZ = get("CP", "Vib Z", "Ref1"); ap1 = get("AP", "Ref1"); apZ = get("AP", "Vib Z")
H1z = cpZ/ap1; g2z = np.abs(cpZ)**2/(apZ*ap1)
cpA = get("CP", "Ref2", "Ref1"); ap2 = get("AP", "Ref2")
YA = (cpA/ap1)/(1j*w)               # Antriebspunkt Ref2/Ref1 als Mobilitaet (Vorzeichen M8 offen)
print("== B-1 an Ref2/Ref1 (Mittel ueber Punkte, Mobilitaet) und H1 Vib Z ==")
YAm = YA.mean(0)
for f0 in [401.6, 418.8, 631.2, 907.8]:
    k = int(np.argmin(abs(f-f0))); k = k-2+int(np.argmax(np.abs(YAm[k-2:k+3])))
    sel = slice(k-6, k+7)
    r = fit(f[sel], YAm[sel], [f[k]], [0.003])
    print(f"Ref2/Ref1 ~{f[k]:.1f} Hz: fr={r['fr'][0]:.3f}±{r['sd_fr'][0]:.3f} Hz z={r['z'][0]:.5f}(±{100*r['sd_z_rel'][0]:.1f} %) B=2zf={2*r['z'][0]*r['fr'][0]:.3f} Hz, B/df={2*r['z'][0]*r['fr'][0]/DF:.2f}, rho={r['rho']:.3f}")
# Einzelpunkte H1 Vib Z: Spitze 401.6 Hz, Punkte mit groesster Antwort
for f0 in [401.6, 618.8, 262.5]:
    k = int(np.argmin(abs(f-f0)))
    amp = np.abs(H1z[:, k]); idx = np.argsort(amp)[::-1][:20]
    zs, frs, rhos = [], [], []
    for p in idx:
        kk = k-2+int(np.argmax(np.abs(H1z[p, k-2:k+3]))); sel = slice(kk-6, kk+7)
        r = fit(f[sel], H1z[p, sel], [f[kk]], [0.003]); zs.append(r['z'][0]); frs.append(r['fr'][0]); rhos.append(r['rho'])
    zs, frs, rhos = map(np.array, (zs, frs, rhos))
    print(f"H1 Vib Z ~{f0} Hz, 20 staerkste Punkte: fr Median {np.median(frs):.3f} Hz (IQR {np.subtract(*np.percentile(frs,[75,25])):.3f}), z Median {np.median(zs):.5f} (IQR {np.subtract(*np.percentile(zs,[75,25])):.5f}), rho Median {np.median(rhos):.3f} max {rhos.max():.3f}")
print("== B-8 Normalen der Geometrie ==")
X = m.punkte.koordinaten_m; E = m.elemente
nE = []; aE = []
for e in E:
    p = X[list(e)]
    c = np.cross(p[2]-p[0], p[3]-p[1]) if len(e) == 4 else np.cross(p[1]-p[0], p[2]-p[0])
    nE.append(c/np.linalg.norm(c)); aE.append(0.5*np.linalg.norm(c))
nE = np.array(nE); aE = np.array(aE)
ref = np.array([0, 0, 1.0]); sgn = np.sign(nE @ ref)
print("Elemente:", len(E), " Vorzeichen bzgl. +z:", np.unique(sgn, return_counts=True), " Flaeche gesamt", aE.sum(), "m2")
nP = np.zeros_like(X)
for e, n, a in zip(E, nE*sgn[:, None], aE):
    for i in e: nP[i] += a*n
nP /= np.linalg.norm(nP, axis=1)[:, None]
winkel = np.degrees(np.arccos(np.clip(nP @ ref, -1, 1)))
print("Punktnormale Winkel zu +z: min %.2f  median %.2f  max %.2f Grad" % (winkel.min(), np.median(winkel), winkel.max()))
V = np.stack([get("CPH", c, "Ref1") for c in ("Vib X", "Vib Y", "Vib Z")], axis=1)  # (P,3,K)
vn = np.einsum("pc,pck->pk", nP, V)
anteil = np.abs(vn)**2/np.sum(np.abs(V)**2, axis=1)
for lo, hi in [(150, 500), (500, 1000), (1000, 2500)]:
    b = (f > lo) & (f <= hi)
    print(f"Anteil |v_n|^2/|v|^2 {lo}-{hi} Hz: Median {np.median(anteil[:, b]):.4f}, 10%-Quantil {np.quantile(anteil[:, b], 0.1):.4f}")
print("== B-5 Drift: Ref2/Ref1-Pol je Punkt ueber die Scanzeit ==")
t = np.array([(z - min(z_ for z_ in m.signale[next(iter(m.signale))].zeit_a)).total_seconds() for z in m.signale[next(iter(m.signale))].zeit_a])
for f0 in [418.8, 631.2, 1507.8]:
    k = int(np.argmin(abs(f-f0))); k = k-2+int(np.argmax(np.abs(YAm[k-2:k+3]))); sel = slice(k-6, k+7)
    frs = []; sds = []
    for p in range(YA.shape[0]):
        r = fit(f[sel], YA[p, sel], [f[k]], [0.003]); frs.append(r['fr'][0]); sds.append(r['sd_fr'][0])
    frs = np.array(frs); A = np.vstack([t, np.ones_like(t)]).T
    (b1, b0), res, *_ = np.linalg.lstsq(A, frs, rcond=None)
    s = np.sqrt(res[0]/(len(t)-2)); sb = s/np.sqrt(np.sum((t-t.mean())**2))
    print(f"~{f[k]:.1f} Hz: Steigung {b1*3600:+.4f} Hz/h (±{sb*3600:.4f}), ueber {t.max()/60:.1f} min {b1*t.max():+.4f} Hz = {b1*t.max()/b0:+.2e} rel; Streuung um Trend {s:.4f} Hz, mittl. Fit-sd {np.mean(sds):.4f} Hz")
```

### gruppe.py – Befunde an der Datei: Gruppenfit 262,5 Hz

```python
import sys, numpy as np
sys.path.insert(0, "/home/user/BA_Jakob-Busch_P/software/tools/svd_analyse")
sys.path.insert(0, "/tmp/claude-0/-home-user/e6b61297-17fb-5003-91f8-95c4534d012c/scratchpad/fg03")
from svd_lesen import lese_svd
from fit import fit
m = lese_svd("/home/user/BA_Jakob-Busch_P/Input/20261012_ref_Mitte.svd")
f = m.frequenz_hz
sig = {(s.art, s.kanaele): s.werte for s in m.signale.values()}
H1 = sig[("CP", ("Vib Z", "Ref1"))]/sig[("AP", ("Ref1",))]
k = int(np.argmin(abs(f-262.5))); amp = np.abs(H1[:, k]); idx = np.argsort(amp)[::-1][:20]
lo, hi = int(np.argmin(abs(f-262.6)))-6, int(np.argmin(abs(f-270.0)))+6
for nm, fr0 in [(1, [262.6]), (2, [262.6, 270.0]), (3, [262.6, 265.0, 270.0])]:
    res = []
    for p in idx:
        sel = slice(lo, hi+1) if nm > 1 else slice(k-6, k+7)
        r = fit(f[sel], H1[p, sel], fr0, [0.003]*nm); res.append((r['fr'], r['z'], r['rho']))
    frs = np.array([x[0] for x in res]); zs = np.array([x[1] for x in res]); rh = np.array([x[2] for x in res])
    print(f"{nm} Mode(n), Band {f[lo] if nm>1 else f[k-6]:.1f}-{f[hi] if nm>1 else f[k+6]:.1f} Hz: fr Median {np.round(np.median(frs,0),3)}, z Median {np.round(np.median(zs,0),5)}, IQR z {np.round(np.subtract(*np.percentile(zs,[75,25],axis=0)),5)}, rho Median {np.median(rh):.3f} max {rh.max():.3f}")
```

### Ergänzung K2 (Fachabnahme FA-W5-2, 2026-10-30)

Ausgeführt aus `software/` mit `uv run python <skript>` gegen die Umsetzung W5-2 (nur lesend); die Skripte lagen im Scratchpad unter `fa_w52/`.

#### drift_k2.py – Drift nach K2-1 (Tabelle Abschnitt 7)

```python
"""FG-03 K2-1: Drift an der Beispieldatei mit Ausschluss je gewählter Mode (Option A)."""
import sys, pathlib, numpy as np
sys.path.insert(0, "tools/auswertung")
import beispiel_svd
from ldv_automation.auswertung import werte_aus
from ldv_automation.auswertung.annahmen import SchwellenStufe2
from ldv_automation.auswertung.svd_adapter import aus_svd_messung, zeit_s_aus_svd_messung
from ldv_automation.auswertung.vergleich import drift_aus, drift_regression
m = beispiel_svd.lese_svd_werkzeug(pathlib.Path("../Input/20261012_ref_Mitte.svd"))
aw = werte_aus(aus_svd_messung(m), antriebspunkt=("Ref2","Ref1","akzeleranz"))
t = zeit_s_aus_svd_messung(m); sp = aw.paare[("Ref2","Ref1")].spitzen.spitzen
for f0 in (418.8, 631.2, 1507.8):
    i = int(np.argmin([abs(s.f_sp_hz - f0) for s in sp]))
    _, fit = drift_aus(aw, t, f0, ("Ref2","Ref1"), schwellen2=SchwellenStufe2(drift_ausschluss=()))
    g = next(g for g in fit.gruppen if i in g.spitzen); mode = g.spitzen.index(i); n = len(g.spitzen)
    fr = np.full(t.size, np.nan); sd = []; mpn = 0
    for e in fit.ergebnisse:
        k = set(e.kennzeichen[mode])
        aus = {"ausserhalb_band", "unsicher"} | ({"nicht_konvergiert"} if n == 1 else set())
        if e.gefittet and not k & aus:
            fr[e.punkt] = e.fr_hz[mode]; sd.append(e.sd_fr_hz[mode]); mpn += "modell_passt_nicht" in k
    d = drift_regression(fr, t)
    print(f"{sp[i].f_sp_hz:.3f} Hz n={n}: b1 {d.steigung_hz_h:+.4f} ± {d.sd_steigung_hz_h:.4f} Hz/h, Dauer {d.dauer_s/60:.1f} min, gesamt {d.gesamt_hz:+.4f} Hz, rel {d.gesamt_rel:+.2e}, s {d.streuung_hz:.4f} Hz, mittl. Fit-sd {np.mean(sd):.4f} Hz, N {d.n_punkte}, davon modell_passt_nicht {mpn}, sig {d.signifikant}")
```

#### drift_var.py – Drift-Varianten: Ausschluss über ρ, Gruppen- vs. Einzelmodenfit (Begründung 4.5)

```python
"""FA-W5-2: Drift-Varianten an der Beispieldatei (nur lesend)."""
import sys, pathlib, numpy as np, collections
sys.path.insert(0, "tools/auswertung")
import beispiel_svd
from ldv_automation.auswertung import werte_aus
from ldv_automation.auswertung.annahmen import SchwellenStufe2
from ldv_automation.auswertung.svd_adapter import aus_svd_messung, zeit_s_aus_svd_messung
from ldv_automation.auswertung.vergleich import drift_aus, drift_regression
from ldv_automation.auswertung.modenfit import fit_moden, mobilitaet_des_paars
m = beispiel_svd.lese_svd_werkzeug(pathlib.Path("../Input/20261012_ref_Mitte.svd"))
aw = werte_aus(aus_svd_messung(m), antriebspunkt=("Ref2","Ref1","akzeleranz"))
t = zeit_s_aus_svd_messung(m)
pa = aw.paare[("Ref2","Ref1")]
f = pa.paar.frequenz_hz
Y = mobilitaet_des_paars(pa, "akzeleranz")
sp = pa.spitzen.spitzen
S = SchwellenStufe2()
for f0 in [418.8, 631.2, 1507.8]:
    i = int(np.argmin([abs(s.f_sp_hz - f0) for s in sp]))
    d, fit = drift_aus(aw, t, f0, ("Ref2","Ref1"), schwellen2=SchwellenStufe2(drift_ausschluss=()))
    g = next(g for g in fit.gruppen if i in g.spitzen); mode = g.spitzen.index(i)
    fr = np.array([e.fr_hz[mode] for e in fit.ergebnisse]); P = np.array([e.punkt for e in fit.ergebnisse])
    rho = np.array([e.rho for e in fit.ergebnisse]); kz = [set(e.kennzeichen[mode]) for e in fit.ergebnisse]
    tt = t[P]
    print(f"== {sp[i].f_sp_hz:.3f} Hz, Gruppe {g.f_sp_hz}, Band {f[g.k_von]:.1f}-{f[g.k_bis]:.1f} Hz")
    print("  Kennzeichen:", dict(collections.Counter(k for s in kz for k in s)))
    print(f"  rho: Median {np.median(rho):.3f}, Quantile 10/90 {np.quantile(rho,0.1):.3f}/{np.quantile(rho,0.9):.3f}; corr(rho,t) {np.corrcoef(rho, tt)[0,1]:+.2f}")
    def reg(maske, name):
        ff = np.where(maske, fr, np.nan); dd = drift_regression(ff, tt)
        print(f"  {name:38s} b1 {dd.steigung_hz_h:+.4f} ± {dd.sd_steigung_hz_h:.4f} Hz/h  N={dd.n_punkte} s={dd.streuung_hz:.4f}")
    alle = np.ones(len(fr), bool)
    reg(alle, "Gruppe, ohne Ausschluss")
    reg(np.array([not s & {"nicht_konvergiert","ausserhalb_band"} for s in kz]), "Gruppe, -nk -ab")
    reg(np.array([not s & {"nicht_konvergiert","ausserhalb_band","unsicher"} for s in kz]), "Gruppe, -nk -ab -uns")
    reg(np.array([not s & set(S.drift_ausschluss) for s in kz]), "Gruppe, Voreinstellung (4 Kz)")
    reg(rho <= 0.10, "Gruppe, nur rho<=0,1")
    reg(rho > 0.10, "Gruppe, nur rho>0,1")
    # Einzelmodenfit wie Prüfskript FG-03 (±6 Linien um Stufe-1-Linie, ohne Neusuche je Punkt)
    k = sp[i].k; sel = slice(k-6, k+7)
    fr1, rho1, kz1 = [], [], []
    for p in range(Y.shape[0]):
        r = fit_moden(f[sel], Y[p, sel], [sp[i].f_sp_hz], [0.003])
        fr1.append(r.fr_hz[0]); rho1.append(r.rho)
    fr1 = np.array(fr1); rho1 = np.array(rho1)
    for name, msk in [("Einzelmode, ohne Ausschluss", np.ones(len(fr1), bool)), ("Einzelmode, rho<=0,1", rho1 <= 0.1)]:
        dd = drift_regression(np.where(msk, fr1, np.nan), t)
        print(f"  {name:38s} b1 {dd.steigung_hz_h:+.4f} ± {dd.sd_steigung_hz_h:.4f} Hz/h  N={dd.n_punkte} s={dd.streuung_hz:.4f}  rho Median {np.median(rho1):.3f}")
```

#### drift_631.py – Gruppe 631,6/640,6 Hz: Ursache von nicht_konvergiert

```python
"""FA-W5-2: Warum nicht_konvergiert bei der Gruppe 631,6/640,6 Hz (Ref2/Ref1)?"""
import sys, pathlib, numpy as np, collections
sys.path.insert(0, "tools/auswertung")
import beispiel_svd
from ldv_automation.auswertung import werte_aus
from ldv_automation.auswertung.annahmen import SchwellenStufe2
from ldv_automation.auswertung.svd_adapter import aus_svd_messung, zeit_s_aus_svd_messung
from ldv_automation.auswertung.vergleich import drift_aus, drift_regression
from ldv_automation.auswertung.modenfit import fit_moden, mobilitaet_des_paars
m = beispiel_svd.lese_svd_werkzeug(pathlib.Path("../Input/20261012_ref_Mitte.svd"))
aw = werte_aus(aus_svd_messung(m), antriebspunkt=("Ref2","Ref1","akzeleranz"))
t = zeit_s_aus_svd_messung(m)
pa = aw.paare[("Ref2","Ref1")]; f = pa.paar.frequenz_hz; sp = pa.spitzen.spitzen
Y = mobilitaet_des_paars(pa, "akzeleranz")
i = int(np.argmin([abs(s.f_sp_hz - 631.2) for s in sp])); j = i + 1
print("Stufe1:", sp[i].f_sp_hz, sp[i].breite_3db_hz, sp[i].kennzeichen, "|", sp[j].f_sp_hz, sp[j].breite_3db_hz, sp[j].kennzeichen)
d, fit = drift_aus(aw, t, 631.2, ("Ref2","Ref1"), schwellen2=SchwellenStufe2(drift_ausschluss=()))
g = next(g for g in fit.gruppen if i in g.spitzen)
ab = collections.Counter(); 
kon = [e for e in fit.ergebnisse if "nicht_konvergiert" not in e.kennzeichen[0]]
nk = [e for e in fit.ergebnisse if "nicht_konvergiert" in e.kennzeichen[0]]
for name, L in (("konvergiert", kon), ("nicht_konvergiert", nk)):
    fr = np.array([e.fr_hz for e in L]); z = np.array([e.zeta for e in L]); sd = np.array([e.sd_fr_hz for e in L]); it = [e.iterationen for e in L]
    print(f"{name}: N={len(L)} it median {np.median(it)}; f_r Median {np.median(fr,0)}; zeta Median {np.median(z,0)}; zeta2 min/max {z[:,1].min():.2e}/{z[:,1].max():.2e}; sd_fr Median {np.nanmedian(sd,0)}")
# Abbruchgrund nachrechnen
k = slice(g.k_von, g.k_bis+1); grund = collections.Counter()
S = SchwellenStufe2()
for e in nk[:30]:
    r = fit_moden(f[k], Y[e.punkt, k], [sp[i].f_sp_hz, sp[j].f_sp_hz], [sp[i].zeta, 1.5625/(2*sp[j].f_sp_hz)], max_iter=S.max_iter)
    grund[r.abbruch] += 1
print("Abbruchgruende (30 Fits):", dict(grund))
r = fit_moden(f[k], Y[nk[0].punkt, k], [sp[i].f_sp_hz, sp[j].f_sp_hz], [sp[i].zeta, 1.5625/(2*sp[j].f_sp_hz)], max_iter=2000)
print("mit 2000 Iterationen:", r.abbruch, r.iterationen, r.fr_hz, r.zeta, r.rho, "vorher", nk[0].fr_hz, nk[0].zeta, nk[0].rho)
```

#### rf_v6.py – Sollwerte RF-V6

```python
"""FG-03 RF-V6: Sollwerte des Drift-Ausschlusses je gewählter Mode (K2-1), nur numpy."""
import numpy as np
t = np.arange(20)*120.0; f = 631.7 - 2e-5*t
def reg(maske):
    tt = t[maske] - t[maske].min(); ff = f[maske]
    b1, b0 = np.polyfit(tt, ff, 1); r = ff - (b0 + b1*tt)
    s = np.sqrt(r @ r/(len(tt)-2)); sb = s/np.sqrt(np.sum((tt-tt.mean())**2))
    print(f"N={maske.sum()} b1={b1*3600:.12f} Hz/h sd={sb*3600:.2e} gesamt={b1*tt.max():.12f} Hz rel={b1*tt.max()/b0:.10e} b0={b0:.10f}")
a = np.ones(20, bool); a[[10, 11, 12]] = False; reg(a)      # (a) Gruppe n = 2
b = np.ones(20, bool); b[[0, 1, 2, 10, 11, 12]] = False; reg(b)  # (b) n = 1
```

#### rf_f3_sd.py – Standardabweichungen RF-F3 (K2-3)

```python
"""FA-W5-2: Standardabweichungen des erzwungenen Ein-Moden-Fits RF-F3."""
import numpy as np
from ldv_automation.auswertung.modenfit import fit_moden
def Y(f, fn, z=0.01):
    w = 2*np.pi*f; wn = 2*np.pi*fn; return 1j*w/(wn**2 - w**2 + 2j*z*wn*w)
f = np.arange(180, 230)*0.5
for f2 in (102.0, 103.0):
    h = Y(f, 100.0) + Y(f, f2); k = int(np.argmax(np.abs(h))); sel = slice(k-4, k+5)
    r = fit_moden(f[sel], h[sel], [f[k]], [0.01])
    print(f"f2={f2}: Max bei {f[k]} Hz, fr={r.fr_hz[0]:.4f} sd_fr={r.sd_fr_hz[0]:.4f} Hz (Δf/2=0,25), zeta={r.zeta[0]:.6f} sd_z_rel={r.sd_zeta_rel[0]:.4f}, rho={r.rho:.4f}, abbruch={r.abbruch}")
```

#### gruppe262.py – Gruppe 262,6 Hz: Punktauswahl je Spitze und Fitband (Abschnitt 7)

```python
"""FA-W5-2: Gruppe 262,6 Hz – Punktauswahl je Spitze (Code) vs. gemeinsame (Prüfskript FG-03)."""
import sys, pathlib, numpy as np
sys.path.insert(0, "tools/auswertung")
import beispiel_svd
from ldv_automation.auswertung import werte_aus
from ldv_automation.auswertung.svd_adapter import aus_svd_messung
from ldv_automation.auswertung.modenfit import schaetze_daempfung
m = beispiel_svd.lese_svd_werkzeug(pathlib.Path("../Input/20261012_ref_Mitte.svd"))
aw = werte_aus(aus_svd_messung(m))
pa = aw.paare[("Vib Z", "Ref1")]; sp = pa.spitzen.spitzen; f = pa.paar.frequenz_hz
wahl = [int(np.argmin([abs(s.f_sp_hz - x) for s in sp])) for x in (262.6, 618.9)]
r = schaetze_daempfung(aw, ("Vib Z", "Ref1"), spitzen=wahl)
for z in r.zusammenfassung:
    print(f"Code  {z.f_sp_hz:8.3f}: fr {z.fr_median_hz:.3f} zeta {z.zeta_median:.5f} rho {z.rho_median:.4f} N {z.n_punkte}")
k = int(np.argmin(abs(f - 262.5))); top = np.argsort(np.abs(pa.frf.h1[:, k]))[::-1][:20]
r2 = schaetze_daempfung(aw, ("Vib Z", "Ref1"), spitzen=wahl[:1], punkte=[int(p) for p in top])
for z in r2.zusammenfassung:
    print(f"Top20@262,5 {z.f_sp_hz:8.3f}: fr {z.fr_median_hz:.3f} zeta {z.zeta_median:.5f} rho {z.rho_median:.4f} N {z.n_punkte}")
rh = [e.rho for e in r2.ergebnisse]; print("rho alle 20 (Gruppe) Median", np.median(rh))
g618 = next(g for g in r.gruppen if wahl[1] in g.spitzen)
e618 = [e for e in r.ergebnisse if e.gruppe == g618.nummer]
print("618,9: rho Median alle", np.median([e.rho for e in e618]), "Kennzeichen", [e.kennzeichen[0] for e in e618 if e.kennzeichen[0]])
g = next(g for g in r.gruppen if wahl[0] in g.spitzen)
print("Code-Fitband Gruppe 262:", f[g.k_von], "-", f[g.k_bis], "Hz,", g.k_bis - g.k_von + 1, "Linien")
```

---

## Änderungsprotokoll

| Datum | Änderung | Freigabe |
|---|---|---|
| 2026-10-30 | Erstfassung (Paket W4-2) | Nutzer, 2026-10-30 (mit E1–E6) |
| 2026-10-30 | Korrektur K2 aus der Fachabnahme FA-W5-2: K2-1 Option A – Drift-Ausschluss je gewählter Mode (`ausserhalb_band`, `unsicher`, `nicht_konvergiert` nur bei n = 1; kein Ausschluss über `modell_passt_nicht`, Anzahl wird ausgegeben), Gruppenfit nach 3.3 in der Drift, Drift-Tabelle in 7 ersetzt (4.5, 6.2, 6.3, 7, RF-V6). K2-2: Abbruchkriterium auch für verworfene Versuchsschritte (3.2, RF-F1). K2-3: σ der Spitzenpaarung = Median der σ_fr, Hinweis zur Drift (4.2, RF-V7); RF-F3 bei 102 Hz zusätzlich `unsicher` (9.1); Abschnitt 7 mit Punktauswahl je Spitze und ρ als Median der verwendeten Punkte. K2-4: γ² = NaN bleibt im Fit, Hinweis „Kohärenz nicht prüfbar“ (3.2, 6.3, RF-F8). Prüfskripte im Anhang (Ergänzung K2) | Nutzer, 2026-10-30 |
