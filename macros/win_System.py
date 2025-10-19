# /macros/win_System.py
from adafruit_hid.keycode import Keycode

app = {
    'name': 'win_system',
    'macros': [
        (0x224466,'DeskL',[Keycode.GUI, Keycode.CONTROL, Keycode.LEFT_ARROW]),
        (0x224466,'DeskR',[Keycode.GUI, Keycode.CONTROL, Keycode.RIGHT_ARROW]),
        (0x334455,'SnapL',[Keycode.GUI, Keycode.LEFT_ARROW]),
        (0x334455,'SnapR',[Keycode.GUI, Keycode.RIGHT_ARROW]),
        (0x445566,'TaskVw',[Keycode.GUI, Keycode.TAB]),
        (0x556677,'Start',[Keycode.GUI]),
        (0x334433,'Lock',[Keycode.GUI, 'l']),
        (0x223344,'SS Full',[Keycode.GUI, Keycode.PRINT_SCREEN]),
        (0x223355,'SS Area',[Keycode.GUI, Keycode.SHIFT, 's']),
        (0x442222,'Run',[Keycode.GUI, 'r']),
        (0x333333,'TermA',[Keycode.GUI, 'x','a']),
        (0x006600,'Enter',[Keycode.ENTER]),
        (0x000000,'Save',[Keycode.CONTROL, 's'])
    ]
}
