<!-- Vom Nutzer am 2026-11-15 freigegeben (F-S1 Bildgröße beim Größenwechsel erhalten, F-S2 Wortlaut freigegeben, F-S3 H1 „je 1 N“, F-S4 kein Ebenenabstand nötig). -->

<!-- Nachtrag 2 zu FG-04: Skalierung bei der Option „Schnelle“, räumlicher Nachbarabstand d_NN in der 3D-Animation, Wortlaut der Bedeutung von θ = 0. Erstellt im Paket FG-04-N2 von strukturdynamik-experte, Stand 2026-11-15. Status: ZUR FREIGABE (noch nicht vom Nutzer freigegeben). FG-04 und Nachtrag 1 sind unverändert. -->

# FG-04, Nachtrag 2 – Schnelle: Skalierung und Pflichtangabe · d_NN im Raum · Wortlaut „θ = 0“

> **Status:** Entwurf zur Freigabe. Ergänzt FG-04 (3.1, 3.5, 4, 5) und Nachtrag 1 (Abschnitt 4, letzter Punkt). Widerspricht keiner freigegebenen Festlegung; **präzisiert** drei Stellen: (1) FG-04 3.5 Pflichtangabe (a) und $s$ für die Option „Schnelle“, (2) FG-04 3.5 „$d_\mathrm{NN}$ wie ADR-025“ für die 3D-Animation, (3) die Beschriftung der Bedeutung von $\theta=0$. Anlass: Fachabnahme FA-AN3 (MAJOR-1, MINOR-4, MINOR-2).

## 1 Zweck und Umfang

| Nr. | Frage | Abschnitt |
|---|---|---|
| N2-1 | Wie ist die Darstellungsskalierung bei „Schnelle“ definiert, benannt, mit Einheit angegeben; wie lauten $s_\mathrm{auto}$, $D_\mathrm{ref}$, Pflichtangabe (a), Überlagerungshinweis? (FA-AN3 MAJOR-1) | 3.1 bis 3.4 |
| N2-2 | Welcher Abstand $d_\mathrm{NN}$ gilt in der 3D-Animation? (FA-AN3 MINOR-4) | 4 |
| N2-3 | Genauer Wortlaut der Bedeutung von $\theta=0$ für Auslenkung (absolut, relativ) und Schnelle (FA-AN3 MINOR-2) | 5 |

**Nicht Teil:** Farbbereich und `TwoSlopeNorm` (MINOR-1), Rangfolge der Kennzeichen (MINOR-3), Angabe der Komponente in Zeile (c) (MINOR-5; Empfehlung dazu in Abschnitt 8), Layout der Pflichtangaben (`ui-designer`), Änderung am Code.

Belegkennzeichen wie in FG-04: **[A]** eigene Herleitung, **[N]** numerisch im Prüfskript (Anhang), **[ANN]** Annahme.

## 2 Konventionen

Es gelten FG-04 Abschnitt 2, Nachtrag 1 Abschnitt 2 und KONVENTIONEN.md. Zusätzlich:

| Größe | Festlegung |
|---|---|
| $\hat v_{pc}$, $\hat w_{pc}$ | komplexe Amplitude der Schnelle (m/s bzw. (m/s)/N), bei relativem Bezug gedreht ($\hat w$, Nachtrag 1); sonst $\hat w:=\hat v$ |
| $\kappa$ | **Skalierung** der Option „Schnelle“ in **s** (Sekunde). Bildstrecke = $\kappa\cdot$ Schnelle. Im Code `skalierung_s`; in Beschriftungen ohne Symbol („Skalierung 7,250 s“), damit es nicht mit dem Linienindex $k^\ast$ verwechselt wird |
| $s$ | **Überhöhung** der Option „Auslenkung“ (dimensionslos, FG-04 3.5) |
| $s_\ddot{a}$ | **Äquivalente Überhöhung** der Option „Schnelle“: $s_\ddot{a}=\kappa\,\omega$ (dimensionslos). Faktor, um den die gezeigte Amplitude größer ist als die reale Auslenkungsamplitude |
| $D_{\mathrm{ref},v}$, $D_{\mathrm{ref},d}$ | größte Spitzenschnelle bzw. Spitzenauslenkung der animierten Punkte; $D_{\mathrm{ref},v}=\omega\,D_{\mathrm{ref},d}$ |
| $d_\mathrm{NN}$, $d_\mathrm{NN,min}$ | Median bzw. Minimum der räumlichen Nächste-Nachbar-Abstände (Abschnitt 4), in m |
| Zahlenanzeige | 4 signifikante Stellen (KONVENTIONEN, Nutzerentscheidung 2026-11-11), Dezimalkomma nach Stil der Oberfläche; Beträge außerhalb 0,001 bis 1 000 000 in „m·10ⁿ“ |
| Testtoleranz | halbe Einheit der letzten angegebenen Stelle (KONVENTIONEN, Nutzerentscheidung 2026-11-14); Textvergleiche exakt |

## 3 Skalierung bei der Option „Schnelle“ (N2-1)

### 3.1 Herleitung [A, N]

FG-04 3.2 definiert die Bildposition mit $s$ und der Auslenkung. Bei der Option „Schnelle“ (FG-04 3.1, E1 b) entfällt die Division durch $i\omega$, die Bildposition ist
$$\boxed{\;\vec x_p(\theta)=\vec X_p+\kappa\sum_{c}\vec e_c\,\mathrm{Re}\{\hat w_{pc}\,e^{i\theta}\}\;}\qquad[\mathrm m],\quad[\kappa]=\mathrm s .$$
Einheiten: $\kappa\,[\mathrm s]\cdot\hat w\,[\mathrm{m/s}]=\mathrm m$. Eine dimensionslose Überhöhung ist hier nicht möglich: Die Größe, die im Bild als Strecke gezeigt wird, ist nicht die Auslenkung. Wird $\kappa$ wie $s$ „Überhöhung ×“ genannt, ist das ein Einheitenfehler, und die Zahl lässt sich nicht mit der Auslenkung vergleichen (FA-AN3: Beispiel „×7,250“ statt tatsächlich ×4555).

**Bezug zur Auslenkung.** Mit $\hat d=\hat w/(i\omega)$ ist $\hat w=i\omega\hat d$ und $\mathrm{Re}\{\hat w e^{i\theta}\}=\omega\,\mathrm{Re}\{\hat d e^{i(\theta+\pi/2)}\}=\omega\,d(\theta+\pi/2)$ (FG-04 3.1, RF-A13). Also
$$\vec x_p^{\,\text{Schnelle}}(\theta;\kappa)=\vec x_p^{\,\text{Auslenkung}}(\theta+\tfrac{\pi}{2};\,s=\kappa\omega),\qquad s_\ddot{a}:=\kappa\,\omega .$$
Das Bild der Schnelle ist das Bild der Auslenkung mit der Überhöhung $s_\ddot{a}$, um $T/4$ in der Zeit verschoben. Die **reale Überhöhung gegenüber der Auslenkung ist $s_\ddot{a}=\kappa\omega$**, nicht $\kappa$. Wegen $\omega$ der gewählten Linie $f_{k^\ast}$ (nicht $f_\mathrm{wahl}$, FG-04 RF-A9) hängt $s_\ddot{a}$ von der Linie ab, $\kappa$ nicht.

### 3.2 Voreinstellung und Bezugsgröße [A, N]

- $D_{\mathrm{ref},v}$: Einzelkomponente $\max_p\lvert\hat w_{pc}\rvert$; 3D: größte große Halbachse der Bahnellipse der Schnelle über die **animierten** Punkte (Maske wie FG-04 3.6, RF-A8). Es gilt $D_{\mathrm{ref},v}=\omega D_{\mathrm{ref},d}$, weil $\hat d$ aus $\hat w$ nur durch einen gemeinsamen Faktor $-i/\omega$ (Drehung um $-\pi/2$ und Division durch $\omega$) hervorgeht; die Halbachsen ändern sich um $1/\omega$.
- **Voreinstellung:** $\kappa_\mathrm{auto}=\alpha\,d_\mathrm{NN}/D_{\mathrm{ref},v}$ mit $\alpha=0{,}25$ (Gestaltungsvorschlag, FG-04 3.5) und $d_\mathrm{NN}$ nach Abschnitt 4. Einheit s.
- **Folge:** $s_{\ddot{a},\mathrm{auto}}=\kappa_\mathrm{auto}\,\omega=\alpha\,d_\mathrm{NN}/D_{\mathrm{ref},d}$ ist **identisch** zu $s_\mathrm{auto}$ der Option „Auslenkung“. Die größte gezeigte Strecke ist in beiden Fällen $\alpha\,d_\mathrm{NN}$ ($=\kappa D_{\mathrm{ref},v}$). Ein Wechsel Auslenkung ↔ Schnelle mit Voreinstellung ändert die Bildgröße nicht, nur den Zeitnullpunkt (FG-04 3.1).
- **Manuelle Eingabe:** Der Nutzer gibt bei „Schnelle“ $\kappa$ in s ein; die Oberfläche zeigt $s_\ddot{a}=\kappa\omega$ daneben (nur lesend). Zahlenfelder nach KONVENTIONEN.

### 3.3 Pflichtangabe (a), Pflichtangabe (b) [A]

Der Text von (a) hängt von der Größe ab. Die Zahl $s_\ddot{a}$ steht **immer** im Bild, damit Thesis-Leser Auslenkung und Schnelle vergleichen können.

| Größe | (a) Wortlaut (Beispiel RF-S1) |
|---|---|
| Auslenkung (unverändert, FA-AN3 ✅) | `Überhöhung ×4555` |
| Schnelle | `Skalierung 7,250 s (Bild = Skalierung · Schnelle) · Amplitude wie Auslenkung mit Überhöhung ×4555` |

Vorlage Schnelle: `Skalierung {κ} s (Bild = Skalierung · Schnelle) · Amplitude wie Auslenkung mit Überhöhung ×{s_ä}`; $\kappa$ und $s_\ddot{a}$ mit je 4 signifikanten Stellen, $s_\ddot{a}=\kappa\omega$ mit $\omega$ der Linie. „Überhöhung ×“ steht bei Schnelle **nur** mit $s_\ddot{a}$, nie mit $\kappa$.

(b) bei Schnelle nennt **beide** realen Spitzenwerte, damit $s_\ddot{a}$ nachprüfbar ist:
`größte reale Spitzenschnelle D_ref = 1,00 mm/s (Spitzenauslenkung 1,59 µm)`
(bei H1: `… 1,00 (mm/s)/N (Spitzenauslenkung 1,59 µm/N)`). Prüfung für den Leser: $\kappa D_{\mathrm{ref},v}=7{,}250\,\mathrm s\cdot1{,}00\,\mathrm{mm/s}=7{,}25$ mm $=s_\ddot{a}\cdot D_{\mathrm{ref},d}=4555\cdot1{,}59\,\mu\mathrm m$. Bei Auslenkung bleibt (b) wie in FG-04 3.5.

Zeilen (c) und (d) unverändert, (d) siehe Abschnitt 5.

### 3.4 Obergrenze und Überlagerungshinweis [A, N]

Die Bedingung aus FG-04 3.5 ($s\,D_\mathrm{ref}\ge d_\mathrm{NN,min}/2$) ist eine Aussage über die **Bildstrecke**: $s\,D_{\mathrm{ref},d}$ und $\kappa D_{\mathrm{ref},v}$ sind beide die größte gezeigte Strecke. Für Schnelle lautet sie
$$\kappa\,D_{\mathrm{ref},v}\ \ge\ d_\mathrm{NN,min}/2\ \Longleftrightarrow\ s_\ddot{a}\,D_{\mathrm{ref},d}\ \ge\ d_\mathrm{NN,min}/2 .$$
Der Hinweis „Punkte können sich überlagern“ erscheint ab dieser Grenze, keine Sperre. Der Code (`ueberhoehung_hinweis(κ, D_ref,v, d_NN,min)`) wertet das bereits richtig aus; nur der Text (a) war falsch. Referenz RF-S5.

### 3.5 Annahmen zu 3.1 bis 3.4

- **[ANN S-1]** Bei manuellem Wert und Wechsel der Größe bleibt die **Bildgröße** erhalten (Empfehlung): $s_\ddot{a}$ wird beibehalten, $\kappa=s_\ddot{a}/\omega$ bzw. $s=\kappa\omega$. Alternativ zurück auf Voreinstellung. Beides ist ehrlich, solange (a) die neue Einheit zeigt. Rückfrage F-S1.
- **[ANN S-2]** Mit Quelle H1 sind alle Bildgrößen auf 1 N Kraft bezogen (FG-04 RF-A1: „je N“). Formal tragen $s$ und $\kappa$ dann die Einheit N bzw. N·s; die Anzeige nennt „s“ und in (c) „je 1 N“. FG-04 behandelt $s$ bei H1 ebenso. Rückfrage F-S3.
- **Unsicher:** Was PSV bei „Schnelle“ skaliert (RA-1 aus FG-04), ist unbekannt. Diese Festlegung gilt für die Software, nicht als Nachbildung von PSV.

## 4 Nachbarabstand $d_\mathrm{NN}$ in der 3D-Animation (N2-2)

### 4.1 Festlegung [A]

Für die 3D-Animation gilt der **räumliche euklidische Abstand** der Ruhelagen $\vec X_p$ in m:
$$d_{\mathrm{NN},i}=\min_{j\ne i,\ \lVert\vec X_i-\vec X_j\rVert_2>0}\lVert\vec X_i-\vec X_j\rVert_2,\qquad d_\mathrm{NN}=\mathrm{median}_i\,d_{\mathrm{NN},i},\quad d_\mathrm{NN,min}=\min_i d_{\mathrm{NN},i}.$$
- Über **alle** Punkte der Geometrie (auch maskierte, ungültige und stehende; FG-04 6 „aus allen Punkten“), weil sie als Ruhelage im Bild stehen und beim Überlagerungshinweis mitzählen.
- Doppelte Punkte (Abstand 0) zählen nicht als Nachbar (wie der Code).
- Dies **ersetzt für die 3D-Animation** die Angabe „wie ADR-025“ in FG-04 3.5. ADR-025 und Ansicht 4 messen in der Ansichtsebene; das bleibt für die Phasenansicht unverändert.

### 4.2 Begründung [A, N]

1. **Die Bewegung ist räumlich.** In 3D hat jede Bahn drei Freiheitsgrade, die Bahnellipse liegt im Raum, nicht in der Bildebene (FG-04 3.4). Zwei Nachbarn mit Abstand $d$ können sich nur berühren, wenn $2\,s\,D_\mathrm{ref}\ge d$ gilt [A]: Jeder Punkt bewegt sich höchstens um $s\,D_\mathrm{ref}$ (große Halbachse), der Abstand bleibt $\ge d-2sD_\mathrm{ref}>0$ (Dreiecksungleichung). Das ist im Raum mit dem 3D-Abstand genau und von der Blickrichtung unabhängig.
2. **Die 3D-Ansicht ist drehbar.** Ein Abstand in einer festen Ebene hängt von der Wahl der Ebene ab; für die Ansicht gibt es keine ausgezeichnete.
3. **Die Projektion verkleinert nur.** Der projizierte Abstand ist $\le$ 3D-Abstand. In der Ebene gemessen wäre $d_\mathrm{NN}$ bei geneigter Geometrie zu klein und $s_\mathrm{auto}$ damit zu klein, ohne dass die Bildreihe dadurch lesbarer wird.
4. **Gleichheit bei ebenen Geometrien parallel zu einer Koordinatenebene** (RF-D1): kein Unterschied zur bisherigen Festlegung, bestehende Ergebnisse bleiben.

**Zahlenbeispiel (RF-D1) [N]:** Raster 29 mm um 60° um die X-Achse gekippt: 3D-Median 29,00 mm, in der XY-Ebene 14,50 mm ($=29\cos60^\circ$). Mit $D_\mathrm{ref}=1{,}59$ µm ergibt sich $s_\mathrm{auto}=4555$ (3D) gegen 2278 (Ebene).

### 4.3 Gültigkeit und Grenzen

- Koordinaten im Koordinatensystem der Geometrie, in m. Maßstab und Einheit des Koordinatenimports sind Voraussetzung (nicht Gegenstand).
- **Kein** Hinweis auf **scheinbare** Überlagerung in der Projektion: Zwei Punkte können in einer Blickrichtung hintereinander liegen, ohne sich im Raum zu nähern. Das ist eine Eigenschaft der Ansicht und wird nicht gemeldet. Wird später eine 2D-Projektion der Animation (Aufsicht) eingeführt, ist dafür eine eigene Festlegung nötig (Ebene, Rückfrage F-S4).
- Nur ein Punkt: $d_\mathrm{NN}$ nicht definiert, $s$ bzw. $\kappa$ nur durch Nutzereingabe (FG-04 6, RF-D3).
- Hinweis für die Umsetzung (nicht fachlich): Der Speicher der Abstandsmatrix wächst mit $24P^2$ Byte (P = 1000: 23 MiB; P = 5000: 572 MiB [N]). Bei sehr großen $P$ ist ein blockweises Verfahren nötig; das Ergebnis darf sich nicht ändern.

## 5 Wortlaut der Bedeutung von $\theta=0$ (N2-3)

### 5.1 Herleitung [A, N]

Die Uhr $\theta$ hat zwei Nullpunkte (FG-04 3.2, Nachtrag 1 Abschnitt 3.1, 4):

- **Absolut:** $\theta=0$ ist der Zeitpunkt, an dem das Referenzsignal Ref1 sein positives Maximum hat ($\mathrm{Ref1}\propto\cos\omega t$). Das gilt für Auslenkung **und** Schnelle gleich, weil die Uhr am Referenzsignal hängt, nicht an der gezeigten Größe. Punkt mit $\varphi=0$: Schnelle im positiven Maximum, Auslenkung steigt durch null. Punkt mit $\varphi=\pi$: Schnelle im negativen Maximum (Gegenphase). Vorläufig, bis M8 bestätigt ist.
- **Relativ:** Nach der Drehung ist die Bezugskomponente $\hat w_{b,c_b}=\lvert\hat v_{b,c_b}\rvert$ reell und positiv (Nachtrag 1 Abschnitt 4). Dann gilt
  $$d_{b,c_b}(\theta)=\tfrac{\lvert\hat v\rvert}{\omega}\sin\theta\ \ (\text{Auslenkung steigt bei }\theta=0\text{ durch null, positives Maximum bei }90^\circ),$$
  $$u_{b,c_b}(\theta)=\lvert\hat v\rvert\cos\theta\ \ (\text{Schnelle im positiven Maximum bei }\theta=0,\ \text{Nulldurchgang bei }90^\circ).$$
  Bei der Option „Schnelle“ ist das **Bild** (nicht die reale Auslenkung) bei $\theta=0$ im Maximum; die reale Auslenkung desselben Punkts steigt zu diesem Zeitpunkt durch null (3.1: Bild eilt um $90^\circ$ vor).

**Gültigkeit der Aussage:** nur für die Bezugskomponente $c_b$ des Bezugspunkts $b$. Alle anderen Komponenten und Punkte haben ihre Phase gegen diese (RF-T5): Bei DS1 steht $d_{0X}(0)/(\lvert\hat v_{0X}\rvert/\omega)=-0{,}8660$, nicht 0. Der Satz darf deshalb im 3D-Modus nicht ohne Einschränkung für „den Punkt“ stehen.

### 5.2 Festgelegte Texte (Zeile (d), zweiter Satz)

Zeile (d) bleibt `θ = {θ}° · Bezug: …` (Nachtrag 1). Dahinter, als eigener Satz bzw. eigene Zeile, steht der **Nullpunkt-Satz** (immer vorhanden, auch im exportierten Standbild und in der Textalternative). Platzhalter: `{R}` Referenzname (z. B. Ref1), `{n}` Originallabel des Bezugspunkts (wie in `Bezug: …`), `{C}` X, Y oder Z (Bezugskomponente; bei Einzelkomponente die gewählte).

| Größe | Bezug | Modus | Nullpunkt-Satz |
|---|---|---|---|
| Auslenkung | absolut | Einzel und 3D | `θ = 0°: {R} im positiven Maximum` |
| Schnelle | absolut | Einzel und 3D | `θ = 0°: {R} im positiven Maximum` |
| Auslenkung | relativ | Einzel | `θ = 0°: Auslenkung von Punkt {n}, Komponente {C} steigt durch null; positives Maximum bei θ = 90°` |
| Auslenkung | relativ | 3D | wie Einzel, Zusatz: `; andere Komponenten mit festem Phasenversatz` |
| Schnelle | relativ | Einzel | `θ = 0°: Schnelle von Punkt {n}, Komponente {C} im positiven Maximum; Nulldurchgang bei θ = 90°` |
| Schnelle | relativ | 3D | wie Einzel, Zusatz: `; andere Komponenten mit festem Phasenversatz` |

Hinweise: „steigt“ heißt in positiver Achsrichtung des Koordinatensystems der Geometrie (FG-04 2). Bei absolutem Bezug bleibt das Kennzeichen M8 (Polarität unbestätigt) Pflicht; ohne M8 wäre der Satz nicht prüfbar (bei vertauschter Polarität wäre $\theta=0$ das Minimum von Ref1). Das Wort „Auslenkung“ bzw. „Schnelle“ im relativen Satz ist die animierte Größe; bei Schnelle gilt zusätzlich die Zeile (a) (3.3). Dezimalzeichen und Grad nach Stil der Oberfläche; die Zahlen 0° und 90° sind feste Texte.

## 6 Ergebnisformeln (Zusammenfassung)

| Größe | Formel | Einheit |
|---|---|---|
| Bildposition, Schnelle | $\vec x_p(\theta)=\vec X_p+\kappa\sum_c\vec e_c\,\mathrm{Re}\{\hat w_{pc}e^{i\theta}\}$ | m |
| Äquivalente Überhöhung | $s_\ddot{a}=\kappa\,\omega$, $\omega=2\pi f_{k^\ast}$ | 1 |
| Bezugsgröße Schnelle | $D_{\mathrm{ref},v}=\omega D_{\mathrm{ref},d}$ | m/s |
| Voreinstellung | $\kappa_\mathrm{auto}=\alpha d_\mathrm{NN}/D_{\mathrm{ref},v}$, $\alpha=0{,}25$; $s_{\ddot{a},\mathrm{auto}}=\alpha d_\mathrm{NN}/D_{\mathrm{ref},d}$ | s; 1 |
| Größte Bildstrecke | $\kappa D_{\mathrm{ref},v}=s_\ddot{a}D_{\mathrm{ref},d}=\alpha d_\mathrm{NN}$ (Voreinstellung) | m |
| Überlagerungshinweis | $\kappa D_{\mathrm{ref},v}\ge d_\mathrm{NN,min}/2$ | m |
| Zusammenhang | $\vec x^{\,\text{Schnelle}}(\theta;\kappa)=\vec x^{\,\text{Auslenkung}}(\theta+\pi/2;\ s=\kappa\omega)$ | m |
| Nachbarabstand 3D | $d_{\mathrm{NN},i}=\min_{j\ne i,\,d_{ij}>0}\lVert\vec X_i-\vec X_j\rVert_2$; Median bzw. Minimum | m |

## 7 Referenzfälle (Tests)

Alle Sollwerte [N] im Prüfskript (Anhang). $f_{k^\ast}=100{,}000$ Hz, $\omega=628{,}3185307$ rad/s, $d_\mathrm{NN}=29{,}00$ mm, $\alpha=0{,}25$. **Toleranz:** halbe Einheit der letzten angegebenen Stelle (KONVENTIONEN, 2026-11-14). Begründung: Die Sollwerte sind geschlossene Ausdrücke in float64, der Rundungsrest ist kleiner als $10^{-15}$ relativ, also weit unter jeder angegebenen Stelle. Nullwerte tragen die Toleranz der Stelle der übrigen Werte der Zeile (Rundungsreste $\le2\cdot10^{-18}$ m). Texte werden exakt verglichen.

### 7.1 Skalierung bei Schnelle (CPH, Einzelkomponente, zwei Punkte)

Punkt 1: $\hat v=1{,}000$ mm/s, Phase 0; Punkt 2: $\hat v=0{,}5000$ mm/s, Phase 0; $\theta_n=0,\ \pi/2,\ \pi,\ 3\pi/2$.

| ID | Eingang | Sollwert | Toleranz |
|---|---|---|---|
| **RF-S1** Voreinstellung | Option „Schnelle“, $\alpha=0{,}25$ | $D_{\mathrm{ref},v}=1{,}000000$ mm/s; $D_{\mathrm{ref},d}=1{,}591549$ µm; $\kappa_\mathrm{auto}=7{,}250000$ s; $s_\ddot{a}=4555{,}3093$; $s_\mathrm{auto}$(Auslenkung)$=4555{,}3093$ (gleich); größte Bildstrecke $\kappa D_{\mathrm{ref},v}=7{,}250000$ mm; Verhältnis Punkt 2/Punkt 1 $=0{,}5000000$. Bild Punkt 1 bei $\theta_n$: $+7{,}250000;\ 0;\ -7{,}250000;\ 0$ mm; Punkt 2: $+3{,}625000;\ 0;\ -3{,}625000;\ 0$ mm | $\pm5\cdot10^{-7}$ mm bzw. $\pm5\cdot10^{-7}$ µm, $\pm5\cdot10^{-5}$ ($s_\ddot{a}$), $\pm5\cdot10^{-7}$ (Verhältnis), $\pm5\cdot10^{-7}$ s |
| **RF-S1t** Texte | wie RF-S1 | (a) `Skalierung 7,250 s (Bild = Skalierung · Schnelle) · Amplitude wie Auslenkung mit Überhöhung ×4555`; (b) `größte reale Spitzenschnelle D_ref = 1,00 mm/s (Spitzenauslenkung 1,59 µm)`; bei Option „Auslenkung“ mit denselben Daten: (a) `Überhöhung ×4555`, (b) `größte reale Spitzenauslenkung D_ref = 1,59 µm` | exakt |
| **RF-S2** Gleichheit mit Auslenkung | RF-S1, Schnelle mit $\kappa=7{,}250$ s gegen Auslenkung mit $s=4555{,}3093$ | $\vec x^{\,\text{Schnelle}}(\theta)=\vec x^{\,\text{Auslenkung}}(\theta+\pi/2)$ für 13 Stützstellen $\theta=0\dots2\pi$, beide Punkte; Auslenkung bei $\theta_n$ (Punkt 1): $0;\ +7{,}250000;\ 0;\ -7{,}250000$ mm (gemessen max. Abweichung $1{,}7\cdot10^{-18}$ m) | $\pm5\cdot10^{-10}$ m |
| **RF-S3** manuelles $\kappa$ | $\kappa=2{,}000$ s | $s_\ddot{a}=1256{,}637$; Bildamplitude Punkt 1 / 2: $2{,}000000$ / $1{,}000000$ mm; (a) `Skalierung 2,000 s (Bild = Skalierung · Schnelle) · Amplitude wie Auslenkung mit Überhöhung ×1257` | $\pm5\cdot10^{-4}$ ($s_\ddot{a}$), $\pm5\cdot10^{-7}$ mm; Text exakt |
| **RF-S4** Linie statt Wunschfrequenz | $f_\mathrm{wahl}=100{,}2$ Hz, $\Delta f=0{,}625$ Hz, $\kappa=7{,}250$ s | Linie 100,000 Hz (Index 159); $s_\ddot{a}=4555{,}3093$. Mit $f_\mathrm{wahl}$ gerechnet wäre es $4564{,}4200$ ($+0{,}2000\,\%$): der Test muss das unterscheiden | $\pm5\cdot10^{-5}$ |
| **RF-S5** Überlagerungshinweis | $\kappa=14{,}4$ s und $14{,}6$ s, $d_\mathrm{NN,min}=29{,}00$ mm | $\kappa D_{\mathrm{ref},v}=14{,}40$ mm bzw. $14{,}60$ mm gegen $14{,}50$ mm: bei 14,4 s **kein** Hinweis, bei 14,6 s „Punkte können sich überlagern“; $s_\ddot{a}D_{\mathrm{ref},d}$ gleich $\kappa D_{\mathrm{ref},v}$ | exakt (Vergleich), $\pm5\cdot10^{-3}$ mm |
| **RF-S6** Quelle H1 | $\hat v=1{,}000$ (m/s)/N ein Punkt, $d_\mathrm{NN}=29{,}00$ mm | $D_{\mathrm{ref},d}=1{,}591549$ mm/N; $\kappa_\mathrm{auto}=7{,}250\cdot10^{-3}$ (je 1 N); $s_\ddot{a}=4{,}5553$ | $\pm5\cdot10^{-7}$ mm/N, $\pm5\cdot10^{-6}$ s, $\pm5\cdot10^{-5}$ |
| **RF-S7** Negativtest (a) | RF-S1 | Der Text (a) der Option „Schnelle“ enthält **nicht** `Überhöhung ×7,250`; $s_\ddot{a}\ne\kappa$ (Faktor $\omega=628{,}3185$) | exakt |

### 7.2 Nachbarabstand im Raum

| ID | Eingang | Sollwert | Toleranz |
|---|---|---|---|
| **RF-D1** geneigte Ebene | $\vec X_0=(0,0,0)$, $\vec X_1=(29{,}00,0,0)$ mm, $\vec X_2=(0;\ 14{,}50;\ 25{,}1147)$ mm ($29\cdot(\cos60^\circ,\sin60^\circ)$ in der Y-Z-Ebene) | 3D: $d_{\mathrm{NN},i}=29{,}00;\ 29{,}00;\ 29{,}00$ mm, Median 29,00 mm, Minimum 29,00 mm. Zum Vergleich (nicht gelten lassen) XY: $14{,}50;\ 29{,}00;\ 14{,}50$ mm, Median 14,50 mm. Mit $D_\mathrm{ref}=1{,}591549$ µm: $s_\mathrm{auto}=4555{,}309$ (3D) gegen $2277{,}655$. Parallele Ebene ($z=100$ mm): 3D = XY = 29,00 mm | $\pm5\cdot10^{-3}$ mm; $\pm5\cdot10^{-4}$ (s) |
| **RF-D2** nicht animierter Punkt zählt | RF-D1 plus $\vec X_3=(5{,}000;0;0)$ mm (maskiert) | $d_{\mathrm{NN},i}=5{,}000;\ 24{,}00;\ 29{,}00;\ 5{,}000$ mm; Median 14,50 mm; Minimum 5,000 mm; $s_\mathrm{auto}=2277{,}655$ | $\pm5\cdot10^{-3}$ mm |
| **RF-D3** Ausschlüsse | (i) RF-D1 plus Duplikat von $\vec X_0$; (ii) ein einziger Punkt | (i) Ergebnis wie RF-D1 (Abstand 0 zählt nicht); (ii) $d_\mathrm{NN}$ nicht definiert, `None`, $s$ nur durch Eingabe | exakt |
| **RF-D4** Grenzfall Berührung | Nachbarpaar 29,00 mm, größte Auslenkung 14,40 mm; 14,50 mm; 14,60 mm | Mindestabstand $\max(d-2A,0)=0{,}20$ mm; $0$; $0$. Nur ab $A\ge14{,}50$ mm Berührung möglich | $\pm5\cdot10^{-3}$ mm |

### 7.3 Wortlaut und Bedeutung von $\theta=0$

Daten $\hat w$ der Bezugskomponente: $\lvert\hat v\rvert=1{,}000$ mm/s, $\omega=628{,}3185$ rad/s, $a=\lvert\hat v\rvert/\omega=1{,}591549$ µm.

| ID | Eingang | Sollwert | Toleranz |
|---|---|---|---|
| **RF-T1** relativ, Auslenkung | Bezugskomponente, nach Drehung reell positiv | $d(0)=0$ µm; $d(\varepsilon)>0$ ($\varepsilon=10^{-3}$ rad); $d(\pi/2)=+1{,}591549$ µm (Maximum) | $\pm5\cdot10^{-7}$ µm |
| **RF-T2** relativ, Schnelle | wie RF-T1 | $u(0)=+1{,}000000$ mm/s (Maximum); $u(\varepsilon)<u(0)$; $u(\pi/2)=0$ mm/s | $\pm5\cdot10^{-7}$ mm/s |
| **RF-T3** zweiter Punkt relativ | $\Delta\varphi=0{,}7$ rad | $d(0)/a=\sin0{,}7=0{,}6442177$; $u(0)/\lvert\hat v\rvert=\cos0{,}7=0{,}7648422$ | $\pm5\cdot10^{-7}$ |
| **RF-T4** absolut | $\varphi=0$ bzw. $\varphi=\pi$ (gegen Ref1) | $\varphi=0$: $d(0)=0$, $u(0)=+1{,}000$ mm/s; $\varphi=\pi$: $u(0)=-1{,}000$ mm/s | $\pm5\cdot10^{-4}$ mm/s |
| **RF-T5** nur Bezugskomponente (3D) | DS1 (Nachtrag 1), Pivot Y, Punkt 0 | $d_c(0)/(\lvert\hat v_c\rvert/\omega)=-0{,}8660254;\ 0;\ -0{,}9923714$ (X, Y, Z); $u_c(0)/\lvert\hat v_c\rvert=0{,}5000000;\ 1{,}000000;\ 0{,}1232843$. Nur die Y-Spalte erfüllt den Nullpunkt-Satz | $\pm5\cdot10^{-7}$ |
| **RF-T6** Texte | Punkt 100, Komponente X, Referenz Ref1 | Auslenkung/Schnelle absolut: `θ = 0°: Ref1 im positiven Maximum`; Auslenkung relativ Einzel: `θ = 0°: Auslenkung von Punkt 100, Komponente X steigt durch null; positives Maximum bei θ = 90°`; Schnelle relativ Einzel: `θ = 0°: Schnelle von Punkt 100, Komponente X im positiven Maximum; Nulldurchgang bei θ = 90°`; 3D relativ: Zusatz `; andere Komponenten mit festem Phasenversatz` | exakt |

## 8 Anforderungen an die Umsetzung (aus der Fachgrundlage, nicht Code)

Nur als Folge der Festlegungen, damit der `software-engineer` nichts raten muss:
1. `pflichttexte`: (a) und (b) nach 3.3 für „Schnelle“; $s_\ddot{a}=\kappa\,\omega$ mit $\omega$ der Linie (`omega_rad_s` der `AnimationsDaten`, nicht $f_\mathrm{wahl}$). Der Test prüft die **Strings** (RF-S1t, RF-S7), nicht nur Stichwörter.
2. (d): Nullpunkt-Satz nach 5.2, auch in Export und Textalternative. M8 bei absolutem, M12 im 3D-Modus gesetzt (FA-AN3 NITPICK).
3. Datenvertrag: `s_auto` hat bei Schnelle die Einheit s; das ist im Docstring und im Feldnamen sichtbar zu machen (z. B. `skalierung_auto_s`) oder durch eine abgeleitete Größe $s_\ddot{a}$ zu ergänzen. Nicht still beides „Überhöhung“ nennen.
4. $d_\mathrm{NN}$: kein Codeunterschied (Abschnitt 4); der Docstring nennt „räumlich, FG-04 N2“.
5. Empfehlung zu FA-AN3 MINOR-5: die gewählte Komponente in Zeile (c) nennen („Auslenkung Y (CPH)“); keine Festlegung dieser Fachgrundlage.

## 9 Gültigkeit und Randfälle

- **Linearität und Stationarität** wie FG-04 6. $s_\ddot{a}$ ist nur eine Veranschaulichung, keine Verformung (FG-04 3.5).
- $\omega>0$ (FG-04 3.1). Bei $\omega=0$ ist $s_\ddot{a}$ nicht definiert: NaN, Anzeige „–“.
- $D_{\mathrm{ref},v}=0$ (alle $\lvert\hat v\rvert=0$): keine Voreinstellung (FG-04 6).
- Sehr kleines oder großes $\kappa$ (außerhalb 0,001 bis 1 000 000): Schreibweise „m·10ⁿ“ nach KONVENTIONEN. $s_\ddot{a}$ kann durch $\omega$ um Größenordnungen von $\kappa$ abweichen (hier ×628); darum wird es nie weggelassen.
- **Schnelle als Option:** Alle Phasendifferenzen und Formen sind gleich wie bei Auslenkung (FG-04 3.1). Nur Zeitnullpunkt und Einheit der Skalierung unterscheiden sich.
- Absolut: M8 offen (Nullpunkt-Satz ist vorläufig). Relativ: unabhängig von M8 (Nachtrag 1, RF-N4).

## 10 Quellen

Alle Herleitungen und Zahlen sind eigene Rechnung [A, N]. Verwendet: FG-04 (3.1, 3.2, 3.5, 6, RF-A7, RF-A9, RF-A13), Nachtrag 1 (3.1, 4, RF-N1), ADR-025, FA-AN3, KONVENTIONEN.md, lesend `animation_daten.py` (`_naechste_abstaende_3d`, `ueberhoehung_auto`) und `animation3d.py` (`pflichttexte`). Keine Lehrbuchaussage wird als belegt behauptet.

## 11 Offene Punkte

**Rückfragen (alle nicht blockierend):**
- **F-S1:** Bei manuellem Wert und Wechsel Auslenkung ↔ Schnelle: Bildgröße erhalten ($s_\ddot{a}$ bleibt, Empfehlung) oder zurück auf Voreinstellung? *Annahme:* Bildgröße erhalten (ANN S-1).
- **F-S2:** Ist der Wortlaut (a), (b) und der Nullpunkt-Sätze in 3.3 und 5.2 so freigegeben, oder soll ein Satz kürzer sein (Platz im Bild; Layout beim `ui-designer`)? *Annahme:* Wortlaut wie Tabellen; Kürzen nur mit neuer Freigabe.
- **F-S3:** Bei H1 „je 1 N“ ohne N-Einheit in $s$, $\kappa$ (ANN S-2)? *Annahme:* ja.
- **F-S4:** Soll für eine spätere 2D-Aufsicht der Animation ein Ebenenabstand gelten (wie ADR-025)? Nicht aktuell. *Annahme:* nicht benötigt.

**Annahmen:** S-1, S-2 (3.5); Beispieldaten sind Referenzwerte, keine Gerätedaten.

**Unsicherheiten:** PSV-Verhalten bei Schnelle (RA-1) unbekannt. Lesbarkeit der längeren Zeile (a) nicht beurteilt. Der Wortlaut ist mit dem Code nicht abgeglichen (nur gelesen); Umsetzung und Abnahme folgen.

**Rechercheaufträge:** keine.

**Vorschlag für KONVENTIONEN.md:** „Option Schnelle: Skalierung in s, daneben immer die äquivalente Überhöhung $s_\ddot{a}=\kappa\omega$; $d_\mathrm{NN}$ in der 3D-Animation räumlich; Nullpunkt-Satz zu θ = 0 gehört zu den Pflichtangaben“ (nur bei Freigabe).

## Anhang: Prüfskript

Ausgeführt im Scratchpad (`fg04n2/fg04n2.py`, Python 3 mit NumPy). Die `assert`-Prüfung lief fehlerfrei („alle Pruefungen bestanden“, Zeile vor dem Abschnitt RF-D2); die gedruckten Werte sind in Abschnitt 7 übernommen.

```python
"""FG-04 Nachtrag 2 Pruefskript: Skalierung bei Schnelle, d_NN im Raum, Bedeutung von theta=0."""
import numpy as np

np.set_printoptions(precision=10, linewidth=140)
F, DF = 100.0, 0.625
OM = 2 * np.pi * F
TH = np.array([0.0, np.pi / 2, np.pi, 3 * np.pi / 2])
ALPHA, DNN = 0.25, 0.029


def re_(vh, th):
    """Re{vh e^{i th}}."""
    return np.real(vh * np.exp(1j * th))


# ---- Teil 1: Skalierung bei Schnelle ------------------------------------------------------
v1, v2 = 1e-3, 0.5e-3                      # m/s, Spitzenwerte, Phase 0
dref_v = max(abs(v1), abs(v2))             # m/s
dref_d = dref_v / OM                       # m
k_auto = ALPHA * DNN / dref_v              # s
s_aeq = k_auto * OM                        # 1
s_auto_d = ALPHA * DNN / dref_d            # Auslenkung (RF-A7)
print("OM", OM)
print("D_ref,v", dref_v, "D_ref,d", dref_d)
print("k_auto [s]", k_auto, " s_aeq", s_aeq, " s_auto(Ausl.)", s_auto_d)
assert abs(s_aeq - s_auto_d) < 1e-9 * s_auto_d
print("k*D_ref,v [m]", k_auto * dref_v, " Verh. P2/P1", (k_auto*v2)/(k_auto*v1))
bild_v1 = k_auto * re_(v1, TH)
bild_v2 = k_auto * re_(v2, TH)
print("Bild Schnelle P1 [m] bei theta_n", bild_v1)
print("Bild Schnelle P2 [m]", bild_v2)
d1 = 1e-3 / (1j * OM)                      # d^ = v^/(i w)
bild_d1 = s_aeq * re_(d1, TH)
print("Bild Ausl. P1 [m] bei theta_n   ", bild_d1)
# Bild_Schnelle(theta) = Bild_Auslenkung(theta + pi/2)
th = np.linspace(0, 2 * np.pi, 13)
dev = np.max(np.abs(k_auto * re_(v1, th) - s_aeq * re_(d1, th + np.pi / 2)))
print("max Abw. Bild_S(th) - Bild_A(th+pi/2) [m]", dev)
# reale Amplitude vs Bild
print("Faktor Bild/real (Auslenkung real) = k*omega =", k_auto * OM)

# Linie statt f_wahl
f_wahl = 100.2
kidx = int(round(f_wahl / DF)); f_lin = kidx * DF
print("Linie", kidx - 1, "(0-basiert) f_lin", f_lin, "(1-basiert k=%d)" % kidx)
om_lin = 2 * np.pi * f_lin
om_wahl = 2 * np.pi * f_wahl
print("s_aeq mit Linie", k_auto * om_lin, " mit f_wahl", k_auto * om_wahl, " rel.", om_wahl / om_lin - 1)

# Manuelles k
k_man = 2.0
print("k=2,000 s -> s_aeq", k_man * OM, " Bildamplitude P1 [m]", k_man * v1)
# Ueberlagerung
dmin = DNN
for k in (14.4, 14.5, 14.6):
    print("k", k, "k*Dref_v", k * dref_v, ">= dmin/2?", k * dref_v >= dmin / 2, " s_aeq*Dref_d", k*OM*dref_d)
# H1: v=1 (m/s)/N
v_h1 = 1.0
k_h1 = ALPHA * DNN / v_h1
print("H1 k_auto", k_h1, " s_aeq", k_h1 * OM, " D_ref,d", v_h1 / OM, "m/N")

# ---- Teil 3: theta = 0 -------------------------------------------------------------------
a = 1e-3 / OM
# relativ, Pivotkomponente: w^ = |v| (reell, positiv)
w = 1e-3
dd = w / (1j * OM)
eps = 1e-3
print("rel. Ausl.  d(0)/a, d(eps)>0, d(pi/2)/a:", re_(dd, 0.0) / a, re_(dd, eps) > 0, re_(dd, np.pi / 2) / a)
print("rel. Schn.  u(0)/w, u(eps)<u(0), u(pi/2)/w:", re_(w, 0.0) / w, re_(w, eps) < re_(w, 0.0), re_(w, np.pi / 2) / w)
# zweiter Punkt relativ dphi = 0.7
dphi = 0.7
print("Punkt dphi=0.7: d(0)/a", re_(w*np.exp(1j*dphi)/(1j*OM), 0.0) / a, " (= sin 0.7 =", np.sin(dphi), ")  u(0)/w", re_(w*np.exp(1j*dphi), 0.0)/w, "(= cos 0.7 =", np.cos(dphi), ")")
# absolut: Punkt phi=0 (gleichphasig mit Ref1) und phi=pi
for phi in (0.0, np.pi):
    vv = 1e-3 * np.exp(1j * phi)
    print("abs phi=%.4f: d(0)/a %.3e  u(0)/1e-3 %.1f" % (phi, re_(vv/(1j*OM), 0.0)/a, re_(vv, 0.0)/1e-3))
# DS1 aus Nachtrag 1, Pivot Y: nur Pivot-Komponente hat Nulldurchgang bei theta=0
e = lambda m, p: m * 1e-3 * np.exp(1j * p)
v0 = np.array([e(0.5, 0), e(1.0, np.pi/3), e(0.3, -0.4)])
psi = np.angle(v0[1])
w0 = v0 * np.exp(-1j * psi)
print("DS1 p0 arg w", np.angle(w0))
dw0 = w0 / (1j * OM)
print("DS1 p0 d_c(0)/(|v_c|/w):", re_(dw0, 0.0) / (np.abs(w0) / OM))
print("DS1 p0 u_c(0)/|v_c|   :", re_(w0, 0.0) / np.abs(w0))

# ---- Teil 2: d_NN raeumlich ---------------------------------------------------------------
def nn(x):
    diff = x[:, None, :] - x[None, :, :]
    dist = np.sqrt((diff**2).sum(2))
    dist = np.where(dist > 0, dist, np.inf)
    n = dist.min(1)
    n = n[np.isfinite(n)]
    return n

beta = np.radians(60.0)
A = 0.029
x = np.array([[0, 0, 0], [A, 0, 0], [0, A*np.cos(beta), A*np.sin(beta)]])
n3 = nn(x); nxy = nn(x[:, :2])
print("geneigt 60 Grad: NN 3D", n3, "median", np.median(n3), "min", n3.min())
print("                 NN XY", nxy, "median", np.median(nxy), "min", nxy.min())
dref = 1.5915494309189535e-6
print("s_auto 3D", ALPHA*np.median(n3)/dref, " XY", ALPHA*np.median(nxy)/dref, " Verh.", np.median(nxy)/np.median(n3), "cos60", np.cos(beta))
# parallele Ebene: gleich
xp = np.array([[0, 0, 0.1], [A, 0, 0.1], [0, A, 0.1]])
print("parallel: 3D", np.median(nn(xp)), " XY", np.median(nn(xp[:, :2])))
# doppelter Punkt wird ausgeschlossen
xd = np.vstack([x, x[0]])
print("mit Duplikat: NN", nn(xd))
# Kollisionsgrenze: Nachbarn mit Abstand d, beide Auslenkung <= A_max -> Abstand >= d - 2A
d = 0.029
for Amax in (0.0144, 0.0145, 0.0146):
    print("Amax", Amax, "2A >= d ?", 2*Amax >= d, "min. Abstand", max(d-2*Amax, 0.0))
# Speicher
for P in (100, 1000, 5000):
    print("P", P, "P*P*3*8 Byte =", P*P*3*8/2**20, "MiB")
print("alle Pruefungen bestanden")

# ---- RF-D2: nicht animierter Punkt zaehlt fuer d_NN (alle Punkte) ---------------------------
x3 = np.vstack([x, [0.005, 0.0, 0.0]])
n = nn(x3)
print("RF-D2 NN", n, "median", np.median(n), "min", n.min(), " s_auto", ALPHA*np.median(n)/dref)
xe = x[:1]
print("RF-D3 ein Punkt:", nn(xe).size)
# Bild-Strings
print("k*D_ref,v in mm", k_auto*dref_v*1e3, " D_ref,d in um", dref_d*1e6)
print("s_aeq(k=2)", 2.0*OM, " Ueberlagerung: s_aeq*D_ref,d bei 14.4 und 14.6:", 14.4*OM*dref_d, 14.6*OM*dref_d)
```
