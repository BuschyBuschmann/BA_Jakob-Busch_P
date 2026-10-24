# Erkundung am PSV-Messrechner (nur Lesen)

Einzeldatei-Werkzeug `erkundung.py` (Version 0.1.0). Es sammelt Fakten für den Entwurf des
COM-Adapters und gehört **nicht** zum Hauptpaket `ldv_automation` (kein Import daraus).
Grundlage: Plan E1 und COM-Referenz I5 (`in_progress/analysen/`), Prüfliste I5 Abschnitt 10.

## Prüfanleitung für den Nutzer

**Wichtig vorab.** Das Skript misst nicht, schaltet keinen Laser, ändert keine Einstellungen
und überschreibt keine Datei. Es liest nur Versionen, Registry-Einträge und den aktuellen
Zustand von PSV. Es beendet PSV nie und startet PSV nur, wenn du es ausdrücklich mit
`--start-psv` verlangst und die Rückfrage mit `JA` bestätigst.

**Hardwaretest-Status.** Bis du das Ergebnis bestätigt hast, ist kein Prüfpunkt am Gerät
bestätigt (Ablauf G). Das Ergebnis wird per `/laborbuch` festgehalten.

### Vorbedingungen

1. Zustimmung geklärt (Frage F4) bzw. du nutzt eine Variante ohne Installation. Das Skript
   braucht **Python 3.11** (Projektvorgabe). Stufe 1 braucht zusätzlich **pywin32**. Stufe 0
   nutzt nur die Standardbibliothek. Bei Python < 3.11 meldet das Skript sofort „braucht Python
   3.11 oder neuer“ (Exit-Code 2), legt nichts an und liest nichts. Die Datei ist so
   geschrieben, dass sie bis zu diesem Check auch unter älteren Versionen parsebar ist
   (geprüft mit Python 3.8 und 3.10).
2. Bei Stufe 1: PSV läuft im **Datenerfassungsmodus**, Messsystem eingeschaltet wie für eine
   normale Messung, **keine laufende Messung**. Kein Prüfling nötig. Der Generator-Ausgang
   darf nicht an einen Shaker/Verstärker angeschlossen sein oder muss aus sein (nur
   Sicherheitsvorsicht; es wird nichts ausgegeben).
3. Für Stufe 1b: eine vorhandene Messdatei (z. B. `Example.svd`), **nicht** in PSV geöffnet.
   Besser eine Kopie (das Skript öffnet sie nur schreibgeschützt).
4. Ausgabeordner auf einem beschreibbaren Laufwerk (nicht in Polytec-Verzeichnissen). Ohne
   `--out` entsteht er neben dem Skript.

### Schritte

1. `erkundung.py` auf den Rechner kopieren (z. B. `C:\Users\<du>\erkundung\`).
2. Eingabeaufforderung oder PowerShell öffnen, in den Ordner wechseln.
3. **Stufe 0 zuerst allein** (PSV dabei noch nicht starten):
   `python erkundung.py --stufe 0` (ca. 1 Minute). Danach `zusammenfassung.md` und
   `registry.reg.txt` ansehen, besonders `P1-2-registry`: Ist `PSV.AcquisitionInstance` als
   `LocalServer32` (eigene EXE) registriert, kann COM diese EXE beim Anlegen des Objekts selbst
   starten. Deshalb gilt die Sperre unten.
4. PSV im Erfassungsmodus öffnen, **keine Dialoge offen lassen**. Stufe 1:
   `python erkundung.py --stufe 1`. Das Skript führt Stufe 0 mit aus und meldet pro Prüfpunkt
   die Dauer. **Sperre:** `PSV.AcquisitionInstance` wird nur angelegt, wenn Stufe 0 in der
   Prozessliste einen laufenden PSV-Prozess (Name enthält „psv“) gefunden hat; sonst steht
   `P1-5-verbinden` auf `uebersprungen`, und der COM-Teil von Stufe 1 läuft nicht. Ausnahme:
   `--start-psv` mit Bestätigung `JA`. Stufe 1b (PolyFile) ist davon nicht betroffen.
5. Optional 1b: `python erkundung.py --stufe 1 --datei "<Pfad>\Example.svd"`. Stufe 1b läuft
   auch, wenn PSV nicht läuft.
6. Ausgabeordner prüfen (`zusammenfassung.md` öffnen) und ins Repository legen:
   `in_progress/versuche/erkundung/` (den ganzen Ordner `erkundung_<Rechnername>_<Zeit>/`,
   ggf. als ZIP).
7. Zusätzlich manuell festhalten (ohne Skript): PSV-Version und Optionen laut
   *Hilfe > PSV Info* (P1-3, Screenshot oder Text). Die Lizenzen sind per COM nicht belegt
   (I5 6).
8. Notieren, ob irgendein Fenster in PSV aufgepoppt ist oder PSV sich anders verhielt.

### Abbruchkriterien (sofort Strg+C, danach den Ordner trotzdem hochladen)

- PSV zeigt unerwartet einen Dialog, einen Fehler oder reagiert nicht mehr.
- Das Skript meldet „blockiert bei ...“ oder es passiert länger als der Watchdog
  (`--timeout-s`, Standard 60 s) nichts. Das Skript beendet sich dann selbst und schreibt
  vorher den Teilbericht.
- Der Laser schaltet sich ein oder aus oder ein Spiegel bewegt sich. Das darf nicht passieren.
  **Wenn doch, Skript abbrechen und melden**; das wäre ein Befund zur Whitelist.
- Das Skript meldet „verweigert (Default deny)“ oder der Bericht enthält Einträge unter
  `verweigert`. Das ist ein Skriptfehler und wird gemeldet (Exit-Code 1).

**Erwartete Dauer** [Einschätzung, nicht gemessen]: Stufe 0 ca. 1 Minute, Stufe 1 und 1b ca. 5
bis 15 Minuten einschließlich Vorbereitung.

**Was geht ins Repository:** der Ausgabeordner (JSON, Markdown, Logs, Registry-Text); keine
Messdaten. Der Benutzername ist standardmäßig durch `<user>` ersetzt (`--keep-user` hebt das
auf), der Rechnername steht im Klartext. Seriennummern von Geräten bleiben im Bericht. Bitte
vor dem Upload kurz durchsehen.

## Kommandozeile

| Schalter | Wirkung |
|---|---|
| `--stufe {0,1}` | 0: ohne COM (Standard). 1: zusätzlich COM lesend; führt Stufe 0 mit aus |
| `--datei PFAD` | Stufe 1b: Messdatei nur schreibgeschützt lesen (nur mit `--stufe 1`) |
| `--start-psv` | PSV starten, falls es nicht läuft; verlangt die Eingabe `JA` (nur Stufe 1) |
| `--out ORDNER` | Ordner, in dem der Ausgabeordner angelegt wird (Standard: neben dem Skript) |
| `--keep-user` | Benutzernamen nicht entfernen |
| `--timeout-s S` | Watchdog je Prüfpunkt (Standard 60) |
| `--max-punkte N` | Messpunkte am Anfang und am Ende (Standard 3) |
| `--max-werte N` | Datenwerte aus `GetData` im Bericht (Standard 6) |

Exit-Codes: 0 normal, 1 Zugriff verweigert, 2 Aufruffehler oder Python zu alt, 3 blockiert,
4 interner Fehler außerhalb eines Prüfpunkts (z. B. Schreibfehler; Restpunkte stehen als
`uebersprungen` im Bericht, `lauf.status` ist `fehler`), 130 Strg+C. Schreibfehler beim
Bericht (z. B. durch einen Virenscanner) werden kurz wiederholt, bevor sie als Fehler zählen.

## Sicherheitskonzept

- Jeder COM-Zugriff läuft über einen Whitelist-Proxy (Default deny, `POLICY` im Skript):
  Nur dort aufgeführte Typen, Properties und Methoden werden weitergereicht, Rückgabewerte
  sind entweder einfache Werte oder wieder Proxys. Über den Proxy sind private Namen,
  Zuweisungen und Löschen gesperrt. Einzige erlaubte Zuweisung: `PolyFile.ReadOnly = True`.
  Der Proxy schützt vor Fehlern im eigenen Skript, nicht vor Absicht: Ein Slot-Zugriff auf das
  interne Attribut `_obj` im Python-Code würde das rohe COM-Objekt liefern.
- Die `BLACKLIST` im Skript ist nur ein Testkatalog (jeder Eintrag hat einen Test).
- Start von PSV (`GetApplication(True, ...)`) ist ohne `--start-psv` samt Bestätigung gesperrt.
- Eine laufende Messung wird nie angefasst (kein `Stop`, kein `Start`).
- Das Skript ruft selbst kein `makepy` und kein `gencache.EnsureDispatch` auf. **Aber:**
  pywin32 kann schon beim `import win32com.client` (Stufe 0, `P1-4-pywin32`) selbst einen
  `gen_py`-Cache im pywin32-Verzeichnis anlegen [nach pywin32-Quelltext, unter Windows nicht
  geprüft]. Das betrifft keine Polytec-Dateien, ist aber ein Schreibzugriff außerhalb des
  Ausgabeordners, den das Skript nicht verhindern kann.
- Mit Late Binding (`Dispatch` ohne Typinformation) kann pywin32 beim Zugriff auf einen
  unbekannten Namen die Property „lesen“ wollen. Betroffen wären nur freigegebene Mitglieder
  (kein Schreib- oder Messbefehl); ob PSV/PFA Typinformation liefern, ist ungeprüft.
- Die Konstantenprüfung (`P1-4-typelibs-com`) läuft bewusst zuletzt; sie ist nur
  aussagekräftig, wenn pywin32 Typbibliotheks-Wrapper geladen hat. Fehlen die Konstanten, steht
  die Ursache als nicht geprüft im Bericht.
- Sonst werden Dateien nur im neuen Ausgabeordner geschrieben; kein Netzwerk, kein
  `eval`/`exec`/`pickle`.
- Schwärzung (`<user>`) nur in personenbezogenen Kontexten, nie als freies Wort im Fließtext
  (Konten heißen oft „Polytec“ oder „Labor“; Pfade, Typbibliotheksnamen und
  `SummaryInfo`-Inhalte bleiben deshalb erhalten): (1) die Profilpfade aus `USERPROFILE` und
  `Path.home()` (auch mit Leerzeichen), (2) jedes Segment direkt unter `<Laufwerk>:\Users`, `/home`
  und `/Users` außer `Public`, `Default`, `All Users` (deckt abweichende Profilordner und
  8.3-Kurznamen wie `JAKOBB~1` ab; Registry-Pfade wie `HKCU\Software\Users` bleiben), (3) Werte von
  Feldern mit Personen- oder Kontonamen (z. B. `SummaryInfo.Author`), dort auch Anmelde- und
  Profilname als freies Wort. Grenzen: fremde Profile mit Leerzeichen nur bis zum
  Leerzeichen, Kontonamen sonst (z. B. `DOMAIN\jbusch` im Fließtext) werden nicht erkannt.
  Der Rechnername bleibt im Klartext.
- **Durchsicht vor dem Upload (Pflicht):** Dein Anmeldename kann in Pfaden außerhalb von
  `…\Users` ungeschwärzt stehen bleiben. Prüfe vor dem Hochladen gezielt diese Stellen in
  `bericht.json`, `zusammenfassung.md` und `konsole.log`:
  - `kommandozeile` und `parameter.datei` (Pfad aus `--datei`, z. B. `D:\Messdaten\<name>\…`),
  - `dateien.*.pfad` (Eingabedatei von Stufe 1b),
  - `Acquisition.ScanFileName` (zuletzt in PSV eingestellter Scan-Dateiname),
  - Netzlaufwerks-Pfade (z. B. `\\server\home$\<name>\…`),
  - Fehlermeldungen (`exception`, `excepinfo`), die Pfade oder Kontonamen enthalten.
  Fremde Personennamen in Messdateien (z. B. `SummaryInfo.Author`) werden bewusst nicht
  geschwärzt; sie gelten als Metadaten der Messung.

## Ausgabe

Neuer Ordner `erkundung_<Rechnername>_<JJJJ-MM-TT_HHMMSS>` (existiert er, wird `_2`, `_3` ...
angehängt; nie überschrieben):

| Datei | Inhalt |
|---|---|
| `bericht.json` | strukturierter Bericht, wird nach jedem Prüfpunkt neu geschrieben |
| `zusammenfassung.md` | Tabelle je Prüfpunkt, Abweichungen von I5, offene Fragen |
| `konsole.log` | vollständiges Konsolenlog |
| `registry.reg.txt`, `typelibs.txt` | Rohauszug der gelesenen Registry-Einträge |

### Schema von `bericht.json` (`schema_version` 1)

- `schema_version`, `skript_version`, `skript_sha256` (SHA-256 der Skriptdatei; kein Git-Hash,
  weil auf dem Messrechner kein Git vorausgesetzt wird)
- `zeitstempel_lokal`, `zeitstempel_utc` (ISO 8601 mit Zeitzone), `rechnername`,
  `benutzername_entfernt`, `kommandozeile`, `stufen`, `parameter`
- `lauf`: `status` (`laeuft` | `vollstaendig` | `blockiert` | `abgebrochen`), `hinweis`
- `umgebung`: Windows, Python (Version, Bitness, Pfad), `pywin32`
- `pruefpunkte[]`: `id`, `stufe` (`0` | `1` | `1b`), `titel`, `beleg_ref`, `status`
  (`ok` | `fehler` | `uebersprungen` | `blockiert`), `kernwert`, `hinweis`, `werte`,
  `auffaelligkeiten[]` (Einzelfehler beim Lesen), `dauer_s`, `exception` (`typ`, `meldung`,
  `hresult`, `hresult_hex`, `excepinfo`, `strerror`, `argerror`, `traceback_gekuerzt`);
  bei Blockade zusätzlich `letzter_aufruf`
- `abweichungen[]`: Abweichungen von der Erwartung aus I5 (`pruefpunkt`, `text`, `beleg_ref`)
- `whitelist_aufrufe[]`: **alle** weitergereichten Zugriffe in Reihenfolge (`nr`, `pruefpunkt`,
  `pfad`, `op`, `argumente`, `dauer_s`, `fehler`)
- `verweigert[]`: blockierte Zugriffsversuche (sollte leer sein)
- `dateien`: bei 1b Größe, mtime, SHA-256 der Eingabedatei vorher und nachher, `unveraendert`

### Prüfpunkte

| ID | Stufe | Inhalt |
|---|---|---|
| P1-1-umgebung, P1-4-pywin32 | 0 | Windows/Python/Bitness, pywin32 |
| P1-2-registry, P1-2-dateien | 0 | ProgIDs, CLSID, Server (64- und 32-Bit-Sicht), PE-Typ, Dateiversion |
| P1-4-typelibs-registry | 0 | registrierte Typbibliotheken mit „Poly“/„PSV“/„VibSoft“ |
| P1-3-verzeichnisse, P1-5-prozess | 0 | `Polytec`-Verzeichnisse, laufende PSV-Prozesse |
| P1-4-typelibs-com | 1 | (läuft zuletzt) `EnumTlbs`, Vergleich der Konstanten mit I5 Abschnitt 8 |
| P1-5-verbinden, P1-5-application | 1 | `IsRunning`, `GetApplication(False)`, Version, Mode |
| P1-6-zustand | 1 | `State`, Mode, Generator, Laser (`GetLaserOn`) |
| P1-6-eigenschaften | 1 | Gruppen, FFT/Mittelung/Allgemein, Validator vorhanden? |
| P1-6-hardware, -scankopf, -vibrometer | 1 | Hardware, Scankopf, Controller und Sensorkopf-Infos (Seriennummer, Firmware, Laserwellenlänge, Laserleistung) |
| P1-6-messpunkte, P1-6-abgleich | 1 | Messpunkte (Index/Label), Abgleich 3D/2D |
| P3-2-existenz | 1 | `PositionDevice`, `DigitalPorts` (nur Existenz) |
| P1-10-oeffnen, -struktur, -daten, -schliessen | 1b | Datei, Domänen/Kanäle, `GetData`, `XAxis` |

Alle diese Punkte sind **am Gerät unbestätigt**, bis der Nutzer das Ergebnis bestätigt.

Die Kennzahlen in `P1-10-daten.abgeleitet` mit Endung `_LIVE_PSV` stammen aus der aktuellen
PSV-Konfiguration (Stufe 1), nicht aus der Datei; ein Hinweisfeld nennt das.

## Abweichungen vom Plan

Vom Nutzer nach Review R-E1 übernommen (Plan-Nachtrag 2026-10-23):

- **Vibrometer:** Gelesen werden `ControllerInfo` (DeviceName, FirmwareVersion, Name,
  SerialNumber) und zusätzlich über den dokumentierten Weg
  `Infos.Vibrometers(g).Controllers(c).SensorHeads(s).SensorHeadInfo` Name, SerialNumber,
  FirmwareVersion, LaserWavelength und LaserPower ([BEM] „Access to General Information“,
  `ISensorHead~SensorHeadInfo`). Vibrometers ist 1-basiert, Controllers und SensorHeads sind
  0-basiert. Nur lesend und über die Whitelist.
- **Kein `pytest`-Test mit Marker `hardware`** für dieses Werkzeug (`pytest` auf dem
  Messrechner widerspräche der Variante ohne Installation). Der Marker bleibt für spätere
  Pakete registriert.
- **Y-Achse** über `Signal.Description.YAxis` statt `GetYAxes` (gleichwertig).
- **Typbasierte Whitelist** statt Pfadmuster; **kein `--makepy`**; Stufe 1 enthält Stufe 0;
  Watchdog je Prüfpunkt (siehe Rückmeldung zu E1-U).
- **Technische Sperre** des COM-Teils von Stufe 1 (siehe Prüfanleitung).

## Entwicklung

Aus `software/`: `uv run pytest` (Tests gegen Fake-PSV, laufen ohne Windows), dazu
`uv run ruff check .`, `uv run ruff format --check .`, `uv run mypy --strict .`. Die
Windows-Adapter (`winreg`, `ctypes`/`version.dll`, `win32com`) sind mit `# pragma: no cover`
begründet ausgenommen. Tests: `software/tests/tools/erkundung/`.
