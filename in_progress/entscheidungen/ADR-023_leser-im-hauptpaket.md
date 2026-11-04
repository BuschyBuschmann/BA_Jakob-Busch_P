# ADR-023: `.svd`-Leser im Hauptpaket (Nachtrag zu ADR-020)

**Datum:** 2026-11-05 · **Status:** angenommen
**Bezug:** ADR-020; Plan P-AUSW (T1.1); Laborbuch 2026-11-03_auswerten-t1-leser-prozess; Entscheidung des Nutzers vom 2026-11-05

## Kontext
ADR-020 macht den eigenen Leser zum Hauptweg. Er lag aber als Werkzeug in `software/tools/svd_analyse/` und war nicht im Wheel; am Messrechner hätte das Paket die Datei nicht lesen können. `olefile` war nur Entwicklungsabhängigkeit.

## Betrachtete Alternativen
| Alternative | Vorteile | Nachteile |
|---|---|---|
| Leser per `git mv` ins Paket (`ldv_automation/auswertung/svd_lesen.py`), `olefile` Hauptabhängigkeit | im Wheel, ein Importweg, mypy-strict-fähig | Importzeilen in Werkzeugen/Tests anpassen |
| Shim-Datei in `tools/`, die ins Paket weiterleitet | weniger Umzug | mypy strict verliert private Namen, doppelte Wege |
| Leser bleibt Werkzeug | keine Änderung | Hauptpaket kann am Messrechner nicht lesen |

## Entscheidung
Leser ins Hauptpaket verschoben; `olefile` und (für die Oberfläche, ADR-021) `matplotlib` sind Hauptabhängigkeiten; Gruppe `werkzeuge` entfällt. Wheelhouse-Pins inkl. Folgepin `tzdata` mit Abgleichtest gegen `uv.lock`.

## Begründung
Planung P-AUSW, Umsetzung T1 und Review R-AUSW-T1; der Abgleichtest fand den im Plan fehlenden Folgepin `tzdata`.

## Konsequenzen
Wheel ca. 19–20 MB größer; Installationsweg für 0.3.0 braucht die neuen Abhängigkeiten (TODO); Aufruf des Lesers als `python -m ldv_automation.auswertung.svd_lesen`.
