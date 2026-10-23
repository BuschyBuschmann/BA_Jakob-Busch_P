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
- Rohdaten werden nie überschrieben.

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
Quelle: Analyseberichte I1 und I2 unter `in_progress/analysen/`.
- „COM“ bezeichnet im Projekt das Component Object Model von Windows. Serielle Ports
  heißen „serielle Schnittstelle“.
- Daten aus Polytec-Schnittstellen (COM, Polytec File Access, Exporte) werden an der
  Adaptergrenze nach `float64` bzw. `complex128` gewandelt.
- Phasen intern in rad. Polytec liefert Betrag/Phase standardmäßig in Grad; im Adapter
  Real/Imag oder Betrag/Phase in rad verwenden bzw. umrechnen.
- Punkt- und Collection-Indizes sind intern 0-basiert. Die Umrechnung von bzw. zu den
  1-basierten Polytec-Indizes erfolgt nur im Adapter; der Originalindex der Messpunkte
  wird mitgeführt.
- Frequenzachse von Polytec-FFT-Daten: $f_k = k\,\Delta f$ mit $k = 1 \dots n_\mathrm{FFT}$
  und $\Delta f = BW/n_\mathrm{FFT}$, DC nicht enthalten. **Vorläufig**, an einer realen
  Messdatei zu bestätigen. Stütze: Matlab-Beispiel zu Polytec File Access
  (`Input/literatur/polytec/Schulungsunterlagen/11.2 Polytec-File-Access_Matlab.pdf`,
  Folie 8: 400 Linien, 12,5 Hz bis 5000 Hz).
- Messpunkte führen im Code immer `index` (COM-Index, 1-basiert, nur im Adapter) und
  `label` getrennt. Was die PSV-Oberfläche „Index“ nennt, heißt im Code `label`.
- Messdateien (Rohdaten) werden mit Polytec File Access nur schreibgeschützt geöffnet;
  geschrieben wird ausschließlich in Kopien.
- Service- und Kalibriermethoden des Scankopfs (z. B. `ScanHeadControl.Write…`) werden
  nie aufgerufen. Der Adapter kapselt nur ausdrücklich freigegebene Methoden.
- Vorzeichen: positive Geschwindigkeit bedeutet Bewegung in Richtung Scankopf;
  3D-Komponenten liegen im Objektkoordinatensystem des 3D-Abgleichs.

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
- **Abbildungen:** Farbe darf im Graustufendruck keine Information tragen, kein Gelb,
  Rot-Grün-Schwäche beachten; inklusive Bildunterschrift auf A5 lesbar; Achsen
  „Größe [Einheit]“; kein Diagrammtitel.
- **Kurzfassung und Abstract:** je höchstens eine Seite, ohne Formeln und
  Literaturhinweise, etwa fünf Schlagwörter alphabetisch.
- **KI-Erklärung:** Jeder KI-Einsatz, der Text, Abbildungen oder Inhalte der Arbeit
  beeinflusst, wird im Register `in_progress/ki-nutzung.md` geführt.

