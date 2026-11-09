<!-- Vom Nutzer am 2026-11-09 freigegeben. F1: Wheel 0.2.0 nie installiert (Termin 09.11. ausgefallen), Feld `abgleich` bleibt unter Schema 2. F2–F6 wie Annahmen im Plan. R-003 aufgeteilt in R-003a/b/c; dieser Plan setzt R-003a und R-003b um. Umsetzung nach Etappe A der Auswertung (gemeinsame Stelle gui/anzeige.py). -->

<!-- Paket P-R003 (software-engineer), Typ Planung. Status: PLAN ZUR FREIGABE (2026-11-09). Es wurde nichts am Repository geändert außer dieser Datei. Nichts ausgeführt am Gerät; alle COM-Aussagen stammen aus Doku und Code (am Messrechner unbestätigt). -->

## Plan: R-003 Stufe 1 und 2 (Abgleichstatus lesen, protokollieren, vor der Messung prüfen)

Grundlage: Analyse A1-B13 (Abschnitt 1, E1 bis E10), Lastenheft R-003/O9, KONVENTIONEN, ADR-007/008/014, Code `geraet/`, `ablauf/steuerung.py`, `protokoll/`, `konfig.py`, Erkundung `P1-6-abgleich`.
Nutzerentscheidung 2026-11-09: Stufe 1 (lesen + protokollieren) und Stufe 2 (Prüfung vor der Messung, Grenze konfigurierbar). Stufe 3 (Abgleich auslösen) ist nicht Teil.

### 0 Kernbefunde

1. **Lesen am Gerät ist unbestätigt.** `P1-6-abgleich` lief am 2026-11-02 nie. Offen: ob `Infos.Alignments` im Erfassungsmodus lesbar ist, die Indexbasis von `Alignments3D.Item` (I5 P2-12), die Zahl der Einträge, ob `Valid`/Qualitäten sinnvolle Werte liefern. Der Plan baut deshalb **feldweise tolerantes Lesen** (jeder Wert einzeln, Fehler als `null` + Grund) und kennzeichnet alles als „unverifiziert“, bis der Nutzer am Gerät bestätigt.
2. **Jeder Bestandsablauf wird berührt.** `lies_abgleich` kommt in jede Messung (nach `lies_einstellungsstand`). Exakte Aufrufreihenfolgen in Bestandstests ändern sich: sicher `tests/sitzung/test_sitzung_korrektur_k_u2.py:97` (Aufrufe nach `verbinde` bleiben: dort wird nur beim Verbinden gelesen, siehe Schritt 5: Lesen nur in der Messung, deshalb voraussichtlich unverändert, zu prüfen), `tests/protokoll/test_protokoll_module.py` (`PFLICHTFELDER`), `tests/ablauf/test_ablauf_akzeptanz.py::_pruefe_schema`. Der Simulator-Aufruf wird protokolliert wie alle anderen.
3. **Schemaversion:** `SCHEMA_VERSION = 2` ist laut Modulkommentar „noch nicht ausgeliefert“. Befund: im Repo liegen keine Protokolle mit Schema 2; Wheel 0.2.0 (Build a0ee2fc, Schema 2) liegt nur auf dem Stick; der Messrechner-Termin 09.11. fiel aus; der Prüfzettel plant die Installation von 0.2.0 erst am nächsten Termin (12./13.11.). Nach KONVENTIONEN gilt „ausgeliefert“ = auf dem Messrechner oder in gespeicherten Daten. **Annahme: nicht ausgeliefert, `abgleich` kommt unter Schema 2.** Wird 0.2.0 vorher installiert oder entsteht ein Schema-2-Protokoll, wird es Schema 3 (Frage F1).
4. **Whitelist:** `Alignment3D.Calculate` steht im `NIE_KATALOG`; Lesefreigaben für `Infos.Alignments` fehlen. `_pruefe_index` verlangt Index >= 1 (passt zu 1-basiert; wäre `Item` 0-basiert, scheitert der Zugriff laut Whitelist und wird als „nicht lesbar“ protokolliert, nicht still umgangen).
5. **Prüfung nach dem Laden:** Die `.set` bringt den Abgleich mit (Lademaske enthält 2D-/3D-Abgleich). Gelesen und geprüft wird deshalb je Messung **nach** `lade_einstellungen`.

### 1 Ansatz

* Neues kleines Protocol `Abgleichsleser` (`lies_abgleich() -> AbgleichStand`) in `geraet/schnittstelle.py`, **neben** `Messgeraet`. Simulator und COM-Adapter erfüllen beide; die Steuerung prüft per `isinstance`. Ein Gerät ohne Leser (Test-Fakes) gilt als „nicht lesbar“. Begründung: `Messgeraet` ist `runtime_checkable`; eine zusätzliche Methode ließe alle Fakes (`tests/gui/gui_hilfen.py`, `tests/geraet_com`) die Prüfung verfehlen.
  *Alternative:* Teil von `EinstellungsStand`. Spart ein Protocol, vermischt aber „Einstellungen“ und „Aufstellung“ und macht jeden Fehler beim Abgleichlesen zu einem Fehler des Einstellungsstands.
* Gelesener Kern (nur Dokumentiertes, Einheiten laut BEM): 3D: `Valid`, `CurrentQuality` (m), `TargetQuality` (m), `PositionUncertainty` (m), `AngleUncertainty` (rad); 2D: `Valid`, `ScanHeadDistance` (m). Nicht Teil: `GetScanHeadPosition`/`GetVideoRect` (ByRef-Ausgabeparameter, mit Late Binding ungeprüft), `CoordDefinitionMode`, `Mirror`, Punktlisten, Kameraabgleich.
* Feldweise tolerantes Lesen: `AbgleichStand` trägt je Eintrag Werte oder `None` plus Grund; `lies_abgleich` wirft nur bei „nicht verbunden“ und Hängern (`ZeitlimitFehler`, wie jeder Aufruf; Hänger bleibt `GERAET_UNKLAR`).
* Protokoll: neues Pflichtfeld `abgleich` je Messung (immer vorhanden, auch bei `fehler`/`abgebrochen`), Muster wie `frequenzachse`.
* Prüfung (Stufe 2) als reine Funktion in neuem Modul `ablauf/abgleich.py`; Modus `aus` (Default) | `warnen` | `verweigern`. Kriterien: alle gelesenen 3D-Abgleiche `Valid == True`, mindestens ein 3D-Abgleich vorhanden, optionale Grenzen (nur aus Konfiguration, keine Standardwerte). Nicht prüfbar (nicht gelesen, Wert fehlt trotz gesetzter Grenze) gilt als **nicht bestanden** (fail-closed), aber nur im Modus `verweigern` mit Wirkung.

### 2 Schritte (riskanteste Annahmen zuerst; nach jedem Schritt ist der Code konsistent und alle Prüfungen laufen)

| # | Schritt | Dateien | verifiziert durch |
|---|---|---|---|
| 0 | **Nutzer am Messrechner (parallel, nicht blockierend):** vorhandene Erkundung `P1-6-abgleich` ausführen (nur lesend, im Prüfzettel Schritt B1) und Count, Valid, Qualitäten, Fehlerbild notieren. Kein neuer Code. | – | Erkundungsbericht; Ergebnis in Annahmenliste und Prüfanleitung |
| 1 | Datentypen und Protocol: `Abgleich3D`, `Abgleich2D` (frozen, `index` 0-basiert, `gueltig: bool\|None`, Werte `float\|None`, `nicht_lesbar: Mapping[str,str]`), `AbgleichStand` (`abgleich_3d`, `abgleich_2d`, `anzahl_3d/2d: int\|None`, `nicht_lesbar`, `hinweis`), `Abgleichsleser`. Moduldoku: Vertrag (Geräte-Thread, nur lesend, Einheiten m/rad). | `geraet/schnittstelle.py` | mypy strict; `tests/geraet/test_geraet_schnittstelle.py`: Dataclasses unveränderlich, `isinstance` für Fake mit/ohne Methode |
| 2 | **Whitelist + COM-Adapter (größtes Risiko):** Lesefreigaben `Infos.HasAlignments`, `Infos.Alignments`; Typen `Alignments` (`Alignments3D`, `Alignments2D`), `Alignments3D`/`Alignments2D` (`Count`, `Item` über `_element`), `Alignment3D` (5 Properties), `Alignment2D` (`Valid`, `ScanHeadDistance`). **Keine** neue S-Nummer, keine Schreibfreigabe. `NIE_KATALOG` ergänzen: `Alignment3D.Invalidate`, `Alignment2D.Calculate/Invalidate`, `Alignments3D/2D.Add/Clear/Remove`, `Alignments3D/2D.Count` setzen, `Alignment3D.Valid` setzen (`Alignment3D.Calculate` bleibt). Adapter `lies_abgleich`: `HasAlignments` prüfen, `Count` lesen, `Item(1..min(Count, MAX_ABGLEICHE))` (Schutzgrenze, Hinweis bei Überschreitung; Konstante nennt ihre Herkunft: Schutz, kein Gerätewert), jedes Feld in eigenem `try`; Bool nur bei echtem `bool`, Float nur endlich, sonst `None` + Grund; Umrechnung Polytec-Index 1-basiert -> `index` 0-basiert nur hier. Docstring `richtlinie.py` um die Lesefreigabe ergänzen. | `geraet/com/richtlinie.py`, `geraet/com/adapter.py`, `tests/geraet_com/fake_psv_com.py` (Fake-Knoten `Alignments`, Parameter `abgleich=…`) | `test_geraet_com_richtlinie.py` (neue Lesefreigaben vorhanden; alle neuen `NIE_KATALOG`-Einträge verweigert; Struktur-Test: im neuen Teilbaum ist nur `Item` ein `call`; Liste der Schreibfreigaben und `schreibbegruendungen()` unverändert), `test_geraet_com_adapter.py` (Fälle in Abschnitt 5), `Welt.schreibende` leer |
| 3 | Simulator: `SimulatorKonfiguration.abgleich: AbgleichStand` (Default gültig mit klar als Testdaten gekennzeichneten Platzhalterwerten), Drehbuch `AbgleichBeiLaden(vorgang, stand)` (Abgleich wechselt mit `lade_einstellungen`, bildet den Fall „veralteter Abgleich in der `.set`“ ab) und `AbgleichNichtLesbar(vorgang, text)`; `lies_abgleich` protokolliert den Aufruf, prüft Verbindung, unterstützt `HaengenderAufruf`/`LangsamerAufruf` mit `methode="lies_abgleich"`. | `geraet/simulator.py` | `tests/geraet/test_geraet_simulator.py`: Default, Wechsel je Vorgang, Nicht-lesbar, Hänger; `isinstance(Simulator, Abgleichsleser)` |
| 4 | Prüflogik und Konfiguration: `AbgleichRegel` (frozen; `modus`, `qualitaet_max_m`, `position_max_m`, `winkel_max_rad` je `float\|None`, `pruefe_2d: bool`; Validierung: endlich und > 0, **keine Obergrenze**, weil jede erfunden wäre) und `pruefe_abgleich(stand, grund, regel) -> AbgleichPruefung` (`ergebnis`: `nicht_geprueft`/`bestanden`/`nicht_bestanden`/`nicht_pruefbar`, `befunde: tuple[str,...]`). `AblaufKonfiguration.abgleich: AbgleichRegel = AbgleichRegel()`. `konfig.py`: optionale Schlüssel `abgleich_pruefung`, `abgleich_qualitaet_max_m`, `abgleich_position_max_m`, `abgleich_winkel_max_rad`, `abgleich_2d_pruefen`; streng geprüft wie bisher; `protokoll_info()["werte"]` enthält sie (damit stehen die Grenzen im Protokoll, KONVENTIONEN „Konfigurationsdatei vollständig ins Messprotokoll“); `schema_version` der Konfigdatei bleibt 1 (neue Schlüssel optional, alte Dateien bleiben gültig). `konfig/beispiel_messrechner.json` bekommt nur `"abgleich_pruefung": "aus"`, **keinen** Grenzwert. Neue `FehlerArt.ABGLEICH`. | `ablauf/abgleich.py` (neu), `ablauf/steuerung.py` (nur `AblaufKonfiguration`), `ablauf/fehlerstrategie.py`, `konfig.py`, `konfig/beispiel_messrechner.json` | neue `tests/ablauf/test_ablauf_abgleich.py` (Tabelle, Abschnitt 5), `tests/test_konfig.py` (gültig, ungültig mit JSON-Pfad, Protokollinfo); `test_vorlaeufige_strategie_fragt_immer` iteriert über alle `FehlerArt` und deckt die neue Art mit ab |
| 5 | Steuerung und Protokoll: `_Aktiv.abgleich`/`abgleich_grund`/`abgleich_pruefung`. In `_fuehre_messung_aus` direkt nach `lies_einstellungsstand`: `_lese_abgleich` (nur wenn `isinstance(geraet, Abgleichsleser)`, via `_aufruf`; `ZeitlimitFehler` -> bestehender Hängerpfad; sonstiger `GeraeteFehler` -> „nicht lesbar“ mit Grund, keine Unterbrechung). Auswertung der Prüfung **nach** den bisherigen Fehlerprüfungen (Abweichung, Modus), also vor `speichere_einstellungen`/Trockenlauf-Ende/`starte_scan`: `verweigern` + nicht bestanden/nicht prüfbar -> `_messung_fehler(..., FehlerArt.ABGLEICH, Text)`, kein Scan; `warnen` -> Ereignis `abgleich_warnung`; `aus` -> nie ein Eingriff. Bei Auffälligkeit (ungültig, nicht lesbar, Befund) ein Ereignis `abgleich_hinweis`, im Durchgang nur bei geändertem Befundtext. `messprotokoll.py`: `abgleich_zu_dict(...)`, `PFLICHTFELDER` um `abgleich` nach `frequenzachse`, Moduldoku, Kommentar an `SCHEMA_VERSION` (bleibt 2, siehe F1). `_protokolliere` schreibt das Feld. | `ablauf/steuerung.py`, `protokoll/messprotokoll.py`, `tests/protokoll/test_protokoll_module.py`, `tests/ablauf/test_ablauf_akzeptanz.py` | Abschnitt 5 Steuerungstests; Gesamtlauf der Standard-Prüfung; Bestandstests ohne Abschwächung angepasst (nur erwartete neue Aufrufe/Felder) |
| 6 | Minimale Anzeige: `abgleich_warnung` und `abgleich_hinweis` in `_WARN_ARTEN` (zwei Wörter in einer `frozenset`-Konstante, Präfix „Warnung:“). **Keine** neuen Widgets, kein Eingriff in Reiter „Auswerten“, `darstellung/` oder `plotflaeche.py`. Ein Fehler des Gates erscheint bereits als „Fehler: …“ über die Ereignisart `fehler`. | `gui/anzeige.py` (eine Konstante) | `tests/gui/test_gui_anzeige.py`: `protokolltext` für beide Arten. **Abstimmung nötig:** Ein anderes Paket ändert parallel `gui/`; `anzeige.py` ist nicht `auswerten_reiter.py`/`darstellung/`, die Änderung ist 1 Zeile; falls Konfliktgefahr, nach dem anderen Paket einspielen |
| 7 | Dokumentation und Prüfanleitung: Prüfanleitung für den Messrechner (Abschnitt 7) unter `in_progress/versuche/…`, Beispiel-Konfigkopie für den Gate-Test, Hinweis im Moduldoc. ADR-Entwürfe liefert der Orchestrator nach Freigabe (Abschnitt 8). Wheel/Version (`pyproject.toml` `version`) erst im Auslieferungspaket des Orchestrators. | `in_progress/versuche/…/pruefanleitung_abgleich.md` (neu) | Review; Ausführung erst am Gerät |

Standard-Prüfung nach Schritt 1 bis 6 jeweils vollständig (`uv run ruff check .`, `ruff format --check .`, `mypy --strict .`, `pytest --cov --cov-fail-under=90`). Die COM-Adapter-Logik bleibt voll abgedeckt (Fake), keine neue `# pragma: no cover` nötig.

### 3 Protokollfeld `abgleich` (Schema 2, siehe F1)

Einheit im Namen, Längen in m, Winkel in rad, Index intern 0-basiert (Polytec-Index nur im Adapter). Nicht lesbar = `null` + Grund in `nicht_lesbar` (Muster `frequenzachse`).

```
"abgleich": {
  "gelesen": bool,                      # false: nicht gelesen (Grund in "grund")
  "grund": str | null,
  "zeit": {"lokal": …, "utc": …} | null,
  "anzahl_3d": int | null, "anzahl_2d": int | null,
  "abgleich_3d": [ {"index": 0, "gueltig": bool|null,
                    "qualitaet_ist_m": f|null, "qualitaet_soll_m": f|null,
                    "positionsunsicherheit_m": f|null, "winkelunsicherheit_rad": f|null,
                    "nicht_lesbar": {feld: grund}} ],
  "abgleich_2d": [ {"index": 0, "gueltig": bool|null, "scankopfabstand_m": f|null,
                    "nicht_lesbar": {…}} ],
  "nicht_lesbar": {…},                  # pauschale Gründe (z. B. Infos.Alignments fehlt)
  "pruefung": {"modus": "aus|warnen|verweigern",
               "ergebnis": "nicht_geprueft|bestanden|nicht_bestanden|nicht_pruefbar",
               "grenzen": {"qualitaet_max_m": …, "position_max_m": …, "winkel_max_rad": …,
                           "pruefe_2d": bool},
               "befunde": [str]},
  "hinweis": "Werte aus COM Infos.Alignments (nur lesend), Einheiten laut BEM, am Gerät unbestätigt; gehört zur geladenen Einstellungsdatei (einstellungsdatei.sha256, lademaske)."
}
```
Die Herkunft (SHA-256 der `.set`, Lademaske) steht schon in `einstellungsdatei`/`lademaske` und wird nicht doppelt geführt. Nicht endliche Floats gelangen nie ins Feld (Adapter wandelt zu `null` + Grund).

### 4 Verhalten bei nicht lesbarem Abgleich

| Lage | Modus `aus` | `warnen` | `verweigern` |
|---|---|---|---|
| Gerät ohne Leser, `HasAlignments` False, Gerätefehler beim Lesen | `gelesen=false` + Grund, Hinweis-Ereignis, Messung läuft | zusätzlich `abgleich_warnung` | Fehler `ABGLEICH`, kein Scan |
| Einzelwert nicht lesbar | Wert `null` + Grund, Messung läuft | Warnung nur, wenn dafür eine Grenze gesetzt ist | Fehler nur, wenn dafür eine Grenze gesetzt ist (sonst Hinweis) |
| `Valid == False`/`null` (3D) | Hinweis, Messung läuft | Warnung | Fehler |
| Hänger | `GERAET_UNKLAR` wie jeder Hänger, unabhängig vom Modus | | |

### 5 Testplan (Simulator, Fakes, Tabellen; keine Hardware)

* **Prüflogik (reiner Test, handrechenbar):** Wert == Grenze besteht; `math.nextafter(grenze, inf)` besteht nicht; `None`/NaN bei gesetzter Grenze -> `nicht_pruefbar`; ohne gesetzte Grenze zählt nur `Valid`; `anzahl_3d == 0` -> nicht bestanden; mehrere 3D-Einträge: alle müssen bestehen; 2D nur mit `pruefe_2d`; Modus `aus` -> `nicht_geprueft`. Vergleiche exakt (`<=`), Begründung: Grenze ist eine Vorgabe, keine Messgröße; Rundung entfällt.
* **Adapter mit Fake-COM:** Normalfall 1x3D + 1x2D (Werte, Einheiten, Index 1 -> 0); `Count` 0; `Item` liefert `None`; `HasAlignments` False; COM-Fehler nur bei `CurrentQuality` (übrige Felder gelesen); `Valid` als Nicht-Bool; NaN/Inf; `Count` über Schutzgrenze; `Welt.schreibende == []`; jeder Zugriff steht im Aufrufprotokoll; Betriebsart `NUR_LESEN` darf lesen.
* **Steuerung mit Simulator:** Aufrufreihenfolge (`lade_einstellungen`, …, `lies_einstellungsstand`, `lies_abgleich`, …, `starte_scan`); `aus` + ungültiger Abgleich -> Messung wird gemessen (Invariante: Aufrufverlauf unterscheidet sich vom Bestand nur um `lies_abgleich`); `verweigern` + schlechter Abgleich -> Status `fehler`, Fehlerart `abgleich`, kein `starte_scan`, Protokoll trägt `abgleich` und Befund; `warnen` -> `fertig` + `abgleich_warnung`; Trockenlauf wertet das Gate aus (Voraussetzung für `MESSEN` bleibt die erste erfolgreiche Trockenmessung); Gerät ohne Leser; `AbgleichNichtLesbar`; `HaengenderAufruf(methode="lies_abgleich")` -> `GERAET_UNKLAR`; Abgleich wechselt zwischen zwei Messungen (`AbgleichBeiLaden`); Fehler vor dem Lesen (Vorprüfung) -> `gelesen=false`; Abbruchpfade schreiben das Feld.
* **Protokoll/Konfig:** `PFLICHTFELDER`-Reihenfolge, `fehlende_pflichtfelder`, JSON-Roundtrip; Konfig gültig/ungültig (negativ, 0, NaN, `true` statt Zahl, unbekannter Modus, unbekannter Schlüssel), `protokoll_info`.
* **Verifikationsarten (mindestens zwei):** handgerechnete Tabellen für die Prüflogik, Fake-COM als unabhängiges Orakel für den Adapter, Invarianten (Modus `aus` verändert den Ablauf nicht; Schreibliste der Whitelist unverändert). Gerätewerte selbst bleiben **unverifiziert**, bis Schritt 0 und die Prüfanleitung am Gerät bestätigt sind.
* **Bestandstests, die sich ändern dürfen:** nur Erwartungen zu Pflichtfeldern bzw. neuer Aufruf; nichts wird gelockert.

### 6 Akzeptanzkriterien

* A1: Jedes Messprotokoll enthält `abgleich` (auch bei `fehler`/`abgebrochen`), Einheiten im Feldnamen, nicht Lesbares als `null` mit Grund. Test: Schemaprüfung über alle Protokolle im Akzeptanztest.
* A2: Mit Simulator und Fake-COM werden Gültigkeit, Ist-/Soll-Qualität, Positions- und Winkelunsicherheit (3D) sowie Gültigkeit und Scankopfabstand (2D) korrekt in das Protokoll übernommen.
* A3: Lesen verändert nichts: Whitelist-Schreibfreigaben unverändert, `Welt.schreibende` leer, keine Methode aus dem `NIE_KATALOG` freigegeben, neue Katalogeinträge verweigert.
* A4: Modus `aus` (Voreinstellung) blockiert nie, auch bei ungültigem oder nicht lesbarem Abgleich.
* A5: Modus `verweigern` startet bei ungültigem Abgleich, überschrittener Grenze oder Nicht-Prüfbarkeit (bei gesetzter Grenze) keinen Scan; Fehlerart `abgleich` mit Befundtext; Grenzfall Wert == Grenze besteht.
* A6: Grenzen stehen nur in der Konfigurationsdatei, ohne Standardwerte; ungültige Werte führen zu `KonfigFehler` mit JSON-Pfad; die verwendeten Werte stehen im Messprotokoll (`konfiguration`) und in `abgleich.pruefung.grenzen`.
* A7: Ein Hänger beim Lesen führt wie jeder Hänger zu `GERAET_UNKLAR`.
* A8: Ohne Leser am Gerät läuft die Messung (Modus `aus`) mit `gelesen=false`.
* A9: Standard-Prüfung vollständig grün, Abdeckung >= 90 %.
* A10 (Hardware, erst nach Bestätigung durch den Nutzer): Am Messrechner liefert das Protokoll Werte, die mit der PSV-Anzeige des Abgleichs übereinstimmen (Einheit und Größenordnung), und das Gate verhält sich wie in der Prüfanleitung.

### 7 Prüfanleitung für den Messrechner (Ablauf G; wird in Schritt 7 ausgearbeitet)

Der Hardwaretest gilt erst als bestanden, wenn der Nutzer es bestätigt (Laborbuch via `/laborbuch`).
1. Vorab Erkundung `P1-6-abgleich` (Schritt 0): Count, Valid, Fehlerbild notieren.
2. Neues Wheel installieren, Selbsttest, Konfig-Kopie ohne Grenzwerte (`abgleich_pruefung: aus`).
3. **Trockenlauf** mit einer vorhandenen Test-`.set` (Warteschlange T4): bewegt weder Laser noch startet er einen Scan. Protokoll öffnen: `abgleich.gelesen`, Werte, Einheiten notieren.
4. Vergleich mit der PSV-Anzeige des 3D-Abgleichs (Qualität, Unsicherheiten): Einheit (m, rad) und Größenordnung prüfen; Abweichung als Befund festhalten, keine Korrektur vor Ort.
5. Gate-Test (Trockenlauf): Konfig-Kopie mit `abgleich_pruefung: verweigern` und einer Grenze **aus dem Messwert abgeleitet** (z. B. halber bzw. doppelter gelesener Wert, nicht aus Zahlen im Plan); erwartet: zu strenge Grenze -> Fehler „Abgleich“, kein Scan; großzügige Grenze -> bestanden.
6. Optional, nur falls eine `.set` ohne gültigen Abgleich vorliegt: Verhalten bei `Valid == False` prüfen. Abgleich nie absichtlich zerstören.
7. Ergebnisse und Befunde sichern, danach `/laborbuch`.
Annahme (am Gerät zu bestätigen): Lesen bewegt Laser und Spiegel nicht.

### 8 Entscheidungen mit Alternativen (ADR-Entwürfe nach Freigabe)

| Nr. | Entscheidung | Alternativen | Empfehlung |
|---|---|---|---|
| D1 | Schnittstelle | (a) Protocol `Abgleichsleser`; (b) Methode in `Messgeraet`; (c) in `EinstellungsStand` | (a) |
| D2 | Ablage | (a) Feld `abgleich` je Messung; (b) nur im Ereignisprotokoll; (c) eigener Warteschlangeneintrag | (a) |
| D3 | Gate-Verhalten | (a) fest verweigern; (b) fest warnen; (c) einstellbar `aus/warnen/verweigern`, Default `aus` | (c), weil Betreuerantwort A5 offen und keine Grenzen bekannt |
| D4 | Fehlerart | (a) neue `FehlerArt.ABGLEICH`; (b) `VORPRUEFUNG` (Doku: „ohne Gerätewirkung“, trifft nicht zu, Gate läuft nach `Settings.Load`); (c) `ABWEICHUNG` | (a) |
| D5 | Ort der Grenzen | (a) flache optionale Schlüssel in der Konfigurationsdatei (ADR-014), Konfig-Schema bleibt 1; (b) verschachteltes Objekt; (c) in der Oberfläche | (a); (c) verworfen (nicht reproduzierbar) |
| D6 | Anzeige | (a) nur Ereignisprotokoll bei Auffälligkeit; (b) Info je Messung; (c) Zeile im Dialog „Gerät“ | (a), (c) später möglich |
| D7 | Zeitpunkt | (a) je Messung nach Laden; (b) einmal je Durchgang | (a) (jede `.set` bringt ihren Abgleich); A6 an Betreuer |
| D8 | Whitelist | ADR-007 Nachtrag: Lesefreigaben `Infos.Alignments…`, ohne neue S-Nummer | wie vorgeschlagen |

### 9 Risiken

| Risiko | Erkennung/Maßnahme |
|---|---|
| `Alignments` im Erfassungsmodus nicht lesbar oder `Item` 0-basiert | Feldweise „nicht lesbar“ + Grund; Schritt 0; Whitelist verweigert Index 0 bewusst, Anpassung nur nach Gerätebefund |
| Einheiten oder Werte unplausibel (z. B. Qualität in mm statt m) | Prüfanleitung Schritt 4; Hinweis im Protokoll „unbestätigt“; Grenzen nur aus gemessenen Werten ableiten |
| Gate blockiert zu Unrecht (z. B. 2D irrelevant) | Default `aus`; 2D nur mit eigenem Schalter; `warnen` als Zwischenstufe |
| Grenzwert mit falscher Einheit in der Konfig (m statt mm) | Einheit im Schlüsselnamen; Grenzen werden im Protokoll und im Fehlertext in lesbaren Einheiten (mm, mrad) neben dem SI-Wert genannt |
| Schema-Konflikt, falls 0.2.0 schon verteilt | Frage F1; Umstellung auf Schema 3 kostet eine Zeile plus Testanpassung |
| Ein zusätzlicher Geräteaufruf je Messung (Zeit, Hänger) | `aufruf_grenze_s` gilt; Lesen ist klein (Count + wenige Items); Hänger-Pfad getestet |
| Paralleles Paket ändert `gui/` | Nur eine Konstante in `gui/anzeige.py`; Reihenfolge der Einspielung klären (F7) |

### 10 Nicht enthalten

Abgleich auslösen/neu berechnen/invalidieren (Stufe 3, A1/A4 beim Betreuer), Kameraabgleich, Kopfpositionen, Punktlisten, Konditionszahl, Vergleich zum Vorwert (A6), Anzeige im Reiter „Auswerten“, R-025, Wheel-Bau und Versionssprung.

### 11 Offene Fragen

Blockierend (für Schritt 5, nicht für Schritt 1 bis 4):
* **F1** Ist Wheel 0.2.0 / Schema 2 auf dem Messrechner installiert, oder liegen Schema-2-Protokolle irgendwo vor (nicht nur auf dem Stick)? *Auswirkung:* ja -> `SCHEMA_VERSION = 3`; nein -> bleibt 2. *Annahme bis zur Klärung:* nein.

Nicht blockierend:
* F2 (Betreuer A3) Welche Grenzwerte gelten (Qualität, Positions-, Winkelunsicherheit)? *Annahme:* keine; Modus `aus`, Grenzen leer.
* F3 (Betreuer A5) Verweigern oder warnen, und zu welchem Zeitpunkt (je Messung/Durchgang/nach Umbau)? *Annahme:* alle drei Modi einstellbar, je Messung.
* F4 Soll im Gate der 2D-Abgleich mitzählen? *Annahme:* nein (`abgleich_2d_pruefen` aus).
* F5 Kameraabgleich ins Protokoll? *Annahme:* nein.
* F6 Anzeige der Winkel in Texten: Grad (KONVENTIONEN) oder mrad (Polytec-Sprache)? *Annahme:* Grad mit mrad in Klammern.
* F7 Reihenfolge zum parallelen GUI-Paket für die Ein-Zeilen-Änderung in `gui/anzeige.py`.
* F8 Lastenheft R-003 (Akzeptanzkriterium „Abgleich aus der Software gestartet“) ist mit Stufe 1/2 nicht erfüllbar; Aufteilung R-003a (lesen), R-003b (prüfen), R-003c (auslösen, offen) über `/anforderungs-analyst` empfohlen. Nachverfolgungsmatrix danach anpassen.
* Hinweis zur Hängerbehandlung: Ein hängender Lesezugriff stoppt den Durchgang auch im Modus `aus` (`GERAET_UNKLAR`), das ist gewollt.
