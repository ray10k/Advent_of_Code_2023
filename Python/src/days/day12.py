from pathlib import Path
from time import perf_counter_ns
from typing import NamedTuple
from functools import cache

INPUT_NAME = "day12.txt"
INPUT_PATH = Path(__file__).parent.parent.parent / "input" / INPUT_NAME

class Record(NamedTuple):
    line:str
    groups:tuple[int,...]
    
    @classmethod
    def parse_line(cls,line:str) -> "Record":
        split_point = line.index(' ')
        numbers = tuple(int(x) for x in line[split_point+1:].split(','))
        return cls(line[0:split_point],numbers)
    
    def unfold(self) -> "Record":
        new_line = "?".join(self.line for _ in range(5))
        new_groups = tuple(i for _ in range(5) for i in self.groups)
        return self.__class__(new_line,new_groups)
    
    def __repr__(self) -> str:
        return f"{self.line} -> {' '.join(str(x) for x in self.groups)}"
    
    def arrangements(self) -> int:
        return _get_arrangements(self.line,self.groups)

@cache
def _get_arrangements(line:str,groups:tuple[int,...]) -> int:
    """Recursive solver to find the total number of ways a sequence of springs can be arranged.

    Args:
        line (str): The input, consisting of .#?
        groups (tuple[int,...]): The numbers of consecutive broken springs.

    Returns:
        int: The number of possible arrangements.
    """
    #Step 1: check if all groups have been matched, and there are no more # in the string.
    if len(groups) == 0:
        if any(char == '#' for char in line):
            return 0
        return 1
    curr_group = groups[0]
    #If the line start is past the end of the line, or there are not enough characters left, reject.
    if len(line) == 0 or len(line) < curr_group:
        return 0
    
    #step 2: Check what the first character in the line is, and process accordingly.
    
    initial = line[0]
    next_start = curr_group + 1
    if initial == '.':
        #Nothing to do here, move along.
        return _get_arrangements(line[1:],groups)
    elif initial == '#':
        #The *whole* group has to fit in. If not, reject.
        if all(char != '.' for char in line[0:curr_group]):
            #Either the entire line has to be exhausted, or the character after the current
            # group has to be anything but a #
            if curr_group == len(line) or line[curr_group] != '#':
                return _get_arrangements(line[next_start:],groups[1:])
        #Otherwise, this can't possibly be a valid arrangement.
        return 0
    else: # Must be a ?
        total = 0
        #First, run things as if the ? is really a #
        if all(char != '.' for char in line[:curr_group]):
            #Same as before. Either we're out of characters, or the next character is a .
            if curr_group == len(line) or line[curr_group] != '#':
                total += _get_arrangements(line[next_start:],groups[1:])
        #Second, run things as if the ? is really a .
        total += _get_arrangements(line[1:],groups)
        return total

def parse_line(line:str):
    """ Parse one line of the input into an 'object' for the solution.
    If a line should be discarded, return None instead. """
    line = line.strip()
    if line == "":
        return None
    return Record.parse_line(line)

def parse_input(file_path = INPUT_PATH):
    """ Loads the given file, and parses it line-by-line. Should return
    some useful representation of the input. """
    parsed_input = None
    if file_path.exists():
        with open(file_path) as input_file:
            parsed_input = tuple(parse_line(line) for line in input_file)
    return tuple(x for x in parsed_input if x is not None)

def solution_one(parsed_input:tuple[Record,...]) -> str:
    """ Takes the (parsed) input of the puzzle and uses it to solve for
    the first star of the day. """
    total = 0
    for rec in parsed_input:
        count = rec.arrangements()
        total += count
        #print(repr(rec),";",count)
    return str(total)

def solution_two(parsed_input:tuple[Record,...]) -> str:
    """ Takes the (parsed) input of the puzzle and uses it to solve for
    the second star of the day. """
    total = 0
    for rec in parsed_input:
        total += rec.unfold().arrangements()
    return str(total)

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
    print(f"=== Day 12 ===\n  · Part 1: {result_one}\n  · Part 2: {result_two}\n  · Time: {time_parse}; {time_one}; {time_two}; {time_total}")
    return time_one, time_two, time_total

if __name__ == "__main__":
    solve_day()
