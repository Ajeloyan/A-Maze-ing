from enum import Enum
from mazegen.generator import Grid
import sys
import time
from mazegen.validator import Colors, MazeConfig


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
            print(f"{colors.CYAN.value}    ╔═════════════════════════╗")
            print(f"    ║{colors.RESET.value}  {colors.BOLD.value}"
                  f"1.{colors.RESET.value} Generate new maze   "
                  f"{colors.CYAN.value}║")
            print(f"    ║{colors.RESET.value}  {colors.BOLD.value}"
                  f"2.{colors.RESET.value} Show path           "
                  f"{colors.CYAN.value}║")
            print(f"    ║{colors.RESET.value}  {colors.BOLD.value}"
                  f"3.{colors.RESET.value} Hide path           "
                  f"{colors.CYAN.value}║")
            print(f"    ║{colors.RESET.value}  {colors.BOLD.value}"
                  f"4.{colors.RESET.value} change color        "
                  f"{colors.CYAN.value}║")
            print(f"    ║{colors.RESET.value}  {colors.BOLD.value}"
                  f"q.{colors.RESET.value} Quit                "
                  f"{colors.CYAN.value}║")
            print(f"    ╚═════════════════════════╝{colors.RESET.value}")

            try:
                user_choice: str = input("Please, enter a choice: ")
                if user_choice == "1":
                    grid.reset_grid()
                    grid.dig_maze()
                    grid.maze_solver()
                    self.run_menu(grid)
                elif user_choice == "2":
                    grid.visible_path = True
                    grid.draw_grid()
                    self.run_menu(grid)
                elif user_choice == "3":
                    grid.visible_path = False
                    grid.draw_grid()
                    self.run_menu(grid)
                elif user_choice == "4":
                    self.colors_menu(grid)
                    self.run_menu()
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
