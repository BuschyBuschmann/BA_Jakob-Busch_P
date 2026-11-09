# 2026-11-09 – Betreuertermin mit Daniel: Vorführung und neue Anforderungen

**Art:** Betreuertermin
**Paket/Bezug:** Lastenheft (neue Anforderungen folgen über `/anforderungs-analyst`); Versuch 2026-11-09 (ausgefallen); Erwartungsmanagement F30
**Commit:** 68bfd96 (Stand der vorgeführten Software: Wheel 0.2.0, Build a0ee2fc)
**Beteiligt:** Jakob Busch, Daniel Alboldt

## Ziel
Stand der Software vorführen und Rückmeldung zu Datenerfassung und Auswertung einholen.

## Vorgehen
- Der geplante Termin am Messrechner fiel aus, weil der Rechner nicht verfügbar war. Versuchsplan 2026-11-09 wurde nicht durchgeführt.
- Vorführung ohne Messrechner anhand von Bildern: Oberfläche im Simulator (Reiter „Messen“ mit leerer Warteschlange, Reiter „Auswerten“ mit der Beispielmessung `20261012_ref_Mitte.svd`) und Thesis-Vorschaubilder (Spektrum, FRF, Spitzen, Schwingform). Eine Ansicht mit gefüllter Warteschlange ließ sich im Simulator nicht erzeugen.

## Ergebnis
Vorgaben von Daniel (laut Jakob alle notwendig, „muss rein“; keine Reihenfolge genannt):

| Nr. | Vorgabe |
|---|---|
| B1 | 2D- und 3D-Abgleich (Alignment) muss in die Software. |
| B2 | Fernzugriff: Remotedesktop reicht; keine eigene Netzsteuerung nötig. |
| B3 | Mitteilung der Software, wenn etwas fertig ist: bevorzugt über Webex, Alternative E-Mail. |
| B4 | Messungen vergleichen, Auswertungen nebeneinanderlegen. |
| B5 | Auswertungen plotten. |
| B6 | Transformation des Koordinatensystems (z. B. bei kugelförmigen Formen das KOS immer in Normalrichtung zur Form). |
| B7 | Animation der Messungen übernehmen. |
| B8 | Visualisierung aus PSV generell übernehmen. |
| B9 | Ausschnitte einfacher darstellen, Achsen entsprechend einstellen lassen. |
| B10 | Recherche: Welche Auswertungsmöglichkeiten gibt es, die anderes als PSV abbilden und sinnvoll sind? |

## Verifikation
Mündliche Vorgaben, Notizen von Jakob. Keine Messung, kein Hardwaretest.

## Probleme und verworfene Ansätze
- Messrechner nicht verfügbar; alle Punkte des Versuchsplans 2026-11-09 (Prüfdateien R/A/B, T4–T6, D2, D3) und der Checkliste bleiben offen.
- Eigene Netzsteuerung der Software (Oberfläche auf anderem PC, Dienst am Messrechner) wurde erwogen und ist laut Daniel nicht nötig (B2).

## Offene Punkte
- Nächster Termin: 12. oder 13.11.2026 (genaues Datum offen).
- Nicht besprochen, weiter offen: maximale Generator-Amplitude (0,04 V), Zeitdaten speichern, Reflexfolie auf dem Impedanzkopf, Waage, Handbücher kopieren, Datum und Befehl der COM-Registrierung, Ort der .set vom 12.10., Datenblatt PCB 288D01, Gliederung (G1–G4), Umfang und Abgabetermin.
- Keine Fristen vereinbart.
- B1–B10 ins Lastenheft aufnehmen (Priorität laut Jakob: alles notwendig); Umfang und Machbarkeit je Punkt klären (z. B. Alignment über COM, Webex-Anbindung).

## Thesis-Bezug
3.4 Anforderungen; 4.2 Ansteuerung (B1, B3); 4.4/4.5 Auswertung und Darstellung (B4–B9); 2 Stand der Technik bzw. 3 Methodik (B10).
