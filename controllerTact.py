import os
from gpiozero import MCP3008, Button, LED
from time import sleep
import RPi.GPIO as gpio
import time
import client

directions = []
buttons = []

#Y = MCP3008(1)
#X = MCP3008(2)
Pot = MCP3008(0)

previouspotvalue = 0

input_state1 = False
input_state2 = False
input_state3 = False
input_state4 = False

previousinputstate1 = False
previousinputstate2 = False
previousinputstate3 = False
previousinputstate4 = False

gpio.setup(21, gpio.IN, pull_up_down=gpio.PUD_UP)
gpio.setup(20, gpio.IN, pull_up_down=gpio.PUD_UP)
gpio.setup(16, gpio.IN, pull_up_down=gpio.PUD_UP)
gpio.setup(12, gpio.IN, pull_up_down=gpio.PUD_UP)


class joyStick:
    def __init__(self, channel, direction):
        self.direction = direction
        self.channel = MCP3008(channel)
        directions.append(self)

    def readDirection(self):
        chan = self.channel
        intChan = int(chan.value * 100)
        if intChan == 100:
            retVal = 10
        elif intChan < 40:
            retVal = -1
        elif intChan > 60:
            retVal = 1
        else :
            retVal = 0

        return retVal


class pushButton:
    def __init__(self, pin, collor):
        self.collor = collor
        self.pin = Button(pin)
        buttons.append(self)

    def pressButton(self):
        button = self.pin
        buttonState = button.is_pressed
        return buttonState

#yDir = joyStick(0, 'Y')
#xDir = joyStick(1, 'X')
#gButton = pushButton(2, 'green')


def sendAllInput(directions, buttons):
    sendDict = {}
    for direction in directions:
        print(direction.direction)
        sendDict[direction.direction] = direction.readDirection()
    
    for button in buttons:
        print(button.collor)
        sendDict[button.collor] = button.pressButton()

    return sendDict

RedLed = LED(13)
YellowLed = LED(19)
GreenLed = LED(26)

while True:
##    print("jemoeder")
    detectedvalue = round(Pot.value, 2)
    if detectedvalue != previouspotvalue:
        client.send("tacPot1" + str(detectedvalue))
        previouspotvalue = detectedvalue
    
    # if previousinputstate1 != input_state1:
    #     client.send("jemoeder")
    #     previousinputstate1 = input_state1
    # elif previousinputstate2 != input_state2:
    #     client.send("tacinput2")
    #     previousinputstate2 = input_state2
    # elif previousinputstate3 != input_state3:
    #     client.send("tacinput3")
    #     previousinputstate3 = input_state3
    # elif previousinputstate4 != input_state4:
    #     client.send("tacinput4")
    #     previousinputstate4 = input_state4
    
    if not input_state1:
        client.send("tacinput1")
    if not input_state2:
        client.send("tacinput2")
    if not input_state3:
        client.send("tacinput3")
    if not input_state4:
        client.send("tacinput4")

    # if Pot.value > 0.67:
    #     RedLed.off()
    #     YellowLed.off()
    #     GreenLed.on()
    # elif Pot.value > 0.34:
    #     RedLed.off()
    #     YellowLed.on()
    #     GreenLed.off()
    # elif Pot.value < 0.339:
    #     RedLed.on()
    #     YellowLed.off()
    #     GreenLed.off()
    
    input_state1 = gpio.input(21)
    input_state2 = gpio.input(20)
    input_state3 = gpio.input(16)
    input_state4 = gpio.input(12)

    # if input_state1 == False:
    #     print('Button1 Pressed')
    #     time.sleep(0.2)
    # elif input_state2 == False:
    #     print('Button2 Pressed')
    #     time.sleep(0.2)
    # elif input_state3 == False:
    #     print('Button3 Pressed')
    #     time.sleep(0.2)
    # elif input_state4 == False:
    #     print('Button4 Pressed')
    #     time.sleep(0.2)
    # print('Y value ', Y.value)
    # print('X value ', X.value)
    # print('Pot value ', Pot.value)


    sleep(0.1)

##while True:
##    input_state1 = gpio.input(21)
##    input_state2 = gpio.input(20)
##    input_state3 = gpio.input(16)
##    input_state4 = gpio.input(12)
##    if input_state1 == False:
##        print('Button1 Pressed')
##        time.sleep(0.2)
##    elif input_state2 == False:
##        print('Button2 Pressed')
##        time.sleep(0.2)
##    elif input_state3 == False:
##        print('Button3 Pressed')
##        time.sleep(0.2)
##    elif input_state4 == False:
##        print('Button4 Pressed')
##        time.sleep(0.2)
