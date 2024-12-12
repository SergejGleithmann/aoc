from copy import copy
from functools import reduce
from typing import List, Tuple


with open("aoc/2024/day12/resources/data.txt", "r") as file:
    data = file.readlines()

""" with open("aoc/2024/day12/resources/test.txt", "r") as file:
    data = file.readlines() """

type Map = List[str]
type Point = Tuple[int, int]


def get_dim(field: Map) -> Point:
    return len(field), len(field[0])


def in_bounds(p: Point, d: Point) -> bool:
    return 0 <= p[0] < d[0] and 0 <= p[1] < d[1]


def add_points(x: Point, y: Point) -> Point:
    return (x[0] + y[0], x[1] + y[1])


map = [[(None, c) for c in line.strip()] for line in data]

ids = {}
dirs = [(0, 1), (1, 0), (0, -1), (-1, 0)]


def get_adj(map: Map, p: Point, discount=False) -> int:
    res = 0
    dim = get_dim(map)
    p_val = map[p[0]][p[1]]
    if discount:
        for i in range(len(dirs)):
            q1 = add_points(dirs[i], p)
            q2 = add_points(dirs[(i + 1) % len(dirs)], p)
            x = add_points(dirs[i], q2)
            # #edges = #corner
            if (  # outer corner
                (not in_bounds(q1, dim) or p_val != map[q1[0]][q1[1]])
                and (not in_bounds(q2, dim) or p_val != map[q2[0]][q2[1]])
            ) or (  # inner corner
                (in_bounds(q1, dim) and p_val == map[q1[0]][q1[1]])
                and (in_bounds(q2, dim) and p_val == map[q2[0]][q2[1]])
                and (in_bounds(x, dim) and p_val != map[x[0]][x[1]])
            ):
                res += 1
    else:
        for dir in dirs:
            q = add_points(dir, p)
            if not in_bounds(q, dim) or p_val != map[q[0]][q[1]]:
                res += 1
    return res


def get_cost(map: Map, discount=False) -> int:
    d = {}
    for i in range(len(map)):
        for j in range(len(map[0])):
            old_res = d.get(map[i][j], (0, 0))
            d[map[i][j]] = add_points(old_res, (1, get_adj(map, (i, j), discount)))
    return sum([perimiter * size for perimiter, size in d.values()])


def set_group_ids(map: Map, id: int, name: str, p: Point):
    i, j = p
    if in_bounds(p, get_dim(map)) and map[i][j][0] is None and map[i][j][1] == name:
        map[i][j] = (id, map[i][j][1])
        for d in dirs:
            set_group_ids(map, id, map[i][j][1], add_points(d, (i, j)))


def set_ids(map: Map):
    ids = {}
    for i in range(len(map)):
        for j in range(len(map[0])):
            if map[i][j][0] is None:
                curr_id = ids.get(map[i][j][1], 0)
                map[i][j] = (curr_id, map[i][j][1])
                ids[map[i][j][1]] = curr_id + 1
                for d in dirs:
                    set_group_ids(map, curr_id, map[i][j][1], add_points(d, (i, j)))


set_ids(map)
print(get_cost(map, False))
print(get_cost(map, True))
