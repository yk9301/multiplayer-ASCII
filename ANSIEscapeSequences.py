from dataclasses import dataclass

# https://gist.github.com/fnky/458719343aabd01cfb17a3a4f7296797
#  \033#A 	moves cursor up # lines                         A
#  \033#B 	moves cursor down # lines                     D   C
#  \033#C 	moves cursor right # columns                    B
#  \033#D 	moves cursor left # columns
#  \033[H   moves cursor to 0, 0
#  \033[2J 	erase entire screen
#  \033[2K 	erase the entire line
#  "\r"     move cursor to the beginning of line
# https://www.unicode.org/charts/PDF/U2600.pdf

Color = {
    "HEADER": "\033[95m",
    "BLUE": "\033[94m",
    "GREEN": "\033[92m",
    "RED": "\033[91m",
    "ENDC": "\033[0m",
}
@dataclass
class ESC:
    @staticmethod
    def red(string : str):
        return Color["RED"] + string + Color["ENDC"]

    @staticmethod
    def green(string : str):
        return Color["GREEN"] + string + Color["ENDC"]

    @staticmethod
    def blue(string : str):
        return Color["BLUE"] + string + Color["ENDC"]

    @staticmethod
    def up(n: int):
        return f"\033[{n}A"

    @staticmethod
    def down(n: int):
        return f"\033[{n}B"

    @staticmethod
    def left(n: int):
        return f"\033[{n}D"

    @staticmethod
    def right(n: int):
        return f"\033[{n}C"

    @staticmethod
    def start_of_line():
        return "\r"

    @staticmethod
    def go_home():
        return "\033[H"

    @staticmethod
    def clear_screen():
        return "\033[2J"

    @staticmethod
    def clear_line():
        return "\033[2K"
