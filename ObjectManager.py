from dataclasses import dataclass
from queue import SimpleQueue
from Coord import *

WORLD_SIZE = 10


@dataclass
class Object:
    x: int
    y: int
    id: int
    shape = None


@dataclass
class ObjectManager:
    instance = None
    objectsDict = dict()
    total_objects = 0  # is used for the id, ids are always unique and never re-used.
    world_size = WORLD_SIZE
    world = Grid(WORLD_SIZE, WORLD_SIZE)
    update_queue = SimpleQueue()
    delete_queue = SimpleQueue()
    create_queue = SimpleQueue()

    def __new__(cls):
        if not cls.instance:
            cls.instance = super(ObjectManager, cls).__new__(cls)
        return cls.instance

    def update(self):
        while self.create_queue.qsize() > 0:
            obj = self.create_queue.get()
            self.objectsDict[obj.id] = obj
            self.world[(obj.x, obj.y)] = obj.shape
            self.update_queue.put((obj.x, obj.y))

        while self.delete_queue.qsize() > 0:
            obj = self.objectsDict[self.delete_queue.get()]
            self.objectsDict.pop(obj.id)
            self.world.coord[obj.x][obj.y] = self.world.default_char
            self.update_queue.put((obj.x, obj.y))

    def create_object(self, x, y, datatype, id=None, **super_vars):
        obj = datatype(x, y, self.total_objects if id is None else id, **super_vars)
        self.total_objects += 1
        self.create_queue.put(obj)
        return obj.id

    def delete_object(self, obj_id, throw_error=True):
        if obj_id in self.objectsDict or not throw_error:
            self.delete_queue.put(obj_id)
        elif throw_error:
            assert False, "ERROR: Attempt to delete an object that is not in objectsDict."

    def move_object(self, object_or_id: Object | int, right, down, relative=True):
        """down and right are relative coordinates. right = 2 means obj.x += 2"""
        if object_or_id is Object:
            obj = object_or_id
        else:
            if object_or_id not in self.objectsDict:
                assert False, "ERROR: Attempt to move an object that is not in objectsDict."
            obj = self.objectsDict[object_or_id]

        # Change the facing direction of the object, if applicable
        try:
            obj.look_direction = (right, down)
        except AttributeError:
            pass

        # Collision
        try:
            if not self.world.coord[obj.x + right][obj.y + down] == self.world.default_char:
                return
        except KeyError:
            return

        # Place '0' where the object used to be - add to draw queue
        self.world[(obj.x, obj.y)] = self.world.default_char
        self.update_queue.put((obj.x, obj.y))

        # Update Object position
        if relative:
            x, y = obj.x + right, obj.y + down
        else:
            x, y = right, down
        obj.x, obj.y = min(max(x, 0), self.world_size - 1), min(max(y, 0), self.world_size - 1)

        # Place obj.shape where object should go - add to draw queue
        self.world[(obj.x, obj.y)] = obj.shape
        self.update_queue.put((obj.x, obj.y))

    def get_pos(self, object_or_id):
        """A tuple is returned, unpack with: x, y = get_pos(object_or_id)"""
        if object_or_id is Object:
            return object_or_id.x, object_or_id.y
        return self.objectsDict[id].x, self.objectsDict[id].y

    def dequeue(self):
        return self.update_queue.get()