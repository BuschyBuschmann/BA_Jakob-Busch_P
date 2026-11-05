# Ablaufplan: nächster Termin am Messrechner (Entwurf zur Freigabe)

**Status:** ENTWURF (überarbeitet nach Fachprüfung FD-P3), nicht freigegeben · **Datum:** JJJJ-MM-TT (unbekannt) · **Rechner:** BEOWOLF
**Bearbeiter am Rechner:** Jakob (mit dem Orchestrator direkt, KONVENTIONEN „Arbeitsweise bei Terminen vor Ort“)
Paket P3 (Planung). Dazu gehören [protokoll.md](protokoll.md) (zum Ausfüllen) und [pruefzettel.md](pruefzettel.md) (Kurzliste zum Abhaken).

**Wunsch des Nutzers:** am Termin variabler reagieren können, wenn etwas wie die COM-Schnittstelle nicht
funktioniert. Deshalb ist der Plan **kein linearer Ablauf**, sondern ein Satz von Blöcken mit
Entscheidungsbaum. Jeder Abschnitt nennt **Weiter**, **Abbruch** und **Ersatz**.

**Termindauer (Entscheidung des Nutzers 2026-11-02):** Jakob klärt mit Daniel einen längeren Termin, z. B. 4 h. Geplant wird mit **ca. 240 min [Annahme, nach Klärung mit Daniel]**.
Für den Fall, dass es doch nur ca. 150 min werden, gibt es eine verkürzte Reihenfolge (Abschnitt 4.2). Die Software-Version des neuen Wheels ist **0.2.0** (Entscheidung des Nutzers).

Kennzeichnung: **[Annahme]** = nicht belegt, **[offen]** = muss geklärt werden, **[Wissen]** = allgemeines
Wissen, am Gerät nicht geprüft, **[N]** = Nachrechnung der Fachprüfung (FD-P3) bzw. des Experten, nicht am Gerät geprüft. Alle **Dauern sind grobe Annahmen** (nicht gemessen) und dienen nur der Priorisierung.
Nichts hier ist freigegeben: weder eine Messung noch die Anregung noch ein Eingriff in den Aufbau.

Grundlagen: [Laborbuch 2026-11-02](../../laborbuch/2026-11-02_messrechner-erster-termin.md),
[Tagesanalyse](../2026-11-02_prototyp/tagesanalyse.md), [Ergebnisse 7b](../2026-11-02_prototyp/ergebnisse_7b.md),
[COM-Registrierung](../2026-11-02_prototyp/com_registrierung_psv104.md), [Rückfragen](../2026-11-02_prototyp/rueckfragen_heute.md),
[alter Ablaufplan](../2026-11-02_prototyp/ablaufplan_vor_ort.md), [Übersicht nach dem Termin, Abschnitt 1 und 2a](../../analysen/2026-11-02_nach-termin_uebersicht.md),
[Installation](../2026-11-02_prototyp/installation_messrechner.md), [Erkundung-README](../../../software/tools/erkundung/README.md),
[Prüfanleitung U3](../2026-11-02_prototyp/pruefanleitung_U3_com-adapter.md), [Test-.set](../2026-11-02_prototyp/anleitung_test_set.md).

---

## 1 Grundregeln (aus dem alten Plan übernommen, gelten den ganzen Termin)

1. **Eine echte Messung läuft nur nach deiner eigenen ausdrücklichen Entscheidung** (Zeit, Entscheidung, Grund ins
   Protokoll). Das gilt für jeden Scan, auch den Mini-Scan (D1) und jede Einzelpunktmessung, ob über das Programm oder direkt in PSV.
   Über das Programm nie, bevor T1 und T2 ohne Befund durch sind. Ein Hardwaretest gilt erst als bestanden, wenn du ihn bestätigt hast.
2. **Shaker erst nach Freigabe.** Solange die Anregung nicht freigegeben ist (Frage F2, Daniel), bleibt der Shaker
   (TMS Mini SmartShaker mit eingebautem Verstärker) vom Netz bzw. das Signalkabel getrennt, und der Generator
   wird nicht eingeschaltet. Die Freigabe wird mit Name und Uhrzeit ins Protokoll geschrieben; sie wird nie unterstellt.
3. **Rohdaten nie überschreiben** (KONVENTIONEN). Neue Messdateien erhalten neue Namen (Vorschlag [Annahme]:
   `JJJJMMTT_<zweck>_<nn>.svd`, angelehnt an `20261012_ref_Mitte.svd`). Vorhandene Dateien werden nicht gespeichert, verschoben oder umbenannt.
4. **Kopien für File Access.** Die Beispieldatei und jede andere Messdatei werden nur als Kopie mit
   File Access geöffnet, und nur, wenn sie nicht in PSV geöffnet ist (Ausnahme: gezielter Test C7, mit Kopie).
5. **Nur eine PSV-Instanz.** Vor jedem COM-Test `Get-Process PSV` prüfen, PID notieren. PSV nie per Skript starten
   (`--start-psv` nicht verwenden).
6. **Nach einem Hänger die Anwendung nicht einfach weiterbenutzen** (siehe Ersatzplan EP-5). Das Programmfenster
   nicht im pausierten Zustand schließen.
7. **Ordner lokal, nicht im Repository:** Messdaten nicht unter ProgramFiles/ProgramData/Windows, nicht in einem
   Ordnerteil „Polytec“ direkt unter der Laufwerkswurzel, nicht in einem Git-Repository. Ob `PyCharmProject` ein Git-Repository ist, ist **[offen]**
   (Rückfrage C1 vom letzten Mal); deshalb Messdaten **nicht** darunter ablegen.
8. **Service- und Kalibriermethoden des Scankopfs werden nie aufgerufen**; per COM nur Lesen, außer in den
   ausdrücklich freigegebenen Prototyp-Tests.
9. **PSV nicht beenden, solange eine Messung läuft.** Beim Schließen von PSV auf „Speichern?“ immer „Nein“ (Auswertungs-Kopien).
10. **Fotos des Aufbaus vor jeder Änderung am Aufbau** (Wiegen E1, Verlegen von Kabeln, Impedanzkopf).

Arbeitsvariablen für alle PowerShell-Befehle unten (Pfade aus dem letzten Termin; Skriptordner **[Annahme]**: `erkundung.py` lag dort laut
[COM-Registrierung](../2026-11-02_prototyp/com_registrierung_psv104.md); wo `einstellungen_lesen.py` und `daten_lesen.py` liegen, ist **[offen]**):

```powershell
$PY  = "D:\Messdaten\DAL\BA Jakob Busch\PyCharmProject\.venv\Scripts\python.exe"
$ARB = "D:\Messdaten\DAL\BA Jakob Busch"          # Skripte, erkundung\, daten\  [Annahme]
$T   = "$ARB\termin_JJJJ-MM-TT"                    # Ausgaben dieses Termins  [Annahme, Datum einsetzen]
mkdir "$T\erkundung","$T\daten","$T\export","$T\fotos" -ErrorAction SilentlyContinue
```

Aufruf immer mit `& $PY ...` (der Pfad enthält Leerzeichen). Das Venv wird nicht aktiviert.

---

## 2 Entscheidungsbaum: was tun, wenn X blockiert?

Der Baum ist die Hauptstütze des Termins. Er wird an den Knoten K1 bis K9 durchlaufen; Ergebnis und gewählter Pfad kommen
ins Protokoll (Abschnitt 2). Die Pfade sind **A** (COM funktioniert), **B** (COM aus) und die Zusatzzweige D (Anregung) und E (ohne PSV).

```
START
 |
 K1  Nur 1 PSV-Prozess oder keiner?  (Get-Process PSV)
 |    nein (2 oder mehr) --> Ruhe. Prüfen: läuft eine Messung, steht ein Dialog offen? Nein: überzählige Instanz
 |                           regulär schließen (Speichern: Nein). Nicht per Task-Manager beenden, solange unklar (EP-5).
 |    ja ----------------+
 |
 K2  Erkundung Stufe 0 (PSV darf noch zu sein): PSV.AcquisitionInstance registriert?
 |    ja, LocalServer32 = ...\PSV 10.4\PSV.exe --> K4
 |    ja, aber zeigt auf 10.2/10.3 -------------> Befund sichern, Daniel fragen (nur eine Version registrierbar), erst dann K3
 |    nein ------------------------------------> K3
 |
 K3  Registrierung nachholen (nur mit Zustimmung von Daniel, A2)
 |    Daniel da und stimmt zu --> PSV.exe /regserver (Admin), Stufe 0 neu --> registriert? ja: K4
 |                                                                         nein: Reparaturinstallation (Daniel) --> ja: K4
 |    Daniel nicht erreichbar / keine Zustimmung / Versuch erfolglos ---> PFAD B (EP-1). Zeitlimit für K3: 30 min [Annahme].
 |
 K4  Installation/Update (A1) parallel zu K3 möglich. I1 bis I4 ok?
 |    ja --> weiter       nein --> EP-3 (alter Stand 530af41 oder nur Skripte), COM-Arbeit geht trotzdem weiter
 |
 K5  PSV über „PSV 10.4 Deutsch“ starten (/Acquisition), PID notieren, Stufe 1 (B1): Verbinden ok?
 |    ja --> PFAD A
 |    nein -> Fehlerbild sichern (bericht.json: P1-5-verbinden, hresult_hex, excepinfo).
 |            Läuft die Instanz wirklich mit /Acquisition? (CommandLine) nein: falscher Modus, neu starten, K5 wiederholen
 |            ja, Modus stimmt, trotzdem Fehler --> Desktop-Gegenprobe X1 (Diagnose) --> PFAD B (EP-1)
 |
 K6  Freigabe der Anregung (F2)?
 |    ja, mit Name/Uhrzeit --> Zweig D möglich (jeweils eigene Entscheidung je Messung)
 |    nein / unklar -------> Zweig D entfällt (EP-4), kein T4 bis T8, Shaker bleibt aus
 |
 K7  Läuft etwas schief in PSV (hängt, Dialog, Laser/Spiegel unerwartet)? --> EP-5, Befund sichern, ggf. Pfad wechseln
 |
 K8  Zeit: Rest weniger als geplant? --> EP-6 (Streichreihenfolge, Abschnitt 4)
 |
 K9  Ende: Sicherung A2, Protokoll abschließen. Immer, auch bei Abbruch.

PFAD A (COM an):  A0, A1, B1, X1 (am Ende), B2, B3, B4 (T0 bis T2) --> Entscheidung Messung --> Zweig D; dazu parallel Zweig C und E in Wartezeiten
PFAD B (COM aus): A0, A1 (nur Skripte/Datei), Zweig C (File Access auf Kopien), Zweig E, Simulator-Vorführung (EP-1), Prüfzettel ohne COM;
                  mit Anregung: Zweig D manuell in PSV (ohne Programm); PSV-Fehlerbild (X1) dokumentieren
```

### Tabelle: Blockade und nächster Schritt

| Was blockiert | Sofort | Weiter mit | Siehe |
|---|---|---|---|
| COM nicht registriert | Befund sichern (Stufe 0), Daniel anrufen | K3, sonst Pfad B | EP-1, A0 |
| Verbinden scheitert trotz Registrierung | Fehlerbild sichern, Modus der Instanz prüfen | X1 Gegenprobe, dann Pfad B | EP-1, EP-2 |
| PSV läuft im Desktop-Modus | Nur lesen und Fehlerbild notieren, nicht weiter COM-testen | Neustart über „PSV 10.4 Deutsch“ | EP-2 |
| Installation/Update scheitert | Meldung wörtlich sichern | alter Stand 530af41 bzw. nur Skripte | EP-3 |
| Keine Freigabe der Anregung | Shaker bleibt aus | Zweig C, E, B ohne Messung; D1 bis D4 entfallen | EP-4 |
| PSV hängt oder Dialog | Nichts anklicken, was nicht eindeutig ist; Foto | Zustand prüfen, dann entscheiden | EP-5 |
| Zeit wird knapp | Streichliste, Sicherung vorziehen | Muss zuerst | EP-6, Abschnitt 4 |
| Datei lässt sich mit File Access nicht öffnen | Kopie prüfen, nicht in PSV geöffnet? | PSV-Oberfläche statt Skript | EP-7 |
| Daniel nicht erreichbar | nichts ohne Zustimmung ändern | Pfad B, Fragen sammeln | EP-1 |

---

## 3 Vorbereitung vor dem Termin

### 3.1 Fragen an Daniel (vor dem Termin klären; Antworten ins Protokoll Abschnitt 1)

| Nr | Frage | Auswirkung |
|---|---|---|
| F1 | **Ist die COM-Registrierung erfolgt** (wer, wann, Befehl)? Ist 10.4 die registrierte Version, und ist 10.2/10.3 noch im Einsatz (A1/A2 vom letzten Mal)? | Pfad A oder B |
| F2 | **Ist die Anregung (Shaker/Verstärker) freigegeben?** Wofür genau (Mini-Scan, Zwei-Amplituden-Test, Wiederholungsmessung T8)? Bis zu welcher Generator-Amplitude? | Zweig D |
| F3 | Termin: Datum, Beginn, Ende; **ist ein längerer Termin (z. B. 4 h) möglich?** Ist Daniel erreichbar (Registrierung, Rückfragen)? | Zeitplan (240 min nur nach Klärung), Streichliste |
| F4 | Darf beim Mini-Scan `SaveTimeDataForScan` an sein (setzt Signal Enhancement auf „Fast“, nur Testscan)? Wo dürfen die Zeitdaten-Dateien liegen (Größe unbekannt)? | D1 |
| F5 | Gibt es eine Waage (Genauigkeit, Messbereich) und darf der Impedanzkopf bzw. die Platte dafür aus dem Aufbau genommen werden? | E1 |
| F6 | Darf der Laser auf den Impedanzkopf gerichtet werden? **Darf eine kleine Reflexfolie (flach, einige mm²) auf die Stirnfläche des Impedanzkopfs geklebt werden** (Zustimmung Daniel; Spray statt Folie als Alternative)? Wenn nein oder Kopf nicht einsehbar: Ersatzpunkt auf der Plattenvorderseite gegenüber der Kopfmontage. | D2 |
| F7 | Darf der Rechner ins Internet bzw. auf GitHub (A4 vom letzten Mal); darf ein Stick benutzt werden? | Installationsweg A1 |
| F8 | Dürfen die Handbücher aus dem Programmordner kopiert werden (Lizenz/Ablage in `Input/literatur/polytec/`)? | E2 |

### 3.2 Auf dem Entwicklungsrechner (Orchestrator/Jakob, **[offen]**, nicht Teil dieses Plans)

- Wheel **0.2.0** (Version entschieden) nach dem letzten Commit neu bauen (`version` in `software/pyproject.toml` auf 0.2.0), **gepusht**, Build-Info mit `git_dirty: false`; Git-Hash und SHA-256 der Wheel-Datei notieren. Dateiname erwartet `ldv_automation-0.2.0-py3-none-any.whl` **[Annahme, Standardschema]**; Ablageort im Repository **[offen]**.
  **Nachtrag 2026-11-03 (erledigt):** gebaut aus 6d84318 (`git_dirty: false`; ersetzt die nicht ausgelieferten Builds f66af80 und b5300e1), abgelegt unter `in_progress/versuche/naechster-termin_messrechner/stick/wheelhouse/`, SHA-256 `e6c3940830e81eb75fa5bd156b9d4563e1e838a5168c10be89f93e432f9bc96f`; Skripte und Hashes in `stick/LIESMICH.txt`. Seit 530af41 geändert: K-ACHSE (Auswertung) und K-2D (COM-Adapter: Hinweise bei fehlender Registrierung/Desktop-Modus, SignalDelay lesen) – die Aussage „Adapter unverändert“ unten gilt damit nicht mehr.
  **Nachtrag 2026-11-05 (offen):** Der Build 6d84318 wird durch einen neuen Build mit gleicher Versionsnummer 0.2.0 ersetzt (Reiter „Auswerten“ mit neuen Laufzeitpaketen matplotlib 3.11.2 mit Abhängigkeiten, olefile 0.47, tzdata 2026.6; Pins laut `software/tools/wheelhouse/erzeuge_wheelhouse.py`). Die SHA-256 `e6c39…` gilt danach nur noch für 6d84318. Offen und vom Orchestrator nach dem Bau einzutragen: Wheel-Name **[folgt]**, Git-Hash des Builds **[folgt]**, SHA-256 **[folgt]**, Ablageort **[folgt]**, Wheelhouse mit den neuen Paketen unter `stick/wheelhouse/` **[folgt]**.
  Stand heute (geprüft): Das Wheel in Git ist noch der Build 530af41; im Arbeitsverzeichnis liegen noch nicht eingecheckte Änderungen unter
  `software/src/ldv_automation/auswertung/` (K-ACHSE, `git status`). Der COM-Adapter ist seit 530af41 **unverändert** (`git diff 530af41..HEAD -- software/src` ist leer).
- Skripte `erkundung.py`, `einstellungen_lesen.py`, `daten_lesen.py` im aktuellen Stand (nach Review: Exit-Codes, Spaltenlängen) bereitstellen.
- Für Golden File v2 (C3): `daten_lesen.py` hat eine feste Signalliste (`AUSWAHL`, 8 Signale). Die Namen für Kohärenz, H2, PSD/ESD, Terzen stehen in der Erkundung 1b **nicht**
  (die Erkundung listet nur bis zu 8 Kanäle und 6 Signale je Kanal, `MAX_CHANNELS = 8`, `MAX_SIGNALS = 6`; die Domäne „Terzen“ wird nicht aufgelistet). Entweder die Liste vorher erweitern (Paket SKRIPTE) oder am Termin
  die Namen in PSV ablesen (C3, Ersatz).
- Für M11 (C2) **vorab prüfen** (Fachprüfung): Die Kennzeichenfreiheit der Kandidaten (617,9; 631,7; 644,8; 693,5; 757,3; 867,9 Hz) gilt in FG-02 Abschnitt 8 am **Punktmittel**, nicht am Einzelpunkt. Am Entwicklungsrechner mit der Stufe-1-Spitzenerkennung am gewählten Punkt (Label 132 oder anderer) bestimmen, welche Kandidaten dort ohne Kennzeichen sind. **Erledigt (V2):** an Label 132 gewählt 921,5 / 632,5 / 483,8 Hz, Reserve 949,3 / 644,8 Hz (siehe C2).
- Für D1/D2 offline vorbereiten: Auswerteweg für die Phasen-/Betragsauswertung von D2 (Fit φ(f), |H1|·ω) und die eigene FFT je Block (D1); Testdaten für B5 (siehe B5).
- SHA-256 der vorhandenen Handbücher unter `Input/literatur/polytec/Handbücher/` notieren, um am Termin zu erkennen, ob die 10.4-Fassung abweicht (E2). Die Version der vorhandenen Handbücher ist **[offen]**.
- Am Messrechner genügt das normale `pip install --upgrade --no-deps`, wenn dort 530af41 (0.1.0) steht. War 6d84318 (gleiche Version 0.2.0) installiert, ist `--force-reinstall` nötig (A1, Schritt 3).

### 3.3 Mitnehmen / bereitlegen

- [ ] Stick mit: aktuellem Wheel, Skripten, Konfigvorlage `beispiel_messrechner.json`, diesen drei Dateien (ausgedruckt: Prüfzettel), Python-Installer 3.11.9 (Rückfall)
- [ ] Handy/Kamera für Fotos; Maßband oder Messschieber (Maße der Platte, Position des Impedanzkopfs) **[Annahme: nützlich]**
- [ ] Notizzettel für PID und Uhrzeiten (falls Protokoll nicht offen ist)

---

## 4 Zeit, Priorität, Streichreihenfolge

### 4.1 Planung mit ca. 240 min

Termindauer: **ca. 240 min [Annahme, nach Klärung mit Daniel]** (F3; Jakob klärt z. B. 4 h). Letztes Mal waren es 150 min (14:30 bis 17:00).
Der **Muss-Block** summiert sich nach den Dauer-Annahmen auf 180 min (A0 15 + A1 20 + B1 15 + B2 20 + B3 30 + B4 50 + A2 30) und passt damit mit T0 bis T2 vollständig hinein.
Verbleiben ca. 60 min. Die Soll-Punkte summieren sich auf ca. 220 min (D2 40, C2 30, E1 15, C3 20, D3 30, E2 10, D1 50, C4 10, X1 15) und passen **nicht alle**; es gilt die Rangfolge unten.
Wartezeiten (Registrierung mit Daniel, Scandauer, Download) werden mit Zweig C und E gefüllt, weil diese weder COM noch Anregung brauchen; dadurch rückt mehr hinein, als die Summe vermuten lässt (nicht belegt).

| Nr | Abschnitt | Dauer (Annahme) | Priorität | Voraussetzung COM | Voraussetzung Anregung | Voraussetzung Datei (Kopie) |
|---|---|---|---|---|---|---|
| A0 | Schritt 0: Registrierung, Stufe 0, PSV-Instanz | 15 min (+ 15 min bei Registrierung mit Daniel) | **Muss** | nein | nein | nein |
| A1 | Installation/Update der Software (Wheel 0.2.0) | 20 min (gekürzt 10 min) | **Muss** | nein | nein | nein |
| B1 | Erkundung Stufe 1 (und 1b) | 15 + 10 min | **Muss** (bei COM) | ja | nein | 1b: ja |
| B2 | Ergebnisse sichern, Schalter, Konfigurationsdatei | 20 min | **Muss** (bei COM) | ja | nein | nein |
| B3 | Test-.set anlegen | 30 min | **Muss** für T2, sonst Soll | nein (PSV läuft) | nein (Generator aus) | nein |
| B4 | Prototyp-Prüfung T0, T1, T2 | T0 in A1, T1 20 + T2 30 min | **Muss** (bei COM) | ja | nein | nein |
| A2 | Sicherung und Rückmeldung | 30 min | **Muss** | nein | nein | nein |
| D2 | Messpunkt auf dem Impedanzkopf (Vorzeichen M8, SignalDelay, Kalibrierung) | 30 bis 40 min | **Soll, Rang 1 (hoch)** | nein (in PSV manuell) | **ja** | nein |
| C2 | M11 an drei Spitzen ohne Kennzeichen | 30 min | Soll, Rang 2 | nein | nein | ja |
| E1 | Platte und Impedanzkopf wiegen | 15 min | Soll, Rang 3 | nein | nein | nein |
| C3 | Golden File v2 (zuerst H1 Ref2/Ref1) | 20 min | Soll, Rang 4 | nein | nein | ja |
| D3 | Zwei-Amplituden-Test A-B-A (0,02 / 0,04 / 0,02 V) | 30 min | Soll, Rang 5 | nein | **ja** | nein |
| E2 | Handbücher 10.4 kopieren | 10 min | Soll, Rang 6 | nein | nein | nein |
| D1 | Mini-Scan 3×3 mit Zeitdaten (+ Referenzscan) | 45 bis 50 min + Scandauer (ca. 3 min je 3×3) | Soll, Rang 7 | nein (in PSV manuell) | **ja** | nein |
| C4 | Generator-Dialog **nur ablesen** (Signalform, Burstlänge; Voraussetzung der Leckage-Deutung in D1) | 10 min | **Soll**, Rang 8 | nein | nein | ja (oder PSV-Generatordialog) |
| X1 | Desktop-Modus bewusst testen, Fehlerbild | 15 min | Soll, Rang 9 (bei COM-Fehler vorziehen) | teilweise (Verbinden wird getestet) | nein | nein |
| B5 | `PolyMath.PeakFit` per COM mit Testdaten | 20 min | Kann | PolyMath-Typbibliothek registriert (Stufe 0, 150024); ProgID ungeprüft; PSV-Registrierung nicht nötig **[Annahme]** | nein | Testdaten |
| C1 | Kopien der Beispieldatei anlegen | 5 min | Muss für Zweig C | nein | nein | ja |
| C5 | Beobachtung `einstellungen_lesen.py` (fälschlich „übersprungen“?) | 0 min extra (läuft mit C3/C4) | Kann | nein | nein | ja |
| C6 | UFF-Export als Gegenprobe; ATFX/ME'scope wählbar? | 15 min | Kann | nein | nein | ja |
| C7 | File Access bei in PSV geöffneter Datei | 10 min | Kann | nein | nein | ja (Kopie) |
| C8 | Restpunkte M13, M14, M15 | 20 min | Kann | nein | nein | ja |
| D4 | Wiederholungsmessung T8 (nur mit Freigabe, Frage an Daniel) | 45 min + **Scandauer ca. 40 min** (Beispieldatei) | **Kann**, nur nach Entscheidung | nein oder ja | **ja** | nein |
| D5 | T3 bis T7 (Meldungsprobe, echte Messung über Programm, Abbruch, Warteschlange) | 10 bis 45 min je Schritt | Kann, nur nach Entscheidung | ja | **ja** (T4 ff.) | nein |

Die Rangfolge der Soll-Punkte (D2 > C2 > E1 > C3 > D3 > E2 > D1 > C4 > X1) stammt aus der Fachprüfung FD-P3. **D2 und E2 werden nie zusammen gestrichen**: D2 ist der wichtigste offene Befund (M8) und wird vor E2 geschützt.

### Streichreihenfolge bei Zeitmangel (zuerst gestrichen wird oben) [Vorschlag, bitte bestätigen]

Nie gestrichen: A0, A1 (mindestens I1 bis I4), B1 bei funktionierender COM, A2.

1. **Kann:** D5 ab T5, D4, C7, C6, B5, C8 (M14, M15 zuerst, M13 zuletzt), C5
2. **Soll (niedrig):** X1 (bei COM-Fehler stattdessen vorziehen), C4 (zusammen mit D1; ohne C4 hat D1 keine Leckage-Aussage), D1
3. **Soll (mittel):** E2, D3, C3
4. **Soll (hoch):** E1, C2, **D2 zuletzt**
5. **Muss (zuletzt):** B4 T2 und B3 Test-.set, danach B2

### 4.2 Fall: Termin doch nur ca. 150 min

Entscheidung beim Termin (K8) nach A0, spätestens nach B1. Verkürzte Reihenfolge nach der Fachprüfung (Vorschlag, bitte bestätigen):
1. **A1 kürzen** auf I1 bis I4 und Skripte kopieren (ca. 10 min). Das Wheel-Update (0.2.0) bleibt **Pflicht vor T0** (ca. 5 min; Nutzerentscheidung 2026-11-03: Der COM-Adapter hat sich mit K-2D geändert, die neuen Hinweise werden am Gerät mitgetestet). **B2** nur so weit, wie T1/T2 die Konfigurationsdatei brauchen.
2. **Bei freigegebener Anregung (F2 ja): D2 vor B3/T2** (und D3 A-B-A am Kopfpunkt gleich dahinter). B3 und T2 (60 min) sind nur Einstellungstests; D2 ist nur dort möglich. Reihenfolge: **A0, B1, T1, D2 (+ D3), dann B3/T2 nach Zeit, E1, E2, A2.**
3. **D4 und D5 entfallen** (Folgetermin).
4. Weitere Soll-Punkte nach der Rangfolge oben, soweit Zeit bleibt. **Sichtbarkeitsprüfung von D2 höchstens 10 min**, sonst Ersatzpunkt.
Ohne Freigabe der Anregung (F2 nein): normaler Muss-Block, danach C2, E1, C3, E2 (alle ohne Anregung).

## 5 Abschnitte (Weiter / Abbruch / Ersatz)

### A0 Schritt 0: Ist die COM-Registrierung erfolgt? (Muss, 15 min)

**Zweck:** Vor allem anderen klären, ob COM überhaupt möglich ist, und eine saubere PSV-Ausgangslage herstellen.
**Voraussetzung:** keine. PSV darf zu sein (Stufe 0 braucht PSV nicht).

1. Aufbau-Foto, Uhrzeit, Kopf des Protokolls ausfüllen (F1 bis F8 notieren).
2. **Prozesse zählen und PID notieren** (nur eine Instanz):
   ```powershell
   Get-Process PSV -ErrorAction SilentlyContinue | Select-Object Id, ProcessName, StartTime, Path
   ```
   Mehr als eine Instanz: K1, nicht „einfach schließen“, erst Zustand prüfen (EP-5).
3. **Erkundung Stufe 0 als Erstes** (ohne `--stufe 1`):
   ```powershell
   & $PY "$ARB\erkundung.py" --stufe 0 --out "$T\erkundung"
   ```
   `zusammenfassung.md` und `registry.reg.txt` öffnen: Abschnitt `P1-2-registry` (`PSV.AcquisitionInstance`, `PresentationInstance`, `Application`; `LocalServer32`),
   `psv_prozesse`, `P1-4-pywin32`. Zusätzlich nur lesend:
   ```powershell
   Get-ChildItem Registry::HKEY_CLASSES_ROOT | Where-Object { $_.PSChildName -like 'PSV*' } | Select-Object PSChildName
   ```
4. **Weiter (K2 ja):** `PSV.AcquisitionInstance` vorhanden und `LocalServer32` zeigt auf `C:\Program Files\Polytec\PSV 10.4\PSV.exe`. Dann PSV über die Verknüpfung
   **„PSV 10.4 Deutsch“** starten (= `PSV.exe /Acquisition /german`), nicht „Desktop“. Danach erneut `Get-Process PSV`: **eine** Instanz, PID und StartTime ins Protokoll.
   Modus der Instanz belegen (Windows-PowerShell, **[Wissen]**, am Gerät ungeprüft):
   ```powershell
   Get-CimInstance Win32_Process -Filter "Name='PSV.exe'" | Select-Object ProcessId, CommandLine
   ```
   Erwartet `/Acquisition` in der Kommandozeile. Keine Dialoge offen, keine Messung.
5. **Abbruch:** `LocalServer32` zeigt auf 10.2 oder 10.3: Befund sichern, nichts ändern, Daniel fragen. Mehr als eine PSV-Instanz mit unklarem Zustand: EP-5.
6. **Ersatz (nicht registriert):** K3 (Registrierung nach [com_registrierung_psv104.md](../2026-11-02_prototyp/com_registrierung_psv104.md), **nur mit Zustimmung von Daniel**, Adminrechte, Fragen A1/A2 vorher klären):
   `cd /d "C:\Program Files\Polytec\PSV 10.4"` und `PSV.exe /regserver` in einer Eingabeaufforderung „Als Administrator“. Danach Stufe 0 erneut, Ergebnis ins Protokoll.
   Geht das nicht oder ist niemand befugt: **Pfad B (EP-1)**, A1 (Installation) und Zweig C/E laufen weiter. Währenddessen A1 parallel erledigen.
**Ablage:** `$T\erkundung\erkundung_BEOWOLF_<Zeit>\` (Durchsicht vor Upload: Pfade/Kontonamen, siehe Erkundung-README).

### A1 Installation bzw. Update der Software (Muss, 20 min; gekürzt 10 min)

**Zweck:** Den aktuellen Stand der Software (Wheel und Skripte) in die vorhandene PyCharm-venv bringen. Ausgangslage: venv unter
`D:\Messdaten\DAL\BA Jakob Busch\PyCharmProject\.venv`, Python 3.11.9, pywin32 312 und die gepinnten Pakete aus dem Internet; Wheel 530af41 installiert
(Laborbuch 2026-11-02). **Voraussetzung:** keine; PSV darf laufen. **Nicht** PySide6 6.12.0 installieren (ADR-001); deshalb beim Wheel immer `--no-deps`.

**Update vor T0 Pflicht** (Nutzerentscheidung 2026-11-03): Seit 530af41 hat sich der COM-Adapter geändert (K-2D: Hinweise bei fehlender Registrierung bzw. Desktop-Modus, SignalDelay lesen). Die frühere Annahme, für T0 bis T2 genüge der alte Stand, gilt nicht mehr; A1 wird auch in der gekürzten Reihenfolge nicht ausgelassen.
Das Update bringt die Frequenzachsen-Korrektur der Auswertung (K-ACHSE) und die überarbeiteten Skripte. Ist das Update nicht erreichbar, entfällt nur die Auswertung, nicht der Termin (EP-3).

**Weg G (Git, bevorzugt, Internet nötig; F7):**
1. Wheel aus dem Repository holen. Neues Wheel **0.2.0** (`ldv_automation-0.2.0-py3-none-any.whl`; Ablageort im Repository **[offen]**, bisher liegt unter `in_progress/versuche/2026-11-02_prototyp/stick/wheelhouse/` nur der Build 530af41 als 0.1.0; der neue Build liegt noch nicht vor, siehe 3.2). Download im Browser über die GitHub-Seite des Repositorys
   (`https://github.com/BuschyBuschmann/BA_Jakob-Busch_P`, Arbeitsbranch `claude/wizardly-carson-mii3uf` bzw. der dann aktuelle Branch) → Datei → „Download raw file“.
   Ob das Repository ohne Anmeldung erreichbar ist, ist **[offen]**; am gemeinsam genutzten Messrechner nicht mit dem persönlichen GitHub-Konto anmelden **[Vorschlag]**. Dann Weg S.
2. SHA-256 prüfen und mit dem vorab notierten Wert (3.2) vergleichen:
   ```powershell
   Get-FileHash "<Download-Ordner>\ldv_automation-0.2.0-py3-none-any.whl" -Algorithm SHA256
   ```
3. Installieren (neue Version 0.2.0 gegen den Bestand 0.1.0: normales `--upgrade` genügt; `--no-deps`, damit keine Abhängigkeit unbeabsichtigt aktualisiert wird):
   ```powershell
   & $PY -m pip install --upgrade --no-deps "<Download-Ordner>\ldv_automation-0.2.0-py3-none-any.whl"
   ```
   **Vorher, neu mit diesem Build:** Die neuen Laufzeitpakete müssen vor dem Wheel in der venv sein: matplotlib 3.11.2 mit Abhängigkeiten, olefile 0.47, tzdata 2026.6 (Pins und Befehle in `installation_0.2.0.md`, Abschnitte 1 und 3; Weg S aus dem Wheelhouse, Ablage **[folgt]**). Ohne sie ist die Auswertung nicht lauffähig.
   **Rückfall** nur, falls pip trotzdem „already satisfied“ meldet oder I6 den alten Hash zeigt (z. B. falsche Datei, Cache; war 6d84318 installiert, ist er nötig): `--upgrade --force-reinstall --no-deps` mit demselben Pfad. In I3 muss `ldv-automation 0.2.0` stehen, dazu die neuen Pakete aus dem Vorher-Schritt.
4. Skripte aus Git holen (sind **nicht** im Wheel): `software/tools/erkundung/erkundung.py`, `einstellungen_lesen.py`, `daten_lesen.py` und `software/konfig/beispiel_messrechner.json`
   nach `$ARB` (die alten Fassungen vom letzten Termin vorher als `*_alt.py` beiseite legen, nicht überschreiben). `skript_sha256` des neuen `erkundung.py` im Protokoll festhalten.

**Weg S (Stick):** dieselben Dateien vom Stick; Installationsbefehl wie in Schritt 3 mit dem Pfad vom Stick. **Ohne Internet (`pip` aus dem Wheelhouse):** nur nötig, falls sich die Pins geändert haben:
`& $PY -m pip install --no-index --find-links "<Stick>\wheelhouse" --no-deps ...`.

**Prüfschritte (wie I1 bis I7 im [alten Plan](../2026-11-02_prototyp/installation_messrechner.md), mit `$PY`):**

```powershell
& $PY --version                                                     # I1  Python 3.11.9
& $PY -c "import struct; print(struct.calcsize('P')*8)"             # I2  64
& $PY -m pip list                                                   # I3  ldv-automation 0.2.0, matplotlib 3.11.2, olefile 0.47, tzdata 2026.6, PySide6_Essentials 6.11.3, shiboken6 6.11.3, pywin32 312; kein PySide6 6.12.0
& $PY -c "import win32com.client; print('win32com ok')"             # I4
mkdir "$T\daten\selbsttest" -ErrorAction SilentlyContinue
& $PY -m ldv_automation selbsttest --ordner "$T\daten\selbsttest"   # I5  „Selbsttest bestanden“
& $PY -c "import json,importlib.resources as r; print(json.loads(r.files('ldv_automation').joinpath('_build_info.json').read_text('utf-8')))"   # I6  git_hash, git_dirty
& $PY -m ldv_automation gui --simulator                             # I7  Titel „… SIMULATOR“, Symbole sichtbar
```

**Ergänzung (Reiter „Auswerten“):** Der neue Build 0.2.0 enthält den Reiter „Auswerten“ und braucht neue Laufzeitpakete (Schritt 3, I3). Dafür gilt zusätzlich `installation_0.2.0.md` (Pins, Wheelhouse, Prüfschritte N1 bis N7), danach die Checkliste `pruefanleitung_auswerten.md`. Wheel-Name, Ablageort und SHA-256 **[folgt]**.

**Weiter:** I1 bis I4 ok **und** I6 zeigt den erwarteten Git-Hash mit `git_dirty: False`. **Abbruch:** I1 bis I4 schlagen fehl: Meldung wörtlich sichern, nichts weiter installieren.
**Ersatz:** EP-3. **Ablage:** Protokoll Abschnitt 4 (Hash, SHA-256, `pip list`).

### B1 Erkundung Stufe 1 und 1b (Muss bei COM, 15 + 10 min)

**Zweck:** Verbinden mit PSV per COM, Version, Modus, Zustand, Validator, Konstanten; 1b: Datei-Struktur. **Voraussetzung:** K2/K3 erfolgreich, **eine** Instanz mit `/Acquisition`, keine Dialoge, keine Messung.
Sicherheit: Shaker/Verstärker vom Netz bzw. Signalkabel getrennt (Aufbau ist anders als beim ersten Termin: Shaker hängt am Blech) **[Vorschlag]**.

```powershell
& $PY "$ARB\erkundung.py" --stufe 1 --out "$T\erkundung"
# optional 1b mit Kopie (nicht in PSV geöffnet; mehr Namen bei Bedarf, siehe C3):
& $PY "$ARB\erkundung.py" --stufe 1 --datei "$T\daten\<kopie>.svd" --out "$T\erkundung"
```

Exit-Codes: 0 normal, 1 verweigert, 2 Aufruffehler/Python zu alt, 3 blockiert, 4 interner Fehler, 130 Strg+C.
Zusätzlich manuell: *Hilfe > PSV Info* (Foto), ob ein Fenster in PSV aufpoppte.
**Weiter (Pfad A):** `P1-5-verbinden` ok, `Mode` = Acquisition, `State` gelesen, Validator-Befund, Konstanten wie [I5 §8](../../analysen/2026-10-23_I5_com-referenz.md).
**Abbruch (Strg+C, Ordner trotzdem sichern):** unerwarteter Dialog/Fehler in PSV, „blockiert bei …“, Laser/Spiegel schaltet, „verweigert (Default deny)“.
**Ersatz:** Verbinden scheitert: Fehlerbild sichern (Exit-Code, `P1-5-verbinden.exception` mit `hresult_hex`, `excepinfo`, Dauer, Fenster in PSV?), Modus der Instanz prüfen (A0 Schritt 4), dann **X1** als Gegenprobe, dann **Pfad B (EP-1)**.
Konstanten weichen von I5 §8 ab oder der Prozessname enthält nicht „psv“: **nichts weiter am Gerät** (B4 entfällt), Befund melden.

### X1 Desktop-Modus bewusst testen (Soll, 15 min)

**Zweck:** Das Fehlerbild von `GetApplication`/Verbinden im Desktop-Modus kennen, damit künftig Fehlerbilder „nicht registriert“ und „falscher Modus“ unterscheidbar sind (Thesis-Baustein: Bewertung der Schnittstelle).
Erwartung **[Annahme, laut Basic Engine Manual: `AcquisitionInstance` in Desktop-Versionen nicht verfügbar]**: Verbinden scheitert. Das ist hier ein Versuch, kein Fehler.
**Voraussetzung:** keine Messung, keine Dialoge; **nur lesen**.

**Wann:** Bei funktionierender COM **erst am Ende der Acquisition-Arbeiten** (B1 bis B4, D), weil dafür PSV beendet und im anderen Modus neu gestartet wird.
Bei COM-Fehler in K5 **früh** (Diagnose-Gegenprobe). Kann mit C1 bis C8 kombiniert werden, wenn die Auswertung (Analysator) dafür ohnehin in der Desktop-Version läuft **[offen: in welchem Modus die Auswertung am 02.11. lief]**.

1. PSV regulär beenden (Speichern: Nein), `Get-Process PSV` leer.
2. Über **„PSV 10.4 Desktop Deutsch“** starten (= `PSV.exe /Desktop /german`). Fenstertitel „PSV Auswertung“ erwartet **[aus der Faktenliste A3]**. PID notieren, CommandLine prüfen (`/Desktop`).
3. Erkundung Stufe 1 (nur lesend) wie in B1, Ausgabe in `$T\erkundung`. Notieren: Exit-Code, `P1-5-verbinden`-Status und Meldung, `hresult_hex`, `excepinfo`, Dauer, Fenster in PSV aufgepoppt (ja/nein, Foto).
4. PSV beenden, über **„PSV 10.4 Deutsch“** neu starten, Stufe 1 **erneut** (Gegenprobe: gleicher Rechner, anderer Modus). Beide Fehlerbilder gegenüberstellen.
**Weiter:** Fehlerbild notiert (auch wenn Verbinden im Desktop-Modus wider Erwarten gelingt: dann genau das notieren, nichts weiter tun).
**Abbruch:** Dialog oder PSV reagiert nicht (Strg+C, EP-5).
**Ersatz:** Neustart über die Acquisition-Verknüpfung klappt nicht: Daniel, EP-5. **Ablage:** Protokoll Abschnitt 6, Erkundungsordner.

### B2 Ergebnisse sichern, Schalter, Konfigurationsdatei (Muss bei COM, 20 min)

Wie [alter Plan, Abschnitt 4](../2026-11-02_prototyp/ablaufplan_vor_ort.md): Erkundungsordner sichern und **Durchsicht vor Upload** (`kommandozeile`, `parameter.datei`, `dateien.*.pfad`, `Acquisition.ScanFileName`, Netzlaufwerkspfade, Fehlermeldungen),
Schalterwerte nach [U3, „Schalter aus der Erkundung übernehmen“](../2026-11-02_prototyp/pruefanleitung_U3_com-adapter.md) bestimmen, **Kopie** von `beispiel_messrechner.json` nach `$T\konfig_termin.json`, Werte eintragen
(`validator_rueckfall_direkt`, `lademaske`, `aufruf_grenze_s`, `aufruf_warnung_s`, `stop_frist_s`, `standard_zeitlimit_s`; Vorgaben false / Acquisition-Alignment-APS-2DAlignment-3DAlignment / 60 / 5 / 10 / 600), **Pfad und SHA-256 der Kopie** ins Protokoll:
`Get-FileHash "$T\konfig_termin.json"`. Kein Eingriff in installierten Code. Ungültige Konfiguration: Start bricht mit Rückgabewert 2 ab, Meldung notieren, korrigieren.
**Weiter:** Schalter bestimmt. **Abbruch:** Konstanten abweichend, Prozessname ohne „psv“ oder Fehltreffer: **stoppen**. **Ersatz:** ohne Konfigurationsdatei mit den Vorgaben zu arbeiten ist nicht vorgesehen; dann entfällt B4, weiter mit Pfad B.

### B3 Test-.set anlegen (Muss für T2, 30 min)

Nach [anleitung_test_set.md](../2026-11-02_prototyp/anleitung_test_set.md): FFT-Modus, wenige Punkte (z. B. 3×3), **Generator aus**, Bandbreite ≠ 5600 Hz (z. B. 5000 Hz), Mittelung 3, speichern als `D:\...\vorlagen\test_3x3.set`
(Ordner lokal, nicht in Polytec-Ordnern, Standard-Einstellungsdateien nicht überschreiben), **Kopie** anlegen, Rückprobe (Laden zeigt dieselben Werte), alles ins Protokoll Abschnitt 8.
Die Menübezeichnungen sind im Repository nicht belegt: „in PSV die Funktion … verwenden; genaue Bezeichnung vor Ort“ und die gefundenen Pfade ins Protokoll schreiben.
**Option [Idee, nicht freigegeben]:** eine zweite Kopie als Mini-Scan-Vorlage (Generator an, Zeitdaten an; D1) nur mit Freigabe der Anregung; die Test-.set für T2/T4 bleibt mit Generator aus (Regel S5).
**Weiter:** Rückprobe ok. **Abbruch:** PSV fragt unerwartet, Dialog offen: EP-5. **Ersatz:** Keine Punkte definierbar/Abgleich fehlt: Datei ohne Scanpunkte speichern, T2 nur mit Parameter-Lesen und Laden prüfen, im Protokoll vermerken; ohne COM trotzdem anlegen (für später).

### B4 Prototyp-Prüfung T0 bis T2 (Muss bei COM)

**T0:** Installation/Simulator (I5, I7, Handtest F4 Symbole) bereits in A1.
**T1 `NUR_LESEN` (20 min):** nach [U3, T1](../2026-11-02_prototyp/pruefanleitung_U3_com-adapter.md) (Python-Konsole mit `& $PY`) oder über die Oberfläche:
```powershell
& $PY -m ldv_automation gui --psv --betriebsart nur_lesen --messdaten "$ARB\daten" --konfig "$T\konfig_termin.json"
```
Prüfen: 1-0 (nur PSV im Prozesstreffer) bis 1-6 und U5-Ergänzung (Dialog „Gerät …“: Zugriffe ohne Verweigerung, Messpunkte, Generator, `psv_prozesse`, Lademaske). Messdaten-Wurzel `"$ARB\daten"` **[Annahme, C1 offen]**; nicht im Repository.
**Weiter zu T2:** keine Verweigerung, alles wie Erkundung und PSV-Anzeige. **Abbruch:** Abweichung/Verweigerung, unerwarteter Dialog, Laser/Spiegel bewegt: Protokoll sichern, keine weiteren Tests am Gerät.
**T2 `TROCKENLAUF` (30 min):** ändert die aktuellen PSV-Einstellungen (bewegt nichts; Hinweisdialog). Zuerst Konfigdatei prüfen, mit `--konfig` starten:
```powershell
& $PY -m ldv_automation gui --psv --betriebsart trockenlauf --messdaten "$ARB\daten" --konfig "$T\konfig_termin.json"
```
Prüfen 2-1 bis 2-7 (U3), insbesondere **Einrasten bei 5600 Hz** (Wert notieren) und Übereinstimmung mit der PSV-Anzeige. Danach den PSV-Zustand wieder auf den gewünschten Stand bringen (Einstellungen wurden verändert), Foto.
**Ersatz:** T1/T2 scheitern wegen COM: nur Simulator-Vorführung (EP-1); Hardwaretest **nicht** als bestanden melden.

**Entscheidung echte Messung (T4 ff.):** Erst danach, nur wenn **du** es entscheidest, T1 und T2 ohne Befund, Freigabe der Anregung (K6) vorliegt (falls der Aufbau mit Shaker gemessen wird); Zeit, Entscheidung, Grund ins Protokoll. T4 wie im alten Plan (Trockenlauf mit derselben .set in derselben Sitzung ohne PSV-Neustart, Startdialog prüfen, `MESSEN` eintippen). D5 enthält die Reihenfolge T4 vor T5 vor T6.

### B5 `PolyMath.PeakFit` per COM probieren (Kann, 20 min)

**Zweck:** Prüfen, ob der Peak-Fit der Polytec-Bibliothek (`PolyMathLib`, Objekt `PeakFit`: Anpassung der Frequenzgangfunktion eines Einmassenschwingers an ein reales oder komplexes Spektrum, Methoden `Fit`, `FitXY`, `GetFunction`, `GetPeak`, `GetWidth`) die PSV-Peak-Anpassung mit voller Stellenzahl reproduziert. Das ist zugleich ein Weg zu den vollen Stellen für C2.
**Voraussetzung:** PolyMath-Typbibliothek registriert (Stufe 0, 150024); ProgID und Signatur am Gerät **[offen]**; PSV-Registrierung vermutlich nicht nötig **[Annahme]**. Kein PSV-Zugriff, keine Messung, nur Rechnung mit Testdaten.
**Testdaten (Sollwerte rechnerisch von der Fachprüfung hergeleitet [N], nicht im Skript geprüft):**

| Fall | Testsignal | Band | Sollwerte |
|---|---|---|---|
| 1 | Mobilität eines Einmassenschwingers, f_n = 700 Hz, ζ = 0,01 (B = 14 Hz, Q = 50, B/Δf = 22), m = 1 kg, Raster Δf = 0,625 Hz bis 1000 Hz, ohne Rauschen | 665 bis 735 Hz | f = 700,0 Hz (±0,01 Hz), ζ = 0,0100 (±1 %) |
| 2 | f_n = 670 Hz, ζ = 1,4·10⁻³ (B/Δf = 3,0), sonst wie Fall 1 | zwei Bänder (z. B. ±2 B, ±4 B) | Bias des −3-dB-Schätzers +2,6 % bis +5,2 % (FG-02 3.9); ein Modellfit sollte nahe exakt liefern |

Offen: ob `PeakFit` auf |H| oder komplex fittet **[offen]**, Fitfenster und Gewichtung (nicht dokumentiert). Danach dieselben Bandgrenzen wie in C2 an realen Daten und Vergleich mit der PSV-Anzeige.
**Weiter:** Fälle 1 und 2 laufen. **Abbruch:** Objekt nicht anlegbar oder Dialog in PSV: sichern, B5 streichen. **Ersatz:** nur die ProgID-/Typbibliotheksauflistung (`typelibs.txt`) ins Protokoll und Folgetermin. **Ablage:** Protokoll 10.5.

### Zweig C: File Access auf Kopien (ohne COM, ohne Anregung)

Voraussetzung: **C1** zuerst.

**C1 Kopien anlegen (5 min).** Von `20261012_ref_Mitte.svd` (Original nie öffnen) **zwei** Kopien: eine für PSV (Anzeige), eine für File-Access-Skripte (nie in PSV geöffnet gleichzeitig), wie am 02.11. (`…_KOPIE.svd`, `…_KOPIE_KOPIE2.svd`). Größe 27 115 520 Byte (Vergleich mit dem Original). Wo das Original liegt, ist **[offen]**; nur lesend kopieren.
**Ersatz:** Original nicht auffindbar: andere vorhandene Messdatei als Kopie nehmen, Datei im Protokoll nennen; Bezug Label 132 gilt dann nicht (C2, D3 anpassen).

**C2 M11 an drei Spitzen ohne Kennzeichen wiederholen (Soll, Rang 2, 30 min).**
*Zweck:* Die Toleranzzeilen für Spitzen ohne Warnkennzeichen (FG-02 Abschnitt 8) sind bisher **nicht geprüft**; beide Spitzen vom 02.11. waren `aufloesungsbegrenzt`.
*Kandidaten* (FG-02 Abschnitt 8, Punktmittel |H1| Vib Z/Ref1 ohne Kennzeichen, **korrigierte Achse, Hz**): 617,9; 631,7; 644,8; 693,5; 757,3; 867,9.
*Kandidaten vorab am Punkt prüfen:* Die Kennzeichenfreiheit gilt in FG-02 §8 am **Punktmittel**, nicht am Einzelpunkt (3.2). Grobe Vorabrechnung der Fachprüfung **[N]** mit ζ ≈ 1,4·10⁻³ (aus nur zwei Spitzen) und B = 2ζf: 1,73 Hz (617,9), 1,77 (631,7), 1,81 (644,8), 1,94 (693,5), 2,12 (757,3), 2,43 Hz (867,9) gegen 3Δf = 1,875 Hz. Erst ab ca. 670 Hz ist B ≥ 3Δf: **693,5 / 757,3 / 867,9 Hz sind am aussichtsreichsten**, die ersten drei sind am Einzelpunkt wahrscheinlich wieder `aufloesungsbegrenzt`. Auswahl der drei Spitzen erst nach der Vorabprüfung in Stufe 1 am gewählten Punkt.

*Vorabprüfung V2 (Fachanalyse, 2026-11-02, korrigierter Leser, Label 132, H1 Vib Z/Ref1; Skripte im Scratchpad, Werte [N]):* Von den Punktmittel-Kandidaten ist an Label 132 nur 644,8 Hz kennzeichenfrei (631,7 → Spitze 632,5 Hz); 693,5 und 757,3 tragen `nachbarmode`, 867,9 `ueberlappend`, 617,9 hat keine Spitze. **Gewählt (Reihenfolge):**

| Rang | Spitze (Stufe 1) | B; B/Δf | Band ±2B (Hz) | Band ±4B (Hz) | eigener B-1 ±2B: f_r / ζ / ρ | B-1 ±4B: f_r / ζ |
|---|---|---|---|---|---|---|
| 1 | 921,546 Hz | 2,894 Hz; 4,63 | 915,625 – 927,500 (20 Linien) | 910,000 – 933,125 (38) | 921,6578 / 1,6556e-3 / 0,056 | 921,5496 / 1,8651e-3 (`modell_passt_nicht`) |
| 2 | 632,514 Hz | 2,576 Hz; 4,12 | 627,500 – 637,500 (17) | 622,500 – 643,125 (34) | 632,4926 / 1,6884e-3 / 0,066 | 632,4912 / 1,6613e-3 (`modell_passt_nicht`) |
| 3 | 483,827 Hz | 1,917 Hz; 3,07 | 480,000 – 487,500 (13) | 476,250 – 491,250 (25) | 483,7730 / 1,9528e-3 / 0,054 | 483,7887 / 1,8712e-3 (`modell_passt_nicht`) |
| Reserve | 949,301 Hz | 6,102 Hz; 9,76 | 936,875 – 961,250 | 925,000 – 973,750 | 949,1154 / 2,5995e-3 / 0,082 | – |
| Reserve | 644,824 Hz | 2,870 Hz; 4,59 | 639,375 – 650,625 | (unbrauchbar) | 645,0121 / 1,9801e-3 / 0,145 | – |

Spitze am Gerät über die Frequenz prüfen (632,5 Hz liegt 1,2 Δf neben dem Punktmittelwert 631,7 Hz). Rückfallpunkte, falls Label 132 ungeeignet: Label 338 (u. a. 921,0 Hz, ρ 0,035), Label 298. Im ±4B-Band ist der Ein-Moden-Fit für keine Spitze sauber (ρ > 0,10) – Aussage über die Modellgüte, nicht über PSV.

*Klickpfad (vom 02.11. bekannt):* Datei (Kopie) in PSV öffnen → Ansichten-Menü (Symbol links in der zweiten Symbolleiste) → **Alt+2** Einzelner Scanpunkt (Alt+1 Messobjekt, Alt+3 Gemitteltes Spektrum, Alt+4 Profil, Alt+5 Banddaten, Alt+6 Punktdaten) → Punkt Label 132 anklicken →
Analysator-Menü: Domäne FFT, Kanal **Vib 3D & Ref1**, Komponente Z, Signal H1 Geschwindigkeit/Kraft → Analysator → **Band-Cursor** → Cursor-Eigenschaften → **Peak-Anpassung** (f max, −3 dB, Q-Faktor, Zeta). **Strg+K** = Autoskalieren, Zoomen/Verschieben im Analysator-Menü.
*Bandregel (ersetzt die Regel „Breite ≥ 3 Δf“ des ersten Entwurfs, die fachlich falsch war):* Bandgrenzen als Vielfache von Δf = 0,625 Hz; Band mit **mindestens 7 Linien** (FG-03: ≥ 4n+3 bei n = 1, sonst für B-1 nicht rechenbar) und mehrere B breit. **Zwei Bänder je Spitze** (z. B. ±2 B und ±4 B), weil das PSV-ζ bandabhängig ist (−6 % bei engerem Band). `aufloesungsbegrenzt` hängt an der −3-dB-Breite B der **Spitze** (FG-02 3.9), nicht am Cursorband.
*Notieren je Spitze und Band:* Cursorgrenzen (Hz), f max, −3 dB, **Q und ζ**, Screenshot. **Q und ζ zeigt PSV mit mehr Stellen als f max und −3 dB** (siehe M11-Tabelle); ζ = 1/(2Q) deshalb mit **voller angezeigter Stellenzahl** ablesen. f max nur mit 0,1 Hz (= ±0,08 Δf): als Grenze vermerken und, wenn möglich, mit B5 oder C6 gegenprüfen.
*Rechnung danach:* B-1 an demselben Punkt mit **denselben** Bandgrenzen (nicht am Rechner, später).
**Weiter:** drei Spitzen mit je zwei Bändern notiert. **Abbruch:** PSV fragt beim Schließen nach Speichern (immer „Nein“), Dialog/Fehler: sichern. **Ersatz:** Auswertungsansicht nicht auffindbar (kostete letztes Mal viel Zeit): Pfad oben verwenden, **15 min** Höchstdauer, dann nur eine Spitze mit einem Band; Screenshot der Ansicht.

**C3 Golden File v2 (Soll, Rang 4, 20 min).** *Zweck:* weitere Referenzsignale von PSV für den eigenen Leser: H2, Kohärenz, PSD/ESD, H1 Ref2/Ref1, Terzen.
*Zuerst H1 Ref2/Ref1:* Dieses Signal prüft ohne Laser den Ref1/Ref2-Vorzeichenbefund (Phase 0°/180°) und die Massenlinie (Betrag m = |F/a| bei 1 bis 6 Hz; offline zu rechnen) und gehört zu M8/E1. Der Name ist per File Access laut Faktenliste C6 **nicht lesbar**: dann im Analysator Kanal „Ref2 & Ref1“ ablesen bzw. exportieren (ASCII/UFF), nicht erst nach den anderen Signalen.
*Skalierungsangaben festhalten* (Protokoll 10.3): einseitig/zweiseitig, RMS oder Spitze bei PSD/ESD, Fensterkorrektur, Terzbasis (Basis 10 oder 2), Mittenfrequenzen, Mittelungsart.
*Schritt 1, Namen klären:* Die Erkundung 1b zeigt nur bis zu 8 Kanäle und 6 Signale je Kanal; die Kohärenz und Terzen-Domäne sind nicht benannt. Ein erneuter Lauf der Erkundung 1b zeigt dieselbe Begrenzung; deshalb **Namen in PSV ablesen** (Kanalwahl: Vib 3D, Ref1, Ref2, Vib 3D & Ref1, Vib 3D & Ref2, Ref2 & Ref1; Domäne Terzen im Analysator) und ins Protokoll schreiben, oder die vorab erweiterte Fassung (3.2) verwenden.
*Schritt 2, lesen:*
```powershell
& $PY "$ARB\daten_lesen.py" "$T\daten\<kopie_fa>.svd" "$T\export\golden_v2_punkt1_label132.csv" [Punktnummer]
```
Exit-Codes: 0 vollständig, 1 nichts gelesen, 2 Aufruffehler/Ziel existiert (kein stilles Überschreiben), 3 unvollständig (Begleitdatei `.fehlend.txt`). Bekannt: `Ref1 | Kraft` hat keine Real/Imag-Darstellung; `Ref2 & Ref1 | H1 Beschleunigung / Kraft` ist über diesen Namen nicht lesbar (Faktenliste C6).
*Weiter:* CSV mit den gewünschten Signalen. **Abbruch:** Ausnahme/Traceback (Exit-Code 1 bedeutet hier Abbruch durch Ausnahme, keine CSV). **Ersatz:** Skript kennt die Namen nicht: Werte in PSV als ASCII exportieren (Format und Optionen notieren; PSV-Menüpfad **[offen]**); mindestens H1 Ref2/Ref1, H2 und Kohärenz für Label 132.

**C4 Generator-Dialog ablesen: Signalform und Burstlänge (Soll, Rang 8, 10 min).** *Zweck:* Die Waveform-Parameter des Generators (Signalform, Burstlänge, Amplitude) sind per dynamischem Dispatch in `einstellungen_lesen.py` nicht lesbar (Faktenliste C3: Cast nötig). Ohne sie ist die Leckage-Auswertung von D1 nicht deutbar (die Spitzen der Beispieldatei klingen nach 1,6 s Blocklänge noch zu 9,9 % bzw. 3,2 % nach; ob das Leckage erzeugt, hängt von Burstform und -länge ab).
*Vorgehen am Termin (Soll):* **nur lesen, nichts ändern:** Generator-Dialog der Beispieldatei bzw. der Messeinstellung in PSV öffnen und Signalform, Burstlänge, Amplitude ablesen und fotografieren; ohne Anregung möglich.
*Optional (Kann):* Der Cast im Skript ist eine Änderung (Paket SKRIPTE); am Termin nur, wenn vorab umgesetzt oder der Orchestrator live in einer Python-Konsole (nur lesend) hilft.

**C5 Beobachtung `einstellungen_lesen.py` (Kann, 0 min extra).** Aus dem Re-Review: beim Lauf achten, ob **Eigenschaften** fälschlich als „übersprungen (aufrufbar, keine Eigenschaft)“ gemeldet werden:
```powershell
& $PY "$ARB\einstellungen_lesen.py" "$T\daten\<kopie_fa>.svd" > "$T\export\einstellungen_<kopie>.txt"
```
Ausgabe durchsehen: Jede Zeile mit „übersprungen“ notieren (Name) und mit der Dokumentation (Basic Engine Manual) oder in PSV vergleichen, ob es eine Eigenschaft ist, deren Wert in PSV sichtbar ist. Nur beobachten, nicht ändern.

**C6 UFF-Export als Gegenprobe (Kann, 15 min).** In PSV an der Kopie: Export als **UFF** für Label 132 (Vib Z & Ref1 H1, Vib X Geschwindigkeit) – Formatwahl und Optionen notieren (Programmordner enthält `PolyUFFExport.dll`, `PolyAtfxExport.dll`, `PolyMEScopeExport.dll` laut Faktenliste A7). Prüfen und notieren, **ob ATFX und ME'scope als Exportformat wählbar sind** (Lizenzlage **[offen]**, beim Betreuer klären). Vergleich der Zahlen später (Toleranz FG-02 Abschnitt 8: rtol 1e-5 bzw. Exportrundung).
**Ersatz:** nur die Auswahlliste der Formate fotografieren.

**C7 File Access bei in PSV geöffneter Datei (Kann, 10 min).** *Zweck:* Verhalten dokumentieren (Fehler? Sperre? alte Daten?). Nur mit einer **Kopie**, die in PSV geöffnet ist, dann `daten_lesen.py` oder `einstellungen_lesen.py` mit ReadOnly (Skript setzt `ReadOnly = True`), Ziel in `$T\export`. Meldung/Ausnahme und Ergebnis notieren. Nichts speichern.
**Abbruch:** PSV zeigt Dialog oder reagiert nicht: Strg+C, EP-5.

**C8 Restpunkte M13 bis M15 (Kann, 20 min).**

| Nr | Was prüfen | Sollwert / Bisher |
|---|---|---|
| M13 | Achsen des **3D-Abgleichs**: Achsenbezeichnung aus dem Abgleich-Dialog ablesen/fotografieren **und die Kopfpositionen im Geometrie-KS notieren**; offline die Normale der Plattenebene aus den Punktkoordinaten anpassen | Sollwert \|n_z\| ≈ 1 (grob gleich dem Indiz η ≈ 0,995 aus M12); bisher plausibel (Z-Achse aus dem Bild zu den Scanköpfen, D = 2,82 m), nicht formal geprüft |
| M14 | **Nur wenn die Datei Elemente enthält:** ein Element ansehen, **Eckpunkt-Labels gegen Indizes** (0-basiert?) | sonst „nicht prüfbar mit dieser Datei“ (**[offen]**, ob die Beispieldatei Elemente enthält) |
| M15 | **Messzeit:** Zeitstempel je Punkt gegen die Rechneruhr, am besten mit dem Scan aus D1 (Start- und Endzeit des Scans von Hand aufschreiben); sonst PSV-Info der Beispieldatei | Sollwert: konstanter Offset, Differenzen zwischen Punkten gleich der Uhrzeit auf ±1 s; bisher offen (Feld +0x3C je Punkt = Zahl erfasster Blöcke 7 bis 25 laut P0b) |

**Ersatz:** Elemente fehlen: M14 als „nicht prüfbar mit dieser Datei“ festhalten, ggf. mit der Mini-Scan-Datei (D1) wiederholen. M15 ohne D1: nur an der Beispieldatei beobachten und als unvollständig vermerken.

### Zweig D: Anregung (nur mit Freigabe, jede Messung eigene Entscheidung)

**Vor jeder Messung in D:** Freigabe F2 im Protokoll mit Name/Uhrzeit; Aufbau-Foto; Verstärkerstellung (Regler) notieren; Generator-Amplitude und -Typ ablesen; Zieldatei neuer Name; Ordner außerhalb von Repo. Entscheidung (Zeit, Grund) ins Protokoll. Messungen in D laufen **direkt in PSV** (Pfad B tauglich), nur D5 über das Programm (COM).
**Weiter:** Messung ohne Dialog, Datei vorhanden. **Abbruch:** unerwarteter Dialog, Laser/Spiegel unerwartet, Messung hängt: EP-5. **Ersatz:** keine Freigabe: EP-4.

**D1 Mini-Scan 3×3 mit Zeitdaten (Soll, Rang 7, 45 bis 50 min + Scandauer).**
*Zweck* (Fachprüfung): (a) **Eigene FFT je Block** (Rechteckfenster, Skalierung FG-02 2.1) gegen die PSV-Spektren (CP/AP) mit **rtol 1·10⁻⁵** (FG-02 §8); Abweichungen weisen auf Delay-Kompensation oder andere Vorverarbeitung hin. (b) **n_d bestimmen** (offene M5-Frage): eigene Mittelung über die ersten n Blöcke, n = 1 … N, gegen PSV; das passende n ist n_d. (c) **Streuung je Block** gegen das Modell aus FG-02 3.4 (σ_|H|/|H| ≈ √(1−γ²)/(|γ|√(2n))). (d) **Messzeit-Stempel gegen die Rechneruhr (M15):** Start- und Endzeit des Scans aufschreiben. Dazu Dateigröße und Wirkung auf Signal Enhancement.
*Schritte:* In PSV 3×3-Raster auf dem Blech (Generator an, Amplitude wie in der Beispieldatei 0,02 V **[Annahme; mit Daniel abstimmen]**); die Option **SaveTimeDataForScan** (Name der Eigenschaft in COM; Bezeichnung in der Oberfläche **[offen]**, in den Erfassungseinstellungen suchen; in der Beispieldatei aus, Faktenliste C2) einschalten.
**Hinweis: SaveTimeDataForScan setzt Signal Enhancement (SE) auf „Fast“.** Vorher Einstellung fotografieren, nach dem Test auf den vorherigen Stand zurückstellen und im Protokoll festhalten.
*Referenzscan:* Die „Wirkung auf SE“ lässt sich nur mit Referenz klären: **zusätzlich dieselben 9 Punkte ohne `SaveTimeDataForScan`** (vorherige SE-Einstellung), gleiche sonstige Einstellungen; beide Dateien vergleichen (Dauer, Spektren, Zahl erfasster Blöcke je Punkt).
*Dauer:* ca. 17,8 s je Punkt aus dem Beispielscan (40 min / 135 Punkte, **[Annahme aus altem Plan]**), also ca. 3 min je 3×3-Scan.
*Dateigröße (F4) grob:* 4000 Samples × 4 B = 16 kB je Block und Kanal **[Annahme: float32]**; bei 25 Blöcken und 8 Kanälen ca. 29 MB für 3×3 und ca. 430 MB für 135 Punkte **[N]**.
*Leckage:* Die Spitzen der Beispieldatei haben τ = 1/(ζ·2πf) = 0,69 s (160,6 Hz) bzw. 0,46 s (247,7 Hz); nach 1,6 s Blocklänge sind noch 9,9 % bzw. 3,2 % der Amplitude übrig (ζ aus B-1 in M11, **[N]**). Deutung nur mit Burstform und -länge aus **C4** (daher C4 Soll).
Speichern unter neuem Namen; Dauer, Dateigröße, Zeit pro Punkt notieren. Danach Rückleseprobe mit File Access auf der **Kopie**: sind Zeitdaten lesbar?
*Voraussetzung:* F2 **ja** und F4 **ja**. **Ersatz:** Anregung nicht freigegeben, aber Scan erlaubt (Laser): Scan **ohne Anregung** nur um Dateigröße, Dauer und Lesbarkeit der Zeitdaten zu klären (Aussagen zu H1/Kohärenz entfallen) **[Idee, braucht Freigabe zum Scannen]**.

**D2 Messpunkt auf dem Impedanzkopf (Soll, Rang 1 (hoch), 30 bis 40 min).**
*Zweck:* Mit einer Messung drei Fragen beantworten: (1) **Vorzeichen (M8):** Ist Ref2 gegenüber Vib und Ref1 gedreht? (2) **SignalDelay:** Wie groß ist die verbleibende Laufzeit τ_res zwischen Vib und Ref2 bzw. Ref1? (3) **Kalibrierung und Amplitudengang:** gilt |H1(Vib Z/Ref2)|·ω = 1 s·rad/s, auch bis 1000 Hz (zugleich Rest von M7 „Amplitudengang“)?
*Physik:* Kopf und Laserpunkt bewegen sich unterhalb weniger kHz gemeinsam **[Annahme]**. Dann gilt H = v/a = 1/(iω): Betrag 1/ω, **Phase −90°**; gedrehter Ref2: **+90°**. Am Treibpunkt gilt zusätzlich Re{v/F} ≥ 0 (Phase von Vib Z/Ref1 in [−90°, +90°], an Spitzen ≈ 0°; Passivität, wie FG-02 9.7). Dieses Kriterium gilt am **Treibpunkt**, nicht am Transferpunkt Label 132.
*Reichweite der Aussage:* D2 entscheidet die **relative** Polarität (Ref2 gegen {Vib, Ref1}). Die absolute Richtung und die Ursache klärt das Datenblatt PCB 288D01 (R-0211); für die Software-Korrektur (`vorzeichen_kanal`) genügen die Produkte der Vorzeichen, das Datenblatt ersetzt die Messung nicht **[N, Fachprüfung]**.
*Vorbereitung:*
 (a) F6 geklärt, Foto.
 (b) **Sichtbarkeit prüfen, bevor Zeit investiert wird (höchstens 10 min):** Sehen alle drei Scanköpfe eine zur Kraftachse senkrechte Fläche des Kopfes (Stirnfläche, nicht Mantel)? Der Beschleunigungssensor sitzt strukturseitig **[Wissen, am Gerät nicht geprüft]**; Messpunkt möglichst nahe an der Montagefläche.
 (c) **Reflexfolie** (flach, einige mm², Masse vernachlässigbar **[Annahme]**) auf die Stirnfläche, **nur mit Zustimmung von Daniel (F6)**. Spray streut diffus und kann Speckle/Dropouts erzeugen; auf Mantelflächen funktioniert Folie nicht (streifender Einfall). Folie oder Spray, Fläche und Punktstatus („Optimal“/„Gültig“) ins Protokoll.
 (d) **Winkel θ** zwischen Kraftachse und Laser-Z abschätzen (Foto). Amplitudenfehler cos θ: 5° 0,996, 10° 0,985, 15° 0,966, das Vorzeichen bleibt unbeeinflusst **[N]**. **Vib X und Vib Y mit aufzeichnen** (Querbewegung/Kippen); bei großem θ die Projektion aus X/Y/Z nachrechnen.
 (e) **Gleiche Einstellungen wie bei der Beispieldatei:** Bandbreite 1000 Hz, f_s 2500 Hz, 4000 Samples (Δf = 0,625 Hz), Rechteckfenster, komplexe Mittelung, n_d ≥ 7, gleicher Decoder-Bereich, gleiche SE-Einstellung (ob SE die SignalDelay ändert, ist **[offen]**; SignalDelay-Werte für Vib, Ref1 und **Ref2** vor und nach über `einstellungen_lesen.py` bzw. Foto notieren; der Ref2-SignalDelay ist in der Faktenliste nicht genannt und wird vor Ort abgelesen). Generator wie in der Beispieldatei (0,02 V, F2).
*Messung:* Einzelpunkt, **als .svd unter neuem Namen speichern** (nicht nur ablesen), Mittelungszahl möglichst ≥ 10. **Wiederholung nach kurzer Pause** zur Reproduzierbarkeit. Jede Messung mit eigener Entscheidung (Regel 1).
*Vor-Ort-Schnellprüfung (3 min):* Analysator, Kanal Vib 3D & Ref2, Signal H1 Geschwindigkeit/Beschleunigung (Namen vor Ort ablesen), Komponente Z. **Phase bei 20 bis 50 Hz** ablesen (dort verfälscht ein unkompensierter Vib-Delay höchstens 24°; das Vorzeichen ±90° ist eindeutig). Dann die Kohärenz in 100 bis 1000 Hz ansehen. Gleiches für Vib 3D & Ref1. Der Bereich „< 20 Hz“ ist als Stützstelle ungeeignet (Rauschen, hochpassartige Effekte, erste elastische Struktur ab etwa 20 bis 30 Hz); besser Kurve 10 bis 50 Hz (Vorzeichen) und 50 bis 1000 Hz (Delay, Betrag).
*Auswertung (nach dem Termin, an den Rohdaten):*
 1. Linien mit **γ² ≥ 0,98** wählen (bei n_d = 7 etwa 2,2° Phasenstreuung je Linie; Betrag-Bias bei reinem Eingangsrauschen ≤ 2 %) **[N]**.
 2. Fit φ(f) = φ₀ − 360°·f·τ_res mit φ₀ ∈ {−90°, +90°}, Phase entfaltet. φ₀ liefert das Vorzeichen s_V·s_2, τ_res die Kompensation. Zum Vergleich unkompensiert: bei 100/500/1000 Hz −48,0°/−240,0°/−480,1° (nur Vib, 1,3336 ms) bzw. −43,3°/−216,5°/−433,0° (Vib minus Ref1, falls Ref2 keinen Delay hat) **[N]**.
 3. Betrag: |H1|·ω als Funktion von f. Sollwert 1 (entspricht |H1| = 1,592 / 0,318 / 0,159 ms bei 100/500/1000 Hz; in der PSV-Einheit (mm/s)/(m/s²) dieselben Zahlen mal 10³). Einheit und ggf. g-Umrechnung (9,80665 m/s²) prüfen **[N]**.
 4. Vib Z/Ref1 am Treibpunkt: Anteil der Linien mit Re ≥ 0 (nur γ² ≥ 0,9; die Phase ist robust gegen Eingangsrauschen, der Betrag an Kraft-Einbrüchen nicht; dort zusätzlich H2 oder Hv).
*Entscheidungstabelle:*

| Vib Z/Ref2 | Vib Z/Ref1 (Treibpunkt) | Schluss |
|---|---|---|
| +90° | Phase in [−90°, +90°] | **Ref2 gedreht**, s_Ref2 = −1 (wie 7b) |
| −90° | Phase in [−90°, +90°] | beide konsistent; die Deutung aus 7b (Starrkörper < 20 Hz) war nicht tragfähig → Aufbau und Starrkörperbereich neu prüfen |
| −90° | um 180° versetzt | Ref1 gedreht |
| +90° | um 180° versetzt | Ref1 und Ref2 gedreht gegenüber Vib (Vib ist der Ausreißer) |

*Akzeptanz-Arbeitswerte* **[Annahme]**, bis Datenblattwerte vorliegen: |τ_res| ≤ 14 µs (5° bei 1 kHz); |H1|·ω zwischen 0,95 und 1,05; Abweichung > 10 % ist ein Befund.
*Weiter:* eindeutig nach der Tabelle. **Abbruch:** Dialog, Laser/Spiegel unerwartet, Kopf nicht messbar nach 10 min Sichtbarkeitsprüfung.
*Ersatz bei nicht sichtbarem Kopf oder ohne Zustimmung zur Folie (F6):* **Ersatzpunkt auf der Plattenvorderseite direkt gegenüber der Kopfmontage** (die Stirnflächen-Annahme entfällt; die Aussage zu Kraft und Vorzeichen gilt, die Amplitudenaussage nur bis zur ersten lokalen Plattennachgiebigkeit **[Annahme]**). *Ersatz ohne Freigabe der Anregung:* Datenblatt PCB 288D01 (Recherche R-0211); das Datenblatt erklärt die Ursache, ersetzt die Messung für die Software-Korrektur aber nicht. Kontrollversuch ohne Shaker (z. B. Klopfen) nur als Idee und nur mit Daniel/Betreuer.
**Voraussetzung:** F2 **ja**, F6 geklärt.

**D3 Zwei-Amplituden-Test A-B-A: 0,02 / 0,04 / 0,02 V an Label 132 (Soll, Rang 5, 30 min + Messdauer).**
*Zweck:* Linearität prüfen und von Drift trennen: Mit nur zwei Messungen wäre Nichtlinearität von Drift nicht unterscheidbar. Die Beispieldatei wurde mit 0,02 V gemessen (Faktenliste C3). Zusätzlich 0,01 V, **falls freigegeben** (F2).
*Schritte:* Gleicher Punkt wie Label 132 (gleiches Raster/.set wie `20261012_ref_Mitte`, **[offen]**, ob die .set vorliegt; sonst Punkt per Koordinaten (0,19089 / 0,42602 / −0,23125 m) setzen und notieren). **Reihenfolge A-B-A (0,02 / 0,04 / 0,02 V)**, je Messung nur Sekunden bis Minuten, sonst identische Einstellungen (Generator-Amplitude in PSV, Bezeichnung vor Ort), Verstärkerstellung unverändert und notiert, drei neue Dateinamen.
*Option:* D3 am Kopfpunkt (D2) statt an Label 132 (spart das erneute Anfahren); der Vergleich mit der Beispieldatei gehört dann zu D4.
*Auswertung:* |H1| und Phase **abseits der Spitzenlinien** (an unaufgelösten Spitzen verändert schon eine kleine Frequenzverschiebung den Linienwert stark, B < Δf); f_r und ζ der Spitzen bei 160,6 und 247,7 Hz über B-1. **Unterschied A-A (Drift) gegen A-B (Nichtlinearität).** Schwelle vorab (zufälliger Fehler, n_d = 7): |H| ≈ 9 % bei γ² = 0,9, 2,7 % bei 0,99, 0,85 % bei 0,999 **[N]**.
*Erwartung Kohärenz < 60 Hz:* Ist sie rauschbegrenzt, sinkt 1−γ² bei doppelter Amplitude etwa um den Faktor 4. Bleibt sie gleich, liegt Nichtlinearität, Zeitvarianz oder Leckage vor **[N]**. **Ref1-Autospektrum** beider Amplituden vergleichen (Kraft-Verhältnis ≈ 2, sonst Verstärker/Shaker-Sättigung).
**Voraussetzung:** F2 **ja** (auch für 0,04 V). **Ersatz:** nur 0,02 V freigegeben: Messung zweimal wiederholen (A-A, Reproduzierbarkeit/Drift) statt zweiter Amplitude, im Protokoll klar benennen.

**D4 Wiederholungsmessung T8 (Kann, nur mit Freigabe; Frage an Daniel F2).** Wie [alter Plan, T8](../2026-11-02_prototyp/ablaufplan_vor_ort.md): zweite Messung am selben Aufbau mit den Einstellungen von `20261012_ref_Mitte` (Vergleich B-5, FG-03 Abschnitt 4); wenn möglich zusätzlich mit neu abgeglichenem/verschobenem Raster; neuer Dateiname; Raumtemperatur Anfang/Ende, Uhrzeit, Änderungen am Aufbau notieren. Direkt in PSV oder über das Programm (Entscheidung ins Protokoll).
**Scandauer ca. 40 min** (Beispieldatei, Annahme aus dem alten Plan) plus ca. 45 min Vorbereitung; passt nur bei einem langen Termin (Planung 240 min) und nach allen Soll-Punkten, sonst **Folgetermin**. D3 A-B-A deckt die kurzzeitige Reproduzierbarkeit teilweise ab.
**Ersatz:** keine Freigabe: entfällt (EP-4); ein verkleinertes Raster (D1) kann den Zweck nur teilweise ersetzen.

**D5 T3 bis T7 über das Programm (Kann, nur nach Entscheidung).** Wie [alter Plan, Abschnitt 8](../2026-11-02_prototyp/ablaufplan_vor_ort.md): T3 Meldungsprobe, T4 erste echte Messung (mit Trockenlauf derselben .set, Startdialog prüfen, 4-1 bis 4-3, 4-1a), T5 Abbruch (5-1, 5-2), T6 Warteschlange (drei Messungen), T7 Speichern/Laden.
Reihenfolge T4 vor T5 vor T6; nach jedem Abbruchkriterium keine weiteren Messtests. **Voraussetzung:** COM ja, Anregung ja für T4 ff. Der Hardwaretest gilt erst nach deiner Bestätigung.
**Optional [Idee]:** D1 und T4 zusammenlegen (gleiche 3×3-Punkte), steht im Widerspruch zur Regel „Generator in der Test-.set aus“; nur nach eigener Entscheidung.

### Zweig E: ohne PSV, ohne COM, ohne Anregung

**E1 Platte und Impedanzkopf wiegen (Soll, Rang 3, 15 min).** *Zweck:* Massenlinie als grobe Kalibrierprobe (H1 Beschleunigung/Kraft ≈ 1/m im Massebereich); Masse von Platte und Impedanzkopf einzeln.
*Erwartung (grob):* **4,5 bis 6,7 kg** aus 1/(|Y|·ω) bei 1,25 bis 6,25 Hz im Golden File Label 132, ±20 % Streuung **[N, Fachprüfung; Betrag stark verrauscht, Transferpunkt statt Treibpunkt]**.
*Welche Masse gemeint ist:* die Masse auf der **Plattenseite des Kraftsensors**: Platte + plattenseitige Kopfhälfte (Datenblatt, „mass cancellation“) + Schrauben, Folie, anteilige Kabel. **Stinger und Shaker nicht.** Teile einzeln wiegen und die Zuordnung notieren.
*Gültiger Bereich der Massenlinie:* wegen der Antiresonanz (|Y| bricht bei 10 Hz um den Faktor 10 ein) **nur bis ca. 5 Hz**. Genauigkeit schlechter als eine Kalibrierprobe im Prozentbereich, bis eine bessere Messung vorliegt.
*Dreieckskontrolle:* Zusammen mit D2 entsteht eine Kontrolle: E1 prüft die Vib/Ref1-Kalibrierung, D2 die Vib/Ref2-Kalibrierung; daraus folgt Ref2/Ref1.
*Wann:* **Erst nach allen Messungen am Aufbau**, weil dafür der Aufbau verändert wird (Foto vorher; Impedanzkopf nur mit Zustimmung von Daniel lösen, Montageart **[offen]**; Anzugsmoment/Kleber unbekannt).
Waage (Typ, Auflösung, F5) ins Protokoll; Platte frei, Wert dreimal ablesen; Abmessungen (Maßband). Kopplung, Stinger, Seile gesondert, falls abnehmbar.
**Ersatz:** keine Waage/keine Freigabe zum Abbauen: Maße und Dicke der Platte messen (Material **[offen]**), Masse aus dem Datenblatt für den Impedanzkopf nachtragen; im Protokoll „nicht gewogen“.

**E2 Handbücher 10.4 kopieren (Soll, 10 min).** Quelle (Faktenliste A8): `C:\Program Files\Polytec\PSV 10.4\Doc` (Theory Manual.pdf, Software Handbuch PSV.pdf, Software Manual PSV.pdf, PSV-Desktop-Varianten, Basic Engine Manual.chm, Release Notes). Nur **kopieren** (nicht verschieben), auf den Stick bzw. nach `$T\export\handbuecher`; später nach `Input/literatur/polytec/` mit Versionskennzeichen im Namen (z. B. `…_PSV10.4.pdf`), vorhandene Dateien nicht überschreiben.
Dateigröße und SHA-256 notieren: `Get-FileHash "<Datei>"` und mit dem Hash der vorhandenen Fassung in `Input/literatur/polytec/Handbücher/` vergleichen (3.2). F8 beachten.
**Ersatz:** Zugriff verweigert oder Stick unbrauchbar: nur Dateiliste (`dir` des Ordners) sichern und Fotos der Titelseiten (Versionsstand).

### A2 Sicherung und Rückmeldung (Muss, 30 min; immer, auch bei Abbruch)

| Was | Ziel (Repository, nach dem Termin) | Hinweis |
|---|---|---|
| Erkundungsordner | `in_progress/versuche/erkundung/` | Durchsicht vor Upload |
| Ausgefülltes `protokoll.md`, Prüfzettel (Foto/Scan) | dieser Ordner | Anmeldenamen in Pfaden prüfen |
| Konsolenausgaben, Durchgangsordner, Konfigkopie mit SHA-256 | `…/ergebnisse` | `.svd` nur nach Rücksprache (Größe) |
| Golden File v2, Exporte (UFF/ASCII), `einstellungen_*.txt` | `…/export` | nur Kopien der Beispieldatei verwendet |
| `.svd` neuer Messungen (D1 bis D4), Zeitdaten | Rücksprache wegen Größe | nie überschreiben |
| Fotos (Aufbau vorher/nachher, PSV-Info, Dialoge) | `…/fotos` | |
| Handbücher | `Input/literatur/polytec/` | nach F8 |
| Test-.set, Nachweis-.set | | |
| PSV in sauberem Zustand (keine Messung, kein Dialog; Shaker wieder getrennt bzw. aus) | | |

Danach `/laborbuch` (Hardwaretest- und Versuchseintrag). Ein Befund gilt als „am Gerät bestätigt“ erst, wenn du ihn bestätigt hast.

---

## 6 Ersatzpläne

### EP-1 COM nicht registriert oder Verbinden scheitert

**Auslöser:** K2 „nein“ und K3 erfolglos, oder B1 „Verbinden scheitert“. **Entscheidung nach höchstens 30 min** [Annahme], damit die Termin-Zeit nicht in der Fehlersuche verschwindet.
**Weiter (Pfad B):**
1. Befund sichern: Stufe 0/1 komplett, Registry-Auszug, Fehlerbild (HRESULT), Foto; Uhrzeit.
2. **File Access ohne COM-Registrierung** läuft weiter (PolyFile registriert, A5/C7): Zweig C (C1 bis C8) auf Kopien.
3. **Prüfzettel ohne COM:** C2 bis C8, E1, E2, B5 (PolyMath-Typbibliothek ist registriert; PSV-Registrierung nicht nötig **[Annahme]**), B3 (Test-.set anlegen, Material für später).
4. **Simulator-Vorführung:** `& $PY -m ldv_automation gui --simulator` bzw. `selbsttest` (I5/I7), damit der Termin einen vorzeigbaren Software-Stand hat; **kein** Hardwaretest, so im Protokoll formulieren.
5. Mit Anregung (K6 ja): Zweig D **manuell in PSV** (D1 bis D4 brauchen kein COM).
6. Fragen an Daniel/Polytec-Support sammeln: Fehlerbild (HRESULT, Meldung „basic engine is not available, because the software is not registered as COM-server“), Registrierung, Lizenzbedarf (kein Beleg für Lizenzbedarf, Hinweis im Dokument zur Registrierung).
**Abbruch:** Dialog/Hänger in PSV: EP-5. **Ersatz für das Verbinden selbst:** Reparaturinstallation (Daniel), danach Stufe 0/1 erneut; Desktop-Gegenprobe X1.

### EP-2 Desktop-Modus

Läuft PSV (versehentlich oder bewusst) im Desktop-Modus:
- **Versehentlich:** nur lesen, nichts weiter an COM probieren, Fehlerbild notieren (wie X1), PSV beenden, über „PSV 10.4 Deutsch“ neu starten, PID neu notieren, Stufe 1 wiederholen.
- **Bewusst (X1):** Vorgehen X1. **Auswertung (C2, C8):** Die Analysator-Ansicht kann im Desktop-Modus laufen **[offen]**; dann C-Zweig in diesem Modus erledigen und COM-Arbeiten (B1 bis B4) vorher oder nachher in Acquisition.
- **Keine Mischung:** nie zwei Instanzen gleichzeitig; Wechsel immer über Beenden → `Get-Process PSV` leer → Start.

### EP-3 Installation scheitert

| Symptom | Ersatz |
|---|---|
| Kein Internet / GitHub nicht erreichbar / Repo privat | Weg S (Stick). Kein Stick: alten Stand 530af41 weiternutzen |
| `pip install` Fehler (Meldung wörtlich notieren) | Ohne Update weiter mit Stand 530af41 (I5, I6 prüfen: Hash `530af419`). T0 bis T2 laufen dann mit dem alten Adapter; die K-2D-Hinweise (Registrierung, Desktop-Modus) sind nicht testbar, Auswertung/K-ACHSE bleibt außen vor (im Entscheidungsprotokoll vermerken) |
| pip meldet „already satisfied“ oder I3/I6 zeigen noch 0.1.0 bzw. den alten Hash | Rückfall: `--upgrade --force-reinstall --no-deps` mit dem 0.2.0-Wheel; Dateiname und SHA-256 prüfen, Hash in I6 prüfen |
| I1 bis I4 schlagen fehl (z. B. Python 32-Bit, pywin32 fehlt) | Nicht weiter installieren; `erkundung.py` braucht nur Python 3.11 (Stufe 0) bzw. pywin32 (Stufe 1) und läuft auch **ohne** das Wheel; Prototyp dann nur als Befund |
| I5 oder I7 scheitern (Selbsttest, GUI) | Erkundung und COM-Tests der Erkundung bleiben möglich; Prototyp als Befund (nur CLI/Selbsttest) |
| Skripte nicht aktuell | Alte Skripte weiterverwenden (nur lesend; Exit-Codes anders), Stand (`skript_sha256`) im Protokoll |
| PySide6 6.12.0 wurde versehentlich gezogen | nicht benutzen (ADR-001); `pip install "pyside6-essentials==6.11.3" "shiboken6==6.11.3"` |
Nie mit dem Internet „nachhelfen“, bevor die Ursache bekannt ist; keine Änderungen an Polytec-Verzeichnissen.

### EP-4 Keine Freigabe der Anregung

Kein T4 bis T8, kein Mini-Scan (D1), kein D2/D3, Shaker/Verstärker bleiben vom Netz, Generator aus.
**Weiter mit:** A0, A1, B1 bis B4 (T0 bis T2 laufen ohne Anregung), Zweig C (inkl. M11 C2, Golden File v2 C3, C4 nur ablesen), Zweig E, B5, X1. Der Zeitgewinn (Wegfall D1 bis D4) geht zuerst in C2, E1, C3, E2.
**Ersatz für D2 (M8):** Datenblatt PCB 288D01 (Recherche R-0211, offen); C3 mit H1 Ref2/Ref1 (ohne Laser, Phase 0°/180° und Massenlinie bei 1 bis 6 Hz) stützt die relative Polarität von Ref1/Ref2 an vorhandenen Daten; D2 selbst ist nur mit Anregung möglich und wird für den Folgetermin vorgemerkt („was ginge mit Freigabe“).
**Ersatz für D1:** Test-.set mit Zeitdaten-Option anlegen (B3 Variante) und nicht laufen lassen; Dateigröße-Abschätzung aus der Beispieldatei **[Annahme]**.
**Frage an Daniel** wiederholen und Antwort samt Bedingungen (Amplitude, Dauer, Aufsicht) ins Protokoll.

### EP-5 PSV hängt oder Dialog

1. **Nichts hektisch klicken.** Foto/Screenshot des Dialogs, Uhrzeit. Läuft eine Messung (Laser, Spiegel, Scan-Fortschritt)? Steht der Shaker unter Strom?
2. **Skript/Programm zuerst anhalten:** Strg+C im Skript; das Programm im pausierten Zustand **nicht schließen**; Wächterhinweis „PSV reagiert nicht seit … s“ bzw. `GERAET_UNKLAR` notieren.
3. **Dialog lesen.** Eindeutig harmlos (Information): mit der Standardantwort „OK“ quittieren und notieren. Unklar, Speicher-/Überschreib-/Lizenzdialog: im Zweifel nicht bestätigen (Speichern: Nein, Überschreiben: Nein), Daniel.
4. **PSV wartet mehr als 5 Minuten [Annahme]** ohne Lebenszeichen: Daniel; erst danach PSV über den Task-Manager beenden. Zustand der laufenden Messdatei danach prüfen (nie verändern, Kopie ansehen).
5. **Nach Neustart:** `Get-Process PSV` (eine Instanz, neue PID), COM-Registrierung bleibt bestehen **[Annahme]**, Stufe 0 kurz wiederholen, dann an der Stelle vorher weitermachen, **nicht** mit der Messung, die gehangen hat, ohne neue Entscheidung.
6. Verursacher klären (Skript, Dialog, Messung) und ins Protokoll; war es das Skript: keine weiteren Skript-Aufrufe am Gerät.
**Ersatz:** Pfad B, Zweig C/E, Sicherung vorziehen.

### EP-6 Zeit wird knapp

1. **Zeit prüfen bei K8** nach A0/A1, nach B4 (bzw. nach EP-1 Entscheidung) und zu Beginn der Anregungs-Blöcke.
2. Streichreihenfolge Abschnitt 4 anwenden, das Protokoll führt jeden gestrichenen Punkt mit Grund.
3. **Spätestens 30 min vor Ende:** A2 beginnen (Sicherung, PSV sauber, Shaker getrennt, Dateien kopieren).
4. Ein begonnener Messschritt wird zu Ende gebracht oder sauber abgebrochen, nicht abgebrochen „halb“ gelassen.
5. Gestrichene Punkte landen auf der Liste für den Folgetermin (Prüfzettel unten abhaken/übertragen).
6. **Termin doch nur ca. 150 min:** verkürzte Reihenfolge nach Abschnitt 4.2 (A1 kürzen, bei freigegebener Anregung D2 vor B3/T2, D4/D5 auf den Folgetermin). D2 und E2 werden nie zusammen gestrichen.

### EP-7 File Access scheitert (Ergänzung)

Fehler beim Öffnen (Lizenz VBEng vorhanden, ReadOnly funktionierte am 02.11.): Kopie prüfen (nicht in PSV geöffnet, Größe gleich, kein Schreibschutz-Problem), `PolyFile.PolyFile` laut Stufe 0 registriert? Ersatz: Werte aus der PSV-Oberfläche ablesen/exportieren (C2, C3 über Export). Die Ergebnisse vom 02.11. bleiben gültig.

---

## 7 Offene Punkte und Annahmen dieses Plans

- **[offen]** Datum, Beginn, Ende, Verfügbarkeit von Daniel (F3). **Planung mit ca. 240 min [Annahme, nach Klärung mit Daniel]**; Fall 150 min in 4.2.
- **[offen]** Registrierung erfolgt? Zustimmung (F1); Freigabe Anregung (F2); Internet/GitHub/Stick (F7); Waage (F5).
- **[offen]** Ablageort der Skripte und Messdaten am Rechner, ob `PyCharmProject` ein Git-Repository ist (C1 alt).
- **[offen]** neues Wheel **0.2.0** (Build nach K-ACHSE) existiert noch nicht, Ablageort offen; PeakFit-Signatur und -Modell (B5); Burstform/-länge des Generators (C4); ob SE „Fast“ die SignalDelay ändert; Ref2-SignalDelay; ob PSV die Referenzrichtung im Vorzeichen auswertet (unbelegt, im Handbuch nachsehen); Skripte im aktuellen Stand; Namen für Golden File v2; vorab-Kandidatenprüfung für M11.
- **[offen]** In welchem PSV-Modus die Auswertung am 02.11. lief; Menübezeichnungen für SaveTimeDataForScan, Generator-Amplitude, Export, Test-.set.
- **[Annahme]** alle Dauern; Pfade `$ARB`/`$T`; Dateinamensschema; „nach höchstens 30 min Entscheidung“ in EP-1; „5 Minuten“ in EP-5; PolyMath ohne PSV-Registrierung nutzbar; Update nicht nötig für T0 bis T2; Kopf bis 1 kHz starr, Folie masselos (D2); Arbeitstoleranzen in D2 (14 µs, ±5 %).
- Zahlen mit **[N]** stammen aus Nachrechnungen der Fachprüfung (FD-P3) und sind nicht am Gerät geprüft; ζ ≈ 1,4·10⁻³ für die Kandidaten-Vorabrechnung stammt aus nur zwei Spitzen.
- Kein Befund aus diesem Plan ist am Gerät geprüft. Alle Windows-Befehle sind **ungetestet**.
