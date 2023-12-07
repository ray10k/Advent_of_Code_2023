from pathlib import Path
from time import perf_counter_ns
from typing import NamedTuple
from collections import Counter

INPUT_NAME = "day07.txt"
INPUT_PATH = Path(__file__).parent.parent.parent / "input" / INPUT_NAME
CARD_ORDER = {rank:value for value,rank in enumerate("23456789TJQKA")}
CARD_JOKER = {rank:value for value,rank in enumerate("J23456789TQKA")}

def hand_rank(hand:str) -> int:
    counts = Counter(hand)
    matches = sorted((x for x in counts.values()),reverse=True)
    if matches == [5]: #5 of a kind!?
        return 6
    if matches == [4,1]: #4 of a kind
        return 5
    if matches == [3,2]: #Full house!
        return 4
    if matches == [3,1,1]: #3 of a kind
        return 3
    if matches == [2,2,1]: #Two pairs
        return 2
    if matches == [2,1,1,1]: #single pair
        return 1
    return 0 #Any

def joker_rank(hand:str) -> int:
    counts = Counter(hand)
    jokers = counts.get("J",0)
    matches = sorted((y for x,y in counts.items() if x != "J"),reverse=True)
    
    if jokers == 5:
        return 6 # 5 of a kind
    
    if len(matches) == 1:
        if matches[0] + jokers == 5:
            return 6 # 5 of a kind, again?
        
    if len(matches) == 2:
        if matches[0] + jokers == 4:
            return 5 # 4 of a kind!
        if (matches == [2,2] and jokers == 1) or matches == [3,2]:
            return 4 # Full house!
    
    if len(matches) == 3:
        if matches[1] == 1 and matches[2] == 1:
            return 3 # 3 of a kind.
        if matches == [2,2,1]:
            return 2 # two pairs.
        
    if len(matches) == 4:
        return 1 # single pair.
    
    return 0 #Any


class CardHand(NamedTuple):
    cards:str
    bid:int
    rank:int
    joker_rank:int

    def hand_strength(self,jokers=False) -> int:
        running_total = 0
        for position,character in enumerate(self.cards[::-1]):
            running_total += (13 ** position) * (CARD_JOKER[character] if jokers else CARD_ORDER[character])
        running_total += (13 ** (len(self.cards)+1)) * (self.joker_rank if jokers else self.rank)
        return running_total
    
    def __repr__(self) -> str:
        return f"{self.cards},{self.bid}. Rank {self.rank}; Strength {self.hand_strength()}/{self.hand_strength(True)}"
    
    @classmethod
    def from_line(cls,line:str):
        parts = line.split(" ")
        rank = hand_rank(parts[0])
        j_rank = joker_rank(parts[0])
        return CardHand(parts[0],int(parts[1]),rank,j_rank)
        
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
    ordered_cards = sorted(parsed_input,key=lambda x: x.hand_strength())
    total_winnings = sum(card.bid * order for order,card in enumerate(ordered_cards,start = 1))
    return str(total_winnings)

def solution_two(parsed_input:tuple[CardHand,...]) -> str:
    """ Takes the (parsed) input of the puzzle and uses it to solve for
    the second star of the day. """
    ordered_cards = sorted(parsed_input,key=lambda x: x.hand_strength(True))
    total_winnings = sum(card.bid * order for order,card in enumerate(ordered_cards,start=1))
    return str(total_winnings)

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
