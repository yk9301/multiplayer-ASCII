from dataclasses import dataclass
import os, time, threading
from pynput import keyboard
from ObjectManager import *
from Cursor import Cursor
from GameObjects import *
from publisher import *
import paho.mqtt.client as mqtt
from ANSIEscapeSequences import ESC

DEBUG = True
PLAYER = 1

def game_loop():
    cursor = Cursor()
    cursor.reprint_whole_map(mObjectManager, same_position=False)
    while True:
        cursor.print_changes(mObjectManager)
        time.sleep(0.01)


def on_press(key):
    try:
        match key.char:
            case "w":
                mObjectManager.move_object(PLAYER, 0, -1)
            case "s":
                mObjectManager.move_object(PLAYER, 0, 1)
            case "a":
                mObjectManager.move_object(PLAYER, -1, 0)
            case "d":
                mObjectManager.move_object(PLAYER, 1, 0)
    except AttributeError:
        print('special key {0} pressed'.format(key))
        if '{0}'.format(key) == 'Key.enter':
            os._exit(0)

    if not DEBUG:
            # place for publisher function call
            publisher(str(mObjectManager.objectsDict[PLAYER].x)+ ',' +str(mObjectManager.objectsDict[PLAYER].y) + ',' + str(mObjectManager.objectsDict[PLAYER].id) + ';', PLAYER)


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
    #logging.basicConfig(level=logging.DEBUG)

    # Client initialisieren
    subscriber = "subscriber" + str(PLAYER)
    client = mqtt.Client(client_id=subscriber, protocol=mqtt.MQTTv311)
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
        print(f"failed connection attemp: {e}, Debug Mode activ")
        

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
    
    # Aktion basierend auf der Nachricht ausführen
    if topic == "update":
        x = int(message[0])
        y = int(message[2])
        id = int(message[4:-1])
        
        mObjectManager.move_object(id,x - mObjectManager.objectsDict[id].x, y - mObjectManager.objectsDict[id].y)
        

if __name__ == "__main__":
    mObjectManager = ObjectManager()
    
    # map is loaded by parser
    mObjectManager.world.coord = map_parser("map.txt")
    mObjectManager.look_for_objects() # adds objects to dict

    # player init
    mObjectManager.create_object(0, 9, Player, 0)
    mObjectManager.create_object(0,0, Player, 1)
    mObjectManager.create_object(9,9, Player, 2)

    # multithreading start
    t1 = threading.Thread(target=game_loop)
    t2 = threading.Thread(target=keyboard_loop)
    
    if not DEBUG:
        t3 = threading.Thread(target=subscriber)
        t3.start()
    
    t1.start()
    t2.start()

    
    