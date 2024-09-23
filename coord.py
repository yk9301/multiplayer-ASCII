from dataclasses import dataclass

@dataclass
class Coord:
    x: int
    y: int
    coord = {}

    def __post_init__(self):
        for i in range(self.x):
            self.coord[i] = {}
            for j in range(self.y):
                self.coord[i][j] = '0'

    def __str__(self) -> str:
        result = ""
        for j in range(self.y):
            for i in range(self.x):
                result += self.coord[i][j]
                result += ' '
            result += '\n'
        return result

    def __getitem__(self, x, y):
        return self.coord[x][y]
    
