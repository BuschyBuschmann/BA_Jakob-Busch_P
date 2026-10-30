# Ablaufplan vor Ort: PSV-Messrechner, Mo 2026-11-02

Stand: 2026-10-27, Paket P6. Jakob arbeitet allein am Messrechner.
Details stehen in den verlinkten Dokumenten; hier nur Reihenfolge, Zeitbedarf, Weiter-/Abbruchbedingungen.
Zeiten sind **grobe Annahmen** (nicht gemessen, nicht belegt) und dienen nur zur Priorisierung.

Quellen: [Plan P2, Abschnitt 9](../../planung/plaene/2026-10-26_P2_architektur-prototyp.md) (E0 bis T7),
[Prüfanleitung U3](pruefanleitung_U3_com-adapter.md), [Handtest U4](handtest_U4_gui.md),
[Erkundung-README](../../../software/tools/erkundung/README.md),
[Installation](installation_messrechner.md), [Test-.set](anleitung_test_set.md),
[Protokollvorlage](protokoll_vor_ort.md).

## Grundregeln (gelten den ganzen Tag)

1. **Eine echte Messung (T4 ff.) läuft nur nach deiner eigenen ausdrücklichen Entscheidung**
   und nie, bevor T1 und T2 ohne Befund durch sind. Ein Hardwaretest gilt erst als bestanden,
   wenn du ihn bestätigt hast.
2. **Nach einem Hänger nie die Anwendung einfach weiterbenutzen.** Erst in PSV selbst den
   Zustand prüfen (läuft eine Messung? steht ein Dialog offen?), Hinweis des Wächters („PSV
   reagiert nicht seit … s“) bzw. `GERAET_UNKLAR` notieren. Das Programmfenster **nicht im
   pausierten Zustand schließen** (der Durchgang ist dann noch offen; das Verhalten beim
   Schließen im pausierten Zustand ist im Handtest nicht geprüft). Erst fortsetzen oder abbrechen.
3. **Tabellen-Nr ≠ Dateinummer.** Die Nr in der Tabelle ist vorläufig (grau/kursiv), bis der Durchgang
   die Messung startet; die Dateinummer vergibt die Steuerung in Startreihenfolge. Zuordnung
   Datei ↔ Eintrag immer über **Name/ID im Messprotokoll**, nicht über die Zeilennummer.
4. Alle Ordner **lokal** (z. B. `C:\ldv\…`), kein Netzlaufwerk. Messdaten-Ordner nicht unter
   Programm-/Datenordnern (ProgramFiles, ProgramFiles(x86), ProgramW6432, ProgramData, Windows-Ordner), einem Ordnerteil „Polytec“ direkt unter der Laufwerkswurzel oder im Repository.
5. Rohdaten werden nie überschrieben (KONVENTIONEN). Bei Abbruch gilt: Ordner trotzdem sichern.
6. Shaker/Verstärker bleiben getrennt, solange der Betreuer die Anregung nicht freigegeben hat.

## Zeitplan und Priorität

Gesamt etwa 8 bis 9 Stunden bei vollem Programm (Summe der Annahmen unten, ohne Scandauer T8). Reicht die Zeit nicht,
gilt diese Reihenfolge der Streichung [Vorschlag, bitte bestätigen]: zuletzt entfallen T6/T7, T8, 1b,
T3, T5; **nicht streichen**: 0 bis 4 (Installation, Erkundung, Schalter), T0, T1, T2.

| Nr | Abschnitt | Annahme | Priorität |
|---|---|---|---|
| 0 | Vorbereitung | 15 min | Muss |
| 1 | Installation (E0) | 30 min (Weg A) | Muss |
| 2 | Erkundung Stufe 0 | 5 min | Muss |
| 3 | Erkundung Stufe 1 | 15 min | Muss |
| 3b | Erkundung Stufe 1b | 10 min | Kann |
| 4 | Ergebnisse sichern, Schalter bestimmen | 20 min | Muss |
| 5 | Test-.set anlegen (nach [Anleitung](anleitung_test_set.md)) | 30 min, hängt von PSV-Bedienung ab | Muss für T2 |
| 6 | T0, T1, T2 | 15 + 20 + 30 min | Muss |
| 6b | Handtest U4 (Teilmenge) | 30 min | Soll |
| 7 | T3 (Meldungsprobe), optional | 10 min | Kann |
| 7b | Auswertungs-Prüfungen in PSV (M1–M15, Export) | 45 min | Soll |
| 8 | T4 erste echte Messung | 30 min | Soll, nur nach Entscheidung |
| 8b | T5 Abbruch | 20 min | Kann, nur nach Entscheidung |
| 8c | T6 Warteschlange mit drei Messungen | 45 min | Kann, nur nach Entscheidung |
| 8d | T7 Speichern/Laden, `--ereignisse` | 15 min | Kann |
| 8e | T8 Wiederholungsmessung für B-5 | 45 min + Messdauer (Beispieldatei: ca. 40 min Scan) | Soll, nur nach Entscheidung |
| 9 | Sicherung und Rückmeldung | 30 min | Muss |

## 0 Vorbereitung (ca. 15 min)

- [ ] Stick: Wheelhouse inkl. `ldv_automation-0.1.0-py3-none-any.whl`, Python-3.11-Installer,
  `erkundung.py`, diese Dokumente (siehe [Installation, Abschnitt 3](installation_messrechner.md)).
- [ ] Ordner anlegen: `C:\ldv\daten` (Messdaten), `C:\ldv\vorlagen` (`.set`), `C:\ldv\erkundung`.
  Kein Netzlaufwerk, nicht unter Polytec/Programmordnern/Repository.
- [ ] [Protokollvorlage](protokoll_vor_ort.md) öffnen (Kopf ausfüllen: Datum, Rechner, PSV-Version
  laut *Hilfe > PSV Info*).
- [ ] PSV läuft im **Erfassungsmodus**, keine Messung, keine offenen Dialoge. In PSV
  „Meldungen bei Automatisierung unterdrücken“ aktiv (Adapter schaltet es nie selbst ein; genaue
  Bezeichnung in der Oberfläche vor Ort ablesen und notieren).
- [ ] Prüfling noch nicht anregen; Shaker/Verstärker getrennt.

## 1 Installation (E0, ca. 30 min)

Nach [installation_messrechner.md](installation_messrechner.md), Abschnitte 2, 5, 6 (I1 bis I7).
**Weiter, wenn:** I1 bis I4 ok. **Fehler:** Meldung wörtlich notieren; ohne pywin32 nur Simulator
vorführen (Plan E0).

## 2 Erkundung Stufe 0 (ca. 5 min)

Nach [Erkundung-README](../../../software/tools/erkundung/README.md), Schritte 1 bis 3:

```powershell
C:\ldv\venv\Scripts\python.exe C:\ldv\erkundung\erkundung.py --stufe 0 --out C:\ldv\erkundung
```

`zusammenfassung.md` und `registry.reg.txt` ansehen, besonders `P1-2-registry` (`LocalServer32`?)
und `psv_prozesse` (nur PSV selbst, Abbildname notieren). **Weiter, wenn:** pywin32 importierbar,
ProgIDs registriert.

## 3 Erkundung Stufe 1 und 1b (ca. 15 + 10 min)

PSV im Erfassungsmodus, **keine Dialoge offen**, keine laufende Messung:

```powershell
C:\ldv\venv\Scripts\python.exe C:\ldv\erkundung\erkundung.py --stufe 1 --out C:\ldv\erkundung
# optional 1b, mit Kopie einer vorhandenen Messdatei, nicht in PSV geöffnet:
C:\ldv\venv\Scripts\python.exe C:\ldv\erkundung\erkundung.py --stufe 1 --datei "C:\ldv\vorlagen\Example.svd" --out C:\ldv\erkundung
```

Das Skript startet PSV nicht (`--start-psv` nicht verwenden). Zusätzlich manuell: PSV-Version und
Optionen laut *Hilfe > PSV Info* (Text oder Foto) und ob ein Fenster in PSV aufpoppte.
**Weiter, wenn:** Verbinden klappt, `Mode`, `State`, Version gelesen, Validator-Befund, `Suppress`,
Konstanten passen zu I5 §8. **Fehler:** Verbinden scheitert, dann kein COM-Test des Prototyps,
nur Simulator und Befunde sichern.

## 4 Ergebnisse sichern und Schalter bestimmen (ca. 20 min)

1. Ausgabeordner `erkundung_<Rechnername>_<Zeit>` komplett sichern (Stick, ggf. ZIP). Er geht später
   nach `in_progress/versuche/erkundung/`.
2. **Durchsicht vor jedem Upload (Pflicht)** nach [Erkundung-README, Sicherheitskonzept](../../../software/tools/erkundung/README.md):
   in `bericht.json`, `zusammenfassung.md`, `konsole.log` prüfen auf `kommandozeile`, `parameter.datei`,
   `dateien.*.pfad`, `Acquisition.ScanFileName`, Netzlaufwerkspfade, Fehlermeldungen (`exception`,
   `excepinfo`) mit Pfaden oder Kontonamen. Der Rechnername bleibt im Klartext, Seriennummern
   im Bericht.
3. Schalterwerte nach der Tabelle in [U3, „Schalter aus der Erkundung übernehmen“](pruefanleitung_U3_com-adapter.md)
   bestimmen (Validator ja/nein; Konstanten weichen ab, Prozessname ohne `psv` oder Fehltreffer: **stoppen**)
   und im Protokoll (A3) festhalten.

4. **Konfigurationsdatei anlegen.** Die Schalter stehen in einer JSON-Datei, die mit `--konfig DATEI`
   beim Start von `gui` und `selbsttest` angegeben wird (`software/konfig/beispiel_messrechner.json`,
   Modul `ldv_automation.konfig`). Vorgehen:
   - Beispieldatei **kopieren**, z. B. nach `C:\ldv\konfig_montag.json` (Original nicht ändern).
   - Werte aus der Erkundung eintragen: `validator_rueckfall_direkt` (true, wenn der Validator fehlt),
     `lademaske` (Gruppennamen; Camera und Windows lässt die Richtlinie nicht zu),
     `aufruf_grenze_s`, `aufruf_warnung_s`, `stop_frist_s`, `standard_zeitlimit_s`
     (Vorgaben: false, Acquisition/Alignment/APS/2DAlignment/3DAlignment, 60, 5, 10, 600). Zeiten, die erst
     T4/T5 liefern, bleiben zunächst bei der Vorgabe und werden nach der Messung in einer neuen Kopie nachgezogen.
   - Ungültige Datei (unbekannter Schlüssel, falscher Typ, Wert außerhalb des Bereichs): Der Start bricht mit
     Rückgabewert 2 ab; Meldung notieren, korrigieren.
   - **Pfad und SHA-256 der Kopie** (`Get-FileHash C:\ldv\konfig_montag.json`) im Protokoll festhalten
     (Abschnitt 1). Beides steht auch in jedem Messprotokoll und im Dialog „Gerät …“ und ist dort zu vergleichen.
   - Start dann mit `--konfig`, z. B.
     `C:\ldv\venv\Scripts\python.exe -m ldv_automation gui --psv --betriebsart trockenlauf --messdaten C:\ldv\daten --konfig C:\ldv\konfig_montag.json`.
   - **Kein Eingriff in den installierten Code.** Nach jeder Änderung der Werte eine neue Kopie mit neuer SHA-256
     anlegen, die alte aufheben.

## 5 Test-.set vorbereiten (ca. 30 min)

Nach [anleitung_test_set.md](anleitung_test_set.md): kleine Einstellungsdatei mit wenigen Punkten,
Generator aus, speichern unter `C:\ldv\vorlagen\test_3x3.set`. Prüfling vorbereiten (Aufbau, Lagerung
und Anregung entscheidest du; nichts anschließen, was der Betreuer nicht freigegeben hat).

## 6 Prototyp-Prüfung T0 bis T2

**T0 (ca. 15 min).** Bereits in Abschnitt 1 (I5 und I7); zusätzlich Handtest F4 (Symbole).
Dokumentiert in [Prüfanleitung U3, Ergänzung U5](pruefanleitung_U3_com-adapter.md).

**T1 `NUR_LESEN` (ca. 20 min).** U3, Abschnitt T1 (Konsole oder Oberfläche):

```powershell
C:\ldv\venv\Scripts\python.exe -m ldv_automation gui --psv --betriebsart nur_lesen --messdaten C:\ldv\daten --konfig C:\ldv\konfig_montag.json
```

Prüfen: 1-0 bis 1-6 (U3) und U5-Ergänzung (Dialog „Gerät …“: „N Zugriffe, keine Verweigerung“,
Messpunkte, Generator, `psv_prozesse`, Lademaske). **Weiter, wenn** keine Verweigerung und alles wie
Erkundung/PSV-Anzeige. **Abbruch:** Abweichung oder Verweigerung, Protokoll sichern.

**T2 `TROCKENLAUF` (ca. 30 min).** Der Trockenlauf **ändert die aktuellen PSV-Einstellungen**
(bewegt nichts; Hinweisdialog erscheint). Zuerst die Konfigurationsdatei aus Abschnitt 4 prüfen und mit `--konfig` starten
(Validator-Rückfall und Lademaske kommen daraus; die Konsole nach U3, T2 bleibt als Ausweg). Prüfen: 2-1 bis 2-7 (U3), insbesondere **Einrasten bei 5600 Hz**
(Wert notieren) und Übereinstimmung mit der PSV-Anzeige. **Abbruch:** unerwarteter Dialog, Laser-
oder Spiegelbewegung, Abweichung zur PSV-Anzeige.

## 6b Handtest U4 am Messrechner (ca. 30 min, Teilmenge)

Der [Handtest U4](handtest_U4_gui.md) ist ein Simulatortest. War er auf dem Entwicklungsrechner
noch nicht komplett durch, am Messrechner mindestens: A1 bis A5, C1, C4 bis C9, D1 bis D3, F3, F4
(Windows-spezifisch: Schrift, Symbole, 1100 × 680) [Vorschlag]. Start über Venv-Python mit
`gui --simulator` statt `uv run`. Dazu: Messdaten-Ordner im Dialog „Einstellungen …“ setzen und die
Ordnerregeln der Sitzung (K-U5b) prüfen; notieren, **in welchen Ordnern PSV selbst Daten ablegt**.
Die Pfade werden normiert. Abgelehnt werden: relative Pfade, Netzwerkpfade, Ordner unter ProgramFiles,
ProgramFiles(x86), ProgramW6432, ProgramData oder dem Windows-Ordner (SystemRoot), ein Ordnerteil
„…Polytec…“ direkt unter der Laufwerkswurzel (z. B. `C:\Polytec\…`), Git-Repositorys und
8.3-Kurznamen (z. B. `PROGRA~3`; dann den langen Pfad angeben). Das Benutzerkonto `C:\Users\Polytec\…` ist erlaubt.
Im Dialog „Einstellungen …“ werden Ordner und Standard-Zeitlimit nur **gemeinsam** übernommen.

## 7 T3 Meldungsprobe (optional, ca. 10 min)

Nur mit dir am Gerät (I5 P1-8): Existiert die Zieldatei, fängt die Vorprüfung ab und PSV erhält
keinen Aufruf (U3 6-1).

## 7b Auswertungs-Prüfungen in PSV (ca. 45 min, ohne Messung)

Ziel: die Annahmen der Auswertung (FG-02 Abschnitt 11: M1–M11, FG-03 Abschnitt 11: M12–M15) am
Original-PSV prüfen. Grundlage ist eine **Kopie** von `20261012_ref_Mitte.svd` auf dem Messrechner
(nie das Original öffnen); in PSV nichts speichern. Ergebnisse in [Protokoll](protokoll_vor_ort.md),
Abschnitt 6b, Screenshots sichern. Bezugspunkt ist **Label 132**.

| Nr. | Was in PSV ablesen bzw. tun |
|---|---|
| M1 | „Vib X & Ref1“, H1, Phase (oder Real/Imag) bei 100, 500, 1000 Hz |
| M2 | erste und letzte Frequenz der Achse (erwartet 1,5625 Hz und 2500 Hz) |
| M4 | „Vib X Geschwindigkeit“ bei 100, 500, 1000 Hz (Betrag, Skalierung Spitze/RMS notieren) |
| M5 | Fenster, Generator (Signalform, Burstlänge), Mittelungsart und -anzahl, Signal Enhancement |
| M6 | Scanstatus der Punkte (besonders Punkte mit Statuswert 1 und 3) |
| M7 | Bedeutung „Bandbreitenbereich 1 kHz“ (Anzeige, Datenblatt, Betreuer fragen) |
| M8 | Typ, Ort, Einbaurichtung von Kraftsensor (Ref1) und Beschleunigungsaufnehmer (Ref2), Shakerposition; Foto |
| M10 | Band 100–200 Hz definieren, RMS „Vib Z Geschwindigkeit“ ablesen |
| M11 | Band-Cursor-Fit auf H1 „Vib Z & Ref1“: an drei Spitzen ohne Warnkennzeichen und einer mit, **zusätzlich bei 401,6 Hz und 618,9 Hz** (Vergleich mit dem Modenfit B-1); f_max, „Dämpfung“ und Cursorgrenzen notieren |
| M12 | Achsen des 3D-Abgleichs: liegen die 3D-Komponenten im Koordinatensystem der Geometrie? |
| M13 | Lage der Scanköpfe zum Prüfling: zeigt +z vom Prüfling zu den Köpfen? |
| M14 | ein Element ansehen: Eckpunkt-Labels gegen die Indizes (0-basiert?) |
| M15 | Messzeit in der PSV-Info: Zeitstempel je Punkt = Messzeitpunkt? |
| Export | Golden File: für Label 132 „Vib X Geschwindigkeit“ und H1 „Vib Z & Ref1“ als ASCII exportieren (Formatwahl und Optionen notieren) |

**Abbruch:** PSV fragt beim Schließen nach Speichern (immer „Nein“), Dialog oder Fehler: Befund sichern.
Fehlt die Zeit, gilt die Reihenfolge M8, M1, M11, M12–M15, Export, Rest [Vorschlag].

## 8 Echte Messung T4 bis T7 (nur nach deiner eigenen ausdrücklichen Entscheidung)

Vor T4 selbst entscheiden und im Protokoll vermerken (Zeit, Entscheidung, Grund). Voraussetzungen
(Plan 6, Freischaltung von `MESSEN`): Verbindung steht, `State == Stopped`, Meldungen unterdrückt,
Git-Hash bekannt, Messdaten-Wurzel gesetzt und beschreibbar, Trockenlauf des ersten Eintrags ohne Abweichung.

- **T4 (ca. 30 min):** Vorher in derselben Sitzung einen **Trockenlauf mit genau der .set**, die gemessen wird, und **ohne PSV-Neustart**
  dazwischen (PSV nicht mit `--start-psv` selbst gestartet). Nur dann übernimmt der Startdialog gelesene Messpunkte
  und Generator aus dem Trockenlauf (Kennzeichnung „aus (übernommen)“; Bedingung: gleicher nicht-leerer
  PSV-Prozesstreffer, gleiche Lademaske, unveränderte .set). Sonst steht „unbekannt“ mit roter Warnung: dann den
  Generator **von Hand in PSV prüfen** und nur mit Freigabe von Shaker/Verstärker fortfahren.
  `MESSEN` freischalten, Durchgang mit **einer** Messung. Im Startdialog Generatorzeile
  prüfen (rot: nur mit Freigabe von Shaker/Verstärker fortfahren), `MESSEN` eintippen. Prüfen: 4-1 bis 4-3,
  4-1a (erster `State` nach `ScanEx`, Wert notieren, erwartet `ScanAll` = 3), 4-2 (blockiert `ScanEx`?),
  `.svd` am Zielpfad, Dauer notieren.
- **T5 (ca. 20 min):** Abbrechen nach wenigen Punkten; 5-1, 5-2. `GERAET_UNKLAR`: PSV manuell prüfen,
  **Ende der Messtests**.
- **T6 (ca. 45 min):** drei Messungen und ein Pausenpunkt, Bearbeiten im Lauf; Zeitlimit für eine Messung
  bewusst knapp (Fehlerpfad, R-019 vorläufig). Messtabelle und Protokolle später über Name/ID zuordnen.
- **T7 (ca. 15 min, optional):** `--ereignisse`, `--fortschritt punktstatus`, Speichern und Laden der Warteschlange.

- **T8 Wiederholungsmessung (Soll, ca. 45 min plus Scandauer):** zweite Messung am selben Aufbau mit den
  Einstellungen von `20261012_ref_Mitte` (für den Vergleich B-5 nach FG-03 Abschnitt 4). Wenn möglich
  zusätzlich eine Messung mit **neu abgeglichenem bzw. verschobenem Raster** (prüft die Punktzuordnung
  über Koordinaten). Unter neuem Dateinamen speichern, nie eine vorhandene Datei überschreiben.
  Notieren: Raumtemperatur am Anfang und Ende (Drift, FG-03 4.5), Uhrzeit, Änderungen am Aufbau.
  Kann über das Programm (Warteschlange) oder direkt in PSV laufen; Entscheidung im Protokoll.

Die Reihenfolge ist bindend: T4 vor T5 vor T6; nach jedem Abbruchkriterium keine weiteren Messtests.

## 9 Sicherung und Rückmeldung (ca. 30 min)

Zu sichern (alles nach `in_progress/versuche/2026-11-02_prototyp/` bzw. `…/erkundung/`, Pfade ohne Geräteordner):

| Was | Hinweis |
|---|---|
| Erkundungsordner `erkundung_<Rechner>_<Zeit>/` | Durchsicht (Abschnitt 4, Punkt 2); keine Messdaten |
| Durchgangsordner (Protokolle, `durchgang.ereignisse.jsonl`, Warteschlangenkopie) | `.svd` nur nach Rücksprache (Größe) |
| Konsolenausgabe, `g.aufrufe()`, Verweigerungen (aus T1/T2) | |
| ausgefülltes [Protokoll](protokoll_vor_ort.md), Fotos/Screenshots PSV | Anmeldenamen in Pfaden prüfen |
| Nachweis-`.set` aus T2, Test-`.set` | |
| Notizen zu Handtest-Zeilen (✔/✖) | |
| Ergebnisse 7b (Screenshots, ASCII-Export Golden File) | nur Kopie der Beispieldatei verwendet |
| `.svd` der Wiederholungsmessung(en) T8 | nach `Input/` über Upload; Größe beachten |

Danach `/laborbuch` (Hardwaretest- und Versuchseintrag). Ein Befund gilt als „am Gerät bestätigt“ erst,
wenn du ihn bestätigt hast.

## Abbruchkriterien (gesammelt)

Bei jedem Punkt: aufhören, Befund sichern (Ordner trotzdem hochladen), nicht „einfach weitermachen“.

| Quelle | Kriterium |
|---|---|
| Plan 9, U3 | unerwarteter Dialog in PSV |
| Plan 9, U3 | Laser oder Spiegel bewegt sich außerhalb von T4 bis T6 |
| Plan 9, U3 | Eintrag unter `verweigert` bzw. „verweigert“ in der Oberfläche, nicht bewusst provoziert |
| Plan 9, U3 | GUI/PSV reagiert länger als die Wächtergrenze nicht (Band „PSV reagiert nicht seit N s“) |
| Plan 9, U3 | eine vorhandene Datei wurde verändert |
| Plan 9, U3 | Generator gibt unerwartet aus |
| U3 | T1 Nr 1-0: `psv_prozesse` enthält etwas anderes als PSV (Fehltreffer) |
| U3 | **4-1a:** erster Poll nach `ScanEx` liefert `Stopped`, obwohl der Scan danach läuft: Start ist asynchron, der Adapter würde den Scan als fremd behandeln und **nicht stoppen**. Sofort aufhören, PSV manuell stoppen, Befund melden |
| U3 | `State` wird nach `Stop` nicht `Stopped` (`GERAET_UNKLAR`): PSV manuell prüfen, keine weiteren Messtests |
| U3 | Konstanten weichen von I5 §8 ab: nichts weiter am Gerät |
| Erkundung | PSV zeigt Dialog/Fehler/reagiert nicht; „blockiert bei …“; Laser/Spiegel schaltet bei Stufe 1 (Befund zur Whitelist); „verweigert (Default deny)“ (Strg+C) |
| Plan 9, T4 | `State` wird nicht `Stopped` innerhalb des Zeitlimits, Dialog, Fehlermeldung: Abbrechen (eigener `Stop`), keine weiteren Messungen |
| Handtest G | PSV-Dialog erscheint und Oberfläche bleibt nicht bedienbar |

Nach einem Abbruch: Python-Konsole bzw. Programm schließen, **PSV nicht beenden**, solange eine Messung
läuft; Zustand in PSV selbst prüfen.

## Dokumente dieses Ordners

Siehe [README.md](README.md).
