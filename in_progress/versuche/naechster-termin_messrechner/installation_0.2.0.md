# Installation Version 0.2.0 (Auswertungsoberfläche) am PSV-Messrechner

Stand: 2026-11-05, Paket U-AUSW-T5. Ergänzt `ablaufplan.md` Block A1 (dort Wheel 0.2.0) und
`../2026-11-02_prototyp/installation_messrechner.md` (Prüfschritte I1 bis I7, Python,
Rückbau); Letzteres bleibt gültig, hier steht nur, was für den neuen Build 0.2.0 neu ist.

**Prüfstatus.** Kein Schritt ist am Messrechner getestet, es wurde nichts heruntergeladen oder
installiert. Marker: **[Annahme]** = nicht belegt, **[offen]** = muss geklärt werden.
Abgeglichen gegen `software/pyproject.toml`, `software/uv.lock` und `PINS` in
`software/tools/wheelhouse/erzeuge_wheelhouse.py`.

## 1 Was sich gegenüber dem Stick-Build 0.2.0 ändert

Der neue Build trägt dieselbe Versionsnummer 0.2.0 wie der Stick-Build 6d84318 vom 2026-11-03
und ersetzt ihn; der Git-Hash ist ein anderer (N3 prüfen). Der neue Build enthält den Reiter
„Auswerten“ (Darstellung der `.svd`-Datei mit matplotlib, Lesen über `olefile`), der Stick-Build
6d84318 nicht. Dafür kommen **neue Laufzeitabhängigkeiten** hinzu. Das Wheel selbst wird wie
bisher mit `--no-deps` installiert (PySide6 6.12.0 darf nie hineinkommen, ADR-001); die neuen
Pakete müssen daher **vorher** einzeln mit festen Pins in die venv.

| Neu in der venv | Pin |
|---|---|
| matplotlib | `matplotlib==3.11.2` |
| Abhängigkeiten von matplotlib | `contourpy==1.3.3`, `cycler==0.12.1`, `fonttools==4.68.0`, `kiwisolver==1.5.1`, `packaging==26.3`, `pillow==13.0.0`, `pyparsing==3.3.3`, `python-dateutil==3.0.0`, `six==1.17.0`, `tzdata==2026.6` |
| `.svd`-Leser | `olefile==0.47` |

Unverändert und bereits in der venv (nur kontrollieren): `numpy==2.4.6`,
`pyside6-essentials==6.11.3`, `shiboken6==6.11.3`, `pywin32==312`. Die Pins müssen exakt
`PINS` in `erzeuge_wheelhouse.py` entsprechen (ein Test erzwingt `PINS` == `uv.lock`); bei
Abweichung gilt die Liste im Skript, nicht diese Tabelle.

## 2 Ausgangslage und Variablen

Vorhandene PyCharm-venv (Stand laut Ablaufplan A1: Wheel 530af41 bzw. 0.1.0; 0.2.0 ist dort
nicht als installiert belegt; das Vorgehen ist gleich): `D:\Messdaten\DAL\BA Jakob Busch\PyCharmProject\.venv`,
Python 3.11.9.

```powershell
$PY = "D:\Messdaten\DAL\BA Jakob Busch\PyCharmProject\.venv\Scripts\python.exe"
& $PY --version        # erwartet Python 3.11.9
```

Die venv wird nicht aktiviert, alle Befehle rufen `$PY` auf. Wheel-Name: **[folgt]** (Version
0.2.0; Standardschema `ldv_automation-0.2.0-py3-none-any.whl` **[Annahme]**); SHA-256: **[folgt]**;
Ablageort: **[folgt]**.

## 3 Neue Abhängigkeiten installieren

**Weg 1: online mit Pins** (nur wenn der Rechner ins Internet darf, Frage F7 im Ablaufplan):

```powershell
& $PY -m pip install "matplotlib==3.11.2" "contourpy==1.3.3" "cycler==0.12.1" `
  "fonttools==4.68.0" "kiwisolver==1.5.1" "packaging==26.3" "pillow==13.0.0" `
  "pyparsing==3.3.3" "python-dateutil==3.0.0" "six==1.17.0" "tzdata==2026.6" "olefile==0.47"
```

**Weg 2: offline aus dem Wheelhouse.** Auf dem Entwicklungsrechner erzeugt
`python tools/wheelhouse/erzeuge_wheelhouse.py --ziel wheelhouse` (Windows x64, CPython 3.11,
`--only-binary=:all:`, alle `PINS`) die Wheels; Ordner auf den Stick. Das bisherige Stick-Wheelhouse
unter `stick/wheelhouse/` enthält nur das Wheel 0.2.0 (Stick-Build 6d84318, wird ersetzt), nicht die neuen Pakete. Ort des neuen
Wheelhouse: **[folgt]**. Am Messrechner:

```powershell
& $PY -m pip install --no-index --find-links "<Stick>\wheelhouse" `
  "matplotlib==3.11.2" "contourpy==1.3.3" "cycler==0.12.1" "fonttools==4.68.0" `
  "kiwisolver==1.5.1" "packaging==26.3" "pillow==13.0.0" "pyparsing==3.3.3" `
  "python-dateutil==3.0.0" "six==1.17.0" "tzdata==2026.6" "olefile==0.47"
```

Meldet pip „No matching distribution“, fehlt ein Wheel im Ordner: Meldung wörtlich notieren,
nicht auf Quellcode-Installation ausweichen.

## 4 Wheel 0.2.0 (neuer Build) installieren

Nur `--no-deps`; vorher SHA-256 gegen den Wert in 2 prüfen. Die neuen Pakete aus 3 müssen
vorher installiert sein.

```powershell
Get-FileHash "<Ordner>\<Wheel-Name>" -Algorithm SHA256
& $PY -m pip install --upgrade --no-deps "<Ordner>\<Wheel-Name>"
```

Rückfall nur, falls pip „already satisfied“ meldet oder N3 den alten Git-Hash 6d84318 zeigt:
`--upgrade --force-reinstall --no-deps` mit demselben Pfad. Das ist der Fall, wenn der
Stick-Build 6d84318 (gleiche Versionsnummer) bereits installiert war. Skripte (`erkundung.py` usw.) und
`tools/auswertung/zeiten_messen.py` liegen **nicht** im Wheel und kommen separat auf den Rechner
(Stick bzw. Git, wie A1 Schritt 4).

## 5 Prüfschritte

| Nr | Befehl | Erwartet |
|---|---|---|
| N1 | `& $PY -m pip list` | `ldv-automation 0.2.0`, `matplotlib 3.11.2`, `olefile 0.47`, `tzdata 2026.6`, `numpy 2.4.6`, `PySide6_Essentials 6.11.3`, `shiboken6 6.11.3`, `pywin32 312`; **kein** PySide6 6.12.0 |
| N2 | `& $PY -c "import ldv_automation; print(ldv_automation.__version__)"` | `0.2.0` |
| N3 | `& $PY -c "import json,importlib.resources as r; print(json.loads(r.files('ldv_automation').joinpath('_build_info.json').read_text('utf-8')))"` | `git_hash` = Hash des Builds (Orchestrator trägt ihn ein: **[folgt]**), `git_dirty` = `False` |
| N4 | `& $PY -c "import matplotlib.font_manager; print('Font-Cache ok')"` | `Font-Cache ok`. Der **erste** Import baut den Schriftcache und kann spürbar dauern (Dauer notieren, siehe Prüfanleitung); der zweite ist schnell |
| N5 | I1 bis I4 und I5 wie im [alten Plan](../2026-11-02_prototyp/installation_messrechner.md) | wie dort |
| N6 | `& $PY -m ldv_automation gui --simulator` | Oberfläche startet, Reiter „Messen“ und „Auswerten“ sichtbar |
| N7 | Im Reiter „Auswerten“ (Alt+2) eine **Kopie** der Beispieldatei öffnen (`20261012_ref_Mitte.svd`, im Repository unter `Input/`; Kopie z. B. nach `$ARB\daten\`, nie das Original in PSV-Ordnern öffnen) | Datei lädt, Kurven erscheinen, Fußzeile „Prüfung: …“ |

Schlägt N1 bis N3 fehl: nichts weiter installieren, Meldung sichern, alter Stand bleibt nutzbar
(EP-3 im Ablaufplan). Schlägt N4, N6 oder N7 fehl: Meldung/Foto sichern; die COM-Arbeit
(Reiter „Messen“, Erkundung) ist davon unabhängig. Ergebnisse in `protokoll.md` Abschnitt 4.
Weiter mit `pruefanleitung_auswerten.md`.

## 6 Offene Punkte

- **[offen]** Ablageort und SHA-256 des Wheels, Git-Hash des Builds, Ort des Wheelhouse für
  die neuen Pakete: trägt der Orchestrator nach dem Bau ein.
- **[offen]** Ob der Messrechner Internet hat (F7) und damit Weg 1 oder 2 gilt.
- **[Annahme]** Python 3.11.9 und `pywin32 312` sind wie im Ablaufplan A1 beschrieben vorhanden.
- **[Annahme]** `packaging`, `six` o. ä. können schon in der PyCharm-venv liegen; die Pins
  gelten trotzdem, pip ersetzt eine abweichende Version.
