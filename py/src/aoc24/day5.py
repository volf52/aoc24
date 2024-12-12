from collections import defaultdict
from collections.abc import Sequence
from dataclasses import dataclass
from typing import Self

from aoc24 import utils

Page = str
Order = list[Page]
Deps = dict[Page, list[Page]]


@dataclass
class Processed:
    dependencies: dict[Page, set[Page]]
    dependents: Deps
    orders: list[Order]

    @classmethod
    def from_lines(cls, lines: Sequence[str]) -> Self:
        dependencies: dict[Page, set[Page]] = defaultdict(set)
        dependents: Deps = defaultdict(list)

        offset = 0
        for line in lines:
            if line == "":
                break
            x, y = line.split("|")
            dependencies[y].add(x)
            dependents[x].append(y)
            offset += 1

        orders: list[Order] = [line.split(",") for line in lines[offset + 1 :]]

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


def get_correct_order(processed: Processed, order: Order) -> Order:
    new_order: Order = order[:]

    i = 0
    # Kinda like insertion sort ensure that the part before i is okay,
    # and keep a value's deps before it by swapping
    while i < len(new_order):
        curr = new_order[i]
        curr_deps = processed.dependencies.get(curr, set())
        swapped = False
        for j, other in enumerate(new_order[i + 1 :], start=i + 1):
            if other in curr_deps:
                new_order[i], new_order[j] = new_order[j], new_order[i]
                swapped = True
                break
        if not swapped:
            i += 1

    return new_order


def part2_count(processed: Processed):
    count = 0
    for order in processed.orders:
        if not processed.is_order_correct(order):
            # find correct
            correct_order = get_correct_order(processed, order)
            # get mid of correct
            mid = correct_order[len(correct_order) // 2]

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
    for order in processed.orders:
        print(order)
    print("-" * 70)
    print(part1_count(processed))
    print(part2_count(processed))
    print(get_correct_order(processed, processed.orders[5]))
