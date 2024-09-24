from ObjectManager import Object
from dataclasses import dataclass
import time

@dataclass
class Player(Object):
    def __post_init__(self):
        if self.id == 0:
            self.shape = '\033[91mT\033[0m'
        if self.id == 1:
            self.shape = '\033[94mY\033[0m'
        if self.id == 2:
            self.shape = '\033[93mK\033[0m'


@dataclass
class Bomb(Object):
    time_since_spawn: int
    time_at_spawn: int

    def __post_init__(self):
        time_since_spawn = 0
        time_at_spawn = 0

    def update(self):
        if self.timer < self.current_time:
            pass

@dataclass
class Wall(Object):
    def __post_init__(self):
        self.shape = '\033[90mx\033[0m'
                