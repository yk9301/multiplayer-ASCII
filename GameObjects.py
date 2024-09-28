from ANSIEscapeSequences import *
from dataclasses import dataclass
from ObjectManager import *
import time

ROLLING_BOMB_COOLDOWN = 4
MINE_COOLDOWN = 4


def place_or_throw_object(thrower_id, data_type):
    obj = ObjectManager.objectsDict[thrower_id]
    if data_type == RollingBomb:
        if obj.bomb_cooldown < ROLLING_BOMB_COOLDOWN * 400000000:
            return
    elif data_type == Mine:
        if obj.bomb_cooldown < MINE_COOLDOWN * 400000000:
            return
    direction = obj.look_direction
    if not 0 <= obj.x + direction[0] < WORLD_SIZE or not 0 <= obj.y + direction[1] < WORLD_SIZE:
        return
    ObjectManager().create_object(obj.x + direction[0], obj.y + direction[1], data_type, player=thrower_id, look_direction=direction)
    obj.time_at_bomb = time.time_ns()


def explode(obj_id: int, size):
    om = ObjectManager()
    obj = om.objectsDict[obj_id]
    om.delete_object(obj.id)
    if size == 3:
        for x in [(0, -2), (0, -1), (0, 1), (0, 2), (1, -1), (1, 0), (0, 0),
                  (1, 1), (2, 0), (-1, -1), (-1, 0), (-1, 1), (-2, 0)]:
            exp = om.create_object(min(max(x[0] + obj.x, 0), om.world_size-1), min(max(0, x[1] + obj.y), om.world_size-1),
                                   Explosion)


@dataclass
class Player(Object):
    look_direction: tuple[int, int] = (0, 1)
    bomb_cooldown: int = 0
    time_at_bomb: int = time.time_ns()

    def __post_init__(self):
        if self.id == 0:
            self.shape = '\033[91mT\033[0m'
        if self.id == 1:
            self.shape = '\033[94mY\033[0m'
        if self.id == 2:
            self.shape = '\033[93mK\033[0m'

    def update(self):
        self.bomb_cooldown = time.time_ns() - self.time_at_bomb


@dataclass
class RollingBomb(Object):
    player: int
    look_direction: tuple[int, int]
    time_since_spawn: int = 0
    time_at_spawn: int = 0
    state: int = 0

    def __post_init__(self):
        self.time_at_spawn = time.time_ns()
        self.shape = ESC.blinking(ESC.red("O"))
        self.state = 0

    def update(self):
        self.time_since_spawn = time.time_ns() - self.time_at_spawn
        t = 600000000
        if self.state == 0:
            if self.time_since_spawn > 1 * t:
                self.state = 1
                self.roll()
        elif self.state == 1:
            if self.time_since_spawn > 2 * t:
                self.state = 2
                self.roll()
        elif self.state == 2:
            if self.time_since_spawn > 3 * t:
                self.state = 3
                self.roll()
        elif self.state == 3:
            if self.time_since_spawn > 4 * t:
                pass
                explode(self.id, 3)

    def roll(self):
        ObjectManager().move_object(self.id, self.look_direction[0], self.look_direction[1])


@dataclass
class Mine(Object):
    player: int
    look_direction: tuple[int, int]
    time_since_spawn: int = 0
    time_at_spawn: int = 0

    def __post_init__(self):
        self.time_at_spawn = time.time_ns()
        self.shape = ESC.blinking(ESC.red("O"))

    def update(self):
        self.time_since_spawn = time.time_ns() - self.time_at_spawn
        t = 600000000
        if self.time_since_spawn > 4 * t:
            explode(self.id, 3)


@dataclass
class Wall(Object):
    def __post_init__(self):
        self.shape = ESC.gray("▢")

    def update(self):
        pass


@dataclass
class Explosion(Object):
    time_since_spawn: int = 0
    time_at_spawn: int = 0
    om = ObjectManager()

    def __post_init__(self):
        self.time_at_spawn = time.time_ns()
        self.shape = ESC.red("X")

    def update(self):
        self.time_since_spawn = time.time_ns() - self.time_at_spawn
        t = 100000000
        if self.time_since_spawn > t * 1:
            self.shape = ESC.orange("X")
            self.om.world.coord[self.x][self.y] = self.shape
            self.om.update_queue.put((self.x, self.y))
        if self.time_since_spawn > t * 2:
            self.shape = ESC.yellow("X")
            self.om.world.coord[self.x][self.y] = self.shape
            self.om.update_queue.put((self.x, self.y))
        if self.time_since_spawn > t * 3:
            ObjectManager().delete_object(self.id, False)
