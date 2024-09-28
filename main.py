from dataclasses import dataclass
import os, time, threading
from pynput import keyboard
from ObjectManager import *
from Cursor import Cursor
from parser import *
#from GameObjects import *
from publisher import *
import paho.mqtt.client as mqtt
from ANSIEscapeSequences import ESC

DEBUG = False
PLAYER = 0


def game_loop():
    cursor = Cursor()
    cursor.reprint_whole_map(mObjectManager, same_position=False)
    while True:
        cursor.print_changes(mObjectManager)
        for obj in mObjectManager.objectsDict:
            mObjectManager.objectsDict[obj].update()
        mObjectManager.update()
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
            case "f":
                throw_bomb(PLAYER)
    except AttributeError:
        print('special key {0} pressed'.format(key))
        if '{0}'.format(key) == 'Key.enter':
            print(ESC.visible_cursor())
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
        client.subscribe("update")  # subscribtion for specific subject#
        client.subscribe("map")
    else:
        print(f"Subscriber Verbindung fehlgeschlagen mit Code {rc}")

def message_parser(message):
    """enables bigger maps due to parsing coords > 10"""
    result = []
    acc = ""
    for string in message:
        if string != "," and string != ";":
            acc += string
        if string == "," or string == ";":
            result.append(int(acc))
            acc = ""
    return result

def on_message(client, userdata, msg):
    message = msg.payload.decode()
    topic = msg.topic
    
    match topic:
        case "update":
            array = message_parser(message)
            x, y, id = array[0], array[1], array[2]
            if array[2] > 2:
                mObjectManager.create_object(x, y, Bomb, id)
            else:
                mObjectManager.move_object(id,x - mObjectManager.objectsDict[id].x, y - mObjectManager.objectsDict[id].y)
        case "map":
            if message == "0" and PLAYER == 1:
                publisher(str(len(str(mObjectManager.world_size))) + str(mObjectManager.world_size) + mObjectManager.world_as_string, PLAYER, "map")
            if message != "0" and PLAYER != 1:
                i = int(message[0]) # first string is len
                mObjectManager.world.coord = map_as_coord(message[(i + 1):], mObjectManager.world.x)
                look_for_objects(mObjectManager)
                mObjectManager.map_shared = True


if __name__ == "__main__":
    print(ESC.invisible_cursor(), end="\r")
    mObjectManager = ObjectManager()
    
    if DEBUG is False:
        if PLAYER == 1:
            mObjectManager.world.coord = map_parser("map.txt")
            look_for_objects(mObjectManager) # loads players if placed on map.txt

            # saves map as string to share it to player
            mObjectManager.world_as_string = map_as_string("map.txt")

            t1 = threading.Thread(target=subscriber)
            t1.start()
        else:
            # other players waiting in loop until they recieve the map
            t1 = threading.Thread(target=subscriber)
            t1.start()
            counter = 0
            while(mObjectManager.map_shared == False):
                publisher("0", PLAYER, "map")
                time.sleep(0.1)
                print(f"\r waiting for map {bin(counter)}", end="\r")
                counter += 1
                
            
    else:
        mObjectManager.world.coord = map_parser("map.txt")
        look_for_objects(mObjectManager) # loads players if placed on map.txt


    # multithreading start
    t2 = threading.Thread(target=game_loop)
    t3 = threading.Thread(target=keyboard_loop)
    
    t2.start()
    t3.start()

    
    