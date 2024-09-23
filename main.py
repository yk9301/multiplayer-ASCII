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
        cursor.print(Map)
        mObjectManager.update(Map)
        time.sleep(0.01)


def on_press(key):
    try:
        Map.coord[mObjectManager.objectsDict[0].x][mObjectManager.objectsDict[0].y] = '0'
        if key.char == "w":
            if mObjectManager.objectsDict[0].y - 1 >= 0:
                mObjectManager.objectsDict[0].y -= 1
        if key.char == "s":
            if Map.y > mObjectManager.objectsDict[0].y + 1:
                mObjectManager.objectsDict[0].y += 1
        if key.char == "a":
            if mObjectManager.objectsDict[0].x - 1 >= 0:
                mObjectManager.objectsDict[0].x -= 1
        if key.char == "d":
            if Map.x > mObjectManager.objectsDict[0].x + 1:
                mObjectManager.objectsDict[0].x += 1
    
        
        if debug != False:
            # place for publisher function call
            publisher(str(mObjectManager.objectsDict[0].x)+ ',' +str(mObjectManager.objectsDict[0].y) + ',' +mObjectManager.objectsDict[0].shape + ';')
    except AttributeError:
        print('special key {0} pressed'.format(key))

def on_release(key):
    # print('{0} released'.format(key))
    if key == keyboard.Key.esc:
        # Stop listener
        return False

def keyboardLoop():
    # Collect events until released
    with keyboard.Listener(on_press=on_press,on_release=on_release) as listener:
        listener.join()


if __name__ == "__main__":
    os.system("")

    # object init
    Map = Grid(10, 10)
    mObjectManager = ObjectManager()
    mObjectManager.createObject(1, 5, '\033[91mZ\033[0m')
    mObjectManager.placeObject(Map, mObjectManager.objectsDict[0])
    Map.coord[4][5] = '\033[92mA\033[0m'

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

    
    