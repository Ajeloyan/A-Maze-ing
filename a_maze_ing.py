from mazegen.generator import MazeGenerator
from mazegen.validator import parsing
import sys
from menu import Menu


def main() -> None:
    try:
        config = parsing(sys.argv[1])
        maze = MazeGenerator(config)
        menu = Menu()
        maze.dfs_generation()
        maze.draw_grid()
        menu.run_menu(maze)
    except Exception as e:
        print(e)
        sys.exit(1)


if __name__ == "__main__":
    main()
