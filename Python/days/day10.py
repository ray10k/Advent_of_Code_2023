from pathlib import Path
from time import perf_counter_ns

INPUT_NAME = "day10.txt"
INPUT_PATH = Path(__file__).parent.parent.parent / "input" / INPUT_NAME

parsed_input = None

def parse_line(line:str):
    return line

if INPUT_PATH.exists():
    with open(INPUT_PATH) as input_file:
        parsed_input = tuple(parse_line(line) for line in input_file)

def solution_one(parsed_input:tuple) -> str:
    return ""

def solution_two(parsed_input:tuple) -> str:
    return ""

def solve_day() -> tuple[float,float,float]:
    start_time = perf_counter_ns()
    result_one = solution_one(parsed_input)
    mid_time = perf_counter_ns()
    result_two = solution_two(parsed_input)
    end_time = perf_counter_ns()
    time_one = (mid_time - start_time) / 1_000_000
    time_two = (end_time - mid_time) / 1_000_000
    time_total = (end_time - start_time) / 1_000_000
    print(f"=== Day 10 ===\n  · Part 1: {result_one}\n  · Part 2: {result_two}\n  · Time: {time_one}; {time_two}; {time_total}")
    return time_one, time_two, time_total