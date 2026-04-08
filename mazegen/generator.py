from validator import parsing
from enum import Enum
from random import randint


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
        self.bin: list[int] = [0, 0, 0, 0]
        self.hex: str = ""
        self.fixed: bool = False
        
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
    def __init__(self) -> None:
        config = parsing("config.txt")
        self.width: int = config.WIDTH
        self.height: int = config.HEIGHT
        self.matrix: list[list[Cell]] = [[Cell(x, y) for x in range(self.width)]
                                         for y in range(self.height)]
        self.count_tot = self.width * self.height
        self.all_visited: bool = True if self.count_tot == 0 else False
        self.repeat: int = 10
        
        # mid_cell = self.mid_cellule()
        # x = mid_cell.x
        # y = mid_cell.y
        # cell = self.matrix[y - 1][x]
        # print(cell.bin)

    def draw_grid(self) -> None:
        if self.width >= 11 and self.height >= 10:
            self.forty_two()
        self.dig_maze()
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

    # def forty_two2(self) -> None:
    #     mid_cell: Cell = self.mid_cellule()
    #     x: int = mid_cell.x
    #     y: int = mid_cell.y
    #     for i in range(1, 4):
    #         self.matrix[y][x - i].fixed = True
    #         self.matrix[y][x - i].is_fixed()
    #         self.matrix[y + 1][x - i].walls["north"] = True
    #         self.matrix[y][x].walls["west"] = True

    def forty_two(self) -> None:
        mid_cell: Cell = self.mid_cellule()
        x: int = mid_cell.x
        y: int = mid_cell.y
        j: int = 1
        for j in range(1, 3):
            self.matrix[y][x - j].fixed = True,
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
        while self.count_tot > 0:
            y = randint(0, self.height - 1)
            x = randint(0, self.width - 1)

            work = grid.matrix[y][x]
            if work.is_visited is False:
                work.is_visited = True
                
                print(self.count_tot)
                if not x == self.width - 1:
                    work_b = grid.matrix[y][x+1]
                    if work.fixed is False and work_b.fixed is False:
                        grid.break_wall(work, work_b)
                else:
                    work_b = grid.matrix[y][x-1]
                    grid.break_wall(work, work_b)
                self.count_tot -= 1
            else:
                continue


if __name__ == "__main__":
    grid = Grid()
    for i in range(grid.width):
        if i < grid.width - 1:
            print(f"  {i}  ", end="")
        else:
            print(f"  {i}  ")
    mid_cell = grid.mid_cellule()
    x = mid_cell.x
    y = mid_cell.y
    cell = grid.matrix[y][x - 1]
    print()
    # grid.forty_two()
    grid.draw_grid()
    print()
