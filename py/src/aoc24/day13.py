from dataclasses import dataclass
from enum import unique
from typing import NamedTuple, Self

from aoc24.utils import Pair, read_contents

BUTTON_A_MUL = 3
BUTTON_B_MUL = 1


def cost(a: int | float, b: int | float) -> float:
    return BUTTON_A_MUL * a + b


@dataclass()
class Result:
    a: float
    b: float
    unique: bool

    def is_int(self) -> bool:
        return self.a == int(self.a) and self.b == int(self.b)


def solve_for_a_b(vec_a: Pair, vec_b: Pair, vec_c: Pair) -> Result | None:
    A = [[vec_a.x, vec_b.x], [vec_a.y, vec_b.y]]
    C = [vec_c.x, vec_c.y]

    det_A = vec_a.determinant(vec_b)

    if det_A != 0:
        # Unique solution exists
        a = (C[0] * A[1][1] - C[1] * A[0][1]) / det_A
        b = (A[0][0] * C[1] - A[1][0] * C[0]) / det_A

        return Result(a, b, unique=True)

    # No unique solution
    return None


@dataclass()
class Machine:
    button_a: Pair
    button_b: Pair
    prize: Pair

    @classmethod
    def from_str(cls, s: str) -> Self:
        lines = s.strip().splitlines()
        assert len(lines) == 3, "expected 3 lines for machine constr input"

        button_a = Pair.from_str(lines[0], line_offset=9, part_offset=2)
        button_b = Pair.from_str(lines[1], line_offset=9, part_offset=2)
        prize = Pair.from_str(lines[2], line_offset=7, part_offset=2)

        return cls(button_a, button_b, prize)


def load_machines() -> list[Machine]:
    s = read_contents(13)

    parts = s.split("\n\n")
    machines = [Machine.from_str(part) for part in parts]

    return machines


def part1():
    machines = load_machines()

    results = [
        solve_for_a_b(machine.button_a, machine.button_b, machine.prize) for machine in machines
    ]

    good_results = [r for r in results if r is not None and r.is_int()]
    # print(f"Good results: {len(good_results)}")

    total_cost = sum(cost(r.a, r.b) for r in good_results)

    print(f"Day 13 part 1: {int(total_cost)}")


def part2():
    machines = load_machines()

    to_add = Pair(10000000000000, 10000000000000)

    for m in machines:
        m.prize = m.prize + to_add

    results = [solve_for_a_b(m.button_a, m.button_b, m.prize) for m in machines]
    good_results = [r for r in results if r is not None and r.is_int()]
    total_cost = sum(cost(r.a, r.b) for r in good_results)

    print(f"Day 13 part 2: {int(total_cost)}")


if __name__ == "__main__":
    test = """Button A: X+94, Y+34
Button B: X+22, Y+67
Prize: X=8400, Y=5400

Button A: X+26, Y+66
Button B: X+67, Y+21
Prize: X=12748, Y=12176

Button A: X+17, Y+86
Button B: X+84, Y+37
Prize: X=7870, Y=6450

Button A: X+69, Y+23
Button B: X+27, Y+71
Prize: X=18641, Y=10279"""

    parts = test.split("\n\n")
    machines = [Machine.from_str(p) for p in parts]

    results = [solve_for_a_b(m.button_a, m.button_b, m.prize) for m in machines]
    print(results)

    s = results[0]
    print(s.a == int(s.a))
