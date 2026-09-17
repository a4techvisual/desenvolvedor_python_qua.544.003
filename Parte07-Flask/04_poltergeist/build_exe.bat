@echo off
title Git Poltergeist v2.0 - WebView
cd /d "%~dp0"
python -m pip install --upgrade pywebview pyinstaller
if errorlevel 1 goto erro
pyinstaller --noconfirm --clean --onefile --windowed --add-data "index;index" --add-data "image;image" --add-data "font;font" --icon="image\image.ico" --name "Git Poltergeist v2.0" main.py
if errorlevel 1 goto erro
echo.
echo EXE criado em:
echo %cd%\dist\Git Poltergeist v2.0.exe
pause
exit /b 0
:erro
echo Erro ao gerar o EXE.
pause
exit /b 1
