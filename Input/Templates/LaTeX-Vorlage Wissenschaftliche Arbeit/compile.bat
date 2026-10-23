@echo off
set file=Preambel_main

echo Performing clean compile, invoking cleanup.bat
call cleanup.bat

echo Running LaTeX passes...
pdflatex -draftmode %file%.tex
makeindex -s %file%.ist -t %file%.alg  -o %file%.acr  %file%.acn
makeindex -s %file%.ist -t %file%.slg1 -o %file%.syi1 %file%.syg1
makeindex -s %file%.ist -t %file%.slg2 -o %file%.syi2 %file%.syg2
biber %file%
pdflatex -draftmode %file%.tex
pdflatex %file%.tex

echo Clearing files, invoking cleanup.bat
call cleanup.bat
