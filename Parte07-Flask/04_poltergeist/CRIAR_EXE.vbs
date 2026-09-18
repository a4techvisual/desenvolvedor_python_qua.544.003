Option Explicit

Dim shell, fso, base, pythonExe, args, result
Set shell = CreateObject("WScript.Shell")
Set fso = CreateObject("Scripting.FileSystemObject")
base = fso.GetParentFolderName(WScript.ScriptFullName)

pythonExe = shell.ExpandEnvironmentStrings("%LocalAppData%") & "\Programs\Python\Python313\python.exe"
If Not fso.FileExists(pythonExe) Then pythonExe = shell.ExpandEnvironmentStrings("%LocalAppData%") & "\Programs\Python\Python312\python.exe"
If Not fso.FileExists(pythonExe) Then pythonExe = shell.ExpandEnvironmentStrings("%LocalAppData%") & "\Programs\Python\Python311\python.exe"
If Not fso.FileExists(pythonExe) Then pythonExe = "python.exe"

' Compila sem cmd.exe: o WScript executa o Python diretamente e mantém o processo oculto.
args = " -m pip install --upgrade pyinstaller"
result = shell.Run(Chr(34) & pythonExe & Chr(34) & args, 0, True)
If result <> 0 Then
    MsgBox "Não foi possível instalar/atualizar o PyInstaller." & vbCrLf & vbCrLf & _
           "Verifique se o Python está instalado.", vbCritical, "Git Poltergeist v2.0"
    WScript.Quit 1
End If

args = " -m PyInstaller --noconfirm --clean --onefile --windowed --noconsole --icon=" & _
       Chr(34) & base & "\image\image.ico" & Chr(34) & _
       " --name " & Chr(34) & "Git Poltergeist v2.0" & Chr(34) & _
       " --distpath " & Chr(34) & base & "\dist" & Chr(34) & _
       " --workpath " & Chr(34) & base & "\build" & Chr(34) & _
       " " & Chr(34) & base & "\main.pyw" & Chr(34)

result = shell.Run(Chr(34) & pythonExe & Chr(34) & args, 0, True)

If result = 0 Then
    MsgBox "EXE criado com sucesso!" & vbCrLf & vbCrLf & _
           "Abra diretamente:" & vbCrLf & _
           base & "\dist\Git Poltergeist v2.0.exe", _
           vbInformation, "Git Poltergeist v2.0"
Else
    MsgBox "Não foi possível criar o EXE." & vbCrLf & vbCrLf & _
           "Código de erro: " & result, vbCritical, "Git Poltergeist v2.0"
End If
