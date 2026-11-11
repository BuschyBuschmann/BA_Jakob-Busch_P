<!-- Vom Nutzer am 2026-11-11 freigegeben: AN1–AN5 parallel zu Etappe B, AN6–AN9 nach S3/S7/S9 von P-AUSW2; F-A3 ←/→ Phase, Umschalt+Pfeile und ↑/↓ drehen; F-A4 Frequenzwechsel → zurück ins Standbild; F-A2 wird durch Ergänzung zu FG-04 geklärt (bis dahin 3D nur absolut); übrige Annahmen (Abschnitt 14) übernommen. -->

<!-- Paket P-AUSW3 (software-engineer), Typ Planung. Status: PLAN ZUR FREIGABE (2026-11-11). Es wurde nichts am Repository geändert außer dieser Datei. Messungen: Linux-Container (4 Kerne, Python 3.11, matplotlib 3.11.2, Agg ohne Qt), am Messrechner nicht bestätigt. Stand des Arbeitsbaums: Etappe A von P-AUSW2 (Achsen) liegt uncommittet vor (u. a. `darstellung/achsen.py`, `gui/achsen_zustand.py`, `gui/achsenleiste.py`); Namen und Zeilen können sich bis zum Start ändern. -->

## Plan: R-071 Animation der Betriebsschwingform, 3D drehbar (Paket P-AUSW3, Typ Planung)

Grundlage: Design-Brief `2026-11-09_K1-AUSW2_design-brief.md` (Abschnitt 3.3, UI-22 bis UI-33; UI-34 bis UI-38 allgemein), Fachgrundlage FG-04 (E1 bis E5, A-1, RF-A1 bis RF-A14), ADR-029 (matplotlib `mplot3d`, Rückfallreihenfolge), Analyse A-3D, ADR-021, 024, 025, 028, KONVENTIONEN, Plan P-AUSW2 (Andockstellen, Abschnitt 8). Nicht Teil: R-070, R-072, Video/GIF, Differenz-/Vergleichskurven.

### 0 Kernbefunde

1. **Der Rechenkern ist nur halb da.** `auswertung/schwingform.py::momentanwert` liefert die **Schnelle** Re{v̂ e^{iθ}}; die Auslenkung d̂ = v̂/(iω), die relativ gedrehte Amplitude ŵ, die Überhöhung, D_ref und die Bildwinkel fehlen (FG-04 Abschnitt 7, Befund 1 und 4). Dazu kommt die Falle aus FG-04 3.1: Wer `momentanwert` unverändert animiert, verschiebt die Bildfolge um T/4 und beschriftet sie falsch. Neue Funktionen kommen in ein **neues Modul**, `momentanwert` bleibt bitgleich (Docstring bekommt nur den Zusatz „Schnelle“).
2. **Der Datenvertrag trägt eine Komponente.** `SchwingformDaten` hat `amplitude (P,)`, bei 3D `None`, und nur die Kohärenzmaske **einer** Komponente. Die 3D-Animation braucht Amplituden `(P,3)` und Masken `(P,3)` (A-1: bewegt sich nur bei drei gültigen Komponenten). Das heißt **drei Kanalpaare im `PaarCache`** (heute LRU 2, je ca. 28 MiB). Ansicht 4 selbst bleibt unverändert; eine neue Datenfunktion liegt daneben.
3. **Die vorhandene Zeichenfunktion (`darstellung/schwingform.py`, 931 Zeilen) ist eine 2D-Aufsicht mit Layout in pt** und lässt sich nicht sinnvoll um 3D erweitern. Der Modus „Standbild“ bleibt diese Funktion unverändert (alle bisherigen Tests bleiben die Messlatte), die Animation bekommt eine **eigene Zeichenfunktion** `zeichne_animation` in einem neuen Modul.
4. **mplot3d ist auf der Sandbox schneller als in A-3D gemessen und stark vom Achsenwerk abhängig** (eigener Spike, 135 Punkte, Agg, nur Scatter): Positionen und Farbe setzen plus `draw` **34 ms** mit Achsen/Panes/Ticks, **5,8 ms** mit `set_axis_off`; Drehschritt (`view_init` + `draw`) 32 ms; Rechnung der Positionen ca. 1 µs. Das stützt Rückfallstufe 2 von ADR-029 (vereinfachte Achsen während der Bewegung). Übertragbar sind nur Verhältnisse, keine absoluten Zeiten (Windows, Remotedesktop offen, UI-38).
5. **`mpl_toolkits` ist für die Importregel ein neues Paket.** `tests/test_importrichtung.py` erlaubt in `darstellung` nur `numpy` und `matplotlib` (`DARSTELLUNG_EXTERN`). `mpl_toolkits.mplot3d` importiert weder `pyplot` noch Qt (geprüft), liegt aber im selben Wheel. Der Test braucht deshalb **ein begründetes `mpl_toolkits`**, und `pyproject.toml` braucht den mypy-Override aus ADR-029. Beides ist die einzige Änderung an Konfiguration; `uv.lock` und `PINS` bleiben unverändert.
6. **Der Brief widerspricht sich bei den Pfeiltasten** (3.3: „Pfeiltasten drehen“; 6 und UI-24/UI-32: ←/→ ändern die Phase in Einzelschritten). Vorschlag in 5.2, Frage F-A3.
7. **FG-04 lässt eine Lücke für 3D mit relativem Phasenbezug:** ŵ_p = v̂_p v̂_b*/|v̂_b| ist für einen Skalar v̂_b definiert, der Bezugspunkt hat aber drei Komponenten. Das ist **fachlich** zu klären (F-A2), nicht vom Umsetzer zu erfinden.
8. **Es gibt keine Flächen- oder Kantengeometrie im Datenmodell** (`Punkte`: index, label, koordinaten_m). Verbindungslinien/Flächen (Brief: „wo vorhanden“, Kann) sind deshalb nicht Teil (F-A6).

### 1 Bestandsaufnahme

| Baustein | Stand | Verwendung in R-071 |
|---|---|---|
| `auswertung/schwingform.py` (`betriebsschwingform`, `Schwingform.amplitude (P,3)`, `f_hz`, `phase_gueltig`, `ellipse_kennwerte`, `phase_relativ_rad`, `waehle_bezugspunkt`) | Kern, getestet (RF-3D*) | **wiederverwendet**; `Schwingform` liefert v̂ (P,3), Linie, f_{k*}, `phase_gueltig` |
| `darstellung/auswahl.py` (`schwingform_daten`, `PaarCache`, `standard_bezug`, `_standard_referenz`, `KOMPONENTEN_3D`) | Ansicht-4-Daten für eine Komponente | **Muster** für die neue Datenfunktion; `PaarCache` mit `groesse=3` (Konstruktor-Parameter vorhanden, `setze_groesse` kommt mit P-AUSW2 S5) |
| `darstellung/schwingform.py` (Marker „x“ unsicher, „D“ hohl ungültig, „s“ kein Wert; `waehle_ebene`, `_abstand_naechster`) | 2D-Aufsicht, Konstanten privat | Symbole, d_NN und Ebene **wiederverwenden**; fehlt ein öffentlicher Name, wird er hochgezogen (kleiner Diff, Verhalten gleich, vorhandene Tests sichern) |
| `darstellung/zeichnung.py` (`Zeichnung`, `Ansicht`, `kennzeichen_*`, `layout_rect`) | gemeinsame Bausteine | `Zeichnung` als Rückgabe; `Ansicht` bleibt unberührt, die Animation ist ein **Modus von Ansicht 4**, keine fünfte/sechste Ansicht |
| `darstellung/bild.py` (`speichere_arbeitsbild`, `baue_stempel`) | Stempel mit einem Dateinamen; P-AUSW2 S9 ergänzt `dateien` | wiederverwendet; `baue_stempel` bekommt **optional `zusatz`** (Winkel, Überhöhung, Frequenz) |
| `darstellung/stil.py` (`Plotstil`: `verlauf()`, `zyklisch()`, Linienarten) | keine divergierende Skala | neue Methode `divergierend()` (Abschnitt 3.4) |
| `darstellung/achsen.py` (`Bereich`, `parse_zahl`, `pruefe_bereich`, `feld_text`) | neu aus Etappe A | **Farbbereich-Eingabe** (von/bis, leer = Auto, Meldung wie UI-5) ohne neue Logik |
| `gui/plotflaeche.py` (`ZEICHNER`, Toolbar, Cursor, `speichere`) | 2D-Canvas mit Cursor und Werkzeugleiste | **bleibt unberührt**; 3D bekommt eine eigene Fläche (E-A2) |
| `gui/auswahl_auswerten.py::AuswahlSchwingform` (Frequenz, Spitze, Ebene, Komponente, Darstellung, Bezug) | AD von Ansicht 4 | Modusschalter und Animationsabschnitt kommen dazu; Frequenz/Spitze/Komponente/Ebene/Bezug werden **geteilt** |
| `gui/auswerten_reiter.py` (`_zeichne_ansicht_4`, `_a4_*`, `_fuelle_ansicht_4`, `lbl_plotkopf`, `tab_kette`) | eine Messung; P-AUSW2 S4 macht `_geladen` usw. zu Eigenschaften der aktiven Messung | Integrationsstelle; **geteilte Datei** mit P-AUSW2 (Abschnitt 11) |
| `gui/achsenleiste.py::FlussLayout` | Flusslayout für AG (Etappe A) | **für AH wiederverwenden** (P-AUSW2 Abschnitt 8) |
| `gui/anzeige_aktionen.py` (`AKTIONS_TASTEN`, `bild_unbestaetigt`, `stempel_ansicht`) | eine Quelle für Tasten und Kennzeichen | Tasten für Animation; `bild_unbestaetigt` für Animation (M8 nur bei absolutem Bezug) |
| `gui/tokens.py` (`KONTRAST_PAARE`, `symbol`) und `gui/stil.py` | Tokens | neue Paare für AH-Zustände, Farbleisten-Beschriftung |
| `hintergrund`, ADR-022 | Rechenaufträge in spawn-Prozess | **nicht nötig** für die Positionsrechnung (µs); 3 Kanalpaare siehe 2.3 |
| Tests: `tests/gui/gui_ausw_hilfen.py::synth_geladen` (P=4, K=64, Δf 0,5 Hz), `tests/darstellung/dar_daten.py` (`synthetische_messdaten`) | Testdaten | Referenzfälle RF-A* auf kleinen synthetischen Daten; Beispieldatei nur für einen langsamen Test |

### 2 Datenvertrag 3D

#### 2.1 Rechenkern `auswertung/animation.py` (NumPy, ohne Daten- und Darstellungsbezug)

Nur Formeln aus FG-04, Eingabe `ndarray`, Einheiten im Namen, Quelle im Docstring:

| Funktion | Formel (FG-04) | Hinweis |
|---|---|---|
| `auslenkung_amplitude(v, f_hz)` | d̂ = v̂/(iω), ω = 2π f_{k*} | `f_hz` ist die **Linienfrequenz** (RF-A9); `f_hz <= 0` oder nicht endlich → NaN (3.1), nie Division durch null |
| `relativ_gedreht(v, bezug)` | ŵ = v̂ · conj(v̂_b)/|v̂_b| (Einzelkomponente) | 3D siehe F-A2; `|v̂_b| = 0` → `ValueError` |
| `verschiebung(d, theta)` | Re{d̂ e^{iθ}} | `theta` Skalar oder Feld; Feld als neue letzte Achse wie `momentanwert` |
| `bewegt_maske(...)` | Einzelkomponente: γ²-Maske ∧ M6 ∧ endlich; 3D: alle drei Komponenten (A-1) | Rückgabe `(P,)` bool plus Status je Punkt (Abschnitt 2.2) |
| `bezugsgroesse(d, bewegt)` | D_ref = max über bewegte Punkte von |d̂_pc| bzw. `auslenkung_max_p/ω` (3D) | leere Menge oder 0 → `None` (kein `s`, FG-04 Abschnitt 6) |
| `ueberhoehung_auto(d_nn, d_ref, alpha=0.25)` | s = α d_NN/D_ref | `d_nn is None` (ein Punkt) → `None` |
| `ueberhoehung_hinweis(s, d_ref, d_nn_min)` | Hinweis, wenn s·D_ref ≥ d_NN,min/2 | nur Hinweis, keine Sperre |
| `maximum_theta(phase_rad, groesse)` | π/2 − φ (Weg), −φ (Schnelle), mod 2π | für Tests und Beschriftung |
| `bildwinkel(n)` | θ_j = 2πj/N, j = 0…N−1 | kein Bild bei 2π (RF-A12) |
| `phasenfehler_grenze(n)` | δ ≤ π/N; ΔA/A = 1 − cos(π/N) | für Beschriftung kleiner N |

`Schwingform.momentanwert` und `momentanwert` bleiben unverändert (Schnelle). Eine neue Methode `Schwingform.auslenkung(theta)` ist nicht nötig; die Datenfunktion ruft den Kern.

#### 2.2 Datenobjekt `AnimationsDaten` (`darstellung/animation_daten.py`, GUI-frei)

`@dataclass(frozen=True, kw_only=True, eq=False)`, gefüllt durch `animation_daten(daten, cache, f_wahl_hz, *, komponente, groesse="auslenkung", bezug_modus="relativ", bezug=None, referenz=None, quelle="cph", alpha=0.25)`:

| Feld | Form | Inhalt |
|---|---|---|
| `f_wahl_hz`, `f_hz`, `linie`, `omega_rad_s` | Skalar | Linie k* und ω = 2π f_{k*} |
| `koordinaten_m` | `(P,3)` float64 | Ruhelage X_p, Koordinaten der Messgeometrie |
| `label` | `(P,)` | Punktlabels |
| `amplitude_v` | `(P,3)` complex128 | v̂ aus `Schwingform.amplitude` (Schnelle bzw. (m/s)/N) |
| `amplitude_anim` | `(P,3)` complex128 | **animierte** Amplitude: d̂ = ŵ/(iω) bzw. ŵ (Option Schnelle); NaN für nicht bewegte Punkte und nicht gewählte Komponenten (Einzelkomponente: die anderen zwei Spalten 0 und `achsen_aktiv` markiert die gewählte) |
| `achsen_aktiv` | `(3,)` bool | Einzelkomponente: genau eine; 3D: alle |
| `kohaerenz`, `kohaerenz_ok` | `(P,3)` | γ² und Maske je Komponente (3D: alle drei Paare; Einzelkomponente: nur die gewählte, Rest `NaN`/`True`) |
| `status` | `(P,)` int8 | `BEWEGT`, `NULL` (|v̂| = 0, gültig, bewegt sich nicht, kein Kennzeichen), `UNSICHER` (γ² < γ²_min, bei 3D: mindestens eine Komponente), `UNGUELTIG` (M6), `KEIN_WERT` (NaN/Inf); Rangfolge KEIN_WERT > UNGUELTIG > UNSICHER |
| `grund_3d_unvollstaendig` | `(P,)` bool | UNSICHER wegen 3D (mehr als eine Komponente betroffen) für die Zeichenerklärung (FG-04 3.6) |
| `d_ref`, `d_nn_m`, `s_auto`, `s_hinweis` | Skalare/`None` | Bezugsgröße (m bzw. m/N bzw. m/s), Median-Abstand zum nächsten Nachbarn (aller Punkte, Ebene: dreidimensional), automatische Überhöhung, Hinweistext |
| `groesse`, `einheit_anim`, `quelle`, `referenz`, `bezug_modus`, `bezug_index` | | Beschriftung: „Auslenkung [m]“ / „je N [m/N]“ / „Schnelle [m/s]“; Phasenbezug |
| `kohaerenz_min`, `phase_gueltig`, `hinweise`, `annahmen` | | wie `SchwingformDaten` |

Methoden (rein, ohne Zustand, damit „zustandslos“ aus FG-04 Abschnitt 6 gilt): `positionen(theta, s) -> (P,3)` (= X_p + s·Re{d̂ e^{iθ}} für `BEWEGT`, sonst exakt X_p, **Gleichheit der Positionen, nicht Näherung**, RF-A8), `auslenkung(theta) -> (P,3)` (ohne s, in m), `betrag(theta)` und `farbwert(theta, komponente)`.

**Fehler:** `phase_gueltig = False` → `DarstellungsFehler` mit dem Text „Animation braucht eine Phase: keine Referenz.“ (Kern: `ValueError`, RF-A14; Umwandlung wie in `schwingform_daten`). Alle Punkte nicht bewegt oder `D_ref = 0` → `DarstellungsFehler` „Keine Punkte mit gültiger Phase.“ (Meldung statt Division durch null). Frequenz außerhalb: Text des Kerns.

#### 2.3 Last und Cache

- `animation_daten` wird **erst beim Wechsel in den Modus „Animation“ und bei Frequenz-/Komponenten-/Bezugswechsel** gerufen, nicht im Standbild.
- 3D braucht die Paare X/Y/Z mit derselben Referenz (`_standard_referenz(daten, ("3D",))`). Der Reiter erzeugt den `PaarCache` der aktiven Messung dann mit **`groesse >= 3`** (bis P-AUSW2 S5 `setze_groesse` liefert: Konstruktor-Parameter; danach `max(3, …)` je aktive Messung). Speicher: +28 MiB je Messung (3 statt 2 Paare), gemessen in P-AUSW2.
- **Zeit:** In AN3 wird die Zeit der drei Paare an der Beispieldatei gemessen. Liegt sie unter dem Ziel der Oberfläche (400 ms je Wechsel, ADR-022 Nachtrag), läuft die Berechnung synchron mit Warte-Cursor; sonst werden die Paare nacheinander je Ereignisschleifen-Durchlauf berechnet (`QTimer.singleShot`), die Oberfläche bleibt bedienbar. **Keine** Hintergrundprozess-Lösung für die Positionsrechnung (µs). Entscheidung nach Messung, Befund in der Rückmeldung.
- Die Bildfolge wird **nicht** vorberechnet; jedes Bild rechnet `positionen(θ, s)` neu (1 µs gemessen). Das hält Standbild und Animation zwangsläufig identisch (UI-25).

### 3 Zeichenfunktion `darstellung/animation3d.py` (GUI-frei, kein Qt, kein `pyplot`)

```
Blick(azim_grad, elev_grad, zoom)                      # frozen; Voreinstellung aus der Projektionsebene
BLICK_VORGABEN = {"xy": …, "xz": …, "yz": …, "iso": …}  # Aufsicht xy (elev 90, azim -90), xz (0, -90), yz (0, 0), Isometrisch (≈35,3°, -45°)
AnimationsOptionen(theta_rad, ueberhoehung: float | None, farbe: "auslenkung"|"betrag",
                   farb_komponente: str | None, farbbereich: Bereich, blick: Blick,
                   vereinfacht: bool = False, ruhelage: bool = True, punktlabels: bool = False,
                   kennzeichen_phase: str | None, kennzeichen_koordinaten: str | None)
zeichne_animation(fig, daten, opt, stil) -> Zeichnung
aktualisiere_animation(zeichnung, daten, opt, stil) -> None    # Teilaktualisierung ohne fig.clear()
```

#### 3.1 Aufbau des Bildes
- Eine `Axes3D` (`fig.add_subplot(projection="3d", computed_zorder=False)`, feste Zeichenreihenfolge: Ruhelage → Marker → bewegte Punkte), rechts bzw. unten **Farbleiste mit Einheit** und **Zeichenerklärung** (Symbole gekennzeichneter Punkte mit Anzahl, UI-29). Achsentitel „x [m]“, „y [m]“, „z [m]“ (Achsen „Größe [Einheit]“). Kein Diagrammtitel.
- **Pflichttexte im Bild** (FG-04 3.5, Kennzeichnung (a) bis (d); UI-26): „Überhöhung ×4555“ (Zahl aus `opt`/`s_auto`), „größte reale Spitzenauslenkung D_ref = 1,59 µm“ (bei H1 „m/N“), „f = 100,000 Hz · Auslenkung (CPH)“, „θ = 90,0° · Bezug: relativ zu Punkt 17“. Diese Texte sind Teil der **Zeichenfunktion**, nicht des Stempels, damit Thesis-Standbild und Oberfläche gleich sind. Der Stempel (Arbeitsansicht, Datei, Git-Hash) kommt nur über `speichere_arbeitsbild` dazu (ADR-024); die Zeichenfunktion enthält „Arbeitsansicht“ nicht (Test).
- Kennzeichen: `kennzeichen_phase` („⚠ unbestätigt (M8)“, nur bei absolutem Bezug) und `kennzeichen_koordinaten` („Komponenten im Geometrie-KS unbestätigt (M12)“ bei 3D und bei jeder Komponente, solange M12 offen ist) als Textkasten wie `kennzeichen_anbringen`.
- Gekennzeichnete Punkte (FG-04 3.6, E5): bleiben im Bild in der **Ruhelage** mit denselben Symbolen wie im Standbild (Kreuz = unsicher, hohle Raute = M6-ungültig, Quadrat = kein Wert); die Form trägt die Aussage, nicht die Farbe. Zeichenerklärung nennt Symbol, Wort und Anzahl, bei „3D unvollständig“ den Zusatz „(mindestens eine Komponente unter γ²_min)“. Kein Punkt wird mit Phase „erfunden“.
- **Ruhelage**: kleine graue hohle Punkte an X_p unter den bewegten Punkten (Referenz für Vorzeichen und Richtung der Bewegung; abschaltbar `ruhelage`).

#### 3.2 Bewegung und Teilaktualisierung
- `zeichne_animation` baut Achse, Texte, Farbleiste, Legende vollständig (Standbild, Speichern, Resize).
- `aktualisiere_animation` setzt **nur** Artist-Daten: Scatter-`_offsets3d` (bzw. `set_data_3d`), `set_array` für die Farbe, die wenigen Textobjekte und bei Bedarf `view_init`. Es ruft nie `fig.clear()` oder Layout. Das ist die erste Rückfallstufe von OE-A2 („nur betroffene Zeichenobjekte“).
- **Gleichheitstest als Kern der Qualitätssicherung:** `aktualisiere` nach `zeichne` mit anderem θ liefert dieselben Positionen, Farben und Texte wie ein frisches `zeichne` mit diesem θ (Figure-Struktur).
- `opt.vereinfacht = True` (Wiedergabe, Ziehen): Achsen/Panes/Ticks aus (`set_axis_off` bzw. Panes unsichtbar), Texte bleiben; nach Stillstand ein Voll-Neuzeichnen. Gemessen 34 → 6 ms.

#### 3.3 Achsengrenzen und z-Skalierung (E-A5)
- **Grenzen sind während der Bewegung fest** (hängen nur von Daten und `s` ab, nie von θ): je Achse `[min(X_p − s|d̂_pc|), max(X_p + s|d̂_pc|)]` über bewegte Punkte, dazu die Ruhelage aller Punkte, plus 5 % Rand. Sonst würde die Szene mit θ „atmen“.
- **Gleichmaßstab** (`set_box_aspect` = Spannweiten): alle drei Richtungen im selben Maßstab, die Überhöhung wirkt gleich auf alle Komponenten (ein Faktor, FG-04 3.5). Eine nahezu ebene Platte hat dann eine **Mindesthöhe** der z-Box von 15 % der größeren x/y-Spannweite (Konstante, begründet: sonst degeneriert die Box und die Panes flackern); die z-Grenzen liegen symmetrisch um den Mittelwert und enthalten immer ±s·D_ref.
- **Folge:** Mit s = α d_NN/D_ref (α = 0,25) ist die größte Auslenkung 25 % des Punktabstands. Bei einer 480-mm-Platte mit 29 mm Punktabstand sind das 7 mm, schräg gesehen wenig. Der Regler „Überhöhung“ (Faktor ×0,1 bis ×20 auf `s_auto`, logarithmisch) ist dafür das Mittel. Eine **zweite, nur auf z wirkende Streckung** würde die Geometrie in einer Richtung verzerren und wäre ein zweiter Faktor neben `s`. Sie ist als Option vorbereitbar (`z_streckung: float = 1.0`, im Bild genannt, wenn ≠ 1) und gehört **nicht** in den Umfang ohne Freigabe (F-A5).

#### 3.4 Farbe
- **Farbe zeigt Auslenkung** (Vorgabe): vorzeichenbehaftete Komponente `farb_komponente`, Voreinstellung die Achse **senkrecht zur Projektionsebene** (die in `daten.ebene` fehlende Achse); Einzelkomponente: die gewählte. **Farbe zeigt Betrag:** Betrag des momentanen Auslenkungsvektors, Einfarbverlauf (`stil.verlauf()`).
- Neue `Plotstil.divergierend()`: zwei Farbtöne, **Helligkeit monoton** von „negativ hell“ über Mitte (neutral grau) nach „positiv dunkel“, damit das Vorzeichen auch in Graustufen aus der Helligkeit lesbar ist (Brief 2); kein Gelb, keine `hsv`/`jet`. Test: Luminanz entlang der Skala streng monoton und Abstand der Enden ≥ festgelegte Schwelle; Rot-Grün-Schwäche: Farbtöne aus Blau- und Braun-/Orangebereich. Der genaue Farbvorschlag ist Sache des `ui-designer` (Abnahme nach AN7).
- **Farbbereich**: `Bereich(von, bis)` (leer = Auto); Auto bei Auslenkung symmetrisch um 0 (±max |Auslenkung| der bewegten Punkte über **eine volle Periode**, nicht über das aktuelle Bild, damit die Skala nicht pumpt), bei Betrag 0…max. Einheit physikalisch (m, µm bei Anzeige: Faktor an der Anzeigegrenze, Beschriftung nennt die Einheit).

### 4 Oberfläche

#### 4.1 Struktur
- **Neues Widget `gui/animationsflaeche.py::AnimationsFlaeche`** (eigene `Figure` + `FigureCanvasQTAgg`, ADR-021, kein `pyplot`), mit der schmalen Schnittstelle `zeichne(daten, optionen, beschreibung)`, `aktualisiere(...)`, `speichere(pfad, stempel)`, `leere()`, `blick`/`setze_blick`. Sie liegt zusammen mit der bestehenden `PlotFlaeche` in einem `QStackedWidget` in AE; Modus „Standbild“ zeigt die 2D-Seite, „Animation“ die 3D-Seite. Die 2D-Fläche, ihr Cursor und die Werkzeugleiste bleiben unberührt.
- **Qt-freie Logik** (voll im Standardlauf getestet) in `gui/animation_steuerung.py`: `Phasenuhr` (θ, Tempo, Schrittweite, Richtung, injizierbare Zeitquelle), `Blickzustand` (Drehen, Zoomgrenzen, Voreinstellungen, Zurücksetzen), `taste_zu_aktion(taste, modifikatoren, fokus)`, `beschreibung_animation(...)` (Textalternative), `tabelle_auslenkungen(daten, theta, s)` (Soll), Anzeigeformate (Grad mit Dezimalkomma, Überhöhungsfaktor).
- **AD (Ansicht 4)**: Abschnitt „Darstellung: Standbild | Animation“ (`rb_modus_standbild`/`rb_modus_animation`); im Modus Animation sind die Gruppen „Darstellung (Betrag/Phase)“ ausgeblendet und ersetzt durch: Größe `rb_groesse_auslenkung` (Voreinstellung)/`rb_groesse_schnelle`; Phasenbezug `rb_bezug_relativ` (Voreinstellung, mit dem vorhandenen Bezugspunkt-Auswahlfeld) / `rb_bezug_absolut` (⚠ M8); „Farbe zeigt“ `rb_farbe_auslenkung`/`rb_farbe_betrag`; `feld_farbe_von`/`feld_farbe_bis` (Einheit als Suffix, leer = Auto, Meldung wie UI-5); Blickknöpfe `btn_blick_xy`, `_xz`, `_yz`, `_iso`, `btn_blick_zurueck`; Bildrate `combo_bildrate`. Frequenz, Spitzenwahl, Komponente, Ebene, Bezugspunkt gelten für beide Modi.
- **AH `animationsleiste`** (nur im Modus Animation sichtbar), Gruppen im `FlussLayout`: `btn_abspielen` („Abspielen“/„Pause“, Text, nicht nur Symbol), `btn_schritt_zurueck`/`btn_schritt_vor` mit `feld_schrittweite` (Voreinstellung 10° = 36 Bilder je Periode, E3), `regler_phase` (0 bis 359,9° in 0,1°-Schritten) mit `lbl_phase_grad` („θ = 90,0°“, Tooltip: „θ = 0° heißt: …“ je nach Bezug), `regler_tempo` (Perioden je Sekunde, Zeitlupe, unabhängig von f_{k*}), `regler_ueberhoehung` (Faktor ×0,1 bis ×20 auf `s_auto`, Anzeige der Zahl), `btn_ansicht_zurueck`.
- **Kopf `lbl_plotkopf`**: Datei · Linie f · Größe/Quelle · Phasenbezug; „⚠ Phase unbestätigt (M8)“ nur bei absolutem Bezug, **dauerhaft sichtbar**, verschwindet ohne GUI-Änderung, wenn `ist_annahme` für M8 `False` ist (UI-28); „⚠ Komponenten im Geometrie-KS unbestätigt (M12)“ (FG-04 3.4) solange offen.
- **AF**: „Wiedergabe langsamer als eingestellt“ (Brief 4), Überhöhungshinweis „Punkte können sich überlagern“, Zustände (keine Phase → Modus deaktiviert, UI-30: `rb_modus_animation` deaktiviert mit Text „Animation braucht eine Phase: keine Referenz.“).
- **Zustände:** Beim Öffnen und bei **Frequenzwechsel** steht der Modus auf „Standbild“, Wiedergabe aus (UI-22, Auslegung F-A4). Beim Wechsel in den Modus Animation ist die Wiedergabe pausiert, θ = 0. Wechsel von Komponente, Bezug, Größe, Farbe berechnet die Daten neu und behält Blick und θ.

#### 4.2 Wiedergabe (Timer in der Oberfläche)
- Ein `QTimer` (Qt.PreciseTimer) im Hauptthread **je Bild einzeln neu gestartet** (kein Anstauen von Zeitereignissen): Der Takt ist das Intervall 1000/Bildrate; **θ ergibt sich aus der Uhr** (`θ = θ_0 + 2π · tempo · (t_jetzt − t_0)`), nicht aus der Zahl der Takte. Eine langsame Zeichnung lässt also Bilder aus, die Bewegung bleibt zeitrichtig (FG-04 3.7: nicht die Echtzeit, die Phase wird abgetastet; kein Aliasing im signalverarbeitenden Sinn).
- Die Oberfläche misst die Zeit je Bild (gleitender Median der letzten 30). Liegt sie über dem Intervall, erscheint der Hinweis in AF (Brief 4), die Bildrate wird nicht still herabgesetzt.
- **Pausiert automatisch** beim Ziehen/Drehen, beim Ziehen des Phasenreglers, bei Fensterverkleinerung, beim Verlassen des Reiters „Auswerten“ und beim Wechsel von Modus, Frequenz oder Messung; Fortsetzen nur durch Nutzeraktion.
- `Ausfuehrer.beende()` / Schließen: Timer wird gestoppt (kein hängender Timer beim Beenden, Test).
- Zeichnen im Hauptthread ist mit ADR-022/KONVENTIONEN vereinbar (die Regel betrifft **Rechnungen**; hier rechnet nichts außer 1 µs).

#### 4.3 Rückfallstufen (aus ADR-029, über eine Einstellung der Fläche, nicht über Verzweigungen im Code verteilt)
| Stufe | Verhalten | Auslöser |
|---|---|---|
| L0 | Teilaktualisierung + volle Achsen im Stand, vereinfachte Achsen in Bewegung | Voreinstellung |
| L1 | Vereinfachte Achsen auch beim Ziehen des Reglers | Messung zeigt Ruckeln beim Drehen |
| L2 | Neuzeichnen **beim Loslassen** (Regler `tracking` aus, Drehen zeigt Gummiband/Achsen-Skelett), Einzelschritt statt Wiedergabe | OE-A2: Remotedesktop zu langsam |
| L3 | Variante (c) eigene 2D-Projektion mit Blitting | nur nach neuem Beschluss |
Die Stufe ist eine Konstante/Einstellung (`animation_stufe`), die Bedienelemente bleiben gleich. L0 bis L2 gehören zum Umfang; L3 und GL-Bibliotheken nicht.

### 5 Maus- und Tastatursteuerung

#### 5.1 Maus (eigene Steuerung, `Axes3D.disable_mouse_rotation()`, damit nicht zwei Steuerungen konkurrieren)
| Eingabe | Wirkung | Bemerkung |
|---|---|---|
| Linke Taste ziehen | Drehen: Azimut += k·dx, Elevation −= k·dy, Elevation auf [−90°, 90°] begrenzt | pausiert die Wiedergabe; während des Ziehens `vereinfacht=True`; Voll-Neuzeichnen beim Loslassen |
| Mausrad | Zoom, Faktor 1,1 je Raste, Grenzen [0,4; 6] | über `set_box_aspect(…, zoom=)`, im Spike zu prüfen, ob `zoom` bei jedem `draw` gilt |
| Doppelklick links | Ansicht zurücksetzen | zusätzlich zu Pos1 |
| Rechte/mittlere Taste | keine Wirkung (kein Verschieben; Kann) | |
Die Umrechnung Pixel → Winkel liegt in `Blickzustand` (Qt-frei, testbar mit synthetischen Ereignissen).

#### 5.2 Tastatur (nur bei Fokus in `AnimationsFlaeche` bzw. AH und Modus Animation; alle Belegungen in `AKTIONS_TASTEN`, U-A4)
| Taste | Aktion |
|---|---|
| Leertaste | Abspielen/Pause (Fokus im Plot oder AH) |
| ← / → | Phase um die Schrittweite zurück/vor (Brief 6, UI-24, UI-32) |
| ↑ / ↓ | Elevation ±5° |
| Umschalt+← / Umschalt+→ | Azimut ±5° (Drehen per Tastatur) |
| + / − | Zoom |
| Pos1 | Ansicht zurücksetzen (Blick und Zoom; **nicht** θ und nicht `s`) |
| Strg+← / Strg+→ | Phase in 90°-Schritten (Kann, nur wenn AKTIONS_TASTEN frei) |
**Abweichung vom Brieftext 3.3** („Pfeiltasten drehen“): ←/→ gehören der Phase (UI-24/UI-32 sind Muss und prüfbar), das Drehen bekommt Umschalt+Pfeile und ↑/↓. Frage F-A3. Die 2D-Cursorbelegung aus K-AUSW gilt weiter nur in `PlotFlaeche` (im Modus Animation ist sie nicht sichtbar, keine Doppelbelegung); Pos1 wirkt per `WidgetWithChildrenShortcut` im Teilbaum der `AnimationsFlaeche`, kollidiert also nicht mit `act_plot_zuruecksetzen`. Sichtbarer Fokusrahmen um die Fläche (UI-34); Tab-Reihenfolge … → AE → AH → AF (Brief 6).

### 6 Leistung und Messpunkte (UI-38)

**Gemessen (Sandbox, nicht Messrechner):** siehe Kernbefund 4; A-3D: ca. 20 Bilder/s voll bzw. ca. 50/s mit einfachen Achsen im Qt-Canvas, echtes Maus-Ziehen ca. 19/s. **Nicht gemessen:** Windows, Remotedesktop, HiDPI, Qt-Canvas auf dem Messrechner.

**Messskript** `software/tools/auswertung/animation_messen.py` (neu, nicht im Wheel, ca. 60 Zeilen, in AN1 als Spike, in AN9 als Werkzeug): öffnet eine `.svd`, baut `AnimationsDaten`, `AnimationsFlaeche` (Qt) und misst Median/Maximum von 100 Wiederholungen für:

| Nr | Messpunkt | Zweck |
|---|---|---|
| M1 | Zeit je Bild: voll / mit vereinfachten Achsen / Drehschritt (`view_init`+Draw) | Wahl der Stufe L0 bis L2 |
| M2 | effektive Bildrate bei Soll 5, 10, 20/s (Wiedergabe 10 s) und Anzahl ausgelassener Bilder | Voreinstellung Bildrate (U-A2) |
| M3 | Zeit Maus-Ziehen → sichtbares Neuzeichnen (synthetische Ereignisse) | Drehen flüssig |
| M4 | Phasenregler ziehen: Teilaktualisierung vs. Neuzeichnen beim Loslassen | Regler-`tracking` |
| M5 | Zeit `animation_daten` (3 Paare kalt/warm) und RSS-Zuwachs | 2.3, Speicher |
| M6 | Zeit Standbild speichern PNG/PDF | UI-31 |
| M7 | Nutzerurteil über Remotedesktop: flüssig? lesbar? (nicht automatisch messbar) | UI-38 |

M1 bis M6 laufen lokal am Messrechner **und** in der Remotedesktop-Sitzung; das Skript schreibt eine Tabelle (Datei, Rechner, Sitzungsart, Python/matplotlib-Versionen). Die Voreinstellungen (Bildrate, Tempo, Stufe) stehen bis zur Messung als **vorläufig** im Code (10 Bilder/s, 0,25 Perioden/s, L0) und werden danach angepasst. UI-38 bleibt **offen, bis der Nutzer bestätigt** (Ablauf G, Prüfanleitung durch AN9).

### 7 Schritte (riskanteste zuerst; je Schritt lauffähig und getestet)

Nach **jedem** Schritt: `uv run ruff check .`, `uv run ruff format --check .`, `uv run mypy --strict .`, `uv run pytest --cov --cov-fail-under=90` und `QT_QPA_PLATFORM=offscreen uv run pytest -m gui`; die Zahl der bestehenden Tests sinkt nie. Aufwand in Personentagen, grob ±40 %.

| Nr | Schritt | Dateien | Verifikation | Tage | Risiko |
|---|---|---|---|---|---|
| AN1 | **Spike Technik (Wegwerfskript im Scratchpad, Ergebnis in der Rückmeldung).** `Axes3D` in `FigureCanvasQTAgg` (offscreen): (a) `disable_mouse_rotation`, eigene Maus/Rad/Taste, `zoom` bleibt nach `draw`; (b) Teilaktualisierung (`_offsets3d`, `set_array`) vs. Voll-Neuzeichnen, vereinfachte Achsen; (c) `speichere_arbeitsbild` mit `Axes3D` (Stempel, PNG, PDF, Vektor); (d) feste Achsengrenzen ohne Atmen, `computed_zorder=False` bei Aufsicht und Schrägansicht; (e) Messpunkte M1 bis M3 offscreen. | Scratchpad, später `tools/auswertung/animation_messen.py` | Erkenntnisse (a) bis (e) schriftlich; bei (a) oder (c) negativ: Plan melden (Abschnitt 12), nicht improvisieren | 0,5 | **hoch** |
| AN2 | **Rechenkern** `auswertung/animation.py` und Referenztests RF-A1 bis RF-A13 (Kern), `momentanwert`-Docstring „Schnelle“. | `auswertung/animation.py` (neu), `auswertung/schwingform.py` (nur Docstring), `tests/auswertung/test_aw_animation.py` (neu) | RF-A1 bis A8 (Kern), A10 bis A13 mit den Sollwerten und Toleranzen aus FG-04 Abschnitt 5; Randfälle (ω = 0 → NaN, alle maskiert, D_ref = 0, ein Punkt); **Fachabnahme `strukturdynamik-experte`** | 1,5 | mittel (Fachlogik, Grundlage von allem) |
| AN3 | **Datenvertrag** `animation_daten` mit Masken `(P,3)`, Status, A-1, relativ/absolut, Größe; Zeitmessung der drei Paare (Entscheidung synchron/gestaffelt); 3D-relativ nach Klärung F-A2. | `darstellung/animation_daten.py` (neu), `darstellung/__init__.py`, `tests/darstellung/test_dar_animation_daten.py` (neu) | RF-A8 (Maske, M6, NaN: Position gleich Ruhelage, `s` unverändert), A9 (Linie 100,0 Hz, Index 159), A10/A11 auf Datenebene, A14 (`DarstellungsFehler`); 3D-Maske nur bei drei gültigen Komponenten; `array_equal` der Amplitude gegen `betriebsschwingform` | 1,5 | mittel |
| AN4 | **Zeichenfunktion** `zeichne_animation`/`aktualisiere_animation`, Blickvorgaben, Farbe, Divergierend-Skala, Texte und Kennzeichen, feste Grenzen, z-Box; mypy-Override, `DARSTELLUNG_EXTERN` um `mpl_toolkits` (begründet). | `darstellung/animation3d.py` (neu), `darstellung/stil.py`, `darstellung/schwingform.py` (nur Hochziehen von Symbolkonstanten, falls privat), `pyproject.toml`, `tests/test_importrichtung.py`, `tests/darstellung/test_dar_animation3d.py` (neu) | UI-23 (Blickvorgaben `elev/azim`), UI-25 (Positionen in der Figure = `AnimationsDaten.positionen`), UI-26/UI-28/UI-29 (Texte, Kennzeichen, Symbole und Anzahl), UI-33 (Importtest), Gleichheit `aktualisiere` = `zeichne`, Grenzen unabhängig von θ, Luminanz der Skala monoton, „Arbeitsansicht“ nicht enthalten | 2,5 | **hoch** (mplot3d, Tiefensortierung, Layout) |
| AN5 | **Qt-freie Steuerung** `Phasenuhr`, `Blickzustand`, Tasten, Beschreibung, Formate; `AKTIONS_TASTEN`-Einträge. | `gui/animation_steuerung.py` (neu), `gui/anzeige_aktionen.py`, `tests/gui/test_animation_steuerung.py` (neu, Standardlauf) | UI-24 (Winkel in Grad, Schritte, Umlauf mit injizierter Uhr: nach T/4 θ = 90°, Auslassen von Bildern ändert die Phase nicht), UI-32 (Tastenabbildung), Blickgrenzen, Pos1 | 1 | niedrig |
| AN6 | **`AnimationsFlaeche`** (Canvas, Maus, Rad, Tasten, Fokusrahmen, Timer, Messung der Bildzeit, Stufen L0/L1). | `gui/animationsflaeche.py` (neu), `pyproject.toml` (omit mit Begründung), `tests/gui/test_gui_animationsflaeche.py` (neu) | UI-23 (Drehen per Mausziehen und Rad ändert `ax.azim/elev`/Zoom), UI-24 (Abspielen läuft, Pause hält an, per Hand getakteter Timer), Wiedergabe pausiert beim Ziehen, Timer stoppt beim Schließen, Fokus sichtbar | 2,5 | **hoch** |
| AN7 | **Integration in Ansicht 4:** Modusschalter, AD-Abschnitt, AH mit `FlussLayout`, Kopf, AF-Meldungen, Zustände (Standbild nach Öffnen/Frequenzwechsel, keine Phase), `PaarCache`-Größe 3, Tab-Reihenfolge, Tokens und `KONTRAST_PAARE`. | `gui/auswahl_auswerten.py`, `gui/auswerten_reiter.py`, `gui/anzeige_auswerten.py`, `gui/tokens.py`, `gui/stil.py`, `gui/achsenleiste.py` (nur Import von `FlussLayout`), `tests/gui/test_gui_animation.py` (neu) | UI-22, UI-24 bis UI-30, UI-32, UI-35 (Kontrast); Regression: Modus Standbild unverändert, alle bisherigen GUI-Tests grün; Layout bei 1100×680 und 1366×768 (UI-36, AE mit AH mindestens 600×320) | 2,5 | **hoch** (geteilte Datei, Refaktor-Berührung) |
| AN8 | **Standbild speichern** im Modus Animation: Winkel, Blick, Überhöhung, Frequenz im Stempel (`zusatz`), PNG/PDF, Kennzeichen M8 im Stempel, kein Video/GIF. | `darstellung/bild.py`, `gui/anzeige_aktionen.py`, `gui/auswerten_reiter.py`, `tests/darstellung/test_dar_bild.py`, `tests/gui/test_gui_animation.py` | UI-31 (Magic Bytes `\x89PNG`/`%PDF`, Stempeltexte, `DATEIFILTER_BILD` ohne gif/mp4/avi), UI-28 (Stempel), Standbild bei θ = Animationszustand bei θ (Positionen) | 1,5 | mittel |
| AN9 | **Querschnitt:** Textalternative (`accessibleDescription`), „Werte als Tabelle“ (Soll), `animation_messen.py` als Werkzeug, Prüfanleitung für den Messrechner (Ablauf G, UI-38), Versionsnummer nur auf Anweisung; Dokumentation der Entscheidungen (ADR-Kandidaten, Abschnitt 10). | `gui/animationsflaeche.py`, `tools/auswertung/animation_messen.py` (neu), Prüfanleitung (Ablage nach Anweisung des Orchestrators) | UI-26 (Textalternative nennt Faktor), UI-34, UI-36, UI-37 (Eingaben im Farbbereich zeichnen erst bei Enter/Fokuswechsel), M1 bis M6 laufen; UI-38 **offen bis zur Nutzerbestätigung** | 1,5 | niedrig |

Summe **ca. 15 Personentage** (±40 %). Abhängigkeiten: AN1 → AN4/AN6 (Spike entscheidet über Eigenbau Maus/Zoom und Teilaktualisierung); AN2 → AN3 → AN4 → AN6/AN7; AN5 → AN6; AN7 → AN8 → AN9.

### 8 Testplan

**Ebenen.** (1) Unit/Standardlauf (Qt-frei, in der 90-%-Abdeckung): `auswertung/animation.py`, `darstellung/animation_daten.py`, `darstellung/animation3d.py`, `gui/animation_steuerung.py`, `bild.py`-Erweiterung. (2) GUI offscreen (`pytest -m gui`, `QT_QPA_PLATFORM=offscreen`; Figure-Struktur und Zustände, **keine Pixelprüfung**, Timer von Hand getaktet über `_tick()` mit injizierter Uhr, damit nichts von echter Zeit abhängt). (3) Hardwaretest nur UI-38. Langsamer Test mit der Beispieldatei je einmal (Marker), sonst `synth_geladen`/`synthetische_messdaten`; für RF-A9 eine synthetische Datei mit Δf = 0,625 Hz.

**Referenzfälle (FG-04 Abschnitt 5) → Tests.** Toleranzen wie in FG-04: `rtol = 1e-12`, Nullwerte `atol = 1e-12·a` (Rundung von θ_n), Zeitpunkte `atol = 1e-12` rad, RF-A7 `rtol = 1e-10` (s), RF-A12 `rtol = 1e-9`.

| RF | Prüfung | Ebene |
|---|---|---|
| A1, A2 | d̂ = −i·1,5915494309e−6 m; d(θ_n) = 0, +a, 0, −a; sin(θ+π/3)-Werte; Schnelle u(θ_n); H1-Variante „m/N“ | Kern |
| A3 | zwei Punkte gegenphasig: d₂ = −d₁ (13 Stützstellen), Δφ = +π (einheitlich 180°) | Kern + Daten |
| A4 | θ_max,p = π/2, θ_max,q = 0; Δt = −T/4 (analytisch und Gitter) | Kern |
| A5 | reelle gleich komplexe Form für φ ∈ {0; 0,7; −2,0; π} | Kern |
| A6 | 3D-Kreisbahn (1, i, 0): Positionen bei T/4-Vielfachen, Drehsinn m = (0,0,−1)·1e−6, Halbachsen | Kern + Daten + Figure (Positionen der Scatter) |
| A7 | s = 4555,3093477, s·D_ref = 7,25e−3 m, Verhältnis 0,5 | Kern + Daten |
| A8 | maskiert/M6/NaN: Position **exakt** Ruhelage, `s` unverändert, Kennzeichen gesetzt | Daten + Figure |
| A9 | Linie 100,0 Hz bei f_wahl = 100,2 Hz; Betrag mit f_{k*}, nicht f_wahl (Unterschied −0,1996 %) | Daten |
| A10 | M8: −v̂ → Bildfolge um N/2 = 18 Bilder verschoben; relativ identisch | Kern + Daten |
| A11 | ŵ₀ reell positiv; Δφ = (0; 63,03°; −114,59°) | Kern |
| A12 | N = 36 und 12: θ₉ = π/2, letztes Bild 350°, δ ≤ 5°, ΔA/A | Kern |
| A13 | u(θ) = ω d(θ + π/2) | Kern |
| A14 | ohne Phase: `ValueError` (Kern), `DarstellungsFehler` (Daten), GUI: Modus deaktiviert | Kern + Daten + GUI |

Zusätzlich: Maske 3D (A-1) mit genau einer Komponente unter γ²_min (Punkt steht, Zeichenerklärung „3D unvollständig“); alle Punkte maskiert (Meldung, keine Division durch null); `D_ref = 0`; ein Punkt (kein `d_NN`, `s_auto = None`); Obergrenzen-Hinweis; `momentanwert` unverändert (Regression).

**UI-Kriterien → Tests:**

| UI | Prüfung |
|---|---|
| UI-22 | nach `oeffne_datei` und Frequenzwechsel `rb_modus_standbild` aktiv; Timer nicht aktiv; nie Abspielen ohne Klick/Taste |
| UI-23 | Mausziehen (QTest) ändert Azimut/Elevation; Rad ändert Zoom; fünf Knöpfe setzen `elev/azim` auf die Vorgaben; Pos1 stellt wieder her |
| UI-24 | `lbl_phase_grad` zeigt Grad; Abspielen lässt θ umlaufen (Uhr injiziert), Pause hält, Einzelschritt = Schrittweite |
| UI-25 | Scatter-Positionen der Figure bei zwei Winkeln und zwei Punkten = FG-04-Sollwerte (RF-A1, A2, A4) und = `AnimationsDaten.positionen`; Phase der 2D-Phasenansicht (`phase_relativ_rad`) = arg ŵ (A11) und θ_max = π/2 − φ |
| UI-26 | Textobjekt „Überhöhung ×…“ mit Zahl in Figure, Textalternative, gespeichertem Bild |
| UI-27 | Farbbereich: Eingabe, Meldung bei von ≥ bis (wie UI-5), `Farbleiste.vmin/vmax`, Einheit in der Beschriftung |
| UI-28 | Kennzeichen im Kopf bei absolutem Bezug; verschwindet bei `ist_annahme(M8) == False` ohne GUI-Änderung; im Stempel des Bildes |
| UI-29 | Symbole gleich wie Standbild; Anzahl in der Zeichenerklärung |
| UI-30 | ohne Referenz: `rb_modus_animation` deaktiviert, Text exakt |
| UI-31 | siehe AN8 |
| UI-32 | alle Aussagen über Regler und ←/→ erreichbar, ohne Wiedergabe |
| UI-33 | Importtest ohne Qt und `pyplot` für `animation3d.py` und `animation_daten.py`; `mpl_toolkits` in `DARSTELLUNG_EXTERN` |
| UI-34 bis UI-37 | `focusPolicy`, Tab-Kette, Kontrastpaare, Überlappung bei 1100×680, AE ≥ 600×320 bei 1366×768 mit AH, Zahl der Zeichenaufrufe bei Tippen im Farbfeld |
| UI-38 | Hardwaretest nach Prüfanleitung, **nie vor Nutzerbestätigung als bestanden melden** |

Fachabnahme (`strukturdynamik-experte`) nach AN3 gegen FG-04; Stichprobe der Beschriftungstexte (Einheit „je N“, Größe, Bezug) durch den `reviewer`.

### 9 Akzeptanzkriterien dieses Plans

- **A1 (Rechenkern):** RF-A1 bis RF-A14 sind als Tests umgesetzt und bestehen mit den Toleranzen aus FG-04; `momentanwert` unverändert.
- **A2 (Datenvertrag):** `AnimationsDaten` trägt Amplituden `(P,3)` und Masken `(P,3)`; 3D bewegt sich nur bei drei gültigen Komponenten (A-1); gekennzeichnete Punkte stehen exakt in der Ruhelage und gehen nicht in `D_ref` ein.
- **A3 (Zeichenfunktion/UI-33):** `zeichne_animation` ohne Qt und `pyplot`; Standbild bei θ ist dieselbe Funktion und derselbe Datenpfad wie die Bewegung; PNG und PDF (Vektor) ohne Zusatz erzeugbar; Thesis-tauglich, weil Kennzeichnung (a) bis (d) aus FG-04 3.5 im Bild steht.
- **A4 (UI-22 bis UI-32):** wie Abschnitt 8.
- **A5 (Regression):** alle bei Beginn bestehenden Tests laufen unverändert grün; Modus „Standbild“ und Ansicht 4 bit- und verhaltensgleich.
- **A6 (Qualität):** `ruff`, `mypy --strict`, `pytest --cov --cov-fail-under=90`, `pytest -m gui` fehlerfrei; Importregeln eingehalten (einzige Änderung: `mpl_toolkits` in `DARSTELLUNG_EXTERN`, mypy-Override); keine neue Abhängigkeit (`uv.lock`, `PINS` unverändert).
- **A7 (Leistung):** Messskript und Prüfanleitung liegen vor; Messwerte M1 bis M6 stehen in der Rückmeldung der Ausführung; UI-38 ist als **offen bis zur Nutzerbestätigung** ausgewiesen.
- **A8 (Doku):** Rückmeldung nennt je Schritt Prüfbefehle und Ergebnisse; nicht ausführbare (Messrechner) werden benannt.

### 10 Entscheidungen mit Alternativen (ADR-Kandidaten, nach Freigabe)

| Nr | Entscheidung | Alternativen | Empfehlung |
|---|---|---|---|
| E-A1 | **Dreiteilung**: Kern `auswertung/animation.py`, Daten `darstellung/animation_daten.py`, Zeichnung `darstellung/animation3d.py` | alles in `auswertung/schwingform.py`/`darstellung/schwingform.py` (931 Zeilen, Layout in pt, Tests der Ansicht 4 gefährdet) | neue Module, vorhandene bleiben bitgleich |
| E-A2 | **Eigene `AnimationsFlaeche`** neben `PlotFlaeche` im Stapel | 3D als `Ansicht` in `ZEICHNER` der `PlotFlaeche` (teilt Cursor/Werkzeugleiste/Zoom-Zustand, die für 3D nicht passen und mit P-AUSW2-Umbau von `PlotFlaeche` kollidieren) | eigene Fläche; schmale Schnittstelle bleibt |
| E-A3 | **Eigene Maus-/Tastatursteuerung** (`disable_mouse_rotation`) | eingebaute mplot3d-Steuerung (Rad und Tastatur fehlen, Rotation nicht begrenzbar, nicht pausierbar) | Eigenbau (ADR-029 nennt ihn) |
| E-A4 | **Phase aus der Uhr** (`θ = θ₀ + 2π·tempo·Δt`), Bilder werden ausgelassen | feste Phasenschritte je Takt (langsame Zeichnung dehnt die Zeit, Tempo hängt vom Rechner ab) | Uhr |
| E-A5 | **z-Skalierung: Gleichmaßstab + Mindesthöhe**, feste Grenzen aus Daten und `s` | getrennte z-Streckung (zweiter Faktor, verzerrt Geometrie; als Option vorbereitbar, F-A5); automatische Grenzen je Bild (Szene atmet) | Gleichmaßstab, Regler `s` als Mittel |
| E-A6 | **Teilaktualisierung der Artist-Daten + vereinfachte Achsen in Bewegung** | immer Voll-Neuzeichnen (34 ms); Blitting (in mplot3d nicht tragfähig, nur in Variante (c)) | Teilaktualisierung |
| E-A7 | **Divergierende Skala mit monotoner Helligkeit** (`Plotstil.divergierend()`) | `RdBu` (in Graustufen nicht nach Vorzeichen trennbar); `twilight` (zyklisch, ADR-025 nur für Phase) | eigene Skala, Abnahme `ui-designer` |
| E-A8 | **Tastenbelegung** ←/→ Phase, Umschalt+Pfeile/↑↓ Drehen | Pfeile drehen und Phase über `,`/`.` (widerspricht UI-24/UI-32 im Wortlaut) | wie links, F-A3 |
| E-A9 | **Gekennzeichnete Punkte in Ruhelage mit denselben Symbolen** | ausblenden (E5 verworfen: ADR-025) | Ruhelage + Symbol |
| E-A10 | **Berechnung im Hauptthread**, falls die Zeit der 3 Paare unter 400 ms liegt, sonst gestaffelt; kein spawn-Auftrag für die Bildrechnung | Hintergrundprozess für alles (Overhead größer als Rechnung) | wie links nach Messung in AN3 |
| E-A11 | **Voreinstellung relativer Phasenbezug** (M8-unabhängig), absolut als Option mit Kennzeichen | absolut (Brief zeigt M8-Kennzeichen als Normalfall) | relativ (FG-04 E4, ADR-025) |

### 11 Abhängigkeit zu P-AUSW2 (Reihenfolge und gemeinsame Dateien)

| Datei | P-AUSW2-Schritt | R-071-Schritt | Konflikt |
|---|---|---|---|
| `gui/auswerten_reiter.py` | S2 (Aufrufstellen), S3, S4 (Eigenschaften der aktiven Messung, `_uebernehme` zerlegt, `_a4_*` Rücksetzen), S5, S7, S9, S10 | AN7, AN8 | **hoch**, ein Agent zur Zeit; `_a4_*`-Zustand und `_zeichne_ansicht_4` ändert S4 |
| `gui/anzeige_aktionen.py` (`AKTIONS_TASTEN`, `bild_unbestaetigt`, Stempel) | S7, S9, S10 | AN5, AN8 | mittel |
| `darstellung/bild.py` (`baue_stempel`) | S9 (`dateien`) | AN8 (`zusatz`) | mittel, **AN8 nach S9** |
| `gui/tokens.py`, `gui/stil.py` | S3 | AN7 | niedrig, additive Einträge |
| `gui/achsenleiste.py` (`FlussLayout`) | S3 | AN7 (nur Import) | niedrig; AH-Layout braucht den stabilen S3-Stand |
| `darstellung/auswahl.py` (`PaarCache.setze_groesse`) | S5 | AN3/AN7 (Größe 3) | niedrig; AN3 nutzt bis dahin den Konstruktor-Parameter |
| `pyproject.toml` (`omit`, mypy-Override) | S3 und weitere | AN4, AN6 | niedrig, additive Einträge |
| `tests/test_importrichtung.py` | – | AN4 | niedrig |
| `gui/plotflaeche.py`, `gui/arbeitsbild.py`, `darstellung/zeichnung.py`, `spitzen.py` | S2, S6 | – | keine (R-071 fasst sie nicht an) |

**Empfohlene Reihenfolge:**
- **Qt-freie Schritte AN1 bis AN5** (neue Dateien, nahezu keine Überschneidung) dürfen **parallel zu Etappe B und C** von P-AUSW2 laufen, solange ein anderer Agent nicht dieselben Dateien schreibt (`pyproject.toml` und `test_importrichtung.py` nur als kleine, additive Änderungen in AN4).
- **AN6 nach P-AUSW2 S3** (stabiles `FlussLayout`, Tokens), **AN7 nach S4** (Refaktor von `_uebernehme` und `Messungen.aktive` abgeschlossen; sonst doppelte Arbeit an `_a4_*`), besser **nach S7**.
- **AN8 nach S9**, **AN9 nach S10** (Querschnitt gemeinsam: Tab-Reihenfolge, Kontrast, Prüfanleitung eine gemeinsame Anleitung für UI-38).
- Die Nutzervorgabe „R-073, R-058, R-059 zuerst“ bleibt erfüllt; nur Qt-freie Vorarbeiten laufen früher. Sicherste Variante (keine Parallelarbeit): R-071 komplett nach S10; Mehrkosten ca. 0, Verzögerung ca. 7 bis 9 Tage.
- Aktive Messung als einzige Eingabe: `AnimationsDaten` bekommt `Messdaten` und `PaarCache` der **aktiven** Messung; Wechsel der aktiven Messung löst Standbild und Neuberechnung aus (P-AUSW2 Abschnitt 8).

### 12 Risiken

| Risiko | Auswirkung | Erkennung / Gegenmaßnahme |
|---|---|---|
| mplot3d über Remotedesktop am Messrechner zu langsam | UI-38 nicht erfüllbar im Wunschumfang | AN1 und M1 bis M4; Rückfall L1 → L2 (Einzelschritt, Neuzeichnen beim Loslassen, OE-A2), dann Beschluss über L3 |
| Tiefensortierung (`computed_zorder=False`) bei streifender Sicht fehlerhaft | Punkte scheinbar falsch verdeckt | AN1(d) Sichtprüfung; bei Punktwolke ohne Flächen unkritisch; Hinweis in Zeichenerklärung nicht nötig |
| Eigene Maus/Zoom kollidiert mit mplot3d-Interna (`zoom` geht bei `draw` verloren, `disable_mouse_rotation` wirkungslos) | Steuerung unbrauchbar | AN1(a) vor AN4/AN6; Rückfall: `scroll_event`-Handler setzt Box-Aspekt vor jedem Draw |
| Fachliche Lücke 3D-relativ (F-A2) | falsche Bewegung bei 3D mit relativem Bezug | Klärung durch `strukturdynamik-experte` vor dem 3D-relativ-Teil von AN3; bis dahin nur Einzelkomponente relativ und 3D absolut |
| M12 offen, R-070 nicht umgesetzt: Komponenten nicht im Geometrie-KS bestätigt | Bewegungsrichtung kann falsch sein | Kennzeichen „M12“ dauerhaft im Kopf und Bild (FG-04 3.4); keine Aussage über Richtung ohne Kennzeichen |
| Auslenkung vs. Schnelle vermischt (Zeitnullpunkt um T/4) | Phase der Bewegung ≠ dargestellte Phase | Kern-Tests RF-A1/A13; Beschriftung der Größe in Kopf, Bild und Textalternative; Voreinstellung Auslenkung |
| Geteilte Datei `auswerten_reiter.py` mit P-AUSW2 (S4 Refaktor) | Merge-Konflikte, Regression | AN7 erst nach S4; nur ein schreibender Agent; bisherige GUI-Tests als Messlatte |
| Drei Kanalpaare im Speicher (LRU 3) bei vier offenen Messungen | +28 MiB je Messung, Messrechner-RAM unbekannt | `setze_groesse(3)` nur für die **aktive** Messung im Modus Animation; `speicher_messen.py` aus P-AUSW2 deckt es ab |
| Kohärenz-Paare im Hauptthread: Wartezeit beim ersten Wechsel in den Modus | Oberfläche friert kurz ein | Messung in AN3, bei >400 ms gestaffelte Berechnung (E-A10) |
| Überhöhung s wechselt mit der Linie (automatisch), Nutzer liest Auslenkung falsch | falsche Aussage über Verformung | Zahl im Bild und Kopf; Hinweis bei Wechsel einer automatischen Überhöhung (FG-04 3.5); optional fester Wert |
| Mindestzoom/Rad auf dem Messrechner (HiDPI, Touchpad) liefert andere Schrittweiten | Zoom zu träge/zu sprunghaft | Faktor je Raste in einer Konstante; Prüfanleitung enthält den Punkt |
| Divergierende Skala ist in Graustufen oder bei Rot-Grün-Schwäche schwer lesbar | UI-20-artige Abnahme scheitert | Luminanztest, Abnahme `ui-designer` mit Graustufenumsetzung |
| Kennzeichnung (a) bis (d) aus FG-04 3.5 wird beim Speichern abgeschnitten | falsche Aussage im Bild | Test auf Texte in Figure **und** auf Platz im gespeicherten Bild (Textboxen innerhalb der Figure) |

### 13 Nicht enthalten

R-070 (Koordinatentransformation), R-072 (PSV-Visualisierungen); Video/GIF; Verbindungslinien und Flächen zwischen Punkten (keine Geometrie im Datenmodell, F-A6); Verschieben (Pan) im 3D-Bild; getrennte z-Streckung (F-A5); Quelle H1 in der Oberfläche (Kern kann es, F-A7); Animation von Zeitdaten; GL-Bibliotheken und Variante (c) (L3); Thesis-Skript für ein 3D-Standbild in `darstellung_beispiel.py` (nur auf Wunsch, Brief A-7); Änderungen am Reiter „Messen“; Auslieferung (Versionsnummer, Wheelhouse) und Commits.

### 14 Offene Fragen

**Blockierend (nur für den genannten Teilschritt, der Start von AN1 bis AN2 ist frei):**
- **F-A2 (Fachfrage, 3D mit relativem Phasenbezug).** FG-04 definiert ŵ = v̂ · v̂_b*/|v̂_b| für einen Skalar. Welcher Skalar gilt für einen 3D-Bezugspunkt? Vorschlag: Phase der **betragsgrößten Komponente** von v̂_b (M8-unabhängig, erhält alle Komponenten- und Punktbeziehungen); Alternative: Phase der großen Halbachse der Bahnellipse (aufwendiger, bei Kreisbahn unbestimmt). *Auswirkung:* nur der Zeitnullpunkt der 3D-Animation; Form und Phasendifferenzen bleiben. *Annahme bis zur Klärung:* AN3 liefert Einzelkomponente relativ und 3D **absolut**; 3D relativ erst nach Antwort des `strukturdynamik-experte`.

**Nicht blockierend (Annahme gilt, bis geklärt):**
- **F-A1 UI-25, Auslegung „Standbild identisch mit Animationszustand“.** *Annahme:* Standbild = das gespeicherte/angezeigte Bild des Modus Animation bei Winkel φ (dieselbe Funktion, dieselben Daten) **und** Konsistenz mit der 2D-Phasenansicht über die Phase (arg ŵ = `phase_relativ_rad`, θ_max = π/2 − φ). Der 2D-Modus „Standbild“ zeigt keine Auslenkung, ein Pixelvergleich ist nicht gemeint.
- **F-A3 Tastenbelegung** (Widerspruch im Brief, Abschnitt 5.2). *Annahme:* ←/→ Phase, Umschalt+Pfeile und ↑/↓ Drehen.
- **F-A4 UI-22 „bei Frequenzwechsel Standbild“.** *Annahme:* wörtlich: Modus springt auf „Standbild“ zurück. Alternative: Modus „Animation“ bleibt, Wiedergabe pausiert, θ = 0. Für das Durchschalten mehrerer Frequenzen wäre die Alternative bequemer.
- **F-A5 z-Streckung.** *Annahme:* keine (Gleichmaßstab), Regler „Überhöhung“ genügt. Eine optionale zweite Streckung (im Bild gekennzeichnet) kostet ca. 0,5 Tage.
- **F-A6 Verbindungslinien/Flächen.** *Annahme:* nicht enthalten; bräuchten Geometrie aus der Datei oder eine Dreiecksvermaschung (ohne `scipy`, ADR-017).
- **F-A7 Quelle H1 (m/N) in der Oberfläche.** *Annahme:* nur CPH in der Oberfläche; der Kern rechnet H1 schon (RF-A1).
- **F-A8 Voreinstellungen** Bildrate (10/s), Tempo (0,25 Perioden/s), Schrittweite (10° = 36 Bilder, E3): vorläufig bis zur Messung am Messrechner (U-A2).
- **F-A9 Farbkomponente bei 3D.** *Annahme:* die Achse senkrecht zur Projektionsebene; wählbar über ein Auswahlfeld, falls der Nutzer eine andere will.
- **F-A10 Reihenfolge** (Abschnitt 11): Qt-freie Vorarbeit parallel zu P-AUSW2 Etappe B/C oder komplett danach? *Empfehlung:* Parallel nur AN1 bis AN5; AN6/AN7 nach S4/S7.
- **Rechercheaufträge (aus FG-04, nicht blockierend):** RA-1 (welche Größe, Skalierung und Darstellung ungültiger Punkte PSV animiert; Vergleichsbasis für die Abnahme am Gerät), RA-2 (Definition ODS gegen Eigenform für die Thesis).

**Fragen an die Hardware-Prüfung (Nutzer):** Arbeitsspeicher des Messrechners (aus P-AUSW2 offen); ob die Animation über Remotedesktop flüssig genug ist (UI-38); ob die Voreinstellung Bildrate/Tempo passt.

### 15 Hinweis zu Review und Abnahme

Fachabnahme `strukturdynamik-experte` nach AN3 (und AN2-Tests); Reviewer nach AN4 (Zeichenfunktion), AN6/AN7 (Interaktion, geteilte Datei) und am Ende (AN9); Design-Abnahme `ui-designer` nach AN7 (AH, Farbskala, Kennzeichen, Graustufen) und AN9; Hardwaretest UI-38 durch den Nutzer nach Prüfanleitung.
