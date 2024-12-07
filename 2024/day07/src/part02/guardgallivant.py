from copy import copy
import time
from typing import Any, Callable, List, Set, Tuple

with open("aoc/2024/day06/resources/data.txt", "r") as file:
    data = file.readlines()


def stoptime(f: Callable[..., Any], args: Any) -> Any:
    t1 = time.time()
    res = f(args)
    t2 = time.time()
    print(f"Duration: {t2-t1:.2f} seconds")
    return res


def preprocess_data(
    data: List[str],
) -> Tuple[List[List[str]], Tuple[int, int], Tuple[int, int]]:
    area = [[*line.strip()] for line in data]
    starting = (-1, -1)
    for r_index, row in enumerate(area):
        for c_index, pos in enumerate(row):
            if pos not in [".", "#"]:
                assert pos == "^"
                starting = (r_index, c_index)
                set_pos(area, *starting, ".")
    dimension = (len(area), len(area[0]))
    assert starting != (-1, -1)
    return area, dimension, starting


dirs = [(-1, 0), (0, 1), (1, 0), (0, -1)]


def add_pos(pos1: Tuple[int, int], pos2: Tuple[int, int]) -> Tuple[int, int]:
    return (pos1[0] + pos2[0], pos1[1] + pos2[0])


def set_pos(l: List[List[Any]], i: int, j: int, val: Any) -> None:
    l[i][j] = val


def get_pos(l: List[List[Any]], i: int, j: int) -> Any:
    return l[i][j]


def in_bounds(dimension: Tuple[int, int], position: Tuple[int, int]) -> bool:
    return 0 <= position[0] < dimension[0] and 0 <= position[1] < dimension[1]


def get_positions(data: List[str]) -> Set[Tuple[int, int]]:
    area, dimension, starting = preprocess_data(data)
    guard = starting
    visited = {guard}
    dir = 0
    while True:
        dir_vec = dirs[dir]
        new_pos = add_pos(guard, dir_vec)
        if in_bounds(dimension, new_pos):
            if get_pos(area, *new_pos) == ".":
                guard = new_pos
                visited.add(guard)
            elif get_pos(area, *new_pos) == "#":
                dir = (dir + 1) % 4
        else:
            break
    return visited


def count_loops(data: List[str]) -> int:
    area, dimension, starting = preprocess_data(data)
    guard = starting
    path = get_positions(data)
    loops = 0
    old_progress = 0
    for idx, position in enumerate(path):
        # monitoring
        progress = int(idx * 100 / len(path))
        if progress != old_progress:
            print(f"\033[AProgress : {progress} %")
            old_progress = progress
        if position == starting:
            continue
        dir = 0
        guard = starting
        visited = {(guard, dir)}
        loop_found = False
        copy_area = [copy(row) for row in area]
        set_pos(copy_area, *position, "#")
        while not loop_found:
            dir_vec = dirs[dir]
            position = add_pos(dir_vec, guard)
            if (position, dir) in visited:
                loop_found = True
            if in_bounds(dimension, position):
                if get_pos(copy_area, *position) == ".":
                    guard = position
                    visited.add((guard, dir))
                elif get_pos(copy_area, *position) == "#":
                    dir = (dir + 1) % 4
            else:
                # out of bounds
                break

        if loop_found:
            loops += 1
    print(f"\033[ADone")
    return loops


print(len(get_positions(data)))

print(stoptime(count_loops, data))
