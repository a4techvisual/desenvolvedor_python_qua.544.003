@echo off
cd /d "%~dp0"

rem Executa o aplicativo sem abrir uma janela de CMD.
if exist "%~dp0dist\Git Poltergeist v2.0.exe" (
    start "" "%~dp0dist\Git Poltergeist v2.0.exe"
    exit /b 0
)

rem Se o EXE ainda não foi gerado, executa o Python com pythonw (sem console).
where pythonw.exe >nul 2>&1
if not errorlevel 1 (
    start "" pythonw.exe "%~dp0main.py"
    exit /b 0
)

rem Último recurso: gera uma mensagem e encerra.
msg * "Git Poltergeist: o EXE ainda não foi criado. Execute build_exe.bat uma vez."
exit /b 1
