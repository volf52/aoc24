use std::collections::HashMap;

use crate::utils;

type Num = u32;

fn process_line(s: &str) -> (Num, Num) {
    let (first, second) = {
        let mut sp = s.split_whitespace();
        (
            sp.next().expect("Failed to extract the first element"),
            sp.next().expect("Failed to extract the second element"),
        )
    };

    let (fnum, snum) = (
        first
            .parse::<Num>()
            .expect("First element is not a valid number"),
        second
            .parse::<Num>()
            .expect("Second element is not a valid number"),
    );

    (fnum, snum)
}

pub fn part1() {
    let lines = utils::read_day_lines(1);
    let mut pairs: (Vec<_>, Vec<_>) = lines.iter().map(|s| process_line(s.as_str())).unzip();

    pairs.0.sort();
    pairs.1.sort();

    let res = pairs
        .0
        .iter()
        .zip(pairs.1.iter())
        .map(|(a, b)| a.abs_diff(*b))
        .sum::<Num>();

    println!("Day 1 part 1: {res}");
}

pub fn part2() {
    let lines = utils::read_day_lines(1);
    let pairs: (Vec<_>, Vec<_>) = lines.iter().map(|s| process_line(s.as_str())).unzip();

    let mut counter: HashMap<Num, u32> = HashMap::new();

    for num in pairs.1 {
        counter
            .entry(num)
            .and_modify(|e| {
                *e += 1;
            })
            .or_insert(1);
    }

    let res = pairs
        .0
        .iter()
        .fold(0_u32, |acc, &curr| match counter.get(&curr) {
            Some(&count) => acc + curr * count,
            None => acc,
        });

    println!("Day 1 part 2: {res}");
}
