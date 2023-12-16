from pathlib import Path
from time import perf_counter_ns

INPUT_NAME = "day11.txt"
INPUT_PATH = Path(__file__).parent.parent.parent / "input" / INPUT_NAME

def parse_line(line:str):
    """ Parse one line of the input into an 'object' for the solution.
    If a line should be discarded, return None instead. """
    line = line.strip()
    if line == "":
        return None
    return line

def parse_input(file_path = INPUT_PATH):
    """ Loads the given file, and parses it line-by-line. Should return
    some useful representation of the input. """
    parsed_input = None
    if file_path.exists():
        with open(file_path) as input_file:
            parsed_input = tuple(parse_line(line) for line in input_file)
    return tuple(x for x in parsed_input if x is not None)

def solution_one(parsed_input:tuple[str,...]) -> str:
    """ Takes the (parsed) input of the puzzle and uses it to solve for
    the first star of the day. """
    # Step 1: Find the empty rows, and empty collumns.
    empty_collumns = [x for x in range(len(parsed_input[0]))]
    empty_rows = []
    galaxies = set()
    for y,line in enumerate(parsed_input):
        if line.count('#') > 0:
            next_start = 0
            while (index := line.find('#',next_start)) >= 0:
                next_start = index + 1
                galaxies.add((index,y))
                try:
                    empty_collumns.remove(index)
                except:
                    pass
        else:
            empty_rows.append(y)
    # Step 2: adjust the galaxies.
    shifted_galaxies = set()
    for x,y in galaxies:
        offset = 0
        for coll in empty_collumns:
            if coll < x:
                offset += 1
        x += offset
        offset = 0
        for row in empty_rows:
            if row < y:
                offset += 1
        y += offset
        shifted_galaxies.add((x,y))
    # Step 3: calculate *all* the distances between galaxies.
    retval = 0
    while len(shifted_galaxies) > 0:
        current_galaxy = shifted_galaxies.pop()
        for other in shifted_galaxies:
            retval += (abs(current_galaxy[0]-other[0])+abs(current_galaxy[1]-other[1]))
    return str(retval)

def solution_two(parsed_input:tuple) -> str:
    """ Takes the (parsed) input of the puzzle and uses it to solve for
    the second star of the day. """
        # Step 1: Find the empty rows, and empty collumns.
    empty_collumns = [x for x in range(len(parsed_input[0]))]
    empty_rows = []
    galaxies = set()
    for y,line in enumerate(parsed_input):
        if line.count('#') > 0:
            next_start = 0
            while (index := line.find('#',next_start)) >= 0:
                next_start = index + 1
                galaxies.add((index,y))
                try:
                    empty_collumns.remove(index)
                except:
                    pass
        else:
            empty_rows.append(y)
    # Step 2: adjust the galaxies.
    shifted_galaxies = set()
    for x,y in galaxies:
        offset = 0
        for coll in empty_collumns:
            if coll < x:
                offset += 999_999
        x += offset
        offset = 0
        for row in empty_rows:
            if row < y:
                offset += 999_999
        y += offset
        shifted_galaxies.add((x,y))
    # Step 3: calculate *all* the distances between galaxies.
    retval = 0
    while len(shifted_galaxies) > 0:
        current_galaxy = shifted_galaxies.pop()
        for other in shifted_galaxies:
            retval += (abs(current_galaxy[0]-other[0])+abs(current_galaxy[1]-other[1]))
    return str(retval)

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
    print(f"=== Day 11 ===\n  · Part 1: {result_one}\n  · Part 2: {result_two}\n  · Time: {time_parse}; {time_one}; {time_two}; {time_total}")
    return time_one, time_two, time_total

if __name__ == "__main__":
    solve_day()
