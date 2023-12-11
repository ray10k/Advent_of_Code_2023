use crate::{Solution, SolutionPair};
use std::fs::read_to_string;
use std::cmp::min;
use std::fmt::{Formatter,Display,Result as fmtResult};

#[derive(Copy,Clone,Debug, Eq,Ord)]
struct Range {
    start:u64,
    end:u64
}

#[derive(Eq,Ord,Copy,Clone,Debug)]
struct MappingRange {
    source:u64,
    offset:i64
}

#[derive(Debug)]
struct MappingRule {
    pub name:String,
    ranges:Vec<MappingRange>
}

impl Range {
    fn from_length(start:u64,length:u64) -> Self {
        Range { start: start, end: (start+length)-1 }
    }

    fn from_start_end(start:u64,end:u64) -> Self {
        Range { start: start, end: end}
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
    fn from_start_offset(start:u64,offset:i64) -> Self {
        MappingRange { source: start, offset: offset }
    }

    fn map_number(&self, to_map:u64) -> u64 {
        if to_map >= self.source {
            (to_map as i64 + self.offset) as u64
        } else {
            to_map
        }
    }

    fn map_range(&self, to_map:&Range) -> (Option<Range>,Option<Range>) {
        if to_map.end < self.source {
            (Some(to_map.clone()),None)
        } else if to_map.start < self.source {
            let other = Range::from_start_end(self.map_number(self.source),self.map_number(to_map.end));
            (Some(Range::from_start_end(to_map.start,self.source-1)),Some(other))
        } else {
            let other = Range::from_start_end(self.map_number(to_map.start), self.map_number(to_map.end));
            (None,Some(other))
        }
    }

    fn will_map(&self, to_check:u64) -> bool {
        self.source <= to_check
    }
}

impl PartialEq for MappingRange {
    fn eq(&self, other: &Self) -> bool {
        self.source == other.source && self.offset == other.offset
    }
}

impl PartialOrd for MappingRange {
    fn partial_cmp(&self, other: &Self) -> Option<std::cmp::Ordering> {
        //For sorting, I need negative offsets to be greater than 0 offsets.
        //ugly hack
        match self.source.partial_cmp(&other.source) {
            Some(core::cmp::Ordering::Equal) => {}
            ord => return ord,
        }
        i64::abs(self.offset).partial_cmp(&i64::abs(other.offset))
    }
}

impl MappingRule {
    fn new(name:&str, rules:Vec<MappingRange>) -> Self {
        MappingRule { name: String::from(name), ranges: Vec::<MappingRange>::from(rules) }
    }

    fn map_number(&self, to_map:u64) -> u64 {
        //Look backwards along the list for the last range that includes the
        //given number, and map.
        for mapping in self.ranges.iter().rev() {
            if mapping.will_map(to_map) {
                return mapping.map_number(to_map);
            }
        }

        to_map
    }

    fn map_range(&self, to_map:&Range) -> Vec<Range> {
        if self.ranges.len() == 0 {
            return vec![to_map.clone()]
        }
        //Starting from the *end* of the list of ranges, first find the
        // range in which the *end* of the range-to-map is included, then
        // work backwards to the first range that splits to a single 
        // range.
        let mut remainder:Option<Range> = Some(to_map.clone());
        let mut rng_iter = self.ranges.iter().rev();
        let mut retval:Vec<Range> = Vec::new();

        while let Some(next_up) = remainder {
            let rng = match rng_iter.next() {
                Some(x) => x,
                None => return retval,
            };
            let result = rng.map_range(&next_up);
            remainder = result.0;
            if let Some(mapped) = result.1 {
                retval.push(mapped);
            }
        }
        retval
    }
}

impl Display for MappingRule {
    fn fmt(&self, f: &mut Formatter) -> fmtResult {
        writeln!(f,"Rule {}",self.name)?;
        for step in self.ranges.iter() {
            write!(f,"{} ({});",step.source,step.offset)?;
        }
        fmtResult::Ok(())
    }
}
///////////////////////////////////////////////////////////////////////////////

pub fn solve() -> SolutionPair {
    let lines = read_to_string("input/day05.txt").unwrap();
    let mut line_iter = lines.lines();
    //Parsing, step one: Pull out the Seeds and split to numbers.
    let seed_line = line_iter
        .next()
        .unwrap();
    let seeds:Vec<u64> = seed_line.split(':')
        .nth(1)
        .unwrap()
        .split(' ')
        .filter(|x|x.len() > 0)
        .map(|x| x.parse::<u64>().unwrap())
        .collect();
    line_iter.next(); //Skip over the initial empty line.
    let mut rules:Vec<MappingRule> = Vec::with_capacity(7);
    let mut temp_lines:Vec<MappingRange> = Vec::new();
    let mut current_name:String = String::from("");
    let digits = "0123456789";

    for line in line_iter {
        if line.trim().len() == 0 {
            //Empty line; 'compile' mapping ranges and make a MappingRule.
            temp_lines.sort_unstable();
            //It is possible that one range starts right where another ends. Double-check
            // and remove the 0-offset Rules from the collection.
            let mut deduped_ranges:Vec<MappingRange> = temp_lines.windows(2)
                .filter(|window|window[0].source != window[1].source && window[0].offset != window[1].offset)
                .map(|x|x[0])
                .collect();
            deduped_ranges.push(temp_lines.pop().unwrap());
            if deduped_ranges[0].source != 0 {
                deduped_ranges.insert(0,MappingRange{source:0,offset:0});
            }
            rules.push(MappingRule::new(&current_name,deduped_ranges));
            temp_lines.clear();
            continue;
        }
        let first = line.chars().next().unwrap();
        if digits.contains(first) {
            //Number line; make a new mapping range.
            let new_range:Vec<u64> = line.trim().split(" ").map(|x|x.parse::<u64>().unwrap()).collect();

            let dest = new_range[0];
            let src = new_range[1];
            let len = new_range[2];

            let offset = dest as i64 - src as i64;
            let end = src+len;
            temp_lines.push(MappingRange::from_start_offset(src, offset));
            temp_lines.push(MappingRange::from_start_offset(end, 0));
        } else {
            //Non-number line; name for the new rule.
            current_name = String::from(&line[0..line.find(' ').unwrap()])
        }
    }
    temp_lines.sort_unstable();
    let mut deduped_ranges:Vec<MappingRange> = temp_lines.windows(2)
        .filter(|window|window[0].source != window[1].source || window[0].offset > window[1].offset)
        .map(|x|x[0])
        .collect();
    if deduped_ranges[0].source != 0 {
        deduped_ranges.push(MappingRange::from_start_offset(0, 0));
    }
    rules.push(MappingRule::new(&current_name,deduped_ranges));


    let seed_ranges:Vec<Range> = seeds.chunks(2).map(|x|Range::from_length(x[0],x[1])).collect();

    // Your solution here...
    let sol1: u64 = seeds.iter()
        .map(|x|{
            rules.iter()
            .fold(*x, |acc,ele| ele.map_number(acc))
        }).fold(u64::MAX,|acc,ele|min(acc, ele));
    let sol2: u64 = seed_ranges.iter()
        .map(|rn|{
            let mut active_ranges:Vec<Range> = vec![*rn];
            for rule in rules.iter() {
                let temp:Vec<Range> = active_ranges.iter().map(|rg|rule.map_range(rg)).flatten().collect();
                active_ranges = temp;
            }
            active_ranges.sort_unstable();
            active_ranges[0].start
        }).min().unwrap_or(u64::MAX);

    (Solution::from(sol1), Solution::from(sol2))
}
