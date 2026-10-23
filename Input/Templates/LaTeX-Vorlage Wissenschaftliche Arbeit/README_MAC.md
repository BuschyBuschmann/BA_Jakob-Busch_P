# MAC Anleitung

Anleitung der LaTeX Vorlage für MAC Benutzer erstellt by Stefan Groß.

## Installation

Die meisten benötigten Programme können als ein einziges Paket von der MacTeX-Website heruntergeladen werden:

http://www.tug.org/mactex/mactex-download.html

Nach dem Download müssen Sie lediglich auf das Paket in Ihrem Download-Ordner klicken. Daraufhin öffnet sich ein Fenster für die Installation. Nach Abschluss sind die TeX Live Distribution, der Editor TeXShop, das Bibliographieverwaltungsprogramm BibDesk und einige weitere Programm installiert.

Download and Installieren zusätzlich Sie den empfohlenen Editor Texstudio
https://www.texstudio.org → download latest Version
Ziehen Sie das Programm aus dem heruntergeladenen .dmg File in ihren Programme Ordner.


## Einrichten TexStudio
0. Starten Sie TexStudio und öffnen Sie die Vorlage Preambel_main.tex

1. Einstellungen → Erzeugen → Standardcompiler: “PdfLaTex”, Standard Bibliographieprogramm: “Biber”

2. Einstellungen → Befehle → Eintrag Makeindex: “makeindex”

3. Einstellungen → Erzeugen → Benutzerbefehle → hinzufügen: Run1: 	“txs:///pdflatex | txs:///makeindex -s %.ist -t %.alg -o %.acr %.acn| txs:///makeindex -s %.ist -t %.slg1 -o %.syi1 %.syg1| txs:///makeindex -s %.ist -t %.slg2 -o %.syi2 %.syg2 | txs:///pdflatex”

4. In der Datei Biblio.bib können Quellenangaben im BibTex Format hinzugefügt werden. Alternativ kann in der Präambel unter LOAD GLOSSARY/BIBLIOGRAPHY über Änderung des Dateinamens in “\bibliography{<Dateiname>}” eine eigene .bib Datei eingebunden werden. Diese kann aus gängigen Literaturverwaltungen z.B. aus Citavi exportiert werden https://www1.citavi.com/sub/manual6/de/index.html?101_creating_a_publication_with_latex.html) und wird im Projektordner, in der sich die Preambler.tex Datei usw. befindet, abgelegt.
Damit nur die Literatur, die im Text tatsächlich referenziert wurde (\cite{<bibTexKey>}), im Literaturverzeichnis aufgeführt wird, kommentieren Sie zudem bitte in der Preambel im Abschnitt BIBLIOGRAPHY die Zeile “%\nocite{*}” aus.

## Benutzung der Vorlage
Nun können Sie den Inhalt der einzelnen TeX-Dateien Einleitung.tex, Theorie.tex, usw. durch Ihre Inhalte ersetzen. Wird eine neue Datei erstellt, kann ihr Inhalt durch den Befehl \include{Dateiname} unter Content in Preambel_main.tex hinzugefügt werden.

## PDF Erzeugen
Tools → Benutzer → Run1

## Hilfreiches
Der Backslash \ liegt auf der Tastenkombination option+shift+7.
Umlaute werden im Editor durch den entsprechenden Vokal und ein Anführungszeichen ersetzt (“a = ä, “U = Ü, “s = ß).

Deutsche Anführungszeichen lassen sich mit den Befehlen \glqq („) und \grqq (“) erstellen. Formeln, die im Fließtext stehen sollen, werden zwischen zwei $ geschrieben.

Latex-Code für Sonderzeichen und griechische Buchstaben:
https://de.wikibooks.org/wiki/LaTeX-Kompendium:_Sonderzeichen

Latex-Code für mathematische Symbole:
https://de.wikipedia.org/wiki/Liste_mathematischer_Symbole

schnelle Handschrifterkennung für Symbole:
http://detexify.kirelabs.org/classify.html