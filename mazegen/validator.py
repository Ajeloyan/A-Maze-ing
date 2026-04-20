from pydantic import BaseModel, model_validator, Field
from typing import Self, Optional
import sys
from enum import Enum
from random import choice


class Colors(Enum):
    ORANGE = "ORANGE"
    SALMON = "SALMON"
    GREEN = "GREEN"
    CYAN = "CYAN"
    PURPLE = "PURPLE"
    WHITE = "WHITE"
    MULTI = "MULTI"

    def define(self):
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
    WIDTH: int = Field(ge=4, le=500)
    HEIGHT: int = Field(ge=4, le=500)
    ENTRY: tuple[int, int]
    EXIT: tuple[int, int]
    OUTPUT_FILE: str
    PERFECT: bool = Field(default=True)
    WALL_COLOR: Colors
    PATH_COLOR: Colors
    SPEC_COLOR: Colors
    SEED: Optional[int] = Field(default=None)

    @model_validator(mode='after')
    def entry_validator(self) -> Self:
        if (self.ENTRY[0] < 0 or self.ENTRY[0] > self.WIDTH - 1
                or self.ENTRY[1] < 0 or self.ENTRY[1] > self.HEIGHT - 1):
            raise ValueError("Entry point must have values between 0 "
                             "and width-1 or 0 and height-1")
        return self

    @model_validator(mode='after')
    def exit_validator(self) -> Self:
        if (self.EXIT[0] < 0 or self.EXIT[0] > self.WIDTH - 1
                or self.EXIT[1] < 0 or self.EXIT[1] > self.HEIGHT - 1):
            raise ValueError("Exit point must have values between 0 "
                             "and width-1 or 0 and height-1")
        return self

    @model_validator(mode='after')
    def check_dif(self) -> Self:
        if self.ENTRY == self.EXIT:
            raise ValueError("Exit and Entry must be different")
        return self

    @model_validator(mode='after')
    def check_output_file(self) -> Self:
        if not self.OUTPUT_FILE.endswith(".txt"):
            raise ValueError("Output file must be a .txt file")
        return self

    @model_validator(mode='after')
    def check_colors(self) -> Self:
        if self.WALL_COLOR == self.PATH_COLOR or self.WALL_COLOR == \
           self.SPEC_COLOR or self.PATH_COLOR == self.SPEC_COLOR:
            raise ValueError("Colors must be different")
        return self


def parsing(file: str) -> MazeConfig:
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

    except (KeyError, ValueError) as e:
        print(f"Parsing error:{e.errors()[0]["loc"]} {e.errors()[0]["msg"]}")
        sys.exit(1)
