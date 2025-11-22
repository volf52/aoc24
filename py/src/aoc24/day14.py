from dataclasses import dataclass
from functools import reduce
from typing import Self

from aoc24 import utils
from aoc24.utils import Pair

MAX_X = 101
MAX_Y = 103
MID_X = MAX_X // 2
MID_Y = MAX_Y // 2


@dataclass()
class Robot:
    pos: Pair
    vel: Pair

    @classmethod
    def from_line(cls, line: str) -> Self:
        a, b = line.split(" ")
        pos = Pair.from_line(a)
        vel = Pair.from_line(b)

        return cls(pos, vel)

    def step(self, max_x: int, max_y: int) -> None:
        new_x = self.pos.x + self.vel.x
        new_x %= max_x

        new_y = self.pos.y + self.vel.y
        new_y %= max_y

        self.pos = Pair(new_x, new_y)

    def n_steps(self, n: int, max_x: int, max_y: int) -> None:
        new_x = self.pos.x + n * self.vel.x
        new_x %= max_x

        new_y = self.pos.y + n * self.vel.y
        new_y %= max_y

        self.pos = Pair(new_x, new_y)


def part1():
    lines = utils.read_lines(14)
    robots = [Robot.from_line(line.strip()) for line in lines]

    for r in robots:
        r.n_steps(100, MAX_X, MAX_Y)

    q_sum = [0] * 4
    x_range_0 = range(MID_X)
    x_range_1 = range(MID_X + 1, MAX_X)

    y_range_0 = range(MID_Y)
    y_range_1 = range(MID_Y + 1, MAX_Y)

    quadrants = [
        (x_range_0, y_range_0),
        (x_range_1, y_range_0),
        (x_range_0, y_range_1),
        (x_range_1, y_range_1),
    ]

    for r in robots:
        for i, (quad_x, quad_y) in enumerate(quadrants):
            if r.pos.x in quad_x and r.pos.y in quad_y:
                q_sum[i] += 1

    res = reduce(lambda x, y: x * y, q_sum)

    print(f"Day 14 part 1: {res}")


def part2():
    lines = utils.read_lines(14)
    robots = [Robot.from_line(line.strip()) for line in lines]

    ii = -1
    for i in range(10_000):
        for r in robots:
            r.step(MAX_X, MAX_Y)

        poses = set(r.pos for r in robots)

        if len(poses) == len(robots):
            ii = i
            break

    print(f"Day 14 part 2: {ii+1}")
