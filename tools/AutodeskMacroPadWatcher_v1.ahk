; AutoHotkey v1 - Autodesk MacroPad watcher
COM_PORT := "COM5"   ; change to your CIRCUITPY CDC data port
CHECK_MS := 200

sp := "\\.\" . COM_PORT
h := FileOpen(sp, "w")
if (!h) {
    MsgBox, 16, Error, Failed to open %sp%`nCheck Device Manager and COM port.
    ExitApp
}
last := ""

SetTimer, Tick, %CHECK_MS%
return

Tick:
WinGet, exe, ProcessName, A
StringLower, exe, exe
token := "SYSTEM"
if (exe = "fusion360.exe")
    token := "FUSION"
else if (exe = "revit.exe")
    token := "REVIT"
else if (exe = "acad.exe")
    token := "ACAD"
else if (exe = "inventor.exe")
    token := "INVENTOR"
else if (exe = "maya.exe")
    token := "MAYA"

if (token != last) {
    h.WriteLine(token)
    h.Flush()
    last := token
}
return

OnExit:
if (h)
    h.Close()
ExitApp
