<!-- Vom Nutzer am 2026-11-11 freigegeben (F-N1 Mechanismus C mit Voreinstellung A, F-N2 Bezugskomponente nur angezeigt, F-N3 A-2 und A-3 bestätigt). -->

<!-- Nachtrag 1 zu FG-04: skalarer Phasenbezug für einen 3D-Bezugspunkt (Frage F-A2 aus P-AUSW3). Erstellt im Paket FG-04-N1 von strukturdynamik-experte, Stand 2026-11-11. Status: ZUR FREIGABE (noch nicht vom Nutzer freigegeben). FG-04 selbst ist unverändert. -->

# FG-04, Nachtrag 1 – Welcher Skalar ist der Phasenbezug bei einem 3D-Bezugspunkt? (F-A2)

> **Status:** Entwurf zur Freigabe. Ergänzt FG-04 Abschnitt 3.2 („Zeitnullpunkt bei relativem Bezug“) für den Fall, dass der Bezugspunkt $b$ drei komplexe Komponenten hat. Widerspricht keiner freigegebenen Festlegung: Für eine Einzelkomponente ergibt sich **genau** die Formel aus FG-04 ($\hat w_p = \hat v_p\,\hat v_b^*/\lvert\hat v_b\rvert$). Baut auf FG-04 (E1–E5, A-1), FG-02 (2.1, 2.4, 3.4), FG-03 (5.3), ADR-025 und dem Plan P-AUSW3 auf.

## 1 Zweck und Frage

FG-04 3.2 definiert für eine skalare Komponente
$$\hat w_p = \hat v_p\,\frac{\hat v_b^{*}}{\lvert\hat v_b\rvert}.$$
Bei der 3D-Animation (Plan P-AUSW3, Modus „3D“) hat der Bezugspunkt $\hat{\vec v}_b = (\hat v_{bX},\hat v_{bY},\hat v_{bZ})$. Gesucht ist **ein** Phasenfaktor $e^{i\psi_b}$ (ein Skalar mit $\lvert\cdot\rvert=1$), mit dem **alle** Punkte und **alle** Komponenten gedreht werden: $\hat{\vec w}_p = \hat{\vec v}_p\,e^{-i\psi_b}$.

**Nicht Teil:** Gestaltung der Auswahl in der Oberfläche (`ui-designer`), Koordinatentransformation (R-070), Änderung von FG-04.

Belegkennzeichen wie in FG-04: **[A]** eigene Herleitung, **[N]** numerisch im Prüfskript (Anhang), **[ANN]** Annahme.

## 2 Konventionen

Alle Konventionen von FG-04 Abschnitt 2 und KONVENTIONEN.md gelten (Zeitabhängigkeit $e^{+i\omega t}$, einseitiges Spitzenwertspektrum, positives $\varphi$ = eilt voraus, Winkel in rad). Zusätzlich:

| Größe | Festlegung |
|---|---|
| $\hat{\vec v}_p\in\mathbb C^3$ | Komplexe Amplitude (Schnelle bzw. H1) von Punkt $p$ an der gewählten Linie, Komponenten $c\in\{X,Y,Z\}$ = Indizes 0, 1, 2 |
| $\psi_b$ | Bezugsphase in rad, $\psi_b\in(-\pi,\pi]$; $\hat{\vec w}_p=\hat{\vec v}_p e^{-i\psi_b}$ |
| Pivot $c_b$ | Index der Komponente des Bezugspunkts, deren Phase $\psi_b$ liefert: $\psi_b=\arg\hat v_{b,c_b}$ |
| $\arg$ | $\arg 0$ ist undefiniert; $+\pi$ statt $-\pi$ (wie `phase_relativ_rad`) |
| Animierter Punkt | alle drei Komponenten gültig (M6), $\gamma^2\ge\gamma^2_\mathrm{min}$, endlich (FG-04 3.6, **A-1**) |

## 3 Herleitung

### 3.1 Jede gemeinsame Drehung ist eine reine Zeitverschiebung [A, N]

Für beliebiges reelles $\psi$ gilt $\mathrm{Re}\{\hat{\vec v}\,e^{-i\psi}e^{i\theta}\}=\mathrm{Re}\{\hat{\vec v}\,e^{i(\theta-\psi)}\}$, also für Auslenkung und Bildposition (FG-04 3.2)
$$\vec x_p^{\,w}(\theta)=\vec x_p^{\,v}(\theta-\psi).$$
Eine **für alle Punkte und Komponenten gemeinsame** Bezugsphase verschiebt nur den Zeitnullpunkt um $\psi/\omega$. Unverändert bleiben: Beträge, Phasendifferenzen zwischen Punkten **und** zwischen Komponenten, Bahnellipsen (Halbachsen, Orientierung, Drehsinn), Amplitudenverhältnisse (RF-N1). Damit sind die Kriterien 2 bis 4 aus FG-04 3.3 für **jede** Wahl von $\psi_b$ erfüllt; Kriterium 1 gilt mit $\varphi:=\arg\hat w$:
$$\theta_{\max,pc}=\tfrac{\pi}{2}-\arg\hat w_{pc}=\tfrac{\pi}{2}-\arg\hat v_{pc}+\psi_b .$$
Die Frage F-A2 betrifft also **nur den Zeitnullpunkt**, nie Form, Richtung oder Gleichphasigkeit. Ein Fehler in $\psi_b$ (z. B. durch Rauschen) verschiebt das ganze Bild zeitlich, er verzerrt es nicht.

### 3.2 Komponentenweise Drehung ist falsch (Alternative D) [A, N]

Wendet man die FG-04-Formel naiv je Komponente an, $\hat w_{pc}=\hat v_{pc}\,\hat v_{bc}^*/\lvert\hat v_{bc}\rvert$, wird jede Komponente um ihre **eigene** Phase gedreht. Die Phasendifferenz zweier Komponenten desselben Punkts ändert sich dann um $\arg\hat v_{bc}-\arg\hat v_{bc'}\neq0$:
$$\arg\hat w_{pc}-\arg\hat w_{pc'}=(\varphi_{pc}-\varphi_{pc'})-(\varphi_{bc}-\varphi_{bc'}).$$
Das ändert die Bahnellipse. Beispiel (RF-N2): $\hat{\vec v}_b=10^{-3}(1,i,0)$ ist eine Kreisbahn; komponentenweise gedreht wird daraus $10^{-3}(1,1,0)$, eine **Linie** (Halbachsen $1{,}414\cdot10^{-3}$ und $0$). Für Komponenten, in denen $\hat v_{bc}=0$ ist, ist der Faktor undefiniert. FG-04 3.4 („Die Bildreihe darf die Komponenten nicht einzeln in der Phase angleichen“) verbietet das ausdrücklich. **Alternative D scheidet aus.** Es bleibt: $\psi_b$ ist **ein** Skalar, der aus $\hat{\vec v}_b$ abgeleitet wird.

### 3.3 Anforderungen an die Ableitung von $\psi_b$ aus $\hat{\vec v}_b$

| Nr. | Anforderung | Begründung |
|---|---|---|
| K1 | **Kovarianz:** $\psi_b(e^{i\alpha}\hat{\vec v}_b)=\psi_b(\hat{\vec v}_b)+\alpha$ (mod $2\pi$). Dann ist $\hat{\vec w}$ unabhängig von jeder gemeinsamen Drehung der Daten | Deckt M8 ($\alpha=\pi$, FG-02 2.4), eine andere Referenzphase und eine Triggerverschiebung ($\alpha=\omega\tau$) ab. Ohne K1 wäre die „relative“ Darstellung nicht relativ [A] |
| K2 | Reduktion auf FG-04 bei Einzelkomponente und bei linearem $b$ | Keine Sonderlogik, Test RF-N3 |
| K3 | Definiert für jedes $\hat{\vec v}_b\neq0$ | sonst Ausfall der Animation |
| K4 | Wenig Sprünge in $\hat{\vec v}_b$ (z. B. beim Wechsel der Linie) | nur Zeitnullpunkt, aber sichtbar und unerklärlich |
| K5 | Konsistenz mit der 2D-Phase der Einzelkomponente (ADR-025, `phase_relativ_rad`; F-A1) | „Phase der Bewegung = dargestellte Phase“ muss zwischen Standbild und Animation stimmen |
| K6 | Hängt nicht von offenen Annahmen ab (M8, M12, M13) | sonst erbt der Bezug deren Unsicherheit |
| K7 | In einem Satz erklärbar („$\theta=0$ heißt …“) | Beschriftung nach FG-04 3.5 (d) |
| K8 | Rauschrobust | der Bezug kommt aus einem einzelnen Messpunkt |

### 3.4 Die Alternativen [A, N]

**A – Phase der betragsgrößten Komponente.** $c_b=\arg\max_c\lvert\hat v_{bc}\rvert$ (Gleichstand: kleinster Index X<Y<Z), $\psi_b=\arg\hat v_{b,c_b}$.
K1 ja (Betragsauswahl ist invariant gegen Drehung, $\arg$ kovariant). K2 ja. K3 ja: $\lvert\hat v_{b,c_b}\rvert\ge\lVert\hat{\vec v}_b\rVert/\sqrt3>0$. K4: **Sprung bei Betragsgleichheit**, Größe $\lvert\arg\hat v_{bc_1}-\arg\hat v_{bc_2}\rvert$ (beliebig bis $\pi$; RF-N6: 1,0 rad bei Wechsel X→Y). K5 nur für die Komponente $c_b$ (siehe 3.5). K6 ja. K7: „Die Komponente $c_b$ von Punkt $b$ steigt bei $\theta=0$ durch null.“ K8: die größte Komponente hat den größten Betrag, die Phase wird durch die Kohärenz der Komponente bestimmt, die durch A-1 für alle drei $\ge\gamma^2_\mathrm{min}$ ist.

**B – Hauptachse der Bahnellipse (erster Singulärvektor).** Mit $S=\sum_i\hat v_{bi}^2$ ist $\psi_b=\tfrac12\arg S$ (mod $\pi$) und damit $\hat{\vec w}_b=\hat{\vec v}_b e^{-i\psi_b}$ mit $\mathrm{Re}\,\hat{\vec w}_b\perp\mathrm{Im}\,\hat{\vec w}_b$ und $\lVert\mathrm{Re}\rVert\ge\lVert\mathrm{Im}\rVert$. Beweis [A]: $\sum_i\hat w_i^2=S e^{-2i\psi_b}=\lvert S\rvert>0$ reell, Imaginärteil $=2\,\mathrm{Re}\,\hat{\vec w}\cdot\mathrm{Im}\,\hat{\vec w}=0$, Realteil $=\lVert\mathrm{Re}\rVert^2-\lVert\mathrm{Im}\rVert^2=\lvert S\rvert$. Das ist FG-03 5.3 mit $\theta^\ast=-\psi_b$. „Komponente entlang der Hauptachse“ ist dasselbe: $\vec e_\mathrm{max}\cdot\hat{\vec v}_b=\lVert\mathrm{Re}\,\hat{\vec w}_b\rVert\,e^{i\psi_b}$ (RF-N5, [N]), und der erste Singulärvektor von $[\mathrm{Re}\,\hat{\vec w}_b;\ \mathrm{Im}\,\hat{\vec w}_b]$ ist $\vec e_\mathrm{max}$; die drei Formulierungen sind äquivalent.
K1: $\psi$ ist nur **mod $\pi$** bestimmt; das Vorzeichen braucht eine Regel (FG-03: $\vec e_\mathrm{max}\cdot\vec e_\mathrm{ref}\ge0$ mit $\vec e_\mathrm{ref}=(0,0,1)$ **[ANN M13]**, bei $0$ erste nichtverschwindende Komponente positiv). Mit dieser Regel auf $\hat{\vec w}_b$ angewandt ist $\psi_b$ kovariant, **aber K6 verletzt** (hängt von M13 ab), und die Regel springt, wenn $\vec e_\mathrm{max}\perp\vec e_\mathrm{ref}$ (Sprung $\pi$ = halbe Periode). K3 **nein**: Bei Kreisbahn ($\lvert S\rvert<10^{-12}\sum\lvert\hat v_{bi}\rvert^2$) ist $\psi_b$ undefiniert (RF-N2: NaN); in der Nähe wächst die Unsicherheit ohne Grenze. K4: stetig, solange $\lvert S\rvert$ groß ist (RF-N6: größter Schritt $7{,}6\cdot10^{-5}$ rad), nahe Kreisbahn Sprung $\pi/2$ (RF-N6). K5 **nein** (siehe 3.5). K7: „Punkt $b$ erreicht bei $\theta=\pi/2$ die Spitze der großen Halbachse“ (anschaulich, aber nur bei erkennbarer Ellipse). K8: **schlecht** nahe Kreisbahn (RF-N8: Standardabweichung von $\psi_B$ bei 1 % Rauschen: 0,011 rad für Achsenverhältnis 0,5; 0,050 rad für 0,9; **0,56 rad** für 0,99 gegen 0,008/0,026/0,007 rad für A).

**C – vom Nutzer gewählte Komponente.** $c_b$ vorgegeben, $\psi_b=\arg\hat v_{b,c_b}$.
K1 ja, K2 ja, K6 ja, K7 ja (wie A). K4 stetig (RF-N6: Schritt 0). K3 nur wenn $\hat v_{b,c_b}\neq0$ (sonst `ValueError`, RF-N2/N3). **K5 ja für $c_b$** und exakt: Mit demselben $b$ und derselben Komponente ist $\arg\hat w_{p,c_b}=\Delta\varphi_p$ aus `phase_relativ_rad`. Reproduzierbar (die Wahl steht in der Beschriftung). Nachteil: eine zusätzliche Wahl für den Nutzer.

**E – globale Hauptphase ohne Bezugspunkt.** $\psi=\tfrac12\arg\sum_{p,c}\hat v_{pc}^2$. Erfüllt K1 (mod $\pi$), aber es gibt keinen Bezugspunkt mehr (ADR-025 und E4(b) verlangen ihn), die Phase hängt von allen Punkten einschließlich verrauschter ab, und bei laufender Welle ($\sum\hat v^2\approx0$) ist sie undefiniert. Nicht weiterverfolgt.

### 3.5 Konsistenz mit der 2D-Phase (ADR-025, F-A1) [A, N]

Für jeden Skalar $\psi_b$ gilt für Komponente $c'$:
$$\arg\hat w_{pc'}-\Delta\varphi^{2D}_{pc'}=\arg\hat v_{bc'}-\psi_b,\qquad \Delta\varphi^{2D}_{pc'}=\arg(\hat v_{pc'}\hat v_{bc'}^*)$$
(konstant über alle Punkte $p$). Die Differenz ist null **genau für die Pivot-Komponente** $c'=c_b$ (A, C) und im Allgemeinen für keine Komponente bei B. Für die übrigen Komponenten ist der Offset $\arg\hat v_{bc'}-\arg\hat v_{b,c_b}$ **unvermeidbar**: er ist genau der Preis dafür, dass die Phasenbeziehung zwischen den Komponenten erhalten bleibt (3.2). DS1 (RF-N1) mit Pivot Y: Offsets $-\pi/3$ (X) und $-1{,}4472$ rad (Z), identisch für alle Punkte.
**Folge für die Anzeige:** In der 3D-Animation steht die Phase „gegen Bezugskomponente $c_b$ von Punkt $b$“, nicht gegen die gleichnamige Komponente. Phasenbilder der Einzelkomponenten (ADR-025) stimmen mit der Animation nur für $c'=c_b$ in der Zahl überein; für die anderen Komponenten stimmen die **Phasendifferenzen zwischen den Punkten** überein, die absolute Zahl nicht. Das gehört in die Beschriftung (3.7).

### 3.6 Verhalten bei Kreisbahn des Bezugspunkts, Frequenzwechsel, M8

| Fall | A | B | C |
|---|---|---|---|
| Kreisbahn $\hat{\vec v}_b=10^{-3}(1,i,0)$ (RF-N2) | Gleichstand, $c_b$=X, $\psi=0$ (deterministisch) | **undefiniert** (NaN) | wohldefiniert: $\psi=0$ (X), $\pi/2$ (Y); Z: Fehler |
| Wechsel der Linie, Beträge kreuzen sich (RF-N6) | Sprung 1,0 rad (Beispiel) | stetig | stetig |
| Wechsel der Linie nahe Kreisbahn (RF-N6) | Sprung wie A | Sprung $\pi/2$ | stetig |
| M8, $\hat v\to-\hat v$ (RF-N4) | $\psi\to\psi+\pi$, $\hat w$ gleich | wie A | wie A |
| Abhängigkeit von M13 | nein | **ja** (Vorzeichenregel) | nein |

Alle drei sind kovariant (K1): $\hat w$ ändert sich bei $\hat v\to-\hat v$ nicht, die Animation ist bildgleich (FG-04 3.2, RF-A10 erweitert auf 3D, RF-N4). Nach F-A4 (Plan) führt ein Frequenzwechsel ohnehin ins Standbild zurück; die Unstetigkeit von A betrifft nur den Nullpunkt beim Durchschalten benachbarter Linien. Sie ist durch die Anzeige der gewählten Komponente erklärt.

## 4 Empfehlung

**C als Mechanismus, A als Voreinstellung für die Komponente.** Die rechnende Funktion bekommt die Bezugskomponente als Parameter (C); die Voreinstellung wählt die betragsgrößte Komponente von $b$ (A). Der Nutzer kann die Komponente überschreiben. Begründung:

1. Nur C und A erfüllen K1 bis K3 ohne Zusatzannahme; B scheitert bei Kreisbahn und nahe daran (K3, K8), braucht die Annahme M13 (K6) und hat eine mod-$\pi$-Mehrdeutigkeit mit Sprungstelle.
2. C stimmt für die Pivot-Komponente exakt mit der 2D-Phase überein (K5). Wählt der Nutzer in der 2D-Ansicht eine Komponente und schaltet zur Animation, bekommt er dieselbe Zahl für diese Komponente.
3. A ist eine eindeutige, von der Oberfläche unabhängige Voreinstellung (reproduzierbare Thesis-Abbildung: die Beschriftung nennt Punkt und Komponente), liefert nie $\lvert\hat v_{b,c_b}\rvert=0$ bei $\hat{\vec v}_b\neq0$ und vermeidet die Kreisbahn-Falle. Ihr Nachteil (Sprung bei Betragsgleichheit) betrifft nur den Zeitnullpunkt und wird angezeigt.
4. Die Entscheidung ändert Form und Phasenbeziehungen nicht (3.1).

**Festlegung für die Umsetzung** [A]:
- $c_b$: Voreinstellung $\arg\max_c\lvert\hat v_{bc}\rvert$ (`numpy.argmax`, Gleichstand kleinster Index); Überschreibung durch den Nutzer; bei Einzelkomponenten-Animation ist $c_b$ die dargestellte Komponente (dann identisch mit FG-04).
- $\hat{\vec w}_p=\hat{\vec v}_p\cdot\overline{u_b}$ mit $u_b=\hat v_{b,c_b}/\lvert\hat v_{b,c_b}\rvert$ für **alle** $p$ und **alle** drei Komponenten; die Pivot-Komponente von $b$ ist danach bis auf Rundung reell und positiv ($\lvert\mathrm{Im}\rvert<10^{-12}\lvert\hat v\rvert$), nicht bitgleich null.
- $\lvert\hat v_{b,c_b}\rvert=0$ oder nicht endlich: `ValueError`; $\hat{\vec v}_b=0$: kein gültiger Bezugspunkt.
- **Bezugspunkt in 3D muss ein animierter Punkt sein** (A-1; **[ANN A-2]**): Eine manuelle Wahl eines Punkts mit einer maskierten oder ungültigen Komponente wird mit Meldung abgelehnt, weil ein stehender Punkt keinen sichtbaren Nulldurchgang hat.
- **Voreinstellung des Bezugspunkts in 3D** (ergänzt FG-04 3.2, da `standard_bezug` ohne einzelne Komponente `None` liefert; **[ANN A-3]**): der animierte Punkt mit der größten `auslenkung_max` (große Halbachse der Bahn, FG-03 5.3), Gleichstand kleinster Index; kein animierter Punkt mit $\hat{\vec v}\neq0$: kein Bezug. Dieselbe Größe liefert $D_\mathrm{ref}$ (FG-04 3.5). Bei Wahl nach $\lVert\hat{\vec v}_p\rVert_2$ ergibt sich in RF-N7 dieselbe Reihenfolge; die Wahl ändert nur den Zeitnullpunkt.
- Bedeutung von $\theta=0$ in der Beschriftung: „Bezug: relativ zu Punkt $n$, Komponente $c_b$: deren Auslenkung steigt bei θ = 0° durch null, Maximum bei θ = 90°“. Für die übrigen Komponenten gilt 3.5 (Offset), das der Tooltip nennt. Absolut: wie FG-04 3.2 (Ref1, M8).

## 5 Ergebnisformeln

| Größe | Formel | Einheit |
|---|---|---|
| Pivot (Voreinstellung) | $c_b=\arg\max_c\lvert\hat v_{bc}\rvert$ (kleinster Index bei Gleichstand) | – |
| Bezugsphase | $u_b=\hat v_{b,c_b}/\lvert\hat v_{b,c_b}\rvert$, $\psi_b=\arg u_b$ | 1, rad |
| gedrehte Amplitude | $\hat w_{pc}=\hat v_{pc}\,\overline{u_b}$ für alle $p$, $c$ | wie $\hat v$ |
| Auslenkung | $\hat d_{pc}=\hat w_{pc}/(i\omega)$ | m bzw. m/N |
| Bildposition | $\vec x_p(\theta)=\vec X_p+s\sum_c\vec e_c\,\mathrm{Re}\{\hat d_{pc}e^{i\theta}\}=\vec x_p^{\,v}(\theta-\psi_b)$ | m |
| Zeit des Maximums | $\theta_{\max,pc}=\pi/2-\arg\hat w_{pc}$ | rad |
| angezeigte Phase | $\Delta\varphi_{pc}=\arg(\hat v_{pc}\,\overline{u_b})\in(-\pi,\pi]$ | rad |
| Offset zur 2D-Phase | $\Delta\varphi_{pc'}-\Delta\varphi^{2D}_{pc'}=\arg\hat v_{bc'}-\psi_b$ (konstant in $p$; null für $c'=c_b$) | rad |
| Alternative B (nicht empfohlen) | $\psi_b=\tfrac12\arg\sum_i\hat v_{bi}^2$ + Vorzeichenregel | rad |

## 6 Referenzfälle (Tests)

Alle Sollwerte im Prüfskript (Anhang), Skala $10^{-3}$ m/s, $f=100$ Hz, $\omega=628{,}3185307$ rad/s, $a_0=10^{-3}/\omega=1{,}5915494309\cdot10^{-6}$ m. **Toleranzen:** Die Sollwerte sind geschlossene Ausdrücke; Fehlerquelle ist nur float64-Rundung (gemessen $<10^{-16}$ relativ). `rtol=1e-12` für Werte ungleich null, `atol=1e-12` rad für Winkel (Winkel bei $\pm\pi$ über $e^{i\varphi}$ vergleichen), `atol=1e-12·a₀` m für Positionen. Zeichen: Pivot-Komponente = Y (Index 1).

**Datensatz DS1** ($P=3$, in $10^{-3}$ m/s; $b=0$):
$\hat v_0=(0{,}5,\ 1{,}0e^{i\pi/3},\ 0{,}3e^{-0{,}4i})$,
$\hat v_1=(0{,}2e^{0{,}2i},\ 0{,}4e^{i(\pi/3+\pi/2)},\ 0{,}1e^{2{,}0i})$,
$\hat v_2=(0{,}3e^{1{,}0i},\ 0{,}6e^{i(\pi/3-\pi)},\ 0{,}2e^{-1{,}0i})$.

| ID | Eingang | Sollwert | Toleranz |
|---|---|---|---|
| **RF-N1** Rotation, Voreinstellung A | DS1, $b=0$ | $c_b=Y$ (Index 1), $\psi_b=\pi/3=1{,}0471975512$ rad. $\arg\hat w$ (Zeilen $p$, Spalten X, Y, Z): $p_0$: $-1{,}0471975512;\ 0;\ -1{,}4471975512$; $p_1$: $-0{,}8471975512;\ \pi/2;\ 0{,}9528024488$; $p_2$: $-0{,}0471975512;\ \pi;\ -2{,}0471975512$. $\hat w_{0Y}=10^{-3}$ (reell, positiv). Beträge $\lvert\hat w\rvert=\lvert\hat v\rvert$. Positionen: $d_{0Y}(\theta_n)/(\lvert\hat v_{0Y}\rvert/\omega)=0,\ 1,\ 0,\ -1$ für $\theta_n=0,\pi/2,\pi,3\pi/2$; $d_{1Y}(\theta_n)/(\lvert\hat v_{1Y}\rvert/\omega)=1,\ 0,\ -1,\ 0$. **Zeitverschiebung:** $d^w(\theta)=d^v(\theta-\pi/3)$ für 13 Stützstellen, alle $p$, $c$ (gemessen max. Abw. $4\cdot10^{-22}$ m) | s. o. |
| **RF-N1b** Bahn unverändert | DS1 | Halbachsen (Schnelle, m/s) und Drehsinn $\vec m=\mathrm{Im}\times\mathrm{Re}$ vor und nach der Rotation gleich. $p_0$: $1{,}0399657157\cdot10^{-3}$ / $5{,}084007377\cdot10^{-4}$, $\vec m=(2{,}9771142,\,-0{,}58412751,\,-4{,}3301270)\cdot10^{-7}$; $p_1$: $4{,}3641466585\cdot10^{-4}$ / $1{,}3979356006\cdot10^{-4}$; $p_2$: $6{,}771649794\cdot10^{-4}$ / $1{,}7733468559\cdot10^{-4}$ (Auslenkung: durch $\omega$) | rtol 1e-12 |
| **RF-N2** Kreisbahn $b$ | $\hat v_b=10^{-3}(1,i,0)$, zweiter Punkt $\hat v_p=10^{-3}(0{,}5,\ 0{,}5i\,e^{0{,}3i},\ 0{,}2)$ | A: Gleichstand, $c_b=$ X, $\psi=0$; $\hat w_b=10^{-3}(1,i,0)$; $\vec d_b(\theta_n)/a_0=(0,1,0),(1,0,0),(0,-1,0),(-1,0,0)$ (wie FG-04 RF-A6); Halbachsen beide $10^{-3}$, $\vec m=(0,0,-10^{-6})$. C(Y): $\psi=\pi/2$, $\hat w_b=10^{-3}(-i,1,0)$, $\vec d_b(\theta_n)/a_0=(-1,0,0),(0,1,0),(1,0,0),(0,-1,0)$ (gleiche Kreisbahn, um $T/4$ verschoben). C(Z): `ValueError`. B: NaN. **Negativtest D:** komponentenweise Drehung ergäbe $\hat w_b=10^{-3}(1,1,0)$, Halbachsen $(1{,}41421356,\,0)\cdot10^{-3}$; die Umsetzung muss die Halbachsen und die Phasendifferenz X→Y von $p$ ($\pi/2+0{,}3=1{,}8707963$ rad, nicht $0{,}3$) erhalten | rtol 1e-12; Negativtest: Differenz $>0{,}1$ rad |
| **RF-N3** lineares $b$ | $\hat v_b=10^{-3}e^{0{,}4i}(1,1,0)$ | A, C(X), C(Y): $\psi=0{,}4$; B: $0{,}4$ (Regel „erste Komponente positiv“ greift, da $\vec e_\mathrm{max}\perp\vec e_\mathrm{ref}$). C(Z): `ValueError`. Reduktion auf FG-04 | atol 1e-12 rad |
| **RF-N4** Polarität / Kovarianz | DS1, $\hat v\to-\hat v$ | $\psi_b\to\psi_b-\pi$ (mod $2\pi$) für A, B, C(Y); $\hat w$ **identisch** (max. Abw. $4\cdot10^{-19}$ m/s, relativ $<10^{-15}$); Bildfolge bildgleich. Zusätzlich $\hat v\to e^{i\alpha}\hat v$, $\alpha=0{,}7$: $\hat w$ identisch | atol 1e-12·$10^{-3}$ m/s |
| **RF-N5** Konsistenz mit 2D | DS1, Pivot Y | $\arg\hat w_{pY}=$ `phase_relativ_rad(v[:,1], 0)` für alle $p$ (Abw. $<10^{-16}$); für X konstanter Offset $-\pi/3=-1{,}0471975512$ rad, für Z $-1{,}4471975512$ rad (gleich für alle $p$). B-Äquivalenz: $\vec e_\mathrm{max}\cdot\hat v_b$ hat die Phase $\psi_B=0{,}9001846763$; $\mathrm{Re}\,\hat w_b\cdot\mathrm{Im}\,\hat w_b=7\cdot10^{-23}\approx0$ | atol 1e-12 rad |
| **RF-N6** Gleichstand, Sprungverhalten | $\hat v_b=10^{-3}(1,\ r\,e^{1{,}0i},\ 0{,}3e^{0{,}5i})$, $r=0{,}99;\ 1{,}01$ | A: $\psi=0$ (X) bei 0,99 und $1{,}0$ (Y) bei 1,01: Sprung $1{,}0$ rad (**dokumentiertes Verhalten**). C(X): $0$, C(Y): $1{,}0$ für beide $r$ (stetig). B: $0{,}49278$ / $0{,}50716$ (stetig; feiner Sweep $r=0{,}8\dots1{,}2$: größter Schritt $7{,}6\cdot10^{-5}$ rad, A: ein Schritt $1{,}0$). **Test:** bei exakt gleichen Beträgen wählt A den kleineren Index | atol 1e-12 rad |
| **RF-N7** Bezugspunkt 3D | DS1 | Voreinstellung $b=0$ (`auslenkung_max` $1{,}04\cdot10^{-3}$ > $6{,}77\cdot10^{-4}$ ($p_2$) > $4{,}36\cdot10^{-4}$ ($p_1$); nach $\lVert\hat v\rVert_2$ gleiche Reihenfolge: $1{,}1576\cdot10^{-3}$, $7{,}0\cdot10^{-4}$, $4{,}58\cdot10^{-4}$). $p_0$ in einer Komponente maskiert: $b=2$ ($p_0$ steht, A-1). Manuelle Wahl von $p_0$ in diesem Fall: abgelehnt (A-2). Alle $\hat v=0$ oder alle maskiert: kein Bezug, Meldung | exakt (Index) |
| **RF-N8** Rauschen (Charakterisierung, kein Test) | gekippte Ellipse, Achsenverhältnis $\rho=0{,}5;\ 0{,}9;\ 0{,}99$, komplexes Rauschen mit Standardabweichung 0,01 (große Halbachse 1), 4000 Ziehungen, Seed 1 | Standardabweichung $\psi_A$: 0,0076; 0,026; 0,0071 rad. $\psi_B$: 0,011; 0,050; **0,56** rad (größte Abweichung 1,59 rad). Begründet die Ablehnung von B als Voreinstellung | – |

## 7 Gültigkeit und Randfälle

**Voraussetzungen**
- Alle Punkte und Komponenten beziehen sich auf **dieselbe** Referenz (FG-04 6); sonst ist schon der Phasenvergleich zwischen Komponenten sinnlos (unabhängig von diesem Nachtrag).
- Linearität, Stationarität wie FG-04 6.
- Die Wahl von $\psi_b$ ändert nur den Zeitnullpunkt (3.1). Aussagen über Gleich- oder Gegenphasigkeit sind davon unabhängig.

**Randfälle**
- $\hat{\vec v}_b=0$: kein Bezug (ADR-025 `waehle_bezugspunkt` schließt $\lvert v\rvert=0$ aus).
- $\hat v_{b,c_b}=0$ bei vom Nutzer gewählter Komponente: `ValueError` mit Hinweis, eine andere Komponente oder „automatisch“ zu wählen. Die Voreinstellung A tritt nie in diesen Fall.
- Kleiner Betrag $\lvert\hat v_{b,c_b}\rvert$ bei Überschreibung: Es gibt **keinen** aus den Betrags­verhältnissen ableitbaren Grenzwert. Die Zuverlässigkeit der Phase hängt an $\gamma^2$ der Komponente (FG-02 3.4), und das ist für alle drei Komponenten von $b$ durch A-1 mit $\ge\gamma^2_\mathrm{min}$ sichergestellt. Ein Fehler in $\psi_b$ verschiebt nur den Zeitnullpunkt (3.1); ein Hinweistext ist optional (Gestaltung, **keine** fachliche Schwelle).
- Maskierte Komponenten des Bezugspunkts: ausgeschlossen durch A-2. Maskierte Komponenten **anderer** Punkte: Punkt steht (A-1), geht nicht in $D_\mathrm{ref}$ ein; $\psi_b$ wird davon nicht berührt.
- Gleichstand der Beträge: deterministisch, kleinster Index; bei Rundungsrauschen kann der Gleichstand kippen (Zeitnullpunkt springt, Form nicht).
- Kreisbahn von $b$: A und C wohldefiniert, B nicht (3.4).
- **M8:** wirkt nicht (K1, RF-N4). **M12** (Komponenten im Geometrie-KS): ändert die Bewegungsrichtung, nicht die Bezugsphase; Kennzeichen wie FG-04 3.4. **M13:** nur Alternative B hängt davon ab.
- Einzelkomponente: $c_b$ = die dargestellte Komponente; Ergebnis identisch zu FG-04 3.2 und `relativ_gedreht` des Plans.

## 8 Quellen

Alle Herleitungen und Zahlen sind eigene Rechnung [A, N]. Verwendet: FG-04 (3.2, 3.3, 3.4, 3.6, RF-A6, RF-A10), FG-02 (2.4, 3.4), FG-03 (5.3), ADR-025, Plan P-AUSW3 (Abschnitt 14, F-A2). Keine Lehrbuchaussage wird als belegt behauptet. Die Phasenfixierung der Bahnellipse über $\tfrac12\arg\sum v^2$ folgt FG-03 5.3 und ist dort ebenfalls eigene Herleitung.

## 9 Offene Punkte

**Rückfragen (alle nicht blockierend)**
- **F-N1:** Empfehlung C-Mechanismus mit A als Voreinstellung (Abschnitt 4) so freigeben? *Annahme bis zur Klärung:* ja.
- **F-N2:** Soll die Bezugskomponente in der Oberfläche **wählbar** sein (Auswahl „automatisch | X | Y | Z“) oder nur **angezeigt** werden? Fachlich reicht Anzeige; die Funktion nimmt die Komponente als Parameter. *Annahme:* nur Anzeige im Kopf („Bezug: Punkt n, Komponente Z“), Auswahl später, falls gewünscht.
- **F-N3:** A-2 (Bezugspunkt muss animierter Punkt sein) und A-3 (Voreinstellung nach größter `auslenkung_max`). *Annahme:* ja.

**Annahmen:** A-2, A-3 (Abschnitt 4); Kennzeichen M8 (nur bei absolutem Bezug) und M12 bleiben wie in FG-04.

**Unsicherheiten:** Wie PSV in seiner 3D-Animation den Phasenbezug wählt, ist nicht bekannt (Rechercheauftrag RA-1 aus FG-04 deckt das mit ab). Die Rausch-Zahlen (RF-N8) gelten für das gewählte Modell (unabhängiges, gleichverteiltes komplexes Rauschen je Komponente), nicht für reale Kohärenzfehler. Die Aussagen sind nur durch Herleitung und Rechnung belegt, nicht durch Literatur.

**Rechercheaufträge:** keine zusätzlichen.

## Anhang: Prüfskript

Ausgeführt im Scratchpad (`fg04n1/fg04n1.py`, Python 3 mit NumPy). Die Selbstprüfung am Ende lief fehlerfrei („alle Pruefungen bestanden“); die gedruckten Werte sind in Abschnitt 6 übernommen.

```python
"""FG-04 Nachtrag 1 Pruefskript: skalarer Phasenbezug fuer einen 3D-Bezugspunkt."""
import numpy as np

np.set_printoptions(precision=10, suppress=False, linewidth=140)
F = 100.0
OM = 2 * np.pi * F
A0 = 1e-3 / OM  # 1 mm/s -> m


def psi_a(vb):
    """Alternative A: Phase der betragsgroessten Komponente (Gleichstand: kleinster Index)."""
    c = int(np.argmax(np.abs(vb)))
    return float(np.angle(vb[c])), c


def psi_c(vb, c):
    """Alternative C: Phase der gewaehlten Komponente c."""
    if abs(vb[c]) == 0:
        raise ValueError("Bezugskomponente hat Betrag 0")
    return float(np.angle(vb[c]))


def psi_b(vb, e_ref=(0.0, 0.0, 1.0)):
    """Alternative B: Hauptachse der Bahnellipse, psi = 1/2 arg(sum v^2), Vorzeichenregel FG-03 5.3."""
    s = np.sum(vb**2)
    if abs(s) < 1e-12 * np.sum(np.abs(vb) ** 2):
        return float("nan")
    psi = 0.5 * np.angle(s)
    e = np.real(vb * np.exp(-1j * psi))
    e = e / np.linalg.norm(e)
    d = float(np.dot(e, e_ref))
    if abs(d) < 1e-12:
        k = int(np.argmax(np.abs(e) > 1e-12))
        neg = e[k] < 0
    else:
        neg = d < 0
    if neg:
        psi += np.pi
    return float(np.angle(np.exp(1j * psi)))


def rot(v, psi):
    return v * np.exp(-1j * psi)


def disp(w, theta):
    """d(theta) = Re{ w/(i om) e^{i theta} }, w (...,3)."""
    return np.real(w / (1j * OM) * np.exp(1j * theta))


def semi(w):
    """Halbachsen (max,min) der Bahn Re{w e^{i th}}: Singulaerwerte von [Re; Im]."""
    m = np.vstack([w.real, w.imag])
    s = np.linalg.svd(m, compute_uv=False)
    return s[0], s[1]


def sig(w):
    m = np.cross(w.imag, w.real)
    return m


print("=== RF-N1: Datensatz DS1 (P=3), Skala 1e-3 m/s ===")
v = 1e-3 * np.array([
    [0.5, 1.0 * np.exp(1j * np.pi / 3), 0.3 * np.exp(-0.4j)],
    [0.2 * np.exp(0.2j), 0.4 * np.exp(1j * (np.pi / 3 + np.pi / 2)), 0.1 * np.exp(2.0j)],
    [0.3 * np.exp(1.0j), 0.6 * np.exp(1j * (np.pi / 3 - np.pi)), 0.2 * np.exp(-1.0j)],
])
b = 0
pa, ca = psi_a(v[b])
print("psi_A, c*", pa, ca, "(pi/3 =", np.pi / 3, ")")
print("psi_B", psi_b(v[b]))
for c in range(3):
    print("psi_C", c, psi_c(v[b], c))
for name, psi in [("A", pa), ("C_x", psi_c(v[b], 0)), ("C_z", psi_c(v[b], 2)), ("B", psi_b(v[b]))]:
    w = rot(v, psi)
    print(name, "arg w (P x 3) in rad:")
    print(np.angle(w))
    print("  w_b =", w[b])
# Konsistenz mit 2D-Phase der Einzelkomponente
w = rot(v, pa)
for c in range(3):
    ph2d = np.angle(v[:, c] * np.conj(v[b, c]))
    ph3d = np.angle(w[:, c])
    off = np.angle(np.exp(1j * (ph3d - ph2d)))
    print("comp", c, "3D-minus-2D Phase (rad):", off, " erwartet const =", np.angle(v[b, c] * np.conj(v[b, ca])) * -1 + 0)
# Invarianz der Halbachsen/Drehsinn und Verschiebung d_w(th)=d_v(th-psi)
for p in range(3):
    print("p", p, "semi v", semi(v[p]), "semi w", semi(rot(v[p], pa)), "m_v", sig(v[p]), "m_w", sig(rot(v[p], pa)))
th = np.linspace(0, 2 * np.pi, 13)
dw = np.array([disp(rot(v, pa), t) for t in th])
dv = np.array([disp(v, t - pa) for t in th])
print("max |d_w(th)-d_v(th-psi)| =", np.max(np.abs(dw - dv)), " Skala", A0)
# Zeitnullpunkt: b, Komp c*: d = |v|/om sin(th); Maximum bei pi/2
thn = np.array([0, np.pi / 2, np.pi, 3 * np.pi / 2])
print("d_b,c*(theta_n)/(|v_b,c*|/om):", disp(w[b], thn[:, None])[:, ca] / (abs(v[b, ca]) / OM))
print("d_p1,c*(theta_n)/a0 and expected sin(th+arg w):", disp(w[1], thn[:, None])[:, ca] / (abs(v[1, ca]) / OM),
      np.sin(thn + np.angle(w[1, ca])))

print("\n=== RF-N2: Kreisbahn b = 1e-3 (1, i, 0), zweiter Punkt p = 1e-3 (0.5, 0.5i*e^{i0.3}.. ) ===")
vb = 1e-3 * np.array([1, 1j, 0])
vp = 1e-3 * np.array([0.5, 0.5j * np.exp(0.3j), 0.2])
V = np.array([vb, vp])
print("psi_A", psi_a(vb), " psi_B", psi_b(vb), " psi_C(x)", psi_c(vb, 0), " psi_C(y)", psi_c(vb, 1))
try:
    psi_c(vb, 2)
except ValueError as e:
    print("psi_C(z) -> ValueError:", e)
for name, w in [("A", rot(V, 0.0)), ("C_y", rot(V, np.pi / 2))]:
    print(name, "w_b =", w[0], " semi_b =", semi(w[0]), " Drehsinn m_b =", sig(w[0]))
    print("    d_b(theta_n)/a0 =\n", disp(w[0], thn[:, None]) / A0)
# Alternative D (VERBOTEN): jede Komponente mit ihrer eigenen Bezugsphase (z=0: Faktor undefiniert, hier 1)
wd = V * np.conj(vb) / np.where(np.abs(vb) > 0, np.abs(vb), 1)
print("D (komponentenweise, korrekt) w_b =", wd[0], " semi", semi(wd[0]), " m", sig(wd[0]))
print("D w_p =", wd[1], " rel. Phase x->y von p (A):", np.angle(V[1,1]*np.conj(V[1,0])), " (D):", np.angle(wd[1,1]*np.conj(wd[1,0])))

print("\n=== RF-N3: lineares b = 1e-3 e^{0.4i} (1,1,0) ===")
vb = 1e-3 * np.exp(0.4j) * np.array([1, 1, 0])
print("psi_A", psi_a(vb), "psi_B", psi_b(vb), "psi_C(x)", psi_c(vb, 0), "psi_C(y)", psi_c(vb, 1))

print("\n=== RF-N4: M8: v -> -v ===")
for name, f in [("A", lambda x: psi_a(x)[0]), ("B", psi_b), ("C_y", lambda x: psi_c(x, 1))]:
    p1, p2 = f(v[b]), f(-v[b])
    w1, w2 = rot(v, p1), rot(-v, p2)
    print(name, "psi:", p1, p2, " diff mod 2pi:", np.angle(np.exp(1j * (p2 - p1))), " max|w1-w2| =", np.max(np.abs(w1 - w2)))

print("\n=== RF-N5: B: Ausrichtung ===")
wB = rot(v[b], psi_b(v[b]))
print("B: Re w_b . Im w_b =", np.dot(wB.real, wB.imag), " |Re|,|Im| =", np.linalg.norm(wB.real), np.linalg.norm(wB.imag), semi(v[b]))
print("B: e_max.z =", wB.real[2] / np.linalg.norm(wB.real))
print("B: Proj. e_max.v_b Phase =", np.angle(np.dot(wB.real / np.linalg.norm(wB.real), v[b])), "psi_B", psi_b(v[b]))

print("\n=== RF-N6: Stetigkeit (Sweep) ===")
rr = [0.99, 1.0, 1.01]
for r in rr:
    vb = 1e-3 * np.array([1.0, r * np.exp(1.0j), 0.3 * np.exp(0.5j)])
    print("r", r, "psi_A", psi_a(vb), "psi_B", psi_b(vb), "psi_C(x)", psi_c(vb, 0), "psi_C(y)", psi_c(vb, 1))
for r in [0.9, 0.99, 1.0, 1.01, 1.1]:
    vb = 1e-3 * np.array([1.0, 1j * r, 0.0])
    print("circ r", r, "psi_B", psi_b(vb), "psi_A", psi_a(vb)[0])
# feiner Sweep: Sprunggroesse
rs = np.linspace(0.8, 1.2, 4001)
def sweep(f):
    ps = np.array([f(1e-3 * np.array([1.0, r * np.exp(1.0j), 0.3 * np.exp(0.5j)])) for r in rs])
    d = np.abs(np.angle(np.exp(1j * np.diff(ps))))
    return d.max(), int((d > 0.1).sum())
print("sweep r 0.8..1.2: max step, #steps>0.1 rad: A", sweep(lambda x: psi_a(x)[0]), "B", sweep(psi_b),
      "C_x", sweep(lambda x: psi_c(x, 0)), "C_y", sweep(lambda x: psi_c(x, 1)))
# ABC bei Sweep in Phase der Y-Komponente (Frequenzgang durch Resonanz): phi_y 0..pi
phis = np.linspace(0, 2 * np.pi, 4001)
def sweep2(f):
    ps = np.array([f(1e-3 * np.array([1.0, 0.5 * np.exp(1j * p), 0.3 * np.exp(0.5j)])) for p in phis])
    d = np.abs(np.angle(np.exp(1j * np.diff(ps))))
    return d.max()
print("sweep phi_y (|y|=0.5): max step A", sweep2(lambda x: psi_a(x)[0]), "B", sweep2(psi_b), "C_x", sweep2(lambda x: psi_c(x, 0)))

print("\n=== RF-N7: Rauschempfindlichkeit von psi (Monte Carlo, Seed 1) ===")
rng = np.random.default_rng(1)
for rho in [0.5, 0.9, 0.99]:
    # Ellipse in x-z gekippt: major (cos20, 0, sin20)*1, minor (0,1,0)*rho
    maj = np.array([np.cos(0.35), 0.0, np.sin(0.35)])
    mnr = np.array([0.0, 1.0, 0.0])
    ph0 = 0.8
    vb0 = (maj + 1j * rho * mnr) * np.exp(1j * ph0)
    pa0, _ = psi_a(vb0)
    sA, sB = [], []
    for _ in range(4000):
        n = 0.01 * (rng.standard_normal(3) + 1j * rng.standard_normal(3)) / np.sqrt(2)
        vv = vb0 + n
        sA.append(np.angle(np.exp(1j * (psi_a(vv)[0] - pa0))))
        pb = psi_b(vv)
        sB.append(pb)
    sB = np.array(sB)
    pb0 = psi_b(vb0)
    dB = np.angle(np.exp(1j * (sB - pb0)))
    print("rho", rho, "std psi_A", np.std(sA), " std psi_B", np.std(dB), " max|dB|", np.max(np.abs(dB)), " psi_A0, psi_B0", pa0, pb0)

print("\n=== Selbstpruefung der Sollwerte ===")
v = 1e-3 * np.array([
    [0.5, 1.0 * np.exp(1j * np.pi / 3), 0.3 * np.exp(-0.4j)],
    [0.2 * np.exp(0.2j), 0.4 * np.exp(1j * (np.pi / 3 + np.pi / 2)), 0.1 * np.exp(2.0j)],
    [0.3 * np.exp(1.0j), 0.6 * np.exp(1j * (np.pi / 3 - np.pi)), 0.2 * np.exp(-1.0j)],
])
u = v[0, 1] / abs(v[0, 1])
w = v * np.conj(u)  # am Pivot reell bis auf Rundung (|Im| < 1e-12*|v|)
assert abs(w[0, 1].imag) < 1e-12 * abs(v[0, 1]) and np.isclose(w[0, 1].real, abs(v[0, 1]), rtol=1e-12)
assert np.allclose(np.exp(1j*np.angle(w)), np.exp(1j*np.array([[-1.0471975512, 0, -1.4471975512],[-0.8471975512, np.pi/2, 0.9528024488],[-0.0471975512, np.pi, -2.0471975512]])), atol=1e-9)
assert np.isclose(psi_b(v[0]), 0.900184676349882, rtol=1e-12)
assert np.isnan(psi_b(1e-3*np.array([1, 1j, 0])))
assert psi_a(1e-3*np.array([1, 1j, 0]))[1] == 0
print("alle Pruefungen bestanden")
```
