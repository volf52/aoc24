from collections import Counter
from pathlib import Path

from aoc24 import utils


def read_data(pth: Path) -> tuple[list[int], list[int]]:
    c = pth.read_text().splitlines()
    c = (x.split("   ") for x in c)
    c = ((int(a), int(b)) for (a, b) in c)
    left_list: list[int] = []
    right_list: list[int] = []

    for a, b in c:
        left_list.append(a)
        right_list.append(b)

    left_list.sort()
    right_list.sort()

    return left_list, right_list


def part1():
    datapth = utils.get_data_file(1)
    lst_a, lst_b = read_data(datapth)

    distances = (abs(a - b) for a, b in zip(lst_a, lst_b, strict=False))
    final = sum(distances)

    print(f"Day 1 part 1: {final}")


def part2():
    datapth = utils.get_data_file(1)
    lst_a, lst_b = read_data(datapth)

    counts = Counter(lst_b)

    sim_scores = (a * counts.get(a, 0) for a in lst_a)
    final = sum(sim_scores)

    print(f"Day 1 part 2: {final}")
