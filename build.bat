@echo off

set jbname=out

cd /d "%~dp0"
echo Working folder: %~dp0
echo Starting compilation in silent mode...
rem Precompilating tasks tex-file
rem TODO: сделать перенос основной части сборки проекта в python-скрипт
python src/generate_tasks.py
python src/generate_categories.py

rem Compilating in 3 times
pdflatex src/main.tex -aux-directory="__compile" -jobname=%jbname% -quiet
pdflatex src/main.tex -aux-directory="__compile" -jobname=%jbname% -quiet
rem pdflatex src/main.tex -aux-directory="__compile" -jobname=%jbname% -quiet
rem %jbname%.pdf
echo Done!