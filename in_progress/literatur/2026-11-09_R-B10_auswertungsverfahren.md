# R-B10: Auswertungsverfahren über die PSV-Standardauswertung hinaus (Stand 2026-11-09)

**Auftrag:** Betreuervorgabe B10 (Laborbuch `in_progress/laborbuch/2026-11-09_betreuertermin-daniel.md`).
**Prüfstand aller neuen Quellen: `metadaten`** (Existenz über Suchtreffer auf Verlags-, Repositoriums-, Katalog- und Indexseiten bestätigt; Inhalt **nicht gelesen**). Ausnahme: Python-Pakete, deren PyPI-Metadaten direkt abgerufen wurden (siehe Software). Keine Aussage aus diesen Quellen darf als belegt zitiert werden, bevor der Volltext gelesen wurde. Die Kurzbeschreibungen unten stammen aus Abstracts, Katalog- und Verlagsangaben bzw. PyPI-Beschreibungen.

**Grenzen der Prüfung:** `doi.org`, `api.crossref.org`, `sciencedirect.com`, `sandia.gov`, `osti.gov`, `readthedocs.io`, `github.com` (403), `zenodo.org` waren in der Cloud-Sitzung nicht erreichbar. DOI-Auflösung wurde nicht durchgeführt. Eine DOI gilt nur dann als gesichert, wenn mehrere Suchtreffer sie übereinstimmend nennen (siehe `note` je Eintrag). Direkter Abruf gelang nur für PyPI (JSON-Schnittstelle).

## 1. Zuordnung Quelle → Verfahren

Verlässlichkeit: **S** = Standardwerk/Lehrbuch, **B** = begutachteter Artikel, **K** = Konferenzbeitrag (Peer Review nicht geprüft), **N** = Norm, **H** = Herstellerdokument/graue Literatur, **SW** = Software/Paketdokumentation (keine Fachliteratur). Zu jedem Eintrag: Existenz bestätigt, Inhalt nicht gelesen.

### 1.1 Modalparameter-Identifikation (EMA, FRF-basiert)

| bibkey | Verfahren / Thema | Typ | Anmerkung |
|---|---|---|---|
| peeters2004polymax | PolyMAX (poly-reference LSCF) auf MIMO-FRF, Stabilisierungsdiagramm | B | Standardreferenz für PolyMAX. Laut Abstract Fallstudien Automobil und Luftfahrt, Vergleich mit Peak-Picking, Prediction Error u. a. Open Access laut DOAJ-Listung |
| guillaume2003polyreference | Poly-reference LSCF (Ursprung von PolyMAX) | K | Seitenangaben unsicher, Autorenliste nur aus Issuu-Kopie. Nur zitieren, wenn Ursprung des Verfahrens belegt werden soll |
| richardson1982rfp | Rational Fraction Polynomial (RFP), SDOF/MDOF-Anpassung der FRF | K | Zitat unsicher (zweiter Autor, Jahr in Sekundärquelle widersprüchlich). Besser über Lehrbuch (ewins2000modal, maia1997theoretical, heylen1998modal) zitieren |
| ewins2000modal, maia1997theoretical, heylen1998modal | Modalparameter-Identifikation allgemein (Peak-Picking, Kreisanpassung, MDOF-Verfahren), MAC | S | Bereits in L1 (Ewins, Maia); Heylen jetzt als Eintrag mit unsicheren Angaben |
| pintelon2012system | Frequenzbereichs-Identifikation, Schätzer-Eigenschaften | S | bereits in L1 |
| reynders2012review | Überblick Identifikationsverfahren (u. a. Subspace, Frequenzbereich), Vergleich per Monte Carlo | B | Einordnung von LSCF/PolyMAX, SSI. Laut Titel/Abstract (OMA-Schwerpunkt) |
| reynders2012automated | Automatisierte Polselektion (Clustering von Polen aus Stabilisierungsdiagrammen) | B | Relevant für automatisierte Auswertung vieler Messungen. Folgearbeiten nennen Einschränkungen bei starker Dämpfung (nur Suchtreffer-Hinweis) |
| peeters1999ssi | Stochastic Subspace Identification (SSI) mit Referenzsensoren | B | Output-only. Beim Strukturtest mit gemessener Kraft ist FRF-Identifikation (PolyMAX/LSCF) der direktere Weg; SSI nur ergänzend |
| brincker2015oma | Operational Modal Analysis (Lehrbuch) | S | wie oben; nur falls Output-only-Fall behandelt wird |

### 1.2 Vergleichsmaße

| bibkey | Maß | Typ | Anmerkung |
|---|---|---|---|
| allemang1982mac | MAC (Ersteinführung) | K | wird als Ursprung zitiert; Seiten 110-116 aus mehreren Literaturlisten |
| allemang2003mac | MAC, Nutzung und Missbrauch | B/Magazin | bereits in L1; nützlich für Grenzen des MAC (Skalierung, Mehrdeutigkeit) |
| lieven1988comac | COMAC (Ort-bezogene Korrelation) | K | Originalquelle nur indirekt belegt (Springer-Referenzeintrag) |
| heylen1996frac | FRAC (Vergleich von FRF) | K | Katalogeintrag TIB; Sekundärquellen: Wertebereich 0 bis 1, keine Amplitudenberücksichtigung. Formel nicht gesehen |
| (Sekundär, nicht aufgenommen) | Altair-Dokumentation FRAC, ANSYS-Hilfe COMAC | SW/H | nur zur Orientierung; keine Fachquelle |

### 1.3 Datenqualität, Plausibilität, Unsicherheit

| bibkey | Thema | Typ | Anmerkung |
|---|---|---|---|
| rothberg1989pseudo | Pseudo-Vibration durch Speckle (Ersteinführung des Begriffs) | B | Loughborough-Repositorium, DOI aus Repositorium |
| rothberg2006speckle | Numerische Simulation von Speckle-Rauschen | B | DOI nicht bestätigt |
| martarelli2006speckle | Speckle-Rauschen bei kontinuierlich scannendem LDV | B | Angaben nur indirekt (Wikipedia) belegt, daher unsicher |
| rothberg2017ldvreview, castellini2006ldv | Überblick LDV, Fehlerquellen | B | bereits in L1 |
| rothberg2012framework | Vektormodell der gemessenen Geschwindigkeit | B | bereits in L1; Basis für Unsicherheit der 3D-Zerlegung |
| rohe2020alignment | Ausrichtung der Laserköpfe (Euler-Winkel) per Photogrammetrie; manuelle Ausrichtung als unquantifizierte Unsicherheitsquelle | unklar (Sandia-Veröffentlichung) | Venue/Autorennamen unbestätigt. Einziger Treffer zu Ausrichtungsfehlern bei 3D-SLDV. Weitere Sandia-Treffer (Nasenkegel-Test, Folien) nicht aufgenommen |
| pintelon2007uncertainty | Unsicherheitsgrenzen der Modalparameter aus der Identifikation | B | DOI nur aus Folgezitat. Passt zu GUM-Begriffen (jcgm2008gum, L1) |
| jcgm2008gum | Messunsicherheit allgemein | N/Leitfaden | bereits in L1 |
| bendat2010random | Kohärenz, Schätzfehler H1/H2 | S | bereits in L1 |
| pyfrf (SW) | H1, H2, Hv, ODS-FRF in Python | SW | PyPI-Metadaten gelesen, Algorithmus nicht geprüft |
| iso2019mobility5 | Messung von FRF mit Impulsanregung (Anforderungen) | N | nur Katalogseite im Treffer, kostenpflichtig |

### 1.4 Nichtlinearitätsprüfung

| bibkey | Thema | Typ | Anmerkung |
|---|---|---|---|
| kerschen2006nonlinear | Erkennung, Charakterisierung, Identifikation von Nichtlinearität in der Strukturdynamik (Übersicht) | B | Open-Access-Kopie auf HAL laut Treffer; DOI aus mehreren Einträgen übereinstimmend |
| ewins2000modal | Linearitätsprüfung im Modaltest | S | Ob und wo das Buch Linearitätsprüfungen beschreibt, ist **nicht** geprüft; erst nach Lesen behaupten |

### 1.5 Modell-Abgleich mit FE

| bibkey | Thema | Typ | Anmerkung |
|---|---|---|---|
| friswell1995fem | FE-Modellabgleich (Lehrbuch) | S | ISBN aus Katalogen; Standardwerk laut Katalogeinordnung "erstes Buch zum Thema" |
| mottershead1993updating | Übersicht Modellabgleich | B | DOI aus Structurae-Eintrag |
| sauer2010closing | Messpunkte aus FE-Knoten, Koordinatensystem aus FE-Modell, Roboter-3D-SLDV, FE-Abgleich | K/H | Polytec-Beteiligung, graue Literatur. Passt zu B1 (Alignment) |
| yuan2023threed | Koordinatenbeziehungen von drei Vibrometern zu Messkoordinatensystem auf gekrümmter Oberfläche; Vergleich mit kommerziellem 3D-SLDV | B | DOI nicht bestätigt |
| chen2021threesldv, rothberg2012framework | 3D-Zerlegung und Alignment | B | bereits in L1 |
| (nicht aufgenommen, Hinweis) | Polytec-Anwendungsberichte "InFocus": Blisk-Modellkorrelation (Doku-Nr. 52051 laut URL), Satellitenpaneel FalconSAT-5, FE-Validierung | H | Herstellerberichte, nur Suchtreffer-Auszüge; MAC-Werte und Verbesserungsangaben darin nicht übernommen |

### 1.6 Visualisierung (Animation, Koordinatentransformation, Flächennormale)

| bibkey | Thema | Typ | Anmerkung |
|---|---|---|---|
| schwarz1999ods | ODS vs. Mode Shape | K/grau | bereits in W1, unsicher |
| yuan2023threed, rohe2020alignment, sauer2010closing | Koordinatensysteme, Ausrichtung, Messpunkte aus FE | s. o. | Nur Ansatzpunkte. **Keine** Quelle gefunden, die die punktweise Rotation in die Flächennormale (lokales KOS) herleitet |
| polytec2015theory, polytec2022psvsoftware, polytec2022psvpresentationen (Repo) | PSV-Darstellung, 3D-Triangulation | H | liegt im Repo; für B6/B7/B8 (Übernahme der PSV-Visualisierung) die Handbuchabschnitte zu Darstellung/Animation/Koordinatensystemen gezielt lesen (nicht Teil dieses Pakets) |
| sdypy (SW), sdypy-view | 3D-Netzdarstellung und Animation von Modenformen (Knoten, Elemente, Modenform (n,3)) über PyVista | SW | PyPI-Beschreibung gelesen, Funktionsfähigkeit nicht getestet. Version 0.2.0 jung |

### 1.7 Offene Python-Werkzeuge

| bibkey | Werkzeug | Stand laut PyPI (abgerufen 2026-11-09) | Anmerkung |
|---|---|---|---|
| sdypyema | sdypy-EMA / pyEMA | 0.31.0 (2026-09-29); MIT (Klassifikator); Python >=3.10, damit 3.11 abgedeckt; Abhängigkeiten numpy, scipy, matplotlib, pyuff, tqdm | Pole-Schätzung aus FRF-Matrix mit Stabilisierungsdiagramm, Modalkonstanten, Rekonstruktion. **Welcher Schätzalgorithmus** (z. B. LSCF) in der PyPI-Beschreibung nicht genannt; Dokumentation nicht abrufbar. pyEMA ist laut PyPI nur noch ein Port von sdypy-EMA |
| pyuff | UFF lesen/schreiben | 2.5.8 (2026-09-25) | bereits aus W1; Typen laut PyPI siehe Eintrag |
| pyfrf | H1/H2/Hv-Schätzer | 1.5.0 (2026-10-02) | neu; mögliche Gegenprobe zu eigenen FRF-Schätzern |
| sdypy | Dachpaket, MIT, Namespace-Pakete | 0.6.0 (2026-11-06) | Zugang zu EMA, io, FRF, excitation, view, model |

## 2. Wichtigste Treffer je Schwerpunkt (Kurzempfehlung)

1. Identifikation (PolyMAX/LSCF): peeters2004polymax, dazu Lehrbuch (ewins2000modal oder heylen1998modal) für SDOF/MDOF-Grundlagen.
2. Vergleichsmaße: allemang1982mac, allemang2003mac, lieven1988comac, heylen1996frac; Formeln erst nach Lesen übernehmen. Zur FRAC-Definition ist eine Sekundärquelle mit lesbarem Volltext nötig.
3. Datenqualität: rothberg1989pseudo und rothberg2006speckle für Speckle/Pseudovibration; Polytec-SE-Abschnitte liegen bereits im Repo (R-0211).
4. Unsicherheit: pintelon2007uncertainty (Modalparameter), rohe2020alignment (Ausrichtung 3D-SLDV), jcgm2008gum.
5. Nichtlinearität: kerschen2006nonlinear.
6. FE-Abgleich: friswell1995fem, mottershead1993updating, sauer2010closing.
7. Python: sdypy-EMA (Dokumentation der festgelegten Version lesen), pyuff, pyfrf, sdypy-view.

## 3. Lücken (keine belastbare Quelle gefunden)

1. **Flächennormale/lokales Koordinatensystem pro Messpunkt (B6):** keine Quelle mit Herleitung gefunden. Ansatzpunkte nur yuan2023threed (3 Koordinatensysteme zu Messkoordinatensystem) und Polytec-Dokumentation (nicht gelesen).
2. **Unsicherheit der 3D-Zerlegung/Fehlerfortpflanzung** bei 3D-SLDV: außer rohe2020alignment (Ausrichtung) und rothberg2012framework (L1) nichts Belastbares; Rohe/Witt-Angaben unverifiziert.
3. **Aerospace-spezifische Richtlinie** zu Auswertung/Plausibilisierung von Modaltests (Norm/Richtlinie) nicht gefunden. ISO 7626-5 behandelt Impulsanregung allgemein. ECSS-Dokumente aus L1 sind noch nicht inhaltlich auf Modal-Survey geprüft.
4. **Linearitätsprüfung im Modaltest** mit Verweis auf konkrete Lehrbuchabschnitte: nicht geprüft (Ewins nicht gelesen).
5. **Algorithmus-Details von sdypy-EMA** (LSCF ja/nein): nicht belegt; readthedocs/GitHub nicht erreichbar.
6. **Peer-reviewter aerospace-spezifischer Artikel zu 3D-SLDV + EMA + FE-Abgleich:** nicht gefunden; nur Herstellerberichte (Polytec) und eine Konferenz-/Anwendungsarbeit (sauer2010closing).
7. DOIs offen bei rothberg2006speckle, yuan2023threed und guillaume2003polyreference; Volumen/Heft offen bei peeters1999ssi; Zugriff auf Originale für Vornamen nötig.
