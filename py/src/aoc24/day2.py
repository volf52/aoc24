import itertools
from pathlib import Path
from typing import Self

from aoc24 import utils


class Report:
    __slots__ = ("__condist", "__readings")

    __readings: list[int]
    __condist: list[int]

    def __init__(self, readings: list[int]) -> None:
        self.__readings = readings
        self.__condist = [(a - b) for (a, b) in itertools.pairwise(readings)]

    @classmethod
    def from_str(cls, line: str) -> Self:
        readings = list(map(int, line.split(" ")))

        return cls(readings)

    @property
    def cond1(self):
        return all(x > 0 for x in self.__condist) or all(x < 0 for x in self.__condist)

    @property
    def within_interval(self):
        return all(abs(x) in range(1, 3 + 1) for x in self.__condist)

    @property
    def naive_safe(self):
        return self.cond1 and self.within_interval

    @property
    def is_safe(self):
        p1 = self.naive_safe

        if p1:
            return True

        s = self.__readings
        candidates = (s[:i] + s[i + 1 :] for i in range(len(s)))

        for candidate in candidates:
            r = Report(candidate)
            if r.naive_safe:
                return True

        return False


def read_data(pth: Path) -> list[Report]:
    lines = pth.read_text().splitlines()

    return [Report.from_str(s) for s in lines]


def part1():
    data_pth = utils.get_data_file(2)

    reports = read_data(data_pth)

    final = sum(1 for r in reports if r.naive_safe)

    print(f"Day 2 part 1: {final}")


def part2():
    data_pth = utils.get_data_file(2)
    reports = read_data(data_pth)
    final = sum(1 for r in reports if r.is_safe)

    print(f"Day 2 part 2: {final}")
