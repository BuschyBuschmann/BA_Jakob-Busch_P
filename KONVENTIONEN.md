# Projektkonventionen

Verbindlich für alle Agenten und für den gesamten Code unter `software/`.
Existiert `software/pyproject.toml` noch nicht, ist das Anlegen von Projektgerüst,
Lockfile und Werkzeugkonfiguration das erste Umsetzungspaket.
Abweichung nur auf ausdrücklichen Auftrag des Nutzers.

## Umgebung
- Python 3.11, verwaltet mit `uv`.
- `requires-python = ">=3.11,<3.12"` in `software/pyproject.toml`.
- Das Paket liegt unter `software/`. Alle Befehle werden aus `software/` heraus ausgeführt.
- `uv.lock` wird eingecheckt, damit die Umgebung reproduzierbar ist.

## Standard-Prüfung
Vor jeder Rückmeldung eines Agenten, der Code unter `software/` ändert, müssen alle
Prüfungen fehlerfrei laufen (aus `software/`):

```bash
uv run ruff check .
uv run ruff format --check .
uv run mypy --strict .
uv run pytest --cov --cov-fail-under=90
```

- Lint und Format: `ruff`.
- Typprüfung: `mypy --strict`.
- Tests: `pytest` mit Testabdeckung (`pytest-cov`).
- Mindestabdeckung: 90 % (vom Nutzer festgelegt).
- Ausnahmen nur für dünnen Code direkt an der Hardware (COM-Adapter) oder am
  Bildschirm (GUI), der ohne Gerät bzw. Anzeige nicht testbar ist: per
  `# pragma: no cover` bzw. `[tool.coverage] omit`, jeweils mit Begründung als Kommentar an der Stelle (im Code
  bzw. in `pyproject.toml`).
  Logik bleibt voll abgedeckt.
- Nicht ausgeführte Prüfungen werden in der Rückmeldung ausdrücklich benannt.

## Code
- Docstrings im NumPy-Stil.
- SI-Einheiten; die Einheit steht im Namen (z. B. `freq_hz`, `velocity_m_s`) oder im Docstring.
- Winkel in rad, Zeit in s. Abweichende Einheiten werden nur an der Grenze zur COM-Schnittstelle umgerechnet.
- Zufall nur über einen übergebenen Seed bzw. `numpy.random.Generator`.

## Hardware
- Zugriff auf das Vibrometer (COM) nur über eine abstrakte Schnittstelle.
- Ein Simulator dieser Schnittstelle ist Pflicht, damit alles ohne Vibrometer testbar ist.
- Tests dürfen keine echte Hardware voraussetzen. Tests, die Hardware oder die Oberfläche
  brauchen, werden per `pytest`-Marker gekennzeichnet; standardmäßig laufen nur Simulator-Tests.

## Messdaten
- Messdaten werden in Dateien gespeichert, zusammen mit der Softwareversion (Git-Hash).
- Jeder an den Messrechner ausgelieferte Stand erhält eine neue Versionsnummer
  (`version` in `software/pyproject.toml`).
- Rohdaten werden nie überschrieben.
- Exporte der Auswertung tragen je Stufe eine eigene Formatkennung
  (`ldv_automation.auswertung.export[.stufeN]`) und nutzen den gemeinsamen Schreibweg
  `schreibe_export` (SHA-256 der Datendatei, Git-Hash, Herkunft der Messdatei). Eine neue Stufe
  ändert das Format einer bestehenden Stufe nicht.
- Jede inhaltliche Änderung an einem Export (auch neue Felder) erhöht dessen `format_version`;
  dasselbe gilt für die `schema_version` des Messprotokolls (Nutzerentscheidung 2026-11-03).
  Solange eine Version noch nicht ausgeliefert ist (nicht auf dem Messrechner und nicht in
  gespeicherten Daten), werden weitere Änderungen unter derselben Version geführt.
- Jede Dämpfungsangabe trägt `zeta`, die Bandgrenzen `band_u_hz` und `band_o_hz` und die
  `methode`, mit der sie bestimmt wurde (R-055). Das gilt für ζ-Angaben und ζ-Differenzen;
  reine Frequenzangaben (z. B. Frequenzdrift in Hz/h) sind keine Dämpfungsangaben.
  Eine ζ-Differenz gilt als belegt, wenn beide Ausgangswerte mit Bandgrenzen und Methode
  daneben stehen (z. B. `daempfung_a`/`daempfung_b` zu `delta_zeta`).

## Verifikation
- Jede Auswertefunktion wird gegen einen analytischen Referenzfall aus
  `in_progress/fachgrundlagen/` getestet.
- Toleranzen (`rtol`/`atol`) werden in Tests immer explizit angegeben und begründet.

## Abbildungen
- Abbildungen entstehen nur per Skript aus gespeicherten Daten.
- Skripte liegen unter `software/` (genauer Pfad wird mit dem ersten Abbildungspaket
  festgelegt), Ausgaben unter `in_progress/thesis/abbildungen/`.
- Jede Ausgabe nennt das erzeugende Skript und den Git-Hash der Eingangsdaten.
- Erstellt werden sie vom `software-engineer` im Umsetzungspaket.

## Polytec-Konventionen
Quelle: Analyseberichte I1, I2, I5 und I5-F unter `in_progress/analysen/`.
- „COM“ bezeichnet im Projekt das Component Object Model von Windows. Serielle Ports
  heißen „serielle Schnittstelle“.
- Daten aus Polytec-Schnittstellen (COM, Polytec File Access, Exporte) werden an der
  Adaptergrenze nach `float64` bzw. `complex128` gewandelt.
- Phasen intern in rad. Polytec liefert Betrag/Phase standardmäßig in Grad; im Adapter
  Real/Imag oder Betrag/Phase in rad verwenden bzw. umrechnen.
- Punkt- und Collection-Indizes sind intern 0-basiert. Die Umrechnung von bzw. zu den
  1-basierten Polytec-Indizes erfolgt nur im Adapter; der Originalindex der Messpunkte
  wird mitgeführt.
- Frequenzachse von Polytec-FFT-Daten: **bestätigt** (`20261012_ref_Mitte.svd`, PSV 10.4,
  2026-11-02; Laborbuch 2026-11-02_k-achse-frequenzachse) $f_k = k\,\Delta f$ mit
  $\Delta f = f_s/N = BW/n_\mathrm{FFT} = 1/T$ und $k = k_\mathrm{min} \dots k_\mathrm{max}$;
  im Vollbereich $k = 1 \dots n_\mathrm{FFT}$, DC nicht enthalten. Das Feld `Fft` @4 der
  `.svd` ist die Abtastfrequenz $f_s$, nicht die Bandbreite. Das Satzfeld +0x34 ist keine
  Blockdauer, seine Bedeutung ist offen. Bei eingeschränktem Bereich (Von/Bis) enthält die
  Datei möglicherweise weniger Linien. Die Achse wird deshalb immer gegen die Achsdaten der
  Datei (`XAxis`) oder ein Golden File geprüft. Stützen: Matlab-Beispiel zu Polytec File
  Access (`Input/literatur/polytec/Schulungsunterlagen/11.2 Polytec-File-Access_Matlab.pdf`,
  Folie 8), Software-Handbuch PSV 7-16/7-17.
- Spektren von Polytec sind einseitig und amplitudentreu auf die Spitzenamplitude
  (0-to-peak) skaliert. Real/Imag entsprechen $A\,e^{i\varphi_0}$ bei Zeitabhängigkeit
  $e^{+i\omega t}$, also $A\cos(\omega t + \varphi_0)$. Eine Phase ist nur gültig, wenn die
  Messung eine Referenz oder einen Trigger hatte; sonst kennzeichnet der Adapter sie als
  ungültig.
- Messpunkte führen im Code immer `index` (COM-Index, 1-basiert, nur im Adapter) und
  `label` getrennt. Was die PSV-Oberfläche „Index“ nennt, heißt im Code `label`.
- Messdateien (Rohdaten) werden mit Polytec File Access nur schreibgeschützt geöffnet;
  geschrieben wird ausschließlich in Kopien.
- Service- und Kalibriermethoden des Scankopfs (z. B. `ScanHeadControl.Write…`) werden
  nie aufgerufen. Der Adapter kapselt nur ausdrücklich freigegebene Methoden.
- Vorzeichen: Bei Kanälen je Scankopf (1D) bedeutet positive Geschwindigkeit Bewegung
  in Richtung Scankopf. Bei den 3D-Komponenten X/Y/Z bedeutet positiv Bewegung entlang
  der jeweiligen Achse des Koordinatensystems aus dem 3D-Abgleich (vorläufig, am Gerät
  zu bestätigen).
- Polarität der Referenzkanäle (vorläufig, nach Messung D2 und Datenblatt PCB 288D01 zu
  bestätigen): Sie wird bei jedem neuen Aufbau am Treibpunkt relativ zu den anderen Kanälen
  geprüft (Soll: v/a = −90°, Re{v/F} ≥ 0). `vorzeichen_kanal` beschreibt die Korrektur. Die
  absolute Richtung belegt das Datenblatt.
- Jeder COM-Zugriff, auch in Hilfsskripten, läuft über einen Whitelist-Proxy
  (Default deny): Nur ausdrücklich freigegebene Objekte, Methoden und Properties werden
  weitergereicht. Hilfswerkzeuge liegen unter `software/tools/` und importieren nicht
  aus dem Hauptpaket. **Ausnahme:** Reine Lesewerkzeuge für Polytec File Access (derzeit
  `software/tools/erkundung/einstellungen_lesen.py` und `daten_lesen.py`) dürfen ohne Proxy
  arbeiten. Voraussetzung ist ein statischer Test, der erzwingt, dass `ReadOnly = True` die
  einzige Zuweisung an ein COM-Objekt ist (Nutzerentscheidung 2026-11-03).

## Arbeitsweise bei Terminen vor Ort
- Bei Terminen am Messrechner arbeitet der Orchestrator direkt mit dem Nutzer, damit schnell
  Ergebnisse entstehen (Skripte, Auswertungen, Anleitungen ohne Arbeitsgruppe und ohne Review).
- Danach werden diese Ergebnisse über die Arbeitsgruppe geprüft (Review, Fachprüfung) und
  dokumentiert (Laborbuch), bevor darauf aufgebaut wird.
- Termine am Messrechner folgen einem Ablaufplan mit Entscheidungsbaum und Ersatzplänen.
  Abweichungen werden im Entscheidungsprotokoll festgehalten.
- Messdaten und Skriptausgaben werden nicht unter `PyCharmProject` abgelegt.
- Außerhalb solcher Termine gilt strikt der Ablauf über Aufbereitung, Freigaben und Review.

## Thesis-Formalien
Quelle: SLA-LaTeX-Vorlage unter `Input/Templates/LaTeX-Vorlage Wissenschaftliche Arbeit/`
(insbesondere `APPENDIX/` und `CHAPTERS_*`), siehe Analysebericht I3. Bis zur Klärung
mit dem Betreuer hat die SLA-Vorlage Vorrang vor
`Input/Templates/Richtlinien_fuer_wissenschaftliches_Arbeiten.pdf` (Wirtschaftswissenschaften).
- **Aufbau:** Titelseite, KI-Erklärung, Kurzfassung (DE), Abstract (EN), Verzeichnisse,
  Kapitel Einleitung · Stand der Technik · Methodik · Umsetzung · Analyse und Auswertung ·
  Schlussfolgerung und Ausblick, Literaturverzeichnis, Anhang.
- **Umfang:** unter 50 Seiten ohne Anhang.
- **Stil:** 3. Person, durchgängig Präsens (auch in der Durchführung), aktiv, Indikativ;
  kurze Sätze, einheitliche Fachbegriffe; Kapitel mit ein bis zwei Sätzen Einleitung und
  Abschluss.
- **Gliederung:** höchstens vierte Ebene; eine neue Ebene nur mit mindestens zwei
  Einträgen; Ergebnisse, Versuchspläne und Gerätedaten in Tabellen statt Aufzählungen.
- **Abkürzungen** beim ersten Auftreten einführen (außer Duden-Abkürzungen).
- **Zahlen** eins bis zwölf ausschreiben, ab 13 in Ziffern.
- **Formeln:** Multiplikationspunkt statt Stern; Differentialoperator und Einheiten
  aufrecht; im Fließtext Schrägstrich statt Bruch; Dezimalkomma.
- **Zitieren** numerisch mit biblatex/biber (`\cite`, `\textcite`).
- **Plots in der Oberfläche (ADR-021):** nie `pyplot`, nur `matplotlib.figure.Figure` mit
  `FigureCanvasQTAgg`. Je Abbildung gibt es eine gemeinsame Zeichenfunktion für Oberfläche und
  Thesis-Abbildung (Nutzerentscheidung 2026-11-03).
- **Abbildungen:** Farbe darf im Graustufendruck keine Information tragen, kein Gelb,
  Rot-Grün-Schwäche beachten; inklusive Bildunterschrift auf A5 lesbar; Achsen
  „Größe [Einheit]“; kein Diagrammtitel.
- **Kurzfassung und Abstract:** je höchstens eine Seite, ohne Formeln und
  Literaturhinweise, etwa fünf Schlagwörter alphabetisch.
- **KI-Erklärung:** Jeder KI-Einsatz, der Text, Abbildungen oder Inhalte der Arbeit
  beeinflusst, wird im Register `in_progress/ki-nutzung.md` geführt.

