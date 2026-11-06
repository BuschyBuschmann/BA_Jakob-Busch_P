# FG-V1 – Prüfdateien Fenster/Mittelung und Plausibilitätskriterien der ersten Warteschlangen-Messung

**Status:** FREIGEGEBEN (Nutzer, 2026-11-05) aus Fachanalyse FA-V1 (strukturdynamik-experte, sonnet). Gilt für den Termin am PSV-Messrechner (Mo 2026-11-09, PSV 10.4).
**Zweck:** Sollwerte und Erwartungen für (1) zwei zusätzliche .svd-Dateien (A: Hanning, B: Betragsmittelung 10) samt Referenzdatei R, mit denen das Fenster-Feld und das Mittelungs-Feld im .svd-Leser identifiziert werden, und (2) die fachliche Plausibilitätsprüfung der ersten automatisierten Messung (T4 bis T6).
Kennzeichnung: **[N]** nachgerechnet im Prüfskript (Anhang), am Gerät nicht geprüft; **[TM]** Polytec Theory Manual (Stand Software 9.1, `polytec2015theory`); **[SM]** Polytec Software Manual PSV 10.1 (`polytec2022psvsoftware`); **[D]** aus der Beispieldatei `20261012_ref_Mitte.svd` gerechnet; **[A]** Annahme; **[H]** Hypothese, am Gerät zu prüfen.

## 1 Konventionen (unverändert aus FG-02)
Einseitige Spitzenwert-Spektren, $\hat X_k = \frac{2}{\sum w_n}\sum w_n x_n e^{-i2\pi kn/N}$, Zeitabhängigkeit $e^{+i\omega t}$, $W_\mathrm{RBW}=N\sum w_n^2/(\sum w_n)^2$. $N=4000$, $f_s=2500$ Hz, $\Delta f=0{,}625$ Hz, $T=1{,}6$ s. Hanning periodisch, $w_n=0{,}5-0{,}5\cos(2\pi n/N)$.

## 2 Fenster Hanning gegenüber Rechteck: Sollwerte
| Größe | Rechteck | Hanning | Beleg |
|---|---|---|---|
| $W_\mathrm{RBW}$ | 1,0 | 1,5 | [TM] Tab. 5.1 (S. 5-7); [N] |
| Amplitude eines Tons auf einer Linie | $A$ | $A$ (gleich) | [TM] 3.2 (S. 3-3) „Scaling“, [N] |
| Skalierungsfaktor gegenüber $2/N$ | 1 | 2 | [N] ($N/\sum w=2$) |
| Rauschboden (stationär, breitbandig), AP-Verhältnis Hanning/Rechteck | – | 1,5 (+1,76 dB) | [N] MC 1,5005 |
| Korrelation benachbarter Linien (komplexes Rauschspektrum) | 0 | −2/3 | [N] analytisch und MC (−0,6666) |
| Korrelation der AP-Schwankung benachbarter Linien | 0 | $(2/3)^2=0{,}444$ | [N] MC 0,4447 (auch für $n_d=7$) |
| max. Amplitudenfehler (Ton zwischen zwei Linien) | −36 % | −15 % | [TM] Tab. 5.1; FG-02 RF-S2 |
| Gesamtleistung $\sum_k \mathrm{AP}_\mathrm{Ref1}$, Verhältnis A/R | 1 | $4\langle w^2\rangle_x\in(0;4]$; 1,5 bei zeitlich gleichmäßiger Energie, 2,77 Burst über mittlere 50 % der Blockdauer, 3,75 über 20 % | [N] Parseval |
| RMS-Korrektur (Kanaleigenschaft `WindowFunctionRMSCorrection`) | 1,0 [D] | **[H]** entweder 2,0 oder 1,633 ($1/\sqrt{\langle w^2\rangle}$) oder 1,0; im Dialog/File Access ablesen | [N] Kandidaten |
| Spitze mit $B<\Delta f$ in $|H_1|$ bei stationär-zufälliger Anregung | Bezug | $H_{1,A}[k]=\tfrac23H_k+\tfrac16(H_{k-1}+H_{k+1})$, Spitze × 0,69 bis 0,71 (−29 bis −31 %) | [N], nur für zufällige Anregung hergeleitet |

Fenster-Code: `PTCWindowFunction` Rechteck 0, Hanning 7, Tapered Hanning 8 ([BEM] `PolyMathLib/PTCWindowFunction.md`). Hanning hat keinen Parameter (anders als Tapered Hanning, Force, Exponential; [SM] 7.2.5), das Kanalrecord-Layout sollte also gleich lang bleiben **[H]**.

## 3 Mittelung Betrag(10) gegenüber Komplex(7): Sollwerte
`PTCAverageType` Betrag 1, Komplex 2; `Count` zulässig 3 bis 10000 ([BEM] `AverageAcqPropertiesContainer.md`).

* **H1, H2 und Kohärenz werden vom Mittelungstyp nicht beeinflusst** [TM] 6.4 (S. 6-5): „For cross power signals complex averaging is used even if magnitude averaging mode is selected … The method of averaging has no influence on the signals H1/H2/Coherence.“ Folge: Der Typ ist **nicht** an H1 oder Kohärenz erkennbar. Differenzen H1(B) − H1(R) sind reine Zufallsfehler: $\varepsilon\approx\sqrt{1-\gamma^2}/(\gamma\sqrt{2n_d})$ (FG-02 3.4): $\gamma^2=0{,}999$: 0,85 % ($n_d=7$) bzw. 0,71 % (10); $\gamma^2=0{,}99$: 2,7 % bzw. 2,2 %; $\gamma^2=0{,}9$: 8,9 % bzw. 7,5 % [N].
* Ändern kann sich nur das Antwortspektrum (CPH, „Spektrum“ von Vib und Ref2): Bei Betragsmittelung wird $\langle|V|\rangle$ mit der Phase des Kreuzspektrums belegt [TM] 6.4, Tab. 6.1. In der Beispieldatei gilt $|\mathrm{CPH}|=|\mathrm{CP}|/\sqrt{\mathrm{AP}_\mathrm{Ref}}$ auf 10⁻⁷ [D]. Erwartetes Verhältnis $\rho=|\mathrm{CPH}_B|/(|\mathrm{CP}|/\sqrt{\mathrm{AP}_\mathrm{Ref}})$ als Funktion der wahren Kohärenz (Median, $|R|$ nahezu konstant wie in der Datei, AP/ABS² = 1,00001 [D]) [N]:

| $\gamma^2$ | 0,9999 | 0,99 | 0,9 | 0,7 | 0,5 | 0,3 | 0,1 |
|---|---|---|---|---|---|---|---|
| $\rho$, $n_d=7$ | 1,000 | 1,002 | 1,022 | 1,087 | 1,213 | 1,468 | 2,066 |
| $\rho$, $n_d=10$ | 1,000 | 1,002 | 1,024 | 1,095 | 1,235 | 1,512 | 2,234 |

  Bei $\gamma^2\approx0{,}9999$ (Beispieldatei, Median 0,99988 über 60 bis 1000 Hz [D]) ist der Typ im Spektrum **nicht unterscheidbar**. Nutzbar sind nur Linien mit $\hat\gamma^2<0{,}9$: in der Beispieldatei 0,94 % aller Linien (≈ 15 je Punkt), $<0{,}5$: 0,31 % (≈ 5 je Punkt, Median bei 7,5 Hz) [D]. Bei 3×3 Punkten also ca. 135 bzw. 45 Linien, bei einem Einzelpunkt nur ca. 5. Binnen nach $\hat\gamma^2$ aus derselben Datei verzerrt (Selektionsbias); Richtung und Größenordnung zählen, kein Zahlenvergleich.
* Rauschboden (nur für rauschdominierte Linien): komplex fällt wie $1/\sqrt{n}$ (−8,45 dB bei 7, −10,0 dB bei 10), Betrag nicht [N].
* Blockzahl je Punkt (Feld +0x3C): erwartet Minimum = Count (R, A: 7; B: 10) **[H]**; Maximum bis Count × SE-Faktor ([SM] 7.2.7: „Defaults“ bis 3×, „Best“ bis 5×; in der Beispieldatei 7 bis 25, also nicht „Fast“).
* Magnitude ist laut [SM] 7.2.1 für Messungen ohne Referenz/Trigger oder stochastische Anregung gedacht; B (mit Ref1) ist ein Prüfaufbau, keine empfohlene Messkonfiguration.

## 4 Dateiplan R, A, B (alle gleiche .set, gleiches 3×3-Raster, kurz nacheinander)
| Datei | Änderung gegenüber R | Zweck |
|---|---|---|
| R | keine; Einstellungen der Beispieldatei: FFT, 1000 Hz, 1600 Linien, $f_s=2500$ Hz, 4000 Abtastwerte, Überlappung 0, Rechteck, Komplex 7, SE wie Beispiel, Trigger aus, Generator 0,02 V, Zeitdaten aus | Grundlinie für Diff und Spektrenvergleich; zugleich Referenzscan von D1 und Vergleichsmessung für T4 |
| A | Fenster Rechteck → Hanning, alle aktiven Kanäle | Fenster-Feld, $W_\mathrm{RBW}$, Skalierung |
| B | Fenster zurück auf Rechteck; Mittelung Komplex 7 → Betrag 10 (Typ und Anzahl, Vorgabe des Nutzers) | Mittelungs-Feld; Aussagen aus Abschnitt 3 |

Erwartete Stream-Änderungen: Ein Stream-Vergleich (olefile, Byte-Diff je Stream unter `Info/` und je `Static_Info`) R↔Beispieldatei liefert die Grundlinie der von Einstellungen unabhängigen Felder (Zeit, Kennungen).
* R→A: `Info/DAQ_Settings_Fft/Channels` (3436 Byte in der Beispieldatei, 11 Kanalrecords): ein int32 0→7 je aktivem Kanal (mindestens Vib 3D, Ref1, Ref2) **am gleichen relativen Offset im Record** und der double „RMS-Korrektur“ 1,0→c; `Average`, `Fft`, `Global`, `Trigger`, `SignalEnhancement` unverändert **[H]**.
* R→B: `Average` `[1,2,0,7]` → `[1,1,0,10]` (int32 an Offset 4 und 12); `Global` Offset 0 enthält in der Beispieldatei ebenfalls die 7 (Bedeutung offen): ändert es sich auf 10, ist es die Anzahl; `Static_Info`-Formeln der 17 Signale gleich oder geändert: offen **[H]**.
* Abnahme „gesichert“: Fenster, wenn (a) ein einziges Offsetmuster 0→7 in ≥ 3 Kanalrecords auftritt und (b) COM-Rücklesewert `WindowFunction`=7 und RMS-Korrektur zum Dateiwert passen. Mittelung, wenn `Average` genau `[1,1,?,10]` zeigt und COM `Type`=1, `Count`=10 liest (beide Werte stimmen unabhängig überein; Feld 2 bleibt „offen“, solange es konstant 0 bleibt). Eine dritte Datei (Komplex 10) ist dafür nicht nötig.

## 5 Plausibilitätskriterien für die erste automatisierte Messung (3×3, Generator wie Beispieldatei)
Kriterien (Vorschläge, [A] wo kein Beleg):
| Nr | Kriterium | Soll |
|---|---|---|
| K1 | Zustand FERTIG, Datei vorhanden, vom Leser lesbar, 9 Punkte | Dateigröße ca. 3,5 MB (9 × 185,7 kB + 1,82 MB [N]), 2,8 bis 4,2 MB [A] |
| K2 | Fft und Mittelung aus Datei gleich der .set | exakt: 2500 Hz, 4000, 1600, 1000 Hz, 0,625 Hz, Komplex 7 |
| K3 | Punktstatus | alle 9 gültig (1) oder optimal (3) |
| K4 | Leser-Prüfungen | P-01 bis P-06 ok; P-07 q ≥ 0,9; P-09 ≤ 0,05 (Beispiel 0,0108) |
| K5 | Anregung wirksam | Median $\gamma^2$(Vib Z/Ref1), 60 bis 1000 Hz, je Punkt ≥ 0,99 (Beispiel 0,99988); 0,9 bis 0,99 Hinweis; < 0,9 Befund |
| K6 | Kraft | Effektivwert Ref1 0,43 N ± 10 % [A] (bei 0,02 V, gleicher Verstärkerstellung); gegenüber R ± 3 % [A] |
| K7 | Spitzen | lokales Maximum von $|H_1|$ bei 160,625 ± 0,625 Hz (Fenster 158,75 bis 163,75 Hz) und 247,5 ± 0,625 Hz (245,6 bis 250,6 Hz) in ≥ 7 von 9 Punkten [A] |
| K8 | Pegel | Vib-Z-Effektivwert 0,3 bis 10 mm/s [A]; kein Overrange |
| K9 | Gegenprobe T4 gegen R | Spitzen ± 1 Linie; Linien mit $\gamma^2\ge0{,}99$: $|\Delta H|/|H|\le3\sqrt{\varepsilon_R^2+\varepsilon_T^2}$ in ≥ 90 % der Linien [A] |
| K10 | Dauer 3×3 | 100,8 s (Minimum) bis 504 s (Count 7, SE ×5); typisch 160 s [N] |

Zahlenbasis [D]: Beispieldatei, Punktstatus 100 % gültig/optimal (13,3 % / 86,7 %); Kraft-Effektivwert $\sqrt{\sum\mathrm{AP}_\mathrm{Ref1}/2}$ = 0,4287 bis 0,4313 N über alle 135 Punkte; Vib-Z-Effektivwert 0,84 bis 4,5 mm/s (Messbereich 50 mm/s); Kohärenz Vib Z/Ref1 Median 0,99988 (60 bis 1000 Hz), kleinster Punktmedian 0,99916; lokales Maximum von $|H_1|$ in 158,75 bis 163,75 Hz bei Linie 160,625 Hz in 99 % der Punkte, in 245,6 bis 250,6 Hz bei 247,5 Hz in 92 %; Drift innerhalb der Beispielmessung −0,13 Hz bei 603,2 Hz in 40 min (FG-03 4.5); Punktabstand im Beispielraster 69,2 mm (Label +1) und 48 bis 50 mm (Label +29), Koordinaten Label 132/133/134/161/162/163/190/191/192 aus dem Leser. Ohne Anregung wäre $E[\hat\gamma^2]=1/n_d=0{,}143$ ($n_d=7$), 95-%-Quantil 0,393 [N, FG-02 3.4]. Zeit: physikalisches Minimum $9\times7\times1{,}6$ s = 100,8 s; Beispiel 17,8 s je Punkt (2,7 min je 3×3); Höchstwert Count × 5 × 1,6 s × 9 = 504 s (R) bzw. 720 s (B) [N].

## 6 Offene Punkte
Bedeutung von Feld 2 im Stream `Average` und von `Global`-Offset 0; ob PSV das Antwortspektrum bei Betragsmittelung tatsächlich als $\langle|V|\rangle$ speichert [H]; Wert der RMS-Korrektur bei Hanning [H]; SE-Stufe der Beispieldatei (Fast/Defaults/Best) aus dem SE-Dialog; ob PSV bei Fensterwechsel weitere Felder (z. B. Überlappung) ändert; Theory Manual nur Stand 9.1, Manual 10.4 vom Messrechner steht aus (E2).

## 7 Quellen
`polytec2015theory` (3.2, 5.4, 5.5 Tab. 5.1, 6.3, 6.4, Tab. 6.1), `polytec2022psvsoftware` (7.2.1, 7.2.5, 7.2.7), Basic Engine Manual (`PTCWindowFunction`, `PTCAverageType`, `AverageAcqPropertiesContainer`, `ChannelAcqProperties`), FG-02 (2.1, 3.3, 3.4, 4), FG-03 (4.2, 4.5), Faktenliste 2026-11-02 (C1 bis C4, D6), `harris1978windows`, `bendat2010random` (nicht gelesen, nur über FG-02).

## Anhang: Prüfskript (Scratchpad-Skript `fa_v1_pruefung.py`, Python 3 mit NumPy; Ausgabe siehe Werte oben)

```python
"""FA-V1: Nachrechnung der Sollwerte (Fenster Hanning, Betragsmittelung, Plausibilitaet).
Scratchpad-Skript, nicht im Repository."""
import numpy as np
rng = np.random.default_rng(20261109)

# ---- S1: Fenster ---------------------------------------------------------------
N = 4000
n = np.arange(N)
w_h = 0.5 - 0.5*np.cos(2*np.pi*n/N)          # periodisch
w_r = np.ones(N)
wrbw = lambda w: N*np.sum(w**2)/np.sum(w)**2
print("S1a W_RBW rect, hann:", wrbw(w_r), wrbw(w_h))                 # 1, 1.5
print("S1b Skalierungsfaktoren 2/sum(w):", 2/np.sum(w_r)*N, 2/np.sum(w_h)*N)  # in Einheiten 2/N: 1, 2
print("S1c RMS-Korrektur-Kandidaten Hann: 1/sqrt(mean w^2) =", 1/np.sqrt(np.mean(w_h**2)), " N/sum(w)=", N/np.sum(w_h))
print("S1d 10log10(1.5) dB =", 10*np.log10(1.5))
# Sinus auf Linie 64: Amplitude bleibt
t = n/2500.0; df = 2500/N
x = 2*np.cos(2*np.pi*64*df*t+np.pi/3)
for nm, w in [("rect", w_r), ("hann", w_h)]:
    X = 2/np.sum(w)*np.fft.fft(w*x)
    print("S1e", nm, abs(X[64]))
# Rauschboden und Nachbarkorrelation, einzelne Bloecke und gemittelte AP
nb = 3000
xs = rng.standard_normal((nb, N))
res = {}
for nm, w in [("rect", w_r), ("hann", w_h)]:
    X = 2/np.sum(w)*np.fft.rfft(w*xs, axis=1)[:, 5:1500]
    ap = np.mean(np.abs(X)**2, axis=0)
    res[nm] = (ap.mean(), X)
    c_cplx = np.mean(X[:, :-1]*np.conj(X[:, 1:]))/np.mean(np.abs(X)**2)
    p = np.abs(X)**2
    pc = np.corrcoef(p[:, :-1].ravel(), p[:, 1:].ravel())[0, 1]
    print("S1f", nm, "Rauschboden AP-Mittel", res[nm][0], " lag1 komplex", c_cplx, " lag1 Leistung", pc)
print("S1g Verhaeltnis AP hann/rect:", res['hann'][0]/res['rect'][0])
# Korrelation der blockgemittelten AP (n=7) benachbarter Linien (Statistik wie in der Datei)
for nm in ("rect", "hann"):
    X = res[nm][1]
    nblk = 7
    m = (X.shape[0]//nblk)*nblk
    ap7 = np.mean(np.abs(X[:m]).reshape(-1, nblk, X.shape[1])**2, axis=1)
    print("S1h", nm, "lag1-Korrelation AP(n=7)", np.corrcoef(ap7[:, :-1].ravel(), ap7[:, 1:].ravel())[0, 1])
# Fenster-Korrelation analytisch: rho1 = sum w^2 e^{-i 2pi n/N} / sum w^2
rho1 = np.sum(w_h**2*np.exp(-2j*np.pi*n/N))/np.sum(w_h**2)
print("S1i rho1 Hann analytisch:", rho1, " |rho|^2 =", abs(rho1)**2)

# ---- S2: Hann-Glaettung der FRF bei stationaer-zufaelliger Anregung ----------
print("S2 H1_A[k] = 2/3 H_k + 1/6 (H_k-1 + H_k+1)")
f0, zeta, dff = 160.6, 1.435e-3, 0.625
def H(f):  # Weg/Kraft normiert, e^{+i w t}: 1/(1-r^2+2 i zeta r)
    r = f/f0
    return 1/(1-r**2+2j*zeta*r)
for off in (0.0, 0.5):
    k0 = round(f0/dff)
    fk = (k0+off+np.arange(-1, 2))*dff
    f_center = fk[1]
    # Peak ueber Linien: Raster so legen, dass eine Linie bei f0+offset*df*? -> Linienraster verschieben
    fr = f0 + (off-0.5+0.5)*0  # dummy
for shift in (0.0, 0.25, 0.5):
    fl = f0 + (np.arange(-3, 4)+shift)*dff
    Hl = H(fl)
    HA = (2/3)*Hl[1:-1] + (1/6)*(Hl[:-2]+Hl[2:])
    print("   Linienraster um f0 verschoben um %.2f df: max|H_rect|=%.4g  max|H1_A|=%.4g  Verhaeltnis %.3f"%(shift, np.abs(Hl).max(), np.abs(HA).max(), np.abs(HA).max()/np.abs(Hl).max()))

# ---- S3: Betragsmittelung vs komplexe Mittelung ------------------------------
def mc(gamma2, nd, trials=40000):
    # R: komplexer Gauss (|R| schwankt) ; V = H R + Nv ; gamma2 = |H|^2 Sr/(|H|^2 Sr+Sn)
    Hh = 1.0
    Sr = 1.0
    Sn = (1-gamma2)/gamma2*Sr   # |H|=1
    # |R| nahezu konstant wie in der Beispieldatei (AP/ABS^2 = 1.00001, cv ~ 0.3 %), Phase zufaellig
    R = (1+0.003*rng.standard_normal((trials, nd)))*np.exp(1j*rng.uniform(0, 2*np.pi, (trials, nd)))
    Nv = (rng.standard_normal((trials, nd))+1j*rng.standard_normal((trials, nd)))*np.sqrt(Sn/2)
    V = Hh*R + Nv
    cp = np.mean(V*np.conj(R), axis=1); apr = np.mean(np.abs(R)**2, axis=1)
    cph_c = np.abs(cp)/np.sqrt(apr)             # komplex: |CPH| = |CP|/sqrt(AP_R)
    cph_m = np.mean(np.abs(V), axis=1)          # Betrag: <|V|>
    return np.median(cph_m/cph_c), np.mean(cph_m)/np.mean(cph_c)
print("S3 Verhaeltnis |CPH_Betrag|/|CPH_komplex| (Median ueber Linien), |R| konstant, nd=7 / 10")
for g2 in (0.9999, 0.99, 0.9, 0.7, 0.5, 0.3, 0.1, 0.01):
    a = mc(g2, 7); b = mc(g2, 10)
    print("   gamma2=%.4f  nd=7: %.4f  nd=10: %.4f"%(g2, a[0], b[0]))
# Rauschboden: komplex ~ 1/sqrt(nd), Betrag ~ konstant
for nd in (7, 10):
    Nn = (rng.standard_normal((40000, nd))+1j*rng.standard_normal((40000, nd)))/np.sqrt(2)
    print("S3b nd=%d: E|<N>| / E<|N|> = %.4f ; 1/sqrt(nd)=%.4f ; in dB %.2f"%(nd, np.mean(np.abs(Nn.mean(1)))/np.mean(np.abs(Nn).mean(1)), 1/np.sqrt(nd), -20*np.log10(np.sqrt(nd))))

# ---- S4: Zufallsfehler H1 fuer nd = 7, 10 ---------------------------------------
eps = lambda g2, nd: np.sqrt(1-g2)/(np.sqrt(g2)*np.sqrt(2*nd))
for g2 in (0.9, 0.99, 0.999):
    print("S4 eps|H1| g2=%.3f nd=7 %.4f nd=10 %.4f"%(g2, eps(g2, 7), eps(g2, 10)))
print("S4b nd-Verhaeltnis sqrt(7/10)=", np.sqrt(0.7))
print("S4c Phasenstreuung deg gamma2=0.98 nd=7:", np.degrees(eps(0.98, 7)))
print("S4d E[gamma2_hat] bei gamma2=0: 1/nd =", 1/7, 1/10, " 95%%-Quantil 1-0.05^(1/(nd-1)): %.3f %.3f"%(1-0.05**(1/6), 1-0.05**(1/9)))

# ---- S5: Nachrechnung Zahlen aus D1/D2/D3 ------------------------------------
for fq, z in ((160.6, 1.435e-3), (247.7, 1.387e-3)):
    tau = 1/(z*2*np.pi*fq); print("S5a f=%.1f tau=%.3f s, Rest nach 1.6 s: %.3f"%(fq, tau, np.exp(-1.6/tau)))
for fq in (100, 500, 1000):
    print("S5b f=%d: 1/w=%.4g ms; Delay Vib %.1f deg; Vib-Ref1 %.1f deg"%(fq, 1e3/(2*np.pi*fq), 360*fq*1.3336e-3, 360*fq*(1.3336-0.13076)*1e-3))
print("S5c 5 deg bei 1 kHz: tau=%.2f us ; 50 Hz Vib-Delay: %.1f deg"%(5/360/1000*1e6, 360*50*1.3336e-3))
print("S5d cos theta:", [round(np.cos(np.radians(a)), 4) for a in (5, 10, 15)])
print("S5e Scan: 135 Punkte in 40 min -> %.1f s/Punkt; 9 Punkte %.1f min; Count 10/7 skaliert: %.1f min; Worst (25 Bloecke x 1.6 s x 9): %.1f min"%(2400/135, 9*2400/135/60, 9*2400/135/60*10/7, 9*25*1.6/60))
print("S5f TDD-Groesse 3x3: 16 kB*25*5 Kanaele*9 = %.1f MB ; 8 Kanaele %.1f MB"%(16e3*25*5*9/1e6, 16e3*25*8*9/1e6))
print("S5g Ref1/AP-Verhaeltnis Kraft A-B: Betrag 2, AP 4")
# ---- S6: Parseval-Verhaeltnis fuer Ref1 (deterministisches Signal) ----------------
# Summe der Linienleistung A/R = 4*<w^2>_x ; gleichmaessig 1.5; Burst in Fenstermitte (Breite 0.2T) :
tt = np.arange(N)
for nm, wid in (("uniform", 1.0), ("Burst 50% mittig", 0.5), ("Burst 20% mittig", 0.2)):
    env = np.zeros(N); lo = int(N*(0.5-wid/2)); hi = int(N*(0.5+wid/2)); env[lo:hi] = 1
    print("S6", nm, "4*sum(w^2 x^2)/sum(x^2) =", 4*np.sum(w_h**2*env)/np.sum(env))

```
