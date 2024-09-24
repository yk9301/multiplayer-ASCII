import os
from dataclasses import dataclass
from ANSIEscapeSequences import *
from Coord import Grid
from ObjectManager import *

@dataclass
class Cursor:
    x: int = None
    y: int = None
    mObjectManager: ObjectManager = None
    def __init__(self):
        self.reset()

    def reset(self):
        print(ESC.clear_screen())
        self.x, self.y = 0, 0

    def goto(self, x: int, y: int):
        if self.x > x:
            print(ESC.left(self.x - x))
        if self.x < x:
            print(ESC.right(x - self.x))
        if self.y > y:
            print(ESC.up(self.y - y))
        if self.y < y:
            print(ESC.down(self.y - y))
        self.x, self.y = x, y

    def go_home(self):
        print(ESC.go_home())

    def print(self, char: str, x: int, y: int):
        assert len(char) == 1
        self.goto(x, y)
        print(char, end='')
        self.x += 1

    def print(self, grid: Grid):
        self.reset()
        for y in range(grid.y):
            for x in range(grid.x):
                print(grid.coord[x][y], end=' ')
            print()
        print(ESC.go_home())
        self.x, self.y = 0, 0


if __name__ == "__main__":
    cur = Cursor()
