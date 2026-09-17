@echo off
cd /d "%~dp0"
python -m pip install --upgrade pyinstaller
if errorlevel 1 goto erro
python -m PyInstaller --noconfirm --clean --onefile --windowed --noconsole --icon="image\image.ico" --name "Git Poltergeist v2.0" main.pyw
if errorlevel 1 goto erro

echo EXE criado em:
echo %cd%\dist\Git Poltergeist v2.0.exe
exit /b 0

:erro
echo Nao foi possivel gerar o EXE.
exit /b 1
