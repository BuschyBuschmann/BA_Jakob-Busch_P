# Installation Version 0.2.0 (Auswertungsoberfläche) am PSV-Messrechner

Stand: 2026-11-05, Paket U-AUSW-T5; aktualisiert 2026-11-18 (P-TERMIN-23: Termin verschoben auf Montag 2026-11-23, Version bleibt 0.2.0, Build 2026-11-19: Git 1208ea2be20a5a45a9475f5acb7c6cb9151bbfad, SHA-256 des Wheels 1947897ee964cf10f2754a7b3e9db817487dc2018c446c3131adf5619f189552; Animation AN7 bis AN9 enthalten; Anleitung für den privaten Rechner: `installation_privat.md`). Ergänzt `ablaufplan.md` Block A1 (dort Wheel 0.2.0) und
`../2026-11-02_prototyp/installation_messrechner.md` (Prüfschritte I1 bis I7, Python,
Rückbau); Letzteres bleibt gültig, hier steht nur, was für den neuen Build 0.2.0 neu ist.

**Prüfstatus.** Kein Schritt ist am Messrechner getestet, es wurde nichts heruntergeladen oder
installiert. Marker: **[Annahme]** = nicht belegt, **[offen]** = muss geklärt werden.
Abgeglichen gegen `software/pyproject.toml`, `software/uv.lock` und `PINS` in
`software/tools/wheelhouse/erzeuge_wheelhouse.py`.

## 1 Was sich gegenüber dem Stick-Build 0.2.0 ändert

Der neue Build trägt dieselbe Versionsnummer 0.2.0 wie die früheren Stick-Builds (zuletzt a0ee2fc,
alle ersetzt und nie am Messrechner installiert; Nutzerentscheidung 2026-11-18: Version bleibt 0.2.0)
und ersetzt sie; der Git-Hash ist ein anderer (N3 prüfen). Der neue Build enthält den Reiter
„Auswerten“ (Darstellung der `.svd`-Datei mit matplotlib, Lesen über `olefile`), der frühe Stick-Build
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

Die venv wird nicht aktiviert, alle Befehle rufen `$PY` auf. Wheel-Name: `ldv_automation-0.2.0-py3-none-any.whl`; SHA-256: 1947897ee964cf10f2754a7b3e9db817487dc2018c446c3131adf5619f189552 (der frühere Wert des ersetzten Builds a0ee2fc gilt nicht mehr);
Ablageort: `stick/wheelhouse/` (Build 1208ea2be20a5a45a9475f5acb7c6cb9151bbfad, git_dirty false).

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
unter `stick/wheelhouse/` enthielt nur das Wheel 0.2.0 eines früheren, ersetzten Builds, nicht die neuen Pakete. Ort des neuen
Wheelhouse: `stick/wheelhouse/` (Stand 2026-11-05: 12 neue Pakete, das Wheel 0.2.0 wird durch den neuen Build ersetzt; SHA-256 in `stick/LIESMICH.txt`; numpy, PySide6, shiboken6 und pywin32 weiterhin aus dem Prototyp-Wheelhouse). Am Messrechner:

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

Rückfall nur, falls pip „already satisfied“ meldet oder N3 den Git-Hash eines früheren Builds zeigt:
`--upgrade --force-reinstall --no-deps` mit demselben Pfad. Das ist der Fall, wenn der
früherer Build mit gleicher Versionsnummer bereits installiert war (nicht belegt). Skripte (`erkundung.py` usw.) und
`tools/auswertung/zeiten_messen.py` liegen **nicht** im Wheel und kommen separat auf den Rechner
(Stick bzw. Git, wie A1 Schritt 4).

## 5 Prüfschritte

| Nr | Befehl | Erwartet |
|---|---|---|
| N1 | `& $PY -m pip list` | `ldv-automation 0.2.0`, `matplotlib 3.11.2`, `olefile 0.47`, `tzdata 2026.6`, `numpy 2.4.6`, `PySide6_Essentials 6.11.3`, `shiboken6 6.11.3`, `pywin32 312`; **kein** PySide6 6.12.0 |
| N2 | `& $PY -c "import ldv_automation; print(ldv_automation.__version__)"` | `0.2.0` |
| N3 | `& $PY -c "import json,importlib.resources as r; print(json.loads(r.files('ldv_automation').joinpath('_build_info.json').read_text('utf-8')))"` | `git_hash` = Hash des Builds (1208ea2be20a5a45a9475f5acb7c6cb9151bbfad, voller Wert in `stick/LIESMICH.txt`), `git_dirty` = `False` |
| N4 | `& $PY -c "import matplotlib.font_manager; print('Font-Cache ok')"` | `Font-Cache ok`. Der **erste** Import baut den Schriftcache und kann spürbar dauern (Dauer notieren, siehe Prüfanleitung); der zweite ist schnell |
| N5 | I1 bis I4 und I5 wie im [alten Plan](../2026-11-02_prototyp/installation_messrechner.md) | wie dort |
| N6 | `& $PY -m ldv_automation gui --simulator` | Oberfläche startet, Reiter „Messen“ und „Auswerten“ sichtbar |
| N7 | Im Reiter „Auswerten“ (Alt+2) eine **Kopie** der Beispieldatei öffnen (`20261012_ref_Mitte.svd`, im Repository unter `Input/`; Kopie z. B. nach `$ARB\daten\`, nie das Original in PSV-Ordnern öffnen) | Datei lädt, Kurven erscheinen, Fußzeile „Prüfung: …“ |

Schlägt N1 bis N3 fehl: nichts weiter installieren, Meldung sichern, alter Stand bleibt nutzbar
(EP-3 im Ablaufplan). Schlägt N4, N6 oder N7 fehl: Meldung/Foto sichern; die COM-Arbeit
(Reiter „Messen“, Erkundung) ist davon unabhängig. Ergebnisse in `protokoll.md` Abschnitt 4.
Für Jakobs privaten Windows-Rechner (nur Auswerten, Simulator): [installation_privat.md](installation_privat.md). Weiter mit `pruefanleitung_auswerten.md` (W1 bis W10), `pruefanleitung_auswerten_vergleich.md` (AV) und, mit COM, `pruefanleitung_abgleich.md` (Abgleich lesen); Einordnung in den Tag: Ablaufplan 4.4.

## 6 Offene Punkte

- **[erledigt 2026-11-19]** Build: Git `1208ea2be20a5a45a9475f5acb7c6cb9151bbfad`, SHA-256 `1947897ee964cf10f2754a7b3e9db817487dc2018c446c3131adf5619f189552`, `git_dirty` false; Wheelhouse der neuen Pakete in `stick/wheelhouse/` (unverändert).
- **[erledigt]** `tools/auswertung/speicher_messen.py` (für AV V1) liegt auf dem Stick.
- **[offen]** Ob der Messrechner Internet hat (F7) und damit Weg 1 oder 2 gilt.
- **[Annahme]** Python 3.11.9 und `pywin32 312` sind wie im Ablaufplan A1 beschrieben vorhanden.
- **[Annahme]** `packaging`, `six` o. ä. können schon in der PyCharm-venv liegen; die Pins
  gelten trotzdem, pip ersetzt eine abweichende Version.
