use crate::{Solution, SolutionPair};
use std::{fs::read_to_string, iter::zip,cmp::{min,max}};

///////////////////////////////////////////////////////////////////////////////

struct RaceStats{
    time:i64,
    distance:i64
}

impl RaceStats {
    fn record_times(&self) -> (u64,u64) {
        //The formula (t-x)*x can also be written 0+tx-x**2.
        //t is the max time, and by subtracting (distance+1)
        //from the result, we get a quadratic formula 
        //-d+tx-x**2 which is 0 at the hold-times where the
        //resulting distance is greater than the record.
        let a = -1.0;
        let b = self.time as f64;
        let c = -(self.distance + 1) as f64;
        let d = f64::sqrt((b*b)- (4.0*a*c));
        let first = (-b + d) / (2.0*a);
        let second = (-b - d) / (2.0*a);
        (first.ceil() as u64,second.floor() as u64)
    }
}

pub fn solve() -> SolutionPair {
    // Your solution here...
    let lines:Vec<String> = read_to_string("input/day06.txt").unwrap().lines().map(|line| String::from(line)).collect();

    let mut full_time:String = String::from("");
    let mut full_dist:String = String::from("");
    let times:Vec<i64> = {
        let start = lines[0].find(':').unwrap();
        let mut relevant = lines[0][start+1..].trim();
        let mut retval:Vec<i64> = Vec::new();
        loop {
            let first_space = relevant.find(' ').unwrap_or(relevant.len());
            if &relevant[0..first_space] == "" {
                break;
            }
            full_time.push_str(&relevant[0..first_space]);
            retval.push(i64::from_str_radix(&relevant[0..first_space], 10).unwrap());
            relevant = relevant[first_space..].trim();
        }
        retval
    };
    let distances:Vec<i64> = {
        let start = lines[1].find(':').unwrap();
        let mut relevant = lines[1][start+1..].trim();
        let mut retval:Vec<i64> = Vec::new();
        loop {
            let first_space = relevant.find(' ').unwrap_or(relevant.len());
            if &relevant[0..first_space] == "" {
                break;
            }
            full_dist.push_str(&relevant[0..first_space]);
            retval.push(i64::from_str_radix(&relevant[0..first_space], 10).unwrap());
            relevant = relevant[first_space..].trim();
        }
        retval
    };
    
    let races:Vec<RaceStats> = zip(times,distances)
        .map(|pair| RaceStats{time:pair.0,distance:pair.1})
        .collect();
    let bigrace = RaceStats{
        time:i64::from_str_radix(&full_time[0..], 10).unwrap(),
        distance:i64::from_str_radix(&full_dist[0..], 10).unwrap()
    };

    let sol1: u64 = races.iter()
        .map(|r| r.record_times())
        .map(|(up,down)| (max(up,down) - min(up,down)) + 1)
        .product();
    let (bigfirst,bigsecond) = bigrace.record_times();
    let sol2: u64 = (max(bigfirst,bigsecond) - min(bigfirst,bigsecond))+1;

    (Solution::from(sol1), Solution::from(sol2))
}
