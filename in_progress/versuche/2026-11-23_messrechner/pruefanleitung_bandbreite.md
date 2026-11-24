# Prüfanleitung Bandbreite nur als PSV-Stufe, Von/Bis mitsetzen (Paket BW-2)

Stand: 2026-11-23. Grundlage: Befund T2 vom 23.11. (Laborbuch
`in_progress/laborbuch/2026-11-23_messrechner-com-trockenlauf.md`), Entscheidungen des Nutzers vom
23.11. (Stufen zur Laufzeit aus PSV `AvailableBandwidths`; Von = 0 und Bis = Bandbreite werden
mitgesetzt; Auswahlliste statt freier Eingabe; Abweichung bei der Rückprobe = Fehler, kein Scan),
COM-Referenz `in_progress/analysen/2026-10-23_I5_com-referenz.md` (2.5, 2.6).

**Kein Punkt gilt als bestanden, bevor Jakob ihn bestätigt hat** (danach `/laborbuch`; erst dann
setzt sich der Stand „am Gerät bestätigt“). Im Simulator ist alles automatisiert getestet, am Gerät
ist **nichts** davon bestätigt. Unbestätigt sind insbesondere:

- ob `AvailableBandwidths` am Validator lesbar ist und in welcher Form (erwartet: Liste von Zahlen in Hz),
- ob PSV `StartFrequency` und `EndFrequency` im Validator annimmt,
- ob PSV schon beim Setzen der Bandbreite eine Ausnahme wirft, weil „Bis“ aus der `.set` (5000 Hz)
  größer ist als die neue Bandbreite (möglicher Grund für die Ablehnung von 4000 Hz am 23.11.).

Eine Abweichung ist ein **Befund, kein Fehler der Anleitung**: Zahl, Text und Meldung von PSV
notieren, keine Korrektur vor Ort.

## Sicherheitsrahmen

- Abschnitt 0 liest nur (Betriebsart `NUR_LESEN`).
- Abschnitte 1 bis 3 sind **Trockenläufe**: Sie laden die Test-`.set` mit `Settings.Load`
  (überschreibt den in PSV geladenen Abgleich, siehe `../naechster-termin_messrechner/pruefanleitung_abgleich.md`)
  und setzen Parameter, aber starten keinen Scan. Nur die Test-`.set` verwenden, keinen Abgleich
  überschreiben, den eine echte Messung braucht.
- Generator bleibt aus, keine Anregung.
- Vorlage: `vorlagen/test_5000Hz.set` (FFT 0 bis 5 kHz, 400 Linien, Mittelung komplex 3).

## 0. Lese-Sonde: Stufenliste (nur lesend, vor allem anderen)

1. Software starten, Betriebsart `NUR_LESEN`, mit PSV verbinden (PSV im Erfassungsmodus).
2. „Neue Messung“ öffnen und das Feld **Bandbreite** ansehen.
3. Notieren:
   - **Liste erscheint:** alle angebotenen Werte (Hz) abschreiben. In PSV unter den FFT-Einstellungen
     das Auswahlfeld „Bandbreite“ öffnen und die Werte vergleichen (nur ansehen, nichts ändern).
     Erwartung: dieselben Werte. Kommt 6250 Hz vor? Kommen 5600 Hz und 4000 Hz **nicht** vor?
   - **Statt der Liste steht „Stufenliste nicht lesbar“** oder ein Fehlertext: Text vollständig
     notieren (Hinweis steht im Feld bzw. Tooltip). Dann sind die Abschnitte 1 bis 3 nicht
     aussagekräftig; die Software ist dann bewusst gesperrt (kein Ersatz für fehlende Liste).
4. Optional: Verbindung trennen und prüfen, dass das Feld wieder „Erst mit PSV verbinden“ zeigt und
   gesperrt ist.

## 1. T2-Fall 5600 Hz (keine Stufe)

1. Betriebsart `TROCKENLAUF`, verbunden.
2. In der Oberfläche prüfen: **5600 ist in der Auswahl nicht vorhanden**, freie Eingabe gibt es nicht.
3. Warteschlangendatei erzeugen (eine Messung mit `test_5000Hz.set`, beliebige Bandbreite speichern),
   im Texteditor `"fft.bandbreite_hz"` auf `5600.0` ändern und laden. Erwartung: im Editor steht
   „5600 (keine PSV-Stufe)“ mit Fehler; **Start ist gesperrt** mit Meldung „Bandbreite 5600 Hz ist keine
   PSV-Stufe (Stufen: …)“. Es wird nichts an PSV geschrieben.

## 2. T2-Fall 4000 Hz (keine Stufe)

Wie Abschnitt 1 mit `4000.0`. Erwartung identisch (kein Aufruf an PSV, Start gesperrt). Kommt
4000 Hz in der Stufenliste aus Abschnitt 0 vor, ist das ein Befund (dann gilt: 4000 Hz ist eine
Stufe und PSV lehnt sie am 23.11. aus anderem Grund ab; Ergebnis des Trockenlaufs aufschreiben).

## 3. T2-Fall 6250 Hz (Stufe), Mittelung 5

1. Eine Messung mit `test_5000Hz.set`, Bandbreite **6250** aus der Auswahlliste, Mittelung Anzahl 5.
   Durchgangsname frei, Trockenlauf starten.
2. Erwartung (Soll aus den Entscheidungen, am Gerät unbestätigt): Messung `fertig`.
3. Im Messprotokoll (`<Durchgangsordner>\*.protokoll.json`, Messdatei-Basisname wie in der Tabelle der
   Oberfläche) prüfen:
   - `geaenderte_parameter` enthält drei Zeilen: `fft.bandbreite_hz` (soll 6250, ist 6250),
     `fft.start_frequenz_hz` (soll 0, ist 0), `fft.end_frequenz_hz` (soll 6250, ist 6250).
   - `einstellungen_ist.gruppen.fft`: `bandbreite_hz` 6250, `start_frequenz_hz` 0, `end_frequenz_hz` 6250
     (am 23.11. stand dort 5000), `linien` 400, `abtastfrequenz_hz` 15625 (2,5 mal Bandbreite, Nicht-M-System,
     vgl. I5 2.5), `aufloesung_hz` 15,625 (Bandbreite / Linien).
4. In PSV nachsehen: FFT-Einstellung „Von“ = 0, **„Bis“ = 6,25 kHz** (am 23.11. blieb „Bis“ bei 5 kHz).
   Nur ansehen, nichts ändern.

## 4. Wenn etwas nicht passt (Fehlerfälle, alle fail-closed)

Die Software zeigt in jedem dieser Fälle einen Fehler mit der Strategie „Pausieren und nachfragen“
(Wiederholen / Überspringen / Abbrechen); es wird kein Scan gestartet.

| Beobachtung | Bedeutung | Zu sichern |
|---|---|---|
| Fehler „Abweichung beim Frequenzbereich (Von/Bis)“, `fft.end_frequenz_hz`: Ist ≠ Soll | PSV hat „Bis“ nicht übernommen | `*.protokoll.json` (steht trotzdem komplett im Protokoll), Foto/Text der PSV-FFT-Einstellung |
| Gerätefehler beim Setzen (z. B. „Ungültiger Wert“, HRESULT) | PSV lehnt Bandbreite oder Von/Bis im Validator ab | Fehlertext aus Protokoll und Ereignisprotokoll (`durchgang.ereignisse.jsonl`), Wert, bei dem es auftrat |
| „Bandbreite … ist keine PSV-Stufe“ aus dem Gerät | Stufenliste beim Setzen weicht von der beim Verbinden ab | beide Listen notieren |
| „Stufenliste nicht lesbar“ | `AvailableBandwidths` nicht lesbar oder unerwartete Form | vollständiger Text |

Bei einem Fehler in Abschnitt 3 zusätzlich notieren: Welche Bandbreite war vorher in PSV eingestellt
(5000 Hz aus der `.set`)? Eine mögliche Ursache ist die Schreibreihenfolge (Bandbreite vor Bis); eine
Änderung daran ist erst nach Rückmeldung dieser Befunde vorgesehen.

## Ergebnis eintragen

Für jeden Abschnitt 0 bis 3: Beobachtung (Zahlen, Texte), Protokolldatei, „bestanden / Befund“ als
Entscheidung von Jakob. Danach `/laborbuch`; erst dann gilt der Stand „am Gerät bestätigt“.
