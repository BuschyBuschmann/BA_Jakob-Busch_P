<!-- Plan P2 (software-engineer, opus), Status: PLAN ZUR FREIGABE; unverändert übernommen. -->

## Plan P2: Prototyp Mess-Warteschlange mit kleiner GUI (Test am PSV-Messrechner, Mo 2026-11-02)

**Gelesen:**
- `/home/user/BA_Jakob-Busch_P/KONVENTIONEN.md`
- `/home/user/BA_Jakob-Busch_P/in_progress/anforderungen/lastenheft.md`
- `/home/user/BA_Jakob-Busch_P/in_progress/analysen/2026-10-23_I5_com-referenz.md`, vollständig
- I1, Abschnitt A3 (ADR-Vorschläge)
- Plan E1 (`/home/user/BA_Jakob-Busch_P/in_progress/planung/plaene/2026-10-23_E1_erkundungsskript.md`)
- `/home/user/BA_Jakob-Busch_P/software/pyproject.toml`
- `/home/user/BA_Jakob-Busch_P/software/tools/erkundung/erkundung.py`: Proxy, Policy, Checks
- `/home/user/BA_Jakob-Busch_P/software/tools/erkundung/README.md`
- `/home/user/BA_Jakob-Busch_P/software/tests/tools/erkundung/fake_psv.py`: nur die Struktur
- `/home/user/BA_Jakob-Busch_P/TODO.md`
- Laborbuch-Eintrag Betreuertermin 2026-10-26

In der Textfassung `polytec-chm-text/basic-engine-manual/PSV/` habe ich diese Belege nachgeschlagen:
- `ScanEx` (Modi, Caps, Asynchron-Flag)
- `ScanFileName` („empty → software will ask“)
- `Stop`
- `State` (read-only)
- `SuppressMessagesForAutomation` (Standard true)
- `MessageOccurred` (pVal simuliert die Antwort)
- `Settings.Load` (Einstellungs- oder Messdatei)

Alle anderen Belege stammen aus I5 und sind dort als [ungeprüft], [offen] oder [Einschätzung] gekennzeichnet. Das übernehme ich so.

Im Repository wurde nichts geändert.

**Ausgangslage:** Bisher steht das Gerüst `software/src/ldv_automation/__init__.py` mit leerem Paket. Unter `software/tools/erkundung/` liegen das Erkundungswerkzeug und der Fake-PSV.

Der wichtigste Planungsbefund: **Der Prototyp entsteht, bevor die Erkundung am Gerät gelaufen ist.** Erkundung und Prototyp-Test sind beide am selben Montag. Jede noch unbestätigte Annahme aus I5 braucht deshalb im Prototyp einen Schalter oder einen Rückfallweg. Der Testplan am Montag schaltet sie anhand der Erkundungsergebnisse frei.

---

## Plan

**Ansatz:** Ein GUI-unabhängiger Kern trägt die gesamte Logik:
- Domäne
- Warteschlange
- Ablaufsteuerung als Zustandsmaschine
- Ablage und Protokoll

Der Kern arbeitet gegen ein `Protocol` für die Geräteschnittstelle. Davon gibt es zwei Umsetzungen: einen Simulator (Pflicht nach KONVENTIONEN) und einen COM-Adapter. Jeder COM-Zugriff läuft durch einen neuen Whitelist-Proxy mit „Default deny“, Wertprüfung und einer Messfreigabe-Sperre.

Die GUI ist eine dünne Schicht über einer Sitzungsfassade. Diese liefert ein unveränderliches Zustandsbild und nimmt Befehle an.

Für den Prototyp gilt bewusst die konservativste belegte COM-Variante:
- Late Binding
- Polling von `State`
- Einstellungen per `.set`, Parameter über den Validator, danach Zurücklesen

Events und Early Binding bleiben optional, bis die Erkundung sie bestätigt.

**Verworfene Alternative:** Den Prototyp als Erweiterung von `erkundung.py` bauen. Das ginge schneller, verletzt aber die Trennung Werkzeug/Hauptpaket aus KONVENTIONEN. Außerdem ließe sich daraus keine Warteschlange mit GUI sauber testen.

### 1 Modulstruktur unter `software/src/ldv_automation/`

| Modul | Verantwortung | darf importieren |
|---|---|---|
| `domaene/eintraege.py` | `Messung` (ID als UUID, Name, Pfad der Einstellungsdatei, Parameteränderungen, Zeitlimit in s, Notiz, Versuchszähler) und `Pausenpunkt` (ID, Text); Zustands-Enums je Eintrag | nur stdlib |
| `domaene/parameter.py` | Parameterkatalog: Schlüssel, Typ, Einheit, Wertebereich, Zuordnung zur COM-Gruppe. Erweiterbar, weil O3 offen ist | stdlib |
| `domaene/warteschlange.py` | Geordnete Liste von Einträgen mit Sperre (`threading.Lock`). Einfügen, Entfernen, Bearbeiten und Umsortieren nur für Einträge im Zustand `WARTEND`. Atomares `naechsten_beanspruchen()` für die Ablaufsteuerung | `domaene` |
| `geraet/schnittstelle.py` | `Protocol Messgeraet` plus Datentypen (`GeraeteInfo`, `GeraeteZustand`, `EinstellungsStand`, `Meldung`, `Fortschritt`) und eine Fehlerhierarchie (`GeraeteFehler`, `ZeitlimitFehler`, `AbweichungFehler`, `VerweigertFehler`) | `domaene` |
| `geraet/simulator.py` | Simulator der Schnittstelle (Abschnitt 5) | `geraet.schnittstelle` |
| `geraet/com/konstanten.py` | Eigene `IntEnum`-Spiegelung der benötigten Werte aus I5 Abschnitt 8 | stdlib |
| `geraet/com/whitelist.py` | Allgemeiner Proxy mit Richtlinie als Parameter: get/call/set, Argument- und Wertprüfung, Aufrufprotokoll, Erkennung blockierender Aufrufe („pending“), Sperre `messfreigabe` | stdlib |
| `geraet/com/richtlinie.py` | Produktiv-Richtlinie (Abschnitt 3.3) mit Begründung je Schreiboperation | `whitelist`, `konstanten` |
| `geraet/com/adapter.py` | `PsvComGeraet` setzt `Messgeraet` um. Ablauf aus I5 Abschnitt 3; arbeitet nur über Proxys | `geraet.schnittstelle`, `geraet.com.*` |
| `geraet/com/pywin32_bindung.py` | Dünne Schicht: `Dispatch`, `CoInitialize`/`CoUninitialize`, optional `PumpWaitingMessages`, Prozessprüfung. `# pragma: no cover` mit Begründung. **Einzige Stelle mit pywin32-Import** | pywin32 (nur Windows) |
| `ablauf/uhr.py` | `Protocol Uhr` (monotonic, sleep) plus Echtzeit- und Testuhr. Damit laufen Tests ohne echtes Warten | stdlib |
| `ablauf/fehlerstrategie.py` | `Protocol Fehlerstrategie` plus **vorläufige** Umsetzung `PausierenUndNachfragen`, sichtbar als „vorläufig (O1/F20)“ gekennzeichnet | `domaene` |
| `ablauf/steuerung.py` | Zustandsmaschine des Durchgangs, Arbeitsschleife im Geräte-Thread, Ablauf einer Messung (Abschnitt 3), Befehle Pause/Fortsetzen/Abbrechen/Bestätigen/Fehlerentscheidung | `domaene`, `geraet.schnittstelle`, `protokoll`, `ablauf.*` |
| `protokoll/version.py` | Paketversion plus Git-Hash (Abschnitt 4.4) | stdlib |
| `protokoll/ablage.py` | Ordner- und Dateinamen, Schutz gegen Überschreiben (`exist_ok=False`, Öffnen mit Modus `"x"`), SHA-256 | stdlib |
| `protokoll/messprotokoll.py` | Schema und Schreiben der Messprotokolle sowie des Ereignisprotokolls eines Durchgangs | `domaene`, `geraet.schnittstelle` |
| `persistenz/warteschlangendatei.py` | Warteschlange als JSON speichern und laden, mit Schemaprüfung | `domaene` |
| `sitzung.py` | Fassade für die GUI. Hält Warteschlange, Steuerung, Gerät (Simulator oder COM) und Betriebsart. Liefert `Zustandsbild` (gefrorene Dataclass) und eine Ereigniswarteschlange; Befehlsmethoden | alles außer `gui` |
| `gui/…` | Technologieabhängig, dünn (Abschnitt 2.5) | nur `sitzung`, `domaene` |
| `__main__.py` | Einstieg `python -m ldv_automation [gui\|selbsttest] [--simulator\|--psv] [--betriebsart …] [--start-psv]` | `sitzung`, `gui` |

**Abhängigkeitsrichtung:**
`gui → sitzung → ablauf → (domaene, geraet.schnittstelle, protokoll, persistenz)`
`geraet.simulator / geraet.com → geraet.schnittstelle → domaene`

Nichts zeigt zurück. Ein Test prüft das per `ast`: Er durchsucht die Importe und stellt sicher, dass pywin32 nur in `pywin32_bindung.py` vorkommt und dass `domaene` nichts aus `ablauf` oder `geraet` importiert. Dafür ist keine neue Abhängigkeit nötig.

**Erkundungswerkzeug:** Das Hauptpaket **baut den Proxy neu auf** und importiert ihn nicht. Grund: `tools/erkundung/erkundung.py` ist ein Einzeldatei-Skript mit modulweiter `POLICY`, kein Paket, und das Werkzeug darf nicht aus dem Hauptpaket importieren. Die Gegenrichtung wäre eine Kopplung an ein Werkzeug. Übernommen werden die Konzepte:
- `Member`, Default deny, Prüffunktionen
- Protokoll der Aufrufe und Verweigerungen
- `pending` als Erkennung blockierender Aufrufe
- Sperre `GetApplication(True)` nur mit `--start-psv`
- Prozessprüfung vor dem `Dispatch`

Der Fake-PSV wird als Vorlage für einen COM-Fake in `tests/geraet/com/` genutzt (Kopie, kein Import). Das Werkzeug bleibt unverändert. Die Doppelung ist bewusst und steht als ADR-06 zur Entscheidung.

### 2 Zustandsmodell, Nebenläufigkeit, Regeln

**2.1 Eintrag Messung:**
- `WARTEND → LAEUFT → FERTIG | FEHLER | ABGEBROCHEN`
- `FEHLER → WARTEND` nur über die Fehlerentscheidung „Wiederholen“. Dabei steigt der Versuchszähler, und es gibt eine neue Zieldatei mit Suffix `_v2`. Es wird nie überschrieben.
- `FEHLER` bleibt `FEHLER` bei „Überspringen“. Der Durchgang läuft dann weiter, und im Protokoll steht `uebersprungen_nach_fehler`.
- Bei Abbruch des Durchgangs bleiben nicht gestartete Einträge `WARTEND`. Im Durchgangsprotokoll stehen sie als „nicht gestartet“. So ist nach R-018 nachvollziehbar, was mit jeder Messung geschah, und sie können in einem neuen Durchgang laufen.
- Die Anzeige nach R-031 bildet ab: wartend, läuft, fertig, Fehler, abgebrochen.

**2.2 Eintrag Pausenpunkt** (R-017): `WARTEND → ERREICHT` (wartet auf Bestätigung) `→ ERLEDIGT`. Er lässt sich bearbeiten, verschieben und entfernen wie eine Messung.

**2.3 Durchgang** (Ablaufsteuerung):

| Zustand | Bedeutung | Übergänge |
|---|---|---|
| `BEREIT` | kein Lauf | Start → `LAEUFT` (im Messbetrieb nur nach Bestätigung, Abschnitt 6) |
| `LAEUFT` | Messung aktiv oder Übergang zur nächsten | Pause → `PAUSE_ANGEFORDERT`; Abbrechen → `ABBRUCH_LAEUFT`; Pausenpunkt erreicht → `WARTET_AUF_BESTAETIGUNG`; Fehler → `WARTET_AUF_ENTSCHEIDUNG`; keine wartenden Einträge mehr → `BEENDET` |
| `PAUSE_ANGEFORDERT` | laufende Messung läuft zu Ende, danach startet keine neue (R-018) | → `PAUSIERT` |
| `PAUSIERT` | – | Fortsetzen → `LAEUFT`; Abbrechen → `BEENDET (abgebrochen)` |
| `WARTET_AUF_BESTAETIGUNG` | Pausenpunkt | Bestätigen → `LAEUFT`; Abbrechen → `BEENDET` |
| `WARTET_AUF_ENTSCHEIDUNG` | **vorläufiges** Fehlerverhalten | Wiederholen, Überspringen → `LAEUFT`; Abbrechen → `BEENDET` |
| `ABBRUCH_LAEUFT` | `Stop()` der eigenen Messung, Polling bis `Stopped` | → `BEENDET (abgebrochen)` oder `GERAET_UNKLAR` |
| `GERAET_UNKLAR` | `Stop` greift nicht in der Frist, oder ein COM-Aufruf hängt | keine weiteren COM-Schreibzugriffe; Hinweis an den Nutzer, PSV zu prüfen; nur „Verbindung trennen“ möglich |
| `BEENDET` | vollständig oder abgebrochen | → `BEREIT` |

**2.4 Bearbeitung während des Laufs (R-016):**
- Die GUI ändert die Warteschlange direkt über die Sitzung. Alle Änderungen laufen unter der Sperre der Warteschlange und sind nur für `WARTEND` erlaubt. Sonst kommt `ValueError` mit Grund.
- Die Steuerung beansprucht den nächsten Eintrag atomar über `naechsten_beanspruchen()` (`WARTEND → LAEUFT` unter der Sperre). Änderungen bis zu diesem Moment wirken also im selben Durchgang. Der laufende Eintrag ist unveränderlich.
- Die Steuerung arbeitet mit einer eingefrorenen Kopie der Messdefinition (gefrorene Dataclass). Spätere Bearbeitungen können die laufende Messung deshalb nicht beeinflussen.
- Ein Pausenpunkt vor dem nächsten Eintrag greift, sobald er beim nächsten Beanspruchen an erster wartender Stelle steht.

**2.5 Nebenläufigkeit:**
- Genau **ein Geräte-Thread**. Er ruft `CoInitialize` auf, legt alle COM-Objekte an und besitzt sie (STA, I5 5.5), und die Arbeitsschleife der Ablaufsteuerung läuft in ihm. Es gibt kein Marshalling zwischen Threads.
- Befehle (Pause, Abbrechen, Bestätigen, Fehlerentscheidung, Trennen) gehen über eine thread-sichere Befehlswarteschlange. Die Arbeitsschleife fragt sie in jedem Polling-Takt ab.
- Ausgaben: Die Sitzung baut nach jeder Änderung ein neues `Zustandsbild` und legt Ereignisse in eine `queue.Queue`. Die GUI holt beides **im GUI-Thread** ab und ruft nie selbst in den Geräte-Thread.
- Hängt ein COM-Aufruf länger als `aufruf_warnung_s`, erkennt ein Wächter-Thread das über `pending` des Proxys und meldet „PSV reagiert nicht seit … s“. Die GUI bleibt bedienbar. Die Grenze ist eine Annahme und am Montag einzustellen.

**Was je nach GUI-Wahl anders wäre** (der Kern bleibt gleich):

| GUI | Anbindung an Zustandsbild und Ereignisse | Besonderheit |
|---|---|---|
| Qt/PySide6 | Ein `QTimer` holt ab, oder ein Bridge-Objekt setzt Ereignisse in Signale mit QueuedConnection um | Zusatzpaket auf dem Messrechner; GUI-Tests mit pytest-qt wären eine neue Abhängigkeit |
| Tkinter | Abholen per `after(100 ms)`; Tk ist nicht thread-sicher, deshalb ausschließlich Abholen | keine Zusatzinstallation (Tk gehört zum python.org-Installer) |
| Lokale Weboberfläche | Server-Thread liefert das Zustandsbild als JSON (Polling oder WebSocket); Befehle als POST | Zusatzpakete; Bindung nur an 127.0.0.1; Browser auf dem Messrechner nötig |

**Wichtig für die GUI-Entscheidung:** Freigegeben ist am Messrechner „Python 3.11 + pywin32“. Jedes weitere Paket (PySide6, Web-Framework, ggf. uv) ist davon nicht ausdrücklich gedeckt. Ob der Messrechner Internet hat, ist offen (O2), sodass Pakete eventuell als Wheels per USB mitgebracht werden müssten.

**2.6 Fehlerverhalten (R-019, vorläufig):** Die `Fehlerstrategie` bekommt ein `FehlerEreignis` (Art, Text, Eintrag, ob die Messung gestartet wurde) und liefert eine Entscheidung.

Die einzige Umsetzung `PausierenUndNachfragen` liefert immer „anhalten und fragen“. Die GUI bietet dann Wiederholen, Überspringen oder Durchgang abbrechen an. Strategie und Text sind als „vorläufig, Klärung O1/F20 mit dem Betreuer“ gekennzeichnet: im Code-Docstring, in der GUI-Statuszeile und im Protokollfeld `fehlerstrategie`.

Eine spätere Strategie (überspringen, abbrechen, einstellbar) ist eine neue Klasse. Die Steuerung ändert sich dafür nicht. Ein Test mit einer Test-Strategie belegt die Austauschbarkeit.

Fehlerarten:
- Vorprüfung gescheitert: Zieldatei existiert, Einstellungsdatei fehlt, Parameter ungültig
- Gerät nicht bereit: `State ≠ Stopped`, also eine fremde Messung
- COM-Ausnahme
- Abweichung beim Zurücklesen (eingerasteter Wert ≠ Soll)
- Zeitlimit überschritten: dann `Stop()` und `FEHLER`
- Zieldatei fehlt nach dem Scan
- `GERAET_UNKLAR`

**2.7 Abbrechen (R-018, O1 offen):** Vorläufig gilt: „Abbrechen“ stoppt die laufende **eigene** Messung sofort mit `Stop()`, nach einer Sicherheitsabfrage in der GUI. Status `ABGEBROCHEN`. Die Datei bleibt erhalten, weil gemessene Punkte laut [HB] 8-3/10-8 bleiben. „Pausieren“ ist die sanfte Variante: Die laufende Messung endet regulär. Die Abbrechen-Variante wird als offene Frage geführt.

### 3 Ablauf einer Messung über COM (Adapter), mit Belegen

| Schritt | Aktion | Beleg (I5) | Absicherung |
|---|---|---|---|
| V0 | Verbinden: Prozessprüfung „PSV läuft“; erst dann `Dispatch("PSV.AcquisitionInstance")`, `IsRunning`, `GetApplication(False, …)`. `True` nur mit `--start-psv` und getipptem `JA` | 3.1; E1-Sperre; [BEM] ~GetApplication | verhindert, dass COM PSV ungewollt startet (`LocalServer32`) |
| V1 | `Version`, `Mode == Acquisition`, `SuppressMessagesForAutomation == True`, `Acquisition.State == Stopped`, Hardware lesen | 3.1 Schritte 4–8 | Ist `Suppress` False, wird der Messbetrieb gesperrt mit Hinweis „in PSV aktivieren“. Kein Schreiben dieser Einstellung |
| M1 | Vorprüfung ohne COM: Einstellungsdatei existiert und hat die Endung `.set`; Zielpfad liegt unter dem Messdaten-Wurzelordner und **existiert nicht**; Parameter liegen im Katalogbereich | 3.4 Schritt 1; KONVENTIONEN | Fehler vor jeder Gerätewirkung |
| M2 | `State == Stopped` erneut prüfen | 3.1 Schritt 7 | eine fremde Messung wird nie angefasst |
| M3 | `Settings.Load(pfad, maske)`; Maske konfigurierbar, siehe offene Frage 3 | 2.4; 3.2 Schritt 1; [BEM] PSV~Settings~Load | Teil-Laden wird ohne Events nicht gemeldet ([HB] 10-4), deshalb M5 |
| M4 | Parameter: `ActiveProperties.HasFftProperties` prüfen; Validator lesen; `Bandwidth` und `Lines` setzen; per Zuweisung an `FftAcqPropertiesValidator` atomar übernehmen. Mittelung über `AverageProperties.Type/Count`. Gibt es den Validator nicht, nach ADR-04 direkt über `FftProperties.Bandwidth/Lines` | 2.5, 2.6, 3.2 Schritte 3–6 | Exception bei ungültiger Kombination wird zu `GeraeteFehler` mit `excepinfo` |
| M5 | **Zurücklesen** aller gesetzten Werte und des Modus (FFT erwartet). Soll ≠ Ist ist ein Fehler, bevor der Scan startet. Ganzzahlen exakt vergleichen; Doubles mit `math.isclose(rel_tol=1e-9, abs_tol=0.0)`, weil Doubles über COM als VT_R8 ohne Rundung übertragen werden und die Toleranz nur Darstellungsunterschiede abfängt (Einrastsprünge liegen um Größenordnungen darüber). Zusätzlich vollständigen `EinstellungsStand` lesen: FFT, Mittelung, Allgemein, Trigger, SE, Kanäle (aktiv, Referenz, Größe, Einheit, Kalibrierung), Generator **nur lesend** | 2.6 Folgerung; 3.2 Schritt 8 | R-020 „wie von PSV übernommen“ |
| M6 | Optional `Settings.Save(<durchgang>/<nn>_<name>.einstellungen.set)` als Nachweis, Zieldatei darf nicht existieren | 3.2 Schritt 9 | kann zur Not wegfallen (Abschnitt 8) |
| M7 | Messfreigabe prüfen (Abschnitt 6): Der Proxy verweigert `ScanEx` ohne gesetzte Freigabe | – | doppelte Sicherung, GUI und Proxy |
| M8 | `ScanFileName = zielpfad`, zurücklesen und vergleichen; danach `ScanEx(ptcScanAll, ptcScanCapsNone)` | 3.4 Schritte 2–3; [BEM] ~ScanFileName, ~ScanEx | nie leer (sonst Dialog); kein `AsynchronousScanEvent` |
| M9 | Polling von `State` im Takt `poll_s` (Vorschlag 0,5 s, zwischen den Polytec-Beispielen mit 0,1 s und 1 s, [COM] Folie 12); Befehle prüfen; Zeitlimit prüfen; Fortschritt (Abschnitt 5.3 bzw. ADR-03) | 3.4 Schritte 4–5; 3.5 | Zeitlimit: `Stop()` und Fehler |
| M10 | Abbruch oder Zeitlimit: `Stop()` **nur, wenn diese Sitzung den Scan gestartet hat** (Flag `eigene_messung_aktiv` im Proxy-Kontext), danach Polling bis `Stopped` mit Frist `stop_frist_s`, sonst `GERAET_UNKLAR` | 3.5; [BEM] ~Stop | keine fremde Messung stoppen |
| M11 | Ende: `State == Stopped`; Zieldatei existiert. SHA-256 versuchen; scheitert das (Datei evtl. von PSV gesperrt, P1-9), steht im Protokoll „Hash nicht verfügbar: Grund“, und das ist kein Fehler | 3.4; 5.5 | – |
| M12 | Messprotokoll schreiben, **immer**, auch bei Fehler und Abbruch | R-020 | Datei neu anlegen (Modus „x“) |

**Meldungen (`SuppressMessagesForAutomation`, `MessageOccurred`):** Mit Late Binding und Polling empfängt der Prototyp in der Grundausstattung **keine** Events. Er verlässt sich auf `Suppress == True` (Standard, nach [BEM] belegt). Die Meldungen speichert PSV in der Messdatei (`SummaryInfo.Subject`, [HB] 2-24); ausgewertet werden sie später mit PolyFile, nicht im Prototyp.

Optionaler Zusatz `--ereignisse` (darf zur Not wegfallen): `DispatchWithEvents` auf Application und Acquisition, `PumpWaitingMessages` im Polling-Takt.
- Der Handler protokolliert `MessageOccurred` und antwortet konservativ: Cancel, No oder Abort; nur reine OK-Meldungen mit Ok.
- Eine Meldung mit Fehlersymbol (ICONHAND) macht die Messung zu `FEHLER`.
- Fortschritt kommt dann aus `EndScanPoint`.

Das setzt Typinformation voraus, und pywin32 schreibt dabei einen `gen_py`-Cache. Deshalb ist es ADR-02/03/09 und nur ein Experiment für Montag.

Belegt ist nur, dass `pVal` die Antwort simuliert ([BEM] MessageOccurred). Ob pywin32 sie über den Rückgabewert weitergibt, ist [ungeprüft] (P2-2). Dass Abfragen „in jedem Fall“ angezeigt werden, ist bei Automation [offen] (P1-8).

**3.3 Produktiv-Richtlinie (Whitelist).**

*Lesend* (keine Wirkung auf das Gerät):

| Objekt | Freigegebene Mitglieder |
|---|---|
| `AcquisitionInstance` | `IsRunning`, `GetApplication(False, ms)` |
| `Application` | `Version`, `Mode`, `SuppressMessagesForAutomation`, `WarningLevel`, `Acquisition`, `Settings` |
| `Acquisition` | `State`, `Mode`, `ScanFileName`, `GeneratorsOn`, `ActiveProperties`, `Infos` |
| `ActiveProperties` | `Has…` sowie die Lese-Properties der Gruppen FFT, Mittelung, Allgemein, Trigger, SE, Kanäle und Generator (nur `Active`, `Amplitude`, Signalformtyp) |
| `Infos` | `Hardware` (Kennungen, Firmware), `MeasPoints.Count`, `Has…` |
| Validator | `AvailableBandwidths`, `AvailableLines` und Lesen der Sollfelder |

*Schreibend*, jede Operation mit Begründung, Argumentprüfung und einem Test:

| Nr. | Operation | Begründung | Prüfung im Proxy |
|---|---|---|---|
| S1 | `AcquisitionInstance.GetApplication(True, ms)` | PSV starten, nur auf ausdrücklichen Wunsch | nur mit `--start-psv` plus `JA` |
| S2 | `Settings.Load(pfad, maske)` | R-011: Messung beruht auf einer Einstellungsdatei | Pfad ist str, existiert, Endung `.set`; Maske aus der freigegebenen Menge (ohne `Windows`, ohne `Camera` bis zur Klärung) |
| S3 | Validator: `Bandwidth =`, `Lines =` (nur Staging); `FftProperties.FftAcqPropertiesValidator = v` | R-011, atomare Übernahme | Wertebereich aus dem Katalog; Typ float bzw. int |
| S4 | Rückfall `FftProperties.Bandwidth =`, `.Lines =` | nur, wenn kein Validator vorhanden ist (ADR-04) | wie S3; per Konfigurationsschalter |
| S5 | `AverageProperties.Type =`, `.Count =` | R-011 | Typ aus `PTCAverageType`; Count 3…10000 nach [BEM] (Untergrenze am Gerät offen) |
| S6 | `Acquisition.ScanFileName = pfad` | R-001; sonst fragt PSV per Dialog | Pfad liegt unter der Messdaten-Wurzel, existiert nicht, Endung `.svd` |
| S7 | `Acquisition.ScanEx(0, 0)` | R-001, Scan starten | nur `ptcScanAll`/`None`; Messfreigabe gesetzt; `State == Stopped` unmittelbar davor geprüft |
| S8 | `Acquisition.Stop()` | R-018 und Zeitlimit | nur bei `eigene_messung_aktiv` |
| S9 | `Settings.Save(pfad)` | Nachweis R-020 (optional) | Pfad im eigenen Durchgangsordner, existiert nicht |
| S10 | Antwort auf `MessageOccurred` | nur mit `--ereignisse` | Antwort aus der festen Tabelle |

*Nie freigegeben* (Testkatalog wie in E1):
- `Start`, `Scan` ohne `Ex`, andere Scanmodi
- `SetLaserOn`, `AutoFocusLaser`, `AssignFocusAutomatically`, `GeometryScan`, `SetSelectedMeasPoints`
- `GeneratorsOn =` und jede Zuweisung an Generatoren
- `Acquisition.Mode =`, `Application.*` setzen (`Mode`, `Suppress…`, `WarningLevel`)
- `Settings.Delete`, `Documents`, `Exporter`, `Quit`
- `PositionDevice`, `DigitalPorts`, `Alignment3D.Calculate`
- alles aus `ScanHeadControl.Write…`
- jede PolyFile-Schreiboperation

### 4 Formate und Ablage

**4.1 Warteschlangendatei** (R-021), JSON UTF-8, Endung `.warteschlange.json`:
- Kopf: `schema_version: 1`, `art: "ldv-warteschlange"`, `erstellt_utc`, `paket_version`, `git_hash`
- `eintraege[]`, Messung: `{art:"messung", id, name, einstellungsdatei, parameter:{schluessel: wert}, zeitlimit_s, notiz}`
- `eintraege[]`, Pausenpunkt: `{art:"pausenpunkt", id, text}`

Gespeichert werden nur Definitionen. Nach dem Laden sind alle Einträge `WARTEND`. Das erfüllt R-021: dieselben Messungen in derselben Reihenfolge mit denselben Einstellungen.

Beim Laden wird das Schema streng geprüft: Unbekannte Schlüssel und Werte außerhalb des Katalogs ergeben einen Fehler mit Pfadangabe. Fehlt eine Einstellungsdatei, gibt es eine Warnung statt eines Fehlers, weil die Datei auf einem anderen Rechner entstanden sein kann. Beim Speichern fragt die GUI vor dem Überschreiben einer vorhandenen Datei nach. Die Warteschlangendatei ist kein Rohdatum.

**4.2 Ablage (O5 offen, vorläufig und konfigurierbar):**
```
<messdaten_wurzel>/<JJJJ-MM-TT_HHMMSS>_<durchgangsname>/
    durchgang.ereignisse.jsonl         (nur Anhängen: Start, Zustandswechsel, Befehle, Fehler)
    durchgang.warteschlange.json       (Kopie der Warteschlange beim Start, neu angelegt)
    <nn>_<messungsname>[_v<k>].svd     (Rohdatum, von PSV geschrieben)
    <nn>_<messungsname>[_v<k>].protokoll.json
    <nn>_<messungsname>[_v<k>].einstellungen.set   (optional, M6)
```
- Der Durchgangsordner wird mit `exist_ok=False` angelegt; existiert er schon, wird `_2` angehängt.
- Eigene Dateien werden mit Modus `"x"` geschrieben. Das Ereignisprotokoll wird nur ergänzt, nie neu geschrieben.
- Die `.svd` legt nur PSV an; vorher ist geprüft, dass sie nicht existiert.
- Die Messdaten-Wurzel ist eine Einstellung pro Rechner und liegt **nicht** in Polytec-Verzeichnissen und nicht im Repository.
- Die Ergebnisse vom Montag kopiert der Nutzer nach `in_progress/versuche/2026-11-02_prototyp/`.

**4.3 Messprotokoll** (R-020, Felder nach I5 Abschnitt 6, Umfang Prototyp), `schema_version: 1`:
- **Zuordnung:** `messung_id`, `name`, `versuch`, `durchgang_id`, `position`, `messdatei` (absoluter Pfad), `messdatei_sha256` oder `messdatei_sha256_grund`
- **Status:** `status`, `fehler` (Art, Text, `hresult`, `excepinfo`), `fehlerstrategie: "PausierenUndNachfragen (vorläufig, O1)"`, `fehlerentscheidung`
- **Zeit:** `zeit_start` und `zeit_ende` (ISO 8601 mit Zone und UTC), `dauer_s`, `zeitlimit_s`
- **Versionen:** `paket_version`, `git_hash`, `git_dirty`; `psv_version` (`Application.Version`); `betriebsart`
- **Gerät:** Hardware-Kennungen aus `Infos.Hardware` (Frontend, Erfassungskarte, Firmware, Sensorkopf-Seriennummern, soweit gelesen); `messpunkte_anzahl`
- **Einstellungen:** `einstellungsdatei` (Pfad und SHA-256), `lademaske`
- **Geänderte Parameter:** `geaenderte_parameter[]` mit `{schluessel, einheit, soll, ist}`
- **Wie von PSV übernommen:** `einstellungen_ist` (FFT inkl. `StartFrequency`/`EndFrequency`, `SampleFrequency`, `SampleResolution`, `SampleTime`; Mittelung; Allgemein; Trigger inkl. `PhaseFromRef`; SE; Kanäle; Generator: aktiv, Amplitude, Signalformtyp)
- **Meldungen:** `meldungen[]` (nur mit `--ereignisse`, sonst der Hinweis „Meldungen nur in der Messdatei, SummaryInfo.Subject“)
- **Fortschritt:** `fortschritt_quelle` (Ereignisse oder Zeitschätzung)
- **Einschränkungen:** `einschraenkungen[]`, z. B. „Vollständigkeit des Scans im Prototyp nicht geprüft“

Einheiten stehen im Feldnamen (`_hz`, `_s`, `_v`). Die COM-Werte werden an der Adaptergrenze nach `float64` gewandelt.

**4.4 Git-Hash auf dem Messrechner:** Dort ist kein Git vorausgesetzt. `protokoll/version.py` liest:
1. `git rev-parse HEAD` und `git status --porcelain`, falls aus dem Repository gestartet, sonst
2. die generierte Datei `ldv_automation/_build_info.json`. Diese entsteht vor dem Wheel-Bau per Skript, ist per gitignore ausgenommen und enthält Hash und Dirty-Flag.

Ist der Hash unbekannt, ist der **Messbetrieb gesperrt** (KONVENTIONEN „Messdaten mit Git-Hash“). Simulator, Nur-Lesen und Trockenlauf bleiben erlaubt. Ob ein Dirty-Stand messen darf, ist offene Frage 5.

### 5 Simulator (`geraet/simulator.py`)

Er arbeitet auf der Ebene des `Protocol`, ist deterministisch und mit injizierbarer Uhr. Fehler kommen aus einem **Drehbuch** (Liste von Ereignissen je Messung bzw. Aufrufnummer). Zufall gibt es nur mit übergebenem Seed.

Was er nachbildet:
1. **Verbindung:** PSV läuft oder läuft nicht (Sperre); Version „10.x-SIM“; `Suppress` True oder False (Messbetrieb gesperrt); Erfassungsmodus ja oder nein.
2. **Zustände:** `Stopped → ScanAll → Stopped`; „fremde Messung läuft“ beim Start (`State ≠ Stopped`).
3. **Dauer:** Punkteanzahl × Punktdauer (konfigurierbar). Die Testuhr lässt die Zeit sprungweise laufen. Ein Schrittmodus hält den Scan an definierten Punkten an, damit sich R-016 deterministisch testen lässt.
4. **Punktreihenfolge nicht fortlaufend** (z. B. 3, 2, 1, 4, 5, 6, 9, 8, 7 nach [BEM] ScanStateChanged) für die Fortschrittslogik.
5. **Einrasten:** verfügbare Bandbreiten und Linien als Listen; gesetzte Werte rasten auf den nächsten gültigen Wert ein, und der zurückgelesene Wert weicht ab.
6. **Ungültige Werte** (z. B. Mittelung 2, laut [BEM] gültig 3…10000) lösen eine Ausnahme mit Meldungstext aus.
7. **Fehlender Validator** (Konfiguration), damit der Rückfall S4 testbar ist.
8. **`Settings.Load`:** unbekannte Datei gibt einen Fehler. Optional „Teil-Laden“: ein Parameter bleibt auf dem alten Wert, was das Zurücklesen erkennen muss.
9. **Scandatei:** Der Simulator legt am Zielpfad eine kleine Platzhalterdatei mit Kennung „SIMULATOR“ an, damit Existenzprüfung und Hash echt laufen. Ist die Datei schon vorhanden, gibt es einen Fehler, als Doppelsicherung zur Vorprüfung.
10. **Fehler im Drehbuch:** Ausnahme bei `starte_scan`; Scan endet vorzeitig (State `Stopped` nach k Punkten, wie das Verhalten nach drei Fehlversuchen in [HB] 2-23); Hänger (State wird nie `Stopped`, dann Zeitlimit); `Stop` wirkt nicht (dann `GERAET_UNKLAR`); hängender Aufruf (blockiert, für den Wächter); keine Datei nach dem Scan.
11. **Meldungen:** Meldung mit Stil und Text an Punkt k (für `--ereignisse` und die Fehlerlogik).
12. **Aufrufprotokoll** für Tests, z. B. „kein `starte_scan` ohne Freigabe“.

**5.3 Fortschritt (R-031):** Die Grundausstattung schätzt über die Zeit: Punkte × geschätzte Punktdauer. Die Punktdauer kommt aus der vorherigen Messung desselben Durchgangs, sonst aus der Konfiguration; die Anzeige ist als „geschätzt“ gekennzeichnet. Mit `--ereignisse` zählt sie `EndScanPoint` gegen `MeasPoints.Count`. Ein Experiment für Montag ist Polling des Punktstatus (`Infos.MeasPoints(i).ScanStatus` während des Scans, [ungeprüft]) als Schalter `--fortschritt punktstatus`, nur bei kleinen Gittern.

Daneben gibt es einen **COM-Fake nur in den Tests** (`tests/geraet/com/fake_psv_com.py`, Vorlage ist der Erkundungs-Fake). Gegen ihn laufen Adapter und Proxy ohne Windows. So ist die Adapterlogik voll abgedeckt; ausgenommen ist nur `pywin32_bindung.py`.

### 6 Sicherheitskonzept am Gerät

**Betriebsarten** (umschalten in GUI und CLI; Anzeige dauerhaft in der Statuszeile):

| Betriebsart | erlaubt | COM-Schreibzugriffe |
|---|---|---|
| `SIMULATOR` | alles gegen den Simulator | keine |
| `NUR_LESEN` | Verbinden, Version, Zustand, Hardware, Einstellungen lesen | keine (nur S1 mit `--start-psv`) |
| `TROCKENLAUF` | zusätzlich je Eintrag M1–M6 (Laden, Setzen, Zurücklesen, Protokoll mit Status `trockenlauf`) | S2–S5, S9; **kein** S6–S8 |
| `MESSEN` | voller Ablauf | S2–S9 |

Ein Trockenlauf ändert die aktuellen PSV-Einstellungen. Darauf weist die GUI vor dem Start hin. Spiegel, Laser und Generator bewegt er nicht: Er setzt keinen Scan ab, und die Generator-Zuweisungen sind gesperrt.

**Freischaltung von `MESSEN`** je Sitzung. Voraussetzungen:
- Verbindung steht, `State == Stopped`
- `Suppress == True`
- Git-Hash bekannt
- Messdaten-Wurzel gesetzt und beschreibbar
- ein Trockenlauf des ersten Eintrags ohne Abweichung in dieser Sitzung

**Bestätigung je Durchgang:** Ein Dialog zeigt die Zahl der Messungen, je Messung Einstellungsdatei und Zielpfad, Messpunkte, `GeneratorsOn` und Generator-Aktiv/Amplitude (gelesen). Er verlangt eine ausdrückliche Bestätigung, entweder durch Eintippen von `MESSEN` oder durch einen eigenen Knopf ohne Standardfokus. Erst danach setzt die Sitzung `messfreigabe` im Proxy-Kontext; ohne sie verweigert der Proxy `ScanEx`. Die Bestätigung gilt für den ganzen Durchgang, damit R-010 („läuft ohne Eingriff“) erfüllt bleibt. Nach Ende oder Abbruch erlischt die Freigabe.

**Für Montag:** Der erste echte Durchgang besteht aus **einer** Messung (Abschnitt 9, T4).

**Generator:** `ScanEx` startet einen in der `.set` aktiven Generator automatisch ([HB] 8-3). Der Prototyp setzt den Generator nie, zeigt aber den gelesenen Zustand im Bestätigungsdialog an und warnt rot, wenn er aktiv ist. Am Montag gilt: `.set` mit Generator aus, oder kein Shaker/Verstärker angeschlossen, oder ausdrückliche Freigabe durch den Betreuer.

**Was der Prototyp nie tut:**
- Laser schalten, Fokus, Geometrie-Scan, Abgleich, Positioniereinheit, Digitalports
- Service- oder Kalibriermethoden
- Generator ein/aus oder Signalform setzen
- `Acquisition.Mode` oder `Application`-Einstellungen ändern
- `Settings.Delete`; Speichern in Polytec-Verzeichnisse oder auf die Quell-`.set`
- PSV beenden; PSV ohne `--start-psv` starten
- eine fremde Messung stoppen
- eine Datei überschreiben
- PolyFile schreiben; Export
- DCOM über das Netz

### 7 ADRs zur Entscheidung durch den Nutzer

| ADR | Frage | Alternativen | Empfehlung | Begründung |
|---|---|---|---|---|
| 01 | COM-Bibliothek | pywin32 · comtypes · pythonnet (.NET-Interop) | **pywin32** | am Messrechner freigegeben (F4); von Polytec in den PFA-Python-Beispielen genannt ([PFA] Examples); das Erkundungswerkzeug nutzt pywin32, die Montagsergebnisse gelten also direkt; comtypes und pythonnet wären zusätzliche, nicht freigegebene Installationen |
| 02 | Binding | Late (`Dispatch`) · Early (makepy/`EnsureDispatch`) · Late plus eigene `IntEnum`, Early später | **Late plus eigene `IntEnum`** für den Prototyp | gleicher Weg wie die Erkundung, also am Montag direkt geprüft; kein `gen_py`-Schreibzugriff; der Prototyp braucht keine ByRef-Ausgaben und keine Casts (kein Exporter, kein `GetMinMaxFrequencyRange`); Konstanten im Simulator testbar und am Gerät gegen P1-4 abzugleichen. Nachteil: keine Events, entgegen Polytecs Empfehlung für Early ([BEM] Access to Interfaces) |
| 03 | Scanende und Fortschritt | Polling `State` · Events `ScanStateChanged`/`AcqStateChanged` · Polling fürs Ende plus Events nur für den Fortschritt | **Polling für das Ende** (belegt für externe Programme, [COM] Folie 12); Fortschritt über Zeitschätzung, Events als abschaltbares Experiment | Events aus Python sind ungeprüft (P2-1) und brauchen Typinformation (ADR-02) und eine Nachrichtenschleife; das Ende eines Scans darf nicht an Unbelegtem hängen |
| 04 | Parameter setzen | nur `.set` · `.set` plus Validator · `.set` plus direkte Properties · nur COM-Properties | **`.set` als Basis plus Validator**, Rückfall auf direkte Properties per Schalter, wenn P1-6 keinen Validator findet; immer zurücklesen | R-011 verlangt `.set` als Basis; Scanpunkte und Abgleich gehen praktisch nur per `.set` (I5 2.4); der Validator übernimmt atomar und rastet ein, deshalb ist Zurücklesen Pflicht (I5 2.6) |
| 05 | Datenweg für die spätere Auswertung (R-022, nicht im Prototyp) | `.svd` plus PolyFile nur lesend · UFF-Export per COM nach jeder Messung · Live `GetData` | **`.svd` als einziges Rohdatum, Lesen per PolyFile (`ReadOnly=True`)**; UFF nur als Gegenprobe bzw. Golden File | `.svd` enthält alles inkl. Status und Metadaten; UFF nur in einfacher Genauigkeit, ohne nicht gemessene Punkte, Cast nötig (I5 3.7); `GetData` nur als Momentaufnahme. Endgültig erst nach Erkundung 1b und der Datei vom Betreuer; bis dahin als ADR „vorläufig“ |
| 06 | Whitelist im Produktiv-Adapter | (a) eigener Proxy im Hauptpaket mit Default deny, Wertprüfung, Messfreigabe-Sperre · (b) nur Adaptermethoden als „Whitelist“, ohne Proxy · (c) Proxy des Werkzeugs importieren oder auslagern | **(a)** | (b) widerspricht KONVENTIONEN („jeder COM-Zugriff über Whitelist-Proxy“); (c) koppelt Hauptpaket und Werkzeug, die Richtlinie ist dort modulweit fest, und das Werkzeug darf nicht aus dem Hauptpaket importieren. Preis: das Konzept ist doppelt vorhanden |
| 07 | Nebenläufigkeit | ein COM-Geräte-Thread (STA) mit Steuerung · eigener Geräteprozess | **ein Geräte-Thread** | einfacher, ausreichend; COM-Objekte bleiben in ihrem Thread (I5 5.5); hängt ein COM-Aufruf, bleibt die GUI über den Wächter bedienbar. Ein Prozess wäre robuster gegen Hänger, kostet aber Interprozesskommunikation |
| 08 | Ebene des Simulators | Simulator auf `Protocol`-Ebene im Paket plus COM-Fake in den Tests · Simulator als nachgebautes COM-Objektmodell im Paket | **Protocol-Ebene plus COM-Fake in den Tests** | der Simulator bildet Verhalten ab statt Objektgraph und ist schneller zu bauen; der Adaptercode wird trotzdem über den Fake getestet. Nachteil: Der Simulator prüft nicht den Adapter selbst |
| 09 | Meldungen | nur `Suppress` plus Meldungen später aus der Datei · Events mit fester Antworttabelle · Events nur protokollieren | **nur `Suppress`** im Grundumfang; Events mit konservativer Antwort als Experiment `--ereignisse` | ByRef-Antwort ungeprüft (P2-2); Risiko blockierender Abfragen bleibt (P1-8) und wird am Montag gezielt geprüft |
| 10 | Ablage und Formate (O5) | Durchgangsordner mit JSON-Protokoll je Messung plus Ereignis-JSONL · eine gemeinsame Protokolldatei je Durchgang · HDF5 o. ä. | **Durchgangsordner, JSON je Messung, JSONL nur zum Anhängen** | stdlib, lesbar, eindeutig einer `.svd` zuzuordnen; kein Überschreiben nötig. Vorläufig, bis O5 geklärt ist |
| 11 | Git-Hash auf dem Messrechner | Build-Info-Datei beim Wheel-Bau · Git auf dem Messrechner voraussetzen · nur SHA-256 der Dateien | **Build-Info-Datei** (Rückfall: Git, falls vorhanden) | Git auf dem Messrechner ist nicht freigegeben; KONVENTIONEN verlangen den Git-Hash |

Dazu kommt die ADR zur GUI-Technologie aus dem parallelen Paket. Sie wird hier nur referenziert.

### 8 Arbeitspakete bis Fr 2026-10-30

Für alle Pakete gilt die Standard-Prüfung aus KONVENTIONEN (`ruff check`, `ruff format --check`, `mypy --strict`, `pytest --cov --cov-fail-under=90`).

| Paket | Inhalt | Abhängigkeit | Zeitfenster | Bezug |
|---|---|---|---|---|
| **U1 Kern-Domäne** | `domaene/*`, `geraet/schnittstelle.py` (Protocol und Datentypen, danach fest), `persistenz/warteschlangendatei.py`, Import-Richtungstest | Freigabe dieses Plans | Di nachmittags bis Mi früh | R-011–R-015, R-021 |
| **U2 Ablauf und Simulator** | `ablauf/*`, `geraet/simulator.py`, `protokoll/*`, `sitzung.py` | U1 | Mi bis Do | R-010, R-016–R-020, R-031 (Kern), R-061 |
| **U3 COM-Adapter** | `geraet/com/*`, COM-Fake in den Tests, Prüfanleitung für Montag (Ablauf G) | U1 (Protocol); parallel zu U2, da getrennte Dateien | Mi bis Do | R-001, KONVENTIONEN Hardware/Polytec |
| **U4 GUI** | `gui/*`, `__main__.py`, pytest-Marker `gui` in `pyproject.toml` | GUI-ADR, freigegebener Brief (Mi), U2-Sitzung | Do bis Fr | R-030, R-031 |
| U5 Integration | Selbsttest `python -m ldv_automation selbsttest` (Simulator-Durchgang ohne GUI), Build-Info-Skript, Abgleich der Schnittstellen U2/U3 | U2, U3, U4 | Fr | R-060, R-062 |

Danach folgen Review und Design-Abnahme (Sa) sowie das Montagspaket mit Installationsanleitung (P6, nicht Teil dieses Plans).

**Prüfbare Akzeptanzkriterien:**

U1:
- U1-1: `Warteschlange.einfuegen(pos, e)` setzt `e` an Index `pos`; `pos` außerhalb von 0…len wirft `IndexError`.
- U1-2: Entfernen, Bearbeiten und Verschieben eines Eintrags in `LAEUFT`, `FERTIG`, `FEHLER` oder `ABGEBROCHEN` wirft `ValueError`, und die Warteschlange bleibt unverändert.
- U1-3: Ein Parameterwert außerhalb des Katalogbereichs, z. B. `mittelung.anzahl = 2`, wirft beim Anlegen `ValueError` mit Schlüssel und Bereich.
- U1-4: Speichern und Laden ergibt gleiche Einträge (IDs, Reihenfolge, Parameter, Pausenpunkte); alle geladenen Einträge sind `WARTEND`.
- U1-5: Eine Datei mit unbekanntem Schlüssel oder falscher `schema_version` wirft `ValueError` mit JSON-Pfad.
- U1-6: Der Importtest schlägt fehl, wenn `domaene` aus `ablauf` oder `geraet` importiert oder pywin32 außerhalb von `pywin32_bindung.py` vorkommt.

U2 (alle gegen Simulator und Testuhr):
- U2-1: Eine Warteschlange mit drei Messungen läuft durch; drei Platzhalter-`.svd` und drei Protokolle entstehen; Durchgang `BEENDET (vollständig)` (R-010).
- U2-2: Im Schrittmodus während Messung 1: Messung 2 bearbeiten und Messung 4 einfügen. Messung 2 läuft mit den neuen Werten, Messung 4 im selben Durchgang; das Protokoll von Messung 1 zeigt die ursprünglichen Werte (R-016).
- U2-3: Ein Pausenpunkt zwischen Messung 1 und 2 lässt Messung 2 ohne `bestaetigen()` nicht starten, auch nicht nach simulierten 3600 s; nach `bestaetigen()` startet sie (R-017).
- U2-4: Pause während Messung 1: Messung 1 endet `FERTIG`, Messung 2 bleibt `WARTEND`, bis fortgesetzt wird. Abbrechen während Messung 1: `stoppe()` wird genau einmal aufgerufen, Messung 1 `ABGEBROCHEN`, die übrigen `WARTEND`, das Ereignisprotokoll nennt jeden Eintrag (R-018).
- U2-5: Ein Simulator-Fehler aus dem Drehbuch führt zu `WARTET_AUF_ENTSCHEIDUNG`. „Wiederholen“ erzeugt die Zieldatei `_v2`, die erste Datei bleibt unverändert (Hash gleich); „Überspringen“ setzt den Durchgang fort; „Abbrechen“ beendet ihn. Protokollfeld `fehlerstrategie` enthält „vorläufig“ (R-019 vorläufig).
- U2-6: Eine Test-Fehlerstrategie „immer überspringen“ lässt sich ohne Änderung an `steuerung.py` einsetzen, und der Durchgang läuft ohne Halt durch.
- U2-7: Eingerasteter Wert (Soll 5000 Hz, Ist 6250 Hz im Simulator): Messung `FEHLER` vor `starte_scan`; das Simulatorprotokoll enthält keinen `starte_scan`.
- U2-8: Existiert die Zieldatei schon, ist die Messung `FEHLER` in der Vorprüfung, die Datei bleibt unverändert, und das Gerät erhält keinen Aufruf.
- U2-9: Der Hänger aus dem Drehbuch führt nach Ablauf von `zeitlimit_s` (Testuhr) zu `stoppe()` und `FEHLER`; wirkt `Stop` nicht, zu `GERAET_UNKLAR` ohne weitere Schreibaufrufe.
- U2-10: Jedes Protokoll enthält alle Pflichtfelder aus 4.3 (Schema-Test), auch bei `FEHLER` und `ABGEBROCHEN`; `git_hash` ist gesetzt bzw. die Begründung, warum nicht.
- U2-11: Ohne Git-Hash wirft das Umschalten auf `MESSEN` `ValueError` mit Grund; `SIMULATOR` und `TROCKENLAUF` funktionieren.
- U2-12: Das Zustandsbild ändert sich nach jedem Zustandswechsel, und die Ereigniswarteschlange liefert die Wechsel in Reihenfolge (R-031, Kernteil).

U3 (gegen den COM-Fake):
- U3-1: Jeder Eintrag des „Nie“-Katalogs (3.3) wird verweigert (`PermissionError` „Default deny“) und protokolliert; je Eintrag ein Test.
- U3-2: Ein vollständiger Messablauf erzeugt genau die Aufruffolge V0–M12; das Aufrufprotokoll enthält nur Richtlinien-Einträge und keine Verweigerung.
- U3-3: `ScanEx` ohne Messfreigabe, `Stop` ohne eigene Messung und `ScanFileName` mit vorhandenem Pfad oder außerhalb der Wurzel werden verweigert.
- U3-4: `GetApplication(True, …)` ohne `--start-psv` wird verweigert. Meldet die Prozessprüfung „kein PSV“, gibt es keinen `Dispatch` von `PSV.AcquisitionInstance`.
- U3-5: Ohne Validator (Fake-Variante) nutzt der Adapter S4 nur bei gesetztem Schalter, sonst `GeraeteFehler` „Validator fehlt“.
- U3-6: Eine COM-Ausnahme mit `hresult` und `excepinfo` wird zu `GeraeteFehler` mit Methode, Argumenten und Text.
- U3-7: `pywin32_bindung.py` ist die einzige ausgenommene Datei, jede Ausnahme hat eine Begründung; Adapter und Proxy ≥ 90 % Abdeckung.
- U3-8: Die Prüfanleitung für Montag liegt vor (Abschnitt 9, mit Abbruchkriterien).

U4:
- U4-1: Alle Funktionen R-010 bis R-018 und R-021 sind über die GUI bedienbar, ohne Kommandozeile (R-030); geprüft per Handtest-Checkliste im Simulatorbetrieb, dazu Smoke-Tests mit Marker `gui`.
- U4-2: Status je Eintrag und Fortschritt (mit „geschätzt“-Kennzeichnung) werden angezeigt (R-031).
- U4-3: Betriebsart ist dauerhaft sichtbar; `MESSEN` nur über den Bestätigungsdialog.
- U4-4: Die GUI blockiert nicht, während der Simulator einen hängenden Aufruf simuliert; der Hinweis des Wächters erscheint.
- U4-5: Alle Zustände nach Brief (leer, läuft, Pause, Fehler) sind umgesetzt.

U5:
- U5-1: `python -m ldv_automation selbsttest` läuft unter Linux und Windows ohne pywin32 erfolgreich durch.
- U5-2: Das Build-Info-Skript erzeugt `_build_info.json` mit Hash und Dirty-Flag, und das Wheel enthält die Datei.
- U5-3: Die Standard-Prüfung ist grün.

**Teststrategie:**
- Domänen-Unit-Tests ohne Threads.
- Ablauftests über Simulator, Testuhr und Schrittmodus. Damit sind Nebenläufigkeitsfälle deterministisch, ohne `sleep`. Ein echter Thread-Test prüft Start, Stopp und Join ohne Verklemmung, mit Zeitlimit.
- Proxy- und Adaptertests gegen den COM-Fake mit Abgleich des Aufrufprotokolls.
- Schema-Tests für beide JSON-Formate.
- GUI-Smoke-Tests mit eigenem Marker, standardmäßig nicht ausgeführt.
- Hardware-Tests mit Marker `hardware` sind nicht geplant; dafür gibt es die Prüfanleitung (wie bei E1).
- Keine neue Abhängigkeit außer der GUI-Bibliothek nach ADR. `hypothesis` wäre neu und ist nicht vorgesehen.

**Wenn die Zeit nicht reicht, entfällt in dieser Reihenfolge:**
1. `--ereignisse` und `--fortschritt punktstatus` (Experimente)
2. Einstellungs-Schnappschuss M6
3. Speichern/Laden der Warteschlange (R-021 ist „Soll“)
4. Bedienkomfort der GUI (Drag-and-drop wird zu Knöpfen „hoch/runter“, Bearbeiten-Dialog vereinfacht)
5. Trockenlauf als eigene Betriebsart (dann `NUR_LESEN` plus Messung einzeln)

**Nie streichen:** Whitelist und Messfreigabe, Schutz vor Überschreiben, Messprotokoll, Simulator mit Tests, Kennzeichnung „vorläufig“.

**Kritischer Pfad:** U2 (Zustandsmaschine mit R-016) und die GUI-Entscheidung. Kommt der Brief erst am Donnerstag, reicht für U4 nur eine schlichte Oberfläche.

### 9 Plan für den Test am Montag

**Reihenfolge:** erst lesen, dann schreiben ohne Wirkung auf Hardware, zuletzt messen.

| Schritt | Inhalt | Weiter, wenn | Abbruch bzw. Rückfall |
|---|---|---|---|
| E0 | Python 3.11 und pywin32 installieren, Erkundung Stufe 0 (E1-Anleitung) | pywin32 importierbar, ProgIDs registriert | ohne pywin32: Prototyp nur im Simulator vorführen |
| E1 | Erkundung Stufe 1 | Verbinden mit Late Binding klappt; `Mode`, `State`, Version gelesen; **Validator vorhanden?**; `Suppress == True`; Konstanten passen zu I5 §8 | Verbindung scheitert: kein COM-Test des Prototyps, nur Simulator und Befunde sichern |
| E1b | Erkundung Stufe 1b mit der Betreuerdatei | – | nicht blockierend für den Prototyp |
| T0 | Prototyp installieren (Wheel mit Build-Info); `selbsttest`; GUI im Simulatorbetrieb starten | Selbsttest grün, GUI bedienbar | GUI-Fehler: nur CLI bzw. Selbsttest, Befund aufnehmen |
| T1 | Betriebsart `NUR_LESEN` | GUI zeigt Version, Zustand und Hardware wie Erkundung Stufe 1; Aufrufprotokoll ohne Verweigerung | Abweichung oder Verweigerung: stoppen, Protokoll sichern |
| T2 | Rückfall-Schalter nach E1 setzen (Validator ja/nein); `TROCKENLAUF` mit einer vom Nutzer in PSV vorbereiteten kleinen `.set` (z. B. 3×3 Punkte, Generator aus) und einem geänderten Parameter | Ist-Werte stimmen mit der PSV-Oberfläche überein; Einrasten wird erkannt (bewusst eine einrastende Bandbreite eintragen); kein Laser- oder Spiegelvorgang; kein Dialog | unerwarteter Dialog, Laser- oder Spiegelbewegung, Abweichung zur PSV-Anzeige: abbrechen, melden |
| T3 | Optional, nur mit Nutzer am Gerät: Meldungsprobe (I5 P1-8). Zieldatei existiert: wird von unserer Vorprüfung abgefangen, PSV erhält keinen Aufruf | Vorprüfung greift | – |
| T4 | **Erste echte Messung:** `MESSEN` freischalten, Durchgang mit **einer** Messung, Bestätigungsdialog vom Nutzer lesen und bestätigen lassen (Generator-Anzeige prüfen) | Messung `FERTIG`; `.svd` am Zielpfad; Protokoll vollständig; Dauer notieren (für Zeitlimit und Punktdauer) | `State` wird nicht `Stopped` innerhalb des Zeitlimits, Dialog, Fehlermeldung: Abbrechen (eigener `Stop`), Befund sichern, keine weiteren Messungen |
| T5 | Abbrechen: Messung starten, nach wenigen Punkten „Abbrechen“ | `ABGEBROCHEN`, `State == Stopped`, Datei mit Teilpunkten vorhanden | `GERAET_UNKLAR`: Nutzer prüft PSV manuell, Ende der Messtests |
| T6 | Warteschlange mit drei Messungen und einem Pausenpunkt, Bearbeiten während des Laufs (R-010, R-016, R-017); Zeitlimit bewusst knapp für eine Messung (Fehlerpfad, R-019 vorläufig) | alles nach Akzeptanzkriterien U2 am Gerät beobachtbar | wie T4 |
| T7 | Optional: `--ereignisse`, `--fortschritt punktstatus`; Warteschlange speichern und laden | Befund P2-1/P2-2 | jede Unregelmäßigkeit: Experiment beenden |

Am Ende werden der Erkundungsordner, die Durchgangsordner (`.svd`, Protokolle, Ereignis-JSONL) und Notizen nach `in_progress/versuche/2026-11-02_…` kopiert. Danach folgt `/laborbuch`. Ein Hardwaretest gilt erst nach Bestätigung durch den Nutzer als bestanden.

**Allgemeine Abbruchkriterien:**
- unerwarteter Dialog in PSV
- Laser oder Spiegel bewegt sich außerhalb von T4–T6
- Einträge unter „verweigert“
- GUI oder PSV reagiert nicht länger als die Wächtergrenze
- eine vorhandene Datei wurde verändert
- Generator gibt unerwartet aus

**Empfehlung:** Für die Testmessung (Prüfling, `.set` mit 3×3 Punkten, Generator- und Shakerzustand) vorab einen Mini-Versuchsplan über `/versuchsplanung` erstellen.

### 10 Risiken und offene Fragen

**Risiken** (Woran merke ich es? Gegenmaßnahme):
1. **Late Binding oder pywin32 verhält sich anders als angenommen** (Properties-Zugriff, Validator-Zuweisung, `None` bei typisierten Collections). Erkennbar an E1 und T1/T2. Gegenmaßnahme: Erkundung zuerst, Schalter S4, ausführliche `excepinfo` im Protokoll. Behoben wird erst nach dem Montag.
2. **Blockierende PSV-Dialoge trotz `Suppress`** (I5 5.1 [offen]). Erkennbar am Wächter-Hinweis. Gegenmaßnahme: Nutzer am Gerät, `GERAET_UNKLAR`. Eine Automatik gibt es nicht.
3. **Teil-Laden der `.set` bleibt unbemerkt** (ohne Events). Nur die Katalogparameter und der Modus werden zurückgelesen; andere Teile (Kanäle, Abgleich) sind nur protokolliert, nicht geprüft.
4. **Vorzeitig beendeter Scan** (drei Fehlversuche, [HB] 2-23) gilt im Prototyp als `FERTIG`, wenn die Datei existiert. Die Vollständigkeit wird erst mit PolyFile oder Events prüfbar. Das steht im Protokoll unter `einschraenkungen`.
5. **Zeitplan:** U2, U3 und U4 in drei Tagen ist knapp; abhängig von GUI-ADR und Brief bis Mittwoch. Gegenmaßnahme: Streichreihenfolge aus Abschnitt 8.
6. **Installation am Messrechner:** Zusatzpakete (GUI-Bibliothek, uv) sind nicht ausdrücklich freigegeben; Internetzugang unklar.
7. **Bitness:** Für den Prototyp ist sie unkritisch, da PSV ein Out-of-Process-Server ist [Einschätzung]. Erst später für PFA relevant (P1-2).
8. **Ungeplante Benutzeraktionen in der PSV-GUI** während des Durchgangs (I5 9 [offen]). `State` wird vor jedem Start geprüft; mehr Schutz gibt es nicht.

**Rückfragen:**
- [blockierend für U1–U3] **Entscheidung über ADR-01 bis ADR-11.** Die Empfehlungen stehen in Abschnitt 7. — *Auswirkung:* Struktur von Adapter, Simulator und Ablauf.
- [blockierend für U4] **GUI-Technologie** (paralleles Paket), einschließlich der Frage, ob das gewählte Paket auf dem Messrechner installiert werden darf. — *Auswirkung:* nur `gui/` und Installationsanleitung.
- [nicht blockierend] O1/R-018: Darf „Abbrechen“ die laufende Messung sofort stoppen (`Stop`, Datei mit Teilpunkten bleibt)? — *Annahme bis zur Klärung:* ja, nach Sicherheitsabfrage; „Pausieren“ ist die sanfte Variante.
- [nicht blockierend] Optionen bei Fehler im vorläufigen „pausieren und nachfragen“: Wiederholen, Überspringen, Abbrechen? — *Annahme:* diese drei.
- [nicht blockierend] O3: änderbare Parameter im Prototyp. — *Annahme:* `fft.bandbreite_hz`, `fft.linien`, `mittelung.anzahl`, `mittelung.typ`, über den Katalog erweiterbar. Von/Bis und Generator sind nicht enthalten, Generator bewusst aus Sicherheitsgründen.
- [nicht blockierend] Lademaske für `Settings.Load`. — *Annahme:* Acquisition, APS, Alignment, 2D und 3D-Abgleich; ohne Camera und Windows, weil Camera Optik (Zoom/Fokus) bewegen könnte [Einschätzung]. Am Montag in T2 prüfen und konfigurierbar.
- [nicht blockierend] Darf ein Stand mit `git_dirty = true` echt messen? — *Annahme:* ja, mit Warnung und Kennzeichnung im Protokoll; ohne Hash nicht.
- [nicht blockierend] Standardwert des Zeitlimits je Messung. — *Annahme:* globale Einstellung `zeitlimit_s`, Startwert 600 s (willkürlich, nicht belegt); nach T4 aus der gemessenen Dauer neu setzen. Je Messung überschreibbar.
- [nicht blockierend, wichtig für Montag] Wer bereitet die kleine Test-`.set` (z. B. 3×3 Punkte, Generator aus) und den Prüfling vor, und ist für T4 eine Anregung nötig bzw. erlaubt? — *Auswirkung:* T2–T6.
- [nicht blockierend] Ablageort der Messdaten auf dem Messrechner (O5). — *Annahme:* frei wählbar in der Konfiguration, außerhalb von Polytec-Verzeichnissen.

---

## Rückmeldung an den Orchestrator

**Paket:** P2 · **Status:** PLAN ZUR FREIGABE

**Ergebnis:** Der Plan oben (Abschnitte 1–10). Im Repository wurde nichts geändert und keine Datei angelegt.

**Wie verifiziert:** Ich habe die maßgeblichen Unterlagen gelesen. Die zentralen COM-Belege habe ich in der CHM-Textfassung nachgeschlagen: `ScanEx` (Parameter, Asynchron-Flag), `ScanFileName` (leer heißt Dialog), `Stop`, `State` (read-only), `SuppressMessagesForAutomation` (Standard true), `MessageOccurred` (pVal), `Settings.Load` (`.set` oder Messdatei). Alle übrigen Aussagen stammen aus I5 mit dessen Kennzeichnung. Code wurde weder ausgeführt noch geschrieben (Planungspaket).

**Akzeptanzkriterien des Pakets:**
- Abschnitt 1 Modulstruktur: erfüllt
- Abschnitt 2 Zustände, Nebenläufigkeit, R-016/R-018, vorläufiges Fehlerverhalten: erfüllt
- Abschnitt 3 Ablauf mit Belegen und begründeter Whitelist: erfüllt
- Abschnitt 4 Formate und Ablage: erfüllt
- Abschnitt 5 Simulator: erfüllt
- Abschnitt 6 Sicherheitskonzept: erfüllt
- Abschnitt 7 ADRs: erfüllt (11 Stück plus GUI-ADR)
- Abschnitt 8 Pakete mit Akzeptanzkriterien und Streichliste: erfüllt
- Abschnitt 9 Montagsplan: erfüllt
- Abschnitt 10 Risiken und Fragen: erfüllt

**Annahmen:** siehe die nicht blockierenden Rückfragen in Abschnitt 10. Weitere:
- Der Prototyp nutzt kein PolyFile (R-022 nicht im Umfang).
- Polling-Takt 0,5 s.
- Toleranz beim Zurücklesen von Doubles `rel_tol=1e-9`, begründet in M5.

**Sichtbare Verhaltensänderungen und Risiken:**
- Das Werkzeug `tools/erkundung` bleibt unverändert.
- `pyproject.toml` bekommt in U4 einen Marker `gui` und je nach GUI-ADR eine neue Abhängigkeit.
- Hauptrisiken: Der Prototyp wird vor jeder Gerätebestätigung gebaut; blockierende Dialoge; Zeitplan.

**Unverifiziert:** jedes COM-Verhalten aus Python (I5 [ungeprüft]); bestätigt wird es erst am Montag durch den Nutzer.

**Rückfragen:** Abschnitt 10. Blockierend sind die ADR-Entscheidungen für U1–U3 und die GUI-Technologie samt Installationsfreigabe für U4.

**ADR-Kandidaten zur Anlage nach Freigabe:** ADR-01 bis ADR-11 aus Abschnitt 7.

**Vorschlag für KONVENTIONEN.md:**
- Jede schreibende COM-Operation steht in der Richtlinie mit Begründung, Argumentprüfung und eigenem Test. Messende Aufrufe (`ScanEx`, `Stop`) sind zusätzlich an eine Messfreigabe gebunden.
- Betriebsarten `SIMULATOR` / `NUR_LESEN` / `TROCKENLAUF` / `MESSEN`. Eine echte Messung gibt es nur nach ausdrücklicher Bestätigung je Durchgang.
- Zeitabhängige Logik nutzt eine injizierbare Uhr; Tests warten nicht in Echtzeit.
- Zeitstempel in Protokollen nach ISO 8601 mit Zeitzone plus UTC.

**Empfehlung für den nächsten Schritt:**
- Plan und ADR-Empfehlungen dem Nutzer vorlegen; GUI-ADR aus dem Parallelpaket mit der Installationsfrage abgleichen.
- Danach U1 sofort starten, dann U2 und U3 parallel (getrennte Dateien, Protocol nach U1 fest).
- U2 (Nebenläufigkeit) und U3 (Sicherheitslogik) sind die anspruchsvollsten Pakete und eignen sich für das stärkere freigegebene Modell; U1 und U5 sind normal.

**Review-Empfehlung:** Schwerpunkte für das spätere Review:
- Zustandsmaschine und Sperren (R-016, Pause/Abbruch, `GERAET_UNKLAR`)
- Vollständigkeit der Richtlinie gegenüber dem „Nie“-Katalog
- Messfreigabe-Sperre und Schutz vor Überschreiben
