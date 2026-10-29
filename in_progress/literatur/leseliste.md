# Leseliste und erste Quellensammlung (Paket L1, Stand 2026-10-28)

**Prüfstand aller Einträge: `metadaten`** (Existenz über Suchmaschinen-Treffer auf Verlags-, Repositoriums- und Katalogseiten bestätigt; Inhalt **nicht gelesen**). Details je Eintrag im Feld `note` in `literatur.bib`. Keine Aussage aus diesen Quellen darf als belegt zitiert werden, bevor der Volltext gelesen wurde.

**Grenzen der Prüfung:** `api.crossref.org`, `sciencedirect.com`, `researchgate.net` und `repository.lboro.ac.uk` waren in der Cloud-Sitzung nicht erreichbar (Netzfreigabe fehlt). DOI-Auflösung und Verlagsseiten wurden daher nicht direkt abgerufen. Autorenlisten von NumPy/SciPy sind gekürzt. Zugangsangaben („frei“) stammen aus Suchtreffern, RWTH-Zugang wurde nicht getestet.

**Zugang:** *frei* = laut Suchtreffer ohne Lizenz abrufbar; *RWTH* = voraussichtlich über UB/Netz (nicht getestet); *Bibliothek* = Buch (UB RWTH oder Fachbibliothek, Verfügbarkeit nicht geprüft); *Repo* = liegt unter `Input/literatur/`.
**Priorität Volltext:** A = vor Exposé-Abgabe sinnvoll, B = für Grundlagenkapitel, C = optional.

## Feld 1: Laser-Doppler-Vibrometrie, Scanning- und 3D-LDV

| Kürzel (`bibkey`) | Quelle | Typ | Relevanz / Kapitel | Zugang | Volltext |
|---|---|---|---|---|---|
| rothberg2017ldvreview | Rothberg et al. 2017, Optics and Lasers in Engineering 99, 11-22 | Review-Artikel | Überblick Prinzip, Scanning-LDV, Anwendungen; Grundlagenkapitel LDV, Exposé-Stand der Technik | RWTH; Manuskriptkopien in Hochschul-Repositorien laut Suche | benötigt (A) |
| castellini2006ldv | Castellini, Martarelli, Tomasini 2006, MSSP 20, 1265-1285 | Artikel | Entwicklung und Grenzen von LDV-Systemen (inkl. Scanning); Grundlagenkapitel | RWTH | benötigt (B) |
| rothberg2012framework | Rothberg, Tirabassi 2012, MSSP 26, 141-166 | Artikel | Vektormodell der gemessenen Geschwindigkeit inkl. Strahlorientierung; Messunsicherheit der 3D-Zerlegung (Relevanz vermutet) | RWTH | benötigt (B) |
| chen2021threesldv | Chen, Zhu 2021, J. Sound Vib. 498, 115950 | Artikel | 3D-Messung mit drei Scanning-LDV (Polytec PSV-500-3D) im Vergleich zu Punktscan; aktuelle Primärliteratur | RWTH | benötigt (B) |
| polytec2015theory | Polytec Theory Manual (41088) | Herstellerdok. | Gerätekonventionen, 3D-Triangulation | Repo | im Repo (kein Nachbeschaffen) |
| (ohne Eintrag) | Martarelli, Revel, Santolini 2001, MSSP 15(3), ab S. 581, „Automated modal analysis by scanning laser vibrometry: problems and uncertainties associated with the scanning system calibration“ | Artikel | Unsicherheit der Scanner-Kalibrierung und Wirkung auf Modalparameter | RWTH | **nicht in .bib**: Band/Heft/Seitenende/DOI nicht bestätigt (nur Abstract in Indexseiten, Metadaten dort teils fehlerhaft). Prüfen im Katalog; benötigt (C) |

Lücke: Zu Messunsicherheit und Fehlerfortpflanzung speziell von 3D-Scanning-LDV wurde **keine** gesicherte Quelle gefunden (siehe unten, Lücken).

## Feld 2: Experimentelle Modalanalyse und Strukturtests (inkl. Luft- und Raumfahrt)

| Kürzel | Quelle | Typ | Relevanz / Kapitel | Zugang | Volltext |
|---|---|---|---|---|---|
| ewins2000modal | Ewins, *Modal Testing: Theory, Practice and Application*, 2. Aufl. (Research Studies Press, 2000; Wiley-Angabe 2009 widersprüchlich) | Fachbuch (Standardwerk) | Grundlage Modaltest, FRF, SDOF/MDOF; Exposé und Grundlagen | Bibliothek | benötigt (A); Ausgabe/Verlag am Exemplar prüfen |
| maia1997theoretical | Maia, Silva (Hrsg.), *Theoretical and Experimental Modal Analysis* (Research Studies Press, 1997) | Fachbuch | Theorie und Versuch der Modalanalyse | Bibliothek | benötigt (B) |
| (ohne Eintrag) | Heylen, Lammens, Sas, *Modal Analysis Theory and Testing* (KU Leuven) | Fachbuch | Standardlehrbuch, MAC | Bibliothek | **nicht in .bib**: Jahr (1998/2002?) und ISBN nicht bestätigt. UB-Katalog prüfen; (B) |
| allemang2003mac | Allemang 2003, Sound and Vibration 37(8), „The Modal Assurance Criterion - Twenty Years of Use and Abuse“ | Zeitschriftenartikel | MAC als Vergleichsmaß für Moden (Reproduzierbarkeit) | frei (laut BibBase-Eintrag ein PDF-Link auf sandv.com, nicht geprüft) | benötigt (B) |
| goege2007gvt | Göge et al. 2007, IMAC XXV, „Ground vibration testing of large aircraft - state-of-the-art and future perspectives“ | Konferenzbeitrag | Ground Vibration Test in der Luftfahrt; Kontext Strukturtests | RWTH/SEM-Proceedings oder DLR anfragen (kein Volltext im DLR-Eintrag) | benötigt (A) |
| ecss2012testing / ecss2022testing | ECSS-E-ST-10-03C (Ausgabe 1.6.2012) und Rev.1 (31.5.2022), „Space engineering - Testing“ | Norm (Raumfahrt) | Rahmen für mechanische Prüfungen (u. a. Schwingprüfungen) in der Raumfahrt; welche Ausgabe gilt, ist festzulegen | frei (ecss.nl) | benötigt (B); gelesen werden muss, welche Abschnitte Modal Survey/Sinus betreffen |

Hinweis: Eine Luftfahrt-Norm zum GVT wurde nicht ermittelt (Lücke).

## Feld 3: Signalverarbeitung (FFT, Fenster, Mittelung, H1/H2, Kohärenz)

| Kürzel | Quelle | Typ | Relevanz / Kapitel | Zugang | Volltext |
|---|---|---|---|---|---|
| bendat2010random | Bendat, Piersol, *Random Data*, 4. Aufl. (Wiley, 2010) | Fachbuch (Standardwerk) | H1/H2-Schätzer, Kohärenz, Schätzfehler; Grundlagenkapitel | Bibliothek | benötigt (A) |
| brandt2011noise | Brandt, *Noise and Vibration Analysis*, 1. Aufl. (Wiley, 2011) | Fachbuch | Praxisnahe Darstellung FFT, Fenster, Mittelung, FRF-Schätzung | Bibliothek | benötigt (B) |
| harris1978windows | Harris 1978, Proc. IEEE 66(1), 51-83 | Artikel (Primärliteratur) | Fensterfunktionen, Leckage, Kennwerte (ENBW, Scalloping) | RWTH | benötigt (B) |
| welch1967periodogram | Welch 1967, IEEE Trans. Audio Electroacoust. 15(2), 70-73 | Artikel (Primärliteratur) | Gemittelte Periodogramme (Basis scipy.signal.welch) | RWTH | benötigt (B) |
| heinzel2002spectrum | Heinzel, Rüdiger, Schilling 2002, Technischer Bericht (AEI Hannover) | Techn. Bericht (graue Lit.) | Fenster-Liste, ENBW, Skalierung Spektrum vs. Spektraldichte | frei (Kopien Fermilab/LIGO DCC) | benötigt (B); als Technischer Bericht kennzeichnen |
| pintelon2012system | Pintelon, Schoukens, *System Identification: A Frequency Domain Approach*, 2. Aufl. (2012) | Fachbuch | Nichtparametrische FRF-Schätzung, Anregungssignale | Bibliothek | benötigt (C) |
| polytec2022psvsoftware | Polytec Software Manual PSV 10.1 (41585, EN; DE: 41584) | Herstellerdok. | Skalierung, Mittelung, H1/H2 in PSV | Repo | im Repo |

## Feld 4: Automatisierung, Reproduzierbarkeit, Python in der Messtechnik

| Kürzel | Quelle | Typ | Relevanz / Kapitel | Zugang | Volltext |
|---|---|---|---|---|---|
| harris2020numpy | Harris et al. 2020, Nature 585, 357-362 | Artikel (Referenzpublikation) | Zitat für NumPy | frei (Open Access) | benötigt (C); Zitat reicht, kein inhaltliches Lesen nötig |
| virtanen2020scipy | Virtanen et al. 2020, Nature Methods 17, 261-272 | Artikel (Referenzpublikation) | Zitat für SciPy (`scipy.signal`) | frei (Open Access) | wie oben (C) |
| hunter2007matplotlib | Hunter 2007, Comput. Sci. Eng. 9(3), 90-95 | Artikel (Referenzpublikation) | Zitat für Matplotlib (Abbildungen) | RWTH | (C) |
| wilson2017goodenough | Wilson et al. 2017, PLOS Comput. Biol. 13(6), e1005510 | Artikel | Reproduzierbarkeit von Software und Daten (Versionierung, Datenhaltung); stützt Git-Hash-/Rohdaten-Konvention | frei (Open Access) | benötigt (B) |
| jcgm2008gum | JCGM 100:2008 (GUM) | Leitfaden/Norm | Messunsicherheit, Wiederholbarkeit, Reproduzierbarkeit (Begriffe) | frei (BIPM) | benötigt (B) |
| iso2011laservibrometer | ISO 16063-41:2011 | Norm | Kalibrierung rectilinearer Laservibrometer; Abgrenzung (3D-Scanning-System wird nicht direkt erfasst, Anwendbarkeit prüfen) | Nautos/RWTH (kostenpflichtig bei ISO) | benötigt (C) |

Lücke: Zu **Prüfstandsautomatisierung** (automatisierte Messabläufe, Mess-Warteschlangen) und **Python in der Messtechnik** (z. B. Instrumentensteuerung) wurde keine belastbare, begutachtete Quelle gefunden und geprüft. Python-Pakete zur experimentellen Modalanalyse (z. B. pyEMA, Hinweis aus Suche: PyPI/Read-the-Docs, **kein** Fachartikel gefunden) werden nicht aufgenommen; nur als Hinweis (Software-/Paketdokumentation, keine Fachliteratur).

## Feld 5: Software-Grundlagen und Herstellerdokumentation

| Kürzel | Quelle | Typ | Relevanz / Kapitel | Zugang | Volltext |
|---|---|---|---|---|---|
| microsoft2025comoverview | Microsoft Learn, „COM Technical Overview“ | Herstellerdokumentation | Definition COM als binärer Interoperabilitätsstandard; Begriffsabgrenzung zur seriellen Schnittstelle | frei (online) | benötigt (B) (Seite nicht abgerufen) |
| hammond2000win32 | Hammond, Robinson, *Python Programming on Win32* (O'Reilly, 2000) | Fachbuch (alt) | COM-Client in Python mit pywin32; Prinzip, nicht aktuelle API | Bibliothek / O'Reilly Learning | benötigt (C) |
| polytec2025com | Polytec, „Automatisierung der PSV-Soft / VibSoft via COM“ (Folien, 12/2025) | Herstellerfolien | Einstieg COM-Steuerung PSV-Software; C#-Beispiel; Python-Hinweis des Betreuers (persönliche Mitteilung) | Repo | im Repo |
| polytec2022psvsoftware | Polytec Software Manual PSV Acquisition 10.1 | Herstellerdok. | Software und Parameter | Repo | im Repo |
| polytec2023qtec3d | Polytec Kurzbetriebsanleitung PSV QTec-3D | Herstellerdok. | Systemaufbau, Betriebsbedingungen | Repo | im Repo |
| (ohne Eintrag) | Polytec „Basic Engine Manual“ (CHM) und „Polytec File Access Object Model Reference“ | Herstellerdok. | COM-Objektmodell, Datenzugriff | Repo (`Input/literatur/polytec/Windows Hilfedateien/`; Textauszug `in_progress/analysen/polytec-chm-text/`) | **nicht in .bib**: Titel-/Versionsangaben nicht von mir geprüft (CHM nicht gelesen). Bei Aufnahme Versionsnummer aus der Hilfe notieren |
| (nicht aufnehmen) | `Input/literatur/Example_Library_STABCOOL` | Institutscode | Vorbild/Gegenbeispiel (siehe Analysebericht I1) | Repo | Kein zitierfähiger Fachbeleg; nur als Software des Instituts erwähnbar, Rückfrage Autor/Lizenz an Betreuer |

## Feld 6: Vorhandene Startliteratur im Repo (Sichtung)

- `Input/literatur/polytec/` (Handbücher, Hilfen, Schulungsfolien) und `06_Automatisierung_via_COM`: als Herstellerquelle aufgenommen (siehe Feld 5). Meine Prüfung beschränkt sich auf **Titelseiten und PDF-Metadaten** von Theory Manual, Software Manual PSV (EN/DE), Kurzbetriebsanleitung QTec-3D und COM-Folien.
- Schulungsunterlagen (17 Foliensätze), PSV-Desktop-Handbücher, Einpunkt-Vibrometer-Handbücher: **nicht** gesichtet und nicht aufgenommen. Falls zitiert, Dokumentnummer und Datum von der Titelseite übernehmen.
- Analysebericht I2 (`in_progress/analysen/2026-10-23_I2_messtechnik-fachgrundlagen.md`, Abschnitt 7.3) listet Rechercheaufträge R1-R12. Stand Abdeckung durch diese Sammlung: R1 ✅ (Bendat/Piersol, Brandt, Pintelon/Schoukens; Hv-Schätzer nicht konkret belegt), R2 ✅ (Harris, Welch, Heinzel; Oppenheim/Schafer nicht geprüft), R3 teilweise (Ewins, Maia/Silva, Allemang; Heylen nur Hinweis; LSCF/PolyMAX/Richardson-Formenti nicht recherchiert), R4 teilweise (Rothberg 2017, Castellini 2006; Drain 1980 und Speckle/Pseudovibration nicht recherchiert), R5 Lücke, R6 teilweise (ECSS, Göge), R7 ✅ (GUM, ISO 16063-41), R8 nicht bearbeitet (Schroeder 1970), R9 nicht bearbeitet, R10 nicht bearbeitet (Blevins), R11 nicht bearbeitet (UFF; Polytec File Access liegt als CHM vor), R12 offen (siehe Volltext benötigt).

## Für das Exposé empfohlen (12 Quellen)

Auswahl nach Relevanz fürs Exposé (Stand der Technik, Methodik); alle derzeit nur `metadaten`. Vor dem Zitieren der Aussagen Volltext lesen.

1. rothberg2017ldvreview (LDV-Überblick)
2. chen2021threesldv (aktuelle 3D-Scanning-LDV, Primärliteratur)
3. ewins2000modal (Modaltest-Standardwerk)
4. goege2007gvt (Strukturtests Luftfahrt, GVT)
5. ecss2022testing bzw. ecss2012testing (Raumfahrt-Prüfnorm, Ausgabe festlegen)
6. bendat2010random (Spektralschätzung, H1/H2, Kohärenz)
7. harris1978windows (Fenster)
8. welch1967periodogram (gemittelte Spektren)
9. wilson2017goodenough (Reproduzierbarkeit der Software)
10. jcgm2008gum (Messunsicherheit/Wiederholbarkeit)
11. polytec2022psvsoftware (Hersteller, Mess- und Auswerteparameter PSV 10.1)
12. polytec2025com (Hersteller, COM-Steuerung; mit Kennzeichnung als Herstellerfolie)

Ergänzend nicht gezählt: harris2020numpy, virtanen2020scipy, hunter2007matplotlib als Referenzzitate für verwendete Software.

## Volltext benötigt (PDF nach `Input/literatur/`)

| Priorität | bibkey | Grund |
|---|---|---|
| A | rothberg2017ldvreview | Grundlage LDV-Prinzip, vor Aussagen im Exposé lesen |
| A | ewins2000modal | Standardwerk Modaltest; Ausgabe (RSP 2000 vs. Wiley 2009) klären |
| A | bendat2010random | H1/H2, Kohärenz, Schätzfehler |
| A | goege2007gvt | GVT-Praxis Luftfahrt; kein freier Volltext gefunden |
| B | castellini2006ldv, rothberg2012framework, chen2021threesldv | LDV-Stand der Technik, 3D-Zerlegung und Unsicherheit |
| B | harris1978windows, welch1967periodogram, heinzel2002spectrum, brandt2011noise | Fenster/Spektralschätzung |
| B | allemang2003mac, maia1997theoretical | Modalanalyse, MAC |
| B | ecss2012testing / ecss2022testing | Normauszug, welche Prüfarten (Sinus, Modal Survey) abgedeckt sind |
| B | jcgm2008gum, wilson2017goodenough | Unsicherheit und Reproduzierbarkeit |
| B | microsoft2025comoverview | COM-Begriff, Seite nicht abgerufen |
| C | iso2011laservibrometer, pintelon2012system, hammond2000win32, hunter2007matplotlib, harris2020numpy, virtanen2020scipy | ergänzend / Referenzzitate |
| Spezifikation | Polytec: technische Spezifikation PSV QTec 3D (Messbereiche, Bandbreite, Rauschen) | R12 aus Bericht I2; im Input nicht vorhanden, von mir nicht gefunden (nur PSV-500-3D-Produktseite auf polytec.com) |

## Lücken (keine belastbare Quelle gefunden)

1. Messunsicherheit/Fehlerfortpflanzung speziell für 3D-Scanning-LDV (nur Hinweise: Rothberg/Tirabassi 2012; Rohe/Witt, Sandia, Strahlausrichtung per Photogrammetrie, Quelle nicht verifiziert; Martarelli et al. 2001 nicht abschließend geprüft).
2. Prüfstandsautomatisierung / Messwarteschlange / Python-Instrumentensteuerung als begutachtete Quelle.
3. Luftfahrt-Norm oder Richtlinie zum Ground Vibration Test (außer Konferenzbeitrag Göge et al.).
4. Polytec-Spezifikation PSV QTec 3D (Verfügbarkeit beim Betreuer/Polytec erfragen).
5. Direkter Abruf der Verlagsseiten/DOI-Auflösung nicht möglich; DOI bei Castellini 2006, Rothberg/Tirabassi 2012, Chen/Zhu 2021 offen.

---

# Ergänzung Paket L2 (Stand 2026-10-29)

Prüfstand weiterhin **`metadaten`** (Websuche; Verlags-/Katalogseiten nicht direkt abrufbar, siehe Grenzen oben). Neu in `literatur.bib`: 10 Einträge (38 insgesamt).

## Feld A: Automatisierung von Mess- und Prüfabläufen

| Kürzel (`bibkey`) | Quelle | Typ | Relevanz / Kapitel | Zugang | Volltext |
|---|---|---|---|---|---|
| starkey2013labscript | Starkey et al. 2013, Rev. Sci. Instrum. 84(8), 085111 | Artikel | Skriptgesteuerte Experimentautomatisierung in Python (Atomphysik; Prinzipbeispiel, nicht Strukturdynamik) | RWTH; arXiv 1303.0080 frei | benötigt (B) |
| weber2021pymodaq | Weber 2021, Rev. Sci. Instrum. 92(4), 045104 | Artikel | Modulare Messdatenerfassung/Instrumentensteuerung in Python; vergleichbare Architektur (Plugins je Gerät) | RWTH; HAL-Kopie hal-03331919 | benötigt (B) |
| sandve2013tenrules | Sandve et al. 2013, PLOS Comput. Biol. 9(10), e1003285 | Artikel | Reproduzierbarkeit der Auswertung (Skripte, Versionen, Seeds, Rohdaten) | frei (Open Access) | benötigt (B) |
| peng2011reproducible | Peng 2011, Science 334, 1226-1227 | Perspektive-Artikel | Reproduzierbarkeit als Mindeststandard | RWTH | benötigt (C) |
| wilson2017goodenough (aus L1) | siehe Feld 4 oben | Artikel | wie oben | frei | siehe oben |
| (ohne Eintrag) | Steinbauer, „Mechatronic modal hammer“ (Prag, PDF im ZČU-Repositorium dspace5old.zcu.cz/…/Steinbauer.pdf) | Konferenz-/Hochschulbeitrag (vermutet) | Automatischer Modalhammer mit 3D-LDV, 17 h Dauerbetrieb; Automatisierung des Anregungsteils | frei (laut Suche) | **nicht in .bib**: Jahr, Venue, Affiliation (CTU Prag laut Kopfzeile) unbestätigt; (B) |
| (ohne Eintrag) | Titel „Application of a 3D Scanning Laser Doppler Vibrometer on the Automatization of Modal Testing of Turbine Blades“ | unklar (vermutl. Konferenz) | Fast deckungsgleich mit dem Thema (3D-SLDV und Automatisierung, wenige Zeilen Skript für Hammerfolge) | ResearchGate-Eintrag (nicht abrufbar) | **nicht in .bib**: Autoren/Venue/Jahr nicht ermittelt (Suchtreffer ohne Metadaten); im Katalog der UB suchen; (A) |
| (ohne Eintrag) | Martarelli, Revel, Santolini 2001, MSSP 15(3), ab S. 581 | Artikel | Automatisierte Modalanalyse mit SLDV; Scanner-Kalibrierung | RWTH | siehe Feld 1; (C) |
| (nur Hinweis, graue Lit.) | Polytec: RoboVib (3D-SLDV + Industrieroboter), RotoVib, Scalable Automatic Modal Hammer SAM; PSV-Software mit „Open interface“/Polytec File Access und Visual-Basic-Makros | Herstellerwerbung/Produktseiten | Kommerzielle Referenz für automatisierte Modaltests; Marketingaussagen, nicht als Fachbeleg | frei (polytec.com) | nicht zitierfähig als Fachquelle; höchstens mit Vermerk |
| (nur Hinweis, graue Lit.) | PyVISA, PyMeasure, pyEMA, ladisk/sdypy (Python) | Software-/Paketdokumentation | Beispiele für Instrumentensteuerung bzw. Modalanalyse in Python | frei (readthedocs/PyPI) | **keine** begutachtete Publikation gefunden; nur als Softwarehinweis mit Version |

**Einschätzung:** Für „Automatisierte Schwingungs-/Modaltests“ fand ich **keine** begutachtete Übersichtsarbeit; belastbar sind bisher nur Python-Messsteuerung (Starkey, Weber) und Reproduzierbarkeit (Sandve, Peng, Wilson). Das Turbinenschaufel-Paper und Steinbauer müssen erst beschafft/identifiziert werden.

**Empfehlung Exposé (Feld A, 4 Quellen):** weber2021pymodaq, starkey2013labscript, sandve2013tenrules, wilson2017goodenough (Python-Messsteuerung und Reproduzierbarkeit). Die thematisch nächste Quelle (Automatisierung Modaltest mit 3D-SLDV) erst nach Identifikation aufnehmen.

## Feld B: Strukturtests früher und heute (Luft- und Raumfahrt), Kapitel 2.1

| Kürzel | Quelle | Typ | Relevanz / Kapitel | Zugang | Volltext |
|---|---|---|---|---|---|
| ewins2000modal (aus L1) | Ewins, *Modal Testing*, 2. Aufl. | Fachbuch | Standardwerk; Entwicklung von Phasenresonanz- zu FRF-Verfahren | Bibliothek | benötigt (A) |
| irretier2001history | Irretier 2001, „History and development of experimental modal analysis“ (Journal-Angabe unsicher) | Übersichtsartikel | Historische Entwicklung der EMA (inkl. früher Verfahren) | Kasseler Portal/Bibliothek | benötigt (A); Venue klären |
| brown2007modernera | Brown, Allemang, „The modern era of experimental modal analysis: one historical perspective“ (Sound and Vibration, ca. 2007, unsicher) | Übersichtsartikel | Entwicklung von Analogtechnik zu FFT-Analysatoren, MIMO; moderne EMA seit 1970ern | Zeitschrift (sandv.com) / Scribd-Kopie nicht verwenden | benötigt (A); Quellenangaben am Original klären |
| allemang1986survey | Allemang, Brown 1986, IJAEMA 1(1), 37-44 | Übersichtsartikel | Einteilung der Verfahren (u. a. Forced-Normal-Mode, d. h. Phasenresonanz, und FRF-basierte Verfahren) | VT-Archiv (Abstract-Seite); Volltext nicht geprüft | benötigt (B) |
| ewins2016exciting | Ewins 2016, Meccanica 51, 3241-3258 | Übersichtsartikel (Positionspapier) | Rolle des Versuchs vs. Berechnung, aktuelle Herausforderungen (Nichtlinearität, Fügestellen) | frei (Open Access) | benötigt (B) |
| goege2006overview | Göge 2006, „Ground Vibration Testing of Large Aircraft - An Overview of DLR Activities“ | Konferenz-/Vortragsbeitrag | Phasenresonanz vs. Phasentrennung beim GVT (Airbus A380) | DLR elib: kein Volltext; Autor/DLR anfragen | benötigt (A); Venue klären |
| goege2007gvt (aus L1) | Göge et al. 2007, IMAC XXV | Konferenzbeitrag | GVT-Stand der Technik, Verkürzung durch Kombination der Verfahren | siehe L1 | benötigt (A) |
| peeters2009modern | Peeters, Debille, Climent 2008/2009, SAE 2008-01-2270 / SAE Int. J. Aerosp. 1(1) | Artikel | Moderne GVT-Hard-/Software, Kanalzahlen >1000, kurze Testzeiten | SAE (kostenpflichtig; RWTH prüfen) | benötigt (B) |
| rothberg2017ldvreview, castellini2006ldv (aus L1) | siehe Feld 1 | Review/Artikel | Übergang von Kontaktsensorik zur berührungslosen Messung mit LDV | siehe L1 | siehe L1 |
| allemang2003mac (aus L1) | siehe Feld 2 | Artikel | Kennzahl für Modenvergleich, historische Entwicklung (20 Jahre MAC) | siehe L1 | siehe L1 |

**Inhaltlich aus den Suchtreffern nur als Hinweis (nicht belegt, Volltext nötig):** Phasenresonanzverfahren = Anregung zur Isolierung einzelner Moden, zeitaufwändig, aber für zertifizierungsrelevante Moden eingesetzt; Phasentrennungsverfahren = breitbandige FRF-Auswertung, Standard bei großen Luft- und Raumfahrtstrukturen, spart Zeit; kombiniert beim A350 XWB. Quellen der Zusammenfassungen: DLR-elib-Abstracts (Göge 2006, 2007), ONERA-Folien „GVT Ground Vibration Testing Methods“ (graue Literatur, nicht aufgenommen).

**Empfehlung Exposé (Feld B, 4 Quellen):** ewins2000modal (bereits in L1), irretier2001history oder brown2007modernera (nach Klärung der Angaben), goege2006overview bzw. goege2007gvt, ewins2016exciting. Hinweis: Für „Stimmgabel“/frühe Verfahren (Resonanzprüfung vor den FFT-Analysatoren) habe ich **keine** eigene verifizierte Quelle; sie steht höchstens in den Historienartikeln (Irretier, Brown/Allemang) und ist dort zu lesen.

## Lücken (L2)

1. Keine begutachtete Quelle zu automatisierten Modaltests mit LDV (Turbinenschaufel-Paper und Steinbauer nicht identifiziert).
2. Keine verifizierte Quelle zu historischer Kontaktsensorik/Beschleunigungsaufnehmer und zur Einführung der LDV im Modaltest (außer Rothberg 2017 und Historienartikel).
3. Angaben zu Irretier (Zeitschrift/Band) und Brown/Allemang (Zeitschrift/Jahr/Seiten) sowie Göge 2006 (Venue) unbestätigt.
4. Keine GVT-Norm/Richtlinie gefunden (wie L1).
5. Vornamen bei Peeters/Debille/Climent unbestätigt.

## Volltext benötigt (L2, Ergänzung)

| Priorität | bibkey | Grund |
|---|---|---|
| A | irretier2001history, brown2007modernera | Historische Entwicklung der Modalprüfung (Kapitel 2.1); Metadaten erst am Original klärbar |
| A | goege2006overview | Phasenresonanz vs. Phasentrennung beim GVT; Venue/Volltext über Betreuer bzw. DLR |
| A | (Turbinenschaufel-Paper 3D-SLDV und Automatisierung, Titel siehe oben) | thematisch nächste Quelle zum Paket; erst Bibliografie klären |
| B | ewins2016exciting, allemang1986survey, peeters2009modern | Entwicklung und moderne GVT |
| B | weber2021pymodaq, starkey2013labscript, sandve2013tenrules | Python-Messsteuerung, Reproduzierbarkeit |
| C | peng2011reproducible | ergänzend |
