from pathlib import Path
from time import perf_counter_ns
from typing import NamedTuple
import re

INPUT_NAME = "day06.txt"
INPUT_PATH = Path(__file__).parent.parent.parent / "input" / INPUT_NAME
NUMBR_PATT = re.compile(r"\d+")

class RaceStats(NamedTuple):
    time:int
    distance:int
    
    def __repr__(self) -> str:
        return f"{self.time=}; {self.distance=}"
    
    def minimum_win(self) -> int:
        for i in range(self.time+1):
            time_left = self.time - i
            speed = i
            if time_left * speed > self.distance:
                return i
        return -1
    
    def maximum_win(self) -> int:
        for i in range(self.time,-1,-1):
            time_left = self.time - i
            speed = i
            if time_left * speed > self.distance:
                return i
        return -1


def parse_line(line:str):
    """ Parse one line of the input into an 'object' for the solution.
    If a line should be discarded, return None instead. """
    line = line.strip()
    if line == "":
        return None
    return tuple(int(x.group(0)) for x in NUMBR_PATT.finditer(line))

def parse_input(file_path = INPUT_PATH):
    """ Loads the given file, and parses it line-by-line. Should return
    some useful representation of the input. """
    if file_path.exists():
        with open(file_path) as input_file:
            times = parse_line(next(input_file))
            distances = parse_line(next(input_file))
            return tuple(RaceStats(time,dist) for time,dist in zip(times,distances))
    return tuple()

def solution_one(parsed_input:tuple[RaceStats,...]) -> str:
    """ Takes the (parsed) input of the puzzle and uses it to solve for
    the first star of the day. """
    result = 1
    for race in parsed_input:
        top = race.maximum_win()
        bot = race.minimum_win()
        result *= (top - bot)+1
        #print(f"race {race!r}; {top=} - {bot=}")
    return str(result)

def solution_two(parsed_input:tuple[RaceStats,...]) -> str:
    """ Takes the (parsed) input of the puzzle and uses it to solve for
    the second star of the day. """
    total_time, total_distance = "",""
    for race in parsed_input:
        total_time += str(race.time)
        total_distance += str(race.distance)
    real_race = RaceStats(int(total_time),int(total_distance))
    print(repr(real_race))
    real_min = real_race.minimum_win()
    real_max = real_race.maximum_win()
    return str((real_max - real_min)+1)

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
    print(f"=== Day 06 ===\n  · Part 1: {result_one}\n  · Part 2: {result_two}\n  · Time: {time_parse}; {time_one}; {time_two}; {time_total}")
    return time_one, time_two, time_total

if __name__ == "__main__":
    solve_day()
