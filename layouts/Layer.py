from adafruit_macropad import MacroPad
from adafruit_hid.consumer_control_code import ConsumerControlCode
from rainbowio import colorwheel
import time
import os
import math

#macropad = MacroPad()

class Layer:
    layerActive = bool(False)
    operand = ""

    def activateLayer():
        layerActive = bool(True)
    def disableLayer():
        layerActive = bool(False)

    def chooseOperand():
        while layerActive == True:
            key_event = macropad.keys.events.get()
            if key_event:
                key = key_event.key_number
                if key_event.pressed:
                    if key == 3:
                        operand = "/"
                    if key == 6:
                        operand = "*"
                    if key == 9:
                        operand = "-"
                    if key == 12:
                        operand = "+"
                    layerActive = bool(False)
                
            else:
                macropad.keyboard.release()

