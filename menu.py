from enum import Enum
from mazegen.generator import Grid
import sys
import time
from mazegen.validator import Colors
from mazegen.validator import parsing


class colors(Enum):
    BLUE = "\033[38;2;0;180;255m"
    CYAN = "\033[38;2;200;255;255m"
    RESET = "\033[0m"
    BOLD = "\033[1m"


class Menu():
    def __init__(self) -> None:
        pass

    def clear_screen(self) -> None:
        print("\033[2J\033[H\033[3J", end="", flush=True)

    def colors_menu(self, grid: Grid) -> None:
        while True:
            self.clear_screen()
            grid.draw_grid()
            print(f"{colors.BLUE.value}{colors.BOLD.value}")
            print(" ██████╗  ██████╗ ██╗      ██████╗ ██████╗ ███████╗")
            print("██╔════╝ ██╔═══██╗██║     ██╔═══██╗██╔══██╗██╔════╝")
            print("██║      ██║   ██║██║     ██║   ██║██████╔╝███████╗")
            print("██║      ██║   ██║██║     ██║   ██║██╔══██╗╚════██║")
            print("╚██████╗ ╚██████╔╝███████╗╚██████╔╝██║  ██║███████║")
            print(" ╚═════╝  ╚═════╝ ╚══════╝ ╚═════╝ ╚═╝  ╚═╝╚══════╝")
            print(f"{colors.RESET.value}")
            print(f"{colors.RESET.value}")
            print(f"{colors.CYAN.value}    ╔══════════════╗")
            print(f"    ║{colors.RESET.value}  {colors.BOLD.value}"
                  f"1.{colors.RESET.value} ORANGE   "
                  f"{colors.CYAN.value}║")
            print(f"    ║{colors.RESET.value}  {colors.BOLD.value}"
                  f"2.{colors.RESET.value} SALMON   "
                  f"{colors.CYAN.value}║")
            print(f"    ║{colors.RESET.value}  {colors.BOLD.value}"
                  f"3.{colors.RESET.value} GREEN    "
                  f"{colors.CYAN.value}║")
            print(f"    ║{colors.RESET.value}  {colors.BOLD.value}"
                  f"4.{colors.RESET.value} CYAN     "
                  f"{colors.CYAN.value}║")
            print(f"    ║{colors.RESET.value}  {colors.BOLD.value}"
                  f"5.{colors.RESET.value} PURPLE   "
                  f"{colors.CYAN.value}║")
            print(f"    ║{colors.RESET.value}  {colors.BOLD.value}"
                  f"6.{colors.RESET.value} WHITE    "
                  f"{colors.CYAN.value}║")
            print(f"    ║{colors.RESET.value}  {colors.BOLD.value}"
                  f"7.{colors.RESET.value} MULTI    "
                  f"{colors.CYAN.value}║")
            print(f"    ║{colors.RESET.value}  {colors.BOLD.value}"
                  f"q.{colors.RESET.value} Go back  "
                  f"{colors.CYAN.value}║")
            print(f"    ╚══════════════╝{colors.RESET.value}")

            try:
                user_choice: str = input("Please, enter a choice: ")
                if user_choice == "1":
                    grid.wall_color = Colors.ORANGE
                    self.run_menu(grid)
                elif user_choice == "2":
                    grid.wall_color = Colors.SALMON
                    self.run_menu(grid)
                elif user_choice == "3":
                    grid.wall_color = Colors.GREEN
                    self.run_menu(grid)
                elif user_choice == "4":
                    grid.wall_color = Colors.CYAN
                    self.run_menu(grid)
                elif user_choice == "5":
                    grid.wall_color = Colors.PURPLE
                    self.run_menu(grid)
                elif user_choice == "6":
                    grid.wall_color = Colors.WHITE
                    self.run_menu(grid)
                elif user_choice == "7":
                    grid.wall_color = Colors.MULTI
                    self.run_menu(grid)
                elif user_choice == "q":
                    self.run_menu(grid)

                else:
                    print("A number between 1 and 7 (or 'q') is needed")
                    print("3 sec before retry...")
                    time.sleep(3)
                    self.run_menu(grid)

            except Exception as e:
                print(e)
                sys.exit(1)

    def run_menu(self, grid: Grid) -> None:
        try:
            config = parsing(sys.argv[1])
        except Exception as e:
            print(e)
            sys.exit(1)
        while True:
            self.clear_screen()
            grid.draw_grid()
            print(f"{colors.BLUE.value}{colors.BOLD.value}")
            print("  █████╗           ███╗   ███╗ █████╗ ███████╗███████╗"
                  "          ██╗███╗   ██╗ ██████╗ ")
            print(" ██╔══██╗          ████╗ ████║██╔══██╗╚══███╔╝██╔════╝"
                  "          ██║████╗  ██║██╔════╝ ")
            print(" ███████║  ██████╗ ██╔████╔██║███████║  ███╔╝ █████╗   "
                  "██████╗  ██║██╔██╗ ██║██║  ███╗")
            print(" ██╔══██║  ╚═════╝ ██║╚██╔╝██║██╔══██║ ███╔╝  ██╔══╝   "
                  "╚═════╝  ██║██║╚██╗██║██║   ██║")
            print(" ██║  ██║          ██║ ╚═╝ ██║██║  ██║███████╗███████╗ "
                  "         ██║██║ ╚████║╚██████╔╝")
            print(" ╚═╝  ╚═╝          ╚═╝     ╚═╝╚═╝  ╚═╝╚══════╝╚══════╝ "
                  "         ╚═╝╚═╝  ╚═══╝ ╚═════╝ ")
            print(f"{colors.RESET.value}")
            print(f"{colors.RESET.value}")
            print(f"{colors.CYAN.value}    ╔═══════════════════════"
                  f"══════════════════════════════╗")
            print(f"    ║{colors.RESET.value}  {colors.BOLD.value}"
                  f"1.{colors.RESET.value} Generate new maze       "
                  f"                        "
                  f"{colors.CYAN.value}║")
            if grid.visible_path:
                actual_path = "Show"
                space = "  "
            else:
                actual_path = "Unshow"
                space = ""
            print(f"    ║{colors.RESET.value}  {colors.BOLD.value}"
                  f"2.{colors.RESET.value} Show/hide path         "
                  f"        {space}(actualy: {actual_path})"
                  f"{colors.CYAN.value}║")
            if grid.algo == "dfs":
                space = "    "
            elif grid.algo == "kruskal":
                space = ""
            print(f"    ║{colors.RESET.value}  {colors.BOLD.value}"
                  f"3.{colors.RESET.value} Change algo             "
                  f"      {space}(actualy: {grid.algo})"
                  f"{colors.CYAN.value}║")
            print(f"    ║{colors.RESET.value}  {colors.BOLD.value}"
                  f"4.{colors.RESET.value} Change color          "
                  f"                          "
                  f"{colors.CYAN.value}║")
            if grid.animation:
                actual_anim = "Show"
                space = "  "
            else:
                actual_anim = "Unshow"
                space = ""
            print(f"    ║{colors.RESET.value}  {colors.BOLD.value}"
                  f"5.{colors.RESET.value} Show/Unshow animation   "
                  f"       {space}(actualy: {actual_anim})"
                  f"{colors.CYAN.value}║")
            if grid.is_perfect:
                actual_perfect = "Perfect"
                space = "  "
            else:
                actual_perfect = "Imperfect"
                space = ""
            print(f"    ║{colors.RESET.value}  {colors.BOLD.value}"
                  f"6.{colors.RESET.value} Perfect/Imperfect           "
                  f"{space}(actualy: {actual_perfect})"
                  f"{colors.CYAN.value}║")
            print(f"    ║{colors.RESET.value}  {colors.BOLD.value}"
                  f"q.{colors.RESET.value} Quit                  "
                  f"                          "
                  f"{colors.CYAN.value}║")
            print(f"    ╚════════════════════════════════════════════"
                  f"═════════╝{colors.RESET.value}")

            try:
                user_choice: str = input("Please, enter a choice: ")
                if user_choice == "1":
                    if grid.algo == "dfs":
                        grid.reset_grid()
                        grid.dfs_generator()
                        grid.maze_solver()
                        grid.generate_txt(config.OUTPUT_FILE)
                        self.run_menu(grid)
                    elif grid.algo == "kruskal":
                        grid.reset_grid()
                        grid.kruskal_generator()
                        grid.maze_solver()
                        grid.generate_txt(config.OUTPUT_FILE)
                        self.run_menu(grid)
                elif user_choice == "2":
                    if grid.visible_path is False:
                        grid.visible_path = True
                        grid.draw_grid()
                        self.run_menu(grid)
                    elif grid.visible_path:
                        grid.visible_path = False
                        grid.draw_grid()
                        self.run_menu(grid)

                elif user_choice == "3":
                    if grid.algo == "dfs":
                        grid.algo = "kruskal"
                        self.run_menu(grid)
                    elif grid.algo == "kruskal":
                        grid.algo = "dfs"
                        self.run_menu(grid)
                elif user_choice == "4":
                    self.colors_menu(grid)
                    self.run_menu()
                elif user_choice == "5":
                    if grid.animation:
                        grid.animation = False
                    else:
                        grid.animation = True
                    self.run_menu(grid)
                elif user_choice == "6":
                    if grid.is_perfect:
                        grid.is_perfect = False
                    else:
                        grid.is_perfect = True
                    self.run_menu(grid)
                elif user_choice == "q":
                    print("Goodbye")
                    break
                else:
                    print("A number between 1 and 4 is needed")
                    print("3 sec before retry...")
                    time.sleep(3)
                    self.run_menu(grid)

            except Exception as e:
                print(e)
                sys.exit(1)
        sys.exit(1)
