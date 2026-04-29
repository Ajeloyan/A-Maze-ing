from enum import Enum
from random import shuffle, choice, seed
from typing import Any, TYPE_CHECKING
if TYPE_CHECKING:
    from .validator import MazeConfig


class Colors(Enum):
    """Enumeration of supported terminal colors.

    Each member represents a named color preset used during maze
    rendering. ANSI escape codes are generated through :meth:`define`.

    Attributes:
        ORANGE: Orange foreground color.
        SALMON: Salmon foreground color.
        GREEN: Green foreground color.
        CYAN: Cyan foreground color.
        PURPLE: Purple foreground color.
        WHITE: Default terminal color.
        MULTI: Randomly selected color among predefined presets.
    """
    ORANGE = "ORANGE"
    SALMON = "SALMON"
    GREEN = "GREEN"
    CYAN = "CYAN"
    PURPLE = "PURPLE"
    WHITE = "WHITE"
    MULTI = "MULTI"

    def define(self) -> str:
        """Return the ANSI escape sequence for the selected color.

        If the color is ``MULTI``, one preset is randomly chosen each
        time the method is called.

        Returns:
            ANSI escape sequence usable in terminal output.
        """
        if self == Colors.MULTI:
            col = [
                "\033[38;2;255;160;81m",
                "\033[38;2;248;118;102m",
                "\033[38;2;99;184;155m",
                "\033[38;2;80;167;194m",
                "\033[38;2;131;103;166m",
            ]
            return choice(col)
        return {
            "ORANGE": "\033[38;2;255;160;81m",
            "SALMON": "\033[38;2;248;118;102m",
            "GREEN": "\033[38;2;99;184;155m",
            "CYAN": "\033[38;2;80;167;194m",
            "PURPLE": "\033[38;2;131;103;166m",
            "WHITE": "\033[0;m"
        }[self.value]


class Tiles(Enum):
    """Enumeration of glyph patterns used to render the maze in terminal.

    Each member stores a string segment used to draw walls, paths,
    intersections or fixed cells.
    """
    WALL_H = "▀▀▀▀▀▀"
    PATH_H = "      "
    MID_NO = " "
    JOINT_FULL = "█"
    JOINT_THIN = "▀"
    MID_WALL = "█"
    BOTTOM = "▀▀▀▀▀▀"
    CORNER_BOT = "▀"
    FIXED = "███████"
    PATH_TOP = " ████ "
    PATH_BOT = " ▀▀▀▀ "


class MazeGenerator:
    class Cell:
        """Represent a single cell of the maze grid.

        A cell stores its coordinates, surrounding walls, state flags and
        encoded representations used for export.

        Attributes:
            x: Horizontal coordinate in the grid.
            y: Vertical coordinate in the grid.
            walls: Presence of walls on each side.
            bin: Binary wall representation in NESW order.
            hex: Hexadecimal representation derived from ``bin``.
            fixed: Indicates that the cell is blocked and cannot be carved.
            id: Identifier used by Kruskal's algorithm.
            in_path: Indicates that the cell belongs to the solved path.
            spec: Marks special cells such as entry and exit.
        """
        def __init__(self, x: int, y: int) -> None:
            self.x: int = x
            self.y: int = y
            self.walls = {
                "north": True,
                "south": True,
                "east": True,
                "west": True
            }
            self.bin: list[int] = [0, 0, 0, 0]
            self.hex: str = ""
            self.fixed: bool = False
            self.id: int = 0
            self.in_path = False
            self.spec = False

        def __repr__(self) -> str:
            """Return a developer-friendly representation of the cell.

            Returns:
                Coordinates formatted as ``"x: y"``.
            """
            return f"{self.x}: {self.y}"

        def binary(self) -> None:
            """Compute the binary wall representation of the cell.

            The wall order is:

            * index 0: north
            * index 1: east
            * index 2: south
            * index 3: west
            """
            if self.walls["north"] is True:
                self.bin[3] = 1
            if self.walls["east"] is True:
                self.bin[2] = 1
            if self.walls["south"] is True:
                self.bin[1] = 1
            if self.walls["west"] is True:
                self.bin[0] = 1

        def hexa(self) -> None:
            """Convert the binary wall representation into hexadecimal.

            The result is stored in ``self.hex`` as a single hexadecimal
            character between ``0`` and ``F``.
            """
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
    """Represent the full maze grid and all related operations.

    The grid owns every cell and provides methods to generate, solve,
    display and export the maze.

    Args:
        config: Validated configuration object containing maze settings.

    Attributes:
        width: Number of columns.
        height: Number of rows.
        matrix: Two-dimensional list of ``Cell`` instances.
        ENTRY: Entry coordinates.
        EXIT: Exit coordinates.
        is_perfect: Whether the maze has a unique path.
        animation: Whether intermediate rendering is enabled.
    """
    def __init__(self, config: "MazeConfig | dict") -> None:
        """Initialize the maze grid from configuration."""

        if isinstance(config, dict):
            width: int = config["WIDTH"]
            height: int = config["HEIGHT"]
            entry: tuple[int, int] = config["ENTRY"]
            exit_: tuple[int, int] = config["EXIT"]
            is_perfect: bool = config.get("PERFECT", True)
            wall_color: Colors = config.get("WALL_COLOR", Colors.MULTI)
            path_color: Colors = config.get("PATH_COLOR", Colors.CYAN)
            spec_color: Colors = config.get("SPEC_COLOR", Colors.PURPLE)
            seed_value: int | None = config.get("SEED", None)
            output_file: str = config.get("OUTPUT_FILE", "maze.txt")

        else:
            width = config.WIDTH
            height = config.HEIGHT
            entry = config.ENTRY
            exit_ = config.EXIT
            is_perfect = config.PERFECT
            wall_color = config.WALL_COLOR
            path_color = config.PATH_COLOR
            spec_color = config.SPEC_COLOR
            seed_value = config.SEED
            output_file = config.OUTPUT_FILE

        self.width: int = width
        self.height: int = height

        self.matrix: list[list[MazeGenerator.Cell]] = [
            [MazeGenerator.Cell(x, y) for x in range(self.width)]
            for y in range(self.height)
        ]

        self.ENTRY: tuple[int, int] = entry
        self.EXIT: tuple[int, int] = exit_
        self.is_perfect: bool = is_perfect
        self.wall_color = wall_color
        self.path_color = path_color
        self.spec_color = spec_color
        self.visible_path: bool = False
        self.algo: str = "dfs"
        self.seed: int | None = seed_value
        if self.width >= 11 and self.height >= 10:
            self.forty_two()
        self.animation: bool = True
        self.output_file = output_file

    def coloration(self, cell: Cell, text: str) -> str:
        """Apply ANSI coloring to a rendered tile.

        Path cells, special cells and walls may use different colors.

        Args:
            cell: Cell associated with the tile.
            text: Raw tile text.

        Returns:
            Colored string ready for terminal output.
        """
        if cell.in_path and (text is Tiles.PATH_TOP.value or
                             text is Tiles.PATH_BOT.value):
            return f"{self.path_color.define()}{text}\033[0m"
        elif cell.spec and (text is Tiles.PATH_TOP.value or
                            text is Tiles.PATH_BOT.value):
            return f"{self.spec_color.define()}{text}\033[0m"
        else:
            return f"{self.wall_color.define()}{text}\033[0m"

    def draw_grid(self) -> None:
        """Render the complete maze in terminal.

        Raises:
            ValueError: If entry or exit is placed inside a fixed cell.
        """
        print("\033[H")
        if self.matrix[self.ENTRY[1]][self.ENTRY[0]].fixed:
            raise ValueError("Error: Entry must be"
                             " in a valid Cell (out of 42)")
        elif self.matrix[self.EXIT[1]][self.EXIT[0]].fixed:
            raise ValueError("Error: Exit must be in a valid Cell (out of 42)")
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

                    if (cell.in_path and self.visible_path is True) \
                       or cell.spec:
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
        """Return the central cell of the grid.

        Returns:
            Cell located at integer midpoint of the grid.
        """
        x = self.width // 2
        y = self.height // 2
        mid_cell: MazeGenerator.Cell = self.matrix[y][x]
        return mid_cell

    def forty_two(self) -> None:
        """Create a fixed obstacle pattern shaped as ``42``.

        This pattern is inserted near the center of sufficiently large
        grids.
        """
        mid_cell: MazeGenerator.Cell = self.mid_cellule()
        x: int = mid_cell.x
        y: int = mid_cell.y
        for j in range(1, 3):
            self.matrix[y][x - j].fixed = True
            self.matrix[y][x - j - 1].fixed = True
        for j in range(0, 2):
            self.matrix[y - j][x - 3].fixed = True
            self.matrix[y - j - 1][x - 3].fixed = True
        for j in range(1, 3):
            self.matrix[y + j][x - 1].fixed = True
            self.matrix[y + j - 1][x - 1].fixed = True
        for i in range(1, 3):
            self.matrix[y][x + i].fixed = True
            self.matrix[y][x + i + 1].fixed = True
        for i in range(1, 3):
            self.matrix[y - 2][x + i].fixed = True
            self.matrix[y - 2][x + i + 1].fixed = True
        for i in range(1, 3):
            self.matrix[y + 2][x + i].fixed = True
            self.matrix[y + 2][x + i + 1].fixed = True
        for i in range(0, 2):
            self.matrix[y - i][x + 3].fixed = True
            self.matrix[y - i - 1][x + 3].fixed = True
        for i in range(0, 2):
            self.matrix[y + i][x + 1].fixed = True
            self.matrix[y + i + 1][x + 1].fixed = True

    def break_wall(self, cell_a: Cell, cell_b: Cell) -> None:
        """Open the wall between two adjacent cells.

        Args:
            cell_a: First adjacent cell.
            cell_b: Second adjacent cell.
        """
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
        """Restore the wall between two adjacent cells.

        Args:
            cell_a: First adjacent cell.
            cell_b: Second adjacent cell.
        """
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

    def kruskal_generator(self) -> None:
        """Generate a maze using Kruskal's algorithm.

        Cells are progressively merged into connected sets while removing
        walls between disjoint regions.
        """
        i = 1
        walls: list = []
        seed(self.seed)
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
            if cell_a.id != cell_b.id:
                self.break_wall(cell_a, cell_b)
                check_id = cell_a.id
                for y in range(self.height):
                    for x in range(self.width):
                        if self.matrix[y][x].id == check_id:
                            self.matrix[y][x].id = cell_b.id
            if self.animation:
                self.draw_grid()
        if self.is_perfect is False:
            self.imperfect_maze()
        for y in range(self.height):
            for x in range(self.width):
                self.matrix[y][x].binary()
                self.matrix[y][x].hexa()

    def get_neighbors(self, cell: Cell) -> list:
        """Return accessible neighboring cells.

        Only neighbors connected by an open wall are returned.

        Args:
            cell: Source cell.

        Returns:
            List of reachable adjacent cells.
        """
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

    def get_neighbors_bis(self, cell: Cell) -> list:
        """Return blocked neighboring cells.

        Only neighbors separated by a wall are returned.

        Args:
            cell: Source cell.

        Returns:
            List of adjacent cells still separated by walls.
        """
        neighbors = []
        x, y = cell.x, cell.y
        if cell.walls["north"] and y > 0:
            neighbors.append(self.matrix[y-1][x])
        if cell.walls["east"] and x < self.width - 1:
            neighbors.append(self.matrix[y][x+1])
        if cell.walls["south"] and y < self.height - 1:
            neighbors.append(self.matrix[y+1][x])
        if cell.walls["west"] and x > 0:
            neighbors.append(self.matrix[y][x-1])
        return neighbors

    def maze_solver(self) -> list:
        """Solve the maze using breadth-first search.

        The shortest path between entry and exit is searched.

        Returns:
            Ordered list of cells from entry to exit.
        """
        from collections import deque
        start = self.matrix[self.ENTRY[1]][self.ENTRY[0]]
        end = self.matrix[self.EXIT[1]][self.EXIT[0]]
        start.spec = True
        end.spec = True

        queue = deque([start])
        visited: dict[MazeGenerator.Cell, Any] = {start: None}
        while queue:

            current = queue.popleft()
            if current == end:
                break

            neighbors = [
                case for case in self.get_neighbors(current)
                if case not in visited and not case.fixed
            ]
            for new in neighbors:
                next_cell = new
                visited[(next_cell)] = current
                queue.append(next_cell)
        current = end
        path = []
        while current:
            path.append(current)
            current = visited[current]

        for cell in path:
            if cell not in (start, end):
                cell.in_path = True
        return path[::-1]

    def dfs_generator(self) -> None:
        """Generate a maze using recursive backtracking logic.

        This iterative implementation uses a stack and random neighbor
        selection.
        """
        start = self.matrix[0][0]
        path: list[MazeGenerator.Cell] = [start]
        visited = {start}
        seed(self.seed)
        while path:
            current = path[-1]
            neighbors = [
                case for case in self.get_neighbors_bis(current)
                if case not in visited and not case.fixed
            ]
            if neighbors:
                next_cell = choice(neighbors)
                self.break_wall(current, next_cell)
                path.append(next_cell)
                visited.add(next_cell)
                if self.animation:
                    self.draw_grid()
            else:
                path.pop()
        if self.is_perfect is False:
            self.imperfect_maze()
        for y in range(self.height):
            for x in range(self.width):
                self.matrix[y][x].binary()
                self.matrix[y][x].hexa()

    def imperfect_maze(self) -> None:
        """Introduce additional openings to create loops.

        This method removes selected walls after generation to produce a
        non-perfect maze with multiple possible paths.
        """
        i: int = 0
        cell_broken: list[MazeGenerator.Cell] = []
        for y in range(self.height - 1):
            for x in range(self.width - 1):
                current_cell = self.matrix[y][x]
                next_cell = self.matrix[y + 1][x]
                if i % 7 == 0:
                    if current_cell.fixed is False and next_cell.fixed is \
                       False and self.cell_around(y, x, cell_broken) is False:
                        self.break_wall(current_cell, next_cell)
                        cell_broken.append(current_cell)
                        cell_broken.append(next_cell)
                i += 1

    def cell_around(self, y: int, x: int, list_cell: list[Cell]) -> bool:
        """Check whether surrounding cells are absent from a reference list.

        Args:
            y: Row index of inspected cell.
            x: Column index of inspected cell.
            list_cell: Cells already modified.

        Returns:
            ``True`` if surrounding cells are free of conflicts,
            otherwise ``False``.
        """
        if self.matrix[y - 1][x] in list_cell\
           or self.matrix[y - 1][x - 1] in list_cell \
           or self.matrix[y][x - 1] in list_cell \
           or self.matrix[y + 1][x - 1] in list_cell \
           or self.matrix[y + 1][x] in list_cell \
           or self.matrix[y + 1][x + 1] in list_cell \
           or self.matrix[y][x + 1]:
            return False
        return True

    def get_direction(self, path: list[Cell]) -> str:
        """Convert a solved path into compass directions.

        Directions use the letters ``N``, ``E``, ``S`` and ``W``.

        Args:
            path: Ordered path of cells.

        Returns:
            Concatenated direction string.
        """
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
        """Serialize the grid into hexadecimal wall codes.

        Returns:
            Multiline string containing one hexadecimal code per cell.
        """
        result = []
        for y in range(self.height):
            for x in range(self.width):
                result.append(self.matrix[y][x].hex)
            result.append("\n")
        result.append("\n")
        final = "".join(result)
        return final

    def get_entry(self) -> str:
        """Return the formatted entry coordinates.

        Returns:
            Entry coordinates followed by a newline.
        """
        return f"{self.ENTRY[0]}, {self.ENTRY[1]}\n"

    def get_exit(self) -> str:
        """Return the formatted exit coordinates.

        Returns:
            Exit coordinates followed by a newline.
        """
        return f"{self.EXIT[0]}, {self.EXIT[1]}\n"

    def generate_txt(self) -> None:
        """Export the maze and its solution to a text file.

        The file contains hexadecimal encoding, entry and exit positions,
        then the direction string of the solved path.

        Args:
            output: Destination file path.
        """
        path = self.maze_solver()
        try:
            with open(self.output_file, "w") as file:

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

    def reset_grid(self) -> None:
        """Restore the grid to its initial closed state.

        All walls are rebuilt and path markers are cleared.
        """
        for y in range(self.height):
            for x in range(self.width):
                cell = self.matrix[y][x]
                cell.walls = {"north": True, "south": True,
                              "east": True, "west": True}
                cell.in_path = False
                cell.spec = False

    def dfs_generation(self) -> None:
        self.dfs_generator()
        self.maze_solver()
        self.generate_txt()

    def kruskal_generation(self) -> None:
        self.kruskal_generator()
        self.maze_solver()
        self.generate_txt()
