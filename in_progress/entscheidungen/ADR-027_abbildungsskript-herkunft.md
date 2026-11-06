# ADR-027: Abbildungsskript für Thesis-Abbildungen – Ort der Logik und Git-Regel

**Datum:** 2026-11-06 · **Status:** angenommen (Nutzer, 2026-11-05, Freigabe Plan P-ABB-S1)
**Bezug:** Plan `in_progress/planung/plaene/2026-11-05_P-ABB-S1_abbildungsskript.md` (D1–D5); KONVENTIONEN „Abbildungen“; ADR-021, ADR-024, ADR-025; Laborbuch 2026-11-06_abbildungsskript

## Kontext
Thesis-Abbildungen entstehen nur per Skript aus gespeicherten Daten und nennen Skript und Git-Hash. Aus den Messdateien vom 2026-11-09 sollen alle vier Ansichten im Thesis-Stil entstehen. `tools/auswertung/darstellung_beispiel.py` erzeugt sie bereits, aber ohne Wahl von Kanalpaar und Bezug, ohne Gesamtmanifest und ohne Reaktion auf einen unsauberen Software-Stand.

## Betrachtete Alternativen
| Frage | Alternative | Vorteile | Nachteile |
|---|---|---|---|
| D1 Ort der Logik | **A: vorhandenes Skript erweitern** | kleinster Eingriff, kein neues Wheel, bestehende Tests bleiben | Name „Beispiel“ passt nicht mehr; Skript wird am Messrechner separat kopiert |
| | B: neues Skript, das das alte importiert | sprechender Name | Skript importiert Skript |
| | C: Logik als Paketmodul | im Wheel enthalten | `src/`-Änderung, neues Wheel, mehr Aufwand |
| D2 Unsauberer Stand | **Abbruch, Ausnahme mit `--erlaube-dirty`** | keine Abbildung ohne eindeutigen Stand aus Versehen | Vorschau braucht ggf. den Schalter |
| | nur Warnung | einfach | unklare Stände können in die Thesis gelangen |
| | Kennzeichen im Dateinamen | sichtbar | LaTeX-Verweise ändern sich |
| D3 Eigene Ausgabe macht den Baum unsauber | **zuerst außerhalb des Repos erzeugen, dann kopieren und committen** | Versionsfunktion bleibt unverändert | ein Kopierschritt |
| | Pfadfilter in der Versionsfunktion | direkte Ausgabe ins Repo | Eingriff in zentrale Funktion, wirkt auf Messprotokolle |

## Entscheidung
D1 A, D2 Abbruch mit `--erlaube-dirty`, D3 Ausgabe zuerst außerhalb des Repos. Dateinamen `<Messdatei>_<abbildung>.<fmt>` mit `<Messdatei>_manifest.json` (D4), Format standardmäßig PNG und PDF (D5). Endgültige Abbildungen entstehen in der Cloud aus der ins Repo gelegten .svd, am Messrechner nur Vorschau (Nutzer, Q1). Die Schwingform nutzt dieselbe Referenz wie die Oberfläche (Nutzer, Review-Befund). Jede Pfadkomponente „Input“ und „PyCharmProject“ ist als Ziel gesperrt (Nutzer).

## Begründung
Kleinster Eingriff, am 2026-11-09 nutzbar, keine neue Rechnung; die Zeichenfunktionen bleiben die gemeinsamen aus `darstellung/` (ADR-024). Der Abbruch bei unsauberem Stand setzt die Herkunftsregel aus KONVENTIONEN technisch durch.

## Konsequenzen
- Abbildungen: `python tools/auswertung/darstellung_beispiel.py <svd> --ausgabe <Ordner außerhalb des Repos>`, danach nach `in_progress/thesis/abbildungen/<Messdatei>/` kopieren und committen.
- Offen: Am Messrechner kann `ermittle_build_info` den Hash eines fremden Git-Repos liefern, wenn die venv in einem Repo liegt (`version.py`, eigenes Paket möglich). Die Referenzwahl der Schwingform existiert doppelt (Skript und Oberfläche); Meldungen bei Fehler beim Anlegen des Ordners und bei halb geschriebenem Manifest sind ungenau (Nutzerentscheidung: offen).
