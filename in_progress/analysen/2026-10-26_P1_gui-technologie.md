<!-- Entscheidungsvorlage P1 (software-engineer, sonnet); unverändert übernommen. -->

## Entscheidungsvorlage GUI-Technologie (Paket P1, Analyse, nichts im Repository geändert)

Empfehlung: **PySide6 (nur `pyside6-essentials==6.12.0`, Widgets) mit dünner Qt-Schicht und GUI-freiem Kern.**

Wichtigste Gegenargumente: Qt hat die größte Lernkurve, bringt etwa 84 MB zusätzliche Wheels mit, und das Testen im Container braucht System-Bibliotheken.
Die schnellste Alternative bis Fr 30.10. ist NiceGUI. Tkinter ist der risikoärmste Weg, aber für die späteren Auswertungen der schwächste.

Alle Zahlen stammen aus Proben im Scratchpad `/tmp/claude-0/-home-user/e6b61297-17fb-5003-91f8-95c4534d012c/scratchpad/p1/`. Was ich nicht geprüft habe, ist jeweils als „Wissen“ oder „ungeprüft“ gekennzeichnet.

### A1 Vergleichstabelle

Gemeinsame Probe: ein GUI-freier Kern (`qtprobe/core.py`) mit Job-Liste, Worker-Thread, Fortschritt per Polling-Nachbau und Pausenpunkt. Er wurde pro Option mit einer dünnen GUI-Schicht und je einem Test betrieben. Dabei wurden Verschieben, Einfügen und Pausenbestätigung während des Laufs geprüft.

| Kriterium | **PySide6 6.12.0** | **Tkinter** (Standardbibliothek) | **NiceGUI 3.18.0** (lokale Weboberfläche) |
|---|---|---|---|
| 1 Warteschlange | Beste Eignung. `QTableView` mit eigenem Model: Statuswechsel per `dataChanged`, `QProgressBar`, `QMessageBox` für Pausenpunkte. Drag-and-drop-Umsortieren ist laut Wissen eingebaut (InternalMove), aber nicht geprobt; programmatisches Verschieben, Einfügen und Sperren fertiger Zeilen im Model geprobt. | Ausreichend. `ttk.Treeview`, `Progressbar` und `messagebox` liefen in der Probe. Es gibt kein eingebautes Drag-and-drop-Umsortieren (Wissen), also Auf/Ab-Schaltflächen oder eigener Code. Anmutung veraltet. | Gut. `ui.table`, `ui.linear_progress` und `ui.dialog` liefen in der Probe. `ui.sortable` oder Ähnliches gibt es in 3.18.0 nicht (per `dir(ui)` geprüft). Umsortieren also über Schaltflächen oder AG-Grid-Zeilenziehen (ungeprüft). |
| 2 Nebenläufigkeit (COM-STA-Worker) | Worker als `threading.Thread`. Ein `Signal`, das aus dem Fremd-Thread emittiert wird, kommt als Queued Connection im GUI-Thread an. In der Probe fehlerfrei: Test lief mit Edit-während-Lauf und Pausenpunkt. Risiken: OLE/COM-Initialisierung von Qt im Hauptthread neben pywin32 (am Rechner prüfen). Signalnamen dürfen nicht `event` oder `thread` heißen, sonst mypy-Konflikt mit `QObject`. | Worker plus `queue.Queue`, im GUI-Thread per `root.after(20, poll)` abgeholt. Probe lief fehlerfrei. Einfachstes Modell, aber Handarbeit. Widgets dürfen nur im Hauptthread angefasst werden. | Der Worker bleibt ein normaler Thread. Die Seite fragt den Kernzustand per `ui.timer(0.05, …)` ab. Probe lief fehlerfrei. Zusätzliche Ebene: Server-Ereignisschleife (asyncio) plus Browser. Zustand liegt im Prozess, nicht im Browser. Mehrere Browser-Tabs sind möglich, also eine Seite pro Sitzung bedenken. |
| 3 Installation Messrechner | Windows-Wheels `cp310-abi3-win_amd64` (laut PyPI-Metadaten Python <3.16, ≥3.10). Mit `pyside6-essentials` + `shiboken6` etwa 84 MB zusätzlich (82,2 + 1,3 MB). **Das Meta-Paket `pyside6` zieht addons (40,5 MB), webengine (131,7 MB) und pdf mit und ist unnötig.** Auf Platte etwa 245 MB. Gesamte Auflösung PySide6 + matplotlib + pywin32 für Windows/3.11: 15 Pakete, 121,8 MB. | Nichts nachzuinstallieren. Der python.org-Installer bringt Tcl/Tk mit (Wissen, nicht geprüft). Das unter Linux verwendete uv-Python lieferte Tk 9.0, die Windows-Version ist nicht geprüft. | Auflösung NiceGUI + matplotlib + pywin32: 61 Pakete (u. a. aiohttp, fastapi, uvicorn, pydantic, orjson), 54,5 MB. Zusätzlich braucht es einen Browser am Messrechner (Edge unter Windows 10 laut Wissen vorhanden, ungeprüft). |
| 3 (Fortsetzung) | Offline-Weg belegt: `pip download --platform win_amd64 --python-version 3.11 --only-binary=:all:` holte `shiboken6-6.12.0` und `pywin32-312-cp311-cp311-win_amd64.whl` (6,9 MB) einwandfrei. Wheelhouse also per USB möglich. Alle Pakete nur als Wheels (`--only-binary :all:` löste auf). Kein Admin nötig, wenn Python per-user installiert ist (Wissen). | wie links | Alle Wheels vorhanden (`--only-binary :all:` löste auf). Läuft sonst wie Qt. |
| 4 Testbarkeit im Container | **Geprobt:** pytest-qt 4.5.0 mit `QT_QPA_PLATFORM=offscreen` lief in 0,4–1,0 s. Voraussetzung: System-Bibliotheken. Ohne `libEGL.so.1` brach schon `pytest_configure` ab. Ich installierte `libegl1 libgl1 libxkbcommon0 libfontconfig1 libdbus-1-3 libglib2.0-0`; die minimale Teilmenge habe ich nicht bestimmt. `mypy --strict`: sauber nach Umbenennung der Signale. Der Befund war meine Namensgebung, nicht Qt. | **Geprobt:** Ohne Display Absturz (`TclError: no display name`). Mit `xvfb-run` lief die Probe. Im System-Python 3.11 des Containers fehlt `tkinter` (Debian-Paket `python3-tk`). Das von uv verwaltete Python hat es. `mypy --strict` sauber. | **Geprobt:** Test mit `nicegui.testing.User` ohne Browser lief in 3,3 s (Seite öffnen, Klick, Dialog sehen, Bestätigung). `mypy --strict` sauber. Kein Display und keine System-Bibliotheken nötig. Echte Browserdarstellung ungetestet. |
| 5 Lizenz, Reife, Lernkurve, KI-Assistent | LGPL-3.0-only OR GPL (PyPI-Metadaten); für eine Bachelorarbeit unkritisch. Sehr ausgereift. Größte Lernkurve (Model/View, Signale). Der KI-Assistent (R-040) passt als Dock-Widget, Netzaufrufe laufen im Thread. | Standardbibliothek, Lizenz kein Thema. Flachste Lernkurve. Für R-040 machbar, aber Chat-Oberfläche mühsam. | MIT. Jünger, schnelle Entwicklung. Für R-040 komfortable Chat-Elemente und asynchrone Netzaufrufe. Abhängigkeit von vielen Webpaketen. |
| 6 Auswertung (Spektren, Schwingformen) | `FigureCanvasQTAgg` rendert offscreen (geprobt). `mypy --strict` meldet 2× `no-untyped-call` (matplotlib-Seite, gezielt zu ignorieren). Für 3D-Schwingformen später pyqtgraph oder PyVistaQt (zusätzliche Abhängigkeiten, ungeprüft). | `FigureCanvasTkAgg` laut Wissen möglich, nicht geprobt. Interaktive 3D-Ansicht schwach. | `ui.matplotlib`/`ui.pyplot`, Plotly für interaktive Spektren und `ui.scene` (three.js) für Schwingformen sind laut Dokumentation vorhanden, nicht geprobt. Für Auswertung am stärksten. |

**Weitere Optionen, nur mit Begründung:**
- **Streamlit 1.66.1** (löst auf, 36 Pakete): nicht empfohlen. Es führt das Skript bei jeder Interaktion neu aus, eine reaktive Warteschlange mit Live-Status und Hintergrund-Worker ist dort ein Fremdkörper (Wissen). Nicht geprobt.
- **pywebview / Dear PyGui / wxPython:** nicht geprüft; zusätzlicher Aufwand ohne klaren Vorteil gegenüber den drei Kandidaten.

### A2 Empfehlung mit Begründung

**PySide6 6.12.0**, installiert als `pyside6-essentials==6.12.0` (zieht `shiboken6==6.12.0`), ergänzt durch `pytest-qt==4.5.0` in der Dev-Gruppe.

Gründe:
- Die Warteschlange (R-010 bis R-018, R-030, R-031) ist mit Model/View am saubersten abbildbar.
- Die Thread-Brücke (Fremd-Thread → Signal → GUI) lief in der Probe fehlerfrei, ebenso der Offscreen-Test samt Edit-während-Lauf (R-016) und Pausenpunkt.
- Es ist eine einzige Desktop-Anwendung ohne Server und Browser neben der PSV-Software. Die matplotlib-Einbettung für Schritt 2 ist belegt.
- Offline-Installation per Wheelhouse ist belegt.

Gegenargumente:
1. **Lernkurve:** Qt ist für den Nutzer am anspruchsvollsten. Das ist für Thesis und Verteidigung relevant, kann aber durch einen kleinen Kern und eine sehr dünne GUI abgefedert werden.
2. **Installationsgröße:** etwa 84 MB zusätzlich. Das Meta-Paket `pyside6` wäre deutlich größer und ist zu vermeiden.
3. **Container:** System-Bibliotheken nötig (libEGL u. a.). Ein Setup-Skript oder SessionStart-Hook muss sie bereitstellen, sonst scheitert pytest-qt.
4. **Termin:** Der Prototyp bis Fr 30.10. ist mit Qt knapper als mit NiceGUI.

**Wann ich NiceGUI vorziehen würde:** wenn der Termin Vorrang hat, ein Browser am Messrechner sicher ist (siehe A4) und die interaktive 3D-/Spektrenauswertung im Web gewünscht wird.
**Wann Tkinter:** nur, wenn Null Installationsrisiko wichtiger ist als Bedienkomfort und Auswertung. Das passt schlecht zu Schritt 2.

Die Entscheidung bleibt beim Nutzer. Wegen der gemeinsamen Kernarchitektur (A3) ist ein späterer Wechsel der Schicht ohne Eingriff in den Kern möglich.

### A3 Konsequenzen für Architektur und Tests (gelten für jede Wahl)

- **Kern (`ldv_automation`, GUI-frei):**
  - Job-Modell, Warteschlange, Zustandsautomat (wartend/läuft/fertig/Fehler, Pause, Abbruch), Runner und Persistenz (R-021) enthalten keinen GUI-Import.
  - Kern und Simulator sind voll testbar und fallen unter die 90 %.
- **Befehle und Ereignisse als neutrale Schnittstelle:** Die GUI ruft Methoden (`insert`, `remove`, `move`, `edit`, `pause`, `resume`, `abort`, `confirm`) und abonniert Ereignisse per Callback. Das Marshalling in den GUI-Thread macht allein die GUI-Schicht (Qt: Signal; Tk: `after` + Queue; NiceGUI: Timer).
- **R-016 (Bearbeiten während des Laufs):** Der Kern schützt die Liste mit einer Sperre und „claimt“ den nächsten Job atomar. Ein Job mit Status `läuft` oder `fertig` ist unveränderlich und wird abgelehnt (Probe: `move` einer fertigen Zeile lieferte `False`). Dafür gehört ein eigener Test mit parallelem Thread in den Kern.
- **Pausenpunkte (R-017):** Der Kern kennt nur ein neutrales `Confirmer`-Protokoll. Die GUI stellt den Dialog, Tests nutzen eine skriptbare Bestätigung.
- **COM-Worker:** Alle COM-Objekte werden im Worker-Thread erzeugt und nie über Threads gereicht. `pythoncom.CoInitialize()` am Beginn, `CoUninitialize()` im `finally`. Fortschritt über Polling von `State` (Polytec-Weg, I5 Abschnitt 5.3), nicht über Events. Das vermeidet eine Nachrichtenschleife im Worker. pywin32 wird nur im Adapter importiert, die GUI-Schicht nie.
- **Dateistruktur:** GUI-Code in einem eigenen Unterpaket (z. B. `ldv_automation/gui/`), `PySide6` als optionale Abhängigkeit `gui` neben `com`.
- **Tests:**
  - GUI-Tests tragen den Marker `gui` und sind standardmäßig abgewählt (analog `hardware`, gemäß KONVENTIONEN). Dann braucht der Standardlauf keine Qt-System-Bibliotheken.
  - Wenn GUI-Tests laufen: `QT_QPA_PLATFORM=offscreen`. Das Setup stellt `libegl1`, `libgl1`, `libxkbcommon0` u. a. bereit.
  - `[tool.coverage] omit` für `gui/` mit Kommentar als Begründung, wie in KONVENTIONEN vorgesehen.
  - Der Offscreen-Test aus der Probe ist als Vorlage geeignet (Edit-während-Lauf plus Pausenbestätigung).
- **Typisierung:** Signalnamen nicht `event`/`thread` nennen. Qt-`data()`-Rückgaben sind `Any`. matplotlib-Qt-Klassen brauchen gezielte `# type: ignore[no-untyped-call]` mit Begründung. mypy auf PySide6-Code sollte ohne Systembibliotheken laufen, weil nur die `.pyi` gelesen werden. Das habe ich nicht getrennt geprüft (Bibliotheken waren bereits installiert).

### A4 Unsicherheiten, erst am Messrechner klärbar

1. Darf Python 3.11, pywin32 und PySide6 per Wheelhouse (USB) installiert werden, und stört eine Virenschutz-Prüfung die Qt-DLLs? (O6, P1-1)
2. Läuft Qt im selben Prozess wie pywin32 ohne OLE-Initialisierungskonflikt (Hauptthread STA durch Qt, Worker `CoInitialize`)? Nicht `sys.coinit_flags` auf MTA setzen. Ungeprüft, hängt an P2-10.
3. Ist die Microsoft-VC++-Laufzeit vorhanden und die Windows-10-Version von Qt 6.12 unterstützt? Das habe ich nicht verifiziert.
4. Verhalten bei blockierenden PSV-Dialogen (`SuppressMessagesForAutomation`, I5 Abschnitt 5.1, P1-8): Die GUI bleibt dank Worker bedienbar, ob der Worker-Aufruf aber hängt, ist offen (P1-8, P2-10). Fensterfokus und Überlappung zwischen PSV-Fenstern und unserer Oberfläche.
5. Bildschirmauflösung und Skalierung des Messrechners (DPI) für die Lesbarkeit der Tabelle.
6. Nur für NiceGUI: Ist ein Browser vorhanden und erlaubt, und macht die Firewall bei lokalem Server Probleme?
7. Internetzugang und erlaubter KI-Dienst für R-040 (O2). Unabhängig von der GUI-Wahl.

## Rückmeldung an den Orchestrator

**Paket:** P1 · **Status:** ERLEDIGT (Entscheidung des Nutzers steht aus)

**Was geändert wurde:** Nichts im Repository. Proben liegen im Scratchpad `/tmp/claude-0/-home-user/e6b61297-17fb-5003-91f8-95c4534d012c/scratchpad/p1/` (`qtprobe/`, `tkprobe/`, `ngprobe/`, Venvs `v311`, `vng`, `wheelhouse/`). Im Container wurden die apt-Pakete `libegl1 libgl1 libxkbcommon0 libfontconfig1 libdbus-1-3 libglib2.0-0` nachinstalliert.

**Wie verifiziert:**
- Windows-Auflösung für Python 3.11 mit `uv pip compile --python-platform windows` und PyPI-Metadaten (Versionen, Wheel-Größen, Lizenzen).
- Offline-Weg: `pip download --platform win_amd64` für shiboken6 und pywin32 erfolgreich.
- Qt: pytest-qt offscreen grün (1 passed), `mypy --strict` sauber für Kern, GUI und Test.
- Tk: Lauf unter `xvfb-run` grün, `mypy --strict` sauber.
- NiceGUI: `nicegui.testing.User`-Test grün (1 passed), `mypy --strict` sauber.
- Matplotlib-Einbettung Qt offscreen gerendert.
- Nicht geprüft: echte Windows-Ausführung, Browserdarstellung, Drag-and-drop-Umsortieren, Streamlit-Ausführung, die minimale Teilmenge der System-Bibliotheken.

**Akzeptanzkriterien:** A1 ✅ · A2 ✅ · A3 ✅ · A4 ✅

**Annahmen:**
- Der Messrechner ist 64-Bit-Windows (Auftrag). Die Wheels sind nur für `win_amd64` geprüft.
- „Offline“ heißt: Wheelhouse per USB-Stick vom Entwicklungsrechner.
- Die konkrete Version (6.12.0 usw.) ist die, die der Index in dieser Umgebung zum 2026-10-26 lieferte.

**Sichtbare Verhaltensänderungen und Risiken:** Keine am Code. Risiko bei Qt: Lernkurve und Termin 30.10.

**Unverifiziert:** Alles unter A4 sowie Drag-and-drop, Windows-Laufzeitverhalten und die minimale Systembibliotheken-Menge.

**Rückfragen:**
- [blockierend] Entscheidung des Nutzers: PySide6 (Empfehlung) · NiceGUI · Tkinter. Danach legt der Orchestrator die ADR an. *Auswirkung:* bestimmt Abhängigkeiten in `pyproject.toml`, Container-Setup und den Design-Brief.
- [nicht blockierend] Gilt NiceGUI als Option, braucht es vorab die Klärung, ob am Messrechner ein Browser erlaubt ist. *Annahme bis dahin:* Qt.

**Vorschlag für KONVENTIONEN.md (nach Entscheidung für PySide6):**
- GUI = PySide6 6.12.0 (`pyside6-essentials`), optional als Abhängigkeit `gui`.
- GUI-Code liegt in `ldv_automation/gui/`, Tests mit Marker `gui`, standardmäßig abgewählt, laufen mit `QT_QPA_PLATFORM=offscreen`.
- Kern importiert nie GUI oder pywin32. COM-Objekte leben nur im Worker-Thread. Fortschritt per Polling.

**Review-Empfehlung:** Review nicht nötig, weil reine Analyse ohne Codeänderung. Für das spätere Umsetzungspaket P4 Schwerpunkt auf die Thread-Sicherheit des Kerns (R-016, Pausen, Abbruch).