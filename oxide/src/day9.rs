use crate::utils;

type Num = u64;
type SimpleBlock = Option<Num>;
type SimpleMemory = Vec<SimpleBlock>;

#[derive(Clone, Copy)]
struct AdvBlock {
    length: u32,
    val: SimpleBlock,
}

impl AdvBlock {
    fn new(length: u32, val: SimpleBlock) -> Self {
        Self { length, val }
    }

    fn is_free(&self) -> bool {
        self.val.is_none()
    }

    fn free_with_len(length: u32) -> Self {
        Self::new(length, Option::None)
    }

    fn checksum(&self, start: Num) -> Num {
        match self.val {
            None => 0,
            Some(v) => (start..start + self.length as Num).map(|s| s * v).sum(),
        }
    }

    fn split(&self, new_size: u32, block: SimpleBlock) -> (Self, Option<Self>) {
        let a = AdvBlock::new(new_size, block);
        let b = if new_size == self.length {
            Option::None
        } else {
            Option::Some(Self::free_with_len(self.length - new_size))
        };

        (a, b)
    }
}

fn load_simple_data() -> SimpleMemory {
    let txt = utils::read_day_file(9);

    let mut curr_id: Num = 0;
    let mut is_file = true;

    let mut blocks: SimpleMemory = Vec::new();

    for ch in txt.trim_end().chars() {
        let times = ch.to_digit(10).unwrap() as usize;

        let block: SimpleBlock = if is_file {
            curr_id += 1;
            Option::Some(curr_id - 1)
        } else {
            Option::None
        };

        let slice = std::iter::repeat_n(block, times).collect::<Vec<_>>();
        blocks.extend_from_slice(&slice);
        is_file = !is_file;
    }

    blocks
}

fn simple_compress(memory: &SimpleMemory) -> SimpleMemory {
    let mut mem = memory.clone();

    let mut free_slot = 0;
    let mut to_move_idx = mem.len() - 1;

    while free_slot < to_move_idx && mem[free_slot].is_some() {
        free_slot += 1;
    }

    while to_move_idx > free_slot && mem[to_move_idx].is_none() {
        to_move_idx -= 1;
    }

    while free_slot < to_move_idx {
        mem[free_slot] = mem[to_move_idx];
        mem[to_move_idx] = Option::None;

        while free_slot < to_move_idx && mem[free_slot].is_some() {
            free_slot += 1;
        }

        while to_move_idx > free_slot && mem[to_move_idx].is_none() {
            to_move_idx -= 1;
        }
    }

    mem
}

fn simple_checksum(memory: &SimpleMemory) -> usize {
    memory
        .iter()
        .enumerate()
        .map(|(pos, x)| pos * x.unwrap_or(0) as usize)
        .sum::<usize>()
}

pub fn part1() {
    let mem: SimpleMemory = load_simple_data();
    let compressed = simple_compress(&mem);
    let checksum = simple_checksum(&compressed);

    println!("Day 9 part 1: {checksum}")
}

type AdvMemory = Vec<AdvBlock>;

fn load_adv_data() -> (AdvMemory, Num) {
    let txt = utils::read_day_file(9);

    let mut curr_id: Num = 0;
    let mut is_file = true;

    let mut blocks: AdvMemory = Vec::with_capacity(txt.len());

    for ch in txt.trim_end().chars() {
        let times = ch.to_digit(10).unwrap();

        let block: AdvBlock = if is_file {
            curr_id += 1;

            AdvBlock::new(times, Option::Some(curr_id - 1))
        } else {
            AdvBlock::free_with_len(times)
        };

        blocks.push(block);
        is_file = !is_file;
    }

    (blocks, curr_id - 1)
}

fn adv_compress(memory: &AdvMemory, highest_id: Num) -> AdvMemory {
    let mut mem = memory.clone();

    let mut to_move_id = highest_id;
    let total_blocks = mem.len() - 1;
    let mut prev_to_move_idx = total_blocks + 1;

    while to_move_id > 0 {
        let mut to_move_idx = Option::None;

        for (i, block) in mem[..prev_to_move_idx].iter().rev().enumerate() {
            if let Some(id) = block.val {
                if id == to_move_id {
                    to_move_idx = Option::Some(total_blocks - i);
                    break;
                }
            }
        }
        if to_move_idx.is_none() {
            to_move_id -= 1;
            continue;
        }

        // Found a block to move, now find a block with enough memory
        prev_to_move_idx = to_move_idx.unwrap();
        let block_to_move = mem[prev_to_move_idx];
        let required_size = block_to_move.length;

        let mut free_slot = Option::None;
        for (i, block) in mem[..prev_to_move_idx].iter().enumerate() {
            if block.is_free() && block.length >= required_size {
                free_slot = Option::Some(i);
                break;
            }
        }

        if let Some(free_slot_idx) = free_slot {
            // Two cases, equal size or more
            let (a, b) = mem[free_slot_idx].split(required_size, block_to_move.val);
            mem[prev_to_move_idx] = AdvBlock::free_with_len(required_size);
            mem[free_slot_idx] = a;

            if let Some(another_free) = b {
                mem.insert(free_slot_idx + 1, another_free);
            }
        }

        to_move_id -= 1;
    }

    mem.to_vec()
}

fn adv_checksum(memory: &AdvMemory) -> Num {
    let mut checksum: Num = 0;
    let mut offset: Num = 0;

    for block in memory {
        checksum += block.checksum(offset);
        offset += block.length as Num;
    }

    checksum
}

pub fn part2() {
    let (mem, highest_id) = load_adv_data();
    let compressed = adv_compress(&mem, highest_id);
    let checksum = adv_checksum(&compressed);

    println!("Day 9 part 2: {checksum}")
}
