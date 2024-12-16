import enum
from typing import Self
from dataclasses import dataclass
from aoc24 import utils


SimpleMemory = list[int | None]

FREE_ID = -1


@dataclass
class Block:
    length: int
    id_: int

    @property
    def is_free(self) -> bool:
        return self.id_ == FREE_ID

    def checksum(self, start: int) -> int:
        if self.is_free:
            return 0

        return sum(i * self.id_ for i in range(start, start + self.length))

    def copy(self):
        return Block(self.length, self.id_)

    @classmethod
    def free(cls, length: int):
        return Block(length, FREE_ID)


@dataclass
class AdvancedMemory:
    blocks: list[Block]
    highest_id: int

    @classmethod
    def from_txt(cls, inp: str) -> Self:
        inp = inp.rstrip()
        curr_id = 0
        blocks: list[Block] = []
        is_file = True

        for x in inp:
            times = int(x)

            if is_file:
                block = Block(times, curr_id)
                curr_id += 1
            else:
                block = Block(times, -1)

            blocks.append(block)
            is_file = not is_file

        return cls(blocks, curr_id - 1)

    def copy(self):
        blocks = [x.copy() for x in self.blocks]

        return AdvancedMemory(blocks, self.highest_id)

    def __iter__(self):
        return iter(self.blocks)

    def __len__(self):
        return len(self.blocks)

    def __getitem__(self, idx: int):
        return self.blocks[idx]

    def __setitem__(self, idx: int, val: Block) -> None:
        self.blocks[idx] = val


def to_simple_memory(inp: str) -> SimpleMemory:
    inp = inp.rstrip()
    curr_id = 0
    res: SimpleMemory = []
    is_file = True

    for x in inp:
        times = int(x)

        if is_file:
            res.extend([curr_id] * times)
            curr_id += 1
        else:
            res.extend([None] * times)
        is_file = not is_file

    return res


def simple_compact(memory: SimpleMemory) -> SimpleMemory:
    mem: SimpleMemory = memory[:]

    free_slot = mem.index(None)
    to_move_idx = len(mem) - 1

    while to_move_idx > free_slot and mem[to_move_idx] is None:
        to_move_idx -= 1

    while free_slot < to_move_idx:
        mem[free_slot] = mem[to_move_idx]
        mem[to_move_idx] = None

        while free_slot < to_move_idx and mem[free_slot] is not None:
            free_slot += 1

        while to_move_idx > free_slot and mem[to_move_idx] is None:
            to_move_idx -= 1

    return mem


def simple_checksum(mem: SimpleMemory) -> int:
    return sum(i * x for (i, x) in enumerate(mem) if x is not None)


def adv_checksum(mem: AdvancedMemory) -> int:
    checksum = 0

    offset = 0
    for block in mem:
        checksum += block.checksum(offset)
        offset += block.length

    return checksum


def part1():
    txt = utils.read_contents(9)
    memory = to_simple_memory(txt)
    compact = simple_compact(memory)
    res = simple_checksum(compact)

    print(f"Day 9 part 1: {res}")


def advanced_compact(memory: AdvancedMemory) -> AdvancedMemory:
    mem = memory.copy()

    to_move_id = memory.highest_id
    prev_to_move_idx = len(mem)
    while to_move_id >= 0:
        to_move_idx = -1
        for i in range(prev_to_move_idx):
            if mem[i].id_ == to_move_id:
                to_move_idx = i
                break
        if to_move_idx == -1:
            to_move_id -= 1
            continue

        prev_to_move_idx = to_move_idx
        block_to_move = mem[to_move_idx]
        required_space = block_to_move.length
        free_slot = -1
        for slot, block in enumerate(mem.blocks[:to_move_idx]):
            if block.is_free and block.length >= required_space:
                free_slot = slot
                break

        if free_slot != -1:
            # eq space or less space
            free_block = mem[free_slot]
            if free_block.length == required_space:
                # simple swap is okay
                mem[free_slot] = block_to_move
                mem[to_move_idx] = free_block
            else:
                # split current free into into two parts
                mem[to_move_idx] = Block.free(required_space)
                mem[free_slot] = Block(required_space, block_to_move.id_)
                mem.blocks.insert(free_slot + 1, Block.free(free_block.length - required_space))

        to_move_id -= 1

    return mem


def part2():
    txt = utils.read_contents(9)
    memory = AdvancedMemory.from_txt(txt)
    compact = advanced_compact(memory)
    res = adv_checksum(compact)

    print(f"Day 9 part 2: {res}")


if __name__ == "__main__":
    test1 = "12345"
    test2 = "2333133121414131402"

    test2_simple_mem = to_simple_memory(test2)
    test2_adv_mem = AdvancedMemory.from_txt(test2)

    test2_simple_comp = simple_compact(test2_simple_mem)
    test2_adv_comp = advanced_compact(test2_adv_mem)

    print(simple_checksum(test2_simple_comp))
    print(adv_checksum(test2_adv_comp))
