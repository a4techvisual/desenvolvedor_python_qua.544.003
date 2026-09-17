Option Explicit

Dim shell, fso, base, exePath, pywPath, pythonw
Set shell = CreateObject("WScript.Shell")
Set fso = CreateObject("Scripting.FileSystemObject")
base = fso.GetParentFolderName(WScript.ScriptFullName)

exePath = base & "\dist\Git Poltergeist v2.0.exe"
pywPath = base & "\main.pyw"

If fso.FileExists(exePath) Then
    shell.Run Chr(34) & exePath & Chr(34), 0, False
    WScript.Quit 0
End If

pythonw = shell.ExpandEnvironmentStrings("%LOCALAPPDATA%") & "\Programs\Python\Python313\pythonw.exe"
If Not fso.FileExists(pythonw) Then
    pythonw = shell.ExpandEnvironmentStrings("%LOCALAPPDATA%") & "\Programs\Python\Python312\pythonw.exe"
End If
If Not fso.FileExists(pythonw) Then
    pythonw = shell.ExpandEnvironmentStrings("%LOCALAPPDATA%") & "\Programs\Python\Python311\pythonw.exe"
End If
If Not fso.FileExists(pythonw) Then
    pythonw = "pythonw.exe"
End If

If fso.FileExists(pywPath) Then
    shell.Run Chr(34) & pythonw & Chr(34) & " " & Chr(34) & pywPath & Chr(34), 0, False
Else
    MsgBox "Não encontrei o programa para iniciar." & vbCrLf & vbCrLf & _
           "Gere o EXE pelo arquivo build_exe.bat ou instale o Python para executar o main.pyw.", _
           vbCritical, "Git Poltergeist v2.0"
End If
