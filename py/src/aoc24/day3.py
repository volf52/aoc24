from pathlib import Path
from aoc24 import utils
import re

MULRE = re.compile(r"(don\'t\(\))|(do\(\))|(mul\((\d+)\,(\d+)\))")

print(
    MULRE.findall(
        "xdon't()mul(2,4)do()%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))"
    )
)


def read_data(pth: Path):
    lines = pth.read_text().splitlines()

    group_gen = (match.groups() for line in lines for match in MULRE.finditer(line))
    print(list(group_gen))
    tuple_gen = ((int(a), int(b)) for (a, b) in group_gen)

    to_mul: list[tuple[int, int]] = list(tuple_gen)

    print(len(to_mul))

    return to_mul


def part1():
    data_pth = utils.get_data_file(3)
    data = read_data(data_pth)

    final = sum(a * b for a, b in data)

    print(f"Day 2 part 1: {final}")


def part2():
    data_pth = utils.get_data_file(3)
    data = read_data(data_pth)

    final = sum([1])

    print(f"Day 2 part 2: {final}")
