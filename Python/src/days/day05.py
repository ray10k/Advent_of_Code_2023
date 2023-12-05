from pathlib import Path
from time import perf_counter_ns
from typing import NamedTuple

INPUT_NAME = "day05.txt"
INPUT_PATH = Path(__file__).parent.parent.parent / "input" / INPUT_NAME
NWLN = '\n'

PROCESSING_STEPS = [step for step in "seed soil fertilizer water light temperature humidity location".split(" ")]

class Mapping(NamedTuple):
    dest_start:int
    source_start:int
    range_length:int
    
    def source_contains(self,value:int) -> bool:
        delta = value - self.source_start
        return (delta < self.range_length and delta >= 0)
    
    def map_number(self,value:int) -> int:
        delta = self.dest_start - self.source_start
        return value + delta
    
    def map_range(self,range_s:int,range_l:int) -> list[tuple[int,int]]:
        # 5 possible situations: entire range is in mapping range,
        # range starts outside mapping range and ends inside,
        # range starts inside mapping range and ends outside,
        # range starts before mapping range and ends after,
        # range has no overlap with mapping range.
        
        pass
    
    def __repr__(self) -> str:
        return f"dstart: {self.dest_start} sstart: {self.source_start} length: {self.range_length}"
    
class MapSet(NamedTuple):
    dest_type:str
    mappings:tuple[Mapping,...]
    
    def map_number(self,value:int) -> int:
        mapping = next(filter(lambda x:x.source_contains(value),self.mappings),None)
        if mapping is not None:
            return mapping.map_number(value)
        return value
    
    def map_verbose(self,value:int) -> int:
        mapping = next(filter(lambda x:x.source_contains(value),self.mappings),None)
        if mapping is not None:
            print(f"mapping {value} with {mapping!r}")
            return mapping.map_number(value)
        return value
    
    def __repr__(self) -> str:
        return f"\nMap to {self.dest_type}:\n{NWLN.join(repr(mapping) for mapping in self.mappings)}"

class Almanac(NamedTuple):
    seeds:tuple[int,...]
    mappings:tuple[MapSet,...]
    
    def map_number(self,value:int) -> int:
        for mapping in self.mappings:
            value = mapping.map_number(value)
        return value
    
    def map_verbose(self,value:int) -> int:
        for mapping in self.mappings:
            print(f"mapping {value} to {mapping.dest_type}")
            value = mapping.map_verbose(value)
        print(f"Location: {value}")
        return value
    
    def __repr__(self) -> str:
        return f"seeds: {' '.join(str(seed) for seed in self.seeds)}\n{NWLN.join(repr(mapping) for mapping in self.mappings)}"

def parse_input(file_path = INPUT_PATH):
    """ Loads the given file, and parses it line-by-line. Should return
    some useful representation of the input. """

    if file_path.exists():
        with open(file_path) as input_file:
            seeds = next(input_file).strip().split(": ")[1]
            seeds = tuple(int(seed) for seed in seeds.split(" "))
            mappings = list()
            mapsets = list()
            type_ = ""
            next(input_file)#blank line.
            for line in input_file:
                if line.strip() == "":
                    #blank line stops mapping block
                    mapsets.append(MapSet(type_,tuple(mappings)))
                    mappings.clear()
                    type_ = ""
                    continue
                if line[0].isalpha():
                    #First line of a mapping block
                    type_ = line.split("-")[2].split(" ")[0]
                    continue
                #line of mapping block
                mappings.append(Mapping(*(int(x) for x in line.strip().split(" "))))
            if type_ != "":
                mapsets.append(MapSet(type_,tuple(mappings)))
            return Almanac(seeds,tuple(mapsets))
            
def solution_one(parsed_input:Almanac) -> str:
    """ Takes the (parsed) input of the puzzle and uses it to solve for
    the first star of the day. """
    return str(min(parsed_input.map_number(seed) for seed in parsed_input.seeds))

def solution_two(parsed_input:Almanac) -> str:
    """ Takes the (parsed) input of the puzzle and uses it to solve for
    the second star of the day. """
    total = 0
    for length in parsed_input.seeds[1::2]:
        total += length
    print(total)
    
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
    print(f"=== Day 05 ===\n  · Part 1: {result_one}\n  · Part 2: {result_two}\n  · Time: {time_parse}; {time_one}; {time_two}; {time_total}")
    return time_one, time_two, time_total

if __name__ == "__main__":
    solve_day()
