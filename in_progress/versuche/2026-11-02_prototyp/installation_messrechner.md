# Installation am PSV-Messrechner (Python 3.11, pywin32, Prototyp)

Stand: 2026-10-27, Paket P6. Gilt für den ersten Termin am PSV-Messrechner, Mo 2026-11-02.
Grundlage: `software/pyproject.toml`, `software/uv.lock`, Plan P2 Abschnitt 9 (E0, T0),
`software/tools/erkundung/README.md`, `software/tools/build_info/build_info.py`.

**Prüfstatus.** Alle Befehle sind gegen `pyproject.toml`, `uv.lock` und die READMEs
abgeglichen. **Kein Windows-Schritt ist getestet**, und es wurde nichts heruntergeladen oder
installiert. Marker wie [Wissen] bedeuten: aus allgemeinem Wissen, nicht belegt.
Grenzen: Der Messrechner ist 64-Bit-Windows (Auftrag); die Wheels sind nur für `win_amd64`
und CPython 3.11 vorgesehen.

## 1 Überblick: was auf den Messrechner kommt

| Teil | Zweck | Version (Quelle) |
|---|---|---|
| Python 3.11 (x64) | Laufzeit; `requires-python = ">=3.11,<3.12"` | 3.11.x (siehe 2) |
| `pyside6-essentials` | Oberfläche (ADR-001) | `==6.11.3` (`pyproject.toml`) |
| `shiboken6` | Abhängigkeit von PySide6 | `6.11.3` (`uv.lock`) |
| `pywin32` | COM-Zugriff auf PSV (Extra `com`) | `312` im Lockfile, `>=306` in `pyproject.toml` |
| eigenes Wheel `ldv_automation-0.1.0-py3-none-any.whl` | der Prototyp | `version = "0.1.0"` |
| `erkundung.py` | Erkundung Stufe 0/1/1b, **nicht** im Wheel | `software/tools/erkundung/` |

Die Erkundung braucht nur Python 3.11 (Stufe 0) bzw. zusätzlich pywin32 (Stufe 1). Der
Prototyp braucht alles. **`uv` wird am Messrechner nicht benötigt** (Weg A/B nutzen `venv` und
`pip`); `uv` ist nur ein optionaler Weg (Abschnitt 7).

PySide6 6.12.0 darf **nicht** installiert werden (ADR-001, Nachtrag: Absturz „none_dealloc“
unter Python 3.11). Die Pins oben verhindern das; das Meta-Paket `pyside6` wird nie installiert
(zieht ca. 170 MB zusätzlich, laut Analyse P1).

## 2 Python 3.11

1. Auf einem Rechner mit Internet den **Windows-Installer (64-bit)** für Python 3.11 von
   python.org holen. [Wissen, auf python.org prüfen:] Die letzte 3.11-Version mit fertigem
   Windows-Installer ist 3.11.9; spätere 3.11.x liefert python.org nur als Quelltext.
   Eine andere 3.11.x-Binärversion (z. B. über `uv python install 3.11`) ist ebenfalls zulässig,
   solange `python --version` „3.11.x“ meldet und das Programm 64-Bit ist.
2. Installer per USB auf den Messrechner. Installation **nur für den aktuellen Benutzer**
   („Install for me only“; kein Admin nötig [Wissen]), Option „py launcher“ an. „Add python.exe
   to PATH“ ist bequem, aber nicht nötig: Alle Befehle unten rufen `python.exe` des Venv mit
   vollem Pfad auf.
3. Falls auf dem Messrechner schon ein Python von Polytec liegt: **nicht verwenden und nichts
   darin installieren.** Eigenes Python getrennt halten.
4. Prüfen (PowerShell):

```powershell
py -3.11 --version
py -3.11 -c "import struct; print(struct.calcsize('P') * 8)"
```

Erwartet: `Python 3.11.x` und `64`. Bei `32` oder anderer Version: stoppen und melden.

## 3 Wheelhouse erzeugen (Rechner mit Internet, Vorbereitung vor Montag)

Zweck: alle Pakete für den Messrechner **vorab** als Wheels sammeln, damit dort kein Internet
nötig ist. Das gilt auch, wenn der Messrechner Internet hat (Reproduzierbarkeit, gleiche Pins).

**Fallstrick.** `pip download --platform …` wertet Umgebungsmarker auf dem *laufenden* Rechner
aus. `pywin32` hat in `uv.lock` den Marker `sys_platform == 'win32'`; ein Requirements-Export
aus `uv export` würde das Paket auf Linux/macOS daher weglassen. Deshalb werden die Pakete
unten als **feste Pins ohne Marker** angegeben.

Versionen gegen das Lockfile prüfen (aus `software/`):

```bash
grep -n -A1 '^name = "pywin32"' uv.lock        # erwartet: version = "312"
grep -n -A1 '^name = "pyside6-essentials"' uv.lock # erwartet: version = "6.11.3"
grep -n -A1 '^name = "shiboken6"' uv.lock        # erwartet: version = "6.11.3"
```

Download (aus `software/`; ein Befehl, **hier nicht ausgeführt**):

```bash
python -m pip download --dest wheelhouse --platform win_amd64 --python-version 3.11 \
  --implementation cp --abi cp311 --only-binary=:all: \
  "pyside6-essentials==6.11.3" "shiboken6==6.11.3" "pywin32==312"
```

Dasselbe bündelt das Skript `software/tools/wheelhouse/erzeuge_wheelhouse.py` (nur Anzeige:
`--nur-anzeigen`; optional `--mit-uv`). Es ruft ausschließlich diesen Befehl auf.

Erwartung [aus Analyse P1 abgeleitet, für diese Versionen nicht ausgeführt]: im Ordner
`wheelhouse/` liegen mindestens `pyside6_essentials-6.11.3-cp310-abi3-win_amd64.whl`,
`shiboken6-6.11.3-…win_amd64.whl` und `pywin32-312-cp311-cp311-win_amd64.whl` (Dateinamen laut
Einträgen in `uv.lock`). Zusammen etwa 90 MB. Meldet pip „No matching distribution“, nicht
auf `--no-binary` ausweichen, sondern melden.

Ergänzend ins Wheelhouse bzw. auf den Stick:

| Datei | Woher |
|---|---|
| Python-3.11-Installer (x64) | python.org, siehe 2 |
| `ldv_automation-0.1.0-py3-none-any.whl` | Abschnitt 4 |
| `erkundung.py` (und `README.md` daneben) | `software/tools/erkundung/` |
| `beispiel_messrechner.json` | `software/konfig/` |
| optional: Visual C++ Redistributable (x64) | Microsoft [Wissen: Qt-Wheels brauchen die VC-Laufzeit; auf einem Messrechner meist vorhanden] |
| diese Dokumente | `in_progress/versuche/2026-11-02_prototyp/` (ausgedruckt oder als Datei) |

Für Prüfsummen: `Get-FileHash <Datei>` (PowerShell) bzw. `sha256sum` und die Werte ins
Protokoll (`protokoll_vor_ort.md`) eintragen, damit klar ist, was installiert wurde.

## 4 Eigenes Wheel bauen (Entwicklungsrechner)

Das Wheel muss den Git-Hash enthalten, sonst ist `MESSEN` am Messrechner gesperrt (Plan 4.4,
ADR-012). Seit Korrektur K-U5 erzeugt der Build-Hook `software/hatch_build.py` die Build-Info
**beim Bau selbst** aus dem aktuellen Git-Stand und packt sie als `ldv_automation/_build_info.json`
ins Wheel; `artifacts` in `pyproject.toml` entfällt. Ein separater Lauf von
`tools/build_info/build_info.py` vor dem Bau ist nicht mehr nötig (das Skript bleibt als Werkzeug).
Ist kein Git-Hash ermittelbar (kein Git, kein Repository), **bricht der Bau ab**.

1. **Stand festlegen.** Erst nach dem letzten Commit bauen (Nutzerentscheidung). Der Hook schreibt
   den Hash von `HEAD` und ein Dirty-Flag (`git_dirty`); für Montag soll `git_dirty` **false** sein.
   Der Stand muss auf dem Arbeitsbranch **gepusht** sein, damit der Hash später auflösbar ist.
2. Aus `software/` (der Bau lädt hatchling aus dem Internet, daher auf dem Entwicklungsrechner):

```bash
uv build --wheel      # Ergebnis: dist/ldv_automation-0.1.0-py3-none-any.whl
```

3. **Prüfen, dass die Build-Info im Wheel steckt** (Linux/macOS; unter Windows
   `python -m zipfile -l dist\ldv_automation-0.1.0-py3-none-any.whl` und nach der Zeile suchen):

```bash
unzip -p dist/ldv_automation-0.1.0-py3-none-any.whl ldv_automation/_build_info.json
git rev-parse HEAD
```

   Erwartet: `git_hash` gleich der Ausgabe von `git rev-parse HEAD`, `git_dirty` ist `false`.
   Diesen Hash ins Protokoll eintragen (A3).
4. Wheel in das Wheelhouse bzw. auf den Stick kopieren. Wird später am Code etwas geändert, beginnt der
   Ablauf bei Schritt 1 neu (neuer Hash, neues Wheel).
5. **Konfigurationsdatei** `software/konfig/beispiel_messrechner.json` mit auf den Stick legen
   (Beispiel mit den Standardwerten; Verwendung siehe Ablaufplan, Abschnitt 4). Sie gehört nicht ins
   Wheel und ändert den Git-Hash nicht.

## 5 Installation am Messrechner

Ordnerwahl [Annahme, Laufwerk ggf. anpassen]: alles lokal unter `C:\ldv\`. Kein Netzlaufwerk,
nicht unter ProgramFiles/ProgramData/Windows-Ordner, nicht mit „Polytec“ direkt unter der Laufwerkswurzel und nicht im Repository (`C:\Users\Polytec\…` ist erlaubt; Kurznamen wie `PROGRA~3` werden abgelehnt)
(die Sitzung lehnt solche Messdaten-Ordner ab, siehe Prüfanleitung U3, Ergänzung U5).

```powershell
mkdir C:\ldv, C:\ldv\wheelhouse, C:\ldv\daten, C:\ldv\vorlagen, C:\ldv\erkundung
# Inhalt des Sticks nach C:\ldv\wheelhouse kopieren (Wheels + das eigene Wheel);
# erkundung.py nach C:\ldv\erkundung kopieren.
py -3.11 -m venv C:\ldv\venv
```

Das Venv wird **nicht aktiviert** (`Activate.ps1` kann durch die Ausführungsrichtlinie
blockiert sein); alle Befehle rufen `C:\ldv\venv\Scripts\python.exe` direkt auf.

### Weg A: ohne Internet am Messrechner (Standard)

```powershell
C:\ldv\venv\Scripts\python.exe -m pip install --no-index --find-links C:\ldv\wheelhouse `
  "C:\ldv\wheelhouse\ldv_automation-0.1.0-py3-none-any.whl[com]"
```

`[com]` installiert pywin32 mit. Bricht pip mit „No matching distribution“ ab, fehlt ein Wheel
im Ordner: Meldung notieren, nicht mit dem Internet nachhelfen, bevor das geklärt ist.

### Weg B: mit Internet am Messrechner

Nur nach Rücksprache (Netzfreigabe unklar, Plan Risiko 6). Gleiche Pins verwenden:

```powershell
C:\ldv\venv\Scripts\python.exe -m pip install "pyside6-essentials==6.11.3" "pywin32==312"
C:\ldv\venv\Scripts\python.exe -m pip install --no-deps C:\ldv\wheelhouse\ldv_automation-0.1.0-py3-none-any.whl
```

### Für die Erkundung (Stufe 0/1/1b)

Die Erkundung läuft mit demselben Venv-Python:

```powershell
C:\ldv\venv\Scripts\python.exe C:\ldv\erkundung\erkundung.py --stufe 0
```

Reine Stufe 0 braucht nur die Standardbibliothek und läuft auch mit dem systemweit installierten
Python 3.11. Stufe 1 braucht pywin32 (also das Venv).

### Falls `import pythoncom` an einer DLL scheitert

[Wissen, nicht belegt] pywin32-Wheels ab Version 300 laden ihre DLLs in der Regel ohne
Nachinstallation. Tritt trotzdem „DLL load failed“ auf, nur melden. Das
Nachinstallationsskript `pywin32_postinstall` schreibt in die Registry und braucht
Administratorrechte; es wird **nicht** ohne Absprache ausgeführt.

## 6 Prüfschritte nach der Installation

PowerShell, in beliebigem Ordner. Ergebnisse ins Protokoll (A3) eintragen. **PSV wird dabei nicht
gestartet und nicht angesprochen.**

| Nr | Befehl | Erwartet |
|---|---|---|
| I1 | `C:\ldv\venv\Scripts\python.exe --version` | `Python 3.11.x` |
| I2 | `C:\ldv\venv\Scripts\python.exe -c "import struct; print(struct.calcsize('P')*8)"` | `64` |
| I3 | `C:\ldv\venv\Scripts\python.exe -m pip list` | u. a. `ldv-automation 0.1.0`, `PySide6_Essentials 6.11.3`, `shiboken6 6.11.3`, `pywin32 312` |
| I4 | `C:\ldv\venv\Scripts\python.exe -c "import win32com.client; print('win32com ok')"` | `win32com ok`. **Nur importieren**, nichts anlegen oder dispatchen. Der Import kann einen `gen_py`-Cache im pywin32-Verzeichnis anlegen (Erkundung-README, Sicherheitskonzept); das notieren. |
| I5 | `mkdir C:\ldv\daten\selbsttest` und `C:\ldv\venv\Scripts\python.exe -m ldv_automation selbsttest --ordner C:\ldv\daten\selbsttest` | Ausgabe endet mit „Selbsttest bestanden“ (Simulator, ohne pywin32 und Oberfläche). Unter Windows **bisher ungetestet** (Prüfanleitung U3). |
| I6 | `C:\ldv\venv\Scripts\python.exe -c "import json,importlib.resources as r; print(json.loads(r.files('ldv_automation').joinpath('_build_info.json').read_text('utf-8')))"` | `git_hash` = Hash aus Abschnitt 4, `git_dirty` = `False` |
| I7 | `C:\ldv\venv\Scripts\python.exe -m ldv_automation gui --simulator` | Oberfläche startet mit Titel „LDV-Warteschlange – SIMULATOR“; Symbole ○ ▶ ✔ ✖ ■ ⏸ ⚠ sichtbar (Handtest F4) |

Schlägt I1 bis I4 fehl: nicht weitermachen, Meldung wörtlich notieren. Schlägt I5 oder I7 fehl:
Erkundung und COM-Tests der Erkundung bleiben möglich (kein Import aus dem Hauptpaket); der
Prototyp wird dann nur als Befund aufgenommen (Plan 9, T0: „GUI-Fehler: nur CLI bzw.
Selbsttest“).

Der Handtest U4 nennt `uv sync`/`uv run`. Am Messrechner gilt stattdessen derselbe Aufruf mit
dem Venv-Python (`C:\ldv\venv\Scripts\python.exe -m ldv_automation gui --simulator`).

## 7 Optional: uv am Messrechner

Nur wenn gewünscht (TODO nennt uv). Nicht nötig für Montag. Offline: `uv` mit
`erzeuge_wheelhouse.py --mit-uv` ins Wheelhouse holen und mit
`pip install --no-index --find-links C:\ldv\wheelhouse uv` installieren; online
`pip install uv`. Mit `uv sync` würde aus dem Repository eine Entwicklungsumgebung entstehen;
das Repository liegt am Messrechner aber nicht (Messdaten-Ordner dürfen auch nicht darin liegen).

## 8 Deinstallation und Rückbau

Alles liegt unter `C:\ldv\` (plus Python-Installation und ggf. `gen_py`-Cache). Zurückbauen:
Ordner `C:\ldv\` löschen; Python über „Apps & Features“ entfernen, falls es nur dafür installiert
wurde. Rohdaten (`.svd`, Protokolle) vorher sichern, siehe `ablaufplan_vor_ort.md`.
