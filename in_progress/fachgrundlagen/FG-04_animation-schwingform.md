<!-- Fachgrundlage FG-04: Animation der Betriebsschwingform (R-071). Erstellt im Paket FG-04 von strukturdynamik-experte, Stand 2026-11-09. Entwurf, Freigabe durch den Nutzer ausstehend. -->

**Freigabe:** vom Nutzer am 2026-11-09 freigegeben, mit den Empfehlungen E1–E5 und Annahme A-1 (3D-Punkt bewegt sich nur bei drei gültigen Komponenten).

# FG-04 – Animation der Betriebsschwingform (R-071)

> **Status:** Entwurf vom 2026-11-09, **Freigabe durch den Nutzer ausstehend.** Baut auf FG-02 (Abschnitte 2, 3.4, 3.6, 3.7), FG-03 (Abschnitt 5.3) und ADR-025 auf. Widerspricht keiner freigegebenen Festlegung, **präzisiert** aber FG-02 3.6 an einer Stelle (Abschnitt 3.1: dort ist der „Momentanwert für die Animation“ die Schnelle, nicht die Auslenkung). Die Koordinatentransformation (R-070) ist nicht Teil.

## 1 Zweck und Umfang

R-071 (Muss): „Bei gewählter Frequenz zeigt die Software eine animierte Schwingform auf der Messgeometrie; die Phase der Bewegung entspricht der dargestellten Phase.“

Diese Fachgrundlage legt fest, **was** die Animation fachlich zeigt, damit der Satz „Phase der Bewegung = dargestellte Phase“ prüfbar wird:

| Punkt | Inhalt | Abschnitt |
|---|---|---|
| Z-1 | Zeitverlauf der Auslenkung je Punkt und Komponente aus der komplexen Amplitude, Zeitnullpunkt | 3.1, 3.2 |
| Z-2 | Wahl der Größe (Schnelle oder Weg), Umrechnung $\hat v \to \hat d$ | 3.1 |
| Z-3 | Prüfbare Fassung von „Phase der Bewegung = dargestellte Phase“ | 3.3 |
| Z-4 | Skalierung der Darstellung (Überhöhung) und ihre Kennzeichnung | 3.5 |
| Z-5 | 3D-Vektor gegen Einzelkomponente, Projektion | 3.4 |
| Z-6 | Ungültige Punkte, γ² < γ²_min, NaN | 3.6 |
| Z-7 | Bilder je Periode | 3.7 |
| Z-8 | Referenzfälle RF-A1 bis RF-A14 mit Sollwerten | 5 |

**Nicht enthalten:** Koordinatentransformation und Normalenzerlegung (R-070, FG-03 Abschnitt 5), Auswahl der Gestaltungsmittel (Farbe, Linienstärke, 3D-Ansicht: Sache des `ui-designer`), Export als Film (nur, soweit er Bilder je Periode betrifft), Animation von Zeitdaten (nur Frequenzbereich).

**Kennzeichnung der Belege** wie in FG-02: **[H]** Herstellerangabe, **[D]** an der Datei geprüft, **[A]** eigene Herleitung im Text, **[N]** numerisch im Prüfskript (Anhang), **[ANN]** Annahme, **[L-m]** Literatur nur mit Metadaten.

---

## 2 Konventionen

Es gelten alle Konventionen von FG-02 Abschnitt 2 und KONVENTIONEN.md. Hier ausdrücklich wiederholt, soweit die Animation davon abhängt:

| Größe | Festlegung |
|---|---|
| Zeitabhängigkeit | $e^{+i\omega t}$; ein reales Signal mit komplexer Amplitude $\hat x$ ist $x(t) = \mathrm{Re}\{\hat x\,e^{i\omega t}\} = \lvert\hat x\rvert\cos(\omega t + \arg\hat x)$ (FG-02 2.1) |
| Spektrum | einseitig, Spitzenwert (0-to-peak); $\lvert\hat x\rvert$ ist die Amplitude, nicht der Effektivwert |
| Phase | $\varphi = \arg\hat v$ in rad; **positiv = eilt voraus** (FG-02 2.1, KONVENTIONEN). In der Oberfläche in Grad, mit Subjekt („positiv = Vib Z eilt Ref1 voraus“) |
| Phasenbezug | absolut gegen Ref1 (CPH bzw. H1; vorläufig, Polarität M8 offen) oder relativ zu einem Bezugspunkt $b$: $\Delta\varphi_p = \arg(\hat v_p\,\hat v_b^{*})$ (ADR-025, `phase_relativ_rad`) |
| Kreisfrequenz | $\omega = 2\pi f_{k^\ast}$ in rad/s mit der **Frequenz der gewählten Linie** $f_{k^\ast}$, **nicht** mit $f_\mathrm{wahl}$ (FG-02 3.6, RF-A9) |
| Animationswinkel | $\theta = \omega t$ in rad (Phase der Uhr), $t = \theta/\omega$ in s, Periode $T = 1/f_{k^\ast}$ |
| Richtung | Positive Auslenkung einer Komponente X/Y/Z ist Bewegung entlang der jeweiligen Achse des Koordinatensystems des 3D-Abgleichs (KONVENTIONEN, vorläufig, am Gerät zu bestätigen) |
| Einheiten | $\hat v$ in m/s (CPH) bzw. (m/s)/N (H1); $\hat d$ in m bzw. m/N; Koordinaten $X_p$ in m; Überhöhung $s$ dimensionslos |
| Indizes | Punkt $p = 0\dots P-1$, Komponente $c \in \{X, Y, Z\}$, Linie $k^\ast$ (0-basiert) |

---

## 3 Herleitung und Festlegungen

### 3.1 Größe: Auslenkung statt Schnelle (Entscheidung E1)

Das Vibrometer liefert die **Schnelle**. FG-02 3.6 nennt als „Momentanwert für die Animation“ $u(\theta) = \mathrm{Re}\{\hat v\,e^{i\theta}\}$; das ist die **Schnelle** zum Zeitpunkt $\theta/\omega$, nicht die Auslenkung. Der Code übernimmt das (`auswertung/schwingform.py`, `momentanwert`; Docstring: $u(\theta) = \mathrm{Re}\{\hat v\,e^{i\theta}\}$).

**Herleitung** [A]: Für $v(t) = \mathrm{Re}\{\hat v\,e^{i\omega t}\}$ ist die Auslenkung $d(t) = \int v\,\mathrm{d}t$ (stationär, ohne Gleichanteil)
$$\hat d = \frac{\hat v}{i\omega} = -\,i\,\frac{\hat v}{\omega}\ [\mathrm m],\qquad
d(\theta) = \mathrm{Re}\{\hat d\,e^{i\theta}\} = \frac{\lvert\hat v\rvert}{\omega}\,\sin(\theta + \varphi),\quad \varphi = \arg\hat v .$$
Dies ist FG-02 3.7 (Weg eilt der Schnelle um $\pi/2$ nach). Für die Schnelle gilt dagegen $u(\theta) = \lvert\hat v\rvert\cos(\theta+\varphi)$. Es folgt der Zusammenhang
$$u(\theta) = \omega\,d\!\left(\theta + \tfrac{\pi}{2}\right)\qquad\text{(RF-A13)}.$$

**Folgen:**
- Alle Punkte erhalten **denselben** Versatz $-\pi/2$; Phasendifferenzen zwischen Punkten, die Form und der Bewegungsablauf sind für Schnelle und Auslenkung gleich. Nur der Zeitnullpunkt der Animation verschiebt sich um $T/4$.
- Die **Phase in den Phasenbildern** (ADR-025: Pfeilwinkel, Kreislegende) ist $\arg\hat v$ der **Schnelle**, weil die Messgröße die Schnelle ist. Das ist die Phase im Sinne von R-071. Für die Auslenkung gilt $\arg\hat d = \varphi - \pi/2$. Das darf die Oberfläche nicht vermischen: Die Beschriftung der Phasenbilder bleibt „Phase der Schnelle“; die Animation trägt die Beschriftung der animierten Größe.
- Eine Animation der Auslenkung ist die anschauliche Größe („Schwingform“ = Auslenkungsfigur). **Empfehlung E1: Voreinstellung Auslenkung**, Schnelle als Option. Wird die Schnelle animiert, entfällt die Division durch $\omega$ (und damit die physikalische Auslenkungsamplitude, Abschnitt 3.5).
- **Quelle H1:** $\hat v := H_1$ in (m/s)/N; $\hat d$ ist dann die Rezeptanz in m/N (Auslenkung je 1 N Kraft). Beschriftung „je N“, kein Weg in m (RF-A1).
- Bei $\omega = 0$ (nur ohne Annahme $k_0 = 1$) ist $\hat d$ undefiniert: NaN, Punkt wie ungültig behandeln (3.6). In der Beispieldatei gilt $f_{k^\ast} \ge \Delta f = 0{,}625$ Hz > 0 (FG-02 2.3, bestätigt).

**Ehrlich unsicher:** Welche Größe PSV in seiner Animation zeigt (Weg, Schnelle) und wie PSV skaliert, ist in den Analyseberichten nicht festgehalten (I2: „phasenbezogen, nur mit Trigger oder Referenz“, SWP S. 139–142). Für den Vergleich mit PSV muss nachgesehen werden (Rechercheauftrag RA-1).

### 3.2 Zeitverlauf je Punkt und Komponente, Zeitnullpunkt

Mit $\hat d_{pc} = \hat v_{pc}/(i\omega)$ aus `Schwingform.amplitude` (P, 3) [A]:
$$\boxed{\;\vec x_p(\theta) = \vec X_p + s\sum_{c\in\{X,Y,Z\}} \vec e_c\ \mathrm{Re}\{\hat d_{pc}\,e^{i\theta}\}\;}\qquad[\mathrm m]$$
mit der Ruhelage $\vec X_p$ (Koordinaten der Messgeometrie in m), den Einheitsvektoren $\vec e_c$ der Achsen und der Überhöhung $s$ (3.5). Für eine Einzelkomponente entfällt die Summe über die beiden anderen. Mit $\mathrm{Re}\{\hat d e^{i\theta}\} = \mathrm{Re}\,\hat d\cos\theta - \mathrm{Im}\,\hat d\sin\theta$ ist die reelle Form **identisch** zur komplexen (RF-A5, [N]).

**Zeitnullpunkt $\theta = 0$ (absoluter Bezug).** CPH und H1 sind auf Ref1 bezogen: $\arg\mathrm{CPH} = \varphi_V - \varphi_R$ (FG-02 2.2). Wählt man $t=0$ so, dass $\varphi_R = 0$, ist $\mathrm{Ref1}(t) \propto \cos\omega t$. Also ist $\theta = 0$ der Zeitpunkt, an dem **das Referenzsignal Ref1 ihr positives Maximum** hat; die Auslenkung eines Punkts mit $\varphi = 0$ ist dann null und steigt (RF-A1). Das ist das einzige, was „Phase = absolut gegen Ref1“ bedeutet. Wegen der unbestätigten Polarität (M8) steht an der Uhr „Referenzbezug unbestätigt (M8)“.

**Zeitnullpunkt bei relativem Bezug.** Wähle einen Bezugspunkt $b$ (Voreinstellung wie ADR-025 `standard_bezug`: größtes $\lvert v\rvert$ unter $\gamma^2 \ge \gamma^2_\mathrm{min}$, gültig, $\lvert v\rvert > 0$). Ersetze
$$\hat w_p = \hat v_p\,\frac{\hat v_b^{*}}{\lvert\hat v_b\rvert}\quad\Longrightarrow\quad \arg\hat w_p = \Delta\varphi_p,\ \ \hat w_b = \lvert\hat v_b\rvert\in\mathbb R_{>0},\qquad \hat d_p = \frac{\hat w_p}{i\omega}.$$
Das ist die Drehung aller Amplituden um $-\arg\hat v_b$, also eine reine Verschiebung des Zeitnullpunkts um $\arg\hat v_b/\omega$. Die Form und alle Phasendifferenzen bleiben unverändert. Der Bezugspunkt hat dann $\theta = 0$ als Nulldurchgang (aufsteigend) und sein Maximum bei $\theta = \pi/2$.

**Unabhängigkeit von M8** [A]: Ein gedrehter Kanal ändert $\hat v \to s\hat v$ ($s = \pm1$, FG-02 2.4). Absolut: $x_p(\theta) \to x_p(\theta + \pi)$ für $s=-1$ (RF-A10); die **Folge der Bilder ist dieselbe Schleife**, nur um eine halbe Periode verschoben, das Startbild ist ein anderes. Relativ: $\hat w_p = (s\hat v_p)(s\hat v_b)^*/\lvert\hat v_b\rvert$ ist unverändert; die Animation ist **bildgleich**. Die Thesis-Abbildung (und jede Aussage über „gleich- oder gegenphasig“) nutzt den relativen Bezug, solange M8 offen ist (ADR-025).

### 3.3 Prüfbare Fassung von „Phase der Bewegung = dargestellte Phase“

Die dargestellte Phase ist $\varphi_p = \arg\hat v_p$ (absolut) bzw. $\Delta\varphi_p$ (relativ). Die Animation erfüllt R-071 genau dann, wenn für jede Komponente gilt [A]:

1. **Zeit des positiven Maximums.** Die Auslenkung von Punkt $p$ erreicht ihr Maximum in positiver Achsrichtung bei
$$\theta_{\max,p} = \tfrac{\pi}{2} - \varphi_p \pmod{2\pi}\qquad(\text{Schnelle: }\theta_{\max,p}=-\varphi_p).$$
2. **Vorlauf.** Hat Punkt $q$ gegenüber $p$ die Phase $\Delta\varphi = \varphi_q - \varphi_p \in (-\pi,\pi]$, erreicht $q$ sein Maximum um $\Delta\varphi/\omega$ **früher** (positives $\Delta\varphi$ = eilt voraus = früher), also $\Delta t = -\Delta\varphi/(2\pi f_{k^\ast})$. Für $\Delta\varphi = +\pi/2$ gilt $\Delta t = -T/4$ (RF-A4); bei $\Delta\varphi = \pi$ liegt eine Gegenphase vor, $x_q(\theta) = -x_p(\theta)$ (RF-A3).
3. **Gleiche Frequenz.** Alle Punkte laufen mit **derselben** $\theta$; es gibt keine punktweise Zeitskalierung.
4. **Amplitudenverhältnisse** der Auslenkungen sind $\lvert\hat v_p\rvert/\lvert\hat v_q\rvert$ (gleiche Linie, gleiche Überhöhung $s$ für alle Punkte und Komponenten).

Das Kriterium ist unabhängig von der Wahl Schnelle/Weg (nur $\theta_{\max}$ verschiebt sich um $\pi/2$ für alle gleich).

### 3.4 3D-Vektor gegen Einzelkomponente, Projektion

- **3D-Vektor.** Die drei Komponenten eines Punkts bewegen sich mit **derselben** $\theta$, jede mit ihrer eigenen Phase. Das Ergebnis ist im Allgemeinen eine **Ellipse** (Bahnellipse, FG-03 5.3, Halbachsen `auslenkung_max`/`auslenkung_min`). Gleichphasige Komponenten ergeben eine lineare Bahn. Die Bildreihe darf die Komponenten **nicht** einzeln normieren oder in der Phase angleichen. Der Drehsinn folgt aus FG-03 5.3, $m = \mathrm{Im}\,\hat v \times \mathrm{Re}\,\hat v$ (RF-A6).
- **Einzelkomponente.** Bewegung nur entlang $\vec e_c$ (Auslenkungspfeil), die anderen Komponenten sind null. Das entspricht der Phase-Darstellung nach ADR-025 (Phase nur für eine Einzelkomponente).
- **Voraussetzung** für die 3D-Bewegung: Die Phasen der drei Komponenten sind auf **dieselbe** Referenz bezogen und die Komponenten liegen im Koordinatensystem der Geometrie (**[ANN M12], offen**, FG-03 11). Ist M12 falsch, ist die Bewegungsrichtung falsch, nicht nur ihr Betrag. Die Animation trägt bis dahin das Kennzeichen „Komponenten im Geometrie-KS unbestätigt (M12)“.
- **Projektion.** Die Anzeige ist eine lineare (orthogonale oder perspektivische) Abbildung von $\vec x_p(\theta)$ auf die Bildebene. Eine lineare Abbildung ändert keine Phasen. **Die Komponente entlang der Blickrichtung ist im Bild nicht sichtbar** (z. B. $Z$ in der Aufsicht der Ansicht 4: Es gibt kein Bild einer Bewegung). Darum gilt: Eine Animation einer Komponente senkrecht zur Bildebene zeigt die momentane Auslenkung zusätzlich über eine **vorzeichenbehaftete** Kodierung (ob Farbe, Höhe in einer 3D-Ansicht oder anderes: Entscheidung des `ui-designer`, aber nicht nur Betrag), sonst bewegt sich im Bild nichts, und das ist eine **falsche Aussage**. Die Wahl der Kodierung darf die Phase nicht verändern.
- **Ruhelage.** $\vec X_p$ aus den Koordinaten der Messgeometrie; gemessene Positionen, keine Modellgeometrie. Es gibt keine Interpolation von Werten zwischen Punkten (Verbindungslinien nur zur Orientierung und nur zwischen zwei Punkten, die beide animiert werden, 3.6).

### 3.5 Skalierung der Darstellung (Überhöhung) und Kennzeichnung (Entscheidung E2)

**Größenordnung** [N]: $\lvert\hat v\rvert = 1$ mm/s bei 100 Hz ergibt $\lvert\hat d\rvert = 1{,}59$ µm. Bei Punktabständen von Zentimetern ist die reale Auslenkung unsichtbar klein. Eine Animation ist nur mit **Überhöhung** lesbar, und die Überhöhung ist **keine** physikalische Verformung.

**Festlegung** [A]:
- Die Überhöhung $s$ ist **ein einziger Faktor für alle Punkte, Komponenten und Bilder** einer Animation (dimensionslos). Nur so bleiben Amplitudenverhältnisse, Richtungen und Bahnellipsen richtig (3.3 Punkt 4). Kein Normieren je Punkt, je Komponente oder je Bild.
- **Bezugsgröße** $D_\mathrm{ref}$ = größte Spitzenauslenkung unter den **animierten** Punkten (3.6): Einzelkomponente $\max_p\lvert\hat d_{pc}\rvert = \max_p\lvert\hat v_{pc}\rvert/\omega$; 3D: $\max_p\,\texttt{auslenkung\_max}_p/\omega$ in m (bzw. m/N). Maskierte und ungültige Punkte gehen **nicht** ein (RF-A8).
- **Voreinstellung (Vorschlag, einstellbar):** $s = \alpha\,d_\mathrm{NN}/D_\mathrm{ref}$ mit dem Median $d_\mathrm{NN}$ der Abstände zum nächsten Nachbarn (wie ADR-025) und $\alpha = 0{,}25$. Die größte angezeigte Auslenkung beträgt dann $\alpha\,d_\mathrm{NN}$ (RF-A7).
- **Obergrenze** (nur Hinweis, keine Sperre): Bewegen sich zwei Nachbarn in der Bildebene gegeneinander, kommen sie bei $s\,D_\mathrm{ref} \ge d_\mathrm{NN,min}/2$ zusammen, wobei $d_\mathrm{NN,min}$ der kleinste Nachbarabstand ist. Oberhalb: Hinweis „Punkte können sich überlagern“. $\alpha = 0{,}25$ ist ein Gestaltungsvorschlag, keine fachliche Größe; fachlich ist nur die Grenze 0,5 herleitbar [A].
- **Kennzeichnung (Pflicht):** Jede Anzeige und jedes exportierte Bild/jeder Film nennt (a) „Auslenkung um den Faktor $s$ überhöht“ mit Zahl, (b) die größte reale Spitzenauslenkung $D_\mathrm{ref}$ mit Einheit (m, µm; bei H1 „m/N“), (c) die Frequenz $f_{k^\ast}$ der Linie und die Größe (Weg/Schnelle, Quelle CPH/H1), (d) die Referenz und den Phasenbezug. Ohne diese Angaben wäre die Abbildung eine falsche Aussage über die Verformung.
- **Wechsel der Frequenz/Linie** ändert $D_\mathrm{ref}$ und damit $s$ bei Voreinstellung. Beim Vergleich zweier Linien ist ein fester Wert $s$ (Nutzereingabe) sinnvoll; der Wechsel einer automatischen Überhöhung wird in der Anzeige sichtbar gemacht.
- **Linearität.** $\vec x_p(\theta)$ ist die lineare Überlagerung kleiner Auslenkungen. Bei großem $s$ ist die Bildfolge eine Veranschaulichung, keine Starrkörper- oder Geometrietreue (bewegt werden nur die Messpunkte; zwischen ihnen wird nichts verformt).

### 3.6 Ungültige Punkte, γ² < γ²_min, NaN (ADR-025)

Die Festlegung folgt ADR-025 (Punkte bleiben im Bild, gekennzeichnet, ohne Phasenpfeil) und überträgt sie auf die Bewegung:

| Zustand | Animation |
|---|---|
| gültig (M6) und $\gamma^2 \ge \gamma^2_\mathrm{min}$ und $\hat v$ endlich | bewegt sich nach 3.2 |
| $\gamma^2 < \gamma^2_\mathrm{min}$ | **steht in der Ruhelage** $\vec X_p$, mit demselben Kennzeichen wie in der Phasenansicht (graues Kreuz); geht nicht in $D_\mathrm{ref}$ ein |
| von PSV als ungültig markiert (M6) | **steht in der Ruhelage**, Kennzeichen „hohle Raute“; geht nicht ein |
| $\hat v$ oder $\hat d$ nicht endlich (NaN, Inf) | wie ungültig; **nie** stillschweigend durch 0 ersetzt und nie in Verbindungslinien oder Flächen einbezogen |
| $\lvert\hat v\rvert = 0$ exakt | bewegt sich nicht (Auslenkung 0), gültig; Phase undefiniert, kein Phasenpfeil (wie `waehle_bezugspunkt`) |

**Begründung** [A]: Die Phase eines Punkts mit γ² unter der Schwelle ist ein Rauschwert (FG-02 3.4: der Fehler wächst für γ² → 0 über alle Grenzen; bei wahrem γ² = 0 ist die Phase gleichverteilt [A]). Eine Animation mit dieser Phase wirkt glaubwürdig und ist falsch. Ein stehender Punkt ist die ehrlichere Aussage, **solange er gekennzeichnet ist**, denn „steht“ bedeutet hier „unbekannt“, nicht „Auslenkung null“. Ohne Kennzeichen entstünde der Eindruck einer Knotenlinie.

- **Maske je Komponente.** γ² hängt von der Komponente ab (FG-02 3.5). Bei der Einzelkomponente gilt die Maske dieser Komponente. Beim **3D-Vektor** bewegt sich ein Punkt nur, wenn alle drei Komponenten die Bedingung erfüllen; sonst steht er in der Ruhelage mit Kennzeichen „3D unvollständig“. Eine Teilbewegung (nur die gültigen Komponenten) würde die Bahnrichtung und die Bahnellipse verfälschen. Annahme [ANN A-1], Frage F2.
- **Verbindungslinien und Flächen** zwischen Punkten (R-072 betrifft Darstellung, hier nur die Fachregel): Es wird nicht über einen nicht animierten Punkt interpoliert. Kanten, an denen ein Endpunkt steht oder fehlt, werden nicht gezeichnet oder als nicht animiert gekennzeichnet. PSV rät für Rohdaten ebenfalls zu abgeschalteter Interpolation (W1, F11 Folie 31 [H]).
- **Keine Phase ohne Referenz.** Mit `phase_gueltig = False` gibt es keine Animation, die Anfrage wirft einen Fehler (RF-3D7, FG-02 3.6, `Schwingform.momentanwert`). Es gibt keine „Betrag-Pulsation“ ohne Vorzeichen: Eine Bewegung mit erfundenen Phasen wäre falsch.

### 3.7 Bilder je Periode (Entscheidung E3)

Ob die Wiedergabe in Bildern pro Periode quantisiert ist, hängt vom Weg ab:
- **Interaktiv** mit stetigem $\theta = 2\pi f_\mathrm{anim}\,t_\mathrm{real}$ ist die Phase nicht quantisiert; es gibt keinen fachlichen Mindestwert. Die Wiedergabegeschwindigkeit $f_\mathrm{anim}$ (Perioden je Sekunde Echtzeit) ist unabhängig von $f_{k^\ast}$ (Zeitlupe, Einstellung der Oberfläche), Aliasing im Sinne der Signalverarbeitung entsteht nicht, weil nicht die Echtzeit, sondern die Phase abgetastet wird.
- **Export und Wiedergabe mit $N$ Bildern je Periode:** Bild $j$ bei $\theta_j = 2\pi j/N$, $j = 0\dots N-1$; das Bild $\theta = 2\pi$ wird **nicht** erneut gezeigt (Duplikat, Stocken beim Schleifen).

**Herleitung** [A]: Fällt das Maximum eines Punkts zwischen zwei Bilder, liegt das nächste Bild höchstens $\pi/N$ daneben. Daraus folgt
$$\delta_\varphi \le \frac{\pi}{N}\ \text{(dargestellter Phasenfehler)},\qquad \frac{\Delta A}{A} = 1 - \cos\frac{\pi}{N}\ \text{(größte Unterschreitung der Spitzenauslenkung im Bild)}.$$
$N = 12$: 15°, 3,41 %. $N = 24$: 7,5°, 0,856 %. $N = 36$: 5°, 0,381 %. $N = 72$: 2,5°, 0,095 % [N, Brute-Force über 200 000 Zufallsphasen stimmt mit der Formel überein].

**Ableitbarer Mindestwert:** Er folgt nur, wenn man eine Toleranz $\delta_\varphi$ vorgibt, $N_\mathrm{min} = \lceil\pi/\delta_\varphi\rceil$. Als fachlich begründete Toleranz bietet sich der Zufallsfehler der Phase an: Eine feinere Quantisierung als $\sigma_\varphi$ bildet nur Rauschen ab (FG-02 3.4, $\sigma_\varphi \approx \sqrt{1-\gamma^2}/(\lvert\gamma\rvert\sqrt{2n_d})$ **[L-m, Bendat/Piersol, nicht gelesen]**). Bei der Schwelle $\gamma^2_\mathrm{min} = 0{,}9$ und $n_d = 7$ (Beispieldatei, M5) ist $\sigma_\varphi = 0{,}0891$ rad = 5,10° [N], also $N_\mathrm{min} = \lceil\pi/0{,}0891\rceil = 36$ (35,3). Bei $n_d = 25$: 2,70°, $N = 67$; bei γ² = 0,99, $n_d = 7$: 1,54°, $N = 117$. Der Wert hängt von den Daten ab und ist **kein Gerätegrenzwert**.

**Empfehlung E3:** $N = 36$ für den Export (Vielfaches von 4 und von 12: Bilder liegen exakt bei $0, T/4, T/2, 3T/4$, damit die Referenzfälle RF-A1 bis RF-A6 an Bildern geprüft werden können). Kleinere $N$ (nicht unter 12) nur mit der Angabe des Phasen- und Amplitudenfehlers aus der Tabelle; $N$ steht in der Beschriftung des Exports.

---

## 4 Ergebnisformeln (Zusammenfassung)

| Größe | Formel | Einheit |
|---|---|---|
| Linienfrequenz, Kreisfrequenz | $f_{k^\ast} = \mathrm{Achse}[k^\ast]$, $\omega = 2\pi f_{k^\ast}$ | Hz, rad/s |
| Auslenkungsamplitude | $\hat d_{pc} = \hat v_{pc}/(i\omega)$ | m (CPH) bzw. m/N (H1) |
| relativ gedrehte Amplitude | $\hat w_p = \hat v_p\,\hat v_b^{*}/\lvert\hat v_b\rvert$ | wie $\hat v$ |
| Momentanauslenkung | $d_{pc}(\theta) = \mathrm{Re}\{\hat d_{pc}\,e^{i\theta}\} = (\lvert\hat v_{pc}\rvert/\omega)\sin(\theta+\varphi_{pc})$ | m |
| Momentanschnelle (Option) | $u_{pc}(\theta) = \mathrm{Re}\{\hat v_{pc}\,e^{i\theta}\} = \lvert\hat v_{pc}\rvert\cos(\theta+\varphi_{pc})$ | m/s |
| Bildposition | $\vec x_p(\theta) = \vec X_p + s\sum_c \vec e_c\,d_{pc}(\theta)$ (animierte Punkte), sonst $\vec X_p$ | m |
| Bezugsgröße | $D_\mathrm{ref} = \max_p \lvert\hat d_{pc}\rvert$ bzw. $\max_p\,\texttt{auslenkung\_max}_p/\omega$ über animierte Punkte | m |
| Überhöhung (Voreinstellung) | $s = \alpha\,d_\mathrm{NN}/D_\mathrm{ref}$, $\alpha = 0{,}25$ | 1 |
| Maximum von Punkt $p$ | $\theta_{\max,p} = \pi/2 - \varphi_p$ (Weg), $-\varphi_p$ (Schnelle), mod $2\pi$ | rad |
| Bildwinkel | $\theta_j = 2\pi j/N$, $j = 0\dots N-1$ | rad |
| Fehler durch $N$ | $\delta_\varphi \le \pi/N$; $\Delta A/A = 1-\cos(\pi/N)$ | rad; 1 |

---

## 5 Referenzfälle (Tests)

Alle Sollwerte [N] im Prüfskript (Anhang). Abkürzungen: $f = 100$ Hz (Linie), $\omega = 628{,}3185307$ rad/s, $a = 1\,\mathrm{mm/s}/\omega = 1{,}5915494309\cdot10^{-6}$ m. $\theta_n = 0,\ \pi/2,\ \pi,\ 3\pi/2$ (Zeit $0, T/4, T/2, 3T/4$).

**Toleranz (allgemein):** Die Sollwerte sind geschlossene Ausdrücke in float64; Fehlerquelle ist nur die Rundung, gemessen $< 10^{-16}$ relativ. `rtol = 1e-12` für Werte ungleich null; Nullwerte (z. B. $\cos(\pi/2)\approx 6\cdot10^{-17}$) mit `atol = 1e-12·a` (bezogen auf die Amplitude des Falls), weil der Rundungsrest von $\theta_n$ so skaliert. Zeitpunkte des Maximums (RF-A4, A12) mit `atol = 1e-12` rad bei analytischer Auswertung bzw. halber Gitterbreite bei Suche auf einem Gitter.

| ID | Eingang | Sollwert | Toleranz |
|---|---|---|---|
| **RF-A1** Einzelpunkt reell | $\hat v = 10^{-3}$ m/s, $f = 100$ Hz | $\hat d = -i\cdot1{,}5915494309\cdot10^{-6}$ m. $d(\theta_n) = 0;\ +a;\ 0;\ -a$ (m). Schnelle: $u(\theta_n) = 10^{-3};\ 0;\ -10^{-3};\ 0$ m/s. Mit H1 = 1 (m/s)/N: $\hat d = -i\cdot1{,}5915494309\cdot10^{-3}$ m/N | rtol 1e-12, atol 1e-12·a |
| **RF-A2** Einzelpunkt mit Phase | $\hat v = 10^{-3}e^{i\pi/3}$ m/s | $d(\theta_n)/a = 0{,}8660254038;\ 0{,}5;\ -0{,}8660254038;\ -0{,}5$ (= $\sin(\theta_n + \pi/3)$) | rtol 1e-12 |
| **RF-A3** zwei Punkte gegenphasig | $\hat v_1 = 10^{-3}$, $\hat v_2 = -10^{-3}$ m/s | $d_2(\theta) = -d_1(\theta)$ für alle $\theta$ (13 Stützstellen, Summe $= 0$); $\Delta\varphi = +\pi$ (180° einheitlich); beide erreichen das Maximum um $T/2$ versetzt | atol 1e-12·a |
| **RF-A4** Phasenvorlauf | $\hat v_p = 10^{-3}$, $\hat v_q = i\cdot10^{-3}$ m/s | $\theta_{\max,p} = \pi/2$, $\theta_{\max,q} = 0$; $q$ erreicht das Maximum um $T/4$ früher ($\Delta t = -T/4 = -2{,}5$ ms bei 100 Hz) | atol 1e-12 rad |
| **RF-A5** reelle gegen komplexe Form | $\hat v = 3\cdot10^{-4}e^{i\varphi}$, $\varphi \in \{0;\ 0{,}7;\ -2{,}0;\ \pi\}$ rad | $\mathrm{Re}\{\hat d e^{i\theta}\} = (3\cdot10^{-4}/\omega)(\sin\varphi\cos\theta + \cos\varphi\sin\theta)$ für alle $\theta$; max. Abweichung gemessen $2\cdot10^{-22}$ m | atol 1e-12·(3e-4/ω) |
| **RF-A6** 3D, Kreisbahn | $\hat{\vec v} = 10^{-3}(1, i, 0)$ m/s | $\vec d(\theta_n)/a = (0,1,0);\ (1,0,0);\ (0,-1,0);\ (-1,0,0)$; Drehsinn im Uhrzeigersinn um $+z$, d. h. $m = \mathrm{Im}\,\hat v\times\mathrm{Re}\,\hat v = (0,0,-1)\cdot10^{-6}$, $\sigma = -1$ (FG-03 5.3); Halbachsen `auslenkung_max` = `auslenkung_min` = $a$ (bei der Schnelle $10^{-3}$ m/s, RF-3D1 mit Faktor $10^{-3}$) | atol 1e-12·a |
| **RF-A7** Überhöhung | RF-A1 mit $d_\mathrm{NN} = 0{,}029$ m, $\alpha = 0{,}25$; zweiter Punkt $\hat v = 0{,}5\cdot10^{-3}$ | $D_\mathrm{ref} = 1{,}5915494309\cdot10^{-6}$ m; $s = 4555{,}3093477$; $s\,D_\mathrm{ref} = 7{,}25\cdot10^{-3}$ m; angezeigte Amplitude Punkt 2 / Punkt 1 $= 0{,}5$ | rtol 1e-10 (s), rtol 1e-12 (Verhältnis) |
| **RF-A8** maskierter Punkt | RF-A7 plus dritter Punkt $\hat v = 10^{-2}$ m/s mit γ² < γ²_min | $s$ **unverändert** 4555,3093477 (der Punkt geht nicht in $D_\mathrm{ref}$ ein); $\vec x_3(\theta) = \vec X_3$ für alle $\theta$; Kennzeichen gesetzt. Gleiches für M6-ungültig und NaN-Amplitude | exakt (Gleichheit der Position), rtol 1e-12 (s) |
| **RF-A9** Linienfrequenz | $f_\mathrm{wahl} = 100{,}2$ Hz, $\Delta f = 0{,}625$ Hz (Achse $0{,}625\,k$), $\hat v = 10^{-3}$ m/s | Linie $k^\ast$ = 100,0 Hz (Index 159); $\lvert\hat d\rvert = 1{,}5915494309\cdot10^{-6}$ m. Mit $f_\mathrm{wahl}$ gerechnet wäre es $1{,}5883726855\cdot10^{-6}$ m ($-0{,}1996\,\%$): der Test muss das unterscheiden | rtol 1e-12 |
| **RF-A10** Polarität M8 | $\hat v = 10^{-3}(1,\ 0{,}5e^{1{,}1i},\ 0{,}8e^{-2{,}0i})$, $\hat v \to -\hat v$, $N = 36$ | absolut: Bildfolge für $-\hat v$ = Bildfolge für $\hat v$ um $N/2 = 18$ Bilder zyklisch verschoben (max. Abw. $10^{-21}$ m). Relativ ($b = 0$): $\hat w$ und alle Bilder **identisch** (Abw. 0) | atol 1e-12·a bzw. exakt |
| **RF-A11** relative Amplitude | Daten wie RF-A10, $b = 0$ | $\hat w_0 = 10^{-3}$ (reell, positiv); $\Delta\varphi = (0;\ 1{,}1;\ -2{,}0)$ rad $= (0°;\ 63{,}03°;\ -114{,}59°)$ | atol 1e-12 rad |
| **RF-A12** Bilder je Periode | $N = 36$ bzw. $12$ | $\theta_9 = \pi/2$; letztes Bild $\theta_{35} = 350°$ (kein Bild bei 360°); $\delta_\varphi \le 5°$; $\Delta A/A$ (worst case) $= 1-\cos 5° = 0{,}0038053$ ($N=36$), $0{,}034074$ ($N=12$) | rtol 1e-9 |
| **RF-A13** Weg gegen Schnelle | $\hat v = 10^{-3}e^{0{,}7i}$ m/s | $u(\theta) = \omega\,d(\theta + \pi/2)$ für alle $\theta$ (max. Abw. $6\cdot10^{-19}$ m/s) | atol 1e-12·1e-3 |
| **RF-A14** ohne Phase | `phase_gueltig = False` | Anfrage nach der Animation wirft `ValueError` (RF-3D7); es werden keine Phasen erfunden | – |

Die Fälle RF-A1, A2, A3, A4, A6 sind auf Bildern bei $T/4$-Vielfachen prüfbar ($N$ Vielfaches von 4).

---

## 6 Gültigkeit und Randfälle

**Voraussetzungen**
- **Stationarität und Linearität:** Die Animation zeigt eine rein harmonische Bewegung bei $f_{k^\ast}$. Sie ist eine Rekonstruktion aus **einer** spektralen Linie (kohärenter Anteil), keine Aufnahme der Bewegung. Anteile bei anderen Frequenzen (Oberwellen, Nichtlinearität) und das Rauschen fehlen.
- **Betriebsschwingform, nicht Eigenform:** Die Form ist die erzwungene Antwort bei dieser Anregung und Frequenz (ODS). Nahe benachbarte Moden überlagern sich; sie ist nur an einer isolierten Resonanz einer Eigenform ähnlich [A]. Belegt nur durch Herleitung; die Literatur zur ODS ist noch nicht gelesen (`schwarz1999ods`: Prüfstand **metadaten, UNSICHER**; RA-2).
- **Auflösungsbegrenzte Spitzen** ($B < \Delta f$, Kennzeichen `aufloesungsbegrenzt`): Die Phase wechselt von Linie zu Linie stark (HINWEIS_PHASE_SPRUNG); die Animation einer Linie ist dann eine Momentaufnahme. Hinweis in der Animation, wie in der Phasenansicht.
- **Gemeinsame Referenz** aller Punkte und Komponenten (die Phase aller Punkte bezieht sich auf dieselbe Ref1-Messung; bei Scans: Referenz oder Trigger nötig, FG-02 3.6).
- **Koordinaten:** Komponenten im Koordinatensystem der Geometrie (M12 offen).

**Randfälle**
- $f_\mathrm{wahl}$ außerhalb der Achse: `ValueError` (FG-02 3.6).
- $\omega = 0$: NaN, Punkt behandelt wie ungültig (3.1).
- Alle Punkte maskiert, ungültig oder NaN: Es gibt kein $D_\mathrm{ref}$, keine Überhöhung und keine Animation. Meldung „keine Punkte mit gültiger Phase“ statt Division durch null.
- $D_\mathrm{ref} = 0$ (alle $\lvert\hat v\rvert = 0$): wie oben.
- Nur ein animierter Punkt: $d_\mathrm{NN}$ aus allen Punkten (auch nicht animierten) berechnen; gibt es nur einen Punkt, ist $\alpha\,d_\mathrm{NN}$ nicht definiert, dann $s$ nur durch Nutzereingabe.
- Knotenlinien: Punkte mit sehr kleinem $\lvert\hat v\rvert$ bewegen sich kaum; ihre Phase ist (bei stehender Welle) $0°$ oder $180°$ und wechselt über der Knotenlinie. Das ist korrekt.
- Laufende Welle: Phasen steigen stetig mit dem Ort; die Animation zeigt eine laufende Welle. Das ist korrekt.
- Nyquist/obere Linie: kein Sonderfall, $\omega > 0$.
- Sehr große $s$: Hinweis nach 3.5; keine Begrenzung.
- Ändert die Oberfläche $\theta$ nicht stetig (Sprung), gilt die Bildzuordnung weiter, weil $x_p$ nur von $\theta$ abhängt (zustandslos).

---

## 7 Beobachtungen am vorhandenen Code (Stand 2026-11-09, nicht Teil der Aufgabe)

Nur Lesebefunde, damit die Umsetzung die Lücken kennt; Änderungen sind Sache des `software-engineer`:
1. `auswertung/schwingform.py`: `momentanwert` und `Schwingform.momentanwert` liefern $\mathrm{Re}\{\hat v e^{i\theta}\}$, also die **Schnelle**. Für die Auslenkung fehlt die Division durch $i\omega$ (mit $\omega = 2\pi f_\mathrm{hz}$ der Linie, Attribut `f_hz`). Bei Anwendung ohne Umrechnung wäre die Bildfolge um $T/4$ gegen die Auslenkung verschoben, die Beschriftung „Auslenkung“ aber falsch.
2. `Schwingform.amplitude` ist (P, 3) komplex mit allen drei Komponenten; `SchwingformDaten` in `darstellung/auswahl.py` trägt dagegen nur **eine** Komponente (P,) und für 3D `amplitude = None`, ebenso nur die Maske der einen Komponente. Für die 3D-Animation braucht der Datenvertrag Amplituden (P, 3) und Masken (P, 3) (3.6).
3. `darstellung/schwingform.py` ist eine statische Aufsicht (2D-Projektion auf eine Ebene); eine Animation existiert nicht. In der Aufsicht ist die Komponente entlang der Blickrichtung unsichtbar (3.4).
4. `phase_relativ_rad` liefert nur die Phase. Die gedrehte Amplitude $\hat w_p$ (3.2) fehlt.

---

## 8 Entscheidungen für den Nutzer (Optionen mit Empfehlung)

| Nr. | Frage | Optionen | Empfehlung |
|---|---|---|---|
| E1 | Welche Größe wird animiert? | (a) Auslenkung $\hat d = \hat v/(i\omega)$; (b) Schnelle $\hat v$ | **(a)** als Voreinstellung, (b) als Option. Form und Phasendifferenzen gleich, Zeitnullpunkt um $T/4$ verschoben |
| E2 | Skalierung | (a) ein Faktor für alle, $s = \alpha d_\mathrm{NN}/D_\mathrm{ref}$, $\alpha = 0{,}25$, einstellbar; (b) feste Überhöhung; (c) Normierung je Punkt | **(a)**; (c) verboten (verfälscht Amplituden) |
| E3 | Bilder je Periode im Export | $N = 12, 24, 36, 72$ | **36** (Begründung 3.7); interaktiv stetig |
| E4 | Phasenbezug der Animation | (a) absolut gegen Ref1 mit Kennzeichen M8; (b) relativ zu Bezugspunkt | beide anbieten; **für die Thesis (b)**, bis M8 geklärt ist (ADR-025) |
| E5 | Behandlung maskierter Punkte | (a) stehen in Ruhelage, gekennzeichnet; (b) ausblenden | **(a)** (ADR-025: Punkte bleiben im Bild) |

---

## 9 Quellen

| Kürzel | Quelle | Prüfstand | Verwendet für |
|---|---|---|---|
| FG-02, FG-03, ADR-025, FA-AUSW | Repo (`in_progress/fachgrundlagen/`, `entscheidungen/`, `analysen/`) | freigegeben bzw. Bericht | Konventionen, 3.6/3.7, Bahnellipse, Phasenbezug, Maske |
| I2, W1 | Analyseberichte (PSV-Animation: SWP S. 139–142, 4-23–4-26; F11 Folie 31) | Repo [H], Handbuchstellen nicht erneut gelesen | PSV animiert nur mit Referenz oder Trigger; Interpolation für Rohdaten abschalten |
| Bendat/Piersol (`bendat2010random`) | Random Data | **metadaten** | $\sigma_\varphi$ in 3.7 (nur als Orientierung der Toleranz) |
| Schwarz/Richardson (`schwarz1999ods`) | Introduction to Operating Deflection Shapes | **metadaten, UNSICHER** | nicht verwendet; nur für den Thesis-Text zur ODS-Definition zu beschaffen |

Alle Herleitungen und Zahlen dieser Fachgrundlage sind eigene Rechnung [A, N]. Keine Lehrbuchaussage wird als belegt behauptet.

---

## 10 Offene Punkte

**Rückfragen**
- F1 [nicht blockierend] E1 bis E5 (Abschnitt 8). *Annahme bis zur Klärung:* Empfehlungen.
- F2 [nicht blockierend] 3D-Animation: Bewegt sich ein Punkt nur, wenn alle drei Komponenten γ² ≥ γ²_min erfüllen (**[ANN A-1]**)? *Annahme:* ja.
- F3 [nicht blockierend] Welche Kodierung der Komponente senkrecht zur Bildebene (3.4)? Gestaltung beim `ui-designer`; fachlich nur: vorzeichenbehaftet, phasentreu.

**Annahmen:** A-1 (3D nur mit allen drei gültigen Komponenten); M8 und M12 bleiben offen und stehen als Kennzeichen in der Anzeige (3.2, 3.4); $\alpha = 0{,}25$ und $N = 36$ sind Vorschläge, keine Herstellerwerte.

**Rechercheaufträge**
- RA-1: In SWP S. 139–142 bzw. PSV-Handbuch 10.x nachsehen, **welche Größe** (Weg oder Schnelle) PSV animiert, wie die Skalierung/Überhöhung heißt und gewählt wird und wie ungültige Punkte dargestellt werden (Vergleichsbasis für R-071, R-072).
- RA-2: Definition der ODS und Abgrenzung zur Eigenform (Schwarz/Richardson 1999, Metadaten klären; ggf. Ewins 2000) für Grundlagen und Gültigkeit.

---

## Anhang: Prüfskript

Ausgeführt im Scratchpad (`fg04/fg04.py`, Python 3 mit NumPy); die gedruckten Werte sind in Abschnitt 5 übernommen.

```python
"""FG-04 Pruefskript: Animation der Betriebsschwingform (Sollwerte RF-A1 ... RF-A12)."""
import numpy as np

def auslenkung_amp(v, f_hz):
    """d^ = v^/(i w), w = 2 pi f_line."""
    return v / (1j * 2 * np.pi * f_hz)

def verschiebung(d, theta):
    """Re{d^ e^{i theta}}; d (...), theta (n) -> (..., n)."""
    d = np.asarray(d, complex); th = np.asarray(theta, float)
    return np.real(d[..., None] * np.exp(1j * th))

TH = np.array([0, np.pi/2, np.pi, 3*np.pi/2])
f = 100.0; w = 2*np.pi*f; a = 1e-3/w
print("a = 1e-3/w =", repr(a))

# A1
d = auslenkung_amp(1e-3 + 0j, f)
print("A1 d^ =", d, " u(0,T/4,T/2,3T/4) =", verschiebung(d, TH))
print("A1 Geschwindigkeit      =", np.real(1e-3*np.exp(1j*TH)))
# A2
v = 1e-3*np.exp(1j*np.pi/3); d = auslenkung_amp(v, f)
print("A2 u =", verschiebung(d, TH)/a, " (Soll sin(th+pi/3): 0.8660254, 0.5, -0.8660254, -0.5)")
print("A2 sin-Form:", np.sin(TH+np.pi/3))
# A3 gegenphasig
d1 = auslenkung_amp(1e-3+0j, f); d2 = auslenkung_amp(-1e-3+0j, f)
th = np.linspace(0, 2*np.pi, 13)
print("A3 max|u2+u1| =", np.max(np.abs(verschiebung(d1, th)+verschiebung(d2, th))))
dphi = np.angle(-1e-3 * np.conj(1e-3+0j)); print("A3 dphi =", dphi)
# A4 Phasenvorlauf: v_q = i v_p
dp = auslenkung_amp(1e-3+0j, f); dq = auslenkung_amp(1e-3j, f)
thf = np.linspace(0, 2*np.pi, 360001)[:-1]
tp = thf[np.argmax(verschiebung(dp, thf))]; tq = thf[np.argmax(verschiebung(dq, thf))]
print("A4 theta_max p, q =", tp, tq, " Differenz/(2pi) =", (tp-tq)/(2*np.pi), "(Soll 0.25 = T/4)")
# A5 reell vs komplex
for phi in [0.0, 0.7, -2.0, np.pi]:
    v = 3e-4*np.exp(1j*phi); d = auslenkung_amp(v, f)
    re = 3e-4/w*(np.sin(phi)*np.cos(thf) + np.cos(phi)*np.sin(thf))
    print("A5 phi=%.2f max Abw = %.3e (abs), a=%.3e" % (phi, np.max(np.abs(verschiebung(d, thf)-re)), 3e-4/w))
# A6 3D Kreis
v3 = 1e-3*np.array([1, 1j, 0]); d3 = auslenkung_amp(v3, f)
print("A6 u(theta) / a:\n", verschiebung(d3, TH)/a)
# A7 Skalierung
dNN, alpha = 0.029, 0.25
D = np.abs(auslenkung_amp(1e-3+0j, f)); s = alpha*dNN/D
print("A7 D =", D, " s =", s, " s*D =", s*D)
# zwei Punkte, Amplituden 1e-3 und 0.5e-3 + maskierter Punkt 1e-2
v = np.array([1e-3, 0.5e-3, 1e-2]); ok = np.array([True, True, False])
D2 = np.max(np.abs(v[ok]))/w; s2 = alpha*dNN/D2
print("A7b D =", D2, " s =", s2, " Verhaeltnis angezeigt =", (0.5e-3/w*s2)/(1e-3/w*s2))
# A8 f_wahl vs Linie
df = 0.625; fw = 100.2; k = int(np.argmin(np.abs(np.arange(1, 1601)*df - fw))); fl = (k+1)*df
print("A8 Linie", k, fl, " |d|(f_line)=", 1e-3/(2*np.pi*fl), " |d|(f_wahl)=", 1e-3/(2*np.pi*fw),
      " rel =", (1e-3/(2*np.pi*fw))/(1e-3/(2*np.pi*fl))-1)
# A9 M8: v -> -v
v = np.array([1e-3, 0.5e-3*np.exp(1j*1.1), 0.8e-3*np.exp(-2.0j)])
N = 36; thj = 2*np.pi*np.arange(N)/N
U = verschiebung(auslenkung_amp(v, f), thj); Um = verschiebung(auslenkung_amp(-v, f), thj)
print("A9 -v = Rolle um N/2:", np.max(np.abs(Um - np.roll(U, N//2, axis=1))))
rel = lambda v, b: v*np.conj(v[b])/abs(v[b])
print("A9 relativ M8-unabhaengig:", np.max(np.abs(rel(v,0) - rel(-v,0))))
print("A9 rel. Bezugspunkt reell positiv:", rel(v,0)[0], " dphi:", np.angle(rel(v,0)))
# A10 Frames
for N in [8, 12, 16, 24, 36, 72]:
    print("A10 N=%d  Phasenschritt %.2f deg  max Phasenfehler %.2f deg  Amplitudenverlust %.3f %%" %
          (N, 360/N, 180/N, 100*(1-np.cos(np.pi/N))))
# sigma_phi
for g2, nd in [(0.9, 7), (0.9, 25), (0.99, 7)]:
    s_ = np.sqrt(1-g2)/(np.sqrt(g2)*np.sqrt(2*nd)); print("sigma_phi gamma2=%.2f nd=%d: %.4f rad = %.2f deg ; N=pi/sigma = %.1f" % (g2, nd, s_, np.degrees(s_), np.pi/s_))
# Brute-force worst case amplitude loss over random phases
rng = np.random.default_rng(1); N = 36
ph = rng.uniform(0, 2*np.pi, 200000); thj = 2*np.pi*np.arange(N)/N
m = np.max(np.sin(thj[None, :] + ph[:, None]), axis=1)
print("A10 brute force worst N=36:", 1 - m.min(), " Formel:", 1-np.cos(np.pi/N))
# A11 Pitfall: Geschwindigkeit statt Auslenkung = Zeitverschiebung T/4
dd = auslenkung_amp(1e-3*np.exp(0.7j), f)
print("A11 u_v(th) = w*u_d(th+pi/2):", np.max(np.abs(np.real(1e-3*np.exp(0.7j)*np.exp(1j*thf)) - w*verschiebung(dd, thf+np.pi/2)[...,:] .reshape(-1)[:thf.size])))
```
