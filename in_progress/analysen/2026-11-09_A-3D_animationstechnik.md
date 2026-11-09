# A-3D: Darstellungstechnik der 3D-Animation (OE-A1) – Entscheidungsvorlage

Analyse `software-engineer` (sonnet), 2026-11-09, read-only (Repo unverändert, `pyproject.toml`/`uv.lock` unverändert). Bezug: Design-Brief K1-AUSW2 (R-071, UI-22 bis UI-33, OE-A1/OE-A2), FG-04 (Entwurf), ADR-021, ADR-024, ADR-025.
Kennzeichnung: **[G]** selbst gemessen bzw. geprüft (Scratchpad `/tmp/claude-0/-home-user/e6b61297-17fb-5003-91f8-95c4534d012c/scratchpad/a3d/`), **[R]** recherchiert (PyPI-Metadaten 2026-11-09, Websuche), **[A]** Annahme, **[offen]** am Messrechner zu prüfen.

## 1 Messaufbau und Grenzen der Messung

- Umgebung [G]: Linux (Cloud, 4 vCPU), CPython 3.11.17, numpy 2.4.6, matplotlib 3.11.2, PySide6 6.11.3, pyqtgraph 0.14.0, PyOpenGL 3.1.10, pyvista 0.49.2, pyvistaqt 0.13.2, vtk 9.7.2. OpenGL: Mesa **llvmpipe** (Software, OpenGL 4.5), also Software-Rendering, aber **nicht Windows**.
- Last [G]: Geometrie aus `Input/20261012_ref_Mitte.svd` (135 Punkte, 112 Vierecke, Fläche 0,20 m × 0,48 m, annähernd eben). Die komplexen Amplituden stammen aus Linie 300 der Datei (Spalten CPH M0/M4/M5, **nur als Lastprofil, die Zuordnung zu X/Y/Z ist hier nicht fachlich geprüft**), Auslenkung = v̂/(iω), Überhöhung nach FG-04 3.5 (α = 0,25), 36 Phasenbilder.
- Je Bild: Positionen und Farben neu setzen, dann voll zeichnen. Median von 30 bis 40 Wiederholungen (Min/Max in den Rohdaten der Skripte). Absolute Zeiten übertragen sich **nicht** auf den Messrechner; sie taugen für den Vergleich der Techniken untereinander und als Obergrenze der Rechenarbeit [A].

## 2 Messwerte

| Technik (Szenario, Linux, Software-GL) | Zeit je Bild (Median) | entspricht |
|---|---|---|
| (a) mplot3d, `Agg`, 800×600/1280×800, nur Punkte, Punkte + 112 Flächen, nur Flächen | 46 bis 51 ms (alle Varianten innerhalb der Streuung) | ca. 20 Bilder/s |
| (a) dasselbe, Drehschritt (`view_init` + `draw`) | 37 bis 51 ms | ca. 20/s |
| (a) in `FigureCanvasQTAgg` (Qt offscreen): Bildwechsel + `draw` + `grab` | 53 ms | ca. 19/s |
| (a) echtes Maus-Ziehen (QTest, Qt offscreen): Bewegung bis sichtbares Neuzeichnen | 53 ms (42 bis 66) | ca. 19/s |
| (a) Achsen/Panes aus (`set_axis_off`) | 20 ms | ca. 50/s |
| (a) nur Tick-Texte aus | 33 ms | |
| (c) eigene Projektion in matplotlib-2D (`PolyCollection` + `scatter`), voll | 33 ms | ca. 30/s |
| (c) dasselbe mit Blitting (nur Daten) | 5 ms | ca. 200/s |
| (b1) pyqtgraph.opengl, Bild + Framebuffer lesen (`xcb` unter Xvfb) | 2,8 ms | > 300/s |
| (b2) PyVista offscreen, `Render()` (EGL/llvmpipe) | 18 bis 20 ms | ca. 50/s |
| (b2) PyVista offscreen, Render + Pixel lesen | 23 ms | |
| (b2) pyvistaqt `QtInteractor` (PySide6 6.11.3, `xcb`/Xvfb) inkl. Qt-Ereignisse | 50 ms | ca. 20/s |

Befunde aus den Zahlen [G]:
1. mplot3d ist **unabhängig von der Punkt- und Flächenzahl** dieser Größenordnung: Etwa die Hälfte der Zeit entfällt auf Achsen, Panes und Tick-Texte (voll 43 ms, Achsen aus 20 ms). Während Wiedergabe und Drehen lässt sich also mit vereinfachten Achsen auf rund 20 ms kommen; das Stillstandsbild bleibt vollständig.
2. Die GPU-Techniken sind bei **Software-GL** schneller, aber die PyVista-Variante in Qt (50 ms) ist nicht schneller als mplot3d; die Zeit liegt dort bei Qt/X-Transfer und Fenster-Compositing, nicht im Rendern.
3. Referenzzähler von `None` über 1000 Bilder mit PySide6 6.11.3 (Regressionsthema ADR-001/A-PLOT): matplotlib/Qt, pyqtgraph.opengl und pyvistaqt je **0** (nach `gc.collect()`; ohne `gc` zeigte matplotlib +721 durch noch nicht gesammelten Zyklenmüll, kein Leck).
4. Importzeit (kumulativ, kalt): `mpl_toolkits.mplot3d` 0,34 s (matplotlib ohnehin geladen), `pyqtgraph.opengl` 0,45 s, `pyvista` 0,29 s, `pyvistaqt` 0,94 s.

## 3 Bewertung je Alternative

### (a) matplotlib `mplot3d` in `Figure` + `FigureCanvasQTAgg` (innerhalb ADR-021)
- **Leistung** [G]: 40 bis 55 ms je Bild voll, 20 ms mit vereinfachten Achsen. Für Drehen per Maus ruckelig-flüssig (ca. 20 Bilder/s), für Wiedergabe mit einstellbarer Bildrate (UI: „Bildrate begrenzt und einstellbar“) ausreichend. Drehen und Abspielen schließen sich im Brief ohnehin aus (Wiedergabe pausiert beim Drehen).
- **Remotedesktop**: Zeichnung ist CPU-Rendering (Agg) und braucht **kein OpenGL**; damit ist sie von der GL-Lage in der RDP-Sitzung unabhängig [G, Architektur]. Übertragen wird ein Bitmap-Bereich; die Bandbreite und der Eindruck am Messrechner sind **[offen]** (U-A2).
- **Lizenz**: matplotlib-Lizenz (PSF-artig), bereits Hauptabhängigkeit. Keine neue Abhängigkeit, **keine Wheelhouse- oder Größenänderung** (matplotlib 3.11.2 ist bereits in `PINS`); `mpl_toolkits` liegt im selben Wheel [G].
- **Abhängigkeit zu PySide6 6.11.3**: unverändert wie ADR-021; Qt-Referenztest bestanden (Befund 3).
- **Thesis-Standbild / UI-33** [G]: dieselbe Zeichenfunktion füllt eine übergebene `Figure` (`fig.add_subplot(projection="3d")`), ohne Qt und ohne `pyplot`; PNG und **PDF (Vektor)** gehen direkt (Probe: `standbild_a.png/.pdf`, PDF 30 KB; Farbleiste, Legende der gekennzeichneten Punkte als Kreuz/Raute, Stempelzeile mit Phase, Überhöhung, Frequenz und „⚠ unbestätigt (M8)“ waren ohne Zusatz zeichenbar). Damit bleibt ADR-024 (gemeinsame Zeichenschicht) gewahrt und UI-33 ist erfüllt, ohne Abweichungs-ADR.
- **Graustufen** [G]: Die Farbskala ist ein matplotlib-`Colormap`-Objekt, jede Helligkeitstrennung der divergierenden Skala (Entscheidung `ui-designer`) ist möglich; Probe in Graustufen (`standbild_a_grau.png`) zeigt Vorzeichen über Helligkeit und Punktformen (Kreuz, Raute) unabhängig von Farbe.
- **Testbarkeit offscreen**: voll (Agg, ohne GL); Zeichenfunktion Qt-frei im Standardlauf testbar, Widget unter `pytest -m gui` wie bisher [G].
- **Grenzen** (Merkpunkte für Umsetzung):
  - Typisierung: `mpl_toolkits.mplot3d` hat keine Typinformationen; `mypy --strict` meldet `import-untyped` [G]. Nötig wäre ein `[[tool.mypy.overrides]]` mit `ignore_missing_imports` wie bei `olefile` (kleine Konfigurationsänderung, die der Umsetzer begründen muss).
  - Mausbedienung eingebaut: links drehen, Mitte verschieben, rechts zoomen; **Mausrad-Zoom und Tastatur (Pfeile, `+`/`-`, Pos1) nicht** [G, Quelltext]. Beides ist eigener Code über `scroll_event`/`key_press_event` bzw. Qt-Tastenereignisse (`set_box_aspect(..., zoom=)` und `view_init` sind öffentliche API).
  - Tiefensortierung arbeitet je Artist/je Fläche, nicht je Pixel; bei flachen Prüflingen mit kleiner Auslenkung unkritisch, bei streifender Sicht und bei Punkten über der Fläche möglich fehlerhafte Überdeckung (`computed_zorder=False` mit fester Zeichenreihenfolge in der Probe unauffällig) **[A, Sichtprüfung nur an einer Ansicht]**.
  - Z-Skalierung: Bei Auslenkungen von 1e-4 bis 1e-3 des Prüflings muss die z-Achse bewusst gestreckt bzw. an die überhöhte Auslenkung gebunden werden (Überhöhung steht als Zahl im Bild), sonst wirkt die Schwingform flach [G, Probe]. Gestaltungsfrage für `ui-designer`.
  - Tick-Beschriftung der 3D-Achsen überlappt bei Standardeinstellung; mit eigenen Ticks lesbar [G].
- **Aufwand** [A]: klein bis mittel (ein neues Darstellungsmodul, Maus-/Tastaturanbindung, Phasen-Teilaktualisierung).

### (b1) pyqtgraph.opengl (`GLViewWidget`)
- **Leistung** [G]: 2,8 ms je Bild; mit Abstand schnellste Technik.
- **Remotedesktop** [R]: Braucht ein echtes OpenGL-Widget (`QOpenGLWidget`) und PyOpenGL mit **OpenGL ≥ 2.1** (eigene Prüfung in `initializeGL`, Fehlermeldung sonst). In Remotedesktop-Sitzungen liefert Windows ohne GPU-Richtlinie nach Websuche nur die Software-Implementierung „GDI Generic“ mit OpenGL 1.1; die Gruppenrichtlinie „Use the hardware default graphics adapter for all Remote Desktop Services sessions“ ändert das (nicht in Windows Home) – Quellen nur Dritthersteller und Foren, keine Microsoft-Seite abgerufen. Qt-Rückfall: Der PySide6-Windows-Wheel enthält `opengl32sw.dll` (Mesa-Software-GL, 20,6 MB entpackt) [G, Wheel-Inhalt geprüft]; dass und wie Qt sie in einer RDP-Sitzung automatisch wählt oder per Einstellung (`QT_OPENGL=software`) erzwungen werden muss, ist **[offen]**.
- **Lizenz**: pyqtgraph MIT [R]; PyOpenGL BSD-Klassifikator [G]; `colorama`-Abhängigkeit.
- **Wheel/Größe** [R]: pyqtgraph 1,92 MB + PyOpenGL 3,19 MB (+ `colorama` 0,03 MB), reine Python-Wheels (`py3-none-any`), Zuwachs ca. **5,2 MB**.
- **Abhängigkeit zu PySide6 6.11.3** [G]: läuft mit 6.11.3; Referenztest 0. A-PLOT hatte für pyqtgraph (2D) einen unerklärten Zuwachs (+10 985) gemessen; für `pyqtgraph.opengl` hier nicht reproduziert (Eigenbau-Messung, anderes Modul).
- **Thesis-Standbild / UI-33**: keine Zeichenfunktion für eine `Figure`; Standbild nur als Pixelbild (`grabFramebuffer`). Farbleiste, Achsenbeschriftung, Legende und Stempel gibt es nicht und müssten gebaut werden; Thesis-Abbildung brauchte eine **zweite Zeichenfunktion** (matplotlib) oder Einbettung des Pixelbilds. Widerspricht der gemeinsamen Zeichenschicht ADR-024 und UI-33 (Abweichungs-ADR nötig). In der Probe erschien die Fläche ohne Shader einfarbig grau (Vertexfarben nicht angewandt), die Farbdarstellung bräuchte also zusätzliche Arbeit (Shader/Farbpuffer).
- **Typisierung** [G]: keine `py.typed`; `mypy --strict` meldet `import-untyped`.
- **Testbarkeit offscreen** [G]: Mit `QT_QPA_PLATFORM=offscreen` meldet Qt „QOpenGLWidget is not supported on this platform“ und es gibt **keinen Framebuffer**; ein Test braucht die `xcb`-Plattform mit Xvfb sowie Systembibliotheken (`libxcb-cursor0`, `libxcb-icccm4`, `libxcb-image0`, `libxcb-keysyms1`, `libxcb-render-util0`, `libxcb-util1`, `libxcb-xkb1`, `libxkbcommon-x11-0`; im Sandbox-Container nachinstalliert). Der Standard-GUI-Testlauf der Cloud (`offscreen`) kann das Widget nicht prüfen; zusätzlich schlägt `fmt.version()` in `offscreen` in einer eigenen Prüfung fehl, solange kein Formatwunsch (≥ 2.1) gesetzt ist [G].
- **Aufwand** [A]: mittel bis groß (Netz, Farbleiste, Beschriftung, Fokus/Tastatur, Standbild und Stempel, zweite Zeichenfunktion, Xvfb-Tests, ADR, Wheelhouse).

### (b2) PyVista / pyvistaqt (VTK, OpenGL)
- **Leistung** [G]: 18 bis 20 ms Render (EGL, auch ohne X-Server), 50 ms im `QtInteractor` mit Qt-Ereignissen; kein Vorteil gegenüber (a) im Widget.
- **Remotedesktop** [R]: VTK 9 verlangt OpenGL **3.2**; unter RDP mit nur „GDI Generic“ (1.1) startet das Renderfenster nicht (Berichte in der VTK-Nutzerliste und bei PyVista; Abhilfe: Mesa-Software-DLLs, GPU-Richtlinie oder anderes Fernwartungswerkzeug). Auf dem Messrechner **[offen]**, hohes Risiko im Vergleich zu (a).
- **Lizenz** [R]: vtk BSD, pyvista MIT, pyvistaqt MIT, qtpy MIT, übrige MIT/BSD/Apache/MPL-2.0 (certifi) – unkritisch.
- **Wheel/Größe** [R]: `vtk-9.7.2-cp311-win_amd64.whl` 80,4 MB (am 2026-11-03 erschienen, also sehr jung); mit 21 weiteren reinen Python-Wheels (pyvista 2,73 MB, pygments 1,25 MB, rich, cyclopts, requests, pooch, qtpy, scooby, pyvista-validation u. a.) Summe **ca. 86,4 MB** zusätzlich im Wheelhouse (heute ca. 77 MB PySide6 + 19 MB matplotlib-Anteil usw.). Entpackte Größe unter Windows **[offen]** (Linux-Wheel entpackt 564 MB in `vtkmodules` [G]). Zusätzlich müssen `PINS` und der Test `test_wheelhouse_pins.py` um etwa 22 Einträge erweitert werden.
- **PySide6 6.11.3** [G]: `pyvistaqt.QtInteractor` lief mit `QT_API=pyside6` und 6.11.3 (xcb/Xvfb); Referenztest 0. `qtpy` ist eine zusätzliche Vermittlungsschicht.
- **Thesis-Standbild / UI-33**: Standbild als Pixelbild (`screenshot`), Vektorexport nur eingeschränkt; Beschriftung, Legende, Stempel in VTK-Mitteln oder als Einbettung des Rasterbilds in eine matplotlib-`Figure` (Hybrid). `darstellung/` bleibt dann für die Oberfläche nicht gemeinsam nutzbar (Abweichungs-ADR nötig); die Phasendarstellung nach ADR-025 bleibt in matplotlib, die Schwingform bekäme einen zweiten Weg.
- **Typisierung** [G]: `pyvista`, `pyvistaqt`, `vtkmodules`, `qtpy` führen `py.typed`; ein kleines Beispiel bestand `mypy --strict`.
- **Testbarkeit offscreen** [G]: Rendern ohne Fenster geht auch ohne X-Server (EGL/llvmpipe); das Widget (`QtInteractor`) lief nur unter `xcb` mit Xvfb und den oben genannten Systembibliotheken, nicht unter `offscreen`.
- **Funktionsumfang**: Orbit, Zoom, Kameraansichten, Farbleiste und 3D-Achsen sind eingebaut; bei Bedarf der „vollwertigste“ 3D-Betrachter.
- **Aufwand** [A]: mittel bis groß (neue Großabhängigkeit, Wheelhouse, ADR, Fokus/Tastatur im VTK-Interaktor, Standbild/Stempel, Xvfb-Tests, RDP-Risiko).

### Weitere Variante (c): eigene Orthogonalprojektion in matplotlib-2D
Nicht verlangt, aber als Rückfall im Rahmen von ADR-021 in der Messung enthalten: Rotationsmatrizen in `darstellung/`, Zeichnen als 2D-`PolyCollection` + `scatter`, Drehen und Zoomen per eigener Maus-/Tastaturanbindung. 33 ms voll, **5 ms mit Blitting** [G], dazu keine Tiefensortierungsprobleme des mplot3d (eigene Sortierung nötig), aber **kein eingebauter 3D-Rahmen/Achsen** (Eigenbau, Aufwand mittel). Sinnvoll nur, falls (a) auf dem Messrechner zu langsam ist.

## 4 Gegenüberstellung

| Kriterium | (a) mplot3d | (b1) pyqtgraph.opengl | (b2) PyVista/VTK |
|---|---|---|---|
| Zeit je Bild [G, Linux/SW-GL] | 40–55 ms (20 ms mit einfachen Achsen) | ca. 3 ms | 18–20 ms (50 ms im Qt-Widget) |
| Läuft in RDP ohne GPU-Richtlinie | ja (CPU, kein GL) | **[offen]**, GL ≥ 2.1 nötig; Qt-Software-GL im Wheel | **[offen]**, GL ≥ 3.2 nötig, Risiko hoch [R] |
| Neue Abhängigkeit | nein | ja (ca. +5 MB) | ja (ca. +86 MB, 22 Pakete) |
| Lizenz | wie bisher | MIT/BSD | BSD/MIT |
| Windows-x64/cp311-Wheel | vorhanden (bereits gepinnt) | reine Python-Wheels | vtk-Wheel vorhanden (cp311, win_amd64) |
| Gemeinsame Zeichenfunktion für Thesis (UI-33, ADR-024) | **ja**, Vektor-PDF | nein | nein/Hybrid |
| `mypy --strict` | Override nötig | Override nötig | ohne Override |
| Offscreen-Test in der Cloud | ja (`offscreen`) | nur `xcb`+Xvfb+Systembibliotheken | Render ja; Widget nur `xcb`+Xvfb |
| Mausrad/Tastatur | eigener Code | eingebaut: Maus; Tastatur eigener Code | Maus eingebaut; Tastatur eigener Code |
| Aufwand [A] | klein bis mittel | mittel bis groß | mittel bis groß |

## 5 Empfehlung

**(a) matplotlib `mplot3d` hinter der bestehenden Schnittstelle (ADR-021/ADR-024), mit vereinfachten Achsen während Drehen und Wiedergabe.**

Begründung:
1. Die gestalterischen Muss-Anforderungen sind erfüllbar: Drehen per Maus, Zoom, voreingestellte Ansichten, Graustufentauglichkeit, Kennzeichen M8, Standbild gleich Zustand der Animation (dieselbe Zeichenfunktion), PNG/PDF mit Stempel (UI-31). Die eigentlichen Entscheidungsgrößen für den Nutzer sind Tempo und RDP-Eignung.
2. Das Tempo (ca. 20 Bilder/s voll, ca. 50/s mit einfachen Achsen auf dem Cloudrechner) liegt für eine Betriebsschwingform von 135 Punkten im vertretbaren Bereich; ob es **am Messrechner über Remotedesktop** reicht, ist offen (U-A2, UI-38).
3. Das RDP-Risiko ist bei (a) systembedingt am kleinsten, weil kein OpenGL gebraucht wird. Bei (b1) und besonders (b2) kann die Remotesitzung die Technik ganz verhindern bzw. nur mit Software-GL oder Gruppenrichtlinie laufen lassen – genau dort, wo der Nutzer überwiegend arbeitet.
4. Keine neue Abhängigkeit, kein Wheelhouse-Zuwachs, UI-33 ohne Abweichungs-ADR, ein Zeichenpfad für Oberfläche und Thesis.

Rückfallebenen, in dieser Reihenfolge:
1. **Einzelschrittbetrieb ohne Wiedergabe (OE-A2)**: Phasenregler und ←/→ mit einmaligem Neuzeichnen beim Loslassen (ca. 50 ms je Schritt [G]); alle Aussagen bleiben zugänglich (UI-32).
2. Wiedergabe mit gedrosselter Bildrate und vereinfachten Achsen (Ticks/Panes ausgeblendet) während der Bewegung.
3. Variante (c) (eigene 2D-Projektion mit Blitting, 5 ms) innerhalb ADR-021, falls Drehen am Messrechner zu zäh ist.
4. Erst danach eine GL-Bibliothek, dann bevorzugt (b1) wegen Größe und Geschwindigkeit; (b2) nur, wenn Größe (86 MB) und GL-3.2-Pflicht am Messrechner geklärt sind.

**Zu prüfen am Messrechner (Hardwaretest, nie vorab als bestanden melden):** Zeit je Bild und Drehschritt von (a) über Remotedesktop mit der Beispieldatei; Lesbarkeit; falls (b) erwogen wird, `GL_VERSION`/`GL_RENDERER` in der RDP-Sitzung (GDI Generic 1.1, Basic Render Driver oder Hardware) und ob `QOpenGLWidget` ohne Eingriff startet.

## 6 Offene Punkte

- [offen] Absolute Zeiten und Bandbreite über Windows-Remotedesktop am Messrechner; ob dort eine Hardware-GL-Richtlinie aktiv ist.
- [offen] Entpackte Größe der VTK-/Windows-Dateien; Verhalten von `opengl32sw.dll` bei Qt-Widgets in der RDP-Sitzung.
- [offen] Fachliche Zuordnung der Spalten (nur Lastprofil benutzt); Datenvertrag für 3D-Amplituden fehlt weiter (FG-04 Abschnitt 7, Beobachtung 2: `SchwingformDaten` trägt nur eine Komponente).
- Quellen [R]: PyPI-Seiten der genannten Pakete (2026-11-09); Websuche zu RDP und OpenGL: Beiträge in Foren und Herstellerseiten (u. a. Khronos-Forum, VTK-Nutzerliste „Remote Desktop and the VTK window“, PyVista-Issues #5105/#2155); keine Microsoft-Dokumentation abgerufen.
