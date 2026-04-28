"""Validation and configuration utilities for maze generation.

This module defines:

* ``Colors``: terminal color presets using ANSI escape sequences.
* ``MazeConfig``: validated configuration schema powered by Pydantic.
* ``parsing``: helper function that reads a configuration file and
  returns a validated ``MazeConfig`` instance.

The configuration file is expected to contain ``KEY=VALUE`` pairs, with
optional commented lines beginning with ``#``.
"""
from pydantic import BaseModel, model_validator, Field, ValidationError
from typing import Self, Optional
import sys
from enum import Enum
from random import choice


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


class MazeConfig(BaseModel):
    """Validated configuration model for maze generation.

    This model centralizes all user-defined parameters required to build,
    display and export a maze.

    Attributes:
        WIDTH: Maze width in cells.
        HEIGHT: Maze height in cells.
        ENTRY: Coordinates of the maze entry point.
        EXIT: Coordinates of the maze exit point.
        OUTPUT_FILE: Destination text file path.
        PERFECT: Whether the maze must contain a unique solution path.
        WALL_COLOR: Color used for walls.
        PATH_COLOR: Color used for solved path.
        SPEC_COLOR: Color used for special cells.
        SEED: Optional random seed for reproducibility.
    """
    WIDTH: int = Field(ge=4, le=500)
    HEIGHT: int = Field(ge=4, le=500)
    ENTRY: tuple[int, int]
    EXIT: tuple[int, int]
    OUTPUT_FILE: str
    PERFECT: bool = Field(default=True)
    WALL_COLOR: Colors = Field(default=Colors.MULTI)
    PATH_COLOR: Colors = Field(default=Colors.CYAN)
    SPEC_COLOR: Colors = Field(default=Colors.PURPLE)
    SEED: Optional[int] = Field(default=None)

    @model_validator(mode='after')
    def entry_validator(self) -> Self:
        """Validate that the entry point lies inside the grid.

        Returns:
            Current validated instance.

        Raises:
            ValueError: If entry coordinates are outside maze bounds.
        """
        if (self.ENTRY[0] < 0 or self.ENTRY[0] > self.WIDTH - 1
                or self.ENTRY[1] < 0 or self.ENTRY[1] > self.HEIGHT - 1):
            raise ValueError("Entry point must have values between 0 "
                             "and width-1 or 0 and height-1")
        return self

    @model_validator(mode='after')
    def exit_validator(self) -> Self:
        """Validate that the exit point lies inside the grid.

        Returns:
            Current validated instance.

        Raises:
            ValueError: If exit coordinates are outside maze bounds.
        """
        if (self.EXIT[0] < 0 or self.EXIT[0] > self.WIDTH - 1
                or self.EXIT[1] < 0 or self.EXIT[1] > self.HEIGHT - 1):
            raise ValueError("Exit point must have values between 0 "
                             "and width-1 or 0 and height-1")
        return self

    @model_validator(mode='after')
    def check_dif(self) -> Self:
        """Ensure that entry and exit positions are distinct.

        Returns:
            Current validated instance.

        Raises:
            ValueError: If entry and exit are identical.
        """
        if self.ENTRY == self.EXIT:
            raise ValueError("Exit and Entry must be different")
        return self

    @model_validator(mode='after')
    def check_output_file(self) -> Self:
        """Validate the output file extension.

        Only plain text files using the ``.txt`` extension are accepted.

        Returns:
            Current validated instance.

        Raises:
            ValueError: If the output file extension is invalid.
        """
        if not self.OUTPUT_FILE.endswith(".txt"):
            raise ValueError("Output file must be a .txt file")
        return self

    @model_validator(mode='after')
    def check_colors(self) -> Self:
        """Ensure that all configured colors are different.

        Distinct colors improve readability of walls, paths and special
        cells.

        Returns:
            Current validated instance.

        Raises:
            ValueError: If two or more configured colors are identical.
        """
        if self.WALL_COLOR == self.PATH_COLOR or self.WALL_COLOR == \
           self.SPEC_COLOR or self.PATH_COLOR == self.SPEC_COLOR:
            raise ValueError("Colors must be different")
        return self


def parsing(file: str) -> MazeConfig:
    """Parse a configuration file and build a validated maze config.

    The file must contain ``KEY=VALUE`` entries. Empty or commented lines
    beginning with ``#`` are ignored.

    Expected tuple fields:

    * ``ENTRY=x,y``
    * ``EXIT=x,y``

    Args:
        file: Path to the configuration file.

    Returns:
        Fully validated ``MazeConfig`` instance.

    Raises:
        SystemExit: If the file cannot be read or configuration is
            invalid.
    """
    config: dict = {}

    try:
        with open(file, "r") as f:
            for line in f:
                line = line.strip()
                if line.startswith("#"):
                    continue
                if "=" not in line:
                    continue
                key, value = line.split("=")
                config.update({key: value})
    except (FileNotFoundError, PermissionError) as e:
        print(f"Error: {e}")
        sys.exit(1)

    try:
        x_in, y_in = config["ENTRY"].split(",")
        config["ENTRY"] = (int(x_in), int(y_in))

        x_out, y_out = config["EXIT"].split(",")
        config["EXIT"] = (int(x_out), int(y_out))

        return MazeConfig(**config)

    except ValidationError as e:
        print(e.errors()[0]["msg"].split(",")[1].strip())
        sys.exit(1)
    except Exception as e:
        print(f"Parsing error:{e}")
        sys.exit(1)
