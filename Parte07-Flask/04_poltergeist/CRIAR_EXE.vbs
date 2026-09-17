Option Explicit

Dim shell, fso, base, pythonExe, cmd, result
Set shell = CreateObject("WScript.Shell")
Set fso = CreateObject("Scripting.FileSystemObject")
base = fso.GetParentFolderName(WScript.ScriptFullName)

pythonExe = shell.ExpandEnvironmentStrings("%LocalAppData%") & "\Programs\Python\Python313\python.exe"
If Not fso.FileExists(pythonExe) Then pythonExe = shell.ExpandEnvironmentStrings("%LocalAppData%") & "\Programs\Python\Python312\python.exe"
If Not fso.FileExists(pythonExe) Then pythonExe = shell.ExpandEnvironmentStrings("%LocalAppData%") & "\Programs\Python\Python311\python.exe"
If Not fso.FileExists(pythonExe) Then pythonExe = "python.exe"

cmd = "cmd.exe /c cd /d " & Chr(34) & base & Chr(34) & " && " & Chr(34) & pythonExe & Chr(34) & _
      " -m pip install --upgrade pyinstaller && " & Chr(34) & pythonExe & Chr(34) & _
      " -m PyInstaller --noconfirm --clean --onefile --windowed --noconsole --icon=" & _
      Chr(34) & "image\image.ico" & Chr(34) & " --name " & Chr(34) & "Git Poltergeist v2.0" & Chr(34) & " main.pyw"

' O cmd.exe existe apenas como processo oculto para o processo de compilação.
' Nenhuma janela de console é exibida ao usuário.
result = shell.Run(cmd, 0, True)

If result = 0 Then
    MsgBox "EXE criado com sucesso!" & vbCrLf & vbCrLf & _
           "Agora abra:" & vbCrLf & _
           base & "\dist\Git Poltergeist v2.0.exe", _
           vbInformation, "Git Poltergeist v2.0"
Else
    MsgBox "Não foi possível criar o EXE." & vbCrLf & vbCrLf & _
           "Verifique se o Python está instalado e tente novamente.", _
           vbCritical, "Git Poltergeist v2.0"
End If
