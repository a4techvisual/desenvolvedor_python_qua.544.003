@echo off
title Git Poltergeist v2.0 - Gerar EXE
cd /d "%~dp0"

python -m pip install --upgrade pyinstaller
if errorlevel 1 goto erro

pyinstaller --noconfirm --clean --onefile --windowed --icon="image\image.ico" --name "Git Poltergeist v2.0" main.py
if errorlevel 1 goto erro

echo.
echo ==========================================
echo EXE criado com sucesso:
echo %cd%\dist\Git Poltergeist v2.0.exe
echo ==========================================
pause
exit /b 0

:erro
echo.
echo Nao foi possivel gerar o EXE.
pause
exit /b 1
