# 2026-11-18 – Animation der Schwingform: Datenvertrag, 3D-Zeichenfunktion, Steuerung (R-071, AN3–AN5)

**Art:** Arbeitspaket
**Paket/Bezug:** U-AUSW3-2, K-AUSW3-2, K2-AUSW3-2; R-071; Plan P-AUSW3; FG-04 mit Nachträgen 1–3; ADR-029
**Commit:** e686305 (Stand vor dem Paket-Commit)
**Beteiligt:** software-engineer (sonnet), reviewer (opus, haiku), strukturdynamik-experte (sonnet); Entscheidungen Jakob Busch

## Ziel
Datenvertrag für die 3D-Animation, GUI-freie Zeichenfunktion mit matplotlib mplot3d und Qt-freie Steuerung (Phase, Wiedergabe, Tasten), noch ohne Einbau in die Oberfläche.

## Vorgehen
1. Umsetzung AN3–AN5: `darstellung/animation_daten.py`, `darstellung/animation3d.py`, `gui/animation_steuerung.py`; Importrichtung um `mpl_toolkits` erweitert, mypy-Override.
2. Code-Review (opus) und Fachabnahme: je FREIGABE MIT AUFLAGEN; MAJOR (Fachabnahme): Bei Option „Schnelle“ nannte das Bild einen um ω falschen Überhöhungsfaktor, weil FG-04 die Skalierung dafür nicht festlegte.
3. FG-04 Nachtrag 2 (Skalierung bei Schnelle, räumlicher Punktabstand, Wortlaut θ = 0) vom Nutzer freigegeben; Korrektur 1 mit allen gewählten Befunden (Robustheit, Beschriftung, Farbskala mit neutralem Nullpunkt, Kennzeichen-Rangfolge wie Ansicht 4).
4. Re-Review (haiku): NACHARBEIT NÖTIG – M8/M12 nicht in der Zeichenfunktion erzwungen; nahezu gleiche Punkte verfälschen den Nachbarabstand; Speicher der Abstandsrechnung.
5. FG-04 Nachtrag 3 (Toleranz für doppelte Punkte) vom Nutzer freigegeben; Korrektur 2 (letzte Runde): M8/M12 in der Zeichenfunktion, ×1 bei einem Punkt gekennzeichnet, Duplikatregel, blockweise Abstände.
6. Fachabnahme: FREIGABE; Re-Review (opus): FREIGABE MIT AUFLAGEN (zwei MINOR, ein NITPICK dem Nutzer vorgelegt).

## Ergebnis
Pflichtangaben nach FG-04 3.5 und Nachtrag 2 exakt im Bild; Duplikatregel bitgleich zu einer unabhängigen Referenz (900 Vergleiche); Abstandsrechnung bei 5000 Punkten 33 MiB statt 1335 MiB, 0,35 s statt 1,1 s (Container).

## Verifikation
K2 gemeldet: 2702 passed, Abdeckung 98,50 %, ruff/format/mypy ohne Befund. Re-Review selbst: 696 Tests grün; Fachabnahme: 135 Tests grün und eigene Gegenbeispiele. Cloud-Messwerte (Container): 3 Kanalpaare 163 ms kalt, Bild 57 ms mit Achsen / 33 ms vereinfacht.

## Probleme und verworfene Ansätze
- Erste Fassung zeigte bei „Schnelle“ einen falschen Faktor (Lücke in der Fachgrundlage, durch Nachtrag 2 geschlossen).
- Bericht K-AUSW3-2 gab zu Annahme 3 („Wort statt Sonderzeichen“) Falsches an; im Code steht weiter „×“ (korrigiert festgehalten).

## Offene Punkte
- Leerer Aufrufertext unterdrückt M8/M12; Textalternative nennt bei absolutem Bezug kein M8; M12 nicht an den Annahmenstatus angebunden (dem Nutzer vorgelegt).
- Einbau in die Oberfläche AN6–AN9 (Tasten in `AKTIONS_TASTEN`, Hinweis zu doppelten Punkten, Eingabefeld Skalierung), Design-Abnahme der Kennzeichenkästen.
- Tempo und Lesbarkeit am Messrechner und über Remotedesktop (UI-38).

## Thesis-Bezug
4.4 Auswertung und Darstellung (Animation); 3.3 Betriebsschwingformen.
