from pathlib import Path
from time import perf_counter_ns
from typing import NamedTuple
from itertools import cycle
import re

INPUT_NAME = "day08.txt"
INPUT_PATH = Path(__file__).parent.parent.parent / "input" / INPUT_NAME
LINE_PATT = re.compile(r"(\w{3}) = \((\w{3}), (\w{3})\)")

class PathStep(NamedTuple):
    name:str
    left:str
    right:str

class TravelMap(NamedTuple):
    instructions:str
    steps:dict[str,PathStep]

def parse_line(line:str):
    """ Parse one line of the input into an 'object' for the solution.
    If a line should be discarded, return None instead. """
    line = line.strip()
    if line == "":
        return None
    names = LINE_PATT.match(line).groups()
    return PathStep(*names)

def parse_input(file_path = INPUT_PATH):
    """ Loads the given file, and parses it line-by-line. Should return
    some useful representation of the input. """
    if file_path.exists():
        with open(file_path) as input_file:
            instructions = next(input_file).strip()
            parsed_steps = {step.name:step for step in filter(lambda x: x is not None, (parse_line(line) for line in input_file))}
            return TravelMap(instructions,parsed_steps)

def solution_one(parsed_input:TravelMap) -> str:
    """ Takes the (parsed) input of the puzzle and uses it to solve for
    the first star of the day. """
    current = parsed_input.steps["AAA"]
    stepcount = 0
    instruction = cycle(parsed_input.instructions)
    while current.name != "ZZZ":
        stepcount += 1
        step = next(instruction)
        current = parsed_input.steps[current.left if step == "L" else current.right]

    return str(stepcount)

def solution_two(parsed_input:TravelMap) -> str:
    """ Takes the (parsed) input of the puzzle and uses it to solve for
    the second star of the day. """
    current = {step.name for step in parsed_input.steps.values() if step.name[2] == "A"}
    stepcount = 0
    instruction = cycle(parsed_input.instructions)
    done = lambda s: all(step[2] == "Z" for step in s)

    # Tried doing the solution one *thing* in parallel, left it running for over half an hour
    # without getting a solve. Time to get creative.

    # There is a limited number of starting points, and a limited number of end points. Find both.
    starting_points = set(step.name for step in parsed_input.steps.values() if step.name[2] == "A")
    ending_points = set(step.name for step in parsed_input.steps.values() if step.name[2] == "Z")

    # From each starting point, there will eventually be a stable loop that includes at least one ending point.
    # That stable loop can be defined as "some number of iterations of the instruction set (setup) followed by 
    # another number of iterations of the instruction set (loop)"

    while not done(current):
        stepcount += 1
        current_instruction = next(instruction)
        next_step = set()
        for step in current:
            destination = parsed_input.steps[step]
            next_step.add(destination.left if current_instruction == "L" else destination.right)
        current = next_step
        dones = len(list(filter(lambda x: x[2]=="Z",current)))
        print(f"\r{len(current):< 4}{dones:< 4}{current_instruction}",end="",flush=True)
    print()
    return str(stepcount)

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
    print(f"=== Day 08 ===\n  · Part 1: {result_one}\n  · Part 2: {result_two}\n  · Time: {time_parse}; {time_one}; {time_two}; {time_total}")
    return time_one, time_two, time_total

if __name__ == "__main__":
    solve_day()
