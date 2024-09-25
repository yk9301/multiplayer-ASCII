from ObjectManager import Object
from dataclasses import dataclass
import time

@dataclass
class Player(Object):
    look_direction: tuple[int, int] = (0, 1)

    def __post_init__(self):
        if self.id == 0:
            self.shape = '\033[91mT\033[0m'
        if self.id == 1:
            self.shape = '\033[94mY\033[0m'
        if self.id == 2:
            self.shape = '\033[93mK\033[0m'


    def throw_bomb(self):
        pass


@dataclass
class Bomb(Object):
    player: int
    look_direction: tuple[int, int]
    time_since_spawn: int = 0
    time_at_spawn: int = 0
    state: int = 0

    def __post_init__(self):
        self.time_at_spawn = time.time_ns()

    def update(self):
        self.time_since_spawn = time.time_ns() - self.time_at_spawn

        if self.state == 0:
            if self.time_since_spawn > 300000:
                self.state = 1
                self.roll()
        elif self.state == 1:
            if self.time_at_spawn > 600000:
                self.state = 2
                self.roll()
        elif self.state == 2:
            if self.time_at_spawn > 900000:
                self.state = 3
                self.roll()
        elif self.state == 3:
            if self.time_at_spawn > 1200000:
                self.explode()

    def roll(self):
        pass

    def explode(self):
        pass


@dataclass
class Wall(Object):
    def __post_init__(self):
        self.shape = '\033[90mx\033[0m'

