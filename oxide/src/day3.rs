use chumsky::{
    error::Cheap,
    prelude::{any, end, just},
    text::{self, TextParser},
    Parser,
};
use regex::Regex;
use std::cell::LazyCell;

use crate::utils;

#[derive(Debug)]
enum Token {
    Mul { left: u32, right: u32 },
    Do,
    Dont,
}

const MULRE: LazyCell<Regex> =
    LazyCell::new(|| Regex::new(r"mul\((\d+)\,(\d+)\)").expect("invalid regex"));

fn gen_parser() -> impl Parser<char, Vec<Token>, Error = Cheap<char>> {
    let do_instr = just("don't()").map(|_| Token::Dont);
    let dont_instr = just("do()").map(|_| Token::Do);

    let comma = just(',');
    let digits = text::digits(10).from_str().unwrapped();
    // let digits = filter(|c: &char| c.is_ascii_digit())
    //     .repeated()
    //     .at_least(1)
    //     .collect::<String>()
    //     .map(|s| s.parse::<u32>().unwrap());

    let mul_instr = just("mul(")
        .ignore_then(digits)
        .then_ignore(comma.padded())
        .then(digits)
        .then_ignore(just(')'))
        .map(|(left, right)| Token::Mul { left, right });

    let instruction = mul_instr.or(dont_instr).or(do_instr);

    let garbage = any().ignored().repeated().at_least(0);

    garbage
        .ignore_then(instruction)
        .then_ignore(garbage)
        .repeated()
        .then_ignore(end())
}

fn tokenize(hay: &str) {
    println!("{}", hay);
    let parser = gen_parser();

    match parser.parse(hay) {
        Ok(tokens) => {
            for token in tokens {
                println!("{:?}", &token);
            }
        }
        Err(e) => {
            for err in e {
                println!("Parsing error: {:?}", err);
            }
        }
    };
}

pub fn part1() {
    let s = utils::read_day_file(3);

    // let res = MULRE
    //     .captures_iter(&s)
    //     .map(|m| {
    //         let cap1 = m.get(1).expect("first element not found");
    //         let cap2 = m.get(2).expect("second element not found");
    //
    //         let op1 = cap1.as_str().parse::<u32>().unwrap();
    //         // .expect("first element cannot be parsed into u32");
    //         let op2 = cap2
    //             .as_str()
    //             .parse::<u32>()
    //             .expect("second element cannot be parsed into u32");
    //
    //         op1 * op2
    //     })
    //     .sum::<u32>();

    // println!("Day 3 part 1: {:?}", res);
    tokenize(&s);
}

pub fn part2() {
    let s = utils::read_day_file(3);
    tokenize(&s);
}
