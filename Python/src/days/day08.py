from pathlib import Path
from time import perf_counter_ns
from typing import NamedTuple
from itertools import cycle
from math import lcm
import re

INPUT_NAME = "day08.txt"
INPUT_PATH = Path(__file__).parent.parent.parent / "input" / INPUT_NAME
LINE_PATT = re.compile(r"(\w{3}) = \((\w{3}), (\w{3})\)")

class PathStep(NamedTuple):
    name:str
    left:str
    right:str
    
    def get_next(self,instruction:str):
        """ Returns the name of the next step. """
        if instruction == "L":
            return self.left
        else:
            return self.right
    
    def __repr__(self) -> str:
        return f"{self.name} = ({self.left},{self.right})"

class TravelMap(NamedTuple):
    instructions:str
    steps:dict[str,PathStep]
    
class LoopData(NamedTuple):
    start_to_exit:int
    exit_to_exit:int
    
    def steps_to_exit(self,steps_taken:int) -> int:
        if steps_taken < self.start_to_exit:
            return self.start_to_exit - steps_taken
        steps_taken -= self.start_to_exit
        return steps_taken % self.exit_to_exit

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
        current = parsed_input.steps[current.get_next(step)]

    return str(stepcount)

def solution_two(parsed_input:TravelMap) -> str:
    """ Takes the (parsed) input of the puzzle and uses it to solve for
    the second star of the day. """
    # Tried doing the solution one *thing* in parallel, left it running for over half an hour
    # without getting a solve. Time to get creative.

    # There is a limited number of starting points, and a limited number of end points. Find both.
    starting_points = set(step.name for step in parsed_input.steps.values() if step.name[2] == "A")
    ending_points = set(step.name for step in parsed_input.steps.values() if step.name[2] == "Z")
    
    # Each node points to two other nodes. In other words, it is *possible* that a node only points to itself
    # and never another node, but it is *impossible* to make a node point to "nothing."
    
    # The input has a set of nodes that is defined as the "starting nodes" for the puzzle. In other words, there
    # is an axiomatic set of nodes that are 'valid' to begin from, and all other nodes in the set can safely be
    # disregarded as potential starting points.
    
    # The input is of finite length. In other words, if every node in a set of finite length points to two other
    # nodes in the same set, it is impossible to create an input that features no loops, and it is impossible to
    # create an input where following a fixed series of left-right-instructions will not eventually lead to a loop.
    
    # The input also includes a fixed series of left-right-instructions.

    # From each starting point, there will eventually be a stable loop that includes at least one "terminus" node,
    # where the terminus node is the node that will be visited twice, after some finite number of times of 
    # following the entire given series of left-right-instructions.
    
    # That stable loop can be defined as "some number of iterations of the instruction set (setup) followed by 
    # another number of iterations of the instruction set (loop)"
    # For each starting point, start following the instructions until you run into yourself.
    
    loop_lengths:list[LoopData] = list()
    
    for start in starting_points:
        termini = list() # will contain the names of all locations arrived at after completing a full
        # run of the instructions.
        current = start
        # Find the point where the loop meets itself at the start.
        while current not in termini:
            termini.append(current)
            for instruction in parsed_input.instructions:
                current = parsed_input.steps[current].get_next(instruction)
        loop_steps = (len(parsed_input.instructions) * (len(termini)-termini.index(current))) # steps from loop-point to loop-point
        # Track how many steps it takes while in the loop, to reach a valid end-point.
        start_to_exit = 0
        current = start
        instr_iter = cycle(parsed_input.instructions)
        while current not in ending_points:
            start_to_exit += 1
            current = parsed_input.steps[current].get_next(next(instr_iter))
        loop_lengths.append(LoopData(start_to_exit,loop_steps))
        print(f"Loop analysis starting from {start} complete. Start-to-exit steps: {start_to_exit}. exit-to-exit steps: {loop_steps}.")       
    # Relevant data parsed out. Next step: Figure out the answer.
    # Full disclosure, I had to look this one up here. Also, I don't really understand how this one works :(
    
    final_stepcount = 1
    for dat in loop_lengths:
        final_stepcount = lcm(final_stepcount,dat.start_to_exit)
    
    return str(final_stepcount)

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
