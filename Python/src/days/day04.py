from pathlib import Path
from time import perf_counter_ns
from typing import NamedTuple

INPUT_NAME = "day04.txt"
INPUT_PATH = Path(__file__).parent.parent.parent / "input" / INPUT_NAME

class Scratchcard(NamedTuple):
    card_id:int
    winning:frozenset[int]
    found:frozenset[int]
    
    def total_score(self) -> int:
        overlap = self.winning & self.found
        if len(overlap) == 0:
            return 0
        return 1 << (len(overlap)-1)
    
    def points(self) -> int:
        overlap = self.winning & self.found
        return len(overlap)
    
    def __repr__(self) -> str:
        return f"Card {self.card_id}: {''.join(f' {x:> 2}' for x in self.winning)} | {''.join(f' {x:> 2}' for x in self.found)}; {self.total_score()}"

def parse_line(line:str):
    """ Parse one line of the input into an 'object' for the solution.
    If a line should be discarded, return None instead. """
    line = line.strip()
    if line == "":
        return None
    space = line.index(' ')+1
    colon = line.index(':')
    bar = line.index('|')
    id = int(line[space:colon])
    #print(*(number for number in line[colon+1:bar].split(' ')))
    winners = frozenset(int(number.strip()) for number in line[colon+1:bar].split(' ') if number.strip() != "")
    found = frozenset(int(number.strip()) for number in line[bar+1:].split(' ') if number.strip() != "")
    
    return Scratchcard(id,winners,found)

def parse_input(file_path = INPUT_PATH):
    """ Loads the given file, and parses it line-by-line. Should return
    some useful representation of the input. """
    parsed_input = None
    if file_path.exists():
        with open(file_path) as input_file:
            parsed_input = tuple(parse_line(line) for line in input_file)
    return tuple(x for x in parsed_input if x is not None)

def solution_one(parsed_input:tuple[Scratchcard,...]) -> str:
    """ Takes the (parsed) input of the puzzle and uses it to solve for
    the first star of the day. """
    
    return str(sum(card.total_score() for card in parsed_input))

def solution_two(parsed_input:tuple[Scratchcard,...]) -> str:
    """ Takes the (parsed) input of the puzzle and uses it to solve for
    the second star of the day. """
    #We got lanternfish'd.
    card_counts = [1] * len(parsed_input)
    
    for i,card in enumerate(parsed_input):
        score = card.points()
        #print(f"{i}: {card_counts}, {score}")
        if score == 0:
            continue
        copies = card_counts[i]
        stop_at = min(len(parsed_input),i+score+1)
        for j in range(i+1,stop_at):
            card_counts[j] += copies
    
    #print(card_counts)
    return str(sum(card_counts))

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
    print(f"=== Day 04 ===\n  · Part 1: {result_one}\n  · Part 2: {result_two}\n  · Time: {time_parse}; {time_one}; {time_two}; {time_total}")
    return time_one, time_two, time_total

if __name__ == "__main__":
    solve_day()
