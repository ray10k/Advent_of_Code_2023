use crate::{Solution, SolutionPair};
use std::fs::read_to_string;
use std::collections::HashMap;

fn check_line(line:&str,matches:&Vec<(&str,u64)>) -> u64 {
    for begin in matches {
        if line.starts_with(begin.0) {
            return begin.1;
        }
    }
    return 0;
}

///////////////////////////////////////////////////////////////////////////////

pub fn solve() -> SolutionPair {
    // Your solution here...
    let input_contents = read_to_string("input/day01.txt")
        .unwrap();
    let input_lines:Vec<&str> = input_contents
        .split("\r\n")
        .collect();
    //Star one
    let is_num = |x:char| {"123456789".contains(x)};
    let digit_to_num = |x:char| {x as u64 - 48};
    let mut sol1: u64 = 0;
    for line in input_lines.iter() {
        let first= line.find(is_num).unwrap_or(0);        
        let last = line.rfind(is_num).unwrap_or(0);
        let characters:Vec<char> = line.chars().collect();
        sol1 += (digit_to_num(characters[first]))*10;
        sol1 += digit_to_num(characters[last]);
    }

    //Star two
    let can_start = |x:(usize,char)|{
        match "123456789otfsen".contains(x.1) {
            true => Some(x.0),
            false => None
        }
    };
    let words = HashMap::from([
        ('o',vec![("one",1)]),
        ('t',vec![("two",2),("three",3)]),
        ('f',vec![("four",4),("five",5)]),
        ('s',vec![("six",6),("seven",7)]),
        ('e',vec![("eight",8)]),
        ('n',vec![("nine",9)])
    ]);
    let mut sol2: u64 = 0;
    for line in input_lines.iter(){
        let starting_points:Vec<usize> = line.chars().enumerate().filter_map(can_start).collect();
        let characters:Vec<char> = line.chars().collect();
        sol2 += {
            let mut retval = 0;
            for begin in starting_points.iter() {
                if is_num(characters[*begin]) {
                    retval = digit_to_num(characters[*begin]);
                    break;
                }
                let patt = words.get(&characters[*begin]).unwrap();
                let l_val = check_line(&line[*begin..], patt);
                if l_val != 0 {
                    retval = l_val;
                    break;
                }
            }
            retval
        } * 10;
        sol2 += {
            let mut retval = 0;
            for begin in starting_points.iter().rev() {
                if is_num(characters[*begin]) {
                    retval = digit_to_num(characters[*begin]);
                    break;
                }
                let patt = words.get(&characters[*begin]).unwrap();
                let l_val = check_line(&line[*begin..], patt);
                if l_val != 0 {
                    retval = l_val;
                    break;
                }
            }
            retval
        }
    }

    (Solution::from(sol1), Solution::from(sol2))
}
