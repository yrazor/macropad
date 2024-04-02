from adafruit_macropad import MacroPad
from adafruit_hid.consumer_control_code import ConsumerControlCode
import time
import os
import math

macropad = MacroPad()

class Layer:
    layerActive = false
    operand = ""

    def activateLayer():
        layerActive = true
    def disableLayer():
        layerActive = false

    def chooseOperand():
        while layerActive = true:
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
                    layerActive = false
                
            else:
                macropad.keyboard.release()

