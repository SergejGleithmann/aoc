from typing import List, Set, Tuple


with open("aoc/2024/day08/resources/data.txt", "r") as file:
    data = file.readlines()
""" with open("aoc/2024/day08/resources/test2.txt", "r") as file:
    data = file.readlines() """

field = [[*line.strip()] for line in data]

type Point = Tuple[int, int]
type Pair[T] = Tuple[T, T]


def get_dim(field: List[List[str]]) -> Point:
    return len(field), len(field[0])


def get_pairs(field: List[List[str]]) -> List[Tuple[Point]]:
    l_max, c_max = get_dim(field)
    return [
        ((l1, c1), (l2, c2))
        for l1 in range(l_max)
        for c1 in range(c_max)
        if field[l1][c1] not in [".", "#"]
        for l2 in range(l1, l_max)
        for c2 in range(c1 + 1 if l2 == l1 else 0, c_max)
        if field[l1][c1] == field[l2][c2]
    ]


def in_bounds(p: Point, d: Point) -> bool:
    return 0 <= p[0] < d[0] and 0 <= p[1] < d[1]


def add_points(x, y):
    return (x[0] + y[0], x[1] + y[1])


def sub_points(x, y):
    return (x[0] - y[0], x[1] - y[1])


def get_antinodes(points: Pair[Point], dim: Point, strict=True) -> List[Point]:
    res = []
    p1, p2 = points
    d = sub_points(p2, p1)
    if strict:
        return [p for p in [sub_points(p1, d), add_points(p2, d)] if in_bounds(p, dim)]
    while in_bounds(p1, dim):
        res.append(p1)
        p1 = sub_points(p1, d)
    while in_bounds(p2, dim):
        res.append(p2)
        p2 = add_points(p2, d)
    return res


def get_all_antinodes(field, strict=True) -> Set[Point]:
    pairs = get_pairs(field)
    antinodes = set()
    for pair in pairs:
        antinodes = antinodes.union(get_antinodes(pair, get_dim(field), strict))
    return antinodes


# print(get_pairs(field))
# print(get_antinodes(((2, 5), (3, 7)), get_dim(field)))
print(len(get_all_antinodes(field)))
print(len(get_all_antinodes(field, False)))
