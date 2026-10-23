<!-- Analysebericht I3 – LaTeX-Vorlage, Richtlinien, Plot- und Präsentationsvorlagen; erstellt im Paket der Input-Sichtung von wissenschaftlicher-autor (sonnet); unverändert übernommen. Pfadangaben zum Scratchpad verweisen auf flüchtige Hilfsdateien der Cloud-Sitzung. -->

# Paket I3: Sichtung der Institutsvorlagen (read-only)

Im Repository wurde nichts angelegt oder geändert. Auszüge liegen nur im Scratchpad `/tmp/claude-0/-home-user/e6b61297-17fb-5003-91f8-95c4534d012c/scratchpad/i3/`. Dort liegt auch ein entpacktes PPTX in `pp/`.

Pfadkürzel: **VL** = `/home/user/BA_Jakob-Busch_P/Input/Templates/LaTeX-Vorlage Wissenschaftliche Arbeit/`, **T** = `/home/user/BA_Jakob-Busch_P/Input/Templates/`.

## Wichtigste Befunde vorab

1. **Die `Richtlinien_fuer_wissenschaftliches_Arbeiten.pdf` ist kein SLA-Dokument.** Sie ist die Richtlinie der „TIME Research Area" der Wirtschaftswissenschaften (Prof. Brettel, Hopp, Paluch, Piller, Salge, Wentzel), Stand September 2016. Das belegen PDF-S. 1, 3 und 40. Sie ist für Betriebswirtschaft geschrieben und widerspricht der SLA-Vorlage in mehreren Punkten (Details in Abschnitt 2). Der Nutzer und der Betreuer müssen klären, was für diese Arbeit gilt.
2. **Die SLA-eigenen Formalregeln stehen in der LaTeX-Vorlage selbst**, nämlich in `VL/APPENDIX/appendix.tex` und `VL/APPENDIX/appendix_content.tex`. Sie sind für eine SLA-Bachelorarbeit die naheliegendere Quelle.
3. **Die Vorlage ist unvollständig.**
   - Es fehlt der Ordner `PICTURES/`. Die Titelseite bindet `./PICTURES/rwth_sla` ein (`VL/CHAPTERS_REST/01_titlepage.tex:4`), der Anhang `PICTURES/Beispiel.eps` (`VL/APPENDIX/appendix.tex:87`). In `Input/` gibt es keine EPS- oder Logo-Datei.
   - Ohne das Logo bricht die Kompilierung an der Titelseite ab.
   - `VL/BIB_AND_GLOSSARY/Biblio.bib` enthält nur Beispieldaten (Flugregelung).
4. **Aktualität der Vorlage ist unklar.**
   - `T/HIER AKTUELLE LATEXVORLAGE EINFUEGEN.txt` hat 0 Byte.
   - Die Vorlage enthält die neue KI-Erklärung (`03_integrity.tex`), das Thema „KI" in den Richtlinien-PDF fehlt dagegen ganz.
   - `Preambel_main.pdf` wurde mit MiKTeX 26.5 am 08.07.2026 erzeugt. Das spricht für einen jungen Stand, ist aber kein Nachweis.
   - Das README nennt als Quelle `git-ce.rwth-aachen.de/sla-software/lehre/vorlage_wissenschaftliche_arbeit` (`VL/README.md`, Abschnitt „Download template").
5. **Im Container ist kein LaTeX installiert**, nur `pdftotext`. Kompilieren ist hier nicht möglich.

---

## 1. LaTeX-Vorlage (A1)

### Aufbau
- `Preambel_main.tex` (254 Zeilen) ist die Hauptdatei. `\documentclass[a4paper,12pt,titlepage,twoside,DIV=14,BCOR=6mm,parskip=half,numbers=noenddot,headings=small,headsepline=.4pt,cleardoublepage=empty]{scrbook}` steht in Z. 34–45, also KOMA-Script scrbook, zweiseitig, 12 pt.
- `SETTINGS/`:
  - `packages_set.sty`
  - `better_symbols.sty`
  - `better_units.sty`
  - `document_info.sty`
  - `layout_set.sty`
  - `glossary_set.sty`
  - `biblatex_set.sty`
  - `pdf_set.sty`
- `CHAPTERS_REST/`:
  - `01_titlepage`
  - `03_integrity` (KI-Erklärung)
  - `04_abstract_de`
  - `05_abstract`
  - `06_preface` (optional, auskommentiert)
  - Die Nummer 02 fehlt.
- `CHAPTERS_CONTENT/`: sechs Kapiteldateien (siehe unten).
- `BIB_AND_GLOSSARY/`: `Biblio.bib` und `Input_glossaries.tex`.
- `APPENDIX/`:
  - `appendix_content.tex` (Tipps zum Verfassen)
  - `appendix.tex` (formale Fragen)
  - `appendix_matlab.tex` (auskommentiert)
- `DATA/`: MATLAB-Plotvorlage.
- `MISC/StudentischeArbeit.txsprofile`, ein TeXstudio-Profil (nochmals im Wurzelordner `T/`).
- `compile.sh`, `compile.bat`, `cleanup.sh`, `cleanup.bat`, `README.md`, `README_MAC.md`.
- Dateien liegen mit CRLF-Zeilenenden vor. Die Kodierung ist UTF-8 (`file`), nur einzelne Kommentare in `document_info.sty` sind kaputt kodiert.

### Kapitelstruktur der Vorlage (`Preambel_main.tex:165–248`)
Reihenfolge:
1. Titelseite
2. KI-Erklärung (immer Deutsch, Z. 173–179, mit Unterschriftszeile)
3. Kurzfassung (DE)
4. Abstract (EN)
5. optional Vorwort (Z. 193, auskommentiert)
6. Inhaltsverzeichnis
7. Abkürzungsverzeichnis
8. Symbolverzeichnis
9. Indizes
10. Kapitel 1–6
11. Literaturverzeichnis
12. Anhang

Abbildungs- und Tabellenverzeichnis sind per Chef-Vorgabe ausgeschaltet (Z. 204–205: „Wollte der Chef streichen"). Die Kapitel sind:

| Datei | Kapitel | Vorgaben der Vorlage |
|---|---|---|
| `01_introduction.tex` | Einleitung | Zielsetzung, Stand der Technik (kurz), Übersicht; Richtwert ca. 1–2 Seiten |
| `02_stateofart.tex` | Stand der Technik | bezogen auf Zielsetzung; Potenzial, das die Arbeit rechtfertigt |
| `03_theory.tex` | Methodik / Entwicklung der Methodik | Grundlagen nur, wo sie über die tägliche Arbeit eines Strukturmechanik-Ingenieurs hinausgehen; „Von Experten – Für Experten! / So wenig wie möglich und so viel wie nötig!" |
| `04_execution.tex` | Umsetzung der Methodik | Hilfsmittel samt Einstellungen; alle Daten müssen reproduzierbar ersichtlich sein |
| `05_implementation.tex` | Analyse und Auswertung der Ergebnisse | Randbedingungen, kritische Analyse, Unsicherheiten und Fehler |
| `06_conclusion.tex` | Schlussfolgerung und Ausblick | Rückbezug auf Zielsetzung (BA); Leitfragen: Was wurde gemacht? Hauptergebnisse? Ziel erreicht, wenn nein warum nicht? Forschungsbedarf? |

Weitere Vorgaben stehen im Kurzfassungs-Text (`04_abstract_de.tex`):
- höchstens eine DIN-A4-Seite
- keine Formeln, keine Literaturhinweise
- optional 1–2 Bilder
- etwa fünf Schlagwörter in alphabetischer Reihenfolge

Das Vorwort ist laut `06_preface.tex` bei internen Arbeiten nicht zulässig.

### Compiler und Pakete
- **Compiler:** pdfLaTeX. Der Standardcompiler ist laut `README.md` („Old-README") pdfLaTeX, nicht LuaLaTeX.
- **Literatur:** biber. `biblatex_set.sty:1–4` lädt `style=numeric, subentry, sorting=none, backend=biber`. Die Sortierung erfolgt also nach Zitierreihenfolge, die Zitate sind nummerisch ([1]). Autorennamen stehen in Kapitälchen (Z. 8). Dazu kommen Feldformate für Titel (Z. 11–21).
- **Glossare:** Paket `glossaries` (`nomain,acronym,nostyles`, versionsgebunden `[=v4.49]`, `glossary_set.sty:5`), aber **nicht** `makeglossaries`, sondern manuelle `makeindex`-Aufrufe (`compile.sh:8–12`). Es gibt drei Verzeichnisse:
  - Akronyme (Stil `acrolongcol`)
  - Symbole (`notation`, Stil `symlongcolgrskip`; Spalten Zeichen, Einheit, Beschreibung; getrennt in Lateinisch und Griechisch)
  - Indizes (`subscripts`)
  - Einträge stehen in `BIB_AND_GLOSSARY/Input_glossaries.tex`. Sie erscheinen nur, wenn sie im Text mit `\gls`/`\glsadd` aufgerufen werden, sonst per `\glsaddall`.
- **Schrift und Mathematik:**
  - `mathpazo` (Palatino) mit `pslatex`. `fontenc T1` ist auskommentiert (`packages_set.sty:24`), das kann die Silbentrennung mit Umlauten beeinträchtigen.
  - `amsmath`, `mathtools`, `fixmath`.
  - Weitere Pakete: `tikz`, `booktabs`, `tabularx`, `longtable`, `tabu`, `multirow`, `caption`, `subfig`, `varioref`, `hyperref`, `csquotes`, `pdfpages`.
- **Einheiten:** `better_units.sty` lädt `siunitx` (Z. 1) und setzt die Locale aus `\mylanguage`: UK bei `british`, DE bei `ngerman`. Es bricht mit Fehler ab, wenn die Sprache anders ist (Z. 12–18).
  - `per-mode=symbol-or-fraction`
  - `product-units=single`
  - `bracket-unit-denominator=true`
  - `scientific-notation=true` (Z. 20–25)
  - Der Dezimalmarker folgt damit der Sprache. Das passt zu „Dezimalkomma im deutschen Text".
- **Symbole:** `better_symbols.sty` definiert aus cmex ein größeres Summenzeichen `\Xsum` und überschreibt `\sum` damit (Z. 46–47). Im Anhang wird `\Xsum` als bevorzugt bezeichnet (`appendix.tex`).
- **Sprache:** `\newcommand{\mylanguage}{british}` steht in `Preambel_main.tex:46`. Für eine deutsche Arbeit muss das auf `ngerman` gestellt werden. Das README gibt als Zeilen 66 und 198 an, tatsächlich sind es Z. 46 (Definition), Z. 69 und Z. 199 (`\selectlanguage`).
- **Hyperref:** `pdf_set.sty`. Der PDF-Titel wird aus `document_info.sty` gebildet. `draft=false` ist die Anzeigeversion, für die Druckversion ist `draft=true` zu setzen (Hinweis in `Preambel_main.tex:109`). Links sind farbig (`colorlinks=true`).
- **Kapitelnummerierung:** `layout_set.sty:56–57` setzt `tocdepth=1` und `secnumdepth=2`. Das Inhaltsverzeichnis zeigt also Kapitel und Abschnitte, nummeriert wird bis 1.1.1. Der Anhangstext erlaubt Unterkapitel „bis zur vierten Stufe" (`appendix_content.tex`), dafür müsste `secnumdepth` erhöht werden.
- **Kopfzeile und Layout:**
  - Kopfzeile mit Kapitel- bzw. Abschnittsmarke und Seitenzahl (`layout_set.sty:29–33`)
  - Zeilenabstand `\linespread{1.05}` (Z. 19)
  - Schusterjungen und Hurenkinder werden mit Strafen 10000 unterdrückt (Z. 58–62)
- **Querverweise:** `varioref` mit Sprache aus `\MyVariorefLanguage`. Abbildungen heißen bei `ngerman` „Abb.", bei `british` „Fig." (`packages_set.sty:62–70`). Die Bildunterschrift hat `format=hang, margin=10pt, font=small`.

### Zitierstil
Numerisch mit eckigen Klammern, nach Zitierreihenfolge sortiert (`biblatex_set.sty:1–4`). Das Beispiel steht in `appendix.tex`: `\cite{DOWELL2004}` und `\textcite{...}` für den Autor als Satzsubjekt. `Preambel_main.tex:236` hat `\nocite{*}`, das für die echte Arbeit auskommentiert werden muss („BITTE AUSKOMMENTIEREN FUER DIE ARBEIT", Z. 237–238). Das bestätigt `README_MAC.md`.

Die Überschrift des Literaturverzeichnisses ist hartkodiert englisch (`\renewcommand{\bibname}{Bibliography}`, `biblatex_set.sty:8`, und `\addcontentsline{...}{Bibliography}`, `Preambel_main.tex:235`). Für eine deutsche Arbeit ist das anzupassen. Die Ablaufspalten in den Glossaren sind dagegen zweisprachig.

### Abbildungen
- `\figure` mit `\includegraphics` aus `PICTURES/` (Format .eps oder .png, `epstopdf` ist geladen). Das Beispiel ist `\includegraphics[scale=0.71]{PICTURES/Beispiel.eps}` (`appendix.tex:87`).
- Der Text nennt kleingeschrieben `pictures/` (Z. 84), der Code `PICTURES/`. Auf Linux zählt die Groß-/Kleinschreibung, daher einheitlich wählen.
- **Skalierungsregel (`appendix.tex`):** Bei Strichbreiten 0,35 mm / 0,7 mm und Schrift 16 pt ist die Zeichnung normgerecht. Mit Faktor 1/√2 ≈ 0,71 (`scale=.71`) ergeben sich 0,25 mm / 0,5 mm und 12 pt.
- Tabellen: `booktabs` (`\toprule/\midrule/\bottomrule`), `\captionof{table}` oberhalb, `tabularx` mit `\textwidth-4em`, Maßeinheiten in eckigen Klammern im Kopf.

### `document_info.sty` (Z. 10–52)
Zu füllen sind die Felder mit `XXX-…-XXX`:
- `\mythesistypede` und `\mythesistypeen` (Bachelorarbeit / Bachelor thesis)
- `\mythesisnumber` (Format „BA/PA/MA + Jahr – Nummer", z. B. „BA2019-06")
- `\mythesistypeshort`
- `\mytitlede`, `\mytitleen`, `\mytitleshort`
- `\mysurname`, `\myname`, `\myemail`, `\mymatrnr`
- `\mydeadlineMonth`, `\mydeadlineYYYY`
- `\myadvisorone`
- optional `\mykeywords`

Bereits gesetzt sind Institut, Fakultät (Fakultät für Maschinenwesen), Ort Aachen und Prof. Dr.-Ing. Kai-Uwe Schröder. `\myadvisortwo` und `\myadvinsttwo` werden nur bei einem zweiten Betreuer benötigt.

Die Titelseite (`01_titlepage.tex`) verwendet **immer die englischen Felder** `\mythesistypeen` und `\mytitleen`. Auch bei einer deutschen Arbeit muss der englische Titel gepflegt werden, oder die Titelseite ist anzupassen. Der Satz „Thesis presented at the …" kommt aus dem Sprachzweig von `\iflanguage` in `document_info.sty`.

### `Preambel_main.pdf`
Vorhanden, 40 Seiten, A4, MiKTeX 26.5, 08.07.2026, ausgefüllt mit Platzhaltern. Es zeigt die Titelseite, die KI-Erklärung, Kurz- und Abstract, Inhaltsverzeichnis, die drei Verzeichnisse, die Kapitel mit Blindtext und die Anhänge (Tipps und Formale Fragen). Inhaltlich enthält es die Texte, die auch in den `.tex`-Dateien stehen. Es gibt keine zusätzlichen Hinweise.

`VL/Preambel_main.log` ist **ein anderer Lauf (11:25) und endet fehlerhaft**:
- `! Argument of \reserved@a has an extra }` (Log Z. 1818, 1842)
- `! TeX capacity exceeded, sorry [input stack size=10000]` bei `\begin{document}` (Log Z. 2123), verbunden mit `\extrasenglish`/`varioref`
- „no output PDF file produced" (Log Z. 2140)

Das PDF stammt also von einem früheren erfolgreichen Lauf. Ob die Vorlage mit aktuellem TeX Live/MiKTeX fehlerfrei läuft, ist nicht geklärt (kann ein Kompatibilitätsproblem von `varioref` mit Sprachumschaltung `british`/`ngerman` sein; Annahme, nicht geprüft).

### Build-Artefakte, die nicht ins Repo gehören
- Im Upload liegen versehentlich eingecheckt: `Preambel_main.aux`, `.log`, `.syg1`, `.syg2`, `.acn`, `CHAPTERS_*/*.aux`, `APPENDIX/*.aux`.
- `cleanup.sh` löscht: `*.acn *.acr *.alg *.aux *.bbl *.bcf *.blg *.ist *.log *.out *.xml *.slg1 *.slg2 *.syg1 *.syg2 *.syi1 *.syi2 *.toc`.
- Das README empfiehlt zusätzlich einen gitignore (siehe A3).
- Das PDF `Preambel_main.pdf` ist ein erzeugtes Artefakt und im Template-Ordner nur Referenz.

---

## 2. Richtlinien-PDF (A1, mit Seiten)

Zählung: PDF-Seite (gedruckte Seitenzahl). Die gedruckte Zahl ist im Hauptteil die PDF-Seite minus 2.

**Geltungsbereich:** Die Richtlinien sind die Anforderungen „der TIME Research Area" und können Abweichungen vom Merkblatt der Fakultät für Wirtschaftswissenschaften enthalten (PDF-S. 3 (1)). Ein Bezug auf SLA oder die Fakultät für Maschinenwesen fehlt. Die Beispiele sind betriebswirtschaftlich.

**Aufbau und Gliederung**
- Ordnungsschema: Deckblatt, Inhaltsverzeichnis, ggf. Abbildungs-/Tabellenverzeichnis, ggf. Abkürzungsverzeichnis, Text, ggf. Anhang, Literaturverzeichnis, Versicherung (PDF-S. 17 (15)).
- Gliederung unbedingt mit dem Betreuer besprechen (PDF-S. 17 (15)).
- Gliederungstiefe höchstens drei Ebenen; Nummerierung 1 / 1.1 / 1.1.1 ohne Schlusspunkt; ein Kapitel hat mindestens zwei Unterkapitel; ein Abschnitt hat 0,5 bis ca. 2 Seiten; Überschriften prägnant und nicht als ganzer Satz (PDF-S. 17–18 (15–16)).
- Einleitung (PDF-S. 19 (17)): Problemstellung, Zielsetzung, Relevanz, Ausgangssituation/Forschungsstand, Vorgehen; 1–3 Seiten.
- Hauptteil: roter Faden, Exkurse vermeiden, kurze Überleitungen (PDF-S. 19 (17)). Schluss: Fazit, Beantwortung der Fragestellung, kritische Würdigung, Limitationen, Ausblick (PDF-S. 20 (18)).
- Anhang nicht zwingend; Abbildungen und Tabellen stehen grundsätzlich im Fließtext (PDF-S. 21 (19)).

**Formalia (PDF-S. 22 (20))**

| Punkt | Vorgabe |
|---|---|
| Papier | DIN A4, einseitiger Druck |
| Schrift | Arial oder Times New Roman, 12 pt, Fußnoten 8–10 pt |
| Zeilenabstand | 1,5-zeilig; Absatz 12 pt vor und nach |
| Ränder | 3 cm links, 2 cm rechts, 3 cm oben, 2,5 cm unten |
| Umfang | **Bachelorarbeit 40 Seiten** (höchstens 10 % Abweichung nach unten) |
| Seitenzahlen | Verzeichnisse römisch; Text arabisch ab 1; Anhang und Literatur wieder römisch; Titelblatt ohne Nummer |
| Abgabe | ausgedruckte Exemplare (Anzahl laut Prüfungsordnung) plus PDF |
| Überschriften | Ebene 1: 18 pt fett; 2: 16 pt; 3: 14 pt; 4: 12 pt fett; 5: 12 pt kursiv (PDF-S. 18 (16)) |

**Abkürzungen** (PDF-S. 22–23 (20–21)): sparsam; beim ersten Auftreten ausschreiben und die Abkürzung in Klammern dahinter; Duden-Abkürzungen nicht ins Verzeichnis; alphabetisches Verzeichnis; keine Doppelbelegung und keine Synonyme für dieselbe Abkürzung.

**Tabellen und Abbildungen** (PDF-S. 23–25 (21–23))
- Sie sind überlegt einzusetzen und immer im Text zu referenzieren und zu erläutern.
- Platzierung nach der ersten Erwähnung.
- Durchgehend nummeriert, mit Titel und Quellenangabe.
- Tabellen haben eine Überschrift, Abbildungen eine Unterschrift.
- Eigene Darstellungen werden mit „eigene Darstellung" gekennzeichnet, leicht veränderte mit „in Anlehnung an".
- Fremde Abbildungen werden grundsätzlich selbst neu erstellt; Kopieren nur mit Absprache.
- Anforderung an grafische Qualität: lesbare Schrift, geeignete Farbwahl, übersichtlich.
- Abbildungs-/Tabellenverzeichnis: Nummer und Titel links, Seitenzahl rechts (PDF-S. 25 (23), Muster Anhang 4, PDF-S. 43).

**Zitieren** (PDF-S. 26–31 (24–29))
- **Harvard-Zitierweise** im Text (Autor Jahr, S. xx), keine Fußnoten.
- Bei 2 Autoren beide nennen, bei 3 Autoren beim ersten Mal alle und danach „et al.", ab 4 Autoren „et al.".
- Seitenangaben „S. 75f." oder „S. 75ff.".
- Wörtliche Zitate sparsam und unverändert in Anführungszeichen; sinngemäße Zitate mit Kennzeichnung des Umfangs; Sekundärzitate nur im Notfall („zit. nach").
- Literaturverzeichnis **alphabetisch nach Autoren**, alle Autoren nennen, Formate je Quellentyp (Aufsatz, Monographie, Sammelwerk, Bericht, Konferenz, Internet mit Abrufdatum). Internetquellen sollen gespeichert werden.
- Quellenzahl: **mindestens so viele Quellen wie Seiten** (PDF-S. 4 (2)).
- Unangemessene Quellen: Working Paper, Vorlesungsfolien, Wikipedia, allgemeine Lexika (PDF-S. 4 (2)).
- Fachzeitschriften nach dem VHB-Jourqual-Ranking (betriebswirtschaftlich, für Technik nicht anwendbar) (PDF-S. 5 (3)).

**Versicherung** (PDF-S. 21 (19); Anhang 7, PDF-S. 47): jede Arbeit schließt mit einer Versicherung ab. Ist sie fehlerhaft oder unvollständig, kann die Arbeit als Täuschungsversuch mit „nicht ausreichend" bewertet werden. Nach Anhang 7 ist die eidesstattliche Versicherung gesondert einzureichen und nicht mehr in die Arbeit einzubinden (§ 18 Abs. 1 S. 4 ÜPO).

**Bewertungskriterien** (Checkliste, PDF-S. 34–38 (32–36)):
- Themenerfassung, Strukturierung, Literaturbasis und Formalia sind „Grundvoraussetzung".
- **„Inhalt und Argumentation" ist der zentrale Bewertungsaspekt** (PDF-S. 37–38 (35–36)). Die Gewichtung richtet sich nach der Arbeit.
- Weitere Prüfpunkte: Jede Aussage mit mindestens einer Quelle belegt; Abbildungen lesbar; alle Verweise existieren; Seitenzahlen bei Zitaten; keine doppelten Leerzeichen; sparsamer Umgang mit Abbildungen und Tabellen; Definitionen sachgerecht; kritischer Umgang mit eigener Lösung; Aufzeigen verbleibender Lücken.

**KI / Hilfsmittel:** Die Richtlinien erwähnen KI **nicht**. Die Versicherung (PDF-S. 47) sagt nur „ohne Benutzung anderer als der angegebenen Hilfsmittel". Die KI-Regeln stehen allein in `VL/CHAPTERS_REST/03_integrity.tex` (siehe Abschnitt A2).

**Widersprüche Richtlinien ↔ SLA-Vorlage**

| Thema | Richtlinien (WiWi) | SLA-Vorlage |
|---|---|---|
| Zitierstil | Harvard (Autor Jahr), Literatur alphabetisch | numerisch `[1]`, Sortierung nach Zitierreihenfolge |
| Schrift | Arial/Times, 12 pt, 1,5-zeilig | Palatino 12 pt, `\linespread{1.05}` |
| Umfang BA | 40 Seiten | „< 50 Seiten ohne Anhang" (`appendix_content.tex`) |
| Druck | einseitig | `twoside` (buchartig) |
| Ränder | 3/2/3/2,5 cm | KOMA DIV=14, BCOR 6 mm |
| Versicherung | Anhang 7 (eidesstattlich, gesondert) | KI-Erklärung als Seite 2 in der Arbeit |
| Verzeichnisse | Abbildungs-/Tabellenverzeichnis „ggf." | per Vorgabe des Chefs gestrichen |
| Gliederungstiefe | höchstens 3 Ebenen | Unterkapitel bis 4. Stufe zulässig |

Empfehlung: Wo sich beide widersprechen, gilt die SLA-Vorlage. Das ist eine **Annahme**, die der Betreuer bestätigen muss (siehe A4).

---

## 3. Plot-Gestaltungsregeln (A1, ableitbar für matplotlib)

**Quellen:**
- `VL/DATA/MATLAB_Plot_Vorlage_SLA_2015_11_11.m` (Stand Nov 2015, Autorin J. Schlupkothen)
- `T/gnuplot_Vorlagen/Gnuplot_Demo.gp`
- Anhangstext `VL/APPENDIX/appendix.tex`

**Schrift**
- Isonorm3098 (ISO 3098) in `T/ISONORM3098_Schriften/` (`Ison___.ttf` Regular, `IsonI__.ttf` Italic, `IsonM__.ttf` Monospaced, `IsonIM_.ttf` Italic Monospaced, `IsonGrSymb.ttf` griechische Symbole). Gnuplot enthält zusätzlich `.pfb/.pfa` (Type 1).
- MATLAB: Achsen- und Beschriftungsschrift **9,5 pt**, `FontWeight normal`, `Fontname 'Isonorm3098'` (Z. 49–55). Gnuplot: `Isonorm3098,12` bei 1024×768 Pixeln (Z. 17).
- Alternativschrift laut Vorlage: IsonormD (Freeware) (MATLAB-Z. 11–12).
- Die Schrift trägt ein Copyright („Copyright 1993 Robert Kirchner, published by FontShop International", in der TTF-Metadatenspalte nachgewiesen). Ob sie im Repo weitergegeben werden darf, ist unklar.

**Größen und Export**
- MATLAB: Papierformat 16 × 10 cm, `PaperUnits centimeters`, Export `print -dpng -r300` (Z. 29–32, 59). LaTeX-Hinweis: Textbreite 16 cm, Texthöhe 22,5 cm (Z. 22), `width=.96\textwidth`; zwei Plots pro A4-Seite lassen noch Platz für eine zweizeilige Unterschrift.
  Die 16 cm Textbreite ergeben sich auch rechnerisch aus KOMA (DIV=14, BCOR=6 mm: etwa 160 mm). Das ist von mir gerechnet und nicht kompiliert.
- Seitenverhältnis in Gnuplot: `set size ratio 0.71` (Z. 37), also ≈ 1/√2.
- Alle Diagramme müssen nach `appendix.tex` **inklusive Unterschrift bei Verkleinerung auf A5 lesbar** bleiben.
- Falls Vektorgrafik: Strichbreitensatz 0,35 / 0,7 mm bei 16 pt Schrift, skaliert mit 1/√2 auf 0,25 / 0,5 mm und 12 pt. Die Schrift im Plot soll also so gewählt werden, dass sie im Dokument bei 12 pt Fließtext etwa 12 pt (bzw. 9,5 pt bei MATLAB-PNG) erscheint.

**Linien, Marker, Farben**
- MATLAB: Linienbreite 1, Markergröße 5, **schwarz mit gefüllten Markern**, Marker in der Reihenfolge `s d v ^ > < o *` (Z. 35–36, 45–48). Kommentar: „Vermeiden von Farben, um Druckbarkeit in S/W zu gewährleisten. Stattdessen mit unterschiedlichen Markern arbeiten" (Z. 24–26).
- Gnuplot: 17 `line styles` mit Kombinationen aus Farbe (`colorsequence default/podo/classic`), Strichlinie (`dt 2`, `dt 4`) und Punkttyp. Die Datenreihen haben Linien plus Punkte (`with linespoints`). Gestrichelte Hilfslinien und Pfeile `lw 1`.
- Anhang: Farben müssen im Graustufendruck keine Information verlieren; **Gelb ist unzulässig**; Rot-Grün-Sehschwäche berücksichtigen (`appendix.tex`, Abschnitt „Formale Fragen"). `podo` in Gnuplot ist die farbenblindheitstaugliche Palette.

**Achsen, Gitter, Legende**
- Beschriftung `Text [Einheit]` mit **eckigen Klammern** (MATLAB-Z. 49, Gnuplot `Weg [mm]`, `Kraft [kN]`).
- Gitter an, in Gnuplot gepunktet (`set grid lt 0 lw 0.709`), Rahmen/Box an (`box on`, `set border 31 lw 0.992`).
- Ticks nach innen, an der Gegenseite gespiegelt, Nebenticks (`set tics in`, `mxtics`, `mytics`, `mirror`).
- Zahlenformat `%g` (Z. 53–54). Das Dezimaltrennzeichen soll der Sprache der Arbeit folgen; englisches Format in Grafiken ist in deutschen Arbeiten zulässig, wenn anderes unverhältnismäßigen Aufwand bedeutet (`appendix.tex`, Tabelle `Trennzeichen`).
- Legende: oben links, mit Rahmen (`Northwest`, `box on`; Gnuplot `top left box opaque`).
- Kein Plot-Titel (`#set title` auskommentiert); die Aussage steht in der Bildunterschrift.
- Zahlen von eins bis zwölf werden im Text ausgeschrieben, ab 13 nicht (`appendix.tex`).

**Für matplotlib zu übernehmen (Vorschlag):**
- Isonorm3098 per `font_manager.addfont` einbinden, 9,5 pt, `box` an
- 16 cm Breite (oder `.96\textwidth`), Seitenverhältnis 0,71
- 300 dpi PNG (und zusätzlich PDF/EPS als Vektor)
- Schwarz/Grau mit Markerfolge `s d v ^ > < o *` und Linienstilen statt Farben, falls Farben nötig: farbenblindheitstaugliche Palette (z. B. Okabe-Ito), ohne Gelb, und in Graustufen unterscheidbar
- Gitter an, Ticks innen und gespiegelt, Legende oben links mit Rahmen, Achsen „Größe [Einheit]"
- matplotlib ist im Container nicht installiert (nicht geprüft, ob in `software/` vorgesehen).

---

## 4. PowerPoint-Vorlagen (A1)

In `T/Powerpoint_Vorlagen/`:
- `16-9_vorlage_Praesentation_SLA_20191213.pptx` (421 KB, Stand 13.12.2019): 16:9, 14 Beispielfolien („n von 14") und 14 Layouts (u. a. `Titel_1/3 Farbe`, `Titel_1/3 Foto`, `Titel_2/3 Foto`, `Titel_Text`, `Inhalt_Aufzählung`, `Inhalt_Text`, `Inhalt_Text_Bild`, `Inhalt_Bild`, `Inhalt_Diagramm`, `Abschlussfolie`, `Titelfolie`). Theme-Schrift Arial; RWTH-Farbpalette (z. B. Blau `00549F`, Türkis `0098A1`, Grün `57AB27`, Rot `CC071E`).
- `RWTH-Addin-Seitenzahlen.ppam`: PowerPoint-Add-in für Seitenzahlen („n von N").
Das Material ist für Zwischen- und Abschlussvortrag verwendbar.

---

## 5. LaTeX im Container (A1)

Keine Installation: `which pdflatex lualatex biber xelatex bibtex makeglossaries makeindex latexmk kpsewhich` liefert nichts (nur `pdftotext` ist vorhanden). Das System ist Ubuntu 24.04, Python-Pakete `python-pptx` sind vorhanden, `matplotlib` nicht. Ich habe nichts installiert.

**Zum Kompilieren nötig** (nur festgestellt):
- TeX Live (z. B. Pakete `texlive-latex-extra`, `texlive-science`, `texlive-lang-german`, `texlive-fonts-recommended`/`texlive-fonts-extra`, `texlive-bibtex-extra`) bzw. `texlive-full`
- `biber` (die Vorlage nennt sinnvollerweise `pdflatex`, `biber`, `texlive`)
- `makeindex`
- Rechte zum Installieren (`apt`, Root ist vorhanden, Netzwerk-Proxy konfiguriert)
- Die Pakete `tabu`, `mdwlist`, `anysize`, `ae`, `pslatex`, `subfig`, `glossaries` (auf Version 4.49 festgelegt) sind alt und können in neuem TeX Live Warnungen oder Fehler erzeugen. Bis die Vorlage getestet ist, bleibt das offen.
- Das Logo `PICTURES/rwth_sla.*` muss vorliegen.

---

## A2. Verbindliche Vorgaben zur Übernahme (Vorschlag)

Reihenfolge nach Verlässlichkeit: Aus der SLA-Vorlage zuerst, aus den Richtlinien nur nach Bestätigung durch den Betreuer.

**Aus der SLA-Vorlage (vermutlich verbindlich)**
1. **Sprache und Stil** (`appendix_content.tex`): 3. Person Singular, **durchgängig Präsens** (Präteritum im Durchführungsteil gilt ausdrücklich als Fehler), aktive Formulierung, Indikativ statt Konjunktiv. Abkürzungen außerhalb des Dudens werden eingeführt. Kurze Sätze, einheitliches Fachvokabular, Kapiteleinleitung und -abschluss mit ein bis zwei Sätzen.
   Das betrifft den `wissenschaftlichen-autor` direkt: Ein Kapitel „Durchführung" im Präteritum entspräche nicht der Vorlage.
2. **Umfang:** Bachelorarbeit **unter 50 Seiten ohne Anhang** (`appendix_content.tex`).
3. **Zahlen:** Eins bis zwölf ausgeschrieben, ab 13 Ziffern (`appendix.tex`).
4. **Abbildungen:** Farbe darf im Graustufendruck keine Information tragen; kein Gelb; Rotgrünsehschwäche beachten; A5-Lesbarkeit inklusive Unterschrift; Strichbreiten-/Schriftsatz nach Abschnitt 3.
5. **Formeln:** Multiplikationspunkt statt Stern; Differentialoperator und Einheiten aufrecht (`\mathrm`, `\operatorname{d}`); im abgesetzten Text horizontaler Bruchstrich, im Fließtext Schrägstrich ohne `sfrac` (`N/mm^2`); Summenzeichen `\Xsum`; Dezimal- und Tausendertrennung nach der Sprache der Arbeit (Deutsch: Komma, Punkt).
6. **Gliederung:** höchstens vierte Stufe; neue Stufe nur bei mindestens zwei Einträgen; Tabellenform für Ergebnisse, Versuchspläne, Maschinendaten statt Aufzählung im Fließtext; „So wenig wie möglich, so viel wie nötig"; Grundlagen nur, soweit sie über die tägliche Arbeit eines Strukturmechanik-Ingenieurs hinausgehen (`03_theory.tex`).
7. **Kapitelzuschnitt:** Kapitel 1–6 der Vorlage (siehe Abschnitt 1). Einleitung etwa 1–2 Seiten. Kapitel 4 muss alle Daten und Einstellungen reproduzierbar nennen (`04_execution.tex`), das passt zu den Versuchsprotokollen. Kapitel 5 braucht Unsicherheiten und Fehler.
8. **Kurzfassung** (DE) und **Abstract** (EN): jeweils höchstens eine Seite, ohne Formeln und Literaturhinweise, fünf Schlagwörter alphabetisch.
9. **KI-Erklärung** (`03_integrity.tex`, vom Zentralen Prüfungsamt gefordert): Tabelle „Abschnitt der Arbeit / Einsatzzweck", wo KI Text oder Bilder erzeugt oder bearbeitet hat; ausgenommen sind Grammatik-, Stil-, Rechtschreibprüfung und Übersetzung. Der Nutzer bestätigt, jedes KI-Ergebnis gründlich zu prüfen und die Verantwortung zu übernehmen. **Die ungeprüfte Übernahme von Halluzinationen wird als Täuschungsversuch gewertet.**
   Für dieses Projekt ist das zentral: Alle Rohfassungen des `wissenschaftlichen-autors`, KI-gestützten Abbildungsskripte und der KI-geschriebene Code müssen hier (Seiten/Unterkapitel/Abbildungen) benannt werden. Ich schlage vor, dass der Orchestrator ein Register der KI-Nutzung (Abschnitt, Zweck) fortlaufend führt, z. B. aus `kapitel-map.md` und den Laborbucheinträgen.
10. **Literatur:** numerisch mit biblatex/biber, `\nocite{*}` entfernen, `\textcite` für Autor als Satzsubjekt.

**Aus den Richtlinien (nur nach Bestätigung des Betreuers)**
- Alle Aussagen belegen; Quellen im Text und im Verzeichnis müssen übereinstimmen; Seitenzahlen bei wörtlichen und sinngemäßen Zitaten (S. 33/35 PDF).
- Eigene Darstellungen als „eigene Darstellung" kennzeichnen, veränderte als „in Anlehnung an" (PDF-S. 24 (22)). Fremde Abbildungen nicht kopieren, sondern selbst erstellen.
- Abbildungen und Tabellen nummerieren, im Text erläutern, nach erster Nennung platzieren, nie unkommentiert.
- Keine Wikipedia, keine Vorlesungsfolien, keine Working Paper als Quelle.
- Quellenzahl ≥ Seitenzahl (bei etwa 40–50 Seiten also etwa 40–50 Quellen). Das ist für eine Software-/Messtechnikarbeit anspruchsvoll; Rücksprache nötig.
- Internetquellen mit Abrufdatum und lokal gesichert.
- Abkürzungen beim ersten Auftreten ausschreiben; keine Mehrfachbelegung von Symbolen.
- Bewertungslogik: Inhalt und Argumentation zählen am meisten.

**Wo übernehmen**
- `KONVENTIONEN.md` (Abschnitt neu „Thesis-Formalia"): Punkte 1–8 und 10 aus der Vorlage. Der Nutzer entscheidet, ob sie dauerhaft gelten.
- Agentendefinition `wissenschaftlicher-autor`: Präsens und 3. Person; Zahlenregel; Formelregeln; Zitierbefehle (`\cite`, `\textcite`); Länge unter 50 Seiten.
- Agent `thesis-gutachter`: Prüfliste aus Punkten 1–10 und den Kontrollfragen in `appendix_content.tex`.
- Plotstil in `software/`: Abschnitt 3.

---

## A3. Vorschlag für den Aufbau von `in_progress/thesis/` (nur beschrieben)

`in_progress/thesis/` ist leer. `in_progress/thesis/KONVENTIONEN.md` existiert nicht (die Datei liegt im Projektstamm).

1. **Vorlage übernehmen** (nach Klärung der aktuellen Version, siehe A4): Inhalt von `VL/` nach `in_progress/thesis/` kopieren, **ohne** `Preambel_main.pdf`, `*.aux`, `*.log`, `*.syg*`, `*.acn` und ohne `.gitkeep`. Die Datei `Preambel_main.tex` könnte in `main.tex` umbenannt werden. Dann müssen `compile.sh`, `cleanup.sh` und `.txsprofile` mitgezogen werden. Alternativ den Namen belassen, damit spätere Vorlagenupdates leicht vergleichbar bleiben (Empfehlung).
2. **Fehlende Teile ergänzen:** `PICTURES/` mit RWTH-SLA-Logo (`rwth_sla`) und, falls der Anhang bleibt, `Beispiel.eps`. Ordner `abbildungen/` (laut `KONVENTIONEN.md` des Projekts Ausgabeort der Skripte) anlegen und in `Preambel_main.tex` dem Suchpfad hinzufügen (`\graphicspath{{abbildungen/}{PICTURES/}}`), damit die Konvention „Ausgaben unter `in_progress/thesis/abbildungen/`" und die Vorlage zusammenpassen. Hier ist zu klären, ob der Ordnername der Vorlage (`PICTURES/`) bleibt.
3. **Einstellungen:**
   - `\mylanguage` auf `ngerman` (`Preambel_main.tex:46`).
   - `document_info.sty` mit den Feldern aus Abschnitt 1 füllen. Titel auch englisch, da die Titelseite die englischen Felder nutzt; sonst Titelseite anpassen.
   - `\nocite{*}` auskommentieren (Z. 236).
   - `\bibname` und das `addcontentsline`-Label auf „Literaturverzeichnis" ändern.
   - `draft=true` in `pdf_set.sty` nur für die Druckversion.
   - Vorlagenkapitel durch die Gliederung aus `kapitel-map.md` ersetzen (Dateinamen der Vorlage `01_…` bis `06_…` beibehalten; Kapitel 1–6 passen im Grundsatz zu „Einleitung / Stand / Methodik / Umsetzung / Ergebnisse / Schluss"; die softwarelastige Arbeit braucht evtl. Umbenennung von „Methodik" in Konzept/Entwurf).
   - `Biblio.bib`: Beispieldaten entfernen und stattdessen `in_progress/literatur/literatur.bib` einbinden (`\bibliography{...}` in Z. 134 anpassen oder die Datei in `BIB_AND_GLOSSARY/` ablegen). Ich schlage vor, `literatur.bib` direkt zu referenzieren, damit es nur eine Quelle gibt. Dann `\addbibresource` statt `\bibliography` (Z. 134 verwendet `\bibliography`, ein Befehl, der bei biblatex nur mit Warnung funktioniert; bei der Kompilierung zu prüfen).
   - Glossar: Beispieleinträge (Flugregelung, Indizes) in `Input_glossaries.tex` durch die Projektsymbole und -abkürzungen ersetzen; Stile ggf. auf deutsche Beschriftungen prüfen (Index-Beschreibungen sind englisch).
   - Anhang: `appendix_content.tex` und `appendix.tex` sind Hinweistexte der Vorlage und gehören **nicht** in die fertige Arbeit. Sie sollten entfernt und die `\include`-Zeilen (Z. 246–247) ersetzt werden.
   - Bei Kompatibilitätsproblemen den Test (A4) abwarten und ggf. `\usepackage[T1]{fontenc}` aktivieren.
4. **Kompilierung:** Lokal am Rechner des Nutzers (TeX Live/MiKTeX) oder nach Installation im Container. Der Ablauf laut `compile.sh` ist `pdflatex -draftmode`, `makeindex` ×3, `biber`, `pdflatex -draftmode`, `pdflatex`. In der Cloud ist das erst nach Installation prüfbar.
5. **`.gitignore` für `in_progress/thesis/`** (aus `cleanup.sh` plus README-Empfehlung):
```
# LaTeX-Build-Artefakte
*.acn
*.acr
*.alg
*.aux
*.bbl
*.bcf
*.blg
*.ist
*.log
*.out
*.run.xml
*.toc
*.lof
*.lot
*.fls
*.fdb_latexmk
*.synctex.gz
*.slg1
*.slg2
*.syg1
*.syg2
*.syi1
*.syi2
*.glg
*.glo
*.gls
# erzeugtes PDF der Vorlage (bei Bedarf Abgabe-PDF unter Output/ ablegen)
Preambel_main.pdf
```
   Hinweis: `cleanup.sh` löscht `*.xml`, das ist im Projekt zu breit gefasst; `*.run.xml` ist spezifischer. Entscheidung, ob das erzeugte PDF eingecheckt wird, liegt beim Nutzer (Abgabestände gehören nach `Output/`).
6. **Zeilenenden:** Die Vorlage ist CRLF. Für Git ist eine `.gitattributes`-Regel (`*.tex text eol=lf`) sinnvoll, wenn der Nutzer auf Windows arbeitet; bitte beim Nutzer erfragen.

---

## A4. Offene Fragen

1. **Aktuelle Vorlagenversion:** Ist die hochgeladene Vorlage die aktuelle? Die Platzhalterdatei ist leer. Gibt es eine neuere Version im GitLab des SLA (URL im README)? — *Auswirkung:* Struktur, KI-Erklärung und Titelseite könnten abweichen.
2. **Fehlende Dateien:** `PICTURES/` (Logo `rwth_sla`, `Beispiel.eps`) bitte nachreichen. — *Auswirkung:* ohne Logo keine Kompilierung der Titelseite.
3. **Welche Formalregeln gelten?** SLA-Vorlage oder die WiWi-Richtlinien? Insbesondere Zitierstil (numerisch vs. Harvard), Umfang (< 50 vs. 40 Seiten) und Zeilenabstand. — *Auswirkung:* biblatex-Stil, Seitenbudget, Layout. *Annahme bis zur Klärung:* SLA-Vorlage gilt.
4. **Sprache der Arbeit:** Deutsch ist die Projektvorgabe. Die Vorlage ist mehrsprachig; Titelseite und Abstract bleiben englisch. Soll die Titelseite deutsch werden? — *Auswirkung:* `document_info.sty`, `01_titlepage.tex`.
5. **KI-Erklärung:** Welche Form verlangt das Prüfungsamt genau (Link in `03_integrity.tex`, Datei war im Upload nicht beigelegt)? Reicht die Tabelle in der Vorlage? Was gilt als „Auswirkung auf den wissenschaftlichen Inhalt" bei Rohfassungen, Code und Abbildungsskripten? — *Auswirkung:* Umfang der Dokumentationspflicht, `kapitel-map.md`.
6. **Quellenzahl „mindestens Seitenzahl":** gilt das bei SLA? — *Auswirkung:* Rechercheumfang.
7. **Isonorm3098:** darf die Schrift ins Repo und in Abbildungen eingebettet werden (Lizenz FontShop/FontFont)? Soll stattdessen die Freeware-Alternative IsonormD verwendet werden? — *Auswirkung:* Plotstil, Reproduzierbarkeit.
8. **Abgabeformalien:** Anzahl gedruckter Exemplare, Bindung, PDF-Abgabe, Termin, Matrikel- und Aufgabenstellungsblatt, Druckversion einseitig oder zweiseitig. Dazu gibt es in den Unterlagen nur die allgemeine Angabe „laut Prüfungsordnung". — *Auswirkung:* `twoside`, `draft`-Einstellung, Zeitplan.
9. **Anhangstexte der Vorlage** (Tipps, Formale Fragen) sind Hinweise und nicht Teil der Arbeit; Bestätigung, dass sie entfernt werden dürfen.
10. **Abbildungs- und Tabellenverzeichnis:** in der Vorlage deaktiviert (Wunsch des Chefs). Soll es dabei bleiben (die Richtlinien sehen „ggf." eines vor)?
11. **Weitere Unterlagen:** Das Dokument `Input/HIER EIGENES DOKUMENT ERWARTUNGSMANAGEMENT EINFUEGEN.txt` ist ebenfalls ein leerer Platzhalter und enthält mögliche Betreuerhinweise.

---

## Rückmeldung an den Orchestrator

**Paket:** I3 · **Status:** ERLEDIGT (mit Rückfragen, nicht blockierend)

**Ergebnis:** Sichtungsbericht (oben); keine Repo-Dateien erzeugt oder geändert. Hilfsauszüge: `/tmp/claude-0/-home-user/e6b61297-17fb-5003-91f8-95c4534d012c/scratchpad/i3/` (`preambel.txt`, `richt.txt`, `pp/`).

**Verwendete Unterlagen:** alle Dateien unter `/home/user/BA_Jakob-Busch_P/Input/Templates/` (LaTeX-Vorlage komplett inkl. Log und PDF, Richtlinien-PDF komplett, MATLAB-/Gnuplot-Vorlagen, Schriften (Metadaten), PPTX/PPAM), `/home/user/BA_Jakob-Busch_P/KONVENTIONEN.md`.

**Belegverweise (zentral):**
- Richtlinien sind WiWi/TIME, nicht SLA → Richtlinien-PDF S. 1, 3, 20, 40.
- SLA-Formalregeln (Präsens, 3. Person, < 50 Seiten, Zahlen, Farben, A5) → `VL/APPENDIX/appendix_content.tex` und `appendix.tex`.
- Numerisch/biber/pdflatex → `VL/SETTINGS/biblatex_set.sty:1–4`, `VL/README.md`, `VL/compile.sh`.
- KI-Erklärung → `VL/CHAPTERS_REST/03_integrity.tex`, `Preambel_main.tex:173–179`.
- Plotregeln → `VL/DATA/MATLAB_Plot_Vorlage_SLA_2015_11_11.m:24–59`, `T/gnuplot_Vorlagen/Gnuplot_Demo.gp:17, 36–37, 47, 63, 75–94`.
- Log-Abbruch → `VL/Preambel_main.log` Z. 1818, 2123, 2140.

**Lücken:** `PICTURES/` (Logo, Beispiel.eps) fehlt; aktuelle Vorlagenversion unbestätigt; Kompilierbarkeit mit aktuellem TeX nicht prüfbar (kein LaTeX im Container); Log der Vorlage endet mit „TeX capacity exceeded".

**LaTeX-Prüfung:** nicht kompiliert (kein LaTeX installiert). Nur statisch gelesen.

**Akzeptanzkriterien:** A1 ✅ (Belege mit Datei/Zeile bzw. Seite); A2 ✅ (Vorschlagsliste, Abschnitt A2); A3 ✅ (Aufbau und .gitignore beschrieben, nicht ausgeführt); A4 ✅ (11 offene Fragen).

**Annahmen:**
- Die SLA-Vorlage hat bei Widersprüchen Vorrang vor den WiWi-Richtlinien (Auswirkung: Zitierstil, Seitenbudget; Klärung durch Betreuer).
- Die 16 cm Textbreite folgen aus dem Kommentar im MATLAB-Skript und meiner KOMA-Rechnung (≈ 160 mm), nicht aus einer Kompilierung.
- Der Vorlagenstand vom Juli 2026 ist plausibel aktuell, aber nicht bestätigt.

**Rückfragen:**
- [blockierend für Thesis-Setup] Aktuelle Vorlage/Logo (`PICTURES/rwth_sla`) bereitstellen und Vorlagenversion bestätigen — *Auswirkung:* ohne Logo keine Titelseite, ohne Klärung evtl. veraltete Struktur.
- [blockierend für Zitierstil/Umfang] Gelten SLA-Vorlage oder WiWi-Richtlinien? — *Annahme bis zur Klärung:* SLA-Vorlage (numerisch, < 50 Seiten ohne Anhang).
- [nicht blockierend] Lizenz Isonorm3098 / Alternative IsonormD — *Annahme:* Schrift wird nicht ins Repo eingecheckt, Plotstil fällt auf eine Ersatzschrift zurück.
- [nicht blockierend] Abgabeformalien, KI-Erklärung genaue Form, Quellenzahl, Titelseite deutsch, Abbildungsverzeichnis — *Annahme:* Vorlagenvorgaben bleiben.

**Empfehlung für den nächsten Schritt:**
1. Nutzer um Logo/aktuelle Vorlage und um Klärung beim Betreuer (Formalregeln, Umfang, KI-Erklärung) bitten.
2. Danach Paket „LaTeX-Pflege/Aufsetzen von `in_progress/thesis/`" an den `wissenschaftlichen-autor` nach A3.
3. Nutzer fragen, ob die Vorschläge aus A2 dauerhaft in `KONVENTIONEN.md` (neuer Abschnitt „Thesis-Formalia") und in die Definitionen von `wissenschaftlicher-autor` und `thesis-gutachter` übernommen werden.
4. Paket für einen matplotlib-Plotstil (Abschnitt 3) an den `software-engineer` (nach Klärung der Schriftlizenz).
5. TeX Live im Container erst nach Freigabe installieren (Aufgabe liegt beim Orchestrator).