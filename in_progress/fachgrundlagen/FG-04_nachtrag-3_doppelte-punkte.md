<!-- Vom Nutzer am 2026-11-17 freigegeben (F-N3-1: Phasenansicht unverändert; F-N3-2: ε_rel = 1e-6, ε_abs = 1e-8 m wie festgelegt). -->

<!-- Nachtrag 3 zu FG-04: Ab welchem Abstand gelten zwei Ruhelagen als "gleicher Punkt" (d_NN der 3D-Animation). Erstellt im Paket FG-04-N3 von strukturdynamik-experte, Stand 2026-11-17. Status: ZUR FREIGABE. FG-04, Nachtrag 1 und 2 sind unverändert. -->

# FG-04, Nachtrag 3 – Doppelte Punkte beim Nächste-Nachbar-Abstand $d_\mathrm{NN}$

> **Status:** Entwurf zur Freigabe. Präzisiert FG-04 3.5 und Nachtrag 2 Abschnitt 4 („Abstand 0 zählt nicht“). Anlass: Re-Review R-AUSW3-2, MINOR „Nahezu gleiche Punkte“ (`animation_daten.py:343`, `abstand > 0.0`).

## 1 Zweck und Befund

Zwei Punkte im Abstand $10^{-9}$ m zählen bisher als Nachbarn. $d_\mathrm{NN,min}$ und der Median fallen auf $\approx 10^{-9}$ m, $s_\mathrm{auto}=\alpha\,d_\mathrm{NN}/D_\mathrm{ref}$ kollabiert, die Animation zeigt keine sichtbare Bewegung. Festzulegen: (1) die Toleranz, (2) was mit mehrfachen Duplikaten geschieht, (3) Randfälle.

Belegkennzeichen wie FG-04: **[A]** Herleitung, **[N]** numerisch (Anhang), **[D]** an der Datei geprüft, **[ANN]** Annahme.

## 2 Konvention

Koordinaten $\vec X_p$ in m im Koordinatensystem der Geometrie (Nachtrag 2 4.3); alle Punkte der Geometrie zählen (auch nicht animierte), wie bisher.

## 3 Festlegung

**Skala und Toleranz**

$$S=\max\Big(\big\lVert\max_p\vec X_p-\min_p\vec X_p\big\rVert,\ \max_p\lVert\vec X_p\rVert\Big),\qquad \varepsilon=\max\big(\varepsilon_\mathrm{abs},\ \varepsilon_\mathrm{rel}\,S\big),\quad \varepsilon_\mathrm{rel}=10^{-6},\ \ \varepsilon_\mathrm{abs}=10^{-8}\,\mathrm m .$$

$\max\min$ komponentenweise (achsparallele Umhüllende), Norm euklidisch, $S$ in m.

**Duplikat.** Punkt $i$ ist Duplikat, wenn es einen Punkt $j<i$ (kleinerer Index) mit $\lVert\vec X_i-\vec X_j\rVert\le\varepsilon$ gibt. **Gleichheit zählt als Duplikat** (auch $\varepsilon$ bei exakt gleichen Punkten).

**Nachbarabstand.** $d_\mathrm{NN}$ und $d_\mathrm{NN,min}$ werden **nur über die Nicht-Duplikate** (Repräsentanten, je Ort der erste Punkt) berechnet: Für jeden Repräsentanten das Minimum des räumlichen Abstands zu den **anderen** Repräsentanten, davon Median bzw. Minimum. Alle Abstände zwischen Repräsentanten sind $>\varepsilon$ (folgt aus der Definition [A]).

- Gibt es weniger als zwei Repräsentanten (ein Punkt, alle Punkte gleich, nur zwei Punkte mit Abstand $\le\varepsilon$): $d_\mathrm{NN}$ und $d_\mathrm{NN,min}$ **nicht definiert**; $s$ bzw. $\kappa$ nur durch Nutzereingabe, kein Überlagerungshinweis (wie FG-04 6, RF-D3).
- Duplikate werden weiter gezeichnet und animiert; sie überlagern sich bei jedem $s$ und lösen den Hinweis „Punkte können sich überlagern“ **nicht** aus (Hinweis gilt für Nachbarn, die sich erst durch die Überhöhung berühren, Nachtrag 2 3.4).
- **Empfehlung (Pflicht für das Datenobjekt, Anzeige Gestaltung):** Anzahl $n_\mathrm{dup}$ der Duplikate und $\varepsilon$ werden mitgeführt; bei $n_\mathrm{dup}>0$ erscheint ein Informationshinweis, z. B. „$n_\mathrm{dup}$ Punkte liegen auf dem Ort eines anderen Punkts (Abstand $\le\varepsilon$) und zählen bei $d_\mathrm{NN}$ nicht mit“ (Wortlaut Vorschlag).

## 4 Begründung

**Zwei Fehlerrichtungen [A].** Eine zu kleine Toleranz lässt Duplikate als Nachbarn zu: $s$ kollabiert (Befund). Eine zu große Toleranz unterdrückt **echte** eng liegende Punkte und damit den Überlagerungshinweis. Deshalb ist $\varepsilon$ **numerische** Gleichheit, nicht Messunsicherheit: Zwei Punkte, die wirklich 0,5 mm auseinanderliegen, sind zwei Messpunkte und bleiben Nachbarn (RF-DUP6b), auch wenn die Genauigkeit des 3D-Abgleichs im mm-Bereich liegen mag.

**Untere Schranke [D, A].** In der Beispieldatei (`Input/20261012_ref_Mitte.svd`, 135 Punkte) sind alle 405 Koordinaten **exakt als float32 darstellbar** [D] (Test $x=\mathrm{float32}(x)$). Daraus folgt (Schlussfolgerung, nicht Herstellerangabe [ANN]): Das PSV legt Koordinaten mit float32-Auflösung ab, das Quantum bei Beträgen 0,25 bis 0,5 m ist $2^{-25}=3{,}0\cdot10^{-8}$ m [N]. Ein zweimal gespeicherter oder umgerechneter Ort kann um ein paar Quanten abweichen. Das Quantum wächst mit dem Abstand zum Ursprung, deshalb steht $\max\lVert\vec X\rVert$ in $S$ (RF-DUP7: bei 10 m Abstand vom Ursprung 9,5·10⁻⁷ m, Toleranz allein aus der Ausdehnung 5,7·10⁻⁸ m würde das Duplikat verfehlen). Bei der Beispieldatei: $S=0{,}614$ m, $\varepsilon=6{,}1\cdot10^{-7}$ m = **20 float32-Quanten** (größtes Quantum 3,0·10⁻⁸ m) [N].

**Obere Schranke [ANN].** $\varepsilon$ muss weit unter jedem realen Punktabstand liegen. Beispieldatei: $d_\mathrm{NN}=23{,}87$ mm, kleinster Abstand 23,14 mm, also $\varepsilon/d_\mathrm{NN}=2{,}6\cdot10^{-5}$ und $d_\mathrm{NN,min}/\varepsilon=3{,}8\cdot10^{4}$ [N]. Annahme: Reale Messgitter haben Punktabstände von mindestens $10^{-4}S$ (bei $S=0{,}6$ m etwa 60 µm; **kein Gerätewert**, nur eine Größenordnung); dann liegt $\varepsilon_\mathrm{rel}=10^{-6}$ noch 100-fach darunter. Das Fenster zwischen float32-Quantum ($6\cdot10^{-8}S$) und dieser Obergrenze ($10^{-4}S$) umfasst gut 3 Dekaden; $10^{-6}$ liegt mit Faktor 17 über der unteren und 100 unter der oberen Grenze.

**Absoluter Boden $\varepsilon_\mathrm{abs}=10^{-8}$ m [ANN].** Eine reine Relativtoleranz versagt, wenn die Skala selbst winzig ist: Bei zwei Punkten ist die Umhüllende gleich ihrem Abstand, $\varepsilon_\mathrm{rel}S$ ist dann immer kleiner als der Abstand, zwei Punkte im Abstand $10^{-9}$ m nahe dem Ursprung würden nie als Duplikat erkannt (beim Prüfen aufgefallen [N]). $10^{-8}$ m = 10 nm liegt unter jeder plausiblen Positioniergenauigkeit eines Scansystems oder 3D-Abgleichs (**Genauigkeit des Geräts unbekannt**, Annahme), über dem float64-Rauschen und entspricht etwa einem float32-Quantum bei 0,1 m. Er wirkt nur bei $S<1$ cm. Der Wert ist änderbar, ohne dass die Fachlogik betroffen ist.

**Warum je Ort, nicht je Punkt [A, N].** Zählte man jeden Punkt einzeln (nur Partner innerhalb $\varepsilon$ überspringen), ginge ein dreifach vorhandener Ort dreifach in den Median ein: RF-DUP3 ergibt dann 0,025 m statt 0,015 m (+67 %), $s_\mathrm{auto}$ hinge davon ab, wie oft Orte doppelt gemessen wurden. Mit der Repräsentantenregel ist $d_\mathrm{NN}$ **invariant** gegen beliebig viele Duplikate (RF-DUP1, -DUP3, -DUP7).

## 5 Referenzfälle (Sollwerte im Anhang nachgerechnet)

Alle Koordinaten in m. $D_\mathrm{ref}=10^{-6}$ m (nur bei $s$), $\alpha=0{,}25$. **Toleranz** (KONVENTIONEN): halbe Einheit der letzten angegebenen Stelle des Sollwerts; Rundung der Rechnung liegt bei $<10^{-15}$ relativ, ist also nicht maßgeblich.

| ID | Eingang | Soll | Toleranz |
|---|---|---|---|
| **RF-DUP1** | 3×3-Raster Abstand 0,02 in der XY-Ebene ab Ursprung, dazu ein Punkt (1e-9, 0, 0) (10 Punkte) | $\varepsilon=5{,}657\cdot10^{-8}$; $n_\mathrm{dup}=1$; $d_\mathrm{NN}=d_\mathrm{NN,min}=0{,}02000$; $s=5000{,}0$. Bisherige Regel: $d_\mathrm{NN,min}=10^{-9}$ | atol 5e-6 (d), 0,05 (s) |
| **RF-DUP2** | (0,0,0), (1e-9,0,0), (0,03,0,0), (0,03; 1e-9; 0) (Fall aus dem Re-Review) | $\varepsilon=3{,}0\cdot10^{-8}$; $n_\mathrm{dup}=2$; $d_\mathrm{NN}=d_\mathrm{NN,min}=0{,}030000$ (gerechnet 0,0299999993); $s=7500$ (7499,9998). Bisher: beide $=10^{-9}$, $s\approx0$ | atol 5e-7 (d), 0,5 (s) |
| **RF-DUP3** | Reihe x = 0; 0,01; 0,03; 0,06, dazu zwei Duplikate (0,06; 1e-9; 0) und (0,06; 2e-9; 0) | $n_\mathrm{dup}=2$; Repräsentanten-Abstände 0,01; 0,01; 0,02; 0,03; $d_\mathrm{NN}=0{,}01500$; $d_\mathrm{NN,min}=0{,}01000$. (Negativtest: Zählung je Punkt ergäbe 0,025) | atol 5e-6 |
| **RF-DUP4** | vier Punkte um (0,1; 0,2; 0,3) mit Abweichungen $\le10^{-9}$; zusätzlich vier exakt gleiche Punkte (0,0,0) | $n_\mathrm{dup}=3$; $d_\mathrm{NN}$, $d_\mathrm{NN,min}$ **nicht definiert** (None); $s$ nur durch Nutzereingabe; kein Hinweis. Bei den Nullpunkten $\varepsilon=10^{-8}$ | exakt |
| **RF-DUP5a** | zwei Punkte (0,0,0), (0,02;0;0) | $d_\mathrm{NN}=d_\mathrm{NN,min}=0{,}02000$; $n_\mathrm{dup}=0$ | atol 5e-6 |
| **RF-DUP5b** | zwei Punkte (0,0,0), (1e-9,0,0) | $\varepsilon=10^{-8}$; $n_\mathrm{dup}=1$; nicht definiert | exakt |
| **RF-DUP6a** | (0,0,0), (1,0,0), (0,5e-6; 0; 0) | $\varepsilon=10^{-6}$; $n_\mathrm{dup}=1$; $d_\mathrm{NN}=d_\mathrm{NN,min}=1{,}0000$ | atol 5e-5 |
| **RF-DUP6b** | (0,0,0), (1,0,0), (2e-6; 0; 0) | $n_\mathrm{dup}=0$ (**echter Nachbar bleibt**); Abstände 2e-6; 0,999998; 2e-6; $d_\mathrm{NN}=d_\mathrm{NN,min}=2{,}00\cdot10^{-6}$ | atol 5e-9 |
| **RF-DUP7** | 3×3-Raster 0,02, um (10; 0; 0) verschoben, dazu Punkt im Abstand eines float32-Quantums in x (9,537e-7) | $S=10{,}040$, $\varepsilon=1{,}004\cdot10^{-5}$; $n_\mathrm{dup}=1$; $d_\mathrm{NN}=d_\mathrm{NN,min}=0{,}02000$ (aus $L$ allein wäre $\varepsilon=5{,}7\cdot10^{-8}$: Duplikat würde verfehlt) | atol 5e-6 |
| **RF-DUP8** (Realdaten) | `Input/20261012_ref_Mitte.svd`, 135 Punkte | $S=0{,}6142$, $\varepsilon=6{,}14\cdot10^{-7}$; $n_\mathrm{dup}=0$; $d_\mathrm{NN}=0{,}02387$ (23,875 mm), $d_\mathrm{NN,min}=0{,}02314$; **Ergebnis unverändert gegenüber der bisherigen Regel** | atol 5e-6 (nur Regressionsprüfung, Test mit der Datei nur wenn vorhanden) |

## 6 Gültigkeit und Randfälle

- **Kette** ($a$–$b$ und $b$–$c$ je $\le\varepsilon$, aber $a$–$c>\varepsilon$): wegen $\varepsilon\ll$ Raster praktisch ausgeschlossen. Definiert ist sie durch die Indexregel (jeder Punkt mit früherem Punkt innerhalb $\varepsilon$ ist Duplikat, auch wenn dieser selbst Duplikat ist); sie hängt von der Punktreihenfolge ab. **Kein Referenzfall.**
- **Nicht endliche Koordinaten** (NaN, ∞): nicht behandelt; die Funktion setzt endliche Koordinaten voraus (Aufgabe des Einlesens).
- **Einheit:** Koordinaten müssen in m vorliegen. Wurde mm als m gelesen, ändern sich $S$ und $\varepsilon$ mit, der Boden $\varepsilon_\mathrm{abs}$ nicht; das bleibt Voraussetzung (Nachtrag 2 4.3).
- **Zwei Punkte** liegen im Grenzfall $d$ zwischen $\varepsilon$ und $2\varepsilon$ nicht in einem Referenzfall, weil dort die Rundung der Abstandsberechnung entscheidet; Referenzfälle halten Faktor $\ge2$ Abstand zur Grenze (6a, 6b).
- **Gleiche Position, verschiedene Messdaten:** Duplikate können verschiedene Amplituden haben (z. B. Mehrfachmessung). Die Regel betrifft nur $d_\mathrm{NN}$, nicht die Daten; $D_\mathrm{ref}$ bleibt das Maximum über alle bewegten Punkte.
- **Rechenaufwand:** Die Duplikatprüfung nutzt dieselbe Abstandsmatrix wie $d_\mathrm{NN}$ (Nachtrag 2 4.3, blockweises Verfahren bei großem $P$); das Ergebnis darf davon nicht abhängen.

## 7 Quellen

Keine Literatur nötig: eigene Herleitung [A], Prüfskript [N], Datei [D]. Die float32-Ablage ist aus der Darstellbarkeit der Werte geschlossen, **nicht** aus der Herstellerdokumentation belegt [ANN].

## 8 Offene Punkte

- **F-N3-1** [nicht blockierend] Gilt dieselbe Regel für den **ebenen** Nachbarabstand der Phasenansicht (ADR-025, `schwingform.py:257ff`, „Abstand 0 zählt nicht“)? *Annahme:* eigener Nachtrag/ADR-Änderung, hier nicht festgelegt; dort sind Punkte, die in der Ebene zusammenfallen, aber im Raum verschieden sind, ein anderer Fall (echte Überdeckung im Bild).
- **F-N3-2** [nicht blockierend] $\varepsilon_\mathrm{rel}=10^{-6}$ und $\varepsilon_\mathrm{abs}=10^{-8}$ m sind begründete Annahmen, keine Gerätewerte. *Annahme bis zur Klärung:* wie festgelegt; sobald Genauigkeit von Scankopf und 3D-Abgleich vorliegt (Herstellerangabe, Rechercheauftrag), prüfen, ob größere Duplikate (mm) als „gleicher Punkt“ gelten sollen. Das wäre eine **andere** Frage (physikalische Gleichheit) und würde den Überlagerungshinweis für echte Nahpunkte ausschalten.
- **F-N3-3** Wortlaut des Informationshinweises (Abschnitt 3) ist Gestaltung (`ui-designer`/Umsetzung).

## 9 Anhang: Prüfskript

Scratchpad: `/tmp/claude-0/-home-user/e6b61297-17fb-5003-91f8-95c4534d012c/scratchpad/fg04n3/pruef_n3.py`, ausgeführt aus `software/` mit `uv run --offline python`, Ausgabe „alle Pruefungen bestanden“ (Realdatenteil liest die Beispieldatei mit `lese_svd`).

```python
"""FG-04 Nachtrag 3: Duplikatregel fuer d_NN (Referenzfaelle RF-DUP1..7)."""
import numpy as np

EPS_REL = 1e-6
EPS_ABS = 1e-8  # m, Annahme


def skala(x):
    """S = max(Bounding-Box-Diagonale, groesste Entfernung vom Ursprung) in m."""
    x = np.asarray(x, float)
    diag = float(np.linalg.norm(x.max(0) - x.min(0)))
    return max(diag, float(np.max(np.linalg.norm(x, axis=1))))


def eps_dup(x):
    return max(EPS_ABS, EPS_REL * skala(x))


def dubletten(x):
    """True fuer Punkte, die Duplikat eines frueheren Punkts sind (Abstand <= eps)."""
    x = np.asarray(x, float)
    eps = eps_dup(x)
    d = np.linalg.norm(x[:, None] - x[None], axis=2)
    frueher = np.tril(np.ones(d.shape, bool), k=-1)  # j < i
    return np.any((d <= eps) & frueher, axis=1)


def d_nn(x):
    """(Abstaende zum naechsten Nachbarn der Repraesentanten, n_dup)."""
    x = np.asarray(x, float)
    dup = dubletten(x)
    r = x[~dup]
    if r.shape[0] < 2:
        return np.empty(0), int(dup.sum())
    d = np.linalg.norm(r[:, None] - r[None], axis=2)
    np.fill_diagonal(d, np.inf)
    return d.min(1), int(dup.sum())


def d_nn_alt(x):
    """Bisherige Regel (nur Abstand exakt 0 zaehlt nicht), zum Vergleich."""
    x = np.asarray(x, float)
    d = np.linalg.norm(x[:, None] - x[None], axis=2)
    d = np.where(d > 0, d, np.inf)
    k = d.min(1)
    return k[np.isfinite(k)]


def stat(x):
    n, nd = d_nn(x)
    if n.size == 0:
        return None, None, nd
    return float(np.median(n)), float(n.min()), nd


def gitter(a, nx=3, ny=3, off=(0.0, 0.0, 0.0)):
    return np.array([[i * a + off[0], j * a + off[1], off[2]] for j in range(ny) for i in range(nx)])


def zeige(name, ist, soll, tol):
    ok = all(abs(i - s) <= tol for i, s in zip(ist, soll) if s is not None)
    print(f"{name}: ist={ist} soll={soll} tol={tol} -> {'OK' if ok else 'FEHLER'}")
    assert ok, name


alpha = 0.25

# RF-DUP1
x = gitter(0.02)
x1 = np.vstack([x, [1e-9, 0, 0]])
m, mn, nd = stat(x1)
print("RF-DUP1 S, eps:", skala(x1), eps_dup(x1), "n_dup", nd, "alt min", d_nn_alt(x1).min())
zeige("RF-DUP1", (m, mn), (0.02, 0.02), 5e-7)
assert nd == 1
s = alpha * m / 1e-6
zeige("RF-DUP1 s", (s,), (5000.0,), 0.05)

# RF-DUP2 (zwei Paare 1e-9)
x2 = np.array([[0, 0, 0], [1e-9, 0, 0], [0.03, 0, 0], [0.03, 1e-9, 0]])
m, mn, nd = stat(x2)
print("RF-DUP2 S, eps:", skala(x2), eps_dup(x2), "n_dup", nd, "Rep-Abst", d_nn(x2)[0])
alt = d_nn_alt(x2)
print("  alt: min", alt.min(), "median", np.median(alt))
zeige("RF-DUP2", (m, mn), (0.030000, 0.030000), 5e-7)
assert nd == 2
zeige("RF-DUP2 s", (alpha * m / 1e-6,), (7500.0,), 0.5)

# RF-DUP3 Mehrfachdubletten, ungleichmaessige Reihe
x3 = np.array([[0, 0, 0], [0.01, 0, 0], [0.03, 0, 0], [0.06, 0, 0], [0.06, 1e-9, 0], [0.06, 2e-9, 0]])
m, mn, nd = stat(x3)
print("RF-DUP3 eps", eps_dup(x3), "n_dup", nd, "Rep-Abst", d_nn(x3)[0])
zeige("RF-DUP3", (m, mn), (0.015, 0.010), 5e-8)
assert nd == 2
punkt = np.median(d_nn_alt(np.array([[0, 0, 0], [0.01, 0, 0], [0.03, 0, 0], [0.06, 0, 0], [0.06, 1e-12, 0], [0.06, 2e-12, 0]])))
print("  Gegenprobe pro-Punkt-Zaehlung (Duplikate zaehlen als Punkte, aber nicht als Nachbarn):")
d = np.linalg.norm(x3[:, None] - x3[None], axis=2)
d = np.where(d > eps_dup(x3), d, np.inf)
pp = d.min(1)
print("  pro Punkt:", pp, "Median", np.median(pp))

# RF-DUP4 alle gleich
x4 = np.array([[0.1, 0.2, 0.3], [0.1 + 1e-9, 0.2, 0.3], [0.1, 0.2 + 1e-9, 0.3], [0.1, 0.2, 0.3]])
print("RF-DUP4", stat(x4), "eps", eps_dup(x4))
assert stat(x4)[:2] == (None, None) and stat(x4)[2] == 3
x4b = np.zeros((4, 3))
assert stat(x4b)[:2] == (None, None) and eps_dup(x4b) == 1e-8 and stat(x4b)[2] == 3

# RF-DUP5 zwei Punkte
x5 = np.array([[0, 0, 0], [0.02, 0, 0]])
m, mn, nd = stat(x5)
zeige("RF-DUP5a", (m, mn), (0.02, 0.02), 5e-7)
x5b = np.array([[0, 0, 0], [1e-9, 0, 0]])
print("RF-DUP5b", stat(x5b), "eps", eps_dup(x5b))
assert stat(x5b) == (None, None, 1)

# RF-DUP6 Grenze
x6a = np.array([[0, 0, 0], [1, 0, 0], [0.5e-6, 0, 0]])
x6b = np.array([[0, 0, 0], [1, 0, 0], [2e-6, 0, 0]])
print("RF-DUP6 eps", eps_dup(x6a), eps_dup(x6b))
m, mn, nd = stat(x6a)
zeige("RF-DUP6a", (m, mn), (1.0, 1.0), 0.05)
assert nd == 1
m, mn, nd = stat(x6b)
zeige("RF-DUP6b", (m, mn), (2.0e-6, 2.0e-6), 5e-9)
assert nd == 0
print("  RF-DUP6b alle:", d_nn(x6b)[0])

# RF-DUP7 fernes Gitter (float32-Quantum)
xf = gitter(0.02, off=(10.0, 0.0, 0.0))
ulp = float(np.spacing(np.float32(10.0)))
xf7 = np.vstack([xf, [10.0 + ulp, 0, 0]])
print("RF-DUP7 ulp32(10 m)=", ulp, "S", skala(xf7), "eps", eps_dup(xf7), "eps nur aus L:", EPS_REL * np.linalg.norm(xf7.max(0) - xf7.min(0)))
m, mn, nd = stat(xf7)
zeige("RF-DUP7", (m, mn), (0.02, 0.02), 5e-7)
assert nd == 1

# Realdaten
from ldv_automation.auswertung.svd_lesen import lese_svd
xr = lese_svd("/home/user/BA_Jakob-Busch_P/Input/20261012_ref_Mitte.svd").punkte.koordinaten_m
print("Real: float32-exakt:", bool(np.all(xr == xr.astype(np.float32).astype(np.float64))))
print("Real: L", float(np.linalg.norm(xr.max(0) - xr.min(0))), "max|x|", float(np.max(np.linalg.norm(xr, axis=1))), "S", skala(xr), "eps", eps_dup(xr))
print("Real: groesste ulp32", float(np.max(np.spacing(np.abs(xr).astype(np.float32)))), "n_dup", int(dubletten(xr).sum()))
m, mn, nd = stat(xr)
print("Real: d_NN median", m, "min", mn, "eps/d_NN", eps_dup(xr) / m, "d_NN,min/eps", mn / eps_dup(xr))
print("alle Pruefungen bestanden")
```
