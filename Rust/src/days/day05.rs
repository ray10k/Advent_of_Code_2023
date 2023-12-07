use crate::{Solution, SolutionPair};
use std::fs::read_to_string;
use std::cmp::{min, max};

#[derive(Copy,Clone)]
struct Range {
    start:u64,
    end:u64
}

struct MappingRange {
    source:Range,
    offset:i64
}

struct MappingRule {
    pub name:String,
    ranges:Vec<MappingRange>
}

impl Range {
    fn from_length(start:u64,length:u64) -> Self{
        Range { start: start, end: (start+length)-1 }
    }

    fn contains(&self,number:u64) -> bool {
        self.start >= number && self.end <= number
    }

    fn overlaps(&self,other:&Range) -> bool {
        (self.start <= other.start && self.end >= other.end) || 
        (self.start >= other.start && self.start <= other.end) ||
        (self.end >= other.start && self.end <= other.end)
    }

    fn combine(&self,other:&Range) -> Option<Range> {
        if !self.overlaps(other) {
            None
        } else {
            Some(Range { start: min(self.start,other.start), end: max(self.end,other.end) })
        }
    }

    fn split(&self,split_point:u64) -> (Self,Option<Self>) {
        if split_point > self.end || split_point < self.start {
            return (self.clone(),None)
        }
        (Range{start:self.start,end:split_point},Some(Range{start:split_point+1,end:self.end}))
    }

    fn subrange(&self,other:&Range) -> (Option<Self>,Option<Self>,Option<Self>) {
        if ! self.overlaps(other) {
            (Some(self.clone()),None,None)
        } else {
            if self.contains(other.start) && self.contains(other.end) {
                (None,Some(other.clone()),None)
            } else if other.contains(self.start) && other.contains(self.end) {
                let (left,middle) = other.split(self.start);
                let (middle,right) = middle.unwrap().split(self.end);
                (Some(left),Some(middle),right)
            } else if other.contains(self.start) {
                let (left,right) = other.split(self.start);
                (right,Some(left),None)
            } else {
                let (left,right) = self.split(other.start);
                (Some(left),right,None)
            }
        }
    }

    fn offset(&self,offset:i64) -> Range {
        Range{start: (self.start as i64 + offset) as u64, end: (self.end as i64 + offset) as u64}
    }
}

impl PartialEq for Range {
    fn eq(&self, other: &Self) -> bool {
        self.start == other.start
    }
}

impl PartialOrd for Range {
    fn partial_cmp(&self, other: &Self) -> Option<std::cmp::Ordering> {
        return self.start.partial_cmp(&other.start) 
    }
}

impl MappingRange {
    fn from_ranges(d_start:u64, s_start:u64, length:u64) -> Self {
        let offset = d_start as i64 - s_start as i64;
        MappingRange { source: Range::from_length(s_start, length), offset: offset }
    }

    fn map_number(&self, to_map:u64) -> u64 {
        if self.source.contains(to_map) {
            (to_map as i64 + self.offset) as u64
        } else {
            to_map
        }
    }

    fn map_range(&self, to_map:&Range) -> (Option<Range>,Option<Range>,Option<Range>) {
        let (left,mut midd,right) = self.source.subrange(to_map);
        if let Some(mid) = midd {
            midd = Some(mid.offset(self.offset));
        }
        (left,midd,right)
    }

    fn will_map(&self, to_check:u64) -> bool {
        self.source.contains(to_check)
    }
}

impl MappingRule {
    fn new(name:&str, rules:Vec<MappingRange>) -> Self {
        MappingRule { name: String::from(name), ranges: Vec::<MappingRange>::from(rules) }
    }

    fn map_number(&self, to_map:u64) -> u64 {
        for mapping in self.ranges.iter() {
            if mapping.will_map(to_map) {
                return mapping.map_number(to_map)
            }
        }

        to_map
    }
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
