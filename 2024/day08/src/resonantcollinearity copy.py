from typing import List, Self, Set, Tuple


with open("aoc/2024/day08/resources/data.txt", "r") as file:
    data = file.readlines()
""" with open("aoc/2024/day08/resources/test2.txt", "r") as file:
    data = file.readlines() """

field = [[*line.strip()] for line in data]

# type Point = Tuple[int, int]
type Pair[T] = Tuple[T, T]


class Point:
    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y

    def __add__(self, other: Self) -> Self:
        return Point(self.x + other.x, self.y - other.y)

    def __sub__(self, other: Self) -> Self:
        return Point(self.x - other.x, self.y - other.y)

    def __iter__(self):
        return (self.x, self.y)

    def __eq__(self, other: Self) -> bool:
        return self.x == other.y and self.y == other.y

    def __hash__(self):
        return hash((self.x, self.y))

    def in_bounds(self, d: Self) -> bool:
        return 0 <= self.x < d.x and 0 <= self.y < d.y


def get_dim(field: List[List[str]]) -> Point:
    return len(field), len(field[0])


def get_pairs(field: List[List[str]]) -> List[Tuple[Point]]:
    l_max, c_max = get_dim(field)
    return [
        (Point(l1, c1), Point(l2, c2))
        for l1 in range(l_max)
        for c1 in range(c_max)
        if field[l1][c1] not in [".", "#"]
        for l2 in range(l1, l_max)
        for c2 in range(c1 + 1 if l2 == l1 else 0, c_max)
        if field[l1][c1] == field[l2][c2]
    ]


def get_antinodes(points: Pair[Point], dim: Point, strict=True) -> List[Point]:
    res = []
    p1, p2 = points
    d = p2 - p1
    if strict:
        return [p for p in [p1 - d, p2 + d] if p.in_bounds(dim)]
    while p1.in_bounds(dim):
        res.append(p1)
        p1 -= d
    while p2.in_bounds(dim):
        res.append(p2)
        p2 += d
    return res


def get_all_antinodes(field, strict=True) -> Set[Point]:
    pairs = get_pairs(field)
    antinodes = set()
    for pair in pairs:
        antinodes = antinodes.union(get_antinodes(pair, Point(*get_dim(field)), strict))
    return antinodes


print(len(get_pairs(field)))
# print(get_antinodes(((2, 5), (3, 7)), get_dim(field)))
print(len(get_all_antinodes(field)))
print(len(get_all_antinodes(field, False)))
