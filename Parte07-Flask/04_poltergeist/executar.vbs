Option Explicit

' Inicializador SEM CMD.
' Use este arquivo apenas se o EXE ainda não tiver sido colocado como atalho.
Dim shell, fso, base, exePath
Set shell = CreateObject("WScript.Shell")
Set fso = CreateObject("Scripting.FileSystemObject")
base = fso.GetParentFolderName(WScript.ScriptFullName)

exePath = base & "\dist\Git Poltergeist v2.0.exe"

If fso.FileExists(exePath) Then
    shell.Run Chr(34) & exePath & Chr(34), 0, False
    WScript.Quit 0
End If

MsgBox "O Git Poltergeist ainda não foi compilado." & vbCrLf & vbCrLf & _
       "Execute CRIAR_EXE.vbs para gerar o EXE." & vbCrLf & _
       "Depois, abra o EXE diretamente ou use este arquivo .vbs.", _
       vbInformation, "Git Poltergeist v2.0"
