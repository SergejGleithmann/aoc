from copy import copy
from functools import reduce
from typing import Self
import numpy as np

with open("aoc/2024/day20/resources/data.txt", "r") as file:
    data = file.readlines()

with open("aoc/2024/day20/resources/test.txt", "r") as file:
    data_test = file.readlines()


class Point(tuple[int, int]):
    def __add__(self, other: Self) -> Self:
        return Point(x + y for x, y in zip(self, other))

    def __sub__(self, other: Self) -> Self:
        return Point(x - y for x, y in zip(self, other))

    def __rmul__(self, other: int) -> Self:
        return Point(other * x for x in self)

    def __mod__(self, other: Self) -> Self:
        return Point(x % y for x, y in zip(self, other))

    def in_bounds(self, other: Self) -> bool:
        return 0 <= self[0] < other[0] and 0 <= self[1] < other[1]

    def __abs__(self):
        return sum([abs(x) for x in self])


class Map[X](list[list[X]]):
    def update(self, p: Point, value: X) -> None:
        self[p[1]][p[0]] = value

    def get(self, p: Point) -> X:
        return self[p[1]][p[0]]

    def dim(self):
        return Point((len(self[0]), len(self)))

    def __str__(self) -> str:
        return "\n".join(
            ["".join(map(lambda x: "#" if x is None else str(x), row)) for row in self]
        )


DIRS = (
    Point((1, 0)),
    Point((0, 1)),
    Point((-1, 0)),
    Point((0, -1)),
)


def parse_data(data):
    res = []
    for y, line in enumerate(data):
        line_out = []
        for x, c in enumerate(line.strip()):
            match c:
                case "#":
                    v = None
                case "S":
                    v = 0
                    start = Point((x, y))
                case "E":
                    v = -1
                    end = Point((x, y))
                case _:
                    v = -2

            line_out.append(v)
        res.append(line_out)
    return Map(res), start, end


def run(track, start, end):
    pos = start
    path = {start}
    v = track.get(pos)
    while end != pos:
        for d in DIRS:
            next_pos = pos + d
            vn = track.get(next_pos)
            if vn is not None and vn < 0:
                v += 1
                track.update(next_pos, v)
                pos = next_pos
                path.add(pos)
                break
    return path


def cheats(
    track: Map, p: Point, q: Point, dist: int, min_save: int, exact: bool
) -> set[tuple[Point, Point]]:
    if (
        ((d := abs(p - q) <= dist) and not exact) or (d == dist)
    ) and min_save <= track.get(q) - (track.get(p) + d):
        return 1
    return 0


def all_cheats(track, path: set[Point], dist, min_save, exact=True):
    res = 0
    for p in copy(path):
        for q in path:
            res += cheats(track, p, q, dist, min_save, exact)
        path.remove(p)
    return res


track, start, end = parse_data(data_test)
path = run(track, start, end)
print(track.get(end))
print(all_cheats(track, path, 2, 36))
print(all_cheats(track, path, 20, 76, exact=False))

track, start, end = parse_data(data)
path = run(track, start, end)
print(all_cheats(track, path, 2, 100))

print(all_cheats(track, path, 20, 100, exact=False))

""" r = []
for i in range(50):
    r.append(["."] * 50)
for v in get_vectors_disk(20):
    p = v + Point((25, 25))
    r[p[1]][p[0]] = "X"
r[25][25] = "#"

print("\n".join(["".join(l) for l in r]))
print(len(get_vectors_disk(20)), len(set(get_vectors_disk(20)))) """
