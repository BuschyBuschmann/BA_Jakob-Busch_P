# Prüfzettel: nächster Termin am Messrechner (Kurzliste zum Abhaken)

Datum: JJJJ-MM-TT · Start ____ · Ende ____ · geplant ca. 240 min **[Annahme, nach Klärung mit Daniel]**; Kurzfall 150 min: Ablaufplan 4.2 · Daniel erreichbar: ja / nein · Anregung freigegeben: ja / nein (Name, Uhrzeit: ________)
Details und Ersatzpläne: [ablaufplan.md](ablaufplan.md) · Ausfüllen: [protokoll.md](protokoll.md)
Priorität: **M** Muss · **S** Soll (Rang nach Fachprüfung: D2 > C2 > E1 > C3 > D3 > E2 > D1 > C4 > X1) · **K** Kann · Voraussetzung: **COM** = PSV-COM nötig, **ANR** = Anregung (Freigabe) nötig, **–** keine
Dauern sind Annahmen. Bei Zeitmangel zuerst Kann streichen, dann Soll von hinten nach vorn; **D2 und E2 nie zusammen** (Ablaufplan, Abschnitt 4).

## Vorher (zu Hause / Entwicklungsrechner)

- [ ] Fragen F1 bis F8 an Daniel gestellt, Antworten notiert (Registrierung, **Anregung**, **längerer Termin z. B. 4 h**, Waage, **Laser auf Kopf und Reflexfolie auf der Stirnfläche**, Internet/Stick, Handbücher, Zeitdaten)
- [ ] Wheel **0.2.0** (Stand nach K-ACHSE) gebaut, gepusht, Git-Hash und SHA-256 notiert; Skripte im aktuellen Stand; Stick gepackt
- [ ] Kandidaten für M11 **am Einzelpunkt** vorab geprüft (ohne Kennzeichen; aussichtsreich 693,5 / 757,3 / 867,9 Hz)? · Namen für Golden File v2 geklärt oder Skript erweitert?
- [ ] SHA-256 der vorhandenen Handbücher notiert
- [ ] Prüfzettel ausgedruckt, Handy/Kamera, Maßband

## Beim Termin: immer

- [ ] **M** (–) **A0 Schritt 0:** `Get-Process PSV` (höchstens 1), **Erkundung Stufe 0 zuerst**, `PSV.AcquisitionInstance` registriert? → ja: Start über **„PSV 10.4 Deutsch“** (`/Acquisition`), **PID notieren**: ______
- [ ] **M** (–) **A1 Update:** neues Wheel 0.2.0 (`pip install --upgrade --no-deps`; `--force-reinstall` nur als Rückfall), Skripte neu, I1 bis I7 (I3: `ldv-automation 0.2.0`), Git-Hash passt (`git_dirty` false). Kurzfall: nur I1 bis I4 + Skripte (ca. 10 min)
- [ ] **M** (–) **A2 Sicherung** (spätestens 30 min vor Ende): Ordner, Protokoll, Fotos, Dateien; PSV sauber; Shaker aus

## Pfad A (COM funktioniert)

- [ ] **M** (COM) B1 Erkundung Stufe 1 (und 1b): Verbinden ok? (nein → Fehlerbild sichern, X1, Pfad B)
- [ ] **M** (COM) B2 Ordner sichern (Durchsicht), Schalter, Konfig-Kopie + SHA-256
- [ ] **M** (–) B3 Test-.set anlegen (Generator aus, Bandbreite ≠ 5600 Hz, Mittelung 3)
- [ ] **M** (COM) B4 T0 · T1 `NUR_LESEN` · T2 `TROCKENLAUF` (Einrastwert bei 5600 Hz notieren)
- [ ] **S** (siehe unten) X1 Desktop-Modus bewusst testen (Rang 9; bei COM-Fehler früh als Diagnose)

## Pfad B (COM aus): zusätzlich oder statt

- [ ] Fehlerbild sichern (Stufe 0/1, HRESULT, Foto), Daniel informieren, Fragen sammeln
- [ ] Simulator-Vorführung (`gui --simulator`, `selbsttest`), **kein** Hardwaretest als bestanden melden
- [ ] Prüfzettel ohne COM weiter (Zweig C, E)

## Prüfzettel-Punkte aus der Übersicht (2a)

Ohne Anregung und ohne COM möglich (an **Kopien**, nie am Original):

- [ ] **S** (–) C2 **M11 an drei Spitzen ohne Kennzeichen** (am Einzelpunkt vorab prüfen; aussichtsreich 693,5 · 757,3 · 867,9 Hz; Hz der korrigierten Achse): Alt+2 → Analysator → Band-Cursor → Cursor-Eigenschaften → Peak-Anpassung (Strg+K autoskalieren); **zwei Bänder je Spitze** (Vielfache von Δf = 0,625 Hz, ≥ 7 Linien, ±2 B und ±4 B); Cursorgrenzen, f max, −3 dB, **Q und ζ mit voller Stellenzahl**
- [ ] **S** (–) E1 **Platte und Impedanzkopf wiegen** (erst **nach** allen Messungen am Aufbau; Fotos vorher; Waage ______; Erwartung Plattenseite 4,5 bis 6,7 kg; Stinger/Shaker nicht)
- [ ] **S** (–) C3 **Golden File v2**: **zuerst H1 Ref2/Ref1** (Phase 0°/180°, m = |F/a| bei 1 bis 6 Hz; sonst Analysator „Ref2 & Ref1“), dann H2, Kohärenz, PSD/ESD, Terzen; **Skalierung notieren** (einseitig, RMS/Spitze, Fensterkorrektur, Terzbasis); Exit-Code notieren
- [ ] **S** (–) E2 **Handbücher 10.4 kopieren** (`C:\Program Files\Polytec\PSV 10.4\Doc`: Theory Manual, Software Handbuch/Manual PSV, Desktop-Varianten, Basic Engine Manual, Release Notes) für `Input/literatur/polytec/`
- [ ] **S** (–) C4 **Generator-Dialog nur ablesen** (Signalform, Burstlänge, Amplitude; nichts ändern)
- [ ] **K** (–) C5 **`einstellungen_lesen.py`:** Werden Eigenschaften fälschlich als „übersprungen (aufrufbar)“ gemeldet? Zeilen notieren
- [ ] **K** (PolyMath-Typbibliothek) B5 **`PolyMath.PeakFit` per COM** mit Testdaten (Fall 1: 700 Hz, ζ 0,01 → Soll 700,0 Hz / 0,0100; Fall 2: 670 Hz, ζ 1,4·10⁻³) und gegen PSV-Fit
- [ ] **K** (–) C6 **UFF-Export** als Gegenprobe; **ATFX und ME'scope wählbar?** (Foto der Formatliste)
- [ ] **K** (–) C7 **File Access bei in PSV geöffneter Datei** (Kopie): Ergebnis/Fehler notieren
- [ ] **K** (–) C8 **Restpunkte:** M13 3D-Abgleich-Achsen + Kopfpositionen, offline |n_z| ≈ 1 · M14 Elementindizes (nur wenn Elemente) · M15 Messzeit gegen Rechneruhr (aus D1)

Mit Anregung (nur nach Freigabe **und** eigener Entscheidung je Messung; Shaker sonst aus):

- [ ] **S, Rang 1** (ANR) D2 **Messpunkt auf dem Impedanzkopf** (Sichtbarkeit max. 10 min prüfen; Reflexfolie nur mit Zustimmung Daniel, sonst **Ersatzpunkt Plattenvorderseite**; Winkel θ, Vib X/Y mit; **Datei speichern**, Wiederholung; SignalDelay Vib/Ref1/**Ref2** vor/nach; Kohärenz notieren). **Erwartung: Vib Z/Ref2 = −90° (v gegen a), gedrehter Ref2 = +90°**; |H1|·ω = 1; Vib Z/Ref1 am Treibpunkt in [−90°, +90°]. Entscheidungstabelle im Ablaufplan
- [ ] **S** (ANR) D3 **Zwei-Amplituden-Test A-B-A 0,02 / 0,04 / 0,02 V** an Label 132 (oder Kopfpunkt); drei neue Dateien, Verstärkerstellung notiert; Ref1-Autospektrum, Kohärenz < 60 Hz
- [ ] **S** (ANR) D1 **Mini-Scan 3×3 mit Zeitdaten** (`SaveTimeDataForScan`; **setzt Signal Enhancement auf „Fast“**: vorher Foto, danach zurückstellen) **plus Referenzscan ohne Zeitdaten**; Scan-Start/-Ende nach Rechneruhr (M15); Dauer, Dateigröße, Lesbarkeit der Zeitdaten
- [ ] **S** (COM teilweise) X1 **Desktop-Modus** einmal bewusst: Start „PSV 10.4 Desktop Deutsch“, Stufe 1, **Fehlerbild notieren**, danach zurück zu Acquisition + Gegenprobe
- [ ] **K** (ANR, nur nach Freigabe: Frage an Daniel; Scandauer ca. 40 min, sonst Folgetermin) D4 **Wiederholungsmessung T8** (gleicher Aufbau, ggf. Raster neu abgeglichen; Temperatur Anfang/Ende)
- [ ] **K** (nur nach Entscheidung, ANR bei T4 ff.) D5 T3 bis T7

## Sicherheit (immer)

- [ ] Echte Messung nur nach **eigener** Entscheidung (Zeit/Grund ins Protokoll)
- [ ] **Shaker/Verstärker aus bzw. Signal getrennt**, bis die Freigabe vorliegt
- [ ] **Rohdaten nie überschreiben**; neue Dateinamen; File Access nur auf **Kopien**
- [ ] Nur **eine** PSV-Instanz; PSV nie per Skript starten; PSV nicht beenden, solange eine Messung läuft
- [ ] Hängt PSV oder steht ein Dialog: **nichts hektisch klicken** (Foto, Skript Strg+C, Daniel), Ersatzplan EP-5
- [ ] Nach jedem Abbruchkriterium keine weiteren Messtests

## Kurzfall: Termin doch nur ca. 150 min

- [ ] A1 kürzen (I1 bis I4 + Skripte), B2 nur soweit für T1/T2 nötig
- [ ] Bei Freigabe der Anregung: **A0, B1, T1, D2 (+ D3 A-B-A am Kopfpunkt)**, dann B3/T2 nach Zeit, E1, E2, A2
- [ ] D4 und D5 auf den Folgetermin

## Ende

- [ ] PSV sauber (keine Messung, kein Dialog), Einstellungen (SE, Generator) zurückgestellt, Shaker aus, Aufbau wie vorher (Foto)
- [ ] Gestrichene Punkte für den Folgetermin notiert: ____________________________
- [ ] Danach `/laborbuch` (Hardwaretest- und Versuchseintrag)
