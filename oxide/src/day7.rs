use std::{fs::File, io::Write};

use itertools::{repeat_n, Itertools};

type Num = u64;

#[derive(Debug)]
enum Operator {
    Plus,
    Mult,
    Concat,
}

impl Operator {
    fn eval(&self, a: Num, b: Num) -> Num {
        match self {
            Operator::Plus => a + b,
            Operator::Mult => a * b,
            Operator::Concat => (a.to_string() + &b.to_string()).parse::<Num>().unwrap(),
        }
    }
}

#[derive(Debug)]
pub struct Equation {
    target: Num,
    operands: Vec<Num>,
    is_too_low: bool,
    is_too_high_mul: bool,
    is_too_high_concat: bool,
}

impl Equation {
    fn new(target: Num, operands: Vec<Num>) -> Self {
        let is_too_low = operands.iter().sum::<Num>() > target;
        let is_too_high_mul = operands.iter().product::<Num>() < target;

        let mut concated = String::new();
        for op in &operands {
            concated.push_str(&op.to_string());
        }
        let concated_total = concated.parse::<Num>().unwrap();
        let is_too_high_concat = concated_total < target;

        Self {
            target,
            operands,
            is_too_low,
            is_too_high_mul,
            is_too_high_concat,
        }
    }

    fn from_line(line: &str) -> Self {
        let (target, rest) = {
            let mut parts = line.splitn(2, ':');

            let target = parts.next().unwrap().parse::<Num>().unwrap();
            let rest = parts.next().unwrap();

            (target, rest)
        };

        let operands = rest
            .split_ascii_whitespace()
            .map(|s| s.parse::<Num>().unwrap())
            .collect::<Vec<_>>();

        Self::new(target, operands)
    }

    fn eval(&self, operators: &[&Operator]) -> Num {
        let mut acc = self.operands[0];

        let s = &self.operands[1..];
        for (operand, operator) in s.iter().zip(operators.iter()) {
            acc = operator.eval(acc, *operand);

            if acc > self.target {
                return 0;
            }
        }

        acc
    }

    fn can_be_true_p1(&self, allowed_operators: &[Operator]) -> Num {
        let it =
            repeat_n(allowed_operators.iter(), self.operands.len() - 1).multi_cartesian_product();

        for operators in it {
            let res = self.eval(&operators);
            if res == self.target {
                return res;
            }
        }

        0
    }
    fn can_be_true_p2(&self, allowed_operators: &[Operator]) -> Num {
        let it =
            repeat_n(allowed_operators.iter(), self.operands.len() - 1).multi_cartesian_product();

        for operators in it {
            let res = self.eval(&operators);
            if res == self.target {
                return res;
            }
        }

        0
    }
}

pub fn load_data() -> Vec<Equation> {
    let lines = crate::utils::read_day_lines(7);

    let equations = lines
        .iter()
        .map(|s| Equation::from_line(s))
        .collect::<Vec<_>>();

    equations
}

static TEST_DATA: &str = r#"190: 10 19
3267: 81 40 27
83: 17 5
156: 15 6
7290: 6 8 6 15
161011: 16 10 13
192: 17 8 14
21037: 9 7 18 13
292: 11 6 16 20"#;

pub fn part1() {
    let eqs = TEST_DATA
        .lines()
        .map(Equation::from_line)
        .collect::<Vec<_>>();
    let operators = vec![Operator::Plus, Operator::Mult];

    let res = eqs
        .iter()
        .map(|eq| eq.can_be_true_p1(&operators))
        .sum::<Num>();

    println!("Day 7 part 1 (test): {res}");

    let part_eqs = load_data();
    let res = part_eqs
        .iter()
        .map(|eq| eq.can_be_true_p1(&operators))
        .sum::<Num>();
    println!("Day 7 part 1: {res}");
}

pub fn part2() {
    let eqs = TEST_DATA
        .lines()
        .map(Equation::from_line)
        .collect::<Vec<_>>();
    let operators = vec![Operator::Plus, Operator::Mult, Operator::Concat];

    let res = eqs
        .iter()
        .map(|eq| eq.can_be_true_p2(&operators))
        .sum::<Num>();

    println!("Day 7 part 2 (test): {res}");

    let part_eqs = load_data();

    let res = part_eqs
        .iter()
        .map(|eq| eq.can_be_true_p2(&operators))
        .sum::<Num>();
    println!("Day 7 part 2: {res}");
}

pub fn part1_test() {
    let part_eqs = load_data();

    let operators = vec![Operator::Plus, Operator::Mult];
    let res_lines = part_eqs
        .iter()
        .enumerate()
        .map(|(idx, eq)| {
            let r = eq.can_be_true_p1(&operators);

            let r_t = if r == 0 { "false" } else { "true" };

            format!("{},{},{}", idx, eq.target, r_t)
        })
        .join("\n");

    let mut f = File::create("rust_results.csv").unwrap();
    let _ = f.write(b"index,test_val,operands\n").unwrap();
    let _ = f.write(res_lines.as_bytes()).unwrap();
}
