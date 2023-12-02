from pathlib import Path
from time import perf_counter_ns
from typing import NamedTuple

INPUT_NAME = "day02.txt"
INPUT_PATH = Path(__file__).parent.parent.parent / "input" / INPUT_NAME

class CubeHand(NamedTuple):
    red: int = 0
    green: int = 0
    blue: int = 0
    
    def __repr__(self) -> str:
        return f"{self.red} red, {self.green} green, {self.blue} blue;"
    
    def is_empty(self) -> bool:
        return self.red == 0 and self.green == 0 and self.blue == 0
    
    def __contains__(self, __key: object) -> bool:
        if type(__key) != type(self):
            return False
        return __key.red <= self.red and __key.green <= self.green and __key.blue <= self.blue
    
    def smallest_overlap(self, other:"CubeHand") -> "CubeHand":
        r_o = max(self.red,other.red)        
        g_o = max(self.green,other.green)
        b_o = max(self.blue,other.blue)
        return CubeHand(r_o,g_o,b_o)
    
    def hand_power(self) -> int:
        return self.red * self.blue * self.green

class SingleGame(NamedTuple):
    id_number: int
    hands:tuple[CubeHand,...]
    
    def __repr__(self) -> str:
        return f"Game id {self.id_number}; hands: {' '.join(repr(hand) for hand in self.hands)}"

def parse_line(line:str):
    line = line.strip()
    if line == "":
        return None
    line = line.split(":")
    game_id = int(line[0].split(' ')[1])
    hands = []
    for hand in line[1].split(';'):
        rgb = [0,0,0]
        for colour in hand.split(','):
            _, num, col = colour.split(" ")
            if col == "red":
                rgb[0] = int(num)
            elif col == "green":
                rgb[1] = int(num)
            else:
                rgb[2] = int(num)
        hands.append(CubeHand(*rgb))
            
    return SingleGame(game_id,tuple(hands))

def parse_input(file_path = INPUT_PATH):
    parsed_input = list()
    if file_path.exists():
        with open(file_path) as input_file:
            parsed_input = tuple(parse_line(line) for line in input_file)
    return tuple(i for i in parsed_input if i is not None)

def solution_one(parsed_input:tuple[SingleGame,...]) -> str:
    id_sum = 0
    play_set = CubeHand(12,13,14)
    for _input in parsed_input:
        id_sum += _input.id_number if all(hand in play_set for hand in _input.hands) else 0
    return str(id_sum)

def solution_two(parsed_input:tuple[SingleGame,...]) -> str:
    power_sum = 0
    for _input in parsed_input:
        running_total = _input.hands[0]
        for subhand in _input.hands[1:]:
            running_total = running_total.smallest_overlap(subhand)
        power_sum += running_total.hand_power()
    return str(power_sum)

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
    print(f"=== Day 02 ===\n  · Part 1: {result_one}\n  · Part 2: {result_two}\n  · Time: {time_parse}; {time_one}; {time_two}; {time_total}")
    return time_one, time_two, time_total

if __name__ == "__main__":
    solve_day()
