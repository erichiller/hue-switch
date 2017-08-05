import time
from datetime import datetime
import RPi.GPIO as GPIO

import requests
import pygame

host = "192.168.10.46"
user = "XO3rCiWc269m6rk5wv1OZzudn9PCkAY-JcRMby8x"
default_light = 11

GPIO.setmode(GPIO.BCM)
 
padPin = 23
GPIO.setup(padPin, GPIO.IN)
 
alreadyPressed = True


def check_light_status(light_id=11):
    connection_string = "http://" + host + "/api/" + user + "/lights/" + str(light_id)
    r = requests.get(connection_string).json()
    return r["state"]["on"]


def set_light_state(state, light_id=default_light):
    if state in ( True , "True" , "true" , "on" , "On" ):
        state = "true"
    elif state in ( False , "False" , "false", "off", "Off" ):
        state = "false"
    else:
        exit("invalid state")

    payload = '{ "on": ' + state + ' }'
    requests.put("http://" + host + "/api/" + user + "/lights/" + str(light_id) + "/state",data=payload)


def toggle_light(light_id=default_light):
    status = check_light_status(light_id)

    if status:
        set_light_state(False, default_light)
        return False
    else:
        set_light_state(True, default_light)
        play_turned_on()
        return True

def play_turned_on():
    pygame.mixer.init()
    pygame.mixer.music.load("smithers.wav")
    pygame.mixer.music.play()
    while pygame.mixer.music.get_pos() < 6200:
        continue
    pygame.mixer.music.stop()

if __name__ == "__main__":
    print( datetime.now().strftime("%b %d %H:%M:%S") + ": Starting switch program, entering while loop...")
    while True:
        padPressed =  GPIO.input(padPin)
 
        if padPressed and not alreadyPressed:
            now = datetime.now().strftime("%b %d %H:%M:%S")
            print(now + ": pressed")
            
            if toggle_light() is False:
                print(now + ": Light Turned Off" )
            else:
                print(now + ": Light Turned On" )



    
        alreadyPressed = padPressed
        time.sleep(0.1)


