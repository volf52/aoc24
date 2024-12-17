use crate::utils;

type Num = u32;
type Pair = (Num, Num);

struct Machine {
    button_a: Pair,
    button_b: Pair,
    prize: Pair,
}

fn button_extract(s: &str) -> Pair {
    let mut splits = s.split(',');

    // 9 - len(Button A: X+)
    let x = splits.next().unwrap()[12..].parse::<Num>().unwrap();
    // 3 - len( Y+)
    let y = splits.next().unwrap()[3..].parse::<Num>().unwrap();

    (x, y)
}

fn prize_extract(s: &str) -> Pair {
    let mut splits = s.split(',');

    // 9 - len(Prize: X=)
    let x = splits.next().unwrap()[9..].parse::<Num>().unwrap();
    // 3 - len( Y=)
    let y = splits.next().unwrap()[3..].parse::<Num>().unwrap();

    (x, y)
}

impl From<&str> for Machine {
    fn from(value: &str) -> Self {
        let lines = value.lines().collect::<Vec<_>>();

        let button_a = button_extract(lines[0]);
        let button_b = button_extract(lines[1]);
        let prize = prize_extract(lines[2]);

        Self {
            button_a,
            button_b,
            prize,
        }
    }
}

fn get_machines(s: &str) -> Vec<Machine> {
    s.split("\n\n").map(Machine::from).collect()
}

fn load_data() -> Vec<Machine> {
    let s = utils::read_day_file(13);

    get_machines(&s)
}

pub fn part1() {
    let machines = load_data();
    // use vector stuff
    // pos_vec = 3 * button_a + button_b
}

pub fn part2() {}
