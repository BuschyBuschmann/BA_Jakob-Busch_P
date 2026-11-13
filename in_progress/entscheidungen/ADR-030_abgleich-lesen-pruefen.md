# ADR-030: Abgleich lesen und prüfen (R-003a/b)

**Datum:** 2026-11-13 · **Status:** angenommen (Nutzer, Freigabe Plan P-R003 am 2026-11-09)
**Bezug:** R-003a, R-003b; Plan `in_progress/planung/plaene/2026-11-09_P-R003_abgleich-plan.md` (D1–D8); Analyse A1-B13; ADR-007 (Nachtrag Lesefreigaben), ADR-008, ADR-014

## Kontext
Der Betreuer verlangt den 2D-/3D-Abgleich in der Software (B1). Laut Analyse ist das Auslösen per COM nicht belegt; lesbar sind Gültigkeit und Qualität. Jede `.set` bringt beim Laden ihren eigenen Abgleich mit.

## Betrachtete Alternativen
| Frage | Gewählt | Verworfen |
|---|---|---|
| D1 Schnittstelle | eigenes Protocol `Abgleichsleser` | Methode in `Messgeraet` (bricht alle Fakes), Teil von `EinstellungsStand` |
| D2 Ablage | Pflichtfeld `abgleich` je Messprotokoll | nur Ereignisprotokoll, eigener Warteschlangeneintrag |
| D3 Prüfung | Modus aus/warnen/verweigern, Voreinstellung aus | immer prüfen, nie prüfen |
| D4 Fehlerart | neue `FehlerArt.ABGLEICH` | `VORPRUEFUNG` (Prüfung läuft erst nach dem Laden) |
| D5 Grenzen | optionale Schlüssel der Konfigurationsdatei, ohne Standardwerte | Oberfläche, feste Werte |
| D6 Anzeige | Ereignisprotokoll bei Auffälligkeit | eigenes Widget |
| D7 Zeitpunkt | je Messung nach dem Laden | einmal je Durchgang |
| D8 Whitelist | nur Lesefreigaben `Infos.Alignments…`, `NIE_KATALOG` erweitert | Freigabe von `Calculate` o. ä. |

## Entscheidung
D1–D8 wie empfohlen. Nach Review zusätzlich: nicht endliche Werte und unvollständig gelesene Einträge (mehr als 16) gelten als „nicht prüfbar“ (fail-closed); das Protokollschema bleibt 2 (Wheel 0.2.0 nie installiert).

## Begründung
Keine Bewegung von Laser oder Spiegeln durch die Software; Messung im Modus „aus“ nie blockiert; jede Messung dokumentiert ihren Abgleich.

## Konsequenzen
Neues Pflichtfeld `abgleich` im Messprotokoll; im Modus „verweigern“ führt ein Abgleich mit mehr als 16 Einträgen auch ohne Grenzen zur Fehlerart `abgleich`. Gerätewerte, Einheiten, Indexbasis und „Lesen bewegt nichts“ sind am Messrechner zu prüfen (Prüfanleitung AB1–AB11); R-003c (Auslösen) offen bis zur Klärung mit dem Betreuer.
