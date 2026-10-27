# Montagspaket: erster Termin am PSV-Messrechner, Mo 2026-11-02

Stand: 2026-10-27, Paket P6. Einstieg in alle Unterlagen für den Prototyp-Test (Plan P2, Abschnitt 9).
Jakob arbeitet allein am Messrechner. Eine echte Messung läuft nur nach seiner ausdrücklichen
Entscheidung. Windows-Schritte sind **nicht getestet**; ein Hardwaretest gilt erst als bestanden, wenn
Jakob ihn bestätigt hat.

## Reihenfolge

| Wann | Was | Dokument |
|---|---|---|
| vor Montag (Entwicklungsrechner) | Letzten Stand committen, Wheel bauen (Build-Hook), Konfigurationsbeispiel einpacken, Wheelhouse füllen, Stick packen | [installation_messrechner.md](installation_messrechner.md), Abschnitte 3 und 4; [erzeuge_wheelhouse.py](../../../software/tools/wheelhouse/erzeuge_wheelhouse.py) |
| vor Montag | Dokumente lesen, Protokoll ausdrucken | dieser Ordner |
| Mo, Messrechner | Vorbereitung, Installation, Erkundung 0, 1, 1b, Sicherung, Konfigurationsdatei, Test-.set, T0 bis T2, Handtest-Teilmenge, (nur nach eigener Entscheidung) T3 bis T7, Sicherung | [ablaufplan_vor_ort.md](ablaufplan_vor_ort.md) |
| Mo, beim Ausfüllen | Befunde und Werte eintragen | [protokoll_vor_ort.md](protokoll_vor_ort.md) |
| nach Montag | `/laborbuch`, Erkundungsordner nach `in_progress/versuche/erkundung/` | siehe Ablaufplan, Abschnitt 9 |

## Dokumente in diesem Ordner

| Datei | Inhalt |
|---|---|
| [README.md](README.md) | dieser Einstieg |
| [installation_messrechner.md](installation_messrechner.md) | Python 3.11, Wheelhouse, Wheel mit Build-Info, Installation mit/ohne Internet, Prüfschritte I1 bis I7 |
| [ablaufplan_vor_ort.md](ablaufplan_vor_ort.md) | Reihenfolge mit Zeitannahmen, Grundregeln, Abbruchkriterien |
| [anleitung_test_set.md](anleitung_test_set.md) | kleine Test-.set in PSV anlegen (allgemein, ohne erfundene Menüpfade) |
| [protokoll_vor_ort.md](protokoll_vor_ort.md) | Protokollvorlage zum Ausfüllen |
| [pruefanleitung_U3_com-adapter.md](pruefanleitung_U3_com-adapter.md) | Prüfanleitung COM-Adapter (T1 bis T6, Schalter aus der Erkundung, U5-Ergänzung) |
| [handtest_U4_gui.md](handtest_U4_gui.md) | Handtest der Oberfläche (Simulator) |

Weitere Unterlagen: [Plan P2](../../planung/plaene/2026-10-26_P2_architektur-prototyp.md) (Abschnitte 6, 9, 10),
[Erkundung-README](../../../software/tools/erkundung/README.md), [KONVENTIONEN.md](../../../KONVENTIONEN.md),
[ADR-001](../../entscheidungen/ADR-001_gui-technologie.md), [TODO.md](../../../TODO.md).

## Offene Punkte vor Montag

- Die Schalter stehen in einer Konfigurationsdatei (`--konfig DATEI`, Beispiel
  `software/konfig/beispiel_messrechner.json`); am Montag Kopie anlegen, Werte aus der Erkundung eintragen,
  Pfad und SHA-256 im Protokoll festhalten (Ablaufplan, Abschnitt 4).
- Ordnerregel (K-U5b): gesperrt sind Programm-/Datenordner, „Polytec“ direkt unter der Laufwerkswurzel und 8.3-Kurznamen; `C:\Users\Polytec\…` ist erlaubt. Vor `MESSEN` Trockenlauf mit derselben .set ohne PSV-Neustart, sonst rote Warnung im Startdialog (Generator dann von Hand prüfen; Ablaufplan 6b und 8).
- Das Wheel entsteht erst nach dem letzten Commit mit `uv build --wheel`; der Build-Hook erzeugt die Build-Info
  selbst und bricht ohne Git ab. `git_dirty` soll false sein (Installation, Abschnitt 4).
