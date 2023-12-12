use crate::{Solution, SolutionPair};
use std::fs::read_to_string;

fn list_results(initial:&Vec<i64>) -> (i64,i64) {
    let mut current = initial.clone();
    let mut sides:Vec<(i64,i64)> = Vec::with_capacity(initial.len());
    let all_done = |x:&Vec<i64>|x.len() == 0 || x.iter().all(|i|i == &0);
    while !all_done(&current) {
        sides.push((*current.first().unwrap(),*current.last().unwrap()));
        let mut next:Vec<i64> = Vec::with_capacity(current.len()-1);
        for window in current.windows(2) {
            next.push(window[1] - window[0]);
        }
        current = next;
    }
    //sides.push((0,0));
    sides.iter().rev().fold((0,0),|acc,ele|{
        (ele.0 - acc.0 ,acc.1 + ele.1)
    })
}

///////////////////////////////////////////////////////////////////////////////

pub fn solve() -> SolutionPair {
    // Your solution here...
    let initial_states:Vec<Vec<i64>> = read_to_string("input/day09.txt").unwrap()
        .lines()
        .map(|l|l.trim())
        .filter(|l|l.len() > 0)
        .map(|l|{
            l.split(' ')
                .map(|num| num.parse::<i64>().unwrap_or(i64::MIN))
                .collect::<Vec<i64>>()
        })
        .collect();
    let (sol2,sol1) = initial_states.iter()
        .map(|s|list_results(s))
        .fold((0,0),|acc,ele|(acc.0+ele.0,acc.1+ele.1));
    (Solution::from(sol1), Solution::from(sol2))
}
