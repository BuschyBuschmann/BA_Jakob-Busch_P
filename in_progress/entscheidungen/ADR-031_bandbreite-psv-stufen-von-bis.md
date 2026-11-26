# ADR-031: Bandbreite nur als PSV-Stufe, Von/Bis mitsetzen, Rückprobe fail-closed

**Datum:** 2026-11-26 · **Status:** angenommen
**Bezug:** R-001, R-011, R-023; O1; K-U2b; Laborbuch 2026-11-23_messrechner-com-trockenlauf (T2) und 2026-11-26_bandbreite-psv-stufen; Pakete BW-1 bis BW-9

## Kontext
Im Trockenlauf T2 am 23.11. (PSV 10.4) übernahm PSV 5600 Hz still nicht (zurückgelesen 5000 Hz), lehnte 4000 Hz mit „Ungültiger Wert“ ab und ließ bei 6250 Hz „Bis“ auf 5000 Hz stehen. Die Software schrieb bis dahin nur `Bandwidth` und `Lines`, nie `StartFrequency`/`EndFrequency`.

## Betrachtete Alternativen
| Alternative | Vorteile | Nachteile |
|---|---|---|
| Einrasten des Geräts hinnehmen (bisher) | kein Aufwand | Messung mit anderem Bereich als eingestellt möglich |
| Feste Stufenliste im Code bzw. in `konfig.json` | ohne Verbindung verfügbar | kann von Gerät und .set abweichen, Pflegeaufwand |
| Stufen zur Laufzeit aus PSV (`AvailableBandwidths`) | passt zu Gerät und .set | erst am Gerät prüfbar, ohne Verbindung keine Liste |
| Von/Bis frei je Messung einstellbar | Zoom-Bereiche möglich | neue Funktion und Eingabe, nicht verlangt |

## Entscheidung
Entscheidung des Nutzers (2026-11-23):
- Zulässige Bandbreiten kommen zur Laufzeit aus PSV (`AvailableBandwidths`); die Oberfläche bietet nur diese Stufen als Auswahlliste an, ohne Verbindung ist die Auswahl gesperrt („Erst mit PSV verbinden“). Ist die Liste nicht lesbar, gibt es keine Ersatzliste (fail-closed).
- Beim Setzen der Bandbreite werden Von = 0 und Bis = Soll-Bandbreite im Validator mitgesetzt (Reihenfolge Bandwidth, Lines, StartFrequency, EndFrequency, Übernahme).
- Bandbreite, Von und Bis werden zurückgelesen (Toleranz `REL_TOL_ZURUECKLESEN` = 1e-9 relativ, absolut 0); eine Abweichung ist ein Fehler nach O1, kein Scan.
- Warteschlangen mit Nicht-Stufen lassen sich laden, der Start ist gesperrt. Messprotokoll bleibt bei Schema 2.
- Ein Zeitlimit beim Nachlesen nach einem Fehler gilt nach K-U2b als Hänger (Entscheidung 2026-11-25).

## Begründung
Belege aus T2 (23.11.); fail-closed verhindert, dass still mit einem anderen Bereich gemessen wird. Bis = Soll statt zurückgelesener Bandbreite, damit ein anderes Einrasten die Rückprobe auslöst.

## Konsequenzen
- Ohne Validator (Rückfall S4) wird die Bandbreite nicht mehr gesetzt.
- Am Gerät unbelegt: Lesbarkeit und Form von `AvailableBandwidths`, Annahme von Start/EndFrequency im Validator, Verhalten bei Bis größer als neue Bandbreite. Prüfanleitung `in_progress/versuche/2026-11-23_messrechner/pruefanleitung_bandbreite.md`; vor jeder echten Messung durchzuführen.
- Thesis: 4.2 (Ansteuerung), 5.4 (Grenzen der Schnittstelle).
