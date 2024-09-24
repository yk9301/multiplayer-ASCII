from dataclasses import dataclass
import os
import time, threading
from pynput import keyboard
from ObjectManager import *
from Cursor import Cursor

#import paho.mqtt.client as mqtt
from subscriber import *
from publisher import *
import paho.mqtt.client as mqtt


def gameLoop():
    cursor = Cursor()
    while True:
        cursor.print(mObjectManager.world)
        time.sleep(1)


def on_press(key):
    match key.char:
        case "w":
            mObjectManager.move_object(0, 0, -1)
        case "s":
            mObjectManager.move_object(0, 0, 1)
        case "a":
            mObjectManager.move_object(0, -1, 0)
        case "d":
            mObjectManager.move_object(0, 1, 0)
        case" ":
            pass
        case _:
            assert False, "ERROR: AttributeError: unexpected key {key} was pressed".format(key=key.char)
            
    if debug != False:
            # place for publisher function call
            publisher(str(mObjectManager.objectsDict[0].x)+ ',' +str(mObjectManager.objectsDict[0].y) + ',' +mObjectManager.objectsDict[0].shape + ';')


def on_release(key):
    # print('{0} released'.format(key))
    if key == keyboard.Key.esc:
        # Stop listener
        return False

def keyboardLoop():
    # Collect events until released
    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()


if __name__ == "__main__":
    mObjectManager = ObjectManager() 
    mObjectManager.create_object(1, 5, '\033[91mZ\033[0m')

    debug = True

    if debug != False:
        # network connection
        broker_address = "192.168.86.72"  
        client = mqtt.Client(client_id="Publisher", protocol=mqtt.MQTTv311)
        client.connect(broker_address, 1883, 60)

    # multithreading start
    t1 = threading.Thread(target=gameLoop)
    t2 = threading.Thread(target=keyboardLoop)
    
    if debug != False:
        t3 = threading.Thread(target=subscriber)
    
    t1.start()
    t2.start()
    t3.start()

    
    