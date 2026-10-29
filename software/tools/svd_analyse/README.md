# svd_analyse – PSV-Messdateien ohne Polytec File Access lesen (Prototyp, Paket W2)

Werkzeug außerhalb des Hauptpakets `ldv_automation` (kein Import daraus). Es liest eine
Polytec-PSV-Messdatei (`.svd`, OLE-Verbunddokument) **nur lesend** und liefert die
gespeicherten Punktspektren, Punktmittel, Banddaten, Geometrie und Metadaten als
NumPy-Arrays. Das Format ist nicht offengelegt; Kodierung, Belege und Sicherheitsgrade
stehen in `in_progress/analysen/2026-10-29_W2_svd-format.md`.

## Dateien

| Datei | Zweck |
|---|---|
| `svd_lesen.py` | Dekodierfunktionen (Bytes → Werte) und `lese_svd(pfad) -> SvdMessung`; Kommandozeile gibt eine Übersicht aus |
| `svd_pruefung.py` | Plausibilitätsprüfungen der Dekodierung gegen Größen, die PSV selbst in der Datei ablegt (Punktmittel, Bandwerte je Punkt), gegen Ungleichungen (Kohärenz ≤ 1) und die Punktzuordnung zur Geometrie (Scanreihenfolge, Zeitstempel); nicht durchführbare Prüfungen werden als solche gemeldet |
| `kontrollplots.py` | Je Datenart ein Kontrollbild (PNG) mit Skriptname und SHA-256 der Eingangsdatei |

## Aufruf (aus `software/`)

```bash
uv run python tools/svd_analyse/svd_lesen.py ../Input/20261012_ref_Mitte.svd
uv run python tools/svd_analyse/kontrollplots.py ../Input/20261012_ref_Mitte.svd ../in_progress/analysen/abbildungen
```

Aus Python (mit `tools/svd_analyse` im Pfad):

```python
from svd_lesen import lese_svd
from svd_pruefung import pruefe

m = lese_svd("../Input/20261012_ref_Mitte.svd")
cp = m.signale["M0"].werte  # complex128, (135 Punkte, 1600 Linien), Zeile = Punktindex
f_hz = m.frequenz_hz  # vorläufige Achse k·Δf, k = 1 … 1600
assert all(e.bestanden for e in pruefe(m))
```

## Konventionen und Grenzen

- `float64`/`complex128` an der Grenze, Punktindex 0-basiert; `m.punkte.label` ist die in
  PSV angezeigte Punktnummer (getrennt vom Index). Phasen nur als komplexe Werte;
  `numpy.angle` liefert rad. **Das Vorzeichen der Kreuzspektren-Phase ist offen.**
- Rolle Antwort/Referenz kommt aus der Signalformel; Banddaten dienen nur als Gegenprobe
  (Widerspruch → `SvdFormatFehler`). Zeitstempel sind naive `datetime` (Zeitzone offen).
- Gespeichert sind keine FRF/Kohärenz, sondern gemittelte Kreuz- und Autospektren je Punkt
  (`CP`, `AP`, `ABS`, `CPH`). PSV bildet H1, H2 und Kohärenz daraus beim Anzeigen.
- Unbekanntes Layout führt zu `SvdFormatFehler` statt zu stillen Ersatzwerten. Felder ohne
  Beleg werden nur roh durchgereicht (`Messpunkte.statusfelder`) oder gar nicht gelesen.
- Getestet ist das Layout nur an einer Datei (PSV-QTec-3D, FFT-Modus, 135 Punkte, zwei
  Referenzkanäle). Andere Messmodi (Zeit, Zoom-FFT, MultiFrame), gespeicherte Zeitdaten
  oder Benutzersignale sind nicht abgedeckt.
- Abhängigkeiten: Gruppe `werkzeuge` in `pyproject.toml` (`numpy`, `olefile`, `matplotlib`).

## Tests

`tests/tools/svd_analyse/` – synthetische Bytes im erschlossenen Layout (`svd_synth.py`)
und, falls `Input/20261012_ref_Mitte.svd` vorhanden ist, ein Plausibilitätstest an der
echten Datei (prüft auch, dass die Datei unverändert bleibt).
