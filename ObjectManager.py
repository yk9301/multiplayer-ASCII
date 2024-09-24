from dataclasses import dataclass
from Coord import *
WORLD_SIZE = 10


@dataclass
class Object:
    x: int
    y: int
    shape: str
    id: int


@dataclass
class ObjectManager:
    objectsDict = dict()
    total_objects = 0  # is used for the id, ids are always unique and never re-used.
    world_size = WORLD_SIZE
    world = Coord(WORLD_SIZE, WORLD_SIZE)

    def __init__(self):
        world = Coord(self.world_size, self.world_size)

    def create_object(self, x, y, shape):
        obj = Object(x, y, shape, self.total_objects)
        self.total_objects += 1
        self.objectsDict[obj.id] = obj
        self.world[(x, y)] = obj.shape

    def delete_object(self, object_or_id):
        if object_or_id is Object:
            is_deleted = self.objectsDict.pop(object_or_id.id)
        else:
            is_deleted = self.objectsDict.pop(object_or_id)
        if not is_deleted:
            assert False, "ERROR: Attempt to delete an object that is not in objectsDict."

    def move_object(self, object_or_id: Object | int, down, right):
        """down and right are relative coordinates. right = 1 means obj.x += 1"""
        if object_or_id is Object:
            obj = object_or_id
        else:
            if object_or_id not in self.objectsDict:
                assert False, "ERROR: Attempt to move an object that is not in objectsDict."
            obj = self.objectsDict[object_or_id]
        self.world[(obj.x, obj.y)] = self.world.default_char
        obj.x, obj.y = min(max(obj.x + right, 0), self.world_size - 1), min(max(obj.y + down, 0), self.world_size - 1)
        self.world[(obj.x, obj.y)] = obj.shape
