<!-- Plan P-ABB-S1 (software-engineer, sonnet), vom Nutzer am 2026-11-05 freigegeben: Empfehlungen D1 A (Skript erweitern), D2 Abbruch bei git_dirty mit --erlaube-dirty, D3 Ausgabe zuerst außerhalb des Repos, D4 <Stem>_<Abbildung> in in_progress/thesis/abbildungen/<Stem>/, D5 Format beide. Q1: endgültige Abbildungen in der Cloud aus der ins Repo gelegten .svd, am Messrechner nur Vorschau. Q2–Q6: Annahmen des Plans gelten. -->

## Plan: Thesis-Abbildungen aus einer neuen .svd (P-ABB-S1, Planungspaket, nichts geändert, nichts committet)

Gelesen: `KONVENTIONEN.md` (Abschnitte Messdaten, Abbildungen, Polytec, Thesis-Formalien), `in_progress/README.md`, ADR-021, ADR-024, ADR-025, ADR-026, `darstellung_beispiel.py`, `darstellung/` (`bild.py`, `zeichnung.py`, `stil.py`, `auswahl.py`, Teile von `schwingform.py`), `auswertung/` (`laden.py`, `jobs.py`, `baender.py`, `svd_lesen.py`, `export.py`, `annahmen.py`), `protokoll/version.py` und die vorhandenen Tests.

**Kernbefund:** Der Auftrag ist größtenteils schon gebaut. `software/tools/auswertung/darstellung_beispiel.py` erzeugt alle vier Ansichten mit `THESIS_STIL`, ohne Stempel und mit Begleitdatei. Ich habe es mit der Beispieldatei laufen lassen, die Ausgabe ging in den Scratchpad, nicht ins Repo. Der Lauf mit `--punkt-label 132 --format png` dauerte 5,5 s und lieferte 5 Bilder und 5 `.json`. Die Begleitdatei enthielt `software_git_hash` ec31e8e8…, `software_git_dirty: false` und `messdatei_sha256` 7ef46262…. Es fehlt also nur eine Erweiterung der Bedienung und der Herkunftsdaten (siehe 1.2), kein Neubau.

---

### 1. Bestandsaufnahme

**1.1 Vorhanden und wiederzuverwenden**

| Baustein | Leistung |
|---|---|
| `tools/auswertung/darstellung_beispiel.py` | `erzeuge_figuren` (alle 4 Ansichten, `schwingform` als 3D-Betrag und `schwingform_phase` als Z-Phase relativ zum Bezugspunkt, M8-unabhängig) und `schreibe_abbildungen` (PNG oder PDF je Bild plus `.json` mit Skript, Messdatei, SHA-256, Git-Hash, `git_dirty`, Linienzahl, Achsentitel, Hinweise). Es prüft vor dem ersten Schreiben alle Ziele (kein Überschreiben, keine Teilausgabe), meldet fehlende Phase mit Grund auf stderr und hat die Parameter `--punkt-label`, `--frequenz-hz`, `--format png\|pdf`. |
| `darstellung/` | Zeichenfunktionen `zeichne_spektrum`, `zeichne_frf`, `zeichne_spitzen`, `zeichne_schwingform` ohne Qt und ohne pyplot. `THESIS_STIL` (Graustufen, 9 pt, Dezimalkomma), `neue_figure`, `kennzeichen_kopf`. `auswahl.py` liefert `PaarCache`, `kanalpaare`, `frf_daten`, `spitzen_daten_*`, `schwingform_daten`, `standard_bezug`. M6-ungültige Punkte (Raute ohne Pfeil), Punkte mit γ² < γ²_min und die Kennzeichen sind im Zeichner umgesetzt (ADR-025). |
| `auswertung/` | `lade_svd` (SHA-256, Leser, Adapter, `LadeFehler`), `sha256_datei`, `Annahmen` (Voreinstellung γ²_min = 0,9, `gueltig=None` heißt alle Punkte gültig), Bänder und Spitzen. Der Leser ist in der Beispieldatei gegen PSV geprüft. |
| `protokoll/version.py` | `ermittle_build_info()` liefert Hash und `git_dirty` per Git oder aus `_build_info.json` im Wheel. |
| Tests | `tests/darstellung/test_dar_beispielskript.py` (synthetisch, Überschreibschutz, Herkunft) und `test_dar_datei.py` (Beispieldatei mit PSV-Referenzen, u. a. PSV-CPH an Label 132 und AVGSEQ-Mittel; Toleranz rtol 1e-5, atol 1e-6·max|Größe|, M11). `pythonpath` und Coverage enthalten `tools/auswertung` schon. |

**1.2 Was fehlt (nur das wird gebaut)**
1. **Bedienung:**
   - Das Kanalpaar ist fest `paare[0]`.
   - Die Phasenkomponente ist fest `Z`.
   - Der Bezugspunkt ist fest `standard_bezug`.
   - Es gibt nur ein Format je Lauf.
   - Ein unbekanntes Label gibt `SystemExit`. `LadeFehler` und `DarstellungsFehler` aus `lade_svd` und beim Zeichnen sind in `main` nicht gefangen und enden als Traceback.
2. **Herkunft:**
   - Es gibt nur je eine `.json` pro Bild, keine Gesamtdatei.
   - Die Parameter des Laufs fehlen (Paar, Punkt, Frequenz, Bezug, Komponente, Format, Aufruf).
   - Die Annahmen mit ihrem Status (M8 offen) und γ²_min fehlen.
   - Die Zahl der M6-ungültigen Punkte und der Punkte mit γ² < γ²_min steht nur bei der Phase in der Begleitdatei.
   - Es fehlen Paketversion und Quelle des Hashes (`git` oder `build_info`).
3. **git_dirty und fehlender Hash:** Beides wird nur in die Begleitdatei geschrieben, ohne Reaktion.
4. **Schutz der Ablage:** Die Ausgabe nach `Input/` oder unter `PyCharmProject` wird nicht abgewiesen.
5. **Dateinamen:** Sie lauten `darstellung_<name>.<fmt>` und tragen weder Messdatei noch Paar. Zwei Messdateien im selben Ordner kollidieren, und der Überschreibschutz bricht dann ab.
6. **Reproduzierbarkeit:** Ein PDF trägt von matplotlib standardmäßig einen Erstellungszeitstempel (Annahme aus Kenntnis von matplotlib, noch nicht am Skript geprüft).
7. **Abgrenzung:** `tools/auswertung/abbildungen.py` (pyplot, eigene Zeichenlogik, Export-basiert) bleibt unverändert. ADR-024 sieht die Migration später vor, sie ist nicht Teil dieses Pakets.
8. **Eigenheiten der Beispieldatei:** Die Kanalnamen der Montagsdatei sind unbekannt (Vib X/Y/Z, Ref1, Ref2 in der Beispieldatei). Das Skript darf keine festen Namen voraussetzen, außer als Voreinstellung.

---

### 2. Plan (Umsetzung ist mittel und braucht Freigabe)

**Ansatz:** Das vorhandene Skript bleibt der Kern und wird erweitert (Alternativen in Abschnitt 6, D1). Die Zeichnung bleibt die gemeinsame Zeichenfunktion aus `darstellung/`. Es gibt keine neue Mathematik, kein Diff in `src/`, keine GUI-Änderung. Das Skript fügt nur Bedienung, Herkunft und Schutzregeln hinzu.

**Schritte** (riskanteste Annahme zuerst, jeder Schritt einzeln lauffähig):

1. **Prüfung des Dirty-Risikos (Risikoschritt).** Zeigen, dass `ermittle_build_info` den ganzen Arbeitsbaum prüft. Das Skript wird in einem temporären Klon des Repos an der Beispieldatei zweimal mit Ausgabe innerhalb des Repos gestartet. Erwartung (aus Git-Semantik, noch nicht belegt): Der zweite Lauf meldet `git_dirty = true`, weil die ersten Bilder als „untracked“ zählen. *Verifiziert durch:* Testlauf im Klon im Scratchpad. Das Ergebnis entscheidet D2.
2. **CLI erweitern** in `darstellung_beispiel.py`:
   - `--antwort` und `--referenz` (Voreinstellung: erstes Paar der Datei, wie heute).
   - `--komponente X|Y|Z` für die Phase (Voreinstellung Z).
   - `--bezug-label` (Voreinstellung `standard_bezug`).
   - `--format png|pdf|beide`.
   - `--erlaube-dirty`.
   - Die bestehenden `--punkt-label` und `--frequenz-hz` bleiben, ebenso `--ausgabe`.
   - Alle Fehlerfälle gehen auf eine lesbare Meldung mit Exit-Code statt Traceback.

   *Verifiziert durch:* Tests mit synthetischen Daten (`dar_daten.synthetische_messdaten`), je Parameter ein Fall.
3. **Ablageschutz und Dateinamen.** Eine Ausgabe unter `Input/` oder in einem Pfad mit der Komponente `PyCharmProject` (Groß-/Kleinschreibung egal) wird mit Exit 2 abgelehnt. Das Namensschema wird `<Messdatei-Stem>_<abbildung>.<fmt>` (D4). Der Überschreibschutz bleibt (alle Ziele vor dem ersten Schreiben prüfen). *Verifiziert durch:* Tests für beide Pfadregeln, Doppellauf und Teilausgabe.
4. **Git-Regel (D2/D3).** `ermittle_build_info()` wird einmal am Anfang aufgerufen, vor dem Schreiben.
   - Hash `None`: Abbruch mit Exit 2.
   - `git_dirty` ist `True` oder `None` (unbekannt): Abbruch mit Exit 2 und Hinweis. Mit `--erlaube-dirty` läuft das Skript weiter. Dann steht `git_dirty: true` (bzw. `null`) im Manifest und in jeder Begleitdatei, und die Konsole zeigt eine Warnung.
   - Liegt die Ausgabe im Arbeitsbaum, warnt das Skript, dass der nächste Lauf dadurch „dirty“ wird (siehe D3).

   *Verifiziert durch:* Tests mit eingespielter `BuildInfo` (monkeypatch auf `ermittle_build_info`), alle vier Fälle (sauber, dirty, `None`, `build_info`-Quelle).
5. **Manifest und Begleitdaten.** Neben den Einzeldateien entsteht `<stem>_manifest.json` mit diesen Feldern:
   - Skript, Aufruf (argv).
   - Messdatei (Name, Größe, SHA-256).
   - `software_git_hash`, `git_dirty`, Quelle (`git` oder `build_info`), Paketversion.
   - Alle Parameter des Laufs.
   - Annahmen mit Status (M8 offen) und γ²_min.
   - Je Abbildung: Dateien, Linienzahl, Hinweise.
   - `ausgelassen: {abbildung: grund}`.
   - Anzahl M6-ungültiger Punkte und Anzahl Punkte mit γ² < γ²_min.
   - Zeitstempel `erzeugt_utc`. Er steht nur im Manifest und wird im Determinismus-Test ausgenommen.

   Die Einzel-`.json` bleibt erhalten, damit das Format der bestehenden Dateien sich nicht ändert (Felder werden nur ergänzt). Zusätzlich schreibt `savefig(metadata=…)` den Hash in die Bilddatei und unterdrückt im PDF `CreationDate`. *Verifiziert durch:* Test der Felder, Test „zweimal erzeugen in zwei Ordnern: PNG bitgleich, PDF bitgleich ohne Zeitstempel“ (Falls matplotlib trotzdem Unterschiede liefert, wird die Gleichheit auf die Begleitdaten beschränkt und das berichtet).
6. **Verhalten bei fehlenden Kanälen und Punkten.**
   - Fehlt ein explizit gewählter Kanal, ein Paar, ein Punkt-Label oder ein Bezugspunkt, bricht das Skript mit Exit 2 ab. Es nennt die vorhandenen Paare bzw. Labels.
   - Fehlt die Referenz in der Datei, entfallen FRF und Phase. Das steht im Manifest unter `ausgelassen` und auf stderr. Der Exit-Code bleibt 0, weil das erwartet ist.
   - Ist eine gewählte Phasenabbildung nicht darstellbar (z. B. kein Punkt mit γ² ≥ γ²_min als Bezug), entfällt sie mit Grund, der Exit-Code ist 3. Die übrigen Bilder werden geschrieben.

   *Verifiziert durch:* Tests je Fall (`referenz=False`, falsches Paar, falsches Label, unmöglicher Bezug).
7. **Abweichungen im Bild.** Das Verhalten der Zeichenfunktionen bleibt, es wird nur im Manifest belegt. M6-ungültige Punkte und Punkte mit γ² < γ²_min bleiben im Bild und sind gekennzeichnet. Die Pfeile bleiben konstant lang (ADR-025). Mit `Annahmen.gueltig = None` gelten alle Punkte als gültig, und das Manifest sagt das ausdrücklich. *Verifiziert durch:* Test mit Messdaten, in denen ein Punkt `gueltig = False` hat und ein Punkt γ² < 0,9: Rauten und Pfeile im Bild (über `Zeichnung.marker`) und Zahlen im Manifest.
8. **Test an der Beispieldatei** (Abschnitt 4). Danach die Standard-Prüfung aus `KONVENTIONEN.md`: `ruff check`, `ruff format --check`, `mypy --strict`, `pytest --cov --cov-fail-under=90`.
9. **Kurze Anleitung** (Aufruf, Exit-Codes, Ablage) im Docstring des Skripts. Keine neue Datei, keine Änderung der Thesis.

**Annahmen:** (a) Die Montagsdatei ist ein gewöhnliches PSV-3D-FFT-File derselben Version wie die Beispieldatei, der Leser liest sie ohne Anpassung. (b) Der Nutzer legt sie als Rohdatei ab (Frage Q1). (c) Die Abbildungen sollen für die Thesis nur mit relativer Phase entstehen, solange M8 offen ist (bestehende Regel, ADR-025).

**Risiken:** Der Leser könnte an der Montagsdatei scheitern (andere Version, andere Kanäle). Das Skript meldet dann `LadeFehler` im Klartext, und der Fall wird an den Orchestrator zurückgemeldet. Ferner kann der Dirty-Effekt (Schritt 1) die Erzeugung im Repo erschweren (D3). Beide Risiken sind in den Schritten 1 und 6 abgedeckt.

**Nicht enthalten:** PSV-Vergleich; GUI-Änderung; Migration von `abbildungen.py` (ADR-024); Änderungen in `src/`; neue Zeichen- oder Rechenfunktionen; neuer THESIS_STIL; Wheel-Neubau (nur bei D1 = C).

---

### 3. Aufruf, Ausgabe, Ablage

**Aufruf** (aus `software/`; auf dem Messrechner mit dem Python der venv, nicht unter PyCharmProject):
```
uv run python tools/auswertung/darstellung_beispiel.py <messdatei.svd> --ausgabe <ordner>
    [--antwort "Vib Z" --referenz Ref1] [--punkt-label N] [--frequenz-hz F]
    [--komponente X|Y|Z] [--bezug-label N] [--format png|pdf|beide] [--erlaube-dirty]
```
**Exit-Codes:** 0 alles erzeugt (oder erwartungsgemäß ausgelassen), 2 Abbruch (Eingabe, Pfad, Git), 3 Abbildung entfällt trotz Erwartung (übrige geschrieben).

**Ausgabe** je Lauf, im Ordner `<ausgabe>/`:
- `<stem>_spektrum`, `_frf`, `_spitzen`, `_schwingform`, `_schwingform_phase` mit `.png` und/oder `.pdf`.
- Je Bild eine `<name>.json`.
- `<stem>_manifest.json`.

**Ablageort:** Endgültige Abbildungen nach `in_progress/thesis/abbildungen/<stem>/` (laut `KONVENTIONEN.md`; der Ordner existiert noch nicht und wird beim ersten Lauf angelegt). Rohdaten bleiben unverändert: `lade_svd` öffnet nur lesend, und ein Test prüft den SHA-256 vor und nach dem Lauf. Eine Ausgabe unter `Input/` und unter `PyCharmProject` wird abgelehnt. Messdaten und Skriptausgaben auf dem Messrechner liegen in einem Ordner außerhalb von `PyCharmProject` (der Ordner ist Frage Q2).

**Wo es läuft:**
- **Beispieldatei und Entwicklung:** in der Cloud (belegt: Lauf offline in 5,5 s, `uv run`).
- **Montagsdatei:** Dort entsteht zuerst eine Vorschau am Messrechner mit dem installierten Paket 0.2.0. Die Skripte unter `tools/` liegen nicht im Wheel und werden separat kopiert (Stick, wie `zeiten_messen.py`). Die endgültigen Thesis-Abbildungen werden mit sauberem Git-Hash neu erzeugt. Das steht auch im TODO („Abbildungen mit sauberem Git-Hash neu erzeugen“). Dafür muss die Rohdatei in die Cloud (Frage Q1).
- **Abhängigkeiten:** `numpy`, `matplotlib` (nur `Figure`, kein Backend nötig, kein pyplot), `olefile` und das Paket `ldv_automation`. Alle sind im Wheel 0.2.0 samt Wheelhouse enthalten. Nicht nötig sind Qt, pywin32 und Git. Auf dem Messrechner stammt der Hash aus `_build_info.json` (Wheel a0ee2fc…, `git_dirty: false`, laut `stick/LIESMICH.txt`). Er bezeichnet dann den Stand der Software im Wheel, nicht des Skripts. Das Manifest nennt deshalb die Quelle (`build_info`) und die Paketversion.

---

### 4. Testplan

Neue Tests kommen in `tests/darstellung/test_dar_beispielskript.py`. Die Tests für die Beispieldatei kommen dazu in `test_dar_datei.py`; sie werden bei fehlender Datei übersprungen (wie bisher). Toleranzen sind explizit und begründet.

- **Synthetisch** (`synthetische_messdaten`): alle Parameter und Fehlerfälle aus den Schritten 2 bis 7, außerdem Format `beide`, Namensschema, Überschreibschutz und Ablage unter `Input/` bzw. `PyCharmProject`.
- **Beispieldatei, Referenzwert (Golden Label 132):** `main([...,"--punkt-label","132"])` bzw. `erzeuge_figuren(punkt_label=132)`. Die Spektrum-Kurve an Label 132 wird gegen das PSV-CPH (dieselbe Referenz wie `test_rf_ui_f2c_label_132_ist_der_psv_cph`) verglichen. Toleranz rtol 1e-5, atol 1e-6·max|Größe| (FG-02 Abschnitt 8, M11). Das Punktmittel wird gegen das PSV-AVGSEQ verglichen (wie vorhanden).
- **Beispieldatei, Invarianten (zweite Methode):** SHA-256 der Rohdatei vor und nach dem Lauf gleich; Manifest-SHA gleich `sha256_datei`; zwei Läufe in zwei Ordnern liefern gleiche Begleitdaten (ohne `erzeugt_utc`) und gleiche Bilddateien (Grenzen siehe Schritt 5); Linienzahlen und Achsentitel gleich den Oberflächen-Zeichnungen (wie `test_figuren_mit_referenz…`).
- **Nicht prüfbar ohne Referenz:** Die Lesbarkeit der Bilder im Druck und das Aussehen sind unverifiziert. Ich schlage eine Sichtprüfung der fünf PNG durch den Nutzer vor (Bildunterschrift auf A5, kein Gelb, Graustufen). Phase absolut gegen Ref1 bleibt unbestätigt (M8).

---

### 5. Akzeptanzkriterien (prüfbar)

- **A1:** Aus `Input/20261012_ref_Mitte.svd` entstehen mit `--ausgabe <ordner> --punkt-label 132 --format beide` fünf Abbildungen als PNG und PDF (`spektrum`, `frf`, `spitzen`, `schwingform`, `schwingform_phase`), Exit-Code 0.
- **A2:** Alle Bilder entstehen über die Zeichenfunktionen in `darstellung/` mit `THESIS_STIL`, ohne Diagrammtitel und ohne Stempel „Arbeitsansicht“ (Test: `figure.texts` leer, kein Text „Arbeitsansicht“).
- **A3:** `<stem>_manifest.json` enthält die Felder aus Schritt 5. `software_git_hash` ist 40-stellig, `messdatei_sha256` ist gleich `sha256_datei(Messdatei)`.
- **A4:** Bei `git_dirty = true`, `null` oder fehlendem Hash bricht der Lauf mit Exit 2 ab und schreibt nichts. Mit `--erlaube-dirty` entstehen die Bilder und das Manifest trägt `git_dirty` (außer bei fehlendem Hash, der immer abbricht).
- **A5:** Bei `--antwort`/`--referenz` für ein Paar ohne Kreuzspektrum, bei einem unbekannten `--punkt-label` oder `--bezug-label` und bei unlesbarer Datei endet das Skript mit Exit 2 und einer Meldung ohne Traceback, die verfügbare Paare bzw. Labels nennt.
- **A6:** Ohne Referenzkanal entstehen `spektrum`, `spitzen` und `schwingform`. Das Manifest führt `frf` und `schwingform_phase` unter `ausgelassen` mit Grund.
- **A7:** Ein Punkt mit M6 = ungültig und ein Punkt mit γ² < 0,9 bleiben im Bild und sind gekennzeichnet. Das Manifest nennt beide Anzahlen.
- **A8:** Eine Ausgabe unter `Input/` oder unter einem Pfad mit `PyCharmProject` wird mit Exit 2 abgelehnt. Eine vorhandene Zieldatei wird nicht überschrieben, es entsteht keine Teilausgabe.
- **A9:** Die Rohdatei bleibt unverändert (SHA-256 vor und nach dem Lauf gleich).
- **A10:** Das Skript importiert nur `numpy`, `matplotlib` (ohne `pyplot`), `olefile` und `ldv_automation`.
- **A11:** Die Standard-Prüfung aus `KONVENTIONEN.md` läuft fehlerfrei (Abdeckung ≥ 90 %).
- **A12:** Die Spektrumkurve an Label 132 stimmt innerhalb der Toleranz mit dem PSV-CPH überein.

---

### 6. Entwurfsentscheidungen mit Alternativen (für mögliche ADR)

**D1 – Wo liegt die Logik?**
| Alternative | Vorteile | Nachteile |
|---|---|---|
| A: `darstellung_beispiel.py` erweitern (Empfehlung) | kleinster Diff, bestehende Tests bleiben, kein Wheel-Neubau, am Montag nutzbar | Name „Beispiel“ passt nicht mehr; Skript muss separat auf den Messrechner kopiert werden |
| B: neues Skript `thesis_abbildungen.py`, das `erzeuge_figuren` importiert | sprechender Name | tools-Skript importiert tools-Skript; zwei Dateien kopieren |
| C: Logik als Paketmodul in `darstellung/`, dünnes Skript | im Wheel enthalten, `python -m …` ohne Kopieren | neues Wheel mit neuer Versionsnummer (Konvention), `src/`-Änderung, mehr Aufwand und Review |

**D2 – Verhalten bei `git_dirty` / fehlendem Hash**
| Alternative | Vorteile | Nachteile |
|---|---|---|
| Abbruch, überschreibbar mit `--erlaube-dirty` (Empfehlung) | eine Thesis-Abbildung ohne eindeutigen Stand entsteht nicht aus Versehen | Vorschau am Messrechner braucht den Schalter, wenn dort `git_dirty` nicht `false` ist |
| nur Warnung und Eintrag in der Begleitdatei | einfach | Abbildungen mit unklarem Stand können unbemerkt in die Thesis gehen |
| Kennzeichen im Dateinamen (`_dirty`) | auf einen Blick sichtbar | ändert Dateinamen; LaTeX-Verweise müssten angepasst werden |

**D3 – Dirty durch die eigene Ausgabe (nach Schritt 1 zu bestätigen)**
| Alternative | Vorteile | Nachteile |
|---|---|---|
| Ausgabe zuerst außerhalb des Arbeitsbaums (Scratchpad/Messrechner), danach kopieren und committen (Empfehlung) | `ermittle_build_info` bleibt unverändert, Hash gehört zum erzeugenden Stand | ein Kopierschritt; das Skript warnt, falls die Ausgabe doch im Repo liegt |
| Pfadfilter in `ermittle_build_info` (ignoriert `in_progress/`) | direkte Ausgabe ins Repo möglich | `src/`-Änderung an der zentralen Versionsfunktion, Auswirkung auf Messprotokolle |
| Hash am Start einmal lesen, Mehrfachläufe zulassen | kein Eingriff | nur der erste Lauf ist „sauber“, danach ist der Hash des nächsten Laufs unzuverlässig |

**D4 – Dateinamen und Ordner:** `<stem>_<abbildung>` in `…/abbildungen/<stem>/` (Empfehlung) gegen das heutige `darstellung_<abbildung>` (kein Umbenennen, aber Kollision bei mehreren Messdateien) gegen Zeitstempel im Namen (eindeutig, aber nicht reproduzierbar). Das ist eine Konventionsfrage, kein eigenes ADR nötig (Vorschlag für `KONVENTIONEN.md`, siehe unten).

**D5 – Formate:** `beide` (PDF für LaTeX, PNG als Vorschau) als Voreinstellung gegen nur PDF gegen nur PNG. Das Skript soll die Wahl der Voreinstellung zulassen. Siehe Q3.

---

### 7. Offene Fragen an den Nutzer

- **[blockierend für die Wahl in D1]** Q1: Wo liegt die Montags-.svd, und wo sollen die endgültigen Abbildungen entstehen? Annahme: Die Datei wird vom Nutzer in `Input/` (oder `in_progress/versuche/<datum>/`) abgelegt und die endgültigen Abbildungen entstehen in der Cloud mit sauberem Hash. Am Messrechner entsteht nur eine Vorschau. Wird stattdessen am Messrechner endgültig erzeugt, bleibt der Hash der des Wheels, und D1 = C wäre zu prüfen.
- **[nicht blockierend]** Q2: Welchen Ordner außerhalb von `PyCharmProject` soll das Skript am Messrechner als Ziel nutzen? Annahme: Der Nutzer gibt ihn über `--ausgabe` an, es gibt keinen festen Ordner im Code.
- **[nicht blockierend]** Q3: PNG, PDF oder beide? Annahme: `beide`.
- **[nicht blockierend]** Q4: „mit Git-Hash“ heißt Begleitdatei plus Bilddatei-Metadaten, nicht sichtbar im Bild. Annahme laut ADR-024 (Thesis ohne Stempel) und `KONVENTIONEN.md` („Jede Ausgabe nennt das erzeugende Skript und den Git-Hash“). Soll der Hash sichtbar im Bild stehen?
- **[nicht blockierend]** Q5: M6-ungültig kann nur über die Annahmen gesetzt werden. Die `.svd` liefert den PSV-Punktstatus nicht (der Leser liest keine Statusfelder, `punkte.statusfelder` offen). Das Skript kennt deshalb keinen M6-Schalter, und das Manifest vermerkt „alle Punkte gültig“. Soll ein `--ungueltige-labels` ergänzt werden? Annahme: nein, weil nicht verlangt.
- **[nicht blockierend]** Q6: Im Repo liegen ISONORM-Schriften unter `Input/Templates/`, `THESIS_STIL` nutzt DejaVu Sans. Ob die Abbildungsschrift an die Vorlage angepasst werden soll, ist nicht Teil dieses Pakets. Soll das als eigenes Paket aufgenommen werden?

---

## Rückmeldung an den Orchestrator

**Paket:** P-ABB-S1 · **Status:** PLAN ZUR FREIGABE

**Was geändert wurde:** nichts (read-only). Die Beispieldatei lief nur im Scratchpad (`/tmp/claude-0/-home-user/e6b61297-17fb-5003-91f8-95c4534d012c/scratchpad/abb/`), nicht im Repo.

**Wie verifiziert:** `uv run --offline python tools/auswertung/darstellung_beispiel.py ../Input/20261012_ref_Mitte.svd --ausgabe <scratchpad>/abb --punkt-label 132 --format png` lief in 5,5 s mit 5 PNG und 5 `.json`. Die Begleitdatei hatte `software_git_hash` ec31e8e8…, `software_git_dirty: false` und SHA-256 der Eingabedatei 7ef46262…. Die Bilder habe ich nicht angesehen. Die Test-Suite und die Standard-Prüfung habe ich nicht ausgeführt.

**Akzeptanzkriterien:** A1 bis A12 sind im Plan definiert, noch nichts davon umgesetzt.

**Annahmen:** (a) Die Montagsdatei ist lesbar wie die Beispieldatei. (b) Der Nutzer legt sie ab (Q1). (c) Die Phase erscheint in den Thesis-Abbildungen nur relativ zum Bezugspunkt, M8 bleibt offen. (d) „mit Git-Hash“ meint Begleitdatei und Metadaten, nicht ein sichtbares Bildmerkmal (Q4). (e) Der Dirty-Effekt durch Ausgabe im Repo ist aus Git-Semantik abgeleitet und wird in Schritt 1 belegt.

**Sichtbare Verhaltensänderungen und Risiken:** Dateinamen ändern sich (`darstellung_<name>` → `<stem>_<name>`), der bestehende Test `test_schreibe_abbildungen_mit_herkunft_und_ueberschreibschutz` wird entsprechend angepasst. Neu sind Abbruch bei `git_dirty`/ohne Hash und Ablehnung der Ausgabe unter `Input/` und `PyCharmProject`. Die Begleit-`.json` wird nur ergänzt. Risiko: Die Montagsdatei kann mit dem Leser scheitern (dann Meldung und Rückmeldung).

**Unverifiziert:** Bitgleichheit der PDF/PNG bei Doppellauf, Verhalten der Montagsdatei, Druckqualität der Bilder, Phase absolut (M8).

**Rückfragen:**
- [blockierend] Q1 Ort der Montags-.svd und der endgültigen Erzeugung (entscheidet D1: Annahme A, bei Erzeugung am Messrechner Prüfung von C). Siehe Abschnitt 7.
- [nicht blockierend] Q2 bis Q6, Annahmen jeweils in Abschnitt 7.

**Entwurfsentscheidungen (mögliche ADR):** D1 Ort der Logik, D2/D3 Git-Regel und Dirty durch eigene Ausgabe. D4/D5 sind Konventionen.

**Vorschlag für KONVENTIONEN.md:** (1) Thesis-Abbildungen liegen unter `in_progress/thesis/abbildungen/<Messdatei-Stem>/` mit Dateinamen `<Messdatei-Stem>_<abbildung>.<fmt>`, dazu `<Messdatei-Stem>_manifest.json`. (2) Abbildungen für die Thesis entstehen nur mit sauberem Git-Hash (`git_dirty = false`); Ausnahmen nur mit `--erlaube-dirty` und Kennzeichen in der Begleitdatei. (3) Das Abbildungsskript liegt unter `software/tools/auswertung/darstellung_beispiel.py` (der „genaue Pfad“ aus dem Abschnitt Abbildungen ist damit festgelegt).

**Review-Empfehlung:** Nach der Umsetzung Review mit Schwerpunkt Git-Regel (Schritt 4, alle vier Fälle), Ablageschutz (Schritt 3) und Manifest-Felder gegenüber den Zeichnungen. Eine Fachabnahme ist nicht nötig, weil keine neue Rechnung entsteht. Modell: normal reicht, die Aufgabe hat keine schwierige Numerik.