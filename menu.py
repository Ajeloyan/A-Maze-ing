from enum import Enum
from mazegen.generator import Grid


class colors(Enum):
    BLUE = "\033[38;2;0;180;255m"
    CYAN = "\033[38;2;200;255;255m"
    RESET = "\033[0m"
    BOLD = "\033[1m"


class Menu:
    def __init__(self) -> None:
        pass

    def clear_screen(self) -> None:
        print("\033[2J\033[H\033[3J", end="", flush=True)

    def run_menu(self, grid: Grid, config) -> None:
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
                  f"2.{colors.RESET.value} Show/Unshow path    "
                  f"{colors.CYAN.value}║")
            print(f"    ║{colors.RESET.value}  {colors.BOLD.value}"
                  f"3.{colors.RESET.value} autre               "
                  f"{colors.CYAN.value}║")
            print(f"    ║{colors.RESET.value}  {colors.BOLD.value}"
                  f"q.{colors.RESET.value} Quit                "
                  f"{colors.CYAN.value}║")
            print(f"    ╚═════════════════════════╝{colors.RESET.value}")
            break
