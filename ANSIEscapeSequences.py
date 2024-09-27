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

# \033[1m 	\033[21m 	set bold mode.
# \033[2m 	\033[22m 	set dim/faint mode.
# \033[3m 	\033[23m 	set italic mode.
# \033[4m 	\033[24m 	set underline mode.
# \033[5m 	\033[25m 	set blinking mode
# \033[7m 	\033[27m 	set inverse/reverse mode
# \033[8m 	\033[28m 	set hidden/invisible mode
# \033[9m 	\033[29m 	set strikethrough mode.

# \033[1m 	\033[21m 	set bold mode.
# \033[2m 	\033[22m 	set dim/faint mode.
# \033[3m 	\033[23m 	set italic mode.
# \033[4m 	\033[24m 	set underline mode.
# \033[5m 	\033[25m 	set blinking mode
# \033[7m 	\033[27m 	set inverse/reverse mode
# \033[8m 	\033[28m 	set hidden/invisible mode
# \033[9m 	\033[29m 	set strikethrough mode.

Color = {
    "GRAY": "\033[90m",
    "RED": "\033[91m",
    "GREEN": "\033[92m",
    "YELLOW": "\033[93m",
    "BLUE": "\033[94m",
    "Magenta": "\033[95m",
    "CYAN": "\033[96m",
    "WHITE": "\033[97m",
    "BLACK": "\033[30m",
    "ORANGE": "\033[38;5;214m",
}

DEFAULT_COLOR = "WHITE"



@dataclass
class ESC:
    @staticmethod
    def bold(string: str):
        return "\033[1m" + string + "\033[21m"

    @staticmethod
    def dim(string: str):
        return "\033[2m" + string + "\033[22m"

    @staticmethod
    def italic(string: str):
        return "\033[3m" + string + "\033[23m"

    @staticmethod
    def underlined(string: str):
        return "\033[4m" + string + "\033[24m"

    @staticmethod
    def blinking(string: str):
        return "\033[5m" + string + "\033[25m"

    @staticmethod
    def inverse_colors(string: str):
        return "\033[7m" + string + "\033[27m"

    @staticmethod
    def invisible(string: str):
        return "\033[8m" + string + "\033[28m"

    @staticmethod
    def strikethrough(string: str):
        """Deutsch: Durchgestrichen"""
        return "\033[9m" + string + "\033[29m"

    @staticmethod
    def gray(string: str):
        return Color["GRAY"] + string + Color[DEFAULT_COLOR]

    @staticmethod
    def red(string: str):
        return Color["RED"] + string + Color[DEFAULT_COLOR]

    @staticmethod
    def orange(string: str):
        return Color["ORANGE"] + string + Color[DEFAULT_COLOR]
        return Color["RED"] + string + Color[DEFAULT_COLOR]

    @staticmethod
    def green(string: str):
        return Color["GREEN"] + string + Color[DEFAULT_COLOR]

    @staticmethod
    def yellow(string: str):
        return Color["YELLOW"] + string + Color[DEFAULT_COLOR]
    @staticmethod
    def blue(string: str):
        return Color["BLUE"] + string + Color[DEFAULT_COLOR]

    @staticmethod
    def magenta(string: str):
        return Color["MAGENTA"] + string + Color[DEFAULT_COLOR]

    @staticmethod
    def cyan(string: str):
        return Color["CYAN"] + string + Color[DEFAULT_COLOR]

    @staticmethod
    def white(string: str):
        return Color["WHITE"] + string + Color[DEFAULT_COLOR]

    @staticmethod
    def black(string: str):
        return Color["BLACK"] + string + Color[DEFAULT_COLOR]

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

    @staticmethod
    def clear_until_end_of_screen():
        return "\033[0J"

    @staticmethod
    def save_pos():
        return "\0337"

    @staticmethod
    def load_pos():
        return "\0338"

    @staticmethod
    def goto_pos(start_x: int, start_y: int, goal_x: int, goal_y: int):
        res = ""
        if start_x > goal_x:
            res += ESC.left(start_x - goal_x)
        if start_x < goal_x:
            res += ESC.right(goal_x - start_x)
        if start_y > goal_y:
            res += ESC.up(start_y - goal_y)
        if start_y < goal_y:
            res += ESC.down(goal_y - start_y)
        return res

    @staticmethod
    def invisible_cursor():
        return "\033[?25l"

    @staticmethod
    def visible_cursor():
        return "\033[?25h"
