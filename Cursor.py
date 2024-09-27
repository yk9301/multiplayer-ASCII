import os
from dataclasses import dataclass
from ANSIEscapeSequences import *
from Coord import Grid
from ObjectManager import *


@dataclass
class Cursor:
    # Structure:
    # 0 0 0 0 <- Map
    # 0 0 0 0
    # 0 0 0 0
    # Debug_1 <- Debug Stack
    # Debug_n
    # <- Saved Position (load with ESC.load_pos())
    x: int = None
    y: int = None
    debug_stack_pointer: int = 0

    def __init__(self):
        self.x, self.y = 0, 0

    def print_changes(self, object_manager: ObjectManager):
        if object_manager.update_queue.empty():
            pass
        """update the symbols for every position in the ObjectManagers queue"""
        if object_manager.queue.empty():
            return
        # reset cursor to the top of the debug stack and clear everything other things may have printed
        res = ESC.load_pos() + ESC.clear_until_end_of_screen()
        while not object_manager.update_queue.empty():
            x, y = object_manager.update_queue.get()
            try:  # This try-catch is because for some reason it doesn't work without.
                res += ESC.goto_pos(self.x, self.y, x * 2, y) + object_manager.world.coord[x][y]
            except TypeError:
                pass
            self.x = x * 2 + 1
            self.y = y
        # go to the end of the debug stack and save the position
        res += (ESC.goto_pos(self.x, self.y, 0, object_manager.world_size + self.debug_stack_pointer)
                + ESC.save_pos())
        # update the position
        self.x, self.y = 0, self.debug_stack_pointer + object_manager.world_size
        # print the string and add a \r so the terminal updates itself. It does not get updated without \n or \r
        print(res, end="\r")

    def reprint_whole_map(self, object_manager: ObjectManager, same_position=True):
        """Print the whole map. Use this for the initialization and if something went wrong when updating changes.
        Set same_position to False if the map should get printed at the current cursor position"""
        res = ""
        if same_position:
            res = (ESC.load_pos() + ESC.clear_until_end_of_screen() +
                   ESC.up(self.debug_stack_pointer + object_manager.world_size))
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
        """Only enter one Line!! This line will be added to the bottom of the debug stack"""
        self.debug_stack_pointer += 1
        res = ESC.load_pos() + ESC.clear_until_end_of_screen() + line + "\n" + ESC.save_pos()
        self.y += 1
        print(res, end="\r")
