from functools import reduce
from typing import List, Set, Tuple


with open("aoc/2024/day10/resources/data.txt", "r") as file:
    data = file.readlines()

""" with open("aoc/2024/day10/resources/test.txt", "r") as file:
    data = file.readlines() """

map = [[int(pos) for pos in line if pos != "\n"] for line in data]

type Point = Tuple[int, int]
type Map = List[List[int]]


def get_dim(field: Map) -> Point:
    return len(field), len(field[0])


def in_bounds(p: Point, d: Point) -> bool:
    return 0 <= p[0] < d[0] and 0 <= p[1] < d[1]


def add_points(x: Point, y: Point) -> Point:
    return (x[0] + y[0], x[1] + y[1])


def trail_ends(map: Map, p: Point, expected: int) -> Set[Point]:
    dirs = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    if in_bounds(p, get_dim(map)) and map[p[0]][p[1]] == expected:
        if expected == 9:
            return {p}
        else:
            return reduce(
                Set.union,
                [trail_ends(map, add_points(p, dir), expected + 1) for dir in dirs],
            )

    else:
        return set()


def trail_rating(map: Map, p: Point, expected: int) -> int:
    dirs = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    if in_bounds(p, get_dim(map)) and map[p[0]][p[1]] == expected:
        if expected == 9:
            return 1
        else:
            return sum(
                [trail_rating(map, add_points(p, dir), expected + 1) for dir in dirs]
            )
    else:
        return 0


def sum_all_trail_scores(map: Map) -> int:

    return sum(
        [
            len(trail_ends(map, (l, c), 0))
            for l in range(len(map))
            for c in range(len(map[0]))
        ]
    )


def sum_all_trail_ratings(map: Map) -> int:
    return sum(
        [
            trail_rating(map, (l, c), 0)
            for l in range(len(map))
            for c in range(len(map[0]))
        ]
    )


print(sum_all_trail_scores(map))
print(sum_all_trail_ratings(map))
