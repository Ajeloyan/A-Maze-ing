from validator import parsing
from enum import Enum


class Tiles(Enum):
    TOP_WALL = "█▀▀▀▀"
    TOP_PATH = "█    "
    MID_WALL = "█    "
    MID_PATH = "     "
    V_LINE = "█"
    CORNER = "█"
    BOTTOM = "▀▀▀▀"
    CORNER_BOT = "▀"


class Cell:
    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y
        self.walls = {
            "north": True,
            "south": True,
            "east": True,
            "west": True
        }

    def __repr__(self):
        return f"{self.x}: {self.y}"


class Grid:
    def __init__(self) -> None:
        config = parsing("config.txt")
        self.width: int = config.WIDTH
        self.height: int = config.HEIGHT
        self.matrix: list[list[Cell]] = [[Cell(x, y) for x in range(self.width)]
                                         for y in range(self.height)]
        cell = self.matrix[4][8]
        cell.walls["north"] = False

    # def draw_grid(self) -> None:
    #     for y in range(self.height):
    #         for x in range(self.width - 1):
    #             if self.matrix[x][y].walls["north"] is True:
    #                 print(draw.top.value, end="")

    def draw_grid(self) -> None:
        for y in range(self.height):
            for x in range(self.width):
                cell = self.matrix[y][x]
                if cell.walls["north"]:
                    print(Tiles.TOP_WALL.value, end="")
                else:
                    print(Tiles.TOP_PATH.value, end="")
            print(Tiles.CORNER.value)

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


if __name__ == "__main__":
    grid = Grid()
    grid.draw_grid()
    cell_test = grid.matrix[4][8]
    cell_test = "h"
    print()