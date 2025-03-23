@ECHO OFF

set jbname=out

cd /d "%~dp0"
echo Working folder: %~dp0
echo Starting compilation in silent mode...
pdflatex src/main.tex -aux-directory="__compile" -quiet -jobname=%jbname%
%jbname%.pdf
pause