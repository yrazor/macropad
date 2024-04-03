#based on example file 
#https://github.com/adafruit/Adafruit_CircuitPython_MacroPad/blob/main/examples/macropad_keyboard_layout.py

from adafruit_macropad import MacroPad
from adafruit_hid.consumer_control_code import ConsumerControlCode
from rainbowio import colorwheel
import time
import os
import math

macropad = MacroPad()
last_position = 0

one = ""
two = ""
operand = ""
ans = 0

key = ""
loops = 0
x = 0

layerActive = False


def clearVars():
    global loops
    global one
    global two
    global operand
    global ans
    x=0
    one=""
    two=""
    operand=""
    ans=0
    loops=+1
    layerActive=False

def calculator(first,op,second): #calculator (first int, operand, second int)
    global loops
    global one
    global two
    global operand
    global ans
    #print("debug-----"+first)
    #print("debug-----"+op)
    #print("debug-----"+second)
    if op == "+":
        ans = int(first)+int(second)
    elif op == "-":
        ans = int(first)-int(second)
    elif op == "*":
        ans = int(first)*int(second)
    elif op == "/":
        ans = int(first)/int(second)
    print("="+str(ans))
    #print("debug-----x="+str(x))


keycodes = [
        7, #key 1
        8, #key 2
        9, #etc...:w
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
                    #print(x)
                    if loops == 1:
                        x-=1
                        loops = 0
                    if x==0: #if its the first cycle
                        one = one + str(key) #add the key one
                        print(key, end='') #print
                    elif x==1: #if its 2nd cycle
                        two = two + str(key) #store into two
                        print(key, end='') #print
                elif isinstance(key, str): #if string in the array
                    if key == "layer": #if layer key
                        layerActive = True  #activate layer
                        while layerActive == True:
                            key_event = macropad.keys.events.get()
                            if key_event:
                                key = key_event.key_number
                                if key_event.pressed:
                                    if key == 2:
                                        operand = "/"
                                        x+=1
                                    if key == 5:
                                        operand = "*"
                                        x+=1
                                    if key == 8:
                                        operand = "-"
                                        x+=1
                                    if key == 11:
                                        operand = "+"
                                        x+=1
                                    else:
                                        pass
                                    print(operand,end='')

                                    layerActive = False
                                else:
                                    macropad.keyboard.release(key)
                                
                    if key == "enter": #if enter
                        try:
                            calculator(one, operand, two) #try to calculate
                            clearVars()
                        except ZeroDivisionError:
                            print("\nCannot divide by zero")
                            clearVars()
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
