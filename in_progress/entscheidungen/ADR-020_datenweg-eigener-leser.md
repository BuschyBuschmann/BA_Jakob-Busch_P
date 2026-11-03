# ADR-020: Datenweg für die Auswertung – eigener .svd-Leser als Hauptweg

**Datum:** 2026-11-03 · **Status:** angenommen
**Bezug:** ersetzt ADR-006 (vorläufig); Laborbuch 2026-11-02_messrechner-erster-termin und 2026-11-02_k-achse-frequenzachse; Analyse E-PSV-S (Übersicht 2c); R-050, R-051; Entscheidung des Nutzers vom 2026-11-03

## Kontext
ADR-006 legte `.svd` als einziges Rohdatum fest, gelesen per Polytec File Access, und sollte nach Erkundung 1b endgültig entschieden werden. Neue Belege vom 02.11.:
- Der eigene Leser (`software/tools/svd_analyse/svd_lesen.py`) liefert an Label 132 dieselben Werte wie File Access. Die Spektren Vib X/Y/Z sind bitgleich, H1 stimmt auf ≤ 5,8·10⁻⁸ überein (Golden File `in_progress/versuche/2026-11-02_prototyp/golden_punkt1_label132.csv`, 6 von 8 Signalen). Geprüft wurde das nach der Korrektur der Frequenzachse (K-ACHSE).
- File Access läuft am Messrechner auch ohne PSV-COM-Registrierung (Erkundung 1b, 16:11). Es braucht aber Windows und die Polytec-Installation.
- Das `.svd`-Format ist nicht dokumentiert. Der Achsenfehler aus W2 zeigt, dass Fehldeutungen von Feldern unbemerkt bleiben können, wenn keine Gegenprobe läuft.

## Betrachtete Alternativen
| Alternative | Vorteile | Nachteile |
|---|---|---|
| A eigener Leser als Hauptweg, File Access als Gegenprobe am Messrechner | läuft überall (auch Cloud/Linux, Tests), gegen PSV bestätigt | Format undokumentiert; neue PSV-Versionen könnten brechen |
| B File Access als Hauptweg | offizieller, dokumentierter Weg | nur Windows mit Polytec-Installation; Auswertung nicht in der Cloud testbar; COM-Fakes nötig |
| C beide gleichberechtigt mit automatischem Abgleich | maximale Sicherheit | doppelter Pflegeaufwand |

## Entscheidung
**A:** Die Auswertung liest `.svd`-Dateien mit dem eigenen Leser. Polytec File Access (`daten_lesen.py`, `einstellungen_lesen.py`, nur lesend) dient am Messrechner als Gegenprobe. Ein Golden-File-Abgleich läuft bei jeder neuen PSV-Version und bei jeder neuen Messkonfiguration. UFF bleibt wie in ADR-006 eine mögliche Gegenprobe.

## Begründung
Empfehlung des Orchestrators auf Grundlage der Analyse E-PSV-S und der Golden-File-Validierung, vom Nutzer gewählt. Ausschlaggebend sind drei Punkte: Die Auswertung ist plattformunabhängig, sie bleibt in der Cloud testbar, und es gibt einen belegten Gleichstand mit PSV.

## Konsequenzen
- Ein Golden-File-Test für jede PSV-Version und jede Messkonfiguration gehört zum Ablauf der Termine (Golden File v2 im Ablaufplan des nächsten Termins).
- Felder des Lesers, deren Bedeutung nicht belegt ist (z. B. Satzfeld +0x34), werden gekennzeichnet und nicht zur Auswertung genutzt.
- Bewertung in der Thesis: Validierung des Datenwegs gegen das Herstellerwerkzeug und Grenzen eines undokumentierten Formats.
