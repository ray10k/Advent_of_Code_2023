use crate::{Solution, SolutionPair};
use std::fs::read_to_string;
use std::cmp::{max,min};

///////////////////////////////////////////////////////////////////////////////

struct Part {
    shape:char,
    numbers:Vec<u32>
}

pub fn solve() -> SolutionPair {
    let text:Vec<Vec<char>> = read_to_string("input\\day03.txt")
        .unwrap()
        .lines()
        .map(
            |x| x.chars()
            .collect::<Vec<char>>())
        .collect();
    // Your solution here...
    let height = text.len()-1;
    let width = text[0].len()-1;
    let digits = "0123456789";
    let not_parts = "0123456789.";
    let mut parts:Vec<Part> = Vec::new();

    for (y,line) in text.iter().enumerate() {
        for (x,character) in line.iter().enumerate() {
            if !not_parts.contains(*character) {
                //Current character is a part marker.
                //look around the current character's location.
                let top = max(0,y-1);
                let bottom = min(height,y+1);
                let left = max(0,x-1);
                let right = min(width,x+1);
                let mut numbers:Vec<u32> = Vec::new();
                for vertical in top..=bottom {
                    let current_line = &text[vertical];
                    let mut horizontal = left;
                    while horizontal <= right {
                        if digits.contains(current_line[horizontal]) {
                            //Step left until either hitting x=zero, or finding a non-digit.
                            
                            let num_left = (0..=horizontal).rev().take_while(|l| digits.contains(current_line[*l])).last().unwrap_or(0);
                            let num_right = (horizontal..=width).take_while(|r| digits.contains(current_line[*r])).last().unwrap_or(width);
                            numbers.push(
                                current_line[num_left..=num_right].iter()
                                .collect::<String>()
                                .parse::<u32>()
                                .unwrap()
                            );
                            horizontal = num_right;
                        }
                        horizontal += 1;
                    }
                }
                let newpart = Part {shape: *character, numbers: numbers};
                parts.push(newpart);
            }
        }
    }

    let sol1: u32 = {
        parts.iter()
        .map(
            |p|p.numbers.iter()
            .sum::<u32>())
        .sum::<u32>()
    };
    let sol2: u32 = {
        parts.iter()
        .filter(
            |p| p.shape == '*' && p.numbers.len() == 2
        )
        .map(
            |p| p.numbers[0] * p.numbers[1]
        )
        .sum()
    };

    (Solution::from(sol1), Solution::from(sol2))
}
