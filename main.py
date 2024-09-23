from dataclasses import dataclass
import time, threading
from pynput import keyboard
from ObjectManager import *

#import paho.mqtt.client as mqtt



def gameLoop():
    while True:
        print(Map)
        mObjectManager.update(Map)
        time.sleep(0.01)


def on_press(key):
    try:
        if key.char == "w":
            print("w")
            Map.coord[mObjectManager.objectsDict[0].x][mObjectManager.objectsDict[0].y] = '0'
            mObjectManager.objectsDict[0].y -= 10 
        if key.char == "s":
            Map.coord[mObjectManager.objectsDict[0].x][mObjectManager.objectsDict[0].y] = '0'
            mObjectManager.objectsDict[0].y += 10 
        if key.char == "a":
            #Map.coord[mObjectManager.objectsDict[0].x][mObjectManager.objectsDict[0].y] = '0'
            mObjectManager.objectsDict[0].x -= 1 
        if key.char == "d":
            #Map.coord[mObjectManager.objectsDict[0].x][mObjectManager.objectsDict[0].y] = '0'
            mObjectManager.objectsDict[0].x += 1 
        if key.char == " ":
            pass
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
    Map = Coord(10, 10)
    mObjectManager = ObjectManager() 
    mObjectManager.createObject(1, 5, 'Z')
    mObjectManager.placeObject(Map, mObjectManager.objectsDict[0])
    Map.coord[4][5] = 'A'
    

    t1 = threading.Thread(target=gameLoop)
    t2 = threading.Thread(target=keyboardLoop)
    
    t1.start()
    t2.start()

    
    