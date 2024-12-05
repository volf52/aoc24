use chumsky::{
    error::Cheap,
    prelude::{end, just},
    text::{self, TextParser},
    Parser,
};

use crate::utils;

#[derive(Debug)]
struct Multiply {
    left: u32,
    right: u32,
}

impl Multiply {
    fn eval(&self) -> u32 {
        self.left * self.right
    }
}

#[derive(Debug)]
enum Token {
    Mul(Multiply),
    Do,
    Dont,
}

struct Program {
    tokens: Vec<Token>,
    mul_enabled: bool,
}

impl From<Vec<Multiply>> for Program {
    fn from(values: Vec<Multiply>) -> Self {
        let tokens = values.into_iter().map(Token::Mul).collect();

        Self::new(tokens)
    }
}

impl From<Vec<Token>> for Program {
    fn from(tokens: Vec<Token>) -> Self {
        Self::new(tokens)
    }
}

impl Program {
    fn new(tokens: Vec<Token>) -> Self {
        Self {
            tokens,
            mul_enabled: true,
        }
    }

    fn eval(&self) -> u64 {
        let mut acc: u64 = 0;

        let mut is_mul_enabled = true;

        for token in &self.tokens {
            match token {
                Token::Do => {
                    is_mul_enabled = true;
                }
                Token::Dont => {
                    is_mul_enabled = false;
                }
                Token::Mul(Multiply { left, right }) => {
                    if is_mul_enabled {
                        acc += (*left as u64) * (*right as u64);
                    }
                }
            }
        }

        acc
    }
}

fn gen_general_parser() -> impl Parser<char, Vec<Token>, Error = Cheap<char>> {
    let do_instr = just("don't()").map(|_| Token::Dont);
    let dont_instr = just("do()").map(|_| Token::Do);

    let comma = just(',');
    let digits = text::int(10).from_str().unwrapped();

    let mul_instr = just("mul(")
        .ignore_then(digits)
        .then_ignore(comma.padded())
        .then(digits)
        .then_ignore(just(')'))
        .map(|(left, right)| Token::Mul(Multiply { left, right }));

    let instruction = mul_instr.or(dont_instr).or(do_instr);

    let garbage = instruction.not().ignored().repeated().at_least(0);

    garbage
        .ignore_then(instruction)
        .then_ignore(garbage)
        .repeated()
        .then_ignore(end())
}

fn gen_mul_parser() -> impl Parser<char, Vec<Multiply>, Error = Cheap<char>> {
    let comma = just(',');
    let digits = text::int(10).from_str().unwrapped();

    let mul_instr = just("mul(")
        .ignore_then(digits)
        .then_ignore(comma.padded())
        .then(digits)
        .then_ignore(just(')'))
        .map(|(left, right)| Multiply { left, right });

    let garbage = mul_instr.not().ignored().repeated().at_least(0);

    garbage
        .ignore_then(mul_instr)
        .then_ignore(garbage)
        .repeated()
        .then_ignore(end())
}

fn tokenize_general(hay: &str) -> Vec<Token> {
    let parser = gen_general_parser();

    parser.parse(hay).unwrap()
}

fn tokenize_mul_only(hay: &str) -> Vec<Multiply> {
    let parser = gen_mul_parser();

    parser.parse(hay).unwrap()
}

pub fn part1() {
    let s = utils::read_day_file(3);
    let tokens = tokenize_mul_only(&s);
    let program = Program::from(tokens);

    let res = program.eval();

    println!("Day 3 part 1: {:?}", res);
}

pub fn part2() {
    let s = utils::read_day_file(3);
    let tokens = tokenize_general(&s);
    let program = Program::from(tokens);

    let res = program.eval();

    println!("Day 3 part 2: {:?}", res);
}
