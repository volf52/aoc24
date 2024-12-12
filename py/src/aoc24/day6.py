from collections.abc import Callable, Sequence
from dataclasses import dataclass
from typing import Literal, Self

from aoc24 import utils

Pos = tuple[int, int]
NewPosFunc = Callable[[Pos], Pos]
TOrientation = Literal[">", "<", "^", "v"]
Grid = list[list[str]]


OBSTACLE = "#"
FILL_CHAR = "X"
EMPTY_CHAR = "."

NEW_POS_FUNCS: dict[TOrientation, NewPosFunc] = {
    ">": lambda p: (p[0], p[1] + 1),
    "<": lambda p: (p[0], p[1] - 1),
    "^": lambda p: (p[0] - 1, p[1]),
    "v": lambda p: (p[0] + 1, p[1]),
}
AFTER_TURN: dict[TOrientation, TOrientation] = {">": "v", "v": "<", "<": "^", "^": ">"}


@dataclass
class Orientation:
    _val: TOrientation

    def __init__(self, val: str) -> None:
        if val not in NEW_POS_FUNCS:
            raise ValueError("Invalid guard pos " + val)
        self._val = val

    def get_new_pos(self, old_pos: Pos) -> Pos:
        new_pos_f = NEW_POS_FUNCS[self._val]
        return new_pos_f(old_pos)

    def turn(self):
        self._val = AFTER_TURN[self._val]


@dataclass
class Map:
    grid: Grid
    _traversed: bool

    @classmethod
    def from_lines(cls, lines: Sequence[str]) -> Self:
        grid: Grid = [list(x) for x in lines]
        return cls(grid=grid, _traversed=False)

    @classmethod
    def load(cls) -> Self:
        lines = utils.read_lines(6)
        return cls.from_lines(lines)

    def show_grid(self):
        for line in self.grid:
            print(line)

    def __is_valid_pos(self, pos: Pos) -> bool:
        n_rows = len(self.grid)
        n_cols = len(self.grid[0])
        x, y = pos

        return x in range(n_rows) and y in range(n_cols)

    def is_obstacle(self, pos: Pos) -> bool:
        return self.grid[pos[0]][pos[1]] == OBSTACLE

    def mark_traversed(self, pos: Pos):
        x, y = pos
        self.grid[x][y] = FILL_CHAR

    def traverse(self):
        if self._traversed:
            return

        # Find initial guard position
        guard_pos = (-1, -1)
        orientation: Orientation | None = None
        for i, line in enumerate(self.grid):
            for j, block in enumerate(line):
                if block in NEW_POS_FUNCS:
                    guard_pos = (i, j)
                    orientation = Orientation(block)
                    break
            if orientation is not None:
                break

        if orientation is None:
            msg = "No guard char in map"
            raise ValueError(msg)

        # Patrol across the map
        while True:
            self.mark_traversed(guard_pos)
            next_pos = orientation.get_new_pos(guard_pos)
            if not self.__is_valid_pos(next_pos):
                break
            if self.is_obstacle(next_pos):
                orientation.turn()

            guard_pos = orientation.get_new_pos(guard_pos)

        self._traversed = True

    def count_x(self):
        return sum(row.count(FILL_CHAR) for row in self.grid)


def part1():
    mp = Map.load()
    mp.traverse()

    res = mp.count_x()
    print(f"Day 6 part 1: {res}")


def part2():
    pass


if __name__ == "__main__":
    lines = """....#.....
.........#
..........
..#.......
.......#..
..........
.#..^.....
........#.
#.........
......#...""".splitlines()
    mp = Map.from_lines(lines)
    mp.show_grid()
    mp.traverse()
    mp.show_grid()
