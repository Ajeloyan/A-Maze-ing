from mazegen.generator import Grid
from mazegen.validator import parsing
import sys


def main() -> None:
    try:
        config = parsing(sys.argv[1])
    except Exception as e:
        print(e)
        sys.exit(1)
    grid = Grid(config)
    grid.dig_maze()
    grid.maze_solver()
    grid.draw_grid()
    grid.generate_txt(config.OUTPUT_FILE)


if __name__ == "__main__":
    main()
