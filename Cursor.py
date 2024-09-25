import os
from dataclasses import dataclass
from ANSIEscapeSequences import *
from Coord import Grid
from ObjectManager import *


@dataclass
class Cursor:
    x: int = None
    y: int = None
    debug_stack_pointer: int = 0

    def __init__(self):
        self.reset()

    def reset(self):
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

    def print_char(self, char: str, x: int, y: int):
        assert len(char) == 1
        print(ESC.goto_pos(self.x, self.y, x, y) + char, end='')
        self.x, self.y = x + 1, y

    def print_changes(self, object_manager: ObjectManager):
        if object_manager.queue.empty():
            return

        res = ESC.load_pos() + ESC.clear_until_end_of_screen()
        while not object_manager.queue.empty():
            x, y = object_manager.queue.get()
            res += ESC.goto_pos(self.x, self.y, x * 2 , y) + object_manager.world.coord[x][y]
            self.x = x * 2 + 1
            self.y = y

        res += ESC.goto_pos(self.x, self.y, 0, object_manager.world_size + self.debug_stack_pointer) + ESC.save_pos()
        self.x, self.y = 0, self.debug_stack_pointer + object_manager.world_size
        print(res, end="\r")

    def reprint_whole_map(self, object_manager: ObjectManager, same_position=True):
        res = ESC.load_pos() + ESC.clear_until_end_of_screen() + ESC.up(self.debug_stack_pointer + object_manager.world_size)
        if not same_position:
            res = ""
        res += ESC.clear_until_end_of_screen()

        for y in range(object_manager.world_size):
            for x in range(object_manager.world_size):
                try:
                    res += str(object_manager.world.coord[x][y]) + " "
                except Exception:
                    print(x, y)
            res += "\n"

        res += ESC.save_pos()

        self.x = 0
        self.y = object_manager.world_size
        self.debug_stack_pointer = 0
        print(res, end="\r")

    def print_debug(self, line: str):
        """Only enter one Line!!"""
        self.debug_stack_pointer += 1
        res = ESC.load_pos() + ESC.clear_until_end_of_screen() + line + "\n" + ESC.save_pos()
        self.y += 1
        print(res, end="\r")
