## Fachanalyse FA-AUSW: Empfehlungen zu F-2 und F-4

Es wurde nichts im Repository geändert. Die Zahlen unten sind mit dem Skript `/tmp/claude-0/-home-user/e6b61297-17fb-5003-91f8-95c4534d012c/scratchpad/fa-ausw/fa.py` nachgerechnet. Quellen sind FG-02 (3.1, 3.2, 3.3, 3.4, 3.5, 3.6, 2.4), W2 (`2026-10-29_W2_svd-format.md`), `ergebnisse_7b.md` (M1, M4, M8, M12) und der Kern (`spektren.py`, `mittel.py`, `schwingform.py`).

### F-2: Größe in Ansicht 1

**Empfehlung: beides wählbar, Voreinstellung `spektrum_kohaerent` (|CPH|), Rückfall auf `spektrum_leistung` (√AP) ohne Referenz.**

1. **Was R-050 meint.** R-050 meint |CPH|. In der Datei gilt:
   - PSV „Geschwindigkeit“ für Vib X/Y/Z ist ein CPH-Signal (W2 2.1, Signale M 1/3/5; FG-02 3.1).
   - Die PSV-Spektren Vib X/Y/Z an Label 132 sind bitgleich zum CPH des Lesers (`ergebnisse_7b` M4 und M12) [D].
   - Die Punktmittel `AVGSEQ[ABS[…]]` stimmen bis ≤ 9,3·10⁻⁷ (W2 2.4) [D].
2. **Was für √AP nicht belegt ist.**
   - Die Datei hat AP je Vib-Komponente (W2 M 9–11, Einheit (m/s)²), und PSV kann „AP“ anzeigen (Faktenliste C5).
   - Eine PSV-Anzeige von √AP ist nirgends belegt, es gibt nur das AP-Punktmittel `AVGSEQ[AVG[AP]]`.
   - √AP ist also eine eigene Größe. Sie ist physikalisch sinnvoll (Gesamtleistung inklusive Rauschen und unkorrelierter Anteile) und der einzige Weg ohne Referenz.
   - Der PSV-Abgleich für √AP ist ungeprüft. Ein Prüfschritt am Messrechner wäre: PSV-Signal „AP“ gegen √AP.
3. **Bezeichnung.** |CPH| = γ·√AP_a (FG-02 3.1) hängt von der Referenz ab. Die Achse oder der Plotkopf muss deshalb „Geschwindigkeit, kohärent mit Ref1“ nennen (Kern: `Spektren.referenz`). √AP trägt die Bezeichnung „Leistungsmittel √AP, mit Rauschen, ohne Phase“.
4. **M8 ist hier unerheblich.** Der Betrag |CPH| = |CP|/√AP_b hängt nicht vom Vorzeichen s_a·s_b ab. Ansicht 1 trägt daher kein Kennzeichen „unbestätigt“.

**Definition „Mittel (alle Punkte)“.** Die beiden Spektren brauchen **verschiedene** Mittelformeln. Das ist die wahrscheinlichste Fehlerquelle bei der Umsetzung.

| Größe | Mittel über gültige Punkte (alle 135 gültig, M6 bestätigt) | PSV-Bezug |
|---|---|---|
| \|CPH\| | $M^\mathrm{Betrag}=\frac1n\sum\lvert\mathrm{CPH}_p\rvert$ (`mittel_betrag`) | `AVGSEQ[ABS]` [D] |
| √AP | $M^\mathrm{quadr}(\sqrt{\mathrm{AP}})=\sqrt{\frac1n\sum \mathrm{AP}_p}$ (`mittel_quadratisch`) | identisch zu √ des PSV-Mittels `AVGSEQ[AVG[AP]]` |

- Das Betragsmittel von √AP ist **nicht** PSV-konform. Es darf nicht gezeichnet werden.
- Das komplexe Mittel von CPH gehört nicht zu Stufe 1, weil es sich an Knotenlinien auslöscht (FG-02 3.2).
- Der Hinweis im UI muss die jeweilige Formel nennen, z. B. „Mittel der Beträge über 135 Punkte“ bzw. „Leistungsmittel √(Mittel von AP)“.
- Rechenbeispiel (Skript): CPH = (3, 4i, −5), AP = (16, 25, 36).
  - Betragsmittel |CPH| = 4,0.
  - Quadratisches Mittel von |CPH| = 4,0825.
  - √AP quadratisch = √(77/3) = 5,0662 (PSV-konform).
  - √AP als Betragsmittel = 5,0 (falsch für PSV).
  - |komplexes Mittel| = 1,4907.

**Lücken (nicht belegt, nicht erfinden):**
- **3D-Mittel.** FG-02 3.1 definiert nur den 3D-Betrag je Punkt. Für das Mittel der 3D-Kurve gibt es zwei Kandidaten:
  - Mittel der punktweisen 3D-Beträge: Beispiel x = (1, 0), y = (0, 1) → 1,0.
  - 3D-Betrag der Komponentenmittel: → 0,7071.
  - Die Kandidaten unterscheiden sich also deutlich.
  - Welcher Kandidat PSV entspricht, ist nicht belegt, und W2/FG-02 geben keine Antwort.
  - Plausibel ist das Mittel der punktweisen 3D-Beträge (die Mittelgröße ist dann ein Punktmittel von |3D|). Das gilt als Annahme [A].
  - Der Abgleich fehlt, siehe Rechercheauftrag.
- **Mittel von |CPH| mit Ref2.** Laut W2 sind die CPH der Vib-Kanäle nur gegen Ref1 gespeichert. Für Vib/Ref2 wäre CPH ein Ersatz (CP/√AP_b, Kennzeichen „CPH berechnet“).
- **n_d je Punkt** (M5) beeinflusst die Mittel nicht, nur die Fehlerbänder.

### F-4: Bedeutung von „Phase“

**(a) Ansicht 4 (Schwingform)**

- **Definition.** Phase = arg(CPH_{p,c,k*}) der **gewählten einzelnen Komponente** c ∈ {X, Y, Z}, bezogen auf Ref1 (das Paar der Datei).
  - Nach FG-02 3.3 gilt arg H1 = arg CP = arg CPH, deshalb ist die Phase für `quelle="cph"` und `"h1"` gleich.
  - Für 3D gibt es keine Phase, weil der 3D-Betrag reell ist. Die Phase-Auswahl wird auf eine Komponente beschränkt.
  - Die Vorzeichenkonvention steht in FG-02 3.6: Momentanwert Re{v̂·e^{iθ}} = |v|cos(θ+φ). Positives φ heißt „eilt Ref1 vor“, und das muss in der Legende stehen.
  - Die Voreinstellung der Komponente sollte nachvollziehbar abgeleitet sein, z. B. die Komponente mit größtem Σ_p|v_pc|² bei k*, oder Z als Flächennormale (M13 „plausibel“). Das ist eine UI-Entscheidung. Die Wahl muss im Plotkopf stehen.
- **Was M8 bewirkt.** Eine Drehung von Ref1 verschiebt alle Phasen aller Punkte global um π. Die Form selbst bleibt gleich (FG-02 2.4, 3.6). Es gibt zwei Konsequenzen:
  - **Absolute Phase relativ zu Ref1:** sinnvoll anzeigbar, aber mit Kennzeichen „unbestätigt“. Das entspricht dem Brief.
  - **Phase relativ zu einem Bezugspunkt:** Δφ_p = arg(v_p·v_ref*) in (−π, π]. Hier kürzt sich s_a·s_b heraus: (s·v_p)(s·v_ref)* = v_p·v_ref*. Diese Größe ist unabhängig von M8 und trägt kein Kennzeichen. Sie ist für die Deutung einer Betriebsschwingform (gleich- oder gegenphasig) die eigentlich relevante.
  - Das Skript bestätigt es: v = (1, 0,8·e^{iπ}, 0,5·e^{i0,1}) und −v ergeben dieselben relativen Phasen (0°, 180°, 5,73°), aber um 180° verschobene absolute Phasen.
  - Empfehlung: als zweite Option „Phase relativ zu Punkt <Label>“ anbieten. Voreinstellung für den Bezugspunkt ist der Punkt mit dem größten |v| unter den Punkten mit γ² ≥ γ²_min (FG-02 3.5). Der Bezugspunkt steht im Kopf. Das ist ein Zusatz zum Brief, den der Nutzer freigeben muss.
- **Indiz zu M8.** Die −90° von Vib Z/Ref1 unter 20 Hz sind mit einer Massenlinie v = F/(iωm) vereinbar (`ergebnisse_7b` M8, E-PSV-F [V]). Das spricht für richtiges Ref1 und gedrehtes Ref2. Es bleibt ein Indiz [A] und ist nicht bestätigt, weil Lagerung und Kraftvorzeichen nicht belegt sind. Kennzeichen daher weiter anzeigen.
- **Zuverlässigkeit.**
  - Punkte mit γ²(p,c,k*) < γ²_min (Vorschlag 0,9, FG-02 3.5) markieren, nicht löschen.
  - Zufallsfehler der Phase nach FG-02 3.4: σ_φ ≈ √(1−γ²)/(|γ|√(2n_d)). Bei n_d = 7 gilt:

    | γ² | σ_φ |
    |---|---|
    | 0,99 | 1,5° |
    | 0,9 | 5,1° |
    | 0,5 | 15,3° |
    | 0,1 | 45,9° |

    - Die Formel unterschätzt bei n_d = 7 um bis zu 8 % (FG-02 3.4).
    - n_d je Punkt ist offen (M5).
  - Bei Δf = 0,625 Hz und Spitzenbreiten B < Δf (aufloesungsbegrenzt) ändert sich die Phase von Linie zu Linie stark. Deshalb muss die tatsächliche Linie f_{k*} angezeigt werden (das ist im Brief schon so).

**(b) Ansicht 2, „Mittel“**

- Es gibt **kein** fachlich sinnvolles gemitteltes Phasenmaß.
  - Das PSV-Punktmittel ist ein Betragsmittel (|H1|, |H2|), also ohne Phase (FG-02 3.2, FG-03 Z. 190).
  - Das komplexe Mittel löscht sich an Knoten aus.
  - Ein Phasenmittel über Punkte mit Vorzeichenwechseln (±180°) ist ohne Bedeutung, und verschiedene Punkte sind verschiedene physikalische Größen.
- Der Platzhalter „Phase: für das Mittel nicht definiert (Betragsmittel hat keine Phase)“ ist richtig. „Phase anzeigen“ wird für „Mittel“ deaktiviert, mit Text im Teilbild.
- Betrag (|H1|, |H2| als Betragsmittel) und γ² (arithmetisches Mittel, PSV `AVGSEQ[COH]`) bleiben definiert und anzeigbar.
- Für einzelne Punkte gilt das Kennzeichen „unbestätigt“ wie im Brief.

**(c) Darstellung −180° … +180° in Graustufen**

Herleitung:
1. Die Phase ist zyklisch (−180° ≡ +180°). Eine nicht zyklische Skala erzeugt am Umbruch einen falschen Kontrast.
2. Eine zyklische Skala kann in Graustufen nie eindeutig sein. Die Helligkeit ist eine stetige Funktion auf dem Kreis und nimmt nach dem Zwischenwertsatz jeden Wert zwischen Minimum und Maximum mindestens zweimal an. Zwei verschiedene Phasen sehen dann gleich hell aus.
3. Daraus folgt: Graustufentauglichkeit braucht **redundante Kodierung** durch Winkel oder Form, nicht durch Helligkeit allein.

Empfehlung:
- **Primär: Zeigerdarstellung.** Pro Punkt ein Pfeil oder Zeiger mit Winkel = Phase und Länge ∝ |v|. Ist die Länge konstant, steht der Betrag in der Graufüllung. Dazu eine Kreislegende (0°, ±90°, ±180° beschriftet). Das ist farb- und graustufenunabhängig.
- **Sekundär (nur für die Variante „relativ zum Bezugspunkt“):** gleichphasig (cos Δφ ≥ 0) als gefüllter Kreis und gegenphasig als Ring, Größe ∝ |v|. Das gilt nur für nahezu reelle Moden. Bei |sin Δφ| groß ist es eine Vereinfachung und muss so beschriftet sein.
- **Ergänzend, nicht allein:** eine perceptuell gleichmäßige zyklische Farbskala. Matplotlib war hier nicht installiert, deshalb ist die Wahl einer konkreten Skala nicht geprüft. Es gilt aber: kein Regenbogen (`hsv`, `jet`), und die Farbleiste ist ein Ring mit identischer Farbe bei ±180°. Quellen dafür kämen aus einem Rechercheauftrag.
- Maskierte Punkte (γ² < Schwelle) erscheinen als graue, schraffierte oder durchkreuzte Marker. Ohne diese Kennzeichnung wirkt die Phase aus Rauschen glaubwürdig.
- Die Anzeigeeinheit ist Grad. KONVENTIONEN legt rad für den Code fest, die Umrechnung geschieht an der GUI-Grenze. Das ist im Brief festzuhalten.

### Als Akzeptanzkriterium oder Referenzfall geeignet

| ID | Prüfung | Soll | Toleranz |
|---|---|---|---|
| RF-UI-F2a | CPH = (3, 4i, −5), AP = (16, 25, 36) | Betragsmittel 4,0; quadratisch 4,0825 für \|CPH\|; √AP-Mittel √(77/3) = 5,06623 | rtol 1e-12 (exakt) |
| RF-UI-F2b | Ansicht 1 ohne Referenz | nur √AP, Quelle „kohärent“ deaktiviert mit Grund | – |
| RF-UI-F2c | Golden File: \|CPH\| Vib X/Y/Z, Label 132 und `AvgSeq` | PSV-Werte | FG-02 Abschn. 8: rtol 1e-5, atol 1e-6·max\|Größe\| |
| RF-UI-F2d | Mittel-Formel je Größe | \|CPH\| mit `mittel_betrag`, √AP mit `mittel_quadratisch` | Test: Betragsmittel von √AP wird nie für „Mittel“ gezeichnet |
| RF-UI-F4a | v = (1, 0,8·e^{iπ}, 0,5·e^{i0,1}) und −v | relative Phasen 0°, 180°, 5,7296° identisch; absolute um 180° verschoben | 1e-12 |
| RF-UI-F4b | Ansicht 2, „Mittel“ | Phasen-Teilbild: Platzhalter, keine Daten; Betrag und γ² vorhanden | – |
| RF-UI-F4c | Winkelskala f(−π) = f(+π); φ = +179° und −179° liegen 2° auseinander | Pfeilwinkel stetig am Umbruch | 1e-12 |
| RF-UI-F4d | Maske | Punkte mit γ² < γ²_min tragen Kennzeichen, bleiben im Bild | – |

### Rückmeldung an den Orchestrator

**Paket:** FA-AUSW · **Status:** ERLEDIGT

**Ergebnis:** Empfehlungen zu F-2 und F-4 im Bericht oben. Es wurden keine Dateien im Repository geschrieben.
**Wie verifiziert:** Skript `/tmp/claude-0/-home-user/e6b61297-17fb-5003-91f8-95c4534d012c/scratchpad/fa-ausw/fa.py` rechnet nach: Mittelwerte (RF-UI-F2a), 3D-Mittel-Unterschied (1,0 gegen 0,7071), globale π-Drehung (RF-UI-F4a), σ_φ-Tabelle. Dateiaussagen sind gegen FG-02, W2, `ergebnisse_7b` und den Kern gelesen, nicht neu an der Datei gemessen.
**Akzeptanzkriterien:** F-2 ✅ · F-4(a) ✅ · F-4(b) ✅ · F-4(c) ⚠️ (Prinzip hergeleitet, konkrete Farbskala nicht geprüft, matplotlib nicht installiert)

**Annahmen:**
- Das 3D-Mittel ist das Mittel der punktweisen 3D-Beträge. Ohne Beleg gegen PSV [A].
- Positives φ heißt „eilt Ref1 vor“ (FG-02 3.6, nicht erneut an PSV geprüft).
- Ref1 ist plausibel korrekt gepolt (Massenlinie), unbestätigt.

**Unsicherheiten:**
- PSV-Anzeige von √AP und PSV-3D-Mittel nicht belegt.
- M8 weiter offen.
- Die σ_φ-Formel ist nach FG-02 3.4 nicht aus dem Volltext von Bendat/Piersol gelesen.
- n_d je Punkt offen (M5).
- Die Quellen aus (c) sind nicht geprüft.

**Rechercheaufträge:**
1. Datenblatt PCB 288D01: Polarität von Kraft und Beschleunigung (zu M8; ist in FG-02 schon als Auftrag vermerkt).
2. PSV-Handbuch: Definition des 3D-Mittels im „Gemittelten Spektrum“ und Existenz einer √AP-Anzeige.
3. Bendat/Piersol: Volltext zu σ_φ.
4. Quellen zu zyklischen, perceptuell gleichmäßigen Farbskalen für Phasen (z. B. Crameri et al. 2020, Thyng et al. 2016; aus dem Gedächtnis genannt, ungeprüft).

**Rückfragen:**
- [blockierend] Soll F-2 als „beides wählbar, Voreinstellung kohärent (|CPH|)“ freigegeben werden? *Auswirkung:* Ansicht 1 und R-050.
- [nicht blockierend] Soll die Option „Phase relativ zu Bezugspunkt“ (M8-unabhängig) zusätzlich zum Brief aufgenommen werden? *Annahme bis zur Klärung:* nur absolute Phase relativ zu Ref1 mit Kennzeichen, wie im Brief.
- [nicht blockierend] Soll die 3D-Mittelung am Golden File gegen PSV abgeglichen werden? *Annahme bis zur Klärung:* Mittel der punktweisen 3D-Beträge, gekennzeichnet „nicht gegen PSV geprüft“.

**Vorschlag für KONVENTIONEN.md:** Anzeige von Winkeln in der GUI in Grad bei Rechnung in rad. Positives φ heißt „eilt voraus“.
**Thesis-Bezug:** Auswertekapitel (Spektren, Punktmittel, Betriebsschwingform) und die Darstellung der Phase.
**Empfehlung für den nächsten Schritt:** Nutzerentscheidung zu F-2 und F-4 einholen. Danach UI-Teil mit RF-UI-F2a bis F4d als Tests umsetzen. Zusätzlich je ein Prüfschritt am Messrechner: PSV „AP“ gegen √AP, PSV-3D-Mittel gegen die zwei Kandidaten.