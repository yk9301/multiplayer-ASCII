from GameObjects import *

# creates default map in file

def create_map(filename, length, height, default_char=DEFAULT_CHAR):
    fp = open(filename, "w")
    for y in range(height):
        for x in range(length):
            fp.write(default_char + " ")
        fp.write("\n")


def map_as_string(filename):
    """used for mqtt communication"""
    fp = open(filename, "r")

    world = ""
    for string in fp.readlines():
        world += string
    
    return world


def map_as_coord(world, length):
    coord = dict()

    for i in range(length):
        coord[i] = dict()

    x = 0
    y = 0
    for string in world:
        if string == " ":
            continue
        if string == "\n":
            x = 0
            y += 1
            continue
        coord[x][y] = string
        x += 1
    return coord

def map_parser(filename: str):
    """returns coord dictionary of a created map in .txt file
        ! an string like x (object) is not in objectDict !"""

    fp = open(filename, "r")
    coord = dict()

    world = ""
    length = 0

    for string in fp.readlines():
        world += string

        if length == 0:
            length = (len(string) - 1) // 2

    for i in range(length):
        coord[i] = dict()

    x = 0
    y = 0
    for string in world:
        if string == " ":
            continue
        if string == "\n":
            x = 0
            y += 1
            continue
        coord[x][y] = string
        x += 1
    return coord

def look_for_objects(objectManager: ObjectManager):
        """updates world and objectdict with created map by parser"""
        for y in range(objectManager.world_size):
            for x in range(objectManager.world_size):
                match objectManager.world.coord[x][y]:
                    case "w":
                        objectManager.create_object(x, y, Wall)
                    case "b":
                        objectManager.create_object(x, y, Bomb) # uncommend when bomb can be created
                    case "T":
                        objectManager.create_object(x, y, Player, 0)
                    case "Y":
                        objectManager.create_object(x, y, Player, 1)
                    case "K":
                        objectManager.create_object(x, y, Player, 2)

if __name__ == "__main__":
    create_map("map.txt", 10,10)
    a = map_as_string("map.txt")
    print(a)
 
