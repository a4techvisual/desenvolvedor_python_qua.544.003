@echo off
title Git Poltergeist v2.0 - Gerar EXE
cd /d "%~dp0"

python -m pip install --upgrade pyinstaller
if errorlevel 1 goto erro

if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
if exist "Git Poltergeist v2.0.spec" del /q "Git Poltergeist v2.0.spec"

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
