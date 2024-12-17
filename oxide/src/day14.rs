use std::{collections::HashSet, iter::repeat_n, ops::Range, task::ready};

use crate::utils;

type Num = i32;
type Pair = (Num, Num);

const MAX_X: Num = 101;
const MAX_Y: Num = 103;
const MID_X: Num = MAX_X / 2;
const MID_Y: Num = MAX_Y / 2;

struct Robot {
    pos: Pair,
    vel: Pair,
}

fn extract_pair(s: &str) -> Pair {
    let mut splits = s.split(',');

    let x = splits.next().unwrap()[2..].parse::<Num>().unwrap();
    let y = splits.next().unwrap().parse::<Num>().unwrap();

    (x, y)
}

impl From<&str> for Robot {
    fn from(value: &str) -> Self {
        let mut parts = value.split_ascii_whitespace();

        let pos = extract_pair(parts.next().unwrap());
        let vel = extract_pair(parts.next().unwrap());

        Self { pos, vel }
    }
}

impl Robot {
    fn step(&mut self, max_x: Num, max_y: Num) {
        let mut new_x = (self.pos.0 + self.vel.0) % max_x;
        let mut new_y = (self.pos.1 + self.vel.1) % max_y;

        if new_x < 0 {
            new_x += max_x;
        }
        // if new_x >= max_x {
        //     new_x %= max_x;
        // }

        if new_y < 0 {
            new_y += max_y;
        }
        // if new_y >= max_y {
        //     new_y %= max_y;
        // }

        self.pos = (new_x, new_y);
    }
}

fn from_txt(s: &str) -> Vec<Robot> {
    s.lines().map(Robot::from).collect()
}

fn load_data() -> Vec<Robot> {
    let s = utils::read_day_file(14);

    from_txt(&s)
}

type Quadrant = (Range<Num>, Range<Num>);

fn does_quad_contain(pos: &Pair, quad: &Quadrant) -> bool {
    quad.0.contains(&pos.0) && quad.1.contains(&pos.1)
}

pub fn part1() {
    let mut robots = load_data();

    for _ in 0..100 {
        for r in robots.iter_mut() {
            r.step(MAX_X, MAX_Y);
        }
    }

    let mut q_sum: [u32; 4] = [0, 0, 0, 0];

    let x_range_0 = 0..MID_X;
    let x_range_1 = MID_X + 1..MAX_X + 1;

    let y_range_0 = 0..MID_Y;
    let y_range_1 = MID_Y + 1..MAX_Y + 1;

    let quads: [(Range<Num>, Range<Num>); 4] = [
        (x_range_0.clone(), y_range_0.clone()),
        (x_range_1.clone(), y_range_0),
        (x_range_0, y_range_1.clone()),
        (x_range_1, y_range_1),
    ];

    for (quad, s) in quads.iter().zip(q_sum.iter_mut()) {
        for r in robots.iter() {
            if does_quad_contain(&r.pos, quad) {
                *s += 1;
            }
        }
    }

    dbg!(&q_sum);

    let res = q_sum.iter().product::<u32>();

    println!("Day 14 part 1: {res}");
}

fn display_grid(robots: &[Robot], max_x: Num, max_y: Num) {
    let mut grid_vec: Vec<Vec<usize>> = Vec::with_capacity(max_y as usize);
    for _ in 0..max_y {
        grid_vec.push(repeat_n(0, max_x as usize).collect());
    }

    for r in robots {
        let x = r.pos.0 as usize;
        let y = r.pos.1 as usize;

        grid_vec[y][x] += 1;
    }

    let mut final_str = String::with_capacity(((max_x as usize) + 1) * ((max_y as usize) + 1));
    for row in grid_vec {
        for col in row {
            if col == 0 {
                final_str.push('.');
            } else {
                final_str.push_str(&col.to_string());
            }
        }
        final_str.push('\n');
    }
    final_str.push('\n');

    println!("{}", final_str);
}

fn maybe_unique(robots: &[Robot]) -> bool {
    let total = robots.len();

    let mut pos_set: HashSet<Pair> = HashSet::with_capacity(total);

    for r in robots {
        pos_set.insert(r.pos);
    }

    pos_set.len() == total
}

pub fn part2() {
    let mut robots = load_data();

    println!();

    // let mut found = false;
    let mut ii = 0;
    let iterations = 50_000;
    // let mut can_be: Vec<u64> = Vec::new();
    let pbar = indicatif::ProgressBar::new(iterations);
    for i in 0..iterations {
        ii = i;

        for r in robots.iter_mut() {
            r.step(MAX_X, MAX_Y);
        }

        if maybe_unique(&robots) {
            // found = true;
            // can_be.push(i);
            break;
        }

        pbar.inc(1);
    }

    // let message = if found { "found" } else { "nothing bruh" };

    pbar.finish_and_clear();
    // pbar.finish_with_message(message);
    println!();
    println!();
    println!();

    // if found {
    ii += 1;
    display_grid(&robots, MAX_X, MAX_Y);
    println!("After {ii} iterations");
    // dbg!(&can_be);

    // }

    // display_grid(&robots, MAX_X, MAX_Y);
}

#[cfg(test)]
mod test {
    use crate::day14::Pair;

    use super::Robot;

    static TEST_STR: &str = r#"p=0,4 v=3,-3
p=6,3 v=-1,-3
p=10,3 v=-1,2
p=2,0 v=2,-1
p=0,0 v=1,3
p=3,0 v=-2,-2
p=7,6 v=-1,-3
p=3,0 v=-1,-2
p=9,3 v=2,3
p=7,3 v=-1,2
p=2,4 v=2,-3
p=9,5 v=-3,-3"#;

    #[test]
    fn test_parse() {
        let robots = TEST_STR.lines().map(Robot::from).collect::<Vec<_>>();

        assert_eq!(robots.len(), 12);

        let expected_pos_vel: Vec<(Pair, Pair)> = vec![
            ((0, 4), (3, -3)),
            ((6, 3), (-1, -3)),
            ((10, 3), (-1, 2)),
            ((2, 0), (2, -1)),
            ((0, 0), (1, 3)),
            ((3, 0), (-2, -2)),
            ((7, 6), (-1, -3)),
            ((3, 0), (-1, -2)),
            ((9, 3), (2, 3)),
            ((7, 3), (-1, 2)),
            ((2, 4), (2, -3)),
            ((9, 5), (-3, -3)),
        ];

        for (robot, (expected_pos, expected_vel)) in robots.iter().zip(expected_pos_vel) {
            assert_eq!(
                robot.pos, expected_pos,
                "Expected robot pos {:?} to equal {:?}",
                robot.pos, expected_pos
            );
            assert_eq!(
                robot.vel, expected_vel,
                "Expected robot vel {:?} to equal {:?}",
                robot.vel, expected_vel
            );
        }
    }

    #[test]
    fn test_step() {
        let mut robot = Robot {
            pos: (1, 2),
            vel: (3, -1),
        };

        robot.step(10, 10);
        assert_eq!(robot.pos, (4, 1));
    }

    #[test]
    fn test_teleport() {
        let mut robot = Robot {
            pos: (1, 2),
            vel: (9, -3),
        };

        robot.step(7, 10);
        assert_eq!(robot.pos, (3, 9));
    }

    #[test]
    fn test_teleport_edge() {
        let mut robot = Robot {
            pos: (1, 2),
            vel: (9, -3),
        };

        robot.step(10, 10);
        assert_eq!(robot.pos, (0, 9));
    }
}
