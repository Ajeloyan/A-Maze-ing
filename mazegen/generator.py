from .validator import MazeConfig
from enum import Enum
from random import shuffle, choice, randint


class EntryExitError(Exception):
    print("Entry and Exit should be in a valid cell")


class Tiles(Enum):
    WALL_H = "▀▀▀▀▀▀"
    PATH_H = "      "
    MID_NO = " "
    MID_PATH = "       "
    JOINT_FULL = "█"
    JOINT_THIN = "▀"
    MID_WALL = "█"
    BOTTOM = "▀▀▀▀▀▀"
    CORNER_BOT = "▀"
    FIXED = "███████"
    PATH_TOP = " ████ "
    PATH_BOT = " ▀▀▀▀ "


class Cell:
    def __init__(self, x: int, y: int) -> None:
        self.x: int = x
        self.y: int = y
        self.walls = {
            "north": True,
            "south": True,
            "east": True,
            "west": True
        }
        self.is_visited = False
        self.bin: list[int] = [0, 0, 0, 0]
        self.hex: str = ""
        self.fixed: bool = False
        self.id: int = 0
        self.in_path = False
        self.spec = False

    def is_fixed(self) -> None:
        if self.fixed is True:
            self.walls["north"] = True
            self.walls["south"] = True
            self.walls["east"] = True
            self.walls["west"] = True

    def __repr__(self):
        return f"{self.x}: {self.y}"

    def binary(self) -> None:
        if self.walls["north"] is True:
            self.bin[0] = 1
        if self.walls["east"] is True:
            self.bin[1] = 1
        if self.walls["south"] is True:
            self.bin[2] = 1
        if self.walls["west"] is True:
            self.bin[3] = 1

    def hexa(self) -> None:
        if self.bin == [0, 0, 0, 0]:
            self.hex = "0"
        elif self.bin == [0, 0, 0, 1]:
            self.hex = "1"
        elif self.bin == [0, 0, 1, 0]:
            self.hex = "2"
        elif self.bin == [0, 0, 1, 1]:
            self.hex = "3"
        elif self.bin == [0, 1, 0, 0]:
            self.hex = "4"
        elif self.bin == [0, 1, 0, 1]:
            self.hex = "5"
        elif self.bin == [0, 1, 1, 0]:
            self.hex = "6"
        elif self.bin == [0, 1, 1, 1]:
            self.hex = "7"
        elif self.bin == [1, 0, 0, 0]:
            self.hex = "8"
        elif self.bin == [1, 0, 0, 1]:
            self.hex = "9"
        elif self.bin == [1, 0, 1, 0]:
            self.hex = "A"
        elif self.bin == [1, 0, 1, 1]:
            self.hex = "B"
        elif self.bin == [1, 1, 0, 0]:
            self.hex = "C"
        elif self.bin == [1, 1, 0, 1]:
            self.hex = "D"
        elif self.bin == [1, 1, 1, 0]:
            self.hex = "E"
        elif self.bin == [1, 1, 1, 1]:
            self.hex = "F"


class Grid:
    def __init__(self, config: MazeConfig) -> None:
        self.width: int = config.WIDTH
        self.height: int = config.HEIGHT
        self.matrix: list[list[Cell]] = [[Cell(x, y) for
                                          x in range(self.width)]
                                         for y in range(self.height)]
        self.count_tot = self.width * self.height
        self.all_visited: bool = True if self.count_tot == 0 else False
        self.repeat: int = 10
        self.ENTRY = config.ENTRY
        self.EXIT = config.EXIT
        self.is_digged: bool = False
        self.is_perfect: bool = config.PERFECT
        self.wall_color: str = config.WALL_COLOR
        self.path_color: str = config.PATH_COLOR
        self.spec_color: str = config.SPEC_COLOR

    def coloration(self, cell, text):
       
        if cell.in_path and (text is Tiles.PATH_TOP.value or
                             text is Tiles.PATH_BOT.value):
            return f"{self.path_color.define()}{text}\033[0m"
        elif cell.spec and (text is Tiles.PATH_TOP.value or
                            text is Tiles.PATH_BOT.value):
            return f"{self.spec_color.define()}{text}\033[0m"
        else:
            return f"{self.wall_color.define()}{text}\033[0m"

    def draw_grid(self) -> None:
        print("\033[H")
        if self.width >= 11 and self.height >= 10:
            self.forty_two()
        if self.matrix[self.ENTRY[1]][self.ENTRY[0]].fixed:
            print("ERROR")
        for y in range(self.height):
            for x in range(self.width):
                cell = self.matrix[y][x]

                if cell.fixed:
                    print(self.coloration(cell, Tiles.FIXED.value), end="")
                    continue
                if cell.walls["west"]:
                    print(self.coloration(cell,
                          Tiles.JOINT_FULL.value), end="")
                else:
                    print(self.coloration(cell,
                          Tiles.JOINT_THIN.value), end="")

                if cell.walls["north"]:
                    print(self.coloration(cell,
                          Tiles.WALL_H.value), end="")
                else:
                    print(self.coloration(cell,
                          Tiles.PATH_H.value), end="")

            print(self.coloration(cell, Tiles.MID_WALL.value))
            for i in range(2):
                for x in range(self.width):
                    cell = self.matrix[y][x]

                    if cell.fixed:
                        print(self.coloration(cell,
                              Tiles.FIXED.value), end="")
                        continue

                    if cell.walls["west"]:
                        print(self.coloration(cell,
                              Tiles.MID_WALL.value), end="")
                    else:
                        print(self.coloration(cell,
                              Tiles.MID_NO.value), end="")

                    if cell.in_path or cell.spec:
                        if i == 0:
                            print(self.coloration(cell,
                                  Tiles.PATH_TOP.value), end="")
                        if i == 1:
                            print(self.coloration(cell,
                                  Tiles.PATH_BOT.value), end="")
                    else:
                        print(self.coloration(cell,
                              Tiles.PATH_H.value), end="")
                print(self.coloration(cell, Tiles.MID_WALL.value))

        for x in range(self.width):
            print(self.coloration(cell, Tiles.CORNER_BOT.value +
                  Tiles.BOTTOM.value), end="")
        print(f"{self.coloration(cell, Tiles.CORNER_BOT.value)}\033[K",
              flush=True)

    def mid_cellule(self) -> Cell:
        x = self.width // 2
        y = self.height // 2
        mid_cell: Cell = self.matrix[y][x]
        return mid_cell

    def forty_two(self) -> None:
        mid_cell: Cell = self.mid_cellule()
        x: int = mid_cell.x
        y: int = mid_cell.y
        j: int = 1
        for j in range(1, 3):
            self.matrix[y][x - j].fixed = True
            self.matrix[y][x - j - 1].fixed = True
        j = 0
        for j in range(0, 2):
            self.matrix[y - j][x - 3].fixed = True
            self.matrix[y - j - 1][x - 3].fixed = True
        j = 0
        for j in range(1, 3):
            self.matrix[y + j][x - 1].fixed = True
            self.matrix[y + j - 1][x - 1].fixed = True
        i: int = 1
        for i in range(1, 3):
            self.matrix[y][x + i].fixed = True
            self.matrix[y][x + i + 1].fixed = True
        i = 1
        for i in range(1, 3):
            self.matrix[y - 2][x + i].fixed = True
            self.matrix[y - 2][x + i + 1].fixed = True
        i = 1
        for i in range(1, 3):
            self.matrix[y + 2][x + i].fixed = True
            self.matrix[y + 2][x + i + 1].fixed = True
        i = 1
        for i in range(0, 2):
            self.matrix[y - i][x + 3].fixed = True
            self.matrix[y - i - 1][x + 3].fixed = True
        i = 1
        for i in range(0, 2):
            self.matrix[y + i][x + 1].fixed = True
            self.matrix[y + i + 1][x + 1].fixed = True

    def break_wall(self, cell_a: Cell, cell_b: Cell) -> None:
        if cell_b.x > cell_a.x:
            cell_b.walls["west"] = False
            cell_a.walls["east"] = False
        elif cell_b.y > cell_a.y:
            cell_b.walls["north"] = False
            cell_a.walls["south"] = False
        elif cell_a.x > cell_b.x:
            cell_a.walls["west"] = False
            cell_b.walls["east"] = False
        elif cell_a.y > cell_b.y:
            cell_a.walls["north"] = False
            cell_b.walls["south"] = False

    def add_wall(self, cell_a: Cell, cell_b: Cell) -> None:
        if cell_b.x > cell_a.x:
            cell_b.walls["west"] = True
            cell_a.walls["east"] = True
        elif cell_b.y > cell_a.y:
            cell_b.walls["north"] = True
            cell_a.walls["south"] = True
        elif cell_a.x > cell_b.x:
            cell_a.walls["west"] = True
            cell_b.walls["east"] = True
        elif cell_a.y > cell_b.y:
            cell_a.walls["north"] = True
            cell_b.walls["south"] = True

    def dig_maze(self) -> None:
        i = 1
        walls: list = []
        for y in range(self.height):
            for x in range(self.width):
                self.matrix[y][x].id = i
                i += 1
                if x < self.width - 1:
                    walls.append((self.matrix[y][x], self.matrix[y][x + 1]))
                if y < self.height - 1:
                    walls.append((self.matrix[y][x], self.matrix[y + 1][x]))
        shuffle(walls)
        for i, (cell_a, cell_b) in enumerate(walls):
            if cell_a.fixed is True or cell_b.fixed is True:
                continue
            if cell_a.id != cell_b.id or i % (self.width + self.height) == 0 and \
               self.is_perfect is False:
                self.break_wall(cell_a, cell_b)
                check_id = cell_a.id
                for y in range(self.height):
                    for x in range(self.width):
                        if self.matrix[y][x].id == check_id:
                            self.matrix[y][x].id = cell_b.id

            self.draw_grid()
        self.is_digged = True
        for y in range(self.height):
            for x in range(self.width):
                self.matrix[y][x].binary()
                self.matrix[y][x].hexa()

    def get_neighbors(self, cell: Cell) -> list:
        neighbors = []
        x, y = cell.x, cell.y
        if not cell.walls["north"] and y > 0:
            neighbors.append(self.matrix[y-1][x])
        if not cell.walls["east"] and x < self.width - 1:
            neighbors.append(self.matrix[y][x+1])
        if not cell.walls["south"] and y < self.height - 1:
            neighbors.append(self.matrix[y+1][x])
        if not cell.walls["west"] and x > 0:
            neighbors.append(self.matrix[y][x-1])
        return neighbors


    def maze_solver(self) -> list:
        start = self.matrix[self.ENTRY[1]][self.ENTRY[0]]
        end = self.matrix[self.EXIT[1]][self.EXIT[0]]
        start.spec = True
        end.spec = True
        path = [start]
        visited = {start}
        while path:
            current = path[-1]
            if current == end:
                for cell in path:
                    if cell not in (start, end):
                        cell.in_path = True
                return path
            neighbors = [
                case for case in self.get_neighbors(current)
                if case not in visited and not case.fixed
            ]
            if neighbors:
                next_cell = choice(neighbors)
                path.append(next_cell)
                visited.add(next_cell)
            else:
                path.pop()

    def get_direction(self, path) -> str:
        dirlist = []
        i = 0
        while i < len(path) - 1:
            cell_a = path[i]
            cell_b = path[i + 1]
            if cell_b.x == cell_a.x + 1:
                dirlist.append("E")
            elif cell_b.x == cell_a.x - 1:
                dirlist.append("W")
            elif cell_b.y == cell_a.y - 1:
                dirlist.append("N")
            elif cell_b.y == cell_a.y + 1:
                dirlist.append("S")
            i += 1
        final = "".join(dirlist)
        return final

    def get_hexa(self) -> str:
        result = []
        for y in range(self.height):
            for x in range(self.width):
                result.append(self.matrix[y][x].hex)
            result.append("\n")
        result.append("\n")
        final = "".join(result)
        return final

    def get_entry(self) -> str:
        return f"{self.ENTRY[0]}, {self.ENTRY[1]}\n"

    def get_exit(self) -> str:
        return f"{self.EXIT[0]}, {self.EXIT[1]}\n"

    def generate_txt(self, output: str) -> None:
        path = self.maze_solver()
        try:
            with open(output, "w") as file:

                hexa = self.get_hexa()
                file.write(hexa)
                entry = self.get_entry()
                file.write(entry)
                exi = self.get_exit()
                file.write(exi)
                direc = self.get_direction(path)
                file.write(direc)
        except Exception as e:
            print(e)
        return
