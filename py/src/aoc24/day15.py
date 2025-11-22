from typing import Literal, Self

Direction = Literal[">", "<", "^", "v"]
RobotInstructions = list[Direction]

WALL = "#"
BLOCK = "O"
ROBOT = "@"


class Grid:
    __inner: list[list[str]]

    def __init__(self, inner: list[list[str]]) -> None:
        self.__inner = inner

    @classmethod
    def from_str(cls, s: str) -> Self:
        grid = [[col for col in row] for row in s.splitlines()]

        return cls(grid)


def load_data_from_str(s: str) -> tuple[Grid, RobotInstructions]:
    parts = s.split("\n\n")
