use crate::{Solution, SolutionPair};
use std::fs::read_to_string;
use std::collections::HashSet;

///////////////////////////////////////////////////////////////////////////////

fn delta(left:usize, right:usize) -> usize {
    if left < right {
        right - left
    } else {
        left - right
    }
}

fn distance(left:&(usize,usize),right:&(usize,usize)) -> usize {
    delta(left.0,right.0) + delta(left.1,right.1)
}

pub fn solve() -> SolutionPair {
    let starchart:Vec<String> = read_to_string("input/day11.txt").unwrap().lines().map(|l| String::from(l.trim())).collect();
    let mut empty_collumns:HashSet<usize> = HashSet::from_iter(0..starchart[0].len());
    let mut empty_rows:HashSet<usize> = HashSet::from_iter(0..starchart.len());
    let mut galaxies:HashSet<(usize,usize)> = HashSet::new();

    //println!("{empty_collumns:?} {empty_rows:?}");

    for (row,line) in starchart.iter().enumerate() {
        for (col,ch) in line.chars().enumerate() {
            if ch != '.' {
                empty_collumns.remove(&col);
                empty_rows.remove(&row);
                galaxies.insert((col,row));
            }
        }
    }

    let mut young_galaxies: Vec<(usize,usize)> = Vec::with_capacity(galaxies.len());
    let mut old_galaxies: Vec<(usize,usize)> = Vec::with_capacity(galaxies.len());

    for galaxy in galaxies.iter() {
        let off_x = empty_collumns.iter().filter(|x| x < &&galaxy.0).count();
        let off_y = empty_rows.iter().filter(|y| y < &&galaxy.1).count();
        young_galaxies.push((galaxy.0 + off_x,galaxy.1 + off_y));
        old_galaxies.push((galaxy.0 + (off_x * 999_999), galaxy.1 + (off_y * 999_999)));
    }

    let mut sol1: usize = 0;
    let mut sol2: usize = 0;
    for x in 0..young_galaxies.len()-1 {
        let young = &young_galaxies[x];
        let old = &old_galaxies[x];
        for y in x+1..young_galaxies.len() {
            let o_young = &young_galaxies[y];
            let o_old = &old_galaxies[y];
            sol1 += distance(young,o_young);
            sol2 += distance(old,o_old);
        }
    }

    (Solution::from(sol1), Solution::from(sol2))
}
