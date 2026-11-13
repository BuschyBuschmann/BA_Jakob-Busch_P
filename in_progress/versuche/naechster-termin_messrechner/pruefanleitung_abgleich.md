# Prüfanleitung Abgleichstatus am Messrechner (R-003a lesen, R-003b prüfen)

Stand: 2026-11-12, Paket U-R003. Grundlage: Plan `in_progress/planung/plaene/2026-11-09_P-R003_abgleich-plan.md`
(Abschnitte 4, 6, 7), Analyse `in_progress/analysen/2026-11-09_A1-B13_alignment-benachrichtigung.md`,
KONVENTIONEN (Hardware, Messdaten), ADR-007.

**Kein Punkt gilt als bestanden, bevor Jakob ihn bestätigt hat** (danach `/laborbuch`; erst dann
setzt sich der Stand „am Gerät bestätigt“, Akzeptanzkriterium A10 des Plans). Alle COM-Aussagen
unten stammen aus Dokumentation und Code und sind am Gerät **unbestätigt**: ob `Infos.Alignments`
im Erfassungsmodus lesbar ist, ob `Item` 1-basiert zählt, ob Einheiten (m, rad) stimmen und ob
`Valid` sinnvolle Werte liefert. Eine Abweichung ist ein **Befund, kein Fehler der Anleitung**:
Zahl und Text notieren, keine Korrektur vor Ort.

## Sicherheitsrahmen

- Es wird **nichts** am Abgleich ausgelöst, berechnet oder ungültig gemacht (Stufe 3 ist nicht Teil
  dieser Software). Die Software liest nur: `Infos.HasAlignments`, `Infos.Alignments`,
  `Alignments3D`/`Alignments2D` (`Count`, `Item`) und die Properties `Valid`, `CurrentQuality`,
  `TargetQuality`, `PositionUncertainty`, `AngleUncertainty` bzw. `ScanHeadDistance`.
- **Annahme (am Gerät zu bestätigen):** Lesen bewegt Laser und Spiegel nicht. Beobachte den Aufbau
  beim ersten Lauf; bei jeder Bewegung oder Dialogmeldung von PSV sofort abbrechen und notieren.
- Aber: Die **Trockenlauf**-Betriebsart lädt die Test-`.set` mit `Settings.Load` (Lademaske enthält
  `Alignment`, `2DAlignment`, `3DAlignment`). Das **überschreibt den aktuell in PSV geladenen
  Abgleich** durch den Abgleich aus der `.set`. Vor T2 die Vorgaben aus `ablaufplan.md` (Test-`.set`,
  Hinweisdialog) beachten. Einen Abgleich, der für eine echte Messung gebraucht wird, nie durch
  eine fremde `.set` ersetzen.
- Keine Messung, kein Scan, keine Anregung (Generator bleibt aus).

## Voraussetzungen

1. Schritt 0 des Plans: Erkundung `P1-6-abgleich` (in `erkundung.py --stufe 1`, Prüfzettel B1) lief
   und ihr Ergebnis ist notiert: `Alignments3D.Count`, `Valid`, `CurrentQuality`, Fehlerbild.
   Fehlt es, trotzdem weitermachen; die Software meldet „nicht lesbar“ mit Grund.
2. Installierter Stand mit dieser Funktion. **[offen]** Die Versionsnummer und der Wheel-Build kommen
   mit dem Auslieferungspaket des Orchestrators (KONVENTIONEN: jeder ausgelieferte Stand erhält eine
   neue Versionsnummer). Der Plan-Beschluss F1 (Feld `abgleich` unter Schema 2) gilt nur, solange
   Wheel 0.2.0 nie installiert wurde und kein Schema-2-Protokoll entstanden ist. Vor der
   Installation prüfen und im Protokoll festhalten: `Get-ChildItem "$ARB\daten" -Recurse -Filter *.protokoll.json`
   darf **keine** Datei mit `"schema_version": 2` zeigen. Gibt es eine, vorher Rücksprache (dann
   Schema 3).
3. Selbsttest nach Installation (`ablaufplan.md`, I5) grün.
4. Konfig-Kopie ohne Grenzwerte: Kopie von `beispiel_messrechner.json` nach `$T\konfig_abgleich_aus.json`
   (enthält `"abgleich_pruefung": "aus"`, **keine** Grenze). `Get-FileHash` notieren.

`$PY`, `$ARB`, `$T` wie in `ablaufplan.md`.

## Ablauf

| Nr | Prüfung | Erwartet | Ergebnis / Beobachtung | Jakob bestätigt |
|---|---|---|---|---|
| AB1 | Programm mit Konfig `aus` starten: `& $PY -m ldv_automation gui --psv --betriebsart trockenlauf --messdaten "$ARB\daten" --konfig "$T\konfig_abgleich_aus.json"` | Start ohne Fehlermeldung; Dialog „Gerät“ zeigt in der Konfiguration `abgleich_pruefung: aus` und die vier übrigen Abgleichschlüssel (Grenzen leer) | | |
| AB2 | Trockenlauf mit **einer** vorhandenen Test-`.set` (T2 in `ablaufplan.md`, Generator aus): Durchgang starten, bis „fertig“ | Läuft durch, **Laser und Spiegel bewegen sich nicht**, kein Scan, keine Dialogmeldung von PSV | | |
| AB3 | Protokoll öffnen: `Get-Content "<Durchgangsordner>\01_*.protokoll.json" -Raw \| ConvertFrom-Json \| Select-Object -ExpandProperty abgleich \| ConvertTo-Json -Depth 6` | Feld `abgleich` vorhanden. Notieren: `gelesen`, `grund`, `anzahl_3d`, `anzahl_2d`, je 3D-Eintrag `gueltig`, `qualitaet_ist_m`, `qualitaet_soll_m`, `positionsunsicherheit_m`, `winkelunsicherheit_rad`, `nicht_lesbar`, je 2D-Eintrag `gueltig`, `scankopfabstand_m`. `pruefung.modus = aus`, `pruefung.ergebnis = nicht_geprueft`. Nicht lesbare Werte sind `null` mit Grund | | |
| AB4 | Vergleich mit der PSV-Anzeige des 3D-Abgleichs (Qualität, Unsicherheiten): Einheit (Software: m und rad) und Größenordnung gegen die Anzeige in PSV prüfen | Gleiche Größe nach Umrechnung (z. B. mm → m). Abweichung (z. B. Faktor 1000, Grad statt rad) als Befund festhalten; **keine** Korrektur vor Ort | | |
| AB5 | Ereignisprotokoll `durchgang.ereignisse.jsonl` und Protokollfenster der Oberfläche: bei `Valid = False`, `Count = 0` oder nicht lesbaren Feldern erscheint „Warnung: Abgleich auffällig: …“ (Art `abgleich_hinweis`) | Bei gültigem, vollständig gelesenem Abgleich **kein** Hinweis; sonst genau ein Hinweis je geänderter Befundlage | | |
| AB6 | Indexbasis: Ist `anzahl_3d` ≥ 1 und der Eintrag mit `index: 0` gelesen? Gibt es stattdessen „nicht lesbar“ bei Item? | `Item(1)` liefert den ersten Abgleich (Annahme 1-basiert). Liefert er nichts oder einen Fehler: Text aus `nicht_lesbar` in den Befund; **nicht** `Item(0)` probieren (die Whitelist verweigert es bewusst, I5 P2-12 bleibt offen) | | |
| AB7 | Gate-Test mit zu strenger Grenze (Trockenlauf): **Voraussetzung:** AB3 liefert für `qualitaet_ist_m` eine Zahl > 0. Ist der Wert `null` (nicht lesbar), `0` oder gibt es keinen 3D-Abgleich (`anzahl_3d` = 0, z. B. Ersatzweg B3 mit Test-`.set` ohne Abgleich): **Schritt überspringen** und als Befund notieren (Nr, Wert bzw. `nicht_lesbar`-Text); keine Grenze erfinden, keinen Abgleich herstellen. Kopie `$T\konfig_abgleich_streng.json` mit `"abgleich_pruefung": "verweigern"` und `"abgleich_qualitaet_max_m"` = **halber** in AB3 gelesener `qualitaet_ist_m` (Grenze aus dem Messwert abgeleitet, nicht aus Zahlen im Plan). Neu starten mit `--konfig` auf diese Datei, gleichen Trockenlauf wiederholen | Messung endet mit Fehler **„Abgleich“** (Fehlerart `abgleich`), Text nennt Wert und Grenze in mm und m; **kein** Scan (im Trockenlauf ohnehin keiner: maßgeblich ist Fehlerart und Status `fehler` im Protokoll, `pruefung.ergebnis = nicht_bestanden`); Protokoll enthält `pruefung.grenzen` mit dem eingetragenen Wert | | |
| AB8 | Gate-Test mit großzügiger Grenze: **Voraussetzung:** AB3 lieferte für `qualitaet_ist_m` eine Zahl > 0. Ist der Wert `null` (nicht lesbar), `0` oder gibt es keinen 3D-Abgleich (`anzahl_3d` = 0, z. B. Ersatzweg B3 mit Test-`.set` ohne Abgleich): **Schritt überspringen** und als Befund notieren (Nr, Wert bzw. `nicht_lesbar`-Text); keine Grenze erfinden, keinen Abgleich herstellen. wie AB7, aber **doppelter** gelesener Wert | Trockenlauf läuft durch, `pruefung.ergebnis = bestanden`, Status `trockenlauf` | | |
| AB9 | Modus `warnen`: wie AB7 (strenge Grenze), `"abgleich_pruefung": "warnen"` | Trockenlauf läuft durch (Status `trockenlauf`), im Protokollfenster „Warnung: Messung …: Abgleich nicht_bestanden …“ (Art `abgleich_warnung`) | | |
| AB10 | Ungültige Konfiguration: in einer Kopie `"abgleich_qualitaet_max_m": 0` | Start bricht mit Rückgabewert 2 ab; Meldung nennt `$.abgleich_qualitaet_max_m` | | |
| AB11 | Optional, nur falls eine `.set` **ohne** gültigen Abgleich vorliegt: Modus `verweigern` ohne Grenzen, Trockenlauf mit dieser `.set` | Fehler „Abgleich“ wegen `Valid = False`. Einen Abgleich **nie absichtlich zerstören**, um diesen Punkt zu erzwingen | | |

## Hinweise zur Auswertung

- Befunde mit Nummer, Zahl und ggf. Foto in `protokoll.md` eintragen, die `abgleich`-Blöcke der
  Protokolle (AB3, AB7, AB8) auf den Stick sichern. Nachweise gehen über `/laborbuch` in die
  Nachverfolgung (R-003a/b) ein.
- Grenzwerte dieser Anleitung sind **nur Prüfwerte** aus dem gelesenen Messwert (AB7: halber, AB8:
  doppelter Wert), keine fachlichen Grenzen. Fachliche Grenzen und die Frage „verweigern oder
  warnen, wann“ klärt der Betreuer (Plan F2, F3).
- Bei einem Hänger beim Lesen (Aufruf dauert länger als `aufruf_grenze_s`) wechselt der Durchgang
  nach `GERAET_UNKLAR` wie bei jedem hängenden Geräteaufruf; PSV prüfen, Befund notieren.
- Ein zusätzlicher Geräteaufruf je Messung (`lies_abgleich`: `Count` plus wenige `Item`): Dauer
  im Zugriffsprotokoll (Dialog „Gerät“) notieren.
