use crate::{Solution, SolutionPair};
use std::collections::HashMap;
use core::fmt::Display;
use std::fs::read_to_string;

#[derive(Clone)]
struct RoadFork {
    left:String,
    right:String,
    name:String
}

impl RoadFork{
    fn new(line:&str) -> Self {
        Self { left: String::from(&line[7..=9]), right: String::from(&line[12..=14]), name: String::from(&line[0..=2]) }
    }

    fn next_step<'b>(&'b self, dir:char) -> &'b str{
        if dir == 'L' {
            &self.left[..]
        } else {
            &self.right[..]
        }
    }
}

impl Display for RoadFork {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        write!(f,"{} -> {}/{}",self.name,self.left,self.right)
    }
}

// Borrowing the solution from Reddit user /u/marcosbp19 
// (https://www.reddit.com/r/adventofcode/comments/18df7px/comment/kcmxdku/?utm_source=share&utm_medium=web2x&context=3)
// See also https://paste.rs/foJg9.rs

// I still do *not* understand how or why this works.

fn lcm(a: u64, b: u64) -> u64 {
    (a * b) / gcd(a, b)
}

fn gcd(mut a: u64, mut b: u64) -> u64 {
    while b > 0 {
        let tmp_a = a;
        a = b;
        b = tmp_a % b;
    }
    return a;
}

///////////////////////////////////////////////////////////////////////////////

pub fn solve() -> SolutionPair {
    // Your solution here...
    let lines = read_to_string("input/day08.txt").unwrap();
    let mut line_iter = lines.lines();
    let directions:String = line_iter.next().unwrap().trim().into();
    line_iter.next();
    let forks:Vec<RoadFork> = line_iter.map(|l|RoadFork::new(l)).collect();
    let mut roadmap:HashMap<&str,RoadFork> = HashMap::new();
    for split in forks.iter() {
        roadmap.insert(&split.name[..], split.clone());
    }

    let path_len = |starting_point:&str| {
        let mut step_count = 0;
        let mut instruction_iter = directions.chars();
        let mut current_step = starting_point;
        while !current_step.ends_with('Z') {
            step_count += 1;
            let current_instr = match instruction_iter.next() {
                Some(s) => s,
                None => {
                    instruction_iter = directions.chars();
                    instruction_iter.next().unwrap()
                },
            };
            current_step = roadmap.get(current_step).unwrap().next_step(current_instr);
        }
        step_count
    };

    let sol1: u64 = path_len("AAA");
    let sol2: u64 = forks.iter()
        .filter(|f|f.name.ends_with('A'))
        .map(|f|path_len(&f.name))
        .fold(1,lcm);

    (Solution::from(sol1), Solution::from(sol2))
}
