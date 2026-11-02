# COM-Schnittstelle PSV 10.4 registrieren

Stand: 2026-11-02 · Rechner BEOWOLF · Durchführung nur mit Zustimmung von Daniel

## Befund (Erkundung Stufe 0, 15:00)
- Laufende Version: PSV 10.4 (`C:\Program Files\Polytec\PSV 10.4\PSV.exe`); parallel installiert: 10.2, 10.3.
- Keine Version ist als COM-Server registriert (keine ProgID `PSV.AcquisitionInstance`, keine „Polytec PSV Type Library“).
- Folge: Erkundung Stufe 1 und Prototyp-Tests T1–T8 sind nicht möglich.

## Grundlage
Release Notes PSV 10.4 (`Doc\Release Notes deu.htm`): Bei parallel installierten Versionen
„eine Eingabeaufforderung mit Administratorrechten im Installationsverzeichnis … öffnen und den
Befehl *PSV.exe /regserver* eingeben“. Alternative laut Polytec: Reparaturinstallation.

## Vor dem Start mit Daniel klären
- [ ] Nutzt jemand PSV 10.2 oder 10.3 noch (Makros, Basic Engine)?
- [ ] Ist es in Ordnung, dass 10.4 die registrierte Version wird? (Es kann immer nur eine Version registriert sein.)
- [ ] Ist die externe Automatisierung lizenziert?

## Schritte
1. [ ] Keine Messung läuft. PSV schließen; `Get-Process PSV` findet nichts.
2. [ ] Startmenü → `cmd` → Rechtsklick → **Als Administrator ausführen** (Admin bestätigt).
3. [ ] In der Eingabeaufforderung:
   ```
   cd /d "C:\Program Files\Polytec\PSV 10.4"
   PSV.exe /regserver
   ```
   Einige Sekunden warten. Startet die normale PSV-Oberfläche: schließen und melden.
4. [ ] Prüfen (PyCharm-Terminal, nur lesen):
   ```powershell
   Get-ChildItem Registry::HKEY_CLASSES_ROOT | Where-Object { $_.PSChildName -like 'PSV*' } | Select-Object PSChildName
   ```
   Erwartet: u. a. `PSV.AcquisitionInstance`.
5. [ ] Erkundung Stufe 0 wiederholen, Dateien an Claude schicken:
   ```powershell
   python "D:\Messdaten\DAL\BA Jakob Busch\erkundung.py" --stufe 0 --out "D:\Messdaten\DAL\BA Jakob Busch\erkundung"
   ```
   Erwartet: `PSV.AcquisitionInstance` registriert, `LocalServer32` = `C:\Program Files\Polytec\PSV 10.4\PSV.exe`.
6. [ ] PSV über **„PSV 10.4 Deutsch“** starten (`/Acquisition`, Messmodus), **nicht** „Desktop“.
   Keine Dialoge offen, keine Messung. Dann Erkundung Stufe 1 (Ablaufplan, Abschnitt 3).

## Falls es nicht klappt
- Weiterhin kein `PSV.AcquisitionInstance`: Reparaturinstallation von PSV 10.4 (Einstellungen → Apps → PSV 10.4 → Ändern → Reparieren), dann Schritt 4.
- Registriert, aber Verbinden scheitert in Stufe 1: vermutlich Lizenz oder Desktop-Modus → Daniel/Polytec-Support.

## Fürs Protokoll
| Zeit | Befehl / Aktion | ausgeführt von | Ergebnis |
|---|---|---|---|
| | `PSV.exe /regserver` in `C:\Program Files\Polytec\PSV 10.4` (Admin) | | |

Rückgängig bzw. umschalten: denselben Befehl im Ordner der anderen Version ausführen.
