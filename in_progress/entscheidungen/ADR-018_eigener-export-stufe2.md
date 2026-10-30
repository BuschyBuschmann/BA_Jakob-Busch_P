# ADR-018: Eigener Exportweg für Stufe 2 der Auswertung

**Datum:** 2026-10-30 · **Status:** angenommen
**Bezug:** R-053, R-054; FG-03 Abschnitt 6; Paket W5-2; KONVENTIONEN.md (Messdaten)

## Kontext
Stufe 2 liefert neue Ergebnisse (Modenfit je Punkt, Drift, 3D-Bezug) und neue Annahmen (M12–M15).
Der Export der Stufe 1 (npz + JSON mit SHA-256, Git-Hash, Herkunft) ist fertig, reviewt und
gegen die Datei geprüft.

## Betrachtete Alternativen
| Alternative | Vorteile | Nachteile |
|---|---|---|
| Eigene Formatkennung `…export.stufe2` mit gemeinsamem Schreibweg `schreibe_export`; Annahmen M12–M15 in eigener Klasse `AnnahmenStufe2` | Format und Prüfliste der Stufe 1 bleiben unverändert; Leser weisen falsches Format ab | zwei Exportdateien je Auswertung |
| Stufe-1-Export erweitern, `Annahmen` um M12–M15 ergänzen | eine Datei | ändert Format, Annahmenliste und Tests der bereits abgenommenen Stufe 1 |

## Entscheidung
Stufe 2 schreibt einen eigenen Export mit eigener Formatkennung über den gemeinsamen Schreibweg;
M12–M15 stehen in `AnnahmenStufe2`.

## Begründung
Auftrag W5-2, A4: Stufe 1 bleibt unverändert. Review und Fachabnahme haben das bestätigt.

## Konsequenzen
- Als Konvention in KONVENTIONEN.md (Messdaten) aufgenommen.
- Die JSON-Datei der Stufe 2 ist größer (B-1 je Punkt als Liste, an der Beispieldatei etwa 3,7 MB).
