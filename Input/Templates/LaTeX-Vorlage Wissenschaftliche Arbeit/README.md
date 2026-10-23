# Thesis

In this directory are all the tex-files, pictures etc. The `Preambel_main.tex` is the main TeX file you need to compile when you want to get the entire thesis.

<!-- markdown-toc start - Don't edit this section. Run M-x markdown-toc-refresh-toc -->
**Table of Contents**

- [Thesis](#thesis)
    - [Folder-Structure:](#folder-structure)
    - [Files:](#files)
    - [Information on writing](#information-on-writing)
    - [Getting latex to generate an pdf-file](#getting-latex-to-generate-an-pdf-file)
        - [Windows](#windows)
        - [Linux](#linux)
        - [MAC](#mac)
    - [Versioning](#versioning)
        - [Helpful websites:](#helpful-websites)
        - [Other software:](#other-software)
    - [FAQ](#faq)
        - [Old-README](#old-readme)

<!-- markdown-toc end -->

## Download template
To create your thesis you need to download the template to your computer:

If you have [git](http://git-scm.com/) installed on your computer, this can be done with the command `git clone https://git-ce.rwth-aachen.de/sla-software/lehre/vorlage_wissenschaftliche_arbeit`.

Otherwise, use the download button and extract the compressed file somewhere in your computer.

<img src="https://git-ce.rwth-aachen.de/sla-software/lehre/vorlage_wissenschaftliche_arbeit/uploads/b8933da45a4165783a134e9731b338fc/git_download.png"  width="500">


## Folder-Structure:
- **THESIS/**
    - _**Preambel_main.tex**_: Main file, contains settings and defines document. Compile this file.
    - _**SETTINGS/document_info.sty**_: contains meta data, like title of the thesis or your name.
    - _**BIB_AND_GLOSSARY/Input_glossaries.tex**_: contains your glossary.
    - _**BIB_AND_GLOSSARY/Biblio.bib**_: contains your bibliography, add your literature here manually or with programs like [JabRef](https://www.jabref.org/).
    - **CHAPTERS_CONTENT/**: contains the tex-files with the main chapters.
    - **CHAPTERS_REST/**: contains all additional tex-files like title-page or abstract.
    - **DATA/**: contains data-files like csv or code.
    - **PICTURES/**: contains all the pictures and drawings in the document.
    - **APPENDIX/**: contains tex documents in the appendix.
    - **SETTINGS/**: contains style-sheets (\*.sty). You should not need to change stuff here.

## Files:
- \*.tex - files:
    Tex-files contain text, formulas and code.
- \*.sty - files:
    Style-sheets contain settings of the document. You should only need to change [document_info.sty](document_info.sty).
- \*.log -files:
    If you have errors look up those files. Sometimes they contain information on how to solve the problem.
- the rest:
    If it is not pictures or data of you, it is mostly rubbish, needed by your tex-distribution to compile, and can / should be thrown away after you compiled. It can sometimes happen, that those files are corrupt and prevent the tex-distribution to compile your document successfully.

## Information on writing
**See the files in /APPENDIX. Those have additional information on how to write your thesis.**

## Language
The language of the document has to be set in `Premabel_main.tex` two times: one time for the titlepage (line 66) and another one for the listings and rest of the document (line 198).

## Getting latex to generate an pdf-file
Latex does not work like Microsoft Word. You need two components to get your file. The first is a text-editor, you can actually use word for it however I would not recommend it to you at all. The second one is the tex-distribution. This peace of software contains all the code to compile your script into a PDF-file.

### Windows
**Please read the instructions prior starting to install**

1. First Install your tex-distribution. Get one of these:
    - [TexLive](https://www.tug.org/texlive/acquire-netinstall.html) and follow the [quick installation instructions](https://www.tug.org/texlive/quickinstall.html)
    - [MiKTeX](https://miktex.org/download) and follow the [instructions](https://docs.miktex.org/manual/)

2. Next thing you need is a text-editor.
In general: you can use any text-editor to write your latex files in it. You can even use editor.exe or Microsoft Word. However I strongly recommend you to use one of these:
    - [**TeXstudio**](https://www.texstudio.org/) (used by most research Assistants at SLA),
    - [Overleaf](https://de.overleaf.com/),
    - [Texmaker](https://www.xm1math.net/texmaker/),
    - [Visual Studio Code](https://code.visualstudio.com/),
    - [Atom](https://atom.io/),
    - and many other like vim or emacs, but with language-support.

If you are new to latex I recommend you to use one of the first, since those are relatively easy to setup and have good integration of the tex-distribution.
#### TeXstudio
If you are using TeXstudio, you can use the setting profile provided with the template "StudentischeArbeit.txsprofile". In TeXstudio go to Options -> Load Profile and select the provided profile. Then you can use the command "SLA stud. Arbeit" under Tools -> User to compile the document including the glossaries.

### Linux
For debian-based Linux distributions such as Debian itself and Ubuntu you can just install the packages `pdflatex`, `biber` and `texlive`. If you have enough disk space you can also install `texlive-full`, which directly supports all languages and packages.

> sudo apt install pdflatex biber texlive

To generate the full pdf with glossaries and literature the following commands have to be run.

```
file="Preambel_main"

pdflatex -draftmode $file.tex
makeindex -s $file.ist -t $file.alg  -o $file.acr  $file.acn
makeindex -s $file.ist -t $file.slg1 -o $file.syi1 $file.syg1
makeindex -s $file.ist -t $file.slg2 -o $file.syi2 $file.syg2 
biber $file
pdflatex -draftmode $file.tex
pdflatex $file.tex
```

This can be made settings executable rights to the file `compile.sh` (`chmod +x compile.sh`) and executing it (`./compile.sh`). If you use a dedicated LaTeX editor it should be possible to define this compilation instructions.

### MAC
The manual compilation described in Linux should work in MAC too (packages can be installed using `brew`). A more detailed explanation about the installation can be found on [README_MAC.md](README_MAC.md)

## Versioning
I recommend you to use git. This is perhaps the most common versioning-tool in software-development. [Here is how you get started. ](https://www.freecodecamp.org/news/learn-the-basics-of-git-in-under-10-minutes-da548267cc91/). The RWTH offers a [gitlab-server](https://git.rwth-aachen.de/), where you can log in with your RWTH-credentials and can upload, review and share your thesis. Exclude all the unneccessary files with an .gitignore file form [gitignore.io](https://gitignore.io). Just paste it in your repository and add following lines:

```
## Folders
02_INPUT/

## Added manualy:
*.ist
*.slg1
*.slg2
*.syg1
*.syg2
*.syi1
*.syi2
```

### Helpful websites:
- [NAMSU](https://www.namsu.de/)
- [CTAN, a list with all the packages for latex](https://ctan.org)
- [KOMA-Script, the main style-package](https://komascript.de) (I had to change the package from scrpage2 to scrlayer-scrpage, hopefully everything works now.)
- [TeX Welt](https://texwelt.de)
- And of course: [Google](https://www.google.de)
- To setup Atom with latex [this is a very helpful repository.](https://gist.github.com/Aerijo/5b9522530715e5be6e89fc012e9a72a8)

### Other software:
For sorting your literature you can use [JabRef](https://www.jabref.org/)

## FAQ

### Old-README

The old template did not use style-sheets etc. and subsequently was hardly readable, so I started rebuilding it more or less from scratch. However, this is the info which was formerly in the Preambel_main-template. There are still some useful info in it.

> !TeX document-id = {b43af1e0-c3a7-49c6-bdd0-d7d4a96f2660}
> Vorlage fuer Studentische Arbeiten - Institut fuer Leichtbau - RWTH
> Erstellt von: Johanna Schlupkothen (schlupkothen@ilb.rwth-aachen.de)
> 			und: Ulrike Schlauch (schlauch@ilb.rwth-aachen.de)
> Basierend auf der KOMA Script Klasse scrbook
> Erste Version: v01-1 Stand Oktober 2013
>_______________________________________________________________________________________
> Updates:		Author 			Date			Changes
>---------------------------------------------------------------------------------------
> v01-2			SCHLUPKOTHEN	24.09.2014		- Header changed to Prof. Schroeder
> v01-3 		SCHLUPKOTHEN 	27.08.2015 		- Offizielles Institutslogo
> v01-4 		NUNO		21.08.2018		- Zusammengefuehrt mit paralleler Version, Kommentare hinzugefuegt
>
>
>---------------------------------------------------------------------------------------
>
>---------------------------------------------------------------------------------------
>------                               --------------------------------------------------
>		!!!!!   R E A D   M E   !!!!!
>------                               --------------------------------------------------
>---------------------------------------------------------------------------------------
>
> !!!!! BEVOR IHR FRAGT, WEIL IRGENDETWAS " NICHT FUNKTIONIERT ": SCHAUT IN DIE
> KOMMENTIERUNG DES ZUGEHOERIGEN PACKAGES IN DIESER PRAEAMBEL!!!!!!
>
> Hinweise zur Kompilierung:
> Empfohlener Editor:			TeXstudio
>
>  	Standardcompiler: 			PdfLaTeX
>  	Standardbibliographie: 		Biber
> 	Verarbeitung mit Glossar:	pdflatex %
>								makeindex -s %.ist -t %.alg  -o %.acr  %.acn
>								makeindex -s %.ist -t %.slg1 -o %.syi1 %.syg1
>								makeindex -s %.ist -t %.slg2 -o %.syi2 %.syg2
>								pdflatex %
> 	Definition eines eigenen Befehls fuer das Kompilieren des Glossars in TeXstudio bzw. TeXmakerX:
>	___________________________________________________________________________________________
>	->Optionen-> TeXstudio konfigurieren...->Erzeugen->Benutzerbefehle(siehe Feld unten):
>								Hinzufügen eines neuen Benutzerbefehls, bspw. user0:
>								Eintrag im 2. Feld:
>								txs:///pdflatex | txs:///makeindex -s %.ist -t %.alg -o %.acr %.acn| txs:///makeindex -s %.ist -t %.slg1 -o %.syi1 %.syg1| txs:///makeindex -s %.ist -t %.slg2 -o %.syi2 %.syg2 | txs:///pdflatex
>
> 	Dieses Befehl kann von ->Tools -> Benutzer -> user0 gestartet werden
>___________________________________________________________________________________________
>	->Options-> TeXstudio konfigurieren...->Befehle-> Makeindindex:
> 								Ensure that is written only: makenindex.exe
>								WITHOUT any argument like "%.idx" behind it
>
>
>---------------------------------------------------------------------------------------
>--> Ablauf bei vollständiger Verarbeitung:
> 								pdflatex | pdflatex |biber | pdflatex | user0
>
>
>_______________________________________________________________________________________
>Steuerbefehle fuer TexShop fuer Mac (Gibt TS an, mit welchen Programmen gearbeitet werden soll)
>
> !TEX TS-program = pdflatex
> !BIB TS-program = biber
>---------------------------------------------------------------------------------------
