from dataclasses import dataclass

DEFAULT_CHAR = "."

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
