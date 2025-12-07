Set WshShell = CreateObject("WScript.Shell")
WshShell.Run chr(34) & "C:\repos\AI-Librarian\orchestrator\start_background.bat" & Chr(34), 0
Set WshShell = Nothing
