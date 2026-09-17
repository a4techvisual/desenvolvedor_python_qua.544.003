@echo off
cd /d "%~dp0"
python -m pip install --upgrade pyinstaller
if errorlevel 1 goto erro
pyinstaller --noconfirm --clean --onefile --windowed --noconsole --icon="image\image.ico" --name "Git Poltergeist v2.0" main.pyw
if errorlevel 1 goto erro

echo.
echo ==========================================
echo EXE criado:
echo %cd%\dist\Git Poltergeist v2.0.exe
echo ==========================================
echo.
pause
exit /b 0

:erro
echo.
echo Nao foi possivel gerar o EXE.
pause
exit /b 1
