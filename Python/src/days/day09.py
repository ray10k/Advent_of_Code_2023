from pathlib import Path
from time import perf_counter_ns

INPUT_NAME = "day09.txt"
INPUT_PATH = Path(__file__).parent.parent.parent / "input" / INPUT_NAME

def parse_line(line:str):
    """ Parse one line of the input into an 'object' for the solution.
    If a line should be discarded, return None instead. """
    line = line.strip()
    if line == "":
        return None
    return tuple(int(num) for num in line.split(" "))

def parse_input(file_path = INPUT_PATH):
    """ Loads the given file, and parses it line-by-line. Should return
    some useful representation of the input. """
    parsed_input = None
    if file_path.exists():
        with open(file_path) as input_file:
            parsed_input = tuple(parse_line(line) for line in input_file)
    return tuple(x for x in parsed_input if x is not None)

def delta_up_down(initial:tuple[int,...]) -> tuple[int,int]:
    current = [b - a for a,b in zip(initial[0:],initial[1:])]
    pyramid = [list(initial),current]
    while not all(x == 0 for x in current):
        current = [b - a for a,b in zip(current[0:],current[1:])]
        pyramid.append(current)
    left, right = 0, 0
    for line in pyramid[-2::-1]:
        left = line[0] - left
        right = right + line[-1]
    return left,right

def solution_one(parsed_input:tuple[tuple[int,...],...]) -> str:
    """ Takes the (parsed) input of the puzzle and uses it to solve for
    the first star of the day. """
    result = sum(delta_up_down(x)[1] for x in parsed_input)
    return str(result)

def solution_two(parsed_input:tuple[tuple[int,...],...]) -> str:
    """ Takes the (parsed) input of the puzzle and uses it to solve for
    the second star of the day. """
    result = sum(delta_up_down(x)[0] for x in parsed_input)
    return str(result)

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
    print(f"=== Day 09 ===\n  · Part 1: {result_one}\n  · Part 2: {result_two}\n  · Time: {time_parse}; {time_one}; {time_two}; {time_total}")
    return time_one, time_two, time_total

if __name__ == "__main__":
    solve_day()
