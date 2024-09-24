from dataclasses import dataclass
import os, time, threading, logging
from pynput import keyboard
from ObjectManager import *
from Cursor import Cursor
from publisher import *
import paho.mqtt.client as mqtt



def gameLoop():
    cursor = Cursor()
    while True:
        cursor.print(Map)
        mObjectManager.update(Map)
        time.sleep(0.1)


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

def subscriber():
    # Logging aktivieren für detaillierte Debug-Informationen
    logging.basicConfig(level=logging.DEBUG)

    # Client initialisieren
    client = mqtt.Client(client_id="subscriber1", protocol=mqtt.MQTTv311)
    client.enable_logger()

    # Broker-Adresse und Port
    broker_address = "192.168.86.72" 
    port = 1883  # Standard-MQTT-Port

    # callbacks
    client.on_connect = on_connect
    client.on_message = on_message

    # try to connect
    try:
        client.connect(broker_address, port=port, keepalive=60)
    except Exception as e:
        print(f"Verbindungsfehler: {e}")
        exit(1)

    # loop
    client.loop_forever()


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Subscriber verbunden")
        client.subscribe("update")  # subscribtion for specific subject
    else:
        print(f"Subscriber Verbindung fehlgeschlagen mit Code {rc}")


def on_message(client, userdata, msg):
    message = msg.payload.decode()
    topic = msg.topic
    print(f"Nachricht empfangen: Thema: {topic}, Nachricht: {message}")
    
    # Aktion basierend auf der Nachricht ausführen
    if topic == "update":
        print(message)
        



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

    
    