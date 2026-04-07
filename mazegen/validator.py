from pydantic import BaseModel, model_validator, Field, ValidationError
from typing import Self
import sys


def parsing(file: str) -> dict:
    config: dict = {}
    try:
        with open(file, "r") as file:
            for line in file:
                line = line.strip()
                if line.startswith("#"):
                    continue
                if "=" not in line:
                    continue
                key, value = line.split("=")
                config.update({key: value})
    except FileNotFoundError as e:
        print(f"error :{e}")
        sys.exit(1)

    x, y = config["ENTRY"].split(",")
    config.update({"ENTRY": (int(x), int(y))})
    x, y = config["EXIT"].split(",")
    config.update({"EXIT": (int(x), int(y))})

    return config


class MazeConfig(BaseModel):
    WIDTH: int = Field(ge=0, le=500)
    HEIGHT: int = Field(ge=0, le=500)
    ENTRY: tuple[int, int]
    EXIT: tuple[int, int]
    OUTPUT_FILE: str
    PERFECT: bool = Field(default=True)

    @model_validator(mode='after')
    def entry_validator(self) -> Self:
        if (self.ENTRY[0] < 0 or self.ENTRY[0] >= self.WIDTH
                or self.ENTRY[1] < 0 or self.ENTRY[1] >= self.HEIGHT):
            raise ValueError("Entry point must have values between 0 "
                             "and width or 0 and height")
        return self

    @model_validator(mode='after')
    def exit_validator(self) -> Self:
        if (self.EXIT[0] < 0 or self.EXIT[0] >= self.WIDTH
                or self.EXIT[1] < 0 or self.EXIT[1] >= self.HEIGHT):
            raise ValueError("Exit point must have values between 0 "
                             "and width or 0 and height")
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


if __name__ == "__main__":
    raw_data = parsing("config.txt")
    try:
        config_validated = MazeConfig(**raw_data)
        print("config created/validated")
        print((config_validated))
    except ValidationError as e:
        print(f"Error :\n{e}")
        sys.exit(1)
