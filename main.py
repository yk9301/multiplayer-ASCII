from dataclasses import dataclass
import os, time, threading, logging
from pynput import keyboard
from ObjectManager import *
from Cursor import Cursor
from publisher import *
import paho.mqtt.client as mqtt

DEBUG = False

def game_loop():
    cursor = Cursor(mObjectManager)
    while True:
        cursor.print(mObjectManager.world)
        time.sleep(0.001)


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
            
    if not DEBUG:
            # place for publisher function call
            publisher(str(mObjectManager.objectsDict[0].x)+ ',' +str(mObjectManager.objectsDict[0].y) + ',' + str(mObjectManager.objectsDict[0].id) + ';')


def on_release(key):
    # print('{0} released'.format(key))
    if key == keyboard.Key.esc:
        # Stop listener
        return False


def keyboard_loop():
    # Collect events until released
    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
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
        x = int(message[0])  
        y = int(message[2])
        id = int(message[4:-1])
        print(message * 100)
        mObjectManager.objectsDict[id].x = x
        mObjectManager.objectsDict[id].y = y
        #mObjectManager.move_object(id,x - mObjectManager.objectsDict[id].x, y - mObjectManager.objectsDict[id].y)
        

if __name__ == "__main__":
    mObjectManager = ObjectManager() 
    mObjectManager.create_object(1, 5, '\033[91mZ\033[0m')

    if not DEBUG:
        # network connection
        broker_address = "192.168.86.72"  
        client = mqtt.Client(client_id="Publisher", protocol=mqtt.MQTTv311)
        client.connect(broker_address, 1883, 60)

    # multithreading start
    t1 = threading.Thread(target=game_loop)
    t2 = threading.Thread(target=keyboard_loop)
    
    if not DEBUG:
        t3 = threading.Thread(target=subscriber)
    
    t1.start()
    t2.start()
    t3.start()

    
    