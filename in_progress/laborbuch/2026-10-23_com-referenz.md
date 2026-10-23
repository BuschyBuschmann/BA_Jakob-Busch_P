# 2026-10-23 – Vertiefte Einarbeitung in die COM-Schnittstelle (Paket I5)

**Art:** Arbeitspaket
**Paket/Bezug:** I5; Erwartungsmanagement U1–U7
**Commit:** 065982e (letzter Stand vor dem Paket; noch kein Code unter `software/`)
**Beteiligt:** `software-engineer` (opus), Orchestrator (Stichprobe)

## Ziel
Dauerhafte, belegte Referenz der COM-Automatisierungsschnittstelle der PSV-Software und
des Dateizugriffs (Polytec File Access) als Grundlage für Anforderungen, Architektur,
Umsetzung und Thesis.

## Vorgehen
CHM-Hilfedateien entpackt und in durchsuchbaren Text umgewandelt; Referenzdokument in
elf Abschnitten erstellt, aufbauend auf dem Bericht I1. Alle Polytec-API-Namen per
Skript gegen die Textfassung abgeglichen. Stichprobe durch den Orchestrator:
`IApplication5` ohne `Exporter`, `Application` mit `Exporter` – bestätigt.

## Ergebnis
- `in_progress/analysen/2026-10-23_I5_com-referenz.md`: Objektmodell, Datenerfassung,
  Ablaufsequenzen, Dateizugriff, Meldungen/Fehler/Threading, Reproduzierbarkeits-
  Metadaten, Python-Abbildung (ungeprüft), Enum-Referenz, Abgleich U1–U7, Prüfliste
  für den Messrechner (P1: 10, P2: 12, P3: 8 Punkte).
- `in_progress/analysen/polytec-chm-text/`: vollständige Textfassung von Basic Engine
  Manual und Polytec File Access (918 Dateien, 4 MB) mit Index und Umwandlungsskript.
- Neue Erkenntnisse u. a.: Export erfordert Cast auf `Application`; Validatoren rasten
  Bandbreite/Linien ein, daher Zurücklesen nötig; Frequenzachse k·Δf durch Matlab-
  Beispiel gestützt (weiter vorläufig); Fehler und Warnungen einer Messung in
  `SummaryInfo.Subject`; Service-Methoden des Scankopfs können Werkskalibrierdaten
  überschreiben; Meldungsdialoge sind ein Risiko für unbeaufsichtigte Abläufe.

## Verifikation
Belege je Aussage (CHM-Thema, Seite); API-Namen automatisiert gegen die Textfassung
geprüft; eine Stichprobe manuell. Kein Test mit echter PSV-Software oder am Gerät.

## Probleme und verworfene Ansätze
Versionsstand der Hilfe nicht angegeben (Beispielpfad deutet auf PSV 10.4, Folien zeigen
10.2.1.1); Verhalten aus Python, Bitness, Threading und Events bleiben ungeprüft.

## Offene Punkte
Prüfliste Abschnitt 10 am Messrechner abarbeiten (setzt Klärung F4/F5 voraus);
Referenzmessung (`.svd` + UFF) für die Frequenzachse; ADR-Kandidaten aus I1 und I5.

## Thesis-Bezug
Stand der Technik (PSV-Automatisierung), Methodik und Umsetzung (Schnittstelle,
Architektur), Anhang (Objektmodell).
