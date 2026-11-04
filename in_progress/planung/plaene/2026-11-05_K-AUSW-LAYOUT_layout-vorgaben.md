<!-- Paket K-AUSW-LAYOUT (ui-designer, sonnet). Status: FREIGEGEBEN vom Nutzer am 2026-11-05 (Annahmen: Schwingform nur Punktzahl im Bild; Thesis-Skript wählt Hochformat). Ergänzt den Design-Brief K-AUSW. -->

## Layout-Vorgaben K-AUSW-LAYOUT (Ansicht 3 und 4)

Grundlage: Quelltext von `spitzen.py`, `schwingform.py`, `stil.py`, `auswahl.py` (Datenklassen), ADR-025, KONVENTIONEN (Abbildungen, ζ) und die Renderings `ansicht3_spitze10/19.png`, `ansicht4_phase_relativ.png`. Es wurde nichts geändert und nichts gerendert. Die Zahlen sind aus Geometrie und Schriftgrößen hergeleitet, nicht an Proben geprüft.

### Befund
- **Ansicht 3:** Die 114 Spitzen füllen die Kurve bis zur Achsenoberkante. Der Kasten liegt 16 pt über der Spitze und damit mitten in den Daten. Bei Spitze 19 (f = 105,996 Hz, 0,1 am oberen Rand) läuft er sogar über den Achsenrand hinaus. Im Datenbereich gibt es keinen freien Platz, jede frei schwebende Platzierung scheitert also. Die Legende oben rechts verdeckt ebenfalls Daten.
- **Ansicht 4, Breite:** Das Messraster ist hochformatig (ca. 0,2 m × 0,5 m, Verhältnis 0,4). `set_aspect("equal", adjustable="datalim")` streckt die x-Grenzen auf −0,1 … 0,67 m, damit die Achse querformatig bleibt. Das ist die Ursache für die schmale Punktwolke.
- **Ansicht 4, Überlappungen:** Marker (s = 46, ca. 6,8 pt) und Punktlabels (5,85 pt) sind für den Punktabstand zu groß. Die Labels stehen fest oben rechts, also genau da, wo Pfeile hinzeigen. Das Bezugspunkt-Label (139) liegt unter dem Ring (14 pt). Die Legende „× Phase unsicher“ steht mit `loc="best"` in der Achse.

### Gemeinsame Hilfsgrößen
- **Messung:** Größen in pt erst nach `fig.draw_without_rendering()` bestimmen (`ax.get_window_extent()`, px × 72 / dpi). Bei Größenänderung der Oberfläche neu zeichnen. Hängt die Oberfläche bei Resize nur neu zu rendern, statt `zeichne_*` aufzurufen, sollte der Engineer das prüfen.
- **d_NN** ist der Median der Abstände zum nächsten Nachbarn in der Projektionsebene (Datenkoordinaten, m), ohne Abstand 0. Randfälle (P = 1, alle Punkte identisch) sind frei wählbar, es darf nur nichts abstürzen.
- **d_pt** ist d_NN in pt nach dem Layout.

### Ansicht 3 (Spitzen) – Vorgaben

**3.1 Beschriftungsstreifen statt schwebender Kasten**
- Oberhalb der höchsten Kurvenstelle und aller Marker bleibt ein leerer Streifen innerhalb der Achse. Nur dort liegt der Kasten.
- Streifenhöhe in Achsenanteilen: s = (Boxhöhe_3Zeilen + 16 pt) / Achsenhöhe_pt.
  - Boxhöhe_3Zeilen = 3 × 1,25 × `schrift_pt` + 2 × 0,2 × `schrift_pt` (bei 9 pt ca. 37 pt).
  - s wird auf 0,10 … 0,30 begrenzt.
- Obere y-Grenze:
  - Log: log(top) = log(bottom) + (log(ymax) − log(bottom)) / (1 − s).
  - Linear: top = bottom + (ymax − bottom) / (1 − s).
- `bottom` und `ymax` kommen aus der Autoskalierung der Kurve mit Markern.
- **Der Streifen wird immer reserviert, sobald `daten.spitzen` nicht leer ist**, unabhängig von `gewaehlt` und von der Zeilenzahl. Sonst springt die y-Skala beim Wechsel der Spitze.
- Ohne Spitzen gibt es keinen Streifen (wie bisher).

**3.2 Kasten**
- Schrift `stil.schrift_pt`, Fläche `stil.flaeche`, Rand `stil.achse` 0,6 pt, `boxstyle="square,pad=0.2"` (wie bisher).
- Oberkante 4 pt unter der Achsenoberkante.
- Breite per Messung bestimmen. Der Kasten wird horizontal über der Spitze zentriert und dann in x = [0,01 … 0,99] der Achsenbreite geschoben. Er liegt also immer vollständig in der Achse.
- Höchstens 3 Zeilen. `beschriftung_der_spitze` liefert künftig:
  1. `f = 65,121 Hz · ζ ≈ 0,0058`
  2. `−3-dB-Breite, 64,768 … 65,526 Hz` (Methode und Band)
  3. `⚠ auflösungsbegrenzt`; mehrere Kennzeichen kommagetrennt in dieser einen Zeile.
- Ohne bestimmte Breite: Zeile 1 `f = … Hz · ζ = –`, danach nur die Kennzeichenzeile.
- ζ mit 2 signifikanten Stellen, Methode, Band und Kennzeichen bleiben Pflicht (KONVENTIONEN). Die bestehenden Tests zu `beschriftung_der_spitze` müssen an die Zeilenumbrüche angepasst werden.

**3.3 Leitlinie**
- Senkrecht vom Kastenunterrand bei x der Spitze nach unten. Liegt x der Spitze nach dem Verschieben außerhalb des Kastens, beginnt sie am nächsten Punkt des Unterrandes.
- Sie endet 7 pt vor der Markermitte (`shrinkB=7`), damit sie weder das Dreieck noch den Ring (11 pt) berührt.
- Linienbreite 0,8 pt in `stil.achse`, unter dem Kasten (zorder 4,5 gegenüber 5).
- Der Ring der gewählten Spitze bleibt unverändert (11 pt, 1,5 pt).

**3.4 Legende**
- Sie wandert aus der Achse nach unten außerhalb, z. B. `fig.legend(loc="outside lower center")` mit `ncol` = Anzahl der Einträge. Passen sie nicht in die Bildbreite (Thesis-Format), ist `ncol=1`.
- Das ist nötig, weil oben rechts nichts mehr frei ist, ohne dass der Streifen und die Legende um denselben Platz konkurrieren.

**3.5 Mittelformel und Punktzahl im Bild**
- Der Kurventext in der Legende nennt beides. Beispiele:
  - `Betragsmittel |H1| über 135 Punkte, Vib Z/Ref1`
  - `Leistungsmittel √AP über 135 Punkte` (Spektrum ohne Referenz)
- `SpitzenDaten` braucht dafür ein neues Feld `punktzahl: int`.
  - Befüllt wird es in `auswahl.py` (Zeile 357 hat `n` bereits, `spitzen_daten_frf` und `spitzen_daten_spektrum`).
  - `beschriftung` entsteht dort. Das ist eine kleine Änderung außerhalb der beiden Zeichendateien.

**Prüfbare Kriterien Ansicht 3 (für Test und Abnahme)**
- L3-1: Das `get_window_extent()` des Kastens liegt vollständig in `ax.bbox`. Das gilt für die Spitzen 10 und 19 der Beispieldatei und für eine Spitze am linken und am rechten Rand von x.
- L3-2: Kein Kurven- oder Markerpunkt liegt in der Kasten-Bounding-Box. Der Test projiziert alle `(f, y)` und alle Spitzenmarker per `ax.transData` und prüft die Disjunktheit. Dasselbe gilt für das Bounding-Rechteck der Leitlinie plus Ring.
- L3-3: `ax.get_ylim()` ist identisch für `gewaehlt=None` und für jede gewählte Spitze. Der obere Streifen ist ≥ 12 pt höher als der höchste Markerrand (Marker 5 pt, Ring 11 pt, dazu 4 pt Luft).
- L3-4: Die Legende liegt außerhalb von `ax.bbox`, im Bild und ohne Überlappung mit Achsenbeschriftung und Fußstempel.
- L3-5: Die Kurvenbeschriftung enthält Mittelformel und die Punktzahl (Zahl aus `punktzahl`).
- L3-6: Der Kasten hat höchstens 3 Zeilen. Bei vorhandener Breite stehen ζ (2 signifikante Stellen), Methode, Bandgrenzen und alle Kennzeichen darin.
- L3-7: Alle Kriterien gelten auch in `THESIS_STIL` bei Bildgröße 11,5 cm × 7 cm.

### Ansicht 4 (Schwingform) – Vorgaben

**4.1 Seitenverhältnis und Achsengrenzen**
- `ax.set_aspect("equal", adjustable="box")`, Anker `"C"`. `datalim` entfällt.
- Grenzen: Bounding-Box der Marker-Mittelpunkte ± pad, pad = max(0,9·d_NN, 0,05·L_max). 0,9·d_NN reicht für Markerradius plus Pfeilspitze (0,8·d_NN) am Rand.
- Mindestspanne je Richtung: 0,25 × die längere Spanne plus 2·pad, damit Punktreihen nicht zur Linie entarten.
- `ax.margins(0.1)` entfällt.

**4.2 Bildaufteilung**
- Spalten: Randspalte | Plot | rechte Spalte | Randspalte.
  - Rechte Spalte: max(1,7 in, 0,22 × Bildbreite). Sie enthält Kreislegende, Zeichenerklärung und Farbleiste.
  - Plotspalte: min(Bildbreite − rechte Spalte, q × Plothöhe + Rand für Achsentitel). q ist Breite/Höhe der Achsengrenzen.
  - Die beiden Randspalten nehmen den Rest zu gleichen Teilen. Der Inhalt steht dann mittig und die Achse hat keine Leerfläche zwischen Plot und Legende.
- Fallback für den Engineer, falls das zu aufwendig ist: Nur `adjustable="box"` mit `ax.set_anchor("E")`. Dann steht der Plot direkt neben der rechten Spalte, links bleibt Leerraum.
- **Grenze der Geometrie:** Hochformatdaten (hier q = 0,4) können in einem Querformatbild nie 80 % der Bildbreite füllen. Genutzt wird dann die Höhe (L4-1). Für die Thesis soll das Thesis-Skript das Bild im Hochformat erzeugen, z. B. 11,5 cm breit × 14 … 15 cm hoch. Das ist eine Bildgröße und gehört nicht in die Zeichenfunktion. Sonst sind Marker und Pfeile für die Beispieldatei in A5 zu klein (siehe 4.9).

**4.3 Markergröße: Betrag über Fläche (Phasendarstellung)**
- Radius r = r_max × √(|v| / |v|max), mindestens 0,35 × r_max und mindestens 1,5 pt. Die Fläche ist damit ∝ |v|.
- r_max = min(0,22 × d_pt, 5,5 pt), mindestens 2,5 pt. Die Grenze 0,22 ist so gewählt, dass die Pfeilspitze (0,8·d) bei Pfeilen entlang der Gitterrichtung höchstens den Rand des Nachbarmarkers berührt.
- Die Umsetzung erfolgt über `scatter(s=(2r)²)` in pt² nach dem Layout (`set_sizes`).
- Bei Darstellung `"betrag"` (keine Pfeile): einheitlicher Radius = min(0,35·d_pt, 6,5 pt), mindestens 2,5 pt. Der Betrag steht in der Füllung mit Farbleiste, wie bisher.
- Randlinie bleibt `stil.achse` 0,6 pt.

**4.4 Phasenpfeil (ADR-025)**
- Länge exakt L = 0,8 × d_NN (Datenkoordinaten, damit in pt 0,8 × d_pt), **für alle Punkte gleich** (Toleranz 1e-9 relativ), `pivot="tail"`. Die Mitte ginge unter dem Marker verloren.
- Kein Pfeil bei |v| = 0 oder nicht endlich, sowie bei unsicheren und M6-ungültigen Punkten.
- Schaftbreite 1,4 pt (`units="inches"`, width = 1,4/72), `headwidth` 4, `headlength` 5, Farbe `stil.achse`.
- Heller Rand 0,8 pt in `stil.flaeche` (z. B. `path_effects.withStroke(linewidth=1,4+1,6, foreground=stil.flaeche)`).
- zorder 4 (über Markern 3). `PFEIL_ANTEIL` entfällt.
- Mindestmaß: Ist 0,8·d_pt < 10 pt, wird der Pfeil trotzdem mit 0,8·d gezeichnet. `Zeichnung.hinweise` meldet „Pfeile kürzer als 10 pt: größeres Bild oder Ausschnitt wählen“.

**4.5 Gekennzeichnete Punkte (beide Darstellungen)**
- **Unsicher** (γ² < γ²_min): hellgrauer Kreis (`stil.gitter`, Rand `stil.text_gedaempft`), Radius wie der mittlere Marker (Median von r), plus ×. Das × hat markersize = 1,4 × r_Median. Kein Pfeil.
- **Ungültig (M6)**: hohle Raute `"D"` ohne ×, Füllung `stil.flaeche`, Rand `stil.text_gedaempft` 1,0 pt, Durchmesser wie der mittlere Marker. Kein Pfeil. In der Betragsdarstellung zählen M6-ungültige Punkte nicht zur Farbskala.
- Ist ein Punkt beides, gilt die Raute.
- Die Raute unterscheidet sich vom Kreis nur durch die Form und das fehlende ×. In Graustufen und bei Rot-Grün-Schwäche trägt also nur die Form die Unterscheidung (KONVENTIONEN Abbildungen).

**4.6 Bezugsring**
- Radius r_max + 3 pt, 1,3 pt breit, `stil.achse`, hohl. Er liegt über dem Marker, aber unter Pfeil und Rand. Kein Label am Ring.
- Der Bezugspunkt wird in der Zeichenerklärung benannt: `○ Bezugspunkt 139`.

**4.7 Punktlabels**
- Schrift 0,75 × `schrift_pt` (6,75 pt statt 5,85 pt), weißer Halo 1,5 pt (`withStroke(foreground=stil.flaeche)`).
- Position gegenüber dem Pfeil: in Richtung φ + 180°, mit 2 pt Abstand zum Markerrand, Text am nächsten Rand verankert. In der Betragsdarstellung bei 45° (oben rechts).
- Gezeigt werden Labels nur, wenn d_pt ≥ 2·r_max + 4 pt + gemessene größte Labelbreite (bei dreistelligen Labels ca. 21 pt). Die Entscheidung gilt einheitlich für alle Punkte. Sonst entfallen alle Labels, und `Zeichnung.hinweise` meldet „Punktlabels ausgeblendet: Punkte zu dicht“. Die Oberfläche zeigt diesen Hinweis. Im Thesis-Bild steht er nicht.
- Für die Beispieldatei (d ≈ 16 … 26 pt) heißt das: Labels sind im Standardbild aus.
- Der Schalter `opt.punktlabels` bleibt unverändert (Nutzerwunsch, nicht Layoutregel).

**4.8 Zeichenerklärung in der rechten Spalte (Ersatz für `ax.legend(loc="best")`)**
- Sie steht zwischen Kreislegende (oberhalb) und Farbleiste (unterhalb), mit Einträgen nur bei Vorhandensein:
  - `× γ² < 0,9: Phase unsicher (n)`
  - `◇ ungültig (M6) (n)`
  - `○ Bezugspunkt 139`
- Darunter die Zeile `N Messpunkte`, davon ggf. `n gekennzeichnet`. Das ist die Punktzahl im Bild.
- Das Symbol steht vor dem Wort, Farbe trägt nichts. Die Legende liegt nicht mehr in der Achse, wo sie mit `datalim` frei war, jetzt aber Daten verdecken würde.

**4.9 Mittelformel**
- Pro Punkt ist die Amplitude nach den Datenfeldern kein Mittel über Punkte, daher steht keine Mittelformel im Bild. Die Punktzahl steht laut 4.8 im Bild. Siehe Rückfrage 1.

**Prüfbare Kriterien Ansicht 4**
- L4-1: Die Bounding-Box der Marker-Mittelpunkte belegt in der längeren Richtung ≥ 80 % der Achsenausdehnung (Raster ab 9 Punkten je längere Seite; sonst ≥ 50 %). Die Achsenbox füllt in der Bildspalte der Plotachse mindestens 85 % der verfügbaren Höhe (Hochformatdaten) bzw. Breite (Querformatdaten). Es gibt keine Überstände der Daten (nichts außerhalb von `ax.bbox`).
- L4-2: Alle Pfeile haben dieselbe Länge (Streuung ≤ 1e-9 relativ) = 0,8 × d_NN. Bei d_pt ≥ 12,5 pt ist die Länge ≥ 10 pt. Pfeile zeigen im Winkel `phase` (`grad(phase)` unverändert).
- L4-3: Kein Pfeil bei unsicheren, ungültigen und |v| = 0 oder nicht endlichen Punkten.
- L4-4: r_max ≤ 0,22 · d_pt bzw. ≤ 5,5 pt. Die Marker überlappen einander nicht (paarweise Abstand > r_i + r_j).
- L4-5: Der Bezugsring (Radius r_max + 3 pt) überdeckt keinen Nachbarmarker. Kein Text liegt unter dem Ring.
- L4-6: Label-Bounding-Boxen überlappen keinen Marker, Pfeil oder anderes Label. Sonst, wenn die Dichtebedingung 4.7 nicht erfüllt ist, sind alle Labels aus und `hinweise` enthält den Dichtehinweis.
- L4-7: Unsichere Punkte tragen ×, M6-ungültige tragen die Raute, beide ohne Pfeil. Die Zeichenerklärung führt jedes vorkommende Symbol mit Anzahl auf und steht außerhalb von `ax.bbox`.
- L4-8: `N Messpunkte` steht im Bild und stimmt mit `len(daten.label)` überein.
- L4-9: Alle Kriterien gelten in `THESIS_STIL` bei 11,5 cm × 15 cm (Hochformat) und in der Arbeitsansicht-Größe (ca. 12 × 7,4 in).

### Annahmen
- Die Marker unsicherer und ungültiger Punkte haben konstante Größe (kein Betrag als Größe).
- Die Pfeilfarbe bleibt `stil.achse`, der Rand ist `stil.flaeche`.
- Der Sicherheitsabstand 0,22 · d_pt ist eine Auslegung der Pfeilregel „ca. 0,8 Punktabstand“, damit die Pfeilspitze den Nachbarmarker nicht überdeckt. Der Nutzer hat nur die Pfeillänge festgelegt.

## Rückmeldung an den Orchestrator

**Paket:** K-AUSW-LAYOUT · **Status:** ERLEDIGT

**Ergebnis:** Layout-Vorgaben für Ansicht 3 (Abschnitte 3.1 bis 3.5, Kriterien L3-1 bis L3-7) und Ansicht 4 (4.1 bis 4.9, Kriterien L4-1 bis L4-9). Der Text oben ist als Teil des Arbeitspakets für den `software-engineer` übernehmbar.

**Betroffene Dateien (für die Umsetzung):**
- `/home/user/BA_Jakob-Busch_P/software/src/ldv_automation/darstellung/spitzen.py`
- `/home/user/BA_Jakob-Busch_P/software/src/ldv_automation/darstellung/schwingform.py`
- `/home/user/BA_Jakob-Busch_P/software/src/ldv_automation/darstellung/auswahl.py` (neues Feld `SpitzenDaten.punktzahl` und `beschriftung` dort)
- Das Thesis-Skript für die Bildgröße (Hochformat 4.2), sofern es existiert.

**Tatsächlich durchgeführte Prüfungen:** Lesen von Code, ADR-025, KONVENTIONEN und Renderings (Ansicht 3 Spitzen 10 und 19, Ansicht 4 relativ). Größen hergeleitet. **Nicht geprüft:** Es wurde nichts gerendert. Die pt-Werte (0,22, 12,5, 21 pt) sind Auslegungen und sollten am Engineer-Ergebnis mit den Renderings gegengeprüft werden.

**Annahmen:** siehe oben.

**Rückfragen:**
- [nicht blockierend] 1. Ist die Amplitude je Punkt in Ansicht 4 (Quelle `h1` oder `leistung`) im Sinne von KONVENTIONEN (Abbildungen, Mittelformel) ein Mittelwert, der im Bild zu nennen wäre? *Annahme bis zur Klärung:* nein, nur `N Messpunkte` im Bild.
- [nicht blockierend] 2. Die Thesis-Abbildung der Schwingform sollte im Hochformat entstehen (4.2). Soll das Thesis-Skript die Bildgröße aus dem Datenaspekt wählen? *Annahme:* ja, das ist Sache des Abbildungsskripts, nicht der Zeichenfunktion.

**Empfehlung für den nächsten Schritt:**
1. Umsetzung durch den `software-engineer` mit diesen Vorgaben im Wortlaut. Die Tests sollen Kriterien L3-1 bis L3-7 und L4-1 bis L4-9 per `get_window_extent` und `transData` prüfen.
2. Danach Design-Abnahme durch den `ui-designer` anhand neuer Renderings, parallel zum Review.
3. Als Schwerpunkt der Abnahme: Beispieldatei mit Spitze 19 (Streifen und Kastenrand) und Ansicht 4 relativ (Dichte, Labels, Ring).