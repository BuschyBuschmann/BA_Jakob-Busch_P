# 2026-11-19 – Animation AN7: Einbau in Ansicht 4, M12-Kopplung, Layout der 3D-Abbildung

**Art:** Arbeitspaket
**Paket/Bezug:** U-AUSW3-7, R-AUSW3-7, DA-AUSW3-7, K-AUSW3-7, RR-/DRA-AUSW3-7, K2-AUSW3-7, RR2-/DRA2-AUSW3-7, K3-AUSW3-7, RR3-/DRA3-AUSW3-7; R-071; Plan P-AUSW3 (AN7); ADR-021, ADR-029; FG-04
**Commit:** 2e881a8 (Stand vor dem Paket-Commit)
**Beteiligt:** software-engineer (sonnet), reviewer (opus), ui-designer (sonnet); Entscheidungen Jakob Busch

## Ziel
Animation in Ansicht 4 bedienbar machen (Modusschalter, Bedienleiste, Zustände, Tasten, Kontrast) und das Kennzeichen M12 an den Annahmenstatus koppeln.

## Vorgehen
1. Umsetzung AN7 (durch Nutzungslimit und Container-Neustart unterbrochen; der unfertige Stand war fast vollständig und wurde von einem neuen Aufruf geprüft und abgeschlossen).
2. Review: NACHARBEIT NÖTIG – MAJOR: M12 entfiel bei bestätigtem Status, obwohl die Drehung D ins Geometrie-KS nie angewendet wird (fail-open). Design-Abnahme: NACHARBEIT NÖTIG – Farbleiste überdeckte Pflichtangaben, z-Ticks überlagerten sich. Nutzer: alle Befunde beheben, Farbskala Hellblau–Grau–Braun (#A9D0EC/#8C8C8C/#5A2D0C).
3. Korrektur 1 (13 Befunde): M12 bleibt bei D ≠ I; Status nur mit Vermerk „bestätigt …“ (fail-closed, in der Animation); Cachegröße; Tasten in der Leiste; Farbleiste waagerecht; z-Ticks nach Achslänge; Blickknöpfe in die Leiste; kompakter Kopf. Re-Review FREIGABE MIT AUFLAGEN (Pfeiltasten in Tempo-/Überhöhungsregler), Design-Re-Abnahme: neuer MAJOR – 3D-Bild bei 1100×680 zu klein (ca. 130–230 px).
4. Nutzer: Pfeiltasten nur am Phasenregler umleiten; Status-Regel projektweit als KONVENTION (eigenes Paket nach dem Termin).
5. Korrektur 2: kompakte Stufe, Zoom per Intervallhalbierung; Box bei 1100×680 iso 322×217 px, xy 244×188 px (Ziel 300×200 in xy nicht erreicht, von der Design-Abnahme akzeptiert). Neue Befunde: A5-Bild fiel in die kompakte Stufe (MAJOR), Zoom-Neumessung bei jedem Schritt des Überhöhungsreglers (ca. 230–280 ms), doppelte Zoomsuche.
6. Nach ausgeschöpften zwei Runden entschied der Nutzer eine eng begrenzte dritte Nachkorrektur: kompakt nur bei Bildhöhe < 3,6 in, Zoom erst beim Loslassen des Reglers, eine Zoomsuche je Zeichnen. Re-Review und Screenshot-Prüfung: FREIGABE.

## Ergebnis
Ansicht 4 mit Modus Standbild/Animation, Leiste mit Abspielen, Schritt, Phase, Tempo, Überhöhung, Blickknöpfen; Hinweis zu doppelten Punkten, Skalierungsfeld; 12 Animations-Tasten konfliktfrei; M8/M12 in Kopf, Bild und Textalternative aus einer Quelle. A5-Bild: Box 437×295 px.

## Verifikation
Umsetzer (letzter Stand): ruff, Format, mypy --strict ohne Befund; 2832 passed, Abdeckung 98,36 %; GUI 566 passed im Einzellauf. Ein früherer Fehlschlag von `test_k1_meldung_verschiebt_das_layout_nicht` trat nur bei parallelem Testlauf auf. Orchestrator: ruff, Format, mypy, 195 gezielte Tests grün.

## Probleme und verworfene Ansätze
Ein fehlerhafter Skript-Edit duplizierte `animation3d.py` zeitweise; aus Sicherung wiederhergestellt, Re-Review fand keine Reste. Die erste Layout-Korrektur verkleinerte das 3D-Bild stark; die zweite erfasste A5 ungewollt.

## Offene Punkte
UI-38 am Messrechner; Status-Regel „bestätigt …“ außerhalb der Animation (eigenes Paket); AN8 (Standbild speichern im Animationsmodus, derzeit gesperrt) und AN9; NITPICK: rechter Randpunkt im Format 9×5,6 leicht angeschnitten; xz/yz-Blick: Achse als Punkt mit Tick und Titel übereinander.

## Thesis-Bezug
4.4/4.5 Auswertung und Oberfläche (Animation).
