from dataclasses import dataclass
DEFAULT_CHAR = "▢"


@dataclass
class Grid:
    x: int
    y: int
    coord = {}
    default_char = DEFAULT_CHAR

    def __post_init__(self):
        for i in range(self.x):
            self.coord[i] = {}
            for j in range(self.y):
                self.coord[i][j] = self.default_char

    def __getitem__(self, x, y):
        return self.coord[x][y]

    def __setitem__(self, key, s):
        x, y = key
        self.coord[x][y] = s
    
# creates default map in file
def create_map(filename, length, height, default_char=DEFAULT_CHAR):
    fp = open(filename, "w")
    for y in range(height):
        for x in range(length):
            fp.write(default_char + " ")
        fp.write("\n")

def map_parser(filename: str):
    fp = open(filename, "r")
    coord = dict()

    x = 0
    y = 0

    for string in fp.read():
        if string == " ":
            continue
        if string == "\n":
            x = 0
            y += 1
            continue
        #coord[x][y] = string
        x += 1
    print(result)
    return coord

if __name__ == "__main__":
    #create_map("map.txt", 3,3)
    print(map_parser("map.txt"))