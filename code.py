#based on example file 
#https://github.com/adafruit/Adafruit_CircuitPython_MacroPad/blob/main/examples/macropad_keyboard_layout.py

from adafruit_macropad import MacroPad
from adafruit_hid.consumer_control_code import ConsumerControlCode
from rainbowio import colorwheel
from Layer import Layer
import time
import os
import math

Layer.disableLayer()

macropad = MacroPad()
last_position = 0

one = 0
two = 0
operand = ""
ans = 0

x = 0

def calculator(first,op,second): #calculator (first int, operand, second int)
    if op == "+":
        ans = first+second
    elif op == "-":
        ans = first-second
    elif op == "*":
        ans = first*second
    elif op == "/":
        ans = first/second

keycodes = [
        7, #key 1
        8, #key 2
        9, #etc...
        4,
        5,
        6,
        1,
        2,
        3,
        "layer",
        0,
        "enter",
]
        
while True: #loops
    
    key_event = macropad.keys.events.get() #gets events with each loop
    if key_event:
            key = keycodes[key_event.key_number] #stores key pressed as value from array
            if key_event.pressed:
                if isinstance(key, int): #if key is integer in array
                    if x==0: #if its the first cycle
                        one = key #store into one
                        print(key) #print
                    elif x==3: #if its 3rd cycle
                        two = key #store into two
                        print(key) #print
                elif isinstance(key, str): #if string in the array
                    if key == "layer": #if layer key
                        Layer.activateLayer() #activate layer
                        Layer.chooseOperand()
                        operand = Layer.operand
                    if key == "enter": #if enter
                        try:
                            calculator(one, operand, two) #try to calculate
                            break
                        except ValueError:
                            print("invalid operation")

            else: #if no key event then release the last key
                if isinstance(key, int):
                    macropad.keyboard.release(key)
    
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
