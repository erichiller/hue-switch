import time
import RPi.GPIO as GPIO

import requests


host = "92.168.10.46"
user = "XO3rCiWc269m6rk5wv1OZzudn9PCkAY-JcRMby8x"
default_light = 11

GPIO.setmode(GPIO.BCM)
 
padPin = 23
GPIO.setup(padPin, GPIO.IN)
 
alreadyPressed = False


def check_light_status(light_id=11):
    r = requests.get("http://" + host + "/api/" + user + "/lights/" + light_id).json()
    return r["on"]


def set_light_state(state, light_id=default_light):
    if state in ( True , "True" , "true" , "on" , "On" ):
        state = "true"
    elif state in ( False , "False" , "false", "off", "Off" ):
        state = "false"
    else:
        exit("invalid state")

    payload = '{ "on": "' + state + '" }'
    requests.put("http://" + host + "/api/" + user + "/lights/" + light_id + "/state",data=payload)


def toggle_light(light_id=default_light):
    status = check_light_status(light_id)
    print(status)
    type(status)

    if status:
        set_light_state(True, default_light)
    else:
        set_light_state(False, default_light)

if __name__ == "__main__":
    while True:
        padPressed =  GPIO.input(padPin)
 
        #if padPressed and not alreadyPressed:
        print "pressed"

        toggle_light()


    
        #alreadyPressed = padPressed
        #time.sleep(0.1)
        time.sleep(0.5)


