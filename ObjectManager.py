from dataclasses import dataclass
from Coord import *

@dataclass
class Object:
    x: int
    y: int
    shape: str

@dataclass
class ObjectManager:
    objectsDict = dict()
    count = 0

    def update(self, map: Grid):
        for object in self.objectsDict.values():
            print(object.x, object.y)
            self.placeObject(map, object)

    def createObject(self, x, y, shape):
        o = Object(x, y, shape)
        self.objectsDict[self.count] = o
        self.count += 1

    def placeObject(self, map: Grid, object: Object):
        map.coord[object.x][object.y] = object.shape
    
    def deleteObject(self, id):
        self.objectsDict.pop(id) # deletes id leads to fragmentation in dict
        self.count -= 1