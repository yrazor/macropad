#based on example file 
#https://github.com/adafruit/Adafruit_CircuitPython_MacroPad/blob/main/examples/macropad_keyboard_layout.py
#
#Bongo cat code
#https://github.com/christanaka/circuitpython-bongo

from adafruit_macropad import MacroPad
from adafruit_hid.consumer_control_code import ConsumerControlCode
from rainbowio import colorwheel
from bongo.bongo import Bongo
import time
import os

macropad = MacroPad()
bongo = Bongo()
macropad.display.show(bongo.group)
tone = 250
last_position = 0
timex = 0

def sleep():
	macropad.display_sleep = True
	macropad.pixels.brightness = 0.0

def resume():
    macropad.display_sleep = False
    macropad.pixels.brightness = 0.5
    timex = 0

resume()


keycodes = [
    macropad.Keycode.F13,
    macropad.Keycode.F14,
    macropad.Keycode.F15,
    macropad.Keycode.F16,
    macropad.Keycode.F17,
    macropad.Keycode.F18,
    macropad.Keycode.F19,
    macropad.Keycode.F20,
    macropad.Keycode.F21,
    macropad.Keycode.F22,
    macropad.Keycode.F23,
    macropad.Keycode.F24,
]

#text_lines = macropad.display_text(title="Binds", title_scale=2)


while True:
    
    key_event = macropad.keys.events.get()
    bongo.update(key_event)

    if key_event:
        if key_event.pressed:
            resume()
            macropad.pixels[key_event.key_number] = colorwheel(200)
            macropad.start_tone(tone)
        else: 
            macropad.pixels.fill((0, 0, 0))
            macropad.stop_tone()

    if key_event:
        keycode = keycodes[key_event.key_number]
        if key_event.pressed:
            if isinstance(keycode, int):
                macropad.keyboard.press(keycode)
            else:
                macropad.keyboard_layout.write(keycode)
        else:
            if isinstance(keycode, int):
                macropad.keyboard.release(keycode)
    #text_lines.show()

    macropad.encoder_switch_debounced.update()

    if macropad.encoder_switch_debounced.pressed: #MUTE
        macropad.consumer_control.send(
        macropad.ConsumerControlCode.MUTE
                )

    current_position = macropad.encoder

    if macropad.encoder > last_position: #VOLUME UP
        macropad.consumer_control.send(
        macropad.ConsumerControlCode.VOLUME_INCREMENT
                )

    if macropad.encoder < last_position: #VOLUME DOWN
        macropad.consumer_control.send(
        macropad.ConsumerControlCode.VOLUME_DECREMENT
                )

    last_position = current_position
    
    time.sleep(0.05)