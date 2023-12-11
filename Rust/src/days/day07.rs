use crate::{Solution, SolutionPair};
use std::fs::read_to_string;
use std::collections::HashMap;
use std::cmp::Ordering;
use std::iter::zip;
use core::fmt::Display;

#[derive(PartialEq, Eq, PartialOrd, Ord)]
enum HandRank {
    FiveOfAKind = 10,
    FourOfAKind = 8,
    FullHouse = 6,
    ThreeOfAKind = 4,
    TwoPair = 2,
    OnePair = 1,
    HighCard = 0
}

#[derive(PartialEq, Eq, PartialOrd, Ord)]
struct CamelCard {
    rank:HandRank,
    cards:String,
    bid:u64,
    jokerrank:HandRank
}

impl HandRank {
    fn normal_rank(card_count:&HashMap<char,u8>) -> Self {
        let mut numbs:Vec<u8> = card_count.values().map(|x|*x).collect();
        numbs.sort_unstable();
        match numbs[..] {
            [5] => Self::FiveOfAKind,
            [1,4] => Self::FourOfAKind,
            [2,3] => Self::FullHouse,
            [1,1,3] => Self::ThreeOfAKind,
            [1,2,2] => Self::TwoPair,
            [1,1,1,2] => Self::OnePair,
            _ => Self::HighCard
        }
    }

    fn joker_rank(card_count:&HashMap<char,u8>) -> Self {
        let mut numbs:Vec<u8> = card_count.iter().filter_map(|x|{
            match x.0{
                'J' => None,
                _ => Some(*x.1)
            }
        }).collect();
        numbs.sort_unstable();
        match numbs[..]{
            [_] | [] => Self::FiveOfAKind,
            [1,4] | [1,_] => Self::FourOfAKind,
            [2,3] | [2,2] => Self::FullHouse,
            [1,1,_] => Self::ThreeOfAKind,
            [1,2,2] => Self::TwoPair,
            [1,1,1,2] | [1,1,1,1] => Self::OnePair,
            _ => Self::HighCard
        }
    }
}

impl Display for HandRank{
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        write!(f,"{}",match self {
            HandRank::FiveOfAKind => "Five of a Kind",
            HandRank::FourOfAKind => "Four of a Kind",
            HandRank::FullHouse => "Full House",
            HandRank::ThreeOfAKind => "Three of a Kind",
            HandRank::TwoPair => "Two pairs",
            HandRank::OnePair => "One pair",
            HandRank::HighCard => "High card",
        })
    }
    
}

impl CamelCard {
    fn new(hand:&str,bid:u64) -> Self {
        let mut counts:HashMap<char,u8> = HashMap::new();
        let _:Vec<_> = hand.trim().chars().map(|c|{
            if let Some(prev) = counts.get(&c) {
                counts.insert(c, prev+1)
            } else {
                counts.insert(c,1)
            }
        }).collect();
        Self { rank: HandRank::normal_rank(&counts), cards: String::from(hand), bid: bid, jokerrank: HandRank::joker_rank(&counts) }
    }
}

impl Display for CamelCard {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        write!(f,"Hand of {}; bid of {}. Hand ranks: {}/{}",self.cards,self.bid,self.rank,self.jokerrank)
    }
}


const NORMAL_ORDER:&str = "23456789TJQKA";
const JOKER_ORDER:&str = "J23456789TQKA";

fn compare_cards(hand_l:&CamelCard,hand_r:&CamelCard) -> Ordering {
    match hand_l.rank.cmp(&hand_r.rank) {
        Ordering::Equal => {},
        any => return any,
    };
    for (a,b) in zip(hand_l.cards.chars(),hand_r.cards.chars()) {
        if a == b {
            continue
        }
        let l_val = NORMAL_ORDER.find(a).unwrap_or(0);
        let r_val = NORMAL_ORDER.find(b).unwrap_or(0);
        return l_val.cmp(&r_val);
    }
    Ordering::Equal
}

fn compare_jokers(hand_l:&CamelCard,hand_r:&CamelCard) -> Ordering {
    match hand_l.jokerrank.cmp(&hand_r.jokerrank) {
        Ordering::Equal => {},
        any => return any,
    };
    for (a,b) in zip(hand_l.cards.chars(),hand_r.cards.chars()) {
        if a == b {
            continue
        }
        let l_val = JOKER_ORDER.find(a).unwrap_or(0);
        let r_val = JOKER_ORDER.find(b).unwrap_or(0);
        return l_val.cmp(&r_val);
    }
    Ordering::Equal
}

///////////////////////////////////////////////////////////////////////////////

pub fn solve() -> SolutionPair {
    // Your solution here...
    let mut cards:Vec<CamelCard> = read_to_string("input/day07.txt").unwrap().lines().map(|line|{
        let mut parts = line.trim().split(' ');
        let hand = parts.next().unwrap();
        let bid:u64 = parts.next().unwrap().parse().unwrap();
        CamelCard::new(hand, bid)
    }).collect();

    cards.sort_by(|l,r| compare_cards(l,r));
    let sol1: u64 = cards.iter().enumerate().map(|(r,c)| (r+1) as u64 * c.bid).sum();
    cards.sort_by(|l,r| compare_jokers(l,r));
    let sol2: u64 = cards.iter().enumerate().map(|(r,c)| (r+1) as u64 * c.bid).sum();

    (Solution::from(sol1), Solution::from(sol2))
}
