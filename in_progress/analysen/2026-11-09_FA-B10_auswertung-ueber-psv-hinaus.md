<!-- Fachanalyse FA-B10 (Betreuervorgabe B10): Auswertungsverfahren über PSV hinaus; erstellt von strukturdynamik-experte, Stand 2026-11-09. Kein Code, keine Lastenheft-Änderung. -->

# FA-B10 – Auswertungsverfahren, die über PSV hinausgehen und sinnvoll sind

**Auftrag (B10, Laborbuch 2026-11-09_betreuertermin-daniel):** „Recherche, welche Auswertungsmöglichkeiten existieren, die anderes als PSV abbilden und sinnvoll sind.“
**Art:** Fachanalyse (Bewertung, keine Umsetzung). **Entscheidet nichts**; die Priorisierung in Abschnitt 4 ist eine Empfehlung.

## 0 Kennzeichnung und Grenzen dieser Recherche

| Kürzel | Bedeutung |
|---|---|
| **[H]** | Herstellerangabe (Polytec), Beleg über W1/I2 |
| **[D]** | Befund an `20261012_ref_Mitte.svd` oder Faktenliste 2026-11-02 |
| **[A]** | eigene Herleitung, im Text vollständig |
| **[N]** | numerisch nachgerechnet (Prüfskript im Anhang) |
| **[E]** | fachliche Einschätzung, nicht belegt |
| **[L-m]** | Literatur in `literatur.bib` mit Prüfstand `metadaten`: Inhalt nicht gelesen, also **kein Beleg** |
| **[R]** | Rechercheauftrag offen (Abschnitt 7) |

**Wichtig zur Belegbarkeit.** Es wurde **keine Fachliteratur gelesen und keine Webrecherche** gemacht; die Aufgabe ist eine fachliche Einordnung auf Basis der Projektunterlagen. Alle Literaturstellen der Bibliothek haben den Prüfstand `metadaten`. Autor-/Jahresangaben, die ich in Abschnitt 7 als Suchhinweise nenne, stammen aus dem Gedächtnis und sind **ungeprüft**. Sie dürfen nicht zitiert werden, bevor der `literatur-rechercheur` sie bestätigt hat.

**Annahmen (Auswirkung bei Fehlannahme):**

| Nr. | Annahme | Auswirkung, wenn falsch |
|---|---|---|
| AN1 | Prüfling ist wie bei der Beispieldatei ein frei hängendes Blech, Anregung an **einer** Stelle über Shaker mit Impedanzkopf (Ref1 = Kraft, Ref2 = Beschleunigung am Kraftangriffspunkt) [D]. | Bei mehreren Anregungsorten (MIMO) kämen weitere Verfahren in Betracht (V12). |
| AN2 | Eine Messdatei enthält gemittelte Spektren (AP, CP, ABS, CPH) je Punkt und Kanal, Geometrie und Punktstatus, **keine Zeitdaten und keine Einzelblöcke** (`SaveTimeDataForScan = False`) [D]. | V9 (Zeitdaten) wäre ohne neue Messung nicht möglich; mit gespeicherten Zeitdaten entfallen Einschränkungen von V3 und V10. |
| AN3 | Frequenzachse der Beispieldatei: Δf = 0,625 Hz, 1600 Linien, 0,625 … 1000 Hz, Blockdauer 1,6 s (bestätigt, K-ACHSE) [D]. Zahlen in W3 mit Δf = 1,5625 Hz sind überholt. | Linienzahlen je Halbwertsbreite ändern sich. |
| AN4 | Material und Dicke des Blechs sind **offen** (Versuchsplan 2026-11-09, V2/E1). Masse der Plattenseite grob 4,5 bis 6,7 kg [D, Fachprüfung, ±20 %]. | V3 (Masse), V4 und V11 hängen daran. |
| AN5 | Das Vorzeichen von Ref1/Ref2 ist ungeklärt (M8). P-08 liefert Re{Y} < 0 an der Beispieldatei [D, FG-02 §4]. | Verfahren, die eine absolute Kraft-Antwort-Phase brauchen (V3, V7 mit Skalierung), sind bis zur Klärung nicht belastbar. |
| AN6 | „Stand des Pakets“ = FG-02 (freigegeben), FG-03 (freigegeben), Code unter `software/src/ldv_automation/auswertung/` (P-01…P-11, `modenfit.py`, `vergleich.py`, `bezug3d.py`, `stufe2.py`). Die Umsetzung habe ich nicht abgenommen, nur die Modulliste gelesen. | Was ich als „vorhanden“ führe, ist nach FG-02/03 vorgesehen bzw. laut Nachverfolgung „getestet“. |
| AN7 | Der Projektrahmen schließt eine **vollständige Modalanalyse aus** (Exposé, R-054 „gestuft“, FG-03 E1(c)/E2(c)). | V7 ist deshalb nur als Brücke bzw. Ausblick bewertet. |

---

## 1 Ausgangslage: Was PSV und das Paket schon abdecken

Diese Zeilen dienen der Abgrenzung; sie werden hier nicht neu bewertet.

| Bereich | PSV (Hersteller) | Paket (FG-02/03, Stand laut Nachverfolgung) |
|---|---|---|
| Spektren, Mittelung, FRF/H1/H2/Kohärenz | ja [H] I2 4.1 | R-050, R-051; Spektrum |CPH| und √AP getrennt (A-2) |
| ODS-Animation, Flächen-/Pfeil-/Isolinienansicht | ja [H] | R-052; B7/B8/B9 als Vorgabe gesetzt |
| Band-RMS, Peak-Suche, SDOF-Peak-Fit (−3 dB, Q, ζ) | ja [H] HB 9-11 | R-053; zusätzlich komplexer Moden-Fit (B-1, FG-03 §3) |
| Harmonischer Cursor mit THD; gedämpfte Sinusanpassung im Zeitsignal | ja [H] SWP S.49–51 | – |
| MAC | nur als Beispielformel im Signalprozessor (SM 9-38) [H] | MAC-Funktion für Messung A gegen B (FG-03 §4.4) |
| Vergleich zweier Messungen | Koppeln/Animieren, kombinierte Datei [H] | B-5: Punktzuordnung, Spitzenpaarung, FRF-Vergleich, MAC, Drift (FG-03 §4); B4 gesetzt |
| Plausibilität | manuell | P-01…P-11 (FG-02 §4) |
| Zufallsfehler | nein | B-2 (FG-02 §3.4, Näherung erster Ordnung, [L-m]) |
| Signalprozessor (Formeln, Funktionen u. a. FFT, AP, CP, COH, H1, H2, Statistik) | ja [H] | – (eigener Code) |
| Modalanalyse (MDOF) | **nein**, Export an Fremdsoftware [H] SM 7-10 | ausgeschlossen (AN7) |
| Dehnungsverarbeitung | separates Produkt „Strain Processor“ installiert; Option „Strain“ lizenziert [D] Faktenliste A2/B1; Fähigkeiten nicht in den Unterlagen | – |
| Zeitdaten | Option TDD lizenziert [D]; in der Datei nicht gespeichert | R-056 (Kann), offen |
| Lastenheft | | R-054 (gestuft), R-056, R-057 (Masse aus Massenlinie, Kann), R-055 (Methode und Bandgrenzen bei jedem ζ) |

**Vorbehalt zur Abgrenzung [E]:** Der Signalprozessor von PSV ist ein Tabellenwerkzeug mit Statistik- und Spektralfunktionen. Mehrere der unten genannten Größen ließen sich dort von Hand als Formel bauen. „Anders als PSV“ heißt deshalb in dieser Analyse: nicht als fertige Auswertung vorhanden und nicht reproduzierbar automatisierbar, nicht „in PSV prinzipiell unmöglich“. Das ist für die Thesis richtig zu formulieren.

---

## 2 Übersicht der Verfahren

| Nr. | Verfahren | Fachlich zutreffend? | Aufwand | Daten in `.svd`? | Empfehlung |
|---|---|---|---|---|---|
| V1 | Messreihen-Statistik, Wiederholbarkeit, Vorher/Nachher-Prüfung | ja | klein bis mittel | ja, **aus mehreren Dateien** | **Rang 1** |
| V2 | Linearitätsprüfung (Zwei-Pegel, Frequenzverschiebung, Kohärenz) | ja | klein (auf V1 aufbauend) | ja, zwei Messungen | **Rang 1** (zusammen mit V1) |
| V3 | Energie- und Leistungsgrößen: kinetische Energie, eingeleitete Wirkleistung, Verlustfaktor aus Leistungsbilanz, abgestrahlte Ersatzleistung | ja, bedingt | mittel | ja (+ Masse extern) | **Rang 2** |
| V4 | Starrkörperanalyse (6-FHG-Fit) und Lagerungsgüte, Masse | ja | klein bis mittel | ja (Geometrie + 3D-Phase) | **Rang 3** (Paket) |
| V5 | Erweiterte Qualitätsmaße: Phasenkollinearität, Ausreißerpunkte, Modenüberlappung | ja | klein | ja | **Rang 3** (Paket) |
| V6 | Test-Analyse-Korrelation (FE-Abgleich): MAC, Frequenzabweichung, Kreuzorthogonalität | ja, **wenn FE-Daten vorliegen** | mittel bis groß | Messseite ja, FE-Seite nein | Rang 4 (bedingt) |
| V7 | MDOF-Modalparameter-Identifikation (LSCF/PolyMAX, Stabilisierungsdiagramm, Skalierung) | ja, aber ausgeschlossen | groß (Eigenbau), mittel (Fremdbibliothek als Gegenprobe) | ja (H1 aller Punkte, eine Referenz) | Rang 5 (nur als Brücke) |
| V8 | Modenindikatorfunktionen (CMIF/Summenfunktion) | ja, aber schon abgedeckt | – | ja | keine eigene Umsetzung |
| V9 | Zeitdatenbasierte Verfahren (eigene Spektren/H1, Blockstatistik, Impulsantwort, Zeitbereichs-Identifikation) | ja, bedingt | mittel bis groß | **nein** (nur bei gespeicherten Zeitdaten) | nicht jetzt |
| V10 | Messunsicherheit über B-2 hinaus (GUM-Budget, Geometrie-Fehlerfortpflanzung) | ja | mittel | teilweise | nicht jetzt |
| V11 | Ortsfrequenz-/Wellenzahlanalyse, inverse Materialkennwerte, Dehnung | ja, bedingt | groß | ja, Raster grob | nicht jetzt |
| V12 | Nicht zutreffend: OMA, MIMO-/Multireferenz-Verfahren, Hammer-/Reziprozitätsauswertung aus einer Datei, Transferpfadanalyse | nein (AN1) | – | – | ausgeschlossen |

---

## 3 Steckbriefe

### V1 Messreihen-Statistik, Wiederholbarkeit und Vorher/Nachher-Prüfung

- **Zweck.** Aus mehreren Messungen derselben Struktur statistische Kennwerte bilden (Mittel und Streuung von Spitzenfrequenz $f_r$, $\zeta$, Spitzenhöhe, MAC über Wiederholungen) und Messungen vor/nach einem Ereignis (Test, Umbau, Last) gegen Kriterien prüfen.
- **Nutzen für die Strukturtests.** Wiederholbarkeit ist Kernaussage jedes Tests (I2 P9); das Projektziel „unbeaufsichtigte Messreihen“ (R-010) erzeugt genau diese Datenlage. Vorher/Nachher-Vergleich von Resonanzfrequenzen ist in der Raumfahrtprüfung üblich (Resonanzsuche vor und nach einer Belastung) [E, **nicht belegt**; Quellenprüfung ECSS-Dokumente, [R-3]]. Die Schwellen sind Sache der Prüfvorschrift und werden vom Nutzer gesetzt.
- **Daten.** Mehrere `.svd` mit gleicher Geometrie und gleichen Einstellungen. Die Beispieldatei allein reicht nicht; B-5 ist bisher nur synthetisch getestet [D] (Nachverfolgung R-054).
- **Aufwand.** Klein bis mittel. B-5 (Punktzuordnung, Spitzenpaarung, MAC, Drift, `vergleich.py`) liefert die Bausteine; neu sind Aggregation über $n \ge 3$ Messungen, Kennwerte der Streuung und ein Pass/Fail gegen vom Nutzer gesetzte Toleranzen.
- **Abgrenzung zu PSV.** PSV kann zwei Dateien koppeln und animieren, aber keine Statistik über eine Messreihe und kein reproduzierbares Pass/Fail [H] W1 1.2 (Koppeln/kombinierte Datei).
- **Abgrenzung zu den Vorgaben.** B4 („Messungen vergleichen, Auswertungen nebeneinanderlegen“) ist die **Darstellung** des Vergleichs. V1 ist die **Kennwertbildung** über mehr als zwei Messungen und die Entscheidungsgröße. Beide teilen sich B-5.
- **Bezug.** R-054, R-010 (liefert die Daten), R-055 (jede Streuung von ζ trägt Methode und Bandgrenzen).
- **Gültigkeit.** Gleiche Frequenzachse (FG-03 §4: keine Interpolation), gleiche Punkte; bekannte systematische Drift von etwa $10^{-4}$ relativ über 40 min Scandauer in $f_r$ [D W3 2.7] gehört in die Streuung hinein, nicht heraus gerechnet. Die Aussagekraft hängt von $B/\Delta f$ ab: bei $\Delta f = 0{,}625$ Hz hat eine Spitze mit $f = 100$ Hz, $\zeta = 0{,}005$ nur 1,6 Linien in der Halbwertsbreite, bei 300 Hz und $\zeta = 0{,}004$ 3,8 Linien [N]. Deshalb Streuung von $\zeta$ stets mit dem Kennzeichen `aufloesungsbegrenzt` ausgeben.
- **Quellenbedarf.** Prüfkriterien Vorher/Nachher [R-3]; Statistik selbst ist elementar (Mittelwert, Standardabweichung, Stichprobe $n$).

### V2 Linearitätsprüfung

- **Zweck.** Prüfen, ob die Struktur im Messbereich linear antwortet. Alle Verfahren (FRF, Modalparameter, ζ) setzen Linearität voraus (FG-03 §3.6).
- **Nutzen.** Eine nichtlineare Struktur (Lager, Fügestellen, Seilaufhängung) liefert pegelabhängige Resonanzen und Dämpfungen. Bei frei hängenden Blechen ist das für die Aufhängung relevant [E]. Die Prüfung steht bereits auf dem Prüfzettel („Zwei-Amplituden-Test 0,02/0,04 V an Label 132“, Faktenliste 2a-4) und ist in I2 5.2 als P10 gelistet (Vergleich zweier Anregungsstufen, TM S.41 [H]).
- **Kennwerte (Vorschlag, [A]).**
  - Relative FRF-Abweichung je Linie $\delta_k = \lvert H_k^{(2)} - H_k^{(1)}\rvert / \lvert H_k^{(1)}\rvert$ gegen die Zufallsunsicherheit beider Messungen;
  - relative Verschiebung der Spitzenfrequenz $(f_r^{(2)} - f_r^{(1)})/f_r^{(1)}$ aus dem Moden-Fit (B-1) mit Standardabweichung $\sigma_{f_r}$;
  - Änderung von $\zeta$ zwischen den Pegeln (mit Methode und Band nach R-055);
  - Kohärenzverlauf (nur Hinweis).
- **Nachweisgrenze [N].** Mit der Näherung aus FG-02 §3.4 ($\varepsilon[\lvert H_1\rvert] \approx \sqrt{1-\gamma^2}/(\gamma\sqrt{2 n_d})$, [L-m], eigene Monte-Carlo-Prüfung dort: bei $n_d = 7$ Unterschätzung bis 8 %) liegt die Streuung der **Differenz** zweier Messungen bei $\gamma^2 = 0{,}99$ und $n_d = 7$ bei etwa 3,8 % (1σ); bei $\gamma^2 = 0{,}9$ bei etwa 12,6 %. Pegelabhängigkeiten von |H| unter etwa 8 % sind je Linie nicht nachweisbar. Die Spitzenfrequenz ist die empfindlichere Größe, weil sie den Fit über viele Linien nutzt.
- **Daten.** Zwei Messungen mit unterschiedlicher Generatoramplitude, sonst gleich. Die maximale Generator-Amplitude (0,04 V) ist offen (Laborbuch 2026-11-09). Ohne zwei Pegel nur Kohärenz als schwacher Hinweis; die Kohärenz zeigt systematische Fehler und deterministische Nichtlinearität nicht zuverlässig (W3 Kernaussage 4).
- **Aufwand.** Klein, wenn V1/B-5 vorliegt: es ist ein Sonderfall des Vergleichs mit eigener Interpretation (Pegel statt Wiederholung).
- **Abgrenzung zu PSV.** PSV hat den harmonischen Cursor mit THD für sinusförmige Anregung [H]. Das erkennt Nichtlinearität am Obertonanteil, nicht am Pegelvergleich über alle Punkte und Moden. Beides ergänzt sich.
- **Bezug.** R-054; I2 P10.
- **Quellenbedarf.** Lehrbuchbeleg zu Linearitätstests und Interpretation (Ewins 2000 [L-m], Brandt 2011 [L-m]) [R-3b].

### V3 Energie- und Leistungsgrößen

Dies ist die einzige Gruppe, die eine **andere physikalische Größe** liefert als PSV (PSV zeigt Geschwindigkeit je Punkt, FRF und Band-RMS je Punkt).

- **Zweck und Größen** (Konvention nach KONVENTIONEN: einseitige Spitzenwerte $\hat v$, $e^{+i\omega t}$):
  1. Kinetische Energie je Linie: $E_\mathrm{kin}(f) = \tfrac14 \sum_i m_i\,\lvert\hat{\vec v}_i\rvert^2$ in J. Herleitung: $\overline{\tfrac12 m v^2(t)} = \tfrac14 m \lvert\hat v\rvert^2$ [N]. Die Massen $m_i = (m_\mathrm{ges}/A)\,\Delta A_i$ folgen aus Geometrie (Flächenanteile) und Gesamtmasse bei gleichmäßiger Massenbelegung [A].
  2. Eingeleitete Wirkleistung am Kraftangriffspunkt: $\bar P_\mathrm{ein}(f) = \tfrac12\,\mathrm{Re}\{\hat F^{*}\hat v_p\} = \tfrac12 \lvert\hat F\rvert^2\,\mathrm{Re}\{Y\}$ in W, mit $Y = H_{\mathrm{Ref2/Ref1}}/(i\omega)$ (FG-02 §4, P-08; W3 2.3 [A]).
  3. Verlustfaktor aus der Leistungsbilanz im Band: $\eta = \dfrac{\bar P_\mathrm{ein}}{\omega\,E_\mathrm{ges}}$ mit $E_\mathrm{ges} \approx 2E_\mathrm{kin}$ (Gleichverteilung von kinetischer und potentieller Energie im Band-Mittel), also
  $$\eta(f) = \frac{\lvert\hat F\rvert^2\,\mathrm{Re}\{Y\}}{\omega\,m\,\langle\lvert\hat v\rvert^2\rangle_A},\qquad \eta = 2\zeta \text{ für einen Einmassenschwinger}.$$
  4. Abgestrahlte Ersatzleistung (optional): $P_\mathrm{ERP} = \rho_0 c_0\,\sigma\,\tfrac12 \sum_i \lvert\hat v_{n,i}\rvert^2\,\Delta A_i$ mit Normalgeschwindigkeit $\hat v_n$ (B6/B-8 liefert die Normale), $\rho_0 c_0 \approx 413\ \mathrm{kg/(m^2 s)}$ bei 20 °C [N] und $\sigma \le 1$ (hier $\sigma = 1$: **obere Schranke**).
- **Nachrechnung [N].** (a) Einmassenschwinger ($m = 5$ kg, $f_n = 300$ Hz, $\zeta = 0{,}004$): $\eta = 0{,}008 = 2\zeta$ exakt. (b) Kette mit 40 Massen, modale Dämpfung $\zeta = 0{,}004$, Kraft an einem Freiheitsgrad, alle Freiheitsgrade „gemessen“: über ein Band mit vielen Moden $\eta_\mathrm{Band} = 0{,}00799$ (−0,13 % gegen $2\zeta$); in einem schmalen Band mit 3 Moden −1,1 %; linienweise 0,0074 bis 0,0082. Die Formel ist also im Ideal bandweise sehr genau und linienweise nur etwa ±7 %. **Das ist ein Idealfall** (vollständige räumliche Abtastung, rauschfrei, richtiges Vorzeichen).
- **Nutzen für die Strukturtests.** (i) Dämpfung, die **nicht** von der Linienauflösung und vom Peak-Fit abhängt (PSV-Fit und B-1 sind bei 1–4 Linien je Halbwertsbreite stark auflösungsbegrenzt, siehe V1); (ii) bandgemittelte Dämpfung bei dicht liegenden Moden, wo Einzelmodenverfahren versagen; (iii) Energieverteilung und Schwingungsniveau je Band als Kennwert für Vergleich zwischen Aufbauten; (iv) unabhängige Probe von Kraft/Geschwindigkeit/Masse (Konsistenz zu R-057); (v) ERP als obere Abschätzung der Schallabstrahlung, falls der Betreuer akustische Fragestellungen hat.
- **Daten.** Ref1/Ref2-Spektren, 3D-Spektren aller Punkte, Geometrie [D]. **Masse extern** (Wiegen; Versuchsplan E1). Punktstatus für Maske.
- **Voraussetzungen und Fehlerquellen.**
  - Vorzeichen: $\mathrm{Re}\{Y\} \ge 0$ muss gelten (P-08). Die Beispieldatei verletzt das [D]; **dies wirkt hier direkt auf das Ergebnis** (negatives η). Die Methode ist deshalb auch ein zusätzlicher physikalischer Test des Vorzeichens (M8), aber nur ein Hinweis, kein Beleg für die Ursache.
  - Räumliche Abdeckung: Das Raster 9 × 15 mit 0,029 m Abstand deckt 0,232 × 0,406 m ab [D FG-03]. Ob das die ganze Platte ist, ist **offen** (AN4); nicht gemessene Bereiche und angekoppelte Massen (Impedanzkopf, Stinger) gehen nicht in $\langle\lvert\hat v\rvert^2\rangle$ ein und verfälschen $\eta$ systematisch.
  - Rauschen: Für $\langle\lvert\hat v\rvert^2\rangle$ den kohärenten Anteil (|CPH|², FG-02 A-2) verwenden, sonst geht Rauschleistung ein.
  - Gleichverteilung der Energie ist eine Näherung, gut im Band-Mittel über mehrere Moden, schlecht an einer einzelnen Mode mit stark lokalisierter Form (potentielle und kinetische Energie sind nur im Zeitmittel gleich; über Orte nicht) [A].
  - ERP: Eine Platte von 0,23 × 0,41 m ist bei 1 kHz klein gegen die Schallwellenlänge (0,34 m bei 343 m/s, [A]); der akustische Kurzschluss senkt die tatsächliche Abstrahlung stark, ERP ist dort eine deutliche Überschätzung [E].
- **Aufwand.** Mittel. Die Rechnungen selbst sind einfach (Summen über Punkte); aufwendig sind Massenverteilung, Flächengewichte, Maskenregeln, Bandgrenzen und Kennzeichen sowie Referenzfälle.
- **Abgrenzung zu PSV.** PSV liefert den Band-RMS **je Punkt** und optional Effektivwerte; kein Energie-, Leistungs- oder Verlustfaktor-Ergebnis. Der Signalprozessor könnte es nachbauen [E, Vorbehalt Abschnitt 1].
- **Bezug.** R-055 (neue Methode „Leistungsbilanz“ mit Bandgrenzen), R-053 (Band-RMS), R-057 (Masse), R-052 (3D, Normale), B-9 (quadratisches Punktmittel, flächengewichtet: FG-03 nennt es „nicht enthalten“).
- **Quellenbedarf.** Power-Injection-Methode und Energiegleichverteilung [R-1]; Abstrahlgrad und ERP [R-2].

### V4 Starrkörperanalyse und Lagerungsgüte

- **Zweck.** Die gemessene 3D-Geschwindigkeit je Linie in den Anteil einer Starrkörperbewegung (Translation $\vec v_0$, Rotation $\vec\omega$) und einen elastischen Rest zerlegen:
  $$\hat{\vec v}_i = \hat{\vec v}_0 + \hat{\vec\omega}\times\vec r_i + \hat{\vec v}^\mathrm{el}_i,$$
  komplexe Kleinste-Quadrate-Anpassung mit 6 Unbekannten je Linie aus $3P$ Gleichungen. Kennzahl: Starrkörperanteil $\rho_\mathrm{rb}(f) = \lVert A\hat q\rVert^2/\lVert\hat v\rVert^2$.
- **Nachrechnung [N].** Für exakte Starrkörperbewegung ($P = 60$ Punkte, zufällige komplexe $\vec v_0,\vec\omega$) werden $\vec v_0,\vec\omega$ auf $2\cdot10^{-15}$ wiedergefunden, und für addierten, zum Starrkörperraum orthogonalen elastischen Anteil entspricht das Residuum genau dessen Norm.
- **Nutzen.** (i) Die Aufhängungsmoden eines frei hängenden Blechs sind Starrkörpermoden mit niedriger Frequenz. Ihr Abstand zur ersten elastischen Mode kennzeichnet die Güte der Lagerung (Frei-frei-Näherung). Das führt I2 5.2 (P17, Niederfrequenz-Check) nur als Spektrum-Hinweis. (ii) Schätzung der Masse aus Gesamtbewegung statt Einzelpunkt: unterhalb der ersten Elastikmode gilt $\lvert\hat F\rvert \approx m\,\omega\lvert\hat v_{0,n}\rvert$ für die Komponente in Kraftrichtung, falls $\vec v_0$ der Schwerpunkt ist [A]. Das stützt R-057 (dort aus Ref2/Ref1). (iii) Der elastische Rest ist die für Modenvergleiche (V6, MAC) richtige Form.
- **Daten.** Punktkoordinaten und komplexe 3D-Komponenten relativ zu Ref1 [D]. Phase muss gültig sein (Referenz vorhanden, `PhaseFromRef True` [D]). **Unabhängig vom Vorzeichen von Ref1**: ein globaler Faktor −1 ändert die Anpassung nicht (daher von M8 unberührt).
- **Aufwand.** Klein bis mittel.
- **Abgrenzung zu PSV.** PSV animiert die Bewegung, trennt aber nicht in Starrkörper und Elastik [E, in den Unterlagen kein Hinweis].
- **Abgrenzung zu den Vorgaben.** B6 transformiert das Koordinatensystem auf die Flächennormale; V4 braucht diese Transformation nicht, nutzt aber dieselbe Geometrie. B-8 trennt Normal- und Tangentialanteil je Punkt, V4 Starrkörper- und Elastikanteil über alle Punkte.
- **Gültigkeit.** Geometrie klein gegen die Wellenlänge ist **nicht** nötig; wohl aber ein Raster, das alle sechs Freiheitsgrade bestimmt (nicht alle Punkte auf einer Linie, nicht alle in einer Ebene bei reiner Z-Messung; bei ebener Platte sind Translation in der Ebene und Rotation um die Plattennormale nur mit 3D-Messung bestimmbar).
- **Quellenbedarf.** Starrkörperkinematik ist Lehrbuchstoff; ein Lagerungskriterium (zulässiges Frequenzverhältnis Aufhängung/Elastik) muss belegt werden [R-4].

### V5 Erweiterte Qualitätsmaße

Ergänzung zu P-01…P-11. Alle drei sind aus den vorhandenen Daten berechenbar.

- **a) Phasenkollinearität $\kappa_\varphi$ einer Schwingform.** Für $\vec\phi = \vec a + i\vec b$ ist
  $$\kappa_\varphi = \frac{\lambda_{\max}\!\begin{pmatrix}\vec a\cdot\vec a & \vec a\cdot\vec b\\ \vec a\cdot\vec b & \vec b\cdot\vec b\end{pmatrix}}{\vec a\cdot\vec a+\vec b\cdot\vec b}\in[0{,}5,\ 1].$$
  Sie ist das größte Anteilsverhältnis, das eine reelle Form $\mathrm{Re}\{e^{-i\theta}\vec\phi\}$ über die Drehung $\theta$ erreicht. Gleichung [A], numerisch gegen Brute-Force geprüft: 1,0 für reelle Form mal $e^{i0{,}7}$, 0,5 für kreisförmige Form, 0,8575 gegenüber 0,8575 bei gemischtem Fall [N]. **Eigene Definition, nicht die Literaturdefinition** (MPC); die Lit.-Form ist per Recherche zu prüfen [R-7].
  *Nutzen:* Bei schwach gedämpfter, getrennt liegender Mode ist die Schwingform nahezu reell; eine geringe Kollinearität zeigt Nachbarmoden, Zeit-/Laufzeitfehler, falsche Phase oder Aufbauprobleme. Ergänzt P-07 (Phasensinn).
- **b) Ausreißerpunkte (Dropouts, Speckle).** Abweichung der komplexen Amplitude eines Punkts von der robusten Schätzung aus den Nachbarpunkten, normiert mit der lokalen Amplitude (damit Knotenpunkte nicht fälschlich auffallen). Ergänzt P-10, das nur die PSV-Statuszählung auswertet. [E] Erkennungsgrenze hängt vom Verhältnis Rasterabstand zu Wellenlänge ab (Material/Dicke offen, AN4); wo das Raster die Form nicht abbildet, entstehen Fehlalarme.
- **c) Modenüberlappung.** Ein einfacher Hinweis ist das Produkt aus mittlerer Halbwertsbreite $B$ und der Spitzendichte (Spitzen je Hz) im Band; bei hohem Wert ist die Einzelmodenannahme (−3 dB, B-1 mit $n=1$) unzulässig, B-1 benötigt dann die Gruppenbildung (FG-03 §3.3). [E] mit Quellen [R-5].
- **Aufwand.** Klein je Maß. **Abgrenzung zu PSV:** keine Entsprechung [E]. **Bezug:** R-054, P-07/P-10.
- **Zur Reziprozität.** Eine Prüfung nach Maxwell ($H_{ij} = H_{ji}$) braucht zwei Messungen mit vertauschten Anregungs- und Messorten. Aus einer Datei nicht möglich; höchstens als Versuchsvariante (V12), niedrige Priorität.

### V6 Test-Analyse-Korrelation (Abgleich mit einem FE-Modell)

- **Zweck.** Gemessene Eigenfrequenzen und Schwingformen mit einem Rechenmodell vergleichen: relative Frequenzabweichung $(f_\mathrm{FE}-f_\mathrm{mess})/f_\mathrm{mess}$, MAC-Matrix Messung × FE, optional Kreuzorthogonalität (mit reduzierter Massenmatrix).
- **Nutzen.** Genau dafür werden Modal- und Standschwingungsversuche in der Luft- und Raumfahrt durchgeführt (Modellvalidierung); die Bibliothek enthält dazu Quellen als Metadaten (`goege2007gvt`, `ecss2012testing`, `ecss2022testing`, `allemang2003mac`) [L-m]. Die Inhalte (z. B. übliche Abnahmekriterien) sind **nicht gelesen**; jede Zahlenangabe zu „guter Korrelation“ wäre unbelegt.
- **Daten.** Messseite: Spitzen und ODS aus `.svd`. **FE-Seite: nicht vorhanden, nicht in `.svd`.** Es braucht ein Modell, Knoten-Koordinaten, Modenvektoren (z. B. UFF/CSV) und die Zuordnung Messpunkt ↔ Knoten im selben Koordinatensystem (Passpunkte; Verwandtschaft zu B6).
- **Näherung.** Die ODS an einer isolierten Spitze ist näherungsweise die Eigenform, wenn die Mode getrennt liegt und schwach gedämpft ist [A, nicht quantifiziert]; die Güte zeigt $\kappa_\varphi$ (V5a). Bei dicht liegenden Moden ist der Vergleich ohne MDOF-Identifikation (V7) nicht belastbar.
- **Aufwand.** MAC und Frequenzabweichung mit importierten Vektoren: mittel (MAC existiert, FG-03 §4.4; neu sind Import, Zuordnung, Darstellung). Kreuzorthogonalität und Modellanpassung: groß.
- **Abgrenzung zu PSV.** PSV vergleicht nicht mit externen Modellen; PSV-Geometrieimport (Option ImpGeo lizenziert [D]) dient der Messgeometrie.
- **Abgrenzung zu den Vorgaben.** B4 ist Messung gegen Messung; V6 ist Messung gegen Modell mit demselben MAC.
- **Bezug.** R-054. **Blockierend vor jeder Planung:** Gibt es für den Prüfling oder ähnliche Prüflinge ein FE-Modell am Institut, und in welchem Austauschformat? (Frage an Betreuer, Abschnitt 8.)
- **Quellenbedarf.** [R-5] (MAC im Volltext, Kreuzorthogonalität, Korrelationspraxis).

### V7 MDOF-Modalparameter-Identifikation

- **Zweck.** Aus H1 aller Punkte und Komponenten globale Pole (Frequenz, Dämpfung), Schwingformen und Teilnahmefaktoren identifizieren (z. B. rationale Matrixbruchfunktion im Frequenzbereich, LSCF/PolyMAX), mit Stabilisierungsdiagramm zur Ordnungswahl und Synthese der FRF zur Gütekontrolle.
- **Nutzen.** Eine konsistente Menge von Polen über alle 135 Punkte (statt je Punkt ein Fit), saubere Trennung eng liegender Moden und Modalmassen (Skalierung über den Antriebspunkt Ref2/Ref1) für den Vergleich mit FE.
- **Daten.** vorhanden: H1 je Punkt/Komponente, **eine** Referenz (Einzelreferenz, „SIMO“). Das vereinfacht die Identifikation, weil keine Multireferenzmatrix nötig ist. Die Skalierung nutzt den Antriebspunkt (Ref2/Ref1) und hängt am Vorzeichen (M8, AN5).
- **Abgrenzung zum Projektrahmen.** Das Exposé schließt eine vollständige Modalanalyse aus (AN7); FG-03 E1(c)/E2(c) haben LSCF und globalen Fit ausdrücklich ausgeklammert. Ein Eigenbau wäre ein eigenes Teilprojekt (Modellordnungswahl, Polauswahl, Validierung): **Aufwand groß**.
- **Brücke statt Eigenbau.** (i) UFF-58/ME'scope-Export (B-7, offene Konventionen, FG-02 §5, §12) erlaubt die Weitergabe an Fremdwerkzeuge; PSV exportiert selbst nach UFF/ME'scope [H]. (ii) Eine Python-Bibliothek (`sdypyema` ist in der Bibliothek nur als Software-Eintrag, `metadaten`) als **Gegenprobe** zu B-1 an der Beispieldatei: Aufwand mittel, Lizenz, Version und Zitierbarkeit sind erst zu klären [R-6]. Wichtig für die Thesis: Eine solche Gegenprobe prüft die B-1-Werte unabhängig und stützt die Aussage, wie belastbar ein auflösungsbegrenzter ζ ist.
- **Bezug.** R-054; FG-03 E1/E2.
- **Quellenbedarf.** [R-6].

### V8 Modenindikatorfunktionen

- **Befund [A, N].** Bei **einer** Referenz ist die Matrix der FRFs (Punkte × Referenzen) eine Spalte; ihr einziger Singulärwert ist die euklidische Norm der Spalte (numerisch geprüft: 29,7547 = 29,7547 [N]). Die komplexe Modenindikatorfunktion (CMIF) reduziert sich damit auf $\sqrt{\sum_i\lvert H_i\rvert^2}$, also auf das **quadratische Punktmittel** (B-9, FG-02 §3.2) ohne Flächengewichtung. Mehrfachreferenz-CMIF ist hier unmöglich (AN1).
- **Folgerung.** Keine eigene Umsetzung. Es genügt, im Spektrenvergleich das quadratische Mittel mit der Bezeichnung „Summenfunktion/Modenindikator (Einzelreferenz)“ anzubieten. Die Variante wird bei der Auswahl der Fitbänder (V7) und der Spitzenzahl nützlich.
- **Quelle.** Originalarbeit zu CMIF [R-6b].

### V9 Zeitdatenbasierte Verfahren

- **Mögliche Verfahren.** (a) Eigene Spektren und H1 aus Zeitdaten (R-056, Gegenprobe zu PSV); (b) **Blockstatistik**: aus Einzelblöcken die tatsächliche Streuung von H1 und Kohärenz bestimmen statt der Formel aus FG-02 §3.4; (c) Parseval-Test (I2 P12), Abklingprüfung bei Burst (I2 P7, Leckage), Fensterwechsel offline (z. B. Rechteck gegen Hann); (d) Impulsantwort aus Zeitdaten und Zeitbereichsidentifikation (z. B. Eigensystem-Realisierung) [E].
- **Daten.** Zeitdaten werden nur bei `SaveTimeDataForScan = True` gespeichert; die Beispieldatei hat sie **nicht** [D]. Option TDD ist lizenziert. Der Mini-Scan mit Zeitdaten steht auf dem Prüfzettel (2a-2); Dateigröße und Wirkung auf Signal Enhancement sind noch zu messen.
- **Nebenweg ohne Zeitdaten [A, [E]].** Die Impulsantwort lässt sich aus H1 über inverse FFT näherungsweise bilden; Linie 0 (DC) fehlt in der Datei, die Bandbegrenzung bei 1 kHz erzeugt Rückfalteffekte, die Fensterung wirkt als Verschmierung. Für Dämpfung ist das kein besseres Verfahren als der Frequenzbereichsfit; nicht empfohlen.
- **Aufwand.** Mittel (Leser, a und c) bis groß (b und d). R-056 ist „Kann“.
- **Abgrenzung zu PSV.** PSV rechnet die Spektren selbst, eine unabhängige Nachrechnung ist die Gegenprobe; Zeitdaten und TDD-Funktionen existieren in PSV ([H] gedämpfte Sinusanpassung).
- **Empfehlung.** Nicht jetzt; vorbereiten durch Entscheidung, ob bei künftigen Messungen Zeitdaten gespeichert werden (offene Frage 2026-11-09). Der **größte Zusatznutzen** (b) entsteht erst mit Einzelblöcken, die ich in der Dateistruktur nicht belegt habe [E].
- **Quellenbedarf.** Spektralschätzung: Welch, Harris, Bendat/Piersol, Brandt (alle `metadaten`) [R-8].

### V10 Messunsicherheit über B-2 hinaus

- **Stand.** B-2 deckt den Zufallsfehler von |H1|, Phase und γ² aus $n_d$ ab (FG-02 §3.4), mit dokumentierten Grenzen (keine systematischen Fehler).
- **Erweiterung.** (a) Wiederholbarkeit als empirische Unsicherheit (siehe V1: die belastbarste Aussage, weil sie alle Fehlerquellen enthält); (b) Beitrag der Sensorkalibrierung (Datenblatt PCB 288D01 offen, Faktenliste 2e); (c) Geometriefehler der 3D-Zerlegung: Für $\vec m = D\vec x$ (Strahlkomponenten $\vec m$, kartesische Komponenten $\vec x$) gilt $\lVert\delta\vec x\rVert/\lVert\vec x\rVert \le \kappa(D)\,\lVert\delta\vec m\rVert/\lVert\vec m\rVert$ [A, lineare Algebra]; $\kappa(D)$ ist laut I2 P4 zwischen 1 (symmetrisch, 54,7°) und 1,685 (40°) [H]; die Kopfpositionen sind in der Datei nicht dekodiert (E5/M13), also hier nicht direkt berechenbar.
- **Aufwand.** Mittel; (a) kostet nichts extra, wenn V1 vorliegt.
- **Abgrenzung zu PSV.** PSV gibt keine Unsicherheit an [H] W1.
- **Quellenbedarf.** GUM (`jcgm2008gum`, [L-m]) und Kalibrierung von Vibrometern (`iso2011laservibrometer`, [L-m]) [R-9].
- **Empfehlung.** (a) über V1 abdecken; (b), (c) erst, wenn Datenblatt/Kopfpositionen vorliegen.

### V11 Ortsfrequenz-/Wellenzahlanalyse, inverse Materialkennwerte, Dehnung

- **Zweck.** Aus dem räumlichen Verlauf der Schwingform (zweite Ortsableitung für Biegung) Biegewellenzahlen, Biegesteifigkeit/Elastizitätsmodul (inverse Identifikation), Wellendämpfung und Dehnungsverteilung bestimmen.
- **Grundformel [A].** Dünne Platte: $k_b = (\rho h\,\omega^2/D)^{1/4}$, $D = Eh^3/(12(1-\nu^2))$. Das Raster löst die Welle nur auf, wenn $\Delta x < \lambda_b/2$; also bis $f = \pi c/(2\Delta x^2)$ mit $c = \sqrt{D/(\rho h)}$. Wegen offenem Material und offener Dicke (AN4) **keine Zahl**.
- **Nutzen.** Dehnungen an kritischen Stellen sind für Strukturtests relevant (Vergleich mit Dehnungsmessstreifen) [E]. Die Ableitungsbildung verstärkt Rauschen und Lagefehler stark.
- **Abgrenzung zu PSV.** Polytec bietet mit dem Strain Processor ein eigenes Produkt (installiert, Option lizenziert, Fähigkeiten nicht in den Unterlagen) [D]; ein Eigenbau würde dies doppeln.
- **Aufwand.** Groß, Datenanforderung (feines Raster, Material, Dicke) nicht erfüllt.
- **Empfehlung.** Nicht jetzt. Im Stand-der-Technik-Kapitel als mögliche Erweiterung nennen.
- **Quellenbedarf.** [R-10].

### V12 Nicht zutreffende Verfahren

- **Operational Modal Analysis (OMA):** setzt unbekannte Breitbandanregung voraus; hier gibt es eine gemessene Kraft (Ref1) und eine kontrollierte Anregung.
- **Multireferenz-/MIMO-Verfahren, PCA, Multi-Input-Kohärenz:** ein Shaker, **keine PCA-Lizenz** [D], also eine Referenz.
- **Hammer-Auswertung (Kraft-/Exponentialfenster):** nicht der Versuchsaufbau.
- **Transferpfadanalyse, Substrukturierung:** kein gekoppeltes System.
- **Reziprozität** aus einer Datei: nicht möglich (V5).

---

## 4 Priorisierte Empfehlung (höchstens fünf)

Kriterien: Nutzen für Strukturtests am Institut; Datenlage (liegt es vor oder entsteht es im Projekt?); Aufwand; Quellenlage; Passung zum Projektschwerpunkt Automatisierung und Reproduzierbarkeit; echte Abgrenzung zu PSV. Die Reihenfolge ist **meine** Einschätzung [E]; ob und was umgesetzt wird, entscheidet der Nutzer mit dem Betreuer (Entscheidungspunkt R-054).

| Rang | Paket | Begründung |
|---|---|---|
| **1** | **V1 + V2: Messreihen-, Vorher/Nachher- und Linearitätsprüfung** | Höchster Nutzen pro Aufwand: baut auf B-5 auf (`vergleich.py`, `modenfit.py`), die Daten entstehen durch die Warteschlange (R-010) und die geplanten Versuche (Zwei-Pegel, Wiederholmessung) von selbst; es liefert die **empirische** Unsicherheit, die B-2 nicht kann, und zeigt, was die Automatisierung inhaltlich bringt (Wiederholbarkeit). Quellenlage gering (Statistik, Prüfkriterien aus ECSS zu belegen). |
| **2** | **V3: Energie, Leistung, Verlustfaktor (ERP optional)** | Einzige Gruppe mit einer **anderen physikalischen Größe** als PSV; Dämpfung unabhängig von Linienauflösung und Peak-Fit, wo B-1/PSV bei 1–4 Linien je Halbwertsbreite an Grenzen stoßen. Formeln sind klein und im Ideal auf 0,1–1 % nachgerechnet [N]. Bedingungen: Vorzeichen geklärt (M8), Masse gewogen, räumliche Abdeckung beurteilt. Ohne diese Bedingungen **zurückstellen**. |
| **3** | **V4 + V5: Starrkörper- und Qualitätsmaße** | Klein bis mittel, nur aus vorhandenen Daten, fachlich sauber herleitbar und prüfbar [N]; erhöhen die Belastbarkeit von R-052/R-053/R-057 (Lagerung, Ausreißer, Phasenqualität). Geringer Neuigkeitswert gegenüber PSV, aber hoher Nutzen für die Qualitätssicherung des Tests. |
| **4** | **V6: Test-Analyse-Korrelation** | Für die Luft- und Raumfahrt der naheliegendste Zweck des Versuchs, aber **bedingt** durch das Vorhandensein von FE-Daten. Zuerst nur Frequenzabweichung und MAC (Bausteine vorhanden); Import-Schnittstelle (UFF/CSV) als einziger neuer Teil. |
| **5** | **V7: Modalidentifikation als Brücke** (UFF-Export und Fremdbibliothek als Gegenprobe zu B-1; kein Eigenbau) | Beantwortet die naheliegende Frage des Betreuers nach Modalparametern, ohne den ausgeschlossenen Umfang zu öffnen. Aufwand mittel, Lizenz/Zitierbarkeit der Bibliothek offen. |

**Zurückgestellt, mit Grund:** V9 (Daten fehlen, R-056 „Kann“), V10 (b, c; Daten fehlen; (a) in V1 enthalten), V11 (Daten und Aufwand), V8 (schon abgedeckt, nur Benennung).

**Vorschlag zur Reihenfolge der Entscheidung [E]:** Zuerst Rang 1 (keine Abhängigkeit von offenen Fragen), parallel die Fragen aus Abschnitt 8 klären (FE-Modell, Zeitdaten, Material/Masse/Vorzeichen); Rang 2 und 3 danach; Rang 4 und 5 nur, wenn FE-Daten bzw. der Wunsch des Betreuers vorliegen.

---

## 5 Abgrenzung zu den gesetzten Vorgaben B4–B9

| Vorgabe | Inhalt | Verhältnis zu den Verfahren hier |
|---|---|---|
| B4 Messungen vergleichen, Auswertungen nebeneinanderlegen | Darstellung und Vergleich | V1/V2 nutzen B-5 und liefern Kennwerte und Entscheidungen; V6 vergleicht gegen Modell. Keine Doppelbewertung der Darstellung. |
| B5 Auswertungen plotten | Plotfunktion | Jede neue Größe (η, E, κ, δ) braucht eine Abbildungsform; keine Bewertung. |
| B6 KOS-Transformation (z. B. Normalrichtung) | Koordinaten | V3 (ERP) braucht die Normalkomponente, V4 nutzt die Geometrie, V6 braucht das Modell-KOS; B-8 deckt Normale/Tangente ab. |
| B7 Animation übernehmen | | V4 liefert eine zusätzliche Animationsform (nur elastischer Rest), sonst unabhängig. |
| B8 PSV-Visualisierung generell übernehmen | | unabhängig. |
| B9 Ausschnitte, Achsen | | unabhängig. |

---

## 6 Bezug zu vorhandenen Anforderungen (nur Hinweise, keine Änderung)

| Anforderung | Berührung |
|---|---|
| R-054 (gestuft) | Rahmen für V1, V2, V5, V6, V7; Entscheidungspunkt steht aus |
| R-055 | neue Dämpfungsmethoden (V3 „Leistungsbilanz“, V7) müssen Bandgrenzen und Methode tragen |
| R-056 (Kann) | V9 |
| R-057 (Kann) | V3 und V4 liefern eine unabhängige Masse |
| R-010, R-020 | Datenquelle für V1/V2 |
| R-052 | V4, V5a |
| R-053 | V3 (Alternative zu auflösungsbegrenztem ζ) |

---

## 7 Rechercheaufträge für den `literatur-rechercheur`

Die in Klammern genannten Autoren und Jahre sind **Suchhinweise aus dem Gedächtnis**, keine bestätigten Quellen.

| Nr. | Gegenstand | Gesucht | Nutzen für |
|---|---|---|---|
| R-1 | Leistungsbilanz-/Power-Injection-Methode für Verlustfaktoren; Energiegleichverteilung bei Bandmittelung (Suchhinweis: Bies/Hamid, J. Sound Vib., ca. 1980; Lyon/DeJong, Statistical Energy Analysis; Cremer/Heckl, Körperschall) | begutachtete Quelle oder Lehrbuch mit Gleichung und Gültigkeitsbedingungen | V3 |
| R-2 | Abgestrahlte Ersatzleistung (ERP), Abstrahlgrad ebener Platten, akustischer Kurzschluss (Suchhinweis: Fahy/Gardonio, Sound and Structural Vibration) | Definition, Gleichung, Gültigkeit für kleine Platten | V3 |
| R-3 | Prüfkriterien für Resonanzsuche vor/nach Belastung und Linearitätsprüfung in der Raumfahrt (Bibliothek: `ecss2012testing`, `ecss2022testing`, `goege2007gvt`; Volltext lesen) | Zitierbare Toleranzen, Vorgehen; Unterschied der beiden ECSS-Ausgaben | V1, V2 |
| R-3b | Lehrbuchstelle Linearitätstest (Ewins 2000, Brandt 2011; `metadaten`) | Kapitel/Seite | V2 |
| R-4 | Kriterium für Frei-frei-Lagerung (Verhältnis Aufhängungs- zu erster Elastikfrequenz) (Ewins 2000, Göge) | Wert und Herkunft | V4 |
| R-5 | MAC im Volltext (`allemang2003mac`); Kreuzorthogonalität und Korrelationskriterien Test/Analyse (Suchhinweis: Friswell/Mottershead, Finite Element Model Updating); Modenüberlappung/Modal Overlap Factor | Definitionen, gängige Kriterien mit Belegstelle | V5c, V6 |
| R-6 | LSCF/PolyMAX und Stabilisierungsdiagramm (Suchhinweis: Guillaume et al. 2003; Peeters et al. 2004, Shock and Vibration); Lizenz, Version, Funktionsumfang und Zitierform von pyEMA/sdypy-EMA | Originalquellen; Softwareangaben mit Version | V7 |
| R-6b | Komplexe Modenindikatorfunktion (Suchhinweis: Allemang/Brown, 1980er) | Original | V8 |
| R-7 | Modale Phasenkollinearität/Komplexitätsmaße (MPC, MPD; Suchhinweis: Pappa/Elliott/Schenk, frühe 1990er) | Definitionen zum Abgleich mit $\kappa_\varphi$ | V5a |
| R-8 | Spektralschätzung für Zeitdaten (Welch, Harris, Bendat/Piersol, Brandt; `metadaten`) | Volltexte (PDF nach `Input/literatur/`) | V9, B-2 |
| R-9 | GUM (`jcgm2008gum`) und ISO 16063-41 (`iso2011laservibrometer`): Verwendung für Frequenzgänge und LDV | Kapitel/Abschnitte | V10 |
| R-10 | Wellenzahlverfahren und Dehnung aus LDV-Daten; Polytec Strain Processor Handbuch | Fähigkeiten und Referenz | V11 |

---

## 8 Offene Fragen (an Orchestrator, Nutzer, Betreuer)

**Blockierend für Rang 4 und 5, nicht für Rang 1–3:**
1. Gibt es für den Prüfling oder ähnliche Platten ein FE-Modell und in welchem Format (UFF, CSV, Nastran/Abaqus-Ausgabe)? — *Auswirkung:* ob V6 überhaupt sinnvoll ist.
2. Ist eine Modalidentifikation über Fremdbibliothek (Gegenprobe) für den Betreuer akzeptabel, obwohl „keine vollständige Modalanalyse“ gilt? — *Auswirkung:* Rang 5.

**Nicht blockierend (Annahme in Klammern):**
3. Welche Toleranzen gelten für „Vorher/Nachher bestanden“? (Vom Nutzer zu setzen, einstellbar; keine Voreinstellung ohne Quelle.)
4. Sollen künftig Zeitdaten gespeichert werden (`SaveTimeDataForScan`)? (Annahme: nein; V9 entfällt.)
5. Material, Dicke, Abmessungen des Blechs und Masse (Versuchsplan E1/V2). (Annahme: offen; V3/V4/V11 geben Platzhalter mit Kennzeichen „Annahme“.)
6. Klärung M8 (Vorzeichen Ref2) über Datenblatt PCB 288D01 — *Auswirkung:* Verwertbarkeit von V3.
7. Ist akustische Abstrahlung (ERP) für das Institut ein Thema? (Annahme: nein; ERP nur optional.)

---

## 9 Grenzen und Unsicherheiten

- Keine Literatur gelesen (siehe Abschnitt 0). Alle Aussagen zu üblichen Kriterien in der Raumfahrt sind **[E]**.
- Numerische Prüfungen betreffen **nur** die hier genannten Formeln an synthetischen Idealfällen (Anhang), nicht die Qualität an realen Daten. Besonders V3 ist am realen Prüfling ungeprüft: räumliche Abdeckung, Rauschen, Vorzeichen und die Masse sind echte Fehlerquellen.
- Der Code wurde nicht abgenommen; „vorhanden“ stützt sich auf FG-02/03 und die Nachverfolgungsmatrix.
- Die Bewertung „Aufwand“ ist eine grobe Schätzung ohne Kenntnis der Codebasis im Detail [E].
- Die Abgrenzung zu PSV stützt sich auf W1/I2 (PSV 10.1-Dokumente, Gerät 10.4). Funktionen von PSV 10.4, die in diesen Unterlagen nicht stehen, können existieren.

---

## Anhang: Prüfskript

Ausgeführt im Scratchpad (`/tmp/claude-0/-home-user/e6b61297-17fb-5003-91f8-95c4534d012c/scratchpad/fa_b10/pruef.py`, `python3 -I`, NumPy). Ergebnisse stehen in den Abschnitten oben.

```python
import numpy as np
rng = np.random.default_rng(1)

# (1) Verlustfaktor aus Leistungsbilanz: eta = |F|^2 Re{Y} / (omega m <|v|^2>)
m, zeta, fn = 5.0, 0.004, 300.0
wn = 2*np.pi*fn; c = 2*zeta*wn*m; k = m*wn**2
F = 1.0; w = wn
Y = 1/(c + 1j*(w*m - k/w)); v = F*Y
print("SDOF eta =", abs(F)**2*Y.real/(w*m*abs(v)**2), " 2*zeta =", 2*zeta)   # 0.008 / 0.008

N = 40
Mdiag = rng.uniform(0.8, 1.2, N)*0.1
kk = rng.uniform(0.8, 1.2, N+1)*2.0e6
K = np.zeros((N, N))
for i in range(N):
    K[i, i] += kk[i] + kk[i+1]
    if i > 0: K[i, i-1] -= kk[i]; K[i-1, i] -= kk[i]
Mh = np.diag(1/np.sqrt(Mdiag))
lam, U = np.linalg.eigh(Mh @ K @ Mh)
Phi = Mh @ U; wr = np.sqrt(lam); zr = 0.004
C = np.diag(Mdiag) @ Phi @ np.diag(2*zr*wr) @ Phi.T @ np.diag(Mdiag)
M = np.diag(Mdiag); p = 7
f = np.linspace(0.3, 0.9, 6000)*wr[-1]/(2*np.pi)
Pin = np.zeros_like(f); Etot = np.zeros_like(f)
for j, fj in enumerate(f):
    om = 2*np.pi*fj
    Z = -om**2*M + 1j*om*C + K
    Fv = np.zeros(N, complex); Fv[p] = 1.0
    vv = 1j*om*np.linalg.solve(Z, Fv)
    Pin[j] = 0.5*np.real(np.conj(Fv[p])*vv[p])
    Etot[j] = 2*0.25*np.real(np.conj(vv) @ M @ vv)
om = 2*np.pi*f
print("eta_band =", np.trapezoid(Pin, f)/np.trapezoid(om*Etot, f), " 2*zeta =", 2*zr)
sel = (f > 0.5*f.max()) & (f < 0.6*f.max())
print("schmales Band:", np.trapezoid(Pin[sel], f[sel])/np.trapezoid(om[sel]*Etot[sel], f[sel]))
etal = Pin/(om*Etot); print("linienweise:", etal.min(), np.median(etal), etal.max())

# (2) Starrkoerper-LS: v_i = v0 + w x r_i
P = 60
r = rng.uniform(-0.3, 0.3, (P, 3))
v0 = rng.normal(size=3) + 1j*rng.normal(size=3)
wv = rng.normal(size=3) + 1j*rng.normal(size=3)
vi = v0 + np.cross(wv, r)
def skew(a): return np.array([[0, -a[2], a[1]], [a[2], 0, -a[0]], [-a[1], a[0], 0]])
A = np.vstack([np.hstack([np.eye(3), -skew(ri)]) for ri in r])
sol, *_ = np.linalg.lstsq(A, vi.reshape(-1), rcond=None)
print("Fehler v0, w:", np.abs(sol[:3]-v0).max(), np.abs(sol[3:]-wv).max())
e = rng.normal(size=3*P) + 1j*rng.normal(size=3*P)
Q, _ = np.linalg.qr(A); e_perp = e - Q @ (Q.conj().T @ e)
sol2, *_ = np.linalg.lstsq(A, vi.reshape(-1)+e_perp, rcond=None)
print("Residuum, ||e_perp||:", np.linalg.norm(vi.reshape(-1)+e_perp - A@sol2), np.linalg.norm(e_perp))

# (3) kinetische Energie: Zeitmittel 1/2 m v^2 = 1/4 m |v^|^2
t = np.linspace(0, 1, 200001)[:-1]; vh = 0.3*np.exp(1j*0.7)
vt = np.real(vh*np.exp(1j*2*np.pi*50.0*t))
print(np.mean(0.5*2.0*vt**2), 0.25*2.0*abs(vh)**2)

# (4) Einzelspalte: Singulaerwert = euklidische Norm
H = rng.normal(size=(405, 1)) + 1j*rng.normal(size=(405, 1))
print(np.linalg.svd(H, compute_uv=False)[0], np.linalg.norm(H))

# (5) Zufallsfehler |H1| und Differenz zweier Messungen
for g2 in (0.9, 0.99, 0.999):
    for nd in (7, 25):
        eps = np.sqrt(1-g2)/(np.sqrt(g2)*np.sqrt(2*nd))
        print(g2, nd, round(eps, 4), round(np.sqrt(2)*eps, 4))

# (6) Linien je Halbwertsbreite (df = 0.625 Hz)
for f0, z in ((100, 0.005), (300, 0.004), (700, 0.002)):
    print(f0, z, 2*z*f0, 2*z*f0/0.625)

# (7) Phasenkollinearitaet
def kappa(phi):
    a, b = phi.real, phi.imag
    G = np.array([[a@a, a@b], [a@b, b@b]])
    return np.linalg.eigvalsh(G)[-1]/np.trace(G)
x = rng.normal(size=50)
print(kappa(x*np.exp(1j*0.7)))                       # 1.0
y = rng.normal(size=50); y -= (x@y)/(x@x)*x; y *= np.linalg.norm(x)/np.linalg.norm(y)
print(kappa(x+1j*y))                                  # 0.5
phi = x + 0.4*1j*rng.normal(size=50)
th = np.linspace(0, np.pi, 3601)
print(kappa(phi), max(np.sum(np.real(np.exp(-1j*t)*phi)**2) for t in th)/np.sum(np.abs(phi)**2))

# (8) rho0*c0 bei 20 C
print(1.204*343.2)                                    # 413.2
```
