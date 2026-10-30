<!-- Fachgrundlage FG-02: Auswertung Stufe 1 (R-050 bis R-053 sowie B-2, B-3, B-9, B-10 und fachliche Festlegungen zu B-4, B-6, B-7). Erstellt im Paket W4-1 von strukturdynamik-experte, Stand 2026-10-29, Korrektur K1 eingearbeitet 2026-10-30. -->

> **Status:** Vom Nutzer am 2026-10-29 freigegeben, einschließlich der Toleranzen (Abschnitt 8) und Schwellen (γ²_min = 0,9, n_min = 3, Nachbarmode 3B, P-07 bis P-09). Annahmen M1–M11 werden nach der Prüfung am Messrechner (Mo 2026-11-02) nachgeführt.
> **Korrektur K1** (`FG-02_korrekturvorschlag-K1.md`, K1-1 bis K1-8) am 2026-10-30 eingearbeitet, Nutzerfreigabe; Änderungen siehe Änderungsprotokoll am Ende.

# FG-02 – Auswertung von PSV-Messdaten, Stufe 1

## 1 Zweck und Umfang

Diese Fachgrundlage legt fest, was die Auswertesoftware (Paket W5) aus den Daten einer
PSV-Messdatei berechnet. Für jede Größe stehen hier Definition, Formel, Einheit,
Konvention, Gültigkeitsgrenzen und Datenvertrag. Die analytischen Referenzfälle in
Abschnitt 9 werden zu Tests.

| Punkt | Inhalt | Abschnitt |
|---|---|---|
| A-1 | Phasen- und Vorzeichenkonvention, Konjugations- und Vorzeichenparameter | 2, 8 |
| A-2 / R-050 | Spektren je Punkt: kohärent (\|CPH\|) und Leistungsmittel (√AP), getrennt benannt | 3.1 |
| A-3, B-9 / R-050 | Punktmittel: Betragsmittel (PSV-konform) und quadratisches Mittel | 3.2 |
| A-4 / R-051 | H1, H2, γ² | 3.3 |
| B-2 | Zufallsfehler von \|H1\|, Phase und γ² | 3.4 |
| B-3 | Kohärenzschwelle, Maskierung, Gewichte | 3.5 |
| A-5 / R-052 | Betriebsschwingform, 3D-Betrag, Bahnellipse | 3.6 |
| B-10 | Umrechnung Weg/Schnelle/Beschleunigung | 3.7 |
| A-7 / R-053 | Band-Effektivwerte inkl. Bandgrenzen und $W_\mathrm{RBW}$ | 3.8 |
| A-6 / R-053 | Spitzensuche auf H1, −3-dB-Breite, Warnkriterien | 3.9 |
| B-4 | Plausibilitätsprüfungen mit Schwellen | 4 |
| B-7, B-6 | Fachlicher Inhalt von Export und Abbildungen | 5 |
| A-8 | Frequenzachse | 2.3 |

**Nicht enthalten (Stufe 2):** parametrische Dämpfungsschätzung (B-1), Vergleich mehrerer
Messungen (B-5), Normal- und Tangentialzerlegung (B-8), flächengewichtete Punktmittel.

**Kennzeichnung der Belege:**
- **[H]**: Herstellerangabe Polytec, Fundstelle über W1/I2.
- **[D]**: an der Datei `Input/20261012_ref_Mitte.svd` geprüft (W2, W3 oder hier).
- **[A]**: eigene Herleitung, vollständig im Text.
- **[N]**: numerisch im Prüfskript (Anhang) nachgerechnet.
- **[L-m]**: Literatur mit Prüfstand `metadaten`, Inhalt nicht gelesen, also noch nicht belegt.
- **[ANN]**: einstellbare Annahme, bis zur Klärung am Messrechner (Abschnitt 11) gekennzeichnet.

---

## 2 Konventionen

### 2.1 Zeit, Spektrum, Skalierung

- **Zeitabhängigkeit** $e^{+i\omega t}$. Ein reales Signal mit komplexer Amplitude
  $\hat x$ ist $x(t) = \mathrm{Re}\{\hat x\,e^{i\omega t}\} = \lvert\hat x\rvert\cos(\omega t + \arg\hat x)$
  (KONVENTIONEN; TM S. 9–10 über I2 [H]).
- **Spektren** sind einseitig und amplitudentreu auf den **Spitzenwert** (0-to-peak)
  skaliert. Für ein Zeitsignal $x_n$ mit Fenster $w_n$ ($n = 0 \dots N-1$) gilt bei Linie $k \ge 1$:
  $$\hat X_k = \frac{2}{\sum_n w_n}\sum_{n=0}^{N-1} w_n\,x_n\,e^{-i2\pi kn/N}\qquad[\text{Einheit von }x].$$
  Ein Sinus der Amplitude $A$ auf Linie $k_0$ ergibt $\hat X_{k_0} = A\,e^{i\varphi}$ für
  Rechteck- und Hann-Fenster (RF-S1 [N]). Die Software rechnet keine Spektren aus Zeitdaten.
  Die Formel definiert, was die Dateigrößen bedeuten, und erzeugt die Testdaten.
- **Effektivwert** einer Linie: $\lvert\hat X_k\rvert/\sqrt2$. Er wird nur bei der Anzeige
  umgerechnet, gespeichert wird der Spitzenwert.

### 2.2 Kreuz- und Autospektren

Mit $\langle\cdot\rangle$ als Mittel über die $n_d$ Blöcke einer Messung:

| Größe | Definition | Einheit | Beleg |
|---|---|---|---|
| $\mathrm{AP}_a$ | $\langle\lvert\hat A\rvert^2\rangle$ | $[a]^2$ (Spitzenwert²) | TM S. 14 über I2 [H]; W2 [D] |
| $\mathrm{CP}_{ab}$ | $\langle\hat A\,\hat B^{*}\rangle$, **a = Antwort, b = Referenz** | $[a]\,[b]$ | W3 2.2 [D, A]; TM $\mathrm{CP}_{RV} = R^{*}V$ |
| $\mathrm{ABS}_a$ | $\langle\lvert\hat A\rvert\rangle$ | $[a]$ | W2 [D] |
| $\mathrm{CPH}_{ab}$ | Antwort mit Phase relativ zur Referenz; in der Datei $\lvert\mathrm{CPH}\rvert = \lvert\mathrm{CP}\rvert/\sqrt{\mathrm{AP}_b}$ auf 0,6 % | $[a]$ | W2, W3 [D] |

Der quadratische Mittelwert der Linie ist $\mathrm{AP}/2$, der Effektivwert $\sqrt{\mathrm{AP}/2}$.

### 2.3 Frequenzachse [ANN M2]

$f_k = (k + k_0)\,\Delta f$ für den Array-Index $k = 0 \dots K-1$, $\Delta f = BW/n_\mathrm{FFT}$.
Voreinstellung $k_0 = 1$, die erste Linie liegt also bei $\Delta f$ und DC fehlt (KONVENTIONEN,
vorläufig). Die Achse kommt immer aus der Datei. $k_0$ ist ein Parameter mit Kennzeichen
„M2 unbestätigt“. Für die Datei gilt $\Delta f = 1{,}5625$ Hz und $K = 1600$.

### 2.4 Vorzeichen und Konjugation (A-1)

Die Rohdaten aus der Datei werden vor jeder Rechnung so verarbeitet:

$$\mathrm{CP}_{ab} \leftarrow s_a s_b\cdot\mathcal C(\mathrm{CP}^\mathrm{roh}_{ab}),\qquad
\mathrm{CPH}_{ab} \leftarrow s_a s_b\cdot\mathcal C(\mathrm{CPH}^\mathrm{roh}_{ab}),\qquad \mathrm{AP},\ \mathrm{ABS}\ \text{unverändert}.$$

- $s_c \in \{+1, -1\}$ ist das **Vorzeichen je Kanal** c (Parameter `vorzeichen_kanal`)
  **[ANN M8]**, Voreinstellung $+1$. Für Vib X/Y/Z bleibt $s_c = +1$ (Richtungskonvention
  KONVENTIONEN). Es gilt für jedes Kreuzspektrum, in dem der Kanal vorkommt, als Antwort
  **oder** als Referenz [A]: $\langle (s_aA)(s_bB)^{*}\rangle = s_a s_b\langle AB^{*}\rangle$.
  Beispiel: Ref2 ist Antwort in Ref2/Ref1 und Referenz in Vib/Ref2; ein gedrehter Ref2 wird
  nur mit $s_{\mathrm{Ref2}}$ in **beiden** Paaren korrigiert (K1-1).
  Ein gedrehter Kraftsensor verschiebt alle H1-Phasen und Schwingformen global um π.
- $\mathcal C$ ist die Identität (Voreinstellung) oder die komplexe Konjugation (Parameter
  `konjugieren`). Die Datei ist nach dem Kausalitätstest **nicht** konjugiert (W3 2.2 [D]).
  Ob PSV die Phase genauso anzeigt, ist offen **[ANN M1]**.
- Beide Parameter und ihr Status („Annahme“ oder „bestätigt am …“) gehören in alle Ausgaben
  und Exporte.

### 2.5 Indizes, Formen, Einheiten

- Punktindex $p = 0 \dots P-1$ (0-basiert), Linienindex $k = 0 \dots K-1$. Das Label führt der
  Adapter getrennt (KONVENTIONEN).
- Arrays haben die Form `(P, K)`. 3D-Größen haben die Form `(P, 3, K)` mit der
  Komponentenreihenfolge X, Y, Z.
- Typen: `float64` bzw. `complex128`. Phasen in rad, Frequenz in Hz, Kreisfrequenz
  $\omega_k = 2\pi f_k$ in rad/s.
- SI-Einheiten: Schnelle m/s, Kraft N, Beschleunigung m/s², Weg m.

---

## 3 Auswertungen

### 3.1 Spektren je Punkt (A-2, R-050)

Beide Spektren werden **immer getrennt und benannt** ausgegeben:

| Name im Code (Vorschlag) | Formel | Einheit | Bedeutung |
|---|---|---|---|
| `spektrum_kohaerent` | $\mathrm{CPH}_{ab}$ (komplex), Betrag $\lvert\mathrm{CPH}_{ab}\rvert$ | $[a]$, Spitzenwert | Anteil der Antwort, der mit Referenz b kohärent ist; Phase relativ zu b; entspricht der PSV-Anzeige „Geschwindigkeit“ (W2 [D]) |
| `spektrum_leistung` | $\sqrt{\mathrm{AP}_a}$ (reell) | $[a]$, Spitzenwert | quadratisch gemittelter Betrag aller Blöcke, **mit** Rauschen und unkorrelierten Anteilen; ohne Phase |

- **Beziehung:** $\lvert\mathrm{CPH}\rvert \le \sqrt{\mathrm{AP}_a}$. Ist
  $\mathrm{CPH} = \mathrm{CP}/\sqrt{\mathrm{AP}_b}$, gilt
  $\lvert\mathrm{CPH}\rvert = \gamma_{ab}\sqrt{\mathrm{AP}_a}$ [A]: Aus
  $\lvert\mathrm{CPH}\rvert^2 = \lvert\mathrm{CP}\rvert^2/\mathrm{AP}_b$ und
  $\gamma^2 = \lvert\mathrm{CP}\rvert^2/(\mathrm{AP}_a\mathrm{AP}_b)$ folgt
  $\lvert\mathrm{CPH}\rvert^2 = \gamma^2\,\mathrm{AP}_a$.
- **Ohne Referenz:** nur `spektrum_leistung`; `spektrum_kohaerent` ist nicht vorhanden (kein NaN-Array).
- **CPH fehlt, Referenz vorhanden:** Ersatz $\mathrm{CP}/\sqrt{\mathrm{AP}_b}$ mit Kennzeichen
  „CPH berechnet“. Das ist exakt nur bei konstanter Referenzamplitude über die Blöcke.
- **3D-Betrag je Linie** (PSV-Konvention, I2 3.8 [H]):
  $\lvert\cdot\rvert_\mathrm{3D} = \sqrt{\sum_{c\in\{X,Y,Z\}}\lvert\mathrm{CPH}_c\rvert^2}$ bzw.
  $\sqrt{\sum_c \mathrm{AP}_c}$.

### 3.2 Punktmittel (A-3, B-9, R-050)

Über die Menge $\mathcal P$ der **gültigen** Punkte mit $n_\mathcal P = \lvert\mathcal P\rvert$ und
je Linie:

$$M^\mathrm{Betrag}_k = \frac{1}{n_\mathcal P}\sum_{p\in\mathcal P} \lvert X_{pk}\rvert,\qquad
M^\mathrm{quadr}_k = \sqrt{\frac{1}{n_\mathcal P}\sum_{p\in\mathcal P} \lvert X_{pk}\rvert^2}.$$

| Eingang $X$ | PSV-konform (Name) | Zusätzlich |
|---|---|---|
| CPH, ABS, \|H1\|, \|H2\|, \|CP\| | $M^\mathrm{Betrag}$ (`mittel_betrag`), wie die PSV-Punktmittel `AVGSEQ[ABS[…]]` (W2 [D]) | $M^\mathrm{quadr}$ (`mittel_quadratisch`) |
| AP | $\frac{1}{n_\mathcal P}\sum \mathrm{AP}$ (PSV `AVGSEQ[AVG[AP]]`) | – |
| √AP (`spektrum_leistung`) | $M^\mathrm{quadr}(\sqrt{\mathrm{AP}}) = \sqrt{\overline{\mathrm{AP}}}$ ist **identisch** zum PSV-Mittel von AP | $M^\mathrm{Betrag}(\sqrt{\mathrm{AP}})$ |
| γ² | arithmetisches Mittel (PSV `AVGSEQ[COH]`) | – |

- Es gilt $\lvert\text{komplexes Mittel}\rvert \le M^\mathrm{Betrag} \le M^\mathrm{quadr}$ [A]
  (Dreiecksungleichung, Ungleichung zwischen arithmetischem und quadratischem Mittel).
- Das komplexe Punktmittel gehört nicht zu Stufe 1. An Knotenlinien löscht es sich aus
  (W3 [D]).
- **Gültige Punkte [ANN M6]:** PSV lässt ungültige Punkte weg (W1 [H]). Solange die
  Statusbits nicht gedeutet sind, gelten alle Punkte als gültig, mit Kennzeichen. Die Menge
  $\mathcal P$ ist Parameter.
- Alle Gewichte sind gleich, denn ein flächengewichtetes Mittel gehört zu Stufe 2.
- NaN-Linien eines Punkts werden nicht mitgezählt (`nanmean`), und je Linie wird $n$
  ausgegeben. Ist $n = 0$, ist das Ergebnis NaN.

### 3.3 H1, H2, Kohärenz (A-4, R-051)

$$H_1 = \frac{\mathrm{CP}_{ab}}{\mathrm{AP}_b},\qquad
H_2 = \frac{\mathrm{AP}_a}{\mathrm{CP}_{ab}^{*}},\qquad
\gamma^2_{ab} = \frac{\lvert\mathrm{CP}_{ab}\rvert^2}{\mathrm{AP}_a\,\mathrm{AP}_b} = \frac{H_1}{H_2}\in[0,1].$$

- **Einheit** $[a]/[b]$: Vib/Ref1 in (m/s)/N (Mobilität), Ref2/Ref1 in (m/s²)/N
  (Akzeleranz), Vib/Ref2 in s.
- $\arg H_1 = \arg H_2 = \arg\mathrm{CP}_{ab}$ [A]. $\lvert H_1\rvert \le \lvert H_2\rvert$.
- Die Definitionen sind mit TM S. 14–15 identisch (über I2 [H]). Ihre Beträge reproduzieren
  die PSV-Punktmittel (W2 [D], Abweichung ≤ 9,3·10⁻⁷).
- **Rauschmodell** [A] (I2 3.4 nachgerechnet; Signal $S_x$, unkorreliertes Rauschen $N_R$
  am Eingang und $N_V$ am Ausgang):
  - $H_1 = H\,S_x/(S_x+N_R)$, unbeeinflusst von $N_V$.
  - $H_2 = H\,(\lvert H\rvert^2 S_x + N_V)/(\lvert H\rvert^2 S_x)$, unbeeinflusst von $N_R$.
  - $\gamma^2 = \frac{S_x}{S_x+N_R}\cdot\frac{\lvert H\rvert^2 S_x}{\lvert H\rvert^2S_x + N_V}$.
- **Ohne Mittelung** ($n_d = 1$) ist $\gamma^2 \equiv 1$ ohne Aussage. Dann wird γ² als NaN
  ausgegeben, und H1 wird als „FRF“ bezeichnet (TM 3-5 über W1 [H]).

### 3.4 Zufallsfehler (B-2)

Normierte Zufallsfehler (Standardabweichung/Erwartungswert) nach der Näherung erster
Ordnung, wie sie Bendat/Piersol angeben **[L-m, Volltext nicht gelesen]**:

$$\varepsilon\big[\lvert\hat H_1\rvert\big] \approx \frac{\sqrt{1-\gamma^2}}{\lvert\gamma\rvert\sqrt{2n_d}},\qquad
\sigma\big[\arg\hat H_1\big] \approx \varepsilon\big[\lvert\hat H_1\rvert\big]\ \text{rad},\qquad
\varepsilon\big[\hat\gamma^2\big] \approx \frac{\sqrt2\,(1-\gamma^2)}{\lvert\gamma\rvert\sqrt{n_d}}.$$

- **Eigene Prüfung [N]:** Monte-Carlo-Rechnung mit Gaußschen Blöcken und Rauschen am
  Ausgang, 40 000 Wiederholungen. Bei $n_d = 25$ treffen die Formeln auf ±6 %. Bei
  $n_d = 7$ unterschätzen sie um bis zu 8 % (|H1|) bzw. 18 % (γ² bei γ² = 0,99).
  Das ist für einen Hinweis auf die Messunsicherheit ausreichend, nicht für statistische Tests.
- **Erwartungstreue von γ̂² [N]:** Bei wahrem γ² = 0 gilt $E[\hat\gamma^2] = 1/n_d$, das
  95-%-Quantil ist $1-0{,}05^{1/(n_d-1)}$ (bei $n_d = 7$: 0,393; MC: 0,394).
- **Ausgabe:** `eps_betrag_h1`, `sigma_phase_h1_rad`, `eps_kohaerenz` je Punkt und Linie,
  dazu als Band mit oberer Grenze $\lvert\hat H_1\rvert\,(1 + k_\varepsilon\,\varepsilon)$ und
  unterer Grenze $\max\big(0,\ \lvert\hat H_1\rvert\,(1 - k_\varepsilon\,\varepsilon)\big)$.
  Ist $k_\varepsilon\,\varepsilon \ge 1$, gilt das Kennzeichen „Fehlerband nicht aussagekräftig“
  (K1-6): Ein Betrag kann nicht negativ sein. Bei $n_d = 7$ und $k_\varepsilon = 2$ betrifft das
  γ² < 0,222 (ε > 0,5) [N]. $k_\varepsilon = 2$, einstellbar.
- **Mittelungsanzahl $n_d$ [ANN M5]:** In der Datei vermutlich 7, je Punkt eventuell
  7 bis 25 (Signal Enhancement, W2 3.2). Parameter, Voreinstellung aus `Average`, Kennzeichen.
- **Grenzen:** Die Formeln setzen unabhängige Blöcke und stationäre Zufallssignale voraus.
  Sie erfassen **keine** systematischen Fehler wie Leckage durch nicht abgeklungene
  Burst-Antwort, Auflösungsbias oder Nichtlinearität (W3 2.5). Das wird bei der Ausgabe
  vermerkt.
- **Randfälle:** γ² = 0 → ε = +∞. γ² = 1 → ε = 0. γ² = NaN → NaN. $n_d < 2$ → NaN mit Hinweis.

### 3.5 Kohärenzschwelle, Maske, Gewichte (B-3)

- **Schwelle** $\gamma^2_\mathrm{min}$, **Vorschlag 0,9**, einstellbar. Begründung [N]:
  - Bei $n_d = 7$ beträgt der Zufallsfehler von |H1| dann etwa 9 % (Formel 0,089, MC 0,096).
  - Die Schwelle liegt weit über dem 95-%-Quantil von 0,393, das schon reines Rauschen
    erreichen kann.
- **Maske** `kohaerenz_ok = γ² ≥ γ²_min`. Linien unter der Schwelle werden **gekennzeichnet,
  nicht gelöscht**. Spektren und FRF bleiben vollständig, damit sie mit PSV vergleichbar sind.
- **Gewicht** (inverse Varianz von |H1|): $w = 1/\varepsilon^2 = 2n_d\,\gamma^2/(1-\gamma^2)$;
  für die Rechnung γ² auf ≤ 1 − 10⁻⁶ begrenzen.
- **Verwendung in Stufe 1:**
  - Maske in Spitzensuche und −3-dB-Breite (3.9) und in den Plausibilitätsprüfungen (4).
  - Gewichte werden ausgegeben (für Stufe 2 und für Mittel wiederholter Schätzungen
    **derselben** Größe).
  - **Nicht** für räumliche Punktmittel: Verschiedene Punkte sind verschiedene Größen. Eine
    Gewichtung nach Kohärenz würde Punkte mit großer Antwort bevorzugen und das Mittel
    verfälschen [A/E].

### 3.6 Betriebsschwingform (A-5, R-052)

- **Linienwahl:** $k^\ast = \arg\min_k\lvert f_k - f_\mathrm{wahl}\rvert$. Bei Gleichstand gilt die
  kleinere Linie. Ausgegeben wird $f_{k^\ast}$. Liegt $f_\mathrm{wahl}$ außerhalb
  $[f_0 - \Delta f/2,\ f_{K-1} + \Delta f/2]$, folgt `ValueError`.
- **Komplexe Amplitude** je Punkt p und Komponente c:
  - Voreinstellung `quelle="cph"`: $\hat v_{pc} = \mathrm{CPH}_{pc,k^\ast}$ in m/s (Spitzenwert).
  - Option `quelle="h1"`: $\hat v_{pc} = H_{1,pc,k^\ast}$ in (m/s)/N.
  - In beiden Fällen ist die Phase auf die Referenz bezogen. H1 empfiehlt sich, wenn die
    Anregung von Punkt zu Punkt schwankt (TM 7-1 über I2 [H]).
- **Momentanwert** für die Animation: $u_{pc}(\theta) = \mathrm{Re}\{\hat v_{pc}\,e^{i\theta}\}$ mit
  $\theta = \omega t \in [0, 2\pi)$.
- **Ohne Referenz oder Trigger** [R-052]: nur $\sqrt{\mathrm{AP}_{pc}}$ als Betrag, mit
  `phase_gueltig = False`. Es wird keine Animation mit Vorzeichen gebildet.
- **3D-Kennwerte je Punkt** [A] (Herleitung W3 2.4):
  - `betrag_3d_psv` = $\sqrt{\sum_c\lvert\hat v_c\rvert^2}$ (PSV-Konvention).
  - `auslenkung_max` = $\sqrt{\tfrac12\big(\sum_c\lvert\hat v_c\rvert^2 + \lvert\sum_c \hat v_c^2\rvert\big)}$.
  - `auslenkung_min` = $\sqrt{\max\big(0,\ \tfrac12(\sum_c\lvert\hat v_c\rvert^2 - \lvert\sum_c\hat v_c^2\rvert)\big)}$.
  - Es gilt $\text{min} \le \text{max} \le \text{betrag\_3d\_psv}$. Gleichheit von max und PSV-Betrag
    gilt bei gleichphasigen Komponenten (lineare Bahn).
- Das globale Vorzeichen hängt von $s_a s_b$ ab (2.4). Die Form selbst nicht.

### 3.7 Umrechnung Weg/Schnelle/Beschleunigung (B-10)

Je Linie mit $\omega_k = 2\pi f_k$ [A]:

$$\hat d = \frac{\hat v}{i\omega_k}\ [\mathrm m],\qquad \hat a = i\omega_k\,\hat v\ [\mathrm{m/s^2}];\qquad
\text{Rezeptanz} = \frac{\text{Mobilität}}{i\omega_k}\ [\mathrm{m/N}],\quad \text{Akzeleranz} = i\omega_k\cdot\text{Mobilität}\ [\mathrm{(m/s^2)/N}].$$

- Weg eilt der Schnelle um π/2 nach, Beschleunigung um π/2 vor.
- Für Autospektren gilt $\mathrm{AP}_d = \mathrm{AP}_v/\omega_k^2$ und $\mathrm{AP}_a = \omega_k^2\,\mathrm{AP}_v$.
- Bei $\omega_k = 0$ (nur bei $k_0 = 0$) ist der Weg NaN.
- Band-Effektivwerte umgerechneter Größen werden aus den umgerechneten Linien gebildet, nicht
  durch Umrechnung des Bandwerts.
- Die Spitzensuche (3.9) läuft immer auf der FRF in der gemessenen Form, also der Mobilität.

### 3.8 Band-Effektivwerte (A-7, R-053)

**Bandzugehörigkeit:** Linie k gehört zum Band $[f_u, f_o]$, wenn
$f_u - 10^{-6}\Delta f \le f_k \le f_o + 10^{-6}\Delta f$. Das Band ist also geschlossen, beide
Grenzlinien zählen mit **[ANN M10]**. PSV verlangt Bandgrenzen auf FFT-Linien (SWP 4-14 über I2 [H]).
Ob PSV beide Grenzlinien einschließt, ist am Gerät zu prüfen.

| Ausgabe | Formel | Einheit | Bemerkung |
|---|---|---|---|
| `rms` (physikalisch) | $\sqrt{\sum_{k\in\text{Band}}\mathrm{AP}_k / (2W_\mathrm{RBW})}$ bzw. $\sqrt{\sum\lvert\hat X_k\rvert^2/(2W_\mathrm{RBW})}$ | $[a]$ effektiv | TM Gl. 3.17 über I2 [H]; für Leistungs- bzw. kohärentes Spektrum |
| `rms_psv` | $\sqrt{\sum\lvert\hat X_k\rvert^2/2}$ (für CPH, ABS) bzw. $\sum \mathrm{AP}_k/2$ (für AP, **quadratischer** Mittelwert, ohne Wurzel) | wie PSV | stimmt mit den PSV-Banddaten der Datei überein (W2 [D]) |
| `bandnorm` (FRF) | $\sqrt{\sum\lvert H_k\rvert^2/2}$ | $[a]/[b]$ | für H1 an der Datei bestätigt (S17 = 0,01851376 = eigene Rechnung [D]); **kein** physikalischer Effektivwert, so kennzeichnen |

- $W_\mathrm{RBW} = N\sum w_n^2/(\sum w_n)^2$: Rechteck 1, Hann 1,5 [N].
- $W_\mathrm{RBW}$ ist ein Parameter **[ANN M5]**, Voreinstellung 1 (Rechteck), mit Kennzeichen.
  Bei $W_\mathrm{RBW} = 1$ sind `rms` und `rms_psv` gleich.
- DC ist nicht enthalten (TM 3-8 über I2 [H]).
- **Leeres Band** (keine Linie im Intervall): NaN und Hinweis „leeres Band“.
- $f_u > f_o$: `ValueError`.
- Band ganz außerhalb der Achse: leeres Band. Band teilweise außerhalb: Es zählen nur die
  vorhandenen Linien, mit Hinweis „Band abgeschnitten“.
- **Gültigkeit:** Exakt (Parseval) für Signalanteile auf Linien. Liegt ein Sinus zwischen
  Linien, geht beim Rechteckfenster Energie außerhalb eines schmalen Bands verloren
  (RF-B4: −3,0 % bei ±3 Linien). Beim Hann-Fenster ist der Fehler vernachlässigbar (RF-B5).

### 3.9 Spitzensuche und −3-dB-Breite (A-6, R-053)

**Eingang:** $y_k = \lvert H_{1,k}\rvert$ eines Punkts oder eines Punktmittels
($M^\mathrm{Betrag}$ von |H1|), dazu γ² und der Parametersatz. Für ein Punktmittel ist γ² das
**arithmetische Punktmittel** von γ² des Paars (wie PSV `AVGSEQ[COH]`, K1-7a).

**Schritt 1 – Kandidaten.** Linie k ist Spitze, wenn
- $y_k > y_{k-1}$ und $y_k \ge y_{k+1}$ für $1 \le k \le K-2$ gilt (Randlinien nie),
- $y_k \ge p_\mathrm{min}\cdot\max\big(\min_{j\in[k-W,k)} y_j,\ \min_{j\in(k,k+W]} y_j\big)$ gilt
  (Prominenz),
- und $f_k \ge f_\mathrm{min}$ ist.

Vorschlag $p_\mathrm{min} = 2$, $W = 20$ Linien, $f_\mathrm{min} = f_0$; alle Werte sind
einstellbar und betreffen nur die Auswahl, nicht die Kennwerte. W ist in Linien angegeben,
die Fensterbreite in Hz hängt also von Δf ab. Bei Δf = 1,5625 Hz sind es ±31 Hz. Bei sehr
feiner Auflösung findet das Kriterium breite Spitzen nicht mehr (geprüft [N]: Δf = 0,05 Hz,
B = 2 Hz → keine Spitze). Eine Angabe in Hz oder in Vielfachen von B ist eine Alternative
für W5 (offener Punkt 5).

**Schritt 2 – Frequenz und Höhe** durch eine Parabel durch drei Linien [A]:
$$\delta = \frac{1}{2}\,\frac{y_{k-1}-y_{k+1}}{y_{k-1}-2y_k+y_{k+1}},\quad
f_\mathrm{sp} = f_k + \delta\,\Delta f,\quad
\hat y = y_k - \tfrac14\,(y_{k-1}-y_{k+1})\,\delta .$$
Ist der Nenner ≥ 0 (keine nach unten offene Parabel), gilt δ = 0 und $\hat y = y_k$.

**Schritt 3 – −3-dB-Breite.**
- Schwelle $y_\mathrm{s} = \hat y/\sqrt2$.
- Von k nach links gehen, bis $y_j < y_\mathrm{s}$ ist. Die Kreuzung $f_l$ wird linear zwischen
  $j$ und $j+1$ interpoliert. Rechts entsprechend $f_r$.
- Erreicht die Suche vorher ein lokales Minimum mit $y \ge y_\mathrm{s}$, ist diese Seite nicht
  bestimmt: Kennzeichen `ueberlappend`, $B$ = NaN.
- Ergebnis: $B = f_r - f_l$ [Hz], $Q = f_\mathrm{sp}/B$, $\zeta = B/(2f_\mathrm{sp})$, wie PSV
  (HB 9-11 über W1 [H]). Der Ausgabename ist `breite_3db_hz`, nicht „Dämpfung“.

**Herleitung der Gültigkeit [A].** Für die Mobilität des Einmassenschwingers
$Y = i\omega/(k - m\omega^2 + ic\omega)$ gilt $\lvert Y\rvert^{-2} = c^2 + (k/\omega - m\omega)^2$.
- Das Maximum liegt bei $\omega_n = \sqrt{k/m}$ mit $\lvert Y\rvert_\mathrm{max} = 1/c$.
- Halbe Leistung heißt $(k/\omega - m\omega)^2 = c^2$, also $m\omega^2 \pm c\omega - k = 0$.
- Daraus folgt $\omega_2 - \omega_1 = c/m = 2\zeta\omega_n$ **exakt für jedes ζ**, und
  $\omega_1\omega_2 = \omega_n^2$.

Für die Mobilität sind $B = 2\zeta f_n$ und $f_\mathrm{sp} = f_n$ deshalb exakt. Fehler
entstehen nur aus Diskretisierung, Nachbarmoden, Rauschen und Leckage. Für Rezeptanz und
Akzeleranz gilt die Beziehung nur näherungsweise (I2 FG-04 [N]).

**Diskretisierungsfehler [N]** (Einmassenschwinger, Lage der Resonanz relativ zum Raster
gleichverteilt, 50 Lagen):

| $B/\Delta f$ | max. \|Fehler $f_\mathrm{sp}$\| | Fehler von $B$ (min … max) |
|---|---|---|
| 0,64 | 0,2012 Δf | +31,64 % … +177,53 % |
| 1,0 | 0,1633 Δf | +5,96 % … +88,23 % |
| 1,5 | 0,1195 Δf | −2,37 % … +39,34 % |
| 2,0 | 0,0877 Δf | +0,04 % … +18,31 % |
| 3,0 | 0,0508 Δf | +2,56 % … +5,21 % |
| 4,0 | 0,0322 Δf | +0,05 % … +3,25 % |
| 6,0 | 0,0160 Δf | +0,01 % … +1,11 % |
| 8,0 | 0,0095 Δf | +0,0006 % … +0,54 % |

Werte in voller Stellenzahl aus dem Prüfskript nachgerechnet (K1-3, FA-W5-1).

Ohne Parabel (Höhe = Linienmaximum) sind die Fehler etwa doppelt so groß, bei $f_\mathrm{sp}$
bis 0,5 Δf.

**Warnkennzeichen je Spitze:**

| Kennzeichen | Bedingung | Begründung |
|---|---|---|
| `aufloesungsbegrenzt` | $B/\Delta f < n_\mathrm{min}$, **Vorschlag $n_\mathrm{min} = 3$** | Ab drei Linien beträgt der Fehler von B höchstens +5,21 % (Tabelle) |
| `ueberlappend` | eine Seite nicht bestimmt (Schritt 3) | Halbwertsbreite einer Einzelmode nicht definiert |
| `nachbarmode` | Abstand zur nächsten gefundenen Spitze $< 3B$ | RF-M: ab 3 B Fehler ≤ 0,5 % (untere Mode) bzw. +0,5 % (obere); bei 1,5 B +2,4 % / +3,5 % |
| `kohaerenz_niedrig` | ein $\gamma^2_k < \gamma^2_\mathrm{min}$ für $f_l \le f_k \le f_r$ oder an der Spitzenlinie; ist eine Seite unbestimmt, zählt der Bereich bis zur Spitzenlinie. γ² = NaN löst das Kennzeichen nicht aus. Ist γ² im geprüften Bereich **vollständig** NaN (z. B. $n_d = 1$) oder fehlt γ², gilt der Hinweis „Kohärenz nicht prüfbar“ (K1-7b) | 3.5 |
| `gueltigkeit_offen_m7` | $f_\mathrm{sp} > 1000$ Hz, solange M7 offen **[ANN M7]** | W3 2.6 |

**Grenze:** Zwei Moden, die enger beieinander liegen als etwa B, erscheinen als **eine**
Spitze ohne Kennzeichen (RF-M1: 0,5 B Abstand ergibt +52 % Breite). Das ist eine Grenze des
Verfahrens und muss in der Ausgabe dokumentiert sein.

---

## 4 Plausibilitätsprüfungen beim Einlesen (B-4)

Die Schwellen sind Vorschläge und einstellbar. Ergebnis je Prüfung: `ok` / `warnung` /
`fehler` mit Zahlenwert.

| ID | Prüfung | Kriterium | Stufe bei Verletzung | Beleg |
|---|---|---|---|---|
| P-01 | Kreuzspektrum-Ungleichung | $\lvert\mathrm{CP}_{ab}\rvert^2 \le \mathrm{AP}_a\mathrm{AP}_b\,(1+10^{-5})$ | fehler | W2 [D]; float32-Rundung ≈ 10⁻⁷ |
| P-02 | CPH-Ungleichung | $\lvert\mathrm{CPH}\rvert^2 \le \mathrm{AP}_a(1+10^{-5})$ | fehler | W2 [D] |
| P-03 | Vorzeichen | AP ≥ 0, ABS ≥ 0 | fehler | – |
| P-04 | Jensen | $\mathrm{ABS}^2 \le \mathrm{AP}(1+10^{-5})$ | fehler | W2 [D] |
| P-05 | Kohärenzbereich | $\gamma^2 \le 1 + 10^{-5}$; Werte in $(1, 1+10^{-5}]$ werden auf 1 gesetzt und gezählt | fehler darüber | Rundung |
| P-06 | Frequenzachse | $\lvert f_k - (k+k_0)\Delta f\rvert \le 10^{-6}\Delta f$ | fehler | 2.3 |
| P-07 | Phasensinn (A-1) | Anteil $q$ fallender Phase an Spitzen von $\lvert H_1\rvert$ (Prominenz wie 3.9 mit $p_\mathrm{min} = 2$, γ² ≥ 0,9, zentrale Differenz $\arg H_{k+1} - \arg H_{k-1}$, entfaltet); $q \ge 0{,}9$ ok; $q \le 0{,}1$ fehler „Daten vermutlich konjugiert“; dazwischen warnung; weniger als 10 Spitzen: „nicht prüfbar“ | siehe Kriterium | W3 2.2 [A, D]: Datei q = 0,982 |
| P-08 | Passivität am Antriebspunkt (nur wenn ein Antriebspunkt-Paar konfiguriert ist, z. B. Ref2/Ref1) | Anteil $r$ der Linien mit $\mathrm{Re}\{Y\} \ge 0$ unter γ² ≥ 0,9, mit $Y$ = Mobilität (aus Akzeleranz: $Y = H/(i\omega)$); $r \ge 0{,}95$ ok; $r \le 0{,}05$ warnung „Vorzeichen einer Referenz vermutlich gedreht“; dazwischen warnung „kein Antriebspunkt?“ | warnung | W3 2.3 [A, D]: Datei r = 0,0 |
| P-09 | Referenzstabilität | Median über die Linien, deren **arithmetisches Punktmittel** von γ² des Paars ≥ 0,9 ist, des Variationskoeffizienten von $\sqrt{\mathrm{AP}_b}$ über die gültigen Punkte (Standardabweichung mit ddof = 0) ≤ 0,05; je Kanalpaar | warnung | [D]: Datei 0,0108 (Vib Z/Ref1). Der frühere Wert 0,0105 stammt aus W3 2.7 (Linien 150–2400 Hz, ohne Kohärenzauswahl) (K1-5) |
| P-10 | Punktstatus | Anzahl ungültiger Punkte > 0 | Hinweis | [ANN M6] |
| P-11 | Annahmen | Liste aller Parameter mit Status „Annahme“ ($k_0$, $s_c$, `konjugieren`, $W_\mathrm{RBW}$, $n_d$, M7, Bandgrenzenregel) | Hinweis, immer ausgeben | Abschnitt 11 |

P-07 und P-08 prüfen verschiedene Fehler (W3 2.2): Eine Konjugation dreht den Phasensinn,
ein Vorzeichenwechsel nicht. Ein Vorzeichenwechsel dreht das Vorzeichen von Re{Y}, eine
Konjugation nicht.

---

## 5 Export und Abbildungen (B-7, B-6) – fachliche Festlegungen

**Export, Pflichtinhalt** (Format entscheidet der software-engineer):
1. Frequenzachse `frequenz_hz` und Linienindex k; $\Delta f$, $k_0$ mit Status.
2. Punkte: `index` (0-basiert), `label`, Koordinaten in m, Gültigkeit.
3. **Rohgrößen** CP, AP, ABS, CPH je Kanalpaar, ohne $s_c$ und ohne Konjugation. Komplexe
   Werte als Real- und Imaginärteil in float64, keine Rundung.
4. Abgeleitete Größen H1, H2, γ², Spektren nach 3.1, jeweils mit angewandtem $s_a s_b$ und
   `konjugieren`.
5. Einheit jeder Größe als Text, z. B. `m/s`, `(m/s)/N`, `N^2`. Kennzeichen „Spitzenwert“
   bzw. „Effektivwert“ und „einseitig“.
6. Konventionsangaben: `zeitkonvention = "exp(+i*omega*t)"`,
   `kreuzspektrum = "CP_ab = <A B*>, a = Antwort, b = Referenz"`, $W_\mathrm{RBW}$, $n_d$.
   Alle Annahmen mit Status (P-11).
7. Herkunft: Pfad und SHA-256 der Messdatei, Git-Hash der Software, Datum.

UFF-58-Export: Die Vorzeichen- und Einheitenkonventionen von UFF sind hier **nicht**
festgelegt, weil keine gelesene Quelle vorliegt. Das ist ein offener Punkt (Abschnitt 12).

**Abbildungen:**
- Achsen „Größe [Einheit]“ (KONVENTIONEN), mit Zusatz „Spitzenwert“ oder „Effektivwert“
  bei Spektren.
- Phase in rad, bei Anzeige in Grad ausdrücklich beschriften.
- dB nur als $20\log_{10}(\lvert X\rvert/X_\mathrm{ref})$ mit angegebenem $X_\mathrm{ref}$,
  Vorschlag $X_\mathrm{ref}$ = 1 Einheit.
- Linien mit γ² < γ²_min erkennbar machen, ohne Farbe als einzigen Informationsträger.
- Annahmen-Status in der Fußzeile.

---

## 6 Datenvertrag für W5

### 6.1 Eingaben

| Name | Form | Typ | Einheit | Bedingungen |
|---|---|---|---|---|
| `frequenz_hz` | (K,) | float64 | Hz | streng steigend, äquidistant (P-06), K ≥ 3 für Spitzensuche |
| `cp[a,b]` | (P, K) | complex128 | [a][b] | Rohdaten |
| `ap[a]`, `ap[b]` | (P, K) | float64 | [a]², [b]² | ≥ 0, sonst `ValueError` |
| `abs[a]` | (P, K) | float64 | [a] | ≥ 0 |
| `cph[a,b]` | (P, K) | complex128 | [a] | optional |
| `gueltig` | (P,) | bool | – | Voreinstellung alle True [ANN M6] |
| `n_d` | int oder (P,) | int | – | ≥ 1 [ANN M5] |
| `w_rbw` | float | float64 | – | ≥ 1 [ANN M5], Voreinstellung 1,0 |
| `vorzeichen_kanal[c]` | – | int | – | ±1 je Kanal [ANN M8], Voreinstellung +1; Vib X/Y/Z fest +1 (K1-1) |
| `konjugieren` | – | bool | – | Voreinstellung False [ANN M1] |
| `phase_gueltig` | – | bool | – | Referenz oder Trigger vorhanden |
| Parameter | – | – | – | γ²_min = 0,9; $p_\mathrm{min}$ = 2; W = 20; $n_\mathrm{min}$ = 3; $k_\varepsilon$ = 2; Abstand Nachbarmode 3 B |

### 6.2 Ausgaben (Auszug, Formen)

| Größe | Form | Einheit |
|---|---|---|
| `spektrum_kohaerent`, `spektrum_leistung` | (P, K) bzw. (P, 3, K) | [a] Spitzenwert |
| `h1`, `h2` | (P, K) complex | [a]/[b] |
| `kohaerenz` | (P, K) float | 1 |
| `eps_betrag_h1`, `sigma_phase_h1_rad`, `eps_kohaerenz`, `gewicht` | (P, K) | 1, rad, 1, 1 |
| `mittel_betrag`, `mittel_quadratisch`, `n_mittel` | (K,) | wie Eingang, Anzahl |
| Schwingform: `f_hz`, `amplitude` (P, 3) complex, `betrag_3d_psv`, `auslenkung_max`, `auslenkung_min` (P,), `phase_gueltig` | – | m/s bzw. (m/s)/N |
| Band: `rms`, `rms_psv`, `bandnorm`, `n_linien`, Hinweise | je Punkt (P,) und Mittel | wie 3.8 |
| Spitzen: Liste mit `f_sp_hz`, `hoehe`, `breite_3db_hz`, `q`, `zeta`, `f_l_hz`, `f_r_hz`, `k`, Kennzeichen | je Punkt oder Mittel | Hz, [a]/[b], Hz, 1, 1 |

### 6.3 Randfälle

| Fall | Verhalten |
|---|---|
| $\mathrm{AP}_b = 0$ an Linie k | H1 = NaN+iNaN, γ² = NaN, ε = NaN |
| $\mathrm{CP} = 0$, $\mathrm{AP}_a, \mathrm{AP}_b > 0$ | H1 = 0, H2 = NaN+iNaN, γ² = 0, ε = +∞, Gewicht 0 |
| $\mathrm{AP}_a = 0$ (und damit CP = 0) | H1 = 0, H2 = NaN, γ² = NaN |
| AP < 0 oder ABS < 0 | `ValueError` (P-03) |
| γ² in (1, 1 + 10⁻⁵] | auf 1 setzen, zählen; darüber Fehler P-05 |
| γ² = 1 | ε = 0, Gewicht über die Begrenzung endlich |
| $k_\varepsilon\,\varepsilon \ge 1$ (auch ε = +∞) | untere Fehlergrenze 0, Kennzeichen „Fehlerband nicht aussagekräftig“ (K1-6) |
| γ² im Spitzenbereich vollständig NaN | kein `kohaerenz_niedrig`, Hinweis „Kohärenz nicht prüfbar“ (K1-7b) |
| $n_d = 1$ | γ² = NaN, ε = NaN, H1 als „FRF“ bezeichnen |
| NaN im Eingang | wird weitergegeben; Punktmittel ignorieren NaN und geben $n$ aus |
| keine gültigen Punkte | Punktmittel NaN, $n = 0$ |
| leeres Band | NaN + Hinweis |
| $f_u > f_o$ | `ValueError` |
| $f_\mathrm{wahl}$ außerhalb der Achse | `ValueError` |
| $\omega_k = 0$ | Weg/Rezeptanz NaN |
| K < 3 | keine Spitzen, Hinweis |
| Spitze an Randlinie | wird nicht gemeldet |
| Nenner der Parabel ≥ 0 | δ = 0 |
| −3-dB-Seite nicht erreicht (Ende der Achse) | B = NaN, Kennzeichen `ueberlappend` |

---

## 7 Gültigkeit (Zusammenfassung)

- Linearität und Zeitinvarianz während der Messung. Die Drift über 40 min ist mit
  relativ ≤ 3·10⁻⁴ gering (W3 2.7 [D]).
- H1/H2/γ²: Rauschen unkorreliert mit dem Signal. Fehlerformeln für stationäre
  Zufallssignale und unabhängige Blöcke (3.4).
- Halbwertsbreite: getrennte Moden (Abstand ≥ 3 B), genügend Linien ($B \ge 3\Delta f$),
  abgeklungene Antwort im Messfenster. Leckage wird nicht erkannt (W3 2.5).
- 0-to-peak-Skalierung, $W_\mathrm{RBW}$ und Frequenzachse unter Vorbehalt M2, M4 und M5.
- Oberhalb 1 kHz ist die Gültigkeit offen (M7).

---

## 8 Vorschlag: Toleranzen für „stimmt mit PSV überein“

| Größe | Vorschlag | Begründung |
|---|---|---|
| Spektren, H1, H2, γ², Punktmittel, Bandwerte aus derselben Datei | rtol = 1·10⁻⁵, atol = 10⁻⁶·max\|Größe\| der Kurve | Daten sind float32 (rel. Rundung 6·10⁻⁸); W2 erreicht ≤ 9,3·10⁻⁷. atol fängt Werte nahe 0 ab |
| Werte aus ASCII/UFF-Export von PSV (M4) | rtol = 1·10⁻⁵ bzw. Rundung des Exportformats, falls gröber | einfache Genauigkeit im UFF (W1 [H]) |
| Spitzenfrequenz, ohne Warnkennzeichen oder nur mit `gueltigkeit_offen_m7` | $\lvert f_\mathrm{sp} - f_\mathrm{PSV}\rvert \le 0{,}25\,\Delta f$ | Eigener Fehler ≤ 0,0508 Δf bei B ≥ 3 Δf [N]; PSV-Fit unbekannt (Fitbereich vom Band-Cursor abhängig); Reserve für Modellunterschiede |
| Spitzenfrequenz, mit `aufloesungsbegrenzt` (ggf. zusätzlich `gueltigkeit_offen_m7`) | $\le 0{,}5\,\Delta f$ | Beide Verfahren müssen dieselbe Linie treffen; feiner ist ohne Kenntnis des PSV-Fits nicht begründbar |
| −3-dB-Breite B (bzw. ζ), ohne Warnkennzeichen oder nur mit `gueltigkeit_offen_m7` | $\lvert B/B_\mathrm{PSV} - 1\rvert \le 0{,}10$ | Eigener Bias ≤ +5,21 % bei B ≥ 3 Δf [N]; der Rest ist Reserve für den PSV-Fit |
| B mit einem anderen Warnkennzeichen | kein Vergleich, nur Bericht der Werte | Beide Schätzer sind dort systematisch verzerrt (bis +178 %); Übereinstimmung wäre zufällig |

`gueltigkeit_offen_m7` allein schließt den Vergleich nicht aus: M7 betrifft die physikalische
Gültigkeit oberhalb 1 kHz, nicht die Übereinstimmung mit PSV an denselben Daten (K1-8).

Diese Toleranzen sind **Vorschläge**. Prüfschritt M11 (Abschnitt 11) liefert am Montag
PSV-Werte, an denen sie bestätigt oder enger gefasst werden. Der Nutzer gibt frei.

---

## 9 Referenzfälle (Tests)

Gemeinsame Testdaten: $BW = 2500$ Hz, $n_\mathrm{FFT} = 1600$, $N = 4000$, $f_s = 6250$ Hz,
$\Delta f = 1{,}5625$ Hz. Spektren nach 2.1, Linien $k = 1\dots1600$ ($k_0 = 1$), periodisches
Hann-Fenster $w_n = 0{,}5 - 0{,}5\cos(2\pi n/N)$. „Algorithmus-Sollwert“ bedeutet: Der Wert
folgt deterministisch aus der Vorschrift, die Toleranz deckt nur Gleitkommarundung ab.

### 9.1 Skalierung und Band-RMS (A-7, Testdaten)

| ID | Eingang | Sollwert | Toleranz, Begründung |
|---|---|---|---|
| RF-S1 | $x = 2\cos(2\pi\cdot100\,t + \pi/3)$ m/s (Linie 64), Rechteck und Hann | $\hat X_{64} = 1 + 1{,}7320508076i$ m/s (\|·\| = 2, arg = π/3) | rtol 1e-12 (Rundung) |
| RF-S2 | wie S1, Frequenz $(64{,}5)\Delta f$ | max\|$\hat X$\| = 1,2752815250 (Rechteck, −36,24 %), 1,6976528729 (Hann, −15,12 %) | rtol 1e-9 |
| RF-S3 | Fenster | $W_\mathrm{RBW}$: Rechteck 1,0; Hann 1,5 | rtol 1e-12 |
| RF-B1 | S1, Band $64 \pm 3$ Linien, Rechteck bzw. Hann ($W_\mathrm{RBW}$ 1 bzw. 1,5) | `rms` = $2/\sqrt2$ = 1,4142135624 m/s | rtol 1e-12 (exakt, Parseval) |
| RF-B2 | Band $[100, 100]$ Hz (nur Linie 64), Rechteck | 1,4142135624 m/s | rtol 1e-12; prüft geschlossenes Intervall |
| RF-B3 | Band $[100{,}1;\ 100{,}2]$ Hz | NaN, Hinweis „leeres Band“ | exakt |
| RF-B4 | S2 (Rechteck), Band ±3 / ±10 / ±50 Linien um 64 | 1,3722894714 / 1,4006918958 / 1,4122824908 (−2,96 % / −0,96 % / −0,14 %) | rtol 1e-9 (Algorithmus-Sollwert) |
| RF-B5 | S2 (Hann), Band ±3 / ±10 Linien | 1,4141638634 / 1,4142134072 | rtol 1e-9 |
| RF-B6 | $x = 2\cos(2\pi\cdot100\,t) + 0{,}5\cos(2\pi\cdot1000\,t + 1)$, Rechteck; Bänder [90, 110], [990, 1010], [0, 2500] Hz | 1,4142135624 / 0,3535533906 / 1,4577379737 | rtol 1e-12 |
| RF-B7 | $f_u > f_o$ | `ValueError` | – |
| RF-B8 | FRF-Bandnorm, $H_k = 1 + 0i$ an 4 Linien im Band | $\sqrt{4/2} = 1{,}4142135624$ (m/s)/N | rtol 1e-12 |
| RF-B9 | `rms_psv` für AP: $\mathrm{AP}_k = 4$ an 3 Linien | $\sum \mathrm{AP}/2 = 6$ (m/s)² | exakt |

### 9.2 H1, H2, Kohärenz, Spektren (A-2, A-4)

Die Eingänge werden **direkt als Erwartungswerte** gesetzt (deterministisch):
$S_x = 1$ N², $H = 0{,}8 + 0{,}3i$ (m/s)/N, $\mathrm{AP}_b = S_x + N_R$,
$\mathrm{AP}_a = \lvert H\rvert^2S_x + N_V$, $\mathrm{CP}_{ab} = H\,S_x$.

| ID | $N_R$ [N²] | $N_V$ [(m/s)²] | $H_1$ | $H_2$ | γ² | Toleranz |
|---|---|---|---|---|---|---|
| RF-H1 | 0 | 0 | 0,8 + 0,3i | 0,8 + 0,3i | 1 | rtol 1e-12 |
| RF-H2 | 0,05 | 0,08 | 0,7619047619 + 0,2857142857i (= 0,9523809524 H) | 0,8876712329 + 0,3328767123i (= 1,1095890411 H) | 0,8583186361 | rtol 1e-10 |
| RF-H3 | 0 | 0,08 | H | 1,1095890411 H | 0,9012345679 | rtol 1e-10 |
| RF-H4 | 0,05 | 0 | 0,9523809524 H | H | 0,9523809524 | rtol 1e-10 |

- **RF-H5:** In RF-H2 gilt $\gamma^2 = H_1/H_2$ (Imaginärteil < 1e-15), und
  $\arg H_1 = \arg H_2 = \arg H$, atol 1e-12 rad.
- **RF-H6 (Spektren):** In RF-H2 mit $\mathrm{CPH} := \mathrm{CP}/\sqrt{\mathrm{AP}_b}$ gilt
  `spektrum_kohaerent` = 0,8338093878 m/s, `spektrum_leistung` = 0,9 m/s und das Verhältnis
  0,9264548754 = γ. rtol 1e-10.
- **RF-H7 (Randfälle):**
  - $\mathrm{AP}_b = 0$ → H1 NaN, γ² NaN.
  - CP = 0 mit AP > 0 → H1 = 0, H2 NaN, γ² = 0.
  - AP = −1 → `ValueError`.
  - γ² = 1 + 5·10⁻⁶ (konstruiert) → 1,0 und Zähler 1.
  - γ² = 1,001 → P-05 fehler.
- **RF-H8 (Vorzeichen/Konjugation, K1-1):** Eingang RF-H2.
  - Nur $s_b = -1$ (Referenz): H1 → $-H_1$, H2 → $-H_2$.
  - Nur $s_a = -1$ (Antwort): H1 → $-H_1$, H2 → $-H_2$.
  - $s_a = s_b = -1$: H1 und H2 unverändert.
  - In allen Fällen bleiben γ², AP und ABS gleich. `spektrum_kohaerent` ändert das Vorzeichen
    wie H1.
  - Kanal in zwei Rollen: Paare Ref2/Ref1 und Vib Z/Ref2 mit $s_{\mathrm{Ref2}} = -1$ → beide
    H1 wechseln das Vorzeichen; Vib Z/Ref1 bleibt unverändert.
  - Mit `konjugieren=True` wird H1 zu $H_1^{*}$.
  - rtol 1e-12.

### 9.3 Zufallsfehler und Kohärenzschwelle (B-2, B-3)

| ID | Eingang | Sollwert | Toleranz |
|---|---|---|---|
| RF-U1 | $n_d = 7$, γ² = 0,9 | ε\|H1\| = 0,0890870806; σ_φ = 0,0890870806 rad; ε_γ² = 0,0563436170; Gewicht = 126 | rtol 1e-9 (Formel) |
| RF-U2 | $n_d = 7$, γ² = 0,5 | 0,2672612419; 0,3779644730; Gewicht 14 | rtol 1e-9 |
| RF-U3 | $n_d = 25$, γ² = 0,99 | 0,0142133811; 0,0028426762; Gewicht 4950 | rtol 1e-9 |
| RF-U4 | γ² = 0 / γ² = 1 / $n_d = 1$ | ε = +∞, Gewicht 0 / ε = 0 / NaN | exakt |
| RF-U5 (statistisch, optional) | Monte-Carlo: $x_j$ komplex normal (Varianz 1), $y_j = Hx_j + n_j$ mit $\mathrm{Var}(n) = \lvert H\rvert^2(1/\gamma^2 - 1)$, $n_d = 25$, γ² = 0,9, M = 40 000 Wiederholungen, `numpy.random.default_rng(20261029)` | Standardabweichung von $\lvert\hat H_1\rvert/\lvert H\rvert$ = Formelwert 0,04714 | relativ ±10 % (beobachtet +3 %; Formel ist Näherung erster Ordnung) |
| RF-U6 | Maske mit γ² = [0,95; 0,9; 0,85], γ²_min = 0,9 | [True, True, False] | exakt (Grenze inklusiv) |
| RF-U7 (K1-6) | \|H1\| = 1, $n_d = 7$, $k_\varepsilon = 2$; γ² = 0,9 bzw. 0,2 | γ² = 0,9: Band [0,8218258387; 1,1781741613], kein Kennzeichen. γ² = 0,2: ε = 0,5345224838, untere Grenze 0 (ungekürzt −0,0690449676), obere 2,0690449676, Kennzeichen „Fehlerband nicht aussagekräftig“. γ² = 0: untere Grenze 0, obere +∞, Kennzeichen | rtol 1e-9 |

### 9.4 Einmassenschwinger und zwei Moden (A-6)

Die FRF ist die Mobilität $Y(f) = i\omega/(k - m\omega^2 + ic\omega)$ mit $m = 1$ kg,
$\omega_n = 2\pi f_n$, $k = m\omega_n^2$, $c = 2\zeta m\omega_n$. Das Raster ist
$f_j = (j + \text{off})\,\Delta f$, $j = 1, 2, \dots$; die Eingabe ist $y = \lvert Y\rvert$.

| ID | $f_n$, ζ, Δf, off | Physikalische Wahrheit | Algorithmus-Sollwert (rtol 1e-9) | Kennzeichen |
|---|---|---|---|---|
| RF-P0 | analytisch, 100 Hz, 0,01 | c = 12,566370614 Ns/m; k = 394 784,17604 N/m; \|Y\|max = 1/c = 0,0795774715 (m/s)/N; $f_{1,2}$ = 99,004999875 / 101,004999875 Hz; B = 2,000 Hz | – | – |
| RF-P1 | 100; 0,01; 0,25; 0 | B = 2 Hz, f = 100 Hz | $f_\mathrm{sp}$ = 100,000298644; $\hat y$ = 7,957747494e-2; B = 2,000591366; ζ = 0,010002927 | keins ($B/\Delta f$ = 8,0) |
| RF-P2 | 100; 0,01; 0,25; 0,37 | wie P1 | 100,002070830; 7,953876069e-2; 2,008976145; 0,010044673 | keins |
| RF-P3 | 100; 0,005; 1,5625; 0 | B = 1,0 Hz | 100,002427267; 0,1591552101; 1,316512038; 0,006582400 | `aufloesungsbegrenzt` (0,84) |
| RF-P4 | 100; 0,005; 1,5625; 0,37 | B = 1,0 Hz | 100,303481217; 0,1058309032; 2,095705355; 0,010446823 | `aufloesungsbegrenzt` (1,34) |
| RF-P5 | wie P1, 50 Rasterlagen off ∈ [0, 1) | – | max\|$f_\mathrm{sp}$ − 100\| = 0,00954 Δf (≤ 0,010 Δf); $B$ − 2 in [0; +0,005364·2] Hz, Maximum +0,005364·2 Hz mit Toleranz 1e-6·2 Hz (K1-2) | keins |

Gegen die physikalische Wahrheit gilt die Toleranz aus der Diskretisierungstabelle (3.9),
z. B. RF-P1: \|B/2 − 1\| ≤ 0,0054 und \|f_sp − 100\| ≤ 0,01 Δf.

**Zwei Moden** (RF-M): $Y = \sum_{r=1}^{2} i\omega/(\omega_r^2 - \omega^2 + 2i\zeta\omega_r\omega)$
in (m/s)/N, Modalmasse 1 kg, ζ = 0,01, $f_1 = 100$ Hz, Δf = 0,05 Hz, off = 0. Sollwerte als
Algorithmus-Sollwert mit rtol 1e-6 (vierstellig angegeben, im Test aus dem Prüfskript mit
voller Stellenzahl übernehmen):

| ID | $f_2$ [Hz] | Abstand/B₁ | Ergebnis (f_sp; B) | Kennzeichen |
|---|---|---|---|---|
| RF-M1 | 101 | 0,5 | **eine** Spitze: 100,3150; 3,0375 (+52 %) | keins (Verfahrensgrenze, dokumentiert) |
| RF-M2 | 103 | 1,5 | 99,8449; 2,0489 / 103,1656; 2,1352 | `nachbarmode` an beiden |
| RF-M3 | 106 | 3,0 | 99,8711; 1,9929 / 106,1511; 2,1330 | untere Spitze keins (6,28 Hz ≥ 3·1,99 = 5,98 Hz), obere `nachbarmode` (6,28 Hz < 3·2,13 = 6,40 Hz) |
| RF-M4 | 120 | 10 | 99,9555; 1,9968 / 120,0762; 2,4061 (= 2ζ·120 + 0,2 %) | keins |

Das Kennzeichen `nachbarmode` entsteht, wenn der Abstand der gefundenen Spitzen kleiner als
3·B **der betrachteten Spitze** ist. RF-M3 liegt genau an dieser Grenze und prüft die
Zuordnung je Spitze. Die Prominenzauswahl aus 3.9 Schritt 1 ist in RF-M abgeschaltet: Hier
gelten alle lokalen Maxima als Kandidaten, weil das Fenster W = 20 Linien bei Δf = 0,05 Hz
nur ±1 Hz breit ist.

### 9.5 Schwingform und 3D (A-5)

| ID | $\hat{\vec v}$ [m/s] | betrag_3d_psv | auslenkung_max | auslenkung_min | Toleranz |
|---|---|---|---|---|---|
| RF-3D1 | (1, i, 0) | 1,4142135624 | 1,0 | 1,0 | rtol 1e-12 |
| RF-3D2 | (1, 1, 0)·e^{0,7i} | 1,4142135624 | 1,4142135624 | 0 | rtol 1e-12, min atol 1e-12 |
| RF-3D3 | (1; 0,5·e^{iπ/3}; 0,2i) | 1,1357816692 | 1,0374517607 | 0,4622703151 | rtol 1e-9; gegen Brute-Force über θ geprüft |
| RF-3D4 | (0, 0, 10⁻³·e^{−0,4i}) | 1,0e-3 | 1,0e-3 | 0 | rtol 1e-12 |

- **RF-3D5 (Momentanwert):** Für $\hat v = e^{i\pi/3}$ gilt $u(\theta) = \cos(\theta + \pi/3)$ an
  θ = 0, π/2, π mit den Werten 0,5; −0,8660254038; −0,5. atol 1e-12.
- **RF-3D6 (Linienwahl):** Achse $k\cdot1{,}5625$ Hz.
  - $f_\mathrm{wahl}$ = 100,7 Hz → Linie 100,0 Hz (Index 63).
  - 100,78125 Hz (Gleichstand) → 100,0 Hz.
  - 0 Hz → `ValueError`, denn 0 Hz liegt unter der Grenze $f_0 - \Delta f/2 = 0{,}78125$ Hz.
  - 0,8 Hz → Linie 1,5625 Hz (Index 0).
  - 2500,5 Hz → 2500 Hz.
- **RF-3D7:** Mit `phase_gueltig=False` gibt es nur Beträge, und eine Anfrage nach der
  Animation wirft einen Fehler bzw. liefert ein leeres Ergebnis (Entscheidung W5).

### 9.6 Umrechnung (B-10)

| ID | Eingang | Sollwert | Toleranz |
|---|---|---|---|
| RF-W1 | $\hat v$ = 1 m/s bei 100 Hz | $\hat d = -1{,}5915494309\cdot10^{-3}\,i$ m (\|·\| 1,5915494309e-3, arg −π/2); $\hat a$ = 628,3185307 i m/s² | rtol 1e-12 |
| RF-W2 | RF-P0 bei $f_n$ | Rezeptanz $-1{,}2665147955\cdot10^{-4}\,i$ m/N; Akzeleranz 50 i (m/s²)/N | rtol 1e-10 |
| RF-W3 | $\omega = 0$ ($k_0 = 0$) | Weg NaN | exakt |

### 9.7 Konvention, Phasensinn, Passivität (A-1, B-4)

Zwei-Moden-Mobilität RF-M4 ($f_2$ = 120 Hz) auf dem Raster 0,05 Hz:

| ID | Eingang | P-07: Anteil fallend | P-08: Anteil Re ≥ 0 | Erwartetes Urteil |
|---|---|---|---|---|
| RF-K1 | Y | 1,0 (2 Spitzen) | 1,0 | P-07 „nicht prüfbar“ (< 10 Spitzen); mit Mindestanzahl 1 ist der Rechenwert 1,0 |
| RF-K2 | Y* | 0,0 | 1,0 | P-07 fehler „konjugiert“; P-08 ok |
| RF-K3 | −Y | 1,0 | 0,0 | P-07 ok; P-08 warnung „Vorzeichen gedreht“ |

**RF-K4 (P-07 mit Mindestanzahl 10):** Summe von zwölf Moden bei 100, 120, …, 320 Hz
(ζ = 0,01, Modalmasse 1 kg), Raster $f_j = 0{,}5\,j$ Hz, $j = 1 \dots 799$, Prominenz nach 3.9
($p_\mathrm{min} = 2$, W = 20 Linien), γ² = 1 gesetzt. Erwartet werden **11** Spitzen, die
das Kriterium erfüllen. Ergebnisse:
- Y: q = 1,0, r = 1,0.
- Y*: q = 0,0 („konjugiert“), r = 1,0.
- −Y: q = 1,0, r = 0,0.

Exakt geprüft [N].

### 9.8 Punktmittel (A-3, B-9)

- **RF-G1:** Werte an einer Linie über drei Punkte: $X = (1, -1, 2i)$.
  $M^\mathrm{Betrag}$ = 4/3 = 1,3333333333; $M^\mathrm{quadr} = \sqrt2$ = 1,4142135624;
  |komplexes Mittel| = 2/3 (nur zur Kontrolle der Ungleichung). rtol 1e-12.
- **RF-G2:** Wie G1 mit Punkt 2 ungültig: $M^\mathrm{Betrag}$ = 1, $M^\mathrm{quadr}$ = 1, $n$ = 2.
- **RF-G3:** AP = (1, 4, 9) → PSV-Mittel 14/3. $M^\mathrm{quadr}(\sqrt{\mathrm{AP}}) = \sqrt{14/3}$ = 2,1602468995;
  $M^\mathrm{Betrag}(\sqrt{\mathrm{AP}})$ = 2. rtol 1e-12.
- **RF-G4:** Punkt 0 an der Linie NaN → Mittel über die übrigen, $n$ = 2. Alle ungültig → NaN, $n$ = 0.

### 9.9 Golden-File-Test (nach Montag)

An `Input/20261012_ref_Mitte.svd` müssen die Größen aus 3.2, 3.3 und 3.8 die PSV-eigenen
Punktmittel und Banddaten der Datei mit den Toleranzen aus Abschnitt 8 treffen. Das hat W2
bereits für die Beträge gezeigt. P-07 muss q ≥ 0,9 liefern (W3: 0,982). Nach M1, M4 und M11
kommen die PSV-Exportwerte hinzu.

---

## 10 Quellen

| Kürzel | Quelle | Prüfstand | Verwendet für |
|---|---|---|---|
| TM | Polytec Theory Manual (`polytec2015theory`), S. 9–10, 14–18 | volltext teilweise; Gleichungen von I2 als Bild gelesen | Skalierung, AP/CP/H1/H2/γ², RMS Gl. 3.17, $W_\mathrm{RBW}$ |
| HB, SWP | PSV-Handbücher 10.1 (`polytec2022psvhandbuch`, `polytec2022psvdesktop`) | volltext teilweise | Band-Cursor (f_max, Breite, Q, ζ), Bandgrenzen auf Linien |
| W1, W2, W3, I2 | Analyseberichte unter `in_progress/analysen/` | Repo | Belegketten, Datenbefunde |
| Bendat/Piersol (`bendat2010random`) | Random Data | **metadaten** | Fehlerformeln 3.4: nur numerisch eigen geprüft, Gleichungsnummern fehlen |
| Ewins (`ewins2000modal`) | Modal Testing | **metadaten** | Halbwertsbreite: hier eigene Herleitung, Quelle für den Thesis-Text nötig |
| Brandt (`brandt2011noise`) | Noise and Vibration Analysis | **metadaten** | Leckage und Abklingen (Gültigkeit) |
| Harris (`harris1978windows`), Heinzel (`heinzel2002spectrum`) | Fenster, ENBW | **metadaten** | $W_\mathrm{RBW}$; hier numerisch eigen geprüft |

Gesichert sind nur die Polytec-Textstellen, die Dateibefunde und die eigenen
Herleitungen und Rechnungen. Alle Lehrbuchaussagen sind bis zum Lesen der Volltexte
ungeprüft.

---

## 11 Einstellbare Annahmen und Prüfschritte am Messrechner (Montag, 2026-11-02)

| Nr. | Annahme (Parameter, Voreinstellung) | Prüfschritt | Erwartung / Folge |
|---|---|---|---|
| M1 | `konjugieren = False` | PSV: Punkt Label 132, „Vib X & Ref1“, H1, Phase (oder Real/Imag) bei drei Frequenzen, z. B. 100, 500, 1000 Hz; mit H1 = CP/AP aus dem Leser vergleichen | Gleich → bestätigt. Gespiegelt → PSV-Anzeige ist konjugiert; Daten bleiben nach P-07 physikalisch richtig, für den PSV-Vergleich konjugieren |
| M2 | $k_0 = 1$ | Erste und letzte Frequenz der Achse in PSV oder Export | 1,5625 Hz bzw. 2500 Hz |
| M4 | 0-to-peak | Export „Vib X Geschwindigkeit“ Label 132 bei drei Frequenzen gegen \|CPH\| | gleiche Zahlen (Spitzenwert) |
| M5 | $W_\mathrm{RBW} = 1$ (Rechteck), $n_d = 7$ | Fenster, Generator (Signalform, Burstlänge), Mittelungsart und -anzahl, Signal Enhancement ablesen | $W_\mathrm{RBW}$ setzen; $n_d$ je Punkt deuten |
| M6 | alle Punkte gültig | Scanstatus der Punkte mit Feldwert 1 und 3 | Gültigkeitsmaske |
| M7 | Gültigkeit > 1 kHz offen | Bedeutung „Bandbreitenbereich 1 kHz“ (Datenblatt, Betreuer) | Kennzeichen entfernen oder Gültigkeitsgrenze festschreiben |
| M8 | $s_c = +1$ für Ref1, Ref2 (Vorzeichen je Kanal, K1-1) | Typ, Ort und Einbaurichtung von Kraftsensor und Beschleunigungsaufnehmer; Shakerposition | P-08 an der Datei zeigt heute r = 0 → ein Vorzeichen ist vermutlich zu drehen; welches, entscheidet der Einbau. Gedrehter Ref1: $s_{\mathrm{Ref1}} = -1$; gedrehter Ref2: $s_{\mathrm{Ref2}} = -1$ (wirkt in Ref2/Ref1 und Vib/Ref2) |
| M10 | Band geschlossen, beide Grenzlinien | In PSV ein Band 100–200 Hz definieren, RMS von „Vib Z Geschwindigkeit“ für Label 132 ablesen; mit `rms_psv` für [100, 200] und für (100, 200) vergleichen | Regel bestätigen oder ändern |
| M11 | Toleranzen aus Abschnitt 8 | Band-Cursor-Fit in PSV auf H1 „Vib Z & Ref1“, Label 132, an drei Spitzen ohne Warnkennzeichen und einer mit; f_max und „Dämpfung“ notieren, Cursorgrenzen festhalten | Toleranzen bestätigen oder anpassen |

---

## 12 Offene Punkte

1. Alle Annahmen aus Abschnitt 11 bis Montag.
2. Lehrbuchbelege für 3.4 (Bendat/Piersol), 3.9 (Ewins), Leckage (Brandt): Volltexte lesen
   (Rechercheauftrag).
3. UFF-58-Konventionen (Vorzeichen, Einheitenfelder, Abszissen-Definition) für den Export:
   keine gelesene Quelle.
4. Leckage durch nicht abgeklungene Burst-Antwort wird nicht erkannt. Ein Kriterium braucht
   Zeitdaten oder die Burstlänge (Stufe 2 bzw. Versuchsplanung).
5. Das Prominenzkriterium der Spitzensuche ist eine Auswahlheuristik ohne Literaturbeleg.
6. Ob PSV im Band-Cursor auf H1 oder auf dem Antwortspektrum fittet, hängt von der Anzeige
   ab. Für M11 auf H1 einstellen.

---

## Anhang: Prüfskript

Ausgeführt mit numpy (uv-Gruppe `werkzeuge`) aus `software/`:
`uv run --group werkzeuge python fg02_pruef.py`. Die Ausgabe enthält alle Sollwerte aus
Abschnitt 9. Ergänzend wurden die Werte aus RF-U1 bis RF-U3 und RF-H6 mit einem
Einzeiler berechnet (Formeln aus 3.4 bzw. 3.1). RF-K4 (zwölf Moden, Raster 0,5 Hz, Prominenzkriterium aus 3.9) wurde
ebenfalls mit einem Einzeiler geprüft: 11 Spitzen; q = 1,0 / 0,0 / 1,0; r = 1,0 / 1,0 / 0,0.
Die Prüfungen betreffen nur numpy und den W2-Leser (Stand e7df2e6); die geänderte Zeitstempel-
und Kanalrollenbehandlung des Lesers berührt diese Fachgrundlage nicht. Die Datei-Prüfung der FRF-Bandnorm (S17)
lief über den W2-Leser (`m.baender["S17"].werte` gegen $\sqrt{\sum\lvert\mathrm{CP}_0/\mathrm{AP}_{12}\rvert^2/2}$).

```python
"""Pruefskript FG-02 (Auswertung Stufe 1). numpy only. Alle Sollwerte der Fachgrundlage."""
import numpy as np
np.set_printoptions(precision=10)
BW, NL = 2500.0, 1600; N = int(2.5*NL); FS = 2.5*BW; DF = FS/N   # 6250 Hz, 4000, 1.5625 Hz
t = np.arange(N)/FS

def spek(x, w):
    """einseitig, Spitzenwert, amplitudentreu; Linien k=1..NL (DC weg)."""
    X = 2.0*np.fft.rfft(w*x)/w.sum()
    return X[1:NL+1]
def hann(n):  # periodisch
    return 0.5-0.5*np.cos(2*np.pi*np.arange(n)/n)
rect = np.ones(N); hn = hann(N)
wrbw = lambda w: len(w)*np.sum(w**2)/np.sum(w)**2
print("== RF-S: Skalierung ==")
print("W_RBW rect, hann:", wrbw(rect), wrbw(hn))
A, phi, k0 = 2.0, np.pi/3, 64           # f = 100 Hz
for nm, w in [("rect", rect), ("hann", hn)]:
    X = spek(A*np.cos(2*np.pi*k0*DF*t+phi), w)
    print(nm, "on-line X[k0] =", X[k0-1], "abs", abs(X[k0-1]), "arg", np.angle(X[k0-1]))
    Xh = spek(A*np.cos(2*np.pi*(k0+0.5)*DF*t+phi), w)
    print(nm, "half-line max|X| =", np.abs(Xh).max(), " rel", np.abs(Xh).max()/A)
def band_rms(X, f, flo, fhi, wr):
    sel = (f >= flo-1e-6*DF) & (f <= fhi+1e-6*DF)
    return np.sqrt(np.sum(np.abs(X[sel])**2)/(2*wr)) if sel.any() else np.nan
f = DF*np.arange(1, NL+1)
print("== RF-B: Band-RMS (A=2, Soll A/sqrt2 =", A/np.sqrt(2), ") ==")
for nm, w in [("rect", rect), ("hann", hn)]:
    for off in [0.0, 0.5]:
        X = spek(A*np.cos(2*np.pi*(k0+off)*DF*t+phi), w)
        for half in [3, 10, 50]:
            r = band_rms(X, f, (k0-half)*DF, (k0+half)*DF, wrbw(w))
            print(f"{nm} off={off} band +-{half} lines: RMS={r:.10f} rel.err={r/(A/np.sqrt(2))-1:+.3e}")
x2 = 2*np.cos(2*np.pi*64*DF*t) + 0.5*np.cos(2*np.pi*640*DF*t+1)
X2 = spek(x2, rect)
print("two sines rect: band 90-110 Hz", band_rms(X2,f,90,110,1.0), " band 990-1010 Hz", band_rms(X2,f,990,1010,1.0),
      " band 0-2500", band_rms(X2,f,0,2500,1.0), "soll", np.sqrt(2**2/2+0.5**2/2))
print("empty band 100.1-100.2 Hz:", band_rms(X2, f, 100.1, 100.2, 1.0))
print("edge: band 100.0-100.0 Hz (exakt auf Linie 64):", band_rms(X2, f, 100.0, 100.0, 1.0))

print("== RF-H: H1/H2/gamma2 erwartungstreu (analytisch) ==")
H = 0.8+0.3j; Sx, NR, NV = 1.0, 0.05, 0.08
APR, APV, CP = Sx+NR, abs(H)**2*Sx+NV, H*Sx
H1 = CP/APR; H2 = APV/np.conj(CP); g2 = abs(CP)**2/(APR*APV)
print("H1", H1, "H1/H", H1/H); print("H2", H2, "H2/H", H2/H); print("g2", g2, " H1/H2", H1/H2)
print("nur Ausgang: H1/H", (H*1)/(1.0)/H, "H2/H", (abs(H)**2+NV)/np.conj(H)/H, "g2", abs(H)**2/(abs(H)**2+NV))
print("nur Eingang: H1/H", H/(1+NR)/H, "H2/H", abs(H)**2/np.conj(H)/H, "g2", 1/(1+NR))

print("== MC: Zufallsfehler nach Bendat/Piersol-Naeherung ==")
rng = np.random.default_rng(20261029)
def cgauss(shape, var):
    return np.sqrt(var/2)*(rng.standard_normal(shape)+1j*rng.standard_normal(shape))
for nd in [7, 25]:
    for g2t in [0.5, 0.9, 0.99]:
        M = 40000
        x = cgauss((M, nd), 1.0); NVv = abs(H)**2*(1/g2t-1)   # nur Ausgangsrauschen -> gamma2 = g2t
        y = H*x + cgauss((M, nd), NVv)
        Gxx = (abs(x)**2).mean(1); Gyy = (abs(y)**2).mean(1); Gxy = (y*np.conj(x)).mean(1)
        H1e = Gxy/Gxx; g2e = abs(Gxy)**2/(Gxx*Gyy)
        eH = np.std(abs(H1e))/abs(H); eHf = np.sqrt(1-g2t)/(np.sqrt(g2t)*np.sqrt(2*nd))
        eG = np.std(g2e)/g2t; eGf = np.sqrt(2)*(1-g2t)/(np.sqrt(g2t)*np.sqrt(nd))
        eP = np.std(np.angle(H1e/H))
        print(f"nd={nd:2d} g2={g2t}: eps|H1| MC {eH:.4f} Formel {eHf:.4f} | sigma_phase MC {eP:.4f} | eps g2 MC {eG:.4f} Formel {eGf:.4f} | E[g2^] {g2e.mean():.4f}")
    x = cgauss((40000, nd), 1.0); y = cgauss((40000, nd), 1.0)
    g0 = abs((y*np.conj(x)).mean(1))**2/((abs(x)**2).mean(1)*(abs(y)**2).mean(1))
    print(f"nd={nd}: gamma2_true=0 -> E[g2^] MC {g0.mean():.4f}, 1/nd={1/nd:.4f}, 95%-Quantil MC {np.quantile(g0,0.95):.4f}, analytisch 1-0.05^(1/(nd-1))={1-0.05**(1/(nd-1)):.4f}")

print("== RF-P: SDOF-Mobilitaet, Spitze und -3dB ==")
def sdof_Y(fr, m=1.0, fn=100.0, z=0.01):
    w = 2*np.pi*fr; wn = 2*np.pi*fn; k = m*wn**2; c = 2*z*m*wn
    return 1j*w/(k-m*w**2+1j*c*w)
m_, fn_, z_ = 1.0, 100.0, 0.01
print("c =", 2*z_*m_*2*np.pi*fn_, " k =", (2*np.pi*fn_)**2, " |Y(fn)| = 1/c =", 1/(2*z_*m_*2*np.pi*fn_))
wn = 2*np.pi*fn_; w1 = wn*(np.sqrt(1+z_**2)-z_); w2 = wn*(np.sqrt(1+z_**2)+z_)
print("exakt f1,f2,B:", w1/2/np.pi, w2/2/np.pi, (w2-w1)/2/np.pi)

def peak_est(y, f, k, mode="parab"):
    """y=|H| auf Linien, k=Index lokales Max. Rueckgabe f_peak, A_peak, B, flags."""
    df = f[1]-f[0]; a, b, c = y[k-1], y[k], y[k+1]
    den = a-2*b+c; d = 0.5*(a-c)/den if (mode == "parab" and den < 0) else 0.0
    fp = f[k]+d*df; Ap = b-0.25*(a-c)*d if mode == "parab" else b
    thr = Ap/np.sqrt(2); fl = fr = np.nan; flag = []
    j = k
    while j > 0 and y[j] >= thr:
        if j < k and y[j] < y[j-1] and y[j] <= y[j+1]: flag.append("ueberlappend_links"); break
        j -= 1
    if y[j] < thr: fl = f[j]+(thr-y[j])/(y[j+1]-y[j])*df
    j = k
    while j < len(y)-1 and y[j] >= thr:
        if j > k and y[j] < y[j+1] and y[j] <= y[j-1]: flag.append("ueberlappend_rechts"); break
        j += 1
    if y[j] < thr: fr = f[j-1]+(y[j-1]-thr)/(y[j-1]-y[j])*df
    B = fr-fl
    return fp, Ap, B, flag

def scan(ratio_list, z=0.01, fn=100.0, mode="parab", n_off=50):
    B0 = 2*z*fn
    for R in ratio_list:
        df = B0/R; errs_f, errs_B = [], []
        for off in np.linspace(0, 1, n_off, endpoint=False):
            fgrid = (np.arange(1, int(2*fn/df)) + off)*df
            y = np.abs(sdof_Y(fgrid, fn=fn, z=z)); k = int(np.argmax(y))
            fp, Ap, B, fl = peak_est(y, fgrid, k, mode)
            errs_f.append((fp-fn)/df); errs_B.append(B/B0-1)
        print(f"  {mode}: B/df={R:5.2f}: max|f_err|={np.max(np.abs(errs_f)):.3f} df, B_err min {np.min(errs_B):+.3f} max {np.max(errs_B):+.3f}")
for mode in ["parab", "linie"]:
    scan([0.64, 1.0, 1.5, 2.0, 3.0, 4.0, 6.0, 8.0], mode=mode)
for (z, df, off) in [(0.01, 0.25, 0.0), (0.01, 0.25, 0.37), (0.005, 1.5625, 0.0), (0.005, 1.5625, 0.37)]:
    fgrid = (np.arange(1, 129) + off)*df if df > 1 else (np.arange(1, 801)+off)*df
    y = np.abs(sdof_Y(fgrid, z=z)); k = int(np.argmax(y))
    fp, Ap, B, fl = peak_est(y, fgrid, k)
    print(f"RF-P z={z} df={df} off={off}: k={k} f_k={fgrid[k]:.6f} f_peak={fp:.9f} A={Ap:.9e} B={B:.9f} zeta={B/(2*fp):.9f} B/df={B/df:.4f} flags={fl}")

print("== RF-M: zwei Moden ==")
def two_Y(fr, f1, f2, z=0.01):
    w = 2*np.pi*fr; out = 0
    for fn in (f1, f2):
        wn = 2*np.pi*fn; out = out + 1j*w/(wn**2-w**2+2j*z*wn*w)
    return out
dfm = 0.05
for f2 in [101.0, 103.0, 106.0, 110.0, 120.0]:
    fgrid = np.arange(1, 3000)*dfm; y = np.abs(two_Y(fgrid, 100.0, f2))
    pk = [k for k in range(1, len(y)-1) if y[k] > y[k-1] and y[k] >= y[k+1]]
    res = []
    for k in pk:
        fp, Ap, B, fl = peak_est(y, fgrid, k); res.append(f"f={fp:.4f} B={B:.4f} {fl}")
    print(f"f2={f2}: Abstand/B1={(f2-100)/2:.2f}:", res)

print("== RF-3D: Ellipse ==")
def amp3d(a): return np.sqrt(np.sum(np.abs(a)**2))
def maxel(a): return np.sqrt(0.5*(np.sum(np.abs(a)**2)+abs(np.sum(a**2))))
def minel(a): return np.sqrt(max(0.5*(np.sum(np.abs(a)**2)-abs(np.sum(a**2))), 0))
th = np.linspace(0, 2*np.pi, 200001)
for a in [np.array([1, 1j, 0]), np.array([1, 1, 0])*np.exp(0.7j), np.array([1, 0.5*np.exp(1j*np.pi/3), 0.2j]), np.array([0, 0, 1e-3*np.exp(-0.4j)])]:
    xt = np.real(a[:, None]*np.exp(1j*th[None, :])); r = np.linalg.norm(xt, axis=0)
    print(a, "PSV", amp3d(a), "max", maxel(a), "brute", r.max(), "min", minel(a), "brute", r.min())

print("== RF-U: iw-Umrechnung ==")
V = 1.0; fx = 100.0; w = 2*np.pi*fx
print("D = V/(iw) =", V/(1j*w), abs(V/(1j*w)), np.angle(V/(1j*w)), "  A = iwV =", 1j*w*V)
Y = sdof_Y(np.array([100.0]))[0]
print("SDOF Rezeptanz bei fn:", Y/(1j*w), " Akzeleranz:", 1j*w*Y)

print("== RF-K: Phasensinn / Passivitaet ==")
fgrid = np.arange(1, 4000)*0.05; Yg = two_Y(fgrid, 100.0, 120.0)
def phase_sense(Hc):
    y = np.abs(Hc); ks = [k for k in range(2, len(y)-2) if y[k] > y[k-1] and y[k] >= y[k+1]]
    sl = [np.unwrap(np.angle(Hc[k-1:k+2]))[2]-np.unwrap(np.angle(Hc[k-1:k+2]))[0] for k in ks]
    return np.mean(np.array(sl) < 0), len(ks)
for nm, Hc in [("Y", Yg), ("conj(Y)", np.conj(Yg)), ("-Y", -Yg)]:
    p, n = phase_sense(Hc); print(nm, "Anteil fallende Phase an Spitzen", p, "n", n, " Anteil Re>=0:", np.mean(Hc.real >= 0))

print("== RF-G: Punktmittel ==")
h = np.array([1+0j, -1+0j, 2j])
print("Betrag", np.abs(h).mean(), "quadr", np.sqrt((np.abs(h)**2).mean()), "|komplex|", abs(h.mean()))
```

---

## Änderungsprotokoll

| Datum | Änderung | Freigabe |
|---|---|---|
| 2026-10-29 | Erstfassung (Paket W4-1) | Nutzer, 2026-10-29 |
| 2026-10-30 | K1 eingearbeitet, Nutzerfreigabe (`FG-02_korrekturvorschlag-K1.md`). K1-1: Vorzeichen je Kanal $s_a s_b$ (2.4, 3.6, 4 P-11, 5, 6.1, 9.2 RF-H8, 11 M8). K1-2: RF-P5-Grenze (9.4). K1-3: Tabelle Diskretisierungsfehler in voller Stellenzahl (3.9). K1-4: „höchstens +5,21 %“ (3.9, 8). K1-5: Linienauswahl P-09 und Datei-Wert 0,0108 (4). K1-6: Fehlerband unten bei 0 begrenzt und gekennzeichnet (3.4, 6.3, RF-U7). K1-7: γ² des Punktmittels für die Spitzensuche, Hinweis bei vollständig NaN-γ² (3.9, 6.3). K1-8: PSV-Vergleich auch bei reinem `gueltigkeit_offen_m7` (8) | Nutzer, 2026-10-30 |
