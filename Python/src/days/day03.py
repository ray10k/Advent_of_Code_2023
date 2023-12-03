from pathlib import Path
from time import perf_counter_ns
from itertools import product
from typing import NamedTuple

INPUT_NAME = "day03.txt"
INPUT_PATH = Path(__file__).parent.parent.parent / "input" / INPUT_NAME

class NumberPosition(NamedTuple):
    value:int
    start:int
    end:int
    
    def __contains__(self, __key: object) -> bool:
        if not isinstance(__key, int):
            return False
        return __key >= self.start and __key <= self.end

class PartPostion(NamedTuple):
    shape:str
    position:int

class SchematicRow(NamedTuple):
    numbers:tuple[NumberPosition,...]
    part_positions:tuple[PartPostion,...]
    
    def number_at(self,position:int):
        for number in self.numbers:
            if position in number:
                return number
        return None

    def char_at(self,position:int):
        for part in self.part_positions:
            if position == part.position:
                return part.shape
        for number in self.numbers:
            if position in number:
                number_str = str(number.value)
                return number_str[position - number.start]
        return '.'
    
    def __repr__(self) -> str:
        return f"Row has {len(self.numbers)} numbers and {len(self.part_positions)} parts."
    
class Schematic(NamedTuple):
    rows:tuple[SchematicRow,...]
    width:int
    height:int
    
    def content_of(self,x,y):
        if x < 0 or x >= self.width:
            return '.'
        if y < 0 or y >= self.height:
            return '.'
        return self.rows[y].char_at(x)
        

def parse_line(line:str):
    line = line.strip()
    if line == "":
        return None
    iterator = enumerate(iter(line))
    numbers = []
    parts = []
    number = None
    begin = None
    try:
        while True:
            x, char = next(iterator)
            if char.isdigit():
                if number is None:
                    begin = x
                    number = 0
                number = (10*number) + int(char)
                continue
            if number is not None:
                numbers.append(NumberPosition(number,begin,x-1))
                number = None
            if char != ".":
                parts.append(PartPostion(char,x))
    except:
        if number is not None:
            numbers.append(NumberPosition(number,begin,len(line)-1))
    return SchematicRow(tuple(numbers),tuple(parts))

def parse_input(file_path = INPUT_PATH):
    parsed_input = None
    width,height = 0,0
    if file_path.exists():
        with open(file_path) as input_file:
            lines = input_file.readlines()
            width,height = len(lines[0]),len(lines)
            parsed_input = [parse_line(line) for line in lines]
    return Schematic(tuple(x for x in parsed_input if x is not None),width,height)

def iterate_around(x:int,y:int,width:int,height:int):
    top,bottom = max(y-1,0),min(y+1,height)
    left,right = max(x-1,0),min(x+1,width)
    return product(range(left,right+1),range(top,bottom+1))

def solution_one(parsed_input:Schematic) -> str:
    total = 0
    w,h = parsed_input.width,parsed_input.height
    rows = parsed_input.rows

    for y, row in enumerate(rows):
        for part_x in row.part_positions:
            numbers = set()
            for x_a,y_a in iterate_around(part_x.position,y,w,h):
                num = rows[y_a].number_at(x_a)
                if num is None:
                    continue
                numbers.add(num)
            total += sum(num.value for num in numbers)
    
    return str(total)

def solution_two(parsed_input:Schematic) -> str:
    total = 0
    w,h = parsed_input.width,parsed_input.height
    rows = parsed_input.rows
    
    for y, row in enumerate(rows):
        for part_x in row.part_positions:
            if part_x.shape != "*":
                continue #Only check around gears.
            numbers = set()
            for x_a,y_a in iterate_around(part_x.position,y,w,h):
                num = rows[y_a].number_at(x_a)
                if num is None:
                    continue
                numbers.add(num)
            if len(numbers) != 2:
                continue #Gears have exactly two adjacent numbers.
            total += numbers.pop().value * numbers.pop().value
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
    print(f"=== Day 03 ===\n  · Part 1: {result_one}\n  · Part 2: {result_two}\n  · Time: {time_parse}; {time_one}; {time_two}; {time_total}")
    return time_one, time_two, time_total

if __name__ == "__main__":
    solve_day()