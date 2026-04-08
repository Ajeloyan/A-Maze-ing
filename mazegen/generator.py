from validator import parsing
from enum import Enum


class Tiles(Enum):
    WALL_H = "▀▀▀▀"
    PATH_H = "    "
    MID_WALL = "█    "
    MID_PATH = "     "
    JOINT_FULL = "█"
    JOINT_THIN = "▀"
    V_LINE = "█"
    BOTTOM = "▀▀▀▀"
    CORNER_BOT = "▀"




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

    def __repr__(self):
        return f"{self.x}: {self.y}"


class Grid:
    def __init__(self) -> None:
        config = parsing("config.txt")
        self.width: int = config.WIDTH
        self.height: int = config.HEIGHT
        self.matrix: list[list[Cell]] = [[Cell(x, y) for x in range(self.width)]
                                         for y in range(self.height)]

    def draw_grid(self) -> None:
        self.forty_two()
        for y in range(self.height):
            for x in range(self.width):
                cell = self.matrix[y][x]
                
                if cell.walls["west"]:
                    print(Tiles.JOINT_FULL.value, end="")
                else:
                    print(Tiles.JOINT_THIN.value, end="")
                
                if cell.walls["north"]:
                    print(Tiles.WALL_H.value, end="")
                else:
                    print(Tiles.PATH_H.value, end="")
            
            print(Tiles.V_LINE.value) 

            for _ in range(2):
                for x in range(self.width):
                    cell = self.matrix[y][x]
                    if cell.walls["west"]:
                        print(Tiles.MID_WALL.value, end="")
                    else:
                        print(Tiles.MID_PATH.value, end="")
                print(Tiles.V_LINE.value)

        for x in range(self.width):
            print(Tiles.CORNER_BOT.value + Tiles.BOTTOM.value, end="")
        print(Tiles.CORNER_BOT.value)

    def mid_cellule(self) -> Cell:
        x = self.width // 2
        y = self.height // 2
        mid_cell: Cell = self.matrix[y][x]
        return mid_cell

    def forty_two(self) -> Cell:
        mid_cell: Cell = self.mid_cellule()
        x: int = mid_cell.x
        y: int = mid_cell.y
        j: int = 1
        for j in range(1, 3):
            self.break_wall(self.matrix[y][x - j], self.matrix[y][x - j - 1])
        j = 0
        for j in range(0, 2):
            self.break_wall(self.matrix[y - j][x - 3], self.matrix[y - j - 1][x - 3])
        j = 0
        for j in range(1, 3):
            self.break_wall(self.matrix[y + j][x - 1], self.matrix[y + j - 1][x - 1])
        i: int = 1
        for i in range(1, 3):
            self.break_wall(self.matrix[y][x + i], self.matrix[y][x + i + 1])
        i = 1
        for i in range(1, 3):
            self.break_wall(self.matrix[y - 2][x + i], self.matrix[y - 2][x + i + 1])
        i = 1
        for i in range(1, 3):
            self.break_wall(self.matrix[y + 2][x + i], self.matrix[y + 2][x + i + 1])
        i = 1
        for i in range(0, 2):
            self.break_wall(self.matrix[y - i][x + 3], self.matrix[y - i - 1][x + 3])
        i = 1
        for i in range(0, 2):
            self.break_wall(self.matrix[y + i][x + 1], self.matrix[y + i + 1][x + 1])

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


if __name__ == "__main__":
    grid = Grid()
    for i in range(grid.width):
        if i < grid.width - 1:
            print(f"  {i}  ", end="")
        else:
            print(f"  {i}  ")
    grid.draw_grid()
    print()
