' SMA55 MT4 bridge launcher. No trading functionality.
Option Explicit
Dim sh, fso, script, python, cmd, oneDrive, localDocs
Set sh = CreateObject("WScript.Shell")
Set fso = CreateObject("Scripting.FileSystemObject")
oneDrive = sh.ExpandEnvironmentStrings("%USERPROFILE%") & "\OneDrive\Documents\SMA55 Bridge\mt4_to_github.py"
localDocs = sh.ExpandEnvironmentStrings("%USERPROFILE%") & "\Documents\SMA55 Bridge\mt4_to_github.py"
If fso.FileExists(oneDrive) Then
 script = oneDrive
ElseIf fso.FileExists(localDocs) Then
 script = localDocs
Else
 MsgBox "Cannot find mt4_to_github.py in Documents\SMA55 Bridge", vbExclamation, "SMA55 Bridge"
 WScript.Quit 1
End If
python = "pythonw.exe"
cmd = "pythonw.exe " & Chr(34) & script & Chr(34)
sh.Run cmd, 0, False
