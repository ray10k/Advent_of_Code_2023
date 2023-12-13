from pathlib import Path
from time import perf_counter_ns
from typing import NamedTuple
import random
import tkinter as tk
import tkinter.ttk as ttk

INPUT_NAME = "day10.txt"
INPUT_PATH = Path(__file__).parent.parent.parent / "input" / INPUT_NAME

class Coordinate(NamedTuple):
    h:int
    v:int

    def with_offset(self,h_off:int,v_off:int) -> "Coordinate":
        return Coordinate(self.h+h_off,self.v+v_off)
    
    def all_adjacent(self,max_x:int,max_y:int) -> tuple["Coordinate",...]:
        return tuple(
            self.with_offset(x,y) for x,y in ((1,0),(0,1),(-1,0),(0,-1)) if 0 <= self.h+x < max_x and 0 <= self.v+y < max_y
        )
    
class GridGui(tk.Tk):
    def __init__(self,pipe_grid:tuple[str,...], **kwargs) -> None:
        self.grid_height = len(pipe_grid)
        self.grid_width = len(pipe_grid[0])
        self.tiles = [[0 for _ in range(self.grid_width)] for _ in range(self.grid_height)]
        super().__init__(kwargs.get("screenName","Advent of Code 2023 day 10"))
        
        root_frame = ttk.Frame(self,padding="5")
        root_frame.configure(height=200, width=200)
        canvas1 = tk.Canvas(root_frame)
        canvas1.configure(height=5*self.grid_height, width=5*self.grid_width,border="-2")
        canvas1.grid(column=0, row=0, sticky="nsw")
        frame2 = ttk.Frame(root_frame)
        frame2.configure(height=200, width=200)
        label5 = ttk.Label(frame2)
        label5.configure(text='Star 1:')
        label5.grid(column=0, row=0)
        star_1_l = ttk.Label(frame2)
        star_1_l.configure(font="{Arial} 12 {bold}", text='<>')
        star_1_l.grid(column=0, row=1)
        separator1 = ttk.Separator(frame2)
        separator1.configure(orient="horizontal")
        separator1.grid(column=0, row=2, sticky="ew")
        label3 = ttk.Label(frame2)
        label3.configure(text='Star 2:')
        label3.grid(column=0, row=3)
        label4 = ttk.Label(frame2)
        label4.configure(font="{Arial} 12 {bold}", text='<>')
        label4.grid(column=0, row=4)
        frame2.grid(column=1, row=0, sticky="e")
        frame2.columnconfigure(0, minsize=100)
        root_frame.grid(column=0, row=0)

        self.canvas = canvas1
        self.star_1 = star_1_l
        self.star_2 = label4

        greys = ["#555","#777","#999","#bbb","#ddd"]

        for x in range(self.grid_width):
            for y in range(self.grid_height):
                s_x = x * 5
                s_y = y * 5
                rect_id = canvas1.create_rectangle(s_x,s_y,s_x+6,s_y+6,outline="",fill=random.choice(greys))
                self.tiles[y][x] = rect_id
                pipe = pipe_grid[y][x]
                match pipe:
                    case 'S': 
                        canvas1.itemconfigure(rect_id,{"fill":"#00f"})
                    case '|':
                        canvas1.create_line(s_x+2,s_y,s_x+2,s_y+5)
                    case '-':
                        canvas1.create_line(s_x,s_y+2,s_x+5,s_y+2)
                    case 'L':
                        canvas1.create_line(s_x+2,s_y,s_x+2,s_y+2,s_x+5,s_y+2)
                    case 'J':
                        canvas1.create_line(s_x+2,s_y,s_x+2,s_y+2,s_x-1,s_y+2)
                    case '7':
                        canvas1.create_line(s_x,s_y+2,s_x+2,s_y+2,s_x+2,s_y+5)
                    case 'F':
                        canvas1.create_line(s_x+2,s_y+5,s_x+2,s_y+2,s_x+5,s_y+2)
                    case '.':
                        canvas1.create_oval(s_x+1,s_y+1,s_x+3,s_y+3)
        self.cursor = canvas1.create_rectangle(0,0,5,5,fill='',outline='')
        self.target = canvas1.create_oval(0,0,1,1,fill="",outline="")

    def in_grid(self,tile_x,tile_y) -> bool:
        return tile_x >= 0 and tile_x < self.grid_width and tile_y >= 0 and tile_y < self.grid_height
    
    def mark_tile(self,tile_x,tile_y,colour="#f00"):
        if not self.in_grid(tile_x,tile_y):
            return
        tile_id = self.tiles[tile_y][tile_x]
        self.canvas.itemconfigure(tile_id,{"fill":colour})
    
    def move_target(self,tile_x,tile_y,visible=True):
        if not self.in_grid(tile_x,tile_y):
            return
        if visible:
            s_x = (tile_x*5)+1
            s_y = (tile_y*5)+1
            self.canvas.itemconfigure(self.target,{"outline":"#00f","fill":"#007"})
            self.canvas.coords(self.target,(s_x,s_y,s_x+2,s_y+2))
        else:
            self.canvas.itemconfigure(self.target,{"outline":""})
    
    def move_cursor(self,tile_x,tile_y,visible=True):
        if not self.in_grid(tile_x,tile_y):
            return
        if visible:
            s_x = tile_x*5
            s_y = tile_y*5
            self.canvas.itemconfigure(self.cursor,{"outline":"green"})
            self.canvas.coords(self.cursor,(s_x,s_y,s_x+4,s_y+4))
        else:
            self.canvas.itemconfigure(self.cursor,{"outline":""})


def parse_line(line:str) -> str:
    """ Parse one line of the input into an 'object' for the solution.
    If a line should be discarded, return None instead. """
    line = line.strip()
    if line == "":
        return None
    return line

def parse_input(file_path = INPUT_PATH) -> tuple[str,...]:
    """ Loads the given file, and parses it line-by-line. Should return
    some useful representation of the input. """
    parsed_input = None
    if file_path.exists():
        with open(file_path) as input_file:
            parsed_input = tuple(parse_line(line) for line in input_file)
    return tuple(x for x in parsed_input if x is not None)

def connections(char:str,position:Coordinate) -> None|tuple[Coordinate,Coordinate]:
    if len(char) == 0 or position is None:
        return None
    match char[0]:
        case '|': return position.with_offset(0,1),position.with_offset(0,-1)
        case '-': return position.with_offset(1,0),position.with_offset(-1,0)
        case 'L': return position.with_offset(1,0),position.with_offset(0,-1)
        case 'J': return position.with_offset(-1,0),position.with_offset(0,-1)
        case '7': return position.with_offset(-1,0),position.with_offset(0,1)
        case 'F': return position.with_offset(1,0),position.with_offset(0,1)
        case _: return None
        
def direction(previous:Coordinate,current:Coordinate,pipe:str) -> int:
    # Positive is a clockwise turn, negative is a counter-clockwise turn.
    if pipe == '|' or pipe == '-': #Going straight, no turning.
        return 0
    delta_h = current.h - previous.h
    delta_v = current.v - previous.v
    if delta_h == 0:#moving up/down
        if delta_v > 0:#moving down
            return 1 if pipe == 'J' else -1
        else: #moving up
            return 1 if pipe == 'F' else -1
    else: #moving left/right
        if delta_h > 0: #moving right
            return -1 if pipe == 'J' else 1
        else: #moving left
            return -1 if pipe == 'F' else 1

def adjacencies(previous:Coordinate,current:Coordinate,pipe:str) -> tuple[list[Coordinate],list[Coordinate]]:
    delta_h = current.h - previous.h
    
    ne = current.with_offset(1,-1)
    se = current.with_offset(1,1)
    sw = current.with_offset(-1,1)
    nw = current.with_offset(-1,-1)

    if pipe == '7':
        if delta_h == 0:
            return ([nw,current.with_offset(0,-1),ne,current.with_offset(1,0),se],[sw])
        else:
            return ([sw],[nw,current.with_offset(0,-1),ne,current.with_offset(1,0),se])
    if pipe == 'J':
        if delta_h == 0:
            return ([nw],[ne,current.with_offset(1,0),se,current.with_offset(0,1),sw])
        else:
            return ([ne,current.with_offset(1,0),se,current.with_offset(0,1),sw],[nw])
    if pipe == 'L':
        if delta_h == 0:
            return ([nw,current.with_offset(-1,0),sw,current.with_offset(0,1),se],[ne])
        else:
            return ([ne],[nw,current.with_offset(-1,0),sw,current.with_offset(0,1),se])
    if pipe == 'F':
        if delta_h == 0:
            return ([se],[sw,current.with_offset(-1,0),nw,current.with_offset(0,-1),ne])
        else:
            return ([sw,current.with_offset(-1,0),nw,current.with_offset(0,-1),ne],[se])
    if pipe == '-':
        if delta_h > 0:
            return ([nw,current.with_offset(0,-1),ne],[se,current.with_offset(0,1),sw])
        else:
            return ([se,current.with_offset(0,1),sw],[nw,current.with_offset(0,-1),ne])
    delta_v = current.v - previous.v
    if delta_v > 0:
        return ([ne,current.with_offset(1,0),se],[nw,current.with_offset(-1,0),sw])
    else:
        return ([nw,current.with_offset(-1,0),sw],[ne,current.with_offset(1,0),se])

def side(previous:Coordinate,current:Coordinate,clockwise:bool) -> Coordinate:
    if previous == current:
        return current
    # Clockwise is on the 'right' of current, counterclockwise on the 'left'
    if previous.h == current.h: #moving up/down
        if previous.v > current.v: #moving up
            return current.with_offset(1 if clockwise else -1,0)
        else: #moving down
            return current.with_offset(-1 if clockwise else 1,0)
    else: #moving left/right
        if previous.h > current.h: #moving left
            return current.with_offset(0,-1 if clockwise else 1)
        else: #moving right
            return current.with_offset(0,1 if clockwise else -1)

def solution_one(parsed_input:tuple[str,...],gui:GridGui=None) -> str:
    """ Takes the (parsed) input of the puzzle and uses it to solve for
    the first star of the day. """
    # Find coordinates of starting point
    start = None
    w,h = 0,len(parsed_input)
    for y,line in enumerate(parsed_input):
        for x,char in enumerate(line):
            if char == 'S':
                start = Coordinate(x,y)
            w = max(w,len(line)) 
    print(f"Starting from {start};board size {w}x{h}")
    # Check in which directions the starting point can go- should be between 2 and 4 options
    around = [start.with_offset(1,0),start.with_offset(-1,0),start.with_offset(0,1),start.with_offset(0,-1)]
    connected_to_start:list[Coordinate] = []
    for to_check in around:
        pipe = parsed_input[to_check.v][to_check.h]
        conn = connections(pipe,to_check)
        if conn is not None and start in conn:
            connected_to_start.append(to_check)
    stepcount = 0
    for sub_start in connected_to_start:
        visited = set()
        visited.add(start)
        last = start
        next_ = sub_start
        while next_ != start:
            if gui is not None:
                gui.mark_tile(next_.h,next_.v)
            visited.add(next_)
            pipe = parsed_input[next_.v][next_.h]
            candidates = connections(pipe,next_)
            if candidates is None:
                break
            next_,last = (candidates[0],next_) if candidates[0] != last else (candidates[1],next_)
        stepcount = max(stepcount,len(visited))
    return str(stepcount//2)

def solution_two(parsed_input:tuple[str,...],gui:GridGui=None) -> str:
    """ Takes the (parsed) input of the puzzle and uses it to solve for
    the second star of the day. """
    # Step 1: Find the beginning of the loop.
    h,w = len(parsed_input),len(parsed_input[0])
    start_location:Coordinate = None
    for y,line in enumerate(parsed_input):
        for x,char in enumerate(line):
            if char == 'S':
                start_location = Coordinate(x,y)
                break
    first_pipe = None
    for spot in start_location.all_adjacent(w,h):
        pipe = parsed_input[spot.v][spot.h]
        conns = connections(pipe,spot)
        if start_location in conns:
            first_pipe = spot
            break
    # Step 2: find out which way the area 'turns.' Trace the entire path,
    # counting turns right and subtracting turns left; if the result is
    # positive, the area turns 'clockwise' and the inside is on the right
    # of the path. Also, collect all the locations along the path for future
    # steps.
    turns = 0
    pipe_locations:list[Coordinate] = list()
    pipe_locations.append(start_location)
    previous = start_location
    current = first_pipe
    while current != start_location:
        pipe_locations.append(current)
        pipe = parsed_input[current.v][current.h]
        neighbors = connections(pipe,current)
        next_ = neighbors[0] if neighbors[1] == previous else neighbors[1]
        turns += direction(previous,current,pipe)
        previous = current
        current = next_
    print(f"Found {len(pipe_locations)} pieces of pipe. Total turn number: {turns}; {'clockwise' if turns > 0 else 'counterclockwise'}")
    clockwise = turns > 0
    inside_tiles:set[Coordinate] = set()

    for prev,current in zip(pipe_locations[:],pipe_locations[1:]):
        pipe = parsed_input[current.v][current.h]
        to_fill = adjacencies(prev,current,pipe)[0 if clockwise else 1]
        if gui is not None:
            gui.move_cursor(current.h,current.v)
            gui.move_target(to_fill[0].h,to_fill[0].v)
            gui.update()
        while len(to_fill) > 0:
            current_fill = to_fill.pop()
            if current_fill not in inside_tiles and current_fill not in pipe_locations:
                if gui is not None:
                    gui.mark_tile(current_fill.h,current_fill.v,"#880")
                to_fill.extend(current_fill.all_adjacent(w,h))
                inside_tiles.add(current_fill)
    
    return str(len(inside_tiles))

def solve_day() -> tuple[float,float,float]:
    
    times = [0,0,0,0]
    times[0] = perf_counter_ns()
    parsed_input = parse_input()
    gui = GridGui(parsed_input,screenName = "hello world")
    gui.update()
    times[1] = perf_counter_ns()
    result_one = solution_one(parsed_input,gui)
    gui.star_1["text"] = result_one
    gui.update()
    times[2] = perf_counter_ns()
    result_two = solution_two(parsed_input,gui)
    gui.star_2["text"] = result_two
    gui.update()
    times[3] = perf_counter_ns()

    time_parse = (times[1] - times[0]) / 1_000_000
    time_one = (times[2] - times[1]) / 1_000_000
    time_two = (times[3] - times[2]) / 1_000_000
    time_total = (times[3] - times[0]) / 1_000_000
    print(f"=== Day 10 ===\n  · Part 1: {result_one}\n  · Part 2: {result_two}\n  · Time: {time_parse}; {time_one}; {time_two}; {time_total}")
    gui.mainloop()
    return time_one, time_two, time_total

if __name__ == "__main__":
    test_coord = Coordinate(5,5)
    print(side(test_coord,test_coord.with_offset(-1,0),True),"left")
    print(side(test_coord,test_coord.with_offset(1,0),True),"right")
    print(side(test_coord,test_coord.with_offset(0,-1),True),"up")
    print(side(test_coord,test_coord.with_offset(0,1),True),"down")

    print(direction(test_coord.with_offset(-1,0),test_coord,"J"),direction(test_coord.with_offset(0,-1),test_coord,"J"),"NW")
    print(direction(test_coord.with_offset(-1,0),test_coord,"7"),direction(test_coord.with_offset(0,1),test_coord,"7"),"SW")
    print(direction(test_coord.with_offset(1,0),test_coord,"F"),direction(test_coord.with_offset(0,1),test_coord,"F"),"SE")
    print(direction(test_coord.with_offset(1,0),test_coord,"L"),direction(test_coord.with_offset(0,-1),test_coord,"L"),"NE")

    solve_day()
