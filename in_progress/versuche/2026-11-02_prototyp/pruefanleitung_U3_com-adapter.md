# Prüfanleitung COM-Adapter (U3) für den Test am Messrechner, Mo 2026-11-02

Stand: 2026-10-26, Paket U3 (Ablauf G). Grundlage: Plan P2, Abschnitte 3, 6 und 9.
Diese Anleitung gilt nur für den COM-Adapter. Die Gesamtschritte T0 bis T7 stehen in
Plan P2, Abschnitt 9. Für T4 bis T6 gilt das Versuchsprotokoll aus `/versuchsplanung`.

**Ein Hardwaretest gilt erst als bestanden, wenn du ihn bestätigt hast.** Bis dahin ist
jedes COM-Verhalten des Adapters nur gegen einen Fake geprüft und am Gerät **ungeprüft**.

## Vorbedingungen

- Erkundung E0 und E1 sind gelaufen, der Ergebnisordner ist gesichert.
- PSV läuft im Erfassungsmodus, es läuft keine Messung (`State` = Stopped).
- In PSV ist „Meldungen bei Automatisierung unterdrücken“ aktiv
  (`SuppressMessagesForAutomation = True`). Der Adapter schaltet das nie selbst ein.
- Für T2: eine kleine `.set` (z. B. 3×3 Punkte, **Generator aus**) liegt bereit.
- Messdaten-Wurzelordner angelegt, **nicht** in einem Polytec-Verzeichnis und nicht im
  Repository (z. B. `D:\ldv_messdaten`).
- Shaker bzw. Verstärker sind getrennt, solange der Betreuer die Anregung nicht freigibt.

## Schalter aus der Erkundung übernehmen

| Befund aus E1 | Einstellung im Adapter (`ComKonfiguration`) |
|---|---|
| `FftAcqPropertiesValidator_vorhanden` = ja | `validator_rueckfall_direkt=False` (Standard) |
| Validator fehlt | `validator_rueckfall_direkt=True` (Rückfall S4, ADR-005) |
| Konstanten weichen von I5 §8 ab | **stoppen**, Befund melden; nichts weiter am Gerät |
| PSV-Prozessname enthält nicht `psv` (Stufe 0, `psv_prozesse`) | **stoppen**, Befund melden (der Adapter verbindet dann nicht) |
| `psv_prozesse` (Stufe 0) enthält außer PSV selbst einen weiteren Prozess mit „psv“ im Namen (Fehltreffer) | **stoppen**, Befund melden: Die Prozessprüfung des Adapters würde dann auch ohne laufende PSV verbinden. Zur Gegenprobe zeigt der Adapter alle Treffer (`g.psv_prozesse`, `info.hardware["psv_prozesse"]`) |
| Verbinden scheitert | nur Simulator vorführen, Befund sichern |

Die Lademaske ist voreingestellt auf `Acquisition|Alignment|APS|2DAlignment|3DAlignment`
(ohne Camera und Windows). Ändern nur nach Rücksprache.

## Schritte

Normalerweise laufen T1 bis T6 über die Oberfläche (U4). Fällt die Oberfläche aus, lassen
sich T1 und T2 auch in einer Python-Konsole prüfen (aus dem Paketordner, Python 3.11
mit pywin32). **Messen (T4 bis T6) nur über die Oberfläche**, weil Zeitlimit, Abbruch und
Protokoll in der Steuerung liegen.

### T1: Nur lesen

```python
from ldv_automation.geraet.com.adapter import ComBetriebsart, ComKonfiguration, PsvComGeraet
from ldv_automation.geraet.com.pywin32_bindung import Pywin32Bindung

g = PsvComGeraet(Pywin32Bindung(), ComKonfiguration(betriebsart=ComBetriebsart.NUR_LESEN))
info = g.verbinde(); print(info)
print("PSV-Treffer:", g.psv_prozesse)  # darf nur PSV selbst enthalten
print(g.zustand())
stand = g.lies_einstellungsstand(); print(stand)
for a in g.aufrufe(): print(a)
print("verweigert:", g.verweigerungen())
g.trenne()
```

Prüfen und notieren:

| Nr. | Erwartung | ok? |
|---|---|---|
| 1-0 | `PSV-Treffer:` enthält nur PSV selbst (Abbildname notieren); sonst Abbruch | |
| 1-1 | `psv_version`, Modus und Hardware stimmen mit Erkundung Stufe 1 und der PSV-Anzeige überein | |
| 1-2 | `zustand()` liefert `GESTOPPT` | |
| 1-3 | `stand.modus == "Fft"`; FFT-Werte (Bandbreite, Linien, Abtastfrequenz) wie in PSV | |
| 1-4 | Kanäle und Generator (aktiv, Amplitude) wie in PSV; Einträge mit `__fehler` notieren | |
| 1-5 | `verweigert:` ist leer `()` | |
| 1-6 | Kein Dialog in PSV, keine Laser- oder Spiegelbewegung | |

### T2: Trockenlauf (ändert die PSV-Einstellungen, bewegt nichts)

```python
konf = ComKonfiguration(
    betriebsart=ComBetriebsart.TROCKENLAUF,
    messdaten_wurzel=r"D:\ldv_messdaten",
    validator_rueckfall_direkt=False,  # nach E1 setzen
)
g = PsvComGeraet(Pywin32Bindung(), konf)
g.verbinde()
g.lade_einstellungen(r"D:\ldv_vorlagen\test_3x3.set")
g.setze_parameter({"fft.bandbreite_hz": 5600.0, "mittelung.anzahl": 5})
print(g.lies_parameter(["fft.bandbreite_hz", "mittelung.anzahl"]))
print(g.lies_einstellungsstand())
g.speichere_einstellungen(r"D:\ldv_messdaten\trockenlauf_nachweis.set")
print("verweigert:", g.verweigerungen()); g.trenne()
```

| Nr. | Erwartung | ok? |
|---|---|---|
| 2-1 | Laden ohne Dialog; PSV zeigt die Einstellungen der `.set` | |
| 2-2 | 5600 Hz rastet ein: `lies_parameter` liefert einen anderen Wert (z. B. 6250 Hz); Wert notieren | |
| 2-3 | Zurückgelesene Werte stimmen mit der PSV-Anzeige überein | |
| 2-4 | Nachweis-`.set` liegt im Wurzelordner; ein zweites Speichern unter demselben Namen wird mit `VerweigertFehler` abgelehnt | |
| 2-5 | `g.starte_scan(...)` wird im Trockenlauf mit `VerweigertFehler` abgelehnt, PSV erhält keinen Aufruf | |
| 2-6 | `verweigert:` ist leer (2-5 lehnt schon der Adapter ab, der Proxy wird dabei nicht angefragt) | |
| 2-7 | Keine Laser-, Spiegel- oder Generatoraktivität | |

### T3 bis T6: über die Oberfläche

Zusätzlich zum Plan auf Adapterseite prüfen:

| Nr. | Erwartung | ok? |
|---|---|---|
| 4-1 | Vor dem Scan steht im Aufrufprotokoll: `Acquisition.State`, `ScanFileName` setzen und lesen, `Acquisition.State`, `ScanEx(0, 0)` | |
| 4-1a | **Erster Poll direkt nach `ScanEx`:** Welchen `State` liefert der erste `Acquisition.State` nach `Acquisition.ScanEx` im Aufrufprotokoll (bzw. erste Zustandsanzeige nach dem Start)? Wert notieren (erwartet ScanAll = 3) | |
| 4-2 | **Ob `ScanEx` bis zum Scanende blockiert**, notieren (Wächter-Hinweis „PSV reagiert nicht seit … s“ während des Scans = blockiert) | |
| 4-3 | `.svd` am Zielpfad; Dauer der Messung notieren (Zeitlimit, Punktdauer) | |
| 5-1 | „Abbrechen“ sendet genau ein `Acquisition.Stop`; danach `State` = Stopped innerhalb der Frist | |
| 5-2 | Datei mit Teilpunkten bleibt erhalten | |
| 6-1 | Bei einer vorhandenen Zieldatei erhält PSV keinen Aufruf (Vorprüfung bzw. Adapter) | |

## Abbruchkriterien (sofort aufhören, Befund sichern)

- unerwarteter Dialog in PSV
- Laser oder Spiegel bewegt sich außerhalb von T4 bis T6
- ein Eintrag unter `verweigert:` bzw. „verweigert“ in der Oberfläche, den du nicht bewusst
  provoziert hast
- Oberfläche oder PSV reagiert länger als die Wächtergrenze nicht
- eine vorhandene Datei wurde verändert
- Generator gibt unerwartet aus
- `psv_prozesse` enthält einen anderen Prozess als PSV (Fehltreffer, siehe Schalter oben)
- der erste Poll nach `ScanEx` liefert `Stopped` (4-1a), obwohl der Scan danach läuft:
  Der Start ist dann asynchron, die Steuerung hält den eigenen Scan für beendet und der
  Adapter würde ihn als fremd behandeln und **nicht stoppen**. Sofort aufhören, PSV
  manuell stoppen, Befund melden. Eine Karenzlogik im Code ist bewusst noch nicht
  eingebaut (Entscheidung nach Montag).
- `State` wird nach `Stop` nicht Stopped (Oberfläche zeigt `GERAET_UNKLAR`): PSV manuell
  prüfen, keine weiteren Messtests

Nach einem Abbruch: Python-Konsole bzw. Programm schließen. PSV nicht beenden, solange
eine Messung läuft; den Zustand in PSV selbst prüfen.

## Was zu sichern ist

- Ausgabe der Konsole bzw. die Durchgangsordner (Protokolle, Ereignis-JSONL)
- Aufrufprotokoll (`g.aufrufe()`) und Verweigerungen
- Notizen zu den Tabellen oben (ok/nicht ok, Werte)

Alles nach `in_progress/versuche/2026-11-02_prototyp/` kopieren; danach `/laborbuch`.

## Ergänzung U5 (Integration): T0, T1 und Startdialog

**Vorbereitung (Cloud/Entwicklungsrechner, vor Montag):** aus `software/` nur
`uv build --wheel`. Der Build-Hook (`software/hatch_build.py`, K-U5) schreibt Git-Hash und
Dirty-Flag beim Bau selbst ins Wheel (`ldv_automation/_build_info.json`); ohne Git bricht
der Bau ab. Ohne Build-Info und ohne Git ist `MESSEN` am Messrechner gesperrt.

**Konfiguration (K-U5):** Schalter aus der Erkundung (Validator-Rückfall S4, Lademaske,
Aufrufgrenze, Wächterwarnung, Stop-Frist, Standard-Zeitlimit) in eine Kopie von
`software/konfig/beispiel_messrechner.json` eintragen und mit `--konfig DATEI` übergeben
(gui und selbsttest). Eine ungültige Datei bricht den Start mit Meldung ab. Pfad, SHA-256
und Werte stehen in jedem Messprotokoll und im Dialog „Gerät“.

**T0:** `python -m ldv_automation selbsttest` (und mit `--konfig DATEI`) muss mit „Selbsttest bestanden“ enden
(Simulator, ohne pywin32, ohne Oberfläche). Mit `--ordner D:\Messdaten\selbsttest`
bleiben die Ergebnisse zum Kopieren erhalten. Vorher in Linux geprüft, unter Windows
**noch nicht**.

**T1 (NUR_LESEN), zusätzlich:** Dialog „Gerät …“ prüfen:
- „Aufrufprotokoll“ muss „N Zugriffe, keine Verweigerung“ zeigen. Jede Verweigerung:
  stoppen, Text notieren.
- „Messpunkte“ und „Generator“ (beim Verbinden gelesen) mit der PSV-Oberfläche
  vergleichen (GeneratorsOn, Aktiv, Amplitude). Beim Verbinden wird dafür zusätzlich der
  Einstellungsstand nur lesend abgefragt.
- „Hardware“ enthält `psv_prozesse` (Treffer der Prozessprüfung), „Lademaske“ ist gesetzt.

**Einstellungen:** Messdaten-Ordner und Standard-Zeitlimit werden gemeinsam übernommen
oder gar nicht. Die Sitzung lehnt relative Pfade, Netzwerkpfade, Programm-, Daten- und
Systemordner, Polytec-Ordner unter der Laufwerkswurzel und Git-Repositorys ab (Details
unten).

**Startdialog (T4):** Messpunkte und Generator je Messung werden aus dem Trockenlauf
übernommen, wenn danach dasselbe PSV läuft (gleicher Prozess-Treffer), die Lademaske gleich
und die `.set` unverändert ist (K-U5b). Die Spalte „Generator“ zeigt dann „(übernommen)“,
der Tooltip „gelesen in Betriebsart TROCKENLAUF vom …“; dieselbe Angabe steht im
Ereignisprotokoll des Durchgangs (`startangaben`). Werte aus dem Simulator gelten nie. Nach
„Trennen“ oder bei geänderter `.set` steht „unbekannt“ mit roter Warnzeile. Werte mit der
PSV-Oberfläche vergleichen; bei roter Zeile nur mit Freigabe von Shaker/Verstärker
fortfahren.

**Messdaten-Ordner (K-U5b):** Abgelehnt werden Ordner unter ProgramFiles, ProgramW6432,
ProgramData und SystemRoot sowie Ordner „…Polytec…“ direkt unter einer Laufwerkswurzel;
Pfade werden vorher aufgelöst (`..`, Junctions, Kurznamen). Ein Benutzerkonto wie
`C:\Users\Polytec\…` ist erlaubt. Bitte notieren, wo PSV am Messrechner Daten ablegt.