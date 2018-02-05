import os
from gpiozero import LED
import RPi.GPIO as gpio
import time
import client


healred = LED(2)
healyellow = LED(3)
healgreen = LED(4)

damagered = LED(18)
damageyellow = LED(23)
damagegreen = LED(24)

enginered = LED(22)
engineyellow = LED(16)
enginegreen = LED(20)

gpio.setmode(gpio.BCM)
gpio.setup(14, gpio.IN, pull_up_down=gpio.PUD_UP)
gpio.setup(17, gpio.IN, pull_up_down=gpio.PUD_UP)
gpio.setup(15, gpio.IN, pull_up_down=gpio.PUD_UP)
gpio.setup(27, gpio.IN, pull_up_down=gpio.PUD_UP)
gpio.setup(25, gpio.IN, pull_up_down=gpio.PUD_UP)
gpio.setup(21, gpio.IN, pull_up_down=gpio.PUD_UP)

healplusstate = False
healminstate = False
damageplusstate = False
damageminstate = False
engineplusstate = False
engineminstate = False

# Energy value definition
healing = 1
damage = 1
engine = 1

def setlights(type, red, yellow, green):
    if type == 0:
        green.off()
        yellow.off()
        red.off()
        return
    if type == 1:
        green.on()
        yellow.off()
        red.off()
    if type == 2:
        green.on()
        yellow.on()
        red.off()
    if type == 3:
        green.on()
        yellow.on()
        red.on()

while True:
    time.sleep(0.1)
    
    healplus = gpio.input(14)  # heal +
    healmin = gpio.input(17)  # heal -
    damageplus = gpio.input(15)  # damage +
    damagemin = gpio.input(27)  # damage -
    engineplus = gpio.input(25)  # engine +
    enginemin = gpio.input(21)  # engine -
    
    previoushealing = healing
    previousdamage = damage
    previousengine = engine
        
    if not healplus and not healplusstate:
        healplusstate = True
    elif healplus and healplusstate:
        healplusstate = False
        healing += 1
    if not healmin and not healminstate:
        healminstate = True
    elif healmin and healminstate:
        healminstate = False
        healing -= 1
    
    if not damageplus and not damageplusstate:
        damageplusstate = True
    elif damageplus and damageplusstate:
        damageplusstate = False
        damage += 1
    if not damagemin and not damageminstate:
        damageminstate = True
    elif damagemin and damageminstate:
        damageminstate = False
        damage -= 1
    
    if not engineplus and not engineplusstate:
        engineplusstate = True
    elif engineplus and engineplusstate:
        engineplusstate = False
        engine += 1
    if not enginemin and not engineminstate:
        engineminstate = True
    elif enginemin and engineminstate:
        engineminstate = False
        engine -= 1
    
    if healing > 3:
        healing = 3
    if healing < 0:
        healing = 0
    if damage > 3:
        damage = 3
    if damage < 0:
        damage = 0
    if engine > 3:
        engine = 3
    if engine < 0:
        engine = 0
    
##    print("healing" + str(healing))
##    print("damage" + str(damage))
##    print("engine" + str(engine))
    
    setlights(healing, healred, healyellow, healgreen)
    setlights(damage, damagered, damageyellow, damagegreen)
    setlights(engine, enginered, engineyellow, enginegreen)
    
    if previoushealing != healing:
        client.send("he" + str(healing))
    if previousdamage != damage:
        client.send("da" + str(damage))
    if previousengine != engine:
        client.send("en" + str(engine))










