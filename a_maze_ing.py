from mazegen.generator import Grid
from mazegen.validator import parsing
import sys
from menu import Menu


def main() -> None:
    try:
        config = parsing(sys.argv[1])
    except Exception as e:
        print(e)
        sys.exit(1)
    grid = Grid(config)
    menu = Menu()
    grid.dig_maze()
    grid.maze_solver()
    grid.draw_grid()
    menu.run_menu(grid, config)
    grid.generate_txt(config.OUTPUT_FILE)


if __name__ == "__main__":
    main()
