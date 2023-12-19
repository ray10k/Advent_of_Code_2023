use crate::{Solution, SolutionPair};
use std::fs::read_to_string;

#[derive(PartialEq)]
enum Tile {
    BendJ,
    BendF,
    BendL,
    Bend7,
    StraightH,
    StraightV,
    None
}

#[derive(PartialEq)]
enum Direction {
    North,
    East,
    South,
    West
}

#[derive(PartialEq,Copy,Clone)]
struct Coordinate {
    pub x:usize,
    pub y:usize
}

impl Tile {
    fn from_char(tile:char) -> Self {
        match tile {
            '|' => Self::StraightV,
            '-' => Self::StraightH,
            'L' => Self::BendL,
            'F' => Self::BendF,
            'J' => Self::BendJ,
            '7' => Self::Bend7,
            _ => Self::None,
        }
    }

    fn from_directions(left:&Direction,right:&Direction) -> Self {
        match (left,right) {
            (Direction::North,Direction::East)|(Direction::East,Direction::North)=> Self::BendL,
            (Direction::North,Direction::South)|(Direction::South,Direction::North) => Self::StraightV,
            (Direction::North,Direction::West)|(Direction::West,Direction::North) => Self::BendJ,
            (Direction::East,Direction::South)|(Direction::South,Direction::East) => Self::BendF,
            (Direction::East,Direction::West)|(Direction::West,Direction::East) => Self::StraightH,
            (Direction::South,Direction::West)|(Direction::West,Direction::South) => Self::Bend7,
            _ => Self::None
        }
    }

    fn directions(&self) -> Option<(Direction,Direction)> {
        match self {
            Tile::BendJ => Some((Direction::North,Direction::West)),
            Tile::BendF => Some((Direction::South,Direction::East)),
            Tile::BendL => Some((Direction::North,Direction::East)),
            Tile::Bend7 => Some((Direction::South,Direction::West)),
            Tile::StraightH => Some((Direction::East,Direction::West)),
            Tile::StraightV => Some((Direction::North,Direction::South)),
            Tile::None => None,
        }
    }

    fn turn(&self,in_direction:Direction) -> Option<Direction> {
        if let Some(dirs) = self.directions() {
            Some(
                if dirs.1 == in_direction {
                    dirs.0
                } else {
                    dirs.1
                }
            )
        } else {
            None
        }
    }
}

impl Direction {
    fn step(&self,start:&Coordinate) -> Coordinate {
        let mut copy = start.clone();
        copy.step(self);
        copy
    }

    fn opposite(&self) -> Self {
        match self {
            Direction::North => Direction::South,
            Direction::East => Direction::West,
            Direction::South => Direction::North,
            Direction::West => Direction::East,
        }
    }
}

impl Coordinate {
    fn new() -> Self {
        Self { x: 0, y: 0 }
    }

    fn from_xy(x:usize,y:usize) -> Self {
        Self { x:x, y:y }
    }

    fn step(&mut self, dir:&Direction) -> () {
        match dir{
            Direction::North => self.y -= 1,
            Direction::East => self.x += 1,
            Direction::South => self.y += 1,
            Direction::West => self.x -= 1,
        }
    }
    fn adjacent(&self,max_h:usize,max_v:usize) -> Vec<Coordinate>{
        let mut retval = Vec::<Coordinate>::new();
        if self.x > 0 {
            retval.push(Self { x: self.x-1, y: self.y });
        }
        if self.x < max_h {
            retval.push(Self { x: self.x+1, y: self.y });
        }
        if self.y > 0 {
            retval.push(Self { x: self.x, y: self.y-1 });
        }
        if self.y < max_v {
            retval.push(Self { x: self.x, y: self.y+1 });
        }
        return retval;
    }
}

///////////////////////////////////////////////////////////////////////////////

pub fn solve() -> SolutionPair {
    let pipe_map:Vec<String> = read_to_string("input/day10.txt").unwrap().trim().lines().map(|x|String::from(x)).collect();
    let start_coords = pipe_map.iter().enumerate().find(|x|x.1.contains('S')).map(|x|(x.1.find('S').unwrap(),x.0)).unwrap();
    let start_coords = Coordinate::from_xy(start_coords.0, start_coords.1);
    let (max_h,max_v) = (pipe_map[0].len(),pipe_map.len());
    let mut tile_map:Vec<Vec<Tile>> = pipe_map.iter().map(|x|x.trim()).map(|x|x.chars().map(|c|Tile::from_char(c)).collect::<Vec<Tile>>()).collect();
    // Find what kind of bend the starting tile is.
    let surrounding = start_coords.adjacent(max_h, max_v);
    let start_pipe:Vec<Direction> = surrounding.iter()
        .map(|tile|&tile_map[tile.y][tile.x])
        .filter_map(|pipe|pipe.directions())
        .filter_map(|x|{
            let (end1,end2) = (x.0.step(&start_coords),x.1.step(&start_coords));
            if end1 == start_coords {
                Some(x.0.opposite())
            } else if end2 == start_coords {
                Some(x.1.opposite())
            } else {
                None
            } 
        }).collect();
    assert_eq!(start_pipe.len(),2);
    tile_map[start_coords.y][start_coords.x] = Tile::from_directions(&start_pipe[0], &start_pipe[1]);



    // Your solution here...
    let sol1: u64 = 0;
    let sol2: u64 = 0;

    (Solution::from(sol1), Solution::from(sol2))
}
