# ADR-029: Technik der 3D-Animation der Betriebsschwingform

**Datum:** 2026-11-09 · **Status:** angenommen (Nutzer, 2026-11-09)
**Bezug:** R-071; Design-Brief K1-AUSW2 (OE-A1, UI-22 bis UI-33); FG-04; Analyse `in_progress/analysen/2026-11-09_A-3D_animationstechnik.md`; ADR-021, ADR-024

## Kontext
Der Nutzer hat für R-071 eine 3D drehbare Animation gewählt. Sie muss über Windows-Remotedesktop bedienbar sein, graustufentauglich sein und als Standbild der Phasendarstellung entsprechen; das Thesis-Standbild soll aus derselben Zeichenfunktion kommen (ADR-024).

## Betrachtete Alternativen
| Alternative | Vorteile | Nachteile |
|---|---|---|
| (a) matplotlib `mplot3d` in `Figure` + `FigureCanvasQTAgg` | keine neue Abhängigkeit, kein OpenGL (geringstes Remotedesktop-Risiko), gleiche Zeichenfunktion für Oberfläche und Thesis (Vektor-PDF), offscreen testbar | 40–55 ms je Bild (Cloud), Mausrad-Zoom und Tastatursteuerung selbst zu bauen, Tiefensortierung je Artist |
| (b1) pyqtgraph.opengl | 2,8 ms je Bild, +5 MB | OpenGL ≥ 2.1 über Remotedesktop unklar, nur Pixelbild, zweite Zeichenfunktion für die Thesis |
| (b2) PyVista/VTK | leistungsfähige 3D-Darstellung | +86 MB, OpenGL 3.2 nötig (über Remotedesktop stark gefährdet), zweite Zeichenfunktion |

## Entscheidung
(a) matplotlib `mplot3d` innerhalb von ADR-021 und ADR-024.

## Begründung
Messungen und Abwägung in der Analyse A-3D (Cloud-Linux, Software-GL); entscheidend sind das geringste Risiko über Remotedesktop, keine neue Abhängigkeit im Wheelhouse und die gemeinsame Zeichenfunktion für das Thesis-Standbild.

## Konsequenzen
- mypy-Override `ignore_missing_imports` für `mpl_toolkits.mplot3d`.
- Mausrad-Zoom und Tastatursteuerung werden selbst gebaut; die z-Achse wird an die überhöhte Auslenkung gebunden (Gestaltung im Brief bzw. Korrektur).
- Datenvertrag für 3D-Amplituden (P, 3) mit Masken fehlt noch (FG-04, Abschnitt 7).
- Rückfallreihenfolge, falls am Messrechner zu langsam: 1) Neuzeichnen beim Loslassen (OE-A2), 2) gedrosselte Wiedergabe mit vereinfachten Achsen, 3) eigene 2D-Projektion mit Blitting, 4) erst dann eine OpenGL-Bibliothek, bevorzugt pyqtgraph.
- Tempo und Lesbarkeit über Remotedesktop sind am Messrechner zu prüfen (UI-38) und gelten erst nach Bestätigung des Nutzers.
