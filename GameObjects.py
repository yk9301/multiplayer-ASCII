from ANSIEscapeSequences import *
from dataclasses import dataclass
import time
from ANSIEscapeSequences import ESC


@dataclass
class Object:
    x: int
    y: int
    id: int
    shape = None


@dataclass
class Player(Object):
    look_direction: str = 'w'

    def __post_init__(self):
        if self.id == 0:
            self.shape = '\033[91mT\033[0m'
        if self.id == 1:
            self.shape = '\033[94mY\033[0m'
        if self.id == 2:
            self.shape = '\033[93mK\033[0m'



@dataclass
class Bomb(Object):
    player: int
    look_direction: int
    time_since_spawn: int = 0
    time_at_spawn: int = 0
    state: int = 0

    def __init__(self):
        self.time_since_spawn = 0
        self.time_at_spawn = time.time_ns()
        self.state = 0
        self.shape = ESC.red("B")

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
        self.shape = ESC.gray(ESC.blinking("x"))

