use crate::{Solution, SolutionPair};
use std::fs::read_to_string;
use std::cmp::max;

///////////////////////////////////////////////////////////////////////////////

struct SingleDraw {
    red:u8,
    green:u8,
    blue:u8
}

struct SingleGame {
    id:u64,
    hands:Vec<SingleDraw>
}

impl SingleDraw {
    fn new() -> Self {
        SingleDraw { red: 0, green: 0, blue: 0 }
    }

    fn parse(line:&str) -> Self {
        let line = line.trim();
        let mut retval = SingleDraw{red:0,green:0,blue:0};
        for part in line.split(|x|x==','||x==';') {
            let count_colour = part.trim();
            let split_point = count_colour.find(' ').unwrap();
            let count = count_colour[0..split_point].parse::<u8>().unwrap();
            match &count_colour[split_point+1..split_point+2] {
                "r" => retval.red = count,
                "g" => retval.green = count,
                "b" => retval.blue = count,
                _ => panic!("Unknown colour!"),
            }
        }
        retval
    }

    fn is_possible(&self,red:u8,green:u8,blue:u8) -> bool {
        self.red <= red && self.green <= green && self.blue <= blue
    }

    fn draw_power(self) -> u64 {
        self.red as u64 * self.green as u64 * self.blue as u64
    }

    fn constrain(&mut self, other: &SingleDraw) -> () {
        self.red = max(self.red,other.red);
        self.blue = max(self.blue,other.blue);
        self.green = max(self.green,other.green);
    }
}

impl SingleGame {
    fn parse(line:&str) -> Option<Self> {
        let colon_index = line.find(":")?;
        let space_index = line.find(" ")?;
        let id = line[space_index+1..colon_index].parse::<u64>().ok()?;
        let mut hands:Vec<SingleDraw> = Vec::new();
        for hand in line[colon_index+1..].split(';') {
            hands.push(SingleDraw::parse(hand));
        }
        Some(SingleGame{id:id,hands:hands})
    }
}

pub fn solve() -> SolutionPair {
    // Your solution here...
    let mut sol1: u64 = 0;
    let mut sol2: u64 = 0;
    let contents:Vec<SingleGame> = 
        read_to_string("input\\day02.txt")
        .unwrap()
        .lines()
        .map(|line| SingleGame::parse(line))
        .filter_map(|game| game)
        .collect();
    for game in contents{
        //star 1: check if each *hand* is valid.
        if game.hands.iter().all(|hand| hand.is_possible(12, 13, 14)){
            sol1 += game.id;
        }
        //star 2: Find the minimal possible configuration.
        let mut running_max = SingleDraw::new();
        let _:Vec<_> = game.hands.iter().map(|hand| running_max.constrain(hand)).collect();
        sol2 += running_max.draw_power();
    }



    (Solution::from(sol1), Solution::from(sol2))
}
