; AutoHotkey v2 - Autodesk MacroPad watcher
COM_PORT := "COM5"   ; change to your CIRCUITPY CDC data port
CHECK_MS := 200

sp := "\\.\" COM_PORT
h := FileOpen(sp, "w")
if !h {
    MsgBox "Failed to open " sp ". Check Device Manager and COM port."
    ExitApp
}
last := ""

SendToken(token) {
    global h, last
    if (token != last) {
        try {
            h.WriteLine(token)
            h.Flush()
            last := token
        }
    }
}

SetTimer () => {
    winExe := WinGetProcessName("A")
    token := "SYSTEM"
    switch StrLower(winExe) {
        case "fusion360.exe": token := "FUSION"
        case "revit.exe":     token := "REVIT"
        case "acad.exe":      token := "ACAD"
        case "inventor.exe":  token := "INVENTOR"
        case "maya.exe":      token := "MAYA"
        default:              token := "SYSTEM"
    }
    SendToken(token)
}, CHECK_MS

OnExit( (*) => (h ? h.Close() : 0) )
