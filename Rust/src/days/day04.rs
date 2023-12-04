use crate::{Solution, SolutionPair};
use std::fs::read_to_string;
use std::collections::HashSet;

///////////////////////////////////////////////////////////////////////////////

fn parse_card(card:&str) -> u64 {
    let colon = card.find(':').unwrap()+1;
    let bar = card.find('|').unwrap();
    let mut winners = HashSet::new();
    let mut found = HashSet::new();
    let mut number = 0;
    let digits = "0123456789";

    for i in card[colon..bar].chars() {
        if digits.contains(i) {
            number = (number * 10) + digits.find(i).unwrap() ;
        }
        else if number > 0 {
            winners.insert(number);
            number = 0;
        }
    }
    if number > 0 {
        winners.insert(number);
    }
    number = 0;

    for i in card[bar+1..].chars() {
        if digits.contains(i) {
            number = (number * 10) + digits.find(i).unwrap() ;
        }
        else if number > 0 {
            found.insert(number);
            number = 0;
        }
    }
    if number > 0 {
        found.insert(number);
    }

    let score = winners.intersection(&found);
    score.collect::<Vec<_>>().len() as u64
}

pub fn solve() -> SolutionPair {
    // Your solution here...
    let card_points:Vec<u64> = read_to_string("input/day04.txt")
        .unwrap()
        .lines()
        .map(|x|parse_card(x))
        .collect();
    let sol1: u64 = card_points.iter()
        .map(|x| match x {0 => 0, _ => 1 << (x-1)})
        .sum();
    //println!("{:?}",card_points);
    let mut card_counts:Vec<u64> = vec![1;card_points.len()];
    for i in 0..card_counts.len(){
        let current_count = card_counts[i];
        let current_score = card_points[i] as usize;
        for j in (i+1)..=(i+current_score){
            card_counts[j] += current_count;
        }
    }
    //println!("{:?}",card_counts);
    let sol2: u64 = card_counts.iter().sum();

    (Solution::from(sol1), Solution::from(sol2))
}
