import enum
from pathlib import Path
from typing import NamedTuple

import parsy
from aoc24 import utils
import re
from parsy import digit, match_item

MULRE = re.compile(r"(don\'t\(\))|(do\(\))|(mul\((\d+)\,(\d+)\))")


class MulInstr(NamedTuple):
    left: int
    right: int


class Do_Or_Dont(enum.Enum):
    Do = "do()"
    Dont = "don't()"


def parse_instructions(s: str):
    do_dont = parsy.from_enum(Do_Or_Dont)

    num = digit.at_least(1).concat().map(int)
    mul_instr = parsy.seq(
        __lparen=parsy.string("mul("),
        left=num.desc("left"),
        __comma=match_item(","),
        right=num.desc("right"),
        __end=match_item(")"),
    ).combine_dict(MulInstr)

    valid_instr = mul_instr | do_dont

    instr = (valid_instr | parsy.any_char).many()

    return [
        t
        for t in instr.parse(s)
        if isinstance(t, Do_Or_Dont) or isinstance(t, MulInstr)
    ]


def read_data(pth: Path):
    txt = pth.read_text()
    tokens = parse_instructions(txt)

    return tokens


def part1():
    data_pth = utils.get_data_file(3)
    data = read_data(data_pth)
    res = 0
    for token in data:
        if isinstance(token, MulInstr):
            res += token.left * token.right

    print(f"Day 3 part 1: {res}")


def part2():
    data_pth = utils.get_data_file(3)
    data = read_data(data_pth)

    res = 0
    is_mul_enabled = True

    for token in data:
        if isinstance(token, Do_Or_Dont):
            is_mul_enabled = token == Do_Or_Dont.Do
        elif is_mul_enabled:
            res += token.left * token.right

    print(f"Day 3 part 2: {res}")
