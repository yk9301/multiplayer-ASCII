from dataclasses import dataclass

@dataclass
class Grid:
    x: int
    y: int
    coord = {}

    def __post_init__(self):
        for x in range(self.x):
            self.coord[x] = {}
            for y in range(self.y):
                self.coord[x][y] = '0'

    def __getitem__(self, x, y):
        return self.coord[x][y]
    
