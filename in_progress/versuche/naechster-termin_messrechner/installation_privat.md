# Installation 0.2.0 auf Jakobs privatem Windows-Rechner (nur Auswerten und Simulator)

Stand: 2026-11-19, Paket B-020-23 (Nutzerentscheidung 2026-11-19). Ergänzt `installation_0.2.0.md`
(dort Pins, Prüfschritte N1 bis N7). **Nicht getestet:** Es gibt keinen Windows-Lauf dieser Anleitung;
Marker **[Annahme]** = nicht belegt.

**Vorab klären (mit Daniel):** Ob Institutsmessdaten auf den privaten Rechner dürfen. Bis dahin nur die
Beispieldatei aus dem Repository verwenden; keine PSV-Daten vom Messrechner herüberkopieren.

## Voraussetzungen

- Windows 64 Bit, **Python 3.11.x** (genau 3.11; 3.12 oder neuer wird vom Paket abgelehnt). Quelle:
  python.org (Windows installer 64-bit) oder der Installer vom Stick (Rückfall 3.11.9).
- Der Stick bzw. eine Kopie von `stick/wheelhouse/` und `in_progress/versuche/2026-11-02_prototyp/stick/wheelhouse/`
  (dort numpy, PySide6-Essentials, shiboken6). Wheel: `ldv_automation-0.2.0-py3-none-any.whl`,
  SHA-256 `a483b2c624683ef38fa364a3e86857289074b54c3c563a95117727e3869d8b3d` (Git `3fd4e79df8e9bbde2d4557940efd1730db842164`).
- Kein Internet nötig, kein Administrator nötig **[Annahme]**.

## Installation (PowerShell, offline)

Die venv liegt **außerhalb** von PyCharmProject, z. B. `C:\ldv_privat\venv`. `<W1>` = Wheelhouse
des Sticks, `<W2>` = Prototyp-Wheelhouse.

```powershell
Get-FileHash "<W1>\ldv_automation-0.2.0-py3-none-any.whl" -Algorithm SHA256   # Wert wie oben
py -3.11 -m venv C:\ldv_privat\venv
$PY = "C:\ldv_privat\venv\Scripts\python.exe"
& $PY -m pip install --no-index --find-links "<W1>" --find-links "<W2>" `
  "numpy==2.4.6" "pyside6-essentials==6.11.3" "shiboken6==6.11.3" "matplotlib==3.11.2" `
  "contourpy==1.3.3" "cycler==0.12.1" "fonttools==4.68.0" "kiwisolver==1.5.1" "packaging==26.3" `
  "pillow==13.0.0" "pyparsing==3.3.3" "python-dateutil==3.0.0" "six==1.17.0" "tzdata==2026.6" "olefile==0.47"
& $PY -m pip install --no-index --no-deps "<W1>\ldv_automation-0.2.0-py3-none-any.whl"
```

`pywin32` entfällt, denn der Simulator braucht es nicht **[Annahme: der COM-Import ist verzögert, auf Windows
nicht geprüft]**. Das Wheel immer mit `--no-deps` installieren (PySide6 6.12.0 darf nie hinein, ADR-001).
Prüfen wie N1 bis N4 aus `installation_0.2.0.md` (Version 0.2.0, `git_hash` 3fd4e79…, `git_dirty` False).

## Start und Daten

```powershell
& $PY -m ldv_automation gui          # Simulator ist Standard; nie --psv
```

- Nur der Reiter „Auswerten“ und der Simulator; kein Vibrometer, keine COM-Verbindung.
- Daten: eine **Kopie** von `Input/20261012_ref_Mitte.svd` (Repository `BA_Jakob-Busch_P`) in einen
  Ordner außerhalb von PyCharmProject, z. B. `C:\ldv_privat\daten\`. Das Original in `Input/` nie öffnen oder verändern.
- Ausgaben (Export, Bilder, JSON) nur nach `C:\ldv_privat\daten\`, nie nach PyCharmProject oder `Input/`.

## Was zu Hause geht und was nicht

| Zu Hause (Kopie der Beispieldatei) | Nur am Messrechner |
|---|---|
| `pruefanleitung_auswerten.md` W1 bis W10 (Zeiten nur als Hausrechner-Werte notieren, nicht als Messrechner-Befund; W1 braucht `tools\auswertung\` vom Stick) | COM-Verbindung, PSV |
| `pruefanleitung_auswerten_vergleich.md` AV: Achsenleiste, mehrere Messungen, Ansicht 5, Bild speichern, Tastatur (V1 bis V4, B, C, D, E mit mehreren Kopien der Beispieldatei) | Abgleich lesen (`pruefanleitung_abgleich.md`), Messen, Warteschlangen mit echter `.set` |
| Animation in Ansicht 4: nur Sichtprüfung (Modus „Standbild/Animation“, Wiedergabe, Drehen, Zoom, Phase, Pflichttexte); Prüfanleitung `pruefanleitung_animation.md` (Block A, AN-1 bis AN-13, mit dem Build mit AN8/AN9) | UI-38 (Bedienung über Remotedesktop) und alle Messrechner-Zeiten und -Speicherwerte |

Ergebnisse von zu Hause gelten als Vorprüfung; bestätigt wird weiterhin erst am Messrechner bzw. durch Jakob
im Protokoll. Rückbau: Ordner `C:\ldv_privat\venv` löschen.
