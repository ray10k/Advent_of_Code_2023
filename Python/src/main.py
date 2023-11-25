from types import ModuleType
from days import day01,day02,day03,day04,day05
from days import day06,day07,day08,day09,day10
from days import day11,day12,day13,day14,day15
from days import day16,day17,day18,day19,day20
from days import day21,day22,day23,day24,day25

import sys
from time import perf_counter_ns

def day_module(name:str) -> ModuleType:
    match name:
        case "1" | "01":
            return day01
        case "2" | "02":
            return day02
        case "3" | "03":
            return day03
        case "4" | "04":
            return day04
        case "5" | "05":
            return day05
        case "6" | "06":
            return day06
        case "7" | "07":
            return day07
        case "8" | "08":
            return day08
        case "9" | "09":
            return day09
        case "10":
            return day10
        case "11":
            return day11
        case "12":
            return day12
        case "13":
            return day13
        case "14":
            return day14
        case "15":
            return day15
        case "16":
            return day16
        case "17":
            return day17
        case "18":
            return day18
        case "19":
            return day19
        case "20":
            return day20
        case "21":
            return day21
        case "22":
            return day22
        case "23":
            return day23
        case "24":
            return day24
        case "25":
            return day25
        case _ as x:
            print(f"Day '{x}' is not a valid day.")
            sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Please provide the day(s) to run as a command-line argument, or the string \"all\" to run all days.")
        sys.exit(1)
    days = list()
    if sys.argv[1] == "all":
        days.extend(str(i) for i in range(1,26))
    else:
        days.extend(i for i in sys.argv[1:])
    
    results = dict()
    start_time = perf_counter_ns()
    for day in days:
        daymodule = day_module(day)
        result = daymodule.solve_day()
        results[day] = result
    end_time = perf_counter_ns()
    
    print(f"Total runtime: {(end_time - start_time)/1_000_000}")