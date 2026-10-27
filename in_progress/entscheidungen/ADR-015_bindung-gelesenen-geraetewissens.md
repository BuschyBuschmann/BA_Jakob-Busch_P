# ADR-015: Bindung gelesenen Gerätewissens an seine Herkunft

**Datum:** 2026-10-27 · **Status:** angenommen
**Bezug:** Paket U5 (Integration), Review R-U5/RR-U5; Laborbuch `in_progress/laborbuch/2026-10-27_u5-integration.md`; Entscheidung des Nutzers vom 2026-10-27; Plan P2 Abschnitt 6

## Kontext
Der Startdialog zeigt je Messung Messpunkte und Generatorzustand, die nach dem Laden einer `.set` vom Gerät gelesen wurden. In der ersten Umsetzung galt dieses Wissen auch nach einem Gerätewechsel weiter; Simulatorwerte erschienen dadurch als „gelesen: aus“ für das echte Gerät (Review R-U5, BLOCKER). Ein aktiver Generator in einer `.set` hätte so keine Warnung ausgelöst.

## Betrachtete Alternativen
| Alternative | Vorteile | Nachteile |
|---|---|---|
| Wissen nur an die `.set` gebunden | einfach | falsche Entwarnung nach Gerätewechsel |
| Wissen verfällt bei jedem Gerätewechsel | sicher | in MESSEN immer „unbekannt“, rote Warnung verliert ihre Wirkung |
| Übernahme nur COM → COM bei gleichem PSV-Prozess, gleicher Lademaske und unveränderter `.set` | sicher und aussagekräftig | Regel komplexer; bei selbst gestartetem PSV keine Übernahme |

## Entscheidung
Gelesenes Wissen trägt seine Herkunft (Gerät, Betriebsart, Lademaske, PSV-Prozesstreffer). Es gilt für das verbundene Gerät, wenn es dasselbe ist oder beide COM-Geräte mit gleichem nicht-leerem Prozesstreffer, gleicher Lademaske und unveränderter `.set` sind. Simulatorwissen gilt nie für ein COM-Gerät. Bei Trennen, GERAET_UNKLAR, verlorenem Gerät und fehlgeschlagener Erzeugung verfällt es.

## Begründung
Entscheidung des Nutzers nach Abwägung; im Re-Review RR-U5 an den Gegenbeispielen nachgeprüft.

## Konsequenzen
Am Montag vor MESSEN einen Trockenlauf mit derselben `.set` ohne PSV-Neustart; sonst Generator von Hand prüfen. Ob die Standard-Lademaske den Generator aus der `.set` mitlädt, ist am Gerät zu klären (T2).
