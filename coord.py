from dataclasses import dataclass
import time, threading
from pynput import keyboard
#import paho.mqtt.client as mqtt


@dataclass
class Coord:
    x: int
    y: int
    coord = {}

    def __post_init__(self):
        for i in range(self.x):
            self.coord[i] = {}
            for j in range(self.y):
                self.coord[i][j] = '0'

    def __str__(self) -> str:
        result = ""
        for i in range(self.x):
            for j in range(self.y):
                result += self.coord[i][j]
                result += ' '
            result += '\n'
        return result

    def __getitem__(self, x, y):
        return self.coord[x][y]

@dataclass
class Object:
    x: int
    y: int
    shape: str

@dataclass
class ObjectManager:
    objectsDict = dict()
    count = 0

    def update(self, map: Coord):
        for object in self.objectsDict.values():
            print(object.x, object.y)
            self.placeObject(map, object)

    def createObject(self, x, y, shape):
        o = Object(x, y, shape)
        self.objectsDict[self.count] = o
        self.count += 1

    def placeObject(self, map: Coord, object: Object):
        map.coord[object.x][object.y] = object.shape
    
    def deleteObject(self, id):
        self.objectsDict.pop(id) # deletes id leads to fragmentation in dict
        self.count -= 1


def gameLoop():
    while True:
        print(Map)
        mObjectManager.update(Map)
        time.sleep(1)


def on_press(key):
    try:
        if key.char == "w":
            print("w is pressed")
            mObjectManager.objectsDict[0].y -= 10 
        if key.char == "s":
            mObjectManager.objectsDict[0].y += 10 
        if key.char == "a":
            mObjectManager.objectsDict[0].x -= 1 
        if key.char == "d":
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
    mObjectManager.createObject(0, 5, 'Z')
    mObjectManager.placeObject(Map, mObjectManager.objectsDict[0])
    Map.coord[4][5] = 'A'
    

    t1 = threading.Thread(target=gameLoop)
    t2 = threading.Thread(target=keyboardLoop)
    
    t1.start()
    t2.start()

    
    