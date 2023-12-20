from pathlib import Path
from time import perf_counter_ns
from typing import NamedTuple
from functools import cache

INPUT_NAME = "day12_1.txt"
INPUT_PATH = Path(__file__).parent.parent.parent / "input" / INPUT_NAME

class Record(NamedTuple):
    line:str
    groups:tuple[int,...]
    
    @classmethod
    def parse_line(cls,line:str) -> "Record":
        split_point = line.index(' ')
        numbers = tuple(int(x) for x in line[split_point+1:].split(','))
        return cls(line[0:split_point],numbers)
    
    def __repr__(self) -> str:
        return f"{self.line} -> {' '.join(str(x) for x in self.groups)}"
    
    def arrangements(self) -> int:
        return _get_arrangements(self.line,self.groups,0,0)
    
@cache
def _get_arrangements(line:str,groups:tuple[int,...],line_start:int,group_start:int) -> int:
    total = 0
    gl = len(groups)
    ll = len(line)
    rc = ll - line_start

    #First off, pass-condition; The current group is *past* the last group, and there are no more
    # #'s in the line.
    if gl <= group_start:
        for char in line[line_start:]:
            if char == '#':
                return 0
        return 1
    
    cg = groups[group_start]
    next_start = line_start + cg + 1
    print(f"ls {line_start}; gs {group_start}; {line[line_start:]},{cg}")
    
    #Second: There are at least as many characters left in the line as the current group. Reject otherwise.
    if rc < cg:
        return 0

    #print(f" {line[line_start]}; {groups[group_start]}")
    #Next: if the current character is definitely a ., move on and try with the next.
    if line[line_start] == '.':
        return _get_arrangements(line,groups,line_start+1,group_start)
    #Current character is either a # or a ?.
    #If the current character is a ?, try treating it as a .
    if line[line_start] == '?' or (line_start+1 < ll and line[line_start+1] != '.'):
        total += _get_arrangements(line,groups,line_start+1,group_start)
    #Check if the current sequence of [#?] is long enough for the current group.
    for c in line[line_start:line_start+cg]:
        if c == '.':
            return total
    #Also reject if there is at least one more group to check, and either the line has already ran out or 
    # the character after the current group can't be a .
    if group_start+1 < gl and (next_start >= ll or line[line_start + cg] == '#'):
        return total

    total += _get_arrangements(line,groups,next_start,group_start+1)
    #Current line/group layout has not been rejected yet. Continue with the next group, starting where
    # the current group finished.
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
        print(repr(rec),";",count)
    return str(total)

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
    print(f"=== Day 12 ===\n  · Part 1: {result_one}\n  · Part 2: {result_two}\n  · Time: {time_parse}; {time_one}; {time_two}; {time_total}")
    return time_one, time_two, time_total

if __name__ == "__main__":
    solve_day()
