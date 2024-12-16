import itertools as it
from collections.abc import Callable, Sequence
from dataclasses import dataclass
from operator import add, mul
from time import perf_counter
from typing import Literal, Self

from aoc24 import utils

Operands = list[int]
EqHolder = list[tuple[int, Operands]]
Operator = Literal["+", "*", "||"]


def concat(a: int, b: int) -> int:
    return int(str(a) + str(b))


OPS: dict[Operator, Callable[[int, int], int]] = {"+": add, "*": mul, "||": concat}


@dataclass
class CalibEqs:
    eqs: EqHolder

    @classmethod
    def from_lines(cls, lines: Sequence[str]) -> Self:
        eqs: EqHolder = []

        for line in lines:
            a, b = line.split(":")
            test_val = int(a.strip())
            operands = [int(x) for x in b.strip().split(" ")]

            assert len(operands) > 1, "Invalid operands"

            eqs.append((test_val, operands))

        return cls(eqs)

    @classmethod
    def load(cls) -> Self:
        lines = utils.read_lines(7)
        # print("lines", len(lines))
        return cls.from_lines(lines)


def evaluate_equation(operands: Operands, operators: Sequence[Operator]) -> int:
    assert len(operators) == (len(operands) - 1), "Mismatch bw operators and operands"

    acc = operands[0]
    for operand, operator in zip(operands[1:], operators):
        op = OPS[operator]
        acc = op(acc, operand)
    return acc


PART_1_OPERATORS: list[Operator] = ["+", "*"]


def does_eq_test_val(test_val: int, operands: Operands, operators: Sequence[Operator]) -> bool:
    assert len(operators) == (len(operands) - 1), "Mismatch bw operators and operands"
    acc = operands[0]
    for operand, operator in zip(operands[1:], operators):
        op = OPS[operator]
        acc = op(acc, operand)
        if acc > test_val:
            return False

    return acc == test_val


def part1_sol(holder: CalibEqs):
    correct = 0
    for test_val, operands in holder.eqs:
        for operators in it.product(PART_1_OPERATORS, repeat=len(operands) - 1):
            if does_eq_test_val(test_val, operands, operators):
                correct += test_val
                break

    return correct


PART_2_OPERATORS: list[Operator] = ["+", "*", "||"]


def part2_sol(holder: CalibEqs):
    correct = 0
    for test_val, operands in holder.eqs:
        for operators in it.product(PART_2_OPERATORS, repeat=len(operands) - 1):
            if does_eq_test_val(test_val, operands, operators):
                correct += test_val
                break

    return correct


def part1():
    eqs = CalibEqs.load()
    start = perf_counter()
    correct = part1_sol(eqs)
    took = perf_counter() - start

    print(f"Took {took*1000:.4f} ms")
    print(f"Day 7 part 1: {correct}")


def part2():
    eqs = CalibEqs.load()
    start = perf_counter()
    correct = part2_sol(eqs)
    took = perf_counter() - start

    print(f"Took {took*1000:.4f} ms")
    print(f"Day 7 part 2: {correct}")


def show_eq(operands: Operands, operators: Sequence[Operator]):
    assert len(operands) == (len(operators) + 1)

    res = [str(operands[0])]
    for a, b in zip(operands[1:], operators):
        res.extend([str(b), str(a)])

    return " ".join(res)


if __name__ == "__main__":
    lines = """190: 10 19
3267: 81 40 27
83: 17 5
156: 15 6
7290: 6 8 6 15
161011: 16 10 13
192: 17 8 14
21037: 9 7 18 13
292: 11 6 16 20""".splitlines()
    eqs = CalibEqs.from_lines(lines)
    part1_eqs = CalibEqs.load()
    start = perf_counter()
    result = part1_sol(eqs)
    elapsed = perf_counter() - start
    print(f"{result=}")
    print(f"Took {elapsed*1000:.4f} ms")
    print(list(it.product(["+", "*"], repeat=3)))
