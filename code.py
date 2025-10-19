# SPDX-License-Identifier: MIT
# MacroPad AU build with Windows context auto-switching

import os, time
import displayio, terminalio
import usb_cdc
import adafruit_imageload
from adafruit_display_shapes.rect import Rect
from adafruit_display_text import label
from adafruit_macropad import MacroPad

MACRO_FOLDER = '/macros'
LOGO = '/logo'

class App:
    def __init__(self, appdata):
        self.name = appdata['name']
        self.macros = appdata['macros']
    def switch(self):
        header_label.text = self.name
        for i in range(12):
            if i < len(self.macros):
                macropad.pixels[i] = self.macros[i][0]
                key_labels[i].text = self.macros[i][1]
            else:
                macropad.pixels[i] = 0
                key_labels[i].text = ''
        macropad.keyboard.release_all()
        macropad.consumer_control.release()
        macropad.mouse.release_all()
        macropad.stop_tone()
        macropad.pixels.show()
        macropad.display.refresh()

def show_screen(group):
    macropad.display.show(group)
    macropad.display.refresh()
    time.sleep(2)

macropad = MacroPad()
macropad.display.auto_refresh = False
macropad.display.rotation = 180
macropad.pixels.auto_write = False

# Splash (optional)
try:
    title_group = displayio.Group()
    title_bitmap, title_palette = adafruit_imageload.load(
        LOGO + '/Autodesk_Logo_128X64.bmp',
        bitmap=displayio.Bitmap, palette=displayio.Palette
    )
    title_group.append(displayio.TileGrid(title_bitmap, pixel_shader=title_palette,
                                          width=1, height=1,
                                          tile_width=title_bitmap.width, tile_height=title_bitmap.height))
    show_screen(title_group)
except Exception:
    pass

ui = displayio.Group()
key_labels = []
for key_index in range(12):
    x = key_index % 3
    y = key_index // 3
    lbl = label.Label(terminalio.FONT, text='', color=0xFFFFFF,
                      anchored_position=((macropad.display.width - 1) * x / 2,
                                         macropad.display.height - 1 - (3 - y) * 12),
                      anchor_point=(x / 2, 1.0))
    key_labels.append(lbl)
    ui.append(lbl)
ui.append(Rect(0, 0, macropad.display.width, 12, fill=0xFFFFFF))
header_label = label.Label(terminalio.FONT, text='', color=0x000000,
                           anchored_position=(macropad.display.width//2, -2),
                           anchor_point=(0.5, 0.0))
ui.append(header_label)
macropad.display.show(ui)

apps = []
try:
    files = os.listdir(MACRO_FOLDER)
    files.sort()
except Exception:
    header_label.text = 'NO /macros FOLDER'
    macropad.display.refresh()
    while True: pass

for filename in files:
    if filename.endswith('.py') and not filename.startswith('._'):
        try:
            module = __import__(MACRO_FOLDER + '/' + filename[:-3])
            apps.append(App(module.app))
        except Exception as err:
            print('ERROR in', filename, err)

if not apps:
    header_label.text = 'NO MACRO FILES FOUND'
    macropad.display.refresh()
    while True: pass

name_to_index = {a.name.strip().lower(): i for i, a in enumerate(apps)}
token_alias = {
    'fusion': 'fusion',
    'revit': 'revit',
    'acad': 'autocad',
    'autocad': 'autocad',
    'inventor': 'inventor',
    'maya': 'maya',
    'system': 'win_system'
}
def resolve_token(tok):
    t = tok.strip().lower()
    if t in token_alias:
        frag = token_alias[t]
        for nm, idx in name_to_index.items():
            if frag in nm:
                return idx
    return name_to_index.get(t, None)

last_position = None
last_encoder_switch = macropad.encoder_switch_debounced.pressed
app_index = 0
apps[app_index].switch()

while True:
    if usb_cdc.data and usb_cdc.data.in_waiting:
        try:
            line = usb_cdc.data.readline().decode('utf-8', 'ignore').strip()
            idx = resolve_token(line)
            if idx is not None and idx != app_index:
                app_index = idx
                apps[app_index].switch()
                last_position = macropad.encoder
        except Exception:
            pass

    position = macropad.encoder
    if position != last_position:
        app_index = position % len(apps)
        apps[app_index].switch()
        last_position = position

    macropad.encoder_switch_debounced.update()
    encoder_switch = macropad.encoder_switch_debounced.pressed
    if encoder_switch != last_encoder_switch:
        last_encoder_switch = encoder_switch
        if len(apps[app_index].macros) < 13:
            continue
        key_number = 12
        pressed = encoder_switch
    else:
        event = macropad.keys.events.get()
        if not event or event.key_number >= len(apps[app_index].macros):
            continue
        key_number = event.key_number
        pressed = event.pressed

    sequence = apps[app_index].macros[key_number][2]
    if pressed:
        if key_number < 12:
            macropad.pixels[key_number] = 0xFFFFFF
            macropad.pixels.show()
        for item in sequence:
            if isinstance(item, int):
                if item >= 0: macropad.keyboard.press(item)
                else:         macropad.keyboard.release(-item)
            elif isinstance(item, float):
                time.sleep(item)
            elif isinstance(item, str):
                macropad.keyboard_layout.write(item)
            elif isinstance(item, list):
                for code in item:
                    if isinstance(code, int):
                        macropad.consumer_control.release()
                        macropad.consumer_control.press(code)
                    if isinstance(code, float):
                        time.sleep(code)
            elif isinstance(item, dict):
                if 'buttons' in item:
                    if item['buttons'] >= 0: macropad.mouse.press(item['buttons'])
                    else:                    macropad.mouse.release(-item['buttons'])
                macropad.mouse.move(item.get('x',0), item.get('y',0), item.get('wheel',0))
                if 'tone' in item:
                    if item['tone'] > 0:
                        macropad.stop_tone(); macropad.start_tone(item['tone'])
                    else:
                        macropad.stop_tone()
                elif 'play' in item:
                    macropad.play_file(item['play'])
    else:
        for item in sequence:
            if isinstance(item, int):
                if item >= 0: macropad.keyboard.release(item)
            elif isinstance(item, dict):
                if 'buttons' in item and item['buttons'] >= 0:
                    macropad.mouse.release(item['buttons'])
                elif 'tone' in item:
                    macropad.stop_tone()
        macropad.consumer_control.release()
        if key_number < 12:
            macropad.pixels[key_number] = apps[app_index].macros[key_number][0]
            macropad.pixels.show()
