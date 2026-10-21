# Projektkonventionen

Verbindlich für alle Agenten und für den gesamten Code unter `software/`.
Abweichung nur auf ausdrücklichen Auftrag des Nutzers.

## Umgebung
- Python 3.11, verwaltet mit `uv`.
- `requires-python = ">=3.11,<3.12"` in `software/pyproject.toml`.
- Das Paket liegt unter `software/`. Alle Befehle werden aus `software/` heraus ausgeführt.
- `uv.lock` wird eingecheckt, damit die Umgebung reproduzierbar ist.

## Standard-Prüfung
Vor jeder Rückmeldung müssen alle Prüfungen fehlerfrei laufen (aus `software/`):

```bash
uv run ruff check .
uv run ruff format --check .
uv run mypy --strict .
uv run pytest --cov --cov-fail-under=90
```

- Lint und Format: `ruff`.
- Typprüfung: `mypy --strict`.
- Tests: `pytest` mit Testabdeckung (`pytest-cov`).
- Mindestabdeckung: 90 % (vom Nutzer festgelegt).
- Nicht ausgeführte Prüfungen werden in der Rückmeldung ausdrücklich benannt.

## Code
- Docstrings im NumPy-Stil.
- SI-Einheiten; die Einheit steht im Namen (z. B. `freq_hz`, `velocity_m_s`) oder im Docstring.
- Winkel in rad, Zeit in s. Abweichende Einheiten werden nur an der Grenze zur COM-Schnittstelle umgerechnet.
- Zufall nur über einen übergebenen Seed bzw. `numpy.random.Generator`.

## Hardware
- Zugriff auf das Vibrometer (COM) nur über eine abstrakte Schnittstelle.
- Ein Simulator dieser Schnittstelle ist Pflicht, damit alles ohne Vibrometer testbar ist.
- Tests dürfen keine echte Hardware voraussetzen. Tests, die Hardware oder die Oberfläche
  brauchen, werden per `pytest`-Marker gekennzeichnet; standardmäßig laufen nur Simulator-Tests.

## Messdaten
- Messdaten werden in Dateien gespeichert, zusammen mit der Softwareversion (Git-Hash).
- Rohdaten werden nie überschrieben.

## Verifikation
- Jede Auswertefunktion wird gegen einen analytischen Referenzfall aus
  `in_progress/fachgrundlagen/` getestet.
- Toleranzen (`rtol`/`atol`) werden in Tests immer explizit angegeben und begründet.

## Abbildungen
- Abbildungen entstehen nur per Skript aus gespeicherten Daten.
