use crate::{Solution, SolutionPair};
use std::fs::read_to_string;

struct Range {
    start:u64,
    end:u64
}

struct MappingRange {
    source:Range,
    destination:Range
}

struct MappingRule {
    name:String,
    ranges:Vec<MappingRange>
}



///////////////////////////////////////////////////////////////////////////////

pub fn solve() -> SolutionPair {
    let lines = read_to_string("/input/day05_1.txt").unwrap();
    let mut line_iter = lines.lines();
    //Parsing, step one: Pull out the Seeds and split to numbers.
    let seed_line = line_iter
        .next()
        .unwrap();
    let seeds:Vec<u64> = seed_line.split(':')
        .nth(1)
        .unwrap()
        .split(' ')
        .map(|x| x.parse::<u64>().unwrap())
        .collect();
    line_iter.next(); //Skip over the initial empty line.
    let mut rules:Vec<MappingRule> = Vec::with_capacity(7);
    let mut temp_lines:Vec<MappingRange> = Vec::new();
    let digits = "0123456789";

    for line in line_iter {
        let first = line.chars().next().unwrap();
        if digits.contains(first) {
            //Number line; make a new mapping range.
            let new_range:Vec<u64> = line.trim().split(" ").map(|x|x.parse::<u64>().unwrap()).collect();
            
        } else if line.trim().len() == 0 {

        } else {

        }
    }

    // Your solution here...
    let sol1: u64 = 0;
    let sol2: u64 = 0;

    (Solution::from(sol1), Solution::from(sol2))
}
