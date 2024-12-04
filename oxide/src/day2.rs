use crate::utils;

struct Report {
    positions: Vec<u32>,
    diff: Vec<i32>,
}

impl From<&str> for Report {
    fn from(value: &str) -> Self {
        let parsed = value
            .split_whitespace()
            .map(|s| s.parse::<u32>().expect("invalid u32"))
            .collect::<Vec<_>>();

        parsed.into()
    }
}

impl From<String> for Report {
    fn from(value: String) -> Self {
        value.as_str().into()
    }
}

impl From<Vec<u32>> for Report {
    fn from(value: Vec<u32>) -> Self {
        let r = value
            .windows(2)
            .map(|s| s[1] as i32 - s[0] as i32)
            .collect::<Vec<_>>();

        Self {
            positions: value,
            diff: r,
        }
    }
}

impl Report {
    fn condition1(&self) -> bool {
        let r = self.diff.as_slice();
        let is_pos = r[0] > 0;

        for &diff in r {
            let res = if is_pos { diff > 0 } else { diff <= 0 };

            if !res {
                return false;
            }

            let d = diff.abs();

            if !(1..=3).contains(&d) {
                return false;
            }
        }

        true
    }

    fn condition2(&self) -> bool {
        if self.condition1() {
            return true;
        }

        let r = self.positions.as_slice();
        let len = r.len();

        for i in 0..len {
            let mut candidate: Vec<u32> = Vec::with_capacity(len - 1);
            candidate.extend_from_slice(&r[..i]);
            candidate.extend_from_slice(&r[i + 1..]);
            // println!("{:?}", &candidate);

            let report = Report::from(candidate);

            if report.condition1() {
                return true;
            }
        }

        false
    }

    fn from_string(s: &str) -> Vec<Self> {
        s.lines().map(|s| s.into()).collect()
    }
}

pub fn part1() {
    let lines = utils::read_day_lines(2);
    let safe_reports = lines
        .iter()
        .filter(|s| Report::from(s.as_str()).condition1())
        .count();

    println!("Day 2 part 1: {safe_reports}");
}

pub fn part2() {
    let lines = utils::read_day_lines(2);
    let safe_reports = lines
        .iter()
        .filter(|s| Report::from(s.as_str()).condition2())
        .count();

    println!("Day 2 part 1: {safe_reports}");

    // let other_reports =
    //     Report::from_string("7 6 4 2 1\n1 2 7 8 9\n9 7 6 2 1\n1 3 2 4 5\n8 6 4 4 1\n1 3 6 7 9");
    //
    // let safe = other_reports.iter().filter(|r| r.condition2()).count();
    // println!("Test: {safe}");
}
