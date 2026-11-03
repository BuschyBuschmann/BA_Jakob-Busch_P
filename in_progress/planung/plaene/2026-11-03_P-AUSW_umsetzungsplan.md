<!-- Paket P-AUSW (software-engineer, sonnet). Status: FREIGEGEBEN vom Nutzer am 2026-11-03.
Nutzerentscheidungen zu Abschnitt 6:
- F-1 Bandgrenzen: zunächst ein Gesamtband (0,625 … 1000 Hz) ohne Eingabe; Eingabezeile später.
- F-2 Ansicht 1: beides wählbar, Voreinstellung |CPH| (kohärent), √AP als Alternative und automatisch ohne Referenz; je Größe eigene Mittelformel (|CPH|: mittel_betrag; √AP: mittel_quadratisch) – Fachanalyse FA-AUSW.
- F-3: zweistufiges Laden.
- F-4: Phase in Ansicht 4 nur für eine Einzelkomponente, zwei Optionen „Phase gegen Ref1 (⚠ unbestätigt, M8)“ und „Phase relativ zu Bezugspunkt“ (M8-unabhängig; Bezugspunkt = größtes |v| unter Punkten mit γ² ≥ γ²_min, im Kopf genannt); Darstellung als Pfeil je Punkt mit Kreislegende plus zyklische Farbskala (kein hsv/jet); Punkte mit γ² < γ²_min markiert, nicht gelöscht; Anzeige in Grad. Ansicht 2 „Mittel“: Phase-Platzhalter „für das Mittel nicht definiert“.
- N-1 bis N-11: Annahmen wie im Plan (u. a. Mittelung „plausibel“, Fenster „–“, dB deaktiviert, Kanalpaarwahl auch in Ansicht 3, Modenfit ohne Schaltfläche, Reiter lazy, Version 0.3.0).
- 3D-Mittel: Mittel der punktweisen 3D-Beträge, gekennzeichnet „nicht gegen PSV geprüft“.
Fachanalyse: in_progress/analysen/2026-11-03_FA-AUSW_spektrum-phase.md (Referenzfälle RF-UI-F2a … F4d werden Tests). -->

## Plan: Umsetzung der Auswertungsoberfläche K-AUSW (Paket P-AUSW, Typ Planung)

Es wurde nichts am Repository geändert. Alle Messungen und Prototypen liegen im Scratchpad `/tmp/claude-0/-home-user/e6b61297-17fb-5003-91f8-95c4534d012c/scratchpad/p-ausw/`:
- Skripte: `zeit1.py`, `zeit2.py`, `proto_pool.py`, `proto_pool2.py`, `proto_proc.py`, `pk.py`, `u3.py`, `band.py`, `b1.py`, `qt1.py`.
- Kopie der Beispieldatei: `ref.svd`.
- Probe-Lockfile in `lock/`.

Die Messungen stammen von diesem Linux-Container (4 Kerne, 2,8 GHz, Python 3.11, offscreen). Am Messrechner sind sie nicht bestätigt.

### 0 Kernbefunde

1. **Blockierendes Lesen reicht nicht.** UI-15 ist damit nicht erfüllbar.
   - Der Leser braucht 101 ms (warm) bis 780 ms (erster Lauf), SHA-256 etwa 90–140 ms.
   - Die Stufe-1-Auswertung `werte_aus` braucht 8,0–13,1 s bei 7 Kanalpaaren und 135 Punkten.
   - Die Schwelle aus dem Brief sind 200 ms.
2. **Der Zeitfresser ist die Plausibilitätsprüfung P-07.** Im Profil macht `p07_phasensinn` 12,4 von 14,5 s aus. Ein Paar (`werte_paar_aus`) braucht nur 246 ms (`bereite_paar` 44 ms, `berechne_frf` 193 ms), alle 7 Paare 1,6 s.
3. **Die ganze `Auswertung` darf nicht über eine Prozessgrenze.** Sie ist 247 MB groß, Pickle und Entpacken kosten je etwa 2 s. Ein reduziertes Paket war immer noch 109 MB und kostete 3,2 s Zusatzzeit. `Messdaten` sind nur 48,4 MB.
4. **Mittelung ist in der Datei lesbar, das Fenster nicht eindeutig.** Der Stream `Info/DAQ_Settings_Fft/Average` enthält int32 `[1, 2, 0, 7]`. Das passt zu Typ 2 (komplex) und Anzahl 7 aus File Access vom 02.11. Ein Fenstercode ist nicht zuordenbar (Details U-1).
5. **Der Leser liegt in `tools/` und ist nicht im Wheel.** Das Hauptpaket kann ihn am Messrechner nicht importieren (Details im nächsten Abschnitt).
6. **Zwei Brief-Annahmen stimmen nicht ganz.**
   - A-2: Es gibt kein „Mittel 3D“ im Rechenkern. Es gibt nur `betrag_3d_ap` und `mittel_ap`, die Kombination fehlt.
   - A-3: `Auswertung.annahmen_liste` liegt nicht vor der ersten Darstellung vor. Es gilt aber `Annahmen().eintraege()`, das ist dasselbe Objekt wie in `werte_aus`.
7. **Der Brief hat drei Lücken:**
   - keine Quelle für Bandgrenzen,
   - keine Kanalpaarwahl in Ansicht 3,
   - unklare Phase in Ansicht 4 und beim „Mittel“ in Ansicht 2.

   Die Fragen stehen in Abschnitt 6.

### 1 Klärung der Umsetzerfragen

**U-1 Mittelung und Fenster (OE-1)**

Fundstellen in `Input/20261012_ref_Mitte.svd` (Kopie im Scratchpad):

| Stream | Rohwerte | Deutung |
|---|---|---|
| `Average` (16 B) | int32 `[1, 2, 0, 7]` | Version 1; **Typ 2** = `ptcAverageComplex`; Feld 3 = 0 (offen); **Anzahl 7** |
| `Fft` (52 B) | Leser nutzt 44 B, Rest `00…00` | kein Fenster erkennbar |
| `Global`, `SignalEnhancement`, `Trigger`, `FrontEnd`, `Channels` | siehe unten | kein eindeutiges Fenster-Feld |

- **Mittelung:**
  - Typ 2 und Anzahl 7 stimmen mit den File-Access-Werten vom 02.11. überein (`ergebnisse_7b.md`, M5).
  - Der Enum-Bereich 0–4 schließt eine Vertauschung der Felder aus.
  - Alle Felder außer `Average` lassen den Wert 7 nicht als Mittelungsanzahl erkennen.
  - Offen bleibt: Beleg an nur einer Datei, die Bedeutung des Felds bei +8 ist unbekannt.
  - **Empfehlung:** anzeigen, im Leser als „plausibel“ eingestuft (nicht „gesichert“). Der Leser dekodiert strikt: Länge 16, Version 1, Typ 0–4, Anzahl ≥ 1. Sonst liefert er `None`, die GUI zeigt „–“ mit Tooltip.
  - Falls der Nutzer „nur gesichert“ verlangt: Mittelung ebenfalls „–“. Das ist eine Ein-Zeilen-Änderung.
- **Fenster:**
  - In File Access ist das Fenster eine Kanaleigenschaft (`ChannelAcqProperties.WindowFunction`), vermutlich im Stream `Channels` (3436 B, je Kanal ein Satz).
  - Das Fenster der Datei ist Rechteck, also Code 0. Dieser Wert steckt in allen Streams in sehr vielen Nullfeldern, ein Feld lässt sich nicht herausgreifen.
  - **Der Plan sagt deshalb „–“.** Der Leser bekommt kein Fenster-Feld, das wäre ein toter Platzhalter. Die Parameterzeile hat eine Konstante `FENSTER_IN_DATEI_LESBAR = False` samt Begründung, auf der ein Test besteht.
- **Was eine zweite Datei bräuchte:** Ein Diff aller Streams unter `Info/DAQ_Settings_Fft` kann die Felder festlegen. Dafür werden zwei Dateien gebraucht, die sich nur in einem Wert unterscheiden:
  - (a) gleiches Setup, nur Fenster Hanning (7), zusätzlich ideal Force (5) auf Ref1, falls das Fenster kanalweise gilt;
  - (b) gleiches Setup, nur Mittelung Count 10 und Typ Betrag (1).
  
  Mit (b) wird Mittelung zusätzlich „gesichert“. Der Diff-Befehl ist trivial, er steht im Plan als optionales Werkzeug.
- **R-032 ist damit nur teilweise erfüllt:** Mittelung ja (plausibel), Fenster „–“. Das geht als Befund an den Nutzer.
- **Durchzureichende Felder der Parameterzeile:**

| Zelle | Quelle |
|---|---|
| Bandbreite | `fft.bandbreite_hz` (bisher nicht durchgereicht) |
| Linien | `fft.linien` (bisher nicht durchgereicht) |
| Δf | `fft.delta_f_hz` (durchgereicht) |
| Mittelung | neues Leserfeld |
| Fenster | „–“ |
| Punkte | `len(punkte.index)` |
| Referenz | eindeutige zweite Kanäle in `Messdaten.cp` plus `einheiten`; hier „Ref1 [N], Ref2 [m/s²]“; ohne Referenz „keine“ (kein „–“, der Wert ist bekannt) |

Die Felder gehen als neues Objekt `Dateieinstellungen` nach außen. `Messdaten` bleibt unverändert, damit sich die Export-Formate nicht ändern.

**Zusatzbefund zum Leser:** Er liegt als Werkzeug in `software/tools/svd_analyse/svd_lesen.py`, `olefile` steckt nur in der Gruppe `werkzeuge`, und das Wheel packt nur `src/ldv_automation`. ADR-020 macht den Leser aber zum Hauptweg. Er muss deshalb ins Paket: `git mv` nach `software/src/ldv_automation/auswertung/svd_lesen.py` und `olefile` wird Hauptabhängigkeit.

Die Importzeilen müssen in diesen Dateien angepasst werden:
- `tools/svd_analyse/svd_pruefung.py`
- `tools/svd_analyse/kontrollplots.py`
- `tools/auswertung/beispiel_svd.py`
- `tests/tools/svd_analyse/test_svd_lesen.py` (nutzt private Namen wie `sl._i32`)
- `tests/tools/svd_analyse/svd_synth.py`
- `tests/auswertung/test_aw_golden_datei.py`

Eine Shim-Datei in `tools/` scheidet aus: mypy strict würde die privaten Namen verlieren.

**U-2 Laden ohne Einfrieren**

Messwerte:

| Messung | Wert |
|---|---|
| Lesen im Hauptprozess (3 Läufe) | 780 / 559 / 101 ms |
| SHA-256 | 137 / 86 / 96 ms |
| Adapter | 2 ms |
| `werte_aus`, 7 Paare | 13,1 / 9,2 / 8,0 s |
| mit 2 Bändern | 10,4 / 6,9 / 8,2 s |
| B-1-Modenfit, 1 Paar | 23,2 s |
| Lesen im Worker (inkl. Spawn, Importe, Übertragung) | 1,17 bis 2,29 s |
| Übertragung `Messdaten` | 48,4 MB |
| Prüfjob-Ergebnis (45 Prüfungen, 9 Annahmen) | 0,5 MB |
| RSS nach `werte_aus` | 741 MB |

- **Blockierend scheidet aus.** Selbst das reine Lesen liegt über der 200-ms-Schwelle, wenn der Cache kalt ist (Windows-Virenscanner nicht eingerechnet). Die Auswertung braucht 8–13 s.
- **Empfehlung: eigener Prozess, aber mit `multiprocessing.Process` und `Pipe` statt `ProcessPoolExecutor`.** Beides wurde prototypisch gemessen:
  - `ProcessPoolExecutor` funktioniert (Spawn 80 ms), hat aber drei Nachteile:
    - Ein laufender Auftrag lässt sich nicht beenden. Das Fensterschließen kann bis zu 10 s warten.
    - Beim Senden von 48 MB in den Worker entstand eine Lücke von 983 ms in der Hauptschleife.
    - Beim Empfang von 48 MB entstand eine Lücke von 220 ms.
  - `Process` mit `Pipe` hat folgende Eigenschaften:
    - `terminate()` dauert 2 ms.
    - Der Fehlerpfad liefert den Text der Ausnahme.
    - Die Übertragung läuft in Teilen von 1–4 MiB: Der längste einzelne `recv` dauerte 13–17 ms, die Gesamtübertragung 134–313 ms.
    - Das Entpacken am Ende dauert 37–320 ms.
- **Zweistufiger Ablauf** (Empfehlung):
  - **Auftrag A `lese_job(pfad)`:** Leser, SHA-256, Adapter, `Dateieinstellungen`. Er liefert `Messdaten` und Einstellungen. Ansicht 1 erscheint nach etwa 1–2 s (Spawn und Importe sind enthalten und lassen sich beim ersten Aktivieren des Reiters vorwärmen).
  - **Auftrag B `pruef_job(pfad)`:** liest erneut (Hash-Vergleich gegen A) und rechnet `werte_aus`. Er liefert nur Prüfungen und Annahmen (0,5 MB). So braucht keine große Übertragung in den Worker.
  - Ansichten 2–4 laufen auf der GUI-Seite mit `PaarCache` (lazy `bereite_paar` plus `werte_paar_aus`): 250 ms beim ersten Aufruf eines Paars, danach 0 ms. Vorgewärmt wird das Standardpaar.
  - **`Schwingform`** wird auf der GUI-Seite gerechnet: 82 ms beim ersten Aufruf, 21 ms danach.
  - Aufbau: `PaarCache` läuft in der GUI und nutzt dieselben Kernfunktionen wie `werte_aus`. Das Ergebnis ist dadurch identisch; ein Test vergleicht beides (`array_equal`).
- **Export** (Auftrag C) rechnet im Worker neu (Pfad plus Bänder) und schreibt mit `exportiere`. Das dauert etwa 10 s mit Busy-Anzeige, ist aber zustandslos und braucht keine Übertragung. Vorher prüft die GUI mit `pruefe_ziel`, ob das Ziel existiert.
- **Der Aufruf `python -m ldv_automation` wird im Worker erneut importiert** (spawn). Das kostet etwa 90–140 ms, lädt weder PySide6 noch pywin32 und ist unkritisch.
- **UI-15 ist erfüllbar,** aber nur mit dem Prozess. Der Test läuft über einen Ausführer, der nie fertig wird: Der Klick auf den Reiter „Messen“ muss trotzdem verarbeitet werden. Die echte Reaktionszeit ist am Messrechner zu messen (T5).
- **Das zweistufige Laden ist eine Ergänzung zum Brief** (Ansichten 2–4 zeigen kurz „Berechne …“, die Fußzeile zeigt „Prüfung: wird berechnet …“). Der Nutzer muss das freigeben (Abschnitt 6, Frage F-3).
- **Optional als Performance-Paket:** Eine Vektorisierung von `phasensinn_anteil` würde nach dem Profil `werte_aus` von etwa 8–13 s auf etwa 2 s senken. Das ist ein Eingriff in den Rechenkern mit bitgleicher Prüfung und nicht Teil dieses Plans.
- **ADR-Kandidat:** Ladestrategie, mit diesen Messwerten und den Alternativen (blockierend, `ProcessPoolExecutor`, `Process` plus `Pipe`).

**U-3 Spitzen und Bänder ohne Referenz**

Geprüft an der Beispieldatei mit entfernten `cp`, `cph`, `betrag` und Ref-Kanälen sowie `phase_gueltig=False` (`werte_aus` in 13 ms).
- Spitzen gibt es nur in `PaarAuswertung` (`gesamt.py`). Ohne Kreuzspektrum ist `paare == {}`, also keine Spitzen. „Keine Spitzensuche: Referenzkanal fehlt.“ passt wörtlich.
- Band-RMS bleibt über `band_ap` je Punkt und als Punktmittel erhalten (6 Bandwerte bei 3 Kanälen und einem Band).
- `werte_aus` läuft ohne Referenz fehlerfrei. P-05, P-07, P-09 und P-08 sind „nicht prüfbar“, `schwingform_aus` liefert dann `quelle="leistung"` ohne Phase.
- **Unverifiziert:** Eine echte `.svd` ohne Referenz liegt nicht vor. Der Test läuft über synthetische Daten (`svd_synth`).

**U-4 Frequenzachse**

- `Messdaten.frequenz_hz` kommt aus dem Leser (`Δf·k`, k = 1…Linien), `delta_f_hz` ebenfalls.
- Alle Darstellungen verwenden diese Achse. Zur Auswahl gilt: Anzeige „f_min … f_max“ nehmen aus `frequenz_hz[0]` und `frequenz_hz[-1]`, Einrasten per `waehle_linie`.
- Es wird nirgends neu aus Bandbreite und Linien gebildet. Ein Test erzwingt das mit einer künstlichen Achse (z. B. Δf = 0,3125 Hz).

**U-5 Toolbar-Symbole**

- Die Symbole liegen in `matplotlib/mpl-data/images` und sind Teil des matplotlib-Wheels. Es entsteht keine zusätzliche Dateiabhängigkeit.
- Die Texte der Toolbar sind englisch („Reset original view“ usw.). Plan: Unterklasse von `NavigationToolbar2QT` mit deutschen `toolitems`.
  - Behalten: Zurücksetzen, Zurück, Vor, Verschieben, Zoom.
  - Entfernen: „Subplots“, „Customize“, „Save“ (der Knopf „Bild speichern …“ ersetzt Save).
  - Stil: reine Textknöpfe (`ToolButtonTextOnly`, `coordinates=False`), passend zu P3 „keine Icon-Dateien“.
- Der Plot ist standardmäßig nicht fokussierbar (`focusPolicy` 0). Er muss auf `StrongFocus` gesetzt werden (UI-21).
- Ohne `FigureManager` gibt es keine voreingestellten matplotlib-Tastenkürzel. Pos1 und die Pfeiltasten sind unsere Implementierung.
- **Typisierung:** Eine Probe-Unterklasse ergab unter `mypy --strict` vier Fehler: `NavigationToolbar2QT` ist nicht explizit exportiert, `super().__init__` und `keyPressEvent` sind untypisiert, und `toolitems` hat einen unpassenden Typ. Lösung: Import aus `matplotlib.backends.backend_qt` und gezielte `# type: ignore[no-untyped-call]` mit Begründung, nur in `plotflaeche.py`.

**U-6 Projektionsebene**

- Die Koordinatenausdehnung der Beispieldatei ist x 0,196 m, y 0,484 m, z 0,017 m. Die Ebene der beiden größten Ausdehnungen ist **xy**, die z-Achse ist fast flach.
- Regel: Die Achse mit der kleinsten Ausdehnung entfällt, bei Gleichstand gilt xy vor xz vor yz.
- Die Voreinstellung xy stimmt mit der Beispieldatei überein. Das wird als Test fixiert.
- Die Brieftext-Formulierung „Ebene mit der größten Ausdehnung“ wird so konkretisiert (ein Hinweis, keine Änderung der Absicht).

**U-8 Modenfit-Zeilen**

- B-1 braucht 23 s je Paar (alle 111 Spitzen). Das ist interaktiv nicht tragbar und taugt nicht für den Start.
- Der Plan liefert deshalb die reine Funktion `modenfit_zeilen(ergebnis, frequenz_hz)`:
  - Sie gibt nur Zeilen mit Fitband (`fitband_hz`) und `METHODE_B1` aus, sonst nichts (R-055).
  - Sie wird anhand eines vorhandenen oder synthetischen `ModenfitErgebnis` getestet.
  - Sie ist in dieser Fassung nicht an eine Bedienung gekoppelt. Eine „Modenfit rechnen“-Schaltfläche stünde nicht im Brief (Frage N-5).

**matplotlib und olefile als Hauptabhängigkeit**

- In `software/pyproject.toml` kommen `matplotlib>=3.11.2` und `olefile>=0.47` in `dependencies`. Die Gruppe `werkzeuge` wird leer und verschwindet samt `default-groups`-Eintrag (kleiner Aufräumschritt, kein Verhalten).
- Getestet im Scratchpad (`lock/`): `uv lock --offline` löst in 0,5 s, keine Version ändert sich, nur die Metadaten im Lockfile.
- **`tools/wheelhouse/erzeuge_wheelhouse.py` fehlt `numpy` in `PINS`,** obwohl `installation_messrechner.md` es nennt. Das ist eine bestehende Abweichung und wird mit behoben.
- Neue Pins laut `uv.lock`:

| Paket | Version |
|---|---|
| numpy | 2.4.6 |
| matplotlib | 3.11.2 |
| contourpy | 1.3.3 |
| cycler | 0.12.1 |
| fonttools | 4.68.0 |
| kiwisolver | 1.5.1 |
| packaging | 26.3 |
| pillow | 13.0.0 |
| pyparsing | 3.3.3 |
| python-dateutil | 3.0.0 |
| six | 1.17.0 |
| olefile | 0.47 |

- Zusatzgröße etwa 19–20 MB. Es entsteht ein Test, der `PINS` gegen `uv.lock` abgleicht (verhindert die Abweichung dauerhaft).
- `installation_messrechner.md`, Abschnitt 3 und das `pip install`-Beispiel, müssen angepasst werden (Orchestrator/Dokumentation).
- **Risiko am Messrechner:** Der erste Import von matplotlib baut den Font-Cache. Das dauert unter Windows einige Sekunden bis Minuten, einmalig. In die Installationsprüfliste kommt ein Aufruf `python -c "import matplotlib.font_manager"`.

### 2 Plan

**Ansatz:** Qt-freie Schichten zuerst, dann die Oberfläche in zwei senkrechten Scheiben. Die erste Scheibe (Rahmen, Datei, Zustände, Ansicht 1) macht UI-1 früh sichtbar. Die unsicherste Annahme (Prozess und Datenweg) kommt zuerst.

Alternativen:
- Alles im Hauptprozess spart Code, bricht aber UI-15 und blockiert 8–13 s.
- Vollständiges Auswertungsobjekt aus dem Worker holen kostet etwa 4 s allein für die Übertragung und 250 MB RAM.

**Modulstruktur**

```
software/src/ldv_automation/
  hintergrund.py          GUI-frei, nur Standardbibliothek: Ausfuehrer-Protokoll,
                          ProzessAusfuehrer (spawn, Pipe, Teile ≤ 4 MiB),
                          DirektAusfuehrer (Tests); Auftrag.fertig/ergebnis/abbrechen
  auswertung/
    svd_lesen.py          verschoben (git mv); + Mittelung
    laden.py              Dateieinstellungen, Geladen, lade_svd(pfad)
    jobs.py               lese_job, pruef_job, export_job (Funktionen auf Modulebene)
  darstellung/            GUI-frei, nur Figure
    __init__.py, stil.py (Plotstil, THESIS_STIL), formate.py (Dezimalkomma, Einheiten),
    auswahl.py (Daten-Auswahl für die Kurven, PaarCache, Schwingform-Daten),
    spektrum.py, frf.py, spitzen.py, schwingform.py   (je Ansicht eine Zeichenfunktion),
    bild.py (Arbeitsbild mit Stempel)
  gui/
    anzeige_auswerten.py  rein, ohne Qt (Parameterzeile, Zeilen, Platzhaltertexte,
                          Prüfzusammenfassung, ABHAENGIG_VON, Cursortext, Reiterkopf)
    plotstil.py           baut Plotstil aus tokens (Farben bleiben nur in tokens.py)
    plotflaeche.py        PlotFlaeche + Toolbar-Unterklasse
    auswerten_reiter.py   Zonen AA–AF, Zustandsautomat, Ladesteuerung (QTimer)
    auswahl.py, tabellen_auswerten.py
    hauptfenster.py       nur Reiterrahmen und Aktions-Sperre
tools/auswertung/
    darstellung_beispiel.py   Thesis-Beispiel mit denselben Funktionen (UI-18)
    zeiten_messen.py          Messskript für den Messrechner (U-2/U-7)
```

**Schnittstellen**

```python
# darstellung (alle: keine Qt-, keine pyplot-Importe)
class Ansicht(Enum): SPEKTRUM, FRF, SPITZEN, SCHWINGFORM
zeichne_spektrum(fig: Figure, daten: SpektrumDaten, opt: SpektrumOptionen, stil: Plotstil) -> Zeichnung
zeichne_frf(...); zeichne_spitzen(...); zeichne_schwingform(...)   # gleiche Form
# Zeichnung: Achsen, Linien je Schlüssel, Marker, Hilfsobjekte

speichere_arbeitsbild(zeichne: Callable[[Figure], Zeichnung], pfad: Path,
                      stempel: Stempel, *, dpi: int = 200,
                      grenzen: Mapping[Axes-Index, Grenzen] | None = None) -> None
# baut eine neue Figure, ruft dieselbe Zeichenfunktion auf, übernimmt den Zoom, ergänzt den Stempel

class PaarCache:  # GUI-frei; Auswertung eines Paares bei Bedarf (LRU 2)
    def paar(self, antwort: str, referenz: str) -> PaarAuswertung

# gui
class PlotFlaeche(QWidget):
    zeichne(ansicht: Ansicht, daten: object, optionen: object) -> None
    speichere(pfad: Path, stempel: Stempel) -> None
    setze_cursor(f_hz: float | None) -> None
    zoom_zuruecksetzen() -> None
    # Signale: frequenz_gewaehlt(float), spitze_geklickt(int), cursor_bewegt(float)
```

`Plotstil` enthält Hauptfarbe, Gitter, Achse, Fläche, Band, Linienarten, Serienfarben, Schrift, `dezimalkomma`, `warn_symbol` und Verlauf. Die Oberfläche baut ihn aus `tokens.py` (`C_PLOT_*` und `PLOT_LINIENARTEN` bleiben dort, wie im Brief verlangt). `THESIS_STIL` ist schwarz/grau, 9 pt. So nutzen beide dieselbe Zeichenfunktion, und `darstellung/` importiert nichts aus `gui/`.

**Teilpakete (Reihenfolge nach Risiko, jedes einzeln lauffähig)**

| TP | Inhalt | Verifikation |
|---|---|---|
| **T1.1** | Leser ins Paket (`git mv`), Importzeilen in 6 Dateien, `pyproject.toml` und Lockfile, `PINS` samt Abgleichtest, Importregeln (`auswertung` darf `olefile`; neue Regeln für `darstellung`, `hintergrund`; `gui` darf zusätzlich `auswertung`, `darstellung`, `hintergrund`) | Standard-Prüfung unverändert grün; Golden-Test unverändert |
| **T1.2** | Mittelung im Leser (`Mittelung`, `dekodiere_mittelung`, `SvdMessung.mittelung = None`, `SICHERHEIT["fft.mittelung"] = "plausibel"`); synthetische Streams in `svd_synth`; Fenster als Konstante | Tests: Bytes, fehlender Stream, falsche Version, Typ 9; Golden: Typ 2 und Anzahl 7 an der Beispieldatei (File-Access-Gegenprobe) |
| **T1.3** | Kern-Zusätze, rein additiv: `Dateieinstellungen`, `lade_svd`; Hinweis-Konstanten für Mittel und 3D-Betrag; `daempfung_der_spitze` öffentlich; `berechne_baender` öffentlich als Wrapper um `_baender` | Alle bestehenden Export-Tests bytegleich; neue Funktion gegen die alte; Einstellungen an der Beispieldatei: 1000 Hz, 1600, 0,625 Hz |
| **T1.4** | `hintergrund.py`, `jobs.py`, `zeiten_messen.py` | Tests mit `DirektAusfuehrer`; ein echter Spawn-Test an der Beispieldatei (Lesen, `terminate`, Fehlerfall; ohne Datei übersprungen); Wiederholung der Messung |
| **T2** | `darstellung/` komplett (vier Zeichenfunktionen, Stil, Formate, Auswahl, `PaarCache`, Bild/Stempel), Beispielskript | Figure-Struktur (Linienzahl, `linestyle`, Achsenbeschriftungen, Skalen, Texte); Vergleich gegen den Kern (`array_equal`); Importtests (UI-18) |
| **T3a** | Reiterrahmen (lazy aufgebaut mit Fehlerrückfall), `PlotFlaeche`, Toolbar, AA/AB/AC/AF, Zustände Keine Datei, Laden, Fehler; Ansicht 1; Tokens | UI-1, 2, 3, 4, 12 (Zoom-Anteil), 15, 20, 22, 24 teilweise; bestehende GUI-Tests grün |
| **T3b** | Ansichten 2–4: AD-Seiten, Kanalpaarwahl, Tabellen, Kennzeichnung, Zustände „Keine Referenz“, „Eingabe außerhalb“, „Keine Spitze“ | UI-5 bis 11, 24 vollständig |
| **T4** | Export und Bild speichern, Cursor mit Blitting, Klick-Frequenz, Aktionen und Tastatur, Prüfdialog, Fokus und Tab-Reihenfolge, Drag-and-drop und „Zuletzt geöffnet“ (zuletzt, laut Streichreihenfolge) | UI-12 bis 14, 16, 17, 19, 21, 23, 25 |
| **T5** | Versionsnummer und Wheel (Orchestrator entscheidet), Prüfanleitung für den Messrechner (Messung U-2/U-7), Laborbuch/ADR/Matrix (Orchestrator) | Hardware/Windows-Prüfpunkte, nie als bestanden melden |

Schritte im Detail:

*T1.1 (Voraussetzung für alles)*
- `git mv` des Lesers, danach Importzeilen anpassen.
- `pyproject.toml`: `dependencies` ergänzen, Gruppe `werkzeuge` entfernen, `default-groups` anpassen.
- `uv lock --offline`.
- `tests/test_importrichtung.py`: `AUSWERTUNG_EXTERN` um `olefile` erweitern; Regel für `darstellung` (nur `darstellung` und `auswertung`; extern `numpy` und `matplotlib` ohne `pyplot`, `pylab`, `backend_qt*`, Qt-Pakete); `hintergrund` nur Standardbibliothek; die Regel für `gui` erweitern und nicht aufweichen. Zusätzlich ein Laufzeittest per Subprozess: `import ldv_automation.darstellung` lädt weder `PySide6` noch `matplotlib.pyplot`.
- `tools/wheelhouse/erzeuge_wheelhouse.py`: `PINS` ergänzen, Abgleichtest.
- README von `tools/svd_analyse` anpassen.

*T1.2*
- Strikte Dekodierung wie oben.
- `lese_container` liest `Info/DAQ_Settings_Fft/Average`, fehlt der Stream, ist `mittelung = None`.
- Optional (nur wenn der Nutzer zweite Dateien liefert): kleines Diff-Werkzeug `tools/svd_analyse/einstellungen_diff.py`.

*T1.3*
- `Dateieinstellungen`: `bandbreite_hz`, `linien`, `delta_f_hz`, `abtastfrequenz_hz`, `mittelung`, `punkte`, `referenzen` (Name und Einheit).
- `lade_svd(pfad) -> Geladen(messdaten, einstellungen)` fasst Leser, Hash und Adapter zusammen. Fehler werden als Text mit Pfad weitergereicht.
- Die beiden Hinweise („Mittel: √(Σ AP/n) über gültige Punkte, identisch zum PSV-Mittel von AP“ und „3D: √(Σ AP_c)“) stehen als Konstanten neben den Funktionen im Kern, einmalige Quelle.

*T1.4*
- `ProzessAusfuehrer`: `multiprocessing.get_context("spawn")`, `Pipe` mit Teilen bis 4 MiB, Fehlerkanal, `terminate`. Das Vorwärmen läuft über einen Leer-Auftrag mit `import`.
- `DirektAusfuehrer` läuft synchron, ohne Prozess.

*T2*
- `spektrum_daten`: Mittel und 3D-Betrag aus `mittel_ap` und `betrag_3d_ap`; keine neue Mathematik, nur Zusammensetzung. Das Mittel ist `√(Punktmittel von AP)`, identisch zum PSV-Mittel (FG-02 3.2).
- Log-Skala als Voreinstellung (OE-2), „dB“ nur wenn eine Referenzgröße existiert. Diese gibt es weder in `Messdaten` noch im Kern, deshalb ist die Option immer deaktiviert mit dem Grund „keine Referenzgröße (0 dB) in der Datei“.
- Dezimalkomma über `FuncFormatter`. Ticktexte werden in Tests mit `fig.draw_without_rendering()` geprüft.
- Linienart je Serie paarweise verschieden (`PLOT_LINIENARTEN`), Direktbeschriftung am Kurvenende.
- Ansicht 2: drei Teilbilder mit Höhen 45/30/25 % bzw. 65/35 %. Betrag und Kohärenz je Punkt aus `frf.h1`, `frf.h2`, `frf.kohaerenz`, für „Mittel“ aus `mittel_h1`, `mittel_h2`, `mittel_kohaerenz`.
- Ansicht 3: Spitzenmarker für alle Spitzen. Beschriftet wird nur die gewählte Spitze, bei 111 Spitzen (Beispieldatei, Paar Vib X/Ref1) wären alle Beschriftungen unlesbar.
- Ansicht 4: Streudiagramm der Punkte in der Projektionsebene mit Farbleiste (Einfarbverlauf aus dem Stil); das Dreiecksnetz über `tripcolor` ist optional.
- `speichere_arbeitsbild` baut eine neue Figure aus derselben Zeichenfunktion, übernimmt Zoom und ergänzt den Stempel (Abweichung vom Brief „auf derselben Figure“, Begründung: die Bildschirmfigur bleibt unverändert; Frage N-6).
- Das Thesis-Beispielskript erzeugt aus denselben Daten dieselbe Linienzahl und dieselben Achsentexte (UI-18).

*T3a*
- `Hauptfenster`: `QTabWidget` mit „Messen“ (bisheriger Inhalt unverändert) und „Auswerten“. Die Seite „Auswerten“ wird beim ersten Aktivieren aufgebaut. Damit kostet der Import von matplotlib (616 ms hier gemessen) den Messbetrieb nichts. Schlägt der Aufbau fehl, zeigt der Reiter einen Fehlertext, und der Messbetrieb bleibt unberührt.
- Die Aktionen F5 bis F8 und Strg+N/S/O werden im Reiter „Auswerten“ gesperrt (Prüfung im bestehenden Aktualisierungspfad).
- `Hauptfenster` erhält einen optionalen Parameter `ausfuehrer`, Standard `ProzessAusfuehrer` über `starte_gui`.
- `closeEvent` beendet laufende Aufträge (`abbrechen`).
- Die Reiterkopf-Zusätze (Fälle 1, 4, 5 und „▶ läuft“) kommen aus einer reinen Funktion über `Hinweis.fall` und `bild.durchgang`.
- Ladesteuerung: `QTimer` fragt alle 50 ms ab. Eine Job-ID verwirft veraltete Ergebnisse; ein neuer Dateiaufruf bricht den alten Auftrag ab.

*T3b*
- Kanalpaarwahl: gemeinsames Element für Ansichten 2 und 3 (in der Beispieldatei 7 Paare). Voreinstellung: erstes Paar in Dateireihenfolge, hier Vib X/Ref1 (Frage N-3).
- Tabellen: `QTableView` mit eigenem Modell, Zeilenhöhe 32 px, Sortieren per Spaltenkopf. Eine Zeile mit ζ ohne Bandgrenzen oder Methode wird nicht angezeigt und als Fehler gemeldet. Spitzen ohne bestimmte Breite (NaN) bekommen ζ und Bandgrenzen „–“, die Spitze selbst bleibt sichtbar (Annahme zur Auflösung des Widerspruchs im Brief; Frage N-4).
- Kennzeichnung: `ABHAENGIG_VON = {"phase": ("M8",)}` genau einmal in `anzeige_auswerten.py`; Quelle `Annahmen().eintraege()`, `ist_annahme` und `beschreibung`. Nach Stufe B wird gegen `Auswertung.annahmen_liste` geprüft.
- Zustände aus Brief Abschnitt 6, jeder einzeln testbar.

*T4*
- Export: `QFileDialog` mit `DontConfirmOverwrite`, damit die Meldung des Kerns (`pruefe_ziel`) erscheint. Der Export läuft als Auftrag C.
- Cursor: Blitting (`copy_from_bbox`, `restore_region`, `blit`), Hintergrund bei `draw_event` neu aufnehmen. Fällt Blitting aus, bleibt der Cursor aus.
- Zoom je Ansicht merken. Nach Neuzeichnen wird zuerst die Standardansicht auf den Toolbar-Verlauf gelegt (`push_current`), dann der gemerkte Zoom angewendet, damit „Zurücksetzen“ funktioniert.
- Aktionen als `QAction` mit `Qt.WindowShortcut`.

**Abbildung auf die UI-Kriterien**

| UI | TP | Test |
|---|---|---|
| UI-1 | T1.3, T2, T3a | Widgettest an Beispieldatei oder Attrappe |
| UI-2 | T1.2, T1.3, T3a | rein (Zellen) plus Widget; „Fenster“ stets „–“ mit Tooltip |
| UI-3 | T3a | Widget; Höhe 44 px |
| UI-4 | T2, T3a | Figure: Linienzahl, `linestyle` paarweise verschieden |
| UI-5, 6 | T2, T3b | Figure und Platzhaltertext |
| UI-7, 8 | T3b | rein (Zeilen) plus Figure (Marker, Bandfläche) |
| UI-9, 10, 11 | T2, T3b | Figure, rein; `ist_annahme=False` ändert nichts am GUI-Code |
| UI-12 | T3a, T4 | Zoom über Toolbar-Aufruf, Pos1 |
| UI-13, 14 | T4 | `setze_cursor`, Tastendrücke |
| UI-15 | T1.4, T3a | Ausführer, der nie fertig wird; Reiterklick wird verarbeitet |
| UI-16, 17 | T4 | Export mit Attrappen-Dialog; Figure-Texte mit und ohne Stempel |
| UI-18 | T1.1, T2 | Importtests plus Beispielskript |
| UI-19 | T4 | `QTest`-Tastendrücke, Dialoge per Attrappe |
| UI-20 | T3a | rein plus Widget |
| UI-21 | T3a, T3b, T4 | alle Widgets: `focusPolicy`; `:focus`-Regel |
| UI-22 | T3a | neue Paare in `KONTRAST_PAARE` |
| UI-23 | T3a (Text), T4 (Dialog) | rein; Widget |
| UI-24 | T3a, T3b, T4 | je Zustand |
| UI-25 | T3a, T4 | Geometrie bei 1100×680 und 1366×768 |

### 3 Testplan

- **Standard-Prüfung (alle Befehle aus KONVENTIONEN) und ≥ 90 % Abdeckung:**
  - Der Leser samt `Mittelung`, `laden.py`, `jobs.py`, `hintergrund.py`, `darstellung/` und `gui/anzeige_auswerten.py` laufen ohne Qt und zählen voll in die Abdeckung.
  - Die reinen Funktionen decken Parameterzeile, Zeilen, Platzhalter, Prüfzusammenfassung, Kennzeichnung und Cursortext ab.
  - `darstellung/` testet die Figure-Struktur, nicht Pixel (Linienzahl, `linestyle`, Achsentexte, Skalen, Ticktexte, Texte der Figure).
- **GUI-Tests (Marker `gui`, offscreen):** Widgetmodule kommen mit Begründung in `omit` (wie bisher). Neue Module: `plotflaeche.py`, `auswerten_reiter.py`, `auswahl.py`, `tabellen_auswerten.py`. Die Abdeckung wird separat mit `coverage_gui.toml` gemessen.
- **Referenzen:**
  - Mittelung und Einstellungen: File-Access-Werte vom 02.11. (Typ 2, Anzahl 7) und Golden-File-Test.
  - Zeichenfunktionen: Kerndaten (`array_equal`) und analytische Fälle aus `tests/auswertung/aw_referenz.py` (Einmassenschwinger).
  - `PaarCache` gegen `werte_aus(...).paare` (Gleichheit).
  - Die Annahmen aus `Annahmen().eintraege()` gegen `Auswertung.annahmen_liste`.
- **Importtests:** AST-Prüfung (kein `pyplot`, kein Qt in `darstellung/`) und Laufzeitprüfung per Subprozess.
- **Bestehende Tests:**
  - Die 95 Tests aus `test_gui_fenster.py` müssen grün bleiben (Lauf am Ende von T3a).
  - Die Reiterleiste kommt neu in die Fokusreihenfolge. Der Tab-Reihenfolge-Test im Reiter „Messen“ wird angepasst, nicht aufgeweicht, und das als Verhaltensänderung berichtet.
- **Echter Spawn:** ein Test mit der Beispieldatei in T1.4 (etwa 3 s).
- **Am Messrechner (nur Prüfanleitung, nie als bestanden melden):**
  - Zeiten (Lesen, Paar, Spawn, `zeiten_messen.py`),
  - HiDPI 125/150 %,
  - Schriften und ⚠-Glyph in matplotlib,
  - matplotlib-Font-Cache,
  - Reaktionszeit beim Laden.

### 4 Risiken

| Risiko | Woran man es merkt | Gegenmaßnahme |
|---|---|---|
| Spawn und Importe am Windows-Messrechner langsamer als hier gemessen | `zeiten_messen.py` | Vorwärmen beim ersten Aktivieren des Reiters; Alternative: Paare im Worker |
| Paar-Rechnung in der GUI (250 ms) am Messrechner über etwa 400 ms | Messung T5 | Rechnung als Auftrag in den Worker verlagern (zusätzlicher Pfad) |
| Arbeitsspeicher: Worker 741 MB RSS bei `werte_aus` | Messrechner mit wenig RAM | Messung; Performance-Paket P-07 optional |
| Umbau am Leser (`git mv`, 6 Importzeilen) bricht bestehende Prüfungen | T1.1 Standard-Prüfung | als eigener, reviewter Schritt |
| Bestehende GUI-Tests brechen durch den Reiterrahmen | Lauf am Ende T3a | Tab-Reihenfolge anpassen |
| mypy strict gegen matplotlib-Qt-Klassen | vier Fehler in der Probe | gezielte `type: ignore` nur in `plotflaeche.py` |
| Toolbar-Verlauf nach Neuzeichnen verliert „Zurücksetzen“ | UI-12 | Reihenfolge `push_current`, dann Zoom (T4) |
| Fensterwert nicht lesbar, Mittelung nur plausibel (R-032 teilweise) | – | Befund an den Nutzer; zweite Datei |
| Beschriftung bei 111 Spitzen unlesbar | Ansicht 3 | nur gewählte Spitze beschriften |
| ⚠-Glyph fehlt in der Segoe-UI-Schrift von matplotlib | Messrechner | Fallback über `warn_symbol` aus `tokens.symbol()` |

### 5 Aufwand (grobe Schätzung, nicht gemessen)

| TP | Quellcode | Tests |
|---|---|---|
| T1 gesamt | etwa 700 Zeilen | etwa 600 Zeilen |
| T2 | etwa 1100 Zeilen | etwa 900 Zeilen |
| T3a | etwa 900 Zeilen | etwa 500 Zeilen |
| T3b | etwa 900 Zeilen | etwa 600 Zeilen |
| T4 | etwa 600 Zeilen | etwa 500 Zeilen |
| T5 | klein | – |

Dazu kommen mindestens drei Review- oder Abnahmeläufe (nach T1, nach T3b, nach T4) und bis zu zwei Korrekturrunden je Review.

Modellhinweis: normal reicht für T1.1–T1.3, T2, T3 und T4. Für T1.4 (Prozess, Windows-Spawn) ist nur bei unerwartetem Verhalten ein stärkeres Modell nötig.

Empfehlung zusätzlich: eine kurze Fachfrage an den `strukturdynamik-experte` zu Frage F-2 (Spektrum der Ansicht 1) und zur Phase in Ansicht 4 und beim Mittel (F-4).

### 6 Offene Fragen an den Nutzer

**Blockierend**

- **F-2 Welche Größe zeigt Ansicht 1?**
  - Option (a), Annahme im Plan: `spektrum_leistung` (√AP, mit Rauschen, funktioniert auch ohne Referenz, Mittel identisch zum PSV-Mittel von AP).
  - Option (b): `spektrum_kohaerent` (|CPH|, entspricht laut FG-02 3.1 der PSV-Anzeige „Geschwindigkeit“, nur mit Referenz).
  - *Auswirkung:* Die Kurven und damit „stimmt mit PSV überein“ (R-050) hängen davon ab. Blockiert T2, Ansicht 1.
- **F-3 Zweistufiges Laden freigeben?**
  - Es ergänzt den Brief: Ansicht 1 nach etwa 1–2 s, Ansichten 2–4 laden bei Bedarf (250 ms je Paar), die Fußzeile zeigt „Prüfung: wird berechnet …“ bis zu 10 s.
  - Alternative: einstufig, nichts ist 8–13 s lang sichtbar.
  - *Auswirkung:* Zustände in T3a. Empfehlung: zweistufig.
- **F-1 Woher kommen die Bandgrenzen (R-053)?** Der Brief hat kein Eingabeelement.
  - Option (a): Standard-Gesamtband (0,625 … 1000 Hz) ohne Eingabe.
  - Option (b): Eingabezeile in der Auswahlspalte von Ansicht 3 („von/bis“, Liste, Entfernen); das ist ein Brief-Nachtrag. Die Bänder zu rechnen ist billig (32 ms für ein Band über alle 39 Bandwerte).
  - *Auswirkung:* Blockiert die Bandtabelle in T3b; Option (a) lässt sich später zu (b) ausbauen.
- **F-4 Was bedeutet „Phase“?**
  - Ansicht 4: Von welcher Komponente (X, Y oder Z, oder Auswahl)?
  - Ansicht 2: Bei „Mittel“ gibt es kein komplexes Punktmittel (FG-02 3.2: gehört nicht zu Stufe 1). Der Plan zeigt dort einen Platzhaltertext „Phase: für das Mittel nicht definiert“.
  - Zusätzlich ist offen, wie eine Phase in Graustufen (−180° … +180°) lesbar bleibt.
  - *Auswirkung:* Blockiert nur die Phase-Anteile von UI-9/UI-10, nicht den Rest von T3b.

**Nicht blockierend (Annahme bis zur Klärung)**

- **N-1** Mittelung als „plausibel“ anzeigen (Annahme), Fenster „–“. Optional zwei weitere Dateien beim nächsten Messtermin (Fenster Hanning; Mittelung Count 10 mit Typ Betrag).
- **N-2** „dB“ ist deaktiviert, weil keine Referenzgröße in Datei oder Kern existiert.
- **N-3** Kanalpaarwahl auch in Ansicht 3, Standard = erstes Paar in Dateireihenfolge (nicht Vib Z/Ref1).
- **N-4** Spitze ohne bestimmte −3-dB-Breite bleibt sichtbar, ζ und Bandgrenzen zeigen „–“ (löst die Brief-Formulierung „Zeilen mit fehlenden Feldern werden nicht angezeigt“ für den Fall ζ ohne Grenzen als Fehler auf).
- **N-5** Modenfit nicht automatisch (23 s je Paar). Die Zeilenfunktion ist da, eine Schaltfläche gibt es nicht.
- **N-6** Bild speichern über eine neue Figure aus derselben Zeichenfunktion statt Stempel auf der Bildschirmfigur.
- **N-7** Reiter „Auswerten“ wird beim ersten Öffnen aufgebaut (schützt den Messbetrieb vor matplotlib-Importproblemen).
- **N-8** „Zuletzt geöffnet“ und letzter Ordner in einer INI-Datei über `QSettings` (Ablageort ist neu; ein Test nutzt einen temporären Pfad).
- **N-9** Auslieferung mit neuer Versionsnummer (0.3.0) in T5; Export- und Protokollformate ändern sich nicht, `format_version` bleibt.
- **N-10** Performance-Paket für P-07 optional (Prüfzusammenfassung ab etwa 2 s statt 8–13 s).
- **N-11** Die Spitzenliste hat in der Beispieldatei 111 Zeilen. Ein Filter ist nicht im Brief und nicht geplant.

### 7 ADR-Kandidaten

1. Ladestrategie der Auswertung (eigener Prozess, `Process` plus `Pipe`, Teile, zweistufig, Messwerte oben).
2. Leser ins Hauptpaket (Nachtrag zu ADR-020) mit `olefile` als Hauptabhängigkeit.
3. Aufteilung `darstellung/` und `gui/` mit Stil als Parameter und Zeichenfunktion mit Rückgabeobjekt (Nachtrag zu ADR-021).

### 8 Nicht enthalten

Umrechnung Weg/Schnelle/Beschleunigung; Vergleich zweier Messungen; Modalanalyse über den vorhandenen Modenfit hinaus; drehbare oder animierte Schwingform; Thesis-Abbildungen; Bearbeiten von Messdaten; Änderungen am Reiter „Messen“ außer Reiterrahmen und Reiterkopf-Zusatz; keine Änderung der Export-Formate.

### 9 Hinweise außerhalb des Pakets

- `tools/auswertung/abbildungen.py` zeichnet mit `pyplot` eigene Abbildungen aus dem Export. Das ist doppelte Zeichenlogik zu den neuen Funktionen und widerspricht der Regel „gemeinsame Zeichenfunktion“. Eine Migration ist ein späteres Paket.
- Die Dokumentation `installation_messrechner.md` nennt `numpy` in `PINS`, das Skript tut es nicht (wird in T1.1 behoben).
- Der Brief (Abschnitt 5) legt fest, dass `Auswertung.annahmen_liste` vor der ersten Darstellung vorhanden ist (A-3). Das gilt nur über `Annahmen().eintraege()`; der Brief sollte das beim nächsten Stand nachziehen.
- „Pruefzusammenfassung: 9 ok, 1 Warnung“ im Brief ist ein Beispiel. Die Beispieldatei liefert 45 Ergebnisse (36 ok, 8 nicht prüfbar, 1 Hinweis), es gibt fünf Status.

## Rückmeldung an den Orchestrator

**Paket:** P-AUSW · **Status:** PLAN ZUR FREIGABE

**Was geändert wurde:** Nichts im Repository. Messungen und Prototypen im Scratchpad `/tmp/claude-0/-home-user/e6b61297-17fb-5003-91f8-95c4534d012c/scratchpad/p-ausw/` (insbesondere `zeit1.py`, `zeit2.py`, `proto_pool2.py`, `proto_proc.py`, `pk.py`, `u3.py`, `band.py`, `b1.py`, `qt1.py`, Kopie `ref.svd`).

**Wie verifiziert:** Die Messwerte stammen aus tatsächlich ausgeführten Skripten (siehe oben). Die Prozess-Prototypen (`ProcessPoolExecutor` und `Process` plus `Pipe`) liefen mit der Beispieldatei. Die Probe `uv lock --offline` und die mypy-Probe wurden im Scratchpad ausgeführt. Der bestehende GUI-Testlauf `pytest -m gui tests/gui/test_gui_fenster.py` (95 Tests) ist grün, ausgeführt mit `QT_QPA_PLATFORM=offscreen`.

**Akzeptanzkriterien:** Es handelt sich um ein Planungspaket. Die Abbildung der UI-1…UI-25 auf Teilpakete und Tests steht in Abschnitt 2.

**Annahmen:** Wie in Abschnitt 6 (N-1 bis N-11) mit Auswirkung genannt. Zusätzlich: Die Messwerte gelten für Linux und sind nur ein Anhalt für den Messrechner.

**Sichtbare Verhaltensänderungen und Risiken:**
- Der Leser liegt künftig im Paket, `olefile` und `matplotlib` sind Hauptabhängigkeiten (Wheel etwa 19–20 MB größer).
- Die Reiterleiste kommt in die Fokusreihenfolge; ein bestehender Tab-Reihenfolge-Test wird angepasst.
- Risiken: siehe Abschnitt 4.

**Unverifiziert:**
- Mittelung nur an einer Datei belegt (plausibel). Das Fenster ist nicht zuordenbar. Dafür bräuchte es zwei weitere Dateien (Abschnitt 1, U-1).
- Keine echte `.svd` ohne Referenz (nur synthetisch).
- Alle Windows-Aspekte (Spawn-Zeit, HiDPI, Schriften, Glyphen, Font-Cache, kalter Lesecache).
- Die Messwerte stammen von Linux, nicht vom Messrechner.

**Rückfragen:**
- [blockierend] F-2: Spektrum in Ansicht 1 als √AP oder |CPH|. *Auswirkung:* Werte gegenüber PSV (R-050).
- [blockierend] F-3: zweistufiges Laden mit zusätzlichem Zustand freigeben? *Auswirkung:* Zustände in T3a.
- [blockierend] F-1: Quelle der Bandgrenzen (Gesamtband oder Eingabezeile). *Auswirkung:* Bandtabelle in T3b, R-053.
- [blockierend] F-4: Bedeutung von „Phase“ in Ansicht 4 (Komponente) und bei „Mittel“ in Ansicht 2; Graustufen-Skala. *Auswirkung:* Phase-Anteile von UI-9/10/11.
- [nicht blockierend] N-1 bis N-11 (siehe Abschnitt 6), jeweils mit Annahme bis zur Klärung.

**Vorschlag für KONVENTIONEN.md:**
- Zeichenfunktionen für Oberfläche und Thesis liegen in `ldv_automation/darstellung/`, bekommen eine `Figure`, Daten, Optionen und einen `Plotstil`, importieren kein Qt und kein `pyplot`.
- Hintergrundrechnungen der Oberfläche laufen in einem eigenen Prozess (`spawn`), nie in einem `QThread`; Ergebnisse über die Prozessgrenze sind klein (< 1 MB), große Daten nur in Teilen.
- Sicherheitsgrad von Leserfeldern („gesichert“, „plausibel“, „offen“) wird in der Oberfläche nicht verändert; „offen“ ergibt „–“.

**Review-Empfehlung:** Review nach T1 (Schwerpunkt: Umzug des Lesers, Importregeln, Prozess und Fehlerpfade), nach T3b (Zustände, Kennzeichnung unbestätigter Größen, R-055-Zeilen) und nach T4 (Export, Bild, Tastatur, Fokus) mit Design-Abnahme durch den `ui-designer`. Fachabnahme durch den `strukturdynamik-experte` für F-2 und F-4 vor T2/T3b.