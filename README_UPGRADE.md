# MacroPad Windows Upgrade Pack
Generated: 2025-10-19T02:25:24

## What’s included
- `/boot.py` — enables CDC data serial
- `/code.py` — patched to listen for context tokens and auto-switch layers
- `/macros/win_System.py` — Windows-smart system layer
- `/tools/AutodeskMacroPadWatcher_v2.ahk` — AutoHotkey v2 watcher
- `/tools/AutodeskMacroPadWatcher_v1.ahk` — AutoHotkey v1 watcher

## Install (MacroPad)
1. Mount **CIRCUITPY**.
2. Copy `/boot.py`, `/code.py`, and `/macros/win_System.py` to the device.
3. (Optional) Put `/logo/Autodesk_Logo_128X64.bmp` if you want the splash.
4. **Power-cycle** the MacroPad so `/boot.py` takes effect.

## Windows (AutoHotkey)
1. Find the COM port in **Device Manager → Ports (COM & LPT)** named *CIRCUITPY CDC data (COMx)*.
2. Edit the AHK script to set `COM_PORT := "COMx"`.
3. Run the script. It sends one of: `SYSTEM, FUSION, REVIT, ACAD, INVENTOR, MAYA` based on active app.
4. Ensure your `/macros/*` names or display names contain fragments like `fusion`, `revit`, `autocad`, etc.

## Test
- Focus Fusion → layer auto-switches to Fusion.
- Focus Revit → layer switches to Revit.
- Unknown app → switches to `win_system`.

## Tips
- Prefix favorite Windows layers with `00_` to put them at the top.
- If a layer doesn’t match, adjust `token_alias` in `code.py` or rename app names in `/macros/`.
