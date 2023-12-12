from pathlib import Path
from time import perf_counter_ns
from typing import NamedTuple

INPUT_NAME = "day10.txt"
INPUT_PATH = Path(__file__).parent.parent.parent / "input" / INPUT_NAME

class Coordinate(NamedTuple):
    h:int
    v:int

    def with_offset(self,h_off:int,v_off:int) -> "Coordinate":
        return Coordinate(self.h+h_off,self.v+v_off)
    
    def all_adjacent(self) -> tuple["Coordinate","Coordinate","Coordinate","Coordinate"]:
        return Coordinate(self.h,self.v-1),Coordinate(self.h+1,self.v),Coordinate(self.h,self.v+1),Coordinate(self.h-1,self.v)

def parse_line(line:str) -> str:
    """ Parse one line of the input into an 'object' for the solution.
    If a line should be discarded, return None instead. """
    line = line.strip()
    if line == "":
        return None
    return line

def parse_input(file_path = INPUT_PATH) -> tuple[str,...]:
    """ Loads the given file, and parses it line-by-line. Should return
    some useful representation of the input. """
    parsed_input = None
    if file_path.exists():
        with open(file_path) as input_file:
            parsed_input = tuple(parse_line(line) for line in input_file)
    return tuple(x for x in parsed_input if x is not None)

def connections(char:str,position:Coordinate) -> None|tuple[Coordinate,Coordinate]:
    if len(char) == 0 or position is None:
        return None
    match char[0]:
        case '|': return position.with_offset(0,1),position.with_offset(0,-1)
        case '-': return position.with_offset(1,0),position.with_offset(-1,0)
        case 'L': return position.with_offset(1,0),position.with_offset(0,-1)
        case 'J': return position.with_offset(-1,0),position.with_offset(0,-1)
        case '7': return position.with_offset(-1,0),position.with_offset(0,1)
        case 'F': return position.with_offset(1,0),position.with_offset(0,1)
        case _: return None

def solution_one(parsed_input:tuple[str,...]) -> str:
    """ Takes the (parsed) input of the puzzle and uses it to solve for
    the first star of the day. """
    # Find coordinates of starting point
    start = None
    w,h = 0,len(parsed_input)
    for y,line in enumerate(parsed_input):
        for x,char in enumerate(line):
            if char == 'S':
                start = Coordinate(x,y)
            w = max(w,len(line)) 
    print(f"Starting from {start};board size {w}x{h}")
    # Check in which directions the starting point can go- should be between 2 and 4 options
    around = [start.with_offset(1,0),start.with_offset(-1,0),start.with_offset(0,1),start.with_offset(0,-1)]
    connected_to_start:list[Coordinate] = []
    for to_check in around:
        pipe = parsed_input[to_check.v][to_check.h]
        conn = connections(pipe,to_check)
        if conn is not None and start in conn:
            connected_to_start.append(to_check)
    print(f"Found {len(connected_to_start)} pipes that connect to the starting point.")
    stepcount = 0
    for sub_start in connected_to_start:
        visited = set()
        visited.add(start)
        last = start
        next_ = sub_start
        while next_ != start:
            visited.add(next_)
            pipe = parsed_input[next_.v][next_.h]
            candidates = connections(pipe,next_)
            if candidates is None:
                break
            next_,last = (candidates[0],next_) if candidates[0] != last else (candidates[1],next_)
        stepcount = max(stepcount,len(visited))
    return str(stepcount//2)

def solution_two(parsed_input:tuple) -> str:
    """ Takes the (parsed) input of the puzzle and uses it to solve for
    the second star of the day. """
    # Step 1: find out which way the area 'turns.' Trace the entire path,
    # counting turns right and subtracting turns left; if the result is
    # positive, the area turns 'clockwise' and the inside is on the right
    # of the path. Also, collect all the locations along the path for future
    # steps.
    start_location = None
    for y,line in enumerate(parsed_input):
        for x,char in enumerate(line):
            if char == 'S':
                start_location = Coordinate(x,y)
                break
    first_pipe = None
    for spot in start_location.all_adjacent():
        pipe = parsed_input[spot.v][spot.h]
        if start_location in connections(pipe,spot):
            first_pipe = spot
            break


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
    print(f"=== Day 10 ===\n  · Part 1: {result_one}\n  · Part 2: {result_two}\n  · Time: {time_parse}; {time_one}; {time_two}; {time_total}")
    return time_one, time_two, time_total

if __name__ == "__main__":
    solve_day()
