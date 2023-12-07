from pathlib import Path
from time import perf_counter_ns
from typing import NamedTuple
from collections import Counter

INPUT_NAME = "day07_1.txt"
INPUT_PATH = Path(__file__).parent.parent.parent / "input" / INPUT_NAME
CARD_ORDER = {rank:value for value,rank in enumerate("23456789TJQKA")}

def hand_rank(hand:str) -> int:
    counts = Counter(hand)
    matches = sorted((x for x in counts.values()),reverse=True)
    print(f"{hand} -> {matches}")
    if matches == [5]:
        return 6
    if matches == [4,1]:
        return 5
    if matches == [3,2]:
        return 4
    if matches == [3,1,1]:
        return 3
    if matches == [2,2,1]:
        return 2
    if matches == [2,1,1,1]:
        return 1
    return 0

class CardHand(NamedTuple):
    cards:str
    bid:int
    rank:int
    
    def __gt__(self, __value: "CardHand") -> bool:
        if self.rank != __value.rank:
            return self.rank > __value.rank
        for s,o in zip(self.cards,__value.cards):
            if s == o:
                continue
            return CARD_ORDER[s] > CARD_ORDER[o]
        return False
    
    def __ge__(self, __value: "CardHand") -> bool:
        if self.rank != __value.rank:
            return self.rank > __value.rank
        for s,o in zip(self.cards,__value.cards):
            if s == o:
                continue
            return CARD_ORDER[s] > CARD_ORDER[o]
        return True
    
    def __eq__(self, __value: "CardHand") -> bool:
        return self.cards == __value.cards
    
    def __repr__(self) -> str:
        return f"{self.cards},{self.bid}. Rank {self.rank}"
    
    @classmethod
    def from_line(cls,line:str):
        parts = line.split(" ")
        rank = hand_rank(parts[0])
        return CardHand(parts[0],int(parts[1]),rank)
        
def parse_line(line:str) -> CardHand|None:
    """ Parse one line of the input into an 'object' for the solution.
    If a line should be discarded, return None instead. """
    line = line.strip()
    if line == "":
        return None
    return CardHand.from_line(line)

def parse_input(file_path = INPUT_PATH):
    """ Loads the given file, and parses it line-by-line. Should return
    some useful representation of the input. """
    parsed_input = None
    if file_path.exists():
        with open(file_path) as input_file:
            parsed_input = tuple(parse_line(line) for line in input_file)
    return tuple(x for x in parsed_input if x is not None)

def solution_one(parsed_input:tuple[CardHand,...]) -> str:
    """ Takes the (parsed) input of the puzzle and uses it to solve for
    the first star of the day. """
    ordered_cards = sorted(parsed_input)
    total_winnings = sum(card.bid * order for order,card in enumerate(ordered_cards,start = 1))
    print("\n".join(repr(card) for card in ordered_cards))
    return str(total_winnings)

def solution_two(parsed_input:tuple) -> str:
    """ Takes the (parsed) input of the puzzle and uses it to solve for
    the second star of the day. """
    return ""

def solve_day() -> tuple[float,float,float]:
    times = [0,0,0,0]
    times[0] = perf_counter_ns()
    parsed_input = parse_input()
    times[1] = perf_counter_ns()
    result_one = solution_one(parsed_input)
    times[2] = perf_counter_ns()
    result_two = solution_two(parsed_input)
    times[3] = perf_counter_ns()

    time_parse = (times[1] - times[0]) / 1_000_000
    time_one = (times[2] - times[1]) / 1_000_000
    time_two = (times[3] - times[2]) / 1_000_000
    time_total = (times[3] - times[0]) / 1_000_000
    print(f"=== Day 07 ===\n  · Part 1: {result_one}\n  · Part 2: {result_two}\n  · Time: {time_parse}; {time_one}; {time_two}; {time_total}")
    return time_one, time_two, time_total

if __name__ == "__main__":
    solve_day()
