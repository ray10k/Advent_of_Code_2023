from pathlib import Path
from time import perf_counter_ns
from typing import NamedTuple

INPUT_NAME = "day13.txt"
INPUT_PATH = Path(__file__).parent.parent.parent / "input" / INPUT_NAME

class RockMap(NamedTuple):
    lines:tuple[str,...]
    width:int
    height:int
    
    @classmethod
    def from_lines(cls,lines:list[str]):
        width = max(len(line) for line in lines)
        height = len(lines)
        return cls(tuple(lines),width,height)
    
    def __repr__(self) -> str:
        return f"Map of {self.width} by {self.height}"
    
    def get_rows(self) -> tuple[int,...]:
        rows = []
        for line in self.lines:
            temp = 0
            for pos,char in enumerate(line):
                temp += 1<<pos if char == '#' else 0
            rows.append(temp)
        return tuple(rows)
    
    def get_columns(self) -> tuple[int,...]:
        columns = []
        for column in range(self.width):
            temp = 0
            for pos,line in enumerate(self.lines):
                temp += 1<<pos if line[column] == '#' else 0
            columns.append(temp)
        return tuple(columns)

def parse_input(file_path = INPUT_PATH):
    """ Loads the given file, and parses it line-by-line. Should return
    some useful representation of the input. """
    parsed_input = []
    temp_lines = []
            
    if file_path.exists():
        with open(file_path) as input_file:
            for line in input_file:
                line = line.strip()
                if line:
                    temp_lines.append(line)
                else:
                    parsed_input.append(RockMap.from_lines(temp_lines))
                    temp_lines.clear()
    if temp_lines:
        parsed_input.append(RockMap.from_lines(temp_lines))
    return tuple(parsed_input)

def is_mirror_section(segment:tuple[int,...])->bool:
    #print(f"Testing {segment}")
    if len(segment) % 2 != 0 or len(segment) == 0:
        return False
    midpoint = int(len(segment) / 2)
    return all(l==r for l,r in zip(segment[:midpoint],segment[:midpoint-1:-1]))

def solution_one(parsed_input:tuple[RockMap,...]) -> str:
    """ Takes the (parsed) input of the puzzle and uses it to solve for
    the first star of the day. """
    retval = 0
    for mp in parsed_input:
        #print(f"{mp!r}; {mp.get_columns()}; {mp.get_rows()}")
        rows = mp.get_rows()
        #Check rows against the bottom row.
        for h in range(0,len(rows)):
            if is_mirror_section(rows[h:]):
                up_rows = h + ((len(rows) - h) / 2)
                retval += int(100*up_rows)
                break
            elif is_mirror_section(rows[:h]):
                up_rows = h/2
                retval += int(100*up_rows)
                break
        else:
            columns = mp.get_columns()
            for v in range(0,len(columns)):
                if is_mirror_section(columns[v:]):
                    left_cols = v + ((len(columns) - v) / 2)
                    retval += int(left_cols)
                    break
                elif is_mirror_section(columns[:v]):
                    left_cols = v/2
                    retval += int(left_cols)
                    break

    return str(retval)

def solution_two(parsed_input:tuple[RockMap,...]) -> str:
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
    print(f"=== Day 13 ===\n  · Part 1: {result_one}\n  · Part 2: {result_two}\n  · Time: {time_parse}; {time_one}; {time_two}; {time_total}")
    return time_one, time_two, time_total

if __name__ == "__main__":
    solve_day()
