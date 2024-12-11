from typing import Self
from aoc24 import utils
from collections import defaultdict
from dataclasses import dataclass

Order = list[str]
Deps = dict[str, list[str]]


@dataclass
class Processed:
    dependencies: Deps
    dependents: Deps
    orders: list[Order]

    @classmethod
    def from_lines(cls, lines: list[str]) -> Self:
        dependencies: Deps = defaultdict(list)
        dependents: Deps = defaultdict(list)

        for i, line in enumerate(lines):
            if line == "":
                break
            x, y = line.split("|")
            dependencies[y].append(x)
            dependents[x].append(y)

        orders: list[Order] = []
        for line in lines[i + 1 :]:
            orders.append(line.split(","))

        return cls(dependencies=dependencies, dependents=dependents, orders=orders)

    @classmethod
    def load(cls) -> Self:
        lines = utils.read_lines(5)
        return cls.from_lines(lines)

    def is_order_correct(self, order: Order) -> bool:
        already_seen: set[str] = set()
        for page in order:
            dependents = self.dependents.get(page, [])
            for dependent in dependents:
                if dependent in already_seen:
                    return False
            already_seen.add(page)
        return True


def part1_count(processed: Processed):
    count = 0
    for order in processed.orders:
        if processed.is_order_correct(order):
            # print(order)
            mid = order[len(order) // 2]
            count += int(mid)

    return count


def part1():
    processed = Processed.load()
    count = part1_count(processed)

    print(f"Day 5 part 1: {count}")


def part2_count(processed: Processed):
    count = 0
    for order in processed.orders:
        if not processed.is_order_correct(order):
            # find correct
            # get mid of correct
            mid = 0

            count += int(mid)
    return count


def part2():
    processed = Processed.load()
    count = part2_count(processed)

    print(f"Day 5 part 2: {count}")


if __name__ == "__main__":
    lines = """47|53
97|13
97|61
97|47
75|29
61|13
75|53
29|13
97|29
53|29
61|53
97|53
61|29
47|13
75|47
97|75
47|61
75|61
47|29
75|13
53|13

75,47,61,53,29
97,61,53,29,13
75,29,13
75,97,47,61,53
61,13,29
97,13,75,29,47""".splitlines()
    processed = Processed.from_lines(lines)
    for a, b in processed.dependencies.items():
        if len(b) > 1:
            print(a, b)
    print("-" * 70)
    for a, b in processed.dependents.items():
        if len(b) > 1:
            print(a, b)

    print("-" * 70)
    print(part1_count(processed))
    print(part2_count(processed))
