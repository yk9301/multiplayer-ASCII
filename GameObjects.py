from ObjectManager import Object
from dataclasses import dataclass
import time

@dataclass
class Player(Object):
    pass


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
